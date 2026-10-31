"""GPT-NE01/02: Neu gefundene Originalwerte und Forschungs-Ausnahmen."""
from __future__ import annotations
import os,sys,random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src
import_src()
import kampf, wirtschaft as W, gelaende as G, gildenrangliste_original as GR, einheiten as E

abschnitt('A. Neue Originalprofile, Quelle Wissenswertes S. 5-6')
profile={
    'Kämpfer': (4,22), 'Krieger': (7,29), 'Ritter': (9,43),
    'Paladin': (17,57), 'Kundschafter': (4,37),
    'Waldläufer': (6,44), 'Armbrustschütze': (3,14),
}
for name,wert in profile.items():
    check(f'{name}: neue Kampfwert-Spanne {wert}',kampf.PROFILE[name][1:3] == wert)
check('15 Kampfprofile vollständig',len(kampf.PROFILE)==15)
check('Modellversion dokumentiert', 'GPT-NE01' in kampf.STAND)

abschnitt('B. Originalerträge (Tempel aus Handbuch 2009 = 5/1, Entscheidung 31.10.2026; uebrige aus Wissenswertes S. 4)')
for geb,art,soll in [('tempel','nebelsee',5),('tempel','wald',1),('tempel','grasland',1),
                      ('rinderfarm','grasland',{'Nahrung':1,'Leder':3}),
                      ('rinderfarm','steppe',{'Nahrung':0.5,'Leder':1.5})]:
    check(f'{geb}/{art}: {soll}', G.ertrag_pro_stunde(geb,art)==soll)

abschnitt('C. Gemischte Gebäude und Bonus-Abgrenzungen')
karte={'raster':['wald','wald','grasland','grasland','steppe','berg','nebelsee'],
       'spalten':7,'zeilen':1}
class Dorf:
    def __init__(self,bauten): self.karte=karte;self.bauten=bauten
levels={'Felderwirtschaft':3,'Tierhaltung':4,'Forstwirtschaft':2,'Götterkunde':1}
for bau,food,leather in [('jaeger',2,2),('rinderfarm',1,3)]:
    i=0 if bau=='jaeger' else 2
    e=W.ertrag_gesamt([Dorf({str(i):bau})],levels)
    check(f'{bau}: Nahrung ohne Forschungsbonus',e.get('Nahrung')==food,str(e))
    check(f'{bau}: Leder-Faktor nur für Rinderfarm', e.get('Leder')==round((leather if bau=='jaeger' else leather*1.2),2),str(e))
for geb,art_idx,raw,plus in [('farm',2,4,5.2),('holzfaeller',0,4,4.8)]:
    e=W.ertrag_gesamt([Dorf({str(art_idx):geb})],levels)
    roh='Nahrung' if geb=='farm' else 'Holz'
    check(f'{geb} ohne Forschung {raw}',W.siedlung_ertrag(Dorf({str(art_idx):geb}))[roh]==raw)
    check(f'{geb} mit Forschung {plus}',e[roh]==round(plus,2),str(e))
# Eine gemischte Siedlung enthaelt Jäger + Farm; nur Farm wird gebonust.
e=W.ertrag_gesamt([Dorf({'0':'jaeger','2':'farm','3':'rinderfarm','6':'tempel'})],levels)
check('gemischte Nahrung 2 + 5.2 + 1 (nicht alles auf einmal mal 1.3)',e.get('Nahrung')==8.2,str(e))
check('gemischtes Leder 2 + 3*1.2',e.get('Leder')==5.6,str(e))
check('Tempel 5 * 1.05 (Handbuch 2009; 8/2 war die aeltere Forum-Fassung, Entscheidung 31.10.2026)',e.get('Mana')==5.25,str(e))
check('Aufruf ohne Forschung unverändert', W.siedlung_ertrag(Dorf({'0':'jaeger'}))['Nahrung']==2)

abschnitt('D. Historische Rangliste vom 31.08.2011')
for name,gesamt,durchschnitt,erwartet in [
    ('Kohorte des Himmels',77845,12974,'45409.5'),
    ('Preußisches Restreich',58120,14530,'36325'),
    ('Imperiale Restwelten',26358,8786,'17572'),
]:
    check(name, GR.gildenwertung(gesamt,durchschnitt)==GR.Decimal(erwartet))
check('Rang nach Punktwert', [x['name'] for x in GR.gildenrangliste([
  {'name':'B','gesamt':100,'durchschnitt':50,'mitglieder':2},
  {'name':'A','gesamt':500,'durchschnitt':200,'mitglieder':3}])]==['A','B'])
for invalid in (-1, float('nan'), float('inf')):
    try: GR.gildenwertung(invalid,3)
    except ValueError: check(f'ungültige Wertung {invalid} verworfen',True)
    else: check(f'ungültige Wertung {invalid} verworfen',False)
check('Gilde ohne Mitglieder nicht automatisch positiv bewertet',GR.gildenrangliste([
    {'name':'leer','gesamt':999,'durchschnitt':999,'mitglieder':0}])[0]['wertung']==0)
abschnitt('E. 28 Original-Einheiten: Transport-GS und Mauer-SK bleiben konsistent')
werte={
'Bürgerwehr':(5,1),'Kämpfer':(10,2),'Krieger':(25,3),'Ritter':(20,4),'Paladin':(20,5),
'Streuner':(10,2),'Gauner':(15,3),'Dieb':(20,5),'Meisterdieb':(25,7),
'Kundschafter':(30,9),'Waldläufer':(35,11),
'Kurzbogenschütze':(5,1),'Bogenschütze':(5,2),'Langbogenschütze':(5,4),'Armbrustschütze':(5,5),
'Belagerungsturm':(15,35),'Ramme':(15,25),'Großer Belagerungsturm':(15,45),
'Große Ramme':(15,35),'Balliste':(15,25),'Katapult':(15,45),'Großes Katapult':(15,55),
'Handkarren':(10,0),'Einspänner':(25,0),'Zweispänner':(30,0),
'Handelskarawane':(25,0),'Große Handelskarawane':(30,0),'Siedlerkarren':(20,0)}
check('Tabelle enthält genau 28 gelistete Einheitentypen',len(werte)==28)
for name,(geschwindigkeit,sk) in werte.items():
    check(f'{name}: GS {geschwindigkeit}, SK {sk}',
          E.geschwindigkeit(name)==geschwindigkeit and E.schlagkraft(name)==sk)
sys.exit(bericht())
