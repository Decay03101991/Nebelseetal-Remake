"""Fragt Claude Opus 5.5 (Abo Claude Pro) und legt die Antwort im Repo ab.

WARUM
-----
Bis 08.11.2026 lief jeder Opus-Auftrag ueber eine Datei auf dem Desktop und die Antwort
kam als Datei zurueck. Daniels Ansage 08.11.2026 (Chat, 18:5x): der Koordinator (Weltenfresser) soll selbststaendig
Auftraege an Claude geben duerfen, ohne Desktop-Dateien; die Antwort kommt direkt an ihn.
Dieses Werkzeug ist der Weg dazu - EINE Stelle, damit jeder Auftrag dieselben Grenzen hat.

GRENZEN (nicht verhandelbar)
----------------------------
* **Nur lesen:** `--allowedTools` ist fest `Read,Grep,Bash`; `Edit`, `Write` und alles Schreibende
  fehlen absichtlich. Was gebaut wird, baut der Koordinator.
* **Keine Zugangsdaten:** es wird nur der lokale `claude`-Befehl benutzt (Pro-Abo, kein
  `ANTHROPIC_API_KEY` noetig). Bei Abo entsteht KEINE Abbuchung; `total_cost_usd` in der Antwort ist
  ein Listenpreis-Aequivalent und wird als solcher ausgewiesen.
* **Nicht gleichzeitig mit Arbeit am Projekt:** waehrend eines Sammellaufs oder waehrend Daniels
  Spieltest wird Opus NICHT gefragt (der Rechner hat 2 Kerne; Daniel spielt dann).
* **Eine Frage, ein Lauf.** Kein Nachfassen in derselben Sitzung - sonst waechst der Kontext unklar.

WAS ES TUT
----------
1. startet `claude -p <auftrag> --model opus --effort medium --allowedTools ... --output-format json`
2. schreibt die Antwort als Markdown nach `docs/extern/antworten/<kennung>.md` (mit Kopf: Auftrag,
   Zeit, Dauer, Zuege, Listenpreis-Aequivalent, Modell)
3. druckt den Pfad und den Anfang der Antwort auf die Konsole

AUFRUF
------
    python -X utf8 tools/frage_opus.py --titel e1_handelspreis "Der Auftrag als Text"
    python -X utf8 tools/frage_opus.py --titel pruefung --aus-datei auftrag.txt
"""
from __future__ import annotations

import argparse                        # Kommandozeile
import json                            # Rueckgabe von claude -p --output-format json
import os                              # Pfade
import re                              # Kennung aus dem Titel bauen
import subprocess                      # claude starten
import sys                             # Rueckgabewert
import time                            # Dauer messen

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))      # Projektwurzel
ABLAGE = os.path.join(WURZEL, "docs", "extern", "antworten")               # Antworten
STANDARD_TURNS = 26                                                        # Zuege je Auftrag
ERLAUBTE_WERKZEUGE = "Read,Grep,Bash"                                      # NUR LESEN


def claude_befehl() -> str:
    """Der lokale Claude-Befehl neben dem Hermes-Node (Pro-Abo, keine API).

    Reihenfolge mit Grund: die `.exe` im node_modules ist das echte Programm - sie laeuft aus
    `subprocess` heraus. `claude` (ohne Endung) ist ein POSIX-Shell-Skript und `.cmd` braucht
    `cmd.exe`; beide scheitern mit `WinError 193` (gemessen 08.11.2026).
    """
    node = os.path.join(os.environ.get("LOCALAPPDATA", ""), "hermes", "node")
    kandidaten = [os.path.join(node, "node_modules", "@anthropic-ai", "claude-code", "bin", "claude.exe"),
                  os.path.join(node, "claude.exe")]
    for pfad in kandidaten:
        if pfad and os.path.exists(pfad):
            return pfad
    return "claude"                                                    # Rueckfall: aus dem PATH


def kennung(titel: str) -> str:
    """Dateiname aus dem Titel: Kleinbuchstaben, Ziffern, Unterstrich, Datum davor."""
    sauber = re.sub(r"[^a-z0-9]+", "_", titel.lower()).strip("_") or "auftrag"
    return time.strftime("%Y%m%d_%H%M_") + sauber[:60]


def frage(auftrag: str, titel: str, turns: int, modell: str, aufwand: str) -> dict:
    """Ein Lauf gegen Opus; gibt das Feld `ergebnis` samt Messwerten zurueck."""
    befehl = [claude_befehl(), "-p", auftrag, "--model", modell, "--effort", aufwand,
              "--allowedTools", ERLAUBTE_WERKZEUGE, "--max-turns", str(turns),
              "--output-format", "json"]
    start = time.time()                                                # Dauer messen
    lauf = subprocess.run(befehl, cwd=WURZEL, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=1800)
    dauer = time.time() - start
    roh = (lauf.stdout or "").strip()
    try:
        daten = json.loads(roh)                                        # JSON-Rueckgabe lesen
    except ValueError:
        daten = {"subtype": "kein_json", "result": roh or (lauf.stderr or "")[:4000],
                 "errors": []}
    return {"daten": daten, "dauer": dauer, "exit": lauf.returncode, "stderr": (lauf.stderr or "")[:2000]}


def schreibe(auftrag: str, titel: str, ergebnis: dict, modell: str, aufwand: str) -> str:
    """Legt Auftrag und Antwort als EINE Markdown-Datei ab und gibt den Pfad zurueck."""
    daten = ergebnis["daten"]
    os.makedirs(ABLAGE, exist_ok=True)
    pfad = os.path.join(ABLAGE, kennung(titel) + ".md")
    kosten = daten.get("total_cost_usd")
    zeilen = [
        "# Auftrag an Claude Opus 5.5 - %s" % titel,
        "",
        "> Erarbeitet von Claude Opus 5.5 ueber das Abo Claude Pro (kein API-Aufruf, keine Abbuchung).",
        "> Der Listenpreis-Aequivalent in der JSON-Rueckgabe ist KEINE Zahlung.",
        "> Grenzen des Laufs: `--allowedTools %s` (nur lesen), `--max-turns %d`." % (ERLAUBTE_WERKZEUGE, STANDARD_TURNS),
        "> Abgelegt vom Koordinator (`deepseek-flash`); der Koordinator prueft jede Zahl gegen den Code.",
        "",
        "## Messwerte des Laufs",
        "",
        "| Punkt | Wert |",
        "|---|---|",
        "| Modell | %s (Aufwand %s) |" % (modell, aufwand),
        "| Dauer | %.0f s |" % ergebnis["dauer"],
        "| Zuege | %s |" % daten.get("num_turns"),
        "| Abschluss | %s |" % daten.get("subtype"),
        "| Listenpreis-Aequivalent | %s USD (bei Abo keine Zahlung) |" % (kosten if kosten is not None else "entfaellt"),
        "| Rueckgabewert | %s |" % ergebnis["exit"],
        "",
        "## Auftrag (Wortlaut)",
        "",
        "```text",
        auftrag.strip(),
        "```",
        "",
        "## Antwort",
        "",
        (daten.get("result") or "").strip() or "_Keine Textantwort (subtype %s)._" % daten.get("subtype"),
        "",
    ]
    with open(pfad, "w", encoding="utf-8", newline="\n") as datei:
        datei.write("\n".join(zeilen))
    return pfad


def main() -> int:
    """Liest den Auftrag, fragt Opus einmal und meldet den Ablagepfad."""
    bauer = argparse.ArgumentParser(description="Opus einmal fragen, Antwort im Repo ablegen.")
    bauer.add_argument("auftrag", nargs="?", default="", help="Auftrag als Text")
    bauer.add_argument("--aus-datei", default="", help="Auftrag aus einer Datei lesen")
    bauer.add_argument("--titel", default="auftrag", help="Kurzname fuer den Dateinamen")
    bauer.add_argument("--turns", type=int, default=STANDARD_TURNS, help="hoechstens so viele Zuege")
    bauer.add_argument("--modell", default="opus", help="Modellname fuer claude -p")
    bauer.add_argument("--aufwand", default="medium", help="Denkaufwand: low|medium|high")
    argumente = bauer.parse_args()
    auftrag = argumente.auftrag
    if argumente.aus_datei:
        with open(argumente.aus_datei, encoding="utf-8") as datei:
            auftrag = datei.read()
    if not auftrag.strip():
        print("Kein Auftrag angegeben.")
        return 2
    ergebnis = frage(auftrag, argumente.titel, argumente.turns, argumente.modell, argumente.aufwand)
    pfad = schreibe(auftrag, argumente.titel, ergebnis, argumente.modell, argumente.aufwand)
    antwort = (ergebnis["daten"].get("result") or "").strip()
    print("Ablage: %s" % pfad)
    print("Abschluss: %s, Zuege: %s, Dauer: %.0f s, Listenpreis: %s USD (Abo, keine Zahlung)" % (
        ergebnis["daten"].get("subtype"), ergebnis["daten"].get("num_turns"), ergebnis["dauer"],
        ergebnis["daten"].get("total_cost_usd")))
    print("--- Anfang der Antwort ---")
    print(antwort[:1500])
    return 0 if antwort else 1


if __name__ == "__main__":
    sys.exit(main())
