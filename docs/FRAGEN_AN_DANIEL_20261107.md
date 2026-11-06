# Fragen an Daniel - EINE Runde am 06.11.2026 (Sitzung 06.11.26_V_0.0.2_Session_6)

**Angelegt:** 06.11.2026, 07:5x. **Grundlage:** Auftrag `Weltenfresser_Auftrag.txt` vom Desktop und
Abschnitt 4 der Uebergabe 07:38. **Regel:** alle offenen Entscheidungen in EINER Runde, je Frage
Messlage, Moeglichkeiten mit Folge, Empfehlung zuerst, freie Antwort moeglich.

**Ergebnis: alle fuenf Fragen sind beantwortet.** Die Antworten stehen hier mit ihrer Folge; was
gebaut wurde, steht in Register 260 und in `docs/ENTWICKLUNGSPROTOKOLL.md`.

## Frage 1 - EXE-Name (Widerspruch, belegt)

**Messlage.** Daniel wuenscht V_0.0.2 im EXE-Namen. `data/version.json` nannte
`Nebelseetal_Pre_Release_V_0.0.2.exe`, aber genau diese Datei ist am 05.11.2026, 19:29 als
Pre-Release veroeffentlicht (Tag `v_0.0.2`, 86.984.365 Byte, zwei Downloads); `v_0.0.1` ebenso. Ein
neuer Stand unter demselben Namen haette eine bereits heruntergeladene Fassung ueberschrieben.

- (a) **Empfehlung:** naechster freier Zaehler `V_0.0.3`, Ankuendigung wie gewohnt, `version.json` mitziehen.
- (b) `v_0.0.2` ersetzen (Assets und Tag) - mit Ankuendigung, weil Tester die alte Datei haben.
- (c) In dieser Sitzung keine EXE bauen, erst nach S4/S5.

**Antwort Daniel (06.11.2026):** (a) - neuer Zaehler, V_0.0.3 aus dem S3-Stand, keine Ueberschreibung.

**Folge:** `data/version.json` steht auf `zaehler: 3` und
`Nebelseetal_Pre_Release_V_0.0.3.exe`; das Bauwerkzeug liest den Namen dort. Die Veroeffentlichung
laeuft als eigenes Pre-Release `v_0.0.3` mit eigenen Release-Notizen
(`docs/RELEASE_NOTES_PRE_RELEASE_V_0_0_3.md`).

## Frage 2 - Rundung der Heilungskosten

**Messlage.** 75 Prozent der Kostenposten ergeben Bruchteile (Krieger 262,5 Gold und 0,75 Pferde,
Handkarren je Posten 11,25, Balliste 7,5 Pferde). Gebaut ist die Buchung mit zwei Nachkommastellen
(`verwundete.heilungskosten` rundet auf zwei Stellen, `vorraete` fuehrt Fliesskomma); die Anzeige in
der Kaserne schrieb die Zahl bisher mit Punkt (`%g` - also "0.75 Pferde").

- (a) **Empfehlung:** Kern bleibt ungerundet, Anzeige rundet auf zwei Stellen mit Komma.
- (b) Im Kern abrunden - dann heilt ein Pferd kostenlos, schlecht.
- (c) Kaufmaennisch auf ganze Zahlen runden - jeder Posten kostet mindestens 1.

**Antwort Daniel (06.11.2026):** (a).

**Folge (gebaut):** `hilfen.zahl_de(betrag, stellen=2)` ist die EINE Schreibweise (Komma, hoechstens
zwei Stellen, ganze Zahlen ohne Nachkommastellen). `_heilung_zeile_zeichnen` benutzt sie fuer Preis
und Dauer; Wache: `tests/test_verwundete.py` Abschnitt 11 (sieben Pruefungen), Datei 52/0/0.

## Frage 3 - Welche Modelle bekommen den LLM-Auftrag

**Messlage.** Der Auftrag verlangt den Abgleich mehrerer Modellantworten; Chat-Modelle kosten kein
API-Geld, API-Laeufe fallen unter den Deckel 4,00 USD/Tag.

- (a) **Empfehlung:** zwei bis drei verschiedene Modelle (Gemini, ChatGPT, optional Claude), je Lauf
  dieselbe Datei.
- (b) Nur zwei.
- (c) Nur eines.

**Antwort Daniel (06.11.2026):** (a) - zwei bis drei Modelle; **welche, ist fuer den Auftrag nicht
wichtig**.

**Folge:** die Auftragsdatei nennt keine Modellnamen, sondern nur die Anforderungen an den Lauf
(gleiche Datei, ganze Antwort, keine Rueckfragen, Ablage nach unserem Schema).

## Frage 4 - Was gilt, wenn eine Antwort alte Ablaeufe ersetzt

**Messlage.** Daniel im Auftrag: alte Ablaeufe sind nach der Auswertung eventuell gar nicht mehr
noetig. Gleichzeitig gilt die Projektregel, dass nichts stillschweigend ersetzt wird.

- (a) **Empfehlung:** Abloesen nur als eigener Schnitt mit Beleg (was faellt, was bleibt, was
  migriert), und erst nach dem Abgleich mehrerer Antworten.
- (b) Freie Hand, Pruefung hinterher.
- (c) Alte Ablaeufe bleiben unangetastet, nur Ergaenzungen.

**Antwort Daniel (06.11.2026):** (a).

**Folge:** im LLM-Dokument steht als Pflicht, dass jede Antwort ihre Ablösungen ausdruecklich
benennt (Abschnitt Auftrag, Punkt 6 und die Ablagehinweise in Abschnitt 11).

## Frage 5 - S5 Siedlungsumzug

**Messlage.** `docs/ABLAUF_20261107.md` fuehrt S5 als gesperrt: Gebaeude ziehen mit um, der Preis ist
nicht gerechnet, ohne beides wird nichts gebaut.

- (a) **Empfehlung:** gesperrt lassen, im LLM-Dokument nur als geplant beschreiben.
- (b) Jetzt freigeben, Preis nach Vorschlag.
- (c) Im LLM-Auftrag frei konstruierbar.

**Antwort Daniel (06.11.2026):** (a) - gesperrt, Bau erst nach ausdruecklicher Freigabe und
gerechnetem Preis.

**Folge:** S5 steht im LLM-Dokument als ANGENOMMENER PLAN mit ausdruecklichem Vermerk
"nicht freigegeben" - das Modell darf die Mechanik durchdenken und die Wache beschreiben, aber der
Einbau bleibt gesperrt, bis Daniel Preis und Freigabe gibt.

## Nachtraege

- Alle Antworten der Runde 1 sind am 06.11.2026 in der Sitzung 06.11.26_V_0.0.2_Session_6 eingegangen; die Antworten der Runde 2 (F-1 bis F-5 des Ablaufs) stehen unten.

## Nachtrag 06.11.2026, 11:25 - Antworten der Runde aus Sitzung `06.11.26_V_0.0.3_Session_7`

Fuenf Fragen aus `docs/ABLAUF_LLM_20261106.md` Abschnitt 6, in EINER Runde gestellt und beantwortet.
Die sechste Frage (Sammellauf mit dem Projekt-venv) war keine Entscheidung, sondern eine belegte
Betriebsregel: `.venv/Scripts/python.exe` ist Pflicht, weil dem Hermes-Python `lxml` fehlt und eine rote
Datei in 0,6 s ein Geraetebefund waere.

| Nr | Frage | Antwort Daniels | Folge |
|---|---|---|---|
| F-1 | Grom-Ereignis: Werkzeuge und Eisen gibt es im Spiel nicht | **Eisen meint Erz, mit Werkzeugen sind Messer und dergleichen gemeint.** | Grom tauscht **5 Werkzeug-Waren (Messer und Gleichwertiges) gegen 20 Erz = unser Rohstoff `metall`**. Damit ist V-4 baubar, ohne neue Ware: die Warenliste hat Messer, Dolch, Kurzschwert; Erz ist `metall`. Die Zuordnung wird in `data/diplomatie.json` als Vorschlag mit Begruendung eingetragen. |
| F-2 | A-6-Dauer: gemessen 1.330 s und 1.552 s gegen die Grenze 1.400 s | **Erst beschleunigen (`--parallel`), Grenze vorlaeufig 1.800 s.** | Schritt 12 des Ablaufs: Parallelbetrieb bauen und nachweisen (gleiche Ergebnisliste bei `--parallel 1` und `4`), A-6 nennt bis dahin 1.800 s als VORSCHLAG. Kein stilles Senken der Erwartung. |
| F-3 | Rachetopf nach einem Bot-Sieg | **Topf auf 0 setzen.** | `data/diplomatie.json` bekommt `nach_bot_sieg: 0`; eine Wache prueft, dass der Topf nach einem Sieg genau 0 ist. |
| F-4 | Startwert der Gunst ohne Originalbeleg | **50 als VORSCHLAG eintragen und so lassen.** | Bleibt `start: 50` mit eigener `start_quelle` in `data/diplomatie.json` (VORSCHLAG, Mitte des mittleren Bereichs). |
| F-5 | Kennzahlenblatt direkt nach Schritt 1 (Gunst)? | **Ja, als Schritt 2.** | Der Ablauf bleibt in seiner Reihenfolge; das Kennzahlenblatt liefert die Vorher-Zahlen fuer Rachetopf, Vertraege und Ereignisse. |

## Nachtrag 06.11.2026, 11:32 - Zweite Runde (Skill-Freigaben, Runde 2, Release, Grom-Detail)

| Nr | Frage | Antwort Daniels | Folge |
|---|---|---|---|
| F-7 | Zwei Skill-Vormerkungen (`6cd198de`, `262966e1`) | **Beide freigegeben.** | Die fuenf Lehren der Sitzung 6 stehen bereits als Abschnitt im Skill und als `references/lehren-2026-11-06.md` (5 Abschnitte, 2.585 Byte) - nichts nachzutragen. Die **acht Lehren der Nacht S3** (`6cd198de`) existieren dagegen in KEINER Datei: die Vorgaengeruebergabe nennt sie, geschrieben wurden sie nie. Sie sind nur aus den Protokollzeilen der Nacht zu rekonstruieren - das ist Arbeit der naechsten Sitzung, nicht zu erfinden. |
| F-8 | Wann geht der KI-Auftrag Runde 2 an die externen Modelle? | **Erst nach S4 komplett** (Schritte 1 bis 5 gebaut). | Der Auftrag liegt fertig auf dem Desktop; er wird erst mit dem dann neueren Stand verschickt. Bis dahin bleibt er liegen, nichts wird daran geaendert. |
| F-9 | Wann neue EXE und Release? | **Erst nach S4 komplett** (Gunst, Vertraege, Rachetopf, Ereignisse, Handelspunkte). | Kein Release nach S4 Teil 1. Die veroeffentlichte `V_0.0.3` bleibt die aktuelle Fassung; die naechste Version bekommt den naechsten Zaehler. |
| F-10 | Grom-Detail: welche Werkzeug-Ware? | **5 Messer gegen 20 Erz** (= Rohstoff `metall`), Messer ist die guenstigste Werkzeug-Ware. | Damit ist das Ereignis vollstaendig bestimmt: Ware `Messer`, Menge 5, Gegenleistung Rohstoff `metall`, Menge 20. |
