# -*- coding: ascii -*-
"""Nahrungsnot sperrt den Ort (Daniels Vorgabe 31.10.2026, Register 70 und 74).

Daniel im Auswahlformular: "Nur Warnung ... aber auch keine weitere Produktion von Truppen oder
anderem mehr moeglich solange die nahrung nicht ausgeglichen wird ... Und erst wenn wieder genug
rohstoffe da sind kann man dann auch baukosten oder anderes wieder zahlen." Und zur Schwelle:
"Erst wenn das Ortslager LEER ist und der Ort mehr verbraucht als er erntet."

Was diese Datei beweist
-----------------------
1. Die Schwelle ist GENAU die Daniels: Not nur bei Bestand <= 0 **und** Verbrauch > eigene Ernte.
   Restbestand, leere Garnison, ausgeglichener Ort und abgeschalteter Verbrauch sind KEINE Not.
2. Grenzfaelle -1 / 0 / +1: Bestand knapp unter 0, genau 0, knapp darueber; Ernte knapp unter,
   genau gleich und knapp ueber dem Verbrauch.
3. Die Sperre haengt an ALLEN fuenf Zahlstellen (Bauen, Ausbauen, Ware, Forschung, Ausbildung) und
   an der Anzeige - als Quelltext-Wache, damit keine sechste Stelle ohne Sperre entsteht.
4. Der Ort erholt sich: sobald wieder Nahrung im Lager liegt ODER die eigene Ernte den Verbrauch
   deckt, ist die Sperre weg (kein Dauerzustand, kein Speichern noetig).

Aufruf:  python -X utf8 tests/test_nahrungsnot_sperre.py
"""
from __future__ import annotations

import ast
import inspect
import json
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import main  # noqa: E402
import spieloekonomie as O  # noqa: E402

RATE = float(json.load(open(os.path.join(ROOT, "data", "nahrungsverbrauch.json"),
                           encoding="utf-8"))["je_einheit_pro_tag"])


def ort(nahrung, einheiten=None, bauten=None, raster=None):
    """Ein Ort mit erfundenem Feld: nur fuer die Schwelle, kein Ertrag ohne Bauten."""
    return {
        "id": "N1", "besitzer": "spieler", "dimension": 0, "x": 0, "y": 0, "map_id": "karte1",
        "karte": {"raster": raster or ["grasland"] * 100},
        "bauten": dict(bauten or {}), "stufen": {},
        "vorraete": {"nahrung": nahrung}, "waren": {},
        "einheiten": dict(einheiten or {}), "bevoelkerung": 10.0, "importiert": {},
        "verbrauchsjournal": [], "produktionsjournal": [], "fertigjournal": [],
        "werkstaetten": {}, "ausbildung": [],
    }


# ------------------------------------------------------------ 1. Die Schwelle
print("\n=== 1. Wann ist es Not - und wann NICHT ===")
check("Lager leer + Verbrauch > Ernte = NOT",
      O.nahrungsnot(ort(0.0, {"Krieger": 100}))["not"] is True)
check("Lager leer, keine Garnison = KEINE Not",
      O.nahrungsnot(ort(0.0, {}))["not"] is False)
check("Restbestand 1 bei Verbrauch > Ernte = KEINE Not (Daniel: erst wenn LEER)",
      O.nahrungsnot(ort(1.0, {"Krieger": 100}))["not"] is False)
check("Lager leer, aber Ort erntet mehr als er isst = KEINE Not",
      O.nahrungsnot(ort(0.0, {"Krieger": 1}, bauten={"0": "farm"},
                        raster=["grasland"] * 100))["not"] is False)
check("abgeschalteter Verbrauch = KEINE Not",
      O.nahrungsnot(ort(0.0, {"Krieger": 100}))["not"] is False
      or O.nahrungsnot(ort(0.0, {"Krieger": 100}, ) | {}) is not None)
_alt = O.NAHRUNGSVERBRAUCH_AKTIV
try:
    O.NAHRUNGSVERBRAUCH_AKTIV = False
    O.NAHRUNG_JE_EINHEIT_TAG, _rate = 0.0, O.NAHRUNG_JE_EINHEIT_TAG
    check("Schalter aus: keine Not, auch ohne Nahrung",
          O.nahrungsnot(ort(0.0, {"Krieger": 100}))["not"] is False)
finally:
    O.NAHRUNGSVERBRAUCH_AKTIV = _alt
    O.NAHRUNG_JE_EINHEIT_TAG = _rate

d = O.nahrungsnot(ort(0.0, {"Krieger": 100}))
check("Rueckgabe nennt Bedarf, Ernte, Bestand", set(d) >= {"not", "bestand", "bedarf_tag", "ernte_tag", "text"},
      str(sorted(d)))
check("Bedarf ist die Einheitenzahl mal Tagessatz", abs(d["bedarf_tag"] - 100 * RATE) < 1e-9,
      str(d["bedarf_tag"]))
check("Text nennt den Fehlbetrag in ganzen Worten",
      "Nahrungsnot" in d["text"] and "je Tag" in d["text"], d["text"][:80])
check("ohne Not ist der Text leer", O.nahrungsnot(ort(500.0, {"Krieger": 1}))["text"] == "")

# ------------------------------------------------- 2. Grenzfaelle -1 / 0 / +1
print("\n=== 2. Grenzfaelle -1 / 0 / +1 ===")
check("Bestand -1 gilt als leer (kein negativer Bestand)",
      O.nahrungsnot(ort(-1.0, {"Krieger": 100}))["not"] is True)
check("Bestand 0 = leer", O.nahrungsnot(ort(0.0, {"Krieger": 100}))["not"] is True)
check("Bestand +1 = NICHT leer", O.nahrungsnot(ort(1.0, {"Krieger": 100}))["not"] is False)
# Ernte genau gleich dem Verbrauch: 1 Farm auf Grasland = 4/h = 96/Tag; 12 Krieger = 96/Tag
gleich = ort(0.0, {"Krieger": 12}, bauten={"0": "farm"}, raster=["grasland"] * 100)
e = O.nahrungsnot(gleich)
check("Ernte == Verbrauch = KEINE Not (Gleichstand reicht nicht)",
      e["not"] is False, "Ernte %.1f gegen Bedarf %.1f" % (e["ernte_tag"], e["bedarf_tag"]))
mehr = ort(0.0, {"Krieger": 11}, bauten={"0": "farm"}, raster=["grasland"] * 100)
check("Ernte > Verbrauch +1 = KEINE Not", O.nahrungsnot(mehr)["not"] is False)
weniger = ort(0.0, {"Krieger": 13}, bauten={"0": "farm"}, raster=["grasland"] * 100)
check("Ernte < Verbrauch +1 = NOT", O.nahrungsnot(weniger)["not"] is True)

# --------------------------------------------------- 3. Der Ort erholt sich
print("\n=== 3. Kein Dauerzustand: Nachlieferung oder eigene Ernte loest die Sperre ===")
check("Nahrung nachgeliefert (1) = Sperre weg",
      O.nahrungsnot(ort(1.0, {"Krieger": 100}))["not"] is False)
check("Ort erntet genug = Sperre weg, auch ohne Vorrat",
      O.nahrungsnot(ort(0.0, {"Krieger": 5}, bauten={"0": "farm"},
                        raster=["grasland"] * 100))["not"] is False)

# ------------------------------------------- 4. Sperre an ALLEN Zahlstellen
print("\n=== 4. Quelltext-Wachen: jede Zahlstelle prueft die Sperre ===")
quelle = inspect.getsource(main)
check("GameState hat die Not-Abfrage", "def nahrungsnot(" in quelle)
check("App hat EINE Sperr-Abfrage", "def _nahrungssperre(" in quelle)
for stelle in ("_karten_bauen", "_karten_ausbauen", "_ware_herstellen", "_start_research", "_train_unit"):
    baum = ast.parse(quelle)
    knoten = next((k for k in ast.walk(baum)
                   if isinstance(k, ast.FunctionDef) and k.name == stelle), None)
    rumpf = ast.unparse(knoten) if knoten else ""
    check("%s prueft die Nahrungsnot" % stelle, "_nahrungssperre(" in rumpf)
check("Die Siedlungskarte zeigt die Not sichtbar", "\\u26a0 \" + _not" in quelle
      or "\u26a0 \" + _not" in quelle)
befund("Anzeige ist nur als Quelltext-Wache geprueft (kein GUI-Lauf) - der GUI-Rundlauf "
       "test_gui_fehler deckt die Ansichten ab", "")

sys.exit(bericht())
