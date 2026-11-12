# ANTWORT AUF AUFTRAG NR. 5: Die Ressourcenleiste (T08), 34 Pixel hoch

| | |
|---|---|
| **Antwort auf** | AUFTRAG NR. 5 AN CLAUDE (Klasse Opus 5.5): DIE RESSOURCENLEISTE (T08) - 34 PIXEL HOCH |
| **Auftragsdatei** | `AUFTRAG_CLAUDE_RESSOURCENLEISTE.txt` |
| **Auftrag von** | Hermes Agent „Weltenfresser“, Projekt Nebelseetal Remake, Stand 12.11.2026, 11:2x |
| **Für** | Daniel Kössl |
| **Ort im Spiel** | T08 Ressourcenleiste (nicht T07, nicht T10) |
| **Vorgänger** | Antwort auf Auftrag Nr. 4 (T07 Angriffsfläche), `CLAUDE_ANTWORT_AUFTRAG4_ANGRIFFSFLAECHE.md` |
| **Erarbeitet** | von Opus 5.5 Thinking: Mittel, 12.11.2026 |

Die Gliederung folgt dem Auftrag: Teil A bis E entsprechen Abschnitt 4 des Auftrags. Am Ende steht ein Nachtrag zu T07, der Abschnitt 3 des Auftrags beantwortet.

**Grundlagen der Werte:**
- **Textbreiten** sind mit Liberation Sans gemessen. Diese Schrift hat dieselben Zeichenbreiten wie Arial, die Werte gelten also für Arial.
- **Kontraste** sind nach WCAG gerechnet.
- **Pixelangaben** meinen dieselben logischen Pixel wie eure Messung (Auftrag Abschnitt 2).
- **Farben:** nur aus Auftrag Abschnitt 2.4 (Handbuch Teil 1.2). Ich habe keine neuen Farben verwendet.

---

## Teil A – Raster (Auftrag 4, Teil A)

### Formel für alle Breiten

- **B** ist die Leistenbreite, **n** die Zahl der sichtbaren Zellen.
- **Zellbreite W** = abgerundet aus (B − 32 − (n − 1)) / n.
  - 32 px sind die beiden Endstücke (je 16 px).
  - n − 1 sind die 1-px-Trenner.
- **Obergrenze:** W ist höchstens 132 px. Mehr Platz geht nicht in die Zellen.
- **Restpixel aus dem Abrunden:** Sie werden als glattes Band zwischen Endstück und erster bzw. letzter Zelle verteilt, links abgerundet und rechts aufgerundet.

### Was sich mit der Zellbreite ändert (Regel für das Weichen)

| Zellbreite W | Was angezeigt wird |
|---|---|
| ab 100 px | Name, Rate und Zahl |
| 62 bis 99 px | Name und Zahl. Die Rate fällt weg und steht nur noch im Tooltip. |
| unter 62 px | Felder werden ausgeblendet, in dieser Reihenfolge: **Punkte → Pferde → Siedler**. Stattdessen erscheint eine Zelle „+1“, „+2“ usw. (28 px breit). Beim Darüberfahren zeigt sie die ausgeblendeten Felder. |

**Wolle und Leder werden nie ausgeblendet.** Das war Daniels erster Befund (Auftrag Abschnitt 1).

Herleitung der Schwellen:
- **100 px:** Der breiteste Name „Nahrung“ (41,1 px) plus 6 px Abstand plus die Rate „+1.234/h“ (39,2 px) plus 12 px Innenabstand ergeben 98,3 px.
- **62 px:** Die breiteste Zahl „999,9M“ (50,0 px) plus 12 px Innenabstand ergeben 62 px.

### A1 / A2 / A3 – die drei Breiten

| | A1: 1446 px | A2: 1186 px | A3: 986 px |
|---|---|---|---|
| sichtbare Zellen | 11 | 11 | 11 |
| Zellbreite | **127 px** | **104 px** | **85 px** |
| Restpixel links / rechts | 3 / 4 | 0 / 0 | 4 / 5 |
| Rate sichtbar | ja | ja | nein |
| abgeschnittene Zellen | keine | keine | keine |

Auch bei 986 px passen alle elf Felder. Das erste Feld weicht erst bei einer Leiste unter 724 px, also einem Fenster von etwa 738 px.

Die Schrift ist bei allen drei Breiten gleich: Name 10 px fett, Zahl 15 px fett, Rate 10 px normal. Auch Innenabstand (6 px links und rechts) und Trenner bleiben gleich. **Nichts springt zwischen den Breiten.**

Damit ist der Überlauf aus Auftrag 2.3 gelöst: Die Leiste ist nie breiter als das Fenster, sie passt die Zellbreite an.

---

## Teil B – Gestaltung des Bandes (Auftrag 4, Teil B)

### B1 Aufbau aus drei Stücken (9-Slice, waagerecht)

- **Linkes Endstück:** 16 × 34 px.
- **Mitte:** eine Kachel von **64 × 34 px**, die nur waagerecht **wiederholt** wird. Sie wird nie gedehnt.
- **Rechtes Endstück:** 16 × 34 px, das gespiegelte linke Endstück.
- **Unterkante:** eine Linie über die ganze Breite, 1 px, in der Rahmenfarbe #b8862e, auf y = 33.

Die Trenner sind **nicht** in die Kachel gemalt. Die Kachel ist 64 px breit, die Zellen 85 bis 127 px; gemalte Trenner würden also nie auf die Zellgrenzen treffen.

### B2 Zellen

- **Trenner:** eine Linie, 1 px breit, in der Rahmenfarbe #b8862e, von y = 7 bis y = 27 (20 px hoch). Kontrast gegen die Leiste: 5,94. Ein Ornament gibt es nicht, weil es Platz für Zahlen frisst.
- **Grundfarbe:** Alle Zellen haben denselben Grund, nämlich das Band selbst (Mittel #1a0a09). Ich empfehle keine abwechselnden Farben, weil der Zustand „kritisch“ den Grund als Merkmal braucht.
- **Zierrat** gibt es nur in den Endstücken, in Gold. Dort steht nie Text.

#### Aufbau einer Zelle (Höhe 34 px)

| Zeile | Lage | Inhalt |
|---|---|---|
| Zeile 1 | Schriftbox y = 2 bis 15 | Name links, 10 px fett, Farbe #b8862e. Rate rechts, 10 px normal, Farbe #F2E3BF. |
| Zeile 2 | Schriftbox y = 14 bis 32 | Zahl **rechtsbündig**, 15 px fett, Farbe #F2E3BF. |

### B3 Zustände

Jeder Zustand hat ein Merkmal, das keine Farbe ist.

| Zustand | Darstellung | Merkmal ohne Farbe |
|---|---|---|
| normal | wie oben | – |
| **kritisch** (Bestand 0) | Zellgrund wird #3e1c1a. Die Zahl „0“ steht in Warnung #ff8a70. Darunter liegt ein **Unterstrich von 2 px** in Warnung (y = 31 bis 32, über die Breite minus Innenabstand). | Unterstrich und hellerer Grund |
| **Unterdeckung** (Verbrauch größer als Ertrag) | Das Zeichen **▼** (15 px, 9,9 px breit) steht links vor der Zahl, in Warnung. Die Rate erscheint mit „−“ in Warnung. | ▼ und Minuszeichen. Das ▼ sitzt in der Zahlenzeile und bleibt daher auch bei A3 sichtbar. |
| steigt / fällt (außer der Reihe) | Der Platz der Rate zeigt für kurze Zeit die Änderung, z. B. „+250“ in Erfolg #a5d67a oder „−250“ in Warnung. | Vorzeichen |

**Wichtig zu „steigt / fällt“:** Alle Werte steigen im Minutentakt (Auftrag 3.5). Würde jeder Takt angezeigt, flackerten alle elf Felder jede Minute. Deshalb empfehle ich die Anzeige **nur für Änderungen außerhalb des Takts**, etwa Kauf, Plünderung oder Bau.
- Ob das Spiel solche Änderungen unterscheidet, ist **UNBEKANNT**. Wenn nicht, entfällt dieser Zustand.
- Die Anzeigedauer ist reine Oberfläche, keine Spielmechanik. Mein Vorschlag sind 3 Sekunden; Daniel entscheidet.

Das Zeichen ▼ ist ein Schriftzeichen und kein Emoji. Liberation Sans enthält es; dass es in Arial vorhanden ist, bitte in Tkinter prüfen.

### B4 Breitere Fenster

Ab einer Zellbreite von 132 px wachsen die Zellen nicht mehr. Die elf Zellen bleiben als Block in der Mitte, und das Band läuft links und rechts als leere Fläche weiter. Das ist ab einer Leistenbreite von 1494 px der Fall (11 × 132 + 10 + 32).

---

## Teil C – Zahlen (Auftrag 4, Teil C)

### C1 Schrift

- **Zahl:** Arial fett, 15 px. Die Ziffern von Arial sind von Haus aus tabellarisch: alle zehn sind gleich breit, bei 15 px je 8,34 px.
- **Rechtsbündig:** Die Einerstelle steht immer an derselben Stelle. Beim Wechsel von 999 auf 1.000 springt deshalb nichts.
- **Pixel statt Punkt:** In Tkinter bedeutet „Arial 11“ 11 **Punkt**. Bei Daniels Skalierung von 125 % ergibt das mehr Pixel. Die Größen hier sind Pixelgrößen.
  - Prüfung: „Nahrung“ in 10 px fett muss 41 px breit sein. Wie Tkinter Punkt bei 125 % in Pixel umrechnet, ist **UNBEKANNT**, bitte messen.

### C2 Kürzen

Es gibt höchstens 6 Zeichen. Gekürzt wird **abgerundet**, damit nie mehr angezeigt wird als vorhanden.

| Bestand | Anzeige |
|---|---|
| 0 bis 99.999 | ganz, mit Tausenderpunkt („12.345“) |
| 100.000 bis 999.999 | „100k“ bis „999k“ |
| ab 1 Million | „1,00M“ bis „9,99M“, dann „10,0M“, dann „100M“ |

Die genauen Zahlen stehen im Tooltip.

Ob ein Wert über 999 Millionen steigen kann, ist **UNBEKANNT**. Bitte die Obergrenzen im Originalhandbuch nachsehen.

### C3 Name und Zahl

**Untereinander:** der Name klein oben, die Zahl groß unten. Gemessene Breiten:
- Name: 21,1 px (Holz) bis 41,1 px (Nahrung).
- Zahl: höchstens 50,0 px.

Nebeneinander bräuchte jede Zelle mindestens 103 px. Bei A3 ginge das nicht. Kürzel wie „Na“ oder „Ho“ empfehle ich nicht; die vollen Namen passen ja.

Gemessene Namensbreiten bei 10 px fett:

| Siedler | Nahrung | Holz | Stein | Metall | Gold | Mana | Wolle | Leder | Pferde | Punkte |
|---|---|---|---|---|---|---|---|---|---|---|
| 33,4 | 41,1 | 21,1 | 24,5 | 28,3 | 22,8 | 25,6 | 26,5 | 27,2 | 31,1 | 33,3 |

### C4 Rate

**Ja**, rechts in Zeile 1, 10 px normal, Format „+120/h“, gekürzt nach denselben Regeln wie C2. Gemessene Breiten: „+120/h“ 30,9 px, „+1.234/h“ 39,2 px. Ab einer Zellbreite unter 100 px fällt die Rate weg, sie verdrängt also nie die Zahl.

- **Voraussetzung:** Das Spiel liefert den Ertrag je Zeit. Die Leiste rechnet nicht selbst (Auftrag 5.6).
- Für Siedler, Pferde und Punkte gibt es eine Rate nur, wenn das Spiel eine hat. Sonst bleibt der Platz leer.

---

## Teil D – Bilder (Auftrag 4, Teil D)

### D1 Prompts für das Band

**Stil-Block:**

```
seamless horizontally tileable UI strip texture, painterly digital art, dark carved wood inlaid with oxblood leather, very low contrast, soft warm light, no outlines
```

**Motiv Mitte (64 × 34):**

```
dark oxblood leather band with faint embossed grain, subtle stitched edge along the bottom, average color #1a0a09, no ornaments, nothing larger than 6 px
```

**Motiv Endstück (16 × 34):**

```
small gilded metal clasp cap closing the end of a leather strip, aged gold #b8862e highlights, fits inside 16x34
```

**Negativ-Block:**

```
no text, no letters, no numbers, no icons, no emoji, no faces, no logos, no blood, no 3D render, no photo, no bright spots, no gradient across the strip, no perspective
```

**Prüfung der Mitte:**

1. **Helligkeit:** Kein Pixel heller als die Fläche #3e1c1a (relative Leuchtdichte 0,0193). Dann liegt der Name (#b8862e) überall bei mindestens 4,68. Die Grenze für 4,5 liegt bei Leuchtdichte 0,0221.
2. **Naht, gemessen:** Spalte 0 und Spalte 63 dürfen je Farbkanal höchstens 6 Werte voneinander abweichen.
3. **Naht, mit dem Auge:** Drei Kacheln nebeneinanderlegen und bei 200 % ansehen. Es darf keine Naht sichtbar sein.
4. **Herstellung:** in 512 × 272 erzeugen und erst nach der Nahtprüfung verkleinern.

### D2 Symbole

**Es gilt Text allein.** Begründung:
- Ein Symbol bräuchte mindestens 24 px (Auftrag 2.5).
- Bei 34 px Höhe ließe das nur 5 px Rand oben und unten. Der Name hätte dann keinen Platz mehr, und die Zelle würde um etwa 30 px breiter.
- Bei A3 würden die elf Felder nicht mehr passen.
- Bei 0 von 9 erkannten Symbolen spricht nichts für einen neuen Versuch.

### D3 Ohne Bilddatei

- Das Band wird eine glatte Fläche in #1a0a09 mit der Goldlinie unten.
- Die Endstücke bleiben als glatte Fläche von je 16 px stehen.
- Trenner, Text und Zustände sind unverändert.

**Das Layout hängt nie vom Bild ab.** Fehlt die Datei, verschiebt sich kein Pixel; nur die Struktur der Oberfläche ist weg.

---

## Kontraste (zu Auftrag 4, Teil E und Abschnitt 6)

| Element | auf Leiste #1a0a09 | auf Fläche #3e1c1a (kritisch) |
|---|---|---|
| Zahl und Rate #F2E3BF | 15,13 | 11,92 |
| Name #b8862e | 5,94 | 4,68 |
| Warnung #ff8a70 (Text, ▼, Unterstrich) | 8,36 | 6,58 |
| Erfolg #a5d67a | 11,45 | 9,02 |
| Gold #FFCC33 (nur Endstücke) | 12,77 | – |
| Trenner #b8862e (Zeichen) | 5,94 | 4,68 |

Alle Texte liegen über 4,5, alle Zeichen über 3.

---

## Teil E – Abnahme (Auftrag 4, Teil E)

### E1 Kriterien

| # | Kriterium | Prüfweg |
|---|---|---|
| 1 | Die Leiste ist bei jeder Fensterbreite 34 px hoch. | Messung im Programm bei 1460, 1200 und 1000 px |
| 2 | Bei 1446, 1186 und 986 px ist keine Zelle abgeschnitten, und alle 11 Felder sind sichtbar. | Messung: rechte Kante der letzten Zelle ≤ B − 16 |
| 3 | Beim Wechsel von 999 auf 1.000 bleibt die Einerstelle auf derselben x-Position. | Messung: Bildschirmfoto vorher und nachher, Pixelvergleich |
| 4 | Jeder Text liegt bei mindestens 4,5 : 1 gegen seinen Grund, auch gegen das hellste Pixel der Mittelkachel. | Rechnung mit Pipette, hellstes Pixel ≤ #3e1c1a |
| 5 | Die Mittelkachel zeigt bei drei Wiederholungen keine Naht. | Auge bei 200 %; Messung Spalte 0 gegen 63, ≤ 6 je Kanal |
| 6 | Die Leiste wird nirgends gedehnt. | Messung: Die Kachel ist bei jeder Breite 64 px breit |
| 7 | Wolle und Leder sind bei allen drei Breiten sichtbar. | Auge |
| 8 | Die Zustände „kritisch“ und „Unterdeckung“ sind in Graustufen erkennbar. | Auge an einem entsättigten Bildschirmfoto |
| 9 | Ohne Bilddatei sieht die Leiste vollständig aus, und kein Element verschiebt sich. | Datei umbenennen, Bildschirmfotos vergleichen |
| 10 | Kein Wert hat mehr als 6 Zeichen. | Testwerte 99.999 / 100.000 / 1.234.567 einsetzen |

### E2 Nicht geprüft

- **Schriftgröße bei 125 %:** Wie Tkinter bei Daniels Skalierung Punkt in Pixel umrechnet, konnte ich nicht prüfen. Die Breiten stammen aus der Messung mit Liberation Sans, nicht aus Tkinter.
- **Rate und Änderungen:** Ob das Spiel eine Rate liefert und Änderungen außerhalb des Takts unterscheidet, weiß ich nicht.
- **Obergrenzen:** Die Höchstwerte der Ressourcen kenne ich nicht.
- **Stil:** Ob das Band Daniels Stilgefühl trifft, kann nur er beurteilen.

---

## Nachtrag zu T07 (beantwortet Auftrag Nr. 5, Abschnitt 3)

### Zu 3.2: B7 Dorf betritt oder verlässt die Welt

Ergänzt die Anzeigeregeln B1 bis B6 aus der Antwort auf Auftrag Nr. 4.

- **Betreten:** Der Marker erscheint erst in dem Moment, in dem das Dorf auf seinem Feld ankommt. Vorher erscheint er nicht, auch nicht als Schatten. Im Seitenpanel steht einmal: „Fraktion X hat diese Welt betreten.“
- **Verlassen:** Der Marker verschwindet im selben Moment, und das Feld ist sofort frei.
  - Ist das Dorf gerade ausgewählt, wird die Auswahl aufgehoben. Im Panel steht dann: „Dorf hat die Welt verlassen.“
  - Märsche, die auf dieses Dorf zielen, verhalten sich wie bei Regel 9 der Sprungregeln (`Claude_Opus_5.5_Sprungregeln_Weltkarte.md`).

### Zu 3.4: korrigierte Reihenfolge der Kacheln (ersetzt E1 aus Auftrag Nr. 4)

Nach Häufigkeit: Grasland, Steppe, Wald, Hügel, Berg, Sumpf, Nebelsee.

### Zu 3.1 und 3.3

Zur Kenntnis genommen, keine Änderung nötig. Regel B6 (wer die Anzeige gewinnt) gilt für benachbarte Dörfer wie beschrieben, und das 29-px-Feld bleibt.

---

Ende der Antwort auf Auftrag Nr. 5.
