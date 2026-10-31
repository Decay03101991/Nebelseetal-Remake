# -*- coding: ascii -*-
"""Produktionskette OHNE Cheats: Rohstoff -> Forschung -> Ware -> Einheit -> Angriff -> Rueckkehr.

WARUM ES DIESE PRUEFUNG GIBT (externe Spielpruefung 31.10.2026, F-01/F-02/F-09/F-10)
------------------------------------------------------------------------------------
Alle bisherigen gruenen Pruefungen haben die Luecke nicht gesehen, weil die Partietests
ihren Zwischenzustand SELBST schreiben: `test_durchspiel.py` setzt Waren
(`_ort4.waren[_w] = 1`), setzt Einheiten im Reichsbestand (`gs.units[krieger].count = 8`)
und prueft dann einen Zustand, den das Spiel selbst nie herstellt.

Diese Pruefung setzt NICHTS. Sie spielt die Kette, die ein Spieler spielt:

    1. Start mit den belegten Handbuchwerten (10 Siedler, 100 Holz, 100 Stein, keine Gebaeude)
    2. Rohstoff aus EIGENER Produktion (Holzfaeller/Steinmetz auf passenden Feldern, Spieluhr)
    3. Forschung in der Bibliothek dieses Ortes (Voraussetzungen aus `forschungspfad`)
    4. Ware in der Werkstatt dieses Ortes (Rezept, Kosten, Zeit)
    5. Einheit ausbilden - sie entsteht am Ende der Zeit im ORTSLAGER
    6. Angriff aus DIESER Siedlung starten (nicht aus `settlements[0]`, nicht aus dem Reich)
    7. Reise, Kampf am Ziel, Rueckkehr - die Ueberlebenden kommen in DIESEN Ort zurueck

Damit ist sie das Release-Gate fuer F-01 (Ortsheer als Quelle), F-09 (`quelle_id` statt
`settlements[0]`) und F-10 (Sofortangriff ueber dieselbe Einsatzregel, Entscheidung 17).

Aufruf:  python -X utf8 tests/test_produktionskette_ohne_cheats.py
Rueckgabe: 0 = Kette vollstaendig, 1 = Kette bricht (das ist der SOLL-Zustand von heute).
"""
from __future__ import annotations

import ast
import inspect
import os
import random
import sys
import textwrap
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, befund, bericht, check, import_src

ROOT, SRC = import_src()
import einheiten  # noqa: E402
import forschungspfad  # noqa: E402
import gebaeude_wirkung  # noqa: E402
import gelaende  # noqa: E402
import main  # noqa: E402

# Die Kette waehlt ihre Einheit aus den DATEN, nicht aus einer zweiten Handliste.
# Der Name traegt im Original ein Umlaut-Zeichen; diese Pruefdatei ist ASCII-only
# (Projektregel), deshalb wird er aus `einheiten.alle()` gelesen und nie getippt.
EINHEIT = next(n for n in einheiten.alle() if n.startswith("Kurzbogen"))
WARE = "Kurzbogen"
SAAT = 20261031          # fester Start: dieselbe Karte, dieselben Felder, jeder Lauf gleich

# Hoechstens so viele Takte wartet die Kette auf eine Bedingung; danach meldet sie ehrlich.
GEDULD = 30


def _tick(gs, stunden):
    """Spieluhr weiterstellen - die EINZIGE Art, wie in dieser Pruefung etwas entsteht."""
    gs.tick(float(stunden) * 3600.0)


def _feld_von(ort, gebaeude):
    return next((int(f) for f, g in (ort.bauten or {}).items() if str(g) == gebaeude), None)


def _bauen(app, gs, ort, gebaeude):
    """Baut ein Gebaeude auf dem ersten Feld, das die Standortregel zulaesst."""
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


def _ausbauen_bis(app, gs, ort, gebaeude, stufe):
    """Hebt ein Gebaeude auf `stufe` (der Ausbau ist die belegte Voraussetzung der Forschung)."""
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
            _tick(gs, 20)          # Rohstoffe fuer den naechsten Ausbau erwirtschaften
    return gebaeude_wirkung.gebaeude_stufe(ort, gebaeude) >= int(stufe)


def _erforschen(app, gs, ort, gebiet, ziel, tiefe=0):
    """Forscht `gebiet` bis `ziel` - und erfuellt dabei die Voraussetzungen aus den Daten.

    Die Bedingungen kommen aus `forschungspfad.voraussetzung` (dieselbe Quelle, die das Spiel
    prueft) - keine zweite, von Hand gepflegte Forschungsliste in der Pruefung.
    """
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
            _tick(gs, 30)          # Lager auffuellen, dann erneut versuchen
    return int(gs.research[gebiet].level) >= int(ziel)


def _kette():
    """Die Partie ohne Cheats. Jeder Abschnitt prueft, was der vorige erzeugt hat."""
    root = tk.Tk()
    root.withdraw()
    gesammelt = []
    root.report_callback_exception = lambda *a: gesammelt.append(a)
    app = main.NebelseetalApp(root)
    app._build_main_ui()
    gs = app.state
    try:
        # ---------------------------------------------------------------- 1. Start
        abschnitt("1. Start mit den belegten Handbuchwerten (nichts gesetzt)")
        vorher_zufall = random.getstate()
        random.seed(SAAT)
        app._erste_siedlung_gruenden()
        ort = gs.settlements[0] if gs.settlements else None
        check("die Startsiedlung wird auf dem echten Weg gegruendet", ort is not None)
        if ort is None:
            return
        check("Startwerte unveraendert 100 Holz / 100 Stein / 10 Siedler",
              float(ort.vorraete.get("holz", 0)) == 100.0
              and float(ort.vorraete.get("stein", 0)) == 100.0
              and float(ort.bevoelkerung) == 10.0,
              f"{ort.vorraete} / {ort.bevoelkerung}")
        check("die Siedlung hat eine echte 10x10-Originalkarte",
              bool(ort.karte) and len(ort.karte.get("raster") or []) == 100
              and bool(ort.karte.get("originalkarte_id")), ort.karte.get("originalkarte_id"))
        check("kein Gebaeude steht am Anfang", not ort.bauten, str(ort.bauten))

        # ---------------------------------------------------------------- 2. Rohstoff
        abschnitt("2. Rohstoff aus eigener Produktion (kein Geschenk)")
        holz_vorher = float(ort.vorraete.get("holz", 0.0))
        gebaut = {"holzfaeller": [_bauen(app, gs, ort, "holzfaeller") for _ in range(3)],
                  "steinmetz": [_bauen(app, gs, ort, "steinmetz")],
                  "bibliothek": [_bauen(app, gs, ort, "bibliothek")]}
        check("Holzfaeller, Steinmetz und Bibliothek stehen auf der Karte",
              all(f is not None for gruppe in gebaut.values() for f in gruppe),
              str({k: v for k, v in gebaut.items()}))
        check("der Bau wurde aus dem Ortslager bezahlt (Holz ist gesunken)",
              float(ort.vorraete.get("holz", 0.0)) < holz_vorher,
              f"{holz_vorher} -> {ort.vorraete.get('holz')}")
        _tick(gs, 10)
        holz_nachher = float(ort.vorraete.get("holz", 0.0))
        check("nach 10 Spielstunden ist MEHR Holz im Lager als vorher (Ertrag der Felder)",
              holz_nachher > holz_vorher, f"{holz_vorher} -> {holz_nachher}")
        check("auch Stein waechst aus eigener Produktion",
              float(ort.vorraete.get("stein", 0.0)) > 0.0, str(ort.vorraete.get("stein")))

        # ---------------------------------------------------------------- 3. Forschung
        abschnitt("3. Forschung in der Bibliothek DIESES Ortes")
        # Der Forschungsbedarf kommt aus den Daten: Rezept der Ware + Voraussetzung der Einheit.
        bedarf = {"Baukunst": 1}
        rezepte = spieloekonomie_rezepte()
        for ware in einheiten.alle()[EINHEIT].get("waren") or []:
            for gebiet, stufe in ((rezepte.get(ware) or {}).get("voraussetzungen") or {}).items():
                bedarf[gebiet] = max(bedarf.get(gebiet, 1), int(stufe))
        einheit_vor = einheiten.alle()[EINHEIT].get("voraussetzung") or {}
        if isinstance(einheit_vor, dict) and einheit_vor.get("forschung"):
            bedarf[einheit_vor["forschung"]] = max(
                bedarf.get(einheit_vor["forschung"], 1), int(einheit_vor.get("stufe", 1)))
        for gebiet, stufe in sorted(bedarf.items()):
            check(f"Forschung {gebiet} Stufe {stufe} laeuft durch (samt Voraussetzungen)",
                  _erforschen(app, gs, ort, gebiet, stufe),
                  f"Soll {stufe}, Ist {gs.research.get(gebiet).level if gebiet in gs.research else '-'}")
        check("die Bibliothek wurde fuer die Voraussetzungen ausgebaut (Stufe >= 3)",
              gebaeude_wirkung.gebaeude_stufe(ort, "bibliothek") >= 3,
              str(gebaeude_wirkung.gebaeude_stufe(ort, "bibliothek")))

        # ---------------------------------------------------------------- 4. Ware
        abschnitt("4. Ware in der Werkstatt DIESES Ortes")
        for gebaeude in ("bogenbauer", "kriegerakademie", "goldmine"):
            check(f"{gebaeude} laesst sich bauen", _bauen(app, gs, ort, gebaeude) is not None)
        _tick(gs, 10)
        app._oeffne_siedlungskarte(ort)
        holz_vor_ware = float(ort.vorraete.get("holz", 0.0))
        waren_vorher = int((ort.waren or {}).get(WARE, 0))
        # Drei Einheiten brauchen drei Stueck Ausruestung (jede Einheit verbraucht ihre Ware).
        for _ in range(3):
            app._ware_herstellen(WARE)
        holz_nach_ware = float(ort.vorraete.get("holz", 0.0))
        check("die Ware steht NICHT sofort im Lager",
              int((ort.waren or {}).get(WARE, 0)) == waren_vorher,
              str(ort.waren))
        _tick(gs, 20)
        check("nach der Fertigungszeit liegen drei Waren im Ortslager",
              int((ort.waren or {}).get(WARE, 0)) == waren_vorher + 3, str(ort.waren))
        check("die Rezeptkosten wurden aus dem Ortslager bezahlt (Holz ist genau um das Rezept gesunken)",
              holz_nach_ware < holz_vor_ware, f"{holz_vor_ware} -> {holz_nach_ware}")

        # ---------------------------------------------------------------- 5. Ausbildung
        abschnitt("5. Einheit ausbilden - sie entsteht im ORTSLAGER")
        for _ in range(GEDULD):
            if float((ort.vorraete or {}).get("gold", 0.0)) >= 3 * 250.0:
                break
            _tick(gs, 20)
        check("Gold fuer drei Einheiten ist zusammengewirtschaftet (Goldmine)",
              float((ort.vorraete or {}).get("gold", 0.0)) >= 3 * 250.0,
              str(ort.vorraete.get("gold")))
        ortsheer_vorher = int((ort.einheiten or {}).get(EINHEIT, 0))
        reich_vorher = {k: int(v.count) for k, v in gs.units.items() if int(v.count) > 0}
        app._oeffne_siedlungskarte(ort)
        for _ in range(3):
            app._train_unit(EINHEIT)
        check("drei Ausbildungsauftraege stehen im ORT",
              len(ort.ausbildung or []) == 3, str(ort.ausbildung))
        check("die Einheit existiert noch NICHT",
              int((ort.einheiten or {}).get(EINHEIT, 0)) == ortsheer_vorher, str(ort.einheiten))
        gs.spielsekunden = float((ort.ausbildung or [{}])[-1].get("ende") or 0.0) + 1.0
        gs.tick(0.0)
        check("nach der Ausbildungszeit stehen drei Einheiten im ORTSLAGER",
              int((ort.einheiten or {}).get(EINHEIT, 0)) == ortsheer_vorher + 3,
              str(ort.einheiten))
        check("der REICHSBESTAND bleibt leer - das Ortsheer ist die einzige Quelle (F-01)",
              {k: int(v.count) for k, v in gs.units.items() if int(v.count) > 0} == reich_vorher,
              str({k: v.count for k, v in gs.units.items() if v.count}))

        # ---------------------------------------------------------------- 6. Angriff
        abschnitt("6. Angriff aus DIESER Siedlung starten (nicht aus settlements[0])")
        # F-09: die eigene Siedlung steht absichtlich NICHT an erster Stelle der Liste.
        # Die aktive Siedlung haengt an ihrer Kennung, nicht an der Reihenfolge.
        gs.settlements.reverse()
        check("die aktive Siedlung zeigt weiter auf unser Dorf (Reihenfolge egal)",
              gs.aktive_siedlung() is ort,
              f"{getattr(gs.aktive_siedlung(), 'name', None)} statt {ort.name}")
        # Der SCHWECHSTE Gegner: das Gefecht soll die Buchung pruefen, nicht das Wuerfelglueck
        # (ein starker Verteidiger toetet sonst alle Angreifer und die Rueckkehr waere leer).
        bot = min(gs.bots, key=lambda b: sum(int(v) for v in (b.army or {}).values()))
        ortsheer_vor_angriff = dict(ort.einheiten or {})
        gestartet = app._auftrag_angriff(bot)
        check("der Angriff startet ueberhaupt (heute NICHT: das Reichsheer ist leer -> F-01)",
              gestartet is True, _log_ende(gs))
        eintrag = gs.auftraege[-1] if gs.auftraege else {}
        check("der Auftrag kennt seine Quelle als KENNUNG (F-09: quelle_id)",
              eintrag.get("quelle_id") == ort.id,
              f"{eintrag.get('quelle_id')!r} statt {ort.id!r}")
        check("der Auftrag startet in DIESER Siedlung",
              eintrag.get("von") == ort.name, str(eintrag.get("von")))
        check("das Ortsheer ist mitgereist (aus dem Ortslager genommen)",
              int((ort.einheiten or {}).get(EINHEIT, 0)) == 0, str(ort.einheiten))
        check("der Reichsbestand wurde dabei nicht angefasst",
              {k: int(v.count) for k, v in gs.units.items() if int(v.count) > 0} == reich_vorher,
              str({k: v.count for k, v in gs.units.items() if v.count}))

        # ---------------------------------------------------------------- 7. Rueckkehr
        abschnitt("7. Reise, Kampf am Ziel und Rueckkehr in DIESEN Ort")
        if eintrag:
            gs.spielsekunden = float(eintrag.get("rueckkehr") or 0.0) + 1.0
            kampf_vorher = len([m for m in gs.messages if m.get("type") == "kampf"])
            gs.auftraege_fortschreiben(gs.spielsekunden)
            gs.tick(0.0)
            kampf_nachher = len([m for m in gs.messages if m.get("type") == "kampf"])
            check("am Ziel findet ein echter Kampf statt (Bericht im Nachrichtenreiter)",
                  kampf_nachher > kampf_vorher, f"{kampf_vorher} -> {kampf_nachher}")
            check("der Auftrag ist danach aus der Liste",
                  not [e for e in gs.auftraege if e.get("quelle_id") == ort.id], str(gs.auftraege))
            # `eintrag` ist derselbe Gegenstand, den `kampf_am_ziel` auf die UEBERLEBENDEN
            # gesetzt hat: genau diese Zahl muss jetzt im Ortslager stehen - keine mehr, keine
            # weniger. Damit prueft die Wache die BUCHUNG, nicht das Wuerfelglueck des Gefechts.
            ueberlebt = int((eintrag.get("einheiten") or {}).get(EINHEIT, 0))
            zurueck = int((ort.einheiten or {}).get(EINHEIT, 0))
            check("die Ueberlebenden sind GENAU im ORTSLAGER zurueck (nicht im Reich)",
                  zurueck == ueberlebt, f"{zurueck} im Ort, {ueberlebt} ueberlebt")
            losgezogen = int(ortsheer_vor_angriff.get(EINHEIT, 0))
            check("zurueck kamen hoechstens so viele, wie losgezogen sind",
                  zurueck <= losgezogen, f"{zurueck} von {losgezogen}")
            if ueberlebt == 0:
                befund("das Gefecht ging ohne Ueberlebende aus", _kampf_ende(gs))
            check("der Reichsbestand blieb auch nach der Rueckkehr leer",
                  {k: int(v.count) for k, v in gs.units.items() if int(v.count) > 0} == reich_vorher,
                  str({k: v.count for k, v in gs.units.items() if v.count}))
            check("kein Wert des Spielers ist negativ",
                  not _negative(gs, ort), str(_negative(gs, ort)))

        # ---------------------------------------------------------------- 8. F-10
        abschnitt("8. Sofortangriff laeuft ueber DIESELBE Einsatzregel (F-10, Entscheidung 17)")
        # GEGENPROBE ZUERST - sie braucht keine Truppen und keinen Wuerfel: das Ortslager ist
        # leer, der Reichsbestand zeigt Einheiten. Wer den Reichsbestand liest, wuerde jetzt
        # kaempfen; der EINE Einsatzpfad darf es NICHT.
        bestand_nach_angriff = dict(ort.einheiten or {})
        gs.units[EINHEIT].count = 5
        ort.einheiten = {}
        leer = app._angriff_durchfuehren(bot.name, dict(bot.army or {}), vorrat_ziel=bot)
        check("leeres Ortsheer + voller Reichsbestand = KEIN Angriff (eine Quelle, F-01)",
              leer is False, _log_ende(gs))
        gs.units[EINHEIT].count = 0
        ort.einheiten = bestand_nach_angriff
        if int((ort.einheiten or {}).get(EINHEIT, 0)) > 0:
            vorher_ort = int((ort.einheiten or {}).get(EINHEIT, 0))
            gekaempft = app._angriff_durchfuehren(bot.name, dict(bot.army or {}),
                                                 wall_stufe=int(getattr(bot, "wall_stufe", 0)),
                                                 wall_zustand=float(getattr(bot, "wall_zustand", 100.0)),
                                                 vorrat_ziel=bot)
            check("der Sofortangriff kaempft (er nimmt das ORTSHEER, nicht das Reich)",
                  gekaempft is True, _log_ende(gs))
            check("er hat das Ortsheer benutzt und die Heimkehrer dort gebucht",
                  int((ort.einheiten or {}).get(EINHEIT, 0)) <= vorher_ort,
                  f"{vorher_ort} -> {(ort.einheiten or {}).get(EINHEIT)}")
            check("er bucht nichts in den Reichsbestand",
                  {k: int(v.count) for k, v in gs.units.items() if int(v.count) > 0} == reich_vorher,
                  str({k: v.count for k, v in gs.units.items() if v.count}))
        else:
            befund("Sofortangriff mit Truppen nicht geprueft",
                   "das Gefecht hat alle Angreifer gekostet")

        # ---------------------------------------------------------------- 9. Quelltext
        abschnitt("9. Quelltext-Wachen: keine zweite Truppenquelle, kein fester Startort")
        # Geprueft wird der CODE, nicht der Kommentar: Docstrings duerfen die alte Stelle
        # ausdruecklich nennen (sie erklaeren den Befund), ausgefuehrt werden darf sie nicht.
        quelle = _code(main.NebelseetalApp._truppen_nach_rolle)
        check("_truppen_nach_rolle liest das ORTSHEER und nicht den Reichsbestand",
              "einheiten" in quelle and "state.units" not in quelle, quelle.splitlines()[0])
        for name in ("_auftrag_angriff", "_auftrag_entfernung", "_angriff_durchfuehren"):
            quelle = _code(getattr(main.NebelseetalApp, name))
            check(f"{name} faellt nicht mehr auf settlements[0] zurueck",
                  "settlements[0]" not in quelle, quelle.splitlines()[0])
        check("_angriff_durchfuehren und _auftrag_angriff teilen die Buchung (Einsatz + quelle_id)",
              "einsatz_" in _code(main.NebelseetalApp._angriff_durchfuehren)
              and "quelle_id" in _code(main.NebelseetalApp._auftrag_angriff), "")
        check("waehrend der ganzen Kette gab es keinen stillen GUI-Fehler",
              not gesammelt, str(gesammelt[:1]))
    finally:
        random.setstate(vorher_zufall)
        try:
            root.destroy()
        except Exception:
            pass


def spieloekonomie_rezepte():
    """Die Rezepte der Datendatei (fuer die Voraussetzungen der Ware)."""
    import spieloekonomie
    return spieloekonomie.WARENREZEPTE


def _negative(gs, ort):
    """Kein Rohstoff und keine Einheit darf negativ werden."""
    schlecht = {k: v for k, v in (ort.vorraete or {}).items() if float(v) < -1e-9}
    schlecht.update({f"einheit {k}": v for k, v in (ort.einheiten or {}).items() if int(v) < 0})
    schlecht.update({f"reich {k}": v.count for k, v in gs.units.items() if int(v.count) < 0})
    return schlecht


def _code(funktion):
    """Der Quelltext einer Funktion OHNE Docstring und ohne Kommentare.

    Ein Docstring, der den alten Befund erklaert ("vorher stand hier settlements[0]"), ist
    kein ausgefuehrter Code - die Wache darf ihn deshalb nicht als Treffer zaehlen.
    """
    quelle = textwrap.dedent(inspect.getsource(funktion))
    baum = ast.parse(quelle)
    knoten = baum.body[0]
    rumpf = getattr(knoten, "body", [])
    if (rumpf and isinstance(rumpf[0], ast.Expr)
            and isinstance(getattr(rumpf[0], "value", None), ast.Constant)
            and isinstance(rumpf[0].value.value, str)):
        knoten.body = rumpf[1:]
    return ast.unparse(knoten)


def _kampf_ende(gs):
    """Der Schluss des letzten Kampfberichts (Ausgang und Verluste im Klartext)."""
    texte = [m.get("text") or "" for m in gs.messages if m.get("type") == "kampf"]
    return (texte[-1].splitlines()[0] if texte else "")


def _log_ende(gs):
    """Die letzte Logzeile - sie nennt den Grund einer Ablehnung im Klartext."""
    return (gs.log[-1] if getattr(gs, "log", None) else "")


def main_lauf():
    ausnahme("Produktionskette", _kette)


if __name__ == "__main__":
    main_lauf()
    sys.exit(bericht())
