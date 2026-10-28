"""GPT W-03: Bot-Überfälle rechnen gegen echte Ortswälle statt Gratisbeute.
Autor: ChatGPT, externer temporärer Koordinator. Testet bewusst MAIN-Anbindung.
"""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from main import GameState, BotPlayer, Settlement


def ort():
    return Settlement(name='Testdorf',map_id='kontinent',x=1,y=1,id='spieler:kontinent:1:1',
                      vorraete={'holz':100.,'stein':100.},einheiten={},bevoelkerung=10)


def bot_action(*args, **kwargs):
    return {'aktionen': {'Ulf': 'angreifen'}, 'nachrichten':[],
            'ergebnisse':[{'bot':'Ulf', 'aktion':'angreifen','meldung':'Ulf versucht einen Angriff.',
                           'wirkung':{'beute': {'holz':50},'angriffe':1,
                                     'naechster_angriff':30000, 'letzter_angriff':25000}}]}


class BotWallTests(unittest.TestCase):
    def setUp(self):
        self.state=GameState()
        self.s=ort()
        self.state.settlements=[self.s]
        self.state.noob_protection=False
        self.bot=BotPlayer(name='Ulf',faction='menschlich',aggression=1,trading=0,
                           army={'Bürgerwehr':1},lager={'Handkarren':1},vorraete={})
        self.state.bots=[self.bot]

    def test_kein_gratisangriff_mit_wall(self):
        self.state.research['Verteidigungsanlagen'].level=5
        self.s.mauer_besetzt=True
        vorher=dict(self.s.vorraete)
        with patch('main.botkern.bots_tick', side_effect=bot_action):
            self.state.bots_fortschreiben(25000)
        self.assertEqual(self.s.vorraete, vorher)
        self.assertNotIn('holz', self.bot.vorraete)  # keine Gratisbeute der alten Botlogik
        self.assertEqual(self.s.mauer_zustand,100)

    def test_ohne_fussvolk_keine_gratisbeute(self):
        self.bot.army={}
        vorher=dict(self.s.vorraete)
        with patch('main.botkern.bots_tick', side_effect=bot_action):
            self.state.bots_fortschreiben(25000)
        self.assertEqual(self.s.vorraete, vorher)
        self.assertNotIn('holz',self.bot.vorraete)

    def test_ohne_wall_und_verteidiger_ist_beute_moeglich(self):
        with patch('main.botkern.bots_tick', side_effect=bot_action):
            self.state.bots_fortschreiben(25000)
        self.assertLess(self.s.vorraete['holz'],100)
        self.assertGreater(self.bot.vorraete.get('holz',0),0)

    def test_botwall_dauerhaft_gespeichert(self):
        import tempfile, os
        self.bot.wall_stufe=5
        self.bot.wall_zustand=67.0
        with tempfile.TemporaryDirectory() as t:
            pfad=os.path.join(t,'botwall.json')
            self.assertTrue(self.state.save(pfad))
            andere=GameState()
            self.assertTrue(andere.load(pfad))
            geladen=next(b for b in andere.bots if b.name=='Ulf')
            self.assertEqual(geladen.wall_stufe,5)
            self.assertEqual(geladen.wall_zustand,67.0)

    def test_gotterschutz_bleibt_aktiv(self):
        self.state.noob_protection=True
        vorher=dict(self.s.vorraete)
        with patch('main.botkern.bots_tick', side_effect=bot_action):
            self.state.bots_fortschreiben(25000)
        self.assertEqual(self.s.vorraete,vorher)

if __name__=='__main__': unittest.main()
