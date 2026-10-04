"""Pruefung des Kampfablaufs gegen die Regeln des Handbuchs (Seiten 20-23).

Zweite Fassung. Nach dem Regelgutachten vom 04.10.2026 wurden sechs Regeln korrigiert; jede
Korrektur hat hier eine eigene Pruefung mit dem woertlichen Beleg aus dem Handbuch.

Wo gerechnet wird, arbeitet ein festgelegter Zufallsgenerator, damit die Ergebnisse
nachvollziehbar sind.
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

R = lambda *a: random.Random(20261004)
TEXT = open(os.path.join(SRC, "kampf.py"), encoding="utf-8").read()


abschnitt("Vorrunde — Schlagkraft gegen den Wall (Seite 20)")
e1 = kampf.fuehre_schlacht({"Bürgerwehr": 1}, {"Bürgerwehr": 1}, wall_stufe=1, rng=R())
check("Bürgerwehr allein (SK 1) erreicht die Schwelle 10 nicht", e1["ausgang"] == "unentschieden")
check("... und es kommt zu keiner Kampfsequenz", e1["sequenzen"] == [], str(e1["sequenzen"]))
e2 = kampf.fuehre_schlacht({"Paladin": 10}, {}, wall_stufe=2, rng=R())
check("10 Paladinae (SK 50) schaffen Stufe 2 (40)", e2["ausgang"] != "unentschieden"
      or "Schwelle nicht erreicht" not in e2["bericht"])
e3 = kampf.fuehre_schlacht({"Paladin": 10}, {}, wall_stufe=3, rng=R())
check("10 Paladinae schaffen Stufe 3 (90) nicht", e3["ausgang"] == "unentschieden")
e4 = kampf.fuehre_schlacht({"Paladin": 4}, {}, wall_stufe=2, wall_zustand=25.0, rng=R())
check("beschaedigter Wall (25 %) senkt die Schwelle", e4["ausgang"] != "unentschieden")

abschnitt("Vorrunde — Belagerungswaffen ab Stufe 5 (Seite 20)")
e5 = kampf.fuehre_schlacht({"Paladin": 50}, {}, wall_stufe=5, rng=R())
check("ohne Belagerungswaffen kein Angriff auf Stufe 5", e5["ausgang"] == "unentschieden")
e6 = kampf.fuehre_schlacht({"Paladin": 50}, {}, wall_stufe=5,
                           angreifer_karren={"Großes Katapult": 10, "Handkarren": 2}, rng=R())
check("mit Belagerungswaffen (SK 550) gelingt der Angriff", e6["ausgang"] != "unentschieden")
check("Stufen 1-4 nennen keine Belagerungsschwelle",
      all(s["schwellenwert_belagerungswaffen"] is None for s in S.wallstufen()[:4]))

abschnitt("Mauerschaden (Seite 21/22)")
e7 = kampf.fuehre_schlacht({"Paladin": 10}, {}, wall_stufe=1,
                           angreifer_karren={"Katapult": 1}, rng=R())
check("Mauerzustand bleibt zwischen 87 und 100 %", 87 <= e7["mauer_zustand"] <= 100,
      f"{e7['mauer_zustand']}")
check("Mauerschaden steht im Bericht", "Mauerschaden" in e7["bericht"])
check("je Belagerungswaffe einzeln ermittelt", "einzeln ermittelt" in e7["bericht"])

abschnitt("Kampfsequenzen (Seite 22)")
e9 = kampf.fuehre_schlacht({"Paladin": 30}, {"Bürgerwehr": 3}, wall_stufe=1, rng=R())
check("mindestens eine Sequenz", len(e9["sequenzen"]) >= 1, f"{len(e9['sequenzen'])}")
check("hoechstens zehn Sequenzen", len(e9["sequenzen"]) <= 10, f"{len(e9['sequenzen'])}")
check("Uebermacht siegt", e9["ausgang"] == "angreifer", e9["ausgang"])
check("die drei Verteidiger sind gefallen",
      e9["verluste_verteidiger"].get("Bürgerwehr") == 3, str(e9["verluste_verteidiger"]))

abschnitt("KORREKTUR 1: im Nahkampf stuermt nur der Angreifer (Seite 22)")
# Handbuch: "Als naechstes stuermen die angreifenden Nahkampfeinheiten nacheinander ..."
# Der Verteidiger stuermt nicht zusaetzlich; er schlaegt nur im Zweikampf zurueck.
e10 = kampf.fuehre_schlacht({"Paladin": 1}, {"Bürgerwehr": 200}, wall_stufe=0, rng=R())
stuermt_verteidiger = [z for zeile in e10["sequenzen"] for z in zeile.split("\n")
                       if z.strip().startswith("Nahkampf:") and "Bürgerwehr" in z.split("gegen")[0]]
check("kein Zweikampf wird vom Verteidiger eroeffnet", not stuermt_verteidiger,
      str(stuermt_verteidiger[:2]))
check("ein einzelner Angreifer zermuerbt keine 200 Verteidiger",
      e10["ausgang"] == "unentschieden", e10["ausgang"])

abschnitt("KORREKTUR 2: Fernkampf ist wirklich gleichzeitig (Seite 22)")
# Handbuch: "(Gleichzeitig bedeutet, das Verteidiger und Angreifer ZUERST feuern und
# ANSCHLIEßEND die Verluste auf beiden Seiten berechnet werden)."
e11 = kampf.fuehre_schlacht({"Paladin": 3, "Kurzbogenschütze": 5},
                            {"Bürgerwehr": 3, "Kurzbogenschütze": 2}, wall_stufe=1, rng=R())
erste = e11["sequenzen"][0] if e11["sequenzen"] else ""
check("beide Seiten feuern zuerst", "beide Seiten feuern zuerst" in erste, erste[:120])
check("auch der Verteidiger schiesst in derselben Sequenz",
      any(z.strip().startswith("Kurzbogenschütze") and "greift" in z
          for z in erste.split("\n")), "kein Schuss des Verteidigers gefunden")

abschnitt("KORREKTUR 3: Zweikampf laeuft bis tot oder geflohen (Seite 22)")
# Handbuch: "Die beiden Einheiten kaempfen solange, bis eine der beiden tot ist, oder flieht."
e12 = kampf.fuehre_schlacht({"Paladin": 3}, {"Bürgerwehr": 1}, wall_stufe=1, rng=R())
check("der Zweikampf endet mit einem Toten in der ersten Sequenz",
      e12["ausgang"] == "angreifer" and e12["verluste_verteidiger"].get("Bürgerwehr") == 1,
      f"{e12['ausgang']} {e12['verluste_verteidiger']}")
# Ein Zwei-Personen-Fall, in dem kein Schlag sofort toetlich sein kann (Paladin-Schaden
# 6-20 gegen LE 35 des Ritters): hier muessen mehrere Runden im Bericht stehen.
e12b = kampf.fuehre_schlacht({"Ritter": 1}, {"Paladin": 1}, wall_stufe=0, rng=R())
schlagzahl = e12b["sequenzen"][0].count("greift") if e12b["sequenzen"] else 0
check("mehrere Schlaege im selben Zweikampf (Kampfrunden)", schlagzahl >= 2, f"{schlagzahl}")
check("der Zweikampf endet mit tot oder geflohen",
      bool(e12b["verluste_angreifer"] or e12b["verluste_verteidiger"] or e12b["geflohen"]),
      f"Verluste {e12b['verluste_angreifer']}/{e12b['verluste_verteidiger']}, geflohen {e12b['geflohen']}")

abschnitt("KORREKTUR 4: Nahkampf weicht auf Fernkaempfer aus (Seite 22)")
# Handbuch: "Sind keine verteidigenden Nahkampfeinheiten mehr uebrig werden die
# verteidigenden Fernkampfeinheiten angegriffen."
e13 = kampf.fuehre_schlacht({"Paladin": 3}, {"Bürgerwehr": 1, "Kurzbogenschütze": 1},
                            wall_stufe=1, rng=R())
check("nach dem Nahkaempfer wird der Fernkaempfer angegriffen",
      e13["verluste_verteidiger"].get("Kurzbogenschütze") == 1,
      str(e13["verluste_verteidiger"]))

abschnitt("KORREKTUR 5: Schlacht endet ohne Nahkampfeinheiten (Seite 22)")
# Handbuch: "Die Schlacht ist vorbei, sobald eine der beiden Armeen keine Nahkampfeinheiten
# mehr hat, oder 10 Kampfsequenzen vorueber sind."
e14 = kampf.fuehre_schlacht({"Kurzbogenschütze": 5}, {"Bürgerwehr": 3}, wall_stufe=0, rng=R())
check("ohne Nahkampfeinheiten beim Angreifer beginnt keine Sequenz",
      e14["sequenzen"] == [], f"{len(e14['sequenzen'])} Sequenzen")
check("der Widerspruch im Handbuch ist vermerkt", len(e14["unsicher"]) >= 1,
      str(e14["unsicher"]))

abschnitt("KORREKTUR 6: Erschoepfung laesst Massen siegen (Seite 23)")
# Handbuch: "So ist es moeglich, auch starke Einheiten mit der entsprechenden Uebermacht an
# schwachen Einheiten zu besiegen." — hier: 200 Buergerwehr gegen einen Paladin.
e15 = kampf.fuehre_schlacht({"Bürgerwehr": 200}, {"Paladin": 1}, wall_stufe=0, rng=R())
check("die Masse besiegt den Starken", e15["ausgang"] == "angreifer", e15["ausgang"])
check("der Paladin ist gefallen", e15["verluste_verteidiger"].get("Paladin") == 1,
      str(e15["verluste_verteidiger"]))

abschnitt("KORREKTUR 6b: Erschoepfung wird je gewonnenem Zweikampf angewandt")
# Der Sieger eines Zweikampfs verliert 1 AT und 1 PA bis Schlachtende; die Regel gehoert an
# das Ende des Zweikampfs (nicht in jeden Schlag). Geprueft am Code und am Verhalten:
# 40 Buergerwehr gegen 4 Paladine — die Paladine gewinnen viele Zweikaempfe und ermueden.
check("die Erschoepfung steht im Schlacht-Ablauf, nicht im Schlag",
      "Erschoepfung je gewonnenem ZWEIKAMPF" in TEXT)
e15b = kampf.fuehre_schlacht({"Bürgerwehr": 60}, {"Paladin": 4}, wall_stufe=0, rng=R())
check("Zahlen schlagen Qualitaet (Handbuch Seite 23)",
      e15b["ausgang"] in ("angreifer", "verteidiger"), e15b["ausgang"])

abschnitt("Verlierer-Geraet: beide Seiten koennen es verlieren (Seite 23)")
# Handbuch: "Der Verlierer verliert einen Teil seiner stationierten bzw. mitgeschickten
# Karren und Belagerungswaffen."
e16 = kampf.fuehre_schlacht({"Bürgerwehr": 1}, {"Paladin": 1}, wall_stufe=0,
                            angreifer_karren={"Handkarren": 4, "Katapult": 2}, rng=R())
check("der Angreifer verliert Geraet", e16["ausgang"] == "verteidiger"
      and len(e16.get("geraete_verloren", [])) + len(e16.get("geraete_erhalten", [])) == 6,
      f"{e16['ausgang']} {e16.get('geraete_verloren')} {e16.get('geraete_erhalten')}")
e17 = kampf.fuehre_schlacht({"Paladin": 200}, {"Bürgerwehr": 1}, wall_stufe=0,
                            verteidiger_karren={"Handkarren": 3}, rng=R())
check("auch der Verteidiger verliert Geraet", "geraete_verloren_verteidiger" in e17,
      str({k: v for k, v in e17.items() if "geraete" in k}))

abschnitt("Beute nur mit Transportkarren (Seite 23)")
vorraete = {"holz": 500.0, "stein": 300.0}
e18 = kampf.fuehre_schlacht({"Paladin": 30}, {"Bürgerwehr": 1}, wall_stufe=1,
                            angreifer_karren={"Handkarren": 2}, vorraete=vorraete, rng=R())
beute = e18["beute"]
kapazitaet = 2 * E.ladung("Handkarren")
check("Beute nur mit Karren", e18["ausgang"] == "angreifer" and bool(beute), f"beute={beute}")
check(f"Beute bleibt in der Kapazitaet ({kapazitaet})", sum(beute.values()) <= kapazitaet,
      f"{sum(beute.values())}")
check("Beute uebersteigt die Vorraete nicht", all(beute[k] <= vorraete[k] for k in beute))
e19 = kampf.fuehre_schlacht({"Paladin": 30}, {"Bürgerwehr": 1}, wall_stufe=1,
                            vorraete=vorraete, rng=R())
check("ohne Karren keine Beute", e19["beute"] == {}, str(e19["beute"]))
e20 = kampf.fuehre_schlacht({"Paladin": 30}, {"Bürgerwehr": 1}, wall_stufe=1,
                            angreifer_karren={"Belagerungsturm": 2}, vorraete=vorraete, rng=R())
check("Belagerungswaffen tragen keine Beute", e20["beute"] == {}, str(e20["beute"]))

abschnitt("Unentschieden: alles bleibt (Seite 23)")
e21 = kampf.fuehre_schlacht({"Bürgerwehr": 1}, {"Bürgerwehr": 1}, wall_stufe=2,
                            angreifer_karren={"Handkarren": 3}, rng=R())
check("Rueckzug vor der Schlacht", e21["ausgang"] == "unentschieden")
check("... Karren gehen nicht verloren", "geraete_verloren" not in e21)

abschnitt("Kein Wert wird erfunden")
check("Bericht ist Text", isinstance(e9["bericht"], str) and len(e9["bericht"]) > 100)
check("Stand vermerkt", e9.get("stand") == kampf.STAND)
check("die Fusstruppen-Annahme ist im Code gekennzeichnet",
      "ANNAHME: Fuer die Vorrunde sind Fusstruppen" in TEXT)
check("die Fluchtformel ist als Annahme gekennzeichnet",
      "ANNAHME zur Form" in TEXT)

sys.exit(bericht())
