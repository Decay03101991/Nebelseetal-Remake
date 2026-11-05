# -*- coding: ascii -*-
"""Wache Story 2: die fuenf Bots sprechen (04.11.2026).

WARUM
-----
Die externe Projektpruefung hat gemessen, dass die fuenf Nachbarn stumme Namen sind: sie greifen an,
gruenden Doerfer und rauben, aber kein Satz gehoert zu ihnen. Daniel hat am 04.11.2026 entschieden:
je Bot ein bis zwei Saetze fuer **Angriff, Verteidigung, Gruendung und Beute**, Ton wie Story 1
(abenteuerlich und leicht, kein Pathos).

Was diese Datei beweist
-----------------------
1. Die Texte stehen in `data/bot_stimmen.json`, NICHT im Code.
2. Jeder der fuenf Bots (`botkern.BOT_NAMEN`) hat zu JEDEM der vier Ereignisse ein bis zwei Saetze
   mit echtem Deutsch (Umlaute, kein ASCII-Ersatz).
3. `stimmen.zeile` liefert einen hinterlegten Satz und erreicht beide Saetze (mit festem Zufall).
4. Ein unbekannter Bot, ein unbekanntes Ereignis und eine fehlende Datendatei liefern den neutralen
   Satz bzw. einen leeren Text - NIE einen Absturz, und der sachliche Meldungstext geht nie verloren.
5. Quellwache: `main.py` fragt alle vier Anlaesse ab, und im Code steht kein einziger dieser Texte.
6. App-Lauf: eine echte Meldung des Raubzugs traegt die Stimme des Bots UND den sachlichen Bericht.

Aufruf:  python -X utf8 tests/test_stimmen.py
"""
from __future__ import annotations

import json
import os
import random
import sys
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
import botkern   # noqa: E402
import main as M  # noqa: E402
import stimmen   # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
ROHDATEN = open(os.path.join(ROOT, "data", "bot_stimmen.json"), encoding="utf-8").read()
DATEN = json.loads(ROHDATEN)
BOTS = list(botkern.BOT_NAMEN)                       # die fuenf Namen aus dem Kern, keine Handliste
ERWARTET = ["angriff", "verteidigung", "gruendung", "beute"]

# ==========================================================================
abschnitt("1. Die Texte stehen in der Datendatei, nicht im Code")
# ==========================================================================
check("1 data/bot_stimmen.json ist lesbar und ein Verzeichnis", isinstance(DATEN, dict) and bool(DATEN), "")
check("1 die Datei nennt den Ton (Daniels Entscheidung)", "abenteuerlich" in str(DATEN.get("ton")), "")
check("1 die Datei fuehrt genau die vier Ereignisse aus Story 2",
      list(DATEN.get("ereignisse") or []) == ERWARTET, str(DATEN.get("ereignisse")))
check("1 stimmen.ereignisse() liefert dieselbe Liste", stimmen.ereignisse() == ERWARTET,
      str(stimmen.ereignisse()))
check("1 es gibt einen neutralen Satz fuer fehlende Eintraege", len(str(DATEN.get("neutral") or "")) > 20,
      str(DATEN.get("neutral")))
check("1 die Datei fuehrt GENAU die fuenf Bots des Kerns",
      sorted((DATEN.get("bots") or {}).keys()) == sorted(BOTS), str(sorted((DATEN.get("bots") or {}).keys())))
check("1 stimmen.bots() nennt dieselben Namen", stimmen.bots() == sorted(BOTS), str(stimmen.bots()))

umlaute = [chr(228), chr(246), chr(252), chr(223)]           # ae, oe, ue, ss
check("1 die Texte tragen echte Umlaute (Anzeigetext, kein ASCII-Ersatz)",
      all(z in ROHDATEN for z in umlaute), "mindestens einer der vier Umlaute fehlt")
check("1 kein ASCII-Ersatz im Text",
      "Doerfer" not in ROHDATEN and "Gruendung" not in ROHDATEN and "Fuenf" not in ROHDATEN, "")

# ==========================================================================
abschnitt("2. Jeder Bot hat zu JEDEM Ereignis ein bis zwei echte Saetze")
# ==========================================================================
for bot in BOTS:
    for ereignis in ERWARTET:
        saetze = stimmen.texte(bot, ereignis)
        check("2 %s/%s hat ein bis zwei Saetze" % (bot, ereignis), 1 <= len(saetze) <= 2, str(len(saetze)))
        check("2 %s/%s ist ein ausformulierter Satz" % (bot, ereignis),
              all(len(s) > 25 for s in saetze), str([len(s) for s in saetze]))
        check("2 %s/%s kommt in der Datendatei so vor" % (bot, ereignis),
              all(s in ROHDATEN for s in saetze), "")

alle = [s for bot in BOTS for e in ERWARTET for s in stimmen.texte(bot, e)]
check("2 die fuenf Bots klingen verschieden (kein Satz doppelt)",
      len(alle) == len(set(alle)), "%d Saetze, %d verschiedene" % (len(alle), len(set(alle))))
check("2 die vier Ereignisse sind inhaltlich getrennt (kein Bot-Text doppelt ueber Ereignisse)",
      all(len(set(tuple(stimmen.texte(b, e)) for e in ERWARTET)) == 4 for b in BOTS), "")

# ==========================================================================
abschnitt("3. zeile() liefert einen hinterlegten Satz - und erreicht beide")
# ==========================================================================
for bot in BOTS:
    for ereignis in ERWARTET:
        gezogen = stimmen.zeile(bot, ereignis)
        check("3 %s/%s liefert einen Satz aus der Datei" % (bot, ereignis),
              gezogen in stimmen.texte(bot, ereignis), gezogen[:50])

rng = random.Random(7)                               # fester Zufall: der Lauf ist wiederholbar
gesehen = {b: {e: set() for e in ERWARTET} for b in BOTS}
for _ in range(200):                                 # 200 Ziehungen je Fach
    for bot in BOTS:
        for ereignis in ERWARTET:
            gesehen[bot][ereignis].add(stimmen.zeile(bot, ereignis, rng))
check("3 jede Ziehung ist reproduzierbar (gleicher Zufall, gleicher Satz)",
      stimmen.zeile("Haug", "angriff", random.Random(3)) == stimmen.zeile("Haug", "angriff", random.Random(3)), "")
check("3 beide Saetze werden wirklich erreicht (kein toter Text)",
      all(len(gesehen[b][e]) == len(stimmen.texte(b, e)) for b in BOTS for e in ERWARTET),
      str({b: {e: len(gesehen[b][e]) for e in ERWARTET} for b in BOTS}))

# ==========================================================================
abschnitt("4. Unbekanntes und Fehlendes: neutraler Satz, nie ein Absturz")
# ==========================================================================
neutral = stimmen.neutral()
check("4 ein unbekannter Bot liefert den neutralen Satz", stimmen.zeile("Niemand", "angriff") == neutral,
      stimmen.zeile("Niemand", "angriff"))
check("4 ein unbekanntes Ereignis liefert den neutralen Satz",
      stimmen.zeile("Haug", "hochzeit") == neutral, stimmen.zeile("Haug", "hochzeit"))
check("4 ein Bot ohne Eintrag fuer EIN Ereignis faellt auf neutral zurueck",
      stimmen.zeile("Haug", "") == neutral, stimmen.zeile("Haug", ""))
check("4 auch ein leerer Name stuerzt nicht ab", isinstance(stimmen.zeile("", ""), str), "")
check("4 texte() liefert fuer Unbekanntes eine leere Liste, nie None",
      stimmen.texte("Niemand", "angriff") == [] and stimmen.texte(None, None) == [], "")
check("4 mit_stimme haengt die Stimme vor den Bericht",
      stimmen.mit_stimme("Grom", "gruendung", "Grom hat ein Dorf gegruendet.").endswith(
          "\nGrom hat ein Dorf gegruendet."), "")

# Fehlende Datendatei: genau der Fall "Datei weg oder kaputt" - der Bericht muss stehen bleiben.
echte_datei = stimmen._datei
stimmen._datei = lambda: {}
try:
    check("4 ohne Datendatei gibt es keinen Satz, aber keinen Absturz", stimmen.zeile("Haug", "angriff") == "", "")
    check("4 ohne Datendatei bleibt der sachliche Bericht unveraendert",
          stimmen.mit_stimme("Haug", "angriff", "Haug gegen X: angreifer; Beute 5.")
          == "Haug gegen X: angreifer; Beute 5.", "")
    check("4 ohne Datendatei sind bots() und neutral() leer",
          stimmen.bots() == [] and stimmen.neutral() == "", "")
finally:
    stimmen._datei = echte_datei                    # echte Lesestelle zurueck

# ==========================================================================
abschnitt("5. Quellwache: der Anschluss steht im Code, die Texte nicht")
# ==========================================================================
check("5 main.py fragt den Angriff ab", 'stimmen.mit_stimme(bot.name, "angriff"' in TEXT_MAIN, "")
check("5 main.py fragt die Beute ab", 'stimmen.mit_stimme(bot.name, "beute"' in TEXT_MAIN, "")
check("5 main.py fragt die Gruendung ab", 'stimmen.mit_stimme(bot.name, "gruendung"' in TEXT_MAIN, "")
check("5 main.py fragt die Verteidigung ab (das Ziel ist ein Bot)",
      'stimmen.zeile(bot_ziel.name, "verteidigung")' in TEXT_MAIN, "")
check("5 main.py importiert das Modul", "import stimmen" in TEXT_MAIN, "")
# Register 228 (05.11.2026): die Bot-Aufgabe meldet sich mit der GRUENDUNGS-Stimme
# (`bot_siedlung_aufgeben`) - sie ist ein Siedlungs-Ereignis wie die Gruendung. Damit stehen VIER
# Abfragen mit Stimme und EINE Verteidigungsabfrage im Code, jede an genau einer Stelle.
check("5 die fuenf Abfragen stehen an je einer Stelle (Aufgabe teilt die Gruendungs-Stimme)",
      TEXT_MAIN.count("stimmen.mit_stimme(") == 4 and TEXT_MAIN.count("stimmen.zeile(") == 1,
      "%d / %d" % (TEXT_MAIN.count("stimmen.mit_stimme("), TEXT_MAIN.count("stimmen.zeile(")))
im_code = [s for s in alle if s[:30] in TEXT_MAIN]
check("5 kein einziger Bot-Text steht im Code (kein zweites Gedaechtnis)", im_code == [],
      str(im_code[:2]))
check("5 auch der neutrale Satz steht nicht im Code", neutral[:30] not in TEXT_MAIN, neutral[:30])

# ==========================================================================
abschnitt("6. App-Lauf: die Meldung traegt Stimme UND Bericht")
# ==========================================================================
def _dorf(name, welt=4, einheiten_=None, vorraete=None, haupt=False):
    """Ein Bot-Dorf fuer die Pruefung - nur die Felder, die der Raubzug liest."""
    return M.BotDorf(name=name, x=0, y=0, herkunftswelt=welt, dimension=welt,
                     hauptdorf=haupt, wall_stufe=0, wall_zustand=100.0,
                     einheiten=dict(einheiten_ or {}), vorraete=dict(vorraete or {}))


root = tk.Tk()
root.withdraw()
try:
    app = M.NebelseetalApp(root)
    app._build_main_ui()
    st = app.state
    haug = M.BotPlayer("Haug", "menschlich", 1.0, 0.0, doerfer=[_dorf("Haugs Siedlung 1", haupt=True)])
    ziel = _dorf("Brynhilds Siedlung 1", einheiten_={}, vorraete={"holz": 400, "stein": 400})
    brynhild = M.BotPlayer("Brynhild", "menschlich", 0.5, 0.0, doerfer=[ziel])
    meldung, beute = st._bots_raubzug(haug, brynhild, ziel, {"Krieger": 20},
                                      {"Handkarren": 5}, random.Random(11))
    erwartete_stimme = [s for s in stimmen.texte("Haug", "beute") if meldung.startswith(s + chr(10))]
    check("6 die Meldung beginnt mit der Stimme des Angreifers", bool(erwartete_stimme),
          meldung[:70])
    check("6 der sachliche Bericht steht weiterhin in der Meldung",
          "gegen Brynhild" in meldung and "tats\u00e4chliche Beute" in meldung, meldung[:120])
    check("6 der Bericht ist die ZWEITE Zeile (Stimme, dann Zahlen)",
          "tats\u00e4chliche Beute" in meldung.split(chr(10))[-1], repr(meldung[-60:]))
    check("6 die Meldung steht so im Postfach",
          any(m.get("type") == "kampf" and m.get("text") == meldung for m in st.messages), "")
    ohne = M.BotPlayer("OhneStimme", "menschlich", 1.0, 0.0,
                       doerfer=[_dorf("OhneStimmes Siedlung 1", haupt=True)])
    ziel2 = _dorf("Brynhilds Siedlung 2", einheiten_={}, vorraete={"holz": 400})
    brynhild.doerfer.append(ziel2)
    meldung2, _beute2 = st._bots_raubzug(ohne, brynhild, ziel2, {"Krieger": 20},
                                         {"Handkarren": 5}, random.Random(11))
    check("6 ein Bot ohne Stimme bekommt den neutralen Satz vor dem Bericht",
          meldung2.startswith(stimmen.neutral() + chr(10)) and "gegen Brynhild" in meldung2,
          meldung2[:90])
except Exception as fehler:                                     # noqa: BLE001 - Meldung statt Absturz
    # Ein Absturz hier ist ein FEHLER und kein Befund: der App-Lauf ist der Gegenstand des Abschnitts.
    check("6 der App-Lauf laeuft ohne Ausnahme durch", False, repr(fehler))
finally:
    root.destroy()

sys.exit(bericht())
