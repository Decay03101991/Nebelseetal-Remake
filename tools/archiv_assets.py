"""
Original-Website-Assets aus dem Web-Archiv sichern.

Laedt alle Bild- und Flash-Dateien von nebelseetal.de aus web.archive.org ins Projekt,
spiegelt die Originalpfade und schreibt eine Quellendatei.

Aufruf:  python tools/archiv_assets.py            # nur auflisten
         python tools/archiv_assets.py --laden    # herunterladen
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
ZIEL = WURZEL / "docs" / "original" / "assets_website"
CDX = ("https://web.archive.org/cdx/search/cdx?url=nebelseetal.de*&output=json"
       "&fl=original,timestamp,statuscode,mimetype&collapse=urlkey&limit=3000")
ENDUNGEN = (".gif", ".jpg", ".jpeg", ".png", ".swf", ".bmp", ".ico")


def hole(url: str, roh: bool = False, versuche: int = 3):
    for n in range(versuche):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Recherche)"})
            with urllib.request.urlopen(req, timeout=60) as a:
                return a.read() if roh else a.read().decode("utf-8", errors="replace")
        except Exception:
            if n == versuche - 1:
                raise
            time.sleep(2 + 2 * n)


def liste() -> list:
    daten = json.loads(hole(CDX))
    kopf, *zeilen = daten
    idx = {name: i for i, name in enumerate(kopf)}
    treffer = []
    for z in zeilen:
        orig = z[idx["original"]]
        ts = z[idx["timestamp"]]
        code = z[idx["statuscode"]]
        mime = z[idx.get("mimetype", 0)] if "mimetype" in idx else ""
        pfad = urllib.parse.urlparse(orig).path
        if pfad.lower().endswith(ENDUNGEN) or mime.startswith("image/") or "flash" in mime:
            treffer.append({"original": orig, "timestamp": ts, "statuscode": code, "mimetype": mime})
    return treffer


def ist_bild(daten: bytes) -> bool:
    return (daten[:6] in (b"GIF87a", b"GIF89a") or daten[:2] == b"\xff\xd8"
            or daten[:8] == b"\x89PNG\r\n\x1a\n" or daten[:3] == b"CWS"
            or daten[:3] == b"FWS" or daten[:4] == b"RIFF")


def main() -> int:
    laden = "--laden" in sys.argv
    alle = liste()
    print(f"{len(alle)} Bild-/Flash-Dateien im Archiv gefunden.")
    if not alle:
        return 1
    ZIEL.mkdir(parents=True, exist_ok=True)
    zeilen = ["# Original-Assets der Website nebelseetal.de",
              "",
              "Quelle: web.archive.org. Diese Dateien sind Belegmaterial — sie werden NICHT ins Spiel",
              "eingebaut, solange Daniel sie nicht freigegeben hat.",
              "",
              "| Zeitstempel | Original-URL | Datei im Projekt | Groesse | Status |",
              "|---|---|---|---|---|"]
    geladen = fehlgeschlagen = 0
    for e in sorted(alle, key=lambda x: x["original"]):
        pfad = urllib.parse.urlparse(e["original"]).path.lstrip("/") or "index"
        ziel = ZIEL / pfad.replace("/", os.sep)
        ziel.parent.mkdir(parents=True, exist_ok=True)
        if not laden:
            print(f"  {e['timestamp']}  {e['original']}")
            continue
        if ziel.exists() and ziel.stat().st_size > 0:
            zeilen.append(f"| {e['timestamp']} | {e['original']} | {pfad} | vorhanden | ok |")
            continue
        try:
            daten = hole(f"https://web.archive.org/web/{e['timestamp']}if_/{e['original']}", roh=True)
        except Exception as exc:
            fehlgeschlagen += 1
            zeilen.append(f"| {e['timestamp']} | {e['original']} | - | - | Fehler: {type(exc).__name__} |")
            continue
        if not ist_bild(daten):
            fehlgeschlagen += 1
            zeilen.append(f"| {e['timestamp']} | {e['original']} | - | - | keine Bilddatei |")
            continue
        ziel.write_bytes(daten)
        geladen += 1
        zeilen.append(f"| {e['timestamp']} | {e['original']} | {pfad} | {len(daten)} B | ok |")
        print(f"  geladen: {pfad}  ({len(daten)} B)")
    if laden:
        (ZIEL / "QUELLEN.md").write_text("\n".join(zeilen) + "\n", encoding="utf-8")
        print(f"\n{geladen} geladen, {fehlgeschlagen} fehlgeschlagen.")
        print(f"Quellen: {ZIEL / 'QUELLEN.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
