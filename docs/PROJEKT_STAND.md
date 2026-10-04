# Nebelseetal Remake — Projektstand

**Diese Datei ist der Einstiegspunkt.** Jede neue Sitzung liest zuerst hier — nicht die Chat-Historie.
Sie wird nach jedem Arbeitsschritt aktualisiert. Stand: 04.10.2026.

---

## 1. In drei Befehlen prüfen

```bash
cd /d/Arbeiten/Nebelseetal_Remake
run_tests.bat                     # oder einzeln:
python tests/test_baseline.py     # 29 Prüfungen — läuft das Spiel noch?
python tests/test_spieldaten.py   # 30 Prüfungen — stimmen die Originaldaten?
python tests/test_kampf.py        # 33 Prüfungen — hält sich der Kampf ans Handbuch?
git log --oneline | head -10
```

Erwartet: **92 bestanden, 0 Fehler, 0 Befunde**. Ein grüner Lauf heißt aber *nicht* „Spiel fertig" —
er heißt „nichts ist kaputt und die umgestellten Teile halten sich ans Handbuch". Was noch fehlt,
steht in Abschnitt 4.

## 2. Richtschnur

**Das Original-Handbuch ist verbindlich** (von Daniel bestätigt). Alle Namen, Zahlen und Regeln
stammen daraus. Liegt eine Angabe dort nicht vor, wird sie **null** gesetzt und begründet — es wird
**nichts geschätzt**. Originalquellen: `docs/original/` (PDF, 16 archivierte Seiten, 13 Website-Seiten,
ausgelesene Tabellen als Markdown). Der Plan gegen die 24 Handbuchseiten: `docs/PLAN_AUS_HANDBUCH.md`.

## 3. Was fertig ist

| Paket | Inhalt | Beleg |
|---|---|---|
| **W0** Sicherheitsnetz | Git-Repo (Branch `main`), `.gitignore`, Prüfrahmen `tests/` + `run_tests.bat` | 8 Commits, 92 Prüfungen grün |
| **W1a** Originaldaten | `docs/original/` mit Handbuch, Spielanleitung 2005, Website, ausgelesenen Tabellen | selbst gegen das PDF nachgeprüft |
| **W1b** Icons | 45 Ausschnitte: 17 vorhandene + 28 neu geschnitten, Zuordnung mit Beleg | `data/icon_map.json`, `data/icons_index.json` |
| **W1c** Datengrundlagen | 28 Einheiten, 17 Waren, 21 Forschungen, 9 Rohstoffe, 20 Gebäude + 10 Wallstufen | `data/*.json`, je Datei `_quelle` |
| **W1d** Einheiten im Code | 36 erfundene Einheiten ersatzlos entfernt; Code rechnet aus `data/units.json`; jede Einheit hat eine **Rolle** | Paladin rechnet 1450 statt 0 (10 Stück) |
| **W2** Kampfablauf | `src/kampf.py`: Vorrunde, Mauerschaden, 10 Sequenzen, Zweikampf, Erschöpfung, Flucht, Beute | 33 Prüfungen gegen die Seiten 20–22 |

### Artefaktkarte

| Datei | Inhalt |
|---|---|
| `src/spieldaten.py` | lädt `data/*.json`; **eine** Wertequelle; Originalregeln (Forschungsdauer Stufe², Verteidigungspunkte Stufe³) |
| `src/einheiten.py` | Brücke ins Spiel: 28 Einheiten mit **Rolle** (`kaempfer`, `kundschafter`, `karren`, `belagerung`), Zugriff auf AT/PA/LE/SK/TP/Ladung |
| `src/kampf.py` | Kampfablauf nach Handbuch; Rückgabe mit Bericht, Verlusten, Geflohenen, Beute, Mauerzustand |
| `data/units.json` | **28 Originaleinheiten**: Kosten, Waren, Voraussetzung, Kriegspunkte, Ladung, Kampfwerte, Icon |
| `data/unit_stats.json` | Kampfwerte spaltensicher aus dem Handbuch (15 vollständig, 13 ohne MU — in der Vorlage nicht abgedruckt) |
| `data/items.json` | 17 Waren mit Werkstatt, Voraussetzung, Icon, verbrauchenden Einheiten |
| `data/research.json` | 21 Forschungen + Ablaufregeln (Dauer = Stufe², Kosten verdoppeln sich) |
| `data/resources.json` | 9 Rohstoffe, Ertrag je Geländeart, Siedlerregeln, Startwerte |
| `data/buildings.json` | 20 Gebäude + Verteidigungswall Stufen 1–10 mit Schwellenwerten |
| `data/icon_map.json` | Blatt-Zelle → Originalname, **mit Beleg je Eintrag** |
| `data/icons_index.json` | Originalname → Icon-Datei (45 Einträge) |
| `assets/icons/units/`, `items/` | 11 Einheiten- und 17 Waren-Icons (neu geschnitten) |
| `assets/icons/original_units/` | **Daniels 17 Dateien — unangetastet** |
| `tools/slice_icons.py` | Icon-Schnitt: `--preview` (nummerierte Kontrollblätter), `--write` (schneidet + Index) |
| `tools/build_units.py` | erzeugt `data/units.json` reproduzierbar aus den Originalquellen |
| `tools/pdf_stats.py` | liest die Wertetabelle mit Koordinaten aus dem PDF |
| `tests/test_kampf.py` | belegt jede Kampfregel einzeln (Vorrunde, Wallschwelle, Beute, Flucht, Erschöpfung) |

## 4. Was der Code noch NICHT kann

Die **Einheiten und der Kampf** rechnen jetzt aus den Originaldaten. Der Rest des Codes nicht:

| im Code | Original | Folge | Paket |
|---|---|---|---|
| 10 Rohstoffe (`kristall, stoff, geld, wissen` …) | 9 (Holz, Stein, Metall, Mana, Nahrung, Gold, Wolle, Leder, Pferde) | Ausbildung **überspringt** unbekannte Rohstoffe (`pferde`, `mana`, `wolle`, `metall`) — kein Absturz, aber auch keine echte Bezahlung | als Nächstes |
| 18 Forschungen | 21 | — | W4 |
| 10 Gebäude | 20 (+ 10 Wallstufen) | Bauen und Ertrag stimmen nicht | W4 |
| 17 Waren nur als Emoji-Einträge | 17 gefertigte Waren mit Werkstatt | Handwerk fehlt | W3 |
| „Siedler" ist eine Einheit | Siedler sind Bevölkerung; Siedeln braucht einen **Siedlerkarren** | Siedeln läuft falsch | W4 |
| Ausbildungsdauer: 0 (instant) | Handbuch nennt **keine** Dauer | offene Entscheidung, siehe Abschnitt 6 | W4 |

## 5. Nächste Schritte

1. **W4a — Rohstoffe angleichen (zuerst, blockiert alles Weitere).** Die 9 Originalrohstoffe in
   `main.RESOURCES` übernehmen (`metall, wolle, pferde, mana` kommen hinzu, `kristall, stoff, geld,
   wissen` entfallen), Icons und Produktion nachziehen. Danach bezahlt die Ausbildung wieder vollständig.
2. **W2b — Kampf ins Spiel einhängen.** `src/kampf.py` wird von der Oberfläche aufgerufen; der Bericht
   landet im Nachrichtenbereich. Bisher ist der Ablauf nur als Modul vorhanden und geprüft.
3. **W4b — Gebäude und Forschung** aus `data/buildings.json` / `data/research.json` speisen (20 Gebäude,
   21 Forschungen, Wallstufen mit Schwellenwerten), Siedler von der Einheit zur Bevölkerung machen.
4. **W3 — Handwerk**: Waren in Schmiede/Bogner/Nähstube, Warteschlangen, Waren als Einheitenvoraussetzung.
5. **W5 — Welt und Gegner**, **W6 — Punkte und Ziel**, **W7 — Oberfläche**, **W8 — Speichern**, **W9 — portable Version**.

## 6. Offene Entscheidungen (Daniel)

- **Kampftempo**: Original ist Echtzeit (Forschung Stufe² Stunden). Beschleunigt für Einzelspieler?
- **Kampfdarstellung**: Bericht in einem Zug, oder Schritt für Schritt?
- **Ausbildungsdauer**: Das Handbuch nennt keine. Eigene Regel festlegen (z. B. je Einheit aus Kosten
  und Gebäudestufe), oder Einheiten sofort verfügbar lassen?
- **Ziel**: Siegbedingung — alle Welten + eroberte Siedlungen + Punktzahl, oder reine Punktewertung?
- **MU der 13 Karren/Belagerungswaffen**: im Handbuch nicht abgedruckt. Umgesetzt ist: sie kämpfen
  nicht und fliehen nicht (Rolle, keine fehlende Zahl). Damit erledigt — außer Daniel sieht das anders.

## 7. Arbeitsweise in diesem Projekt

- **Nie schätzen.** Fehlt ein Originalwert: `null` + Begründung, nicht raten.
- **Originaldateien unantastbar**: die 7 Blätter, Daniels 17 Dateien, `docs/original/`.
- **Prüfen statt behaupten**: nach jeder Änderung `run_tests.bat` — **alle drei** Dateien, nicht nur die
  zuletzt geschriebene. Ein einzelner grüner Lauf sagt nichts über die anderen.
- **Unteragenten berichten nur** — jedes Ergebnis wird selbst nachgeprüft (zwei Kinder-Meldungen
  waren schon falsch, drei eigene Prüfungen ebenfalls). Gegengeprüft wird mit einem **anderen
  Verfahren** als dem des Berichtenden.
- **Vor jedem Schreiben sichern**: Eingriffe in `src/main.py` laufen über ein Skript mit
  Sicherungskopie (`nebel_backup/`), das jede Ersetzung einzeln prüft und bei fehlendem Suchtext
  abbricht, **ohne** zu schreiben. Nach jeder Blockersetzung: Grundprüfung laufen lassen — beim
  Einheitenumbau wurde dabei ein mitgelöschter `BUILDINGS`-Block gefunden.
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
| Kanban-Board `nebelseetal` | dauerhafte Warteschlange der 9 Pakete, überlebt Sitzungen | `hermes kanban list` |

**Hinweis:** Der Kanban-Verteiler (Dispatcher) läuft nur mit laufendem Gateway. Ohne Gateway bleiben
Aufgaben in `ready` — dann einzeln starten oder `hermes kanban dispatch` von Hand aufrufen.

## 9. Commit-Historie

| Commit | Inhalt |
|---|---|
| `f46d702` | Grundstand vor dem Umbau: Spiel läuft, 36 Einheiten, Originaldaten und Icons gesichert |
| `329081f` | Datengrundlagen aus den Originaldaten (4 Pakete) |
| `5234e79` | `data/units.json`: 28 Originaleinheiten, `tools/build_units.py` |
| `8d774d7` | `PLAN_AUS_HANDBUCH.md` + `PROJEKT_STAND.md` |
| `d60d2c4` | `src/spieldaten.py` + Prüfung (eine Wertequelle aus `data/*.json`) |
| `5a53c83` | W1d Einheiten + W2 Kampfablauf — **Meldung war falsch**: sie behauptete „89 Prüfungen, keine Fehler", tatsächlich brach der Umbau die Grundprüfung (6 Fehler, `BUILDINGS` war mitgelöscht) |
| *(nächster)* | Reparatur: `BUILDINGS` wiederhergestellt, alte Stufentabelle entfernt, Ausbildung gegen unbekannte Rohstoffe abgesichert, Grundprüfung auf 28 Originaleinheiten umgestellt — **92 Prüfungen, 0 Fehler** |
