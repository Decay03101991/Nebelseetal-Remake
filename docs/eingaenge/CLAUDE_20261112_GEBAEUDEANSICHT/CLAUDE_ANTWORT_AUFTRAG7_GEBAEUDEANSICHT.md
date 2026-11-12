# ANTWORT AUF AUFTRAG NR. 7: Die Gebäudeansicht mit Bildhintergrund

| | |
|---|---|
| **Antwort auf** | AUFTRAG NR. 7 AN CLAUDE (Klasse Opus 5.5): DIE GEBAEUDEANSICHT MIT BILDHINTERGRUND |
| **Auftragsdatei** | `AUFTRAG_CLAUDE_GEBAEUDEANSICHT.txt` |
| **Auftrag von** | Hermes Agent „Weltenfresser“, Stand 12.11.2026, 17:2x |
| **Für** | Daniel Kössl |
| **Ort im Spiel** | Gebäudeansicht (Fläche, auf der gebaut wird) |
| **Vorgänger** | Antwort auf Auftrag Nr. 6 (Gebäudehintergrund 1:1), umgesetzt mit `main` = `25e7a17` |
| **Erarbeitet** | von Opus 5.5 Thinking: Mittel, 12.11.2026 |
| **Umsetzbar für** | `deepseek-v4-flash`, nur Pillow und Tkinter |

Die Haltezone von 8 px an der Naht ist eine richtige Korrektur und gilt ab jetzt. Mein Abschnitt D aus Antwort Nr. 6 ist durch eure Messung überholt: Kein Bedienelement liegt über dem Bild.

---

## 0. Vorschlag zur Einordnung (entscheidet Daniel)

Die neun Bilder sind zwei verschiedene Sorten und gehören an zwei verschiedene Orte:

| Bildsatz | Wofür | Raster darauf? |
|---|---|---|
| 6 Völker-Panoramen | **Siedlungsansicht** des Spielers (je nach Volk), Hintergrund hinter der 20 × 20-Siedlungskarte | ja |
| Elfen-Gebäude (Bibliothek, Kriegerakademie, Stellmacher) | **Einzelansicht** eines Gebäudes, die sich beim Klick auf das Gebäude öffnet | nein |

Wenn Daniel das anders sieht, gelten Teil A und D trotzdem. Nur Teil B betrifft allein die Siedlungsansicht.

---

## A) Wie das Bild in 1037 × 589 kommt

**Ein Weg: fester Ausschnitt 1:1, mittig, ohne Skalierung und ohne Scrollen („bewusst beschnitten“).**

- **W × H** ist die sichtbare Fläche. Bei 1460 × 940 ist sie 1037 × 589.
- **Ausschnitt** im Bild: links = abgerundet aus (1142 − W) / 2, oben = abgerundet aus (1120 − H) / 2, Größe W × H.
- Bei 1037 × 589: **links 52, oben 265**. Sichtbar ist also Bild-x 52 bis 1089 und Bild-y 265 bis 854.
- Bei schmalem Fenster (W = 691): links 225. Die Höhe bleibt gleich.
- **Ist W > 1142 oder H > 1120** (größere Fenster): Das Bild steht 1:1 in der Mitte, der Rest wird mit Fensterfarbe #17212B gefüllt. Bei welcher Fenstergröße das eintritt, ist **UNBEKANNT**. Bitte die sichtbare Fläche beim Deckel 1560 × 1040 messen.
- Der Ausschnitt wird nur bei einer Änderung der Fenstergröße neu geschnitten (Pillow `crop`). Es wird nie skaliert.

**Preis (gerechnet für 1037 × 589):**

| | Höhe | Breite |
|---|---|---|
| fehlt | 531 px = **47 %** | 105 px = 9 % |
| davon Ergänzungsband | 256 px (beide Bänder ganz) | – |
| davon gemaltes Original | 275 px (je 137 bis 138 oben und unten) | 105 px |
| sichtbar vom gemalten Original | 589 von 864 Zeilen = **68 %** | 1037 von 1142 Spalten = **91 %** |

**Ehrlich dazu:** Bei 1460 × 940 ist die Ergänzung aus Auftrag 6 **nicht sichtbar**. Sie wird erst bei Fenstern über 864 px Inhaltshöhe gebraucht. Der Aufwand war trotzdem nicht umsonst: Das Bild bleibt 1:1 und scharf, und größere Fenster bekommen keinen Rand.

**Warum nicht die anderen Wege:**
- **Einpassen** würde auf 0,526 verkleinern (589 / 1120). Das Bild wäre dann 600 × 589, mit 437 px Rand, und Register 469 („1:1“) wäre gebrochen.
- **Scrollen** widerspricht Kriterium E2.
- **Fläche ändern** geht laut eurer Messung bei 125 % nicht.

**Offen:** Der scrollbare Inhalt ist 1881 px hoch. **Was unter der Fläche steht, ist UNBEKANNT.** Bei diesem Weg darf in der Gebäudeansicht nichts unterhalb der Fläche liegen, sonst ist E2 verletzt. Bitte auflisten, was dort heute steht. Ich schlage dann einen Platz dafür vor (Seitenpanel oder Dialog).

---

## B) Wo die Gebäude stehen (Siedlungsansicht)

**Das Raster bleibt.** Begründung:
- Freie Plätze hieße: 20 feste Plätze statt 400 Felder. Das ist ein **Umbau der Spielmechanik** (Regel 3) und kein Gestaltungsthema.
- Dazu kämen Platzlisten für jedes der 6 Bilder, und Abreißen und Neubauen auf beliebigen Feldern ginge verloren.

**Maße:**
- **Feldgröße** = abgerundet aus min(W, H) / 20. Bei 589 Höhe sind das **29 px**, das Raster ist **580 × 580**. Das gilt auch bei W = 691.
- Das Raster steht mittig in der Fläche: bei 1037 × 589 bei x 228 bis 808 und y 4 bis 584. Links und rechts bleiben je 228 px freies Bild.
- **Mittelpunkte:** Ausschnittsmitte, Rastermitte und Bildmitte fallen zusammen. Der Bezug zwischen Bild und Raster bleibt also bei jeder Fenstergröße gleich.

**Wie viele Gebäude und wie groß:**
- Es müssen **20 Gebäude** Platz haben (eure Angabe). Bei einem Feld je Gebäude belegen sie 5 % der 400 Felder.
- **Gebäudekachel höchstens 2 × 2 Felder, also 58 × 58 px**:
  - Ankerpunkt ist die Mitte der Unterkante des eigenen Feldes. Das Bild ragt nach oben und zur Seite über die Nachbarfelder.
  - Gezeichnet wird zeilenweise von oben nach unten, sodass weiter unten stehende Gebäude die oberen überdecken.
  - **Der Klick gehört immer zum Feld**, nicht zum Bild.
- Ob ein Gebäude mechanisch mehr als ein Feld belegt, ist **UNBEKANNT**. Bitte in den Daten nachsehen. Wenn ja, ist die Höchstgröße 2 × Grundfläche in Feldern × 29 px.

**Wichtige Rückfrage:** Hat jedes Feld der Siedlungskarte eine **Geländeart**, die entscheidet, was dort gebaut werden darf (Auftrag 5, Punkt 3.5: Holzfäller auf Wald usw.)? Das ist **UNBEKANNT**.
- **Wenn ja:** Das gemalte Bild darf das Gelände der Felder nicht vortäuschen. Dann liegen die Felder als Geländekacheln aus T07 (Teil A) zu 80 % deckend über dem Bild. Das Bild bleibt nur an den Seiten (je 228 px) und schwach durchscheinend sichtbar.
- **Wenn nein:** Die Felder bleiben durchsichtig. Es gibt nur ein Feldnetz: Linien von 1 px in #1a0a09 mit 35 % Deckung, und beim Darüberfahren ein Rahmen von 2 px in #F2E3BF.

---

## C) Das Wappen

| Platz | Größe | Datei | Halo? |
|---|---|---|---|
| **Kopf** (rechts neben der Leiste, im Bereich 28 + 21 + 30 = 79 px unter der Leiste) | **64 px** | vorhandene 64-px-Datei, nicht neu skaliert | nein, der Kopf liegt nicht auf dem Bild. Der Hintergrund des Kopfes ist **UNBEKANNT**; bitte die Farbe nennen. |
| Einzelansicht eines Gebäudes (oben rechts in der Fläche, 16 px Abstand zum Rand) | **128 px** | vorhandene 128-px-Datei | **ja**, siehe unten |
| Dorfmarker auf der Weltkarte | – | – | **Kein gemaltes Wappen.** Es bleibt die flache Silhouette in 14 bis 16 px aus T07. |
| Siedlungsansicht | – | – | kein Wappen, es steht schon im Kopf |

**Die Untergrenze von 32 px gilt auch für den Dorfmarker.** Weil der Marker kleiner ist, kommt dort kein gemaltes Wappen hin. Selbst in der großen Stufe (Innenfläche 42 px mit Burgminiatur 30 px) bleibt dafür kein Platz von 32 px.

**Halo, wenn das Wappen auf dem Bild liegt:** ein **Doppelring**, innen 2 px Creme #F2E3BF, außen 2 px #1a0a09. Gerechnet:

| Ring | hält 3 : 1, solange das Bild darunter … |
|---|---|
| Creme #F2E3BF (Leuchtdichte 0,7758) | … höchstens Leuchtdichte **0,2253** hat |
| Dunkel #1a0a09 (Leuchtdichte 0,0046) | … mindestens Leuchtdichte **0,1137** hat |

Die beiden Bereiche überlappen sich. **Gegen jedes beliebige Pixel hält also mindestens ein Ring 3 : 1.** Creme gegen Dunkel ergibt 15,13.

Beispiel Elfen-Panorama, Grau 136 (Leuchtdichte 0,2462): Der dunkle Ring hält **5,43**, der Creme-Ring 2,79. Der dunkle Ring trägt hier.

**Bau in Pillow:**
1. Wappen um 4 px Rand erweitern.
2. Alpha mit `MaxFilter(5)` ausdehnen → Maske für den Creme-Ring (2 px).
3. Alpha mit `MaxFilter(9)` ausdehnen → Maske für den dunklen Ring (4 px).
4. Zusammensetzen: erst Dunkel, dann Creme, dann das Wappen obenauf.

---

## D) Drei Ausschlussgründe (prüfbar)

Ein Bild ist als Hintergrund **untauglich**, wenn einer davon zutrifft. Alle drei werden **nur im Ausschnitt aus A** gemessen (1037 × 589, links 52, oben 265), denn nur er ist sichtbar.

1. **Zu unruhig unter dem Raster:** Die Laplace-Varianz im Rasterbereich (580 × 580 in der Mitte) liegt über dem **1,5-Fachen des Medians** der neun Bilder. Dann gehen 29-px-Gebäude darin unter. Die Grenze ist relativ zum eigenen Satz und damit sofort messbar; der Faktor 1,5 ist ein Startwert.
2. **Horizont im Raster:** Liegt eine Horizontkante im Rasterbereich (Zeilenmittel, Nachbarsprung über 12, wie in Auftrag 6), stehen die Gebäude oberhalb davon „im Himmel“. Gilt nur für die Siedlungsansicht.
   - Ausweg ohne neues Bild: den Ausschnitt nach unten verschieben, „oben“ höchstens bis 531 (1120 − 589), bis der Horizont über dem Raster liegt.
   - Geht das nicht, ist das Bild untauglich.
3. **Zu hell oder zu dunkel unter dem Raster:** Mittlerer Grauwert im Rasterbereich über 170 oder unter 25. Dann haben Feldnetz und Hover-Rahmen keinen Kontrast. Die Werte 170 und 25 sind Startwerte.

Text, Logos, Gesichter im Vordergrund und Blut bleiben außerdem Ausschluss nach den bisherigen Negativ-Regeln. Text und Bedienelemente habt ihr schon geprüft.

---

## E) Abnahme (präzisiert)

| # | Kriterium | Prüfweg |
|---|---|---|
| 1 | Der sichtbare Ausschnitt ist genau W × H, mit links = abgerundet (1142 − W) / 2 und oben = abgerundet (1120 − H) / 2. Kein Pixel ist skaliert. | Messung bei 1460 × 940 und bei schmalem Fenster (W = 691) |
| 2 | Ohne Scrollen: Das Raster 580 × 580 liegt ganz in der Fläche, und unter der Fläche steht nichts | Messung: Rasterkante ≤ H, Inhaltshöhe = H |
| 3 | Wappen 64 und 128 px: erkennbar und nicht Matsch | Auge (Daniel) bei 100 % |
| 4 | Doppelring: mindestens ein Ring ≥ 3 : 1 gegen jedes Pixel darunter | WCAG-Rechnung je Ringpixel gegen das Bild darunter |
| 5 | Kein Text und kein Bedienelement im Bild | Sicht, 9 Bilder (erledigt) |
| 6 | Keines der 6 Panoramen fällt unter Ausschlussgrund 1 bis 3 | Messung wie in D |
| 7 | Gebäudebild höchstens 58 × 58 px, verankert an der Unterkante des Feldes, Klick trifft das Feld | Messung im Programm |

---

## Was ich nicht geprüft habe

- **Die Bilder:** Ich habe sie nicht gesehen. Ob ein Horizont im Rasterbereich liegt (Ausschlussgrund 2), weiß ich nicht.
- **Inhalt unter der Fläche:** Was die 1881 px Inhaltshöhe füllt, ist **UNBEKANNT**.
- **Größere Fenster:** Die sichtbare Fläche beim Deckel 1560 × 1040 ist **UNBEKANNT**.
- **Mechanik der Siedlungskarte:** Ob die Felder Geländearten tragen und wie viele Felder ein Gebäude belegt, ist **UNBEKANNT**. Davon hängt ab, ob die Felder deckend sind (B).
- **Kopf:** Seine Hintergrundfarbe kenne ich nicht.
- **Lesbarkeit der Gebäude:** Ob die fertigen Gebäudebilder bei 58 px noch lesbar sind, muss Daniel mit dem Auge prüfen. Ihre Originalgröße ist **UNBEKANNT**.
- **Startwerte:** Die Faktoren 1,5, 12, 170 und 25 sind Startwerte und nicht an euren Bildern geprüft.

---

Ende der Antwort auf Auftrag Nr. 7.
