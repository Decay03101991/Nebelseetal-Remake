# -*- coding: utf-8 -*-
"""Verpflichtende Regression: nur 127 echte 10x10-Originalkarten im aktiven Spiel."""
from __future__ import annotations
import json
import hashlib
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'src'))
import originalkarten
import originalkarten_grafik
import gelaende
import spieloekonomie

class TestNurOriginalkarten(unittest.TestCase):
 def test_127_originalkarten_im_katalog(self):
  alle=originalkarten.alle()
  self.assertEqual(len(alle),127)
  self.assertEqual(len(set(e['id'] for e in alle)),127)
  self.assertEqual(len(originalkarten_grafik.manifest()),127)

 def test_alle_karten_grafiken_korrekt_zugeordnet(self):
  for e in originalkarten.alle():
   with self.subTest(id=e['id']):
    k=originalkarten.karte(e['id'])
    self.assertEqual((k['spalten'],k['zeilen'],len(k['raster'])),(10,10,100))
    self.assertEqual(k['originalkarte_id'],e['id'])
    p=originalkarten_grafik.grafikpfad(k)
    self.assertEqual(p.name,e['id']+'.png')
    self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),originalkarten_grafik.manifest()[e['id']]['sha256'])
    self.assertEqual(p.read_bytes()[:8],b"\x89PNG\r\n\x1a\n")
    self.assertEqual(hashlib.sha256((ROOT/e['originalbild']).read_bytes()).hexdigest(),e['bild_sha256'])

 def test_alle_spielstart_karten_original(self):
  for seed in ('spieler',0,42,4242):
   for person in ('spieler','bot-a','bot-b'):
    k=originalkarten.startkarte(seed,person)
    self.assertTrue(originalkarten_grafik.grafikpfad(k).is_file())
  self.assertEqual(len(originalkarten.vorrat('abc')),126)

 def test_alte_karten_koennen_nicht_neu_erzeugt_werden(self):
  k=gelaende.siedlungskarte_erzeugen(1)
  self.assertEqual(k['originalkarte_id'],originalkarten.START_ID)
  with self.assertRaisesRegex(ValueError,'8x7'):
   gelaende.siedlungskarte_erzeugen(1,typ_id='waldreich')
  with self.assertRaisesRegex(ValueError,'8x7'):
   spieloekonomie.feste_karte('alt',{'id':'x','gewichte':{}})

 def test_8x7_karten_ohne_original_id_werden_abgewiesen(self):
  bad={'spalten':8,'zeilen':7,'raster':['wald']*56}
  with self.assertRaisesRegex(ValueError,'10x10'):
   originalkarten_grafik.grafikpfad(bad)
  bad={'spalten':10,'zeilen':10,'raster':['wald']*100}
  with self.assertRaisesRegex(ValueError,'Original-ID'):
   originalkarten_grafik.grafikpfad(bad)

 def test_aktive_gui_zeichnet_keine_synthetischen_siedlungstexturen(self):
  s=(ROOT/'src/main.py').read_text('utf8')
  teil=s.split('    def _zeichne_siedlungskarte(',1)[1].split('    def _render_settlement_map(',1)[0]
  self.assertIn('originalkarten_grafik.grafikpfad',teil)
  self.assertNotIn('gelaende_plan_fein(',teil)
  self.assertIn('create_image(',teil)

 def test_originalbild_tk_kann_oeffnen(self):
  # Run under Windows with Tk or Linux xvfb-run: do not silently skip this verification.
  import tkinter as tk
  root=tk.Tk();root.withdraw()
  try:
   for kennung in ('original-001',originalkarten.START_ID,originalkarten.kennungen()[-1]):
    bild=tk.PhotoImage(file=str(originalkarten_grafik.grafikpfad(originalkarten.karte(kennung))),master=root)
    self.assertEqual((bild.width(),bild.height()),(640,640))
  finally:root.destroy()

if __name__=='__main__':
 unittest.main(verbosity=2)
