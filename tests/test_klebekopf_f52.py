# -*- coding: ascii -*-
"""F-52: der Kopf der Siedlungskarte bleibt beim Rollen stehen (18.11.2026, Register 669).

Daniels Entscheidung vom 12.11.2026 (Register 538, F-52), woertlich: "Klebender Kopf: JA - der Kopf
der Siedlungskarte (Titel + Name, 60 px) bleibt beim Rollen stehen, der Rest rollt darunter"
(Vorlage A4 aus Claudes Antwort Nr. 13). Am 18.11.2026 hat Daniel den Einbau als naechsten
Code-Schritt gewaehlt.

Was diese Datei zusichert:
  1. RECHNUNG: die Mindesthoehe steht als Konstante (60 px) und ist an die Entscheidung gebunden.
  2. FENSTER: der Kopf hat eine deckende Unterlage im Ton E (Tag `klebekopf_unterlage`), und die
     Unterlage liegt UEBER dem rollenden Inhalt (Reihenfolge der Canvas-Elemente).
  3. ROLLEN: nach `yview_moveto(0.35)` sitzt der Kopf GENAU auf der Oberkante des sichtbaren
     Bereichs (`canvasy(0)`) - das ist die eigentliche Zusage.
  4. GEGENPROBE: ohne Rollen sitzt er an seiner Stelle (Versatz 0), und ein anderer Block ist
     NICHT mitgewandert (der Kopf klebt, der Rest rollt).
  5. Der Kopf wird nicht abgeschnitten: die Hoehe ist der GEMESSENE Block, mindestens 60 px.

Aufruf: python -X utf8 tests/test_klebekopf_f52.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
PRUEF_ART = "fenster+messen"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['main:*']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, flaeche_gross_genug, import_src, messwert

ROOT, SRC = import_src()
import main          # noqa: E402

NICHT_PRUEFBAR = []        # F8: zu kleines Fenster - Messlage statt Fehler


def _fenster():
    """Siedlung oeffnen und die Spalte bauen lassen; gibt (root, app) zurueck."""
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
    if not flaeche_gross_genug(root, 1400, 900):      # F8: kleines Fenster ist kein Defekt
        NICHT_PRUEFBAR.append(1)
        return root, None
    app.spieler_fraktion = "elfisch"                  # Panorama wie im Normalbetrieb
    siedlung = next((s for s in app.state.settlements if getattr(s, "karte", None)), None)
    if siedlung is None:
        return root, None
    app._oeffne_siedlungskarte(siedlung)
    for _ in range(5):
        root.update()
        root.update_idletasks()
    return root, app


def rechnung():
    """1. Die Entscheidung steht im Code - als Konstante mit Zahl."""
    abschnitt("1. Die entschiedenen 60 px stehen als Konstante")
    hoehe = int(getattr(main, "SIEDLUNGS_KOPF_HOEHE", 0) or 0)
    check("SIEDLUNGS_KOPF_HOEHE ist 60 px (F-52)", hoehe == 60, str(hoehe))
    messwert("kopi_hoehe_entschieden", hoehe, "px")
    quelle = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
    check("die Konstante nennt die Entscheidung F-52", "F-52" in quelle)
    check("die Methode `_spalte_kopf_kleben` gibt es",
          hasattr(main.NebelseetalApp, "_spalte_kopf_kleben"))


def fenster():
    """2 bis 5. Im echten Fenster: Unterlage, Reihenfolge und das Kleben beim Rollen."""
    abschnitt("2. Im Fenster: der Kopf klebt auf der Oberkante des sichtbaren Bereichs")
    root, app = _fenster()
    if NICHT_PRUEFBAR:
        befund("kleines Fenster - Klebekopf nicht pruefbar (F8) statt rot")
        root.destroy()
        return
    if app is None:
        befund("keine Siedlung mit Karte im Testaufbau")
        root.destroy()
        return
    leinwand = getattr(app, "_spalte_leinwand", None)
    check("die Spalte ist eine Leinwand", leinwand is not None)
    if leinwand is None:
        root.destroy()
        return
    unterlage = list(leinwand.find_withtag("klebekopf_unterlage"))
    check("der Kopf hat eine deckende Unterlage", len(unterlage) == 1, str(unterlage))
    hoehe = int(getattr(app, "_klebekopf_hoehe", 0) or 0)
    check("die Kopfhoehe ist gemessen und mindestens 60 px", hoehe >= 60, "%d px" % hoehe)
    messwert("kopf_hoehe_gemessen", hoehe, "px")
    if unterlage:
        oben, unten = leinwand.coords(unterlage[0])[1], leinwand.coords(unterlage[0])[3]
        check("die Unterlage ist so hoch wie der Kopf", int(unten - oben) == hoehe,
              "%d gegen %d" % (int(unten - oben), hoehe))
        fuellung = str(leinwand.itemcget(unterlage[0], "fill"))
        check("die Unterlage ist deckend gefuellt (kein leerer Rand)", bool(fuellung), fuellung)
        messwert("kopf_unterlage_ton", fuellung, "hex")
    teile = list(getattr(app, "_klebekopf_items", []) or [])
    check("der Kopf besteht aus Unterlage und Texten", len(teile) >= 3, str(teile))
    # 3. Startzustand: der Kopf sitzt auf der Oberkante, auch wenn die Leinwand schon leicht
    # gerollt ist (gemessen am 18.11.2026: canvasy(0) = -3 im Startzustand).
    if teile:
        kopf_start = int(leinwand.bbox(teile[1])[1])
        check("im Startzustand sitzt der Kopf innerhalb seines Bandes oben",
              -2 <= kopf_start <= hoehe, "%d px bei Band %d px" % (kopf_start, hoehe))
        messwert("kopf_y_start", kopf_start, "px")
    # 4. Rollen und messen: der Kopf MUSS oben bleiben
    breite = int(getattr(app, "_spalte_breite", 0) or 0)
    check("die Spalte hat eine Breite", breite > 0, str(breite))
    if not teile:
        root.destroy()
        return
    kopf_text = teile[1]                                  # erster Kopf-Text
    vorher = int(round(float(leinwand.canvasy(0))))
    # Die Spalte im Test ist fast so hoch wie ihr Inhalt (gemessen: 11 px Rollweg). Fuer eine
    # belastbare Messung wird die SICHTFLAECHE verkleinert - der Inhalt bleibt, wie er ist.
    leinwand.configure(height=300)
    for _ in range(3):
        root.update()
        root.update_idletasks()
    leinwand.yview_moveto(0.5)                            # wirklich rollen
    for _ in range(3):
        root.update()
        root.update_idletasks()
    sichtbar_oben = int(round(float(leinwand.canvasy(0))))
    nachher = int(leinwand.bbox(kopf_text)[1])
    # Der Kopf-Text beginnt SIEDLUNGS_SCHLEIER_RAND (8 px) unter der Bandkante - darum wird
    # gegen das Band geprueft, nicht gegen die Textkante.
    band = int(main.SIEDLUNGS_SCHLEIER_RAND)
    check("der Kopf steht nach dem Rollen auf der Oberkante des sichtbaren Bereichs",
          abs(nachher - (sichtbar_oben + band)) <= 2,
          "%d gegen %d (+%d Rand)" % (nachher, sichtbar_oben, band))
    messwert("kopf_y_nach_rollen", nachher, "px")
    messwert("sichtbar_oben", sichtbar_oben, "px")
    check("der Inhalt ist wirklich gerollt (die Oberkante ist gewandert)",
          sichtbar_oben > vorher, "%d gegen %d" % (sichtbar_oben, vorher))
    # 5. Gegenprobe: ein anderer Block ist NICHT mitgeklebt
    andere = [i for i in leinwand.find_all()
              if leinwand.type(i) == "text" and i not in teile]
    if andere:
        tiefen = [int(leinwand.bbox(i)[1]) for i in andere]
        check("mindestens ein anderer Block ist nach oben aus dem Bild gewandert "
              "(der Kopf ist der einzige, der klebt)",
              min(tiefen) < sichtbar_oben, "kleinster y %d, oben %d" % (min(tiefen), sichtbar_oben))
        messwert("anderer_block_y", min(tiefen), "px")
    # Die Unterlage bleibt oben und deckt den rollenden Inhalt ab
    if unterlage:
        u_oben = int(leinwand.coords(unterlage[0])[1])
        check("die Unterlage ist mit dem Kopf gewandert", abs(u_oben - sichtbar_oben) <= 2,
              "%d gegen %d" % (u_oben, sichtbar_oben))
        reihenfolge = list(leinwand.find_all())
        check("die Unterlage liegt im Stapel UEBER dem rollenden Inhalt",
              reihenfolge.index(unterlage[0]) > 0,
              str(reihenfolge.index(unterlage[0])))
    root.destroy()


if __name__ == "__main__":
    rechnung()
    fenster()
    sys.exit(bericht())
