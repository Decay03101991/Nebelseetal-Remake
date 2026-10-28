"""GPT-PR01: Grundtor -> Profilwahl -> drei Normal-Slots ODER Admin-Testwelt.

Der Test nutzt ausschliesslich Temp-Verzeichnisse; keine realen tor.json oder Saves.
Windows-GUI-Probe hier mit xvfb-run auf Linux. GUI-Funktionalitaet im Windows-Build
ist gesondert zu verifizieren.
"""
from __future__ import annotations
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import main
import spielstaende
import speichern
import tor
import tkinter as tk


class ProfileTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = self.tmp.name
        self.main_gate = os.path.join(self.path, 'tor.json')
        self.admin_gate = os.path.join(self.path, 'admin_tor.json')
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = main.NebelseetalApp(self.root, tor_pfad=self.main_gate)
        self.app.admin_tor_pfad = self.admin_gate
        self.app.slots_ordner = self.path
        self.app._build_loading_screen = lambda: None  # keine asynchrone Spieluhr starten

    def tearDown(self):
        self.root.destroy()
        self.tmp.cleanup()

    def test_01_tor_und_profil_getrennt(self):
        self.assertFalse(self.app._tor_geoeffnet)
        self.app._profil_auswahl()
        self.assertEqual(self.app._profil, None)
        self.assertFalse(hasattr(self.app, 'menu_buttons'))
        self.app.tor_neu1.insert(0, 'GRUND-TOR-TEST')
        self.app.tor_neu2.insert(0, 'GRUND-TOR-TEST')
        self.app._tor_setzen()
        self.assertTrue(tor.hat_passwort(self.main_gate))
        self.assertTrue(self.app._tor_geoeffnet)
        self.assertIsNone(self.app._profil)
        self.assertFalse(os.path.exists(self.admin_gate))
        self.app._profil_auswahl()
        labels = [w.cget('text') for w in _desc(self.root) if isinstance(w, tk.Button)]
        self.assertTrue(any('normal spielen' in s for s in labels))
        self.assertTrue(any('Adminaccount' in s for s in labels))
        self.assertFalse(hasattr(self.app, 'menu_buttons'))

    def test_02_drei_slots_vor_spielstart(self):
        self.app._tor_geoeffnet = True
        self.app._spieler_auswahl()
        buttons = [w for w in _desc(self.root) if isinstance(w, tk.Button)]
        self.assertEqual(len([b for b in buttons if 'Slot ' in b.cget('text')]), 3)
        self.assertEqual(len([b for b in buttons if 'Slot ' in b.cget('text') and b.cget('state') == 'disabled']), 3)
        self.app._spieler_neu_starten()
        self.assertEqual(self.app._profil, 'spieler')
        self.assertFalse(self.app.state.admin_teststand)
        self.assertFalse(self.app._admin_sitzung_freigegeben)

    def test_03_normales_laden_der_drei_slots(self):
        self.app._tor_geoeffnet = True
        for i in spielstaende.SLOTS:
            s = main.GameState()
            s.day = i + 11
            self.assertTrue(s.save(spielstaende.slot_pfad(self.path, i)))
        self.app._spieler_auswahl()
        for i in spielstaende.SLOTS:
            self.app._spieler_slot_starten(i)
            self.assertEqual(self.app._profil, 'spieler')
            self.assertEqual(self.app.state.day, i + 11)
            self.assertFalse(self.app.state.admin_teststand)

    def test_04_adminstand_ist_keine_normale_partie(self):
        self.app._tor_geoeffnet = True
        stand = main.GameState()
        stand.admin_teststand = True
        self.assertFalse(stand.save(spielstaende.slot_pfad(self.path, 1)))
        self.assertFalse(self.app._spiel_starten(stand, 'spieler'))
        self.assertFalse(self.app._spiel_starten(stand, 'admin'))
        self.assertIsNone(self.app._profil)
        self.assertTrue(stand.save(spielstaende.admin_pfad(self.path), admin_freigabe=True))
        self.assertFalse(main.GameState().load(spielstaende.admin_pfad(self.path)))

    def test_05_admin_passwort_unabhaengig(self):
        self.app._tor_geoeffnet = True
        self.assertTrue(tor.setze_passwort('MAIN-SECRET-2026', 'MAIN-SECRET-2026', self.main_gate)[0])
        self.assertTrue(tor.setze_passwort('ADMIN-SECRET-2026', 'ADMIN-SECRET-2026', self.admin_gate)[0])
        self.assertTrue(tor.pruefe_passwort('MAIN-SECRET-2026', self.main_gate)[0])
        self.assertFalse(tor.pruefe_passwort('MAIN-SECRET-2026', self.admin_gate)[0])
        self.assertTrue(tor.pruefe_passwort('ADMIN-SECRET-2026', self.admin_gate)[0])
        self.assertFalse(tor.pruefe_passwort('ADMIN-SECRET-2026', self.main_gate)[0])
        self.assertNotEqual(self.main_gate, self.admin_gate)

    def test_06_adminprofil_eigener_speicherpfad(self):
        self.app._tor_geoeffnet = True
        self.app._admin_sitzung_freigegeben = True
        stand = main.GameState()
        stand.admin_teststand = True
        self.assertTrue(self.app._spiel_starten(stand, 'admin'))
        with patch.object(main, 'schreibordner', lambda: self.path):
            self.assertTrue(self.app._admin_speichern())
            apath = spielstaende.admin_pfad(self.path)
            self.assertTrue(os.path.exists(apath))
            self.assertFalse(any(os.path.isfile(spielstaende.slot_pfad(self.path, i)) for i in (1,2,3)))
            self.assertEqual(speichern.lade(apath)[0]['admin_teststand'], True)
            self.assertTrue(self.app._admin_laden())
            self.assertTrue(self.app.state.admin_teststand)
            self.app._slot_auswahl('save')  # Admin darf kein Normal-Slot-Fenster oeffnen
            self.assertFalse(any(os.path.isfile(spielstaende.slot_pfad(self.path, i)) for i in (1,2,3)))
        self.assertEqual(self.app._profil, 'admin')

    def test_07_admin_ist_nach_profilwechsel_abgemeldet(self):
        self.app._tor_geoeffnet = True
        self.app._admin_sitzung_freigegeben = True
        stand = main.GameState()
        stand.admin_teststand = True
        self.assertTrue(self.app._spiel_starten(stand, 'admin'))
        self.app._profil_auswahl()
        self.assertIsNone(self.app._profil)
        self.assertFalse(self.app._admin_sitzung_freigegeben)
        self.assertFalse(self.app.state.admin_teststand)
        self.app._spieler_neu_starten()
        self.assertEqual(self.app._profil, 'spieler')
        self.assertFalse(self.app.state.admin_teststand)

    def test_09_erstes_adminprofil_direkt_im_programm_einrichten(self):
        self.app._tor_geoeffnet = True
        pw = 'NEUER-ADMIN-CODE-TEST'
        with patch.object(main, 'schreibordner', lambda: self.path), \
             patch('tkinter.messagebox.askyesno', return_value=True), \
             patch('tkinter.messagebox.askyesnocancel', return_value=True), \
             patch('tkinter.simpledialog.askstring', side_effect=[pw, pw]):
            self.app._admin_dialog()
        self.assertTrue(tor.hat_passwort(self.admin_gate))
        self.assertFalse(os.path.exists(self.main_gate))  # Grundtor bleibt unangetastet
        self.assertEqual(self.app._profil, 'admin')
        self.assertTrue(self.app._admin_sitzung_freigegeben)
        self.assertTrue(self.app.state.admin_teststand)
        self.assertTrue(os.path.isfile(spielstaende.admin_pfad(self.path)))
        self.assertFalse(any(os.path.exists(spielstaende.slot_pfad(self.path, n))
                             for n in spielstaende.SLOTS))

    def test_08_admin_button_only_in_admin_mode(self):
        self.app._tor_geoeffnet = True
        self.app._spieler_neu_starten()
        self.app._build_main_ui()
        texts = [b.cget('text') for b in _desc(self.root) if isinstance(b, tk.Button)]
        self.assertIn('Speichern', texts)
        self.assertNotIn('Admin-Werkzeuge', texts)
        self.assertNotIn('Admin-Test', texts)
        self.app._admin_sitzung_freigegeben = True
        stand = main.GameState()
        stand.admin_teststand = True
        self.app._spiel_starten(stand, 'admin')
        self.app._build_main_ui()
        texts = [b.cget('text') for b in _desc(self.root) if isinstance(b, tk.Button)]
        self.assertIn('Admin-Werkzeuge', texts)
        self.assertIn('Admin sichern', texts)
        self.assertNotIn('Speichern', texts)


def _desc(w):
    out = []
    for ch in w.winfo_children():
        out.append(ch)
        out.extend(_desc(ch))
    return out


if __name__ == '__main__':
    unittest.main(verbosity=2)
