# -*- coding: ascii -*-
"""F-04: EINE Prueffunktion fuer Warenvoraussetzungen - Kern UND Anzeige, Quelle warenrezepte.json.

Der Befund (externe Spielpruefung 31.10.2026, Register 68): die Anzeige las `data/items.json`
(Feld `voraussetzung_struktur`) und gab bei FEHLENDER Struktur `True` zurueck ("erlaubt"), waehrend
der Kern `data/warenrezepte.json` prueft. Bei Lederruestung und Magischem Paladinharnisch fehlt die
Struktur in `items.json`, im Rezept stehen aber je ZWEI Bedingungen (UND). Ergebnis: der Knopf war
frei, die Herstellung wurde abgelehnt - zwei Wahrheiten, beide gruen geprueft.

Was diese Datei beweist
-----------------------
1. Datenlage: 17 Waren, jede Bedingung nennt eine Forschung, die das Spiel kennt (sonst waere sie
   nie erfuellbar).
2. Der alte Fehler ist belegbar und behoben: es gibt Waren mit Bedingung(en) OHNE Strukturfeld in
   `items.json`; die neue Funktion sagt fuer sie bei Stufe 0 NEIN (frueher: True).
3. Vollstaendigkeit AUS DEN DATEN (keine zweite Handliste): jede Ware, jede Bedingung, Grenzfaelle
   -1 / exakt Soll / +1; UND-Bedingungen einzeln: fehlt eine, ist die Ware gesperrt.
4. Kern: `spieloekonomie.ware_start` lehnt mit einer Meldung ab, die die Bedingung im Klartext nennt.
5. Anzeige == Kern: `GameState.ware_voraussetzung` liefert fuer alle 17 Waren dieselbe Entscheidung
   wie der Kern (drei Stufen-Saetze), und `ware_voraussetzungen` die Bedingungsliste.
6. Quelltext-Wachen: die Anzeige liest `warenrezepte.json` ueber `spieloekonomie.ware_voraussetzung`
   und NICHT mehr `items.json`; der Kern prueft ueber dieselbe Funktion; die Werkstattansicht zeigt
   jede Bedingung einzeln.

Aufruf:  python -X utf8 tests/test_ware_voraussetzung_eine_quelle.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "quelltext"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['main:*', 'spieloekonomie', 'stimmen']
PRUEF_DATEN = ['items.json', 'research.json', 'warenrezepte.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import ast
import inspect
import json
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, befund, bericht, check, import_src

ROOT, SRC = import_src()
import main  # noqa: E402
import spieloekonomie  # noqa: E402


def _daten(datei):
    with open(os.path.join(ROOT, "data", datei), encoding="utf-8") as f:
        return json.load(f)


REZEPTE = spieloekonomie.WARENREZEPTE
ITEMS = _daten("items.json")["waren"]
FORSCHUNGEN = _daten("research.json")["forschungen"]


def _code(funktion):
    """Der Quelltext einer Funktion OHNE Docstring (ein Docstring ist kein ausgefuehrter Code)."""
    quelle = textwrap.dedent(inspect.getsource(funktion))
    baum = ast.parse(quelle)
    knoten = baum.body[0]
    rumpf = getattr(knoten, "body", [])
    if (rumpf and isinstance(rumpf[0], ast.Expr)
            and isinstance(getattr(rumpf[0], "value", None), ast.Constant)
            and isinstance(rumpf[0].value.value, str)):
        knoten.body = rumpf[1:]
    return ast.unparse(knoten)


def _bedingungen(ware):
    """(gebiet, stufe) je Bedingung - aus den Daten, nie getippt."""
    return list((REZEPTE[ware].get("voraussetzungen") or {}).items())


def _stufen(saetze):
    """Stufenkarte aus {Gebiet: Stufe} bauen; alle Forschungen des Spiels sind vorhanden (=0)."""
    karte = {name: 0 for name in FORSCHUNGEN}
    karte.update(saetze)
    return karte


def main_lauf():
    print("F-04 - eine Prueffunktion fuer Kern UND Anzeige (Quelle warenrezepte.json)\n")

    # ---------------------------------------------------------------- 1. Datenlage
    abschnitt("1. Datenlage: 17 Waren, Bedingungen aus bekannten Forschungen")
    check("warenrezepte.json fuehrt 17 Waren", len(REZEPTE) == 17, str(len(REZEPTE)))
    check("items.json fuehrt dieselben 17 Waren", set(REZEPTE) == set(ITEMS),
          str(sorted(set(REZEPTE) ^ set(ITEMS))))
    unbekannt = sorted({g for w in REZEPTE for g, _ in _bedingungen(w)
                        if g not in FORSCHUNGEN})
    check("jede Bedingung nennt eine bekannte Forschung", not unbekannt, str(unbekannt))
    mit_bedingung = [w for w in REZEPTE if _bedingungen(w)]
    ohne_bedingung = [w for w in REZEPTE if not _bedingungen(w)]
    check("es gibt Waren ohne Voraussetzung (Messer, Wollumhang ...)",
          len(ohne_bedingung) >= 2, str(ohne_bedingung))
    print(f"    Waren mit Bedingung: {len(mit_bedingung)} | ohne: {len(ohne_bedingung)}")

    # ------------------------------------------------- 2. Der alte Fehler, belegt
    abschnitt("2. Der alte Fehler ist belegbar - und die neue Funktion sieht ihn")
    ohne_struktur = [w for w in mit_bedingung
                     if not (ITEMS.get(w) or {}).get("voraussetzung_struktur")]
    check("es gibt Waren mit Bedingung OHNE Strukturfeld in items.json (der alte Fehler)",
          bool(ohne_struktur), str(ohne_struktur))
    zwei_bedingungen = [w for w in ohne_struktur if len(_bedingungen(w)) >= 2]
    check("darunter sind Waren mit ZWEI Bedingungen (UND)", len(zwei_bedingungen) >= 2,
          str(zwei_bedingungen))
    for ware in ohne_struktur:
        erfuellt, grund = spieloekonomie.ware_voraussetzung(ware, _stufen({}))
        check(f"bei Stufe 0 gesperrt: {ware}", erfuellt is False, grund)
    for ware in zwei_bedingungen:
        grund = spieloekonomie.ware_voraussetzung(ware, _stufen({}))[1]
        gebiete = [g for g, _ in _bedingungen(ware)]
        check(f"die Begruendung nennt BEIDE Bedingungen: {ware}",
              all(g in grund for g in gebiete), grund)

    # --------------------------------------------------------- 3. Grenzfaelle
    abschnitt("3. Grenzfaelle je Bedingung: -1 / exakt Soll / +1 (aus den Daten)")
    grenz_fehler = []
    geprueft = 0
    for ware in mit_bedingung:
        for gebiet, noetig in _bedingungen(ware):
            noetig = int(noetig)
            rest = {g: int(n) for g, n in _bedingungen(ware) if g != gebiet}
            # die jeweils ANDERE Bedingung ist erfuellt - geprueft wird genau eine
            if noetig > 0:
                zu_wenig = spieloekonomie.ware_voraussetzung(
                    ware, _stufen({**rest, gebiet: noetig - 1}))[0]
                if zu_wenig is not False:
                    grenz_fehler.append(f"{ware}/{gebiet} Soll {noetig}: -1 war {zu_wenig}")
            exakt = spieloekonomie.ware_voraussetzung(
                ware, _stufen({**rest, gebiet: noetig}))[0]
            if exakt is not True:
                grenz_fehler.append(f"{ware}/{gebiet} Soll {noetig}: exakt war {exakt}")
            if len(rest) < len(_bedingungen(ware)):  # UND: andere Bedingung fehlt absichtlich nicht
                mehr = spieloekonomie.ware_voraussetzung(
                    ware, _stufen({**rest, gebiet: noetig + 1}))[0]
                if mehr is not True:
                    grenz_fehler.append(f"{ware}/{gebiet} Soll {noetig}: +1 war {mehr}")
            geprueft += 3
    check(f"alle Grenzfaelle stimmen ({geprueft} Pruefungen ueber {len(mit_bedingung)} Waren)",
          not grenz_fehler, str(grenz_fehler[:3]))

    # UND-Bedingungen: eine fehlt -> gesperrt, beide da -> frei
    und_fehler = []
    for ware in mit_bedingung:
        bedingungen = _bedingungen(ware)
        if len(bedingungen) < 2:
            continue
        for index, (gebiet, noetig) in enumerate(bedingungen):
            karte = {g: int(n) for g, n in bedingungen}
            karte[gebiet] = int(noetig) - 1  # genau diese eine Bedingung reisst
            if spieloekonomie.ware_voraussetzung(ware, _stufen(karte))[0] is not False:
                und_fehler.append(f"{ware}: fehlende Bedingung {gebiet} wurde nicht gesehen")
    check("UND: fehlt EINE Bedingung, ist die Ware gesperrt", not und_fehler, str(und_fehler))
    alle_da = {w: {g: int(n) for g, n in _bedingungen(w)} for w in mit_bedingung}
    frei = [w for w, karte in alle_da.items()
            if spieloekonomie.ware_voraussetzung(w, _stufen(karte))[0] is not True]
    check("sind ALLE Bedingungen erfuellt, ist jede Ware frei", not frei, str(frei))

    # ---------------------------------------------------------------- 4. Kern
    abschnitt("4. Kern: ware_start prueft ueber dieselbe Funktion")
    kern_fehler = []
    for ware in mit_bedingung:
        try:
            spieloekonomie.ware_start({"werkstaetten": {}, "vorraete": {}}, ware, _stufen({}), 0.0)
            kern_fehler.append(f"{ware}: ohne Forschung NICHT abgelehnt")
        except ValueError as fehler:
            if "Warenvoraussetzung" not in str(fehler):
                kern_fehler.append(f"{ware}: falscher Grund {fehler}")
    check("ohne Forschung lehnt der Kern JEDE Ware mit Bedingung ab", not kern_fehler,
          str(kern_fehler[:3]))
    for ware in ohne_bedingung:
        try:
            spieloekonomie.ware_start({"werkstaetten": {}, "vorraete": {}}, ware, _stufen({}), 0.0)
            kern_fehler.append(f"{ware}: haette ohne Werkstatt abgelehnt werden muessen")
        except ValueError as fehler:
            if "Warenvoraussetzung" in str(fehler):
                kern_fehler.append(f"{ware}: Voraussetzung erfunden, obwohl keine belegt ist")
    check("ohne belegte Voraussetzung erfindet der Kern keine", not kern_fehler,
          str(kern_fehler[:3]))
    # Meldung nennt die Bedingung im Klartext
    probe = zwei_bedingungen[0] if zwei_bedingungen else mit_bedingung[0]
    try:
        spieloekonomie.ware_start({"werkstaetten": {}, "vorraete": {}}, probe, _stufen({}), 0.0)
        meldung = ""
    except ValueError as fehler:
        meldung = str(fehler)
    check(f"die Ablehnung nennt die Bedingung im Klartext ({probe})",
          all(g in meldung for g, _ in _bedingungen(probe)), meldung)

    # ------------------------------------------------------------- 5. Anzeige
    abschnitt("5. Anzeige == Kern: GameState fuer alle 17 Waren, drei Stufen-Saetze")
    gs = ausnahme("GameState anlegen", main.GameState)
    if gs is None:
        return bericht()
    saetze = [{}, {g: int(n) - 1 for w in mit_bedingung for g, n in _bedingungen(w)},
              {g: int(n) + 1 for w in mit_bedingung for g, n in _bedingungen(w)}]
    abweichung = []
    for saetze_index, satz in enumerate(saetze):
        karte = _stufen(satz)
        for name, stand in gs.research.items():
            stand.level = int(karte.get(name, 0))
        for ware in REZEPTE:
            anzeige = gs.ware_voraussetzung(ware)[0]
            kern = spieloekonomie.ware_voraussetzung(ware, gs._forschungsstufen())[0]
            if bool(anzeige) != bool(kern):
                abweichung.append(f"Satz {saetze_index} {ware}: Anzeige {anzeige}, Kern {kern}")
    check("Anzeige und Kern entscheiden bei allen 17 Waren gleich", not abweichung,
          str(abweichung[:3]))
    listen_fehler = [w for w in REZEPTE
                     if len(gs.ware_voraussetzungen(w)) != len(_bedingungen(w))]
    check("die Bedingungsliste hat je Ware genau so viele Eintraege wie das Rezept",
          not listen_fehler, str(listen_fehler))
    for name, stand in gs.research.items():
        stand.level = 0
    zwei = gs.ware_voraussetzungen(zwei_bedingungen[0]) if zwei_bedingungen else []
    check("jede Bedingung ist einzeln sichtbar (Gebiet, Soll, Ist, Urteil)",
          bool(zwei) and all({"gebiet", "noetig", "vorhanden", "erfuellt"} <= set(b) for b in zwei),
          str(zwei))
    check("eine unbekannte Ware gilt als NICHT erfuellt (der Kern lehnt sie ab)",
          gs.ware_voraussetzung("Gibtesnicht")[0] is False, gs.ware_voraussetzung("Gibtesnicht")[1])

    # --------------------------------------------------- 6. Quelltext-Wachen
    abschnitt("6. Quelltext-Wachen: eine Quelle, keine zweite Wahrheit")
    anzeige_code = _code(main.GameState.ware_voraussetzung)
    check("die Anzeige ruft spieloekonomie.ware_voraussetzung",
          "spieloekonomie.ware_voraussetzung(" in anzeige_code, anzeige_code[:120])
    check("die Anzeige liest NICHT mehr items.json", "WARE_EINTRAEGE" not in anzeige_code
          and "voraussetzung_struktur" not in anzeige_code, anzeige_code[:120])
    check("die Anzeige gibt nicht mehr bei fehlender Struktur True zurueck",
          "keine Voraussetzung belegt" not in anzeige_code, anzeige_code[:120])
    kern_code = _code(spieloekonomie.ware_start_menge)
    check("der Kern prueft ueber ware_voraussetzung(",
          "ware_voraussetzung(" in _code(spieloekonomie.ware_grenzen),
          kern_code[:120])
    check("der Kern prueft NICHT mehr selbst die Rezeptbedingungen",
          'rezept["voraussetzungen"]' not in kern_code, kern_code[:120])
    einheit_code = _code(spieloekonomie.ware_voraussetzung)
    liste_code = _code(spieloekonomie.ware_voraussetzungen_liste)
    check("die eine Lesestelle liest die Bedingungen aus dem Rezept",
          "voraussetzungen" in liste_code and "rezept" in liste_code, liste_code[:120])
    check("die Prueffunktion baut auf dieser Lesestelle auf",
          "ware_voraussetzungen_liste(" in _code(spieloekonomie.ware_voraussetzung),
          einheit_code[:120])

    # ANGEPASST 13.11.2026 (Nr. 16 Teil A): Die Bedingungen einer Ware stehen seit dem Umbau im
    # Auswahl-Block des Dorfzentrums (`_dz_auswahl_werkstatt`) - die Dorfzentrum-Methoden heissen
    # jetzt `_dz_*`. Die Aussage bleibt: EINE Ansicht zeigt sie einzeln.
    ansicht = [n for n in dir(main.NebelseetalApp)
               if n.startswith("_render_") or n.startswith("_dz_")]
    treffer = []
    for name in ansicht:
        try:
            if "ware_voraussetzungen(" in _code(getattr(main.NebelseetalApp, name)):
                treffer.append(name)
        except (OSError, TypeError, SyntaxError, IndentationError):
            continue
    check("eine Ansicht zeigt die Bedingungen EINZELN an", bool(treffer), str(treffer))
    check("der Bedingungstext kommt aus _ware_bedingung_text",
          any("_ware_bedingung_text(" in _code(getattr(main.NebelseetalApp, n)) for n in treffer),
          str(treffer))
    text_code = _code(main.NebelseetalApp._ware_bedingung_text)
    check("der Text nennt erfuellt/offen und die Stufen",
          "erfuellt" in text_code and "offen" in text_code, text_code[:120])

    if len(zwei_bedingungen) >= 2:
        befund("die zwei UND-Waren dieser Datenlage: " + ", ".join(zwei_bedingungen))
    return bericht()


sys.exit(main_lauf())
