# -*- coding: utf-8 -*-
"""FIX04b: Ertragsorientierte Spielerhilfe im Baumenue; ohne Regelmutation."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import baumenue_info  # noqa: E402
import gelaende  # noqa: E402


class StandorttippRegeln(unittest.TestCase):
    def test_holzfaeller_wald_statt_steppe(self):
        self.assertIn('Hoechstertrag', baumenue_info.standort_hinweis('holzfaeller', 'wald'))
        tipp = baumenue_info.standort_hinweis('holzfaeller', 'steppe')
        self.assertIn('Wald', tipp)
        self.assertIn('4', tipp)
        self.assertIn('2', tipp)

    def test_steinmetz_berg_und_farm_grasland(self):
        self.assertIn('Berg', baumenue_info.standort_hinweis('steinmetz', 'huegel'))
        self.assertIn('Grasland', baumenue_info.standort_hinweis('farm', 'steppe'))

    def test_nebelsee_tempel_und_jaeger(self):
        self.assertIn('Nebelsee', baumenue_info.standort_hinweis('tempel', 'grasland'))
        self.assertIn('Wald', baumenue_info.standort_hinweis('jaeger', 'steppe'))

    def test_bibliothek_steppe_statt_agrar_oder_tempel(self):
        self.assertIn('Steppe', baumenue_info.standort_hinweis('bibliothek', 'grasland'))
        self.assertIn('Steppe', baumenue_info.standort_hinweis('bibliothek', 'steppe'))
        self.assertIn('Steppe', baumenue_info.standort_hinweis('bibliothek', 'nebelsee'))

    def test_keine_falschen_steppe_empfehlungen(self):
        # Schmiede ist zwar auf Steppe erlaubt; wo das nicht zutrifft,
        # darf kein unmoeglicher Standort empfohlen werden.
        self.assertNotIn('lieber dort', baumenue_info.standort_hinweis('holzfaeller', 'wald'))
        self.assertEqual('', baumenue_info.standort_hinweis('bibliothek', 'wald'))
        self.assertEqual('', baumenue_info.standort_hinweis('bibliothek', 'sumpf'))

    def test_hinweis_aendert_keine_regeldaten(self):
        vorher = gelaende.alle_gebaeude()
        for k in vorher:
            for art in gelaende.GELAENDEARTEN:
                baumenue_info.standort_hinweis(k, art)
        self.assertEqual(vorher, gelaende.alle_gebaeude())


if __name__ == '__main__':
    unittest.main(verbosity=2)
