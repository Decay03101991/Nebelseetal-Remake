"""
Nebelseetal Remake — Icon-Schnitt mit reiner Standardbibliothek.

Zwei Modi:
  --preview   Nur anzeigen: erzeugt pro Blatt ein nummeriertes Kontaktblatt. Schreibt NICHTS
              in assets/. Damit gehen wir die Icons gemeinsam durch.
  --write     Schreibt die freigegebenen Ausschnitte als einzelne PNGs (erst nach Freigabe!).

Grundsaetze (aus den Vorgaenger-Regeln uebernommen):
  * Die Originaldateien werden nie veraendert, umbenannt oder verschoben.
  * Ohne ausdrueckliche Freigabe wird nichts geschrieben.
  * Erkannt wird an echten Trennspalten (Hintergrund ist Schwarz), nicht an einer
    angenommenen Rasterbreite — genau daran ist der frueherere Versuch gescheitert.
"""
from __future__ import annotations

import argparse
import os
import struct
import sys
import zlib

BG_TOL = 18          # Kanalabweichung von Schwarz, ab der ein Pixel als Inhalt gilt
MIN_GAP = 1          # ab so vielen leeren Spalten gilt es als Trennung
MERGE_FACTOR = 1.6   # Blockbreite ab dem Vielfachen der Iconbreite wird geteilt
MIN_BLOCK = 12       # schmalere Spaltenbloecke sind Artefakte (Trennlinien, Sehnen)


# ---------------------------------------------------------------- PNG lesen

def read_png(path: str) -> dict:
    data = open(path, "rb").read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("kein PNG: " + path)
    pos, idat, meta, plte = 8, b"", {}, None
    while pos < len(data):
        ln = struct.unpack(">I", data[pos:pos + 4])[0]
        typ = data[pos + 4:pos + 8]
        chunk = data[pos + 8:pos + 8 + ln]
        if typ == b"IHDR":
            w, h, bd, ct, comp, filt, inter = struct.unpack(">IIBBBBB", chunk)
            meta = dict(w=w, h=h, bd=bd, ct=ct, inter=inter)
        elif typ == b"PLTE":
            plte = chunk
        elif typ == b"IDAT":
            idat += chunk
        elif typ == b"IEND":
            break
        pos += 12 + ln
    if meta.get("inter"):
        raise ValueError("interlaced wird nicht unterstuetzt: " + path)
    bd, ct = meta["bd"], meta["ct"]
    if bd != 8:
        raise ValueError(f"Bittiefe {bd} wird nicht unterstuetzt: {path}")
    nch = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ct]
    w, h = meta["w"], meta["h"]
    raw = zlib.decompress(idat)
    stride = w * nch
    out = bytearray(h * stride)
    prev = bytearray(stride)
    p = 0
    for y in range(h):
        f = raw[p]; p += 1
        line = bytearray(raw[p:p + stride]); p += stride
        if f == 1:
            for i in range(nch, stride):
                line[i] = (line[i] + line[i - nch]) & 255
        elif f == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 255
        elif f == 3:
            for i in range(stride):
                a = line[i - nch] if i >= nch else 0
                line[i] = (line[i] + ((a + prev[i]) >> 1)) & 255
        elif f == 4:
            for i in range(stride):
                a = line[i - nch] if i >= nch else 0
                b = prev[i]
                c = prev[i - nch] if i >= nch else 0
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 255
        out[y * stride:(y + 1) * stride] = line
        prev = line
    return dict(w=w, h=h, ct=ct, nch=nch, px=out, plte=plte)


def to_rgba(img: dict) -> bytearray:
    """Alles auf RGBA bringen, damit nur ein Pfad weiterverarbeitet werden muss."""
    w, h, ct, nch, px = img["w"], img["h"], img["ct"], img["nch"], img["px"]
    if ct == 6:
        return px
    out = bytearray(w * h * 4)
    if ct == 2:
        for i in range(w * h):
            out[i * 4:i * 4 + 3] = px[i * 3:i * 3 + 3]
            out[i * 4 + 3] = 255
    elif ct == 0:
        for i in range(w * h):
            v = px[i]
            out[i * 4:i * 4 + 3] = bytes((v, v, v))
            out[i * 4 + 3] = 255
    elif ct == 4:
        for i in range(w * h):
            v = px[i * 2]
            out[i * 4:i * 4 + 3] = bytes((v, v, v))
            out[i * 4 + 3] = px[i * 2 + 1]
    elif ct == 3:
        pal = img["plte"]
        for i in range(w * h):
            idx = px[i] * 3
            out[i * 4:i * 4 + 3] = pal[idx:idx + 3]
            out[i * 4 + 3] = 255
    return out


# ---------------------------------------------------------------- PNG schreiben

def write_png(path: str, w: int, h: int, rgba: bytes) -> None:
    raw = bytearray()
    stride = w * 4
    for y in range(h):
        raw.append(0)                       # Filter 0 (None)
        raw += rgba[y * stride:(y + 1) * stride]

    def chunk(typ: bytes, data: bytes) -> bytes:
        return (struct.pack(">I", len(data)) + typ + data
                + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF))

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "wb") as f:
        f.write(png)


# ---------------------------------------------------------------- Erkennung

def content_mask(rgba: bytearray, w: int, h: int) -> list[list[bool]]:
    """Inhalt = sichtbar (Alpha) UND heller als der schwarze Hintergrund.

    Wichtig: Alpha allein reicht nicht — die Blätter sind ringsum deckend schwarz,
    ein reiner Alpha-Test würde jeden Pixel als Inhalt zaehlen (frueherer Fehler).
    """
    m = [[False] * w for _ in range(h)]
    for y in range(h):
        row = y * w * 4
        for x in range(w):
            i = row + x * 4
            if rgba[i + 3] > 8 and (rgba[i] > BG_TOL or rgba[i + 1] > BG_TOL
                                    or rgba[i + 2] > BG_TOL):
                m[y][x] = True
    return m


def runs(flags: list[bool], want: bool):
    out, start = [], None
    for i, f in enumerate(list(flags) + [not want]):
        if f == want and start is None:
            start = i
        elif f != want and start is not None:
            out.append((start, i - 1))
            start = None
    return out


def detect_cells(img: dict) -> tuple[list[tuple[int, int, int, int]], dict]:
    """Zellen aus echten Trennspalten ableiten und zu breite Bloecke aufteilen.

    Zwei Fallen, an denen ein reiner Raster-Schnitt scheitert:
      * Manche Nachbar-Icons beruehren sich -> ein Block enthaelt mehrere Icons.
        Aufgeteilt wird an der *schmalsten* Blockbreite (typische Iconbreite), nicht am
        Mittelwert — sonst bleiben Paare zusammen (Karren-Blatt).
      * Einzelne Pixelspalten (Trennlinien, Bogensehnen) sind kein Icon und werden verworfen.
    """
    w, h = img["w"], img["h"]
    rgba = to_rgba(img)
    m = content_mask(rgba, w, h)

    col_has = [any(m[y][x] for y in range(h)) for x in range(w)]
    row_has = [any(m[y][x] for x in range(w)) for y in range(h)]

    y0 = next((i for i, f in enumerate(row_has) if f), 0)
    y1 = next((i for i in range(h - 1, -1, -1) if row_has[i]), h - 1)

    raw_blocks = runs(col_has, True)
    blocks, dropped = [], []
    for a, b in raw_blocks:
        if b - a + 1 < MIN_BLOCK:
            dropped.append((a, b, b - a + 1))
        else:
            blocks.append((a, b))

    widths = sorted(b - a + 1 for a, b in blocks)
    icon_width = widths[0] if widths else 1      # schmalster echter Block = Iconbreite

    cells, split_info = [], []
    for x0, x1 in blocks:
        bw = x1 - x0 + 1
        n = max(1, round(bw / icon_width)) if bw > icon_width * MERGE_FACTOR else 1
        if n > 1:
            split_info.append((x0, x1, bw, n))
        step = bw / n
        for k in range(n):
            cx0 = int(round(x0 + k * step))
            cx1 = int(round(x0 + (k + 1) * step)) - 1
            sub = [any(m[y][x] for y in range(y0, y1 + 1)) for x in range(cx0, cx1 + 1)]
            inner = runs(sub, True)
            if inner:
                cx0 = cx0 + inner[0][0]
                cx1 = cx0 + (inner[-1][1] - inner[0][0])
            cells.append((cx0, y0, cx1 + 1, y1 + 1))
    info = dict(blocks=len(blocks), icon_width=icon_width, splits=split_info,
                dropped=dropped, row_range=(y0, y1), cells=len(cells))
    return cells, info


# ---------------------------------------------------------------- Beschriftung

DIGITS = {
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11111", "00010", "00100", "00010", "00001", "10001", "01110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
}


def draw_text(rgba: bytearray, W: int, H: int, text: str, x: int, y: int,
              scale: int, color=(255, 255, 255)) -> None:
    cx = x
    for ch in text:
        pat = DIGITS.get(ch)
        if pat is None:
            cx += 6 * scale
            continue
        for ry, rowbits in enumerate(pat):
            for rx, bit in enumerate(rowbits):
                if bit != "1":
                    continue
                for dy in range(scale):
                    py = y + ry * scale + dy
                    if not (0 <= py < H):
                        continue
                    for dx in range(scale):
                        px_ = cx + rx * scale + dx
                        if not (0 <= px_ < W):
                            continue
                        i = (py * W + px_) * 4
                        rgba[i:i + 4] = bytes((*color, 255))
        cx += 6 * scale


# ---------------------------------------------------------------- Kontaktblatt

def contact_sheet(img: dict, cells, out_path: str, scale: int = 2,
                  bg=(32, 32, 38), label_scale: int = 3) -> None:
    src = to_rgba(img)
    w = img["w"]
    gap = 8
    label_h = 8 * label_scale
    cw = [scale * (x1 - x0) for (x0, y0, x1, y1) in cells]
    ch = [scale * (y1 - y0) for (x0, y0, x1, y1) in cells]
    W = sum(cw) + gap * (len(cells) + 1)
    H = (max(ch) if ch else 10) + label_h + gap * 2 + 10

    canvas = bytearray(bytes(bg) * (W * H) + b"\xff" * (W * H))
    # Alpha auf 255 setzen
    for i in range(W * H):
        canvas[i * 4 + 3] = 255

    x = gap
    for idx, ((x0, y0, x1, y1), tw, th) in enumerate(zip(cells, cw, ch), start=1):
        for sy in range(y1 - y0):
            for sx in range(x1 - x0):
                si = ((y0 + sy) * w + (x0 + sx)) * 4
                r, g, b, a = src[si], src[si + 1], src[si + 2], src[si + 3]
                if a < 8:
                    continue                       # dahinter bleibt das Blattgrau
                for dy in range(scale):
                    for dx in range(scale):
                        px_ = x + sx * scale + dx
                        py = gap + sy * scale + dy
                        di = (py * W + px_) * 4
                        canvas[di:di + 4] = bytes((r, g, b, 255))
        label = str(idx)
        lw = len(label) * 6 * label_scale - label_scale
        draw_text(canvas, W, H, label, x + max(0, (tw - lw) // 2),
                  gap + max(ch) + 6, label_scale)
        x += tw + gap
    write_png(out_path, W, H, bytes(canvas))


def contact_sheet_grid(img: dict, cells, out_path: str, scale: int = 3, cols: int = 4,
                       bg=(28, 28, 34), label_scale: int = 4, frame=(255, 80, 80)) -> None:
    """Kontaktblatt als Raster: jede Kachel mit grosser Nummer und rotem Schnittrahmen.

    Der rote Rahmen zeigt die tatsaechliche Schnittkante. Beruehrt die Figur den Rahmen,
    ist der Ausschnitt zu knapp — das ist genau der Fehler, der frueher passiert ist.
    """
    src = to_rgba(img)
    w = img["w"]
    n = len(cells)
    cols = max(1, min(cols, n))
    rows = (n + cols - 1) // cols
    gap = 16
    lab = 7 * label_scale + 6

    tws = [scale * (x1 - x0) for (x0, y0, x1, y1) in cells]
    ths = [scale * (y1 - y0) for (x0, y0, x1, y1) in cells]
    tile_w, tile_h = max(tws), max(ths)

    W = cols * tile_w + (cols + 1) * gap
    H = rows * (tile_h + lab) + (rows + 1) * gap
    canvas = bytearray(W * H * 4)
    for i in range(W * H):
        canvas[i * 4:i * 4 + 4] = bytes((*bg, 255))

    def put(px_, py, color):
        if 0 <= px_ < W and 0 <= py < H:
            i = (py * W + px_) * 4
            canvas[i:i + 4] = bytes((*color, 255))

    for idx, ((x0, y0, x1, y1), tw, th) in enumerate(zip(cells, tws, ths), start=1):
        r = (idx - 1) // cols
        c = (idx - 1) % cols
        ox = gap + c * (tile_w + gap)
        oy = gap + r * (tile_h + lab + gap) + lab

        # Nummer gross ueber der Kachel
        label = str(idx)
        lw = len(label) * 6 * label_scale - label_scale
        draw_text(canvas, W, H, label, ox + max(0, (tw - lw) // 2),
                  oy - lab + 3, label_scale, (255, 224, 80))

        # Kachel
        for sy in range(y1 - y0):
            for sx in range(x1 - x0):
                si = ((y0 + sy) * w + (x0 + sx)) * 4
                r_, g_, b_, a_ = src[si], src[si + 1], src[si + 2], src[si + 3]
                if a_ < 8:
                    continue
                for dy in range(scale):
                    for dx in range(scale):
                        put(ox + sx * scale + dx, oy + sy * scale + dy, (r_, g_, b_))

        # Schnittrahmen: zeigt die Kante des Ausschnitts
        for dx in range(tw):
            put(ox + dx, oy, frame)
            put(ox + dx, oy + th - 1, frame)
        for dy in range(th):
            put(ox, oy + dy, frame)
            put(ox + tw - 1, oy + dy, frame)

    write_png(out_path, W, H, bytes(canvas))


def crop_rgba(img: dict, box) -> bytes:
    x0, y0, x1, y1 = box
    rgba = to_rgba(img)
    w = img["w"]
    out = bytearray()
    for y in range(y0, y1):
        out += rgba[(y * w + x0) * 4:(y * w + x1) * 4]
    return bytes(out)


def write_from_map(root: str, map_path: str, dry: bool = False) -> list[str]:
    """Schreibt nur die FEHLENDEN Ausschnitte und legt einen Gesamtindex an.

    Zellen mit vorhandener_datei werden NICHT neu geschnitten — Daniels Dateien bleiben
    die Quelle, sie werden nur unter ihrem Originalnamen im Index gefuehrt. So entsteht
    kein Doppelsatz, und das Spiel hat trotzdem eine vollstaendige Zuordnung.
    """
    import json
    data = json.load(open(map_path, encoding="utf-8"))
    written, problems = [], []
    index = {}
    for sheet, blk in data["blaetter"].items():
        path = target = None
        for sub, t in (("assets/quellbilder/einheiten", "units"), ("assets/quellbilder/waren", "items")):
            p = os.path.join(root, sub, sheet)
            if os.path.exists(p):
                path, target = p, t
                break
        if path is None:
            problems.append(f"Blatt nicht gefunden: {sheet}")
            continue
        img = read_png(path)
        cells, _ = detect_cells(img)
        for z in blk["zellen"]:
            nr = z["nr"]
            name = z["original"]
            if not (1 <= nr <= len(cells)):
                problems.append(f"{sheet}: Zelle {nr} gibt es nicht ({len(cells)} erkannt)")
                continue
            vorhanden = z.get("vorhandene_datei")
            if vorhanden:
                p = os.path.join("assets", "icons", "original_units", vorhanden)
                if not os.path.exists(os.path.join(root, p)):
                    problems.append(f"vorhandene Datei fehlt: {vorhanden}")
                index[name] = {"pfad": p.replace("\\", "/"), "quelle": "vorhanden",
                               "blatt": sheet, "zelle": nr}
                continue
            box = cells[nr - 1]
            outdir = os.path.join(root, "assets", "icons", target)
            os.makedirs(outdir, exist_ok=True)
            out = os.path.join(outdir, name + ".png")
            rel = f"assets/icons/{target}/{name}.png"
            if dry:
                print(f"  wuerde schreiben: {rel}")
            else:
                write_png(out, box[2] - box[0], box[3] - box[1], crop_rgba(img, box))
                written.append(out)
            index[name] = {"pfad": rel, "quelle": "neu", "blatt": sheet, "zelle": nr}

    idx_path = os.path.join(root, "data", "icons_index.json")
    if not dry:
        with open(idx_path, "w", encoding="utf-8") as f:
            json.dump({"_hinweis": "Originalname -> Icon-Datei. 'vorhanden' = Daniels Datei, "
                                  "'neu' = aus dem Blatt geschnitten.",
                       "stand": "2026-10-04", "icons": index}, f,
                      indent=2, ensure_ascii=False)
    neu = sum(1 for v in index.values() if v["quelle"] == "neu")
    alt = sum(1 for v in index.values() if v["quelle"] == "vorhanden")
    print(f"\nNeu geschnitten: {neu} Dateien | vorhandene uebernommen: {alt} | Index: {len(index)} Eintraege")
    if problems:
        print("Probleme:")
        for p in problems:
            print("  -", p)
    return written


# ---------------------------------------------------------------- Hauptlauf

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                  "..", "archiv", "bildstudien", "icon_preview"))
    ap.add_argument("--scale", type=int, default=2)
    ap.add_argument("--only", default="", help="nur Dateien, deren Name das enthaelt")
    args = ap.parse_args()

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sheets = []
    for sub in ("assets/quellbilder/einheiten", "assets/quellbilder/waren"):
        d = os.path.join(root, sub)
        if os.path.isdir(d):
            for f in sorted(os.listdir(d)):
                if f.lower().endswith(".png") and "Sammlung" not in f:
                    sheets.append((sub, f, os.path.join(d, f)))
    if args.only:
        sheets = [s for s in sheets if args.only.lower() in s[1].lower()]

    print(f"{len(sheets)} Blatt/Blätter\n")
    for sub, name, path in sheets:
        img = read_png(path)
        cells, info = detect_cells(img)
        print(f"{sub}\\{name}")
        print(f"   {img['w']}x{img['h']}  Bloecke={info['blocks']}  "
              f"Iconbreite={info['icon_width']}  Zellen={info['cells']}")
        if info["splits"]:
            print(f"   geteilte Blockpaare (beruehrten sich): {info['splits']}")
        if info["dropped"]:
            print(f"   verworfene Splitter: {info['dropped']}")
        print(f"   Zeilenbereich y={info['row_range']}")
        for i, (x0, y0, x1, y1) in enumerate(cells, 1):
            print(f"     {i:2d}. x={x0:4d}..{x1:4d} ({x1-x0:3d} breit)  y={y0}..{y1} ({y1-y0:3d} hoch)")
        if args.preview:
            out = os.path.join(args.out, os.path.splitext(name)[0] + "_nummeriert.png")
            contact_sheet_grid(img, cells, out, scale=args.scale, cols=4)
            print(f"   -> Vorschau: {out}")
        print()
    if args.write:
        write_from_map(root, os.path.join(root, "data", "icon_map.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
