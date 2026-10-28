"""
Baut die ausgelieferte Einzeldatei ``Nebelseetal_Remake.exe`` (Schritt 9 in `docs/WEG_ZUR_EXE.md`).

Warum ein eigenes Skript und kein Aufruf von Hand:
  * Der Build muss **nachprüfbar** sein — jede Stufe prueft sich selbst und bricht bei einem
    Zweifel ab, statt eine halbe EXE stehen zu lassen.
  * Es darf am Ende **genau eine** EXE im Zielordner liegen (Regel aus dem Vorfall mit dem alten
    Build vom 27.08.2026).
  * Das Spiel selbst bleibt **ohne Zusatzpakete** (nur Standardbibliothek). PyInstaller laeuft in
    einer eigenen Bau-Umgebung ausserhalb des Projekts — hier wird nur damit aufgerufen.

Aufruf (die Bau-Umgebung bringt PyInstaller mit):

    python tools/build_exe.py --pruefen
    python tools/build_exe.py --python <bau-venv>/Scripts/python.exe

Danach steht im Projektordner ``Nebelseetal_Remake.exe`` samt Pruefbericht auf der Konsole.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import struct
import subprocess
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
NAME = "Nebelseetal_Remake"
ICON = WURZEL / "assets" / "icons" / "nebelseetal.ico"
BAUORDNER = WURZEL / "build"          # Arbeitsordner von PyInstaller (danach weg)
VERTEILORDNER = WURZEL / "dist"       # Zwischenablage der fertigen EXE (danach weg)
SPEC_DATEI = WURZEL / f"{NAME}.spec"

# Was ins Programm kommt: die Spiel-Daten und die Bilddateien. `docs/` braucht das Spiel zur
# Laufzeit NICHT (nur die Entwicklungsarbeit liest dort).
MITGEBEN = [("data", "data"), ("assets", "assets")]

MINDESTGROESSE = 3 * 1024 * 1024      # eine echte Einzeldatei ist mehrere MB gross


def melde(text: str) -> None:
    print(f"  {text}", flush=True)


def ico_groessen(pfad: Path) -> list:
    """Die im ICO enthaltenen Bildgroessen (leer, wenn es kein ICO ist)."""
    daten = pfad.read_bytes()
    if daten[:4] != b"\x00\x00\x01\x00":
        return []
    anzahl = struct.unpack("<H", daten[4:6])[0]
    return [(daten[6 + 16 * i] or 256, daten[7 + 16 * i] or 256) for i in range(anzahl)]


def pruefe_voraussetzungen() -> list:
    """Prueft alles, was zum Bauen noetig ist — und meldet ehrlich, was fehlt."""
    fehler = []
    melde(f"Projektordner: {WURZEL}")
    if not (WURZEL / "src" / "main.py").exists():
        fehler.append("src/main.py fehlt")
    for quelle, _ziel in MITGEBEN:
        if not (WURZEL / quelle).exists():
            fehler.append(f"mitzugebender Ordner fehlt: {quelle}")
    groessen = ico_groessen(ICON) if ICON.exists() else []
    if not groessen:
        fehler.append(f"Symbol fehlt oder ist kein ICO: {ICON}")
    else:
        melde(f"Symbol: {ICON.name} mit {len(groessen)} Groessen {groessen}")
    if not (WURZEL / "docs" / "WEG_ZUR_EXE.md").exists():
        fehler.append("docs/WEG_ZUR_EXE.md fehlt (der Weg zur EXE ist die Richtschnur)")
    for datei in sorted(WURZEL.glob("*.exe")):
        melde(f"ACHTUNG: im Projektordner liegt schon eine EXE: {datei.name}")
    return fehler


def saeubere() -> None:
    """Reste eines frueheren Baus entfernen — vor UND nach dem Bauen."""
    for ordner in (BAUORDNER, VERTEILORDNER):
        if ordner.exists():
            shutil.rmtree(ordner, ignore_errors=True)
    if SPEC_DATEI.exists():
        SPEC_DATEI.unlink()
    for unter in ("src", "tests", "tools"):
        pycache = WURZEL / unter / "__pycache__"
        if pycache.exists():
            shutil.rmtree(pycache, ignore_errors=True)


def baue(python: str) -> int:
    """Ruft PyInstaller auf. Rueckgabe: Exit-Code."""
    befehl = [
        python, "-m", "PyInstaller",
        "--noconfirm", "--clean", "--onefile", "--noconsole",
        "--name", NAME,
        "--icon", str(ICON),
        "--distpath", str(VERTEILORDNER),
        "--workpath", str(BAUORDNER),
        "--specpath", str(WURZEL),
        "--paths", str(WURZEL / "src"),
    ]
    for quelle, ziel in MITGEBEN:
        befehl += ["--add-data", f"{WURZEL / quelle}{os.pathsep}{ziel}"]
    befehl.append(str(WURZEL / "src" / "main.py"))
    melde("Aufruf: " + " ".join(befehl[:8]) + " …")
    ergebnis = subprocess.run(befehl, cwd=str(WURZEL))
    return ergebnis.returncode


def pruefe_ergebnis() -> Path:
    """Prueft die fertige EXE und legt sie in den Projektordner (genau eine!)."""
    kandidaten = sorted(VERTEILORDNER.glob("*.exe")) if VERTEILORDNER.exists() else []
    if len(kandidaten) != 1:
        raise SystemExit(f"FEHLER: erwartet genau eine EXE im Bauordner, gefunden {len(kandidaten)}")
    exe = kandidaten[0]
    groesse = exe.stat().st_size
    if groesse < MINDESTGROESSE:
        raise SystemExit(f"FEHLER: die EXE ist mit {groesse} Byte zu klein — da fehlt etwas")

    ziel = WURZEL / exe.name
    # Atomarer Austausch: Bei Schreibfehlern bleibt die alte EXE unversehrt.
    zwischen = WURZEL / (exe.name + ".neubau.tmp")
    try:
        shutil.copy2(exe, zwischen)
        os.replace(zwischen, ziel)
    finally:
        if zwischen.exists():
            zwischen.unlink()

    weitere = [p.name for p in WURZEL.glob("*.exe") if p.name != ziel.name]
    if weitere:
        raise SystemExit(f"FEHLER: im Projektordner liegen mehrere EXE: {weitere}")

    summe = hashlib.sha256(ziel.read_bytes()).hexdigest()
    melde(f"fertig: {ziel}")
    melde(f"Groesse: {groesse} Byte ({groesse / 1024 / 1024:.1f} MB)")
    melde(f"SHA256:  {summe}")
    melde(f"EXE im Projektordner: {[p.name for p in WURZEL.glob('*.exe')]}")
    return ziel


def feiere_symbol_cache() -> None:
    """Windows den Symbol-Zwischenspeicher auffrischen lassen (best effort)."""
    for befehl in (["ie4uinit.exe", "-show"],):
        try:
            subprocess.run(befehl, timeout=20, capture_output=True)
            melde("Windows-Symbolcache aufgefrischt (ie4uinit.exe -show).")
        except Exception as fehler:                      # darf den Bau nicht kippen
            melde(f"Symbolcache nicht aufgefrischt ({type(fehler).__name__}) — kein Fehler.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Baut die Nebelseetal-Remake.exe")
    parser.add_argument("--python", default=os.environ.get("NEBEL_BUILD_PYTHON", sys.executable),
                        help="Python der Bau-Umgebung (muss PyInstaller haben)")
    parser.add_argument("--pruefen", action="store_true",
                        help="nur die Voraussetzungen pruefen, nichts bauen")
    parser.add_argument("--ohne-saeubern", action="store_true",
                        help="Reste nicht entfernen (nur fuer Sonderfaelle)")
    args = parser.parse_args()

    print("Nebelseetal Remake — Bau der Einzeldatei (Schritt 9)")
    fehler = pruefe_voraussetzungen()
    if fehler:
        for f in fehler:
            melde(f"FEHLT: {f}")
    if args.pruefen:
        melde("Pruefung beendet." + ("" if not fehler else " Voraussetzungen fehlen."))
        return 1 if fehler else 0
    if fehler:
        melde("Bau abgebrochen — die Voraussetzungen fehlen.")
        return 1
    if sys.platform != "win32":
        melde("ABBRUCH: Windows-.exe darf nur auf Windows gebaut werden; "
              "PyInstaller kann nicht von Linux nach Windows kreuzkompilieren.")
        return 2

    if not args.ohne_saeubern:
        saeubere()
    code = baue(args.python)
    if code != 0:
        melde(f"PyInstaller brach mit Code {code} ab — es bleibt KEINE neue EXE stehen.")
        saeubere()
        return code

    pruefe_ergebnis()
    feiere_symbol_cache()
    saeubere()
    melde("Aufgeraeumt: build/, dist/, .spec und __pycache__ sind entfernt. "
          "Im Projektordner liegt genau eine EXE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
