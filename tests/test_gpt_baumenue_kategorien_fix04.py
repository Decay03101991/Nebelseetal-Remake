# -*- coding: utf-8 -*-
"""FIX04: Historisches Baumenue mit echten Rubriken und einer Baukasse.

Tk-GUI-Tests brauchen einen Windows-Desktop oder xvfb-run; keine privaten Spielstaende.
"""
from __future__ import annotations

import sys
import tkinter as tk
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import main  # noqa: E402
import gelaende  # noqa: E402
import baumenue_info  # noqa: E402


def widgets(start):
    yield start
    for child in start.winfo_children():
        yield from widgets(child)


def texte(start):
    return [str(w.cget('text')) for w in widgets(start) if 'text' in w.keys()]


class TestBaumenueFix04(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = main.NebelseetalApp(self.root)
        self.app._build_main_ui()
        self.app._found_settlement()
        self.ort = self.app.state.settlements[0]
        self.app._oeffne_siedlungskarte(self.ort)
        self.root.update_idletasks()
        self.feld = self.ort.karte['raster'].index('wald')
        self.app._karten_feld_waehlen(self.feld)
        self.root.update_idletasks()

    def tearDown(self):
        self.root.destroy()

    def test_menu_zeigt_produktionsrubrik_und_korrekte_sperren(self):
        self.assertEqual(self.app._karten_baukategorie, 'Produktion')
        zeigen = '\n'.join(texte(self.app.content))
        self.assertIn('Holzfäller', zeigen)
        self.assertNotIn('Kriegerakademie — ', zeigen)
        self.assertIn('Baubereich:', zeigen)
        self.assertIn('Gesperrt: Baukunst Stufe 1', zeigen)
        self.assertEqual(len(self.app.karten_canvas.find_withtag('originalkarte')), 1)
        self.assertEqual(len(self.app.karten_canvas.find_withtag('kartenfeld')), 100)

    def test_rubrikwechsel_und_beschreibungen_aus_originaldaten(self):
        # Kriegerakademie ist nur auf Grasland, Steppe oder Huegel erlaubt.
        self.app._karten_feld_waehlen(self.ort.karte['raster'].index('grasland'))
        self.root.update_idletasks()
        auswahl = [w for w in widgets(self.app.content) if w.winfo_class() == 'Menubutton']
        self.assertTrue(auswahl, 'Rubrik-Auswahl im Kartenmenue vorhanden')
        menu = auswahl[-1].nametowidget(auswahl[-1]['menu'])
        position = baumenue_info.KATEGORIEN.index('Ausbildung')
        menu.invoke(position)
        self.root.update_idletasks()
        self.assertEqual(self.app._karten_baukategorie, 'Ausbildung')
        zeigen = '\n'.join(texte(self.app.content))
        self.assertIn('Kriegerakademie', zeigen)
        self.assertNotIn('Holzfäller — ', zeigen)
        self.assertIn('Gesperrt: Baukunst Stufe 1', zeigen)

    def test_anzeige_liest_lager_aber_aendert_es_nicht(self):
        vorher = (dict(self.ort.vorraete), dict(self.ort.bauten), self.ort.bevoelkerung)
        self.app._render_view()
        self.assertEqual(vorher, (self.ort.vorraete, self.ort.bauten, self.ort.bevoelkerung))
        self.ort.vorraete.update({'holz': 0, 'stein': 0})
        self.app._render_view()
        zeigen = '\n'.join(texte(self.app.content))
        self.assertIn('Fehlt im Ortslager:', zeigen)

    def test_bau_bleibt_einzigem_kassenpfad_und_originalkarte_treu(self):
        self.ort.vorraete.update({'holz': 500, 'stein': 500})
        self.ort.bevoelkerung = 100
        self.app.state._reichsanzeige_aus_orten()
        preis = main.baukosten('holzfaeller')
        vorher = self.ort.vorraete['holz']
        self.app._karten_bauen('holzfaeller')
        self.assertEqual(self.ort.bauten[str(self.feld)], 'holzfaeller')
        self.assertEqual(self.ort.vorraete['holz'], vorher-preis['holz'])
        self.assertEqual(self.app._karten_baukategorie, 'Produktion')
        self.assertEqual(len(self.app.karten_canvas.find_withtag('originalkarte')), 1)

    def test_sumpf_unbebaubar_und_wall_ohne_feld(self):
        sumpf = self.ort.karte['raster'].index('sumpf')
        self.app._karten_feld_waehlen(sumpf)
        self.root.update_idletasks()
        self.assertIn('Sumpf', '\n'.join(texte(self.app.content)))
        self.assertIn('nicht bebaubar', '\n'.join(texte(self.app.content)))
        self.app._karten_feld_waehlen(self.feld)
        self.app._karten_baukategorie = 'Verteidigung'
        self.app._render_view()
        anzeigen = '\n'.join(texte(self.app.content))
        self.assertIn('belegt kein Kartenfeld', anzeigen)


if __name__ == '__main__':
    unittest.main(verbosity=2)
