# -*- coding: ascii -*-
"""Prueft das Dezember-Bildpaket gegen seine Liste (18.11.2026, Sitzung 49).

WOZU
----
Daniel liefert 18 Bilddateien (acht Gruppen, F-101: 4x Anzeige). Dieses Werkzeug sagt ihm und mir
in EINEM Lauf, welche Datei fehlt, welche zu klein ist, welcher die Transparenz fehlt und welche
das falsche Format hat - damit keine Lieferung "irgendwie" eingebaut wird und keine Zahl geraten
werden muss.

DIE LISTE STEHT NICHT HIER
--------------------------
Die Soll-Werte (Groesse, Format, Alpha, Zielpfad) stehen in `data/bildpaket_dezember.json` - der
EINEN Quelle. Dieses Werkzeug liest die Datei nur und misst die Bilder.

GROESSEN OHNE PILLOW
--------------------
PNG und JPEG werden am Dateikopf gelesen (PNG: IHDR, JPEG: SOF-Marker). Damit laeuft die Pruefung
auch ohne Pillow, und ein abgeschnittenes Bild faellt auf (PNG ohne IEND, JPEG ohne FFD9).

AUFRUF
------
    python -X utf8 tools/bildpaket_pruefen.py            # Bericht, Rueckgabe 0
    python -X utf8 tools/bildpaket_pruefen.py --streng    # Rueckgabe 1, solange etwas fehlt
"""
from __future__ import annotations

import json
import os
import sys

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # Projektwurzel
LISTE = os.path.join(HIER, "data", "bildpaket_dezember.json")               # die EINE Quelle

_SOF_MARKER = (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,                    # JPEG: Rahmen-Kennungen
               0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF)                          # ohne DHT/JPG/DAC
_PNG_SIGNATUR = b"\x89PNG\r\n\x1a\n"                                        # PNG-Kennung, 8 Byte


def _png_lesen(daten: bytes):
    """(Breite, Hoehe, Alpha) einer PNG-Datei oder None, wenn der Kopf nicht passt.

    Alpha heisst: Farbtyp 4 (Grau + Alpha) oder 6 (RGBA) - nur dann gibt es echte Transparenz.
    """
    if not daten.startswith(_PNG_SIGNATUR) or len(daten) < 33:              # Kennung und IHDR pruefen
        return None                                                        # kein PNG
    if daten[12:16] != b"IHDR":                                            # erster Block muss IHDR sein
        return None                                                        # dann ist es kein lesbares PNG
    breite = int.from_bytes(daten[16:20], "big")                            # Breite in Bildpunkten
    hoehe = int.from_bytes(daten[20:24], "big")                             # Hoehe in Bildpunkten
    farbtyp = daten[25]                                                     # 0 Grau, 2 RGB, 3 Palette, 4 GA, 6 RGBA
    return breite, hoehe, farbtyp in (4, 6)                                 # Alpha nur bei 4 oder 6


def _jpeg_lesen(daten: bytes):
    """(Breite, Hoehe) einer JPEG-Datei oder None - ueber den SOF-Marker gelesen."""
    if not daten.startswith(b"\xff\xd8"):                                   # JPEG beginnt mit SOI
        return None                                                        # kein JPEG
    i = 2                                                                   # nach SOI weiterlaufen
    while i + 3 < len(daten):                                               # solange Bloecke folgen
        if daten[i] != 0xFF:                                                # Marker muessen mit FF beginnen
            i += 1                                                         # sonst weitersuchen
            continue                                                       # naechste Stelle
        marker = daten[i + 1]                                              # Markerkennung
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:                # Marker ohne Laenge
            i += 2                                                         # ueberspringen
            continue                                                       # naechster Block
        laenge = int.from_bytes(daten[i + 2:i + 4], "big")                  # Blocklaenge
        if marker in _SOF_MARKER:                                          # SOF traegt die Masse
            hoehe = int.from_bytes(daten[i + 5:i + 7], "big")               # Hoehe nach der Praezision
            breite = int.from_bytes(daten[i + 7:i + 9], "big")              # Breite danach
            return breite, hoehe                                            # fertig
        if laenge < 2:                                                      # kaputte Laenge
            return None                                                     # dann aufgeben
        i += 2 + laenge                                                     # naechsten Block anspringen
    return None                                                             # kein SOF gefunden


def bild_messen(pfad: str):
    """(Breite, Hoehe, Alpha, Format) einer Bilddatei - oder None, wenn sie nicht lesbar ist."""
    try:                                                                   # Datei kann fehlen
        with open(pfad, "rb") as fh:                                        # nur den Anfang lesen
            daten = fh.read()                                              # ganze Datei (Bilder sind klein genug)
    except OSError:                                                        # fehlt oder gesperrt
        return None                                                        # dann keine Messung
    png = _png_lesen(daten)                                                 # erst als PNG versuchen
    if png is not None:                                                     # passt der PNG-Kopf
        vollstaendig = b"IEND" in daten[-12:]                               # PNG endet mit IEND-Block
        return (png[0], png[1], png[2], "PNG") if vollstaendig else None     # abgeschnitten = nicht lesbar
    jpeg = _jpeg_lesen(daten)                                               # dann als JPEG versuchen
    if jpeg is not None:                                                    # passt der JPEG-Kopf
        vollstaendig = daten.rstrip(b"\x00").endswith(b"\xff\xd9")          # JPEG endet mit EOI
        return (jpeg[0], jpeg[1], False, "JPEG") if vollstaendig else None   # abgeschnitten = nicht lesbar
    return None                                                             # unbekanntes Format


def eintrag_pruefen(eintrag: dict, wurzel: str = "") -> dict:
    """Ein Eintrag der Liste gegen die Platte halten - Urteil und Begruendung zurueckgeben."""
    ziel = str(eintrag.get("ziel") or "")                                   # Zielpfad aus der Liste
    pfad = os.path.join(wurzel, ziel) if wurzel else os.path.join(HIER, ziel)  # Pfad auf der Platte
    soll = [int(x) for x in (eintrag.get("datei") or [0, 0])]                # Sollmasse aus der Liste
    ergebnis = {"nr": eintrag.get("nr"), "kennung": eintrag.get("kennung"),
                "ziel": ziel, "soll": soll, "ist": None, "urteil": "", "text": ""}
    if not os.path.exists(pfad):                                            # Datei fehlt
        ergebnis.update(urteil="fehlt", text="Datei nicht vorhanden")        # Urteil: fehlt
        return ergebnis                                                     # fertig
    gemessen = bild_messen(pfad)                                            # Bild messen, nicht schaetzen
    if gemessen is None:                                                    # unlesbar oder abgeschnitten
        ergebnis.update(urteil="kaputt", text="Datei ist kein vollstaendiges PNG/JPEG")
        return ergebnis                                                     # fertig
    breite, hoehe, hat_alpha, format_gemessen = gemessen                     # Messwerte
    ergebnis["ist"] = [breite, hoehe]                                       # Istmasse
    ergebnis["ist_alpha"] = hat_alpha                                       # Transparenz gemessen
    ergebnis["ist_format"] = format_gemessen                                # Format gemessen
    if breite < soll[0] or hoehe < soll[1]:                                 # kleiner als die Liste verlangt
        ergebnis.update(urteil="zu klein", text="%d x %d, verlangt %d x %d"
                        % (breite, hoehe, soll[0], soll[1]))                 # Urteil mit beiden Zahlen
        return ergebnis                                                     # fertig
    if bool(eintrag.get("alpha")) and not hat_alpha:                        # Transparenz fehlt
        ergebnis.update(urteil="kein Alpha", text="%s ohne Transparenz" % format_gemessen)
        return ergebnis                                                     # fertig
    format_soll = str(eintrag.get("format") or "").upper()                   # Sollformat, darf "JPG oder PNG" sein
    erlaubt = ["JPEG" if t.strip() == "JPG" else t.strip()                   # JPG und JPEG sind dasselbe Format
               for t in format_soll.replace("/", " oder ").split("oder") if t.strip()]
    if erlaubt and format_gemessen not in erlaubt:                           # falsches Format
        ergebnis.update(urteil="Format", text="%s geliefert, %s verlangt"
                        % (format_gemessen, " oder ".join(erlaubt)))          # Urteil mit beiden
        return ergebnis                                                     # fertig
    ergebnis.update(urteil="ok", text="vorhanden")                          # alles passt
    return ergebnis                                                         # fertig


def liste_lesen(pfad: str = LISTE) -> dict:
    """Die Bildliste lesen (die EINE Quelle der Sollwerte)."""
    with open(pfad, encoding="utf-8") as fh:                                # UTF-8 wie alle Spieldaten
        return json.load(fh)                                                # Inhalt als dict


def pruefung(wurzel: str = "", pfad: str = LISTE):
    """Alle Eintraege pruefen; Rueckgabe: (Ergebnisliste, Zusammenfassung)."""
    daten = liste_lesen(pfad)                                               # Sollwerte lesen
    bilder = daten.get("bilder") or []                                       # nur die Bilder
    ergebnisse = [eintrag_pruefen(e, wurzel) for e in bilder]                # jedes Bild einzeln messen
    zaehler = {}                                                             # Urteile zaehlen
    for e in ergebnisse:                                                     # je Ergebnis
        zaehler[e["urteil"]] = zaehler.get(e["urteil"], 0) + 1               # Urteil hochzaehlen
    zusammenfassung = {"gesamt": len(ergebnisse), "urteile": zaehler}        # Zusammenfassung bauen
    return ergebnisse, zusammenfassung                                       # beides zurueck


def main(argv=None) -> int:
    """Bericht auf der Konsole; Rueckgabe 0 (oder 1 mit --streng, solange nicht alles da ist)."""
    argv = list(sys.argv[1:] if argv is None else argv)                      # Aufrufargumente
    streng = "--streng" in argv                                             # strenger Modus?
    ergebnisse, zusammenfassung = pruefung()                                 # alles pruefen
    print("Dezember-Bildpaket - Pruefung gegen data/bildpaket_dezember.json")
    print("%-4s %-26s %-11s %-11s %-6s %s" % ("Nr", "Kennung", "Soll", "Ist", "Format", "Urteil"))
    for e in ergebnisse:                                                    # eine Zeile je Datei
        soll = "%d x %d" % (e["soll"][0], e["soll"][1])                      # Sollmasse als Text
        ist = "%d x %d" % (e["ist"][0], e["ist"][1]) if e.get("ist") else "-"  # Istmasse oder Strich
        print("%-4s %-26s %-11s %-11s %-6s %s" % (e["nr"], e["kennung"], soll, ist,
                                                  e.get("ist_format") or "-",
                                                  e["urteil"] + ((" (" + e["text"] + ")") if e["text"] else "")))
    z = zusammenfassung["urteile"]                                           # Zaehlung
    print("")
    print("Gesamt %d Dateien: %s" % (zusammenfassung["gesamt"],
                                     ", ".join("%s %d" % (k, v) for k, v in sorted(z.items()))))
    offen = zusammenfassung["gesamt"] - z.get("ok", 0)                       # was noch nicht passt
    print("Damit fehlen noch %d von %d Dateien." % (offen, zusammenfassung["gesamt"]))
    if offen and streng:                                                    # strenger Modus
        return 1                                                            # Rueckgabe 1
    return 0                                                                # sonst 0: der Bericht ist das Ergebnis


if __name__ == "__main__":
    sys.exit(main())
