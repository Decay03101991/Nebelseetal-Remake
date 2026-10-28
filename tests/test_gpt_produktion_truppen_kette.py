"""Unterbrechungsfreie Rezept-/Waren-/Truppen-Kette anhand Originaldaten auditiert."""
from __future__ import annotations
import sys,os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt,check,bericht,import_src
ROOT,SRC=import_src()
import einheiten,ausruestung,werkstatt,spieldaten,spieloekonomie

abschnitt('17 Waren: freigegebenes Rezept, Werkstatt, Preis und Voraussetzungen')
items=spieldaten.waren(); units=spieldaten.einheiten(); rez=spieloekonomie.WARENREZEPTE
check('17 Waren- und Rezeptnamen deckungsgleich', set(items)==set(rez))
for ware,info in items.items():
    wid=werkstatt.werkstatt_fuer(ware)
    check(f'{ware}: Werkstatt zugeordnet',wid is not None,repr(wid))
    preis=rez[ware].get('kosten')
    check(f'{ware}: Rezeptkosten nicht negativ',bool(preis) and all(isinstance(n,(int,float)) and n>=0 for n in preis.values()),repr(preis))
    check(f'{ware}: positive Fertigungsdauer',rez[ware].get('dauer',0)>0)

abschnitt('28 Einheiten: Ausbildungsstaette, Warenbedarf, lueckenlose Erzeugbarkeit')
for name,u in units.items():
    check(f'{name}: hat Ausbildungsgebaeude',u.get('gebaeude') in ('Kriegerakademie','Diebesgilde','Stellmacher'))
    wanted=u.get('waren') or []
    check(f'{name}: jede verlangte Ware existiert samt Rezept',all(w in items and w in rez for w in wanted))
    check(f'{name}: abgeleiteter Warenbedarf unveraendert',ausruestung.bedarf(name)==wanted)
    check(f'{name}: hat logisch lesbare Beschaffungskette',len(ausruestung.kette(name))>=1)

abschnitt('Handbuchbeispiele: Paladin und Handkarren')
p=units['Paladin']; k=units['Handkarren']
check('Paladin benoetigt drei exakt benannte Originalwaren',p['waren']==['Zweihänder','Schwert','Magischer Paladinharnisch'])
check('Paladin kostet 2000 Gold, 10 Mana, 1 Pferd, 1 Siedler',all(p['kosten'].get(r)==v for r,v in {'gold':2000,'mana':10,'pferde':1,'siedler':1}.items()))
check('Paladin Forschung Kriegskunst 10',p['voraussetzung']=={'forschung':'Kriegskunst','stufe':10})
check('Handkarren Originalkosten und Ladung',all(k['kosten'].get(r)==v for r,v in {'holz':100,'metall':15,'leder':15,'wolle':15,'siedler':1}.items()) and k['ladung']==40)
check('Handkarren wird im Stellmacher gebaut',k['gebaeude']=='Stellmacher')
check('Magischer Paladinharnisch braucht zwei Forschungen',rez['Magischer Paladinharnisch']['voraussetzungen']=={'Rüstungsbau':7,'Magiekunde':2})
check('Schwertdauer 1200 s ist der belegte Originalfall',rez['Schwert']['dauer']==1200)
sys.exit(bericht())
