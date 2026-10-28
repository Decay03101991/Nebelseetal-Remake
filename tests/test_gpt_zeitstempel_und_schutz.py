"""GPT-Z02: Nachrichtentimestamp und Spielzeit sind getrennt, finite validiert."""
from __future__ import annotations
import json
import math
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT / 'tools'))
import zeitbasis
import spielzeit
import gpt_erzeuge_startstaende as start


class TestSpielzeitStempel(unittest.TestCase):
    def test_nachricht_fuehrt_spielsekunden_und_utc(self):
        s = start.neu_erzeugen()
        s.tick(3600)
        s.messages.append({'text': 'Test', 'type': 'probe'})
        self.assertEqual(s.messages[-1]['spielzeit_sekunden'], 3600)
        self.assertIn('zeit_utc', s.messages[-1])
        self.assertIn('zeit_lokal', s.messages[-1])
        self.assertEqual(s.messages[-1]['zeit_utc'][-1], 'Z')

    def test_nachricht_spielzeit_bleibt_beim_laden(self):
        s = start.neu_erzeugen()
        s.tick(60)
        s.messages.append({'text':'Transport-Start'})
        with tempfile.TemporaryDirectory() as d:
            datei = os.path.join(d, 'slot1.json')
            self.assertTrue(s.save(datei))
            with open(datei, encoding='utf8') as f:
                daten = json.load(f)
            self.assertEqual(daten['messages'][-1]['spielzeit_sekunden'], 60)
            neu = start.neu_erzeugen()
            self.assertTrue(neu.load(datei))
            self.assertEqual(neu.messages[-1]['spielzeit_sekunden'], 60)
            neu.tick(100)
            neu.messages.append({'text':'Transport-Ankunft'})
            self.assertEqual(neu.messages[-1]['spielzeit_sekunden'], 160)
            self.assertEqual(neu.messages[-2]['spielzeit_sekunden'], 60)

    def test_vorhandene_altnachricht_wird_nicht_umgestempelt(self):
        l = zeitbasis.NachrichtenMitZeit([{'text':'historisch'}], spieluhr=lambda:80)
        self.assertEqual(l[0],{'text':'historisch'})
        l.append({'text':'neu'})
        self.assertEqual(l[-1]['spielzeit_sekunden'],80)

    def test_importierte_zeitstempel_nicht_ueberschreiben(self):
        original = {'text':'gesichert','zeit_utc':'2020-01-01T00:00:00Z','zeit_lokal':'2020-01-01T01:00:00+01:00', 'spielzeit_sekunden':900}
        l=zeitbasis.NachrichtenMitZeit(spieluhr=lambda:10)
        l.append(original)
        self.assertEqual(l[0],original)

    def test_nan_inf_und_negative_ticks_abgelehnt(self):
        s = start.neu_erzeugen()
        for wert in (float('nan'),float('inf'),float('-inf'),-1):
            with self.subTest(wert=wert):
                with self.assertRaises(ValueError):s.tick(wert)
                self.assertEqual(s.spielsekunden,0)

    def test_monotone_nichtendliche_anker_abgewiesen(self):
        with self.assertRaises(ValueError):zeitbasis.Laufzeituhr(lambda: float('nan'))
        zeit=[1]
        l=zeitbasis.Laufzeituhr(lambda:zeit[0]); zeit[0]=float('inf')
        with self.assertRaises(ValueError):l.vergangen()
        with self.assertRaises(ValueError):l.neu_ankern()

    def test_nan_unterbrechung_keine_geschenkte_zeit(self):
        zeit=[1.0]
        l=zeitbasis.Laufzeituhr(lambda: zeit[0])
        zeit[0]=float('nan')
        with self.assertRaises(ValueError):l.vergangen()
        zeit[0]=3.0
        self.assertEqual(l.vergangen(),2.0)

    def test_spielzeittempo_unendliche_datei_abgefangen(self):
        spielzeit.vergessen()
        with patch.object(spielzeit,'daten', return_value={'faktor':float('inf')}):
            self.assertEqual(spielzeit.faktor(),spielzeit.STANDARD_FAKTOR)
        spielzeit.vergessen()

    def test_spielzeittempo_setzen_nan_ignoriert(self):
        spielzeit.vergessen()
        with patch.object(spielzeit,'faktor', return_value=180.0):
            self.assertEqual(spielzeit.setzen(float('nan')), 180.0)
            self.assertEqual(spielzeit.setzen(float('inf')), 180.0)

if __name__=='__main__':unittest.main(verbosity=2)
