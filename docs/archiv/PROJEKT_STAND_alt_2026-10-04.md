# Nebelseetal Remake — Projektstand

**Diese Datei ist der Einstiegspunkt.** Jede neue Sitzung liest zuerst hier — nicht die Chat-Historie.
Sie wird nach jedem Arbeitsschritt aktualisiert. Stand: 04.10.2026.

---

## 1. In drei Befehlen prüfen

```bash
cd /d/Arbeiten/Nebelseetal_Remake
run_tests.bat                     # oder einzeln:
python tests/test_baseline.py     # 29 Prüfungen — läuft das Spiel noch?
python tests/test_spieldaten.py   # 35 Prüfungen — stimmen die Originaldaten und die Rohstoffe?
python tests/test_kampf.py        # 33 Prüfungen — hält sich der Kampf ans Handbuch?
git log --oneline | head -10
```

Erwartet: **97 bestanden, 0 Fehler, 0 Befunde**. Ein grüner Lauf heißt aber *nicht* „Spiel fertig" —
er heißt „nichts ist kaputt und die umgestellten Teile halten sich ans Handbuch". Was noch fehlt,
steht in Abschnitt 4.

## 2. Richtschnur

**Das Original-Handbuch ist verbindlich** (von Daniel bestätigt). Alle Namen, Zahlen und Regeln
stammen daraus. Liegt eine Angabe dort nicht vor, wird sie **null** gesetzt und begründet — es wird
**nichts geschätzt**. Originalquellen: `docs/original/` (PDF, 16 archivierte Seiten, 13 Website-Seiten,
ausgelesene Tabellen als Markdown). Der Plan gegen die 24 Handbuchseiten: `docs/PLAN_AUS_HANDBUCH.md`.

**Wichtig zu wissen:** Das Handbuch nennt **Erträge und Wirkungen, aber keine Preise.** Einheitenkosten
sind abgedruckt (in `data/units.json`), Baupreise und Forschungskosten **nicht**. Wo Preise fehlen,
steht im Code ein Vermerk und die Frage liegt bei Daniel (Abschnitt 6) — es wird nicht geschätzt.

## 3. Was fertig ist

| Paket | Inhalt | Beleg |
|---|---|---|
| **W0** Sicherheitsnetz | Git-Repo (Branch `main`), `.gitignore`, Prüfrahmen `tests/` + `run_tests.bat` | 9 Commits, 97 Prüfungen grün |
| **W1a** Originaldaten | `docs/original/` mit Handbuch, Spielanleitung 2005, Website, ausgelesenen Tabellen | selbst gegen das PDF nachgeprüft |
| **W1b** Icons | 45 Ausschnitte: 17 vorhandene + 28 neu geschnitten, Zuordnung mit Beleg | `data/icon_map.json`, `data/icons_index.json` |
| **W1c** Datengrundlagen | 28 Einheiten, 17 Waren, 21 Forschungen, 9 Rohstoffe, 20 Gebäude + 10 Wallstufen | `data/*.json`, je Datei `_quelle` |
| **W1d** Einheiten im Code | 36 erfundene Einheiten ersatzlos entfernt; Code rechnet aus `data/units.json`; jede Einheit hat eine **Rolle** | Paladin rechnet 1450 statt 0 (10 Stück) |
| **W2** Kampfablauf | `src/kampf.py`: Vorrunde, Mauerschaden, 10 Sequenzen, Zweikampf, Erschöpfung, Flucht, Beute | 33 Prüfungen gegen die Seiten 20–22 |
| **W4a** Rohstoffe | die 9 Originalrohstoffe im Code; Startwerte 100/100/10; Siedler aus der Bevölkerung | `RESOURCES` == `data/resources.json` |

### Artefaktkarte

| Datei | Inhalt |
|---|---|
| `src/spieldaten.py` | lädt `data/*.json`; **eine** Wertequelle; Originalregeln (Forschungsdauer Stufe², Verteidigungspunkte Stufe³) |
| `src/einheiten.py` | Brücke ins Spiel: 28 Einheiten mit **Rolle** (`kaempfer`, `kundschafter`, `karren`, `belagerung`), Zugriff auf AT/PA/LE/SK/TP/Ladung |
| `src/kampf.py` | Kampfablauf nach Handbuch; Bericht, Verluste, Geflohene, Beute, Mauerzustand |
| `data/units.json` | **28 Originaleinheiten**: Kosten, Waren, Voraussetzung, Kriegspunkte, Ladung, Kampfwerte, Icon |
| `data/unit_stats.json` | Kampfwerte spaltensicher aus dem Handbuch (15 vollständig, 13 ohne MU — in der Vorlage nicht abgedruckt) |
| `data/items.json` | 17 Waren mit Werkstatt, Voraussetzung, Icon, verbrauchenden Einheiten |
| `data/research.json` | 21 Forschungen + Ablaufregeln (Dauer = Stufe², Kosten verdoppeln sich — ohne Zahlen) |
| `data/resources.json` | 9 Rohstoffe, Ertrag je Geländeart, Siedlerregeln, Startwerte |
| `data/buildings.json` | 20 Gebäude + Verteidigungswall Stufen 1–10 mit Schwellenwerten |
| `data/icon_map.json`, `icons_index.json` | Blatt-Zelle → Originalname (mit Beleg) bzw. Name → Icon-Datei (45 Einträge) |
| `assets/icons/units/`, `items/` | 11 Einheiten- und 17 Waren-Icons (neu geschnitten) |
| `assets/icons/original_units/` | **Daniels 17 Dateien — unangetastet** |
| `tools/slice_icons.py`, `build_units.py`, `pdf_stats.py` | Icon-Schnitt, `units.json` reproduzierbar, Wertetabelle aus dem PDF |
| `tests/test_kampf.py` | belegt jede Kampfregel einzeln |

## 4. Was der Code noch NICHT kann

Einheiten, Kampf und Rohstoffe rechnen jetzt aus den Originaldaten. Der Rest nicht:

| im Code | Original | Folge | Paket |
|---|---|---|---|
| 18 Forschungen | 21 Forschungen; Handbuch nennt **keine** Kosten | Forschung läuft über Bibliotheksstufe und Dauer, kostet aber keine Rohstoffe | W4b |
| 10 Gebäude mit erfundenen Preisen | 20 Gebäude; Handbuch nennt **keine** Baupreise, nur Erträge je Geländeart | Bauen stimmt nicht; Erträge fehlen | W4b |
| 17 Waren nur als Emoji-Einträge | 17 gefertigte Waren mit Werkstatt | Handwerk fehlt | W3 |
| Erträge fest im Code (`prod_map`) | Ertrag je **Geländeart** (z. B. Holzfäller: Wald 4/h, Steppe 2/h) | Wirtschaft unabhängig vom Gelände | W4b |
| „Siedler" ist noch eine Einheit | Siedler sind Bevölkerung | Siedeln läuft falsch | W4b |
| Ausbildungsdauer 0 (instant) | Handbuch nennt **keine** Dauer | offene Entscheidung (Abschnitt 6) | W4b |
| Kampf nur als Modul | — | noch nicht im Spiel auslösbar | W2b |

## 5. Nächste Schritte

1. **W4b — Gebäude, Erträge, Forschung, Siedler.** Die 20 Originalgebäude aus `data/buildings.json`;
   Erträge **je Geländeart** statt fester Zahlen (dafür braucht die Siedlung ein Gelände — der Code
   kennt bisher `forest, plains, mountain, water, village, ruins`, das Handbuch `Wald, Steppe, Grasland,
   Berg, Hügel, Nebelsee, Sumpf`: die Zuordnung muss belegt erfolgen); die 21 Forschungen; Siedler von
   der Einheit zur Bevölkerung; Siedeln über den Siedlerkarren; Wallstufen mit Schwellenwerten.
2. **W2b — Kampf ins Spiel einhängen**: Angriff öffnet `src/kampf.py`, Bericht in den Nachrichtenbereich.
3. **W3 — Handwerk**: die 17 Originalwaren statt der 17 erfundenen Handelsgüter.
4. **W5 — Welt und Gegner**, **W6 — Punkte und Ziel**, **W7 — Oberfläche**, **W8 — Speichern**, **W9 — portable Version**.

## 6. Offene Entscheidungen (Daniel)

**Icon-Abnahme (läuft):** Alle 45 Icon-Dateien waren deckend — der Blatt-Hintergrund lag als
farbiger Kasten mit im Bild. `tools/clean_icons.py` stellt den Hintergrund frei, die aufbereiteten
Kopien liegen in `assets/icons/clean/` **zusätzlich** zu den Originalen (Daniels 17 Dateien bleiben
unangetastet). Vergleichsblätter: `docs/icon_preview/Vergleich_*.png` (links vorher, rechts nachher,
Zahlen = Legende in der Sitzung). Das Spiel benutzt bereits die freigestellten Fassungen; Daniel
geht die Blätter einzeln durch und kann einzelne Nummern zurückweisen.

Neu hinzugekommen (das Handbuch schweigt hier):

- **Baupreise.** Das Handbuch nennt für Gebäude keine Preise, nur Erträge. Sollen die bisherigen
  Spielzahlen bleiben (jetzt in Originalrohstoffen ausgedrückt) oder eine eigene Regel gelten —
  etwa Preis aus Ertrag und Bauzeit ableiten?
- **Forschungskosten.** Das Handbuch sagt nur „Kosten verdoppeln sich je Stufe", nennt aber **keine**
  Zahlen. Zurzeit kostet Forschung keine Rohstoffe; Begrenzung sind Bibliotheksstufe und Dauer (Stufe²
  Stunden). Sollen Kosten dazukommen, und aus welchem Rohstoff?
- **Ausbildungsdauer.** Ebenfalls nicht im Handbuch. Zurzeit Ausbilden ohne Dauer.

Schon vorher offen:

- **Kampftempo**: Original ist Echtzeit (Forschung Stufe² Stunden). Beschleunigt für Einzelspieler?
- **Kampfdarstellung**: Bericht in einem Zug, oder Schritt für Schritt?
- **Ziel**: Siegbedingung — alle Welten + eroberte Siedlungen + Punktzahl, oder reine Punktewertung?
- **MU der 13 Karren/Belagerungswaffen**: umgesetzt ist „kämpfen nicht und fliehen nicht" (Rolle,
  keine fehlende Zahl). Damit erledigt — außer Daniel sieht das anders.

## 7. Arbeitsweise in diesem Projekt

- **Erst prüfen, WAS läuft** — nicht, was im Ordner liegt. Im Projekt lag ein alter EXE-Build
  (`Nebelsee Memory.exe`, 27.08.2026) mit dem eingefrorenen alten Datenstand. Sein Fenster heißt
  ebenfalls „Nebelseetal Remake", deshalb sah Daniel Golems und Pikeniere, obwohl der Code sie
  längst nicht mehr kennt. **Regel:** Im Projektordner liegt genau **eine** ausführbare Fassung.
  Alte Builds kommen in Quarantäne. Vor jeder Rückmeldung „das ist noch falsch" prüfen:
  `tasklist /v /fo csv` zeigt den Fenstertitel des laufenden Programms, das hilft beim Zuordnen.
- **Nie schätzen.** Fehlt ein Originalwert: `null` + Begründung, nicht raten.
- **Originaldateien unantastbar**: die 7 Blätter, Daniels 17 Dateien, `docs/original/`.
- **Prüfen statt behaupten**: nach jeder Änderung `run_tests.bat` — **alle drei** Dateien, nicht nur die
  zuletzt geschriebene. Ein einzelner grüner Lauf sagt nichts über die anderen.
- **Unteragenten berichten nur** — jedes Ergebnis wird selbst nachgeprüft (zwei Kinder-Meldungen
  waren schon falsch, drei eigene Prüfungen ebenfalls). Gegengeprüft wird mit einem **anderen
  Verfahren** als dem des Berichtenden.
- **Vor jedem Schreiben sichern**: Eingriffe in `src/main.py` laufen über ein Skript mit
  Sicherungskopie (`nebel_backup/`), das jede Ersetzung einzeln prüft und bei fehlendem Suchtext
  **ohne** zu schreiben abbricht. Zweimal hat der Wächter so einen Fehler verhindert (mitgelöschter
  `BUILDINGS`-Block; falsche Trefferzahl bei den Rohstoffnamen).
- **Kleine Commits** nach jedem Paket, damit jeder Schritt rücknehmbar ist.
- **Blätter für Daniel**: `docs/icon_preview/` enthält nummerierte Kontrollblätter; solche
  Entscheidungen werden vorgelegt, nicht allein getroffen.

## 8. Dauerhaftes Arbeitssystem (steht bereit)

| Baustein | Was es leistet | Wo |
|---|---|---|
| `docs/PROJEKT_STAND.md` | Wiederaufnahme ohne Chatverlauf | dieses Dokument |
| `docs/PLAN_AUS_HANDBUCH.md` | Plan gegen die 24 Handbuchseiten | im Projekt |
| `tests/` (3 Dateien) + `run_tests.bat` | Wahrheitsquelle „läuft es noch?" | im Projekt |
| Skill `multi-agent-coding` | Betriebssystem für parallele Coding-Agenten (Zerlegung, Nachprüfung, Pitfalls) | Hermes-Skill |
| Skill `nebelseetal-remake` | Projektwissen, Fallen, Icon-Raster, Vorgängerregeln | Hermes-Skill |
| Profil `coding` | eigener Arbeiter mit geklonten Regeln (`SOUL.md`) | Hermes-Profil |
| Kanban-Board `nebelseetal` | dauerhafte Warteschlange der Pakete | `hermes kanban list` |
| `D:/Arbeiten/_Quarantaene/` | alte Builds und Dateien, die nicht gelöscht werden sollen (dort: `Nebelsee Memory.exe` mit README) | außerhalb des Repos |

**Hinweis:** Der Kanban-Verteiler läuft nur mit laufendem Gateway `Hermes_Gateway`. Ohne Gateway
bleiben Aufgaben in `ready`; die Arbeit in einer Sitzung ist davon nicht betroffen.

## 9. Commit-Historie

| Commit | Inhalt |
|---|---|
| `f46d702` | Grundstand vor dem Umbau: Spiel läuft, 36 Einheiten, Originaldaten und Icons gesichert |
| `329081f` | Datengrundlagen aus den Originaldaten (4 Pakete) |
| `5234e79` | `data/units.json`: 28 Originaleinheiten, `tools/build_units.py` |
| `8d774d7` | `PLAN_AUS_HANDBUCH.md` + `PROJEKT_STAND.md` |
| `d60d2c4` | `src/spieldaten.py` + Prüfung (eine Wertequelle aus `data/*.json`) |
| `5a53c83` | W1d Einheiten + W2 Kampfablauf — **Meldung war falsch**: behauptete „89 Prüfungen, keine Fehler", tatsächlich brach der Umbau die Grundprüfung (6 Fehler, `BUILDINGS` mitgelöscht) |
| `fc59bbd` | Reparatur: `BUILDINGS` zurückgeholt, alte Stufentabelle entfernt, Ausbildung abgesichert — 92 Prüfungen grün |
| `205e8b9` | W4a: die 9 Originalrohstoffe, Startwerte 100/100/10, Siedler aus der Bevölkerung — 97 Prüfungen grün |
