"""GPT-ABS01: Portable Windows-Testkopie / Startpfade / Hermes-Protokoll."""
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

R = Path(__file__).resolve().parent.parent

class Portability(unittest.TestCase):
    def test_layout(self):
        for f in ('src/main.py','data/gelaende.json','assets/icons/nebelseetal.ico',
                  'docs/ENTWICKLUNGSPROTOKOLL.md','START_SPIEL_WINDOWS.bat',
                  'EXE_ERSTELLEN_WINDOWS.bat','tools/build_exe.py'):
            self.assertTrue((R/f).exists(),f)
    def test_external_cwd_asset_resolution(self):
        code = ('import sys;sys.path.insert(0,sys.argv[1]);import spieldaten;'
                'assert spieldaten.projektwurzel()==sys.argv[2]')
        with tempfile.TemporaryDirectory() as wd:
            p=subprocess.run([sys.executable,'-c',code,str(R/'src'),str(R)],cwd=wd,
                             capture_output=True,text=True,timeout=20)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
    def test_backup_default_outside_project(self):
        spec=importlib.util.spec_from_file_location('pruefung_sicherung',R/'tools/protokoll_sichern.py')
        m=importlib.util.module_from_spec(spec)
        old=os.environ.pop('NEBEL_PROTOKOLL_ZIEL',None)
        try: spec.loader.exec_module(m)
        finally:
            if old is not None: os.environ['NEBEL_PROTOKOLL_ZIEL']=old
        self.assertEqual(m.STANDARD_ZIEL,R.parent/'Nebelseetal_Remake_Protokoll')
        self.assertNotEqual(m.STANDARD_ZIEL,R)
        self.assertFalse(m.STANDARD_ZIEL.is_relative_to(R))
    def test_getrennte_test_speicherpfade_ohne_grundpasswort_aenderung(self):
        spec=importlib.util.spec_from_file_location('nebelseetal_main',R/'src/main.py')
        sys.path.insert(0,str(R/'src'))
        import main,tor
        with tempfile.TemporaryDirectory() as t:
            testpfad=str(Path(t)/'testwelt')
            from unittest.mock import patch
            with patch.dict(os.environ,{'NEBEL_SPIELDATEN_ORDNER':testpfad}):
                self.assertEqual(main.schreibordner(),testpfad)
                self.assertTrue(Path(testpfad).exists())
                self.assertNotEqual(main.schreibordner(),tor.ORDNER)
                self.assertEqual(tor.STANDARD_PFAD,str(Path(tor.ORDNER)/'tor.json'))
    def test_exe_ist_keine_quellcode_testfreigabe(self):
        # FIX04j: Die Entwickler-EXE darf inzwischen im Hauptordner stehen.
        # Weder ihre Anwesenheit noch ihr Alter beweisen aktuelle Codegleichheit.
        exe_namen = {f.name for f in R.glob('*.exe')}
        self.assertFalse(exe_namen - {'Nebelseetal_Remake.exe'},
                         f'Unbekannte EXE im Projekt-Hauptordner: {exe_namen}')
        self.assertTrue((R / '.gitignore').is_file())
        self.assertIn('*.exe', (R / '.gitignore').read_text(encoding='utf-8'))
    def test_protokoll_extern(self):
        t=(R/'docs/ENTWICKLUNGSPROTOKOLL.md').read_text(encoding='utf-8')
        self.assertIn('GPT-ABS01',t)
        self.assertIn('ChatGPT',t)

if __name__=='__main__':unittest.main(verbosity=2)
