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

### H. Passworttor und der Weg zur EXE (22:24–22:34)

| Zeit | Schritt | Ergebnis / Beleg |
|---|---|---|
| 22:24 | **Schritt 8: Passworttor gebaut** | `src/tor.py`: PBKDF2-HMAC-SHA256 mit Zufallssalz, **nie** das Passwort selbst; Wartezeit nach je drei Fehlversuchen. Im Fenster: der **Erststart** lässt Daniel das Passwort selbst festlegen (zweimal eingeben), jeder weitere Start verlangt es, ein falsches öffnet das Spiel nicht |
| 22:25 | **Notausgang im Tor** | Hinweis im Fenster und in der Tor-Datei: „Datei löschen verlangt beim nächsten Start ein NEUES Passwort — der Spielstand bleibt." Damit ist auch ein vergessenes Passwort kein Aussperren |
| 22:29 | **Doppelstart-Fund behoben** (aus Abschnitt G offen) | das gefährliche `os.kill(pid, 0)` — unter Windows **beendet** es den Prozess — ersetzt durch reines Nachsehen (`OpenProcess`/`GetExitCodeProcess`). Sperrdatei und Spielstand liegen jetzt in `~/.nebelseetal`, nicht mehr im Programmordner (in der EXE wäre der oft schreibgeschützt) |
| 22:31 | **Pfad für die EXE vorbereitet** | `spieldaten.projektwurzel()` findet die Datendateien nun im entpackten `sys._MEIPASS`-Ordner; ohne diesen Zweig findet eine PyInstaller-Einzeldatei ihre `data/*.json` nicht |
| 22:32 | **grün** | **691 Prüfungen, 0 Fehler, 1 Befund** über **dreizehn** Dateien (neu: `tests/test_tor.py`, 61 Prüfungen). Commit `8a6bd87` |
| 22:33 | **Bau-Skript für Schritt 9** | `tools/build_exe.py`: prüft sich selbst (mehrgrößiges Symbol mit 6 Größen, mitzugebende Ordner), baut die **Einzeldatei ohne Konsole**, prüft Größe und „genau **eine** EXE im Projektordner" und räumt `build/`, `dist/`, `.spec` wieder weg |

**Nachtrag (22:34) — drei Kinder arbeiten parallel** (nach `docs/AGENTEN_PLAN.md`, jedes Kind eine
neue Datei + eigene Prüfdatei): W4b-6 Produktionsfaktoren (`forschung_wirkung.py`), W3 Waren und
Werkstätten (`werkstatt.py`), W5-2 Portalraum (`portalraum.py`). Der Hauptagent hängt die Ergebnisse
selbst in `main.py` ein, prüft jede Kinder-Meldung mit einem **anderen** Verfahren nach und
committet erst danach.

### I. Die `.exe`, die Kinder-Welle und W4b-6 (22:35–23:10)

| Zeit | Schritt | Ergebnis / Beleg |
|---|---|---|
| 22:35 | **Erster `.exe`-Bau** | `tools/build_exe.py` → `Nebelseetal_Remake.exe` (13,4 MB, SHA256 `951ffccc…`), Symbol mit 6 Größen, `build/`, `dist/`, `.spec` danach entfernt — genau eine EXE im Projektordner |
| 22:36 | **Startprüfung 1: FEHLER gefunden** | die EXE startete, brach aber ab: `FileNotFoundError … Temp\data\gelaende.json`. Ursache: `gelaende`, `berater`, `welt`, `gebaeude_wirkung` und `main` leiten den Projektordner aus `__file__` ab — im PyInstaller-Paket zeigt das nicht auf den entpackten Ordner. **Fix:** EINE zentrale Wurzel-Suche in `spieldaten.projektwurzel()` (prüft `sys._MEIPASS`, den Exe-Ordner und den Quelltextordner der Reihe nach und nimmt den ersten, in dem wirklich `data/gelaende.json` liegt); alle fünf Module holen die Wurzel von dort |
| 22:42 | **Zweiter Bau + Startprüfung GRÜN** | Fenster „Nebelseetal Remake" (Kindprozess PID 2716), Sperrdatei mit derselben PID, **sauberes Schließen** über `CloseMainWindow` → Aufräumroutine greift, Sperrdatei weg; Start aus einem Pfad **mit Leerzeichen**; `tor.json` wurde vom Spiel **nicht** angelegt (Daniel setzt selbst) |
| 22:43 | **Daniel richtet das Tor selbst ein** | beim Ansehen des Startfensters das Passwort gesetzt (0 Fehlversuche, 04.10.2026 22:43) — der Erststartweg ist damit am ausgelieferten Programm erprobt |
| 22:45–22:50 | **Fünf Kinder, fünf neue Module** (nach `docs/AGENTEN_PLAN.md`, jedes mit eigener Prüfdatei) | `forschung_wirkung` (W4b-6, **94**) · `werkstatt` (W3, **118**, 1 Befund) · `portalraum` (W5-2, **69**) · `punkte` (W6, **76**) · `kampfbericht` (W2b, **108**) = **465 Prüfungen grün** |
| 22:50 | **Brett der Kinder erweitert** | `tools/brett.py`: **ein Eintrag = eine Datei** in `board/` (Postfach-Muster). Vorher schrieben alle in `docs/BOARD.md` — zwei Kinder gleichzeitig hätten sich überschrieben. Befehle: `lesen`, `belegen`, `melden`, `freigeben`, `luecken` |
| 22:58 | **W4b-6 eingehängt** | `main.RESEARCHES` sind jetzt die **21 Originalforschungen** aus `data/research.json` (vorher 18 erfundene Gebiete), und `bonus_system.get_production_multiplier` liefert die belegten Faktoren für **alle neun** Rohstoffe. Drei Prüfdateien mussten die Forschungsnamen mitziehen; `test_wirtschaft` erwartete außerdem den **erfundenen** Satz von +12 % und steht jetzt auf dem belegten **+10 %** (2,48 → 2,4) |
| 23:02 | **Gesamtlauf** | **1157 Prüfungen, 0 Fehler, 2 Befunde** über **achtzehn** Dateien (`run_tests.bat`, Rückgabewert 0) — im Sammellauf gemessen. Zu den 17 älteren Dateien kam `test_gebaeude_wirkung` (103) hinzu; sie schlug zuerst an, weil sie noch den alten Forschungsnamen benutzte, und war nach der Korrektur grün. Commit `c0f4a5d` |
| 23:05 | **Zweite Kinder-Welle gestartet** | Auftragssystem (WA), Menü-Vergleich (W7), robustes Speichern (W8), Fachschicht (alle Module für die Oberfläche gebündelt), Bot-Kern (W5) — Ergebnisse kommen als Meldung |
| 23:08 | **Kanban und Übergabe geführt** | Karte **W4b auf erledigt** gesetzt; die Karten W2b, W3, W5, W6, W7, W8, W9 haben ehrliche Zwischenmeldungen („Modul fertig, Einhängen offen"). Dazu `docs/FRAGEN_FUER_MORGEN.md` für Daniel |

**Ehrlich offen nach dieser Welle:** die Module für Waren, Kampf, Aufträge, Portal, Punkte, Speichern
und Bots sind **gebaut und geprüft**, aber `main.py` ruft sie noch nicht auf. Der nächste Schritt ist
das **Einhängen** (über die Fachschicht) und danach **ein Neubau der `.exe`**.

---

## Kosten

### Kosten der Nacht (22:15–23:10, gemessen)

| Schritt | Modell | Kosten |
|---|---|---|
| Passworttor, `.exe`-Bau, acht Kinder-Aufträge, W4b-6-Einhängung, Doku | `deepseek-v4-flash` (Standard, Hauptagent **und** Kinder) | **Tagessumme 9,96 → 10,41 USD** = **≈ 0,45 USD (0,40 EUR)** für alles seit 22:15 |

**Gemessen** über `tageskosten_check.py --json` (summiert über alle Profile): 22:15 = 9,96 USD /
8,87 EUR, 23:10 = 10,41 USD / 9,27 EUR. Enthalten ist jede Nutzung im Zeitfenster.
**Kein teures Modell im Einsatz:** `gpt-6-astra` wurde nicht gebraucht (keine Bilddeutung) und
`deepseek-v4-pro` ebenfalls nicht — die Kinder liefen auf dem Standardmodell.
**Guthaben (von Daniel abgelesen, 04.10. Nacht):** OpenAI **4,18 USD**, DeepSeek **2,60 USD**,
davon bleiben **1,00 USD** unangetastet (Daniels Vorgabe für Grundfunktionen).

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

**Sicherung (projektunabhaengig):** 14 Dateien gesichert nach `D:\Arbeiten\Hermes\Nebelseetal_Protokoll\2026-10-04_2302` — Vorgabe von Daniel am 04.10.2026, damit das Protokoll auch ohne diesen Projektordner weiterlebt. Zeiger auf die juengste Fassung: `D:\Arbeiten\Hermes\Nebelseetal_Protokoll\zuletzt.txt`.

**Sicherung (projektunabhaengig):** 14 Dateien gesichert nach `D:\Arbeiten\Hermes\Nebelseetal_Protokoll\2026-10-04_2303` — Vorgabe von Daniel am 04.10.2026, damit das Protokoll auch ohne diesen Projektordner weiterlebt. Zeiger auf die juengste Fassung: `D:\Arbeiten\Hermes\Nebelseetal_Protokoll\zuletzt.txt`.

**Sicherung (projektunabhaengig):** 14 Dateien gesichert nach `D:\Arbeiten\Hermes\Nebelseetal_Protokoll\2026-10-04_2304` — Vorgabe von Daniel am 04.10.2026, damit das Protokoll auch ohne diesen Projektordner weiterlebt. Zeiger auf die juengste Fassung: `D:\Arbeiten\Hermes\Nebelseetal_Protokoll\zuletzt.txt`.

**Sicherung (projektunabhaengig):** 14 Dateien gesichert nach `D:\Arbeiten\Hermes\Nebelseetal_Protokoll\2026-10-04_2307` — Vorgabe von Daniel am 04.10.2026, damit das Protokoll auch ohne diesen Projektordner weiterlebt. Zeiger auf die juengste Fassung: `D:\Arbeiten\Hermes\Nebelseetal_Protokoll\zuletzt.txt`.

**Sicherung (projektunabhaengig):** 17 Dateien gesichert nach `D:\Arbeiten\Hermes\Nebelseetal_Protokoll\2026-10-04_2311` — Vorgabe von Daniel am 04.10.2026, damit das Protokoll auch ohne diesen Projektordner weiterlebt. Zeiger auf die juengste Fassung: `D:\Arbeiten\Hermes\Nebelseetal_Protokoll\zuletzt.txt`.

---

## J. Selbstprüfung, Brett-Abbau und alle zehn Module (23:10–23:35)

| Zeit | Schritt | Ergebnis / Beleg |
|---|---|---|
| 23:12 | **Dritte Kinder-Welle zuerst abgebrochen** | Der erste Anlauf für Aufträge (WA), Menü-Vergleich (W7) und robustes Speichern (W8) wurde nach rund zwei Minuten abgebrochen — **ohne eine einzige Datei**. Die Übergabe behauptete zu diesem Zeitpunkt fälschlich „Modul liegt vor". **Richtiggestellt** und die drei Kinder neu gestartet; das versehentlich mitgeschickte fünfte Kind (Bot-Kern, schon fertig) sofort gestoppt und `src/botkern.py` als **unverändert** nachgeprüft |
| 23:16 | **Auftragssystem (WA)** | `src/auftraege.py` + Prüfdatei: **111 bestanden, 0 Fehler, 1 Befund** — von mir selbst gelaufen, nicht geglaubt |
| 23:18 | **Robustes Speichern (W8)** | `src/speichern.py` + Prüfdatei: **95 bestanden, 0 Fehler, 5 Befunde** (ehrlich: keine Dateisperre gegen zwei Schreiber, Klartext, kein Verzeichnis-Sync) |
| 23:19 | **Menü-Vergleich (W7) — echter Fehler gefunden** | `src/oberflaeche_original.py`: **63 grün, 1 rot**. Der Kind-Test suchte das Wort „tkinter" auch in der *Beschreibung* des Moduls und schlug deshalb an. Die Prüfung verlangt jetzt einen echten Import → **64 grün**. Belegt: verlässlich ist die Prüfzahl des Koordinators, nicht die Meldung des Kindes |
| 23:22 | **Brett der Kinder wieder entfernt** (Vorgabe Daniel) | `tools/brett.py` und `board/` gelöscht; die Anweisungen aus `docs/AGENTEN_PLAN.md`, Übergabe und Skill entfernt. Grund: ein Kinder-Brett ist eine **zweite Wahrheit** — es kann „fertig" melden, während die eigene Prüfdatei rot ist (genau am Menü-Modul passiert). `docs/BOARD.md` bleibt als **Tagebuch des Koordinators für Daniel**. Das **Spiel-Postfach** (Reiter „Nachrichten") ist unberührt — nachgeprüft |
| 23:25 | **Selbstprüfung — Fehler in meiner eigenen Prüfung** | Meine Prüfkette nutzte `grep -c`; bei 0 Treffern bricht `&&` ab, dadurch liefen zwei Prüfungen **gar nicht**, obwohl es nach Erfolg aussah. Nachgeholt: keine `brett`-Reste außerhalb dieser Chronik, **kein** `main`-Import in den neuen Modulen, `data/menue_original.json` gültig (15 Einträge), `botkern.handelspreis(referenzpreis, temperament)` bestätigt |
| 23:30 | **Zehn Kind-Module, 958 Prüfungen** | 94 + 118 + 69 + 76 + 108 + 133 + 90 + 95 + 64 + 111 = **958**, jedes einzeln von mir nachgerechnet und in `run_tests.bat` aufgenommen (jetzt **23 Dateien**). Commit `f48e9d2` |
| 23:32 | **Guthaben (von Daniel abgelesen)** | OpenAI **4,08 USD** (Reihe 8,89 → 5,56 → 4,18 → 4,08) · DeepSeek **2,08 USD** (Reihe 3,32 → 2,60 → 2,08). Über der von Daniel gewünschten 1,00-USD-Marke bleiben bei DeepSeek **1,08 USD** → ab hier sparsamer, Kinder nur noch für klar abgegrenzte Bausteine |

**Stand nach Abschnitt J:** alle zehn Kind-Module sind gebaut **und vom Koordinator nachgerechnet**;
kein Brett der Kinder mehr. **Nächster Schritt bleibt das Einhängen** über `src/spielschicht.py` in
`main.py` und danach ein **Neubau der `.exe`**.

---

## K. Teure Modelle gezielt eingesetzt (23:35–23:50)

**Vorgabe von Daniel:** „Nimm Astra für wichtige Umsetzung des Spiels … fehlerfreie Kampfabläufe und
schöne und gut durchdachte Karten … aber immer genau durchdachte und gezielte Anweisungen auf Kosten
bezogen berechnet: meiste Leistung für geringste Ausgabe."

| Zeit | Schritt | Ergebnis / Beleg |
|---|---|---|
| 23:38 | **Guthaben abgelesen (Daniel)** | OpenAI **4,08 USD** · DeepSeek **2,08 USD**. Tagesmessung vor den teuren Aufrufen: **10,92 USD / 9,73 EUR** (`scripts/tageskosten_check.py --json`, lage `UEBER_LIMIT` — die 4-EUR-Regel ist für diesen Auftrag von Daniel ausgesetzt) |
| 23:40 | **Sammellauf mit allen 23 Dateien** | **1651 bestanden, 0 Fehler, 9 Befunde**, Rückgabewert 0 — jetzt der verbindliche Prüfstand |
| 23:42 | **Modellwahl nach Hauslehre, nicht nach Gefühl** | `docs/LEHREN.md` §6 hält fest: `deepseek-v4-pro` lieferte für **0,12 USD** dieselbe Qualität wie `gpt-6-astra` für **1,27 USD** — bei Textarbeit. Deshalb: **astra nur für die Bilder** (Kartenentwurf aus den Original-Screenshots), **v4-pro für den Umsetzungs- und Kampfplan** (Text) |
| 23:44 | **Zwei gezielte Einzelaufrufe statt Agentenschleifen** | Je EIN `hermes -z`-Aufruf mit festem Zeitlimit (15 bzw. 20 Minuten), Werkzeuge auf das Nötigste begrenzt (`-t vision,file` bzw. `-t file`), Auftrag vorher in eine Datei geschrieben und wortgenau übergeben. Damit kann kein teures Modell in Erkundungsschleifen Geld verbrennen. Eine Änderung der Voreinstellung für Unteragenten (`delegation.model`) wurde **vom Sicherheitsschutz blockiert** — zu Recht; der Einzelaufruf ersetzt sie ohne Systemeingriff |
| 23:45 | **Aufträge** | astra → `docs/KARTEN_ENTWURF.md` + Rohantwort in `docs/audits/astra_karten.txt`; v4-pro → `docs/UMSETZUNG_EINHAENGEN.md` (Einhänge-Liste, Kampfablauf mit allen Fehlerfällen, Kartenansicht, Speichern, Arbeitsreihenfolge mit erwarteten Prüfzahlen) |

**Kostenregel für die teuren Aufrufe:** nach dem Lauf wird sofort gemessen (`tageskosten_check.py`)
und die Differenz ins Protokoll geschrieben. Bei DeepSeek müssen **1,00 USD liegen bleiben**.

### Ausgang der beiden teuren Aufrufe

| Zeit | Aufruf | Ergebnis |
|---|---|---|
| 23:52 | **astra (Bilder, Kartenentwurf) — fertig, Rückgabewert 0** | Geschrieben: `docs/KARTEN_ENTWURF.md` (48 Zeilen, jede Aussage als `[BELEGT: Foto …]` oder `[VORSCHLAG]`) und `docs/audits/astra_karten.txt`. **Der Befund ist negativ und wertvoll: auf keinem der drei GameStar-Fotos ist eine Siedlungskarte zu sehen** — Foto 1 Nachrichtenansicht, Foto 2 **Portal**ansicht (das 20×20-Raster gehört dorthin), Foto 3 Baumenü. Das frühere astra-Gutachten (21:0x) war unabhängig zum selben Ergebnis gekommen → unsere Siedlungskarte ist **eigene Gestaltung**, kein Originalbeleg. Zusätzlich fand astra einen **echten Widerspruch in unseren Daten** (`data/gelaende.json`: 8×5 = 40 Felder *und* 56 Felder), vom Koordinator nachgerechnet und als Frage 12 vorgelegt. **Kosten dieses Aufrufs: +0,67 USD** (Messung 10,92 → 11,59 USD unmittelbar danach) — im Rahmen des Veranschlagten (1,27 USD aus dem letzten Mal) |
| — | **v4-pro (Umsetzungs- und Kampfplan)** | schreibt noch; Ergebnis und Kosten werden nachgetragen |

**Sicherung (projektunabhaengig):** 12 Dateien gesichert nach `D:\Arbeiten\Hermes\Nebelseetal_Protokoll\2026-10-04_2324` — Vorgabe von Daniel am 04.10.2026, damit das Protokoll auch ohne diesen Projektordner weiterlebt. Zeiger auf die juengste Fassung: `D:\Arbeiten\Hermes\Nebelseetal_Protokoll\zuletzt.txt`.

**Sicherung (projektunabhaengig):** 12 Dateien gesichert nach `D:\Arbeiten\Hermes\Nebelseetal_Protokoll\2026-10-04_2324` — Vorgabe von Daniel am 04.10.2026, damit das Protokoll auch ohne diesen Projektordner weiterlebt. Zeiger auf die juengste Fassung: `D:\Arbeiten\Hermes\Nebelseetal_Protokoll\zuletzt.txt`.

**Sicherung (projektunabhaengig):** 12 Dateien gesichert nach `D:\Arbeiten\Hermes\Nebelseetal_Protokoll\2026-10-04_2339` — Vorgabe von Daniel am 04.10.2026, damit das Protokoll auch ohne diesen Projektordner weiterlebt. Zeiger auf die juengste Fassung: `D:\Arbeiten\Hermes\Nebelseetal_Protokoll\zuletzt.txt`.
