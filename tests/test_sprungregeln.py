# -*- coding: ascii -*-
"""Wache: die Sprungregeln der Doerfer (Daniels Entscheidungen 12.11.2026).

DANIELS WOERTER (12.11.2026, nach Claudes Sprungregeln)
-------------------------------------------------------
  "Doerfer duerfen auf der weltkarte nicht auf dem selben feld landen."
  "jede fraktion hat ihre weltkarte und startet auch auf dieser ... der Spieler [hat] anfangs
   in seiner welt sowieso noch keinen feind."
  regel 9: "Moeglichkeit A" - das Dorf darf springen, der anfliegende Marsch kehrt ohne Kampf um.
  sperre:  "Claudes Regel 4" - nur die Truppen DIESES Dorfes zaehlen (vorher global, 01.11.2026).

WAS DIESE DATEI PRUEFT
----------------------
1. Ein Feld traegt NIE zwei Doerfer (`bot_doerfer_positionen_entzerren`).
2. Drachen und Ruinen sperren ein Feld auch fuer den Spieler-Umzug (Daniel 05.11.2026) - das war
   eine Luecke: `drachen_blockiert` wurde nur beim Bot-Gruenden gefragt.
3. Nebelsee und jedes andere nicht bebaubare Gelaende sperrt den Umzug; Grasland nicht.
4. Die Sperre gilt nur fuer das SPRINGENDE Dorf: ein anderes Dorf desselben Spielers mit einem
   laufenden Auftrag blockiert den Sprung nicht mehr (geaenderte Entscheidung).
5. Regel 9A: ein anfliegender Marsch auf ein gesprungenes Dorf endet ohne Kampf - keine
   Verluste, keine Beute, die Truppen kommen zurueck.

Aufruf:  python -X utf8 tests/test_sprungregeln.py
"""
from __future__ import annotations

import ast
import inspect
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src, messwert  # noqa: E402

import_src()
import auftraege  # noqa: E402
import main  # noqa: E402
import portalraum  # noqa: E402


def _code(fn) -> str:
    """Der Rumpf einer Funktion als Code - der Docstring zaehlt NICHT."""
    baum = ast.parse(inspect.getsource(fn).lstrip())
    knoten = baum.body[0]
    rumpf = getattr(knoten, "body", [])
    if rumpf and isinstance(rumpf[0], ast.Expr) and isinstance(getattr(rumpf[0], "value", None), ast.Constant) \
            and isinstance(rumpf[0].value.value, str):
        knoten.body = rumpf[1:]
    return ast.unparse(knoten)


# --------------------------------------------------------------------------------------
def _aufbau():
    """Eine App mit einem gegruendeten Dorf - ohne Fenster zu zeigen."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    app = main.NebelseetalApp(root)
    app._build_main_ui()
    app._erste_siedlung_gruenden()
    return root, app


# --------------------------------------------------------------------------------------
def _quellwachen():
    abschnitt("1. Quellwachen: die drei Pruefungen stehen im Umzug")
    code = _code(main.NebelseetalApp._dorf_versetzen)
    check("der Umzug fragt Drachen und Ruinen", "drachen_blockiert" in code)
    check("der Umzug fragt das Gelaende", "bebaubar" in code.lower())
    check("die Sperre fragt das EIGENE Dorf, nicht den ganzen Spieler",
          "_dorf_unterwegs" in code and "_unterwegs_anzahl" not in code,
          code[:200])
    check("die alte Entscheidung ist im Text genannt (nicht geloescht)",
          "01.11.2026" in inspect.getsource(main.NebelseetalApp._dorf_versetzen))
    kampf = _code(main.GameState.kampf_am_ziel)
    check("der Kampf steigt bei einem gesprungenen Ziel aus", "ziel_gesprungen" in kampf)
    stelle_ausstieg = kampf.find("ziel_gesprungen")
    stelle_kampf = kampf.find("fuehre_schlacht")
    check("der Ausstieg steht VOR dem Kampf",
          stelle_ausstieg >= 0 and (stelle_kampf < 0 or stelle_ausstieg < stelle_kampf),
          "Ausstieg %d, Schlacht %d" % (stelle_ausstieg, stelle_kampf))


# --------------------------------------------------------------------------------------
def _sperren():
    abschnitt("2. Feldregeln: Drache, Ruine, Nebelsee, Grasland - am echten Umzug")
    import json
    root, app = _aufbau()
    try:
        ort = app.state.settlements[0]
        welt = int(app.state.eigene_dimension)
        index = portalraum.index_von(welt)
        daten = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                            "data", "gelaende.json"), encoding="utf-8"))
        arten = {e["id"]: bool(e.get("bebaubar")) for e in daten["gelaendearten"]}
        # BEFUND 12.11.2026: Claudes Sprungregeln sagen "Nebelsee ist nie besetzbar". Das
        # widerspricht der belegten Quelle: auf dem Nebelsee steht ein TEMPEL (8 Mana/h,
        # Handbuch 2009: 5 Mana/h), und unbebaubar ist laut Handbuch S. 11 der SUMPF.
        # Der Code folgt darum den DATEN, nicht dem Modelltext.
        check("Sumpf ist in den DATEN nicht bebaubar (Handbuch S. 11)", arten.get("sumpf") is False, str(arten))
        check("Nebelsee ist bebaubar - dort steht der Tempel", arten.get("nebelsee") is True, str(arten))
        check("Grasland ist bebaubar", arten.get("grasland") is True)
        befund("Claudes Regel 2 widerspricht dem Original",
               "Nebelsee ist NICHT gesperrt - auf ihm steht der Tempel; unbebaubar ist der Sumpf")
        check("der Helfer _portal_feld_bebaubar existiert", hasattr(app, "_portal_feld_bebaubar"))
        if not hasattr(app, "_portal_feld_bebaubar"):
            return
        kante = int(portalraum._achsen())
        raster = portalraum.anzeige_raster(index, kante)
        wasser = next((f for f in raster if f.get("gelaende_bebaubar") is False), None)
        land = next((f for f in raster if f.get("gelaende_bebaubar") is True), None)
        check("es gibt ein nicht bebaubares Feld", wasser is not None)
        if wasser is not None:
            check("der Helfer sperrt das Wasserfeld",
                  app._portal_feld_bebaubar(index, int(wasser["x"]), int(wasser["y"])) is False,
                  str(wasser.get("gelaende")))
        if land is not None:
            check("der Helfer erlaubt das Landfeld",
                  app._portal_feld_bebaubar(index, int(land["x"]), int(land["y"])) is True,
                  str(land.get("gelaende")))
        # Der ECHTE Umzug auf ein nicht bebaubares Feld muss abgelehnt werden.
        if wasser is not None:
            vorher = float(app.state.resources["mana"].amount)
            erlaubt = app._dorf_versetzen(str(ort.name), int(wasser["x"]), int(wasser["y"]), welt)
            check("der Umzug auf Wasser wird abgelehnt", erlaubt is False, str(erlaubt))
            check("dafuer wird kein Mana abgebucht",
                  float(app.state.resources["mana"].amount) == vorher,
                  "%s zu %s" % (app.state.resources["mana"].amount, vorher))
        # Drache oder Ruine sperrt sein Feld. Auf der Spielerwelt steht heute KEIN Drache
        # (gemessen: die drei Drachen liegen auf den Welten 2, 3 und 5) - der Helfer wird darum
        # auf der Welt geprueft, auf der wirklich einer steht.
        import drachen as D
        figur = next(iter(D.alle()), None)
        check("es gibt ueberhaupt einen Drachen zum Pruefen", figur is not None)
        if figur is not None:
            d_welt = int(str(figur.get("welt"))[-1])                   # "d02" -> 2
            dx, dy = app.state.drachen_position(figur)
            check("drachen_blockiert sperrt sein Feld",
                  app.state.drachen_blockiert(d_welt, int(dx), int(dy)) is True, str((dx, dy)))
            check("dasselbe Feld ist gelaendemaessig bebaubar (nur der Drache sperrt)",
                  app._portal_feld_bebaubar(portalraum.index_von(d_welt), int(dx), int(dy)) is True)
            befund("auf der Spielerwelt steht kein Drache",
                   "die drei Drachen liegen auf den Welten 2, 3 und 5; der Umzug kann dort heute "
                   "nicht an einem Drachen scheitern - der Pfad ist ueber die Quellwache belegt")
        messwert("kante", kante, "Felder")
    finally:
        root.destroy()


def _sperre_je_dorf():
    abschnitt("3. Die Sperre gilt nur fuer das springende Dorf")
    root, app = _aufbau()
    try:
        ort = app.state.settlements[0]
        check("der Helfer _dorf_unterwegs existiert", hasattr(app, "_dorf_unterwegs"))
        if not hasattr(app, "_dorf_unterwegs"):
            return
        # Ein laufender Auftrag, der NICHT von diesem Dorf ausgeht, darf nicht sperren.
        fremd = {"art": "angreifen", "einheiten": {"Kaempfer": 1}, "start": app.state.spielsekunden,
                 "reisezeit": 9999, "aktion_dauer": 0, "von": "Ein anderes Dorf",
                 "nach": "irgendwo", "quelle_id": "eine-andere-kennung"}
        app.state.auftraege = [fremd]
        check("ein fremder Auftrag sperrt dieses Dorf NICHT",
              int(app._dorf_unterwegs(ort)) == 0, str(app._dorf_unterwegs(ort)))
        # Ein Auftrag DIESES Dorfes sperrt es.
        eigen = dict(fremd, von=str(ort.name), quelle_id=str(getattr(ort, "id", "") or ""))
        app.state.auftraege = [eigen]
        check("ein Auftrag DIESES Dorfes sperrt es",
              int(app._dorf_unterwegs(ort)) >= 1, str(app._dorf_unterwegs(ort)))
        messwert("sperre_eigene", int(app._dorf_unterwegs(ort)), "Auftraege")
    finally:
        root.destroy()


def _regel9():
    abschnitt("4. Regel 9A: der Marsch kehrt ohne Kampf um")
    root, app = _aufbau()
    try:
        eintrag = {"art": "angreifen", "einheiten": {"Kaempfer": 3},
                   "start": float(app.state.spielsekunden), "reisezeit": 10.0, "aktion_dauer": 0.0,
                   "von": "Testdorf", "nach": "Zieldorf", "ziel": {"name": "Zieldorf"},
                   "ziel_gesprungen": True}
        ergebnis = app.state.kampf_am_ziel(eintrag)
        check("das Ergebnis meldet den gesprungenen Ziel",
              bool(ergebnis.get("ziel_gesprungen")) if isinstance(ergebnis, dict) else False,
              str(ergebnis)[:120])
        if isinstance(ergebnis, dict):
            check("es faellt niemand",
                  not ergebnis.get("verluste_angreifer") and not ergebnis.get("verluste_verteidiger"),
                  str(ergebnis.get("verluste_angreifer")))
            check("es gibt keine Beute",
                  not ergebnis.get("beute"), str(ergebnis.get("beute")))
        check("die Truppen des Auftrags bleiben unangetastet",
              dict(eintrag.get("einheiten") or {}) == {"Kaempfer": 3}, str(eintrag.get("einheiten")))
        befund("Sichtpruefung der Marsch-Anzeige steht aus",
               "der Merker ist gerechnet, die Karte zeigt ihn noch nicht an")
    finally:
        root.destroy()


# --------------------------------------------------------------------------------------
if __name__ == "__main__":
    _quellwachen()
    _sperren()
    _sperre_je_dorf()
    _regel9()
    sys.exit(bericht())
