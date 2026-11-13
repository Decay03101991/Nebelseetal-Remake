# SICHTUNG DER 42 PRUEFNAMEN VON `test_ressourcenleiste` (F-84)

**Auftrag:** Daniel, 13.11.2026 (F-84), woertlich: „Ja, sichten — alte Datei bleibt“.
**Verfahren:** `tools/pruefnamen_abgleich.py` (F-83, neu) vergleicht jede Pruefung des Kandidaten
mit jeder Pruefung des Nachfolgers auf den **gepruefte Gegenstand** — die Bezeichner, die in der
Bedingung wirklich gelesen werden (Funktion, Datenfeld), nicht den Satz. Zwei Pruefungen gelten als
deckungsgleich, wenn sich ihre Gegenstands-Mengen mit Jaccard ab 0,6 ueberschneiden.

**Ergebnis in Zahlen (gemessen, `docs/audits/pruefnamen_gegenstand_20261113.json`):**

| Datei | Pruefungen | woertlich | **Gegenstand** | Nachfolger |
|---|---|---|---|---|
| `test_ressourcenleiste` | 42 | 0.0 % (0) | **21.4 % (9)** | `test_ressourcenleiste_t08` (70) |

**Damit ist die Frage beantwortet:** auch auf den Gegenstand gerechnet deckt T08 nur
**9 von 42** Pruefungen ab. Die alte Datei prueft den Rest
eigenstaendig — sie bleibt. **Es wurde nichts geloescht und nichts uebertragen.**

---

## 1. Die 9 gedeckten Pruefungen (T08 liest denselben Gegenstand)

| Zeile | Pruefname | Gegenstand | Partner | Jaccard |
|---|---|---|---|---|
| 123 | 2 Siedler kommen aus state.population | `main` | 1 elf Felder | 1.00 |
| 125 | 2 Punkte kommen aus punktestand() mit Tausenderpunkt | `main` | 1 elf Felder | 1.00 |
| 128 | 2 ein Rohstoff kommt aus state.resources | `main` | 1 elf Felder | 1.00 |
| 133 | 2 Kommawerte werden abgerundet (nie mehr anzeigen als vorhanden) | `main` | 1 elf Felder | 1.00 |
| 136 | 2 ein fehlender Rohstoff ergibt 0 statt eines Absturzes | `main` | 1 elf Felder | 1.00 |
| 143 | 3 ALLE neun Rohstoffe zeigen in der Detailzeile nur die Rate | `main` | 1 elf Felder | 1.00 |
| 228 | 5 es gibt eine Leistenflaeche im Kopf | `canvas` | 7 es gibt eine Leistenflaeche im Kopf | 1.00 |
| 268 | 6 Bau und Zeichnen lesen die Felder aus `leiste_felder()` | `_inspect, main` | 5 der Zustand 'steigt/faellt' ist entschieden NICHT gebaut ( | 1.00 |
| 271 | 6 die Zahlen kommen aus `leistenwert` und nicht aus einer zweiten Rech | `_inspect, main` | 5 der Zustand 'steigt/faellt' ist entschieden NICHT gebaut ( | 1.00 |

## 2. Die 33 offenen Pruefungen (kein Gegenstand in T08)

Diese Zeilen hat T08 nicht — weder im Wortlaut noch im Gegenstand. Sie sind der Grund, warum die
Datei bleibt.

| Zeile | Pruefname | Gegenstand |
|---|---|---|
| 64 | 1 die Datendatei liegt im Projekt | `—` |
| 65 | 1 main hat sie geladen | `daten` |
| 66 | 1 die Leiste hat elf Felder | `felder` |
| 67 | 1 Reihenfolge: Siedler, neun Rohstoffe, Punkte | `felder` |
| 72 | 1 JEDER Rohstoff des Modells steht auf der Leiste | `felder, main` |
| 75 | 1 Wolle und Leder sind dabei (Daniels Befund D3) | `felder` |
| 78 | 1 jede Quelle ist bekannt | `felder, main` |
| 81 | 1 jedes Feld traegt eine Beschriftung | `felder` |
| 83 | 1 die Hoehe ist ein Streifen, kein Bild (hoechstens 60 px) | `daten` |
| 87 | 1 Zahl-, Namen-, Warn- und Grundfarbe sind eingetragen | `daten, get` |
| 90 | 1 die Masse des Rasters stehen in der Datendatei | `daten` |
| 95 | 1 das alte Bild ist dokumentiert, aber nicht mehr die Grundlage | `daten, get` |
| 162 | 3 Holz (auf der Leiste) zeigt die Rate ohne Betrag | `text_holz` |
| 164 | 3 Wolle steht jetzt auch auf der Leiste und zeigt deshalb NUR die Rate | `text_wolle` |
| 169 | 3 Rate und Zeile lesen dieselbe Verbrauchsquelle (spieloekonomie.verbrauch_pro | `_rate_code, _zeile_code` |
| 172 | 3 keine der beiden Stellen baut eine eigene Verbrauchsformel | `_rate_code, _zeile_code` |
| 191 | 4 elf Zellen entstehen | `—` |
| 192 | 4 alle Zellen sind gleich breit (nichts gedehnt) | `—` |
| 194 | 4 die Zellen liegen in Anzeigereihenfolge von links nach rechts und ueberlappe | `—` |
| 198 | 4 jede Zelle traegt Name und Wert | `—` |
| 200 | 4 die letzte Zelle endet vor dem rechten Endstueck (kein Ueberlauf) | `—` |
| 203 | 4 die Zahl steht rechtsbuendig, der Name linksbuendig | `—` |
| 205 | 4 in einem sehr breiten Fenster waechst die Zelle nur bis zum Deckel | `_masse, _texte, main` |
| 208 | 4 in einem sehr schmalen Fenster weichen Felder, statt abgeschnitten zu werden | `_masse, main` |
| 212 | 4 ohne bekannte Fensterbreite gilt die Wuenschgroesse der Zelle | `_masse, _texte, main` |
| 263 | 6 Aufbau und Neuzeichnen benutzen dieselbe Hilfsfunktion | `quelle` |
| 266 | 6 die Leiste wird im Kopf gebaut und im Takt aktualisiert | `quelle` |
| 232 | 5 alle elf Felder haben Textkennungen | `texte` |
| 236 | 5 je Zelle vier Teile, dazu Band, Goldlinie, zwei Endstuecke und zehn Trenner | `items` |
| 245 | 5 jede Zahl auf der Leiste stimmt mit dem Spielstand ueberein | `stimmt` |
| 246 | 5 kein Bild mehr auf der Flaeche (der Streifen wird gezeichnet) | `canvas, items` |
| 251 | 5 eine Aenderung des Bestands kommt auf der Leiste an | `canvas, kennung` |
| 254 | 5 Wolle hat ein eigenes Feld auf der Flaeche | `texte` |

## 3. Empfehlung (keine Aenderung vorgenommen)

1. **Nichts uebertragen, nichts loeschen.** Daniel hat „sichten“ gesagt, nicht „zusammenlegen“.
2. **Die 33 offenen Pruefungen sind der Wert der Datei** — sie decken Gegenstaende ab, die
   T08 nicht liest (Rastermasse, Zellbreiten, Endstueck, Verbrauchsquelle, alte Bildgrundlage).
   Wer sie spaeter in T08 braucht, uebernimmt sie Namen fuer Namen mit Beleg.
3. **T08 ist der Nachfolger, nicht der Ersatz.** Bei einem spaeteren Umbau der Leiste ist die alte
   Datei die zweite Meinung — genau dafuer bleibt sie stehen.
