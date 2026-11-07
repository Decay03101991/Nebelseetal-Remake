# Nebelseetal Remake - KI-Auftrag Runde 3

## 1. Kopf

- **Auftraggeber:** Daniel Koessl
- **Empfänger:** Claude Sonnet 5.5 (ein kostenloser Testlauf)
- **Stand:** Commit `b51afc3`, Dossier vom 07.11.2026, 18:20 (Register 295)
- **Zweck der Runde 3:** Die offenen Schritte 9 bis 13 und L des fixen Ablaufs vorbereiten, die vier Prüffragen aus Runde 2 mit neuen Messungen beantworten und die dabei gewonnenen Befunde als belastbare Entscheidungsgrundlage für Daniel bündeln.
- **Erwartung an den einen Lauf:** So viel brauchbare Arbeit wie möglich in EINEM Lauf erledigen: lesen, messen, rechnen, prüfen, Befunde mit Belegen dokumentieren und Vorschläge priorisieren. Es gibt keinen zweiten Testlauf; was in diesem Lauf nicht geschafft wird, bleibt offen.

## 2. Deine Rolle und deine Grenzen

**Du darfst:**

- Im Repository lesen: Quellcode, Tests, Daten, Register, Logs, Doku.
- Messen und Rechnen: Sammelläufe, Einzeltests, Werkzeuge, Kennzahlen, Dateiumfang, Abhängigkeiten.
- In deiner Sandbox schreiben: Notizen, Befundlisten, Zwischenergebnisse, geplante Vorschläge.
- Befunde begründen: Jede Aussage braucht einen Beleg (Datei, Zeile, Befehl, Testlauf, Registereintrag, Quellenverweis).
- Priorisieren und Empfehlungen aussprechen, wenn sie auf den Messungen beruhen.

**Du darfst nicht:**

- Das Repository verändern, committen oder pushen. Deine Arbeit bleibt in der Sandbox.
- Zahlen erfinden oder stillschweigend übernehmen, was nicht im Dossier oder in den Dateien belegt ist.
- Bereits belegte Fakten aus Register 284 bis 295 erneut prüfen oder neu bewerten. Diese Einträge sind abgeschlossen.
- Punkte aus Register 284 bis 295 neu aufrollen, es sei denn, du findest einen Widerspruch zu deinen eigenen Messungen; dann ist das ein Befund, keine Neubewertung.
- Handbuch 2009 (PDF) und 2006er Seiten verändern oder deren Inhalte umdeuten. Abweichungen notierst du, du gleichst sie nicht stillschweigend an.

## 2a. Kritik-Auftrag

Dieser Lauf dient ausschließlich der Kritik, nicht der Bestätigung oder dem Wohlwollen. Wohlwollen ist kein Ergebnis. Jeder Befund braucht einen konkreten Beleg (Datei und Zeile); eine Vermutung wird ausdrücklich als Vermutung gekennzeichnet. Ausdrücklich erwünscht sind Widersprüche, Langeweile, unlogische Mechanik, schwache Texte und Bruchstellen in der Geschichte – auch und gerade unbequeme Befunde. Gute Kritik nützt dem Projekt mehr als zwanzig Komplimente. Daniel Kössl kann jeden Punkt einzeln annehmen oder ablehnen, aber jeder Punkt muss so präzise sein, dass eine Entscheidung möglich ist.

## 3. Stand des Projekts

### 3.1 Gebaute Schritte (1 bis 8)

| Nr | Schritt | Register | Kurzstand |
|---|---|---|---|
| 1 | S4-1 Gunst und Status | bis 288 | gebaut, 6 Wachen |
| 2 | S4-2 Kennzahlenblatt (Messung) | bis 295 | gebaut, 4 Wachen |
| 3 | S4-3 Verträge: NAP, Handelsabkommen, Durchmarsch-Anzeige | bis 288/289 | gebaut, 7 Wachen |
| 4 | S4-4 Rachetopf und Angekündigter Angriff | bis 293 | gebaut, 7 Wachen |
| 5 | S4-5 Ereignisse Haug, Grom, Silra | Register 288 | gebaut, 6 Wachen |
| 6 | S4-6 Handelspunkte: Erlös buchen und anzeigen (G-8) | Register 289–292 | gebaut, 4 Wachen |
| 7 | S4-7 Bot-Lücken: Drache, Spionage, Reaktion | Register 293, 294 | gebaut, 8 Wachen |
| 8 | B-1 Sollkurve aus den Daten | Register 295 | gebaut, 4 Wachen; Werkzeug `tools/balance_kreis.py --sollkurve` schreibt `data/sollkurve.json`; Test `tests/test_balance_kreis.py` 29 Prüfungen, 0 Fehler |

Alle acht Schritte sind gebaut. Die Reihenfolge ist so gewählt, dass nach jedem Schritt ein spielbarer, grüner Stand existiert; kein Schritt hängt von einem späteren ab.

### 3.2 Offene Schritte (9 bis 13 und L)

| Nr | Schritt | hängt an | Aufwand | Wachen (Untergrenze) | Fertig-Kriterium (abgeleitet aus Abschnitt 3.3) |
|---|---|---|---|---|---|
| 9 | B-2 Regelkreis, A/B-Urteil, Feedback-Eingang | 8 | 90 min | 5 | Regelkreis liest `data/sollkurve.json`, vergleicht Ist gegen Ideal/Korridor (0,7 bis 1,1, VORSCHLAG), schlägt Anpassung vor, gibt Urteil A/B aus, Feedback-Eingang vorhanden. Wachen: 5 neue Prüfungen. |
| 10 | A-1 E2E-Ketten auf 12 Wege erweitern | 3 bis 10 | 120 min | 12 | 12 E2E-Ketten in einer Datei, je Weg eine; alle 12 Wege ohne Cheats erreichbar. Wachen: 12 neue Prüfungen. |
| 11 | A-2 AST-Quellwache für die Ansichten | 10 | 60 min | 3 | AST-Wache über die Ansichtsmethoden prüft, dass Anzeige nur zeigt, was der Kern erlaubt. Wachen: 3 neue Prüfungen. |
| 12 | A-6 Sammellauf messen und beschleunigen | 11 | 60 min | 2 | Grenze gemessen neu gefasst, Lauf beschleunigt. Wachen: 2 neue Prüfungen. |
| 13 | A-7/A-5 Schlussprüfung: Daten, Schalter, Quellen | 12 | 45 min | 3 | Jeder neue Schnitt bringt `aktiv` mit; jede Zahl belegt oder VORSCHLAG. Wachen: 3 neue Prüfungen. |
| L | Neuer KI-Auftrag aus diesem Ablauf (Meldepflicht) | 3 | 30 min | 0 | Dokument mit offenen Entscheidungen und Empfehlungen liegt vor. |

### 3.3 Ziel-Zustand (A-1 bis A-7) laut Dossier

| Nr | Bedingung | Heute (gemessen) | Nach diesem Ablauf |
|---|---|---|---|
| A-1 | Alle Spielwege ohne Cheats erreichbar | drei Ketten vorhanden (`test_produktionskette_ohne_cheats.py`, `test_durchspiel.py`, `test_gpt_wirtschaft_kette_e2e.py`), Handel und Portal nicht abgedeckt | 12 Ketten in einer Datei, je Weg eine |
| A-2 | Anzeige zeigt nur, was der Kern erlaubt | Textwachen vorhanden, keine maschinelle Rechenwache | AST-Wache über die Ansichtsmethoden |
| A-3 | Kein Spielweg endet in einer Sackgasse | nicht gemessen | Kennzahl `tag_erstes_gefecht` je Partie, 10 Läufe |
| A-4 | Alte Spielstände laden | je Feldgruppe eine Ladewache | bleibt Pflicht je neuem Feld |
| A-5 | Jede Zahl belegt oder VORSCHLAG | Register 266 Einträge | neue Zahlen mit Quelle, Rest als VORSCHLAG bei Daniel |
| A-6 | Voller Sammellauf grün | **rot gegen die eigene Grenze**: 1.612 s und 7.502 Prüfungen gegen unter 1.400 s und 7.495 (G-5) | Grenze gemessen neu gefasst, Lauf beschleunigt |
| A-7 | Balancing ohne Codeänderung | Schalter je Mechanik vorhanden | jeder neue Schnitt bringt `aktiv` mit |

### 3.4 Code-Umfang (laut Dossier)

- Python-Dateien: **324**, zusammen rund **91.216 Zeilen** (ohne `.venv`, `archiv`, `build`)
- `src/`: **63 Dateien**
- `tests/`: **194 Dateien**
- `tools/`: **59 Dateien**
- `data/`: **50 JSON-Dateien**
- Registereinträge: **293** (davon die letzten acht 288–295 im Dossier aufgelistet)

### 3.5 Wachen (letzte gemessene Stände)

- Schritt 8: `tests/test_balance_kreis.py` **29 Prüfungen, 0 Fehler**
- Sammellauf vom 07.11.2026, 18:37: **191 von 193 grün, 0 rot, 7.949 bestandene Prüfungen, 60 Befunde, 955 s** (`docs/audits/sammellauf_20261107_1837.log`)
- Vorlauf: Lauf davor rot in `test_bot_diplomatie.py` (66/1); behoben durch feste Saat und zehn Takte, danach drei Einzelläufe 67/0/0 (Commit `5232137`)

### 3.6 Neuester Stand-Block (Auszug)

- Schritt 8 (B-1 Sollkurve) steht. `tools/balance_kreis.py --sollkurve` spielt die BELEGTE Kette (Holzfäller, Steinmetz, Bibliothek, danach im Kreis Farm/Goldmine, Haus bei Siedlernot) auf den Geländefeldern der belegten Startkarte `original-036` Tag für Tag nach und schreibt `data/sollkurve.json` mit `{ideal, unten, oben}` je Spieltag für Holz, Stein, Nahrung, Gold, Siedler, Gebäude. `unten = Ideal × 0,7`, `oben = Ideal × 1,1` (VORSCHLAG). Der Dateikopf trägt `erzeugt_aus` mit sechs SHA256. Das Punkte-Ziel 3,3 je Spieltag ist mit Quelle (V-3) in der Datei.
- Gemessen: zwei Läufe zeichengleich; Holz +10 Prozent in einer Kopie der Datendatei hebt den Holzkorridor (Tag 10) und lässt Stein unberührt; das Werkzeug schreibt nur `data/sollkurve.json`.
- Fehler behoben: Gebäudenamen-Umlaute (`Holzfäller`, `Jäger`) vs. Plan `holzfaeller`; stille Null behoben über `_normal()`.
- Zwei benannte Lücken: Forschungskosten fehlen in `data/research.json`; auf Berg/Hügel früh belegte Felder, weitere Minen finden keinen Platz.
- Nächster Schritt laut Dossier: Schritt 9 (B-2 Regelkreis), danach 10 bis 13.

## 4. Der fixe Ablauf

Der fixe Ablauf definiert die offenen Schritte 9 bis 13 und L als verbindliche Reihenfolge. Ein Schritt = ein Commit = ein voller Sammellauf (21 bis 23 Minuten Erfahrungswert, keine Messung). Die Wachenzahl ist die Untergrenze der neuen Prüfungen je Schritt.

**Fertig-Kriterien der offenen Schritte** (abgeleitet aus den Zielbedingungen A-1 bis A-7; konkrete Zahlen wie 12 Ketten oder 0,7/1,1 sind durch das Dossier belegt, sofern nicht als VORSCHLAG markiert):

| Schritt | Fertig-Kriterium |
|---|---|
| 9 | `tools/balance_kreis.py` oder ein neues Modul liest `data/sollkurve.json`; es vergleicht den aktuellen Spielstand gegen Ideal und Korridor (0,7 bis 1,1, VORSCHLAG) und gibt ein A/B-Urteil aus; ein Feedback-Eingang (z.B. Konfiguration oder Dateneingabe) wird akzeptiert. 5 neue Wachen (Untergrenze). |
| 10 | Eine neue Datei enthält 12 E2E-Ketten; jede Kette prüft einen Spielweg ohne Cheats; alle 12 Wege sind erreichbar. 12 neue Wachen (Untergrenze). |
| 11 | Eine AST-Quellwache über die Ansichtsmethoden prüft, dass die Anzeige nur Werte zeigt, die der Kern erlaubt. 3 neue Wachen (Untergrenze). |
| 12 | Der volle Sammellauf wird gemessen; die Grenze wird anhand der Messung neu gefasst; die Laufzeit wird beschleunigt (Zielwert: unter der neu gefassten Grenze). 2 neue Wachen (Untergrenze). |
| 13 | Jeder neue Schnitt (Mechanik, Anzeige, Dateneingang) bringt den Schalter `aktiv` mit; alle Zahlen sind belegt oder als VORSCHLAG bei Daniel markiert. 3 neue Wachen (Untergrenze). |
| L | Ein Dokument (KI-Auftrag Runde 4) liegt vor, das die offenen Entscheidungen (F-16 und andere) mit Empfehlungen bündelt. |

Die Reihenfolge ist so gewählt, dass nach jedem Schritt ein spielbarer, grüner Stand existiert; es gibt keinen Schritt, der nur mit einem späteren zusammen funktioniert.

## 5. Die vier Prüffragen aus Runde 2

Die vier Fragen aus Runde 2 werden in Runde 3 mit NEUEN Messungen beantwortet. Jede Antwort braucht eine eigene Messung, ein eigenes Protokoll und eine klare Zuordnung zu den Teilen A bis H.

1. **Ist das Gesamtkonzept tragfähig?** – Beantworte anhand von Code-Struktur, Datenmodell, Abhängigkeiten und den neuen Messungen aus den Teilen A, B, C, D, H. Zeige Widersprüche oder fehlende Bausteine auf.
2. **Ist der Kernkreis ohne Sackgasse?** – Miss die Spielewege (A-1, A-3) mit der Kennzahl `tag_erstes_gefecht` je Partie, 10 Läufe. Beantworte, ob alle Wege erreichbar sind und ob ein Weg in eine Sackgasse führt. Urteil: BESTAETIGT, WIDERLEGT, TEILWEISE oder UNBEKANNT.
3. **Ist das Spiel originaltreu gegen Handbuch 2009 und die 2006er Seiten?** – Vergleiche die gebauten Mechaniken (S4-1 bis S4-7, B-1) mit dem Handbuch 2009 (PDF) und den 2006er Seiten. Notiere jede Abweichung, gleiche sie nicht stillschweigend an. Urteil je Mechanik.
4. **Ist die ausgelieferte Fassung spielbar?** – Führe den vollen Sammellauf durch, anschließend die E2E-Ketten und die neuen Wachen. Prüfe, ob der Stand grün ist, ob alte Spielstände laden (A-4) und ob die Anzeige nur zeigt, was der Kern erlaubt (A-2). Urteil: spielbar / nicht spielbar / bedingt spielbar.

**Erwartung an Runde 3:** Diese vier Fragen werden nicht rhetorisch beantwortet, sondern mit konkreten Messungen, Befunden und Belegen aus den Teilen A bis H. Jede Antwort endet mit einem der vier Urteile.

## 6. Der Lieferumfang in Teilen

Du lieferst ZEHN Teile mit den Kennungen A bis J. Teil I ist der wichtigste: er verlangt harte Kritik an Geschichte, Logik und Mechanik. Jeder Teil hat eine eigene Fragestellung, liefert Befunde im vorgeschriebenen Format und eine Rangliste der wichtigsten Punkte.

**Format für jeden Befund in allen Teilen:**

- **Befund:** Kurzbeschreibung des Sachverhalts (Was wurde gemessen/geprüft?).
- **Beleg:** Datei und Zeile oder Befehl (z.B. `tools/balance_kreis.py:120`, `pytest tests/test_x.py::test_y`, `docs/audits/sammellauf_*.log`, Register-Nummer).
- **Urteil:** Eines der vier Urteile: **BESTAETIGT**, **WIDERLEGT**, **TEILWEISE**, **UNBEKANNT**.
- **Vorschlag mit Aufwand:** Falls ein Handlungsbedarf besteht, ein konkreter Vorschlag mit geschätztem Aufwand (in Minuten, als VORSCHLAG gekennzeichnet, sofern nicht aus dem Dossier belegt). Beispiel: "VORSCHLAG Aufwand: 15 min".

**Rangliste:** Am Ende jedes Teils eine absteigend priorisierte Liste der wichtigsten Punkte (maximal 10) mit Begründung in einem Satz.

**Teile:**

- **A – Gesamtbild und Widersprüche:** Fragestellung: Ist das Projekt in sich konsistent? Was sind die größten Risiken? Was widerspricht dem Dossier, dem Ablauf oder den Zielbedingungen A-1 bis A-7? Liefern: Übersichtstabelle der offenen Punkte, Widersprüche zwischen Dateien, Register, Dossier und Messungen, unbelegte Annahmen, Prioritätenliste.
- **B – Spielmechanik gegen das Original:** Fragestellung: Welche der gebauten Mechaniken (S4-1 bis S4-7, B-1) weichen vom Handbuch 2009 oder den 2006er Seiten ab? Liefern: Je Mechanik ein Befund mit Quellenangabe (Register, Datei, Handbuchseite), Abweichungsliste, Urteil. Keine stillschweigende Angleichung.
- **C – Code und Fehler:** Fragestellung: Wo gibt es Fehler, stille Nullen, inkonsistente Funktionen oder tote Pfade? Liefern: Befundliste mit Datei und Zeile, Reproduktionsbefehl, erwartetes und tatsächliches Verhalten, Schweregrad, Vorschlag mit Aufwand.
- **D – Balance und Zahlen:** Fragestellung: Sind die Zahlen belegt oder als VORSCHLAG markiert? Welche Balance-Korridore (z.B. 0,7 bis 1,1) sind sinnvoll? Wo fehlen Quellen? Liefern: Liste aller Zahlen aus den neuen Schritten mit Quelle oder VORSCHLAG, Prüfung der Sollkurve gegen echte Läufe, Empfehlungen für F-16.
- **E – Oberfläche und Bedienung:** Fragestellung: Ist die Anzeige konsistent mit dem Kern (F-04)? Sind Verkaufsmasken, Kennzahlenblatt, Drachen-Anzeige benutzbar? Liefern: Prüfprotokoll der Ansichten, Belege für Anzeige/Kern-Doppelungen, Vorschläge für A-2.
- **F – Spielbarkeit und Testläufe:** Fragestellung: Ist der aktuelle Stand spielbar? Führe den vollen Sammellauf durch, dokumentiere das Ergebnis, führe die vorhandenen E2E-Ketten aus, bewerte Laufzeit und Grenze. Liefern: Protokoll mit Zahlen (Zeit, Prüfungen, Befunde), Vergleich zu G-5 (1.400 s / 7.495), Empfehlung für A-6.
- **G – Dokumente, Register und Quellen:** Fragestellung: Sind Register, Doku und Datenquellen vollständig und widerspruchsfrei? Welche Registereinträge fehlen oder sind unklar? Liefern: Register-Abgleich mit den Dossier-Einträgen 288–295, fehlende oder unklare Einträge, Quellenlage der Handbuch-Referenzen.
- **H – Offene Entscheidungen mit Empfehlung:** Fragestellung: Welche offenen Entscheidungen (F-16 und andere) müssen vor Schritt 9 geklärt werden? Liefern: Je offene Entscheidung: Kontext, Optionen, Empfehlung mit Begründung, Aufwand der Umsetzung (VORSCHLAG). Am Ende eine Rangliste der dringendsten Entscheidungen.

- **I – Geschichte, Logik und innere Stimmigkeit:**

**Kennung:** I  
**Titel:** Geschichte, Logik und innere Stimmigkeit

**Fragestellung:** Erzählt das Spiel eine zusammenhängende Geschichte? Passt die Chronik zur Spielmechanik (Völker, Drachen, Bots, Portal)? Wo bricht die innere Logik – Zahlen, die zur erzählten Welt nicht passen, Figuren ohne Motiv, Belohnungen ohne Begründung, Textsorten, die einander widersprechen?

**Auftrag:** Analysiere das Projekt „Nebelseetal Remake“ unter diesen Gesichtspunkten. Verlange ausdrücklich harte Kritik: Was ist langweilig, beliebig, klischeehaft oder unklar? Welche Mechanik macht spielerisch keinen Sinn (Sackgassen, Frust, Leerlauf)? Wo fehlt eine Entscheidung mit Gewicht? Welche Texte (Dialoge, Meldungen, Chronik) sind schwach und warum?

**Methodik und Format:**
- Arbeite die folgenden Dateien vollständig durch: `data/story.json` (intro, chronik, ereignisse, sieg, niederlage, menue_geschichten, gesamtsieg), `data/bot_stimmen.json`, `docs/CHRONIK_DER_WELT_20261104.md`, `docs/STORY_GESAMTBILD_20261104.md`, `docs/STORY_BIBEL_ENTWURF_20261104.md`, `docs/SPIELKONZEPT.md`.
- Für jeden Befund: **Befund** (konkreter Sachverhalt), **Beleg** (Datei und Zeile, z. B. `data/story.json`, `docs/CHRONIK_DER_WELT_20261104.md:12`), **Urteil** (BESTAETIGT, WIDERLEGT, TEILWEISE, UNBEKANNT), **Vorschlag mit Aufwand** (z. B. „Text überarbeiten – 1 Stunde“, „Mechanikwert anpassen – 2 Stunden“, „Neue Quest – 1 Tag“).
- Am Ende: Rangliste der zehn wichtigsten Mängel, sortiert nach Schwere für Spielerlebnis und innere Logik.

**Mindestens acht Unterfragen, die du beantworten musst:**
1. Ist die Chronik der Welt in sich schlüssig? Gibt es widersprüchliche Jahreszahlen, Ereignisse oder Personennamen zwischen `docs/CHRONIK_DER_WELT_20261104.md` und `data/story.json`?
2. Passen die drei Völker (menschlich, zwergisch, elfisch) mit ihren je zwei Attributen zu den in der Chronik und im Story-Gesamtbild beschriebenen Fähigkeiten, Schwächen und Bauweisen? Wo weichen erzählte Eigenschaften von den Mechanikwerten ab?
3. Haben die vier Bots (Haug der Plünderer, Brynhild die Wächterin, Grom der Bastionier, Silra die Späherin) erkennbare Motive, Persönlichkeiten und Ziele? Passen ihre Sätze in `data/bot_stimmen.json` zu ihrem Verhalten im Spiel? Oder sind sie austauschbare Gegner?
4. Sind die drei Drachen (Epheus der Weiße, Tardas der Grüne, Salmur der Rote) erzählerisch eingebunden? Gibt es eine Begründung für ihre Existenz, ihr Territorium und ihre Rolle im Spiel? Oder wirken sie als reine Kampfherausforderungen ohne Geschichte?
5. Gibt es Belohnungen (Ressourcen, Gebäudefreischaltungen, Story-Ereignisse), die nicht zur erzählten Welt passen oder ohne Begründung vergeben werden? Wo wird eine Belohnung gegeben, die der Spieler nicht durch Handlung verdient hat?
6. Wo kollabiert die Zahlenlogik zwischen Geschichte und Mechanik? Nenne konkrete Beispiele: Baukosten, Forschungsdauern, Einheitenstärken, Drachen-Lebenspunkte, Bot-Aggressivität, Portalmechanik – gibt es Werte, die der erzählten Welt widersprechen oder spielerisch absurd sind?
7. Welche Texte (Dialoge, Meldungen, Chronik-Einträge, Menü-Geschichten) sind schwach? Nenne konkrete Beispiele für hölzerne, klischeehafte, unklare oder widersprüchliche Formulierungen. Warum sind sie schwach?
8. Bietet die Story echte Entscheidungen mit Gewicht? Welche Entscheidungen des Spielers haben dauerhafte Konsequenzen für Welt, Völker, Bots oder Drachen? Wo fehlen Verzweigungen, und wo wird eine Entscheidung vorgetäuscht, ohne Wirkung zu haben?
9. Gibt es Leerlauf, Frust oder Sackgassen in der Spielmechanik, die auch die Geschichte beschädigen? Wo wartet der Spieler ohne erzählerischen Fortschritt? Wo führt eine Mechanik zu einem toten Ende ohne Erklärung?
10. Sind die Textsorten (Intro, Chronik, Ereignisse, Sieg, Niederlage, Menü-Geschichten, Gesamtsieg) in Ton, Perspektive und Ansprache konsistent? Oder wechseln Stil, Zeitform oder Erzähler unvermittelt?

**Hinweis:** Du darfst und sollst unbequem sein. Eine Bestätigung des Ist-Zustands ist kein Ergebnis. Zeige Widersprüche, Langeweile, unlogische Mechanik, schwache Texte und Bruchstellen in der Geschichte auf. Jeder Befund muss belegt sein; Vermutungen sind als solche zu kennzeichnen.

**Hinweis zu Teil D:** Die Sollkurve (B-1) ist eine OBERGRENZE aus den Daten (jedes Gebäude sofort baubar), kein Erfahrungswert. Ob sie gedrosselt werden soll (z.B. ein Gebäude je Spieltag), ist Frage F-16. Du prüfst diese Frage mit Messungen, nicht mit Meinung.

- **J – Spielgefühl, Langzeitmotivation und Wiederspielwert:** Fragestellung: Macht das Spiel Spaß, und
  würde man es ein zweites Mal beginnen? Liefern: je Unterfrage ein Befund mit Beleg -
  1. Was passiert in den ersten 30 Spielminuten, und ist das genug, um zu bleiben?
  2. Wie steil ist die Lernkurve, und wo bricht sie (Überforderung, Unterforderung, Leerlauf)?
  3. Wo entsteht Grind - welche Tätigkeit wiederholt sich ohne neue Entscheidung, und wie lange?
  4. Ist der Belohnungsrhythmus richtig getaktet (Punkte, Ruf, Freischaltungen), oder kommen Erfolge
     zu spät bzw. zu früh?
  5. Fühlt sich ein Sieg nach Sieg und eine Niederlage nach Niederlage an - oder ist beides beliebig?
  6. Was macht den Wiederspielwert aus (andere Startkarte, andere Taktik, andere Bots), und reicht das?
  7. Wie nah ist das Erlebnis am Original 2005/2009 - und wo ist es BESSER, wo SCHLECHTER, mit Beleg?
  8. Was unterscheidet eine Partie gegen die Bots von einer gegen einen Menschen, und was fehlt dadurch?
  9. Welche drei Punkte würden einen Spieler am ehesten aufhören lassen? Nenne sie mit Beleg.
  10. Wenn nur vier Stunden Arbeitszeit zur Verfügung stünden: welche fünf Änderungen bringen dem
      Spielgefühl am meisten? Mit Begründung und Aufwand.
  Am Ende eine Rangliste der fünf größten Spaßbremsen.

**Mindestumfang (verbindlich):**

- Je Teil mindestens **acht** befundete Punkte, zusammen mindestens **sechzig**. Ein Teil mit drei
  Punkten gilt als nicht geliefert.
- Jeder Punkt hat Beleg (Datei und Zeile, Befehl oder Register-Nummer) und Urteil.
- Jeder Teil endet mit einer Rangliste; Teil J zusätzlich mit den fünf Änderungen für vier Stunden.
- **Selbstprüfung am Ende des Laufs:** eine Liste der Befunde, bei denen du dir selbst unsicher bist
  (Urteil UNBEKANNT oder Vermutung), mit dem Grund. Diese Liste ist Pflicht - sie zeigt Daniel, was
  nachgeprüft werden muss.
- **Nichts wiederholen:** was in Register 284 bis 295 oder in den Sammellauf-Logs steht, gilt als
  bekannt und wird nur bei einem MESSBAREN Widerspruch erneut aufgegriffen.

## 7. Was das Modell NICHT tun soll

- Kein Code schreiben, der das Repository verändern würde.
- Keine Zahl erfinden oder als belegt ausgeben, wenn die Quelle fehlt. Verwende **UNBEKANNT - vom Modell zu messen**, wenn das Dossier keine Angabe macht.
- Keine Punkte aus Register 284–295 neu bewerten oder deren Befunde in Frage stellen, außer du findest einen messbaren Widerspruch; dann ist das ein neuer Befund.
- Keine bereits belegten Fakten erneut prüfen (z.B. die 29 Prüfungen aus `test_balance_kreis.py` sind belegt und bleiben).
- Keine Handbuchseiten umdeuten oder Abweichungen stillschweigend angleichen.
- Keine Links oder gespeicherte Chat-Seiten als Ablage verwenden; nur direkt angehängte Dateien.
- Keine Emojis, keine Werbung, keine Meta-Erklärungen.

## 8. Paket und Ablage

- Jeder Teil (A bis J) wird als **eine Datei** geliefert, bevorzugt Markdown (`.md`) oder CSV/JSON für strukturierte Befundlisten.
- Alle Dateien werden **direkt angehängt**, kein Link, keine gespeicherte Chat-Seite, kein Git-Repository.
- Ein ZIP-Paket pro Teil ist erlaubt, wenn ein Teil mehrere Dateien umfasst; Paketgröße **höchstens 8 MB je ZIP**.
- Dateinamen enthalten das Datum im Format `JJJJMMTT`, z.B. `20261107_Teil_A_Gesamtbild.md` oder `20261107_Teil_C_Code_Fehler.zip`.
- Zusätzlich ein Gesamtdokument `20261107_Runde3_Dokument.md`, das die Antworten auf die vier Prüffragen, die Ranglisten aller Teile und die Liste der UNBEKANNT-Punkte bündelt.
- Alle Befunde in den Dateien enthalten die Belegzeile (Datei und Zeile oder Befehl). Ohne Beleg wird ein Befund nicht gewertet.

## 9. Meldepflicht an Daniel

Nach dem Lauf lieferst du an Daniel zurück:

1. **Gesamtdokument:** `20261107_Runde3_Dokument.md` mit den Antworten auf die vier Prüffragen, den Ranglisten der Teile A bis H, allen Befunden mit Urteilen und den offenen Entscheidungen.
2. **Ranglisten:** Je Teil eine absteigend priorisierte Liste der wichtigsten Punkte (maximal 10 Einträge) mit Begründung in einem Satz.
3. **Liste der UNBEKANNT-Punkte:** Alle Sachverhalte, die du nicht messen oder belegen konntest, mit der Kennzeichnung **UNBEKANNT - vom Modell zu messen** und einer Erklärung, warum die Messung nicht möglich war (z.B. fehlende Datei, fehlender Quelltext, fehlende Quelle).
4. **Verbale Zusammenfassung:** Maximal fünf Sätze, was die wichtigste Erkenntnis der Runde 3 ist und welche Entscheidung Daniel als Nächstes treffen muss.
5. **Keine Änderung am Repository:** Du teilst mit, dass du nichts committet oder gepusht hast, und legst deine Sandbox-Ergebnisse nur als Anhänge vor.

## 10. Prüfliste für den Auftraggeber

Anhand dieser Punkte erkennt Daniel in etwa zwei Minuten, ob die Lieferung brauchbar ist:

1. **Gesamtdokument vorhanden?** Liegt `20261107_Runde3_Dokument.md` vor, mit klarer Gliederung und allen acht Teilen A bis H?
2. **Vier Prüffragen beantwortet?** Sind die vier Fragen aus Abschnitt 5 jeweils mit einer konkreten Messung, einem Beleg und einem Urteil beantwortet?
3. **Belegformat eingehalten?** Enthält jeder Befund eine Belegzeile (Datei und Zeile oder Befehl)? Ohne Beleg ist der Befund unbrauchbar.
4. **UNBEKANNT-Liste vorhanden?** Gibt es eine Liste aller nicht messbaren Punkte mit der Kennzeichnung UNBEKANNT?
5. **Ranglisten je Teil?** Hat jeder Teil A bis H eine eigene Rangliste der wichtigsten Punkte?
6. **Keine Repository-Änderung?** Steht im Dokument, dass kein Commit oder Push erfolgt ist, und sind alle Anhänge direkt beigefügt (kein Link)?
7. **Zahlen korrekt belegt?** Sind alle genannten Zahlen entweder aus dem Dossier (mit Quellenverweis) oder als VORSCHLAG/UNBEKANNT markiert?
8. **Aufwand und Empfehlung für offene Entscheidungen?** Enthält Teil H eine priorisierte Liste der offenen Entscheidungen (insbesondere F-16) mit Empfehlung und Aufwandsvorschlag?
