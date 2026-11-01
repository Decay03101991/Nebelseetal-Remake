# -*- coding: utf-8 -*-
"""Schneidet die Burgen- und Wappen-Sheets in Einzelbilder.

Aufruf: python -X utf8 tools/burgen_wappen_schneiden.py
Quelle: archiv/eingaben/20261101_burgen_wappen/*.png (fremdes Assetpaket, README liegt dabei)
Ziel:   assets/icons/burgen/burg_1..6.png, assets/icons/wappen/wappen_1..10.png
Trennung: leere Spalten und Zeilen im Bild (Projektion), keine geratene Rastervermutung.
"""
import os
from PIL import Image

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUELLE = os.path.join(WURZEL, "archiv", "eingaben", "20261101_burgen_wappen")
ZIELE = {
    "Nebelseetal_Burgen_Iconset_6er.png": (os.path.join("assets", "icons", "burgen"), "burg"),
    "Nebelseetal_Wappen_Iconset_10er.png": (os.path.join("assets", "icons", "wappen"), "wappen"),
}


def bestandteile(pfad, mindest_pixel=20000):
    """Grosse zusammenhaengende Bildbereiche finden (4er-Nachbarschaft auf der Alpha-Maske).

    Eine Projektion ueber Spalten reicht hier nicht: die Icons beruehren sich fast, es gibt
    keine leeren Trennspalten. Die Bestandteile liefern die echten Kacheln (6 bzw. 10).
    """
    from collections import deque
    bild = Image.open(pfad).convert("RGBA")
    alpha = bild.split()[3].load()
    breite, hoehe = bild.size
    gesehen = [[False] * breite for _ in range(hoehe)]
    kisten = []
    for y in range(hoehe):
        for x in range(breite):
            if gesehen[y][x] or alpha[x, y] < 12:
                continue
            schlange = deque([(x, y)])
            gesehen[y][x] = True
            x0 = x1 = x
            y0 = y1 = y
            anzahl = 0
            while schlange:
                cx, cy = schlange.popleft()
                anzahl += 1
                x0, x1 = min(x0, cx), max(x1, cx)
                y0, y1 = min(y0, cy), max(y1, cy)
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < breite and 0 <= ny < hoehe and not gesehen[ny][nx] and alpha[nx, ny] >= 12:
                        gesehen[ny][nx] = True
                        schlange.append((nx, ny))
            if anzahl > mindest_pixel:
                kisten.append((x0, y0, x1, y1))
    kisten.sort(key=lambda k: (k[1] // 200, k[0]))
    return bild, kisten


def schneiden(pfad, zielordner, praefix, rand=4):
    """Jedes Icon einzeln ausschneiden und als PNG ablegen."""
    voll = os.path.join(QUELLE, pfad)
    bild, kisten = bestandteile(voll)
    ziel = os.path.join(WURZEL, zielordner)
    os.makedirs(ziel, exist_ok=True)
    for alt in os.listdir(ziel):
        if alt.startswith(praefix + "_") and alt.endswith(".png"):
            os.remove(os.path.join(ziel, alt))
    for nummer, (x0, y0, x1, y1) in enumerate(kisten, start=1):
        kasten = (max(0, x0 - rand), max(0, y0 - rand), min(bild.width, x1 + rand), min(bild.height, y1 + rand))
        stueck = bild.crop(kasten)
        name = "%s_%02d.png" % (praefix, nummer)
        stueck.save(os.path.join(ziel, name))
        print("  %-16s %4dx%-4d" % (name, stueck.width, stueck.height))
    print("%s: %d Einzelbilder" % (pfad, len(kisten)))
    return len(kisten)


def main():
    gesamt = 0
    for datei, (ordner, praefix) in ZIELE.items():
        print(datei)
        gesamt += schneiden(datei, ordner, praefix)
    print("zusammen:", gesamt, "Einzelbilder")


if __name__ == "__main__":
    main()
