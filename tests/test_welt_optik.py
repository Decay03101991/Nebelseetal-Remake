"""
Prueft die Zeichenplaene der WELTkarte (src/welt_optik.py) OHNE Fenster.

Alle Plaene sind reine Daten (dicts). Geprueft werden: die sechs Gelaendezeichen (Formenzahl,
Lage in der Zelle, Determinismus, ValueError bei unbekannter Art), die Fahne, der
Auswahlrahmen, das Ortszeichen, die Regionsbeschriftung (3x3) und die kleine Uebersichtskarte
(400 Kacheln bei gitter=20).``zeichne`` wird mit einer duck-typisierten Probeleinwand geprueft;
zusaetzlich — falls eine Anzeige vorhanden ist — auf einer zurueckgezogenen tk-Leinwand.

Aufruf:  python tests/test_welt_optik.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import welt_optik as W

ARTEN = ("forest", "plains", "mountain", "water", "village", "ruins")
ZOLL = 1.0   # erlaubter Ueberstand in px (Vorgabe: hoechstens 1 px)


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
    """Liegen ALLE Koordinaten im Zellenkasten (mit Toleranz toll)? """
    xs, ys = _xy_alle(plan)
    return (all(x0 - toll <= v <= x0 + zelle + toll for v in xs)
            and all(y0 - toll <= v <= y0 + zelle + toll for v in ys))


def _formen(plan):
    return [e["form"] for e in plan]


def _nur_hex(plan) -> bool:
    """Jede gesetzte Fuell-/Randfarbe beginnt mit '#'. """
    for e in plan:
        for schluessel in ("farbe", "rand"):
            if schluessel in e and not str(e[schluessel]).startswith("#"):
                return False
    return True


class ProbeLeinwand:
    """Duck-typisierte Leinwand: merkt sich jeden create_*-Aufruf (kein tkinter)."""

    def __init__(self):
        self.aufrufe = []

    def _merke(self, form, tags, kw, args):
        self.aufrufe.append({"form": form, "tags": tuple(tags), "kw": dict(kw), "args": tuple(args)})

    def create_polygon(self, *a, tags=(), **k):
        self._merke("polygon", tags, k, a)

    def create_rectangle(self, *a, tags=(), **k):
        self._merke("rectangle", tags, k, a)

    def create_oval(self, *a, tags=(), **k):
        self._merke("oval", tags, k, a)

    def create_line(self, *a, tags=(), **k):
        self._merke("line", tags, k, a)

    def create_text(self, *a, tags=(), **k):
        self._merke("text", tags, k, a)

    def create_arc(self, *a, tags=(), **k):
        self._merke("arc", tags, k, a)


# ==========================================================================
# 1. Modul und Plan-Format
# ==========================================================================

abschnitt("Modul — die acht oeffentlichen Funktionen und das Plan-Format")

for _name in ("gelaende_plan", "fahne_plan", "auswahl_plan", "regionen_plan",
              "uebersicht_plan", "ortszeichen_plan", "zeichne", "offene_luecken"):
    check(f"Funktion {_name}() vorhanden", callable(getattr(W, _name, None)))

check("sechs erlaubte Zeichenformen", W.FORMEN == ("polygon", "rectangle", "oval", "line",
                                                   "text", "arc"), str(W.FORMEN))
check("sechs Gelaendearten der Weltkarte", tuple(W.GELAENDEARTEN) == ARTEN, str(W.GELAENDEARTEN))

_luecken = W.offene_luecken()
check("offene_luecken() nennt die Luecken (Liste, nicht leer)",
      isinstance(_luecken, list) and len(_luecken) >= 3, str(len(_luecken)))
check("offene_luecken() meldet fehlende Regionsnamen",
      any("Regionsnamen" in z for z in _luecken))
check("offene_luecken() meldet fehlende Zoomstufen",
      any("Zoomstufen" in z for z in _luecken))


# ==========================================================================
# 2. Die sechs Gelaendezeichen
# ==========================================================================

abschnitt("Gelaendezeichen — mindestens vier Formen je Art")

for _art in ARTEN:
    _p = W.gelaende_plan(_art, 40.0, 70.0, 48.0)
    check(f"{_art}: 4 bis 16 Formen",
          4 <= len(_p) <= 16, f"{len(_p)} Formen")

abschnitt("Gelaendezeichen — Formen, Farben, Determinismus, Fehler")

_alle = {a: W.gelaende_plan(a, 0.0, 0.0, 64.0) for a in ARTEN}
check("alle Formen stammen aus dem erlaubten Satz",
      all(f in W.FORMEN for p in _alle.values() for f in _formen(p)))
check("alle Farben sind Hex-Werte",
      all(_nur_hex(p) for p in _alle.values()))
check("die Zeichen sind deterministisch (zweimal gleich)",
      all(W.gelaende_plan(a, 0.0, 0.0, 64.0) == _alle[a] for a in ARTEN))

_ok_fehler = False
try:
    W.gelaende_plan("lavasee", 0.0, 0.0, 48.0)
except ValueError as e:
    _ok_fehler = ("lavasee" in str(e)) and ("erwartet" in str(e))
check("unbekannte Gelaendeart wirft ValueError mit klarer Meldung", _ok_fehler)

abschnitt("Gelaendezeichen — alle Koordinaten in der Zelle (Toleranz 1 px)")

# x0 != y0, damit vertauschte Achsen auffallen.
for _zelle in (24.0, 32.0, 48.0, 64.0, 96.0):
    _treffer = all(_in_zelle(W.gelaende_plan(a, 40.0, 70.0, _zelle), 40.0, 70.0, _zelle)
                   for a in ARTEN)
    check(f"alle sechs Gelaendezeichen liegen bei zelle={int(_zelle)} in der Zelle", _treffer)


# ==========================================================================
# 3. Fahne des eigenen Ortes
# ==========================================================================

abschnitt("Fahne — weisse Fahne auf blauem Sockel")

_fahne = W.fahne_plan(40.0, 70.0, 48.0)
check("Fahne hat mindestens 3 Formen", len(_fahne) >= 3, f"{len(_fahne)} Formen")
check("Fahne ist deterministisch", _fahne == W.fahne_plan(40.0, 70.0, 48.0))
check("Fahne: blauer Sockel und weisse Flagge",
      any(e.get("farbe") == "#2563EB" for e in _fahne)
      and any(e["form"] == "polygon" and e.get("farbe") == "#F3F4F6" for e in _fahne))
check("Fahne liegt in der Zelle (Toleranz 1 px)", _in_zelle(_fahne, 40.0, 70.0, 48.0))
check("Fahne ist skaliert (andere Zellgroesse = andere Koordinaten)",
      W.fahne_plan(0.0, 0.0, 32.0)[0]["box"][2] == 0.0 + 16.0 + 0.16 * 32.0)


# ==========================================================================
# 4. Auswahlrahmen
# ==========================================================================

abschnitt("Auswahlrahmen — ein Cyan-Rand je Feld")

_ausw = W.auswahl_plan(40.0, 70.0, 48.0)
check("Auswahlrahmen ist ein einzelnes Rechteck in Cyan",
      len(_ausw) == 1 and _ausw[0]["form"] == "rectangle"
      and _ausw[0]["rand"] == "#38BDF8", str(_ausw))
check("Auswahlrahmen ohne Fuellung (nur Umriss)", "farbe" not in _ausw[0])
_ausw2 = W.auswahl_plan(40.0, 70.0, 48.0, "#FF3B3B")
check("eigene Auswahlfarbe wird uebernommen", _ausw2[0]["rand"] == "#FF3B3B")
check("Auswahlrahmen liegt in der Zelle (Toleranz 1 px)", _in_zelle(_ausw, 40.0, 70.0, 48.0))


# ==========================================================================
# 5. Ortszeichen (Kreis + winziger Gelaendehinweis)
# ==========================================================================

abschnitt("Ortszeichen — Kreis plus Gelaendehinweis, kein Emoji")

_ort = W.ortszeichen_plan(40.0, 70.0, 48.0, "plains")
check("Ortszeichen hat einen Kreis (Oval)", any(e["form"] == "oval" for e in _ort))
check("Ortszeichen hat Kreis plus Hinweis (>= 2 Formen)", len(_ort) >= 2, f"{len(_ort)}")
check("Ortszeichen nutzt nur erlaubte Formen (kein Emoji)",
      all(f in W.FORMEN for f in _formen(_ort)))
check("Ortszeichen liegt in der Zelle (Toleranz 1 px)", _in_zelle(_ort, 40.0, 70.0, 48.0))
check("Ortszeichen unterscheidet sich nach Gelaende",
      W.ortszeichen_plan(0, 0, 48, "water") != W.ortszeichen_plan(0, 0, 48, "ruins"))
check("Ortszeichen ist deterministisch (_ort bleibt gleich)",
      W.ortszeichen_plan(40.0, 70.0, 48.0, "plains") == _ort)


# ==========================================================================
# 6. Regionsbeschriftung (3x3)
# ==========================================================================

abschnitt("Regionen — genau neun Text-Eintraege in der Mitte der Bloecke")

_reg20 = W.regionen_plan(20, 48.0, 3)
check("gitter=20, anzahl=3 ergibt genau 9 Eintraege", len(_reg20) == 9, str(len(_reg20)))
check("alle Regions-Eintraege sind TEXT", all(e["form"] == "text" for e in _reg20))
_reg_x, _reg_y = _xy_alle(_reg20)
check("alle Regions-Mittelpunkte liegen im Raster",
      all(0.0 <= v <= 20 * 48.0 for v in _reg_x) and all(0.0 <= v <= 20 * 48.0 for v in _reg_y))
check("die neun Namen sind die Regionsnamen",
      tuple(e["text"] for e in _reg20) == W._REGIONNAMEN)
check("jede Region traegt eine Schrift (font-Tupel)",
      all(isinstance(e.get("font"), tuple) and len(e["font"]) == 3 for e in _reg20))

_reg8 = W.regionen_plan(8, 48.0, 3)
check("gitter=8, anzahl=3 ergibt ebenfalls 9 Eintraege", len(_reg8) == 9, str(len(_reg8)))

try:
    import main as M
    check("Regionsnamen stimmen mit main.WELT_REGIONEN ueberein",
          tuple(W._REGIONNAMEN) == tuple(M.WELT_REGIONEN), str(M.WELT_REGIONEN))
    check("Gelaendefarben stimmen mit main.WELT_GELAENDEFARBEN ueberein",
          W._GELAENDEFARBEN == dict(M.WELT_GELAENDEFARBEN))
except Exception as e:      # pragma: no cover - nur wenn main nicht importierbar
    befund("Abgleich mit main.WELT_REGIONEN/WELT_GELAENDEFARBEN uebersprungen", repr(e))


# ==========================================================================
# 7. Kleine Uebersichtskarte
# ==========================================================================

abschnitt("Uebersichtskarte — 400 Kacheln, Orte, Auswahlrahmen")

_tiles = [{"x": i % 20, "y": i // 20, "terrain": ARTEN[i % 6]} for i in range(400)]
_orte = [(1, 1), (2, 3), (19, 18)]
_ueb = W.uebersicht_plan(_tiles, 132.0, 20, orte=_orte, auswahl=(5, 5))
_rechtecke = [e for e in _ueb if e["form"] == "rectangle"]
_ovale = [e for e in _ueb if e["form"] == "oval"]
_linien = [e for e in _ueb if e["form"] == "line"]
check("gitter=20 ergibt genau 400 Kachel-Rechtecke", len(_rechtecke) == 400, str(len(_rechtecke)))
check("je Ort ein Punkt (Oval)", len(_ovale) == len(_orte), f"{len(_ovale)} bei {len(_orte)} Orten")
check("genau ein Auswahlrahmen (Linienzug)", len(_linien) == 1, str(len(_linien)))
check("Gesamtzahl = 400 Kacheln + Orte + Auswahlrahmen",
      len(_ueb) == 400 + len(_orte) + 1, str(len(_ueb)))
check("Kachel-Rechtecke liegen im Quadrat der Kantenlaenge",
      all(0.0 <= v <= 132.0 for e in _rechtecke for v in e["box"]))
check("Orts-Mittelpunkt sitzt in der Zellmitte",
      _ovale[0]["box"][0] < (1 + 0.5) * (132.0 / 20) < _ovale[0]["box"][2])

_ueb2 = W.uebersicht_plan(_tiles, 132.0, 20, orte=_orte, auswahl=(5, 5))
check("Uebersichtskarte ist deterministisch", _ueb == _ueb2)

_ueb_ohne = W.uebersicht_plan(_tiles, 132.0, 20)
check("ohne Auswahl/Auswahl kein Rahmen", all(e["form"] != "line" for e in _ueb_ohne))
check("ohne Orte keine Punkte", all(e["form"] != "oval" for e in _ueb_ohne))

_unbek = W.uebersicht_plan([{"x": 0, "y": 0, "terrain": "lavasee"}], 20.0, 1)
check("unbekanntes Gelaende bekommt KEINE Fuellung (nichts erfunden)",
      _unbek[0]["form"] == "rectangle" and "farbe" not in _unbek[0], str(_unbek[0]))

_bekannt = W.uebersicht_plan([{"x": 0, "y": 0, "terrain": "forest"}], 20.0, 1)
check("bekanntes Gelaende bekommt seine Farbe",
      _bekannt[0].get("farbe") == W._GELAENDEFARBEN["forest"])

_explizit = W.uebersicht_plan([{"x": 0, "y": 0, "farbe": "#123456"}], 20.0, 1)
check("ausdrueckliche Kachelfarbe wird uebernommen", _explizit[0]["farbe"] == "#123456")


# ==========================================================================
# 8. zeichne (Duck-Typing) — Probeleinwand und (falls vorhanden) tk-Leinwand
# ==========================================================================

abschnitt("zeichne — eine Form je Eintrag, tags an jedem Aufruf")

_plan = (W.gelaende_plan("forest", 0.0, 0.0, 48.0)
         + W.gelaende_plan("water", 48.0, 0.0, 48.0)
         + W.regionen_plan(20, 48.0, 3)
         + W.fahne_plan(0.0, 48.0, 48.0)
         + W.auswahl_plan(48.0, 48.0, 48.0)
         + [{"form": "arc", "box": [10.0, 10.0, 50.0, 50.0], "winkel": 0, "weite": 180,
             "stil": "chord", "farbe": "#5B5F63"},
            {"form": "text", "punkt": [5.0, 5.0], "text": "X", "farbe": "#E6E9EE",
             "font": ("TkDefaultFont", 9, "bold")}])

_probe = ProbeLeinwand()
_gezeichnet = W.zeichne(_probe, _plan, tags=("welt",))
check("zeichne() gibt die Zahl der Eintraege zurueck",
      _gezeichnet == len(_plan), f"{_gezeichnet} von {len(_plan)}")
check("zeichne() zeichnet genau ein Objekt je Eintrag",
      len(_probe.aufrufe) == len(_plan), f"{len(_probe.aufrufe)} Aufrufe")
check("zeichne() gibt tags an JEDEN Aufruf weiter",
      all(a["tags"] == ("welt",) for a in _probe.aufrufe))
check("zeichne() deckt alle sechs Formen ab",
      {a["form"] for a in _probe.aufrufe} >= {"polygon", "rectangle", "oval", "line",
                                              "text", "arc"},
      str(sorted({a["form"] for a in _probe.aufrufe})))
check("zeichne() uebergibt den Bogenwinkel (start/extent) korrekt",
      any(a["form"] == "arc" and a["kw"].get("start") == 0 and a["kw"].get("extent") == 180
          for a in _probe.aufrufe))
def _form_fehler() -> bool:
    try:
        W.zeichne(ProbeLeinwand(), [{"form": "kreis"}])
        return False
    except ValueError:
        return True


check("zeichne() meldet unbekannte Formen als ValueError", _form_fehler())

# Echter, aber zurueckgezogener tk-Zeichenbereich (nur Anzeige pruefen, kein sichtbares Fenster).
try:
    import tkinter as tk
    _root = tk.Tk()
    _root.withdraw()
    try:
        _leinwand = tk.Canvas(_root, width=400, height=400)
        _tk_plan = W.gelaende_plan("mountain", 0.0, 0.0, 64.0) + W.regionen_plan(20, 32.0, 3)
        _n = W.zeichne(_leinwand, _tk_plan, tags=("t",))
        _items = len(_leinwand.find_all())
        check("zeichne() auf zurueckgezogener tk-Leinwand: len(plan) == Objekte",
              _n == len(_tk_plan) and _items == len(_tk_plan),
              f"{_n} / {_items} / {len(_tk_plan)}")
    finally:
        _root.destroy()
except Exception as e:      # pragma: no cover - nur ohne Anzeige
    befund("Fensterpruefung zeichne() uebersprungen",
           f"keine Anzeige / kein tkinter: {e!r}")


sys.exit(bericht())
