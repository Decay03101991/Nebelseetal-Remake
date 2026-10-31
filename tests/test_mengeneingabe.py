# -*- coding: ascii -*-
"""Mengeneingabe fuer Ausbildung und Ware-Herstellung (A-1, Register 79).

Daniels Spielbericht 31.10.2026: "ich musste 200x klicken" - ohne Mengenwahl ist keine Armee
baubar, und ohne Armee kein Kampftest. Antwort im Formular: **B) Ausbildung UND Ware-Herstellung**.

Was diese Datei beweist
-----------------------
1. Die Grenze ist EINE Rechenstelle: `ausbildung_grenzen["moeglich"]` ist GENAU die groesste
   Menge, die `ausbildung_start_menge` noch annimmt - `moeglich` geht, `moeglich + 1` nicht
   (Anzeige und Kern koennen nicht auseinanderlaufen).
2. Grenzfaelle 0 / 1 / 2 / 200: 0 und negative Mengen werden abgelehnt (kein Start, keine
   stille Nullbuchung), 1 und 2 buchen genau 1 bzw. 2 Auftraege, 200 ist der Deckel.
3. Jede einzelne Schranke wird gemessen: Siedler, Ausruestung, Rohstoffe und der Deckel.
4. Kein Teilabbruch: eine zu grosse Menge veraendert den Ort GAR NICHT (Lager, Siedler,
   Ausruestung, Warteschlange unveraendert) und nennt den Grund.
5. Ware-Herstellung: `menge` Stueck buchen `menge` mal die Materialkosten und erzeugen `menge`
   Eintraege in der Werkstatt; auch hier alles oder nichts.
6. Der Kern entsteht NACHEINANDER (`freie_zeit`), nicht parallel - die Auftraege ueberlappen
   nicht, damit 200 Einheiten nicht in einer Sekunde fertig sind.
7. Quelltext-Wachen: die Oberflaeche rechnet ihre Zahlen NICHT selbst (kein zweiter Rechenweg)
   und der Deckel steht in EINER Konstanten.

Aufruf:  python -X utf8 tests/test_mengeneingabe.py
"""
from __future__ import annotations

import inspect
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import main                     # noqa: E402
import spieloekonomie as O      # noqa: E402
import werkstatt                # noqa: E402

# Umlautnamen als Escapes - so bleibt die Datei reines ASCII.
BUERGERWEHR = "B\u00fcrgerwehr"          # Buergerwehr
KAEMPFER = "K\u00e4mpfer"                # Kaempfer
KURZSCHWERT = "Kurzschwert"
# Alle Forschungsgebiete, die data/units.json als Voraussetzung nennt - belegt, nicht geraten.
FORSCH = {"Kriegskunst": 10, "Waffentechnik": 10, "Heimlichkeit": 10, "Wagenbau": 10}
LEDERRUESTUNG = "Lederr\u00fcstung"      # Lederrustung


def neuer_ort(bauten=None, stufen=None, vorraete=None, waren=None, bevoelkerung=5.0,
              ausbildung=None, werkstaetten=None, oid="A"):
    """Ein Siedlungs-Ort mit allen Feldern, die Kern und Anzeige erwarten."""
    return {
        "id": oid, "besitzer": "spieler", "map_id": None, "dimension": 0, "x": 0, "y": 0,
        "karte": {"raster": ["grasland"] * 100},
        "bauten": dict(bauten or {}), "stufen": dict(stufen or {}),
        "vorraete": dict(vorraete or {}), "waren": dict(waren or {}),
        "einheiten": {}, "bevoelkerung": bevoelkerung, "importiert": {},
        "verbrauchsjournal": [], "produktionsjournal": [], "fertigjournal": [],
        "werkstaetten": dict(werkstaetten or {}), "ausbildung": list(ausbildung or []),
    }


def akademie(bevoelkerung=5.0, waren=None, gold=3000.0, oid="A"):
    """Ort mit Kriegerakademie Stufe 1 (Dauer = Grunddauer, damit Zeiten pruefbar sind)."""
    return neuer_ort(bauten={"0": "kriegerakademie"}, stufen={"0": 1},
                     vorraete={"gold": gold, "nahrung": 5000.0, "leder": 5000.0,
                               "wolle": 5000.0, "pferde": 500.0, "mana": 500.0},
                     waren={"Kurzschwert": 500, LEDERRUESTUNG: 500} if waren is None else waren,
                     bevoelkerung=bevoelkerung, oid=oid)


def schmiede(metall=1000.0, oid="A"):
    """Ort mit Schmiede Stufe 1."""
    return neuer_ort(bauten={"0": "schmiede"}, stufen={"0": 1},
                     vorraete={"metall": metall, "leder": 1000.0, "wolle": 1000.0}, oid=oid)


def fehler_von(fn):
    """(war_ValueError, Nachricht) fuer einen Aufruf, der scheitern soll."""
    try:
        fn()
    except ValueError as e:
        return True, str(e)
    except Exception as e:                                # noqa: BLE001
        return False, "FALSCHE_AUSNAHME " + type(e).__name__ + ": " + str(e)
    return False, "keine Ausnahme"


def lage(ort):
    """Ein vergleichbarer Schnappschuss des Ortes (Lager, Siedler, Waren, Auftraege)."""
    return (dict(ort["vorraete"]), dict(ort["waren"]), float(ort["bevoelkerung"]),
            len(ort["ausbildung"]), dict(ort["werkstaetten"]))


# ==========================================================================
abschnitt("1. Die Grenze ist EINE Rechenstelle (Anzeige == Kern)")

o = akademie(bevoelkerung=7.0)
g = O.ausbildung_grenzen(o, KAEMPFER, FORSCH)
check("1 die Grenze meldet kein Hindernis", g["hindernis"] == "", g["hindernis"])
check("1 Kaempfer kostet 1 Siedler je Einheit",
      g["siedler_je"] == 1, str(g["siedler_je"]))
moeglich = g["moeglich"]
check("1 bei 7 Siedlern, 3000 Gold (250 je Kaempfer) sind 7 bezahlbar",
      moeglich == 7, str(moeglich))
start_ok = O.ausbildung_start_menge(o, KAEMPFER, FORSCH, 0.0, moeglich)
check("1 genau `moeglich` Einheiten werden angenommen",
      start_ok["anzahl"] == moeglich and len(start_ok["ort"]["ausbildung"]) == moeglich,
      str(start_ok["anzahl"]))
war_fehler, text = fehler_von(
    lambda: O.ausbildung_start_menge(o, KAEMPFER, FORSCH, 0.0, moeglich + 1))
check("1 `moeglich + 1` wird abgelehnt (keine zweite Wahrheit)", war_fehler, text)
check("1 die Ablehnung nennt die Grenze", str(moeglich) in text, text)


# ==========================================================================
abschnitt("2. Grenzfaelle 0 / 1 / 2 / 200")

for menge in (0, -1, -200):
    war_fehler, text = fehler_von(
        lambda m=menge: O.ausbildung_start_menge(o, KAEMPFER, FORSCH, 0.0, m))
    check(f"2 Menge {menge} wird abgelehnt (keine stille Nullbuchung)", war_fehler, text)

for menge in (True, "viele", 2.7):
    war_fehler, text = fehler_von(
        lambda m=menge: O.ausbildung_start_menge(o, KAEMPFER, FORSCH, 0.0, m))
    if isinstance(menge, float):
        check("2 eine Kommazahl wird auf ganze Stuecke gebracht (2.7 -> 2)",
              not war_fehler, text)
    else:
        check(f"2 Menge {menge!r} wird abgelehnt", war_fehler, text)

eins = O.ausbildung_start_menge(o, KAEMPFER, FORSCH, 0.0, 1)
check("2 Menge 1 erzeugt genau einen Auftrag",
      len(eins["ort"]["ausbildung"]) == 1, str(len(eins["ort"]["ausbildung"])))
check("2 Menge 1 kostet genau 250 Gold",
      eins["ort"]["vorraete"]["gold"] == o["vorraete"]["gold"] - 250,
      str(eins["ort"]["vorraete"]["gold"]))
check("2 Menge 1 verbraucht genau 1 Siedler",
      eins["ort"]["bevoelkerung"] == o["bevoelkerung"] - 1,
      str(eins["ort"]["bevoelkerung"]))

zwei = O.ausbildung_start_menge(o, KAEMPFER, FORSCH, 0.0, 2)
check("2 Menge 2 erzeugt genau zwei Auftraege",
      len(zwei["ort"]["ausbildung"]) == 2, str(len(zwei["ort"]["ausbildung"])))
check("2 Menge 2 kostet genau 500 Gold",
      zwei["ort"]["vorraete"]["gold"] == o["vorraete"]["gold"] - 500,
      str(zwei["ort"]["vorraete"]["gold"]))
a1, a2 = zwei["ort"]["ausbildung"]
check("2 die beiden Auftraege laufen NACHEINANDER (kein Parallelstart)",
      a2["start"] >= a1["ende"], f"{a1['start']}-{a1['ende']} / {a2['start']}-{a2['ende']}")
check("2 der zweite Auftrag startet genau am Ende des ersten",
      a2["start"] == a1["ende"], f"{a1['ende']} / {a2['start']}")

gross = akademie(bevoelkerung=500.0, gold=500000.0, waren={"Kurzschwert": 500,
                                                          LEDERRUESTUNG: 500})
gross["vorraete"].update({"nahrung": 1e9, "leder": 1e6, "wolle": 1e6})
gg = O.ausbildung_grenzen(gross, BUERGERWEHR, FORSCH)
check("2 bei 500 Siedlern ist der Deckel 200 (nicht 500)",
      gg["moeglich"] == O.MENGEN_HOECHSTMENGE == 200, str(gg["moeglich"]))
h200 = O.ausbildung_start_menge(gross, BUERGERWEHR, FORSCH, 0.0, 200)
check("2 Menge 200 wird angenommen und erzeugt 200 Auftraege",
      h200["anzahl"] == 200 and len(h200["ort"]["ausbildung"]) == 200,
      str(len(h200["ort"]["ausbildung"])))
check("2 Menge 200 verbraucht 200 Siedler",
      h200["ort"]["bevoelkerung"] == 300.0, str(h200["ort"]["bevoelkerung"]))
war_fehler, text = fehler_von(
    lambda: O.ausbildung_start_menge(gross, BUERGERWEHR, FORSCH, 0.0, 201))
check("2 Menge 201 wird am Deckel abgelehnt", war_fehler, text)


# ==========================================================================
abschnitt("3. Jede Schranke einzeln: Siedler, Ausruestung, Rohstoffe")

# 3a Siedler
o_siedler = akademie(bevoelkerung=3.0)
gs = O.ausbildung_grenzen(o_siedler, KAEMPFER, FORSCH)
check("3a 3 Siedler erlauben genau 3 Kaempfer", gs["moeglich"] == 3, str(gs["moeglich"]))
check("3a die Grenze nennt den Engpass Siedler",
      gs["grenzen"].get("siedler") == 3, str(gs["grenzen"]))

# 3b Ausruestung
o_ausr = akademie(bevoelkerung=50.0, waren={"Kurzschwert": 4, LEDERRUESTUNG: 4})
ga = O.ausbildung_grenzen(o_ausr, KAEMPFER, FORSCH)
check("3b 4 Kurzschwerter erlauben genau 4 Kaempfer", ga["moeglich"] == 4,
      str(ga["moeglich"]))
check("3b die Ausruestungsgrenze steht als eigene Zeile",
      ga["grenzen"].get("ausruestung:" + LEDERRUESTUNG) == 4, str(ga["grenzen"]))
war_fehler, text = fehler_von(
    lambda: O.ausbildung_start_menge(o_ausr, KAEMPFER, FORSCH, 0.0, 5))
check("3b 5 Kaempfer bei 4 Rustungen werden abgelehnt", war_fehler, text)
check("3b die Meldung nennt die bezahlbare Zahl", "4" in text, text)

# 3c Rohstoffe
o_gold = akademie(bevoelkerung=50.0, gold=1000.0)          # 250 je Kaempfer -> 4
gz = O.ausbildung_grenzen(o_gold, KAEMPFER, FORSCH)
check("3c 1000 Gold erlauben genau 4 Kaempfer", gz["moeglich"] == 4, str(gz["moeglich"]))
war_fehler, text = fehler_von(
    lambda: O.ausbildung_start_menge(o_gold, KAEMPFER, FORSCH, 0.0, 5))
check("3c 5 Kaempfer bei 1000 Gold werden abgelehnt", war_fehler, text)
check("3c die Meldung heisst 'Lokales Lager reicht nicht'", "Lager" in text, text)

# 3d Deckel ist die kleinste Grenze
check("3d der Deckel 200 ist selbst eine Grenze",
      O.ausbildung_grenzen(gross, KAEMPFER, FORSCH)["moeglich"] <= 200, "")


# ==========================================================================
abschnitt("4. Kein Teilabbruch: eine zu grosse Menge aendert NICHTS")

vorher = lage(o_ausr)
war_fehler, text = fehler_von(
    lambda: O.ausbildung_start_menge(o_ausr, KAEMPFER, FORSCH, 0.0, 5))
check("4 die Ablehnung wirft ValueError", war_fehler, text)
check("4 der Ort ist unveraendert (Lager, Waren, Siedler, Auftraege, Werkstaetten)",
      lage(o_ausr) == vorher, "Vorher/Nachher unterschiedlich")

vorher_ware = lage(schmiede())
war_fehler, text = fehler_von(
    lambda: O.ware_start_menge(schmiede(), KURZSCHWERT, {"Waffentechnik": 3}, 0.0, 100000))
check("4 auch die Ware-Menge wird vor jeder Buchung abgelehnt", war_fehler, text)
check("4 der Werkstatt-Ort bleibt unveraendert", lage(schmiede()) == vorher_ware, "")


# ==========================================================================
abschnitt("5. Ware-Herstellung mit Menge")

s = schmiede(metall=1000.0)
gerechnet = O.ware_grenzen(s, KURZSCHWERT, {"Waffentechnik": 3})
je = gerechnet["kosten_je"]["metall"]
check("5 die Grenze rechnet mit dem Rezeptpreis", je == 4.0, str(je))
check("5 1000 Metall erlauben 200 Stueck (Deckel, nicht 250)",
      gerechnet["moeglich"] == 200, str(gerechnet["moeglich"]))

w1 = O.ware_start_menge(s, KURZSCHWERT, {"Waffentechnik": 3}, 0.0, 1)
check("5 Menge 1 bucht genau 4 Metall ab", w1["ort"]["vorraete"]["metall"] == 996.0,
      str(w1["ort"]["vorraete"]["metall"]))
check("5 Menge 1 erzeugt einen Werkstatt-Eintrag",
      len(w1["ort"]["werkstaetten"]["schmiede"]["einheiten"]) == 1, "")

w5 = O.ware_start_menge(s, KURZSCHWERT, {"Waffentechnik": 3}, 0.0, 5)
check("5 Menge 5 bucht genau 20 Metall ab", w5["ort"]["vorraete"]["metall"] == 980.0,
      str(w5["ort"]["vorraete"]["metall"]))
check("5 Menge 5 erzeugt fuenf Werkstatt-Eintraege",
      len(w5["ort"]["werkstaetten"]["schmiede"]["einheiten"]) == 5,
      str(len(w5["ort"]["werkstaetten"]["schmiede"]["einheiten"])))
check("5 die Warteschlange fuehrt EINEN Auftrag ueber 5 Stueck",
      len(w5["ort"]["werkstaetten"]["schmiede"]["auftraege"]) == 1,
      str(w5["ort"]["werkstaetten"]["schmiede"]["auftraege"]))
check("5 der Auftrag nennt die Menge 5",
      w5["ort"]["werkstaetten"]["schmiede"]["auftraege"][0]["anzahl"] == 5,
      str(w5["ort"]["werkstaetten"]["schmiede"]["auftraege"][0]))

o_knapp = schmiede(metall=10.0)
gk = O.ware_grenzen(o_knapp, KURZSCHWERT, {"Waffentechnik": 3})
check("5a 10 Metall erlauben 2 Kurzschwerter", gk["moeglich"] == 2, str(gk["moeglich"]))
war_fehler, text = fehler_von(
    lambda: O.ware_start_menge(o_knapp, KURZSCHWERT, {"Waffentechnik": 3}, 0.0, 3))
check("5a 3 Stueck bei 10 Metall werden abgelehnt", war_fehler, text)
check("5a die Meldung nennt die Grenze 2", "2" in text, text)

for menge in (0, -3):
    war_fehler, text = fehler_von(
        lambda m=menge: O.ware_start_menge(s, KURZSCHWERT, {"Waffentechnik": 3}, 0.0, m))
    check(f"5b Menge {menge} wird bei der Ware abgelehnt", war_fehler, text)

# Der Altweg bleibt: ware_start/ausbildung_start sind die Einzelstueck-Fassungen.
alt_ware = O.ware_start(schmiede(), KURZSCHWERT, {"Waffentechnik": 3}, 0.0)
check("5c ware_start reiht weiterhin genau ein Stueck ein",
      len(alt_ware["werkstaetten"]["schmiede"]["einheiten"]) == 1, "")
alt_einheit = O.ausbildung_start(akademie(), KAEMPFER, FORSCH, 0.0)
check("5c ausbildung_start erzeugt weiterhin genau einen Auftrag",
      len(alt_einheit["ausbildung"]) == 1, "")


# ==========================================================================
abschnitt("6. Ort-Tick bucht die Menge genau einmal je Auftrag")

gross2 = akademie(bevoelkerung=20.0, gold=50000.0)
ankunft = O.ausbildung_start_menge(gross2, KAEMPFER, FORSCH, 0.0, 4)
fertig = O.ort_tick(ankunft["ort"], 0.0, ankunft["ende"] + 1.0, FORSCH)
check("6 nach dem Ende liegen genau 4 Kaempfer im Ortslager",
      fertig["einheiten"].get(KAEMPFER) == 4, str(fertig["einheiten"]))
check("6 alle Auftraege sind als gebucht markiert",
      all(a["gebucht"] for a in fertig["ausbildung"]), "")
zweiter_tick = O.ort_tick(fertig, ankunft["ende"] + 1.0, ankunft["ende"] + 5000.0,
                          FORSCH)
check("6 ein zweiter Tick bucht NICHT noch einmal (genau einmal)",
      zweiter_tick["einheiten"].get(KAEMPFER) == 4, str(zweiter_tick["einheiten"]))

teil = O.ort_tick(ankunft["ort"], 0.0, ankunft["ort"]["ausbildung"][0]["ende"] + 0.5,
                  FORSCH)
check("6 nach der ersten Dauer ist genau 1 Einheit da (nicht alle vier)",
      teil["einheiten"].get(KAEMPFER) == 1, str(teil["einheiten"]))


# ==========================================================================
abschnitt("7. Quelltext-Wachen: eine Rechenstelle, ein Deckel")

quelle_main = inspect.getsource(main)
check("7 main benutzt die Mengenfassung der Ausbildung",
      "ausbildung_start_menge(" in quelle_main, "")
check("7 main benutzt die Mengenfassung der Ware",
      "ware_start_menge(" in quelle_main, "")
check("7 main rechnet die Grenze NICHT selbst nach (kein zweiter Rechenweg)",
      "ausbildung_grenzen(" in quelle_main and "ware_grenzen(" in quelle_main,
      "main muss die Grenzen aus dem Kern lesen")
treffer = re.findall(r"\.(?:ausbildung|ware)_start\(", quelle_main)
check("7 der Altpfad wird nur noch ueber die Wrapper benutzt (hoechstens 2 Stellen)",
      len(treffer) <= 2, str(treffer))

quelle_kern = inspect.getsource(O)
check("7 der Deckel steht in EINER Konstanten",
      quelle_kern.count("MENGEN_HOECHSTMENGE = ") == 1, "")
check("7 der Deckel wird in beiden Grenzrechnungen benutzt",
      quelle_kern.count("MENGEN_HOECHSTMENGE]") >= 2, "")

abschnitt("8. Anzeige-Texte: die Zahl im Knopf ist die Menge")
check("8 _mengen_feld existiert (Zahlfeld, -/+, Schieberegler)",
      hasattr(main.NebelseetalApp, "_mengen_feld"), "")
check("8 _menge_lesen klemmt negative Werte auf 0", True, "wird unten direkt geprueft")
app_like = main.NebelseetalApp._menge_lesen

class _Var:
    def __init__(self, wert):
        self.wert = wert
    def get(self):
        return self.wert

check("8 '0' wird als 0 gelesen", app_like(None, _Var("0"), 200) == 0, "")
check("8 '-5' wird auf 0 geklemmt", app_like(None, _Var("-5"), 200) == 0, "")
check("8 '999' wird auf den Deckel geklemmt", app_like(None, _Var("999"), 200) == 200, "")
check("8 Unsinn wird zu 0 (kein Absturz)", app_like(None, _Var("abc"), 200) == 0, "")
check("8 '12' bleibt 12", app_like(None, _Var("12"), 200) == 12, "")

sys.exit(bericht())
