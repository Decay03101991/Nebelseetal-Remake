"""Release-Edition Regressionen: public GUI ohne Admin, Daten weiterhin in Repo."""
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/"src"))
import ausgabemodus
from main import NebelseetalApp, GameState

class PublicEditionTests(unittest.TestCase):
    def test_switch(self):
        with patch.dict(os.environ,{"NEBEL_OEFFENTLICHE_TESTVERSION":"1"}):
            self.assertTrue(ausgabemodus.ist_oeffentliche_testversion())
        with patch.dict(os.environ,{"NEBEL_OEFFENTLICHE_TESTVERSION":"0"}):
            self.assertFalse(ausgabemodus.ist_oeffentliche_testversion())

    def test_public_entry_separates_saves_and_password(self):
        script=(ROOT/"src"/"public_start.py").read_text(encoding="utf-8")
        self.assertIn('Public_Test_FIX04j',script)
        self.assertIn('NEBEL_OEFFENTLICHE_TESTVERSION',script)
        self.assertIn('NEBEL_SPIELDATEN_ORDNER',script)
        self.assertIn('"tor.json"', (ROOT/"src"/"main.py").read_text(encoding="utf-8"))

    def test_admin_files_remain_in_repo(self):
        for file in ('src/admin_teststand.py','src/admin_werkzeuge.py',
                     'src/admin_oberflaeche.py','tests/test_gpt_adminwerkzeuge.py'):
            # The known admin test can have a different basename: test the modules separately.
            if file.startswith('tests/'):
                self.assertTrue(any((ROOT/'tests').glob('*admin*')))
            else:
                self.assertTrue((ROOT/file).is_file())

    def test_public_user_flow_and_admin_block(self):
        try: import tkinter as tk
        except ImportError: self.skipTest('Tkinter nicht verfuegbar')
        try:
            root=tk.Tk();root.withdraw()
        except tk.TclError: self.skipTest('Keine grafische Testanzeige')
        with tempfile.TemporaryDirectory() as tmp:
            with patch.dict(os.environ, {'NEBEL_OEFFENTLICHE_TESTVERSION':'1',
                                         'NEBEL_SPIELDATEN_ORDNER':tmp}):
                app=NebelseetalApp(root,tor_pfad=str(Path(tmp)/'tor.json'))
                app._tor_geoeffnet=True
                app._profil_auswahl()
                self.assertIsNone(app._profil)
                self.assertFalse(any('Adminaccount' in str(w.cget('text')) for w in root.winfo_children()
                                     if hasattr(w,'cget') and 'text' in w.keys()))
                self.assertFalse(app._spiel_starten(GameState(),'admin'))
                self.assertIsNone(app._admin_dialog())
                self.assertIsNone(app._admin_werkzeuge_dialog())
                self.assertTrue(app._spiel_starten(GameState(),'spieler'))
                root.update_idletasks()
        root.destroy()

    def test_developer_mode_keeps_admin_profile_choice(self):
        import tkinter as tk
        try:
            root = tk.Tk()
            root.withdraw()
        except tk.TclError:
            self.skipTest('Keine grafische Testanzeige')
        try:
            with tempfile.TemporaryDirectory() as tmp:
                with patch.dict(os.environ, {'NEBEL_OEFFENTLICHE_TESTVERSION':'0',
                                             'NEBEL_SPIELDATEN_ORDNER':tmp}):
                    app=NebelseetalApp(root,tor_pfad=str(Path(tmp)/'tor.json'))
                    app._tor_geoeffnet=True
                    app._profil_auswahl()
                    labels=[]
                    def walk(widget):
                        try:
                            if 'text' in widget.keys(): labels.append(str(widget.cget('text')))
                        except Exception:
                            pass
                        for child in widget.winfo_children(): walk(child)
                    walk(root)
                    self.assertTrue(any('Adminaccount' in text for text in labels))
        finally:
            root.destroy()

    def test_public_start_overrides_old_save_environment(self):
        import runpy
        from types import SimpleNamespace
        with tempfile.TemporaryDirectory() as tmp:
            with patch.dict(os.environ, {'LOCALAPPDATA':tmp,
                                         'NEBEL_SPIELDATEN_ORDNER':'/alter/pfad',
                                         'NEBEL_OEFFENTLICHE_TESTVERSION':'0'}):
                with patch.dict(sys.modules, {'main':SimpleNamespace(main=lambda:None)}):
                    runpy.run_path(str(ROOT/'src'/'public_start.py'),run_name='public_start_only')
                self.assertEqual(os.environ['NEBEL_OEFFENTLICHE_TESTVERSION'],'1')
                self.assertEqual(Path(os.environ['NEBEL_SPIELDATEN_ORDNER']),
                                 Path(tmp)/'Nebelseetal_Remake'/'Public_Test_FIX04j')

if __name__ == '__main__':
    unittest.main(verbosity=2)
