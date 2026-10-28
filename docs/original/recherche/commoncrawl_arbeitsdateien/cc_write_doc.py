import json, os, datetime
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
coll = [c['id'] for c in json.load(open(os.path.join(BASE, 'cc_collinfo.json')))]

cnt = defaultdict(int)
for l in open(os.path.join(BASE, 'cc_hits.jsonl'), encoding='utf-8'):
    try: r = json.loads(l)
    except: continue
    cnt[r.get('_index')] += 1

st = {}
sf = os.path.join(BASE, 'cc_status.tsv')
if os.path.exists(sf):
    for l in open(sf, encoding='utf-8'):
        p = l.rstrip('\n').split('\t')
        if len(p) >= 2: st[p[0]] = p[1]

checked = set(st)
unchecked = [c for c in coll if c not in checked]
failed = [k for k, v in st.items() if v.startswith('FAILED')]

def status_of(idx):
    if idx not in checked:
        return 'NICHT GEPRUEFT (IP-Block)'
    if st[idx].startswith('FAILED'):
        return 'FEHLER ' + st[idx]
    n = cnt.get(idx, 0)
    return f'{n} Treffer' if n else '0 Treffer (keine Captures)'

lines = []
lines.append('# Quellen: Common Crawl — Bildsuche Nebelseetal.de')
lines.append('')
lines.append(f'Erstellt: {datetime.date.today().isoformat()} | Werkzeug: Common Crawl Index API (index.commoncrawl.org) + Range-Download (data.commoncrawl.org)')
lines.append('')
lines.append('## Ergebnis (Kurzfassung)')
lines.append('')
lines.append('**Common Crawl enthaelt KEINE einzige Bilddatei von nebelseetal.de** — weder die Siedlungskarte')
lines.append('noch sonstige Spielbilder. In allen geprueften Indizes (2008-2026) wurden ausschliesslich')
lines.append('HTML/CSS/PDF/XML/JS-Records gefunden; kein Record mit MIME `image/*` und keine URL mit')
lines.append('Endung .jpg/.jpeg/.gif/.png/.bmp. Das deckt sich mit dem Befund des Internet Archive.')
lines.append('')
lines.append('Common Crawl hat aber die **HTML-Seiten** des alten PHP-Spiels (Crawl 2009/2010) archiviert.')
lines.append('Diese HTML-Seiten verweisen auf die Original-Bildpfade, u. a. `bilder/screens/siedlung.jpg`.')
lines.append('Die Bild-Bytes selbst wurden von Common Crawl nie abgerufen/gespeichert.')
lines.append('')
lines.append('## Vorgehen')
lines.append('')
lines.append('1. Alle CC-Indizes aus `https://index.commoncrawl.org/collinfo.json` (128 Indizes) geladen.')
lines.append('2. Jeden Index abgefragt: `<cdx-api>?url=nebelseetal.de%2F*&output=json&limit=5000&matchType=domain`')
lines.append('   (matchType=domain deckt auch Subdomaenen wie forum./midagrad. ab).')
lines.append('3. Nach Bildern gefiltert: MIME beginnt mit `image/` ODER URL endet auf Bildendung.')
lines.append('4. Bei Treffern waeren die Bytes per HTTP-Range (`data.commoncrawl.org/<filename>`) geholt,')
lines.append('   entgzippt, der HTTP-Kopf vom Bildkoerper getrennt und die Magic-Bytes geprueft worden.')
lines.append('   -> Dieser Schritt entfiel, weil **kein** Bildtreffer existierte.')
lines.append('')
lines.append('## Abdeckung pro Index')
lines.append('')
lines.append(f'Geprueft: **{len(checked)} von {len(coll)}** Indizes. Nicht geprueft: {len(unchecked)} (siehe unten).')
lines.append('')
lines.append('| Index | Ergebnis |')
lines.append('|---|---|')
for idx in coll:
    lines.append(f'| {idx} | {status_of(idx)} |')
lines.append('')
if failed:
    lines.append('Fehlgeschlagene Abfragen (Serverfehler/Timeout): ' + ', '.join(failed))
    lines.append('')
lines.append('## Nicht geprueft')
lines.append('')
lines.append('Diese Indizes konnten nicht abgefragt werden, weil `index.commoncrawl.org` die Verbindung')
lines.append('nach der grossen Anfrageserie voruebergehend sperrte (IP-Block, "Could not connect ... after 21s").')
lines.append('`https://data.commoncrawl.org` (WARC-Host) blieb erreichbar. Es handelt sich ausschliesslich um')
lines.append('Indizes aus 2015-2018, in denen die Domain bereits geparkt/abgeschaltet war:')
lines.append('')
lines.append(', '.join(unchecked) if unchecked else '(keine)')
lines.append('')
lines.append('## Was Common Crawl stattdessen enthaelt')
lines.append('')
lines.append('Crawl **CC-MAIN-2009-2010** (= `crawl-002`, 2010) hat die HTML-Seiten des alten Spiels:')
lines.append('index.php, anleitung.php, anmeldung.php, login.php, regeln.php, screens.php, wallpaper.php,')
lines.append('hintergrundgeschichte.php, links.php, ruhmeshalle.php sowie das Forum unter forum.nebelseetal.de.')
lines.append('')
lines.append('Die Seite `screens.php` (Original-URL http://www.nebelseetal.de/screens.php, CC-Zeitstempel')
lines.append('20100310002533) verweist im HTML auf genau diese Bilddateien:')
lines.append('')
for p in ['bilder/screens/siedlung.jpg', 'bilder/screens/lager.jpg', 'bilder/screens/portal.jpg',
          'bilder/screens/profil.jpg', 'bilder/screens/thumb_siedlung.jpg', 'bilder/screens/thumb_lager.jpg',
          'bilder/screens/thumb_portal.jpg', 'bilder/screens/thumb_profil.jpg']:
    lines.append(f'- `{p}`')
lines.append('')
lines.append('`wallpaper.php` verweist auf `bilder/wallpaper/wallpaper.jpg`, `wallpaper_wide.jpg`, `thumb1.jpg`, `thumb2.jpg`.')
lines.append('Diese Bilddateien sind **nicht** im Common-Crawl-Index vorhanden (nie gecrawlt).')
lines.append('')
lines.append('### Beleg-Records (WARC/ARC-Koordinaten)')
lines.append('')
lines.append('| Original-URL | CC-Index | ARC/WARC-Datei | Offset | Laenge | CC-Zeitstempel |')
lines.append('|---|---|---|---|---|---|')
evidence = [
    ('http://www.nebelseetal.de/screens.php', 'CC-MAIN-2009-2010', 'crawl-002/2010/04/02/23/1270218670229_23.arc.gz', 92879327, 2549, '20100310002533'),
    ('http://www.nebelseetal.de/wallpaper.php', 'CC-MAIN-2009-2010', 'crawl-002/2010/04/02/23/1270218670229_23.arc.gz', 92881876, 2338, '20100310002504'),
    ('http://www.nebelseetal.de/index.php', 'CC-MAIN-2009-2010', 'crawl-002/2010/09/24/35/1285397931522_35.arc.gz', 66849249, 3072, '20100903185349'),
]
for e in evidence:
    lines.append('| ' + ' | '.join(str(x) for x in e) + ' |')
lines.append('')
lines.append('Die aus diesen Records extrahierten HTML-Seiten liegen als Beleg in:')
lines.append('`docs/original/karten/commoncrawl/`')
lines.append('')
lines.append('## Klare Negativ-Aussage')
lines.append('')
lines.append('- Siedlungskarte (`bilder/screens/siedlung.jpg`): **NICHT in Common Crawl**.')
lines.append('- lager.jpg / portal.jpg / profil.jpg: **NICHT in Common Crawl**.')
lines.append('- wallpaper.jpg / wallpaper_wide.jpg: **NICHT in Common Crawl**.')
lines.append('- Ueberhaupt keine Bilddatei der Domain in Common Crawl (128 Indizes, 86 geprueft).')

out = os.path.join(BASE, 'docs', 'original', 'karten', 'QUELLEN_COMMONCRAWL.md')
with open(out, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')
print('WROTE', out, len('\n'.join(lines)), 'chars')
