# -*- coding: utf-8 -*-
"""FIX04i: Seitlicher Original-Schildhintergrund, gespeicherte Slots unberuehrt."""
import os
import sys
import tempfile
import tkinter as tk
import unittest
from pathlib import Path
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import main
import spielstaende


def alle(w):
    for kind in w.winfo_children():
        yield kind
        yield from alle(kind)

class SchildLayout(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = tk.Tk()
        self.root.withdraw()
        self.addCleanup(self.root.destroy)
        with patch.dict(os.environ, {'NEBEL_SPIELDATEN_ORDNER': self.tmp.name}):
            self.app = main.NebelseetalApp(
                self.root, tor_pfad=str(Path(self.tmp.name)/'tor.json'))
        self.app._tor_geoeffnet = True
        self.app._profil = 'spieler'

    def erstes_fenster(self):
        return next(w for w in self.root.winfo_children() if isinstance(w, tk.Toplevel))

    def test_spielstandverwaltung_verwendet_originalschild_ohne_spielstandverlust(self):
        pfad = Path(spielstaende.slot_pfad(self.tmp.name, 1))
        pfad.write_text('{"day": 5}', encoding='utf-8')
        self.assertTrue(self.app._spielstand_verwaltung('spieler'))
        fenster = self.erstes_fenster()
        self.assertIsInstance(getattr(fenster, '_nebelseetal_schild_bild'), tk.PhotoImage)
        self.assertEqual(len([b for b in alle(fenster) if isinstance(b, tk.Button)
                              and b.cget('text') == 'Loeschen (archivieren)']), 3)
        self.assertTrue(pfad.exists())
        fenster.destroy()

    def test_login_ladebild_wird_wiederverwendet(self):
        self.assertTrue(Path(main.ladebild_pfad()).is_file())
        self.assertEqual(main.LADEBILD_PNG[-1], 'Nebelseetal_Loadingpage.png')
        self.assertTrue(self.app._spielstand_verwaltung('spieler'))
        fenster = self.erstes_fenster()
        self.assertGreaterEqual(fenster._nebelseetal_schild_bild.width(), 400)
        self.assertGreaterEqual(fenster._nebelseetal_schild_bild.height(), 300)
        fenster.destroy()

    def test_admin_archiv_mit_originalschild_und_slotzuordnung(self):
        self.app._profil = 'admin'
        self.app.state.admin_teststand = True
        self.app._admin_sitzung_freigegeben = True
        self.assertTrue(self.app._archiv_wiederherstellung_dialog('spieler',self.tmp.name,self.root))
        fenster=self.erstes_fenster()
        self.assertIsInstance(getattr(fenster, '_nebelseetal_schild_bild'), tk.PhotoImage)
        self.assertEqual(len([x for x in alle(fenster) if isinstance(x, tk.Listbox)]),1)
        fenster.destroy()

    def test_laden_speichern_fenster_mit_schild(self):
        self.app._slot_auswahl('load')
        fenster=self.erstes_fenster()
        self.assertIsInstance(getattr(fenster, '_nebelseetal_schild_bild'),tk.PhotoImage)
        self.assertEqual(len([b for b in alle(fenster) if isinstance(b,tk.Button)
                              and b.cget('text').startswith('Laden #')]), 3)
        fenster.destroy()

    def test_admin_aktionsknopf_in_eigener_zeile(self):
        self.app._profil = 'admin'
        self.app._admin_sitzung_freigegeben = True
        self.app.state.admin_teststand = True
        self.app._build_main_ui()
        self.assertIn('Admin-Spielstaende', self.app.aktionsknopfe)
        knopf = self.app.aktionsknopfe['Admin-Spielstaende']
        self.assertIs(knopf.master, self.app.aktionsleiste)
        self.root.update_idletasks()
        self.assertTrue(knopf.winfo_exists())

    def test_hintergrund_fallback_blockiert_nicht(self):
        with patch.object(main, 'ladebild_pfad', return_value='fehlendes-schild.png'):
            self.assertTrue(self.app._spielstand_verwaltung('spieler'))
        fenster=self.erstes_fenster()
        self.assertFalse(hasattr(fenster, '_nebelseetal_schild_bild'))
        self.assertTrue(any(isinstance(x,tk.Button) for x in alle(fenster)))
        fenster.destroy()

if __name__=='__main__':
    unittest.main(verbosity=2)
