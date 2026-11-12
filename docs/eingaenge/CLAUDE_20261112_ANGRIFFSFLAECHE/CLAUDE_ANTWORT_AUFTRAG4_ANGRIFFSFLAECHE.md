# Antwort auf Auftrag Nr. 4: Die Angriffsfläche (T07) mit den echten Maßen

Von Opus 5.5 Thinking: Mittel erarbeitet, 12.11.2026. Für Hermes „Weltenfresser“ und Daniel Kössl.
Alle Kontrastwerte sind gerechnet (WCAG-Leuchtdichte), nicht geschätzt.

**Vorab, bitte zuerst lesen:** Das Handbuch vom 11.11. lag mir bei dieser Antwort nicht vor, und auf den Projektordner hatte ich keinen Lesezugriff. Die Fraktionsfarben aus Teil 1.2 konnte ich deshalb nicht wörtlich übernehmen. Ich rechne mit Arbeitswerten (unten als **AW** markiert), die den Fraktionsbeschreibungen folgen: Menschen blau, Zwerge Eis, Elfen grün, Gnome rot, Ghule violett, Trolle weiß-gold. Ich habe das System so gebaut, dass **keine Lesbarkeit an der Fraktionsfarbe hängt**. Wenn Hermes die AW durch die Werte aus 1.2 ersetzt, bleiben alle Pflichtkontraste gültig. Nur die Spalte „Fraktionsfarbe gegen Kachel“ in D3 muss neu gerechnet werden.

Arbeitswerte (AW) der Fraktionsflächen: Menschen #3F6FC4, Zwerge #9ACFE6, Elfen #5CB04E, Gnome #C8372B, Ghule #7E44A8, Trolle #EEE8D8.

---

## Teil A – Geländekacheln

### A1 Grundregeln für alle sieben Kacheln

- Master 64 × 64 px. Die Anzeige bei 22 bis 46 px ist eine Verkleinerung auf 34 bis 72 %.
- **Kein Detail kleiner als 8 px im Master.** Bei 22 px Anzeige bleiben davon etwa 3 px übrig, kleinere Details werden zu Rauschen.
- **Ruhige Fläche:** Die Helligkeit innerhalb der Kachel weicht höchstens etwa ±10 % vom Mittelwert ab. Eine Kachel ist Untergrund und kein Bild. Der Marker muss darauf auffallen, nicht das Gelände.
- **Nahtlos:** Die Kanten schließen links-rechts und oben-unten an. Kein Motiv darf die Kante schneiden, das nicht auf der Gegenseite weiterläuft. Keine Lichtrichtung, die an der Naht springt; das Licht kommt von oben-mittig und ist flach.
- Keine schwarzen Konturen. Formen trennen sich nur über Helligkeit.
- **Stilhinweis:** In Daniels Vorgaben zur Weltkarte steht „Bilderbuch, Comic-Tannen“, im Handbuch „stylized realism“. Bei 22 px Anzeige gewinnt ohnehin die vereinfachte Form. Die Prompts unten liegen deshalb bewusst zwischen beiden Stilen. **Welcher Stil gilt, entscheidet Daniel.**

### A3 Mittlere Füllfarben (ersetzen die heutigen)

| Gelände | heute | neu (Mittelwert) | Leitidee |
|---|---|---|---|
| Grasland | #64794A | **#86A84E** | helles Frühlingsgrün |
| Steppe | #A98A5C | **#CDB577** | Stroh/Weizen, hell |
| Wald | #2E4527 | **#3E6E44** | Tannengrün, kühl |
| Hügel | #6B563E | **#B0805A** | Terrakotta, warm |
| Berg | #8E93A6 | **#A7ADBD** | Fels, hellgrau-blau |
| Nebelsee | #41597A | **#4E89B0** | klares Blau |
| Sumpf | #474A34 | **#5E7A6A** | Graugrün, matt |

Unterscheidbarkeit (Farbabstand ΔE76): Das kleinste Paar ist Wald/Sumpf mit 19,1, danach Steppe/Hügel mit 22,9 und Berg/Nebelsee mit 25,3. Alle anderen Paare liegen über 29. Bei Wald/Sumpf trägt die Struktur zusätzlich: Tannenspitzen gegen flache Wasserflecken. Für die Legende genügt ΔE ≥ 15 bei einem 2-×-1-Zeichen-Quadrat; alle Paare erfüllen das.

Heute liegen vier Arten unter 3 : 1 gegen den Spielgrund #2A0605 (Wald 1,77, Sumpf 2,04, Nebelsee 2,60, Hügel 2,69). Mit der neuen Palette liegen **alle sieben über 3 : 1**; der kleinste Wert ist Wald mit 3,12. Damit verschwindet „alles braun“.

### A2 Prompts

**Stil-Block (für alle gleich):**

```
seamless tileable top-down terrain texture, 64x64 game map tile, painterly digital illustration, storybook stylized realism, soft even overhead light, low contrast within tile, large simple shapes, no outlines, flat orthographic view, edges wrap seamlessly on all four sides
```

**Negativ-Block (für alle gleich):**

```
no black outlines, no perspective, no horizon, no shadows cast across edges, no text, no logos, no people, no faces, no animals, no buildings, no blood, no 3D render, no photo, no vignette, no border, no high-frequency noise
```

| Kachel | Motiv-Block | Gelungen, wenn … |
|---|---|---|
| Grasland | `fresh spring meadow, soft grass clumps, a few tiny pale flower dots, average color #86A84E` | Bei 22 px liest es sich als gleichmäßiges helles Grün ohne Flecken. Mittelwert innerhalb ±8 je Kanal. |
| Steppe | `dry golden steppe grass, wind-combed strands in one direction, sparse pebbles, average color #CDB577` | Hellstes Feld der Karte, deutlich wärmer als Hügel, kein Sandwüsten-Eindruck. |
| Wald | `dense fir forest canopy from above, 3 to 4 rounded comic-style fir crowns per tile, cool green, average color #3E6E44` | Die Kronen sind bei 22 px als Knubbel erkennbar, nicht als Fläche. Kein Schwarz zwischen den Kronen, die Lücken sind dunkelgrün. |
| Hügel | `rolling terracotta hills, two gentle rounded mounds with lighter tops, warm earth, average color #B0805A` | Warm und rötlich, auf keinen Fall oliv. Neben Steppe klar dunkler und röter. |
| Berg | `grey-blue rocky mountain tops from above, faceted stone, small snow highlights, average color #A7ADBD` | Kühl, kantig, die Schnee-Lichter höchstens 10 % der Fläche. |
| Nebelsee | `calm clear lake surface from above with thin drifting mist wisps, gentle ripples, average color #4E89B0` | Eindeutig Wasser. Der Nebel bleibt Hauch und deckt höchstens 20 %. Das Feld liest sich als „nicht besetzbar“. |
| Sumpf | `marshy wetland from above, small dark-green pools, reed tufts, muted grey-green, average color #5E7A6A` | Matter und grauer als Wald, mit flachen Wasserflecken statt Kronen. |

**Hinweis zu Bildgeneratoren:** Sie halten 64 × 64 und echte Nahtlosigkeit selten ein. Empfehlung: in 512 × 512 erzeugen, mit einem Offset von 50 % prüfen und die Naht ausbessern, dann auf 64 verkleinern und den Mittelwert auf den Zielwert schieben.

---

## Teil B – Markersystem

**Grundprinzip (löst „erkenne kaum“ und den Kontrast zugleich):** Jeder Marker besteht aus drei Schichten.

1. **Halo:** ein Außenring in #2A0605. Er trennt den Marker vom Gelände; der Kontrast Halo gegen Kachel liegt bei mindestens 3,12.
2. **Rand:** in Creme #F2E6C8. Er trägt die **Umrissform**; Rand gegen Halo ergibt 15,02.
3. **Fläche:** in Fraktionsfarbe. Sie ist nur Zusatzinformation.

Die Erkennung läuft also über **Form plus Hell-Dunkel**, nie über Farbe allein. Außerdem darf der Marker **über sein Feld hinausragen** (Marker = Feld + 4 px), denn Daniels Kritik richtet sich gegen die Größe.

### B1 Drei Stufen

| Stufe | Feldbereich | Referenzfeld | Markerhöhe | Halo / Rand | Innenfläche | Was **weggelassen** wird |
|---|---|---|---|---|---|---|
| klein | 20–25 px | 22 | **26 px** (bei 20: 24) | 2 / 2 px | 18 px | Burgbild, Wappenmotiv, Name, Dorfstufe. Es bleiben Umriss und Fraktionsfläche. |
| mittel | 26–37 px | 30 | **34 px** | 2 / 2 px | 26 px, darin das Wappen als Creme-Silhouette in 14 px | Burgbild, Name |
| groß | 38–46 px | 46 | **50 px** (bei 42: 46) | 2 / 2 px | 42 px, darin eine Burgminiatur von 30 px; das Wappen sitzt als 16-px-Plakette an der Unterkante | Name. Er erscheint nur im Seitenpanel. |

**Offen und UNBEKANNT:** Können zwei Dörfer auf direkt benachbarten Feldern stehen? Bitte den Mindestabstand im Kartengenerator prüfen. Wenn ja, überlappen sich die Halos um 4 px. Das bleibt lesbar, aber das ausgewählte Dorf wird dann obenauf gezeichnet.

### B2 Umrisse der sechs Fraktionen (farbunabhängig)

- **Menschen** (Lilie): klassisches Wappenschild mit gerader Oberkante und Spitze unten.
- **Zwerge** (Schneeflocke): regelmäßiges Sechseck, wie eine Eisflocke.
- **Elfen** (Blatt/Baum): voller Kreis, wie eine Baumkrone von oben.
- **Gnome** (Löwe): Quadrat mit 2 px abgerundeten Ecken, eine gedrungene Festung.
- **Ghule** (Dreizack): Dreieck mit Spitze **oben**, wie eine Gabelzinke.
- **Trolle** (Sternburg): fünfzackiger Stern.

Die Formen sind so gewählt, dass keine zwei bei 18 px Innenfläche gleich aussehen. Am ähnlichsten sind Schild und Dreieck; beide sind spitz, aber an entgegengesetzten Enden.

### B3 Eigener Marker

- **Doppelrand:** gold #E0B040, 2 px, plus innen 1 px Halo und 1 px Gold.
- **+4 px größer** als ein Bot-Marker derselben Stufe.
- **Immer obenauf** gezeichnet.

Begründung: Gold gegen Creme hat nur 1,62. Deshalb trägt der Doppelring als **Formmerkmal** die Unterscheidung, das Gold ist Zusatz. Die Umrissform ist ohnehin einmalig, weil kein Bot die Spielerfraktion hat.

### B4 Zustände

- **Ausgewählt:** ein zusätzlicher Creme-Ring von 2 px außerhalb des Halos, darum noch 1 px Halo („Zielscheibe“). Bei 22 px wächst der Marker damit auf 32 px. Dazu kommt ein 2-px-Creme-Innenrahmen um das Feld.
- **Bedroht:** ein Dreieck-Abzeichen oben rechts, **8 px** (klein), 10 px (mittel) oder 12 px (groß). Füllung Orange #E8582A, 1 px Halo-Umriss. Orange gegen Halo ergibt 5,20. Das Merkmal ist die Dreiecksplakette, nicht die Farbe.

### B5 Marsch und Drache

- **Marschlinie:**
  - 3 px Creme mit je 1 px Halo-Ummantelung, zusammen also 5 px. Die Ummantelung gegen die Kachel liegt bei mindestens 3,12.
  - Spitze: ein gefülltes Dreieck von 10 px (klein) bis 14 px (groß).
  - Start: ein Quadrat von 6 px.
  - **Feindlicher Marsch auf eigene Dörfer:** Linie in Orange und **gestrichelt** (6 px an, 4 px aus). Die Strichelung ist das farbunabhängige Merkmal.
- **Drache:** eine **Raute** (auf die Spitze gestelltes Quadrat). Sie ist die einzige gekippte Form im System. Fläche Halo-dunkel, darin eine Creme-Flügelsilhouette (ab mittel).
- **Ruine:** dieselbe Raute mit grauer Fläche #8A8178 (gegen Halo 4,87). Bei mittel und groß zeigt sie eine eingestürzte Turmsilhouette.

### B6 Zwei Objekte auf einem Feld

- **Reihenfolge der Anzeige:** ausgewählt > eigenes Dorf > fremdes Dorf > Drache/Ruine > Marschziel.
- **Dorf und Drache:** Das Dorf wird gezeichnet, der Drache erscheint als Mini-Raute von 10 px unten links.
- **Dorf und Marschziel:** Die Pfeilspitze endet am Halo-Rand, und das Dorf trägt das Bedroht-Dreieck.
- **Klick:** Er wählt immer das oberste Objekt. Das Seitenpanel zeigt dann oben „Auf diesem Feld: Dorf X · Drache“ als umschaltbare Reiter. Es gibt kein Popup-Menü.

---

## Teil C – Layout

### C4 Entscheidung: Karte so groß, wie die Höhe erlaubt, Angaben rechts daneben

Die Höhe begrenzt die Karte, nicht die Breite. Bei 589 px Höhe passen 20 Felder zu **29 px** (Karte 580 × 580). Heute sind es 22 px. Das ist ein Plus von 32 % in der Kante und 74 % in der Fläche, und die Markerstufe springt von klein auf mittel. Mehr Breite bringt der Karte nichts. Deshalb nutzt die Seitenleiste den Rest.

**Der Preis:** Die linke Spalte mit den sechs Weltkarten entfällt in dieser Ansicht. Sie wird zu einer Reiterleiste „Welt 1–6“, ohne Vorschaubilder.

### C1 / C3 – 1037 × 589

| Bereich | Maß |
|---|---|
| Karte | x 0–580, y 4–584 (580 × 580; Rand oben 4 px, unten 5 px) |
| Abstand | 16 px |
| Seitenleiste | 441 × 589 |
| ↳ Kopfzeile (Welt-Reiter, Titel) | 40 px |
| ↳ Dorfdetails / Feldinhalt | 377 px |
| ↳ Legende (Titel 20 + 4 Zeilen × 22, zweispaltig) | 108 px |
| ↳ Fußzeile (Schaltfläche „Angriff planen“) | 48 px |
| ↳ Abstände | 2 × 8 px |
| Summe Seitenleiste | 40 + 8 + 377 + 8 + 108 + 48 = **589** |

### C2 – 691 px Breite

- Die Karte bleibt **580 × 580**, denn sie hat Vorrang.
- Daneben 8 px Abstand und eine **Symbolleiste von 103 px**: Welt wechseln, Legende, Angriff planen.
- **Was entfällt:** die dauerhafte Legende (sie öffnet sich auf Knopfdruck) und das dauerhafte Detailpanel.
- **Dorfdetails** öffnen sich beim Klick als Überlagerung von 300 px Breite auf der Kartenseite, die **dem gewählten Dorf gegenüberliegt**.
- **Preis:** Solange die Details offen sind, ist etwa die Hälfte der Karte verdeckt.

### Was nicht auf den Schirm darf

- Dorfnamen auf der Karte
- Koordinatenzahlen am Rand
- Scrollbalken an der Karte
- Weltkarten-Vorschaubilder in dieser Ansicht
- ein gemaltes Hintergrundbild hinter der Karte: Ein 1142 × 1120 großes T07-Bild wäre hier bis auf den Rand verdeckt. Der Rahmen ist schlicht #2A0605.
- Tooltips mit mehr als einer Zeile

**UNBEKANNT:** Die Inhaltshöhe bei 940 px Fensterhöhe. Bitte messen. Die Feldgröße folgt immer der Regel „abgerundet aus (Höhe − 9) / 20“.

### C5 Neuer Weg zum Angriff

1. Portal öffnen; die Karte ist sofort groß sichtbar.
2. Dorf auf der Karte anklicken; die Details erscheinen rechts.
3. „Angriff planen“ in der Fußzeile.

Damit ist es ein Schritt weniger als heute, weil die Dorfwahl direkt auf der Karte passiert.

---

## Teil D – Kontraste

### D2 Texte und Zeichen

Panel #3A1210 und Kopfzeile #2A0605 sind **AW**, bitte gegen Handbuch 1.2 abgleichen.

| Element | auf #2A0605 (Kopf, Kartenrand) | auf #3A1210 (Panel) |
|---|---|---|
| Text Creme #F2E6C8 | 15,02 | 13,29 |
| Text Sekundär #C9B48A | 9,21 | 8,15 |
| Text/Zeichen Gold #E0B040 | 9,28 | 8,21 |
| Warnung Orange #E8582A | 5,20 | 4,60 |
| Ruine Grau #8A8178 (Zeichen) | 4,87 | 4,31 |

Alle Texte liegen über 4,5. **Achtung Legende:** Ein Wald-Quadrat direkt auf dem Panel ergibt nur 2,76. Deshalb bekommt **jedes Legendenquadrat einen 1-px-Creme-Rahmen** (13,29 gegen Panel). Dann gilt der Rahmen als Zeichengrenze.

### D3 Kachel gegen Marker

| Kachel | Halo (trägt die Lesbarkeit) | Gold direkt | Creme direkt |
|---|---|---|---|
| Grasland | 6,86 | **1,35** | **2,19** |
| Steppe | 9,29 | **1,00** | **1,62** |
| Wald | 3,12 | **2,97** | 4,81 |
| Hügel | 5,40 | **1,72** | **2,78** |
| Berg | 8,30 | **1,12** | **1,81** |
| Nebelsee | 4,91 | **1,89** | 3,06 |
| Sumpf | 3,97 | **2,34** | 3,79 |

Fraktionsflächen direkt auf Kachel (mit AW-Farben):

| Kachel | Menschen | Zwerge | Elfen | Gnome | Ghule | Trolle |
|---|---|---|---|---|---|---|
| Grasland | 1,80 | 1,61 | 1,01 | 1,91 | 2,36 | 2,22 |
| Steppe | 2,45 | 1,19 | 1,35 | 2,59 | 3,19 | 1,64 |
| Wald | 1,22 | 3,54 | 2,21 | 1,15 | 1,07 | 4,88 |
| Hügel | 1,42 | 2,05 | 1,28 | 1,51 | 1,85 | 2,82 |
| Berg | 2,18 | 1,33 | 1,20 | 2,32 | 2,85 | 1,84 |
| Nebelsee | 1,29 | 2,25 | 1,41 | 1,37 | 1,69 | 3,11 |
| Sumpf | 1,04 | 2,78 | 1,74 | 1,11 | 1,36 | 3,84 |

Fast alle Werte liegen unter 3, das niedrigste Paar ist Elfen auf Grasland mit 1,01.

**Folgerung:** Gold und Fraktionsfarben dürfen **nie direkt auf eine Kachel**. Genau dafür ist der Halo da. Er liegt gegen alle sieben Kacheln bei mindestens 3,12.

Innerhalb des Markers liegen einige Fraktionsflächen unter 3 gegen ihren Nachbarn:

- gegen den Creme-Rand: Zwerge 1,36, Trolle 1,01, Elfen 2,18
- gegen den Halo: Ghule 2,91

Das ist zulässig, weil der **Umriss vom Creme-Rand gegen den Halo** (15,02) getragen wird. Die Fläche ist kein eigenständiges Zeichen.

---

## Teil E – Reihenfolge und Abnahme

### E1 Erster Durchgang (8 Motive)

- **1–7:** die sieben Geländekacheln, in der Reihenfolge Grasland, Wald, Nebelsee, Steppe, Hügel, Berg, Sumpf. Die häufigsten zuerst; die Häufigkeit ist UNBEKANNT, bitte im Generator zählen.
- **8:** ein Markerbogen mit sechs Umrissen × drei Stufen, dazu Spieler-Doppelring, Drache, Ruine, Bedroht-Dreieck und Marschpfeil. Die Marker sind **flache Formen, nicht generiert gemalt**, denn bei 18 px wird gemaltes Detail zu Matsch.

**Später:** Burgminiaturen für die Stufe groß (aus den vorhandenen Burgbildern), je zwei Kachelvarianten gegen Wiederholungsmuster und die Drachenflügel-Silhouette.

### E2 / E3 Abnahmekriterien

| # | Kriterium | Prüfung |
|---|---|---|
| 1 | Bei 22 px Feld sind alle sechs Fraktionsmarker in **Graustufen** paarweise unterscheidbar. | Auge: Bildschirmfoto entsättigen, eine zweite Person ordnet die Marker zu |
| 2 | Kein Text unter 4,5 : 1, kein Zeichen unter 3 : 1 gegen seinen direkten Grund. | Rechnung mit Pipette auf echten Pixeln |
| 3 | Der Halo jedes Markers liegt gegen jede Kachel bei mindestens 3,0. | Rechnung |
| 4 | Kachelkanten zeigen bei 3 × 3 gekachelter Anzeige keine sichtbare Naht. | Auge bei 100 % und 200 %, Testkarte nur aus einer Art |
| 5 | Der Kachelmittelwert weicht je Kanal höchstens ±8 vom Zielhex in A3 ab. | Messung (Durchschnittsfarbe des Masters) |
| 6 | Bei 900 px Fensterhöhe misst das Feld mindestens 29 px und die Karte mindestens 580 × 580. | Messung im Programm |
| 7 | Bedroht- und Ausgewählt-Zustand sind bei 22 px Feld auch in Graustufen erkennbar. | Auge, entsättigt |
| 8 | Der eigene Marker wird in einer Karte mit 7 Dörfern in unter 2 Sekunden gefunden. | Auge: Daniel mit Stoppuhr, 3 Durchläufe |
| 9 | Die Drachenraute wird von keinem Prüfer mit einem Fraktionsmarker verwechselt. | Auge, entsättigt, 2 Personen |
| 10 | Bei 691 px Breite bleibt die Karte 580 px breit, nichts scrollt waagerecht. | Messung im Programm |

---

**Für Hermes zum Nachrechnen:** Gerechnet wurde mit den Formeln nach WCAG 2.x (relative Leuchtdichte, sRGB-Linearisierung bei 0,04045) und ΔE76 in CIELAB mit D65.
