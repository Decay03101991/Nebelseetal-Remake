"""GPT-Z03: echter GameState-Transport, Zeitstempel bei grossen Zeitspruengen."""
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'tools')]
import main
import gpt_erzeuge_startstaende

class TestZeitAuftrag(unittest.TestCase):
    def test_ankunft_und_heimkehr_als_eigene_ereignisse(self):
        g=gpt_erzeuge_startstaende.neu_erzeugen()
        ort=g.settlements[0]
        ort.einheiten['Handkarren']=1
        ziel=main.Settlement(id='gpt:zweiter-ort',name='Zeit-Kolonie',
                             map_id=ort.map_id,x=ort.x+1,y=ort.y,
                             besitzer='spieler',dimension=ort.dimension,
                             karte=ort.karte.copy(),vorraete={'holz':0.0,'stein':0.0},
                             bevoelkerung=10)
        g.settlements.append(ziel)
        self.assertEqual(ort.vorraete['stein'],100)
        ok, meld=g.transport_an_ort(ort,ziel,'stein',10,{'Handkarren':1})
        self.assertTrue(ok,meld)
        mission=next(e for e in g.auftraege if e.get('eigentransport'))
        ankunft=float(mission['ankunft'])
        heimkehr=float(mission['rueckkehr'])
        self.assertGreater(heimkehr,ankunft)
        self.assertEqual(ort.vorraete['stein'],90)
        self.assertEqual(ziel.vorraete['stein'],0)
        # Eine grosse Tick-Spanne muss beide Buchungen genau einmal erledigen.
        g.tick(heimkehr+100)
        arriv=[v for v in g.messages if v.get('text','').startswith('Transport angekommen')]
        ret=[v for v in g.messages if v.get('text','').startswith('Transport heimgekehrt')]
        self.assertEqual(len(arriv),1)
        self.assertEqual(len(ret),1)
        self.assertAlmostEqual(arriv[0]['spielzeit_sekunden'],ankunft)
        self.assertAlmostEqual(ret[0]['spielzeit_sekunden'],heimkehr)
        for v in (arriv[0],ret[0]):
            self.assertIn('zeit_utc',v)
            self.assertIn('zeit_lokal',v)
        self.assertEqual(ziel.vorraete['stein'],10 + (heimkehr+100)/3600)
        self.assertEqual(ort.einheiten.get('Handkarren'),1)
        g.tick(10)
        self.assertEqual(len([v for v in g.messages if v.get('text','').startswith('Transport heimgekehrt')]),1)

if __name__=='__main__':unittest.main(verbosity=2)
