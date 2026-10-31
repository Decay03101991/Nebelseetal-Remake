# Code-Audit Nebelseetal Remake — Paket P5: Ordnerstruktur des ganzen Projekts

## Deine Rolle

Du bist Software-Architekt und prüfst einen gewachsenen Python-Code (tkinter-Spiel, deutsch
kommentiert, 18.400 Zeilen Prüfcode). Der Code ist über Monate **angebaut** worden: neue Funktionen
kamen dazu, alte blieben, Doppelungen wurden nie zusammengeführt. Deine Aufgabe ist **nicht**,
Eleganz zu predigen, sondern konkrete, umsetzbare Zusammenführungen zu benennen.

## Harte Regeln (daran wird deine Antwort gemessen)

1. **Das Spiel bleibt unser Spiel.** Kein Verhalten darf sich ändern: keine anderen Zahlen, keine
   anderen Regeln, keine andere Bedienung. Reine Struktur- und Lesbarkeitsarbeit.
2. **Jede Funktion bleibt erhalten**, solange sie aufgerufen wird. Was niemand aufruft, nennst du
   ausdrücklich als „entfernbar" mit Begründung.
3. **Der Prüfcode ist der Beweis.** Zu jedem Vorschlag gehört: welche vorhandene Prüfdatei
   (tests/*.py) muss danach grün bleiben? Wenn keine existiert, sagst du das offen.
4. **Deutsch, ASCII in Code-Kommentaren** (das Projekt hält `src/botkern.py` bewusst ASCII).
5. **Keine erfundenen Zeilenzahlen.** Wenn du eine Ersparnis schätzt, schreib „geschätzt".

## Was das Projekt über sich sagt (gemessen, nicht geschätzt)

* `src/`: 49 Dateien, 21.703 Zeilen, 17.406 Codezeilen, 904 Funktionen/Methoden.
* `main.py` allein: 7.375 Zeilen, 240 Methoden, davon 27 `_render_*`-Methoden.
* Funktionen ab 60 Zeilen: 47 (längste 205 Zeilen, `_render_settlement_map`).
* 58 Sechs-Zeilen-Blöcke stehen mehrfach identisch im Code.
* `kampf.py` (398 Z.) und `kampf_alt_handbuch_2009.py` (401 Z.) enthalten je eine
  `fuehre_schlacht` (188 bzw. 194 Zeilen) — `kampf.py` importiert die alte Fassung.
* Oberfläche: tkinter, alles in einer Klasse; Ansichten `_render_*`, Aufbau `_build_main_ui`.
* Prüfcode: `tests/` 18.418 Zeilen, 98 Dateien, Aufruf über `tools/sammellauf.py`.

## Deine Aufgabe

Entwirf aus der Modulliste die Zielstruktur für `src/`, `tests/` und `tools/`: welche Themenordner, welche Datei wohin, wie bleiben Importe, PyInstaller-Build (`tools/build_exe.py`) und die 98 Prüfdateien intakt? Nenne die Umzugsreihenfolge in Schritten, sodass nach **jedem** Schritt alles noch läuft. Bevorzuge flache, sprechende Namen gegenüber tiefer Verschachtelung.

## Der Code

### Modulliste

```
src/admin_oberflaeche.py                 191 Zeilen
src/admin_teststand.py                   125 Zeilen
src/admin_werkzeuge.py                   246 Zeilen
src/auftraege.py                         638 Zeilen
src/ausgabemodus.py                       11 Zeilen
src/ausruestung.py                       273 Zeilen
src/baumenue_info.py                     133 Zeilen
src/berater.py                           374 Zeilen
src/bonus_system.py                      169 Zeilen
src/bot_angriffsplanung.py               108 Zeilen
src/botkern.py                           622 Zeilen
src/dorfwall.py                          125 Zeilen
src/einheiten.py                         206 Zeilen
src/fehlbestand.py                       140 Zeilen
src/forschung.py                         232 Zeilen
src/forschung_wirkung.py                 177 Zeilen
src/forschungspfad.py                    350 Zeilen
src/gebaeude_wirkung.py                  344 Zeilen
src/gelaende.py                          233 Zeilen
src/gildenrangliste_original.py           48 Zeilen
src/gpt_versorgungsdiagnose.py           126 Zeilen
src/kampf.py                             398 Zeilen
src/kampf_alt_handbuch_2009.py           401 Zeilen
src/kampfbericht.py                      492 Zeilen
src/karten_optik.py                      599 Zeilen
src/karten_optik_fein.py                 863 Zeilen
src/main.py                             7375 Zeilen
src/oberflaeche_original.py              185 Zeilen
src/originalkarten.py                    128 Zeilen
src/originalkarten_grafik.py              36 Zeilen
src/portalraum.py                        216 Zeilen
src/public_start.py                       20 Zeilen
src/punkte.py                            456 Zeilen
src/speichern.py                         338 Zeilen
src/spieldaten.py                        229 Zeilen
src/spielerhilfe.py                      176 Zeilen
src/spieloekonomie.py                   1072 Zeilen
src/spielschicht.py                      664 Zeilen
src/spielstaende.py                       52 Zeilen
src/spielstand_archiv.py                 162 Zeilen
src/spielzeit.py                         169 Zeilen
src/tor.py                               231 Zeilen
src/versorgungsschutz.py                 160 Zeilen
src/welt.py                              135 Zeilen
src/welt_optik.py                        600 Zeilen
src/welt_optik_fein.py                   898 Zeilen
src/werkstatt.py                         422 Zeilen
src/wirtschaft.py                        252 Zeilen
src/zeitbasis.py                         103 Zeilen
```


## Ausgabeformat (genau so, nichts anderes)

### 1. Befund in fünf Sätzen
Was ist hier wirklich das Problem — mit Zahlen aus dem Code.

### 2. Vorschläge (Tabelle, absteigend nach Nutzen)

| # | Was | Dateien/Funktionen | Zeilen vorher → nachher | Risiko (klein/mittel/groß) | Beweis: welche Prüfdatei | Reihenfolge |
|---|---|---|---|---|---|---|

### 3. Zusammenführung im Detail
Für die zwei wichtigsten Vorschläge: welche Funktionen verschmelzen zu welcher neuen Funktion,
welche Parameter, welcher Rückgabewert, was passiert mit Sonderfällen. Kein vollständiger Code —
nur Signatur plus drei bis fünf Zeilen Kern.

### 4. Was du NICHT anfassen würdest
Und warum. (Beispiel: Zeichencode der Oberfläche, der auf Pixel wirkt.)

### 5. Ordnung
Wie sähe eine saubere Ordner-/Dateistruktur für diesen Teil aus? Namen der Dateien, was in welche
gehört, und **in welcher Reihenfolge man umzieht, ohne dass Importe brechen**.
