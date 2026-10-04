# Nebelseetal Remake — Projektstand und Übergabe

Stand: **04.10.2026, 22:00**. Diese Fassung ersetzt die vorherige (archiviert unter
`docs/archiv/PROJEKT_STAND_alt_2026-10-04.md`).
**Diese Datei ist der Einstiegspunkt.** Jede neue Sitzung liest zuerst hier — nicht die Chat-Historie.

---

## 0. DAS LAUFENDE ZIEL — BITTE ÜBERNEHMEN

Daniels Ziel, wörtlich:

> „Eine fertige schlüssige fehlerfrei Spielbare .exe, die stabil das Spiel Nebelseetal (damals
> Browsergame) als remake und Einzelspielerspiel startet. Überprüft und vllt so gesichert das man es
> nur spielen kann mit meinem vorgegebenen Passwort."

Vorgaben aus der Sitzung vom 04.10.2026:

- **Passwort:** Daniel setzt es **selbst beim ersten Start**. Es kommt **niemals** in den Chat, ich
  frage nie danach. Gespeichert wird nur ein gesalzener Prüfwert lokal. Ehrlich benannt: ein lokales
  Tor hält Gelegenheitsspieler ab, mehr nicht. Entwurf: `docs/WEG_ZUR_EXE.md`.
- **Guthaben:** das OpenAI-Guthaben stand für diesen Auftrag zur Verfügung; Auto-Recharge ist aus,
  es können **keine Schulden** entstehen. Bei DeepSeek muss ein **kleiner Rest** bleiben. Teure
  Modelle nur mit Grund, Kosten nach jedem Aufruf messen.
- **Agent-zu-Agent Englisch/ASCII erlaubt**, alles für Daniel bleibt **Deutsch**.
- **Nach jedem groben Schritt eine Zeile ins Entwicklungsprotokoll** (`docs/ENTWICKLUNGSPROTOKOLL.md`):
  Zeit, Schritt, Ergebnis, Beleg (Prüfzahl/Commit). Nur anhängen, Fehler mit hinein — Daniel
  schreibt die Entstehung des Spiels mit.
- **Unteragenten arbeiten an eigenen Dateien und haben ein Kommunikationsbrett** (`docs/BOARD.md`):
  vorher lesen, Dateien beanspruchen, danach Ergebnis mit echten Zahlen eintragen. Aufteilung und
  Modellwahl sind in `docs/AGENTEN_PLAN.md` vorgeschrieben (Daniels Vorgabe vom 04.10.2026).
- **Ordnerstruktur aufgeräumt halten** — Regeln in `docs/ORDNUNG.md`.
- **Kein teuer erarbeitetes Modellergebnis darf verloren gehen** (Abschnitt 4).
- Wenn das Kontextfenster voll wird: **Daniel warnen** und diese Übergabe aktualisieren.

**Startzeile für die neue Sitzung (zum Kopieren):**

```
Lies D:/Arbeiten/Nebelseetal_Remake/docs/PROJEKT_STAND.md und übernimm das laufende Ziel aus
Abschnitt 0. Lies dann docs/AGENTEN_PLAN.md (Agentenaufteilung und Modellwahl) und docs/BOARD.md
(das Kommunikationsbrett der Unteragenten). Arbeite nach Abschnitt 6 weiter — nächster Schritt:
W4b-5, die 20 Originalgebäude samt ihren Wirkungen ins Spiel holen (W4b-4 ist erledigt). Prüfe
jede Zahl selbst nach, statt Meldungen zu glauben.
```

---

## 1. In zwei Befehlen prüfen

```bash
cd /d/Arbeiten/Nebelseetal_Remake
run_tests.bat
git log --oneline | head -12
```

Erwartet: **526 bestanden, 0 Fehler, 0 Befunde** über elf Prüfdateien:
baseline 39 · spieldaten 52 · kampf 42 · gelaende 81 · siedlungskarte 33 · kartenansicht 40 ·
berater 66 · wirtschaft 42 · forschung 68 · welt 42 · ertrag_anbindung 21.

Grün heißt „nichts ist kaputt und die umgestellten Teile halten sich ans Handbuch" — **nicht**
„Spiel ist fertig". Was fehlt, steht in Abschnitt 5.

**Achtung:** `test_kartenansicht.py` braucht einen angemeldeten Windows-Desktop (es baut ein echtes
Fenster und bedient es). Ohne Bildschirm bricht es mit klarer Meldung ab.

## 2. Richtschnur

**Das Original-Handbuch 2009 ist verbindlich.** Alles stammt daraus oder aus belegten Quellen der
alten Website (`docs/original/`). Fehlt eine Angabe, wird sie **null** gesetzt und begründet — es
wird **nichts geschätzt**. Eigene Zahlen stehen immer als `VORSCHLAG` mit Ableitung.

**Erhaltene Original-Spielbilder:** drei echte Screenshots aus dem GameStar-Review vom 09.09.2008,
1261×833 Pixel, in `docs/original/karten/`. Sie sind die **einzige verbliebene Quelle** echter
Spielansichten. Auswertung: `docs/audits/astra_gamestar_antwort.txt` (0,47 USD).

**Die Suche nach den Originalbildern ist ABGESCHLOSSEN — nicht wiederholen.** Vier Wege geprüft,
alle negativ für die Spielansichten:

| Weg | Ergebnis |
|---|---|
| Web-Archiv, CDX über `nebelseetal.de` **und alle sechs Unterdomänen** | kennt nur `screens.php`, **keine** der vier Bilddateien; Wildcard-Zeitstempel 2005–2015 → 404, die Unterdomänen haben 0 Bilddateien |
| Web-Archiv, direkte Bildabrufe über vier Zeitstempel × fünf Server × vier Größen | kein Treffer |
| Browserspiel-Portale, archive.today, YouTube, osnanet, Reddit (blockiert) | keine Spielbilder; der Reddit-Thread ließ sich nicht abrufen |
| **Common Crawl** (66 Abfragen, 1 h) | 2009er Index hat die **Seiten** (`screens.php`, `wallpaper.php` — gesichert), aber **keine Bilder**; 2018 nur die geparkte Startseite |

**Was es gibt und wo es liegt:** die GameStar-Screenshots (3), der Wallpaper, die Website-Schaltflächen
und Logos (32 Bilddateien in `docs/original/karten/`), die Common-Crawl-Seitenruinen
(`docs/original/karten/commoncrawl/`), die vier Website-Bilder in `docs/original/assets_website/`.

## 3. Was fertig ist

| Paket | Inhalt | Beleg / Prüfung |
|---|---|---|
| **W0** Sicherheitsnetz | Git, `.gitignore`, Prüfrahmen, `run_tests.bat` | 526 Prüfungen grün |
| **W1a–c** Originaldaten + Icons | Handbuch 2009, 16 Website-Seiten, 15 Seiten von 2005, 45 Icons | `docs/original/`, `data/*.json` |
| **W1d** Einheiten | 28 Originaleinheiten mit Rollen statt 36 erfundene | Paladin ×10 = 1450 |
| **W2** Kampfablauf | `src/kampf.py`: Vorrunde, Mauerschaden, 10 Sequenzen, Flucht, Beute | 42 Prüfungen, Handbuch S. 20–22 |
| **W4a** Rohstoffe | 9 Originalrohstoffe, Start 100/100/10, Siedler = Bevölkerung | 40 Prüfungen |
| **W4b-1** Gelände | 7 Geländearten, Erträge je Geländeart, Sümpfe gesperrt | `src/gelaende.py`, 81 Prüfungen |
| **W4b-2** Siedlungskarte | eigene Karte je Siedlung, **niemals zwei gleiche**; Bauen mit Eignungsanzeige; Abreißen | 33 + 37 Prüfungen, S. 259/283/292/313 |
| **W4b-3** Wirtschaft | Ertrag aus den bebauten Feldern, Summe über Siedlungen, Forschungsfaktor | `src/wirtschaft.py`, 42 Prüfungen |
| **W4c** Forschung | Stufe steigt erst nach Ablauf · Dauer Stufe² Stunden · Kosten verdoppeln · Bibliothek nötig · Abbruch kostet Rohstoffe | `src/forschung.py`, 68 Prüfungen |
| **W5-1** Weltkarte (Modell) | Limbus mit 20 Dimensionen | `src/welt.py` + `data/welten.json`, 42 Prüfungen |
| **WA** Aufträge/Bots (Entwurf) | Auftragsarten, Ablauf, Bot-Regeln, Beute, drei Scheiterfälle | `docs/ENTWURF_AUFTRAEGE.md`, Seite für Seite nachgeprüft |
| **Auskunft** | Reiter „Chat" antwortet aus den Spieldaten — ohne Netz, ohne Schlüssel | `src/berater.py`, 65 Prüfungen |
| **Karten** | 5 Kartentypen mit eigenen Vorteilen; 2 Mustervorlagen | `docs/MUSTERVORLAGEN.md` |

### Neu gefundene Originalwerte (wichtig!)

**Die Baupreise sind NICHT unbekannt** — sie standen die ganze Zeit in unserem eigenen Code:

| Gebäude | Original (Screenshot 1838857) | Stand im Code |
|---|---|---|
| Holzfäller | 10 Holz, 5 Stein, **1 Siedler** | 10/5/1 Nahrung ✗ |
| Steinmetz | 5 Holz, 10 Stein, 1 Siedler | 5/10/1 Nahrung ✗ |
| Jäger | 25 Holz, 25 Stein, 1 Siedler | 25/25/1 Nahrung ✗ |
| Haus | 80 Holz, 50 Stein | 80/50 ✓ |

Zwei unabhängige Quellen stimmen überein. Der Fehler ist überall derselbe: dritter Posten =
**1 Siedler**, nicht 1 Nahrung. Der daraus abgeleitete Preisentwurf des Modells (8 Holz + 4 Stein)
ist **widerlegt** und in `data/baupreise.json` zu korrigieren.

Weitere belegte Originalregeln (Seiten von 2005):
- **1 Siedler je Stunde**; Siedlergrenze **5 je Siedlung + 5 je Haus**
- Heilkunde: **+10 % Siedlerproduktion je Stufe**
- Weltkoordinaten **(X, Y, Z)**: X/Y im 20×20-Raster der eigenen Dimension, Z = Dimension.
  Andere Dimensionen kosten viel Mana — erst in der eigenen Dimension suchen.
- Koordinatenwechsel: **5.000 Mana aus EINER Siedlung**, höchstens einmal je 24 Stunden
- Portalansicht: **20×20-Raster** über einer Spiralnebelstruktur, eigene Welt **grün**, fremde **rot**
- „Sümpfe sind unbebaubar und somit für Eure Siedlungen völlig wertlos."

### Original-Menü (wörtlich aus dem Screenshot 1838855)

Übersicht · Portal · Diplomatie · Einstellungen · Ruhmeshalle · Gildenhalle · Voraussetzungen ·
Nachrichten · Neuigkeiten · Anleitung · Schlachtsimulator · Forum · Chat · Spieler werben · Logout
Dazu oben die Rohstoffleiste, links „Eure Punkte: Forschung / Krieg / Gesamt", unten „Laufende Aufträge:".

## 4. Die teuer erarbeiteten Modelldaten — WO SIE LIEGEN

**Nichts davon darf verloren gehen.** Alles liegt im Projekt und in Git:

| Ordner | Inhalt | Umfang |
|---|---|---|
| `docs/audits/` | **12 Antworten** der teuren Modelle, unverändert gesichert | 532 KB |
| `docs/audits/eingaben/` | **11 Eingaben** — was den Modellen vorgelegt wurde | 376 KB |

Die wichtigsten Antworten:

| Datei | Was darin steht | Kosten |
|---|---|---|
| `astra_gamestar_antwort.txt` | Analyse der drei Original-Screenshots: Portalansicht (20×20 mit grün/rot), Original-Menü, **Original-Baupreise** | 0,47 USD |
| `astra_audit2_antwort.txt` + `2b` | Konformitätsaudit über alle 24 Handbuchseiten (fand meinen Fehler „10 statt 7 Tage Götterschutz") | ~0,78 USD |
| `astra_wirtschaft_antwort.txt` | Wirtschaftsentwurf (Baupreise, Ausbildungsdauern, Pacing) — Preise **widerlegt**, Rest brauchbar | ~0,8 USD |
| `astra_kampf_antwort.txt` | Kampf-Audit | 0,43 USD |
| `astra_karten_antwort.txt` | Analyse der vier Website-Bilder: **keines zeigt eine Karte** | ~0,3 USD |
| `astra_wallpaper_antwort.txt` | Farbwelt des Originals aus vier Bildern | ~0,2 USD |
| `design_auftraege.txt` | Auftrags- und Bot-System (deepseek-v4-pro) | 0,12 USD |
| `muster_siedlung.txt`, `muster_welt.txt` | die Mustervorlagen | 0,04–0,12 USD |

**Ausgewertet und nutzbar** in: `docs/AUDIT_KONFORMITAET_astra.md`, `docs/ENTWURF_WIRTSCHAFT.md`,
`docs/ENTWURF_AUFTRAEGE.md`, `docs/MUSTERVORLAGEN.md`, `data/gelaende.json` (Farbwelt).

**Regel:** neue Modell-Antworten **immer sofort** aus dem Zwischenspeicher
(`%LOCALAPPDATA%\hermes\cache\scratch`) nach `docs/audits/` kopieren und einchecken — der
Zwischenspeicher wird nach 24 Stunden geleert. Genau so waren am 04.10.2026 zwei Ergebnisse fast
verloren gegangen (die Kartenanalyse und die Siedlungsvorlage).

## 5. Was der Code noch NICHT kann

| fehlt | Folge | Paket |
|---|---|---|
| ~~Kartenerträge an die Rohstoffproduktion angebunden~~ | **erledigt am 04.10.2026 (W4b-4)** — bebaute Felder liefern jetzt wirklich | — |
| 5 Wirkungsgebäude global statt 20 Originalgebäude | die 20 stehen auf der Karte, aber Kaserne/Turm/Portal/Bibliothek/Haus haben ihre Wirkung nur global | W4b-5 |
| Haus und Bibliothek gibt es doppelt (global *und* auf der Karte) | die Kartenfassung hat noch keine Wirkung (+5 Bevölkerung / Forschung) | W4b-5 |
| Forschung wirkt nur auf Holz, Stein, Nahrung | Metall, Leder, Mana, Gold, Wolle, Pferde bleiben bei Faktor 1,0 | W4b-6 |
| 17 Waren als Emoji statt Handwerk | Handwerk fehlt | W3 |
| Auftragssystem nur als Entwurf | keine Missionen auslösbar | WA |
| Kampf nur als Modul | nicht aus dem Spiel auslösbar | W2b |
| Weltkarte nur als Rechenmodell | keine Portalansicht im Fenster | W5-2 |
| Oberfläche weicht vom Original ab | Original-Menü belegt, Reihenfolge fehlt | W7 |
| kein Passworttor, keine `.exe` | **das Ziel ist noch nicht erreicht** | W9 |

## 6. Nächste Schritte (in dieser Reihenfolge)

1. ~~**W4b-4 — Kartenerträge anbinden**~~ **erledigt am 04.10.2026.** `GameState.stundenertrag()`
   speist Zeitlauf und Anzeige aus `wirtschaft.ertrag_gesamt()`; 21 Prüfungen in
   `tests/test_ertrag_anbindung.py` (Holzfäller auf Wald 4/h, Steppe 2/h, zwei Felder 8/h,
   Bergbau Stufe 2 → 4,8/h). **Zwei Befunde dabei, beide behoben:** (a) das Wirtschaftsmodul liefert
   die Kennungen in Lesefassung („Holz") — der Zeitlauf fand sie nicht und schrieb stillschweigend
   nichts gut; jetzt wird an der Grenze umgeschrieben. (b) die fünf rohstofferzeugenden Gebäude
   (Holzfäller, Steinmetz, Jäger, Schmiede, Markt) sind aus der globalen Liste entfernt — sonst
   hätten beide Systeme denselben Rohstoff erzeugt.
   *Achtung — vom Wirtschaftsmodul gemeldet und offen:* `bonus_system.get_production_multiplier`
   erhöht nur **Holz, Stein, Nahrung** (und das alte „eisen"). **Metall, Leder, Mana, Gold, Wolle und
   Pferde bleiben bei Faktor 1,0** — Forschung wirkt dort nicht. Das ist eine Lücke im Bonus-System,
   nicht im neuen Modul; beim Anbinden entscheiden, ob sie geschlossen wird.
2. **Baupreise korrigieren** in `data/baupreise.json`: die vier belegten Werte eintragen
   (1 Siedler statt 1 Nahrung), den widerlegten Vorschlag kennzeichnen.
3. **Weltkarte auf das belegte Modell umstellen**: 20 Dimensionen · je 20×20 Felder · (X, Y, Z) ·
   Ritual 5.000 Mana aus einer Siedlung · eigene Welt grün, fremde rot.
4. **W4b-5 — die 20 Originalgebäude** ins Spiel (statt 10), Preise wie belegt.
5. **WA — Auftragssystem** nach `docs/ENTWURF_AUFTRAEGE.md`.
6. **W2b — Kampf ins Spiel** (auslösbar, Bericht in den Nachrichten).
7. **W7 — Oberfläche** nach der belegten Menüliste.
8. **W9 — Auslieferung** als `.exe` mit Passworttor (`docs/WEG_ZUR_EXE.md`).

## 7. Offene Entscheidungen (Daniel)

**Entschärft:** Baupreise — vier Gebäude sind jetzt belegt (Abschnitt 3). Offen bleibt nur die
Bepreisung der übrigen, deren Menüeintrag wir nicht im Bild haben.

Weiter offen:

- **Zeitfaktor**: Spieltag = 2 Echtzeitstunden (Vorschlag) — oder näher am Original?
- **Forschungstempo**: Handbuchformeln (Stufe² Stunden; Stufe 10 = 100 Stunden) **mit** Zeitfaktor,
  oder gestauchte Zahlen?
- **Baupreise der übrigen 16 Gebäude**: aus dem Ertrag ableiten oder eigene Regel?
- **Bauzeit**: 3 Minuten je Gebäude mit Warteschlange (Vorschlag)?
- **Bots**: Handelsregel (Referenzpreis ×1,2, Temperament ±10 %) · Angriffstakt (alle 6–24 h) ·
  Beutemenge (50 % der Lager, gedeckelt durch Karrenladung)?
- **Kartenmaß**: 8×5 = 40 Felder ist **Vorschlag** — das Handbuch nennt keine Größe.
- **Sieg-/Niederlagebedingung**: nennt das Handbuch nicht — Vorschlag nötig.
- **Kampfdarstellung**: Bericht in einem Zug oder Schritt für Schritt?

## 8. Arbeitsweise in diesem Projekt (bewährt — beibehalten)

- **Erst prüfen, WAS läuft**, nicht was im Ordner liegt. Genau **eine** ausführbare Fassung im
  Projekt, alte Builds in die Quarantäne.
- **Nie schätzen.** Fehlt ein Wert: `null` + Begründung.
- **Nachprüfen statt glauben.** Jedes Modell- oder Agentenergebnis wird gegen die Quelle gehalten.
  In dieser Sitzung deckte das einen Rechenfehler, einen widerlegten Preisvorschlag und einen
  falschen Weltbezug auf.
- **Schreibvorgänge nachprüfen.** Eine Änderung an `run_tests.bat` meldete Erfolg und kam nie an —
  nur durch `grep` aufgefallen. Immer zurücklesen.
- **Modell-Antworten sofort sichern** (Abschnitt 4) — der Zwischenspeicher räumt nach 24 Stunden auf.
- **Originaldateien unantastbar**: `docs/original/`, die 7 Icon-Blätter, Daniels 17 Dateien.
- **Parallel arbeiten, aber nach Dateien trennen**: jedes Kind bekommt eigene neue Dateien + eigene
  Prüfdatei, bestehende Dateien anzufassen ist verboten. Das Einhängen in `main.py` macht der
  Hauptagent selbst, nacheinander.
- **Agent-zu-Agent Englisch/ASCII**, alles für Daniel **Deutsch**.
- **Erst `deepseek-v4-pro`** für Entwürfe und Analysen (0,04–0,12 USD), `gpt-6-astra` nur für
  **Bilddeutung** (0,47 USD für drei Bilder). Merksatz: ein teures Modell ist ein Rechenschritt,
  kein Arbeiter.
- **Kleine Commits** nach jedem Paket.

## 9. Guthaben (Stand 22:00)

| Konto | Stand | Regel |
|---|---|---|
| OpenAI (astra) | **5,56 USD verfügbar** — 3,33 USD am 04.10. verbraucht (gemessen über `/v1/organization/costs?group_by=line_item`), von Daniel von der Billing-Seite abgelesen; Auto-Recharge aus, keine Schulden möglich | nur noch für Bilddeutung |
| DeepSeek | 3,32 USD (**nicht nachgeprüft**) | ein kleiner Rest **muss** bleiben |
| Kosten je Auftrag | v4-pro 0,04–0,12 USD · astra 0,47 USD (3 Bilder). **Größter Posten sind die Cache-Schreibkosten** (3,56 gegen 0,94 USD Ausgabe) → Aufträge kurz halten | `docs/ENTWICKLUNGSPROTOKOLL.md` (Abschnitt Kosten), Skill `kosten-schutzregel` |

## 10. Dauerhaftes Arbeitssystem

| Baustein | Wo |
|---|---|
| `docs/PROJEKT_STAND.md` | dieses Dokument — Wiederaufnahme ohne Chatverlauf |
| `docs/AGENTEN_PLAN.md` | **wie die Sitzung ihre Agenten aufteilt und welches Modell wann** — inklusive Auftragsvorlage zum Kopieren |
| `docs/BOARD.md` | **Kommunikationsbrett der Unteragenten** — Ansprüche, Ergebnisse, Meldungen |
| `docs/LEHREN.md` | **ehrliche Nachlese** der Sitzung: 13 Fehler, was gut lief, was dauerhaft gilt |
| `docs/ENTWICKLUNGSPROTOKOLL.md` | **laufendes Protokoll** der groben Arbeitsschritte **mit Kosten** (Daniel schreibt die Entstehung mit) — nach jedem Schritt fortschreiben |
| `docs/ORDNUNG.md` | was wohin gehört |
| `docs/audits/` + `eingaben/` | alle Modelldaten (Abschnitt 4) |
| `tests/` (elf Dateien) + `run_tests.bat` | Wahrheitsquelle „läuft es noch?" |
| Skills `multi-agent-coding`, `kosten-schutzregel`, `nebelseetal-remake` | Betriebs- und Projektwissen |
| Kanban-Board `nebelseetal` | Paketliste (Verteiler braucht laufendes Gateway) |
| `D:/Arbeiten/_Quarantaene/` | alte Builds (dort: `Nebelsee Memory.exe` mit README) |

## 11. Letzte Commits

| Commit | Inhalt |
|---|---|
| *(neu)* | alle Modelldaten ins Projekt gesichert (23 Dateien, 908 KB) |
| `295301a` | drei neue Module, Mustervorlagen, Original-Screenshots — 488 Prüfungen grün |
| `b75400a` | Auftrags- und Bot-Entwurf, Seite für Seite nachgeprüft |
| `67bec37` | Gesamtlauf um die Prüfdatei der Auskunft erweitert |
| `e1b8d95` | Auskunft im Spiel (Reiter Chat) |
| `9bf3175` | Siedlungsansicht im Fenster: Karte sehen, Feld wählen, bauen, abreißen |
| `bca0392` | Siedlungskarte im Spiel + Ordnung im Projekt |
| `9ee2fac` | Gelände und Siedlungskarten mit fünf Kartentypen |
| `b5f76b2` | Wirtschafts-Entwurf + Weg zur .exe festgelegt |
| `f3e4c4f` | Konformitäts-Audit (astra) über alle 24 Handbuchseiten |
