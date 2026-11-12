"""Belegbilder zum DPI-Umbau (F-51, Register 538/543): weich gegen scharf.

Daniel entscheidet am Bild, ob der Umbau gut aussieht. Dieses Werkzeug baut das ECHTE Fenster mit
der Siedlungskarte und legt einen Bildschirmabzug ab - nicht nachgemalt.

Zwei Laeufe, weil DPI-Bewusstsein prozessweit gilt und sich nicht zuruecknehmen laesst:

    python -X utf8 tools/tafel_dpi_vergleich.py unaware   -> dpi_vorher_weich_20261112.png
    python -X utf8 tools/tafel_dpi_vergleich.py aware     -> dpi_nachher_scharf_20261112.png

Der Abzugsfaktor ist im BEWUSSTEN Prozess 1,0 (Tk-Pixel = Bildpunkt), im unbewussten 1,25
(Windows vergroessert das ganze Fenster). Wer hier immer 1,25 nimmt, schneidet im bewussten Lauf
ein Viertel des Fensters ab - genau der Fehler aus Abschnitt 5 der Uebergabe 39.
"""
import os
import sys
import time

MODUS = sys.argv[1] if len(sys.argv) > 1 else "aware"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _pfad in (ROOT, os.path.join(ROOT, "src")):
    if _pfad not in sys.path:
        sys.path.insert(0, _pfad)

import main  # noqa: E402

BEWUSST = False
if MODUS == "aware":
    BEWUSST = main.dpi_bewusst_machen()

import tkinter as tk  # noqa: E402


def _foto(widget, faktor):
    from PIL import ImageGrab
    x, y = widget.winfo_rootx(), widget.winfo_rooty()
    b, h = widget.winfo_width(), widget.winfo_height()
    return ImageGrab.grab(bbox=(int(x * faktor), int(y * faktor),
                                int((x + b) * faktor), int((y + h) * faktor)))


def _schirm_faktor(root):
    """Der Faktor zwischen Tk-Pixel und Bildpunkt - GEMESSEN, nicht geraten.

    Zwei Wege, die beide NICHT funktionieren (Register 543, 12.11.2026 nachgemessen):
      * `winfo_fpixels('1i')` meldet im unbewussten Prozess 96 dpi (Faktor 1,0), obwohl Windows
        das Fenster um 1,25 streckt;
      * `GetDpiForWindow` und `GetDpiForMonitor` melden fuer ein unbewusstes Fenster ebenfalls 96.
    Richtig ist der Vergleich der physischen Schirmgroesse mit der, die Tk sieht:
        GetDeviceCaps(GetDC(0), DESKTOPHORZRES) / winfo_screenwidth()
    Bewusst: 1920 / 1920 = 1,0. Unbewusst: 1920 / 1536 = 1,25 (gemessen).
    """
    try:
        import ctypes
        hdc = ctypes.windll.user32.GetDC(0)
        phys = ctypes.windll.gdi32.GetDeviceCaps(hdc, 118)          # DESKTOPHORZRES
        log = int(root.winfo_screenwidth())
        if phys and log:
            return float(phys) / float(log)
    except Exception:                                               # noqa: BLE001
        pass
    return max(1.0, float(root.winfo_fpixels("1i")) / 96.0)


def lauf():
    root = tk.Tk()
    root.geometry("1400x900+40+40")
    root.update()
    faktor = _schirm_faktor(root)
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
    app._oeffne_siedlungskarte(siedlung)
    ende = time.time() + 4.0                                   # Bildaufbau: 120 ms nach Ruhe
    while time.time() < ende:
        root.update()
        root.update_idletasks()
    flaeche = app.content_canvas
    bild = _foto(flaeche, faktor)
    name = "dpi_nachher_scharf_20261112.png" if BEWUSST else "dpi_vorher_weich_20261112.png"
    ziel = os.path.join(ROOT, "docs", "audits", name)
    bild.save(ziel)
    print("MODUS=%s bewusst=%s faktor=%.3f k=%.4f fenster=%dx%d flaeche=%dx%d -> %s"
          % (MODUS, BEWUSST, faktor, app.dpi_k, root.winfo_width(), root.winfo_height(),
             flaeche.winfo_width(), flaeche.winfo_height(), ziel))
    print("Bildgroesse %dx%d px" % (bild.size[0], bild.size[1]))
    root.destroy()
    return ziel


lauf()
