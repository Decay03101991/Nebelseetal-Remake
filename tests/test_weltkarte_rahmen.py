# -*- coding: ascii -*-
"""Wache: Weltkarte mit gemaltem Rahmen und Gelaendeton (03.11.2026, Daniels Entscheidung 22:1x).

DANIELS WORTLAUT
----------------
Die Weltkarte soll optisch anders werden - "Rahmen als Bildleiste (`main.leiste_zusammensetzen`)
UND Felder mit Gelaendeton, feiner Trennlinie, Goldrand fuer die Auswahl; Groesse und Aufbau
bleiben" (docs/AKTUELLER_STAND.md, Stand-Block 22:20).

WAS DIESE DATEI PRUEFT
----------------------
1. `gebaeude_optik.rahmen_kanten` liefert vier Randstreifen in Zielmass und meldet sauber, wenn
   kein Bild da ist (dann bleibt die Karte ohne Rahmen, statt abzustuerzen).
2. Das Gelaendekaestchen sitzt IN einem Bildrahmen: vier Bildleisten (oben, unten, links, rechts),
   die Zeichenflaeche bleibt 400 x 400 - Groesse und Aufbau unveraendert.
3. Die Felder tragen Gelaendeton OHNE harte schwarze Umrisse, das Gitter kommt als feine
   Trennlinie (`RASTER_LINIE`).
4. Die Auswahl ist GOLD (vorher blau #38BDF8) und liegt als Goldrand ueber einer dunklen Unterlage.
5. Die Klickwege bleiben: ein Feldklick waehlt dasselbe Feld wie vorher (20 px je Feld).
6. Quellwachen: `_render_portal` baut den Rahmen und benutzt die Trennlinie; ohne Pillow faellt
   die Karte auf die nackte Flaeche zurueck.

Aufruf:  python -X utf8 tests/test_weltkarte_rahmen.py
"""
from __future__ import annotations

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
import gebaeude_optik as G  # noqa: E402
import main as M  # noqa: E402

RAHMEN_PFAD = "assets/icons/gebaeude/rahmen/kachelrahmen_ruhe.png"


def _app(seed: int = 7):
    """Frische App mit Siedlung - ohne Fenster auf dem Schirm."""
    random.seed(seed)                                              # Karte reproduzierbar
    root = tk.Tk()                                                 # Tk-Wurzel
    root.withdraw()                                                # kein Fenster zeigen
    app = M.NebelseetalApp(root)                                   # die App
    app._build_main_ui()                                           # Oberflaeche aufbauen
    app._erste_siedlung_gruenden()                                 # echte Startwerte
    root.update_idletasks()                                        # rechnen lassen
    return root, app


def _code(fn) -> str:
    """Quelltext einer Funktion ohne Docstring (nur echte Anweisungen)."""
    baum = ast.parse(textwrap.dedent(inspect.getsource(fn)))       # Funktion parsen
    baum.body[0].body = [k for k in baum.body[0].body              # Docstring abtrennen
                         if not (isinstance(k, ast.Expr) and isinstance(k.value, ast.Constant)
                                 and isinstance(k.value.value, str))]
    return ast.unparse(baum)


def _karte(app):
    """Die Zeichenflaeche des Gelaendekaestchens (auch im Rahmen gefunden)."""
    def _suchen(widget):
        for kind in widget.winfo_children():
            if isinstance(kind, tk.Canvas) and int(kind.cget("width") or 0) == 400:
                return kind
            treffer = _suchen(kind)
            if treffer is not None:
                return treffer
        return None
    return _suchen(app.content)


def _rahmen(app):
    """Der Rahmen, der die Karte traegt (sein Elternrahmen ist ein Kind des Inhaltsbereichs)."""
    karte = _karte(app)
    return karte.master.master if karte is not None else None


# ==========================================================================
abschnitt("1. Die vier Randstreifen aus dem Kachelrahmen")
# ==========================================================================
teile = G.rahmen_kanten(RAHMEN_PFAD, 400, 400)                     # Rahmen fuer die Kartenmasse
check("1 vier Streifen entstehen", set(teile) >= {"oben", "unten", "links", "rechts"},
      str(sorted(teile)))
check("1 oben und unten sind 400 px breit", teile["oben"].size[0] == 400
      and teile["unten"].size[0] == 400, str(teile["oben"].size))
check("1 links und rechts sind so hoch wie das Kaestchen abzueglich der Ecken",
      teile["links"].size[1] == 400 - 2 * teile["rand"], str(teile["links"].size))
check("1 der Rand wird nicht frei erfunden, sondern aus dem Bild abgeleitet",
      teile["rand"] == 16, str(teile["rand"]))
check("1 fehlende Datei liefert ein leeres dict (kein Absturz)",
      G.rahmen_kanten("assets/gibtsnicht.png", 400, 400) == {}, "")
check("1 zu kleine Masse liefert ein leeres dict",
      G.rahmen_kanten(RAHMEN_PFAD, 20, 20) == {}, "")
# Die Ecke muss aus dem ORIGINAL stammen - sonst waere der Rahmen gemalt statt geliefert.
from PIL import Image  # noqa: E402
_quelle = Image.open(os.path.join(ROOT, RAHMEN_PFAD)).convert("RGBA")
check("1 die linke obere Ecke ist pixelgleich mit dem Original",
      list(teile["oben"].crop((0, 0, 16, 16)).getdata()) == list(_quelle.crop((0, 0, 16, 16)).getdata()),
      "")

# ==========================================================================
abschnitt("2. Das Kaestchen sitzt in einem Bildrahmen, die Masse bleiben")
# ==========================================================================
root, app = _app()
try:
    app._switch_view("Portal")                                     # die Ansicht bauen
    root.update_idletasks()
    karte = _karte(app)
    rahmen = _rahmen(app)
    check("2 die Zeichenflaeche ist 400 x 400 wie bisher",
          karte is not None and int(karte.cget("width")) == 400 and int(karte.cget("height")) == 400,
          str(karte.cget("width") if karte else "-"))
    check("2 sie sitzt in einem eigenen Traeger", rahmen is not None and rahmen is not app.content,
          str(rahmen))
    leisten = [k for k in rahmen.winfo_children() if isinstance(k, tk.Label)] if rahmen else []
    check("2 vier Bildleisten umrahmen sie", len(leisten) == 4, "%d Leisten" % len(leisten))
    check("2 jede Leiste traegt ein Bild",
          all(str(k.cget("image")) for k in leisten), str([str(k.cget("image")) for k in leisten]))
    check("2 der Rahmen haelt seine Bilder (sonst raeumt Tk sie weg)", bool(getattr(rahmen, "bilder", {}))
          if rahmen is not None else False, "")
    check("2 die Bildrahmen sind zwischengespeichert",
          bool(getattr(app, "_kartenrahmen_cache", {})), str(len(getattr(app, "_kartenrahmen_cache", {}))))
finally:
    root.destroy()

# ==========================================================================
abschnitt("3. Gelaendeton und feine Trennlinie statt harter schwarzer Kaesten")
# ==========================================================================
root, app = _app()
try:
    app._switch_view("Portal")
    root.update_idletasks()
    karte = _karte(app)
    rechtecke = [o for o in karte.find_all() if karte.type(o) == "rectangle"]
    umrisse = {str(karte.itemcget(o, "outline")).lower() for o in rechtecke}
    check("3 kein Feld traegt einen schwarzen Umriss mehr", "#111111" not in umrisse, str(sorted(umrisse)))
    linien = [o for o in karte.find_all() if karte.type(o) == "line"]
    check("3 das Gitter besteht aus feinen Linien", len(linien) >= 20, "%d Linien" % len(linien))
    gitter = [o for o in linien if str(karte.itemcget(o, "fill")) == M.RASTER_LINIE]
    check("3 die Trennlinien tragen die eine Farbe aus dem Code",
          len(gitter) == 2 * (20 + 1), "%d von %d Linien" % (len(gitter), len(linien)))
    fuellungen = {str(karte.itemcget(o, "fill")).lower() for o in rechtecke}
    check("3 die Felder tragen Gelaendefarben (mehr als zwei)",
          len(fuellungen) >= 3, str(sorted(fuellungen))[:120])
finally:
    root.destroy()

# ==========================================================================
abschnitt("4. Die Auswahl ist GOLD, nicht mehr blau")
# ==========================================================================
root, app = _app()
try:
    app._switch_view("Portal")
    root.update_idletasks()
    app.portal_auswahl = (3, 4)                                    # ein Feld auswaehlen
    app._render_view()                                             # neu zeichnen
    root.update_idletasks()
    karte = _karte(app)
    umrisse = [str(karte.itemcget(o, "outline")).lower()
               for o in karte.find_all() if karte.type(o) == "rectangle"]
    check("4 es gibt einen Goldrand", app.skin["gold"].lower() in umrisse, str(sorted(set(umrisse))))
    check("4 der alte blaue Rand ist verschwunden", "#38bdf8" not in umrisse, "")
    check("4 der Goldrand liegt auf einer dunklen Unterlage", "#1b0d06" in umrisse, "")
    # S-4 (08.11.2026): die Zeile heisst nicht mehr "Angewaehltes Feld", sondern nennt Feld,
    # Gelaende, Weltkarte UND den Status mit Grund ("ist frei" / "ist belegt: X"). Die Zusage
    # bleibt dieselbe - es gibt eine Zeile unter der Karte, die DIESES Feld nennt.
    texte = [str(w.cget("text")) for w in app.content.winfo_children()
             if isinstance(w, tk.Label) and "x=3" in str(w.cget("text"))
             and "y=4" in str(w.cget("text"))]
    check("4 die Zeile unter der Karte nennt das Feld", bool(texte), str(texte)[:80])
finally:
    root.destroy()

# ==========================================================================
abschnitt("5. Der Klick waehlt dasselbe Feld wie vorher (20 px je Feld)")
# ==========================================================================
root, app = _app()
try:
    app._switch_view("Portal")
    root.update_idletasks()
    zelle = app._portal_zelle(20)
    check("5 ein Feld ist weiter 20 px breit", zelle == 20, str(zelle))
    frei = next(((x, y) for x in range(20) for y in range(20)
                 if app._bot_dorf_an(x, y, 20) is None
                 and app._marsch_an(x, y, 20) is None), None)
    check("5 es gibt ein freies Feld", frei is not None, str(frei))
    app._portal_klick(int(frei[0]), int(frei[1]), 20)              # Feldindex, nicht Pixel (so bindet die Ansicht)
    check("5 der Klick waehlt genau dieses Feld",
          getattr(app, "portal_auswahl", None) == (frei[0], frei[1]),
          str(getattr(app, "portal_auswahl", None)))
finally:
    root.destroy()

# ==========================================================================
abschnitt("6. Quellwachen")
# ==========================================================================
quelle = _code(M.NebelseetalApp._render_portal)                     # echter Code ohne Docstring
check("6 die Ansicht baut den Bildrahmen", "_kartenrahmen_bauen" in quelle, "")
check("6 sie benutzt die eine Trennlinien-Farbe", "RASTER_LINIE" in quelle, "")
check("6 die Auswahl nimmt die Goldfarbe des Skins", "['gold']" in quelle, "")  # ast.unparse schreibt einfache Anfuehrungszeichen
check("6 kein alter schwarzer Feldumriss mehr", "outline=\\\"#111111\\\"" not in quelle, "")
check("6 kein alter blauer Auswahlrand mehr", "#38BDF8" not in quelle, "")
check("6 die Zeichenflaeche haengt an einer EINEN Stelle fuer Pruefungen",
      "self.portal_zeichenflaeche" in quelle, "")
check("6 der Rahmen faellt ohne Bild auf die nackte Flaeche zurueck",
      "_rahmen_flaeche is None" in quelle, "")
check("6 das Rahmenwerkzeug steht in gebaeude_optik", callable(getattr(G, "rahmen_kanten", None)), "")
befund("6 ehrliche Grenze: der Rahmen kommt aus dem vorhandenen Kachelrahmen (64 x 64, C2-Lieferung) "
       "und wird gekachelt - ein eigener breiter Kartenrahmen ist eine Bildlieferung, keine Codefrage. "
       "Ohne Pillow oder ohne Rahmendatei steht das Kaestchen wie bisher ohne Rahmen.", "")

sys.exit(bericht())
