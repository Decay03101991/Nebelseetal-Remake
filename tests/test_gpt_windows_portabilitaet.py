"""Tests fuer eigenstaendige Projektkopien und Windows-Ablauf (keine EXE-Simulation)."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT = Path(__file__).resolve().parent.parent


class PortableRelease(unittest.TestCase):
    def test_spieldaten_aus_fremdem_arbeitsverzeichnis(self):
        code = ('import sys; sys.path.insert(0, sys.argv[1]); import spieldaten;'
                'print(spieldaten.projektwurzel());'
                'assert spieldaten.projektwurzel()==sys.argv[2]')
        with tempfile.TemporaryDirectory(prefix='nebel_portable_') as cwd:
            res = subprocess.run([sys.executable, '-c', code, str(ROOT / 'src'), str(ROOT)],
                                 cwd=cwd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, res.stderr)
    def test_generator_schreibt_nicht_automatisch(self):
        code = (ROOT / 'tools' / 'build_units.py').read_text(encoding='utf-8')
        self.assertIn('--legacy-neuschreiben', code)
        self.assertIn('Path(__file__).resolve().parent.parent', code)
    def test_hermes_zieluebergabe_sucht_eigenen_projektstand(self):
        code = (ROOT / 'tools' / 'zieluebergabe.py').read_text(encoding='utf-8')
        self.assertIn('PROJEKT = Path(__file__).resolve().parent.parent', code)
    def test_startskript_arbeitet_mit_eigenem_ordner(self):
        script = (ROOT/'START_SPIEL_WINDOWS.bat').read_text(encoding='utf-8')
        self.assertIn('%~dp0', script)
        self.assertNotIn('D:\\Arbeiten\\Nebelseetal_Remake', script)
    def test_buildskript_arbeitet_mit_eigenem_ordner(self):
        script = (ROOT/'EXE_ERSTELLEN_WINDOWS.bat').read_text(encoding='utf-8')
        self.assertIn('%~dp0', script)
        self.assertIn('gpt_windows_vorpruefung.py', script)
    def test_keine_mitgelieferten_spielstaende_im_projekt(self):
        self.assertFalse((ROOT/'src'/'savegame.json').exists())
        self.assertFalse((ROOT/'tor.json').exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
