# -*- coding: ascii -*-
"""S-6: BOTS GRUENDEN NACH - hoechstens vier Doerfer je Bot (03.11.2026, Daniels Vorgabe).

Daniels Vorgabe, woertlich-nah: "Nachgruenden, 3 Gruendungen je Bot = 4 Doerfer".

DAS PROBLEM, GEMESSEN (vor dem Bau)
-----------------------------------
Ein Bot konnte ueberhaupt kein Dorf gruenden: `bot_doerfer_sicherstellen` legte nur Datensaetze
fuer die Namen an, die der Kartenaufbau beim Start vergeben hatte. Dazu kam ein zweiter Befund:
der KERN verlangt fuer eine Gruendung einen SIEDLERKARREN (`spieloekonomie.REGELN["gruendung"]`),
und den kann ein Bot nicht bauen - seine Doerfer fuehren nur gold, holz, metall, nahrung, stein,
weil die Bot-Wirtschaft keine Werkstattkette kennt (gemessen 03.11.2026). Deshalb steht der
Schalter `siedlerkarren_pflicht` in `data/bot_gruendung.json`; er ist AUS, und die Siedler des
Karrens ziehen direkt aus dem Ausgangsdorf um. Die Kosten bleiben die des Kerns.

Was diese Datei beweist
-----------------------
1. Die Zahlen kommen aus dem KERN (`spieloekonomie.gruendungskosten`, `REGELN["gruendung"]`) -
   keine zweite Kostentabelle im Code.
2. Die Wachen greifen: ohne Forschung, ohne Mindestbestand, ohne Siedler, ueber der Hoechstzahl
   und innerhalb der Sperre gruendet der Bot NICHT (und bucht nichts).
3. Eine echte Gruendung: viertes Dorf in der HEIMATWELT, eigene Karte, Startpaket, Siedler
   umgezogen, Gebuehr bezahlt, Postfach-Bericht, und das neue Dorf traegt Ertrag.
4. In 24 Spieltagen kommt JEDER Bot auf vier Doerfer (er forscht Wagenbau, weil die
   Forschungsliste ihn ergaenzt) - die Vorgabe ist also im Spiel erreichbar, nicht nur im Test.
5. Quellwachen: der Bot-Takt ruft die Gruendung, und die Forschungsliste ergaenzt die
   Gruendungsforschung, solange der Bot unter der Hoechstzahl steht.

Aufruf:  python -X utf8 tests/test_bot_gruendung.py
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
sys.path[:0] = [os.path.join(ROOT, "tools")]
import gpt_erzeuge_startstaende as starter  # noqa: E402
import main as M  # noqa: E402
import spieloekonomie as S  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
EINST = M.bot_gruendung_einstellungen()
REGEL = dict(S.REGELN.get("gruendung") or {})
PREIS, PAKET, MINIMUM = S.gruendungskosten()


def _dorf(name, welt=4, vorraete=None, bevoelkerung=20.0, karte="", haupt=False):
    """Ein Bot-Dorf fuer die Pruefung - nur die Felder, die die Gruendung liest."""
    return M.BotDorf(name=name, x=0, y=0, herkunftswelt=welt, dimension=welt, hauptdorf=haupt,
                     karte=karte, bevoelkerung=float(bevoelkerung), vorraete=dict(vorraete or {}))


def _bot(name, doerfer, fraktion="menschlich", wagenbau=1):
    """Ein Bot mit Forschungsstand - Wagenbau ist die Gruendungsforschung des Kerns."""
    return M.BotPlayer(name, fraktion, 0.0, 0.0, doerfer=list(doerfer),
                       forschungsstaende={REGEL.get("forschung") or "Wagenbau": int(wagenbau)})


def _reich(vorfaktor=2.0):
    """Genug Vorrat fuer eine Gruendung - die Zahlen kommen aus dem Kern, nicht aus dem Test."""
    return {stoff: float(soll) * float(vorfaktor) for stoff, soll in MINIMUM.items()}


def _code(fn):
    """Der Quelltext einer Funktion OHNE Docstring - ein Kommentar darf keine Wache faerben."""
    baum = ast.parse(textwrap.dedent(inspect.getsource(fn)))
    knoten = baum.body[0]
    if (isinstance(knoten, ast.FunctionDef) and knoten.body
            and isinstance(knoten.body[0], ast.Expr)
            and isinstance(knoten.body[0].value, ast.Constant)):
        knoten.body = knoten.body[1:] or [ast.Pass()]
    return ast.unparse(baum)


# ==========================================================================
abschnitt("1. Die Zahlen kommen aus dem KERN, nicht aus einer zweiten Tabelle")
# ==========================================================================
check("1 die Gruendung ist eingeschaltet", bool(EINST.get("aktiv", False)), str(EINST.get("aktiv")))
check("1 hoechstens vier Doerfer je Bot (Daniels Zahl)", int(EINST.get("hoechstens_doerfer") or 0) == 4,
      str(EINST.get("hoechstens_doerfer")))
check("1 die Forschungsregel ist die des Kerns (Wagenbau, Stufe 1)",
      str(REGEL.get("forschung")) == "Wagenbau" and int(REGEL.get("stufe") or 0) == 1,
      "%s / %s" % (REGEL.get("forschung"), REGEL.get("stufe")))
check("1 Gebuehr, Startpaket und Mindestbestand sind die des Kerns",
      set(MINIMUM) == set(PREIS) and all(abs(float(MINIMUM[k]) - (float(PREIS.get(k, 0)) + float(PAKET.get(k, 0)))) < 1e-6
                                        for k in MINIMUM),
      "Mindestbestand %s" % MINIMUM)
_check_pflicht = bool(EINST.get("siedlerkarren_pflicht", True))
if _check_pflicht:
    befund("1 Siedlerkarren ist PFLICHT - dann kann kein Bot gruenden, solange er keine Warenkette hat",
           "siedlerkarren_pflicht = True")
else:
    befund("1 ehrliche Abweichung: der Siedlerkarren ist fuer Bots NICHT Pflicht (Kernregel verlangt ihn)",
           "Siedler ziehen direkt aus dem Ausgangsdorf, Gebuehr und Startpaket werden voll bezahlt")

# ==========================================================================
abschnitt("2. Die Wachen: ohne Forschung, Vorrat, Siedler, Sperre und Platz wird nicht gegruendet")
# ==========================================================================
gs = M.GameState()

# 2a: keine Forschung
ohne_forschung = _bot("OhneForschung", [_dorf("Dorf 1", vorraete=_reich(), haupt=True)], wagenbau=0)
check("2 ohne die Forschungsstufe des Kerns keine Gruendung",
      gs.bot_dorf_gruenden(ohne_forschung, 1000.0) is None)
check("2 dabei wird nichts gebucht (Doerfer bleiben, wie sie sind)",
      len(M.bot_doerfer_sicherstellen(ohne_forschung)) == 1)

# 2b: zu wenig Vorrat
arm = _bot("Arm", [_dorf("Dorf 1", vorraete={k: float(v) * 0.5 for k, v in MINIMUM.items()}, haupt=True)])
check("2 unter dem Mindestbestand des Kerns keine Gruendung", gs.bot_dorf_gruenden(arm, 1000.0) is None)
check("2 das Dorf behaelt seinen Vorrat unveraendert",
      abs(float(arm.doerfer[0].vorraete.get("holz", 0)) - float(MINIMUM["holz"]) * 0.5) < 1e-6,
      str(arm.doerfer[0].vorraete.get("holz")))

# 2c: zu wenige Siedler
wenig_leute = _bot("WenigLeute", [_dorf("Dorf 1", vorraete=_reich(), bevoelkerung=1.0, haupt=True)])
check("2 zu wenige Siedler im Ausgangsdorf: keine Gruendung",
      gs.bot_dorf_gruenden(wenig_leute, 1000.0) is None)

# 2d: Hoechstzahl erreicht
voll = _bot("Voll", [_dorf("Dorf %d" % i, vorraete=_reich(), haupt=(i == 1)) for i in range(1, 5)])
check("2 mit vier Doerfern ist Schluss (Daniels Hoechstzahl)",
      gs.bot_dorf_gruenden(voll, 1000.0) is None)
check("2 es bleibt bei vier Doerfern", len(M.bot_doerfer_sicherstellen(voll)) == 4)

# 2e: Sperre und echte Gruendung
frisch = _bot("Frisch", [_dorf("Dorf 1", vorraete=_reich(4.0), haupt=True, karte="original-001")])
erstes = gs.bot_dorf_gruenden(frisch, 1000.0)
check("2 eine echte Gruendung gelingt", erstes is not None, str(getattr(erstes, "name", None)))
zweites = gs.bot_dorf_gruenden(frisch, 1060.0)
check("2 die Sperre verhindert die zweite Gruendung im selben Zeitfenster", zweites is None)
check("2 nach Ablauf der Sperre geht die naechste Gruendung",
      gs.bot_dorf_gruenden(frisch, 1000.0 + float(EINST.get("sperre_stunden") or 0) * 3600.0 + 1.0) is not None,
      "Sperre %s h" % EINST.get("sperre_stunden"))

# ==========================================================================
abschnitt("3. Eine Gruendung, nachgerechnet: Heimatwelt, Karte, Startpaket, Gebuehr, Ertrag")
# ==========================================================================
gs2 = M.GameState()
quelle_vorher = {k: float(v) for k, v in _reich(2.0).items()}
bot = _bot("Haug", [_dorf("Haugs Siedlung 1", vorraete=quelle_vorher, karte="original-011", haupt=True)])
vorher_siedler = float(bot.doerfer[0].bevoelkerung)
neu = gs2.bot_dorf_gruenden(bot, 5000.0)

check("3 die Gruendung liefert ein neues Dorf", neu is not None)
if neu is not None:
    check("3 das neue Dorf ist ein NEBENDORF (kein Hauptdorf)", bool(getattr(neu, "hauptdorf", False)) is False)
    check("3 es steht in der HEIMATWELT des Bots (W-1)",
          int(neu.dimension) == 4 and int(neu.herkunftswelt) == 4,
          "%s / %s" % (neu.dimension, neu.herkunftswelt))
    check("3 es traegt eine Karte, die der Bot noch nicht hatte",
          bool(neu.karte) and str(neu.karte) != "original-011", str(neu.karte))
    check("3 es bekommt das Startpaket des Kerns",
          all(abs(float(neu.vorraete.get(k, -1)) - float(v)) < 1e-6 for k, v in PAKET.items()),
          str(neu.vorraete))
    check("3 die Siedler sind umgezogen (Anzahl aus den Einheitendaten)",
          float(neu.bevoelkerung) > 0 and
          abs(float(bot.doerfer[0].bevoelkerung) - (vorher_siedler - float(neu.bevoelkerung))) < 1e-6,
          "neu %.1f, alt %.1f -> %.1f" % (neu.bevoelkerung, vorher_siedler, bot.doerfer[0].bevoelkerung))
    check("3 das Ausgangsdorf hat Gebuehr + Startpaket bezahlt (Mindestbestand des Kerns)",
          all(abs(float(bot.doerfer[0].vorraete.get(k, -1))
                  - (float(quelle_vorher[k]) - float(MINIMUM[k]))) < 1e-6 for k in MINIMUM),
          str(bot.doerfer[0].vorraete))
    check("3 das neue Dorf hat eine Position auf der Karte",
          int(neu.x) != 0 or int(neu.y) != 0, "%s/%s" % (neu.x, neu.y))
    check("3 der Bot zaehlt das Dorf in seiner Dorfliste", len(M.bot_doerfer_sicherstellen(bot)) == 2)
    check("3 die Namensliste des Spielstands kennt es auch",
          str(neu.name) in [str(n) for n in (bot.settlements or [])], str(bot.settlements))
    check("3 der Bericht steht im Postfach",
          any(m.get("type") == "gruendung" and "neues Dorf" in str(m.get("text")) for m in gs2.messages),
          str([m.get("type") for m in gs2.messages]))
    ertrag = M.bot_dorf_ertrag(neu)
    check("3 das neue Dorf traegt Ertrag (es ist ein echtes Dorf, kein Datensatz)",
          sum(float(v) for v in ertrag.values()) > 0, str({k: round(v, 2) for k, v in ertrag.items()}))

# ==========================================================================
abschnitt("4. Im Spiel erreichbar: nach 24 Spieltagen hat JEDER Bot vier Doerfer")
# ==========================================================================
spiel = starter.neu_erzeugen()
zeit = 0.0
while zeit <= 86400.0 * 24:
    zeit += 3600.0 * 6
    spiel.bots_fortschreiben(zeit)
zahlen = []
for je_bot in spiel.bots:
    zahlen.append((je_bot.name, len(M.bot_doerfer_sicherstellen(je_bot))))
check("4 jeder Bot hat nach 24 Spieltagen vier Doerfer (Daniels Zahl)",
      all(n == 4 for _name, n in zahlen), str(zahlen))
check("4 kein Bot hat mehr als vier", all(n <= 4 for _name, n in zahlen), str(zahlen))
check("4 alle neuen Doerfer stehen in der Heimatwelt ihres Bots",
      all(int(d.dimension) == int(d.herkunftswelt)
          for je_bot in spiel.bots for d in M.bot_doerfer_sicherstellen(je_bot)))
check("4 jeder Bot haelt vier VERSCHIEDENE Karten",
      all(len({str(d.karte) for d in M.bot_doerfer_sicherstellen(je_bot)}) == 4
          for je_bot in spiel.bots),
      str([[d.karte for d in M.bot_doerfer_sicherstellen(b)] for b in spiel.bots]))
check("4 die Gruendungen stehen als Nachricht im Postfach",
      sum(1 for m in spiel.messages if m.get("type") == "gruendung") >= 11,
      str(sum(1 for m in spiel.messages if m.get("type") == "gruendung")))

# ==========================================================================
abschnitt("5. Quellwachen")
# ==========================================================================
check("5 der Bot-Takt ruft die Gruendung", "bot_dorf_gruenden(" in TEXT_MAIN)
check("5 die Gruendung liest die Kosten aus dem KERN",
      "spieloekonomie.gruendungskosten()" in _code(M.GameState.bot_dorf_gruenden))
# `ast.unparse` setzt EINFACHE Anfuehrungszeichen - auf den Wortlaut des Schlussels pruefen.
check("5 die Gruendung liest die Forschungsregel aus dem KERN",
      "spieloekonomie.REGELN.get('gruendung')" in _code(M.GameState.bot_dorf_gruenden))
check("5 die Hoechstzahl steht in der Datendatei, nicht im Code",
      "hoechstens_doerfer" in open(os.path.join(ROOT, "data", "bot_gruendung.json"),
                                   encoding="utf-8").read())
# Kommentare ueberleben `ast.unparse` NICHT - geprueft wird deshalb auf den Quelltext selbst,
# nicht auf einen Kommentar (der zaehlt nicht als Code).
check("5 die Forschungsliste ergaenzt die Gruendungsforschung",
      "bot_gruendung_einstellungen()" in _code(M.bot_dorf_forschungsliste)
      and "bis_stufe" in _code(M.bot_dorf_forschungsliste))

sys.exit(bericht())
