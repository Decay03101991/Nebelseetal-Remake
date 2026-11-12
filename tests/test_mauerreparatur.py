# -*- coding: ascii -*-
"""Mauerreparatur - S2 (06.11.2026).

Zahlen aus `docs/S0_TABELLEN_20261107.md` (V-1), von Daniel am 06.11.2026 angenommen:
  * Preis je Prozentpunkt = 16 * Stufe / 100 in Holz UND Stein (Stufe 1: 0,16; 0 auf 100 = 16/16).
  * Dauer je Prozentpunkt 360 Spielsekunden (0,1 Spielstunde), 0 auf 100 = 36000 Spielsekunden
    = 10 Spielstunden = 200 Sekunden echt (Spieluhrfaktor 180).

Was diese Datei beweist
-----------------------
1. Der Preis waechst linear mit der Stufe und haengt am fehlenden Anteil (Grenzfaelle 0 und 100).
2. Die Dauer ist proportional zum fehlenden Anteil.
3. Bei 100 Prozent Zustand ist die Reparatur gesperrt - mit Grund und naechstem Schritt.
4. Ohne Wall, mit Stufe 0, mit laufender Reparatur und bei laufendem Ausbau wird ehrlich gesperrt,
   jeder Grund EINZELN genannt.
5. Die Kosten werden ATOMAR gebucht: fehlt ein Posten, bleibt das Lager unveraendert.
6. Ein zweiter Start bucht nichts nach (die Buchung passiert genau einmal).
7. Der Zustand steigt im Tick stueckweise und steht am Ende auf 100.
8. Ein Angriff bricht die Reparatur ab; der Zustand bleibt, wo er war.
9. Aendert sich die Wallstufe waehrend der Reparatur, bricht sie ab (der Preis passt nicht mehr).
10. Die fuenf Felder ueberleben Speichern und Laden (`asdict`).
11. Anzeige und Kern lesen DIESELBE Funktion (`dorfwall.reparatur_pruefen`) - Quellwache.

Aufruf:  python -X utf8 tests/test_mauerreparatur.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['dorfwall', 'main:*']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import inspect
import json
import os
import sys
import tempfile

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(WURZEL, "src"))
sys.path.insert(0, os.path.join(WURZEL, "tests"))

from harness import abschnitt, bericht, check                      # noqa: E402
import dorfwall                                                    # noqa: E402
import main                                                        # noqa: E402

FORSCHUNG_OK = {"Verteidigungsanlagen": 3}


def ort(zustand=40.0, holz=1000.0, stein=1000.0, besetzt=True):
    """Baut einen Ort mit Wall und gefuelltem Lager (Settlement aus dem Spiel)."""
    s = main.Settlement(name="Pruefwall", map_id="pruef")
    s.mauer_besetzt = bool(besetzt)
    s.mauer_zustand = float(zustand)
    s.vorraete = {"holz": float(holz), "stein": float(stein)}
    return s


def test_preis():
    """1. Preis linear in der Stufe und im fehlenden Anteil."""
    abschnitt("1. Preis je Prozentpunkt (V-1)")
    check("Stufe 1, 0 auf 100 = 16/16", dorfwall.reparatur_preis(1, 0.0) == {"holz": 16.0, "stein": 16.0},
          str(dorfwall.reparatur_preis(1, 0.0)))
    check("Stufe 10, 0 auf 100 = 160/160",
          dorfwall.reparatur_preis(10, 0.0) == {"holz": 160.0, "stein": 160.0})
    check("Stufe 3, halber Zustand = halber Preis",
          dorfwall.reparatur_preis(3, 50.0) == {"holz": 24.0, "stein": 24.0},
          str(dorfwall.reparatur_preis(3, 50.0)))
    check("nichts fehlt = nichts kostet", dorfwall.reparatur_preis(3, 100.0) == {"holz": 0.0, "stein": 0.0})
    check("Stufe 0 wird auf 1 gezogen", dorfwall.reparatur_preis(0, 0.0)["holz"] == 16.0)
    check("Stufe 11 wird auf 10 gezogen", dorfwall.reparatur_preis(11, 0.0)["holz"] == 160.0)


def test_dauer():
    """2. Dauer proportional zum fehlenden Anteil."""
    abschnitt("2. Dauer je Prozentpunkt")
    check("0 auf 100 = 36000 Spielsekunden", dorfwall.reparatur_sekunden(0.0) == 36000.0,
          str(dorfwall.reparatur_sekunden(0.0)))
    check("50 auf 100 = 18000 Spielsekunden", dorfwall.reparatur_sekunden(50.0) == 18000.0)
    check("0 auf 100 sind 200 Sekunden echt bei Faktor 180", (36000.0 / 180.0) == 200.0)


def test_gesperrt():
    """3./4. Jede Sperre nennt ihren Grund einzeln, mit naechstem Schritt."""
    abschnitt("3. Sperren und ihre Gruende")
    voll = ort(zustand=100.0)
    p = dorfwall.reparatur_pruefen(voll, FORSCHUNG_OK, voll.vorraete)
    check("100 Prozent: nicht moeglich", p["moeglich"] is False)
    check("100 Prozent: Grund genannt", any("unbesch" in g for g in p["gruende"]), str(p["gruende"]))
    check("100 Prozent: naechster Schritt", bool(p["naechster_schritt"]))

    ohne = ort(zustand=40.0, besetzt=False)
    p = dorfwall.reparatur_pruefen(ohne, FORSCHUNG_OK, ohne.vorraete)
    check("ohne Wall: gesperrt", p["moeglich"] is False and any("kein Wall" in g for g in p["gruende"]),
          str(p["gruende"]))

    stufe0 = ort(zustand=40.0)
    p = dorfwall.reparatur_pruefen(stufe0, {}, stufe0.vorraete)
    check("Stufe 0: gesperrt", p["moeglich"] is False and any("Wallstufe ist 0" in g for g in p["gruende"]),
          str(p["gruende"]))

    arm = ort(zustand=60.0, holz=1.0, stein=1000.0)
    p = dorfwall.reparatur_pruefen(arm, FORSCHUNG_OK, arm.vorraete)
    check("zu wenig Holz: gesperrt", p["moeglich"] is False)
    check("zu wenig Holz: Menge wird genannt", any("Holz" in g and "fehlen" in g for g in p["gruende"]),
          str(p["gruende"]))
    check("zu wenig Holz: kein Stein-Grund (Stein reicht)", not any("Stein" in g for g in p["gruende"]),
          str(p["gruende"]))

    ausbau = ort(zustand=40.0)
    p = dorfwall.reparatur_pruefen(ausbau, FORSCHUNG_OK, ausbau.vorraete,
                                   {"a": {"gebiet": "Verteidigungsanlagen", "stufe": 4}})
    check("Ausbau laeuft: gesperrt", p["moeglich"] is False and any("ausgebaut" in g for g in p["gruende"]),
          str(p["gruende"]))

    laufend = ort(zustand=40.0)
    dorfwall.reparatur_starten(laufend, FORSCHUNG_OK, laufend.vorraete, 0.0)
    p = dorfwall.reparatur_pruefen(laufend, FORSCHUNG_OK, laufend.vorraete, None, 10.0)
    check("Reparatur laeuft schon: gesperrt", p["moeglich"] is False
          and any("bereits eine Reparatur" in g for g in p["gruende"]), str(p["gruende"]))


def test_buchung_atomar():
    """5./6. Atomare Buchung, genau einmal."""
    abschnitt("5. Atomare Buchung")
    arm = ort(zustand=50.0, holz=4.0, stein=1000.0)                 # Holz reicht nicht fuer 24
    vorher = dict(arm.vorraete)
    ok, meldung = dorfwall.reparatur_starten(arm, FORSCHUNG_OK, arm.vorraete, 0.0)
    check("Start scheitert", ok is False, meldung)
    check("Lager unveraendert (kein Teilabzug)", arm.vorraete == vorher, str(arm.vorraete))
    check("keine Reparatur gesetzt", dorfwall.reparatur_laeuft(arm) is False)

    gut = ort(zustand=50.0, holz=1000.0, stein=1000.0)
    preis = dorfwall.reparatur_preis(3, 50.0)                        # Stufe 3: 24/24
    ok, meldung = dorfwall.reparatur_starten(gut, FORSCHUNG_OK, gut.vorraete, 0.0)
    check("Start gelingt", ok is True, meldung)
    check("Holz genau einmal gebucht", gut.vorraete["holz"] == 1000.0 - preis["holz"], str(gut.vorraete))
    check("Stein genau einmal gebucht", gut.vorraete["stein"] == 1000.0 - preis["stein"])
    check("kein negativer Bestand", gut.vorraete["holz"] >= 0 and gut.vorraete["stein"] >= 0)
    zweiter = dorfwall.reparatur_starten(gut, FORSCHUNG_OK, gut.vorraete, 5.0)
    check("zweiter Start bucht nicht nach", zweiter[0] is False and gut.vorraete["holz"] == 1000.0 - preis["holz"],
          str(gut.vorraete))


def test_tick():
    """7. Zustand steigt stueckweise und endet auf 100."""
    abschnitt("7. Tick laesst den Zustand steigen")
    s = ort(zustand=40.0)
    dorfwall.reparatur_starten(s, FORSCHUNG_OK, s.vorraete, 0.0)
    dauer = dorfwall.reparatur_sekunden(40.0)                        # 60 Punkte = 21600
    dorfwall.reparatur_tick(s, dauer * 0.5, FORSCHUNG_OK)
    mitte = float(s.mauer_zustand)
    check("nach der Haelfte steht der Zustand zwischen 40 und 100", 40.0 < mitte < 100.0, str(mitte))
    check("die Haelfte trifft etwa 70", abs(mitte - 70.0) < 1.0, str(mitte))
    fertig = dorfwall.reparatur_tick(s, dauer + 1.0, FORSCHUNG_OK)
    check("am Ende fertig gemeldet", fertig is True)
    check("Zustand steht auf 100", float(s.mauer_zustand) == 100.0, str(s.mauer_zustand))
    check("danach laeuft keine Reparatur mehr", dorfwall.reparatur_laeuft(s) is False)


def test_abbruch():
    """8./9. Abbruch durch Angriff und durch Stufenwechsel."""
    abschnitt("8. Abbruch")
    s = ort(zustand=50.0)
    dorfwall.reparatur_starten(s, FORSCHUNG_OK, s.vorraete, 0.0)
    dorfwall.reparatur_tick(s, dorfwall.reparatur_sekunden(50.0) * 0.5, FORSCHUNG_OK)
    stand = float(s.mauer_zustand)
    check("Abbruch meldet Erfolg", dorfwall.reparatur_abbrechen(s) is True)
    check("keine Reparatur mehr", dorfwall.reparatur_laeuft(s) is False)
    check("der Zustand bleibt stehen", float(s.mauer_zustand) == stand, str(s.mauer_zustand))
    check("zweiter Abbruch meldet nichts", dorfwall.reparatur_abbrechen(s) is False)

    t = ort(zustand=30.0)
    dorfwall.reparatur_starten(t, FORSCHUNG_OK, t.vorraete, 0.0)     # Stufe 3 gemerkt
    dorfwall.reparatur_tick(t, 1000.0, {"Verteidigungsanlagen": 4})   # Stufe steigt auf 4
    check("Stufenwechsel bricht ab", dorfwall.reparatur_laeuft(t) is False)
    check("nach dem Stufenwechsel kein Fortschritt mehr", float(t.mauer_zustand) < 100.0, str(t.mauer_zustand))


def test_speichern():
    """10. Die Felder ueberleben Speichern und Laden."""
    abschnitt("10. Felder im Spielstand")
    import tkinter as tk
    wurzel = tk.Tk()
    wurzel.withdraw()
    try:
        app = main.NebelseetalApp(wurzel)
        ziel = main.Settlement(name="Walltest", map_id="pruef")
        ziel.mauer_besetzt = True
        ziel.mauer_zustand = 55.0
        ziel.vorraete = {"holz": 500.0, "stein": 500.0}
        ziel.mauer_reparatur_ziel = 100.0
        ziel.mauer_reparatur_ende = 9999.0
        ziel.mauer_reparatur_stufe = 2
        ziel.mauer_reparatur_start_zustand = 55.0
        ziel.mauer_reparatur_start_zeit = 100.0
        app.state.settlements = [ziel]
        pfad = os.path.join(tempfile.gettempdir(), "pruef_s2_wall.json")
        app.state.save(pfad)
        gespeichert = json.load(open(pfad, encoding="utf-8"))
        feld = (gespeichert.get("settlements") or [{}])[0]
        check("das Ziel steht im Spielstand", feld.get("mauer_reparatur_ziel") == 100.0, str(feld.keys())[:80])
        check("die Stufe steht im Spielstand", feld.get("mauer_reparatur_stufe") == 2)
        check("der Startzustand steht im Spielstand", feld.get("mauer_reparatur_start_zustand") == 55.0)
        app.state.load(pfad)
        ort_nach = app.state.settlements[0]
        check("nach dem Laden laeuft die Reparatur weiter", dorfwall.reparatur_laeuft(ort_nach) is True)
        os.remove(pfad)
    finally:
        wurzel.destroy()


def test_anzeige_und_kern():
    """11. Anzeige und Kern lesen dieselbe Funktion."""
    abschnitt("11. Anzeige = Kern (F-04)")
    quelle = inspect.getsource(main.NebelseetalApp._mauer_reparatur_block)
    check("die Anzeige ruft dorfwall.reparatur_pruefen", "dorfwall.reparatur_pruefen" in quelle)
    check("die Anzeige rechnet keinen eigenen Preis", "16 *" not in quelle and "WALLPREIS" not in quelle)
    kern = inspect.getsource(main.GameState.mauer_reparatur_starten)
    check("der Kern ruft dorfwall.reparatur_starten", "dorfwall.reparatur_starten" in kern)
    check("der Kern bucht nicht selbst", "vorraete[" not in kern)


def main_test():
    """Fuehrt alle Pruefungen aus und meldet das Ergebnis."""
    test_preis()
    test_dauer()
    test_gesperrt()
    test_buchung_atomar()
    test_tick()
    test_abbruch()
    test_speichern()
    test_anzeige_und_kern()
    return bericht()


if __name__ == "__main__":
    sys.exit(main_test())
