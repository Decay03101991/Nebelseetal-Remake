# -*- coding: ascii -*-
"""A-10: der Schleier liegt IM BILD, die Texte stehen auf der Leinwand (12.11.2026).

Grundlage: Daniels Wort vom 12.11.2026 (Register 518) -

    "mit 80% Schleiher umbauen und den braunen hintergrund der textbloecke leicht
     transparent machen, sodass man mehr vom hintergrund erkennt. Dementsprechend
     aber auch texte deutlicher schreiben."

und Claudes Antwort auf Auftrag Nr. 12 (docs/eingaenge/CLAUDE_20261112_ANSICHTEN_NR12/):
Bilder mit eingerechneten Schleiern (A1), Texte als Canvas-Elemente (B1), Schriftgrade in
Pixeln (B2), zwei Durchgaenge ueber `bbox` (B3), Ortsbestand mit eigener deckender Flaeche
ohne Schleier (B5), Panels mit Schleier UND Ersatzfarbe E (D).

Was diese Datei zusichert:
1. RECHNUNG ohne Fenster: 80 Prozent #1a0a09 ueber Weiss ist #483b3a, die Mischung ist genau
   0,8 x Farbe + 0,2 x Bild - und `bereich` laesst Pixel AUSSERHALB der Felder unberuehrt.
2. KONTRASTE: Creme 8,42 - Gold 7,10 - Erfolg 6,37 - Warnung 4,65 - Rahmen 3,31 auf dem
   Schleier-Ton (WCAG, selbst gerechnet).
3. FENSTER: die Spalte traegt ein Bild (Tag "schleier"), die FUENF Textbloecke sind
   Canvas-Elemente, und jeder Block ohne eigene Flaeche liegt ganz auf einem Schleierfeld.
4. STICHPIXEL: im Feld steht die gemischte Farbe, in der Luecke zwischen zwei Bloecken das
   unveraenderte Quellpixel des Panoramas.
5. PANEL: die bedienbaren Bloecke tragen die Ersatzfarbe E (Schleier-Ton), nicht das Skin-Braun.
6. RUECKFALL ohne Bild: Panel-Farbe bleibt die Skin-Farbe, kein Bild, keine Ausnahme.

Aufruf:  python -X utf8 tests/test_siedlungsansicht_a10.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster+messen"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['hintergrund_optik', 'main:*']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src, messwert

ROOT, SRC = import_src()
import main          # noqa: E402
import hintergrund_optik as optik   # noqa: E402

# Der Schleier-Ton aus Register 507/518 (80 Prozent #1a0a09 ueber Weiss).
SCHLEIER_TON = "#483b3a"


def _leuchtdichte(farbe: str) -> float:
    """WCAG-Leuchtdichte einer Farbe '#rrggbb'."""
    def _lin(wert: int) -> float:
        anteil = wert / 255.0
        return anteil / 12.92 if anteil <= 0.04045 else ((anteil + 0.055) / 1.055) ** 2.4
    r, g, b = optik.rgb(farbe)
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def kontrast(eins: str, zwei: str) -> float:
    """WCAG-Kontrastverhaeltnis zweier Farben, auf zwei Stellen gerundet."""
    hell, dunkel = sorted((_leuchtdichte(eins), _leuchtdichte(zwei)), reverse=True)
    return round((hell + 0.05) / (dunkel + 0.05), 2)


def rechnung():
    abschnitt("1. Rechnung ohne Fenster: Mischung, Ton und unberuehrte Pixel")
    check("80 Prozent #1a0a09 ueber Weiss ergibt den Schleier-Ton #483b3a",
          optik.schleier_ton(_weiss(), None) == SCHLEIER_TON,
          optik.schleier_ton(_weiss(), None))
    check("die Mischung ist 0,8 x Farbe + 0,2 x Bild (26/10/9 und 255/255/255)",
          optik.rgb(SCHLEIER_TON) == (72, 59, 58), str(optik.rgb(SCHLEIER_TON)))
    messwert("schleier_ton", SCHLEIER_TON, "hex")
    pfad = optik.pfad_panorama("elfisch")
    check("das Elfen-Panorama liegt vor (ohne Bild ist A-10 nicht messbar)", bool(pfad))
    if not pfad:
        return
    feld = (10, 10, 60, 40)
    bild = optik.bereich(pfad, 59, 272, 200, 120, schleier=[feld])
    check("bereich liefert ein Bild in Zielgroesse", bild is not None and bild.size == (200, 120),
          "None" if bild is None else str(bild.size))
    if bild is None:
        return
    quelle = optik._bild_oeffnen(pfad)
    roh = quelle.crop((59, 272, 259, 392))
    # im Feld: gemischt
    x, y = feld[0] + 5, feld[1] + 5
    soll = tuple(int(round(0.8 * a + 0.2 * b)) for a, b in zip(optik.rgb(optik.SCHLEIER_FARBE),
                                                              roh.getpixel((x, y))[:3]))
    ist = bild.getpixel((x, y))[:3]
    check("im Schleierfeld steht die gemischte Farbe (0,8 x Schleier + 0,2 x Bild)",
          all(abs(a - b) <= 1 for a, b in zip(soll, ist)), "%r gegen %r" % (soll, ist))
    # ausserhalb: unveraendert
    x2, y2 = 150, 100
    check("ausserhalb der Felder bleibt das Quellpixel unveraendert",
          bild.getpixel((x2, y2))[:3] == roh.getpixel((x2, y2))[:3],
          "%r gegen %r" % (bild.getpixel((x2, y2))[:3], roh.getpixel((x2, y2))[:3]))
    check("ohne Schleierfelder aendert sich nichts (alter Weg, A-7 bleibt gueltig)",
          optik.bereich(pfad, 59, 272, 120, 60).getpixel((3, 3))
          == quelle.crop((59, 272, 179, 332)).getpixel((3, 3)))


def _weiss():
    """Ein weisses Bild als Vergleichsflaeche (worst case des Schleiers)."""
    from PIL import Image
    return Image.new("RGBA", (10, 10), "#ffffff")


def kontraste():
    abschnitt("2. Kontraste auf dem Schleier-Ton (WCAG, selbst gerechnet)")
    for farbe, name, soll in ((main.SPALTE_CREME, "Creme", 8.42),
                              (main.SPALTE_GOLD, "Gold", 7.10),
                              (main.SPALTE_ERFOLG, "Erfolg", 6.37),
                              (main.SPALTE_WARNUNG, "Warnung", 4.65)):
        ist = kontrast(farbe, SCHLEIER_TON)
        check("%s %s haelt %.2f : 1 auf dem Schleier" % (name, farbe, soll),
              abs(ist - soll) <= 0.01, "ist %.2f" % ist)
        check("%s liegt ueber der Textgrenze 4,5 : 1" % name, ist >= 4.5, "ist %.2f" % ist)
        messwert("kontrast_%s" % name, ist, ": 1")
    rahmen = kontrast("#b8862e", SCHLEIER_TON)
    check("der Rahmen #b8862e haelt 3,31 : 1 (nur Linien, nie Text)", abs(rahmen - 3.31) <= 0.01,
          "ist %.2f" % rahmen)
    check("kein Text unter 12 px (B2, HART)", int(main.SPALTE_TEXT_MIN) >= 12)


def _fenster(ohne_bild: bool = False):
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
    # Die Fraktion bestimmt das Panorama: ohne sie bleibt die Ansicht ohne Bild (A-7). Die
    # erfundene Siedlung des Testaufbaus hat kein Volk, darum wird die Fraktion gesetzt.
    app.spieler_fraktion = "" if ohne_bild else "elfisch"
    if ohne_bild:                                   # Rueckfall C der Antwort Nr. 12
        app._siedlungs_hintergrund = lambda: None    # kein Panorama anlegen
        app._siedlungs_pfad = ""
    siedlung = next((s for s in app.state.settlements if getattr(s, "karte", None)), None)
    if siedlung is None:
        return root, None
    app._oeffne_siedlungskarte(siedlung)
    for _ in range(5):
        root.update()
        root.update_idletasks()
    return root, app


def fenster():
    abschnitt("3. Im Fenster: Bild hinter der Spalte, fuenf Textbloecke auf der Leinwand")
    root, app = _fenster()
    if app is None:
        befund("keine Siedlung mit Karte im Testaufbau")
        root.destroy()
        return
    leinwand = getattr(app, "_spalte_leinwand", None)
    check("die Spalte ist eine Leinwand", leinwand is not None)
    if leinwand is None:
        root.destroy()
        return
    felder = getattr(app, "_spalte_felder", None)
    check("die Schleierfelder sind gemerkt", isinstance(felder, list) and len(felder) >= 5,
          str(felder)[:120])
    messwert("schleierfelder", len(felder or []), "Stueck")
    # 1. Das Bild liegt hinter der Spalte
    bilder = [i for i in leinwand.find_all() if leinwand.type(i) == "image"]
    check("die Spalte traegt ein Hintergrundbild", len(bilder) == 1, str(len(bilder)))
    roh = getattr(app, "_spalte_bild", None)
    check("das Bild liegt als Pillow-Flaeche vor", roh is not None)
    if roh is not None:
        breite = int(getattr(app, "_spalte_breite", 0) or 0)
        check("das Bild ist so breit wie die Spalte", roh.width == breite,
              "%d gegen %d" % (roh.width, breite))
        check("das Bild ist mindestens so hoch wie der Inhalt",
              roh.height >= leinwand.winfo_height(), "%d px" % roh.height)
        messwert("spaltenbild", "%dx%d" % (roh.width, roh.height), "px")
    if bilder:
        check("das Bild liegt GANZ hinten (unter den Texten)",
              leinwand.find_all()[0] == bilder[0] or
              list(leinwand.find_withtag("schleier")) == [bilder[0]],
              str(list(leinwand.find_withtag("schleier"))))
    # 2. Die fuenf Textbloecke sind Canvas-Elemente
    texte = [leinwand.itemcget(i, "text") for i in leinwand.find_all()
             if leinwand.type(i) == "text"]
    zusammen = " | ".join(texte)
    for anfang in ("Siedlungskarte", "W\u00e4hle ein Feld auf der Karte", "Ortsbestand dieser Siedlung",
                   "Zum Vergleich das ganze Reich", "Vorteil:", "Sumpf ist nicht bebaubar"):
        check("der Textblock '%s...' steht auf der Leinwand" % anfang[:28],
              any(t.startswith(anfang) or anfang in t for t in texte), zusammen[:160])
    # 3. Kein Titel-Label mehr in der Spalte (er WAR ein tk.Label, Register 515)
    import tkinter as tk
    label_titel = []
    for kind in app.content.winfo_children():
        for enkel in kind.winfo_children():
            for ur in enkel.winfo_children():
                if isinstance(ur, tk.Label):
                    try:
                        if str(ur.cget("text")) == "Siedlungskarte":
                            label_titel.append(ur)
                    except tk.TclError:
                        pass
    check("der Titel ist KEIN tk.Label mehr (deckend) - er ist ein Canvas-Text",
          not label_titel, str(label_titel[:2]))
    # 4. Jeder nicht-deckende Block liegt ganz auf einem Schleierfeld
    bloecke = getattr(app, "_spalte_bloecke_merken", None)
    check("die Blocklagen sind gemerkt", bloecke is not None)
    if bloecke is not None:
        gefunden, deckend = bloecke[0], 0
        check("es sind genau fuenf Textbloecke", len(gefunden) == 5, str(len(gefunden)))
        namen = [b["name"] for b in gefunden]
        check("die Bloecke heissen kopf, hinweis, ortsbestand, vergleich, legende",
              namen == ["kopf", "hinweis", "ortsbestand", "vergleich", "legende"], str(namen))
        for block in gefunden:
            if block.get("deckend"):
                deckend += 1
                continue
            kaesten = [leinwand.bbox(i) for i in block["items"] if leinwand.bbox(i)]
            if not kaesten:
                befund("Block %s hat keine messbare bbox" % block["name"])
                continue
            x0 = min(k[0] for k in kaesten)
            y0 = min(k[1] for k in kaesten)
            x1 = max(k[2] for k in kaesten)
            y1 = max(k[3] for k in kaesten)
            in_feld = any(fx <= x0 and fy <= y0 and x1 <= fx + fw and y1 <= fy + fh
                          for fx, fy, fw, fh in felder)
            check("Block '%s' liegt ganz auf einem Schleierfeld" % block["name"], in_feld,
                  "bbox %dx%d bis %dx%d" % (x0, y0, x1, y1))
            messwert("block_%s_hoehe" % block["name"], y1 - y0, "px")
        check("genau EIN Block hat eine eigene deckende Flaeche (der Ortsbestand)",
              deckend == 1, str(deckend))
    # 5. Stichpixel gegen die Quelle
    if roh is not None and felder:
        quelle = optik._bild_oeffnen(str(app._siedlungs_pfad))
        links, oben = app._spalte_versatz()
        fx, fy, fw, fh = felder[0]
        px, py = fx + 20, fy + 6
        soll = tuple(int(round(0.8 * a + 0.2 * b)) for a, b in
                     zip(optik.rgb(optik.SCHLEIER_FARBE),
                         quelle.getpixel((links + px, oben + py))[:3]))
        ist = roh.getpixel((px, py))[:3]
        check("Stichpixel IM Feld ist gemischt", all(abs(a - b) <= 1 for a, b in zip(soll, ist)),
              "%r gegen %r" % (soll, ist))
        # Luecke zwischen Block 1 und Block 2
        luecke = int(felder[0][1] + felder[0][3] + 3)
        if luecke < int(felder[1][1]):
            quelle_px = quelle.getpixel((links + 30, oben + luecke))[:3]
            check("Stichpixel in der LUECKE zwischen zwei Bloecken ist die Quelle",
                  roh.getpixel((30, luecke))[:3] == quelle_px,
                  "%r gegen %r" % (roh.getpixel((30, luecke))[:3], quelle_px))
            messwert("luecke_y", luecke, "px")
    # 6. Ersatzfarbe E der bedienbaren Bloecke
    ton = str(getattr(app, "_spalte_schleier_ton", "") or "")
    check("die Ersatzfarbe E ist gemessen", ton.startswith("#") and len(ton) == 7, ton)
    check("E ist NICHT das braune Skin-Panel (das war Daniels Klage)",
          ton != str(app.skin["panel"]), "%s gegen %s" % (ton, app.skin["panel"]))
    check("E haelt Creme ueber 8 : 1", kontrast(main.SPALTE_CREME, ton) >= 8.0,
          "%.2f" % kontrast(main.SPALTE_CREME, ton))
    messwert("ersatzfarbe_E", ton, "hex")
    knoepfe = []

    def _sammeln(widget, tiefe=0):
        if tiefe > 6:
            return
        for kind in widget.winfo_children():
            knoepfe.append(kind)
            _sammeln(kind, tiefe + 1)
    _sammeln(app._spalte_frame)
    panel = [w for w in knoepfe if w.winfo_class() == "Frame"
             and str(w.cget("bg")).lower() == ton.lower()]
    check("die bedienbaren Bloecke stehen auf der Ersatzfarbe E", len(panel) >= 2, str(len(panel)))
    root.destroy()


def rueckfall():
    abschnitt("5. Rueckfall ohne Bild (Antwort Nr. 12, Abschnitt C)")
    root, app = _fenster(ohne_bild=True)
    if app is None:
        befund("keine Siedlung mit Karte im Testaufbau")
        root.destroy()
        return
    check("ohne Panorama bleibt die Panel-Farbe die Skin-Farbe",
          app._panel_ton() == app.skin["panel"],
          "%s gegen %s" % (app._panel_ton(), app.skin["panel"]))
    leinwand = getattr(app, "_spalte_leinwand", None)
    if leinwand is not None:
        bilder = [i for i in leinwand.find_all() if leinwand.type(i) == "image"]
        check("ohne Panorama entsteht kein Spaltenbild", not bilder, str(len(bilder)))
        texte = [i for i in leinwand.find_all() if leinwand.type(i) == "text"]
        check("die Texte stehen trotzdem auf der Leinwand", len(texte) >= 6, str(len(texte)))
    root.destroy()


if __name__ == "__main__":
    rechnung()
    kontraste()
    fenster()
    rueckfall()
    raise SystemExit(bericht())
