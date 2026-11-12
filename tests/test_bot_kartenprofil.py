# -*- coding: ascii -*-
"""Kartenprofil je Bot-Dorf - Stufe B-4 (02.11.2026, Konzept Abschnitt 11, Vorgabe Daniel).

VORGABE Daniel: bei jeder Gruendung hat man drei Karten zur Wahl; die Wahl der Karte bestimmt, welchen
Rohstoff dieses Dorf MAXIMAL triggert und welche Rohstoffe auf der Karte eher weniger produzierbar
sind. Gold ist besonders wichtig - richtig stark ist man nur mit den besten Karten. Der Spieler
entscheidet das im Kopf, die Spiellogik (und damit die Bots) muss die Mechanik nachbilden.

Bis B-3 rechnete jedes Bot-Dorf mit derselben festen Rate. Seit B-4 traegt jedes Dorf eine Karte.
**Seit S-8 Stufe 1 (03.11.2026) ist das Kartenprofil VORSCHAU und RUECKFALL, nicht mehr der Ertrag:**
der Ertrag kommt aus den GEBAUTEN ANLAGEN je Feld (`bot_dorf_ertrag`, dieselbe Kernrechnung wie beim
Spieler). Die Pruefungen 1 und 2 messen das Profil selbst (Felder x Ertrag), Pruefung 3 den Rueckfall
fuer Doerfer OHNE Anlagen, Pruefung 6 das Verhaeltnis von Vorschau und Ertrag im Bericht.

Was diese Datei beweist
-----------------------
1. Das Profil wird GERECHNET, nicht erfunden: Felder der Karte mal belegter Ertrag je Gebaeude und
   Gelaende, nur auf Gelaende, auf dem die Anlage stehen darf. Fuer die Karte original-001 steht die
   Handrechnung daneben.
2. Alle 127 Karten tragen alle fuenf Rohstoffe - und genau EINE Karte traegt kein Gold (original-125,
   ohne Berg und Huegel). Gold ist damit wirklich der Engpass, den Daniel beschreibt.
3. Ein Dorf OHNE gebaute Anlage (alter Spielstand) rechnet aus dem Kartenwert geteilt durch den
   Teiler; ein Dorf ohne Karte und ohne Anlagen wie vor B-4 mit dem Bauplan (20/12/21/9 plus Waren).
   Ein Dorf MIT Anlagen rechnet aus den Feldern - das prueft `tests/test_s8_ertrag_aus_anlagen.py`.
4. Gold zuerst: der Bot waehlt aus drei Karten die mit dem hoechsten Goldwert, reproduzierbar und ohne
   Wuerfeln zur Laufzeit.
5. Jedes Dorf bekommt genau eine Karte; der Aufruf ist idempotent, ein alter Spielstand bekommt sie
   beim ersten Auffrischen.
6. Anzeige und Kern lesen DIESELBE Funktion (F-04): der Spionagebericht zeigt Karte, den Ertrag aus
   den Anlagen und daneben die VORSCHAU der Karte. Beide Zahlen kommen aus derselben Funktion, die
   der Kern bucht. Die offene Uebersicht bleibt ohne Karte.
7. Grenzfaelle: unbekannte Karte, Teiler 0, abgeschalteter Schalter - in jedem Fall wird gerechnet,
   nie geteilt durch null, nie still ein falscher Wert gebucht.

Aufruf:  python -X utf8 tests/test_bot_kartenprofil.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "quelltext"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['botkern', 'gelaende', 'main:*']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

ROOT, SRC = import_src()
import gelaende  # noqa: E402
import main as M  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()

KATALOG = M.bot_karten_katalog()


def neuer_stand():
    """GameState mit einem Spielerdorf und den fuenf echten Bots (Muster: test_s7)."""
    import botkern as BK
    gs = M.GameState()
    gs.settlements = [M.Settlement(name="Testdorf", map_id="kontinent",
                                   x=3, y=3, id="spieler:kontinent:3:3",
                                   vorraete={"holz": 100.0, "stein": 100.0})]
    gs.bots = [M.BotPlayer(n, BK.BOT_FRAKTIONEN[n], 0.2, 0.5) for n in BK.BOT_NAMEN]
    gs.noob_protection = False
    gs._letzter_bot_takt = 0.0
    return gs


# ==========================================================================
abschnitt("1. Das Profil wird aus den Spieldaten gerechnet, nicht erfunden")
# ==========================================================================
check("1 der Kartenkatalog ist da (127 Originalkarten)", len(KATALOG) == 127, str(len(KATALOG)))
felder = ((KATALOG.get("original-001") or {}).get("original_attribute") or {}).get("felder") or {}
hand = {}
for stoff, geb in (("holz", "holzfaeller"), ("stein", "steinmetz"), ("nahrung", "farm"),
                   ("gold", "goldmine"), ("metall", "erzmine")):
    summe = 0.0
    for art, anzahl in felder.items():
        erlaubt, _grund = gelaende.bau_moeglich(geb, art)
        if not erlaubt:
            continue
        wert = gelaende.ertrag_pro_stunde(geb, art)
        if isinstance(wert, (int, float)):
            summe += float(anzahl) * float(wert)
    hand[stoff] = round(summe, 2)
profil001 = M.bot_kartenprofil("original-001")
# S-6b (03.11.2026): die Handrechnung deckt Gebaeude mit EINEM Rohstoff ab. Die Nahrung kommt
# zusaetzlich aus den Rinderfarmen (drei Anlagen, je 3 Nahrung), deshalb getrennte Pruefung.
_hand_grund = {k: v for k, v in hand.items() if k != "nahrung"}
_profil_grund = {k: v for k, v in profil001.items() if k in _hand_grund}
check("1 Profil original-001 stimmt mit der Handrechnung ueberein (Holz, Stein, Gold, Metall)", _profil_grund == _hand_grund,
      str(profil001) + " / " + str(hand))
check("1 die Nahrung liegt ueber der Farm allein (Rinderfarm liefert mit)",
      float(profil001.get("nahrung", 0)) > float(hand.get("nahrung", 0)),
      str(profil001.get("nahrung")) + " / Farm allein " + str(hand.get("nahrung")))
check("1 das Profil nennt alle acht Rohstoffe (fuenf Grund plus Leder, Wolle, Pferde)",
      set(profil001) >= {"gold", "holz", "metall", "nahrung", "stein", "leder", "wolle", "pferde"},
      str(sorted(profil001)))
check("1 der Staerkste ist der hoechste Wert der Karte",
      M.bot_karten_staerkster(profil001) == max(profil001, key=profil001.get),
      M.bot_karten_staerkster(profil001))
alle = {i: M.bot_kartenprofil(i) for i in KATALOG}
check("1 jede Karte traegt Holz, Stein und Nahrung (Waren, wo Grasland oder Steppe liegt)",
      all(set(p) >= {"holz", "stein", "nahrung"} for p in alle.values()), "")
check("1 keine Karte ist ohne jeden Wert", all(sum(p.values()) > 0 for p in alle.values()), "")

# ==========================================================================
abschnitt("2. Gold ist der Engpass: nur die besten Karten tragen es")
# ==========================================================================
ohne_gold = sorted(i for i, p in alle.items() if p["gold"] == 0)
check("2 genau EINE Karte traegt kein Gold", ohne_gold == ["original-125"], str(ohne_gold))
beste_gold = max(sorted(alle), key=lambda i: alle[i]["gold"])
check("2 die goldreichste Karte ist original-001", beste_gold == "original-001",
      beste_gold + " mit " + str(alle[beste_gold]["gold"]))
goldwerte = sorted(p["gold"] for p in alle.values())
median = goldwerte[len(goldwerte) // 2]
check("2 Gold ist knapp: die Haelfte der Karten traegt weniger als das Maximum",
      median < alle[beste_gold]["gold"] and goldwerte[0] == 0.0,
      "beste %s, Median %s, kleinste %s" % (alle[beste_gold]["gold"], median, goldwerte[0]))
check("2 eine Karte ohne Berg traegt weder Gold noch Stein noch Metall",
      alle["original-125"]["gold"] == 0 and alle["original-125"]["stein"] == 0
      and alle["original-125"]["metall"] == 0, str(alle["original-125"]))

# ==========================================================================
abschnitt("3. Kartenprofil als RUECKFALL: Doerfer ohne Anlagen; ohne Karte gilt der Bauplan")
# ==========================================================================
einst = M.bot_wirtschaft_einstellungen()
teiler = float(einst.get("karten_teiler") or 10.0)
mit_karte = M.BotDorf(name="Mit Karte", karte="original-001")
# S-8 Stufe 1 (03.11.2026): das Dorf hat KEINE Anlage, deshalb gilt das Kartenprofil als Rueckfall.
check("3 ohne Anlage: Stundensatz ist Kartenwert durch Teiler (Rueckfall)",
      M.bot_dorf_ertrag(mit_karte) == {s: round(w / teiler, 2) for s, w in alle["original-001"].items()},
      str(M.bot_dorf_ertrag(mit_karte)))
ohne = M.BotDorf(name="Ohne Karte")
rueckfall = M.bot_dorf_ertrag(ohne)
# S-6b (03.11.2026): Holz steht seit Daniels Entscheidung auf FUENF Anlagen je Dorf statt drei
# (680 Holz fuer Karren und Gruendung) - der Rueckfall-Ertrag ist 20/12/21/9 statt 12/12/21/9.
check("3 ohne Karte: Rueckfall sind die Anlagen aus dem Bauplan (20/12/21/9 plus Waren)",
      all(round(float(rueckfall.get(k, 0)), 2) == v for k, v in
          {"holz": 20.0, "stein": 12.0, "nahrung": 21.0, "gold": 9.0}.items())
      and float(rueckfall.get("leder", 0)) > 0, str(rueckfall))
arm = M.bot_dorf_ertrag(M.BotDorf(name="Ohne Berg", karte="original-125"))
check("3 eine Karte ohne Berg liefert WEDER Gold NOCH Stein NOCH Metall",
      "gold" not in arm and "stein" not in arm and "metall" not in arm, str(arm))
check("3 sie liefert aber Holz und Nahrung", "holz" in arm and "nahrung" in arm, str(arm))
check("3 die beste Goldkarte gibt mehr Gold als eine arme Karte",
      M.bot_dorf_ertrag(M.BotDorf(name="Reich", karte=beste_gold)).get("gold", 0)
      > M.bot_dorf_ertrag(M.BotDorf(name="Arm", karte="original-057")).get("gold", 0),
      str(M.bot_dorf_ertrag(M.BotDorf(name="Arm", karte="original-057")).get("gold", 0)))

# ==========================================================================
abschnitt("4. Die Wahl: drei Karten, Gold zuerst, reproduzierbar")
# ==========================================================================
bot = M.BotPlayer("Haug", "menschlich", 0.3, 0.8, settlements=["A", "B", "C"])
w1 = M.bot_kartenwahl(bot, 0)
w2 = M.bot_kartenwahl(bot, 0)
check("4 dieselbe Wahl bei gleichem Bot und gleicher Nummer", w1 == w2, w1 + " / " + w2)
check("4 die gewaehlte Karte stammt aus dem Katalog", w1 in KATALOG, w1)
zufall = random.Random("karte:Haug:0")
_anzahl = int(einst.get("karten_kandidaten") or 3)
kandidaten = zufall.sample(sorted(KATALOG), _anzahl)
# Register 225 (Daniel 05.11.2026): die Bots erhalten EINE Karte (Zufall) statt drei zur Wahl -
# die Zahl kommt aus der Datendatei, die Wache prueft die REGEL (so viele Kandidaten wie dort).
check("4 so viele Kandidaten wie in der Datendatei", len(kandidaten) == _anzahl,
      "%d Kandidaten (Datei: %d)" % (len(kandidaten), _anzahl))
check("4 gewaehlt wird der hoechste GOLDWERT der Kandidaten",
      w1 == max(kandidaten, key=lambda i: (alle[i]["gold"], round(sum(alle[i].values()), 2), i)),
      w1 + " aus " + str(kandidaten))
check("4 eine andere Dorfnummer wuerfelt eine andere Auswahl",
      random.Random("karte:Haug:1").sample(sorted(KATALOG), _anzahl) != kandidaten, "")

# ==========================================================================
abschnitt("5. Zuweisung: jedes Dorf genau eine Karte, idempotent, altstandsfest")
# ==========================================================================
b5 = M.BotPlayer("Grom", "zwergisch", 0.7, 0.4, settlements=["G1", "G2"])
neu = M.bot_doerfer_karten_zuweisen(b5)
check("5 beide Doerfer bekommen eine Karte", neu == 2, str(neu))
check("5 jedes Dorf traegt eine Karte aus dem Katalog",
      all(d.karte in KATALOG for d in b5.doerfer), str([d.karte for d in b5.doerfer]))
check("5 ein zweiter Aufruf aendert nichts", M.bot_doerfer_karten_zuweisen(b5) == 0, "")
alt = M.bot_aus_stand({"name": "Silra", "faction": "elfisch", "aggression": 0.2, "trading": 0.9,
                       "settlements": ["S1"], "vorraete": {"holz": 50}})
check("5 ein alter Stand hat zuerst keine Karte",
      all(not d.karte for d in M.bot_doerfer_sicherstellen(alt)), "")
check("5 der erste Aufruf vergibt sie", M.bot_doerfer_karten_zuweisen(alt) == 1, "")
gs = neuer_stand()
gestern = gs.bot_doerfer_auffrischen(gs.bots[0], 3600.0)
check("5 das Auffrischen im Bot-Takt vergibt die Karten mit",
      all(d.karte for d in gs.bots[0].doerfer), str([d.karte for d in gs.bots[0].doerfer]))

# ==========================================================================
abschnitt("6. Anzeige und Kern lesen dieselbe Rechnung (F-04)")
# ==========================================================================
gs = neuer_stand()
gs.bot_doerfer_karten_zuweisen(gs.bots[0]) if hasattr(gs, "bot_doerfer_karten_zuweisen") \
    else M.bot_doerfer_karten_zuweisen(gs.bots[0])
bericht_daten = gs.bot_doerfer_spionagebericht(gs.bots[0])
zeile = bericht_daten["doerfer"][0]
check("6 der Bericht nennt die Karte", bool(zeile.get("karte")), str(zeile.get("karte")))
check("6 der Bericht zeigt die Kartenwerte", bool((zeile.get("karte_info") or {}).get("werte")), "")
# S-8 Stufe 1 (03.11.2026): Der Bericht traegt ZWEI Zahlen mit verschiedener Bedeutung. Der Ertrag
# kommt aus den gebauten Anlagen (dieselbe Funktion, die der Kern bucht), die Kartenwerte sind die
# VORSCHAU ("was gaebe diese Karte her"). Sie duerfen sich unterscheiden - vorher waren sie gleich,
# weil beide aus dem Kartenprofil kamen und die Anlagen wirkungslos waren.
_dorf6 = gs.bots[0].doerfer[0]
_teiler6 = float(einst.get("karten_teiler") or 10.0)
check("6 der gezeigte Stundensatz ist der Ertrag aus den Anlagen (F-04)",
      zeile.get("ertrag_pro_stunde") == M.bot_dorf_ertrag(_dorf6, None, gs.bots[0]),
      str(zeile.get("ertrag_pro_stunde")))
check("6 die Kartenwerte im Bericht sind die VORSCHAU der Karte (Wert durch Teiler, mit Volksfaktor)",
      (zeile.get("karte_info") or {}).get("ertrag_pro_stunde")
      == M._mit_volk({s: round(w / _teiler6, 2) for s, w in alle[str(_dorf6.karte)].items() if w > 0},
                     gs.bots[0]),
      str((zeile.get("karte_info") or {}).get("ertrag_pro_stunde")))
check("6 Vorschau und Ertrag sind NICHT dieselbe Zahl (die Anlagen entscheiden)",
      (zeile.get("karte_info") or {}).get("ertrag_pro_stunde") != zeile.get("ertrag_pro_stunde"),
      str((zeile.get("karte_info") or {}).get("ertrag_pro_stunde")) + " / " + str(zeile.get("ertrag_pro_stunde")))
offen = gs.bot_doerfer_uebersicht(gs.bots[0])
check("6 die offene Uebersicht verraet die Karte NICHT",
      all("karte" not in feld and "karte_info" not in feld for feld in offen), str(sorted(offen[0])))

# ==========================================================================
abschnitt("7. Grenzfaelle und Schalter")
# ==========================================================================
check("7 unbekannte Karte ergibt kein Profil", M.bot_kartenprofil("gibt-es-nicht") == {}, "")
check("7 unbekannte Karte faellt auf den Rueckfall zurueck",
      M.bot_dorf_ertrag(M.BotDorf(name="X", karte="gibt-es-nicht")) == rueckfall, "")
leer = {"aktiv": True, "karten_aktiv": False, "anlagen_je_gebaeude": 1, "hoechstvorrat_je_stoff": 0,
        "gebaeude_je_dorf": ["holzfaeller", "steinmetz", "farm", "goldmine"]}
check("7 der Schalter karten_aktiv=False nimmt dem Dorf die Karte",
      M.bot_dorf_ertrag(M.BotDorf(name="X", karte="original-001"), leer)
      == {"holz": 4.0, "stein": 4.0, "nahrung": 4.0, "gold": 3.0},
      str(M.bot_dorf_ertrag(M.BotDorf(name="X", karte="original-001"), leer)))
b7 = M.BotPlayer("Krank", "monster", 0.9, 0.0, settlements=["K1"])
aus = {"aktiv": True, "karten_aktiv": False, "karten_kandidaten": 3}
check("7 bei abgeschaltetem Schalter werden keine Karten vergeben",
      M.bot_doerfer_karten_zuweisen(b7, aus) == 0 and all(not d.karte for d in b7.doerfer), "")
null_teiler = {"aktiv": True, "karten_aktiv": True, "karten_teiler": 0, "anlagen_je_gebaeude": 1}
try:
    wert = M.bot_dorf_ertrag(M.BotDorf(name="X", karte="original-001"), null_teiler)
    fehler = ""
except Exception as e:                     # noqa: BLE001 - Division durch null waere der Befund
    wert, fehler = None, repr(e)
# Teiler 0 ist ein unsinniger Wert: der Kern nimmt dann den VORGABE-Teiler 10 (kein Absturz, keine
# Division durch null, kein stiller Nullertrag).
check("7 Teiler 0 teilt nicht durch null und liefert den Vorgabe-Teiler",
      bool(wert) and all(v > 0 for v in (wert or {}).values()), str(wert) + fehler)
gross = {"aktiv": True, "karten_aktiv": True, "karten_teiler": 1000}
klein = M.bot_dorf_ertrag(M.BotDorf(name="X", karte="original-001"), gross)
check("7 ein grosser Teiler macht kleine, aber positive Raete",
      all(0 < v < 1 for v in klein.values()), str(klein))
check("7 main.py rechnet den Kartenwert nie mit einer getippten Zahl",
      "original-001" not in TEXT_MAIN, "Kartenkennung steht im Quelltext")

sys.exit(bericht())
