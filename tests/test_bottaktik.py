"""Pruefung der Bot-Taktik (Paket BT) - Koordinaten, Taktiken, Gedaechtnis, Signale.

Belegt gegen `docs/AUFTRAG_BOTTAKTIK_MODUL.md` und den Entwurf
`docs/design/SPIELSPANNUNG_UND_BOTTAKTIK_20261101.md` (Abschnitt D/G).
Geprueft werden: vier Taktiken entscheiden in derselben Lage unterschiedlich,
Koordinaten sind deterministisch, Entfernung ist Manhattan, kein Angriff ohne
Ankuendigung (ausser Raecher), das Gedaechtnis, die Rueckwaertsvertraeglichkeit,
die Anzeige und das Rechenbudget.

Reine Logik: kein Fenster, keine Uhr - `jetzt` wird immer uebergeben, Zufall
kommt aus `random.Random(seed)`.
"""
from __future__ import annotations

import copy
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

ROOT, SRC = import_src()
import bottaktik as BT

TEXT = open(os.path.join(SRC, "bottaktik.py"), encoding="utf-8").read()

WELT = {"spielerdorf": {"x": 10, "y": 10, "name": "Spielerdorf"}}


def baue_bot(name, **werte):
    bot = {"name": name, "aggression": 0.6, "trading": 0.5}
    bot.update(werte)
    return bot


# ============================================================ 1. Taktiken als Daten
abschnitt("1. Taktiken als Daten - die echten Gegennamen")

check("TAKTIKEN ist ein dict", isinstance(BT.TAKTIKEN, dict))
check("fuenf echte Gegennamen (main.BOTS)", set(BT.TAKTIKEN)
      == {"Haug", "Brynhild", "Grom", "Silra", "Krank"})
pflicht = {"name", "naehe", "abstand_grenze", "angriff_schwelle",
           "rueckzug_schwelle", "zielwahl", "erstes_zeichen", "blitz",
           "startzustand"}
check("jede Taktik traegt die Pflichtfelder",
      all(pflicht <= set(t) for t in BT.TAKTIKEN.values()))
check("genau eine Taktik greift ohne Ankuendigung an",
      sum(1 for t in BT.TAKTIKEN.values() if t["blitz"]) == 1)
check("alle Zustaende haben einen Klartext",
      set(BT.ZUSTAENDE) == {BT.SAMMELN, BT.WACHSEN, BT.SICHERN, BT.SUCHEN,
                            BT.MARSCHIEREN, BT.RAUBERN, BT.FLIEHEN, BT.RAECHEN})


# ============================================================ 2. vier Taktiken entscheiden verschieden
abschnitt("2. vier Taktiken entscheiden in derselben Lage unterschiedlich")

namen = ["Haug", "Brynhild", "Grom", "Silra"]
aktionen = {}
for name in namen:
    bot = baue_bot(name, aggression=0.6, x=10, y=6, zustand=BT.SUCHEN)
    e = BT.tick(bot, WELT, 0.0, random.Random(1))
    aktionen[name] = e["aktion"]
check("vier Taktiken liefern vier verschiedene Aktionen",
      len(set(aktionen.values())) == 4, str(aktionen))
check("jede Aktion liegt im erlaubten Satz",
      all(a in ("sammeln", "wachsen", "sichern", "suchen", "marschieren",
                "raeubern", "fliehen", "raechen", "warten")
          for a in aktionen.values()), str(aktionen))


# ============================================================ 3. Koordinaten
abschnitt("3. dorf_positionen - deterministisch, verschieden, im Raster")

check("zwei Aufrufe liefern dieselbe Lage",
      BT.dorf_positionen({"name": "Haug"}, {})
      == BT.dorf_positionen({"name": "Haug"}, {}))
check("verschiedene Bots haben verschiedene Lage",
      BT.dorf_positionen({"name": "Haug"}, {})
      != BT.dorf_positionen({"name": "Grom"}, {}))
check("hoechstens drei Doerfer je Bot",
      all(len(BT.dorf_positionen({"name": n}, {})) <= 3 for n in BT.TAKTIKEN))
check("mindestens ein Dorf je Bot",
      all(len(BT.dorf_positionen({"name": n}, {})) >= 1 for n in BT.TAKTIKEN))
check("alle Felder liegen im 20x20-Raster",
      all(0 <= p["x"] < 20 and 0 <= p["y"] < 20
          for n in BT.TAKTIKEN for p in BT.dorf_positionen({"name": n}, {})))


# ============================================================ 4. Entfernung
abschnitt("4. entfernung - Manhattan statt Kartenmitte")

check("(1,1) zu (4,5) ist 7", BT.entfernung((1, 1), (4, 5)) == 7)
check("Manhattan ist symmetrisch",
      BT.entfernung((1, 1), (4, 5)) == BT.entfernung((4, 5), (1, 1)))
check("gleiche Punkte ergeben 0", BT.entfernung((3, 3), (3, 3)) == 0)
check("keine Kartenmitte-Schaetzung (nicht pauschal 10)",
      BT.entfernung((1, 1), (4, 5)) != 10)


# ============================================================ 5. kein Angriff ohne Signal
abschnitt("5. kein raeubern ohne Signal - Raecher ist die Ausnahme")

for name in ("Haug", "Brynhild", "Grom", "Silra"):
    bot = baue_bot(name, aggression=1.0, x=0, y=0, zustand=BT.SUCHEN)
    e = BT.tick(bot, {"spielerdorf": {"x": 0, "y": 0, "name": "Spielerdorf"}},
                0.0, random.Random(2))
    check(f"{name}: kein Blitzangriff (aktion={e['aktion']})", e["aktion"] != "raeubern")

raecher = {"name": "Krank", "aggression": 0.9, "zustand": BT.RAECHEN,
           "gedaechtnis": {"geschlagen_von": "MeinDorf"}}
e_rache = BT.tick(raecher, {"spielerdorf": {"x": 0, "y": 0, "name": "MeinDorf"}},
                  0.0, random.Random(2))
check("Raecher greift ohne vorherigen Marsch an", e_rache["aktion"] == "raechen")
check("Raecher-Signal ist 'rache'", e_rache["signal"] == "rache")
check("Raecher zielt auf den Schlaeger", e_rache["ziel"] == "MeinDorf")

# positiver Weg: erst der Marsch (mit Signal), dann der Angriff
welt_pos = {"spielerdorf": {"x": 2, "y": 0, "name": "Spielerdorf"}}
bot = baue_bot("Haug", aggression=1.0, x=0, y=0, zustand=BT.SUCHEN)
rng = random.Random(3)
e1 = BT.tick(bot, welt_pos, 0.0, rng)
check("Haug kuendigt den Marsch an", e1["aktion"] == "marschieren", e1["grund"])
check("der Marsch traegt ein Signal und eine Reisezeit > 0",
      bool(e1["signal"]) and (e1["reisezeit"] or 0) > 0)
bot2 = BT.wirkung_anwenden(bot, e1, 0.0)
check("nach dem Marsch ist der Zustand MARSCHIEREN", bot2["zustand"] == BT.MARSCHIEREN)
check("der Marsch hat eine Ankunftszeit", bot2["marsch_ankunft"] > 0.0)
e2 = BT.tick(bot2, welt_pos, bot2["marsch_ankunft"], rng)
check("nach der Reisezeit folgt der Angriff", e2["aktion"] == "raeubern")


# ============================================================ 6. Gedaechtnis
abschnitt("6. wirkung_anwenden - Schlaeger merken, aggressiver werden")

bot = {"name": "Haug", "aggression": 0.5,
       "gedaechtnis": {"geschlagen_von": None}}
entscheidung = {"aktion": "fliehen", "geschlagen_von": "MeinDorf",
                "beute_verloren": 40,
                "wirkung": {"aggression_delta": 0.1}}
neu = BT.wirkung_anwenden(bot, entscheidung, 1000.0)
check("der Schlaeger steht im Gedaechtnis",
      neu["gedaechtnis"]["geschlagen_von"] == "MeinDorf")
check("der Bot wird aggressiver",
      neu["aggression"] > bot["aggression"],
      f"{bot['aggression']} -> {neu['aggression']}")
check("der Beuteverlust wird gemerkt",
      neu["gedaechtnis"]["beute_verloren"] == {"menge": 40, "zeit": 1000.0})
check("die Eingabe bleibt unveraendert",
      bot["gedaechtnis"]["geschlagen_von"] is None and bot["aggression"] == 0.5)


# ============================================================ 7. Rueckwaertsvertraeglichkeit
abschnitt("7. alter Spielstand ohne Gedaechtnis-Felder laeuft")

alt = {"name": "Haug", "aggression": 0.5}
e_alt = BT.tick(alt, WELT, 0.0, random.Random(4))
check("tick auf alten Stand wirft nicht", isinstance(e_alt, dict) and "aktion" in e_alt)
neu_alt = BT.wirkung_anwenden(alt, e_alt, 0.0)
check("wirkung_anwenden auf alten Stand wirft nicht", isinstance(neu_alt, dict))
check("Gedaechtnis-Defaults sind gesetzt",
      neu_alt["gedaechtnis"]["geschlagen_von"] is None)
check("tick mit fehlender Welt wirft nicht und wartet",
      BT.tick(alt, None, 0.0, random.Random(4))["aktion"] == "warten")
check("tick mit leerer Welt wartet",
      BT.tick(alt, {}, 0.0, random.Random(4))["aktion"] == "warten")


# ============================================================ 8. Anzeige
abschnitt("8. anzeige - eine kurze Zeile ohne Zahlenwueste")

z = BT.anzeige({"name": "Haug", "zustand": BT.SUCHEN,
                "letzter_abstand": 3, "naechster_marsch_h": 4.5})
check("anzeige ist eine einzelne Zeile ohne Umbruch",
      isinstance(z, str) and "\n" not in z and len(z) > 0, z)
check("anzeige bleibt kurz", len(z) <= 80, f"len={len(z)}")
check("anzeige wirft bei leerem Bot nicht", isinstance(BT.anzeige({}), str))
check("anzeige nennt die Taktik", "Pluenderer" in z, z)


# ============================================================ 9. Rechenbudget
abschnitt("9. Rechenbudget - 1000 Zugentscheidungen unter einer Sekunde")

bot = baue_bot("Haug", aggression=0.6, x=10, y=6, zustand=BT.SUCHEN)
rng = random.Random(5)
start = time.perf_counter()
for _ in range(1000):
    BT.tick(bot, WELT, 0.0, rng)
dauer = time.perf_counter() - start
check("1000 tick in unter 1 s", dauer < 1.0, f"{dauer * 1000:.1f} ms")


# ============================================================ 10. Selbstpruefung
abschnitt("10. pruefe_taktik - leer = gut")

verstoesse = BT.pruefe_taktik()
check("pruefe_taktik meldet keine Verstoesse", verstoesse == [], str(verstoesse))


# ============================================================ 11. Quellhygiene
abschnitt("11. bottaktik.py - reine Logik, nur Standardbibliothek")

check("bottaktik.py ist reines ASCII", all(ord(c) < 128 for c in TEXT))
check("kein tkinter", "tkinter" not in TEXT)
check("kein main-Import", "import main" not in TEXT and "from main" not in TEXT)
check("keine Datei wird geschrieben", "open(" not in TEXT)
check("Standardkennung vorhanden", BT.STAND.startswith("2026-"))


sys.exit(bericht())
