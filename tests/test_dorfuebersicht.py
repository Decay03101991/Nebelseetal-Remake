# -*- coding: ascii -*-
"""Dorfuebersicht neben der Siedlungskarte (A-3, Register 80).

Daniels Spielbericht 31.10.2026: "welche gebaeude habe ich, wie viele, welcher ertrag" - die
Siedlungskarte zeigte nur Felder. Antwort im Formular: **A) rechte Spalte der Siedlungskarte**.

Was diese Datei beweist
-----------------------
1. Die Dorfuebersicht rechnet mit DERSELBEN Rechnung wie die Produktion: die Summe ueber alle
   Gebaeudetypen ist Punkt fuer Punkt der Ertrag aus `wirtschaft.siedlung_ertrag`.
2. Die Anzahl je Gebaeudetyp stimmt mit den bebauten Feldern ueberein - inklusive der Felder, die
   nichts liefern (sie zaehlen als Gebaeude, aber mit 0 Ertrag, und stehen in `uebersprungen`).
3. Die Anteile summieren sich auf 1 (erlaubte Rundung 1e-3) und sind 0, wenn es keinen Ertrag gibt.
4. Die Stufen werden je Gebaeudetyp gesammelt und lesbar genannt ("Stufe 2", "Stufen 1, 2").
5. Siedler-Bindung: mit Daniels Entscheidung (Frage 5 = B, Schalter `data/bausiedler.json`
   `aktiv: false`) bindet KEIN Bau Siedler; mit `aktiv: true` meldet der Holzfaeller wieder 1 je
   Stueck. Die BELEGTEN Preise in `data/baupreise.json` bleiben dabei unveraendert stehen - die
   Abweichung ist ein Schalter, keine geloeschte Quelle.
6. `baukosten` nimmt den Siedler-Posten genau dann heraus, wenn der Schalter aus ist.

Aufruf:  python -X utf8 tests/test_dorfuebersicht.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import main               # noqa: E402
import wirtschaft         # noqa: E402

HOLZFAELLER = "holzfaeller"
STEINMETZ = "steinmetz"
JAEGER = "jaeger"


def siedlung(bauten, stufen=None, raster=None):
    """Eine Siedlung mit 8x8-Raster; nur die bebauten Felder zaehlen."""
    return {
        "id": "S1", "name": "Testdorf", "besitzer": "spieler",
        "karte": {"raster": raster or ["grasland"] * 64, "spalten": 8, "zeilen": 8,
                  "typ_name": "Testkarte"},
        "bauten": dict(bauten), "stufen": dict(stufen or {}),
        "vorraete": {}, "waren": {}, "einheiten": {}, "bevoelkerung": 10.0,
    }


# ==========================================================================
abschnitt("1. Summe der Uebersicht == Ertrag der Produktion (eine Rechnung)")

# 2 Holzfaeller (Wald), 3 Farmen (Grasland), 1 Jaeger (Wald) - Jaeger liefert ZWEI Rohstoffe.
raster = ["wald"] * 64
bauten = {"0": HOLZFAELLER, "1": HOLZFAELLER, "8": "farm", "9": "farm",
          "16": "farm", "24": JAEGER}
s = siedlung(bauten, raster=raster)
ueb = wirtschaft.dorf_uebersicht(s, {}, siedler_bindend=False)
ertrag = {k: v for k, v in wirtschaft.siedlung_ertrag(s, {}).items()
          if k != wirtschaft.UEBERSPRUNGEN}
check("1 die Summe der Uebersicht ist der Ertrag aus siedlung_ertrag",
      ueb["summe"]["ertrag"] == {r: round(v, 2) for r, v in ertrag.items()},
      f"{ueb['summe']['ertrag']} vs {ertrag}")
check("1 die Summe aller Einzelertraege stimmt mit der Summenzeile",
      round(sum(g["summe"] for g in ueb["gebaeude"]), 2) == ueb["summe"]["summe"],
      str([g["summe"] for g in ueb["gebaeude"]]))

zaehlung = {}
for g in ueb["gebaeude"]:
    zaehlung[g["gebaeude"]] = g["anzahl"]
check("1 zwei Holzfaeller werden als zwei gezaehlt", zaehlung.get(HOLZFAELLER) == 2,
      str(zaehlung))
check("1 drei Farmen werden als drei gezaehlt", zaehlung.get("farm") == 3, str(zaehlung))
check("1 die Summenzeile zaehlt alle Gebaeude", ueb["summe"]["anzahl"] == 6,
      str(ueb["summe"]["anzahl"]))
jaeger = next(g for g in ueb["gebaeude"] if g["gebaeude"] == JAEGER)
check("1 der Jaeger liefert ZWEI Rohstoffe (Nahrung und Leder)",
      len(jaeger["ertrag"]) == 2, str(jaeger["ertrag"]))


# ==========================================================================
abschnitt("2. Anteile und Stufen")

summe_anteil = round(sum(g["anteil"] for g in ueb["gebaeude"]), 3)
check("2 die Anteile summieren sich auf 1", abs(summe_anteil - 1.0) <= 0.001, str(summe_anteil))
check("2 der staerkste Gebaeudetyp steht oben",
      ueb["gebaeude"][0]["summe"] >= ueb["gebaeude"][-1]["summe"],
      f"{ueb['gebaeude'][0]['summe']} / {ueb['gebaeude'][-1]['summe']}")

leer = siedlung({}, raster=["grasland"] * 64)
check("2 ohne Gebaeude ist die Uebersicht leer (kein Anteil 0/0)",
      wirtschaft.dorf_uebersicht(leer, {})["gebaeude"] == [], "")

s_stufen = siedlung({"0": HOLZFAELLER, "1": HOLZFAELLER}, stufen={"0": 1, "1": 3},
                    raster=raster)
g_stufen = wirtschaft.dorf_uebersicht(s_stufen, {})["gebaeude"][0]
check("2 zwei verschiedene Stufen werden gesammelt genannt",
      g_stufen["stufen"] == [1, 3] and g_stufen["stufen_text"] == "Stufen 1, 3",
      f"{g_stufen['stufen']} / {g_stufen['stufen_text']}")
s_eine = siedlung({"0": HOLZFAELLER}, stufen={"0": 2}, raster=raster)
g_eine = wirtschaft.dorf_uebersicht(s_eine, {})["gebaeude"][0]
check("2 eine einzige Stufe heisst 'Stufe 2'", g_eine["stufen_text"] == "Stufe 2",
      g_eine["stufen_text"])


# ==========================================================================
abschnitt("3. Siedler-Bindung: Schalter statt geloeschter Quelle")

preise = json.load(open(os.path.join(ROOT, "data", "baupreise.json"), encoding="utf-8"))["preise"]
check("3 die BELEGTEN Preise stehen unveraendert in der Datei (Holzfaeller 1 Siedler)",
      preise[HOLZFAELLER].get("siedler") == 1, str(preise[HOLZFAELLER]))
check("3 auch Steinmetz und Jaeger tragen ihren Siedler-Preis in der Datei",
      preise[STEINMETZ].get("siedler") == 1 and preise[JAEGER].get("siedler") == 1, "")
schalter = json.load(open(os.path.join(ROOT, "data", "bausiedler.json"), encoding="utf-8"))
check("3 Daniels Entscheidung (Frage 5 = B) ist der Schalter aus",
      schalter.get("aktiv") is False, str(schalter.get("aktiv")))

aus = wirtschaft.dorf_uebersicht(s, {}, siedler_bindend=False)
an = wirtschaft.dorf_uebersicht(s, {}, siedler_bindend=True)
check("3 mit Daniels Entscheidung bindet kein Bau Siedler",
      aus["summe"]["siedler"] == 0 and all(g["siedler"] == 0 for g in aus["gebaeude"]),
      str(aus["summe"]["siedler"]))
check("3 der Hinweis nennt die Abweichung und die belegten Preise",
      "keine Siedler" in aus["hinweis"] and "Holzf" in aus["hinweis"], aus["hinweis"])
check("3 mit dem Original-Schalter binden 2 Holzfaeller + 1 Jaeger genau 3 Siedler",
      an["summe"]["siedler"] == 3, str(an["summe"]["siedler"]))
check("3 der Hinweis nennt mit dem Original den Beleg",
      "1838857" in an["hinweis"], an["hinweis"])

abschnitt("4. baukosten folgt demselben Schalter")
check("4 baukosten(Holzfaeller) enthaelt mit Daniels Entscheidung keinen Siedler",
      "siedler" not in main.baukosten(HOLZFAELLER), str(main.baukosten(HOLZFAELLER)))
check("4 baukosten liefert weiter Holz und Stein (nur der Siedler faellt weg)",
      main.baukosten(HOLZFAELLER).get("holz") == 10
      and main.baukosten(HOLZFAELLER).get("stein") == 5, str(main.baukosten(HOLZFAELLER)))
check("4 main liest den Schalter aus EINER Stelle (wirtschaft)",
      main.bausiedler_aktiv() == wirtschaft.siedler_bindung_aktiv(), "")


# ==========================================================================
abschnitt("5. Nichts wird still verschluckt")

s_kaputt = siedlung({"0": JAEGER, "1": "GIBTESNICHT"},
                    raster=["sumpf"] + ["grasland"] * 63)
u_kaputt = wirtschaft.dorf_uebersicht(s_kaputt, {})
check("5 unbekannte Gebaeude stehen in uebersprungen",
      any("unbekanntes Gebaeude" in t for t in u_kaputt["uebersprungen"]),
      str(u_kaputt["uebersprungen"]))
check("5 ein Jaeger auf Sumpf wird mit Begruendung uebersprungen",
      any("Sumpf" in t for t in u_kaputt["uebersprungen"]), str(u_kaputt["uebersprungen"]))
check("5 das Gebaeude selbst wird trotzdem gezaehlt (es steht ja da)",
      any(g["gebaeude"] == JAEGER for g in u_kaputt["gebaeude"]),
      str([g["gebaeude"] for g in u_kaputt["gebaeude"]]))

befund("Die GUI-Spalte ist in dieser Datei nicht gezeichnet - der GUI-Rundlauf und die Probe "
       "auf dem echten Spielstand decken sie ab", "")

print("\nHinweis: Schalterstand jetzt =", "AN" if wirtschaft.siedler_bindung_aktiv() else "AUS")
sys.exit(bericht())
