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

## Wie dieses Protokoll geführt wird

- **Nur anhängen**, nie rückwirkend umschreiben. (Einzige Ausnahme: die Verdichtung vom 04.10.2026
  auf Daniels Wunsch — Zahlen, Entscheidungen, Fehler und Lehren blieben dabei vollständig erhalten.)
- **Eine Zeile je grobem Schritt**: Zeit · Schritt · Ergebnis mit **echter** Zahl oder Commit.
- **Fehler und Irrwege gehören hinein** — mit der Lehre daraus, nicht beschönigt.
- **Kein „Stand"-Abschnitt pro Etappe**: neue Prüfstände sind eine Zeile in der Meilenstein-Tabelle.
- **Sicherungen stehen nicht hier**, sondern in `docs/SICHERUNGEN.md` (maschinell geführt).
- **Kosten nur gemessen** und mit Messmethode; Schätzung wird als Schätzung gekennzeichnet. Ein
  Kostenabschnitt, nicht mehrere.
- **Zielgröße: deutlich unter dem heutigen Umfang** (Verdichtung vom 04.10.2026: 364 -> 300 Zeilen). Wächst es darüber, wird verdichtet — nie auf Kosten von Inhalt.

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

## Kosten (gemessen, nicht geschätzt)

**Regel:** nur belegte Beträge. Tagesdifferenz über `scripts/tageskosten_check.py --json`, einzelne
Modellaufträge über den Anbieter. Schätzungen sind als Schätzung gekennzeichnet.

| Zeitraum / Schritt | Modell | Kosten |
|---|---|---|
| 22:15–23:10: Passworttor, `.exe`-Bau, Kinder-Wellen, W4b-6, Doku | `deepseek-v4-flash` (Standard) | **≈ 0,45 USD** (Tagessumme 9,96 → 10,41 USD, gemessen) |
| W4b-5 (Wirkungsmodul + Einhängen + 103 Prüfungen) | Standard | **≈ 0,06 EUR** (Differenz 8,81 → 8,87 EUR, gemessen) |
| Kartenentwurf aus den Original-Screenshots (23:35) | `gpt-6-astra` | **0,67 USD** (10,92 → 11,59 USD, gemessen) |
| Umsetzungs- und Kampfplan (23:35) | `deepseek-v4-pro` | **0,12 USD** (Anteil) |
| **Beide teuren Aufrufe zusammen** | astra + v4-pro | **+0,79 USD** (10,9244 → 11,71 USD) |
| **05.10. 23:49–00:32: Schritte 1–3 und 6 einhängen (Speichern, Punkte, Kampf, Portal) + drei Verdrahtungs-Prüfdateien** | `deepseek-v4-flash` (Koordinator) + `flash`-Unteragenten — **kein** teurer Aufruf | **0,1928 USD = 0,1718 EUR** (Tagessumme 05.10. bis 00:32, `scripts/tageskosten_check.py --json`: 4 Sitzungen, Modelle `deepseek-flash`/`deepseek-v4-flash`; Kurs 0,89087) |
| **05.10. 00:31: Rat des teuren Modells an den Koordinator** (auf Daniels Wunsch, Frage und Antwort in `docs/audits/`) | `gpt-6-astra` | **0,3444 USD** (Differenz 0,1928 → 0,5372 USD, gemessen) — **ein** Umlauf ohne Werkzeuge, 1 min 47 s; Tagessumme danach **0,5372 USD = 0,4786 EUR** |

**Bezahlte Modellaufträge am 04.10.2026 (Tagesverlauf, vor dieser Sitzung):**

| Auftrag | Modell | Kosten |
|---|---|---|
| Kampf-Audit gegen das Handbuch | gpt-6-astra | 0,43 USD |
| Konformitäts-Audit über 24 Handbuchseiten | gpt-6-astra | ~0,78 USD |
| Wirtschaftsentwurf | gpt-6-astra | ~0,80 USD |
| vier Website-Bilder gedeutet | gpt-6-astra | ~0,30 USD |
| Farbwelt aus vier Bildern | gpt-6-astra | ~0,20 USD |
| drei GameStar-Screenshots gedeutet (brachte die **echten Baupreise**) | gpt-6-astra | 0,47 USD |
| Auftrags- und Bot-System-Entwurf | deepseek-v4-pro | 0,12 USD |
| zwei Siedlungskarten-Vorlagen | deepseek-v4-pro | 0,04–0,12 USD |

**Summe der astra-Einzelposten:** ~2,98 USD (sechs Aufträge) · **gemessen 3,33 USD** Verbrauch am
04.10. über `/v1/organization/costs?group_by=line_item` (der **Tageswert** der Ausgaben-API ist
unbrauchbar, er aktualisiert in Schüben — daher früher falsche Zahlen).
**Kontostände:** 8,89 → 5,56 → 4,18 → **4,08 USD** (OpenAI) · 3,32 → 2,60 → **2,08 USD** (DeepSeek),
alle von Daniel abgelesen. **Auto-Recharge ist aus** — es können keine Schulden entstehen.
Bei DeepSeek bleiben 1,00 USD Reserve (Daniels Vorgabe); aktuell 1,08 USD darüber.

**Teuerste Einzelheit (Lehre):** bei `gpt-6-astra` sind die **Cache-Schreibkosten** der größte Posten
(3,56 USD gegen 0,94 USD Ausgabe) — dieselbe lange Auftragsformulierung wiederholt sich teuer. Deshalb:
Aufträge kurz halten, Formulierungen wiederverwenden, **Bilder nur an astra** (seine Stärke),
Textarbeit an `deepseek-v4-pro` (gleiche Qualität zum Zehntelpreis, siehe `docs/LEHREN.md` §6).

**Zur 4-EUR-Tagesregel:** der Tag liegt weit darüber; für den Auftrag „Nebelseetal Remake so gut wie
möglich" hat Daniel die Regel ausgesetzt (Skill `kosten-schutzregel`, laufende Ausnahme).

## Meilensteine (Prüfstand-Verlauf)

Die jeweils **gemessenen** Sammelläufe; Details in `docs/PROJEKT_STAND.md` und im Git-Verlauf.
Jeder neue Prüfstand kommt hier als **eine Zeile** dazu — kein eigener „Stand"-Abschnitt mehr.

| Zeit (04.10.2026) | Prüfstand | Was erreicht wurde | Commit |
|---|---|---|---|
| 15:36 | **526** / 11 Dateien, 0 Fehler | Sicherheitsnetz, erste Belege, Rohbau | `472704f` |
| 22:15 | **630** / 12, 0 Fehler, 1 Befund | **W4b-5**: die 20 Originalgebäude wirken aus den bebauten Feldern | `a158175` |
| 22:34 | **691** / 13, 0 Fehler | **Passworttor** (PBKDF2) + `tools/build_exe.py` | — |
| 23:02 | **1157** / 18, 0 Fehler, 2 Befunde | **W4b-6**: 21 Originalforschungen, Faktoren für alle neun Rohstoffe | `c0f4a5d` |
| 23:40 | **1651** / 23, 0 Fehler, 9 Befunde | **zehn Kind-Module** fertig und nachgerechnet; Brett der Kinder abgeschafft | `f48e9d2` |

Die zwei Befunde der Frühphase sind ehrlich und bekannt: (1) das Handbuch nennt keine
Ausbildungsdauer, deshalb senkt die Stufe einer Ausbildungsstätte noch nichts messbar; (2) `werkstatt`
meldet eine Lücke in den Waren-Regeln, die das Handbuch offen lässt.

**Offen und neu entdeckt:** `src/forschung.py` (Wartezeit) und der Portalraum sind fertig geprüft,
aber noch **nicht eingehängt** — die Forschungsstufe steigt noch im selben Klick, im Portal steckt
noch das alte `MAPS`-Modell.

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
| 23:38 | **astra (Bilder, Kartenentwurf) — fertig, Rückgabewert 0** | (Logdatei um 23:38 vollständig geschrieben, Fertigmeldung kam später) Geschrieben: `docs/KARTEN_ENTWURF.md` (48 Zeilen, jede Aussage als `[BELEGT: Foto …]` oder `[VORSCHLAG]`) und `docs/audits/astra_karten.txt`. **Der Befund ist negativ und wertvoll: auf keinem der drei GameStar-Fotos ist eine Siedlungskarte zu sehen** — Foto 1 Nachrichtenansicht, Foto 2 **Portal**ansicht (das 20×20-Raster gehört dorthin), Foto 3 Baumenü. Das frühere astra-Gutachten (21:0x) war unabhängig zum selben Ergebnis gekommen → unsere Siedlungskarte ist **eigene Gestaltung**, kein Originalbeleg. Zusätzlich fand astra einen **echten Widerspruch in unseren Daten** (`data/gelaende.json`: 8×5 = 40 Felder *und* 56 Felder), vom Koordinator nachgerechnet und als Frage 12 vorgelegt. **Kosten dieses Aufrufs: +0,67 USD** (Messung 10,92 → 11,59 USD unmittelbar danach) — im Rahmen des Veranschlagten (1,27 USD aus dem letzten Mal) |
| — | **v4-pro (Umsetzungs- und Kampfplan)** | **fertig, Rückgabewert 0**: `docs/UMSETZUNG_EINHAENGEN.md` (352 Zeilen, 22,5 KB) — 1.0 Datenmodell-Abweichung (main.py = Datenklassen, Module = dict; Brücke `_als_dict`/`_aus_dict`), 1.1–1.9 je Modul die konkreten Aufrufstellen, 2 Kampfablauf mit allen fünf Fehlerfällen samt wörtlichen Meldungen, 3 Kartenansicht (laut Plan **kein** Umbau nötig), 4 Umstellung auf `speichern` (`main.py:627-628`), 5 Arbeitsreihenfolge mit erwarteten Prüfzahlen. **Beide teuren Aufrufe zusammen: +0,79 USD** (Messung 10,9244 → 11,71 USD) — deutlich unter dem Veranschlagten (1,39 USD) |
| 23:42 | **Kontrolle durch den Koordinator** | Die drei „unklar"-Stellen des Plans aufgeklärt und in Abschnitt 6 des Plans nachgetragen (auftraege **111**, botkern **90**, Gesamt **1651/23**); bestätigt, dass der direkte Schreibort wirklich `main.py:627-628` ist. Startzeile in der Übergabe auf den Plan umgestellt. **Eigener Fehler dabei gefunden und behoben:** zwei Zeitangaben („00:05", „05.10.") waren geschätzt statt geprüft — `date` sagt 04.10.2026, 23:42, alle drei Stellen korrigiert |

---

## Sitzungswechsel (04.10.2026, 23:47 — Uhrzeit mit `date` geprüft)

**Auftrag von Daniel:** „fertig machen zum Session-Wechsel" und „trage den Sessionwechsel in das
Protokoll ein". Diese Sitzung endet hier sauber; die nächste macht genau an dieser Stelle weiter.

**Zustand beim Wechsel — jeder Punkt mit Beleg, nichts geschätzt:**

| Punkt | Beleg |
|---|---|
| Arbeitsverzeichnis | **sauber**, letzter Commit `c329893` (`git status` leer). Der Sitzungswechsel-Eintrag selbst ist Commit `3ec1fca`, davor `0206e8a` |
| Prüfstand | **1651 bestanden, 0 Fehler, 9 Befunde** über 23 Dateien, `run_tests.bat` Rückgabewert **0**, gemessen 04.10.2026 23:40 |
| Nichts läuft | kein Hintergrundprozess, kein Unteragent, kein offenes Fenster (nachgeprüft) |
| Zehn Kind-Module | fertig und **vom Koordinator nachgerechnet**: 94 + 118 + 69 + 76 + 108 + 133 + 90 + 111 + 95 + 64 = **958** — aber **nicht eingehängt** |
| Auslieferung | `Nebelseetal_Remake.exe`, 14.024.744 Byte, mit Passworttor startgeprüft (04.10. 22:42) |
| Papiere gesichert | `D:\Arbeiten\Hermes\Nebelseetal_Protokoll\2026-10-04_2346` — 14 Dateien, SHA256 je Datei im `MANIFEST.txt` geprüft; Zeiger `zuletzt.txt` |
| Kosten der Sitzung | teure Aufrufe zusammen **+0,79 USD** (astra für die Bilder, v4-pro für den Plan). Guthaben: OpenAI **4,08** · DeepSeek **2,08** USD — die von Daniel gewünschte 1,00-USD-Reserve ist unberührt |
| Offene Fragen | **13** an Daniel, in `docs/FRAGEN_FUER_MORGEN.md` |

**Was die neue Sitzung NICHT neu prüfen muss:** `docs/PROJEKT_STAND.md`, Abschnitt 0b, Tabelle
„Nicht erneut zu prüfen". Es genügt der Sekunden-Check (`git log --oneline -3`, `git status --short`) —
der Sammellauf wird erst nach der ersten echten Änderung an `src/` wiederholt.

**Der eine nächste Schritt:** `src/speichern.py` einhängen in `main.py:608-634` (das direkte Schreiben
steht in Zeile **627-628**); danach `tests/test_speichern_robust.py` → **95 grün** und
`tests/test_baseline.py` → **40 grün**. Der vollständige Plan steht in `docs/UMSETZUNG_EINHAENGEN.md`,
Abschnitte 4 und 5; die Startzeile in `docs/PROJEKT_STAND.md`, Abschnitt 0.

**Neue Hausregel aus dieser Sitzung:** Übergaben werden nach dem Skill `uebergabe-handoff` geschrieben —
Stand in Belegen, **der eine** nächste Schritt mit `Datei:Zeile` und erwarteter Prüfzahl, eine
„nicht erneut zu prüfen"-Tabelle, Sekunden-Checks statt Sammellauf. Dazu gehört auch: **keine halbe
Änderung hinterlassen** — lieber sauber enden als `main.py` halb umgebaut übergeben.

---

## 05.10.2026 — Tag 2: die zehn Module in die Oberfläche einhängen (Fortsetzung, ab 04.10. 23:49)

**Auftrag von Daniel (Startzeile + Zuruf um 00:0x):** die Arbeitsreihenfolge aus Abschnitt 5 von
`docs/UMSETZUNG_EINHAENGEN.md` abarbeiten — Schritt 1 ist `speichern` an `main.py:627-628` —, nach
jedem Schritt `run_tests.bat` und eine Protokollzeile, am Ende die `.exe` neu bauen und startprüfen.
Nachträglich: das Ziel selbstständig weiterverfolgen, Aufgaben sinnvoll delegieren, Ergebnisse
wiederholt prüfen, sparsam mit den teuren Modellen. Guthaben bei Übernahme (Daniel, 00:0x):
DeepSeek **1,70 USD**, OpenAI **3,04 USD** — deshalb **keine** teuren Aufrufe (kein astra, kein v4-pro)
und nur `flash`-Unteragenten.

**Nebenbefund beim Start (ehrlich vermerkt):** zwischen 23:47 und 23:50 sind noch zwei Commits der
Vorgängersitzung eingetroffen (`5f7ee39`, `4bf6a45` — beide nur `docs/`), während diese Sitzung schon
lief. Sie wurden **nicht** überschrieben, sondern gelesen; `main.py` trägt ausschließlich die eigenen
Änderungen (Beleg: `git diff --stat src/main.py` = 42 Einfügungen, 9 Löschungen).

**Daniels Input in dieser Sitzung.** Belegte Uhrzeit gibt es nur für den Sitzungsbeginn (23:49, `date`);
die Chat-Zurufe stehen ohne Uhrzeit im Verlauf und sind deshalb **in der Reihenfolge** gelistet.

| Nr. | Zeit (Beleg) | Input |
|---|---|---|
| 1 | 23:49 (04.10.), `date` | **Startauftrag** (wörtlich in `docs/PROJEKT_STAND.md`, Abschnitt 0): Ziel übernehmen, dann die Arbeitsreihenfolge aus `docs/UMSETZUNG_EINHAENGEN.md`, Abschnitt 5, abarbeiten — Schritt 1 ist `speichern` an `main.py:627-628` —, nach jedem Schritt `run_tests.bat` (erwartet 1651/0/9 über 23 Dateien) und eine Protokollzeile; am Ende die `.exe` neu bauen und startprüfen |
| 2 | während Schritt 1 | „ich möchte dass du das Ziel nun selbstständig weiter verfolgst, bitte delegier die aufgaben sinnvoll und arbeite effektiv. Prüfe immer wieder deine ergebnisse, arbeite sauber effizient und klug mit teuren modellen" + Kontostände: DeepSeek **1,70 USD**, OpenAI **3,04 USD** |
| 3 | während Schritt 1 | „viel erfolg bei der zielerfüllung" |
| 4 | nach Commit `9ec34fb` (00:03) | „beachte das du das protokoll sinnvoll weiterführst" |
| 5 | nach Commit `b14f7f5` (00:25) | „halte das entwicklungsprotokoll übersichtlich und schlank und sinnvoll" |
| 6 | während Schritt 6 (00:26) | „Wichtig ist: Wann haben wir es getan, was war mein Input und was deiner, was haben wir grob vor gehabt bis hin zu das kam dabei heraus … inklusive Kosten und Ausgaben die real passiert sind mit Belegen und Zeitstempel" |

**Mein Vorgehen (Koordinator, damit es nachvollziehbar bleibt):** Ausgangsmarke **selbst messen** statt
aus der Übergabe abschreiben · jede Änderung mit einer **eigenen** Nachprüfung nach anderem Verfahren als
der Kind-Test · `main.py` nur selbst anfassen, `flash`-Unteragenten nur für **neue** Prüfdateien · nach
jedem Schritt Sammellauf, Protokollzeile, projektunabhängige Sicherung, kleiner Commit · kein teurer Aufruf.

| Zeit | Schritt | Ergebnis / Beleg |
|---|---|---|
| 23:52 | **Ausgangsmarke gemessen** (nicht aus der Übergabe abgeschrieben) | 23 Prüfdateien in der Bash nachgefahren — `run_tests.bat` endet mit `pause` und läuft ohne Tastatur nicht durch, deshalb ein eigenes Laufskript (`nebel_suite.py`, liest die Dateiliste aus `run_tests.bat`): **1651 bestanden, 0 Fehler, 9 Befunde über 23 Dateien**, Rückgabewert 0 (Laufprotokoll 23:52:49). Deckt sich mit der Übergabe — keine Abweichung |
| 23:55 | **1 · W8 Speichern** (`main.py:627-628`, Änderung 23:55:29) | statt direktem `json.dump`/`json.load` jetzt `speichern.sichere_kopie` + `speichere` (geprüfte `.tmp`, dann `os.replace`) und im Lesen `lade` + `wiederherstellen` aus `.bak`; `aufraeumen` beim Start; `_save`/`_load` melden den ehrlichen Ausgang |
| 23:56 | **Nachprüfung (eigenes Verfahren, nicht der Kind-Test)** | `nebel_w8_probe.py` **7 Proben**: Sicherung trägt den **alten** Stand · Wiederherstellung nach Beschädigung · ehrliches `False` bei unmöglichem Ziel · keine `.tmp`-Leiche · altes Dateiformat lädt weiter |
| 00:00–00:02 | **Kind-Test, Grundprüfung, Sammellauf** | speichern **95/0/5** · baseline **40/0/0** · Sammellauf **1651/0/9** über 23 Dateien (Laufprotokoll 00:01:52) — unverändert grün |
| 00:00–00:21 | **Unteragenten beauftragt (flash)** | je eine neue Prüfdatei für die **Verdrahtung** (Einzelheiten am Ende des Abschnitts); Dateizeitstempel 00:00:50 / 00:13 / 00:21:30 |
| 00:03 | **1 · W8 Speichern abgeschlossen** | Commit `9ec34fb` (00:03:07); Papiere gesichert (16 Dateien, Prüfsummen gleich) |
| 00:05–00:10 | **2 · W6 Punkte** | Seitenleiste und Ruhmeshalle rechnen mit `punkte.*` (Stufe³ · Einheitenwerte + Wallstufe³ · halbe Summe) statt `score`/`ruf`; eigener Nachweis `nebel_w6_probe.py` **6 Proben** (00:04:08) · `test_punkte.py` **76/0/0** · Sammellauf **1651/0/9** (00:09:58) |
| 00:11–00:18 | **3 · W2/W2b Kampf** | beide Daumenangriffe ersetzt durch **einen** Weg: `_truppen_nach_rolle` → `kampf.fuehre_schlacht` → `kampfbericht.spieldaten_anwenden` → Bericht in den Reiter Nachrichten; eigener Nachweis `nebel_w2_probe.py` **7 Proben** (00:13:50) · Sammellauf **1651/0/9** (00:18:01) |
| 00:24 | **Schritte 1–3 festgeschrieben** | Commit `b14f7f5` (00:24:46): Punkte + Kampf + die zwei fertigen Verdrahtungs-Prüfdateien; Sammellauf mit den neuen Dateien **1734/0/14 über 25 Dateien** (Laufprotokoll 00:24:18) |
| 00:26–00:29 | **6 · W5-2 Portalraum** | `import portalraum`; der Portalreiter zeigt jetzt das **20×20-Raster** des Limbus (eigene Dimension grün, fremde rot — belegter Wortlaut), 20 Dimensionsknöpfe, Mana, Festpreis und Sperre; der Koordinatenwechsel prüft über `portalraum.wechsel_erlaubt`, bucht über `nach_wechsel` **genau einmal** 5.000 Mana ab und sperrt 24 h. Neue Zustandsfelder `eigene_dimension`/`eigene_dimensionen`/`letzter_wechsel` werden mitgespeichert. Die alte Kartenliste im Portalreiter ist ersetzt (Plan §1.6), die Bot-Liste bleibt. Sammellauf **1776 bestanden, 0 Fehler, 14 Befunde über 26 Dateien** (Laufprotokoll 00:28:58) |
| 00:26 | **Nachprüfung Schritt 6** | `nebel_w5_probe.py` **7 Proben**: Ansicht rendert · **400 Felder** im Raster · ohne Mana ehrlich abgelehnt ohne Änderung · mit Mana genau 5.000 abgebucht · zweiter Wechsel in der Sperre **ohne** zweite Abbuchung · nach 25 h wieder möglich · Portalzustand übersteht Speichern/Laden |

| 00:31 | **Teurer Aufruf auf Daniels Wunsch: `gpt-6-astra` um Rat gefragt** | Frage wortgetreu in `docs/audits/eingaben/astra_frage_koordinator.txt`, Antwort wortgetreu in **`docs/audits/astra_koordinator_rat.txt`** (47 Zeilen, Lauf 1 min 47 s, Sitzung `20261005_003107_da3e92`). Daniels Auftrag: worauf der Koordinator mit `flash` am meisten achten muss, welche Skills/Checklisten helfen, und wie der **Kontext** aufgebaut sein muss, damit trotz schwachem Modell möglichst wenig schiefgeht. **Kosten gemessen: 0,3444 USD** (Tagessumme vor dem Aufruf 0,1928 → danach **0,5372 USD**, `tageskosten_check.py --json`) |
| 00:33 | **Was astra rät — sofort umgesetzt** | (a) **Nur eine Spieleraktion je Commit**, keine fremde Aufräumarbeit; (b) jede Einhängung mit **Rückruf-Vertrag** beginnen (Eingaben, Modulaufruf, veränderte Felder, Verhalten bei Ablehnung, Anzeige-Auffrischung, Speicherung) und **vor** jeder Änderung ablehnen, was nicht erfüllt ist; (c) **Verdrahtungsinventar** führen (Modul → Funktion → Aufrufer → erreichbare Aktion → geprüft) — Unteragent `tools/pruefe_verdrahtung.py` beauftragt; (d) **stille tkinter-Fehler laut machen** (`root.report_callback_exception`) — Unteragent `tests/test_gui_fehler.py` beauftragt; (e) Kontext klein halten: vollständiges `main.py` und ganze Testprotokolle **nicht** in den Kontext, Belege auf der Platte; (f) Berichte an Datei-Prüfsummen binden; (g) `.exe` aus einem **anderen Ordner** starten und dort Speichern/Laden prüfen |

| 00:41–00:52 | **5 · W3 Werkstatt und Waren** | `import werkstatt`; das Lager zeigt jetzt die **17 Originalwaren** aus `data/items.json` mit ihren **Original-Icons** (statt der erfundenen Emoji-Liste) und darunter die Werkstätten. Eine Werkstatt entsteht nur aus einem **wirklich bebauten Feld** (`werkstatt.werkstaetten_bestand`); je Ware steht die **belegte Voraussetzung** (Forschung + Stufe) am Knopf — ohne sie wird **vor** jeder Änderung abgelehnt. Warteschlangen und fertige Waren laufen über `neu_warteschlange`/`einreihen`/`fertige_waren`, der Zeitlauf bucht Fertiges **genau einmal** ins Lager. Warenlager und Warteschlangen werden mitgespeichert |
| 00:45 | **Nachprüfung Schritt 5** | `nebel_w3_probe.py` **9 Proben**: 17 Waren ohne Werkstatt · Schmiede auf der Karte gebaut ⇒ genau eine Schlange · Ansicht zeigt Werkstatt und Warenknöpfe · **Voraussetzung greift** („Waffentechnik Stufe 5 noetig, vorhanden ist Stufe 0", nichts eingereiht) · Ware **ohne belegte Dauer** wird ehrlich als wartend geführt und wird nie fertig · Schwert (20 min) kommt **genau einmal** an · fremde Werkstatt ehrlich abgelehnt · Lager und Schlange überstehen Speichern/Laden · `GameState.tick` bucht selbst |
| 00:47 | **Schritt 5 geprüft** | Sammellauf **1776 bestanden, 0 Fehler, 14 Befunde über 26 Dateien** (Laufprotokoll 00:47:18) — unverändert grün |
| 00:38–00:42 | **Die beiden astra-Aufträge sind gebaut und nachgeprüft** | `tools/pruefe_verdrahtung.py` (Unteragent `flash`): Textbeweis aus `main.py` — **13 verdrahtet, `botkern` nur importiert, `auftraege`/`forschung`/`welt` nicht eingebunden**, Rückgabewert 1; keine doppelte Funktionsdefinition. Es meldete außerdem acht `player_power`-Treffer: **sechs davon sind echte Reste** im **Kampfsimulator** (`_render_battle_simulator`, `_simulate_random_battle` rechnen noch mit `get_combat_power`, dem alten erfundenen Weg), **zwei waren ein Fehlalarm durch meinen eigenen Kommentar** (Kommentar umformuliert). `tests/test_gui_fehler.py` (Unteragent `flash`): **22/0/1** — **18 Ansichten und 13 Aktionen ohne Fenster geprüft, 0 echte Rückruf-Fehler**; der Sammler für stille tkinter-Fehler wurde mit einem absichtlich kaputten Knopf bewiesen. Beide vom Koordinator selbst nachgefahren; die Prüfdatei ist in `run_tests.bat` aufgenommen (Gesamtzahl steigt auf **1798 über 27 Dateien**) |
| 00:52 | **Neuer offener Punkt aus dem Verdrahtungsbeweis** | Der **Kampfsimulator** ist der letzte Ort mit einer erfundenen Kampfformel (`get_combat_power`). Er gehört als eigener kleiner Schritt auf `kampf.fuehre_schlacht` umgestellt (der Original-Menüpunkt heißt „Schlachtsimulator"); angriffslos, ohne Spielstandänderung. Steht als nächster kleiner Schritt im Plan |

**Offene Punkte aus dieser Sitzung (ehrlich):**

- Angriffe auf **Bots** sind mit den heutigen Armeen (20–120 Stück **je Einheit**, alter Code, **nicht** aus
  dem Handbuch) praktisch aussichtslos; echte Bot-Stärken und echtes Bot-Lager gehören zu Schritt 8 (botkern).
- Die Vorräte eines Ziels kommen bis dahin aus den **VORSCHLAG**-Spannen in `botkern` (dort als Vorschlag
  gekennzeichnet); für **Kartenangriffe** gibt es kein belegtes Lager → Frage an Daniel.
- **Portal (Schritt 6):** unser Mana liegt in **einem** gemeinsamen Vorrat, das Handbuch verlangt die
  5.000 Mana **aus einer Siedlung** — im Spiel steht dieser Hinweis sichtbar in der Ansicht, sauber wäre
  ein Manavorrat je Siedlung (steht auch in `spielschicht.offene_luecken()`). Die **Startdimension 1** ist
  ein VORSCHLAG; das Handbuch nennt keine.

**Unteragenten** (flash, je eine **neue** Prüfdatei, die ausschließlich die **Verdrahtung** prüft — nie
die Module selbst; sie committen nicht, der Koordinator prüft nach): `test_w8_einhaengung.py` **39/0/5**,
`test_punkte_einhaengung.py` **44/0/0** und `test_kampf_einhaengung.py` **42/0/0** — alle drei vom
Koordinator selbst nachgefahren und inhaltlich geprüft, alle drei in `run_tests.bat` aufgenommen. Der
Sammellauf steht dadurch bei **1776 bestanden, 0 Fehler, 14 Befunde über 26 Dateien** (die fünf
zusätzlichen Befunde sind die ehrlichen Grenzen von `speichern`, die der Kind-Test meldet).

**Zeitaufwand.** 04.10. 23:49 → 05.10. 00:29 = **40 Minuten**, eine Sitzung, vier Schritte (Speichern,
Punkte, Kampf, Portal), drei Unteragenten, vier eigene Nachprüfungen, vier Sammelläufe.

**Was danach noch offen ist (Reihenfolge aus `docs/UMSETZUNG_EINHAENGEN.md`, Abschnitt 5):** Schritt 4
(Kartenansicht — laut Plan nur zu verifizieren), 5 (`werkstatt`), 7 (`auftraege`), 8 (`botkern`),
9 (Fachschicht, freiwillig) und 10 (`.exe` neu bauen und startprüfen). Die `.exe` bleibt bis dahin die
alte Fassung vom 04.10. 22:42 — neu gebaut wird sie **ganz zuletzt**, nach `docs/WEG_ZUR_EXE.md`.
