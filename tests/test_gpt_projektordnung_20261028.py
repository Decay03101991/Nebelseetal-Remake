"""Prueft Pfade und die einzige aktive Entwicklungschronik der Konsolidierung."""
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class ProjektOrdnung(unittest.TestCase):
 def test_nur_ein_aktives_protokoll(self):
  self.assertEqual([p.name for p in (ROOT/'docs').glob('*ENTWICKLUNGSPROTOKOLL*.md')],['ENTWICKLUNGSPROTOKOLL.md'])
 def test_aktives_spiel(self):
  for p in ['src/main.py','data/gelaende.json','assets/loadingpage/Nebelseetal_Loadingpage.png','docs/AGENTEN_PLAN.md','docs/ENTWICKLUNGSPROTOKOLL.md','docs/HERMES_UEBERGABE_AKTUELL.md']:
   self.assertTrue((ROOT/p).is_file(),p)
 def test_bildquellen_vorhanden(self):
  for p in ['assets/quellbilder/Nebelseetal_Loadingpage.jpg','assets/quellbilder/nebelseetal.png','assets/quellbilder/waren/WaffenWerkzeuge_Icons.png','assets/quellbilder/einheiten/Nahkämpfer_Icons.png','docs/nebelseetal_gamestar2.jpg']:
   self.assertTrue((ROOT/p).is_file(),p)
 def test_archiv_github_ausgeschlossen(self):
  self.assertIn('/archiv/', (ROOT/'.gitignore').read_text('utf-8'))
 def test_alter_stand_archiviert(self):
  self.assertTrue((ROOT/'archiv/altstaende/HERMES_HAUPTSTAND_VOR_GPT_KONSOLIDIERUNG_2026-10-28.zip').is_file())
if __name__=='__main__': unittest.main()
