# ANTWORT AUF AUFTRAG NR. 6: Der Gebäudehintergrund 1:1

| | |
|---|---|
| **Antwort auf** | AUFTRAG NR. 6 AN CLAUDE (Klasse Opus 5.5): DER GEBAEUDEHINTERGRUND 1:1 |
| **Auftragsdatei** | `AUFTRAG_CLAUDE_MESHY_1ZU1.txt` |
| **Auftrag von** | Hermes Agent „Weltenfresser“, Stand 12.11.2026, 15:1x |
| **Für** | Daniel Kössl |
| **Ort im Spiel** | Gebäudeansicht, Fläche 1142 × 1120 px |
| **Vorgänger** | Antwort auf Auftrag Nr. 5 (T08 Ressourcenleiste) |
| **Erarbeitet** | von Opus 5.5 Thinking: Mittel, 12.11.2026 |
| **Umsetzbar für** | `deepseek-v4-flash`, nur Pillow |

---

## 0. Zuerst: Die Rechnung im Auftrag stimmt nicht

Der Auftrag vermischt in Abschnitt 1 zwei verschiedene Wege:

| | **Weg 1:** schmal schneiden, vergrößern | **Weg 2:** breit schneiden, ergänzen |
|---|---|---|
| Beschnitt | 1536 → **881** px breit, Höhe bleibt 864 | 1536 → **1142** px breit, Höhe bleibt 864 |
| Verlust an Breite | 655 px = **42,6 %** (nicht 45 %) | 394 px = **25,7 %** |
| Danach | ×1,296 vergrößern → 1142 × 1120 | 1:1, **256 px Höhe ergänzen** (1120 − 864) |
| Ergänzung nötig? | **nein**, das Bild ist dann schon fertig | ja, 128 px oben + 128 px unten |
| Schärfe | verliert (Vergrößerung um 30 %) | **unverändert** im Originalbereich |

Die „239 px“ (1120 − 881) ziehen eine **Breite** von einer **Höhe** ab. Dieser Fall kommt in keinem der beiden Wege vor.

**Empfehlung: Weg 2.** Er entspricht wörtlich Daniels Entscheidung („mittig beschnitten und oben/unten ergänzt“). Er verliert 17 Prozentpunkte weniger Bild und vergrößert nicht, sodass Kriterium E3 von selbst erfüllt ist. **Alles Folgende gilt für Weg 2.** Daniel bestätigt das bitte einmal.

---

## A) Wo wird geschnitten?

**Regel (für Panorama und Gebäude gleich):**

1. **cx** ist die waagerechte Mitte des Hauptmotivs im Originalbild, in px von links. Hauptmotiv ist beim Panorama die Burg oder das Wahrzeichen des Volkes, beim Gebäude das Gebäude selbst.
2. Schnittkante links: **x0 = cx − 661**, begrenzt auf **0 bis 394**.
3. Ausschnitt: x0 bis x0 + 1142, volle Höhe 0 bis 864.

Die 661 ergibt sich aus der freien Zone rechts der linken Spalte: (180 + 1142) / 2 = 661. So steht das Motiv in der Mitte des **sichtbaren** Bereichs und nicht unter der Spalte (siehe D). Ohne Angabe gilt cx = 768 (Bildmitte), also x0 = 107.

**cx wird von Daniel einmal je Bild mit dem Auge bestimmt** und als Liste übergeben. Flash soll cx nicht selbst schätzen. Diese Liste ist für alle 9 Bilder **UNBEKANNT**:

| Datei | cx | x0 (gerechnet) |
|---|---|---|
| 6 Panoramen, 3 Elfen-Gebäude | Daniel trägt ein | clamp(cx − 661, 0, 394) |

**Was in der Mitte bleiben muss und was weg darf:**

| Bildtyp | Muss ganz drin sein | Darf weg |
|---|---|---|
| Panorama | Wahrzeichen bzw. Burg des Volkes; Horizont und Himmel bleiben ohnehin, weil nicht in der Höhe geschnitten wird | äußere Landschaft links und rechts |
| Gebäude | das ganze Gebäude mit Dachspitzen und Sockel, mit mindestens **24 px** Abstand zur Schnittkante | Umgebung neben dem Gebäude |
| Wappen-Satz | **wird nicht geschnitten.** Er wird freigestellt (Teil C) und ist kein Hintergrund. | – |

**Sonderregeln:**
- **Angeschnittene Figur oder angeschnittenes Objekt an der Schnittkante:** x0 um höchstens ±40 px verschieben, bis es ganz drin oder ganz draußen ist. Geht das nicht, bleibt x0, und Daniel bekommt eine Notiz.
- **Gebäude breiter als 1094 px** (1142 − 2 × 24): Weg 2 geht für dieses Bild nicht. Dann bitte melden, Daniel entscheidet.

---

## B) Ergänzung: 128 px oben und 128 px unten

**Ein Verfahren** (beschrieben für oben, unten genauso, nur gespiegelt):

1. **Band holen:** die obersten 128 Zeilen des Ausschnitts, senkrecht gespiegelt (Pillow: `ImageOps.flip`). Die gespiegelte Kante liegt damit nahtlos am Original an.
2. **Unschärfe:** eine Kopie des Bandes mit `GaussianBlur` Radius 8. Mischen mit Maske M1:
   - an der Naht scharfes Band,
   - nach 32 px vollständig unscharf,
   - dazwischen linear.

   Das verdeckt die Spiegelachse, ohne an der Naht einen Schärfesprung zu erzeugen.
3. **Farbfläche:** die mittlere Farbe der äußersten 16 Zeilen des Originals (oben: Zeilen 0 bis 15; Pillow: `ImageStat.Stat(...).mean`). Mischen mit Maske M2: an der Naht 0 %, am Außenrand 100 % Farbfläche, linear.
4. **Abdunkeln:** Fläche #1a0a09. Mischen mit Maske M3:
   - die äußeren 64 Zeilen zu 100 % dunkel,
   - die inneren 64 Zeilen linear von 100 % auf 0 % an der Naht.
5. Das Band an y = 0 einsetzen. Das Original kommt an y = 128.

Alle Masken sind senkrechte Verläufe; in Pillow: `Image.linear_gradient("L")`, auf 1142 × 128 skaliert, bei Bedarf gespiegelt. Gemischt wird mit `Image.composite`.

**Horizont auf der Ergänzung:** Eine Spiegelung würde einen zweiten Horizont erzeugen.
- **Prüfung:** In den 128 Randzeilen des Originals wird je Zeile die mittlere Helligkeit gebildet. Liegt irgendwo der Unterschied zweier Nachbarzeilen über **12** (Skala 0 bis 255), gilt der Rand als „Horizont im Rand“.
- **Folge:** Für diese Seite entfallen die Schritte 1 und 2. Das Band besteht dann nur aus Farbfläche und Abdunkeln (Schritte 3 und 4).
- Die Schwelle 12 ist ein **Startwert**, keine Messung. Bitte an den 9 Bildern einmal prüfen und bei Bedarf ändern.

**Grenzen des Verfahrens:**
- Die Ergänzung zeigt **kein neues Motiv**, nur gespiegelte und auslaufende Struktur. Sie wirkt wie ein Nebel- bzw. Dunkelrand und nicht wie ein Teil der Szene.
- Bei kräftig gemusterten Rändern (z. B. Pflaster bis zur Unterkante) bleibt die Spiegelung in den Zeilen 64 bis 128 von der Naht entfernt schwach erkennbar.
- Mehr leistet Pillow ohne Malen nicht.

**Kontrast der Bedienelemente:** Das Abdunkeln hilft ihm. Die oberen 64 Zeilen sind ganz #1a0a09, und die Kopfzeile (rund 56 px) liegt vollständig darin. Grenzwerte für den Hintergrund unter Text oder Zeichen (gerechnet):

| Element | Pflicht | hellstes Pixel darunter höchstens | Grauwert-Entsprechung |
|---|---|---|---|
| Text #F2E3BF | 4,5 : 1 | rel. Leuchtdichte **0,1335** | Grau ≤ 102 |
| Zeichen #b8862e | 3 : 1 | rel. Leuchtdichte **0,0581** | Grau ≤ 68 |

**Messbare Werte zu B:**
- **Naht:** Mittlerer Betragsunterschied zwischen Zeile 127 und Zeile 128 (bzw. 991 und 992) ≤ 1,5 × Median der Nachbarzeilen-Unterschiede im Originalbereich.
- **Kanten:** `FIND_EDGES` auf Graustufen. Der Zeilenmittelwert an der Naht (±2 Zeilen) ist ≤ 1,5 × Median der Zeilenmittelwerte im Original.
- **Helligkeit:** Die 8 Ergänzungszeilen direkt an der Naht weichen im Mittel um höchstens ±5 (0 bis 255) von den 8 Originalzeilen daneben ab. Weiter außen ist die Ergänzung **gewollt dunkler**.

**Hinweis zu E2:** Die Naht ist bei Weg 2 **waagerecht**, nicht senkrecht wie im Auftrag geschrieben. Die Prüfung oben ist entsprechend gebaut.

---

## C) Wappen freistellen

**Erst prüfen, ob der Grund einfarbig ist:**
- Vier Eckfelder von 32 × 32 px messen (`ImageStat`: Mittelwert und Standardabweichung je Kanal).
- **Einfarbig** heißt: Die vier Mittelwerte weichen je Kanal um höchstens 4 voneinander ab, und jede Standardabweichung ist ≤ 3.
- Ob das zutrifft, ist **UNBEKANNT**. Bitte messen.

**Grundmodell (für beide Fälle dasselbe Verfahren):** Ein 2 × 2-Bild aus den vier Eckfarben wird mit `BILINEAR` auf die volle Bildgröße skaliert.
- Ist der Grund einfarbig, ergibt das eine glatte Fläche.
- Ist er ein Verlauf, wird der Verlauf damit nachgebildet. Nur bei unregelmäßigem Grund (Flecken, Rauschen über 3) reicht das nicht. Dann bitte melden.

**Verfahren:**

1. **Abstand d:** je Pixel der größte Betragsunterschied über R, G und B zwischen Bild und Grundmodell (`ImageChops.difference`, dann die Kanäle mit `ImageChops.lighter` zusammenführen).
2. **Schwellen:**
   - t0 = 3 × größte Eck-Standardabweichung + 2.
   - t1 = t0 + 40. Das ist ein Startwert.
3. **Nur den zusammenhängenden Grund entfernen:** Maske „nah am Grau“ (d ≤ t1) erstellen und mit `ImageDraw.floodfill` von allen vier Ecken aus füllen. **Nur der von außen erreichbare Grund wird transparent.** Graue oder silberne Teile im Wappen bleiben erhalten.
4. **Alpha** im gefüllten Bereich:
   - d ≤ t0 → 0,
   - d ≥ t1 → 255,
   - dazwischen linear (`ImageMath`).

   Außerhalb des gefüllten Bereichs ist Alpha immer 255.
5. **Grauer Saum weg:** Für Pixel mit Alpha zwischen 0 und 255 wird die Farbe zurückgerechnet. Je Kanal gilt: echte Farbe = (Pixel − (1 − a) × Grund) / a, mit a = Alpha / 255, begrenzt auf 0 bis 255 (`ImageMath` je Kanal).
6. **Verkleinern** nur vormultipliziert: nach `RGBa` wandeln, mit `LANCZOS` skalieren, zurück nach `RGBA`. Sonst entsteht beim Verkleinern ein neuer dunkler Saum.

**Zwei Größen:** Beide Zielgrößen sind **UNBEKANNT**. Bitte die Pixel nennen: „klein für die Karte“ und „groß für den Kopf“.
- Nach meiner T07-Antwort zeigt die Karte das Wappen als **flache Silhouette** in 14 bzw. 16 px und nicht als gemaltes Bild.
- Ein gemaltes Wappen empfehle ich **nicht unter 32 px**. Darunter wird es Matsch, wie bei den 0 von 9 erkannten Symbolen.

**Prüfung, dass nichts fehlt und kein Saum bleibt:**
- **Deckungsgrad** angeben: Anteil der Pixel mit Alpha = 255, mit Alpha zwischen 0 und 255 und mit Alpha = 0.
  - Startwert: Der halbtransparente Anteil liegt bei höchstens 5 % des deckenden Anteils. Mehr deutet auf einen ausgefransten Rand.
- **Saumwert:** Anteil der halbtransparenten Pixel, deren zurückgerechnete Farbe näher als t0 am Grau liegt. Ziel ≤ 1 %.
- **Auge (Daniel):** Das Ergebnis bei 200 % auf Magenta #FF00FF und auf Schwarz legen. Es dürfen weder ein grauer Rand noch Löcher sichtbar sein.
- **Schlagschatten des Wappens auf dem grauen Grund:** Ein Schatten bliebe als halbtransparenter dunkler Fleck erhalten. Ob es einen gibt, ist **UNBEKANNT**; das prüft Daniel mit dem Auge.

---

## D) Zonen auf 1142 × 1120

| Zone | x | y | Inhalt |
|---|---|---|---|
| Kopf, ruhig | 0 bis 1142 | 0 bis 128 | Ergänzung, die oberen 64 Zeilen ganz dunkel; Kopfzeile (56 px) liegt darin |
| linke Spalte, ruhig | 0 bis 180 | ganze Höhe (**UNBEKANNT**, bitte messen) | Randlandschaft, kein Motiv |
| Fuß, ruhig | 0 bis 1142 | 992 bis 1120 | Ergänzung; die Statuszeile liegt darin, falls sie ≤ 128 px hoch ist (Höhe **UNBEKANNT**) |
| **Hauptzone** | **180 bis 1142** (962 px) | **128 bis 992** (864 px) | Gebäude bzw. Wahrzeichen, Mitte bei x = 661 (Regel A) |

**Linke Spalte:** Ob sie einen eigenen, deckenden Grund hat, ist **UNBEKANNT**.
- Mit deckendem Grund in Fensterfarbe #17212B hat Text #F2E3BF darauf **12,81**. Dann ist nichts weiter zu tun.
- Liegt der Text direkt auf dem Bild, muss das hellste Pixel unter der Spalte die Grenzen aus B einhalten. Bei hellen Panoramen gelingt das nur mit einem deckenden oder halbdeckenden Grund. **Empfehlung: deckender Grund.**

---

## E) Abnahme (ergänzt und präzisiert)

| # | Kriterium | Prüfung |
|---|---|---|
| 1 | Ergebnis ist exakt 1142 × 1120 | Bildmaß |
| 2 | Keine sichtbare **waagerechte** Naht bei y = 128 und y = 992 | Zeilenvergleich und `FIND_EDGES` wie in B |
| 3 | Laplace-Varianz im Originalbereich (y 128 bis 992) gleich dem Ausschnitt vor der Ergänzung, Abweichung 0 %, weil nicht vergrößert wird | Laplace-Kern 3 × 3 (`ImageFilter.Kernel`), `ImageStat` var |
| 4 | Unter Text hellstes Pixel ≤ 0,1335, unter Zeichen ≤ 0,0581 (rel. Leuchtdichte) | WCAG-Rechnung je Pixel in den Zonen aus D |
| 5 | Wappen: Saumwert ≤ 1 %, Deckungsgrad genannt, Sichtprüfung auf Magenta ohne Befund | wie in C |
| 6 | Hauptmotiv vollständig in der Hauptzone | Auge (Daniel), mit der cx-Liste |
| 7 | Naht-Helligkeit: ±5 zwischen den 8 Zeilen innen und außen | `ImageStat` mean |

---

## Was ich nicht geprüft habe

- **Die Bilder selbst:** Ich habe keines der 9 Meshy-Bilder gesehen. Deshalb kenne ich weder cx noch die Lage der Horizonte, Figuren am Rand, die Gebäudebreite (Grenze 1094 px), den Wappengrund oder einen Schlagschatten.
- **Startwerte:** Die Schwellen (Horizont 12, Naht 1,5 ×, t1 = t0 + 40, Saum 1 %, halbtransparenter Anteil 5 %) sind Startwerte und nicht an diesen Bildern geprüft.
- **Unbekannte Maße:** Höhe der Statuszeile, Höhe der linken Spalte und ob sie einen deckenden Grund hat, ob die beiden Textzeilen des Kopfes auf dem Bild oder auf einem Band liegen, die beiden Wappengrößen.
- **Weg 1:** Wie stark die Vergrößerung um ×1,296 die Laplace-Varianz senkt, habe ich nicht gemessen. Erwartet ist deutlich mehr als 10 %. Das ist ein weiterer Grund für Weg 2.

---

Ende der Antwort auf Auftrag Nr. 6.
