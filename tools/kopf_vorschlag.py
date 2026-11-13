"""Pruefstand-Kopf vorschlagen und schreiben (M1, Claude Nr. 16).

Schreibt die vier Kopfangaben in eine Pruefdatei - als VORSCHLAG aus Paket 15b, also aus den
gemessenen Daten des Sammellaufs, nicht aus dem Gedaechtnis:

    PRUEF_ART = "fenster"                 # rechnen | fenster | quelltext (optional "+messen")
    PRUEF_STUFE = 2                       # 1..4
    PRUEF_BETRIFFT = ["main:*", "gelaende"]
    PRUEF_DATEN = ["gelaende.json"]

Konvention, die dieses Werkzeug einfuehrt (und die `tools/auswahl.py` liest):
  * `modul`       - eine Aenderung an diesem Modul zieht die Datei
  * `modul:fn`    - nur diese Funktion des Moduls (M2, Regel 6)
  * `main:*`      - irgendeine Funktion in `main.py` - ehrliche Uebergangsform fuer die 184
                    Dateien, die heute an `main` haengen; sie wird beim Anfassen genauer.

Stufe (Startregel aus Nr. 16, M1 Punkt c):
  1 = rechnen/quelltext unter 2 s
  2 = fenster bis 20 s oder rechnen ab 2 s
  3 = alles Uebrige
  4 = die neun T4-Dateien (vor jeder EXE und woechentlich)

Aufruf:
  python -X utf8 tools/kopf_vorschlag.py --pruefen            # nur zeigen, nichts schreiben
  python -X utf8 tools/kopf_vorschlag.py --paket 0 20         # Paket 1 (die ersten 20)
  python -X utf8 tools/kopf_vorschlag.py                      # alle, die noch keinen Kopf haben
"""
from __future__ import annotations

import argparse
import ast
import csv
import os
import re
import sys

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS = os.path.join(HIER, "tests")
PAKET = os.path.join(HIER, "docs", "auftraege", "PAKET_15B_PRUEFDATEIEN_20261112.csv")
FELDER = ("PRUEF_ART", "PRUEF_STUFE", "PRUEF_BETRIFFT", "PRUEF_DATEN")

# Die acht langen Dateien (Claude, Nr. 16, Punkt 7) - sie laufen nur vor einer EXE und woechentlich.
T4 = ("test_produktionskette_ohne_cheats.py", "test_durchspiel.py", "test_overlay_ingame.py",
      "test_doppelpuffer.py", "test_bot_gruendung.py", "test_bot_takt_scheiben.py",
      "test_bot_warenkette.py", "test_kaserne_ohne_gebaeude.py", "test_e2e_wege.py")


def paket_lesen(pfad: str = PAKET) -> list:
    """Paket 15b als Liste von Woerterbuechern (Trenner ';', UTF-8 mit BOM)."""
    with open(pfad, encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh, delimiter=";"))


def stufe_fuer(zeile: dict) -> int:
    """Die Startstufe aus Art und Dauer (Nr. 16, M1c)."""
    datei = zeile.get("datei", "")
    name = datei if datei.endswith(".py") else datei + ".py"
    if name in T4:
        return 4
    art = (zeile.get("art") or "").strip().lower()
    try:
        dauer = float(zeile.get("dauer_s") or 0.0)
    except (TypeError, ValueError):
        dauer = 0.0
    rechnen = art.startswith("rechnen") or art.startswith("quelltext")
    if rechnen:
        return 1 if dauer < 2.0 else 2
    if art.startswith("fenster"):
        return 2 if dauer <= 20.0 else 3
    return 3


def betrifft_fuer(zeile: dict) -> list:
    """BETRIFFT aus der Spalte `src_module`; `main` wird zu `main:*` (Uebergangsform)."""
    module = [m for m in (zeile.get("src_module") or "").split() if m]
    ergebnis = []
    for modul in module:
        ergebnis.append("main:*" if modul == "main" else modul)
    return sorted(set(ergebnis))


def daten_fuer(zeile: dict) -> list:
    """DATEN aus der Spalte `daten`."""
    return sorted({d for d in (zeile.get("daten") or "").split() if d})


def kopf_zeilen(zeile: dict) -> list:
    """Die Kopfzeilen als Text (ASCII, ohne Zeilenenden)."""
    art = (zeile.get("art") or "rechnen").strip()
    return [
        "# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------",
        "# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b",
        "# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.",
        'PRUEF_ART = "%s"' % art,
        "PRUEF_STUFE = %d" % stufe_fuer(zeile),
        "PRUEF_BETRIFFT = %s" % repr(betrifft_fuer(zeile)),
        "PRUEF_DATEN = %s" % repr(daten_fuer(zeile)),
        "# --- Ende Pruefstand-Kopf -------------------------------------------------------",
    ]


def hat_kopf(pfad: str) -> bool:
    """Traegt die Datei schon einen Kopf? (AST, ohne Import)"""
    try:
        with open(pfad, encoding="utf-8", errors="replace") as fh:
            baum = ast.parse(fh.read())
    except (OSError, SyntaxError):
        return False
    for knoten in baum.body:
        if isinstance(knoten, ast.Assign) and len(knoten.targets) == 1:
            ziel = knoten.targets[0]
            if isinstance(ziel, ast.Name) and ziel.id in FELDER:
                return True
    return False


def einfuegezeile(quelle: str) -> int:
    """Nach welcher Zeile (0-basiert) der Kopf beginnt.

    Der Kopf enthaelt Zuweisungen und darf darum NICHT vor `from __future__ import ...` stehen
    (Python verlangt diese Zeilen ganz oben). Reihenfolge: Coding-Zeile, Docstring, alle
    `__future__`-Importe - danach der Kopf.
    """
    zeilen = quelle.splitlines()
    start = 0
    for index in range(min(2, len(zeilen))):
        if re.search(r"coding[:=]", zeilen[index]):
            start = index + 1
    try:
        baum = ast.parse(quelle)
    except SyntaxError:
        return start
    for knoten in baum.body:
        if isinstance(knoten, ast.Expr) and isinstance(getattr(knoten, "value", None),
                                                      ast.Constant) and \
                isinstance(knoten.value.value, str):
            start = max(start, getattr(knoten, "end_lineno", start) or start)
            continue
        if isinstance(knoten, ast.ImportFrom) and knoten.module == "__future__":
            start = max(start, getattr(knoten, "end_lineno", start) or start)
            continue
        break
    return start


def kopf_schreiben(pfad: str, zeile: dict) -> bool:
    """Den Kopf in die Datei schreiben; Zeilenenden der Datei bleiben erhalten."""
    with open(pfad, "rb") as fh:
        roh = fh.read()
    text = roh.decode("utf-8")
    ende = "\r\n" if "\r\n" in text[:2000] else "\n"
    zeilen = text.splitlines()
    stelle = einfuegezeile(text)
    kopf = kopf_zeilen(zeile)
    neu = zeilen[:stelle] + ([""] if stelle and zeilen[stelle - 1].strip() else []) + kopf + zeilen[stelle:]
    with open(pfad, "wb") as fh:
        fh.write((ende.join(neu) + ende).encode("utf-8"))
    return True


def main(argv=None) -> int:
    leser = argparse.ArgumentParser(description="Pruefstand-Kopf schreiben (M1)")
    leser.add_argument("--paket", nargs=2, type=int, metavar=("NR", "GROESSE"),
                       help="nur ein Paket (0-basiert)")
    leser.add_argument("--pruefen", action="store_true", help="nur zeigen, nichts schreiben")
    leser.add_argument("--alle", action="store_true", help="auch Dateien mit Kopf neu schreiben")
    args = leser.parse_args(argv)
    zeilen = paket_lesen()
    if args.paket:
        nummer, groesse = args.paket
        zeilen = zeilen[nummer * groesse:(nummer + 1) * groesse]
    geschrieben, uebersprungen, fehlend = [], [], []
    for zeile in zeilen:
        name = zeile.get("datei") or ""
        pfad = os.path.join(TESTS, name if name.endswith(".py") else name + ".py")
        if not os.path.exists(pfad):
            fehlend.append(name)
            continue
        if not args.alle and hat_kopf(pfad):
            uebersprungen.append(name)
            continue
        if args.pruefen:
            print("%-52s Stufe %d, Art %s, BETRIFFT %s, DATEN %s"
                  % (name, stufe_fuer(zeile), zeile.get("art"),
                     ",".join(betrifft_fuer(zeile)) or "-", ",".join(daten_fuer(zeile)) or "-"))
            continue
        kopf_schreiben(pfad, zeile)
        geschrieben.append(name)
    if args.pruefen:
        print("\n%d Dateien im Paket, %d uebersprungen (Kopf vorhanden), %d fehlen"
              % (len(zeilen), len(uebersprungen), len(fehlend)))
        return 0
    print("Kopf geschrieben: %d Dateien" % len(geschrieben))
    if uebersprungen:
        print("  schon vorhanden: %d" % len(uebersprungen))
    if fehlend:
        print("  NICHT GEFUNDEN: %s" % ", ".join(fehlend))
    for name in geschrieben:
        print("  %s" % name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
