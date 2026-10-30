"""Authentische Rasterbilder der 127 Originalkarten, keine Legacy-Symbole.

UI-frei: prueft die ID gegen den Katalog und verwaltet nur Pfade. Die PNGs
wurden direkt aus den originalen ODT-Kartenbildern (NEAREST, 640x640) erzeugt.
Build aus den Originalquellen: tools/originalkarten_grafiken_bauen.py.
"""
from __future__ import annotations
import json
from pathlib import Path
from functools import lru_cache
import spieldaten

@lru_cache(maxsize=1)
def manifest():
    p = Path(spieldaten.projektwurzel()) / "data/originalkarten/grafik_manifest.json"
    d = json.loads(p.read_text(encoding="utf8"))
    if d["raster"] != [10, 10] or len(d["karten"]) != 127:
        raise ValueError("Originalkarten-Grafikmanifest unvollstaendig")
    return {k["id"]: k for k in d["karten"]}


def grafikpfad(karte: dict) -> Path:
    """Eine Originalkarte. Alte 8x7-Karten werden NICHT gezeichnet."""
    if not isinstance(karte, dict):
        raise ValueError("Ungueltiges Kartendatenformat")
    if (karte.get("spalten") != 10 or karte.get("zeilen") != 10
            or len(karte.get("raster") or ()) != 100):
        raise ValueError("Alte Karte: nur 10x10-Originalkarten sind aktiv")
    ident = karte.get("originalkarte_id")
    if not ident or ident not in manifest():
        raise ValueError("Karte ohne gueltige Original-ID: keine Ersatzgrafik erlaubt")
    p = Path(spieldaten.projektwurzel()) / manifest()[ident]["datei"]
    if not p.is_file():
        raise FileNotFoundError("Originalkarten-Grafik fehlt: " + str(p))
    return p
