# -*- coding: ascii -*-
"""AUSBILDUNG JE ORT - Stufe S-5a (03.11.2026, Daniels Entscheidung 4).

Daniels Vorgabe, woertlich: "S-5 Ausbildung je Ort (Warteschlange statt Kauf; Armee zieht in die
Doerfer und isst dort)". S-5b (Armee in den Doerfern) und S-5c (Essen je Dorf) sind gebaut; hier
kommt der letzte Teil: der Bot BILDET AUS statt zu kaufen.

Was diese Datei beweist
-----------------------
1. Der Bot startet eine Warteschlange ueber DENSELBEN Weg wie der Spieler
   (`spieloekonomie.ausbildung_start_menge`) - die Einheit steht NICHT sofort da.
2. Die Kosten zahlen das DORF (sein Lager faellt), nicht eine zweite Kasse.
3. Ist die Ausbildungszeit vorbei, steht die Einheit in GENAU DIESEM Dorf und damit in `bot.army`.
4. Ein Dorf OHNE Ausbildungsstaette bildet nichts aus, auch wenn das Reich reich ist ("Ort statt
   Reich").
5. Die Forschungsgrenze gilt: eine Einheit, deren Forschung fehlt, wird nicht begonnen.
6. Quellwachen: die Aufstellung ruft den Kern, und es gibt keine Sofort-Buchung der Armee mehr.

Aufruf:  python -X utf8 tests/test_bot_ausbildung_je_ort.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "quelltext"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['ausruestung', 'einheiten', 'main:*', 'spieloekonomie']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

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
import spieloekonomie as S  # noqa: E402
import ausruestung as A  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()


def dorf_mit_staette(name: str = "Haupt", staette: bool = True):
    """Ein Dorf, das ausbilden KANN - oder bewusst ohne Staette."""
    dorf = M.BotDorf(name=name, hauptdorf=True, karte="original-036",
                     vorraete={"holz": 5000.0, "stein": 5000.0, "nahrung": 5000.0,
                               "gold": 5000.0, "metall": 5000.0, "leder": 500.0, "wolle": 500.0},
                     bevoelkerung=200.0)
    if staette:
        dorf.bauten["7"] = "kriegerakademie"
        dorf.stufen["7"] = 1
        dorf.waren.update(A.fehlende("Krieger", {}))
    return dorf


def bot_mit(dorf):
    bot = M.BotPlayer("Pruefbot", "menschlich", 0.3, 0.5)
    bot.doerfer = [dorf]
    return bot


# ==========================================================================
abschnitt("1. Warteschlange statt Kauf")
# ==========================================================================
gs = M.GameState()
dorf = dorf_mit_staette()
bot = bot_mit(dorf)
gs.bots = [bot]
_vorher_armee = sum(int(v) for v in bot.army.values())
_vorher_lager = dict(dorf.vorraete)
_begonnen = gs.bot_armee_aufstellen(bot, 3600.0)
check("1 der Bot beginnt eine Ausbildung", isinstance(_begonnen, str) and bool(_begonnen),
      str(_begonnen))
check("1 die Einheit steht NOCH NICHT da (kein Kauf)", sum(int(v) for v in bot.army.values()) == _vorher_armee,
      str(bot.army))
check("1 der Auftrag steht in SEINEM Dorf", len(dorf.ausbildung) == 1, str(dorf.ausbildung))
check("1 der Auftrag traegt Einheit, Gebaeude, Start und Ende",
      all(k in (dorf.ausbildung[0] or {}) for k in ("einheit", "gebaeude", "start", "ende")),
      str(dorf.ausbildung[0]))
check("1 die Kosten zahlt das DORF (sein Lager ist kleiner geworden)",
      float(dorf.vorraete.get("nahrung", 0)) < float(_vorher_lager.get("nahrung", 0)),
      f"{_vorher_lager.get('nahrung')} -> {dorf.vorraete.get('nahrung')}")
check("1 die Ausbildungsdauer kommt aus dem Kern (nicht aus einer zweiten Zahl)",
      float(dorf.ausbildung[0]["ende"]) > float(dorf.ausbildung[0]["start"]),
      f"{dorf.ausbildung[0]['start']} -> {dorf.ausbildung[0]['ende']}")

# ==========================================================================
abschnitt("2. Die Einheit entsteht in DIESEM Dorf")
# ==========================================================================
_ende = float(dorf.ausbildung[0]["ende"])
_einheit = str(dorf.ausbildung[0]["einheit"])
dorf.ernte_seit = 3600.0                    # das Dorf hat schon geerntet (sonst setzt der erste Takt nur die Zeit)
M.bot_doerfer_ernten(bot, _ende + 10.0, M.bot_wirtschaft_einstellungen())   # Karten-Weg bucht faellig
check("2 nach der Ausbildungszeit steht die Einheit im Dorf",
      int(dorf.einheiten.get(_einheit, 0)) == 1, str(dorf.einheiten))
check("2 und damit in der Armee des Bots", int(bot.army.get(_einheit, 0)) == 1, str(bot.army))
check("2 der Auftrag ist als gebucht markiert (kein zweites Mal)",
      bool(dorf.ausbildung[0].get("gebucht")), str(dorf.ausbildung[0]))
M.bot_doerfer_ernten(bot, _ende + 20.0, M.bot_wirtschaft_einstellungen())
check("2 ein zweiter Takt bucht NICHT doppelt", int(dorf.einheiten.get(_einheit, 0)) == 1,
      str(dorf.einheiten))

# ==========================================================================
abschnitt("3. Ort statt Reich: ohne Staette keine Ausbildung")
# ==========================================================================
gs2 = M.GameState()
ohne = dorf_mit_staette("Ohne", staette=False)
bot2 = bot_mit(ohne)
gs2.bots = [bot2]
check("3 ohne Ausbildungsstaette beginnt der Bot nichts", gs2.bot_armee_aufstellen(bot2, 3600.0) is None,
      str(ohne.ausbildung))
check("3 und es steht kein Auftrag in der Warteschlange", ohne.ausbildung == [], str(ohne.ausbildung))
check("3 das reiche Lager bleibt unangetastet",
      float(ohne.vorraete.get("nahrung", 0)) == 5000.0, str(ohne.vorraete.get("nahrung")))

# ==========================================================================
abschnitt("4. Die Forschungsgrenze gilt auch fuer den Bot")
# ==========================================================================
grenzen = S.ausbildung_grenzen(M.bot_dorf_als_ort(dorf_mit_staette("F"), bot_mit(dorf_mit_staette("F"))),
                              "Krieger", {})
check("4 ein Krieger braucht Kriegskunst (der Kern verweigert ohne Forschung)",
      "Kriegskunst" in str(grenzen.get("hindernis")), str(grenzen.get("hindernis"))[:80])
check("4 der Bot bildet dann eine Einheit aus, die er wirklich darf",
      bool(_begonnen) and _begonnen != "Krieger", str(_begonnen))

# ==========================================================================
abschnitt("5. Quellwachen")
# ==========================================================================


def _code(fn) -> str:
    baum = ast.parse(textwrap.dedent(inspect.getsource(fn)))
    knoten = baum.body[0]
    if (isinstance(knoten, ast.FunctionDef) and knoten.body
            and isinstance(knoten.body[0], ast.Expr)
            and isinstance(knoten.body[0].value, ast.Constant)):
        knoten.body = knoten.body[1:] or [ast.Pass()]
    return ast.unparse(baum)


_aufstellen = _code(M.GameState.bot_armee_aufstellen)
check("5 die Aufstellung ruft den Kern-Weg", "ausbildung_start_menge" in _aufstellen,
      "main.GameState.bot_armee_aufstellen")
check("5 sie bucht die Einheit NICHT mehr sofort",
      "bot_armee_buchen" not in _aufstellen, "keine Sofort-Buchung mehr")
check("5 sie schreibt den Auftrag ins Dorf", "bot_dorf_aus_ort" in _aufstellen, "")
check("5 der Kern hat EINE Abschluss-Regel fuer alle Wege",
      "ausbildung_abschluss(neu, bis)" in open(os.path.join(SRC, "spieloekonomie.py"),
                                               encoding="utf-8").read(),
      "spieloekonomie.ort_tick")
check("5 der Karten-Weg der Bots bucht faellige Ausbildungen ebenfalls",
      "spieloekonomie.ausbildung_abschluss(_ort, jetzt)" in TEXT_MAIN, "main.bot_doerfer_ernten")

befund("5 ehrliche Grenze: der Bot bildet nur Kaempfer und Kundschafter aus (VORSCHLAG dieser "
       "Sitzung, wie bisher) und nur, wenn die Kaufbremse (`bot_nahrung_deckt`) es erlaubt. Karren "
       "und Belagerungswaffen stellt er weiterhin nicht selbst her - das waere ein eigener Schnitt.",
       "")

sys.exit(bericht())
