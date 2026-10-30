"""Originalkarten: echte GameState-Persistenz und bewusst abgewiesene alte Siedlungen."""
import tempfile, sys, json
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from main import GameState, Settlement
import originalkarten

class KartenSpeicher(unittest.TestCase):
 def test_originalkarte_bleibt_beim_laden_gleich(self):
  original=GameState()
  k=originalkarten.startkarte('roundtrip','spieler')
  s=Settlement(name='Neustadt',map_id='kontinent',x=1,y=1,karte=k,
               id='spieler:kontinent:1:1',vorraete={'holz':100.0,'stein':100.0},bevoelkerung=10)
  original.settlements=[s]
  with tempfile.TemporaryDirectory() as t:
   p=str(Path(t)/'slot.json')
   self.assertTrue(original.save(p))
   copy=GameState()
   self.assertTrue(copy.load(p))
   self.assertEqual(copy.settlements[0].karte['originalkarte_id'],k['originalkarte_id'])
   self.assertEqual(copy.settlements[0].karte['raster'],k['raster'])

 def test_legacy_karte_lehnt_vor_mutation_ab(self):
  original=GameState()
  s=Settlement(name='Altstadt',map_id='kontinent',x=1,y=1,karte={'spalten':8,'zeilen':7,'raster':['wald']*56},id='spieler:kontinent:1:1',
               vorraete={'holz':50.0,'stein':50.0},bevoelkerung=10)
  original.settlements=[s]
  with tempfile.TemporaryDirectory() as t:
   p=str(Path(t)/'slot.json')
   self.assertTrue(original.save(p))
   copy=GameState()
   copy.population=999
   self.assertFalse(copy.load(p))
   self.assertEqual(copy.population,999)
   self.assertEqual(len(copy.settlements),0)

if __name__=='__main__':unittest.main(verbosity=2)
