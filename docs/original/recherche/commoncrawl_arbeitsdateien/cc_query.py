import json, urllib.request, urllib.parse, os, sys, time

BASE = os.path.dirname(os.path.abspath(__file__))
coll = json.load(open(os.path.join(BASE, 'cc_collinfo.json')))
hitfile = os.path.join(BASE, 'cc_hits.jsonl')
donefile = os.path.join(BASE, 'cc_done.txt')

done = set()
if os.path.exists(donefile):
    done = set(l.strip() for l in open(donefile) if l.strip())

hf = open(hitfile, 'a', encoding='utf-8')
df = open(donefile, 'a', encoding='utf-8')

for c in coll:
    api = c['cdx-api']
    idx = c['id']
    if idx in done:
        continue
    url = api + '?url=' + urllib.parse.quote('nebelseetal.de/*', safe='') + '&output=json&limit=2000&matchType=domain'
    tried = 0
    ok = False
    while tried < 3 and not ok:
        tried += 1
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'cc-research/1.0'})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read().decode('utf-8', 'replace')
            ok = True
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', 'replace')
            if e.code == 404:
                print(f'{idx}: no captures', flush=True)
                ok = True
                data = ''
            else:
                print(f'{idx}: HTTP {e.code} {body[:120]}', flush=True)
                time.sleep(2)
                continue
        except Exception as e:
            print(f'{idx}: ERR {e}', flush=True)
            time.sleep(2)
            continue
    if not ok:
        print(f'{idx}: FAILED after retries', flush=True)
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
        hf.write(json.dumps(rec, ensure_ascii=False) + '\n')
        n += 1
    hf.flush()
    df.write(idx + '\n')
    df.flush()
    print(f'{idx}: {n} records', flush=True)

hf.close()
df.close()
print('DONE', flush=True)
