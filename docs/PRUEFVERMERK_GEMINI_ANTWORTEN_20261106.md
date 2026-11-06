# Pruefvermerk zu den fuenf Gemini-Antworten (06.11.2026)

**Zweck:** jede Antwort Zeile fuer Zeile gegen den Code gehalten, BEVOR daraus ein Paket wird.
Rangfolge bleibt: Gesamtbalancing > Daniels Entscheidung > Original als Richtwert > Vorschlag.
**Keine Zahl aus einer Gemini-Antwort wird uebernommen, ohne dass wir sie aus unseren Daten
nachrechnen** (Daniel, 06.11.2026: nichts einfach uebernehmen).

Grundlage: `docs/eingaenge/GEMINI_ANTWORTEN_20261106/` (5 Antworten + Arbeitsweise-Feedback,
hashgeprueft abgelegt), Auftraege in `docs/auftraege/20261106/`, Daniels Antworten in
`docs/ENTSCHEIDUNGEN_DANIEL_20261106_GEMINI_ANTWORTEN.md`.

## A1 - Postfach und Ruhmbalken

**Brauchbar:** Felder `read`, `archived`, `expiry_ts` im vorhandenen dict; Ablauf im Tick;
Militärberichte ohne Ablauf; Paginierung statt 500 Widgets; Balken mit `tk.Canvas`; Text bei
0 Nachrichten.

**Falsch oder gegen unsere Regeln:**
- **Fristen "hart im Code als Konstanten"** widerspricht dem datengesteuerten Aufbau: Fristen gehoeren
  nach `data/` (z. B. `data/nachrichten.json`), nicht als Konstanten in `GameState`.
- **Rangschwellen 2.500 / 10.000** sind erfunden - Daniel hat entschieden (Frage 1), dass wir sie aus
  unseren Punktzahlen ableiten (die vier Spieltests endeten bei 19 bis 40 Punkten nach 8 bis 12 Tagen).
- **Cache `state.aktuelle_punkte`** ist ein neues Spielstandfeld; es braucht `.get`-Fallback und darf
  beim Laden nicht fehlen. Der Hinweis selbst (Punkte nicht im Render rechnen) ist richtig.
- **Namensvorschlag `tests/test_messages.py`** passt zu unserer Konvention (`tests/test_*.py`); neue
  Pruefdatei ist erlaubt, sie baut auf `tests/harness.py` auf.

**Regel fuer den Einbau:** Fristen und Kategorien in `data/`, Anzeige liest dieselbe Lesestelle wie der
Tick, Punkte nur beim echten Tick rechnen, Balken mit `tk.Canvas`.

## A2 - Mauerreparatur

**Brauchbar:** Denkmodell (Kosten je Prozentpunkt, Zustand steigt stueckweise, Abbruch bei Angriff,
Sperre zwischen Reparatur und Ausbau, Anzeige mit allen fehlenden Bedingungen).

**Falsch oder gegen unsere Regeln:**
- **Kostenbasis:** es gibt KEINE Staffel je Stufe. `data/baupreise.json` fuehrt genau EINEN Wall-Preis
  (`verteidigungswall`: 16 Holz, 16 Stein). Geminis Formel `Baukosten(S)/100 × 0,5` hat damit nur einen
  Datenpunkt. Daniel hat entschieden (Frage 2): wir rechnen eine Preistabelle je Stufe aus 16/16 und
  legen sie vor.
- **Rechenfehler in der Zeit:** "1 Prozentpunkt = 120 Spielsekunden (6 Spielstunden)" ist falsch - 120
  Spielsekunden sind 2 Spielminuten; 6 Spielstunden waeren 21.600 Spielsekunden. Auch die
  Echtzeit-Angabe ("10 Spielstunden ≈ 66 Echtzeitsekunden") ist in sich widerspruechlich. Bei
  Spieluhrfaktor 180: 1 Spielstunde = 20 Sekunden Rechnerzeit.
- **Speicherort:** `Settlement` ist eine **dataclass mit Feldern** (Attribute wie `vorraete`,
  `bevoelkerung`, `stufen`), kein dict. Neue Werte also als Felder, nicht als `siedlung["repair_target"]`.
- **"Wall steht still"** hat Daniel anders entschieden: Reparatur kostet Holz, Stein UND Spielzeit, nur
  in der eigenen Siedlung (Frage 2 der ersten Runde). Ob der Wall waehrend der Reparatur schuetzt, ist
  bei uns zu klaeren - Geminis "teilaktiv" ist eine Auslegung, keine Vorgabe.

**Regel fuer den Einbau:** ein neues Feldpaar an `Settlement` (Reparaturziel, Fertig-Zeitpunkt), Buchung
der Rohstoffe atomar, Zustand steigt im Tick, `kampf.fuehre_schlacht` bleibt der EINZIGE Kampfweg und
bricht eine laufende Reparatur ab.

## A3 - Verwundetenheilung

**Brauchbar:** Verwundete je Siedlung; Entstehung VOR der Verlustbuchung; Rundung nach unten; Heilung
ueber die vorhandene Warteschlange; blockiert ohne Ausbildungsstaette; Anzeige mit allen Bedingungen.

**Falsch oder gegen unsere Regeln:**
- **`data/kaserne.json` existiert nicht.** Gemessen: `data/` fuehrt `baupreise.json`, aber keine
  Kaserne-Datei. Die Einheitenkosten stehen in `data/units.json` (`kosten`, `waren`), die
  Ausbildungsdauer kommt aus `spieloekonomie.ausbildung_grenzen` (`dauer_je`).
- **"Basis_Gold_Kosten"** gilt nur fuer Goldeinheiten. Gemessen: Kaempfer 175 Gold; Buergerwehr 100
  Nahrung + 50 Leder + 50 Wolle; Krieger 350 Gold + 1 Pferd. Daniel hat deshalb entschieden (Frage 6):
  **75 Prozent ALLER Kostenposten der Einheit, keine Ausruestung, halbe Ausbildungsdauer.**
- **`siedlung["ausbildungs_queue"]` gibt es nicht.** Die Warteschlange heisst im Kern `ausbildung` und
  ist eine Liste mit `einheit`, `gebaeude`, `start`, `ende`, `dauer_sekunden`, `stufe`, `gebucht`
  (`src/spieloekonomie.py:1136`). Heilungen dort einzureihen ist richtig, aber mit einem eigenen
  Kennzeichen, damit die Buchung sie nicht als Ausbildung behandelt.
- **Ausrüstung bleibt am Soldaten** - das ist eine Annahme. Bei uns wird Ausruestung bei der Ausbildung
  VERBRAUCHT; ob eine geheilte Einheit ihre Waffe behaelt, ist eine Daniels-Entscheidung, keine
  Selbstverstaendlichkeit. Vorschlag: ja, sie behaelt sie (sonst waere Heilung sinnlos).

**Regel fuer den Einbau:** Verwundete als Feld an `Settlement`, Entstehung in `kampf.fuehre_schlacht`
vor der Verlustbuchung, Heilung in der vorhandenen Warteschlange, Kosten aus `data/units.json`
gerechnet (nicht geschaetzt).

## A4 - Diplomatie, Rachetopf, Events

**Brauchbar:** Gunst und Status als Bot-Feld; Rachetopf im vorhandenen Bot-Gedaechtnis; Vertraege als
Liste im Spielstand; Statusgrenzen; Ankuendigung bei Rache 3; Bruchwarnung vor einem Angriff;
Anzeigezeile mit Gunst, Status und Restlaufzeit.

**Falsch oder gegen unsere Regeln:**
- **`state.bots[bot_name]["favor"]` passt nicht.** `BotPlayer` ist eine **dataclass** (Felder wie
  `name`, `faction`, `aggression`, `trading`, `ruf`, `gedaechtnis`). Fuer die Kern-Dict-Form gibt es
  `bot_als_dict`/`bot_aus_dict` - dort muessen neue Felder mitgefuehrt werden, sonst gehen sie beim
  Speichern verloren (bekannte Falle: `asdict()` laesst Eigenschaften weg).
- **Durchmarschrecht "Portalpassage durch sein Gebiet"** passt nicht: wir haben keine Bot-Gebiete,
  sondern sechs Dimensionen und Siedlungen darin. Was das Recht bei uns bewirken soll, muss neu
  definiert werden (offene Frage an Daniel, siehe Plan).
- **Rabatt 15 Prozent auf die Gegenleistung** beruehrt den gebauten Handelsweg
  (`spieloekonomie.handel_start`/`handel_entscheiden`); ein Rabatt darf nur dort entstehen, nicht in
  der Diplomatie-Anzeige (F-04-Muster).
- **`tk.Messagebox`** nutzen wir nicht - Dialoge sind eigene Overlays (`_overlay_oeffnen`), sonst
  blockiert die Modalitaet die Spieluhr.
- **"Angriffsstaerke mindestens 50"** ist eine fremde Skala; Daniel hat entschieden (Frage 9), dass wir
  die Schwelle aus `bot_angriffsplanung.schlagkraft` ableiten.
- **Gunst-Verfall zum Basiswert 20** und **Ereigniszahlen** (2.000 Gold, 5.000 Holz, 200 Werkzeuge,
  1.000 Eisen, 500 Gold) sind erfunden; Daniel hat entschieden (Frage 7): aus unseren Preisen ableiten
  und vorlegen.

**Regel fuer den Einbau:** Bot-Felder ueber `bot_als_dict`/`bot_aus_dict` fuehren, Vertraege im
Spielstand, NAP-Pruefung im vorhandenen Angriffsweg (kein zweiter), Rachetopf im Bot-Gedaechtnis,
Ereignisse ueber die vorhandene Overlay-Technik, alle Zahlen gerechnet und vorgelegt.

## A5 - Siedlungsumzug

**Brauchbar:** Zufallskarte aus `originalkarten.zufalls_originalkarte(seed, vergeben)`; alte Karte
zurueck in den Vorrat; Blockade solange Auftraege unterwegs sind; Rueckfrage vor dem Vollzug;
Vorschau der neuen Karte.

**Falsch oder gegen unsere Regeln:**
- **`siedlung.vorraete["siedler"]` gibt es nicht.** Siedler sind `Settlement.bevoelkerung` (float),
  nicht ein Rohstoff im Lager.
- **`welt.portalkosten` nimmt DIMENSIONEN, keine Koordinaten** (`portalkosten(von, nach)`, Formel aus
  `data/welten.json`: Grundbetrag + Kosten je Schritt × Entfernung). Ein Umzug innerhalb derselben Welt
  hat damit keine Portalkosten - die Kostenbasis muss neu bestimmt werden.
- **"Alle Gebaeude und Ausbaustufen gehen verloren"** ist durch Daniel ersetzt (Frage 8: **Gebaeude
  bleiben erhalten und ziehen mit**); dafuer muss der Umzug deutlich teurer werden. Der Preis ist zu
  rechnen und vorzulegen.
- **"5 Siedler"** war an Geminis Verlust-Variante gebunden und ist damit offen.
- **`GameState.umzug_siedlung_ausfuehren`** ist ein neuer Name in einer bestehenden Klasse - zulaessig,
  aber die Sperrpruefung MUSS die vorhandene Zaehlfunktion `_unterwegs_anzahl` benutzen.

**Regel fuer den Einbau:** Umzug als Methode in `GameState`, Sperren ueber die vorhandene
Zaehlfunktion, Kartenziehen ueber `originalkarten`, Siedler ueber `bevoelkerung`, Kosten aus unseren
Daten gerechnet.

## A6 - Geminis Arbeitsweise-Feedback (A bis D)

| Vorschlag | Urteil | Begruendung |
|---|---|---|
| A Stub-Datei `src/interfaces_stub.py` | **teilweise** | Der Nutzen stimmt, der Ort nicht: eine erzeugte Signatur-Sammlung gehoert nach `tools/` oder in den Scratch, nicht als `src/`-Modul. |
| B Logik aus `main.py` auslagern | **schon so** | Reine Rechnung liegt bereits in `punkte.py`, `spieloekonomie.py`, `kampf.py`, `wirtschaft.py`. Code nur zum Verkleinern zu verschieben, bringt keinen Fehlergewinn. |
| C Strict Typing, `int`/`floor`, keine negativen Bestaende | **uebernehmen** | Deckt sich mit unseren Regeln (atomare Buchung, `max(0, …)`, `hilfen.als_int`). Wird Prompt-Regel fuer Modellauftraege. |
| D Schema-Wache beim Laden | **anders loesen** | Unsere Regel ist: keine Migration, `.get` mit Standardwert. Eine **lesende** Pruefung, die fehlende Schluessel MELDET, ist erlaubt; eine, die sie still schreibt, waere eine zweite Wahrheit. |
| "via WSL" | **falsch** | Es gibt keinen WSL-Bezug; Entwicklung und Pruefung laufen nativ auf Windows. |

**Fazit:** die Antworten sind als Denkmodell brauchbar, als Code nicht. Vier Stellen haetten bei
unserem Aufbau sofort gebrochen (dict-Zugriff auf dataclasses, fehlende `data/kaserne.json`,
Siedler im Lager, Portalkosten aus Koordinaten). Genau deshalb gilt: Zahlen und Strukturen rechnen wir.
