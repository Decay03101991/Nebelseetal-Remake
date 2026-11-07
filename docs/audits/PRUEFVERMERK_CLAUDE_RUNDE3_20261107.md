# Prüfvermerk: Claude Sonnet 5.5, Runde 3 (07.11.2026)

Quelle: `C:\Users\saras\Desktop\Claude_Sonnet_Antwort_Runde3.txt` **die Datei hat Daniel selbst angelegt**, weil das Modell die Sitzung beendet
und nur Text im Chat hinterlassen hat (bestaetigt 07.11.2026, 21:15; Ablage unter
`docs/extern/`). Auftrag war
`docs/extern/Nebelseetal_LLM_Auftrag_Runde3_20261107.md`.

**Was geliefert wurde:** keine Dateien. Die Antwort sagt selbst, das Werkzeuglimit sei vor dem
Schreiben erreicht worden; zehn Dateien und ein `20261107_Runde3_Dokument.md` fehlen. Sieben von zehn
Teilen (A, B, C, D, G, I, J) erreichen die geforderte Untergrenze von acht Befunden, die Teile E, F und
H nicht. Nichts im Repository wurde verändert, committet oder gepusht.

**Was das für die Abnahme heißt:** als **Lieferung** ist Runde 3 nicht erfüllt (kein Paket, drei Teile
unter Umfang). Als **Befundsammlung** ist sie brauchbar und wird hier nach der Projektregel behandelt:
jeder Befund wird am heutigen Code nachgemessen und als bestätigt, widerlegt oder offen geführt.

## 1. Selbst nachgemessen am Code von `bd59488` (bestätigt)

| Nr | Behauptung | Beleg im Projekt | Urteil |
|---|---|---|---|
| I-1 | Die Ereignisart wird nach dem **Index** des Bots rotiert, nicht nach seinem Namen | `src/main.py:7251` `_art = _arten[_index % len(_arten)]`, Meldung `"%s: %s" % (_bot_ereignis.name, _titel_ereignis)` (7258). Arten: `haug, grom, silra` (`data/diplomatie.json`), Bots: Haug, Brynhild, Grom, Silra, Krank (`src/botkern.py:54`) → „Brynhild: Grom braucht Messer“ ist möglich | **BESTÄTIGT**, Schwere hoch (Text und Wirkung treffen verschiedene Figuren) |
| A-1 | Zwei Spieltag-Längen im selben Spiel | `data/diplomatie.json:66-68`: `spieltag_sekunden`, `vorlauf_sekunden`, `nach_paktende_sekunden` = **28800**; `src/diplomatie.py:445,496,503` liest sie; `src/botkern.py:38` und `src/punkte.py:42`: `SEKUNDEN_JE_TAG = 86400`. Folge: die Frist `frist_sekunden: 57600` ist als „zwei Spieltage“ dokumentiert, sind aber 0,67 Tage; Rachetopf und Vorlauf laufen alle 8 statt 24 Spielstunden | **BESTÄTIGT**, Schwere hoch (Zahlen, die niemand als falsch sieht) |
| I-3 | Haug und Silra haben keine Gegenleistung | `data/diplomatie.json` Block `ereignisse.arten`: `haug.gegenleistung = {}`, `silra.gegenleistung = {}`, `grom.gegenleistung = {metall: 20}`. Silras Text verspricht einen Umweg (`data/story.json`) | **BESTÄTIGT** (Grom hat eine, die beiden anderen nicht) |
| C-4 | `drachen.json` führt je Drache zwei widersprüchliche Einheitenangaben | `einheiten = {Krieger 20, Bogenschütze 20}` **und** `verteidigung.einheiten = {Krieger 120, Bogenschütze 60, Paladin 24}` bei allen drei Drachen (`drache_d02/d03/d05`). Welche im Kampf zählt, ist **nicht gemessen** | **BESTÄTIGT** als Datenwiderspruch; die Wirkung ist offen (F-04-Muster: zwei Wahrheiten) |
| I-10 | `story.ausgang_text` ist ein toter Pfad | Aufrufe nur in `tests/test_story.py:95`; in `src/main.py` wird bei Niederlage `punkte.spielausgang` angezeigt | **BESTÄTIGT** |
| C-6 | Das Wort „VORSCHLAG:“ steht in einer Spielermeldung | `src/punkte.py:301` (Text der Niederlage) | **BESTÄTIGT**, sichtbar für den Spieler |
| G-1 | Das Register hat Lücken | 294 Zeilen, höchste Nummer 296, **272 und 273 fehlen** (per Skript über die Tabellenzeilen gezählt) | **BESTÄTIGT** (die Antwort nannte 293/295 — der Stand ist inzwischen 296) |

**Widerlegt als Fehler, bestätigt als Entscheidung:** B-5 (Handelspunkte fließen nicht in
`gesamtpunkte`). Das ist im Code ausdrücklich begründet (`src/punkte.py:388-395`: die 2006er Fassung
rechnet drei Drittel, das Handbuch 2009 kennt zwei Arten) — es ist eine dokumentierte Abweichung, kein
Fehler. Die Antwort führt es selbst als „TEILWEISE“.

## 2. Nicht nachgemessen — als offene Prüfung geführt

I-2, I-4 bis I-9, I-11 bis I-13, A-2 bis A-9, B-1 bis B-8, D-1 bis D-8, E-1 bis E-3, F-1 bis F-3,
G-2 bis G-7, H-1 bis H-4. Sie stehen in der Antwort mit Zeilenbelegen; nach der Projektregel gilt ein
fremder Befund erst nach eigener Messung als bestätigt. Sie werden in der Reihenfolge aus Abschnitt 4
einzeln nachgemessen, nicht vorab geglaubt.

**Zwei Aussagen der Antwort sind bereits jetzt zu berichtigen:**

- **„Entscheiden muss Daniel als Erstes die Spieltag-Definition vor Schritt 9“** — Schritt 9 ist seit
  20:15 gebaut und gepusht (`91a6525`, Register 296). Die Reihenfolge der Antwort ist überholt.
- **„Spielbar: UNBEKANNT, der Sammellauf war ohne tkinter nicht ausführbar“** — das ist ein Befund
  über die **Sandbox des Modells** (Python 3.12 ohne tkinter), nicht über das Projekt. Der Sammellauf
  lief hier am 07.11.2026 um 20:18 mit dem Projekt-venv: 192 von 194 grün, 0 rot.
- **G-3 (Handbuch heißt 2009, trägt aber 2006)** ist ein **bekannter** Punkt: das Projekt führt die
  beiden Fassungen getrennt (`docs/quellen/ABWEICHUNGEN_2006_zu_2009.md`) und behandelt
  Balance-Zahlen aus 2009, Struktur aus beiden. Kein neuer Befund.

## 3. Was die Antwort über die eigene Arbeit sagt (ehrlich und brauchbar)

Sie nennt selbst, was sie nicht gelesen hat (Story-Bibel, Gesamtkonzept, Vorgaben,
`FRAGEN_AN_DANIEL`, die `ORIGINAL_*`-Dokumente, `tools/`, den Großteil von `src/` und `tests/`) und
markiert geschätzte Zeilennummern mit „ca.“. Zehn Punkte stehen unter „wo ich unsicher bin“. Das ist
die Form, die der Auftrag verlangt hat — nur der Lieferumfang fehlt.



**Lehre fuer Runde 4 (von Daniel bestaetigt):** der Auftrag muss verlangen, dass die Antwort
auch dann als DATEI entsteht, wenn die Sitzung frueher endet - also in mehreren kleineren
Antworten mit Zwischenablage, statt alles am Ende schreiben zu wollen. Sonst legt der
Empfaenger die Datei selbst an, und die Abgabe ist nicht mehr maschinell pruefbar. Kosten
dieses Laufs: **0 USD** (Daniels kostenloses Versuchsguthaben bei Claude).

## 4. Vorschlag für die Reihenfolge (Frage F-21 an Daniel)

Nach Schwere und Aufwand, gemessen an dem, was ich selbst bestätigt habe:

| Paket | Inhalt | Aufwand | Warum zuerst |
|---|---|---|---|
| R3-1 | **A-1 Spieltag-Definition** vereinheitlichen (86.400 s), Diplomatie-Zahlen umrechnen (Frist, Vorlauf, Pakt, Rachetopf) | 60 min | falsche Zeitbasen verfälschen jede spätere Messung, auch den Regelkreis |
| R3-2 | **I-1 Ereignis-Zuordnung** am Botnamen festmachen + Wache | 30 min | der sichtbarste Fehler im Spiel (Text nennt den falschen Bot) |
| R3-3 | **C-6** „VORSCHLAG:“ aus Spieltexten entfernen, **I-10** `ausgang_text` an Sieg/Niederlage hängen, **C-4** klären, welche Drachen-Einheiten zählen | 90 min | kleine, sichere Schnitte mit großer Wirkung auf den Eindruck |
| R3-4 | **I-2** Ereignisse erst ab einer Wirtschaftsschwelle und mit ortsrelativen Preisen | 60 min | der Anfänger wird sonst in 29 Echtminuten feindselig gestellt |
| danach | Schritte 10 bis 13 des Ablaufs (A-1-Codekette, AST-Wache, Sammellauf, Schlussprüfung) | 5 h | wie geplant |

**Empfehlung:** R3-1 und R3-2 vor Schritt 10 einschieben (zusammen 90 min, beide mit eigenen Wachen),
R3-3 und R3-4 danach. Grund: A-1 verändert Zahlen, die in jede folgende Messung eingehen, und I-1 ist
im Spiel sichtbar.

## 5. Kosten und Ablage

Der Lauf hat **nichts gekostet** (Daniels Testlauf bei Claude, keine API-Abrechnung im Projekt). Diese
Prüfung ist rein lokal. Die Antwort liegt als Textdatei bei, die Ablage erfolgt unter
`docs/extern/Claude_Sonnet_Antwort_Runde3_20261107.txt`.
