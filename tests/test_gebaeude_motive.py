# -*- coding: ascii -*-
"""Gebaeudemotive auf der Siedlungskarte - Stand 02.11.2026 (Register 119).

Geschichte in zwei Saetzen: A-2 (Register 82) brachte acht aus dem Handbuch geschnittene Motive auf
die Karte, von denen nur drei belegt waren. Daniel hat am 02.11.2026 entschieden, dass die Karte die
**20 freigestellten C2-Motive** zeigt (`quelle_der_karte: "c2"`), weil diese alle zwanzig Gebaeude
abdecken und echte Transparenz haben. Die acht Handbuchmotive bleiben als Beleg und Rueckfallsatz in
`data/gebaeude_motive.json` stehen - nichts wird geloescht.

Was diese Datei beweist
-----------------------
1. Die Karte liest die 20 C2-Motive: `main.GEBAEUDE_MOTIVE` deckt GENAU die Gebaeude aus
   `data/buildings.json` ab (kein Motiv ohne Gebaeude, kein Gebaeude ohne Motiv).
2. Alle Motivdateien existieren, sind PNG mit Alphakanal (Farbtyp 6), 256 x 256 px.
3. Der Schalter `quelle_der_karte` entscheidet, welche Fassung gilt; auf "c2" stehen die
   Handbuchmotive NICHT mehr in der Karte.
4. Die Kachelrahmen (C2-Lieferung, 64 x 64 px) sind eingetragen, ihre Deckkraft ist eine Zahl in
   der Datendatei (Daniel kann sie ohne Codeaenderung aendern).
5. Ein Gebaeude ohne Motiv zeichnet weiter den Baukoerper: die Funktion liefert dann None.
6. Die Ausbaustufe bleibt bei Motiven sichtbar (Stufenpips), wie die Legende es verspricht.

Aufruf:  python -X utf8 tests/test_gebaeude_motive.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "quelltext"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['main:*']
PRUEF_DATEN = ['buildings.json', 'gebaeude_motive.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import main  # noqa: E402


def png_kopf(pfad):
    """(breite, hoehe, farbtyp) aus dem PNG-Kopf - ohne Fremdbibliothek.

    Farbtyp 6 = RGBA (mit Alphakanal), 2 = RGB ohne Transparenz.
    """
    with open(pfad, "rb") as f:
        kopf = f.read(26)                       # Signatur (8) + IHDR (8) + Masse (8) + Tiefe/Farbtyp (2)
    if kopf[:8] != b"\x89PNG\r\n\x1a\n":        # PNG-Signatur
        return None                             # kein PNG
    breite, hoehe = struct.unpack(">II", kopf[16:24])   # Masse aus dem IHDR-Block
    return breite, hoehe, kopf[25]              # Farbtyp steht im Byte 25


daten = json.load(open(os.path.join(ROOT, "data", "gebaeude_motive.json"), encoding="utf-8"))
handbuch = daten["motive"]                       # acht geschnittene Handbuchmotive (Beleg, Rueckfall)
c2 = daten.get("c2_motive") or []                # 20 freigestellte C2-Motive (gelten auf der Karte)
ids = {e["id"] for e in json.load(
    open(os.path.join(ROOT, "data", "buildings.json"), encoding="utf-8"))["gebaeude"]}

# ==========================================================================
abschnitt("1. Die Karte liest die 20 C2-Motive (Entscheidung Daniel 02.11.2026)")

check("1 der Schalter quelle_der_karte steht auf c2", daten.get("quelle_der_karte") == "c2",
      str(daten.get("quelle_der_karte")))
check("1 die Datendatei fuehrt genau 20 C2-Motive", len(c2) == 20, str(len(c2)))
check("1 die Karte kennt genau diese 20 Gebaeude",
      set(main.GEBAEUDE_MOTIVE) == {e["gebaeude"] for e in c2},
      str(sorted(main.GEBAEUDE_MOTIVE)))
check("1 jedes Gebaeude aus buildings.json hat ein Motiv", set(main.GEBAEUDE_MOTIVE) == ids,
      "fehlend: %s / zu viel: %s" % (sorted(ids - set(main.GEBAEUDE_MOTIVE)),
                                     sorted(set(main.GEBAEUDE_MOTIVE) - ids)))
check("1 kein Motiv ohne Gebaeude", {e["gebaeude"] for e in c2} <= ids, "")
check("1 die Liste nennt keine Dubletten", len({e["gebaeude"] for e in c2}) == len(c2), "")
check("1 die Handbuchmotive sind noch da (Beleg und Rueckfallsatz, nichts geloescht)",
      len(handbuch) == 8, str(len(handbuch)))
check("1 die Handbuchmotive stehen NICHT mehr in der Karte",
      not any(str(m.get("datei")) in main.GEBAEUDE_MOTIVE.values() for m in handbuch), "")


# ==========================================================================
abschnitt("2. Jede Motivdatei ist brauchbar und freigestellt")

for e in c2:
    name = e["gebaeude"]
    pfad = os.path.join(ROOT, str(e["datei"]).replace("/", os.sep))
    check(f"2 {name}: Datei liegt im Projekt", os.path.exists(pfad), str(e["datei"]))
    if not os.path.exists(pfad):
        continue
    kopf = png_kopf(pfad)
    check(f"2 {name}: ist ein PNG mit Alphakanal (Farbtyp 6)", kopf is not None and kopf[2] == 6,
          str(kopf))
    check(f"2 {name}: 256 x 256 px", kopf is not None and kopf[0] == 256 and kopf[1] == 256,
          str(kopf[:2] if kopf else kopf))
    check(f"2 {name}: als freigestellt gekennzeichnet", e.get("freigestellt") is True, "")


# ==========================================================================
abschnitt("3. Kachelrahmen sind eingetragen und in der Zeichnung angeschlossen")

rahmen = daten.get("kachelrahmen") or {}
for art in ("ruhe", "auswahl"):
    datei = str(rahmen.get(art) or "")
    pfad = os.path.join(ROOT, datei.replace("/", os.sep))
    check(f"3 Rahmen {art}: Pfad eingetragen", bool(datei) and datei.endswith(".png"), datei)
    check(f"3 Rahmen {art}: Datei liegt im Projekt", os.path.exists(pfad), pfad)
    if os.path.exists(pfad):
        kopf = png_kopf(pfad)
        check(f"3 Rahmen {art}: 64 x 64 px mit Alphakanal",
              kopf is not None and kopf[0] == 64 and kopf[1] == 64 and kopf[2] == 6, str(kopf))
check("3 die Deckkraft ist eine Zahl zwischen 0 und 100",
      isinstance(rahmen.get("deckkraft_prozent"), int) and 0 <= rahmen["deckkraft_prozent"] <= 100,
      str(rahmen.get("deckkraft_prozent")))
check("3 der Wert kommt wirklich aus der Datendatei (main.RAHMEN_DECKRAFT)",
      getattr(main, "RAHMEN_DECKRAFT", None) == rahmen.get("deckkraft_prozent"),
      str(getattr(main, "RAHMEN_DECKRAFT", None)))
check("3 main kennt beide Rahmenarten", set(getattr(main, "KACHELRAHMEN", {})) == {"ruhe", "auswahl"},
      str(sorted(getattr(main, "KACHELRAHMEN", {}))))

import inspect  # noqa: E402
quelle = inspect.getsource(main)
check("3 die Karte zeichnet die Rahmen je Feld", "_lade_kachelrahmen(" in quelle
      and "kachelrahmen" in quelle, "")
check("3 die Karte zeichnet das Motiv statt des Baukoerpers",
      "_lade_gebaeude_motiv(" in quelle and "create_image(" in quelle, "")
check("3 die Stufenpips werden beim Motiv gezeichnet", "_stufenpips_zeichnen(" in quelle, "")
check("3 der erfundene Baukoerper bleibt als Rueckfall erhalten",
      "gebaeude_baukasten_plan(" in quelle, "")
check("3 die Motivgroesse ist an die Kachel gebunden (nicht fest getippt)",
      "zelle * 0.7" in quelle, "")


# ==========================================================================
abschnitt("4. Ohne Motiv bleibt der gezeichnete Baukoerper")

app_klasse = main.NebelseetalApp


class _Leer:
    """Ein Objekt, das nur den Cache kennt - mehr braucht die Motivsuche im Fehlerfall nicht."""
    _motiv_cache = {}


_ergebnis = app_klasse._lade_gebaeude_motiv(_Leer(), "gibtesnicht")
check("4 ein Gebaeude ohne Motiv liefert None (kein Absturz)", _ergebnis is None, str(_ergebnis))
check("4 die Zuordnung ist eine geschlossene Liste (kein Platzhalterpfad)",
      all(p.startswith("assets/icons/gebaeude/") for p in main.GEBAEUDE_MOTIVE.values()),
      str(list(main.GEBAEUDE_MOTIVE.values())))

befund("Die Karte selbst wird hier nicht gezeichnet - die Vorschau "
       "docs/audits/kartenvergleich_c2_20261102.png und die GUI decken das Aussehen ab", "")

sys.exit(bericht())
