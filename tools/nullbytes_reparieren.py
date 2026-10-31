"""Entfernt Null-Bytes aus Textdateien (einmaliger Reparaturlauf, 31.10.2026).

Hintergrund: beim Schreiben ueber die Shell sind in zwei Dateien Null-Bytes gelandet
(`Finanzen\\x00_Uebersicht`). Sie machen Dateien fuer grep zu "Binaerdateien" und werden von
manchen Editoren stillschweigend abgeschnitten.

Aufruf:
    python -X utf8 tools/nullbytes_reparieren.py --pruefen
    python -X utf8 tools/nullbytes_reparieren.py --schreiben
"""
from __future__ import annotations

import os
import sys

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENDUNGEN = (".md", ".py", ".txt", ".json", ".csv", ".log")


def dateien():
    for ordner in ("docs", os.path.join("docs", "audits"), "src", "tests", "tools", "."):
        voll = os.path.join(HIER, ordner)
        if not os.path.isdir(voll):
            continue
        for name in sorted(os.listdir(voll)):
            pfad = os.path.join(voll, name)
            if os.path.isfile(pfad) and name.endswith(ENDUNGEN) and os.path.getsize(pfad) < 3_000_000:
                yield pfad


def main() -> int:
    schreiben = "--schreiben" in sys.argv
    treffer = 0
    for pfad in dateien():
        with open(pfad, "rb") as f:
            roh = f.read()
        anzahl = roh.count(b"\x00")
        if not anzahl:
            continue
        treffer += 1
        print(f"{os.path.relpath(pfad, HIER):56s} {anzahl} Null-Byte(s)")
        if schreiben:
            # Null-Bytes durch einen einfachen Schraegstrich ersetzen (Pfadtrenner-Reparatur)
            with open(pfad, "wb") as f:
                f.write(roh.replace(b"\x00", b"\\"))
    print(f"\nDateien mit Null-Bytes: {treffer} ({'repariert' if schreiben else 'nur gemeldet'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
