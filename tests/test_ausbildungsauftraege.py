# -*- coding: ascii -*-
"""Pruefung der Pilotrezepte, lokalen Ausbildung und Verbrauchsbelege.

Gegenstand sind die NEUEN Funktionen in src/spieloekonomie.py:
  ware_start(ort, ware, forschung, jetzt, rezepte=None) -> neuer Ort
  ausbildung_start(ort, name, forschung, jetzt)          -> neuer Ort

Richtschnur ist der Entwurf archiv/analysen/audits/entwurf_spieloekonomie_sol_2026-10-05.txt,
Zeilen 507-590 ('jede der 17 Waren hat Herkunft; kombinierte Sperren vollstaendig;
Materialabzug genau einmal; Wollumhang 1 Wolle/20min, Kurzschwert 4 Metall/80min,
Lederrustung 4 Leder/80min; Schwertdauer bleibt 1200s') und Abschnitt 4 des Entwurfs.

Geprueft werden die zehn Pflichtzusagen:
  1. Kurzschwert, Waffentechnik 3, Schmiede vor Ort: Metall 10 -> 6, Warteschlange
     der Schmiede mit einem Eintrag dauer 4800.
  2. Zweimal einreihen bucht ZWEIMAL ab (10 -> 2), kein Einmal-Abzug.
  3. Jede Ablehnung einzeln (Forschung, Werkstatt, Material, unbekannte Ware).
  4. Die einzige BELEGTE Dauer bleibt: Schwert (Waffentechnik 5) -> dauer 1200.
  5. Alle 17 Waren aus data/warenrezepte.json sind einreihbar (Werkstatt selbst
     aus werkstatt.werkstatt_fuer abgeleitet).
  6. Der Abzug geschieht aus dem LOKALEN Lager; ein zweiter Ort bleibt unveraendert.
  7. Kaempfer: Gold 300 -> 50, Bevoelkerung 5 -> 4, beide Waren auf 0, Auftrag
     ende = jetzt + 1200.
  8. Jede Ablehnung der Ausbildung einzeln.
  9. Zwei Auftraege NACHEINANDER in derselben Staette (fortlaufend, nicht gleichzeitig).
 10. Der Auftrag selbst hat 'gebucht': False (die Einheit entsteht spaeter).

Aufruf:  python -X utf8 tests/test_ausbildungsauftraege.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

ROOT, SRC = import_src()
import spieloekonomie as O       # noqa: E402
import werkstatt                 # noqa: E402

# Umlautnamen als Escapes - so bleibt die Datei reines ASCII.
KAEMPFER = "K\u00e4mpfer"                 # Kaempfer
LEDERRUESTUNG = "Lederr\u00fcstung"       # Lederrustung


# --------------------------------------------------------------------------- Hilfen
def neuer_ort(oid="A", besitzer="spieler", dimension=0, x=0, y=0,
              bauten=None, stufen=None, vorraete=None, waren=None, einheiten=None,
              bevoelkerung=5, importiert=None, journal=None, werkstaetten=None,
              ausbildung=None):
    """Ein Siedlungs-Ort mit allen Feldern, die ware_start/ausbildung_start erwarten."""
    return {
        "id": oid,
        "besitzer": besitzer,
        "map_id": None,
        "dimension": dimension,
        "x": x,
        "y": y,
        "bauten": dict(bauten) if bauten is not None else {},
        "stufen": dict(stufen) if stufen is not None else {},
        "vorraete": dict(vorraete) if vorraete is not None else {},
        "waren": dict(waren) if waren is not None else {},
        "einheiten": dict(einheiten) if einheiten is not None else {},
        "bevoelkerung": bevoelkerung,
        "importiert": dict(importiert) if importiert is not None else {},
        "verbrauchsjournal": list(journal) if journal is not None else [],
        "werkstaetten": dict(werkstaetten) if werkstaetten is not None else {},
        "ausbildung": list(ausbildung) if ausbildung is not None else [],
    }


def schmiede_ort(vorraete=None, oid="A"):
    """Ein Ort mit einer Schmiede vor Ort."""
    return neuer_ort(oid, bauten={"0": "schmiede"}, stufen={"0": 1},
                     vorraete={"metall": 10.0} if vorraete is None else vorraete,
                     importiert={"metall": 0.0})


def akademie_ort(gold=300.0, bevoelkerung=5, waren=None, oid="A"):
    """Ein Ort mit einer Kriegerakademie vor Ort."""
    return neuer_ort(oid, bauten={"0": "kriegerakademie"}, stufen={"0": 1},
                     vorraete={"gold": gold}, importiert={"gold": 0.0},
                     bevoelkerung=bevoelkerung,
                     waren={"Kurzschwert": 1, LEDERRUESTUNG: 1} if waren is None else waren)


def wert_fehler(fn):
    """Fuehrt fn aus; liefert (war_es_ValueError, Nachricht)."""
    try:
        fn()
    except ValueError as e:
        return True, str(e)
    except Exception as e:  # noqa: BLE001
        return False, "FALSCHE_AUSNAHME " + type(e).__name__ + ": " + str(e)
    return False, "keine Ausnahme"


# ==========================================================================
abschnitt("1. ware_start: Kurzschwert zieht genau 4 Metall, Warteschlange 4800")

o1 = schmiede_ort()
n1 = O.ware_start(o1, "Kurzschwert", {"Waffentechnik": 3}, 0.0)
check("1 Metall nimmt von 10 auf 6 ab (genau 4)",
      n1["vorraete"]["metall"] == 6, str(n1["vorraete"]["metall"]))
schl = n1["werkstaetten"].get("schmiede")
check("1 die Warteschlange der Schmiede entsteht", isinstance(schl, dict), str(schl))
check("1 die Warteschlange enthaelt genau einen Eintrag",
      len(schl["einheiten"]) == 1, str(len(schl["einheiten"])))
e1 = schl["einheiten"][-1]
check("1 der Eintrag nennt die Ware Kurzschwert", e1["ware"] == "Kurzschwert", str(e1["ware"]))
check("1 der Eintrag hat die Dauer 4800", e1["dauer"] == 4800, str(e1["dauer"]))
check("1 reine Funktion: die Vorlage behaelt Metall 10 und keine Werkstatt",
      o1["vorraete"]["metall"] == 10 and o1["werkstaetten"] == {}, str(o1["vorraete"]))


# ==========================================================================
abschnitt("2. zweimal einreihen bucht ZWEIMAL ab (kein Einmal-Abzug)")

n2 = O.ware_start(n1, "Kurzschwert", {"Waffentechnik": 3}, 0.0)
check("2 nach dem zweiten Einreihen ist Metall auf 2 (10 -> 2)",
      n2["vorraete"]["metall"] == 2, str(n2["vorraete"]["metall"]))
check("2 die Warteschlange waechst auf zwei Eintraege",
      len(n2["werkstaetten"]["schmiede"]["einheiten"]) == 2,
      str(len(n2["werkstaetten"]["schmiede"]["einheiten"])))


# ==========================================================================
abschnitt("3. ware_start: jede Ablehnung einzeln")

# 3a ohne Forschungsvoraussetzung (Kurzschwert verlangt Waffentechnik 3)
o3a = schmiede_ort()
ok, t = wert_fehler(lambda: O.ware_start(o3a, "Kurzschwert", {}, 0.0))
check("3a ohne Forschungsvoraussetzung -> ValueError", ok and "Warenvoraussetzung" in t, t)

# 3b ohne Werkstatt vor Ort (Forschung erfuellt, Material vorhanden)
o3b = neuer_ort(vorraete={"metall": 10.0}, importiert={"metall": 0.0})
ok, t = wert_fehler(lambda: O.ware_start(o3b, "Kurzschwert", {"Waffentechnik": 3}, 0.0))
check("3b ohne Werkstatt vor Ort -> ValueError", ok and "Werkstatt" in t, t)

# 3c ohne Material im lokalen Lager (Forschung erfuellt, Schmiede vorhanden)
o3c = neuer_ort(bauten={"0": "schmiede"}, stufen={"0": 1}, vorraete={})
ok, t = wert_fehler(lambda: O.ware_start(o3c, "Kurzschwert", {"Waffentechnik": 3}, 0.0))
check("3c ohne Material im lokalen Lager -> ValueError", ok and "Lager" in t, t)

# 3d unbekannte Ware (nicht in data/warenrezepte.json)
o3d = schmiede_ort()
ok, t = wert_fehler(lambda: O.ware_start(o3d, "Mondstahlklinge", {}, 0.0))
check("3d unbekannte Ware -> ValueError", ok and "Rezept" in t, t)

# eine Ablehnung laesst den Ort unveraendert
check("3 eine Ablehnung veraendert den Ausgangsort nicht",
      o3c["vorraete"] == {} and o3c["werkstaetten"] == {}, str(o3c))


# ==========================================================================
abschnitt("4. die einzige BELEGTE Dauer bleibt: Schwert (Waffentechnik 5) = 1200")

o4 = schmiede_ort()
s4 = O.ware_start(o4, "Schwert", {"Waffentechnik": 5}, 0.0)
d4 = s4["werkstaetten"]["schmiede"]["einheiten"][-1]["dauer"]
check("4 Schwert bei Waffentechnik 5 ergibt dauer 1200", d4 == 1200, str(d4))
check("4 werkstatt.dauer_belegt('Schwert') bleibt True",
      werkstatt.dauer_belegt("Schwert") is True, str(werkstatt.dauer_belegt("Schwert")))
check("4 nur das Schwert ist belegt: Kurzschwert bleibt unbelegt",
      werkstatt.dauer_belegt("Kurzschwert") is False,
      str(werkstatt.dauer_belegt("Kurzschwert")))
check("4 die Kurzschwertdauer 4800 kommt aus dem Rezept, nicht aus einer Belegbehauptung",
      n1["werkstaetten"]["schmiede"]["einheiten"][-1]["dauer"] == 4800,
      str(n1["werkstaetten"]["schmiede"]["einheiten"][-1]["dauer"]))


# ==========================================================================
abschnitt("5. alle 17 Waren aus data/warenrezepte.json sind einreihbar")

check("5.0 data/warenrezepte.json hat genau 17 Waren",
      len(O.WARENREZEPTE) == 17, str(len(O.WARENREZEPTE)))
check("5.1 jede Ware hat eine Werkstatt (werkstatt.werkstatt_fuer)",
      all(werkstatt.werkstatt_fuer(w) for w in O.WARENREZEPTE),
      str([w for w in O.WARENREZEPTE if not werkstatt.werkstatt_fuer(w)]))

n_waren = 0
fehler_waren = []
for ware in sorted(O.WARENREZEPTE):
    typ = werkstatt.werkstatt_fuer(ware)
    ort5 = neuer_ort(bauten={"0": typ}, stufen={"0": 1},
                     vorraete={"metall": 1000.0, "holz": 1000.0,
                               "wolle": 1000.0, "leder": 1000.0},
                     importiert={})
    forschung5 = dict(O.WARENREZEPTE[ware]["voraussetzungen"])
    try:
        neu5 = O.ware_start(ort5, ware, forschung5, 0.0)
        letzter = neu5["werkstaetten"][typ]["einheiten"][-1]
        if letzter["ware"] != ware:
            raise AssertionError("falsche Ware in der Warteschlange")
        n_waren += 1
    except Exception as exc:  # noqa: BLE001
        fehler_waren.append(ware + ": " + repr(exc))
print("  -> geprueft: " + str(n_waren) + " von " + str(len(O.WARENREZEPTE)) + " Waren")
check("5.2 alle 17 Waren sind einreihbar (Werkstatt + Forschung erfuellt)",
      n_waren == 17, "geprueft=" + str(n_waren) + " fehlend=" + repr(fehler_waren))


# ==========================================================================
abschnitt("6. der Abzug kommt aus dem LOKALEN Lager, nicht global")

links = schmiede_ort(oid="links")
rechts = schmiede_ort(oid="rechts")
nl = O.ware_start(links, "Kurzschwert", {"Waffentechnik": 3}, 0.0)
check("6 der bearbeitete Ort verliert das Metall (10 -> 6)",
      nl["vorraete"]["metall"] == 6, str(nl["vorraete"]["metall"]))
check("6 ein zweiter Ort bleibt voellig unveraendert (Metall 10, leere Werkstatt)",
      rechts["vorraete"]["metall"] == 10 and rechts["werkstaetten"] == {}, str(rechts))
check("6 abgebucht wird genau aus dem lokalen Lager des Ortes",
      nl["vorraete"]["metall"] == links["vorraete"]["metall"] - 4,
      str(links["vorraete"]["metall"]))


# ==========================================================================
abschnitt("7. ausbildung_start: Kaempfer (Kriegskunst 1) in der Kriegerakademie")

jetzt7 = 100.0
o7 = akademie_ort()
n7 = O.ausbildung_start(o7, KAEMPFER, {"Kriegskunst": 1}, jetzt7)
check("7 Gold sinkt genau um 250 (300 -> 50)",
      n7["vorraete"]["gold"] == 50, str(n7["vorraete"]["gold"]))
check("7 Bevoelkerung sinkt um genau einen Siedler (5 -> 4)",
      n7["bevoelkerung"] == 4, str(n7["bevoelkerung"]))
check("7 BEIDE Waren sind danach auf 0",
      n7["waren"].get("Kurzschwert") == 0 and n7["waren"].get(LEDERRUESTUNG) == 0,
      str(n7["waren"]))
check("7 genau ein Ausbildungsauftrag steht in ort['ausbildung']",
      len(n7["ausbildung"]) == 1, str(n7["ausbildung"]))
a7 = n7["ausbildung"][0]
check("7 der Auftrag nennt die Einheit Kaempfer", a7["einheit"] == KAEMPFER, str(a7))
check("7 der Auftrag nennt die Kriegerakademie",
      a7["gebaeude"] == "kriegerakademie", str(a7["gebaeude"]))
check("7 der Auftrag endet bei jetzt + 1200 (pilot_ausbildung_minuten 20)",
      a7["ende"] == jetzt7 + 1200, str(a7["ende"]))
check("7 der Auftrag beginnt bei jetzt", a7["start"] == jetzt7, str(a7["start"]))
check("7 reine Funktion: die Vorlage behaelt Gold 300 und 5 Siedler",
      o7["vorraete"]["gold"] == 300 and o7["bevoelkerung"] == 5
      and o7["ausbildung"] == [], str(o7))


# ==========================================================================
abschnitt("8. ausbildung_start: jede Ablehnung einzeln")

# 8a ohne Kriegskunst
ok, t = wert_fehler(lambda: O.ausbildung_start(akademie_ort(), KAEMPFER, {}, 0.0))
check("8a ohne Kriegskunst -> ValueError", ok and "forschung" in t.lower(), t)

# 8b ohne Ausbildungsstaette vor Ort
o8b = neuer_ort(vorraete={"gold": 300.0}, bevoelkerung=5,
                waren={"Kurzschwert": 1, LEDERRUESTUNG: 1})
ok, t = wert_fehler(lambda: O.ausbildung_start(o8b, KAEMPFER, {"Kriegskunst": 1}, 0.0))
check("8b ohne Ausbildungsstaette vor Ort -> ValueError",
      ok and "Ausbildungsst" in t, t)

# 8c ohne Ausruestung im Lager
o8c = akademie_ort(waren={})
ok, t = wert_fehler(lambda: O.ausbildung_start(o8c, KAEMPFER, {"Kriegskunst": 1}, 0.0))
check("8c ohne Ausruestung im Lager -> ValueError", ok and "Ausr" in t, t)

# 8d ohne genug freie Siedler (Kosten siedler 1, Bevoelkerung 0)
o8d = akademie_ort(bevoelkerung=0)
ok, t = wert_fehler(lambda: O.ausbildung_start(o8d, KAEMPFER, {"Kriegskunst": 1}, 0.0))
check("8d ohne genug freie Siedler -> ValueError", ok and "Siedler" in t, t)

# 8e unbekannte Einheit
ok, t = wert_fehler(lambda: O.ausbildung_start(akademie_ort(), "Nichtsda", {}, 0.0))
check("8e unbekannte Einheit -> ValueError", ok and "Unbekannte Einheit" in t, t)


# ==========================================================================
abschnitt("9. zwei Auftraege NACHEINANDER in derselben Staette")

# freie_zeit := max(jetzt, spaetestes 'ende' aller Auftraege DERSELBEN Staette)
# (spieloekonomie.ausbildung_start: max([jetzt] + [a["ende"] ... if a["gebaeude"] == geb])).
# Darum reihen sich Auftraege in einer Staette fortlaufend, nicht gleichzeitig.
o9 = akademie_ort(gold=900.0, bevoelkerung=5,
                  waren={"Kurzschwert": 3, LEDERRUESTUNG: 3})
m1 = O.ausbildung_start(o9, KAEMPFER, {"Kriegskunst": 1}, 0.0)
m2 = O.ausbildung_start(m1, KAEMPFER, {"Kriegskunst": 1}, 0.0)
m3 = O.ausbildung_start(m2, KAEMPFER, {"Kriegskunst": 1}, 0.0)
check("9 drei Auftraege stehen in ort['ausbildung']",
      len(m3["ausbildung"]) == 3, str(len(m3["ausbildung"])))
b1, b2, b3 = m3["ausbildung"]
check("9 der zweite Auftrag beginnt NICHT vor dem Ende des ersten",
      b2["start"] >= b1["ende"], "b1.ende=" + str(b1["ende"]) + " b2.start=" + str(b2["start"]))
check("9 der zweite beginnt genau am Ende des ersten (nacheinander, nicht gleichzeitig)",
      b2["start"] == b1["ende"], "b1.ende=" + str(b1["ende"]) + " b2.start=" + str(b2["start"]))
check("9 der erste Auftrag laeuft 0..1200", b1["start"] == 0 and b1["ende"] == 1200, str(b1))
check("9 der zweite Auftrag laeuft 1200..2400", b2["start"] == 1200 and b2["ende"] == 2400, str(b2))
check("9 der dritte Auftrag wartet auf das Ende des zweiten (freie_zeit=2400)",
      b3["start"] == 2400 and b3["ende"] == 3600, str(b3))
check("9 Gold wurde fuer alle drei Auftraege abgebucht (900 -> 150)",
      m3["vorraete"]["gold"] == 150, str(m3["vorraete"]["gold"]))
check("9 die Siedler sanken fuer alle drei (5 -> 2)",
      m3["bevoelkerung"] == 2, str(m3["bevoelkerung"]))
check("9 das Warenlager ist nach drei Auftraegen leer (3 -> 0)",
      m3["waren"].get("Kurzschwert") == 0 and m3["waren"].get(LEDERRUESTUNG) == 0,
      str(m3["waren"]))


# ==========================================================================
abschnitt("10. der Auftrag hat 'gebucht': False (die Einheit entsteht spaeter)")

check("10 der erste Auftrag traegt gebucht=False",
      b1.get("gebucht") is False, str(b1.get("gebucht")))
check("10 auch der zweite und dritte Auftrag sind noch nicht gebucht",
      b2.get("gebucht") is False and b3.get("gebucht") is False,
      str([b1.get("gebucht"), b2.get("gebucht"), b3.get("gebucht")]))
check("10 noch steht keine Kaempfer-Einheit am Ort (sie entsteht erst am Auftragsende)",
      m3["einheiten"].get(KAEMPFER, 0) == 0, str(m3["einheiten"]))


# ==========================================================================
abschnitt("11. Ausbildungsdauer haengt von der Gebaeudestufe ab (Richtung belegt, Zahlen VORSCHLAG)")

_ort1 = neuer_ort("s1", bauten={"0": "kriegerakademie"}, stufen={"0": 1},
                  vorraete={"gold": 300.0}, importiert={"gold": 0.0}, bevoelkerung=5,
                  waren={"Kurzschwert": 1, LEDERRUESTUNG: 1})
_ort3 = neuer_ort("s3", bauten={"0": "kriegerakademie"}, stufen={"0": 3},
                  vorraete={"gold": 300.0}, importiert={"gold": 0.0}, bevoelkerung=5,
                  waren={"Kurzschwert": 1, LEDERRUESTUNG: 1})
_a1 = O.ausbildung_start(_ort1, KAEMPFER, {"Kriegskunst": 1}, 0.0)["ausbildung"][0]
_a3 = O.ausbildung_start(_ort3, KAEMPFER, {"Kriegskunst": 1}, 0.0)["ausbildung"][0]
check("11 Stufe 1: Dauer = Grunddauer (20 min = 1200 s)",
      _a1.get("dauer_sekunden") == 1200.0, str(_a1.get("dauer_sekunden")))
check("11 Stufe 3: Dauer ist ein Drittel (400 s)",
      _a3.get("dauer_sekunden") == 400.0, str(_a3.get("dauer_sekunden")))
check("11 die Stufe steht im Auftrag", _a1.get("stufe") == 1 and _a3.get("stufe") == 3,
      f"{_a1.get('stufe')}/{_a3.get('stufe')}")
check("11 hoehere Stufe ist schneller (Richtung belegt: 'Je hoeher die Stufe, desto schneller')",
      _a3["ende"] - _a3["start"] < _a1["ende"] - _a1["start"],
      f"{_a3['ende'] - _a3['start']} gegen {_a1['ende'] - _a1['start']}")

_alt = O.AUSBILDUNG_STUFENFAKTOR_AKTIV
O.AUSBILDUNG_STUFENFAKTOR_AKTIV = False
try:
    _a3b = O.ausbildung_start(_ort3, KAEMPFER, {"Kriegskunst": 1}, 0.0)["ausbildung"][0]
    check("11 der Schalter stellt die feste Dauer wieder her (kein Loeschen von Code)",
          _a3b.get("dauer_sekunden") == 1200.0, str(_a3b.get("dauer_sekunden")))
finally:
    O.AUSBILDUNG_STUFENFAKTOR_AKTIV = _alt


sys.exit(bericht())
