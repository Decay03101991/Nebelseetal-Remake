# -*- coding: ascii -*-
"""Nahrung der Bot-Armee - Stufe S-2 (03.11.2026, Daniel: "Bots als echte Gegner").

Daniels Vorgabe, woertlich: "Nahrung 1:1" wie beim Spieler (8 je Einheit und Spieltag), bei
Unterdeckung KEINE Desertion, aber ein Kaufstopp; aufgestellt wird nur, solange das Lager den
Tagesbedarf der Armee PLUS Reserve deckt.

Was diese Datei beweist
-----------------------
1. Rechnung: `bot_nahrungsbedarf` ist die Rechnung des Spielers (100 Einheiten = 800 je Tag),
   die Reserve das Doppelte (100 Einheiten = 1.600), beides aus den Datendateien, nicht aus
   Literalen im Code.
2. Buchen: eine Stunde mit 100 Einheiten kostet 33,33 Nahrung; der Bestand faellt hoechstens auf
   0; der Rest steht als `unterdeckung` im `produktionsjournal` des Dorfes - in DERSELBEN
   Zeilenform wie beim Spieler (ab, bis, mengen, verbrauch, unterdeckung).
3. Gleiche Rechnung wie der Spieler: `spieloekonomie.ort_tick` kommt fuer dieselbe Armee und
   dieselbe Spanne auf denselben Verbrauch (eine Wahrheit, F-04).
4. Kaufbremse: exakt Soll deckt, Soll - 1 deckt nicht, Soll + 1 deckt; ein frischer Bot ohne
   Armee und ohne Vorrat ist offen (sonst koennte er nie anfangen).
5. Anschluss im Ernteweg: nur das HAUPTDORF isst (ein Bot hat EINE Armee), ein Dorf ohne
   Erntezeit bucht nichts, und der Verbrauch wird genau EINMAL je Spanne gebucht.
6. Bauplan: `bot_doerfer_bebauen` setzt 12 Anlagen und beim zweiten Aufruf KEINE mehr (sonst
   legte jeder Bot-Takt drei weitere nach).
7. Quellwache: der Ernteweg ruft `bot_futter_buchen`, die Aufstellung fragt `bot_nahrung_deckt`.

Aufruf:  python -X utf8 tests/test_bot_nahrung.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

ROOT, SRC = import_src()
import botkern as BK  # noqa: E402
import main as M  # noqa: E402
import spieloekonomie as O  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()


def bot_mit_armee(anzahl: int = 100, nahrung: float = 0.0, doerfer: int = 1):
    """Ein Bot mit EINER Armee und wahlweise mehreren Doerfern (Hauptdorf = das erste)."""
    bot = M.BotPlayer("Pruefbot", BK.BOT_FRAKTIONEN[BK.BOT_NAMEN[0]], 0.3, 0.5)
    # S-5b (03.11.2026): die Armee steht in den DOERFERN (Summe = `bot.army`). Deshalb erst die
    # Doerfer anlegen, dann die Armee setzen - umgekehrt haette das Setzen kein Dorf zum Buchen.
    bot.doerfer = [M.BotDorf(name="Haupt", hauptdorf=(i == 0),
                             vorraete={"nahrung": float(nahrung)})
                   for i in range(doerfer)]
    bot.army = {"Krieger": int(anzahl)} if anzahl else {}
    return bot


# ==========================================================================
abschnitt("1. Rechnung: Tagesbedarf und Reserve")
# ==========================================================================
b100 = bot_mit_armee(100)
check("1 100 Einheiten brauchen 800 Nahrung je Tag (8 je Einheit, Datendatei)",
      abs(M.bot_nahrungsbedarf(b100) - 800.0) < 1e-9, str(M.bot_nahrungsbedarf(b100)))
check("1 die Reserve ist Bedarf + Bedarf x reserve_stunden / versorgung_stunden = 1.600",
      abs(M.bot_reserve_nahrung(b100) - 1600.0) < 1e-9, str(M.bot_reserve_nahrung(b100)))
b0 = bot_mit_armee(0)
check("1 ohne Armee ist der Bedarf 0", M.bot_nahrungsbedarf(b0) == 0.0, str(M.bot_nahrungsbedarf(b0)))
check("1 die Reserve waechst mit der ZAHL der Einheiten (101 Einheiten = 1.616)",
      abs(M.bot_reserve_nahrung(bot_mit_armee(101)) - 1616.0) < 1e-9,
      str(M.bot_reserve_nahrung(bot_mit_armee(101))))
check("1 die Reserve einer ZUSATZ-Einheit ist der Bedarf dieser Einheit plus Reserve (8 x 2 = 16)",
      abs((M.bot_reserve_nahrung(b100, 1) - M.bot_reserve_nahrung(b100)) - 16.0) < 1e-9,
      str(M.bot_reserve_nahrung(b100, 1) - M.bot_reserve_nahrung(b100)))

# ==========================================================================
abschnitt("2. Buchen: eine Stunde, kein negativer Bestand, Unterdeckung im Journal")
# ==========================================================================
b = bot_mit_armee(100, nahrung=1000.0)
dorf = b.doerfer[0]
zeile = M.bot_futter_buchen(b, dorf, 0.0, 3600.0, {"nahrung": 12.0})
check("2 eine Stunde mit 100 Einheiten kostet 33,33 Nahrung (800 / 24)",
      abs(zeile["verbrauch"] - 33.33) < 0.01, str(zeile["verbrauch"]))
check("2 der Bestand sinkt genau um den Verbrauch (1000 -> 966,67)",
      abs(float(dorf.vorraete["nahrung"]) - 966.67) < 0.01, str(dorf.vorraete["nahrung"]))
check("2 keine Unterdeckung, solange das Lager reicht", zeile["unterdeckung"] == 0.0, str(zeile))
letzte = dorf.produktionsjournal[-1]
check("2 die Journalzeile hat die Form des Spielers (ab, bis, mengen, verbrauch, unterdeckung)",
      sorted(letzte) == ["ab", "bis", "mengen", "unterdeckung", "verbrauch"], str(sorted(letzte)))
check("2 'mengen' traegt die reine Ernte der Spanne (nicht den Verbrauch)",
      letzte["mengen"] == {"nahrung": 12.0} and letzte["verbrauch"] == {"nahrung": 33.33},
      str(letzte))
check("2 'ab'/'bis' sind die gefragte Spanne",
      letzte["ab"] == 0.0 and letzte["bis"] == 3600.0, str((letzte["ab"], letzte["bis"])))

arm = bot_mit_armee(100, nahrung=10.0)
zweit = M.bot_futter_buchen(arm, arm.doerfer[0], 0.0, 3600.0)
check("2 der Bestand faellt hoechstens auf 0 (10 vorhanden, 33,33 gebraucht)",
      float(arm.doerfer[0].vorraete["nahrung"]) == 0.0, str(arm.doerfer[0].vorraete))
check("2 der Rest steht als Unterdeckung (33,33 - 10 = 23,33)",
      abs(zweit["unterdeckung"] - 23.33) < 0.01, str(zweit["unterdeckung"]))
check("2 die Unterdeckung steht auch im Journal",
      abs(float(arm.doerfer[0].produktionsjournal[-1]["unterdeckung"]) - 23.33) < 0.01,
      str(arm.doerfer[0].produktionsjournal[-1]))
check("2 kein Verbrauch bei leerer Spanne", M.bot_futter_buchen(b, dorf, 3600.0, 3600.0)["verbrauch"] == 0.0,
      "bis == ab")
check("2 kein Verbrauch bei rueckwaerts laufender Uhr",
      M.bot_futter_buchen(b, dorf, 7200.0, 3600.0)["verbrauch"] == 0.0, "bis < ab")
ohne = bot_mit_armee(0, nahrung=100.0)
check("2 ohne Armee isst niemand und es entsteht keine Journalzeile",
      M.bot_futter_buchen(ohne, ohne.doerfer[0], 0.0, 3600.0)["verbrauch"] == 0.0
      and ohne.doerfer[0].produktionsjournal == [], str(ohne.doerfer[0].produktionsjournal))
alt = M.BotDorf(**{"name": "Alt", "vorraete": None})
b_alt = bot_mit_armee(10)
b_alt.doerfer = [alt]
M.bot_futter_buchen(b_alt, alt, 0.0, 86400.0)
# S-5c (03.11.2026): gegessen wird je DORF fuer SEINE Garnison. Ein Dorf ohne Einheiten isst
# nichts - dann wird auch kein Vorratsfeld angelegt (der Fruehfall kommt vor dem Anlegen). Geprueft
# wird deshalb beides: kein Absturz ohne Garnison UND angelegt, sobald das Dorf Einheiten hat.
check("2 ein altes Dorf ohne Garnison stuerzt nicht ab (kein Essen, kein Feld)",
      M.bot_futter_buchen(b_alt, alt, 0.0, 86400.0)["verbrauch"] == 0.0, str(alt.vorraete))
alt.einheiten = {"Krieger": 10}
alt.vorraete = None
M.bot_futter_buchen(b_alt, alt, 0.0, 86400.0)
check("2 ein altes Dorf MIT Garnison legt das Vorratsfeld an statt abzustuerzen",
      isinstance(alt.vorraete, dict) and float(alt.vorraete.get("nahrung", -1)) == 0.0,
      str(alt.vorraete))

# ==========================================================================
abschnitt("3. Dieselbe Rechnung wie beim Spieler (eine Wahrheit)")
# ==========================================================================
b = bot_mit_armee(100, nahrung=1000.0)
M.bot_futter_buchen(b, b.doerfer[0], 0.0, 3600.0)
bot_verbrauch = 1000.0 - float(b.doerfer[0].vorraete["nahrung"])
check("3 Bot: 100 Einheiten verbrauchen in einer Stunde genauso viel wie tagesbedarf/24",
      abs(bot_verbrauch - round(O.tagesbedarf_nahrung({"Krieger": 100}) / 24.0, 2)) < 0.01,
      f"Bot {bot_verbrauch} gegen Kern {O.tagesbedarf_nahrung({'Krieger': 100}) / 24.0:.4f}")
spieler_ort = {"vorraete": {"nahrung": 1000.0}, "einheiten": {"Krieger": 100},
               "bauten": {}, "stufen": {}, "bevoelkerung": 0.0, "werkstaetten": {},
               "ausbildung": [], "waren": {}, "produktionsjournal": [], "fertigjournal": [],
               "karte": {}}
neu = O.ort_tick(spieler_ort, 0.0, 3600.0, {})
spieler_verbrauch = (1000.0 - float(neu["vorraete"].get("nahrung", 0.0))
                     + float((neu.get("produktionsjournal") or [{}])[-1].get("mengen", {})
                             .get("nahrung", 0.0)))
check("3 Spieler (ort_tick) und Bot (bot_futter_buchen) kommen auf denselben Verbrauch",
      abs(spieler_verbrauch - bot_verbrauch) < 0.02,
      f"Spieler {spieler_verbrauch:.4f} gegen Bot {bot_verbrauch:.4f}")

# ==========================================================================
abschnitt("4. Kaufbremse: exakt Soll deckt, Soll - 1 nicht")
# ==========================================================================
b = bot_mit_armee(100)
soll = M.bot_reserve_nahrung(b, 1)                       # Deckung fuer die NAECHSTE Einheit
b.doerfer[0].vorraete["nahrung"] = soll
check("4 genau Soll deckt (Grenze geschlossen)", M.bot_nahrung_deckt(b, 1) is True, str(soll))
b.doerfer[0].vorraete["nahrung"] = soll - 1
check("4 Soll - 1 deckt NICHT", M.bot_nahrung_deckt(b, 1) is False, str(soll - 1))
b.doerfer[0].vorraete["nahrung"] = soll + 1
check("4 Soll + 1 deckt", M.bot_nahrung_deckt(b, 1) is True, str(soll + 1))
frisch = bot_mit_armee(0, nahrung=0.0)
check("4 ein frischer Bot ohne Armee und ohne Vorrat ist offen (er muss anfangen koennen)",
      M.bot_nahrung_deckt(frisch, 1) is True, str(M.bot_kasse(frisch)))

gs = M.GameState()
gs.bots = [bot_mit_armee(100, nahrung=100.0)]
hungrig = gs.bots[0]
hungrig.doerfer[0].vorraete.update({"holz": 5000.0, "stein": 5000.0, "gold": 5000.0, "siedler": 500.0,
                                    "leder": 500.0, "wolle": 500.0})
check("4 die Aufstellung blockt bei zu wenig Futter",
      gs.bot_armee_aufstellen(hungrig) is None, str(M.bot_kasse(hungrig)))
check("4 der blockierte Bot hat trotzdem Holz, Stein und Gold (es fehlt NUR das Futter)",
      float(hungrig.vorraete.get("holz", 0)) == 5000.0, str(hungrig.vorraete))

satt = bot_mit_armee(100, nahrung=5000.0)
satt.doerfer[0].vorraete.update({"holz": 5000.0, "stein": 5000.0, "gold": 5000.0,
                                 "nahrung": 5000.0, "siedler": 500.0,
                                 "leder": 500.0, "wolle": 500.0})   # S-5a: Preis der Einheit
# S-5a (03.11.2026): "Warteschlange statt Kauf" - Staette und Ausruestung muessen VOR ORT stehen.
satt.doerfer[0].bauten["7"] = "kriegerakademie"
satt.doerfer[0].stufen["7"] = 1
satt.doerfer[0].waren.update(M.ausruestung.fehlende("Krieger", {}))
gekauft = gs.bot_armee_aufstellen(satt)
check("4 mit gedecktem Futter beginnt der Bot eine Ausbildung", bool(gekauft), str(gekauft))
check("4 der Auftrag steht in der Warteschlange SEINES Dorfes",
      len(satt.doerfer[0].ausbildung) == 1, str(satt.doerfer[0].ausbildung))
check("4 die Armee waechst erst mit der Ausbildung, nicht sofort",
      sum(int(v) for v in satt.army.values()) == 100, str(satt.army))
# S-3 (03.11.2026): Siedler sind seit Register 156 Menschen in `bevoelkerung`, nicht mehr ein
# Rohstoff im Lager. Die Ernte liefert deshalb weiterhin keinen Posten "siedler" - der Nachwuchs
# kommt aus dem Siedlerzuwachs (1 je Ort und Stunde, gedeckelt durch die Gebaeude).
_siedler_aus_ernte = "siedler" in M.bot_dorf_ertrag(M.BotDorf(name="X", karte=""),
                                                   M.bot_wirtschaft_einstellungen())
check("4 die Ernte liefert keinen Rohstoff 'siedler' (Siedler sind Bevoelkerung, keine Ware)",
      _siedler_aus_ernte is False, str(_siedler_aus_ernte))
check("4 der gekaufte Bot hat danach weniger Bevoelkerung im Hauptdorf (Preis bezahlt)",
      float(M.bot_doerfer_sicherstellen(satt)[0].bevoelkerung) < 500.0,
      str(M.bot_doerfer_sicherstellen(satt)[0].bevoelkerung))

# ==========================================================================
abschnitt("5. Anschluss im Ernteweg: nur das Hauptdorf isst, genau einmal je Spanne")
# ==========================================================================
b = bot_mit_armee(100, nahrung=0.0, doerfer=2)
b.doerfer[0].vorraete = {"nahrung": 1000.0}
b.doerfer[1].vorraete = {"nahrung": 1000.0}
for d in b.doerfer:
    d.karte = ""
    d.ernte_seit = 0.0
M.bot_doerfer_ernten(b, 1000.0)                               # erster Lauf: nur Zeitstempel
check("5 der erste Lauf bucht nichts (kein Nachtrag fuer die Vergangenheit)",
      b.doerfer[0].produktionsjournal == [] and b.doerfer[1].produktionsjournal == [],
      str([len(d.produktionsjournal) for d in b.doerfer]))
M.bot_doerfer_ernten(b, 4600.0)                               # eine Stunde spaeter
check("5 nach einer Stunde hat NUR das Hauptdorf eine Futterzeile",
      len(b.doerfer[0].produktionsjournal) == 1 and b.doerfer[1].produktionsjournal == [],
      str([len(d.produktionsjournal) for d in b.doerfer]))
_zeile = b.doerfer[0].produktionsjournal[0] if b.doerfer[0].produktionsjournal else {}
_std = float(_zeile.get("verbrauch", {}).get("nahrung", 0.0))
check("5 im Hauptdorf sind genau die 33,33 der Stunde abgebucht",
      abs(_std - 33.33) < 0.01, str(_std))
_ernte_std = float((_zeile.get("mengen") or {}).get("nahrung", 0.0))
check("5 der Bestand ist Ernte minus Verbrauch (keine zweite Buchung daneben)",
      abs(float(b.doerfer[0].vorraete["nahrung"]) - (1000.0 + _ernte_std - _std)) < 0.02,
      f"Bestand {b.doerfer[0].vorraete['nahrung']} gegen {1000.0 + _ernte_std - _std:.2f}")
_rate_neben = float(M.bot_dorf_ertrag(b.doerfer[1], M.bot_wirtschaft_einstellungen(), b).get("nahrung", 0.0))
check("5 das Nebendorf erntet, isst aber nichts (ein Bot hat EINE Armee)",
      b.doerfer[1].produktionsjournal == []
      and abs(float(b.doerfer[1].vorraete["nahrung"]) - (1000.0 + _rate_neben)) < 0.02,
      f"{b.doerfer[1].vorraete['nahrung']} = 1000 + {_rate_neben}")
M.bot_doerfer_ernten(b, 4600.0)
check("5 eine stehende Uhr bucht nichts nach (kein Doppelverbrauch)",
      len(b.doerfer[0].produktionsjournal) == 1,
      str(len(b.doerfer[0].produktionsjournal)))
M.bot_doerfer_ernten(b, 8200.0)
check("5 eine zweite Stunde bucht genau eine zweite Zeile",
      len(b.doerfer[0].produktionsjournal) == 2,
      str(len(b.doerfer[0].produktionsjournal)))
_summe = sum(float((z.get("verbrauch") or {}).get("nahrung", 0.0))
             for z in b.doerfer[0].produktionsjournal)
check("5 zwei Stunden kosten 66,67 (zwei Zeilen zu 33,33)",
      abs(_summe - 66.67) < 0.02, str(_summe))

# ==========================================================================
abschnitt("6. Bauplan: einmal setzen, beim zweiten Mal nichts")
# ==========================================================================
beb = M.BotDorf(name="Bau", hauptdorf=True, karte="original-036")
erst = M.bot_doerfer_bebauen(beb)
zweit = M.bot_doerfer_bebauen(beb)
check("6 der erste Aufruf setzt die 12 Grundanlagen", erst == 12, str(erst))
check("6 der zweite Aufruf setzt NICHTS nach (sonst waechst jeder Bot-Takt weiter)",
      zweit == 0, str(zweit))
check("6 es bleiben 12 Anlagen im Dorf", len(beb.bauten) == 12, str(len(beb.bauten)))
check("6 jede Anlage steht auf Stufe 1", all(int(s) == 1 for s in beb.stufen.values()),
      str(sorted(set(beb.stufen.values()))))

# ==========================================================================
abschnitt("7. Quellwache: der Anschluss ist im Code, nicht nur in dieser Datei")
# ==========================================================================
check("7 der Ernteweg ruft bot_futter_buchen", "bot_futter_buchen(bot, dorf, seit, jetzt" in TEXT_MAIN,
      "main.bot_doerfer_ernten")
# ENTSCHEIDUNG GEAENDERT (S-5c, 03.11.2026): gebucht wird NICHT mehr nur im Hauptdorf, sondern in
# JEDEM Dorf fuer seine eigene Garnison. Die Wache prueft jetzt genau das - der Aufruf steht ohne
# Hauptdorf-Bedingung im Ernteweg, und die Bedingung ist aus dem Kern-Weg verschwunden.
check("7 gebucht wird je Dorf, nicht mehr nur im Hauptdorf",
      "bot_futter_buchen(bot, dorf, seit, jetzt" in TEXT_MAIN
      and "if getattr(dorf, \"hauptdorf\", False):                             # die Armee isst im Hauptdorf"
      not in TEXT_MAIN,
      "main.bot_doerfer_ernten")
check("7 die Aufstellung fragt die Kaufbremse", "if not bot_nahrung_deckt(bot, 1):" in TEXT_MAIN,
      "main.bot_armee_aufstellen")
check("7 der Kartenweg setzt den Bauplan", "bot_doerfer_bebauen(dorf, einstellungen)" in TEXT_MAIN,
      "main.bot_doerfer_karten_zuweisen")

sys.exit(bericht())
