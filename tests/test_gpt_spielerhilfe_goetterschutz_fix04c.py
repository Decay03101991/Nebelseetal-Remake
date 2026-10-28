# -*- coding: utf-8 -*-
"""FIX04c – Hilfe erscheint nur während echten Schutzes, bleibt aufrufbar."""
import sys
import tkinter as tk
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import spielerhilfe  # noqa: E402
import main  # noqa: E402


def alle_widgets(widget):
    yield widget
    for child in widget.winfo_children():
        yield from alle_widgets(child)


class HilfeOhneSpielzustandMutation(unittest.TestCase):
    def test_kurzinfo_zeigt_aktuellen_tag_und_start(self):
        zustand = main.GameState()
        self.assertTrue(spielerhilfe.schutz_aktiv(zustand))
        self.assertIn('Tag 1', spielerhilfe.kurzinfo(zustand))
        self.assertIn('Siedlung', spielerhilfe.kurzinfo(zustand))

    def test_vorgefertigte_fragen_und_richtige_regeln(self):
        z = main.GameState()
        self.assertGreaterEqual(len(spielerhilfe.FRAGEN), 8)
        for frage in spielerhilfe.FRAGEN:
            self.assertTrue(spielerhilfe.antwort(frage, z), frage)
        self.assertIn('Steppe', spielerhilfe.antwort('Wie baue ich ressourcenschonend?', z))
        self.assertIn('Sümpfe', spielerhilfe.antwort('Warum kann ich hier nicht bauen?', z))
        self.assertIn('Kriegspunkt', spielerhilfe.antwort('Was bedeutet Götterschutz?', z))
        self.assertIn('drei', spielerhilfe.antwort('Wie speichere und lade ich?', z))
        self.assertIn('Ortslager', spielerhilfe.antwort('Wie funktionieren Ortslager?', z))

    def test_hilfe_aendert_kein_spiel(self):
        z = main.GameState()
        before = (z.day, z.noob_protection, dict(z.punktestand()),
                  {k: v.amount for k, v in z.resources.items()})
        for frage in spielerhilfe.FRAGEN:
            spielerhilfe.antwort(frage, z)
        spielerhilfe.kurzinfo(z)
        self.assertEqual(before, (z.day, z.noob_protection, dict(z.punktestand()),
                                  {k: v.amount for k, v in z.resources.items()}))


class HilfeGUI(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = main.NebelseetalApp(self.root)
        self.app._build_main_ui()
        self.root.update_idletasks()

    def tearDown(self):
        self.root.destroy()

    def test_pane_zuerst_da_nach_schutz_weg(self):
        self.assertEqual(self.app.hilfe_rahmen.winfo_manager(), 'pack')
        self.assertIn('Götterschutz aktiv', self.app.hilfe_kurztext.cget('text'))
        self.app.state.day = 4
        self.app._render()
        self.assertIn('Tag 4', self.app.hilfe_kurztext.cget('text'))
        # Genau dasselbe Flag, das der Regelkern auch bei Kriegspunkten beendet.
        self.app.state.noob_protection = False
        self.app._render()
        self.assertFalse(self.app.hilfe_rahmen.winfo_manager())
        self.app._switch_view('Anleitung')
        texte = ' '.join(str(w.cget('text')) for w in alle_widgets(self.app.content)
                         if 'text' in w.keys())
        self.assertIn('Götterschutz beendet', texte)
        self.assertIn('Wie baue ich ressourcenschonend?', texte)
        self.assertIn('Weitere Fragen', texte)

    def test_vorgefertigte_frage_bleibt_nach_ablauf_abrufbar(self):
        self.app.state.noob_protection = False
        self.app._switch_view('Anleitung')
        self.app._spielerhilfe_frage('Wie baue ich ressourcenschonend?')
        texte = ' '.join(str(w.cget('text')) for w in alle_widgets(self.app.content)
                         if 'text' in w.keys())
        self.assertIn('Bibliotheken', texte)
        self.assertIn('Steppe', texte)
        # Auch nach Skin-/UI-Neuaufbau bleibt die Hilfe erreichbar, die Pane versteckt.
        self.app._cycle_skin()
        self.assertFalse(self.app.hilfe_rahmen.winfo_manager())
        knoepfe = [w for w in alle_widgets(self.root)
                   if w.winfo_class() == 'Button' and w.cget('text') == 'Spielerhilfe']
        self.assertEqual(len(knoepfe), 1)
        knoepfe[0].invoke()
        self.assertEqual(self.app.current_view, 'Anleitung')


if __name__ == '__main__':
    unittest.main(verbosity=2)
