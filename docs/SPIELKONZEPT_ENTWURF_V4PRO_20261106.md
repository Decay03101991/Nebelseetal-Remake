# Aufgabe 1 - Entscheidungen zu den Streitpunkten A bis H

## A Schwächster Schritt
**Entscheidung:** Schritt 7 (Bot-Lücken) ist der schwächste Schritt.

**Begründung:** Zwei unabhängige Prüfungen (Grok und AI Collaborator) benennen Schritt 7 als schwächsten Schritt, und zwar mit unterschiedlichen, aber konkret benannten Risiken: Doppelauslöser von Racheangriff und Drachenzug sowie dauerhaftes Einfrieren eines Bots im Spionage-Wartezustand. Schritt 7 bündelt drei Verhaltenswege in einem Schritt und hat die größte Wirkung auf das Spielgefühl, da der gemessene Leerlauf (92 %) vor allem aus passiven Bots resultiert. Schritt 9 (Regelkreis) ist später korrigierbar, Schritt 4 (Rachetopf) ist in seinem Umfang kleiner.

**Folge:** Schritt 7 wird in kleinere Arbeitspakete zerlegt (zuerst Reaktion und Spionage-Wartezustand, dann Drache). Die Wache für Schritt 7 muss einen Bot über mehrere Spieltage beobachten und prüfen, dass er nicht einfriert und nicht doppelt angreift.

## B Zusätzliche Abhängigkeit
**Entscheidung:** Die zusätzliche Abhängigkeit von GPT (Schritt 7 muss zusätzlich von Schritt 4 abhängen) gilt. Zusätzlich wird die Kontakt-Definition aus Collaborators Vorschlag in Schritt 4 aufgenommen, ohne die Reihenfolge umzudrehen.

**Begründung:** Der Rachetopf (Schritt 4) erzeugt einen speziellen Angriffsauftrag, der mit den normalen Bot-Verhaltenswegen (Schritt 7) kollidieren kann. Ohne diese Abhängigkeit entstehen Doppelangriffe oder widersprüchliches Verhalten. Collaborators Punkt ist berechtigt, weil Kontakt im Ablauf nirgends definiert ist, aber die Lösung ist eine Definition innerhalb von Schritt 4, nicht eine Verschiebung von Schritt 5 vor 4.

**Folge:** Ablauf-Tabelle ändern: Schritt 7 erhält als Abhängigkeit zusätzlich 4. Schritt 4 erhält den Auftrag, den Begriff Kontakt verbindlich zu definieren, bevor der Rachetopf implementiert wird.

## C Schritt streichbar
**Entscheidung:** Keiner der Schritte 1 bis 13 ist streichbar.

**Begründung:** Groks Vorschlag, Schritt 8 (Sollkurve) zu streichen, würde den Regelkreis (Schritt 9) ohne belastbare Referenz lassen. Die Sollkurve aus den gemessenen Daten ist notwendig, um später ein A/B-Urteil überhaupt fällen zu können. Die anderen Modelle sehen ebenfalls keinen verzichtbaren Schritt.

**Folge:** Schritt 8 bleibt erhalten, wird aber als schlanker Datenaufbereitungsschritt verstanden, der die vorhandenen Kennzahlen in eine Referenzkurve überführt, nicht als aufwändige neue Simulation.

## D Aufbauzeit Schritt 3
**Entscheidung:** Collaborators Position ist teilweise richtig: Ein Nichtangriffspakt kann die Aufbauzeit erhöhen, wenn der Spieler dadurch auf Plünderungen verzichtet.

**Begründung:** Die pauschale Aussage senkt sie im Ablauf ist falsch, weil ein NAP dem Spieler die Möglichkeit nimmt, den Bot zu plündern. GPTs bedingt ist zu vage, Collaborator liefert den konkreten Mechanismus. Der Effekt hängt von der Spielerstrategie ab.

**Folge:** Text im Ablauf korrigieren: Aufbauzeit Schritt 3 ist uneindeutig und hängt von der Spielerstrategie ab. Ein NAP senkt sie nur, wenn er Verteidigungsausgaben erspart; er erhöht sie, wenn er Plünderungen verhindert.

## E Aufbauzeit Schritt 4
**Entscheidung:** GPTs Position gilt: Schritt 4 kann die Aufbauzeit erhöhen, nicht nur Druck ausüben.

**Begründung:** Ein ausgelöster Racheangriff kostet den Spieler nachweislich Einheiten und Zeit, was die Aufbauzeit direkt verlängert. Die Aussage nur Druck ist daher nicht belegt.

**Folge:** Text im Ablauf korrigieren: Schritt 4 kann die Aufbauzeit erhöhen, belegt durch mögliche Einheitenverluste und Zeitaufwand für Verteidigung.

## F Aufbauzeit Schritt 5
**Entscheidung:** GPTs Position ist teilweise richtig: Schritt 5 ist nicht pauschal neutral, weil die Annahme von Ereignissen Rohstoffe kosten kann.

**Begründung:** Die Ereignisse Haug und Silra verlangen bei Annahme Rohstoffabgaben, was direkt die Aufbauzeit beeinflusst. Ablehnung hat andere Kosten (Gunstverlust). Grok sagt neutral, übersieht aber diese Kosten.

**Folge:** Text im Ablauf korrigieren: Schritt 5 Aufbauzeit ist abhängig von Annahme oder Ablehnung der Ereignisse. Annahme kann die Aufbauzeit erhöhen, Ablehnung kann sie senken, aber verursacht Gunstverlust.

## G Wechselwirkung
**Entscheidung:** Groks Tick-Reihenfolge ist der zentrale Punkt, GPTs Ereignis-NAP-Kette ist ein wichtiger Spezialfall. Collaborators Profil-Bruch und Geminis NAP-Topf-Einfrieren sind nachrangig.

**Begründung:** Alle vier Wechselwirkungen haben dieselbe Wurzel: Im Tageswechsel ist die Reihenfolge von Gunständerungen, Vertragsbruch, Rachetopf-Tick und Bot-Aktionen nicht festgelegt. GPT zeigt, wie eine Ereignis-Ablehnung unter einem NAP zu einer Doppelbuchung führt. Grok zeigt, dass dadurch der Vorlauf für den Racheangriff unklar wird. Collab und Gemini beschreiben Sonderfälle, die sich durch eine klare Tick-Reihenfolge auflösen.

**Folge:** Ein zentraler Tageswechsel-Prozess wird definiert, der die Reihenfolge festlegt: Ereignis-Auswirkungen, Gunst und Status, Vertragsbruch-Prüfung, Rachetopf-Tick, danach Bot-Aktionen. Dieser Prozess wird als Unterpunkt in Schritt 4 aufgenommen und in Schritt 7 referenziert.

## H Aussagekraft der Wachen
**Entscheidung:** Die einhellige Position gilt: Quellwachen und statistische Wachen reichen nicht aus.

**Begründung:** Alle vier Modelle bemängeln, dass bisherige Wachen nur das Vorhandensein von Aufrufen prüfen, nicht die Wirkung am echten Pfad. Das zeigt sich konkret bei Schritt 2 (Determinismus nur für Eingaben), Schritt 4 (Wache setzt Auftrag selbst) und Schritt 7 (Wache prüft nur, dass ein Auftrag entsteht, nicht dass er ausgeführt wird).

**Folge:** Wachen werden zu dynamischen Verhaltensprüfungen ausgebaut: Integrationstests, die über mehrere Spieltage laufen und das tatsächliche Bot-Verhalten, die Buchung von Handelspunkten und die Reihenfolge im Tageswechsel prüfen.

# Aufgabe 2 - Der beste Weg für das Spiel

Die nächste Arbeit sollte die Diplomatie-Mechaniken in dieser Reihenfolge umsetzen: Schritt 3 (Verträge), Schritt 4 (Rachetopf inklusive Kontaktdefinition), Schritt 5 (Ereignisse), dann Schritt 7 (Bot-Lücken). Grund: Verträge und Rachetopf erzeugen unmittelbar Entscheidungsdruck und aktive Bot-Aktionen, während Ereignisse zusätzliche Abwechslung bringen. Schritt 7 baut auf der geklärten Tick-Reihenfolge auf und vermeidet so Doppelangriffe.

Zuerst messen würde ich:

1. **Leerlaufanteil** in Prozent der Spielsekunden. Aktuell gemessen: 92 % (956.400 von 1.036.800 Spielsekunden). Die Kennzahl muss sinken, VORSCHLAG Ziel unter 50 %.
2. **Längste Strecke ohne neuen Meilenstein** in Spieltagen. Aktuell gemessen: 5,347 Spieltage. Die Kennzahl muss sinken, VORSCHLAG Ziel unter 1,5 Spieltage.
3. **Entscheidungsdichte** in Anzahl spielerrelevanter Entscheidungen pro Spieltag (z. B. Ereignisangebote, Vertragsoptionen, Rachewarnungen). Aktuell nicht gemessen, VORSCHLAG Ziel mindestens 2 Entscheidungen pro Spieltag.

Die Kennzahl, die sich als erstes ändern muss, ist der Leerlaufanteil: Er ist der deutlichste Hinweis darauf, dass das Spielgefühl unter passiven Gegnern leidet. Richtung: deutlich reduzieren.

# Aufgabe 3 - Das zentrale Spielkonzept

Die Datei docs/SPIELKONZEPT.md erhält folgende Gliederung mit 12 Kapiteln. Zu jedem Kapitel werden drei bis fünf Kernaussagen formuliert, die jeweils als BELEGT, VORSCHLAG oder OFFEN markiert sind.

## Kapitel 1: Vision und Spielerlebnis
- Kernaussagen: Ziel ist ein portables, offline spielbares Einzelspieler-Remake des Originals. BELEGT: Ein Sieg ist bewusst nicht vorgesehen, jede Partie endet nach eigenen Zielen. VORSCHLAG: Das Spielgefühl soll durch aktive Diplomatie und regelmäßige Entscheidungen geprägt sein. OFFEN: Endgültige Zieldefinition für eine erfüllte Partie.

## Kapitel 2: Ausgangslage und gemessener Stand
- BELEGT: Version V_0.0.3, Commit 11d41ab, Kennzahlenblatt aus Partie Saat 7: Leerlauf 92 %, erstes Gefecht Spieltag 2,0, Ruhm-Stufe 2. BELEGT: Sammellauf 1.290 s ohne Nebenlast, 2.363 s mit Nebenlast. OFFEN: Dauerhafte Optimierung der Sammellaufzeit.

## Kapitel 3: Originaltreue und Belegsystem
- BELEGT: Regel aus Abschnitt 1: Jede Zahl wird gegen eine Quelle gehalten, Urteil BELEGT, WIDERSPRUCH, NICHT BELEGT oder VORSCHLAG. BELEGT: Fehlende Quelle führt nicht zu erfundenen Zahlen. OFFEN: Vollständiges Belegregister für alle Daten in data/.

## Kapitel 4: Wirtschaft und Siedlungsaufbau
- BELEGT: Jede Siedlung hat ein eigenes Lager, die Reichsanzeige ist die Summe der Orte. BELEGT: Erste fertige Ware im Kennzahlenblatt Spieltag 7,833. VORSCHLAG: Ausbaukosten und Warenketten müssen im Einklang mit dem Original bleiben. OFFEN: Keine Werkzeuge und kein Eisen im Spiel, Grom tauscht 5 Messer gegen 20 Erz.

## Kapitel 5: Forschung, Waren und Einheiten
- BELEGT: Punkteformel: Forschung Stufe hoch drei, Krieg Einheitenwerte plus Wallstufe hoch drei, Gesamt halbe Summe. BELEGT: Kurzschwert braucht Waffentechnik 3, erste Bibliothek Spieltag 0,042. VORSCHLAG: Weitere Waren und Einheiten folgen der Originalstruktur.

## Kapitel 6: Diplomatie: Gunst, Status und Verträge
- BELEGT: Jeder Bot hat Gunst 0 bis 100, Start 50, Status wird gerechnet, nie gespeichert. BELEGT: Status feindselig unter 40, wachsam 40 bis 59, freundlich ab 60. VORSCHLAG: Verträge: Nichtangriffspakt ab Gunst 40, Handelsabkommen ab 40, Durchmarsch ab 60 als reine Anzeige. OFFEN: Durchmarsch-Mechanik bleibt vorerst Anzeige.

## Kapitel 7: Rachetopf und angekündigter Angriff
- BELEGT: Rachetopf plus 1 je Niederlage und je Spieltag ohne Kontakt, ab 3 Ankündigung, Angriff erst ab Armee 99 SK. BELEGT: Gemessen G-2: 99 SK, nicht 90. OFFEN: Definition von Kontakt muss verbindlich festgelegt werden. OFFEN: Tick-Reihenfolge im Tageswechsel.

## Kapitel 8: Ereignisse: Haug, Grom, Silra
- BELEGT: Ereignisse haben Frist, Annahme Gunst plus 5, Ablehnung oder Ablauf minus 5. BELEGT: Haug und Silra kosten bei Annahme Rohstoffe. OFFEN: Häufigkeit und Auslösebedingungen der Ereignisse.

## Kapitel 9: Handelspunkte
- BELEGT: Handelspunkte 1 Punkt je 100 Gold Erlös, Verfall 1 je 24 Spielstunden. BELEGT: Gemessen G-8: gold_erloes wird nirgends geschrieben, Handelspunkte bleiben null. OFFEN: Doppelbuchung beim Speichern und Laden muss in Schritt 6 geprüft werden.

## Kapitel 10: Bot-Verhalten und Lücken
- BELEGT: Aktuell passive Bots, Leerlauf 92 %. BELEGT: Drache, Spionage und Reaktion sind offene Punkte aus Schritt 7. VORSCHLAG: Bot-Profile sollen in Schritt 7 eingeführt werden. OFFEN: Verhinderung von Einfrieren im Spionage-Wartezustand.

## Kapitel 11: Balance, Sollkurve und Regelkreis
- BELEGT: Schritt 8 Sollkurve aus den Daten, Schritt 9 Regelkreis mit A/B-Urteil. BELEGT: Derzeit keine belastbare Sollkurve vorhanden. OFFEN: Auswahl der Startwerte für repräsentative Tests.

## Kapitel 12: Regeln für Aktualität und offene Punkte
- BELEGT: Das Konzept wird bei jedem abgeschlossenen Schritt aktualisiert. VORSCHLAG: Automatische Übernahme von Kennzahlen aus dem Kennzahlenblatt. OFFEN: Verantwortlichkeiten für Pflege sind festzulegen.

# Aufgabe 4 - Was du aus den vier Prüfungen NICHT übernimmst

| Vorschlag | Modell | Grund der Ablehnung |
|---|---|---|
| Kennzahlenblatt nach Verträgen kalibrieren, also Schritt 2 nach Schritt 3 | Gemini | Widerspricht der Messlogik: Basisdaten müssen vor dem Einbau neuer Mechaniken stehen, sonst wird die Ausgangslage verfälscht. |
| Schritt 8 Sollkurve streichen | Grok | Ohne Sollkurve fehlt dem Regelkreis aus Schritt 9 die belastbare Referenz; ein A/B-Urteil würde auf bloßen Meinungen basieren. |
| Schritt 5 vor Schritt 4 legen | AI Collaborator | Führt zu Zirkularität, weil Schritt 4 die Kontaktdefinition braucht, die in Schritt 5 verwendet wird. Die Definition kann in Schritt 4 erfolgen, ohne die Reihenfolge zu ändern. |
| NAP friert Rachetopf ein | Gemini | Dieser Vorschlag ist nicht durch das Original belegt und würde den Rachetopf zu stark abschwächen. Die Klärung der Tick-Reihenfolge löst das Problem sauberer. |

# Aufgabe 5 - Regeln, damit das Konzept aktuell bleibt

1. **Regel der Schrittverantwortung:** Jeder, der einen Ablauf-Schritt abschließt, muss im selben Arbeitsschritt die betroffenen Kapitel des Spielkonzepts aktualisieren. Dazu gehören neue Zahlen mit Quelle (BELEGT, VORSCHLAG oder OFFEN) und geänderte Abhängigkeiten. Verantwortlich ist der Umsetzer des Schritts, die Freigabe erfolgt durch Daniel.

2. **Regel der Vorab-Prüfung:** Vor Beginn jedes neuen Schritts liest der Umsetzer das Spielkonzept und vergleicht es mit dem aktuellen Stand. Ergeben sich Abweichungen, werden diese als Tickets erfasst und vor dem Einbau geklärt. Verantwortlich ist der Auftragnehmer des nächsten Schritts, die Kontrolle liegt bei Daniel.

3. **Regel der Kennzahlen-Pflege:** Nach jedem Sammellauf oder jedem Kennzahlenblatt-Lauf werden die gemessenen Werte im Kapitel Ausgangslage und gemessener Stand eingetragen, mit Zeitstempel und Belegstatus. Verantwortlich ist derjenige, der den Sammellauf startet, die Freigabe erfolgt durch Daniel.

# Aufgabe 6 - Offene Fragen an Daniel

## Frage 1: Definition von Kontakt im Rachetopf
**Empfehlung zuerst:** Möglichkeit A.
Möglichkeit A: Jede Interaktion mit dem Bot (Handel, Ereignis, Kampf) setzt den Zähler für Spieltag ohne Kontakt zurück. Folge: Der Rachetopf wächst nur bei tatsächlicher Funkstille, der Druck bleibt bestehen, aber nicht künstlich.
Möglichkeit B: Nur diplomatische Austausche (Vertragsangebot, Ereignis) gelten als Kontakt. Folge: Der Topf steigt schneller, wenn der Spieler nur kämpft, was zu mehr Racheangriffen führt.

## Frage 2: Rachetopf und aktiver Nichtangriffspakt
**Empfehlung zuerst:** Möglichkeit A.
Möglichkeit A: Der Rachetopf steigt auch während eines NAP weiter, der Angriff wird aber erst nach Ablauf des NAP ausgelöst. Folge: Der Druck bleibt erhalten, Verträge schützen nur vor sofortigen Angriffen.
Möglichkeit B: Der Rachetopf friert während eines NAP ein. Folge: Verträge neutralisieren den Rachemechanismus vollständig und machen ihn wirkungslos.

## Frage 3: Durchmarsch-Vertrag
**Empfehlung zuerst:** Möglichkeit A.
Möglichkeit A: Durchmarsch bleibt reine Anzeige ohne Mechanikwirkung. Folge: Geringerer Aufwand, hohe Originaltreue, keine neuen Wegfindungsprobleme.
Möglichkeit B: Durchmarsch erlaubt Bot-Einheiten, Spielergebiet zu durchqueren, ohne Kampf. Folge: Mehr Tiefe, aber erfordert neue Wegfindung und Kollisionsregeln.

## Frage 4: Balance-Zahlen für neue Mechaniken
**Empfehlung zuerst:** Möglichkeit A.
Möglichkeit A: Jede neue Zahl muss belegt sein, sonst wird sie als VORSCHLAG mit Rechenweg ausgewiesen. Folge: Strikte Originaltreue, aber möglicherweise langsamer Fortschritt.
Möglichkeit B: Für neue Mechaniken dürfen Zahlen frei vorgeschlagen werden, wenn sie im Geist des Originals sind. Folge: Schnellere Anpassung, aber höheres Risiko von Abweichungen.

## Frage 5: Priorität Spielgefühl versus Vollständigkeit
**Empfehlung zuerst:** Möglichkeit A.
Möglichkeit A: Diplomatie zuerst ausbauen, um den Leerlauf (92 %) und die längste Strecke ohne Meilenstein (5,347 Spieltage) zu reduzieren. Folge: Schnell mehr Interaktion und Entscheidungen, aber Wirtschaft und Forschung bleiben vorerst unvollständig.
Möglichkeit B: Erst Wirtschaft und Forschung vervollständigen, danach Diplomatie. Folge: Tieferes Wirtschaftssystem, aber der Leerlauf bleibt länger bestehen und das Spielgefühl leidet.