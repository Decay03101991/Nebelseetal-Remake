# -*- coding: ascii -*-
"""Pruefung des lokalen Forschungsstarts und -abschlusses je Siedlung.

Gegenstand sind die NEUEN Funktionen in src/spieloekonomie.py:
  forschung_start(ort, gebiet, wissen, jetzt, weitere_orte=())  -> neuer Ort (ValueError)
  forschung_abschluss(ort, wissen, jetzt)                        -> (neuer Ort, neues wissen)

Richtschnur sind die Pflichtzusagen aus
docs/audits/entwurf_spieloekonomie_sol_2026-10-05.txt, Zeile 650-686, woertlich:
  'zweite Forschung in derselben Bibliothek abgelehnt, in zweiter Bibliothek anderes Gebiet
   erlaubt; ... Adapter muss ausserdem gleichzeitige Forschung derselben Zielstufe in
   verschiedenen Staedten verhindern, sonst doppelte Kosten ohne Wissensgewinn'.

Belegte Regeln (forschung.kosten / forschung.dauer_stunden):
  Stufe 1 = 50 Holz, Dauer = Stufe zum Quadrat in Stunden, Stufe 1 also 1 h = 3600 s.
Die Gebiete werden ueber forschungspfad.erfuellt selbst nachgeschlagen; eine Voraussetzung
gilt als erfuellt, wenn erfuellt(...) True meldet, sonst als gesperrt.

Die Orte werden in dieser Datei selbst als dicts erzeugt. Jede Zusage nennt bei Verletzung
Soll und Ist.

Aufruf:  python -X utf8 tests/test_lokale_forschung.py
"""
from __future__ import annotations

import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

ROOT, SRC = import_src()
import spieloekonomie as O
import forschung
import forschungspfad

# --------------------------------------------------------------------------- Gebiete
# Alle Namen sind ASCII; die Auswahl stammt aus einer Abfrage von
# forschungspfad.erfuellt(name, {}, bibliothek=1).
GEBIET_A = "Baukunst"          # erfuellbar ab Bibliothek 1
GEBIET_B = "Heimlichkeit"      # anderes erfuellbares Gebiet
GEBIET_C = "Bogenbau"          # drittes erfuellbares Gebiet
GEBIET_GESPERRT = "Waffentechnik"   # gesperrt: Bibliothek 3 + Schmiedekunst 1

START = 1000                   # jetzt in Sekunden
KOSTEN_STUFE_1 = 50            # Holz, aus forschung.kosten(1)


# --------------------------------------------------------------------------- Hilfen
def ort(oid, bauten=None, stufen=None, vorraete=None, forschungsauftrag=None,
        bevoelkerung=5.0):
    """Ein Siedlungs-Ort mit allen Feldern, die forschung_start/-abschluss erwarten."""
    return {
        "id": oid,
        "besitzer": "spieler",
        "dimension": 0,
        "x": 0,
        "y": 0,
        "map_id": "karte1",
        "karte": {"raster": ["wald"]},
        "bauten": dict(bauten) if bauten else {},
        "stufen": dict(stufen) if stufen else {},
        "vorraete": dict(vorraete) if vorraete is not None else {"holz": 500.0},
        "waren": {},
        "einheiten": {},
        "bevoelkerung": bevoelkerung,
        "importiert": {},
        "verbrauchsjournal": [],
        "produktionsjournal": [],
        "fertigjournal": [],
        "werkstaetten": {},
        "ausbildung": [],
        "forschungsauftrag": forschungsauftrag,
    }


def bibliothek_ort(oid, vorraete=None, forschungsauftrag=None):
    """Ort mit genau EINER Bibliothek Stufe 1 (bauten-Feld 0, stufen-Feld 0 = 1)."""
    return ort(oid, bauten={"0": "bibliothek"}, stufen={"0": 1},
               vorraete=vorraete, forschungsauftrag=forschungsauftrag)


def value_fehler(fn):
    """Fuehrt fn aus; liefert (war_es_ValueError, Nachricht)."""
    try:
        fn()
    except ValueError as e:
        return True, str(e)
    except Exception as e:  # noqa: BLE001
        return False, "FALSCHE_AUSNAHME " + type(e).__name__ + ": " + str(e)
    return False, "keine Ausnahme"


def lauf(fn):
    """Fuehrt fn aus; liefert (Ausnahme_oder_None, Ergebnis_oder_None)."""
    try:
        return None, fn()
    except Exception as e:  # noqa: BLE001
        return e, None


# ==========================================================================
abschnitt("1. ERFOLG: Gebiet mit erfuellten Voraussetzungen startet")

o = bibliothek_ort("A", vorraete={"holz": 500.0})
wissen = {}
neu = O.forschung_start(o, GEBIET_A, wissen, START)
a = neu.get("forschungsauftrag") or {}
check("1a der zurueckgegebene Ort traegt einen forschungsauftrag",
      isinstance(neu.get("forschungsauftrag"), dict), str(neu.get("forschungsauftrag")))
check("1b gebiet == " + GEBIET_A, a.get("gebiet") == GEBIET_A,
      "Ist " + str(a.get("gebiet")))
check("1c zielstufe == 1", a.get("zielstufe") == 1, "Ist " + str(a.get("zielstufe")))
check("1d startzeit == " + str(START), a.get("startzeit") == START,
      "Ist " + str(a.get("startzeit")))
check("1e dauer_stunden == 1", a.get("dauer_stunden") == 1,
      "Ist " + str(a.get("dauer_stunden")))
check("1f kosten == {'holz': 50}", a.get("kosten") == {"holz": KOSTEN_STUFE_1},
      "Ist " + str(a.get("kosten")))
check("1g genau diese fuenf Felder: gebiet, zielstufe, startzeit, dauer_stunden, kosten",
      set(a.keys()) == {"gebiet", "zielstufe", "startzeit", "dauer_stunden", "kosten"},
      "Ist " + str(sorted(a.keys())))


# ==========================================================================
abschnitt("2. KOSTEN GENAU EINMAL: Vorrat sinkt um genau sum(kosten)")

o = bibliothek_ort("A2", vorraete={"holz": 500.0})
wissen = {}
neu = O.forschung_start(o, GEBIET_A, wissen, START)
kosten = neu["forschungsauftrag"]["kosten"]
summe = sum(kosten.values())
vorher = 500.0
nachher = neu["vorraete"]["holz"]
check("2a sum(kosten) ist genau 50 (Stufe 1)", summe == 50,
      "Ist " + str(summe))
check("2b Holz VORHER ist 500.0 (eigene Zahl)", vorher == 500.0,
      "Ist " + str(vorher))
check("2c Holz NACHHER ist genau 450.0", nachher == 450.0,
      "Ist " + str(nachher))
check("2d die Abnahme ist genau sum(kosten) = 50", vorher - nachher == summe,
      "Abnahme " + str(vorher - nachher) + " Soll " + str(summe))


# ==========================================================================
abschnitt("3. ZWEITE FORSCHUNG IN DERSELBEN BIBLIOTHEK WIRD ABGELEHNT")

o = bibliothek_ort("A3", vorraete={"holz": 500.0})
neu = O.forschung_start(o, GEBIET_A, {}, START)
vorrat_vorher = dict(neu["vorraete"])
ok, t = value_fehler(lambda: O.forschung_start(neu, GEBIET_B, {}, START))
check("3a der zweite forschung_start wirft ValueError", ok, t)
check("3b der Vorrat bleibt unveraendert (450.0)", neu["vorraete"] == vorrat_vorher,
      "Ist " + str(neu["vorraete"]) + " Soll " + str(vorrat_vorher))
check("3c die Meldung nennt die laufende Bibliothek",
      "Bibliothek" in t or "forscht bereits" in t, t)


# ==========================================================================
abschnitt("4. ZWEITES GEBIET IN ZWEITER BIBLIOTHEK IST ERLAUBT")

erst = bibliothek_ort("B1", vorraete={"holz": 500.0})
erst = O.forschung_start(erst, GEBIET_A, {}, START)
zweit = bibliothek_ort("B2", vorraete={"holz": 500.0})
err, neu2 = lauf(lambda: O.forschung_start(zweit, GEBIET_B, {}, START,
                                           weitere_orte=[erst]))
check("4a ein anderes Gebiet in eigener Bibliothek wirft KEINEN Fehler",
      err is None, repr(err))
check("4b der zweite Ort hat einen Auftrag fuer " + GEBIET_B,
      bool(neu2) and neu2.get("forschungsauftrag", {}).get("gebiet") == GEBIET_B,
      str(neu2.get("forschungsauftrag") if neu2 else None))


# ==========================================================================
abschnitt("5. GLEICHE ZIELSTUFE IN ZWEITER STADT WIRD ABGELEHNT (Entwurf Z. 685)")

erst = bibliothek_ort("C1", vorraete={"holz": 500.0})
erst = O.forschung_start(erst, GEBIET_A, {}, START)
# Gleiches Gebiet, gleiche Zielstufe (1), zweite Stadt, erster Ort gemeldet:
zweit = bibliothek_ort("C2", vorraete={"holz": 500.0})
ok, t = value_fehler(lambda: O.forschung_start(zweit, GEBIET_A, {}, START,
                                               weitere_orte=[erst]))
check("5a gleiches Gebiet + gleiche Zielstufe in zweiter Stadt -> ValueError", ok, t)
# MIT einem anderen Gebiet wird es NICHT abgelehnt:
zweit2 = bibliothek_ort("C3", vorraete={"holz": 500.0})
err, neu3 = lauf(lambda: O.forschung_start(zweit2, GEBIET_C, {}, START,
                                           weitere_orte=[erst]))
check("5b mit einem ANDEREN Gebiet wird es NICHT abgelehnt", err is None, repr(err))
check("5c der dritte Ort hat einen Auftrag fuer " + GEBIET_C,
      bool(neu3) and neu3.get("forschungsauftrag", {}).get("gebiet") == GEBIET_C,
      str(neu3.get("forschungsauftrag") if neu3 else None))


# ==========================================================================
abschnitt("6. OHNE BIBLIOTHEK ABGELEHNT (Meldung nennt die Bibliothek)")

ohne = ort("D", bauten={"0": "holzfaeller"}, vorraete={"holz": 500.0})
ok, t = value_fehler(lambda: O.forschung_start(ohne, GEBIET_A, {}, START))
check("6a ein Ort ohne Bibliothek wird abgelehnt", ok, t)
check("6b die Meldung nennt die Bibliothek", "Bibliothek" in t, t)


# ==========================================================================
abschnitt("7. UNBEKANNTES GEBIET ABGELEHNT")

o = bibliothek_ort("E", vorraete={"holz": 500.0})
ok, t = value_fehler(lambda: O.forschung_start(o, "Gibtsnicht", {}, START))
check("7a ein unbekanntes Gebiet wird abgelehnt", ok, t)
check("7b die Meldung nennt 'Unbekannt'", "Unbekannt" in t, t)


# ==========================================================================
abschnitt("8. GESPERRTE VORAUSSETZUNG ABGELEHNT (Meldung nennt Soll und Ist)")

o = bibliothek_ort("F", vorraete={"holz": 500.0})
frei, grund = forschungspfad.erfuellt(GEBIET_GESPERRT, {}, 1)
check("8a Vorbedingung: erfuellt meldet das Gebiet als NICHT erfuellt", not frei, grund)
ok, t = value_fehler(lambda: O.forschung_start(o, GEBIET_GESPERRT, {}, START))
check("8b forschung_start lehnt es ab", ok, t)
check("8c die Meldung nennt Soll und Ist (Bibliothek 3/1)", "Bibliothek 3" in t, t)
check("8d die Meldung nennt Soll und Ist (Schmiedekunst 0/1)", "Schmiedekunst" in t, t)
check("8e die Meldung ist die Begruendung von forschungspfad.erfuellt", t == grund,
      "Ist " + repr(t) + " Soll " + repr(grund))


# ==========================================================================
abschnitt("9. ABSCHLUSS ZUR RICHTIGEN ZEIT (startzeit + dauer*3600 = Grenze)")

o = bibliothek_ort("G", vorraete={"holz": 500.0})
wissen = {}
neu = O.forschung_start(o, GEBIET_A, wissen, START)
a = neu["forschungsauftrag"]
ende = a["startzeit"] + a["dauer_stunden"] * 3600
check("9a die Grenze ist startzeit + dauer_stunden*3600 = 4600", ende == 4600,
      "Ist " + str(ende))
neu_ende, kenntnis = O.forschung_abschluss(neu, wissen, ende)
check("9b bei genau der Grenze steigt die Stufe auf zielstufe",
      kenntnis.get(GEBIET_A) == a["zielstufe"] == 1,
      "Ist " + str(kenntnis.get(GEBIET_A)) + " Soll " + str(a["zielstufe"]))
check("9c der Auftrag ist danach None", neu_ende["forschungsauftrag"] is None,
      str(neu_ende["forschungsauftrag"]))
fj = [e for e in neu_ende["fertigjournal"] if e.get("art") == "forschung"]
check("9d im fertigjournal steht ein Eintrag mit art 'forschung'", len(fj) == 1,
      str(neu_ende["fertigjournal"]))
check("9e der Eintrag nennt das Gebiet " + GEBIET_A,
      len(fj) == 1 and fj[0].get("name") == GEBIET_A, str(fj))
check("9f der Eintrag traegt die Abschlusszeit", len(fj) == 1 and fj[0].get("zeit") == ende,
      str(fj))


# ==========================================================================
abschnitt("10. ZU FRUEH PASSIERT NICHTS (eine Sekunde davor)")

o = bibliothek_ort("H", vorraete={"holz": 500.0})
wissen = {}
neu = O.forschung_start(o, GEBIET_A, wissen, START)
ende = neu["forschungsauftrag"]["startzeit"] + \
    neu["forschungsauftrag"]["dauer_stunden"] * 3600
neu_vor, kenntnis_vor = O.forschung_abschluss(neu, wissen, ende - 1)
check("10a eine Sekunde davor bleibt wissen unveraendert", kenntnis_vor == wissen,
      "Ist " + str(kenntnis_vor) + " Soll " + str(wissen))
check("10b der Auftrag steht noch", neu_vor["forschungsauftrag"] is not None,
      str(neu_vor["forschungsauftrag"]))
check("10c es gibt noch keinen fertigjournal-Eintrag", neu_vor["fertigjournal"] == [],
      str(neu_vor["fertigjournal"]))


# ==========================================================================
abschnitt("11. ZWEIMAL ABSCHLIESSEN DOPPELT NICHTS")

o = bibliothek_ort("I", vorraete={"holz": 500.0})
wissen = {}
neu = O.forschung_start(o, GEBIET_A, wissen, START)
ende = neu["forschungsauftrag"]["startzeit"] + \
    neu["forschungsauftrag"]["dauer_stunden"] * 3600
neu_ende, kenntnis = O.forschung_abschluss(neu, wissen, ende)
neu2, kenntnis2 = O.forschung_abschluss(neu_ende, kenntnis, ende + 3600)
check("11a die Stufe ist nach dem zweiten Abschluss gleich (kein Aufstieg)",
      kenntnis2.get(GEBIET_A) == 1, "Ist " + str(kenntnis2.get(GEBIET_A)))
check("11b kein Fehler und der Auftrag bleibt None", neu2["forschungsauftrag"] is None,
      str(neu2["forschungsauftrag"]))
check("11c das fertigjournal hat weiterhin genau EINEN forschung-Eintrag",
      len([e for e in neu2["fertigjournal"] if e.get("art") == "forschung"]) == 1,
      str(neu2["fertigjournal"]))


# ==========================================================================
abschnitt("12. DER URSPRUNGSORT BLEIBT UNBERUEHRT (kein stiller Seiteneffekt)")

o = bibliothek_ort("J", vorraete={"holz": 500.0})
kopie = copy.deepcopy(o)
_ = O.forschung_start(o, GEBIET_A, {}, START)
check("12a forschung_start veraendert das uebergebene dict NICHT", o == kopie,
      "Urspruengs-Ort weicht ab")
check("12b im Urspruengs-Ort steht kein forschungsauftrag", o["forschungsauftrag"] is None,
      str(o["forschungsauftrag"]))
check("12c der Vorrat im Urspruengs-Ort bleibt 500.0", o["vorraete"] == {"holz": 500.0},
      str(o["vorraete"]))

o2 = bibliothek_ort("K", vorraete={"holz": 500.0})
neu = O.forschung_start(o2, GEBIET_A, {}, START)
kopie2 = copy.deepcopy(neu)
wissen2 = {}
_ = O.forschung_abschluss(neu, wissen2, START + 3600)
check("12d forschung_abschluss veraendert das uebergebene dict NICHT", neu == kopie2,
      "Urspruengs-Ort weicht ab")
check("12e der Auftrag im Urspruengs-Ort steht weiter", neu["forschungsauftrag"] is not None,
      str(neu["forschungsauftrag"]))


# ==========================================================================
abschnitt("13. STUFE STEIGT BEIM START NICHT")

o = bibliothek_ort("L", vorraete={"holz": 500.0})
wissen = {}
neu = O.forschung_start(o, GEBIET_A, wissen, START)
check("13a die Stufe im wissen ist direkt nach dem Start noch die alte (0)",
      wissen.get(GEBIET_A, 0) == 0, "Ist " + str(wissen.get(GEBIET_A, 0)))
check("13b das uebergebene wissen-dict bleibt leer/alt", wissen == {},
      str(wissen))


sys.exit(bericht())
