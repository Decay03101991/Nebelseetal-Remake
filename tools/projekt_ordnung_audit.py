#!/usr/bin/env python3
"""Read-only Nebelseetal project hygiene audit for an EXISTING Hermes cleanup job.

Only generates local reports. Never deletes, moves, edits project files, or schedules jobs.
Example: py -3 tools/projekt_ordnung_audit.py
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

ACTIVE_ROOT = {"README.md", "START_SPIEL_WINDOWS.bat", "EXE_ERSTELLEN_WINDOWS.bat", "START_EXE_TEST_WINDOWS.bat", "run_tests.bat"}
CANONICAL = {"docs/ENTWICKLUNGSPROTOKOLL.md", "docs/AKTUELLER_STAND.md", "docs/HERMES_UEBERGABE_AKTUELL.md", "README.md"}
EXCLUDES = {"archiv", "alles alte", ".git", "__pycache__", "original", ".venv", "venv", "dist", "build", ".github"}
DOC_EXT = {".md", ".txt", ".rst"}
OLD_ROOT = {"START_HIER.txt", "PROJEKTUEBERSICHT_WINDOWS.txt", "Nebelseetal_Remake.bat", "EXE_NEUESTEN_STAND_BAUEN.bat", "NEBELSEETAL_FIX02_FORTSCHRITT_WINDOWS.txt", "NEBELSEETAL_FIX02c_PRUEFBERICHT_WINDOWS.txt"}


def audit(root: Path) -> dict:
    issues = []
    if not (root / "src" / "main.py").is_file():
        raise ValueError(f"Kein erkanntes Nebelseetal-Hauptprojekt: {root}")
    # Root-Dateien nur unmittelbar lesen, docs/ einmal rekursiv. Sonst
    # erscheint dasselbe Dokument wegen doppeltem Walk als falsches Duplikat.
    present = []
    if root.is_dir():
        for path in sorted(root.iterdir()):
            if path.is_file() and path.suffix.lower() in DOC_EXT | {".bat", ".cmd"}:
                present.append(path)
    docs = root / "docs"
    if docs.is_dir():
        for path in sorted(docs.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in DOC_EXT | {".bat", ".cmd"}:
                continue
            if any(part.casefold() in EXCLUDES for part in path.relative_to(docs).parts[:-1]):
                continue
            present.append(path)
    by_hash = defaultdict(list)
    for path in present:
        rel = path.relative_to(root).as_posix()
        if path.suffix.lower() in DOC_EXT and path.stat().st_size < 8_000_000:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            by_hash[digest].append(rel)
    for group in by_hash.values():
        if len(group) > 1:
            issues.append({"typ": "IDENTISCHER_DOKUMENTINHALT", "pfade": group, "empfehlung": "Verwendung und Referenzen pruefen, nur nach Freigabe archivieren", "risiko": "mittel"})
    for file in OLD_ROOT:
        if (root / file).is_file():
            issues.append({"typ": "MOEGLICHER_ALTEINSTIEG", "pfade": [file], "empfehlung": "Pruefen, ob bereits durch aktive Start-/Build-Datei abgedeckt, dann geprueft archivieren", "risiko": "mittel"})
    for rel in sorted(CANONICAL):
        if not (root / rel).is_file():
            issues.append({"typ": "KANONISCH_FEHLT", "pfade": [rel], "empfehlung": "Aktuellen Pfad und erlaubte Umzuege pruefen", "risiko": "hoch"})
    # Heuristics are suggestions, not a declaration of an unused or obsolete file.
    for path in present:
        rel = path.relative_to(root).as_posix()
        if rel in CANONICAL:
            continue
        name = path.name.lower()
        if path.parent == root and path.suffix.lower() == ".txt" and ("start" in name or "uebersicht" in name or "fortschritt" in name or "prüfbericht" in name or "pruefbericht" in name):
            issues.append({"typ": "ROOT_DOKUMENT_ZU_PRUEFEN", "pfade": [rel], "empfehlung": "Mit README.md, docs/HERMES_UEBERGABE_AKTUELL.md und docs/AKTUELLER_STAND.md vergleichen; Zusammenfassung vorschlagen", "risiko": "niedrig"})
        if path.parent == root / "docs" and path.suffix.lower() == ".md" and ("uebergabe" in name or "start_hermes" in name or "projekt_stand" in name or "entwicklungsprotokoll_" in name):
            issues.append({"typ": "PARALLELE_DOKUMENTATION_PRUEFEN", "pfade": [rel], "empfehlung": "Pruefen ob historische Kopie; eine aktuell gueltige Fassung und nur Archivkopien", "risiko": "mittel"})
    return {
        "projekt": str(root),
        "datum_utc": datetime.now(timezone.utc).isoformat(),
        "modus": "NUR_LESEN_KEINE_AENDERUNGEN",
        "gescannte_root_und_docs_dateien": len(present),
        "hinweise": issues,
        "naechste_aktion": "Hermes: Bericht pruefen, mit bestehenden Skills abgleichen und Vorschlaege vorlegen. Cronjob niemals automatisch loeschen/verschieben lassen."
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Nebelseetal-Ordnungspruefung ohne Schreibzugriff aufs Projekt")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--report-dir", type=Path, default=None)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        report = audit(root)
    except (OSError, ValueError) as ex:
        print(f"ABBRUCH: {ex}")
        return 2
    if args.report_dir is not None:
        output = args.report_dir.expanduser().resolve()
    elif os.environ.get("LOCALAPPDATA"):
        output = Path(os.environ["LOCALAPPDATA"]) / "Nebelseetal_Remake" / "cleanup_reports"
    else:
        output = Path.home() / ".local" / "share" / "Nebelseetal_Remake" / "cleanup_reports"
    if root == output or root in output.parents:
        print("ABBRUCH: Berichtsausgabe darf nicht im Projekt liegen")
        return 2
    output.mkdir(parents=True, exist_ok=True)
    name = f"ordnung_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    result = output / name
    result.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Ordner-Audit (nur lesend): {len(report['hinweise'])} Hinweise, {report['gescannte_root_und_docs_dateien']} Dateien angesehen")
    print(f"Lokaler Bericht: {result}")
    print("ACHTUNG: Heuristische Hinweise, keine sicheren Loeschkandidaten. Es wurde NICHTS verschoben oder geloescht.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
