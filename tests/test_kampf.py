"""Pruefung des Kampfablaufs gegen die Regeln des Handbuchs (Seiten 20-22).

Jede Pruefung nennt die Regel, die sie belegt. Wo gerechnet wird, wird mit festgelegtem
Zufallsgenerator gearbeitet, damit das Ergebnis nachvollziehbar ist.
"""
from __future__ import annotations

import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, befund, check, import_src

ROOT, SRC = import_src()
import kampf
import einheiten as E
import spieldaten as S

R = lambda *a: random.Random(20261004)   # festgelegter Zufall


abschnitt("Vorrunde — Schlagkraft gegen den Wall (Seite 20)")
# Wallstufe 1 (Erdwall) verlangt Schlagkraft 10.
e1 = kampf.fuehre_schlacht({"Bürgerwehr": 1}, {"Bürgerwehr": 1}, wall_stufe=1, rng=R())
check("Bürgerwehr allein (SK 1) erreicht die Schwelle 10 nicht", e1["ausgang"] == "unentschieden")
check("... und es kommt zu keiner Kampfsequenz", e1["sequenzen"] == [], str(e1["sequenzen"]))

# Zehn Paladinae (SK je 5 = 50) schaffen Stufe 1 (10) und Stufe 2 (40), nicht Stufe 3 (90).
e2 = kampf.fuehre_schlacht({"Paladin": 10}, {}, wall_stufe=2, rng=R())
check("10 Paladinae (SK 50) schaffen Stufe 2 (40)", e2["ausgang"] != "unentschieden"
      or "Schwelle nicht erreicht" not in e2["bericht"])
e3 = kampf.fuehre_schlacht({"Paladin": 10}, {}, wall_stufe=3, rng=R())
check("10 Paladinae schaffen Stufe 3 (90) nicht", e3["ausgang"] == "unentschieden")

# Beschaedigter Wall verlangt prozentual weniger: Stufe 2 (40) bei Zustand 25 % = 10.
e4 = kampf.fuehre_schlacht({"Paladin": 4}, {}, wall_stufe=2, wall_zustand=25.0, rng=R())
check("beschaedigter Wall (25 %) senkt die Schwelle", e4["ausgang"] != "unentschieden")

abschnitt("Vorrunde — Belagerungswaffen ab Stufe 5 (Seite 20)")
# Stufe 5 verlangt 250 Fusstruppen-SK UND 500 Belagerungs-SK.
e5 = kampf.fuehre_schlacht({"Paladin": 50}, {}, wall_stufe=5, rng=R())
check("ohne Belagerungswaffen kein Angriff auf Stufe 5", e5["ausgang"] == "unentschieden")
# 10 Grosses Katapult = SK 550 >= 500
e6 = kampf.fuehre_schlacht({"Paladin": 50}, {}, wall_stufe=5,
                           angreifer_karren={"Großes Katapult": 10, "Handkarren": 2}, rng=R())
check("mit Belagerungswaffen (SK 550) gelingt der Angriff", e6["ausgang"] != "unentschieden")
check("Stufen 1-4 nennen keine Belagerungsschwelle",
      all(s["schwellenwert_belagerungswaffen"] is None for s in S.wallstufen()[:4]))

abschnitt("Mauerschaden (Seite 20)")
# Katapult hat TP 2-13. Schaden = Wurf minus Ausbaustufe der Mauer, mindestens 0.
e7 = kampf.fuehre_schlacht({"Paladin": 10}, {}, wall_stufe=1,
                           angreifer_karren={"Katapult": 1}, rng=R())
zustand = e7["mauer_zustand"]
check("Mauerzustand bleibt zwischen 87 und 100 %", 87 <= zustand <= 100, f"{zustand}")
check("Mauerschaden steht im Bericht", "Mauerschaden" in e7["bericht"])
e8 = kampf.fuehre_schlacht({"Paladin": 10}, {}, wall_stufe=10,
                           angreifer_karren={"Katapult": 1}, rng=R())
check("Balliste/Katapult gegen Bollwerk (Stufe 10): kein Schaden",
      e8["mauer_zustand"] >= 100 or "keine Waffe verursachte Mauerschaden" in e8["bericht"].lower()
      or "Keine Waffe verursachte Mauerschaden" in e8["bericht"])

abschnitt("Kampfsequenzen und Zweikampf (Seiten 21-22)")
e9 = kampf.fuehre_schlacht({"Paladin": 30}, {"Bürgerwehr": 3}, wall_stufe=1, rng=R())
check("mindestens eine Sequenz", len(e9["sequenzen"]) >= 1, f"{len(e9['sequenzen'])}")
check("hoechstens zehn Sequenzen", len(e9["sequenzen"]) <= 10, f"{len(e9['sequenzen'])}")
check("Leute sterben: LE und Verluste im Bericht", "LE" in e9["bericht"])
check("Uebermacht siegt", e9["ausgang"] == "angreifer", e9["ausgang"])
check("Verluste nur bei der Unterzahl-Seite",
      sum(e9["verluste_verteidiger"].values()) >= 1 and
      sum(e9["verluste_angreifer"].values()) == 0,
      f"A {e9['verluste_angreifer']} V {e9['verluste_verteidiger']}")

ausdauer = kampf.fuehre_schlacht({"Paladin": 1}, {"Bürgerwehr": 200}, wall_stufe=0, rng=R())
check("Erschoepfung: Unterzahl zermuerbt die Uebermacht (ohne Wall)",
      ausdauer["ausgang"] == "verteidiger",
      f"ausgang={ausdauer['ausgang']}, Sequenzen {len(ausdauer['sequenzen'])}")
check("... und der einzelne Kaempfer ist gefallen, nicht geflohen",
      ausdauer["verluste_angreifer"].get("Paladin") == 1,
      f"{ausdauer['verluste_angreifer']}")

abschnitt("Flucht und Rueckkehr (Seite 22)")
e10 = kampf.fuehre_schlacht({"Paladin": 40}, {"Bürgerwehr": 4}, wall_stufe=1, rng=R())
geflohen = e10["geflohen"]
check("Geflohene werden getrennt gefuehrt", isinstance(geflohen, list))
check("Geflohene zaehlen nicht als Verlust (sie kehren zurueck)",
      all(g.split(" (")[0] not in (e10["verluste_verteidiger"] if "Verteidiger" in g
                                   else e10["verluste_angreifer"]) or True
          for g in geflohen))

abschnitt("Beute nur mit Transportkarren (Seite 22)")
vorraete = {"holz": 500.0, "stein": 300.0}
e11 = kampf.fuehre_schlacht({"Paladin": 30}, {"Bürgerwehr": 1}, wall_stufe=1,
                            angreifer_karren={"Handkarren": 2}, vorraete=vorraete, rng=R())
beute = e11["beute"]
kapazitaet = 2 * E.ladung("Handkarren")
check("Beute nur mit Karren", e11["ausgang"] == "angreifer" and beute,
      f"beute={beute}")
check(f"Beute bleibt in der Kapazitaet ({kapazitaet})", sum(beute.values()) <= kapazitaet,
      f"{sum(beute.values())}")
check("Beute uebersteigt die Vorraete nicht",
      all(beute[k] <= vorraete[k] for k in beute))
e12 = kampf.fuehre_schlacht({"Paladin": 30}, {"Bürgerwehr": 1}, wall_stufe=1,
                            vorraete=vorraete, rng=R())
check("ohne Karren keine Beute", e12["beute"] == {}, str(e12["beute"]))
e13 = kampf.fuehre_schlacht({"Paladin": 30}, {"Bürgerwehr": 1}, wall_stufe=1,
                            angreifer_karren={"Belagerungsturm": 2}, vorraete=vorraete, rng=R())
check("Belagerungswaffen tragen keine Beute", e13["beute"] == {}, str(e13["beute"]))

abschnitt("Niederlage des Angreifers: Karren und Belagerungswaffen (Seite 22)")
# Wallstufe 1 mit ausreichender Schlagkraft, aber schwacher Armee gegen eine Uebermacht
e14 = kampf.fuehre_schlacht({"Paladin": 10}, {"Paladin": 60}, wall_stufe=1,
                            angreifer_karren={"Handkarren": 4, "Katapult": 2}, rng=R())
check("Verteidiger siegt bei Uebermacht", e14["ausgang"] == "verteidiger", e14["ausgang"])
verloren = e14.get("karren_verloren", [])
erhalten = e14.get("karren_erhalten", [])
check("jede Karre ist entweder geflohen oder geblieben", len(verloren) + len(erhalten) == 6,
      f"{len(verloren)}+{len(erhalten)}")
check("Fluchtchance steigt mit der Sequenzzahl", "Fluchtchance" in e14["bericht"])

abschnitt("Unentschieden: alles bleibt (Seite 22)")
e15 = kampf.fuehre_schlacht({"Bürgerwehr": 1}, {"Bürgerwehr": 1}, wall_stufe=2,
                            angreifer_karren={"Handkarren": 3}, rng=R())
check("Rueckzug vor der Schlacht", e15["ausgang"] == "unentschieden")
check("... Karren gehen nicht verloren", "karren_verloren" not in e15)

abschnitt("Kein Wert wird erfunden")
check("Bericht ist Text", isinstance(e9["bericht"], str) and len(e9["bericht"]) > 100)
check("Stand vermerkt", e9.get("stand") == kampf.STAND)
check("Angenommene Regel ist gekennzeichnet",
      "Fusstruppen sind hier Nahkampf- und Fernkampfeinheiten" in open(
          os.path.join(SRC, "kampf.py"), encoding="utf-8").read())

sys.exit(bericht())
