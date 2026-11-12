# ANTWORT AUF AUFTRAG NR. 12: Eine Vorlage für alle Ansichten

| | |
|---|---|
| **Auftrag von** | Hermes Agent „Weltenfresser“, `deepseek-v4-flash`, Top-Koordinator des Projekts |
| **Antwort von** | Claude Opus 5.5 (Thinking: Mittel) |
| **Meine Rolle** | Ich arbeite zu. Ich liefere ein Baurezept (D2) mit Vorprüfung (D1). Weltenfresser zerlegt, misst, baut und führt das Register, und Daniel entscheidet. |
| **Antwort auf** | AUFTRAG NR. 12 AN CLAUDE (Klasse Opus 5.5): EINE VORLAGE FÜR ALLE ANSICHTEN, `AUFTRAG_CLAUDE_ANSICHTEN_NR12.md` |
| **Für** | Daniel Kössl |
| **Gilt für** | Dorfzentrum, Lager, Kaserne/Ausbildung, Forschung, Stellmacher, Portal; die Siedlungskarte mit kleinen Änderungen |

**Kennzeichnung:** **HART** · **Startwert** · **PLATZHALTER** · **UNBEKANNT**, wie im Auftrag. Alle Kontraste sind nach WCAG gerechnet, alle Textbreiten mit Liberation Sans gemessen (gleiche Breiten wie Arial).

---

## Der Grundsatz in einem Satz

**Links lesen, rechts handeln.**
- **Links** steht in jeder Ansicht dieselbe Spalte mit Kopf und Erklärung.
- **Rechts** steht die Arbeitsfläche dieser Ansicht: die Karte, die Kacheln, die Liste.

Die Siedlungskarte hat das schon. Alle anderen Ansichten bekommen dasselbe Gerüst.

---

## A) Das Grundgerüst

### A1 Ebenen (hinten nach vorne) – HART

| Ebene | Inhalt |
|---|---|
| 0 | Hintergrundbild mit eingerechneten Schleiern (EIN Canvas-Bild) |
| 1 | Canvas-Texte der Spalte |
| 2 | Arbeitsfläche rechts: Canvas-Kacheln oder Widgets |
| 3 | Widgets (Knöpfe, Eingaben) |
| 4 | Auswahl- und Hover-Rahmen |

### A2 Hintergrund – welches Bild (Reihenfolge der Wahl, HART)

1. **Motivbild des Gebäudes** zu dieser Ansicht, **für das Volk des Spielers**, falls die Datei existiert. Heute gibt es nur Elfen-Bilder: Bibliothek → Forschung, Kriegerakademie → Ausbildung, Stellmacher → Stellmacher.
2. Sonst das **Völker-Panorama** des Spielers.
3. Sonst gilt der **Rückfall C**.

Der Ausschnitt ist immer mittig 1:1 und wird nie skaliert (Register 502). Die Formel steht in Antwort Nr. 9, Teil C.

### A3 Aufteilung – HART

| Fläche | Spalte S | Abstand | Arbeitsfläche R |
|---|---|---|---|
| Formel | S = **min(477, max(316, W − 17 − 588))** | 17 px, darin der Rollbalken der Spalte | R = W − S − 17 |
| 1037 × 589 | **432** | 17 | **588** |
| 1151 × 785 | 477 | 17 | 657 |
| 867 × 565 | 316 | 17 | 534 |
| W unter 650 | übereinander (Regel aus Nr. 9) | – | – |

**Begründung:**
- Bei 1037 × 589 ergibt das **genau die Maße der Siedlungskarte** (432 + 17 + 588). Damit sieht jede Ansicht gleich aufgeteilt aus.
- **Portal:** Die Karte bekommt R = 588. Mit `_portal_zelle` folgt daraus f = 588 // 20 = **29 px**, die Stufe „mittel“ aus Antwort Nr. 10. Die Weltkarte wird also automatisch größer als heute (20 px).

### A4 Kopf – HART

- Oben in der Spalte, **60 px** hoch (Startwert), **klebt beim Rollen fest**.
- Er besteht aus einem Schleierblock mit Innenabstand 8 px:
  - Titel 20 px fett in Gold #FFCC33 (Zeilenhöhe 24),
  - 4 px Abstand,
  - Kontextzeile 13 px normal in Creme #F2E3BF (Zeilenhöhe 15).
- Inhalt der Kontextzeile: Bauplan **[Siedlungsname] · [eine Kennzahl dieser Ansicht]**. Welche Kennzahl, legt Weltenfresser je Ansicht fest.

**Siedlungskarte:** Dort rollt der Titel heute mit. Nach dieser Vorlage klebt er fest. Das ist eine kleine Änderung an einer schon gebauten Ansicht; Daniel entscheidet.

### A5 Wo rollt was – HART

| Bereich | Regel |
|---|---|
| **Spalte** | rollt unterhalb des Kopfes, sobald ihr Inhalt höher ist als H − 60 (bei H = 589: über 529 px). Der Rollbalken sitzt im 17-px-Abstand. |
| **Arbeitsfläche** | rollt **nur senkrecht und nur, wenn nötig**. Ihr Rollbalken (17 px) liegt **innen am rechten Rand**; die nutzbare Breite ist dann R − 17. |
| **Ganze Ansicht** | rollt **nie**, außer bei der Anordnung übereinander. |
| **Bild** | rollt nicht. Die Schleier der Spalte liegen in einem eigenen Spaltenbild, das mit der Spalte rollt (Antwort Nr. 9, Teil B). |

---

## B) Die Textblöcke

### B1 Canvas-Text oder Widget – die Grenze (HART)

| Art | wird |
|---|---|
| Text, Zahl, Überschrift, Erklärung (nur lesen) | **Canvas-Text** (`create_text`) |
| Kachel oder Zeile, die man **nur anklickt**, um sie auszuwählen | **Canvas** (Rechteck mit Klickbindung über Tag) |
| **Knopf** (Bauen, Ausbilden, Forschen …) | **Widget** (Button), wegen Sperrzustand und Tastatur |
| **Eingabe** (Menge, Text, Auswahlliste, Schieber) | **Widget** |
| Tabelle mit **mehr Zeilen als sichtbar** oder mit Eingaben in Zellen | **Widget** (Treeview) |

**Die Regel kurz:** Sobald die Tastatur oder ein Sperrzustand nötig ist, ist es ein Widget. Alles andere kommt auf die Leinwand.

### B2 Schriftgrade (in **Pixeln**, nicht Punkten)

**Wichtig für Tk:** Eine **negative** Größe bedeutet Pixel. `("Arial", -13)` sind 13 px, `("Arial", 13)` sind 13 Punkt und bei 125 % etwa 22 px. Das erklärt, warum die heutigen Größen je nach Skalierung anders wirken.

| Rolle | Größe | Stil | Farbe | Zeilenhöhe | Zeichen je 416 px |
|---|---|---|---|---|---|
| Titel | 20 px | fett | Gold #FFCC33 | 24 | ≈ 43 |
| Zwischentitel | 15 px | fett | Gold #FFCC33 | 18 | ≈ 58 |
| Fließtext | **13 px** | normal | Creme #F2E3BF | 15 | ≈ 71 |
| Zahl | 15 px | fett | Creme #F2E3BF | 18 | – |
| Kleintext (Untergrenze) | **12 px** | normal | Creme | 14 | ≈ 77 |
| Warnung | wie Fließtext | fett | #ff8a70 | 15 | – |
| Erfolg | wie Fließtext | normal | #a5d67a | 15 | – |

**Kein Text unter 12 px** (HART). Das Rahmenbraun #b8862e ist **nie Textfarbe auf dem Schleier**, denn es erreicht dort nur 3,31.

### B3 Zeilenumbruch

`create_text` mit `width = 416` (Spaltenbreite 432 − 2 × 8 Innenabstand) bricht an Wortgrenzen um.

**Faustregel:** Zeichen je Zeile ≈ Breite / (0,45 × Größe) bei normaler Schrift und Breite / (0,48 × Größe) bei fetter.

Die **Höhe** eines Blocks wird nicht geschätzt, sondern **nach dem Anlegen gemessen** (`bbox`). Daraus folgt der Ablauf in zwei Durchgängen:
1. Alle Texte der Spalte anlegen; jede Oberkante = Unterkante des Blocks davor + 8 + 8 + 8. Die `bbox` jedes Blocks merken.
2. Aus den `bbox` die Schleierrechtecke rechnen (bbox ± 8 px), sie **einmal** mit Pillow ins Spaltenbild einrechnen und das Bild ganz nach hinten legen (`tag_lower`).

### B4 Abstände (Startwerte)

| Abstand | Wert |
|---|---|
| Innenabstand des Schleiers | **8 px** an allen Seiten |
| Lücke zwischen zwei Blöcken, in der das Bild sichtbar ist | **8 px** |
| Schleier zum Spaltenrand | **0 px**. Der Schleier geht über die volle Spaltenbreite 432; Text steht bei x = 8 bis 424. |
| zwischen Zwischentitel und Text | 4 px |

### B5 Wo kein Schleier hingehört – HART

- Flächen mit **eigener deckender Farbe**: der Ortsbestand (#1B2A2F) und die Koordinatenleiste.
- **Unter Widgets:** Die tragen ihre eigene Farbe (Teil D).
- **Über der Karte** und **über Kacheln** mit eigenem Bild.
- **In die Lücken** zwischen den Blöcken. Dort soll das Bild zu sehen sein.

### Kontraste auf dem Schleier (schlimmster Fall: reines Weiß darunter → #483b3a)

| Farbe | auf Schleier | auf #1a0a09 | auf #3e1c1a |
|---|---|---|---|
| Creme #F2E3BF | **8,42** | 15,13 | 11,92 |
| Gold #FFCC33 | **7,10** | 12,77 | 10,06 |
| Erfolg #a5d67a | **6,37** | 11,45 | 9,02 |
| Warnung #ff8a70 | **4,65** | 8,36 | 6,58 |
| Rahmen #b8862e (nur Linien) | 3,31 | 5,94 | 4,68 |

**„Texte deutlicher“ (Daniels Wunsch)** wird über **Größe** erreicht: Fließtext 13 statt bisher Tk 8 Punkt, Titel 20 px fett. Ein Schattenwurf ist nicht nötig, denn der Kontrast ist schon im schlimmsten Fall ≥ 4,65.

---

## C) Rückfall ohne Bild

Das gilt, wenn das Bild fehlt **oder Pillow fehlt**. Gezeichnet wird deshalb **nur mit Canvas-Rechtecken**, ohne Pillow.

| Teil | Darstellung |
|---|---|
| Grund der ganzen Ansicht | **#3e1c1a** (Handbuch „Fläche“) |
| jeder Textblock | Rechteck **#1a0a09** (deckend statt 80 %) mit **1 px Rahmen #b8862e** |
| Lücken zwischen den Blöcken | bleiben #3e1c1a |
| Ersatzfarbe der Widgets (D) | **#1a0a09** |

Kontraste: Rahmen gegen Grund 4,68, Rahmen gegen Block 5,94, Text im Block 15,13. Es entsteht ein geordnetes **„Karten auf dem Tisch“-Bild**: dieselben Blöcke an denselben Stellen, nur ohne Bild. Das Layout verschiebt sich um **0 px**.

---

## D) Die bedienbaren Blöcke (Panels)

**Empfehlung: beides zusammen.**
1. Die **Panelfläche bekommt im Bild einen Schleier** wie ein Textblock (80 %).
2. Die **Widgets darauf** bekommen als Hintergrund die **Ersatzfarbe E**, die dem Schleier an dieser Stelle im Mittel entspricht. So fallen die Widget-Rechtecke kaum auf.

**Formel je Panel (Startwert, einmal je Neuschnitt):**
- **M** = mittlere Farbe (R, G, B) des **ungeschleierten** Bildausschnitts unter dem Panel (Pillow, `ImageStat.mean`).
- **E** = (20,8 + 0,2 × M_R ; 8,0 + 0,2 × M_G ; 7,2 + 0,2 × M_B), auf ganze Zahlen gerundet.

Das ist genau 0,8 × #1a0a09 (26, 10, 9) + 0,2 × M.

**Kontrast – HART erfüllt:** Der hellste mögliche Wert ist E = #483b3a (bei M = Weiß). Darauf gilt:
- Text in Creme ≥ **8,42**, Gold ≥ 7,10, Warnung ≥ 4,65.
- Für Knopftexte und Tabellentexte gilt das ebenso, **in Creme** geschrieben.

**Knöpfe:** Hintergrund E, Rahmen 1 px #b8862e (≥ 3,31 gegen E), Text Creme 13 px fett. **Gesperrt:** Text bleibt Creme, davor das Zeichen „✕“, **nicht** ausgegraut, damit die 4,5 : 1 auch im Sperrzustand halten.

---

## E) Muster „Lager“ und Reihenfolge

### E1 Lager, vollständig (bei 1037 × 589)

**Spalte (432 breit)**, von oben:

| Block | Höhe | Inhalt | Schrift |
|---|---|---|---|
| Kopf (klebt) | 60 | „Lager“ · [Siedlung] · [Belegung / Kapazität] | 20 fett Gold / 13 Creme |
| Auswahl | ≈ 90, gemessen | Name der gewählten Ware; Bestand; Rate je Stunde (wie T08); „entsteht in“ / „gebraucht für“ | 15 fett Gold; 15 fett Zahl; 13 Text |
| Summen | ≈ 70, gemessen | Bestände nach Rubrik, je eine Zeile „Name … Zahl“, Zahl rechtsbündig bei x = 424 | 13 / 15 fett |
| Hinweis | ≈ 50, gemessen | eine Zeile Erklärung, z. B. Kapazitätswarnung als Warnung | 13 |

Summe ≈ 60 + 8 + 90 + 8 + 70 + 8 + 50 = **294 px**. Die Spalte rollt also nicht.

**Arbeitsfläche (588 × 589): Kachelraster**

| Größe | Formel | bei R = 588 |
|---|---|---|
| Spalten c | max(2, (R − 8) // 145) | **4** |
| Kachel T | (R − 16 − (c − 1) × 8) // c | **137 × 137** |
| Rand / Abstand | 8 / 8 | |
| ohne Rollen sichtbar | 4 Reihen | **16 Kacheln** |

Aufbau einer Kachel (ein Canvas-Rechteck mit Klickbindung, darauf das Bild und zwei Texte):
- Schleier 80 % (im Bild eingerechnet), 1 px Rahmen #b8862e.
- Symbol **64 × 64** oben mittig, 8 px vom oberen Rand.
- Name 13 px Creme, mittig, 6 px darunter.
- Zahl 15 px fett Creme, mittig, 2 px darunter.
- Höhe: 8 + 64 + 6 + 15 + 2 + 18 + 8 = **121 ≤ 137**.

Die Auswahl zeigt einen 2-px-Creme-Rahmen innen.

**Offen:**
- **UNBEKANNT:** Anzahl der Lagerposten (11 Leistenwerte? 17 Waren? beides?) und Größe der Symbole aus T10. Bei mehr als 16 Posten rollt die Arbeitsfläche.
- **Daniel:** Die Symbole lagen in T08 bei 0 von 9 erkannt. Das war bei unter 24 px; 64 px sind ein anderer Fall. Bitte mit dem Auge prüfen.

### E2 Reihenfolge der übrigen Ansichten

| # | Ansicht | Was dort anders ist |
|---|---|---|
| 1 | **Lager** (Muster) | nur lesen und auswählen, keine Widgets außer dem Rollbalken: der einfachste Fall |
| 2 | **Forschung** | 21 Einträge mit Zustand (gesperrt / möglich / läuft / fertig). Rechts eine Liste als Canvas-Zeilen (Zeilenhöhe 32 px, also 18 sichtbar). Links Details zur Wahl. Ein Knopf „Forschen“. Zustand als **Zeichen plus Wort**, nicht nur als Farbe. Motivbild Bibliothek. |
| 3 | **Kaserne / Ausbildung** | 28 Einheiten, dazu **Mengeneingabe** (Widget) und Verwundete. Rechts Kacheln wie im Lager, links Details mit Eingabe und Knopf. Motivbild Kriegerakademie. |
| 4 | **Stellmacher** | 17 Rezepte mit je **4 Zutaten**. Rechts eine Liste, links das Rezept als Tabelle mit 4 Zeilen „Zutat · vorhanden / nötig“ (Canvas), dazu Menge (Widget). Fehlende Zutat in Warnung **mit „✕“**. |
| 5 | **Dorfzentrum** | die gemischteste Ansicht: Überblick, Gründen und Berater mit **Texteingabe**. Sie kommt zuletzt, weil sie alle Bausteine der anderen vier braucht. |
| – | **Portal** | Es gilt nur A3 (R = 588, f = 29) plus das Markersystem aus Nr. 10. Kein eigener Schritt nötig. |

---

## F) Abnahme

| # | Kriterium | Art | Prüfweg |
|---|---|---|---|
| 1 | Jede Ansicht hat Kopf 60 px, S nach der Formel aus A3 und die Bildwahl aus A2 | HART | Messung |
| 2 | Jeder Text liegt auf Schleier, auf deckender Eigenfarbe oder auf E; Text ≥ 4,5, Linien ≥ 3 | HART | Rechnung gegen #483b3a bzw. E |
| 3 | Kein Block ist schmaler als seine Wunschbreite; wenn doch, gilt die Umbruchregel aus Nr. 9 | HART | Messung |
| 4 | Bei 1037 × 589 sind ohne Rollen sichtbar: Kopf, der erste Block der Spalte und die erste Reihe der Arbeitsfläche | HART | Messung |
| 5 | Ohne Bilddatei und ohne Pillow: Rückfall C, keine Lage verschiebt sich | HART | Start mit umbenannter Datei; Start ohne Pillow |
| 6 | Kein Text unter 12 px; alle Schriftgrößen als negative Tk-Größen (Pixel) | HART | Codeprüfung, Messung |
| 7 | Höchstens **N = 150** Canvas-Objekte je Ansicht, ohne Karte und ohne Marker | Startwert | `find_all` zählen |

**Zu N = 150:** 1 Hintergrundbild + rund 15 Spaltentexte + je Kachel 4 Objekte (Klickfläche, Symbol, Name, Zahl) × 28 Einheiten = 112 + Auswahlrahmen. Damit reicht es auch für die größte Ansicht (Kaserne).

---

## Was ich nicht geprüft habe

- **Lager:** die genaue Liste der Lagerposten und die Größe der Symbole aus T10.
- **Inhalte der Ansichten:** was Forschung, Kaserne, Stellmacher und Dorfzentrum heute genau anzeigen. Ich kenne nur die Zahlen aus Abschnitt 0 des Auftrags.
- **Schrift:** wie die Größen bei 125 % wirklich aussehen. Das hängt an Z1 aus Antwort Nr. 10 (DPI-Verdacht), siehe unten.
- **Zeichen ✕:** ob es in Arial unter Tkinter dargestellt wird.
- **Leistung:** wie lange das Einrechnen der Schleier je Ansicht dauert.

---

## Anmerkungen an Weltenfresser (zusätzlich, nicht beauftragt)

> Hinweise, keine Anweisungen.

**Z1 Der DPI-Verdacht aus Antwort Nr. 10 ist jetzt entscheidend.** Diese Vorlage legt Schriften in Pixeln fest. Ist das Programm nicht DPI-aware, vergrößert Windows alles um 1,25 und macht es weich. Dann wirkt auch eine perfekte Vorlage „verwaschen“. Bitte die 100-px-Probe **vor** dem Umbau der ersten Ansicht machen. Ihr Ergebnis bestimmt, ob 13 px Fließtext am Bildschirm wirklich 13 oder 16 Bildpunkte sind.

**Z2 Eine Funktion für alle Ansichten, nicht fünf Kopien.** Die Vorlage (Gerüst A, Kopf, Schleier mit zwei Durchgängen, Rückfall C, Ersatzfarbe E) gehört an **eine** Stelle, etwa neben `hintergrund_optik.py`. Jede Ansicht übergibt nur noch ihre Blöcke. Kleine Modelle bauen solche Vorlagen sonst in jede Ansicht hinein, und die fünf Fassungen laufen auseinander. Eine Prüfung dazu: Die Zahl 432 oder die Formel für S darf nur an einer Stelle im Code stehen.

**Z3 `test_quelle_ast`:** Die Rechnung für E (Mittelwert und Mischung) ist Bildverarbeitung, keine Ökonomie. Sie bleibt in der Ansicht erlaubt. Gehört sie aber in das gemeinsame Modul aus Z2, kann die Wache gar nicht erst anschlagen.

**Z4 Neu einrechnen nur bei Änderung.** Das Spaltenbild mit Schleiern wird nur neu gebaut, wenn sich die Fenstergröße oder **die Blockhöhen** ändern (zum Beispiel ein neuer Hinweistext). Nicht beim Rollen und nicht bei jedem Takt. Sonst ruckelt die Ansicht im Minutentakt der Ressourcen. Zahlen, die sich ändern, ohne dass sich die Blockhöhe ändert, werden mit `itemconfigure` auf dem vorhandenen Canvas-Text getauscht.

**Z5 Neue Datenschlüssel:** Die Startwerte (Kopf 60, Abstände 8 / 8, Schriftgrößen, N, Kachelformel) gehören in **eine** Datendatei, so wie `ressourcenleiste.json` für die Leiste. Ob es schon eine passende gibt, zum Beispiel für den Skin, ist UNBEKANNT. Eine neue Datei nur mit Daniels Zustimmung.

---

Ende der Antwort auf Auftrag Nr. 12.
