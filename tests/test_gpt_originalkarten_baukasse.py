# -*- coding: utf-8 -*-
"""GPT-FIX02b: Siedlungskarten-Baupruefung mit echtem 10x10-Originalbild.

Kein historisches 8x7-Raster, keine Reichsanzeige als Buchungskonto, kein
Admin-Modus; der GUI-Weg zur Bauaktion wird wirklich ausgefuehrt.
"""
import sys
import tkinter as tk
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import main  # noqa: E402


class TestOriginalkartenBaukasse(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = main.NebelseetalApp(self.root)
        self.app._build_main_ui()
        self.app._found_settlement()
        self.ort = self.app.state.settlements[0]
        self.app._oeffne_siedlungskarte(self.ort)
        self.root.update_idletasks()
        self.assertEqual((self.ort.karte['spalten'], self.ort.karte['zeilen']), (10, 10))
        self.assertEqual(len(self.ort.karte['raster']), 100)
        self.wald = self.ort.karte['raster'].index('wald')
        self.ort.vorraete.update({'holz': 500.0, 'stein': 500.0})
        self.ort.bevoelkerung = 100.0
        self.app.state._reichsanzeige_aus_orten()

    def tearDown(self):
        self.root.destroy()

    def _bau(self, feld, gebaeude):
        self.app._karten_feld_waehlen(feld)
        self.app._karten_bauen(gebaeude)
        self.root.update_idletasks()

    def test_holzfaeller_bucht_nur_ortsbestandskosten_und_siedler(self):
        kosten = main.baukosten('holzfaeller')
        vorher = dict(self.ort.vorraete)
        bevoelkerung = self.ort.bevoelkerung
        self._bau(self.wald, 'holzfaeller')
        self.assertEqual(self.ort.bauten.get(str(self.wald)), 'holzfaeller')
        self.assertEqual(self.ort.stufen.get(str(self.wald)), 1)
        self.assertEqual(self.ort.vorraete['holz'], vorher['holz'] - kosten['holz'])
        self.assertEqual(self.ort.vorraete['stein'], vorher['stein'] - kosten['stein'])
        self.assertEqual(self.ort.bevoelkerung, bevoelkerung - kosten['siedler'])
        self.assertEqual(self.app.state.resources['holz'].amount, self.ort.vorraete['holz'])
        self.assertEqual(self.app.state.resources['stein'].amount, self.ort.vorraete['stein'])
        self.assertEqual(self.app.karten_feld, self.wald)
        self.assertTrue(self.app.karten_canvas.find_withtag(f'feld:{self.wald}'))

    def test_belegtes_feld_wird_ohne_zweite_buchung_abgewiesen(self):
        self._bau(self.wald, 'holzfaeller')
        vorher = (dict(self.ort.bauten), dict(self.ort.vorraete), self.ort.bevoelkerung)
        self._bau(self.wald, 'holzfaeller')
        self.assertEqual((self.ort.bauten, self.ort.vorraete, self.ort.bevoelkerung), vorher)
        self.assertIn('Bau nicht moeglich', self.app.state.log[-1])

    def test_bau_ohne_rohstoffe_mutiert_keine_kasse_und_keinen_bauplatz(self):
        # Ersten Holzfaeller setzen; zweiten Waldplatz bewusst unterfinanzieren.
        self._bau(self.wald, 'holzfaeller')
        andere = next(i for i, art in enumerate(self.ort.karte['raster'])
                     if art == 'wald' and str(i) not in self.ort.bauten)
        self.ort.vorraete['holz'] = 0.0
        self.ort.vorraete['stein'] = 0.0
        self.app.state._reichsanzeige_aus_orten()
        vorher = (dict(self.ort.bauten), dict(self.ort.vorraete), self.ort.bevoelkerung)
        self._bau(andere, 'holzfaeller')
        self.assertEqual((self.ort.bauten, self.ort.vorraete, self.ort.bevoelkerung), vorher)
        self.assertTrue(any('Nicht genug' in zeile for zeile in self.app.state.log[-3:]))

    def test_urspruengliches_kartenbild_und_koordinaten_bleiben_nach_bau(self):
        self._bau(self.wald, 'holzfaeller')
        cv = self.app.karten_canvas
        self.assertEqual(len(cv.find_withtag('originalkarte')), 1)
        self.assertEqual(len(cv.find_withtag('kartenfeld')), 100)
        self.assertTrue(cv.find_withtag(f'feld:{self.wald}'))
        self.assertTrue(cv.find_withtag('auswahl'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
