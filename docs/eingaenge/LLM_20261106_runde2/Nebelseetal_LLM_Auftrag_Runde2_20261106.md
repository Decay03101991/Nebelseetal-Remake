# NEBELSEETAL REMAKE - Wissens- und Auftragsdokument, RUNDE 2

**Stand:** 06.11.2026, Pre-Release `V_0.0.3`, Kopf-Commit der Runde 1: `20fa959`.
**Runde:** 2 (zweite Befragung externer Modelle; Runde 1 liegt als
`docs/extern/Nebelseetal_LLM_Auftrag_20261106.md` im Projekt).
**Was neu ist:** In Runde 1 haben vier Modelle (Claude Opus 5.5, UseAI Instant, Grok 4.5, Gemini)
Antworten geliefert. Diese Antworten wurden Punkt fuer Punkt gegen den Code geprueft, und daraus ist
**ein fester Ablauf** entstanden. Dieses Dokument enthaelt den geprueften Ablauf. Deine Aufgabe ist
NICHT, ihn neu zu erfinden, sondern ihn zu zerlegen.

## 1. Das Spiel in eigenen Worten

Nebelseetal Remake ist eine lokale Neuauflage eines Browser-Aufbauspiels: Python 3.14, tkinter,
JSON-Spielstand, offline, portabel. Ein Spieler tritt gegen fuenf Bots mit eigener Wirtschaft an,
dazu ein Drache und Ruinen auf sechs Welten. Es gibt keinen Sieg, sondern Punkte (Krieg, Forschung,
Gesamt) und vier Auszeichnungen.

Die Spieluhr laeuft mit Faktor x180: eine Spielstunde sind 20 echte Sekunden, ein Spieltag 28.800
Spielsekunden = 8 echte Minuten. Alles Fachliche rechnet in Spielsekunden, nie in Rechnerzeit.

Kernkreis: gruenden, produzieren (Gelaende mal Gebaeude, ortsgebundene Lager), forschen (Bibliothek,
Baukunst, dann Goldmine/Farm/Kriegerakademie), ausruesten (Waren aus Werkstatt und Rezepten),
ausbilden (Warteschlange je Ort, kostet Siedler), bewegen (Auftraege, Rueckweg doppelt), kaempfen
(Vorrunde, Wall, Phasen, Beute, Flucht), punkten.

Gerechnet wird in Fachmodulen unter `src/`, die Zahlen kommen aus `data/*.json`. `main.py` (rund
15.400 Zeilen, zwei grosse Klassen `GameState` und `NebelseetalApp`) liest und zeichnet. Anzeige und
Kern rufen dieselbe Funktion auf - das ist die Regel F-04, und ihre Verletzung ist der haeufigste
Fehler der Vergangenheit.

**Umfang heute:** 63 Quelldateien, 163 Pruefdateien, 8.200+ Pruefungen, davon 0 rot. Ein voller
Prueflauf dauert 21 bis 23 Minuten.

## 2. Was Runde 1 ergeben hat - und was die Pruefung davon uebrig liess

Von den vier Antworten sind nach der Pruefung am Code **acht Befunde** uebrig geblieben. Sie sind
gemessen, nicht behauptet, und gelten als Vorgabe:

| Nr | Befund | Beleg |
|---|---|---|
| G-1 | Die Angriffssperre ist `punkte.angreifbar`, verdrahtet an zwei Stellen: `main.py:7051` (Bot greift den Spieler an) und `main.py:6624` (Diebstahl Bot gegen Bot). Dazu kommt `noob_protection` (`main.py:6966`), das JEDEN Bot-Angriff bis zum ersten Kriegspunkt sperrt, und die Demo-Regel (`main.py:6960`). `src/versorgungsschutz.py` ist KEIN Angriffsgate, sondern eine Vorabpruefung auf Rohstoff-Sackgassen - zwei Antworten hatten das behauptet. | Code |
| G-2 | Die Rache-Schwelle ist **99 SK** (Wallstufe 3 = 90 SK plus 10 Prozent Reserve), nicht 90. | `docs/S0_TABELLEN_20261107.md` V-5 |
| G-3 | Die Ereigniszahlen V-4 sind nachrechenbar: Nahrung `(grasland+steppe) * 2 * 24 = 1.723`, Gold `berg * 0,5 * 24 = 128`; beide Formeln sind im Werkzeug als VORSCHLAG gekennzeichnet. | `tools/s0_tabellen.py:110-111` |
| G-4 | Werkzeuge und Eisen gibt es im Spiel nicht: 17 Waren (Waffen und Ruestungen), 9 Rohstoffe (holz, stein, metall, mana, nahrung, gold, wolle, leder, pferde). Das Grom-Ereignis aus V-4 ist so nicht baubar. | `data/items.json`, `data/resources.json` |
| G-5 | A-6 ist heute NICHT erfuellt: der Sammellauf braucht 1.612 s und hat 7.502 Pruefungen, die Bedingung nennt unter 1.400 s und 7.495. | `docs/audits/sammellauf_20261106_0755.log` |
| G-6 | `BotPlayer` hatte kein Feld fuer Gunst und keines fuer den Rachetopf; der Leseweg ist `bot_als_dict`/`bot_aus_dict`. | `src/main.py` |
| G-7 | Fuer die Bot-Luecken sind alle Bauteile da (`spionage.py`, `drachen.py`, `bottaktik.py`, `data/bot_raubzug.json`, `data/bot_stimmen.json`); es fehlen Daten und Aufrufer, keine Module. | `src/`, `data/` |
| G-8 | Die Handelspunkte koennen strukturell nie steigen: `punkte.handelspunkte` rechnet aus `gold_erloes`, aber `gold_erloes` wird NIRGENDS geschrieben, und die Anzeige uebergibt es nicht. Der Handelsweg selbst ist vollstaendig gebaut. Die Behauptung dreier Antworten, der Handelsweg sei eine Sackgasse, ist widerlegt. | `src/punkte.py:400-414`, `src/main.py:8813` |

**Lehre aus Runde 1:** Uebereinstimmung mehrerer Modelle ist kein Beleg. Zwei Antworten irrten
gleich (G-1), drei gleich (G-8). Was zaehlt, ist die Quelle: Handbuch 2009 mit Seite, 2006er Seiten,
Datendatei, gerechnete Tabelle - oder das Wort VORSCHLAG.

## 3. Der feste Ablauf (das Ergebnis der Runde 1, bereits beschlossen)

Der Ablauf steht unten woertlich, damit du ohne Projektzugriff arbeiten kannst. Er ist in dieser Runde
in Arbeit: **Schritt 1 (Gunst und Status) ist gebaut und gruen** (Wache 33/0/0), die Schritte 2 bis 13
sind geplant. Jeder Schritt nennt: Ziel, Dateien, Aenderung, Daten mit Herkunft, Wache mit Faellen,
Fertig-Kriterium, Aufbauzeit-Effekt, Abloesung, Risiko.

## 3. Der Ablauf in Reihenfolge

Ein Schritt = ein Commit = ein voller Sammellauf (21 bis 23 Minuten). Aufwand ist Erfahrungswert
dieses Projekts, keine Messung; die Wachenzahl ist die Untergrenze der neuen Pruefungen.

| Nr | Schritt | haengt an | Aufwand | Wachen | Aufbauzeit-Effekt |
|---|---|---|---|---|---|
| 1 | S4-1 Gunst und Status | - | 60 min | 6 | keiner |
| 2 | S4-2 Kennzahlenblatt (Messung) | 1 | 60 min | 4 | keiner |
| 3 | S4-3 Vertraege: NAP, Handelsabkommen, Durchmarsch-Anzeige | 1, 2 | 75 min | 7 | senkt sie |
| 4 | S4-4 Rachetopf und Angekuendigter Angriff | 3 | 60 min | 7 | erhoeht den Druck, nicht die Dauer |
| 5 | S4-5 Ereignisse Haug, Grom, Silra | 1, 3 | 75 min | 6 | neutral (Ablehnen moeglich) |
| 6 | S4-6 Handelspunkte: Erloes buchen und anzeigen (G-8) | 2 | 45 min | 4 | keiner, oeffnet einen Weg |
| 7 | S4-7 Bot-Luecken: Drache, Spionage, Reaktion | 5 | 90 min | 8 | kann sie heben (Faktoren gedeckelt) |
| 8 | B-1 Sollkurve aus den Daten | 2 | 60 min | 4 | keiner |
| 9 | B-2 Regelkreis, A/B-Urteil, Feedback-Eingang | 8 | 90 min | 5 | keiner |
| 10 | A-1 E2E-Ketten auf 12 Wege erweitern | 3 bis 10 | 120 min | 12 | keiner |
| 11 | A-2 AST-Quellwache fuer die Ansichten | 10 | 60 min | 3 | keiner |
| 12 | A-6 Sammellauf messen und beschleunigen | 11 | 60 min | 2 | keiner |
| 13 | A-7/A-5 Schlusspruefung: Daten, Schalter, Quellen | 12 | 45 min | 3 | keiner |
| L | Neuer KI-Auftrag aus diesem Ablauf (Meldepflicht) | 3 | 30 min | 0 | keiner (Dokument) |

Summe: rund **13 Stunden Arbeit** plus 13 Sammellaeufe - also mehrere Sitzungen. Die Reihenfolge ist so
gewaehlt, dass **nach jedem Schritt ein spielbarer, gruener Stand** existiert; es gibt keinen Schritt,
der nur mit einem spaeteren zusammen funktioniert.

## 4. Die Schritte im Einzelnen

### 1 - S4-1 Gunst und Status

| Feld | Inhalt |
|---|---|
| Ziel | Jeder Bot hat eine Gunst 0..100; der Status (feindselig, wachsam, freundlich) wird daraus **gerechnet**, nie gespeichert. Eine Anzeigezeile in der Diplomatie-Ansicht liest dieselbe Funktion. |
| Dateien | neu: `src/diplomatie.py` (Gunst, spaeter Rache, Vertraege, Ereignisse - EIN Thema, ein Modul), `data/diplomatie.json` (jede Zahl mit `quelle`), `tests/test_diplomatie.py`; geaendert: `src/main.py` (`BotPlayer`-Feld ueber `bot_als_dict` :6482 / `bot_aus_dict` :6507, `_render_diplomacy` :13251) |
| Aenderung | `BotPlayer.gunst: int = 50` (additiv). `diplomatie.gunst_setzen(bot_daten, wert) -> int` klemmt auf 0..100, `gunst_aendern(daten, delta, grund) -> int`; `diplomatie.status(gunst) -> str` liest die Grenzen aus `data/diplomatie.json`. Anzeige: `Diplomatie: <name> - Gunst <n> (<status>)`. Kein zweiter Speicher fuer den Status. |
| Daten | Grenzen 39/40 und 59/60: Auftragsdokument Abschnitt 7.1 (Originalbeleg im Handbuch 2009 noch nachzuziehen, offener Punkt A-5). Startwert 50: VORSCHLAG. Aenderungen (Geschenk, Angriff, Vertragsbruch) erst in Schritt 3 und 4. Schalter `aktiv`. |
| Wache | `tests/test_diplomatie.py`: (1) `gunst_setzen` bei -5 / 0 / 50 / 100 / 130; (2) `status(0/39/40/59/60/100)`; (3) alter Spielstand ohne Feld laedt mit 50, und die Datei wird dabei **nicht** geschrieben (Hash vorher gleich nachher); (4) Quellwache: `_render_diplomacy` enthaelt keine 40 oder 60 und keinen Vergleich auf die Gunst, nur den Aufruf `diplomatie.status`; (5) Gunst aendert weder Rachetopf noch Punkte; (6) `bot_als_dict`/`bot_aus_dict` tragen das Feld (Rundlauf). |
| Fertig-Kriterium | Wache 6 von 6 gruen, voller Sammellauf 0 rot, kein neues Feld ohne Ladewache. |
| Aufbauzeit-Effekt | keiner - eine Zahl ohne Wirkung. |
| Abloesung | keine; neue Felder additiv, nichts faellt. |
| Risiko | Zwei Speicher fuer eine Groesse (Feld plus Status) waeren schon hier der F-04-Fehler - deshalb Wache (4). |

### 2 - S4-2 Kennzahlenblatt

| Feld | Inhalt |
|---|---|
| Ziel | Jede Partie hinterlaesst einen messbaren Fingerabdruck, damit ab dem Rachetopf jede Aenderung eine Vorher-Zahl hat. |
| Dateien | geaendert: `tools/spieltest_simulation.py` (Kennzahlenblatt mit `--kennzahlen`), `tools/balancing_messung.py` (Kennzahlen uebernehmen, wo sie schon rechnet); neu: `docs/balancing/kennzahlen.jsonl` (eine Zeile je Partie), `docs/balancing/KENNZAHLEN_<Datum>.md`, `tests/test_kennzahlenblatt.py` |
| Aenderung | Zwoelf Pflichtschluessel je Partie: `startwert`, `stand`, `daten_hash`, `tag_erstes_haus`, `tag_erste_bibliothek`, `tag_erste_ware`, `tag_erster_krieger`, `tag_erstes_gefecht`, `ruhm_stufe`, `ausgaben`, `leerlauf_sek`, `fehlschlaege` (Aktion, Grund, Anzahl), `handelspunkte`, `beute_je_feldzug`, `verluste_je_gefecht`. Fehlt ein Meilenstein, steht `null` - nicht 0, sonst ist Nicht-Erreichtes von Null-Messung nicht zu unterscheiden. Zusaetzlich die Kennzahl `abstand_meilensteine_max` (laengste Strecke ohne neuen Meilenstein) als Spielgefuehl-Mass. |
| Daten | Punkte-Ziel 3,3 je Spieltag: V-3. Keine neuen Zahlen; die Baender kommen erst in B-1. |
| Wache | `tests/test_kennzahlenblatt.py`: (1) alle Pflichtschluessel vorhanden; (2) gleicher Startwert und gleicher Stand ergeben eine identische Zeile (ohne Zeitstempel); (3) fehlender Meilenstein ist `null`; (4) `daten_hash` aendert sich, wenn eine Datendatei geaendert wird; (5) das Werkzeug schreibt nur unter `docs/balancing/`, nie in `data/` oder `src/`. |
| Fertig-Kriterium | Ein Lauf ueber 12 Spieltage mit festem Startwert erzeugt eine Zeile; zwei Laeufe sind identisch. |
| Aufbauzeit-Effekt | keiner (nur Messung). |
| Abloesung | keine; das Kennzahlenblatt ist ein Zusatz zum vorhandenen Spieltest. |
| Risiko | Ohne Determinismus sind zwei Laeufe nicht vergleichbar. Vor dem Blatt pruefen: ist derselbe Startwert wirklich dasselbe Spiel? Wenn nicht, gehoert die Zufallsquelle in den Spielstand (eigener Schnitt, VORSCHLAG). |

### 3 - S4-3 Vertraege: Nichtangriffspakt, Handelsabkommen, Durchmarsch

| Feld | Inhalt |
|---|---|
| Ziel | Ein Nichtangriffspakt sperrt Bot-Angriffe **und** Diebstahl im Kern; ein Handelsabkommen nutzt den vorhandenen Handelsweg; das Durchmarschrecht ist eine reine Anzeige. |
| Dateien | geaendert: `src/diplomatie.py`, `data/diplomatie.json`, `src/main.py` (die zwei Gate-Stellen `:7051` und `:6624`, Knoepfe in `_render_diplomacy`), `src/punkte.py` bleibt unveraendert; neu: `tests/test_diplomatie_vertraege.py` |
| Aenderung | `diplomatie.vertrag_anbieten(daten, bot, art, jetzt) -> (ok, grund)`, `vertrag_aktiv(daten, bot, art, jetzt) -> bool`, `vertraege_tick(daten, bots, jetzt)` (Ablauf, Bruch unter 40). **Ein** Urteil fuer die Sperre: `diplomatie.angriff_gesperrt(bot, ziel_punkte, jetzt) -> (bool, grund)` fragt zuerst den Vertrag, dann `punkte.angreifbar`; die zwei Aufrufstellen in `main.py` rufen **diese** Funktion statt `punkte.angreifbar` direkt. `punkte.angreifbar` bleibt die einzige Rechenstelle der Punktgrenzen - die Sperre bekommt eine Vorbedingung, keine zweite Rechnung. Handelsabkommen ruft `spieloekonomie.handel_start` (kein zweiter Weg). Durchmarsch: Text ab Gunst 60, kein Aufruf in `auftraege`. |
| Daten | NAP ab Gunst 40, Dauer 3 Spieltage = 86.400 Spielsekunden, Bruch unter 40 kostet 20 Gunst und +1 Rachetopf, Durchmarsch ab 60: Auftragsdokument 7.2, also **VORSCHLAG** (kein Originalbeleg; 86.400 s ist rechnerisch 3 x 28.800 richtig). Handelsabkommen ab 40: VORSCHLAG. Schalter `vertraege_aktiv`. |
| Wache | `tests/test_diplomatie_vertraege.py`: (1) aktiver NAP: Angriff startet nicht, Grund `nap`; (2) dasselbe fuer den Diebstahl; (3) NAP laeuft nach genau 86.400 s ab, bei 86.399 s noch aktiv; (4) Gunst faellt auf 39: Pakt bricht, Gunst genau -20, Rache genau +1; (5) Angebot bei Gunst 39 wird abgelehnt; (6) Quellwache: beide `main.py`-Stellen rufen `diplomatie.angriff_gesperrt`, keine ruft `punkte.angreifbar` direkt; (7) Durchmarsch hat keine Mechanikwirkung; (8) alter Spielstand ohne `vertraege` laedt. |
| Fertig-Kriterium | 8 von 8 gruen, voller Sammellauf 0 rot. |
| Aufbauzeit-Effekt | senkt sie - ein Pakt verhindert Angriffe. |
| Abloesung | **keine Loeschung**: der direkte `punkte.angreifbar`-Aufruf in den zwei Zeilen wird durch die neue Funktion ersetzt, ihre Rechnung bleibt. Eigener Commit, weil sich der Aufrufweg aendert. |
| Risiko | Ein NAP, der nur in der Ansicht wirkt, ist wirkungslos - Wache (6) faengt genau das. |

### 4 - S4-4 Rachetopf und angekuendigter Angriff

| Feld | Inhalt |
|---|---|
| Ziel | Bots reagieren auf den Spieler: Niederlagen und Funkstille fuellen einen Topf; ab 3 folgt eine Ankuendigung, der Angriff erst wenn die eigene Armee 99 SK erreicht. |
| Dateien | geaendert: `src/diplomatie.py`, `data/diplomatie.json`, `src/main.py` (Niederlage im Bot-Angriff, Tageswechsel, Goetterschutz-Pruefung), `data/nachrichten.json` (Typ `ankuendigung`), `data/bot_stimmen.json` (Drohstufen 1/2/3); neu: `tests/test_diplomatie_rache.py` |
| Aenderung | `rache_buchen(daten, bot, grund)`, `rache_tag(daten, bots, jetzt)` (ruht unter `self.noob_protection` und waehrend eines laufenden Vertrags; je Bot und Spieltag hoechstens +1), `rache_bereit(daten, bot, armee_sk) -> bool` (Topf >= 3 **und** SK >= 99). Ankuendigung genau einmal je Ausloesung, Nachricht mit Vorlauf; danach laeuft der Angriff ueber den vorhandenen Raubzugweg (`_bots_raubzug` / Bot-Angriff in `main.py`) - kein zweiter Angriffspfad. Nach einem Bot-Sieg Topf 0 (F-3). |
| Daten | +1 je Niederlage, +1 je Spieltag ohne Kontakt, Schwelle 3: Auftragsdokument 7.2 = VORSCHLAG. Armee-Schwelle 99 SK: **V-5, UEBERNEHMEN** (G-2: 90 SK ist die Wall-Schwelle, nicht die Rache-Schwelle). Ruhen unter Goetterschutz und Vertrag: VORSCHLAG (G-1: `noob_protection` sperrt heute schon jeden Angriff, ein Topf ohne Ruhen feuerte am ersten Tag danach). Vorlauf 1 Spieltag = 28.800 s: VORSCHLAG (entspricht der Berichtsfrist). Schalter `rache_aktiv`. |
| Wache | `tests/test_diplomatie_rache.py`: (1) unter Goetterschutz bleibt der Topf nach 5 Tagen 0; (2) ohne Schutz und ohne Kontakt steht er nach 3 Tagen auf 3, nach 4 Tagen nicht auf 4 (Deckel je Tag); (3) Topf 3 mit SK 98: kein Angriff, mit SK 99: Angriff; (4) genau eine Ankuendigung je Ausloesung, vor dem Angriff; (5) nach Bot-Sieg Topf 0; (6) aktiver NAP blockiert trotz Topf 3; (7) alter Spielstand ohne `rache` laedt; (8) hoechstens ein laufender Auftrag je Bot und Ziel. |
| Fertig-Kriterium | 8 von 8 gruen, voller Sammellauf 0 rot, Kennzahlenblatt vorher/nachher mit gleichem Startwert. |
| Aufbauzeit-Effekt | erhoeht den Druck nach Niederlagen, nicht die Aufbauzeit selbst. |
| Abloesung | keine; die vorhandene Zeitwahl des Raubzugs bleibt, der Topf ist ein zusaetzlicher Ausloeser. |
| Risiko | Doppelangriff (Takt plus Rache) - Wache (8); Wechselwirkung mit dem NAP - deshalb Schritt 3 vorher. |

### 5 - S4-5 Ereignisse: Haug, Grom, Silra

| Feld | Inhalt |
|---|---|
| Ziel | Drei Bot-Ereignisse mit Frist ueber die vorhandene Overlay-Technik, mit Gunstwirkung und Ablehnung. |
| Dateien | geaendert: `src/diplomatie.py`, `data/diplomatie.json` (Ereignisse mit `quelle`), `src/main.py` (Tageswechsel, Overlay-Aufruf), `data/story.json` (Texte); neu: `tests/test_diplomatie_ereignisse.py` |
| Aenderung | `ereignis_erzeugen(daten, bot, art, jetzt)`, `ereignis_annehmen(daten, ort, id) -> (ok, grund)` (atomar: fehlt der Bestand **am Ort**, wird nichts gebucht), `ereignisse_tick(daten, orte, jetzt)` (Ablauf nach Frist). Annehmen Gunst +5, Ablehnen oder Ablauf -5. Texte in der Datendatei, nicht im Code. |
| Daten | Haug 990 Holz ODER 64 Gold, Silra 12 Gold (mindestens 1): **V-4, UEBERNEHMEN**; Rechenweg zusaetzlich in `docs/S0_TABELLEN_20261107.md` nachtragen (G-3). Grom 5 Waren gegen 20 Metall: VORSCHLAG, wartet auf F-1 (G-4: Werkzeuge und Eisen gibt es nicht). Frist 2 Spieltage = 57.600 s, Haeufigkeit 1 je Bot und 3 Spieltage, Gunst +5/-5: VORSCHLAG. Schalter `ereignisse_aktiv`. |
| Wache | `tests/test_diplomatie_ereignisse.py`: (1) Ablauf nach 57.600 s mit Gunst -5, bei 57.599 s noch offen; (2) Annahme mit 989 Holz abgelehnt, Bestand unveraendert; (3) Annahme Holz: genau 990 abgebucht, Gunst +5; (4) Silra bei Goldertrag 5: Preis faellt auf den Mindestwert 1; (5) Overlay und Kern lesen dieselbe Preisfunktion (Quellwache); (6) alter Spielstand ohne `ereignisse` laedt. |
| Fertig-Kriterium | 6 von 6 gruen, voller Sammellauf 0 rot, F-1 entschieden. |
| Aufbauzeit-Effekt | neutral - Ablehnen ist immer moeglich. |
| Abloesung | keine; die Overlay-Technik bleibt, wie sie ist. |
| Risiko | Ein Preis aus fester Zahl statt aus dem Ertrag - Wache (4). |

### 6 - S4-6 Handelspunkte: Erloes buchen und anzeigen

| Feld | Inhalt |
|---|---|
| Ziel | Ein normaler Spieler erzielt ohne Cheats Handelspunkte groesser 0, und die Auszeichnung Haendler bewegt sich. Grundlage ist G-8: die Kennzahl hat keine Quelle, der Handelsweg selbst ist fertig. |
| Dateien | geaendert: `src/main.py` (Buchung beim Abschluss, Anzeige :8813), `src/punkte.py` (nur falls ein Feldzugriff fehlt - die Rechnung bleibt unangetastet); neu: `tests/test_handelspunkte.py` |
| Aenderung | EINE Buchstelle: beim Abschluss eines Handelsvertrags (`spieloekonomie.handel_abschluss` liefert `vertrag["erloes"]`) den Erloes auf einen Zaehler `handels_erloes` im Spielstand addieren und `letzter_handel` auf die Spielzeit setzen - genau einmal je Vertrag (Feld `abgerechnet`). Die Anzeige uebergibt beide Werte an `punkte.auszeichnungen`; `punkte.handelspunkte` rechnet unveraendert (1 Punkt je 100 Gold, Verfall 1 je 24 Spielstunden). Kein neuer Handelsweg, keine neue Formel. |
| Daten | 1 Punkt je 100 Gold, Verfall 1 Punkt je 24 Stunden: `src/punkte.py:395-414`, belegt aus der Vorversion 2006 (`punktesystem.php`). Keine neuen Zahlen. |
| Wache | `tests/test_handelspunkte.py`: (1) E2E ohne gesetzte Zustaende: Karawane kauft beim Bot, Vertrag kommt an, Erloes gebucht, Handelspunkte groesser 0; (2) derselbe Vertrag wird **nicht** zweimal gebucht (Feld `abgerechnet`); (3) 100 Gold Erloes ergeben genau 1,0 Punkte, 20 Gold genau 0,2; (4) Verfall: nach 24 Spielstunden ein Punkt weniger, nicht unter 0; (5) Anzeige und `punkte.handelspunkte` liefern denselben Wert (Quellwache); (6) alter Spielstand ohne `handels_erloes` laedt mit 0. |
| Fertig-Kriterium | Wache 6 von 6 gruen, Kennzahlenblatt zeigt `handelspunkte` groesser 0 in mindestens einem von zehn Laeufen. |
| Aufbauzeit-Effekt | keiner - der Weg laeuft parallel zum Aufbau. |
| Abloesung | keine; nur ein fehlender Leser wird angeschlossen. |
| Risiko | Doppelbuchung bei jedem Tick - Wache (2) und die vorhandene Flagge `abgerechnet` schuetzen davor. |

### 7 - S4-7 Bot-Luecken: Drache, Spionage, Reaktion

| Feld | Inhalt |
|---|---|
| Ziel | Bots meiden oder schlagen den Drachen, spaehen vor einem Raubzug und reagieren auf den Spielerfortschritt - ohne neues Modul. |
| Dateien | geaendert: `src/bottaktik.py` (Entscheidung), `src/spionage.py` (vorhandener Weg, vertauschte Rollen), `src/drachen.py` (`bedrohung(ort)`), `src/main.py` (Aufrufer); neu: `data/bot_diplomatie.json` (Meidung, Spionagefrist, Reaktionsfaktoren - EINE Datei je Thema), `tests/test_bot_diplomatie.py` |
| Aenderung | `bottaktik.bot_drache_entscheidung(bot, drachenwert, eigene_sk) -> meiden/angreifen` (angreifen nur bei SK >= Drachenwert x Sicherheitsfaktor); vor einem Raubzug genau ein Spionageauftrag, wenn der letzte Bericht aelter als die Frist ist; Reaktionsstufe je Bot aus `data/bot_diplomatie.json` (Faktoren auf vorhandene Schwellen, keine neue Logik). Alle drei Gates (Goetterschutz, NAP, Demo) gelten auch fuer Spionage und Drachenzug. |
| Daten | Sicherheitsfaktor 1,5, Spionagefrist 1 Spieltag, Reaktionsfaktoren 0,8 bis 1,2, Meidungsstufen 3: alle VORSCHLAG (kein Originalbeleg, bewusst kleine Spanne). Schalter `aktiv`. |
| Wache | `tests/test_bot_diplomatie.py`: (1) SK unter der Schwelle: nie ein Auftrag gegen den Drachen; (2) SK darueber mit Profil `gierig`: angreifen; (3) vor einem Raubzug ohne frischen Bericht genau ein Spionageauftrag; (4) Spionage laeuft durch dieselben Gates wie der Angriff; (5) alter Spielstand ohne Profil laedt mit dem Standard; (6) im Automatenspiel kein Totalverlust gegen den Drachen in 10 Laeufen; (7) Kennzahlenblatt: `tag_erstes_gefecht` verschiebt sich um hoechstens einen Spieltag. |
| Fertig-Kriterium | 7 von 7 gruen, Sammellauf 0 rot, Kennzahlenblatt vorher/nachher. |
| Aufbauzeit-Effekt | kann sie heben (vorsichtige Bots) - deshalb Faktoren gedeckelt und Kennzahl (7). |
| Abloesung | keine; die Konstanten in `data/bot_raubzug.json` bleiben, die Faktoren multiplizieren sie. |
| Risiko | Die Profile machen Laeufe unvergleichbar - Gegenmittel: Profil haengt am festen Startwert. |

### 8 - B-1 Sollkurve aus den Daten

| Feld | Inhalt |
|---|---|
| Ziel | Ein Zielkorridor je Spieltag, gerechnet statt getippt. |
| Dateien | neu: `tools/balance_kreis.py` (Teil `sollkurve`), `data/sollkurve.json` (erzeugt, Kopf `erzeugt_aus` mit den Hashes der Eingabedateien), `tests/test_balance_kreis.py` |
| Aenderung | Aus `data/resources.json`, `data/baupreise.json`, `data/research.json`, `data/units.json` und der Startkarte spielt ein deterministischer Idealplan die belegte Kette nach; untere Grenze Ideal x 0,7, obere x 1,1. Punkte-Ziel 3,3 je Spieltag (V-3). |
| Daten | 3,3 Punkte je Spieltag: V-3. Baender 0,7 und 1,1, Goldband und Punkteband: VORSCHLAG. |
| Wache | `tests/test_balance_kreis.py`: (1) Neu rechnen ohne Datenänderung ergibt eine identische Datei; (2) Holz plus 10 Prozent in `resources.json` verschiebt den Holzkorridor; (3) `balance_kreis.py` schreibt nie unter `src/`. |
| Fertig-Kriterium | `data/sollkurve.json` erzeugt, zwei Laeufe identisch, Test 3 von 3 gruen. |
| Aufbauzeit-Effekt | keiner. |
| Abloesung | keine. |
| Risiko | Der Idealplan ist eine Annahme - er steht als VORSCHLAG in der Datei, nicht als Wahrheit. |

### 9 - B-2 Regelkreis, A/B-Urteil und Feedback

| Feld | Inhalt |
|---|---|
| Ziel | Abweichungen werden gemessen, Aenderungen vorgeschlagen, vorher/nachher belegt und erst dann angenommen. |
| Dateien | geaendert: `tools/balance_kreis.py`; neu: `docs/balancing/URTEIL_<n>.md`, `docs/feedback/VORLAGE.md`, `docs/feedback/BUENDEL.md`, `tests/test_balance_urteil.py` |
| Aenderung | `messung` (10 Laeufe, Startwerte 1..10), `vorschlag` (hoechstens EIN Datenwert je Runde, Schrittweite hoechstens 10 Prozent, BELEGT-Werte nie vorschlagen), `ab` (dieselben Startwerte mit und ohne Aenderung, Daten in temporaerer Kopie, kein Schreiben in `data/`), `urteil` (Zielabweichung mindestens 20 Prozent besser, keine andere Groesse aus dem Korridor, `tag_erstes_gefecht` nicht spaeter). Feedback: Vorlage mit Was, Wann, Stand, Zahl, Gefuehl 1-5; ab 3 Meldungen mit demselben Schluessel wird daraus ein Messauftrag. |
| Daten | Schwellen 20 Prozent Verbesserung, 10 Prozent Schrittweite, 3 Meldungen: VORSCHLAG (C 4.3, U 15 Prozent - beide ohne Beleg). |
| Wache | `tests/test_balance_urteil.py`: (1) identische Listen ergeben nicht angenommen; (2) Ziel 50 Prozent besser, aber eine andere Groesse schlechter: abgelehnt mit Nennung; (3) ungleiche Startwert-Reihenfolge ist ein Fehler; (4) `tag_erstes_gefecht = null` wird uebergangen, nicht als 0 gezaehlt; (5) zwei gleiche Meldungen ergeben ein Buendel mit Zaehler 2. |
| Fertig-Kriterium | 5 von 5 gruen, ein vollstaendiger Durchlauf messen - vorschlagen - ab - urteil auf dem heutigen Stand protokolliert. |
| Aufbauzeit-Effekt | keiner (Werkzeug). |
| Abloesung | keine. |
| Risiko | Der Regelkreis kalibriert auf das Automatenspiel statt auf Menschen - deshalb sticht ein Tester-Buendel (3 Meldungen) eine reine Kennzahl, und Daniel entscheidet. |

### 10 - A-1 E2E-Ketten auf 12 Wege erweitern

| Feld | Inhalt |
|---|---|
| Ziel | Jeder Spielweg ist als Kette ohne gesetzten Zustand belegt. |
| Dateien | neu: `tests/test_e2e_wege.py` (Vorlage: `tests/test_produktionskette_ohne_cheats.py`); vorhanden und unveraendert: `tests/test_durchspiel.py`, `tests/test_gpt_wirtschaft_kette_e2e.py` |
| Aenderung | Zwoelf Ketten: Rohstoff, Forschung, Ware, Ausbildung, Einsatz, Rueckkehr, Speichern/Laden, Handel (Schritt 6), Heilung, Mauerreparatur, Vertrag (Schritt 3), Portal als Langweg. Der Portalweg laeuft mit Zeitsprung im Tick, nicht in Echtzeit (5.000 Mana bei 120 je Tag sind 41,7 Spieltage, E-6). Keine Spielmechanik wird geaendert. |
| Daten | keine neuen Zahlen; Portal 5.000 Mana / 120 je Tag aus `data/`. |
| Wache | `tests/test_e2e_wege.py`: je Weg eine Kette ohne `state.<feld> = `-Zuweisung ausser dem Startwert. |
| Fertig-Kriterium | 12 von 12 gruen, voller Sammellauf 0 rot. |
| Aufbauzeit-Effekt | keiner. |
| Abloesung | keine. |
| Risiko | Laufzeit (G-5) - deshalb nach Schritt 12 messen, nicht vorher. |

### 11 - A-2 AST-Quellwache fuer die Ansichten

| Feld | Inhalt |
|---|---|
| Ziel | Keine Ansicht rechnet selbst; Docstrings und Kommentare zaehlen dabei nicht als Code. |
| Dateien | neu: `tests/test_quelle_ast.py`, `tests/quelle_ast_ausnahmen.json` (begruendete Ausnahmen, z. B. Pixelrechnung im Canvas) |
| Aenderung | Ueber `ast` werden die Methoden von `NebelseetalApp` geprueft, deren Name mit `_zeige`/`_zeichne`/`_render` beginnt (aus dem Quelltext ableiten, nicht raten): jede Multiplikation oder Division auf einen Datenwert und jeder Vergleich gegen eine Ganzzahl groesser 1 ist ein Befund, ausser er steht in der Ausnahmeliste. |
| Daten | keine neuen Zahlen. |
| Wache | die Datei selbst: sie muss auf dem heutigen Stand gruen sein und bei einer absichtlich eingebauten Rechnung rot werden (Gegenprobe im Test). |
| Fertig-Kriterium | gruen, Gegenprobe rot, Sammellauf 0 rot. |
| Aufbauzeit-Effekt | keiner. |
| Abloesung | die Textwachen bleiben; die AST-Wache kommt hinzu, keine wird entfernt. |
| Risiko | Zu breite Muster erzeugen Falschalarm - Gegenmittel ist die Ausnahmeliste mit Begruendung, nicht ein gelockertes Muster. |

### 12 - A-6 Sammellauf messen und beschleunigen

| Feld | Inhalt |
|---|---|
| Ziel | Der Sammellauf ist wieder eine belastbare Rueckmeldung: 0 rot und eine Grenze, die dem gemessenen Lauf entspricht. |
| Dateien | geaendert: `tools/sammellauf.py` (Schalter `--parallel N`, Standard 1), `docs/extern/Nebelseetal_LLM_Auftrag_20261106.md` (A-6 neu fassen), `docs/AKTUELLER_STAND.md`; neu: `tests/test_sammellauf_parallel.py` |
| Aenderung | Erst messen (Ist 1.612 s, 183 Dateien), dann `--parallel` mit `ProcessPoolExecutor`, Vorbedingung: keine Pruefdatei schreibt in einen gemeinsamen Pfad. A-6 wird auf die gemessene Zahl umgestellt (VORSCHLAG 1.800 s), nicht stillschweigend gesenkt. Die zwei Dateien ohne Ergebniszeile bekommen eine Pflichtzeile, sonst kann ein Parallel-Lauf gruen nicht von nichts geprueft unterscheiden. |
| Daten | 1.612 s und 7.502 Pruefungen: G-5 (gemessen). 1.400 s und 7.495: Auftrag A-6 (alt). Neue Grenze: VORSCHLAG, Daniel bestaetigt (F-2). |
| Wache | `tests/test_sammellauf_parallel.py`: Aufruf mit `--parallel 1` und `--parallel 4` liefert identische Ergebnislisten; Rueckgabewert ist 0 nur bei 0 rot. |
| Fertig-Kriterium | zwei Laeufe mit verschiedenen Prozesszahlen liefern dieselbe Liste; A-6 nennt die gemessene Grenze. |
| Aufbauzeit-Effekt | keiner. |
| Abloesung | Der Einprozess-Lauf bleibt Standard; `--parallel` ist ein Schalter, keine Abloesung. |
| Risiko | Parallelitaet erzeugt Flakiness - deshalb nur nach der Identitaetspruefung, und ein roter Lauf im Parallelbetrieb gilt als nicht belastbar. |

### 13 - A-7/A-5 Schlusspruefung

| Feld | Inhalt |
|---|---|
| Ziel | Jede Balance-Zahl liegt in `data/`, jede Mechanik hat einen Schalter, jede Zahl traegt eine Quelle oder das Wort VORSCHLAG. |
| Dateien | neu: `tests/test_daten_und_quellen.py` |
| Aenderung | Das Werkzeug prueft drei Dinge: keine Balance-Zahl im Code (Ausnahmen begruendet), ein Schalter `aktiv` je Mechanik, jede Zahl in den neuen Datendateien mit `quelle`. Was fehlt, wird als VORSCHLAG an Daniel gemeldet, nicht erfunden. |
| Daten | keine neuen Zahlen. |
| Wache | die Datei selbst, drei Abschnitte. |
| Fertig-Kriterium | gruen, offene VORSCHLAG-Zahlen in `docs/FRAGEN_AN_DANIEL_20261107.md` nachgetragen. |
| Aufbauzeit-Effekt | keiner. |
| Abloesung | keine. |
| Risiko | Ein zu strenges Muster macht bestehende Dateien rot - dann Ausnahmen mit Begruendung, keine Lockerung. |

### L - Neuer KI-Auftrag aus diesem Ablauf (Meldepflicht)

| Feld | Inhalt |
|---|---|
| Ziel | Eine zweite Runde mit anderen Modellen, diesmal mit dem fertigen Ablauf im Ruestzeug. |
| Dateien | Die **geschuetzte** Datei `C:\Users\saras\Desktop\Nebelseetal_LLM_Auftrag_20261106.md` bleibt bis zu diesem Schritt unberuehrt; die neue Fassung bekommt einen eigenen Namen mit Datum. |
| Aenderung | Die Fassung nennt: Stand (Version, Kopf-Commit), diesen Ablauf, den Stand des Codes, die vier Prueffragen, dieselben Ablagehinweise. |
| Fertig-Kriterium | Entwurf liegt auf dem Desktop, **und Daniel ist ausdruecklich darauf hingewiesen** (er hat das woertlich verlangt). |
| Aufbauzeit-Effekt | keiner (Dokument). |

## 4. Was wir von dir wollen (Runde 2)

Runde 1 hat den Ablauf geliefert. Runde 2 soll ihn **zerlegen**, nicht wiederholen. Beantworte in
acht Teilen:

**Teil 1 - Der schwaechste Schritt.** Nenne genau EINEN der 13 Schritte, den du fuer den
fehleranfaelligsten haeltst, mit Begruendung und mit dem konkreten Fall, der ihn widerlegen wuerde.
Nicht drei, nicht alle - einen.

**Teil 2 - Die schwaechste Wache.** Nenne je Schritt hoechstens eine Wache, die nichts beweist (weil
sie den Zwischenzustand selbst schreibt, weil sie nur die Anzeige prueft oder weil sie eine Zahl
festnagelt, die sich legitimaendern darf), und sage, welche Pruefung sie ersetzen sollte.

**Teil 3 - Die Zahl ohne Beleg.** Der Ablauf markiert mehrere Werte als VORSCHLAG (Gunst-Start 50,
NAP-Dauer 3 Spieltage, Bruch -20, Rachetopf-Schwelle 3, Frist der Ereignisse 2 Spieltage, Gunst
plus/minus 5, Sicherheitsfaktor Drache 1,5, Profilfaktoren 0,8 bis 1,2, Sollkurven-Baender 0,7 und
1,1). Ordne sie nach Risiko fuer das Spielgefuehl, gefaehrlichste zuerst, und nenne zu jeder genau
EINE Messung, die sie vor dem Einbau pruefbar macht (Kennzahl, Laufzahl, Startwerte).

**Teil 4 - Die fehlende Abhaengigkeit.** Der Ablauf behauptet eine Reihenfolge. Nenne eine
Abhaengigkeit, die dort NICHT steht, aber noetig ist, oder beweise, dass die Reihenfolge tragfaehig
ist. Achte besonders auf: Kennzahlenblatt vor dem Rachetopf, Vertraege vor dem Rachetopf,
Bot-Luecken nach den Ereignissen, E2E-Ketten ganz am Ende.

**Teil 5 - Der Schritt, der weg kann.** Nenne einen Schritt, der ohne Schaden fuer A-1 bis A-7
gestrichen werden koennte, mit Begruendung. Wenn keiner streichbar ist, sage das und begruende es.

**Teil 6 - Die Wechselwirkung, die keiner sieht.** Der Ablauf fuehrt Vertraege (Nichtangriffspakt),
Rachetopf, Ereignisse und Bot-Profile ein. Nenne eine Wechselwirkung zwischen zweien davon, die im
Ablauf nicht bedacht ist, und die kleinste Wache, die sie abfaengt.

**Teil 7 - Die Aufbauzeit.** Ziel des ganzen Ablaufs ist der Zustand, in dem nur noch Balancing und
Bugfixing noetig ist - NICHT eine kuerzere Aufbauzeit. Pruefe fuer jeden Schritt, ob sein
Aufbauzeit-Effekt im Ablauf richtig angegeben ist, und nenne die Stelle, an der du widersprichst.

**Teil 8 - Die drei Pruefungen, die den Ablauf am schnellsten widerlegen.** Je eine Zeile: was tun,
was messen, was waere das Ergebnis, das den Ablauf kippt.

## 5. Form und Grenzen

- **Deutsch, Markdown, keine Emojis.** Tabellen wo das hilft.
- **Jede Zahl traegt ihre Herkunft** (Handbuch 2009 mit Seite, 2006er Seite, Datendatei, gerechnete
  Tabelle) oder das Wort VORSCHLAG. Eine plausible Zahl ohne Quelle ist ein Fehler, auch wenn sie
  zufaellig stimmt.
- **Kein Code.** Signaturen als Vorschlag sind erlaubt, muessen aber als Vorschlag gekennzeichnet
  sein. Du hast keinen Zugriff auf das Repository - was du nicht wissen kannst, schreibst du als
  Annahme hin, nicht als Tatsache.
- **Kein Alternativplan.** Eine Empfehlung, nicht drei Varianten.
- **Keine Wiederholung von Abschnitt 3.** Was dort steht, ist beschlossen; du pruefst es, du
  referierst es nicht.
- **S5 Siedlungsumzug ist gesperrt.** Vorschlaege erlaubt, Einbau nicht.

## 6. Ablage

Diese Datei ist die Projektfassung. Deine Antwort bitte als eine zusammenhaengende Markdown-Datei mit
den acht Teilen, Kopfzeile mit Modellname, Datum und der Dokumentversion, die hier steht
(`V_0.0.3`, Stand 06.11.2026). Wenn du Dateien anhaengst, dann als echte Anhaenge; eine gespeicherte
Chat-Seite mit Verweisen gilt nicht als Lieferung.

Pruefe deine Antwort vor der Abgabe an diesen vier Fragen (dieselben wie in Runde 1):

1. Passt der Vorschlag zur Mechanik, wie sie in Abschnitt 1 bis 3 beschrieben ist?
2. Ist die Zahl belegt - und wenn nicht, steht VORSCHLAG dabei?
3. Hilft es dem Spielgefuehl (dichter Aufbau, sichtbare Reaktion der Welt, keine Sackgasse)?
4. Braucht es ein neues Bauteil - und wenn ja, warum reicht keines der vorhandenen?
