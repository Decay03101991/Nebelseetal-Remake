"""Belegbild: die Elfen-Gebaeudebilder in der Einzelansicht (A-8, 12.11.2026).

Daniels Entscheidung F-44 (Register 502): die drei gelieferten Elfen-Gebaeude gehoeren in die
Einzelansicht des jeweiligen Gebaeudes. Dieses Werkzeug oeffnet die Ansicht im echten Fenster und
macht einen Bildschirmabzug der Inhaltsflaeche - Beleg statt Behauptung.

DPI-Regel (Pruefstand-Konventionen 3d): `ImageGrab` liefert physische Pixel, Tk logische. Jede
Koordinate wird mit dem gemessenen Faktor multipliziert.

Aufruf:
    python -X utf8 tools/tafel_einzelansicht.py            # Forschung (Bibliothek)
    python -X utf8 tools/tafel_einzelansicht.py Kaserne    # Kriegerakademie
Ergebnis: docs/audits/einzelansicht_<ansicht>_20261112.png
"""
import os
import re
import sys
import time
import tkinter as tk

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _pfad in (ROOT, os.path.join(ROOT, "src")):
    if _pfad not in sys.path:
        sys.path.insert(0, _pfad)

import main  # noqa: E402


def _foto(widget, faktor):
    """Bildschirmabzug eines Widgets, Koordinaten in physischen Pixeln."""
    from PIL import ImageGrab
    x, y = widget.winfo_rootx(), widget.winfo_rooty()
    b, h = widget.winfo_width(), widget.winfo_height()
    return ImageGrab.grab(bbox=(int(x * faktor), int(y * faktor),
                               int((x + b) * faktor), int((y + h) * faktor)))


def aufnehmen(ansicht: str) -> str:
    root = tk.Tk()
    root.geometry("1400x900+40+40")
    root.update()
    faktor = float(root.winfo_fpixels("1i")) / 96.0
    app = main.NebelseetalApp(root)
    app._build_main_ui()
    app._erste_siedlung_gruenden()
    for _ in range(3):
        root.update()
        root.update_idletasks()
    siedlung = next((s for s in app.state.settlements if getattr(s, "karte", None)), None)
    if siedlung is not None:
        app.state.aktive_siedlung_id = siedlung.id
        app.karten_siedlung = siedlung
    app._switch_view(ansicht)
    for _ in range(4):                              # Story-Overlay schliessen: es verdunkelt die Ansicht
        root.update()
        root.update_idletasks()
        if not app._overlay_offen():
            break
        app._overlay_schliessen()
    ende = time.time() + 4.0
    while time.time() < ende:                       # Hintergrund wird 120 ms nach Ruhe gebaut
        root.update()
        root.update_idletasks()
        if getattr(app, "_hintergrund_flaeche", None) is not None:
            break
        time.sleep(0.05)
    time.sleep(0.6)
    root.update()
    name = re.sub(r"[^a-z0-9]+", "_", ansicht.lower()).strip("_")
    ziel = os.path.join(ROOT, "docs", "audits", "einzelansicht_%s_20261112.png" % name)
    _foto(app.content_canvas, faktor).save(ziel)
    print("Bild: %s (Faktor %.2f, Flaeche %dx%d)" % (
        ziel, faktor, app.content_canvas.winfo_width(), app.content_canvas.winfo_height()))
    root.destroy()
    return ziel


if __name__ == "__main__":
    aufnehmen(sys.argv[1] if len(sys.argv) > 1 else "Forschung")
