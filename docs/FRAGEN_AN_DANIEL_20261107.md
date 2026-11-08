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

## Frage F-13 (07.11.2026, 12:10) - Preisfunktion des Handels gegen das Punktesystem

**Messlage:** Der Handels-Schwellenpreis ist `botkern.referenzpreis_aus_beschaffung(250) x 1,0` =
**300 Gold je Einheit** (Temperament 0,0). Die 250 sind der Handbuchpreis des Kaempfers
(`docs/original/ORIGINAL_Einheiten_Waren_Rohstoffe.md` Zeile 32: 1 Siedler, 250 Gold). Die Daten
fuehren den Kaempfer seit Daniels Entscheidung vom 05.11.2026 (Goldkosten der Militaereinheiten
30 Prozent runter, Register 225) mit **175 Gold**. Gemessen im echten Spiel am 07.11.2026: ein Bot
hat an Spieltag 1 zwischen 357 und 1.027 Gold, an Spieltag 10 zwischen 3.002 und 18.052.
`punkte.handelspunkte` gibt 1 Punkt je 100 Gold. Ein einziger Verkauf von 33 Einheiten Holz bringt
deshalb 9.900 Gold und **95 Handelspunkte** - der ganze uebrige Lauf kommt auf 42 Gesamtpunkte.

**Frage:** Soll der Schwellenpreis bei 300 Gold je Einheit bleiben, oder mit den gesenkten
Einheitenpreisen mitgehen?

- **A (Empfehlung, kleinster Schnitt) - bleibt 300, der Handel ist bewusst stark.** Kein Code, kein
  neuer Sammellauf; der Befund steht im Register. Folge: der Haendler-Titel ist mit einem Handel
  erreichbar, das Kennzahlenblatt zeigt grosse Handelspunkte neben kleinen Gesamtpunkten.
- **B - Schwellenpreis auf den Datenpreis umstellen (175 -> 210 Gold).** Eine Zeile in
  `botkern.BESCHAFFUNGSKOSTEN`, danach Sammellauf. Folge: 33 Einheiten bringen 6.930 Gold und
  69 Punkte; der Handel bleibt dominant, aber weniger.
- **C - Preise je Rohstoff trennen (eigener Schnitt, mehrere Stunden).** Der Handel bekommt eine
  Preistafel je Rohstoff statt eines Einheitspreises. Folge: echte Knappheitspreise, aber eine neue
  Datendatei, eine neue Wache und ein eigener Sammellauf; ohne Quelle sind alle Zahlen VORSCHLAG.

**Auswirkung:** A kostet nichts und aendert kein Verhalten. B aendert den Preis IM SPIEL (auch fuer
den Bot-Kauf), braucht einen Sammellauf und ist eine Balancing-Entscheidung. C ist der saubere Weg,
aber ein eigener Schnitt.


## F-14 - Drache: zusaetzlich ein Meidungs-Urteil der Bots bauen?

**Messlage:** der Ablauf (Schritt 7) nennt `drachen.bedrohung(ort)` als neue Funktion. Am Code
nachgemessen: das Urteil der Bots gibt es seit W-14 (05.11.2026) als `drachen.bot_entscheidung` mit
eigener Wache (`tests/test_drachen_einhaengung.py`), aufgerufen in `main._bots_drachenzug`. Ein Bot
greift nur an, wenn seine Schlagkraft die Drachenschwelle mal Sicherheitsfaktor 1,6 erreicht; sonst
meldet er "Drache zu stark". Eine zweite Funktion fuer dieselbe Frage waere die zweite Wahrheit
(F-04) und ohne Aufrufer toter Code.

**Frage:** soll zusaetzlich eine Meidung gebaut werden - Bots weichen Drachenfeldern aus, gruenden
nicht daneben, marschieren nicht durch?

- **A (Empfehlung) - nichts bauen.** Das Urteil ist da und geprueft; die Meidung waere eine neue
  Mechanik ohne Quelle (weder Handbuch 2009 noch 2006 sagen etwas dazu). Kosten: null.
- **B - Meidung als reine Anzeige.** `drachen.bedrohung(ort)` liefert nur einen Text ("ein Drache
  steht zwei Felder entfernt"), den die Bot-Meldung zeigt. Kosten: eine Stunde, keine Mechanik.
- **C - echte Meidung (eigener Schnitt).** Weltfelder mit Drachen werden bei Gruendung und Marsch
  gemieden. Kosten: mehrere Stunden, beruehrt Karten-, Gruendungs- und Marschpfad, ohne Originalbeleg.

**Auswirkung:** A aendert nichts. B macht die Karte lesbarer. C aendert das Spielgefuehl deutlich und
braucht einen eigenen Sammellauf.

## F-15 - Reaktionsstufen der Bots: 0,8 / 1,0 / 1,2 richtig?

**Messlage:** der Ablauf nennt "Reaktionsfaktoren 0,8 bis 1,2" und "Meidungsstufen 3" - beides ohne
Originalbeleg. Umgesetzt: Bereitschaft aus der Taktik (Pluenderer 1,2, Waechterin 0,8, Bastionier
0,8, Spaeherin 1,0, unbekannt 1,0); sie teilt `armee_schwelle` (6) und `staerke_faktor` (1,5) aus
`data/bot_raubzug.json`. Gemessen: gierig 6 -> 5 und 1,5 -> 1,25; vorsichtig 6 -> 8 und 1,5 -> 1,875.
Zusaetzlich macht ein Spieler-Vorsprung von 50 Prozent jeden Bot vorsichtiger (x 0,9).

**Frage:** bleiben diese Zahlen und die Zuordnung Taktik -> Stufe so?

- **A (Empfehlung) - bleibt.** Alle Werte sind VORSCHLAG und stehen in `data/bot_diplomatie.json`;
  Daniel kann sie dort ohne Codeaenderung stellen.
- **B - Spanne kleiner (0,9 bis 1,1).** Wirkung: die Bots verhalten sich aehnlicher, der Unterschied
  zwischen gierig und vorsichtig verschwindet fast.
- **C - Zuordnung nach Fraktion statt nach Taktik.** Wirkung: Voelker statt Charaktere; braucht eine
  zweite Tabelle und ist ohne Quelle ebenso willkuerlich.

**Auswirkung:** A kostet nichts. B und C sind Balancing-Entscheidungen mit eigenem Sammellauf.


## Nachtrag 07.11.2026, 17:40 - die drei Fragen sind beantwortet (Daniel, im Chat)

| Nr | Frage | Antwort | Folge |
|---|---|---|---|
| F-13 | Schwellenpreis 300 Gold je Einheit? | **A - bleibt bei 300 Gold.** | Kein Code, kein neuer Sammellauf. Der Handel bleibt bewusst stark; der Befund (95 Handelspunkte aus einem Verkauf) steht weiter im Register 292 und in `docs/balancing/kennzahlen.jsonl`. |
| F-14 | Drache: zusaetzlich eine Meidung bauen? | **B - nur Anzeige.** `drachen.bedrohung(ort)` liefert einen Text. | Gebaut in dieser Sitzung (Register 294): `drachen.bedrohung` nennt Name und Manhattan-Abstand des naechsten offenen Drachen, Reichweite 5 Felder; die Bot-Meldung im Zweig "zu stark" haengt den Satz an. **Keine** Meidung, weder Gruendung noch Marsch weichen Drachenfeldern aus, und nichts wird gebucht. |
| F-15 | Reaktionsstufen 0,8 / 1,0 / 1,2 und Zuordnung nach Taktik? | **A - bleibt so.** | Kein Code. Die Werte stehen in `data/bot_diplomatie.json` (Block `reaktion`) und sind dort ohne Codeaenderung zu stellen. |

**Was aus den Antworten NICHT folgt:** kein neuer Schnitt ausser der Anzeige (F-14 = B). F-13 und F-15
sind reine Bestaetigungen des dokumentierten Stands - sie aendern keine Datei.


## F-16 - Sollkurve: Obergrenze oder gedrosselter Erfahrungswert?

**Messlage:** `data/sollkurve.json` zeigt am Spieltag 5 Holz 2.449, Stein 2.537, Nahrung 2.880, Gold
1.836. Das ist eine OBERGRENZE: der Idealplan baut jedes Gebäude, sobald er es bezahlen kann (kein
Bauzwang, keine Wegzeiten, keine Kämpfe). Eine echte Partie liegt weit darunter - das Kennzahlenblatt
nennt für Spieltag 6 rund 841 Gold und 35 Holz. Der Korridor 0,7 bis 1,1 um diese Obergrenze wird
deshalb von echten Läufen NIE erreicht; für den Regelkreis (B-2) taugt er nur als VERGLEICH zwischen
zwei Versionen, nicht als Erwartungswert.

**Frage:** Soll die Sollkurve gedrosselt werden?

- **A (Empfehlung, kleinster Schnitt) - bleibt Obergrenze, aber so benannt.** Kein Code. In B-2 wird
  nur die VERAENDERUNG zwischen zwei Versionen verglichen (A/B mit demselben Idealplan). Die
  Kennzahlen aus echten Läufen bleiben die zweite, ehrlichere Messung.
- **B - Bauzwang einbauen (ein Gebäude je Spieltag).** Wirkung: die Kurve kommt in die Nähe echter
  Partien; die Zahl "ein Gebäude je Spieltag" ist aber ohne Quelle (VORSCHLAG) und müsste in
  `data/sollkurve.json` als Annahme stehen.
- **C - Kurve aus echten Läufen kalibrieren (Kennzahlenblatt).** Wirkung: Korridor = gemessene Partien
  x 0,7/1,1; braucht 10 Läufe je Neurechnung (rund 4 Minuten) und macht die Kurve von der Messschicht
  abhängig, nicht von den Daten.

**Auswirkung:** A kostet nichts. B ändert nur das Werkzeug. C koppelt Balancing an die Messschicht
und ist ein eigener Schnitt.

**Nebenbefund (kein Beschluss noetig):** V-4 rechnet Gold mit 0,5 je Bergfeld und Stunde, die
Datendatei `data/resources.json` nennt 3. Beide Zahlen stehen im Projekt; welche fuer den Korridor
gilt, entscheidet die Datendatei (dort steht die Quelle) - der Unterschied ist notiert, nicht
geglaettet.


## Nachtrag 07.11.2026, 19:00 - Antworten der zweiten Runde (Daniel, im Chat)

| Nr | Frage | Antwort | Folge |
|---|---|---|---|
| F-16 | Sollkurve: Obergrenze oder gedrosselt? | **A - Obergrenze bleibt, so benannt.** | Kein Code. B-2 vergleicht nur die VERAENDERUNG zwischen zwei Versionen (gleicher Idealplan, A/B); die Kennzahlen aus echten Laeufen bleiben die zweite, ehrlichere Messung. `data/sollkurve.json` traegt den Satz schon im Feld `zweck`. |
| F-17 | Ab welcher Verbesserung gilt eine Balance-Aenderung als angenommen? | **A - 20 Prozent Verbesserung, hoechstens 10 Prozent Schrittweite, 3 gleiche Meldungen.** | Wird in Schritt 9 (B-2) so gebaut: die drei Zahlen stehen in einer Datendatei (`data/regelkreis.json`, VORSCHLAG) und nicht im Code. |
| F-19 | Womit laeuft der neue KI-Auftrag (Schritt L, Runde 3)? | **Paket fuer Claude Sonnet 5.5, deutlich umfangreicher als Runde 2 - "richtig viel erarbeiten".** Der Lauf kostet nichts (frisch angemeldet, Testlauf frei). | Der Auftrag wird als eigene Datei mit Datum gebaut (die geschuetzte `Nebelseetal_LLM_Auftrag_20261106.md` bleibt unberuehrt), mit Dossier, Ablauf, Stand des Codes, Prueffragen und Ablagehinweisen; hoechstens 8 MB je ZIP, Dateien direkt angehaengt. **Erste Aufgabe der Sitzung 14** (Abhaengigkeit ist Schritt 3, der steht). |

**Was aus diesen Antworten folgt:** F-16 und F-17 sind Vorgaben fuer Schritt 9; F-19 ist eine eigene
Aufgabe (Schritt L), die VOR den Schritten 9 bis 13 laufen kann, weil sie nur vom Ablauf selbst abhaengt.

## Nachtrag 07.11.2026, 20:45 - Antwort F-20 (Daniel, im Chat)

| Nr | Frage | Antwort | Folge |
|---|---|---|---|
| F-20 | Der erste A/B-Lauf zeigt: eine Preisänderung von 10 Prozent bewegt die Kennzahl nicht (Zielabweichung bleibt 6,06 Prozent). Der Abstand zur Sollkurve kommt aus der SPIELERPOLITIK - der Automat gibt Gold und Holz für Armee und Forschung aus, der Idealplan der Kurve gibt nichts aus. Was soll der Regelkreis daraus machen? | **B - Vorschlagsquelle erweitern: auch Schwellen der Spielerpolitik dürfen vorgeschlagen werden (erst prüfen, was davon in `data/` steht).** | Eigener kommender Schnitt, NICHT nebenbei gebaut. Erste Messung dazu (in dieser Sitzung gelesen): die Politik steht heute im CODE von `tools/spieltest_simulation.py` (`GEBAEUDE_REIHENFOLGE`, `STILE`, `FORSCHUNGSZIELE`, Schrittweite `SCHRITT = 1200`) - in `data/` liegt NICHTS davon. Der Schnitt braucht deshalb zwei Teile: (1) die Politik-Schwellen als Datendatei (Vorschlag `data/spieltest_politik.json`) mit Quelle je Wert, (2) `_preis_kandidaten` zu `_kandidaten` erweitern, damit der Vorschlag auch einen Politik-Wert nennen darf - weiterhin höchstens EIN Wert je Runde und Schrittweite ≤ 10 Prozent. Die Sollkurve bleibt Obergrenze (F-16 = A), das Urteil vergleicht weiter nur die Veränderung. |

**Was aus dieser Antwort folgt:** B-2 bleibt als Werkzeug unverändert richtig (die Ablehnung war ein
echtes Ergebnis). Die Erweiterung ist ein eigener Schnitt nach den Schritten 10 bis 13 und wird erst
gebaut, wenn die Politik in `data/` steht - sonst hätte der Vorschlag wieder eine zweite Wahrheit
im Code (F-04-Muster).

## Frage F-21 (07.11.2026, 20:48) - Reihenfolge nach der dritten Modellrunde

**Messlage:** Die Antwort von Claude Sonnet 5.5 ist als Lieferung unvollständig (keine Dateien, E/F/H
unter Mindestumfang), als Befundsammlung brauchbar. Selbst nachgemessen und **bestätigt** sind sieben
Punkte: I-1 (Ereignisart nach Bot-Index), A-1 (zwei Spieltag-Längen: 28.800 s gegen 86.400 s), I-3
(Haug und Silra ohne Gegenleistung), C-4 (zwei widersprüchliche Einheitenangaben je Drache), I-10
(`ausgang_text` nur im Test), C-6 („VORSCHLAG:“ in einer Spielermeldung), G-1 (Register 272/273
fehlen). Der Rest ist ungemessen und gilt nach Projektregel noch nicht als bestätigt.
Belege: `docs/audits/PRUEFVERMERK_CLAUDE_RUNDE3_20261107.md`.

**Was zur Entscheidung steht:** ob die drei kleinen Fehlerpakete VOR Schritt 10 des Ablaufs laufen
(zusammen 90 bis 150 min) oder erst danach.

| | Weg | Folge |
|---|---|---|
| A | **R3-1 (A-1 Spieltag, 60 min) und R3-2 (I-1 Ereignis-Zuordnung, 30 min) vor Schritt 10**, danach R3-3 und R3-4 | zwei sichtbare bzw. zahlenverfälschende Fehler raus, bevor weitere Messungen entstehen; Schritt 10 verschiebt sich um rund 1,5 h |
| B | erst den Ablauf zu Ende (Schritte 10 bis 13), danach alle R3-Pakete in einem Zug | der Ablauf bleibt wie geplant; A-1 verfälscht bis dahin jede Zeitmessung |
| C | nur I-1 (30 min) sofort, alles andere nach dem Ablauf | kleinster Eingriff; A-1 bleibt offen |

**Empfehlung: A.** A-1 verändert Zahlen, die in jede spätere Messung eingehen (auch in den neuen
Regelkreis), und I-1 ist der sichtbarste Fehler im Spiel. R3-3 und R3-4 kosten zusammen 150 min und
laufen nach dem Ablauf.

**Antwort Daniel 07.11.2026, 20:50: A.** R3-1 (A-1 Spieltag-Definition) und R3-2 (I-1
Ereignis-Zuordnung) laufen VOR Schritt 10, danach der Ablauf (10 bis 13), danach R3-3 (C-6, I-10, C-4)
und R3-4 (I-2). Jeder dieser Schnitte bekommt seine eigene Wache, einen Registereintrag, eine
Protokollzeile und einen vollen Sammellauf.

## Nachtrag 22:12 - zwei Antworten Daniels (F-22, F-23)

**F-22 Skill-Ergaenzung: FREIGEGEBEN (Daniel 22:07).** Teil 8 (acht Lehren aus Sitzung 14, B-2
Regelkreis) und Teil 9 (sieben Lehren aus Sitzung 15, R3-1/R3-2) sind in den Skill
`nebelseetal-remake` aufgenommen - Teil 8 **wortgleich** aus der freigegebenen Vormerkung
`ce4981df`, Teil 9 neu geschrieben. Folge: die Vormerkung ist damit erledigt und aus der Warteschlange
in `pending/skills/skills_archiv_20261107_2212/` gelegt (nichts geloescht). Der Skill steht jetzt bei
**98.356 Zeichen** - die naechste Ergaenzung muss zuerst einen Block nach `references/` auslagern
(Grenze 100.000).

**F-23 Diplomatiefristen in Echtzeit: SO LASSEN (Daniel 22:07).** Frist zwei Spieltage, Haeufigkeit
drei Spieltage, Pakt drei Spieltage und der eine Spieltag Vorlauf bleiben, wie sie sind; ein Spieltag
ist ein Spieltag. Folge: bei Spieluhrfaktor 180 wirken diese Fristen dreimal so lange wie vor dem
R3-1-Schnitt (Ereignisfrist 16 statt 5,3 Echtminuten, Pakt und Haeufigkeit 24 statt 8) - das ist
gewollt und **kein Fehler**. Wer die Echtzeit spaeter kuerzen will, aendert die Zahl in SPIELTAGEN
(1 statt 2, 1 statt 3), nie in Sekunden - sonst entsteht wieder eine zweite Tageslaenge.

## Nachtrag 22:40 - Dauerregel fuer die Uebergabe (Daniel, mündlich im Chat)

**Daniels Wortlaut (07.11.2026, 22:38):** "ich mag es nicht wenn einfach dauerhaft eine uebergabe auf
dem desktop liegt. Ich mag es lieber wenn es da erst erscheint wenn es wirklich fertig und auf
neuestem stand ist."

**Regel ab jetzt (gilt fuer jede Sitzung, keine Rueckfrage mehr noetig):**

1. **Das Archiv ist der Arbeitsort.** Die Uebergabe wird in `D:\Arbeiten\Hermes\Uebergaben\<JJJJMMTT_HHMM>\`
   geschrieben, gelesen, gegengeprueft und nachgebessert. Fuer jede Zwischenfassung gilt: nur dort.
2. **Der Desktop bekommt GENAU EINE Handlung:** die fertige, geprueft Fassung wird als **letzter
   Schritt** aufgelegt - nach `sha256sum` beider Kopien und einer Gegenlesung auf Kopf-Commit,
   Commit-Zahl und Zahlen.
3. **Wird die Fassung danach noch geaendert, verschwindet die Desktop-Kopie SOFORT** (Hash vorher
   gegen das Archiv pruefen), die Aenderung passiert im Archiv, und erst die fertige Fassung wird
   wieder aufgelegt. Keine halbfertige Datei auf dem Desktop, auch nicht fuer Minuten.
4. **Die Vorgaengerfassung** wird beim Auflegen in derselben Aktion vom Desktop entfernt (Archiv
   bleibt unveraendert).
5. **Der frueher hier notierte Ablauf "schreibende Sitzung laesst die Desktop-Kopie stehen" ist damit
   ueberholt** - er hat am 07.11.2026 zu einer Datei gefuehrt, die nach dem Auflegen noch zweimal
   geaendert wurde (14.698 -> 15.984 Byte) und im Chat als alte Fassung erschien.

**Fundstelle der Regel im Skill:** `nebelseetal-remake` → `references/uebergabe-ablage.md`
(Vormerkung, Freigabe offen).

# Nachtrag 08.11.2026, 16:10 - Schritt 13: Zahlen ohne Quelle (VORSCHLAG, keine Aenderung vorgenommen)

`tests/test_daten_und_quellen.py` (Register 310) hat den Bestand gemessen. Nichts davon ist
umgerechnet oder geglaettet - die Zahlen stehen, wie sie stehen, und warten auf Daniels Wort.

**Frage 15 - neun Balance-Werte im Code ohne belegte Quelle.** Sollen sie so bleiben (dann bekommen
sie einen Satz "VORSCHLAG bleibt" in die Zeile) oder sollen sie in `data/` wandern?
`auftraege.py`: HIN_UND_RUECK_FAKTOR 2.0, DROSSELUNG_SCHRITTE_PROZENT 10, BEUTE_ANTEIL_PROZENT 50;
`botkern.py`: BESCHAFFUNGSKOSTEN 250.0 (Herleitung im Kommentar: Kaempferpreis x 1,2);
`dorfwall.py`: SEKUNDEN_JE_PROZENT 360.0; `spieldaten.py`: FORSCHUNG_GRUNDKOSTEN_HOLZ 50;
`spieloekonomie.py`: MENGEN_HOECHSTMENGE 200 (Schutz gegen Tippfehler);
`spielzeit.py`: STANDARD_FAKTOR 180.0 (dein Tempo); `werkstatt.py`: STUFE_TEMPO_PROZENT 10.

**Frage 16 - sechs Datendateien ohne Quellenangabe.** `bot_bedarf.json`, `bot_diebstahl.json`,
`bot_forschung.json`, `bot_stimmen.json`, `spionage.json` (VORSCHLAG) und `marsch_optik.json`
(Anzeige, kein Spielwert). Sollen die fuenf VORSCHLAG-Dateien eine Herkunftszeile bekommen, sobald
du sagst, woraus sie stammen?

**Sofort erledigt, ohne Frage:** jede Datendatei mit Schalter `aktiv` wird im Quelltext gelesen -
17 von 17, keine Attrappe. Und eine NEUE Zahl ohne Quelle oder Bestandseintrag macht die Wache rot.

# Nachtrag 08.11.2026, 16:35 - aus Spieltest 3

**Frage 17 - Bibliothek versetzen.** Du schreibst: "ich kann die falsch positionierte Bibliothek
nicht wo anders neu bauen und vom falschen Feld abreißen". Nachgemessen: der Abriss der LETZTEN
Bibliothek ist gesperrt (deine Regel vom 30.10.2026: "Die Bibliothek ist essenziell - die LETZTE darf
nicht abgerissen werden"), und eine zweite Bibliothek je Siedlung verbietet die Datenregel
`max_je_siedlung: 1`. Bis eine zweite SIEDLUNG steht, ist die erste Bibliothek damit unversetzbar.
Drei Wege: (a) Abriss der letzten Bibliothek mit Rueckfrage erlauben (Forschung steht dann still),
(b) ein Knopf "Bibliothek versetzen" (abreissen und im selben Zug neu setzen), (c) so lassen.

**Frage 18 - Pakt annehmen oder ablehnen.** Dein Wunsch aus Test 3: "ein bot soll einen pakt auch
annehmen oder ablehnen koennen aufgrund seiner Einstellung zu mir". Heute bucht der Knopf den Pakt
immer. Soll der Bot nach seiner Gunst und Taktik entscheiden (dann braucht es eine Regel: Schwelle,
Wahrscheinlichkeit, Begruendung im Postfach)?

**Sofort notiert, ohne Frage:** der Wall wandert in die Siedlungskarte unter "Verteidigung" (deine
Anweisung), die Marktplatz-Ansicht wird klar als Handelsplatz erkennbar (Karawane, Zustand, Hinweis),
und die Portal-Auswahl soll per Klick auf ein freies Weltfeld gehen statt per Auswahlliste.
