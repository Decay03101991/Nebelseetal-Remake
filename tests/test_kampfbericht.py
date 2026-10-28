"""Pruefung des Kampfberichts (Paket W2b) gegen das Originalhandbuch (Seiten 20-23).

Prueft die vier neuen Teile: Vorrunde, Mauerschaden, Beute und Bericht fuer den Reiter
'Nachrichten' - sowie die reine Anwendung auf den Spielstand (`spieldaten_anwenden`).

Die Schlacht selbst laeuft weiterhin durch `src/kampf.py`; hier wird NICHTS nachgebaut.
Wo gewuerfelt wird, arbeitet ein festgelegter Zufallsgenerator (oder ein Stub mit festen
Werten), damit die Zahlen nachvollziehbar bleiben.
"""
from __future__ import annotations

import copy
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, befund, check, import_src

ROOT, SRC = import_src()
import kampf
import kampfbericht as KB
import einheiten as E
import gebaeude_wirkung as GW
import spieldaten as S

R = lambda *a: random.Random(20261004)
TEXT = open(os.path.join(SRC, "kampfbericht.py"), encoding="utf-8").read()


class FesterZufall:
    """Stub: liefert vorgegebene Wuerfe der Reihe nach (fuer die Handbuchbeispiele)."""

    def __init__(self, werte):
        self.werte = list(werte)
        self.i = 0

    def randint(self, a, b):
        v = self.werte[self.i % len(self.werte)]
        self.i += 1
        return max(a, min(b, v))


# =========================================================== Vorrunde (Seite 20/21)
abschnitt("Vorrunde - Schlagkraft gegen den Wall")

r = KB.vorrunde(9, 0, 1)
check("Stufe 1: SK 9 erreicht die Schwelle 10 nicht", r["bestanden"] is False)
check("... der Grund nennt die Schwelle", isinstance(r["grund"], str) and "10" in r["grund"],
      r["grund"])
r1 = KB.vorrunde(10, 0, 1)
check("Stufe 1: SK 10 besteht", r1["bestanden"] is True)
check("Schwelle steht als Nennwert 10 in der Rueckgabe",
      r1["schwelle"]["fusstruppen"]["nennwert"] == 10)
check("erforderlich ist genau 10.0", r1["schwelle"]["fusstruppen"]["erforderlich"] == 10.0)
check("Stufe 2: SK 40 besteht", KB.vorrunde(40, 0, 2)["bestanden"] is True)
check("Stufe 2: SK 39 scheitert", KB.vorrunde(39, 0, 2)["bestanden"] is False)
check("Stufe 4: SK 160 besteht", KB.vorrunde(160, 0, 4)["bestanden"] is True)
check("Stufe 4: SK 159 scheitert", KB.vorrunde(159, 0, 4)["bestanden"] is False)
check("Stufen 1-4 fordern KEINE Belagerungswaffen",
      all(s["schwellenwert_belagerungswaffen"] is None for s in S.wallstufen()[:4]))
check("Stufe 10: SK 999 scheitert", KB.vorrunde(999, 1000, 10)["bestanden"] is False)
check("Stufe 10: SK 1000 (Fuss) + 1000 (Belagerung) besteht",
      KB.vorrunde(1000, 1000, 10)["bestanden"] is True)
check("Stufe 10: Schwellenwert Fusstruppen ist 1000",
      KB.vorrunde(1000, 1000, 10)["schwelle"]["fusstruppen"]["nennwert"] == 1000)
check("Stufe 10: Schwellenwert Belagerungswaffen ist 1000",
      KB.vorrunde(1000, 1000, 10)["schwelle"]["belagerungswaffen"]["nennwert"] == 1000)

r5 = KB.vorrunde(250, 0, 5)
check("ab Stufe 5 ist Belagerungskraft noetig: 250/0 scheitert", r5["bestanden"] is False)
check("... der Grund nennt die Belagerungswaffen", "Belagerungswaffen" in r5["grund"],
      r5["grund"])
check("... der Belagerungs-Zweig ist als nicht erreicht vermerkt",
      r5["schwelle"]["belagerungswaffen"]["erreicht"] is False)
check("Stufe 5: 250 Fusstruppen, aber nur 499 Belagerung scheitert",
      KB.vorrunde(250, 499, 5)["bestanden"] is False)
check("Stufe 5: 250 + 500 besteht", KB.vorrunde(250, 500, 5)["bestanden"] is True)

abschnitt("Vorrunde - beschaedigte Mauer verlangt weniger (Seite 21)")
# Handbuchbeispiel: verstaerkte Mauer (7) bei 50 % -> 245 Fusstruppen + 350 Belagerung.
r7 = KB.vorrunde(245, 350, 7, 50)
check("Stufe 7 bei 50 %: 245/350 besteht", r7["bestanden"] is True)
check("Stufe 7 bei 50 %: Faktor ist 0.5", r7["schwelle"]["faktor"] == 0.5)
check("Stufe 7 bei 50 %: erforderlich Fusstruppen ist 245.0",
      r7["schwelle"]["fusstruppen"]["erforderlich"] == 245.0)
check("Stufe 7 bei 50 %: 244 Fusstruppen scheitert", KB.vorrunde(244, 350, 7, 50)["bestanden"] is False)
check("Stufe 7 bei 50 %: 349 Belagerung scheitert", KB.vorrunde(245, 349, 7, 50)["bestanden"] is False)
check("Stufe 7 bei vollem Zustand: 245/350 scheitert", KB.vorrunde(245, 350, 7)["bestanden"] is False)
r2b = KB.vorrunde(10, 0, 2, 25)
check("Stufe 2 bei 25 %: 10 Fusstruppen besteht", r2b["bestanden"] is True)
check("... erforderlich ist 10.0", r2b["schwelle"]["fusstruppen"]["erforderlich"] == 10.0)
check("Stufe 2 bei 0 %: 0/0 besteht", KB.vorrunde(0, 0, 2, 0)["bestanden"] is True)

abschnitt("Vorrunde - kein Wall / unbekannte Stufe")
rn = KB.vorrunde(0, 0, 0)
check("ohne Wall entfaellt die Vorrunde", rn["bestanden"] is True)
check("... der Grund sagt das auch", "Kein Wall" in rn["grund"], rn["grund"])
ru = KB.vorrunde(0, 0, 99)
check("unbekannte Stufe: kein Wert erfunden, Vorrunde bestanden", ru["bestanden"] is True)
check("... der Grund weist auf die fehlende Schwelle hin", "keine Schwelle" in ru["grund"],
      ru["grund"])
check("Wallname Stufe 1 ist aus den Daten (Erdwall)", KB.vorrunde(0, 0, 1)["schwelle"]["wall_name"] == "Erdwall"
      or GW.wall_name(1) == "Erdwall")
check("Wallname Stufe 10 ist aus den Daten (Bollwerk)", GW.wall_name(10) == "Bollwerk")


# =========================================================== Mauerschaden (Seite 21/22)
abschnitt("Mauerschaden - je Waffe einzeln, minus Ausbaustufe")
# Handbuchbeispiel: Katapult (2-13) gegen Mauer Stufe 6, gewuerfelt 8 -> 8-6=2 -> 100 % -> 98 %.
m = KB.mauer_schaden({"Katapult": 1}, 6, 100.0, FesterZufall([8]))
check("Katapult wuerfelt 8, Stufe 6 -> Zustand 98 %", m["mauer_zustand_prozent"] == 98.0)
check("... der Schaden betraegt 2", m["schaden_gesamt"] == 2)
check("... die Waffe wird einzeln gefuehrt: Wurf 8, Rest 2",
      m["je_waffe"]["Katapult"]["wuerfe"] == [8] and m["je_waffe"]["Katapult"]["rest"] == [2])
check("... die Waffensumme stimmt mit den Restwerten ueberein",
      m["je_waffe"]["Katapult"]["schaden"] == sum(m["je_waffe"]["Katapult"]["rest"]))
m2 = KB.mauer_schaden({"Katapult": 2}, 6, 100.0, FesterZufall([8, 5]))
check("zweites Katapult wuerfelt 5 -> 5-6<0 -> nur 2 Schaden gesamt", m2["schaden_gesamt"] == 2)
check("... die Restwerte sind [2, 0]", m2["je_waffe"]["Katapult"]["rest"] == [2, 0])
m3 = KB.mauer_schaden({"Katapult": 1}, 7, 100.0, FesterZufall([3]))
check("Wurf unter der Ausbaustufe -> kein Schaden", m3["schaden_gesamt"] == 0)
check("... der Zustand bleibt 100 %", m3["mauer_zustand_prozent"] == 100.0)
m4 = KB.mauer_schaden({"Katapult": 1}, 6, 5.0, FesterZufall([13]))
check("der Zustand faellt nie unter 0 %", m4["mauer_zustand_prozent"] == 0.0)
m5 = KB.mauer_schaden({"Belagerungsturm": 3}, 1, 100.0, FesterZufall([18]))
check("Belagerungsturm (Schaden 0-0) bricht keine Mauer", m5["schaden_gesamt"] == 0)
check("... Zustand bleibt 100 %", m5["mauer_zustand_prozent"] == 100.0)
m6 = KB.mauer_schaden({}, 4, 100.0, FesterZufall([5]))
check("ohne Belagerungswaffen kein Mauerschaden", m6["schaden_gesamt"] == 0 and m6["je_waffe"] == {})
m7 = KB.mauer_schaden({"Katapult": 1}, 6, 80.0, FesterZufall([8]))
check("der Ausgangszustand wird als vorher_prozent zurueckgegeben", m7["vorher_prozent"] == 80.0)
check("... der neue Zustand ist 78 %", m7["mauer_zustand_prozent"] == 78.0)
m8 = KB.mauer_schaden({"Katapult": 1, "Balliste": 1}, 6, 100.0, FesterZufall([13, 10]))
check("mehrere Waffenarten summieren sich (7+4=11)", m8["schaden_gesamt"] == 11)
check("... der Zustand ist 89 %", m8["mauer_zustand_prozent"] == 89.0)
m9 = KB.mauer_schaden({"Katapult": 5}, 6, 100.0, R())
check("mit echtem Zufall bleibt der Schaden im Bereich (max 7 je Treffer)",
      0 <= m9["schaden_gesamt"] <= 5 * 7, f"{m9['schaden_gesamt']}")
check("... und der Zustand ist 100 % minus Schaden",
      m9["mauer_zustand_prozent"] == max(0.0, 100.0 - m9["schaden_gesamt"]))
m10 = KB.mauer_schaden({"Unbekannte Waffe": 2}, 6, 100.0, FesterZufall([5, 5]))
check("unbekannte Waffe: kein Wert erfunden, kein Schaden", m10["schaden_gesamt"] == 0)
m11 = KB.mauer_schaden({"Katapult": 0}, 6, 100.0, FesterZufall([8]))
check("Anzahl 0 -> kein Wurf", m11["je_waffe"]["Katapult"]["anzahl"] == 0
      and m11["je_waffe"]["Katapult"]["schaden"] == 0)
m12 = KB.mauer_schaden({"Katapult": -3}, 6, 100.0, FesterZufall([8]))
check("negative Anzahl wird auf 0 begrenzt", m12["je_waffe"]["Katapult"]["anzahl"] == 0)


# =========================================================== Beute (Seite 22/23)
abschnitt("Beute - nur was die Karren tragen")
vorraete = {"holz": 500.0, "stein": 300.0}
b = KB.beute({"Handkarren": 2}, vorraete)
check("2 Handkarren (2x40) laden anteilig: holz 50, stein 30",
      b == {"holz": 50, "stein": 30}, str(b))
check("... die Beute fuellt die Kapazitaet genau (80)", sum(b.values()) == 80)
check("die Beute uebersteigt nie die Kapazitaet",
      sum(KB.beute({"Einspänner": 1}, {"holz": 1000}).values()) <= E.ladung("Einspänner"))
b2 = KB.beute({"Handkarren": 2}, vorraete)
check("die Beute uebersteigt nie den Vorrat je Rohstoff",
      all(b2[k] <= vorraete[k] for k in b2))
check("ohne Karren keine Beute", KB.beute({"Paladin": 10}, vorraete) == {})
check("Belagerungswaffen tragen keine Beute",
      KB.beute({"Belagerungsturm": 3}, vorraete) == {})
check("ohne Vorrat keine Beute", KB.beute({"Handkarren": 2}, {}) == {})
check("mehr Platz als Vorrat -> der ganze Vorrat wird genommen",
      KB.beute({"Handkarren": 10}, {"holz": 50}) == {"holz": 50})
check("Katapulte zaehlen nicht zur Kapazitaet: 1 Handkarren -> 40",
      KB.beute({"Handkarren": 1, "Katapult": 5}, {"holz": 1000}) == {"holz": 40})
check("ein einziger Rohstoff wird exakt begrenzt",
      KB.beute({"Handkarren": 1}, {"holz": 1000}) == {"holz": 40})
check("negative Vorraete werden ignoriert",
      KB.beute({"Handkarren": 1}, {"holz": -5, "stein": 10}) == {"stein": 10})


# =========================================================== Bericht (Nachrichten)
abschnitt("Bericht fuer den Reiter 'Nachrichten'")
sieghtml = kampf.fuehre_schlacht({"Paladin": 30}, {"Bürgerwehr": 3}, wall_stufe=1,
                                 angreifer_karren={"Handkarren": 2}, vorraete=vorraete, rng=R())
bw = KB.bericht(sieghtml)
check("der Bericht hat den Typ 'kampf'", bw["typ"] == "kampf")
check("der Bericht hat einen Titel", isinstance(bw["titel"], str) and bw["titel"].startswith("Schlachtbericht"))
check("der Titel nennt den Angreifersieg", "Angreifer siegt" in bw["titel"], bw["titel"])
check("der Bericht hat Zeilen (>=3)", isinstance(bw["zeilen"], list) and len(bw["zeilen"]) >= 3,
      str(len(bw["zeilen"])))
check("alle Zeilen sind Text", all(isinstance(z, str) for z in bw["zeilen"]))
zusammen = "\n".join(bw["zeilen"])
check("der Ausgang steht in den Zeilen", "Ausgang:" in zusammen)
check("die Verluste des Angreifers stehen darin", "Verluste Angreifer:" in zusammen)
check("die Beute steht darin", "Beute:" in zusammen)

vorrueckzug = kampf.fuehre_schlacht({"Bürgerwehr": 1}, {"Bürgerwehr": 1}, wall_stufe=1, rng=R())
bu = KB.bericht(vorrueckzug)
check("gescheiterte Vorrunde: Titel ist 'Unentschieden'", "Unentschieden" in bu["titel"], bu["titel"])
check("... die Berichtszeilen sind trotzdem gefuellt", len(bu["zeilen"]) >= 2)
bl = KB.bericht({})
check("leeres Ergebnis stuerzt nicht ab", bl["typ"] == "kampf" and bool(bl["titel"]))
check("... ohne Beute steht 'keine Beute' darin", any("keine" in z for z in bl["zeilen"]))


# =========================================================== Spieldaten anwenden
abschnitt("Spieldaten anwenden - reine Funktion")
zustand = {"ressourcen": {"holz": 100, "stein": 100}, "einheiten": {"Paladin": 30, "Handkarren": 4}}
kopie = copy.deepcopy(zustand)
synthetisch = {"ausgang": "angreifer", "beute": {"holz": 50, "stein": 30},
               "verluste_angreifer": {"Paladin": 2}, "geraete_verloren": ["Handkarren"],
               "mauer_zustand": 96.0}
neu = KB.spieldaten_anwenden(zustand, synthetisch)
check("Beute erhoeht die Rohstoffe genau um die Beute",
      neu["ressourcen"]["holz"] - 100 == 50 and neu["ressourcen"]["stein"] - 100 == 30,
      str(neu["ressourcen"]))
check("Verluste gehen von den Einheiten ab (Paladin 30 -> 28)",
      neu["einheiten"]["Paladin"] == 28)
check("zurueckgelassene Geraete gehen ebenfalls ab (Handkarren 4 -> 3)",
      neu["einheiten"]["Handkarren"] == 3)
check("der Mauerzustand wird uebernommen", neu["wall_zustand_prozent"] == 96.0)
check("der Eingabestand wird nicht veraendert", kopie == zustand, str(zustand))
check("... auch die verschachtelten Rohstoffe nicht", zustand["ressourcen"] == {"holz": 100, "stein": 100})
check("es kommt ein NEUES dict zurueck", neu is not zustand)
check("Einheiten fallen nie unter 0",
      KB.spieldaten_anwenden({"einheiten": {"Bürgerwehr": 1}},
                             {"verluste_angreifer": {"Bürgerwehr": 5}})["einheiten"]["Bürgerwehr"] == 0)
leer = KB.spieldaten_anwenden({}, {})
check("leerer Stand bekommt leere Felder", leer["ressourcen"] == {} and leer["einheiten"] == {})

abschnitt("Voller Kampf durch src/kampf.py -> Bericht + Stand")
check("der echte Kampf geht an den Angreifer", sieghtml["ausgang"] == "angreifer", sieghtml["ausgang"])
voll = KB.spieldaten_anwenden(zustand, sieghtml)
beute_aus_kampf = sieghtml["beute"]
check("die Rohstoffe aendern sich genau um die Kampfbeute",
      voll["ressourcen"]["holz"] - 100 == beute_aus_kampf.get("holz", 0)
      and voll["ressourcen"]["stein"] - 100 == beute_aus_kampf.get("stein", 0),
      f"{beute_aus_kampf}")
check("die Einheiten aendern sich genau um die Verluste des Angreifers",
      voll["einheiten"]["Paladin"] == 30 - sieghtml["verluste_angreifer"].get("Paladin", 0))
check("die Beute aus kampf.py stimmt mit kampfbericht.beute ueberein",
      beute_aus_kampf == KB.beute({"Handkarren": 2}, vorraete), f"{beute_aus_kampf}")
check("der Bericht eines echten Kampfes hat Titel und Zeilen",
      bool(bw["titel"]) and len(bw["zeilen"]) >= 3)
kampf_mit_mauer = kampf.fuehre_schlacht({"Paladin": 10}, {"Bürgerwehr": 2}, wall_stufe=1,
                                        angreifer_karren={"Katapult": 2}, rng=R())
bm = KB.bericht(kampf_mit_mauer)
check("Mauerschaden erscheint im Bericht", any("Mauerzustand" in z for z in bm["zeilen"]))


# =========================================================== Luecken / keine Erfindung
abschnitt("Offene Luecken und 'kein Wert erfunden'")
luecken = KB.offene_luecken()
check("offene_luecken liefert eine nicht-leere Liste", isinstance(luecken, dict) and len(luecken) >= 5)
check("alle Luecken sind Text", all(isinstance(k, str) and isinstance(v, str) for k, v in luecken.items()))
check("die Fluchtformel-Luecke ist benannt", "flucht_formel" in luecken)
check("die Beute-Verteilungs-Luecke ist benannt", "beute_verteilung" in luecken)
luecken["flucht_formel"] = "geaendert"
check("offene_luecken gibt jedes Mal eine frische Kopie", KB.offene_luecken()["flucht_formel"] != "geaendert")
check("Stufen 1-4 nennen keine Belagerungsschwelle (keine erfunden)",
      GW.wall_schwelle(4)["belagerungswaffen"] is None)
check("Stufe 5 nennt 500 (aus den Daten)", GW.wall_schwelle(5)["belagerungswaffen"] == 500)
check("Belagerungsturm hat laut Daten Mauerschaden (0,0)",
      E.mauer_schaden("Belagerungsturm") == (0, 0))
check("der Code kennzeichnet Annahmen mit ANNAHME", "ANNAHME" in TEXT)


# =========================================================== Zu wenig SK -> keine Beute
abschnitt("Zu wenig Schlagkraft -> Vorrunde scheitert, keine Beute")
check("direkte Vorrunde scheitert (SK 1 < 10)", KB.vorrunde(1, 0, 1)["bestanden"] is False)
kein_angriff = kampf.fuehre_schlacht({"Bürgerwehr": 1}, {"Bürgerwehr": 1}, wall_stufe=1,
                                     angreifer_karren={"Handkarren": 2}, vorraete=vorraete, rng=R())
check("der Kampf endet unentschieden (Rueckzug)", kein_angriff["ausgang"] == "unentschieden",
      kein_angriff["ausgang"])
check("... es wird KEINE Beute genommen", kein_angriff["beute"] == {}, str(kein_angriff["beute"]))
stand_danach = KB.spieldaten_anwenden(zustand, kein_angriff)
check("... der Spielstand behaelt alle Rohstoffe",
      stand_danach["ressourcen"] == {"holz": 100, "stein": 100}, str(stand_danach["ressourcen"]))
check("... der Angreifer verliert auch keine Einheiten",
      stand_danach["einheiten"] == zustand["einheiten"], str(stand_danach["einheiten"]))
check("... der Bericht nennt trotzdem einen Ausgang",
      "Ausgang:" in "\n".join(KB.bericht(kein_angriff)["zeilen"]))


sys.exit(bericht())
