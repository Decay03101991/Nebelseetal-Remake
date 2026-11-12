# -*- coding: ascii -*-
"""Messung an den Meshy-Bildern fuer Auftrag Nr. 6 (12.11.2026).

Beantwortet die UNBEKANNT aus Claudes Antwort, soweit sie an den Bildern messbar sind:
1. Ist der Grund des Wappenbildes einfarbig? (vier 32x32-Eckfelder, Mittelwert und Streuung)
2. Liegt ein Horizont in den Randzeilen? (Claudes Startwert: Unterschied zweier Nachbarzeilen > 12)
3. Kontaktbogen mit Lineal fuer die cx-Liste (Daniel bestimmt die Motivmitte mit dem Auge).

Aufruf:  python -X utf8 tools/messe_meshy_1zu1.py
"""
from __future__ import annotations

import os
import sys

from PIL import Image, ImageDraw, ImageFont, ImageStat

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASIS = os.path.join(ROOT, "docs/eingaenge/MESHY_20261112_BILDASSETS")

BILDER = [
    ("panorama/ref_panorama_menschlich.png", "Panorama menschlich"),
    ("panorama/ref_panorama_elfisch.png", "Panorama elfisch"),
    ("panorama/ref_panorama_zwergisch.png", "Panorama zwergisch"),
    ("panorama/ref_panorama_gnome.png", "Panorama gnomisch"),
    ("panorama/ref_panorama_trolle.png", "Panorama trollisch"),
    ("panorama/ref_panorama_ghule.png", "Panorama ghulisch"),
    ("elfen/ref_elfen_bibliothek.png", "Elfen Bibliothek"),
    ("elfen/ref_elfen_kriegerakademie.png", "Elfen Kriegerakademie"),
    ("elfen/ref_elfen_stellmacher.png", "Elfen Stellmacher"),
]
WAPPEN = "elfen/ref_elfen_wappen_und_banner.png"


def eckfelder(bild, kante=32):
    """Mittelwert und Streuung je Kanal in den vier 32x32-Eckfeldern."""
    w, h = bild.size
    felder = {
        "oben links": (0, 0, kante, kante),
        "oben rechts": (w - kante, 0, w, kante),
        "unten links": (0, h - kante, kante, h),
        "unten rechts": (w - kante, h - kante, w, h),
    }
    ergebnis = {}
    for name, box in felder.items():
        st = ImageStat.Stat(bild.crop(box).convert("RGB"))
        ergebnis[name] = (st.mean, st.stddev)
    return ergebnis


def randzeilen(bild, hoehe=128):
    """Groesster Unterschied zweier Nachbarzeilen (Graumittel) in den oberen/unteren Randzeilen."""
    g = bild.convert("L")
    w, h = g.size
    aus = {}
    for seite, box in (("oben", (0, 0, w, hoehe)), ("unten", (0, h - hoehe, w, h))):
        streifen = g.crop(box)
        mittel = []
        for y in range(streifen.height):
            st = ImageStat.Stat(streifen.crop((0, y, w, y + 1)))
            mittel.append(st.mean[0])
        sprung = max(abs(mittel[i + 1] - mittel[i]) for i in range(len(mittel) - 1))
        aus[seite] = (round(sprung, 1), round(min(mittel), 1), round(max(mittel), 1))
    return aus


def main():
    print("=== 1. Wappenbild: ist der Grund einfarbig? ===")
    pfad = os.path.join(BASIS, WAPPEN)
    wappen = Image.open(pfad)
    print("Datei:", WAPPEN, wappen.size, wappen.mode)
    felder = eckfelder(wappen)
    mittel = []
    streuung = []
    for name, (m, s) in felder.items():
        print("  %-12s Mittel %s | Streuung %s" % (name, [round(x, 1) for x in m],
                                                   [round(x, 1) for x in s]))
        mittel.append(m)
        streuung.append(max(s))
    je_kanal = [max(m[k] for m in mittel) - min(m[k] for m in mittel) for k in range(3)]
    print("  Abweichung der Mittelwerte je Kanal:", [round(x, 1) for x in je_kanal])
    print("  groesste Streuung:", round(max(streuung), 1))
    einfarbig = all(x <= 4 for x in je_kanal) and max(streuung) <= 3
    print("  Urteil nach Claudes Regel:", "EINFARBIG" if einfarbig else "NICHT einfarbig")

    print("\n=== 2. Liegt ein Horizont in den Randzeilen? (Startwert 12) ===")
    for rel, name in BILDER:
        p = os.path.join(BASIS, rel)
        if not os.path.exists(p):
            print("  fehlt:", rel)
            continue
        bild = Image.open(p)
        r = randzeilen(bild)
        oben, unten = r["oben"], r["unten"]
        print("  %-22s %s | oben Sprung %5.1f (%s..%s) %s | unten Sprung %5.1f (%s..%s) %s"
              % (name, bild.size, oben[0], oben[1], oben[2], "HORIZONT" if oben[0] > 12 else "ruhig",
                 unten[0], unten[1], unten[2], "HORIZONT" if unten[0] > 12 else "ruhig"))

    print("\n=== 3. Kontaktbogen mit Lineal fuer die cx-Liste ===")
    spalten, zeilen = 3, 3
    zelle_w, zelle_h = 470, 300
    rand = 34
    bogen = Image.new("RGB", (spalten * (zelle_w + rand) + rand,
                              zeilen * (zelle_h + rand + 26) + rand), (24, 24, 28))
    zeichner = ImageDraw.Draw(bogen)
    try:
        schrift = ImageFont.truetype("arial.ttf", 15)
        klein = ImageFont.truetype("arial.ttf", 12)
    except Exception:                                   # noqa: BLE001
        schrift = klein = ImageFont.load_default()
    for i, (rel, name) in enumerate(BILDER):
        p = os.path.join(BASIS, rel)
        if not os.path.exists(p):
            continue
        bild = Image.open(p).convert("RGB")
        w, h = bild.size
        skala = zelle_w / float(w)
        vorschau = bild.resize((zelle_w, int(h * skala)), Image.LANCZOS)
        x = rand + (i % spalten) * (zelle_w + rand)
        y = rand + (i // spalten) * (zelle_h + rand + 26)
        bogen.paste(vorschau, (x, y))
        zeichner.text((x, y - 18), name, fill=(240, 230, 200), font=schrift)
        # Lineal in ORIGINAL-Pixeln alle 100 px
        for px in range(0, w + 1, 100):
            sx = x + int(px * skala)
            hoch = 8 if px % 500 else 14
            zeichner.line((sx, y + vorschau.height, sx, y + vorschau.height + hoch),
                          fill=(200, 190, 160))
            if px % 200 == 0:
                zeichner.text((sx - 8, y + vorschau.height + hoch + 1), str(px),
                              fill=(180, 175, 160), font=klein)
        # Standard-Fenster fuer cx = 768 (Bildmitte): x0 = 107 bis 1249
        x0 = 107
        zeichner.line((x + int(x0 * skala), y, x + int(x0 * skala), y + vorschau.height),
                      fill=(255, 120, 90), width=2)
        zeichner.line((x + int((x0 + 1142) * skala), y, x + int((x0 + 1142) * skala), y + vorschau.height),
                      fill=(255, 120, 90), width=2)
    ziel = os.path.join(ROOT, "docs/audits/meshy_cx_bogen_20261112.png")
    bogen.save(ziel)
    print("  Bogen:", ziel, bogen.size)
    print("  rote Linien = Ausschnitt bei cx = 768 (Bildmitte), also x0 = 107 bis 1249")


if __name__ == "__main__":
    main()
