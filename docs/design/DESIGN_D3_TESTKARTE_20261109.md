# D-3: Testkarte 20 x 20 mit gemalten Kacheln - Beleg

**Stand:** 09.11.2026, 02:20. **Gegenstand:** `src/weltkarte_malerei.py` (neu),
`tools/testkarte_fenster.py` (neu), `tests/test_weltkarte_malerei.py` (neu, 67 Pruefungen).
**Kein Spielcode geaendert:** `_render_portal` zeichnet weiter flache Gelaendefarben - der Einbau
ist D-4 und folgt erst nach Daniels Urteil.

## 1. Was D-3 verlangt hat

Aus `docs/design/DESIGN_ARBEITSWEISE.md`: eine Testkarte 20 x 20 mit den sieben Gelaendearten und
Tannen, **gemalt**, mit **Belastungstest im Fenster**. Daniel hat am 09.11.2026, 02:03 entschieden:
flaches Raster mit gemalten Kacheln (Register 328); isometrisch nur, wenn der Stil flach nicht
traegt.

## 2. Zwei Anlaeufe, der erste verworfen (gemessen, nicht geschaetzt)

**Anlauf 1 - Kachel fuer Kachel.** 400 Kacheln einzeln gemalt, zusammengesetzt, die Grenzen
weichgezeichnet. Ergebnis bei 48 px: ein Fliesenmuster mit harten 90-Grad-Kanten; das
Weichzeichnen der Kachelraender legte ein Waffelmuster ueber die ganze Karte. **Verworfen.**

**Anlauf 2 - die Karte als EIN Bild** (so steht es jetzt im Modul):

1. **Farbfeld:** die 20 x 20-Gelaendematrix als 20 x 20 Pixel, bikubisch auf Kartengroesse
   hochgerechnet, danach Kontrast und Farbe leicht angehoben (sonst verwaschen sieben Toene zu
   einem Brei).
2. **Motive je Feld:** zwei bis drei Tannen, ein bis zwei Gipfel, Duenen, Wellen, Schilf - je Feld
   mit eigener Saat aus seiner Lage. Damit gibt es keine Wiederholung mehr, und die Feldmitte
   traegt weiter das Feld, das der Klick trifft.
3. **Ein Licht und ein Korn** ueber der ganzen Karte (warm oben links, Schatten unten rechts).

Der erste Anlauf hatte eine Stilprobe-A-Lesung, die sich als falsch erwies: das Paket beschreibt
"runde Laubbaeume", D-3 verlangt aber ausdruecklich **Tannen** - die Stilprobe B ist die
Tannen-Vorlage. Gebaut sind Tannen.

## 3. Belastungstest im Fenster (gemessen)

`tools/testkarte_fenster.py` oeffnet ein echtes Tk-Fenster mit der gemalten Karte (Weltkarte d01,
alle sieben Arten: berg 48, grasland 80, huegel 52, nebelsee 28, steppe 80, sumpf 40, wald 72) und
zeichnet sie fuenfmal:

| Groesse | kalt (malen) | warm (Zwischenspeicher) | Tk-Grafik bauen + setzen | fuenf Zeichnungen min/mittel/max |
|---|---|---|---|---|
| 20 px je Feld (Portal heute) | 0,462 s | 0,00013 s | - | - |
| 48 px je Feld (Testkarte) | 0,742 s | 0,00014 s | 0,235 s (erste) | 0,032 / 0,089 / 0,235 s |

**Lesart:** malen kostet einmalig unter einer Sekunde, danach ist die Karte EIN Objekt im
Zwischenspeicher; das Setzen dauert danach rund 30 ms. Die heutige Anzeige zeichnet 400 Rechtecke
und 42 Rasterlinien je Ansicht - die gemalte Karte waere EIN `create_image`, also weniger Objekte
im Canvas als heute.

## 4. Was die Pruefdatei zusichert (67 Pruefungen, 0 Fehler, 1 Befund)

- **Eine Quelle je Wert:** die Hex-Farben der sieben Arten stehen NICHT im Quelltext; das Modul
  liest `gelaende.farbe()` (also `data/gelaende.json`). Hell- und Dunkeltoene werden gerechnet.
- **Gemalt, nicht gefuellt:** jede Kachel hat ueber 600 Farben, ihr Mittelton liegt trotzdem an der
  Gelaendefarbe (Abweichung 4 bis 22 von 255).
- **Der Wald traegt Tannen:** 1.361 dunkle Nadelgruen-Pixel gegen 112 im Grasland.
- **Ohne Pillow wird nicht gemalt:** `MalereiFehler` mit Grund, kein Ersatzbild; kein PIL- und kein
  tkinter-Import im Modulkopf.
- **Zwischenspeicher und Determinismus:** zweiter Abruf liefert dasselbe Objekt, gleiche Eingabe
  ergibt pixelgleiches Bild, drei Varianten sind wirklich verschieden.
- **Die ganze Karte** hat die Masse Spalten x Kante mal Zeilen x Kante, unbekannte Gelaendearten
  werden abgelehnt statt still uebergangen.

## 5. Was NICHT gebaut ist (bewusst)

- **Kein Einbau ins Spiel.** Solange Daniel den Stil nicht freigegeben hat, bleibt `_render_portal`
  unveraendert. Der Einbau (EIN Bild statt 400 Rechtecke, Klick ueber die Feldkoordinaten) ist ein
  eigener Schnitt nach D-4.
- **Keine Burgen, Drachen, Maersche auf der gemalten Karte** - die liegen ueber dem Bild und
  brauchen den Einbau (D-4 bis D-6).
- **Kein Zoom.** Die Kante ist ein Parameter; die Portalansicht ist heute auf 20 px festgelegt.

## 6. Offene Fragen an Daniel (werden gesammelt, nicht einzeln gestellt)

1. **Stil:** traegt die flache gemalte Karte (Bilder im Archiv), oder soll der isometrische Umbau
   (Stilprobe A, Register 328 zurueckgestellt) kommen?
2. **Kante:** reichen 20 px je Feld fuer die gemalten Motive, oder soll die Portalkarte groesser
   werden (32 oder 48 px, dann mit Rollbalken)?
3. **Tannen oder Laubbaeume:** D-3 nennt Tannen, das Paket beschreibt runde Laubbaeume. Beides ist
   jetzt moeglich - was soll der Wald tragen?

## 7. Belege

- `archiv/design/20261109_d3_testkarte/testkarte_d01_48px.png` (960 x 960)
- `archiv/design/20261109_d3_testkarte/testkarte_d01_20px_portal.png` (400 x 400, echte Portalmasse)
- `archiv/design/20261109_d3_testkarte/kacheln_sieben_arten_256px.png` (sieben Einzelkacheln)
- `SHA256SUMS.txt` im selben Ordner
- Messwerte: `docs/audits/messwerte/test_weltkarte_malerei_20261109_0223.json`
