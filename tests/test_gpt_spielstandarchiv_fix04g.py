# -*- coding: utf-8 -*-
"""FIX04g: private Spielstand-Archive und Verwalten; Testdaten nur in tempfile."""

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['admin_teststand', 'main:*', 'speichern', 'spielstaende', 'spielstand_archiv']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------
import os                     # von der uebernommenen Klasse gebraucht (F-81)
import json
import sys
import tempfile
import tkinter as tk
import unittest
from pathlib import Path
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import spielstand_archiv as archiv
import spielstaende
import speichern
import main

class SaveArchiv(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root = Path(self.t.name)
        self.p = Path(spielstaende.slot_pfad(str(self.root), 1))
        self.p.write_text('{"day": 3, "admin_teststand": false}',encoding='utf-8')

    def test_ordner_bereit(self):
        struktur = archiv.ordner_anlegen(str(self.root))
        for x in ('spieler/slot_1','spieler/slot_2','spieler/slot_3',
                  'admin','testbereinigung','abgebrochen'):
            self.assertTrue((struktur/x).is_dir())

    def test_loeschen_verschiebt_mit_datum(self):
        ok,ziel=archiv.archiviere(str(self.p),'spieler','Vom Spieler gel\u00f6scht')
        self.assertTrue(ok,ziel)
        self.assertFalse(self.p.exists())
        self.assertTrue(Path(ziel).exists())
        self.assertEqual(json.loads(Path(ziel).read_text(encoding='utf-8'))['day'],3)
        self.assertRegex(Path(ziel).parent.name,r'^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}')
        self.assertEqual(json.loads((Path(ziel).parent/'ARCHIV_INFO.json').read_text(encoding='utf-8'))['grund'],'Vom Spieler gel\u00f6scht')

    def test_archive_niemals_ueberschrieben(self):
        ok,z1=archiv.archiviere(str(self.p),'spieler','test')
        self.assertTrue(ok)
        self.p.write_text('{"day":9}',encoding='utf-8')
        ok,z2=archiv.archiviere(str(self.p),'spieler','test')
        self.assertTrue(ok)
        self.assertNotEqual(z1,z2)
        self.assertEqual(len(archiv.archivierte_staende(str(self.root),'spieler',1)),2)

    def test_sicherung_bei_loeschen_mit_im_archiv(self):
        bak=Path(str(self.p)+'.bak');bak.write_text('backup',encoding='utf-8')
        ok,z=archiv.archiviere(str(self.p),'spieler','test')
        self.assertTrue(ok)
        self.assertFalse(bak.exists())
        self.assertEqual((Path(z).parent/bak.name).read_text(encoding='utf-8'),'backup')

    def test_bewusstes_ueberschreiben_legt_kein_archiv_an(self):
        self.assertTrue(speichern.speichere({'day':77},str(self.p))[0])
        self.assertEqual(json.loads(self.p.read_text(encoding='utf-8'))['day'],77)
        self.assertEqual(archiv.archivierte_staende(str(self.root),'spieler',1),[])

    def test_restore_keine_heimliche_ueberschreibung(self):
        ok,z=archiv.archiviere(str(self.p),'spieler','test')
        self.assertTrue(ok)
        self.p.write_text('{"day":12}',encoding='utf-8')
        ok,m=archiv.wiederherstellen(z,str(self.p))
        self.assertFalse(ok)
        self.assertEqual(json.loads(self.p.read_text(encoding='utf-8'))['day'],12)
        ok,m=archiv.wiederherstellen(z,str(self.p),ueberschreiben=True)
        self.assertTrue(ok,m)
        self.assertEqual(json.loads(self.p.read_text(encoding='utf-8'))['day'],3)
        self.assertTrue(Path(z).exists())

    def test_admin_eigenes_archiv_kein_spielerslot(self):
        p=Path(spielstaende.admin_pfad(str(self.root)))
        p.write_text('{"day":42,"admin_teststand":true}',encoding='utf-8')
        self.assertFalse(archiv.archiviere(str(p),'spieler','test')[0])
        ok,z=archiv.archiviere(str(p),'admin','test')
        self.assertTrue(ok,z)
        self.assertIn('/admin/',str(Path(z)).replace('\\','/'))
        self.assertFalse(archiv.wiederherstellen(z,str(self.p),ueberschreiben=True)[0])

    def test_archiv_darf_keine_fremde_datei_wiederherstellen(self):
        fremd=self.root/'fremd.json';fremd.write_text('{"day":1}',encoding='utf-8')
        self.assertFalse(archiv.wiederherstellen(str(fremd),str(self.p),ueberschreiben=True)[0])

    def test_tmp_reste_archiviert_statt_geloescht(self):
        p=self.root/'savegame.json';temp=Path(str(p)+'.tmp')
        temp.write_text('halbfertige testdatei',encoding='utf-8')
        entfernt=speichern.aufraeumen(str(p))
        self.assertIn(str(temp),entfernt)
        self.assertFalse(temp.exists())
        z=list((archiv.archivwurzel(str(self.root))/'abgebrochen').glob('*/savegame.json.tmp'))
        self.assertEqual(len(z),1)
        self.assertEqual(z[0].read_text(encoding='utf-8'),'halbfertige testdatei')

    def test_fehler_beim_archivieren_laesst_spielstand_stehen(self):
        self.assertFalse(archiv.archiviere(str(self.p),'nicht_erlaubt','x')[0])
        self.assertTrue(self.p.exists())

class SpeicherGUI(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
        self.root=tk.Tk();self.root.withdraw();self.addCleanup(self.root.destroy)
        with patch.dict('os.environ',{'NEBEL_SPIELDATEN_ORDNER':self.t.name}):
            self.app=main.NebelseetalApp(self.root,tor_pfad=str(Path(self.t.name)/'tor_test.json'))
        self.app._tor_geoeffnet=True

    def test_spieler_hat_verwaltung_ohne_admin(self):
        self.app._profil='spieler'
        self.assertTrue(self.app._spielstand_verwaltung('spieler'))
        for widget in self.root.winfo_children():
            if isinstance(widget,tk.Toplevel):widget.destroy()
        self.assertFalse(self.app._spielstand_verwaltung('admin'))

    def test_gui_loeschen_wiederherstellen_wirklich(self):
        self.app._profil='spieler'
        pfad=Path(spielstaende.slot_pfad(self.t.name, 1))
        pfad.write_text('{"day":3,"admin_teststand":false}',encoding='utf-8')
        self.assertTrue(self.app._spielstand_verwaltung('spieler'))
        fenster=next(w for w in self.root.winfo_children() if isinstance(w,tk.Toplevel))
        def buttons(w):
            erg=[]
            for x in w.winfo_children():
                if isinstance(x,tk.Button):erg.append(x)
                erg+=buttons(x)
            return erg
        with patch('tkinter.messagebox.askyesno',return_value=True):
            next(b for b in buttons(fenster) if b.cget('text')=='L\u00f6schen (archivieren)' and str(b.cget('state'))=='normal').invoke()
        self.assertFalse(pfad.exists())
        self.assertEqual(len(archiv.archivierte_staende(self.t.name,'spieler',1)),1)
        # FIX04h: geloeschte Staende sind im normalen Spieler-Menue nicht
        # automatisch angeboten, bleiben fuer autorisierte Entwickler erhalten.
        self.assertFalse(any('Wiederherstellen' in b.cget('text') for b in buttons(fenster)))
        fenster.destroy()
        self.app._profil = 'admin'
        self.app.state.admin_teststand = True
        self.app._admin_sitzung_freigegeben = True
        self.assertTrue(self.app._archiv_wiederherstellung_dialog('spieler', self.t.name, self.root))
        dialog = next(w for w in self.root.winfo_children() if isinstance(w,tk.Toplevel))
        # FIX04i: Das Schild-Hintergrundlayout verschachtelt die Widgets
        # in einer lesbaren Bedienflaeche. Daher rekursiv nach der Liste suchen.
        def alle(w):
            for kind in w.winfo_children():
                yield kind
                yield from alle(kind)
        optionen = [w for w in alle(dialog) if isinstance(w, tk.Listbox)]
        self.assertEqual(optionen[0].size(),1)
        self.assertIn('Slot 1',optionen[0].get(0))
        optionen[0].selection_set(0)
        with patch('tkinter.messagebox.askyesno',return_value=True):
            next(b for b in buttons(dialog) if b.cget('text')=='Ausgew\u00e4hlten Stand wiederherstellen').invoke()
        self.assertTrue(pfad.exists())
        self.assertEqual(json.loads(pfad.read_text(encoding='utf-8'))['day'],3)
        dialog.destroy()

    def test_admin_getrennte_berechtigung(self):
        self.app._profil='admin';self.app.state.admin_teststand=True
        self.assertFalse(self.app._spielstand_verwaltung('admin'))
        self.app._admin_sitzung_freigegeben=True
        self.assertTrue(self.app._spielstand_verwaltung('admin'))
        self.assertFalse(self.app._spielstand_verwaltung('spieler'))


# F-81 (Daniel 13.11.2026: "Name fuer Name uebernehmen, dann streichen"): uebernommen aus
# `tests/test_gpt_spielstand_gui_fix04h.py`, unveraendert. gleiche Pruefart (Fenster), gleicher Gegenstand (Spielstand-Archiv).


def widgets(rahmen, typ):
    aus = []
    for kind in rahmen.winfo_children():
        if isinstance(kind, typ):
            aus.append(kind)
        aus.extend(widgets(kind, typ))
    return aus


class ArchivGuiFix04h(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = tk.Tk()
        self.root.withdraw()
        self.addCleanup(self.root.destroy)
        with patch.dict(os.environ, {'NEBEL_SPIELDATEN_ORDNER': self.tmp.name}):
            self.app = main.NebelseetalApp(self.root,
                tor_pfad=str(Path(self.tmp.name) / 'tor_test.json'))
        self.app._tor_geoeffnet = True
        self.app._profil = 'spieler'
        self.slot2 = Path(spielstaende.slot_pfad(self.tmp.name, 2))
        self.slot2.write_text('{"day": 1, "admin_teststand": false}', encoding='utf-8')
        ok, self.archiv2 = archiv.archiviere(str(self.slot2), 'spieler', 'test')
        self.assertTrue(ok)

    def test_normaler_spieler_sieht_keine_archivliste_und_keinen_restore_button(self):
        self.assertTrue(self.app._spielstand_verwaltung('spieler'))
        fenster = next(w for w in self.root.winfo_children() if isinstance(w, tk.Toplevel))
        self.assertFalse(widgets(fenster, tk.Listbox))
        texte = [w.cget('text') for w in widgets(fenster, tk.Button)]
        self.assertFalse(any('Wiederherstellen' in txt or 'Entwicklerarchiv' in txt for txt in texte))
        self.assertFalse(widgets(fenster, tk.ttk.Combobox) if hasattr(tk, 'ttk') else False)
        fenster.destroy()

    def test_normaler_spieler_kommt_nicht_ueber_direkten_aufruf_ins_archiv(self):
        self.assertFalse(self.app._archiv_wiederherstellung_dialog('spieler', self.tmp.name, self.root))
        self.assertFalse(any(isinstance(w, tk.Toplevel) for w in self.root.winfo_children()))

    def test_admin_archiv_zeigt_nur_echte_slot2_archivversion(self):
        self.app._profil = 'admin'
        self.app.state.admin_teststand = True
        self.app._admin_sitzung_freigegeben = True
        self.assertTrue(self.app._archiv_wiederherstellung_dialog('spieler', self.tmp.name, self.root))
        fenster = next(w for w in self.root.winfo_children() if isinstance(w, tk.Toplevel))
        listen = widgets(fenster, tk.Listbox)
        self.assertEqual(len(listen), 1)
        self.assertEqual(listen[0].size(), 1)
        self.assertIn('Slot 2', listen[0].get(0))
        self.assertNotIn('Slot 3', listen[0].get(0))
        labels = [w.cget('text') for w in widgets(fenster, tk.Label)]
        self.assertTrue(any('Archivgr\u00f6\u00dfe' in txt for txt in labels))
        fenster.destroy()

    def test_admin_restauriert_gezielt_slot2_nach_zweifacher_bestaetigung(self):
        self.app._profil = 'admin'
        self.app.state.admin_teststand = True
        self.app._admin_sitzung_freigegeben = True
        self.app._archiv_wiederherstellung_dialog('spieler', self.tmp.name, self.root)
        fenster = next(w for w in self.root.winfo_children() if isinstance(w, tk.Toplevel))
        liste = widgets(fenster, tk.Listbox)[0]
        liste.selection_set(0)
        with patch('tkinter.messagebox.askyesno', return_value=True) as frage:
            next(w for w in widgets(fenster, tk.Button)
                 if w.cget('text') == 'Ausgew\u00e4hlten Stand wiederherstellen').invoke()
            frage.assert_called_once()
        self.assertTrue(self.slot2.is_file())
        self.assertEqual(json.loads(self.slot2.read_text(encoding='utf-8'))['day'], 1)
        self.assertTrue(Path(self.archiv2).exists())
        fenster.destroy()

    def test_archivgroesse_ohne_dateiloeschung(self):
        anzahl, groesse = archiv.archiv_groesse(self.tmp.name)
        self.assertGreaterEqual(anzahl, 2)  # savegame + metadata
        self.assertGreater(groesse, 0)
        self.assertFalse(self.slot2.exists())
        self.assertTrue(Path(self.archiv2).exists())

    def test_admin_steuerung_ist_gesondert_freigegeben(self):
        self.app._profil = 'admin'
        self.app.state.admin_teststand = True
        self.assertFalse(self.app._spielstand_verwaltung('admin'))
        self.app._admin_sitzung_freigegeben = True
        self.assertTrue(self.app._spielstand_verwaltung('admin'))
        fenster = next(w for w in self.root.winfo_children() if isinstance(w, tk.Toplevel))
        texte = [w.cget('text') for w in widgets(fenster, tk.Button)]
        self.assertIn('Spielerslot-Archive pr\u00fcfen (Admin)', texte)
        fenster.destroy()

if __name__ == '__main__':unittest.main(verbosity=2)
