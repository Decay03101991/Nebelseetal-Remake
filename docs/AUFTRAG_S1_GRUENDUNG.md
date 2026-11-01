# AUFTRAG: Schnitt S-1 — die Gründung bringt Tempel, Holzfäller und Steinmetz mit (01.11.2026)

Du bist **Spielarchitekt und Programmierer** eines abgegrenzten Umbaus. Du änderst genau zwei Dateien.

## 0. Rolle und harte Grenzen

* **Erlaubt:** alles im Projekt `D:\Arbeiten\Nebelseetal_Remake` lesen; **genau zwei** Dateien ändern:
  `src/main.py` und **neu** `tests/test_gruendung_startgebaeude.py`.
* **Verboten:** andere Dateien ändern (auch nicht `data/*.json` — lies sie nur), löschen, verschieben;
  `git` schreiben (nur `git status`/`git diff` lesen); das Spiel oder die EXE starten.
* Prüfdatei **reines ASCII** (keine Umlaute, kein ß, kein Gedankenstrich).
* Keine Zahl als Originalwert ausgeben, die keine Quelle hat. Jeder eigene Wert trägt im Code den
  Vermerk `VORSCHLAG`.

## 1. Die Vorgabe (bindend, Daniel 01.11.2026)

> „Der Siedlungskarren liefert bei der Gründung mit: Siedler, Grundrohstoffe und drei Gebäude —
> Holzfäller (möglichst auf Wald), Steinmetz (möglichst auf Hügel oder Berg), Tempel (möglichst auf
> Nebelsee; ohne Nebelsee auf Steppe).“ — `docs/KONZEPT_SECHS_DOERFER_20261101.md`, Abschnitt 1 und Anhang 1.

Festgelegt ist außerdem:

* **Tempel-Ausnahme bei der Gründung:** „Ausnahme bei Gründungssetzung weil der Siedlungskarren diesen
  Tempel quasi schon mitbringt“. Der **Nachbau** eines Tempels verlangt weiter `Baukunst`.
* **Startressourcen je Dorf: 10 Siedler, 100 Holz, 100 Stein** (belegte Startwerte des Handbuchs).
* **Die Platzwahl ist Geländevorliebe, kein Zwang:** findet sich kein Wunschgelände, nimmt die Gründung
  das beste freie Feld und **sagt es in der Meldung**.
* Der **Portalplatz entfällt** als Gebäude: der Tempel ist der Reiseort (Anhang 1). Kein neues Gebäude
  `portal` bauen.

## 2. Ist-Zustand, der vorher zu lesen ist (nicht raten)

Lies in dieser Reihenfolge, bevor du eine Zeile schreibst:

1. `docs/KONZEPT_SECHS_DOERFER_20261101.md` — Abschnitt 1, 3 (M-1 bis M-5) und **beide Anhänge**.
2. `src/main.py`: `_erste_siedlung_gruenden`, `_found_settlement`, `_kolonie_gruenden`,
   `_aktive_siedlung`/`aktive_siedlung`, `GameState` gegen `NebelseetalApp` (zwei Klassen! `self.state`
   gibt es nur in der App), `siedlung_startressourcen` oder wie die Startwerte heute gesetzt werden.
3. `src/gelaende.py` — wie Geländearten heißen (`Wald`, `Hügel`, `Berg`, `Nebelsee`, `Steppe`, `Sumpf`)
   und wie ein Feld belegt wird (`bau_moeglich`, `bauen_auf_karte` oder wie die Funktionen heißen).
4. `data/buildings.json` (Gebäudeliste, `voraussetzung`, `ertrag_pro_stunde`, Geländeerträge),
   `data/baupreise.json`, `data/gelaende.json`.
5. `src/wirtschaft.py` — wie Erträge je Feld gerechnet werden (die Meldung soll den erwarteten Ertrag
   nennen können, ohne eine zweite Rechnung zu bauen).
6. `tests/test_startspiel.py` und `tests/test_originalkarten_baukasse.py` — was dort über die Gründung
   behauptet wird. **Diese Zusagen dürfen nicht still brechen**: entweder sie gelten weiter, oder du
   benennst sie um und der Docstring nennt die Entscheidung und ihre Quelle.

## 3. Was gebaut werden soll

1. **Bei JEDER Gründung** (erstes Dorf **und** jede Kolonie) setzt der Kern zusätzlich zum bisherigen
   Start: **Holzfäller** (bevorzugt auf `Wald`), **Steinmetz** (bevorzugt auf `Hügel` oder `Berg`),
   **Tempel** (bevorzugt auf `Nebelsee`, sonst `Steppe`).
   * Diese drei Gebäude kosten den Spieler **nichts** (der Karren bringt sie mit) und **binden keine
     Siedler** — die Startressourcen bleiben 10 Siedler / 100 Holz / 100 Stein. Wenn die Datenlage es
     anders erzwingt, ändere **nichts** an den Daten, sondern setze die Gebäude über den Kern.
   * Der Tempel wird **ohne** `Baukunst` gesetzt (Ausnahme). Ein späterer Nachbau bleibt forschungspflichtig.
2. **EINE Funktion für die Platzwahl** (z. B. `_startgebaeude_setzen(ort, karte)`), die
   * je Gebäude das Wunschgelände in einer **Vorlieben-Tabelle** führt (keine if-Kette),
   * die Reihenfolge so wählt, dass sich die drei Gebäude nicht gegenseitig den Platz wegnehmen,
   * für jedes gesetzte Gebäude zurückgibt: Gebäude, Gelände am Feld, Feldkoordinate und ob es das
     Wunschgelände war oder ein Ersatz.
3. **Die Meldung nennt die Felder.** Ein Satz je Gebäude in der Form
   `Tempel auf Nebelsee (4,7) · Holzfäller auf Wald (2,7) · Steinmetz auf Huegel (7,5)` und, wenn ein
   Wunschgelände fehlte, ausdrücklich `kein Wald frei - Ersatz auf Steppe (3,3)`. Die Meldung geht in
   `state.messages` **und** in `state.log` (wie die anderen Gründungsmeldungen) und muss **deutsche
   Anführungszeichen paarig** führen, wenn sie welche benutzt.
4. **Kein stiller Fehlschlag:** ist die Karte zu klein oder voll, setzt der Kern so viele Gebäude wie
   möglich, nennt die fehlenden in der Meldung und wirft **nicht**.
5. **Rückwärtsverträglich:** ein alter Spielstand ohne diese Gebäude lädt weiter; die Funktion läuft nur
   bei einer Gründung.

## 4. Die Prüfdatei `tests/test_gruendung_startgebaeude.py`

Stil wie `tests/test_startspiel.py` (`harness`: `abschnitt`, `check`, `ausnahme`, `bericht`,
`import_src`), reines ASCII, **kein** Netz, **kein** sichtbares Fenster (`root.withdraw()`).
Mindestens diese Prüfungen, jede mit einer echten Zahl im Detailtext:

1. Erste Gründung: genau die drei Gebäude stehen danach auf der Karte, jedes mit seiner Stufe 1.
2. Wunschgelände: gibt es Wald, steht der Holzfäller auf Wald; gibt es Nebelsee, steht der Tempel dort.
   (Karte mit passendem Gelände aus den echten Kartendaten bauen, nicht erfinden.)
3. Ersatzfall: eine Karte **ohne** Nebelsee — der Tempel steht trotzdem, die Meldung sagt, welches
   Gelände es wurde.
4. Startressourcen: 10 Siedler, 100 Holz, 100 Stein bleiben **unverändert** (die Gebäude kosten nichts).
5. Tempel ohne Baukunst: die Gründung setzt ihn trotzdem; ein **Nachbau** über den normalen Bauweg wird
   ohne Baukunst weiter abgelehnt (beide Seiten prüfen).
6. Kolonie: eine zweite Siedlung bekommt dieselben drei Gebäude (nicht nur die erste).
7. Meldung: sie nennt alle drei Gebäude mit Gelände und Koordinate, und sie steht in `state.messages`
   und in `state.log`.
8. Volles Feld / kleines Dorf: der Kern wirft nicht und nennt in der Meldung, was fehlt.
9. Quelltext-Wachen (`inspect.getsource`): die Platzwahl ist **eine** Funktion; die drei Gebäude kommen
   aus einer Vorlieben-Tabelle; im Gründungspfad steht kein `random` (die Wahl ist Gelände, kein Würfel).

## 5. Fertig-Definition

* `python -X utf8 -c "import sys;sys.path.insert(0,'src');import main"` läuft.
* `python -X utf8 tests/test_gruendung_startgebaeude.py` **grün** (0 Fehler).
* `python -X utf8 tests/test_startspiel.py`, `tests/test_durchspiel.py`,
  `tests/test_originalkarten_baukasse.py`, `tests/test_auftraege.py` laufen (Ergebnis nennen; wenn eine
  Datei rot wird, ist deine Änderung schuld — reparieren, nicht die Prüfung löschen).
* `git status --porcelain` zeigt **nur** `src/main.py` und die neue Prüfdatei (git nur lesen).
* Antworte am Ende **nur** mit: `FERTIG <Zeilen main.py diff> <Pruefungen gruen> <rot> <Dateien>`.

Wenn eine Vorgabe mit dem Code unvereinbar ist, baue **nicht** auf Verdacht: halte die Stelle in der
Antwort fest (Datei, Zeile, Widerspruch) und baue den Rest.
