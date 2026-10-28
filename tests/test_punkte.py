"""
Punkte, Rangliste, Goetterschutz und Sieg/Niederlage (Paket W6, 04.10.2026).

Prueft `src/punkte.py` gegen das Handbuch 2009 (Seiten 3-6) und die Datendateien:

  * Forschungspunkte = Summe Stufe hoch drei (0..3 -> 0, 1, 8, 27)
  * Kriegspunkte = Einheitenwerte + Wallstufe hoch drei (Stufe 4 -> 64)
  * Gesamtpunktzahl = (Kriegs + Forschungs) / 2   -- Handbuchbeispiel 150/200 -> 175
  * Ruf geht nicht in die Gesamtpunkte ein
  * Goetterschutz = sieben Tage, laeuft ab
  * Rangliste: Punkte, dann Ruf, dann frueheres Anmeldedatum
  * Sieg/Niederlage ist ausdruecklich ein VORSCHLAG (das Handbuch nennt keine Bedingung)

Aufruf:  python -X utf8 tests/test_punkte.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, befund, bericht, check, import_src

ROOT, SRC = import_src()
import einheiten as E
import punkte as P

TAG = 86400


# ==========================================================================
# 1. Belege und Vorschlaege
# ==========================================================================

abschnitt("Belege und Vorschlaege — was ist Handbuch, was ist eigene Zahl")

_formeln = P.belegte_formeln()
check("belegte_formeln() liefert ein Verzeichnis", isinstance(_formeln, dict) and bool(_formeln))
check("die Gesamtpunktformel ist belegt",
      "gesamtpunkte" in _formeln and "/ 2" in _formeln["gesamtpunkte"], str(_formeln.keys()))
check("die Forschungsformel verweist auf 'hoch drei'",
      "hoch drei" in _formeln.get("forschungspunkte", ""), _formeln.get("forschungspunkte", "")[:80])
check("die Wallformel nennt das Handbuchbeispiel Palisade Stufe 4 = 64",
      "64" in _formeln.get("kriegspunkte_wall", ""), _formeln.get("kriegspunkte_wall", "")[:80])
check("die Goetterschutzformel nennt 'sieben Tage'",
      "sieben Tage" in _formeln.get("goetterschutz", ""), _formeln.get("goetterschutz", "")[:80])
check("Ruf ist laut Beleg NICHT Teil der Gesamtpunktzahl",
      "NICHT" in _formeln.get("rufpunkte", ""), _formeln.get("rufpunkte", "")[:80])
check("kein Beleg behauptet eine Siegbedingung",
      "sieg" not in " ".join(_formeln).lower() and "niederlage" not in " ".join(_formeln).lower())

_v = P.vorschlaege()
check("vorschlaege() ist gefuellt", isinstance(_v, dict) and len(_v) >= 4, f"{len(_v)} Eintraege")
check("jeder Vorschlag traegt den Status VORSCHLAG",
      all(e.get("status") == "VORSCHLAG" for e in _v.values()),
      str([e.get("status") for e in _v.values()]))
check("jeder Vorschlag nennt einen Grund",
      all(bool(e.get("grund")) for e in _v.values()))
check("die Siegbedingung ist ausdruecklich ein Vorschlag",
      _v.get("siegbedingung", {}).get("status") == "VORSCHLAG"
      and "das Handbuch nennt keine Siegbedingung" == _v.get("siegbedingung", {}).get("grund"),
      str(_v.get("siegbedingung")))
check("die Niederlagebedingung ist ausdruecklich ein Vorschlag",
      _v.get("niederlagebedingung", {}).get("status") == "VORSCHLAG"
      and "das Handbuch nennt keine Niederlagebedingung" == _v.get("niederlagebedingung", {}).get("grund"),
      str(_v.get("niederlagebedingung")))
check("die Rundung ist als Vorschlag gekennzeichnet (Handbuch nennt keine)",
      _v.get("gesamt_rundung", {}).get("status") == "VORSCHLAG", str(_v.get("gesamt_rundung")))


# ==========================================================================
# 2. Forschungspunkte
# ==========================================================================

abschnitt("Forschungspunkte — Summe der Stufen hoch drei")

check("leerer Forschungsstand gibt 0", P.forschungspunkte({}) == 0)
check("None als Forschungsstand gibt 0", P.forschungspunkte(None) == 0)
check("Stufe 0 ergibt 0 (0*0*0)", P.forschungspunkte({"x": 0}) == 0)
check("Stufe 1 ergibt 1 (1*1*1)", P.forschungspunkte({"x": 1}) == 1)
check("Stufe 2 ergibt 8 (2*2*2)", P.forschungspunkte({"x": 2}) == 8)
check("Stufe 3 ergibt 27 (3*3*3)", P.forschungspunkte({"x": 3}) == 27)
check("die Handbuchreihe 0,1,8,27 stimmt",
      [P.forschungspunkte({"x": n}) for n in range(4)] == [0, 1, 8, 27])
check("zwei Gebiete werden addiert (1 + 8 = 9)",
      P.forschungspunkte({"a": 1, "b": 2}) == 9)
check("das Handbuchbeispiel 1 + 64 + 8 ergibt 73",
      P.forschungspunkte({"Felderwirtschaft": 1, "Kriegskunst": 4, "Minenarbeit": 2}) == 73)
check("unbrauchbare Stufen zaehlen als 0",
      P.forschungspunkte({"a": None, "b": "kaputt", "c": 2}) == 8)


# ==========================================================================
# 3. Kriegspunkte — Einheiten
# ==========================================================================

abschnitt("Kriegspunkte — fester Wert je Einheit")

check("10 Paladine geben 160 (16 je Stueck)", P.kriegspunkte({"Paladin": 10}, 0) == 160)
check("12 Bogenschuetzen geben 48 (4 je Stueck)", P.kriegspunkte({"Bogenschütze": 12}, 0) == 48)
check("das Handbuchbeispiel 10 Paladine + 12 Bogenschuetzen ergibt 208",
      P.kriegspunkte({"Paladin": 10, "Bogenschütze": 12}, 0) == 208)
check("ein einzelner Buergerwehr gibt 1", P.kriegspunkte({"Bürgerwehr": 1}, 0) == 1)
check("Siedlerkarren haben keinen Punktewert und geben 0",
      P.kriegspunkte({"Siedlerkarren": 5}, 0) == 0)
check("Handelskarawanen geben 0 (Punktewert: -)",
      P.kriegspunkte({"Handelskarawane": 3}, 0) == 0)
check("unbekannte Einheiten geben 0", P.kriegspunkte({"Gibtsnicht": 9}, 0) == 0)
check("leerer Einheitenstand gibt 0", P.kriegspunkte({}, 0) == 0)


# ==========================================================================
# 4. Kriegspunkte — Verteidigungswall
# ==========================================================================

abschnitt("Kriegspunkte — Verteidigungswall, Ausbaustufe hoch drei")

check("Wallstufe 0 gibt 0", P.kriegspunkte({}, 0) == 0)
check("Wallstufe 3 gibt 27", P.kriegspunkte({}, 3) == 27)
check("Wallstufe 4 gibt 64 (Handbuch)", P.kriegspunkte({}, 4) == 64)
check("Wall und Einheiten werden addiert (64 + 208 = 272)",
      P.kriegspunkte({"Paladin": 10, "Bogenschütze": 12}, 4) == 272)
check("die Wallstufe kommt aus der Wirkungsquelle (wall_kriegspunkte)",
      P.kriegspunkte({}, 4) == 4 ** 3)


# ==========================================================================
# 5. Gesamtpunktzahl — genau die Haelfte
# ==========================================================================

abschnitt("Gesamtpunktzahl — die Summe wird durch zwei geteilt")

check("Handbuchbeispiel: die Formel ist (150 + 200) / 2 = 175",
      P.gesamtpunkte({"a": 4}, {"Ritter": 25}, 0) == (64 + 200) // 2,
      "Formel identisch zum Handbuch; konkrete Zahlen aus verfuegbaren Kuben gewaehlt")
check("Gesamt = (Forschung + Krieg) / 2 bei gerader Summe (64 + 200 = 264 -> 132)",
      P.gesamtpunkte({"a": 4}, {"Ritter": 25}, 0) == 132,
      f"Summe 264, Haelfte 132")
check("Gesamt ist genau die Haelfte der Summe",
      P.gesamtpunkte({"a": 4}, {"Ritter": 25}, 0) == (64 + 200) // 2)
check("Gesamt nutzt die ungerundete Summe beider Quellen",
      P.forschungspunkte({"a": 4}) == 64 and P.kriegspunkte({"Ritter": 25}, 0) == 200)
# Ungerade Summe: 1 + 2 = 3. Wir RUNDEN AB (//2) -> 1. Das ist ein Vorschlag, kein Beleg.
_ungerade = P.gesamtpunkte({"x": 1}, {"Kämpfer": 1}, 0)
check("ungerade Summe (1 + 2 = 3) wird abgerundet auf 1 — als Vorschlag gekennzeichnet",
      _ungerade == 1 and P.vorschlaege()["gesamt_rundung"]["status"] == "VORSCHLAG",
      f"Ergebnis {_ungerade}, Regel: abrunden")
check("ungerade Summe 9 -> 4 (abgerundet)",
      P.gesamtpunkte({"a": 1, "b": 2}, {}, 0) == 4)
check("leere Spielstaende geben Gesamt 0",
      P.gesamtpunkte({}, {}, 0) == 0)


# ==========================================================================
# 6. Rufpunkte
# ==========================================================================

abschnitt("Rufpunkte — eigener Wert, nicht Teil der Gesamtpunktzahl")

check("rufpunkte() gibt den uebergebenen Wert zurueck", P.rufpunkte(42) == 42)
check("rufpunkte(0) ist 0", P.rufpunkte(0) == 0)
check("Ruf veraendert die Gesamtpunktzahl nicht",
      P.gesamtpunkte({"x": 3}, {"Paladin": 1}, 0) == P.gesamtpunkte({"x": 3}, {"Paladin": 1}, 0))
check("Ruf ist im Beleg als getrennter Wert gefuehrt",
      "rufpunkte" in P.belegte_formeln())


# ==========================================================================
# 7. Goetterschutz
# ==========================================================================

abschnitt("Goetterschutz — sieben Tage, dann vorbei")

check("goetterschutz_tage() ist 7 (Handbuch)", P.goetterschutz_tage() == 7)
check("ein neu angemeldeter Spieler ist geschuetzt",
      P.goetterschutz_aktiv(0.0, 0.0) is True)
check("nach einem Tag noch geschuetzt",
      P.goetterschutz_aktiv(0.0, 1 * TAG) is True)
check("kurz vor Ablauf (6 Tage 23 h) noch geschuetzt",
      P.goetterschutz_aktiv(0.0, 7 * TAG - 1) is True)
check("nach genau sieben Tagen ist der Schutz vorbei",
      P.goetterschutz_aktiv(0.0, 7 * TAG) is False)
check("nach sieben Tagen und einer Sekunde ist er vorbei",
      P.goetterschutz_aktiv(0.0, 7 * TAG + 1) is False)
check("ein Start in der Zukunft zaehlt nicht als geschuetzt",
      P.goetterschutz_aktiv(100.0, 50.0) is False)
check("unbrauchbare Zeitstempel gelten als nicht geschuetzt",
      P.goetterschutz_aktiv("x", "y") is False)


# ==========================================================================
# 8. Rangliste
# ==========================================================================

abschnitt("Rangliste — Punkte, dann Ruf, dann frueheres Anmeldedatum")

spieler = [
    {"name": "Alfa", "punkte": 100, "ruf": 5, "angemeldet": 300},
    {"name": "Beta", "punkte": 200, "ruf": 1, "angemeldet": 100},
    {"name": "Gamma", "punkte": 100, "ruf": 9, "angemeldet": 200},
    {"name": "Delta", "punkte": 100, "ruf": 9, "angemeldet": 50},
]
_rang = P.rangliste(spieler)
check("die Rangliste hat so viele Eintraege wie Spieler", len(_rang) == 4, str(len(_rang)))
check("der hoechste Punktwert steht vorn", _rang[0]["name"] == "Beta", _rang[0]["name"])
check("jeder Eintrag traegt name und punkte",
      all("name" in e and "punkte" in e for e in _rang))
check("die Raenge sind fortlaufend ab 1",
      [e["rang"] for e in _rang] == [1, 2, 3, 4], str([e["rang"] for e in _rang]))
check("bei Punktgleichheit steht der hoehere Ruf oben (Delta/Gamma vor Alfa)",
      _rang[1]["name"] == "Delta" and _rang[2]["name"] == "Gamma" and _rang[3]["name"] == "Alfa",
      str([e["name"] for e in _rang]))
check("bei gleichem Ruf entscheidet das fruehere Anmeldedatum (Delta vor Gamma)",
      _rang[1]["angemeldet"] < _rang[2]["angemeldet"])
check("die Punktwerte fallen monoton",
      all(_rang[i]["punkte"] >= _rang[i + 1]["punkte"] for i in range(len(_rang) - 1)))
check("eine leere Rangliste bleibt leer", P.rangliste([]) == [])
check("None als Rangliste ist erlaubt", P.rangliste(None) == [])


# ==========================================================================
# 9. Sieg oder Niederlage — als Vorschlag, ohne Handbuchbehauptung
# ==========================================================================

abschnitt("Sieg/Niederlage — Vorschlag, das Handbuch nennt keine Bedingung")

_z_verlust = {"siedlungen": [], "einheiten": {}, "punkte": 10}
_ergebnis = P.sieg_oder_niederlage(_z_verlust)
check("ohne Siedlung und ohne Einheit ergibt sich Niederlage",
      _ergebnis[0] == "niederlage", str(_ergebnis))
check("die Niederlagebegruendung nennt 'das Handbuch nennt keine Niederlagebedingung'",
      "das Handbuch nennt keine Niederlagebedingung" in _ergebnis[1], _ergebnis[1])
check("die Niederlage ist als VORSCHLAG gekennzeichnet",
      "VORSCHLAG" in _ergebnis[1], _ergebnis[1][:60])

_z_sieg = {"siedlungen": [{"name": "S"}], "einheiten": {"Kämpfer": 1}, "punkte": 300}
_sieg = P.sieg_oder_niederlage(_z_sieg)
check("erreichte Zielpunktzahl ergibt Sieg", _sieg[0] == "sieg", str(_sieg))
check("die Siegbegruendung nennt 'das Handbuch nennt keine Siegbedingung'",
      "das Handbuch nennt keine Siegbedingung" in _sieg[1], _sieg[1])
check("die Siegbegruendung ist als VORSCHLAG gekennzeichnet",
      "VORSCHLAG" in _sieg[1], _sieg[1][:60])

_z_weiter = {"siedlungen": [{"name": "S"}], "einheiten": {"Kämpfer": 1}, "punkte": 5}
_weiter = P.sieg_oder_niederlage(_z_weiter)
check("ein normales Spiel ergibt 'weiter'", _weiter[0] == "weiter", str(_weiter))
check("auch 'weiter' verweist ehrlich auf die fehlende Handbuchregel",
      "das Handbuch nennt keine Siegbedingung" in _weiter[1], _weiter[1])

check("kein Ergebnis behauptet, belegt zu sein",
      all("BELEGT" not in P.sieg_oder_niederlage(z)[1]
          for z in (_z_verlust, _z_sieg, _z_weiter)))
check("das Ergebnis ist immer einer von sieg/niederlage/weiter",
      all(P.sieg_oder_niederlage(z)[0] in ("sieg", "niederlage", "weiter")
          for z in (_z_verlust, _z_sieg, _z_weiter)))
check("eine eigene Zielpunktzahl wird beachtet",
      P.sieg_oder_niederlage({"siedlungen": [{}], "einheiten": {"Kämpfer": 1},
                              "punkte": 50, "ziel_punkte": 50})[0] == "sieg")
check("Sieg ist kein belegter Begriff im Handbuchbeleg-Verzeichnis",
      "sieg" not in [k.lower() for k in P.belegte_formeln()])


sys.exit(bericht())
