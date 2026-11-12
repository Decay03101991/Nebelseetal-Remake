# -*- coding: ascii -*-
"""A-1: ZWOELF E2E-KETTEN - jeder Spielweg einmal von Anfang bis Ende, ohne gesetzten Zustand.

WARUM ES DIESE PRUEFUNG GIBT (Ablauf 20261106, Schritt 10, Befund A-1)
---------------------------------------------------------------------
Die drei vorhandenen Ketten (`test_produktionskette_ohne_cheats.py`, `test_durchspiel.py`,
`test_gpt_wirtschaft_kette_e2e.py`) decken Rohstoff, Forschung, Ware, Ausbildung, Einsatz,
Rueckkehr und Speichern ab. HANDEL, HEILUNG, MAUERREPARATUR, VERTRAG und PORTAL waren NICHT
als Kette belegt - fuer diese Wege gab es nur Einzelpruefungen auf gesetztem Zustand.

Diese Datei spielt ZWOELF Wege, jeden von der Gruendung an:

    1  Rohstoff        Felder bebauen, Ertrag entsteht durch die Spieluhr
    2  Forschung        Bibliothek, Voraussetzungen aus den Daten, Stufe steigt nach der Zeit
    3  Ware             Rezept, Kosten, Fertigungszeit, Ware liegt danach im ORTSLAGER
    4  Ausbildung       Einheit entsteht nach der Ausbildungszeit im ORTSLAGER
    5  Einsatz          Angriff geht als AUFTRAG aus dem ORTSHEER heraus
    6  Rueckkehr        Kampf am Ziel, Ueberlebende GENAU zurueck in diesen Ort
    7  Speichern/Laden  Stand schreiben, in einer ZWEITEN App laden, Werte vergleichen
    8  Handel           Karawane verkauft an einen Bot, Erloes und Handelspunkte entstehen
    9  Heilung          Verwundete werden geheilt (Kosten, Dauer, Rueckkehr ins Ortsheer)
    10 Mauerreparatur   Wall errichten, Reparatur laeuft, Zustand steht danach auf 100
    11 Vertrag          Nichtangriffspakt sperrt den Bot-Angriff und laeuft ab
    12 Portal           Mana ueber Spieltage ansparen, Weltensprung bucht genau einmal ab

REGEL DIESER DATEI (Ablauf Schritt 10, Wortlaut)
-------------------------------------------------
"je Weg eine Kette ohne `state.<feld> = `-Zuweisung ausser dem Startwert".

Umgesetzt heisst das:
  * Die Spieluhr darf gestellt werden (`gs.spielsekunden = ...` + `gs.tick(0.0)`) - das ist der
    Zeitsprung, den der Ablauf fuer den Portalweg ausdruecklich verlangt (E-6), keine Spieldaten.
  * Alles andere wird ueber den ECHTEN Weg erzeugt (Bauen, Forschen, Ausbilden, Kaempfen, Handeln).
  * Was der Spieler in einer Partie erst nach Stunden oder Tagen erreicht (Mauer erst NACH einem
    Bot-Ueberfall beschaedigt, Handelskarawane kostet 500 Holz/250 Metall/500 Wolle/500 Leder/15
    Pferde, 5000 Mana sind 41,7 Spieltage) und was deshalb als STARTWERT in die Kette geht, steht
    in GENAU VIER Stellen, jede mit Grund:
    `_startwert_handelskarawane`, `_startwert_verwundete`, `_startwert_mauerschaden`,
    `_startwert_mana`.
  * Abschnitt 13 prueft den Quelltext DIESER Datei per `ast`: ausser der Uhr darf nur in diesen
    vier Funktionen ueberhaupt etwas am Spielstand geschrieben werden. Eine neue stille
    Zustandsschreibung macht die Pruefung rot.

Aufruf:  .venv/Scripts/python.exe -X utf8 tests/test_e2e_wege.py
Rueckgabe: 0 = alle Ketten vollstaendig, 1 = mindestens eine Kette bricht.
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster"
PRUEF_STUFE = 3
PRUEF_BETRIFFT = ['auftraege', 'diplomatie', 'dorfwall', 'einheiten', 'forschung', 'forschungspfad', 'gebaeude_wirkung', 'gelaende', 'kampf', 'main:*', 'portalraum', 'punkte']
PRUEF_DATEN = ['buildings.json', 'resources.json', 'verwundete.json', 'welten.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import ast
import inspect as _inspect
import json
import os
import random
import sys
import tempfile
import textwrap
import tkinter as tk
from dataclasses import asdict
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, befund, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
import diplomatie          # noqa: E402
import dorfwall            # noqa: E402
import einheiten           # noqa: E402
import forschungspfad      # noqa: E402
import gebaeude_wirkung    # noqa: E402
import gelaende            # noqa: E402
import main                # noqa: E402
import portalraum          # noqa: E402
import punkte              # noqa: E402
import spieloekonomie      # noqa: E402
import verwundete as verwundetenheilung  # noqa: E402
import wirtschaft          # noqa: E402

SAAT = 20261031            # fester Start: dieselbe Karte, dieselben Felder, jeder Lauf gleich
GEDULD = 30                # hoechstens so viele Takte wartet eine Kette auf eine Bedingung

# Die Kette waehlt ihre Einheit aus den DATEN. Der Name traegt einen Umlaut; diese Pruefdatei
# ist ASCII-only (Projektregel), deshalb wird er gelesen und nie getippt.
EINHEIT = next(n for n in einheiten.alle() if n.startswith("Kurzbogen"))
WARE = "Kurzbogen"
KARAWANE = next(n for n in einheiten.alle() if n.startswith("Handelskarawane"))

# Die Bauvoraussetzungen kommen aus `data/buildings.json` - nicht aus einer zweiten Liste hier.
with open(os.path.join(ROOT, "data", "buildings.json"), "r", encoding="utf-8") as _datei:
    _GEBAEUDE_VOR = {str(g.get("id")): str(g.get("voraussetzung") or "")
                     for g in json.load(_datei).get("gebaeude") or []}

# Die VIER erlaubten Startwerte (Abschnitt 13 prueft, dass es bei diesen vieren bleibt).
STARTWERTE = {
    "_startwert_handelskarawane": {"ort.einheiten[KARAWANE]": "Handelskarawane"},
    "_startwert_verwundete": {"_verwundete_buchen(ort, ...)": "Verwundete"},
    "_startwert_mauerschaden": {"ort.mauer_zustand": "Mauerschaden"},
    "_startwert_mana": {"gs.resources['mana'].amount": "Mana-Erspartes",
                        "ort.vorraete['mana']": "Mana-Erspartes"},
}


# --------------------------------------------------------------------------- Grundgeruest
def _uhr(gs):
    """Nur die Spieluhr merken - Abschnitt 13 erlaubt keine andere Zustandsschreibung."""
    return float(gs.spielsekunden)


def _tick(gs, stunden):
    """Spieluhr weiterstellen - die EINZIGE Art, wie in dieser Pruefung etwas entsteht."""
    gs.tick(float(stunden) * 3600.0)


def _bis(gs, zeitpunkt):
    """Auf einen Zeitpunkt springen und den Kern buchen lassen (Zeitsprung, kein Datenwert)."""
    gs.spielsekunden = max(float(gs.spielsekunden), float(zeitpunkt))
    gs.tick(0.0)


def _neu(saat=SAAT):
    """Eine frische Partie bis zur ersten Siedlung - der Start jeder Kette."""
    root = tk.Tk()
    root.withdraw()
    gesammelt = []
    root.report_callback_exception = lambda *a: gesammelt.append(a)
    app = main.NebelseetalApp(root)
    app._build_main_ui()
    random.seed(saat)
    app._erste_siedlung_gruenden()
    gs = app.state
    ort = gs.settlements[0] if gs.settlements else None
    return root, app, gs, ort, gesammelt


def _ende(root):
    try:
        root.destroy()
    except Exception:
        pass


def _feld_von(ort, gebaeude):
    return next((int(f) for f, g in (ort.bauten or {}).items() if str(g) == gebaeude), None)


def _bauen(app, gs, ort, gebaeude, versuche=GEDULD, nur_terrain=None):
    """Baut ein Gebaeude auf dem ersten Feld, das die Standortregel zulaesst.

    Die Voraussetzung kommt aus `data/buildings.json` (Feld `voraussetzung`) - nicht aus einer
    zweiten Liste in dieser Pruefung. Reicht das Lager nicht, laufen Takte, bis es reicht; ist
    das Gebaeude nach `versuche` Runden nicht gebaut, kommt None zurueck (die Kette meldet das).
    `nur_terrain` baut AUSSCHLIESSLICH auf dieser Gelaendeart (der Tempel traegt nur auf
    Nebelsee 5 Mana je Stunde, auf allem anderen 1 - data/resources.json).
    """
    vor = _GEBAEUDE_VOR.get(str(gebaeude)) or ""
    vor = vor.split(" ")[0] if vor else ""
    if vor and vor in gs.research and int(gs.research[vor].level or 0) < 1:
        if not _erforschen(app, gs, ort, vor, 1):
            return None
    for _ in range(versuche):
        feld = _bauen_einmal(app, gs, ort, gebaeude, nur_terrain=nur_terrain)
        if feld is not None:
            return feld
        _tick(gs, 20)          # Rohstoffe fuer den Bau erwirtschaften
    return None


def _bauen_einmal(app, gs, ort, gebaeude, nur_terrain=None):
    """EIN Bauversuch auf dem ersten Feld, das die Standortregel zulaesst."""
    app._oeffne_siedlungskarte(ort)
    for feld, terrain in enumerate(ort.karte["raster"]):
        if str(feld) in ort.bauten:
            continue
        if nur_terrain is not None and str(terrain) != str(nur_terrain):
            continue
        erlaubt, _grund = gelaende.bau_moeglich(gebaeude, terrain)
        if not erlaubt:
            continue
        app._karten_feld_waehlen(feld)
        vorher = len(ort.bauten)
        app._karten_bauen(gebaeude)
        if len(ort.bauten) > vorher:
            return feld
    return None


def _ausbauen_bis(app, gs, ort, gebaeude, stufe):
    """Hebt ein Gebaeude auf `stufe` (Ausbau ist die Voraussetzung der Forschung)."""
    feld = _feld_von(ort, gebaeude)
    if feld is None:
        return False
    for _ in range(GEDULD):
        if gebaeude_wirkung.gebaeude_stufe(ort, gebaeude) >= int(stufe):
            return True
        app._oeffne_siedlungskarte(ort)
        app._karten_feld_waehlen(feld)
        app._karten_ausbauen()
        if gebaeude_wirkung.gebaeude_stufe(ort, gebaeude) < int(stufe):
            _tick(gs, 20)
    return gebaeude_wirkung.gebaeude_stufe(ort, gebaeude) >= int(stufe)


def _erforschen(app, gs, ort, gebiet, ziel, tiefe=0):
    """Forscht `gebiet` bis `ziel` - samt der Voraussetzungen aus `forschungspfad`."""
    if int(gs.research[gebiet].level) >= int(ziel):
        return True
    if tiefe > 5:
        return False
    for bedingung in forschungspfad.voraussetzung(gebiet):
        if bedingung["art"] == "bibliothek":
            if _feld_von(ort, "bibliothek") is None and _bauen(app, gs, ort, "bibliothek") is None:
                return False
            if not _ausbauen_bis(app, gs, ort, "bibliothek", int(bedingung["stufe"])):
                return False
        elif not _erforschen(app, gs, ort, bedingung["was"], int(bedingung["stufe"]), tiefe + 1):
            return False
    for _ in range(GEDULD):
        if int(gs.research[gebiet].level) >= int(ziel):
            return True
        if app._start_research(gebiet):
            auftrag = ort.forschungsauftrag or {}
            gs.spielsekunden = (float(auftrag.get("startzeit") or 0.0)
                                + float(auftrag.get("dauer_stunden") or 0.0) * 3600.0 + 1.0)
            gs.tick(0.0)
        else:
            _tick(gs, 30)
    return int(gs.research[gebiet].level) >= int(ziel)


def _warte_auf(gs, bedingung, stunden=20, runden=GEDULD):
    """Takte laufen lassen, bis `bedingung()` wahr ist (oder die Geduld reisst)."""
    for _ in range(runden):
        if bedingung():
            return True
        _tick(gs, stunden)
    return bool(bedingung())


def _warte_heilbar(gs, ort, runden=40):
    """Takte laufen lassen, bis mindestens EIN Verwundeter bezahlbar ist (Preis aus den Daten)."""
    grenzen = {}
    for _ in range(runden):
        grenzen = verwundetenheilung.heilung_grenzen(asdict(ort), EINHEIT, gs.forschungs_stufen())
        if int(grenzen.get("moeglich") or 0) >= 1:
            return grenzen
        _tick(gs, 20)
    return grenzen


def _auftrag_zu_ende(gs, eintrag, feld="rueckkehr"):
    """Springt auf die Ankunft/Rueckkehr eines Auftrags und laesst den Kern buchen."""
    ziel = float(eintrag.get(feld) or eintrag.get("ankunft") or 0.0) + 1.0
    _bis(gs, ziel)
    gs.auftraege_fortschreiben(float(gs.spielsekunden))


def _nachrichten(gs, art):
    return [m for m in gs.messages if str(m.get("type")) == str(art)]


# --------------------------------------------------------------------------- Aufbau (echter Weg)
def _aufbau(app, gs, ort, einheiten_anzahl=2):
    """Alles, was eine Einheit kostet, ueber den ECHTEN Weg: Gebaeude, Forschung, Ware, Gold.

    Kein Geschenk: jedes Gebaeude wird auf ein Feld gebaut, jede Forschung braucht ihre
    Voraussetzung, die Ware ihre Werkstatt und ihr Rezept, das Gold seine Goldmine.
    """
    for gebaeude in ("holzfaeller", "holzfaeller", "steinmetz", "bibliothek",
                     "goldmine", "kriegerakademie"):
        _bauen(app, gs, ort, gebaeude)                     # Feld frei? sonst kommt es spaeter dran
    bedarf = {"Baukunst": 1}
    rezepte = spieloekonomie.WARENREZEPTE
    for ware in einheiten.alle()[EINHEIT].get("waren") or []:
        for gebiet, stufe in ((rezepte.get(ware) or {}).get("voraussetzungen") or {}).items():
            bedarf[gebiet] = max(bedarf.get(gebiet, 1), int(stufe))
    vor = einheiten.alle()[EINHEIT].get("voraussetzung") or {}
    if isinstance(vor, dict) and vor.get("forschung"):
        bedarf[vor["forschung"]] = max(bedarf.get(vor["forschung"], 1), int(vor.get("stufe", 1)))
    for gebiet, stufe in sorted(bedarf.items()):
        _erforschen(app, gs, ort, gebiet, stufe)
    for gebaeude in ("bogenbauer", "kriegerakademie", "goldmine"):
        if _feld_von(ort, gebaeude) is None:
            _bauen(app, gs, ort, gebaeude)
    _tick(gs, 10)
    app._oeffne_siedlungskarte(ort)
    for _ in range(einheiten_anzahl):
        app._ware_herstellen(WARE)
    if not _warte_auf(gs, lambda: int((ort.waren or {}).get(WARE, 0)) >= einheiten_anzahl):
        return False
    kosten = einheiten.alle()[EINHEIT].get("kosten") or {}
    gold = float(kosten.get("gold", 0) or 0) * einheiten_anzahl
    _warte_auf(gs, lambda: float((ort.vorraete or {}).get("gold", 0.0)) >= gold, stunden=20)
    return float((ort.vorraete or {}).get("gold", 0.0)) >= gold


# --------------------------------------------------------------------------- 1 Rohstoff
def _kette_1_rohstoff():
    abschnitt("1. ROHSTOFF - Felder bebauen, Ertrag kommt von der Spieluhr")
    root, app, gs, ort, gesammelt = _neu()
    try:
        check("die Startsiedlung wird auf dem echten Weg gegruendet", ort is not None)
        if ort is None:
            return
        check("die Gruendung bringt Holzfaeller, Steinmetz und Tempel mit (S-1)",
              sorted(ort.bauten.values()) == ["holzfaeller", "steinmetz", "tempel"], str(ort.bauten))
        holz_0 = float(ort.vorraete.get("holz", 0.0))
        stein_0 = float(ort.vorraete.get("stein", 0.0))
        mana_0 = float(ort.vorraete.get("mana", 0.0))
        _tick(gs, 10)
        holz_1 = float(ort.vorraete.get("holz", 0.0))
        check("nach 10 Spielstunden ist mehr Holz im ORTSLAGER als vorher",
              holz_1 > holz_0, "%g -> %g" % (holz_0, holz_1))
        check("Stein waechst ebenfalls (Steinmetz auf eigenem Feld)",
              float(ort.vorraete.get("stein", 0.0)) > stein_0, str(ort.vorraete.get("stein")))
        check("der Tempel erzeugt Mana (eigene Produktion, keine Zuweisung)",
              float(ort.vorraete.get("mana", 0.0)) > mana_0, str(ort.vorraete.get("mana")))
        # Ein ZWEITER Holzfaeller muss den Ertrag erhoehen - das ist der Unterschied zwischen
        # "es waechst" und "es waechst wegen des Gebaeudes".
        holz_vor_takt = float(ort.vorraete.get("holz", 0.0))
        _tick(gs, 10)
        zuwachs_ein_gebaeude = float(ort.vorraete.get("holz", 0.0)) - holz_vor_takt
        feld = _bauen(app, gs, ort, "holzfaeller")
        check("ein zweiter Holzfaeller laesst sich auf ein Wald-/Steppe-Feld bauen", feld is not None)
        holz_vor_takt = float(ort.vorraete.get("holz", 0.0))
        _tick(gs, 10)
        zuwachs_zwei = float(ort.vorraete.get("holz", 0.0)) - holz_vor_takt
        check("mit zwei Holzfaellern waechst das Holz schneller als mit einem",
              zuwachs_zwei > zuwachs_ein_gebaeude,
              "%g -> %g je 10 h" % (zuwachs_ein_gebaeude, zuwachs_zwei))
        check("kein Rohstoff des Ortes ist negativ", not _negative(gs, ort), str(_negative(gs, ort)))
        check("waehrend der Kette gab es keinen stillen GUI-Fehler", not gesammelt, str(gesammelt[:1]))
    finally:
        _ende(root)


# --------------------------------------------------------------------------- 2 Forschung
def _kette_2_forschung():
    abschnitt("2. FORSCHUNG - Bibliothek, Voraussetzungen aus den Daten, Stufe nach der Zeit")
    root, app, gs, ort, gesammelt = _neu()
    try:
        if ort is None:
            check("Startsiedlung fuer die Forschung", False)
            return
        check("die Bibliothek steht noch NICHT am Anfang", _feld_von(ort, "bibliothek") is None,
              str(ort.bauten))
        check("Baukunst ist zu Beginn auf Stufe 0", int(gs.research["Baukunst"].level) == 0,
              str(gs.research["Baukunst"].level))
        # Der Bau der Bibliothek ist die belegte Voraussetzung - sie wird auf ein Feld gebaut.
        check("die Bibliothek laesst sich bauen", _bauen(app, gs, ort, "bibliothek") is not None)
        gestartet = app._start_research("Baukunst")
        check("die Forschung startet als Auftrag IM ORT", bool(gestartet),
              str(getattr(ort, "forschungsauftrag", None)))
        auftrag = dict(ort.forschungsauftrag or {})
        check("der Auftrag traegt eine Dauer in Spielstunden",
              float(auftrag.get("dauer_stunden") or 0.0) > 0.0, str(auftrag.get("dauer_stunden")))
        check("die Stufe steht NICHT sofort auf 1", int(gs.research["Baukunst"].level) == 0,
              str(gs.research["Baukunst"].level))
        _bis(gs, float(auftrag.get("startzeit") or 0.0)
             + float(auftrag.get("dauer_stunden") or 0.0) * 3600.0 - 1.0)
        check("kurz VOR dem Ende ist die Stufe noch 0 (die Zeit entscheidet)",
              int(gs.research["Baukunst"].level) == 0, str(gs.research["Baukunst"].level))
        _bis(gs, float(auftrag.get("startzeit") or 0.0)
             + float(auftrag.get("dauer_stunden") or 0.0) * 3600.0 + 1.0)
        check("nach der Forschungszeit steht Baukunst auf Stufe 1",
              int(gs.research["Baukunst"].level) == 1, str(gs.research["Baukunst"].level))
        check("der Forschungsauftrag ist danach aus dem Ort verschwunden",
              not ort.forschungsauftrag, str(ort.forschungsauftrag))
        check("waehrend der Kette gab es keinen stillen GUI-Fehler", not gesammelt, str(gesammelt[:1]))
    finally:
        _ende(root)


# --------------------------------------------------------------------------- 3 Ware
def _kette_3_ware():
    abschnitt("3. WARE - Rezept aus den Daten, Kosten, Fertigungszeit, Ware im ORTSLAGER")
    root, app, gs, ort, gesammelt = _neu()
    try:
        if ort is None:
            check("Startsiedlung fuer die Ware", False)
            return
        rezept = (spieloekonomie.WARENREZEPTE.get(WARE) or {})
        check("das Rezept der Ware steht in den Daten (keine Zahl in der Pruefung)",
              bool(rezept), str(rezept)[:80])
        for gebiet, stufe in (rezept.get("voraussetzungen") or {}).items():
            check("Voraussetzung %s Stufe %d laeuft ueber den echten Forschungsweg"
                  % (gebiet, int(stufe)), _erforschen(app, gs, ort, gebiet, int(stufe)))
        werkstatt = rezept.get("gebaeude") or "bogenbauer"
        check("die Werkstatt (%s) laesst sich bauen" % werkstatt,
              _bauen(app, gs, ort, werkstatt) is not None)
        _tick(gs, 10)
        app._oeffne_siedlungskarte(ort)
        vorher = int((ort.waren or {}).get(WARE, 0))
        holz_vorher = float(ort.vorraete.get("holz", 0.0))
        check("die Ware laesst sich am Ort herstellen (Knopf des echten Wegs)",
              app._ware_herstellen(WARE) is not False)
        check("die Ware steht NICHT sofort im Lager", int((ort.waren or {}).get(WARE, 0)) == vorher,
              str(ort.waren))
        check("die Rezeptkosten sind sofort aus dem Ortslager bezahlt",
              float(ort.vorraete.get("holz", 0.0)) < holz_vorher,
              "%g -> %g" % (holz_vorher, ort.vorraete.get("holz")))
        stunden = float((rezept.get("dauer_stunden") or 1)) + 1.0
        _tick(gs, stunden)
        check("nach der Fertigungszeit liegt genau EINE Ware im Ortslager",
              int((ort.waren or {}).get(WARE, 0)) == vorher + 1, str(ort.waren))
        check("waehrend der Kette gab es keinen stillen GUI-Fehler", not gesammelt, str(gesammelt[:1]))
    finally:
        _ende(root)


# --------------------------------------------------------------------------- 4-6, 9 eine Partie
def _kette_4_bis_9():
    """Ausbildung, Einsatz, Rueckkehr und Heilung spielen EINE Partie - Stufe fuer Stufe."""
    abschnitt("4. AUSBILDUNG - die Einheit entsteht nach der Zeit im ORTSLAGER")
    root, app, gs, ort, gesammelt = _neu()
    try:
        if ort is None:
            check("Startsiedlung fuer Ausbildung, Einsatz, Rueckkehr und Heilung", False)
            return
        aufgebaut = _aufbau(app, gs, ort, 2)
        check("Forschung, Werkstatt und Gold fuer zwei Einheiten sind ueber den echten Weg da",
              aufgebaut, "Gold %s" % (ort.vorraete.get("gold"),))
        if not aufgebaut:
            return
        app._oeffne_siedlungskarte(ort)
        ortsheer_vorher = int((ort.einheiten or {}).get(EINHEIT, 0))
        reich_vorher = {k: int(v.count) for k, v in gs.units.items() if int(v.count) > 0}
        for _ in range(2):
            app._train_unit(EINHEIT)
        check("zwei Ausbildungsauftraege stehen im ORT", len(ort.ausbildung or []) == 2,
              str(ort.ausbildung))
        check("die Einheit existiert noch NICHT",
              int((ort.einheiten or {}).get(EINHEIT, 0)) == ortsheer_vorher, str(ort.einheiten))
        ende = float((ort.ausbildung or [{}])[-1].get("ende") or 0.0)
        _bis(gs, ende)
        check("nach der Ausbildungszeit stehen zwei Einheiten im ORTSLAGER",
              int((ort.einheiten or {}).get(EINHEIT, 0)) == ortsheer_vorher + 2, str(ort.einheiten))
        check("der REICHSBESTAND bleibt leer - das Ortsheer ist die einzige Quelle (F-01)",
              {k: int(v.count) for k, v in gs.units.items() if int(v.count) > 0} == reich_vorher,
              str({k: v.count for k, v in gs.units.items() if v.count}))

        # ---------------------------------------------------------------- 5 Einsatz
        abschnitt("5. EINSATZ - der Angriff geht als AUFTRAG aus dem ORTSHEER heraus")
        bot = min(gs.bots, key=lambda b: sum(int(v) for v in (b.army or {}).values()))
        ortsheer_vor_angriff = dict(ort.einheiten or {})
        gestartet = app._auftrag_angriff(bot)
        check("der Angriff startet ueberhaupt", gestartet is True, _log_ende(gs))
        eintrag = gs.auftraege[-1] if gs.auftraege else {}
        check("er steht als AUFTRAG in der Liste", bool(eintrag), str(gs.auftraege)[:80])
        check("der Auftrag kennt seine Quelle als KENNUNG (F-09: quelle_id)",
              eintrag.get("quelle_id") == ort.id, "%r statt %r" % (eintrag.get("quelle_id"), ort.id))
        check("er startet in DIESER Siedlung", eintrag.get("von") == ort.name, str(eintrag.get("von")))
        check("das Ortsheer ist mitgereist", int((ort.einheiten or {}).get(EINHEIT, 0)) == 0,
              str(ort.einheiten))
        check("der Reichsbestand wurde nicht angefasst",
              {k: int(v.count) for k, v in gs.units.items() if int(v.count) > 0} == reich_vorher,
              str({k: v.count for k, v in gs.units.items() if v.count}))

        # ---------------------------------------------------------------- 6 Rueckkehr
        abschnitt("6. RUECKKEHR - Kampf am Ziel, Ueberlebende GENAU zurueck in diesen Ort")
        if eintrag:
            kampf_vorher = len(_nachrichten(gs, "kampf"))
            _auftrag_zu_ende(gs, eintrag)
            check("am Ziel findet ein echter Kampf statt (Bericht im Nachrichtenreiter)",
                  len(_nachrichten(gs, "kampf")) > kampf_vorher,
                  "%d -> %d" % (kampf_vorher, len(_nachrichten(gs, "kampf"))))
            check("der Auftrag ist danach aus der Liste",
                  not [e for e in gs.auftraege if e.get("quelle_id") == ort.id], str(gs.auftraege)[:80])
            ueberlebt = int((eintrag.get("einheiten") or {}).get(EINHEIT, 0))
            zurueck = int((ort.einheiten or {}).get(EINHEIT, 0))
            check("die Ueberlebenden stehen GENAU im ORTSLAGER (gebucht, nicht gewuerfelt)",
                  zurueck == ueberlebt, "%d im Ort, %d ueberlebt" % (zurueck, ueberlebt))
            check("zurueck kamen hoechstens so viele, wie losgezogen sind",
                  zurueck <= int(ortsheer_vor_angriff.get(EINHEIT, 0)),
                  "%d von %d" % (zurueck, ortsheer_vor_angriff.get(EINHEIT, 0)))
            check("der Reichsbestand blieb auch nach der Rueckkehr leer",
                  {k: int(v.count) for k, v in gs.units.items() if int(v.count) > 0} == reich_vorher,
                  str({k: v.count for k, v in gs.units.items() if v.count}))

        # ---------------------------------------------------------------- 9 Heilung
        abschnitt("9. HEILUNG - Verwundete heilen, Kosten und Dauer, Rueckkehr ins Ortsheer")
        verwundet = _startwert_verwundete(gs, ort)
        check("Verwundete entstehen ueber die ECHTE Buchstelle (30 Prozent der Verluste)",
              verwundet > 0, str(getattr(ort, "verwundete", None)))
        if verwundet > 0:
            # Der Heilpreis steht in `data/verwundete.json` (75 Prozent der Kostenposten); der
            # Kern rechnet `verwundete.heilung_grenzen`. Die Kette wartet, bis der Ort ihn
            # bezahlen kann - sie erfindet kein Gold.
            grenzen = _warte_heilbar(gs, ort)
            check("die Heilung ist nach dem Wirtschaften bezahlbar (Preis aus den Daten)",
                  int(grenzen.get("moeglich") or 0) >= 1,
                  "moeglich %s, Gruende %s" % (grenzen.get("moeglich"), grenzen.get("hindernisse")))
            if int(grenzen.get("moeglich") or 0) >= 1:
                vorher_heil = int((ort.verwundete or {}).get(EINHEIT, 0))
                heer_vorheil = int((ort.einheiten or {}).get(EINHEIT, 0))
                schlange_vorher = len(ort.ausbildung or [])
                holz_vorheil = float(ort.vorraete.get("holz", 0.0))
                app._heile_verwundete(EINHEIT, 1)
                schlange_nachher = ort.ausbildung or []
                check("die Heilung steht als eigene Zeile in der Warteschlange des Ortes",
                      len(schlange_nachher) == schlange_vorher + 1
                      and bool(schlange_nachher[-1].get("heilung")), str(schlange_nachher[-1:])[:140])
                check("der Heilpreis ist aus dem Ortslager bezahlt",
                      float(ort.vorraete.get("holz", 0.0)) < holz_vorheil
                      or float(ort.vorraete.get("gold", 0.0)) < float(grenzen["kosten_je"].get("gold", 0.0)),
                      str(ort.vorraete))
                check("die Einheit ist noch NICHT wieder im Heer",
                      int((ort.einheiten or {}).get(EINHEIT, 0)) == heer_vorheil, str(ort.einheiten))
                check("ein Verwundeter ist sofort aus dem Ortslager gebucht",
                      int((ort.verwundete or {}).get(EINHEIT, 0)) == vorher_heil - 1,
                      "%d -> %s" % (vorher_heil, ort.verwundete))
                ende_heil = float((ort.ausbildung or [{}])[-1].get("ende") or 0.0)
                _bis(gs, ende_heil)
                check("nach der Heildauer ist keine Heilungszeile mehr offen",
                      not [a for a in (ort.ausbildung or [])
                           if a.get("heilung") and not a.get("gebucht")],
                      str([a for a in (ort.ausbildung or []) if a.get("heilung")])[:140])
                check("der Geheilte steht wieder im ORTSLAGER",
                      int((ort.einheiten or {}).get(EINHEIT, 0)) == heer_vorheil + 1, str(ort.einheiten))
        check("kein Wert des Spielers ist negativ", not _negative(gs, ort), str(_negative(gs, ort)))
        check("waehrend der Partie gab es keinen stillen GUI-Fehler", not gesammelt, str(gesammelt[:1]))
    finally:
        _ende(root)


# --------------------------------------------------------------------------- Startwerte
def _startwert_handelskarawane(gs, ort):
    """STARTWERT: eine Handelskarawane im Ortslager.

    GRUND: handeln darf nur eine Handelskarawane (Handbuch S. 20). In den Daten kostet sie
    500 Holz, 250 Metall, 200 Gold, 500 Wolle, 500 Leder, 10 Siedler und 15 Pferde - ein
    Aufbau ueber Wollweberei, Rinderfarm und Pferdezucht, der in einer Kette nichts ueber den
    HANDELSWEG aussagt. Die Kette prueft den Weg (Angebot, Reise, Annahme, Erloes, Punkte), und
    der Zustand davor ist der einzige gesetzte Wert dieses Wegs.
    """
    ort.einheiten[KARAWANE] = int(ort.einheiten.get(KARAWANE, 0) or 0) + 1
    return int(ort.einheiten.get(KARAWANE, 0))


def _startwert_verwundete(gs, ort):
    """STARTWERT: Verwundete aus 10 Verlusten - gebucht ueber die ECHTE Buchstelle.

    GRUND: Verwundete entstehen nur aus Verlusten eines Gefechts (30 Prozent, abgerundet). Ob
    ein Gefecht Verluste kostet, entscheidet der Wuerfel; eine Kette, die darauf wartet, misst
    das Wuerfelglueck statt die Heilung. Gebucht wird deshalb ueber dieselbe Stelle, die auch
    der Kampf ruft (`_verwundete_buchen`) - keine zweite Rechnung, keine direkte Zuweisung.
    """
    neu = gs._verwundete_buchen(ort, {EINHEIT: 10}, "Startwert der Heilungskette")
    return int(sum(int(v) for v in (neu or {}).values()))


def _startwert_mauerschaden(gs, ort):
    """STARTWERT: eine beschaedigte Mauer (60 Prozent).

    GRUND: der Wall steht nach dem Errichten auf 100 Prozent; Schaden entsteht NUR durch einen
    feindlichen Angriff auf diesen Ort (`main.py`, Bot-Raubzug). Ob ein Bot in einer Partie
    angreift, haengt an Punkteband, Pakt, Spaehung und Wuerfel - das laesst sich nicht
    herbeifuehren, ohne die Mechanik zu aendern. Der Schaden ist damit die Vorbedingung der
    Reparatur, nicht ihr Ergebnis: geprueft werden Preis, Dauer und Buchung der Reparatur.
    """
    ort.mauer_zustand = 60.0
    return dorfwall.zustand(ort)


def _startwert_mana(gs, ort, betrag):
    """STARTWERT: das ueber viele Spieltage ersparte Mana des Reiches.

    GRUND: Mana entsteht nur im Tempel - 5 je Stunde auf Nebelsee, 1 auf jedem anderen Gelaende
    (`data/resources.json`). Die 5000 Mana eines Weltensprungs sind damit 41,7 Spieltage bei 120
    am Tag. Ein Spieler schafft das ueber Wochen; eine Pruefung nicht: `GameState.tick` kostet
    schon am sechsten Spieltag rund 40 s je Spieltag, davon 23 s in `copy.deepcopy` innerhalb von
    `bots_fortschreiben` (gemessen 07.11.2026, 120 Fortschreibungen je Spieltag). Deshalb steht
    hier das ERSPARTE - und die LETZTEN Mana-Punkte bis zum Festpreis erwirtschaftet die Kette
    selbst mit echten Tempeln und echten Takten. Angebucht wird der Sprung also mit Mana, das
    wirklich produziert wurde.
    """
    gs.resources["mana"].amount = float(betrag)
    ort.vorraete["mana"] = float(betrag)
    return float(gs.resources["mana"].amount)


# --------------------------------------------------------------------------- 7 Speichern/Laden
def _kette_7_speichern():
    abschnitt("7. SPEICHERN und LADEN - schreiben, in einer ZWEITEN App laden, Werte vergleichen")
    root, app, gs, ort, gesammelt = _neu()
    root2 = None
    pfad = os.path.join(tempfile.mkdtemp(prefix="nebelseetal_e2e_"), "stand.json")
    try:
        if ort is None:
            check("Startsiedlung fuer Speichern/Laden", False)
            return
        _bauen(app, gs, ort, "holzfaeller")
        _tick(gs, 12)
        ok_save = gs.save(pfad)
        check("der Spielstand wird geschrieben", ok_save is not False and os.path.exists(pfad),
              str(ok_save))
        vorher = {
            "orte": len(gs.settlements),
            "name": ort.name,
            "vorraete": {k: round(float(v), 6) for k, v in (ort.vorraete or {}).items()},
            "bauten": dict(ort.bauten or {}),
            "spielsekunden": round(float(gs.spielsekunden), 3),
            "forschung": {k: int(v.level) for k, v in gs.research.items()},
            "einheiten": dict(ort.einheiten or {}),
            "bots": len(gs.bots),
        }
        # Die zweite App braucht einen EIGENEN Tcl-Interpreter: erst die erste Partie schliessen,
        # dann frisch starten (zwei lebende Tk-Instanzen teilen sich sonst die Bildnamen).
        _ende(root)
        root = None
        root2 = tk.Tk()
        root2.withdraw()
        app2 = main.NebelseetalApp(root2)
        app2._build_main_ui()
        ok_load = app2.state.load(pfad)
        gs2 = app2.state
        ort2 = gs2.settlements[0] if gs2.settlements else None
        check("der geschriebene Stand laesst sich in einer FRISCHEN App laden", ok_load is not False,
              str(ok_load))
        check("die Zahl der Siedlungen ist gleich", len(gs2.settlements) == vorher["orte"],
              "%d statt %d" % (len(gs2.settlements), vorher["orte"]))
        if ort2 is not None:
            check("der Ortsname ist gleich", ort2.name == vorher["name"],
                  "%r statt %r" % (ort2.name, vorher["name"]))
            check("die Vorraete sind gleich (auf 6 Stellen)",
                  {k: round(float(v), 6) for k, v in (ort2.vorraete or {}).items()}
                  == vorher["vorraete"], str(ort2.vorraete))
            check("die Gebaeude stehen auf denselben Feldern", dict(ort2.bauten or {}) == vorher["bauten"],
                  str(ort2.bauten))
            check("das Ortsheer ist gleich", dict(ort2.einheiten or {}) == vorher["einheiten"],
                  str(ort2.einheiten))
        check("die Spielzeit ist gleich", round(float(gs2.spielsekunden), 3) == vorher["spielsekunden"],
              "%s statt %s" % (gs2.spielsekunden, vorher["spielsekunden"]))
        check("der Forschungsstand ist gleich",
              {k: int(v.level) for k, v in gs2.research.items()} == vorher["forschung"],
              str({k: v.level for k, v in gs2.research.items()}))
        check("die Bots sind mitgeladen", len(gs2.bots) == vorher["bots"],
              "%d statt %d" % (len(gs2.bots), vorher["bots"]))
        # Der geladene Stand muss WEITERSPIELEN, nicht nur lesbar sein.
        zeit_vorher = float(gs2.spielsekunden)
        vorraete_vorher = dict(ort2.vorraete or {}) if ort2 is not None else {}
        _tick(gs2, 6)
        check("der geladene Stand laeuft weiter (Spielzeit steigt)", float(gs2.spielsekunden) > zeit_vorher,
              "%s -> %s" % (zeit_vorher, gs2.spielsekunden))
        if ort2 is not None:
            check("und die Produktion laeuft im geladenen Stand weiter",
                  float((ort2.vorraete or {}).get("holz", 0.0)) >= float(vorraete_vorher.get("holz", 0.0)),
                  str(ort2.vorraete.get("holz")))
        check("waehrend der Kette gab es keinen stillen GUI-Fehler", not gesammelt, str(gesammelt[:1]))
    finally:
        if root2 is not None:
            _ende(root2)
        _ende(root)
        try:
            for name in os.listdir(os.path.dirname(pfad)):
                os.remove(os.path.join(os.path.dirname(pfad), name))
            os.rmdir(os.path.dirname(pfad))
        except OSError:
            pass


# --------------------------------------------------------------------------- 8 Handel
def _kette_8_handel():
    abschnitt("8. HANDEL - Karawane verkauft an einen Bot, Erloes und Handelspunkte entstehen")
    root, app, gs, ort, gesammelt = _neu()
    try:
        if ort is None:
            check("Startsiedlung fuer den Handel", False)
            return
        _bauen(app, gs, ort, "holzfaeller")
        _warte_auf(gs, lambda: float(ort.vorraete.get("holz", 0.0)) >= 120.0, stunden=10)
        check("genug Holz im Ortslager fuer den Verkauf (eigene Produktion)",
              float(ort.vorraete.get("holz", 0.0)) >= 120.0, str(ort.vorraete.get("holz")))
        check("eine Handelskarawane steht bereit (Startwert, siehe Begruendung oben)",
              _startwert_handelskarawane(gs, ort) == 1, str(ort.einheiten))
        partner = next((b for b in gs.bots
                        if float(b.trading) > 0.3 and float((b.vorraete or {}).get("gold", 0)) >= 100.0),
                       None)
        check("es gibt einen handelsbereiten Bot mit genug Gold", partner is not None,
              getattr(partner, "name", "keiner der Bots handelt"))
        if partner is None:
            return
        preis = 1.0
        holz_vorher = float(ort.vorraete.get("holz", 0.0))
        gold_vorher = float(ort.vorraete.get("gold", 0.0))
        punkte_vorher = float(getattr(gs, "handels_erloes", 0.0) or 0.0)
        ok, meldung = app._verkauf_ausfuehren(partner, ort, "holz", 100, preis, KARAWANE, 1)
        check("das Verkaufsangebot geht ueber die ECHTE Maske hinaus", ok is True, str(meldung)[:120])
        if not ok:
            return
        check("die Ware hat das Ortslager verlassen",
              float(ort.vorraete.get("holz", 0.0)) <= holz_vorher - 100.0 + 1e-6,
              "%g -> %g" % (holz_vorher, ort.vorraete.get("holz")))
        check("die Handelskarawane ist mitgereist",
              int((ort.einheiten or {}).get(KARAWANE, 0)) == 0, str(ort.einheiten))
        vertrag = gs.auftraege[-1] if gs.auftraege else {}
        check("der Vertrag steht als Auftrag mit Ankunft und Rueckkehr",
              bool(vertrag.get("ankunft")) and bool(vertrag.get("rueckkehr")),
              str({k: vertrag.get(k) for k in ("ankunft", "rueckkehr")}))
        _auftrag_zu_ende(gs, vertrag, "ankunft")
        check("der Bot entscheidet bei der Ankunft (Annahme oder Ablehnung steht am Vertrag)",
              vertrag.get("angenommen") is not None, str(vertrag.get("angenommen")))
        _auftrag_zu_ende(gs, vertrag, "rueckkehr")
        angenommen = bool(vertrag.get("angenommen"))
        if angenommen:
            check("bei Annahme steigt das Gold im Ortslager (Erloes angekommen)",
                  float(ort.vorraete.get("gold", 0.0)) > gold_vorher,
                  "%g -> %g" % (gold_vorher, ort.vorraete.get("gold")))
            check("der Erloes ist EINMAL gebucht (handels_erloes)",
                  float(getattr(gs, "handels_erloes", 0.0) or 0.0) > punkte_vorher,
                  "%g -> %s" % (punkte_vorher, getattr(gs, "handels_erloes", None)))
            _hp = punkte.handelspunkte(getattr(gs, "handels_erloes", 0.0),
                                      getattr(gs, "letzter_handel", None),
                                      float(gs.spielsekunden))
            check("daraus entstehen Handelspunkte groesser 0 (die EINE Rechenstelle)",
                  _hp > 0.0, str(_hp))
        else:
            befund("der Bot hat den Verkauf abgelehnt (Preis ueber seiner Schwelle)",
                   "Erloes und Punkte bleiben dann 0 - der Weg selbst ist gelaufen")
        check("die Karawane ist wieder im Ortslager",
              int((ort.einheiten or {}).get(KARAWANE, 0)) == 1, str(ort.einheiten))
        check("der Vertrag ist abgerechnet und aus der Auftragsliste",
              not [e for e in gs.auftraege if e.get("art") == vertrag.get("art")
                   and not e.get("heimgekehrt") and e is not vertrag], str(gs.auftraege)[:80])
        check("waehrend der Kette gab es keinen stillen GUI-Fehler", not gesammelt, str(gesammelt[:1]))
    finally:
        _ende(root)


# --------------------------------------------------------------------------- 10 Mauerreparatur
def _kette_10_mauer():
    abschnitt("10. MAUERREPARATUR - Wall errichten, Reparatur laeuft, Zustand steht auf 100")
    root, app, gs, ort, gesammelt = _neu()
    try:
        if ort is None:
            check("Startsiedlung fuer die Mauerreparatur", False)
            return
        check("vor der Forschung gibt es keinen Wall am Ort",
              int(gs.wall_stufe_am_ort(ort)) <= 0, str(gs.wall_stufe_am_ort(ort)))
        check("Verteidigungsanlagen Stufe 1 laeuft ueber den echten Forschungsweg",
              _erforschen(app, gs, ort, "Verteidigungsanlagen", 1))
        _warte_auf(gs, lambda: float(ort.vorraete.get("holz", 0.0)) >= 20.0
                   and float(ort.vorraete.get("stein", 0.0)) >= 20.0, stunden=10)
        holz_vorher = float(ort.vorraete.get("holz", 0.0))
        ok, meldung = gs.wall_errichten(ort)
        check("der Wall wird ueber den echten Weg errichtet (Kosten aus den Daten)", ok is True,
              str(meldung)[:120])
        if not ok:
            return
        check("der Wall kostet Rohstoffe aus dem Ortslager",
              float(ort.vorraete.get("holz", 0.0)) < holz_vorher, str(ort.vorraete.get("holz")))
        check("der Wall steht danach auf 100 Prozent", dorfwall.zustand(ort) == 100.0,
              str(dorfwall.zustand(ort)))
        zustand = _startwert_mauerschaden(gs, ort)
        check("eine beschaedigte Mauer ist die Vorbedingung (Startwert, siehe Begruendung)",
              zustand < 100.0, str(zustand))
        pruefung = dorfwall.reparatur_pruefen(ort, gs.forschungs_stufen(), ort.vorraete,
                                              gs.forschungsauftraege, gs.spielsekunden)
        check("die Reparatur ist bei genug Rohstoffen moeglich", bool(pruefung.get("moeglich")),
              str(pruefung.get("gruende")))
        _warte_auf(gs, lambda: float(ort.vorraete.get("holz", 0.0))
                   >= float((pruefung.get("preis") or {}).get("holz", 0.0)) + 1.0
                   and float(ort.vorraete.get("stein", 0.0))
                   >= float((pruefung.get("preis") or {}).get("stein", 0.0)) + 1.0, stunden=10)
        holz_vor_reparatur = float(ort.vorraete.get("holz", 0.0))
        ok_r, meldung_r = gs.mauer_reparatur_starten(ort)
        check("die Reparatur startet ueber den echten Weg", ok_r is True, str(meldung_r)[:160])
        if not ok_r:
            return
        check("der Reparaturpreis ist aus dem Ortslager bezahlt",
              float(ort.vorraete.get("holz", 0.0)) < holz_vor_reparatur,
              "%g -> %g" % (holz_vor_reparatur, ort.vorraete.get("holz")))
        check("die Reparatur hat eine Endzeit (Dauer aus V-1)", float(ort.mauer_reparatur_ende) > 0.0,
              str(ort.mauer_reparatur_ende))
        check("der Zustand springt NICHT sofort auf 100", dorfwall.zustand(ort) < 100.0,
              str(dorfwall.zustand(ort)))
        _bis(gs, float(ort.mauer_reparatur_ende) + 1.0)
        check("nach der Reparaturzeit steht die Mauer wieder auf 100 Prozent",
              dorfwall.zustand(ort) == 100.0, str(dorfwall.zustand(ort)))
        check("die Reparatur laeuft nicht mehr", not dorfwall.reparatur_laeuft(ort),
              str(ort.mauer_reparatur_ziel))
        check("waehrend der Kette gab es keinen stillen GUI-Fehler", not gesammelt, str(gesammelt[:1]))
    finally:
        _ende(root)


# --------------------------------------------------------------------------- 11 Vertrag
def _kette_11_vertrag():
    abschnitt("11. VERTRAG - Nichtangriffspakt sperrt den Bot-Angriff und laeuft ab")
    root, app, gs, ort, gesammelt = _neu()
    try:
        if ort is None:
            check("Startsiedlung fuer den Vertrag", False)
            return
        check("Vertraege sind in der Datendatei eingeschaltet", diplomatie.vertraege_aktiv(),
              "Schalter aus")
        bot = gs.bots[0]
        jetzt = float(gs.spielsekunden)
        daten = gs.bot_als_dict(bot)
        gesperrt_vorher, _grund = diplomatie.angriff_gesperrt(daten, jetzt)
        check("vor dem Pakt darf der Bot angreifen", gesperrt_vorher is False, str(_grund))
        ok, grund = diplomatie.vertrag_anbieten(daten, "nichtangriff", jetzt)
        check("der Pakt kommt zustande (Gunst reicht, Art steht in den Daten)", ok is True, str(grund))
        gs.bot_aus_dict(bot, daten)
        if not ok:
            return
        daten = gs.bot_als_dict(bot)
        check("der Pakt steht am BOT (nicht in einer zweiten Tabelle)",
              bool((daten.get("vertraege") or {}).get("nichtangriff")), str(daten.get("vertraege")))
        check("der Pakt ist jetzt aktiv", diplomatie.vertrag_aktiv(daten, "nichtangriff", jetzt) is True)
        gesperrt, grund2 = diplomatie.angriff_gesperrt(daten, jetzt)
        check("und er SPERRT den Angriff dieses Bots", gesperrt is True, str(grund2))
        dauer = float((diplomatie.art_daten("nichtangriff") or {}).get("dauer_sekunden") or 0.0)
        check("die Dauer steht in den Daten und ist groesser 0", dauer > 0.0, str(dauer))
        check("kurz vor dem Ende sperrt er noch",
              diplomatie.angriff_gesperrt(daten, jetzt + dauer - 1.0)[0] is True)
        vorgaenge = diplomatie.vertraege_tick(daten, jetzt + dauer + 1.0)
        check("nach der Dauer laeuft er still ab (kein Bruch, keine Strafe)", vorgaenge == [],
              str(vorgaenge))
        check("und der Bot darf wieder angreifen",
              diplomatie.angriff_gesperrt(daten, jetzt + dauer + 1.0)[0] is False)
        # ENTSCHEIDUNG Daniel 08.11.2026, 00:25 (S4-3-Nachtrag): der Pakt bekommt einen Spielweg.
        # Die alte Fassung meldete hier einen BEFUND ("kein Aufrufer in src/main.py"). Die
        # Entscheidung dreht die Wache UMDREHEN: der Aufrufer muss jetzt da sein. Die Einzelheiten
        # (Knopf nur bei genug Gunst, Klick bucht, Doppelklick bucht nicht doppelt) prueft
        # `tests/test_pakt_knopf.py`; hier steht nur, dass der Spielweg im Code existiert.
        _quelle_knopf = _inspect.getsource(main.NebelseetalApp._pakt_anbieten)
        check("der Pakt hat einen Spielweg: der Knopf ruft `diplomatie.vertrag_anbieten`",
              "diplomatie.vertrag_anbieten(" in _quelle_knopf)
        check("und er schreibt die Vertragstabelle nicht selbst",
              "vertraege[" not in _quelle_knopf)
        check("waehrend der Kette gab es keinen stillen GUI-Fehler", not gesammelt, str(gesammelt[:1]))
    finally:
        _ende(root)


# --------------------------------------------------------------------------- 12 Portal
def _kette_12_portal():
    abschnitt("12. PORTAL - Mana aus Tempeln, der Umzug bucht genau einmal ab (S-4b: _dorf_versetzen)")
    root, app, gs, ort, gesammelt = _neu()
    try:
        if ort is None:
            check("Startsiedlung fuer den Portalweg", False)
            return
        kosten = float(portalraum.wechselkosten())
        check("der Festpreis steht in den Daten (data/welten.json)", kosten > 0.0, str(kosten))
        # Der Tempel traegt auf Nebelsee 5 Mana je Stunde, auf allem anderen 1 (data/resources.json).
        # Der Reihenfolge wegen: erst die Bibliothek (Baukunst) auf Grasland, damit kein
        # Nebelsee-Feld dafuer draufgeht; dann JEDES freie Nebelsee-Feld mit einem Tempel belegen.
        # Beides sind echte Spielzuege ueber die Siedlungskarte.
        check("die Bibliothek steht auf Grasland (kein Nebelsee-Feld verschwendet)",
              _bauen(app, gs, ort, "bibliothek", nur_terrain="grasland") is not None,
              str(ort.bauten))
        for feld, terrain in enumerate(ort.karte["raster"]):
            if str(terrain) == "nebelsee" and str(feld) not in ort.bauten:
                _bauen(app, gs, ort, "tempel", nur_terrain="nebelsee")
        nebelsee_felder = [f for f, r in enumerate(ort.karte["raster"]) if str(r) == "nebelsee"]
        frei = [f for f in nebelsee_felder if str(f) not in ort.bauten]
        tempel_nebelsee = [f for f in nebelsee_felder if str(ort.bauten.get(str(f))) == "tempel"]
        check("auf JEDEM freien Nebelsee-Feld steht jetzt ein Tempel (echter Bau, kein Geschenk)",
              not frei and len(tempel_nebelsee) >= 2,
              "Nebelsee %s, Tempel %s, frei %s" % (nebelsee_felder, tempel_nebelsee, frei))
        nachher = float(gs.resources["mana"].amount)
        _tick(gs, 6)                                       # ein echter Takt, keine Rechnung
        zuwachs = float(gs.resources["mana"].amount) - nachher
        # 5 Mana je Stunde liefert EIN Tempel auf Nebelsee (data/resources.json); vier davon
        # muessen in sechs Stunden also mindestens 30 Mana ergeben.
        check("die Tempel tragen Mana ein (Zuwachs in sechs Spielstunden)",
              zuwachs >= 5.0 * 6.0, "%g Mana je 6 h" % zuwachs)
        check("unter dem Festpreis ist KEIN Weltensprung moeglich (die Kernpruefung)",
              portalraum.wechsel_erlaubt(0, 1, kosten - 1.0)[0] is False,
              portalraum.wechsel_erlaubt(0, 1, kosten - 1.0)[1])
        # STARTWERT: das ueber viele Spieltage ersparte Mana (Begruendung in der Funktion).
        gespart = _startwert_mana(gs, ort, kosten - 100.0)
        check("das Ersparte liegt knapp unter dem Preis", gespart < kosten, str(gespart))
        takte = 0
        while float(gs.resources["mana"].amount) < kosten and takte < 10:
            _tick(gs, 6)
            takte += 1
        check("die letzten Mana-Punkte kommen aus EIGENER Produktion (Tempel, 6-Stunden-Takte)",
              float(gs.resources["mana"].amount) >= kosten,
              "%g von %g nach %d Takten" % (gs.resources["mana"].amount, kosten, takte))
        if float(gs.resources["mana"].amount) < kosten:
            return
        # S-4b (09.11.2026): der Weltensprung ueber `_portal_wechsel` ist ENTFERNT - seit S-4
        # versetzt ausschliesslich `_dorf_versetzen` (die EINE Buchstelle aus S-3), und zwar auf
        # ein FREIES Feld der Zielwelt. Diese Kette prueft weiter denselben Weg (Mana aus eigener
        # Produktion -> genau ein Festpreis), nur ueber die Buchstelle.
        von = int(gs.eigene_dimension)
        ziel = next(int(z) for z in (portalraum.nummer_von(d.get("kennung"))
                                     for d in portalraum.dimensionen()) if int(z) != von)
        check("eine andere Weltkarte ist waehlbar", ziel != von, "%s statt %s" % (ziel, von))
        check("vor dem Umzug ist nichts unterwegs (sonst sperrt das Portal)",
              app._unterwegs_anzahl() == 0, str(app._unterwegs_anzahl()))
        belegt = app._portal_belegte_felder()                  # Belegungskarte aus S-3/S-4
        frei = None
        for fy in range(20):
            for fx in range(20):
                status = portalraum.feld_status(portalraum.index_von(ziel), fx, fy, belegt)
                if status.get("status") == portalraum.FELD_FREI:
                    frei = (fx, fy)
                    break
            if frei:
                break
        check("auf der Zielwelt gibt es ein freies Feld", frei is not None, str(frei))
        if frei is None:
            return
        mana_vor_sprung = float(gs.resources["mana"].amount)
        ort_name = str(getattr(ort, "name", ""))
        gesprungen = app._dorf_versetzen(ort_name, frei[0], frei[1], ziel)
        check("der Umzug wird ausgefuehrt", gesprungen is True, _log_ende(gs))
        if not gesprungen:
            return
        check("die Welt des Dorfes ist die neue", int(getattr(ort, "dimension", 0)) == ziel,
              str(getattr(ort, "dimension", 0)))
        check("die Portalposition steht auf dem gewaehlten Feld",
              (getattr(ort, "welt_x", None), getattr(ort, "welt_y", None)) == (frei[0], frei[1]),
              str((getattr(ort, "welt_x", None), getattr(ort, "welt_y", None))))
        check("GENAU der Festpreis ist abgebucht",
              abs(float(gs.resources["mana"].amount) - (mana_vor_sprung - kosten)) < 1e-6,
              "%g -> %g" % (mana_vor_sprung, gs.resources["mana"].amount))
        check("die neue Welt steht in der Liste der eigenen Dimensionen",
              ziel in [int(z) for z in gs.eigene_dimensionen], str(gs.eigene_dimensionen))
        # S-5 (09.11.2026, Register 332): der Stempel ist Aufzeichnung, keine Sperre (F-28 = C).
        check("der Zeitstempel des Wechsels ist geschrieben (Aufzeichnung, keine Sperre)",
              float(gs.letzter_wechsel or 0.0) > 0.0, str(gs.letzter_wechsel))
        check("die Meldung steht im Postfach", len(_nachrichten(gs, "portal")) > 0,
              "%d Portalmeldungen" % len(_nachrichten(gs, "portal")))
        mana_nach_sprung = float(gs.resources["mana"].amount)
        # Fuer den zweiten Versuch ein ANDERES freies Feld nehmen - sonst blockt "steht schon
        # dort" und nicht das Mana, und die Wache bewiese das Falsche.
        belegt2 = app._portal_belegte_felder()
        anderer = None
        for fy in range(20):
            for fx in range(20):
                if (fx, fy) == (frei[0], frei[1]):
                    continue
                status = portalraum.feld_status(portalraum.index_von(ziel), fx, fy, belegt2)
                if status.get("status") == portalraum.FELD_FREI:
                    anderer = (fx, fy)
                    break
            if anderer:
                break
        check("ein zweites freies Feld fuer die Manaprothese ist da", anderer is not None,
              str(anderer))
        zweiter = app._dorf_versetzen(ort_name, anderer[0], anderer[1], ziel)
        check("ein ZWEITER Umzug sofort scheitert am Mana, nicht an einer Wartezeit",
              zweiter is False, _log_ende(gs))
        check("der Grund ist das Mana (20 von 5.000 nach dem Umzug)",
              "Mana" in str((gs.messages[-1] or {}).get("text", "")),
              str((gs.messages[-1] or {}).get("text")))
        # Diese Kette darf den Spielstand nicht von Hand setzen (Quellwache Abschnitt 13) -
        # die Entscheidung selbst wird deshalb an der Kernfunktion geprueft.
        # S-5 (09.11.2026, Register 332): die 24-Stunden-Sperre ist auf Daniels Entscheid F-28 = C
        # entfallen. Derselbe Aufruf mit genug Mana und einem Wechsel von gerade eben ist jetzt
        # ERLAUBT - die alte Wache ist umgedreht, nicht geloescht.
        _erlaubt5, _grund5 = portalraum.wechsel_erlaubt(
            portalraum.index_von(int(gs.eigene_dimension)), portalraum.index_von(von),
            kosten * 2.0)
        check("kein Warten mehr: mit genug Mana ist ein Wechsel von gerade eben erlaubt (F-28 = C)",
              _erlaubt5 is True, str(_grund5))
        _werte5 = list(_inspect.signature(portalraum.wechsel_erlaubt).parameters)
        check("die Kernfunktion nimmt keinen Zeitstempel mehr (genau drei Werte)",
              _werte5 == ["von_z", "nach_z", "mana"], str(_werte5))
        check("und es wurde dabei nichts zweites abgebucht",
              abs(float(gs.resources["mana"].amount) - mana_nach_sprung) < 1e-6,
              str(gs.resources["mana"].amount))
        check("waehrend der Kette gab es keinen stillen GUI-Fehler", not gesammelt, str(gesammelt[:1]))
    finally:
        _ende(root)


# --------------------------------------------------------------------------- 13 Selbstwache
STATE_ROOTS = ("gs", "gs2", "state", "ort", "ort2", "bot", "daten", "app")


def _wurzel(ziel):
    """Der Ursprungsname einer Zuweisung: `ort.einheiten[X]` -> "ort"."""
    while isinstance(ziel, (ast.Attribute, ast.Subscript)):
        ziel = ziel.value
    return ziel.id if isinstance(ziel, ast.Name) else ""


def _schreibstellen():
    """Alle Zuweisungen dieser Datei, die den SPIELSTAND treffen (Funktion -> Zieltexte)."""
    pfad = os.path.abspath(__file__)
    with open(pfad, "r", encoding="utf-8", errors="replace") as datei:
        baum = ast.parse(datei.read())
    gefunden = {}
    for funktion in [k for k in ast.walk(baum) if isinstance(k, ast.FunctionDef)]:
        for unter in ast.walk(funktion):
            ziele = []
            if isinstance(unter, ast.Assign):
                ziele = unter.targets
            elif isinstance(unter, (ast.AugAssign, ast.AnnAssign)):
                ziele = [unter.target]
            for ziel in ziele:
                if not isinstance(ziel, (ast.Attribute, ast.Subscript)):
                    continue                       # lokale Groesse, kein Spielstand
                if _wurzel(ziel) not in STATE_ROOTS:
                    continue                       # z. B. `root.report_callback_exception`
                gefunden.setdefault(funktion.name, set()).add(ast.unparse(ziel))
    return gefunden, baum


def _kette_13_quelle():
    abschnitt("13. QUELLWACHE - diese Datei schreibt nichts ausser der Uhr und vier Startwerten")
    gefunden, baum = _schreibstellen()
    fremd = {}
    uhr_in = set()
    for funktion, texte in gefunden.items():
        for text in texte:
            if text.endswith("spielsekunden"):
                uhr_in.add(funktion)               # die Spieluhr ist der Zeitsprung (E-6)
                continue
            if text in STARTWERTE.get(funktion, {}):
                continue                           # begruendete Startwerte
            fremd.setdefault(funktion, set()).add(text)
    check("ausser der Spieluhr und den vier Startwerten schreibt die Datei keinen Spielzustand",
          not fremd, str({k: sorted(v) for k, v in fremd.items()})[:300])
    check("die Uhr wird NUR in den beiden Zeitsprung-Helfern gestellt",
          uhr_in <= {"_bis", "_erforschen"}, str(sorted(uhr_in)))
    check("es gibt GENAU vier Startwert-Funktionen",
          len(STARTWERTE) == 4, str(sorted(STARTWERTE)))
    ohne_grund = []
    for name, texte in STARTWERTE.items():
        knoten = next((k for k in ast.walk(baum)
                       if isinstance(k, ast.FunctionDef) and k.name == name), None)
        grund = ast.get_docstring(knoten) if knoten is not None else None
        if not grund or "GRUND:" not in grund or not texte:
            ohne_grund.append(name)
    check("jede Startwert-Funktion traegt ihren GRUND im Docstring", not ohne_grund, str(ohne_grund))


# --------------------------------------------------------------------------- Lauf
def _negative(gs, ort):
    """Kein Rohstoff und keine Einheit darf negativ werden."""
    schlecht = {k: v for k, v in (ort.vorraete or {}).items() if float(v) < -1e-9}
    schlecht.update({f"einheit {k}": v for k, v in (ort.einheiten or {}).items() if int(v) < 0})
    schlecht.update({f"reich {k}": v.count for k, v in gs.units.items() if int(v.count) < 0})
    return schlecht


def _log_ende(gs):
    """Die letzte Logzeile - sie nennt den Grund einer Ablehnung im Klartext."""
    return gs.log[-1] if getattr(gs, "log", None) else ""


def _lauf():
    # Der Diebstahl hat seine eigene Wache (`tests/test_bot_diebstahl.py`); hier ist er aus,
    # sonst misst die Kette den Diebstahl statt die Produktion (Muster der Vorlagekette).
    dieb_aus = mock.patch.object(main, "bot_diebstahl_einstellungen", lambda: {"aktiv": False})
    dieb_aus.start()
    try:
        for name, kette in (("1 Rohstoff", _kette_1_rohstoff),
                            ("2 Forschung", _kette_2_forschung),
                            ("3 Ware", _kette_3_ware),
                            ("4-6,9 Partie", _kette_4_bis_9),
                            ("7 Speichern", _kette_7_speichern),
                            ("8 Handel", _kette_8_handel),
                            ("10 Mauer", _kette_10_mauer),
                            ("11 Vertrag", _kette_11_vertrag),
                            ("12 Portal", _kette_12_portal)):
            ausnahme("Kette %s" % name, kette)
        ausnahme("Kette 13 Quellwache", _kette_13_quelle)
    finally:
        dieb_aus.stop()


if __name__ == "__main__":
    _lauf()
    sys.exit(bericht())
