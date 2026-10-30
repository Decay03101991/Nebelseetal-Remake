"""FIX05: Benutzer-Tempo bleibt dauerhaft, ohne Source-/EXE-Bundle zu mutieren."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src'))
import spielzeit


class SpielzeitEinstellungen(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.env = patch.dict(os.environ, {'NEBEL_SPIELDATEN_ORDNER': self.temp.name})
        self.env.start()
        self.addCleanup(self.env.stop)
        spielzeit.vergessen()
        self.addCleanup(spielzeit.vergessen)

    def test_schreibt_nur_in_privaten_ordner_und_laedt_nach_neustart(self):
        original = Path(spielzeit.PFAD).read_bytes()
        self.assertEqual(spielzeit.setzen(60), 60)
        datei = Path(self.temp.name) / 'spielzeit_einstellung.json'
        self.assertTrue(datei.is_file())
        self.assertEqual(json.loads(datei.read_text(encoding='utf-8'))['faktor'], 60)
        self.assertEqual(Path(spielzeit.PFAD).read_bytes(), original)
        spielzeit.vergessen()
        self.assertEqual(spielzeit.faktor(), 60)

    def test_zwei_editionen_haben_getrennte_einstellungen(self):
        spielzeit.setzen(20)
        with tempfile.TemporaryDirectory() as public:
            with patch.dict(os.environ, {'NEBEL_SPIELDATEN_ORDNER': public}):
                spielzeit.vergessen()
                self.assertEqual(spielzeit.faktor(), spielzeit.STANDARD_FAKTOR)
                spielzeit.setzen(600)
                self.assertEqual(spielzeit.faktor(), 600)
        spielzeit.vergessen()
        self.assertEqual(spielzeit.faktor(), 20)

    def test_ungueltige_stufendatei_macht_einstellungen_nicht_unbenutzbar(self):
        datei = Path(self.temp.name) / 'spielzeit_einstellung.json'
        datei.write_text(json.dumps({'faktor': 60, 'stufen': [1, 'kaputt', None, float('inf'), 20]}))
        spielzeit.vergessen()
        self.assertEqual(spielzeit.stufen(), [1.0, 20.0, 60.0])

    def test_schreibfehler_ersetzt_weder_datei_noch_aktiven_faktor(self):
        spielzeit.setzen(20)
        datei = Path(self.temp.name) / 'spielzeit_einstellung.json'
        alt = datei.read_bytes()
        with patch.object(spielzeit.os, 'replace', side_effect=OSError('Datentraeger voll')):
            with self.assertRaises(OSError):
                spielzeit.setzen(600)
        self.assertEqual(datei.read_bytes(), alt)
        self.assertEqual(spielzeit.faktor(), 20)
        self.assertEqual(list(datei.parent.glob('.spielzeit_*.tmp')), [])

    def test_gui_einstellung_schreibt_in_laufzeitordner(self):
        try:
            import tkinter as tk
            from main import NebelseetalApp, GameState
            root = tk.Tk()
        except Exception as exc:
            self.skipTest(f'Grafischer Test nicht moeglich: {exc}')
        root.withdraw()
        try:
            app = NebelseetalApp(root, tor_pfad=str(Path(self.temp.name) / 'tor_test.json'))
            app._tor_geoeffnet = True
            self.assertTrue(app._spiel_starten(GameState(), 'spieler'))
            app._build_main_ui()
            app._render_settings()
            def widgets(widget):
                for child in widget.winfo_children():
                    yield child
                    yield from widgets(child)
            knopf = next(w for w in widgets(root)
                         if isinstance(w, tk.Button) and '×60 ' in str(w.cget('text')))
            knopf.invoke()
            self.assertEqual(spielzeit.faktor(), 60)
            self.assertTrue(spielzeit.einstellungspfad().is_file())
        finally:
            root.destroy()

    def test_defektes_benutzer_json_faellt_auf_bundled_default_zurueck(self):
        datei = Path(self.temp.name) / 'spielzeit_einstellung.json'
        datei.write_text('{defekt', encoding='utf-8')
        self.assertEqual(spielzeit.faktor(), spielzeit.STANDARD_FAKTOR)
        self.assertEqual(spielzeit.setzen(180), 180)
        self.assertEqual(json.loads(datei.read_text(encoding='utf-8'))['faktor'], 180)


if __name__ == '__main__':
    unittest.main(verbosity=2)
