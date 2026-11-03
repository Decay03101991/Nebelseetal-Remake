# -*- coding: ascii -*-
"""DIE ARMEE STEHT IN DEN DOERFERN - Stufe S-5b/S-5c (03.11.2026).

Daniels Vorgabe (12:20): "S-5 Ausbildung je Ort (Warteschlange statt Kauf; Armee zieht in die
Doerfer und isst dort)". Der Docstring von `bot_dorf_tick` sagt, warum das ZUERST kommen muss:
"sobald S-5 Einheiten je Ort ausbildet, muss die Armee dort hineinwandern (sonst isst sie zweimal)".

Was diese Datei beweist
-----------------------
1. `bot.army` ist die SUMME der Dorf-Garnisonen (eine Wahrheit), und ein Schreibzugriff auf die
   Eigenschaft aendert nichts still (der B-3-Fehler).
2. `bot_armee_buchen` ist der EINE Schreiber: positiv, negativ, nie unter 0, zweimal 0 == 0.
3. Ein alter Spielstand mit `armee` am Bot landet EINMALIG im Hauptdorf - die Summe bleibt gleich.
4. Jedes Dorf isst fuer seine EIGENE Garnison; ein Dorf ohne Einheiten isst nichts.
5. Quellwachen: kein `bot.army[...] = ...` mehr in `src/`, die Eigenschaft existiert, das Feld nicht.

Aufruf:  python -X utf8 tests/test_bot_armee_je_dorf.py
"""
from __future__ import annotations

import ast
import inspect
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
sys.path[:0] = [SRC, os.path.join(ROOT, "tools")]
import main as M  # noqa: E402
import botkern as BK  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()


def neuer_bot(doerfer: int = 2, armee=None):
    """Ein Bot mit mehreren Doerfern (Hauptdorf = das erste) und optional einer Armee."""
    bot = M.BotPlayer("Pruefbot", BK.BOT_FRAKTIONEN[BK.BOT_NAMEN[0]], 0.3, 0.5)
    bot.doerfer = [M.BotDorf(name="Haupt" if i == 0 else "Neben%d" % i, hauptdorf=(i == 0),
                             vorraete={"nahrung": 1000.0})
                   for i in range(max(1, doerfer))]
    if armee:
        bot.army = dict(armee)                      # Setter verteilt auf die Doerfer
    return bot


# ==========================================================================
abschnitt("1. Die Armee ist die Summe der Doerfer")
# ==========================================================================
bot = neuer_bot(3)
bot.doerfer[0].einheiten = {"Krieger": 4}
bot.doerfer[2].einheiten = {"Krieger": 3, "Bogenschuetze": 2}
check("1 die Summe zaehlt ALLE Doerfer", M.bot_armee(bot) == {"Krieger": 7, "Bogenschuetze": 2},
      str(M.bot_armee(bot)))
check("1 `bot.army` liest dieselbe Summe", bot.army == {"Krieger": 7, "Bogenschuetze": 2},
      str(bot.army))
check("1 ein Dorf ohne Einheiten traegt nichts bei", bot.doerfer[1].einheiten == {}, "")
# Der B-3-Fehler: auf die EIGENSCHAFT zu schreiben darf nichts bewirken.
_vor = dict(bot.army)
bot.army["Krieger"] = 999                                                   # landet in einer Kopie
check("1 ein Schreibzugriff auf `bot.army[...]` aendert NICHTS (B-3-Fehler ausgeschlossen)",
      bot.army == _vor, f"{_vor} gegen {bot.army}")
bot.army = {"Krieger": 5}                                                   # der Setter verteilt
check("1 der Setter legt die Armee ins HAUPTDORF", bot.doerfer[0].einheiten == {"Krieger": 5}
      and bot.doerfer[2].einheiten == {}, str([d.einheiten for d in bot.doerfer]))

# ==========================================================================
abschnitt("2. bot_armee_buchen: der EINE Schreiber")
# ==========================================================================
bot2 = neuer_bot(2)
check("2 buchen legt die Einheit ins Hauptdorf", M.bot_armee_buchen(bot2, "Krieger", 3) == 3,
      str(bot2.doerfer[0].einheiten))
check("2 nochmal buchen zaehlt dazu", M.bot_armee_buchen(bot2, "Krieger", 2) == 5,
      str(bot2.doerfer[0].einheiten))
check("2 abbuchen geht", M.bot_armee_buchen(bot2, "Krieger", -4) == 1, str(bot2.doerfer[0].einheiten))
check("2 unter 0 geht nicht", M.bot_armee_buchen(bot2, "Krieger", -99) == 0,
      str(bot2.doerfer[0].einheiten))
check("2 eine auf 0 gebuchte Einheit steht nicht mehr im Dorf",
      "Krieger" not in bot2.doerfer[0].einheiten, str(bot2.doerfer[0].einheiten))
check("2 zweimal 0 buchen aendert nichts",
      M.bot_armee_buchen(bot2, "Krieger", 0) == 0 and bot2.army == {}, str(bot2.army))
check("2 auf ein bestimmtes Dorf buchen geht",
      M.bot_armee_buchen(bot2, "Bogenschuetze", 2, bot2.doerfer[1]) == 2
      and bot2.doerfer[1].einheiten == {"Bogenschuetze": 2}, str(bot2.doerfer[1].einheiten))

# ==========================================================================
abschnitt("3. Alter Spielstand mit `armee` am Bot")
# ==========================================================================
alt = {"name": "Alt", "faction": "menschlich", "aggression": 0.5, "trading": 0.5,
       "settlements": ["Alts Siedlung 1", "Alts Siedlung 2"],
       "armee": {"Krieger": 6, "Bogenschuetze": 4}, "vorraete": {"holz": 50}}
geladen = M.bot_aus_stand(alt)
check("3 die Armee kommt im Hauptdorf an",
      geladen.doerfer[0].einheiten == {"Krieger": 6, "Bogenschuetze": 4},
      str(geladen.doerfer[0].einheiten))
check("3 die Summe ist dieselbe wie vorher (keine Verdopplung)", geladen.army == {"Krieger": 6,
                                                                                  "Bogenschuetze": 4},
      str(geladen.army))
_zweite = M.bot_aus_stand(M.asdict(geladen) if hasattr(M, "asdict") else
                          {"name": "Alt", "faction": "menschlich", "aggression": 0.5,
                           "trading": 0.5, "settlements": ["Alts Siedlung 1"],
                           "doerfer": [{"name": "Alts Siedlung 1", "hauptdorf": True,
                                        "einheiten": {"Krieger": 6, "Bogenschuetze": 4}}]})
check("3 ein NEUER Spielstand (Armee in den Doerfern) laedt ohne Verdopplung",
      _zweite.army == {"Krieger": 6, "Bogenschuetze": 4}, str(_zweite.army))

# ==========================================================================
abschnitt("4. Essen je Dorf (S-5c)")
# ==========================================================================
bot3 = neuer_bot(2)
bot3.doerfer[1].einheiten = {"Krieger": 10}                                 # nur das Nebendorf hat Truppen
_essen_neben = M.bot_futter_buchen(bot3, bot3.doerfer[1], 0.0, 86400.0)
_essen_haupt = M.bot_futter_buchen(bot3, bot3.doerfer[0], 0.0, 86400.0)
check("4 das Dorf MIT Garnison isst", float(_essen_neben.get("verbrauch") or 0) > 0,
      str(_essen_neben))
check("4 das Dorf OHNE Garnison isst nichts", float(_essen_haupt.get("verbrauch") or 0) == 0.0,
      str(_essen_haupt))

# ==========================================================================
abschnitt("5. Quellwachen")
# ==========================================================================


def _code(fn) -> str:
    """Der Quelltext einer Funktion OHNE Docstring (sonst faerbt die eigene Erklaerung rot)."""
    baum = ast.parse(textwrap.dedent(inspect.getsource(fn)))
    knoten = baum.body[0]
    if (isinstance(knoten, ast.FunctionDef) and knoten.body
            and isinstance(knoten.body[0], ast.Expr)
            and isinstance(knoten.body[0].value, ast.Constant)):
        knoten.body = knoten.body[1:] or [ast.Pass()]
    return ast.unparse(baum)


check("5 `BotPlayer` hat KEIN Feld `army` mehr",
      "army: Dict[str, int] = field(" not in TEXT_MAIN, "main.BotPlayer")
check("5 `bot.army` ist eine Eigenschaft", "@property" in _code(M.BotPlayer.army.fget)
      and "bot_armee(self)" in _code(M.BotPlayer.army.fget), "main.BotPlayer.army")
_schreibstellen = [z for z in TEXT_MAIN.splitlines() if z.strip().startswith("bot.army[")]
check("5 in `src/` schreibt niemand mehr auf `bot.army[...]`", not _schreibstellen,
      str(_schreibstellen[:3]))
# ENTSCHEIDUNG GEAENDERT (S-5a, 03.11.2026): der KAUF bucht nicht mehr selbst - er startet eine
# Warteschlange (die Einheit entsteht im Dorf). Der EINE Schreiber bleibt fuer Verluste und fuer
# alles, was eine Armee auf einmal setzt.
check("5 der Verlust bucht ueber den EINEN Schreiber",
      TEXT_MAIN.count("bot_armee_buchen(bot, name, -int(menge))") == 1, "")
check("5 der Kauf bucht NICHT mehr direkt, sondern bildet aus",
      "bot_armee_buchen(bot, name, 1" not in TEXT_MAIN
      and "ausbildung_start_menge" in TEXT_MAIN, "")

befund("5 ehrliche Grenze: die Armee steht im HAUPTDORF, bis S-5a die Ausbildung je Ort baut - erst "
       "dann entstehen Einheiten dort, wo die Kaserne steht. Das Essen rechnet schon jetzt je Dorf "
       "(S-5c), damit die Umstellung keine zweite Wahrheit erzeugt.", "")

sys.exit(bericht())
