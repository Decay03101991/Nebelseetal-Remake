"""Ehrliche, portable Vorpruefung VOR einem Windows-Testbuild.

Keine erzwungene 'Releasefreigabe' und kein globales Beenden frueher roter Alttests.
Autor: ChatGPT, externer Entwicklungsagent / 28.10.2026.
"""
from __future__ import annotations
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
TESTS = (
    'test_gpt_ne01_origwerte.py',
    'test_gpt_kampf_forum_neu.py',
    'test_kampf_einhaengung.py',
    'test_gpt_wirtschaft_kette_e2e.py',
    'test_gpt_originalkarten_katalog.py',
    'test_gpt_profile_login.py',
)


def run() -> int:
    print(f'Projekt: {ROOT}', flush=True)
    for rel in ('src/main.py', 'data/gelaende.json', 'assets', 'tests/vorlagen'):
        if not (ROOT / rel).exists():
            print(f'FEHLER: {rel} fehlt', flush=True)
            return 1
    # Der Test aus einem FREMDEN Verzeichnis verhindert Abhaengigkeiten vom Arbeitsordner.
    check = ('import sys;sys.path.insert(0,sys.argv[1]);import spieldaten;'
             'assert spieldaten.projektwurzel()==sys.argv[2], spieldaten.projektwurzel();'
             'print("Datenpfad aus Fremdordner OK")')
    import tempfile
    with tempfile.TemporaryDirectory(prefix='nebelseetal_fremdpfad_') as cwd:
        p = subprocess.run([sys.executable, '-c', check, str(ROOT/'src'), str(ROOT)],
                           cwd=cwd, capture_output=True, text=True, timeout=20)
    print(p.stdout or p.stderr, flush=True)
    if p.returncode:
        return 1
    passed = 0
    for name in TESTS:
        path = ROOT / 'tests' / name
        if not path.exists():
            print(f'FEHLER: Testdatei fehlt: {name}', flush=True)
            return 1
        print(f'Pruefe {name} ...', flush=True)
        try:
            p = subprocess.run([sys.executable, str(path)], cwd=str(ROOT),
                               capture_output=True, text=True, timeout=120,
                               env={**os.environ, 'PYTHONUTF8': '1'})
        except subprocess.TimeoutExpired:
            print(f'FEHLER: {name} ist in 120 Sekunden nicht abgeschlossen.', flush=True)
            return 1
        text = (p.stdout or '') + '\n' + (p.stderr or '')
        # Auch 'schlechte' Tests mit Exit-Code 0, aber FEHLER-Text erkennen.
        error_markers = ('FEHLER ', 'FEHLER:', 'Traceback (most recent call last)',
                         'FAILED (failures=', 'FAILED (errors=', 'ERGEBNIS: 0 bestanden,')
        if p.returncode or any(marker in text for marker in error_markers):
            print(f'ROT: {name}; exit={p.returncode}\n{text[-3500:]}', flush=True)
            return 1
        print(f'GRUEN: {name}', flush=True)
        passed += 1
    print(f'Vorpruefung OK: {passed}/{len(TESTS)} Testdateien. KEINE vollstaendige Releasepruefung.', flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(run())
