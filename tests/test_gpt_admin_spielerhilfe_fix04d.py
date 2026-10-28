# -*- coding: utf-8 -*-
"""FIX04d – Admin überschreibt nur die HilfedARSTELLUNG, nicht Spielregeln."""
from __future__ import annotations

import sys
import tempfile
import tkinter as tk
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import admin_werkzeuge
import admin_oberflaeche
import admin_teststand
from tkinter import ttk
import main
import spielerhilfe
import speichern


class AdminHilferegeln(unittest.TestCase):
    def setUp(self):
        self.state = main.GameState()
        self.state.admin_teststand = True
        self.state.oekonomie_aktiv = True

    def test_standard_waehrend_schutz_und_danach(self):
        self.assertEqual(self.state.admin_hilfe_modus, 'auto')
        self.assertTrue(spielerhilfe.hilfe_sichtbar(self.state, admin_freigabe=True))
        self.state.noob_protection = False
        self.assertFalse(spielerhilfe.hilfe_sichtbar(self.state, admin_freigabe=True))

    def test_admin_darf_anzeige_waehrend_schutz_aus_und_an_schalten(self):
        self.assertTrue(self.state.noob_protection)
        admin_werkzeuge.spielerhilfe_modus_setzen(self.state, 'ausblenden', freigabe=True)
        self.assertFalse(spielerhilfe.hilfe_sichtbar(self.state, admin_freigabe=True))
        self.assertTrue(self.state.noob_protection)  # Kein Abschalten des Götterschutzes!
        admin_werkzeuge.spielerhilfe_modus_setzen(self.state, 'anzeigen', freigabe=True)
        self.assertTrue(spielerhilfe.hilfe_sichtbar(self.state, admin_freigabe=True))
        self.state.noob_protection = False
        self.assertTrue(spielerhilfe.hilfe_sichtbar(self.state, admin_freigabe=True))
        self.assertIn('Götterschutz beendet', spielerhilfe.kurzinfo(self.state, admin_freigabe=True))

    def test_ohne_admin_freigabe_oder_mit_falschem_modus_gesperrt(self):
        with self.assertRaises(PermissionError):
            admin_werkzeuge.spielerhilfe_modus_setzen(self.state, 'ausblenden')
        with self.assertRaises(ValueError):
            admin_werkzeuge.spielerhilfe_modus_setzen(self.state, 'deaktivierter_schutz', freigabe=True)
        self.assertEqual(self.state.admin_hilfe_modus, 'auto')
        self.state.admin_hilfe_modus = 'ausblenden'
        self.assertTrue(spielerhilfe.hilfe_sichtbar(self.state, admin_freigabe=False))
        self.state.admin_teststand = False
        self.assertTrue(spielerhilfe.hilfe_sichtbar(self.state, admin_freigabe=True))

    def test_adminmodus_getrennt_sichern_laden_und_spieler_nicht_veraendern(self):
        admin_werkzeuge.spielerhilfe_modus_setzen(self.state, 'ausblenden', freigabe=True)
        with tempfile.TemporaryDirectory() as temp:
            admin_path = str(Path(temp) / 'admin_test.json')
            self.assertTrue(self.state.save(admin_path, admin_freigabe=True))
            gespeicherte, _ = speichern.lade(admin_path)
            self.assertEqual(gespeicherte.get('admin_hilfe_modus'), 'ausblenden')
            self.assertFalse(main.GameState().load(admin_path))
            neu = main.GameState()
            self.assertTrue(neu.load(admin_path, admin_freigabe=True))
            self.assertEqual(neu.admin_hilfe_modus, 'ausblenden')
            spieler = main.GameState()
            spieler.admin_hilfe_modus = 'anzeigen'  # defensive Test-Eingabe
            spieler_path = str(Path(temp) / 'spieler.json')
            self.assertTrue(spieler.save(spieler_path))
            daten, _ = speichern.lade(spieler_path)
            self.assertNotIn('admin_hilfe_modus', daten)
            laden = main.GameState()
            self.assertTrue(laden.load(spieler_path))
            self.assertEqual(laden.admin_hilfe_modus, 'auto')


class AdminHilfeGUI(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = main.NebelseetalApp(self.root)
        self.app.state.admin_teststand = True
        self.app.state.oekonomie_aktiv = True
        self.app._profil = 'admin'
        self.app._admin_sitzung_freigegeben = True
        self.app._build_main_ui()

    def tearDown(self):
        self.root.destroy()

    def test_toggle_bei_aktivem_und_abgelaufenem_schutz(self):
        self.assertEqual(self.app.hilfe_rahmen.winfo_manager(), 'pack')
        admin_werkzeuge.spielerhilfe_modus_setzen(self.app.state, 'ausblenden', freigabe=True)
        self.app._spielerhilfe_anzeige_aktualisieren()
        self.assertFalse(self.app.hilfe_rahmen.winfo_manager())
        admin_werkzeuge.spielerhilfe_modus_setzen(self.app.state, 'anzeigen', freigabe=True)
        self.app._spielerhilfe_anzeige_aktualisieren()
        self.assertEqual(self.app.hilfe_rahmen.winfo_manager(), 'pack')
        self.app.state.noob_protection = False
        self.app._spielerhilfe_anzeige_aktualisieren()
        self.assertIn('Götterschutz beendet', self.app.hilfe_kurztext.cget('text'))
        self.assertEqual(self.app.hilfe_rahmen.winfo_manager(), 'pack')
        self.app._switch_view('Anleitung')
        self.assertEqual(self.app.current_view, 'Anleitung')
        admin_werkzeuge.spielerhilfe_modus_setzen(self.app.state, 'auto', freigabe=True)
        self.app._spielerhilfe_anzeige_aktualisieren()
        self.assertFalse(self.app.hilfe_rahmen.winfo_manager())

    def test_admin_dialog_bietet_die_drei_anzeigemodi(self):
        self.app.state.generate_map(self.app.state.current_map)
        admin_teststand.teststand_aufbauen(
            self.app.state, main.Settlement, main.siedlung_kennung)
        fenster = admin_oberflaeche.oeffnen(
            self.root, self.app.state, main.MAPS,
            speichern=lambda: True,
            aktualisieren=self.app._spielerhilfe_anzeige_aktualisieren)
        try:
            books = [w2 for w in fenster.winfo_children() for w2 in w.winfo_children()
                     if isinstance(w2, ttk.Notebook)]
            self.assertEqual(len(books), 1)
            labels = [books[0].tab(k, 'text') for k in books[0].tabs()]
            self.assertIn('Spielerhilfe / Anzeige', labels)
            feld = books[0].nametowidget(books[0].tabs()[labels.index('Spielerhilfe / Anzeige')])
            radios = [w for w in feld.winfo_children() if isinstance(w, ttk.Radiobutton)]
            self.assertEqual(len(radios), 3)
            self.assertEqual({w.cget('value') for w in radios}, {'auto', 'anzeigen', 'ausblenden'})
            [r for r in radios if r.cget('value') == 'ausblenden'][0].invoke()
            [w for w in feld.winfo_children() if isinstance(w, ttk.Button)][0].invoke()
            self.assertEqual(self.app.state.admin_hilfe_modus, 'ausblenden')
            self.assertFalse(self.app.hilfe_rahmen.winfo_manager())
        finally:
            fenster.destroy()

    def test_normalprofil_ignoriert_adminanzeige_und_hilfe_immer_erreichbar(self):
        self.app._profil = 'spieler'
        self.app._admin_sitzung_freigegeben = False
        self.app.state.admin_hilfe_modus = 'ausblenden'
        self.app._spielerhilfe_anzeige_aktualisieren()
        self.assertEqual(self.app.hilfe_rahmen.winfo_manager(), 'pack')
        self.app.state.noob_protection = False
        self.app._spielerhilfe_anzeige_aktualisieren()
        self.assertFalse(self.app.hilfe_rahmen.winfo_manager())
        self.app._switch_view('Anleitung')
        self.assertEqual(self.app.current_view, 'Anleitung')


if __name__ == '__main__':
    unittest.main(verbosity=2)
