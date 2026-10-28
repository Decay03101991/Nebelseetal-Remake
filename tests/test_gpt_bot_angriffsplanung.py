"""GPT-B01: Original-SK/Belagerung und echte Botberichte (externer GPT-Agent)."""
from __future__ import annotations
import copy
import random
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import bot_angriffsplanung as A
from main import BotPlayer, GameState, Settlement


def ort(name, x, stufe=0, besetzt=True, truppen=None):
    s = Settlement(name=name, map_id='kontinent', x=x, y=2,
                   id=f'spieler:kontinent:{x}:2',
                   vorraete={'holz': 100.0, 'stein': 100.0},
                   einheiten=truppen or {}, bevoelkerung=10.0,
                   mauer_besetzt=besetzt)
    s._test_wall = stufe
    return s


def bot_zug(*a, **kw):
    return {'aktionen': {'angreifen': 1},
            'ergebnisse': [{'bot':'Pruefbot', 'aktion':'angreifen',
                            'meldung':'FEHLER: Bot erbeutet bereits 50 Holz',
                            'wirkung':{'beute': {'holz':50},'angriffe':1,
                                       'naechster_angriff':50000.0, 'letzter_angriff':25000.0}}],
            'nachrichten':['FEHLER: Bot erbeutet bereits 50 Holz']}


class PlanungTests(unittest.TestCase):
    def test_wall_ohne_belagerung(self):
        p=A.pruefe_vorrunde({'Bürgerwehr': 100}, {}, 5)
        self.assertFalse(p['moeglich'])
        self.assertIn('Belagerungs', p['grund'])

    def test_ohne_wall_mit_truppe(self):
        self.assertTrue(A.pruefe_vorrunde({'Bürgerwehr':1},{},0)['moeglich'])

    def test_ohne_fusstruppen_trotz_geschuetz(self):
        self.assertFalse(A.pruefe_vorrunde({}, {'Katapult':10},0)['moeglich'])

    def test_exakte_originalwerte(self):
        p=A.pruefe_vorrunde({'Bürgerwehr': 10}, {}, 1)
        self.assertTrue(p['moeglich'])
        self.assertEqual(p['sk']['fusstruppen'], 10)
        self.assertEqual(p['schwelle']['fusstruppen'], 10)

    def test_stufe5_original_geratewerte(self):
        p=A.pruefe_vorrunde({'Bürgerwehr':250},{'Großes Katapult':10},5)
        # Geraete-SK ist Originalwert 55 -> 550
        self.assertTrue(p['moeglich'])
        self.assertEqual(p['sk']['belagerungswaffen'], 550)
        self.assertEqual(p['schwelle']['belagerungswaffen'], 500)

    def test_beschaedigung_halbiert_schwellen(self):
        p=A.pruefe_vorrunde({'Bürgerwehr':125}, {'Großes Katapult':5},5,50)
        self.assertTrue(p['moeglich'])
        self.assertEqual(p['schwelle'], {'fusstruppen':125.0,'belagerungswaffen':250.0})

    def test_transportkarren_kein_belagerungsgeraet(self):
        p=A.pruefe_vorrunde({'Bürgerwehr':250},{'Handkarren':100},5)
        self.assertFalse(p['moeglich'])
        self.assertEqual(p['sk']['belagerungswaffen'],0)

    def test_auswahl_waehlt_leichteren_wall(self):
        hoch=ort('Hoch',1,6)
        niedrig=ort('Niedrig',2,0,False)
        ziel, _=A.waehle_ziel([hoch,niedrig], {'Bürgerwehr':5}, {},
                              lambda s:(s._test_wall,100))
        self.assertIs(ziel,niedrig)

    def test_keiner_ueberwindbar(self):
        ziel, d=A.waehle_ziel([ort('Feste',1,10)], {'Bürgerwehr':2}, {},
                              lambda s:(s._test_wall,100))
        self.assertIsNone(ziel)
        self.assertFalse(d['moeglich'])

    def test_reinheit_der_planung(self):
        truppen={'Bürgerwehr':10}
        vor=copy.deepcopy(truppen)
        A.pruefe_vorrunde(truppen,{},1)
        self.assertEqual(truppen,vor)


class BotIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.g=GameState()
        self.g.noob_protection=False
        self.g.settlements=[ort('Stark',1),ort('Schwach',2,besetzt=False)]
        self.g.bots=[BotPlayer(name='Pruefbot',faction='menschlich',aggression=1,
                               trading=0,army={'Bürgerwehr':10},
                               lager={'Handkarren':1}, vorraete={})]

    def _run(self):
        with patch('main.botkern.bots_tick', side_effect=bot_zug):
            with patch.object(self.g,'bot_armee_aufstellen', return_value=None):
                return self.g.bots_fortschreiben(25000)

    def test_kein_phantombericht_nach_blockade(self):
        self.g.noob_protection=True
        self._run()
        self.assertFalse(any('FEHLER:' in t for t in self.g.log))
        self.assertFalse(any('erbeutet' in t for t in self.g.log))
        self.assertEqual(self.g.bots[0].vorraete,{})

    def test_schutz_nochmals_wirksam(self):
        self.g.noob_protection=True
        vorher=[dict(s.vorraete) for s in self.g.settlements]
        self._run()
        self.assertEqual(vorher,[s.vorraete for s in self.g.settlements])

    def test_auswahl_realistisch_nicht_erstes_dorf(self):
        self.g.research['Verteidigungsanlagen'].level=5
        self.g.settlements[0].mauer_besetzt=True
        vorher=dict(self.g.settlements[0].vorraete)
        self._run()
        self.assertEqual(self.g.settlements[0].vorraete,vorher)
        self.assertTrue(any('Schwach' in t for t in self.g.log))

    def test_kein_bot_heer_keine_illusion_beute(self):
        self.g.bots[0].army={}
        self._run()
        self.assertEqual(self.g.bots[0].vorraete,{})
        self.assertTrue(any('verschoben' in t for t in self.g.log))

    def test_sortierte_botantwort_niemals_falschem_bot_zubuchen(self):
        # Das echte botkern.bots_tick sortiert seine Ergebnisse alphabetisch.
        # Die BotPlayer-Liste darf in anderer Reihenfolge gespeichert sein.
        self.g.bots = [
            BotPlayer(name='Zulu', faction='menschlich', aggression=0,
                      trading=0, vorraete={'holz':100}),
            BotPlayer(name='Alpha', faction='menschlich', aggression=0,
                      trading=0, vorraete={'holz':200}),
        ]
        def sortiert(*_a, **_kw):
            return {'aktionen': {'warten':2}, 'nachrichten': [], 'ergebnisse': [
                {'bot':'Alpha', 'aktion':'warten', 'meldung':'Alpha wartet',
                 'wirkung': {'naechster_angriff':1111}},
                {'bot':'Zulu', 'aktion':'warten', 'meldung':'Zulu wartet',
                 'wirkung': {'naechster_angriff':2222}},
            ]}
        with patch('main.botkern.bots_tick', side_effect=sortiert), \
             patch.object(self.g, 'bot_armee_aufstellen', return_value=None):
            self.g.bots_fortschreiben(25000)
        self.assertEqual(self.g.bots[0].naechster_angriff,2222)
        self.assertEqual(self.g.bots[1].naechster_angriff,1111)
        self.assertEqual(self.g.bots[0].vorraete,{'holz':100})
        self.assertEqual(self.g.bots[1].vorraete,{'holz':200})

    def test_keine_prognose_aus_botkern_uebernehmen(self):
        self.g.settlements=[ort('Stark',1)]
        self.g.research['Verteidigungsanlagen'].level=5
        self.g.settlements[0].mauer_besetzt=True
        self._run()
        self.assertEqual(self.g.bots[0].vorraete,{})
        self.assertFalse(any('FEHLER:' in t for t in self.g.log))


if __name__ == '__main__':
    unittest.main()
