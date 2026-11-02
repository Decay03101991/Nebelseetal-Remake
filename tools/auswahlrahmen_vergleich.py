# -*- coding: ascii -*-
"""Sichtvergleich des Auswahlrahmens auf der Siedlungskarte - Register 130 (02.11.2026).

Die Uebergabe verlangt einen SICHTVERGLEICH als Kontaktblatt unter `docs/audits/`: der gelieferte
C2-Rahmen (`kachelrahmen_auswahl.png`) soll den bisher gezeichneten goldenen Rahmen
(`karten_optik_fein.auswahl_plan_fein`, astra "Siedlung 3") ersetzen. Dieses Werkzeug zeigt drei
Fassungen DESSELBEN Renderers auf DEMSELBEN Feld:

  A  ruhige Karte, kein Feld gewaehlt (Vergleichsbasis)
  B  BISHER: gezeichneter Goldrahmen (das Bild fuer die Auswahl ist absichtlich abgeschaltet)
  C  NEU: gelieferter C2-Rahmen, volle Deckkraft

Aufgenommen wird die echte Zeichenflaeche (`main._zeichne_siedlungskarte`) als Bildschirmfoto
(Pillow `ImageGrab`), nicht nachgemalt - nur so ist der Vergleich ein Beleg. Jede Fassung bekommt
ein EIGENES Fenster (Toplevel) in fester Groesse: im Hauptfenster wuerde die Karte zusammengedrueckt.

Aufruf:  python -X utf8 tools/auswahlrahmen_vergleich.py
Ergebnis: docs/audits/auswahlrahmen_vergleich_<JJJJMMTT>.png
"""
from __future__ import annotations

import os
import sys
import time
import tkinter as tk

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # Projektwurzel
for _pfad in (ROOT, os.path.join(ROOT, "src")):                     # Projekt und src importierbar
    if _pfad not in sys.path:
        sys.path.insert(0, _pfad)

import main  # noqa: E402 - erst nach dem Suchpfad

HEADER = 28            # Hoehe der Beschriftungszeile je Bild
BG = "#17212B"         # dunkler Grund wie die Karte (Tk-Farbe)
BG_RGB = (23, 33, 43)  # derselbe Ton fuer Pillow


def _foto(canvas):
    """Bildschirmfoto genau der Zeichenflaeche als Pillow-Bild."""
    from PIL import ImageGrab
    x = canvas.winfo_rootx()
    y = canvas.winfo_rooty()
    breite = canvas.winfo_width()
    hoehe = canvas.winfo_height()
    return ImageGrab.grab(bbox=(x, y, x + breite, y + hoehe))


def _tafel(bild, beschriftung):
    """Bild mit einer Beschriftungszeile darueber."""
    from PIL import Image, ImageDraw
    tafel = Image.new("RGB", (bild.width, bild.height + HEADER), BG_RGB)
    tafel.paste(bild.convert("RGB"), (0, HEADER))
    ImageDraw.Draw(tafel).text((8, 2), beschriftung, fill=(226, 199, 125))
    return tafel


def _aufnehmen(app, siedlung, feld, beschriftung, rahmen_lieferant):
    """Eine Fassung in einem eigenen Fenster zeichnen und als Tafel zurueckgeben."""
    app._lade_kachelrahmen = rahmen_lieferant      # Bildquelle fuer diese Fassung
    app.karten_feld = feld                         # gewaehltes Feld (None = keine Auswahl)
    fenster = tk.Toplevel(app.root)
    fenster.geometry("720x720+40+40")              # feste Groesse: Karte 658 x 658 + Rand
    flaeche = tk.Frame(fenster, bg=BG)
    flaeche.pack(anchor="nw")
    app._zeichne_siedlungskarte(siedlung, siedlung.karte, eltern=flaeche)
    fenster.update_idletasks()
    fenster.update()
    time.sleep(0.5)                                # dem Fenster Zeit zum Zeichnen geben
    tafel = _tafel(_foto(app.karten_canvas), beschriftung)
    fenster.destroy()
    return tafel


def main_() -> int:
    root = tk.Tk()
    root.withdraw()                                # Hauptfenster bleibt unsichtbar
    app = main.NebelseetalApp(root)
    app._build_main_ui()
    app._erste_siedlung_gruenden()
    siedlung = app.state.settlements[-1]
    feld = 12 if len(siedlung.karte["raster"]) > 12 else 0
    echt = app._lade_kachelrahmen

    def ohne_auswahlbild(art="ruhe", px=64):
        """Ruherahmen normal, Auswahlbild absichtlich NICHT liefern -> gezeichnete Fassung."""
        return None if str(art) == "auswahl" else echt(art, px)

    tafeln = [
        _aufnehmen(app, siedlung, None, "A  ohne Auswahl (Basis)", echt),
        _aufnehmen(app, siedlung, feld, "B  bisher: gezeichneter Goldrahmen (astra)", ohne_auswahlbild),
        _aufnehmen(app, siedlung, feld, "C  neu: gelieferter C2-Rahmen, 100 Prozent", echt),
    ]

    from PIL import Image, ImageDraw
    breite = sum(t.width for t in tafeln) + 12
    hoehe = max(t.height for t in tafeln) + 34
    blatt = Image.new("RGB", (breite, hoehe), BG_RGB)
    ImageDraw.Draw(blatt).text((6, 8), "Auswahlrahmen Siedlungskarte - Feld %d, Vergleich %s"
                               % (feld, time.strftime("%d.%m.%Y")), fill=(255, 255, 255))
    x = 0
    for tafel in tafeln:
        blatt.paste(tafel, (x, 26))
        x += tafel.width + 6
    ziel = os.path.join(ROOT, "docs", "audits", "auswahlrahmen_vergleich_%s.png"
                        % time.strftime("%Y%m%d"))
    blatt.save(ziel)
    print("Kontaktblatt geschrieben:", ziel, blatt.size)
    root.destroy()
    return 0


if __name__ == "__main__":
    sys.exit(main_())
