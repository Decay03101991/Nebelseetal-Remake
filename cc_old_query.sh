#!/bin/bash
# Query the oldest CC indexes in parallel for nebelseetal.de
cd /d/Arbeiten/Nebelseetal_Remake
IDX="CC-MAIN-2008-2009 CC-MAIN-2009-2010 CC-MAIN-2012 CC-MAIN-2013-20 CC-MAIN-2013-48 CC-MAIN-2014-10 CC-MAIN-2014-15 CC-MAIN-2014-23 CC-MAIN-2014-35 CC-MAIN-2014-41 CC-MAIN-2014-42 CC-MAIN-2014-49 CC-MAIN-2014-52"
for i in $IDX; do
  (
    url="https://index.commoncrawl.org/${i}-index?url=nebelseetal.de%2F*&output=json&limit=2000&matchType=domain"
    out=$(curl -sS -m 120 "$url" 2>&1)
    if echo "$out" | grep -q '"url"'; then
      echo "$out" | python -c "
import sys,json
idx='$i'
for l in sys.stdin:
    l=l.strip()
    if not l: continue
    try: r=json.loads(l)
    except: continue
    r['_index']=idx
    print(json.dumps(r,ensure_ascii=False))
" >> cc_old_hits.jsonl
      echo "$i: $(echo "$out" | grep -c '\"url\"') records" >> cc_old_log.txt
    else
      echo "$i: $(echo "$out" | head -c 120)" >> cc_old_log.txt
    fi
  ) &
done
wait
echo "OLD-DONE" >> cc_old_log.txt
