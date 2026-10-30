"""Prueft Ergebnis-TEXT plus Prozess-RC statt 'exit 0' blind zu vertrauen.

Externe Zuarbeit 28.10.2026. Kein Ersatz fuer den Windows-Sammellauf.
Beispiel: python tools/gpt_prueflauf_ehrlich.py tests/test_spielzeit.py
"""
from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys

ERGEBNIS = re.compile(r'ERGEBNIS:\s*(\d+)\s*bestanden,\s*(\d+)\s*Fehler,\s*(\d+)\s*Befunde',re.I)
UNITTEST = re.compile(r'Ran\s+(\d+)\s+tests?\s+in\s+',re.I)
UNITTEST_FAIL = re.compile(r'^FAILED\s*\(',re.M)
UNITTEST_OK = re.compile(r'^OK\s*$',re.M)


def prueftext(ausgabe: str, rc: int):
    """(bool, bestandene Tests, Fehleranzahl, Meldung). Befunde sind kein Fehler."""
    treffer=list(ERGEBNIS.finditer(ausgabe))
    if treffer:
        # Letztes Ergebnis ist massgeblich; es kann mehrere Abschnitte geben.
        m=treffer[-1]
        bestanden,fehler,befunde=(int(x) for x in m.groups())
        return rc == 0 and fehler == 0, bestanden, fehler, f'{bestanden} OK, {fehler} Fehler, {befunde} Befunde, RC {rc}'
    u=list(UNITTEST.finditer(ausgabe))
    if u:
        fehler=int(bool(UNITTEST_FAIL.search(ausgabe)))
        ok=bool(UNITTEST_OK.search(ausgabe)) and fehler == 0 and rc == 0
        return ok, int(u[-1].group(1)) if ok else 0,fehler, f'unittest: {"OK" if ok else "FEHLER"}, RC {rc}'
    # Kein erkannter Textbeleg => kein 'gruen' nur aus dem Prozesscode.
    return False,0,0,f'KEIN PRUEFBELEG, RC {rc}'


def ausfuehren(testdatei, timeout=60):
    try:
        lauf=subprocess.run([sys.executable,'-X','utf8',str(testdatei)],
                            stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                            text=True,encoding='utf-8',errors='replace',timeout=timeout)
        return prueftext(lauf.stdout,lauf.returncode),lauf.stdout
    except subprocess.TimeoutExpired as e:
        return (False,0,1,f'Timeout nach {timeout} s'),str(e)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('dateien',nargs='+')
    p.add_argument('--timeout',type=int,default=60)
    a=p.parse_args(argv)
    gesamt=0
    ok_all=True
    for name in a.dateien:
        path=pathlib.Path(name)
        (ok, bestanden, fehler, msg),ausgabe=ausfuehren(path,a.timeout)
        gesamt+=bestanden
        ok_all &= ok
        print(f'{"OK" if ok else "ROT"} {path.name}: {msg}')
        if not ok:
            print('  Ursache:')
            print('\n'.join(ausgabe.splitlines()[-20:]))
    print('TESTGESAMT',gesamt,'bestanden; Freigabe:', 'JA' if ok_all else 'NEIN')
    return 0 if ok_all else 1

if __name__=='__main__':raise SystemExit(main())
