# -*- coding: ascii -*-
"""Wache: B4 Lagerkacheln - gleiche Masse, klares Band, grosses Symbol (12.11.2026).

DANIELS BEFUND (Testbogen V_0.0.4, Register 454)
------------------------------------------------
T4 hat die Kacheln kleiner gemacht, sein Urteil blieb aber: "besser aber immer noch nicht
uebersichtlich und schoen genug gestaltet". Gemessen im Vorschaufenster war der Grund NICHT die
Groesse, sondern die fehlende Ordnung: jede Zelle war nur so breit wie ihr Inhalt - Kachelbreiten
61 bis 168 px, Hoehen 99 bis 106 px, Symbole 28 bis 49 px in verschiedenen Formen.

WAS DIESE DATEI PRUEFT
----------------------
1. Die vier Kachelmasse stehen als EINE Quelle im Code und acht Kacheln passen in die gemessene
   Inhaltsbreite von 1037 px.
2. Die Spaltenzahl folgt der gemessenen Breite und ist gedeckelt (nie unter 3, nie ueber 9);
   ohne Messung gilt die Vorgabe 8.
3. Im echten Aufbau hat JEDE Kachel dieselbe Anforderungsgroesse, jedes Symbol sitzt in einem
   Kasten gleicher Hoehe, der Name ist fest zweizeilig und die Zahl steht in einem eigenen Band
   mit fester Hoehe - nichts springt bei anderer Zahl.
4. Zahlen werden ohne sinnlose Nachkommastelle gezeigt, grosse Zahlen mit Punkt.
5. Quellwachen: der Entwicklertext aus data/items.json ist weg, die doppelte Textzeile
   (`werkstatt.lager_text` als Fliesstext) ist weg, und die drei Mittel stehen im Code:
   `grid_propagate(False)` (feste Kachel), `uniform=` (gleiche Spalten), eigenes Zahlenband.

Aufruf:  python -X utf8 tests/test_lager_kacheln_b4.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster+messen"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['einheiten', 'main:*', 'werkstatt']
PRUEF_DATEN = ['items.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import ast
import inspect
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src, messwert  # noqa: E402

import_src()
import main  # noqa: E402


# --------------------------------------------------------------------------------------
def _code(fn) -> str:
    """Den Rumpf einer Funktion als Code - Docstrings zaehlen NICHT als Code."""
    text = ast.unparse(ast.parse(inspect.getsource(fn).lstrip()).body[0])
    return text


class _Stellvertreter:
    """Leichtgewichtiger Stellvertreter fuer `_lager_spalten`: nur die gemessene Breite zaehlt."""

    def __init__(self, breite: int):
        self._breite = breite

    def _inhalt_breite(self) -> int:
        return self._breite


# --------------------------------------------------------------------------------------
def _masse():
    abschnitt("1. Die Kachelmasse sind EINE Quelle und passen achtmal in 1037 px")
    breite = int(main.LAGER_KACHEL_BREITE)
    hoehe = int(main.LAGER_KACHEL_HOEHE)
    luecke = int(main.LAGER_KACHEL_LUECKE)
    check("die Kachel ist 118 px breit", breite == 118, str(breite))
    check("die Kachel ist 136 px hoch", hoehe == 136, str(hoehe))
    check("zwischen zwei Kacheln liegen 6 px", luecke == 6, str(luecke))
    check("der Symbolkasten ist 64 x 56 px",
          (int(main.LAGER_SYMBOL_BREITE), int(main.LAGER_SYMBOL_HOEHE)) == (64, 56),
          str((main.LAGER_SYMBOL_BREITE, main.LAGER_SYMBOL_HOEHE)))
    gesamt = 8 * breite + 7 * luecke                     # acht Kacheln samt Luft
    check("acht Kacheln passen in die gemessene Inhaltsbreite 1037",
          gesamt <= 1037, "%d px gebraucht" % gesamt)
    check("der Name hat innen Platz (wraplength = Breite - 16)",
          breite - 16 >= 100, str(breite - 16))
    messwert("kachel_breite", breite, "px")
    messwert("kachel_hoehe", hoehe, "px")
    messwert("acht_kacheln_gesamt", gesamt, "px")


# --------------------------------------------------------------------------------------
def _spalten():
    abschnitt("2. Die Spaltenzahl folgt der gemessenen Breite")
    gross = main.NebelseetalApp._lager_spalten(_Stellvertreter(1037))
    klein = main.NebelseetalApp._lager_spalten(_Stellvertreter(691))
    sehr_klein = main.NebelseetalApp._lager_spalten(_Stellvertreter(300))
    ohne = main.NebelseetalApp._lager_spalten(_Stellvertreter(0))
    breit = main.NebelseetalApp._lager_spalten(_Stellvertreter(2400))
    check("bei 1037 px Inhaltsbreite stehen 8 Spalten", gross == 8, str(gross))
    check("bei 691 px (kleines Fenster) stehen 5 Spalten", klein == 5, str(klein))
    check("bei 300 px bleiben mindestens 3 Spalten", sehr_klein == 3, str(sehr_klein))
    check("ohne Messung gilt die Vorgabe 8", ohne == int(main.LAGER_SPALTEN_VORGABE), str(ohne))
    check("die Spalten sind bei 2400 px auf 9 gedeckelt", breit == 9, str(breit))
    check("acht Spalten brauchen nicht mehr als die Inhaltsbreite",
          8 * 118 + 7 * 6 <= 1037, "rechnerisch")
    messwert("spalten_bei_1037", gross, "Spalten")
    messwert("spalten_bei_691", klein, "Spalten")


# --------------------------------------------------------------------------------------
def _zahlen():
    abschnitt("3. Zahlen ruhig und ohne sinnlose Nachkommastelle")
    zahl = main.NebelseetalApp._lager_zahl
    check("0 bleibt 0", zahl(0) == "0", zahl(0))
    check("7 bleibt 7", zahl(7) == "7", zahl(7))
    check("1334.0 wird 1334", zahl(1334.0) == "1334", zahl(1334.0))
    check("12345 bekommt einen Punkt", zahl(12345) == "12.345", zahl(12345))
    check("2.5 bleibt 2.5", zahl(2.5) == "2.5", zahl(2.5))
    check("Text faellt nicht um", zahl("k.A.") == "k.A.", zahl("k.A."))


# --------------------------------------------------------------------------------------
def _quellwachen():
    abschnitt("4. Quellwachen: Entwicklertext und Doppelanzeige sind weg, die drei Mittel sind da")
    quelle = inspect.getsource(main.NebelseetalApp._render_storage)
    check("der Entwicklertext aus data/items.json steht nicht mehr in der Ansicht",
          "data/items.json" not in quelle, "steht noch drin")
    check("die doppelte Fliesstext-Zeile (werkstatt.lager_text) ist entfallen",
          "lager_text" not in quelle, "steht noch drin")
    check("der alte Rahmenstil relief=tk.RIDGE ist entfallen",
          "relief=tk.RIDGE" not in quelle, "steht noch drin")
    check("die Ansicht baut die Abschnitte ueber _lager_abschnitt",
          "_lager_abschnitt(" in quelle)
    check("die Ansicht ruft _lager_kacheln_zeichnen",
          "_lager_kacheln_zeichnen(" in quelle)
    check("beide Raster liegen als Attribut fuer die Wache",
          "lager_waren_rahmen" in quelle and "lager_einheiten_rahmen" in quelle)
    kachel = _code(main.NebelseetalApp._lager_kachel)
    check("die Kachel haelt ihre Masse (grid_propagate(False))",
          "grid_propagate(False)" in kachel)
    check("die Kachel hat ein eigenes Zahlenband mit fester Hoehe",
          "pack_propagate(False)" in kachel and "zahlband" in kachel)
    check("der Name ist fest zweizeilig (height=2)",
          "height=2" in kachel)
    raster = _code(main.NebelseetalApp._lager_raster)
    check("alle Spalten sind gleich breit (uniform=)",
          "uniform=" in raster)
    symbol = _code(main.NebelseetalApp._lager_symbol)
    check("das Symbol behaelt sein Seitenverhaeltnis (min von Breite und Hoehe)",
          "min(" in symbol and "LANCZOS" in symbol)
    check("ohne Pillow faellt das Symbol auf tk.PhotoImage zurueck",
          "PhotoImage" in symbol)


# --------------------------------------------------------------------------------------
def _aufbau():
    abschnitt("5. Echter Aufbau im Fenster: gleiche Kacheln, gleiches Band, gleiche Symbolhoehe")
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
        app._switch_view("Dorfzentrum")
        for _ in range(3):
            root.update()
            root.update_idletasks()
        waren = getattr(app, "lager_waren_rahmen", None)
        einheiten = getattr(app, "lager_einheiten_rahmen", None)
        check("die Warenkacheln stehen in der Ansicht", waren is not None)
        check("die Einheitenkacheln stehen in der Ansicht", einheiten is not None)
        if waren is None or einheiten is None:
            return
        messwert("inhalt_breite_im_aufbau", int(app._inhalt_breite()), "px")
        messwert("spalten_im_aufbau", int(app._lager_spalten()), "Spalten")
        check("es sind so viele Warenkacheln wie Lagerfaecher im Spielstand",
              len(waren.grid_slaves()) == len(app.state.waren),
              "%d Kacheln zu %d Waren" % (len(waren.grid_slaves()), len(app.state.waren)))
        check("es sind so viele Einheitenkacheln wie Einheiten im Spielstand",
              len(einheiten.grid_slaves()) == len(app.state.units),
              "%d Kacheln zu %d Einheiten" % (len(einheiten.grid_slaves()), len(app.state.units)))
        messwert("kacheln_waren", len(waren.grid_slaves()), "Kacheln")
        messwert("kacheln_einheiten", len(einheiten.grid_slaves()), "Kacheln")
        for name, rahmen in (("Waren", waren), ("Einheiten", einheiten)):
            kacheln = rahmen.grid_slaves()
            breiten = sorted({int(k.winfo_width()) for k in kacheln})
            hoehen = sorted({int(k.winfo_height()) for k in kacheln})
            check("%s: alle Kacheln sind GEMESSEN gleich breit (%d px)" % (name, breiten[0]),
                  len(breiten) == 1, str(breiten))
            check("%s: alle Kacheln sind GEMESSEN gleich hoch (%d px)" % (name, hoehen[0]),
                  len(hoehen) == 1, str(hoehen))
            check("%s: jede Kachel traegt die feste Breite in ihren Optionen" % name,
                  {int(k.cget("width")) for k in kacheln} == {int(main.LAGER_KACHEL_BREITE)},
                  str(sorted({int(k.cget("width")) for k in kacheln})))
            check("%s: jede Kachel traegt die feste Hoehe in ihren Optionen" % name,
                  {int(k.cget("height")) for k in kacheln} == {int(main.LAGER_KACHEL_HOEHE)},
                  str(sorted({int(k.cget("height")) for k in kacheln})))
            spalten = {int(k.grid_info()["column"]) for k in kacheln}
            check("%s: die Kacheln stehen in hoechstens neun Spalten" % name,
                  max(spalten) <= 8, str(sorted(spalten)))
            band_y, band_h, symhoehen, namen, baender = set(), set(), set(), 0, 0
            for kachel in kacheln:
                for innen in kachel.winfo_children():
                    if innen.winfo_class() == "Frame":
                        if int(innen.cget("height")) == 24:            # das Zahlenband
                            baender += 1
                            band_y.add(int(innen.winfo_y()))           # gleiche Hoehe in JEDER Kachel
                            band_h.add(int(innen.winfo_height()))
                        else:                                          # der Symbolkasten
                            symhoehen.add(int(innen.winfo_height()))
                    elif innen.winfo_class() == "Label":
                        namen += 1
                        if int(str(innen.cget("height"))) != 2:
                            namen -= 100                               # unmoeglich -> faellt unten auf
            check("%s: jedes Symbol ist GEMESSEN gleich hoch (%d px)" % (name, 56),
                  symhoehen == {int(main.LAGER_SYMBOL_HOEHE)}, str(symhoehen))
            check("%s: das Zahlenband sitzt in jeder Kachel auf derselben Hoehe" % name,
                  len(band_y) == 1, str(sorted(band_y)))
            check("%s: das Band ist ueberall gleich hoch (%d px)" % (name, 24),
                  band_h == {24}, str(band_h))
            check("%s: jede Kachel hat genau einen zweizeiligen Namen" % name,
                  namen == len(kacheln), str(namen))
            check("%s: jede Kachel hat genau ein Zahlenband" % name,
                  baender == len(kacheln), str(baender))
        # Ueberschriften in Spielersprache
        texte = []

        def _sammle(widget):
            try:
                t = widget.cget("text")
            except Exception:                                              # noqa: BLE001
                t = ""
            if t:
                texte.append(str(t))
            for kind in widget.winfo_children():
                _sammle(kind)

        _sammle(app.content)
        gesamt = " | ".join(texte)
        check("der Abschnitt heisst 'Waren im Lager'", "Waren im Lager" in gesamt, gesamt[:120])
        check("der Abschnitt heisst 'Einheiten im Lager'", "Einheiten im Lager" in gesamt)
        check("die Artenzahl steht dabei", "Arten" in gesamt)
        check("kein Pfad und keine JSON-Datei im Text",
              "json" not in gesamt and "data/" not in gesamt)
        befund("Sichtpruefung durch Daniel steht aus",
               "die Kacheln sind hier gemessen; das Bild liegt als b4_waren.png im Scratch")
    finally:
        try:
            root.destroy()
        except Exception:                                                  # noqa: BLE001
            pass


# --------------------------------------------------------------------------------------
def _nachziehen():
    abschnitt("6. Der Nachlauf greift nur bei geaenderter Spaltenzahl")
    quelle = inspect.getsource(main.NebelseetalApp._lager_nachziehen)
    check("der Nachlauf vergleicht die Spaltenzahl", "_lager_spalten()" in quelle)
    check("der Nachlauf merkt sich den Stand", "_lager_spalten_ist" in quelle)
    check("der Nachlauf prueft, ob die Ansicht noch existiert", "winfo_exists" in quelle)
    render = inspect.getsource(main.NebelseetalApp._render_storage)
    check("die Configure-Bindung wird nur EINMAL gesetzt", "_lager_configure_gebunden" in render)


# --------------------------------------------------------------------------------------
if __name__ == "__main__":
    _masse()
    _spalten()
    _zahlen()
    _quellwachen()
    _aufbau()
    _nachziehen()
    sys.exit(bericht())
