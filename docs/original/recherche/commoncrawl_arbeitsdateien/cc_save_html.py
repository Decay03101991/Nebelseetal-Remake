import json, os, gzip, io, re, urllib.request, socket

BASE = os.path.dirname(os.path.abspath(__file__))
socket.setdefaulttimeout(90)
OUT = os.path.join(BASE, 'docs', 'original', 'karten', 'commoncrawl')
os.makedirs(OUT, exist_ok=True)

targets = []
for l in open(os.path.join(BASE, 'cc_hits.jsonl'), encoding='utf-8'):
    try: r = json.loads(l)
    except: continue
    if r.get('_index') == 'CC-MAIN-2009-2010' and r.get('mime') == 'text/html':
        u = r.get('url', '')
        if u.endswith(('screens.php', 'wallpaper.php', 'index.php')):
            targets.append(r)

def decode(raw):
    try: return gzip.GzipFile(fileobj=io.BytesIO(raw)).read()
    except Exception: return raw

saved = []
for r in targets:
    fn = r['filename']; off = int(r['offset']); ln = int(r['length'])
    req = urllib.request.Request('https://data.commoncrawl.org/' + fn,
                                 headers={'Range': f'bytes={off}-{off+ln-1}', 'User-Agent': 'cc-research/1.0'})
    with urllib.request.urlopen(req, timeout=90) as resp:
        raw = resp.read()
    data = decode(raw)
    if not data.startswith(b'<'):
        nl = data.find(b'\n'); body = data[nl+1:]
    else:
        body = data
    host = r['url'].split('//', 1)[-1].split('/', 1)[0]
    name = 'cc_2009_CRAWL_CC-MAIN-2009-2010_' + host + '_' + r['url'].rstrip('/').rsplit('/', 1)[-1] + '.html'
    path = os.path.join(OUT, name)
    with open(path, 'wb') as f:
        f.write(body)
    saved.append((name, len(body), fn, off, ln, r['url'], r.get('timestamp')))

for s in saved:
    print(s)
print('SAVED', len(saved))
