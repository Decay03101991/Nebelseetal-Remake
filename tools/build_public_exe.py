"""Baut die oeffentliche Test-EXE, ohne Entwickler-EXE oder Saves zu ueberschreiben.

Nur unter Windows. Admin-Quellcode wird NICHT aus dem Repository entfernt;
public_start.py sperrt den Zugriff auf die Admin-Oberflaeche.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import shutil
import struct
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
def _version() -> dict:
    """Der Name des Pakets kommt aus `data/version.json` - dieselbe Quelle wie der Entwickler-Bau.

    Daniel 05.11.2026, buchstabengenau: die erste veroeffentlichte Spielversion heisst
    `Nebelseetal_Pre_Release_V_0.0.1.exe`. Bis heute stand hier ein fester Name und eine feste
    Version ("0.5.0-pre.1") - beides war eine zweite Wahrheit neben der Datendatei.
    """
    try:                                                     # Datei lesen
        with open(ROOT / "data" / "version.json", encoding="utf-8") as f:   # feste Datendatei
            daten = json.load(f)                              # Inhalt als dict
    except (OSError, ValueError):                             # fehlt oder kaputt
        return {"dateiname": "Nebelseetal_Remake.exe", "version": "0.0.0"}   # alter Name, alte Zahl
    if not isinstance(daten, dict):                           # kein dict = unbrauchbar
        return {"dateiname": "Nebelseetal_Remake.exe", "version": "0.0.0"}   # alter Name
    dateiname = str(daten.get("dateiname") or "Nebelseetal_Remake.exe").strip()   # Name der EXE
    try:                                                      # Zaehler als Zahl
        nummer = int(daten.get("zaehler") or 0)               # Zahl aus den Daten
    except (TypeError, ValueError):                           # kaputter Wert
        nummer = 0                                            # dann 0
    version = "0.0.%d" % nummer if nummer > 0 else "0.0.0"    # Versionsbezeichnung des Pakets
    return {"dateiname": dateiname, "version": version}       # beide Werte zurueck


_AUS_VERSION = _version()                                     # einmal lesen
NAME = _AUS_VERSION["dateiname"].rsplit(".exe", 1)[0]         # Name ohne Endung
VERSION = _AUS_VERSION["version"]                             # z. B. 0.0.1
OUTPUT = ROOT / "release_public"
ICON = ROOT / "assets" / "icons" / "nebelseetal.ico"
ENTRY = ROOT / "src" / "public_start.py"
DOCS = ("START_HIER.txt", "SYSTEMANFORDERUNGEN.txt", "BEKANNTE_GRENZEN.txt", "FEHLER_MELDEN.txt")

# Daniel 01.11.2026, woertlich: "in der demo exe darf es keine vorhandenen spielstaende geben sie muss
# leer sein." Der Bau prueft deshalb die gebundelten Ordner (data, assets) auf Spielstaende, den
# Admin-Teststand, das Passworttor und Sperrdateien und bricht ab, wenn er etwas findet - lieber keine
# EXE als eine mit fremden Staenden.
SPIELSTAND_MUSTER = ("savegame", "admin_teststand", "tor.json", "game.lock",
                     "spielzeit_einstellung")


def spielstaende_im_paket(wurzel=None) -> list:
    """Spielstaende/Sperren in den gebundelten Ordnern (data, assets) - leer heisst auslieferbar."""
    basis = Path(wurzel) if wurzel is not None else ROOT
    treffer = []
    for ordner in ("data", "assets"):
        pfad = basis / ordner
        if not pfad.is_dir():
            continue
        for datei in sorted(pfad.rglob("*")):
            if not datei.is_file():
                continue
            name = datei.name.lower()
            if any(stueck in name for stueck in SPIELSTAND_MUSTER):
                treffer.append(str(datei.relative_to(basis)))
    return treffer


def check() -> None:
    required = [ENTRY, ICON, ROOT / "src" / "ausgabemodus.py", ROOT / "src" / "main.py"]
    required += [ROOT / folder for folder in ("data", "assets")]
    required += [ROOT / "release_vorlage" / name for name in DOCS]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    if missing: raise RuntimeError("Fehlende Dateien: " + ", ".join(missing))
    if ICON.read_bytes()[:4] != b"\0\0\1\0":
        raise RuntimeError("Ungueltige ICO-Datei")
    staende = spielstaende_im_paket(ROOT)
    if staende:
        raise RuntimeError("Spielstaende im Paket - die Demo muss LEER ausgeliefert werden: "
                           + ", ".join(staende))

def pack(exe: Path) -> tuple[Path, str]:
    """EXE plus Infopaket zu einem ZIP schnueren, SHA256 daneben und im ZIP."""
    sha = hashlib.sha256(exe.read_bytes()).hexdigest()
    (OUTPUT / "SHA256SUMS.txt").write_text(f"{sha}  {exe.name}\n", encoding="ascii")
    bundle = OUTPUT / f"{NAME}.zip"      # der Name traegt die Version schon (data/version.json)
    with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        z.write(exe, exe.name)
        z.write(OUTPUT / "SHA256SUMS.txt", "SHA256SUMS.txt")
        for doc in DOCS:
            z.write(ROOT / "release_vorlage" / doc, doc)
    with zipfile.ZipFile(bundle) as z:
        bad = z.testzip()
        if bad: raise RuntimeError(f"Release-ZIP fehlerhaft: {bad}")
    return bundle, sha

def main() -> int:
    global VERSION
    ap = argparse.ArgumentParser()
    ap.add_argument("--pruefen", action="store_true")
    ap.add_argument("--version", default=VERSION, help="Versionsbezeichnung im Dateinamen, z. B. 0.5.0-pre.1")
    args = ap.parse_args()
    VERSION = args.version
    try: check()
    except Exception as e:
        print("FEHLER (Vorpruefung):", e, file=sys.stderr)
        return 1
    print("Public-Test: Einstieg / Laufzeitdateien / Icon / Infopaket OK.")
    if args.pruefen: return 0
    if sys.platform != "win32":
        print("Windows-Build ist nur unter Windows moeglich", file=sys.stderr)
        return 1
    try: import PyInstaller  # noqa: F401
    except ImportError:
        print("PyInstaller fehlt in der isolierten Bauumgebung", file=sys.stderr)
        return 1
    OUTPUT.mkdir(parents=True, exist_ok=True)
    dist = ROOT / "dist_public_tmp"
    work = ROOT / "build_public_tmp"
    spec = ROOT / f"{NAME}.spec"
    # NICHT die Entwickler-EXE, deren .spec oder private Spielstaende anfassen.
    if dist.exists(): shutil.rmtree(dist)
    if work.exists(): shutil.rmtree(work)
    cmd = [sys.executable,"-m","PyInstaller","--noconfirm","--clean", "--onefile","--noconsole",
           "--name",NAME,"--icon",str(ICON),"--distpath",str(dist),
           "--workpath",str(work),"--specpath",str(ROOT),
           "--paths",str(ROOT/"src")]
    # F-102 (Daniel 13.11.2026): private Dateien NIE mitliefern. PyInstaller kann bei `--add-data`
    # nicht ausschliessen, deshalb wird `assets` vorher gefiltert in den Bauordner kopiert.
    sys.path.insert(0, str(ROOT / "tools"))
    from paket_ausschluss import kopiere_assets
    _weg = kopiere_assets(ROOT / "assets", work / "_paket_assets")
    print("Private Dateien bleiben zurueck:", ", ".join(_weg) if _weg else "keine", flush=True)
    cmd += ["--add-data",str(ROOT/"data")+os.pathsep+"data"]
    cmd += ["--add-data",str(work / "_paket_assets")+os.pathsep+"assets"]
    cmd.append(str(ENTRY))
    print("Erstelle separate oeffentliche Windows-EXE ...",flush=True)
    result = subprocess.run(cmd,cwd=ROOT)
    if result.returncode: return result.returncode
    exe = dist / f"{NAME}.exe"
    if not exe.is_file() or exe.stat().st_size < 3*1024*1024:
        print("FEHLER: Windows-EXE fehlt oder ist zu klein",file=sys.stderr)
        return 1
    with exe.open("rb") as f:
        if f.read(2)!=b"MZ":
            print("FEHLER: Kein PE/Windows-EXE-Header",file=sys.stderr)
            return 1
    target=OUTPUT/exe.name
    shutil.copy2(exe,target)
    zipfile_path,sha=pack(target)
    print("EXE:",target)
    print("Release-Paket:",zipfile_path)
    print("SHA256:",sha)
    print("Manueller Start-/Save-Test und Rechtepruefung fehlen noch.")
    # Aufraeumen nur unsere temporaeren Build-Dateien.
    for p in (work,dist):
        shutil.rmtree(p,ignore_errors=True)
    spec.unlink(missing_ok=True)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
