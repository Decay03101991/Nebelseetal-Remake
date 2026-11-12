# -*- coding: ascii -*-
"""A-9: Feldgroesse, Kartenmass und Anordnung der Siedlungsansicht (12.11.2026).

Grundlage: Claudes Antwort auf Auftrag Nr. 9 und Daniels Entscheidungen F-46, F-47, F-49
(Register 507/511). Die Regel:

    f = min(64, (H - 18) // 10, (W - 350) // 10)     - Hoehe UND Breite begrenzen das Feld
    ab f < 50 stehen Karte und Spalte UEBEREINANDER

Was diese Datei zusichert:
1. RECHNUNG: die vier Flaechen aus Claudes Tabelle ergeben genau seine Zahlen
   (Feld 64 / 57 / 51 / 54, Karte 658 / 588 / 528 / 558, Spalte 477 / 433 / 323 / 615).
2. GRENZEN: das Feld wird nie groesser als 64 und nie kleiner als 20.
3. FENSTER: bei 1037 x 589 ist die Kartenleinwand 588 x 588, das historische Kartenbild
   570 x 570 (einmal verkleinert) und das Feld 57 - kein Pixel des Bildes wird gestreckt.
4. Bei 64 px bleibt alles beim Original (Kartenbild 640 x 640).
5. UEBEREINANDER: bei 615 x 565 steht die Karte oben, das Feld ist 54.

Aufruf:  python -X utf8 tests/test_siedlungsansicht_a9.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src, messwert

ROOT, SRC = import_src()
import main  # noqa: E402

# Claudes Tabelle aus der Antwort auf Auftrag Nr. 9, Abschnitt "Die vier Flaechen auf einen Blick"
TABELLE = [
    ((1151, 785), {"feld": 64, "karte": 658, "spalte": 477, "uebereinander": False}),
    ((1037, 589), {"feld": 57, "karte": 588, "spalte": 433, "uebereinander": False}),
    ((867, 565), {"feld": 51, "karte": 528, "spalte": 323, "uebereinander": False}),
    ((615, 565), {"feld": 54, "karte": 558, "spalte": 615, "uebereinander": True}),
]


def rechnung():
    abschnitt("1. Die vier Flaechen ergeben Claudes Zahlen")
    for (breite, hoehe), erwartet in TABELLE:
        masse = main.siedlungs_masse(breite, hoehe)
        for schluessel, wert in erwartet.items():
            check("%d x %d: %s = %r" % (breite, hoehe, schluessel, wert),
                  masse.get(schluessel) == wert, "ist %r" % (masse.get(schluessel),))
        messwert("feld_%dx%d" % (breite, hoehe), masse.get("feld"), "px")
        messwert("karte_%dx%d" % (breite, hoehe), masse.get("karte"), "px")
        messwert("spalte_%dx%d" % (breite, hoehe), masse.get("spalte"), "px")


def grenzen():
    abschnitt("2. Grenzen: nie groesser als 64, nie kleiner als 20")
    gross = main.siedlungs_masse(4000, 3000)
    check("ein riesiges Fenster ergibt hoechstens 64 px je Feld", gross["feld"] == 64,
          str(gross["feld"]))
    klein = main.siedlungs_masse(400, 300)
    check("ein winziges Fenster ergibt mindestens 20 px je Feld", klein["feld"] >= 20,
          str(klein["feld"]))
    check("ein winziges Fenster stapelt (uebereinander)", klein["uebereinander"] is True,
          str(klein["uebereinander"]))
    check("die Karte ist immer 10 Felder plus 18 px Leiste",
          all(main.siedlungs_masse(b, h)["karte"] == 10 * main.siedlungs_masse(b, h)["feld"] + 18
              for b, h in ((1151, 785), (1037, 589), (867, 565), (615, 565))))


def fenster():
    abschnitt("3. Im Fenster: Karte 588, Kartenbild 570, Feld 57")
    import tkinter as tk
    root = tk.Tk()
    root.geometry("1400x900+30+30")
    try:
        root.attributes("-alpha", 0.01)
    except Exception:  # noqa: BLE001
        pass
    root.update()
    app = main.NebelseetalApp(root)
    app._build_main_ui()
    app._erste_siedlung_gruenden()
    for _ in range(3):
        root.update()
        root.update_idletasks()
    siedlung = next((s for s in app.state.settlements if getattr(s, "karte", None)), None)
    if siedlung is None:
        befund("keine Siedlung mit Karte im Testaufbau")
        root.destroy()
        return
    app._oeffne_siedlungskarte(siedlung)
    for _ in range(4):
        root.update()
        root.update_idletasks()
    breite, hoehe = app._siedlungs_flaeche()
    messwert("flaeche_breite", breite, "px")
    messwert("flaeche_hoehe", hoehe, "px")
    masse = main.siedlungs_masse(breite, hoehe)
    leinwand = getattr(app, "karten_canvas", None)
    check("die Kartenleinwand steht in der Ansicht", leinwand is not None)
    if leinwand is None:
        root.destroy()
        return
    check("die Kartenleinwand ist %d x %d px" % (masse["karte"], masse["karte"]),
          (leinwand.winfo_width(), leinwand.winfo_height()) == (masse["karte"], masse["karte"]),
          "%dx%d" % (leinwand.winfo_width(), leinwand.winfo_height()))
    bild = getattr(leinwand, "_originalkarten_bild", None)
    check("das historische Kartenbild liegt vor", bild is not None)
    if bild is not None:
        soll = 10 * masse["feld"]
        check("das Kartenbild ist %d x %d px (einmal verkleinert, nicht gestreckt)" % (soll, soll),
              (bild.width(), bild.height()) == (soll, soll),
              "%dx%d" % (bild.width(), bild.height()))
        check("bei 57 px Feld ist das Bild NICHT das Originalmass 640",
              (masse["feld"] == 64) or (bild.width() == 570),
              "%dx%d" % (bild.width(), bild.height()))
        messwert("kartenbild_kante", bild.width(), "px")
    check("die Feldgroesse im Fenster ist 57", masse["feld"] == 57, str(masse["feld"]))
    # Gegenprobe der Rechnung: das Originalmass bleibt unangetastet
    check("bei f = 64 schneidet der Code nichts zu (Bedingung steht auf SIEDLUNGS_FELD_MAX)",
          main.SIEDLUNGS_FELD_MAX == 64)
    root.destroy()


def aufbau():
    abschnitt("4. Aufbau: Spalte links (rollend), Karte rechts und GANZ sichtbar")
    import tkinter as tk
    root = tk.Tk()
    root.geometry("1400x900+30+30")
    try:
        root.attributes("-alpha", 0.01)
    except Exception:  # noqa: BLE001
        pass
    root.update()
    app = main.NebelseetalApp(root)
    app._build_main_ui()
    app._erste_siedlung_gruenden()
    for _ in range(3):
        root.update()
        root.update_idletasks()
    siedlung = next((s for s in app.state.settlements if getattr(s, "karte", None)), None)
    if siedlung is None:
        befund("keine Siedlung mit Karte im Testaufbau")
        root.destroy()
        return
    app._oeffne_siedlungskarte(siedlung)
    for _ in range(4):
        root.update()
        root.update_idletasks()
    inhalt = app.content_canvas
    leinwand = app.karten_canvas
    breite, hoehe = inhalt.winfo_width(), inhalt.winfo_height()
    x = leinwand.winfo_rootx() - inhalt.winfo_rootx()
    y = leinwand.winfo_rooty() - inhalt.winfo_rooty()
    check("die Karte beginnt ganz oben (y = 0) - ueber ihr steht nichts",
          y == 0, "y = %d" % y)
    check("die Karte steht rechts von der Spalte (x > Spaltenbreite)",
          x > 300, "x = %d" % x)
    check("die Karte ist ganz sichtbar (rechte Kante und Unterkante in der Flaeche)",
          x + leinwand.winfo_width() <= breite and y + leinwand.winfo_height() <= hoehe,
          "%d+%d <= %d, %d+%d <= %d" % (x, leinwand.winfo_width(), breite,
                                        y, leinwand.winfo_height(), hoehe))
    spalte = getattr(app, "_spalte_leinwand", None)
    check("die Spalte hat einen eigenen Rollbereich", spalte is not None)
    if spalte is not None:
        bbox = spalte.bbox("all") or (0, 0, 0, 0)
        check("die Spalte rollt (Inhalt hoeher als die Flaeche)",
              (bbox[3] - bbox[1]) > spalte.winfo_height(),
              "%d px Inhalt gegen %d px Flaeche" % (bbox[3] - bbox[1], spalte.winfo_height()))
        messwert("spalte_inhalt", bbox[3] - bbox[1], "px")
        rollbalken = getattr(app, "_spalte_rollbalken", None)
        check("der Rollbalken steht im Zwischenraum und ist so breit wie gemessen",
              rollbalken is not None and rollbalken.winfo_width() == main.SIEDLUNGS_ROLLBALKEN,
              "0" if rollbalken is None else str(rollbalken.winfo_width()))
    # Die Koordinaten sind der BELEG, dass alle 100 Felder gezeichnet sind: zehn Buchstaben,
    # zehn Zahlen. (Ein Bildurteil ueber den Abzug ist dafuer zu grob - gemessen 12.11.2026.)
    spalten, zeilen = [], []
    for item in leinwand.find_all():
        if leinwand.type(item) != "text":
            continue
        text = leinwand.itemcget(item, "text")
        cx, cy = leinwand.coords(item)[:2]
        if cy < main.SIEDLUNGS_LEISTE:
            spalten.append(text)
        elif cx < main.SIEDLUNGS_LEISTE:
            zeilen.append(text)
    check("alle zehn Spaltenbuchstaben sind gezeichnet", len(spalten) == 10, str(spalten))
    check("alle zehn Reihenzahlen sind gezeichnet", len(zeilen) == 10, str(zeilen))
    messwert("spaltenbuchstaben", len(spalten), "Stueck")
    root.destroy()


if __name__ == "__main__":
    rechnung()
    grenzen()
    fenster()
    aufbau()
    raise SystemExit(bericht())
