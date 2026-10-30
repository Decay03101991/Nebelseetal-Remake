"""Unabhaengige Integrationspruefung nach Originalhandbuch und Daniels Karten-/Handelsentscheidungen.

Standard: rot erkannte Altabweichung = BEFUND, damit Hermess Sammellauf nicht ungesteuert
blockiert. --strict: dieselben Abweichungen werden FEHLER zur gezielten Reparaturabnahme.
"""
from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src
ROOT,SRC=import_src()
import main as M
import spieloekonomie as O
strict='--strict' in sys.argv

def erwarte(name, gut, details=''):
    if gut or strict: check(name, gut, details)
    else: befund(name, details)

abschnitt('Ortslager darf NICHT aus Reichskasse bezahlen (neuer Oekonomiemodus)')
g=M.GameState()
a=M.Settlement(id='a',name='Dorf A',map_id='kontinent',vorraete={'holz':0,'stein':0})
b=M.Settlement(id='b',name='Dorf B',map_id='kontinent',vorraete={'holz':100,'stein':100})
g.settlements=[a,b]
g.resources['holz'].amount=100
vor=(dict(a.vorraete),dict(b.vorraete),g.resources['holz'].amount)
# Nur die Deckungsfrage pruefen: sie darf bei fehlender LOKALER Deckung kein OK melden.
fehl=g.ortsdeckung(a,{'holz':10})
erwarte('Dorf A ohne Holz: Bau nicht bezahlt, obwohl Dorf B 100 Holz besitzt',
        'holz' in fehl, f'ortsdeckung={fehl}; Dorflager A={a.vorraete}, B={b.vorraete}')
check('Deckungsprobe veraendert nichts',vor==(dict(a.vorraete),dict(b.vorraete),g.resources['holz'].amount))
# Die BUCHUNG selbst bestaetigt das Problem (nur auf einem Wegwerf-Spielstand).
erfolg,meldung=g.verbrauche_am_ort(a,{'holz':10})
erwarte('Buchung ohne lokales Holz wird abgelehnt',not erfolg,
        f'erfolg={erfolg}, A={a.vorraete}, B={b.vorraete}, Reich={g.resources["holz"].amount}')

abschnitt('Gebaeude ohne Forschung Baukunst duerfen nicht baubar sein')
g2=M.GameState()
k=O.startkarte('test-002','spieler')
s=M.Settlement(id='s',name='Dorf',map_id='kontinent',karte=k,vorraete={'holz':100,'stein':100})
feld=k['raster'].index('grasland')
# bau auf karte ist der Kern hinter der UI; diese Platzierung prueft keine Forschungsstufe.
ok,meldung=M.bauen_auf_karte(s,'farm',feld)
erwarte('Farm ohne Baukunst muss abgelehnt werden',not ok,
        f'erlaubt={ok}, meldung={meldung}, gelaende={k["raster"][feld]}, research[Baukunst]=0')
# Original: Holzfaeller ohne Forschung erlaubt und Sumpf gesperrt.
s2=M.Settlement(id='s2',name='Dorf',map_id='kontinent',karte=k,vorraete={'holz':100,'stein':100})
wald=k['raster'].index('wald')
ok_h,_=M.bauen_auf_karte(s2,'holzfaeller',wald)
check('Holzfaeller als Startbau zugelassen',ok_h)
sumpf=k['raster'].index('sumpf')
ok_s,_=M.bauen_auf_karte(s2,'holzfaeller',sumpf)
check('Sumpf als Bauplatz gesperrt',not ok_s)

abschnitt('Kern-Kassenbuch als korrekte Referenz')
ort={'id':'a','vorraete':{'holz':0},'importiert':{'holz':0},'verbrauchsjournal':[]}
try: O.verbrauchen(ort,{'holz':10},0)
except ValueError: ok_kern=True
else:ok_kern=False
check('spieloekonomie.verbrauchen verhindert lokale Unterdeckung korrekt',ok_kern)

sys.exit(bericht())
