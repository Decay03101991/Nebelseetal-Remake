"""GPT W-04: Sichtbarer Kartenrahmen ohne Feldverlust, realer Tk-Canvas (Xvfb/Windows)."""
import sys, unittest, tkinter as tk
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from main import GameState,Settlement,NebelseetalApp
import originalkarten

class GUIWall(unittest.TestCase):
    def setUp(self):
        self.root=tk.Tk()
        self.root.withdraw()
        self.state=GameState()
        # Nur echte Originalkarten: keine 8x7-Fixture und kein Fantasie-Raster.
        self.karte = originalkarten.startkarte('wall-gui-regression', 'spieler')
        self.ort=Settlement(name='A',map_id='kontinent',karte=self.karte,
                            id='spieler:kontinent:1:1',vorraete={'holz':100,'stein':100})
        self.state.settlements=[self.ort]
        self.state.research['Verteidigungsanlagen'].level=5
        self.app=NebelseetalApp.__new__(NebelseetalApp)
        self.app.state=self.state
        self.app.content=tk.Frame(self.root)
        self.app.content.pack()
        self.app.karten_feld=None
        self.app.karten_siedlung=self.ort
    def tearDown(self): self.root.destroy()
    def test_kein_rahmen_ohne_wall(self):
        self.app._zeichne_siedlungskarte(self.ort,self.karte)
        self.assertEqual(len(self.app.karten_canvas.find_withtag('dorfwall')),0)
    def test_wall_rahmt_100_originalfelder_ohne_belegung(self):
        vorher=dict(self.ort.bauten)
        self.ort.mauer_besetzt=True
        self.app._zeichne_siedlungskarte(self.ort,self.karte)
        self.assertEqual(len(self.app.karten_canvas.find_withtag('dorfwall')),5)
        self.assertEqual(self.ort.bauten,vorher)
        self.assertEqual(len(self.karte['raster']),100)
    def test_rahmen_automatisch_nach_forschung_aktualisiert(self):
        self.ort.mauer_besetzt=True
        self.app._zeichne_siedlungskarte(self.ort,self.karte)
        self.assertEqual(len(self.app.karten_canvas.find_withtag('dorfwall')),5)
        erste=self.app.karten_canvas.itemcget(self.app.karten_canvas.find_withtag('dorfwall')[0],'width')
        self.state.research['Verteidigungsanlagen'].level=3
        self.app._zeichne_siedlungskarte(self.ort,self.karte)
        neue=self.app.karten_canvas.itemcget(self.app.karten_canvas.find_withtag('dorfwall')[0],'width')
        self.assertNotEqual(erste,neue)
    def test_echte_wall_schaltflaeche_bucht_ort(self):
        from main import SKINS
        self.app.root=self.root
        self.app.skin=SKINS['standard']
        self.app._render_view=lambda :None
        self.ort.vorraete={'holz':100.,'stein':100.}
        # Die Versorgungssperre ist absichtlich aktiv: erst lebenswichtige
        # Produzenten errichten, dann darf das Dorf seinen Wall bezahlen.
        wald = self.karte['raster'].index('wald')
        berg = self.karte['raster'].index('berg')
        self.ort.bauten={str(wald):'holzfaeller',str(berg):'steinmetz'}
        self.app._render_settlement_map()
        def buttons(w):
            for child in w.winfo_children():
                if isinstance(child,tk.Button):
                    yield child
                yield from buttons(child)
        knopf=next(b for b in buttons(self.app.content)
                   if 'Wall errichten' in str(b.cget('text')))
        knopf.invoke()
        self.assertTrue(self.ort.mauer_besetzt)
        self.assertEqual(self.ort.vorraete['holz'],84)
        self.assertEqual(self.ort.vorraete['stein'],84)
        self.assertEqual(self.ort.bauten,{str(wald):'holzfaeller',str(berg):'steinmetz'})

if __name__=='__main__':unittest.main()
