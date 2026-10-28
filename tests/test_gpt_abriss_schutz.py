"""Externer GPT-Koordinator 28.10.: keine Abriss-Softlocks; Originalbauwerte unveraendert."""
import os,sys,copy,unittest
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','src'))
import main, spieloekonomie, versorgungsschutz

class AbrissSicherung(unittest.TestCase):
    def ort(self,stein=0,holz=0):
        k=spieloekonomie.startkarte('gpt-abriss', 'spieler')
        return main.Settlement(id='s',name='Stadt',map_id='kontinent',karte=k,
            vorraete={'holz':float(holz),'stein':float(stein)},bevoelkerung=10)
    def feld(self,s,arten):
        return next(i for i,a in enumerate(s.karte['raster']) if a in arten and str(i) not in s.bauten)
    def einsetzen(self,s,art,arten):
        i=self.feld(s,arten);s.bauten[str(i)]=art;s.stufen[str(i)]=1;return i
    def gui(self,s,i):
        z=main.GameState(); z.settlements=[s]; z.mode=main.MODUS_NEU;z.oekonomie_aktiv=True
        g=main.NebelseetalApp.__new__(main.NebelseetalApp)
        g.state=z;g.karten_siedlung=s;g.karten_feld=i;g._render_view=lambda:None
        meldungen=[];g._log=meldungen.append
        return g,meldungen
    def test_original_grundrate_erlaubt_steinmetz_abriss(self):
        s=self.ort();self.einsetzen(s,'holzfaeller',('wald',));i=self.einsetzen(s,'steinmetz',('berg',))
        kopie=copy.deepcopy(s)
        g,log=self.gui(s,i);g._karten_abreissen()
        self.assertNotIn(str(i), s.bauten)
        self.assertFalse(any('VERSORGUNGSWARNUNG' in t for t in log))
    def test_original_grundrate_erlaubt_holzfaeller_abriss(self):
        s=self.ort();i=self.einsetzen(s,'holzfaeller',('wald',));self.einsetzen(s,'steinmetz',('berg',))
        g,log=self.gui(s,i);g._karten_abreissen()
        self.assertNotIn(str(i),s.bauten)
        self.assertFalse(any('VERSORGUNGSWARNUNG' in t for t in log))
    def test_nicht_lebenswichtiges_gebaeude_abbauen(self):
        s=self.ort();self.einsetzen(s,'holzfaeller',('wald',));self.einsetzen(s,'steinmetz',('berg',))
        i=self.einsetzen(s,'farm',('grasland',))
        g,log=self.gui(s,i);g._karten_abreissen()
        self.assertNotIn(str(i),s.bauten)
    def test_genug_stein_und_holz_fuer_neubau(self):
        s=self.ort(stein=100,holz=100);i=self.einsetzen(s,'holzfaeller',('wald',));self.einsetzen(s,'steinmetz',('berg',))
        self.assertEqual(versorgungsschutz.risiko_nach_abriss(s,i,main.baukosten),[])
    def test_bereits_blockierte_stadt_kann_feld_freimachen(self):
        s=self.ort(stein=0,holz=0)
        i=self.einsetzen(s,'erzmine',('berg',))
        self.assertEqual(versorgungsschutz.risiko_nach_abriss(s,i,main.baukosten),[])
    def test_abriss_pruefung_ist_rein(self):
        s=self.ort(); self.einsetzen(s,'steinmetz',('berg',));i=self.einsetzen(s,'holzfaeller',('wald',))
        kopie=copy.deepcopy(s)
        versorgungsschutz.risiko_nach_abriss(s,i,main.baukosten)
        self.assertEqual(s,kopie)
    def test_legacy_baut_ohne_neue_abriss_sperre_ab(self):
        s=self.ort();i=self.einsetzen(s,'holzfaeller',('wald',))
        g,log=self.gui(s,i);g.state.mode=main.MODUS_LEGACY
        g._karten_abreissen();self.assertNotIn(str(i),s.bauten)
    def test_admin_kann_risiko_abriss_fuer_tests_machen(self):
        s=self.ort();i=self.einsetzen(s,'holzfaeller',('wald',))
        g,log=self.gui(s,i);g.state.admin_teststand=True
        g._karten_abreissen();self.assertNotIn(str(i),s.bauten)

if __name__=='__main__':unittest.main(verbosity=2)
