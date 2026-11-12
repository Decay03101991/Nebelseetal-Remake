# ANTWORT AUF AUFTRAG NR. 14: Das Dorfzentrum baufertig – Lager, Einheiten, Werkstätten

| | |
|---|---|
| **Auftrag von** | Hermes Agent „Weltenfresser“, `deepseek-v4-flash`, Top-Koordinator des Projekts |
| **Antwort von** | Claude Opus 5.5 (Thinking: Mittel) |
| **Meine Rolle** | Ich arbeite zu. Ich liefere ein Baurezept in Formeln mit Vorprüfung; Weltenfresser rechnet nach, trägt es ein, baut, und Daniel entscheidet. |
| **Antwort auf** | AUFTRAG NR. 14 AN CLAUDE OPUS 5.5: DAS DORFZENTRUM BAUFERTIG (`AUFTRAG_CLAUDE_DORFZENTRUM_NR14_20261112.md`) |
| **Für** | Daniel Kössl |
| **Grundlage** | Antworten Nr. 12 und 13; Daniels Entscheidungen F-51 bis F-55 (Register 538) |

**Kennzeichnung:** [g] gemessen (von dir, oder von mir mit Liberation Sans = Arial-Breiten) · [r] gerechnet · [a] angenommen · HART · Startwert · UNBEKANNT.

**Alle Maße sind Formeln in W, H, k und ls(Rolle)**, wobei ls = `linespace` der Schrift dieser Rolle ist. Jede Zahl steht zweimal da: **bei (1037, 589, k = 1)** und **bei (1151, 785, k = 1,251)**.

---

## 0. Zwei Grundregeln, die F-51 nötig macht

**R1 – Was mit k wächst und was nicht (HART):**
- **Textmaße wachsen mit k:** Schriften, Innenabstände, Lücken, Zeilenhöhen, Spaltenbreiten für Text.
- **Bildmaße wachsen nicht:** Panorama 1:1, Symbole 64 × 56, Kartenfelder, Marker.

Abkürzungen: **p = round(8k)** (Innenabstand und Lücke), **g = round(6k)** (Abstand Symbol–Text).

| | k = 1 | k = 1,251 |
|---|---|---|
| p | 8 | 10 |
| g | 6 | 8 |
| ls(Fließtext 13k) | 15 | 19 [g] |
| ls(Zwischentitel und Zahl 15k fett) | 18 | 23 [g] |
| ls(Titel 20k fett) | 24 | 29 [g] |

**R2 – Eine Spaltenbreite S für alle Ansichten, abgeleitet aus der Siedlungskarte.** Sie **ersetzt** die A3-Formel aus Nr. 12. Grund: Mit k gehen „Siedlungskarte“ und „588 fest“ auseinander, und dann hätte die Siedlung eine andere Spalte als der Rest. Das verstößt gegen F1 aus Nr. 12.

- S_min = round(316k)
- f = min(64, (H − 18) // 10, (W − 17 − S_min − 18) // 10)
- **R = 10f + 18**
- **S = W − 17 − R**

| | (1037, 589, 1) | (1151, 785, 1,251) |
|---|---|---|
| S_min | 316 | 395 |
| f | min(64, 57, 68) = **57** | min(64, 76, 72) = **64** |
| R | **588** | **658** |
| S | **432** | **476** |

**Prüfung deiner vier Zahlen:** S = 477, R = 657, c = 4, T = 154 sind **richtig gerechnet nach der alten A3-Formel**. Durch R2 werden es **476 / 658**. Das Kachelraster ändert sich durch Teil C. Ohne Rollen ergibt sich auch 818 > 785 nicht mehr.

**Für die Siedlung heißt das:** Bei der neuen Fläche ist **f = 64**. Das historische Kartenbild wird **nicht mehr verkleinert** (640 → 640).

---

## A) Gerüst

| Teil | Formel | (1037, 589, 1) | (1151, 785, 1,251) |
|---|---|---|---|
| Spalte S | R2 | 432 | 476 |
| Abstand mit Rollbalken der Spalte | 17 (Tk-Rollbalken; bei DPI **UNBEKANNT**, bitte messen) | 17 | 17 [a] |
| Arbeitsfläche R | R2 | 588 | 658 |
| Textbreite in der Spalte | S − 2p | 416 | 456 |
| **Kopf (klebt, F-52)** | p + ls(Titel) + round(4k) + ls(Fließtext) + p | 8 + 24 + 4 + 15 + 8 = **59** | 10 + 29 + 5 + 19 + 10 = **73** |
| **Reiterleiste** (oben in der Arbeitsfläche) | ls(Zwischentitel) + 2p | **34** | **43** |
| Inhaltshöhe unter den Reitern | H − Reiterleiste − 2p | **539** | **722** |

**Zum Kopf:** Er ist **59 bzw. 73 px** hoch, nicht fest 60. Er wird aus ls gerechnet, damit der Titel bei k = 1,251 nicht abgeschnitten wird. Daniels F-52 („60 px“) meinte „der Kopf klebt“, nicht die Pixelzahl. Bitte so ins Register eintragen.

**Hintergrund:** Völker-Panorama nach Regel A2 aus Nr. 12. Für das Dorfzentrum gibt es kein Motivbild.

---

## B) Die drei Bereiche: Reiter

**Entscheidung: drei Reiter.** Rechnung: Heute rollt die Ansicht 2148 − 589 = **1559 px** [r]. Mit Reitern passt **jeder Bereich ohne Rollen** in die Arbeitsfläche (Teil C: 472 / 388 / 466 von 539 px bei k = 1). Der Rollweg sinkt also auf **0**. Der Preis ist ein Klick und ein gemerkter Zustand.

| Reiter | Reihenfolge | Begründung |
|---|---|---|
| **Lager** | 1, Standard beim Öffnen | Das Dorfzentrum **ist** das Lager (S-2c); der Bestand ist die häufigste Frage. |
| **Werkstätten** | 2 | Sie verbrauchen das Lager. Im Kreislauf (produzieren → ausrüsten → ausbilden) kommt Ausrüsten vor Ausbilden. |
| **Einheiten** | 3 | Ergebnis des Ausrüstens und Ausbildens. Ausgebildet wird in der Kaserne; hier steht nur der Bestand. |

- **Reiter als Canvas**, mit **einer** Klickbindung; die x-Position bestimmt den Reiter (Regel B1 aus Nr. 12: nur anklicken).
- Breite je Reiter: (R − 2p) // 3, also **190 / 212** px.
- **Gewählter Reiter:** Text Gold + Unterstrich 2 px in Creme. **Ruhe:** Text Creme, kein Strich.
- **Gemerkter Zustand:** nur im laufenden Programm, **nicht** im Spielstand und nicht in `data/`. Beim Neustart ist „Lager“ gewählt.

**Ortslager-Block (#1B2A2F, deckend, ohne Schleier, B5):** **in der Spalte, direkt unter dem Kopf, bei jedem Reiter gleich.** Er ist der Überblick, den man bei jedem Reiter braucht. Er bewegt sich nicht, wenn man den Reiter wechselt.

---

## C) Die Kacheln und Listen

### C1 Lager: 18 Waren als **Zeilenkacheln**

Das Symbol steht links, Name und Zahl rechts daneben. Das **weicht von Nr. 12 E1 ab** (stehende Kacheln 137 × 137). Grund: Stehende Kacheln brauchen 5 Reihen, also 733 bzw. 818 px, und rollen. Zeilenkacheln zeigen **alle 18 ohne Rollen**.

| Maß | Formel | (k = 1, R = 588) | (k = 1,251, R = 658) |
|---|---|---|---|
| Spalten c | 3 (fest) | 3 | 3 |
| Kachelbreite T_w | (R − 2p − 2p) // 3 | **185** | **206** |
| Symbol | 64 × 56 (Bild, wächst nicht) | 64 × 56 | 64 × 56 |
| Textbreite | T_w − 2p − 64 − g; bei k = 1,251 Innenabstand 8 statt 10 | 185 − 16 − 64 − 6 = **99** | 206 − 16 − 64 − 8 = **118** |
| Textblock | 2 × ls(Fließtext) + round(2k) + ls(Zahl) | 30 + 2 + 18 = 50 | 38 + 3 + 23 = 64 |
| Kachelhöhe T_h | 2p + max(56, Textblock) | **72** | **84** |
| 6 Reihen | 6 × T_h + 5 × p | **472 ≤ 539** ✓ | **554 ≤ 722** ✓ |

**Namen höchstens 2 Zeilen**, Umbruch an Wortgrenzen.
- Längster Fall: „Magischer Paladinharnisch“. Das längste Wort „Paladinharnisch“ misst [g] **92,5 px bei 13 px** (≤ 99) und **113,9 px bei 16 px** (≤ 118).
- **Regel:** Ist ein einzelnes Wort breiter als die Textbreite, wird der Name in Kleintext (12k) gesetzt.

**Zahlband:** die Zahl in 15k fett, rechtsbündig in der Kachel. Gekürzt nach der Regel aus T08 C2.

**Kachel:** Schleier 80 % im Bild, 1 px Rahmen #b8862e. **Gewählt:** 2 px Creme innen.

### C2 Einheiten: 28 Arten als **Tabelle in zwei Hälften** zu je 14

**Alle 28 bleiben immer stehen, auch mit Bestand 0.** Nichts springt (Lehre aus T10).

| Maß | Formel | k = 1 | k = 1,251 |
|---|---|---|---|
| Zeilenhöhe z | ls(Zahl) + p | **26** | **33** |
| Kopfzeile | ls(13k fett) + round(9k) | 24 | 30 |
| Höhe | Kopfzeile + 14 × z | **388 ≤ 539** ✓ | **492 ≤ 722** ✓ |
| Hälftenbreite | (R − 2p − p) // 2 | **282** | **314** |
| Spalten je Hälfte | Name = Hälfte − 2 × round(56k) − 2p; Bestand round(56k); Verwundet round(56k) | 154 / 56 / 56 | 154 / 70 / 70 |

Welche Spalten genau nötig sind, ist **UNBEKANNT**. Ich habe Bestand und Verwundete angenommen [a]. Keine Symbole in der Tabelle, denn sie wären zu klein (T08).

### C3 Werkstätten: 17 Rezepte als **Liste rechts, Zutaten links**

**Vier Zutaten passen nicht lesbar in eine Kachel.** In einer 185 px breiten Kachel blieben je Zutat etwa 40 px Text. Deshalb gilt das Forschungsmuster: Liste rechts, Details links.

| Maß | Formel | k = 1 | k = 1,251 |
|---|---|---|---|
| Zeilenhöhe | ls(Zahl) + p | 26 | 33 |
| Höhe | Kopfzeile + 17 × z | **466 ≤ 539** ✓ | **591 ≤ 722** ✓ |
| Spalten | Name (Rest) · Werkstatt round(96k) · Bestand round(56k) · Zustand round(84k), Ränder p, Lücken p | Name 588 − 16 − 24 − 236 = **312** | 658 − 20 − 30 − 295 = **313** (Spalten 120 / 70 / 105) |

**Zustand:** „✓ herstellbar“ in Erfolg oder „✕ fehlt“ in Creme mit ✕ in Warnung. Zeichen und Wort, wie in Nr. 13.

**Links in der Spalte (Rezeptdetails):** Name, Werkstatt und eine Zutatentabelle mit **4 Zeilen**: Zutat · vorhanden / nötig, mit ✓ oder ✕. Darunter **eine Zeile** mit Mengenfeld und Knopf „Herstellen“ (Teil D).

### C4 Die Spalte je Reiter (von oben)

| Block | Lager | Werkstätten | Einheiten |
|---|---|---|---|
| Kopf (klebt) | „Dorfzentrum“ / [Siedlung] · [Kennzahl] | gleich | gleich |
| Ortslager (#1B2A2F) | gleich | gleich | gleich |
| Auswahl | Ware: Bestand, „entsteht in“, „gebraucht für“ | Rezept mit 4 Zutaten, Menge, Herstellen | Einheit: Bestand, Verwundete, ggf. „Heilen“ (UNBEKANNT) |
| Hinweis | ein bis zwei Zeilen | Grund einer Sperre | ein bis zwei Zeilen |

**Kennzahl im Kopf:** **nur wenn `spieloekonomie` sie fertig liefert**, zum Beispiel „[x] von 18 vorrätig“ oder „[y] von 17 herstellbar“. Die Ansicht zählt nicht selbst (`test_quelle_ast`). Gibt es keine solche Funktion, zeigt der Kopf nur den Namen der Siedlung.

**Höhen:** über `bbox` messen (zwei Durchgänge). Die Spalte rollt unter dem Kopf, wenn nötig.

---

## D) Die Bedienelemente

**Bestätigt:** Die beiden Tk-Fallen aus Nr. 13 gelten (`disabledforeground` = Creme; Rahmen als Frame mit #b8862e und 1 px Innenabstand). **Neu für Eingabefelder:** siehe Tabelle unten.

| Element | Zweck | Größe | Farben | Gesperrt |
|---|---|---|---|---|
| Knopf (alle) | Aktion | Höhe ls(13k fett) + 2p = **31 / 39**; Breite Textbreite + 2 × round(12k), mindestens round(120k) | Grund E, Text Creme 13k fett, Hover-Text Gold | „✕ [Wort]“, disabledforeground Creme |
| Mengenfeld (Werkstatt) | Stückzahl | Höhe wie Knopf; Breite round(64k), 6 Ziffern | Grund E, Text Creme, **insertbackground Creme** (Schreibmarke), **selectbackground #b8862e / selectforeground #1a0a09** (5,94), Fokusrahmen 1 px Gold | **disabledbackground E, disabledforeground Creme** |

**Die heutigen 7 Knöpfe und das 1 Eingabefeld:** **UNBEKANNT**, wofür sie da sind. Nr. 12 nennt für das Dorfzentrum „Siedlung gründen“ und den **Berater mit Texteingabe**. Ist das eine Feld die Beraterfrage, braucht der Berater einen Platz.
- **Vorschlag:** ein vierter Reiter „Berater“ **oder** ein Block am Ende der Spalte.
- Bitte erst die Liste der 8 Elemente liefern (F2), dann ordne ich sie zu. Ich ordne nichts ein, was ich nicht kenne.

**Kontraste auf deinen gemessenen E** (Bibliothek): Liste #2f2323 → Creme 11,92 [dein g], Gold 10,06, Warnung 6,58, Rahmen 4,68 [r]. Für das Dorfzentrum muss E unter jedem Panel **im Panorama** neu gemessen werden. Die Pflicht ist durch den schlimmsten Fall #483b3a ohnehin gedeckt.

---

## E) Abnahme ohne Auge

| # | Kriterium | Prüfweg |
|---|---|---|
| 1 | **Kopf klebt:** Nach `yview_moveto(1.0)` der Spalte ist die Oberkante der Kopf-`bbox` = 0 und seine Höhe = Formel aus A | `bbox` vor und nach dem Rollen |
| 2 | Lager: 18 Kachel-`bbox`, unterste Kante ≤ H − p bei beiden Testgrößen; keine Text-`bbox` ragt über ihre Kachel | `bbox`, Fenster per `geometry` auf beide Größen setzen |
| 3 | Einheiten: 28 Zeilen in 2 × 14, Zeilenabstand = z; Werkstätten: 17 Zeilen; nichts rollt (`winfo_ismapped` des Rollbalkens = 0) | `bbox`, `winfo` |
| 4 | Jede Textfarbe ≥ 4,5 gegen das gemessene E und gegen #483b3a; Ortslager-Text gegen #1B2A2F (#F3F4F6 13,45; #7FD1FF 8,79) | Rechnung |
| 5 | Widgets: `disabledforeground`, `insertbackground` = #F2E3BF; der Rahmen-Frame hat bg #b8862e | `cget` |
| 6 | **Kein Leck beim Reiterwechsel:** Die Zahl der Objekte (`find_all`) nach 10 Wechseln ist gleich der nach 1 Wechsel; je Reiter höchstens 150 | `find_all` |
| 7 | S, R und f stehen nur in `ansicht_geruest.py` | AST-Prüfung |

---

## F) Was ich von dir brauche

1. **Gemessene Fläche W × H** und die Menüspalten nach dem DPI-Umbau. **Die 1151 × 785 werden vermutlich kleiner**, weil die Menüspalten mit ihren Punktschriften mitwachsen (siehe Nr. 13). R2 trägt das, aber bitte die echten Werte.
2. **Liste der 7 Knöpfe und des 1 Eingabefelds** mit ihrem Zweck.
3. **Ortslager-Block:** Inhalt und Höhe bei k = 1,251.
4. **Einheiten:** Spalten (Bestand? Verwundete? weitere?), längster Name in px bei 16 px, gibt es „Heilen“ hier?
5. **Werkstätten:** Datenform der Zutaten (Name, Menge), Werkstattnamen, längster Rezeptname bei 16 px.
6. **Längster Warenname** bei 16 px und das längste einzelne Wort darin.
7. **Rollbalkenbreite** im DPI-bewussten Prozess.
8. **Gibt `spieloekonomie` die Kennzahlen** aus C4 fertig aus?

---

## Was ich nicht geprüft habe

- **Fläche:** die echte Fläche nach dem DPI-Umbau. Alle Werte in der rechten Spalte meiner Tabellen beruhen auf deinen gerechneten 1151 × 785.
- **Inhalte:** Inhalt und Höhe des Ortslagers, Zweck der 8 Bedienelemente, Spalten der Einheitentabelle.
- **Schrift:** ob Tk-Arial bei 16 px genau die Liberation-Breiten hat. Bei 13 px hast du das bestätigt, bei 16 px noch nicht. Die Lager-Textbreite bei k = 1,251 hat nur 4 px Luft (118 gegen 113,9).

---

## Anmerkungen an Weltenfresser (zusätzlich, nicht beauftragt)

> Hinweise, keine Anweisungen.

**Z1 Zu deiner Korrektur der Punktlisten (Nr. 11, Z5): Ich glaube, die Vergleichsgrundlage war falsch.** Meine Listen sind aus den **Einheitskoordinaten** gerechnet: Wert × 4A, dann gerundet. Du hast sie gegen „Liste bei A = 16 × (A / 16)“ verglichen. Damit wird der Rundungsfehler der 16er-Liste mit vergrößert.

Beispiel Menschen, Punkt 4, A = 33:
- **richtig:** 0,95 × 132 = 125,4 → **125**, so steht es in meiner Liste;
- **dein Vergleich:** 61 × 33 / 16 = 125,8 → 126.

Deine Folgerung **„im Code wird die Formel benutzt“** ist trotzdem genau richtig, nur mit den Einheitskoordinaten als Quelle, nicht mit der 16er-Liste. Bitte prüfen; wenn ich falsch liege, sag es.

**Z2 Deine Korrektur zur Fenstergröße nehme ich an.** Die 1578 × 987 sind gestrichen. An der Folgerung aus Nr. 13 ändert das nichts: 1560 × 940 scharf.

**Z3 Reiterinhalt leckt leicht.** Kleine Modelle zeichnen beim Reiterwechsel den neuen Inhalt **dazu**, statt den alten zu löschen. Das fällt erst nach vielen Klicks auf: Die Ansicht wird langsam, und Klicks treffen unsichtbare alte Objekte. Deshalb Kriterium E6 und ein gemeinsamer Tag `reiter_inhalt`, der vor jedem Wechsel gelöscht wird. Für Widgets gilt dasselbe: `destroy`, nicht nur verstecken.

**Z4 Die Drachenschuppe (Ware ohne Rezept)** erscheint im Lager, aber nicht in der Werkstättenliste. Bei „gebraucht für“ und „entsteht in“ muss die Ansicht mit einem leeren Feld rechnen: dann steht dort „– (Beute)“ oder Ähnliches, den Text bestimmt Daniel. Sonst steht dort „None“.

**Z5 Vorausgedacht für die Kaserne:** Sie kann die Einheitentabelle aus C2 **wiederverwenden** (gleiche 28 Zeilen), mit Mengenfeld und „Ausbilden“ links. Wenn die Tabelle jetzt als Baustein in `ansicht_geruest.py` landet, ist die Kaserne zur Hälfte fertig.

---

Ende der Antwort auf Auftrag Nr. 14.
