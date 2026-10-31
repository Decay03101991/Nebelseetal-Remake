"""Drei stabile, unabhaengige Speicherslots und ein gesonderter Admin-Teststand.

Die bestehende savegame.json bleibt als Altstand erhalten und wird NICHT migriert.
Dieses Modul hat bewusst keine GUI und keine Spielregeln.
"""
from __future__ import annotations

import os
from pathlib import Path

SLOTS = (1, 2, 3)


def ordner_vorbereiten(ordner: str) -> str:
    """Legt den Speicherordner an, falls er fehlt, und gibt seinen Pfad zurueck."""
    p = Path(ordner)
    p.mkdir(parents=True, exist_ok=True)
    return str(p)


def slot_pfad(ordner: str, nummer: int) -> str:
    """Dateipfad eines Speicherslots (nur 1, 2 oder 3 sind zulaessig)."""
    if type(nummer) is not int or nummer not in SLOTS:
        raise ValueError("Nur die Speicherslots 1, 2 oder 3 sind zulaessig.")
    return str(Path(ordner) / f"savegame_slot{nummer}.json")


def altstand_pfad(ordner: str) -> str:
    """Pfad des alten Einzelspielstands (savegame.json) - nur fuer die Migration."""
    return str(Path(ordner) / "savegame.json")


def admin_pfad(ordner: str) -> str:
    """Pfad des Admin-Teststands (admin_teststand.json)."""
    return str(Path(ordner) / "admin_teststand.json")


def slot_status(ordner: str, nummer: int) -> str:
    """Beschriftung ohne Aenderung am Stand; Fehler sind sichtbar, nicht 'leer'."""
    import speichern
    pfad = slot_pfad(ordner, nummer)
    if not os.path.isfile(pfad):
        return f"Slot {nummer}: leer"
    daten, fehler = speichern.lade(pfad)
    if daten is None:
        return f"Slot {nummer}: NICHT LESBAR ({fehler})"
    if daten.get("admin_teststand"):
        return f"Slot {nummer}: ADMIN-DATEN (gesperrt)"
    dorf = len(daten.get("settlements", []))
    tag = daten.get("day", "?")
    return f"Slot {nummer}: Tag {tag}, {dorf} Siedlung(en)"
