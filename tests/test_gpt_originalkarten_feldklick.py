# -*- coding: utf-8 -*-
"""Regression: Originalbild bleibt echt, 100 Felder sind einzeln erreichbar.

Unter Windows interaktiv oder unter Linux mit ``xvfb-run -a`` ausfuehren.
Der Test aendert weder Bilddateien noch Spielstaende oder Passwortkonfiguration.
"""
from __future__ import annotations

import sys
import tkinter as tk
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import main  # noqa: E402
import karten_optik_fein  # noqa: E402


class TestOriginalkartenFeldklick(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = main.NebelseetalApp(self.root)
        self.app._build_main_ui()
        self.app._found_settlement()
        self.siedlung = self.app.state.settlements[0]
        self.app._oeffne_siedlungskarte(self.siedlung)
        self.root.update()

    def tearDown(self):
        self.root.destroy()

    def test_100_semantische_feldregionen(self):
        canvas = self.app.karten_canvas
        karte = self.siedlung.karte
        self.assertEqual((karte["spalten"], karte["zeilen"]), (10, 10))
        self.assertEqual(len(karte["raster"]), 100)
        self.assertEqual(len(canvas.find_withtag("originalkarte")), 1)
        self.assertTrue(hasattr(canvas, "_originalkarten_bild"))
        self.assertEqual(len(canvas.find_withtag("kartenfeld")), 100)
        for feld in range(100):
            with self.subTest(feld=feld):
                self.assertTrue(canvas.find_withtag(f"feld:{feld}"))

    def test_echte_mausklicks_waehlen_rand_und_innenfelder(self):
        rand = int(karten_optik_fein.KOORDINATEN_BREITE)
        for feld in (0, 9, 50, 55, 90, 99):
            canvas = self.app.karten_canvas  # nach jedem Klick neu gerendert
            x = rand + (feld % 10) * 64 + 32
            y = rand + (feld // 10) * 64 + 32
            canvas.event_generate("<Button-1>", x=x, y=y)
            self.root.update()
            self.assertEqual(self.app.karten_feld, feld)
            self.assertTrue(self.app.karten_canvas.find_withtag("auswahl"))
        # Klick auf Koordinatenleiste ist KEIN Kartenfeld-Klick.
        vorher = self.app.karten_feld
        self.app.karten_canvas.event_generate("<Button-1>", x=3, y=3)
        self.root.update()
        self.assertEqual(self.app.karten_feld, vorher)


if __name__ == "__main__":
    unittest.main(verbosity=2)
