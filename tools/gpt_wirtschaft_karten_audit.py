"""Wirtschaftspotenzial der 127 Originalkarten, ohne historische Gueteklasse als Bonus.

Nur lesend. Ohne Forschung, auf Grundlage der im Spiel verwendeten Raster.
Die theoretische Kapazitaet fuer EINEN Rohstoff darf nicht gleichzeitig
mit allen anderen Kapazitaeten addiert werden: ein Feld traegt nur EIN Gebaeude.

Aufruf: python -X utf8 tools/gpt_wirtschaft_karten_audit.py --ausgabe <ordner>
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import originalkarten
import wirtschaft

ROH=('Holz','Stein','Metall','Mana','Nahrung','Gold','Wolle','Leder','Pferde')

def pruefen():
    zeilen=[]
    for eintrag in originalkarten.alle():
        k=originalkarten.karte(eintrag['id'])
        grund=wirtschaft.ertrag_gesamt([{'karte':k,'bauten':{}}])
        potential=wirtschaft.kapazitaet({'karte':k})
        if set(grund)!={'Holz','Stein'} or grund['Holz']!=1 or grund['Stein']!=1:
            raise AssertionError('Historische Grundrate verletzt: '+eintrag['id'])
        z={'id':eintrag['id'],'name':eintrag['name'],
           'historische_gruppe_nur_metadaten':eintrag['kategorie'],
           'anzahl_felder':len(k['raster']), 'bebaubar':k['bauplaetze'],
           'originalbild_unsicher':k.get('originalkarte_pruefung_offen',False),
           'grund_holz_h':grund['Holz'],'grund_stein_h':grund['Stein']}
        for r in ROH:
            z['theoretisch_'+r.lower()+'_h']=potential.get(r,0)
        z['ohne_eigenen_goldstandort']=potential.get('Gold',0)==0
        z['ohne_eigenen_metallstandort']=potential.get('Metall',0)==0
        z['ohne_eigene_nahrungsproduktion']=potential.get('Nahrung',0)==0
        zeilen.append(z)
    if len(zeilen)!=127 or len(set(x['id'] for x in zeilen))!=127:
        raise AssertionError('Originalkatalog nicht vollstaendig')
    uebersicht={'karten':len(zeilen),
                'bei_gold_nur_import_oder_trade':sum(x['ohne_eigenen_goldstandort'] for x in zeilen),
                'bei_metall_nur_import_oder_trade':sum(x['ohne_eigenen_metallstandort'] for x in zeilen),
                'bei_nahrung_nur_import_oder_trade':sum(x['ohne_eigene_nahrungsproduktion'] for x in zeilen),
                'sichtpruefung_offen':sum(x['originalbild_unsicher'] for x in zeilen),
                'hinweis':'Pro Ressource unabhaengige obere Schranke: nicht gleichzeitig realisierbar; Kategorien reine Metadaten.'}
    return zeilen, uebersicht

def speichern(ordner):
    liste,bericht=pruefen()
    p=Path(ordner);p.mkdir(parents=True,exist_ok=True)
    with (p/'ORIGINALKARTEN_WIRTSCHAFTSPOTENZIAL.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=list(liste[0]))
        writer.writeheader();writer.writerows(liste)
    (p/'ORIGINALKARTEN_WIRTSCHAFTSAUDIT.json').write_text(
        json.dumps(bericht,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return bericht

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--ausgabe',required=True)
    z=a.parse_args()
    print(json.dumps(speichern(z.ausgabe),ensure_ascii=False,indent=2))
