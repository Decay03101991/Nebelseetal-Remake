# -*- coding: ascii -*-
"""Wache: das Dezember-Bildpaket ist vollstaendig beschrieben und wird GEMESSEN, nicht geschaetzt.

WARUM
-----
Daniel liefert im Dezember 18 Bilddateien in acht Gruppen (F-101: 4x Anzeige). Damit keine
Lieferung "irgendwie" eingebaut wird, gibt es eine EINE Liste der Sollwerte
(`data/bildpaket_dezember.json`) und ein Werkzeug, das die Platte misst
(`tools/bildpaket_pruefen.py`). Diese Wache haelt beide zusammen.

WAS DIESE DATEI PRUEFT
----------------------
1. Die Liste hat 18 Eintraege in den acht Gruppen (1 + 2 + 2 + 6 + 1 + 2 + 3 + 1) - die frueher
   genannte Zahl 16 war ein Zaehlfehler (18.11.2026 nachgerechnet).
2. Jede Sollgroesse stimmt mit dem Beschlussdokument ueberein (4x der groessten Anzeige).
3. Alle Zielpfade liegen unter `assets/`, sind eindeutig und nennen eine Endung.
4. Jede der drei Gruppen mit bereits fest eingetragenem Pfad (B8, B5, B13) passt zur jeweiligen
   Datendatei bzw. Konstante - die Liste erfindet keinen zweiten Ort.
5. Das Werkzeug MISST: mit erfundenen Bilddateien im Scratch meldet es "ok", "zu klein",
   "kein Alpha", "Format" und "kaputt" richtig; ohne Dateien meldet es fuer alle 18 "fehlt".
6. Farbtyp (18.11.2026): alpha true verlangt bei PNG Farbtyp 6, alpha false Farbtyp 2 - ein
   deckendes RGBA-Bild faellt damit auf. JPEG hat keinen PNG-Farbtyp.
7. Seitenverhaeltnis (18.11.2026): `toleranz_px` je Eintrag (0 bei B1/B2/B10/B12/B13, 1 bei
   B5/B8/B9), BEIDE Seiten geprueft; die Leisten-Endstuecke sind 8 : 17, die Mittelkachel 32 : 17.

Aufruf:  .venv/Scripts/python.exe -X utf8 tests/test_bildpaket_dezember.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ---------------- 
# Gelesen von harness.kopf_lesen und tools/auswahl.py.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['bildpaket_pruefen', 'bildpaket_dezember']
PRUEF_DATEN = ['bildpaket_dezember.json', 'portal_kopfbaender.json', 'drachen.json',
               'ressourcenleiste.json', 'gebaeude_motive.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import json
import os
import struct
import sys
import tempfile
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
sys.path.insert(0, os.path.join(ROOT, "tools"))
import bildpaket_pruefen as BP  # noqa: E402

# Sollwerte aus docs/BILDBEDARF_ENTSCHEIDUNGEN_20261113.md, Abschnitt 2 (Daniels Entscheidungen).
ERWARTET = [
    ("B1", "ruine_weltkarte", (176, 176), True),
    ("B2", "drache_gruen", (176, 176), True),
    ("B2", "drache_rot", (176, 176), True),
    ("B5", "startbild_anmelden", (4096, 2880), False),
    ("B5", "startbild_laden", (4096, 2880), False),
    ("B8", "kopfband_menschlich", (4508, 868), False),
    ("B8", "kopfband_zwergisch", (4508, 868), False),
    ("B8", "kopfband_elfisch", (4508, 868), False),
    ("B8", "kopfband_trolle", (4508, 868), False),
    ("B8", "kopfband_ghule", (4508, 868), False),
    ("B8", "kopfband_gnome", (4508, 868), False),
    ("B9", "weltkarte_goldrahmen", (3680, 3680), True),
    ("B10", "kachelrahmen_ruhe", (256, 256), True),
    ("B10", "kachelrahmen_auswahl", (256, 256), True),
    ("B12", "leiste_mitte", (256, 136), True),
    ("B12", "leiste_ende_links", (64, 136), True),
    ("B12", "leiste_ende_rechts", (64, 136), True),
    ("B13", "marktplatz_kennzeichen", (384, 384), False),
]


def png_schreiben(pfad: str, breite: int, hoehe: int, alpha: bool = True, kaputt: bool = False,
                  farbtyp: int = None) -> None:
    """Ein echtes, kleines PNG schreiben - damit gemessen und nicht ueber die Liste geraten wird.

    `farbtyp` ueberschreibt die Vorgabe aus `alpha`: 6 = RGBA, 2 = RGB, 4 = Grau+Alpha, 0 = Grau.
    Ohne Vorgabe gilt alpha true = 6, alpha false = 2. Die Bildpunkte werden deckend geschrieben
    (Alphakanal 255) - genau der Fall, den das Werkzeug frueher stillschweigend als "mit Alpha" las.
    """
    if farbtyp is None:                                                      # keine ausdrueckliche Vorgabe
        farbtyp = 6 if alpha else 2                                          # dann aus alpha ableiten
    kanaele = {0: 1, 2: 3, 4: 2, 6: 4}[farbtyp]                              # Bytes je Bildpunkt je Farbtyp
    punkt = bytes([90, 70, 40, 255][:kanaele])                               # ein Bildpunkt mit dieser Kanalzahl
    zeile = b"\x00" + punkt * breite                                         # Filterbyte + Punkte
    roh = zeile * hoehe                                                      # alle Zeilen untereinander
    komp = zlib.compress(roh, 1)                                             # schnell verdichten reicht

    def block(typ: bytes, daten: bytes) -> bytes:                            # ein PNG-Block mit CRC
        return (struct.pack(">I", len(daten)) + typ + daten
                + struct.pack(">I", zlib.crc32(typ + daten) & 0xFFFFFFFF))   # Laenge, Typ, Daten, Pruefsumme

    ihdr = struct.pack(">IIBBBBB", breite, hoehe, 8, farbtyp, 0, 0, 0)        # Kopfdaten des Bildes
    teile = [b"\x89PNG\r\n\x1a\n", block(b"IHDR", ihdr), block(b"IDAT", komp)]  # Kennung, Kopf, Daten
    if not kaputt:                                                           # heiles Bild
        teile.append(block(b"IEND", b""))                                    # Abschlussblock
    with open(pfad, "wb") as fh:                                             # Datei schreiben
        fh.write(b"".join(teile))                                            # alle Bloecke zusammen


def jpeg_schreiben(pfad: str, breite: int, hoehe: int) -> None:
    """Ein minimales JPEG-Gerippe (SOI, SOF0, EOI) - nur damit der Leser die Masse findet."""
    sof = (b"\xff\xc0" + struct.pack(">H", 11) + bytes([8])                  # Marker, Laenge, 8 Bit
           + struct.pack(">HH", hoehe, breite) + bytes([1, 1, 0x11, 0]))     # Hoehe, Breite, ein Kanal
    with open(pfad, "wb") as fh:                                             # Datei schreiben
        fh.write(b"\xff\xd8" + sof + b"\xff\xd9")                            # SOI + Rahmen + EOI


def liste_lesen():
    with open(os.path.join(ROOT, "data", "bildpaket_dezember.json"), encoding="utf-8") as fh:
        return json.load(fh)


def gruppen(bilder):
    """Nummer -> Anzahl, in der Reihenfolge des ersten Auftretens."""
    zaehler = {}
    for e in bilder:
        zaehler[e.get("nr")] = zaehler.get(e.get("nr"), 0) + 1
    return zaehler


def main() -> int:
    daten = liste_lesen()                                                    # die EINE Quelle lesen
    bilder = daten.get("bilder") or []                                       # nur die Bildliste

    abschnitt("1. Die Liste: 18 Dateien in acht Gruppen")
    check("die Liste hat 18 Eintraege", len(bilder) == 18, "gefunden %d" % len(bilder))
    z = gruppen(bilder)                                                      # Gruppen zaehlen
    check("die Gruppen zaehlen 1 / 2 / 2 / 6 / 1 / 2 / 3 / 1",
          z == {"B1": 1, "B2": 2, "B5": 2, "B8": 6, "B9": 1, "B10": 2, "B12": 3, "B13": 1}, str(z))
    check("die Liste nennt die Zaehlung selbst (18, nicht 16)",
          "18" in str(daten.get("_zaehlung") or ""), str(daten.get("_zaehlung"))[:60])

    abschnitt("2. Sollgroessen stimmen mit dem Beschlussdokument")
    ist = [(e.get("nr"), e.get("kennung"), tuple(e.get("datei") or ()), bool(e.get("alpha")))
           for e in bilder]
    check("Reihenfolge, Kennungen, Masse und Alpha wie beschlossen", ist == ERWARTET,
          str([x for x in zip(ist, ERWARTET) if x[0] != x[1]])[:200])

    abschnitt("3. Zielpfade: unter assets, eindeutig, mit Endung")
    ziele = [str(e.get("ziel") or "") for e in bilder]
    check("alle 18 Pfade liegen unter assets/", all(p.startswith("assets/") for p in ziele),
          str([p for p in ziele if not p.startswith("assets/")]))
    check("kein Pfad doppelt", len(set(ziele)) == len(ziele),
          "%d Pfade, %d verschieden" % (len(ziele), len(set(ziele))))
    check("jeder Pfad nennt .png oder .jpg",
          all(p.lower().endswith((".png", ".jpg")) for p in ziele),
          str([p for p in ziele if not p.lower().endswith((".png", ".jpg"))]))
    check("jeder Eintrag nennt Zweck, Motiv, Slot und Aktivierung",
          all(e.get("zweck") and e.get("motiv") and e.get("slot") and e.get("aktivierung") for e in bilder),
          str([e.get("kennung") for e in bilder
               if not (e.get("zweck") and e.get("motiv") and e.get("slot") and e.get("aktivierung"))]))

    abschnitt("4. Andockstellen: kein zweiter Ort fuer denselben Pfad")
    with open(os.path.join(ROOT, "data", "portal_kopfbaender.json"), encoding="utf-8") as fh:
        baender = json.load(fh)                                              # Kopfband-Zuordnung
    b8 = [e for e in bilder if e.get("nr") == "B8"]                          # die sechs Kopfbaender
    soll_b8 = sorted(baender.get("voelker", {}).values())                    # Pfade aus der Datendatei
    check("B8: die sechs Pfade stehen wortgleich in data/portal_kopfbaender.json",
          sorted(e["ziel"] for e in b8) == soll_b8,
          str(sorted(set(soll_b8) - set(e["ziel"] for e in b8)))[:150])

    with open(os.path.join(ROOT, "data", "gebaeude_motive.json"), encoding="utf-8") as fh:
        motive = json.load(fh).get("kachelrahmen") or {}                     # Rahmenblock
    check("B9 und B10: die Andockstelle kachelrahmen.weltkarte / .ruhe / .auswahl existiert",
          all(motive.get(k) for k in ("weltkarte", "ruhe", "auswahl")),
          str([k for k in ("weltkarte", "ruhe", "auswahl") if not motive.get(k)]))
    check("B9 und B10: die Liste zeigt auf NEUE Dateien (die alten bleiben als Quelle liegen)",
          all(e["ziel"] != motive.get(k) for e, k in
              (([e for e in bilder if e["kennung"] == "weltkarte_goldrahmen"][0], "weltkarte"),
               ([e for e in bilder if e["kennung"] == "kachelrahmen_ruhe"][0], "ruhe"),
               ([e for e in bilder if e["kennung"] == "kachelrahmen_auswahl"][0], "auswahl"))),
          "einer der neuen Pfade ist der alte")

    with open(os.path.join(ROOT, "data", "ressourcenleiste.json"), encoding="utf-8") as fh:
        leiste = json.load(fh).get("band") or {}                             # Bandbeschreibung
    check("B12: die Mittelkachel hat einen Slot (band.datei, heute leer)",
          "datei" in leiste and not str(leiste.get("datei") or "").strip(),
          "band.datei = %r" % (leiste.get("datei"),))
    enden = [e for e in bilder if e["kennung"].startswith("leiste_ende")]
    check("B12: die zwei Endstuecke nennen die Andockstelle band.ende_links / band.ende_rechts",
          len(enden) == 2 and all(e["slot"].startswith("vorhanden") for e in enden)
          and {"ende_links", "ende_rechts"} == set(k for e in enden for k in ("ende_links", "ende_rechts")
                                                   if k in e["aktivierung"]),
          str([e["slot"][:40] for e in enden]))
    check("B12: die Datendatei traegt die zwei Felder (heute leer, bis die Bilder kommen)",
          "ende_links" in leiste and "ende_rechts" in leiste
          and not str(leiste.get("ende_links") or "").strip(),
          str({k: leiste.get(k) for k in ("ende_links", "ende_rechts")}))

    import main as spiel                                                   # das Spiel selbst lesen
    check("B13: die Konstante MARKTPLATZ_KENNZEICHEN existiert und zeigt heute auf die 96er-Datei",
          "marktplatz_kennzeichen_96.png" in "/".join(spiel.MARKTPLATZ_KENNZEICHEN),
          "/".join(spiel.MARKTPLATZ_KENNZEICHEN))
    check("B5: STARTBILD_MOTIVE kennt 'anmelden' und 'laden'",
          set(("anmelden", "laden")) <= set(spiel.STARTBILD_MOTIVE), str(sorted(spiel.STARTBILD_MOTIVE)))
    with open(os.path.join(ROOT, "data", "drachen.json"), encoding="utf-8") as fh:
        drachen = json.load(fh)                                              # Drachenbestand
    check("B1: das Feld figur.ruine_bild existiert (leer = Platzhalter)",
          "ruine_bild" in (drachen.get("figur") or {}),
          str((drachen.get("figur") or {}).get("ruine_bild")))
    ids = {d.get("id") for d in (drachen.get("drachen") or [])}               # Kennungen der Drachen
    check("B2: drache_d03 (Tardas) und drache_d05 (Salmur) sind da", {"drache_d03", "drache_d05"} <= ids,
          str(sorted(ids)))

    abschnitt("5. Das Werkzeug MISST (erfundene Dateien im Scratch)")
    scratch = tempfile.mkdtemp(prefix="bildpaket_")                          # eigener Scratch-Ordner
    klein = {"bilder": [
        {"nr": "X1", "kennung": "passt", "datei": [8, 6], "format": "PNG", "alpha": True,
         "ziel": "a/passt.png", "zweck": "x", "motiv": "x", "slot": "x", "aktivierung": "x"},
        {"nr": "X2", "kennung": "zu_klein", "datei": [64, 64], "format": "PNG", "alpha": True,
         "ziel": "a/klein.png", "zweck": "x", "motiv": "x", "slot": "x", "aktivierung": "x"},
        {"nr": "X3", "kennung": "ohne_alpha", "datei": [8, 6], "format": "PNG", "alpha": True,
         "ziel": "a/rgb.png", "zweck": "x", "motiv": "x", "slot": "x", "aktivierung": "x"},
        {"nr": "X4", "kennung": "falsches_format", "datei": [8, 6], "format": "PNG", "alpha": False,
         "ziel": "a/bild.jpg", "zweck": "x", "motiv": "x", "slot": "x", "aktivierung": "x"},
        {"nr": "X5", "kennung": "abgeschnitten", "datei": [8, 6], "format": "PNG", "alpha": True,
         "ziel": "a/kaputt.png", "zweck": "x", "motiv": "x", "slot": "x", "aktivierung": "x"},
        {"nr": "X6", "kennung": "jpeg_passt", "datei": [8, 6], "format": "JPG", "alpha": False,
         "ziel": "a/passt.jpg", "zweck": "x", "motiv": "x", "slot": "x", "aktivierung": "x"},
    ]}
    liste_pfad = os.path.join(scratch, "liste.json")                         # eigene kleine Liste
    with open(liste_pfad, "w", encoding="utf-8") as fh:
        json.dump(klein, fh)                                                 # schreiben
    os.makedirs(os.path.join(scratch, "a"), exist_ok=True)                   # Zielordner
    png_schreiben(os.path.join(scratch, "a", "passt.png"), 8, 6, alpha=True)  # richtiges Bild
    png_schreiben(os.path.join(scratch, "a", "klein.png"), 32, 32, alpha=True)  # zu klein
    png_schreiben(os.path.join(scratch, "a", "rgb.png"), 8, 6, alpha=False)   # ohne Transparenz
    jpeg_schreiben(os.path.join(scratch, "a", "bild.jpg"), 8, 6)              # falsches Format
    png_schreiben(os.path.join(scratch, "a", "kaputt.png"), 8, 6, alpha=True, kaputt=True)  # ohne IEND
    jpeg_schreiben(os.path.join(scratch, "a", "passt.jpg"), 8, 6)            # richtiges JPEG

    ergebnisse, zusammenfassung = BP.pruefung(wurzel=scratch, pfad=liste_pfad)  # Werkzeug laufen lassen
    urteil = {e["kennung"]: e["urteil"] for e in ergebnisse}                  # Kennung -> Urteil
    check("sechs Eintraege geprueft", zusammenfassung["gesamt"] == 6, str(zusammenfassung))
    check("ein passendes PNG wird als 'ok' gemessen", urteil.get("passt") == "ok", str(urteil))
    check("ein passendes JPEG wird als 'ok' gemessen", urteil.get("jpeg_passt") == "ok", str(urteil))
    check("32 x 32 gegen 64 x 64 wird 'zu klein'", urteil.get("zu_klein") == "zu klein", str(urteil))
    check("RGB ohne Transparenz wird 'kein Alpha'", urteil.get("ohne_alpha") == "kein Alpha", str(urteil))
    check("JPEG gegen PNG-Soll wird 'Format'", urteil.get("falsches_format") == "Format", str(urteil))
    check("PNG ohne IEND wird 'kaputt'", urteil.get("abgeschnitten") == "kaputt", str(urteil))
    gemessen = BP.bild_messen(os.path.join(ROOT, "assets", "bilder", "drache_weiss.png"))  # echtes Bild
    check("ein vorhandenes Projektbild wird gelesen (PNG, Masse > 0)",
          gemessen is not None and gemessen[0] > 0 and gemessen[1] > 0 and gemessen[3] == "PNG",
          str(gemessen))

    abschnitt("6. Gegenprobe: leerer Bestand meldet 18 x 'fehlt'")
    leer = tempfile.mkdtemp(prefix="bildpaket_leer_")                        # nichts darin
    ergebnisse2, zusammenfassung2 = BP.pruefung(wurzel=leer)                 # gegen die ECHTE Liste
    check("18 Eintraege geprueft", zusammenfassung2["gesamt"] == 18, str(zusammenfassung2))
    check("alle 18 gelten als 'fehlt'", zusammenfassung2["urteile"] == {"fehlt": 18},
          str(zusammenfassung2["urteile"]))
    if zusammenfassung2["urteile"] != {"fehlt": 18}:                         # nur dann benennen
        befund("Bestand weicht von 'alles fehlt' ab",
               str([(e["kennung"], e["urteil"]) for e in ergebnisse2 if e["urteil"] != "fehlt"]))

    abschnitt("7. Farbtyp: alpha true verlangt 6, alpha false verlangt 2 (nur PNG)")
    typ_scratch = tempfile.mkdtemp(prefix="bildpaket_farbtyp_")              # eigener Scratch-Ordner
    typ_liste = {"bilder": [                                                 # fuenf kleine Faelle
        {"nr": "F1", "kennung": "rgba_richtig", "datei": [8, 6], "format": "PNG",
         "alpha": True, "ziel": "a/rgba.png"},
        {"nr": "F2", "kennung": "rgba_statt_rgb", "datei": [8, 6], "format": "PNG",
         "alpha": False, "ziel": "a/rgb_soll.png"},
        {"nr": "F3", "kennung": "grau_alpha", "datei": [8, 6], "format": "PNG",
         "alpha": True, "ziel": "a/grau.png"},
        {"nr": "F4", "kennung": "rgb_richtig", "datei": [8, 6], "format": "PNG",
         "alpha": False, "ziel": "a/rgb.png"},
        {"nr": "F5", "kennung": "jpeg_ohne_farbtyp", "datei": [8, 6], "format": "JPG oder PNG",
         "alpha": False, "ziel": "a/deckend.jpg"},
    ]}
    typ_pfad = os.path.join(typ_scratch, "liste.json")                       # eigene kleine Liste
    with open(typ_pfad, "w", encoding="utf-8") as fh:
        json.dump(typ_liste, fh)                                             # schreiben
    os.makedirs(os.path.join(typ_scratch, "a"), exist_ok=True)               # Zielordner
    rgba = os.path.join(typ_scratch, "a", "rgba.png")                        # RGBA, Punkte deckend
    png_schreiben(rgba, 8, 6, farbtyp=6)                                     # Farbtyp 6
    png_schreiben(os.path.join(typ_scratch, "a", "rgb_soll.png"), 8, 6, farbtyp=6)   # RGBA, obwohl deckend bestellt
    png_schreiben(os.path.join(typ_scratch, "a", "grau.png"), 8, 6, farbtyp=4)       # Grau + Alpha
    png_schreiben(os.path.join(typ_scratch, "a", "rgb.png"), 8, 6, farbtyp=2)        # RGB
    jpeg_schreiben(os.path.join(typ_scratch, "a", "deckend.jpg"), 8, 6)      # JPEG, kein Farbtyp
    typ_ergebnisse, _ = BP.pruefung(wurzel=typ_scratch, pfad=typ_pfad)        # Werkzeug laufen lassen
    typ_urteil = {e["kennung"]: e["urteil"] for e in typ_ergebnisse}          # Kennung -> Urteil
    check("PNG mit Farbtyp 6 gegen alpha true ist ok", typ_urteil.get("rgba_richtig") == "ok",
          str(typ_urteil))
    check("PNG mit Farbtyp 6 gegen alpha false (deckend bestellt) wird 'Farbtyp'",
          typ_urteil.get("rgba_statt_rgb") == "Farbtyp", str(typ_urteil))
    check("PNG mit Farbtyp 4 gegen alpha true wird 'Farbtyp' (6 verlangt)",
          typ_urteil.get("grau_alpha") == "Farbtyp", str(typ_urteil))
    check("PNG mit Farbtyp 2 gegen alpha false ist ok", typ_urteil.get("rgb_richtig") == "ok",
          str(typ_urteil))
    check("JPEG kennt keinen PNG-Farbtyp und bleibt ok", typ_urteil.get("jpeg_ohne_farbtyp") == "ok",
          str(typ_urteil))
    gemessen_rgba = BP.bild_messen(rgba)                                     # echte Messung des Farbtyps
    gemessen_jpg = BP.bild_messen(os.path.join(typ_scratch, "a", "deckend.jpg"))
    check("bild_messen nennt den Farbtyp als Zahl (6 bei RGBA, None bei JPEG)",
          gemessen_rgba is not None and gemessen_rgba[4] == 6
          and gemessen_jpg is not None and gemessen_jpg[4] is None,
          "%s / %s" % (gemessen_rgba, gemessen_jpg))

    abschnitt("8. Seitenverhaeltnis: 0 px bei B1/B2/B10/B12/B13, 1 px bei B5/B8/B9")
    beschluss_toleranz = {"B1": 0, "B2": 0, "B5": 1, "B8": 1, "B9": 1, "B10": 0, "B12": 0, "B13": 0}
    check("toleranz_px steht bei allen 18 Eintraegen und lautet wie beschlossen",
          all(e.get("toleranz_px") == beschluss_toleranz[e["nr"]] for e in bilder),
          str([(e["kennung"], e.get("toleranz_px")) for e in bilder
               if e.get("toleranz_px") != beschluss_toleranz[e["nr"]]]))
    check("die Toleranz-Regel steht auch im Kopf der Liste (keine stille Annahme)",
          "toleranz_px" in str(daten.get("_toleranz_regel") or ""),
          str(daten.get("_toleranz_regel"))[:80])
    check("ohne Feld gilt 0 und ein negativer Wert wird auf 0 gezogen",
          BP._toleranz({}) == 0 and BP._toleranz({"toleranz_px": -3}) == 0,
          "%d / %d" % (BP._toleranz({}), BP._toleranz({"toleranz_px": -3})))
    check("B12: das Endstueck 64 x 136 ist 8 : 17", 64 * 17 == 136 * 8,
          "%d gegen %d" % (64 * 17, 136 * 8))
    check("B12: die Mittelkachel 256 x 136 ist 32 : 17", 256 * 17 == 136 * 32,
          "%d gegen %d" % (256 * 17, 136 * 32))

    mass_scratch = tempfile.mkdtemp(prefix="bildpaket_masse_")               # Scratch fuer echte Sollmasse

    def _ziel(relativ: str) -> str:                                          # Pfad im Scratch anlegen
        pfad = os.path.join(mass_scratch, relativ)                            # Zielpfad laut Liste
        os.makedirs(os.path.dirname(pfad), exist_ok=True)                    # Ordner sicherstellen
        return pfad                                                          # Pfad zurueck

    def _urteil(kennung: str) -> str:                                        # Urteil EINER Kennung
        ergebnisse, _ = BP.pruefung(wurzel=mass_scratch)                     # gegen die ECHTE Liste
        return {e["kennung"]: e["urteil"] for e in ergebnisse}.get(kennung, "?")  # Kennung -> Urteil

    b1 = _ziel("assets/bilder/ruine_weltkarte_176.png")                      # B1, 176 x 176, 0 px
    png_schreiben(b1, 176, 176)                                             # exakt
    check("B1 mit genau 176 x 176 ist ok", _urteil("ruine_weltkarte") == "ok",
          _urteil("ruine_weltkarte"))
    png_schreiben(b1, 177, 176)                                             # ein Punkt zu breit
    check("B1 mit 177 x 176 wird 'zu gross' (0 px Toleranz)",
          _urteil("ruine_weltkarte") == "zu gross", _urteil("ruine_weltkarte"))
    png_schreiben(b1, 176, 175)                                             # ein Punkt zu flach
    check("B1 mit 176 x 175 wird 'zu klein'", _urteil("ruine_weltkarte") == "zu klein",
          _urteil("ruine_weltkarte"))
    b13 = _ziel("assets/bilder/marktplatz_kennzeichen_384.png")              # B13, 384 x 384, deckend
    png_schreiben(b13, 384, 384, farbtyp=2)                                  # RGB, deckend
    check("B13 mit 384 x 384 in RGB (Farbtyp 2) ist ok",
          _urteil("marktplatz_kennzeichen") == "ok", _urteil("marktplatz_kennzeichen"))
    b12 = _ziel("assets/bilder/leiste_ende_links_64x136.png")                # B12, Endstueck 8 : 17
    png_schreiben(b12, 64, 136)                                             # exakt
    check("B12: das Endstueck mit 64 x 136 ist ok", _urteil("leiste_ende_links") == "ok",
          _urteil("leiste_ende_links"))
    png_schreiben(b12, 65, 136)                                             # ein Punkt zu breit
    check("B12: 65 x 136 wird 'zu gross' (0 px Toleranz, sonst kippt 8 : 17)",
          _urteil("leiste_ende_links") == "zu gross", _urteil("leiste_ende_links"))
    b8 = _ziel("assets/bilder/portal_kopfband_menschlich_4508x868.png")      # B8, 4508 x 868, 1 px
    png_schreiben(b8, 4508, 869, farbtyp=2)                                 # deckend, ein Punkt mehr
    check("B8 mit 4508 x 869 ist ok (1 px Toleranz)", _urteil("kopfband_menschlich") == "ok",
          _urteil("kopfband_menschlich"))
    png_schreiben(b8, 4508, 870, farbtyp=2)                                 # deckend, zwei Punkte mehr
    check("B8 mit 4508 x 870 wird 'zu gross'", _urteil("kopfband_menschlich") == "zu gross",
          _urteil("kopfband_menschlich"))
    b5 = _ziel("assets/referenzbilder/startbild_anmelden_4096x2880.jpg")     # B5, 4096 x 2880, 1 px
    jpeg_schreiben(b5, 4096, 2881)                                          # ein Punkt mehr, JPEG
    check("B5 als JPEG mit 4096 x 2881 ist ok (1 px Toleranz, kein Farbtyp)",
          _urteil("startbild_anmelden") == "ok", _urteil("startbild_anmelden"))

    return bericht()                                                         # Zusammenfassung


if __name__ == "__main__":
    sys.exit(main())
