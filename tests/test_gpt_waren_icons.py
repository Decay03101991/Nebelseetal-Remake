"""GPT-WI-01: Warenbild-Zuordnung, 28.10.2026; externer GPT-Agent.

Die folgenden Prüfsummen sind der VORHERIGEN Bilddatei in die KORRIGIERTE
Datei zugeordnet. Keine Pixel wurden verändert, nur die sechs Namen getauscht.
"""
import hashlib
import json
import struct
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EXPECTED_HASHES = {'Fellrüstung': '3c57d88c633b2ca44d58c1c13db3710c4af2b3d9d26576378a6287388257b5a8', 'Kettenhemd': '6abebcba353c3eabf8f47ea9d4a8f43a89b31c40cece4a47eee8efc0ca6539cf', 'Magischer Paladinharnisch': 'ffdf1d8c7efc43e3e90c650a0a1359bca87922afd9e176514305539ec6590d1c', 'Lederrüstung': 'bf0dc3856777788b6d9654234399d7837cd31b16d29c7984bb3c14ccf3c88fcd', 'Plattenrüstung': '8ac1df74ebae0f0e9ea09be8bb81770510fbfd33898402bf86cd525765f4c35b', 'Wollumhang': '5edb7d191f48b82117125fc975a3682efa77765874cd339ca9b56875d30eba94'}
EXPECTED_CELLS = {'Fellrüstung': 1, 'Kettenhemd': 3, 'Magischer Paladinharnisch': 5, 'Lederrüstung': 2, 'Plattenrüstung': 4, 'Wollumhang': 8}
EXPECTED_CLEAN_HASHES = {'Fellrüstung': '2f6b203cf8f3f7f92bddf363de4ba17525bf10c6300af79bdb2c4a3c578c37e8', 'Kettenhemd': 'ae3c408f90c1781c71f896d48c9593a3b970ebb56fe09ead40b67cf39512abd7', 'Magischer Paladinharnisch': 'bbbd1b4137dd812975ac87ba59cbf89842a9499b0a34a9acee56b30e4d74aa8a', 'Lederrüstung': '9c32cb509432f44a72c35cec8f88825d650332cf81975d7cccbfec1ad4504fae', 'Plattenrüstung': '15654222e2ff613440b5d1ff3c3a771283b79f09942aa892565b6c7400869287', 'Wollumhang': '676f4dcf533f64f2cab4beb0a92cc1fa7a2e80e0404d10894a4e43091c7ba431'}

class TestWarenbilder(unittest.TestCase):
    def test_original_asset_mapping(self):
        for name, expected in EXPECTED_HASHES.items():
            with self.subTest(name=name):
                icon=(ROOT/'assets/icons/items'/(name+'.png'))
                self.assertTrue(icon.is_file())
                self.assertEqual(hashlib.sha256(icon.read_bytes()).hexdigest(),expected)

    def test_tatsaechlich_geladene_clean_icons(self):
        # main.icon_pfad hat Prioritaet fuer assets/icons/clean/items.
        import sys
        sys.path.insert(0,str(ROOT/'src'))
        from main import icon_pfad
        for name, expected in EXPECTED_CLEAN_HASHES.items():
            with self.subTest(name=name):
                rel='assets/icons/items/'+name+'.png'
                pfad=Path(icon_pfad(rel))
                self.assertIn('clean',pfad.parts)
                self.assertEqual(pfad.name,name+'.png')
                self.assertEqual(hashlib.sha256(pfad.read_bytes()).hexdigest(),expected)

    def test_alle_17_clean_icons_und_keine_doppelung(self):
        pfade=list((ROOT/'assets/icons/clean/items').glob('*.png'))
        self.assertEqual(len(pfade),17)
        self.assertEqual(len({hashlib.sha256(p.read_bytes()).hexdigest() for p in pfade}),17)

    def test_17_waren_auf_dateien_abbilden(self):
        data=json.loads((ROOT/'data/items.json').read_text(encoding='utf-8'))['waren']
        self.assertEqual(len(data),17)
        paths=[]
        for name, entry in data.items():
            with self.subTest(name=name):
                path=ROOT/entry['icon']
                self.assertTrue(path.is_file())
                raw=path.read_bytes()
                self.assertTrue(raw.startswith(b'\x89PNG\r\n\x1a\n'))
                width,height=struct.unpack('>II',raw[16:24])
                self.assertGreater(width,0)
                self.assertGreater(height,0)
                paths.append(hashlib.sha256(raw).hexdigest())
        self.assertEqual(len(set(paths)),17,'Jede der 17 Waren braucht ihr eigenes Bild')

    def test_iconindex_mit_quellzellen_konsistent(self):
        idx=json.loads((ROOT/'data/icons_index.json').read_text(encoding='utf-8'))['icons']
        for name,cell in EXPECTED_CELLS.items():
            with self.subTest(name=name):
                self.assertEqual(idx[name]['zelle'],cell)
                self.assertEqual(idx[name]['pfad'],'assets/icons/items/'+name+'.png')
                self.assertEqual(idx[name]['blatt'],'RüstungenMäntel_Icons.png')

    def test_originaltafeln_bleiben_vorhanden(self):
        self.assertTrue((ROOT/'assets/quellbilder/waren/RüstungenMäntel_Icons.png').is_file())
        self.assertTrue((ROOT/'assets/quellbilder/waren/WaffenWerkzeuge_Icons.png').is_file())

if __name__=='__main__':
    unittest.main(verbosity=2)
