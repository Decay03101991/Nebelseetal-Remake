# -*- coding: ascii -*-
"""A-7 / A-8: die neun Meshy-Bilder als Hintergrund der Ansichten (12.11.2026).

Daniels Entscheidungen (Register 502): F-44 - die sechs Voelker-Panoramen tragen die
SIEDLUNGSANSICHT, die drei Elfen-Gebaeude (Bibliothek, Kriegerakademie, Stellmacher) die
EINZELANSICHT. F-45 - die Bilder bleiben 1142 x 1120, gezeigt wird der MITTIGE 1:1-AUSSCHNITT,
und es wird NIE skaliert; ist die Flaeche groesser als das Bild, steht das Bild mittig und der
Rest wird mit der Fensterfarbe #17212B gefuellt.

Was diese Datei zusichert:
1. RECHNUNG: versatz(1037, 589) = (52, 265) - der Ausschnitt ist die Haelfte des Ueberstands,
   abgerundet, wie in Claudes Antwort Teil A (nachgerechnet in
   docs/design/PRUEFUNG_CLAUDE_AUFTRAG7_GEBAEUDEANSICHT_20261112.md).
2. KEINE SKALIERUNG: das Ergebnis hat genau die Zielgroesse, und jeder Pixel stammt aus dem
   Quellbild (Pixelvergleich an drei Ecken) - nicht aus einer Veraenderung der Groesse.
3. GROESSERE FLAECHE: 1400 x 1300 ergibt ein Bild in Zielgroesse, Randpixel im Fuellton,
   Bildmitte aus dem Bild.
4. ZUORDNUNG: jedes der sechs Voelker hat ein Panorama, die drei Gebaeude ihre Einzelansicht,
   unbekannte Namen ergeben None (kein fremdes Bild).
5. ECHTER AUFBAU: die Siedlungsansicht bekommt die Flaeche als ERSTES Kind des Inhalts (also
   hinter allen Texten) und das Bild in der abgerundeten Zielgroesse.
6. OHNE FRAKTION kein Bild - dann bleibt die Ansicht wie vorher.

Aufruf:  python -X utf8 tests/test_gebaeudeansicht_a7.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster+messen"
PRUEF_STUFE = 3
PRUEF_BETRIFFT = ['hintergrund_optik', 'main:*', 'stimmen', 'voelker']
PRUEF_DATEN = ['gebaeude_motive.json', 'voelker.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src, messwert

ROOT, SRC = import_src()
import main  # noqa: E402
import hintergrund_optik as hg  # noqa: E402

TESTBILD = os.path.join(ROOT, "docs", "audits", "messwerte", "_testbild_a7.png")


def _testbild_bauen():
    """Ein 1142 x 1120 Testbild, dessen Pixel ihre Lage verraten: (x % 256, y % 256, 7)."""
    from PIL import Image
    bild = Image.new("RGB", (hg.BILD_BREITE, hg.BILD_HOEHE))
    bild.putdata([(x % 256, y % 256, 7)
                  for y in range(hg.BILD_HOEHE) for x in range(hg.BILD_BREITE)])
    os.makedirs(os.path.dirname(TESTBILD), exist_ok=True)
    bild.save(TESTBILD, "PNG")
    return bild


def _rgb(bild, x, y):
    """RGB eines Pixels als Tupel (auch bei RGBA-Quellen)."""
    px = bild.convert("RGB").getpixel((int(x), int(y)))
    return tuple(px[:3])


def _hex_rgb(wert):
    """'#17212B' -> (23, 33, 43)."""
    text = str(wert).lstrip("#")
    return tuple(int(text[i:i + 2], 16) for i in (0, 2, 4))


# --------------------------------------------------------------------------------------
def rechnung():
    abschnitt("1. Der Ausschnitt ist die Haelfte des Ueberstands, abgerundet")
    faelle = [((1037, 589), (52, 265)), ((691, 589), (225, 265)), ((1142, 1120), (0, 0)),
              ((1141, 1119), (0, 0)), ((1400, 1300), (0, 0))]
    for masse, erwartet in faelle:
        ist = hg.versatz(*masse)
        check("versatz%r = %r" % (masse, erwartet), ist == erwartet, "ist %r" % (ist,))
        messwert("versatz_%dx%d" % masse, list(ist), "px")
    check("die gelieferte Bildgroesse ist 1142 x 1120 (Register 469/502)",
          (hg.BILD_BREITE, hg.BILD_HOEHE) == (1142, 1120),
          "%dx%d" % (hg.BILD_BREITE, hg.BILD_HOEHE))
    check("der Fuellton ist die Fensterfarbe #17212B", str(hg.FUELLTON).upper() == "#17212B",
          str(hg.FUELLTON))


def schnitt_ohne_skalierung():
    abschnitt("2. Geschnitten, nie skaliert: jeder Pixel stammt aus dem Quellbild")
    quelle = _testbild_bauen()
    flaeche = hg.ausschnitt(TESTBILD, 1037, 589)
    check("das Ergebnis hat genau die Zielgroesse", flaeche is not None and flaeche.size == (1037, 589),
          str(getattr(flaeche, "size", None)))
    if flaeche is None:
        return
    links, oben = hg.versatz(1037, 589)
    ecken = [(0, 0), (0, 588), (1036, 0), (1036, 588), (518, 294)]
    stimmt = True
    for x, y in ecken:
        soll = _rgb(quelle, links + x, oben + y)
        ist = _rgb(flaeche, x, y)
        if soll != ist:
            stimmt = False
            check("Ecke (%d,%d) stammt aus dem Quellbild" % (x, y), False,
                  "soll %r, ist %r" % (soll, ist))
            break
    check("fuenf Stichpixel stimmen mit dem Quellbild ueberein (kein Resize)", stimmt,
          "Ausschnitt links %d, oben %d" % (links, oben))
    messwert("ausschnitt_1037x589_links", links, "px")
    messwert("ausschnitt_1037x589_oben", oben, "px")


def groessere_flaeche():
    abschnitt("3. Flaeche groesser als das Bild: 1:1 in der Mitte, Rest im Fuellton")
    flaeche = hg.ausschnitt(TESTBILD, 1400, 1300)
    check("das Ergebnis hat die Zielgroesse 1400 x 1300",
          flaeche is not None and flaeche.size == (1400, 1300),
          str(getattr(flaeche, "size", None)))
    if flaeche is None:
        return
    fuell = _hex_rgb(hg.FUELLTON)
    check("die linke obere Ecke ist der Fuellton", _rgb(flaeche, 0, 0) == fuell,
          str(_rgb(flaeche, 0, 0)))
    check("die rechte untere Ecke ist der Fuellton", _rgb(flaeche, 1399, 1299) == fuell,
          str(_rgb(flaeche, 1399, 1299)))
    # Das Bild steht mittig: sein erster Pixel liegt bei ((1400-1142)//2, (1300-1120)//2).
    mx, my = (1400 - hg.BILD_BREITE) // 2, (1300 - hg.BILD_HOEHE) // 2
    quelle = _testbild_bauen()
    check("die Bildmitte stammt aus dem Bild (nicht skaliert)",
          _rgb(flaeche, mx + 10, my + 10) == _rgb(quelle, 10, 10),
          "Versatz %d, %d" % (mx, my))
    messwert("fuell_rand_links", mx, "px")


def zuordnung():
    abschnitt("4. Zuordnung: sechs Voelker, drei Gebaeude, nichts erfunden")
    import json
    with open(os.path.join(ROOT, "data", "voelker.json"), encoding="utf-8") as datei:
        fraktionen = [str(f.get("kennung")) for f in (json.load(datei).get("fraktionen") or [])]
    check("die Datendatei fuehrt sechs Fraktionen", len(fraktionen) == 6, ", ".join(fraktionen))
    fehlend = [f for f in fraktionen if not hg.pfad_panorama(f)]
    check("jede Fraktion hat ein Panorama im Ordner", not fehlend, ", ".join(fehlend) or "keine")
    check("die Schreibweise ist egal ('trolle' findet 'Trolle')",
          hg.pfad_panorama("trolle") == hg.pfad_panorama("Trolle"),
          str(hg.pfad_panorama("trolle")))
    check("eine unbekannte Fraktion ergibt None", hg.pfad_panorama("Orks") is None)
    check("eine leere Fraktion ergibt None", hg.pfad_panorama("") is None)
    for kennung in ("bibliothek", "kriegerakademie", "stellmacher"):
        check("Gebaeude '%s' hat eine Einzelansicht" % kennung, hg.pfad_gebaeude(kennung) is not None)
    check("ein Gebaeude ohne Bild ergibt None (alter Weg bleibt)", hg.pfad_gebaeude("haus") is None)
    dateien = sorted(os.listdir(os.path.join(ROOT, hg.ORDNER)))
    check("im Ordner liegen genau neun Bilder", len(dateien) == 9, str(len(dateien)))
    messwert("bilder_im_ordner", len(dateien), "Dateien")


def echter_aufbau():
    abschnitt("5. Echter Aufbau: Flaeche als erstes Kind, Bild in der Zielgroesse")
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
    app.spieler_fraktion = "elfisch"
    app._oeffne_siedlungskarte(siedlung)
    for _ in range(4):
        root.update()
        root.update_idletasks()
    leinwand = getattr(app, "_siedlungs_leinwand", None)
    check("die Hintergrundflaeche steht in der Ansicht", leinwand is not None)
    if leinwand is None:
        root.destroy()
        return
    kinder = list(app.content.winfo_children())
    check("die Flaeche ist das ERSTE Kind des Inhalts (liegt also hinter den Texten)",
          kinder and kinder[0] is leinwand, str(kinder.index(leinwand) if leinwand in kinder else -1))
    # Der Bildaufbau laeuft 120 ms nach der letzten Groessenaenderung - hier warten.
    ende = time.time() + 3.0
    while time.time() < ende:
        root.update()
        root.update_idletasks()
        if leinwand.find_withtag("panorama"):
            break
        time.sleep(0.05)
    treffer = leinwand.find_withtag("panorama")
    check("das Panorama liegt auf der Flaeche", bool(treffer), str(len(treffer)))
    if treffer:
        bild = leinwand.itemcget(treffer[0], "image")
        breite = int(float(root.tk.call("image", "width", bild)))
        hoehe = int(float(root.tk.call("image", "height", bild)))
        soll = (max(64, (leinwand.winfo_width() // 64) * 64),
                max(64, (leinwand.winfo_height() // 64) * 64))
        check("das Bild ist so gross wie die Flaeche in 64-px-Schritten (kein Hochskalieren)",
              (breite, hoehe) == soll, "ist %dx%d, soll %dx%d" % (breite, hoehe, soll[0], soll[1]))
        check("das Bild ist NICHT das Quellmass 1142 x 1120 (also wirklich geschnitten)",
              (breite, hoehe) != (1142, 1120), "%dx%d" % (breite, hoehe))
        messwert("siedlung_bild_breite", breite, "px")
        messwert("siedlung_bild_hoehe", hoehe, "px")
        messwert("siedlung_flaeche_breite", leinwand.winfo_width(), "px")
        messwert("siedlung_flaeche_hoehe", leinwand.winfo_height(), "px")

    abschnitt("6. Ohne Fraktion kein Bild - die Ansicht bleibt wie vorher")
    app.spieler_fraktion = ""
    siedlung.volk = ""
    check("ohne Fraktion gibt es keine Hintergrundflaeche",
          app._siedlungs_fraktion() == "", repr(app._siedlungs_fraktion()))
    root.destroy()


def einzelansicht():
    abschnitt("7. Einzelansicht der drei Elfen-Gebaeude (1:1, Zielgroesse)")
    pfad = hg.pfad_gebaeude("bibliothek")
    flaeche = hg.ausschnitt(pfad, 800, 600) if pfad else None
    check("die Bibliothek ergibt eine Flaeche 800 x 600",
          flaeche is not None and flaeche.size == (800, 600),
          str(getattr(flaeche, "size", None)))
    if flaeche is not None:
        links, oben = hg.versatz(800, 600)
        from PIL import Image
        with Image.open(pfad) as roh:
            quelle = roh.convert("RGB")
        check("der erste Pixel stammt aus der Bildmitte der Quelle",
              _rgb(flaeche, 0, 0) == _rgb(quelle, links, oben),
              "soll %r" % (_rgb(quelle, links, oben),))
        messwert("einzelansicht_versatz_links", links, "px")
        messwert("einzelansicht_versatz_oben", oben, "px")


def zahlen_je_weg():
    abschnitt("8. Zahlen je Weg: die 1:1-Bilder bekommen keinen Schleier")
    check("die Vorgabe fuehrt die beiden 1zu1-Schluessel",
          "abdunkeln_prozent_1zu1" in main.HINTERGRUND_VORGABE
          and "weichzeichnen_px_1zu1" in main.HINTERGRUND_VORGABE,
          ", ".join(sorted(main.HINTERGRUND_VORGABE)))
    alt = {"abdunkeln_prozent": 18.0, "weichzeichnen_px": 2.0}
    neu = main.NebelseetalApp._hintergrund_werte(None, "bibliothek", dict(alt))
    check("ein 1:1-Bild bekommt 0 Prozent Schleier und 0 px Weichzeichnen", neu == (0.0, 0.0), str(neu))
    bleibt = main.NebelseetalApp._hintergrund_werte(None, "haus", dict(alt))
    check("ein Gebaeude ohne 1:1-Bild behaelt die alten Zahlen (18 / 2)", bleibt == (18.0, 2.0),
          str(bleibt))
    import json
    with open(os.path.join(ROOT, "data", "gebaeude_motive.json"), encoding="utf-8") as datei:
        werte = json.load(datei).get("ansicht_hintergrund") or {}
    check("die Datendatei stellt beide Zahlen auf 0 (Daniel stellt sie dort)",
          float(werte.get("abdunkeln_prozent_1zu1", -1)) == 0.0
          and float(werte.get("weichzeichnen_px_1zu1", -1)) == 0.0,
          "%r / %r" % (werte.get("abdunkeln_prozent_1zu1"), werte.get("weichzeichnen_px_1zu1")))
    messwert("abdunkeln_1zu1", werte.get("abdunkeln_prozent_1zu1"), "Prozent")


if __name__ == "__main__":
    rechnung()
    schnitt_ohne_skalierung()
    groessere_flaeche()
    zuordnung()
    echter_aufbau()
    einzelansicht()
    zahlen_je_weg()
    raise SystemExit(bericht())
