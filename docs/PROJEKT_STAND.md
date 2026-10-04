# Nebelseetal Remake — Projektstand

**Diese Datei ist der Einstiegspunkt.** Jede neue Sitzung liest zuerst hier — nicht die Chat-Historie.
Sie wird nach jedem Arbeitsschritt aktualisiert. Stand: 04.10.2026.

---

## 1. In drei Befehlen prüfen

```bash
cd /d/Arbeiten/Nebelseetal_Remake
python tests/test_baseline.py     # oder: run_tests.bat
git log --oneline | head -10
```

Erwartet: **26 bestanden, 0 Fehler, 2 Befunde**. Die zwei Befunde sind bekannte Altlasten im Code
(29 Einheiten ohne Kampfkraft, Platzhalter-Icons) und werden in W1b/W2 abgebaut. Ein grüner Lauf
bedeutet also *nicht* „Spiel fertig".

## 2. Richtschnur

**Das Original-Handbuch ist verbindlich** (von Daniel bestätigt). Alle Namen, Zahlen und Regeln
stammen daraus. Liegt eine Angabe dort nicht vor, wird sie **null** gesetzt und begründet — es wird
**nichts geschätzt**. Originalquellen: `docs/original/` (PDF, 16 archivierte Seiten, 13 Website-Seiten,
ausgelesene Tabellen als Markdown).

## 3. Was fertig ist

| Paket | Inhalt | Beleg |
|---|---|---|
| **W0** Sicherheitsnetz | Git-Repo (Branch `main`), `.gitignore`, Prüfrahmen `tests/` + `run_tests.bat` | 3 Commits, 26 Prüfungen grün |
| **W1a** Originaldaten | `docs/original/` mit Handbuch, Spielanleitung 2005, Website, ausgelesenen Tabellen | selbst gegen das PDF nachgeprüft |
| **W1b** Icons | 45 Ausschnitte: 17 vorhandene + 28 neu geschnitten, Zuordnung mit Beleg | `data/icon_map.json`, `data/icons_index.json` |
| **W1c** Datengrundlagen | 28 Einheiten, 17 Waren, 21 Forschungen, 9 Rohstoffe, 20 Gebäude + 10 Wallstufen | `data/*.json`, je Datei `_quelle` |

### Artefaktkarte

| Datei | Inhalt |
|---|---|
| `data/units.json` | **28 Originaleinheiten**: Kosten, Waren, Voraussetzung, Kriegspunkte, Ladung, Kampfwerte, Icon |
| `data/unit_stats.json` | Kampfwerte spaltensicher aus dem Handbuch (15 vollständig, 13 ohne MU — in der Vorlage nicht abgedruckt) |
| `data/items.json` | 17 Waren mit Werkstatt, Voraussetzung, Icon, verbrauchenden Einheiten |
| `data/research.json` | 21 Forschungen + Ablaufregeln (Dauer = Stufe², Kosten verdoppeln sich) |
| `data/resources.json` | 9 Rohstoffe, Ertrag je Geländeart, Siedlerregeln, Startwerte |
| `data/buildings.json` | 20 Gebäude + Verteidigungswall Stufen 1–10 mit Schwellenwerten |
| `data/icon_map.json` | Blatt-Zelle → Originalname, **mit Beleg je Eintrag** |
| `data/icons_index.json` | Originalname → Icon-Datei (45 Einträge) |
| `assets/icons/units/` | 11 Einheiten-Icons (neu geschnitten) |
| `assets/icons/items/` | 17 Waren-Icons (neu geschnitten) |
| `assets/icons/original_units/` | **Daniels 17 Dateien — unangetastet** |
| `tools/slice_icons.py` | Icon-Schnitt: `--preview` (nummerierte Kontrollblätter), `--write` (schneidet + Index) |
| `tools/build_units.py` | erzeugt `data/units.json` reproduzierbar aus den Originalquellen |
| `tools/pdf_stats.py` | liest die Wertetabelle mit Koordinaten aus dem PDF |
| `docs/original/ORIGINAL_*.md` | ausgelesene Originaldaten als lesbare Fassung |
| `docs/icon_preview/` | Kontrollblätter für die gemeinsame Abnahme |

## 4. Was der Code noch NICHT kann (der eigentliche Umbau)

Der Code läuft, benutzt aber **erfundene Daten**. Gemessen:

| im Code | Original | Folge |
|---|---|---|
| **36 Einheiten**, davon 31 erfunden (Worg, Drache, Troll, Ork, Golem …) | **28** | Kampf sinnlos: 29 von 36 haben Kampfkraft 0 |
| 10 Rohstoffe (`kristall, stoff, geld, wissen` …) | 9 (Holz, Stein, Metall, Mana, Nahrung, Gold, Wolle, Leder, Pferde) | falsche Wirtschaft |
| 18 Forschungen | 21 | — |
| 10 Gebäude | 20 | — |
| 17 Waren nur als Emoji-Einträge | 17 gefertigte Waren mit Werkstatt | Handwerk fehlt |
| Kampf = ein Zufallsvergleich | Vorrunde + bis zu 10 Kampfsequenzen + Zweikämpfe | kein Kampfablauf |
| keine Karren, keine Belagerung | 6 Karren + 7 Belagerungswaffen | — |

## 5. Nächste Schritte

**Der verbindliche Plan liegt in `docs/PLAN_AUS_HANDBUCH.md`** — kapitelweise gegen die 24 Seiten des
Handbuchs, mit Einzelspieler-Umsetzung je Seite und Paketzuordnung. Kurzfassung der Reihenfolge:

1. **W1d — Code auf die Originaldaten umstellen.** `src/main.py` und `src/bonus_system.py` aus
   `data/*.json` speisen statt aus eigenen Tabellen. Danach: **eine** Wertequelle, Anzeige stimmt
   mit Rechnung überein. Erwartetes Ergebnis: 28/28 Einheiten mit Kampfkraft > 0.
2. **W2 — Kampfablauf** nach `docs/original/ORIGINAL_Kampf_und_Punkte.md`: Vorrunde mit
   Wallschwellen, bis zu 10 Kampfsequenzen, Fernkampf gleichzeitig, Zweikämpfe mit AT/PA/RS/TP,
   Erschöpfung, Flucht ab LE < 5, Beute durch Transportkarren, Bericht.
3. **W3 — Handwerk**: Waren in Schmiede/Bogner/Nähstube fertigen (Warteschlangen, mehrere
   Werkstätten parallel), Waren als Voraussetzung für Einheiten.
4. **W4 — Wirtschaft**: Bauzeiten (Stufe² bei Forschung belegt), Siedler (1/Stunde, Grenze 10, +5 je Haus), Lagerkapazität.
5. **W5 — Welt und Gegner**: Bots nach Originalverhalten, Götterschutz (7 Tage, eingeschränkt bis 299 Punkte).
6. **W6 — Punkte und Ziel**: Forschungspunkte = Σ Stufe³, Kriegspunkte je Einheit, Verteidigungsanlagen³, Gesamt = (Krieg + Forschung) / 2.
7. **W7 — Oberfläche**: Original-Icons einbinden, Kaserne/Lager/Karten mit echten Werten.
8. **W8 — Speichern** robust + Versionskennung; **W9 — portable Windows-Version**.

## 6. Offene Entscheidungen (Daniel)

- **Kampftempo**: Original ist Echtzeit (Forschung Stufe² Stunden). Beschleunigt für Einzelspieler?
- **Karten**: Reicht der Kontinent mit Sektoren, oder die vier kleinen Welten voll ausbauen?
- **Ziel**: Siegbedingung — alle Welten + eroberte Siedlungen + Punktzahl, oder reine Punktewertung?
- **Einheitenwert-Lücken**: Für die 13 Karren/Belagerungswaffen fehlt MU in der Vorlage. Regel
  festlegen (z. B. MU = 0, damit sie nicht fliehen — Karren sollen laut Handbuch Waren bergen).

## 7. Arbeitsweise in diesem Projekt

- **Nie schätzen.** Fehlt ein Originalwert: `null` + Begründung, nicht raten.
- **Originaldateien unantastbar**: die 7 Blätter, Daniels 17 Dateien, `docs/original/`.
- **Prüfen statt behaupten**: nach jeder Änderung `python tests/test_baseline.py`, bei
  Oberflächenänderungen zusätzlich ein echter Start mit Fenstertitel-Prüfung.
- **Unteragenten berichten nur** — jedes Ergebnis wird selbst nachgeprüft (zwei Kinder-Meldungen
  waren schon falsch, drei eigene Prüfungen ebenfalls). Gegengeprüft wird mit einem **anderen
  Verfahren** als dem des Berichtenden.
- **Kleine Commits** nach jedem Paket, damit jeder Schritt rücknehmbar ist.
- **Blätter für Daniel**: `docs/icon_preview/` enthält nummerierte Kontrollblätter; solche
  Entscheidungen werden vorgelegt, nicht allein getroffen.

## 8. Dauerhaftes Arbeitssystem (steht bereit)

| Baustein | Was es leistet | Wo |
|---|---|---|
| `docs/PROJEKT_STAND.md` | Wiederaufnahme ohne Chatverlauf | dieses Dokument |
| `docs/PLAN_AUS_HANDBUCH.md` | Plan gegen die 24 Handbuchseiten | im Projekt |
| `tests/test_baseline.py` + `run_tests.bat` | Wahrheitsquelle „läuft es noch?" | im Projekt |
| Skill `multi-agent-coding` | Betriebssystem für parallele Coding-Agenten (Zerlegung, Nachprüfung, Pitfalls) | Hermes-Skill |
| Skill `nebelseetal-remake` | Projektwissen, Fallen, Icon-Raster, Vorgängerregeln | Hermes-Skill |
| Profil `coding` | eigener Arbeiter mit geklonten Regeln (`SOUL.md`) | Hermes-Profil |
| Kanban-Board `nebelseetal` | dauerhafte Warteschlange der Pakete, überlebt Sitzungen | `hermes kanban list` |

**Hinweis:** Der Kanban-Verteiler (Dispatcher) läuft nur mit laufendem Gateway. Ohne Gateway bleiben
Aufgaben in `ready` — dann einzeln starten oder `hermes kanban dispatch` von Hand aufrufen.

## 9. Commit-Historie

| Commit | Inhalt |
|---|---|
| `5234e79` | `data/units.json`: 28 Originaleinheiten, `tools/build_units.py` |
| `329081f` | Datengrundlagen aus den Originaldaten (4 Pakete) |
| `f46d702` | Grundstand vor dem Umbau: Spiel läuft, Originaldaten und Icons gesichert |
