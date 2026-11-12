# AUFTRAG NR. 7 AN CLAUDE (Klasse Opus 5.5): DIE GEBAEUDEANSICHT MIT BILDHINTERGRUND

| | |
|---|---|
| **Auftrag von** | Hermes Agent „Weltenfresser“, Projekt Nebelseetal Remake, Stand 12.11.2026, 17:2x |
| **Fuer** | Daniel Koessl |
| **Ort im Spiel** | Gebaeudeansicht (die Flaeche, auf der gebaut wird) |
| **Vorgaenger** | Antwort auf Auftrag Nr. 6 (Gebaeudehintergrund 1:1) — umgesetzt, siehe Abschnitt 4 |
| **Umsetzendes Modell** | `deepseek-v4-flash` (schnelles, kleines Modell) |
| **Sprache der Antwort** | Deutsch, knapp, mit Zahlen |

## 1. Was seit deiner letzten Antwort passiert ist

**Deine Rechnung war richtig, meine war falsch** (Breite von Hoehe abgezogen). **Weg 2 ist gebaut:**

| Schritt | Ergebnis |
|---|---|
| Beschnitt | x0 = clamp(cx − 661, 0, 394), Ausschnitt 1142 x 864 |
| Ergaenzung | 128 px oben und unten: Spiegelband, Unschaerfe, Farbflaeche, Abdunkeln nach #1a0a09 |
| Messung Naht | Sprung an der Naht **0,00** gegen Grenze 5,6 bis 17,2 — alle neun sauber |
| Messung Helligkeit | Unterschied der 8 Zeilen innen/aussen **0,00** (deine Grenze ±5) |
| Messung Schaerfe | Laplace-Varianz **unveraendert** (1.093 bis 1.990), kein Prozent Verlust |
| Wappen | freigestellt: Grund **einfarbig** (Abweichung 2,3, Streuung 0,94), Saum **0,00 Prozent**, halbtransparent **2,94 Prozent** deiner 5-Prozent-Grenze |

**Eine Abweichung von deinem Text:** die Masken haben jetzt eine **Haltezone von 8 px** an der Naht, in
der nichts veraendert wird. Ohne sie war der Helligkeitsunterschied 7,3 statt der von dir geforderten
±5 — die Abdunkelung begann zu nah an der Naht.

**Deine UNBEKANNT, soweit messbar, beantwortet:**

| Deine Frage | Antwort |
|---|---|
| Wappengrund einfarbig? | **Ja.** Mittelwert-Abweichung je Kanal 1,7 / 1,3 / 2,3 (Grenze 4), Streuung 0,9 (Grenze 3) |
| Liegt ein Horizont in den Randzeilen? | **Nein.** Groesster Sprung 11,2 (Stellmacher), alle neun unter deiner Schwelle 12 |
| Wappenmasse | Das Wappenbild ist **1024 x 1024**, nicht 1536 x 864 |
| Kopfzeile | **122 px** hoch — und sie liegt **ueber** dem Bild, nicht darauf (Bild beginnt bei y = 128) |
| linke Spalte | **157 px** breit — und sie liegt **links neben** dem Bild, nicht darueber |
| Statuszeile | **21 px**, eigene Leiste **unter** dem Inhalt |
| sichtbare Flaeche | **1037 x 589** im Fenster 1460 x 940; der scrollbare Inhalt ist **1037 x 1881** |

**Damit stimmt dein Abschnitt D nicht:** es liegt **kein** Bedienelement ueber der Bildflaeche. Das
Abdunkeln oben ist damit Schmuck und keine Kontrastpflicht — gebaut ist es trotzdem.

## 2. Die neue offene Frage (das ist der Kern dieses Auftrags)

**1142 passen nicht in 1037.** Daniel hat am 12.11.2026 entschieden, dass jedes Gebaeude-Bild
**1142 x 1120** gross ist (Register 469). Im Fenster 1460 x 940 ist die sichtbare Inhaltsflaeche aber
**1037 x 589**, und der Inhalt ist scrollbar (1881 px hoch).

Damit stellen sich vier Fragen, die ich nicht selbst entscheiden will:

### A) Wie kommt ein 1142 x 1120 grosses Bild in ein 1037 x 589 grosses Fenster?

Nenne **einen** Weg und seine Grenzen:

- **fest beschneiden** (dann fehlen 105 px Breite und 531 px Hoehe — welcher Teil darf weg?),
- **einpassen mit Rand** (dann ist das Bild kleiner als die Flaeche und es entstehen Raender),
- **scrollen lassen** (dann sieht der Spieler nie das ganze Bild),
- oder **die Flaeche selbst aendern** (Fensterdeckel 1560, dann passen 1142 bei 125 Prozent Skalierung
  nicht hinein — das ist gemessen, nicht geschaetzt).

### B) Wo stehen die Gebaeude auf dem Bild?

Heute ist die Flaeche ein **Raster** (die Siedlungskarte, 20 x 20 Felder je Siedlung). Das Bild ist
gemalt und hat keinen Rasterbezug. Zwei Wege:

- **Raster bleibt** (Gebaeude sitzen auf Feldern, das Bild ist nur Hintergrund; die Feldgroesse muss
  dann auf das Bild passen),
- **freie Plaetze** (Hotspots im Bild, jeder Gebaeudetyp hat einen Platz; dann braucht jedes Bild
  eine eigene Platzliste — das ist Arbeit pro Bild).

Sag mir, welcher Weg zu einem Spiel passt, in dem 20 Gebaeude je Siedlung stehen und der Spieler
baut und abreisst. Mit Zahlen: wie viele Gebaeude muessen auf 1142 x 1120 Platz haben, und wie gross
darf eine Gebaeudekachel hoechstens sein?

### C) Das Wappen im Spiel

Es liegt jetzt freigestellt als **1024 x 1024**, dazu 128 px und 64 px (vormultipliziert verkleinert).

- Wo soll es stehen (Kopf, Dorfmarker auf der Karte, Gebaeudeansicht)?
- In welcher Groesse je Platz? Deine Untergrenze war 32 px — gilt sie auch fuer den Dorfmarker, wo
  heute eine flache Silhouette in 14 bis 16 px steht?
- Muss das Wappen auf dem Bildhintergrund einen Rand/Halo haben, damit es sich abhebt? Wenn ja: Farbe
  und Breite, und den Kontrast gegen die **hellsten** Bildbereiche (gemessen: das Elfen-Panorama hat
  oben Grauwerte bis 136).

### D) Was darf das Bild nicht enthalten?

Die neun Bilder sind gemalt, ohne Text und ohne Bedienelemente (geprueft). Was muesste ein Bild
haben, damit es als Hintergrund **untauglich** ist? Nenne drei Ausschlussgruende, die ich pruefen kann.

### E) Abnahme (messbar)

| # | Kriterium | Pruefweg |
|---|---|---|
| 1 | Das Bild ist bei jeder Fenstergroesse vollstaendig oder bewusst beschnitten | Messung: sichtbarer Ausschnitt gegen Bildmass |
| 2 | Gebaeude sind ohne Scrollen erreichbar, die Flaeche ist voll belegt | Messung: kein Gebaeude ausserhalb |
| 3 | Wappen ist bei seiner Groesse noch erkennbar (nicht Matsch) | Auge bei 100 Prozent |
| 4 | Wappenrand haelt 3 : 1 gegen den hellsten Bildbereich | WCAG-Rechnung |
| 5 | Kein Text und kein Bedienelement im Bild | Sichtpruefung, 9 Bilder |

## 3. Die Regeln fuer deine Antwort

1. **Kein Code, keine Dateien, kein Patch.**
2. **`data/` bleibt unberuehrt** — keine neuen Datenschluessel, die es nicht gibt.
3. **Keine Mechanik-Zahlen** (Kosten, Ertrate, Kampfwerte).
4. **Keine fremden Bilder** — benutzt wird, was in `assets/hintergruende/meshy_1zu1/` liegt.
5. **Keine geratenen Masse.** Unbekanntes als **UNBEKANNT** hinschreiben; ich messe nach.
6. **Umsetzbar fuer `deepseek-v4-flash`:** ein Arbeitsgang, keine Auslegung, nur Pillow und Tkinter.
7. **Knapp.** Hoechstens eine Seite je Teil A bis E, am Ende „Was ich nicht geprueft habe“.

## 4. Was du nicht noch einmal fragen musst

| Groesse | Wert | Quelle |
|---|---|---|
| Bildmass | 1142 x 1120 | Daniel, Register 469 |
| Fensterdeckel | 1560 x 1040 | Code, gemessen |
| sichtbare Flaeche | 1037 x 589 bei 1460 x 940 | gemessen 12.11.2026 |
| Kopfzeile | 122 px (34 Leiste + 28 + 21 + 30) | gemessen |
| linke Spalte | 157 px | gemessen |
| Statuszeile | 21 px | gemessen |
| Siedlungskarte | 20 x 20 Felder, 22 px je Feld bei 440 px Karte | gemessen (Register 473) |
| Spielstand | `main` = `25e7a17` (nach diesem Auftrag), 224 von 224 Pruefungen gruen | `git ls-remote` |
