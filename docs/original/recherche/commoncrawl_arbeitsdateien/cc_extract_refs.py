import json, os, gzip, io, re, urllib.request, socket, time

BASE = os.path.dirname(os.path.abspath(__file__))
socket.setdefaulttimeout(90)
os.makedirs(os.path.join(BASE, 'docs', 'original', 'karten', 'commoncrawl'), exist_ok=True)

recs = []
for l in open(os.path.join(BASE, 'cc_hits.jsonl'), encoding='utf-8'):
    try: r = json.loads(l)
    except: continue
    u = r.get('url', '')
    if r.get('_index') == 'CC-MAIN-2009-2010' and r.get('mime') == 'text/html' and \
       any(u.endswith(p) for p in ['index.php', 'screens.php', 'wallpaper.php', 'anleitung.php', 'regeln.php', '/']):
        recs.append(r)

def get_range(filename, offset, length):
    url = 'https://data.commoncrawl.org/' + filename
    req = urllib.request.Request(url, headers={'Range': f'bytes={offset}-{offset+length-1}', 'User-Agent': 'cc-research/1.0'})
    with urllib.request.urlopen(req, timeout=90) as resp:
        return resp.read()

def decode(raw):
    try:
        return gzip.GzipFile(fileobj=io.BytesIO(raw)).read()
    except Exception:
        return raw

allimgs = {}
for r in recs:
    try:
        raw = get_range(r['filename'], int(r['offset']), int(r['length']))
    except Exception as e:
        print('DL FAIL', r['url'], e); continue
    data = decode(raw)
    # ARC record: first line header, then HTTP response
    if data.startswith(b'<'):
        body = data
    else:
        nl = data.find(b'\n')
        body = data[nl+1:]
    txt = body.decode('latin-1', 'replace')
    imgs = re.findall(r'(?i)(?:src|href)\s*=\s*["\']([^"\']+\.(?:jpg|jpeg|gif|png|bmp))["\']', txt)
    allimgs[r['url']] = imgs
    print(r['url'], '->', len(imgs), 'img refs')
    time.sleep(1)

print('\n=== IMAGE PATHS REFERENCED (from CC HTML) ===')
for u, imgs in allimgs.items():
    for i in sorted(set(imgs)):
        print(f'{i}\t(from {u})')
