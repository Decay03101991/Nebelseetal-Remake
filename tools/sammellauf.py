"""Sammellauf: ALLE Pruefdateien nacheinander, mit ehrlichem Ergebnis.

Warum dieses Werkzeug: der Sammellauf wurde bisher von Hand gefahren, es gab kein Skript
im Projekt. Ergebnis war eine Zahl in einer Uebergabe ("60 von 60 gruen, 568 s"), die
niemand reproduzieren konnte. Hier steht der Lauf als Werkzeug, mit Protokoll und
Rueckgabewert.

Grundsaetze (aus den Regeln dieser Sitzung):
  * Das Spiel muss GESCHLOSSEN sein - sonst ist die erste Datei unzuverlaessig.
  * Eine Datei gilt nur als gruen, wenn ihr Prozess-RC 0 ist UND die letzte
    ERGEBNIS-Zeile 0 Fehler nennt (nicht blind auf "exit 0" vertrauen).
  * Befunde (Befund != Fehler) werden gezaehlt, aber nicht als Fehler gewertet.
  * Kein Zeitlimit fuer den ganzen Lauf; je Datei 420 s, damit ein Haenger auffaellt.
    (300 s waren zu knapp: `test_durchspiel.py` braucht normal 214 s und lief am 31.10.2026
    unter Last in das Limit - das ist kein Fehler im Spiel, sondern ein zu enger Deckel.)

Aufruf:
  python -X utf8 tools/sammellauf.py                 # alle Dateien
  python -X utf8 tools/sammellauf.py test_kampf test_welt   # Auswahl (Teilstring)
Ergebnis: docs/audits/sammellauf_<JJJJMMTT_HHMM>.log  + Zusammenfassung auf stdout
"""
from __future__ import annotations

import datetime
import os
import re
import subprocess
import sys
import time

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS = os.path.join(HIER, "tests")
ERGEBNIS = re.compile(r"ERGEBNIS:\s*(\d+)\s*bestanden,\s*(\d+)\s*Fehler,\s*(\d+)\s*Befunde", re.I)
UNITTEST = re.compile(r"Ran\s+(\d+)\s+tests?", re.I)
UNITTEST_FAIL = re.compile(r"^FAILED\s*\(", re.M)
JE_DATEI_SEKUNDEN = 420


def dateien(auswahl):
    namen = sorted(n for n in os.listdir(TESTS)
                   if n.startswith("test_") and n.endswith(".py"))
    if auswahl:
        namen = [n for n in namen if any(a in n for a in auswahl)]
    return namen


def deute(ausgabe: str, rc: int):
    """(gruen, bestanden, fehler, befunde, kurztext)"""
    treffer = list(ERGEBNIS.finditer(ausgabe))
    if treffer:
        bestanden, fehler, befunde = (int(x) for x in treffer[-1].groups())
        return (rc == 0 and fehler == 0), bestanden, fehler, befunde, \
               f"{bestanden}/{fehler}/{befunde}"
    u = list(UNITTEST.finditer(ausgabe))
    if u:
        fehler = 1 if UNITTEST_FAIL.search(ausgabe) or rc != 0 else 0
        return fehler == 0, int(u[-1].group(1)), fehler, 0, f"{u[-1].group(1)} Tests"
    # keine Auswertung: dann zaehlt nur der Rueckgabewert, und das wird benannt
    return rc == 0, 0, 0 if rc == 0 else 1, 0, f"ohne ERGEBNIS-Zeile, RC {rc}"


def main():
    auswahl = [a for a in sys.argv[1:] if not a.startswith("-")]
    namen = dateien(auswahl)
    if not namen:
        print("Keine Pruefdatei gefunden.")
        return 2
    ordner = os.path.join(HIER, "docs", "audits")
    os.makedirs(ordner, exist_ok=True)
    logpfad = os.path.join(ordner, "sammellauf_%s.log" % time.strftime("%Y%m%d_%H%M"))
    start = time.time()
    zeilen, gut, tot_bestanden, tot_fehler, tot_befunde, other, ausgesetzt = [], [], 0, 0, 0, [], []
    with open(logpfad, "w", encoding="utf-8", newline="\n") as log:
        kopf = (f"Sammellauf {datetime.datetime.now():%d.%m.%Y %H:%M} - {len(namen)} Dateien, "
                f"je {JE_DATEI_SEKUNDEN} s\n" + "=" * 78 + "\n")
        log.write(kopf)
        print(kopf, end="")
        for i, name in enumerate(namen, 1):
            t0 = time.time()
            pfad = os.path.join(TESTS, name)
            # Zurueckgezogene Pruefdatei: ihr Kopf sagt ausdruecklich, dass sie NICHT mehr im
            # Sammellauf laeuft (Zeitzeugnis, Nachfolger uebernimmt den Dienst). Sie wird nicht
            # geloescht, aber auch nicht als rot gezaehlt - sie wird als AUSGESETZT benannt.
            with open(pfad, encoding="utf-8", errors="replace") as fh:
                kopftext = fh.read(3000).upper()
            # NUR dieser Satz ist der Marker. Ein frueheres "ZURUECKGEZOGEN" war zu grob und hat
            # `test_welt_optik.py` faelschlich ausgesetzt ("zurueckgezogene tk-Leinwand").
            if "NICHT MEHR IM SAMMELLAUF" in kopftext:
                dauer = time.time() - t0
                zeile = f"AUSGESETZT {name:48s} {'dokumentiert zurueckgezogen':24s} {dauer:6.1f} s\n"
                print(zeile, end="")
                log.write(zeile)
                ausgesetzt.append(name)
                continue
            try:
                p = subprocess.run([sys.executable, "-X", "utf8", os.path.join(TESTS, name)],
                                   capture_output=True, text=True, encoding="utf-8",
                                   errors="replace", timeout=JE_DATEI_SEKUNDEN, cwd=HIER)
                ausgabe, rc = (p.stdout or "") + (p.stderr or ""), p.returncode
            except subprocess.TimeoutExpired:
                ausgabe, rc = "", 124
            gruen = False
            if rc == 124:
                kurz = f"ZEITLIMIT {JE_DATEI_SEKUNDEN} s"
            else:
                gruen, bestanden, fehler, befunde, kurz = deute(ausgabe, rc)
                tot_bestanden += bestanden
                tot_fehler += fehler
                tot_befunde += befunde
                if gruen:
                    gut.append(name)
                else:
                    other.append(name)
            dauer = time.time() - t0
            zeile = f"{'OK ' if gruen else 'ROT'} {name:52s} {kurz:24s} {dauer:6.1f} s\n"
            print(zeile, end="")
            log.write(zeile)
            if not gruen:
                schwanz = "\n".join(ausgabe.strip().splitlines()[-25:])
                log.write("     --- Ausgabe der roten Datei ---\n"
                          + "\n".join("     " + z for z in schwanz.splitlines()) + "\n")
            zeilen.append((name, gruen, kurz, dauer))
        gesamt = time.time() - start
        fuss = ("=" * 78 + f"\nSAMMELLAUF: {len(gut)} von {len(namen)} gruen, {len(other)} rot, "
                f"{gesamt:.0f} s\n{len(namen)} Dateien, zusammen {tot_bestanden} bestandene Pruefungen, "
                f"{tot_fehler} Fehler, {tot_befunde} Befunde\n")
        if other:
            fuss += "ROT: " + ", ".join(other) + "\n"
        log.write(fuss)
    print(fuss)
    print(f"Protokoll: {logpfad}")
    return 0 if not other else 1


if __name__ == "__main__":
    sys.exit(main())
