# -*- coding: ascii -*-
"""Sichtvergleich der Ressourcenleiste bei breiten Fenstern - P-3 (02.11.2026).

Daniels Befund: bei sehr breiten Fenstern wiederholt sich die gemalte Landschaft in den Luecken.
Dieses Werkzeug legt drei Fassungen untereinander, alle aus DEMSELBEN Renderer
(`main.leiste_zusammensetzen`): ALT (Luecken nehmen die ganze Restbreite, wie bis 02.11.2026),
NEU (Lueckendehnung gedeckelt, Rest gleichmaessig skaliert) und NEU bei Ueberbreite.

Aufruf:  python -X utf8 tools/leisten_vergleich.py [--breiten 2560,3440]
Ergebnis: docs/audits/leisten_vergleich_<JJJJMMTT>.png
"""
from __future__ import annotations

import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in (ROOT, os.path.join(ROOT, "src")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import main  # noqa: E402

BG = (23, 33, 43)      # dunkler Grund wie die Kopfleiste (#17212B) fuer Pillow
HEADER = 22            # Hoehe der Beschriftung je Streifen


def _streifen(bild, text):
    from PIL import Image, ImageDraw
    tafel = Image.new("RGB", (bild.width, bild.height + HEADER), BG)
    tafel.paste(bild.convert("RGB"), (0, HEADER))
    ImageDraw.Draw(tafel).text((6, 1), text, fill=(226, 199, 125))
    return tafel


def main_() -> int:
    breiten = [2560, 3440]
    for i, arg in enumerate(sys.argv):
        if arg == "--breiten" and i + 1 < len(sys.argv):
            breiten = [int(b) for b in sys.argv[i + 1].split(",")]
    basis = dict(main.RESSOURCENLEISTE)
    alt = dict(basis)
    alt["luecke_max"] = 99.0            # ALT: keine Grenze, Luecken nehmen alles
    alt["rest_auffuellen"] = "leer"
    neu = dict(basis)                    # NEU: Werte aus der Datendatei

    tafeln = []
    for zb in breiten:
        for name, quelle in (("ALT", alt), ("NEU", neu)):
            bild, mitten, skala = main.leiste_zusammensetzen(quelle, zb)
            if bild is None:
                print("keine Leiste (Pillow fehlt)")
                return 1
            sichtbar = bild.getchannel("A").getbbox()
            gefuellt = sichtbar[2] if sichtbar else 0
            tafeln.append(_streifen(bild, "%s  %d px  Skala %.2f  gefuellt bis %d px"
                                    % (name, zb, skala, gefuellt)))
            print(f"{name} {zb}: skala {skala:.3f}, gefuellt bis {gefuellt}")

    from PIL import Image
    breite = max(t.width for t in tafeln)
    hoehe = sum(t.height for t in tafeln) + 8 * len(tafeln)
    blatt = Image.new("RGB", (breite, hoehe), BG)
    y = 0
    for t in tafeln:
        blatt.paste(t, (0, y))
        y += t.height + 8
    ziel = os.path.join(ROOT, "docs", "audits", "leisten_vergleich_%s.png" % time.strftime("%Y%m%d"))
    blatt.save(ziel)
    print("Kontaktblatt:", ziel, blatt.size)
    return 0


if __name__ == "__main__":
    sys.exit(main_())
