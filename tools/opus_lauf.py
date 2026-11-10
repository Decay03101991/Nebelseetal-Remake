"""Faehrt EINEN Pruefaufruf an ein starkes Modell (Claude, Klasse Opus) ueber das gebaute Paket.

Kein Sammellauf, kein Agent: **genau ein Aufruf**, Eingabe = `docs/audits/OPUS_PRUEFPAKET_20261110.md`,
Ausgabe = einer neuer Beleg unter `docs/audits/`. Die Antwort kommt ueber die Standardausgabe, die Datei
schreibt DIESES Werkzeug.

**Das Modell arbeitet gegen das VEROEFFENTLICHTE Repo, nicht gegen den Arbeitsordner** (Daniel, 10.11.2026):
der Aufruf laeuft in einem leeren Arbeitsordner AUSSERHALB des Projekts, `Read`/`Grep`/`Glob`/`Bash` sind
verboten, nur `WebFetch` ist erlaubt - und das Paket nennt je Datei die Abruf-URL am gepinnten Commit.

Kostenbremse: ohne `--scharf` passiert nichts (nur Messung und Kommandozeile). Vor dem scharfen Lauf
muss Daniel zustimmen; der Lauf laeuft im Hintergrund und wird an der usage-Datei gemessen, nicht an
der Antwortdatei.

Aufruf: python -X utf8 tools/opus_lauf.py [--trocken] [--scharf] [--modell opus] [--zeitlimit 3600]
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAKET = os.path.join(HIER, "docs", "audits", "OPUS_PRUEFPAKET_20261110.md")
ZIELORDNER = os.path.join(HIER, "docs", "audits")
MINDESTZEICHEN, HOECHSTZEICHEN = 15000, 60000


def _neue_pfade() -> tuple[str, str]:
    stempel = time.strftime("%Y%m%d_%H%M")
    return (os.path.join(ZIELORDNER, f"OPUS_PRUEFUNG_{stempel}.md"),
            os.path.join(ZIELORDNER, f"opus_usage_{stempel}.json"))


def _messen(paket: str) -> int:
    zeichen = os.path.getsize(paket)
    with open(paket, encoding="utf-8") as griff:
        text = griff.read()
    print(f"Paket:       {paket}")
    print(f"Zeichen:     {len(text)} (Grenze {MINDESTZEICHEN} bis {HOECHSTZEICHEN})")
    print(f"Prompt-Token: rund {len(text) // 3.6:.0f} (Schaetzung 3,6 Zeichen je Token)")
    print(f"Zeilen:      {text.count(chr(10)) + 1}")
    return len(text)


def _im_projekt(pfad: str) -> bool:
    """Liegt `pfad` im Projektordner? Zwei verschiedene Laufwerke liegen nie ineinander.

    `os.path.commonpath` wirft `ValueError: Paths don't have the same drive`, sobald die Pfade auf
    verschiedenen Laufwerken liegen - und genau das ist hier der erwuenschte Normalfall (Temp auf C:,
    Projekt auf D:). Belegt am 10.11.2026: der scharfe Lauf starb an dieser Zeile per Traceback, BEVOR
    irgendein Modell aufgerufen wurde. Deshalb hier eine reine Zeichenketten-Pruefung mit Trenner,
    damit `D:\\Arbeiten\\Nebelseetal_Remake_alt` nicht als "im Projekt" gilt.
    """
    hier = os.path.normcase(os.path.abspath(HIER))
    kandidat = os.path.normcase(os.path.abspath(pfad))
    return kandidat == hier or kandidat.startswith(hier + os.sep)


def _claude_exe() -> "str | None":
    """Findet die wirklich STARTBARE Claude-Code-Datei.

    Zwei belegte Fehlschlaege am 10.11.2026: `shutil.which("claude")` liefert unter Windows die
    POSIX-Huelle OHNE Endung (npm legt `claude`, `claude.cmd` und `claude.ps1` nebeneinander ab), und
    `subprocess.run(["claude", ...])` scheitert dann mit `FileNotFoundError [WinError 2]`, weil
    CreateProcess keine endungslose Datei startet. Die `.cmd`-Huelle wiederum ruft nur
    `node_modules\\@anthropic-ai\\claude-code\\bin\\claude.exe` auf - genau diese Datei wird hier gesucht,
    weil sie ohne Zwischenschale laeuft und stdin sauber durchreicht.
    """
    kandidaten: list[str] = []
    for name in ("claude.exe", "claude.cmd", "claude.bat"):
        treffer = shutil.which(name)
        if treffer:
            kandidaten.append(treffer)
    huelle = shutil.which("claude")
    if huelle:
        ordner = os.path.dirname(huelle)
        kandidaten.append(os.path.join(ordner, "node_modules", "@anthropic-ai",
                                       "claude-code", "bin", "claude.exe"))
        kandidaten.append(os.path.join(ordner, "claude.exe"))
    for pfad in kandidaten:                    # erst die echte EXE
        if pfad.lower().endswith(".exe") and os.path.isfile(pfad):
            return pfad
    for pfad in kandidaten:                    # dann die Huelle (laeuft ueber cmd.exe /c)
        if os.path.isfile(pfad):
            return pfad
    return None


def _claude_befehl(argumente: "list[str]") -> "list[str] | None":
    """Baut die startbare Kommandozeile. `.cmd`/`.bat` brauchen `cmd.exe /c`, eine EXE nicht."""
    exe = _claude_exe()
    if exe is None:
        return None
    if exe.lower().endswith((".cmd", ".bat")):
        return ["cmd.exe", "/c", exe, *argumente]
    return [exe, *argumente]


def main() -> int:
    zerleger = argparse.ArgumentParser(description="Einen Pruefaufruf an ein starkes Modell fahren")
    zerleger.add_argument("--scharf", action="store_true", help="wirklich aufrufen (kostet!)")
    zerleger.add_argument("--trocken", action="store_true", help="nur messen und zeigen (Vorgabe)")
    zerleger.add_argument("--modell", default="opus", help="Modell-Alias des Anbieters (Vorgabe: opus)")
    zerleger.add_argument("--zeitlimit", type=int, default=3600)
    args = zerleger.parse_args()

    if not os.path.isfile(PAKET):
        print(f"FEHLER: Paket fehlt - erst bauen: python -X utf8 tools/opus_paket_bauen.py")
        return 2
    zeichen = _messen(PAKET)
    if not (MINDESTZEICHEN <= zeichen <= HOECHSTZEICHEN):
        print(f"FEHLER: Paketgroesse ausserhalb der Grenzen - erst das Paket pruefen.")
        return 2

    zusatz = ("Du pruefst gegen das oeffentliche Repository unter der im Paket genannten, gepinnten "
              "Commit-Adresse. Lies keine lokalen Dateien, fuehre keine Befehle aus, schreibe nichts. "
              "Wenn du etwas nachsehen willst, lade die im Paket genannte raw.githubusercontent-URL.")
    ziel, usage = _neue_pfade()
    print(f"Ziel:        {ziel}")
    print(f"Messdatei:   {usage}")
    print(f"Modell:      {args.modell}")
    print(f"Aufruf:      {_claude_exe() or '(nicht gefunden)'}")
    print(f"Kommando:    claude -p --output-format json --model {args.modell} "
          f"--allowedTools WebFetch --disallowedTools Read,Grep,Glob,Bash,Write,Edit,MultiEdit "
          f"< {os.path.basename(PAKET)}")
    print("Arbeitsordner: leerer Ordner unter dem Temp-Pfad, AUSSERHALB des Projekts")
    print("\nHinweis: das Modell liest NUR das Repo (raw.githubusercontent am gepinnten Commit) und schreibt"
          " nichts; die Antwortdatei schreibt dieses Werkzeug.")

    if not args.scharf:
        print("\nTrockenlauf: nichts aufgerufen, nichts geschrieben.")
        print("Scharf erst nach Daniels Zustimmung: --scharf")
        return 0

    argumente = ["-p", "--output-format", "json", "--model", args.modell,
                 "--allowedTools", "WebFetch",
                 "--disallowedTools", "Read,Grep,Glob,Bash,Write,Edit,MultiEdit",
                 "--append-system-prompt", zusatz]
    befehl = _claude_befehl(argumente)
    if befehl is None:
        print("FEHLER: Claude Code (claude.exe) nicht gefunden - Weg A nicht verfuegbar.")
        return 5

    if os.path.exists(ziel):
        print("FEHLER: Zieldatei existiert schon - Abbruch, nichts ueberschrieben.")
        return 3

    # Arbeitsordner AUSSERHALB des Projekts: das Modell soll nicht auf der Platte lesen.
    arbeitsordner = os.path.join(tempfile.gettempdir(), "opus_pruefung_" + time.strftime("%Y%m%d_%H%M"))
    os.makedirs(arbeitsordner, exist_ok=True)
    if _im_projekt(arbeitsordner):
        print("FEHLER: Arbeitsordner liegt im Projekt - Abbruch.")
        return 4
    print(f"Arbeitsordner: {arbeitsordner} (ausserhalb des Projekts)")

    beginn = time.time()
    try:
        with open(PAKET, "rb") as eingabe:
            lauf = subprocess.run(befehl, cwd=arbeitsordner, stdin=eingabe, capture_output=True,
                                  timeout=args.zeitlimit)
    except FileNotFoundError as fehler:
        print(f"FEHLER: Aufruf nicht startbar ({befehl[0]}): {fehler}")
        print("Nichts geschrieben, nichts bezahlt.")
        return 5
    dauer = round(time.time() - beginn, 1)
    roh = lauf.stdout.decode("utf-8", "replace")
    fehlertext = lauf.stderr.decode("utf-8", "replace")
    nutzung, antwort = {}, roh
    for zeile in reversed(roh.splitlines()):
        zeile = zeile.strip()
        if zeile.startswith("{"):
            try:
                daten = json.loads(zeile)
            except json.JSONDecodeError:
                continue
            antwort = daten.get("result") or daten.get("text") or roh
            nutzung = {k: daten.get(k) for k in ("model", "usage", "total_cost_usd",
                                                 "num_turns", "duration_ms", "session_id")}
            break

    with open(ziel, "w", encoding="utf-8", newline="\n") as griff:
        griff.write(f"# Pruefung des starken Modells - {_dt.datetime.now():%d.%m.%Y %H:%M}\n\n")
        griff.write(f"Paket: `{os.path.basename(PAKET)}` ({zeichen} Zeichen) - Modell: `{args.modell}`\n\n")
        griff.write(antwort if antwort.strip() else "(LEER)\n")
    with open(usage, "w", encoding="utf-8", newline="\n") as griff:
        json.dump({"dauer_s": dauer, "rueckgabe": lauf.returncode, "nutzung": nutzung,
                   "arbeitsordner": arbeitsordner, "aufruf": befehl[0],
                   "paket_sha256": hashlib.sha256(open(PAKET, "rb").read()).hexdigest(),
                   "stderr": fehlertext[-2000:], "paket": PAKET, "ziel": ziel},
                  griff, ensure_ascii=False, indent=2)
    print(f"EXIT={lauf.returncode} dauer={dauer}s Antwortzeichen={len(antwort)}")
    print(f"geschrieben: {ziel}")
    print(f"gemessen:    {usage}")
    if fehlertext.strip():
        print("stderr (Auszug):", fehlertext.strip()[-400:])
    return 0 if lauf.returncode == 0 and antwort.strip() else 1


if __name__ == "__main__":
    sys.exit(main())
