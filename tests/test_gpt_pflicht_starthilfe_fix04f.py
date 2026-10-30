# -*- coding: utf-8 -*-
"""FIX04f: Starthilfe ist bis Gruendung + tatsaechlicher Grundproduktion Pflicht.

Betrifft ausschliesslich die Dorfzentrum-Aufgabenkarte. Das rechte Hilfepanel
unterliegt weiterhin Schutz-/Admin-Regeln. Kein Saveflag, keine neuen Spielregeln.
"""
from __future__ import annotations
import sys
import tempfile
import tkinter as tk
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import main
import spieloekonomie
import spielerhilfe
import admin_werkzeuge


def _erste_siedlung(zustand):
    karte = spieloekonomie.startkarte('pflicht-test', 'spieler')
    ort = main.Settlement(name='Siedlung 1', map_id=zustand.current_map,
                          karte=karte, id='pflicht-s1')
    zustand.settlements = [ort]
    return ort


def _baue(ort, geb, art):
    idx = next(i for i, gel in enumerate(ort.karte['raster'])
               if gel == art and str(i) not in ort.bauten)
    ort.bauten[str(idx)] = geb


def _texte(widget):
    a = []
    for child in widget.winfo_children():
        if isinstance(child, tk.Label):
            a.append(str(child.cget('text')))
        a += _texte(child)
    return a


class PflichtStartregel(unittest.TestCase):
    def setUp(self):
        self.z = main.GameState()

    def test_ohne_erste_siedlung_immer_pflicht_auch_ohne_schutz(self):
        self.assertTrue(spielerhilfe.startaufgabe_pflicht(self.z))
        self.z.noob_protection = False
        self.assertTrue(spielerhilfe.startaufgabe_pflicht(self.z))

    def test_passiver_holz_stein_grundertrag_genuegt_nicht(self):
        _erste_siedlung(self.z)
        self.assertEqual(self.z.ertrag_je_ort(self.z.settlements[0])['holz'], 1)
        self.assertEqual(self.z.ertrag_je_ort(self.z.settlements[0])['stein'], 1)
        self.assertTrue(spielerhilfe.startaufgabe_pflicht(self.z))
        self.assertEqual(spielerhilfe.grundproduktion_erste_siedlung(self.z),
                         {'holz':0,'stein':0,'nahrung':0})

    def test_erst_drei_wirkliche_produktionen_beenden_pflicht(self):
        ort = _erste_siedlung(self.z)
        for geb, terrain, schluessel in (('holzfaeller','wald','holz'),
                                         ('steinmetz','berg','stein'),
                                         ('jaeger','wald','nahrung')):
            _baue(ort, geb, terrain)
            self.assertGreater(spielerhilfe.grundproduktion_erste_siedlung(self.z)[schluessel], 0)
            self.assertEqual(spielerhilfe.startaufgabe_pflicht(self.z), schluessel!='nahrung')

    def test_ungueltiger_oder_unproduktiver_bau_zahlt_nicht(self):
        ort = _erste_siedlung(self.z)
        ort.bauten['0'] = 'holzfaeller'  # Feld 0 kann Sumpf o.a. sein
        ort.bauten['999'] = 'jaeger'  # ausserhalb, darf niemals zaehlen
        self.assertTrue(spielerhilfe.startaufgabe_pflicht(self.z))
        self.assertEqual(spielerhilfe.grundproduktion_erste_siedlung(self.z)['nahrung'], 0)

    def test_weitere_siedlung_ersetzt_nicht_die_startversorgung(self):
        erste = _erste_siedlung(self.z)
        zweite = main.Settlement(name='Kolonie', map_id=self.z.current_map,
                                 karte=spieloekonomie.startkarte('kolonie','spieler'))
        for geb, gel in (('holzfaeller','wald'),('steinmetz','berg'),('jaeger','wald')):
            _baue(zweite, geb, gel)
        self.z.settlements.append(zweite)
        self.assertTrue(spielerhilfe.startaufgabe_pflicht(self.z))
        for geb, gel in (('holzfaeller','wald'),('steinmetz','berg'),('jaeger','wald')):
            _baue(erste, geb, gel)
        self.assertFalse(spielerhilfe.startaufgabe_pflicht(self.z))


class PflichtKarteGUI(unittest.TestCase):
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

    def karte_da(self):
        return 'Dein nächster Schritt' in _texte(self.app.content)

    def test_verpflichtend_trotz_admin_ausblenden_und_schutzende(self):
        admin_werkzeuge.spielerhilfe_modus_setzen(self.app.state,'ausblenden',freigabe=True)
        self.app.state.noob_protection = False
        self.app._spielerhilfe_anzeige_aktualisieren()
        self.assertFalse(self.app.hilfe_rahmen.winfo_manager())
        self.assertTrue(self.karte_da())
        self.app._switch_view('Lager')
        self.app._switch_view('Dorfzentrum')
        self.assertTrue(self.karte_da())
        self.assertTrue(any('Gründe zuerst eine Siedlung' in text for text in _texte(self.app.content)))

    def test_nach_drei_produktionen_wieder_admin_ausblenden(self):
        admin_werkzeuge.spielerhilfe_modus_setzen(self.app.state,'ausblenden',freigabe=True)
        ort = _erste_siedlung(self.app.state)
        self.app._spielerhilfe_anzeige_aktualisieren()
        self.assertTrue(self.karte_da())
        for geb, gel in (('holzfaeller','wald'),('steinmetz','berg'),('jaeger','wald')):
            _baue(ort,geb,gel)
        self.app._spielerhilfe_anzeige_aktualisieren()
        self.assertFalse(self.karte_da())
        self.app._switch_view('Dorfzentrum')
        self.assertFalse(self.karte_da())
        self.assertFalse(self.app.hilfe_rahmen.winfo_manager())
        self.app._switch_view('Anleitung')
        self.assertIn('Spielerhilfe', _texte(self.app.content))

    def test_auto_nach_grundversorgung_folgt_wieder_schutz(self):
        ort = _erste_siedlung(self.app.state)
        for geb, gel in (('holzfaeller','wald'),('steinmetz','berg'),('jaeger','wald')):
            _baue(ort,geb,gel)
        self.app._spielerhilfe_anzeige_aktualisieren()
        self.assertTrue(self.karte_da())
        self.app.state.noob_protection = False
        self.app._spielerhilfe_anzeige_aktualisieren()
        self.assertFalse(self.karte_da())

    def test_ausblenden_ohne_wechsel_keine_renderendlosschleife(self):
        admin_werkzeuge.spielerhilfe_modus_setzen(self.app.state,'ausblenden',freigabe=True)
        self.app._spielerhilfe_anzeige_aktualisieren()
        self.assertTrue(self.karte_da())
        original = self.app._render_view
        zaehler = []
        try:
            self.app._render_view = lambda: zaehler.append(1)
            for _ in range(12):
                self.app._spielerhilfe_anzeige_aktualisieren()
            self.assertEqual(zaehler, [])
        finally:
            self.app._render_view = original

if __name__ == '__main__':
    unittest.main(verbosity=2)
