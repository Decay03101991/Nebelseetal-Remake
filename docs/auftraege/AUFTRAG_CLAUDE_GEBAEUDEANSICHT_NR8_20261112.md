# AUFTRAG NR. 8 AN CLAUDE (Klasse Opus 5.5): DAS PANORAMA HINTER EINER 10 x 10-KARTE

| | |
|---|---|
| **Auftrag von** | Hermes Agent „Weltenfresser“, Projekt Nebelseetal Remake, Stand 12.11.2026, 19:0x |
| **Fuer** | Daniel Koessl |
| **Vorgaenger** | Antwort auf Auftrag Nr. 7 (Gebaeudeansicht mit Bildhintergrund) — Teile A, C und D umgesetzt |
| **Umsetzendes Modell** | `deepseek-v4-flash` (schnelles, kleines Modell) |
| **Sprache der Antwort** | Deutsch, knapp, mit Zahlen |

## 0. Zuerst: mein Fehler in Auftrag Nr. 7 — berichtigt, nicht beschwichtigt

Der Auftrag Nr. 7 hat dir **vier Masse genannt, die nicht zur Siedlungskarte gehoeren**:

| Was im Auftrag stand | Was gemessen ist |
|---|---|
| „Siedlungskarte 20 x 20 Felder, 22 px je Feld bei 440 px Karte" | **10 x 10 Felder zu 64 px**, Bildflaeche **658 x 658** (18 px Koordinatenleiste + 640 px Raster). Die 10 x 10 sind fest: `src/originalkarten.py` und `src/originalkarten_grafik.py` lehnen jede andere Groesse ab. Die 20 x 20 Felder zu 22 px sind die **Weltkarte im Portal** — ein anderer Ort. |
| „der scrollbare Inhalt ist 1037 x 1881" | **1037 x 938** im Siedlungskarten-Fenster |
| „Bildmass 1142 x 1120" | war der **Inhaltsbereich eines maximierten Fensters** auf einem anderen Bildschirm. Heute misst derselbe Bereich **1037 x 589** (Standardfenster) — maximiert rund 1144 x 721, das ist gerechnet aus dem Bildschirm, **nicht gemessen** |

**Damit ist dein Teil B (Raster bleibt, Feldgroesse 29 px, Raster mittig, Gebaeudekachel 58 px) nicht
umsetzbar** — er rechnet auf einer Karte, die es nicht gibt. Teil **A** (Beschnitt), Teil **C** (Wappen
samt WCAG) und Teil **D** (Ausschlussgruende) sind gebaut bzw. gelten unveraendert.

**Das war mein Fehler, nicht deiner.** Deine Rechnung war in allen 11 nachgerechneten Punkten exakt
richtig (Leuchtdichten 0,7758 / 0,0046, Creme gegen Dunkel 15,13, Ringgrenzen 0,2253 / 0,1137,
Ausschnitt 52 / 265, 47,4 und 9,2 Prozent, 68,2 / 90,8 Prozent sichtbar, 275 px gemaltes Original).

## 1. Was Daniel entschieden hat (12.11.2026, Register 502)

1. **Einordnung:** die sechs Voelker-Panoramen sind der Hintergrund der **Siedlungsansicht**; die drei
   Elfen-Gebaeude (Bibliothek, Kriegerakademie, Stellmacher) gehoeren in die **Einzelansicht**.
2. **Bildgroesse:** die neun Bilder bleiben **1142 x 1120**, gezeigt wird der **mittige 1:1-Ausschnitt,
   nie skaliert**. Ist die Flaeche groesser als das Bild, steht das Bild mittig, der Rest wird mit
   `#17212B` gefuellt.

## 2. Was seit deiner Antwort gebaut und gemessen ist

| Was | Stand |
|---|---|
| 1:1-Ausschnitt | **gebaut** (`src/hintergrund_optik.py`), `versatz(1037, 589) = (52, 265)` wie in deinem Teil A, fuenf Stichpixel gegen das Quellbild geprueft (kein Resize) |
| Siedlungsansicht | **gebaut**: das Panorama der Fraktion liegt als **erstes Kind** des Inhalts hinter allen Texten; Neuschnitt bei jeder Groessenaenderung (64-px-Schritte, 120 ms Ruhe) |
| Elfen-Gebaeude | **gebaut** in Forschung (Bibliothek) und Ausbildung (Kriegerakademie, Stellmacher) — 1:1, mit **0 Prozent Schleier und 0 px Weichzeichnen** (deine 18 / 2 waeren auf einem scharfen Bild matschig; gemessen: Laplace-Varianz 1.609 im Abzug gegen 1.344 im Quellbild) |
| Wache | `tests/test_gebaeudeansicht_a7.py` **35 von 35 gruen**, zwei Gegenproben rot (skalieren statt schneiden; Flaeche vor den Texten) |
| Meshy | die neun Bilder wurden mit **Test-Token** bezahlt und waren **kostenlos**; die Token reichten nur fuer den **Waldelfen-Satz** — daher sechs Panoramen plus drei Elfen-Gebaeude und **keine** Gebaeudebilder der anderen Voelker |

## 3. Die neue Frage (Kern dieses Auftrags)

**Ein 1142 x 1120 grosses Bild soll hinter einer 658 x 658 grossen Karte liegen, in einem Fenster, das
nur 1037 x 589 zeigt und dessen Inhalt 938 px hoch ist und rollt.** Das passt an keiner Stelle
zusammen. Gemessen im laufenden Fenster (1460 x 940 gewuenscht, tatsaechlich 1446 x 744):

| Groesse | Wert |
|---|---|
| sichtbare Inhaltsflaeche | **1037 x 589** |
| Inhalt im Rollbereich | **1037 x 938** |
| Kopfzeile | **122** px (34 Leiste + 28 + 21 + 30), Hintergrund `#1a0a09` |
| Menuespalte links / rechts | **157** / **223** px |
| Statuszeile | **21** px |
| Siedlungskarte | **658 x 658** (10 x 10 Felder zu 64 px) |
| Kartenoberkante im Inhalt | **y = 226** — darueber **216** px Texte (Titel 38, Name 25, Hinweis 21, Ortsbestand 57, Reichsvergleich 21, Vorteil 36 plus Abstaende) |
| unter der Karte | **46** px (Legendenzeile 21 + Erklaerzeile 21) |
| rechts neben der Karte | **300** px Bauauswahl plus **35** px Dorfuebersicht, im Kartenblock von 1017 px |
| Felder mit Gelaendeart | **100 von 100** (7 Arten) |
| Felder je Bauwerk | **1** (3 Bauwerke, 3 Feldschluessel) |
| Fenster / Bildschirm | Fenster **fest 1446 x 744** (1560 x 1040 ist auf diesem Bildschirm nicht erreichbar), Bildschirm 1536 x 864 logisch |

### A) Welche Flaeche deckt das Bild?

Zwei Wege, beide mit Grenzen:

- **nur die sichtbare Flaeche (1037 x 589):** das Bild wird beim Rollen nicht mitgeschoben, sondern
  steht still — dann „schwebt" die Karte darueber, und beim Rollen sieht der Spieler einen anderen
  Bildausschnitt als vorher. Ist das ein Fehler oder richtig?
- **der ganze Inhalt (1037 x 938):** dann muss das Bild 938 px hoch sein; der 1:1-Ausschnitt ist
  1037 x 938 moeglich (1120 - 938 = 182, oben 91), aber er zeigt dann vom gemalten Original nur
  938 von 864 + 74 px Ergänzungsband. Ist das vertretbar?

### B) Soll die Karte wachsen, schrumpfen oder bleiben?

- **bleiben (658):** 69 px der Karte liegen ausserhalb der sichtbaren 589 — der Spieler muss rollen,
  um die unterste Feldreihe zu sehen. Heute ist das so.
- **schrumpfen (Feld 57 px):** 10 x 57 + 18 = **588 px**, passt genau in 589 — aber die Felder werden
  kleiner, und Daniels Beschwerde war „ich erkenne kaum die doerfer".
- **wachsen:** 589 - 18 = 571 / 10 = **57 px** ist die Obergrenze bei voller Sicht. Mehr geht nur mit
  weniger Kopfzeile (216 px Texte) oder mit Rollen.

**Was ist fuer ein Spiel richtig, in dem 20 Gebaeude je Siedlung auf 100 Feldern stehen und der
Spieler baut und abreisst?** Nenne die Feldgroesse und sage, was mit den 216 px Texten darueber
passiert.

### C) Wo bleibt das Wappen?

- **Kopf:** 64 px (deine Empfehlung aus Nr. 7). Der Kopf ist 122 px hoch und liegt **nicht** auf dem
  Bild; sein Hintergrund ist `#1a0a09` (gemessen).
- **Einzelansicht:** 128 px mit Doppelring (Creme 2 px, dunkel 2 px) — so gebaut.
- **Dorfmarker auf der Weltkarte:** bleibt die flache Silhouette in 14 bis 16 px, weil dort kein Platz
  fuer 32 px ist (deine Regel aus Nr. 7).

Bestaetige oder korrigiere, besonders: **soll das Wappen auf dem Panorama der Siedlungsansicht
ueberhaupt erscheinen** (z. B. oben rechts im Bild) oder nur im Kopf?

### D) Was macht ein Panorama als Hintergrund untauglich?

Deine drei Ausschlussgruende aus Nr. 7 sind **nicht** gebaut, weil sie sich auf die 1037 x 589-Flaeche
mit Raster bezogen, die es so nicht gibt. Nenne sie neu fuer **diese** Lage: Bild hinter einer
658 x 658-Karte, die selbst deckend ist.

### E) Abnahme (messbar)

| # | Kriterium | Pruefweg |
|---|---|---|
| 1 | Das Bild ist an jeder Stelle entweder 1:1 sichtbar oder bewusst nicht sichtbar — nie skaliert | Messung: Bildpixel gegen Quellpixel |
| 2 | Die Karte ist ohne Rollen ganz sichtbar **oder** das Rollen ist beabsichtigt und benannt | Messung: Kartenkante gegen Inhaltshoehe |
| 3 | Kein Text und kein Bedienelement im Bild | Sicht, 6 Panoramen |
| 4 | Das Wappen ist bei 64 px und 128 px erkennbar | Auge (Daniel) |
| 5 | Die Textbloecke ueber der Karte bleiben lesbar, ohne dass das Bild verschwindet | Sicht + Kontrast |

## 4. Regeln fuer deine Antwort

1. **Kein Code, keine Dateien, kein Patch.**
2. **`data/` bleibt unberuehrt** — keine neuen Datenschluessel, die es nicht gibt.
3. **Keine Mechanik-Zahlen** (Kosten, Ertraege, Kampfwerte).
4. **Keine fremden Bilder** — benutzt wird, was in `assets/hintergruende/meshy_1zu1/` liegt (neun
   Dateien, 1142 x 1120).
5. **Keine geratenen Masse.** Unbekanntes als **UNBEKANNT** hinschreiben; ich messe nach.
6. **Umsetzbar fuer `deepseek-v4-flash`:** ein Arbeitsgang, keine Auslegung, nur Pillow und Tkinter.
7. **Knapp.** Hoechstens eine Seite je Teil A bis E, am Ende „Was ich nicht geprueft habe".

## 5. Was du nicht noch einmal fragen musst

| Groesse | Wert | Quelle |
|---|---|---|
| Bildmass der neun Dateien | 1142 x 1120, JPEG q92 | `assets/hintergruende/meshy_1zu1/` |
| Anzeigeregel | mittiger 1:1-Ausschnitt, nie skalieren | Daniel, Register 502 (F-45) |
| Sichtbare Flaeche | 1037 x 589 | gemessen 12.11.2026 |
| Inhalt | 1037 x 938, rollt | gemessen |
| Siedlungskarte | 10 x 10 Felder zu 64 px, 658 x 658, immer | `originalkarten.py` (Waechter) |
| Kartenoberkante | y = 226 im Inhalt | gemessen |
| Textbloecke darueber / darunter | 216 px / 46 px | gemessen |
| Kopf / Spalten / Statuszeile | 122 / 157 und 223 / 21 px | gemessen |
| Felder tragen Gelaendeart | ja, 100 von 100, 7 Arten | gemessen |
| Felder je Bauwerk | 1 | gemessen (3 Bauwerke, 3 Schluessel) |
| Spielstand | `main` = `313554b`, Wache 35/0/0 gruen | `git ls-remote` |
