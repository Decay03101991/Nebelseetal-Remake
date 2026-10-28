"""Lokale Einrichtung eines SEPARATEN Admin-Passworts fuer den Teststand.

Aufruf (Windows): python tools/admin_einrichten.py
Es wird kein Geheimnis im Quellcode, in einer ZIP oder in einem Chat hinterlegt.
"""
from pathlib import Path
import getpass
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))
import tor

ADMIN_TOR = str(Path(__import__('os').environ.get('NEBEL_SPIELDATEN_ORDNER') or tor.ORDNER) / 'admin_tor.json')


def main():
    if tor.hat_passwort(ADMIN_TOR):
        print('Admin-Konto bereits eingerichtet; nichts ueberschrieben.')
        return 1
    print('Admin-Teststand: Einrichtung eines zweiten, gesonderten Passworts.')
    print('Nur lokal verwenden, Admin-Passwort niemals im Chat oder Projektarchiv teilen.')
    pwd = getpass.getpass('Neues Admin-Passwort (mind. 12 Zeichen): ')
    repeat = getpass.getpass('Wiederholen: ')
    if len(pwd) < 12:
        print('Mindestens 12 Zeichen erforderlich.')
        return 1
    ok, msg = tor.setze_passwort(pwd, repeat, ADMIN_TOR)
    print(msg)
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
