"""Pruefdatei fuer src/fehlbestand.py - reine Rechnungen, keine Fenster, kein git.

Geprueft wird jede Zusage der Schnittstelle mit echten Zahlen, nicht mit
Platzhaltern: die Fehlmenge muss aus Kosten minus Vorrat aufgehen, die
Reihenfolge muss die der Rezeptur bleiben, und der Text muss exakt so
aussehen, wie die Meldung im Spiel ihn braucht.
"""
from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

ROOT, SRC = import_src()
import fehlbestand as F

abschnitt('Fehlende Menge ist genau die Differenz')
kosten = {'holz': 100}
vorrat = {'holz': 37.2}
fehlt = F.fehlbestand(vorrat, kosten)
check('holz 100 gebraucht, 37.2 da -> 62.8 fehlt',
      fehlt == {'holz': 62.8} and fehlt['holz'] == 100 - 37.2, str(fehlt))
check('nur der fehlende Rohstoff steht im Ergebnis',
      list(fehlt) == ['holz'] and 'stein' not in fehlt, str(list(fehlt)))
check('genau ausreichender Vorrat ergibt nichts',
      F.fehlbestand({'holz': 100}, {'holz': 100}) == {}, str(F.fehlbestand({'holz': 100}, {'holz': 100})))
check('Vorrat ueber Bedarf ergibt nichts',
      F.fehlbestand({'holz': 240}, {'holz': 100}) == {}, str(F.fehlbestand({'holz': 240}, {'holz': 100})))

abschnitt('Bedarf ohne Vorratseintrag')
fehlt2 = F.fehlbestand({'holz': 5}, {'stein': 50, 'holz': 5})
check('Kosten ohne Vorrat zaehlen voll als fehlend',
      fehlt2 == {'stein': 50.0} and fehlt2['stein'] == 50 - 0, str(fehlt2))
check('leerer Vorrat: jeder Bedarf ist voll fehlend',
      F.fehlbestand({}, {'holz': 10, 'stein': 2.5}) == {'holz': 10.0, 'stein': 2.5},
      str(F.fehlbestand({}, {'holz': 10, 'stein': 2.5})))
check('Rohstoff im Vorrat, aber ohne Bedarf, wird nicht gemeldet',
      F.fehlbestand({'gold': 999}, {'holz': 10}) == {'holz': 10.0},
      str(F.fehlbestand({'gold': 999}, {'holz': 10})))

abschnitt('Robustheit: negativer Vorrat, Text-Zahlen, Unfug')
check('negativer Vorrat zaehlt als 0 (30 gebraucht, -12 da -> 30 fehlt)',
      F.fehlbestand({'holz': -12}, {'holz': 30}) == {'holz': 30.0},
      str(F.fehlbestand({'holz': -12}, {'holz': 30})))
check('String-Zahl im Vorrat wird gelesen (\"100\" deckt 100)',
      F.fehlbestand({'holz': '100'}, {'holz': 100}) == {},
      str(F.fehlbestand({'holz': '100'}, {'holz': 100})))
check('String-Zahl mit Nachkommastelle (\" 37.5 \") wird gelesen',
      F.fehlbestand({'holz': ' 37.5 '}, {'holz': 100}) == {'holz': 62.5},
      str(F.fehlbestand({'holz': ' 37.5 '}, {'holz': 100})))
check('Text ohne Zahl (\"viel\") zaehlt als 0 -> voll fehlend',
      F.fehlbestand({'holz': 'viel'}, {'holz': 20}) == {'holz': 20.0},
      str(F.fehlbestand({'holz': 'viel'}, {'holz': 20})))
check('None als Vorrat und als Wert stuerzt nicht ab',
      F.fehlbestand(None, {'holz': 7}) == {'holz': 7.0}
      and F.fehlbestand({'holz': None}, {'holz': 7}) == {'holz': 7.0},
      str(F.fehlbestand(None, {'holz': 7})))
check('bool zaehlt als 0, nicht als 1',
      F.fehlbestand({'holz': True}, {'holz': 5}) == {'holz': 5.0},
      str(F.fehlbestand({'holz': True}, {'holz': 5})))
check('negativer Bedarf wird nicht zum Fehlbestand',
      F.fehlbestand({'holz': 0}, {'holz': -5}) == {},
      str(F.fehlbestand({'holz': 0}, {'holz': -5})))

abschnitt('Rundung auf 2 Stellen ohne Gleitkomma-Reste')
fehlt3 = F.fehlbestand({'holz': 37.2}, {'holz': 100})
roh = str(fehlt3['holz'])
check('62.800000000000004 kommt nicht vor',
      roh == '62.8' and '0000000' not in roh, roh)
check('jeder Wert ist schon auf 2 Stellen gerundet',
      all(v == round(v, 2) for v in fehlt3.values()), str(fehlt3))
fehlt4 = F.fehlbestand({'ton': 3.331}, {'ton': 10.005})
check('dritte Stelle wird gerundet (10.005 - 3.331 = 6.674 -> 6.67)',
      fehlt4 == {'ton': 6.67}, str(fehlt4))
check('Rest unter der Rundungsstelle verschwindet (0.001 fehlt nicht)',
      F.fehlbestand({'holz': 99.999}, {'holz': 100}) == {},
      str(F.fehlbestand({'holz': 99.999}, {'holz': 100})))

abschnitt('Kurztext')
check('leeres fehlt ergibt leeren Text', F.text({}, vorrat, kosten) == '',
      repr(F.text({}, vorrat, kosten)))
check('ein Rohstoff steht genau im Format',
      F.text({'holz': 62.8}, {'holz': 37.2}, {'holz': 100}) == 'holz fehlt 62.80 (37.20 von 100)',
      repr(F.text({'holz': 62.8}, {'holz': 37.2}, {'holz': 100})))
zwei = F.fehlbestand({'holz': 37.2, 'stein': 90}, {'holz': 100, 'stein': 150})
zwei_text = F.text(zwei, {'holz': 37.2, 'stein': 90}, {'holz': 100, 'stein': 150})
check('zwei Rohstoffe durch ", " getrennt',
      zwei_text == 'holz fehlt 62.80 (37.20 von 100), stein fehlt 60.00 (90 von 150)',
      repr(zwei_text))
check('Reihenfolge bleibt die der Rezeptur, nicht alphabetisch',
      [n for n in zwei] == ['holz', 'stein'] and zwei_text.index('holz') < zwei_text.index('stein'),
      str(list(zwei)))
check('keine Gleitkomma-Reste im Text',
      '0000000' not in zwei_text and re.search(r'\d\.\d{3}', zwei_text) is None, zwei_text)
check('Rohstoffnamen bleiben unveraendert (kein Umschreiben)',
      'Nahrung fehlt' in F.text({'Nahrung': 3}, {'Nahrung': 1}, {'Nahrung': 4}),
      repr(F.text({'Nahrung': 3}, {'Nahrung': 1}, {'Nahrung': 4})))

abschnitt('Leere Kostenliste')
check('kosten leer -> {} und Text ""',
      F.fehlbestand({'holz': 100}, {}) == {} and F.text({}, {'holz': 100}, {}) == '',
      str(F.fehlbestand({'holz': 100}, {})))
check('kosten None wird wie leer behandelt',
      F.fehlbestand({'holz': 100}, None) == {}, str(F.fehlbestand({'holz': 100}, None)))

abschnitt('Baustein bleibt projektunabhaengig')
quelle = open(os.path.join(SRC, 'fehlbestand.py'), encoding='utf-8').read()
importe = [z.strip() for z in quelle.splitlines()
           if z.strip().startswith(('import ', 'from '))]
check('nur Standardbibliothek importiert (math, __future__)',
      importe == ['from __future__ import annotations', 'import math'], str(importe))
check('kein Zugriff auf Spielmodule im Quelltext',
      not any(m in quelle for m in ('import spieloekonomie', 'import main', 'import wirtschaft')),
      str(len(quelle)) + ' Zeichen')
sys.exit(bericht())
