"""Durchspiel mit START-WERTEN ueber ECHTE Knopfdruecke — findet „es passiert nichts".

Warum es diese Pruefung gibt
---------------------------
Am 05.10.2026 meldete Daniel nach dem Spielen: „spielbar ist hier noch gar nichts … ich kann
keine neue Siedlung gruenden, weil es passiert ja gar nichts … Karte bebauen, Truppen
ausbilden, forschen — keines der Ziele erfuellt." Der Sammellauf war gleichzeitig GRUEN.

Der Grund war eine Luecke in der Pruefung selbst, nicht im Testrahmen:

* `tests/test_gui_fehler.py` faehrt die Aktionen ueber die METHODEN der App
  (`app._found_settlement()`), nie ueber die Schaltflaechen im Fenster.
* Es setzt vorher `resources = 100000` und `population = 5000` — die Startwerte des
  Handbuchs (100 Holz, 100 Stein, 10 Siedler) kommen nie vor.
* Es prueft den ZUSTAND („die Siedlung steht in `state.settlements`"), nie das FENSTER
  („steht sie auch in der Liste, gibt es den Knopf ‚Karte öffnen'"). Genau dort lag der
  Fehler: `_found_settlement` zeichnete die Ansicht nicht neu — der Spieler sah nichts.

Diese Pruefung spielt deshalb wie ein Mensch: sie DRUECKT die Knoepfe im Fenster
(`Button.invoke()`, also ueber Tkinter-CallWrapper) und prueft nach jedem Schritt BEIDES —
den Zustand und das, was im Fenster steht.

Aufruf:  python -X utf8 tests/test_startspiel.py   (braucht einen angemeldeten Desktop)
"""
from __future__ import annotations

import os
import sys
import time
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, bericht, befund, check, import_src   # noqa: E402

ROOT, SRC = import_src()
os.chdir(SRC)

import tkinter as tk                                  # noqa: E402
import main                                           # noqa: E402
import karten_optik_fein                              # noqa: E402

# ---------- Hilfen: im Fenster lesen und druecken ----------

_still: list = []


def _texte(widget) -> list:
    """Alle sichtbaren Beschriftungen unterhalb von *widget*."""
    out = []
    try:
        t = widget.cget("text")
        if t:
            out.append(str(t))
    except Exception:
        pass
    for k in widget.winfo_children():
        out.extend(_texte(k))
    return out


def _knoepfe(widget, teil: str) -> list:
    t = []
    try:
        if widget.winfo_class() == "Button" and teil.lower() in str(widget.cget("text")).lower():
            t.append(widget)
    except Exception:
        pass
    for k in widget.winfo_children():
        t.extend(_knoepfe(k, teil))
    return t


def _drueck(app, teil: str):
    """Drueckt die erste Schaltflaeche, deren Beschriftung *teil* enthaelt. (gefunden, beschriftung)"""
    ks = _knoepfe(app.root, teil)
    if not ks:
        return False, ""
    beschriftung = str(ks[0].cget("text")).split("\n")[0]
    ks[0].invoke()          # echter Tkinter-Aufruf: Ausnahmen landen im Sammler
    app.root.update_idletasks()
    app.root.update()
    return True, beschriftung


def main_() -> int:
    try:
        root = tk.Tk()
    except tk.TclError as fehler:
        print(f"Kein Fenster moeglich (kein Desktop): {fehler}")
        print("Diese Pruefung braucht einen angemeldeten Windows-Desktop.")
        return 0
    root.withdraw()

    app = ausnahme("App aufbauen", lambda: main.NebelseetalApp(root))
    if app is None:
        root.destroy()
        return bericht()
    ausnahme("Hauptoberflaeche aufbauen", app._build_main_ui)
    root.report_callback_exception = lambda e, w, s: _still.append(f"{e.__name__}: {w}")

    st = app.state

    def tick():
        root.update_idletasks()
        root.update()

    # ---------------------------------------------------------------- 1 Startwerte
    abschnitt("1. Start wie im Handbuch (S. 7): 100 Holz, 100 Stein, 10 Siedler")
    check("Holz startet mit 100", st.resources["holz"].amount == 100, str(st.resources["holz"].amount))
    check("Stein startet mit 100", st.resources["stein"].amount == 100, str(st.resources["stein"].amount))
    check("10 Siedler zu Beginn", st.population == 10, str(st.population))
    check("keine Siedlung zu Beginn", not st.settlements, str(len(st.settlements)))
    check("kein Gold zu Beginn (Gold kommt aus dem Bergbau/Handel)", st.resources["gold"].amount == 0,
          str(st.resources["gold"].amount))

    # ---------------------------------------------------------------- 2 Siedlung gruenden
    abschnitt("2. Siedlung gruenden — ueber den Knopf im Fenster")
    app._switch_view("Dorfzentrum")
    tick()
    gefunden, beschriftung = _drueck(app, "Neue Siedlung")
    check("der Knopf 'Neue Siedlung gründen' steht im Dorfzentrum", gefunden, beschriftung)
    check("danach gibt es genau eine Siedlung", len(st.settlements) == 1, str(len(st.settlements)))
    fenster = _texte(app.content)
    check("die neue Siedlung steht SICHTBAR in der Liste",
          any("Siedlung 1" in z for z in fenster),
          " | ".join(z for z in fenster if "Siedlung" in z) or "(nichts)")
    check("der Knopf 'Karte öffnen' wird angeboten",
          any("Karte" in z and "öffnen" in z for z in fenster), str(fenster)[:200])
    check("die Statuszeile nennt die Gruendung (nicht nur die technische Karte)",
          "gegründet" in app.lbl_status.cget("text"), app.lbl_status.cget("text")[:120])
    # Das war der eigentliche Fehler: ohne Neuzeichnen blieb die Liste leer.
    check("die Ansicht wurde neu gezeichnet (kein stiller Knopfdruck)",
          not _still, " | ".join(_still))

    # ------------------------------------------- 2b Daniels Spielbericht vom 05.10.2026
    # „so kann es passieren, dass man kein holz mehr bekommt, weil man keinen holzfäller
    # gebaut hatte" — die Aufgabenkarte muss den fehlenden Erzeuger VOR dem Forschen nennen.
    abschnitt("2b. Aufgabenkarte nennt den fehlenden Rohstoff-Erzeuger")
    _schritt = app.naechster_schritt()
    check("ohne Gebäude führt sie zum Holzfäller", "Holzfäller" in _schritt["text"],
          _schritt["text"][:160])

    _sied = st.settlements[0]
    _raster = _sied.karte["raster"]
    _gras = [i for i, a in enumerate(_raster) if a == "grasland"]
    if _gras:
        ok, meldung = main.bauen_auf_karte(_sied, "haus", _gras[0])
        check("Haus gebaut — aber kein einziger Erzeuger", ok is True, meldung)
        _schritt = app.naechster_schritt()
        check("jetzt nennt die Karte ausdrücklich das fehlende Holz",
              "Holz" in _schritt["text"] and "Holzfäller" in _schritt["text"],
              _schritt["text"][:200])
        check("und sagt, wo Holz wächst (Wald)", "Wald" in _schritt["text"],
              _schritt["text"][:200])
        check("der Knopf führt in die Siedlungskarte", "öffnen" in _schritt["knopf"],
              _schritt["knopf"])
        app._render()
        check("die Warnung steht auch in der Kopfzeile (⚠ statt einer irreführenden 0)",
              "⚠" in app.res_labels_top["holz"].cget("text"),
              app.res_labels_top["holz"].cget("text"))

        _wald = [i for i, a in enumerate(_raster) if a == "wald"]
        if _wald:
            ok, meldung = main.bauen_auf_karte(_sied, "holzfaeller", _wald[0])
            check("Holzfäller auf Wald gebaut", ok is True, meldung)
            _schritt = app.naechster_schritt()
            check("mit Holzquelle verschwindet die Holz-Warnung aus der Karte",
                  "kein Holz da" not in _schritt["text"], _schritt["text"][:200])
            app._render()
            check("und aus der Kopfzeile", "⚠" not in app.res_labels_top["holz"].cget("text"),
                  app.res_labels_top["holz"].cget("text"))

    # ---------------------------------------------------------------- 3 Karte oeffnen
    abschnitt("3. Karte oeffnen und Felder sehen")
    geoeffnet, _ = _drueck(app, "Karte öffnen")
    check("der Knopf 'Karte öffnen' funktioniert", geoeffnet)
    check("die Siedlungskarte ist die aktuelle Ansicht", app.current_view == "Siedlungskarte",
          app.current_view)
    siedlung = st.settlements[-1]
    # Die Karte ist jetzt eine Zeichenfläche (astra-Gutachten: 64-px-Felder mit Emblem).
    # Geprüft wird, dass jedes Feld als anklickbares Objekt (tag 'feld:i') vorhanden ist.
    canvas = getattr(app, "karten_canvas", None)
    check("die Karte ist eine Zeichenfläche", canvas is not None)
    if canvas is not None:
        felder_da = [i for i in range(len(siedlung.karte["raster"]))
                     if canvas.find_withtag(f"feld:{i}")]
        check("jedes Feld ist auf der Karte gezeichnet und anklickbar",
              len(felder_da) == len(siedlung.karte["raster"]),
              f"{len(felder_da)} von {len(siedlung.karte['raster'])}")
        # Feld A1 mit einem ECHTEN Klick wählen und den Auswahlrahmen prüfen.
        canvas.event_generate("<Button-1>", x=18 + 32, y=18 + 32)   # Feld A1 (Leiste 18 px)
        tick()
        check("der Klick auf ein Feld wählt genau dieses Feld", app.karten_feld == 0,
              str(getattr(app, "karten_feld", None)))
        # Nach dem Klick wird die Ansicht neu gezeichnet — die Zeichenfläche ist dann ein
        # NEUES Objekt. Deshalb frisch holen (sonst greift die Prüfung auf ein zerstörtes zu).
        frisch = app.karten_canvas
        # astra „Siedlung 3" (05.10.2026): statt des alten Cyanrahmens der goldene Auswahlrahmen
        # 3 px nach innen — dunkle Unterkontur #172128 mit 5 px, darueber #E4C77D mit 2 px und
        # vier 8-px-Eckwinkel. Die Farben kommen aus dem Modul, nicht aus dem Test.
        _auswahl = frisch.find_withtag("auswahl")
        check("das gewählte Feld bekommt den goldenen Auswahlrahmen (astra Siedlung 3)",
              len(_auswahl) == 6
              and any(frisch.itemcget(o, "outline") == karten_optik_fein.AUSWAHL_GOLD
                      for o in _auswahl if frisch.type(o) == "rectangle")
              and any(frisch.itemcget(o, "outline") == karten_optik_fein.AUSWAHL_UNTER_FARBE
                      for o in _auswahl if frisch.type(o) == "rectangle"),
              f"{len(_auswahl)} Objekte: "
              f"{[frisch.itemcget(o, 'outline') for o in _auswahl if frisch.type(o) == 'rectangle']}")
    else:
        befund("keine Zeichenfläche gefunden — Kartendarstellung nicht geprueft")

    # ---------------------------------------------------------------- 4 Bebauen
    abschnitt("4. Ein Feld bebauen — über echte Klicks auf die Zeichenfläche")
    gebaut = None
    klick_ok = False
    ZELLE, RAND = 64, int(karten_optik_fein.KOORDINATEN_BREITE)   # Leiste 18 px (astra)
    for i in range(len(siedlung.karte["raster"])):
        if str(i) in siedlung.bauten:
            continue
        # Echter Klick auf das Feld in der Zeichenfläche (geht über tag_bind wie ein Mausklick).
        cx = RAND + (i % int(siedlung.karte.get("spalten") or 8)) * ZELLE + ZELLE // 2
        cy = RAND + (i // int(siedlung.karte.get("spalten") or 8)) * ZELLE + ZELLE // 2
        canvas = getattr(app, "karten_canvas", None)
        if canvas is None:
            break
        canvas.event_generate("<Button-1>", x=cx, y=cy)
        tick()
        if getattr(app, "karten_feld", None) == i:
            klick_ok = True
        for wahl in _knoepfe(app.content, ""):
            beschriftung = str(wahl.cget("text"))
            if any(n in beschriftung for n in ("Holzfäller", "Steinmetz", "Jäger", "Farm",
                                              "Erzmine", "Goldmine", "Schafszucht")):
                vorher = {k: st.resources[k].amount for k in st.resources}
                wahl.invoke()
                tick()
                nachher = {k: st.resources[k].amount for k in st.resources}
                gebaut = {"feld": i, "gebaeude": beschriftung.split("\n")[0],
                          "art": siedlung.karte["raster"][i],
                          "bezahlt": {k: round(vorher[k] - nachher[k], 1) for k in vorher
                                      if vorher[k] != nachher[k]}}
                break
        if gebaut:
            break
    # Nach einem erfolgreichen Bau löscht das Spiel die Auswahl (karten_feld = None) — die
    # Prüfung merkt sich deshalb, ob ein Klick getroffen hat, statt am Ende zu messen.
    check("der Klick auf ein Feld wählt genau dieses Feld", klick_ok)
    check("auf einem Feld liess sich ein Rohstoffbetrieb bauen", bool(gebaut), str(gebaut))
    if gebaut:
        check("das Gebaeude steht auf dem Feld",
              siedlung.bauten.get(str(gebaut["feld"])) is not None, str(siedlung.bauten))
        check("die Kosten wurden abgezogen", bool(gebaut["bezahlt"]), str(gebaut["bezahlt"]))
        canvas = getattr(app, "karten_canvas", None)
        if canvas is not None:
            texte_auf_feld = [canvas.itemcget(o, "text")
                              for o in canvas.find_withtag(f"feld:{gebaut['feld']}")
                              if canvas.type(o) == "text"]
            # astra (05.10.2026, „Siedlung 1" und „Siedlung 3"): Name, Ertrag UND Stufenstempel
            # gehoeren NICHT auf die 64-px-Felder — dort steht nur der Baukörper. Namen, Stufe und
            # Ertrag nennt die Zeile unter der Karte (naechste Pruefung).
            check("das Feld traegt nur das Gebaeudezeichen und KEINEN Text mehr",
                  bool(canvas.find_withtag(f"feld:{gebaut['feld']}")) and not texte_auf_feld,
                  f"Texte auf dem Feld: {texte_auf_feld}")
            check("das Feld bleibt nach dem Bau ausgewaehlt", app.karten_feld == gebaut["feld"],
                  str(app.karten_feld))
            panel = " ".join(_texte(app.content))
            check("unter der Karte stehen Name, Stufe und Ertrag des Gebaeudes",
                  gebaut["gebaeude"] in panel and "Stufe" in panel,
                  " | ".join(z for z in _texte(app.content) if "Hier steht" in z)[:200] or panel[:160])
        else:
            befund("keine Zeichenfläche — Gebaeude auf dem Feld nicht nachpruefbar")

    # ---------------------------------------------------------------- 5 Ertrag
    abschnitt("5. Eine Stunde Spielzeit: der Betrieb muss liefern")
    ertrag = st.stundenertrag()
    check("die bebauten Felder liefern ueberhaupt Ertrag", any(v > 0 for v in ertrag.values()),
          str({k: round(v, 2) for k, v in ertrag.items() if v}))
    vorher = {k: st.resources[k].amount for k in st.resources}
    st.tick(3600.0)
    nachher = {k: st.resources[k].amount for k in st.resources}
    zuwachs = {k: round(nachher[k] - vorher[k], 2) for k in vorher if nachher[k] != vorher[k]}
    check("nach einer Stunde ist etwas DAZUKOMMEN", any(v > 0 for v in zuwachs.values()), str(zuwachs))
    check("durch den Ertrag ALLEIN geht nichts verloren", all(v > 0 for v in zuwachs.values()), str(zuwachs))

    # ---------------------------------------------------------------- 6 Noobschutz
    abschnitt("6. Noobschutz (Tag 1-3): kein Bot darf die Startwerte pluendern")
    check("der Noobschutz ist am ersten Tag aktiv", st.noob_protection)
    # Bot-Zuege erzwungen wiederholen: ob ein Bot angreift, entscheidet der Zufall
    # (`botkern`), deshalb wird hier ueber mehrere Zuege gemessen statt auf einen zu hoffen.
    angriff_gesehen = False
    gestohlen = {}
    for i in range(25):
        st._letzter_bot_takt = 0.0            # Bot-Zug erzwingen
        # Die Zeit MITFUEHREN: `botkern` laesst einen Bot nur alle 6-24 h ziehen, sonst
        # liefe die Schleife leer und der Schutzweg waere nie ausgeloest.
        jetzt = time.time() + i * 3600.0
        vorher = {k: st.resources[k].amount for k in st.resources}
        st.bots_fortschreiben(jetzt)
        nachher = {k: st.resources[k].amount for k in st.resources}
        for k in vorher:
            if nachher[k] < vorher[k]:
                gestohlen[k] = round(gestohlen.get(k, 0.0) + vorher[k] - nachher[k], 2)
        if any("Noobschutz" in str(m.get("text")) for m in st.messages):
            angriff_gesehen = True
    check("kein Rohstoff wird waehrend des Noobschutzes gestohlen (25 Bot-Zuege)",
          not gestohlen, str(gestohlen))
    if angriff_gesehen:
        check("ein abgewehrter Angriff steht mit Begruendung in den Nachrichten",
              any("Noobschutz" in str(m.get("text")) for m in st.messages),
              str([m.get("text") for m in st.messages][-1:]))
    else:
        befund("in 25 erzwungenen Bot-Zuegen kam kein Angriff vor — der Schutzweg wurde "
               "in diesem Lauf nicht ausgeloest (nichts gestohlen, aber auch nichts belegt)")

    # ---------------------------------------------------------------- 7 Ausbildung
    abschnitt("7. Ausbildung: Gebaeude bauen, dann den Knopf druecken")
    # Genug Mittel, damit dieser Schritt die Ausbildung prueft und nicht die Wirtschaft.
    for k in ("holz", "stein", "nahrung", "leder", "wolle", "gold"):
        if k in st.resources:
            st.resources[k].amount = 5000
    st.population = 100.0
    akademie_gebaut = False
    for i in range(len(siedlung.karte["raster"])):
        if str(i) in siedlung.bauten:
            continue
        app._karten_feld_waehlen(i)
        tick()
        ok, beschriftung = _drueck(app, "Kriegerakademie")
        if ok:
            akademie_gebaut = True
            break
    if not akademie_gebaut:
        befund("Kriegerakademie liess sich auf dieser Karte nicht setzen (Standortregel) — "
               "Ausbildung konnte nicht geprueft werden")
    else:
        app._switch_view("Kaserne")
        tick()
        ks = _knoepfe(app.root, "Ausbilden")
        check("mit der Kriegerakademie steht ein 'Ausbilden'-Knopf bereit", bool(ks),
              f"{len(ks)} Knoepfe")
        if ks:
            # Die guenstigste bezahlbare Einheit nehmen (Kampfeinheiten kosten Gold).
            vorher = sum(u.count for u in st.units.values())
            ks[0].invoke()
            tick()
            nachher = sum(u.count for u in st.units.values())
            check("ein Knopfdruck bildet GENAU eine Einheit aus", nachher == vorher + 1,
                  f"{vorher} -> {nachher} | Status: {app.lbl_status.cget('text')[:80]}")
            check("die neue Einheit ist im Fenster zu sehen",
                  any("Anzahl: 1" in z for z in _texte(app.root)),
                  " | ".join(z for z in _texte(app.root) if "Anzahl" in z)[:200])

    # ---------------------------------------------------------------- 8 Forschung
    abschnitt("8. Forschung: Bibliothek bauen, dann forschen")
    # Wichtig: erst wieder auf die Karte wechseln — `_karten_feld_waehlen` zeichnet die
    # AKTUELLE Ansicht neu, und die war nach dem Kaserne-Schritt nicht mehr die Karte.
    app._oeffne_siedlungskarte(siedlung)
    tick()
    biblio = False
    for i in range(len(siedlung.karte["raster"])):
        if str(i) in siedlung.bauten:
            continue
        app._karten_feld_waehlen(i)
        tick()
        ok, _ = _drueck(app, "Bibliothek")
        if ok:
            biblio = True
            break
    if not biblio:
        befund("Bibliothek liess sich auf dieser Karte nicht setzen (nur Grasland/Steppe/Nebelsee) "
               "— Forschung konnte nicht geprueft werden")
    else:
        app._switch_view("Forschung")
        tick()
        ks = _knoepfe(app.root, "Forschen")
        check("mit der Bibliothek steht ein 'Forschen'-Knopf bereit", bool(ks), f"{len(ks)} Knoepfe")
        if ks:
            key = next((k for k, r in st.research.items() if r.level < r.max_level), None)
            vorher = st.research[key].level if key else None
            ks[0].invoke()
            tick()
            auftrag = st.forschungsauftraege.get(key) or {}
            check("die Forschung LAEUFT (Auftrag gesetzt) statt sofort zu steigen", bool(auftrag),
                  str(auftrag)[:120])
            check("die Stufe steigt NICHT im selben Klick",
                  key is None or st.research[key].level == vorher,
                  f"{vorher} -> {st.research[key].level if key else '?'}")

    abschnitt("9. Keine stillen Rueckruf-Fehler im ganzen Durchspiel")
    check("kein stiller Tkinter-Fehler", not _still, " | ".join(_still))

    root.destroy()
    return bericht()


if __name__ == "__main__":
    sys.exit(main_())
