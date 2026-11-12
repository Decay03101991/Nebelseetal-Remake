# PRUEFUNG: Claudes Antwort auf Auftrag Nr. 7 (Gebaeudeansicht mit Bildhintergrund)

Stand 12.11.2026, 18:0x. Antwort abgelegt unter
`docs/eingaenge/CLAUDE_20261112_GEBAEUDEANSICHT/CLAUDE_ANTWORT_AUFTRAG7_GEBAEUDEANSICHT.md`
(10.713 Byte, 157 Zeilen, SHA256 `38502893887567ef04449867f13ecf844db2ff4598d16a149ec49f93b526f478`,
hashgleich mit der Desktop-Fassung, die nach dem Pruefen geraeumt wurde).

## 1. Was nachgerechnet ist - und stimmt

Alle Zahlen der Antwort wurden nachgerechnet, nicht geglaubt.

| Behauptung | Nachgerechnet | Urteil |
|---|---|---|
| Leuchtdichte Creme `#F2E3BF` = 0,7758 | **0,7758** | richtig |
| Leuchtdichte Dunkel `#1a0a09` = 0,0046 | **0,0046** | richtig |
| Creme gegen Dunkel = 15,13 | **15,13** | richtig |
| Creme haelt 3:1 bis L_unter 0,2253 | **0,2253** | richtig |
| Dunkel haelt 3:1 ab L_unter 0,1137 | **0,1137** | richtig |
| Grau 136: dunkler Ring 5,43, Creme-Ring 2,79 | **5,43 / 2,79** | richtig |
| Ausschnitt bei 1037 x 589: links 52, oben 265 | **52 / 265** | richtig |
| Ausschnitt bei W = 691: links 225 | **225** | richtig |
| fehlt 531 px Hoehe = 47 Prozent, 105 px Breite = 9 Prozent | **47,4 / 9,2** | richtig |
| sichtbar vom gemalten Original: 68 Prozent Zeilen, 91 Prozent Spalten | **68,2 / 90,8** | richtig |
| gemaltes Original fehlt 275 px (531 - 256) | **275** | richtig |

**Ergebnis: keine Abweichung.** Das ist die zweite Antwort hintereinander, in der seine Rechnung
vollstaendig stimmt.

## 2. Was im Fenster gemessen ist (neues Werkzeug `tools/messe_gebaeudeansicht.py`)

Gemessen im laufenden Fenster, Siedlungskarte geoeffnet, 12.11.2026.

| Groesse | Gemessen |
|---|---|
| sichtbare Inhaltsflaeche | **1037 x 589 px** |
| Hoehe des Inhalts im Rollbereich | **938 px** (nicht 1881) |
| Kopfzeile | 122 px (34 Leiste + 28 + 21 + 30), Hintergrund `#1a0a09` |
| Menuespalte links | 157 px |
| Statuszeile | 21 px, `#1a0a09` |
| Siedlungskarte | **658 x 658 px** = 18 px Koordinatenleiste + **10 x 10 Felder zu 64 px** |
| Kartenoberkante im Inhalt | **y = 226 px** |
| unter der Karte | **46 px**: Legendenzeile 21 px + Erklaerzeile 21 px |
| ueber der Karte | **216 px**: Titel, Name, Hinweis, Ortsbestand, Reichsvergleich, Vorteil |
| Felder mit Gelaendeart | **100 von 100** (7 Arten: Berg, Grasland, Huegel, Nebelsee, Steppe, Sumpf, Wald) |
| Felder je Bauwerk | **1** (3 Bauwerke, 3 Feldschluessel im Spielstand) |
| Bildschirm (Tk, logisch) | **1536 x 864 px** |
| Fenster | fest **1446 x 744**; Wunschgroessen 1460x940, 1560x1040 und 1000x940 ergaben dasselbe Fenster |

## 3. Mein Fehler im Auftrag - offen

Der Auftrag Nr. 7 nennt vier Masse, die **nicht** zur Siedlungskarte gehoeren:

| Im Auftrag | Wahrheit |
|---|---|
| "Siedlungskarte 20 x 20 Felder, 22 px je Feld bei 440 px Karte" | Die Siedlungskarte hat **10 x 10 Felder zu 64 px** (658 x 658). Die 20 x 20 Felder zu 22 px sind die **Weltkarte im Portal**, nicht die Bauflaeche. |
| "sichtbare Flaeche 1037 x 589" | richtig - aber das ist der **Inhaltsbereich**, nicht die Karte |
| "der scrollbare Inhalt ist 1037 x 1881" | **938 px** im gemessenen Fenster |
| "Bildmass 1142 x 1120" (= Register 469) | 1142 x 1120 war der **Inhaltsbereich eines maximierten Fensters** auf einem anderen Bildschirm (Register 468/469). Heute misst derselbe Bereich **1037 x 589** im Standardfenster und rund 1144 x 721 maximiert (Bildschirm 1536 x 864 logisch). |

**Folge fuer die Antwort:** Teil **A** (Beschnitt-Formel), Teil **C** (Wappen samt WCAG) und Teil **D**
(Ausschlussgruende) haengen an der sichtbaren Flaeche und gelten unveraendert. Teil **B** (Raster
bleibt, Feldgroesse 29 px, Gebaeudekachel 58 px, Raster mittig) ruht auf den falschen Massen und ist
so nicht umsetzbar - die Siedlungskarte ist bereits 658 x 658 mit 64-px-Feldern und steht 226 px tief
im Inhalt, nicht mittig.

**Das ist mein Fehler, nicht seiner** - ich habe im Auftrag Weltkarte und Siedlungskarte verwechselt
und die 1142 aus Register 469 weitergegeben, ohne sie heute nachzumessen.

## 4. Was die Antwort brauchbar macht

- **Der Weg ist klar und billig:** fester 1:1-Ausschnitt, nie skalieren, nur bei
  Groessenaenderung neu schneiden. Das ist ein `crop` in Pillow, kein Umbau.
- **Der Platz fuer die Elfen-Gebaeudebilder ist schon da:** `_ansicht_hintergrund()` gibt es seit
  dem 02.11.2026 fuer Lager, Bibliothek und die Werkstaetten (`data/gebaeude_motive.json`,
  Schluessel `ansicht_hintergrund`). Die Einzelansicht muss also nicht neu erfunden werden.
- **Feld-Masse sind geklaert:** jedes Feld traegt eine Gelaendeart (100 von 100), jedes Bauwerk
  belegt genau ein Feld. Damit gilt Claudes Fall "wenn ja": die Felder muessen ueber dem Bild
  liegen, das Bild scheint nur an den Seiten durch.

## 5. Offen (Entscheidung Daniel)

1. Die Einordnung aus Abschnitt 0 der Antwort: sechs Voelker-Panoramen an die Siedlungsansicht,
   drei Elfen-Gebaeude an die Einzelansicht.
2. Was mit der Entscheidung 1142 x 1120 (Register 469) passiert, nachdem die Flaeche heute anders
   misst.
