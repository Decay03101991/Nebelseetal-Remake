"""Prueft das Entwicklungsprotokoll auf seine eigenen Regeln — ohne den Text zu bewerten.

Was dieses Werkzeug prueft (und was nicht), ehrlich gesagt:
  * Es prueft die **Form**: Zielgroesse, Tabellenzeilen, Zeitangaben, dass keine Sicherungszeilen
    darin stehen (die gehoeren in `docs/SICHERUNGEN.md`).
  * Es prueft die **Belegbarkeit**: jede im Protokoll genannte Commit-Kennung muss es in git
    wirklich geben. Erfundene Kennungen fliegen auf.
  * Es prueft **Vollstaendigkeit gegen die Vor-Fassung**: jede Commit-Kennung und jede Pruefzahl
    der Vor-Verdichtung muss in der geltenden Fassung noch vorkommen (Verdichten darf nie auf
    Kosten von Inhalt gehen).
  * Es prueft NICHT, ob eine Aussage inhaltlich stimmt. Das kann nur der Mensch oder eine
    Gegenprobe im Projekt selbst.

Aufruf:
    python tools/pruefe_protokoll.py                 (geltende Fassung gegen die Vor-Fassung)
    python tools/pruefe_protokoll.py --nach <datei>  (eine andere Fassung pruefen)
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
PROTOKOLL = WURZEL / "docs" / "ENTWICKLUNGSPROTOKOLL.md"
VORFASSUNG = WURZEL / "archiv" / "dokumentation" / "protokoll_alte_fassungen" / "ENTWICKLUNGSPROTOKOLL_VOR_VERDICHTUNG_2026-10-05.md"
SICHERUNGEN = WURZEL / "archiv" / "dokumentation" / "projektunterlagen_historisch" / "SICHERUNGEN.md"

# Zielgroesse aus den Regeln im Protokollkopf (Verdichtung 04.10.: 364 -> 300 Zeilen).
ZIELZEILEN = 320
COMMIT = re.compile(r"\b[0-9a-f]{7}\b")
PRUEFZAHL = re.compile(r"\b\d{1,4}\s*/\s*\d{1,3}\s*/\s*\d{1,3}\b|\b\d{1,4}\s+bestanden\b")
ZEILE = re.compile(r"^\|\s*\d{1,2}[:.]\d{2}")

fehler: list[str] = []
befunde: list[str] = []


def melde(text: str) -> None:
    print(text, flush=True)


def git_kennt(kennung: str) -> bool:
    lauf = subprocess.run(["git", "cat-file", "-e", f"{kennung}^{{commit}}"],
                          cwd=WURZEL, capture_output=True, text=True)
    return lauf.returncode == 0


def main() -> int:
    zerleger = argparse.ArgumentParser(description="Entwicklungsprotokoll pruefen")
    zerleger.add_argument("--nach", default=str(PROTOKOLL), help="zu pruefende Fassung")
    argumente = zerleger.parse_args()
    ziel = Path(argumente.nach).resolve()
    if not ziel.exists():
        melde(f"FEHLER: Datei fehlt: {ziel}")
        return 1

    text = ziel.read_text(encoding="utf-8")
    zeilen = text.splitlines()
    try:
        name = ziel.relative_to(WURZEL)
    except ValueError:
        name = ziel
    melde(f"Fassung: {name} — {len(zeilen)} Zeilen, {len(text)} Zeichen")

    # 1. Form
    if len(zeilen) > ZIELZEILEN:
        befunde.append(f"Zielgroesse ueberschritten: {len(zeilen)} Zeilen (Regel: unter {ZIELZEILEN}) "
                       f"-> verdichten, aber nie auf Kosten von Inhalt")
    tabellenzeilen = [z for z in zeilen if z.startswith("| ")]
    # Kopf- und Hilfszeilen anderer Tabellen (Meilensteine, Kosten, Plaene) sind keine Schritte.
    kopfwoerter = ("| Was ", "|---", "| Zeit ", "| Zeitraum", "| Wert", "| Größe", "| Kosten",
                   "| Messung", "| Prüfung", "| Frage", "| Tabelle", "| Schritt ")
    ohne_zeit = [z for z in tabellenzeilen if not ZEILE.match(z) and not z.startswith(kopfwoerter)
                 and ZEILE.match(z) is None and z.count("|") >= 3
                 and any(w in z[:24] for w in (":", "–", "("))]
    melde(f"  Tabellenzeilen: {len(tabellenzeilen)}, Zeitangaben nach Muster: "
          f"{len([z for z in tabellenzeilen if ZEILE.match(z)])}")
    if ohne_zeit:
        befunde.append(f"{len(ohne_zeit)} Tabellenzeile(n) ohne Zeitangabe im Schritt-Muster")

    # 2. Sicherungszeilen gehoeren nicht ins Protokoll (nur echte Eintraege zaehlen, nicht die
    #    Rede ueber sie: eine Zeile, deren Schritt-Spalte "Sicherungszeile" heisst).
    sicherungszeilen = [z for z in zeilen
                        if re.match(r"^\|\s*\d{1,2}[:.]\d{2}\s*\|\s*\*{0,2}Sicherungszeile", z)]
    if sicherungszeilen:
        befunde.append(f"{len(sicherungszeilen)} Sicherungszeile(n) im Protokoll — die gehoeren nach "
                       f"{SICHERUNGEN.name}")
    else:
        melde("  Keine Sicherungszeilen im Protokoll (wie vorgesehen)")

    # 4b. Prosa-Verluste finden: jeder Absatz der Vor-Fassung beginnt mit einer fetten Ueberschrift
    #     ("**...**"). Fehlt deren Wortlaut in der geltenden Fassung, kann der ganze Absatz
    #     verschwunden sein — genau dieser Fall ist am 05.10.2026 einmal aufgetreten
    #     ("Was danach noch offen ist"). Gemeldet wird als Befund zum Nachsehen, nicht als Fehler:
    #     ein umformulierter Anfang ist erlaubt, ein fehlender Absatz nicht.
    if VORFASSUNG.exists() and ziel != VORFASSUNG:
        alt_text = VORFASSUNG.read_text(encoding="utf-8")
        anfaenge = {a.strip() for a in re.findall(r"^\*\*([^*\n]{8,80})\*\*", alt_text, re.M)}
        fehlende_anfaenge = sorted(a for a in anfaenge if a not in text)
        melde(f"  Absatz-Anfaenge der Vor-Fassung: {len(anfaenge)}, nicht mehr woertlich vorhanden: "
              f"{len(fehlende_anfaenge)}")
        if fehlende_anfaenge:
            befunde.append("Absatz-Anfaenge der Vor-Fassung fehlen woertlich (einzeln nachsehen, ob "
                           f"der Inhalt verloren ging): {' | '.join(fehlende_anfaenge[:10])}")

    # 5. Belegbarkeit: jede Commit-Kennung muss es in git geben
    kennungen = sorted(set(COMMIT.findall(text)))
    kennungen = [k for k in kennungen if not k.isdigit()]
    unbekannt = [k for k in kennungen if not git_kennt(k)]
    melde(f"  Commit-Kennungen im Text: {len(kennungen)}, davon unbekannt: {len(unbekannt)}")
    if unbekannt:
        fehler.append(f"unbelegte Commit-Kennung(en): {', '.join(unbekannt)}")

    # 4. Verdichten darf nichts wegnehmen: gegen die Vor-Fassung vergleichen
    if VORFASSUNG.exists() and ziel != VORFASSUNG:
        alt = VORFASSUNG.read_text(encoding="utf-8")
        alt_kennungen = {k for k in set(COMMIT.findall(alt)) if not k.isdigit()}
        alt_zahlen = set(PRUEFZAHL.findall(alt))
        jetzt_zahlen = set(PRUEFZAHL.findall(text))
        fehlende_k = sorted(alt_kennungen - set(kennungen))
        fehlende_z = sorted(alt_zahlen - jetzt_zahlen)
        melde(f"  Gegen die Vor-Fassung: {len(alt_kennungen)} Commits, {len(alt_zahlen)} Pruefzahlen")
        if fehlende_k:
            fehler.append(f"{len(fehlende_k)} Commit-Kennung(en) der Vor-Fassung fehlen: "
                          f"{', '.join(fehlende_k[:8])}")
        if fehlende_z:
            fehler.append(f"{len(fehlende_z)} Pruefzahl(en) der Vor-Fassung fehlen: "
                          f"{', '.join(fehlende_z[:8])}")
        if not fehlende_k and not fehlende_z:
            melde("  Nichts verloren: alle Commit-Kennungen und Pruefzahlen der Vor-Fassung sind da")
    else:
        befunde.append(f"Vor-Fassung nicht gefunden ({VORFASSUNG.name}) — Vollstaendigkeit nicht pruefbar")

    melde("")
    if befunde:
        melde("Befunde (kein Fehler):")
        for b in befunde:
            melde(f"  - {b}")
    if fehler:
        melde("Fehler (muessen behoben werden):")
        for f in fehler:
            melde(f"  - {f}")
        return 1
    melde("OK: Form und Belegbarkeit in Ordnung.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
