"""Sammellauf: ALLE Pruefdateien, wahlweise nacheinander oder parallel, mit ehrlichem Ergebnis.

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

Parallelbetrieb (Schritt 12, 08.11.2026):
  * `-j N` / `--parallel N` faehrt N Dateien gleichzeitig (Vorgabe 1 = nacheinander, wie
    bisher). Auf diesem Rechner stehen 2 Kerne; mehr als 2 gleichzeitige Laeufe bringen
    hier erfahrungsgemaess nur Wartezeit, nicht Durchsatz.
  * JEDE Datei bekommt ihren eigenen Spielordner ueber `NEBEL_SPIELDATEN_ORDNER` - auch im
    seriellen Betrieb. Grund (gemessen): mehrere Pruefdateien schreiben ihren Spielstand
    sonst nach `src/savegame.json`; gleichzeitig gestartet raeumen sie einander die Datei weg.
    Mit eigenem Ordner ist der Pfad je Prozess getrennt.
  * Startreihenfolge: die laengsten Dateien zuerst (Dauern aus
    `docs/audits/messwerte/index.json`). Damit laufen die beiden Brocken (210 s und 150 s)
    von der ersten Sekunde an mit.
  * Das Protokoll listet die Dateien am Ende SORTIERT nach Namen - die Reihenfolge der
    Ausfuehrung schwankt, das Ergebnis nicht.
  * Die gemessenen Einzeldauern stehen im Parallelbetrieb unter Last und sind NICHT mit
    Einzellaeufen vergleichbar; die Gesamtzeit ist die Vergleichszahl.

Aufruf:
  python -X utf8 tools/sammellauf.py                 # alle Dateien, nacheinander
  python -X utf8 tools/sammellauf.py -j 2            # alle Dateien, zwei gleichzeitig
  python -X utf8 tools/sammellauf.py test_kampf test_welt   # Auswahl (Teilstring)
Ergebnis: docs/audits/sammellauf_<JJJJMMTT_HHMM>.log  + Zusammenfassung auf stdout
"""
from __future__ import annotations

import concurrent.futures
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS = os.path.join(HIER, "tests")
# Das Befunde-Feld ist FREIWILLIG: zwei Pruefdateien (test_projektpfade, test_textqualitaet)
# schreiben "N bestanden, M Fehler (X Dokumente)" ohne Befunde. Ohne diese Toleranz wertete der
# Sammellauf sie als "ohne ERGEBNIS-Zeile" und zaehlte 573 bestandene Pruefungen gar nicht mit -
# gruen war dann nur der Rueckgabewert, nicht die Zusage. (Schritt 12, 08.11.2026)
ERGEBNIS = re.compile(r"ERGEBNIS:\s*(\d+)\s*bestanden,\s*(\d+)\s*Fehler(?:,\s*(\d+)\s*Befunde)?", re.I)
UNITTEST = re.compile(r"Ran\s+(\d+)\s*tests?", re.I)
UNITTEST_FAIL = re.compile(r"^FAILED\s*\(", re.M)
JE_DATEI_SEKUNDEN = 420
MARKER = "NICHT MEHR IM SAMMELLAUF"
SPIELDATEN_VARIABLE = "NEBEL_SPIELDATEN_ORDNER"
INDEX = os.path.join(HIER, "docs", "audits", "messwerte", "index.json")
# M12.0 (Claude Nr. 16, Teil B): EINE Zeile je Datei und Lauf. Grund: `test_textqualitaet` hatte
# 0 Laeufe in der Messwerte-Ablage und war trotzdem rot (Lauf 22:18) - "keine Historie" hiess also
# nur "schreibt nichts in den Index". Die Zeile entsteht darum AUS DEM PROZESSERGEBNIS, nicht aus
# dem harness, und schliesst die 46 blinden Flecken auf einen Schlag.
LAEUFE = os.path.join(HIER, "docs", "audits", "laeufe.jsonl")
KOPF_STUFE = re.compile(r"^\s*PRUEF_STUFE\s*=\s*(\d+)", re.M)
STUFE_OHNE_KOPF = 3        # Ersatzwert nach M1: ohne Kopf gilt Stufe 3


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
        bestanden, fehler, befunde = (int(x or 0) for x in treffer[-1].groups())
        return (rc == 0 and fehler == 0), bestanden, fehler, befunde, \
               f"{bestanden}/{fehler}/{befunde}"
    u = list(UNITTEST.finditer(ausgabe))
    if u:
        fehler = 1 if UNITTEST_FAIL.search(ausgabe) or rc != 0 else 0
        return fehler == 0, int(u[-1].group(1)), fehler, 0, f"{u[-1].group(1)} Tests"
    # keine Auswertung: dann zaehlt nur der Rueckgabewert, und das wird benannt
    return rc == 0, 0, 0 if rc == 0 else 1, 0, f"ohne ERGEBNIS-Zeile, RC {rc}"


def dauer_schaetzung(pfad_index=INDEX):
    """{dateiname: dauer_s} aus der Messwerte-Ablage - Grundlage der Startreihenfolge.

    Fehlt der Index oder eine Datei darin, wird sie mit 0 geschaetzt und damit zuletzt
    gestartet. Ein fehlender Index ist kein Fehler: dann laeuft der Lauf in Namensreihenfolge.
    """
    try:
        with open(pfad_index, encoding="utf-8") as datei:
            roh = json.load(datei)
    except (OSError, ValueError):
        return {}
    dateien_im_index = roh.get("dateien") if isinstance(roh, dict) else None
    if not isinstance(dateien_im_index, dict):
        return {}
    ergebnis = {}
    for name, eintrag in dateien_im_index.items():
        if not isinstance(eintrag, dict):
            continue
        try:
            ergebnis[str(name) + ".py"] = float(eintrag.get("dauer_s") or 0.0)
        except (TypeError, ValueError):
            continue
    return ergebnis


def startreihenfolge(namen, schaetzung):
    """Laengste zuerst; Gleichstand und Unbekannte alphabetisch (deterministisch)."""
    return sorted(namen, key=lambda n: (-schaetzung.get(n, 0.0), n))


def spielordner_fuer(wurzel, name):
    """Eigener Spielordner je Pruefdatei (NEBEL_SPIELDATEN_ORDNER)."""
    ordner = os.path.join(wurzel, name[:-3] if name.endswith(".py") else name)
    os.makedirs(ordner, exist_ok=True)
    return ordner


def fahre(name, spielordner):
    """Fuehrt EINE Pruefdatei und liefert ihr Ergebnis als dict."""
    pfad = os.path.join(TESTS, name)
    ergebnis = {"name": name, "gruen": False, "ausgesetzt": False, "kurz": "",
                "bestanden": 0, "fehler": 0, "befunde": 0, "ausgabe": "", "ordner": "",
                "rc": None}
    t0 = time.time()
    # Zurueckgezogene Pruefdatei: ihr Kopf sagt ausdruecklich, dass sie NICHT mehr im
    # Sammellauf laeuft (Zeitzeugnis, Nachfolger uebernimmt den Dienst). Sie wird nicht
    # geloescht, aber auch nicht als rot gezaehlt - sie wird als AUSGESETZT benannt.
    with open(pfad, encoding="utf-8", errors="replace") as fh:
        kopftext = fh.read(3000).upper()
    # NUR dieser Satz ist der Marker. Ein frueheres "ZURUECKGEZOGEN" war zu grob und hat
    # `test_welt_optik.py` faelschlich ausgesetzt ("zurueckgezogene tk-Leinwand").
    if MARKER in kopftext:
        ergebnis.update(ausgesetzt=True, kurz="dokumentiert zurueckgezogen",
                        dauer=time.time() - t0)
        return ergebnis
    umgebung = dict(os.environ)
    umgebung[SPIELDATEN_VARIABLE] = spielordner      # eigener Spielstand je Prozess
    try:
        p = subprocess.run([sys.executable, "-X", "utf8", pfad],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=JE_DATEI_SEKUNDEN, cwd=HIER,
                           env=umgebung)
        ausgabe, rc = (p.stdout or "") + (p.stderr or ""), p.returncode
    except subprocess.TimeoutExpired:
        ausgabe, rc = "", 124
    if rc == 124:
        ergebnis.update(kurz=f"ZEITLIMIT {JE_DATEI_SEKUNDEN} s", ausgabe=ausgabe, rc=rc)
    else:
        gruen, bestanden, fehler, befunde, kurz = deute(ausgabe, rc)
        ergebnis.update(gruen=gruen, bestanden=bestanden, fehler=fehler,
                        befunde=befunde, kurz=kurz, ausgabe=ausgabe, rc=rc)
    ergebnis["dauer"] = time.time() - t0
    ergebnis["ordner"] = spielordner                 # nur fuer die Diagnose gemerkt
    return ergebnis


def kopf_stufe(pfad: str) -> int:
    """Die Pruefstufe aus dem Dateikopf (M1) - ohne die Datei zu importieren.

    Fehlt der Kopf, gilt `STUFE_OHNE_KOPF` (3, Claudes Ersatzwert). Gelesen wird nur der Anfang
    der Datei als Text; ein kaputter Kopf ist kein Fehler, sondern ergibt ebenfalls 3.
    """
    try:
        with open(pfad, encoding="utf-8", errors="replace") as fh:
            anfang = fh.read(4000)
    except OSError:
        return STUFE_OHNE_KOPF
    treffer = KOPF_STUFE.search(anfang)
    if treffer is None:
        return STUFE_OHNE_KOPF
    try:
        stufe = int(treffer.group(1))
    except ValueError:
        return STUFE_OHNE_KOPF
    return stufe if 1 <= stufe <= 4 else STUFE_OHNE_KOPF


def dateien_fuer_stufe(namen, stufe: int, tests_ordner: str = TESTS) -> list:
    """F-63: die Pruefdateien bis zur Stufe N (1..4). Stufe 4 heisst ALLE.

    Die Stufe steht im Kopf der Datei (M1, `PRUEF_STUFE`); ohne Kopf gilt 3. Damit ist der
    haeufige Lauf klein (T1/T2) und der volle Lauf (T4) bleibt die Ausnahme vor jeder EXE.
    """
    stufe = max(1, min(4, int(stufe)))
    if stufe >= 4:
        return list(namen)
    return [n for n in namen if kopf_stufe(os.path.join(tests_ordner, n)) <= stufe]


def commit_kurz() -> str:
    """Der kurze Commit-Hash dieses Standes (fuer die Laufzeile); "" wenn git fehlt."""
    try:
        p = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True,
                           text=True, cwd=HIER, timeout=20)
        return (p.stdout or "").strip() if p.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def zeilen_fuer_lauf(ergebnisse: dict, zeitpunkt: str, commit: str, parallel: int) -> list:
    """Eine Zeile je Datei - reine Funktion, damit die Wache sie ohne Prozess pruefen kann.

    Felder (Claude Nr. 16, M12.0): `datei`, `zeit`, `lauf`, `commit`, `stufe`, `rc`, `bestanden`,
    `fehler`, `befunde`, `dauer`, `parallel`, `allein`, `ausgesetzt`.
    `bestanden` ist None, wenn die Datei ausgesetzt (nicht gelaufen) ist - so ist "nie
    aufgezeichnet" von "nie gelaufen" zu unterscheiden.
    """
    zeilen = []
    for name in sorted(ergebnisse):
        e = ergebnisse[name]
        ausgesetzt = bool(e.get("ausgesetzt"))
        zeilen.append({
            "datei": name,
            "zeit": zeitpunkt,
            "lauf": zeitpunkt,
            "commit": commit,
            "stufe": kopf_stufe(os.path.join(TESTS, name)),
            "rc": e.get("rc"),
            "bestanden": None if ausgesetzt else bool(e.get("gruen")),
            "fehler": int(e.get("fehler") or 0),
            "befunde": int(e.get("befunde") or 0),
            "dauer": round(float(e.get("dauer") or 0.0), 2),
            "parallel": int(parallel),
            "allein": "ja" if int(parallel) == 1 else "nein",
            "ausgesetzt": ausgesetzt,
        })
    return zeilen


def zeilen_schreiben(zeilen, pfad: str = LAEUFE) -> str:
    """Die Laufzeilen anhaengen (JSON je Zeile) und den Pfad zurueckgeben."""
    os.makedirs(os.path.dirname(pfad), exist_ok=True)
    with open(pfad, "a", encoding="utf-8", newline="\n") as fh:
        for zeile in zeilen:
            fh.write(json.dumps(zeile, ensure_ascii=False, sort_keys=True) + "\n")
    return pfad


def main():
    roh = [a for a in sys.argv[1:]]
    gleichzeitig = 1
    stufe = 4                       # F-63: ohne Angabe der volle Lauf (T4)
    auswahl = []
    i = 0
    while i < len(roh):
        a = roh[i]
        if a in ("-j", "--parallel"):
            if i + 1 >= len(roh):
                print("Fehler: %s braucht eine Zahl." % a)
                return 2
            try:
                gleichzeitig = max(1, int(roh[i + 1]))
            except ValueError:
                print("Fehler: %s erwartet eine Zahl, nicht %r." % (a, roh[i + 1]))
                return 2
            i += 2
            continue
        if a.startswith("--parallel="):
            try:
                gleichzeitig = max(1, int(a.split("=", 1)[1]))
            except ValueError:
                print("Fehler: %s erwartet eine Zahl." % a)
                return 2
            i += 1
            continue
        if a in ("-s", "--stufe"):
            if i + 1 >= len(roh):
                print("Fehler: %s braucht eine Zahl 1..4." % a)
                return 2
            try:
                stufe = max(1, min(4, int(roh[i + 1])))
            except ValueError:
                print("Fehler: %s erwartet 1..4, nicht %r." % (a, roh[i + 1]))
                return 2
            i += 2
            continue
        if a.startswith("--stufe="):
            try:
                stufe = max(1, min(4, int(a.split("=", 1)[1])))
            except ValueError:
                print("Fehler: %s erwartet 1..4." % a)
                return 2
            i += 1
            continue
        if not a.startswith("-"):
            auswahl.append(a)
        i += 1

    namen = dateien(auswahl)
    if stufe < 4:
        alle = len(namen)
        namen = dateien_fuer_stufe(namen, stufe)
        print("Stufe T%d: %d von %d Dateien (F-63; T4 laeuft vor jeder EXE)."
              % (stufe, len(namen), alle))
    if not namen:
        print("Keine Pruefdatei gefunden.")
        return 2
    kerne = os.cpu_count() or 1
    if gleichzeitig > kerne:
        print("Hinweis: %d gleichzeitig auf %d Kernen - mehr Wartezeit, kaum mehr Durchsatz."
              % (gleichzeitig, kerne))
    ordner = os.path.join(HIER, "docs", "audits")
    os.makedirs(ordner, exist_ok=True)
    beginn = datetime.datetime.now()                            # EINE Uhr fuer Dateiname und Kopf
    logpfad = os.path.join(ordner, "sammellauf_%s.log" % beginn.strftime("%Y%m%d_%H%M"))
    spielwurzel = tempfile.mkdtemp(prefix="nebel_sammellauf_spiel_")
    reihenfolge = startreihenfolge(namen, dauer_schaetzung())
    start = time.time()
    ergebnisse = {}
    sperre = threading.Lock()
    fertig = [0]

    def lauf(name):
        e = fahre(name, spielordner_fuer(spielwurzel, name))
        with sperre:                                 # Fortschritt live, Zaehler ohne Rennen
            fertig[0] += 1
            nr = fertig[0]
        print("%s [%d/%d] %-52s %-24s %6.1f s"
              % ("AUSGESETZT" if e["ausgesetzt"] else ("OK " if e["gruen"] else "ROT"),
                 nr, len(reihenfolge), name, e["kurz"], e["dauer"]), flush=True)
        return e

    print("Sammellauf %s - %d Dateien, %d gleichzeitig, %d Kerne"
          % (beginn.strftime("%d.%m.%Y %H:%M"), len(namen), gleichzeitig, kerne))
    if gleichzeitig > 1:
        print("Parallelbetrieb: Einzeldauern stehen unter Last, die Gesamtzeit ist die Vergleichszahl.")
    with concurrent.futures.ThreadPoolExecutor(max_workers=gleichzeitig) as pool:
        for e in pool.map(lauf, reihenfolge):
            ergebnisse[e["name"]] = e
    gesamt = time.time() - start

    gut, other, ausgesetzt = [], [], []
    tot_bestanden = tot_fehler = tot_befunde = 0
    summe_einzeln = 0.0
    zeilen = []
    for name in sorted(ergebnisse):
        e = ergebnisse[name]
        summe_einzeln += e["dauer"]
        if e["ausgesetzt"]:
            ausgesetzt.append(name)
            zeile = "AUSGESETZT %-48s %-24s %6.1f s\n" % (name, e["kurz"], e["dauer"])
        else:
            tot_bestanden += e["bestanden"]
            tot_fehler += e["fehler"]
            tot_befunde += e["befunde"]
            (gut if e["gruen"] else other).append(name)
            zeile = "%s %-52s %-24s %6.1f s\n" % (
                "OK " if e["gruen"] else "ROT", name, e["kurz"], e["dauer"])
        zeilen.append(zeile)

    kopf = ("Sammellauf %s - %d Dateien, %d gleichzeitig, je %d s, %d Kerne\n"
            "Spielordner je Datei: %s\n"
            % (beginn.strftime("%d.%m.%Y %H:%M"), len(namen),
               gleichzeitig, JE_DATEI_SEKUNDEN, kerne, spielwurzel) + "=" * 78 + "\n")
    fuss = ("=" * 78 + "\n"
            "SAMMELLAUF: %d von %d gruen, %d rot, %d ausgesetzt, %.0f s bei %d gleichzeitig\n"
            "%d Dateien gefunden, zusammen %d bestandene Pruefungen, %d Fehler, %d Befunde\n"
            "Summe der Einzeldauern %.0f s, Gesamtzeit %.0f s, Beschleunigung x%.2f\n"
            % (len(gut), len(gut) + len(other), len(other), len(ausgesetzt), gesamt,
               gleichzeitig, len(namen), tot_bestanden, tot_fehler, tot_befunde,
               summe_einzeln, gesamt, (summe_einzeln / gesamt) if gesamt else 1.0))
    if other:
        fuss += "ROT: " + ", ".join(other) + "\n"
    with open(logpfad, "w", encoding="utf-8", newline="\n") as log:
        log.write(kopf)
        for zeile in zeilen:
            log.write(zeile)
        for name in sorted(other):                   # Ausgabe der roten Dateien in den Log
            schwanz = "\n".join(ergebnisse[name]["ausgabe"].strip().splitlines()[-25:])
            log.write("\n     --- Ausgabe der roten Datei %s ---\n" % name
                      + "\n".join("     " + z for z in schwanz.splitlines()) + "\n")
        log.write(fuss)
    print()
    print(fuss, end="")
    print("Protokoll: %s" % logpfad)
    # M12.0: EINE Zeile je Datei und Lauf, aus dem Prozessergebnis - unabhaengig davon, ob die
    # Pruefdatei den harness benutzt. Damit hat JEDE gefundene Datei eine Historie.
    try:
        _zeilen = zeilen_fuer_lauf(ergebnisse, beginn.strftime("%Y-%m-%dT%H:%M:%S"),
                                   commit_kurz(), gleichzeitig)
        _pfad = zeilen_schreiben(_zeilen)
        print("Laufzeilen: %d Zeilen in %s" % (len(_zeilen), _pfad))
    except OSError as fehler:                        # Schreibfehler darf den Lauf nicht kippen
        print("Hinweis: Laufzeilen nicht geschrieben (%s)." % fehler)

    behalten = []
    for name in sorted(other) + sorted(n for n in ausgesetzt):
        pfad = ergebnisse[name].get("ordner")
        if pfad and os.path.isdir(pfad):
            behalten.append(pfad)
    for name in sorted(ergebnisse):                  # alles Gruene: Spielordner weg
        if name in other or name in ausgesetzt:
            continue
        shutil.rmtree(ergebnisse[name].get("ordner") or "", ignore_errors=True)
    if behalten:
        print("Spielordner der roten/ausgesetzten Dateien behalten:")
        for pfad in behalten:
            print("  %s" % pfad)
    else:
        shutil.rmtree(spielwurzel, ignore_errors=True)
    return 0 if not other else 1


if __name__ == "__main__":
    sys.exit(main())
