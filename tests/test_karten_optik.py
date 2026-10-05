"""
Pruefung der Zeichenplaene fuer die Siedlungskarte (src/karten_optik.py).

Die Plaene sind reine Daten — hier wird ohne Fenster geprueft, dass jede der sieben
Gelaendearten ein reiches Emblem bekommt, dass alle Koordinaten in der Zelle bleiben, dass
die Gebaeudezeichen sich nach Familie und Stufe unterscheiden und dass Wege und Raster die
richtige Zahl von Formen liefern. Nur der letzte Abschnitt braucht ein (unsichtbares) Fenster;
fehlt es, wird das als Befund gemeldet, nie still uebersprungen.

Aufruf:  python -X utf8 tests/test_karten_optik.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, befund, bericht, check, import_src

ROOT, SRC = import_src()
import gelaende as G
import karten_optik as KO

TERRAINS = G.GELAENDEARTEN
PIP = getattr(KO, "_PIP", "#F2C94C")


# --------------------------------------------------------------------------
# Testhilfen
# --------------------------------------------------------------------------

def koordinaten(plan: list[dict]):
    """Alle x- und y-Werte eines Plans (aus 'punkte', 'box' und 'punkt')."""
    xs: list = []
    ys: list = []
    for e in plan:
        if "punkte" in e:
            for k in range(0, len(e["punkte"]), 2):
                xs.append(e["punkte"][k])
                ys.append(e["punkte"][k + 1])
        if "box" in e:
            b = e["box"]
            xs += [b[0], b[2]]
            ys += [b[1], b[3]]
        if "punkt" in e:
            xs.append(e["punkt"][0])
            ys.append(e["punkt"][1])
    return xs, ys


def pips(plan: list[dict]) -> int:
    """Zahl der Stufen-Pips (kleine Rechtecke in der Pip-Farbe)."""
    return sum(1 for e in plan
               if e.get("form") == "rectangle" and e.get("farbe") == PIP)


# ==========================================================================
# 1. Gelaende-Embleme
# ==========================================================================

abschnitt("Gelaende-Embleme — jede der sieben Arten ist reicher als wenige Striche")

_plaene = {art: KO.emblem_plan(art, 0.0, 0.0, 64.0) for art in TERRAINS}
for art in TERRAINS:
    check(f"Emblem {art}: mindestens 4 Formen", len(_plaene[art]) >= 4,
          f"{len(_plaene[art])} Formen")

check("genau die sieben Gelaendearten aus gelaende.GELAENDEARTEN sind abgedeckt",
      set(KO._EMBLEME) == set(TERRAINS),
      str(sorted(set(KO._EMBLEME) ^ set(TERRAINS))))
check("wald hat mindestens 9 Formen (3 Baeume mit Krone und Stamm)",
      len(_plaene["wald"]) >= 9, f"{len(_plaene['wald'])} Formen")
check("jede Emblemform hat eine gueltige Zeichenform",
      all(e.get("form") in KO.FORMEN for art in TERRAINS for e in _plaene[art]),
      str(sorted({e.get("form") for art in TERRAINS for e in _plaene[art]} - set(KO.FORMEN))))
check("die Embleme sind deterministisch (zwei Aufrufe ergeben denselben Plan)",
      all(KO.emblem_plan(a, 0.0, 0.0, 64.0) == KO.emblem_plan(a, 0.0, 0.0, 64.0)
          for a in TERRAINS))

for z in (32, 48, 64, 96):
    _xs: list = []
    _ys: list = []
    for art in TERRAINS:
        x, y = koordinaten(KO.emblem_plan(art, 10.0, 20.0, float(z)))
        _xs += x
        _ys += y
    _ok = (min(_xs) >= 10.0 - 1.0 and max(_xs) <= 10.0 + z + 1.0
           and min(_ys) >= 20.0 - 1.0 and max(_ys) <= 20.0 + z + 1.0)
    check(f"Embleme bleiben bei {z} px in der Zelle (+-1 px Toleranz)", _ok,
          f"x {min(_xs):.1f}..{max(_xs):.1f}, y {min(_ys):.1f}..{max(_ys):.1f}")


# ==========================================================================
# 2. Rasterlinien
# ==========================================================================

abschnitt("Raster — (spalten+1) senkrechte und (zeilen+1) waagerechte Linien")

check("raster_plan(8, 5, 64) liefert 9 + 6 = 15 Linien",
      len(KO.raster_plan(8, 5, 64.0)) == 15,
      f"{len(KO.raster_plan(8, 5, 64.0))} Linien")
check("raster_plan(3, 2, 48) liefert 4 + 3 = 7 Linien",
      len(KO.raster_plan(3, 2, 48.0)) == 7,
      f"{len(KO.raster_plan(3, 2, 48.0))} Linien")
check("alle Rasterformen sind Linien mit Farbe und Breite",
      all(e["form"] == "line" and "farbe" in e and "breite" in e
          for e in KO.raster_plan(4, 4, 64.0)))
check("raster_plan ist deterministisch",
      KO.raster_plan(8, 5, 64.0) == KO.raster_plan(8, 5, 64.0))


# ==========================================================================
# 3. Wege zwischen bebauten Feldern
# ==========================================================================

abschnitt("Wege — nur orthogonale Nachbarschaft, ein Eintrag je Paar")

_w1 = KO.wege_plan({"0": "holzfaeller", "1": "haus"}, 8, 64.0)
check("zwei waagerecht benachbarte Felder ergeben genau einen Weg",
      len(_w1) == 1, f"{len(_w1)} Wege")
check("der Weg ist eine Linie durch den Kantenmittelpunkt (3 Punkte)",
      _w1 and _w1[0]["form"] == "line" and len(_w1[0]["punkte"]) == 6,
      str(_w1[0] if _w1 else None))
check("der Kantenmittelpunkt liegt auf der geteilten Kante (x = 64, y = 32)",
      _w1 and abs(_w1[0]["punkte"][2] - 64.0) < 1e-6 and abs(_w1[0]["punkte"][3] - 32.0) < 1e-6,
      str(_w1[0]["punkte"] if _w1 else None))
check("zwei nicht benachbarte Felder ergeben keinen Weg (0 und 2)",
      len(KO.wege_plan({"0": "haus", "2": "haus"}, 8, 64.0)) == 0)
check("Felder ueber den Zeilenumbruch sind nicht benachbart (7 und 8)",
      len(KO.wege_plan({"7": "haus", "8": "haus"}, 8, 64.0)) == 0)
check("senkrecht benachbarte Felder ergeben einen Weg (0 und 8)",
      len(KO.wege_plan({"0": "haus", "8": "haus"}, 8, 64.0)) == 1)
_w5 = KO.wege_plan({"0": "a", "1": "b", "8": "c"}, 8, 64.0)
check("drei Felder mit zwei Nachbarschaften ergeben zwei Wege (0-1, 0-8)",
      len(_w5) == 2, f"{len(_w5)} Wege")
check("die Wegefarbe ist ein Hexwert",
      all(str(e["farbe"]).startswith("#") for e in _w5))


# ==========================================================================
# 4. Gebaeudezeichen
# ==========================================================================

abschnitt("Gebaeude — Familien, Stufen-Pips und klare Fehler")

_keys = [g["id"] for g in json.load(
    open(os.path.join(ROOT, "data", "buildings.json"), encoding="utf-8"))["gebaeude"]]
check("data/buildings.json fuehrt genau 20 Originalgebaeude", len(_keys) == 20,
      f"{len(_keys)} Stueck")

_geb_plaene = ausnahme("gebaeude_plan fuer alle 20 Kennungen",
                       lambda: {k: KO.gebaeude_plan(k, 0.0, 0.0, 64.0) for k in _keys})
check("gebaeude_plan liefert fuer alle 20 Gebaeude einen Plan",
      bool(_geb_plaene) and len(_geb_plaene) == 20,
      f"{0 if _geb_plaene is None else len(_geb_plaene)} Plaene")
check("jedes Gebaeudezeichen hat mindestens 3 Formen",
      bool(_geb_plaene) and all(len(p) >= 3 for p in _geb_plaene.values()))

_s1 = KO.gebaeude_plan("kriegerakademie", 0.0, 0.0, 64.0, stufe=1, max_stufe=5)
_s3 = KO.gebaeude_plan("kriegerakademie", 0.0, 0.0, 64.0, stufe=3, max_stufe=5)
check("Stufe 3 zeichnet mehr Formen als Stufe 1 (max_stufe = 5)",
      len(_s3) > len(_s1), f"{len(_s1)} -> {len(_s3)}")
check("die Zahl der Pips ist min(stufe, max_stufe) = 3", pips(_s3) == 3, str(pips(_s3)))
check("Stufe 1 hat genau 1 Pip", pips(_s1) == 1, str(pips(_s1)))
check("ohne max_stufe (None) werden keine Pips gezeichnet",
      pips(KO.gebaeude_plan("haus", 0.0, 0.0, 64.0, stufe=1, max_stufe=None)) == 0)
check("ohne max_stufe ist der Plan kuerzer als mit",
      len(KO.gebaeude_plan("haus", 0.0, 0.0, 64.0, stufe=1, max_stufe=None))
      < len(KO.gebaeude_plan("haus", 0.0, 0.0, 64.0, stufe=1, max_stufe=5)))
check("eine Stufe ueber der Obergrenze wird gedeckelt (9 auf 5 Pips)",
      pips(KO.gebaeude_plan("verteidigungswall", 0.0, 0.0, 64.0, stufe=9, max_stufe=5)) == 5)

_familien = ["haus", "holzfaeller", "schmiede", "kriegerakademie",
             "verteidigungswall", "bibliothek"]
_finger = []
for _k in _familien:
    _finger.append(tuple(sorted(
        (str(e.get("form")), str(e.get("farbe")), str(e.get("rand")),
         str(e.get("box") or e.get("punkte"))) for e in KO.gebaeude_plan(_k, 0.0, 0.0, 64.0))))
check("die sechs Familien zeichnen sechs verschiedene Zeichen",
      len(set(_finger)) == 6, f"{len(set(_finger))} verschiedene")

check("gebaeude_plan ist deterministisch",
      KO.gebaeude_plan("holzfaeller", 0.0, 0.0, 64.0, stufe=2, max_stufe=5)
      == KO.gebaeude_plan("holzfaeller", 0.0, 0.0, 64.0, stufe=2, max_stufe=5))

_xa: list = []
_ya: list = []
for _k in _keys:
    x, y = koordinaten(KO.gebaeude_plan(_k, 5.0, 7.0, 64.0, stufe=5, max_stufe=5))
    _xa += x
    _ya += y
check("Gebaeudezeichen bleiben in der Zelle (+-1 px)",
      min(_xa) >= 5.0 - 1.0 and max(_xa) <= 5.0 + 64.0 + 1.0
      and min(_ya) >= 7.0 - 1.0 and max(_ya) <= 7.0 + 64.0 + 1.0,
      f"x {min(_xa):.1f}..{max(_xa):.1f}, y {min(_ya):.1f}..{max(_ya):.1f}")


def _unbekannt_geb():
    try:
        KO.gebaeude_plan("drache", 0.0, 0.0, 64.0)
        return None
    except ValueError as e:
        return str(e)


def _unbekannt_art():
    try:
        KO.emblem_plan("wueste", 0.0, 0.0, 64.0)
        return None
    except ValueError as e:
        return str(e)


_geb_fehl = _unbekannt_geb()
check("ein unbekanntes Gebaeude wirft einen klaren ValueError und nennt die Kennung",
      _geb_fehl is not None and "drache" in _geb_fehl, str(_geb_fehl))
_art_fehl = _unbekannt_art()
check("eine unbekannte Gelaendeart wirft einen klaren ValueError und nennt die Kennung",
      _art_fehl is not None and "wueste" in _art_fehl, str(_art_fehl))


# ==========================================================================
# 5. Format und offene Luecken
# ==========================================================================

abschnitt("Format — nur Hexfarben, keine Emoji, offene Luecken benannt")

_alle = [KO.emblem_plan(a, 0.0, 0.0, 64.0) for a in TERRAINS]
_alle += [KO.gebaeude_plan(k, 0.0, 0.0, 64.0, stufe=2, max_stufe=5) for k in _keys]
_alle += [KO.wege_plan({"0": "haus", "1": "holzfaeller"}, 8, 64.0)]
_alle += [KO.raster_plan(3, 3, 64.0)]
check("alle Farben sind Hexwerte (kein Emoji, kein Farbname)",
      all(str(e[k]).startswith("#") for plan in _alle for e in plan
          for k in ("farbe", "rand") if k in e))
check("kein Plan-Eintrag enthaelt Emoji oder Nicht-ASCII im Textfeld",
      all(not any(ord(c) > 127 for c in str(e.get("text", ""))) for plan in _alle for e in plan))
check("offene_luecken nennt mindestens eine Luecke als Text",
      isinstance(KO.offene_luecken(), list) and len(KO.offene_luecken()) >= 1
      and all(isinstance(s, str) and s.strip() for s in KO.offene_luecken()),
      f"{len(KO.offene_luecken())} Luecken")


# ==========================================================================
# 6. zeichne() auf einer unsichtbaren Leinwand (nur wenn moeglich)
# ==========================================================================

abschnitt("zeichne() — Zahl der gezeichneten Objekte entspricht der Planlaenge")

tk = None
_fehler = ""
try:
    import tkinter as tk
except Exception as e:           # noqa: BLE001 — jedes Fehlen von tkinter ist ein Befund
    _fehler = repr(e)

_root = None
if tk is not None:
    try:
        _root = tk.Tk()
        _root.withdraw()
    except Exception as e:       # noqa: BLE001 — kein Anzeigegeraet ist ein Befund
        _fehler = repr(e)
        _root = None

if _root is None:
    befund("zeichne() nicht pruefbar", f"kein Fenster/kein Anzeigegeraet: {_fehler}")
else:
    try:
        _leinwand = tk.Canvas(_root, width=200, height=200)
        for _art in TERRAINS:
            _plan = KO.emblem_plan(_art, 0.0, 0.0, 64.0)
            _n = KO.zeichne(_leinwand, _plan, tags=("probe",))
            check(f"zeichne() malt alle {len(_plan)} Emblemformen von {_art}",
                  _n == len(_plan), f"{_n} gezeichnet")
        _bplan = KO.gebaeude_plan("haus", 0.0, 0.0, 64.0, stufe=3, max_stufe=5)
        check("zeichne() malt alle Gebaeudeformen samt Pips",
              KO.zeichne(_leinwand, _bplan, tags=("probe",)) == len(_bplan))
        _wplan = KO.wege_plan({"0": "haus", "1": "holzfaeller"}, 8, 64.0)
        check("zeichne() malt den Wegeplan vollstaendig",
              KO.zeichne(_leinwand, _wplan) == len(_wplan))
        _rplan = KO.raster_plan(4, 3, 48.0)
        check("zeichne() malt den Rasterplan vollstaendig",
              KO.zeichne(_leinwand, _rplan) == len(_rplan))
    except Exception as e:       # noqa: BLE001
        befund("zeichne() nicht vollstaendig pruefbar", repr(e))
    finally:
        _root.destroy()


sys.exit(bericht())
