"""GPT-KA02: Original-Fund 'Das Kampfsystem.odt'; neu erklaerte Schlachtmechanik.

Eindeutige Originaldaten statt alter LE/AT/PA-Tests. Keine Uhr-/GUI-Abhaengigkeit.
Aufruf: python -X utf8 tests/test_gpt_kampf_forum_neu.py
"""
from __future__ import annotations
import copy, random, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src
import_src()
import kampf, einheiten as E, spieldaten

R = lambda n=11: random.Random(n)

class Zufall:
    """Kontrollierter Treffer-/Konstitutionstest, kein verdeckter Zufall."""
    def __init__(self, treffer): self.treffer=treffer
    def choice(self, seq): return seq[0]
    def random(self): return self.treffer
    def randint(self, lo,hi): return hi

abschnitt('A. Forum-Originalwerte – pro Einheit vollständig')
EXPECTED = {
 'Bürgerwehr': (5,1,12,0,None,0,1), 'Kämpfer': (15,4,22,2,None,0,3),
 'Krieger': (25,7,29,4,None,0,5), 'Ritter': (50,9,43,8,None,0,7),
 'Paladin': (70,17,57,12,None,0,9),
 'Kurzbogenschütze': (15,1,12,0,20,1,1), 'Bogenschütze': (25,1,12,0,30,2,2),
 'Langbogenschütze': (35,1,12,0,55,3,3), 'Armbrustschütze': (45,3,14,2,70,4,4),
 'Streuner': (5,2,15,0,None,0,1), 'Gauner': (15,2,20,0,None,0,2),
 'Dieb': (25,2,25,0,None,0,3), 'Meisterdieb': (35,2,30,0,None,0,4),
 'Kundschafter': (45,4,37,2,None,0,5), 'Waldläufer': (55,6,44,4,None,0,6)}
check('genau 15 Kampfprofile, alle in units.json', set(kampf.PROFILE)==set(EXPECTED) and set(EXPECTED)<=set(E.alle()))
for n,werte in EXPECTED.items():
    check(f'Originalprofil: {n}', kampf.PROFILE.get(n)==werte)

abschnitt('B. Wall, Schlagkraft und Geraete')
check('Originalwall Stufe 5 verlangt echte Belagerung', spieldaten.wallstufen()[4]['schwellenwert_belagerungswaffen']==500)
# Forumtext unterscheidet Nahkampfeinheiten ausdrücklich von Fernkämpfern.
# Krieger besitzt SK 3, neun Armbrustschützen hätten zusammen SK 45:
# die Fernkämpfer dürfen die Schwelle (Wall 1, SK 10) NICHT auffüllen.
fern_rechnet_nicht = kampf.fuehre_schlacht({'Krieger':1, 'Armbrustschütze':9},
                                            {'Bürgerwehr':1}, 1, rng=R())
check('Wall 1: Fernkämpfer erhöhen keine Nahkampf-Schlagkraft',
      not fern_rechnet_nicht['vorrunde_bestanden'] and
      'Fußtruppen: Schwelle nicht erreicht' in fern_rechnet_nicht['bericht'])

block=kampf.fuehre_schlacht({'Bürgerwehr':250,'Katapult':6},{'Bürgerwehr':1},5,angreifer_karren={'Katapult':6},rng=R())
check('Katapult bei Doppelargument nur EINMAL bewertet', not block['vorrunde_bestanden'] and not block['kampf_stattgefunden'])
check('gescheiterte Vorrunde verursacht weder Opfer noch Beute noch Mauerschaden',
      not block['verluste_angreifer'] and not block['verluste_verteidiger'] and not block['beute'] and block['mauer_zustand']==100)
check('abgeschlagener Angriff im Bericht klar erkennbar', 'Belagerungs-Schlagkraft zu gering' in block['bericht'])
check('keine Truppen = kein Kampf', not kampf.fuehre_schlacht({}, {}, 0, rng=R())['kampf_stattgefunden'])
check('ohne Wall ist Mauer nicht beschaedigbar', kampf.fuehre_schlacht({'Krieger':2},{},0,
         angreifer_karren={'Katapult':2},rng=R())['mauer_zustand']==100)

abschnitt('C. Fernkampf, Erschoepfung, Forschung')
# 0.21: Kurzbogenschuetze ohne Bogenbau (20%) verfehlt; mit Stufe 1 (22%) trifft.
def test_pfeil(stufe):
    return kampf.fuehre_schlacht({'Kurzbogenschütze':1},{'Bürgerwehr':1}, 0,
        rng=Zufall(0.21), forschung_angreifer={'Bogenbau':stufe},forschung_verteidiger={})
kein=test_pfeil(0); mit=test_pfeil(1)
check('ohne Bogenbau ist Trefferchance 20%', '0 Treffer' in kein['bericht'].split('\n')[1])
check('Bogenbau Stufe 1 erhoeht auf 22%', '1 Treffer' in mit['bericht'].split('\n')[1])
check('Erschoepfung macht Buergerwehr kampfunfaehig', mit['verluste_verteidiger'].get('Bürgerwehr')==1)
check('Wallstufe bestimmt Vorrundenanzahl',len(kampf.fuehre_schlacht({'Paladin':100},{},2,rng=R())['sequenzen'])>=3)

abschnitt('D. Schlacht, Beute, Reproduzierbarkeit, Eingabeschutz')
a={'Krieger':4};v={'Bürgerwehr':2};kosten={'holz':90,'stein':30}
orig=(copy.deepcopy(a), copy.deepcopy(v), copy.deepcopy(kosten))
r1=kampf.fuehre_schlacht(a,v,0,angreifer_karren={'Handkarren':2},vorraete=kosten,rng=R())
r2=kampf.fuehre_schlacht(a,v,0,angreifer_karren={'Handkarren':2},vorraete=kosten,rng=R())
check('identischer Seed liefert identischen Schlachtbericht',r1==r2)
check('Eingabedaten unveraendert', (a,v,kosten)==orig)
check('Beute nur bei Angreifersieg', r1['ausgang']=='angreifer' or not r1['beute'])
check('Beute niemals hoeher als Lager und Karrenladung',
      sum(r1['beute'].values())<=80 and all(x<=kosten[k] for k,x in r1['beute'].items()))
check('keine Karren -> keine Beute', not kampf.fuehre_schlacht({'Krieger':10},{},0,
      vorraete={'holz':100},rng=R())['beute'])
check('Aufruf mit Geraeten in Angreiferliste ist erlaubt', isinstance(kampf.fuehre_schlacht(
      {'Krieger':2, 'Katapult':1}, {}, 0, rng=R())['bericht'],str))
check('Leere Beteiligte ohne Truppen duerfen keine Beute erzeugen',
      not kampf.fuehre_schlacht({}, {},0,angreifer_karren={'Handkarren':2},vorraete={'holz':100},rng=R())['beute'])
# 31.10.2026: Die alte Schlachtfassung (kampf_alt_handbuch_2009.py) wurde aus dem Spielcode
# entfernt - sie wurde von niemandem importiert (nur diese Pruefung hielt sie am Leben).
# Sie liegt als Beleg in archiv/alter_code/ und bleibt in der Git-Historie. Damit gilt:
# genau EINE Schlachtfunktion im Spiel.
check('nur eine Schlacht-Implementierung im Spielcode', not os.path.isfile(os.path.join(os.path.dirname(os.path.dirname(__file__)),'src','kampf_alt_handbuch_2009.py')))
check('Kampfmodell eindeutig gekennzeichnet', 'GPT-NE01.wissenswertes' in kampf.STAND)

abschnitt("Vorschlaege sind als solche gefuehrt (externe Gegenpruefung, Nr. 9/10/11)")
_v = kampf.vorschlaege()
check('kampf.vorschlaege() ist gefuellt', isinstance(_v, dict) and len(_v) >= 5, str(len(_v)))
check('jeder Eintrag nennt Wert, Grund, Status und Stelle',
      all(all(k in e for k in ('wert', 'grund', 'status', 'stelle')) for e in _v.values()),
      str([k for k, e in _v.items() if not all(x in e for x in ('wert', 'grund', 'status', 'stelle'))]))
check('der Mauermalus (erfundene Formel) ist als VORSCHLAG gefuehrt',
      _v.get('mauerabzug', {}).get('status') == 'VORSCHLAG')
check('der Turmschutz ist als VORSCHLAG gefuehrt',
      _v.get('turmschutz', {}).get('status') == 'VORSCHLAG')
check('die Rueckzug-Rundung ist als VORSCHLAG gefuehrt',
      _v.get('rueckzug_rundung', {}).get('status') == 'VORSCHLAG')
check('die Beutestaffelung ist als Abweichung (E4) gekennzeichnet',
      _v.get('beute_anteil', {}).get('status') == 'VORSCHLAG'
      and 'E4' in _v.get('beute_anteil', {}).get('grund', ''))
check('kein Eintrag behauptet, belegt zu sein',
      all(e.get('status') != 'BELEGT' for e in _v.values()))
sys.exit(bericht())
