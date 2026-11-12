# -*- coding: ascii -*-
"""F-60: `dorfzentrum_kennzahlen` - die Oekonomie zaehlt, die Ansicht formatiert.

Daniels Entscheidung vom 12.11.2026 (F-60, Register 550): der Kopf des Dorfzentrums zeigt
Kennzahlen, die NICHT in der Ansicht gezaehlt werden. Die Zahlen kommen aus
`spieloekonomie.dorfzentrum_kennzahlen`; die Ansicht schreibt sie nur hin.

Was diese Datei beweist
-----------------------
1. LEERER ORT: alle Zaehlwerte 0, `waren_gesamt` und `rezepte_gesamt` kommen aus den DATEN
   (17 und 17 - hier von Hand als Sollwert, nicht im Code nachgeschlagen).
2. EINE WARE, EIN ROHSTOFF, EINE WERKSTATT: `vorraetig` = 1 und `herstellbar` = 1. Die Sollwerte
   stehen VON HAND hier - die Wache ruft `ware_grenzen` NICHT zum Vergleichen auf (das waere die
   Spiegelwache, Claudes Befund 4.4.1).
3. GEGENPROBE: dieselbe Ware auf 0 gesetzt -> `vorraetig` = 0; ohne Werkstatt vor Ort ->
   `herstellbar` = 0 (die Werkstatt ist Teil der Bedingung, Nachrechnung Nr. 16 Befund B3).
4. Zaehlweise: eine Ware, die nicht in `data/items.json` steht, zaehlt NICHT mit; Einheiten werden
   summiert und nach Arten gezaehlt; Textwerte im Bestand brechen nichts.
5. QUELLTEXT: die Funktion steht in `spieloekonomie` (Oekonomie) und liest die Warengrenze ueber
   `ware_grenzen` - es gibt keine zweite Rechnung.

Aufruf:  python -X utf8 tests/test_dorfzentrum_kennzahlen.py
"""
from __future__ import annotations

import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src, messwert

ROOT, SRC = import_src()
import spieloekonomie  # noqa: E402

OHNE_FORSCHUNG = {}


def kennzahlen(ort):
    return spieloekonomie.dorfzentrum_kennzahlen(ort, OHNE_FORSCHUNG)


# ==========================================================================
abschnitt("1. Leerer Ort: alles 0, die Summen kommen aus den Daten (17 / 17)")
# ==========================================================================
leer = kennzahlen({})
check("vorraetig = 0", leer["vorraetig"] == 0, str(leer["vorraetig"]))
check("herstellbar = 0", leer["herstellbar"] == 0, str(leer["herstellbar"]))
check("einheiten = 0", leer["einheiten"] == 0, str(leer["einheiten"]))
check("einheiten_arten = 0", leer["einheiten_arten"] == 0, str(leer["einheiten_arten"]))
check("waren_gesamt = 17 (aus data/items.json, nicht im Code)", leer["waren_gesamt"] == 17,
      str(leer["waren_gesamt"]))
check("rezepte_gesamt = 17 (aus data/warenrezepte.json)", leer["rezepte_gesamt"] == 17,
      str(leer["rezepte_gesamt"]))
check("ein fehlender Ort (None) bricht nicht", kennzahlen(None)["vorraetig"] == 0)
messwert("waren_gesamt", leer["waren_gesamt"], "Waren")
messwert("rezepte_gesamt", leer["rezepte_gesamt"], "Rezepte")

# ==========================================================================
abschnitt("2. Eine Ware, ein Rohstoff, eine Werkstatt: vorraetig 1, herstellbar 1")
# ==========================================================================
# Messer: Rezept {metall: 1}, keine Forschungsvoraussetzung, Werkstatt Schmiede. Der Ort hat genau
# EIN Metall im Lager - damit ist genau ein Rezept bezahlbar. Die Sollwerte sind von HAND gesetzt.
ort = {
    "name": "Pruef-Ort",
    "bauten": {"0": "schmiede"},           # die Werkstatt steht auf Feld 0
    "stufen": {"0": 1},
    "vorraete": {"metall": 1, "holz": 0, "wolle": 0, "leder": 0},
    "waren": {"Messer": 1},
    "einheiten": {},
}
eins = kennzahlen(ort)
check("vorraetig = 1 (nur das Messer liegt im Lager)", eins["vorraetig"] == 1,
      str(eins["vorraetig"]))
check("herstellbar = 1 (nur ein Metall im Lager, Schmiede steht)", eins["herstellbar"] == 1,
      str(eins["herstellbar"]))
check("waren_gesamt bleibt 17", eins["waren_gesamt"] == 17, str(eins["waren_gesamt"]))
messwert("kennzahl_vorraetig", eins["vorraetig"], "Waren")
messwert("kennzahl_herstellbar", eins["herstellbar"], "Waren")

# ==========================================================================
abschnitt("3. Gegenproben: Ware weg, Werkstatt weg, Rohstoff weg")
# ==========================================================================
ohne_ware = dict(ort)
ohne_ware["waren"] = {"Messer": 0}
check("Gegenprobe Ware: derselbe Ort mit Messer = 0 ergibt vorraetig = 0",
      kennzahlen(ohne_ware)["vorraetig"] == 0, str(kennzahlen(ohne_ware)["vorraetig"]))
ohne_werkstatt = dict(ort)
ohne_werkstatt["bauten"] = {}
check("Gegenprobe Werkstatt: ohne Schmiede vor Ort ist herstellbar = 0",
      kennzahlen(ohne_werkstatt)["herstellbar"] == 0,
      str(kennzahlen(ohne_werkstatt)["herstellbar"]))
ohne_metall = dict(ort)
ohne_metall["vorraete"] = {"metall": 0, "holz": 0, "wolle": 0, "leder": 0}
check("Gegenprobe Rohstoff: ohne Metall im Lager ist herstellbar = 0",
      kennzahlen(ohne_metall)["herstellbar"] == 0, str(kennzahlen(ohne_metall)["herstellbar"]))
# Die Forschung sperrt zusaetzlich: Dolch braucht Waffentechnik 1 - mit 2 Metall und ohne Forschung
# bleibt es bei genau dem Messer (1 Stueck Metall reicht; 2 Metall reichen fuer das Messer und
# nicht fuer den Dolch, weil die Forschung fehlt).
zwei_metall = dict(ort)
zwei_metall["vorraete"] = {"metall": 2, "holz": 0, "wolle": 0, "leder": 0}
check("Gegenprobe Forschung: 2 Metall ohne Waffentechnik ergibt weiter herstellbar = 1",
      kennzahlen(zwei_metall)["herstellbar"] == 1, str(kennzahlen(zwei_metall)["herstellbar"]))
mit_forschung = dict(zwei_metall)
_mit_f = spieloekonomie.dorfzentrum_kennzahlen(mit_forschung, {"Waffentechnik": 1})
check("mit Waffentechnik 1 und 2 Metall werden es 2 (Messer und Dolch)",
      _mit_f["herstellbar"] == 2, str(_mit_f["herstellbar"]))

# ==========================================================================
abschnitt("4. Zaehlweise: fremde Ware, Einheiten, kaputte Werte")
# ==========================================================================
fremd = dict(ort)
fremd["waren"] = {"Messer": 1, "Erfundene Ware": 5}
check("eine Ware ausserhalb von data/items.json zaehlt nicht mit",
      kennzahlen(fremd)["vorraetig"] == 1, str(kennzahlen(fremd)["vorraetig"]))
mit_einheiten = dict(ort)
mit_einheiten["einheiten"] = {"Krieger": 3, "Bogenschuetze": 2, "Kundschafter": 0}
_einh = kennzahlen(mit_einheiten)
check("einheiten = 5 (Summe)", _einh["einheiten"] == 5, str(_einh["einheiten"]))
check("einheiten_arten = 2 (nur Arten mit Bestand groesser 0)", _einh["einheiten_arten"] == 2,
      str(_einh["einheiten_arten"]))
kaputt = dict(ort)
kaputt["waren"] = {"Messer": "viel"}
kaputt["einheiten"] = {"Krieger": None}
_kaputt = kennzahlen(kaputt)
check("Textwerte im Warenlager brechen die Zaehlung nicht", _kaputt["vorraetig"] == 0,
      str(_kaputt["vorraetig"]))
check("leere Einheitenwerte zaehlen nicht", _kaputt["einheiten"] == 0, str(_kaputt["einheiten"]))

# ==========================================================================
abschnitt("5. Quelltext: die Rechnung steht in der Oekonomie, nicht in der Ansicht")
# ==========================================================================
_quelle = open(os.path.join(SRC, "spieloekonomie.py"), encoding="utf-8", errors="replace").read()
_ast = ast.parse(_quelle)
_funktionen = [k.name for k in ast.walk(_ast) if isinstance(k, ast.FunctionDef)]
check("spieloekonomie.dorfzentrum_kennzahlen ist vorhanden",
      "dorfzentrum_kennzahlen" in _funktionen)
_teil = _quelle[_quelle.find("def dorfzentrum_kennzahlen"):]
_teil = _teil[:_teil.find("\ndef ", 10)]
check("die Funktion ruft ware_grenzen (eine Rechenstelle, keine zweite)",
      "ware_grenzen(" in _teil, _teil.count("ware_grenzen(").__str__())
check("die Zahl der Waren kommt aus spieldaten.waren() und wird gezaehlt (kein Literal 17)",
      "spieldaten.waren()" in _teil and "len(alle_waren)" in _teil, "")
# Die Anzeige darf spaeter NICHT selbst zaehlen - der Quelltext der Ansicht wird hier noch nicht
# geprueft, weil es sie erst mit dem Dorfzentrum-Umbau gibt (Schritt 8 des Nachtplans).

bericht()
