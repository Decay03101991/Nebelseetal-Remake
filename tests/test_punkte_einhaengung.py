"""Einbindung der Punkteanzeige fuer Dorfwaelle und Legacy-Stand.

GPT W-05, 28.10.2026. Ersetzt veraltete *Testannahmen*, keine Spiellogik.
Der vollstaendige vorherige Test steht unter
`docs/archiv/test_punkte_einhaengung_vor_GPT_WALL_2026-10-28.py`.
Nicht nur Returncodes: unittests pruefen echte GUI-Labels und Punktewerte.
"""
from __future__ import annotations

import sys
import tkinter as tk
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import main
import punkte


def _texte(widget):
    ergebnis = []
    for child in widget.winfo_children():
        try:
            s = str(child.cget('text'))
            if s: ergebnis.append(s)
        except (tk.TclError,AttributeError):
            pass
        ergebnis.extend(_texte(child))
    return ergebnis


def _dorf(name, x, active=False):
    return main.Settlement(name=name,map_id='kontinent',x=x,y=1,
                           id=f'spieler:kontinent:{x}:1',
                           karte={'spalten':8,'zeilen':7,'raster':['wald']*56,
                                  'typ_name':'Test','zaehlung':{},'vorteil':''},
                           vorraete={'holz':100.,'stein':100.},
                           mauer_besetzt=active)

class PunkteAnzeigeNeumodus(unittest.TestCase):
    def setUp(self):
        self.root=tk.Tk();self.root.withdraw()
        self.app=main.NebelseetalApp(self.root)
        self.app._build_main_ui()
        self.state=self.app.state
        self.state.settlements=[]
        for f in self.state.research.values(): f.level=0
        for u in self.state.units.values(): u.count=0
        self.state.score=999
        self.state.ruf=777
        self.state.spielende=None
        self.state.hatte_siedlung=False
        self.assertEqual(self.state.mode,main.MODUS_NEU)
        self.assertTrue(self.state.oekonomie_aktiv)

    def tearDown(self): self.root.destroy()

    def render_labels(self):
        self.app._render()
        self.root.update_idletasks()
        return (self.app.lbl_forschung.cget('text'),
                self.app.lbl_krieg.cget('text'),
                self.app.lbl_gesamt.cget('text'))

    def assert_synchron(self):
        punkte_state=self.state.punktestand()
        self.assertEqual(self.render_labels(),
            (f"Forschung: {punkte_state['forschung']}",
             f"Krieg: {punkte_state['krieg']}",
             f"Gesamt: {punkte_state['gesamt']}"))
        self.app._switch_view('Ruhmeshalle')
        texte=_texte(self.app.content)
        for zeile in self.render_labels():
            self.assertIn(zeile,texte)
        return texte

    def test_punktemodul_verwendet(self):
        self.assertIs(main.punkte,punkte)
        self.assertEqual(punkte.kriegspunkte({'Krieger':2},0),8)
        self.assertEqual(punkte.forschungspunkte({'Felderwirtschaft':3,'Minenarbeit':3}),54)

    def test_alle_null_trotz_alter_felder(self):
        self.assertEqual(self.state.punktestand()['gesamt'],0)
        self.assert_synchron()

    def test_forschung_kubik_und_truppenkosten(self):
        self.state.research['Felderwirtschaft'].level=3
        self.state.research['Minenarbeit'].level=3
        self.state.units['Krieger'].count=2
        self.assertEqual(self.state.punktestand()['forschung'],54)
        self.assertEqual(self.state.punktestand()['krieg'],8)
        self.assertEqual(self.state.punktestand()['gesamt'],31)
        self.assert_synchron()

    def test_technologiestufe_allein_zaehlt_keinen_wall(self):
        self.state.research['Verteidigungsanlagen'].level=4
        ort=_dorf('A',1,False)
        self.state.settlements=[ort]
        self.assertEqual(self.state.wall_stufe_am_ort(ort),0)
        self.assertEqual(self.state.wall_kriegspunkte(),0)
        self.assertIn('Wallstufe: 0',self.assert_synchron())

    def test_eine_aktivierte_mauer_zaehlt_stufe_hoch_drei(self):
        self.state.research['Verteidigungsanlagen'].level=4
        ort=_dorf('A',1,True)
        self.state.settlements=[ort]
        self.state.units['Krieger'].count=2
        self.assertEqual(self.state.punktestand()['krieg'],72)
        self.assertEqual(self.state.punktestand()['forschung'],64)
        self.assertEqual(self.state.punktestand()['gesamt'],68)
        self.assertIn('Wallstufe: 4',self.assert_synchron())

    def test_zwei_ortswaelle_kein_maximum_als_summe(self):
        self.state.research['Verteidigungsanlagen'].level=4
        self.state.settlements=[_dorf('A',1,True),_dorf('B',2,True)]
        self.assertEqual(self.state.punktestand()['wall_stufe'],4)
        self.assertEqual(self.state.wall_kriegspunkte(),128)
        self.assertEqual(self.state.punktestand()['krieg'],128)
        self.assertEqual(self.state.punktestand()['gesamt'],96)
        self.assert_synchron()

    def test_altes_feld_gewaehrt_keine_doppelten_neupunkte(self):
        self.state.research['Verteidigungsanlagen'].level=3
        ort=_dorf('A',1,True)
        ort.bauten={'0':'verteidigungswall'}
        ort.stufen={'0':10}
        self.state.settlements=[ort]
        self.assertEqual(self.state.wall_kriegspunkte(),27)
        self.assertEqual(self.state.punktestand()['krieg'],27)
        self.assert_synchron()

    def test_forschungsupdate_automatisch_in_beiden_anzeigen(self):
        self.state.research['Verteidigungsanlagen'].level=3
        self.state.settlements=[_dorf('A',1,True)]
        self.assertEqual(self.state.punktestand()['krieg'],27)
        self.assert_synchron()
        self.state.research['Verteidigungsanlagen'].level=5
        self.assertEqual(self.state.punktestand()['krieg'],125)
        self.assert_synchron()

    def test_spielausgang_ohne_sieg(self):
        """E5 (31.10.2026): es gibt KEINEN Sieg mehr - hohe Punkte ergeben 'weiter'.

        Frueher stand hier die Erwartung 'sieg' bei Forschungsstufe 9 (ueber 300 Punkte). Diese
        Zielzahl ist als Siegbedingung verworfen (Handbuch 2009, Seite 3); das Original kennt
        nur eigene Ziele. Niederlage bleibt der einzige Abbruch.
        """
        self.state.hatte_siedlung=True
        self.state.settlements=[_dorf('A',1,False)]
        self.state.research['Felderwirtschaft'].level=9
        self.assertEqual(self.state.spielausgang()[0],'weiter')
        self.state.settlements=[]
        self.state.research['Felderwirtschaft'].level=0
        self.assertEqual(self.state.spielausgang()[0],'niederlage')

    def test_legacy_feldwall_ohne_neumodus_migrieren(self):
        self.state.mode='legacy'
        self.state.research['Verteidigungsanlagen'].level=4
        ort=_dorf('Alt',1,False)
        ort.bauten={'0':'verteidigungswall'}
        ort.stufen={'0':4}
        self.state.settlements=[ort]
        self.assertEqual(self.state.wall_stufe_am_ort(ort),4)
        self.assertEqual(self.state.wall_kriegspunkte(),64)
        self.assertEqual(self.state.punktestand()['krieg'],64)
        self.assert_synchron()

if __name__=='__main__': unittest.main()
