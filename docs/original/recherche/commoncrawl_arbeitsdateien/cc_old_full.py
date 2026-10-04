import json, urllib.request, urllib.parse, os, time, socket

BASE = os.path.dirname(os.path.abspath(__file__))
socket.setdefaulttimeout(120)
OLD = ["CC-MAIN-2008-2009","CC-MAIN-2009-2010","CC-MAIN-2012","CC-MAIN-2013-20","CC-MAIN-2013-48",
       "CC-MAIN-2014-10","CC-MAIN-2014-15","CC-MAIN-2014-23","CC-MAIN-2014-35","CC-MAIN-2014-41",
       "CC-MAIN-2014-42","CC-MAIN-2014-49","CC-MAIN-2014-52"]
outfile = os.path.join(BASE, 'cc_old_full.jsonl')
logfile = os.path.join(BASE, 'cc_old_full.log')
of = open(outfile, 'a', encoding='utf-8')
lf = open(logfile, 'a', encoding='utf-8')

def fetch(url):
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={'User-Agent':'cc-research/1.0'})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read().decode('utf-8','replace')
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return ''
            time.sleep(5*(attempt+1))
        except Exception:
            time.sleep(5*(attempt+1))
    return None

for idx in OLD:
    api = f'https://index.commoncrawl.org/{idx}-index'
    url = api + '?url=' + urllib.parse.quote('nebelseetal.de/*', safe='') + '&output=json&limit=5000&matchType=domain'
    data = fetch(url)
    if data is None:
        msg = f'{idx}: FAILED'; print(msg, flush=True); lf.write(msg+'\n'); lf.flush(); continue
    if not data.strip():
        msg = f'{idx}: 0 captures'; print(msg, flush=True); lf.write(msg+'\n'); lf.flush(); continue
    n=0; imgs=0
    for line in data.splitlines():
        line=line.strip()
        if not line: continue
        try: rec=json.loads(line)
        except: continue
        rec['_index']=idx
        of.write(json.dumps(rec,ensure_ascii=False)+'\n'); n+=1
        m=rec.get('mime','') or ''; u=rec.get('url','')
        if m.startswith('image/') or u.lower().endswith(('.jpg','.jpeg','.gif','.png','.bmp','.svg')):
            imgs+=1
    of.flush()
    msg=f'{idx}: {n} records, {imgs} image-like'
    print(msg, flush=True); lf.write(msg+'\n'); lf.flush()
    time.sleep(3)
of.close(); lf.close()
print('OLDFULLDONE', flush=True)
