"""GPT-OEK04: wirtschaftliche Kette auf echten 10x10-Karten.

Bau mit echten Kosten -> lokale Werkstatt -> Rezept und Zeit -> Warenlager
-> Originalausruestung -> Ausbildung und Zeit -> Truppenlager -> eigener
Karrentransport und Ankunft. Keine versteckten Rohstoffgeschenke.
"""
from __future__ import annotations
from dataclasses import asdict
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'tools')]
import main
import spieloekonomie
import gpt_erzeuge_startstaende

class TestWirtschaftKette(unittest.TestCase):
    def setUp(self):
        self.g = gpt_erzeuge_startstaende.neu_erzeugen()
        self.o = self.g.settlements[0]
        self.o.vorraete.update({'metall': 100., 'leder': 100., 'nahrung': 500.,
                                'gold': 1000., 'wolle':100.})
        self.g._reichsanzeige_aus_orten()
        self.technik={'Baukunst':1, 'Waffentechnik':3, 'Nähkunst':1,
                      'Rüstungsbau':2, 'Kriegskunst':1, 'Wagenbau':1}
        for n,v in self.technik.items():
            self.g.research[n].level=v

    def bauen(self,geb):
        i=next(i for i,art in enumerate(self.o.karte['raster'])
               if str(i) not in self.o.bauten and gelaende_bau(geb,art))
        preis=main.baukosten(geb)
        v=(self.o.vorraete['holz'],self.o.vorraete['stein'])
        deckung=self.g.ortsdeckung(self.o,preis)
        self.assertEqual(deckung,{})
        ok,msg=self.g.verbrauche_am_ort(self.o,preis)
        self.assertTrue(ok,msg)
        ok,msg=main.bauen_auf_karte(self.o,geb,i,self.technik)
        self.assertTrue(ok,msg)
        self.assertEqual(self.o.vorraete['holz'],v[0]-preis.get('holz',0))
        self.assertEqual(self.o.vorraete['stein'],v[1]-preis.get('stein',0))
        return i

    def uebernehmen(self, daten):
        self.assertTrue(self.g._ort_uebernehmen(self.o.id,daten))

    def test_werkstatt_und_kaempfer_echte_waren_und_zeit(self):
        for geb in ('schmiede','naehstube','kriegerakademie'):
            self.bauen(geb)
        vorher=dict(self.o.vorraete)
        for ware in ('Kurzschwert','Lederrüstung'):
            self.uebernehmen(spieloekonomie.ware_start(asdict(self.o),ware,self.technik,
                                                       self.g.spielsekunden))
        self.assertEqual(self.o.waren, {})
        self.assertEqual(self.o.vorraete['metall'],vorher['metall']-4)
        self.assertEqual(self.o.vorraete['leder'],vorher['leder']-4)
        self.g.tick(9000)
        self.assertEqual(self.o.waren['Kurzschwert'],1)
        self.assertEqual(self.o.waren['Lederrüstung'],1)
        before_gold=self.o.vorraete['gold']
        before_people=self.o.bevoelkerung
        self.uebernehmen(spieloekonomie.ausbildung_start(asdict(self.o),'Kämpfer',
                                                        self.technik,self.g.spielsekunden))
        self.assertEqual(self.o.vorraete['gold'],before_gold-250)
        self.assertEqual(self.o.bevoelkerung,before_people-1)
        self.assertEqual(self.o.waren['Kurzschwert'],0)
        self.assertEqual(self.o.waren['Lederrüstung'],0)
        self.assertEqual(self.o.einheiten.get('Kämpfer',0),0)
        self.g.tick(1200)
        self.assertEqual(self.o.einheiten['Kämpfer'],1)
        self.g.tick(1200)
        self.assertEqual(self.o.einheiten['Kämpfer'],1)

    def test_ausbildung_ohne_waren_keine_abbuchung(self):
        self.bauen('kriegerakademie')
        vor=asdict(self.o)
        with self.assertRaisesRegex(ValueError,'Ausrüstung'):
            spieloekonomie.ausbildung_start(asdict(self.o),'Kämpfer',
                                           self.technik,self.g.spielsekunden)
        self.assertEqual(asdict(self.o),vor)

    def test_warenbau_ohne_forschung_keine_abbuchung(self):
        self.bauen('schmiede')
        vor=asdict(self.o)
        with self.assertRaisesRegex(ValueError,'Warenvoraussetzung'):
            spieloekonomie.ware_start(asdict(self.o),'Kurzschwert',
                                      {'Waffentechnik':0},0)
        self.assertEqual(asdict(self.o),vor)

    def test_handkarren_entsteht_nur_nach_ausbildung_und_fracht_nur_am_ziel(self):
        self.bauen('stellmacher')
        # Gebaude- und Einheitenkosten werden aus den Regeldaten gelesen;
        # Waren, die ein Karren nicht benoetigt, werden nicht erfunden.
        # 100 Start-Holz reichen nach dem Stellmacherbau noch nicht. Die
        # historisch belegte Grundrate holt den Mangel durch Spielzeit ein.
        self.g.tick(40 * 3600)
        self.assertGreaterEqual(self.o.vorraete['holz'],100)
        v=asdict(self.o)
        v=spieloekonomie.ausbildung_start(v,'Handkarren',self.technik,self.g.spielsekunden)
        self.uebernehmen(v)
        self.assertFalse(self.o.einheiten.get('Handkarren'))
        self.g.tick(1200)
        self.assertEqual(self.o.einheiten.get('Handkarren'),1)
        ziel=main.Settlement(id='spielerdorf2', name='Kolonie', map_id='kontinent',
                             x=self.o.x+1,y=self.o.y,besitzer='spieler',dimension=1,
                             karte=spieloekonomie.startkarte('zweites', 'spieler'),
                             vorraete={'holz':0.0,'stein':0.0},bevoelkerung=10)
        # Mission ist eine echte Kernbuchung und keine globale Teleportation.
        laden=min(10, int(self.o.vorraete['stein']))
        von=asdict(self.o)
        hin=asdict(ziel)
        vor=von['vorraete']['stein']
        neu,mission=spieloekonomie.transport_start(von,hin,{'Handkarren':1},
                       {'stein':laden},self.g.spielsekunden)
        self.assertEqual(neu['vorraete']['stein'], vor-laden)
        self.assertEqual(hin['vorraete']['stein'],0)
        orte={neu['id']:neu,hin['id']:hin}
        orte,mission=spieloekonomie.transport_fortschritt(mission,orte,mission['ankunft'])
        self.assertEqual(orte[hin['id']]['vorraete']['stein'],laden)
        self.assertEqual(orte[neu['id']]['einheiten']['Handkarren'],0)
        orte,mission=spieloekonomie.transport_fortschritt(mission,orte,mission['rueckkehr'])
        self.assertEqual(orte[neu['id']]['einheiten']['Handkarren'],1)
        orte2,m2=spieloekonomie.transport_fortschritt(mission,orte,mission['rueckkehr']+1)
        self.assertEqual(orte2,orte)


def gelaende_bau(geb,art):
    return main.gelaende.bau_moeglich(geb,art)[0]

if __name__=='__main__': unittest.main(verbosity=2)
