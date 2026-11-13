"""Was NICHT in die EXE darf - an EINER Stelle (Daniel 13.11.2026, F-102, Register 627).

**Warum es diese Datei gibt:** In `assets/bilder/` lagen `daniel_portrait.png` und
`daniel_portrait_klein.png` - ein Foto einer echten Person, im Spiel **unbenutzt**. PyInstaller kennt
bei `--add-data` keinen Ausschluss: wer den Ordner `assets` mitgibt, gibt alles mit. Beide Bauwege
(`tools/build_exe.py` fuer die Entwickler-EXE, `tools/build_public_exe.py` fuer die oeffentliche
Ausgabe) kopieren den Ordner deshalb vorher in einen Zwischenordner und lassen diese Namen weg.

Daniels Entscheidung (F-102), woertlich: **"Ja, aus dem Paketbau ausschliessen, die Datei aber im
Projekt lassen"**. Sie bleibt also im Projektordner - fuer die Entwicklung - und wird nur nicht
mitgeliefert.

**Wenn spaeter weitere private Dateien dazukommen:** Namen hier eintragen, sonst reisen sie mit. Die
Wache `tests/test_oeffentliche_ausgabe_portrait.py` prueft, dass beide Bauwege diesen Filter benutzen
und dass die Datei im Projekt noch liegt.
"""

from __future__ import annotations

import shutil
from pathlib import Path

#: Dateinamen (ohne Ordner), die **nie** in ein Paket wandern. Vergleich ueber den Dateinamen,
#: damit auch eine Kopie in einem Unterordner erwischt wird.
PRIVAT = frozenset({
    "daniel_portrait.png",
    "daniel_portrait_klein.png",
})

#: Ordner, die beim Kopieren gar nicht erst angefasst werden (Arbeitsstaende, Zwischenbilder).
NIE_KOPIEREN = frozenset({
    "__pycache__",
})


def _ignorieren(ordner: str, namen: list) -> list:
    """`shutil.copytree`-Rueckruf: sagt, welche Namen in diesem Ordner uebersprungen werden."""
    return [n for n in namen if n in PRIVAT or n in NIE_KOPIEREN]


def kopiere_assets(quelle, ziel) -> list:
    """`assets` nach `ziel` kopieren - ohne private Dateien. Gibt die weggelassenen Pfade zurueck.

    Was hinein geht: Quellordner (normalerweise `<Projekt>/assets`) und Zielordner (der Zwischenordner
    des Paketbaus). Was heraus kommt: die Liste der **weggelassenen** Dateien, relativ zur Quelle, damit
    der Bau sie in sein Protokoll schreiben kann.

    Fehlt die Quelle, wird nichts kopiert und eine leere Liste zurueckgegeben - der Bau bricht dann
    ohnehin spaeter ab, weil `assets` zur Laufzeit fehlt.
    """
    quelle = Path(quelle)
    ziel = Path(ziel)
    weggelassen = []
    if quelle.is_dir():
        for pfad in quelle.rglob("*"):
            if pfad.is_file() and pfad.name in PRIVAT:
                weggelassen.append(str(pfad.relative_to(quelle)).replace("\\", "/"))
    if ziel.exists():
        shutil.rmtree(ziel)
    if quelle.is_dir():
        shutil.copytree(quelle, ziel, ignore=_ignorieren)
    return sorted(weggelassen)
