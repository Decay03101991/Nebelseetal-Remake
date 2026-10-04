import json, urllib.request, urllib.parse, os, time, socket

BASE = os.path.dirname(os.path.abspath(__file__))
coll = json.load(open(os.path.join(BASE, 'cc_collinfo.json')))
hitfile = os.path.join(BASE, 'cc_hits.jsonl')
statusfile = os.path.join(BASE, 'cc_status.tsv')

# load already-recorded results
status = {}
if os.path.exists(statusfile):
    for line in open(statusfile, encoding='utf-8'):
        p = line.rstrip('\n').split('\t')
        if len(p) >= 2:
            status[p[0]] = p[1]
# also count hits already present to avoid dupes
seen = set()
if os.path.exists(hitfile):
    for line in open(hitfile, encoding='utf-8'):
        try:
            r = json.loads(line)
            seen.add((r.get('_index'), r.get('url'), r.get('offset')))
        except Exception:
            pass

hf = open(hitfile, 'a', encoding='utf-8')
sf = open(statusfile, 'a', encoding='utf-8')
socket.setdefaulttimeout(60)

for c in coll:
    idx = c['id']
    if idx in status and status[idx] != 'RETRY':
        continue
    api = c['cdx-api']
    url = api + '?url=' + urllib.parse.quote('nebelseetal.de/*', safe='') + '&output=json&limit=2000&matchType=domain'
    data = None
    last = ''
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'cc-research/1.0'})
            with urllib.request.urlopen(req, timeout=90) as r:
                data = r.read().decode('utf-8', 'replace')
            break
        except urllib.error.HTTPError as e:
            last = 'HTTP%d' % e.code
            if e.code == 404:
                data = ''
                break
            time.sleep(min(3 * (attempt + 1), 20))
        except Exception as e:
            last = type(e).__name__
            time.sleep(min(3 * (attempt + 1), 20))
    if data is None:
        print(f'{idx}: FAILED ({last})', flush=True)
        sf.write(f'{idx}\tFAILED:{last}\n'); sf.flush()
        continue
    if 'No Captures' in data:
        print(f'{idx}: 0 records', flush=True)
        sf.write(f'{idx}\t0\n'); sf.flush()
        continue
    n = 0
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except Exception:
            continue
        rec['_index'] = idx
        key = (idx, rec.get('url'), rec.get('offset'))
        if key in seen:
            continue
        seen.add(key)
        hf.write(json.dumps(rec, ensure_ascii=False) + '\n')
        n += 1
    hf.flush()
    print(f'{idx}: {n} records', flush=True)
    sf.write(f'{idx}\t{n}\n'); sf.flush()
    time.sleep(1)

hf.close(); sf.close()
print('ALLDONE', flush=True)
