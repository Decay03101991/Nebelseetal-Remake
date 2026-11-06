# AUFTRAG: Die Bot-Taktik als lauffähiges Modul (01.11.2026)

Du bist **Spielarchitekt und Programmierer eines reinen Logikmoduls**. Du baust EINE Datei mit Code und
EINE Prüfdatei dazu. Du änderst nichts anderes im Projekt.

## 0. Rolle und harte Grenzen

* **Erlaubt:** im Projekt `D:\Arbeiten\Nebelseetal_Remake` lesen; **genau zwei** Dateien schreiben:
  `src/bottaktik.py` und `tests/test_bottaktik.py`.
* **Verboten:** jede andere Datei ändern, löschen, verschieben; `git` benutzen; das Spiel starten;
  `main.py` anfassen; Zahlen als Originalwert ausgeben, die keine Quelle haben.
* **Sprache im Code:** Kommentare und Docstrings auf Deutsch, **reines ASCII** (keine Umlaute, kein ß,
  kein Gedankenstrich — auch nicht in der Prüfdatei; ein einziges Nicht-ASCII-Zeichen macht sie dort
  beim Import unbrauchbar).
* **Kein tkinter, kein main-Import, keine Uhr, keine Datei.** Die Zeit wird **immer übergeben**, aller
  Zufall kommt aus einem übergebenen `random.Random(seed)` — wie in `src/botkern.py`.

## 1. Was gebaut werden soll

Ein Bot, der auf den Spieler **wie ein Gegenspieler mit Absicht** wirkt: eigene Koordinaten, eigene
Dörfer, eine von mehreren Taktiken, ein Gedächtnis und **sichtbare Vorzeichen** vor einem Angriff.
Daniels Vorgabe wörtlich:

> „Bots bekommen nicht nur feste Koordinaten, damit sie im weltbild sichtbar sind sondern auch all ihre
> gegründeten dörfer und auch sie sollen wie der spieler selbst eine von ein paar zufälligen taktiken
> nutzen um durch koordinaten näherung oder entfernung sich zu schützen oder eben anzugreifen usw“

Es gibt **keine KI** im Projekt und es soll keine werden: das Verhalten ist ein **Zustandsautomat mit
Zahlen-Schwellen**, der billig rechnet und dessen Absichten der Spieler lesen kann.

## 2. Vorlage: der vorhandene Entwurf (verbindlich in der Richtung, frei in der Zahl)

Lies **zuerst** `docs/design/SPIELSPANNUNG_UND_BOTTAKTIK_20261101.md`, Abschnitt **D** (Zustände,
Taktiken, Gedächtnis, Signale, Koordinaten, Rechenbudget) und Abschnitt **G** (Rangfolge). Dieser
Entwurf ist die Vorgabe; du setzt ihn in Code um und darfst Schwellen verbessern, wenn du es begründest.

Lies außerdem, bevor du schreibst:
* `src/botkern.py` vollständig — dort steht die **reine Logik** des heutigen Bots (`tick`,
  `wirkung_anwenden`, `naechster_angriff_moeglich`, `beute_begrenzen`, `VORSCHLAG_START_VORRAETE`,
  `BOT_NAMEN`, `SEKUNDEN_JE_TAG`). Dein Modul ist die **Ergänzung** dazu, kein Ersatz: `botkern` bleibt
  unangetastet.
* `src/auftraege.py` — `reisezeit_sekunden(entfernung, geschwindigkeit)`, `SEKUNDEN_JE_FELD`.
* `data/units.json` — Einheitenrollen und Karrenladungen.
* `src/main.py`, Klasse `BotPlayer` (etwa Zeile 185) — welche Felder ein Bot heute hat
  (`name`, `aggression`, `trading`, `army`, `vorraete`, `wall_stufe`, `wall_zustand`,
  `noob_protection`, `naechster_angriff`). **Du liest sie nur** — dein Modul bekommt ein solches Objekt
  oder ein Dict und darf es **nicht verändern**; es gibt neue Daten zurück.

## 3. Pflicht-Inhalt von `src/bottaktik.py`

1. **Kopf-Docstring**: was das Modul tut, was es NICHT tut (keine KI, keine Pfadsuche, keine Uhr),
   und woher die Schwellen kommen (`[VORSCHLAG]`, abgeleitet aus dem Entwurf).
2. **Zustände als Konstanten** (deutsch, ASCII): mindestens `SAMMELN`, `WACHSEN`, `SICHERN`, `SUCHEN`,
   `MARSCHIEREN`, `RAUBERN`, `FLIEHEN`, `RAECHEN` — plus eine Tabelle `ZUSTAENDE` mit Klartext.
3. **Taktiken** (mindestens vier) als Daten, nicht als if-Kette: je Taktik Nähe/Abstand, Schwelle zum
   Angriff, Schwelle zum Rückzug, Zielwahl, erstes sichtbares Zeichen. Eine Taktik muss sich in
   **derselben** Lage anders entscheiden als die andere — das ist die Kernforderung.
4. **Gedächtnis als eigenes Dict** je Bot (`geschlagen_von`, `beute_verloren`,
   `staerke_zuletzt`, `letzter_kontakt`) — mit Default-Werten, damit ein alter Spielstand ohne diese
   Felder weiterläuft (Rückwärtsverträglichkeit, klar dokumentiert).
5. **`dorf_positionen(bot, welt)`**: feste Koordinaten je Bot-Dorf, **deterministisch** aus
   `random.Random("nebel-bot-<name>-<n>")` — gleicher Bot, gleiche Lage, auch nach einem Neustart.
   Höchstens 3 Dörfer je Bot. Innerhalb des Rasters bleiben (Welt ist 20 x 20 Felder, `MAPS` in
   `src/main.py`).
6. **`entfernung(a, b)`**: Manhattan-Abstand, als Ersatz für die heutige Schätzung „“.
7. **`tick(bot, welt, jetzt, rng)` → `dict`**: EINE Entscheidung je Aufruf, Rückgabe mindestens
   `{"zustand", "taktik", "aktion", "ziel", "signal", "grund"}`. Aktionen: `sammeln`, `wachsen`,
   `sichern`, `suchen`, `marschieren`, `raeubern`, `fliehen`, `raechen`, `warten`.
   * `jetzt` in Spielsekunden, `welt` ein Dict mit `{"spielerdorf": {"x","y"}, "doerfer": [...],
     "bots": [...]}` — **Toleranz**: fehlende Schlüssel dürfen nicht werfen, sondern führen zu
     `warten` mit `grund`.
   * Ein Angriff darf **nur** entstehen, wenn die Taktik-Schwelle erreicht ist UND der Marsch
     (Reisezeit > 0) vorher angekündigt wurde (`signal` gesetzt). Kein Blitzangriff — außer bei der
     Taktik, die genau das als Merkmal hat (dann `signal` = `rache`).
8. **`wirkung_anwenden(bot, entscheidung, jetzt)` → neuer Bot-Zustand**: reine Funktion, Eingabe wird
   **nicht** verändert (Kopie zurück), schreibt das Gedächtnis fort (wer hat geschlagen, wie viel Beute
   weg, welche Stärke zuletzt gesehen).
9. **`anzeige(bot)` → kurze deutsche Zeile** für die Oberfläche, z. B.
   `"Pluenderer sucht Naehe (Abstand 3), naechster Marsch in 4,5 h"` — genau das, was der Spieler lesen
   soll, ohne Zahlen zu studieren.
10. **`pruefe_taktik() -> list[str]`**: Selbstprüfung ohne Fremdimport (Liste der Verstöße, leer = gut).
    Sie muss mindestens prüfen: jede Taktik entscheidet anders, Koordinaten sind stabil, kein Angriff
    ohne Signal, `tick` wirft bei fehlender `welt` nicht, `wirkung_anwenden` verändert die Eingabe nicht.

## 4. Pflicht-Inhalt von `tests/test_bottaktik.py`

Im Stil der vorhandenen Prüfungen (schau dir `tests/test_botkern.py` an: `harness`-Funktionen
`abschnitt`, `check`, `ausnahme`, `bericht`, Import über `import_src`). **Reines ASCII.** Mindestens:

* vier Taktiken entscheiden in derselben Lage unterschiedlich (konkret: gleicher Zustand, gleiche
  Koordinaten, verschiedene `aktion`) — mit den echten Namen aus `objekt`.
* Koordinaten sind deterministisch (zwei Aufrufe gleich) und je Bot verschieden.
* Entfernung ist Manhattan, nicht Kartenmitte (z. B. (1,1) zu (4,5) = 7).
* Kein `raeubern` ohne vorheriges `signal`; die Rächer-Taktik ist die einzige Ausnahme.
* Gedächtnis: nach `wirkung_anwenden` steht der Schläger drin, und der Bot wird aggressiver (Zahl
  vorher/nachher zeigen).
* Alter Spielstand ohne Gedächtnis-Felder läuft ohne Ausnahme.
* `anzeige()` liefert eine Zeile ohne Zahlenwüste (Länge prüfen, keine Ausnahme).
* Rechenbudget: 1000 Aufrufe von `tick` dauern unter einer Sekunde (mit `time.perf_counter` gemessen,
  Zahl im Bericht) — der Laptop ist schwach, das ist die eigentliche Wache.

## 5. Form und Fertig-Definition

* `src/bottaktik.py` höchstens **450 Zeilen**, `tests/test_bottaktik.py` höchstens **250 Zeilen**.
* Beide Dateien **reines ASCII** — prüfe es am Ende selbst:
  `python -c "print(all(ord(c)<128 for c in open('src/bottaktik.py',encoding='utf-8').read()))"`.
* `python -X utf8 tests/test_bottaktik.py` läuft **grün** (0 Fehler). Führe es aus und nenne die Zahl.
* `python -X utf8 -c "import sys;sys.path.insert(0,'src');import bottaktik"` läuft ohne Fehler.
* Keine Datei außer den beiden geändert: `git status --porcelain` darf nur diese zwei Zeilen zeigen
  (git nur **lesen**, nicht schreiben).
* Antworte am Ende **nur** mit: `FERTIG <Zeilen src> <Zeilen tests> <Pruefungen gruen>`.
