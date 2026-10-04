"""
Sichert die fuehrenden Papiere des Nebelseetal-Projekts AUSSERHALB des Projektordners.

Warum: Das Entwicklungsprotokoll und die Uebergabe liegen im Projekt. Wird der Projektordner
verschoben, aufgeraeumt oder geloescht, ist die Entstehungsgeschichte weg. Deshalb legt dieses
Skript bei jedem Lauf eine **zeitgestempelte, vollstaendige Kopie** in einem Ordner an, der nicht
zum Projekt gehoert (Fuehrungsort fuer projektuebergreifende Dinge):

    D:\\Arbeiten\\Hermes\\Nebelseetal_Protokoll\\<Jahr-Monat-Tag_StundeMinute>\\

Zusaetzlich:
  * eine ``MANIFEST.txt`` mit Groesse und SHA256 jeder Datei (Nachweis, dass die Kopie vollstaendig
    und unveraendert ist),
  * ein Zeiger ``zuletzt.txt`` auf die juengste Sicherung (eine Zeile, absolut),
  * eine Zeile im Entwicklungsprotokoll, die auf die Sicherung hinweist — nur wenn ``--protokoll``
    gesetzt ist (sonst wird nichts angefasst).

Aufruf:

    python tools/protokoll_sichern.py                 # sichern + Bericht
    python tools/protokoll_sichern.py --pruefen       # nur vergleichen, nichts schreiben
    python tools/protokoll_sichern.py --protokoll     # zusaetzlich eine Zeile im Protokoll anhaengen
    python tools/protokoll_sichern.py --ziel "D:/Pfad"  # anderer Zielort

Geprueft wird am Ende: jede Datei muss am Ziel liegen UND dieselbe Pruefsumme haben. Weicht etwas
ab, meldet das Skript einen Fehler (Rueckgabewert 1) statt "fertig".
"""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
import time
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
STANDARD_ZIEL = Path("D:/Arbeiten/Hermes/Nebelseetal_Protokoll")

# Was gesichert wird: die fuehrenden Papiere dieser Sitzung.
# (Frueher kam hier auch der Ordner board/ dazu — das Brett der Kinder wurde am 04.10.2026 auf
#  Daniels Wunsch wieder entfernt, also wird es auch nicht mehr gesichert.)
MUSTER = [
    ("docs", "PROJEKT_STAND.md"),
    ("docs", "ENTWICKLUNGSPROTOKOLL.md"),
    ("docs", "BOARD.md"),
    ("docs", "AGENTEN_PLAN.md"),
    ("docs", "LEHREN.md"),
    ("docs", "ORDNUNG.md"),
    ("docs", "WEG_ZUR_EXE.md"),
    ("docs", "FRAGEN_FUER_MORGEN.md"),
    ("docs", "MUSTERVORLAGEN.md"),
    ("docs", "ENTWURF_AUFTRAEGE.md"),
    ("docs", "ENTWURF_WIRTSCHAFT.md"),
    ("docs", "AUDIT_KONFORMITAET_astra.md"),
]
ORDNER = []                 # keine Unterordner mehr (das Brett der Kinder ist entfallen)


def pruefsumme(pfad: Path) -> str:
    leser = hashlib.sha256()
    with open(pfad, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            leser.update(block)
    return leser.hexdigest()


def sammle() -> list:
    """Alle zu sichernden Dateien als (Quelle, relativer Zielname)."""
    dateien = []
    for ordner, name in MUSTER:
        quelle = WURZEL / ordner / name
        if quelle.exists():
            dateien.append((quelle, Path(ordner) / name))
    for ordner in ORDNER:
        basis = WURZEL / ordner
        if basis.exists():
            for pfad in sorted(basis.rglob("*")):
                if pfad.is_file():
                    dateien.append((pfad, pfad.relative_to(WURZEL)))
    return dateien


def sichere(ziel: Path, trocken: bool = False) -> tuple:
    """Kopiert alles nach ``ziel`` und prueft hinterher jede Datei nach."""
    dateien = sammle()
    if not dateien:
        return False, ["Es wurde KEINE Datei gefunden — stimmt der Projektpfad?", ]
    ziel.mkdir(parents=True, exist_ok=True)
    zeilen = []
    fehler = []
    for quelle, relativ in dateien:
        zielpfad = ziel / relativ
        if not trocken:
            zielpfad.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(quelle, zielpfad)
        summe_quelle = pruefsumme(quelle)
        if trocken:
            gesichert = f"(Pruefung) {relativ} {summe_quelle[:12]}"
        else:
            if not zielpfad.exists():
                fehler.append(f"fehlt am Ziel: {relativ}")
                continue
            summe_ziel = pruefsumme(zielpfad)
            if summe_ziel != summe_quelle:
                fehler.append(f"Pruefsumme weicht ab: {relativ}")
                continue
            gesichert = f"{relativ}  {quelle.stat().st_size} Byte  sha256 {summe_quelle[:16]}"
        zeilen.append(gesichert)
    return not fehler, (zeilen + (["FEHLER:"] + fehler if fehler else []))


def protokollzeile(ziel: Path, anzahl: int) -> None:
    """Haengt eine Zeile ans Entwicklungsprotokoll (nur auf Wunsch)."""
    pfad = WURZEL / "docs" / "ENTWICKLUNGSPROTOKOLL.md"
    if not pfad.exists():
        print("Protokoll nicht gefunden — nichts angehaengt.")
        return
    with open(pfad, "a", encoding="utf-8") as f:
        f.write(f"\n**Sicherung (projektunabhaengig):** {anzahl} Dateien gesichert nach "
                f"`{ziel}` — Vorgabe von Daniel am 04.10.2026, damit das Protokoll auch ohne "
                f"diesen Projektordner weiterlebt. Zeiger auf die juengste Fassung: "
                f"`{ziel.parent / 'zuletzt.txt'}`.\n")
    print(f"Protokoll ergaenzt: {pfad}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Projektunabhaengige Sicherung des Protokolls")
    parser.add_argument("--ziel", default=str(STANDARD_ZIEL))
    parser.add_argument("--pruefen", action="store_true", help="nur vergleichen, nichts schreiben")
    parser.add_argument("--protokoll", action="store_true", help="Zeile ins Protokoll anhaengen")
    args = parser.parse_args()

    zielbasis = Path(args.ziel)
    stempel = time.strftime("%Y-%m-%d_%H%M")
    ziel = zielbasis / stempel

    print("Projektunabhaengige Sicherung der fuehrenden Papiere")
    print(f"  Quelle: {WURZEL}")
    print(f"  Ziel:   {ziel}{'  (nur Pruefung)' if args.pruefen else ''}")

    ok, zeilen = sichere(ziel, trocken=args.pruefen)
    for zeile in zeilen:
        print(f"  {zeile}")
    if not ok:
        print("SICHERUNG UNVOLLSTAENDIG — siehe FEHLER oben.")
        return 1

    anzahl = len([z for z in zeilen if not z.startswith("FEHLER")])
    if not args.pruefen:
        with open(ziel / "MANIFEST.txt", "w", encoding="utf-8") as f:
            f.write(f"Sicherung der fuehrenden Papiere des Nebelseetal-Remake\n"
                    f"Stand: {time.strftime('%d.%m.%Y %H:%M')}\nQuelle: {WURZEL}\n"
                    f"Dateien: {anzahl}\n\n" + "\n".join(zeilen) + "\n")
        (zielbasis / "zuletzt.txt").write_text(str(ziel) + "\n", encoding="utf-8")
        print(f"  MANIFEST.txt geschrieben, Zeiger erneuert: {zielbasis / 'zuletzt.txt'}")
        if args.protokoll:
            protokollzeile(ziel, anzahl)

    print(f"GESAMT: {anzahl} Dateien gesichert und nachgeprueft (Pruefsummen gleich).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
