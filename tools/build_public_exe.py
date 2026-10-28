"""Baut die oeffentliche Test-EXE, ohne Entwickler-EXE oder Saves zu ueberschreiben.

Nur unter Windows. Admin-Quellcode wird NICHT aus dem Repository entfernt;
public_start.py sperrt den Zugriff auf die Admin-Oberflaeche.
"""
from __future__ import annotations
import argparse
import hashlib
import os
import shutil
import struct
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME = "Nebelseetal_Remake_Testversion"
OUTPUT = ROOT / "release_public"
ICON = ROOT / "assets" / "icons" / "nebelseetal.ico"
ENTRY = ROOT / "src" / "public_start.py"
DOCS = ("START_HIER.txt", "SYSTEMANFORDERUNGEN.txt", "BEKANNTE_GRENZEN.txt", "FEHLER_MELDEN.txt")

def check() -> None:
    required = [ENTRY, ICON, ROOT / "src" / "ausgabemodus.py", ROOT / "src" / "main.py"]
    required += [ROOT / folder for folder in ("data", "assets")]
    required += [ROOT / "release_vorlage" / name for name in DOCS]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    if missing: raise RuntimeError("Fehlende Dateien: " + ", ".join(missing))
    if ICON.read_bytes()[:4] != b"\0\0\1\0":
        raise RuntimeError("Ungueltige ICO-Datei")

def pack(exe: Path) -> tuple[Path, str]:
    sha = hashlib.sha256(exe.read_bytes()).hexdigest()
    (OUTPUT / "SHA256SUMS.txt").write_text(f"{sha}  {exe.name}\n", encoding="ascii")
    bundle = OUTPUT / f"{NAME}_FIX04j.zip"
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
    ap = argparse.ArgumentParser()
    ap.add_argument("--pruefen", action="store_true")
    args = ap.parse_args()
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
    for f in ("data", "assets"):
        cmd += ["--add-data",str(ROOT/f)+os.pathsep+f]
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
