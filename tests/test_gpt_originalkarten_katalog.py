"""GPT-OK01/02: Originalkarten-Katalog, Quellenbindung und echte Spielanbindung.
Ausfuehren: python -X utf8 tests/test_gpt_originalkarten_katalog.py
Autor: ChatGPT, externer Entwicklungsagent (28.10.2026).
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path
from collections import Counter

P=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(P/'src'))
import originalkarten as O
import spieloekonomie as E

checks=0

def ok(condition,label):
 global checks
 checks+=1
 if not condition: raise AssertionError(label)

quelle=O.alle()
ok(len(quelle)==127,'127 Originalgrafiken')
ok(len({x['original_nummer'] for x in quelle})==125,'125 eindeutige historische Nummern')
ok(len(O.alle('beste'))==35,'35 beste')
ok(len(O.alle('mittlere'))==43,'43 mittlere')
ok(len(O.alle('schlechte'))==49,'49 schlechte')
ok({x['original_nummer'] for x in quelle if x['variante']}=={38,118},'nur Dubletten 38 und 118')
ok(len(O.kennungen())==len(set(O.kennungen()))==127,'eindeutige Karten-IDs')
for info in quelle:
 id=info['id']
 bild=P/info['originalbild']
 ok(bild.is_file(),id+': Originalbild vorhanden')
 ok(hashlib.sha256(bild.read_bytes()).hexdigest()==info['bild_sha256'],id+': Originalbild unveraendert')
 m=O.karte(id)
 ok(m['spalten']==m['zeilen']==10,id+': 10x10')
 ok(len(m['raster'])==100,id+': hundert Spielzellen')
 ok(sum(m['zaehlung'].values())==100,id+': Zaehlung passend')
 ok(m['originalkarte_id']==id,id+': Herkunft im Spielzustand')
 ok(len(m['zeilen_raster'])==10 and all(len(row)==10 for row in m['zeilen_raster']),id+': 10 volle Zeilen')
 ok(m['bauplaetze']==100-m['zaehlung']['sumpf'],id+': nur Sumpf gesperrt')
 # Original values remain original: mismatches must NOT be silently overwritten.
 r=info['original_attribute']
 ok(len(r['felder'])==7 and all(type(v) is int and v>=0 for v in r['felder'].values()),id+': Quellenzahlen gespeichert')
 ok(info['quelle']['website']=='http://www.osnanet.de/kathrin-hildebrand/',id+': Herkunft')

v1=E.vorrat('pruefsaat');v2=E.vorrat('pruefsaat')
ok(len(v1)==126,'126 freie Originale plus private Spieler-Startkarte')
ok(v1==v2,'deterministischer Kartenvorrat')
ok('original-036' not in v1,'private Startkarte nicht doppelt')
start=E.startkarte('pruefsaat','spieler')
ok(start['originalkarte_id']=='original-036','Startkarte Das Z')
ok(start['zaehlung']['wald']>=2,'Startkarte mit Holz')
ok(start['zaehlung']['berg']+start['zaehlung']['huegel']>=2,'Startkarte mit Gestein')
ok(start['zaehlung']['grasland']>=2,'Startkarte mit Agrargrundlage')
ok(E.relativ(start)==(1.0,1.0,1.0),'Vergleichsbasis verwendet Original statt Altkarte')
ok(E.startkarte('a','spieler')['raster']==E.startkarte('b','spieler')['raster'],'Originalbildpositionen bleiben fest')
print(f'GPT-OK: {checks} Pruefungen bestanden; 0 Fehler')
