# Entscheidungen Daniel - Gemini-Input, eine Runde (06.11.2026, 01:20 bis 01:31)

**Form:** ein Auswahlformular, neun Fragen, zwei Blaetter derselben Runde
(`docs/FRAGEN_AN_DANIEL_20261106_GEMINI.md`). Antworten hier **woertlich**, je mit Folge.
**Regel:** Antworten gelten als Vorgabe; was sie verlangen, aber nicht zum laufenden Schnitt gehoert,
wird als eigener kommender Schnitt vermerkt und nicht nebenbei eingebaut.

| Nr. | Frage | Antwort Daniels (woertlich) | Folge |
|---|---|---|---|
| 1 | Reihenfolge der sechs uebernehmbaren Stuecke | "A (Empfehlung): Postfach-Archiv und Ruhm-Balken zuerst (klein, reine Anzeige), dann Mauerreparatur und Heilung, dann Diplomatie als eine Runde" | Baufolge: **B-3 Postfach-Archiv** und **B-8 Ruhm-Balken** zuerst, danach B-4 Mauerreparatur, B-5 Verwundetenheilung, zuletzt B-1 und B-2 als eine Diplomatie-Runde. A1b/A2 laufen unabhaengig weiter. |
| 2 | Mauerreparatur: Modell und Preis | "A: Reparatur kostet Holz und Stein UND Spielzeit (Wall steht still), nur in der eigenen Siedlung" | Reparatur bindet Zeit: der Wall hat einen Reparaturzustand, waehrend dessen er nicht schuetzt oder nicht weitergebaut wird. Zahlen (Holz, Stein, Stunden je Prozent Zustand) werden im Paket als VORSCHLAG aus unseren Daten gerechnet, nicht aus der KI uebernommen. |
| 3 | Verwundetenheilung: Quote und Preis | "A (Empfehlung): 30 % der Gefallenen verwundet, heilbar gegen Gold und Spielzeit in der Kaserne" | 30 Prozent der Verluste eines Gefechts werden als Verwundete gefuehrt; Heilung kostet Gold und Spielstunden in der Kaserne. Kein Sofort-Heilen. Aufbauzeit bleibt unberuehrt (Leitlinie 237). |
| 4 | Diplomatie: Gunst, Status, Vertraege | "A (Empfehlung): Gunst 0-100, drei Statusstufen, drei Vertraege (NAP ab Gunst 40, Durchmarsch 60, Handelsabkommen 30), Bruch senkt Gunst und fuellt Kranks Rachekonto" | Gunstskala 0 bis 100, Status feindselig/wachsam/freundlich, drei Vertraege mit den genannten Mindestwerten; Bruch kostet 20 Gunst und speist den Rachetopf (Frage 5). |
| 5 | Rachetopf: Wachstum und Ausloeser | "A (Empfehlung): +1 je erlittener Niederlage, +1 je Spieltag ohne Kontakt, ab 3 angekuendigter Angriff; Rache faellt bei einem Bot-Sieg" | Rache als Zahl im Bot-Gedaechtnis, Ankuendigung bei 3, Loeschung durch einen Bot-Sieg. Ergaenzt `bottaktik.gedaechtnis` - EINE Speicherstelle, keine zweite. |
| 6 | Diplomatie-Events: Forderungen und Fristen | "A (Empfehlung): drei Ereignisse - Haugs Tribut (Holz oder Gold, 2 Spieltage Frist), Groms Handelsangebot, Silras Informationsverkauf; Ablehnung senkt Gunst, Angriff folgt nur wenn die Bot-Armee es hergibt" | Drei Ereignisse ueber die vorhandene Overlay-Technik, Frist 2 Spieltage; keine im Code festgeschriebene Rachearmee. |
| 7 | Etappen-Reise ueber das Portal | "A (Empfehlung): erst A2 messen, dann entscheiden; wenn ja, Etappen mit denselben Geschwindigkeiten (keine neue Zahl)" | **Nicht bauen.** Zuerst A2 Messpflicht-Tabelle; danach erneut vorlegen. Neue Zahlen sind ausgeschlossen. |
| 8 | Siedlungsumzug | "B: Umzug gegen Siedler und Portalkosten, Zielkarte zufaellig" | **Abweichung von der Empfehlung, Daniels Entscheidung gilt.** Siedlungsumzug wird gebaut: Kosten in Siedlern und Portalkosten, Zielkarte zufaellig gezogen. Beruehrt die Kartenregel (Register 228/229) und wird ein **eigener Schnitt** - nicht nebenbei, weil er Kartenziehen, Siedler und Portalkosten gleichzeitig anfasst. |
| 9 | `pathlib` und Type Hints | "A (Empfehlung): Regel fuer neuen Code, bestehende Dateien beim naechsten Anfassen mitziehen - kein eigener Umbau" | Kein Aufraeumschnitt; die Regel gilt fuer neuen Code und beim Anfassen. |

**Was daraus als naechstes gebaut wird (in dieser Reihenfolge, je mit den sieben Phasen):**
1. **B-3 Postfach-Archiv** (Filter, Archiv, Ablauf; Militaerberichte bleiben) - kleinste Wirkung, kein Balancing.
2. **B-8 Ruhm-Fortschrittsbalken** (auf `punkte.auszeichnungen`, mit `tk.Canvas`).
3. **B-4 Mauerreparatur** nach Entscheidung 2.
4. **B-5 Verwundetenheilung** nach Entscheidung 3.
5. **B-1 und B-2 Diplomatie** als eine Runde, mit dem Rachetopf aus Entscheidung 5.
6. **B-7 Siedlungsumzug** als eigener Schnitt nach Entscheidung 8 (Kartenregel zuerst pruefen).
7. **B-6 Etappen-Reise:** gesperrt bis A2 gemessen ist (Entscheidung 7).

**Nicht gebaut, nicht vergessen:** T-4 (Dimensionen) ist erledigt, B-9 haengt an B-3, B-10 ist eine Regel.
