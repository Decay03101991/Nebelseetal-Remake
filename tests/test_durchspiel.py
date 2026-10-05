"""Durchspiel-Pruefung (Ziel des Auftrags: eine fehlerfreie, spielbare Partie).

Warum es diese Pruefung gibt
---------------------------
Die Einzelpruefungen decken je ein Modul oder eine Einhaengung ab. Dieses Paket spielt
stattdessen **eine Partie zusammen** — vom Start ueber Siedlungsgruendung, Bauen auf der
Karte, Forschung mit Wartezeit, Ausbildung, Auftrag mit Kampf am Ziel, Bot-Zug, Portalwechsel
bis Speichern/Laden — und prueft dabei die Stellen, die nur im **Zusammenspiel** sichtbar
werden: keine negativen Werte, nichts wird zweimal gebucht, keine stillen Rueckruf-Fehler.

Das Passworttor wird NICHT passiert (Regel: kein Passwort durch den Agenten); das Tor selbst
prueft `tests/test_tor.py`, die ausgelieferte Einzeldatei wird ausserdem aus einem anderen
Ordner startgeprueft (Belege in `docs/ENTWICKLUNGSPROTOKOLL.md`).

Aufruf:  python -X utf8 tests/test_durchspiel.py
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import time
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, befund, bericht, check, import_src

ROOT, SRC = import_src()
import einheiten  # noqa: E402
import werkstatt  # noqa: E402


def alle_text(w):
    """Alle Beschriftungen eines Fensterbaums (fuer die Nachrichtenpruefung)."""
    treffer = []
    for k in w.winfo_children():
        try:
            treffer.append(str(k.cget("text")))
        except Exception:
            pass
        treffer += alle_text(k)
    return treffer


def keine_negativen(gs):
    """Kein Rohstoff, keine Einheit und kein Bot-Vorrat darf je negativ werden."""
    schlecht = {k: v.amount for k, v in gs.resources.items() if float(v.amount) < 0}
    schlecht.update({f"einheit {k}": u.count for k, u in gs.units.items() if int(u.count) < 0})
    for b in gs.bots:
        schlecht.update({f"bot {b.name} {s}": m for s, m in (b.vorraete or {}).items()
                         if int(m) < 0})
    return schlecht


def baue(app, sied, key):
    """Baut ein Gebaeude auf dem ersten Feld, das die Standortregel zulaesst.

    Ablehnungen des Spiels sind ehrlich (Meldung im Log) — gesucht wird das naechste Feld.
    """
    app._oeffne_siedlungskarte(sied)
    app._karten_feld_waehlen(0)
    for i in range(len(sied.karte["raster"])):
        if str(i) in sied.bauten:
            continue
        app._karten_feld_waehlen(i)
        vorher = len(sied.bauten)
        app._karten_bauen(key)
        if len(sied.bauten) > vorher:
            return i
    return None


def partiedurchlauf():
    """Die Partie in einem Block: ein Fehler bricht sie ab, statt weiterzuspielen."""
    main = ausnahme("main importieren", lambda: __import__("main"))
    if main is None:
        return

    root = tk.Tk()
    root.withdraw()
    gesammelt = []
    root.report_callback_exception = lambda *a: gesammelt.append(a)
    try:
        # ------------------------------------------------------------- 1. Start
        abschnitt("1. Start — Oberflaeche, Ansichten, erste Siedlung")
        app = main.NebelseetalApp(root)
        app._build_main_ui()
        root.update()
        gs = app.state
        check("das Spiel startet ohne stillen Rueckruf-Fehler", not gesammelt, str(gesammelt[:1]))
        check("die Startwerte stehen wie im Handbuch (10 Siedler, 100 Holz, 100 Steine)",
              int(gs.population) == 10 and gs.resources["holz"].amount == 100
              and gs.resources["stein"].amount == 100,
              f"{gs.population} / {gs.resources['holz'].amount} / {gs.resources['stein'].amount}")

        for ansicht in list(main.MENU_ITEMS):
            app._switch_view(ansicht)
            root.update()
        app._switch_view("Dorfzentrum")
        check("alle Menuepunkte lassen sich oeffnen, ohne stillen Fehler",
              not gesammelt, str(gesammelt[:1]))

        gs.resources["holz"].amount = 3000.0
        gs.resources["stein"].amount = 3000.0
        gs.resources["nahrung"].amount = 3000.0
        gs.resources["gold"].amount = 3000.0
        gs.population = 60.0
        app._found_settlement()
        check("die erste Siedlung wird gegruendet", bool(gs.settlements))
        sied = gs.settlements[0]
        check("sie hat eine eigene Karte mit 56 Feldern",
              bool(sied.karte) and len(sied.karte["raster"]) == 56,
              str(len(sied.karte["raster"]) if sied.karte else 0))

        # ------------------------------------------------------------- 2. Bauen
        abschnitt("2. Bauen auf der Siedlungskarte")
        gebaut = {key: baue(app, sied, key)
                  for key in ("holzfaeller", "haus", "bibliothek", "kriegerakademie", "schmiede")}
        check("alle fuenf Gebaeude stehen auf der Karte",
              all(v is not None for v in gebaut.values()), str(gebaut))
        felder = [v for v in gebaut.values() if v is not None]
        check("kein Gebaeude steht zweimal auf demselben Feld", len(set(felder)) == len(felder))
        check("nach dem Bauen ist kein Wert negativ",
              not keine_negativen(gs), str(keine_negativen(gs)))

        # Ein Gebaeude MIT belegten Stufen ausbauen. Das Haus hat laut Handbuch keine Stufen —
        # die Ablehnung („Haus kennt keinen Ausbau") ist richtig und steht ehrlich im Log.
        feld_bib = gebaut.get("bibliothek")
        if feld_bib is not None:
            app._karten_feld_waehlen(feld_bib)
            stufe_vorher = int(sied.stufen.get(str(feld_bib), 1))
            app._karten_ausbauen()
            stufe_nachher = int(sied.stufen.get(str(feld_bib), 1))
            check("ein Feld mit belegten Stufen laesst sich ausbauen (Ausbaustufe steigt)",
                  stufe_nachher == stufe_vorher + 1, f"{stufe_vorher} -> {stufe_nachher}")

        # ------------------------------------------------------------- 3. Forschung
        abschnitt("3. Forschung braucht Zeit (W4c)")
        forsch_key = ("Felderwirtschaft" if "Felderwirtschaft" in gs.research
                      else next(iter(gs.research)))
        stufe0 = int(gs.research[forsch_key].level)
        check("die Forschung startet mit der Bibliothek", app._start_research(forsch_key) is True)
        check("die Stufe steigt NICHT im selben Klick", int(gs.research[forsch_key].level) == stufe0)
        gs.forschungsauftraege[forsch_key]["startzeit"] -= 24 * 3600.0
        gs.tick(0.0)
        check("nach Ablauf der Zeit steigt sie genau einmal",
              int(gs.research[forsch_key].level) == stufe0 + 1
              and forsch_key not in gs.forschungsauftraege,
              f"{stufe0} -> {gs.research[forsch_key].level}")

        # ------------------------------------------------------------- 4. Ausbildung
        abschnitt("4. Einheiten ausbilden")
        for stoff in ("wolle", "leder", "pferde", "metall", "gold", "nahrung"):
            gs.resources[stoff].amount = 5000.0

        def bezahlbar(k):
            """Reicht unser Lager fuer die belegten Kosten dieser Einheit? (Siedler = Bevoelkerung)"""
            for stoff, menge in (einheiten.alle()[k].get("kosten") or {}).items():
                res = gs.resources.get(stoff)
                if res is not None and res.amount < menge:
                    return False
            return True

        krieger = next((k for k, u in gs.units.items()
                        if u.rolle == "kaempfer" and bezahlbar(k)), None)
        check("es gibt eine bezahlbare Kampfeinheit im Spiel", krieger is not None)
        vorher_anzahl = int(gs.units[krieger].count)
        app._train_unit(krieger)
        check("mit der Kriegerakademie laesst sich eine Kampfeinheit ausbilden",
              int(gs.units[krieger].count) == vorher_anzahl + 1,
              f"{krieger}: {vorher_anzahl} -> {gs.units[krieger].count}")
        check("dafuer wurde bezahlt, ohne ins Minus zu rutschen", not keine_negativen(gs))

        # ------------------------------------------------------------- 5. Auftrag
        abschnitt("5. Auftrag: angreifen, kaempfen, heimkehren")
        bot = gs.bots[0]
        for u in gs.units.values():
            if u.rolle == "karren":
                u.count = 2
        gs.units[krieger].count = 8
        auftrag_ok = app._auftrag_angriff(bot)
        check("der Auftrag startet", auftrag_ok is True)
        check("die Einheiten sind unterwegs (aus dem Bestand genommen)",
              int(gs.units[krieger].count) == 0, str(gs.units[krieger].count))
        eintrag = gs.auftraege[0]
        eintrag["start"] = time.time() - (float(eintrag["reisezeit"]) * 2.0 + 300.0)
        vorher_berichte = len([m for m in gs.messages if m.get("type") in ("auftrag", "kampf")])
        gs.auftraege_fortschreiben(time.time())
        nachher_berichte = len([m for m in gs.messages if m.get("type") in ("auftrag", "kampf")])
        check("die Ankunft erzeugt Berichte (Auftrag und Kampf am Ziel)",
              nachher_berichte > vorher_berichte, f"{vorher_berichte} -> {nachher_berichte}")
        kampf_meldungen = [m["text"] for m in gs.messages if m.get("type") == "kampf"]
        check("die Kampfmeldung nennt das Ziel (nicht nur das Log)",
              any(("Ziel " + bot.name) in t for t in kampf_meldungen),
              str(kampf_meldungen[:1])[:120])
        check("die ueberlebenden Einheiten kommen heim",
              int(gs.units[krieger].count) > 0, str(gs.units[krieger].count))
        check("der Auftrag ist aus der Liste", not gs.auftraege)
        check("die Bot-Vorrate bleiben nicht negativ",
              all(int(v) >= 0 for v in bot.vorraete.values()), str(bot.vorraete))
        check("kein Wert des Spielers ist negativ",
              not keine_negativen(gs), str(keine_negativen(gs)))

        # ------------------------------------------------------------- 6. Bots
        abschnitt("6. Ein Bot-Zug im Zeitlauf (W5)")
        gs._letzter_bot_takt = 0.0
        zug = gs.bots_fortschreiben(time.time())
        check("der Bot-Zug laeuft ueber alle Bots", zug["bots"] == len(gs.bots), str(zug["bots"]))
        check("in derselben Stunde laeuft kein zweiter Zug",
              gs.bots_fortschreiben(time.time())["bots"] == 0)
        check("die Bots bleiben im Plus", not keine_negativen(gs), str(keine_negativen(gs)))

        # ------------------------------------------------------------- 7. Speichern
        abschnitt("7. Speichern und Laden mitten im Spiel")
        pfad = os.path.join(tempfile.gettempdir(), "nebel_durchspiel.json")
        for endung in ("", ".bak", ".tmp"):
            if os.path.exists(pfad + endung):
                os.remove(pfad + endung)
        merk = {"holz": gs.resources["holz"].amount, "stufe": int(gs.research[forsch_key].level),
                "siedlungen": [s.name for s in gs.settlements],
                "einheiten": {k: int(u.count) for k, u in gs.units.items()},
                "bot": dict(gs.bots[0].vorraete)}
        check("das Speichern meldet Erfolg", gs.save(pfad) is True)
        zweit = main.GameState()
        check("das Laden meldet Erfolg", zweit.load(pfad) is True)
        ist = {"holz": zweit.resources["holz"].amount, "stufe": int(zweit.research[forsch_key].level),
               "siedlungen": [s.name for s in zweit.settlements],
               "einheiten": {k: int(u.count) for k, u in zweit.units.items()},
               "bot": dict(zweit.bots[0].vorraete)}
        abweichung = {k: (merk[k], ist[k]) for k in merk if merk[k] != ist[k]}
        check("Holz, Forschungsstufe, Siedlungen, Einheiten und Bot-Vorrat kommen unveraendert zurueck",
              not abweichung, f"weicht ab: {abweichung}")
        roh = json.load(open(pfad, encoding="utf-8"))
        check("die Spielstandsdatei ist lesbares JSON mit allen Bereichen",
              {"auftraege", "forschungsauftraege", "bots", "settlements"} <= set(roh))
        for endung in ("", ".bak", ".tmp"):
            if os.path.exists(pfad + endung):
                os.remove(pfad + endung)

        # ------------------------------------------------------------- 8. Portal
        abschnitt("8. Portal: Wechsel kostet 5.000 Mana und sperrt 24 Stunden")
        gs.resources["mana"].amount = 6000.0
        ziel_dimension = 2 if int(gs.eigene_dimension) != 2 else 3
        check("der Koordinatenwechsel wird gebucht", app._portal_wechsel(ziel_dimension) is True)
        check("genau 5.000 Mana sind weg", gs.resources["mana"].amount == 1000.0,
              str(gs.resources["mana"].amount))
        check("die Sperre steht", gs.letzter_wechsel is not None)
        mana_vorher = gs.resources["mana"].amount
        check("in der Sperre ist kein zweiter Wechsel moeglich",
              app._portal_wechsel(ziel_dimension) is False
              and gs.resources["mana"].amount == mana_vorher)

        # ------------------------------------------------------------- 10. Handel
        abschnitt("10. Handel mit einem Bot")
        bot.trading = 0.9
        bot.gehandelt = 0
        log_vorher = len(gs.log)
        handel = app._trade(bot)
        check("der Handel laeuft und nennt die belegte Schwelle",
              handel is True and any("Schwellenpreis" in z for z in gs.log[log_vorher:]),
              str(gs.log[log_vorher:]))
        check("der Handel wird am Bot gezaehlt", int(bot.gehandelt) == 1)
        bot.trading = 0.1
        check("ein Bot ohne Handelsneigung handelt nicht", app._trade(bot) is False)

        # ------------------------------------------------------------- 11. Werkstatt
        abschnitt("11. Werkstatt: eine Ware herstellen")
        check("die gebaute Schmiede fuehrt eine Warteschlange",
              "schmiede" in gs.werkstatt_schlangen(), str(list(gs.werkstatt_schlangen())))
        ware = next((w for w in werkstatt.waren_der_werkstatt("schmiede")
                     if gs.ware_voraussetzung(w)[0]), None)
        check("es gibt eine Ware mit erfuellter Voraussetzung", ware is not None, str(ware))
        check("sie laesst sich einreihen", app._ware_herstellen("schmiede", ware) is True)
        if ware and not werkstatt.dauer_sekunden(ware, 1):
            befund(f"Ware '{ware}' ohne belegte Dauer",
                   "das Handbuch nennt fuer sie keine Bauzeit — sie bleibt wartend in der "
                   "Warteschlange stehen (ehrlich, es wird nichts erfunden); die Lieferung "
                   "selbst prueft test_werkstatt mit einer belegten Ware")

        # ------------------------------------------------------------- 12. Karte
        abschnitt("12. Kartenwechsel und Kartenangriff")
        gs.resources["gold"].amount = 5000.0
        gold_vorher = gs.resources["gold"].amount
        switch_kosten = gs.map_switch_cost
        app._activate_map("wald")
        check("eine noch nicht freigeschaltete Karte wird ehrlich abgelehnt (kein Gold weg)",
              gs.current_map != "wald" and gs.resources["gold"].amount == gold_vorher,
              f"{gs.current_map} / {gs.resources['gold'].amount}")
        gs.active_maps = list(dict.fromkeys(list(gs.active_maps) + ["wald"]))
        app._activate_map("wald")
        check("der Kartenwechsel kostet Gold und wechselt die Karte",
              gs.current_map == "wald"
              and gs.resources["gold"].amount == gold_vorher - switch_kosten,
              f"{gs.current_map} / {gs.resources['gold'].amount}")
        gs.units[krieger].count = 8
        kampf_vorher = len([m for m in gs.messages if m.get("type") == "kampf"])
        app._attack_map("wald")
        kampf_nachher = len([m for m in gs.messages if m.get("type") == "kampf"])
        check("ein Kartenangriff erzeugt einen Kampfbericht",
              kampf_nachher > kampf_vorher, f"{kampf_vorher} -> {kampf_nachher}")
        check("der Kartenbericht nennt das Ziel der Karte",
              any("Nebelwald" in m["text"] for m in gs.messages if m.get("type") == "kampf"),
              str([m["text"][:40] for m in gs.messages if m.get("type") == "kampf"][-1:]))
        check("auch nach dem Kartenangriff ist kein Wert negativ",
              not keine_negativen(gs), str(keine_negativen(gs)))

        # ------------------------------------------------------------- 9. Schlussstand
        abschnitt("9. Schlussstand")
        app._switch_view("Nachrichten")
        root.update()
        texte = alle_text(app.content)
        check("die Nachrichten zeigen die Berichte der Partie",
              any("Auftragsbericht" in t or "Schlachtsbericht" in t or "Forschung" in t
                  for t in texte), str(texte[:3]))
        check("kein stiller tkinter-Fehler im ganzen Durchlauf", not gesammelt, str(gesammelt[:1]))
        check("zum Schluss ist kein Wert negativ",
              not keine_negativen(gs), str(keine_negativen(gs)))
        befund("Passworttor",
               "in dieser Pruefung absichtlich NICHT passiert — das Tor prueft tests/test_tor.py, "
               "die Einzeldatei wird aus einem anderen Ordner startgeprueft")
    finally:
        try:
            root.destroy()
        except Exception:
            pass


partiedurchlauf()
sys.exit(bericht())
