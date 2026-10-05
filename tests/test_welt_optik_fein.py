"""
Prueft die FEINEREN Zeichenplaene der WELTkarte (src/welt_optik_fein.py) OHNE Fenster.

Grundlage sind die astra-Zahlen aus docs/audits/ux_astra_karten_feinheit_2026-10-05.txt
(Abschnitte Welt 1/2/3). Geprueft werden: die sechs Gelaendezeichen (Formenzahl, Lage in der
Zelle, Determinismus, Nachbarkanten, Ufersaum, Zoomstufen, ValueError), die drei Ortsilhouetten,
die Fahne, die goldene Auswahl, die Regionsbeschriftung mit Schatten, die 4-px-Uebersichtskarte
und die Panelmaße. Kein tkinter, kein Fenster.

Aufruf:  python -X utf8 tests/test_welt_optik_fein.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import welt_optik_fein as F

ARTEN = ("forest", "plains", "mountain", "water", "village", "ruins")
ZOLL = 1.0   # erlaubter Ueberstand in px


# --------------------------------------------------------------------------
# Testhilfen
# --------------------------------------------------------------------------

def _xy_alle(plan):
    """Alle x- und y-Koordinaten eines Plans als getrennte Listen."""
    xs, ys = [], []
    for e in plan:
        if "box" in e:
            b = e["box"]
            xs += [b[0], b[2]]
            ys += [b[1], b[3]]
        if "punkte" in e:
            p = e["punkte"]
            xs += list(p[0::2])
            ys += list(p[1::2])
        if "punkt" in e:
            xs.append(e["punkt"][0])
            ys.append(e["punkt"][1])
    return xs, ys


def _in_zelle(plan, x0, y0, zelle, toll=ZOLL) -> bool:
    """Liegen ALLE Koordinaten im Zellenkasten (mit Toleranz toll)?"""
    xs, ys = _xy_alle(plan)
    return (all(x0 - toll <= v <= x0 + zelle + toll for v in xs)
            and all(y0 - toll <= v <= y0 + zelle + toll for v in ys))


def _formen(plan):
    return [e["form"] for e in plan]


def _nur_hex(plan) -> bool:
    """Jede gesetzte Fuell-/Randfarbe beginnt mit '#'."""
    for e in plan:
        for schluessel in ("farbe", "rand"):
            if schluessel in e and not str(e[schluessel]).startswith("#"):
                return False
    return True


def _hat_emoji(plan) -> bool:
    """Sucht Emoji in allen Textfeldern (Umlaute sind erlaubt, Emoji nicht)."""
    bereiche = ((0x1F300, 0x1FAFF), (0x2600, 0x27BF), (0x1F000, 0x1F2FF),
                (0x2190, 0x21FF), (0xFE00, 0xFE0F), (0x2B00, 0x2BFF))
    for e in plan:
        for wert in e.values():
            if isinstance(wert, str):
                for ch in wert:
                    if any(a <= ord(ch) <= b for a, b in bereiche):
                        return True
    return False


def _kanten_namen(plan, schluessel):
    return {e.get(schluessel) for e in plan if schluessel in e}


def _saum(plan):
    return [e for e in plan if "ufersaum" in e]


# ==========================================================================
# 1. Modul und Konstanten
# ==========================================================================

abschnitt("Modul — die neun oeffentlichen Funktionen")

for _name in ("gelaende_plan_fein", "ortsilhouette_plan", "fahne_plan_fein", "auswahl_plan_fein",
              "regionen_plan_fein", "uebersicht_plan_fein", "zoom_detail", "detail_masse",
              "offene_luecken"):
    check(f"Funktion {_name}() vorhanden", callable(getattr(F, _name, None)))

check("sechs Gelaendearten der Weltkarte", tuple(F.GELAENDEARTEN) == ARTEN, str(F.GELAENDEARTEN))
check("Grundmass 48 px ist gesetzt (astra: 'bei 48 px')", F.MASS_PX == 48.0, str(F.MASS_PX))

abschnitt("Konstanten — astra-Zahlen verbatim")

check("Welt 1: Grundfarben wie astra",
      (F.WELT1_EBENE, F.WELT1_WALD, F.WELT1_GEBIRGE, F.WELT1_WASSER)
      == ("#707B58", "#405A43", "#75766F", "#405F70"))
check("Welt 1: Rasterlinie 1 px in #38433C",
      F.WELT1_RASTER == "#38433C" and F.WELT1_RASTER_BREITE == 1)
check("Welt 1: drei Lichtfarben wie astra",
      (F.WELT1_LICHT_GRUEN, F.WELT1_LICHT_GEBIRGE, F.WELT1_LICHT_WASSER)
      == ("#637451", "#96958A", "#658594"))
# Vorgabe Daniel 05.10.2026: der Wald bekommt eine EIGENE, aus seiner Grundfarbe GERECHNETE
# Lichtfarbe — astra nennt nur drei Lichtfarben fuer vier Gelaendearten.
check("Welt 1: der Wald hat eine eigene Lichtfarbe (getrennt von der Ebene)",
      F.WELT1_LICHT_WALD != F.WELT1_LICHT_GRUEN and F.WELT1_LICHT_WALD.startswith("#")
      and len(F.WELT1_LICHT_WALD) == 7, f"{F.WELT1_LICHT_WALD} gegen {F.WELT1_LICHT_GRUEN}")
check("Welt 1: die Wald-Lichtfarbe ist aus der Wald-Grundfarbe gerechnet (heller, nicht gleich)",
      F.WELT1_LICHT_WALD != F.WELT1_WALD
      and all(int(F.WELT1_LICHT_WALD[i:i + 2], 16) > int(F.WELT1_WALD[i:i + 2], 16)
              for i in (1, 3, 5)), f"{F.WELT1_WALD} -> {F.WELT1_LICHT_WALD}")
check("Welt 1: der Ableitungsfaktor liegt im Bereich der astra-Paare (0.15 bis 0.30)",
      0.15 <= F.LICHT_ABLEITUNG_FAKTOR <= 0.30, str(F.LICHT_ABLEITUNG_FAKTOR))
check("Welt 1: die Wald-Lichtfarbe steht im Plan der Waldgruppen, das astra-Gruen nicht",
      any(e.get("farbe") == F.WELT1_LICHT_WALD for e in F.gelaende_plan_fein("forest", 0.0, 0.0, 48.0))
      and not any(e.get("farbe") == F.WELT1_LICHT_GRUEN
                  for e in F.gelaende_plan_fein("forest", 0.0, 0.0, 48.0)))
check("Welt 1: Ufersaum-Band #938A70, 2–3 px",
      F.WELT1_UFER == "#938A70" and (F.WELT1_UFER_MIN, F.WELT1_UFER_MAX) == (2, 3))
check("Welt 2: Ortsfarben wie astra",
      (F.WELT2_WAND, F.WELT2_DACH, F.WELT2_RUINE, F.WELT2_KONTUR)
      == ("#B9A582", "#81503F", "#969083", "#292B27"))
check("Welt 2: Fahne (Sockel #356D98, Mast #D8D3BD, Fahne #F2EEDB)",
      (F.WELT2_SOCKEL, F.WELT2_MAST, F.WELT2_FAHNE) == ("#356D98", "#D8D3BD", "#F2EEDB"))
check("Welt 2: Regionsfarbe #D7CEB4 mit Schatten #26312B, 18 px, 1 px Versatz",
      F.WELT2_REGION_FARBE == "#D7CEB4" and F.WELT2_REGION_SCHATTEN == "#26312B"
      and F.WELT2_REGION_SCHRIFT == 18 and F.WELT2_REGION_VERSATZ == 1)
check("Welt 3: Auswahl gold #E4C77D, 2 px eingerueckt, 6 px Eckwinkel",
      F.WELT3_AUSWAHL_GOLD == "#E4C77D" and F.WELT3_AUSWAHL_EINRUECKUNG == 2
      and F.WELT3_AUSWAHL_ECKE == 6)
check("Welt 3: Uebersicht 4 x 4 px je Weltfeld", F.WELT3_UEBERSICHT_KACHEL == 4)
check("Welt 3: Sichtrahmen weiss 1 px #F2EEDB",
      F.WELT3_SICHT_RAHMEN == "#F2EEDB" and F.WELT3_SICHT_RAHMEN_BREITE == 1)


# ==========================================================================
# 2. Zoomstufen
# ==========================================================================

abschnitt("zoom_detail — drei Stufen (astra Welt 2)")

check("zoom_detail(16) == 'einfach'", F.zoom_detail(16) == "einfach")
check("zoom_detail(24) == 'einfach'", F.zoom_detail(24) == "einfach")
check("zoom_detail(32) == 'reduziert'", F.zoom_detail(32) == "reduziert")
check("zoom_detail(48) == 'voll'", F.zoom_detail(48) == "voll")
check("zoom_detail(64) == 'voll'", F.zoom_detail(64) == "voll")
check("zoom_detail(96) == 'voll'", F.zoom_detail(96) == "voll")


# ==========================================================================
# 3. Gelaendezeichen (Welt 1)
# ==========================================================================

abschnitt("Gelaendezeichen — Formenzahl (astra: 4–11, Wald bis 14)")

for _art in ARTEN:
    _p = F.gelaende_plan_fein(_art, 40.0, 70.0, 48.0)
    _max = F.WELT1_BEFEHLE_WALD_MAX if _art == "forest" else F.WELT1_BEFEHLE_MAX
    check(f"{_art}: Formenzahl zwischen {F.WELT1_BEFEHLE_MIN} und {_max}",
          F.WELT1_BEFEHLE_MIN <= len(_p) <= _max, f"{len(_p)} Formen")

_alle = {a: F.gelaende_plan_fein(a, 0.0, 0.0, 48.0) for a in ARTEN}
check("alle Formen stammen aus dem erlaubten Satz",
      all(f in F.FORMEN for p in _alle.values() for f in _formen(p)))
check("alle Farben sind Hex-Werte", all(_nur_hex(p) for p in _alle.values()))
check("keine Emoji in den Gelaendeplaenen",
      all(not _hat_emoji(p) for p in _alle.values()))
check("Gelaendeflaeche ist die erste Form (Fuellfarbe wie astra)",
      all(p[0]["form"] == "rectangle" and p[0].get("farbe") for p in _alle.values()))

abschnitt("Gelaendezeichen — alle Koordinaten in der Zelle (Toleranz 1 px)")

for _zelle in (24, 32, 48, 64, 96):
    _treffer = all(_in_zelle(F.gelaende_plan_fein(a, 40.0, 70.0, float(_zelle)), 40.0, 70.0,
                             float(_zelle)) for a in ARTEN)
    check(f"alle sechs Gelaendezeichen liegen bei zelle={_zelle} in der Zelle", _treffer)

# Mit Ufersaum: Landfeld mit Wassernachbar und Wasserfeld mit Landnachbarn.
_bz = [F.gelaende_plan_fein("plains", 40.0, 70.0, 48.0, nachbarn={"norden": "water"}),
       F.gelaende_plan_fein("water", 40.0, 70.0, 48.0, nachbarn={"norden": "forest"}),
       F.gelaende_plan_fein("mountain", 40.0, 70.0, 96.0,
                            nachbarn={"norden": "water", "sueden": "water"})]
check("Gelaendezeichen MIT Ufersaum bleiben in der Zelle",
      all(_in_zelle(p, 40.0, 70.0, p is _bz[2] and 96.0 or 48.0) for p in _bz))

abschnitt("Gelaendezeichen — Determinismus und Varianten")

_dopp = F.gelaende_plan_fein("forest", 40.0, 70.0, 48.0, feld=(3, 4))
check("gleiche Feldkoordinaten -> byte-identischer Plan (Determinismus)",
      _dopp == F.gelaende_plan_fein("forest", 40.0, 70.0, 48.0, feld=(3, 4)))
check("verschiedene Feldkoordinaten -> unterschiedliche Plaene (Varianten existieren)",
      (F.gelaende_plan_fein("forest", 0.0, 0.0, 48.0, feld=(0, 0))
       != F.gelaende_plan_fein("forest", 0.0, 0.0, 48.0, feld=(1, 0))))
check("mehrere Feldkoordinaten liefern verschiedene Varianten (Spiegelung/Verschiebung)",
      len({repr(F.gelaende_plan_fein("water", 0.0, 0.0, 48.0, feld=f))
           for f in ((0, 0), (0, 1), (1, 0), (2, 0), (0, 2))}) >= 3)

abschnitt("Nachbarkanten und Ufersaum (astra Welt 1)")

_none = F.gelaende_plan_fein("forest", 0.0, 0.0, 48.0, feld=(0, 0), nachbarn=None)
_same = F.gelaende_plan_fein("forest", 0.0, 0.0, 48.0, feld=(0, 0),
                             nachbarn={"norden": "forest"})
check("gleichartiger Nachbar unterdrueckt die Innenkante (ein Befehl weniger)",
      len(_same) == len(_none) - 1, f"{len(_same)} vs {len(_none)}")
check("gleichartiger Nachbar: KEINE Rasterlinie an der Nordkante",
      "norden" not in _kanten_namen(_same, "kante"))
check("ohne Nachbarangabe: Nordkante wird gezeichnet",
      "norden" in _kanten_namen(_none, "kante"))
check("deutscher Nachbarname ('wald') wirkt wie 'forest'",
      len(F.gelaende_plan_fein("forest", 0.0, 0.0, 48.0, nachbarn={"norden": "wald"}))
      == len(_same))

_land_wasser = F.gelaende_plan_fein("plains", 0.0, 0.0, 48.0, nachbarn={"norden": "water"})
check("Land/Wasser-Grenze: Ufersaum an der Nordkante",
      _kanten_namen(_land_wasser, "ufersaum") == {"norden"},
      str(_kanten_namen(_land_wasser, "ufersaum")))
check("Land/Wasser-Grenze: Ufersaum in #938A70 und 2–3 px breit",
      all(e["farbe"] == "#938A70"
          and (e["box"][3] - e["box"][1] in (2.0, 3.0) or e["box"][2] - e["box"][0] in (2.0, 3.0))
          for e in _saum(_land_wasser)))
check("Land/Wasser-Grenze: statt Rasterlinie kein 1-px-Innenstrich an der Nordkante",
      "norden" not in _kanten_namen(_land_wasser, "kante"))
_land_land = F.gelaende_plan_fein("plains", 0.0, 0.0, 48.0, nachbarn={"norden": "mountain"})
check("Land/Land-Grenze: KEIN Ufersaum",
      _saum(_land_land) == [])
check("Land/Land-Grenze: Rasterlinie an der Nordkante",
      "norden" in _kanten_namen(_land_land, "kante"))

_wasser_vier = F.gelaende_plan_fein("water", 0.0, 0.0, 48.0,
                                    nachbarn={"norden": "forest", "sueden": "forest",
                                              "westen": "forest", "osten": "forest"})
check("Wasserfeld mit vier Landnachbarn: genau vier Ufersaeume",
      len(_saum(_wasser_vier)) == 4, str(len(_saum(_wasser_vier))))
_wasser_wasser = F.gelaende_plan_fein("water", 0.0, 0.0, 48.0, nachbarn={"norden": "water"})
check("Wasser/Wasser: KEIN Ufersaum und keine Innenkante im Norden",
      _saum(_wasser_wasser) == [] and "norden" not in _kanten_namen(_wasser_wasser, "kante"))

abschnitt("Zoomstufen — weniger Formen bei kleiner Zelle")

for _art in ARTEN:
    _klein = F.gelaende_plan_fein(_art, 0.0, 0.0, 24.0)
    _gross = F.gelaende_plan_fein(_art, 0.0, 0.0, 48.0)
    check(f"{_art}: Plan bei 24 px hat weniger Formen als bei 48 px",
          len(_klein) < len(_gross), f"{len(_klein)} < {len(_gross)}")

abschnitt("Unbekannte Gelaendeart")

_ok_fehler = False
try:
    F.gelaende_plan_fein("lavasee", 0.0, 0.0, 48.0)
except ValueError as e:
    _ok_fehler = all(k in str(e) for k in ARTEN) and "lavasee" in str(e)
check("unbekannte Gelaendeart wirft ValueError und nennt die sechs Schluessel", _ok_fehler)


# ==========================================================================
# 4. Ortsilhouetten (Welt 2)
# ==========================================================================

abschnitt("Ortsilhouetten — dorf/ruine/lager")

for _art in ("dorf", "ruine", "lager"):
    _p = F.ortsilhouette_plan(_art, 40.0, 70.0, 48.0)
    check(f"{_art}: 7 bis 13 Befehle bei 48 px",
          F.WELT2_ORT_BEFEHLE_MIN <= len(_p) <= F.WELT2_ORT_BEFEHLE_MAX, f"{len(_p)}")
    check(f"{_art}: liegt in der Zelle (Toleranz 1 px)", _in_zelle(_p, 40.0, 70.0, 48.0))
    check(f"{_art}: deterministisch",
          _p == F.ortsilhouette_plan(_art, 40.0, 70.0, 48.0))
    check(f"{_art}: keine Emoji", not _hat_emoji(_p))

_o24 = F.ortsilhouette_plan("dorf", 0.0, 0.0, 24.0)
_o32 = F.ortsilhouette_plan("dorf", 0.0, 0.0, 32.0)
_o48 = F.ortsilhouette_plan("dorf", 0.0, 0.0, 48.0)
check("Ortszeichen bei 24 px kleiner als bei 48 px (astra Welt 2)",
      len(_o24) < len(_o48), f"{len(_o24)} < {len(_o48)}")
check("Ortszeichen bei 32 px reduziert (weniger als 48 px)",
      len(_o32) < len(_o48), f"{len(_o32)} < {len(_o48)}")
check("alle Silhouetten bei 24/32/48 in der Zelle",
      all(_in_zelle(F.ortsilhouette_plan(a, 40.0, 70.0, float(z)), 40.0, 70.0, float(z))
          for a in ("dorf", "ruine", "lager") for z in (24, 32, 48)))
def _signatur(plan):
    """Hashbare, geordnete Kurzbeschreibung eines Plans."""
    return tuple(sorted(repr(e) for e in plan))


check("die drei Silhouetten sind voneinander verschieden",
      len({_signatur(F.ortsilhouette_plan(a, 0.0, 0.0, 48.0))
           for a in ("dorf", "ruine", "lager")}) == 3)

_ort_fehler = False
try:
    F.ortsilhouette_plan("schloss", 0.0, 0.0, 48.0)
except ValueError as e:
    _ort_fehler = "schloss" in str(e) and "dorf" in str(e)
check("unbekanntes Ortszeichen wirft ValueError", _ort_fehler)


# ==========================================================================
# 5. Fahne (Welt 2)
# ==========================================================================

abschnitt("Fahne — weisse Fahne auf blauem Sockel")

_fahne = F.fahne_plan_fein(40.0, 70.0, 48.0)
check("Fahne: 4 bis 5 Befehle", F.WELT2_FAHNE_BEFEHLE_MIN <= len(_fahne) <= F.WELT2_FAHNE_BEFEHLE_MAX,
      f"{len(_fahne)}")
check("Fahne: blauer Sockel #356D98 vorhanden",
      any(e.get("farbe") == "#356D98" for e in _fahne))
check("Fahne: weisse Fahne als POLYGON #F2EEDB",
      any(e["form"] == "polygon" and e.get("farbe") == "#F2EEDB" for e in _fahne))
check("Fahne: Mast in #D8D3BD", any(e.get("farbe") == "#D8D3BD" for e in _fahne))
check("Fahne: deterministisch", _fahne == F.fahne_plan_fein(40.0, 70.0, 48.0))
check("Fahne: liegt bei 24/48/96 in der Zelle",
      all(_in_zelle(F.fahne_plan_fein(40.0, 70.0, float(z)), 40.0, 70.0, float(z))
          for z in (24, 48, 96)))
check("Fahne: Sockelbreite skaliert (20 px bei zelle 48)",
      F.fahne_plan_fein(0.0, 0.0, 48.0)[0]["box"][2] - F.fahne_plan_fein(0.0, 0.0, 48.0)[0]["box"][0]
      == 20.0)
check("Fahne: keine Emoji", not _hat_emoji(_fahne))


# ==========================================================================
# 6. Auswahl (Welt 3)
# ==========================================================================

abschnitt("Auswahl — goldene Markierung mit Eckwinkeln")

_aus = F.auswahl_plan_fein(40.0, 70.0, 48.0)
check("Auswahl: genau sechs Befehle (zwei Rahmen + vier Eckwinkel)",
      len(_aus) == 6, f"{len(_aus)}")
check("Auswahl: goldene Markierung #E4C77D und dunkle Unterkontur #17212B",
      any(e.get("rand") == F.WELT3_AUSWAHL_GOLD for e in _aus)
      and any(e.get("rand") == F.WELT3_AUSWAHL_DUNKEL for e in _aus))
check("Auswahl: zwei px eingerueckt (2 px bei zelle 48)",
      _aus[0]["box"][0] == 42.0 and _aus[0]["box"][1] == 72.0, str(_aus[0]["box"]))
check("Auswahl: vier Eckwinkel-Linien in Gold",
      sum(1 for e in _aus if e["form"] == "line" and e.get("farbe") == F.WELT3_AUSWAHL_GOLD) == 4)
check("Auswahl: liegt in der Zelle (Toleranz 1 px)", _in_zelle(_aus, 40.0, 70.0, 48.0))
check("Auswahl: deterministisch", _aus == F.auswahl_plan_fein(40.0, 70.0, 48.0))


# ==========================================================================
# 7. Regionen (Welt 2)
# ==========================================================================

abschnitt("Regionen — neun Namen in #D7CEB4 mit Schatten #26312B")

for _gitter in (20, 8):
    _reg = F.regionen_plan_fein(_gitter, 48.0, 3)
    _namen = [e for e in _reg if e.get("farbe") == F.WELT2_REGION_FARBE]
    check(f"gitter={_gitter}: genau 9 Text-Eintraege mit Fuellfarbe #D7CEB4",
          len(_namen) == 9, str(len(_namen)))
    check(f"gitter={_gitter}: die neun Namen sind die Regionsnamen",
          tuple(e["text"] for e in _namen) == F._REGIONNAMEN)
    check(f"gitter={_gitter}: alle Eintraege sind TEXT",
          all(e["form"] == "text" for e in _reg))

_reg20 = F.regionen_plan_fein(20, 48.0, 3)
_schatten = [e for e in _reg20 if e.get("farbe") == F.WELT2_REGION_SCHATTEN]
check("zwei Textbefehle je Regionsname (9 Schatten #26312B)", len(_schatten) == 9,
      str(len(_schatten)))
check("insgesamt 18 Textbefehle (9 Namen + 9 Schatten)", len(_reg20) == 18, str(len(_reg20)))
check("Schatten ist um 1 px versetzt",
      all(any(abs(e["punkt"][0] - n["punkt"][0]) == 1.0 and abs(e["punkt"][1] - n["punkt"][1]) == 1.0
              for n in _reg20 if n.get("rolle") == "name" and n["text"] == e["text"])
          for e in _schatten))
check("Schriftgroesse ist 18 px bei zelle 48",
      all(e["font"][1] == 18 for e in _reg20 if e.get("rolle") == "name"))
check("alle Regionsnamen liegen im Raster",
      all(0.0 <= v <= 20 * 48.0 for v in _xy_alle(_reg20)[0] + _xy_alle(_reg20)[1]))
check("keine Emoji in der Regionsbeschriftung", not _hat_emoji(_reg20))

try:
    import main as M
    check("Regionsnamen stimmen mit main.WELT_REGIONEN ueberein",
          F._REGIONNAMEN == tuple(M.WELT_REGIONEN))
    check("Uebersichtsfarben stimmen mit main.WELT_GELAENDEFARBEN ueberein",
          F._GELAENDEFARBEN == dict(M.WELT_GELAENDEFARBEN))
except Exception as e:      # pragma: no cover - nur wenn main nicht importierbar
    befund("Abgleich mit main.WELT_REGIONEN/WELT_GELAENDEFARBEN uebersprungen", repr(e))


# ==========================================================================
# 8. Uebersichtskarte (Welt 3)
# ==========================================================================

abschnitt("Uebersichtskarte — 4 x 4 px je Feld, Orte, Auswahl")

_tiles = [{"x": i % 20, "y": i // 20, "terrain": ARTEN[i % 6]} for i in range(400)]
_orte = [(1, 1), (2, 3), (19, 18)]
_ueb = F.uebersicht_plan_fein(_tiles, 80.0, 20, orte=_orte, auswahl=(5, 5))
_rechtecke = [e for e in _ueb if e["form"] == "rectangle"]
_vier = [e for e in _rechtecke
         if e["box"][2] - e["box"][0] == 4.0 and e["box"][3] - e["box"][1] == 4.0]
check("gitter=20 ergibt genau 400 Kachel-Rechtecke", len(_rechtecke) == 400, str(len(_rechtecke)))
check("jede Kachel ist 4 x 4 px (kante = 4 * gitter)",
      len(_vier) == 400, str(len(_vier)))
check("je Ort ein Punkt (Oval)", sum(1 for e in _ueb if e["form"] == "oval") == len(_orte))
check("genau eine goldene Auswahl-Markierung",
      sum(1 for e in _ueb if e.get("farbe") == F.WELT3_AUSWAHL_GOLD
          and e.get("ortszeichen") == "auswahl") == 1)
check("Auswahl hat eine dunkle Unterkontur",
      any(e.get("farbe") == F.WELT3_AUSWAHL_DUNKEL for e in _ueb))
check("Uebersicht ist deterministisch",
      _ueb == F.uebersicht_plan_fein(_tiles, 80.0, 20, orte=_orte, auswahl=(5, 5)))

_ueb_ohne = F.uebersicht_plan_fein(_tiles, 80.0, 20)
check("ohne Orte/Auswahl keine Ovale und keine Auswahl-Marke",
      all(e["form"] != "oval" for e in _ueb_ohne)
      and not any(e.get("ortszeichen") == "auswahl" for e in _ueb_ohne))

_unbek = F.uebersicht_plan_fein([{"x": 0, "y": 0, "terrain": "lavasee"}], 20.0, 1)
check("unbekanntes Gelaende bekommt KEINE Fuellung",
      _unbek[0]["form"] == "rectangle" and "farbe" not in _unbek[0], str(_unbek[0]))
_bekannt = F.uebersicht_plan_fein([{"x": 0, "y": 0, "terrain": "forest"}], 20.0, 1)
check("bekanntes Gelaende bekommt seine Farbe",
      _bekannt[0].get("farbe") == F._GELAENDEFARBEN["forest"])
check("keine Emoji in der Uebersicht", not _hat_emoji(_ueb))

_ueb8 = F.uebersicht_plan_fein([{"x": i % 8, "y": i // 8, "terrain": "plains"}
                                for i in range(64)], 32.0, 8)
check("gitter=8 ergibt genau 64 Kachel-Rechtecke zu 4 x 4 px",
      sum(1 for e in _ueb8 if e["form"] == "rectangle"
          and e["box"][2] - e["box"][0] == 4.0) == 64)


# ==========================================================================
# 9. Panelmaße und offene Luecken
# ==========================================================================

abschnitt("Detailpanel — astra-Maße und offene Luecken")

_masse = F.detail_masse()
check("detail_masse() liefert die vier Panelmaße",
      _masse == {"breite": 248, "innenabstand": 12, "schrift": 14, "titel": 18}, str(_masse))
check("Panelbreite 248, Innenabstand 12, Schrift 14, Titel 18",
      (_masse.get("breite"), _masse.get("innenabstand"), _masse.get("schrift"),
       _masse.get("titel")) == (248, 12, 14, 18))
check("detail_masse() ist ein dict", isinstance(_masse, dict))

_luecken = F.offene_luecken()
check("offene_luecken() nennt Luecken (Liste, nicht leer)",
      isinstance(_luecken, list) and len(_luecken) >= 3, str(len(_luecken)))
check("offene_luecken() meldet die fehlenden Regionsnamen",
      any("Regionsnamen" in z for z in _luecken))
check("offene_luecken() meldet die drei Lichtfarben fuer vier Gelaendearten",
      any("Lichtfarben" in z for z in _luecken))

# Plan-Format gegen das erlaubte Formenset pruefen (alle oeffentlichen Erzeuger).
abschnitt("Plan-Format — nur erlaubte Formen in allen Erzeugern")

_mix = (F.gelaende_plan_fein("forest", 0.0, 0.0, 48.0)
        + F.gelaende_plan_fein("water", 48.0, 0.0, 48.0)
        + F.ortsilhouette_plan("dorf", 0.0, 48.0, 48.0)
        + F.ortsilhouette_plan("ruine", 0.0, 96.0, 48.0)
        + F.ortsilhouette_plan("lager", 0.0, 144.0, 48.0)
        + F.fahne_plan_fein(48.0, 48.0, 48.0)
        + F.auswahl_plan_fein(96.0, 96.0, 48.0)
        + F.regionen_plan_fein(20, 48.0, 3)
        + F.uebersicht_plan_fein(_tiles, 80.0, 20, orte=_orte, auswahl=(5, 5)))
check("alle Formen stammen aus FORMEN",
      all(e["form"] in F.FORMEN for e in _mix),
      str(sorted({e["form"] for e in _mix})))
check("im gesamten Plan-Mix keine Emoji", not _hat_emoji(_mix))


sys.exit(bericht())
