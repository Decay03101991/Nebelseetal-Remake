# -*- coding: ascii -*-
"""Kaserne-Ansicht ohne Gebaeude am aktiven Ort - Register 126.

BEFUND (02.11.2026, beim Bau von `tests/test_gebaeude_icons.py` aufgefallen): `menu_sichtbar`
zeigt "Kaserne", sobald die Kriegerakademie auf IRGENDEINER Siedlung steht - die Ansicht rechnet
aber mit der AKTIVEN Siedlung. Steht dort kein Gebaeude, liefert
`spieloekonomie.siedler_reserve` den Fruehfall, und der enthielt die Schluessel `guenstigste` und
`teuerste` NICHT. `_siedler_warnung_zeichnen` las `reserve["guenstigste"]` -> `KeyError`, die
Ansicht brach ab.

Was diese Datei beweist
-----------------------
1. Der Fruehfall von `siedler_reserve` liefert DIESELBEN Schluessel wie der Normalfall (Vergleich
   der Schluesselmengen aus zwei echten Orten - keine zweite Handliste).
2. Die Kaserne-Ansicht rendert mit einer aktiven Siedlung OHNE Gebaeude, ohne Ausnahme.
3. Die Siedlerwarnung erscheint in diesem Fall trotzdem (freie Siedler stehen im Kopf).

Aufruf:  python -X utf8 tests/test_kaserne_ohne_gebaeude.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster"
PRUEF_STUFE = 4
PRUEF_BETRIFFT = ['main:*', 'spieloekonomie']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import sys
import tempfile
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, bericht, check, import_src

ROOT, SRC = import_src()
import main              # noqa: E402
import spieloekonomie     # noqa: E402

# ==========================================================================
abschnitt("1. Fruehfall und Normalfall liefern dieselben Schluessel")
# ==========================================================================

# Zwei ECHTE Orts-Dicts: einer mit Gebaeude (Normalfall), einer ohne (Fruehfall). Die Bauart kommt
# aus `main.Settlement` (asdict), damit die Pruefung nicht an einer erfundenen Struktur misst.
mit = main.Settlement(name="Mit Akademie", map_id="kontinent", x=5, y=5, id="t:kontinent:5:5")
mit.bauten["3"] = "kriegerakademie"      # ein Gebaeude, das Einheiten ausbildet
mit.stufen["3"] = 1
ohne = main.Settlement(name="Ohne Gebaeude", map_id="kontinent", x=6, y=6, id="t:kontinent:6:6")

from dataclasses import asdict  # noqa: E402

normal = spieloekonomie.siedler_reserve(asdict(mit), {})
frueh = spieloekonomie.siedler_reserve(asdict(ohne), {})

check("1 der Normalfall kennt ueberhaupt Einheiten (sonst misst die Pruefung nichts)",
      bool(normal.get("bedarf_je_einheit")), str(list(normal.get("bedarf_je_einheit") or {})))
check("1 der Fruehfall ist wirklich der Fruehfall (kein Bedarf)",
      not frueh.get("bedarf_je_einheit"), str(frueh.get("bedarf_je_einheit")))
check("1 beide Faelle liefern DIESELBEN Schluessel",
      set(normal) == set(frueh), "fehlt: %s, zuviel: %s" % (
          sorted(set(normal) - set(frueh)), sorted(set(frueh) - set(normal))))
check("1 'guenstigste' steht im Fruehfall (der gelesene Schluessel)",
      "guenstigste" in frueh, str(sorted(frueh)))
check("1 'guenstigste' ist ein Paar (Name, Siedler)",
      isinstance(frueh.get("guenstigste"), tuple) and len(frueh["guenstigste"]) == 2,
      str(frueh.get("guenstigste")))
check("1 der Fruehfall warnt nicht (es gibt nichts auszubilden)",
      frueh.get("warnung") is False and frueh.get("text") == "", str(frueh.get("text")))

# ==========================================================================
abschnitt("2. Die Kaserne-Ansicht rendert ohne Gebaeude am aktiven Ort")
# ==========================================================================

root = tk.Tk()                                            # echtes Fenster, nur nicht sichtbar
root.withdraw()
tor_pfad = os.path.join(tempfile.gettempdir(), "nebel_kaserne_pruef_tor.json")
app = main.NebelseetalApp(root, tor_pfad=tor_pfad)
app._build_main_ui()
app._found_settlement()                                   # echte Gruendung
root.update()
erste = app.state.settlements[0]
# Ein freies Feld der ersten Siedlung bekommt die Kriegerakademie - damit steht "Kaserne" im Menue.
raster = erste.karte["raster"]
frei = next(i for i, art in enumerate(raster) if not erste.bauten.get(str(i)))
erste.bauten[str(frei)] = "kriegerakademie"
erste.stufen[str(frei)] = 1
# Zweite Siedlung OHNE Gebaeude, aktiv gemacht: genau Daniels Lage nach einem Ortswechsel.
zweite = main.Settlement(name="Zweites Dorf", map_id="kontinent", x=7, y=7, id="pruef:kontinent:7:7")
zweite.karte = dict(erste.karte)
app.state.settlements.append(zweite)
app.state.aktive_siedlung_id = zweite.id
check("2 die aktive Siedlung ist die ohne Gebaeude",
      app.state.aktive_siedlung() is zweite and not zweite.bauten, str(zweite.bauten))
app._menue_auffrischen()
root.update()
check("2 'Kaserne' steht im Menue (die Akademie steht ja auf der anderen Siedlung)",
      "Kaserne" in app.menu_buttons, str(sorted(app.menu_buttons)))

ergebnis = ausnahme("2 Kaserne-Ansicht rendert ohne Gebaeude am aktiven Ort",
                    lambda: (app._switch_view("Kaserne"), root.update_idletasks()))
check("2 die Ansicht ist aufgebaut", ergebnis is not None, "kein Abbruch")

texte = []


def _sammle(widget):
    """Alle Beschriftungen unter einem Widget einsammeln (auch verschachtelt)."""
    for kind in widget.winfo_children():
        try:
            t = str(kind.cget("text"))
        except Exception:                                  # noqa: BLE001 - Widget ohne Text
            t = ""
        if t:
            texte.append(t)
        _sammle(kind)


_sammle(app.content)
gesamt = " | ".join(texte)
check("2 die Siedlerwarnung steht in der Ansicht", "Freie Siedler" in gesamt, gesamt[:160])
check("2 die Ausbildungshinweise stehen da", "Kriegerakademie" in gesamt, gesamt[:160])

root.destroy()

# ==========================================================================
sys.exit(bericht())
