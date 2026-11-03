# -*- coding: ascii -*-
"""DER BOT-TAKT AN FESTEN SPIELZEIT-PUNKTEN - Stufe S-13 (03.11.2026, Daniels Entscheidung 3).

Daniels Entscheidung, woertlich: "Ereignis-Splitting wie beim Spieler (`spieloekonomie.tick_bis`)
- groesserer Umbau, aber eine Wahrheit".

DAS PROBLEM, GEMESSEN
---------------------
Bis heute feuerte der Bot-Takt, wenn `jetzt - letzter >= BOT_TAKT_SEKUNDEN` war. Ob das in einer
Zeitspanne eintrat, hing an der Fliesskomma-Summe: `1 x 3600 s` und `10 x 360 s` auf dieselbe
Spielzeit fuhren UNTERSCHIEDLICH VIELE Bot-Aktionen. Aufgefallen ist es, sobald der Diebstahl (S-12)
das Spielerlager beruehrt: `test_gpt_fixrunde_ortslager_zeit` meldete 98,79 gegen 105,0.

DIE LOESUNG
-----------
`main.bot_takt_punkte(ab, bis)` liefert die FESTEN Vielfachen des Takts in der Spanne. Der Takt in
`GameState.tick` bucht die Orte bis zu jedem dieser Punkte (`_orte_abschnitt`) und laesst DANN den
Bot auf genau diesem Stand handeln. Damit haengt das Ergebnis nur an der Spielzeit, nicht am
Zuschnitt des Takts.

Was diese Datei beweist
-----------------------
1. `bot_takt_punkte` liefert genau die Punkte (ab exklusiv, bis inklusiv) und nichts bei leerer
   Spanne oder unbrauchbarem Takt.
2. DIE WACHE: `1 x 3600` und `10 x 360` ergeben DIESELBEN Bot-Zeitpunkte, DIESELBEN Vorraete der
   Orte und DIESELBEN Bot-Kassen.
3. Dasselbe fuer `1 x 3600` gegen `60 x 60` (feinere Scheiben) und gegen `2 x 1800`.
4. Der Bot feuert nur am festen Punkt: `1800` loest keinen Zug aus, `3600` genau einen, ein
   zweiter Aufruf auf demselben Punkt keinen zweiten.
5. Quellwachen: die alte Fliesskomma-Bedingung ist weg, der Takt ruft die Punkte-Funktion und den
   Abschnitt, und `_letzter_bot_takt` traegt einen PUNKT (keine freie Zeit).

Aufruf:  python -X utf8 tests/test_bot_takt_scheiben.py
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

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
TAKT = float(M.BOT_TAKT_SEKUNDEN)


def _stand():
    """Ein ECHTER Startstand (Gruendung ueber den GUI-Pfad, feste Saat) mit Bots und einem Ort."""
    return starter.neu_erzeugen()


def _messen(gs):
    """Haengt einen Zaehler vor den Bot-Takt und sammelt JEDEN echten Zug (Zeit, Punkt).

    Der Zaehler sitzt als Instanz-Attribut vor der Methode - so zaehlt er genau die Aufrufe, die
    der Takt selbst macht, ohne dass im Spiel eine Zeile dafuer noetig waere.
    """
    echt = gs.bots_fortschreiben
    zuege = []

    def zaehlend(jetzt):
        ergebnis = echt(jetzt)
        if ergebnis.get("bots"):
            zuege.append((float(jetzt), ergebnis.get("punkt")))
        return ergebnis

    gs.bots_fortschreiben = zaehlend
    return zuege


def _fahren(gs, schritte, dauer):
    """Faehrt `schritte` Takte von je `dauer` Spielsekunden und liefert die Bot-Zuege."""
    zuege = _messen(gs)
    for _ in range(schritte):
        gs.tick(dauer)
    return zuege


def _lage(gs):
    """Der vergleichbare Zustand: Vorraete der Orte, Kassen der Bots, Spielzeit, Meldungen."""
    return {
        "orte": [dict(sorted((k, round(float(v), 6)) for k, v in o.vorraete.items()))
                 for o in gs.settlements],
        "kassen": [dict(sorted((k, round(float(v), 6)) for k, v in b.vorraete.items()))
                   for b in gs.bots],
        "zeit": round(float(gs.spielsekunden), 6),
        "meldungen": [m.get("text") for m in gs.messages],
    }


# ==========================================================================
abschnitt("1. bot_takt_punkte: die festen Punkte selbst")
# ==========================================================================
check("1 eine Stunde liefert genau den Punkt 3600", M.bot_takt_punkte(0, 3600) == [3600.0],
      str(M.bot_takt_punkte(0, 3600)))
check("1 zwei Stunden liefern 3600 und 7200",
      M.bot_takt_punkte(0, 7200) == [3600.0, 7200.0], str(M.bot_takt_punkte(0, 7200)))
check("1 der Anfang gehoert NICHT dazu (ab exklusiv)",
      M.bot_takt_punkte(3600, 7200) == [7200.0], str(M.bot_takt_punkte(3600, 7200)))
check("1 eine Spanne ganz ohne Punkt liefert nichts", M.bot_takt_punkte(0, 3599) == [],
      str(M.bot_takt_punkte(0, 3599)))
check("1 eine Spanne von 0 s liefert nichts", M.bot_takt_punkte(0, 0) == [], "")
check("1 ein Punkt mitten in der Spanne zaehlt mit", M.bot_takt_punkte(100, 3600) == [3600.0],
      str(M.bot_takt_punkte(100, 3600)))
check("1 zehn feine Scheiben liefern denselben Punkt wie eine grobe",
      M.bot_takt_punkte(3240, 3600) == [3600.0] and M.bot_takt_punkte(0, 3600) == [3600.0], "")
check("1 ein unbrauchbarer Takt liefert nichts",
      M.bot_takt_punkte(0, 7200, takt=0) == [] and M.bot_takt_punkte(0, 7200, takt=-1) == [], "")
check("1 die Punkte sind aufsteigend und ohne Dublette",
      M.bot_takt_punkte(0, 10800) == [3600.0, 7200.0, 10800.0],
      str(M.bot_takt_punkte(0, 10800)))

# ==========================================================================
abschnitt("2. DIE WACHE: 1 x 3600 ist genau so viel wie 10 x 360")
# ==========================================================================
_grob = _stand()
_fein = copy.deepcopy(_grob)
_zuege_grob = _fahren(_grob, 1, 3600.0)
_zuege_fein = _fahren(_fein, 10, 360.0)
check("2 der grobe Takt hat ueberhaupt Bot-Zuege", len(_zuege_grob) >= 1, str(_zuege_grob))
check("2 beide Zuschnitte fahren DIESELBEN Bot-Zeitpunkte",
      [p for _t, p in _zuege_grob] == [p for _t, p in _zuege_fein],
      f"{[p for _t, p in _zuege_grob]} gegen {[p for _t, p in _zuege_fein]}")
check("2 die Anzahl der Bot-Aktionen ist gleich",
      len(_zuege_grob) == len(_zuege_fein), f"{len(_zuege_grob)} gegen {len(_zuege_fein)}")
_lage_grob = _lage(_grob)
_lage_fein = _lage(_fein)
check("2 die Orte tragen dieselben Vorraete", _lage_grob["orte"] == _lage_fein["orte"],
      f"{_lage_grob['orte']} gegen {_lage_fein['orte']}")
check("2 die Bots tragen dieselben Kassen", _lage_grob["kassen"] == _lage_fein["kassen"],
      f"{_lage_grob['kassen']} gegen {_lage_fein['kassen']}")
check("2 die Spielzeit steht bei beiden auf 3600", _lage_grob["zeit"] == _lage_fein["zeit"] == 3600.0,
      f"{_lage_grob['zeit']} gegen {_lage_fein['zeit']}")
check("2 auch die Meldungen sind gleich", _lage_grob["meldungen"] == _lage_fein["meldungen"],
      f"{len(_lage_grob['meldungen'])} gegen {len(_lage_fein['meldungen'])}")

# ==========================================================================
abschnitt("3. Dasselbe fuer 60 x 60 und 2 x 1800 (drei Stunden)")
# ==========================================================================
_basis = _stand()
_sechzig = copy.deepcopy(_basis)
_zwei = copy.deepcopy(_basis)
_z_basis = _fahren(_basis, 1, 10800.0)
_z_sechzig = _fahren(_sechzig, 180, 60.0)
_z_zwei = _fahren(_zwei, 6, 1800.0)
check("3 drei Stunden ergeben drei feste Punkte",
      [p for _t, p in _z_basis] == [3600.0, 7200.0, 10800.0], str([p for _t, p in _z_basis]))
check("3 180 x 60 s fahren dieselben Punkte",
      [p for _t, p in _z_sechzig] == [p for _t, p in _z_basis],
      f"{[p for _t, p in _z_sechzig]} gegen {[p for _t, p in _z_basis]}")
check("3 6 x 1800 s fahren dieselben Punkte",
      [p for _t, p in _z_zwei] == [p for _t, p in _z_basis],
      f"{[p for _t, p in _z_zwei]} gegen {[p for _t, p in _z_basis]}")
check("3 die Orte tragen bei allen drei Zuschnitten dieselben Vorraete",
      _lage(_basis)["orte"] == _lage(_sechzig)["orte"] == _lage(_zwei)["orte"],
      f"{_lage(_basis)['orte']} / {_lage(_sechzig)['orte']} / {_lage(_zwei)['orte']}")
check("3 die Kassen sind bei allen drei Zuschnitten gleich",
      _lage(_basis)["kassen"] == _lage(_sechzig)["kassen"] == _lage(_zwei)["kassen"],
      f"{_lage(_basis)['kassen']} / {_lage(_sechzig)['kassen']} / {_lage(_zwei)['kassen']}")

# ==========================================================================
abschnitt("4. Der Bot feuert nur am FESTEN Punkt")
# ==========================================================================
gs = _stand()
check("4 1800 s loesen keinen Zug aus", gs.bots_fortschreiben(1800.0).get("bots", 0) == 0,
      str(gs.bots_fortschreiben(1800.0).get("punkt")))
_erster = gs.bots_fortschreiben(3600.0)
check("4 3600 s loesen genau einen Zug aus", _erster.get("bots", 0) == len(gs.bots),
      str(_erster.get("bots")))
check("4 der Zug nennt seinen Punkt", _erster.get("punkt") == 3600.0, str(_erster.get("punkt")))
check("4 ein zweiter Aufruf auf demselben Punkt tut nichts",
      gs.bots_fortschreiben(3600.0).get("bots", 0) == 0, "")
check("4 3599 s nach dem Punkt tun nichts",
      gs.bots_fortschreiben(7199.0).get("bots", 0) == 0, "")
check("4 die naechste volle Stunde feuert wieder", gs.bots_fortschreiben(7200.0).get("punkt") == 7200.0,
      str(gs._letzter_bot_takt))
check("4 eine unsinnige Zeit (unendlich) feuert nicht",
      gs.bots_fortschreiben(float("inf")).get("bots", 0) == 0, "")

# ==========================================================================
abschnitt("5. Quellwachen")
# ==========================================================================
check("5 die alte Fliesskomma-Bedingung ist weg", "jetzt - letzter < BOT_TAKT_SEKUNDEN" not in TEXT_MAIN,
      "main.bots_fortschreiben")
check("5 der Takt fragt die festen Punkte", "for _punkt in bot_takt_punkte(_ab, _bis):" in TEXT_MAIN,
      "main.GameState.tick")
check("5 der Takt bucht je Abschnitt", "_wissen = self._orte_abschnitt(_abschnitt, _punkt, _wissen, eingetroffen)"
      in TEXT_MAIN, "main.GameState.tick")
check("5 der Bot laeuft danach auf genau diesem Punkt",
      "self.bots_fortschreiben(_punkt)" in TEXT_MAIN, "main.GameState.tick")
check("5 der gemerkte Takt ist ein Punkt, keine freie Zeit",
      "self._letzter_bot_takt = punkt" in TEXT_MAIN, "main.bots_fortschreiben")
check("5 einen zweiten Bot-Aufruf am Taktende gibt es nicht mehr",
      "self.bots_fortschreiben(self.spielsekunden)" not in TEXT_MAIN, "main.GameState.tick")

befund("5 ehrliche Grenze: der Bot handelt jetzt je voller Spielstunde GENAU EINMAL - ein sehr "
       "grosser Sprung (etwa ein geladener Altstand mit langer Pause) faehrt entsprechend viele "
       "Zuege nacheinander. Das ist gewollt (ein Zug je Stunde Spielzeit), kostet bei riesigen "
       "Spruengen aber Laufzeit; gemessen wird das im Sammellauf, nicht hier.", "")

sys.exit(bericht())
