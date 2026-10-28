"""Externe GPT-Pruefung: drei Slots, Admin-Zugriff, reproduzierbarer Teststand.

Es wird keine echte Benutzerdatei geoeffnet/ueberschrieben. Fensterslos pruefbar.
"""
from __future__ import annotations
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import abschnitt, check, ausnahme, bericht, import_src
import_src()

import main
import gelaende
import spielstaende
import admin_teststand
import speichern
import tor


def pruefen():
    abschnitt('Drei voneinander getrennte Slots')
    with tempfile.TemporaryDirectory() as temp:
        paths = [spielstaende.slot_pfad(temp, i) for i in (1, 2, 3)]
        check('Slot-Pfade drei verschiedene Namen', len(set(paths)) == 3)
        check('kein Pfad ist der Altstand', all(p != spielstaende.altstand_pfad(temp) for p in paths))
        check('Admin-Pfad getrennt', spielstaende.admin_pfad(temp) not in paths)
        check('leere Slots werden gezeigt', all('leer' in spielstaende.slot_status(temp, i) for i in (1,2,3)))
        for bad in (0, 4, -1, '1', 1.0, True):
            try:
                spielstaende.slot_pfad(temp, bad)
            except ValueError:
                check(f'ungueltiger Slot {bad!r} abgewiesen', True)
            else:
                check(f'ungueltiger Slot {bad!r} abgewiesen', False)
        stand1 = main.GameState()
        stand1.day = 6
        check('Slot1 sichert', stand1.save(paths[0]))
        check('Slot2 bleibt leer', not os.path.exists(paths[1]))
        check('Slot3 bleibt leer', not os.path.exists(paths[2]))
        check('Slot1 Status hat Tag6', 'Tag 6' in spielstaende.slot_status(temp, 1))
        check('Slot1 laedt', main.GameState().load(paths[0]))
        alt = spielstaende.altstand_pfad(temp)
        stand1.day = 19
        check('Altstand wird separat gesichert', stand1.save(alt))
        data, _ = speichern.lade(paths[0])
        check('Altstand hat Slot nicht ueberschrieben', data['day'] == 6)
        check('Altstand bleibt 19', speichern.lade(alt)[0]['day'] == 19)

        abschnitt('Getrenntes Passworttor')
        admin_tor = os.path.join(temp,'admin_tor.json')
        check('kein unkonfiguriertes Admin-Tor', not tor.hat_passwort(admin_tor))
        ok, _ = tor.setze_passwort('test-only-admin-12','test-only-admin-12',admin_tor)
        check('eigenes Admin-Tor installierbar', ok and tor.hat_passwort(admin_tor))
        check('richtiges Test-Passwort akzeptiert', tor.pruefe_passwort('test-only-admin-12',admin_tor)[0])
        check('falsches Passwort abgewiesen', not tor.pruefe_passwort('falsch',admin_tor)[0])

        abschnitt('Admin-Testwelt ohne normale Spielslots')
        state = main.GameState()
        state.generate_map(state.current_map)
        admin_teststand.teststand_aufbauen(state, main.Settlement, main.siedlung_kennung)
        check('Admin-Marker nur im Teststand', state.admin_teststand)
        check('sechs unterschiedliche Doerfer', len(state.settlements) == 6 and
              len({s.id for s in state.settlements}) == 6)
        check('sechs unterschiedliche Kartentypen', len({s.karte['typ'] for s in state.settlements}) == 6)
        for ort in state.settlements:
            # GPT-OK02: neues Originalarchiv ist 10x10; der Quell-Sumpfanteil
            # variiert je Karte, deswegen NICHT die alte 56/40-Konstante nutzen.
            check(f'{ort.name} 100-Felder-Originalkarte', len(ort.karte['raster']) == 100 and
                  ort.karte['spalten'] == ort.karte['zeilen'] == 10 and
                  sum(gelaende.ist_bebaubar(a) for a in ort.karte['raster']) ==
                  100 - ort.karte['zaehlung']['sumpf'])
            check(f'{ort.name} kein Bau auf Sumpf', all(
                ort.karte['raster'][int(i)] != 'sumpf' for i in ort.bauten))
            check(f'{ort.name} hat Holz+Steinproduktion',
                  state.ertrag_je_ort(ort).get('holz',0)>0 and state.ertrag_je_ort(ort).get('stein',0)>0)
            check(f'{ort.name} lokale Vorratsbasis', ort.vorraete['stein'] >= 1000 and
                  ort.vorraete['holz'] >= 1000)
            check(f'{ort.name} Karren und Kampftruppen',
                  ort.einheiten.get('Handkarren',0) > 0 and ort.einheiten.get('Krieger',0) > 0)
            check(f'{ort.name} Warenlager original',
                  len(ort.waren) == len(state.waren) and all(v > 0 for v in ort.waren.values()))
        check('nicht in normalen Slot sicherbar', not state.save(paths[0]))
        check('Originalslot blieb unveraendert', speichern.lade(paths[0])[0]['day'] == 6)
        ap = spielstaende.admin_pfad(temp)
        check('Admin-Speicherung mit Freigabe', state.save(ap,admin_freigabe=True))
        check('Admin-Feld steht in gespeicherten Daten', speichern.lade(ap)[0]['admin_teststand'] is True)
        neu = main.GameState()
        check('ohne Freigabe wird Adminstand abgewiesen', not neu.load(ap))
        check('abgewiesener Stand mutiert keine Karte', len(neu.settlements) == 0 and not neu.admin_teststand)
        check('Admin kann laden', neu.load(ap,admin_freigabe=True))
        check('Adminzustand nach Laden vollstaendig',
              neu.admin_teststand and len(neu.settlements)==6 and
              neu.settlements[0].vorraete['stein'] == state.settlements[0].vorraete['stein'])
        check('normales Laden setzt Admin-Marker zurueck', neu.load(paths[0]) and not neu.admin_teststand)
        check('Altstand wird nicht automatisch zum Adminstand', not neu.admin_teststand)


if __name__ == '__main__':
    ausnahme('Speicher-/Admin-Integrationslauf', pruefen)
    sys.exit(bericht())
