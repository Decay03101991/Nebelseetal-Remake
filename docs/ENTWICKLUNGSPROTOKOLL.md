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
| 19:51 | **Kampf gegen Handbuch geprüft** | **acht bestätigte Abweichungen** behoben (astra Einsatz 1) — **0,43 USD** |
| 19:58 | **Konformitäts-Audit** | Arbeitsliste über alle 24 Handbuchseiten (astra Einsatz 2 + 2b) — **~0,78 USD** |

### D. Karten, Gelände, Wirtschaft (20:06–20:51)

| Zeit | Schritt | Ergebnis / Beleg |
|---|---|---|
| 20:06 | **Wirtschafts-Entwurf + Weg zur `.exe`** | astra Einsatz 3 (**~0,8 USD**); Befund: Handbuch-Forschungstempo = 385 h, unspielbar als Einzelspieler |
| 20:26 | **Gelände und Siedlungskarten** | 7 Geländearten, **5 Kartentypen** mit messbarem Vorteil; `src/gelaende.py` |
| 20:33 | **Siedlungskarte im Spiel + Ordnung** | eigene Karte je Siedlung, niemals zwei gleiche; `docs/ORDNUNG.md` |
| 20:37 | **Farbwelt des Originals** | aus den vier erhaltenen Website-Bildern übernommen (astra Einsätze 4+5: **~0,3 + ~0,2 USD**) |
| 20:51 | **Siedlungsansicht im Fenster** | 8×5-Raster, Feld anklicken, Eignung, bauen, abreißen |

### E. Auskunft, Entwürfe, Originalbilder (21:14–21:33)

| Zeit | Schritt | Ergebnis / Beleg |
|---|---|---|
| 21:14 | **Auskunft im Spiel** | Reiter „Chat" antwortet aus Handbuch und Daten — ohne Netz, ohne Schlüssel |
| 21:16 | **Gesamtlauf** | die neue Prüfdatei aufgenommen |
| 21:18 | **Auftrags- und Bot-System** | Entwurf von `deepseek-v4-pro` (**0,12 USD**), **Seite für Seite nachgeprüft**: 9/9 Angaben korrekt |
| 21:28 | **Drei neue Module** | `wirtschaft`, `forschung`, `welt` + zwei Siedlungsvorlagen (**0,04–0,12 USD**); echte Original-Screenshots analysiert (**0,47 USD**) → **488 Prüfungen grün** |
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

### G. W4b-5: die 20 Originalgebäude wirken (22:05–22:15)

| Zeit | Schritt | Ergebnis / Beleg |
|---|---|---|
| 22:05 | **W4b-5 begonnen** | Übergabe, Agentenplan, Brett und dieses Protokoll gelesen; Ist-Stand gemessen: **526 Prüfungen grün** über elf Dateien |
| 22:06 | **Kosten vorher gemessen** | Tagessumme **8,81 EUR** (9,89 USD) — über dem normalen 4-EUR-Limit, aber für diesen Auftrag von Daniel ausgesetzt (Skill `kosten-schutzregel`, laufende Ausnahme). Kein teures Modell nötig |
| 22:08 | **Wirkungsmodul gebaut** | `src/gebaeude_wirkung.py` + `data/gebaeude_wirkung.json`: Bevölkerung (10 Siedler je Siedlung, +5 je Haus, 1 Siedler/Stunde, Heilkunde +10 % je Stufe), Bibliothekspflicht und Standortregel, die drei Ausbildungsstätten (Zuordnung aus `data/units.json`, kein Wert geraten), Wallstufen mit Schwellenwerten und Kriegspunkten |
| 22:10 | **ins Spiel gehängt** | `main.BUILDINGS` ist leer: Haus hebt die Siedlergrenze, Bibliothek schaltet Forschung frei, Ausbildung nur mit der zuständigen Stätte (Stufe = Tempo), Verteidigungsbonus am Wall statt am erfundenen Wachturm, Ausbauen auf der Karte (Wall bis 10); `max_je_siedlung` wird durchgesetzt |
| 22:11 | **erster Lauf rot — und das war richtig so** | `test_siedlungskarte` schlug an, weil ich den Gebäudeschlüssel beim Bauen normalisiert hatte; die Prüfung hielt zu Recht fest, dass `bauten` den übergebenen Schlüssel speichert. **Verhalten zurückgenommen, nicht die Prüfung aufgeweicht.** Dazu zwei eigene Testfehler (Krieger kostet Gold und Pferde; ohne belegte Ausbildungsdauer bleibt die Zeit bei 0,5 Minuten) — beide ehrlich gemacht statt weggerechnet |
| 22:12 | **grün** | `run_tests.bat`: **630 Prüfungen, 0 Fehler, 1 Befund** über **zwölf** Dateien (neu: `tests/test_gebaeude_wirkung.py`, 103 Prüfungen). Commit `a158175` |
| 22:13 | **echter Start** | `python src/main.py` im Fenster: Fenstertitel „Nebelseetal Remake" (PID 19232), danach beendet; keine Dateileiche im Projektordner, keine zweite Fassung |
| 22:15 | **Kosten nachher gemessen** | Tagessumme **8,87 EUR** (9,96 USD) → dieser Schritt ≈ **0,06 EUR** |

**Drei ehrliche Nebenbefunde beim Nachprüfen** (stehen in `docs/PROJEKT_STAND.md` Abschnitt 5/6):
der erfundene Portal-Bau ist ersatzlos entfallen (weitere Karten schaltet jetzt die Forschung
„Vermessung" frei — Entscheidung für Daniel); die Originalregel „höchstens eines je Siedlung" gilt
jetzt; und beim Nachsehen fiel auf, dass `src/forschung.py` und `src/welt.py` zwar fertig geprüft,
im Spiel aber **nicht eingehängt** sind — die Forschung steigt noch im selben Klick, und im Portal
steckt noch das alte `MAPS`-Modell.

**Nachtrag (22:17) — ein Fund beim Aufräumen, noch NICHT behoben:** `src/main.py` schützt sich gegen
einen doppelten Start über `src/game.lock` (dort steht die Prozessnummer). Die Prüfung benutzt
`os.kill(pid, 0)` — unter Windows **beendet** `os.kill` den Prozess, statt nur zu fragen (Signal 0 wird
dort als `TerminateProcess` ausgeführt). Steht eine alte Nummer in der Sperrdatei und ist sie inzwischen
an ein fremdes Programm vergeben, würde der Spielstart dieses Programm beenden. Beim Teststart blieb
außerdem eine Sperrdatei zurück (mein Abbruch umging die Aufräumroutine); sie ist entfernt. Der Fund
gehört zu Paket **W9** (Auslieferung, doppelter Start) — geändert wurde hier nichts, damit der Schritt
prüfbar bleibt.

---

## Kosten

**Grundsatz:** nur belegte Beträge. Die Einzelposten sind Schätzungen je Auftrag (gerundet), der
Tageswert ist **gemessen**. Wo nichts steht, wurde nichts bezahlt — die Unteragenten laufen auf
`deepseek-flash` (Bruchteile eines Cents), die Recherchen (Web-Archiv, Common Crawl, GameStar) sind
kostenlos.

### Bezahlte Modellaufträge am 04.10.2026

| Schritt | Modell | Kosten |
|---|---|---|
| Kampf-Audit gegen das Handbuch (19:51) | gpt-6-astra | 0,43 USD |
| Konformitäts-Audit über 24 Handbuchseiten (19:58) | gpt-6-astra | ~0,78 USD |
| Wirtschaftsentwurf (20:06) | gpt-6-astra | ~0,80 USD |
| vier Website-Bilder gedeutet (20:26) | gpt-6-astra | ~0,30 USD |
| Farbwelt aus vier Bildern (20:37) | gpt-6-astra | ~0,20 USD |
| drei GameStar-Screenshots gedeutet (brachte die **echten Baupreise**) | gpt-6-astra | 0,47 USD |
| Auftrags- und Bot-System-Entwurf | deepseek-v4-pro | 0,12 USD |
| zwei Siedlungskarten-Vorlagen | deepseek-v4-pro | 0,04–0,12 USD |

**Summe der astra-Einzelposten:** ~2,98 USD (sechs Aufträge).
**Gemessen:** **3,33 USD** Verbrauch am 04.10. — ermittelt über
`/v1/organization/costs?group_by=line_item`, nicht über den Tageswert.
**Kontostand danach: 5,56 USD verfügbar** (von Daniel von der Billing-Seite abgelesen, Stand
04.10.2026; erster Stand war 8,89 USD). Auto-Recharge ist **aus** — es können keine Schulden
entstehen, bei aufgebrauchtem Guthaben brechen die Aufrufe ab.
**DeepSeek:** 3,32 USD (aus der Übergabe; **nicht nachgeprüft**). Davon muss ein Rest bleiben.

### Kosten dieses Schritts (W4b-5, 04.10.2026)

| Schritt | Modell | Kosten |
|---|---|---|
| W4b-5 (Wirkungsmodul, Einhängen in `main.py`, 103 neue Prüfungen, Doku) | `deepseek-v4-flash` (Standard) | **≈ 0,06 EUR** — gemessen als Differenz der Tagessumme |

**Wie gemessen:** `tageskosten_check.py --json` vor dem Schritt (8,81 EUR) und danach (8,87 EUR);
die Differenz enthält jede Modellnutzung im selben Zeitfenster (auch andere Profile). Kein teures
Modell im Einsatz: `gpt-6-astra` war nicht nötig (keine Bilddeutung — alle Zahlen stehen im Handbuch
und in den Datendateien), `deepseek-v4-pro` ebenfalls nicht.
**Zur 4-EUR-Regel:** der Tag liegt mit 8,87 EUR über dem normalen Limit; für den Auftrag
„Nebelseetal Remake so gut wie möglich" hat Daniel die Regel ausgesetzt (Skill `kosten-schutzregel`,
laufende Ausnahme). Auto-Recharge ist aus — Schulden sind nicht möglich.
**DeepSeek-Guthaben:** nicht nachgeprüft (der Schlüssel liegt nur in Hermes, nicht in der Shell).

### Die teuerste Einzelheit (wichtig fürs nächste Mal)

Bei `gpt-6-astra` sind die **Cache-Schreibkosten** der größte Posten: **3,56 USD gegen 0,94 USD
Ausgabe**. Dieselbe lange Auftragsformulierung wiederholt sich also teuer. Regel daraus: Aufträge
kurz halten und gleiche Formulierungen wiederverwenden.

### Widerspruch, richtiggestellt

Ältere Notizen im Projekt und in der Übergabe nannten „4,54 USD verbraucht → 1,02 USD Reserve" und
„6,31 USD heute, 4,06 USD Mission, 1,50 USD Reserve". Diese Zahlen widersprechen sich und dem
Messwert. **Richtig ist: 3,33 USD verbraucht, 5,56 USD verfügbar.** Die alten Angaben stammen aus
dem Tageswert der Ausgaben-API, der in Schüben aktualisiert und deshalb unbrauchbar ist.

---

## Stand

- **526 Prüfungen, 0 Fehler** über elf Dateien (`run_tests.bat`), Commit `472704f`.
- **Ziel noch offen:** es gibt noch keine `.exe` mit Passworttor (Paket W9).
- **Nächster Schritt:** W4b-5 — die 20 Originalgebäude samt ihren Wirkungen ins Spiel holen.
- Die vollständige Historie: `git log --oneline` (40 Commits).

---

## Stand nach W4b-5 (04.10.2026, 22:15)

- **630 Prüfungen, 0 Fehler, 1 Befund** über **zwölf** Dateien (`run_tests.bat`), Commit `a158175`.
  Der Befund ist bekannt und ehrlich: das Handbuch nennt keine Ausbildungsdauer, deshalb senkt die
  Stufe einer Ausbildungsstätte noch nichts messbar.
- **Ziel weiterhin offen:** es gibt noch keine `.exe` mit Passworttor (Paket W9).
- **Nächster Schritt:** W4b-6 — der Produktionsfaktor für alle neun Rohstoffe (gehört mit den
  21 Originalforschungen zusammen, weil die Faktoren an deren Namen hängen).
- **Neu entdeckt und als eigener Schritt vermerkt:** `src/forschung.py` und `src/welt.py` sind fertig
  geprüft, aber im Spiel **nicht eingehängt** — die Forschungsstufe steigt noch im selben Klick, und
  im Portal steckt noch das alte `MAPS`-Modell.
- Die vollständige Historie: `git log --oneline`.
