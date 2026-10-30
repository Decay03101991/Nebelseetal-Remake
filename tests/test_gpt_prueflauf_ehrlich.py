"""Externe GPT-Pruefung: Kinder-Pruefungen duerfen nicht 'falsch gruen' sein."""
import os,sys,unittest
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','tools'))
import gpt_prueflauf_ehrlich as P

class ParserTests(unittest.TestCase):
 def test_erkennt_false_green(self):
  t='ERGEBNIS: 19 bestanden, 5 Fehler, 0 Befunde'
  self.assertFalse(P.prueftext(t,0)[0])
 def test_gruen_wirklich_gruen(self):
  self.assertTrue(P.prueftext('ERGEBNIS: 42 bestanden, 0 Fehler, 2 Befunde',0)[0])
 def test_befunde_sind_keine_fehler(self):
  self.assertEqual(P.prueftext('ERGEBNIS: 1 bestanden, 0 Fehler, 22 Befunde',0)[2],0)
 def test_unittest_ok(self):
  self.assertTrue(P.prueftext('Ran 5 tests in 0.004s\n\nOK\n',0)[0])
 def test_unittest_fehler(self):
  self.assertFalse(P.prueftext('Ran 5 tests in 0.004s\n\nFAILED (failures=1)\n',0)[0])
 def test_nur_rc_0_nicht_genug(self):
  self.assertFalse(P.prueftext('Tests laufen fertig',0)[0])
 def test_rc_1_bei_text_gruen_rot(self):
  self.assertFalse(P.prueftext('ERGEBNIS: 42 bestanden, 0 Fehler, 0 Befunde',1)[0])

if __name__=='__main__':unittest.main(verbosity=2)
