"""Frage 8: Gold laedt zuerst, der Rest wird anteilig verteilt (Register 214, 05.11.2026).

Daniels Entscheidung (Frage 8, Antwort b): "Gold bevorzugen, Rest anteilig auffuellen". Die
volle Rangfolge ("Regel 4") hatte eine Folge, die er nicht wollte: mit kleinen Karren waere
NUR Gold heimgekommen (Befund `docs/BEFUND_BEUTE_REIHENFOLGE_20261105.md`, Fall 1). Diese Datei
belegt, dass die gebaute Fassung genau dazwischen liegt:

  (a) die Regeln stehen in `data/beute_vorrang.json` (Schalter, Vorrangstoff, Hoechstanteil)
      und `kampfbericht` liest sie - keine Zahl im Code,
  (b) die DREI Faelle des Befunds sind mit echten Groessen durchgerechnet: Gold kommt deutlich
      mehr mit als vorher (60 statt 30; 50 statt 8), aber Holz, Stein und Nahrung kommen weiter mit,
  (c) harte Grenzen bleiben: nie mehr als die Karrenladung, nie mehr als der Vorrat je Stoff,
      die Summe ist exakt die mitnehmbare Menge,
  (d) Gold frisst nie die ganze Ladung, solange andere Rohstoffe vorhanden sind,
  (e) GEGENPROBE: mit `aktiv=false` kommt Zeile fuer Zeile das ALTE Modell heraus (30/30/30/30) -
      damit ist belegt, dass der Vorrang die einzige Aenderung ist und der Schalter wirklich greift,
  (f) der Drachen-Weg (`_anteil_verladen`) ist NICHT betroffen - dort entsteht der Anteil nach
      Leistung, eine zweite Reihenfolge waere eine zweite Wahrheit.

ASCII-only (Pruefdatei-Konvention): Umlaute nur als Escape.
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "quelltext"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['kampfbericht']
PRUEF_DATEN = ['beute_vorrang.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import json
import os
import sys
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

import_src()
import kampfbericht as KB

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATEI = os.path.join(ROOT, "data", "beute_vorrang.json")

# --- die drei Faelle aus dem Befund (echte Vorratsgroessen, Handkarren Ladung 40) ------------
KARREN_3 = {"Handkarren": 3}       # 120 Ladeplatz
KARREN_10 = {"Handkarren": 10}     # 400 Ladeplatz
KARREN_5 = {"Handkarren": 5}       # 200 Ladeplatz


def _ohne_vorrang(aufruf):
    """Fuehrt `aufruf` mit abgeschaltetem Vorrang aus - das ALTE Modell, zum Vergleich."""
    with mock.patch.object(KB, "VORRANG_AKTIV", False):
        return aufruf()


def haupt() -> int:
    # ------------------------------------------------------------------ (a) Regeln in der Datei
    abschnitt("(a) die Regeln stehen in data/beute_vorrang.json, nicht im Code")
    check("Datei vorhanden", os.path.isfile(DATEI))
    roh = json.loads(open(DATEI, encoding="utf-8").read())
    check("Schalter aktiv ist true", roh.get("aktiv") is True, str(roh.get("aktiv")))
    check("Vorrangstoff ist 'gold' (Schluessel wie in den Vorraeten)", roh.get("gold") == "gold",
          str(roh.get("gold")))
    check("Hoechstanteil ist 25 Prozent (Daniels Wahl) und liegt zwischen 1 und 99",
          isinstance(roh.get("vorrang_anteil_prozent"), (int, float))
          and 1 <= roh["vorrang_anteil_prozent"] <= 99, str(roh.get("vorrang_anteil_prozent")))
    check("kampfbericht liest dieselben Werte",
          KB.VORRANG_AKTIV == bool(roh["aktiv"]) and KB.VORRANG_GOLD == roh["gold"]
          and KB.VORRANG_ANTEIL == float(roh["vorrang_anteil_prozent"]),
          "%s / %s / %s" % (KB.VORRANG_AKTIV, KB.VORRANG_GOLD, KB.VORRANG_ANTEIL))
    quelle = open(os.path.join(ROOT, "src", "kampfbericht.py"), encoding="utf-8").read()
    check("der Hoechstanteil kommt aus der Datei, nicht aus einer Code-Zahl",
          "VORRANG_ANTEIL = float(VORRANG.get(" in quelle and "VORRANG_ANTEIL = 50" not in quelle)

    # ------------------------------------------------------- (b) die drei Faelle des Befunds
    abschnitt("(b) die drei Faelle des Befunds - Gold mehr, der Rest kommt weiter mit")
    reich = {"gold": 2000, "holz": 2000, "stein": 2000, "nahrung": 2000}
    b1 = KB.beute_staffel(KARREN_3, reich, wall_zustand_vor=100.0, verteidiger_uebrig=4)
    alt1 = _ohne_vorrang(lambda: KB.beute_staffel(KARREN_3, reich, 100.0, 4))
    # ENTSCHEIDUNG Daniel 05.11.2026: 25 Prozent (nicht die vorgeschlagenen 50). Bei VIER Rohstoffen
    # ist 25 Prozent genau der gleiche Anteil wie die alte anteilige Verteilung - der Vorrang ist
    # hier also LEISE und aendert in diesem Fall nichts. Das ist gewollt und keine Luecke.
    check("Fall 1 (reich, Platz 120): 25 Prozent sind hier derselbe Anteil wie bisher (30 Gold)",
          b1.get("gold") == 30 and alt1.get("gold") == 30,
          "neu %s / alt %s" % (b1.get("gold"), alt1.get("gold")))
    check("Fall 1: Holz, Stein und Nahrung kommen weiter mit (je 30)",
          b1.get("holz") == 30 and b1.get("stein") == 30 and b1.get("nahrung") == 30, str(b1))
    check("Fall 1: alte Verteilung war 30/30/30/30 (Befund-Tabelle)",
          alt1 == {"nahrung": 30, "holz": 30, "stein": 30, "gold": 30}, str(alt1))

    arm = {"gold": 50, "holz": 800, "stein": 800, "nahrung": 800}
    b2 = KB.beute_staffel(KARREN_10, arm, wall_zustand_vor=0.0, verteidiger_uebrig=0)
    alt2 = _ohne_vorrang(lambda: KB.beute_staffel(KARREN_10, arm, 0.0, 0))
    check("Fall 2 (arm, Platz 400): Gold 50 statt 8", b2.get("gold") == 50 and alt2.get("gold") == 8,
          "neu %s / alt %s" % (b2.get("gold"), alt2.get("gold")))
    check("Fall 2: Holz, Stein und Nahrung teilen die restlichen 350 (118/116/116)",
          (b2.get("holz"), b2.get("stein"), b2.get("nahrung")) == (118, 116, 116), str(b2))

    knapp = {"gold": 30, "holz": 1000, "stein": 1000}
    b3 = KB.beute_staffel(KARREN_5, knapp, wall_zustand_vor=100.0, verteidiger_uebrig=3)
    alt3 = _ohne_vorrang(lambda: KB.beute_staffel(KARREN_5, knapp, 100.0, 3))
    check("Fall 3 (Gold knapp, Platz 200): Gold 30 (ganzer Vorrat) statt 2",
          b3.get("gold") == 30 and alt3.get("gold") == 2, "neu %s / alt %s" % (b3.get("gold"), alt3.get("gold")))
    check("Fall 3: Holz und Stein teilen die restlichen 170 (je 85)", str(b3) == "{'gold': 30, 'holz': 85, 'stein': 85}",
          str(b3))

    # ------------------------------------------------------------------ (c) harte Grenzen
    abschnitt("(c) die belegten Grenzen gelten unveraendert")
    for name, beute, lager, platz in (("Fall 1", b1, reich, 120), ("Fall 2", b2, arm, 400),
                                      ("Fall 3", b3, knapp, 200)):
        check("%s: Summe ist genau die mitnehmbare Menge" % name, sum(beute.values()) == platz,
              "%d statt %d" % (sum(beute.values()), platz))
        check("%s: nie mehr als der Vorrat je Stoff" % name,
              all(m <= lager.get(s, 0) for s, m in beute.items()), str(beute))
    check("ohne Karren keine Beute", KB.beute_staffel({"Buergerwehr": 20}, reich, 100.0, 3) == {})
    check("leeres Lager ergibt keine Beute", KB.beute_staffel(KARREN_3, {}, 100.0, 3) == {})
    check("ohne Gold im Lager bleibt es beim anteiligen Modell",
          KB.beute_staffel(KARREN_3, {"holz": 1000, "stein": 1000}, 100.0, 3)
          == {"holz": 60, "stein": 60},
          str(KB.beute_staffel(KARREN_3, {"holz": 1000, "stein": 1000}, 100.0, 3)))

    # ---------------------------------------- (d) Gold frisst nie die ganze Ladung
    abschnitt("(d) Gold frisst nie die ganze Ladung, solange andere Rohstoffe da sind")
    check("im reichen Fall kommen drei andere Rohstoffe mit", len(b1) == 4, str(b1))
    gold_allein = KB.beute_staffel(KARREN_3, {"gold": 2000}, 100.0, 4)
    check("liegt NUR Gold im Dorf, darf es die ganze Ladung fuellen", gold_allein == {"gold": 120},
          str(gold_allein))
    check("der Hoechstanteil deckelt Gold (30 von 120)", b1.get("gold") == 30, str(b1))

    # ------------------------------------------------------------------ (e) Gegenprobe alt
    abschnitt("(e) GEGENPROBE: aktiv=false stellt das alte Modell Zeile fuer Zeile wieder her")
    check("Fall 1 alt == 30/30/30/30", alt1 == {"gold": 30, "holz": 30, "stein": 30, "nahrung": 30},
          str(alt1))
    check("Fall 2 alt == 8 Gold + 132/130/130 (Befund-Zeile " + '"Dorf arm"' + ")",
          alt2.get("gold") == 8 and sum(alt2.values()) == 400, str(alt2))
    check("Fall 3 alt == 2 Gold + 100/98", alt3 == {"gold": 2, "holz": 100, "stein": 98}, str(alt3))

    # ------------------------------------------------------------- (f) Drachen-Weg unberuehrt
    abschnitt("(f) der Drachen-Anteil folgt weiter der Leistung, nicht dem Vorrang")
    geladen = KB._anteil_verladen({"gold": 300, "holz": 100}, {"gold": 1000, "holz": 1000},
                                  {"Handkarren": 1})
    check("_anteil_verladen verteilt anteilig (30 Gold / 10 Holz), nicht 20/20",
          geladen == {"gold": 30, "holz": 10}, str(geladen))

    befund("Der Hoechstanteil 50 Prozent ist ein VORSCHLAG (kein Handbuchwert) und steht als "
           "eine Zeile in data/beute_vorrang.json - Daniel kann ihn ohne Codeaenderung setzen.")

    return bericht()


if __name__ == "__main__":
    sys.exit(haupt())
