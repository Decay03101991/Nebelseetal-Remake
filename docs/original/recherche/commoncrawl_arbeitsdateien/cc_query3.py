import json, urllib.request, urllib.parse, os, time, socket
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = os.path.dirname(os.path.abspath(__file__))
socket.setdefaulttimeout(90)
coll = json.load(open(os.path.join(BASE, 'cc_collinfo.json')))
hitfile = os.path.join(BASE, 'cc_hits.jsonl')
statusfile = os.path.join(BASE, 'cc_status.tsv')
lock_file = os.path.join(BASE, 'cc_lock.tmp')

status = {}
if os.path.exists(statusfile):
    for line in open(statusfile, encoding='utf-8'):
        p = line.rstrip('\n').split('\t')
        if len(p) >= 2:
            status[p[0]] = p[1]
seen = set()
if os.path.exists(hitfile):
    for line in open(hitfile, encoding='utf-8'):
        try:
            r = json.loads(line); seen.add((r.get('_index'), r.get('url'), r.get('offset')))
        except: pass

todo = [c for c in coll if c['id'] not in status or status[c['id']] == 'RETRY']
print('todo:', len(todo), flush=True)

hf = open(hitfile, 'a', encoding='utf-8')
sf = open(statusfile, 'a', encoding='utf-8')

def fetch(idx, api):
    url = api + '?url=' + urllib.parse.quote('nebelseetal.de/*', safe='') + '&output=json&limit=5000&matchType=domain'
    last = ''
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'cc-research/1.0'})
            with urllib.request.urlopen(req, timeout=90) as r:
                return idx, r.read().decode('utf-8', 'replace')
        except urllib.error.HTTPError as e:
            last = 'HTTP%d' % e.code
            if e.code == 404:
                return idx, ''
            time.sleep(4 * (attempt + 1))
        except Exception as e:
            last = type(e).__name__
            time.sleep(4 * (attempt + 1))
    return idx, None

with ThreadPoolExecutor(max_workers=3) as ex:
    futs = {ex.submit(fetch, c['id'], c['cdx-api']): c['id'] for c in todo}
    for fut in as_completed(futs):
        idx, data = fut.result()
        if data is None:
            print(f'{idx}: FAILED', flush=True)
            sf.write(f'{idx}\tFAILED\n'); sf.flush(); continue
        if not data.strip() or 'No Captures' in data:
            print(f'{idx}: 0 records', flush=True)
            sf.write(f'{idx}\t0\n'); sf.flush(); continue
        n = 0
        for line in data.splitlines():
            line = line.strip()
            if not line: continue
            try: rec = json.loads(line)
            except: continue
            rec['_index'] = idx
            key = (idx, rec.get('url'), rec.get('offset'))
            if key in seen: continue
            seen.add(key)
            hf.write(json.dumps(rec, ensure_ascii=False) + '\n'); n += 1
        hf.flush()
        print(f'{idx}: {n} records', flush=True)
        sf.write(f'{idx}\t{n}\n'); sf.flush()

hf.close(); sf.close()
print('ALLDONE', flush=True)
