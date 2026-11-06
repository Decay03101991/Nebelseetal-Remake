# Kennzahlenblatt - 06.11.2026 12:04

Erzeugt von `tools/spieltest_simulation.py --kennzahlen`. Eine Zeile je Partie, dieselben Schluessel bei jedem Lauf. `-` heisst **nicht erreicht oder nicht gemessen** (im JSONL steht dort `null`), nicht `0`. Die Rechenwege stehen in `docs/balancing/README_KENNZAHLEN.md`.

| # | Stand | Saat/Stil/Tage | Haus | Bibliothek | Ware | Krieger | Gefecht | Ruhm | Leerlauf s | Handelspunkte | Beute (Feldzuege) | Verluste (Gefechte) | groesste Luecke |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ddea42d* | 7/breit/12 | 2.486 | 0.042 | 7.833 | 1.167 | 2 | 2 | 956400 | - | 190 in 6 | 0 in 6 | 5.347 |

## Legende

| Schluessel | Bedeutung | Quelle im Werkzeug |
|---|---|---|
| `startwert` | Saat, Stil und Laenge des Laufs - die volle Eingabe | `startwert()` |
| `stand` | Kopf-Commit und ob der Arbeitsbaum sauber war (`*` = schmutzig) | `git rev-parse`/`status` |
| `daten_hash` | Pruefsumme ueber alle `data/*.json` - belegt den Datenstand | `daten_hash()` |
| `tag_*` | Spieltag des ERSTEN Ereignisses; `null` = nie erreicht | `_meilensteine_aus_zustand` |
| `ruhm_stufe` | Ruhm-Stufe zum Endpunktestand | `postfach.rang` (EINE Lesestelle) |
| `ausgaben` | je Rohstoff die Summe der Abbuchungen in Spielschritten | Reichskasse vor/nach den Aktionen |
| `leerlauf_sek` | Spielsekunden ohne eine einzige erfolgreiche Aktion | `leerlauf_schritte x 1200` |
| `fehlschlaege` | Aktion, Grund, Anzahl - die haeufigsten Gruende; Zahlen im Grund sind `#` (gruppiert) | `_fehlschlag_gruppen` |
| `handelspunkte` | Handelspunkte am Ende; `null`, solange der Zaehler fehlt (G-8) | `_handelspunkte` |
| `beute_je_feldzug` | Beute je GEFOCHTENEM Gefecht | `log['kaempfe']` |
| `verluste_je_gefecht` | eigene Verluste je Gefecht | Gefechtsergebnis |
| `abstand_meilensteine_max` | laengste Strecke ohne neuen Meilenstein (Spieltage) | `_abstand_meilensteine` |

**Determinismus:** der Lauf bekommt EINEN festen Zufallsgenerator (`random.Random(saat)`) und gibt ihn an jedes Gefecht weiter. Zwei Laeufe mit demselben `startwert` und demselben `stand` ergeben darum dieselbe Zeile.
