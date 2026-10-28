"""
Vergleichsblatt bauen: jedes Icon vorher (mit Blatt-Hintergrund) und nachher (freigestellt).

Die Zahlen im Blatt entsprechen der Nummer in der Legende, die Daniel zum Blatt bekommt.
Aufbau je Zeile: [Nummer] [vorher] [nachher] auf grauem Grund, damit Transparenz sichtbar ist.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from slice_icons import read_png, to_rgba, write_png, draw_text

WURZEL = Path(__file__).resolve().parent.parent
GRUND = (96, 96, 96)          # grauer Grund: Transparenz ist so erkennbar
RAND = 10


def _lege(rgba, w, h, ziel, W, H, x0, y0):
    for y in range(h):
        if y0 + y >= H:
            break
        for x in range(w):
            if x0 + x >= W:
                break
            p = (y * w + x) * 4
            z = ((y0 + y) * W + (x0 + x)) * 4
            a = rgba[p + 3]
            if a == 0:
                continue                      # durchsichtig -> Grund bleibt
            if a == 255:
                ziel[z:z + 3] = rgba[p:p + 3]
            else:                             # weich mischen
                for k in range(3):
                    ziel[z + k] = (rgba[p + k] * a + GRUND[k] * (255 - a)) // 255


def blatt(zeilen, ziel_pfad: str):
    """zeilen: Liste von (nummer, pfad_vorher, pfad_nachher)."""
    bilder = []
    for nummer, vorher, nachher in zeilen:
        iv = read_png(str(vorher))
        in_ = read_png(str(nachher))
        rv = to_rgba(iv)
        rn = to_rgba(in_)
        bilder.append((nummer, iv["w"], iv["h"], rv, in_["w"], in_["h"], rn))

    hoehe_zeile = max(max(b[2], b[5]) for b in bilder) + 2 * RAND
    breite_nummer = 46
    breite_zelle = max(max(b[1], b[4]) for b in bilder) + 2 * RAND
    W = breite_nummer + 2 * breite_zelle
    H = hoehe_zeile * len(bilder)

    # Grundfläche als RGBA aufbauen (4 Byte je Pixel, deckend) — write_png erwartet RGBA.
    blatt_px = bytearray()
    for _ in range(W * H):
        blatt_px += bytes((GRUND[0], GRUND[1], GRUND[2], 255))

    for i, (nummer, w1, h1, r1, w2, h2, r2) in enumerate(bilder):
        y0 = i * hoehe_zeile
        draw_text(blatt_px, W, H, str(nummer), 8, y0 + RAND + 6, 2, (255, 255, 255))
        _lege(r1, w1, h1, blatt_px, W, H, breite_nummer + (breite_zelle - w1) // 2,
              y0 + (hoehe_zeile - h1) // 2)
        _lege(r2, w2, h2, blatt_px, W, H, breite_nummer + breite_zelle + (breite_zelle - w2) // 2,
              y0 + (hoehe_zeile - h2) // 2)
        for y in range(y0, min(y0 + hoehe_zeile, H)):      # Trennlinie
            p = (y * W + breite_nummer - 1) * 4
            blatt_px[p:p + 3] = bytes((40, 40, 40))

    write_png(ziel_pfad, W, H, bytes(blatt_px))
    print(f"  {ziel_pfad}  {W}x{H}px, {len(bilder)} Zeilen")
    return [z[0] for z in zeilen]


def main() -> int:
    zielordner = WURZEL / "archiv" / "bildstudien" / "icon_preview"
    zielordner.mkdir(parents=True, exist_ok=True)
    gruppen = [
        ("Einheiten_original", "assets/icons/original_units"),
        ("Einheiten_neu", "assets/icons/units"),
        ("Waren", "assets/icons/items"),
    ]
    for name, ordner in gruppen:
        basis = WURZEL / ordner
        dateien = sorted(basis.glob("*.png"))
        zeilen = []
        for i, p in enumerate(dateien, 1):
            sauber = WURZEL / "assets/icons/clean" / p.relative_to(WURZEL / "assets/icons")
            if not sauber.exists():
                print(f"  uebersprungen (nicht aufbereitet): {p.name}")
                continue
            zeilen.append((i, p, sauber))
        if not zeilen:
            continue
        ausgabe = zielordner / f"Vergleich_{name}.png"
        nummern = blatt(zeilen, str(ausgabe))
        print(f"    Nummern: {nummern[0]}-{nummern[-1]}")
        for n, p in zip(nummern, dateien):
            print(f"      {n:>2}  {p.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
