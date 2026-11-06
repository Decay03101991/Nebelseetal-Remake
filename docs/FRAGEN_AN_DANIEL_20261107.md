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

## Nachtrag 13:50 - fuenf Antworten (Runde 2 des Ablaufs)

Daniel hat die fuenf Fragen aus `docs/SPIELKONZEPT.md` Abschnitt 12 in EINER Runde beantwortet.
Jede Antwort mit ihrer Folge:

1. **Kontakt** = jede Interaktion (Handel, Ereignis, Kampf, Geschenk). Folge: der Rachetopf waechst
   nur bei echter Funkstille; wer den Bot beschenkt oder mit ihm handelt, haelt ihn ruhig.
2. **Rachetopf unter Pakt** steigt weiter, Angriff fruehestens 28.800 s nach Paktende. Folge: ein
   Pakt kauft Zeit, nicht Ruhe; die Ankuendigung darf waehrend des Pakts nicht feuern.
3. **Durchmarsch** bleibt reine Anzeige. Folge: keine Wegfindung, keine Kollisionsregeln.
4. **Paktwirkung einseitig:** der Bot greift nicht an, der Spieler darf pluendern - bezahlt aber mit
   schnellerer Vergeltung (Gunst sinkt, Rachetopf steigt bei Angriff auf einen Pakt-Bot). Folge fuer
   Schritt 3: der Angriffspfad braucht eine Pakt-Pruefung, die den Pakt BRICHT (Gunst-Abzug, Topf +1),
   nicht eine Sperre. Neue Wache: Angriff auf Pakt-Bot -> kein Verbot, aber Pakt gebrochen und Topf +1.
5. **Prioritaet:** Diplomatie zuerst fertig (Schritte 3 bis 7), Wirtschaft und Forschung danach.

Register 284.


## Nachtrag 14:00 - fuenf weitere Antworten (Vertraege, Bilder, Besucherdokumente, Push)

1. **Paktbruch beim ABSENDEN eines Angriffs, nicht bei Ankunft.** Daniel woertlich-nah: die Absicht
   zaehlt, und ein angegriffenes Ziel kann waehrend des Marsches nicht weglaufen. Gilt fuer Bots wie
   fuer den Spieler, soweit mechanisch machbar und in alle verknuepften Bereiche integriert.
   Folge: `_angriff_auftrag_starten` bricht den Pakt VOR dem Start; der Bot-Angriff bleibt gesperrt,
   solange der Pakt steht (dann gibt es nichts zu brechen).
2. **Ein laufendes Handelsabkommen bricht NICHT mit** - es endet still bei Ablauf.
3. **Die Referenzbilder kommen MIT in die EXE** (3,3 MB sind egal). Im Repo ist zu vermerken: der
   Ordner `assets/referenzbilder/` waechst mit der Designentwicklung deutlich, die Bilder werden
   teils ingame genutzt, teils dienen sie nur als Stilreferenz - darum tragen sie meist
   "ReferenzBild" im Namen.
4. **Besucherdokumente buendeln:** SPIEL_ERKLAERUNG, FRAKTIONEN_WELTEN und VORSCHAU wandern in
   BESUCHER.md, die alten Fassungen nach `docs/archiv/`.
5. **Push:** in dieser Sitzung erlaubt (erledigt, `ddea42d..dedd524`); fuer die NAECHSTE Sitzung im
   Voraus freigegeben, ohne Rueckfrage (Daniel 14:05). Ergebnis trotzdem pruefen, nicht durch eine
   Pipe messen.

Arbeit aus 1 bis 4 ist in der Uebergabe 14:05 als naechste Aufgabe vermerkt; erledigt ist bisher nur
die Vertragslogik im Modul (Commit `dedd524`).


## Offene Frage F-11 (06.11.2026, 17:41) - Motive der SPIELANSICHTEN

**Messlage:** Gebaut sind seit Register 287 zwei Startbilder (Panorama hinter der Anmeldung aus dem
Elfen-Waldlandreich, Ladebild mit Menschen und Ritter) - beide aus Daniels eigenen Referenzbildern.
Die Spielansichten selbst haben seit 03.11.2026 EIN Hintergrundbild (`_hintergrund_bauen`,
`data/hintergrund.json`), also ein und dasselbe Motiv fuer alle Ansichten.

**Frage:** Sollen die Spielansichten andere, waermere Motive aus `assets/referenzbilder/` bekommen
(je Ansicht oder je Fraktion eines), oder bleibt es beim jetzigen einen Hintergrund?

**Auswirkung:** Ein Wechsel ist reine Optik ohne Spielwirkung; er kostet die Auswahl und das
Einpassen je Bild (Zuschnitt, Abdunkelung fuer die Lesbarkeit) und macht die EXE groesser (die
Referenzbilder sind ohnehin schon im Paket, Register 285 Punkt 3). Bleibt es beim jetzigen Bild,
ist nichts zu tun.

**Empfehlung:** beim jetzigen einen Hintergrund bleiben, bis die Startbilder eine Runde im Betrieb
waren - dann entscheidet das Auge, welches Motiv wo stoert. Kein Umbau auf Vorrat.

**Antwort Daniels:** offen.
## Offene Frage F-12 (06.11.2026, 23:50) - Handelspunkte: WESSEN Gold zaehlt?

**Messlage** (selbst gemessen am 06.11.2026 zwischen 23:35 und 23:45 mit dem Projekt-venv; Messkripte
`messung_handelspunkte.py` und `messung_handelspunkte2.py` im Hermes-Scratch):

1. **Quelle 2006** (`docs/original/Spielanleitung_2005/punktesystem.php.txt`, Zeilen 34 bis 47):
   Handelspunkte gibt es fuer Gold, das man **durch Verkauf erwirtschaftet** (Beispiel der Quelle:
   100 Schwerter fuer 300 Gold = 3 Punkte). Fuer gekaufte Ware nennt die Quelle nichts.
2. **Der einzige Handelsweg macht den Spieler zum KAEUFER.** `GameState.handel_mit_bot` uebergibt
   `asdict(quelle)` als Kaeufer an `spieloekonomie.handel_start`. Gemessen: Kauf von 1 Holz zu 301 Gold
   ergibt am Ort **minus 301 Gold**, beim Bot **plus 301 Gold**, `vertrag erloes = 301.0`.
3. `erloes` ist damit die Einnahme des **Verkaeufers**, also des Bots. Die im Ablauf fuer Schritt 6
   vorgesehene Buchung `handels_erloes += erloes` gaebe dem Spieler Punkte fuer **ausgegebenes** Gold -
   das Gegenteil der Quelle.
4. **Die Gegenrichtung nimmt der Kern heute nicht an:** `bot_als_ort` setzt `einheiten: {}`, und
   `handel_start` verlangt die Karawane beim Kaeufer - gemessen: `ValueError: Karawane fehlt vor Ort`.
   Gibt man dem Bot seinen Wagenpark (Feld `lager`, ein bis zwei Karren je Bot) als `einheiten`, nimmt
   der Kern die Gegenrichtung an (gemessen) - es fehlen nur die Datenfuellung und eine Kauf-Entscheidung
   des Bots.
5. **Die Kennzahl kann sich auch mit richtiger Buchung nicht bewegen:** `tools/spieltest_simulation.py`
   faehrt `spielschicht.neuer_zustand`, und `src/spielschicht.py` (739 Zeilen) hat **weder Handel noch
   Bots** (kein Treffer fuer handel, kauf, karawane oder bots in der Datei).

**Frage:** Woraus sollen die Handelspunkte entstehen?

- **A (Empfehlung) - Verkaufsrichtung bauen, die Quelle ernst nehmen.** Der Spieler verkauft Ware an
  einen Bot, der Bot zahlt aus seinem Gold (er hat welches, gemessen), gefahren wird mit der eigenen
  Karawane. Gebucht wird dann `erloes` als echtes Einkommen. Drei Teile: **6a** Felder, Speichern/Laden
  und Anzeige (klein); **6b** Verkaufsrichtung im Kern (Richtungsparameter fuer die Karawane,
  `bot_als_ort` fuellt `einheiten` aus `bot.lager`, Kauf-Entscheidung des Bots mit DERSELBEN Preisfunktion
  `botkern.handelspreis` - keine zweite Preisrechnung); **6c** ein Handels-Schritt in der Spielschicht,
  damit das Kennzahlenblatt die Zahl wirklich zeigt.
- **B - Umsatz statt Erloes buchen.** Der Zaehler summiert das beim Kauf ausgegebene Gold. Eine Stunde
  Arbeit, widerspricht aber der Quelle: Punkte fuer Ausgaben. Muesste als bewusste Abweichung im Register
  stehen (VORSCHLAG), und der Haendler-Titel waere dann kein Handelserfolg mehr.
- **C - Schritt 6 zurueckstellen.** Nichts Falsches bauen, mit Schritt 7 (Bot-Luecken) weitermachen und
  die Handelspunkte nach der Verkaufsrichtung nachziehen.

**Auswirkung:** A kostet Schaetzung zwei Arbeitstakte (6b ist die meiste Arbeit, 6c ein halber), C kostet
nichts und verschiebt nur die Reihenfolge. B ist billig, aber falsch im Kern der Mechanik - der Spieler
bekaeme den Haendler-Titel fuer Einkaufen.

**Empfehlung:** A, in der Reihenfolge 6a, dann 6b, dann 6c.

**Antwort Daniels:** offen.
## Nachtrag 07.11.2026, 00:05 - Antwort auf F-12 (Handelspunkte)

| Frage | Antwort Daniels | Folge |
|---|---|---|
| F-12 | **A - Verkaufsrichtung bauen** (6a Felder/Anzeige, 6b Verkauf im Kern, 6c Handel in der Spielschicht). | Der Spieler verkauft eigene Ware an einen Bot; der Bot zahlt aus seinem Gold, die eigene Karawane faehrt (`karawane_seite="verkaeufer"` im Kern). Gebucht wird `erloes` (echtes Einkommen) genau einmal in `_fremdvertrag_buchen`. **Kein** Punkt fuer gekaufte Ware - das waere die Abweichung B gewesen und ist damit abgelehnt. 6a und 6b sind gebaut (Register 290), 6c (Handel in der Spielschicht, damit das Kennzahlenblatt die Zahl zeigt) steht noch offen, ebenso der Knopf in der Handelsmaske. |
