"""GPT-OK01/02: Originalkarten-Katalog, Quellenbindung und echte Spielanbindung.
Ausfuehren: python -X utf8 tests/test_gpt_originalkarten_katalog.py
Autor: ChatGPT, externer Entwicklungsagent (28.10.2026).
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['originalkarten', 'spieloekonomie']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------
import hashlib
import json
import sys
from pathlib import Path
from collections import Counter

P=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(P/'tests'))            # harness liegt in tests/
sys.path.insert(0,str(P/'src'))
import _originalpfade as OP          # Register 407: Originale liegen ausserhalb des Repos
import originalkarten as O
import spieloekonomie as E
# F-80 (Daniel 13.11.2026): eigene Zaehlung durch `harness` ersetzt. `ok(bedingung, label)` bleibt
# als Name stehen, damit keine der 27 Pruefungen angefasst werden muss - gezaehlt wird jetzt von
# `harness` (Messwerte, Befundkanal, eine ERGEBNIS-Zeile).
from harness import befund, bericht, check as _hcheck  # noqa: E402


def ok(condition, label):
    return _hcheck(str(label), bool(condition))

quelle=O.alle()
ok(len(quelle)==127,'127 Originalgrafiken')
ok(len({x['original_nummer'] for x in quelle})==125,'125 eindeutige historische Nummern')
ok(len(O.alle('beste'))==35,'35 beste')
ok(len(O.alle('mittlere'))==43,'43 mittlere')
ok(len(O.alle('schlechte'))==49,'49 schlechte')
ok({x['original_nummer'] for x in quelle if x['variante']}=={38,118},'nur Dubletten 38 und 118')
ok(len(O.kennungen())==len(set(O.kennungen()))==127,'eindeutige Karten-IDs')
ohne_original=0
for info in quelle:
 id=info['id']
 bild=OP.finde(info['originalbild'])
 if bild is None:                     # Register 407: Original liegt weder im Repo noch in der Ablage
  ohne_original+=1
 else:
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
if ohne_original:
    befund("Originale fehlen (Register 407)", OP.fehlt_hinweis(ohne_original))
sys.exit(bericht())
