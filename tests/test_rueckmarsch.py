"""Prueft den Rueckweg einer Truppe auf der Weltkarte (E3, 31.10.2026).

Daniels Beobachtung: Truppen waren nach der Ankunft sofort wieder verfuegbar, obwohl der
Auftrags-Pfad fuer den Rueckweg dieselbe Zeit noch einmal veranschlagt. Hier wird die reine
Rechnung geprueft (main.rueckmarsch_eintrag) - ohne Fenster, ohne Spielstand.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

import main  # noqa: E402

FEHLER = []
PRUEFUNGEN = 0


def check(name, bedingung, wert=""):
    global PRUEFUNGEN
    PRUEFUNGEN += 1
    if not bedingung:
        FEHLER.append(f"{name} {wert}".strip())


# ---------------------------------------------------------------- 1. Hinweg 3600 s
hin = {"from": "10:10", "to": "14:10", "units": {"handkarren": 2},
       "start": 1000.0, "arrival": 4600.0, "map": "original-036",
       "target_bot": "Testbot", "tile_key": "14:10", "rueckweg": False}
rueck = main.rueckmarsch_eintrag(hin, 4600.0)
check("1 Rueckmarsch entsteht", rueck is not None, rueck)
check("2 Start und Ziel getauscht", rueck and rueck["from"] == "14:10" and rueck["to"] == "10:10", rueck)
check("3 gleiche Dauer wie der Hinweg", rueck and abs((rueck["arrival"] - rueck["start"]) - 3600.0) < 0.01, rueck)
check("4 Ankunft = jetzt + Dauer", rueck and abs(rueck["arrival"] - 8200.0) < 0.01, rueck)
check("5 Truppen bleiben dieselben", rueck and rueck["units"] == {"handkarren": 2}, rueck)
check("6 als Rueckweg markiert", rueck and rueck["rueckweg"] is True, rueck)
check("7 kein Bot am Rueckweg", rueck and rueck["target_bot"] is None, rueck)
check("8 Karte wird mitgenommen", rueck and rueck["map"] == "original-036", rueck)

# ---------------------------------------------------------------- 2. Truppen sind eine Kopie
rueck["units"]["handkarren"] = 99
check("9 Truppenliste ist eine Kopie", hin["units"]["handkarren"] == 2, hin["units"])

# ---------------------------------------------------------------- 3. Kein Kreislauf
check("10 Rueckweg erzeugt keinen zweiten", main.rueckmarsch_eintrag(rueck, 8200.0) is None)

# ---------------------------------------------------------------- 4. Ohne Dauer sofort zurueck
sofort = {"from": "1:1", "to": "2:1", "units": {"spaeher": 1},
          "start": 500.0, "arrival": 500.0, "rueckweg": False}
check("11 Dauer 0 -> kein Rueckmarsch", main.rueckmarsch_eintrag(sofort, 500.0) is None)

# ---------------------------------------------------------------- 5. Kaputte Eingaben
check("12 None bleibt None", main.rueckmarsch_eintrag(None, 1.0) is None)
check("13 fehlendes Feld bleibt None", main.rueckmarsch_eintrag({"from": "1:1"}, 1.0) is None)
check("14 Text statt Zahl bleibt None", main.rueckmarsch_eintrag(
    {"from": "1:1", "to": "2:1", "start": "x", "arrival": "y"}, 1.0) is None)

# ---------------------------------------------------------------- 6. Lange Reise
weit = {"from": "1:1", "to": "40:40", "units": {"krieger": 3},
        "start": 0.0, "arrival": 79200.0, "rueckweg": False}
r2 = main.rueckmarsch_eintrag(weit, 79200.0)
check("15 22 Spielstunden Rueckweg", r2 and abs((r2["arrival"] - r2["start"]) - 79200.0) < 0.01, r2)
check("16 Rueckweg beginnt bei Ankunft", r2 and r2["start"] == 79200.0, r2)

print(f"ERGEBNIS: {PRUEFUNGEN - len(FEHLER)} bestanden, {len(FEHLER)} Fehler")
for f in FEHLER:
    print("  -", f)
sys.exit(1 if FEHLER else 0)
