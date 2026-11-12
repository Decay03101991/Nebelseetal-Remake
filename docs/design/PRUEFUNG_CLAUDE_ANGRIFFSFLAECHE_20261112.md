# Prüfung: Claudes Antwort auf Auftrag Nr. 4 (Angriffsfläche T07)

**Gegenstand:** `Claude_Opus_5.5_Antwort.md`, 16.812 Byte, Stand 12.11.2026 (Daniels Abo-Lauf im Browser).
**Geprüft:** 12.11.2026, 11:0x, von Hermes (Weltenfresser). **Verfahren:** eigene Rechnung, kein Modell.
**Gerechnet mit:** WCAG 2.x (relative Leuchtdichte, sRGB-Linearisierung bei 0,04045) und ΔE76 in CIELAB (D65) —
dieselben Formeln, die er selbst nennt. Skript: `scratch/pruefung_claude4.py`, Ausgabe unten zusammengefasst.

## 1. Ergebnis in einer Zeile

**75 von 75 Kontrastwerten stimmen** (Abweichung über 0,05: **0**), **drei ΔE-Werte exakt**, **vier Layout-Rechnungen
exakt**, **sechs Marker-Maße exakt**. Seine Kernbegründung trägt: Gold und Fraktionsfarben dürfen nicht direkt
auf eine Kachel, der Halo trägt die Lesbarkeit.

## 2. Kontraste (75 Werte, alle nachgerechnet)

| Gruppe | Werte | Ergebnis |
|---|---|---|
| D2 Texte/Zeichen gegen Grund #2A0605 und Panel #3A1210 | 10 | alle exakt (Creme 15,02 / 13,29; Gold 9,28 / 8,21; Orange 5,20 / 4,60; Ruine 4,87 / 4,31; Sekundär 9,21 / 8,15) |
| Rand Creme gegen Halo, Gold gegen Creme | 2 | exakt (15,02 und 1,62) |
| D3 Halo / Gold / Creme gegen die sieben neuen Kacheln | 21 | alle exakt, u. a. Halo gegen Wald **3,12** (der schwächste Wert im ganzen System) |
| Fraktionsflächen mit seinen Arbeitswerten (AW) gegen die sieben Kacheln | 42 | alle exakt, schwächstes Paar Elfen auf Grasland **1,01** |
| Summe | **75** | **75 richtig, 0 falsch** |

## 3. Farbabstände (ΔE76) — exakt

Gemessen: Wald/Sumpf **19,1** · Steppe/Hügel **22,9** · Berg/Nebelsee **25,3**, das nächste Paar Grasland/Steppe
**29,2**, danach über 30. Seine Aussage „alle anderen Paare über 29" stimmt.

## 4. Die Palette

**Seine Behauptung über die alte Palette stimmt genau:** gegen den Spielgrund #2a0605 liegen heute vier Arten
unter 3 zu 1 — Wald **1,77**, Sumpf **2,04**, Nebelsee **2,60**, Hügel **2,69**; die drei anderen liegen darüber
(Grasland 3,88, Steppe 5,75, Berg 6,10).

**Mit seiner neuen Palette liegen alle sieben über 3 zu 1**, der kleinste ist Wald mit **3,12**:

| Gelände | heute | neu | gegen #2a0605 heute → neu |
|---|---|---|---|
| Grasland | #64794A | #86A84E | 3,88 → 6,86 |
| Steppe | #A98A5C | #CDB577 | 5,75 → 9,29 |
| Wald | #2E4527 | #3E6E44 | 1,77 → **3,12** |
| Hügel | #6B563E | #B0805A | 2,69 → 5,40 |
| Berg | #8E93A6 | #A7ADBD | 6,10 → 8,30 |
| Nebelsee | #41597A | #4E89B0 | 2,60 → 4,91 |
| Sumpf | #474A34 | #5E7A6A | 2,04 → 3,97 |

Damit ist „alles braun" nicht nur behauptet, sondern **an Zahlen belegt und mit Zahlen beantwortet**.

## 5. Layout und Marker-Maße (nachgerechnet, alle exakt)

- Seitenleiste 40 + 8 + 377 + 8 + 108 + 48 = **589** ✓ (genau die gemessene Inhaltshöhe)
- Feldgröße aus (589 − 9) / 20 = **29,0** → abgerundet **29 px**, Karte **580 × 580** ✓
- Gewinn gegen heute: Kante **+31,8 %**, Fläche **+73,8 %** (er sagt „32 % / 74 %") ✓
- Schmales Fenster: 580 + 8 + 103 = **691** ✓ (genau die gemessene schmale Inhaltsbreite)
- Marker = Feld + 4 px: 22 → 26, 30 → 34, 42 → 46, 46 → 50 ✓
- Innenfläche bei Halo 2 px + Rand 2 px je Seite: 26 → 18, 34 → 26, 50 → 42 ✓ (je Seite 4 px abgezogen)

## 6. Sein Vorbehalt zur Palette — geprüft und bestätigt

Er sagt: er hatte das Handbuch nicht, rechnet mit Arbeitswerten (AW) und behauptet, **keine Lesbarkeit hänge an
der Fraktionsfarbe**; nur die Spalte „Fraktionsfarbe gegen Kachel" müsse neu gerechnet werden. **Das stimmt.**

Mit den echten **Akzentfarben aus Teil 1.2 des Handbuchs** (Menschen #e8667a, Zwerge #9fb3c8, Elfen #7fcf8f,
Trolle #c39bea, Ghule #7fb2ea, Gnome #ff6b6b):

| Fraktion | gegen Creme-Rand | gegen Halo | schlechteste Kachel |
|---|---|---|---|
| Menschen | 2,56 | 5,87 | Hügel 1,09 |
| Zwerge | 1,74 | 8,66 | Berg 1,04 |
| Elfen | 1,51 | 9,96 | Steppe 1,07 |
| Trolle | 1,84 | 8,16 | Berg 1,02 |
| Ghule | 1,79 | 8,40 | Berg 1,01 |
| Gnome | 2,24 | 6,72 | Grasland 1,02 |

Die Fraktionsfläche fällt damit **noch tiefer** als mit seinen AW (bis 1,01 gegen eine Kachel), aber die
**Pflichtkontraste bleiben unberührt**: Halo gegen jede Kachel ≥ **3,12**, Creme-Rand gegen Halo **15,02**.
Sein System ist also tatsächlich palettenfest — weil die Fläche kein eigenes Zeichen ist. Wer das später
„schöner" machen will, indem er die Fläche zum Merkmal macht, bricht genau diese Zusage.

## 7. Seine drei UNBEKANNT — hier beantwortet

1. **„Können zwei Dörfer auf benachbarten Feldern stehen?"** — **Ja.** Die Lage eines Bot-Dorfs kommt aus
   einem festen Streuwert (Name + Nummer), es gibt **keinen Mindestabstand**; zwei Dörfer können benachbart
   sein, und zwei Dörfer können sogar auf **demselben Feld** landen (dann gewinnt die Anzeige-Regel B6).
   Gemessen am 12.11.2026: 20 geprüfte Lagen, 0 Doppelbelegungen, aber ohne Garantie.
2. **„Die Inhaltshöhe bei 940 px Fensterhöhe"** — **589 px** (gemessen im laufenden Fenster, 12.11.2026).
   Damit ist sein 29-px-Feld die richtige Rechnung.
3. **„Häufigkeit der Geländearten"** — gemessen aus den Spieldaten (Anteil der 400 Felder):
   **Grasland 20, Steppe 20, Wald 18, Hügel 13, Berg 12, Sumpf 10, Nebelsee 7** Prozent.
   Seine Reihenfolge (Grasland, Wald, Nebelsee, Steppe …) ist damit **nicht** die richtige: die häufigsten
   sind Grasland und Steppe, der Nebelsee ist mit 7 % der **seltenste**.

## 8. Was Daniel entscheiden muss, bevor gebaut wird

1. **Burg oder flache Form?** Sein System lässt bei kleinen Feldern das gemalte Burgbild **weg** (Stufe klein:
   nur Umriss + Fraktionsfläche). Das ist ein Bruch mit den heute gelieferten Burgen und Wappen aus
   `data/bot_wappen.json` — die blieben dann nur für die Stufe „groß".
2. **Die sechs Weltkarten fallen weg.** Sein Layout opfert die linke Spalte (heute sechs Vorschaukarten) für
   eine Reiterleiste „Welt 1–6". Preis: keine Vorschau mehr, dafür 580 statt 440 px Karte.
3. **Im schmalen Fenster (691 px)** öffnen sich die Dorfdetails als Überlagerung und verdecken die halbe Karte.

## 9. Was ich NICHT geprüft habe (ehrlich)

- Seine Aussage über Bildgeneratoren („halten 64 × 64 und Nahtlosigkeit selten ein") — **nicht geprüft**, das
  ist Erfahrungswissen und für uns nicht nachrechenbar.
- Ob der Marker „Feld + 4 px" im Betrieb wirklich besser lesbar ist: das ist **eine Frage für Daniels Auge**,
  nicht für eine Rechnung. Kontrast ist Arithmetik, Erkennbarkeit nicht.
- Die Formen (Schild, Sechseck, Kreis, Quadrat, Dreieck, Stern) sind auf dem Papier unterscheidbar; ob sie es
  bei 18 px Innenfläche noch sind, entscheidet ein Probelauf am Bildschirm.
