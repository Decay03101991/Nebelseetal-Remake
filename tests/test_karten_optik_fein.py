"""
Pruefung der FEINEREN Zeichenplaene fuer die Siedlungskarte (src/karten_optik_fein.py).

Die Plaene sind reine Daten. Hier wird ohne Fenster geprueft, dass alle sieben Gelaendearten
mindestens vier Formen bekommen und im Feld bleiben, dass Wald reicher ist als Ebene, dass das
Uferband NUR an echten Wasser-Grenzen erscheint, dass Wege exakt an der Feldkante enden, dass
die goldene Auswahl im Feld bleibt, dass die Zahl der Stufenpips der Obergrenze entspricht, dass
die Koordinatenleiste die Ziffern traegt und dass alle Plaene deterministisch sind. Kein
tkinter, kein Fenster.

Aufruf:  python -X utf8 tests/test_karten_optik_fein.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import gelaende as G
import karten_optik_fein as KF

TERRAINS = list(G.GELAENDEARTEN)
GEBAEUDE = sorted(G.alle_gebaeude())
ZELLEN = (32, 48, 64, 96)

# Eine Kennung je Silhouettenfamilie fuer den Vergleich der sieben Familien.
FAMILIEN_VERTRETER = {
    "lager": "lager",
    "kaserne": "kriegerakademie",
    "produktion": "holzfaeller",
    "ausbildungsstaette": "diebesgilde",
    "wall": "verteidigungswall",
    "haus": "haus",
    "bibliothek": "bibliothek",
}


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


def hat_farbe(plan: list[dict], farbe: str) -> bool:
    """Traegt irgendein Eintrag diese Farbe (Fuellung oder Rand)?"""
    return any(e.get("farbe") == farbe or e.get("rand") == farbe for e in plan)


def fingerabdruck(plan: list[dict]):
    """Vergleichsform eines Plans fuer den Familienvergleich."""
    return tuple(sorted(
        (str(e.get("form")), str(e.get("farbe")), str(e.get("rand")),
         str(e.get("box") or e.get("punkte"))) for e in plan))


def kein_emoji(plan: list[dict]) -> bool:
    """Kein Text/Farbwert enthaelt ein Zeichen ab U+2500 (Zeichen-Emoji/Blockelemente)."""
    return all(ord(c) < 0x2500 for e in plan
               for k in ("text", "farbe", "rand") if k in e for c in str(e[k]))


def tuplify(richtungen: tuple) -> tuple:
    return tuple(richtungen)


# ==========================================================================
# 1. Gebaeude — Baukasten mit sieben Silhouettenfamilien
# ==========================================================================

abschnitt("Gebaeude — sieben Familien, Stufen nur als Pips, klare Fehler")

_plaene = {k: KF.gebaeude_baukasten_plan(k, 0.0, 0.0, 64.0) for k in GEBAEUDE}
check("alle 20 Gebaeude aus gelaende.alle_gebaeude() liefern einen Plan",
      len(_plaene) == len(GEBAEUDE) == 20, f"{len(_plaene)} Plaene")
check("jeder Gebaeudeplan hat mindestens 10 Formen",
      all(len(p) >= 10 for p in _plaene.values()),
      f"min {min(len(p) for p in _plaene.values())}")
check("jede Gebaeudeform hat eine gueltige Zeichenform",
      all(e.get("form") in KF.FORMEN for p in _plaene.values() for e in p),
      str(sorted({e.get("form") for p in _plaene.values() for e in p} - set(KF.FORMEN))))

_finger = {fam: fingerabdruck(KF.gebaeude_baukasten_plan(k, 0.0, 0.0, 64.0))
           for fam, k in FAMILIEN_VERTRETER.items()}
check("die sieben Silhouettenfamilien zeichnen sieben verschiedene Zeichen",
      len(set(_finger.values())) == 7, f"{len(set(_finger.values()))} verschiedene")
check("alle 20 Gebaeude sind einer der sieben Familien zugeordnet",
      set(KF._FAMILIE[k] for k in GEBAEUDE) <= set(KF.FAMILIEN),
      str(sorted(set(KF._FAMILIE[k] for k in GEBAEUDE) - set(KF.FAMILIEN))))

check("gebaeude_baukasten_plan ist deterministisch",
      KF.gebaeude_baukasten_plan("holzfaeller", 0.0, 0.0, 64.0, stufe=2, max_stufe=5)
      == KF.gebaeude_baukasten_plan("holzfaeller", 0.0, 0.0, 64.0, stufe=2, max_stufe=5))

_basis = KF.gebaeude_baukasten_plan("haus", 5.0, 7.0, 64.0, stufe=1, max_stufe=None)
_mit = KF.gebaeude_baukasten_plan("haus", 5.0, 7.0, 64.0, stufe=1, max_stufe=5)
check("ohne max_stufe kommt kein Pip und kein Streifen vor (kuerzerer Plan)",
      len(_mit) == len(_basis) + 1 + 5, f"{len(_basis)} -> {len(_mit)}")
check("stufe/max_stufe fuegen NUR die Pips an (Anfangsplan unveraendert)",
      _mit[:len(_basis)] == _basis)
check("ohne max_stufe ist gar kein Pip in der Pip-Farbe vorhanden",
      not hat_farbe(_basis, KF.PIP_FARBE))

_xa: list = []
_ya: list = []
for _k in GEBAEUDE:
    x, y = koordinaten(KF.gebaeude_baukasten_plan(_k, 5.0, 7.0, 64.0, stufe=3, max_stufe=5))
    _xa += x
    _ya += y
check("Gebaeudezeichen bleiben in der Zelle (+-1 px)",
      min(_xa) >= 5.0 - 1.0 and max(_xa) <= 5.0 + 64.0 + 1.0
      and min(_ya) >= 7.0 - 1.0 and max(_ya) <= 7.0 + 64.0 + 1.0,
      f"x {min(_xa):.1f}..{max(_xa):.1f}, y {min(_ya):.1f}..{max(_ya):.1f}")

for _z in ZELLEN:
    _xs: list = []
    _ys: list = []
    for _k in GEBAEUDE:
        x, y = koordinaten(KF.gebaeude_baukasten_plan(_k, 10.0, 20.0, float(_z),
                                                      stufe=3, max_stufe=5))
        _xs += x
        _ys += y
    check(f"Gebaeude bleiben bei {_z} px in der Zelle (+-1 px)",
          min(_xs) >= 10.0 - 1.0 and max(_xs) <= 10.0 + _z + 1.0
          and min(_ys) >= 20.0 - 1.0 and max(_ys) <= 20.0 + _z + 1.0,
          f"x {min(_xs):.1f}..{max(_xs):.1f}, y {min(_ys):.1f}..{max(_ys):.1f}")

try:
    KF.gebaeude_baukasten_plan("drache", 0.0, 0.0, 64.0)
    _geb_fehl = None
except ValueError as e:
    _geb_fehl = str(e)
check("ein unbekanntes Gebaeude wirft einen klaren ValueError und nennt die Kennung",
      _geb_fehl is not None and "drache" in _geb_fehl, str(_geb_fehl))
check("die Fehlermeldung listet die bekannten Kennungen auf",
      _geb_fehl is not None and "holzfaeller" in _geb_fehl)
check("kein Gebaeudeplan enthaelt Emoji/Blockzeichen in text/farbe/rand",
      all(kein_emoji(p) for p in _plaene.values()))


# ==========================================================================
# 2. Gelaende — sieben Arten, Ufer, unterdrueckte Innenkanten
# ==========================================================================

abschnitt("Gelaende — sieben Arten, Ufer nur an Wasser, gleiche Nachbarn ohne Innenkante")

_gel = {art: KF.gelaende_plan_fein(art, 0.0, 0.0, 64.0) for art in TERRAINS}
for art in TERRAINS:
    check(f"Gelaende {art}: mindestens 4 Formen", len(_gel[art]) >= 4,
          f"{len(_gel[art])} Formen")
check("genau die sieben Gelaendearten sind abgedeckt",
      set(KF._GELAENDE_DETAIL) == set(TERRAINS),
      str(sorted(set(KF._GELAENDE_DETAIL) ^ set(TERRAINS))))
check("Wald hat mehr Formen als Ebene (Grasland)",
      len(_gel["wald"]) > len(_gel["grasland"]),
      f"{len(_gel['wald'])} > {len(_gel['grasland'])}")

for _z in ZELLEN:
    _xs: list = []
    _ys: list = []
    for art in TERRAINS:
        x, y = koordinaten(KF.gelaende_plan_fein(art, 10.0, 20.0, float(_z)))
        _xs += x
        _ys += y
    check(f"Gelaendeformen bleiben bei {_z} px in der Zelle (+-1 px)",
          min(_xs) >= 10.0 - 1.0 and max(_xs) <= 10.0 + _z + 1.0
          and min(_ys) >= 20.0 - 1.0 and max(_ys) <= 20.0 + _z + 1.0,
          f"x {min(_xs):.1f}..{max(_xs):.1f}, y {min(_ys):.1f}..{max(_ys):.1f}")

check("jede Gelaendeform hat eine gueltige Zeichenform",
      all(e.get("form") in KF.FORMEN for p in _gel.values() for e in p))

_mit_wasser = KF.gelaende_plan_fein("grasland", 0.0, 0.0, 64.0, {"norden": "wasser"})
_ohne = KF.gelaende_plan_fein("grasland", 0.0, 0.0, 64.0)
_mit_wald = KF.gelaende_plan_fein("grasland", 0.0, 0.0, 64.0, {"norden": "wald"})
check("Uferband erscheint bei Wasser-Nachbarn", hat_farbe(_mit_wasser, KF.UFER_FARBE))
check("Uferband fehlt ohne Nachbarangabe", not hat_farbe(_ohne, KF.UFER_FARBE))
check("Uferband fehlt bei einem Wald-Nachbarn", not hat_farbe(_mit_wald, KF.UFER_FARBE))
check("die Uferfarbe ist das Astra-Band #999071", KF.UFER_FARBE == "#999071")
_alle_vier = KF.gelaende_plan_fein("grasland", 0.0, 0.0, 64.0,
                                   {"norden": "wasser", "osten": "wasser",
                                    "sueden": "wasser", "westen": "wasser"})
check("vier Wasser-Nachbarn ergeben vier Uferbaender",
      sum(1 for e in _alle_vier if e.get("farbe") == KF.UFER_FARBE) == 4,
      str(sum(1 for e in _alle_vier if e.get("farbe") == KF.UFER_FARBE)))
check("ein Wasserfeld bekommt selbst kein Uferband",
      not hat_farbe(KF.gelaende_plan_fein("nebelsee", 0.0, 0.0, 64.0, {"norden": "grasland"}),
                    KF.UFER_FARBE))

for art in TERRAINS:
    _nb = {r: art for r in KF.RICHTUNGEN}
    _diff = len(KF.gelaende_plan_fein(art, 0.0, 0.0, 64.0)) - len(
        KF.gelaende_plan_fein(art, 0.0, 0.0, 64.0, _nb))
    check(f"{art}: gleiche Nachbarn unterdruecken die vier Innenkanten",
          _diff == 4, f"{_diff} weniger Formen")

check("gelaende_plan_fein ist deterministisch",
      all(KF.gelaende_plan_fein(a, 0.0, 0.0, 64.0, {"norden": "wasser"})
          == KF.gelaende_plan_fein(a, 0.0, 0.0, 64.0, {"norden": "wasser"})
          for a in TERRAINS))

try:
    KF.gelaende_plan_fein("wueste", 0.0, 0.0, 64.0)
    _art_fehl = None
except ValueError as e:
    _art_fehl = str(e)
check("eine unbekannte Gelaendeart wirft einen klaren ValueError und nennt die Kennung",
      _art_fehl is not None and "wueste" in _art_fehl, str(_art_fehl))
check("kein Gelaendeplan enthaelt Emoji/Blockzeichen in text/farbe/rand",
      all(kein_emoji(p) for p in _gel.values()))


# ==========================================================================
# 3. Wege — ein Segment je Richtung, exakt bis an die geteilte Kante
# ==========================================================================

abschnitt("Wege — exakt an der Feldkante, zwei gespiegelte Felder schliessen an")

check("leeres Richtungstupel ergibt einen leeren Plan",
      KF.wegabschnitt_plan((), 0.0, 0.0, 64.0) == [])

_nord = KF.wegabschnitt_plan(("norden",), 0.0, 0.0, 64.0)
_ende = _nord[0]["punkte"][2:4]
check("der Nordabschnitt endet exakt auf der geteilten Kante (y == y0)",
      _nord and _ende[1] == 0.0, str(_ende))
check("der Nordabschnitt endet auf der Feldmitte (x == x0+zelle/2)",
      _nord and _ende[0] == 32.0, str(_ende[0]))
check("je Richtung entstehen zwei Linien (8 px Weg + 4 px Innenlinie)",
      len(_nord) == 2, f"{len(_nord)} Linien")
_alle = KF.wegabschnitt_plan(KF.RICHTUNGEN, 0.0, 0.0, 64.0)
check("vier Richtungen ergeben acht Linien", len(_alle) == 8, f"{len(_alle)} Linien")

_sued_a = KF.wegabschnitt_plan(("sueden",), 0.0, 0.0, 64.0)[0]["punkte"][2:4]
_nord_b = KF.wegabschnitt_plan(("norden",), 0.0, 64.0, 64.0)[0]["punkte"][2:4]
check("zwei gespiegelte Felder treffen sich exakt auf der gemeinsamen Kante",
      _sued_a == _nord_b == [32.0, 64.0], f"{_sued_a} / {_nord_b}")

_wege = KF.wegabschnitt_plan(("norden",), 0.0, 0.0, 64.0)
check("die Aussenlinie ist 8 px breit (#75674F)",
      _wege[0]["breite"] == 8.0 and _wege[0]["farbe"] == KF.WEG_FARBE,
      f"{_wege[0]['breite']} / {_wege[0]['farbe']}")
check("die Innenlinie ist 4 px breit (#A28E69)",
      _wege[1]["breite"] == 4.0 and _wege[1]["farbe"] == KF.WEG_INNEN_FARBE,
      f"{_wege[1]['breite']} / {_wege[1]['farbe']}")
check("wegabschnitt_plan ist deterministisch",
      KF.wegabschnitt_plan(KF.RICHTUNGEN, 0.0, 0.0, 64.0)
      == KF.wegabschnitt_plan(KF.RICHTUNGEN, 0.0, 0.0, 64.0))

try:
    KF.wegabschnitt_plan(("oben",), 0.0, 0.0, 64.0)
    _weg_fehl = None
except ValueError as e:
    _weg_fehl = str(e)
check("eine unbekannte Richtung wirft einen klaren ValueError", _weg_fehl is not None,
      str(_weg_fehl))

_weg_xs, _weg_ys = koordinaten(_alle)
check("Wege bleiben im Feld (+-1 px)",
      min(_weg_xs) >= -1.0 and max(_weg_xs) <= 65.0
      and min(_weg_ys) >= -1.0 and max(_weg_ys) <= 65.0,
      f"x {min(_weg_xs):.1f}..{max(_weg_xs):.1f}, y {min(_weg_ys):.1f}..{max(_weg_ys):.1f}")


# ==========================================================================
# 4. Auswahl und Stufenpips
# ==========================================================================

abschnitt("Auswahl und Pips — goldener Rahmen innen, Pips gleich der Obergrenze")

_auswahl = KF.auswahl_plan_fein(10.0, 20.0, 64.0)
check("der Auswahlrahmen hat mindestens 5 Eintraege", len(_auswahl) >= 5,
      f"{len(_auswahl)} Eintraege")
_ax, _ay = koordinaten(_auswahl)
check("der Auswahlrahmen bleibt im Feld (+-1 px)",
      min(_ax) >= 10.0 - 1.0 and max(_ax) <= 10.0 + 64.0 + 1.0
      and min(_ay) >= 20.0 - 1.0 and max(_ay) <= 20.0 + 64.0 + 1.0,
      f"x {min(_ax):.1f}..{max(_ax):.1f}, y {min(_ay):.1f}..{max(_ay):.1f}")
check("die dunkle Unterkontur ist #172128",
      hat_farbe(_auswahl, "#172128") and KF.AUSWAHL_UNTER_FARBE == "#172128")
check("das Gold der Auswahl ist #E4C77D",
      hat_farbe(_auswahl, "#E4C77D") and KF.AUSWAHL_GOLD == "#E4C77D")
check("der Auswahlrahmen ist deterministisch",
      KF.auswahl_plan_fein(0.0, 0.0, 64.0) == KF.auswahl_plan_fein(0.0, 0.0, 64.0))

_p5 = KF.stufenpips_plan(0.0, 0.0, 64.0, 3, 5)
check("die Zahl der Pips entspricht max_stufe (Streifen + 5 Quadrate)",
      len(_p5) - 1 == 5, f"{len(_p5) - 1} Pips")
check("ohne max_stufe ist der Pipplan leer",
      KF.stufenpips_plan(0.0, 0.0, 64.0, 3, None) == [])
check("genau die erreichte Stufe ist in Gold gefuellt",
      sum(1 for e in _p5 if e.get("farbe") == KF.PIP_FARBE) == 3,
      str(sum(1 for e in _p5 if e.get("farbe") == KF.PIP_FARBE)))
check("max_stufe 10 ergibt 10 Pips",
      len(KF.stufenpips_plan(0.0, 0.0, 64.0, 4, 10)) - 1 == 10)
_px, _py = koordinaten(_p5)
check("die Pips bleiben im Feld (+-1 px)",
      min(_px) >= -1.0 and max(_px) <= 65.0 and min(_py) >= -1.0 and max(_py) <= 65.0,
      f"x {min(_px):.1f}..{max(_px):.1f}, y {min(_py):.1f}..{max(_py):.1f}")


# ==========================================================================
# 5. Koordinatenleiste
# ==========================================================================

abschnitt("Koordinatenleiste — Ziffern in der 18 px breiten bzw. hohen Leiste")

_leiste = KF.koordinatenleiste_plan(8, 7, 64.0)
_texte = [e for e in _leiste if e.get("form") == "text"]
check("die Leiste traegt spalten+zeilen = 15 Ziffern", len(_texte) == 8 + 7,
      f"{len(_texte)} Texte")
check("alle Koordinatentexte sind Ziffern",
      all(str(e.get("text", "")).isdigit() for e in _texte))
check("die Leiste ist standardmaessig 18 px dick",
      KF.koordinatenleiste_plan(8, 7, 64.0, rand=18.0) == _leiste and KF.KOORDINATEN_BREITE == 18.0)
_oben = [e for e in _leiste if e.get("form") == "rectangle"
         and e.get("box")[0] == 18.0 and e.get("box")[1] == 0.0]
check("die obere Leiste ist rand hoch (18 px)",
      _oben and _oben[0]["box"][3] - _oben[0]["box"][1] == 18.0,
      str(_oben[0]["box"] if _oben else None))
check("die Koordinatenleiste ist deterministisch",
      KF.koordinatenleiste_plan(8, 7, 64.0) == KF.koordinatenleiste_plan(8, 7, 64.0))

# Die Siedlungskarte uebergibt die im Spiel ueblichen Buchstaben (main._spaltenname A-H), damit
# die Leiste und das Detailpanel dieselbe Koordinate nennen (Einhängen 05.10.2026).
_leiste_buchstaben = KF.koordinatenleiste_plan(8, 7, 64.0,
                                               spaltennamen=[chr(ord("A") + i) for i in range(8)],
                                               zeilennamen=[str(z + 1) for z in range(7)])
_buchstaben = [e.get("text") for e in _leiste_buchstaben if e.get("form") == "text"][:8]
check("spaltennamen ersetzen die Ziffern der Leiste (A-H)",
      _buchstaben == list("ABCDEFGH"), str(_buchstaben))
check("ohne spaltennamen bleibt es bei den Ziffern",
      [e.get("text") for e in KF.koordinatenleiste_plan(8, 7, 64.0)
       if e.get("form") == "text"][:3] == ["1", "2", "3"])
check("die Leiste hat mit Namen so viele Texte wie mit Ziffern",
      len([e for e in _leiste_buchstaben if e.get("form") == "text"]) == len(_texte))
try:
    KF.koordinatenleiste_plan(8, 7, 64.0, spaltennamen=["A", "B"])
    _kurz = None
except ValueError as _f:
    _kurz = str(_f)
check("eine zu kurze Namenliste wird abgelehnt statt still gemischt",
      _kurz is not None and "spaltennamen" in _kurz, str(_kurz))


# ==========================================================================
# 6. Farben, Format und offene Luecken
# ==========================================================================

abschnitt("Farben, Format und offene Luecken")

_f = KF.farben()
check("farben() liefert die Astra-Werte fuer Dach und Waende",
      _f.get("dach_hell") == "#875241" and _f.get("dach_dunkel") == "#59382F"
      and _f.get("wand_hell") == "#C0AD86" and _f.get("wand_dunkel") == "#8F795C",
      str({k: _f.get(k) for k in ("dach_hell", "dach_dunkel", "wand_hell", "wand_dunkel")}))
check("farben() liefert die vier Gelaendefarben aus dem Astra-Bericht",
      _f.get("ebene") == "#74805A" and _f.get("wald") == "#455E43"
      and _f.get("gebirge") == "#77776C" and _f.get("wasser") == "#416875")
check("farben() nennt Kontur, Bodenschatten, Ufer und Weg",
      _f.get("kontur") == "#302924" and _f.get("bodenschatten") == "#343B30"
      and _f.get("ufer") == "#999071" and _f.get("weg") == "#75674F"
      and _f.get("weg_innen") == "#A28E69")
check("offene_luecken nennt mindestens eine Luecke als Text",
      isinstance(KF.offene_luecken(), list) and len(KF.offene_luecken()) >= 1
      and all(isinstance(s, str) and s.strip() for s in KF.offene_luecken()),
      f"{len(KF.offene_luecken())} Luecken")

_alle_plaene = list(_gel.values()) + list(_plaene.values())
_alle_plaene += [KF.gebaeude_baukasten_plan(k, 0.0, 0.0, 64.0, stufe=3, max_stufe=5)
                 for k in GEBAEUDE]
_alle_plaene += [KF.wegabschnitt_plan(KF.RICHTUNGEN, 0.0, 0.0, 64.0),
                 KF.auswahl_plan_fein(0.0, 0.0, 64.0),
                 KF.stufenpips_plan(0.0, 0.0, 64.0, 3, 5),
                 KF.koordinatenleiste_plan(8, 7, 64.0),
                 KF.gelaende_plan_fein("grasland", 0.0, 0.0, 64.0, {"norden": "wasser"})]
check("alle Farben aller Plaene sind Hexwerte",
      all(str(e[k]).startswith("#") for plan in _alle_plaene for e in plan
          for k in ("farbe", "rand") if k in e))
check("kein Plan-Eintrag enthaelt Emoji/Blockzeichen in text/farbe/rand",
      all(kein_emoji(plan) for plan in _alle_plaene))
check("alle Plans sind Listen von dicts",
      all(isinstance(plan, list) and all(isinstance(e, dict) for e in plan)
          for plan in _alle_plaene))


sys.exit(bericht())
