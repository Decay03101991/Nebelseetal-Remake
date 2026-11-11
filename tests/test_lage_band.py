# -*- coding: ascii -*-
"""T7: das Lage-Band im Dorfzentrum - Forschung, Goetterschutz, Wallbau sichtbar (11.11.2026).

Daniels Befunde aus dem Spieltest (Register 421 bis 424):
  * B07 Forschung: "total unscheinbar und klein, obwohl es ABSOLUT WICHTIG ist im Spielablauf".
  * B11 Goetterschutz: "Nein, nicht auffaellig genug, falls es irgendwo sein sollte".
  * B11 Wallbau: "noch viel zu unscheinbar designed".

Neu steht unter dem Titel des Dorfzentrums eine eigene Zeile mit drei Feldern. Gerechnet wird dort
NICHTS: Forschung aus `ort.forschungsauftrag`, Schutz aus `state.noob_protection` und der Tageslaenge,
Wall aus `wall_stufe_am_ort` - dieselben Stellen wie bisher.

Was diese Datei beweist
-----------------------
1. Es sind immer GENAU drei Felder in fester Reihenfolge (Forschung, Goetterschutz, Wallbau).
2. Jeder Zustand hat seinen eigenen Text: kein Auftrag / Auftrag mit Restzeit, Schutz an / aus,
   Mauer da / keine Mauer.
3. Das Dorfzentrum baut das Band wirklich ein (Quelltext-Wache).
4. Die Ansicht rendert ohne Ausnahme (echte Tk-Flaeche).

Aufruf:  python -X utf8 tests/test_lage_band.py
"""
from __future__ import annotations

import inspect
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

ROOT, SRC = import_src()
import main  # noqa: E402


def _app():
    """Eine echte App ohne Fenster (wie die anderen Oberflaechen-Wachen)."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    app = main.NebelseetalApp(root)
    app._build_main_ui()
    app._erste_siedlung_gruenden()
    return root, app


root, app = _app()
try:
    abschnitt("1. Drei Felder, feste Reihenfolge")
    zeilen = app.lage_band_texte()
    check("1 es sind genau drei Felder", len(zeilen) == 3, str(len(zeilen)))
    # 11.11.2026: Daniel hat in V_0.0.4 gesehen, dass die Ueberschrift "Goetterschutz" hiess.
    # Das ist die Anzeige, nicht der Bezeichner - hier gilt seine Regel: ingame echte Umlaute.
    # Die Wache haelt jetzt den Umlaut fest, damit die Ersatzschreibweise nicht zurueckkommt.
    check("1 Reihenfolge: Forschung, G\u00f6tterschutz, Wallbau",
          [z[0] for z in zeilen] == ["Forschung", "G\u00f6tterschutz", "Wallbau"], str([z[0] for z in zeilen]))
    check("1 jedes Feld hat einen Text", all(str(z[1] or "").strip() for z in zeilen), str(zeilen))

    abschnitt("2. Jeder Zustand hat seinen eigenen Text")
    ort = app.state.aktive_siedlung()
    if ort is not None:
        ort.forschungsauftrag = None
        check("2 ohne Auftrag sagt die Forschung das deutlich",
              "keine" in app.lage_band_texte()[0][1].lower(), app.lage_band_texte()[0][1])
        ort.forschungsauftrag = {"gebiet": "Wagenbau", "zielstufe": 1, "dauer_stunden": 1.0,
                                 "startzeit": float(app.state.spielsekunden)}
        text = app.lage_band_texte()[0][1]
        check("2 ein laufender Auftrag nennt Gebiet und Stufe", "Wagenbau" in text and "1" in text, text)
        check("2 er nennt die Restzeit in Stunden und Minuten", "noch " in text and ":" in text, text)

    app.state.noob_protection = True
    app.state.day = 1
    an = app.lage_band_texte()[1][1]
    app.state.noob_protection = False
    aus = app.lage_band_texte()[1][1]
    check("2 der Goetterschutz nennt die verbleibenden Tage", "noch" in an.lower() and "Tag" in an, an)
    check("2 ein beendeter Schutz steht als beendet da", "beendet" in aus.lower(), aus)

    _wall0 = app.lage_band_texte()[2][1]
    check("2 ohne Mauer sagt der Wallbau, wo man baut", "keine" in _wall0.lower() or "noch" in _wall0.lower(),
          _wall0)

    abschnitt("3. Das Dorfzentrum baut das Band ein")
    _ov = inspect.getsource(main.NebelseetalApp._render_overview)
    check("3 der Aufbau des Bandes steht im Dorfzentrum", "self._lage_band()" in _ov, "")
    check("3 das Band rechnet nicht selbst, es liest `lage_band_texte`",
          "lage_band_texte" in inspect.getsource(main.NebelseetalApp._lage_band), "")

    abschnitt("4. Die Ansicht rendert wirklich")
    app._switch_view("Dorfzentrum")
    app.content.update_idletasks()
    kinder = list(app.content.winfo_children())
    rahmen = [k for k in kinder if type(k).__name__ == "Frame"
              and any("FORSCHUNG" == str(t.cget("text")) for t in k.winfo_children()
                      if type(t).__name__ == "Frame"
                      for t in t.winfo_children() if type(t).__name__ == "Label")]
    check("4 im Dorfzentrum steht ein Rahmen mit dem Feld FORSCHUNG", bool(rahmen), str(len(kinder)))
finally:
    root.destroy()

sys.exit(bericht())
