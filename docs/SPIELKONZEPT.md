# SPIELKONZEPT - Nebelseetal Remake (das EINE aktuelle Konzept)

**Stand:** 06.11.2026, 13:40 · **Version** V_0.0.3 · **Kopf** `f09b672` · **Register** 280 bis 282
**Führend für:** Spielziel, Mechaniken, Zahlen-Maßstab, Belegpflicht. **Nicht führend für:** die
Reihenfolge der Arbeit (das ist `docs/ABLAUF_LLM_20261106.md`) und den Tagesstand (das ist
`docs/AKTUELLER_STAND.md`).

**Warum diese Datei existiert:** Es gab bisher viele gute Einzeldokumente (Plan, Anforderungen,
Konzeptpapiere, Entwürfe, Entscheidungsverzeichnis), aber kein EINES, das den aktuellen Stand
zusammenhält. Wer neu einsteigt, musste raten, was gilt. Ab 06.11.2026 gilt dieses Dokument; es
verweist auf die Details, statt sie zu wiederholen.

**Urteile, die überall gelten:** BELEGT (Quelle nennt es), WIDERSPRUCH (Quelle sagt etwas anderes),
NICHT BELEGT (Quelle schweigt), VORSCHLAG (unsere bewusste Entscheidung), OFFEN (Entscheidung
nötig). Jede Zahl in diesem Dokument trägt eines davon. Die Belege stehen im Register
`docs/PRUEFREGEL_ORIGINAL.md`.

---

## 1. Vision und Spielerlebnis

- **BELEGT (Daniel):** ein portables, offline spielbares Einzelspieler-Remake des Browserspiels
  Nebelseetal, kostenlos, ohne Konto, mit eigenem Spielstand auf der Platte.
- **BELEGT (E5):** einen Sieg gibt es bewusst NICHT - das Original nennt keine Siegbedingung, jeder
  Spieler hat eigene Ziele. Niederlage nur ohne Siedlung und ohne Einheit.
- **BELEGT (Original, Handbuch 2009):** aufbauen, forschen, ausrüsten, ausbilden, ziehen, kämpfen,
  punkten. Die Kette ist der Kern; wer sie abkürzt, verliert das Spielgefühl.
- **VORSCHLAG:** das Spielgefühl entsteht aus ENTSCHEIDUNGEN, nicht aus Wartezeit. Gemessener
  Maßstab: Leerlaufanteil (Ziel unter 50 %), längste Strecke ohne neuen Meilenstein (Ziel unter
  1,5 Spieltage), sichtbare Reaktionen der Bots mit Vorwarnung.
- **OFFEN:** wann eine Partie für Daniel "erfüllt" ist (Frage an Daniel, siehe Abschnitt 12).

## 2. Ausgangslage und gemessener Stand

- **BELEGT (gemessen 06.11.2026):** Version V_0.0.3, Kennzahlenblatt einer Partie über 12 Spieltage
  (Saat 7, Stil breit): erstes Haus Tag 2,486, erste Bibliothek 0,042, erste Ware 7,833, erster
  Krieger 1,167, erstes Gefecht 2,0, Ruhm-Stufe 2, Beute 190 in 6 Gefechten, eigene Verluste 0,
  **Leerlauf 92 %**, größte Lücke 5,347 Spieltage, Handelspunkte `null`.
- **BELEGT (gemessen):** der Lauf ist deterministisch - ein `random.Random(saat)` für die ganze
  Partie; zwei Läufe sind zeichengleich.
- **BELEGT (gemessen):** voller Sammellauf 183 von 185 grün, 0 rot, 1.290 s ohne Nebenlast; unter
  Nebenlast 2.363 s und zwei rote Dateien. Die Grenze 1.800 s ist tragfähig, 1.400 s nicht.
- **OFFEN:** der hohe Leerlauf ist ein Befund über den AUTOMATEN (Spielerpolitik des Spieltests),
  nicht über das Spiel - wie viel davon im echten Spiel bleibt, weiß niemand. Die nächste Messung
  mit dem Kennzahlenblatt zeigt es.

## 3. Originaltreue und Belegsystem

- **BELEGT (Daniel, 30.10.2026):** jede neue Zahl, jeder Ablauf, jede Meldung wird vor dem Einbau
  gegen eine Quelle gehalten; das Urteil kommt ins Register, und was dort steht, wird nicht erneut
  geprüft - nur bei echtem Widerspruch.
- **BELEGT (Daniel, 31.10.2026):** Balance-Zahlen aus dem Handbuch 2009, Struktur und Mechanik aus
  beiden Fassungen (2005/2006 und 2009). Abweichungen gehören nach
  `docs/quellen/ABWEICHUNGEN_2006_zu_2009.md` - niemals stillschweigend angleichen.
- **BELEGT:** fehlt die Quelle, wird nichts erfunden - der Wert steht als VORSCHLAG mit Rechenweg
  und Daniel entscheidet.
- **VORSCHLAG:** Modelle und starke Helfer liefern ENTWÜRFE, nie Zahlen. Eine Zahl aus einer
  Modellantwort wird erst übernommen, wenn sie eine Quelle hat.

## 4. Wirtschaft und Siedlungsaufbau

- **BELEGT (Original):** jede Siedlung hat ein eigenes Lager; es gibt keine globale Kapazität. Die
  Reichsanzeige ist die Summe der Orte (`_reichsanzeige_aus_orten`) - niemals eine zweite Kasse.
- **BELEGT (Screenshot `web_1838857`):** Baupreise Holzfäller 10 Holz/5 Stein/1 Siedler, Steinmetz
  5/10/1, Jäger 25/25/1, Haus 80/50; ein Haus hebt die Siedlergrenze um 5.
- **BELEGT (Original):** Siedlergrenze 10 + 5 je Haus, höchstens 6 Siedlungen, 127 Originalsiedlungs-
  karten. Der harte Engpass sind Siedler, nicht Rohstoffe.
- **BELEGT (gemessen 31.10.):** Beute ist strukturell gedeckelt (Anteil 10/30/60/100 % UND
  Karrenladung); "alles stehlen" geht nur früh.
- **VORSCHLAG:** Nahrung als zweiter Engpass (8 je Einheit und Spieltag, `data/nahrungsverbrauch.json`
  mit Schalter) - hergeleitet aus dem Reichsertrag, in der Datei nachgerechnet.

## 5. Forschung, Waren und Einheiten

- **BELEGT (Original):** 21 Forschungen, 17 Waren, 9 Rohstoffe, 28 Einheiten; Waren brauchen
  Werkstätten (Schmiede, Näherei, Bogenbauer) und Forschungen; Einheiten brauchen Waren UND Gold.
- **BELEGT (gemessen):** Werkzeuge und Eisen gibt es im Spiel NICHT (Befund G-4). Das Grom-Ereignis
  tauscht darum 5 Messer gegen 20 Erz (Rohstoff `metall`) - Daniels Entscheidung F-1 vom 06.11.2026.
- **BELEGT (Original, Wagenbau):** Karrenladung wächst mit der Forschung "Wagenbau"; Basiswerte
  bleiben die des Originals, der Bonus kommt obendrauf (`data/karrenkapazitaet.json`).
- **VORSCHLAG:** Werkstätten haben keine Ausbaustufen - der Ausbau ist die Forschung (Entscheidung 16).
- **BELEGT (Original):** Punkte = Forschung (Stufe hoch drei), Krieg (Einheitenwerte + Wallstufe
  hoch drei), Gesamt die halbe Summe; Ruf/Ruhm in vier Stufen (`data/ruhm.json`).

## 6. Diplomatie: Gunst, Status und Verträge

- **BELEGT (gebaut, Schritt 1):** jeder Bot hat Gunst 0..100, Start 50; der Status (feindselig unter
  40, wachsam 40..59, freundlich ab 60) wird GERECHNET und nie gespeichert. EINE Lesestelle:
  `src/diplomatie.py`; die Anzeige liest dieselbe Funktion.
- **VORSCHLAG (Auftragsdokument 7.1, Originalbeleg offen = A-5):** die Grenzen 40 und 60.
- **VORSCHLAG (Schritt 3):** Nichtangriffspakt ab Gunst 40, Dauer 3 Spieltage (86.400 Spielsekunden),
  Bruch unter 40 kostet 20 Gunst und +1 Rachetopf; Handelsabkommen ab 40 über den vorhandenen
  Handelsweg; Durchmarsch ab 60 ist eine reine ANZEIGE ohne Mechanikwirkung.
- **BELEGT (Befund G-1, gemessen):** die Angriffssperre ist `punkte.angreifbar` mit genau zwei
  Aufrufstellen (`main.py:6638` Diebstahl, `main.py:7065` Angriff). Der Pakt setzt dort eine
  Vorbedingung - es entsteht KEINE zweite Rechnung und kein zweites Gate.
- **OFFEN:** ob der Pakt nur den Spieler schützt oder beidseitig wirkt, und damit, ob er auch
  eigene Plünderungen sperrt (siehe Aufbauzeit, Abschnitt 11).

## 7. Rachetopf und angekündigter Angriff

- **BELEGT (Befund G-2):** die Rache-Schwelle ist **99 SK** - 90 SK ist die Wall-Schwelle.
- **VORSCHLAG (Schritt 4):** +1 je Niederlage und +1 je Spieltag ohne Kontakt; Schwelle 3; Ruhen
  unter Götterschutz und während eines Vertrags; Ankündigung genau einmal, Angriff frühestens einen
  Spieltag (28.800 s) später; nach einem Bot-Sieg Topf auf 0 (Daniel, F-3).
- **OFFEN - die wichtigste offene Definition:** was "Kontakt" heißt. Der Ablauf nennt das Wort,
  definiert es aber nirgends (gemessen 06.11.2026). Die Definition gehört VOR den Einbau:
  Vorschlag siehe Abschnitt 12, Frage 1.
- **OFFEN:** die Reihenfolge im Tageswechsel (Ereignisse, Gunst, Vertragsbruch, Rachetopf,
  Bot-Aktionen). Vier unabhängige Gegenprüfungen haben diese Lücke gefunden; der Vorschlag steht in
  `docs/ABGLEICH_LLM_20261106_runde2.md`, Abschnitt 5.

## 8. Ereignisse: Haug, Grom, Silra

- **VORSCHLAG (V-4, nachrechenbar über `tools/s0_tabellen.py:110-111`):** Haug 990 Holz ODER 64
  Gold, Silra 12 Gold (mindestens 1); Grom tauscht 5 Messer gegen 20 Erz (F-1).
- **VORSCHLAG (Schritt 5):** Frist 2 Spieltage (57.600 s), höchstens ein Ereignis je Bot in 3
  Spieltagen, Annahme Gunst +5, Ablehnung oder Ablauf -5, Annahme atomar aus dem ORTSLAGER (fehlt
  der Bestand, wird nichts gebucht).
- **BELEGT (Muster Story):** Texte stehen in Datendateien (`data/story.json`), nie im Code.
- **OFFEN:** ob ein abgelehntes Ereignis bei Gunst 40 einen Pakt bricht - die Wechselwirkung
  Ereignis/NAP ist gemessen möglich und braucht eine eigene Wache (Schritt 4 und 5).

## 9. Handelspunkte

- **BELEGT (Original 2006, `punktesystem.php`):** 1 Punkt je 100 Gold Erlös, Verfall 1 Punkt je 24
  Spielstunden (`src/punkte.py:400-414`).
- **BELEGT (Befund G-8, gemessen):** `gold_erloes` wird im Spiel nirgends geschrieben - die Kennzahl
  kann darum nie steigen. Der Handelsweg selbst ist fertig (`handel_abschluss` setzt `erloes` genau
  einmal); es fehlt nur die Buchung und die Übergabe an die Anzeige.
- **VORSCHLAG (Schritt 6):** Erlös auf einen Zähler `handels_erloes` buchen, `letzter_handel` setzen,
  genau einmal je Vertrag (Feld `abgerechnet`), Anzeige und Punkterechnung lesen dieselbe Funktion.
- **OFFEN:** Doppelbuchung beim Speichern und Laden - muss Wache werden, nicht Annahme.

## 10. Bot-Verhalten und Lücken

- **BELEGT (gemessen):** Bots haben eine eigene Wirtschaft, eigene Dörfer, Weltkarten, Armeen und
  Wappen; sie greifen den Spieler seit jeher an (`main.py:6896`).
- **BELEGT (gemessen):** der Automatenspieler steht 92 % der Partie still - die Bots sind also nicht
  der einzige Grund für fehlende Interaktion, aber der sichtbarste.
- **VORSCHLAG (Schritt 7):** Drachenentscheidung mit Sicherheitsfaktor 1,5, genau ein Spionageauftrag
  vor einem Raubzug (Frist 1 Spieltag), Reaktionsprofile 0,8 bis 1,2 - alles gedeckelt, alle drei
  Gates (Götterschutz, Pakt, Demo) gelten auch hier.
- **OFFEN:** das dauerhafte Einfrieren im Zustand "warte auf Spionage" (Collaborator, Runde 2) - die
  Wache muss über mehrere Spieltage prüfen, dass der Raubzug weiterläuft.

## 11. Balance, Aufbauzeit und Regelkreis

- **BELEGT (gemessen):** Aufbauzeit ist messbar über die Meilensteine des Kennzahlenblatts. Sie ist
  die Größe, die jede neue Mechanik ungewollt verändern kann.
- **WIDERLEGT (Runde 2, gemessen am Ablauftext):** die pauschalen Angaben "senkt sie" (Schritt 3) und
  "nur Druck, nicht Dauer" (Schritt 4) und "neutral" (Schritt 5). Richtig ist: ein Pakt senkt sie nur
  bei wirksamem Schutz und kann eigene Beute kosten; ein Racheangriff kostet Einheiten und Zeit; eine
  angenommene Ereignis-Hilfe kostet Rohstoffe.
- **VORSCHLAG (Schritt 8):** Sollkurve aus den Daten mit Bändern 0,7 und 1,1; Punkte-Ziel 3,3 je
  Spieltag (V-3). **VORSCHLAG (Schritt 9):** eine Änderung gilt erst als angenommen, wenn die
  Zielabweichung mindestens 20 % besser ist, keine andere Größe den Korridor verlässt UND ein
  ZUSÄTZLICHER, nicht in der A/B-Gruppe enthaltener Startwert nicht schlechter ist (neu aus Runde 2).
- **BELEGT:** die Schwellen 20 % und 10 % sind VORSCHLAG, nicht Original.

## 12. Wie dieses Dokument aktuell bleibt (und was offen ist)

**Drei Regeln (aus Runde 2, übernommen):**
1. **Wer einen Schritt abschließt, zieht das Konzept im selben Arbeitsschritt nach** - neue Zahlen mit
   Urteil und Quelle, geänderte Abhängigkeiten, neue OFFEN-Punkte. Freigabe: Daniel.
2. **Vor jedem neuen Schritt wird das Konzept gelesen und gegen den Stand gehalten.** Abweichungen
   werden als offene Punkte notiert und VOR dem Einbau geklärt - nicht danach.
3. **Nach jedem Kennzahlenblatt-Lauf wandern die gemessenen Werte mit Datum in Abschnitt 2.** Der
   Startende trägt sie ein; ohne Eintrag gilt die Messung als nicht geschehen.

**Offene Punkte (Fragen an Daniel, in einer Runde):**
1. **Kontakt** im Rachetopf: jede Interaktion (Handel, Ereignis, Kampf) setzt den Zähler zurück, oder
   nur diplomatische Austausche? (Empfehlung: jede Interaktion.)
2. **Rachetopf unter Pakt:** steigt er weiter und feuert nach Paktende, oder friert er ein?
   (Empfehlung: steigt weiter, feuert frühestens 28.800 s nach Paktende.)
3. **Durchmarsch:** reine Anzeige bleiben, oder echte Mechanik (Bot-Truppen dürfen durchziehen)?
   (Empfehlung: Anzeige - Originalbeleg fehlt, und neue Wegfindung ist ein eigener Schnitt.)
4. **Paktwirkung:** schützt er nur den Spieler, oder sperrt er auch dessen Plünderungen?
   (Empfehlung: beidseitig - ein Pakt ist ein Pakt, und die Aufbauzeit-Zahl wird dadurch ehrlich.)
5. **Priorität:** Diplomatie zuerst fertig (Leerlauf senken) oder Wirtschaft und Forschung
   vervollständigen? (Empfehlung: Diplomatie zuerst, weil der Ablauf steht und der Leerlauf die
   größte gemessene Zahl ist.)

**Verweise (Details, nicht wiederholen):** `docs/PLAN_Einzelspieler.md` (Bauplan),
`docs/ABLAUF_LLM_20261106.md` (Arbeitsreihenfolge), `docs/ENTSCHEIDUNGSVERZEICHNIS.md` (Daniels
Entscheidungen), `docs/PRUEFREGEL_ORIGINAL.md` (Belege), `docs/quellen/` (Originalquellen),
`docs/ABGLEICH_LLM_20261106_runde2.md` (Runde 2), `docs/balancing/README_KENNZAHLEN.md` (Messung),
`docs/KONZEPT_SECHS_DOERFER_20261101.md` und `docs/KONZEPT_DORF_TAKTIKEN_20261102.md` (Detailkonzepte
Bots und Dörfer), `docs/STORY_GESAMTBILD_20261104.md` (Welt und Chronik).
