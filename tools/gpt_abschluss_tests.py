"""Dokumentierte GPT-Teilabnahme (kein Gesamttest, keine Releasefreigabe)."""
from pathlib import Path
import json,os,re,subprocess,sys,time
ROOT=Path(__file__).resolve().parent.parent
NAMES=[
 'test_gpt_portable_uebergabe.py','test_gpt_ne01_origwerte.py',
 'test_gpt_kampf_forum_neu.py','test_kampf_einhaengung.py',
 'test_gpt_wirtschaft_kette_e2e.py','test_gpt_grundproduktion_original.py',
 'test_gpt_produktion_truppen_kette.py','test_gpt_softlock_schutz.py',
 'test_gpt_originalkarten_katalog.py','test_gpt_originaltreue.py',
 'test_gpt_profile_login.py','test_gpt_speicherslots_admin.py',
 'test_gpt_adminwerkzeuge.py','test_gpt_rechnerzeit_einheitlich.py',
 'test_gpt_zeit_auftragsketten.py','test_gpt_wallsystem_eingehaengt.py',
 'test_gpt_bot_angriffsplanung.py','test_gpt_kampf_botbeute_echte_kasse.py',
 'test_gpt_waren_icons.py','test_gpt_versorgungsdiagnose.py',
 'test_gpt_prueflauf_ehrlich.py'
]

def main():
 rows=[]; begin=time.monotonic()
 for name in NAMES:
  file=ROOT/'tests'/name
  if not file.exists(): rows.append(dict(name=name,status='MISSING'));continue
  try:
   p=subprocess.run([sys.executable,str(file)],cwd=ROOT,capture_output=True,text=True,
      timeout=35,env={**os.environ,'PYTHONUTF8':'1'})
   out=p.stdout+'\n'+p.stderr
   match=re.findall(r'ERGEBNIS:\s*(\d+) bestanden,\s*(\d+) Fehler',out)
   unittest_match=re.findall(r'Ran (\d+) tests? in',out)
   error_markers=['Traceback (most recent call last)','  FEHLER ', 'FAILED (', 'FEHLER:', 'AssertionError']
   passed=int(match[-1][0]) if match else (int(unittest_match[-1]) if unittest_match else None)
   failed=int(match[-1][1]) if match else None
   good=p.returncode==0 and not any(mark in out for mark in error_markers) and (failed in (None,0))
   row=dict(name=name,status='PASS' if good else 'FAIL',passed=passed,failed=failed,returncode=p.returncode,tail=out[-750:])
  except subprocess.TimeoutExpired as e:
   row=dict(name=name,status='TIMEOUT',tail=str(e))
  rows.append(row)
  print(row['status'],name, 'checks:',row.get('passed'),flush=True)
 status={x:sum(r['status']==x for r in rows) for x in ('PASS','FAIL','TIMEOUT','MISSING')}
 data=dict(date='2026-10-28',author='ChatGPT – externer zeitweiliger Entwicklungsagent',environment=sys.platform,
           gui=bool(os.environ.get('DISPLAY')),scope='gezielt: kein umfassender Release-Test',
           duration_seconds=round(time.monotonic()-begin,1),totals=status,
           passed_assertions_known=sum(r.get('passed') or 0 for r in rows if r['status']=='PASS'),tests=rows,
           unresolved=['Windows-EXE nicht in Linux gebaut/getestet','8x7-Altannahmen in altem Oekonomie-Testsatz',
                       '25 Originalkarten mit offener optischer Rasterpruefung','Bot-Wirtschaft/kompletter Durchspieltest'])
 (ROOT/'docs/GPT_ABSCHLUSS_TESTERGEBNISSE.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('TOTAL',status,'ASSERTIONS',data['passed_assertions_known'],'DURATION',data['duration_seconds'],flush=True)
 return 0 if not (status['FAIL'] or status['TIMEOUT'] or status['MISSING']) else 1
if __name__=='__main__':sys.exit(main())
