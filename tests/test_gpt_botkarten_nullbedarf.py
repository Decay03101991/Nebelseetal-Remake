"""GPT-B03: Bot-Kartenwahl darf bei Null-/Fehlbedarf nicht abstuerzen."""
import sys
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import botkern
import spieloekonomie

class TestBotKarte(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frei=spieloekonomie.vorrat('botkarten-test')
        cls.eigen=[spieloekonomie.startkarte('botkarten-test','spieler')]
        cls.regeln=spieloekonomie.REGELN

    def waehle(self,bedarf,raten=None,stufe='mittel'):
        return botkern.oekonomie_kartenwahl(stufe,self.eigen,self.frei,
                                            raten or {},bedarf,self.regeln)

    def test_alle_null(self):
        self.assertIsNone(self.waehle({'holz':0,'stein':0}))

    def test_leerer_bedarf(self):
        self.assertIsNone(self.waehle({}))

    def test_ein_null_ein_positiv(self):
        self.assertIsInstance(self.waehle({'holz':0,'stein':100}),str)

    def test_null_auch_bei_vorhandener_rate(self):
        self.assertIsNone(self.waehle({'holz':0},{'holz':1000}))

    def test_nichtnumerisch_wird_ignoriert(self):
        self.assertIsNone(self.waehle({'stein':'unbekannt'}))

    def test_nan_und_inf_verursachen_keinen_crash(self):
        self.assertIsNone(self.waehle({'stein':float('nan'),'holz':float('inf')}))

    def test_negative_bedarfe_ausgeschlossen(self):
        self.assertIsNone(self.waehle({'holz':-10}))

    def test_determinismus_und_nicht_mutieren(self):
        b={'holz':100,'stein':150}; r={'holz':25,'stein':1}
        a=self.waehle(b,r)
        self.assertEqual(a,self.waehle(b,r))
        self.assertEqual(b,{'holz':100,'stein':150})
        self.assertEqual(r,{'holz':25,'stein':1})

    def test_leicht_gruendet_nicht(self):
        self.assertIsNone(self.waehle({'stein':100},stufe='leicht'))

if __name__=='__main__': unittest.main(verbosity=2)
