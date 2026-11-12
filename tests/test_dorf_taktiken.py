# -*- coding: ascii -*-
"""Dorf-Verhalten: Wahl aus der Lage, Sperrzeit, Anzeigegrenze - Stufe B-2 (02.11.2026).

VORGABE Daniel (Konzept K-1, Abschnitt 8.5): Verhalten IST die Taktik eines Dorfes, Doerfer duerfen
wechseln (mit Sperrzeit), und beim Bot bedeutet das Verhalten auch, wie das Dorf sich verhaelt -
beim Spieler aendert es nur die Werte. Die Wahl darf NICHT durch Nachdenken entstehen, sondern als
festes Paket aus der Lage.

Was diese Datei beweist
-----------------------
1. Position: derselbe Name mit derselben Nummer ergibt immer dieselbe Position, sie liegt im
   Kartenbereich, und verschiedene Doerfer liegen (in der Regel) nicht auf demselben Feld.
2. Bewertung: die vier Lagen verschieben die Punktwerte so, wie Daniel es beschreibt -
   stark und nah macht RAUBERN wahrscheinlich, schwach und weit macht SAMMELN/WACHSEN
   wahrscheinlich, gebrochener Wall und Niederlage heben SICHERN bzw. RAECHEN.
3. Wahl: Sperrzeit wird eingehalten; danach gewinnt der hoechste Punktwert; Gleichstand wird mit
   dem uebergebenen Zufall reproduzierbar aufgeloest; das Ergebnis ist immer ein bekanntes Verhalten.
4. Setzen: ein Wechsel schreibt Verhalten UND Zeitpunkt; ohne Wechsel bleibt der Zeitpunkt stehen
   (sonst waere die Sperrzeit nie erreichbar).
5. Die Bruecke in main zieht die Lage aus vorhandenen Werten (kein erfundenes Feld) und waehlt.
6. ANZEIGEGRENZE (Daniel 02.11.2026): die offene Uebersicht nennt Name, Position, Wall und
   Hauptdorf-Kennzeichen - die AKTIVE TAKTIK steht ausdruecklich NICHT darin; sie gehoert in einen
   Spionagebericht.

Aufruf:  python -X utf8 tests/test_dorf_taktiken.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['bottaktik', 'main:*', 'welt']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

ROOT, SRC = import_src()
import main       # noqa: E402
import bottaktik  # noqa: E402

# ==========================================================================
abschnitt("1. Position je Dorf ist fest und im Kartenbereich")
# ==========================================================================
a1 = bottaktik.dorf_position("Haug", 0)
a2 = bottaktik.dorf_position("Haug", 0)
check("1 gleicher Name und gleiche Nummer ergeben dieselbe Position", a1 == a2, f"{a1} / {a2}")
check("1 die Position liegt im 20x20-Raster",
      all(0 <= v < 20 for v in a1) and len(a1) == 2, str(a1))
b1 = bottaktik.dorf_position("Haug", 1)
check("1 die zweite Siedlung liegt woanders", b1 != a1, f"{a1} / {b1}")
check("1 ein anderes Volk liegt woanders", bottaktik.dorf_position("Grom", 0) != a1, "")
check("1 das Raster ist einstellbar (z. B. eine groessere Karte)",
      all(0 <= v < 100 for v in bottaktik.dorf_position("Haug", 0, raster=100)),
      str(bottaktik.dorf_position("Haug", 0, raster=100)))

# ==========================================================================
abschnitt("2. Die Lage verschiebt die Punktwerte wie beschrieben")
# ==========================================================================
stark_nah = bottaktik.dorf_taktik_bewerten({"naehe": 1.0, "staerke": 1.0, "wall": 1.0, "niederlage": 0.0})
check("2 stark und nah: RAUBERN ist die staerkste Neigung",
      max(stark_nah, key=stark_nah.get) == "RAUBERN",
      str(sorted(stark_nah.items(), key=lambda x: -x[1])[:3]))
schwach_fern = bottaktik.dorf_taktik_bewerten({"naehe": -1.0, "staerke": -1.0, "wall": 1.0, "niederlage": 0.0})
check("2 schwach und weit: SAMMELN oder WACHSEN fuehrt",
      max(schwach_fern, key=schwach_fern.get) in ("SAMMELN", "WACHSEN"),
      str(sorted(schwach_fern.items(), key=lambda x: -x[1])[:3]))
wall_kaputt = bottaktik.dorf_taktik_bewerten({"naehe": 1.0, "staerke": -1.0, "wall": -1.0, "niederlage": 0.0})
check("2 gebrochener Wall bei Naehe: SICHERN oder FLIEHEN fuehrt",
      max(wall_kaputt, key=wall_kaputt.get) in ("SICHERN", "FLIEHEN"),
      str(sorted(wall_kaputt.items(), key=lambda x: -x[1])[:3]))
niederlage = bottaktik.dorf_taktik_bewerten({"naehe": 0.5, "staerke": 0.4, "wall": -0.2, "niederlage": 1.0})
check("2 gerade verloren: RAECHEN ist die staerkste Neigung",
      max(niederlage, key=niederlage.get) == "RAECHEN",
      str(sorted(niederlage.items(), key=lambda x: -x[1])[:3]))
leer = bottaktik.dorf_taktik_bewerten({})
check("2 ohne Lage gewinnt die Grundneigung (SAMMELN oder WACHSEN)",
      max(leer, key=leer.get) in ("SAMMELN", "WACHSEN"),
      str(sorted(leer.items(), key=lambda x: -x[1])[:3]))
check("2 jede Bewertung nennt ALLE acht Verhalten", set(leer) == set(bottaktik.ZUSTAENDE),
      str(sorted(leer)))

# ==========================================================================
abschnitt("3. Wahl mit Sperrzeit, deterministisch")
# ==========================================================================
SPERRE = bottaktik.DORF_WECHSEL_SPERRE
check("3 die Sperrzeit ist eine positive Zahl (Vorschlag: 48 h)",
      isinstance(SPERRE, (int, float)) and SPERRE > 0, f"{SPERRE / 3600:g} h")
gewaehlt = bottaktik.dorf_taktik_waehlen({"staerke": 1.0, "naehe": 1.0}, "", 0.0, 0.0)
check("3 ohne bisheriges Verhalten wird gewaehlt", gewaehlt in bottaktik.ZUSTAENDE, gewaehlt)
in_sperre = bottaktik.dorf_taktik_waehlen({"staerke": -1.0, "naehe": -1.0}, "SICHERN", 1000.0,
                                          1000.0 + SPERRE - 60.0)
check("3 innerhalb der Sperrzeit bleibt das Verhalten", in_sperre == "SICHERN", in_sperre)
nach_sperre = bottaktik.dorf_taktik_waehlen({"staerke": -1.0, "naehe": -1.0}, "SICHERN", 1000.0,
                                            1000.0 + SPERRE + 60.0)
check("3 nach der Sperrzeit darf gewechselt werden", nach_sperre != "SICHERN", nach_sperre)
check("3 das Ergebnis ist immer ein bekanntes Verhalten", nach_sperre in bottaktik.ZUSTAENDE, nach_sperre)
gleich = bottaktik.dorf_taktik_bewerten({"naehe": 0.0, "staerke": 0.0, "wall": 0.0, "niederlage": 0.0})
eins = bottaktik.dorf_taktik_waehlen({}, "", 0.0, 0.0, random.Random("probe"))
zwei = bottaktik.dorf_taktik_waehlen({}, "", 0.0, 0.0, random.Random("probe"))
check("3 gleicher Zufall ergibt dieselbe Wahl (reproduzierbar)", eins == zwei, f"{eins} / {zwei}")
ohne = bottaktik.dorf_taktik_waehlen({}, "", 0.0, 0.0, None)
check("3 ohne Zufall entscheidet die feste Reihenfolge", ohne == "SAMMELN", ohne)

# ==========================================================================
abschnitt("4. Setzen schreibt Verhalten und Zeitpunkt")
# ==========================================================================
dorf = {"taktik": "", "taktik_seit": 0.0}
gewechselt = bottaktik.dorf_taktik_setzen(dorf, 5000.0, {"staerke": 1.0, "naehe": 1.0})
check("4 der erste Aufruf setzt ein Verhalten", gewechselt is True and dorf["taktik"] in bottaktik.ZUSTAENDE,
      str(dorf))
check("4 der Zeitpunkt wird geschrieben", abs(dorf["taktik_seit"] - 5000.0) < 1e-9, str(dorf["taktik_seit"]))
vorher = dict(dorf)
unveraendert = bottaktik.dorf_taktik_setzen(dorf, 5200.0, {"staerke": 1.0, "naehe": 1.0})
check("4 ohne Wechsel kommt False zurueck", unveraendert is False, "")
check("4 ohne Wechsel bleibt der Zeitpunkt stehen (sonst waere die Sperre nie erreichbar)",
      dorf["taktik_seit"] == vorher["taktik_seit"], f"{dorf['taktik_seit']} / {vorher['taktik_seit']}")
check("4 ein Nicht-Dict ergibt kein Ergebnis", bottaktik.dorf_taktik_setzen(None, 1.0) is False, "")

# ==========================================================================
abschnitt("5. Die Bruecke in main waehlt aus vorhandenen Werten")
# ==========================================================================


class _Ort:
    """Minimaler Ort fuer die Naehe (nur x/y)."""
    def __init__(self, x, y):
        self.x, self.y, self.name = x, y, "Testdorf"


class _App:
    """Duck-Typ statt echter Spielstand: die Methoden brauchen nur settlements."""
    settlements = []

    def bot_dorf_platz(self, welt, x, y):
        """Stub ohne Drachen: die Sperre selbst prueft test_drachen_einhaengung (05.11.2026)."""
        return (int(x), int(y))


bot = main.BotPlayer("Grom", "zwergisch", aggression=0.7, trading=0.4)
bot.settlements = ["Groms Siedlung 1", "Groms Siedlung 2"]
bot.army = {"Kaempfer": 40}
app = _App()
geaendert = main.GameState.bot_doerfer_auffrischen(app, bot, 1000.0, _Ort(0, 0))
check("5 beide Doerfer bekommen ein Verhalten", geaendert == 2, str(geaendert))
check("5 die Positionen sind gesetzt (nicht mehr 0/0 bei beiden)",
      any(int(d.x) or int(d.y) for d in bot.doerfer), str([(d.x, d.y) for d in bot.doerfer]))
check("5 jedes Dorf fuehrt ein bekanntes Verhalten",
      all(d.taktik in bottaktik.ZUSTAENDE for d in bot.doerfer), str([d.taktik for d in bot.doerfer]))
nochmal = main.GameState.bot_doerfer_auffrischen(app, bot, 1200.0, _Ort(0, 0))
check("5 innerhalb der Sperrzeit aendert sich nichts mehr", nochmal == 0, str(nochmal))
spaeter = main.GameState.bot_doerfer_auffrischen(app, bot, 1000.0 + SPERRE + 60.0, _Ort(0, 0))
check("5 nach der Sperrzeit darf sich etwas aendern (0 oder mehr ist beides erlaubt)",
      isinstance(spaeter, int) and spaeter >= 0, str(spaeter))

# ==========================================================================
abschnitt("6. Anzeigegrenze: die offene Uebersicht verraet die Taktik NICHT")
# ==========================================================================
zeilen = main.GameState.bot_doerfer_uebersicht(app, bot)
check("6 die Uebersicht nennt jedes Dorf", len(zeilen) == len(bot.doerfer), str(len(zeilen)))
check("6 sie nennt Name, Position, Hauptdorf, Fraktion und die bekannten Volkswerte",
      all(set(z) == {"name", "x", "y", "hauptdorf", "fraktion", "volk_plus", "volk_minus"}
          for z in zeilen), str(sorted(zeilen[0])))
check("6 die aktive Taktik steht NICHT in der offenen Uebersicht (nur im Spionagebericht)",
      all("taktik" not in z for z in zeilen), str(sorted(zeilen[0])))
check("6 die WALLSTUFE ist ein Kampfdatum und steht NICHT in der offenen Uebersicht",
      all("wall_stufe" not in z and "wall_zustand" not in z for z in zeilen), str(sorted(zeilen[0])))
bericht_daten = main.GameState.bot_doerfer_spionagebericht(app, bot)
check("6 der Spionagebericht nennt Wall, Taktik, Truppen und Vorraete",
      bericht_daten["doerfer"] and all(
          {"wall_stufe", "wall_zustand", "taktik", "truppen", "vorraete"} <= set(d)
          for d in bericht_daten["doerfer"]), str(sorted(bericht_daten["doerfer"][0])))

sys.exit(bericht())
