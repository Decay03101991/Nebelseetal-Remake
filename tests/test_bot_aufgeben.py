# -*- coding: ascii -*-
"""Register 228: Bots gruenden, beurteilen und GEBEN AUF - mit Ruecklage und Sperre.

DIE ENTSCHEIDUNG (Daniel, 05.11.2026, Register 228, Antwort 3, woertlich-nah)
----------------------------------------------------------------------------
"Der Bot gruendet, beurteilt und gibt auf, wenn die Karte fuer seine Taktik zu schlecht ist - aber
er muss die Kosten aus seiner Rohstoffproduktion erneut ansparen koennen." Dafuer ist ausdruecklich
eine geeignete Loesung gefordert.

DIE GEMESSENE GEFAHR
--------------------
Die erste Fassung warf die Bots von vier Doerfern auf eines zurueck (`test_bot_gruendung` 3 rot):
jede zweite Karte liegt unter dem Durchschnitt, und der Bot gruendete und verwarf im Minutentakt.
Deshalb hat die neue Fassung vier Sperren (GameState.bot_siedlung_aufgeben):
1. RUECKLAGE - die Gebuehr geht VOR dem Aufgeben in das zahlende Dorf zurueck, und aufgegeben wird
   nur, wenn danach ein anderes Dorf die naechste Gruendung bezahlen kann (Kosten aus dem KERN).
2. SPERRE je Bot (`aufgeben.sperre_stunden`).
3. ERINNERUNG - eine abgelehnte Karte kauft derselbe Bot nicht wieder (`abgelehnte_karten`).
4. ABBRUCH - nie das Hauptdorf, nie das letzte Dorf, hoechstens `aufgeben.aufgaben_max`.

Was diese Datei beweist
-----------------------
1. Die Regeln stehen in `data/bot_gruendung.json`, die Kosten kommen aus dem KERN.
2. Eine Aufgabe bucht: Dorf weg, Gebuehr zurueckgelegt, Erinnerung geschrieben, Bericht im Postfach.
3. Eine tragende Karte, ein fehlendes Zahlungsziel, die Sperre und die Abbruchregel verhindern die
   Aufgabe - und buchen dabei NICHTS.
4. Das Hauptdorf ist nie aufgebenbar.
5. Die Gruendung kauft eine abgelehnte Karte nicht wieder.

Aufruf:  python -X utf8 tests/test_bot_aufgeben.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
import main as M  # noqa: E402
import originalkarten as O  # noqa: E402
import spieloekonomie as S  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
EINST = M.bot_gruendung_einstellungen()
AUFGABE = dict(EINST.get("aufgeben") or {})
REGEL = dict(S.REGELN.get("gruendung") or {})
PREIS, PAKET, MINIMUM = S.gruendungskosten()
SPERRE_H = float(AUFGABE.get("sperre_stunden") or 0.0)


def _dorf(name, karte, vorraete=None, haupt=False, welt=4):
    """Ein Bot-Dorf mit den Feldern, die Urteil und Aufgabe lesen."""
    return M.BotDorf(name=name, x=0, y=0, herkunftswelt=welt, dimension=welt, hauptdorf=haupt,
                     karte=str(karte or ""), bevoelkerung=20.0, vorraete=dict(vorraete or {}))


def _bot(doerfer, name="Haug", wagenbau=1):
    """Ein Bot mit Forschungsstand (Wagenbau ist die Gruendungsforschung des Kerns)."""
    b = M.BotPlayer(name, "menschlich", 0.3, 0.5, doerfer=list(doerfer),
                    forschungsstaende={REGEL.get("forschung") or "Wagenbau": int(wagenbau)})
    b.gedaechtnis = {}
    b.settlements = [str(d.name) for d in doerfer]
    return b


def _reich(vorfaktor=2.0):
    """Genug Vorrat, dass eine Gruendung bezahlbar bleibt - Zahlen aus dem KERN."""
    return {stoff: float(soll) * float(vorfaktor) for stoff, soll in MINIMUM.items()}


def _karten():
    """(tragende Karte, nicht tragende Karte) fuer die Taktik eines Probebots."""
    probe = _bot([])
    gut, schlecht = "", ""
    for kennung in sorted(O.kennungen()):
        urteil = M.bot_kartenurteil(probe, kennung)
        if urteil["gut_genug"] and not gut:
            gut = kennung
        if (not urteil["gut_genug"]) and not schlecht:
            schlecht = kennung
        if gut and schlecht:
            break
    return gut, schlecht


_GUT, _SCHLECHT = _karten()

# ==========================================================================
abschnitt("1. Die Regeln stehen in der Datendatei, die Kosten im KERN")
# ==========================================================================

check("1 die Aufgabe ist eingeschaltet", bool(AUFGABE.get("aktiv", False)), str(AUFGABE.get("aktiv")))
check("1 die Sperre ist eine Zahl aus der Datei", SPERRE_H > 0, str(SPERRE_H))
check("1 die Erinnerung ist eine Zahl aus der Datei",
      int(AUFGABE.get("erinnerung_max") or 0) >= 1, str(AUFGABE.get("erinnerung_max")))
check("1 die Abbruchregel ist eine Zahl aus der Datei",
      int(AUFGABE.get("aufgaben_max") or 0) >= 1, str(AUFGABE.get("aufgaben_max")))
check("1 die Datendatei nennt den Grund der Sperre",
      "Drehschleife" in str(AUFGABE.get("bedingungen") or "")
      or "Ruecklage" in str(AUFGABE.get("bedingungen") or ""), str(AUFGABE.get("bedingungen"))[:80])
check("1 es gibt je Taktik Karten ueber und unter dem Durchschnitt",
      bool(_GUT) and bool(_SCHLECHT), "%s / %s" % (_GUT, _SCHLECHT))
_bad = M.bot_kartenurteil(_bot([]), _SCHLECHT)
check("1 die schlechte Karte liegt wirklich unter dem Durchschnitt",
      _bad["gut_genug"] is False and _bad["punkte"] < _bad["durchschnitt"],
      "%.2f / %.2f" % (_bad["punkte"], _bad["durchschnitt"]))

# ==========================================================================
abschnitt("2. Eine Aufgabe bucht: Ruecklage, Dorf weg, Erinnerung, Bericht")
# ==========================================================================

gs = M.GameState()
_main = _dorf("Haupt", _GUT, _reich(2.0), haupt=True)
_jung = _dorf("Zweites", _SCHLECHT, {"holz": 10.0})
bot = _bot([_main, _jung])
vorher = {k: float(v) for k, v in _main.vorraete.items()}
bericht1 = gs.bot_siedlung_aufgeben(bot, 1000.0)

check("2 die Aufgabe meldet einen Bericht", isinstance(bericht1, dict), str(bericht1))
if isinstance(bericht1, dict):
    check("2 der Bericht nennt Bot, Dorf und Karte",
          bericht1.get("bot") == "Haug" and bericht1.get("dorf") == "Zweites"
          and bericht1.get("karte") == _SCHLECHT, str(bericht1))
    check("2 der Bericht nennt die Ruecklage in allen drei Rohstoffen",
          set(bericht1.get("ruecklage") or {}) == set(PREIS),
          str(sorted((bericht1.get("ruecklage") or {}))))
check("2 das juengste Dorf ist weg", len(bot.doerfer) == 1, str([d.name for d in bot.doerfer]))
check("2 die Namensliste des Spielstands kennt es nicht mehr",
      [str(n) for n in bot.settlements] == ["Haupt"], str(bot.settlements))
check("2 die Gebuehr ist in das zahlende Dorf zurueckgelegt",
      all(abs(float(_main.vorraete.get(k, 0.0)) - (vorher[k] + float(PREIS[k]))) < 1e-6
          for k in PREIS),
      str(_main.vorraete))
check("2 die Sperre je Bot beginnt jetzt",
      abs(float(bot.gedaechtnis.get("aufgabe_seit") or 0.0) - 1000.0) < 1e-6,
      str(bot.gedaechtnis.get("aufgabe_seit")))
check("2 die Aufgabe ist gezaehlt", int(bot.gedaechtnis.get("aufgabe_anzahl") or 0) == 1,
      str(bot.gedaechtnis.get("aufgabe_anzahl")))
check("2 die Karte ist in der Erinnerung",
      int((bot.gedaechtnis.get("abgelehnte_karten") or {}).get(_SCHLECHT) or 0) == 1,
      str(bot.gedaechtnis.get("abgelehnte_karten")))
check("2 der Bot darf neu gruenden (Sperre der Gruendung aufgehoben)",
      float(bot.gedaechtnis.get("gruendung_seit") or 0.0) == 0.0,
      str(bot.gedaechtnis.get("gruendung_seit")))
check("2 die Kasse ist die Summe der Doerfer",
      all(abs(float(bot.vorraete.get(k, 0) or 0) - round(float(_main.vorraete.get(k, 0.0)))) <= 1.0
          for k in PREIS), str(bot.vorraete))
check("2 der Bericht steht im Postfach",
      any("aufgegeben" in str(m.get("text")) for m in gs.messages), str(gs.messages[-1:]))

# ==========================================================================
abschnitt("3. Was die Aufgabe verhindert - und dabei NICHTS bucht")
# ==========================================================================

# 3a: die juengste Karte traegt die Taktik
_gs3 = M.GameState()
_main3 = _dorf("Haupt", _GUT, _reich(2.0), haupt=True)
_jung3 = _dorf("Zweites", _GUT, {"holz": 10.0})
bot3 = _bot([_main3, _jung3])
check("3 eine tragende Karte wird nicht aufgegeben",
      _gs3.bot_siedlung_aufgeben(bot3, 1000.0) is None)
check("3 das Dorf steht noch", len(bot3.doerfer) == 2, str(len(bot3.doerfer)))
check("3 der Vorrat ist unveraendert", abs(float(_main3.vorraete.get("holz", 0)) - _reich(2.0)["holz"]) < 1e-6,
      str(_main3.vorraete.get("holz")))

# 3b: niemand kann die naechste Gruendung bezahlen
_gs3b = M.GameState()
_arm = _dorf("Haupt", _GUT, {"holz": 100.0, "stein": 100.0, "nahrung": 100.0}, haupt=True)
_armjung = _dorf("Zweites", _SCHLECHT, {"holz": 0.0})
bot3b = _bot([_arm, _armjung])
check("3 ohne zahlendes Dorf KEINE Aufgabe (Daniel: er muss neu ansparen koennen)",
      _gs3b.bot_siedlung_aufgeben(bot3b, 1000.0) is None)
check("3 das Dorf bleibt stehen", len(bot3b.doerfer) == 2, str(len(bot3b.doerfer)))
check("3 die Gebuehr ist NICHT zurueckgelegt",
      abs(float(_arm.vorraete.get("holz", 0.0)) - 100.0) < 1e-6, str(_arm.vorraete))

# 3c: Sperre je Bot
_gs3c = M.GameState()
_m1 = _dorf("Haupt", _GUT, _reich(4.0), haupt=True)
_m2 = _dorf("Zweites", _SCHLECHT, {"holz": 10.0})
bot3c = _bot([_m1, _m2])
erste3c = _gs3c.bot_siedlung_aufgeben(bot3c, 1000.0)
check("3 die erste Aufgabe gelingt", isinstance(erste3c, dict), str(erste3c))
bot3c.doerfer.append(_dorf("Drittes", _SCHLECHT, {"holz": 5.0}))
bot3c.settlements.append("Drittes")
check("3 innerhalb der Sperre gibt der Bot NICHT wieder auf",
      _gs3c.bot_siedlung_aufgeben(bot3c, 1000.0 + 3600.0) is None)
check("3 nach Ablauf der Sperre geht die naechste Aufgabe",
      isinstance(_gs3c.bot_siedlung_aufgeben(bot3c, 1000.0 + SPERRE_H * 3600.0 + 1.0), dict),
      "Sperre %s h" % SPERRE_H)

# 3d: Abbruchregel
_gs3d = M.GameState()
_d1 = _dorf("Haupt", _GUT, _reich(4.0), haupt=True)
_d2 = _dorf("Zweites", _SCHLECHT, {"holz": 10.0})
bot3d = _bot([_d1, _d2])
bot3d.gedaechtnis["aufgabe_anzahl"] = int(AUFGABE.get("aufgaben_max") or 0)
check("3 nach der Hoechstzahl gibt der Bot nicht mehr auf",
      _gs3d.bot_siedlung_aufgeben(bot3d, 10 ** 7) is None)
check("3 das Dorf bleibt", len(bot3d.doerfer) == 2, str(len(bot3d.doerfer)))

# 3e: das Hauptdorf und das letzte Dorf
_gs3e = M.GameState()
_nur = _dorf("Haupt", _SCHLECHT, _reich(2.0), haupt=True)
bot3e = _bot([_nur])
check("3 das EINZIGE Dorf wird nie aufgegeben", _gs3e.bot_siedlung_aufgeben(bot3e, 1000.0) is None)
check("3 das Dorf steht", len(bot3e.doerfer) == 1, str(len(bot3e.doerfer)))
check("3 ohne Doerfer passiert nichts",
      _gs3e.bot_siedlung_aufgeben(_bot([]), 1000.0) is None)

# ==========================================================================
abschnitt("4. Die Gruendung kauft eine abgelehnte Karte nicht wieder")
# ==========================================================================

_gs4 = M.GameState()
_grund = _dorf("Haupt", _GUT, _reich(4.0), haupt=True)
_grund.einheiten = {"Siedlerkarren": 3}
bot4 = _bot([_grund])
bot4.gedaechtnis["abgelehnte_karten"] = {kennung: int(AUFGABE.get("erinnerung_max") or 1)
                                        for kennung in O.kennungen()}
neu4 = _gs4.bot_dorf_gruenden(bot4, 1000.0)
check("4 mit lauter abgelehnten Karten gruendet der Bot nicht", neu4 is None, str(neu4))
check("4 es bleibt bei einem Dorf", len(M.bot_doerfer_sicherstellen(bot4)) == 1,
      str(len(M.bot_doerfer_sicherstellen(bot4))))

_gs4b = M.GameState()
_grund4b = _dorf("Haupt", _GUT, _reich(4.0), haupt=True)
_grund4b.einheiten = {"Siedlerkarren": 3}
bot4b = _bot([_grund4b])
neu4b = _gs4b.bot_dorf_gruenden(bot4b, 1000.0)
check("4 ohne Erinnerung gruendet derselbe Bot", neu4b is not None,
      str(getattr(neu4b, "name", None)))
check("4 die Gruendung merkt sich das zahlende Dorf",
      str(bot4b.gedaechtnis.get("gruendung_quelle") or "") == "Haupt",
      str(bot4b.gedaechtnis.get("gruendung_quelle")))
check("4 die Gruendung merkt sich die Gebuehr",
      set(bot4b.gedaechtnis.get("gruendung_gebuehr") or {}) == set(PREIS),
      str(bot4b.gedaechtnis.get("gruendung_gebuehr")))

# ==========================================================================
abschnitt("5. Quellwachen: EINE Rechnung, EINE Quelle fuer Kern und Anzeige")
# ==========================================================================

check("5 die Aufgabe rechnet mit den Kosten des KERNS",
      "spieloekonomie.gruendungskosten()" in TEXT_MAIN)
check("5 die Aufgabe fragt das Urteil der Taktik",
      "bot_kartenurteil(bot, karte)" in TEXT_MAIN)
check("5 der Bot-Takt ruft die Aufgabe", "self.bot_siedlung_aufgeben(" in TEXT_MAIN)
check("5 der Takt legt das Ergebnis ab", 'ergebnis["aufgaben"]' in TEXT_MAIN)
check("5 die Sperre des Spielers und die Anzeige lesen DIESELBE Funktion",
      TEXT_MAIN.count("aufgeben_grund(") >= 3, str(TEXT_MAIN.count("aufgeben_grund(")))
check("5 die Startkarte ist fuer das Hauptdorf fest",
      "originalkarten.START_ID" in TEXT_MAIN and "Hauptdorf" in TEXT_MAIN)
check("5 die Datendatei nennt die Aufgabe als Regel",
      "GameState.bot_siedlung_aufgeben" in json.dumps(
          json.load(open(os.path.join(ROOT, "data", "bot_gruendung.json"), encoding="utf-8")),
          ensure_ascii=False))
befund("5 die Aufgabe ist ein VORSCHLAG mit Zahlen aus der Datei (24 h Sperre, dreimal je Bot)",
       "Daniel kann sie ohne Codeaenderung stellen")

sys.exit(bericht())
