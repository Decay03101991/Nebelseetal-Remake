# Kommunikationsbrett

**Zweck:** Unteragenten arbeiten an getrennten Dateien, müssen aber voneinander wissen. Dieses Brett
ist der einzige gemeinsame Ort — es liegt in Git, also sieht es jede Sitzung und jeder Agent.

**Regeln (kurz):**

1. **Vor dem Arbeiten lesen.** Wer hier Dateien beansprucht hat, ist für andere tabu.
2. **Beanspruchen, bevor geschrieben wird** — eine Zeile in „Laufende Ansprüche".
3. **Nach dem Arbeiten Ergebnis eintragen** — mit **echten** Zahlen aus der eigenen Prüfung.
4. **Nur anhängen.** Fremde Einträge niemals ändern oder löschen.
5. **Bei Kollision nicht selbst lösen**: hier melden und den Hauptagenten entscheiden lassen.
6. Kurz halten: drei Zeilen reichen. Das Brett ist kein Tagebuch.

Format einer Zeile: `Zeit | Agent | Dateien | Ziel/Ergebnis | Prüfung | offen`

---

## Laufende Ansprüche

*Zurzeit keine — alle Kinder sind beendet, alle Dateien sind frei.*

## Abgeschlossene Arbeiten (neueste zuerst)

| Zeit | Agent | Dateien | Ergebnis | Prüfung |
|---|---|---|---|---|
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
