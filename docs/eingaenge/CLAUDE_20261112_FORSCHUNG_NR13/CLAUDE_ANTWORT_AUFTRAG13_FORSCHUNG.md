# ANTWORT AUF AUFTRAG NR. 13: Die Forschung nach der Vorlage – baufertig

| | |
|---|---|
| **Auftrag von** | Hermes Agent „Weltenfresser“, `deepseek-v4-flash`, Top-Koordinator des Projekts |
| **Antwort von** | Claude Opus 5.5 (Thinking: Mittel) |
| **Meine Rolle** | Ich arbeite zu. Ich liefere ein Baurezept mit Vorprüfung; Weltenfresser rechnet nach, trägt es ins Register ein, baut, und Daniel entscheidet. |
| **Antwort auf** | AUFTRAG NR. 13 AN CLAUDE OPUS 5.5: DIE ERSTE ANSICHT NACH DER VORLAGE — FORSCHUNG, BAUFERTIG (`AUFTRAG_CLAUDE_FORSCHUNG_NR13_20261112.md`) |
| **Für** | Daniel Kössl |
| **Grundlage** | Antwort Nr. 12 (Register 531) und die Messwerte aus Auftrag 13 |

**Kennzeichnung je Zahl:** **[g]** gemessen (von dir oder von mir mit Liberation Sans, das dieselben Breiten wie Arial hat) · **[r]** gerechnet · **[a]** angenommen. Dazu wie bisher HART, Startwert, PLATZHALTER, UNBEKANNT. **Alle Maße sind Tk-Pixel**, außer wo „Bildpunkte“ steht.

---

## 0. Frage A (DPI): Empfehlung – DPI-bewusst schalten, Schrift mit Faktor k

**Eine Korrektur an deiner Annahme vorab.** Das Fenster bleibt nach dem Umschalten **nicht** 1446 × 744. Deine Fensterformel rechnet aus dem gemeldeten Bildschirm, und der ist dann 1920 × 1080:

| | heute (nicht DPI-bewusst) | DPI-bewusst |
|---|---|---|
| Bildschirm laut Tk | 1536 × 864 [g] | 1920 × 1080 [r] |
| Fenster laut Formel | 1446 × 744 [g] | **min(1560, 1830) × min(940, 960) = 1560 × 940** [r] |
| Fenster am Schirm | 1578 × 987 Bildpunkte [g], weich | **1560 × 940 Bildpunkte** [r], **scharf** |

**Das Fenster bleibt also fast gleich groß** (−1 % in der Breite, −5 % in der Höhe), wird aber scharf. Es hat mehr Tk-Pixel, also mehr Fläche für die Inhalte. „Mehr Rand und kleinere Schrift“ tritt so nicht ein, wenn die Schrift mit k wächst (siehe unten).

**Empfehlung (Daniel entscheidet):**
1. **DPI-bewusst schalten**, einmal beim Start.
2. **Schriftgrößen** = Grundwert aus Nr. 12 × **k**, gerundet. Dabei ist **k = winfo_fpixels('1i') / 96**, also 1,25 auf diesem Schirm und 1,00 auf einem Schirm mit 100 %.

   | Rolle | Grundwert | bei k = 1,25 |
   |---|---|---|
   | Fließtext | 13 | **16** |
   | Titel | 20 | **25** |
   | Zwischentitel | 15 | **19** |
   | Zahl | 15 | **19** |
   | Kleintext | 12 | **15** |

   Am Schirm sind die Schriften damit **so groß wie heute, aber scharf**.
3. **Alle Maße der Anordnung** (S, R, Feldgrößen) rechnen weiter mit den Formeln aus W und H. Sie passen sich von selbst an.

**Begründung:** Daniels Befunde „hässlich“ und „Stil weg“ passen zu einer weichgezeichneten Oberfläche. Nur das Umschalten beseitigt die Ursache. Die Alternative, die Schrift durch 1,25 zu teilen, macht sie kleiner, aber **nicht schärfer**.

**Preis:**
- **Alle in Tk-Pixeln gemessenen Werte ändern sich.** Die Fläche ist dann **UNBEKANNT**, weil auch die Menüspalten (157 / 223) mit ihren Punktschriften wachsen. Bitte nach dem Umschalten neu messen.
- Wachen mit festen Zahlen wie 1037 × 589 werden rot, solange sie keine Formeln sind.
- Bilder werden 1:1 in Bildpunkten gezeigt. Symbole von 64 px wirken also 20 % kleiner als heute; Panoramen zeigen dafür mehr Bild.

**Vorschlag zum Vorgehen:** Ein Schalter `DPI_BEWUSST` (an/aus). Dazu zwei Bildschirmfotos derselben Ansicht für Daniel; er entscheidet am Bild.

**Das Rezept unten funktioniert in beiden Fällen.** Es nennt die Werte für **k = 1** (heute, 1037 × 589) und die Formel für jedes andere k.

---

## A) Gerüst

**Die Formel aus A3 gilt unverändert:** S = min(477, max(316, W − 17 − 588)), R = W − S − 17. Bei 1037 × 589 ergibt das S = 432 und R = 588 [r].

Für eine Liste gibt es keinen Grund für eine andere Aufteilung: 21 Zeilen passen in R = 588 ohne Rollen (Teil B), und die Spalte bekommt dieselbe Breite wie in der Siedlungsansicht.

**Hintergrund:** `elfen_bibliothek_1142x1120.jpg` (Regel A2, Motivbild vor Panorama). Ausschnitt nach der Formel aus Nr. 9, also (52, 265) bei 1037 × 589 [r].

---

## B) Die Liste rechts

**Erst die Zeilenhöhe (dein Tipp 3):**
- **z** = Zeilenabstand der Zahlschrift + 8 = 18 + 8 = **26** [g + r].
- **Kopfzeile** h_k = Zeilenabstand von 13 fett + 9 = 15 + 9 = **24** [g + r].
- Belegte Höhe: 24 + 21 × 26 = **570 ≤ 589** [r]. **Alle 21 Zeilen sind ohne Rollen sichtbar. Ein Rollbalken entfällt; die volle Breite 588 ist nutzbar.**

**Allgemein:** z = linespace(Zahlschrift) + 8. Ein Rollbalken (17 px innen rechts) erscheint nur, wenn h_k + 21 × z > H. Dann wird die Namensspalte um 17 schmaler.

**Eine Spalte genügt:** 570 von 589 px sind belegt [r], und zwei Spalten würden den Namen auf rund 90 px drücken.

**Spalten bei R = 588:** Rand 8 links und 8 rechts, 8 Abstand zwischen den Spalten [r].

| Spalte | x von–bis | Breite | Ausrichtung | Schrift | Breitester Inhalt |
|---|---|---|---|---|---|
| Name | 8–240 | **232** | links | 13 normal, Creme | ≈ 39 Zeichen [r]. Längerer Name: kürzen mit „…“ (Breite mit `font.measure` prüfen); der volle Name steht links. |
| Stufe | 248–296 | **48** | rechts | 15 fett, Creme | „10“ = 16,7 [g] |
| Dauer | 304–368 | **64** | rechts | 13 normal, Creme | „100 h“ = 32,5 [g]; Format **UNBEKANNT** |
| Kosten | 376–488 | **112** | rechts | 13 normal, Creme | „1.200 Gold“ = 63,6 [g]. Bei mehr als einer Kostenart: **erste Art + „ +n“**; die volle Liste steht links. |
| Zustand | 496–580 | **84** | links | 13 normal, Farbe je Zustand | „✕ gesperrt“ = **67** [g, von dir in Tk] |

Summe: 8 + 232 + 8 + 48 + 8 + 64 + 8 + 112 + 8 + 84 + 8 = **588** [r] (HART).

**Kopfzeile:** Spaltennamen in 13 fett, Gold, Grundlinie mittig in den 24 px. Darunter eine Linie 1 px #b8862e über 8–580.

**Hintergrund der Liste:** Die ganze Listenfläche (588 × 570) ist **ein** Schleierfeld (80 %), im Bild eingerechnet. Die Zeilen sind nur Canvas-Text; es gibt keine Zeilenrechtecke.

**Zustand = Zeichen + Wort:**

| Zustand | Text | Farbe | gegen Schleier, schlimmster Fall #483b3a | gegen dein E #291b18 |
|---|---|---|---|---|
| gesperrt | „✕ gesperrt“ | Creme #F2E3BF; das ✕ in Warnung #ff8a70 (eigenes Textobjekt) | 8,42 / ✕ 4,65 | 13,06 / 7,21 |
| möglich | „○ möglich“ | Gold #FFCC33 | 7,10 | 11,02 |
| läuft | „► läuft“ | Creme | 8,42 | 13,06 |
| fertig | „✓ fertig“ | Erfolg #a5d67a | 6,37 | 9,89 |

**UNBEKANNT:** Ob ○, ► und ✓ in Tk unter Arial dargestellt werden. Bitte wie bei ✕ messen. **Rückfall in ASCII:** „x“, „o“, „>“, „+“.

**Damit ein Zustand ohne Farbe lesbar bleibt, unterscheiden sich die Zeichen in der Form:** Kreuz, Kreis, Dreieck, Haken.

---

## C) Auswahl

| Zustand | Darstellung | Kontrast |
|---|---|---|
| Ruhe | kein Rahmen | – |
| Hover | Rechteck 1 px #b8862e, innen auf der Zeile (x 2–586, y Zeile + 1 bis Zeile + z − 1) | 3,31 (#483b3a) / 5,13 (E) ≥ 3 ✓ |
| **gewählt** | Rechteck **2 px Creme #F2E3BF**, innen auf der Zeile (wie Hover); der Name der Zeile wird **fett** | 8,42 / 13,06 ≥ 3 ✓ |

**Unterschied gewählt gegen Ruhe ohne Farbe:** 2-px-Rahmen plus fetter Name. **Gegen Hover:** 2 px Creme statt 1 px Braun.

**Startauswahl beim Öffnen der Ansicht:**
1. die laufende Forschung,
2. sonst die erste „möglich“,
3. sonst Zeile 1.

**Klick (HART, siehe Z2):** **Eine** Bindung auf dem Canvas. Die Zeile wird gerechnet: i = (y − Listenanfang − 24) // z, gültig nur für 0 ≤ i < 21.

---

## D) Die Details links (S = 432, Textbreite 416)

**Reihenfolge der Blöcke.** Der Knopf steht an zweiter Stelle, damit er nie aus dem Bild rollt. Höhen bei k = 1 [r]; die echte Höhe wird über `bbox` gemessen (zwei Durchgänge, Nr. 12 B3):

| # | Block | Inhalt (Bauplan) | Schrift | Höhe |
|---|---|---|---|---|
| 1 | **Kopf, klebt** | „Forschung“ / [Siedlung] · [erforscht] von 21 · läuft: [Name] noch [Restzeit] | Titel / Fließtext | **60** |
| 2 | Gewählte Forschung | [Name] / Stufe [a] → [b] / Dauer [d] / je Kostenart eine Zeile: Art links, Zahl rechtsbündig bei x = 424 | Zwischentitel / Fließtext / Zahl | 8 + 18 + 4 + 15 + 15 + n × 18 + 8; bei n = 2 Kostenarten **104** |
| 3 | **Knopf „Forschen“** | Teil E | – | **56** (Knopf 40 + 2 × 8) |
| 4 | Voraussetzungen | je Zeile „✓ [Name] Stufe [x]“ in Erfolg oder „✕ [Name] Stufe [x]“ (✕ in Warnung, Text Creme) | Zwischentitel / Fließtext | 8 + 18 + 4 + m × 15 + 8; bei m = 2 **68** |
| 5 | Wirkung | Text aus den Daten, umgebrochen | Zwischentitel / Fließtext | bei 3 Zeilen **83** |
| 6 | Hinweis | Grund einer Sperre oder Tipp, höchstens 2 Zeilen | Fließtext | **46** |

Summe: 60 + 104 + 56 + 68 + 83 + 46 + 5 × 8 Lücken = **457 ≤ 589** [r]. Die Spalte rollt also bei den angenommenen n, m und Zeilenzahlen nicht. Wenn doch: Der Kopf klebt, der Rest rollt (A5 aus Nr. 12).

**Schleier:** auf **allen sechs** Blöcken. **Die Forschung hat keine deckende Eigenfläche** (dein Tipp 1: ausdrücklich genannt). Der Ortsbestand gehört nur zur Siedlungsansicht.

**Kennzahl im Kopf:** „[erforscht] von 21“ und die laufende Forschung mit Restzeit. Das ist die Frage, die der Spieler beim Öffnen hat: Was läuft gerade, und wie weit bin ich? Ob mehrere Forschungen gleichzeitig laufen können, ist **UNBEKANNT**. Wenn ja: „läuft: [Anzahl]“ statt des Namens.

---

## E) Der Knopf „Forschen“

**Ja, die Tabelle gilt.** Die Pflicht 4,5 : 1 ist gegen den **schlimmsten** Fall (#483b3a) gerechnet. Jedes gemessene E ist dunkler und hat damit mehr Kontrast. **Rahmen und Sperrfarbe ändern sich nicht.**

**Aber:** Dein E #291b18 stammt aus dem **elfischen Panorama** der Siedlungsansicht. Die Forschung liegt auf der **Bibliothek**. **E muss dort neu gemessen werden**, und zwar unter dem Knopfblock (Block 3) im Bibliotheksausschnitt.

| Teil | Wert |
|---|---|
| Größe | Breite 416, Höhe **40** [a, Startwert]; bei k > 1: 40 × k |
| Grund | E (gemessen unter Block 3) |
| Rahmen | 1 px #b8862e, gebaut als **Frame mit Hintergrund #b8862e und 1 px Innenabstand, darin der Button ohne Rand** (siehe Z3) |
| Text | Creme, 13 fett (× k) |
| Hover | Text in Gold #FFCC33 (≥ 7,10), Grund bleibt E |
| **gesperrt** | Text „✕ Forschen nicht möglich“, **disabledforeground = Creme** (siehe Z3); der Grund steht in Block 6 |
| läuft schon | Text „► läuft – noch [Restzeit]“, gesperrt wie oben |

---

## F) Abnahme ohne Auge

| # | Kriterium | Prüfweg |
|---|---|---|
| 1 | Bei 1037 × 589: 21 Zeilen, je `bbox`-Abstand **26**, Kopfzeile 24, letzte Zeile endet bei **y ≤ 570**, kein Rollbalken sichtbar (`winfo_ismapped` = 0) | `bbox`, `winfo` |
| 2 | Spaltengrenzen 8 / 240 / 248 / 296 / 304 / 368 / 376 / 488 / 496 / 580; **kein Text-`bbox` ragt über seine Spalte** | `bbox` je Textobjekt |
| 3 | Jede Textfarbe ≥ 4,5 : 1 gegen #483b3a **und** gegen 5 Stichpixel unter der Liste im fertigen Bild | Rechnung |
| 4 | Simulierter Klick auf die Mitte jeder Zeile 0 bis 20 wählt genau diese Zeile; ein Klick in der Kopfzeile wählt nichts | `event_generate`, 22 Proben |
| 5 | Gesperrter Knopf: `cget('disabledforeground')` = #F2E3BF, und der Text beginnt mit „✕“ | `cget` |
| 6 | Linke Blöcke: Lücke zwischen zwei Schleierfeldern = 8 (± 0); der Kopf bleibt beim Rollen auf y = 0; 432 und die Formel für S stehen nur in `ansicht_geruest.py` | `bbox`, Stichpixel, AST-Prüfung |
| 7 (Startwert) | Höchstens 150 Canvas-Objekte (erwartet ≈ 130: 105 Zellen + 5 Spaltenköpfe + 1 Linie + 2 Bilder + 2 Rahmen + ≈ 15 Texte links) [r] | `find_all` |

---

## G) Was ich von dir brauche (zum Messen)

1. **Längster Forschungsname** in px bei Arial −13 (`font.measure`). Ist er > 232, braucht die Namensspalte „…“; ab > 260 würde ich die Spalten neu teilen.
2. **Kostenarten je Forschung:** größte Anzahl und das Textformat einer Zeile. Davon hängen Block 2 und die Kostenspalte ab.
3. **Format der Dauer** und größter Wert, als fertiger Text aus `spieloekonomie`.
4. **Höchstzahl der Voraussetzungen** je Forschung und **längste Wirkung** in Zeilen bei Breite 416.
5. **Gleichzeitige Forschungen:** ja oder nein.
6. **Zustandswerte im Code:** Heißen die vier Zustände so? Gibt es weitere, etwa „Stufe maximal“?
7. **Darstellung von ○ ► ✓** in Tk unter Arial −13, mit Breite.
8. **E unter Block 3** und unter der Liste im Bibliotheksausschnitt (52, 265).
9. **Nach einem DPI-Umschalten:** Fläche W × H und die Breiten der Menüspalten.

---

## Was ich nicht geprüft habe

- **Texte:** die echten Namen, Kosten, Dauern und Wirkungstexte der 21 Forschungen (siehe G).
- **Zeichen:** ob ○, ► und ✓ in Tk unter Windows dargestellt werden. Liberation Sans hat alle drei, Arial unter Windows vermutlich nicht alle (Tk weicht dann auf eine andere Schrift aus, wie bei ✕).
- **Menüspalten:** wie stark sie nach einem DPI-Umschalten wachsen.
- **Bibliothek:** wie hell das Bibliotheksbild unter der Liste ist (nur der schlimmste Fall ist gerechnet).

---

## Anmerkungen an Weltenfresser (zusätzlich, nicht beauftragt)

> Hinweise, keine Anweisungen. Bitte prüfen und mir sagen, wo ich falsch liege.

**Z1 Erst die DPI-Frage, dann die zweite Ansicht.** Nach einem Umschalten ändert sich jede Tk-Pixel-Zahl im Register. Wird die Forschung jetzt mit **Formeln** (W, H, k, linespace) gebaut statt mit 1037 / 589 / 26, übersteht sie das Umschalten ohne Umbau. Das ist der wichtigste Punkt dieses Auftrags.

**Z2 Tk-Falle: Klicks auf leere Rechtecke.** Ein Canvas-Rechteck mit `fill=""` (durchsichtig) nimmt Klicks **nur auf seinem Rand** an, nicht innen. Kleine Modelle bauen dafür gern 21 unsichtbare Klickrechtecke und wundern sich, dass nichts passiert. Deshalb: **eine** Bindung auf dem Canvas und die Zeile aus y rechnen (Teil C). Das spart nebenbei 21 Objekte.

**Z3 Tk-Falle: Knöpfe unter Windows.**
- Ein gesperrter `Button` zeichnet seinen Text in `disabledforeground`, standardmäßig **grau**. Den Wert ausdrücklich auf Creme setzen, sonst ist Daniels Regel „nicht ausgrauen“ verletzt, ohne dass es jemand bemerkt.
- Die **Randfarbe** eines Buttons lässt sich unter Windows nicht zuverlässig setzen. Deshalb der Rahmen als umgebender Frame (Teil E).

**Z4 Dein 7-px-Fehler ist eine gute Wache für alle Ansichten.** Die Stichpixel-Prüfung „Spaltenausschnitt = Hintergrundausschnitt“ gehört **in `ansicht_geruest.py`** und läuft damit für jede Ansicht mit. Zum Schnitt des Moduls ein Satz: **Teile es in eine reine Rechenfunktion ohne Tk** (Maße, Schleierrechtecke, E) **und eine Zeichenfunktion.** Die Rechenfunktion lässt sich dann ohne Fenster in Millisekunden prüfen, und das verkürzt eure 35-Minuten-Läufe für diese Wachen.

**Z5 Zwei Zahlen passen nicht zusammen (D5):** **18 Waren** im Spielstand gegen **17 Rezepte** im Register. Möglich ist eine Ware ohne Rezept, etwa ein Rohstoff, oder ein fehlendes Rezept. Bitte nachsehen, bevor das Dorfzentrum mit 18 Kacheln gebaut wird.

**Z6 Vorausgedacht für das Dorfzentrum (18 Waren-Kacheln):**
- Nach Nr. 12 E1 sind es bei R = 588 vier Spalten mit Kacheln von 137 px. 18 Kacheln ergeben **5 Reihen = 5 × 137 + 4 × 8 + 16 = 733 px > 589**; die Arbeitsfläche rollt also.
- Heute sind es 8 Spalten mit Kacheln von 112 × 130 bei 2148 px Inhalt.
- Mit DPI-Umschaltung und größerem H kann sich das ändern. Deshalb auch hier: erst Z1 entscheiden.

---

Ende der Antwort auf Auftrag Nr. 13.
