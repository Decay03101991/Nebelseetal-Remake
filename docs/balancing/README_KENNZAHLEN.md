# Kennzahlenblatt - wie gemessen wird

Ablauf Schritt 2 (`docs/ABLAUF_LLM_20261106.md`, entschieden von Daniel am 06.11.2026, F-5).
Zweck: ab dem Rachetopf (Schritt 4) veraendert jeder Umbau das Spielgefuehl. Ohne eine Vorher-Zahl
ist "besser" nur ein Gefuehl - mit ihr ist jede Aenderung messbar.

## Erzeugen

```
.venv/Scripts/python.exe -X utf8 tools/spieltest_simulation.py --tage 12 --kennzahlen
```

Das schreibt

* `docs/balancing/kennzahlen.jsonl` - EINE Zeile je Partie, angehaengt (nichts wird ueberschrieben),
* `docs/balancing/KENNZAHLEN_<JJJJ-MM-TT>.md` - die lesbare Tabelle ueber ALLE Zeilen des Tages,
* daneben wie immer `docs/audits/SPIELTEST_LOG_<datum>.md` - der volle Verlauf.

Der Spieltest selbst bleibt, wie er war; ohne `--kennzahlen` entsteht keine Zeile.

## Die Schluessel und woher sie kommen

| Schluessel | Bedeutung | Herkunft |
|---|---|---|
| `startwert` | Saat, Stil, Laenge - die volle Eingabe des Laufs | Parameter des Laufs |
| `stand` | Kopf-Commit und ob der Arbeitsbaum sauber war | `git rev-parse`, `git status` (nur lesend) |
| `daten_hash` | Pruefsumme ueber alle `data/*.json` | `daten_hash()` |
| `tag_erstes_haus` | Spieltag des ersten Hauses | Zustand der Siedlung |
| `tag_erste_bibliothek` | Spieltag der ersten Bibliothek | Zustand der Siedlung |
| `tag_erste_ware` | Spieltag der ersten FERTIGEN Ware im Lager | Warenlager |
| `tag_erster_krieger` | Spieltag der ersten Kampfeinheit im Heer | Einheiten des Reichs |
| `tag_erstes_gefecht` | Spieltag des ersten GEFOCHTENEN Gefechts | Rueckgabe von `spielschicht.angriff` |
| `ruhm_stufe` | Ruhm-Stufe zum Endpunktestand | `postfach.rang` (dieselbe Lesestelle wie die Anzeige) |
| `ausgaben` | je Rohstoff die Summe der Abbuchungen | Reichskasse vor/nach den Aktionen eines Schritts |
| `leerlauf_sek` | Spielsekunden ohne eine einzige erfolgreiche Aktion | Schrittzahl x 1200 s |
| `fehlschlaege` | die haeufigsten Gruende (Aktion, Grund, Anzahl), Zahlen im Grund zu `#` | `log['fehlschlaege']` |
| `handelspunkte` | Handelspunkte am Ende, `null` solange der Zaehler fehlt (Befund G-8) | `punkte.handelspunkte` |
| `beute_je_feldzug` | Beute je Gefecht | Gefechtsergebnis |
| `verluste_je_gefecht` | eigene Verluste je Gefecht | Gefechtsergebnis |
| `abstand_meilensteine_max` | laengste Strecke ohne neuen Meilenstein (Spieltage) | Abstand der Meilensteine |

**`null` heisst nicht 0.** Ein Meilenstein, der nie erreicht wurde, steht als `null`; wer 0
schreibt, macht "nicht erreicht" von "bei Tag 0 erreicht" ununterscheidbar. Dasselbe gilt fuer
`handelspunkte`: solange es keinen Zaehler gibt, ist der Wert NICHT GEMESSEN.

## Warum zwei Laeufe dieselbe Zeile ergeben

Der Lauf bekommt EINEN festen Zufallsgenerator (`random.Random(saat)`) und gibt ihn an jedes
Gefecht weiter (`spielschicht.angriff(..., rng=)`). Vorher zog `kampf.fuehre_schlacht` bei jedem
Gefecht ein neues `random.Random()` - derselbe Startwert ergab dann andere Zahlen, und eine
Vorher-Zahl waere nichts wert gewesen. Gemessen am 06.11.2026: zwei Laeufe ueber 12 Spieltage sind
Zeichen fuer Zeichen gleich (2.596 Byte je Zeile).

Der Zeitstempel gehoert deshalb NICHT in die Zeile - er steht nur im Dateinamen und im Kopf der
Markdown-Fassung.

## Erste Messung (Vorher-Zahl fuer die Schritte 3 bis 6)

Partie `Saat 7, Stil breit, 12 Spieltage`, Datenstand `daten_hash sha256:048225466a...`:

* erstes Haus **Tag 2,486**, erste Bibliothek **0,042**, erste Ware **7,833**,
  erster Krieger **1,167**, erstes Gefecht **Tag 2,0**
* Ruhm-Stufe **2**, Beute **190** Rohstoffe in **6** Gefechten, eigene Verluste **0**
* **Leerlauf 956.400 s von 1.036.800 s** (92 % der Partie ohne eine einzige erfolgreiche Aktion) -
  der laengste Abschnitt ohne neuen Meilenstein ist **5,347 Spieltage**.
  Das ist die eigentliche Zahl dieser Messung: die Spielerpolitik steht die meiste Zeit still
  ("alle Gebaeude der Kette stehen (je 2)", Ausbau zu teuer, Kurzschwert braucht Waffentechnik 3).
  Sie ist ein Befund ueber den AUTOMATEN, nicht ueber das Spiel - und die Vorher-Zahl, gegen die
  Schritt 8 (Sollkurve) und Schritt 9 (Regelkreis) antreten.
* `handelspunkte` ist `null`: der Zaehler fehlt noch (Befund G-8, Schritt 6 des Ablaufs).

## Wachen

`tests/test_kennzahlenblatt.py` (21 Pruefungen): Pflichtschluessel vollstaendig, zwei Laeufe
identisch, fehlender Meilenstein `null` und ein frueher `0`, `daten_hash` folgt dem Datenstand,
und das Schreiben fasst ausschliesslich `docs/balancing/` an - `data/` und `src/` bleiben Byte
fuer Byte unberuehrt.
