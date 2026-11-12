"""GPT extern: neue Partie statt Rettung eines nicht benoetigten Legacy-Saves."""

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['admin_teststand', 'main:*', 'spielstaende', 'wirtschaft']
PRUEF_DATEN = ['bot_diebstahl.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------
import sys,os,tempfile,pathlib,unittest
from unittest import mock
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','tools'))
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','src'))
import main,spielstaende,wirtschaft
import gpt_erzeuge_startstaende as vorlagen

class Frischstart(unittest.TestCase):
    def test_startwerte_und_kartenmass(self):
        state=vorlagen.neu_erzeugen()
        s=state.settlements[0]
        self.assertEqual((s.vorraete['holz'],s.vorraete['stein'],s.bevoelkerung),(100,100,10))
        self.assertEqual((s.karte['spalten'],s.karte['zeilen'],len(s.karte['raster'])),(10,10,100))
        self.assertEqual(s.karte['originalkarte_id'], 'original-036')
        self.assertEqual(sum(g!='sumpf' for g in s.karte['raster']), s.karte['bauplaetze'])
        # SCHNITT S-1 (Daniel 01.11.2026, docs/KONZEPT_SECHS_DOERFER_20261101.md Anhang 1): der
        # Siedlungskarren bringt Holzfaeller, Steinmetz und Tempel mit. Die Wache hiess frueher
        # "kein Gebaeude am Anfang" und prueft jetzt die neue Wahrheit: genau diese drei, sonst
        # nichts (keine erforschten Ausbaustufen, kein viertes Gebaeude).
        self.assertEqual(sorted(s.bauten.values()), ['holzfaeller', 'steinmetz', 'tempel'])
        self.assertIsNone(state.spielende)
        self.assertFalse(state.admin_teststand)
        self.assertTrue(state.oekonomie_aktiv)
    def test_vorlagen_rundlauf(self):
        with tempfile.TemporaryDirectory() as tmp:
            path,admin=vorlagen.erzeugen(tmp)
            g=main.GameState();self.assertTrue(g.load(path))
            self.assertEqual(len(g.settlements),1)
            self.assertFalse(g.load(admin))
            self.assertEqual(len(g.settlements),1)  # Ablehnung vor Mutation
            self.assertTrue(g.load(admin,admin_freigabe=True))
            self.assertEqual(len(g.settlements),6)
            self.assertTrue(g.admin_teststand)
            for s in g.settlements:
                self.assertIn('steinmetz',s.bauten.values())
                self.assertIn('holzfaeller',s.bauten.values())
                self.assertIn('bogenbauer',s.bauten.values())
                r=wirtschaft.siedlung_ertrag(s)
                self.assertGreater(r.get('Holz',0),0)
                self.assertGreater(r.get('Stein',0),0)
            self.assertEqual(g.spielende,None)
    def test_vorlage_darf_slot_nicht_ueberschreiben(self):
        with tempfile.TemporaryDirectory() as tmp:
            path,admin=vorlagen.erzeugen(tmp)
            stand=pathlib.Path(path).read_bytes()
            with self.assertRaises(FileExistsError):
                vorlagen.erzeugen(tmp)
            self.assertEqual(pathlib.Path(path).read_bytes(),stand)
    def test_regulaere_hoechstpunkte_nicht_vorweggenommen(self):
        n=vorlagen.neu_erzeugen()
        # S-1: Stufen stehen nur auf den drei Startgebaeuden (je Stufe 1) - nichts vorweggenommen.
        # Frueher hiess die Wache "keine Stufe ueberhaupt"; die Zusage bleibt, der Anker ist neu.
        self.assertEqual(sorted((f,int(v)) for s in n.settlements for f,v in s.stufen.items()),
                         sorted((f,1) for s in n.settlements for f in s.bauten))
        self.assertEqual(n.day,1)
        self.assertEqual(n.spielsekunden,0)
        self.assertTrue(n.noob_protection)
    def test_echter_start_baut_produzenten_und_erntet_nach_einer_stunde(self):
        # S-13 (03.11.2026, Register 162): der Diebstahl ist EINGESCHALTET (data/bot_diebstahl.json).
        # Diese Wache belegt die ERNTE des Startorts, nicht den Diebstahl (eigene Wache:
        # tests/test_bot_diebstahl.py) - deshalb ist der Diebstahl hier ausdruecklich aus.
        # Ohne diese Zeile zog der Bot-Takt 5,56 Holz und 5,44 Stein ab (gemessen 88,44 / 86,56).
        with mock.patch.object(main, "bot_diebstahl_einstellungen", lambda: {"aktiv": False}):
            self._start_und_ernte_pruefen()

    def _start_und_ernte_pruefen(self):
        state=vorlagen.neu_erzeugen()
        ort=state.settlements[0]
        gui=main.NebelseetalApp.__new__(main.NebelseetalApp)
        gui.state=state;gui.karten_siedlung=ort;gui._render_view=lambda:None
        gui._log=state._log
        for geb,gel in (('holzfaeller','wald'),('steinmetz','berg')):
            gui.karten_feld=next(i for i,a in enumerate(ort.karte['raster'])
                                   if a==gel and str(i) not in ort.bauten)
            gui._karten_bauen(geb)
        self.assertEqual((ort.vorraete['holz'],ort.vorraete['stein']),(85.0,85.0))
        state.tick(3600)
        # Original-Tutorial: Grundproduktion 1/h je Holz/Stein plus 4/h Gebaeudeertrag.
        # S-1 (Daniel 01.11.2026): die zwei gebauten Gebaeude kommen zu den Startgebaeuden dazu -
        # Holz: 1/h Grund + 4/h Start-Holzfaeller (Wald) + 4/h neuer Holzfaeller (Wald) = 9/h,
        # Stein: 1/h Grund + 2/h Start-Steinmetz (Huegel) + 4/h neuer Steinmetz (Berg) = 7/h.
        # Der alte Wert 5/h je Stoff galt fuer den leeren Aufbauzustand.
        self.assertEqual((ort.vorraete['holz'],ort.vorraete['stein']),(94.0,92.0))
        self.assertEqual(state.spielsekunden,3600)
        self.assertIsNone(state.spielende)

    def test_admin_muss_separat_bleiben(self):
        a=vorlagen.admin_erzeugen()
        self.assertTrue(a.admin_teststand)
        self.assertFalse(a.save('/tmp/gpt_test_normal_no_write.json'))

if __name__=='__main__':unittest.main(verbosity=2)
