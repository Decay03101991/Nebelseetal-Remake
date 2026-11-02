# -*- coding: ascii -*-
"""Bot-Doerfer, Stufe B-1 (Konzept K-1 Abschnitt 5) - 02.11.2026.

BEFUND: Bis heute fuehrt ein Bot nur NAMEN seiner Doerfer (`BotPlayer.settlements`, vom Kartenaufbau
mit 1 bis 3 Eintraegen gefuellt - main.py, Abschnitt generate_map) und EINEN gemeinsamen Vorrat. Im
Code steht ausdruecklich, dass die eigene Ortsstruktur je Bot-Siedlung eine spaetere Stufe ist.
Fuer Dorf-Taktiken (jedes Dorf waehlt und wechselt seine Taktik) braucht es je Dorf einen eigenen
Datensatz. B-1 legt diesen Traeger an - ohne die Wirtschaft umzubauen.

Was diese Datei beweist
-----------------------
1. `BotDorf` und das Feld `BotPlayer.doerfer` existieren (Vorgabe: leer).
2. Ein Bot ohne Doerfer bekommt genau EIN Hauptdorf mit dem bisherigen Standardnamen.
3. Ein Bot mit drei Siedlungsnamen bekommt drei Doerfer, und genau das ERSTE ist das Hauptdorf.
4. Wall, Wallzustand und die Zaehler werden uebernommen (alter Stand verliert nichts).
5. Der Aufruf ist idempotent: zweimal sicherstellen ergibt dieselbe Zahl.
6. Speichern und Laden: `asdict` -> `bot_aus_stand` macht aus den dicts wieder Objekte, Werte gleich.
7. Ein Spielstand von VOR B-1 (ohne Feld `doerfer`) laedt ohne Fehler und bekommt danach sein
   Hauptdorf.
8. Vorraete und Siedlungsnamen bleiben unangetastet.
9. BEFUND (Zwischenstand, bewusst): die Dorf-Vorraete sind in B-1 NICHT fuehrend - der Bot-Vorrat
   bleibt die eine Wahrheit, bis B-3 die Wirtschaft je Dorf bucht. Diese Datei haelt den
   Zwischenstand fest, statt ihn zu verschweigen.

Aufruf:  python -X utf8 tests/test_bot_doerfer.py
"""
from __future__ import annotations

import os
import sys
from dataclasses import asdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import main  # noqa: E402

# ==========================================================================
abschnitt("1. Die Traeger existieren")
# ==========================================================================
check("1 main.BotDorf ist eine Klasse", isinstance(getattr(main, "BotDorf", None), type), "")
feld = getattr(main.BotPlayer, "__dataclass_fields__", {}).get("doerfer")
check("1 BotPlayer fuehrt das Feld doerfer (Vorgabe: leere Liste)", feld is not None,
      str(sorted(getattr(main.BotPlayer, "__dataclass_fields__", {}))[:3]) + " ...")

frisch = main.BotPlayer("Haug", "menschlich", aggression=0.3, trading=0.8)
check("1 ein frischer Bot hat noch kein Dorf", frisch.doerfer == [], str(frisch.doerfer))
check("1 BotDorf traegt den Taktik-Slot (leer = noch nicht gewaehlt)",
      main.BotDorf(name="x").taktik == "" and main.BotDorf(name="x").hauptdorf is False, "")

# ==========================================================================
abschnitt("2. Ein Bot ohne Namen bekommt EIN Hauptdorf")
# ==========================================================================
ohne = main.BotPlayer("Silra", "elfisch", aggression=0.2, trading=0.9)
doerfer = main.bot_doerfer_sicherstellen(ohne)
check("2 genau ein Dorf angelegt", len(doerfer) == 1, str([d.name for d in doerfer]))
check("2 das Dorf ist das Hauptdorf", doerfer[0].hauptdorf is True, str(doerfer[0].hauptdorf))
check("2 der Name ist der bisherige Standardname", doerfer[0].name == "Silras Siedlung 1", doerfer[0].name)
check("2 die Liste haengt am Bot", ohne.doerfer is doerfer or ohne.doerfer == doerfer, "")

# ==========================================================================
abschnitt("3. Drei Siedlungsnamen ergeben drei Doerfer, das erste ist das Hauptdorf")
# ==========================================================================
drei = main.BotPlayer("Brynhild", "menschlich", aggression=0.5, trading=0.6)
drei.settlements = ["Brynhilds Siedlung 1", "Brynhilds Siedlung 2", "Brynhilds Siedlung 3"]
liste = main.bot_doerfer_sicherstellen(drei)
check("3 drei Doerfer", len(liste) == 3, str(len(liste)))
check("3 genau EIN Hauptdorf und zwar das erste",
      [d.hauptdorf for d in liste] == [True, False, False], str([d.hauptdorf for d in liste]))
check("3 die Namen kommen aus dem Bot (nichts erfunden)",
      [d.name for d in liste] == list(drei.settlements), str([d.name for d in liste]))

# ==========================================================================
abschnitt("4. Wall und Zaehler werden uebernommen")
# ==========================================================================
wall = main.BotPlayer("Grom", "zwergisch", aggression=0.7, trading=0.4)
wall.wall_stufe, wall.wall_zustand, wall.gebaut, wall.geforscht = 3, 80.0, 5, 2
erste = main.bot_doerfer_sicherstellen(wall)[0]
check("4 Wallstufe uebernommen", erste.wall_stufe == 3, str(erste.wall_stufe))
check("4 Wallzustand uebernommen", abs(erste.wall_zustand - 80.0) < 1e-9, str(erste.wall_zustand))
check("4 Zaehler uebernommen", (erste.gebaut, erste.geforscht) == (5, 2),
      f"{erste.gebaut}/{erste.geforscht}")

# ==========================================================================
abschnitt("5. Der Aufruf ist idempotent")
# ==========================================================================
nochmal = main.bot_doerfer_sicherstellen(wall)
check("5 zweimal sicherstellen ergibt dieselbe Zahl", len(nochmal) == 1, str(len(nochmal)))
check("5 es bleibt dasselbe Dorf (kein zweites Hauptdorf)", nochmal[0].name == erste.name, nochmal[0].name)
check("5 hoechstens ein Hauptdorf je Bot",
      sum(1 for d in main.bot_doerfer_sicherstellen(drei) if d.hauptdorf) == 1, "")

# ==========================================================================
abschnitt("6. Speichern und Laden behaelt die Doerfer")
# ==========================================================================
stand = asdict(wall)                                    # so schreibt `save` die Bots
check("6 der gespeicherte Stand fuehrt doerfer als dict", isinstance(stand["doerfer"][0], dict), "")
geladen = main.bot_aus_stand(stand)
check("6 nach dem Laden sind es wieder BotDorf-Objekte",
      all(isinstance(d, main.BotDorf) for d in geladen.doerfer), str(type(geladen.doerfer[0]).__name__))
check("6 die Werte sind unveraendert",
      geladen.doerfer[0].name == erste.name and geladen.doerfer[0].wall_stufe == 3, "")

# ==========================================================================
abschnitt("7. Ein Spielstand von VOR B-1 laedt ohne Fehler")
# ==========================================================================
alt = {"name": "Krank", "faction": "monster", "aggression": 0.9, "trading": 0.0,
       "settlements": ["Kranks Siedlung 1", "Kranks Siedlung 2"]}      # kein Feld doerfer
try:
    krank = main.bot_aus_stand(alt)
    fehler = ""
except Exception as e:                                  # noqa: BLE001 - Fehler ist der Befund
    krank, fehler = None, repr(e)
check("7 ein alter Bot-Stand laedt ohne Ausnahme", krank is not None, fehler)
if krank is not None:
    check("7 er hat danach noch kein Dorf (das macht der Aufruf danach)", krank.doerfer == [], "")
    nachher = main.bot_doerfer_sicherstellen(krank)
    check("7 nach dem Sicherstellen hat er seine zwei Doerfer", len(nachher) == 2, str(len(nachher)))
    check("7 das erste ist das Hauptdorf", nachher[0].hauptdorf is True, "")

# ==========================================================================
abschnitt("8. Vorraete und Siedlungsnamen bleiben unangetastet")
# ==========================================================================
voll = main.BotPlayer("Haug", "menschlich", aggression=0.3, trading=0.8)
voll.vorraete = {"holz": 120, "stein": 80}
voll.settlements = ["Haugs Siedlung 1"]
vorher_vorraete, vorher_namen = dict(voll.vorraete), list(voll.settlements)
main.bot_doerfer_sicherstellen(voll)
check("8 die Bot-Vorraete sind unveraendert", voll.vorraete == vorher_vorraete, str(voll.vorraete))
check("8 die Siedlungsnamen sind unveraendert", voll.settlements == vorher_namen, str(voll.settlements))

# ==========================================================================
abschnitt("9. Zwischenstand, bewusst festgehalten")
# ==========================================================================
befund("9 die Dorf-Vorraete sind in B-1 noch NICHT fuehrend",
       "der Bot-Vorrat bleibt die eine Wahrheit, bis B-3 die Wirtschaft je Dorf bucht")
check("9 das Dorf traegt dennoch ein eigenes Vorratsfeld",
      isinstance(main.BotDorf(name="x").vorraete, dict), "")

sys.exit(bericht())
