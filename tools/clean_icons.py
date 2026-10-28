"""
Icon-Hintergrund sauber entfernen.

Befund vom 04.10.2026: alle 45 Icon-Dateien sind zwar RGBA, aber der Alpha-Kanal ist
unbenutzt — jedes Icon traegt seinen Blatt-Hintergrund als deckendes Rechteck mit sich
(Alpha 255 in allen Ecken). Im Spiel erscheint dadurch ein farbiger Kasten.

Dieses Werkzeug entfernt den Hintergrund per Flutfuellung vom Rand aus und schreibt das
Ergebnis in einen **neuen** Ordner. Die Quelldateien werden NIE ueberschrieben — Daniels
17 Dateien in `assets/icons/original_units/` bleiben unangetastet.

Aufruf:
    python tools/clean_icons.py --probe          # nur messen, nichts schreiben
    python tools/clean_icons.py --write          # aufbereitete Kopien schreiben
"""
from __future__ import annotations

import os
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from slice_icons import read_png, to_rgba, write_png

WURZEL = Path(__file__).resolve().parent.parent
QUELLEN = ["assets/icons/original_units", "assets/icons/units", "assets/icons/items"]
ZIEL = "assets/icons/clean"
TOLERANZ = 42          # Abstand je Farbkanal, ab dem ein Pixel noch als Hintergrund gilt


def _abstand(c1, c2) -> int:
    return max(abs(c1[0] - c2[0]), abs(c1[1] - c2[1]), abs(c1[2] - c2[2]))


def _hintergrundfarbe(rgba, w, h):
    """Haeufigste Farbe am Bildrand — das ist der Blatthintergrund."""
    rand = []
    for x in range(w):
        rand.append(tuple(rgba[(0 * w + x) * 4:(0 * w + x) * 4 + 3]))
        rand.append(tuple(rgba[((h - 1) * w + x) * 4:((h - 1) * w + x) * 4 + 3]))
    for y in range(h):
        rand.append(tuple(rgba[(y * w) * 4:(y * w) * 4 + 3]))
        rand.append(tuple(rgba[(y * w + w - 1) * 4:(y * w + w - 1) * 4 + 3]))
    # in Stufen von 8 zusammenfassen, damit Rauschen nicht stoert
    grob = Counter((r // 8 * 8, g // 8 * 8, b // 8 * 8) for r, g, b in rand)
    (br, bg, bb), _ = grob.most_common(1)[0]
    treffer = [p for p in rand if _abstand(p, (br, bg, bb)) <= 24]
    if not treffer:
        return (br, bg, bb)
    n = len(treffer)
    return (sum(p[0] for p in treffer) // n, sum(p[1] for p in treffer) // n, sum(p[2] for p in treffer) // n)


def entferne_hintergrund(pfad: Path, toleranz: int = TOLERANZ):
    """Flutfuellung vom Rand. Gibt (rgba, w, h, hintergrund, entfernt_prozent) zurueck."""
    img = read_png(str(pfad))
    w, h = img["w"], img["h"]
    rgba = to_rgba(img)
    hintergrund = _hintergrundfarbe(rgba, w, h)

    besucht = bytearray(w * h)
    stapel = []
    for x in range(w):
        stapel.append((x, 0))
        stapel.append((x, h - 1))
    for y in range(h):
        stapel.append((0, y))
        stapel.append((w - 1, y))

    entfernt = 0
    while stapel:
        x, y = stapel.pop()
        if x < 0 or y < 0 or x >= w or y >= h:
            continue
        i = y * w + x
        if besucht[i]:
            continue
        besucht[i] = 1
        p = i * 4
        if _abstand((rgba[p], rgba[p + 1], rgba[p + 2]), hintergrund) > toleranz:
            continue                       # das gehoert zur Figur
        if rgba[p + 3] == 0:
            continue                       # schon durchsichtig
        rgba[p + 3] = 0                    # Hintergrund -> durchsichtig
        entfernt += 1
        stapel.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))

    return rgba, w, h, hintergrund, 100.0 * entfernt / (w * h)


def main() -> int:
    schreiben = "--write" in sys.argv
    gesamt = 0
    zeilen = []
    for ordner in QUELLEN:
        basis = WURZEL / ordner
        if not basis.exists():
            continue
        for pfad in sorted(basis.glob("*.png")):
            rgba, w, h, hg, prozent = entferne_hintergrund(pfad)
            gesamt += 1
            zeilen.append((ordner, pfad.name, w, h, hg, prozent))
            if schreiben:
                ziel = WURZEL / ZIEL / pfad.relative_to(WURZEL / "assets/icons")
                write_png(str(ziel), w, h, bytes(rgba))
    print(f"{'Ordner':<26}{'Datei':<34}{'Groesse':>10}{'Hintergrund':>16}{'entfernt':>10}")
    for ordner, name, w, h, hg, prozent in zeilen:
        print(f"{ordner:<26}{name:<34}{f'{w}x{h}':>10}{str(hg):>16}{prozent:8.1f} %")
    if schreiben:
        print(f"\n{gesamt} aufbereitete Kopien in {ZIEL}/ geschrieben.")
        print("Die Quelldateien sind unveraendert.")
    else:
        print(f"\n{gesamt} Dateien gemessen. Nichts geschrieben (--write fehlt).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
