"""Pruefung des Bot-Kerns (Paket W5) - was Computergegner ueber die Zeit tun.

Belegt gegen `docs/ENTWURF_AUFTRAEGE.md` (Bot-KI) und `data/units.json` (Karrenladungen).
Geprueft werden: die belegten Wertebereiche, der 6-24-h-Angriffstakt, die Beute (50 %,
gedeckelt durch die Karrenladung), der Handelspreis (Referenzpreis x 1,2, Temperament
+-10 %), die Wiederholbarkeit mit festem Seed, der Unterschied zwischen kriegerischen und
friedlichen Bots ueber dieselbe Zeitspanne und die Liste der offenen Luecken.

Reine Logik: kein Fenster, keine Uhr - `jetzt` wird immer uebergeben, Zufall kommt aus
`random.Random(seed)`.
"""
from __future__ import annotations

import copy
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, befund, check, import_src

ROOT, SRC = import_src()
import botkern as BK
import einheiten as E

TEXT = open(os.path.join(SRC, "botkern.py"), encoding="utf-8").read()

SEK_UHR = BK.SEKUNDEN_JE_STUNDE


def karren_mit_ladung(wert):
    """Der Originalkarren mit genau dieser Ladung (aus data/units.json, kein Literal)."""
    for n in E.nach_rolle("karren"):
        if E.ladung(n) == wert:
            return n
    return None


KLEIN = karren_mit_ladung(40)      # Handkarren
MITTEL = karren_mit_ladung(100)    # Einspaenner
GROSS = karren_mit_ladung(250)     # Zweispaenner


class FesterZufall:
    """Stub mit vorgegebenen random()-Werten und fester Wartezeit (6 h)."""

    def __init__(self, werte):
        self.werte = list(werte)
        self.i = 0

    def random(self):
        v = self.werte[self.i % len(self.werte)]
        self.i += 1
        return v

    def uniform(self, a, b):
        return a

    def randint(self, a, b):
        return a


def baue_bot(**werte):
    bot = {
        "name": "Testbot", "fraktion": "menschlich",
        "aggression": 0.5, "trading": 0.5, "temperament": 0.0,
        "punkte": 100, "ruf": 10, "vorraete": {"holz": 100}, "lager": {KLEIN: 1},
        "letzter_angriff": None, "naechster_angriff": 0.0, "angriffe": 0,
    }
    bot.update(werte)
    return bot


WELT = {"vorraete": {"holz": 200, "stein": 100}, "referenzpreis": 1000.0}


# ============================================================ 1. neue Bots
abschnitt("1. neue Bots - belegte Wertebereiche, Wiederholbarkeit")

bots5 = BK.neue_bots(5, random.Random(20261005))
check("neue_bots liefert eine Liste", isinstance(bots5, list))
check("neue_bots(5) hat fuenf Eintraege", len(bots5) == 5)
check("jeder Bot ist ein dict", all(isinstance(b, dict) for b in bots5))
noetig = {"name", "fraktion", "aggression", "trading", "temperament",
          "vorraete", "lager", "naechster_angriff"}
check("jeder Bot traegt die noetigen Felder", all(noetig <= set(b) for b in bots5))
check("aggression immer in [0,1] (belegter Bereich)",
      all(0.0 <= b["aggression"] <= 1.0 for b in bots5),
      str([b["aggression"] for b in bots5]))
check("trading immer in [0,1] (belegter Bereich)",
      all(0.0 <= b["trading"] <= 1.0 for b in bots5),
      str([b["trading"] for b in bots5]))
check("temperament immer in [-1,1] (+-10 %)",
      all(-1.0 <= b["temperament"] <= 1.0 for b in bots5))
check("die fuenf belegten Gegennamen (main.BOTS)",
      [b["name"] for b in bots5] == BK.BOT_NAMEN)
check("die belegten Fraktionen stimmen",
      [b["fraktion"] for b in bots5] == ["menschlich", "menschlich", "zwergisch",
                                         "elfisch", "monster"])

check("gleicher Seed -> gleiche Bots (Wiederholbarkeit)",
      BK.neue_bots(5, random.Random(77)) == BK.neue_bots(5, random.Random(77)))
check("anderer Seed -> andere Bots",
      BK.neue_bots(5, random.Random(1)) != BK.neue_bots(5, random.Random(2)))
check("anzahl 0 -> leere Liste", BK.neue_bots(0, random.Random(1)) == [])
check("negatives anzahl -> leere Liste", BK.neue_bots(-3, random.Random(1)) == [])
mehr = BK.neue_bots(7, random.Random(5))
check("mehr als fuenf Bots moeglich (Name mit Nummer)", len(mehr) == 7 and
      mehr[5]["name"].endswith("-2"))

# Wagenpark besteht nur aus belegten Karren mit Ladung
kap_summe = sum(E.kapazitaet(n, a) for b in bots5 for n, a in b["lager"].items())
check("der Wagenpark neuer Bots hat echte Ladekapazitaet",
      all(E.kapazitaet(n, 1) > 0 for b in bots5 for n in b["lager"]), str(kap_summe))


# ============================================================ 2. Uebersicht
abschnitt("2. bot_uebersicht")

ue = BK.bot_uebersicht(bots5[0])
check("bot_uebersicht liefert ein dict", isinstance(ue, dict))
check("Uebersicht traegt Name und Werte", ue["name"] == bots5[0]["name"] and
      ue["aggression"] == bots5[0]["aggression"])
check("aggression 0.9 -> kriegerisch",
      BK.bot_uebersicht(baue_bot(aggression=0.9))["haltung"] == "kriegerisch")
check("aggression 0.1 -> friedlich",
      BK.bot_uebersicht(baue_bot(aggression=0.1))["haltung"] == "friedlich")
check("temperament_prozent ist Temperament x 10",
      BK.bot_uebersicht(baue_bot(temperament=0.7))["temperament_prozent"] == 7.0)
vorher = copy.deepcopy(bots5[0])
BK.bot_uebersicht(bots5[0])
check("bot_uebersicht veraendert den Bot nicht", bots5[0] == vorher)


# ============================================================ 3. Handelspreis
abschnitt("3. Handelspreis - Referenzpreis x 1,2, Temperament +-10 %")

check("Referenzpreis = Beschaffungskosten x 1,2",
      BK.referenzpreis_aus_beschaffung(1000) == 1200.0)
ref = BK.referenzpreis_aus_beschaffung(1000)
check("Temperament 0 -> Referenzpreis unveraendert", BK.handelspreis(ref, 0.0) == 1200.0)
check("Temperament +1 -> +10 %", BK.handelspreis(ref, 1.0) == 1320.0)
check("Temperament -1 -> -10 %", BK.handelspreis(ref, -1.0) == 1080.0)
check("drei Temperamente folgen der belegten Regel",
      [BK.handelspreis(ref, t) for t in (-1.0, 0.0, 1.0)] == [1080.0, 1200.0, 1320.0])
check("Temperament +0.5 -> +5 %", BK.handelspreis(ref, 0.5) == 1260.0)
check("Temperament ueber 1 wird geklemmt", BK.handelspreis(ref, 5.0) == 1320.0)
check("Temperament unter -1 wird geklemmt", BK.handelspreis(ref, -5.0) == 1080.0)
check("Preis steigt monoton mit dem Temperament",
      BK.handelspreis(ref, -1.0) < BK.handelspreis(ref, 0.0) < BK.handelspreis(ref, 1.0))
check("unbrauchbares Temperament wirkt wie 0", BK.handelspreis(ref, "x") == 1200.0)


# ============================================================ 4. Angriffstakt
abschnitt("4. naechster_angriff_moeglich - Zeit wird uebergeben")

b = baue_bot(naechster_angriff=1000.0)
check("vor dem Fenster kein Angriff", BK.naechster_angriff_moeglich(b, 999.0) is False)
check("genau am Fenster Angriff moeglich", BK.naechster_angriff_moeglich(b, 1000.0) is True)
check("nach dem Fenster Angriff moeglich", BK.naechster_angriff_moeglich(b, 1001.0) is True)
check("frischer Bot (0.0) darf sofort", BK.naechster_angriff_moeglich(baue_bot(), 0.0) is True)
check("keine Uhr im Modul - nur `jetzt` entscheidet",
      BK.naechster_angriff_moeglich(b, 500.0) != BK.naechster_angriff_moeglich(b, 1500.0))


# ============================================================ 5. Beute
abschnitt("5. beute_begrenzen - genau 50 %, gedeckelt durch die Karrenladung")

check("Karrenladungen aus den Spieldaten: 40 / 100 / 250",
      (E.ladung(KLEIN), E.ladung(MITTEL), E.ladung(GROSS)) == (40, 100, 250))

voll = BK.beute_begrenzen({"holz": 200, "stein": 100}, {GROSS: 2})  # Kapazitaet 500
check("genau 50 % der Vorraete bei genug Platz", voll == {"holz": 100, "stein": 50},
      str(voll))
check("kein Rohstoff bekommt mehr als die Haelfte",
      all(voll[k] <= {"holz": 200, "stein": 100}[k] * 0.5 for k in voll))
check("Summe nie groesser als die Karrenladung", sum(voll.values()) <= 500)

eng = BK.beute_begrenzen({"holz": 200, "stein": 100}, {"kapazitaet": 10})
check("enge Karrenladung: gedeckelt auf 10", sum(eng.values()) <= 10, str(eng))
check("auch gekappt nie mehr als 50 % je Rohstoff",
      all(eng[k] <= {"holz": 200, "stein": 100}[k] * 0.5 for k in eng))

check("Kapazitaet genau gleich der Haelfte -> volle 50 %",
      BK.beute_begrenzen({"holz": 100, "stein": 50}, {"kapazitaet": 75})
      == {"holz": 50, "stein": 25})
check("ohne Karren keine Beute", BK.beute_begrenzen({"holz": 200}, {}) == {})
check("leere Vorraete -> keine Beute", BK.beute_begrenzen({}, {GROSS: 5}) == {})
check("rng veraendert die Beute nicht",
      BK.beute_begrenzen({"holz": 200}, {GROSS: 2}, random.Random(1))
      == BK.beute_begrenzen({"holz": 200}, {GROSS: 2}, random.Random(9)))
check("lager als {karren: {...}} wird gelesen",
      BK.beute_begrenzen({"holz": 200}, {"karren": {GROSS: 1}}) == {"holz": 100})
check("lager als {Karrenname: Anzahl} wird gelesen",
      BK.beute_begrenzen({"holz": 200}, {GROSS: 1}) == {"holz": 100})


# ============================================================ 6. Ein Zug / Intervall
abschnitt("6. tick - Angriff nur ausserhalb des 6-24-h-Fensters")

tb = baue_bot(aggression=1.0, naechster_angriff=0.0, lager={GROSS: 2})
e1 = BK.tick(tb, WELT, 0.0, random.Random(11))
check("tick liefert die drei Felder aktion/meldung/wirkung",
      {"aktion", "meldung", "wirkung"} <= set(e1))
check("erster Zug ist der Angriff", e1["aktion"] == "angreifen")
check("Meldung ist ein nicht-leerer Text", isinstance(e1["meldung"], str) and e1["meldung"])

b1 = BK.wirkung_anwenden(tb, e1)
fenster = b1["naechster_angriff"] - 0.0
check("naechstes Fenster liegt bei 6 bis 24 Stunden",
      BK.ANGRIFF_MIN_STUNDEN * SEK_UHR <= fenster <= BK.ANGRIFF_MAX_STUNDEN * SEK_UHR,
      f"{fenster / SEK_UHR:.2f} h")
check("1 h nach dem Angriff kein zweiter Angriff moeglich",
      BK.naechster_angriff_moeglich(b1, SEK_UHR) is False)
check("kurz vor dem Fenster kein Angriff",
      BK.naechster_angriff_moeglich(b1, fenster - 1.0) is False)
check("genau am Fenster ist der Angriff wieder moeglich",
      BK.naechster_angriff_moeglich(b1, fenster) is True)
e2 = BK.tick(b1, WELT, fenster, random.Random(12))
check("nach dem Fenster greift der Bot erneut an", e2["aktion"] == "angreifen")

check("tick veraendert den Bot nicht (rein)", tb == baue_bot(
    aggression=1.0, naechster_angriff=0.0, lager={GROSS: 2}))
welt_kopie = copy.deepcopy(WELT)
BK.tick(tb, WELT, 0.0, random.Random(11))
check("tick veraendert die Welt nicht (rein)", WELT == welt_kopie)


# ============================================================ 7. Alle Aktionen erreichbar
abschnitt("7. tick - alle fuenf Aktionen sind erreichbar")

fern = 10 ** 12
check("warten erreichbar",
      BK.tick(baue_bot(trading=0.0, naechster_angriff=fern), WELT, 0.0,
              FesterZufall([0.0, 0.9]))["aktion"] == "warten")
check("forschen erreichbar",
      BK.tick(baue_bot(trading=0.0, naechster_angriff=fern), WELT, 0.0,
              FesterZufall([0.0, 0.1]))["aktion"] == "forschen")
check("bauen erreichbar",
      BK.tick(baue_bot(trading=0.0, naechster_angriff=fern), WELT, 0.0,
              FesterZufall([0.0, 0.6]))["aktion"] == "bauen")
check("handeln erreichbar",
      BK.tick(baue_bot(trading=1.0, naechster_angriff=fern), WELT, 0.0,
              FesterZufall([0.0]))["aktion"] == "handeln")
check("angreifen erreichbar",
      BK.tick(baue_bot(aggression=1.0, naechster_angriff=0.0, lager={GROSS: 2}),
              WELT, 0.0, FesterZufall([0.0]))["aktion"] == "angreifen")
check("jede Aktion liegt im erlaubten Satz",
      all(BK.tick(baue_bot(naechster_angriff=fern), WELT, 0.0,
                  FesterZufall([0.0, x]))["aktion"]
          in ("bauen", "forschen", "handeln", "angreifen", "warten")
          for x in (0.0, 0.3, 0.6, 0.9)))


# ============================================================ 8. Wirkung anwenden
abschnitt("8. wirkung_anwenden - nur hier aendert sich ein Bot")

bot_v = baue_bot(angriffe=0)
erg = {"aktion": "angreifen", "meldung": "x",
       "wirkung": {"beute": {"holz": 30}, "naechster_angriff": 5000.0, "angriffe": 1}}
neu = BK.wirkung_anwenden(bot_v, erg)
check("Beute wandert in die Vorraete", neu["vorraete"]["holz"] == 130)
check("Angriff wird gezaehlt", neu["angriffe"] == 1)
check("naechstes Fenster wird uebernommen", neu["naechster_angriff"] == 5000.0)
check("der Ausgangsbot bleibt unveraendert",
      bot_v["vorraete"]["holz"] == 100 and bot_v["angriffe"] == 0 and
      bot_v["naechster_angriff"] == 0.0)


# ============================================================ 9. bots_tick
abschnitt("9. bots_tick - sortiert, mit Kurzfassung fuer Nachrichten")

kopf = BK.neue_bots(4, random.Random(3))
liste = list(reversed(kopf))
bt = BK.bots_tick(liste, WELT, 0.0, random.Random(99))
check("bots_tick nennt die Anzahl", bt["anzahl"] == 4)
namen = [e["bot"] for e in bt["ergebnisse"]]
check("die Ergebnisse sind nach Name sortiert", namen == sorted(namen), str(namen))
check("je Bot eine Nachricht", len(bt["nachrichten"]) == 4)
check("Aktionszaehler summiert auf die Anzahl",
      sum(bt["aktionen"].values()) == 4)
check("Kurzfassung enthaelt Meldungen", isinstance(bt["text"], str) and
      all(z.strip() for z in bt["text"].splitlines()))
check("gleicher Seed -> gleiches bots_tick",
      BK.bots_tick(kopf, WELT, 0.0, random.Random(42)) ==
      BK.bots_tick(kopf, WELT, 0.0, random.Random(42)))


# ============================================================ 10. Wiederholbarkeit
abschnitt("10. Zwei Laeufe mit gleichem Seed sind identisch")

def lauf(seed, schritte=48):
    rng = random.Random(seed)
    bot = baue_bot(aggression=0.7, naechster_angriff=0.0, lager={GROSS: 1})
    welt = {"vorraete": {"holz": 400, "stein": 100}, "referenzpreis": 500.0}
    spur = []
    jetzt = 0.0
    for _ in range(schritte):
        e = BK.tick(bot, welt, jetzt, rng)
        spur.append((e["aktion"], e["meldung"]))
        bot = BK.wirkung_anwenden(bot, e)
        jetzt += 3600.0
    return spur, bot


s1, _ = lauf(2026)
s2, _ = lauf(2026)
check("gleicher Seed -> identische Zugfolge", s1 == s2)
s3, _ = lauf(999)
check("anderer Seed -> andere Zugfolge", s1 != s3)


# ============================================================ 11. Kriegerisch vs friedlich
abschnitt("11. Kriegerischer Bot greift oefter an als ein friedlicher")

def zaehle_angriffe(aggression, seed, tage=40):
    bot = baue_bot(aggression=aggression, trading=0.0, naechster_angriff=0.0,
                   lager={GROSS: 1})
    rng = random.Random(seed)
    n = 0
    jetzt = 0.0
    ende = tage * BK.SEKUNDEN_JE_TAG
    while jetzt <= ende:
        e = BK.tick(bot, WELT, jetzt, rng)
        if e["aktion"] == "angreifen":
            n += 1
        bot = BK.wirkung_anwenden(bot, e)
        jetzt += 3600.0
    return n


for _s in (1, 7, 42):
    k = zaehle_angriffe(0.9, _s)
    f = zaehle_angriffe(0.1, _s)
    check(f"Seed {_s}: kriegerisch ({k}) oefter als friedlich ({f})", k > f)


# ============================================================ 12. Offene Luecken
abschnitt("12. offene_luecken - keine erfundene Zahl ohne Kennzeichnung")

luecken = BK.offene_luecken()
check("offene_luecken liefert ein dict", isinstance(luecken, dict))
check("die Lueckenliste ist nicht leer", len(luecken) >= 5)
check("alle Eintraege sind Texte", all(isinstance(v, str) for v in luecken.values()))
check("das Angriffsintervall ist als Vorschlag benannt", "angriffsintervall" in luecken)
check("Startinventar und Gewichte sind benannt",
      "startinventar" in luecken and "aktionsgewichte" in luecken)
check("jede Luecke begruendet sich (VORSCHLAG / Nicht geregelt)",
      all(("VORSCHLAG" in v) or ("Nicht geregelt" in v) for v in luecken.values()))


# ============================================================ 13. Bot-Punkte (Register 46)
abschnitt("13. Bot-Punkte kommen aus der belegten Formel, nicht aus dem Zufall")

import punkte as P

_leer = {"armee": {}, "punkte": 0}
check("ein Bot ohne Armee hat 0 Punkte", BK.bot_punkte(_leer) == 0, str(BK.bot_punkte(_leer)))
check("Punkte entsprechen punkte.kriegspunkte der Armee",
      BK.bot_punkte({"armee": {"Kämpfer": 2, "Ritter": 1}}) ==
      P.kriegspunkte({"Kämpfer": 2, "Ritter": 1}, 0),
      str(BK.bot_punkte({"armee": {"Kämpfer": 2, "Ritter": 1}})))
check("eine Wallstufe zaehlt hoch drei mit",
      BK.bot_punkte({"armee": {}, "wall_stufe": 2}) == 8,
      str(BK.bot_punkte({"armee": {}, "wall_stufe": 2})))
check("Unsinn in der Armee ergibt 0 statt Absturz",
      BK.bot_punkte({"armee": "kaputt"}) == 0)

_bots = BK.neue_bots(5, random.Random(7))
check("kein neuer Bot startet mit Zufallspunkten",
      all(b.get("punkte") == 0 for b in _bots), str([b.get("punkte") for b in _bots]))
check("jeder neue Bot traegt ein Wallfeld", all("wall_stufe" in b for b in _bots))
check("gleicher Seed ergibt gleiche Punkte",
      [b.get("punkte") for b in BK.neue_bots(5, random.Random(7))] ==
      [b.get("punkte") for b in _bots])

_w = BK.wirkung_anwenden({"armee": {}, "punkte": 99}, {"wirkung": {}})
check("wirkung_anwenden rechnet die Punkte neu (kein Fortschreiben der Wuerfelzahl)",
      _w.get("punkte") == 0, str(_w.get("punkte")))
_w2 = BK.wirkung_anwenden({"armee": {"Kämpfer": 3}, "punkte": 99}, {"wirkung": {}})
check("Punkte folgen der Armee", _w2.get("punkte") == P.kriegspunkte({"Kämpfer": 3}, 0),
      str(_w2.get("punkte")))


# ============================================================ 14. Quellhygiene
abschnitt("13. botkern.py - reine Logik, nur Standardbibliothek")

check("botkern.py ist reines ASCII", all(ord(c) < 128 for c in TEXT))
check("kein tkinter", "tkinter" not in TEXT)
check("kein Netzwerk", not any(w in TEXT for w in ("requests", "urllib", "socket", "http")))
check("keine Datei wird geschrieben", "open(" not in TEXT)
check("Standardkennung vorhanden", BK.STAND.startswith("2026-"))


sys.exit(bericht())
