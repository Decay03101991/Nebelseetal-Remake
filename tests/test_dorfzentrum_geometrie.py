# -*- coding: ascii -*-
"""Wache: die GEOMETRIE der Dorfzentrum-Spalte im gebauten Fenster (F-89a, Sitzung 44).

WARUM DIESE DATEI NOETIG IST
----------------------------
`test_dorfzentrum_ansicht.py` haelt Zahlen gegen Zahlen: es liest `_dz_block_hoehen` und
addiert sie zur Fensterhoehe. Solange die Zahlen aus dem Verteiler stammen, ist die Summe per
Bauart gleich der Fensterhoehe - die Wache war 119 + 44 mal gruen, waehrend die Spalte 1149 px
hoch war bei 764 px Sichtfenster und `yview` bei (0.0, 0.665) stand. Diese Datei misst
stattdessen das GEBAUTE Fenster:

1. `winfo_height()` jeder Blockrahmen ist echt (groesser als 1) und die Summe samt Luecken ist
   genau die Hoehe der Leinwand.
2. `yview()` der Leinwand ist (0.0, 1.0) - es fehlt kein Stueck.
3. Der letzte Block (Hinweis) liegt mit seiner Unterkante IM Sichtfenster.
4. Die Bloecke liegen untereinander ohne Ueberlappung, in der Reihenfolge aus Nr. 16.
5. Block 5 (Auswahl) ist der groesste Block - er nimmt den Rest.
6. Die Spalte ist so breit wie `masse()["spalte"]`, und der Inhalt des Auswahlblocks laeuft
   nicht ueber seinen Rahmen hinaus.

Aufruf: python -X utf8 tests/test_dorfzentrum_geometrie.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py.
PRUEF_ART = "fenster+messen"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['dorfzentrum', 'main:*', 'spieloekonomie']
PRUEF_DATEN = ['items.json', 'warenrezepte.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src, messwert  # noqa: E402

ROOT, SRC = import_src()
os.chdir(SRC)

import dorfzentrum  # noqa: E402
import main  # noqa: E402

REIHENFOLGE = ("kopf", "naechster", "ort", "aktionen", "auswahl", "hinweis")


def _probe():
    """Fenster wirklich aufbauen und der Geometrie mehrere Zyklen geben."""
    import tkinter as tk
    root = tk.Tk()
    root.geometry("1560x940+40+20")
    try:
        root.attributes("-alpha", 0.01)
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
        app._dz_reiter = 0
        app._switch_view("Dorfzentrum")
        for _ in range(5):                     # Tk braucht mehrere Zyklen fuer grid + weight
            root.update()
            root.update_idletasks()
        return app, root
    except Exception:
        root.destroy()
        raise


def _namen_und_rahmen(app):
    """(Name, Rahmen) in der Reihenfolge, in der die Spalte sie haelt."""
    rahmen = dict(getattr(app, "_dz_block_rahmen", {}) or {})
    return [(n, rahmen[n]) for n in REIHENFOLGE if n in rahmen]


def _lauf():
    app, root = _probe()
    try:
        m = getattr(app, "_dz_masse", None) or {}
        leinwand = getattr(app, "_dz_leinwand", None)
        spalte = getattr(app, "_dz_spalte", None)
        check("Leinwand und Spalte sind gebaut", leinwand is not None and spalte is not None, "")
        if leinwand is None or spalte is None:
            return

        p = int(m.get("p") or 0)
        sicht = int(leinwand.winfo_height())
        paare = _namen_und_rahmen(app)

        # ---------------------------------------------------------------- 1. echte Blockhoehen
        abschnitt("1. Die Bloecke haben GEMESSENE Hoehen (nicht 1 px)")
        hoehen = {}
        for name, rahmen in paare:
            h = int(rahmen.winfo_height())
            hoehen[name] = h
            messwert("block_%s" % name, h, "px")
            check("Block %s ist gemessen hoeher als 1 px" % name, h > 1, str(h))
        check("es sind sechs Bloecke (Technik nur im Entwicklerbetrieb)",
              sorted(hoehen) == sorted(REIHENFOLGE), str(sorted(hoehen)))

        # ---------------------------------------------------------------- 2. Summe = Sichtfenster
        abschnitt("2. Summe der Bloecke + Luecken = Sichtfenster")
        summe = sum(hoehen.values()) + len(hoehen) * p
        messwert("summe_bloecke_und_luecken", summe, "px")
        messwert("sichtfenster", sicht, "px")
        check("Summe der Bloecke + Luecken ist die Hoehe der Leinwand (%d px)" % sicht,
              abs(summe - sicht) <= 1, "%d gegen %d" % (summe, sicht))

        # ---------------------------------------------------------------- 3. yview
        abschnitt("3. Die Spalte rollt NICHT (yview)")
        y0, y1 = leinwand.yview()
        messwert("yview_oben", round(y0, 3), "")
        messwert("yview_unten", round(y1, 3), "")
        check("yview beginnt bei 0.0", abs(y0) <= 0.001, "%.3f" % y0)
        check("yview endet bei 1.0 - es fehlt kein Stueck", abs(y1 - 1.0) <= 0.001, "%.3f" % y1)

        # ---------------------------------------------------------------- 4. letzter Block sichtbar
        abschnitt("4. Der letzte Block liegt im Sichtfenster")
        for name, rahmen in paare:
            y = int(rahmen.winfo_rooty()) - int(spalte.winfo_rooty())
            unterkante = y + int(rahmen.winfo_height())
            messwert("y_%s" % name, y, "px")
            check("Block %s beginnt im Sichtfenster (y=%d)" % (name, y), y < sicht, str(y))
            check("Block %s endet im Sichtfenster (Unterkante %d <= %d)" % (name, unterkante, sicht),
                  unterkante <= sicht + 1, "%d gegen %d" % (unterkante, sicht))

        # ---------------------------------------------------------------- 5. Reihenfolge
        abschnitt("5. Die Bloecke liegen untereinander in der Reihenfolge aus Nr. 16")
        _vorher = -1
        for name, rahmen in paare:
            y = int(rahmen.winfo_rooty()) - int(spalte.winfo_rooty())
            check("Block %s liegt unter dem vorigen (y=%d)" % (name, y), y >= _vorher, str(y))
            _vorher = y
            check("Block %s ist nicht zusammengefallen (Breite > 0)" % name,
                  int(rahmen.winfo_width()) > 0, str(rahmen.winfo_width()))

        # ---------------------------------------------------------------- 6. Auswahl = Rest
        abschnitt("6. Block 5 (Auswahl) nimmt den Rest")
        check("die Auswahl ist der groesste Block", hoehen.get("auswahl") == max(hoehen.values()),
              str(hoehen))
        check("die Auswahl ist mindestens 120 px hoch", int(hoehen.get("auswahl") or 0) >= 120,
              str(hoehen.get("auswahl")))

        # ---------------------------------------------------------------- 7. Breite und Inhalt
        abschnitt("7. Die Spalte ist so breit wie berechnet, der Inhalt bleibt im Rahmen")
        check("die Spalte ist %d px breit" % int(m.get("spalte") or 0),
              abs(int(spalte.winfo_width()) - int(m.get("spalte") or 0)) <= 1,
              "%d gegen %d" % (int(spalte.winfo_width()), int(m.get("spalte") or 0)))
        _auswahl = (getattr(app, "_dz_block_rahmen", {}) or {}).get("auswahl")
        if _auswahl is not None:
            _letztes = None
            for kind in _auswahl.winfo_children():
                if int(kind.winfo_height()) > 1:
                    _letztes = kind
            if _letztes is not None:
                _unterkante = (int(_letztes.winfo_rooty()) - int(_auswahl.winfo_rooty())
                               + int(_letztes.winfo_height()))
                messwert("auswahl_inhalt_unterkante", _unterkante, "px")
                check("der Inhalt des Auswahlblocks endet in seinem Rahmen (%d <= %d)"
                      % (_unterkante, int(_auswahl.winfo_height())),
                      _unterkante <= int(_auswahl.winfo_height()) + 1,
                      "%d gegen %d" % (_unterkante, int(_auswahl.winfo_height())))

        befund("die Hoehen sind aus dem gebauten Fenster gelesen",
               "dieselbe Ansicht im Entwicklerbetrieb (Technikblock) ist hier nicht gemessen; "
               "die Zahlen gelten fuer den Spielerbetrieb")
    finally:
        try:
            root.destroy()
        except Exception:                                                  # noqa: BLE001
            pass


try:
    _lauf()
except Exception as _fehler:                                               # noqa: BLE001
    import traceback
    traceback.print_exc()
    check("die Ansicht baut ohne Ausnahme", False, repr(_fehler))

sys.exit(bericht())
