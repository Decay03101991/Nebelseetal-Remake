"""Generiert die 640x640-Kartenbilder aus der archivierten historischen Originalgrafik.
Abhaengigkeit nur fuer dieses Werkzeug: Pillow. Der Windows-Spielstart braucht kein Pillow.
Aufruf: py -m pip install Pillow, dann py tools\originalkarten_grafiken_bauen.py
"""
from pathlib import Path
import json, hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent
CAT=json.loads((ROOT/'data/originalkarten/katalog.json').read_text('utf8'))
OUT=ROOT/'assets/karten/spielfeld';OUT.mkdir(parents=True,exist_ok=True)
entries=[]
for c in CAT['karten']:
 src=ROOT/c['originalbild']
 if hashlib.sha256(src.read_bytes()).hexdigest()!=c['bild_sha256']:
  raise RuntimeError('Quellgrafik geaendert: '+str(src))
 with Image.open(src) as img:
  img.convert('RGB').resize((640,640),Image.Resampling.NEAREST).save(OUT/(c['id']+'.png'),compress_level=1)
 dst=OUT/(c['id']+'.png')
 entries.append({'id':c['id'],'datei':dst.relative_to(ROOT).as_posix(),'originalbild':c['originalbild'],
                 'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'source_sha256':c['bild_sha256'],
                 'sichtpruefung_ausstehend':bool(c['raster_nachweis']['manuelle_sichtpruefung_ausstehend'])})
manifest={'version':1,'stand':'2026-10-28','pixelgroesse':[640,640],'raster':[10,10],
          'darstellung':'Originalbilder NEAREST ohne neue Terrain-Interpretation','karten':entries}
(ROOT/'data/originalkarten/grafik_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),'utf8')
print('Originalkarten-Bilder gebaut:',len(entries))
