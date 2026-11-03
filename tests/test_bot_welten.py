# -*- coding: ascii -*-
"""DIE HERKUNFTSWELT EINES BOT-DORFES - Stufe W-1/W-2 (03.11.2026, Daniels Vorgabe im Chat).

Daniels Vorgabe, woertlich: "das hauptdorf eines Bots [muss] immer in seiner Ursprungs und
herkunftswelt bleiben ... Waehrend der spieler selbst mit dem hauptdorf die welten wechseln darf,
koennen bots nur ihre Nebendoerfer in andere welten transferieren."

DAS PROBLEM, GEMESSEN
---------------------
Jedes Bot-Dorf trug zwar ein Feld `dimension`, aber es stand auf der Vorgabe **1 (Armageddon)**,
waehrend die Heimat des Spielers **4 (Midgard)** ist. Die Anzeige prueft die Welt GAR NICHT
(`_bot_doerfer_im_raster` sah nur `x`/`y`) - fremde Doerfer erschienen deshalb auf JEDER Weltkarte,
und ein Klick startete einen Marsch ueber die Weltgrenze, als waere sie nicht da.

Was diese Datei beweist
-----------------------
1. Ein neu angelegtes Bot-Dorf entsteht in der STARTWELT (Midgard) und traegt sie als
   `herkunftswelt`.
2. Die Karte zeigt nur die Doerfer IHRER Welt; auf einer fremden Welt ist die Liste leer.
3. Die Herkunftswelt bleibt stehen, auch wenn ein Dorf (Nebendorf) die Welt wechselt - `dimension`
   aendert sich, `herkunftswelt` nicht.
4. Nach vielen Bot-Takten ist die Herkunftswelt des Hauptdorfs unveraendert (W-1).
5. Ein Dorf aus einem ALTEN Spielstand (ohne Herkunftswelt, Wert 0) bleibt sichtbar - die Anzeige
   filtert dort nicht, sonst waeren seine Doerfer unsichtbar.
6. Quellwachen: die Anzeige filtert ueberhaupt (die alte Fassung hatte keine Weltbedingung), und der
   Anlageweg schreibt die Startwelt hinein.

Aufruf:  python -X utf8 tests/test_bot_welten.py
"""
from __future__ import annotations

import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
sys.path[:0] = [SRC, os.path.join(ROOT, "tools")]
import gpt_erzeuge_startstaende as starter  # noqa: E402
import main as M  # noqa: E402
import welt as W  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
HEIMAT = int(W.startwelt_nummer() or 1)


def _bildschirm(gs):
    """Eine App-Huelle ohne Fenster: `_bot_doerfer_im_raster` braucht nur `state`."""
    gui = M.NebelseetalApp.__new__(M.NebelseetalApp)
    gui.state = gs
    return gui


# ==========================================================================
abschnitt("1. Ein Bot-Dorf entsteht in der STARTWELT und kennt seine Herkunft")
# ==========================================================================
gs = starter.neu_erzeugen()
check("1 der Startstand hat Bots", bool(gs.bots), str(len(gs.bots)))
check("1 die Heimatwelt des Spielers ist Midgard (Nummer 4)", int(gs.eigene_dimension) == 4,
      str(gs.eigene_dimension))
check("1 die Startwelt aus den Daten ist dieselbe", HEIMAT == 4, str(HEIMAT))
_alle = [(b, d) for b in gs.bots for d in M.bot_doerfer_sicherstellen(b)]
check("1 jedes Bot-Dorf steht in der Startwelt",
      all(int(d.dimension) == HEIMAT for _b, d in _alle),
      str([(d.name, d.dimension) for _b, d in _alle]))
check("1 jedes Bot-Dorf traegt seine Herkunftswelt",
      all(int(getattr(d, "herkunftswelt", 0)) == HEIMAT for _b, d in _alle),
      str([(d.name, getattr(d, "herkunftswelt", None)) for _b, d in _alle]))
check("1 genau ein Hauptdorf je Bot",
      all(sum(1 for _b, d in _alle if _b is b and d.hauptdorf) == 1 for b in gs.bots), "")

# ==========================================================================
abschnitt("2. Die Karte zeigt nur die Doerfer IHRER Welt")
# ==========================================================================
gui = _bildschirm(gs)
auf_midgard = gui._bot_doerfer_im_raster(20)
check("2 auf Midgard stehen alle Doerfer", len(auf_midgard) == len(_alle),
      f"{len(auf_midgard)} von {len(_alle)}")
check("2 auf Valhalla (Welt 5) steht keiner", gui._bot_doerfer_im_raster(20, 5) == [],
      str(len(gui._bot_doerfer_im_raster(20, 5))))
# Ein Dorf zieht um (so darf es mit einem NEBENDORF spaeter passieren): es erscheint dann dort,
# wo es steht - und NICHT mehr in seiner Herkunftswelt.
_bot, _dorf = _alle[1]
_dorf.dimension = 5
check("2 das umgezogene Dorf erscheint auf der neuen Welt",
      any(d is _dorf for _b, d in gui._bot_doerfer_im_raster(20, 5)), "")
check("2 und verschwindet von der Herkunftswelt",
      not any(d is _dorf for _b, d in gui._bot_doerfer_im_raster(20, 4)), "")
check("2 seine Herkunftswelt bleibt dabei stehen (W-2)",
      int(_dorf.herkunftswelt) == HEIMAT, str(_dorf.herkunftswelt))
check("2 die anderen Doerfer bleiben, wo sie waren",
      len(gui._bot_doerfer_im_raster(20, 4)) == len(_alle) - 1,
      str(len(gui._bot_doerfer_im_raster(20, 4))))

# ==========================================================================
abschnitt("3. W-1: nach vielen Takten steht das Hauptdorf noch in seiner Welt")
# ==========================================================================
gs2 = starter.neu_erzeugen()
_haupt = {b.name: next(d for d in M.bot_doerfer_sicherstellen(b) if d.hauptdorf) for b in gs2.bots}
_vorher = {n: (int(d.dimension), int(d.herkunftswelt)) for n, d in _haupt.items()}
for _i in range(12):
    gs2.tick(3600.0)
_nachher = {n: (int(d.dimension), int(d.herkunftswelt)) for n, d in _haupt.items()}
check("3 die Herkunftswelt jedes Hauptdorfs ist unveraendert", _vorher == _nachher,
      f"{_vorher} gegen {_nachher}")
check("3 das Hauptdorf steht nach 12 Takten noch in seiner Welt",
      all(int(d.dimension) == HEIMAT for d in _haupt.values()),
      str([(n, d.dimension) for n, d in _haupt.items()]))

# ==========================================================================
abschnitt("4. Alter Spielstand ohne Herkunftswelt bleibt sichtbar")
# ==========================================================================
gs3 = copy.deepcopy(gs2)
for _b in gs3.bots:
    for _d in M.bot_doerfer_sicherstellen(_b):
        _d.herkunftswelt = 0                    # so lagen Doerfer VOR dieser Stufe im Speicher
        _d.dimension = 1
gui3 = _bildschirm(gs3)
check("4 ohne Herkunftswelt wird NICHT gefiltert (nichts wird unsichtbar)",
      len(gui3._bot_doerfer_im_raster(20, 4)) == len([(b, d) for b in gs3.bots
                                                      for d in M.bot_doerfer_sicherstellen(b)]),
      str(len(gui3._bot_doerfer_im_raster(20, 4))))
befund("4 ehrliche Grenze: ein ALTES Dorf ohne Herkunftswelt wird weiter auf jeder Karte gezeigt, "
       "weil wir seine Welt nicht kennen. Ab dem naechsten Anlegen eines Dorfes traegt es die "
       "Startwelt - bestehende Staende werden NICHT still umgeschrieben.", "")

# ==========================================================================
abschnitt("5. Quellwachen")
# ==========================================================================
check("5 die Anzeige prueft die Welt ueberhaupt",
      "int(dorf.dimension) != welt" in TEXT_MAIN, "main._bot_doerfer_im_raster")
check("5 der Anlageweg schreibt die Startwelt hinein",
      "dimension=_heimat, herkunftswelt=_heimat" in TEXT_MAIN, "main.bot_doerfer_sicherstellen")
check("5 die Herkunftswelt ist ein Feld am Dorf",
      "herkunftswelt: int = 0" in TEXT_MAIN, "main.BotDorf")
check("5 die Vorgabe im Code ist NICHT mehr Welt 1 fuer neue Doerfer",
      "dimension: int = 1" in TEXT_MAIN, "Vorgabewert bleibt fuer alte Staende stehen - siehe 4")

sys.exit(bericht())
