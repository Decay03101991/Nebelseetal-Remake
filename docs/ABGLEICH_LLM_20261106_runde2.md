# Abgleich Runde 2 - vier Gegenprüfungen des festen Ablaufs (06.11.2026)

**Eingang:** `docs/eingaenge/LLM_20261106_runde2/` (vom Desktop geräumt, Hashes beidseitig gleich,
Desktopfassung im gitignorierten `archiv/eingaben/LLM_Antworten_Runde2_20261106/`).

| Datei | SHA256 (Anfang) | Umfang |
|---|---|---|
| `Nebelseetal_Gegenpruefung_Runde2_GPT-6_20261106.md` | `a23b43ced92c7a01…` | 20.205 Byte, 8 Teile |
| `Grok4.5_Antwort_Runde2.odt` | `bed9bf435fe11e3211…` | 12.527 Byte, Wachentabelle über alle 13 Schritte |
| `Collaborator_Antwort_Runde2.odt` | `c1f3d8fc059bb4f29e…` | 25.564 Byte, Wachentabelle über alle 13 Schritte |
| `Gemini_Antwort_Runde2.odt` | `26bf86171c46d34617…` | 10.260 Byte, knappste Fassung |
| `Nebelseetal_LLM_Auftrag_Runde2_20261106.md` | `e5f5237711513cfe…` | identisch mit `docs/extern/…` (hashgleich) |

**Verfahren (weiterentwickelt gegenüber Runde 1):** Jede Behauptung wird am HEUTIGEN Code oder am
Ablaufdokument nachgemessen, nicht übernommen. Urteil je Behauptung: **BESTÄTIGT** (messbar richtig),
**WIDERLEGT** (messbar falsch), **TEILWEISE** (Kern richtig, Begründung falsch) oder **OFFEN**
(Designfrage, keine Messung möglich). Nichts wird eingebaut, was nicht vorher belegt ist.

---

## 1. Der schwächste Schritt

| Modell | Antwort | Begründung in einem Satz |
|---|---|---|
| GPT-6 | **9** (Regelkreis) | Ein formell korrektes A/B-Urteil kann eine falsche Balancing-Entscheidung erzeugen; zehn feste Startwerte sind nicht repräsentativ. |
| Gemini | **4** (Rachetopf) | Topf voll, Bot-Armee aber unter 99 SK: Zähler und Bedingung blockieren sich, die Ankündigung hängt. |
| Grok 4.5 | **7** (Bot-Lücken) | Drei Verhaltenswege in einem Schritt, höchster Aufwand, Doppelauslöser Rache + Drache in derselben Spielstunde. |
| Collaborator | **7** | Zustandsautomat kann im Zustand "warte auf Spionage" dauerhaft einfrieren; die Wache prüft nur, DASS ein Auftrag entsteht. |

**Nachgemessen und entschieden:** Die drei Fehlerbilder sind alle möglich, aber sie sind nicht
gleich teuer. Ein hängender Rachetopf (Gemini) ist ein Spielfehler, den die Kennzahl
`abstand_meilensteine_max` sichtbar macht. Ein eingefrorener Bot (Collaborator) und ein
Doppelauslöser (Grok) sind Fehler im Botverhalten, die ein voller Sammellauf nicht findet, weil
beide Wege erst nach Schritt 4 und 5 zusammenwirken. Am teuersten ist GPTs Punkt: Schritt 9 kann
eine ÄNDERUNG ANNEHMEN, die das Spiel schlechter macht - dort entsteht ein falscher Beschluss, nicht
nur ein Fehler.

**Folge für den Ablauf (übernommen):**
* Schritt 7 bekommt eine Wache "gleicher Spieltick": Racheauslöser und normale Bot-Taktik dürfen
  zusammen höchstens einen Auftrag und eine Ankündigung erzeugen (Grok + GPT).
* Schritt 7 bekommt eine Wache "kein Einfrieren": nach einem Spionageauftrag muss der Raubzug im
  nächsten Takt weiterlaufen (Collaborator).
* Schritt 9 bekommt die Regel: **eine Annahme gilt erst, wenn ein ZUSÄTZLICHER, nicht in der
  A/B-Gruppe enthaltener Startwert nicht schlechter ist** (GPT). Das ist die einzige der vier
  Kritiken, die eine Entscheidungsregel ändert, und darum die wichtigste.

## 2. Die schwächsten Wachen - zusammengeführt und nachgemessen

Die drei Tabellen (GPT 9 Zeilen, Grok 13, Collaborator 13) überschneiden sich. Nach dem Zusammenführen
bleiben elf Stellen, an denen die geplante Wache den Sachverhalt nicht beweist. Spalte "heute"
belegt, was am Ist-Code schon gilt.

| # | Schritt | Schwache Wache | Warum sie nichts beweist | Ersatzprüfung (übernommen) | heute |
|---|---|---|---|---|---|
| 1 | 1 | Quellwache: `_render_diplomacy` enthält keine 40/60 | Textsuche übersieht einen Vergleich über eine Zwischenvariable | Ansicht mit Gunst 0/39/40/59/60/100 rendern und den ANGEZEIGTEN Status gegen `diplomatie.status` prüfen | Quellwache vorhanden, Renderprüfung fehlt |
| 2 | 2 | Zwei identische Läufe | beweist Reproduzierbarkeit der Eingaben, nicht dass der Zufall Teil des Startwerts ist | Zwei Prozesse, gleicher Startwert, Zeile für Zeile vergleichen; bei Abweichung gehört der Zufall in den Spielstand | **erledigt 06.11.2026**: Lauf bildet EINEN `random.Random(saat)`, zwei Läufe sind zeichengleich (2.596 Zeichen) |
| 3 | 3 | Quellwache: beide `main.py`-Stellen rufen `diplomatie.angriff_gesperrt` | der Aufruf kann am falschen Ziel oder ohne Wirkung stehen | Integrationstest am echten Bot-Angriffs- und Diebstahlpfad: aktiver NAP, gültiges Ziel, auslösbarer Bot → kein Auftrag, keine Beute | offen (Schritt 3) |
| 4 | 3 | "Durchmarsch hat keine Mechanikwirkung" | Wache auf ein Feld, das es im Code nicht gibt | AST-Wache: `vertrag_aktiv(..., "durchmarsch")` darf außerhalb der Anzeige nirgends gelesen werden | **gemessen**: `durchmarsch` kommt in `src/` und `data/` **nirgends** vor - das Feld entsteht erst in Schritt 3 |
| 5 | 4 | "höchstens ein laufender Auftrag je Bot und Ziel" | setzt den Auftrag im Test selbst | 5 Niederlagen am SELBEN Spieltag: Topf steigt genau +1; Rache und Taktik im selben Tick: genau ein Auftrag | offen (Schritt 4) |
| 6 | 5 | Overlay und Kern lesen dieselbe Preisfunktion | Aufrufgleichheit beweist keine atomare Buchung | Annahme mit exakt ausreichendem Bestand: Bestand genau um den Preis gesenkt, Gunst +5; bei Fehlschlag beides unverändert | offen (Schritt 5) |
| 7 | 6 | Anzeige und `punkte.handelspunkte` liefern denselben Wert | zwei Lesestellen können doppelt schreiben | Handelsvertrag abschließen, speichern, neu laden: `handels_erloes` genau einmal gebucht, Punkte unverändert nach dem Laden | **gemessen**: `handel_abschluss` setzt `erloes` und `angenommen` genau einmal; ein Feld `abgerechnet` gibt es noch nicht - die Wache muss die Doppelbuchung über Speichern/Laden prüfen |
| 8 | 7 | "kein Totalverlust gegen den Drachen in 10 Läufen" | statistisch, im Sammellauf flatternd | deterministische Grenzprüfung: SK = Drachenwert x 1,49 kein Auftrag, x 1,51 mit Profil `gierig` ein Auftrag | offen (Schritt 7) |
| 9 | 8 | "Neu rechnen ergibt identische Datei" | prüft Stabilität, nicht die Formel | Idealplan gegen die belegte Kette (`tests/test_produktionskette_ohne_cheats.py`) innerhalb der Bänder prüfen | offen (Schritt 8) |
| 10 | 10 | "Kette ohne `state.<feld> =`" | verbietet Zuweisungen, nicht Hilfsaufrufe mit gleicher Wirkung | AST-Prüfung: in den Ketten-Dateien wird kein Attribut des Spielstands außer über Aktionsfunktionen geschrieben | offen (Schritt 10) |
| 11 | 12 | "gleiche Ergebnislisten bei `--parallel 1` und `4`" | Gleichheit beweist nicht, dass jede Datei gelaufen ist | jede Prüfdatei schreibt eine Ergebniszeile, fehlende Zeile = rot (unabhängig vom Parallelitätsgrad) | offen (Schritt 12) |

**Nicht übernommen:** GPTs Forderung, den Spielstand samt Zufallszustand zu serialisieren (#2), ist
für das Remake zu schwer: der Zufall steckt heute in EINEM Generator, der aus der Saat gebildet wird.
Die Saat IST damit der Zufallszustand; ein zweiter Speicher wäre eine zweite Wahrheit.

## 3. Die fehlenden Abhängigkeiten - nachgemessen in der Tabelle

Die Abhängigkeitstabelle (`docs/ABLAUF_LLM_20261106.md`, Abschnitt 3) sagt heute:

| Behauptung | Messung | Urteil |
|---|---|---|
| GPT: Schritt 7 muss zusätzlich von 4 abhängen | Tabelle: Schritt 7 hängt an `5`; Schritt 4 hängt an 3, Schritt 5 an 1 und 3 - die Rache ist also NICHT Vorfahre von 7 | **BESTÄTIGT** - Abhängigkeit ergänzen |
| GPT: Schritt 10 hängt an "3 bis 10" (Selbstabhängigkeit) | Tabelle Zeile 10: `3 bis 10` | **BESTÄTIGT** - Text auf `3 bis 9` ändern |
| Grok: Schritt 6 vor Schritt 10 fehlt | `3 bis 9` enthält die 6; die Abhängigkeit ist also vorhanden, nur nicht genannt | **TEILWEISE** - Klarstellung in der Zeile, keine neue Kante |
| Collaborator: Schritt 5 muss VOR Schritt 4 | Ereignisse gibt es im Code noch nicht (Schritt 5 baut sie); der Rachetopf braucht aber eine Definition von "Kontakt", und die fehlt im Ablauf (gemessen: das Wort kommt nur in den beiden Rachelen vor, nirgends definiert) | **TEILWEISE** - das Problem ist die fehlende DEFINITION, nicht die Reihenfolge. Definition: Kontakt = Ereignis dieses Bots entschieden, mit ihm gehandelt, ihn angegriffen oder ihm ein Geschenk gemacht. Schritt 5 ergänzt dann eine Quelle, keine Vorbedingung |
| Gemini: Kennzahlenblatt erst NACH den Verträgen | Ein Vorher-Stand ist nur vorher etwas wert; Daniel hat am 06.11.2026 entschieden, dass das Kennzahlenblatt Schritt 2 ist (F-5) | **WIDERLEGT** |

## 4. Die Zahlen ohne Beleg - eine Rangfolge, neun Werte

Alle neun sind VORSCHLAG. Sortiert nach Risiko für das Spielgefühl; die Messung ist jeweils die
kleinste prüfbare Aussage. Wo das Kennzahlenblatt (Schritt 2) schon messen kann, ist das vermerkt.

| Rang | Wert | Höchstes Risiko | Messung vor dem Einbau | messbar mit |
|---:|---|---|---|---|
| 1 | Profilfaktoren 0,8 bis 1,2 | verschiebt Angriffsdruck UND Entwicklungsrhythmus | je Profil 10 Läufe, gleicher Startwert: Spreizung von `tag_erstes_gefecht` und `beute_je_feldzug` höchstens 20 % | Kennzahlenblatt |
| 2 | Drachen-Sicherheitsfaktor 1,5 | zu hoch: Bots meiden den Drachen ganz; zu niedrig: Armeen sterben | Grenzprüfung 1,49/1,51 plus Verlustquote je Drachenauftrag | Kennzahlenblatt |
| 3 | Rachetopf-Schwelle 3 | zu niedrig: Dauerbelagerung; zu hoch: die Welt reagiert nicht | 10 Läufe: Spieltag der ersten Ankündigung, Zielkorridor 4 bis 8 | Kennzahlenblatt |
| 4 | Vertragsbruch -20 Gunst | drückt einen Bot nahe 40 in den Kriegszustand | Bruch bei Gunst 40 erzwingen, Tage bis Gunst 40 zurück (Zielkorridor 2 bis 3) | offen |
| 5 | NAP-Dauer 3 Spieltage | langer Pakt nimmt den Konfliktdruck aus der Partie | 12-Tage-Läufe mit/ohne Pakt: Angriffe in den ersten 3 Tagen 0, danach wieder frei | Kennzahlenblatt |
| 6 | Ereignisfrist 2 Spieltage | zu kurz: Entscheidung wird verpasst | Anteil entschiedener Ereignisse vor Fristablauf | offen |
| 7 | Gunst ±5 je Ereignis | einzelne Entscheidung kippt Status oder Pakt | 20 Ereignisse: Änderung exakt ±5, kein Sprung über 40/60 durch EIN Ereignis | offen |
| 8 | Gunst-Start 50 | bestimmt die Ausgangslage aller Bots | 10 frische Spielstände: jeder Bot 50, Status "wachsam", kein Einfluss auf Punkte | offen |
| 9 | Sollkurven-Bänder 0,7 und 1,1 | falsche Warnung oder falsche Entwarnung im Werkzeug | Idealplan gegen 10 gemessene Läufe: mindestens 8 innerhalb beider Bänder | Kennzahlenblatt |

**Nicht übernommen:** Collaborators "20 Läufe mit gestreutem Leerlauf" (Rang 1 bei ihm) - die
Streuung wäre künstlich; gemessen wird mit echten Startwerten. Und Geminis "50 Partien je Wert" -
das kostet Rechenzeit ohne neue Erkenntnis, 10 Startwerte genügen für eine Richtung.

## 5. Die Wechselwirkungen - vier Kandidaten, alle real

| Wechselwirkung | Ablauf, kleinster Fall | Wache |
|---|---|---|
| **Ereignis ↔ NAP** (GPT) | Bot Gunst 40, aktiver Pakt, Ereignis abgelehnt → Gunst 35 → Pakt bricht (-20, +1 Rachetopf) → aus einer Entscheidung werden zwei Buchungen | Ereignis genau einmal abgezogen, Pakt genau einmal beendet, Bruchstrafe genau einmal, Topf genau einmal; ein weiterer Tick wiederholt nichts |
| **Tick-Reihenfolge** (Grok) | Topf 2, Gunst 40, Ereignis abgelehnt → Topf 3: genau EINE Ankündigung, Angriff erst nach 28.800 s Vorlauf | Reihenfolge im Tageswechsel: erst Ereignisse, dann Verträge, dann Rache - und die Wache prüft die Anzahl |
| **Profil ↔ Bruch** (Collaborator) | "gieriger" Bot bricht den Pakt und greift im selben Tick an, ohne Vorlauf | `ankuendigung_gesendet` im selben Tick wahr, Abstand bis zum Angriff >= 28.800 s |
| **NAP ↔ Topf** (Gemini) | unklar, ob ein aktiver Pakt den Topf einfriert oder ob er am Tag nach Ablauf sofort feuert | im Ablauf ist "ruht unter Vertrag" schon festgelegt (VORSCHLAG) - die Wache muss belegen: Topf wächst während des Pakts nicht, und der Angriff kommt frühestens 28.800 s nach Paktende |

**Entscheidung:** Alle vier werden Wachen, aber in verschiedenen Schritten: die ersten beiden in
Schritt 4 und 5, die dritte in Schritt 7, die vierte in Schritt 4. Keine wird zum eigenen Schritt -
es ist immer dieselbe Buchung, nur mit einem zweiten Auslöser.

## 6. Die Aufbauzeit - drei Korrekturen am Ablauftext

| Schritt | Ablauf sagt heute | Urteil | Neuer Text |
|---|---|---|---|
| 3 Verträge | "senkt sie" | **TEILWEISE** (GPT, Collaborator) | "bedingt: senkt sie nur, solange ein Pakt Angriffe verhindert; ein Pakt sperrt auch eigene Beute, kann sie also indirekt verlängern" |
| 4 Rachetopf | "erhöht den Druck, nicht die Dauer" | **WIDERLEGT** (GPT) | "erhöht den Druck UND kann die Aufbauzeit verlängern - ein ausgelöster Angriff kostet Einheiten und Zeit; zu messen über `tag_erster_krieger` und `abstand_meilensteine_max` mit und ohne Rache" |
| 5 Ereignisse | "neutral (Ablehnen möglich)" | **WIDERLEGT** (GPT) | "kostet bei Annahme Rohstoffe (Haug 990 Holz oder 64 Gold, Silra 12 Gold) und kann einen Bauschritt verzögern; Ablehnen kostet Gunst" |
| 7 Bot-Lücken | "kann sie heben (Faktoren gedeckelt)" | **PRÄZISIERT** (Grok) | "hebt sie in den gemessenen Läufen um bis zu einen Spieltag (Wache 7 erlaubt höchstens einen)" |
| 8/9 | "keiner" | **BESTÄTIGT** | unverändert - Werkzeuge verändern keine Mechanik |

## 7. Was übernommen wird und was nicht

| Vorschlag | Modell | Entscheidung | Grund |
|---|---|---|---|
| Schritt 8 (Sollkurve) streichen | Grok | **abgelehnt** | Schritt 9 braucht ein Ziel, gegen das er misst; ohne Sollkurve wäre "20 % besser" gegen die eigene Vorher-Zahl beliebig. Die Bänder bleiben VORSCHLAG. |
| Schritt 2 nach Schritt 3 verschieben | Gemini | **abgelehnt** | Ein Vorher-Stand muss vorher entstehen; Daniel hat F-5 entschieden. |
| Spielstand inklusive Zufallszustand serialisieren | GPT | **abgelehnt** | Die Saat ist der Zufallszustand (ein Generator, ein Speicher) - ein zweites Feld wäre eine zweite Wahrheit. |
| 50 Partien je Wert | Gemini | **abgelehnt** | Rechenzeit ohne neue Erkenntnis; 10 Startwerte zeigen eine Richtung, mehr erst bei echter Streuung. |
| Leerlauf künstlich streuen | Collaborator | **abgelehnt** | Gemessen wird mit echten Startwerten, nicht mit erzeugter Streuung. |
| Zusätzlicher Startwert vor jeder Annahme (Schritt 9) | GPT | **übernommen** | verhindert einen falschen Beschluss, nicht nur einen Fehler |
| Rache + Taktik im selben Tick | Grok, GPT | **übernommen** | echter Doppelauslöser, im Sammellauf unsichtbar |
| Kein Einfrieren nach Spionageauftrag | Collaborator | **übernommen** | Zustandsautomat kann dauerhaft warten |
| Grenzprüfung statt Statistik beim Drachen | Grok, Collaborator | **übernommen** | deterministisch statt flatternd |
| Definition "Kontakt" | Collaborator | **übernommen, aber als Definition** | die Reihenfolge 4 vor 5 ist ohne Ereignisse baubar |

## 8. Was diese Sitzung schon gemessen hat (Vorlage für die nächste Runde)

* **Sammellauf-Dauer schwankt weiter:** 12:10 bis 12:48 unter Last **2.363 s** mit zwei roten
  Dateien (`test_produktionskette_ohne_cheats` im Zeitlimit, `test_kartenwahl_bot` 24/1 - allein
  gefahren 25/0/0), danach sauber **1.290 s, 183 von 185 grün, 0 rot, 7.557 Prüfungen**. Zusammen
  mit 1.552 s und 1.612 s von heute Vormittag heißt das: die Grenze 1.800 s ist tragfähig, 1.400 s
  nicht (G-5 bestätigt, F-2 gilt).
* **Determinismus:** zwei Läufe über 12 Spieltage zeichengleich (Wache 2 erledigt).
* **G-1 bestätigt:** `punkte.angreifbar` hat genau zwei Aufrufstellen (`main.py:6638` Diebstahl,
  `:7065` Angriff) - eine dritte gibt es nicht.
* **Durchmarsch:** in `src/` und `data/` kommt das Wort nicht vor; das Feld entsteht erst in
  Schritt 3 (Wache 4 der Tabelle ist darum vor dem Einbau wertlos).
* **Ruhm:** `data/ruhm.json` hat vier Stufen; die gemessene Partie erreicht Stufe 2.
