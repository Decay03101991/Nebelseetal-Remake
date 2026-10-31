"""Externe GPT-Koordinator-Zuarbeit (28.10.2026).

Gezielte Integrations- und Regeltests; keine Aenderung an Originaldaten.
Tests verwenden explizit Mode + Ort-IDs und pruefen reale Transport-Buchungen.
"""
from __future__ import annotations

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import main
import spieloekonomie


class KoordinatorRegression(unittest.TestCase):
    def state(self):
        g = main.GameState()
        a = main.Settlement(id='spieler:kontinent:1:1', name='A', map_id='kontinent',
                            x=1, y=1, vorraete={'holz': 50, 'stein': 20},
                            bevoelkerung=5, einheiten={'Handkarren': 1})
        b = main.Settlement(id='spieler:kontinent:2:2', name='B', map_id='kontinent',
                            x=2, y=2, vorraete={'holz': 10, 'stein': 0}, bevoelkerung=5)
        g.settlements = [a, b]
        g._reichsanzeige_aus_orten()
        return g, a, b

    def test_buchungsquelle_nur_ortsbestand(self):
        g, a, b = self.state()
        self.assertEqual(g.resources['holz'].amount, 60)
        self.assertIn('holz', g.ortsdeckung(b, {'holz': 11}))
        self.assertFalse(g.verbrauche_am_ort(b, {'holz': 11})[0])
        self.assertEqual((a.vorraete['holz'], b.vorraete['holz']), (50, 10))

    def test_ortsabbuchung_erhaelt_reichssumme(self):
        g, a, b = self.state()
        self.assertTrue(g.verbrauche_am_ort(a, {'holz': 20})[0])
        self.assertEqual(a.vorraete['holz'], 30)
        self.assertEqual(g.resources['holz'].amount, 40)

    def test_reichsweit_physisch_ohne_doppelbelegung(self):
        g, a, b = self.state()
        self.assertIn('holz', g.reichsdeckung({'holz': 61}))
        self.assertFalse(g.verbrauche_reichsweit({'holz': 61})[0])
        self.assertTrue(g.verbrauche_reichsweit({'holz': 55})[0])
        self.assertEqual(sum(x.vorraete['holz'] for x in g.settlements), 5)
        self.assertEqual(g.resources['holz'].amount, 5)

    def test_keine_doppelten_siedler(self):
        g, a, b = self.state()
        self.assertEqual(g.population, 10)
        self.assertIn('siedler', g.ortsdeckung(a, {'siedler': 6}))
        self.assertIn('siedler', g.reichsdeckung({'siedler': 11}))

    def test_legacy_nicht_automatisch_migriert(self):
        g, a, b = self.state()
        g.mode = main.MODUS_LEGACY
        g.resources['holz'].amount = 20
        self.assertEqual(g.ortsdeckung(b, {'holz': 15}), {})

    def test_no_reichskarren_shortcut(self):
        g, a, b = self.state()
        a.einheiten.clear()
        g.units['Handkarren'].count = 10
        self.assertEqual(g.transport_karren_bestand(a), {})
        ok, _ = g.transport_an_ort(a, b, 'holz', 10, {'Handkarren': 1})
        self.assertFalse(ok)
        self.assertEqual(a.vorraete['holz'], 50)
        self.assertEqual(b.vorraete['holz'], 10)

    def test_karre_liefert_erst_nach_ankunft(self):
        g, a, b = self.state()
        ok, msg = g.transport_an_ort(a, b, 'holz', 10, {'Handkarren': 1})
        self.assertTrue(ok, msg)
        self.assertEqual(a.vorraete['holz'], 40)
        self.assertEqual(b.vorraete['holz'], 10)
        self.assertEqual(g.resources['holz'].amount, 50)
        # Die Ankunftszeit haengt an der Reiseformel (Vorgabe Daniel 31.10.2026: Faktor 2).
        # Deshalb wird sie hier AUS DEM AUFTRAG gelesen statt hartkodiert - so bleibt die
        # Pruefung richtig, wenn der Faktor bewusst angepasst wird.
        _ankunft = float(g.auftraege[0]['ankunft'])
        self.assertGreater(_ankunft, 720, 'Faktor 2 verdoppelt die Reisezeit')
        g.auftraege_fortschreiben(_ankunft - 1)
        self.assertEqual(b.vorraete['holz'], 10)
        g.auftraege_fortschreiben(_ankunft)
        self.assertEqual(b.vorraete['holz'], 20)
        self.assertEqual(g.resources['holz'].amount, 60)
        # Auch die Rueckkehr haengt an der Formel (Rueckweg = eine Strecke, zusammen doppelt).
        _rueck = float(g.auftraege[0]['rueckkehr'])
        g.auftraege_fortschreiben(_rueck - 1)
        self.assertEqual(len(g.auftraege), 1, 'vor der Rueckkehr ist der Auftrag noch offen')
        g.auftraege_fortschreiben(_rueck)
        self.assertEqual(a.einheiten.get('Handkarren'), 1)
        self.assertEqual(len(g.auftraege), 0)

    def test_original_baukunst_ohne_freie_mengen(self):
        k = spieloekonomie.startkarte('gpt-bau-test', 'spieler')
        s = main.Settlement(id='x', name='T', map_id='kontinent', karte=k)
        f = k['raster'].index('grasland')
        self.assertFalse(main.bauen_auf_karte(s, 'farm', f, {})[0])
        self.assertTrue(main.bauen_auf_karte(s, 'farm', f, {'Baukunst':1}, nur_pruefen=True)[0])
        self.assertEqual(s.bauten, {})
        self.assertTrue(main.bauen_auf_karte(s, 'farm', f, {'Baukunst':1})[0])
        self.assertIn(str(f), s.bauten)

    def test_v2_vor_aktivierung_wird_nicht_still_migriert(self):
        import json
        g, a, b = self.state()
        g.resources['holz'].amount = 175  # alter, noch eigenstaendiger Reichswert
        with tempfile.TemporaryDirectory() as temp:
            pfad = os.path.join(temp, 'preactivation.json')
            self.assertTrue(g.save(pfad))
            with open(pfad, encoding='utf-8') as stream:
                daten = json.load(stream)
            daten.pop('oekonomie_aktiv')  # v2 aus der Hermes-Vorphase
            daten['resources']['holz']['amount'] = 175
            with open(pfad, 'w', encoding='utf-8') as stream:
                json.dump(daten, stream)
            neu = main.GameState()
            self.assertTrue(neu.load(pfad))
            self.assertFalse(neu.oekonomie_aktiv)
            self.assertEqual(neu.resources['holz'].amount, 175)
            self.assertEqual(neu.settlements[0].vorraete['holz'], 50)

    def test_mehrtage_und_schutz(self):
        g = main.GameState()
        g.tick(7 * 86400)
        self.assertEqual(g.day, 8)
        self.assertEqual(g._day_accum, 0)
        self.assertFalse(g.noob_protection)

    def test_negative_spielsekunden_verboten(self):
        g = main.GameState()
        with self.assertRaises(ValueError):
            g.tick(-1)

    def test_neuer_speicherstand_lokal_und_altmodus_getrennt(self):
        g, a, b = self.state()
        g.verbrauche_am_ort(a, {'holz': 11})
        with tempfile.TemporaryDirectory() as temp:
            pfad = os.path.join(temp, 'save.json')
            self.assertTrue(g.save(pfad))
            neu = main.GameState()
            self.assertTrue(neu.load(pfad))
            self.assertEqual(neu.mode, main.MODUS_NEU)
            self.assertEqual(neu.resources['holz'].amount,
                             sum(s.vorraete.get('holz', 0) for s in neu.settlements))

if __name__ == '__main__':
    unittest.main(verbosity=2)
