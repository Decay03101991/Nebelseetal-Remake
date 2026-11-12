# ANTWORT AUF AUFTRAG NR. 9: Die linke Spalte bei jeder Fenstergröße

| | |
|---|---|
| **Antwort auf** | AUFTRAG NR. 9 AN CLAUDE (Klasse Opus 5.5): DIE LINKE SPALTE BEI JEDER FENSTERGROESSE |
| **Auftragsdatei** | `AUFTRAG_CLAUDE_SPALTE_NR9.md` |
| **Auftrag von** | Hermes Agent „Weltenfresser“, Stand 12.11.2026, 19:4x |
| **Für** | Daniel Kössl |
| **Ort im Spiel** | Siedlungsansicht: Spalte links, Karte rechts (F-47) |
| **Vorgänger** | Antwort auf Auftrag Nr. 8; F-46, F-47 und F-48 gelten |
| **Erarbeitet** | von Opus 5.5 Thinking: Mittel, 12.11.2026 |
| **Umsetzbar für** | `deepseek-v4-flash`, nur Pillow und Tkinter |

**Abkürzungen:**
- **W × H**: sichtbare Fläche.
- **S**: Spaltenbreite.
- **f**: Feldgröße in px.
- **Karte** = 10 × f + 18.

---

## 0. Zwei Befunde vorab

1. **F-46 braucht einen Breitenterm.** Mit `min(64, (H − 18) // 10)` allein bliebe bei 615 × 565 eine Spalte von **41 px** (615 − 16 − 558) und bei 867 × 565 eine von 293 px. Darin passt die Bauauswahl (300 px) nicht.
   - **Vorschlag** (Daniel bestätigt bitte): f = min(64, (H − 18) // 10, (W − 350) // 10).
   - Die 350 ergeben sich aus 16 Abstand + 316 Mindestspalte (300 Bauauswahl + 2 × 8 Schleierabstand) + 18 Leiste.
   - Bei 1037 × 589 ändert das nichts, f bleibt 57.
2. **Der Ausschnitt in eurem E4 stimmt bei anderen Breiten nicht.** Der Wert 52 gilt nur für W = 1037. Allgemein ist links = (1142 − W) // 2. Bei W = 1151 ist das **−5** (abgerundet): Dann fehlen links 5 px und rechts 4 px Bild, gefüllt mit #17212B.

---

## Die vier Flächen auf einen Blick

| Fläche | f | Karte | Anordnung | S | Dorfübersicht | Spalte rollt? |
|---|---|---|---|---|---|---|
| 1151 × 785 | 64 | 658 | nebeneinander | **477** | 1 Zeile | nein (772 ≤ 785) |
| 1037 × 589 | 57 | 588 | nebeneinander | **433** | 2 Zeilen | ja, um 267 px (856 − 589) |
| 867 × 565 | **51** | 528 | nebeneinander | **323** | 2 Zeilen | ja, um 291 px |
| 615 × 565 | 54 | 558 | **übereinander** | 615 | 1 Zeile | der ganze Inhalt rollt, um 781 px |

**Regel für die Anordnung:**
- **Nebeneinander**, solange f nach der Formel aus Befund 1 **mindestens 50** ist.
- **Sonst übereinander:** Die Karte steht oben, rechtsbündig bei x = W − Karte. Die Spalte steht darunter in voller Breite. Hier gilt f = min(64, (H − 18) // 10, (W − 18) // 10).
- Der Wert 50 ist ein Startwert. Er sorgt dafür, dass das historische Kartenbild höchstens auf 78 % verkleinert wird.

---

## A) Die Dorfübersicht

**Ein Weg: Umbruch, nichts kürzen.**

- **Inhaltsbreite** = S − 16 (8 px Schleierabstand links und rechts).
- **Einzeilig**, wenn die Inhaltsbreite ≥ 428 ist. Das trifft nur bei S = 477 zu (461 px).
- **Sonst zweizeilig:**
  - Die Tabellenspalten werden geteilt: Spalte 1 bis ⌈n/2⌉ kommen in Zeile 1, der Rest in Zeile 2. Das gilt **für jedes Dorf**.
  - Die Tabelle wird dann 2 × 80 + 4 = **164 px hoch**, der ganze Block **324 px** statt 240.
  - Die Halbzeilen sind etwa 214 px breit. Sie passen also auch bei S = 323 (Inhalt 307).

**Bei S = 433 fehlen nur 11 px** (417 statt 428). Kürzen wäre hier verlockend, aber welche Spalte zuerst fällt, hängt vom Inhalt ab.

**UNBEKANNT:** n und die Breite jeder Tabellenspalte. Bitte die Spaltenliste mit Breiten nennen.
- Ist eine einzelne Halbzeile breiter als 307 px, gilt der Umbruch bei S = 323 nicht.
- Mit der Liste kann ich auch sagen, ob bei S = 433 das Kürzen einer Spalte besser ist als zwei Zeilen.

**Pflichtangaben:** Ich empfehle **alle Spalten als Pflicht**. Deshalb bricht die Tabelle um und kürzt nicht. Welche Spalten es gibt, ist UNBEKANNT (siehe oben).

---

## B) Das Rollen der Spalte

**Höhe der Spalte (gerechnet):**
- Blöcke: 652 px.
- 5 Schleierblöcke × 16 px Innenabstand = 80 px.
- 5 Lücken zwischen den 6 Blöcken × 8 px, in denen das Bild sichtbar bleibt = 40 px.
- Summe **772 px**, mit zweizeiliger Dorfübersicht **856 px**.

**Wann sie rollt:** sobald diese Höhe größer als H ist. Siehe die Tabelle oben.
- Bei 1151 × 785 rollt nichts, es bleiben 13 px frei.
- Bei allen anderen Flächen rollt die Spalte.

**Rollbalken:** **im 16-px-Abstand zwischen Spalte und Karte.** Die Spalte verliert dadurch keine Breite.
- Ist der Tkinter-Rollbalken bei 125 % breiter als 16 px (**UNBEKANNT**, bitte `winfo_width` messen), wird der Abstand so breit wie der Rollbalken. Diese Breite ersetzt dann die 16 in allen Formeln.
- Rollt nichts, wird der Rollbalken ausgeblendet. Der Abstand bleibt.

**Legende:** **Sie bleibt unten kleben.** Sie erklärt die Karte und wird bei jeder Bauentscheidung gebraucht.
- Legende und Erklärzeile bilden einen Schleierblock von 42 + 16 = **58 px** am unteren Rand der Spalte.
- Darüber rollt der Rest in einer Fläche von H − 58 − 8 px.
- Bei der Anordnung **übereinander** steht die Legende direkt unter der Karte und rollt mit. Dort rollt ohnehin alles.

**Hintergrund beim Rollen** (wichtig für flash). Der Schleier wird mit Pillow ins Bild eingerechnet; Tkinter kann keine Halbtransparenz. Würde nur der Text rollen, müsste das Bild bei jedem Rollschritt neu gerechnet werden. Deshalb:
- **Das Panorama liegt im rollenden Bereich der Spalte und rollt mit ihr.** Es wird einmal je Fenstergröße gerechnet.
- Neben der Karte steht kein Bild. Der Abstand und der Platz unter der Karte sind #1a0a09. Bei 1151 × 785 sind das 127 px unter der Karte.

---

## C) Das Panorama bei jeder Fläche

**Ausschnitt für die Spalte:**
- links = (1142 − W) // 2, Breite S.
- oben = (1120 − Hs) // 2, wobei **Hs = max(H, Spaltenhöhe)**.
- Bei der Anordnung **übereinander**: Hs = gesamte Inhaltshöhe = Karte + 16 + Spalte.

| Fläche | links | Hs | oben | Füllung #17212B |
|---|---|---|---|---|
| 1151 × 785 | −5 | 785 | 167 | 5 px links (rechts liegt die Karte) |
| 1037 × 589 | 52 | 856 | 132 | – |
| 867 × 565 | 137 | 856 | 132 | – |
| 615 × 565 | 263 | 1346 | −113 | je 113 px oben und unten |

**Das ersetzt E4 des Auftrags:** Der Ausschnitt hängt jetzt von Hs ab und nicht von H, weil das Bild mit der Spalte rollt (Regel aus Nr. 8).

**Ist der Bereich größer als das Bild** (H > 1120 oder Hs > 1120): **So lassen**, also Bild mittig und Rest #17212B, wie Daniel es in Register 502 entschieden hat.

**Mindestgröße des Fensters:** **1024 × 720**, gesetzt mit `minsize`.
- Diese Zahl steht schon als Untergrenze in eurer Fensterrechnung, sie ist also nicht neu.
- Daraus folgt eine sichtbare Fläche von mindestens 615 × 565, f mindestens 54 (übereinander) und eine ganz sichtbare Karte.
- **Ein Feld von 22 px ist nicht spielbar.** Bei genau dieser Größe kam Daniels Befund „erkenne kaum die Dörfer“.
- **Grenze:** Die Abzüge von 409 und 155 px sind gemessen. Ändern sich die Menüspalten oder der Kopf, muss die Mindestgröße neu geprüft werden.

---

## D) Schleier je Block

| # | Block | Schleier? | Grund |
|---|---|---|---|
| 1 | Titel und Name | **ja** | Text direkt auf dem Bild |
| 2 | Ortsbestand | **nein** | eigene deckende Fläche #1B2A2F, siehe unten |
| 3 | Bauauswahl | **ja** | Ob sie eine eigene Fläche hat, ist UNBEKANNT. Hat sie eine deckende, dann nein. |
| 4 | Dorfübersicht | **ja** | |
| 5 + 6 | Legendenzeile und Erklärzeile | **ja, als ein gemeinsamer Block** | spart 16 px. Die Farbfelder bekommen einen Rahmen von 1 px in #F2E3BF, wie in T07. |
| 7 | Zusätze | **ja** | |
| 8 | Koordinatenleiste | **nein** | gehört zur Karte, deckend #1a0a09 (Nr. 8) |

**Ortsbestand:** Seine eigene Fläche reicht. Ein zusätzlicher Schleier liegt **unter** der deckenden Fläche und ändert nichts. Gerechnet:

| Farbe | auf #1B2A2F (eigene Fläche) | auf Schleier, schlimmster Fall #483b3a |
|---|---|---|
| #7FD1FF (Rahmen/Text) | **8,79** | 6,35 |
| #F3F4F6 (Text) | **13,45** | 9,72 |

Beide halten auf jeder Fläche 4,5 : 1.

**Nur sichtbar ohne Schleier:** Der Rahmen #7FD1FF liegt gegen reines Weiß unter dem Bild bei 1,68. Das ist unkritisch, denn der Rahmen trennt nur. Die Kante wird von der dunklen Fläche getragen (#1B2A2F gegen Weiß: 14,80).

---

## E) Abnahme

| # | Kriterium | Prüfweg |
|---|---|---|
| 1 | Bei allen vier Flächen gelten f, Karte, S und Anordnung wie in der Tabelle; die Karte ist ganz sichtbar (bei „übereinander“ in Rollstellung 0) | Messung |
| 2 | Die Dorfübersicht zeigt bei S = 433 alle Spalten, zweizeilig, und keine Zelle ist abgeschnitten | Messung und Auge |
| 3 | Jeder Textblock außer Ortsbestand und Koordinatenleiste liegt auf einem Schleier von 80 %; Text ≥ 4,5, Rahmen ≥ 3 | Rechnung je Blockfarbe gegen #483b3a |
| 4 | Ausschnitt = ((1142 − W) // 2, (1120 − Hs) // 2), kein Pixel skaliert | Messung, Stichpixel |
| 5 | Das Fenster lässt sich nicht kleiner als 1024 × 720 ziehen | `winfo_width/height` nach Ziehen |
| 6 | Die Legende bleibt beim Rollen der Spalte an ihrer y-Position | Messung vor und nach dem Rollen |
| 7 | Das Bild rollt mit der Spalte: nach 100 px Rollen steht dasselbe Bildpixel 100 px höher | Messung |

---

## Was ich nicht geprüft habe

- **Tabelle der Dorfübersicht:** n und die Spaltenbreiten. Davon hängt ab, ob der Umbruch bei S = 323 passt.
- **Rollbalken:** seine Breite bei 125 %.
- **Bauauswahl:** ob sie eine eigene deckende Fläche hat.
- **Startwert 50:** Ob die Schwelle für „nebeneinander“ und die Verkleinerung des Kartenbildes auf 510 px (bei f = 51) gut aussehen, muss Daniel mit dem Auge prüfen.
- **Abzüge:** Ob 409 und 155 px bei allen vier Bildschirmen gleich sind. Ihr habt sie an einem Rechner gemessen.
- **Abstände zwischen den Blöcken:** Ob die 652 px schon Abstände enthalten. Ich habe angenommen, dass nicht. Wenn doch, sinken die Spaltenhöhen um bis zu 40 px.

---

Ende der Antwort auf Auftrag Nr. 9.
