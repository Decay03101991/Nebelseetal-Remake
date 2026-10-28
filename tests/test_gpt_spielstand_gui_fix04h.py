# -*- coding: utf-8 -*-
"""FIX04h: Sichtbarkeit der Spielstandarchive; Admin-Zugang; UI-Verknuepfung."""
import os
import json
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
import spielstand_archiv as archiv


def widgets(rahmen, typ):
    aus = []
    for kind in rahmen.winfo_children():
        if isinstance(kind, typ):
            aus.append(kind)
        aus.extend(widgets(kind, typ))
    return aus


class ArchivGuiFix04h(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = tk.Tk()
        self.root.withdraw()
        self.addCleanup(self.root.destroy)
        with patch.dict(os.environ, {'NEBEL_SPIELDATEN_ORDNER': self.tmp.name}):
            self.app = main.NebelseetalApp(self.root,
                tor_pfad=str(Path(self.tmp.name) / 'tor_test.json'))
        self.app._tor_geoeffnet = True
        self.app._profil = 'spieler'
        self.slot2 = Path(spielstaende.slot_pfad(self.tmp.name, 2))
        self.slot2.write_text('{"day": 1, "admin_teststand": false}', encoding='utf-8')
        ok, self.archiv2 = archiv.archiviere(str(self.slot2), 'spieler', 'test')
        self.assertTrue(ok)

    def test_normaler_spieler_sieht_keine_archivliste_und_keinen_restore_button(self):
        self.assertTrue(self.app._spielstand_verwaltung('spieler'))
        fenster = next(w for w in self.root.winfo_children() if isinstance(w, tk.Toplevel))
        self.assertFalse(widgets(fenster, tk.Listbox))
        texte = [w.cget('text') for w in widgets(fenster, tk.Button)]
        self.assertFalse(any('Wiederherstellen' in txt or 'Entwicklerarchiv' in txt for txt in texte))
        self.assertFalse(widgets(fenster, tk.ttk.Combobox) if hasattr(tk, 'ttk') else False)
        fenster.destroy()

    def test_normaler_spieler_kommt_nicht_ueber_direkten_aufruf_ins_archiv(self):
        self.assertFalse(self.app._archiv_wiederherstellung_dialog('spieler', self.tmp.name, self.root))
        self.assertFalse(any(isinstance(w, tk.Toplevel) for w in self.root.winfo_children()))

    def test_admin_archiv_zeigt_nur_echte_slot2_archivversion(self):
        self.app._profil = 'admin'
        self.app.state.admin_teststand = True
        self.app._admin_sitzung_freigegeben = True
        self.assertTrue(self.app._archiv_wiederherstellung_dialog('spieler', self.tmp.name, self.root))
        fenster = next(w for w in self.root.winfo_children() if isinstance(w, tk.Toplevel))
        listen = widgets(fenster, tk.Listbox)
        self.assertEqual(len(listen), 1)
        self.assertEqual(listen[0].size(), 1)
        self.assertIn('Slot 2', listen[0].get(0))
        self.assertNotIn('Slot 3', listen[0].get(0))
        labels = [w.cget('text') for w in widgets(fenster, tk.Label)]
        self.assertTrue(any('Archivgroesse' in txt for txt in labels))
        fenster.destroy()

    def test_admin_restauriert_gezielt_slot2_nach_zweifacher_bestaetigung(self):
        self.app._profil = 'admin'
        self.app.state.admin_teststand = True
        self.app._admin_sitzung_freigegeben = True
        self.app._archiv_wiederherstellung_dialog('spieler', self.tmp.name, self.root)
        fenster = next(w for w in self.root.winfo_children() if isinstance(w, tk.Toplevel))
        liste = widgets(fenster, tk.Listbox)[0]
        liste.selection_set(0)
        with patch('tkinter.messagebox.askyesno', return_value=True) as frage:
            next(w for w in widgets(fenster, tk.Button)
                 if w.cget('text') == 'Ausgewaehlten Stand wiederherstellen').invoke()
            frage.assert_called_once()
        self.assertTrue(self.slot2.is_file())
        self.assertEqual(json.loads(self.slot2.read_text(encoding='utf-8'))['day'], 1)
        self.assertTrue(Path(self.archiv2).exists())
        fenster.destroy()

    def test_archivgroesse_ohne_dateiloeschung(self):
        anzahl, groesse = archiv.archiv_groesse(self.tmp.name)
        self.assertGreaterEqual(anzahl, 2)  # savegame + metadata
        self.assertGreater(groesse, 0)
        self.assertFalse(self.slot2.exists())
        self.assertTrue(Path(self.archiv2).exists())

    def test_admin_steuerung_ist_gesondert_freigegeben(self):
        self.app._profil = 'admin'
        self.app.state.admin_teststand = True
        self.assertFalse(self.app._spielstand_verwaltung('admin'))
        self.app._admin_sitzung_freigegeben = True
        self.assertTrue(self.app._spielstand_verwaltung('admin'))
        fenster = next(w for w in self.root.winfo_children() if isinstance(w, tk.Toplevel))
        texte = [w.cget('text') for w in widgets(fenster, tk.Button)]
        self.assertIn('Spielerslot-Archive pruefen (Admin)', texte)
        fenster.destroy()

if __name__ == '__main__':
    unittest.main(verbosity=2)
