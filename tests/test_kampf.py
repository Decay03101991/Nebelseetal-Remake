"""Kampfkern nach neu gefundenem Originaldokument 'Das Kampfsystem.odt'.

Vorheriger, durch Quellenwechsel unzutreffender Test: 
  docs/archiv/test_kampf_handbuch_2009_vor_GPT_KA02.py
Werte/Detailtests: tests/test_gpt_kampf_forum_neu.py
"""
from __future__ import annotations
import sys,os,random
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt,bericht,check,import_src
import_src()
import kampf,einheiten,spieldaten

R=lambda:random.Random(141)
abschnitt('A. Original: Einheiten und Forschungsbonus')
check('Originalkonstitution Paladin 70%',kampf.PROFILE['Paladin'][0]==70)
check('Original-Schwelle Erschoepfung Krieger 5',kampf.PROFILE['Krieger'][-1]==5)
check('Bogenbau-Bonus stammt aus dem neuen Original: 2%/Stufe', '0.02 * _forschungsstufe' in open(kampf.__file__,encoding='utf8').read())
check('Schmiedekunst: 10%/Stufe', '0.10 * _forschungsstufe' in open(kampf.__file__,encoding='utf8').read())

abschnitt('B. Wallvorrunde und wirkliche Schlacht')
block=kampf.fuehre_schlacht({'Bürgerwehr':1},{'Paladin':4},5,rng=R())
check('Wall nicht ueberwunden -> keine Schlacht',block['vorrunde_bestanden'] is False and block['kampf_stattgefunden'] is False)
check('Wegen Wall niemand getoetet',not block['verluste_angreifer'] and not block['verluste_verteidiger'])
check('Wegen Wall keine Beute', not block['beute'])
normal=kampf.fuehre_schlacht({'Krieger':20},{'Bürgerwehr':2},1,rng=R())
check('Wall-SK ausreichend -> Schlacht',normal['vorrunde_bestanden'] and normal['kampf_stattgefunden'])
check('Ergebnis kommt aus Dreiklang Angreifer/Verteidiger/Unentschieden',normal['ausgang'] in ('angreifer','verteidiger','unentschieden'))
check('Fuer Wall Stufe1 genau zwei Fernkampf-Vorrunden', sum(z.startswith('Fernkampf-Vorrunde') for z in normal['sequenzen'])==2)

abschnitt('C. Schaden und Ressourcen')
wall=kampf.fuehre_schlacht({'Krieger':100},{},1,angreifer_karren={'Katapult':1},rng=R())
check('Mauerzustand faellt nie unter null',0<=wall['mauer_zustand']<=100)
check('Mauerschaden nicht durch fiktive neue Werte erzeugt',einheiten.mauer_schaden('Katapult')==(2,13))
check('Keine Karren -> Beute bleibt leer',not kampf.fuehre_schlacht({'Krieger':100},{},0,vorraete={'stein':100},rng=R())['beute'])
mit=kampf.fuehre_schlacht({'Krieger':100},{},0,angreifer_karren={'Handkarren':1},vorraete={'stein':100},rng=R())
check('Beute bei Sieg maximal 40 Handkarren-Ladung',0<=mit['beute'].get('stein',0)<=40)
check('Sieg ohne Verteidiger wirklich berechnet',mit['ausgang']=='angreifer')

sys.exit(bericht())
