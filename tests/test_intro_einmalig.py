# -*- coding: ascii -*-
"""Das Ankunftsfenster kommt EINMAL je Installation - und der Merker funktioniert wirklich.

BEFUND (08.11.2026, beim Vorbereiten von Test 3 gefunden): `story._merkdatei()` rief
`spieldaten.schreibordner()` auf. Diese Funktion gab es in `spieldaten` GAR NICHT - nur in `main`.
Folgen, beide still:

  * `story.intro_gesehen()` fing den AttributeError und meldete "noch nicht gesehen" -> das Intro kam
    bei JEDEM Start wieder.
  * `story.intro_merken()` fing nur `OSError`, der AttributeError lief bis in den Aufrufer
    (`_intro_weiter`, dort `except Exception: pass`) -> der Merker wurde NIE geschrieben. Nach dem
    Klick auf "Los geht es" lag keine `geschichte.json` neben dem Spielstand.

Behoben: die Aufloesung steht jetzt EINMAL in `spieldaten.schreibordner` (mit
`NEBEL_SPIELDATEN_ORDNER` fuer isolierte Testwelten), `main.schreibordner` reicht nur durch.

Aufruf:  python -X utf8 tests/test_intro_einmalig.py
"""
from __future__ import annotations

import inspect
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import main  # noqa: E402
import spieldaten  # noqa: E402
import story  # noqa: E402

abschnitt("1. Eine Stelle fuer den Schreibordner")

check("spieldaten hat den Schreibordner selbst", hasattr(spieldaten, "schreibordner"))
check("main reicht nur durch (keine zweite Aufloesung)",
      "return spieldaten.schreibordner()" in inspect.getsource(main.schreibordner))
check("main und spieldaten nennen denselben Ordner",
      os.path.abspath(main.schreibordner()) == os.path.abspath(spieldaten.schreibordner()),
      "%s vs %s" % (main.schreibordner(), spieldaten.schreibordner()))

abschnitt("2. Der Merker wird wirklich geschrieben und gelesen")

_alt = os.environ.get("NEBEL_SPIELDATEN_ORDNER")
_tmp = tempfile.mkdtemp(prefix="nebel_intro_")
os.environ["NEBEL_SPIELDATEN_ORDNER"] = _tmp            # isolierte Testwelt, kein echter Spielstand
try:
    check("isolierten Ordner nimmt der Schreibordner an",
          os.path.abspath(spieldaten.schreibordner()) == os.path.abspath(_tmp),
          spieldaten.schreibordner())
    check("vor dem Merken: Intro NICHT gesehen", story.intro_gesehen() is False)
    story.intro_merken()                                 # das macht der Knopf "Los geht es"
    _pfad = os.path.join(_tmp, "geschichte.json")
    check("die Merkdatei liegt neben dem Spielstand", os.path.isfile(_pfad), _pfad)
    check("nach dem Merken: Intro gesehen", story.intro_gesehen() is True)
    story.intro_merken()                                 # zweiter Aufruf darf nicht scheitern
    check("zweiter Aufruf bleibt gueltig", story.intro_gesehen() is True)
finally:
    if _alt is None:
        os.environ.pop("NEBEL_SPIELDATEN_ORDNER", None)
    else:
        os.environ["NEBEL_SPIELDATEN_ORDNER"] = _alt
    try:
        for _name in os.listdir(_tmp):
            os.remove(os.path.join(_tmp, _name))
        os.rmdir(_tmp)
    except OSError:
        pass

abschnitt("3. Der Knopf ruft Merken UND Weitergehen")

_quelle = inspect.getsource(main.NebelseetalApp._intro_weiter)
check("der Knopf merkt das Intro", "story.intro_merken()" in _quelle)
check("ein Fehler beim Merken blockiert den Spielweg nicht",
      "except Exception" in _quelle.split("story.intro_merken()")[1][:200], _quelle[:160])
check("danach wird die Ansicht gewechselt", "_switch_view(" in _quelle)

befund("Was NICHT geprueft ist: der echte Start der EXE (dort liegt der Merker in "
       "`~/.nebelseetal/geschichte.json`). Dieser Ordner ist im Test NICHT angefasst worden - "
       "die Pruefung arbeitet in einer eigenen Testwelt.", "")
sys.exit(bericht())
