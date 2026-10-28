"""Externe, nur lesende Pruefdatei. Kein tkinter, kein Commit, keine Hauptdatei."""
from __future__ import annotations
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src
ROOT, SRC = import_src()
import gpt_versorgungsdiagnose as D
import spieloekonomie as O


def ort(bauten=None, vorraete=None, bewohner=10):
    k = O.startkarte('audit-002', 'spieler')
    return {'id': 's1', 'name': 'Testsiedlung', 'karte': k,
            'bauten': bauten or {}, 'vorraete': vorraete if vorraete is not None else {'holz': 100, 'stein': 100},
            'bevoelkerung': bewohner}

def feld(k, art):
    return k['karte']['raster'].index(art)

abschnitt('Originalkarte und Startversorgung')
a = ort()
d = D.untersuche(a)
check('Originalkarte: 100 Felder', d['kartenfelder'] == 100, str(d['kartenfelder']))
check('Baufelder sind 100 minus tatsaechliche Suempfe', d['bebaubare_felder'] == 100 - a['karte']['zaehlung']['sumpf'], str(d['bebaubare_felder']))
check('Start: Holzfaeller sofort erreichbar', any(x['gebaeude'] == 'holzfaeller' and x['status']=='sofort_baubar' for x in d['grundversorgung']['holz']['bauoptionen']))
check('Start: Steinmetz sofort erreichbar', any(x['gebaeude'] == 'steinmetz' and x['status']=='sofort_baubar' for x in d['grundversorgung']['stein']['bauoptionen']))
check('Start: Jaeger sofort erreichbar', any(x['gebaeude'] == 'jaeger' and x['status']=='sofort_baubar' for x in d['grundversorgung']['nahrung']['bauoptionen']))
check('Farm wartet auf Baukunst', any(x['status']=='forschung_fehlend' for x in d['grundversorgung']['nahrung']['bauoptionen']))
abschnitt('Keine erfundenen Rohstoffe oder Rettung')
b = ort(vorraete={'holz': 0, 'stein': 0})
db = D.untersuche(b)
check('Holz ohne Gebaeude waechst mit 1 pro Stunde', db['grundversorgung']['holz']['produktion_pro_spielstunde']==1 and db['grundversorgung']['holz']['status']=='laufende_produktion')
check('Stein ohne Gebaeude waechst mit 1 pro Stunde', db['grundversorgung']['stein']['produktion_pro_spielstunde']==1 and db['grundversorgung']['stein']['status']=='laufende_produktion')
check('Nahrung durch Holz-/Stein-Grundrate erschiessbar', db['grundversorgung']['nahrung']['status']=='produzent_erschliessbar')
check('Eingabestand bleibt unveraendert', b['vorraete']=={'holz': 0, 'stein':0})
check('Keine falsch positiven Warnungen durch Grundversorgung', db['warnungen']==[])
abschnitt('Produktion und Warten')
c = ort(vorraete={'holz': 0, 'stein': 10})
wald = feld(c, 'wald')
c['bauten'][str(wald)] = 'holzfaeller'
dc = D.untersuche(c)
check('Waldholz 4 plus Grundversorgung 1 pro Stunde', dc['grundversorgung']['holz']['produktion_pro_spielstunde']==5.0)
check('Holz kann durch Warten fuer Steinmetz erworben werden', any(x['gebaeude']=='steinmetz' and x['status']=='durch_warten_erreichbar' and abs(x['wartezeit_stunden']-1.0)<1e-6 for x in dc['grundversorgung']['stein']['bauoptionen']))
check('Warten ist keine Rohstoffgutschrift', c['vorraete']['holz']==0)
check('Textansicht zeigt ehrliche Produktion', '1/h' in D.drucktext(db) and 'keine laufende Produktion' not in D.drucktext(db))
sys.exit(bericht())
