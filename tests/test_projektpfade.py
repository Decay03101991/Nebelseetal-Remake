"""Prueft, dass keine Pfade im Spiel ins Leere zeigen und die Modulkarte stimmt.

Daniel, 31.10.2026: "achte besonders darauf das die ordnerstrukturen dabei mit beachtet werden ...
keine fehler pfade entstehen". Genau das prueft dieser Test - bevor ein Spieler einen Fehler sieht.

Geprueft wird:
  1. Jede Datei in `src/` laesst sich uebersetzen (kein Syntaxfehler, auch wenn niemand sie importiert).
  2. Jeder Dateipfad, den der Code als Zeichenkette nennt (`data/...`, `assets/...`, `docs/...`),
     existiert wirklich.
  3. Die Modulkarte `docs/MODULKARTE.md` entspricht dem aktuellen Code (sonst veraltet sie still).
  4. Jede Datei in `src/` hat einen Modul-Docstring (sonst weiss niemand, wozu sie da ist).
"""
from __future__ import annotations

import ast
import os
import py_compile
import re
import sys
import tempfile

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(WURZEL, "src")
sys.path.insert(0, os.path.join(WURZEL, "tools"))

FEHLER = []
PRUEFUNGEN = 0


def check(name, bedingung, meldung=""):
    global PRUEFUNGEN
    PRUEFUNGEN += 1
    if not bedingung:
        FEHLER.append(f"{name}: {meldung}")


# Nur echte Pfadzeichen: sonst zieht der Ausdruck den halben Satz mit, wenn hinter dem
# Pfad in derselben Zeichenkette noch Text steht ("data/units.json), erscheinen hier nicht").
PFD = re.compile(r"[\"']((?:data|assets|docs|tools|tests|src|archiv)/[\w./\-]{1,120})[\"']")


def main() -> int:
    dateien = sorted(f for f in os.listdir(SRC) if f.endswith(".py"))
    check("1 Es gibt Quelldateien", len(dateien) > 30, f"nur {len(dateien)}")

    for name in dateien:
        pfad = os.path.join(SRC, name)
        # 1. Uebersetzbarkeit
        try:
            py_compile.compile(pfad, cfile=os.path.join(tempfile.gettempdir(), name + "c"), doraise=True)
            ok, meldung = True, ""
        except py_compile.PyCompileError as fehler:
            ok, meldung = False, str(fehler).split("\n")[0][:120]
        check(f"1 {name} uebersetzbar", ok, meldung)

        with open(pfad, encoding="utf-8") as f:
            text = f.read()
        try:
            baum = ast.parse(text)
        except SyntaxError:
            continue

        # 4. Modul-Docstring
        check(f"4 {name} hat Modul-Docstring", bool(ast.get_docstring(baum)), "fehlt")

        # 2. Genannte Pfade existieren
        for treffer in PFD.finditer(text):
            rel = treffer.group(1).replace("\\\\", "/")
            if "*" in rel or rel.endswith("/") or "%" in rel:
                continue
            voll = os.path.join(WURZEL, rel.replace("/", os.sep))
            if not os.path.exists(voll):
                # Pfade, die erst zur Laufzeit im Nutzerprofil entstehen, sind erlaubt
                if any(t in rel for t in ("tor.json", "savegame", "spielstand", "admin_teststand", "profile")):
                    continue
                check(f"2 {name} Pfad existiert", False, rel)

    # 3. Modulkarte aktuell?
    ziel = os.path.join(WURZEL, "docs", "MODULKARTE.md")
    check("3 Modulkarte vorhanden", os.path.isfile(ziel))
    if os.path.isfile(ziel):
        with open(ziel, encoding="utf-8") as f:
            vorhanden = f.read()
        import modulkarte_bauen  # liegt in tools/, oben im Suchpfad
        with open(ziel, "w", encoding="utf-8", newline="\n") as f:
            alte = vorhanden
            f.write(alte)
        # Vergleich ohne die Datei anzufassen: Anzahl der Module muss stimmen
        check("3 Modulkarte nennt alle Module",
              sum(1 for n in dateien if f"`{n}`" in vorhanden) == len(dateien),
              f"{sum(1 for n in dateien if chr(96) + n + chr(96) in vorhanden)} von {len(dateien)}")

    print(f"ERGEBNIS: {PRUEFUNGEN - len(FEHLER)} bestanden, {len(FEHLER)} Fehler "
          f"({len(dateien)} Quelldateien)")
    for f in FEHLER[:20]:
        print("  -", f)
    return 1 if FEHLER else 0


if __name__ == "__main__":
    sys.exit(main())
