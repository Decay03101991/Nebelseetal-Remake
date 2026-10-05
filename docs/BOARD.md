# Tagebuch des Koordinators

**Zweck:** Dies ist **Daniels** Brett. Der Hauptagent (Koordinator) trägt hier zusammen, was die
Unteragenten geliefert haben — mit **echten** Prüfzahlen. Es ist **kein** Brett der Kinder mehr:
die Kinder sprechen nicht untereinander und führen kein eigenes Brett (Vorgabe Daniel, 04.10.2026).

**Warum kein Brett der Kinder:** Ein Kinder-Brett ist eine zweite Wahrheit — ein Kind kann dort
„fertig" melden, während seine eigene Prüfdatei rot ist (genau so passiert am 04.10.2026:
`oberflaeche_original` 63 grün / 1 rot; gefunden hat es der Koordinator, nicht das Brett).
Verbindlich sind allein `run_tests.bat`, die Commits und die Übergabe.

**Regeln (kurz):**

1. Der Koordinator trägt ein, was er **selbst nachgeprüft** hat.
2. Jede Zeile braucht eine echte Prüfzahl oder einen Commit.
3. **Nur anhängen.** Fremde Einträge werden nicht geändert.
4. Kurz halten: zwei Zeilen reichen.

Format einer Zeile: `Zeit | Agent | Dateien | Ergebnis | Prüfung`

---

## Laufende Ansprüche

*Zurzeit keine — alle Kinder sind beendet, alle Dateien sind frei.*

## Abgeschlossene Arbeiten (neueste zuerst)

| Zeit | Agent | Dateien | Ergebnis | Prüfung |
|---|---|---|---|---|
| 13:33 | kind-pruefer (Geländeregeln) | — (nur lesend, nichts geändert/committet) | **Unabhängige Gegenprüfung der Geländeregeln (Schritt 27):** 6 Prüfsteine, **0 Abweichungen**. 20 Gebäude × 7 Gelände = 140 Paare, kein leeres Ergebnis, Sumpf 0× erlaubt; die 11 belegten Regeln exakt unangetastet (u. a. Tempel = alles außer Sumpf); auf Nebelsee genau Bibliothek und Tempel; alle 9 Vorschlagsregeln wie beschrieben; gültiges JSON mit Vorschlagsblöcken; **Alt-Spielstände bleiben ladbar** (dynamisch geprüft: Haus auf Berg im Spielstand → `load()` ohne Ausnahme). Klarstellung des Prüfers: „Schmiede zusätzlich Berg" heißt **ohne Wald** — deckt sich mit `tests/test_gelaende.py:69` | eigener Nachbau des Kindes gegen die Datei + vollständiger Lauf `test_gelaende` **86/0/0** |
| 13:39 | Hauptagent | `src/spielzeit.py` (neu), `data/spielzeit.json` (neu), `src/main.py`, `tests/test_spielzeit.py` (neu), `tests/test_startspiel.py`, `run_tests.bat` | **Daniels Spielbericht abgearbeitet (Vorrang).** Zwei belegte Ursachen: **(1)** die Spieluhr lief im Originaltempo (1 Echtzeitsekunde = 1 Spielsekunde) — ein Holzfäller lieferte 4 Holz je **echter** Stunde, nach einer Sekunde rundete der Kern auf 0,00 → „kein regelmäßiger Rohstoffeingang". Neu: **Zeitfaktor** (`data/spielzeit.json`, Vorschlag ×180 = 1 Spielstunde in 20 s), die Handbuchformeln bleiben unangetastet, nur die Spieluhr läuft schneller; an EINER Stelle angewandt (`_tick_loop`), Wegezeiten rechnen mit, in den **Einstellungen** umstellbar, Kopfzeile zeigt „Tempo ×180". **(2)** Ohne Erzeuger gab es keine Warnung: die **Aufgabenkarte** nennt jetzt vor dem Forschen den fehlenden Erzeuger mit Feld und Preis (Holz → Holzfäller auf Wald/Steppe · Stein → Steinmetz auf Berg/Hügel · Nahrung → Farm auf Grasland/Steppe), die **Kopfzeile** zeigt „⚠" statt einer irreführenden „(0)" | `test_spielzeit` **24/0/0** (neu) · `test_startspiel` **46/0/0** (37 + 9 neue) · `test_baseline` 40/0/0 · **Sammellauf 2599/0/21 über 41 Dateien** |
| 13:26 | Hauptagent | `data/buildings.json`, `tests/test_gelaende.py`, `tests/test_kartenansicht.py`, `tests/test_gebaeude_wirkung.py`, `tests/test_spielschicht.py` | **Geländeregeln für alle 20 Gebäude** (Vorgabe Daniel: „ein gebäude hat im sumpf nichts verloren als regel … intelligent angewendet auf alle gebäude"). Vorher gemessen: Sumpf für alle gesperrt (galt schon), Produktionsgebäude über die Handbuch-Erträge geregelt — **9 Gebäude ohne jede Regel** (Haus, Lager, Schmiede, Bogenbauer, Nähstube, Kriegerakademie, Diebesgilde, Stellmacher, Wall). Jetzt je Gebäude eine begründete Eignung, im Datenblatt als **Vorschlag** gekennzeichnet; Nebelsee nur noch Bibliothek und Tempel. Vier Prüfdateien zogen ihre alten Annahmen nach | `test_gelaende` **86/0/0** (neu: jedes Gebäude gibt auf jedem Gelände eine Begründung · Nebelsee nur Bibliothek und Tempel) · `test_kartenansicht` 42/0/0 · `test_gebaeude_wirkung` 113/0/1 · `test_spielschicht` 133/0/1 · **Sammellauf 2565/0/21 über 40 Dateien** |
| 12:35 | kind-pruefer (A3) | — (nur lesend) | **Unabhängige Nachprüfung des Weltkarten-Umbaus** gegen das astra-Gutachten A3: Satz für Satz ERFÜLLT (Titel, gedämpfte Farben, 48 px, beide Scrollbalken, Zoom, Regionsnamen, Übersicht, Fahne, Detailpanel, Auswahlklick, Gebietsleiste). **Zwei Abweichungen gefunden und behoben:** (1) „Stationieren" stand auch im Gebiets-Panel — jetzt ausdrücklich „Einheiten auf dieses Gebiet stationieren" (das astra-Verbot gilt für den ausgewählten Ort); (2) das gesperrte Gebiet nannte keine Stufe — jetzt „Vermessung auf Stufe 1, dafür eine Bibliothek" | eigener Testlauf des Kindes: `test_weltkarte` 58/0/0 nachgestellt; `karten_optik` 54/0/0, `welt_optik` 70/0/0 bestätigt |
| 12:22 | Hauptagent | `src/main.py`, `run_tests.bat`, `tests/test_gui_fehler.py`, `tests/test_gebaeude_wirkung.py` | **Ausrüstungskette und Forschungssperren eingehängt** (Daniels Befund): Ausbildung verlangt Forschungsstufe UND Waren, Waren werden verbraucht; Forschung verlangt ihre Voraussetzungen; Ansichten zeigen Grund und Freischaltung | Sammellauf **2559/0/21** über **40 Dateien** · `test_gebaeude_wirkung` 113/0/1 · `test_gui_fehler` 23/0/1 |
| 12:2x | Koordinator | `src/ausruestung.py`, `src/forschungspfad.py` | Kinder-Module mit **eigenem** Verfahren gegen `data/units.json`, `data/items.json` und `data/research.json` nachgerechnet | **0 Fehler** (Bedarf je Einheit, Fehlmengen, Verbrauch ohne Minus, 21 Voraussetzungen, Freischaltungen) |
| 12:00 | Hauptagent | `src/main.py`, `src/gebaeude_wirkung.py`, `data/gebaeude_wirkung.json`, `tests/test_weltkarte.py`, `tests/test_gebaeude_wirkung.py` | Feinkarten-Module (`karten_optik`, `welt_optik`) eingehängt, drei alte Zeichenroutinen entfernt; Ortsnamen raus aus den Feldern, „Vorkommen" statt „Gebäude" (astra-Gutachten); **Hausausbau bis Stufe 4** (je +5 Siedler, Vorgabe Daniel) | `test_weltkarte` **60/0/0** · `test_gebaeude_wirkung` **107/0/1** · Sammellauf **2150/0/20** über 36 Dateien (vor der Haus-Änderung) |
| 11:5x | kind-weltoptikfein | `src/welt_optik_fein.py` (neu), `tests/test_welt_optik_fein.py` (neu) | feinere Weltkarte nach dem zweiten astra-Gutachten: Gelände mit deterministischen Varianten und Uferbändern, Orts-Silhouetten, Fahne, goldene Auswahl, Regionsnamen mit Schatten, 4×4-Übersicht, Zoomstufen | Kind-Test gemeldet, Koordinator prüft nach |
| 11:5x | kind-kartenoptikfein | `src/karten_optik_fein.py` (neu), `tests/test_karten_optik_fein.py` (neu) | feinere Siedlungskarte: Gebäude-Baukörper mit Silhouettenfamilien, reicheres Gelände, Wege, goldene Auswahl, Stufenpips, äußere Koordinatenleiste | Kind-Test gemeldet, Koordinator prüft nach |
| 11:5x | kind-ausruestung | `src/ausruestung.py` (neu), `tests/test_ausruestung.py` (neu) | Ausrüstungskette als Datenschicht: Warenbedarf je Einheit, Fehlmengen im Lager, Ausbildbarkeit, Verbrauch, Spielerkette | Kind-Test gemeldet, Koordinator prüft nach |
| 11:5x | kind-forschungspfad | `src/forschungspfad.py` (neu), `tests/test_forschungspfad.py` (neu) | Forschung als Baum: erfüllte/blockierte Voraussetzungen, sichtbare Wirkung, was eine Forschung freischaltet, Empfehlungsreihenfolge | Kind-Test gemeldet, Koordinator prüft nach |
| 11:23 | Hauptagent | `src/main.py`, `tests/test_weltkarte.py` (neu), `run_tests.bat` | **Weltkarte nach der astra-Vorgabe (A3) umgebaut**: Zeichenfläche mit 48 px je Feld in eigenen Scrollbalken, Zoomstufen „− 100 % +", Übersichtskarte mit Ausschnittsrechteck, festes Detailpanel rechts, Gebietsleiste oben mit benannten gesperrten Gebieten, Fahne „Hier", Regionsnamen 9× einmal groß — der Klick wählt nur noch aus. Fund: die Zeichenfläche wuchs auf Fensterbreite, die Scrollbalken waren wirkungslos → behoben | `tests/test_weltkarte.py` **58/0/0** · Sammellauf **2023/0/21** über 34 Dateien |
| 11:16 | kind-weltoptik | `src/welt_optik.py` (neu), `tests/test_welt_optik.py` (neu) | feinere Zeichenpläne für die Weltkarte: sechs Geländesymbole (4–10 Formen), Fahne, Auswahlrahmen, 9 Regionsnamen, Übersichtskarte mit 400 Kacheln; Pläne als **Daten** (ohne Fenster prüfbar), `offene_luecken()` benennt Regionsnamen und Zoomstufen als Vorschlag | Kind-Test **70/0/0** · Koordinator-Nachrechnung **0 Fehler** |
| 11:10 | kind-kartenoptik | `src/karten_optik.py` (neu), `tests/test_karten_optik.py` (neu) | feinere Zeichenpläne für die Siedlungskarte: 7 Gelände-Embleme (4–10 Formen), Gebäudezeichen mit Stufenpips, Wege zwischen benachbarten bebauten Feldern, Rasterplan | Kind-Test **54/0/0** · Koordinator-Nachrechnung **0 Fehler** |
| 22:58 | Hauptagent | `src/main.py`, `src/bonus_system.py`, `tests/test_baseline.py`, `tests/test_ertrag_anbindung.py`, `run_tests.bat` | **W4b-6 eingehängt**: die 21 Originalforschungen sind im Spiel (statt 18 erfundener Gebiete), und `get_production_multiplier` liefert jetzt die BELEGTEN Faktoren für **alle neun** Rohstoffe aus `forschung_wirkung.py` | Gesamtlauf siehe Protokoll |
| 22:50 | kind-punkte | `src/punkte.py`, `tests/test_punkte.py` | W6: Forschungspunkte Stufe³, Kriegspunkte, Gesamt = halbe Summe, Ruf, Götterschutz 7 Tage, Sieg/Niederlage als gekennzeichneter Vorschlag | **76 grün** |
| 22:50 | kind-kampfbericht | `src/kampfbericht.py`, `tests/test_kampfbericht.py` | W2b: Vorrunde (Wallschwellen), Mauerschaden, Beute nach Karrenladung, Bericht für die Nachrichten | **108 grün** |
| 22:47 | kind-portalraum | `src/portalraum.py`, `tests/test_portalraum.py` | W5-2: 20 Dimensionen × 20×20 Felder, (X,Y,Z), Wechsel 5.000 Mana aus einer Siedlung, einmal je 24 h, eigen grün / fremd rot | **69 grün** |
| 22:46 | kind-werkstatt | `src/werkstatt.py`, `tests/test_werkstatt.py` | W3: 17 Waren, Warteschlangen, parallele Werkstätten — Handbuchbeispiel 10 Schwerter mit 2 Schmieden = 100 min exakt nachgerechnet | **118 grün**, 1 Befund |
| 22:45 | kind-forschung | `src/forschung_wirkung.py`, `tests/test_forschung_wirkung.py` | W4b-6: belegte Produktionsfaktoren für alle neun Rohstoffe samt `offene_luecken()` | **94 grün** |
| 22:42 | Hauptagent | `tools/build_exe.py`, `src/*` (Wurzel-Suche) | **.exe gebaut und geprüft**: startet aus einem Pfad mit Leerzeichen, Fenster „Nebelseetal Remake", sauberes Schließen; Fehler dabei gefunden und behoben (die EXE fand ihre `data/*.json` nicht) | Startlauf belegt |
| 22:12 | Hauptagent | `src/gebaeude_wirkung.py` (neu), `data/gebaeude_wirkung.json` (neu), `src/main.py`, `src/gelaende.py`, `data/buildings.json`, `tests/test_gebaeude_wirkung.py` (neu), `tests/test_baseline.py`, `run_tests.bat` | **W4b-5**: die 20 Originalgebäude wirken aus den bebauten Feldern — Haus/Bibliothek/Ausbildungsstätten/Wall; die fünf erfundenen globalen Gebäude entfallen | **103 grün** (neu), Gesamtlauf **630, 0 Fehler, 1 Befund**, Commit `a158175` |
| 21:17 | codewirtschaft | `src/wirtschaft.py`, `tests/test_wirtschaft.py` | Ertrag aus den Siedlungskarten, Kapazität, Textfassung | **42 grün** |
| 23:05 | Hauptagent | `src/main.py`, `tests/test_ertrag_anbindung.py` | **W4b-4**: Kartenerträge liefern jetzt wirklich — Zeitlauf UND Anzeige aus einer Quelle | **21 grün**, Gesamtlauf 526 |
| 23:00 | Hauptagent | `data/baupreise.json`, `src/main.py`, `src/berater.py` | die vier BELEGTEN Originalpreise; Siedler kostet Bevölkerung | Gesamtlauf 526 grün |
| 21:14 | codeforschung | `src/forschung.py`, `tests/test_forschung.py` | Forschungsablauf mit Zeit, Kosten, Abbruch | **68 grün** |
| 21:15 | codewelt | `src/welt.py`, `data/welten.json`, `tests/test_welt.py` | Limbus, 20 Dimensionen, Entfernung, Portalkosten | **42 grün** |
| 22:11 | astra (Bildmodell) | `docs/audits/astra_gamestar_antwort.txt` | drei Original-Screenshots gedeutet: Portalansicht 20×20 mit grün/rot, Original-Menü, **echte Baupreise** | 0,47 USD, vom Hauptagenten nachgeprüft |
| 21:23 | musterwelt | `docs/audits/muster_welt.txt` | Weltkarten-Vorlage — Bezug war falsch (Weltnamen sind Dimensionen), korrigiert | 0,12 USD |
| 21:23 | mustersiedlung | `docs/audits/muster_siedlung.txt` | zwei Siedlungskarten-Vorlagen (Mana-Rush, Erz-Industrie) | 0,04 USD, Raster nachgerechnet |
| 21:11 | designauftraege | `docs/audits/design_auftraege.txt` | Auftrags- und Bot-System | 0,12 USD, 9/9 Seitenangaben stimmten |
| 20:30 | ccgrab | `docs/original/karten/commoncrawl/` | Common Crawl: Seiten ja, **Bilder nein** — Suche damit abgeschlossen | 66 Abfragen, 1 h |

## Meldungen an den Hauptagenten

- **Zwei fertige Module hängen NICHT im Spiel** (Hauptagent, 22:12): `src/forschung.py` (Dauer =
  Stufe² Stunden, Stufe steigt erst nach Ablauf) und `src/welt.py` (20 Dimensionen, Portalkosten)
  sind beide geprüft grün, werden aber vom Fenster nicht benutzt — `_start_research` erhöht die
  Stufe noch im selben Klick, und im Portal steckt weiter das alte `MAPS`-Modell. Beides steht jetzt
  als eigener Schritt in `docs/PROJEKT_STAND.md` Abschnitt 5/6 (W4c-Nachtrag, W5-2).
- **Bibliothek und Ausbildungsstätten: Stufen sind Vorschlag** (Hauptagent, 22:12): belegt ist nur,
  DASS es Stufen gibt. Eingetragen sind 5 (Wall: die belegten 10) — in `data/gebaeude_wirkung.json`
  änderbar. Ebenso nicht belegt: die Höhe des Verteidigungsboni (+50 % je Stufe aus `bonus_system`).
- **Ausbildungsdauer fehlt im Handbuch** (Hauptagent, 22:12): `bonus_system.UNIT_TRAIN_BASE = 0`,
  daher bleibt die Ausbildungszeit bei 0,5 Minuten stehen und die Stufe der Stätte senkt noch nichts
  messbar. Ehrlich als Befund gemeldet, nicht als grün verkauft.
- **Kennungen in Lesefassung** (Hauptagent, 23:05): `wirtschaft.ertrag_gesamt()` liefert die
  Rohstoffe als „Holz“, „Nahrung“ … — das Spiel rechnet mit „holz“. Beim Anbinden unbedingt
  umschreiben (`k.lower()`), sonst schreibt der Zeitlauf stillschweigend **nichts** gut.
- **Eine Quelle für Rohstoffe** (Hauptagent, 23:05): die 5 rohstofferzeugenden Gebäude sind aus
  `main.BUILDINGS` entfernt (Holzfäller, Steinmetz, Jäger, Schmiede, Markt). Es gibt jetzt genau
  **eine** Produktionsquelle: die bebauten Felder der Siedlungskarten. Wer sie zurückholt, erzeugt
  doppelten Ertrag. **Seit W4b-5 ist `main.BUILDINGS` ganz leer** — auch Haus, Bibliothek, Kaserne,
  Wachturm und Portal sind entfallen; ihre Wirkungen stehen in `src/gebaeude_wirkung.py`.
- **Doppelte JSON-Schlüssel sind jetzt geprüft** (`tests/test_spieldaten.py`): JSON nimmt still den
  letzten Eintrag. Real passiert in `data/baupreise.json` (jaeger + haus doppelt) — der Test schlug
  mit 8/4 statt 80/50 an. Neue Datendateien sind damit abgesichert.
- **Lücke im Produktionsfaktor** (von codewirtschaft, 21:17): `bonus_system.get_production_multiplier`
  erhöht nur Holz, Stein, Nahrung (und das alte „eisen"). Metall, Leder, Mana, Gold, Wolle und Pferde
  bleiben bei 1,0 — Forschung wirkt dort nicht. Betrifft W4b-4.
- **Weltbezug** (von musterwelt, 21:23): die sechs Weltnamen sind Dimensionen, keine Felder in einem
  Raster. Belegt durch `portal.php` 2005 — steht in `docs/MUSTERVORLAGEN.md`.
- **Preisvorschlag widerlegt** (Hauptagent, 21:50): astra's abgeleitete Baupreise (8 Holz + 4 Stein)
  sind falsch; die echten stehen im GameStar-Screenshot und stimmen mit unserem alten Code überein.

## Freie Dateien (können sofort beansprucht werden)

`src/main.py` (nur durch den Hauptagenten) · `src/gelaende.py` · `src/wirtschaft.py` ·
`src/forschung.py` · `src/welt.py` · `src/berater.py` · `data/*.json` ·
`tests/test_*.py` (je Datei ein Agent)
