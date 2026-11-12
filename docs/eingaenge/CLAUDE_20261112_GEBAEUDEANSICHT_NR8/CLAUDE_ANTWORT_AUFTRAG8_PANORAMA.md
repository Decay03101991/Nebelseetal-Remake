# ANTWORT AUF AUFTRAG NR. 8: Das Panorama hinter einer 10 × 10-Karte

| | |
|---|---|
| **Antwort auf** | AUFTRAG NR. 8 AN CLAUDE (Klasse Opus 5.5): DAS PANORAMA HINTER EINER 10 x 10-KARTE |
| **Auftragsdatei** | `AUFTRAG_CLAUDE_GEBAEUDEANSICHT_NR8.md` |
| **Auftrag von** | Hermes Agent „Weltenfresser“, Stand 12.11.2026, 19:0x |
| **Für** | Daniel Kössl |
| **Ort im Spiel** | Siedlungsansicht (Siedlungskarte 10 × 10 mit Völker-Panorama) |
| **Vorgänger** | Antwort auf Auftrag Nr. 7; deren Teil B ist hiermit **ersetzt** |
| **Erarbeitet** | von Opus 5.5 Thinking: Mittel, 12.11.2026 |
| **Umsetzbar für** | `deepseek-v4-flash`, nur Pillow und Tkinter |

Die Berichtigung ist angekommen; Teil B aus Antwort Nr. 7 ist gestrichen.

Die Reihenfolge ist hier **B vor A**, weil die Antwort auf B die Frage A fast vollständig auflöst.

---

## B) Die Karte: 57 px je Feld, nie rollen

**Entscheidung:** Feldgröße = **min(64, abgerundet aus (H − 18) / 10)**, wobei H die sichtbare Inhaltshöhe ist.

- Bei H = 589 ergibt das **57 px**. Die Karte ist dann 10 × 57 + 18 = **588 × 588** und steht ganz im Bild, bei y = 0 bis 588.
- Größere Fenster bekommen bis zu 64 px, also das Original. Größer wird das Feld nie.

**Begründung:**
- Wer baut und abreißt, muss **alle 100 Felder mit ihrer Geländeart gleichzeitig sehen**, um zu planen. Eine unterste Reihe, die man erst durch Rollen erreicht, ist bei jeder Bauentscheidung ein Hindernis.
- 57 px sind **2,6-mal so groß wie das Weltkartenfeld (22 px)**. Daniels Beschwerde „erkenne kaum die Dörfer“ betraf die Weltkarte, nicht diese Karte.
- **Preis:** Die Feldkante wird 11 % kleiner (Fläche −21 %).

**Wichtige Voraussetzung, UNBEKANNT:** Werden Gelände- und Gebäudegrafik der Siedlungskarte gezeichnet oder als Bitmap in 64 px geladen?
- **Gezeichnet:** 57 px kostet nichts.
- **Bitmap:** Sie wird einmal mit LANCZOS von 64 auf 57 verkleinert. Das ist zulässig, denn die Regel „nie skalieren“ (Register 502) gilt für die Hintergrundbilder. **Daniel bestätigt bitte**, dass sie für Kartenkacheln nicht gilt.
- **Lehnt `originalkarten.py` jede Feldgröße außer 64 ab** (nicht nur andere Rastergrößen), gilt der Rückfall: **64 px**, Karte 658 und **benanntes Rollen von 69 px**. Für diesen Fall gilt A2.

**Wohin die 216 px Texte und die 46 px darunter gehen:** Sie wandern in eine **rechte Spalte**. Über und unter der Karte steht nichts mehr.

| Bereich | Maß (bei 1037 × 589) |
|---|---|
| Karte | x 0 bis 588, y 0 bis 588 |
| Abstand | 16 px |
| rechte Spalte | **433 × 589**, x 604 bis 1037 |

Inhalt der rechten Spalte, von oben nach unten:
1. Titel und Name in einer Zeile (38 px).
2. Ortsbestand (57 px).
3. Bauauswahl (bisher 300 px breit; jetzt hat sie 433 px).
4. Dorfübersicht.
5. Legende mit Erklärzeile (42 px), am unteren Rand.

Die Zeilen „Hinweis“, „Reichsvergleich“ und „Vorteil“ (zusammen 57 px und Abstände) kommen ans Ende der Spalte.

**Nur die Spalte darf rollen, die Karte nie.** Wie hoch die Bauauswahl ist, ist **UNBEKANNT**. Bitte messen. Erst damit steht fest, ob die Spalte überhaupt rollen muss.

---

## A) Welche Fläche das Bild deckt

**Regel: Das Bild deckt immer den ganzen Inhalt und rollt mit ihm.** Es steht nie still.

- **Ausschnitt:** links = abgerundet aus (1142 − 1037) / 2 = **52**, oben = abgerundet aus (1120 − Hc) / 2, wobei **Hc die Inhaltshöhe** ist.
- **A1 (Empfehlung aus B):** Hc = H = 589, also Ausschnitt **(52, 265)**. Das ist genau der schon gebaute Ausschnitt, und es rollt nichts. Die Frage aus dem Auftrag stellt sich damit nicht mehr.
- **A2 (Rückfall mit 64 px):** Hc = 938, also Ausschnitt **(52, 91)**.
  - Sichtbar ist dann das **ganze gemalte Original (864 von 864 Zeilen)** plus je 37 px Ergänzungsband oben und unten.
  - Diese Bandzeilen liegen 1 bis 37 px von der Naht entfernt, also in der Haltezone und im inneren Verlauf, nicht im dunklen Außenteil.
  - **Vertretbar: ja.** Das Band ist dafür gebaut.

**Ein still stehendes Bild ist falsch.** Begründung:
1. **Es rutscht unter der Karte weg.** Beim Rollen ändert sich der Ausschnitt in den Lücken neben der Karte. Das sieht wie ein Fehler aus, nicht wie eine Tiefenwirkung.
2. **Tkinter verschiebt das Bild bereits mit.** Liegt es als erstes Element im rollenden Inhalt, wandert es von selbst mit. Ein stehendes Bild müsste bei jedem Rollschritt neu gesetzt werden. Das ist ein zusätzlicher Arbeitsschritt und eine zusätzliche Fehlerquelle für flash.

**Befund, den Daniel kennen sollte:** Die Karte ist deckend, weil alle 100 Felder ein Gelände tragen, und belegt 57 % der Breite.

Nach der Regel aus Auftrag 6 (x0 = cx − 661) steht das Wahrzeichen im 1142er-Bild bei **x = 661**, im Inhalt also bei 661 − 52 = **609**. Die Kartenkante liegt bei 588, die Spalte beginnt bei 604. **Das Wahrzeichen wird damit von der Kartenkante zerschnitten:** Die linke Hälfte liegt unter der Karte, die rechte Hälfte steht im oberen Teil der Spalte.

Wurde x0 bei einem Bild auf 0 begrenzt (cx < 661), liegt das Wahrzeichen weiter links und ganz unter der Karte. Welche Bilder das betrifft, zeigt die cx-Liste aus Auftrag 6.

**Ausweg ohne Bruch der Regel „mittig, nie skalieren“:** Die **Karte rechts** anordnen und die Spalte links. Dann gilt:
- Spalte x 0 bis 433, Abstand 16 px, Karte x 449 bis 1037.
- Das Wahrzeichen bei 609 liegt dann **ganz unter der Karte**. Das ist besser als zerschnitten, aber nicht sichtbar.

In beiden Anordnungen ist das Panorama hier also **Rahmen und Stimmung, kein Motiv**. **Empfehlung: Karte rechts**, weil ein zerschnittenes Wahrzeichen schlechter aussieht als ein verdecktes. Daniel entscheidet. Für diesen Fall tauschen in B und D alle x-Angaben: Spalte x 0 bis 433, Karte ab x 449; Ausschlussgrund 3 prüft dann die **linke** Kartenkante bei x 449.

Wenn Daniel das Motiv sehen will, empfehle ich **einen Schalter „Panorama“** in der Spalte. Er blendet Karte und Spalte aus und zeigt den 1:1-Ausschnitt ohne Schleier, bis zum nächsten Klick. Der Preis ist ein Knopf; es braucht keine neue Fläche.

---

## Schleier hinter den Texten (zu Kriterium E5)

Die Texte der rechten Spalte liegen auf dem Bild. Deshalb bekommt jeder **Textblock** ein eigenes Schleierfeld:
- **#1a0a09 mit 80 % Deckung**, 8 px Innenabstand um den Block.
- **Zwischen den Blöcken bleibt das Bild ohne Schleier**, damit es nicht verschwindet.
- In Pillow einmal je Neuschnitt in den Ausschnitt einrechnen (`Image.composite`). Tkinter kann keine Halbtransparenz.

Gerechnet gegen den **schlimmsten Fall reines Weiß** unter dem Schleier (Ergebnis #483b3a, Leuchtdichte 0,0481):

| Element | Kontrast | Pflicht |
|---|---|---|
| Text #F2E3BF | 8,42 | 4,5 ✓ |
| Gold #FFCC33 | 7,10 | 4,5 ✓ |
| Erfolg #a5d67a | 6,37 | 4,5 ✓ |
| Warnung #ff8a70 | 4,65 | 4,5 ✓ |
| Rahmen/Zeichen #b8862e | 3,31 | 3 ✓ |

**Untergrenze 80 %:** Bei 75 % fiele Warnung auf 3,87 und Rahmen auf 2,75. Die genauen Mindestdeckungen sind 79 % für Warnung und 78 % für Rahmen.

**Koordinatenleiste der Karte (18 px):** Sie ist deckend in #1a0a09, gehört also zur Karte. Text darauf hat 15,13.

---

## C) Wappen: bestätigt, mit einer Ergänzung

| Platz | Entscheidung |
|---|---|
| Kopf | **64 px, bestätigt.** Ergänzung: Hintergrund ist #1a0a09, und dunkle Wappenteile könnten darin verschwinden. **Prüfung:** Mindestens 90 % der äußersten deckenden Wappenpixel liegen bei ≥ 3 : 1 gegen #1a0a09. Wenn nicht, bekommt das Wappen **nur den Creme-Ring von 2 px** (15,13 gegen den Kopf). Die 90 % sind ein Startwert. |
| Einzelansicht | 128 px mit Doppelring, **bestätigt**. |
| Dorfmarker Weltkarte | flache Silhouette 14 bis 16 px, **bestätigt**. |
| Panorama der Siedlungsansicht | **Nein, kein Wappen.** Es steht schon im Kopf, und Karte plus Spalte nutzen die Fläche ganz. Ein zweites Wappen zeigt nichts Neues. |

---

## D) Drei Ausschlussgründe für diese Lage

Gemessen wird nur, was sichtbar ist: der **Spaltenbereich**. Bei A1 mit der Karte links ist das Bild-x 656 bis 1089, mit der Karte rechts (Empfehlung) Bild-x 52 bis 485; in beiden Fällen Bild-y 265 bis 854. Die Karte ist deckend und wird nicht gemessen.

1. **Zu unruhig hinter der Spalte:** Die Laplace-Varianz im Spaltenbereich liegt über dem **1,5-Fachen des Medians** der sechs Panoramen. Dann flimmern die Lücken zwischen den Schleierfeldern neben ruhigen Textblöcken. Faktor 1,5 ist ein Startwert.
2. **Zu hell in den Lücken:** Der mittlere Grauwert im Spaltenbereich liegt über **170**. Dann blenden die schleierfreien Lücken neben den 80-%-Feldern; die Spalte wirkt wie ein Streifenmuster. Startwert 170.
3. **Angeschnittene Figur am Kartenrand:** Eine Figur, ein Tier oder ein Gesicht wird von der rechten Kartenkante (Inhalts-x 588) zerschnitten. Prüfung mit dem Auge (Daniel), an einem Bildschirmfoto der Ansicht.

Weiterhin gilt der Ausschluss aus den bisherigen Regeln: kein Text, keine Logos, kein Blut, keine Gesichter im Vordergrund.

---

## E) Abnahme

| # | Kriterium | Prüfweg |
|---|---|---|
| 1 | Jedes sichtbare Bildpixel entspricht dem Quellpixel am Ausschnitt (52, oben); außerhalb der Schleierfelder ist es unverändert | Messung: 5 Stichpixel außerhalb, 5 innerhalb (innerhalb = 0,8 × #1a0a09 + 0,2 × Quelle, ±1) |
| 2 | Bei H = 589 ist die Karte 588 × 588 und ganz sichtbar, die Inhaltshöhe ist 589, nichts rollt außer der Spalte | Messung: Kartenunterkante ≤ H |
| 2b | Rückfall 64 px: Rollen genau 938 − 589 = 349 px, im Register als beabsichtigt benannt | Messung |
| 3 | Kein Text und kein Bedienelement im Bild | Sicht, 6 Panoramen (erledigt) |
| 4 | Wappen 64 und 128 px erkennbar; Kopf-Wappen ≥ 90 % Randpixel bei ≥ 3 : 1 oder mit Creme-Ring | Auge (Daniel) und Rechnung |
| 5 | Jeder Text liegt auf einem Schleierfeld (≥ 80 %), zwischen den Feldern ist das Bild sichtbar | Messung der Schleierfelder; Sicht |
| 6 | Das Bild rollt mit dem Inhalt: Nach 100 px Rollen ist dasselbe Bildpixel 100 px weiter oben | Messung |
| 7 | Keines der 6 Panoramen fällt unter Ausschlussgrund 1 bis 3 | wie in D |

---

## Was ich nicht geprüft habe

- **Karte:** Ob `originalkarten.py` nur die Rastergröße festlegt oder auch die Feldgröße von 64 px. Davon hängt ab, ob B gilt oder der Rückfall A2.
- **Kacheln:** Ob die Gelände- und Gebäudekacheln gezeichnet oder als Bitmaps geladen werden, und ob sie bei 57 px noch gut aussehen (Auge, Daniel).
- **Spalte:** Die Höhe der Bauauswahl und der Dorfübersicht, also ob die rechte Spalte rollen muss.
- **Wahrzeichen:** Wo das Wahrzeichen in den sechs Panoramen genau liegt (cx-Liste). Der Befund „bei x = 609, zerschnitten“ gilt nur für Bilder, bei denen x0 nicht auf 0 oder 394 begrenzt wurde. Die Breite des Wahrzeichens ist UNBEKANNT.
- **Startwerte:** Die Werte 1,5, 170 und 90 % sind Startwerte und nicht an euren Bildern geprüft.
- **Schleier:** Er ist für reines Weiß berechnet. Die tatsächlichen Werte über den sechs Panoramen liegen höher, wurden aber nicht gemessen.

---

Ende der Antwort auf Auftrag Nr. 8.
