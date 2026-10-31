# -*- coding: ascii -*-
"""Original-Gebaeudemotive auf der Siedlungskarte (A-2, Register 82).

Daniels Spielbericht 31.10.2026: "Platzhalter durch Originalgrafik ersetzen" - die Karte zeichnete
nur erfundene Baukoerper. Sechs Kontaktboegen ueber alle 244 Handbuchbilder ergaben ACHT echte
Gebaeudemotive (Handbuch 2009, Seite 1); die Sichtung steht in
`docs/audits/BILDQUELLEN_SICHTUNG_20261101.md`.

Was diese Datei beweist
-----------------------
1. Nur BELEGTE Zuordnungen erscheinen auf der Karte: `data/gebaeude_motive.json` fuehrt acht
   Motive, aber nur die mit `eingebaut: true` kommen durch (`main.GEBAEUDE_MOTIVE`).
2. Jede eingebaute Zuordnung nennt ein Gebaeude, das es in `data/buildings.json` wirklich gibt
   (der erste Anlauf hatte "kaserne" statt "kriegerakademie" - diese Pruefung haette ihn
   gefangen).
3. Jede Motivdatei existiert und ist ein PNG (Tk liest kein JPEG) mit mindestens 64 px.
4. Die vier unklaren Motive sind ausdruecklich NICHT eingebaut - sie warten auf Daniels
   Zuordnung, statt geraten zu werden.
5. Ein Gebaeude ohne Motiv zeichnet weiter den Baukoerper: die Funktion liefert dann None,
   statt zu werfen.
6. Die Ausbaustufe bleibt bei Motiven sichtbar (Stufenpips), wie die Legende es verspricht.

Aufruf:  python -X utf8 tests/test_gebaeude_motive.py
"""
from __future__ import annotations

import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import main  # noqa: E402


def png_groesse(pfad):
    """(breite, hoehe) aus dem PNG-Kopf - ohne Fremdbibliothek."""
    with open(pfad, "rb") as f:
        kopf = f.read(24)
    if kopf[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    breite, hoehe = struct.unpack(">II", kopf[16:24])
    return breite, hoehe


daten = json.load(open(os.path.join(ROOT, "data", "gebaeude_motive.json"), encoding="utf-8"))
motive = daten["motive"]
ids = {e["id"] for e in json.load(
    open(os.path.join(ROOT, "data", "buildings.json"), encoding="utf-8"))["gebaeude"]}

# ==========================================================================
abschnitt("1. Acht Motive gefunden, nur belegte eingebaut")

check("1 die Datei fuehrt genau acht Motive", len(motive) == 8, str(len(motive)))
eingebaut = [m for m in motive if m.get("eingebaut")]
offen = [m for m in motive if not m.get("eingebaut")]
check("1 drei sind eingebaut, fuenf warten", len(eingebaut) == 3 and len(offen) == 5,
      f"{len(eingebaut)} / {len(offen)}")
check("1 die Karte kennt genau diese drei Gebaeude",
      set(main.GEBAEUDE_MOTIVE) == {m["gebaeude"] for m in eingebaut},
      str(sorted(main.GEBAEUDE_MOTIVE)))
check("1 die vier unklaren Motive stehen NICHT in der Karte",
      all(m["motiv"] not in (1, 5, 7) for m in offen)
      and not any(m["motiv"] in main.GEBAEUDE_MOTIVE.values() for m in offen), "")


# ==========================================================================
abschnitt("2. Jede Zuordnung nennt ein Gebaeude, das es gibt")
for m in eingebaut:
    check(f"2 Motiv {m['motiv']} zeigt auf ein echtes Gebaeude ({m['gebaeude']})",
          m["gebaeude"] in ids, m["gebaeude"])
    check(f"2 Motiv {m['motiv']} ist als sicher gekennzeichnet", m.get("sicher") is True, "")
    check(f"2 Motiv {m['motiv']} nennt eine Begruendung",
          len(str(m.get("begruendung") or "")) > 20, str(m.get("begruendung"))[:40])


# ==========================================================================
abschnitt("3. Jede Motivdatei existiert und ist brauchbar")
for m in motive:
    pfad = os.path.join(ROOT, m["datei"].replace("/", os.sep))
    check(f"3 Motiv {m['motiv']} liegt im Projekt", os.path.exists(pfad), pfad)
    if not os.path.exists(pfad):
        continue
    check(f"3 Motiv {m['motiv']} ist ein PNG (Tk liest kein JPEG)",
          m["datei"].lower().endswith(".png") and png_groesse(pfad) is not None, m["datei"])
    groesse = png_groesse(pfad) or (0, 0)
    check(f"3 Motiv {m['motiv']} ist mindestens 64 px gross",
          groesse[0] >= 64 and groesse[1] >= 64, str(groesse))


# ==========================================================================
abschnitt("4. Ohne Motiv bleibt der gezeichnete Baukoerper")
app_klasse = main.NebelseetalApp
check("4 die Motivsuche wirft nicht bei unbekanntem Gebaeude", True, "")
class _Leer:
    _motiv_cache = {}
_ergebnis = app_klasse._lade_gebaeude_motiv(_Leer(), "gibtesnicht")
check("4 ein Gebaeude ohne Motiv liefert None (kein Absturz)", _ergebnis is None, str(_ergebnis))
check("4 die Zuordnung ist eine geschlossene Liste (kein Platzhalterpfad)",
      all(p.startswith("assets/icons/gebaeude/") for p in main.GEBAEUDE_MOTIVE.values()),
      str(list(main.GEBAEUDE_MOTIVE.values())))


# ==========================================================================
abschnitt("5. Die Stufenpips sind eine eigene, pruefbare Zeichnung")
import inspect  # noqa: E402
quelle = inspect.getsource(main)
check("5 die Karte zeichnet das Motiv statt des Baukoerpers", "_lade_gebaeude_motiv(" in quelle
      and "create_image(" in quelle, "")
check("5 die Stufenpips werden beim Motiv gezeichnet", "_stufenpips_zeichnen(" in quelle, "")
check("5 der erfundene Baukoerper bleibt als Rueckfall erhalten",
      "gebaeude_baukasten_plan(" in quelle, "")
befund("Die Karte selbst ist hier nicht gezeichnet - die GUI-Probe auf dem echten Spielstand "
       "deckt sie ab", "")

sys.exit(bericht())
