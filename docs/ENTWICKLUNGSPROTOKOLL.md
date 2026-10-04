# Entwicklungsprotokoll — Nebelseetal Remake

**Wozu:** Daniel will das Entstehen des Spiels mitschreiben. Dieses Protokoll hält die **groben
Arbeitsschritte** in der Reihenfolge fest, in der sie passiert sind — mit Beleg (Prüfzahlen,
Commit) und Datum.

**Regeln für dieses Protokoll:**

- **Nach jedem groben Schritt eine Zeile.** Kein Schritt ohne Beleg: Commit-Kennung, Prüfzahl,
  Quelle. Wer nichts belegen kann, schreibt „unbelegt" dazu.
- **Immer anhängen**, nie umschreiben. Frühere Einträge bleiben stehen, auch wenn sich etwas
  später als falsch herausstellt — dann kommt ein neuer Eintrag, der es richtigstellt.
- Die **echten Datumsangaben** kommen aus `git log --date=format:'%d.%m.%Y %H:%M' --pretty='%ad | %s'`,
  nicht aus dem Gedächtnis.
- Fehler gehören ins Protokoll, nicht nur ins Ergebnis. Das ist der Punkt: man soll sehen, wie es
  wirklich entstanden ist.

---

## Vorgeschichte (vor dem 04.10.2026)

Das Spiel selbst entstand früher: ein älterer Build (`Nebelsee Memory.exe` vom 27.08.2026) enthielt
noch **36 erfundene Einheiten** (Worg, Drache, Troll, Golem …). Er liegt in der Quarantäne, damit im
Projektordner genau **eine** startbare Fassung steht. Die Belege der Originalrecherche (Handbuch
2009, 16 Website-Seiten, 15 Seiten von 2005, Archivbilder) liegen in `docs/original/`.

## 04.10.2026 — Tag 1: vom Rohbau zum Handbuchspiel

### A. Sicherheitsnetz und Belege (14:51–15:36)

| Zeit | Schritt | Ergebnis / Beleg |
|---|---|---|
| 14:51 | **Grundstand gesichert** | das vorhandene Spiel läuft; 36 Einheiten, Originaldaten und Icons ins Git |
| 14:54 | **Datengrundlagen** | 4 Pakete aus den Originaldaten ausgewertet |
| 14:59 | **28 Originaleinheiten** | `data/units.json` aus dem Handbuch — die 36 erfundenen ersetzt |
| 15:08 | **Plan gegen das Handbuch** | `docs/PLAN_AUS_HANDBUCH.md` + Projektstand als Einstiegspunkt |
| 15:10 | **Datenschicht** | `src/spieldaten.py` — eine Wertequelle aus `data/*.json` |
| 15:20 | **W1d + W2** | eine Wertequelle und echter Kampfablauf nach Handbuch S. 20–22; Paladin ×10 = 1450 |
| 15:23 | **Reparatur nach dem Umbau** | Grundprüfung wieder grün: **92 Prüfungen, 0 Fehler** |
| 15:35 | **W4a** | die 9 Originalrohstoffe; 17 Waren statt erfundener |
| 15:36 | **Projektstand** | auf W4a gebracht, Baupreise als offene Frage vermerkt |

### B. Icons, Oberfläche, genau eine Fassung (19:13–19:38)

| Zeit | Schritt | Ergebnis / Beleg |
|---|---|---|
| 19:13 | **Forschungskosten** | Handbuch S. 13: Stufe 1 = 50 Holz, Verdopplung je Stufe |
| 19:15 | **Icons aufbereitet** | Hintergrund messbar entfernt, Vergleichsblätter zur Abnahme |
| 19:15 | **Vergleichsblätter repariert** | Grundfläche war RGB statt RGBA |
| 19:17 | **Icons im Spiel** | sauber eingesetzt, Abnahme von Daniel vermerkt |
| 19:33 | **Alter EXE-Build in Quarantäne** | der Projektordner hat jetzt **genau eine** startbare Fassung |
| 19:38 | **Rollbarer Inhaltsbereich** | Lager und Kaserne waren unten abgeschnitten |
| 19:38 | **Zahlenangabe korrigiert** | ein zu früh gemeldeter Wert richtiggestellt |

### C. Regelgutachten mit gpt-6-astra (19:44–19:58)

| Zeit | Schritt | Ergebnis / Beleg |
|---|---|---|
| 19:44 | **Einsatzplan astra** | „Gutachter, nicht Arbeiter" — ein Umlauf, kein Werkzeug, klarer Auftrag |
| 19:51 | **Kampf gegen Handbuch geprüft** | **acht bestätigte Abweichungen** behoben (astra Einsatz 1) |
| 19:58 | **Konformitäts-Audit** | Arbeitsliste über alle 24 Handbuchseiten (astra Einsatz 2) |

### D. Karten, Gelände, Wirtschaft (20:06–20:51)

| Zeit | Schritt | Ergebnis / Beleg |
|---|---|---|
| 20:06 | **Wirtschafts-Entwurf + Weg zur `.exe`** | astra Einsatz 3; Befund: Handbuch-Forschungstempo = 385 h, unspielbar als Einzelspieler |
| 20:26 | **Gelände und Siedlungskarten** | 7 Geländearten, **5 Kartentypen** mit messbarem Vorteil; `src/gelaende.py` |
| 20:33 | **Siedlungskarte im Spiel + Ordnung** | eigene Karte je Siedlung, niemals zwei gleiche; `docs/ORDNUNG.md` |
| 20:37 | **Farbwelt des Originals** | aus den vier erhaltenen Website-Bildern übernommen |
| 20:51 | **Siedlungsansicht im Fenster** | 8×5-Raster, Feld anklicken, Eignung, bauen, abreißen |

### E. Auskunft, Entwürfe, Originalbilder (21:14–21:33)

| Zeit | Schritt | Ergebnis / Beleg |
|---|---|---|
| 21:14 | **Auskunft im Spiel** | Reiter „Chat" antwortet aus Handbuch und Daten — ohne Netz, ohne Schlüssel |
| 21:16 | **Gesamtlauf** | die neue Prüfdatei aufgenommen |
| 21:18 | **Auftrags- und Bot-System** | Entwurf von `deepseek-v4-pro` (0,12 USD), **Seite für Seite nachgeprüft**: 9/9 Angaben korrekt |
| 21:28 | **Drei neue Module** | `wirtschaft`, `forschung`, `welt` + zwei Siedlungsvorlagen; echte Original-Screenshots gefunden → **488 Prüfungen grün** |
| 21:29 | **Modelldaten gesichert** | 23 Dateien (12 Antworten, 11 Eingaben, 908 KB) in `docs/audits/` — nichts darf verloren gehen |
| 21:31 | **Übergabe geschrieben** | `docs/PROJEKT_STAND.md`: Ziel, Stand, Modelldaten, nächste Schritte |
| 21:33 | **Bildsuche abgeschlossen** | vier Wege geprüft, alle negativ; der Fund sind die drei GameStar-Screenshots |

### F. Arbeitssystem und der nächste Schritt (21:35–21:50)

| Zeit | Schritt | Ergebnis / Beleg |
|---|---|---|
| 21:35 | **Arbeitssystem** | `docs/BOARD.md` (Kommunikationsbrett der Unteragenten) + `docs/AGENTEN_PLAN.md` (Aufteilung, Modellwahl) |
| 21:36 | **Nachlese** | `docs/LEHREN.md`: 13 eigene Fehler mit Ursache und Konsequenz |
| 21:41 | **Baupreise belegt** | die vier echten Preise aus dem GameStar-Screenshot (10/5+1 Siedler usw.); Siedler kostet Bevölkerung |
| 21:41 | **Doppelte JSON-Schlüssel geprüft** | Falle real passiert (jaeger, haus) — jetzt in `tests/test_spieldaten.py` abgesichert |
| 21:50 | **W4b-4: Kartenerträge angebunden** | bebaute Felder liefern wirklich Rohstoffe; ein echter Fehler dabei gefunden (Kennungen „Holz" gegen „holz") → **526 Prüfungen, 0 Fehler über elf Dateien** |

---

## Stand

- **526 Prüfungen, 0 Fehler** über elf Dateien (`run_tests.bat`), Commit `472704f`.
- **Ziel noch offen:** es gibt noch keine `.exe` mit Passworttor (Paket W9).
- **Nächster Schritt:** W4b-5 — die 20 Originalgebäude samt ihren Wirkungen ins Spiel holen.
- Die vollständige Historie: `git log --oneline` (40 Commits).
