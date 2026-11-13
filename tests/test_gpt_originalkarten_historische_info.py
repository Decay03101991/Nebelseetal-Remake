"""GPT-OK04: historische Karteninfos werden nie als Gratisrohstoffe verwendet.

Erstellt: ChatGPT, externer Entwicklungsagent, 28.10.2026.
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['originalkarten', 'spieldaten']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------
from pathlib import Path
from collections import Counter
from zipfile import ZipFile
from lxml import etree
import hashlib
import json
import sys

R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'tests'))            # harness liegt in tests/
sys.path.insert(0,str(R/'src'))
import _originalpfade as OP          # Register 407: Originale liegen ausserhalb des Repos
import originalkarten
import spieldaten
# F-80 (Daniel 13.11.2026): eigene Zaehlung durch `harness` ersetzt. Die F-74-Messung hatte diese
# Datei mit "0 Pruefungen" gefuehrt - das war ein Zaehlfehler des Messwerkzeugs: es sucht `check(`,
# `self.assert...` und `ok(`, hier heisst die Zusicherung aber `ck(`. Der Lauf zeigt 650 Pruefungen.
from harness import befund, bericht, check as _hcheck  # noqa: E402


def ck(a, label):
    return _hcheck(str(label), bool(a))

j=json.loads((R/'data/originalkarten/katalog.json').read_text('utf8'))
h=j['historischer_quellkontext']
ck(h['zahl_aller_karten_laut_forumzitierung']==154,'historische 154 sind eine Forumsaussage')
ck(h['zahl_in_der_historischen_kartothek_laut_vorwort']==125,'historische Kartothek 125')
ck(h['kategorien_laut_historischem_vorwort']=={'beste':35,'mittlere':42,'schlechte':48},'historische 35/42/48')
ck(j['zaehlungen']=={'gesamt_varianten':127,'verschiedene_originalnummern':125,'beste':35,'mittlere':43,'schlechte':49},'extrahierte 127: 35/43/49')
ck(h['berechnungsbedingungen']=='ohne Forschungsboni, normale Weltengeschwindigkeit','Produktionsbedingung aus Quelle')
ck(set(j['quellunterseiten'])=={'beste','mittlere','schlechte'},'Quellunterseiten je Gruppe')
ck(all(e['quelle']['quellunterseite']==j['quellunterseiten'][e['kategorie']] for e in j['karten']),'Quelle pro Karte')
ck(all(e['quelle']['quellunterseite_nachweis'].startswith('Links der Original') for e in j['karten']),'URL aus ODT, nicht Web-Verifikation')
ohne_odt=0
for docname in ('Karten_BesteKarten.odt','Karten_MittlereKarten.odt','Karten_SchlechteKarten.odt'):
 p=OP.finde('docs/original/karten_sammlung_odt/'+docname)
 if p is None:                        # Register 407: ODT liegt weder im Repo noch in der Ablage
  ohne_odt+=1
  continue
 ck(p.is_file(),f'Original ODT vorhanden {docname}')
 with ZipFile(p) as z:
  b=z.read('content.xml')
  root=etree.fromstring(b)
  links=set(root.xpath('//@*[local-name()="href"]'))
  ck(any('osnanet.de/kathrin-hildebrand/Siedlungskarten' in str(x) for x in links),'Hyperlink im Original')
 for e in j['karten']:
  if e['quelle']['dokument']==docname:
   ck(hashlib.sha256(p.read_bytes()).hexdigest()==e['quelle']['dokument_sha256'],'Quell-ODT-Hash')
# All 127 archived image files remain exactly preserved, including duplicate numbers.
ohne_bild=0
for e in j['karten']:
 img=OP.finde(e['originalbild'])
 if img is None:                      # Register 407: Originalbild liegt ausserhalb des Repos
  ohne_bild+=1
 else:
  ck(img.is_file() and hashlib.sha256(img.read_bytes()).hexdigest()==e['bild_sha256'],f"Bild {e['id']}")
 k=originalkarten.karte(e['id'])
 ck(k['originalkarte_id']==e['id'] and len(k['raster'])==100, f"10x10 {e['id']}")
 ck(k['originalkarte_quelle']==j['website'],'Website attribution stays attached')
 ck('gold' not in k.get('vorraete',{}) and 'leder' not in k.get('vorraete',{}),'Keine Gratisrohstoffe')
ck(Counter(x['original_nummer'] for x in j['karten'] if x['variante'])=={38:2,118:2},'Dublette bleiben zwei verschiedene Karten')
if ohne_odt: befund("Original-ODT fehlt (Register 407), gezaehlt: %d" % ohne_odt,
                    OP.fehlt_hinweis(ohne_odt))
if ohne_bild: befund("Originalbilder fehlen (Register 407), gezaehlt: %d" % ohne_bild,
                     OP.fehlt_hinweis(ohne_bild))
sys.exit(bericht())
