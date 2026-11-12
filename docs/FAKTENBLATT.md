# FAKTENBLATT - automatisch gezaehlt aus `data/` (M11)

**Erzeugt:** 12.11.2026 23:39 · **Stand von `data/`:** 12.11.2026 18:30 (`b1a6189`)

> **Nicht von Hand aendern.** Diese Datei entsteht mit `python -X utf8 tools/faktenblatt.py`; die Wache `test_faktenblatt` meldet jede Abweichung zwischen Blatt und Daten. Wer eine Zahl im Auftrag nennt, nimmt sie von hier - dann wandern keine abgetippten Zahlen mehr in Rezepte.

## Waren, Rezepte, Zutaten

| Groesse | Zahl | Quelle |
|---|---|---|
| Waren | **17** | `data/items.json` (`waren`) |
| Rezepte | **17** | `data/warenrezepte.json` |
| hoechste Zutatenzahl je Rezept | **1** | `data/warenrezepte.json` (`kosten`) |
| Rezepte mit holz | 4 (Summe 33) | `warenrezepte.json` |
| Rezepte mit metall | 8 (Summe 37) | `warenrezepte.json` |
| Rezepte mit wolle | 2 (Summe 4) | `warenrezepte.json` |
| Rezepte mit leder | 3 (Summe 16) | `warenrezepte.json` |
| Rezepte ohne Zutaten | 0 | `warenrezepte.json` |
| Waren ohne Rezept | 0 | Abgleich `items.json` gegen `warenrezepte.json` |

## Werkstaetten

Quelle: data/items.json, Feld werkstatt. **Die Rezepte tragen noch KEIN Feld `werkstatt`** (F-61/F-64 offen) - die Zuordnung steht heute nur an der Ware.

| Werkstatt | Waren | Anzahl |
|---|---|---|
| Bogner | Armbrust, Bogen, Kurzbogen, Langbogen | **4** |
| Nähstube | Diebesumhang, Fellrüstung, Fellumhang, Lederrüstung, Wollumhang | **5** |
| Schmiede | Dolch, Kettenhemd, Kurzschwert, Magischer Paladinharnisch, Messer, Plattenrüstung, Schwert, Zweihänder | **8** |

## Einheiten, Forschungen, Gebaeude

| Groesse | Zahl | Quelle |
|---|---|---|
| Einheiten | **28** | `data/units.json` |
| Forschungen | **21** | `data/research.json` |
| Gebaeude | **20** | `data/buildings.json` |
| davon Ausbildung | 3 | `buildings.json` (`kategorie`) |
| davon Produktion | 10 | `buildings.json` (`kategorie`) |
| davon Sonstiges | 3 | `buildings.json` (`kategorie`) |
| davon Verteidigung | 1 | `buildings.json` (`kategorie`) |
| davon Werkstatt | 3 | `buildings.json` (`kategorie`) |

## Voelker, Welten, Gelaende

| Groesse | Zahl | Quelle |
|---|---|---|
| Voelker | **6** | `data/voelker.json` |
| Welten | **6** | `data/welten.json` |
| Welten mit Heimatwelt | _nicht gefuehrt_ | `data/welten.json` hat kein Feld `heimatwelt` je Welt (Stand 12.11.2026) |
| Gelaendearten | **7** | `data/gelaende.json` |

## Textbreiten (Tk, 16 px)

| Name | Breite |
|---|---|
| laengster Warenname: Magischer Paladinharnisch | **188 px** |
| laengster Einheitenname: Große Handelskarawane | **173 px** |

