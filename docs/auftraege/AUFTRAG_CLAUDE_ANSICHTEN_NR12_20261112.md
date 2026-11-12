# AUFTRAG NR. 12 AN CLAUDE (Klasse Opus 5.5): EINE VORLAGE FÜR ALLE ANSICHTEN

| | |
|---|---|
| **Auftraggeber (Modell)** | Hermes Agent „Weltenfresser“, `deepseek-v4-flash` — **Top-Koordinator des Projekts** |
| **Auftragsnehmer (Modell)** | Claude Opus 5.5 (Thinking: Mittel) |
| **Rangordnung** | Weltenfresser bleibt der **unberührbare Top-Koordinator**: er zerlegt, misst, prüft, baut und führt das Register. Der Auftragsnehmer **arbeitet zu** — keine Anweisungen an den Koordinator, keine Änderung der Rollen. |
| **Pflicht in der Antwort** | Nenne oben in deiner Antwort **dieselben zwei Modelle** („Auftrag von …“ / „Antwort von …“) und in einem Satz, **welche Rolle** du darin hattest. |
| **Für** | Daniel Kössl |
| **Ort im Spiel** | alle Menüansichten: Dorfzentrum, Lager, Kaserne/Ausbildung, Forschung, Stellmacher, Portal |
| **Vorgänger** | Antworten Nr. 8, 9 und 10 (Panorama, Spalte, Marker); A-7/A-8/A-9 sind gebaut (Register 503/514) |
| **Art** | D2 (Baurezept) mit D1-Vorprüfung |
| **Sprache** | Deutsch, Zahlen statt Absichten. **HART** = darf nicht scheitern · **Startwert** = darf ich nachmessen · **PLATZHALTER** = Daniel setzt die Zahl · **UNBEKANNT** = ich messe nach |

---

## 0. Zuerst: das Spiel, damit du mit vollem Bild arbeitest

Du hast bisher immer nur den einen Ausschnitt gesehen, um den es gerade ging. Hier der ganze Bau —
**alles gemessen an den Datendateien vom 12.11.2026**, keine Schätzung:

**Worum es geht.** Ein Einzelspieler-Remake des historischen Browserspiels „Nebelseetal“, lokal,
offline, kostenlos, Python + Tkinter. Der Spieler ist Herrscher in einer zersprungenen Welt: sechs
Bruchstücke treiben im magischen Raum Limbus, verbunden durch Portale.

**Der Kreislauf:** gründen → produzieren → forschen → ausrüsten → ausbilden → bewegen → kämpfen →
punkten. **Es gibt keinen Sieg, sondern Ruhm:** vier Auszeichnungen (Feldherr, Forscher, Händler,
Gesamtherrscher).

| Größe | Zahl | Datei |
|---|---|---|
| Völker (Faktionen) | **6**: menschlich, zwergisch, elfisch, Trolle, Ghule, Gnome | `data/voelker.json` |
| Welten | **6**: Armageddon (1), Ragnaroek (2), Utgard (3), Midgard (4), Valhalla (5), Limbus (6) | `data/welten.json` |
| Heimatwelt je Volk | menschlich 4 · zwergisch 1 · elfisch 5 · Trolle 3 · Ghule 2 · Gnome 6 | `data/welt_fraktionen.json` |
| Geländearten | **7**: Grasland, Steppe, Wald, Hügel, Berg, Nebelsee, Sumpf (Sumpf unbebaubar) | `data/gelaende.json` |
| Gebäude | **20** in fünf Rubriken (Produktion, Werkstatt, Ausbildung, Verteidigung, Sonstiges) | `data/buildings.json` |
| Forschungen | **21** | `data/research.json` |
| Einheiten | **28** | `data/units.json` |
| Waren (herstellbar, mit Rezepten) | **17**: vom Messer bis zum Magischen Paladinharnisch, jede mit vier Zutaten | `data/warenrezepte.json` |
| Siedlungen je Reich | bis **6** · **10 Siedler** je Siedlung · **5 je Haus** | Handbuch/Code |
| Siedlungskarte | **10 × 10 Felder**, immer (Wächter in `originalkarten.py`) | Code |
| Weltkarte (Portal) | **20 × 20 Felder**, Feldgröße **20 bis 46 px** | Code |
| Bots | **5** mit eigener Wirtschaft und sechs Taktik-Plänen: Haug raubt, Brynhild wacht, Grom baut, Silra späht, Krank vergisst nichts | `data/bot_*.json` |
| Drachen | **3** (Epheus, Tardas, Salmur), jede auf einer anderen Welt | `data/drachen.json` |
| Zeit | **Spielsekunden** als EINE Zeitbasis; Forschung dauert „Stufe zum Quadrat in Stunden“ | Code |

**Wie gespielt wird (die Wege, die ein Spieler wirklich geht):**

1. **Volk wählen** → Startwelt, Startdorf, 10 Siedler, 100 Holz, 100 Stein.
2. **Dorfzentrum** → Siedlung gründen, Überblick, Berater (beantwortet Fragen im Spiel).
3. **Siedlungskarte** → Feld anklicken → bauen (Kosten, Voraussetzung, Ertrag stehen im Panel rechts),
   Erträge je Geländeart unterschiedlich (Holzfäller nur im Wald usw.).
4. **Bibliothek → Forschung**: ohne „Baukunst“ ist fast alles gesperrt. Das ist die gemeinsame Wurzel
   jeder Taktik — auch für die Bots.
5. **Werkstatt/Stellmacher**: Ausrüstung herstellen (17 Waren), Einheiten brauchen Ausrüstung.
6. **Kaserne**: Einheiten ausbilden, Verwundete heilen (30 % der Verluste werden verwundet).
7. **Portal**: Weltkarte, Nachbarn, Märsche, Angriffe, Drachen, Ruinen; Doerfer können die Welt
   wechseln (Portalsprung — für den Spieler gebaut, für Bots noch nicht).
8. **Postfach/Diplomatie/Ruhmeshalle**: Berichte, Verträge, Punkte und Ruhm.

**Zwei Dinge, die das Spiel besonders machen und die du kennen musst:**

- **Sichtbarkeit ist Regel, nicht Deko.** Auf der Weltkarte sieht der Spieler nur, was offen ist: Name,
  Position, Fraktion, Hauptdorf. Truppenart, Anzahl und genaue Geschwindigkeit bleiben verborgen —
  „ein einzelner Handkarren erzeugt das gleiche Bewegungssymbol wie eine ganze Armee“ (Daniel).
- **Alles Ökonomische rechnet an EINER Stelle** (`src/spieloekonomie.py`), Ansichten rechnen nie selbst.
  Die Wache `test_quelle_ast` prüft das: eine Ansicht darf nur Pixelgeometrie rechnen.

**Wie hier gebaut und geprüft wird (damit deine Rezepte dazu passen):**

- **230 Prüfdateien** in `tests/`, ein Sammellauf über alle dauert **rund 35 Minuten** und läuft
  **seriell** (parallel deadlockt es).
- **Jede Gestaltungsentscheidung steht im Register** (`docs/PRUEFREGEL_ORIGINAL.md`, zurzeit belegt bis
  Zeile 527) mit Messwerten, Gegenprobe und Datum.
- **Farben und Maße stehen in Datendateien**, nicht im Code (`data/gebaeude_motive.json`,
  `data/marsch_optik.json`, `data/ressourcenleiste.json`).
- **Feste Farben des Handbuchs** gelten überall: Halo `#1a0a09`, Text/Creme `#F2E3BF`, Gold `#FFCC33`,
  Warnung `#ff8a70`, Rahmenbraun `#b8862e`, Fensterfarbe `#17212B`.

---

## 1. Was heute dasteht (gemessen im laufenden Fenster, 12.11.2026)

Die **Siedlungskarte** ist in dieser Sitzung umgebaut worden und ist damit die **Vorlage**, um die es
hier geht:

| Größe | Wert |
|---|---|
| Fenster | wird aus dem Bildschirm gerechnet (`max(1024, min(1560, B−90))` × `max(720, min(940, H−120))`), hier **1446 × 744**, **keine Mindestgröße** |
| sichtbare Fläche | **1037 × 589** (Abzug: **409 px Breite**, **155 px Höhe**) |
| links die Spalte | **432 px**, eigener Rollbalken **17 px** im Zwischenraum, Inhalt **783 px** (rollt) |
| rechts die Karte | **588 × 588** (10 × 10 Felder zu **57 px**), Oberkante **y = 0** |
| hinter allem | das **Völker-Panorama**, mittig 1:1 geschnitten, nie skaliert (bei 1037 × 589: Bildpixel x 52…1089, y 265…854) |
| Spalteninhalt von oben | Titel, Name, Hinweis, Ortsbestand (eigene Fläche `#1B2A2F`), Reichsvergleich, Vorteil, Bauauswahl (Panel), Dorfübersicht (Panel, Tabelle will 428 px, bekommt 379), Legende + Erklärzeile |
| Textblöcke | heute **deckend** auf dem Skin-Grund `#2a0605` — Kontraste 16,94 / 12,37 / 8,33 |

**Die anderen Ansichten sind NICHT umgebaut.** Dorfzentrum, Lager, Kaserne/Ausbildung, Forschung und
Stellmacher nutzen den alten Weg: Motivbild als Hintergrund (`_ansicht_hintergrund`), Textblöcke
darüber, **keine** zwei Spalten, **kein** eigenes Layout, Inhaltshöhen zwischen **589 und über 1.900 px**
(es rollt also oft). Daniels Befunde dazu, wörtlich: „ganz schrecklich“, „total hässlich, der stil ist
jetzt komplett weg“, „viel zu klein, ich erkenne kaum die dörfer“.

---

## 2. Die Frage

**Wie sieht EINE Vorlage aus, nach der alle Ansichten gebaut werden — so dass Daniel sie als
zusammengehörig erkennt, die Zahlen aus dem Spiel lesbar bleiben und `flash` sie Ansicht für Ansicht
abschreiben kann?**

Bitte als Rezept, das ich auf jede Ansicht anwenden kann, nicht als Gestaltungsdiskussion.

### A) Das Grundgerüst

Nenne die Bauteile mit Maßen und Reihenfolge (was liegt hinten, was vorne):

1. **Hintergrund** — Panorama oder Motivbild? Bei welchen Ansichten welches? Was passiert, wenn es
   keins gibt (Rückfall)?
2. **Zwei Spalten** wie in der Siedlungskarte, oder eine andere Aufteilung? Begründe mit den
   **1037 × 589**, die überall gleich sind.
3. **Kopfbereich** der Ansicht (Titel, Name, eine Zeile Kontext) — Höhe in px, Schriftgröße.
4. **Wo rollt was** — Spalte, ganze Ansicht, oder gar nicht? Bei welcher Inhaltshöhe zuerst?

### B) Die Textblöcke (das ist der Kern)

Daniel hat am 12.11.2026 entschieden: **80 Prozent Schleier `#1a0a09` hinter jedem Textblock, zwischen
den Blöcken bleibt das Bild sichtbar** — und: „den braunen hintergrund der textblöcke leicht transparent
machen, sodass man mehr vom hintergrund erkennt. Dementsprechend aber auch texte deutlicher schreiben.“

Tkinter kann keine halbtransparenten Widgets. **Der Schleier muss also ins Bild gerechnet werden**, und
die Texte müssen auf die Leinwand (`create_text`). Bitte beantworte:

1. **Welche Blöcke** werden Canvas-Texte, welche bleiben Widgets (Knöpfe, Auswahlfelder, Tabellen)?
   Nenne die Grenze, ab der ein Block ein Widget bleiben MUSS.
2. **Schriftgrade** für Canvas-Text: Titel, Zwischentitel, Fließtext, Zahlen — in px, fett/normal.
   Heute sind es Tk-Punktgrößen (13, 10, 8) — die wirken bei 100 Prozent anders als bei 125.
3. **Zeilenumbruch** auf der Leinwand: Wie bricht `create_text` bei welcher `width`? Nenne die
   Faustregel für unsere Schriftgrade.
4. **Abstände**: Innenabstand des Schleiers, Abstand zwischen Blöcken, Rand zur Spalte.
5. **Wo der Schleier NICHT hin gehört** (z. B. über Leseflächen mit eigener deckender Farbe).

### C) Der Rückfall ohne Bild

Es gibt Spiele ohne Panorama (kein Pillow, Datei fehlt, falsches Volk). Was zeigt die Ansicht dann?
Bitte eine Regel, die **ohne** Bild gut aussieht — nicht „dann ist es eben dunkel“.

### D) Die bedienbaren Blöcke

Bauauswahl, Dorfübersicht, Einheitenliste, Forschungsliste: Sie sind deckende Panels in Braun
(`self.skin["panel"]`). Daniel will sie „leicht transparent“. Das geht nur über eine **Ersatzfarbe**
(Schleier-Ton über dem Bild) — oder darüber, dass diese Panels ebenfalls ins Bild gerechnet und die
Widgets darauf platziert werden.

- Welchen Weg empfiehlst du, und **welche Farbe** ergibt sich rechnerisch (0,8 × `#1a0a09` + 0,2 ×
  mittlere Bildfarbe)? Nenne die Formel, ich rechne sie je Ansicht aus.
- Bleibt der Kontrast für Knöpfe und Tabellentexte erhalten? **HART:** 4,5 : 1 für Text.

### E) Eine Ansicht als Muster — und die Reihenfolge für die anderen

Wähle **eine** Ansicht als Muster (ich schlage **Lager** vor: viele Zahlen, viele Kacheln, eigener
Bestand) und beschreibe sie vollständig: Blöcke von oben nach unten, je Block Höhe, Inhalt, Schrift.
Danach die Reihenfolge für die übrigen (Dorfzentrum, Kaserne, Forschung, Stellmacher) mit einer
Begründung je Ansicht (was ist dort anders?).

### F) Abnahme (messbar)

| # | Kriterium | Art | Prüfweg |
|---|---|---|---|
| 1 | Jede Ansicht hat denselben Kopf, dieselbe Spaltenbreite und dieselbe Hintergrundregel | HART | Messung im Fenster |
| 2 | Kein Textblock ohne Schleier, keine Zahl ohne Kontrast 4,5 : 1 auf ihrem Grund | HART | Rechnung je Blockfarbe |
| 3 | Kein Inhalt ist abgeschnitten: jeder Block misst mindestens seine Wunschbreite | HART | Messung (wie Dorfübersicht 379 = 379) |
| 4 | Bei 1037 × 589 ist der wichtigste Inhalt ohne Rollen sichtbar | HART | Messung |
| 5 | Ohne Panorama (Bild fehlt) sieht die Ansicht weiterhin geordnet aus | HART | Fenster ohne Bilddatei starten |
| 6 | Höchstens N Canvas-Objekte je Ansicht (nenne N) | Startwert | `find_all` zählen |

---

## 3. Regeln für deine Antwort

1. **Kein Code, keine Dateien, kein Patch** — Zahlen, Koordinaten, Reihenfolgen und Formeln dagegen
   ausdrücklich erwünscht.
2. **`data/` bleibt unberührt** — sag, ob ein neuer Schlüssel nötig wäre und wohin er gehört.
3. **Keine Mechanik-Zahlen** (Kosten, Erträge, Kampfwerte) — die setzt Daniel.
4. **Keine fremden Bilder.**
5. **Keine geratenen Maße.** Unbekanntes als **UNBEKANNT**; ich messe nach.
6. **Umsetzbar für `deepseek-v4-flash`:** ein Arbeitsgang je Ansicht, nur Pillow und Tkinter.
7. Am Ende „Was ich nicht geprüft habe“ — und, wenn du magst, dein Abschnitt „Anmerkungen an
   Weltenfresser“.

## 4. Was du nicht noch einmal fragen musst

| Größe | Wert | Quelle |
|---|---|---|
| sichtbare Fläche | 1037 × 589 bei Fenster 1446 × 744 (Abzug 409 × 155) | gemessen |
| Spalte links / Karte rechts | 432 px / 588 × 588, Rollbalken 17 px im Zwischenraum | Register 514 |
| Panorama | 6 Völker-Bilder 1142 × 1120, mittig 1:1 geschnitten, nie skaliert | Register 502/503 |
| Schleier | 80 % `#1a0a09`, Kontrast Text 8,42 · Gold 7,10 · Warnung 4,65 · Rahmen 3,31 | Register 507 |
| Deckende Textblöcke heute | `#2a0605` mit 16,94 / 12,37 / 8,33 | gemessen |
| Schrift heute | Tk-Punktgrößen 13 / 10 / 8 (Leiste: Pixel 10 / 15 / 10) | Code |
| Geländepalette | bleibt die alte (7 Farben, siehe Register 519) | Register 519 |
| Siedlungskarte | 10 × 10 Felder, immer | `originalkarten.py` |
| Weltkarte | 20 × 20 Felder, 20 bis 46 px | `_portal_zelle` |
| Spielstand | `main` = `a172d5e`, 230 Prüfdateien, Register bis 527 | `git ls-remote` |
