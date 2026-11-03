# -*- coding: ascii -*-
"""Wache A: Doppel-Puffer im Ansichtswechsel (03.11.2026, Daniels Wunsch nach Fluessigkeit).

DAS PROBLEM, GEMESSEN
---------------------
`_render_view` machte den Inhaltsbereich bei JEDEM Aufruf erst leer (`widget.destroy()` je Kind) und
fuellte ihn danach neu - 46 Aufrufstellen, also praktisch jeder Klick. Das Flackern und das Gefuehl
"abgehakt" kamen daher, nicht aus der Rechenzeit
(`docs/EINSCHAETZUNG_INGAME_FENSTER_20261103.md`).

WAS DIESE DATEI PRUEFT
---------------------
1. Nach einem Ansichtswechsel steht IMMER Inhalt im Bereich - nie ein leeres Fenster.
2. Es bleibt genau EIN Inhaltsrahmen im Canvas (der alte wird entfernt, keine Leiche, kein Wachstum).
3. Der Wechsel laeuft ueber einen ZWEITEN Rahmen: der Quelltext zerstoert nicht mehr am Anfang,
   sondern baut neu und tauscht.
4. Scheitert der Aufbau, bleibt der ALTE Inhalt stehen (kein weisser Bildschirm) und der Fehler
   kommt durch.
5. Die Zahl der Widgets waechst nicht mit jedem Wechsel (kein Speicherleck ueber Klicks).

Aufruf:  python -X utf8 tests/test_doppelpuffer.py
"""
from __future__ import annotations

import ast
import inspect
import os
import random
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
import tkinter as tk  # noqa: E402
import main as M  # noqa: E402

ANSICHTEN = ("Dorfzentrum", "Lager", "Kaserne", "Portal", "Forschung", "Nachrichten")


def _code(fn) -> str:
    """Quelltext einer Funktion ohne Docstring (nur echte Anweisungen)."""
    baum = ast.parse(textwrap.dedent(inspect.getsource(fn)))       # Funktion parsen
    baum.body[0].body = [k for k in baum.body[0].body              # Docstring abtrennen
                         if not (isinstance(k, ast.Expr) and isinstance(k.value, ast.Constant)
                                 and isinstance(k.value.value, str))]
    return ast.unparse(baum)


def _app(seed: int = 7):
    """Frische App mit einer Siedlung (derselbe Start wie im Spiel)."""
    random.seed(seed)                                              # Karte reproduzierbar
    root = tk.Tk()                                                 # Tk-Wurzel
    root.withdraw()                                                # kein Fenster auf dem Schirm
    app = M.NebelseetalApp(root)                                   # die App
    app._build_main_ui()                                           # Oberflaeche aufbauen
    app._erste_siedlung_gruenden()                                 # erste Siedlung, echte Startwerte
    return root, app


# ==========================================================================
abschnitt("1. Jeder Wechsel hinterlaesst Inhalt - nie ein leeres Fenster")
# ==========================================================================
root, app = _app()
try:
    leer = []                                                      # Wechsel ohne Inhalt
    for name in ANSICHTEN:                                         # jede Ansicht einmal
        app._switch_view(name)                                     # umschalten (echter Weg)
        root.update_idletasks()                                    # Oberflaeche rechnen lassen
        if not app.content.winfo_children():                       # nichts im Inhaltsbereich?
            leer.append(name)                                      # dann merken
    check("1 keine Ansicht bleibt leer", not leer, str(leer))
    for _ in range(3):                                             # mehrere Runden
        for name in ANSICHTEN:                                     # alle Ansichten
            app._switch_view(name)                                 # umschalten
            root.update_idletasks()                                # rechnen lassen
    check("1 auch nach drei Runden steht Inhalt da", bool(app.content.winfo_children()), "")
finally:
    root.destroy()

# ==========================================================================
abschnitt("2. Genau EIN Inhaltsrahmen - der alte wird entfernt, nicht gestapelt")
# ==========================================================================
root, app = _app()
try:
    for name in ANSICHTEN:                                         # mehrfach wechseln
        app._switch_view(name)                                     # umschalten
        root.update_idletasks()                                    # rechnen lassen
    rahmen = [k for k in app.content_canvas.winfo_children() if isinstance(k, tk.Frame)]
    check("2 im Canvas haengt nur EIN Inhaltsrahmen", len(rahmen) == 1, "%d Rahmen" % len(rahmen))
    check("2 dieser Rahmen ist der aktuelle Inhalt", rahmen and rahmen[0] is app.content,
          str(rahmen == [app.content]))
    fenster = [i for i in app.content_canvas.find_all()
               if app.content_canvas.type(i) == "window"]
    check("2 genau EIN Fenstereintrag im Canvas", len(fenster) == 1, str(fenster))
finally:
    root.destroy()

# ==========================================================================
abschnitt("3. Der Quelltext tauscht, statt am Anfang zu leeren")
# ==========================================================================
quelltext = inspect.getsource(M.NebelseetalApp._render_view)       # echter Quelltext
check("3 der Docstring nennt den Doppel-Puffer", "DOPPEL-PUFFER" in quelltext, "")
check("3 es wird ein ZWEITER Rahmen gebaut", "tk.Frame(self.content_canvas" in quelltext, "")
check("3 der alte Fenstereintrag wird geloescht", "self.content_canvas.delete(alt_fenster)" in quelltext, "")
check("3 am Anfang wird NICHT mehr alles zerstoert",
      "for widget in self.content.winfo_children()" not in quelltext, "")
check("3 der alte Rahmen wird erst NACH dem Aufbau abgeraeumt",
      quelltext.index("alt_inhalt.destroy()") > quelltext.index("mapping[self.current_view]()"), "")

# ==========================================================================
abschnitt("4. Scheitert der Aufbau, bleibt der alte Inhalt stehen")
# ==========================================================================
root, app = _app()
try:
    app._switch_view("Lager")                                      # einen guten Stand setzen
    root.update_idletasks()                                        # rechnen lassen
    vorher = len(app.content.winfo_children())                     # Widgets vorher
    echt = M.NebelseetalApp._render_storage                        # echte Ansicht merken

    def _kaputt(self):                                             # absichtlich kaputte Ansicht
        raise RuntimeError("Pruef-Absicht: Ansicht scheitert")

    M.NebelseetalApp._render_storage = _kaputt                     # Ansicht ersetzen
    try:                                                           # Wechsel muss scheitern
        app._switch_view("Lager")                                  # ruft die kaputte Ansicht
        fehler = ""
    except Exception as e:                                         # noqa: BLE001 - erwartet
        fehler = repr(e)
    finally:                                                       # Ansicht zurueckstellen
        M.NebelseetalApp._render_storage = echt                    # echtes Verhalten wiederherstellen
    nachher = len(app.content.winfo_children())                    # Widgets nachher
    check("4 der Fehler kommt durch (nicht verschluckt)", "Pruef-Absicht" in fehler, fehler)
    check("4 der alte Inhalt steht noch da", nachher == vorher and nachher > 0,
          "%d -> %d" % (vorher, nachher))
    check("4 der Inhaltsbereich ist nicht leer", bool(app.content.winfo_children()), "")
    app._switch_view("Lager")                                      # heilt sich beim naechsten Wechsel
    root.update_idletasks()                                        # rechnen lassen
    check("4 der naechste Wechsel baut die Ansicht wieder", bool(app.content.winfo_children()), "")
finally:
    root.destroy()

# ==========================================================================
abschnitt("5. Kein Wachstum ueber viele Wechsel")
# ==========================================================================
root, app = _app()
try:
    app._switch_view("Lager")                                      # erster Aufbau
    root.update_idletasks()                                        # rechnen lassen
    erste = len(app.content.winfo_children())                      # Widget-Zahl am Anfang
    for _ in range(5):                                             # fuenf Runden
        app._switch_view("Lager")                                  # dieselbe Ansicht neu zeichnen
        root.update_idletasks()                                    # rechnen lassen
    letzte = len(app.content.winfo_children())                     # Widget-Zahl am Ende
    check("5 die Widget-Zahl bleibt gleich (keine Leichen)", letzte == erste,
          "%d -> %d" % (erste, letzte))
finally:
    root.destroy()

sys.exit(bericht())
