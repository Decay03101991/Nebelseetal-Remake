"""Regression fuer die gespiegelte Reichskasse im oeokonomie-1-Modus.

Keine Originaldateien werden geaendert. Normalmodus dokumentiert Befunde;
--strict macht daraus Abnahmetests nach der Reparatur.
"""
from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src
ROOT, SRC = import_src()
import main
import spieloekonomie
STRICT = '--strict' in sys.argv

def erwarte(name, ok, details=''):
    if ok or STRICT:
        check(name, ok, details)
    else:
        befund(name, details)

def simuliere():
    g = main.GameState()
    g.resources['holz'].amount = 0
    karte = spieloekonomie.startkarte('gpt-doppelquelle-test', 'spieler')
    feld = karte['raster'].index('wald')
    ort = main.Settlement(id='testort', name='Testort', map_id='kontinent',
                          karte=karte, vorraete={'holz':0},
                          bauten={str(feld):'holzfaeller'}, stufen={str(feld):1})
    g.settlements = [ort]
    g.tick(3600)
    return g, ort

abschnitt('Echte Holzernte fuer eine Spielstunde')
g, ort = simuliere()
check('Spielstand benutzt neueren Oekonomiemodus', g.mode == 'oeokonomie-1', str(g.mode))
check('Ernte: 4 Waldholz + 1 Grundeinkommen im Ortslager', ort.vorraete['holz']==5.0, str(ort.vorraete))
check('Reichsressource spiegelt dieselben 5 Holz', g.resources['holz'].amount==5.0,
      str(g.resources['holz'].amount))
abschnitt('Doppelte Deckung trotz nur 5 Holz im einzigen Ort')
erwarte('7 Holz duerfen lokal nicht gedeckt sein',
        'holz' in g.ortsdeckung(ort, {'holz':7}), str(g.ortsdeckung(ort, {'holz':7})))
erwarte('Reichsweite Deckung darf gespiegelte 5 Holz nicht als 10 behandeln',
        'holz' in g.reichsdeckung({'holz':7}), str(g.reichsdeckung({'holz':7})))
g2, ort2 = simuliere()
ok, meldung=g2.verbrauche_am_ort(ort2, {'holz':7})
erwarte('Realer Ortsbau 7 Holz darf nicht aus der gespiegelten Kasse gelingen', not ok,
        f'ok={ok}, Ort={ort2.vorraete["holz"]}, Reich={g2.resources["holz"].amount}')
g3, ort3 = simuliere()
ok3, meldung3=g3.verbrauche_reichsweit({'holz':7})
erwarte('Reichsweite 7-Holz-Zahlung mit nur 5 echtem Holz muss scheitern', not ok3,
        f'ok={ok3}, Ort={ort3.vorraete["holz"]}, Reich={g3.resources["holz"].amount}')
abschnitt('Auch Siedlerduplikate als Risiko der gleichen Ursache')
g4, ort4 = simuliere()
# Ein global mitgefuehrter Siedlerstand ist eine Anzeige der ortsweisen Bevoelkerung,
# aber die Zahlungsprobe darf ihn im Neumodus nicht noch einmal als eigenes Reservoir ansehen.
ort4.bevoelkerung = 5.0
g4.population = 5.0
check('Lokale Siedlerzahl des Testorts ist 5', ort4.bevoelkerung == 5)
erwarte('8 Siedler nicht durch Addition derselben 5+5 finanzierbar',
        'siedler' in g4.ortsdeckung(ort4, {'siedler':8}),
        f'Ort={ort4.bevoelkerung}, Gesamt={g4.population}, Deckung={g4.ortsdeckung(ort4, {"siedler":8})}')

sys.exit(bericht())
