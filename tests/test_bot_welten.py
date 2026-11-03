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
import voelker as V  # noqa: E402
WELTEN = V.welten_je_fraktion()          # Fraktion -> Heimatwelt (Datendatei, W-9)


def _welt_von(bot):
    """Die Welt, in der dieser Bot laut seiner FRAKTION startet (0 = keine eingetragen)."""
    return int(WELTEN.get(str(bot.faction), 0))


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
check("1 es sind fuenf Bots (W-5: 5 Bots und 1 Spieler fuer die 6 Welten)",
      len(gs.bots) == 5, str(len(gs.bots)))
check("1 jede Fraktion hat eine Heimatwelt in den Daten (W-9)", len(WELTEN) == 6, str(WELTEN))
_alle = [(b, d) for b in gs.bots for d in M.bot_doerfer_sicherstellen(b)]
check("1 jedes Bot-Dorf steht in der Welt SEINER FRAKTION",
      all(int(d.dimension) == _welt_von(b) for b, d in _alle),
      str([(b.name, b.faction, d.dimension, _welt_von(b)) for b, d in _alle]))
check("1 jedes Bot-Dorf traegt genau diese Herkunftswelt",
      all(int(getattr(d, "herkunftswelt", 0)) == _welt_von(b) for b, d in _alle),
      str([(d.name, getattr(d, "herkunftswelt", None)) for _b, d in _alle]))
# VOR der Voelkerwahl duerfen zwei Bots dasselbe Volk tragen (so steht es in `BOTS`: Haug und
# Brynhild sind beide menschlich) - sie stehen dann in derselben Welt. ERST die Wahl des Spielers
# verteilt die Voelker ohne Doppelung (Abschnitt 5).
check("1 jeder Bot traegt eine Fraktion aus der Datendatei",
      all(str(b.faction) in WELTEN for b in gs.bots),
      str([(b.name, b.faction) for b in gs.bots]))
check("1 genau ein Hauptdorf je Bot",
      all(sum(1 for _b, d in _alle if _b is b and d.hauptdorf) == 1 for b in gs.bots), "")

# ==========================================================================
abschnitt("2. Die Karte zeigt nur die Doerfer IHRER Welt")
# ==========================================================================
gui = _bildschirm(gs)
_eigene = int(gs.eigene_dimension)
auf_eigener = gui._bot_doerfer_im_raster(20)
check("2 auf der eigenen Welt stehen NUR die Doerfer, die dort liegen",
      all(int(d.dimension) == _eigene for _b, d in auf_eigener), str(len(auf_eigener)))
check("2 die Summe ueber alle Welten ist jedes Dorf genau einmal",
      sum(len(gui._bot_doerfer_im_raster(20, w)) for w in sorted(set(WELTEN.values())))
      == len(_alle), f"{[len(gui._bot_doerfer_im_raster(20, w)) for w in sorted(set(WELTEN.values()))]}")
# Ein Dorf zieht um (so darf es mit einem NEBENDORF spaeter passieren): es erscheint dann dort,
# wo es steht - und NICHT mehr in seiner Herkunftswelt.
_bot, _dorf = _alle[1]
_dorf.dimension = 5
_herkunft_dorf = int(_dorf.herkunftswelt)
check("2 das umgezogene Dorf erscheint NUR auf der neuen Welt",
      any(d is _dorf for _b, d in gui._bot_doerfer_im_raster(20, 5))
      and not any(d is _dorf for _b, d in gui._bot_doerfer_im_raster(20, 4)), "")
check("2 seine Herkunftswelt bleibt dabei stehen (W-2)",
      int(_dorf.herkunftswelt) == _herkunft_dorf, str(_dorf.herkunftswelt))

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
      all(int(d.dimension) == _welt_von(next(b for b in gs2.bots if b.name == n))
          for n, d in _haupt.items()),
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
abschnitt("5. W-9: der Spieler startet in der Welt SEINER FRAKTION")
# ==========================================================================
for _volk in ("menschlich", "zwergisch", "elfisch", "Trolle", "Ghule", "Gnome"):
    gs4 = starter.neu_erzeugen()
    gui4 = _bildschirm(gs4)
    gui4._log = gs4._log                      # die Ansicht schreibt ins Spiel-Log
    gui4._volk_waehlen(_volk)
    _w = int(WELTEN[_volk])
    check("5 %s startet in seiner Heimatwelt %d" % (_volk, _w),
          int(gs4.eigene_dimension) == _w, str(gs4.eigene_dimension))
    check("5 %s traegt sie als eigene Welt" % _volk, _w in list(gs4.eigene_dimensionen),
          str(gs4.eigene_dimensionen))
    check("5 die Bot-Doerfer stehen danach in den Welten ihrer NEUEN Fraktionen",
          all(int(d.dimension) == int(WELTEN.get(str(b.faction), 0))
              for b in gs4.bots for d in M.bot_doerfer_sicherstellen(b)),
          str([(b.name, b.faction, d.dimension) for b in gs4.bots
               for d in M.bot_doerfer_sicherstellen(b)]))
    check("5 die Herkunftswelt der Bot-Doerfer ist mitgezogen",
          all(int(getattr(d, "herkunftswelt", 0)) == int(WELTEN.get(str(b.faction), 0))
              for b in gs4.bots for d in M.bot_doerfer_sicherstellen(b)), "")

check("5 es gibt KEINEN Midgard-Zwang im Startweg",
      "eigene_dimension = 4" not in TEXT_MAIN and "startwelt_nummer() or 4" not in TEXT_MAIN, "")
check("5 die Welt kommt aus der Fraktion, an EINER Lesestelle",
      TEXT_MAIN.count("voelker.welt_von_fraktion(") >= 3, str(TEXT_MAIN.count("voelker.welt_von_fraktion(")))

# ==========================================================================
abschnitt("6. Quellwachen")
# ==========================================================================
check("6 die Anzeige prueft die Welt ueberhaupt",
      "int(dorf.dimension) != welt" in TEXT_MAIN, "main._bot_doerfer_im_raster")
check("6 der Anlageweg schreibt die Heimatwelt hinein",
      "dimension=_heimat, herkunftswelt=_heimat" in TEXT_MAIN, "main.bot_doerfer_sicherstellen")
check("6 die Herkunftswelt ist ein Feld am Dorf",
      "herkunftswelt: int = 0" in TEXT_MAIN, "main.BotDorf")
check("6 die Vorgabe im Code ist NICHT mehr Welt 1 fuer neue Doerfer",
      "dimension: int = 1" in TEXT_MAIN, "Vorgabewert bleibt fuer alte Staende stehen - siehe 4")

sys.exit(bericht())
