# ANTWORT AUF AUFTRAG NR. 10: Das Markersystem auf der Weltkarte – baufertig

| | |
|---|---|
| **Antwort auf** | AUFTRAG NR. 10 AN CLAUDE (Klasse Opus 5.5): DAS MARKERSYSTEM AUF DER WELTKARTE — BAUFERTIG |
| **Auftragsdatei** | `AUFTRAG_CLAUDE_MARKER_NR10.md` |
| **Auftrag von** | Hermes Agent „Weltenfresser“, Stand 12.11.2026, 20:2x |
| **Für** | Daniel Kössl |
| **Ort im Spiel** | Portalansicht, Weltkarte 20 × 20 (nicht die Siedlungskarte) |
| **Ersetzt** | Antwort auf Auftrag Nr. 4, Teile B1 bis B6, vollständig. Wo diese Antwort abweicht, gilt diese. |
| **Erarbeitet** | von Opus 5.5 Thinking: Mittel, 12.11.2026 |
| **Umsetzbar für** | `deepseek-v4-flash`, nur Pillow und Tkinter |

**Geprüft:** Alle sechs Formen, der Drache, der eigene Marker und die Auswahl habe ich mit genau diesem Rezept in Pillow auf allen sieben Geländefarben gerendert, bei f = 20, 22, 30 und 46, farbig und in Graustufen. Bei f = 20 sind alle Formen ohne Farbe unterscheidbar.

---

## 0. Begriffe und Farben (gelten überall)

| Zeichen | Bedeutung |
|---|---|
| **f** | Feldgröße in px (20 bis 46) |
| **A** | Größe der Innenform = **f − 4** |
| **S** | die Innenform der Fraktion, in ein Quadrat A × A gezeichnet |
| **S ⊕ n** | S, um n px nach außen gewachsen (mit runden Ecken) |

| Rolle | Farbe | Herkunft |
|---|---|---|
| Halo | **#1a0a09** | Handbuch 1.2 (Leiste) |
| Rand Bot | **#F2E3BF** | Handbuch 1.2 (Text) |
| Rand eigen | **#FFCC33** | Handbuch 1.2 (Gold) |
| Bedroht, feindlicher Marsch | **#ff8a70** | Handbuch 1.2 (Warnung) |
| Ruine | #8A8178 | Antwort Nr. 4 (B5) |
| Fläche je Fraktion | Arbeitswerte Menschen #3F6FC4, Zwerge #9ACFE6, Elfen #5CB04E, Gnome #C8372B, Ghule #7E44A8, Trolle #EEE8D8 | Arbeitswerte. Die Fläche trägt keinen Kontrast und darf durch eure Fraktionsfarben ersetzt werden. |

**Abweichung von Nr. 4:** Gold war dort #E0B040, Orange #E8582A und Halo #2A0605. Hier gelten die Handbuchwerte. Damit kommt keine neue Farbe hinzu.

---

## A) Die Formen als Zahlen

Alle Punkte sind in **0..1 im Quadrat A × A**: x nach rechts, y nach unten, Ursprung links oben. Gezeichnet wird mit Pillow `ImageDraw`. **Je Form gibt es genau eine Zeichenart:**

| Fraktion | Form | Zeichenart | Punkte bzw. Werte | Anzahl |
|---|---|---|---|---|
| Menschen | Schild | `polygon` | (0,000; 0,000) (1,000; 0,000) (1,000; 0,400) (0,950; 0,620) (0,820; 0,800) (0,500; 1,000) (0,180; 0,800) (0,050; 0,620) (0,000; 0,400) | 9 |
| Zwerge | Sechseck, Spitze oben | `polygon` | (0,500; 0,000) (0,933; 0,250) (0,933; 0,750) (0,500; 1,000) (0,067; 0,750) (0,067; 0,250) | 6 |
| Elfen | Kreis | `ellipse` | Rahmen (0; 0) bis (1; 1), also Mittelpunkt (0,5; 0,5) und Radius 0,5 | – |
| Gnome | Quadrat, gerundet | `rounded_rectangle` | (0,06; 0,06) bis (0,94; 0,94), Eckenradius **0,12 × A** | 4 |
| Ghule | Dreieck, Spitze oben | `polygon` | (0,500; 0,040) (1,000; 0,960) (0,000; 0,960) | 3 |
| Trolle | Stern, 5 Zacken | `polygon` | (0,500; 0,048) (0,647; 0,346) (0,976; 0,393) (0,738; 0,625) (0,794; 0,953) (0,500; 0,798) (0,206; 0,953) (0,262; 0,625) (0,024; 0,393) (0,353; 0,346) | 10 |
| Drache und Ruine | Raute | `polygon` | (0,500; 0,000) (1,000; 0,500) (0,500; 1,000) (0,000; 0,500) | 4 |

**Herleitungen:**
- **Stern:** Außenradius 0,5, Innenradius 0,25, Mitte (0,5; 0,548), Winkel ab −90° in Schritten von 36°. Der dicke Innenradius hält die Zacken bei A = 16 lesbar.
- **Quadrat:** Es ist auf 0,06..0,94 eingerückt, damit seine Fläche (0,77) etwa der des Kreises (0,79) entspricht und es nicht schwerer wirkt.

**Wachsen (S ⊕ n) je Zeichenart:**
- `ellipse`: Rahmen um n größer.
- `rounded_rectangle`: Rahmen um n größer, Eckenradius ebenfalls um n größer.
- `polygon`: zuerst gefüllt zeichnen. Dann den Umriss als geschlossene `line` mit Breite 2n und `joint="curve"` nachziehen; dabei die ersten zwei Punkte am Ende wiederholen. Zusätzlich an jedem Eckpunkt eine Scheibe mit Radius n setzen.

**Burg beim großen Marker:** **nur Schmuck.** Die Fraktion trägt immer die Form, bei jeder Stufe. Die Wappenplakette (heute 40 %) entfällt auf der Karte ganz. `data/bot_wappen.json` bleibt unberührt; die Prozentwerte werden nur nicht mehr gelesen.

---

## B) Stufen als Pixelrezept

**Eine Regel für alle Stufen:** Markerhöhe **M = f + 4**, Halo 2 px, Rand 2 px, Innenform A = f − 4. Der Marker steht **mittig auf dem Feld** und ragt **2 px je Seite** über das Feld.

| Stufe | Feld | M | Halo / Rand | A | Inhalt | weggelassen |
|---|---|---|---|---|---|---|
| klein | 20–25 | 24–29 | 2 / 2 | 16–21 | Form mit Fläche | Burg, Wappen |
| mittel | 26–37 | 30–41 | 2 / 2 | 22–33 | Form mit Fläche | Burg, Wappen |
| groß | 38–46 | 42–50 | 2 / 2 | 34–42 | Form mit Fläche, darin die Burg mit **abgerundet(0,75 × A)** = 25–31 px, mittig, **auf die Innenform zugeschnitten** (Maske = S) | Wappen |

**Abweichung von Nr. 4:** Die Wappen-Silhouette beim mittleren Marker entfällt. Es gibt dafür keine Bilddatei, und ein gemaltes Wappen unter 32 px ist Matsch (eure Regel aus Nr. 7).

**Antworten auf die drei Fragen:**
1. Es gilt **f + 4**. Bei 20 px ergibt das **24 px**. Die 26 px aus Nr. 4 waren das Beispiel für f = 22.
2. **Die Burg bleibt nur in der Stufe groß**, als Schmuck.
3. **Der Marker wächst mit:** Bei 46 px Feld ist er **50 px**.

**Bau eines Bot-Markers** (einmal je Fraktion und f, dann im Cache, siehe F):
1. Leeres RGBA-Bild **4 × M** im Quadrat (vierfache Überabtastung). Alle Längen ×4.
2. Zeichnen in dieser Reihenfolge, Versatz 4 px (×4):
   1. S ⊕ 4 in Halo
   2. S ⊕ 2 in Rand
   3. S in Fläche
   4. nur bei Stufe groß: die Burg
3. `reduce(4)` auf M × M. Fertig.

---

## C) Eigener Marker, Auswahl, Bedrohung

**Eigener Marker:** Er hat **dasselbe A** wie ein Bot-Marker dieser Stufe, aber andere Ringe. Gezeichnet in dieser Reihenfolge:
1. S ⊕ 6 Halo
2. S ⊕ 4 Gold
3. S ⊕ 3 Halo
4. S ⊕ 2 Gold
5. S Fläche
6. bei groß: Burg

Damit ist **M_eigen = f + 8** (also +4 gegenüber dem Bot), mit 4 px Überstand je Seite.
- **Ohne Farbe erkennbar:** am **Doppelring** (hell, dunkler Strich, hell). Ein Bot hat einen einfachen hellen Ring.
- Der eigene Marker wird immer **über** fremden gezeichnet (Reihenfolge in E).

**Auswahl:** Außen kommen zwei Ringe hinzu, **zuerst gezeichnet**:
- Halo bei (äußerster Ring + 3),
- Creme #F2E3BF bei (äußerster Ring + 2).

| | Bot | eigen |
|---|---|---|
| ausgewählt, Formel | **f + 10** | **f + 14** |
| bei f = 20 | 30 | 34 |
| bei f = 22 | 32 | 36 |
| bei f = 46 | 56 | 60 |

Der Überstand je Seite beträgt dann 5 bzw. 7 px. Das ausgewählte Objekt wird **zuletzt** gezeichnet.

**Feldrahmen bei Auswahl:** Er liegt **auf der Geländekachel**, unter dem Marker, und besteht aus zwei Rechtecken:
1. außen: 1 px Halo am Feldrand,
2. innen: 2 px Creme.

Creme allein läge auf Steppe bei 1,62 und auf Berg bei 1,81; der Halo darunter macht ihn sichtbar.

**Bedroht:**
- Dreieck mit Spitze oben, Kantenmaß **b = 8 / 10 / 12 px** (klein / mittel / groß).
- Gebaut als Innenform (0,5; 0) (1; 1) (0; 1) mit A = b − 2, **⊕ 1 Halo**, Fläche #ff8a70.
- **Anker:** Die rechte obere Ecke des Abzeichens liegt genau auf der rechten oberen Ecke des **Grundmarkers** (M × M, ohne Auswahlringe), also um **0 px** verschoben.
- Es **vergrößert den Marker nicht**. Es ist ein eigenes Bild, über dem Marker gezeichnet.

---

## D) Marsch, Drache, Ruine

**Märsche als ein Pillow-Bild:**
- Alle laufenden Märsche kommen in **ein** RGBA-Bild in Kartengröße. Es ist **ein einziges** Canvas-Objekt und wird nur neu gebaut, wenn ein Marsch beginnt oder endet oder sich f ändert.
- Grund: Unter Windows zeichnet Tk die Strichelung breiter Linien möglicherweise nicht (UNBEKANNT, bitte prüfen). Mit Pillow ist sie unabhängig davon.

| Teil | Rezept |
|---|---|
| Ummantelung | Linie in Halo, **5 px**, **durchgehend**, auch beim feindlichen Marsch |
| eigener Marsch | darauf eine Linie in Creme, 3 px, durchgehend |
| feindlicher Marsch | darauf Orange #ff8a70, 3 px, **gestrichelt 8 px an / 6 px aus**, gemessen entlang der Linie ab dem Start |
| Ende der Linie | im Abstand **Ziel-M / 2** vor der Zielmitte |
| Spitze | gefülltes Dreieck. Länge t = **10 / 12 / 14** (klein / mittel / groß), Breite 8 / 10 / 11, Farbe wie die Linie, 1 px Halo-Umriss. Die Spitze liegt am Linienende. |
| Start | Quadrat **6 px** in der Linienfarbe, 1 px Halo-Umriss |

**Zur Strichelung:** 6 an / 4 aus mit gestricheltem Halo wäre zu eng. Die Lücken würden Gelände zeigen, und die Linie zerfiele. Mit **durchgehendem Halo und 8 / 6** wechseln Orange und Dunkel deutlich, auch in Graustufen.

**`data/marsch_optik.json`:** Die Zahlen gehören dort hinein, **wenn es passende Schlüssel schon gibt** (Breite, Farbe, Strich). Welche Schlüssel es gibt, ist UNBEKANNT. Neue Schlüssel nur nach Daniels Zustimmung.

**Drache und Ruine:** Raute aus A, mit denselben Ringen wie ein Bot (S ⊕ 4 Halo, S ⊕ 2 Creme), also M = f + 4.
- Diagonale = A, **Kantenlänge = 0,707 × A**: klein 11,3 bis 14,8 px, mittel 15,6 bis 23,3 px, groß 24,0 bis 29,7 px.
- **Drache:** Fläche #1a0a09. Ab mittel kommt ein Flügelwinkel in Creme dazu, als `polygon` in 0..1: (0,20; 0,45) (0,50; 0,62) (0,80; 0,45) (0,80; 0,58) (0,50; 0,78) (0,20; 0,58).
- **Ruine:** Fläche #8A8178. Ab mittel kommt ein gebrochener Turm in #1a0a09 dazu: (0,40; 0,75) (0,40; 0,42) (0,47; 0,36) (0,53; 0,45) (0,60; 0,38) (0,60; 0,75).

**Mini-Raute** (Dorf und Drache auf einem Feld):
- Raute mit A = 6, ⊕ 1 Creme, ⊕ 2 Halo, also **10 px** groß.
- Ihre linke untere Ecke liegt auf der linken unteren Ecke des Grundmarkers.
- **Sie liegt über dem Dorfmarker und verschiebt ihn nicht.**

---

## E) Treffer, Reihenfolge, Reiter

**Trefferfläche = das Feld (f × f), nichts sonst.** Feld = (x // f, y // f), gerechnet ab dem Ursprung der Karte. Der Überstand eines Markers ist nicht anklickbar. So trifft ein Klick immer genau ein Feld.

**Priorität beim Klick** (kleinste Zahl gewinnt):

| Objekt | Zahl |
|---|---|
| eigenes Dorf | 1 |
| fremdes Dorf | 2 |
| Drache oder Ruine | 3 |

Das Marschziel ist kein eigenes Objekt; es ist das Dorf. „Ausgewählt“ ist ein Zustand, keine Priorität.

**Zeichenreihenfolge** (unten nach oben). Innerhalb einer Ebene wird zeilenweise von oben nach unten gezeichnet:
1. Gelände
2. Feldrahmen der Auswahl
3. Marschbild
4. Drache und Ruine (nur auf Feldern ohne Dorf)
5. fremde Dörfer
6. eigene Dörfer
7. Mini-Rauten
8. Bedroht-Abzeichen
9. das ausgewählte Objekt mit seinen Auswahlringen (`tag_raise`)

**Reiter:** **höchstens 2.** Kein Feld trägt zwei Dörfer (eure Angabe), und Drache und Ruine sind dasselbe Objekt vor bzw. nach dem Sieg. Märsche belegen kein Feld. Ob ein Drache auf einem Dorffeld stehen kann, ist UNBEKANNT. Kann er es nicht, gibt es nie Reiter.

---

## F) Leistung

**Formen als Pillow-Bild im Cache, nicht als Canvas-Polygon.** Begründung:
- Ringe mit gleichmäßiger Breite und geglättete Kanten gehen nur so.
- Ein Marker kostet damit **ein** Canvas-Objekt.
- Die Bilder werden **in Zielgröße gebaut**, mit vierfacher Überabtastung und `reduce`. Es wird also kein gemaltes Bild nachträglich vergrößert.
- **Einzige Ausnahme:** Die Burg (Stufe groß) wird einmal aus `assets/icons/burgen/` mit LANCZOS verkleinert. **Daniel bestätigt bitte**, dass Register 502 („nie skalieren“) für Marker nicht gilt.

**Cache-Schlüssel:** (Form, f, bot/eigen, ausgewählt ja/nein). Dazu je f ein Bedroht-Abzeichen und eine Mini-Raute.
- Bei einem Wechsel von f wird der Cache geleert und nur das Gebrauchte neu gebaut. Das sind höchstens 6 × 2 × 2 (Fraktionen) + 2 × 2 (Drache, Ruine) + 2 (Abzeichen, Mini-Raute) = 30 Bilder.
- Die Bildobjekte müssen im Cache gehalten werden, sonst verschwinden sie unter Tkinter.

**Höchstzahl an Canvas-Objekten je Marker:**

| Fall | Objekte |
|---|---|
| Dorf, normal | **1** |
| bedroht | 2 |
| mit Mini-Raute | 3 |
| ausgewählt (Marker mit Ringen, 2 Feldrahmen, Abzeichen, Mini-Raute) | **höchstens 5** |
| Märsche zusammen | 1 |

Bei 20 Dörfern sind das höchstens rund 45 Objekte für alle Marker. Heute sind es 232 Objekte je Karte einschließlich Gelände.

---

## G) Abnahme mit Zahlen

| # | Kriterium | Wert | Prüfweg |
|---|---|---|---|
| 1 | Sechs Formen bei M = 24 (f = 20) ohne Farbe unterscheidbar | ja (von mir gerendert) | Sicht, Graustufen |
| 2 | Halo #1a0a09 gegen Kachel ≥ 3 | Grasland 7,08 · Steppe 9,60 · **Wald 3,22** · Hügel 5,57 · Berg 8,57 · Nebelsee 5,07 · Sumpf 4,09 | Rechnung |
| 3 | Rand gegen Halo; Gold gegen Halo; Warnung gegen Halo; Ruine gegen Creme | 15,13 · 12,77 · 8,36 · 3,01 | Rechnung |
| 3b | Fläche gegen Creme (keine Pflicht, die Form trägt) | Menschen 3,86 · Zwerge 1,33 · Elfen 2,12 · Gnome 4,09 · Ghule 5,04 · Trolle 1,04 | Rechnung |
| 4 | Überstand je Seite höchstens: Bot 2, eigen 4, ausgewählt 5 / 7 px; Nachbarmarker überlappen höchstens um 4 bzw. 8 px | wie angegeben | Messung |
| 5 | Eigener Marker in Graustufen am Doppelring erkennbar | ja (von mir gerendert) | Sicht |
| 6 | Feindlicher Marsch in Graustufen an der Strichelung 8 / 6 erkennbar | – | Sicht |
| 7 | Klick: Feld = (x // f, y // f), dann das Objekt mit der kleinsten Prioritätszahl | – | Messung |
| 8 | Canvas-Objekte je Marker höchstens 5, normal 1 | – | `find_all` zählen |

**Wichtig zu G2:** Diese Werte gelten **nur mit der Geländepalette aus Antwort Nr. 4, Teil A3**. Mit der alten Palette liegen Wald (1,83), Sumpf (2,10), Nebelsee (2,69) und Hügel (2,77) unter 3. Ob `data/gelaende.json` schon die neue Palette hat, ist **UNBEKANNT**.

---

## Was ich nicht geprüft habe

- **Echtes Programm:** Ich habe die Formen nur in Pillow gerendert, nicht im laufenden Tkinter-Fenster bei 125 %.
- **Strichelung:** Ob Tk unter Windows breite Linien gestrichelt zeichnet. Das ist durch das Pillow-Marschbild umgangen, aber nicht geprüft.
- **Daten:** Die Schlüssel von `data/marsch_optik.json`, die echten Fraktionsfarben in den Daten und ob `data/gelaende.json` die neue Palette trägt.
- **Burg:** Wie die Burgbilder bei 25 bis 31 px aussehen. Das prüft Daniel mit dem Auge.
- **Drache:** Ob ein Drache auf einem Dorffeld stehen kann.
- **Cache:** Wie lange der Aufbau bei einem Wechsel von f dauert. Bitte messen.

---

## ZUSATZINFORMATIONEN (nicht beauftragt, von Claude ergänzt)

> **Hinweis für Weltenfresser:** Dieser Abschnitt stand nicht im Auftrag. Er enthält Dinge, die beim Bauen leicht übersehen werden. Alles ist **Empfehlung**, nichts davon ändert die Teile A bis G. Wo „Verdacht“ steht, ist es nicht geprüft.

### Z1 Verdacht: Unschärfe durch Windows-Skalierung (wichtig, auch für T08 und alle Schriften)

- **Befund:** Daniels Bildschirm ist 1920 × 1080 bei 125 %, das Programm misst aber „1536 × 864 logisch“.
- **Verdacht:** Das deutet darauf hin, dass das Programm **nicht DPI-aware** ist. Dann vergrößert Windows das ganze Fenster nachträglich als Bitmap um 1,25. **Alles wird weich**: Schrift, Marker, Kacheln. Pixelgenaue Marker würden dann unscharf, egal wie gut sie gebaut sind. Das könnte zu Daniels Befunden „hässlich“ und „Stil komplett weg“ beitragen.
- **Prüfung:** Ein Rechteck von genau 100 px zeichnen und ein Bildschirmfoto in voller Auflösung machen.
  - Ist es **125 px breit mit weichen Kanten**, trifft der Verdacht zu.
  - Ist es **100 px breit und scharf**, ist alles in Ordnung.
- **Wenn er zutrifft:** Das ist eine Entscheidung für Daniel. Wird das Programm DPI-aware geschaltet, ändern sich **alle gemessenen Flächen** (×1,25). Fenster und Flächen müssten dann neu gemessen werden.

### Z2 Fraktionsnamen: Zuordnung genau so übernehmen

Die Namen in `data/voelker.json` lauten anders als in dieser Antwort:

| Name in den Daten | Fraktion in dieser Antwort | Form |
|---|---|---|
| menschlich | Menschen | Schild |
| zwergisch | Zwerge | Sechseck |
| elfisch | Elfen | Kreis |
| Gnome | Gnome | Quadrat |
| Ghule | Ghule | Dreieck |
| Trolle | Trolle | Stern |

Die genaue Schreibweise der Schlüssel in der Datei ist **UNBEKANNT**, bitte nachsehen. Eine falsche Zuordnung fällt sonst erst im Spiel auf.

### Z3 Ganze Pixel, kein Runden nötig

M = f + 4 hat dieselbe Gerade/Ungerade-Eigenschaft wie f. Die linke obere Ecke eines Markers liegt deshalb immer **ganzzahlig** relativ zur linken oberen Ecke seines Feldes:

| Marker | Versatz in x und y |
|---|---|
| Bot | −2 |
| eigen | −4 |
| Bot, ausgewählt | −5 |
| eigen, ausgewählt | −7 |

Mit diesen festen Werten muss nicht gerundet werden. Bitte nicht über „Mitte − M/2“ rechnen.

### Z4 Pillow: drei Fallen

1. **Pillow-Version prüfen** (`PIL.__version__`). `rounded_rectangle` braucht mindestens 8.2 und `reduce` mindestens 7.0. Ich habe mit Pillow 12.3 gerendert.
2. **Burg einsetzen (Stufe groß):** Die Burg zuerst auf 4 × Zielgröße bringen, dann einsetzen und erst danach `reduce(4)` auf das Ganze anwenden. Als Maske dient die Burg-Transparenz **multipliziert** mit der Maske der Innenform (`ImageChops.multiply`). Sonst steht die Burg über den Ring hinaus.
3. **`ImageDraw` mischt nicht, es überschreibt.** Das ist hier gewollt, denn jede Schicht ist deckend. Die weichen Kanten entstehen erst durch `reduce(4)`. Nicht zusätzlich weichzeichnen.

### Z5 Tkinter: drei Fallen

1. **Bildobjekte festhalten:** Jedes `ImageTk.PhotoImage` muss in einer Liste oder einem Dict gespeichert bleiben, solange es angezeigt wird. Sonst ist der Marker **unsichtbar**, ohne dass eine Fehlermeldung erscheint. Das ist der häufigste Tkinter-Fehler.
2. **Klick bei gerollter Karte:** Die Klickkoordinate muss erst mit `canvasx` / `canvasy` umgerechnet werden. Dann wird der Kartenursprung abgezogen (gibt es eine Koordinatenleiste? UNBEKANNT). Erst danach wird durch f geteilt.
3. **Nicht alles neu zeichnen:** Jedes Objekt bekommt einen Tag, zum Beispiel `marker`, `auswahl`, `marsch`. Bei einem Auswahlwechsel werden nur die Objekte mit dem Tag `auswahl` gelöscht und neu gesetzt. Die Karte bleibt stehen. Das senkt die Kosten pro Klick von „alles“ auf 2 bis 5 Objekte.

### Z6 Marschbild: zwei Fallen

1. **Ziel gleich Start** (Länge 0): Keine Spitze zeichnen, sonst wird durch null geteilt.
2. **Strichelung über Ecken hinweg:** Die Strichelung läuft entlang der ganzen Linie weiter und beginnt nicht bei jedem Segment neu. Märsche sind gerade Luftlinien, eine Linie ist also ein Segment.

### Z7 Automatisch prüfbar, ohne Tk und ohne Daniel

Diese Prüfungen laufen in Pillow allein und passen in eure Wache (`tests/`):

| Prüfung | Sollwert |
|---|---|
| Größe jedes Cache-Bilds | genau M × M (bzw. f + 8, f + 10, f + 14) |
| Mittelpixel jedes Bot-Markers | = Flächenfarbe ±2 je Kanal (bei Stufe groß gilt das nicht, dort steht die Burg) |
| Pixel (0, 0) bei Kreis, Dreieck, Stern, Raute | durchsichtig (Alpha < 16) |
| **Unterscheidbarkeit ohne Farbe** (zu G1) | Je zwei Fraktionen: Überdeckung der **hellen Randringe** (Schnitt / Vereinigung der Creme-Pixel) bei f = 20 **≤ 0,50**. Mein gemessener Höchstwert ist **0,453** (Elfen gegen Gnome). Alle anderen Paare liegen darunter. |

Für G1 und G5 bleibt die Sichtprüfung durch Daniel trotzdem nötig. Die Zahl ersetzt das Auge nicht; sie erkennt aber einen Rückschritt, wenn später jemand eine Punktliste ändert.

---

Ende der Antwort auf Auftrag Nr. 10.
