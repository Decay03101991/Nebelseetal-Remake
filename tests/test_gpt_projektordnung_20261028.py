"""Prueft Pfade und die einzige aktive Entwicklungschronik der Konsolidierung."""
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class ProjektOrdnung(unittest.TestCase):
 def test_nur_ein_aktives_protokoll(self):
  # ENTSCHEIDUNG Daniel 02.11.2026: das Protokoll liegt in ZWEI Heften - ein AKTIVES Heft und ein
  # GESCHLOSSENES Geschichtsheft.
  # ENTSCHEIDUNG Daniel 05.11.2026 (Frage 4, Register 218): AUSLAGERN statt verdichten - es duerfen
  # deshalb MEHRERE Historienhefte (`..._HISTORIE*.md`) daneben liegen. Die Wache haelt weiter fest,
  # was sie soll: genau EIN aktives Heft, und alles andere, was wie ein Protokoll heisst, ist ein
  # Historienheft. Eine feste Zahl waere hier falsch - sie wuerde jede Auslagerung rot machen.
  namen = sorted(p.name for p in (ROOT/'docs').glob('*ENTWICKLUNGSPROTOKOLL*.md'))
  self.assertIn('ENTWICKLUNGSPROTOKOLL.md', namen)
  andere = [n for n in namen if n != 'ENTWICKLUNGSPROTOKOLL.md']
  self.assertTrue(andere, 'kein Historienheft gefunden')
  for n in andere:
   self.assertIn('_HISTORIE', n, n)
 def test_aktives_spiel(self):
  for p in ['src/main.py','data/gelaende.json','assets/loadingpage/Nebelseetal_Loadingpage.png','docs/AGENTEN_PLAN.md','docs/ENTWICKLUNGSPROTOKOLL.md','docs/HERMES_UEBERGABE_AKTUELL.md']:
   self.assertTrue((ROOT/p).is_file(),p)
 def test_bildquellen_vorhanden(self):
  # docs/nebelseetal_gamestar2.jpg ist am 11.11.2026 mit den Originalquellen aus dem oeffentlichen
  # Stand genommen (Register 407) und liegt lokal unter archiv/originalquellen_20261111/.
  for p in ['assets/quellbilder/Nebelseetal_Loadingpage.jpg','assets/quellbilder/nebelseetal.png','assets/quellbilder/waren/WaffenWerkzeuge_Icons.png','assets/quellbilder/einheiten/Nahkämpfer_Icons.png']:
   self.assertTrue((ROOT/p).is_file(),p)
 def test_archiv_github_ausgeschlossen(self):
  self.assertIn('/archiv/', (ROOT/'.gitignore').read_text('utf-8'))
 def test_alter_stand_archiviert(self):
  self.assertTrue((ROOT/'archiv/altstaende/HERMES_HAUPTSTAND_VOR_GPT_KONSOLIDIERUNG_2026-10-28.zip').is_file())
if __name__=='__main__': unittest.main()
