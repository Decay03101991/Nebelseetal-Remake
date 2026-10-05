# Entwicklungsprotokoll — Nebelseetal Remake

**Wozu:** Daniel schreibt das Entstehen des Spiels mit. Kurz und mit Beleg: die wichtigsten
Schritte und ihre Kennungen — kein Tagebuch.

**Regeln für dieses Protokoll:**
- Nach jedem groben Schritt eine Zeile — immer hinten anhängen.
- Genau eine Zeile je grobem Schritt (das hält es übersichtlich).
- Fehler und Irrwege gehören hinein.
- Sicherungen stehen nicht hier (die gehören nach `docs/SICHERUNGEN.md`).
- Kosten nur gemessen, nie geschätzt.
- Zielgröße: deutlich unter 320 Zeilen. Wird sie überschritten, wird verdichtet — vorher die
  unveränderte Fassung sichern und committen.

**Nichts ist gelöscht.** Die vollständigen Fassungen liegen im Projekt und in git:
`docs/ENTWICKLUNGSPROTOKOLL_VOLLFASSUNG_2026-10-05_0820.md` (320 Zeilen) und
`docs/ENTWICKLUNGSPROTOKOLL_VOR_VERDICHTUNG_2026-10-05.md` (462 Zeilen).
Diese Kurzfassung entstand am 05.10.2026 auf Vorgabe Daniel: „nur noch übersichtlich die
wichtigsten Punkte, der Rest fliegt raus".

## Vorgeschichte (vor dem 04.10.2026)

Ein älterer Build (`Nebelsee Memory.exe`, 27.08.2026) liegt in der Quarantäne. Am 04./05.10.2026
wurde das Spiel neu auf das **Original-Handbuch 2009** gestellt. Richtschnur: alles stammt aus dem
Handbuch oder aus belegten Quellen — fehlt ein Wert, wird er **null** gesetzt und begründet,
nichts wird geschätzt.

## 04.10.2026 — Tag 1: vom Rohbau zum Handbuchspiel

| Zeit | Schritt | Ergebnis / Belege |
|---|---|---|
| 14:51–15:36 | Sicherheitsnetz, Datengrundlagen, 28 Originaleinheiten, Datenschicht, W1d+W2, W4a | Prüfstand **526 bestanden** / 11 Dateien, 0 Fehler · Baupreise auf die belegten Werte korrigiert (`4b84544`) |
| 19:13–19:38 | Icons aufbereitet und im Spiel, alter EXE-Build in die Quarantäne, Inhalt rollbar | genau **eine** EXE im Projekt |
| 19:44–19:58 | Regelgutachten `gpt-6-astra`: Kampf gegen das Handbuch, Konformitäts-Audit über 24 Seiten | fand meinen Fehler „10 statt 7 Tage Götterschutz" |
| 20:06–20:51 | Wirtschafts-Entwurf, Gelände + Siedlungskarten (5 Kartentypen), Siedlungsansicht im Fenster | Preisentwurf **widerlegt**, Rest brauchbar |
| 21:14–21:33 | Auskunft (Reiter „Chat"), Auftrags-/Bot-Entwurf, drei neue Module, Modelldaten gesichert, Bildsuche **abgeschlossen** (vier Wege, alle negativ) | 908 KB Belege in `docs/audits/` |
| 21:35–21:50 | Arbeitssystem, Nachlese (`docs/LEHREN.md`), **W4b-4** Kartenerträge angebunden | `472704f` — 526 Prüfungen grün |
| 22:05–22:15 | **W4b-5**: die 20 Originalgebäude wirken aus den Siedlungskarten | `a158175` — **630 bestanden**, 0 Fehler, 1 Befund |
| 22:24–22:34 | **Passworttor** (Schritt 8) + Bau-Skript für die `.exe`, Doppelstart-Fund behoben | `8a6bd87` — **691 bestanden** / 13 Dateien |
| 22:35–23:10 | Erste `.exe` (Startprüfung erst **rot**, dann grün), fünf Kind-Module, **W4b-6** | `c0f4a5d` — **1157 bestanden** / 18 Dateien, 2 Befunde |
| 23:10–23:35 | Dritte Kinder-Welle, alle zehn Module nachgerechnet, Brett der Kinder wieder entfernt | `f48e9d2` — **1651 bestanden** / 23 Dateien, 9 Befunde |
| 23:35–23:50 | Gezielte teure Aufrufe statt Agentenschleifen: `gpt-6-astra` (Bilder), `deepseek-v4-pro` (Plan) | teure Aufrufe zusammen **+0,79 USD** |
| 23:47 | Sitzungswechsel: Stand, Belege, der EINE nächste Schritt (`speichern` einhängen) | `3ec1fca` |

## 05.10.2026 — Tag 2: Module einhängen, Spielbarkeit, Oberfläche

| Zeit | Schritt | Ergebnis / Belege |
|---|---|---|
| 23:49–00:29 | **W8 Speichern** (`9ec34fb`), **W6 Punkte** und **W2/W2b Kampf** eingehängt, je mit eigener Nachprüfung | `b14f7f5` — **1734/0/14** über 25 Dateien |
| 00:00–00:29 | Einzeltests der Kind-Module: speichern **95 bestanden** (5 Befunde: **95/0/5**) · baseline **40/0/0** · gui_fehler **22/0/1** · auftraege **111 bestanden** (**111/0/1**) · punkte **76/0/0** · w8_einhaengung **39/0/5** · punkte_einhaengung **44/0/0** · kampf_einhaengung **42/0/0** | Sammellauf **1651/0/9** |
| 00:03–00:41 | **W5-2 Portalraum**, **W3 Werkstatt + 17 Originalwaren** eingehängt, Verdrahtungs- und GUI-Fehler-Prüfung aufgenommen | `a1f224a` — **1798 bestanden** / 27 Dateien (**1798/0/15**) |
| 01:15–02:16 | Auftragssystem fertig (Kern + Oberfläche), Durchspiel-Prüfung fand einen **echten** Fehler (Einheiten wurden nie gespeichert), Kampfsimulator auf das echte Schlachtmodell | `697ab1b` · durchspiel **36/0/1**, dann **48/0/2** · gebaeude_wirkung **104/0/1** |
| 02:24–02:45 | Aufträge kämpfen am Ziel, Kampfbericht nennt das Ziel, `tools/zieluebergabe.py`, Ladeansicht mit Titelbild, Symbol aus dem Nebelsee-Bild | **1799/0/15**, **1776 bestanden**, **1835/0/16**, **1847/0/17**, **1873/0/17**, **1892/0/18**, **1912/0/19**; Symbol in sechs Größen **16/32/48/64/128/256** (die alte braune Wappenfarbe war **65/31/13**, die beigelegte Datei war ein GIF) |
| 02:47–03:00 | Protokoll verdichtet (462 → 302 Zeilen); die Verlustprüfung fand einen **echten Verlust** und behob ihn | `9e2a1e4` (Vor-Fassung aufbewahrt), `dece98b` |
| 06:06–06:28 | Sitzung sauber übergeben: Zielregister beendet, Kanban-Karten archiviert, Übergabe nachgezogen, neues Ziel gesetzt | `32152e1`, `15a8cff`, `dece98b` |
| 06:41 | **Der schwerste Fund:** „spielbar ist gar nichts" — eine fehlende Neuzeichnung blockierte das ganze Spiel; dazu plünderten die Bots am Tag 1 im Noobschutz **70 Holz + 70 Stein** | `3688912` — **1959/0/20** über 33 Dateien |
| 07:04 | **Benutzerführung und Karten** nach dem Bildgutachten von `gpt-6-astra`: Aufgabenkarte, Siedlungskarte als Zeichenfläche, Weltkarte ohne Konfetti | `c80154a`, `2a2b0a1` — **1967/0/19** über 33 Dateien |
| 07:14 | Protokoll auf Ihre Vorgabe hin gekürzt; die vollständige Fassung (320 Zeilen) aufbewahrt und committet | `6cf1920` |

**Eigene Korrektur, mit `git log` belegt:** die drei Zeilen zu Schritt 21/22 und zur Kürzung standen
zuerst mit **geschätzten** Zeiten (07:05, 08:20, 08:45). Die echten Commit-Zeiten sind **06:41**,
**07:04** und **07:14** — ich hatte vor dem Schreiben nicht `date` gefragt. Zeiten werden ab jetzt
immer mit `date` (oder `git log --format=%ci`) geholt, nie aus dem Gefühl geschrieben.

## Kennungen (alle Commits, die dieses Protokoll nennt)

`0206e8a` Protokoll · `3ec1fca` Sitzungswechsel · `472704f` W4b-4 · `4bf6a45` Sicherungszeile ·
`5f7ee39` Sicherungen ausgelagert · `697ab1b` Kampfsimulator · `8a6bd87` Passworttor ·
`9ec34fb` W8 Speichern · `a158175` W4b-5 · `a1f224a` W3 Werkstatt · `b14f7f5` W6+W2 ·
`c0f4a5d` W4b-6 · `c329893` Protokoll · `f48e9d2` zehn Kind-Module nachgerechnet ·
`9e2a1e4` Vor-Fassung aufbewahrt · `dece98b` Protokoll verdichtet · `32152e1` Übergabe 06:08 ·
`15a8cff` Übergabe + Skill · `26766d6` Übergabe übernommen · `3688912` Spielbarkeit ·
`c80154a` Benutzerführung · `2a2b0a1` Nachprüfung + EXE · `6cf1920` Vollfassung aufbewahrt.

## Kosten (nur gemessen)

| Zeitraum | Modelle | Betrag |
|---|---|---|
| 04.10. abends (Astra-Bilder, v4-pro) | `gpt-6-astra`, `deepseek-v4-pro` | **+0,79 USD** für beide teuren Aufrufe zusammen |
| 05.10. 00:00–01:24 | `deepseek-v4-flash` (Koordinator) + `flash`-Unteragenten | Sitzung **0,8362 USD = 0,7449 EUR** |
| 05.10. ab 00:00 (Messung 03:00) | alles `deepseek-v4-flash` | Tag **1,0378 USD ≈ 0,925 EUR** |
| 05.10. ab 00:00 (Messung 07:0x) | `flash` + zwei Bildaufrufe an `gpt-6-astra` | Tag **1,4593 EUR** |

**Regel:** nur belegte Beträge, gemessen mit `scripts/tageskosten_check.py --json` (summiert über
alle Profile). Der Schlüssel des Agenten liegt nur in Hermes, deshalb werden Kontostände von
Daniel abgelesen. **Lehre:** bei `gpt-6-astra` sind die Cache-Schreibkosten der größte Posten —
Aufträge kurz halten. Die 4-EUR-Tagesregel gilt; für den Auftrag „Nebelseetal Remake" hat Daniel
sie ausgesetzt.

## Offen (Stand 05.10.2026)

- **Abnahme „fehlerfrei spielbar"** — die Partie mit Daniels Passwort. Das Tor passiert nur er,
  nie der Agent.
- **Drei belegte Handbuch-Lücken** (jede braucht eine Zahl von Daniel): Mana je Siedlung statt
  eines gemeinsamen Vorrats · Materialkosten der Werkstätten · **Sieg-/Niederlagebedingung**
  (das Handbuch nennt keine).
- **Weltkarte**: der mittlere Umbau ist drin (Farben, Legende, „Hier", kein Namensrauschen);
  Zoomstufen, Scrollbalken und Detailpanel stehen noch aus.
- Der **Erlös beim Handeln** ist weiterhin ein VORSCHLAG (das Handbuch nennt keinen Warenpreis).
- **Arbeitsweise, die sich bewährt hat:** erst prüfen, was wirklich läuft (nicht, was im Ordner
  liegt) · nie schätzen — fehlt ein Wert, `null` plus Begründung · jede Modell- und Kind-Antwort
  nachrechnen · Unteragenten arbeiten nur an neuen Dateien mit eigener Prüfdatei und führen kein
  eigenes Brett · Agent-zu-Agent Englisch/ASCII, alles für Daniel Deutsch · kleine Commits.

| 10:42 | **23 · Sitzungswechsel: Übergabe neu geschrieben und einen eigenen Zeitfehler korrigiert** | Abschnitt 0 und 0c in `docs/PROJEKT_STAND.md` neu gefasst: Stand in Belegen, der EINE nächste Schritt (**Weltkarte nach der astra-Vorgabe**), das Kontext-Paket und die Startzeile zum Kopieren. **Zielregister geprüft:** kein fremdes aktives Ziel, kein Spielprozess offen — und das eigene Ziel hat der **Zielrichter auf `done` gesetzt** (1/20 Takte), es läuft also nichts von selbst weiter; eine neue Sitzung setzt ein **neues** Ziel. **Eigener Fehler, gefunden und behoben:** drei Zeilen dieses Protokolls standen mit **geschätzten** Uhrzeiten (07:05 / 08:20 / 08:45), die echten Commit-Zeiten sind **06:41 / 07:04 / 07:14** — korrigiert und als Korrektur gekennzeichnet. Belege: Prüfstand **1967/0/19** über 33 Dateien · `.exe` 14.464.338 Byte, SHA256 `58cd48e9…`, aus einem anderen Ordner startgeprüft · Arbeitsverzeichnis sauber. |
| 11:23 | **24 · Weltkarte nach der astra-Vorgabe (A3) umgebaut · zwei Kinder-Module für feinere Karten nachgerechnet** | `src/main.py`: Zeichenfläche mit **48 px je Feld** in eigenen waagerechten und senkrechten Scrollbalken, Zoomstufen „− 100 % +" (16–96 px), kleine Übersichtskarte mit Ausschnittsrechteck, festes Detailpanel (Ort · Koordinate / Gelände / Status / Gebäude / Aktion), Gebietsleiste **oben** mit ausdrücklich benannten gesperrten Gebieten („Nebelwald – gesperrt", „Zum Portal" / „Zur Forschung"), Fahne „Hier", 9 Regionsnamen einmal groß — und der Klick **wählt nur noch aus** (vorher erforschte und erledigte er still: Ruf +15, Gold +20, Aufgabe, Truppenbewegung). **Fund beim Prüfen:** die Zeichenfläche wuchs auf Fensterbreite, dadurch waren die Scrollbalken wirkungslos; behoben. Neue Prüfdatei `tests/test_weltkarte.py` **58/0/0**. Kinder (je eine neue Datei + eigene Prüfdatei): `src/karten_optik.py` **54/0/0** und `src/welt_optik.py` **70/0/0** — vom Koordinator mit **eigenem** Verfahren nachgerechnet (**0 Fehler**: Randtreue bei 32/48/64/96 px, Determinismus, keine Emoji, kein tkinter-Import, kein Zufall). **Sammellauf: 2023 bestanden, 0 Fehler, 21 Befunde über 34 Dateien** (vorher 1967/0/19 über 33); die zwei zusätzlichen Befunde sind ehrliche Hinweise, keine Fehler (in 25 Bot-Zügen kam kein Angriff vor · Absatz-Anfänge der Protokoll-Vor-Fassung). Die beiden Module sind gebaut und geprüft, aber **noch nicht eingehängt**. Kosten: nur `deepseek-v4-flash`, kein teures Modell. |
| 12:00 | **25 · Feinkarten-Module eingehängt · Hausausbau bis Stufe 4 · astra- und v4-pro-Gutachten gesichert** | `src/main.py`: die Siedlungskarte zeichnet mit `src/karten_optik.py` (7 Gelände-Embleme, Gebäudezeichen mit Stufenpips, **Wege** zwischen benachbarten Feldern — in drei Durchgängen, damit die Wege unter den Gebäuden liegen), die Weltkarte mit `src/welt_optik.py` (feinere Geländemalerei, Fahne, Auswahl, 400-Kachel-Übersicht). Die drei alten Zeichenroutinen `_gelaende_emblem`, `_gebaeude_zeichen` und `_welt_gelaende_zeichen` sind **entfernt** — keine zweite Wahrheit für dieselbe Zeichnung. Nach dem zweiten **astra**-Gutachten (`docs/audits/ux_astra_karten_feinheit_2026-10-05.txt`, aus zwei echten Aufnahmen): **Ortsnamen stehen nicht mehr auf jedem Feld** (nur noch im Detailpanel) und ein Rohstofffeld heißt **„Vorkommen"** statt „Gebäude". **Hausausbau** auf Vorgabe Daniel: `data/gebaeude_wirkung.json` + `src/gebaeude_wirkung.py` — Haus bis **Stufe 4**, je Stufe **+5 Siedler** (Stufe 1 = das belegte Haus; alte Spielstände zählen jedes Haus als Stufe 1). Vier Kinder-Module gebaut und vom Koordinator nachgerechnet, **noch nicht eingehängt**: `src/ausruestung.py`, `src/forschungspfad.py`, `src/karten_optik_fein.py`, `src/welt_optik_fein.py`. Belege: `tests/test_weltkarte.py` **60/0/0** · `tests/test_gebaeude_wirkung.py` **107/0/1** · Sammellauf **2150 bestanden, 0 Fehler, 20 Befunde über 36 Dateien** (dieser Lauf entstand VOR der Haus-Änderung). Entwurf von `deepseek-v4-pro` zu Ausrüstungskette, Forschung und Hausausbau: `docs/audits/entwurf_ausruestung_forschung_haus_2026-10-05.txt`. |
| 12:22 | **26 · Ausrüstungskette, Forschungssperren und Hausausbau eingehängt · vier Kinder-Module nachgerechnet** | `src/main.py`: `_train_unit` prüft jetzt **beides** aus `data/units.json` — die **Forschungsstufe** (Kämpfer 1 · Krieger 3 · Ritter 7 · Paladin 10 · Gauner Heimlichkeit 1 · Karren und Belagerungswaffen Wagenbau 1–10) **und die Ausrüstung** (14 der 28 Einheiten brauchen Waren; Krieger: Schwert + Kettenhemd · Paladin: Zweihänder + Schwert + Magischer Paladinharnisch). Vorher war KEINE der beiden Bedingungen im Spiel wirksam — genau Daniels Befund. Die Waren werden beim Erteilen des Auftrags verbraucht (Entwurf: „Auftrag erteilen setzt vorhandene Mittel voraus"); der Ausbilden-Knopf ist gesperrt und nennt das Fehlende mit Soll/Ist (eine Quelle: `main._ausbildungs_hindernis` + `src/ausruestung.py`). `_start_research` erzwingt die Voraussetzungen aus `data/research.json` (z. B. Waffentechnik = Bibliothek 3 + Schmiedekunst 1); die Forschungsansicht zeigt je Eintrag „schaltet frei — Waren/Einheiten" bzw. „gesperrt: <Grund mit Soll/Ist>" (`src/forschungspfad.py`). **Hausausbau bis Stufe 4** (je +5 Siedler; Stufe 1 = das belegte Haus). Vier Kinder-Module gebaut und vom Koordinator mit **eigenem** Verfahren gegen die Datendateien nachgerechnet (**0 Fehler**): `ausruestung` **68/0/1**, `forschungspfad` **123/0/0**, `karten_optik_fein` **80/0/0**, `welt_optik_fein` **128/0/0**. Zwei Prüfdateien mussten ihre alte Annahme aufgeben („mit Akademie wird ein Krieger ausgebildet" → jetzt: ohne Forschung/Ausrüstung abgelehnt, mit beidem ausgebildet und die Waren verbraucht). **Sammellauf: 2559 bestanden, 0 Fehler, 21 Befunde über 40 Dateien.** Kosten: `deepseek-v4-pro` (Entwurf) und `gpt-6-astra` (zwei echte Bildaufnahmen). |
| 13:26 | **27 · Geländeregeln für ALLE 20 Gebäude** | Vorgabe Daniel („ein gebäude hat im sumpf nichts verloren als regel … zum beispiel" / „intelligent angewendet auf alle gebäude"). **Gemessen zuerst:** die Sumpfregel gilt schon für jedes Gebäude; belegt geregelt waren auch Holzfäller (Steppe/Wald), Steinmetz, Erz- und Goldmine (Hügel/Berg), die vier Zuchten (Grasland/Steppe), Jäger (Steppe/Wald), Bibliothek (Grasland/Steppe/Nebelsee) und Tempel (überall außer Sumpf) — **ohne jede Regel waren 9 Gebäude**: Haus, Lager, Schmiede, Bogenbauer, Nähstube, Kriegerakademie, Diebesgilde, Stellmacher, Verteidigungswall (mein eigener Testaufbau hatte ein Haus mitten in den Nebelsee gesetzt, nichts hinderte ihn). Jetzt in `data/buildings.json` als **VORSCHLAG** gesetzt und in der Datei gekennzeichnet: Haus/Lager/Bogenbauer/Stellmacher Grasland+Steppe+Wald+Hügel · Schmiede zusätzlich Berg (Erz) · Nähstube Grasland+Steppe+Wald (Wolle, Leder, Felle) · Kriegerakademie Grasland+Steppe+Hügel · Diebesgilde Grasland+Steppe+Wald · Wall alles außer Nebelsee/Sumpf. **Folge: im Nebelsee stehen nur noch Bibliothek und Tempel — beide belegt.** Neue Prüfungen in `tests/test_gelaende.py` (u. a. „im Nebelsee dürfen nur Bibliothek und Tempel stehen"). **Fünf Prüfdateien mussten ihre alte Annahme aufgeben** (`test_gelaende`, `test_kartenansicht`, `test_gebaeude_wirkung`, `test_spielschicht` — sie bauten Schmiede, Akademie, Gilde und Wall auf beliebigen Feldern; `test_kartenansicht` prüft jetzt beide Richtungen: im Wald **nicht** angeboten, auf Grasland **schon**). **Sammellauf: 2565 bestanden, 0 Fehler, 21 Befunde über 40 Dateien.** Ein Fund am Rande: `test_baseline` schlug als ERSTE Datei des Sammellaufs zweimal mit leerer Ausgabe fehl (Rückgabe 1), während parallel das laufende Spiel offen war — allein und im sauberen Lauf **40/0/0**; also Umgebung, kein Codefehler. Offene Entscheidung für Daniel: die neun Vorschlagsregeln bestätigen oder ändern (eine Zeile in `data/buildings.json` genügt). |
| 13:39 | **28 · Zeitfaktor, sichtbarer Rohstoffeingang und Aufgabenkarte gegen das Festbauen** (Daniels Spielbericht) | Daniels Bericht, wörtlich: „statt eine kriegerakademie zu bauen habe ich willkürlich viele andere gebäude ohne regelung bauen können und hatte am ende keine rohstoffe für wichtige gebäude. So kann es passieren das man kein holz mehr bekommt weil man keine holzfäller gebaut hatte. auserdem sehe ich keinen regelmäßigen rohstoffeingang oben" — **zwei belegte Ursachen gefunden.** **(1) Die Spieluhr lief im Originaltempo:** `GameState.tick(dt_seconds)` rechnete `dt_h = dt_seconds / 3600`, also eine Echtzeitsekunde = eine Spielsekunde. Ein Holzfäller auf Wald („4 Holz/Stunde") lieferte damit **4 Holz in einer echten Stunde**; bei der Rundung des Kerns auf zwei Stellen zeigte die Kopfzeile nach einer Sekunde sogar **0,00 Holz** — genau der Eindruck „kein Eingang". Neu: `src/spielzeit.py` + `data/spielzeit.json` mit dem **Zeitfaktor** (Vorschlag ×180 = 1 Spielstunde in 20 Sekunden; Originaltempo 1× bleibt wählbar). **Die Handbuchformeln bleiben unangetastet** — nur die Spieluhr läuft schneller (genau der Weg, den `docs/ENTWURF_WIRTSCHAFT.md` und `docs/PLAN_AUS_HANDBUCH.md` beschreiben, dort ausdrücklich als Daniels Entscheidung vermerkt). Der Faktor wird an EINER Stelle angewandt (`_tick_loop`), Wegezeiten rechnen mit (`spielzeit.echtzeit_fuer_spielstunden`); in den **Einstellungen** ist er umstellbar (×1/×20/×60/×180/×600), in der Kopfzeile steht „Tempo ×180 · 1 Std = 20 s". **(2) Ohne Rohstoffquelle gab es keine Warnung:** die Aufgabenkarte führt jetzt **vor** dem Forschen zum fehlenden Erzeuger, mit Feld und Preis — „Ohne Holz-Quelle geht es nicht weiter: es ist kein Holz da und es wächst keines nach. Baue einen Holzfäller — auf Wald 4 Holz/h, auf Steppe 2 (Kosten: …)". Ebenso für Stein (Steinmetz) und Nahrung (Farm). **In der Kopfzeile steht bei einem Kernrohstoff ohne Erzeuger jetzt „⚠"** statt einer irreführenden „(0)". Neue Prüfdatei `tests/test_spielzeit.py` **24/0/0** (u. a. „im Originaltempo rundet EINE echte Sekunde auf 0,00 Holz — genau der Befund Daniels" und „20 echte Sekunden bei ×180 sind eine Spielstunde — genau 4 Holz"); `tests/test_startspiel.py` von 37 auf **46/0/0** erweitert (Karte nennt den fehlenden Erzeuger, Warnung in der Kopfzeile erscheint und verschwindet mit dem Holzfäller). **Sammellauf: 2599 bestanden, 0 Fehler, 21 Befunde über 41 Dateien.** |
