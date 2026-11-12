# -*- coding: ascii -*-
"""S-7: Bot-Taktik angebunden - Verhalten, Sperrzeit, Ankuendigung, Attribute.

Geprueft wird die Anbindung des Zustandsautomaten `bottaktik` an den Spielkern
(Schnitt S-7 aus docs/auftraege/B3_paket_20261101.md):

  * je Taktik eine andere Entscheidung in derselben Lage (fuenf echte Gegner)
  * ein Zustandswechsel wird angekuendigt (genau einmal) und hat eine Sperrzeit
  * Volksattribute sind dauerhaft, Verhaltensboni befristet (mit Ablaufzeit)
  * beide additiv im Spielstand: ein ALTER Stand ohne die neuen Felder laedt
  * Anzeige und Kern benutzen DIESELBE Funktion (`bottaktik.anzeige`)
  * Punkte bleiben die belegte Formel `(Krieg + Forschung) // 2`
  * Zeitbasis ist Spielzeit (`jetzt`), kein `time.time()` im neuen Pfad
  * Demo-Regel: Bots greifen in der oeffentlichen Testversion nicht an

Reine Logik und Spielstand: kein Fenster, keine Rechnerzeit im neuen Pfad.
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "quelltext"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['auftraege', 'botkern', 'bottaktik', 'main:*', 'punkte', 'voelker', 'welt']
PRUEF_DATEN = ['voelker.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import copy
import json
import os
import random
import sys
import tempfile
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import bottaktik as BT
import botkern as BK
import main as M

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
TEXT_TAKTIK = open(os.path.join(SRC, "bottaktik.py"), encoding="utf-8").read()

WELT = {"spielerdorf": {"x": 10, "y": 10, "name": "Spielerdorf"}}


def baue_bot(name, fraktion, aggression=0.6):
    """Ein Bot-dict in der Form, mit der `bottaktik` rechnet."""
    return {"name": name, "fraktion": fraktion, "aggression": aggression,
            "trading": 0.5, "x": 10, "y": 6}


def neuer_stand():
    """Ein GameState mit einem Spielerdorf und den fuenf echten Bots."""
    gs = M.GameState()
    gs.settlements = [M.Settlement(name="Testdorf", map_id="kontinent",
                                   x=3, y=3, id="spieler:kontinent:3:3",
                                   vorraete={"holz": 100.0, "stein": 100.0})]
    gs.bots = [M.BotPlayer(n, BK.BOT_FRAKTIONEN[n], 0.2, 0.5)
               for n in BK.BOT_NAMEN]
    gs.noob_protection = False
    gs._letzter_bot_takt = 0.0
    return gs


# ============================================================ 1. S-7-Daten
abschnitt("1. S-7-Daten - Sperrzeit, Ablaufzeit, Volksattribute, Boni")

check("SPERRZEIT_NACH_WECHSEL ist positiv", BT.SPERRZEIT_NACH_WECHSEL > 0)
check("VERHALTENSBONUS_DAUER ist positiv", BT.VERHALTENSBONUS_DAUER > 0)
# UMGESTELLT 03.11.2026 (A2, Register 148): seit Daniels Entscheidung gibt es SECHS Fraktionen
# (menschlich, zwergisch, elfisch, Trolle, Ghule, Gnome - die drei letzten ersetzen "monster"). Die
# alte Wache nagelte "genau die vier Fraktionen der Bots" fest; geprueft wird jetzt die neue
# Entscheidung: die Quelle `data/voelker.json` traegt sechs, und jede Fraktion, die ein Bot traegt,
# ist darin bekannt.
check("die Quelle kennt genau die sechs Fraktionen",
      set(BT.VOLKSATTRIBUTE) == {str(e["kennung"]) for e in BT.fraktionen()}
      and len(BT.fraktionen()) == 6,
      str(sorted(BT.VOLKSATTRIBUTE)))
check("jede Fraktion der Bots ist in der Quelle bekannt",
      set(BK.BOT_FRAKTIONEN.values()) <= set(BT.VOLKSATTRIBUTE),
      str(sorted(set(BK.BOT_FRAKTIONEN.values()) - set(BT.VOLKSATTRIBUTE))))
check("jede Fraktion traegt plus und minus",
      all({"plus", "minus"} <= set(v) for v in BT.VOLKSATTRIBUTE.values()))
check("jede Taktik traegt ein Bonusfeld",
      all(isinstance(t.get("bonus"), str) for t in BT.TAKTIKEN.values()))
check("volksattribute liefert die zwergischen Werte",
      BT.volksattribute({"fraktion": "zwergisch"})["plus"] == "Steinertrag +5 %")
check("volksattribute einer unbekannten Fraktion ist leer",
      BT.volksattribute({"fraktion": "gibtsnicht"}) == {"plus": "", "minus": ""})
check("volksattribute veraendert die Eingabe nicht",
      (lambda b: (BT.volksattribute(b), b["fraktion"])[1])(
          {"fraktion": "elfisch"}) == "elfisch")
check("verhaltensbonus_aktiv ist bei abgelaufenem Bonus False",
      BT.verhaltensbonus_aktiv({"verhaltensbonus": {"bis": 100.0}}, 200.0) is False)
check("verhaltensbonus_aktiv ist vor Ablauf True",
      BT.verhaltensbonus_aktiv({"verhaltensbonus": {"bis": 100.0}}, 50.0) is True)
check("verhaltensbonus_aktiv ohne Bonus ist False",
      BT.verhaltensbonus_aktiv({}, 0.0) is False)


# ============================================================ 2. je Taktik anders
abschnitt("2. fuenf Taktiken entscheiden in derselben Lage verschieden")

aktionen = {}
for name in BK.BOT_NAMEN:
    bot = baue_bot(name, BK.BOT_FRAKTIONEN[name])
    e = BT.tick(bot, WELT, 0.0, random.Random(1))
    aktionen[name] = e["aktion"]
check("fuenf Bots liefern fuenf verschiedene Aktionen",
      len(set(aktionen.values())) == 5, str(aktionen))
check("jede Aktion ist eine bekannte Zustandsaktion",
      all(a in BT.ZUSTANDS_AKTION.values() or a == "warten"
          for a in aktionen.values()), str(aktionen))


# ============================================================ 3. Sperrzeit greift
abschnitt("3. Sperrzeit nach einem Zustandswechsel")

bot = {"name": "Haug", "fraktion": "menschlich", "aggression": 0.5,
       "zustand": BT.SAMMELN, "gedaechtnis": dict(BT.GEDAECHTNIS_DEFAULT)}
e1 = {"aktion": "sammeln", "naechster_zustand": BT.WACHSEN, "wirkung": {}}
neu1 = BT.wirkung_anwenden(bot, e1, 1000.0)
check("ein Wechsel setzt die Sperrzeit",
      neu1["wechsel_sperre_bis"] == 1000.0 + BT.SPERRZEIT_NACH_WECHSEL,
      str(neu1.get("wechsel_sperre_bis")))
check("der Wechsel wurde vollzogen", neu1["zustand"] == BT.WACHSEN)

e2 = {"aktion": "wachsen", "naechster_zustand": BT.SICHERN, "wirkung": {}}
neu2 = BT.wirkung_anwenden(neu1, e2, 1500.0)
check("innerhalb der Sperrzeit wird nicht gewechselt",
      neu2["zustand"] == BT.WACHSEN, str(neu2.get("zustand")))
check("der blockierte Wechsel wird als solcher markiert",
      neu2.get("wechsel_blockiert") is True)

e3 = {"aktion": "wachsen", "naechster_zustand": BT.SICHERN, "wirkung": {}}
neu3 = BT.wirkung_anwenden(neu2, e3, 9999.0)
check("nach Ablauf der Sperrzeit wird gewechselt",
      neu3["zustand"] == BT.SICHERN, str(neu3.get("zustand")))


# ============================================================ 4. Ankuendigung genau einmal
abschnitt("4. ein Wechsel wird angekuendigt - genau einmal")

bot = {"name": "Grom", "fraktion": "zwergisch", "aggression": 0.5,
       "zustand": BT.SAMMELN, "gedaechtnis": dict(BT.GEDAECHTNIS_DEFAULT)}
e_w = {"aktion": "sammeln", "naechster_zustand": BT.WACHSEN, "wirkung": {}}
neu_w = BT.wirkung_anwenden(bot, e_w, 1000.0)
check("der Wechsel traegt eine Ankuendigung",
      isinstance(neu_w.get("wechsel_ankuendigung"), str)
      and "wechselt" in neu_w["wechsel_ankuendigung"],
      str(neu_w.get("wechsel_ankuendigung")))

e_gleich = {"aktion": "wachsen", "naechster_zustand": BT.WACHSEN, "wirkung": {}}
neu_gleich = BT.wirkung_anwenden(neu_w, e_gleich, 2000.0)
check("kein Wechsel, keine zweite Ankuendigung",
      neu_gleich.get("wechsel_ankuendigung") is None)

# Auf der Hauptebene: ein echter Wechsel wird genau EINMAL angekuendigt.
gs = neuer_stand()
gs.bots = [M.BotPlayer("Haug", "menschlich", 0.2, 0.5)]
gs.bots[0].zustand = BT.SAMMELN
gs.bots[0].vorraete = {"holz": 200}   # ueber SCHWELLE_SAMMELN_HOLZ -> Wechsel zu WACHSEN
gs.bots[0].gedaechtnis = dict(BT.GEDAECHTNIS_DEFAULT)
gs.bots_fortschreiben(3600.0)
wechsel = [m.get("text", "") for m in gs.messages
           if m.get("type") == "bot" and "wechselt" in m.get("text", "")]
check("der Wechsel wird auf der Hauptebene angekuendigt",
      len(wechsel) == 1, str(wechsel))
check("die Ankuendigung nennt Bot und neuen Zustand",
      bool(wechsel) and "Haug" in wechsel[0] and "Dorf ausbauen" in wechsel[0],
      wechsel[0] if wechsel else "")
check("der Bot traegt den neuen Zustand",
      gs.bots[0].zustand == BT.WACHSEN, str(gs.bots[0].zustand))


# ============================================================ 5. Anbindung in bots_fortschreiben
abschnitt("5. bots_fortschreiben schreibt Zustand, Gedaechtnis, Attribute")

gs = neuer_stand()
gs.bots_fortschreiben(3600.0)
check("jeder Bot traegt jetzt einen Zustand",
      all(b.zustand in BT.ZUSTAENDE for b in gs.bots),
      str([b.zustand for b in gs.bots]))
check("jeder Bot fuehrt das Gedaechtnis mit den Defaults",
      all(bot.gedaechtnis.get("geschlagen_von") is None
          and "letzter_kontakt" in bot.gedaechtnis for bot in gs.bots))
check("jeder Bot traegt dauerhafte Volksattribute aus seiner Fraktion",
      all(b.volksattribute == BT.volksattribute({"fraktion": b.faction})
          for b in gs.bots),
      str([b.volksattribute for b in gs.bots]))
check("jeder Bot traegt einen befristeten Verhaltensbonus mit Ablaufzeit",
      all(isinstance(b.verhaltensbonus, dict)
          and float(b.verhaltensbonus.get("bis", 0.0)) > 3600.0
          for b in gs.bots),
      str([b.verhaltensbonus for b in gs.bots]))
check("der Verhaltensbonus der Taktik steht im Bonusfeld",
      gs.bots[0].verhaltensbonus.get("text") == BT.taktik_von(
          {"name": gs.bots[0].name})["bonus"],
      str(gs.bots[0].verhaltensbonus))


# ============================================================ 6. alter Spielstand laedt
abschnitt("6. alter Spielstand ohne die neuen Felder laedt ohne Umwandlung")

with tempfile.TemporaryDirectory() as tmp:
    pfad = os.path.join(tmp, "s7_stand.json")
    gs = neuer_stand()
    gs.bots_fortschreiben(3600.0)
    check("der neue Stand speichert", gs.save(pfad) is True)

    # Rueckweg: die neuen Felder ueberleben einen Speichern/Laden-Zyklus.
    andere = M.GameState()
    check("der neue Stand laedt wieder", andere.load(pfad) is True)
    geladen = {b.name: b for b in andere.bots}
    check("der Zustand ueberlebt das Laden",
          all(geladen[n].zustand in BT.ZUSTAENDE for n in BK.BOT_NAMEN))
    check("die Volksattribute ueberleben das Laden",
          geladen["Grom"].volksattribute.get("plus") == "Steinertrag +5 %")

    # Alter Stand: die S-7-Felder fehlen komplett.
    roh = json.loads(open(pfad, encoding="utf-8").read())
    for b in roh.get("bots", []):
        for feld in ("zustand", "gedaechtnis", "marsch_ankunft", "flucht_ende",
                     "letzter_abstand", "naechster_marsch_h", "wechsel_sperre_bis",
                     "volksattribute", "verhaltensbonus"):
            b.pop(feld, None)
    alt_pfad = os.path.join(tmp, "s7_alt.json")
    with open(alt_pfad, "w", encoding="utf-8") as fh:
        json.dump(roh, fh)
    alt = M.GameState()
    check("der alte Stand (ohne S-7-Felder) laedt", alt.load(alt_pfad) is True)
    alt_bot = next(b for b in alt.bots if b.name == "Haug")
    check("fehlender Zustand faellt auf die Vorgabe zurueck",
          alt_bot.zustand == "" and alt_bot.gedaechtnis == {}
          and alt_bot.volksattribute == {} and alt_bot.verhaltensbonus == {},
          str(alt_bot.zustand))
    check("der alte Bot laesst sich weiter fortschreiben",
          (lambda g: (setattr(g, "_letzter_bot_takt", 0.0),
                      g.bots_fortschreiben(7200.0))[1])(alt)["bots"] == len(alt.bots))


# ============================================================ 7. Anzeige == Kern
abschnitt("7. die Anzeige nutzt dieselbe Funktion wie der Kern")

check("main.py ruft bottaktik.anzeige auf (keine zweite Anzeige)",
      "bottaktik.anzeige" in TEXT_MAIN)
gs = neuer_stand()
gs.bots_fortschreiben(3600.0)
zeilen = {b.name: BT.anzeige(gs.bot_als_dict(b)) for b in gs.bots}
check("die Anzeige nennt fuer jeden Bot den Taktiknamen",
      all(BT.taktik_von({"name": n})["name"] in zeilen[n] for n in BK.BOT_NAMEN),
      str(zeilen))
check("die Anzeige bleibt eine einzelne kurze Zeile",
      all("\n" not in z and len(z) <= 80 for z in zeilen.values()),
      str([len(z) for z in zeilen.values()]))


# ============================================================ 8. Punkte unveraendert
abschnitt("8. Punkte bleiben (Krieg + Forschung) // 2 - keine zweite Formel")

bot_punkte_probe = {"name": "Haug", "fraktion": "menschlich",
                    "armee": {"Paladin": 10},
                    "wall_stufe": 4, "forschung_stufen": {"a": 2}}
check("bot_punkte rechnet weiter die belegte Formel",
      BK.bot_punkte(bot_punkte_probe) == (224 + 8) // 2,
      str(BK.bot_punkte(bot_punkte_probe)))
check("bottaktik fuehrt keine zweite Punkteformel ein",
      "punkte" not in BT.ZUSTAENDE and "bot_punkte" not in TEXT_TAKTIK)
bot_mit_punkten = {"name": "Haug", "fraktion": "menschlich", "punkte": 42,
                   "zustand": BT.SAMMELN, "gedaechtnis": dict(BT.GEDAECHTNIS_DEFAULT)}
neu_p = BT.wirkung_anwenden(bot_mit_punkten,
                            {"aktion": "sammeln", "naechster_zustand": BT.WACHSEN}, 1000.0)
check("bottaktik.wirkung_anwenden laesst punkte unangetastet",
      neu_p.get("punkte") == 42, str(neu_p.get("punkte")))


# ============================================================ 9. Zeitbasis Spielsekunden
abschnitt("9. Zeitbasis ist Spielzeit - kein time.time() im neuen Pfad")

# Der neue bottaktik-Block in bots_fortschreiben darf nicht auf die Rechneruhr greifen.
kern = TEXT_MAIN.split("def bots_fortschreiben")[1].split("def tick")[0]
check("der Bot-Zug-Pfad ruft kein time.time() auf",
      "time.time()" not in kern)

gefangen = {}

def tick_fake(bot, welt, jetzt, rng=None):
    gefangen["jetzt"] = jetzt
    return {"aktion": "warten", "meldung": "", "wirkung": {},
            "naechster_zustand": bot.get("zustand") or BT.taktik_von(bot)["startzustand"]}

gs = neuer_stand()
with patch.object(BT, "tick", side_effect=tick_fake):
    gs.bots_fortschreiben(4711.0)
check("bottaktik.tick erhaelt die uebergebene Spielzeit",
      gefangen.get("jetzt") == 4711.0, str(gefangen.get("jetzt")))


# ============================================================ 10. Demo-Regel
abschnitt("10. Demo-Regel - in der oeffentlichen Testversion greifen Bots nicht an")

demo_zug = {"aktionen": {"angreifen": 1},
            "ergebnisse": [{"bot": "Haug", "aktion": "angreifen",
                            "meldung": "Haug versucht einen Angriff.",
                            "wirkung": {"beute": {"holz": 50}, "angriffe": 1,
                                        "naechster_angriff": 50000.0}}],
            "nachrichten": []}
gs = neuer_stand()
vorher = dict(gs.settlements[0].vorraete)
try:
    os.environ["NEBEL_OEFFENTLICHE_TESTVERSION"] = "1"
    with patch("main.botkern.bots_tick", side_effect=lambda *a, **k: demo_zug):
        gs.bots_fortschreiben(25000.0)
finally:
    os.environ.pop("NEBEL_OEFFENTLICHE_TESTVERSION", None)
check("in der Demo wird keine Beute vom Spielerdorf genommen",
      gs.settlements[0].vorraete == vorher, str(gs.settlements[0].vorraete))
check("die Demo-Begruendung steht in der Meldung",
      any("nicht freigeschaltet" in t for t in gs.log),
      str([t for t in gs.log if "Demo" in t or "nicht freigeschaltet" in t][:2]))


sys.exit(bericht())
