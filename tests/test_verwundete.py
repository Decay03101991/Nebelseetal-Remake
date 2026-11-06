# -*- coding: ascii -*-
"""Verwundetenheilung - S3 (06.11.2026).

Zahlen aus `docs/S0_TABELLEN_20261107.md` (V-2) und Daniels Entscheidungen 6 und 6a:
  * 30 Prozent der Verluste je Einheitentyp werden verwundet, ABGERUNDET.
  * Heilung kostet 75 Prozent der Kostenposten aus `data/units.json` - ohne `siedler`, ohne `waren`.
  * Heildauer 50 Prozent der Ausbildungsdauer der Stufe (Stufe 1: 1200 s -> 600 s).
  * Alle Zahlen stehen in `data/verwundete.json` - kein Prozentwert im Code.

Was diese Datei beweist
-----------------------
1. Ohne Verluste entstehen keine Verwundeten.
2. Die 30 Prozent werden ABGERUNDET (10 -> 3, 9 -> 2, 1 -> 0) und je Typ einzeln gerechnet.
3. Ohne bezahlbares Lager gibt es keine Heilung UND keine Buchung (atomar, nichts halb gebucht).
4. Nach der Heildauer steht die Einheit in `einheiten`, die Verwundetenzahl ist gefallen und das
   `fertigjournal` nennt die Art `heilung` (nicht `einheit`).
5. Ein alter Spielstand ohne das Feld `verwundete` laedt (Vorgabe leer, keine Migration).
6. Der Schalter `aktiv` in der Datendatei schaltet die Mechanik wirklich ab.
7. `main.GameState._verwundete_buchen` schreibt die Zahl an die Siedlung (Kernweg).
8. Kern und Anzeige lesen DIESELBE Funktion (Quellwache: kein zweiter Prozentsatz im Code).

Aufruf:  python -X utf8 tests/test_verwundete.py
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(WURZEL, "src"))
sys.path.insert(0, os.path.join(WURZEL, "tests"))

from harness import abschnitt, bericht, check                      # noqa: E402
import main                                                        # noqa: E402
import spieloekonomie                                              # noqa: E402
import verwundete                                                  # noqa: E402

FORSCHUNG_OK = {"Kriegskunst": 3, "Verteidigungsanlagen": 3}
EINHEIT = "Krieger"


def ort(gold=10000.0, pferde=100.0, verwundete_zahl=2, stufe=1):
    """Ein Orts-dict, wie es der Kern liest: Kaserne auf Feld 7, Lager mit Gold und Pferden."""
    return {"id": "ort-1", "name": "Testort", "bevoelkerung": 10.0,
            "vorraete": {"gold": gold, "pferde": pferde}, "waren": {},
            "einheiten": {}, "importiert": {}, "verbrauchsjournal": [],
            "ausbildung": [], "fertigjournal": [],
            "verwundete": ({EINHEIT: verwundete_zahl} if verwundete_zahl else {}),
            "bauten": {"7": "kriegerakademie"}, "stufen": {"7": stufe}, "karte": None}


def main_lauf():
    abschnitt("1. Ohne Verluste keine Verwundeten")
    check("leere Verluste", verwundete.anteil_verwundete({}) == {})
    check("Nullverlust", verwundete.anteil_verwundete({EINHEIT: 0}) == {})
    check("keine Angabe", verwundete.anteil_verwundete(None) == {})

    abschnitt("2. 30 Prozent, abgerundet, je Typ einzeln")
    check("10 Verluste -> 3", verwundete.anteil_verwundete({EINHEIT: 10}) == {EINHEIT: 3})
    check("9 Verluste -> 2", verwundete.anteil_verwundete({EINHEIT: 9}) == {EINHEIT: 2})
    check("4 Verluste -> 1", verwundete.anteil_verwundete({EINHEIT: 4}) == {EINHEIT: 1})
    check("3 Verluste -> 0", verwundete.anteil_verwundete({EINHEIT: 3}) == {})
    check("1 Verlust -> 0", verwundete.anteil_verwundete({EINHEIT: 1}) == {})
    gemischt = verwundete.anteil_verwundete({EINHEIT: 10, "Kaempfer": 9, "Bogenschuetze": 1})
    check("zwei Typen", gemischt == {EINHEIT: 3, "Kaempfer": 2}, str(gemischt))

    abschnitt("3. Preis und Dauer aus den belegten Zahlen (V-2)")
    kosten = verwundete.heilungskosten(EINHEIT)
    check("Krieger kostet 262,5 Gold", abs(kosten.get("gold", 0) - 262.5) < 1e-6, str(kosten))
    check("Krieger kostet 0,75 Pferde", abs(kosten.get("pferde", 0) - 0.75) < 1e-6)
    check("kein Siedler im Heilpreis", "siedler" not in kosten)
    check("keine Ausruestung im Heilpreis", "waren" not in kosten)
    check("Heildauer Stufe 1 = 600 s", abs(verwundete.heilungsdauer(EINHEIT) - 600.0) < 1e-6)

    abschnitt("4. Ohne bezahlbares Lager keine Heilung und keine Buchung")
    arm = ort(gold=1.0)
    vorher = json.dumps(arm, sort_keys=True)
    grund = ""
    try:
        verwundete.heilung_start_menge(arm, EINHEIT, FORSCHUNG_OK, 0.0, 1)
    except ValueError as fehler:
        grund = str(fehler)
    check("Heilung wirft mit Grund", "gold" in grund or "fehlt" in grund, grund)
    check("Ort unveraendert (atomar)", json.dumps(arm, sort_keys=True) == vorher)

    abschnitt("5. Nach der Heildauer steht die Einheit in der Armee")
    frisch = ort()
    ergebnis = verwundete.heilung_start_menge(frisch, EINHEIT, FORSCHUNG_OK, 1000.0, 1)
    danach = ergebnis["ort"]
    check("Verwundete abgezogen", danach["verwundete"].get(EINHEIT, 0) == 1,
          str(danach["verwundete"]))
    check("Gold gebucht", abs(float(danach["vorraete"]["gold"]) - (10000.0 - 262.5)) < 1e-6,
          str(danach["vorraete"]["gold"]))
    check("eine Heilung in der Schlange", len(danach["ausbildung"]) == 1)
    check("Zeile ist als Heilung gekennzeichnet", bool(danach["ausbildung"][0].get("heilung")))
    check("Dauer der Zeile 600 s",
          abs(float(danach["ausbildung"][0]["dauer_sekunden"]) - 600.0) < 1e-6)
    spieloekonomie.ausbildung_abschluss(danach, ergebnis["ende"] + 1.0)
    check("Einheit steht nach der Dauer im Ort", danach["einheiten"].get(EINHEIT) == 1,
          str(danach["einheiten"]))
    letzte = (danach["fertigjournal"] or [{}])[-1]
    check("Journal nennt die Art heilung", letzte.get("art") == "heilung", str(letzte))

    abschnitt("6. Zwei Verwundete, Menge 2 - beide in der Schlange")
    zwei = ort(verwundete_zahl=2)
    beides = verwundete.heilung_start_menge(zwei, EINHEIT, FORSCHUNG_OK, 0.0, 2)
    check("zwei Zeilen", len(beides["ort"]["ausbildung"]) == 2)
    check("keine Verwundeten mehr", beides["ort"]["verwundete"].get(EINHEIT, 0) == 0)
    check("Menge 3 wird abgelehnt", _wirft(verwundete.heilung_start_menge, zwei, EINHEIT,
                                           FORSCHUNG_OK, 0.0, 3))

    abschnitt("7. Alter Spielstand ohne das Feld laedt")
    alt = main.Settlement(name="Alt", map_id="m1")
    check("Settlement ohne Feld hat leere Verwundete", alt.verwundete == {})
    check("Feld ist ein eigenes dict", alt.verwundete is not main.Settlement(name="X",
                                                                            map_id="m2").verwundete)

    abschnitt("8. Der Kernweg schreibt Verwundete an die Siedlung")
    siedlung = main.Settlement(name="Ort", map_id="m1")
    # Der Kernweg schreibt jetzt auch den VERLUSTBERICHT (Block 5, Typ `verlust`) - dafuer braucht
    # der Aufruf ein Postfach. Ein leerer Stellvertreter genuegt, weil die Methode nur `messages` liest.
    app = type("Stellvertreter", (), {"messages": []})()
    neu = main.GameState._verwundete_buchen(app, siedlung, {EINHEIT: 10, "Kaempfer": 9}, "Testort")
    check("drei Verwundete gebucht", siedlung.verwundete.get(EINHEIT) == 3, str(siedlung.verwundete))
    check("zwei Verwundete beim zweiten Typ", siedlung.verwundete.get("Kaempfer") == 2)
    check("Rueckgabe nennt die Zahl", neu == {EINHEIT: 3, "Kaempfer": 2}, str(neu))
    check("keine Verluste -> keine Buecherung",
          main.GameState._verwundete_buchen(app, siedlung, {}) == {})
    check("genau EIN Verlustbericht", len(app.messages) == 1, str(len(app.messages)))
    check("Verlustbericht traegt den Typ verlust",
          (app.messages[0].get("type") if app.messages else "") == "verlust",
          str(app.messages[:1]))
    check("Verlustbericht nennt den Anlass", "Testort" in str(app.messages[0].get("text", "")))

    abschnitt("9. Der Schalter in der Datendatei schaltet die Mechanik ab")
    alt_pfad = verwundete.DATENDATEI
    with tempfile.TemporaryDirectory() as ordner:
        datei = os.path.join(ordner, "verwundete.json")
        with open(datei, "w", encoding="utf-8") as zeiger:
            json.dump({"aktiv": False, "verwundeten_anteil_prozent": 30}, zeiger)
        verwundete.DATENDATEI = type(alt_pfad)(datei)
        try:
            check("aktiv ist aus", verwundete.aktiv() is False)
            still = main.Settlement(name="Still", map_id="m1")
            still_app = type("Stellvertreter", (), {"messages": []})()
            check("Kernweg bucht nichts",
                  main.GameState._verwundete_buchen(still_app, still, {EINHEIT: 10}) == {})
            check("Verlustbericht kommt TROTZdem (haengt nicht am Schalter)",
                  len(still_app.messages) == 1)
            check("Siedlung bleibt leer", still.verwundete == {})
        finally:
            verwundete.DATENDATEI = alt_pfad
    check("Schalter wieder an", verwundete.aktiv() is True)

    abschnitt("10. Kern und Anzeige lesen dieselbe Funktion (Quellwache)")
    with open(os.path.join(WURZEL, "src", "main.py"), encoding="utf-8", errors="replace") as zeiger:
        quelle = zeiger.read()
    check("main nutzt anteil_verwundete", "verwundetenheilung.anteil_verwundete(" in quelle)
    check("main nutzt heilung_grenzen", "verwundetenheilung.heilung_grenzen(" in quelle)
    check("main nutzt heilung_start_menge", "verwundetenheilung.heilung_start_menge(" in quelle)
    # Die Quellwache schaut NUR in die Buchungs- und Anzeigefunktion: dort darf kein zweiter
    # Prozentsatz stehen, sonst rechneten Kern und Anzeige mit zwei Wahrheiten (F-04-Muster).
    import inspect                                                    # Quelltext der Methoden lesen
    buchung = inspect.getsource(main.GameState._verwundete_buchen)     # Kernweg der Verwundeten
    anzeige = inspect.getsource(main.NebelseetalApp._heilung_zeile_zeichnen)   # Anzeige-Zeile
    # Docstrings zaehlen nicht als Code (sie erklaeren die 30 Prozent) - erst abschneiden.
    buchung_code = buchung.split('"""')[2] if buchung.count('"""') >= 2 else buchung
    # Auch Kommentare zaehlen nicht - sie nennen die 30 Prozent absichtlich. Nur Code pruefen.
    buchung_code = "\n".join(zeile.split("#")[0] for zeile in buchung_code.splitlines())
    # Geprueft wird nur die RECHNUNG, nicht das Prozentzeichen der Textformatierung
    # ("Verlustbericht%s: %s" % ...) - sonst schlaegt die Wache auf die Meldung an, nicht auf Zahlen.
    check("kein zweiter Prozentsatz im Kernweg",
          "0.3" not in buchung_code and "* 30" not in buchung_code
          and "30 *" not in buchung_code and "/ 100" not in buchung_code)
    check("kein zweiter Prozentsatz in der Anzeige",
          "0.75" not in anzeige and "0.5" not in anzeige)


def _wirft(funktion, *argumente) -> bool:
    try:
        funktion(*argumente)
        return False
    except ValueError:
        return True


if __name__ == "__main__":
    main_lauf()
    bericht()
