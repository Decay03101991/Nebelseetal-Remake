# AUFTRAG NR. 9 AN CLAUDE (Klasse Opus 5.5): DIE LINKE SPALTE BEI JEDER FENSTERGROESSE

| | |
|---|---|
| **Auftrag von** | Hermes Agent „Weltenfresser“, Projekt Nebelseetal Remake, Stand 12.11.2026, 19:4x |
| **Fuer** | Daniel Koessl |
| **Vorgaenger** | Antwort auf Auftrag Nr. 8 (Panorama hinter einer 10 x 10-Karte) — drei Entscheidungen gefallen, Umbau beginnt |
| **Umsetzendes Modell** | `deepseek-v4-flash` (schnelles, kleines Modell) |
| **Sprache der Antwort** | Deutsch, knapp, mit Zahlen |

## 0. Was seit deiner letzten Antwort festgelegt und gemessen ist

Daniel hat am 12.11.2026 entschieden (Register 507):

| # | Entscheidung |
|---|---|
| F-46 | **Feldgroesse 57 px** (`zelle = min(64, (H − 18) // 10)`), Karte **588 x 588**, alle 100 Felder ohne Rollen sichtbar. Preis bewusst angenommen: das historische Kartenbild wird einmal von 640 auf **570 px** verkleinert |
| F-47 | **Karte rechts, Spalte links** — Spalte x 0..433, 16 px Abstand, Karte x 449..1037; kein Panorama-Schalter |
| F-48 | **Schleier 80 Prozent `#1a0a09`** hinter jedem Textblock, zwischen den Bloecken bleibt das Bild sichtbar |

**Beim Vorbereiten gemessen** (echtes Fenster, 12.11.2026):

| Block | Wunschmass | bekommt heute | Anmerkung |
|---|---|---|---|
| Karte | 658 x 658 | 658 x 658 | 10 x 10 Felder zu 64 px + 18 px Leiste |
| Bauauswahl (Info) | **300 x 218** | 300 x 658 | passt in eine Spalte von 433 |
| Dorfübersicht | **442 x 240** | **35 x 658** | ihre Tabelle will allein **428 x 80** — sie ist heute praktisch unsichtbar |
| Zusaetze (Hinweis, Reichsvergleich, Vorteil) | 152 x ~130 | volle Breite | kommen ans Ende der Spalte |

**Damit steht fest: 588 (Karte) + 16 (Abstand) + 442 (Dorfübersicht) = 1046 > 1037.** Die Spalte ist
9 px zu schmal fuer die Dorfübersicht in ihrer heutigen Form.

**Ein zweiter Punkt ist wichtiger und bisher nirgends benannt:** die Fenstergroesse wird aus dem
Bildschirm gerechnet, und das Fenster hat **keine Mindestgroesse**:

```
_breit = max(1024, min(1560, Bildschirmbreite - 90))
_hoch  = max(720,  min(940,  Bildschirmhoehe - 120))
```

Gemessen sind die Abzuege vom Fenster zur sichtbaren Inhaltsflaeche **409 px Breite** (157 Menuespalte
links + 223 rechts + Rahmen) und **155 px Hoehe** (122 Kopf + 21 Statuszeile + Rahmen). Daraus:

| Bildschirm | Fenster | sichtbare Flaeche | Feldgroesse (H − 18) // 10 | Karte |
|---|---|---|---|---|
| 1920 x 1080 | 1560 x 940 (gedeckelt) | **1151 x 785** | 76 -> gedeckelt **64** | 658 |
| 1536 x 864 (dieser Rechner) | **1446 x 744** | **1037 x 589** | **57** | 588 |
| 1366 x 768 | 1276 x 720 | **867 x 565** | **54** | 558 |
| 1024 x 720 (Rueckfall) | 1024 x 720 | **615 x 565** | **54** | 558 |

## 1. Die Frage (Kern dieses Auftrags)

**Wie sieht die Siedlungsansicht aus, wenn die sichtbare Flaeche von 1151 x 785 bis 615 x 565
schwankt — und was passiert, wenn der Spieler das Fenster kleiner zieht als das?**

Teil A bis E, bitte mit Zahlen, die aus den vier Zeilen oben folgen.

### A) Die Dorfübersicht in 433 px (und in 615 - 16 - Karte bei 867 px Breite)

Sie will heute 442 px, ihre Tabelle allein 428 px. Nenne **einen** Weg und seine Grenzen:

- **Umbruch:** die Tabelle bricht auf zwei Zeilen (dann wie hoch?), Spaltenzahl je Zeile?
- **Kuerzen:** weniger Spalten (welche fallen zuerst, in welcher Reihenfolge?)
- **Zweite Zeile im Layout:** Dorfübersicht unter die Bauauswahl statt daneben (sie steht in der
  Spalte ohnehin schon untereinander — dann ist die Frage, wie breit ihre Tabelle sein darf)

Bei 867 px Breite hat die Spalte **nur 293 px** (867 − 16 − 558). Was bleibt da von der Übersicht?

### B) Die Spalte rollt — aber wie, wenn sie schmaler wird?

Gemessener Inhalt der Spalte bei 433 px: Titel/Name 38, Ortsbestand 57, Bauauswahl 218,
Dorfübersicht 240, Legende mit Erklaerung 42, Zusaetze 57 = **652 px**. Sichtbar sind je nach
Bildschirm 785 / 589 / 565 / 565 px.

- **Wann rollt sie** (bei welcher Hoehe zuerst)?
- **Wo sitzt der Rollbalken** — rechts an der Spalte (dann 16 px weniger Breite) oder aussen?
- **Bleibt die Legende unten kleben** oder rollt sie mit?

### C) Das Panorama, wenn die Flaeche schrumpft

Der Ausschnitt ist `(52, (1120 − H) // 2)`. Bei H = 565 ist das oben **277**, bei H = 785 oben **167**.

- **Bei H > 1120** (kommt erst bei Fenstern ueber 1275 px Hoehe vor, also praktisch nie): Bild mittig,
  Rest `#17212B` — bleibt so, oder?
- **Bei sehr kleinem H** (Fenster auf 400 px Hoehe gezogen): H = 245, Ausschnitt oben 437, Karte
  `(245 − 18) // 10 = 22` px je Feld, also 220 x 220. **Ist das noch spielbar** oder braucht es eine
  Mindestgroesse fuer das Fenster (welche, mit welcher Begruendung)?

### D) Welche Bloecke bekommen einen Schleier?

Bei 80 Prozent Deckung und 8 px Innenabstand. Bitte als **Liste** (Block -> ja/nein):

1. Titel und Name in einer Zeile
2. Ortsbestand (eigener Kasten `#1B2A2F` mit Rahmen `#7FD1FF`)
3. Bauauswahl
4. Dorfübersicht
5. Legendenzeile (die 14 Farbfelder mit Namen)
6. Erklaerzeile (»Sumpf ist nicht bebaubar …«)
7. Zusaetze: Hinweis, Reichsvergleich, Vorteil
8. die 18 px breite Koordinatenleiste der Karte

**Wichtig:** der Ortsbestand hat schon eine **eigene** Hintergrundfarbe (`#1B2A2F`) und einen Rahmen.
Bekommt er zusaetzlich einen Schleier, oder reicht seine eigene Flaeche? Wenn er einen bekommt:
welche Kontraste ergeben sich fuer `#7FD1FF` und `#F3F4F6` auf `0,8 × #1a0a09 + 0,2 × Bild` im
schlimmsten Fall (reines Weiss darunter)?

### E) Abnahme (messbar)

| # | Kriterium | Pruefweg |
|---|---|---|
| 1 | Bei jeder der vier Flaechen ist die Karte ganz sichtbar und keine Spalte schneidet Text ab | Messung: Kartenkante, Blockbreiten |
| 2 | Die Dorfübersicht zeigt bei 433 px **alle** ihre Pflichtangaben (welche sind Pflicht?) | Messung + Auge |
| 3 | Kein Text ohne Schleierfeld, jedes Schleierfeld haelt 4,5 : 1 fuer Text und 3 : 1 fuer Rahmen | Rechnung je Blockfarbe |
| 4 | Bei H = 565 und H = 785 ist der Bildausschnitt `(52, (1120 − H) // 2)` und nichts skaliert | Messung |
| 5 | Unterhalb der Mindestgroesse (deine Zahl aus C) verweigert das Fenster das Schrumpfen | Messung `winfo_width/height` |

## 2. Regeln fuer deine Antwort

1. **Kein Code, keine Dateien, kein Patch.**
2. **`data/` bleibt unberuehrt.**
3. **Keine Mechanik-Zahlen** (Kosten, Ertraege, Kampfwerte).
4. **Keine fremden Bilder.**
5. **Keine geratenen Masse.** Unbekanntes als **UNBEKANNT** hinschreiben; ich messe nach.
6. **Umsetzbar fuer `deepseek-v4-flash`:** ein Arbeitsgang, nur Pillow und Tkinter.
7. **Knapp.** Hoechstens eine Seite je Teil A bis E, am Ende „Was ich nicht geprueft habe".

## 3. Was du nicht noch einmal fragen musst

| Groesse | Wert | Quelle |
|---|---|---|
| Bildmass | 1142 x 1120, JPEG q92 | `assets/hintergruende/meshy_1zu1/` |
| Anzeigeregel | mittiger 1:1-Ausschnitt, nie skalieren | Daniel, Register 502 (F-45) |
| Feldgroesse | `min(64, (H − 18) // 10)`, Daniel: 57 px | Register 507 (F-46) |
| Anordnung | Karte rechts, Spalte links, 16 px Abstand | Register 507 (F-47) |
| Schleier | 80 Prozent `#1a0a09`, 8 px Innenabstand | Register 507 (F-48) |
| Siedlungskarte | 10 x 10 Felder, immer (`originalkarten.py` prueft das Raster) | Code |
| Kartengrund | **EIN** historisches Bitmap 640 x 640, bei 57 px einmal auf 570 verkleinert | gemessen |
| Abzug Fenster -> Flaeche | 409 px Breite, 155 px Hoehe | gemessen |
| Bauauswahl / Dorfübersicht | 300 x 218 / 442 x 240 (Wunschmasse) | gemessen 12.11.2026 |
| Spalteninhalt gesamt | 652 px | gerechnet aus den Wunschmassen |
| Spielstand | `main` = `bdda6f8`, Wache 35/0/0 gruen | `git ls-remote` |
