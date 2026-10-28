# -*- coding: utf-8 -*-
"""FIX04e: Admin-Hilfemodus gilt auch im Dorfzentrum nach jeder Navigation.

Praeziser Regressionstest zu Daniels Windows-Befund vom 28.10.2026:
'ausblenden' versteckte die rechte Seitenleiste, aber das alte Dorfzentrum
zeichnete eine unabhaengige Hilfekarte bei jedem Besuch erneut.
"""
from __future__ import annotations

import sys
import tkinter as tk
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import main
import admin_werkzeuge
import spieloekonomie


def _beschriftungen(widget):
    aus = []
    for kind in widget.winfo_children():
        if isinstance(kind, tk.Label):
            aus.append(str(kind.cget('text')))
        aus.extend(_beschriftungen(kind))
    return aus


class BegleitendeHilfeBleibtAus(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = main.NebelseetalApp(self.root)
        self.app.state.admin_teststand = True
        self.app.state.oekonomie_aktiv = True
        self.app._profil = 'admin'
        self.app._admin_sitzung_freigegeben = True
        # FIX04f: Die alten 04e-Tests pruefen die optionale Hilfe NACH
        # der abgeschlossenen Pflicht-Startversorgung, nicht vor ihr.
        karte = spieloekonomie.startkarte('fix04e-test', 'spieler')
        ort = main.Settlement(name='Siedlung 1', map_id=self.app.state.current_map,
                              karte=karte)
        for geb, gel in (('holzfaeller','wald'), ('steinmetz','berg'), ('jaeger','wald')):
            idx = next(i for i, a in enumerate(karte['raster'])
                       if a == gel and str(i) not in ort.bauten)
            ort.bauten[str(idx)] = geb
        self.app.state.settlements = [ort]
        self.app._build_main_ui()
        self.root.update_idletasks()

    def tearDown(self):
        self.root.destroy()

    def _hat_aufgabenkarte(self):
        return 'Dein nächster Schritt' in _beschriftungen(self.app.content)

    def test_admin_ausblenden_bleibt_auch_nach_dorfzentrum_navigation_aus(self):
        self.assertTrue(self._hat_aufgabenkarte())
        self.assertEqual(self.app.hilfe_rahmen.winfo_manager(), 'pack')
        admin_werkzeuge.spielerhilfe_modus_setzen(self.app.state, 'ausblenden', freigabe=True)
        self.app._admin_ansicht_aktualisieren()  # realer Admin-Dialog-Callback
        self.assertFalse(self.app.hilfe_rahmen.winfo_manager())
        self.assertFalse(self._hat_aufgabenkarte())
        self.app._switch_view('Lager')
        self.app._switch_view('Dorfzentrum')
        self.assertFalse(self._hat_aufgabenkarte())
        self.assertFalse(self.app.hilfe_rahmen.winfo_manager())
        self.assertEqual(self.app.state.admin_hilfe_modus, 'ausblenden')
        self.assertTrue(self.app.state.noob_protection)
        self.assertIn('Siedlungen:', _beschriftungen(self.app.content))

    def test_admin_anzeigen_gilt_auch_nach_schutzende_und_navigation(self):
        self.app.state.noob_protection = False
        admin_werkzeuge.spielerhilfe_modus_setzen(self.app.state, 'anzeigen', freigabe=True)
        self.app._spielerhilfe_anzeige_aktualisieren()
        self.assertTrue(self._hat_aufgabenkarte())
        self.assertEqual(self.app.hilfe_rahmen.winfo_manager(), 'pack')
        self.app._switch_view('Dorfzentrum')
        self.assertTrue(self._hat_aufgabenkarte())

    def test_automatik_entfernt_beide_hilfen_bei_schutzende_sofort(self):
        self.assertTrue(self._hat_aufgabenkarte())
        self.app.state.noob_protection = False
        self.app._spielerhilfe_anzeige_aktualisieren()  # wie beim Spiel-Tick
        self.assertFalse(self._hat_aufgabenkarte())
        self.assertFalse(self.app.hilfe_rahmen.winfo_manager())
        self.app._switch_view('Dorfzentrum')
        self.assertFalse(self._hat_aufgabenkarte())

    def test_manuelle_spielerhilfe_bleibt_bei_ausblenden_immer_erreichbar(self):
        admin_werkzeuge.spielerhilfe_modus_setzen(self.app.state, 'ausblenden', freigabe=True)
        self.app._spielerhilfe_anzeige_aktualisieren()
        self.app._switch_view('Anleitung')
        self.assertIn('Spielerhilfe', _beschriftungen(self.app.content))
        self.assertFalse(self.app.hilfe_rahmen.winfo_manager())
        self.app._switch_view('Dorfzentrum')
        self.assertFalse(self._hat_aufgabenkarte())

    def test_normaler_spieler_ignoriert_admin_modus(self):
        admin_werkzeuge.spielerhilfe_modus_setzen(self.app.state, 'ausblenden', freigabe=True)
        self.app._profil = 'spieler'
        self.app._admin_sitzung_freigegeben = False
        self.app._spielerhilfe_anzeige_aktualisieren()
        self.assertTrue(self._hat_aufgabenkarte())
        self.assertEqual(self.app.hilfe_rahmen.winfo_manager(), 'pack')
        self.app.state.noob_protection = False
        self.app._spielerhilfe_anzeige_aktualisieren()
        self.assertFalse(self._hat_aufgabenkarte())


if __name__ == '__main__':
    unittest.main(verbosity=2)
