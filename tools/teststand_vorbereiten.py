"""Legt den VORBEREITETEN Spielstand fuer Daniels Spieltest an (08.11.2026, Sitzung 17).

Wozu: Daniel testet morgens mit einer Anleitung in zwei Teilen - Teil A frisches Spiel (fruehe
Wege), Teil B vorbereiteter Stand (spaete Wege: Wall repararieren, Handeln mit Karawane, Portal,
Pakt). Was man sonst erst nach Stunden erspielt, steht in diesem Stand bereit; der Stand ist
deshalb ausdruecklich als VORBEREITET gekennzeichnet (die Anleitung sagt es, und der Dateiname
traegt es).

Was ueber ECHTE Wege entsteht (kein gesetzter Wert):
  * die Siedlung selbst (`_erste_siedlung_gruenden`),
  * die Forschung `Verteidigungsanlagen` samt ihrer Voraussetzungen (`_start_research` + Spieluhr),
  * der Wall (`GameState.wall_errichten` - Preis und Ortsskasse aus den Datendateien).

Die DREI Startwerte, jeder mit Grund:
  * Handelskarawane: handeln darf nur eine Karawane (Handbuch S. 20); sie kostet 500 Holz,
    250 Metall, 200 Gold, 500 Wolle, 500 Leder, 10 Siedler und 15 Pferde - ein Aufbau ueber
    Wollweberei, Rinderfarm und Pferdezucht. Der Stand soll den HANDELSWEG zeigen, nicht den Aufbau.
  * Mauerzustand 60 Prozent: Schaden entsteht NUR durch einen feindlichen Angriff; dass ein Bot
    angreift, haengt an Punkteband, Pakt, Spaehung und Wuerfel. Der Schaden ist die Vorbedingung
    der Reparatur, nicht ihr Ergebnis.
  * Mana 5000: der Weltensprung kostet 5000 (Festpreis). Mana entsteht nur im Tempel (5 je Stunde
    auf Nebelsee) - das sind 41,7 Spieltage, in einer Partie am Abend nicht zu schaffen.

Aufruf:
    .venv/Scripts/python.exe -X utf8 tools/teststand_vorbereiten.py [zielpfad]

Vorgabe fuer den Zielpfad ist `~/.nebelseetal/savegame_slot2.json` (Spielerslot 2). Das Skript
schreibt NUR diesen Pfad und meldet am Ende, was im Stand steht.
"""
from __future__ import annotations

import json
import os
import random
import sys
import tkinter as tk
from dataclasses import asdict

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(WURZEL, "src"))

import einheiten          # noqa: E402
import forschungspfad     # noqa: E402
import gelaende           # noqa: E402
import gebaeude_wirkung   # noqa: E402
import main               # noqa: E402

SAAT = 20261108                                     # fester Start: derselbe Stand, jeder Lauf gleich
GEDULD = 30                                         # hoechstens so viele Runden je Bedingung
KARAWANE = next(n for n in einheiten.alle() if n.startswith("Handelskarawane"))
MANA_START = 5000.0                                 # Festpreis des Weltensprungs
MAUER_START = 60.0                                  # Vorgabe: beschaedigt, reparabel

with open(os.path.join(WURZEL, "data", "buildings.json"), "r", encoding="utf-8") as _datei:
    _GEBAEUDE_VOR = {str(g.get("id")): str(g.get("voraussetzung") or "")
                     for g in json.load(_datei).get("gebaeude") or []}


def _tick(gs, stunden):
    """Spieluhr weiterstellen - die einzige Art, wie hier etwas entsteht."""
    gs.tick(float(stunden) * 3600.0)


def _bauen_einmal(app, gs, ort, gebaeude):
    """EIN Bauversuch auf dem ersten Feld, das die Standortregel zulaesst."""
    app._oeffne_siedlungskarte(ort)
    for feld, terrain in enumerate(ort.karte["raster"]):
        if str(feld) in ort.bauten:
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


def _feld_von(ort, gebaeude):
    """Das Feld, auf dem dieses Gebaeude steht (None, wenn es fehlt)."""
    return next((int(f) for f, g in (ort.bauten or {}).items() if str(g) == gebaeude), None)


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


def _bauen(app, gs, ort, gebaeude, versuche=GEDULD):
    """Baut ein Gebaeude - die Voraussetzung kommt aus `data/buildings.json`, nicht aus einer Liste."""
    vor = (_GEBAEUDE_VOR.get(str(gebaeude)) or "").split(" ")
    vor = vor[0] if vor else ""
    if vor and vor in gs.research and int(gs.research[vor].level or 0) < 1:
        if not _erforschen(app, gs, ort, vor, 1):
            return None
    for _ in range(versuche):
        feld = _bauen_einmal(app, gs, ort, gebaeude)
        if feld is not None:
            return feld
        _tick(gs, 20)                                # Rohstoffe fuer den Bau erwirtschaften
    return None


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


def main_lauf(ziel: str) -> int:
    """Baut den Stand und schreibt ihn nach `ziel`. Rueckgabe: 0 = geschrieben."""
    root = tk.Tk()
    root.withdraw()
    fehler = []
    root.report_callback_exception = lambda *a: fehler.append(a)
    app = main.NebelseetalApp(root)
    app._build_main_ui()
    random.seed(SAAT)
    app._erste_siedlung_gruenden()
    gs, ort = app.state, (app.state.settlements[0] if app.state.settlements else None)
    if ort is None:
        print("FEHLER: keine Siedlung gegruendet")
        return 1

    # 1) Forschung Verteidigungsanlagen (Voraussetzung des Walls) - echter Weg.
    if not _erforschen(app, gs, ort, "Verteidigungsanlagen", 1):
        print("FEHLER: Verteidigungsanlagen liessen sich nicht erforschen")
        return 1
    print("Forschung Verteidigungsanlagen:", int(gs.research["Verteidigungsanlagen"].level))

    # 2) Wall errichten - GameState.wall_errichten (Preis und Ortsskasse aus den Daten).
    ok, meldung = gs.wall_errichten(ort)
    for _ in range(GEDULD):
        if ok:
            break
        _tick(gs, 20)                                # Rohstoffe fuer den Wall erwirtschaften
        ok, meldung = gs.wall_errichten(ort)
    print("Wall:", ok, meldung)
    if not ok:
        return 1

    # 3) STARTWERT Handelskarawane (Grund im Kopf dieser Datei).
    ort.einheiten[KARAWANE] = int(ort.einheiten.get(KARAWANE, 0) or 0) + 1
    # 4) STARTWERT Mauerzustand (Grund im Kopf dieser Datei).
    ort.mauer_zustand = float(MAUER_START)
    # 5) STARTWERT Mana (Grund im Kopf dieser Datei).
    gs.resources["mana"].amount = float(MANA_START)
    ort.vorraete["mana"] = float(MANA_START)

    # 6) Ein paar Takte, damit der Stand "gelebt" ist (Vorratsstaende, keine Sonderbuecher).
    _tick(gs, 24)

    # 7) Der Stand sagt selbst, dass er vorbereitet ist (Postfach, nicht nur Dateiname).
    gs.messages.append({"text": ("VORBEREITETER TESTSTAND vom 08.11.2026: Wall und Verteidigungs-"
                                 "anlagen stehen, eine Handelskarawane und 5000 Mana liegen bereit, "
                                 "die Mauer ist absichtlich bei 60 Prozent. Das ist kein Fehler im "
                                 "Spiel, sondern damit die spaeten Wege sofort testbar sind."),
                        "type": "system"})

    ordner = os.path.dirname(os.path.abspath(ziel))
    os.makedirs(ordner, exist_ok=True)
    ok_save = gs.save(ziel)
    print("gespeichert:", ok_save, ziel)
    print("Wallstufe am Ort:", gs.wall_stufe_am_ort(ort), "| Zustand:", ort.mauer_zustand)
    print("Karawanen im Ort:", ort.einheiten.get(KARAWANE, 0))
    print("Mana Reich/Ort:", gs.resources["mana"].amount, ort.vorraete.get("mana"))
    print("Spielzeit (s):", gs.spielsekunden, "| Forschung:", {k: int(v.level)
                                                              for k, v in gs.research.items()
                                                              if int(v.level or 0) > 0})
    print("Siedlungen:", len(gs.settlements), "| Bauten:", dict(ort.bauten))
    if fehler:
        print("WARNUNG: Ausnahmen im Fenster:", fehler[:1])
    try:
        root.destroy()
    except Exception:
        pass
    return 0 if ok_save is not False else 1


if __name__ == "__main__":
    ziel = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.expanduser("~"),
                                                              ".nebelseetal", "savegame_slot2.json")
    sys.exit(main_lauf(ziel))
