# Fragen an Daniel - Gemini-Input, eine Runde (06.11.2026)

**Zweck:** alle Entscheidungen, die der Gemini-Input aufwirft, in EINER Runde. Jede Frage nennt
Messlage, zwei bis drei Moeglichkeiten **mit Folge** und eine Empfehlung. Freie Antwort ist immer
moeglich. Grundlage: `docs/eingaenge/GEMINI_INPUT_20261106/` (besonders `05_BEWERTUNG.md`).

**Regel, die fuer alle neun gilt:** nichts wird gebaut, bevor die Antwort hier steht (Register 238/239,
sieben Phasen). Zahlen aus dem Gemini-Entwurf sind erfunden und werden nicht uebernommen.

---

## Frage 1 - Reihenfolge der sechs uebernehmbaren Stuecke

**Messlage:** sechs Stuecke sind brauchbar und keines haengt an einem anderen:
B-3 Postfach-Archiv (S), B-8 Ruhm-Balken (S), B-4 Mauerreparatur (M), B-5 Verwundetenheilung (M),
B-1 Diplomatie mit Vertraegen (L), B-2 Diplomatie-Events (M, sinnvoll nur mit B-1).

**Moeglichkeiten:**
- **A (Empfehlung):** B-3 und B-8 zuerst (klein, reine Anzeige, kein Balancing), dann B-4 und B-5
  (brauchen deine Zahlen), dann B-1 und B-2 als eine Diplomatie-Runde.
- **B:** Diplomatie zuerst - groesste Wirkung, aber sie bindet dich fuer Zahlen und dauert am laengsten.
- **C:** nur die zwei kleinen Anzeigen (B-3, B-8) und danach zurueck zu A1b/A2.

**Folge von A:** zwei kleine Schnitte sind schnell sichtbar, der Aufbau bleibt unberuehrt.
**Empfehlung:** A.

## Frage 2 - Mauerreparatur: Modell und Preis

**Messlage:** der Wall rechnet in Stufe + Zustand in Prozent (`wall_zustand`); das Handbuch sagt nichts
zur Reparatur (`kampfbericht.py:566`). 0 Wallschaden in allen bisherigen Laeufen - beurteilbar erst
mit A3.

**Moeglichkeiten:**
- **A (Empfehlung):** Reparatur kostet Holz und Stein und **Spielzeit** (Wall steht still, solange
  repariert wird); kein Deckel pro Tag, aber nur in der eigenen Siedlung.
- **B:** Reparatur kostet nur Rohstoffe, sofort - einfach, aber fast kostenlos im Spielgefuehl.
- **C:** erst bauen, wenn A3 echten Wallschaden zeigt (dann mit gemessener Zahl statt Bauchgefuehl).

**Folge von A:** der Wall wird ein Posten in der Wirtschaft, nicht ein Knopf.
**Empfehlung:** C ist ehrlich, A ist besser, sobald A3 steht. Wenn du jetzt willst: A.

## Frage 3 - Verwundetenheilung: wie viel und zu welchem Preis

**Messlage:** Heilung existiert nicht; `Heilkunde` ist Siedlerproduktion +10 Prozent je Stufe.
Verluste sind heute endgueltig. Leitlinie 237: der Aufbau darf NICHT kuerzer werden.

**Moeglichkeiten:**
- **A (Empfehlung):** 30 Prozent der Gefallenen sind verwundet und heilbar, gegen Gold und Zeit in
  der Kaserne; Heilung laeuft ueber Spielstunden, nicht sofort.
- **B:** 50 Prozent heilbar, ohne Zeitanteil (nur Gold) - schneller, aber entwertet Verluste.
- **C:** 20 Prozent, nur nach einem gewonnenen Gefecht - am haertesten.

**Folge von A:** Kaempfe bleiben teuer, Verluste sind nicht endgueltig; keine Verkuerzung des Aufbaus,
weil Heilung Zeit UND Gold bindet.
**Empfehlung:** A.

## Frage 4 - Diplomatie: Gunst, Status, Vertraege

**Messlage:** die Ansicht zeigt je Bot nur Handel und Aggression in Prozent und zwei Knoepfe
(`main.py:13135`); Vertraege gibt es nicht.

**Moeglichkeiten:**
- **A (Empfehlung):** Gunstskala 0 bis 100, drei Statusstufen (feindselig, wachsam, freundlich),
  drei Vertraege: Nichtangriffspakt (Mindestgunst 40), Durchmarschrecht (60), Handelsabkommen (30);
  Bruch senkt Gunst um 20 und fuellt Kranks Rachetopf.
- **B:** nur Gunst und Status, keine Vertraege - halber Aufwand, aber ohne echte Entscheidung.
- **C:** Vertraege ohne Gunstskala, jeder Nachbar hat feste Neigungen.

**Folge von A:** die Ansicht wird ein Verhandlungsfeld; die Zahlen sind Vorschlag und im Register
als VORSCHLAG zu fuehren.
**Empfehlung:** A.

## Frage 5 - Diplomatie-Events: Forderungen und Fristen

**Messlage:** Overlay-Technik vorhanden (35 Stellen), aber kein Ereignis fordert eine Antwort.

**Moeglichkeiten:**
- **A (Empfehlung):** drei Ereignisse zum Start - Haugs Tribut (Holz oder Gold, Frist 2 Spieltage),
  Groms Handelsangebot (Ware gegen Gold), Silras Informationsverkauf (Gold gegen Aufklaerung);
  Ablehnung senkt die Gunst, ein Angriff folgt erst, wenn die Bot-Armee es hergibt (keine feste Armee
  im Code).
- **B:** nur ein Ereignis als Muster, Rest spaeter.
- **C:** keine Events, nur Vertraege.

**Folge von A:** der Spieler entscheidet unter Zeitdruck; die Bot-Armee bleibt aus der Bot-Wirtschaft.
**Empfehlung:** A, aber erst nach Frage 4.

## Frage 6 - Rachetopf: waechst die Rache, und ab wann greift der Bot zurueck

**Messlage:** das Gedaechtnis `geschlagen_von` ist gebaut (`bottaktik.py:345/566`), der Zustand
`RAECHEN` greift den gemerkten Schaediger an (`:483`). Es fehlt die **Menge**.

**Moeglichkeiten:**
- **A (Empfehlung):** Rache +1 je erlittener Niederlage, +1 je Spieltag ohne Kontakt, ab 3 ein
  angekuendigter Angriff; Rache faellt bei einem Sieg des Bots.
- **B:** Rache nur je Niederlage, kein Verfall - der Bot bleibt feindlich.
- **C:** Rache je verlorener Beute (Grammgenau, aber schwer erklaerbar).

**Folge von A:** "Krank vergisst nichts" wird zu einer Zahl mit Ankuendigung; der Spieler kann sie
durch einen Sieg loeschen.
**Empfehlung:** A.

## Frage 7 - Etappen-Reise ueber das Portal

**Messlage:** kein Etappenbegriff im Code; eine Reise ist heute EINE Strecke. Eine Etappe
**verlaengert** Reisen - das beruehrt Leitlinie 237 und die Messpflicht-Tabelle A2.

**Moeglichkeiten:**
- **A (Empfehlung):** erst A2 messen, dann entscheiden; wenn ja, Etappe = Siedlung, Portal der
  Ausgangswelt, Portal der Zielwelt, Ziel, mit denselben Geschwindigkeiten (keine neue Zahl).
- **B:** Etappen jetzt bauen mit Aufschlag (50 Mana war der Vorschlag der KI - erfunden).
- **C:** keine Etappen, Reisen bleiben eine Strecke.

**Folge von A:** keine Verlaengerung ohne Messung; Zahlen entstehen aus unseren Daten.
**Empfehlung:** A.

## Frage 8 - Siedlungsumzug

**Messlage:** es gibt Gruenden, Aufgeben (ab sechs Siedlungen) und den Weltensprung des Dorfes, aber
kein Versetzen einer bestehenden Siedlung.

**Moeglichkeiten:**
- **A (Empfehlung):** nicht bauen - der feste Platz ist Teil der Kartenentscheidung (Register 228/229).
- **B:** Umzug gegen Siedler und Portalkosten, Zielkarte zufaellig.
- **C:** Umzug nur innerhalb derselben Welt auf ein freies Feld.

**Folge von A:** keine neue Mechanik, die das Kartenziehen entwertet.
**Empfehlung:** A.

## Frage 9 - Aufraeumschnitt `pathlib` und Type Hints

**Messlage:** 14 von 60 Modulen nutzen `pathlib`, 767 `def`-Zeilen tragen Rueckgabetypen.
Kein Spielnutzen.

**Moeglichkeiten:**
- **A (Empfehlung):** Regel fuer NEUEN Code, bestehende Dateien beim naechsten Anfassen mitziehen -
  kein eigener Umbau-Schnitt.
- **B:** eigener Aufraeumschnitt ueber alle 60 Module.
- **C:** nicht verfolgen.

**Folge von A:** kein Risiko fuer gruene Wachen, kein Nutzenverlust.
**Empfehlung:** A.

---

**Antworten bitte in einer Runde.** Was du nicht beantwortest, bleibt liegen (kein Bau) - der
dokumentierte Stand gilt weiter.
