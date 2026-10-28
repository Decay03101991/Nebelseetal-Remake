"""GPT-Z01: monotone echte Laufzeit; Datumsstempel nie als Wirtschaftsuhr.

Tests fuer Wallclock-Spruenge, Tageszeiten, Nachrichten, speichern/laden und
Originalproduktion. Keine externen Tools, kein Fenster, keine Passwoerter.
"""
import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
sys.path.insert(0,str(ROOT/'tools'))
import zeitbasis
import gpt_erzeuge_startstaende as vorlage


class TestRechnerzeit(unittest.TestCase):
    def test_monoton_unabhaengig_von_systemuhr(self):
        t=[100.0]
        lauf=zeitbasis.Laufzeituhr(lambda:t[0])
        with patch('time.time', return_value=17):
            t[0]=101.25
            self.assertAlmostEqual(lauf.vergangen(),1.25)
        with patch('time.time', return_value=999999999):
            t[0]=104.5
            self.assertAlmostEqual(lauf.vergangen(),3.25)

    def test_ruecksprung_nicht_negativ_und_kein_rueckstaueffekt(self):
        t=[40.0]
        l=zeitbasis.Laufzeituhr(lambda:t[0]);t[0]=35
        self.assertEqual(l.vergangen(),0)
        t[0]=36
        self.assertEqual(l.vergangen(),1)

    def test_paused_anker(self):
        t=[10.0]
        l=zeitbasis.Laufzeituhr(lambda:t[0]);t[0]=10000
        l.neu_ankern();t[0]=10001
        self.assertEqual(l.vergangen(),1)

    def test_utc_stamp_and_offset(self):
        stamp=zeitbasis.zeitmarke(datetime(2026,10,28,10,30,tzinfo=timezone(timedelta(hours=1))))
        self.assertEqual(stamp['zeit_utc'],'2026-10-28T09:30:00.000Z')
        self.assertTrue(datetime.fromisoformat(stamp['zeit_lokal']).tzinfo is not None)

    def test_naive_abgewiesen(self):
        with self.assertRaises(ValueError):
            zeitbasis.zeitmarke(datetime(2026,1,1))

    def test_neue_nachricht_einmal_gestempelt(self):
        liste=zeitbasis.NachrichtenMitZeit()
        original={'text':'Transport angekommen','type':'auftrag'}
        liste.append(original)
        self.assertNotIn('zeit_utc',original)
        self.assertEqual(len(liste),1)
        self.assertIn('zeit_utc',liste[0])
        self.assertIn('zeit_lokal',liste[0])
        self.assertEqual(liste[0]['text'],original['text'])

    def test_altnachricht_bleibt_ohne_erdachten_zeitpunkt(self):
        l=zeitbasis.NachrichtenMitZeit([{'text':'alt','type':'system'}]);
        self.assertNotIn('zeit_utc',l[0]);self.assertEqual(zeitbasis.zeitstempel_text(l[0]),'')

    def test_json_export(self):
        l=zeitbasis.NachrichtenMitZeit();l.extend([{'text':'eins'},{'text':'zwei'}]);
        assert len(l)==2
        self.assertEqual(len(json.loads(json.dumps(l))),2)
        self.assertTrue(all('zeit_utc' in v for v in l))

    def test_load_resets_realtime_clock_and_prevents_offline_tick(self):
        s=vorlage.neu_erzeugen()
        s.tick(3600)
        with tempfile.TemporaryDirectory() as d:
            p=os.path.join(d,'slot1.json')
            self.assertTrue(s.save(p))
            saved=json.load(open(p,encoding='utf-8'))
            self.assertIn('zeit_utc', saved)
            self.assertIn('zeit_lokal',saved)
            self.assertEqual(saved['spielsekunden'],3600)
            loaded=vorlage.neu_erzeugen()
            self.assertTrue(loaded.load(p))
            self.assertEqual(loaded.spielsekunden,3600)
            self.assertLess(loaded._laufzeituhr.vergangen(),3)

    def test_25h_tick_uses_one_source_for_economy_and_day(self):
        s=vorlage.neu_erzeugen()
        ort=s.settlements[0]
        s.tick(25*3600)
        self.assertEqual(s.day,2)
        self.assertEqual(s.spielsekunden,25*3600)
        self.assertEqual(ort.vorraete['holz'],125)
        self.assertEqual(ort.vorraete['stein'],125)

    def test_nachrichtenliste_im_spielstand_gestempelt(self):
        s=vorlage.neu_erzeugen()
        s.messages.append({'type':'test','text':'Zeitkontrolle'})
        self.assertIn('zeit_utc',s.messages[-1]);self.assertIn('zeit_lokal',s.messages[-1])


if __name__=='__main__':
    unittest.main(verbosity=2)
