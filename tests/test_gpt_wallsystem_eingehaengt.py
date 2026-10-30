"""GPT W-02: echte Integration Ortswall in GameState, Karte, Buchung, Punkte, Save/Load.
Autor: ChatGPT externer Entwicklungsagent, 28.10.2026. Keine Originalwerte verändert.
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from main import GameState, Settlement, bauen_auf_karte, baukosten
import dorfwall
import originalkarten


def neuer_ort(name, x):
    karte = originalkarten.startkarte('wall-test:'+str(x), 'spieler')
    return Settlement(name=name, map_id='kontinent', x=x, y=1,
                      id=f'spieler:kontinent:{x}:1', karte=karte,
                      vorraete={'holz': 50., 'stein': 50.}, bevoelkerung=10)


class EingehaengterWall(unittest.TestCase):
    def setUp(self):
        self.state = GameState()
        self.a, self.b = neuer_ort('A', 1), neuer_ort('B', 2)
        self.state.settlements = [self.a, self.b]
        self.state.research['Verteidigungsanlagen'].level = 4
        self.assertTrue(self.state._lokale_kasse_aktiv())

    def test_zwei_ortswaelle_statt_maximalwall(self):
        self.assertTrue(self.state.wall_errichten(self.a)[0])
        self.assertEqual(self.state.wall_stufe_am_ort(self.a), 4)
        self.assertEqual(self.state.wall_stufe_am_ort(self.b), 0)
        self.assertEqual(self.state.wall_kriegspunkte(), 64)
        self.assertTrue(self.state.wall_errichten(self.b)[0])
        self.assertEqual(self.state.wall_kriegspunkte(), 128)
        self.assertEqual(self.state.punktestand()['krieg'], 128)
        self.assertEqual(self.a.bauten, {})
        self.assertEqual(self.b.bauten, {})

    def test_neuerrichtung_verwendet_lokale_kasse(self):
        preis = baukosten('verteidigungswall')
        self.assertEqual(preis, {'holz': 16, 'stein': 16})
        vor_a = dict(self.a.vorraete)
        vor_b = dict(self.b.vorraete)
        self.assertTrue(self.state.wall_errichten(self.a)[0])
        self.assertEqual(self.a.vorraete['holz'], vor_a['holz'] - preis['holz'])
        self.assertEqual(self.a.vorraete['stein'], vor_a['stein'] - preis['stein'])
        self.assertEqual(self.b.vorraete, vor_b)

    def test_kein_doppelbau_keine_doppelzahlung(self):
        self.assertTrue(self.state.wall_errichten(self.a)[0])
        davor = dict(self.a.vorraete)
        self.assertFalse(self.state.wall_errichten(self.a)[0])
        self.assertEqual(self.a.vorraete, davor)

    def test_mangel_kein_ortsfremder_zugriff(self):
        self.a.vorraete['stein'] = 0
        vorher = dict(self.a.vorraete)
        ok, _ = self.state.wall_errichten(self.a)
        self.assertFalse(ok)
        self.assertEqual(self.a.vorraete, vorher)
        self.assertFalse(self.a.mauer_besetzt)

    def test_forschungsstufe_null_sperrt(self):
        self.state.research['Verteidigungsanlagen'].level = 0
        ok, _ = self.state.wall_errichten(self.a)
        self.assertFalse(ok)
        self.assertFalse(self.a.mauer_besetzt)

    def test_automatischer_ausbau_ohne_neue_abbuchung(self):
        self.assertTrue(self.state.wall_errichten(self.a)[0])
        nach_bau = dict(self.a.vorraete)
        self.state.research['Verteidigungsanlagen'].level = 5
        self.assertEqual(self.state.wall_stufe_am_ort(self.a), 5)
        self.assertEqual(self.state.wall_kriegspunkte(), 125)
        self.assertEqual(self.a.vorraete, nach_bau)
        self.assertEqual(dorfwall.kennwerte(self.a, self.state.research)['belagerungswaffen'], 500)

    def test_legacy_nicht_stillschweigend_migriert(self):
        self.a.bauten['0'] = 'verteidigungswall'
        self.a.stufen['0'] = 3
        self.state.mode = 'legacy'
        self.assertEqual(self.state.wall_stufe_am_ort(self.a), 3)
        self.assertEqual(self.state.wall_kriegspunkte(), 27)
        self.assertFalse(self.state.wall_errichten(self.a)[0])

    def test_neuer_spielstand_roundtrip(self):
        self.assertTrue(self.state.wall_errichten(self.a)[0])
        self.a.mauer_zustand = 37.5
        with tempfile.TemporaryDirectory() as t:
            path = os.path.join(t, 'save.json')
            self.assertTrue(self.state.save(path))
            neu = GameState()
            self.assertTrue(neu.load(path))
            self.assertTrue(neu.settlements[0].mauer_besetzt)
            self.assertEqual(neu.settlements[0].mauer_zustand, 37.5)
            self.assertEqual(neu.wall_stufe_am_ort(neu.settlements[0]), 4)

    def test_neumodus_keine_wallplatzierung_ueber_gui(self):
        # Die API bleibt nur fuer Alt-Builds erreichbar; die neue GUI sperrt sie.
        self.assertFalse(self.a.mauer_besetzt)
        self.assertFalse('0' in self.a.bauten)


if __name__ == '__main__':
    unittest.main()
