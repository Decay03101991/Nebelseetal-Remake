"""Macht stille Tkinter-Rueckruf-Fehler laut.

Warum es diese Pruefung gibt
---------------------------
Ein Rueckruf (Button-`command`, `after`-Timer, Bindung) laeuft in Tkinter ueber
`tkinter.CallWrapper`. Wirft er eine Ausnahme, faengt der Wrapper sie ab und ruft
`root.report_callback_exception(...)` — die Standardfassung druckt den Traceback
nur nach stderr und laesst das Spiel WEITERLAUFEN. Das Fenster bleibt oben, das
Spiel tut still das Falsche, und keine einzige Pruefung merkt es.

Diese Pruefung ersetzt `root.report_callback_exception` durch einen Sammler, der
jede solche Ausnahme (Art, Widget, Traceback) festhaelt, besucht ALLE Ansichten
und faehrt die Kernaktionen ueber die Methoden der App selbst (nicht per Pixelklick).
Jeder gefangene Rueckruf-Fehler ist ein FEHLER. Eine absichtlich kaputte
Schaltflaeche beweist, dass die Falle wirklich greift.

Aufruf:  python -X utf8 tests/test_gui_fehler.py
"""
from __future__ import annotations

import os
import sys
import traceback
import tempfile
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, bericht, befund, check, import_src

ROOT, SRC = import_src()
os.chdir(SRC)

main = ausnahme("main importieren", lambda: __import__("main"))
if main is None:
    sys.exit(bericht())

import random
import tkinter as tk
import gelaende as G
import einheiten      # data/units.json: die Forschungs- und Waren-Voraussetzung je Einheit

# Marke, an der die absichtliche Fehlerzeile spaeter wieder erkannt und aus der
# gezaehlten Liste entfernt wird (Punkt 5 der Aufgabe).
FALEN_MARKE = "ABSICHTLICHER-FALEN-FEHLER"

ANZAHL_ERWARTET = 18          # 17 MENU_ITEMS + "Spielerprofile"


class RueckrufSammler:
    """Faengt Tkinter-Rueckruf-Fehler, statt sie nur zu drucken.

    Tk ruft diesen Sammler ueber `widget._report_exception()` ->
    `root.report_callback_exception(exc, val, tb)` auf. Er wirft NICHT weiter,
    damit Tk seinen Ereignislauf wie gewohnt fortsetzt.
    """

    def __init__(self):
        self.fehler = []      # Liste von dicts: art, wert, widget, spuren

    def sammeln(self, exc, wert, spuren):
        eintrag = {
            "art": getattr(exc, "__name__", str(exc)),
            "wert": str(wert),
            "widget": self._widget_aus(spuren),
            "spuren": "".join(traceback.format_exception(exc, wert, spuren)).strip(),
        }
        self.fehler.append(eintrag)
        # Sofortsichtbar, damit ein Mensch es live sieht — zusaetzlich zum Sammeln.
        print(f"  STILLER RUECKRUF-FEHLER [{eintrag['art']}] auf {eintrag['widget']}: "
              f"{eintrag['wert']}")

    @staticmethod
    def _widget_aus(spuren):
        """Das ausloesende Widget aus dem Traceback holen.

        Der CallWrapper haelt das Widget in `self.widget`; sein Rahmen liegt im
        Traceback. So bekommen wir den Namen, ohne Tk zu veraendern.
        """
        while spuren is not None:
            obj = spuren.tb_frame.f_locals.get("self")
            if isinstance(obj, tk.CallWrapper):
                w = getattr(obj, "widget", None)
                if w is not None:
                    try:
                        return f"{w.winfo_class()} {w.winfo_name()}"
                    except Exception:
                        return type(w).__name__
            spuren = spuren.tb_next
        return "unbekannt"

    def texte(self):
        return [f"[{e['art']}] {e['widget']}: {e['wert']}" for e in self.fehler]


befund_direkt = []      # direkte Ausnahmen beim Ansichtswechsel (nicht als Rueckruf)


def pruefen():
    global root, app
    abschnitt("1. Aufbau ohne Fenster und Sammler einhaengen")

    root = ausnahme("Fenster anlegen", tk.Tk)
    if root is None:
        return
    root.withdraw()
    app = ausnahme("App aufbauen", lambda: main.NebelseetalApp(root))
    if app is None:
        return
    ausnahme("Hauptoberflaeche aufbauen", app._build_main_ui)

    sammler = RueckrufSammler()
    root.report_callback_exception = sammler.sammeln

    check("der Sammler ist als Rueckruf-Faenger eingetragen (nicht Tks Standarddruck)",
          getattr(root.report_callback_exception, "__self__", None) is sammler)
    check("die Oberflaeche steht (Statuszeile vorhanden)",
          hasattr(app, "lbl_status") and app.lbl_status.winfo_exists())

    def tick():
        root.update_idletasks()
        root.update()

    # ------------------------------------------------------------------ 2 Ansichten
    abschnitt("2. Jede Ansicht besuchen (MENU_ITEMS + Spielerprofile)")
    views = list(main.MENU_ITEMS) + ["Spielerprofile"]
    direkte = []
    for v in views:
        try:
            app._switch_view(v)
            tick()
        except Exception:
            direkte.append((v, traceback.format_exc()))
            befund_direkt.append(v)

    check(f"genau {ANZAHL_ERWARTET} Ansichten werden besucht",
          len(views) == ANZAHL_ERWARTET, f"{len(views)}: {views}")
    check("keine Ansicht wirft beim Aufbau direkt eine Ausnahme",
          not direkte, "; ".join(v for v, _ in direkte))
    for v, tb in direkte:
        print(f"  DIREKTE AUSNAHME in Ansicht {v!r}:\n{tb}")

    check("kein stiller Rueckruf-Fehler beim Durchlauf aller Ansichten",
          not sammler.fehler,
          " | ".join(sammler.texte()))

    # ------------------------------------------------------------------ 3 Aktionen
    abschnitt("3. Kernaktionen ueber die App-Methoden fahren")
    aktionen = 0

    # Reicher Zustand wie in tests/test_baseline.py: genug Rohstoffe und Siedler.
    for k in app.state.resources:
        app.state.resources[k].amount = 100000
    app.state.population = 5000.0

    # Deterministische Karte, damit die Siedlungsgruendung nicht flackert.
    random.seed(20261005)
    app.state.generate_map(app.state.current_map)

    try:
        vorher_siedlungen = len(app.state.settlements)
        app._found_settlement()
        tick()
        aktionen += 1
        check("Siedlung gruenden legt genau eine Siedlung an",
              len(app.state.settlements) == vorher_siedlungen + 1,
              f"{vorher_siedlungen} -> {len(app.state.settlements)}")
        siedlung = app.state.settlements[-1]

        def freies_feld(key):
            for i, art in enumerate(siedlung.karte["raster"]):
                if str(i) in siedlung.bauten:
                    continue
                ok, _ = G.bau_moeglich(key, art)
                if ok:
                    return i
            return None

        # Eine Karte finden, die Platz fuer alle benoetigten Gebaeude bietet.
        benoetigt = ["haus", "verteidigungswall", "bibliothek", "kriegerakademie"]
        for _ in range(80):
            if all(freies_feld(k) is not None for k in benoetigt):
                break
            siedlung.karte = main.neue_siedlungskarte([])
            siedlung.bauten.clear()
            siedlung.stufen.clear()

        # Siedlungskarte oeffnen
        app._oeffne_siedlungskarte(siedlung)
        tick()
        aktionen += 1
        check("Siedlungskarte oeffnen zeigt die Ansicht 'Siedlungskarte'",
              app.current_view == "Siedlungskarte", app.current_view)

        # Bauen: auf ein Feld setzen schreibt settlement.bauten
        f_haus = freies_feld("haus")
        app._karten_feld_waehlen(f_haus)
        app._karten_bauen("haus")
        tick()
        aktionen += 1
        check("Bauen auf einem Feld schreibt settlement.bauten",
              siedlung.bauten.get(str(f_haus)) == "haus", str(siedlung.bauten))

        # Der Wall ist seit GPT-W02 KEIN Feldgebäude. Teste den Gebaeudeausbau
        # deshalb an einer Bibliothek; die Wall-Logik hat eigene Regressionen.
        f_bib = freies_feld("bibliothek")
        app._karten_feld_waehlen(f_bib)
        app._karten_bauen("bibliothek")
        tick()
        app._karten_feld_waehlen(f_bib)
        app._karten_ausbauen()
        tick()
        aktionen += 1
        check("Ausbauen hebt die Stufe eines ausbaubaren Feldgebaeudes",
              siedlung.stufen.get(str(f_bib)) == 2,
              f"Feld {f_bib}: Stufe {siedlung.stufen.get(str(f_bib))}")

        # Abrissbestaetigung ist in einer automatischen GUI-Pruefung keine
        # Gelegenheit fuer einen menschlichen Mausklick: das positive Ergebnis
        # wird eng fuer diesen einen Dialog simuliert. Der echte Button existiert.
        app._karten_feld_waehlen(f_haus)
        with patch("tkinter.messagebox.askyesno", return_value=True):
            app._karten_abreissen()
        tick()
        aktionen += 1
        check("Abreissen entfernt das Gebaeude vom Feld",
              str(f_haus) not in siedlung.bauten, str(siedlung.bauten))

        # Die Bibliothek steht bereits: erst Baukunst regulär erforschen, damit
        # nachher die Akademie gebaut werden darf. Keine Forschungsfreischaltung
        # durch stilles Direktsetzen einer Stufe.
        aktionen += 1
        forsch_key = "Baukunst"
        stufe_vorher = app.state.research[forsch_key].level
        app._start_research(forsch_key)
        tick()
        aktionen += 1
        # W4c: Die Forschung LAEUFT jetzt (Wartezeit) — die Stufe steigt erst nach Ablauf der Zeit.
        # Teil 6 (Rest): der Auftrag steht im AKTIVEN ORT, und die Spieluhr bucht den Abschluss.
        startet_ohne_stufe = app.state.research[forsch_key].level == stufe_vorher
        _ort_f = app.state.aktive_siedlung()
        _auftrag = getattr(_ort_f, "forschungsauftrag", None) or {}
        app.state.spielsekunden = (float(_auftrag.get("startzeit") or 0)
                                   + float(_auftrag.get("dauer_stunden") or 0) * 3600.0 + 1.0)
        app.state.tick(0.0)
        tick()
        check("Forschung laeuft mit Wartezeit und steigt erst nach Ablauf",
              startet_ohne_stufe
              and app.state.research[forsch_key].level == stufe_vorher + 1
              and getattr(_ort_f, "forschungsauftrag", None) is None,
              f"{forsch_key}: {stufe_vorher} -> {app.state.research[forsch_key].level}, "
              f"Auftrag {getattr(_ort_f, 'forschungsauftrag', None)}")

        # Ausbildung: Kriegerakademie bauen, dann eine Einheit ausbilden.
        # Vorgabe Daniel 05.10.2026: Forschung UND Ausruestung sind Bedingungen. Teil 6c: Rohstoffe,
        # Siedler und Ausruestung liegen VOR ORT (`Settlement.vorraete/bevoelkerung/waren`) — und die
        # Einheit entsteht erst AM ENDE der Ausbildungszeit im Ortslager, gebucht von `ort_tick`.
        f_aka = freies_feld("kriegerakademie")
        app._karten_feld_waehlen(f_aka)
        app._karten_bauen("kriegerakademie")
        tick()
        aktionen += 1
        einheit_key = "Bürgerwehr"  # ohne weitere Forschung oder Werkstattwaren ausbildbar
        _roh = einheiten.alle().get(einheit_key) or {}
        _vor = (_roh.get("voraussetzung") or {}).get("forschung")
        if _vor:
            app.state.research[_vor].level = int(_roh["voraussetzung"]["stufe"])
        _ort_g = app.state.aktive_siedlung()
        for _stoff in app.state.resources:                      # die belegten Kosten vor Ort
            _ort_g.vorraete[_stoff] = max(float(_ort_g.vorraete.get(_stoff, 0.0)), 5000.0)
        _ort_g.bevoelkerung = max(float(_ort_g.bevoelkerung), 20.0)
        for _ware in (_roh.get("waren") or []):
            _ort_g.waren[_ware] = 1
        anzahl_vorher = int((_ort_g.einheiten or {}).get(einheit_key, 0))
        app._train_unit(einheit_key)
        tick()
        aktionen += 1
        check("die Ausbildung steht als Auftrag VOR ORT",
              any(a.get("einheit") == einheit_key for a in (_ort_g.ausbildung or [])),
              str(_ort_g.ausbildung))
        # Die Spieluhr vorstellen: danach bucht `ort_tick` die Einheit ins Ortslager (genau einmal).
        app.state.spielsekunden = float((_ort_g.ausbildung or [{}])[-1].get("ende", 0.0)) + 1.0
        app.state.tick(0.0)
        tick()
        check("Ausbildung erhoeht die Anzahl der Einheit IM ORTSLAGER",
              int((_ort_g.einheiten or {}).get(einheit_key, 0)) == anzahl_vorher + 1,
              f"{einheit_key}: {anzahl_vorher} -> {(_ort_g.einheiten or {}).get(einheit_key)}")

        # Und die Sperre wirkt: ohne die Ausruestung gibt es keine zweite Einheit.
        for _ware in (_roh.get("waren") or []):
            _ort_g.waren[_ware] = 0
        if _roh.get("waren"):
            _vorher = int((_ort_g.einheiten or {}).get(einheit_key, 0))
            app._train_unit(einheit_key)
            tick()
            check("ohne Ausruestung wird KEINE weitere Einheit ausgebildet",
                  int((_ort_g.einheiten or {}).get(einheit_key, 0)) == _vorher,
                  f"{einheit_key}: {_vorher} -> {(_ort_g.einheiten or {}).get(einheit_key)}")

        # Moderne Version: drei Spielerslots oeffnen Dialoge; der alte
        # .save()/.load()-UI-Test an savegame.json wuerde im Hintergrund haengen.
        # Der Dateitest nutzt deshalb einen EINZIGEN isolierten temporären Pfad.
        # Slot-Dialoge haben eigene Tests; es wird hier kein Privat-Save beruehrt.
        _pruef_save = os.path.join(tempfile.gettempdir(),
                                  f"nebelseetal_gui_fehlertest_{os.getpid()}.json")
        check("Speichern schreibt in einen isolierten Testpfad",
              app.state.save(_pruef_save) and os.path.exists(_pruef_save), _pruef_save)
        aktionen += 1
        _zweitzustand = main.GameState()
        check("Laden der erzeugten Datei meldet Erfolg",
              _zweitzustand.load(_pruef_save) is True)
        for _ende in ("", ".bak", ".tmp"):
            try:
                os.remove(_pruef_save + _ende)
            except FileNotFoundError:
                pass
        aktionen += 1

        # Neu zeichnen
        ausnahme("app._render()", app._render)
        tick()
        aktionen += 1
        check("erzwungenes Neuzeichnen app._render() laeuft ohne direkte Ausnahme",
              True)

        # Der echte periodische Rueckruf, den das Spiel per after() startet.
        root.after(0, app._tick_loop)
        tick()
        aktionen += 1
        check("der echte after-Rueckruf _tick_loop laeuft ohne stillen Fehler",
              not sammler.fehler, " | ".join(sammler.texte()))

        check("kein einziger stiller Rueckruf-Fehler bei den Aktionen",
              not sammler.fehler, " | ".join(sammler.texte()))
    except Exception:
        ausnahme("Aktionsblock", lambda: (_ for _ in ()).throw(sys.exc_info()[1]))

    # ------------------------------------------------------------------ 4 Falle
    abschnitt("4. Falle: faengt der Sammler wirklich einen kaputten Rueckruf?")
    vorher = len(sammler.fehler)

    def falle():
        raise RuntimeError(FALEN_MARKE)

    falle_knopf = tk.Button(root, text="Falle", command=falle)
    falle_knopf.pack()
    tick()
    falle_knopf.invoke()      # geht durch Tks CallWrapper -> unser Sammler
    tick()
    neu = sammler.fehler[vorher:]

    check("der Sammler faengt den absichtlichen Rueckruf-Fehler",
          len(neu) >= 1, str([e["wert"] for e in neu]))
    check("die Falle meldet genau den erwarteten Fehlertext",
          len(neu) == 1 and FALEN_MARKE in neu[0]["wert"],
          str([e["wert"] for e in neu]))
    check("der Sammler nennt Fehlerart und Widget",
          bool(neu) and neu[0]["art"] == "RuntimeError"
          and neu[0]["widget"] != "unbekannt",
          str(neu[0]) if neu else "nichts gefangen")
    if neu:
        befund("Fallen-Pruefung bestanden: der Sammler greift",
               f"[{neu[0]['art']}] auf {neu[0]['widget']}: {neu[0]['wert']}")

    # Die kuenstliche Fehlerzeile wieder aus der gezaehlten Liste entfernen —
    # sie darf die echten Befunde nicht verfaelschen.
    sammler.fehler = [e for e in sammler.fehler if FALEN_MARKE not in e["wert"]]
    try:
        falle_knopf.destroy()
    except Exception:
        pass
    tick()

    # ------------------------------------------------------------------ 5 Auswertung
    abschnitt("5. Auswertung — echte Rueckruf-Fehler verbatim melden")
    echte = list(sammler.fehler)
    check("kein echter stiller Rueckruf-Fehler im gesamten Durchlauf",
          not echte, f"{len(echte)} Stueck")
    for e in echte:
        print(f"  ROTER BEFUND [{e['art']}] auf {e['widget']}: {e['wert']}")
        print(e["spuren"])
        befund(f"stiller Rueckruf-Fehler [{e['art']}] auf {e['widget']}", e["wert"])

    check("keine Ansicht mit direkter Ausnahme",
          not direkte, str(direkte))

    print(f"\nDURCHLAUF: {len(views)} Ansichten und {aktionen} Aktionen ohne Fenster "
          f"geprueft — {len(echte)} echte Rueckruf-Fehler.")


# ---------------------------------------------------------------------- Lauf
save_pfad = None
save_war_da = False


def aufraeumen():
    try:
        root.destroy()
    except Exception:
        pass
    # Nur wegraeumen, was wir selbst erzeugt haben (savegame.json ist gitignored).
    if save_pfad and not save_war_da:
        for p in (save_pfad, save_pfad + ".bak", save_pfad + ".tmp"):
            try:
                if os.path.exists(p):
                    os.remove(p)
            except Exception:
                pass


try:
    # savegame.json vor dem Lauf merken, damit nichts Fremdes geloescht wird.
    _pfad = os.path.join(SRC, "savegame.json")
    save_war_da = os.path.exists(_pfad)
    pruefen()
finally:
    try:
        save_pfad = getattr(app, "save_path", _pfad) if "app" in dir() else _pfad
    except Exception:
        save_pfad = _pfad
    aufraeumen()

sys.exit(bericht())
