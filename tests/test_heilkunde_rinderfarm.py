# -*- coding: ascii -*-
"""Heilkunde-Bonus und Rinderfarm-Ertrag: die zwei Fixes aus Register 105, umgesetzt 01.11.2026.

Wache fuer Register 118. Zwei belegte Originalregeln, die der Code vorher falsch las:

A. Heilkunde (Handbuch 2009, Abschnitt 5: "Siedlerproduktion +10 % je Stufe").
   `gebaeude_wirkung.siedler_zuwachs_pro_stunde` las den Schluessel SELBST in Kleinschreibung
   ("heilkunde"), waehrend data/research.json die Forschung "Heilkunde" nennt - der Bonus griff
   im Spiel NIE (gemessen 1,0 statt 1,5 Siedler je Stunde bei Stufe 5). Seit dem Fix kommt der
   Bonus aus `forschung_wirkung.siedlerfaktor`, der EINEN Quelle fuer Forschungsnamen und
   Prozentwert (F-04-Muster: eine Wahrheit fuer Kern UND Anzeige).

B. Rinderfarm (Handbuch 2009, Seite 10, woertlich: "Rinderfarm | Leder | Grasland
   (3 Nahrung, 3 Leder), Steppe (1,5 Nahrung, 1,5 Leder)"). Der Code lieferte 1/3 bzw. 0,5/1,5
   aus WeitereWerteKampfsystem.odt, S. 4. Daniels Entscheidung 01.11.2026: der 2009er Wert gilt.

Beide Zahlen werden hier aus den DATEN gelesen, nicht getippt - eine zweite Handliste waere die
naechste Wahrheit.
"""
from __future__ import annotations

import ast
import inspect
import json
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

import_src()
import forschung_wirkung as FW
import gebaeude_wirkung as GW
import gelaende as G
import spieloekonomie as O

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _daten(name):
    """Eine Datendatei aus data/ als JSON - eine Lesestelle fuer alle Pruefungen hier."""
    with open(os.path.join(WURZEL, "data", name), encoding="utf-8") as f:
        return json.load(f)


def _code(funktion):
    """Quelltext einer Funktion OHNE Docstring - Docstrings zaehlen nicht als Code."""
    baum = ast.parse(textwrap.dedent(inspect.getsource(funktion)))
    koerper = baum.body[0].body
    if koerper and isinstance(koerper[0], ast.Expr) and isinstance(koerper[0].value, ast.Constant):
        koerper = koerper[1:]
    baum.body[0].body = koerper
    return ast.unparse(baum)


# --------------------------------------------------------------------------
abschnitt("A. Heilkunde wirkt auf den Siedlerzuwachs (Register 105a/118)")

check("A1 ohne Forschung waechst 1 Siedler je Stunde und Siedlung",
      GW.siedler_zuwachs_pro_stunde(["a"]) == 1.0,
      str(GW.siedler_zuwachs_pro_stunde(["a"])))
check("A2 Heilkunde Stufe 5 ergibt 1,5 Siedler je Stunde (der Befund war 1,0)",
      GW.siedler_zuwachs_pro_stunde(["a"], {"Heilkunde": 5}) == 1.5,
      str(GW.siedler_zuwachs_pro_stunde(["a"], {"Heilkunde": 5})))
check("A3 Heilkunde Stufe 5 auf zwei Siedlungen ergibt 3,0",
      GW.siedler_zuwachs_pro_stunde(["a", "b"], {"Heilkunde": 5}) == 3.0,
      str(GW.siedler_zuwachs_pro_stunde(["a", "b"], {"Heilkunde": 5})))
check("A4 Stufe 0 und fehlende Stufe sind gleich (kein Sonderfall)",
      GW.siedler_zuwachs_pro_stunde(["a"], {"Heilkunde": 0})
      == GW.siedler_zuwachs_pro_stunde(["a"], {}))
check("A5 der alte Kleinbuchstaben-Schluessel wirkt NICHT (sonst kehrt der Befund zurueck)",
      GW.siedler_zuwachs_pro_stunde(["a"], {"heilkunde": 5}) == 1.0,
      str(GW.siedler_zuwachs_pro_stunde(["a"], {"heilkunde": 5})))
check("A6 ohne Siedlung waechst niemand",
      GW.siedler_zuwachs_pro_stunde([], {"Heilkunde": 10}) == 0.0)
check("A7 Stufe 10 (Deckel der Forschung) ergibt 2,0 je Siedlung",
      GW.siedler_zuwachs_pro_stunde(["a"], {"Heilkunde": 10}) == 2.0,
      str(GW.siedler_zuwachs_pro_stunde(["a"], {"Heilkunde": 10})))

check("A8 die Funktion rechnet ueber forschung_wirkung.siedlerfaktor (eine Rechenstelle)",
      "siedlerfaktor(" in _code(GW.siedler_zuwachs_pro_stunde), _code(GW.siedler_zuwachs_pro_stunde))
check("A9 sie liest den Schluessel NICHT mehr selbst",
      "heilkunde" not in _code(GW.siedler_zuwachs_pro_stunde).lower(),
      _code(GW.siedler_zuwachs_pro_stunde))

# Der Prozentwert steht an zwei Stellen (Datendatei = Beleg, forschung_wirkung = Rechnung).
# Diese Wache haelt beide gleich, sonst entsteht wieder eine zweite Wahrheit.
_json_prozent = _daten("gebaeude_wirkung.json")["bevoelkerung"]["heilkunde_prozent_je_stufe"]
_code_prozent = FW.belegte_faktoren()["siedler"]["prozent_je_stufe"]
check("A10 Datendatei und Rechenquelle nennen denselben Heilkunde-Prozentsatz",
      int(_json_prozent) == int(_code_prozent),
      "data/gebaeude_wirkung.json %s gegen forschung_wirkung %s" % (_json_prozent, _code_prozent))

# Die Anzeige muss DIESELBE Stufenkarte lesen wie der Kern (F-04-Muster).
with open(os.path.join(WURZEL, "src", "main.py"), encoding="utf-8") as f:
    _main = f.read()
check("A11 die Gebaeudewirkungs-Anzeige gibt die Forschungsstufen mit",
      "siedler_zuwachs_pro_stunde(self.state.settlements, _stufen)" in _main,
      "erwartet: Aufruf mit _stufen (= self.state.forschungs_stufen())")
check("A12 die Anzeige holt die Stufen aus der EINEN Lesestelle",
      "self.state.forschungs_stufen()" in _main)


# --------------------------------------------------------------------------
abschnitt("B. Rinderfarm liefert 3/3 auf Grasland und 1,5/1,5 auf Steppe (Register 105b/118)")

check("B1 Grasland: 3 Nahrung und 3 Leder",
      G.ertrag_pro_stunde("rinderfarm", "grasland") == {"Nahrung": 3, "Leder": 3},
      str(G.ertrag_pro_stunde("rinderfarm", "grasland")))
check("B2 Steppe: 1,5 Nahrung und 1,5 Leder",
      G.ertrag_pro_stunde("rinderfarm", "steppe") == {"Nahrung": 1.5, "Leder": 1.5},
      str(G.ertrag_pro_stunde("rinderfarm", "steppe")))

_farm = None
for _g in _daten("buildings.json")["gebaeude"]:
    if _g.get("id") == "rinderfarm":
        _farm = _g
check("B3 die Datendatei fuehrt die Rinderfarm ueberhaupt", _farm is not None)
if _farm:
    check("B4 die Abweichung nennt Handbuch 2009 Seite 10 als Quelle",
          "Seite 10" in str(_farm.get("abweichung")), str(_farm.get("abweichung"))[:120])
    check("B5 die Abweichung nennt die Entscheidung vom 01.11.2026",
          "01.11.2026" in str(_farm.get("abweichung")), str(_farm.get("abweichung"))[:120])
    check("B6 die Herkunft der alten Werte bleibt nachlesbar (nichts verschwiegen)",
          "WeitereWerteKampfsystem" in str(_farm.get("abweichung")), "")

# Der Nahrungsanteil ist von Forschungsboni ausgenommen - das ist eine eigene, unbelegte Regel.
_klasse = type("Dorf", (), {})
_d = _klasse()
_d.karte = {"raster": ["grasland", "grasland"], "spalten": 2, "zeilen": 1}
_d.bauten = {"0": "rinderfarm"}
_d.stufen = {}


def _ertrag_mit_forschung():
    """Rinderfarm auf Grasland mit Felderwirtschaft 5 und Tierhaltung 5.

    Tierhaltung hebt Leder (+5 % je Stufe), Felderwirtschaft wuerde Nahrung heben - beim
    Rinderfarm-Nahrungsanteil ist der Bonus aber ausgenommen (eigene Regel, siehe B8).
    """
    import wirtschaft as W
    return W.ertrag_gesamt([_d], {"Felderwirtschaft": 5, "Tierhaltung": 5})


_e = _ertrag_mit_forschung()
check("B7 Leder bekommt den Forschungsbonus (3 * 1,25 = 3,75)",
      _e.get("Leder") == 3.75, str(_e))
check("B8 Nahrung bleibt beim belegten Wert 3 (Ausnahme, offene Frage an Daniel)",
      _e.get("Nahrung") == 3, str(_e))


# --------------------------------------------------------------------------
abschnitt("C. Quellen der beiden Zahlen stehen im Register (Register 105/118)")

with open(os.path.join(WURZEL, "docs", "PRUEFREGEL_ORIGINAL.md"), encoding="utf-8") as f:
    _register = f.read()
check("C1 das Register nennt den Heilkunde-Befund", "siedlerfaktor" in _register)
check("C2 das Register nennt die Rinderfarm-Zahlen gegen Handbuch Seite 10",
      "Rinderfarm liefert 1 Nahrung statt 3" in _register)
check("C3 der umgesetzte Punkt ist als eigener Registerpunkt eingetragen",
      "| 118 |" in _register)

sys.exit(bericht())
