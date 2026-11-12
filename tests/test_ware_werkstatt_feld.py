# -*- coding: ascii -*-
"""F-61/F-64: die Werkstatt steht am REZEPT - und stimmt mit der Ware ueberein.

Daniels Entscheidungen vom 12.11.2026 (Register 550/553):
  F-61  Werkstatt = Schmiede, Bogenbauer und alles, was Items fuer spaetere Truppen herstellt;
        Pferde, Wolle und Leder sind ROHSTOFFE, keine Werkstaetten.
  F-64  Die Zuordnung steht als Feld `werkstatt` je Rezept in `data/warenrezepte.json`
        (Gebaeude-Kennung).

Warum die Ableitung es schreibt (Befund B4 der Nachrechnung Nr. 16)
-------------------------------------------------------------------
Die Zuordnung existierte schon: `data/items.json` fuehrt je Ware ein Feld `werkstatt`, und
`src/werkstatt.py` liest NUR diese eine Stelle (`werkstatt_fuer`). Ein von Hand eingetragenes Feld
in `warenrezepte.json` haette eine ZWEITE Liste erzeugt - und `test_warenrezepte` waere rot
geworden, weil die Datei stueckweise der frischen Ableitung entsprechen muss. Darum schreibt
`tools/warenrezepte_ableiten.py` das Feld jetzt mit: eine Quelle (`items.json`), zwei Ansichten
(Ware und Rezept).

Was diese Datei beweist
-----------------------
1. Jedes der 17 Rezepte traegt `werkstatt`, und der Wert ist eine Gebaeude-Kennung
   (schmiede / bogenbauer / naehstube - klein, wie in `data/buildings.json`).
2. Die Zahlen stimmen mit Daniel's Aufteilung: Schmiede 8, Naehstube 5, Bogenbauer 4.
3. BEIDE SEITEN STIMMEN UEBEREIN: Rezept-Feld == `werkstatt.werkstatt_fuer(ware)` fuer alle 17 -
   ohne Ausnahme, in beide Richtungen.
4. Kein Rohstoff ist eine Werkstatt: Pferde, Wolle und Leder stehen NICHT als Wert im Feld.
5. Die eingefrorene Datei ist weiterhin gleich der frischen Ableitung (kein Handeintrag).

Aufruf:  python -X utf8 tests/test_ware_werkstatt_feld.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['warenrezepte_ableiten', 'werkstatt']
PRUEF_DATEN = ['items.json', 'warenrezepte.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src, messwert

ROOT, SRC = import_src()
import werkstatt  # noqa: E402

sys.path.insert(0, os.path.join(ROOT, "tools"))
import warenrezepte_ableiten as W  # noqa: E402

with open(os.path.join(ROOT, "data", "warenrezepte.json"), encoding="utf-8") as fh:
    REZEPTE = json.load(fh)
with open(os.path.join(ROOT, "data", "items.json"), encoding="utf-8") as fh:
    WAREN = json.load(fh)["waren"]

KENNUNGEN = {"schmiede", "bogenbauer", "naehstube"}

# ==========================================================================
abschnitt("1. Jedes Rezept traegt eine Werkstatt-Kennung")
# ==========================================================================
check("es sind 17 Rezepte", len(REZEPTE) == 17, str(len(REZEPTE)))
_ohne = sorted(n for n, r in REZEPTE.items() if "werkstatt" not in (r or {}))
check("kein Rezept ohne Feld `werkstatt`", not _ohne, str(_ohne))
_falsch = sorted(n for n, r in REZEPTE.items() if (r or {}).get("werkstatt") not in KENNUNGEN)
check("jeder Wert ist eine Gebaeude-Kennung (klein, keine Anzeigenamen)", not _falsch, str(_falsch))
check("kein Anzeigename als Wert (Schmiede/Bogner/Naehstube waeren falsch)",
      not any((r or {}).get("werkstatt") in ("Schmiede", "Bogner", "N\u00e4hstube")
              for r in REZEPTE.values()), "")

# ==========================================================================
abschnitt("2. Die Aufteilung ist 8 / 5 / 4")
# ==========================================================================
_zaehlung = {}
for rezept in REZEPTE.values():
    fach = (rezept or {}).get("werkstatt")
    _zaehlung[fach] = _zaehlung.get(fach, 0) + 1
check("Schmiede 8", _zaehlung.get("schmiede") == 8, str(_zaehlung.get("schmiede")))
check("Naehstube 5", _zaehlung.get("naehstube") == 5, str(_zaehlung.get("naehstube")))
check("Bogenbauer 4", _zaehlung.get("bogenbauer") == 4, str(_zaehlung.get("bogenbauer")))
messwert("werkstatt_schmiede", _zaehlung.get("schmiede"), "Rezepte")
messwert("werkstatt_naehstube", _zaehlung.get("naehstube"), "Rezepte")
messwert("werkstatt_bogenbauer", _zaehlung.get("bogenbauer"), "Rezepte")

# ==========================================================================
abschnitt("3. BEIDE SEITEN STIMMEN UEBEREIN (Rezept gegen Ware, alle 17)")
# ==========================================================================
_abweichend = []
for ware in sorted(REZEPTE):
    aus_rezept = (REZEPTE[ware] or {}).get("werkstatt")
    aus_ware = werkstatt.werkstatt_fuer(ware)
    if aus_rezept != aus_ware:
        _abweichend.append((ware, aus_rezept, aus_ware))
check("Rezept-Feld == werkstatt_fuer(ware) fuer alle 17 Waren", not _abweichend, str(_abweichend))
check("auch die Gegenrichtung ist still: jede Ware aus items.json hat ein Rezept",
      set(WAREN) == set(REZEPTE), str(sorted(set(WAREN) ^ set(REZEPTE))))

# ==========================================================================
abschnitt("4. Rohstoffe sind keine Werkstaetten (F-61)")
# ==========================================================================
for rohstoff in ("Pferde", "Wolle", "Leder"):
    check("%s ist kein Werkstatt-Wert" % rohstoff,
          rohstoff not in {str((r or {}).get("werkstatt")) for r in REZEPTE.values()}, rohstoff)

# ==========================================================================
abschnitt("5. Kein Handeintrag: die Datei ist gleich der frischen Ableitung")
# ==========================================================================
_frisch = W.rezepte_ableiten()
check("data/warenrezepte.json == frische Ableitung (kein Handeintrag)",
      _frisch == REZEPTE,
      str({n: (r, REZEPTE.get(n)) for n, r in _frisch.items() if REZEPTE.get(n) != r})[:300])
check("die Ableitung schreibt das Feld selbst (kein Nachtrag von Hand)",
      all((r or {}).get("werkstatt") for r in _frisch.values()), "")
_messer = _frisch.get("Messer") or {}
check("Messer entsteht in der Schmiede", _messer.get("werkstatt") == "schmiede",
      str(_messer.get("werkstatt")))
check("Kurzbogen entsteht beim Bogenbauer",
      (_frisch.get("Kurzbogen") or {}).get("werkstatt") == "bogenbauer",
      str((_frisch.get("Kurzbogen") or {}).get("werkstatt")))
check("Wollumhang entsteht in der Naehstube",
      (_frisch.get("Wollumhang") or {}).get("werkstatt") == "naehstube",
      str((_frisch.get("Wollumhang") or {}).get("werkstatt")))

bericht()
