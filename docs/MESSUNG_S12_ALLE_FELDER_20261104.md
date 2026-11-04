# Messung S-12: alle Felder nutzen (04.11.2026)

**Wozu:** S-12 verlangt, dass ein Bot-Dorf jedes Feld belegt, das seine Taktik sinnvoll fuellen kann,
und dass die Zahl der Anlagen von Karte zu Karte verschieden ist. Bis zum 04.11. blieb der Huegel
ganz fuer Haus, Bibliothek, Lager, Schmiede, Akademie und Wall frei - auf Huegel-reichen Karten
damit bis zu 24 Felder ungenutzt (gemessen: `original-001` hat 24 Huegelfelder).

## 1. Was gebaut wurde

1. **Huegel steht jetzt in `restfelder`** jeder Taktik (`data/bot_bauplan.json`): Steinmetz zuerst
   (2 je Stunde - der beste Ertrag dort), dann Goldmine oder Erzmine (1,5). Beim Raecher die Erzmine,
   weil Metall sein Engpass ist; bei den anderen die Goldmine.
2. **Die Feldreserve wird am GELAENDE gemessen.** Vorher zaehlte der Code nur, wie viele Felder frei
   sind: auf `original-001` blieben 19 Sumpffelder frei, die Reserve galt als erfuellt, und kein Haus
   fand mehr Platz (`IndexError`, weil gar kein Bibliotheksfeld mehr frei war). Jetzt waehlt
   `main.bot_bauplan_reservierte_felder` fuer jedes OFFENE Gebaeude des Bauplans ein passendes Feld
   (`main.bot_bauplan_offene_liste`) und die Restfeld-Phase fasst diese Felder nicht an.
3. **Das Bibliotheksfeld bleibt geschuetzt**, solange keine Bibliothek steht.

## 2. Messung: 24 Spieltage, echte Bot-Takte

Werkzeug: `python -X utf8 tools/bot_wirtschaft_messung.py --tage 24 --aus <datei>`.

| Bot | Anlagen je Dorf (vor S-12) | Anlagen je Dorf (mit S-12) | Stein in der Kasse (vorher -> jetzt) |
|---|---|---|---|
| Haug (Pluenderer) | 76 / 76 / 76 / 52 | 73 / 73 / 73 / 80 | 18.907 -> 36.296 |
| Brynhild (Waechterin) | 97 / 81 / 85 / 55 | 97 / 83 / 85 / 66 | 32.162 -> 61.395 |
| Grom (Bastionier) | 77 / 76 / 91 / 83 | 74 / 73 / 98 / 92 | 25.882 -> 53.719 |
| Silra (Spaeherin) | 84 / 84 / 78 / 56 | 90 / 90 / 82 / 63 | 15.801 -> 59.345 |
| Krank (Raecher) | 85 / 64 / 91 / 76 | 90 / 97 / 95 / 77 | 16.349 -> 56.396 |

**Dorfzahl unveraendert 4/4/4/4/4.** Die Anlagenzahl ist je Karte verschieden (63 bis 98) - das ist
die zweite Pruefzusage von S-12 (vorher 52 bis 97).

## 3. Befund: Stein laeuft ueber

Der Huegel traegt nach Ertrag den Steinmetz - und Stein ist in diesem Spiel kein Engpass (300 je
Gruendung gegen 680 Holz). Ergebnis: die Steinvorraete der Bots steigen auf 36.000 bis 61.000 je Bot.
Das ist **kein Fehler**, sondern die Folge der Vorgabe "Restfelder nach Ertrag"; ein Abnehmer fuer
Stein oder ein Umbau (S-13 Abriss und Umbau) ist der naechste Schritt dafuer. Bis dahin bleibt der
Lagerdeckel (`hoechstvorrat_je_stoff`, 20.000 je Stoff und Dorf) die Bremse.

**Sumpf und Nebelsee bleiben ungenutzt** - auf Sumpf darf kein Gebaeude stehen, auf Nebelsee nur die
Bibliothek. Das ist eine Regel des Spiels, keine Luecke im Plan.

## 4. Pruefstand

- Wache `tests/test_s8_stufe3_bauplaene.py` **185/0/0** (Abschnitt 9 ist neu: Huegel traegt Anlagen,
  Sumpf nie, alles Nutzbare ist belegt oder reserviert, und der Plan baut auf fuenf Karten ohne
  Absturz - auch wenn kein Bibliotheksfeld mehr frei ist).
- Gegenprobe: Huegel-Fuellung abgeschaltet (aus `restfelder` entfernt) - **20 Pruefungen rot**,
  `data/bot_bauplan.json` per SHA256 unveraendert zurueck.
