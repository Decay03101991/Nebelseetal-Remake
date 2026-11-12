# -*- coding: ascii -*-
"""Wache: Overlay-Basis - Dialoge INGAME statt Desktop-Fenster (03.11.2026).

DANIELS WUNSCH (22:2x)
----------------------
"Dialoge INGAME ueber dem Hauptfenster, Hintergrund abgedunkelt und durchscheinend" - keine
Zusatzfenster auf dem Desktop mehr. Vorher standen 10 `tk.Toplevel` im Code, jedes ein eigenes
Fenster (`docs/EINSCHAETZUNG_INGAME_FENSTER_20261103.md`).

WAS DIESE DATEI PRUEFT
----------------------
1. Nach dem Oeffnen existiert KEIN zusaetzliches Fenster und die Flaeche liegt ueber dem Inhalt.
2. Escape schliesst, und die Tastenbindung ist danach wieder frei.
3. Ein Klick NEBEN den Kasten schliesst (der Kasten selbst nicht).
4. Die Eingabesperre ist waehrend des Dialogs gesetzt und nach dem Schliessen wieder frei
   (`grab_current()` ist None) - sonst bliebe das Spiel gesperrt.
5. Ein Ansichtswechsel schliesst den Dialog (er haengt sonst ueber dem neuen Inhalt, A-Doppelpuffer).
6. Die drei umgestellten Dialoge (Dorf-Optionen, Truppen-Auswahl, Spionagebericht) sind ingame,
   keiner baut ein `Toplevel`, und ihr Schliessen-Knopf schliesst wirklich.
7. Quellwachen: die drei Funktionen nennen kein `tk.Toplevel(` mehr; die Zahlen stehen in
   `data/overlay.json`.

Aufruf:  python -X utf8 tests/test_overlay_ingame.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster"
PRUEF_STUFE = 4
PRUEF_BETRIFFT = ['auftraege', 'main:*']
PRUEF_DATEN = ['overlay.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import ast
import inspect
import os
import random
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
import tkinter as tk  # noqa: E402
import main as M  # noqa: E402


def _app(seed: int = 7, sichtbar: bool = True):
    """Frische App mit einer Siedlung - auf Wunsch als SICHTBARES Fenster (fuer die Eingabesperre)."""
    random.seed(seed)                                              # Karte reproduzierbar
    root = tk.Tk()                                                 # Tk-Wurzel
    app = M.NebelseetalApp(root)                                   # die App (Tor-Bildschirm)
    app._build_main_ui()                                           # Oberflaeche aufbauen
    app._erste_siedlung_gruenden()                                 # erste Siedlung, echte Startwerte
    if sichtbar:                                                   # echtes Fenster fuer grab_set
        root.geometry("1020x720+30+30")                            # feste Groesse
        root.deiconify()                                           # anzeigen
    else:                                                          # Kopfbetrieb
        root.withdraw()                                            # kein Fenster auf dem Schirm
    root.update()                                                  # einmal rechnen lassen
    return root, app


def _toplevels(widget) -> list:
    """Alle echten Zusatzfenster unter einem Widget (das ist der Stein des Anstosses)."""
    return [w for w in widget.winfo_children() if isinstance(w, tk.Toplevel)]


def _texte(widget) -> list:
    """Alle Texte unter einem Widget einsammeln (Knopf finden ohne Handliste)."""
    raus = []
    try:
        raus.append(str(widget.cget("text")))
    except Exception:
        pass
    for kind in widget.winfo_children():
        raus.extend(_texte(kind))
    return raus


def _knopf(widget, text: str):
    """Den Knopf mit genau diesem Text finden (rekursiv)."""
    if isinstance(widget, tk.Button) and str(widget.cget("text")) == text:
        return widget
    for kind in widget.winfo_children():
        treffer = _knopf(kind, text)
        if treffer is not None:
            return treffer
    return None


def _code(fn) -> str:
    """Quelltext einer Funktion ohne Docstring (nur echte Anweisungen)."""
    baum = ast.parse(textwrap.dedent(inspect.getsource(fn)))        # Funktion parsen
    baum.body[0].body = [k for k in baum.body[0].body               # Docstring abtrennen
                         if not (isinstance(k, ast.Expr) and isinstance(k.value, ast.Constant)
                                 and isinstance(k.value.value, str))]
    return ast.unparse(baum)


# ==========================================================================
abschnitt("1. Oeffnen legt eine Flaeche INGAME - kein zusaetzliches Fenster")
# ==========================================================================
root, app = _app()
try:
    vorher = len(_toplevels(root))                                  # Fenster vor dem Oeffnen
    app._overlay_oeffnen("Pruefdialog", lambda inhalt, schliessen: tk.Label(
        inhalt, text="Inhalt des Dialogs").pack(anchor=tk.W))
    root.update_idletasks()                                         # rechnen lassen
    check("1 der Dialog gilt als offen", app._overlay_offen(), str(app._overlay_offen()))
    check("1 es entsteht KEIN neues Fenster", len(_toplevels(root)) == vorher,
          "%d -> %d" % (vorher, len(_toplevels(root))))
    check("1 die Flaeche liegt im Inhaltsbereich",
          app._overlay is not None and app._overlay.master is app.inhalt_rahmen,
          str(type(app._overlay.master).__name__))
    check("1 sie deckt den Bereich ganz ab",
          float(app._overlay.place_info().get("relwidth", 0) or 0) == 1.0
          and float(app._overlay.place_info().get("relheight", 0) or 0) == 1.0,
          str(app._overlay.place_info()))
    kinder = app.inhalt_rahmen.winfo_children()                     # Zeichenreihenfolge
    check("1 sie liegt UEBER dem Inhalt (letztes Kind)", kinder and kinder[-1] is app._overlay,
          str([type(k).__name__ for k in kinder][-3:]))
    check("1 der Dialogtitel steht im Kasten", "Pruefdialog" in _texte(app._overlay_dialog),
          "")
    check("1 die Abdunkelung ist ein Bild (Pillow) oder eine dunkle Flaeche",
          app._overlay_bild is not None or len(app._overlay.winfo_children()) > 0,
          str(app._overlay_bild is not None))
finally:
    root.destroy()

# ==========================================================================
abschnitt("2. Escape schliesst - die Tastenbindung ist danach wieder frei")
# ==========================================================================
root, app = _app()
try:
    app._overlay_oeffnen("Escape-Test", lambda inhalt, schliessen: tk.Label(inhalt, text="x").pack())
    root.update_idletasks()
    check("2 waehrend des Dialogs ist Escape gebunden", bool(root.bind("<Escape>")),
          repr(root.bind("<Escape>")))
    app._overlay_escape()                                           # der gebundene Weg
    root.update_idletasks()
    check("2 Escape schliesst den Dialog", not app._overlay_offen(), "")
    check("2 danach ist die Bindung weg", not root.bind("<Escape>"), repr(root.bind("<Escape>")))
    check("2 die Flaeche ist zerstoert", not app._overlay)
finally:
    root.destroy()

# ==========================================================================
abschnitt("3. Klick NEBEN den Kasten schliesst, ein Klick IM Kasten nicht")
# ==========================================================================
root, app = _app()
try:
    app._overlay_oeffnen("Klick-Test", lambda inhalt, schliessen: tk.Label(inhalt, text="x").pack())
    root.update_idletasks()
    schleier = app._overlay.winfo_children()[0]                     # die Abdunkelung
    check("3 die Abdunkelung hat einen Klick-Befehl", bool(schleier.bind("<Button-1>")),
          repr(schleier.bind("<Button-1>")))
    app._overlay_dialog.event_generate("<Button-1>")                 # Klick in den Kasten
    root.update()
    check("3 ein Klick im Kasten schliesst NICHT", app._overlay_offen(), "")
    schleier.event_generate("<Button-1>")                           # Klick daneben
    root.update()
    check("3 ein Klick daneben schliesst", not app._overlay_offen(), "")
finally:
    root.destroy()

# ==========================================================================
abschnitt("4. Eingabesperre gesetzt und nach dem Schliessen wieder frei")
# ==========================================================================
root, app = _app(sichtbar=True)                                     # sichtbar: nur so gibt es einen grab
try:
    app._overlay_oeffnen("Sperre", lambda inhalt, schliessen: tk.Label(inhalt, text="x").pack())
    root.update()
    gesperrt = tk.Misc.grab_current(root)                           # wer hat die Eingabe?
    check("4 waehrend des Dialogs haelt die Flaeche die Eingabe",
          gesperrt is not None and str(gesperrt) == str(app._overlay),
          "%r gegen %r" % (gesperrt, app._overlay))
    app._overlay_schliessen()
    root.update()
    check("4 nach dem Schliessen ist die Eingabe frei",
          tk.Misc.grab_current(root) is None, repr(tk.Misc.grab_current(root)))
finally:
    root.destroy()

# ==========================================================================
abschnitt("5. Ansichtswechsel schliesst den Dialog (Doppel-Puffer, A)")
# ==========================================================================
root, app = _app()
try:
    app._switch_view("Portal")                                      # eine Ansicht aufbauen
    root.update_idletasks()
    app._overlay_oeffnen("Wechsel-Test", lambda inhalt, schliessen: tk.Label(inhalt, text="x").pack())
    check("5 der Dialog ist offen", app._overlay_offen(), "")
    app._switch_view("Lager")                                       # Ansicht wechseln
    root.update_idletasks()
    check("5 der Wechsel schliesst ihn", not app._overlay_offen(), "")
    check("5 die neue Ansicht steht vollstaendig da", bool(app.content.winfo_children()), "")
    check("5 kein Fenster entstanden", not _toplevels(root), str(len(_toplevels(root))))
finally:
    root.destroy()

# ==========================================================================
abschnitt("6. Die drei Dialoge sind ingame und lassen sich schliessen")
# ==========================================================================
root, app = _app()
try:
    bot, dorf = next((b, d) for b in app.state.bots              # ein Dorf der EIGENEN Welt
                     for d in M.bot_doerfer_sicherstellen(b)
                     if int(d.dimension) == int(app.state.eigene_dimension))
    # a) Dorf-Optionen
    app._bot_dorf_optionen(bot, dorf)
    root.update_idletasks()
    check("6a Dorf-Optionen sind ingame", app._overlay_offen() and not _toplevels(root),
          str(len(_toplevels(root))))
    check("6a sie bieten Angriff und Spionage",
          "Angriff planen" in _texte(app._overlay_dialog)
          and "Spionage" in _texte(app._overlay_dialog), "")
    _knopf(app._overlay_dialog, "Abbrechen").invoke()                # Schliessen-Knopf
    root.update_idletasks()
    check("6a Abbrechen schliesst sie", not app._overlay_offen(), "")
    # b) Truppen-Auswahl
    app._truppen_auswahl(bot, dorf, "angreifen")
    root.update_idletasks()
    check("6b Truppen-Auswahl ist ingame", app._overlay_offen() and not _toplevels(root),
          str(len(_toplevels(root))))
    check("6b sie traegt ihren Knopf 'Auftrag starten'",
          _knopf(app._overlay_dialog, "Auftrag starten") is not None, "")
    _knopf(app._overlay_dialog, "Abbrechen").invoke()
    root.update_idletasks()
    check("6b Abbrechen schliesst sie", not app._overlay_offen(), "")
    check("6b kein Auftrag gestartet", len(app.state.auftraege) == 0,
          str(len(app.state.auftraege)))
    # c) Spionagebericht
    app._spionage_bericht_anzeigen({"titel": "Spionage: Pruefdorf", "text": "Berichtstext"})
    root.update_idletasks()
    check("6c der Bericht ist ingame", app._overlay_offen() and not _toplevels(root),
          str(len(_toplevels(root))))
    check("6c er zeigt seinen Text", "Berichtstext" in " | ".join(_texte(app._overlay_dialog)), "")
    _knopf(app._overlay_dialog, "Schlie\u00dfen").invoke()
    root.update_idletasks()
    check("6c Schliessen schliesst ihn", not app._overlay_offen(), "")
finally:
    root.destroy()

# ==========================================================================
abschnitt("7. Quellwachen und Zahlen aus der Datendatei")
# ==========================================================================
for name, fn in (("Dorf-Optionen", M.NebelseetalApp._bot_dorf_optionen),
                 ("Truppen-Auswahl", M.NebelseetalApp._truppen_auswahl),
                 ("Spionagebericht", M.NebelseetalApp._spionage_bericht_anzeigen)):
    quelle = _code(fn)                                              # echter Code ohne Docstring
    check("7 %s baut kein Toplevel mehr" % name, "Toplevel" not in quelle, "")
    check("7 %s oeffnet den Ingame-Dialog" % name, "_overlay_oeffnen" in quelle, "")
check("7 die Basis hat oeffnen und schliessen",
      hasattr(M.NebelseetalApp, "_overlay_oeffnen")
      and hasattr(M.NebelseetalApp, "_overlay_schliessen"), "")
check("7 der Ansichtswechsel schliesst den Dialog",
      "_overlay_schliessen" in _code(M.NebelseetalApp._render_view), "")
werte = M.overlay_einstellungen()                                   # Zahlen aus data/overlay.json
check("7 die Deckkraft steht in der Datendatei", werte["abdunkeln"]["deckkraft"] == 140,
      str(werte["abdunkeln"].get("deckkraft")))
check("7 Escape ist als Schliessweg eingetragen", werte["schliessen"]["escape"] is True, "")
check("7 der Klick daneben ebenfalls", werte["schliessen"]["klick_daneben"] is True, "")
check("7 der Bildschirmabzug ist eingeschaltet (durchscheinend)",
      werte["abdunkeln"]["bildschirmabzug"] is True, "")
befund("7 ehrliche Grenze: Tk kann keine Transparenz je Widget - das Durchscheinen kommt aus einem "
       "Bildschirmabzug des Inhaltsbereichs mit dunklem Schleier. Ist der Abzug nicht moeglich "
       "(Fenster verdeckt, kein Pillow), liegt eine dunkle Flaeche darueber.", "")

sys.exit(bericht())
