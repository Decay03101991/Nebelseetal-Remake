# -*- coding: ascii -*-
"""Pruefung der Zielpruefung: zielstatus(orte, jetzt, haltestart) -> dict.

Gegenstand ist die NEUE Funktion in src/spieloekonomie.py (Abschnitt "Schritt 7"):
  zielstatus(orte, jetzt, haltestart=None) -> dict
Sie liefert: sieg, haltestart, qualitaet, deckung, reserve, handel, armee, plan.

Richtschnur sind die Pflichtzusagen aus
docs/audits/entwurf_spieloekonomie_sol_2026-10-05.txt, Zeile 688-715, woertlich u. a.:
  "Forschungs-/Kriegspunktfarm mit schlechten Karten gewinnt nie;
   Hin-und-her-Fracht ohne Verbrauch gewinnt nie;
   Verlust einer Schluesselkarte setzt Haltebeginn zurueck;
   Speicherstand bewahrt Haltebeginn;
   die Reservepruefung verwendet oertlichen Bestand".

Regeln aus data/spieloekonomie.json:
  versorgung_stunden = 24 (Halte- UND Messfenster), mindestsiedlungen = 4,
  portfoliofaktor = 1.0, spezialistenfaktor = 1.4, plan = 9 Rohstoffe.

WICHTIG (Falle aus der Vormessung): fensterproduktion zaehlt nur Zeilen im Fenster
[jetzt-24h, jetzt]. Jede Messung baut darum einen Zustand, dessen Produktionszeile
GENAU dieses Fenster abdeckt - sonst misst der Test seinen Datensatz, nicht die Funktion.

Die Orte entstehen in dieser Datei selbst als dicts. Jede Zusage nennt bei Verletzung
Soll und Ist. Aufruf:  python -X utf8 tests/test_versorgungsziel.py
"""
from __future__ import annotations

import copy
import itertools
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
import spieloekonomie as O  # noqa: E402
import einheiten as E  # noqa: E402

REGELN = O.REGELN
PLAN = REGELN["plan"]
FENSTER = REGELN["versorgung_stunden"] * 3600  # 86400 s
J = 1000000.0  # neutrale Spielzeit

# Ein Trenner fuer Details, damit Soll/Ist lesbar bleiben.
def si(soll, ist):
    return "Soll " + str(soll) + " / Ist " + str(ist)


# --------------------------------------------------------------------------- Hilfen
def suche_verbund():
    """Per Schleife ein Vierergespann aus dem Kartenvorrat, das die Qualitaet erfuellt."""
    eintraege = O.G["kartenvorrat"]["kolonien"]
    for combo in itertools.combinations(range(len(eintraege)), 4):
        karten = [O.feste_karte("verbund" + str(i), eintraege[i]) for i in combo]
        if O.kartenqualitaet(karten)["erfuellt"]:
            return karten, combo
    return None, None


KARTEN, COMBO = suche_verbund()
SCHLECHT = O.feste_karte("schlecht", O.G["kartenvorrat"]["start"])


def ort(oid, karte, vorraete=None, reserve=None, einheiten_=None,
        produktionsjournal=None, verbrauchsjournal=None, fertigjournal=None):
    """Ein Ort mit genau den Feldern, die zielstatus liest."""
    return {
        "id": oid,
        "karte": karte,
        "vorraete": dict(vorraete or {}),
        "reserve": dict(reserve or {}),
        "einheiten": dict(einheiten_ or {}),
        "produktionsjournal": list(produktionsjournal or []),
        "verbrauchsjournal": list(verbrauchsjournal or []),
        "fertigjournal": list(fertigjournal or []),
    }


def gutes_feld(jetzt, karten=None, vorrat_verdoppelt=True):
    """Vier Orte, die ALLE acht Bedingungen erfuellen - gemessen zum Zeitpunkt jetzt.

    Das Produktionsjournal deckt genau [jetzt-24h, jetzt] ab (Fensterfalle vermieden);
    der Verbrauch liegt frisch im Fenster; beide Rollen und Ware+Forschung sind gesetzt.
    """
    karten = karten or KARTEN
    basis = {r: v * 2.0 for r, v in PLAN.items()} if vorrat_verdoppelt else dict(PLAN)
    o0 = ort(
        "O0", karten[0],
        vorraete=basis,
        reserve=dict(PLAN),
        einheiten_={"Krieger": 1, "Kundschafter": 1},
        produktionsjournal=[{"ab": jetzt - FENSTER, "bis": jetzt, "mengen": dict(PLAN)}],
        verbrauchsjournal=[{"zeit": jetzt - 3600, "rohstoff": "holz", "menge": 5, "ziel": "O1"}],
        fertigjournal=[{"zeit": jetzt, "art": "ware", "name": "Brot"},
                       {"zeit": jetzt, "art": "forschung", "name": "Wagenbau"}],
    )
    o1 = ort("O1", karten[1],
             verbrauchsjournal=[{"zeit": jetzt - 3600, "rohstoff": "stein", "menge": 5, "ziel": "O0"}])
    o2 = ort("O2", karten[2])
    o3 = ort("O3", karten[3])
    return [o0, o1, o2, o3]


# ==========================================================================
abschnitt("0. Aufbau: der geprueften Verbund traegt die Kartenqualitaet")

check("0a es gibt ein Vierergespann (mindestsiedlungen = 4)", KARTEN is not None,
      "kein Gespann gefunden")
if KARTEN is None:  # ohne Karten ist alles Weitere sinnlos - sauber beenden
    sys.exit(bericht())
check("0b das gefundene Gespann ist genau vier Karten", len(KARTEN) == 4,
      si(4, len(KARTEN)))
q0 = O.kartenqualitaet(KARTEN)
check("0c seine Kartenqualitaet ist erfuellt", bool(q0["erfuellt"]), str(q0["erfuellt"]))
check("0d Mittelwert je Achse >= portfoliofaktor 1.0",
      min(q0["mittel"]) >= REGELN["portfoliofaktor"], si(">= 1.0", [round(x, 3) for x in q0["mittel"]]))
check("0e bester Einzelwert je Achse >= spezialistenfaktor 1.4",
      min(q0["beste"]) >= REGELN["spezialistenfaktor"], si(">= 1.4", [round(x, 3) for x in q0["beste"]]))
print("      Gespann:", str(COMBO), [e["id"] for e in [O.G["kartenvorrat"]["kolonien"][i] for i in COMBO]])


# ==========================================================================
abschnitt("1. ERFUELLTER VERBUND: haltestart == jetzt, sieg False, alle acht Werte")

r1 = O.zielstatus(gutes_feld(J), J, None)
check("1a sieg ist False (das Haltefenster hat noch nicht begonnen zu laufen)",
      r1["sieg"] is False, si(False, r1["sieg"]))
check("1b haltestart ist genau jetzt (nicht None)", r1["haltestart"] == J,
      si(J, r1["haltestart"]))
check("1c haltestart ist nicht None", r1["haltestart"] is not None, str(r1["haltestart"]))
check("1d qualitaet.erfuellt ist True", bool(r1["qualitaet"]["erfuellt"]) is True,
      str(r1["qualitaet"]))
check("1e deckung ist >= 1.0", r1["deckung"] >= 1.0, si(">= 1.0", r1["deckung"]))
check("1f reserve ist True", r1["reserve"] is True, str(r1["reserve"]))
check("1g handel ist True", r1["handel"] is True, str(r1["handel"]))
check("1h armee ist True", r1["armee"] is True, str(r1["armee"]))
check("1i plan ist True", r1["plan"] is True, str(r1["plan"]))
print("      Rueckgabe:", str({k: r1[k] for k in
      ("sieg", "haltestart", "deckung", "reserve", "handel", "armee", "plan")}),
      "| qualitaet.erfuellt", r1["qualitaet"]["erfuellt"])


# ==========================================================================
abschnitt("2. HALTEFENSTER GENAU: eine Sekunde vor / genau bei haltestart + 24 h")

H = 500000.0
vor = O.zielstatus(gutes_feld(H + FENSTER - 1), H + FENSTER - 1, H)
genau = O.zielstatus(gutes_feld(H + FENSTER), H + FENSTER, H)
check("2a eine Sekunde vor haltestart + 24 h ist sieg False",
      vor["sieg"] is False, si(False, vor["sieg"]))
check("2b genau bei haltestart + 24 h ist sieg True",
      genau["sieg"] is True, si(True, genau["sieg"]))
check("2c der Zustand davor ist noch erfuellt (Vorbedingung, nicht Fehlerquelle)",
      vor["haltestart"] == H, si(H, vor["haltestart"]))
check("2d haltestart wandert bei der Sekunde davor NICHT", vor["haltestart"] == H,
      si(H, vor["haltestart"]))
check("2e haltestart wandert beim Sieg NICHT", genau["haltestart"] == H,
      si(H, genau["haltestart"]))
check("2f bei haltestart=None wuerde der Beginn bei jetzt neu gesetzt (Gegenprobe)",
      O.zielstatus(gutes_feld(J), J, None)["haltestart"] == J, si(J, "None-Fall"))


# ==========================================================================
abschnitt("3. VORGEHEN: uebergebener haltestart kommt unveraendert zurueck")

frisch_start = J - 3600
r3 = O.zielstatus(gutes_feld(J), J, frisch_start)
check("3a haltestart wird uebergeben und unveraendert zurueckgegeben",
      r3["haltestart"] == frisch_start, si(frisch_start, r3["haltestart"]))
check("3b frischer Beginn (< 24 h zurueck) -> sieg noch False", r3["sieg"] is False,
      si(False, r3["sieg"]))
r3b = O.zielstatus(gutes_feld(J), J, J - FENSTER)
check("3c auch bei vollem Fenster bleibt der uebergebene Beginn stehen (kein Neustart)",
      r3b["haltestart"] == J - FENSTER, si(J - FENSTER, r3b["haltestart"]))
check("3d ein bereits gelaufenes Fenster macht sieg True", r3b["sieg"] is True,
      si(True, r3b["sieg"]))


# ==========================================================================
abschnitt("4. SCHLUESSELKARTE VERLOREN: eine Karte weniger -> haltestart None")

drei = gutes_feld(J)[:3]
r4 = O.zielstatus(drei, J, H)  # H = alter Haltebeginn, darf NICHT ueberleben
check("4a mit drei Karten ist die Qualitaet nicht erfuellt",
      not r4["qualitaet"]["erfuellt"], str(r4["qualitaet"]))
check("4b haltestart wird None (Haltebeginn zurueckgesetzt)", r4["haltestart"] is None,
      si(None, r4["haltestart"]))
check("4c sieg ist False", r4["sieg"] is False, si(False, r4["sieg"]))


# ==========================================================================
abschnitt("5. HIN-UND-HER-FRACHT OHNE VERBRAUCH: leeres verbrauchsjournal")

f5 = gutes_feld(J)
for o in f5:
    o["verbrauchsjournal"] = []
r5 = O.zielstatus(f5, J, None)
check("5a ohne Verbrauch ist handel False", r5["handel"] is False, si(False, r5["handel"]))
check("5b haltestart ist None", r5["haltestart"] is None, si(None, r5["haltestart"]))
check("5c sieg ist False", r5["sieg"] is False, si(False, r5["sieg"]))


# ==========================================================================
abschnitt("6. VERBRAUCH IN NUR EINEM ORT: zwei Rohstoffe, aber nur EIN Ort")

f6 = gutes_feld(J)
f6[0]["verbrauchsjournal"] = [
    {"zeit": J - 3600, "rohstoff": "holz", "menge": 5, "ziel": "O1"},
    {"zeit": J - 3600, "rohstoff": "stein", "menge": 5, "ziel": "O1"},
]
f6[1]["verbrauchsjournal"] = []
r6 = O.zielstatus(f6, J, None)
check("6a zwei Rohstoffe aus nur einem Ort ergeben handel False",
      r6["handel"] is False, si("False (zwei Orte verlangt)", r6["handel"]))
check("6b haltestart ist None", r6["haltestart"] is None, si(None, r6["haltestart"]))
# Gegenprobe: derselbe Verbrauch auf ZWEI Orte -> handel True
f6b = gutes_feld(J)
r6b = O.zielstatus(f6b, J, None)
check("6c derselbe Verbrauch auf zwei Orte ergibt handel True (Gegenprobe)",
      r6b["handel"] is True, si(True, r6b["handel"]))


# ==========================================================================
abschnitt("7. RESERVE AUS OERTLICHEM BESTAND, nicht global")

f7 = gutes_feld(J)
# O0 fordert mehr Reserve, als es SELBST im Vorrat hat; O1 hat riesigen Vorrat.
f7[0]["reserve"] = {"holz": 5000.0}
f7[1]["vorraete"] = {"holz": 1.0e9}
r7 = O.zielstatus(f7, J, None)
check("7a Reserve des Ortes > sein eigener Vorrat -> reserve False",
      r7["reserve"] is False, si(False, r7["reserve"]))
check("7b der hohe Vorrat des ANDEREN Ortes gleicht das NICHT aus",
      r7["reserve"] is False, si("False trotz 1e9 in O1", r7["reserve"]))
check("7c haltestart ist None", r7["haltestart"] is None, si(None, r7["haltestart"]))
# Gegenprobe: Reserve im eigenen Vorrat -> reserve True
f7b = gutes_feld(J)
r7b = O.zielstatus(f7b, J, None)
check("7d Reserve im eigenen Vorrat -> reserve True (Gegenprobe)",
      r7b["reserve"] is True, si(True, r7b["reserve"]))


# ==========================================================================
abschnitt("8. PRODUKTION EINGESTELLT: leeres produktionsjournal -> deckung 0.0")

f8 = gutes_feld(J)
for o in f8:
    o["produktionsjournal"] = []
r8 = O.zielstatus(f8, J, None)
check("8a deckung ist 0.0", r8["deckung"] == 0.0, si(0.0, r8["deckung"]))
check("8b haltestart ist None", r8["haltestart"] is None, si(None, r8["haltestart"]))
check("8c sieg ist False", r8["sieg"] is False, si(False, r8["sieg"]))


# ==========================================================================
abschnitt("9. BEIDE ROLLEN: ohne Kaempfer ODER ohne Kundschafter -> armee False")

f9a = gutes_feld(J)
f9a[0]["einheiten"].pop("Krieger")
r9a = O.zielstatus(f9a, J, None)
check("9a ohne Kaempfer ist armee False", r9a["armee"] is False, si(False, r9a["armee"]))
check("9b haltestart ist None", r9a["haltestart"] is None, si(None, r9a["haltestart"]))

f9b = gutes_feld(J)
f9b[0]["einheiten"].pop("Kundschafter")
r9b = O.zielstatus(f9b, J, None)
check("9c ohne Kundschafter ist armee False", r9b["armee"] is False, si(False, r9b["armee"]))
check("9d haltestart ist None", r9b["haltestart"] is None, si(None, r9b["haltestart"]))

check("9e Krieger hat Rolle kaempfer", E.rolle("Krieger") == "kaempfer",
      si("kaempfer", E.rolle("Krieger")))
check("9f Kundschafter hat Rolle kundschafter", E.rolle("Kundschafter") == "kundschafter",
      si("kundschafter", E.rolle("Kundschafter")))


# ==========================================================================
abschnitt("10. WARE UND FORSCHUNG: nur eines reicht nicht, beide tragen")

f10a = gutes_feld(J)
f10a[0]["fertigjournal"] = [{"zeit": J, "art": "ware", "name": "Brot"}]
r10a = O.zielstatus(f10a, J, None)
check("10a nur 'ware' im fertigjournal -> kein Sieg", r10a["sieg"] is False,
      si(False, r10a["sieg"]))
check("10b nur 'ware' -> haltestart None", r10a["haltestart"] is None,
      si(None, r10a["haltestart"]))

f10b = gutes_feld(J)
f10b[0]["fertigjournal"] = [{"zeit": J, "art": "forschung", "name": "Wagenbau"}]
r10b = O.zielstatus(f10b, J, None)
check("10c nur 'forschung' im fertigjournal -> kein Sieg", r10b["sieg"] is False,
      si(False, r10b["sieg"]))
check("10d nur 'forschung' -> haltestart None", r10b["haltestart"] is None,
      si(None, r10b["haltestart"]))

f10c = gutes_feld(J)  # hat beide Arten (Basiszustand)
r10c = O.zielstatus(f10c, J, None)
check("10e beide Arten -> haltestart wird gesetzt (traegt)", r10c["haltestart"] == J,
      si(J, r10c["haltestart"]))


# ==========================================================================
abschnitt("11. PUNKTEFARM GEWINNT NIE: vier schlechte Karten")

schlechte = [SCHLECHT, SCHLECHT, SCHLECHT, SCHLECHT]
q_schlecht = O.kartenqualitaet(schlechte)
check("11a vier Startkarten erfuellen die Qualitaet NICHT",
      not q_schlecht["erfuellt"], str(q_schlecht))
f11 = gutes_feld(J, karten=schlechte)  # alles andere perfekt, nur die Karten schlecht
r11 = O.zielstatus(f11, J, H)  # alter Haltebeginn H, darf NICHT ueberleben
check("11b sieg ist False trotz erfuellter Nebenwerte", r11["sieg"] is False,
      si(False, r11["sieg"]))
check("11c haltestart ist None", r11["haltestart"] is None, si(None, r11["haltestart"]))
check("11d plan/reserve/handel/armee bleiben daneben erfuellt (Karten sind der Grund)",
      r11["plan"] is True and r11["reserve"] is True and r11["handel"] is True
      and r11["armee"] is True,
      "plan/reserve/handel/armee = " + str((r11["plan"], r11["reserve"],
                                            r11["handel"], r11["armee"])))


# ==========================================================================
abschnitt("12. LEERER VERBUND: zielstatus([], jetzt, None) stuerzt nicht ab")

r12 = O.zielstatus([], J, None)
check("12a liefert ueberhaupt ein dict", isinstance(r12, dict), str(type(r12)))
check("12b sieg ist False", r12["sieg"] is False, si(False, r12["sieg"]))
check("12c haltestart ist None", r12["haltestart"] is None, si(None, r12["haltestart"]))
check("12d kein leer-wahr: reserve ist False", r12["reserve"] is False,
      si(False, r12["reserve"]))
check("12e deckung ist 0.0", r12["deckung"] == 0.0, si(0.0, r12["deckung"]))


# ==========================================================================
abschnitt("13. KEIN SEITENEFFEKT: die uebergebenen Orte bleiben unveraendert")

f13 = gutes_feld(J)
vorher13 = copy.deepcopy(f13)
O.zielstatus(f13, J, 123.0)
check("13a ein erfuellter Verbund wird nicht veraendert", f13 == vorher13,
      "deepcopy-Vergleich")

f13b = gutes_feld(J)
f13b[0]["produktionsjournal"] = []
vorher13b = copy.deepcopy(f13b)
O.zielstatus(f13b, J, None)
check("13b auch ein nicht erfuellter Verbund wird nicht veraendert", f13b == vorher13b,
      "deepcopy-Vergleich")


# ==========================================================================
abschnitt("14. ZEITFENSTER: Verbrauch AELTER als 24 h zaehlt NICHT mehr")

f14 = gutes_feld(J)
alt = J - FENSTER - 1  # eine Sekunde aelter als das Fenster erlaubt
for o in f14:
    o["verbrauchsjournal"] = [dict(z, zeit=alt) for z in o["verbrauchsjournal"]]
r14 = O.zielstatus(f14, J, None)
check("14a ein Verbrauch von vor mehr als 24 h -> handel False",
      r14["handel"] is False, si(False, r14["handel"]))
check("14b haltestart ist None", r14["haltestart"] is None, si(None, r14["haltestart"]))

f14b = gutes_feld(J)
frisch = J - 3600  # klar innerhalb des Fensters
for o in f14b:
    o["verbrauchsjournal"] = [dict(z, zeit=frisch) for z in o["verbrauchsjournal"]]
r14b = O.zielstatus(f14b, J, None)
check("14c derselbe Verbrauch frisch (1 h alt) -> handel True (zweite Zeit)",
      r14b["handel"] is True, si(True, r14b["handel"]))

# Randprobe sauber: zeit exakt auf jetzt-24h ist die untere Aussengrenze (ab < z verlangt)
f14c = gutes_feld(J)
for o in f14c:
    o["verbrauchsjournal"] = [dict(z, zeit=J - FENSTER) for z in o["verbrauchsjournal"]]
r14c = O.zielstatus(f14c, J, None)
check("14d genau auf jetzt - 24 h (ab == zeit) zaehlt NICHT (Grenze ist echt)",
      r14c["handel"] is False, si(False, r14c["handel"]))


# ==========================================================================
abschnitt("15. Sieg erst NACH dem vollen Fenster (Zusammenspiel mit dem Abbau)")

# Ein Zustand, der genau erfuellt ist, und ein alter Beginn: sieg True.
r15 = O.zielstatus(gutes_feld(J), J, J - FENSTER)
check("15a erfuellt + volles Fenster zurueck -> sieg True", r15["sieg"] is True,
      si(True, r15["sieg"]))
# Faellt eine Bedingung weg, muss der Haltebeginn zurueckgesetzt werden (kein Sieg).
f15 = gutes_feld(J)
f15[0]["einheiten"].pop("Kundschafter")
r15b = O.zielstatus(f15, J, J - FENSTER)
check("15b faellt eine Bedingung weg, kein Sieg mehr", r15b["sieg"] is False,
      si(False, r15b["sieg"]))
check("15c und der Haltebeginn ist zurueckgesetzt (None)", r15b["haltestart"] is None,
      si(None, r15b["haltestart"]))


sys.exit(bericht())
