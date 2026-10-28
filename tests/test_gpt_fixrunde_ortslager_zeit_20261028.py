"""GPT-FIX01 28.10.2026: neue Wirtschafts-Regressionen zur Fehlerklassifizierung.

Bewusst der echte Startpfad (statt Settlement ohne Anfangsvorraete).
Bei aktivem Oekonomiemodus liegt Holz/Stein ausschliesslich im Ortslager;
die Reichswerte sind reine Anzeigen. Alle Tests arbeiten mit temporaeren Saves.
"""
from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'tools')]
import gpt_erzeuge_startstaende as starter
import main


class OrtskasseUndSpieluhr(unittest.TestCase):
    def start(self):
        state = starter.neu_erzeugen()
        self.assertTrue(state._lokale_kasse_aktiv())
        self.assertEqual(len(state.settlements), 1)
        return state

    def gegenprobe(self, state):
        expected = state.ortslager()
        for stoff in ('holz', 'stein'):
            self.assertAlmostEqual(state.resources[stoff].amount, expected[stoff], places=8)

    def test_grundertrag_und_reichssumme(self):
        state = self.start()
        ort = state.settlements[0]
        self.assertEqual(ort.vorraete['holz'], 100.0)
        self.assertEqual(ort.vorraete['stein'], 100.0)
        state.tick(3600)
        self.assertAlmostEqual(ort.vorraete['holz'], 101.0)
        self.assertAlmostEqual(ort.vorraete['stein'], 101.0)
        self.gegenprobe(state)

    def test_zeitscheiben_bewirken_keine_doppelte_ernte(self):
        einzeln = self.start()
        scheiben = copy.deepcopy(einzeln)
        einzeln.tick(3600)
        for _ in range(10):
            scheiben.tick(360)
        for stoff in ('holz', 'stein'):
            self.assertAlmostEqual(einzeln.settlements[0].vorraete[stoff],
                                   scheiben.settlements[0].vorraete[stoff], places=7)
        self.gegenprobe(scheiben)

    def test_speichern_laden_und_weiterproduzieren(self):
        state = self.start()
        state.tick(1800)
        with tempfile.TemporaryDirectory() as temp:
            pfad = str(Path(temp) / 'unabhaengiger_rundlauf.json')
            self.assertTrue(state.save(pfad))
            neu = main.GameState()
            self.assertTrue(neu.load(pfad))
            self.assertAlmostEqual(neu.settlements[0].vorraete['holz'], 100.5)
            self.assertAlmostEqual(neu.settlements[0].vorraete['stein'], 100.5)
            self.assertAlmostEqual(neu.spielsekunden, 1800)
            self.gegenprobe(neu)
            neu.tick(1800)
            self.assertAlmostEqual(neu.settlements[0].vorraete['holz'], 101.0)
            self.assertAlmostEqual(neu.settlements[0].vorraete['stein'], 101.0)
            self.gegenprobe(neu)

    def test_anzeigewert_ist_keine_versteckte_kasse(self):
        state = self.start()
        ort = state.settlements[0]
        # Ein direkter GUI-/Legacy-Zugriff auf die Anzeige darf kein reales Holz
        # in die lokale Kasse zaubern.
        state.resources['holz'].amount = 1000000
        self.assertFalse(state.verbrauche_am_ort(ort, {'holz': 101})[0])
        self.assertEqual(ort.vorraete['holz'], 100.0)
        state._reichsanzeige_aus_orten()
        self.gegenprobe(state)

    def test_ortsabbuchung_auch_nach_laden_einmal(self):
        state = self.start()
        ort = state.settlements[0]
        ok, meldung = state.verbrauche_am_ort(ort, {'holz': 15, 'stein': 3})
        self.assertTrue(ok, meldung)
        self.assertAlmostEqual(ort.vorraete['holz'], 85.0)
        self.assertAlmostEqual(ort.vorraete['stein'], 97.0)
        with tempfile.TemporaryDirectory() as temp:
            pfad = str(Path(temp) / 'abbuchung.json')
            self.assertTrue(state.save(pfad))
            neu = main.GameState()
            self.assertTrue(neu.load(pfad))
            self.assertAlmostEqual(neu.settlements[0].vorraete['holz'], 85.0)
            self.assertAlmostEqual(neu.settlements[0].vorraete['stein'], 97.0)
            self.gegenprobe(neu)


if __name__ == '__main__':
    unittest.main()
