# -*- coding: ascii -*-
"""Wache: die Lagerkacheln im Dorfzentrum - gleiche Masse, klares Band, grosses Symbol.

DANIELS BEFUND (Testbogen V_0.0.4, Register 454)
------------------------------------------------
T4 hat die Kacheln kleiner gemacht, sein Urteil blieb aber: "besser aber immer noch nicht
uebersichtlich und schoen genug gestaltet". Gemessen im Vorschaufenster war der Grund NICHT die
Groesse, sondern die fehlende Ordnung: jede Zelle war nur so breit wie ihr Inhalt - Kachelbreiten
61 bis 168 px, Hoehen 99 bis 106 px, Symbole 28 bis 49 px in verschiedenen Formen.

WAS SICH AM 13.11.2026 GEAENDERT HAT
------------------------------------
Die erste Fassung dieser Wache pruefte die damaligen Masse (118 x 136 px, 8 Spalten, Handliste in
`main.py`). Mit Claudes Antwort Nr. 16 (Teil A, Abschnitt C1) hat Daniel die Form geaendert:
**3 Spalten, 206 x 83 px je Kachel, 6 Reihen** - alle Gueter ohne Rollen sichtbar -, und die Masse
stehen seither an EINER Stelle (`src/dorfzentrum.py`). Diese Wache prueft die SUBSTANZ unveraendert
weiter (gleiche Kacheln, eigenes Zahlenband, Symbol im festen Kasten, Name zweizeilig), aber
gegen die neue Quelle.

WAS DIESE DATEI PRUEFT
----------------------
1. Kachelmasse in BEIDEN Fenstergroessen aus `dorfzentrum.lager_masse`: 206 x 83 / 185 x 72,
   Symbol 64 x 56, Textbreite 118 / 99, 6 Reihen 548 / 472 - jeweils unter der Inhaltshoehe.
2. Die alte Handliste (LAGER_KACHEL_BREITE/HOEHE, 8 Spalten) steht NICHT mehr im Code.
3. Die Kachel haelt ihre Masse: `grid_propagate(False)`, fester Symbolkasten, zweizeiliger Name,
   Zahl im eigenen Label, Klick waehlt die Ware.
4. Zahlen ohne sinnlose Nachkommastelle, grosse Zahlen mit Punkt - EINE Funktion.
5. Im echten Aufbau: 18 Kacheln, ALLE gleich gross, jede mit ihrer Zahl, drei passen in die
   Arbeitsflaeche. Genau das war vorher NICHT so - das war Daniels Befund.

Aufruf:  python -X utf8 tests/test_lager_kacheln_b4.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py.
PRUEF_ART = "fenster+messen"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['dorfzentrum', 'main:*']
PRUEF_DATEN = ['items.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import ast
import inspect
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src, messwert  # noqa: E402

ROOT, SRC = import_src()
os.chdir(SRC)

import dorfzentrum  # noqa: E402
import main  # noqa: E402

# Die gemessenen Zeilenhoehen (Nr. 16, A1): Fall 1 bei k = 1, Fall 2 bei k = 1,2512.
LS1 = {"text": 15, "zw": 18, "zahl": 18, "titel": 24}
LS2 = {"text": 19, "zw": 22, "zahl": 22, "titel": 30}


def _code(fn) -> str:
    """Den Rumpf einer Funktion als Code - Docstrings zaehlen NICHT als Code."""
    return ast.unparse(ast.parse(inspect.getsource(fn).lstrip()).body[0])


# --------------------------------------------------------------------------------------
abschnitt("1. Die Kachelmasse kommen aus EINER Quelle (dorfzentrum.lager_masse)")
_klein = dorfzentrum.lager_masse(588, 1.0, LS1)
_gross = dorfzentrum.lager_masse(658, 1.2512, LS2)
check("Fall 1: 3 Spalten", _klein["spalten"] == 3, str(_klein["spalten"]))
check("Fall 1: die Kachel ist 185 px breit", _klein["kachel_breite"] == 185,
      str(_klein["kachel_breite"]))
check("Fall 1: die Kachel ist 72 px hoch", _klein["kachel_hoehe"] == 72, str(_klein["kachel_hoehe"]))
check("Fall 1: die Textbreite in der Kachel ist 99 px", _klein["textbreite"] == 99,
      str(_klein["textbreite"]))
check("Fall 2: die Kachel ist 206 px breit", _gross["kachel_breite"] == 206,
      str(_gross["kachel_breite"]))
check("Fall 2: die Kachel ist 83 px hoch", _gross["kachel_hoehe"] == 83, str(_gross["kachel_hoehe"]))
check("Fall 2: die Textbreite in der Kachel ist 118 px", _gross["textbreite"] == 118,
      str(_gross["textbreite"]))
check("der Symbolkasten ist in beiden Faellen 64 x 56 px (Bildmass, waechst nicht)",
      (_klein["symbol_breite"], _klein["symbol_hoehe"]) == (64, 56)
      and (_gross["symbol_breite"], _gross["symbol_hoehe"]) == (64, 56), "")
check("Fall 1: 6 Reihen brauchen 472 px (<= 539 Inhaltshoehe)", _klein["hoehe"] == 472,
      str(_klein["hoehe"]))
check("Fall 2: 6 Reihen brauchen 548 px (<= 702 Inhaltshoehe)", _gross["hoehe"] == 548,
      str(_gross["hoehe"]))
check("17 Waren ergeben 6 Reihen (letzte Reihe mit 2 Kacheln)",
      dorfzentrum.lager_masse(658, 1.2512, LS2, waren=17)["reihen"] == 6, "")
check("18 Gueter ergeben ebenfalls 6 Reihen (die letzte ist voll)",
      dorfzentrum.lager_masse(658, 1.2512, LS2, waren=18)["reihen"] == 6, "")
check("GEGENPROBE: 19 Waren ergeben 7 Reihen - keine Ware faellt still heraus",
      dorfzentrum.lager_masse(658, 1.2512, LS2, waren=19)["reihen"] == 7, "")
messwert("kachel_breite_fall2", _gross["kachel_breite"], "px", "dorfzentrum.lager_masse")
messwert("kachel_hoehe_fall2", _gross["kachel_hoehe"], "px", "dorfzentrum.lager_masse")
messwert("lager_hoehe_fall2", _gross["hoehe"], "px", "dorfzentrum.lager_masse")

# --------------------------------------------------------------------------------------
abschnitt("2. Die alte Handliste ist entfallen (kein zweites Kachelmass)")
for _name in ("LAGER_KACHEL_BREITE", "LAGER_KACHEL_HOEHE", "LAGER_KACHEL_LUECKE",
              "LAGER_SPALTEN_VORGABE", "LAGER_SPALTEN_HOECHSTENS"):
    check("%s steht nicht mehr in main.py" % _name, not hasattr(main, _name), "")
for _name in ("_lager_spalten", "_lager_raster", "_lager_kachel", "_lager_nachziehen",
              "_lager_kacheln_zeichnen", "_lager_zahl"):
    check("%s ist mit der alten Kachelform entfallen" % _name,
          not hasattr(main.NebelseetalApp, _name), "")
check("der Symbolkasten steht weiter als Bildmass (64 x 56) in main.py",
      (int(main.LAGER_SYMBOL_BREITE), int(main.LAGER_SYMBOL_HOEHE)) == (64, 56),
      str((main.LAGER_SYMBOL_BREITE, main.LAGER_SYMBOL_HOEHE)))

# --------------------------------------------------------------------------------------
abschnitt("3. Die Kachel haelt ihre Masse (Quellwachen)")
_kachel = _code(main.NebelseetalApp._dz_kachel)
# KORRIGIERT 13.11.2026: Die Kinder der Kachel werden GEPACKT - gegen sie wirkt nur
# `pack_propagate(False)`. Die erste Fassung pruefte `grid_propagate`; die Kachel schrumpfte
# damit auf 146 px statt 185 (im Fenster gemessen), ohne dass eine Wache rot wurde.
check("die Kachel haelt ihre Masse (pack_propagate(False))",
      "pack_propagate(False)" in _kachel and "grid_propagate(False)" not in _kachel, "")
check("die Kachelbreite kommt aus der Rechnung, nicht aus einer Zahl",
      "kachel_breite" in _kachel and "width=206" not in _kachel
      and "width=185" not in _kachel, "")
check("der Symbolkasten ist fest (pack_propagate(False))",
      "pack_propagate(False)" in _kachel, "")
check("der Name bricht in der Textbreite der Kachel um (wraplength)",
      "wraplength=int(_k['textbreite'])" in _kachel, _kachel[:200])
check("der Name ist fest zweizeilig (height=2)", "height=2" in _kachel, "")
check("die Zahl steht in einem eigenen Label (eigenes Band, nichts springt)",
      "dorfzentrum.zahl_text(menge)" in _kachel, "")
check("ein Klick auf die Kachel waehlt die Ware", "_dz_auswahl_setzen" in _kachel, "")
check("die gewaehlte Kachel ist gezeichnet (2 px Creme innen)",
      "SPALTE_CREME if gewaehlt" in _kachel, "")
_symbol = _code(main.NebelseetalApp._lager_symbol)
check("das Symbol behaelt sein Seitenverhaeltnis (min von Breite und Hoehe)",
      "min(" in _symbol and "LANCZOS" in _symbol, "")
check("ohne Pillow faellt das Symbol auf tk.PhotoImage zurueck",
      "PhotoImage" in _symbol, "")
_lager = _code(main.NebelseetalApp._dz_lager)
check("das Raster nimmt die Spaltenzahl aus der Rechnung", "'spalten'" in _lager, "")
check("die Kacheln kommen aus der Warenliste der DATEN, nicht aus einer Handliste",
      "WARE_ICONS" in _lager, "")
_storage = _code(main.NebelseetalApp._render_storage)
check("der Entwicklertext aus data/items.json steht nicht in der Ansicht",
      "data/items.json" not in _storage, "")
check("die doppelte Fliesstext-Zeile (werkstatt.lager_text) ist entfallen",
      "lager_text" not in _storage and "lager_text" not in _lager, "")
check("der alte Rahmenstil relief=tk.RIDGE ist entfallen",
      "relief=tk.RIDGE" not in _storage and "relief=tk.RIDGE" not in _lager, "")
check("die stillgelegte Route benutzt dasselbe Raster (eine Anzeige, zwei Wege)",
      "_dz_lager" in _storage, "")
check("kein Pfad und keine JSON-Datei im Spielertext",
      "json" not in _lager and "data/" not in _lager, "")

# --------------------------------------------------------------------------------------
abschnitt("4. Zahlen ruhig und ohne sinnlose Nachkommastelle")
check("0 bleibt 0", dorfzentrum.zahl_text(0) == "0", dorfzentrum.zahl_text(0))
check("7 bleibt 7", dorfzentrum.zahl_text(7) == "7", dorfzentrum.zahl_text(7))
check("1334.0 wird 1334", dorfzentrum.zahl_text(1334.0) == "1334", dorfzentrum.zahl_text(1334.0))
check("12345 bekommt einen Punkt", dorfzentrum.zahl_text(12345) == "12.345",
      dorfzentrum.zahl_text(12345))
check("2.5 bleibt 2.5", dorfzentrum.zahl_text(2.5) == "2.5", dorfzentrum.zahl_text(2.5))
check("Text faellt nicht um", dorfzentrum.zahl_text("k.A.") == "k.A.",
      dorfzentrum.zahl_text("k.A."))
check("die Ansicht benutzt DIESE Zahlenfunktion (keine zweite)",
      "dorfzentrum.zahl_text" in _kachel, "")


# --------------------------------------------------------------------------------------
def _aufbau():
    abschnitt("5. Echter Aufbau im Fenster: 18 Kacheln, alle gleich gross")
    import tkinter as tk
    root = tk.Tk()
    root.geometry("1400x900+40+40")
    try:
        root.attributes("-alpha", 0.01)                                   # unsichtbar, aber VERMESSEN
    except Exception:                                                      # noqa: BLE001
        pass
    root.update()
    try:
        app = main.NebelseetalApp(root)
        app._build_main_ui()
        app._erste_siedlung_gruenden()
        for _ in range(3):
            root.update()
            root.update_idletasks()
        app._dz_reiter = 0                                                 # Reiter Lager
        app._switch_view("Dorfzentrum")
        for _ in range(3):
            root.update()
            root.update_idletasks()
        masze = getattr(app, "_dz_masse", None) or {}
        kachel_masse = masze.get("lager") or {}
        inhalt = getattr(app, "_dz_reiter_inhalt", None)
        check("die Arbeitsflaeche des Dorfzentrums steht", inhalt is not None, "")
        if inhalt is None:
            return
        kacheln = []
        for rahmen in [k for k in inhalt.winfo_children() if type(k).__name__ == "Frame"]:
            kacheln += [k for k in rahmen.winfo_children() if type(k).__name__ == "Frame"]
        check("im Reiter Lager stehen 18 Kacheln (17 Waren + Drachenschuppe)",
              len(kacheln) == 18, str(len(kacheln)))
        if not kacheln:
            return
        breiten = {int(k.cget("width")) for k in kacheln}
        hoehen = {int(k.cget("height")) for k in kacheln}
        check("ALLE Kacheln sind gleich breit (Daniels Befund war 61 bis 168 px)",
              len(breiten) == 1, str(sorted(breiten)))
        check("ALLE Kacheln sind gleich hoch", len(hoehen) <= 1, str(sorted(hoehen)))
        check("die Breite ist die gerechnete Kachelbreite",
              breiten == {int(kachel_masse.get("kachel_breite") or -1)},
              "%s gegen %s" % (sorted(breiten), kachel_masse.get("kachel_breite")))
        check("die Hoehe ist die gerechnete Kachelhoehe",
              hoehen <= {int(kachel_masse.get("kachel_hoehe") or -1)},
              "%s gegen %s" % (sorted(hoehen), kachel_masse.get("kachel_hoehe")))
        check("drei Kacheln passen in die Arbeitsflaeche R",
              len(kacheln) >= 3
              and 3 * int(kachel_masse.get("kachel_breite") or 0) <= int(masze.get("karte") or 0),
              str(3 * int(kachel_masse.get("kachel_breite") or 0)))
        mit_zahl = 0
        for kachel in kacheln:
            gefunden = False
            for kind in kachel.winfo_children():
                for enkel in kind.winfo_children():
                    try:
                        if str(enkel.cget("text")).replace(".", "").isdigit():
                            gefunden = True
                            break
                    except Exception:                                  # noqa: BLE001
                        continue
                if gefunden:
                    break
            if gefunden:
                mit_zahl += 1
        check("JEDE Kachel zeigt ihre Zahl", mit_zahl == len(kacheln),
              "%d von %d" % (mit_zahl, len(kacheln)))
        messwert("kacheln_im_aufbau", len(kacheln), "Stueck")
        messwert("kachel_breite_aufbau", sorted(breiten)[0], "px")
        messwert("kachel_hoehe_aufbau", sorted(hoehen)[0], "px")
        befund("Kein Nachziehen der Kacheln bei Groessenaenderung",
               "Die Arbeitsflaeche R haengt an der Fensterbreite; die Kacheln werden beim "
               "Neuaufbau gesetzt, nicht bei jedem Fensterzug (der fruehere Nachlauf "
               "`_lager_nachziehen` ist mit der alten Kachelform entfallen). Im Spiel ist das "
               "Fenster fest (1560 x 940 DPI-bewusst / 1446 x 744 unbewusst), darum faellt es "
               "dort nicht auf - offen bleibt es trotzdem.")
    finally:
        try:
            root.destroy()
        except Exception:                                                  # noqa: BLE001
            pass


try:
    _aufbau()
except Exception as _fehler:                                               # noqa: BLE001
    check("der Aufbau im Fenster laeuft ohne Ausnahme", False, repr(_fehler))

sys.exit(bericht())
