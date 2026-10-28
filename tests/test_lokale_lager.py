# -*- coding: ascii -*-
"""Pruefung der lokalen Lager und Transportbuchung (Schritt 3 der Spieloekonomie).

Gegenstand sind die NEUEN Funktionen in src/spieloekonomie.py:
  verbrauchen, transport_start, transport_fortschritt, station_start.

Geprueft werden die acht Pflichtzusagen aus
docs/audits/entwurf_spieloekonomie_sol_2026-10-05.txt, Zeile 505:
  1. Verbrauch zieht genau die Kosten, begrenzt aufs lokale Lager, Journal anteilig.
  2. Startpruefungen (Besitzer, Dimension, Ausgangsgarnison, Karrenpflicht, Fracht).
  3. Gute Fahrt: genaue Abbuchung, Ankunft genau einmal, Rueckkehr, kein Doppelbuchen.
  4. Zielverlust: Fracht bleibt am Auftrag, volle Rueckgabe an den Ausgangsort.
  5. Ausgangsort verloren: Ersatzsiedlung oder Fracht bleibt am Auftrag (beide Faelle).
  6. Stationieren: Einheiten bleiben am Ziel und kommen NICHT zurueck.
  7. Speichern/Laden mitten im Auftrag (JSON) bucht weiterhin genau einmal.
  8. Es entsteht und verschwindet kein Rohstoff.

Aufruf:  python -X utf8 tests/test_lokale_lager.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

ROOT, SRC = import_src()
import spieloekonomie as O


# --------------------------------------------------------------------------- Hilfen
def ort(oid, besitzer="spieler", dimension=0, x=0, y=0,
        vorraete=None, waren=None, einheiten=None, importiert=None, journal=None):
    """Ein Siedlungs-Ort mit allen Feldern, die die Transportfunktionen erwarten."""
    return {
        "id": oid,
        "besitzer": besitzer,
        "dimension": dimension,
        "x": x,
        "y": y,
        "vorraete": dict(vorraete) if vorraete is not None else {"holz": 100.0},
        "waren": dict(waren) if waren is not None else {},
        "einheiten": dict(einheiten) if einheiten is not None else {"Handkarren": 2},
        "importiert": dict(importiert) if importiert is not None else {"holz": 0.0},
        "verbrauchsjournal": list(journal) if journal is not None else [],
    }


def paar():
    """Zwei eigene Siedlungen mit je zwei Handkarren, Abstand 5 (>0)."""
    return ort("A"), ort("B", x=5)


def value_fehler(fn):
    """Fuehrt fn aus; liefert (war_es_ValueError, Nachricht)."""
    try:
        fn()
    except ValueError as e:
        return True, str(e)
    except Exception as e:  # noqa: BLE001
        return False, "FALSCHE_AUSNAHME " + type(e).__name__ + ": " + str(e)
    return False, "keine Ausnahme"


# ==========================================================================
abschnitt("1. verbrauchen: lokale Kosten, Importanteil, Verbrauchsjournal")

# importiert 50 von 100 Holz, Kosten 10 Holz -> Journalmenge 5.0, importiert 45, vorraete 90
v = ort("V", vorraete={"holz": 100}, importiert={"holz": 50})
nv = O.verbrauchen(v, {"holz": 10}, 1234.0)
check("verbrauchen senkt den Bestand genau um die Kosten (100 -> 90)",
      nv["vorraete"]["holz"] == 90, str(nv["vorraete"]["holz"]))
check("verbrauchen senkt den importierten Anteil um 5.0 (50 -> 45)",
      nv["importiert"]["holz"] == 45.0, str(nv["importiert"]["holz"]))
check("das Verbrauchsjournal bekommt genau eine Zeile",
      len(nv["verbrauchsjournal"]) == 1, str(nv["verbrauchsjournal"]))
zeile = nv["verbrauchsjournal"][0]
check("die Journalmenge ist anteilig 5.0", abs(zeile["menge"] - 5.0) < 1e-9, str(zeile))
check("das Journal nennt Rohstoff, Zeit und Herkunftsort",
      zeile["rohstoff"] == "holz" and zeile["zeit"] == 1234.0 and zeile["ziel"] == "V",
      str(zeile))
check("die Vorlage bleibt unveraendert (reine Funktion)",
      v["vorraete"]["holz"] == 100 and v["importiert"]["holz"] == 50
      and v["verbrauchsjournal"] == [], str(v))

# importiert 0 -> keine Journalzeile
v0 = ort("V0", vorraete={"holz": 100}, importiert={"holz": 0})
n0 = O.verbrauchen(v0, {"holz": 10}, 5.0)
check("bei importiert 0 entsteht KEINE Journalzeile",
      n0["verbrauchsjournal"] == [] and n0["vorraete"]["holz"] == 90,
      str(n0["verbrauchsjournal"]))

# Lager reicht nicht
v1 = ort("V1", vorraete={"holz": 100}, importiert={"holz": 50})
ok_v, t_v = value_fehler(lambda: O.verbrauchen(v1, {"holz": 150}, 0.0))
check("ein zu kleines lokales Lager wird als ValueError abgelehnt",
      ok_v and "Lager" in t_v, t_v)


# ==========================================================================
abschnitt("2. transport_start: jede Ablehnung einzeln")

# 2a fremder Besitzer
a, b = paar()
b["besitzer"] = "bot"
ok, t = value_fehler(lambda: O.transport_start(a, b, {"Handkarren": 1}, {}, 0.0))
check("2a fremder Besitzer -> ValueError", ok, t)

# 2b verschiedene Dimension
a, b = paar()
b["dimension"] = 1
ok, t = value_fehler(lambda: O.transport_start(a, b, {"Handkarren": 1}, {}, 0.0))
check("2b verschiedene Dimension -> ValueError", ok, t)

# 2c Einheiten nicht am Ausgangsort
a, b = paar()
ok, t = value_fehler(lambda: O.transport_start(a, b, {"Handkarren": 3}, {}, 0.0))
check("2c Einheiten nicht am Ausgangsort -> ValueError",
      ok and "Ausgangsort" in t, t)

# 2d Nicht-Karren-Einheit (Krieger): Karrenpflicht ist BELEGT (Handbuch S. 23)
a, b = paar()
a["einheiten"]["Krieger"] = 1
ok, t = value_fehler(lambda: O.transport_start(a, b, {"Krieger": 1}, {}, 0.0))
check("2d Nicht-Karren-Einheit (Krieger) -> ValueError mit dem Text 'Karren'",
      ok and "Karren" in t, t)

# 2e negative Fracht
a, b = paar()
ok, t = value_fehler(lambda: O.transport_start(a, b, {"Handkarren": 1}, {"holz": -5}, 0.0))
check("2e negative Fracht -> ValueError", ok, t)

# 2f unbekannter Rohstoff im Rohstoffkanal
a, b = paar()
ok, t = value_fehler(lambda: O.transport_start(a, b, {"Handkarren": 1},
                                               {"unbekannt": 1}, 0.0))
check("2f unbekannter Rohstoff im Rohstoffkanal -> ValueError", ok, t)

# 2g zu wenig Fracht im Lager (Fracht passt auf die Karren, Lager deckt sie nicht)
a, b = paar()
a["vorraete"] = {"holz": 30}
a["importiert"] = {"holz": 0}
ok, t = value_fehler(lambda: O.transport_start(a, b, {"Handkarren": 2},
                                               {"holz": 50}, 0.0))
check("2g zu wenig Fracht im Lager -> ValueError", ok and "fehlt" in t, t)

# 2h Ueberladung ueber die Ladung (2 Handkarren = 80)
a, b = paar()
ok, t = value_fehler(lambda: O.transport_start(a, b, {"Handkarren": 2},
                                               {"holz": 90}, 0.0))
check("2h Ueberladung ueber die Ladung (2 x 40) -> ValueError",
      ok and "Ueberladen" in t, t)

# eine Ablehnung bucht nichts halb
a, b = paar()
b["dimension"] = 1
O_ok = value_fehler(lambda: O.transport_start(a, b, {"Handkarren": 1}, {"holz": 20}, 0.0))[0]
check("eine Ablehnung laesst die Quelle unveraendert",
      O_ok and a["vorraete"]["holz"] == 100 and a["einheiten"]["Handkarren"] == 2,
      str(a))


# ==========================================================================
abschnitt("3. gute Fahrt: Abbuchung, Ankunft, Rueckkehr, kein Doppelbuchen")

a, b = paar()
fracht = {"holz": 20}
jetzt = 1000.0
qa, m = O.transport_start(a, b, {"Handkarren": 1}, fracht, jetzt)
check("Quelle verliert genau die Fracht (100 -> 80)", qa["vorraete"]["holz"] == 80,
      str(qa["vorraete"]["holz"]))
check("Quelle verliert genau einen Karren (2 -> 1)", qa["einheiten"]["Handkarren"] == 1,
      str(qa["einheiten"]))
check("die Mission ist ein eigentransport", m.get("eigentransport") is True,
      str(m.get("eigentransport")))
check("die Mission traegt genau die Fracht", m["fracht"] == {"holz": 20},
      str(m["fracht"]))
check("der Frachtkanal ist vorraete", m["frachtkanal"] == "vorraete", str(m["frachtkanal"]))
check("Quelle und Ziel bleiben unveraendert (reine Funktion)",
      a["vorraete"]["holz"] == 100 and a["einheiten"]["Handkarren"] == 2
      and b["vorraete"]["holz"] == 100, str(a))

check("Ankunft liegt eine Strecke spaeter (5/10 h = 1800 s)",
      m["ankunft"] == jetzt + 1800.0, str(m["ankunft"]))
check("Rueckkehr liegt zwei Strecken spaeter (3600 s)",
      m["rueckkehr"] == jetzt + 3600.0, str(m["rueckkehr"]))

o1, m1 = O.transport_fortschritt(m, {"A": qa, "B": b}, m["ankunft"])
check("Ankunft: das Ziel bekommt die Fracht genau einmal (100 -> 120)",
      o1["B"]["vorraete"]["holz"] == 120, str(o1["B"]["vorraete"]["holz"]))
check("Ankunft: die gelieferte Fracht wird als importiert gefuehrt (0 -> 20)",
      o1["B"]["importiert"]["holz"] == 20, str(o1["B"]["importiert"]))
check("Ankunft: die Fracht ist am Auftrag leer", m1["fracht"] == {}, str(m1["fracht"]))
check("Ankunft: der Merker geliefert_lokal ist gesetzt",
      m1.get("geliefert_lokal") is True, str(m1.get("geliefert_lokal")))
check("Ankunft: der Ausgangsort bleibt unveraendert (80)",
      o1["A"]["vorraete"]["holz"] == 80, str(o1["A"]["vorraete"]))

o2, m2 = O.transport_fortschritt(m1, o1, m["ankunft"])
check("zweiter Aufruf zur Ankunftszeit bucht NICHTS doppelt (Ziel bleibt 120)",
      o2["B"]["vorraete"]["holz"] == 120 and o2["B"]["importiert"]["holz"] == 20,
      str(o2["B"]["vorraete"]))
check("zweiter Aufruf laesst die Fracht leer", m2["fracht"] == {}, str(m2["fracht"]))

o3, m3 = O.transport_fortschritt(m2, o2, m["rueckkehr"])
check("Rueckkehr: die Einheiten sind wieder am Ausgangsort (1 -> 2)",
      o3["A"]["einheiten"]["Handkarren"] == 2, str(o3["A"]["einheiten"]))
check("Rueckkehr: die Fracht ist leer (sie wurde geliefert)", m3["fracht"] == {},
      str(m3["fracht"]))
check("Rueckkehr: kein Rohstoff springt zum Ausgangsort zurueck (bleibt 80)",
      o3["A"]["vorraete"]["holz"] == 80, str(o3["A"]["vorraete"]))
check("Rueckkehr: der Merker heimgekehrt_lokal ist gesetzt",
      m3.get("heimgekehrt_lokal") is True, str(m3.get("heimgekehrt_lokal")))

o4, m4 = O.transport_fortschritt(m3, o3, m["rueckkehr"])
check("zweiter Aufruf zur Rueckkehrzeit verdoppelt die Einheiten NICHT (bleibt 2)",
      o4["A"]["einheiten"]["Handkarren"] == 2, str(o4["A"]["einheiten"]))


# ==========================================================================
abschnitt("4. Zielverlust: Fracht bleibt am Auftrag, volle Rueckgabe")

# 4a Ziel beim Ankunftszeitpunkt fremd
a, b = paar()
qa, m = O.transport_start(a, b, {"Handkarren": 1}, {"holz": 30}, 0.0)
b_fremd = dict(b)
b_fremd["besitzer"] = "bot"
o1, m1 = O.transport_fortschritt(m, {"A": qa, "B": b_fremd}, m["ankunft"])
check("4a fremdes Ziel: keine Gutschrift (Ziel bleibt 100)",
      o1["B"]["vorraete"]["holz"] == 100, str(o1["B"]["vorraete"]))
check("4a fremdes Ziel: keine Geistergutschrift als importiert",
      o1["B"]["importiert"]["holz"] == 0, str(o1["B"]["importiert"]))
check("4a fremdes Ziel: die Fracht bleibt an der Mission",
      m1["fracht"] == {"holz": 30}, str(m1["fracht"]))
o2, m2 = O.transport_fortschritt(m1, o1, m["rueckkehr"])
check("4a Zielverlust: die Fracht kommt VOLL zum Ausgangsort zurueck (70 -> 100)",
      o2["A"]["vorraete"]["holz"] == 100, str(o2["A"]["vorraete"]))
check("4a Zielverlust: die Einheiten sind wieder am Ausgangsort (1 -> 2)",
      o2["A"]["einheiten"]["Handkarren"] == 2, str(o2["A"]["einheiten"]))
check("4a Zielverlust: keine Fracht bleibt am Auftrag", m2["fracht"] == {}, str(m2["fracht"]))

# 4b Ziel fehlt ganz
a, b = paar()
qa, m = O.transport_start(a, b, {"Handkarren": 1}, {"holz": 30}, 0.0)
o1, m1 = O.transport_fortschritt(m, {"A": qa}, m["ankunft"])
check("4b fehlendes Ziel: die Fracht bleibt an der Mission",
      m1["fracht"] == {"holz": 30}, str(m1["fracht"]))
o2, m2 = O.transport_fortschritt(m1, o1, m["rueckkehr"])
check("4b fehlendes Ziel: volle Rueckgabe an den Ausgangsort (70 -> 100)",
      o2["A"]["vorraete"]["holz"] == 100, str(o2["A"]["vorraete"]))


# ==========================================================================
abschnitt("5. Ausgangsort verloren: Ersatzsiedlung oder Fracht bleibt")

# 5a Ersatzsiedlung vorhanden (Ausgangsort erobert, Ziel ebenfalls nicht mehr eigen)
a, b = paar()
c = ort("C")
qa, m = O.transport_start(a, b, {"Handkarren": 1}, {"holz": 30}, 0.0)
qa_verloren = dict(qa)
qa_verloren["besitzer"] = "bot"
b_fremd = dict(b)
b_fremd["besitzer"] = "bot"
o1, m1 = O.transport_fortschritt(m, {"A": qa_verloren, "B": b_fremd, "C": c},
                                 m["rueckkehr"])
check("5a Ausgangsort erobert: eine eigene Ersatzsiedlung wird gesucht (C)",
      m1.get("ersatzort") == "C", str(m1.get("ersatzort")))
check("5a die Ersatzsiedlung bekommt die Fracht (100 -> 130)",
      o1["C"]["vorraete"]["holz"] == 130, str(o1["C"]["vorraete"]))
check("5a die Ersatzsiedlung bekommt die Einheiten (2 -> 3)",
      o1["C"]["einheiten"]["Handkarren"] == 3, str(o1["C"]["einheiten"]))
check("5a die Fracht ist danach leer", m1["fracht"] == {}, str(m1["fracht"]))

# 5b keine Ersatzsiedlung: Fracht und Einheiten bleiben an der Mission
a, b = paar()
qa, m = O.transport_start(a, b, {"Handkarren": 1}, {"holz": 30}, 0.0)
qa_verloren = dict(qa)
qa_verloren["besitzer"] = "bot"
b_fremd = dict(b)
b_fremd["besitzer"] = "bot"
o1, m1 = O.transport_fortschritt(m, {"A": qa_verloren, "B": b_fremd}, m["rueckkehr"])
check("5b ohne Ersatzsiedlung bleibt die Fracht an der Mission",
      m1["fracht"] == {"holz": 30}, str(m1["fracht"]))
check("5b ohne Ersatzsiedlung bleiben auch die Einheiten an der Mission",
      m1["einheiten"] == {"Handkarren": 1}, str(m1["einheiten"]))
check("5b kein Ersatzort wird erfunden", m1.get("ersatzort") is None,
      str(m1.get("ersatzort")))
check("5b die fremden Siedlungen bekommen nichts (B bleibt 100)",
      o1["B"]["vorraete"]["holz"] == 100, str(o1["B"]["vorraete"]))


# ==========================================================================
abschnitt("6. station_start: Einheiten bleiben am Ziel")

a, b = paar()
qa, m = O.station_start(a, b, {"Handkarren": 1}, {"holz": 10}, 0.0)
check("station_start setzt stationieren_lokal",
      m.get("stationieren_lokal") is True, str(m.get("stationieren_lokal")))
check("station_start ist ebenfalls ein eigentransport",
      m.get("eigentransport") is True, str(m.get("eigentransport")))
check("Quelle verliert Fracht und Karren (90 / 1)",
      qa["vorraete"]["holz"] == 90 and qa["einheiten"]["Handkarren"] == 1, str(qa))

o1, m1 = O.transport_fortschritt(m, {"A": qa, "B": b}, m["ankunft"])
check("Ankunft: die Fracht kommt am Ziel an (100 -> 110)",
      o1["B"]["vorraete"]["holz"] == 110, str(o1["B"]["vorraete"]))
check("Ankunft: die Einheiten stehen am ZIEL (2 -> 3)",
      o1["B"]["einheiten"]["Handkarren"] == 3, str(o1["B"]["einheiten"]))
check("Ankunft: die Mission fuehrt keine Einheiten mehr", m1["einheiten"] == {},
      str(m1["einheiten"]))

o2, m2 = O.transport_fortschritt(m1, o1, m["rueckkehr"])
check("Rueckkehr: die Einheiten sind NICHT wieder am Ausgangsort (bleibt 1)",
      o2["A"]["einheiten"]["Handkarren"] == 1, str(o2["A"]["einheiten"]))
check("Rueckkehr: das Ziel behaelt die stationierten Einheiten (bleibt 3)",
      o2["B"]["einheiten"]["Handkarren"] == 3, str(o2["B"]["einheiten"]))


# ==========================================================================
abschnitt("7. Speichern/Laden mitten im Auftrag")

a, b = paar()
qa, m = O.transport_start(a, b, {"Handkarren": 1}, {"holz": 20}, 0.0)
text = json.dumps(m)                      # muss ohne Ausnahme gehen
m_l = json.loads(text)
check("die Mission ist JSON-faehig (dumps/loads ohne Ausnahme)",
      isinstance(m_l, dict) and isinstance(text, str), text[:60])
check("nach dem Laden stimmen ankunft und rueckkehr",
      m_l["ankunft"] == m["ankunft"] and m_l["rueckkehr"] == m["rueckkehr"], str(m_l["ankunft"]))
check("nach dem Laden stimmen fracht und frachtkanal",
      m_l["fracht"] == {"holz": 20} and m_l["frachtkanal"] == "vorraete", str(m_l["fracht"]))

o1, m1 = O.transport_fortschritt(m_l, {"A": qa, "B": b}, m_l["ankunft"])
check("nach dem Laden bucht die Ankunft weiterhin genau einmal (100 -> 120)",
      o1["B"]["vorraete"]["holz"] == 120, str(o1["B"]["vorraete"]))
o2, m2 = O.transport_fortschritt(m1, o1, m_l["ankunft"])
check("nach dem Laden bucht ein zweiter Aufruf nichts doppelt (bleibt 120)",
      o2["B"]["vorraete"]["holz"] == 120, str(o2["B"]["vorraete"]))
o3, m3 = O.transport_fortschritt(m2, o2, m_l["rueckkehr"])
check("nach dem Laden kehren die Einheiten zur Rueckkehr zurueck (1 -> 2)",
      o3["A"]["einheiten"]["Handkarren"] == 2, str(o3["A"]["einheiten"]))


# ==========================================================================
abschnitt("8. Erhaltung: es entsteht und verschwindet kein Rohstoff")

a, b = paar()
vorher = a["vorraete"]["holz"] + b["vorraete"]["holz"]
qa, m = O.transport_start(a, b, {"Handkarren": 1}, {"holz": 20}, 0.0)
o1, m1 = O.transport_fortschritt(m, {"A": qa, "B": b}, m["ankunft"])
nachher = o1["A"]["vorraete"]["holz"] + o1["B"]["vorraete"]["holz"]
check("Summe Quelle+Ziel vor der Fahrt = 200", vorher == 200, str(vorher))
check("Summe Quelle+Ziel nach der Ankunft ist unveraendert (200)",
      nachher == 200, str(nachher))
check("nichts entsteht: das Ziel hat genau die Fracht mehr (120)",
      o1["B"]["vorraete"]["holz"] == b["vorraete"]["holz"] + 20,
      str(o1["B"]["vorraete"]))


sys.exit(bericht())
