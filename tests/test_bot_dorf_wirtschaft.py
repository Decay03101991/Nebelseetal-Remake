# -*- coding: ascii -*-
"""Wirtschaft je Bot-Dorf - Stufe B-3 (02.11.2026, Konzept K-1).

BEFUND B-1: jeder Bot hatte EINE Kasse (`BotPlayer.vorraete`); die Doerfer trugen zwar ein eigenes
Vorratsfeld, es war aber ausdruecklich NICHT fuehrend. B-3 dreht das: die DOERFER halten das Gut,
die Kasse des Bots ist ihre Summe. Damit wird der Bot erstmals wirtschaftlich - vorher hatte er nur
seine Startvorrate und konnte nach dem ersten Einkauf nie wieder etwas bezahlen.

Was diese Datei beweist
-----------------------
1. Traeger: `BotDorf.ernte_seit` und das Dorflager existieren; der Bot fuehrt KEIN eigenes
   Vorratsfeld mehr (sonst waere es die zweite Buchfuehrung).
2. EINE Lesestelle: `bot_dorf_ertrag` rechnet den Stundensatz aus `data/buildings.json`; die Werte
   stimmen mit `gelaende.ertrag_pro_stunde` auf dem besten Gelaende ueberein, auf dem die Anlage
   stehen darf, mal der Zahl der Anlagen je Grundrohstoff (Daniel 02.11.2026: drei = 12/12/12/9) -
   keine zweite Zahlenliste, kein Literal im Code.
3. Ernte: der erste Lauf bucht NICHTS (nur den Zeitstempel), eine Stunde bringt die Rate je Dorf,
   zwei Stunden das Doppelte, eine stehende oder rueckwaerts laufende Uhr bucht nichts, der
   Lagerdeckel haelt, der Schalter `aktiv` schaltet die Wirtschaft ab.
4. Kasse = Summe der Doerfer: Lesen liefert die Summe, Setzen verteilt OHNE Rest, Buchen ist der
   einzige Schreibweg, der Bestand wird nie negativ, ein Schreibversuch in ein Zwischenergebnis
   aendert still nichts.
5. Ausbildung zahlt aus den Doerfern: nach dem Kauf ist die Summe genau um den belegten Preis
   kleiner - kein zweites Lager, aus dem man kostenlos Einheiten ziehen koennte.
6. Migration: ein Spielstand mit EINER alten Kasse laedt ohne Fehler und verliert nichts; ein altes
   Dorf ohne `ernte_seit` bekommt beim ersten Lauf KEINE Nachtragsrente fuer die Vergangenheit.
7. Anzeige: der Spionagebericht nennt je Dorf Vorrate und Ertrag aus DERSELBEN Funktion (F-04); die
   offene Uebersicht bleibt ohne Vorrate (Anzeigegrenze Daniel 02.11.2026).
8. Der Bot-Takt erntet VOR dem Zug und meldet die Ernte.

Aufruf:  python -X utf8 tests/test_bot_dorf_wirtschaft.py
"""
from __future__ import annotations

import os
import sys
from dataclasses import asdict, fields

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

ROOT, SRC = import_src()
import gelaende  # noqa: E402
import botkern as BK  # noqa: E402
import main as M  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()


def neuer_stand():
    """Ein GameState mit einem Spielerdorf und den fuenf echten Bots (Muster: test_s7)."""
    gs = M.GameState()
    gs.settlements = [M.Settlement(name="Testdorf", map_id="kontinent",
                                   x=3, y=3, id="spieler:kontinent:3:3",
                                   vorraete={"holz": 100.0, "stein": 100.0})]
    gs.bots = [M.BotPlayer(n, BK.BOT_FRAKTIONEN[n], 0.2, 0.5)
               for n in BK.BOT_NAMEN]
    gs.noob_protection = False
    gs._letzter_bot_takt = 0.0
    return gs


# ==========================================================================
abschnitt("1. Traeger: Dorflager und Erntezeit, aber keine zweite Kasse")
# ==========================================================================
dorf = M.BotDorf(name="Pruefdorf")
check("1 das Dorf traegt Vorrate", isinstance(dorf.vorraete, dict), str(dorf.vorraete))
check("1 das Dorf traegt eine Erntezeit (Vorgabe 0)", float(dorf.ernte_seit) == 0.0, str(dorf.ernte_seit))
feldnamen = [f.name for f in fields(M.BotPlayer)]
check("1 der Bot hat KEIN Feld vorraete mehr", "vorraete" not in feldnamen,
      str([n for n in feldnamen if "vorrat" in n]))
b0 = M.BotPlayer("Haug", "menschlich", 0.3, 0.8, settlements=["Haus A", "Haus B"])
b0.vorraete = {"holz": 40}
check("1 die Kasse ist eine Eigenschaft (kein eigener Speicher)",
      "vorraete" not in b0.__dict__ and M.bot_kasse(b0) == {"holz": 40.0}, str(b0.__dict__.keys()))
# Quelltext-Wache (ast, damit Docstrings nicht mitzaehlen - ein Kommentar IST kein Schreibzugriff):
# keine Stelle in `src/main.py` darf in `bot.vorraete[...]` schreiben. Mit der Eigenschaft landet
# ein solcher Schreibzugriff in einem Zwischenergebnis und waere STILL verloren.
import ast  # noqa: E402

_schreibstellen = []
for _knoten in ast.walk(ast.parse(TEXT_MAIN)):
    if isinstance(_knoten, (ast.Assign, ast.AugAssign)):
        _ziele = _knoten.targets if isinstance(_knoten, ast.Assign) else [_knoten.target]
        for _ziel in _ziele:
            if (isinstance(_ziel, ast.Subscript) and isinstance(_ziel.value, ast.Attribute)
                    and _ziel.value.attr == "vorraete"
                    and isinstance(_ziel.value.value, ast.Name)
                    and _ziel.value.value.id in ("bot", "b")):
                _schreibstellen.append(getattr(_knoten, "lineno", 0))
check("1 main.py schreibt nirgends in bot.vorraete[...] (nur bot_kasse_buchen)",
      _schreibstellen == [], str(_schreibstellen))
# Dieselbe Falle als METHODENAUFRUF: `bot.vorraete.clear()` / `.update()` wuerde in der Kopie der
# Eigenschaft landen und die Beute aus dem Nichts erzeugen (real passiert am 02.11.2026 im
# Beute-Pfad, gefunden von `test_gpt_kampf_botbeute_echte_kasse`).
_methoden = []
for _knoten in ast.walk(ast.parse(TEXT_MAIN)):
    if isinstance(_knoten, ast.Call) and isinstance(_knoten.func, ast.Attribute):
        _ziel = _knoten.func.value
        if (isinstance(_ziel, ast.Attribute) and _ziel.attr == "vorraete"
                and isinstance(_ziel.value, ast.Name) and _ziel.value.id in ("bot", "b")
                and _knoten.func.attr in ("clear", "update", "pop", "setdefault")):
            _methoden.append((_knoten.func.attr, getattr(_knoten, "lineno", 0)))
check("1 main.py ruft keine veraendernde Methode auf bot.vorraete auf",
      _methoden == [], str(_methoden))

# ==========================================================================
abschnitt("2. EINE Lesestelle: der Stundensatz kommt aus den Spieldaten")
# ==========================================================================
werte = M.bot_dorf_ertrag()
einstellungen = M.bot_wirtschaft_einstellungen()
anzahl = int(einstellungen.get("anlagen_je_gebaeude") or 1)
erwartet = {}
for geb in ("holzfaeller", "steinmetz", "farm", "goldmine"):
    eintrag = gelaende.alle_gebaeude().get(geb) or {}
    bester = 0.0
    for art in gelaende.GELAENDEARTEN:
        erlaubt, _grund = gelaende.bau_moeglich(geb, art)
        if not erlaubt:
            continue
        wert = gelaende.ertrag_pro_stunde(geb, art)
        if isinstance(wert, (int, float)) and float(wert) > bester:
            bester = float(wert)
    if eintrag.get("rohstoff"):
        erwartet[str(eintrag["rohstoff"]).lower()] = round(bester * anzahl, 2)
check("2 der Ertrag stimmt mit data/buildings.json mal Anlagenzahl ueberein", werte == erwartet,
      str(werte) + " / " + str(erwartet) + " (Anlagen je Art: " + str(anzahl) + ")")
check("2 Daniels Entscheidung 02.11.2026 steht in der Datendatei (drei Anlagen)",
      anzahl == 3, str(anzahl))
check("2 die vier Grundrohstoffe sind gesetzt",
      sorted(werte) == ["gold", "holz", "nahrung", "stein"], str(sorted(werte)))
check("2 keine Null und keine erfundene Grosszahl", all(0 < v <= 40 for v in werte.values()), str(werte))
check("2 die Funktion ist wiederholbar (Cache liefert dieselben Zahlen)",
      M.bot_dorf_ertrag() == werte, str(M.bot_dorf_ertrag()))
leer = {"aktiv": True, "gebaeude_je_dorf": [], "hoechstvorrat_je_stoff": 0}
check("2 ohne Anlagen gibt es keinen Ertrag", M.bot_dorf_ertrag(None, leer) == {}, "")

# ==========================================================================
abschnitt("3. Ernte: Grenzfaelle 0 s, 1 h, 2 h, rueckwaerts, Deckel, Schalter")
# ==========================================================================
b1 = M.BotPlayer("Brynhild", "menschlich", 0.5, 0.6, settlements=["A", "B"])
# V-5 (03.11.2026): der Ertrag haengt jetzt am VOLK des Bots (menschlich: Holz +5 %, Stein -5 %).
# Die Wache bleibt dieselbe - sie fragt nur mit demselben Bot wie die Ernte (12,6 / 11,4 je Dorf).
rate = M.bot_dorf_ertrag(None, None, b1)
doerfer = len(M.bot_doerfer_sicherstellen(b1))
check("3 zwei Doerfer angelegt", doerfer == 2, str(doerfer))
leer0 = M.bot_doerfer_ernten(b1, 1000.0)
check("3 der erste Lauf bucht NICHTS (nur Zeitstempel)", leer0 == {}, str(leer0))
check("3 der Zeitstempel steht jetzt auf der Spielzeit",
      all(float(d.ernte_seit) == 1000.0 for d in b1.doerfer), str([d.ernte_seit for d in b1.doerfer]))
gleich = M.bot_doerfer_ernten(b1, 1000.0)
check("3 exakt 0 Sekunden buchen nichts", gleich == {}, str(gleich))
e1 = M.bot_doerfer_ernten(b1, 4600.0)
check("3 eine Stunde bringt die Rate je Dorf",
      e1 == {k: round(v * doerfer, 2) for k, v in rate.items()}, str(e1))
e2 = M.bot_doerfer_ernten(b1, 8200.0)
check("3 die naechste Stunde bringt wieder dieselbe Rate (nicht kumulativ)",
      e2 == {k: round(v * doerfer, 2) for k, v in rate.items()}, str(e2))
rueck = M.bot_doerfer_ernten(b1, 5000.0)
check("3 eine rueckwaerts laufende Uhr bucht nichts", rueck == {}, str(rueck))
check("3 die Erntezeit bleibt dabei auf dem letzten gueltigen Wert",
      all(float(d.ernte_seit) == 8200.0 for d in b1.doerfer), str([d.ernte_seit for d in b1.doerfer]))

b2 = M.BotPlayer("Grom", "zwergisch", 0.7, 0.4, settlements=["C"])
M.bot_doerfer_ernten(b2, 100.0)
gedeckelt = {"aktiv": True, "gebaeude_je_dorf": ["holzfaeller"], "hoechstvorrat_je_stoff": 10}
e3 = M.bot_doerfer_ernten(b2, 100.0 + 3600.0 * 1000, gedeckelt)
check("3 der Lagerdeckel haelt die Ernte an", e3.get("holz") == 10, str(e3))
check("3 das Dorflager steht genau auf dem Deckel",
      float(b2.doerfer[0].vorraete.get("holz", 0)) == 10.0, str(b2.doerfer[0].vorraete))

b3 = M.BotPlayer("Silra", "elfisch", 0.2, 0.9, settlements=["D"])
M.bot_doerfer_ernten(b3, 100.0)
aus = {"aktiv": False, "gebaeude_je_dorf": ["holzfaeller"], "hoechstvorrat_je_stoff": 0}
check("3 der Schalter aktiv=False schaltet die Wirtschaft ab",
      M.bot_doerfer_ernten(b3, 5000.0, aus) == {}, str(M.bot_kasse(b3)))

# ==========================================================================
abschnitt("4. Kasse = Summe der Doerfer, Buchen ist der einzige Schreibweg")
# ==========================================================================
b4 = M.BotPlayer("Krank", "monster", 0.9, 0.0, settlements=["E", "F", "G"])
b4.vorraete = {"holz": 101, "stein": 7}
kasse = M.bot_kasse(b4)
check("4 die Summe ist exakt der gesetzte Wert", kasse == {"holz": 101.0, "stein": 7.0}, str(kasse))
check("4 die Summe der Doerfer ist genau die Kasse",
      round(sum(float(d.vorraete.get("holz", 0)) for d in b4.doerfer), 2) == 101.0,
      str([d.vorraete for d in b4.doerfer]))
check("4 kein Dorf traegt einen negativen Bestand",
      all(float(v) >= 0 for d in b4.doerfer for v in d.vorraete.values()), str(b4.doerfer))
vorher = M.bot_kasse(b4)["holz"]
b4.vorraete["holz"] = 0
check("4 ein Schreibversuch in ein Zwischenergebnis aendert still NICHTS",
      M.bot_kasse(b4)["holz"] == vorher, str(M.bot_kasse(b4)["holz"]))
check("4 Buchen zieht ab", M.bot_kasse_buchen(b4, "holz", -50) == 51.0, str(M.bot_kasse(b4)))
check("4 Buchen wird nie negativ", M.bot_kasse_buchen(b4, "holz", -99999) == 0.0, str(M.bot_kasse(b4)))
check("4 Buchen kann zubuchen", M.bot_kasse_buchen(b4, "gold", 12) == 12.0, str(M.bot_kasse(b4)))
check("4 nach dem Buchen ist die Kasse weiter die Summe der Doerfer",
      M.bot_kasse(b4) == {"holz": 0.0, "stein": 7.0, "gold": 12.0}, str(M.bot_kasse(b4)))

# ==========================================================================
abschnitt("5. Ausbildung zahlt aus den Doerfern (kein zweites Lager)")
# ==========================================================================
gs = neuer_stand()
b5 = M.BotPlayer("Haug", "menschlich", 0.3, 0.8, settlements=["H"])
b5.vorraete = {"holz": 5000, "stein": 5000, "nahrung": 5000, "gold": 5000,
               "metall": 5000, "siedler": 500}
vorher_kasse = M.bot_kasse(b5)
# S-3 (03.11.2026, Register 156): Siedler sind MENSCHEN und stehen in `bevoelkerung` des
# Hauptdorfes, nicht mehr als Rohstoff in der Kasse. Die Wache vergleicht deshalb jeden
# Rohstoffposten mit der Kasse und den Siedler-Posten mit der Bevoelkerung - die Zusicherung
# "der Bot zahlt den belegten Preis" bleibt, nur die Buchungsstelle ist die richtige.
vorher_bev = float(M.bot_doerfer_sicherstellen(b5)[0].bevoelkerung)
gestellt = gs.bot_armee_aufstellen(b5)
check("5 der Bot stellt eine Einheit auf", isinstance(gestellt, str) and bool(gestellt), str(gestellt))
gestellt = gestellt if isinstance(gestellt, str) else ""
kosten = {str(k): float(v) for k, v in ((M.einheiten.alle().get(gestellt) or {}).get("kosten") or {}).items()}
nachher_kasse = M.bot_kasse(b5)
check("5 die Kasse ist genau um den Preis kleiner (Rohstoffe)",
      all(round(nachher_kasse.get(s, 0.0), 2) == round(vorher_kasse.get(s, 0.0) - k, 2)
          for s, k in kosten.items() if s != "siedler"),
      str({s: (vorher_kasse.get(s), nachher_kasse.get(s), k) for s, k in kosten.items()
           if s != "siedler"}))
check("5 die Siedler gehen von der Bevoelkerung des Hauptdorfes ab",
      abs(float(M.bot_doerfer_sicherstellen(b5)[0].bevoelkerung)
          - (vorher_bev - float(kosten.get("siedler", 0)))) < 0.01,
      f"vorher {vorher_bev}, nachher {M.bot_doerfer_sicherstellen(b5)[0].bevoelkerung}, "
      f"Siedler-Preis {kosten.get('siedler')}")
check("5 Siedler stehen NICHT mehr als Rohstoff in der Kasse",
      "siedler" not in nachher_kasse, str(sorted(nachher_kasse)))
check("5 die Doerfer tragen die Abbuchung (Summe bleibt die Kasse)",
      round(sum(float(d.vorraete.get("holz", 0)) for d in b5.doerfer), 2) == nachher_kasse.get("holz", 0.0),
      str([d.vorraete.get("holz") for d in b5.doerfer]))

# ==========================================================================
abschnitt("6. Migration: alte Kasse, alte Doerfer, Speichern und Laden")
# ==========================================================================
alt = {"name": "Grom", "faction": "zwergisch", "aggression": 0.7, "trading": 0.4,
       "settlements": ["Groms Siedlung 1", "Groms Siedlung 2"],
       "vorraete": {"holz": 50, "gold": 7}}
try:
    alt_bot = M.bot_aus_stand(alt)
    fehler = ""
except Exception as e:                     # noqa: BLE001 - der Fehler ist der Befund
    alt_bot, fehler = None, repr(e)
check("6 ein Stand mit EINER alten Kasse laedt ohne Ausnahme", alt_bot is not None, fehler)
if alt_bot is not None:
    check("6 die alte Kasse steckt jetzt in den Doerfern",
          M.bot_kasse(alt_bot) == {"holz": 50.0, "gold": 7.0}, str(M.bot_kasse(alt_bot)))
    check("6 der Bot fuehrt kein eigenes Vorratsfeld", "vorraete" not in alt_bot.__dict__, "")
    erste = M.bot_doerfer_ernten(alt_bot, 7200.0)
    check("6 ein alter Stand bekommt KEINE Nachtragsrente", erste == {}, str(erste))
    zweite = M.bot_doerfer_ernten(alt_bot, 10800.0)
    check("6 danach wirtschaftet er normal", bool(zweite), str(zweite))
    rund = M.bot_aus_stand(json_daten := asdict(alt_bot))
    check("6 Speichern und Laden erhaelt die Kasse",
          M.bot_kasse(rund) == M.bot_kasse(alt_bot), str((M.bot_kasse(rund), M.bot_kasse(alt_bot))))
altes_dorf = M.BotDorf(**{"name": "Alt", "vorraete": {"holz": 3}})
check("6 ein Dorf ohne ernte_seit bekommt die Vorgabe 0", float(altes_dorf.ernte_seit) == 0.0,
      str(altes_dorf.ernte_seit))
check("6 ein Dorf ohne Vorratsfeld bekommt ein leeres", isinstance(M.BotDorf(name="Leer").vorraete, dict), "")

# ==========================================================================
abschnitt("7. Anzeige: Spionagebericht und offene Uebersicht")
# ==========================================================================
gs = neuer_stand()
bericht_bot = gs.bots[0]
bericht_bot.vorraete = {"holz": 90, "stein": 30}
berichtsdaten = gs.bot_doerfer_spionagebericht(bericht_bot)
check("7 je Dorf ein Berichtsteil",
      len(berichtsdaten["doerfer"]) == len(bericht_bot.doerfer), str(len(berichtsdaten["doerfer"])))
check("7 der Bericht zeigt den Ertrag aus DERSELBEN Funktion",
      all(d.get("ertrag_pro_stunde") == M.bot_dorf_ertrag(dorf, None, bericht_bot)
          for d, dorf in zip(berichtsdaten["doerfer"], bericht_bot.doerfer)), "")
check("7 der Bericht fuehrt die Kasse als Summe der Doerfer",
      berichtsdaten.get("kasse") == M.bot_kasse(bericht_bot), str(berichtsdaten.get("kasse")))
check("7 der Bericht nennt die Vorrate JE DORF",
      all(isinstance(d.get("vorraete"), dict) for d in berichtsdaten["doerfer"]), "")
offen = gs.bot_doerfer_uebersicht(bericht_bot)
check("7 die offene Uebersicht bleibt ohne Vorrate",
      all("vorraete" not in zeile for zeile in offen), str(sorted(offen[0])))

# ==========================================================================
abschnitt("8. Der Bot-Takt erntet vor dem Zug")
# ==========================================================================
gs = neuer_stand()
erster_zug = gs.bots_fortschreiben(3600.0)
check("8 der erste Takt meldet die Ernte als Feld", "ernte" in erster_zug, str(sorted(erster_zug)))
check("8 der erste Takt bucht noch nichts (Doerfer ohne Erntezeit)",
      erster_zug.get("ernte") == {}, str(erster_zug.get("ernte")))
zweiter_zug = gs.bots_fortschreiben(7200.0)
check("8 der zweite Takt erntet", bool(zweiter_zug.get("ernte")), str(zweiter_zug.get("ernte")))
check("8 die Doerfer aller Bots tragen danach die Spielzeit",
      all(float(d.ernte_seit) == 7200.0 for b in gs.bots for d in b.doerfer),
      str([(b.name, [d.ernte_seit for d in b.doerfer]) for b in gs.bots]))
check("8 die Doerfer haben Gut im Lager",
      all(any(float(v) > 0 for v in d.vorraete.values()) for b in gs.bots for d in b.doerfer),
      str([(b.name, d.vorraete) for b in gs.bots for d in b.doerfer]))

sys.exit(bericht())
