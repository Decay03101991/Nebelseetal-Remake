# -*- coding: ascii -*-
"""Ergebnistafel: die neun 1:1-Hintergruende und das freigestellte Wappen auf Magenta und Schwarz."""
from __future__ import annotations

import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HG = os.path.join(ROOT, "assets/hintergruende/meshy_1zu1")
WAPPEN = os.path.join(ROOT, "assets/wappen")
ZIEL = os.path.join(ROOT, "docs/audits/meshy_1zu1_ergebnis_20261112.png")


def main():
    namen = sorted(n for n in os.listdir(HG) if n.endswith(".jpg"))
    zelle_w, zelle_h = 320, 314
    rand = 26
    spalten = 3
    zeilen = 3 + 1                      # dritte Zeile frei fuer das Wappen
    bogen = Image.new("RGB", (spalten * (zelle_w + rand) + rand,
                              zeilen * (zelle_h + rand) + rand + 60), (22, 22, 26))
    zeichner = ImageDraw.Draw(bogen)
    try:
        schrift = ImageFont.truetype("arial.ttf", 14)
    except Exception:                   # noqa: BLE001
        schrift = ImageFont.load_default()
    zeichner.text((rand, 14), "Meshy auf 1:1 (1142 x 1120): Mitte beschnitten, 128 px oben und unten "
                              "ergaenzt - Naht 0,00, Schaerfe unveraendert", fill=(240, 232, 210), font=schrift)
    for i, name in enumerate(namen):
        bild = Image.open(os.path.join(HG, name)).convert("RGB")
        vorschau = bild.resize((zelle_w, zelle_h), Image.LANCZOS)
        x = rand + (i % spalten) * (zelle_w + rand)
        y = 46 + (i // spalten) * (zelle_h + rand)
        bogen.paste(vorschau, (x, y))
        zeichner.text((x, y + zelle_h + 2), name.replace("_1142x1120.jpg", ""), fill=(190, 185, 170),
                      font=schrift)
    # Wappen: auf Magenta und auf Schwarz, in drei Groessen
    y = 46 + 3 * (zelle_h + rand)
    x = rand
    wappen = Image.open(os.path.join(WAPPEN, "elfen_wappen.png")).convert("RGBA")
    for grund, farbe in (("Magenta", (255, 0, 255)), ("Schwarz", (0, 0, 0))):
        flaeche = Image.new("RGB", (3 * 150 + 20, 200), farbe)
        for j, kante in enumerate((128, 64, 32)):
            klein = wappen.resize((kante, kante), Image.LANCZOS)
            flaeche.paste(klein, (10 + j * 150, 36), klein)
            zeichner.text((x + 10 + j * 150, y + 18), "%d px" % kante, fill=(250, 250, 250), font=schrift)
        bogen.paste(flaeche, (x, y))
        zeichner.text((x, y + 205), "Wappen auf %s" % grund, fill=(200, 195, 180), font=schrift)
        x += 3 * 150 + 60
    bogen.save(ZIEL)
    print("Tafel:", ZIEL, bogen.size)


if __name__ == "__main__":
    main()
