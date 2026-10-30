"""Eigenstaendiger Regressionstest der externen Wall-Zuarbeit.

Aufruf (aus Projektwurzel): python -X utf8 tests/test_gpt_dorfwall.py
"""
from __future__ import annotations
import copy
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import dorfwall as DW


class DorfwallPruefungen(unittest.TestCase):
    def setUp(self):
        self.s = {'bauten': {'0': 'holzfaeller'}, 'mauer_besetzt': False}
        self.f = {'Verteidigungsanlagen': 4, 'Mauerbau': 10}
        self.lager = {'holz': 20.0, 'stein': 20.0}
        self.preis = {'holz': 16, 'stein': 16, 'budget': 'VORSCHLAG'}

    def test_ohne_wache_keine_mauer(self):
        self.assertEqual(DW.stufe(self.s, self.f), 0)

    def test_forschung_mauerbau_allein_nicht_freischalten(self):
        self.assertEqual(DW.forschungsstand({'Mauerbau': 10}), 0)

    def test_ohne_forschung_keine_aktivierung_keine_abbuchung(self):
        vorher = copy.deepcopy((self.s, self.lager))
        ok, _ = DW.wache_besetzen(self.s, {}, self.lager, self.preis)
        self.assertFalse(ok)
        self.assertEqual((self.s, self.lager), vorher)

    def test_aktivierung_bezahlt_nur_lokal_kein_bauplatz(self):
        ok, _ = DW.wache_besetzen(self.s, self.f, self.lager, self.preis)
        self.assertTrue(ok)
        self.assertEqual(self.s['bauten'], {'0': 'holzfaeller'})
        self.assertEqual(self.lager, {'holz': 4.0, 'stein': 4.0})
        self.assertEqual(DW.stufe(self.s, self.f), 4)

    def test_keine_freien_ressourcen_bei_unterdeckung(self):
        self.lager['stein'] = 15
        vorher = copy.deepcopy((self.s, self.lager))
        ok, _ = DW.wache_besetzen(self.s, self.f, self.lager, self.preis)
        self.assertFalse(ok)
        self.assertEqual((self.s, self.lager), vorher)

    def test_keine_doppelabbuchung(self):
        self.assertTrue(DW.wache_besetzen(self.s, self.f, self.lager, self.preis)[0])
        vorher = copy.deepcopy(self.lager)
        self.assertFalse(DW.wache_besetzen(self.s, self.f, self.lager, self.preis)[0])
        self.assertEqual(self.lager, vorher)

    def test_automatisches_upgrade_nach_forschung(self):
        DW.wache_besetzen(self.s, self.f, self.lager, self.preis)
        self.f['Verteidigungsanlagen'] = 7
        self.assertEqual(DW.stufe(self.s, self.f), 7)
        self.assertEqual(DW.kennwerte(self.s, self.f)['belagerungswaffen'], 700)

    def test_jeder_ort_hat_eigenen_status(self):
        anderes = {'mauer_besetzt': False}
        DW.wache_besetzen(self.s, self.f, self.lager, self.preis)
        self.assertEqual(DW.stufe(anderes, self.f), 0)

    def test_wall_4_ohne_belagerungszwang(self):
        DW.wache_besetzen(self.s, self.f, self.lager, self.preis)
        self.assertIsNone(DW.kennwerte(self.s, self.f)['belagerungswaffen'])
        self.assertEqual(DW.kennwerte(self.s, self.f)['fusstruppen'], 160)

    def test_wall_5_erst_mit_belagerung(self):
        self.f['Verteidigungsanlagen'] = 5
        DW.wache_besetzen(self.s, self.f, self.lager, self.preis)
        self.assertEqual(DW.kennwerte(self.s, self.f)['belagerungswaffen'], 500)

    def test_mauerzustand_pro_siedlung(self):
        DW.wache_besetzen(self.s, self.f, self.lager, self.preis)
        self.s['mauer_zustand'] = 34.0
        self.assertEqual(DW.kennwerte(self.s, self.f)['zustand_prozent'], 34.0)
        self.assertEqual(DW.zustand({}), 100.0)

    def test_ueberhoehte_forschungsstufen_begrenzt(self):
        self.assertEqual(DW.forschungsstand({'Verteidigungsanlagen': {'level': 999}}), 10)
        self.assertEqual(DW.forschungsstand({'Verteidigungsanlagen': -4}), 0)

    def test_zustand_serialisierbar(self):
        DW.wache_besetzen(self.s, self.f, self.lager, self.preis)
        self.assertEqual(json.loads(json.dumps(self.s))['mauer_besetzt'], True)

    def test_kartenrahmen_ohne_mauer_leer(self):
        self.assertEqual(DW.rahmen_plan(8, 7, 64, 18, 0), [])

    def test_kartenrahmen_sichtbar_mit_tor(self):
        formen = DW.rahmen_plan(8, 7, 64, 18, 5)
        self.assertEqual(len(formen), 5)
        self.assertTrue(all(f['breite'] == 7 for f in formen))
        self.assertTrue(formen[3]['linie'][2] < formen[4]['linie'][0])


if __name__ == '__main__':
    unittest.main(verbosity=2)
