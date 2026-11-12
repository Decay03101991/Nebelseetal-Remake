"""Belegbild: das Voelker-Panorama hinter der Siedlungsansicht (A-7, 12.11.2026).

Warum ein Bild und keine Behauptung: Daniel beurteilt Gestaltung mit dem Auge. Dieses Werkzeug
baut das echte Fenster, oeffnet die Siedlungskarte, macht einen Bildschirmabzug der Inhaltsflaeche
und legt ihn unter `docs/audits/` ab. Der Abzug ist das Fenster selbst - nicht nachgemalt.

WICHTIG (Pruefstand-Konventionen, Abschnitt 3d): `ImageGrab` liefert PHYSISCHE Pixel, Tk rechnet
in LOGISCHEN. Bei 125 Prozent Skalierung liegt der Abzug sonst um Faktor 1,25 daneben. Darum wird
jede Koordinate mit dem gemessenen Faktor multipliziert.

Aufruf:
    python -X utf8 tools/tafel_siedlungsansicht.py             # elfisch, 1400x900
    python -X utf8 tools/tafel_siedlungsansicht.py Trolle
Ergebnis: docs/audits/siedlungsansicht_panorama_<fraktion>_20261112.png
"""
import os
import sys
import time
import tkinter as tk

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _pfad in (ROOT, os.path.join(ROOT, "src")):
    if _pfad not in sys.path:
        sys.path.insert(0, _pfad)

import main  # noqa: E402


def _foto(widget, faktor):
    """Bildschirmabzug genau eines Widgets, Koordinaten in physischen Pixeln."""
    from PIL import ImageGrab
    x, y = widget.winfo_rootx(), widget.winfo_rooty()
    b, h = widget.winfo_width(), widget.winfo_height()
    return ImageGrab.grab(bbox=(int(x * faktor), int(y * faktor),
                               int((x + b) * faktor), int((y + h) * faktor)))


def tafel(fraktion: str) -> str:
    root = tk.Tk()
    root.geometry("1400x900+40+40")
    root.update()
    faktor = float(root.winfo_fpixels("1i")) / 96.0          # 1.0 = 100 %, 1.25 = 125 %
    app = main.NebelseetalApp(root)
    app._build_main_ui()
    app._erste_siedlung_gruenden()
    for _ in range(3):
        root.update()
        root.update_idletasks()
    siedlung = next((s for s in app.state.settlements if getattr(s, "karte", None)), None)
    if siedlung is None:
        print("keine Siedlung mit Karte")
        root.destroy()
        return ""
    app.spieler_fraktion = fraktion
    app._oeffne_siedlungskarte(siedlung)
    ende = time.time() + 4.0                                  # Bildaufbau: 120 ms nach Ruhe
    while time.time() < ende:
        root.update()
        root.update_idletasks()
        leinwand = getattr(app, "_siedlungs_leinwand", None)
        if leinwand is not None and leinwand.find_withtag("panorama"):
            break
        time.sleep(0.05)
    time.sleep(0.4)                                           # dem Fenster Zeit zum Zeichnen
    root.update()
    ziel = os.path.join(ROOT, "docs", "audits",
                        "siedlungsansicht_panorama_%s_20261112.png" % fraktion.lower())
    bild = _foto(app.content_canvas, faktor)
    bild.save(ziel)
    print("Bild: %s (%d x %d, Faktor %.2f)" % (ziel, bild.width, bild.height, faktor))
    root.destroy()
    return ziel


if __name__ == "__main__":
    tafel(sys.argv[1] if len(sys.argv) > 1 else "elfisch")
