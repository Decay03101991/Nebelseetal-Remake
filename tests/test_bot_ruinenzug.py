# -*- coding: ascii -*-
"""Frage 1: Bots raeumen gepluenderte Ruinen - mit Karren und OHNE Kampf (Register 215).

Daniels Entscheidung (05.11.2026, Frage 1): "Ja, mit Karren und ohne Kampf" - ein Bot laeuft
die Ruine eines gefallenen Drachen an, laedt ein, was noch liegt, und schlaegt sich nicht.

Vorher gab es diesen Weg nicht: `_bots_drachenzug` sammelte nur DRACHEN, die noch stehen
(`id not in drachen_besiegt`). Eine Ruine mit Restbeute war fuer jeden Bot unsichtbar - der
Hort blieb liegen, bis der Spieler kam.

Was diese Datei beweist
-----------------------
1. Mit Karren raeumt der Bot: er laeuft hin, laedt bis zur Ladung, der Rest bleibt liegen -
   und es gibt KEIN Gefecht (keine Verluste, keine Wache, kein Feueratem).
2. Ohne Karren bleibt alles liegen; eine leere Ruine wird nicht angefahren; ohne besiegten
   Drachen passiert nichts; ein Bot einer fremden Welt kommt nicht hin.
3. Die Beute landet in der Bot-Kasse, der Hort schrumpft um genau diese Menge - gebucht ueber
   DENSELBEN Weg wie beim Spieler (`_drachen_kampf` -> `_drachen_ruine_pluendern`).
4. Der Bot rechnet mit SEINER Forschung (Wagenbau), nicht mit der des Spielers.
5. Quellwachen: der Bot-Takt fragt die Ruine VOR dem Drachen, und in den Zug gehen nur Karren
   (kein Kaempfer, keine Belagerung) - das ist "ohne Kampf" im Code, nicht nur im Kommentar.
6. Gegenprobe: mit einem STEHENDEN Drachen tut der Ruinenzug nichts (der Weg ist nicht der
   Kampfweg und darf es nicht werden).

ASCII-only (Pruefdatei-Konvention): Umlaute nur als Escape.

Aufruf:  python -X utf8 tests/test_bot_ruinenzug.py
"""
from __future__ import annotations

import ast
import inspect
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, ausnahme, import_src

ROOT, SRC = import_src()
import drachen  # noqa: E402
import einheiten  # noqa: E402
import main as M  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
KARRE = "Handkarren"                                # Ladung 40 je Stueck (data/units.json)
DRACHE = drachen.finde_id("drache_d02")             # der Drache der Welt d02
KENNUNG = str(DRACHE.get("id"))                     # seine Kennung
WELT = int(str(DRACHE.get("welt")).lstrip("d"))     # Weltnummer aus der Kennung

# Der Hort einer Ruine, mit dem die Pruefung rechnet (Reste nach einem Gefecht).
HORT = {"gold": 3000, "holz": 1000, "stein": 1000}
HORT_SUMME = sum(HORT.values())


def _code(fn) -> str:
    """Der Quelltext einer Funktion OHNE Docstring - ein Kommentar darf keine Wache faerben."""
    baum = ast.parse(textwrap.dedent(inspect.getsource(fn)))
    baum.body[0].body = [s for s in baum.body[0].body
                         if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant))]
    return ast.unparse(baum)


def _bot(karren=2, welt=WELT, forschung=None):
    """Ein Bot mit EINEM Hauptdorf in der genannten Welt und einem Wagenpark."""
    dorf = M.BotDorf(name="Raeumer-Dorf", x=1, y=1, herkunftswelt=welt, dimension=welt,
                     hauptdorf=True, einheiten={}, vorraete={})
    bot = M.BotPlayer("Raeumer", "menschlich", 1.0, 0.0, doerfer=[dorf])
    bot.lager = {KARRE: int(karren)} if karren else {}
    bot.forschungsstaende = dict(forschung or {})
    return bot


def _stand(besiegt=True, hort=None):
    """Ein Spielstand mit einer Ruine (oder einem stehenden Drachen) und ihrem Hort."""
    st = M.GameState()
    st.spielsekunden = 1000.0
    st.drachen_besiegt = [KENNUNG] if besiegt else []
    st.drachen_vorraete = {KENNUNG: dict(HORT if hort is None else hort)}
    return st


def _kasse(bot) -> float:
    """Die Summe der Bot-Kasse (EINE Wahrheit: `bot_kasse`)."""
    return sum(float(v or 0.0) for v in (M.bot_kasse(bot) or {}).values())


def haupt() -> int:
    # ------------------------------------------------------------------ 1. Mit Karren raeumen
    abschnitt("1. Mit Karren raeumt der Bot - und schlaegt sich nicht")
    st = _stand()
    bot = _bot(karren=2)
    ergebnis = ausnahme("Ruinenzug mit Karren", lambda: st._bots_ruinenzug(bot, 1000.0))
    ok, meldung = ergebnis if isinstance(ergebnis, tuple) else (False, "")
    check("1 der Bot faehrt zur Ruine", ok is True, str(meldung))
    check("1 die Meldung sagt, dass es kein Kampf war", "kein Kampf" in str(meldung), str(meldung))
    check("1 die Meldung nennt den Namen der Ruine", str(DRACHE.get("name")) in str(meldung), str(meldung))

    ladung = einheiten.ladung_der_gruppe({KARRE: 2})
    rest = sum(int(v) for v in (st.drachen_vorraete.get(KENNUNG) or {}).values())
    check("1 der Hort schrumpft um genau die Karrenladung (%d)" % ladung, rest == HORT_SUMME - ladung,
          "%d von %d" % (rest, HORT_SUMME))
    check("1 die Beute steht in der Bot-Kasse", _kasse(bot) == float(ladung), "%s" % _kasse(bot))

    check("1 KEIN Gefecht: keine Verluste beim Bot (Armee unveraendert)", M.bot_armee(bot) == {},
          str(M.bot_armee(bot)))
    check("1 KEIN Gefecht: die Wache des Drachen bleibt unangetastet",
          not (getattr(st, "drachen_wachen", {}) or {}).get(KENNUNG, {}),
          str((getattr(st, "drachen_wachen", {}) or {}).get(KENNUNG)))
    bericht_text = str((st.messages[-1] if st.messages else {}).get("text") or "")
    check("1 der Bericht meldet keine Verluste", "erlust" not in bericht_text, bericht_text[-120:])
    check("1 der Bericht nennt die Ruine", "Ruine" in bericht_text, bericht_text[-120:])

    # ------------------------------------------------------------------- 2. Die harten Grenzen
    abschnitt("2. Ohne Karren, ohne Beute, ohne Ruine, ohne Welt: kein Zug")
    st2 = _stand()
    ohnehin = sum(int(v) for v in (st2.drachen_vorraete.get(KENNUNG) or {}).values())
    check("2 ohne Karren kein Zug", st2._bots_ruinenzug(_bot(karren=0), 1000.0) == (False, ""))
    check("2 ohne Karren bleibt der Hort unveraendert",
          sum(int(v) for v in (st2.drachen_vorraete.get(KENNUNG) or {}).values()) == ohnehin,
          str(st2.drachen_vorraete.get(KENNUNG)))

    st3 = _stand()
    leer = _bot(karren=2)
    st3.drachen_vorraete = {KENNUNG: {}}
    check("2 eine leere Ruine wird nicht angefahren", st3._bots_ruinenzug(leer, 1000.0) == (False, ""))
    check("2 ohne Fahrt keine Beute", _kasse(leer) == 0.0, "%s" % _kasse(leer))

    st4 = _stand(besiegt=False)
    check("2 ein STEHENDER Drache ist kein Ruinenziel", st4._bots_ruinenzug(_bot(karren=2), 1000.0) == (False, ""))

    st5 = _stand()
    andere = _bot(karren=2, welt=(WELT % 6) + 1)
    check("2 ein Bot einer anderen Welt kommt nicht hin", st5._bots_ruinenzug(andere, 1000.0) == (False, ""))

    # -------------------------------------------------- 3. Gebucht ueber DENSELBEN Weg
    abschnitt("3. Der Weg ist der des Spielers (eine Buchstelle, keine zweite Beuteregel)")
    rumpf = _code(M.GameState._bots_ruinenzug)
    check("3 der Ruinenzug ruft den gemeinsamen Kampf-/Pluenderweg",
          "_drachen_kampf" in rumpf and "_drachen_ruine_pluendern" not in rumpf, "ruft _drachen_kampf")
    check("3 der Ruinenzug rechnet die Beute NICHT selbst",
          "beute_staffel" not in rumpf and "beute_am_ziel" not in rumpf, "keine eigene Beuterechnung")

    # --------------------------------------------------- 4. Eigene Forschung, nicht fremde
    abschnitt("4. Der Bot laedt mit SEINER Forschung (Wagenbau), nicht mit der des Spielers")
    st6 = _stand()
    klug = _bot(karren=2, forschung={"Wagenbau": 5})
    ok6, _ = st6._bots_ruinenzug(klug, 1000.0)
    mit_bonus = einheiten.ladung_der_gruppe({KARRE: 2}, {"Wagenbau": 5})
    check("4 mit Wagenbau 5 passt mehr in die Karren", mit_bonus > ladung, "%d > %d" % (mit_bonus, ladung))
    check("4 der Bot laedt die Menge MIT seinem Bonus", _kasse(klug) == float(mit_bonus),
          "%s statt %d" % (_kasse(klug), mit_bonus))
    check("4 die Spielerforschung bleibt aussen vor (der Stand hat keine)", bool(ok6))

    # ---------------------------------------------------------------- 5. Quellwachen
    abschnitt("5. Quellwachen: nur Karren reisen, und die Ruine kommt vor dem Drachen")
    check("5 der Zug enthaelt keine Kaempfer", "kaempfer" not in rumpf.lower(), "kein Kaempfer im Code")
    check("5 der Zug enthaelt keine Belagerung", "belagerung" not in rumpf.lower(), "keine Belagerung")
    check("5 der Zug reist mit `karren`", "karren" in rumpf, "Karren im Code")
    stelle_ruine = TEXT_MAIN.find("self._bots_ruinenzug(bot, jetzt)")
    stelle_drache = TEXT_MAIN.find("self._bots_drachenzug(bot, jetzt)")
    check("5 der Bot-Takt fragt die Ruine VOR dem Drachen",
          0 <= stelle_ruine < stelle_drache, "%d < %d" % (stelle_ruine, stelle_drache))
    check("5 die Entscheidung steht im Code benannt",
          "Frage 1" in TEXT_MAIN, "Verweis auf die Entscheidung")

    befund("Der Bericht der Ruine geht als Nachricht vom Typ 'kampf' ins Postfach - auch wenn ein "
           "BOT geraeumt hat. Das ist der gemeinsame Buchungsweg; ob der Spieler diese Meldung "
           "sehen soll, ist eine Anzeigefrage und keine Regel.")

    return bericht()


if __name__ == "__main__":
    sys.exit(haupt())
