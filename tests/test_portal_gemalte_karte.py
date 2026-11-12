# -*- coding: ascii -*-
"""Wache: die GEMALTE Karte im Gelaendekaestchen des Portals (D-4, 09.11.2026).

DANIELS ENTSCHEIDUNG (F-35, 09.11.2026)
---------------------------------------
"Die Vorschau + 28 % ist ok aber halte fest das ich es vom stil wie bei der Stilprobe A will aber
das die karte gerade angezeigt wird wie bei vorschau + 28%" und "eine weltkarte bleibt ... bitte
also 20 px". Also: gerade Draufsicht, 20 px je Feld (400 x 400 px), kein Rollbalken. D-4 baut die
in D-3 gemalte Karte (`src/weltkarte_malerei.py`) in `_render_portal` ein.

WAS DIESE DATEI PRUEFT
----------------------
1. `_portal_raster` baut aus den Feldern der Anzeige Zeilen von oben nach unten. Eine fehlende
   oder unbekannte Gelaendekennung ergibt None - es wird kein Gelaende erfunden.
2. Die Ansicht legt GENAU EIN Bild von 400 x 400 px auf die Zeichenflaeche; die 400 Gelaende-
   rechtecke und die 42 Gitterlinien von vor D-4 sind weg. Die Dorfmarken bleiben unberuehrt.
3. Bild und Rasterlage stimmen: in einem selbst gemalten Bild sitzt die abweichende Gelaendeart
   an der Bildstelle IHRES Feldes - in der Zeile UND in der Spalte (ein x/y-Tausch faellt auf).
4. Der Klick trifft dasselbe Feld wie vorher: die Feldmitte (x + 0,5) * 20 px liegt im Feld x,
   und ein Klick dort waehlt genau dieses Feld.
5. Der Rueckfall OHNE Malerei zeichnet weiter 400 Felder und 42 Trennlinien in RASTER_LINIE -
   ohne Pillow ist die Ansicht nicht schlechter als vor D-4.
6. Quellwachen: die Ansicht benutzt `weltkarte_malerei.karte_malen`, der Rueckfall die eine
   Trennlinien-Farbe, und die Feldmitte rechnet mit 0.5 (kein Versatz durch das Bild).

Aufruf:  .venv/Scripts/python.exe -X utf8 tests/test_portal_gemalte_karte.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster"
PRUEF_STUFE = 3
PRUEF_BETRIFFT = ['gelaende', 'main:*', 'portalraum', 'stimmen', 'weltkarte_malerei']
PRUEF_DATEN = []
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
import gelaende  # noqa: E402
import main as M  # noqa: E402
import portalraum as P  # noqa: E402
import weltkarte_malerei as W  # noqa: E402

KANTE = 20                                                          # Felder je Achse
ZELLE = 20                                                          # px je Feld (F-35)


def _app(seed: int = 7):
    """Frische App mit Siedlung - ohne Fenster auf dem Schirm."""
    random.seed(seed)
    root = tk.Tk()
    root.withdraw()
    app = M.NebelseetalApp(root)
    app._build_main_ui()
    app._erste_siedlung_gruenden()
    root.update_idletasks()
    return root, app


def _code(fn) -> str:
    """Quelltext einer Funktion ohne Docstring (nur echte Anweisungen)."""
    baum = ast.parse(textwrap.dedent(inspect.getsource(fn)))
    baum.body[0].body = [k for k in baum.body[0].body
                         if not (isinstance(k, ast.Expr) and isinstance(k.value, ast.Constant)
                                 and isinstance(k.value.value, str))]
    return ast.unparse(baum)


def _mittel(bild, x: int, y: int, r: int = 3) -> tuple:
    """Mittlere Farbe eines kleinen Kastens um (x, y) - robuster als ein einzelner Pixel."""
    px = bild.load()
    summe = [0, 0, 0]
    anzahl = 0
    for yy in range(y - r, y + r + 1):
        for xx in range(x - r, x + r + 1):
            punkt = px[xx, yy]
            summe[0] += punkt[0]
            summe[1] += punkt[1]
            summe[2] += punkt[2]
            anzahl += 1
    return tuple(wert // anzahl for wert in summe)


# ==========================================================================
abschnitt("1. Das Raster der Anzeige - Zeilen von oben nach unten, kein erfundenes Gelaende")
# ==========================================================================
felder = [{"x": x, "y": y, "gelaende": "grasland"}
          for y in range(KANTE) for x in range(KANTE)]             # die Anzeige liefert alle 400
felder[0 * KANTE + 0]["gelaende"] = "wald"                          # Feld (0,0)
felder[3 * KANTE + 19]["gelaende"] = "nebelsee"                     # Feld (19,3)
felder[19 * KANTE + 7]["gelaende"] = "berg"                         # Feld (7,19)
raster = M.NebelseetalApp._portal_raster(felder, KANTE) or []
check("1 es entstehen 20 Zeilen", len(raster) == 20, str(len(raster)))
check("1 jede Zeile hat 20 Felder", bool(raster) and all(len(z) == 20 for z in raster), "")
check("1 das Feld (0,0) steht in Zeile 0, Spalte 0", bool(raster) and raster[0][0] == "wald",
      str(raster[0][0] if raster else "-"))
check("1 das Feld (19,3) steht in Zeile 3, Spalte 19",
      bool(raster) and raster[3][19] == "nebelsee", str(raster[3][19] if raster else "-"))
check("1 das Feld (7,19) steht in Zeile 19, Spalte 7", bool(raster) and raster[19][7] == "berg",
      str(raster[19][7] if raster else "-"))
check("1 ohne Gelaende gibt es None statt eines erfundenen Feldes",
      M.NebelseetalApp._portal_raster([{"x": 0, "y": 0, "gelaende": "wald"}], KANTE) is None, "")
check("1 eine unbekannte Gelaendeart gibt None",
      M.NebelseetalApp._portal_raster(felder[:0] + [{"x": 1, "y": 1, "gelaende": "vulkan"}],
                                      KANTE) is None, "")
check("1 das echte Weltbild der ersten Weltkarte ergibt ein volles Raster",
      all(art in gelaende.ARTEN
          for zeile in (M.NebelseetalApp._portal_raster(
              P.anzeige_raster(0, 10, ()), KANTE) or [])
          for art in zeile), "")

# ==========================================================================
abschnitt("2. Genau EIN gemaltes Bild, keine 400 Rechtecke und kein Gitter mehr")
# ==========================================================================
root, app = _app()
try:
    app._switch_view("Portal")
    root.update_idletasks()
    flaeche = app.portal_zeichenflaeche
    check("2 die Ansicht sagt, dass sie gemalt hat", getattr(app, "_portal_karte_art", "") == "gemalt",
          str(getattr(app, "_portal_karte_art", "-")))
    check("2 es liegt genau EIN Bild auf der Flaeche",
          len(flaeche.find_withtag("kartenbild")) == 1,
          str(len(flaeche.find_withtag("kartenbild"))))
    check("2 das Bild deckt die ganze Flaeche 400 x 400 ab",
          tuple(flaeche.bbox("kartenbild") or ()) == (0, 0, 400, 400),
          str(flaeche.bbox("kartenbild")))
    bild = getattr(app, "portal_kartenbild", None)
    check("2 das Bild ist 400 x 400 px (20 px je Feld, kein Rollbalken)",
          bild is not None and (bild.width(), bild.height()) == (400, 400),
          str(None if bild is None else (bild.width(), bild.height())))
    ohne_tag = [o for o in flaeche.find_all()
                if flaeche.type(o) == "rectangle" and not flaeche.gettags(o)]
    check("2 die 400 Gelaenderechtecke sind weg", ohne_tag == [], str(len(ohne_tag)))
    linien = [o for o in flaeche.find_all() if flaeche.type(o) == "line"]
    gitter = [o for o in linien if str(flaeche.itemcget(o, "fill")) == M.RASTER_LINIE]
    check("2 die 42 Gitterlinien sind weg", gitter == [], str(len(gitter)))
    check("2 die Marken der Doerfer bleiben gezeichnet (eigener Tag)",
          len(flaeche.find_withtag("portalspieler")) >= 1,
          str(len(flaeche.find_withtag("portalspieler"))))
finally:
    root.destroy()

# ==========================================================================
abschnitt("3. Bild und Rasterlage stimmen - in der Zeile UND in der Spalte")
# ==========================================================================
# Ein eigenes Raster, in dem Zeile 7 UND Spalte 5 Nebelsee sind: ein x/y-Tausch beim Malen
# wuerde die Probe an genau einer der beiden Stellen rot machen.
_raster = [["grasland"] * KANTE for _ in range(KANTE)]
for _y in range(KANTE):
    _raster[_y][5] = "nebelsee"                                     # Spalte 5
for _x in range(KANTE):
    _raster[7][_x] = "nebelsee"                                     # Zeile 7
_karte = W.karte_malen(_raster, ZELLE)
_mitte = lambda feld: (int((feld[0] + 0.5) * ZELLE), int((feld[1] + 0.5) * ZELLE))  # noqa: E731
_spalte = _mittel(_karte, *_mitte((5, 12)))                         # Nebelsee in der Spalte
_rechts = _mittel(_karte, *_mitte((6, 12)))                         # Grasland daneben
_zeile = _mittel(_karte, *_mitte((12, 7)))                          # Nebelsee in der Zeile
_unten = _mittel(_karte, *_mitte((12, 8)))                          # Grasland darunter
check("3 das Nebelsee-Feld der SPALTE ist blau (b deutlich groesser als r)",
      _spalte[2] - _spalte[0] > 30, str(_spalte))
check("3 das Feld rechts daneben ist Gras (g deutlich groesser als b)",
      _rechts[1] - _rechts[2] > 30, str(_rechts))
check("3 das Nebelsee-Feld der ZEILE ist blau (kein x/y-Tausch)",
      _zeile[2] - _zeile[0] > 30, str(_zeile))
check("3 das Feld darunter ist Gras", _unten[1] - _unten[2] > 30, str(_unten))
check("3 das Bild hat die Masse 400 x 400 px", _karte.size == (400, 400), str(_karte.size))

# ==========================================================================
abschnitt("4. Der Klick trifft dasselbe Feld wie das Bild")
# ==========================================================================
root, app = _app()
try:
    app._switch_view("Portal")
    root.update_idletasks()
    zelle = app._portal_zelle(KANTE)
    check("4 ein Feld ist 20 px breit", zelle == 20, str(zelle))
    check("4 die Feldmitte rechnet mit 0.5 (kein Versatz durch das Bild)",
          abs((3 + 0.5) * zelle - 70.0) < 1e-9, str((3 + 0.5) * zelle))
    frei = [(x, y) for x in range(KANTE) for y in range(KANTE)
            if app._bot_dorf_an(x, y, KANTE) is None and app._marsch_an(x, y, KANTE) is None]
    check("4 es gibt freie Felder", len(frei) > 10, str(len(frei)))
    probe = [frei[0], frei[len(frei) // 2], frei[-1]]
    daneben = 0
    for x, y in probe:
        px, py = int((x + 0.5) * zelle), int((y + 0.5) * zelle)     # Feldmitte in px
        if (px // zelle, py // zelle) != (x, y):                    # Klickweg der Ansicht
            daneben += 1
    check("4 die Feldmitte liegt im eigenen Feld", daneben == 0, str(probe))
    px, py = int((probe[1][0] + 0.5) * zelle), int((probe[1][1] + 0.5) * zelle)   # Feldmitte
    app._portal_klick(px // zelle, py // zelle, KANTE)              # so bindet die Ansicht
    check("4 der Klick waehlt genau dieses Feld", getattr(app, "portal_auswahl", None) == probe[1],
          str(getattr(app, "portal_auswahl", None)))
finally:
    root.destroy()

# ==========================================================================
abschnitt("5. Rueckfall ohne Malerei: 400 Felder und 42 Trennlinien wie vor D-4")
# ==========================================================================
root, app = _app()
try:
    leinwand = tk.Canvas(app.content, width=KANTE * ZELLE, height=KANTE * ZELLE,
                         bg=app.skin["bg"], highlightthickness=0)   # eigene Flaeche, kein Umbau
    felder = P.anzeige_raster(0, 10, ())
    app._portal_karte_flach(leinwand, felder, KANTE, ZELLE)
    rechtecke = [o for o in leinwand.find_all() if leinwand.type(o) == "rectangle"]
    linien = [o for o in leinwand.find_all()
              if leinwand.type(o) == "line"
              and str(leinwand.itemcget(o, "fill")) == M.RASTER_LINIE]
    check("5 der Rueckfall zeichnet 400 Felder", len(rechtecke) == 400, str(len(rechtecke)))
    check("5 der Rueckfall zeichnet 42 Trennlinien in RASTER_LINIE", len(linien) == 2 * (KANTE + 1),
          str(len(linien)))
    fuellungen = {str(leinwand.itemcget(o, "fill")).lower() for o in rechtecke}
    check("5 die Felder tragen Gelaendefarben (mehr als zwei)", len(fuellungen) >= 3,
          str(sorted(fuellungen))[:120])
finally:
    root.destroy()

# ==========================================================================
abschnitt("6. Quellwachen")
# ==========================================================================
quelle = _code(M.NebelseetalApp._render_portal)
check("6 die Ansicht laesst die Karte malen", "_portal_karte_zeichnen" in quelle, "")
check("6 sie merkt sich den Weg (gemalt/flach) fuer die Wachen", "_portal_karte_art" in quelle, "")
check("6 sie zeichnet die Gelaendefelder nicht mehr selbst (kein Gelaendeton in der Ansicht)",
      "gelaende_farbe" not in quelle, "")
check("6 der Goldrand der Auswahl bleibt in der Ansicht", "['gold']" in quelle, "")
flach = _code(M.NebelseetalApp._portal_karte_flach)
check("6 der Rueckfall benutzt die eine Trennlinien-Farbe", "RASTER_LINIE" in flach, "")
check("6 der Rueckfall zeichnet die Felder weiter selbst", "create_rectangle" in flach, "")
bild_code = _code(M.NebelseetalApp._portal_karte_bild)
check("6 das Bild kommt aus weltkarte_malerei.karte_malen", "karte_malen" in bild_code, "")
check("6 das Bild liegt bei (0, 0) mit Anker NW", "0, 0" in bild_code and "NW" in bild_code, "")
check("6 der Bildverweis bleibt am Fenster (Tk gibt ihn sonst frei)",
      "self.portal_kartenbild" in bild_code, "")
check("6 ohne Pillow faellt die Ansicht auf die flachen Felder zurueck",
      "return False" in bild_code and "_portal_karte_flach" in _code(
          M.NebelseetalApp._portal_karte_zeichnen), "")
befund("6 ehrliche Grenze: gemalt wird mit Pillow. Fehlt Pillow oder ein belegtes Gelaende, zeigt "
       "die Ansicht die flachen Felder samt Trennlinien wie vor D-4 - sie stuerzt nicht ab und "
       "erfindet kein Gelaende.", "")

sys.exit(bericht())
