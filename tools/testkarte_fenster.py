"""Testkarte 20 x 20 mit gemalten Kacheln - Fenster und Belastungstest (Designschritt D-3).

Was es tut
----------
Oeffnet ein echtes Tk-Fenster mit der GEMALTEN Weltkarte einer der sechs Weltkarten (Vorgabe d01,
alle sieben Gelaendearten kommen dort vor - gezaehlt, nicht behauptet), zeichnet sie als EIN Bild
und misst dabei:

* `kalt`  - die Karte zum ersten Mal malen (Kacheln entstehen, alles wird gerechnet)
* `warm`  - dieselbe Karte noch einmal (Zwischenspeicher)
* `tk`    - daraus eine Tk-Grafik bauen und auf die Leinwand setzen
* `wiederholung` - fuenf Zeichnungen hintereinander, min/mittel/max

Danach speichert es das Bild als PNG (`--bild <pfad>`) und schliesst sich (`--schliessen`).

Warum ein eigenes Fenster und nicht das Spiel
---------------------------------------------
D-3 ist ein STIL-ENTSCHEID: Daniel soll sehen, ob die flache gemalte Karte traegt. Solange er das
nicht entschieden hat, wird der Zeichner des Spiels (`_render_portal`) nicht umgebaut - das ist
D-4 und folgt erst nach seinem Urteil. Der Belastungstest hier misst denselben Weg, den das Spiel
gehen wuerde: EIN gemaltes Bild je Karte, einmal gebaut, dann nur noch gesetzt.

Aufruf
------
    .venv/Scripts/python.exe -X utf8 tools/testkarte_fenster.py --kante 48 --bild out.png
    .venv/Scripts/python.exe -X utf8 tools/testkarte_fenster.py --welt d03 --kante 64 --schliessen
"""
from __future__ import annotations

import argparse
import os
import sys
import time

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(WURZEL, "src"))

import portalraum                    # Weltkarten, Raster, Gelaendeverteilung
import weltkarte_malerei as malerei  # der Maler (Pillow, ohne tkinter)


def raster_der_welt(kennung: str) -> list:
    """Das 20 x 20-Gelaenderaster EINER Weltkarte (aus `portalraum.weltbild`)."""
    bild = portalraum.weltbild(kennung)
    return bild["raster"]


def arten_im_raster(raster) -> dict:
    """{Gelaendeart: Anzahl} - gezaehlt, damit niemand eine Art im Bild vermutet."""
    zaehlung: dict = {}
    for zeile in raster:
        for art in zeile:
            zaehlung[art] = zaehlung.get(art, 0) + 1
    return zaehlung


def messen(kennung: str, kante: int) -> dict:
    """Die Karte malen und die Zeiten messen - ohne Fenster (fuer Pruefung und Bericht)."""
    raster = raster_der_welt(kennung)
    malerei.leeren()
    beginn = time.perf_counter()
    bild = malerei.karte_malen(raster, kante)
    kalt = time.perf_counter() - beginn
    beginn = time.perf_counter()
    erneut = malerei.karte_malen(raster, kante)
    warm = time.perf_counter() - beginn
    return {"welt": kennung, "kante": kante, "raster": raster, "bild": bild,
            "kalt": kalt, "warm": warm, "gleiches_bild": erneut is bild,
            "arten": arten_im_raster(raster)}


def fenster(kennung: str, kante: int, bildpfad: str = "", schliessen: bool = False) -> dict:
    """Die Testkarte in einem echten Fenster zeigen und den Zeichenweg messen."""
    import tkinter as tk
    ergebnis = messen(kennung, kante)
    raster, bild = ergebnis["raster"], ergebnis["bild"]
    zeilen, spalten = len(raster), max(len(z) for z in raster)

    wurzel = tk.Tk()
    wurzel.title("Testkarte 20 x 20 - gemalt (D-3) - Weltkarte %s, %d px je Feld"
                 % (kennung, kante))
    wurzel.configure(bg="#0F1418")
    kopf = tk.Label(wurzel, text=("Weltkarte %s  -  %d x %d Felder, %d px je Feld  -  "
                                  "sieben Gelaendearten und Tannen, gemalt"
                                  % (kennung, spalten, zeilen, kante)),
                    fg="#DAA520", bg="#0F1418")
    kopf.pack(anchor="w", padx=10, pady=(8, 2))
    leinwand = tk.BooleanVar()
    flaeche = tk.Label(wurzel, bg="#0F1418", bd=0)
    flaeche.pack(padx=10, pady=4)

    zeiten = []
    for _ in range(5):                                   # Belastungstest: fuenfmal zeichnen
        beginn = time.perf_counter()
        from PIL import ImageTk
        grafik = ImageTk.PhotoImage(bild)                # EINE Tk-Grafik fuer die ganze Karte
        flaeche.configure(image=grafik)
        flaeche.image = grafik                           # Referenz halten (Tk gibt sonst frei)
        wurzel.update_idletasks()
        zeiten.append(time.perf_counter() - beginn)
    ergebnis.update({"tk": zeiten[0], "wiederholung": zeiten,
                     "min": min(zeiten), "mittel": sum(zeiten) / len(zeiten),
                     "max": max(zeiten), "leinwand": leinwand})
    if bildpfad:
        bild.save(bildpfad)
        ergebnis["bildpfad"] = bildpfad
    legende = tk.Frame(wurzel, bg="#0F1418")
    legende.pack(anchor="w", padx=10, pady=(0, 8))
    tk.Label(legende, text="Gelaende:", fg="#DAA520", bg="#0F1418").pack(side="left")
    for eintrag in portalraum.legende():
        tk.Label(legende, text="", bg=eintrag["farbe"], width=2).pack(side="left", padx=(6, 2))
        tk.Label(legende, text="%s %d" % (eintrag["name"], eintrag["haeufigkeit"]),
                 fg="#E8E8E8", bg="#0F1418", font=("TkDefaultFont", 8)).pack(side="left")
    if schliessen:
        wurzel.after(400, wurzel.destroy)
    wurzel.mainloop()
    ergebnis["fenster_offen"] = True
    return ergebnis


def bericht(ergebnis: dict) -> str:
    """Die Messzahlen als Text - dieselben Zahlen kommen in Register und Protokoll."""
    arten = ergebnis["arten"]
    return "\n".join([
        "Weltkarte %s, Kante %d px, %d x %d Felder"
        % (ergebnis["welt"], ergebnis["kante"], len(ergebnis["raster"]),
           len(ergebnis["raster"][0])),
        "Gelaendearten im Raster: %d - %s"
        % (len(arten), ", ".join("%s %d" % (art, zahl) for art, zahl in sorted(arten.items()))),
        "kalt  (erste Malkacheln): %.3f s" % ergebnis["kalt"],
        "warm  (Zwischenspeicher): %.6f s" % ergebnis["warm"],
        "gleiches Bildobjekt beim zweiten Abruf: %s" % ergebnis["gleiches_bild"],
        "tk    (Grafik + setzen):  %.4f s" % ergebnis.get("tk", 0.0),
        "fuenf Zeichnungen: min %.4f  mittel %.4f  max %.4f s"
        % (ergebnis.get("min", 0.0), ergebnis.get("mittel", 0.0), ergebnis.get("max", 0.0)),
        "Bild: %s" % ergebnis.get("bildpfad", "(nicht gespeichert)"),
    ])


def main() -> int:
    zerleger = argparse.ArgumentParser(description="Testkarte 20 x 20 mit gemalten Kacheln (D-3)")
    zerleger.add_argument("--welt", default="d01", help="Weltkarte (d01 bis d06), Vorgabe d01")
    zerleger.add_argument("--kante", type=int, default=48, help="Pixel je Feld, Vorgabe 48")
    zerleger.add_argument("--bild", default="", help="PNG-Pfad fuer die fertige Karte")
    zerleger.add_argument("--schliessen", action="store_true", help="Fenster nach kurzer Zeit zu")
    zerleger.add_argument("--ohne-fenster", action="store_true", help="nur malen und messen")
    args = zerleger.parse_args()
    if not malerei.verfuegbar():
        print("Pillow fehlt - ohne Pillow wird nicht gemalt (das Spiel faellt auf Farben zurueck).")
        return 2
    if args.ohne_fenster:
        ergebnis = messen(args.welt, args.kante)
        if args.bild:
            ergebnis["bild"].save(args.bild)
            ergebnis["bildpfad"] = args.bild
    else:
        ergebnis = fenster(args.welt, args.kante, args.bild, args.schliessen)
    print(bericht(ergebnis))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
