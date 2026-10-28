"""Baut das EXE-Symbol (`assets/icons/nebelseetal.ico`) aus einem PNG — reine Standardbibliothek.

Warum ein eigenes Werkzeug:
  * Das Spiel laeuft ohne Zusatzpakete; fuer das Symbol wird deshalb **kein Pillow** gebraucht,
    sondern PNG lesen/schreiben und das ICO zusammensetzen laufen ueber `zlib` + `struct`.
  * Das Symbol MUSS **mehrere Groessen** enthalten (16, 32, 48, 64, 128, 256). Mit nur einer
    Groesse zeigt Windows eine unscharf hochgerechnete Fassung — das war der Grund, warum das
    Symbol am 27.08.2026 unbrauchbar klein aussah.
  * Jeder Lauf prueft sich selbst: das geschriebene ICO wird zurueckgelesen, Groessen und
    Bildformat werden geprueft und gemeldet. Kein „muesste passen".

Aufruf:
    python tools/mache_icon.py --quelle assets/icons/nebelseetal_symbol.png
    python tools/mache_icon.py --quelle <bild.png> --ziel assets/icons/nebelseetal.ico --trockenlauf
"""

from __future__ import annotations

import argparse
import os
import shutil
import struct
import sys
import time
import zlib
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
GROESSEN = (16, 32, 48, 64, 128, 256)


def melde(text: str) -> None:
    print(text, flush=True)


# ------------------------------------------------------------------ PNG lesen

def png_lesen(pfad: Path):
    """PNG entschluesseln -> (breite, hoehe, RGBA-Bytes). Filterarten 0-4, Farbtypen 2/3/6."""
    daten = pfad.read_bytes()
    if daten[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{pfad.name}: kein PNG (Kopf {daten[:8]!r})")
    stelle, breite, hoehe, tiefe, farbtyp, plte, idat = 8, 0, 0, 0, 0, b"", b""
    while stelle < len(daten):
        laenge = struct.unpack(">I", daten[stelle:stelle + 4])[0]
        art = daten[stelle + 4:stelle + 8]
        inhalt = daten[stelle + 8:stelle + 8 + laenge]
        if art == b"IHDR":
            breite, hoehe, tiefe, farbtyp = struct.unpack(">IIBB", inhalt[:10])
        elif art == b"PLTE":
            plte = inhalt
        elif art == b"IDAT":
            idat += inhalt
        elif art == b"IEND":
            break
        stelle += 12 + laenge
    if tiefe != 8:
        raise ValueError(f"{pfad.name}: nur 8 Bit je Kanal unterstuetzt (hat {tiefe})")
    kanaele = {2: 3, 3: 1, 6: 4}[farbtyp]
    roh = zlib.decompress(idat)
    zeilenlaenge = breite * kanaele
    zeilen, vorige, stelle = [], bytearray(zeilenlaenge), 0
    for _ in range(hoehe):
        art = roh[stelle]
        stelle += 1
        zeile = bytearray(roh[stelle:stelle + zeilenlaenge])
        stelle += zeilenlaenge
        for i in range(zeilenlaenge):
            a = zeile[i - kanaele] if i >= kanaele else 0
            b = vorige[i]
            c = vorige[i - kanaele] if i >= kanaele else 0
            if art == 1:
                zeile[i] = (zeile[i] + a) & 0xFF
            elif art == 2:
                zeile[i] = (zeile[i] + b) & 0xFF
            elif art == 3:
                zeile[i] = (zeile[i] + (a + b) // 2) & 0xFF
            elif art == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                zeile[i] = (zeile[i] + (a if pa <= pb and pa <= pc else (b if pb <= pc else c))) & 0xFF
        vorige = zeile
        zeilen.append(bytes(zeile))

    rgba = bytearray()
    for zeile in zeilen:
        for x in range(breite):
            st = x * kanaele
            if farbtyp == 6:
                rgba += zeile[st:st + 4]
            elif farbtyp == 2:
                rgba += zeile[st:st + 3] + b"\xff"
            else:  # Farbtyp 3: Palette
                index = zeile[st] * 3
                rgba += plte[index:index + 3] + b"\xff"
    return breite, hoehe, bytes(rgba)


# ------------------------------------------------------------------ Groessen

def verkleinern(breite, hoehe, rgba, neu_w, neu_h):
    """Mittelwert je Zielzelle (sauber beim Verkleinern, korrekt fuer Alphabilder)."""
    neu = bytearray(neu_w * neu_h * 4)
    for zy in range(neu_h):
        y0, y1 = zy * hoehe // neu_h, max(zy * hoehe // neu_h + 1, (zy + 1) * hoehe // neu_h)
        for zx in range(neu_w):
            x0, x1 = zx * breite // neu_w, max(zx * breite // neu_w + 1, (zx + 1) * breite // neu_w)
            r = g = b = a = 0
            for y in range(y0, min(y1, hoehe)):
                basis = y * breite
                for x in range(x0, min(x1, breite)):
                    st = (basis + x) * 4
                    alpha = rgba[st + 3]
                    r += rgba[st] * alpha
                    g += rgba[st + 1] * alpha
                    b += rgba[st + 2] * alpha
                    a += alpha
            ziel = (zy * neu_w + zx) * 4
            if a:
                neu[ziel] = min(255, r // a)
                neu[ziel + 1] = min(255, g // a)
                neu[ziel + 2] = min(255, b // a)
                neu[ziel + 3] = min(255, a // ((y1 - y0) * (x1 - x0)))
            else:
                neu[ziel:ziel + 4] = b"\x00\x00\x00\x00"
    return bytes(neu)


def vergroessern(breite, hoehe, rgba, neu_w, neu_h):
    """Bilinear (nur noetig, wenn die Quelle kleiner als 256 px ist — wird ehrlich gemeldet)."""
    neu = bytearray(neu_w * neu_h * 4)
    for zy in range(neu_h):
        fy = (zy + 0.5) * hoehe / neu_h - 0.5
        y0 = max(0, min(hoehe - 1, int(fy)))
        y1 = min(hoehe - 1, y0 + 1)
        wy = max(0.0, fy - y0)
        for zx in range(neu_w):
            fx = (zx + 0.5) * breite / neu_w - 0.5
            x0 = max(0, min(breite - 1, int(fx)))
            x1 = min(breite - 1, x0 + 1)
            wx = max(0.0, fx - x0)
            ziel = (zy * neu_w + zx) * 4
            for k in range(4):
                links = rgba[(y0 * breite + x0) * 4 + k] * (1 - wx) + rgba[(y0 * breite + x1) * 4 + k] * wx
                rechts = rgba[(y1 * breite + x0) * 4 + k] * (1 - wx) + rgba[(y1 * breite + x1) * 4 + k] * wx
                neu[ziel + k] = int(links * (1 - wy) + rechts * wy + 0.5)
    return bytes(neu)


def png_schreiben(breite, hoehe, rgba):
    """Ein PNG mit Filter 0 je Zeile — die Symbol-Eintraege des ICO sind genau das."""
    roh = bytearray()
    for y in range(hoehe):
        roh.append(0)
        roh += rgba[y * breite * 4:(y + 1) * breite * 4]

    def block(art, inhalt):
        return (struct.pack(">I", len(inhalt)) + art + inhalt
                + struct.pack(">I", zlib.crc32(art + inhalt) & 0xFFFFFFFF))

    return (b"\x89PNG\r\n\x1a\n"
            + block(b"IHDR", struct.pack(">IIBBBBB", breite, hoehe, 8, 6, 0, 0, 0))
            + block(b"IDAT", zlib.compress(bytes(roh), 9))
            + block(b"IEND", b""))


# ------------------------------------------------------------------ ICO

def ico_schreiben(eintraege, ziel: Path) -> None:
    """ICO mit PNG-Nutzlast je Groesse schreiben (Windows Vista+ liest das, tut es seit dem
    27.08.2026 auch fuer die ausgelieferte EXE)."""
    anzahl = len(eintraege)
    kopf = struct.pack("<HHH", 0, 1, anzahl)
    verzeichnis = b""
    nutzlasten = b""
    versatz = 6 + 16 * anzahl
    for breite, hoehe, daten in eintraege:
        verzeichnis += struct.pack("<BBBBHHII", breite % 256, hoehe % 256, 0, 0, 1, 32,
                                   len(daten), versatz + len(nutzlasten))
        nutzlasten += daten
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_bytes(kopf + verzeichnis + nutzlasten)


def ico_pruefen(pfad: Path) -> list:
    """Zuruecklesen: (breite, hoehe, art, bytes) je Eintrag — ehrliche Gegenprobe."""
    daten = pfad.read_bytes()
    if daten[:4] != b"\x00\x00\x01\x00":
        raise ValueError(f"{pfad.name}: keine ICO-Signatur")
    anzahl = struct.unpack("<H", daten[4:6])[0]
    ergebnis = []
    for i in range(anzahl):
        breite, hoehe, _, _, _, bit, laenge, versatz = struct.unpack(
            "<BBBBHHII", daten[6 + 16 * i:22 + 16 * i])
        stueck = daten[versatz:versatz + laenge]
        ist_png = stueck[:8] == b"\x89PNG\r\n\x1a\n"
        masse = struct.unpack(">II", stueck[16:24]) if ist_png else (breite or 256, hoehe or 256)
        ergebnis.append((breite or 256, hoehe or 256, "PNG" if ist_png else "BMP/DIB",
                         bit, laenge, masse))
    return ergebnis


def main() -> int:
    zerleger = argparse.ArgumentParser(description="EXE-Symbol aus einem PNG bauen")
    zerleger.add_argument("--quelle", default=str(WURZEL / "assets" / "icons" / "nebelseetal_symbol.png"))
    zerleger.add_argument("--ziel", default=str(WURZEL / "assets" / "icons" / "nebelseetal.ico"))
    zerleger.add_argument("--trockenlauf", action="store_true", help="nur pruefen, nichts schreiben")
    argumente = zerleger.parse_args()

    quelle, ziel = Path(argumente.quelle), Path(argumente.ziel)
    if not quelle.exists():
        melde(f"FEHLER: Quelle fehlt: {quelle}")
        return 1
    breite, hoehe, rgba = png_lesen(quelle)
    melde(f"Quelle: {quelle.name} — {breite}x{hoehe} Pixel")

    eintraege = []
    for groesse in GROESSEN:
        if groesse == breite:
            daten = png_schreiben(groesse, groesse, rgba)
            weg = "unveraendert uebernommen"
        elif groesse < breite:
            daten = png_schreiben(groesse, groesse, verkleinern(breite, hoehe, rgba, groesse, groesse))
            weg = "verkleinert (Mittelwert)"
        else:
            daten = png_schreiben(groesse, groesse, vergroessern(breite, hoehe, rgba, groesse, groesse))
            weg = "interpoliert (Quelle kleiner!)"
        eintraege.append((groesse, groesse, daten))
        melde(f"  {groesse:>3}x{groesse:<3} {len(daten):>7} Byte  {weg}")

    if argumente.trockenlauf:
        melde("Trockenlauf: nichts geschrieben.")
        return 0

    if ziel.exists():
        # Sicherung NICHT neben das Ziel legen: der Ordner `assets` wird komplett in die EXE
        # gebuendelt, eine Kopie daneben wuerde unnoetig mitreisen.
        sicherungsordner = Path(os.environ.get("LOCALAPPDATA", str(ziel.parent))) / "hermes" / "cache" / "scratch" / "nebel_backup"
        try:
            sicherungsordner.mkdir(parents=True, exist_ok=True)
            zeit = time.strftime("%Y%m%d_%H%M%S")
            sicherung = sicherungsordner / f"{ziel.stem}{ziel.suffix}_alt_{zeit}"
            shutil.copy2(ziel, sicherung)
            melde(f"Vorherige Fassung gesichert: {sicherung}")
        except Exception as fehler:
            melde(f"WARNUNG: Sicherung der vorherigen Fassung nicht moeglich ({fehler})")

    ico_schreiben(eintraege, ziel)
    melde(f"Geschrieben: {ziel} ({ziel.stat().st_size} Byte)")

    melde("Gegenprobe (zurueckgelesen):")
    gefunden = ico_pruefen(ziel)
    for groesse, _, art, bit, laenge, masse in gefunden:
        melde(f"  {groesse:>3}px  {art:7} {bit} Bit  {laenge:>7} Byte  Bild {masse[0]}x{masse[1]}")
    soll = [(g, g) for g in GROESSEN]
    groessen_ist = [eintrag[0] for eintrag in gefunden]
    alle_png = all(eintrag[2] == "PNG" for eintrag in gefunden)
    masse_ok = all(eintrag[5] == (eintrag[0], eintrag[1]) for eintrag in gefunden)
    if groessen_ist != list(GROESSEN) or not alle_png or not masse_ok:
        melde(f"FEHLER: die Gegenprobe stimmt nicht (Groessen {groessen_ist}, PNG {alle_png}, "
              f"Masse {masse_ok}) — Symbol NICHT uebernehmen.")
        return 1
    melde(f"OK: {len(gefunden)} Groessen im Symbol, jede als echtes Bild in der richtigen Groesse.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
