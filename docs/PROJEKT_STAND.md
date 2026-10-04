# Nebelseetal Remake — Projektstand und Übergabe

Stand: **05.10.2026, 00:55**. Diese Fassung ersetzt die vorherige (archiviert unter
`docs/archiv/PROJEKT_STAND_alt_2026-10-04_2345.md`; die Fassungen davor unter
`docs/archiv/PROJEKT_STAND_alt_2026-10-04_2200.md` und `..._alt_2026-10-04.md`).
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
- **Unteragenten arbeiten nur an eigenen Dateien und führen kein eigenes Brett** (Vorgabe Daniel,
  04.10.2026): sie bauen neue Dateien, prüfen sie selbst und melden ihr Ergebnis im
  Abschlussbericht. Der **Koordinator** prüft nach und trägt in `docs/BOARD.md` ein. Aufteilung und
  Modellwahl stehen in `docs/AGENTEN_PLAN.md`.
- **Ordnerstruktur aufgeräumt halten** — Regeln in `docs/ORDNUNG.md`.
- **Kein teuer erarbeitetes Modellergebnis darf verloren gehen** (Abschnitt 4).
- Wenn das Kontextfenster voll wird: **Daniel warnen** und diese Übergabe aktualisieren.

**Startzeile für die neue Sitzung (zum Kopieren):**

```
Lies D:/Arbeiten/Nebelseetal_Remake/docs/PROJEKT_STAND.md (Einstiegspunkt) und übernimm das laufende
Ziel aus Abschnitt 0. Lies dann NUR das Kontext-Paket aus Abschnitt 0c (eine Seite + zwei
Dokumentabschnitte + die Zieldatei an der Aufrufstelle) — die Chat-Historie brauchst du nicht.
Der EINE nächste Schritt steht in Abschnitt 0c: das Auftragssystem (`src/auftraege.py`) einhängen.
Nach jedem Schritt: betroffenen Einzeltest + einmal Sammellauf, eine Protokollzeile (Zeit, Schritt,
Ergebnis, Beleg, Kosten), `python tools/protokoll_sichern.py --protokoll`, kleiner Commit. Prüfende
Unteragenten erst NACH dem Commit loslassen. Am Ende der Reihe die `.exe` neu bauen
(`tools/build_exe.py`) und aus einem anderen Ordner startprüfen.
```

---

## 0c. Stand beim Sitzungswechsel (05.10.2026, 00:49 — mit `date` geprüft)

**Nichts läuft. Arbeitsverzeichnis sauber** (Commit `a1f224a`, `git status` leer), Papiere
projektunabhängig gesichert (`python tools/protokoll_sichern.py --protokoll`: 16 Dateien, Prüfsummen
gleich, Zeiger `D:\Arbeiten\Hermes\Nebelseetal_Protokoll\zuletzt.txt`).

| Was | Stand (gemessen) |
|---|---|
| Prüfstand | **1798 bestanden, 0 Fehler, 15 Befunde über 27 Dateien**, Rückgabewert 0 (Lauf 05.10. 00:49:17) |
| Neu eingehängt in dieser Sitzung | **1 · `speichern`** (atomar, Sicherung, Wiederherstellung) · **2 · `punkte`** (Originalformeln in Seitenleiste + Ruhmeshalle) · **3 · `kampf` + `kampfbericht`** (ein Angriffsweg für Karte und Bot, Bericht in die Nachrichten) · **6 · `portalraum`** (20×20-Raster, 5.000 Mana, 24-h-Sperre) · **5 · `werkstatt`** (17 Originalwaren mit Original-Icons, Werkstätten, Warteschlangen, Voraussetzungen) |
| Neue Prüfdateien | `test_w8_einhaengung` 39 · `test_punkte_einhaengung` 44 · `test_kampf_einhaengung` 42 · `test_gui_fehler` 22 (stille tkinter-Fehler werden laut) |
| Neues Werkzeug | `tools/pruefe_verdrahtung.py` — Textbeweis aus `main.py`: 13 verdrahtet, `botkern` nur importiert, `auftraege`/`forschung`/`welt` nicht eingebunden; meldet doppelte Definitionen und zweite Wahrheiten |
| **Noch nicht eingehängt** | `auftraege` (Missionen), `forschung` (Wartezeit statt Sofort-Stufe), `welt` (Weltkarte), Teile von `botkern` (Bot-Verhalten je Runde) |
| **Neu erledigt (01:02)** | Der **Kampfsimulator** rechnet nicht mehr mit der erfundenen Kampfkraft, sondern über `kampf.fuehre_schlacht` als Trockenkurs (bucht nichts, kennzeichnet den Übungsgegner als ausgedacht); die nicht mehr benutzten `bonus_system`-Importe sind entfernt. **`tools/pruefe_verdrahtung.py`: Summe Treffer 0** — keine zweite Wahrheit mehr in `main.py` |
| `.exe` | **05.10. 00:53 neu gebaut**: `Nebelseetal_Remake.exe`, **14.108.111 Byte (13,5 MB)**, SHA256 `73e04b5909b0dedd177a7d331e2501051f1d5f15e185d333c1ed731699dacbc4`; **Startprüfung bestanden** (Ordner mit Leerzeichen, Fenster „Nebelseetal Remake", kein Absturz, Passworttor steht; das Passwort wurde **nicht** eingegeben). Enthält Speichern, Punkte, Kampf, Portal und Werkstatt — **nicht** die noch offenen Module |
| Kosten dieser Sitzung | **0,7082 USD = 0,6309 EUR** (`scripts/tageskosten_check.py --json`, Messung 01:02), davon **0,3444 USD** der auf Daniels Wunsch geholte `gpt-6-astra`-Rat; der Rest ist Koordinator + `flash`-Unteragenten |
| Guthaben | Daniel ablesen lassen: OpenAI **3,04 → ~2,70 USD**, DeepSeek **1,70 USD** (Reserve 1,00 USD unberührt) — bitte bei der nächsten Sitzung erneut ablesen, ich kann es nicht messen |

### Der EINE nächste Schritt

**Auftragssystem einhängen — `src/auftraege.py` (Modul fertig, 111 Prüfungen grün).** Der Plan steht in
`docs/UMSETZUNG_EINHAENGEN.md`, Abschnitt 1.7: `GameState` bekommt eine Auftragsliste
(`auftraege.neue_liste()`), gestartet wird über `auftraege.starten(liste, art, einheiten, von, nach,
entfernung, jetzt, fracht)` — der vorhandene Knopf „Transport" und eine neue Auftragsliste im Fenster
sind die Oberfläche; im `_tick_loop` laufen `auftraege.fortschritt` / `angekommen` /
`spieldaten_anwenden`, Berichte über `auftraege.bericht` in den Reiter „Nachrichten". Hinweis aus der
Modulprüfung: „Ueberladen: X Einheiten Fracht passen nicht auf Y Ladeplaetze." ist der einzige echte
Überlade-Fehler. Erwartet: `tests/test_auftraege.py` → **111 grün**, `tests/test_gui_fehler.py` →
**22 grün**, Sammellauf → **1798 grün** (er steigt, wenn eine neue Prüfdatei dazukommt).

### Kontext-Paket für die neue Sitzung (bewusst klein halten — spart Geld und Fehler)

| Reihenfolge | Was laden | Warum nicht mehr |
|---|---|---|
| 1 | **diese Datei, Abschnitt 0c** | Stand in Belegen und der eine nächste Schritt; der Rest der Datei ist Historie |
| 2 | `docs/ENTWICKLUNGSPROTOKOLL.md`, **nur den Abschnitt „05.10.2026 — Tag 2"** | was zuletzt wirklich passierte, samt Irrwegen und Kosten |
| 3 | `docs/UMSETZUNG_EINHAENGEN.md`, **nur § 1.7 (Aufträge) und § 2 (Kampfablauf-Fehlerfälle)** | der Plan für genau diesen Schritt |
| 4 | `src/auftraege.py` — **nur der Modulkopf und die öffentlichen Funktionen** (`grep -n "^def "`) | die Signaturen genügen; das Innenleben ist durch 111 Prüfungen gedeckt |
| 5 | `src/main.py` — **nur** `GameState.__init__`, die Fundstelle des „Transport"-Knopfes, `_tick_loop`, `save`/`load` | nie die ganze 2400-Zeilen-Datei laden |
| 6 | `data/*.json` **nur**, wenn eine konkrete Zahl gebraucht wird (und dann mit Quelle) | Zahlen haben eine Quelle, nicht im Kopf |

**Nicht in den Kontext:** die vollständige `main.py`, ganze Testprotokolle (nur Fehlerzeilen),
die Chat-Historie, `docs/archiv/`, `docs/audits/` (außer man braucht ein bestimmtes Gutachten),
abgeschlossene Schritte im Detail, wiederholte Regeltexte.

**Werkzeuge statt Lesen:** `python tools/pruefe_verdrahtung.py` sagt in Sekunden, welche Module wirklich
verdrahtet sind (und ob es eine zweite Wahrheit gibt); der Sammellauf ist die Wahrheit über den Zustand;
`docs/SICHERUNGEN.md` zeigt, wo die Papiere liegen; `git log --oneline -3` + `git status --short` sind
die Sekunden-Checks vor dem Anfassen von `src/`.

**Zwei Hausregeln, die diese Sitzung teuer gelernt hat:** (a) **eine Spieleraktion je Commit** —
keine fremde Aufräumarbeit mit hineinnehmen; (b) **prüfende Unteragenten erst nach dem Commit
loslassen**, sonst messen sie einen bewegten Zwischenstand.

### Danach in dieser Reihenfolge

`auftraege` (Reisezeit, Rückkehr, Beute, Bericht) · `forschung` mit Wartezeit statt Sofort-Stufe ·
`botkern` vollständig (Bot-Stärken und echtes Bot-Lager — heute sind die Bot-Armeen erfundene
20–120 je Einheit, dadurch ist ein Bot-Angriff praktisch aussichtslos) · `welt`/Portalraum-Feinschliff ·
**danach die `.exe` erneut bauen** (die Fassung vom 05.10. 00:53 enthält die noch offenen Module nicht)
und wieder aus einem anderen Ordner startprüfen.

### Nicht erneut zu prüfen (Beleg steht hier)

| Sache | Beleg | Stand |
|---|---|---|
| Prüfstand | Laufprotokoll 00:49:17, Rückgabewert 0 | 1798 / 0 Fehler / 15 Befunde, 27 Dateien |
| Die fünf Einhängungen | je eigene Nachprüfung des Koordinators + Sammellauf | 05.10. 00:00–00:52 |
| Stille tkinter-Fehler | `test_gui_fehler` 22/0/1 | 18 Ansichten, 13 Aktionen, 0 echte Fehler |
| Verdrahtungsstand | `tools/pruefe_verdrahtung.py` | 13 verdrahtet, 1 nur importiert, 3 offen |
| Papiere gesichert | `MANIFEST.txt` mit SHA256 je Datei | 05.10. 00:49, 16 Dateien |

### So startet die neue Sitzung (Sekunden-Checks statt Sammellauf)

```bash
cd /d/Arbeiten/Nebelseetal_Remake
git log --oneline -3     # nur docs/* dazu? dann ist nichts nachzuprüfen
git status --short       # leer = sauber
```

Nur wenn `src/` angefasst wird: betroffenen Einzeltest laufen lassen, **einmal** am Ende des Schritts
den Sammellauf.

---

## 0b. Stand beim Sitzungswechsel (04.10.2026, 23:45 — mit `date` geprüft)

**Nichts ist in Arbeit. Kein Prozess läuft, kein Kind arbeitet. Arbeitsverzeichnis sauber**
(Commit `9bbb3c2`), alles committet, Papiere projektunabhängig gesichert
(`D:\Arbeiten\Hermes\Nebelseetal_Protokoll\`, 14 Dateien, Prüfsummen geprüft).

| Was | Stand (gemessen) |
|---|---|
| Prüfstand | **1651 bestanden, 0 Fehler, 9 Befunde** über **23 Dateien** (`run_tests.bat`, Rückgabewert 0) |
| Fertige Module (alle vom Koordinator nachgerechnet) | `forschung_wirkung` 94 · `werkstatt` 118 · `portalraum` 69 · `punkte` 76 · `kampfbericht` 108 · `spielschicht` 133 · `botkern` 90 · `auftraege` 111 · `speichern` 95 · `oberflaeche_original` 64 |
| Eingehängt | W4b-5 (Gebäudewirkungen), W4b-6 (21 Forschungen + alle neun Rohstoffe), Passworttor |
| **Nicht** eingehängt | die zehn Module in der Oberfläche — **das ist der nächste Schritt**, nach `docs/UMSETZUNG_EINHAENGEN.md` |
| `.exe` | liegt im Projektordner (14.024.744 Byte), mit Tor startgeprüft; **Neubau erst nach dem Einhängen** |
| Kosten der Nacht | teure Aufrufe zusammen **+0,79 USD** (astra für die Bilder, v4-pro für den Plan); Guthaben: OpenAI **4,08** · DeepSeek **2,08** USD (1,00-USD-Reserve unberührt) |
| Offene Fragen an Daniel | **13** — `docs/FRAGEN_FUER_MORGEN.md` |
| Brett der Kinder | **abgeschafft** (Daniel, 04.10.) — Kinder melden im Abschlussbericht, der Koordinator prüft nach und trägt in `docs/BOARD.md` ein |

### So startet die neue Sitzung (kurz — nichts doppelt prüfen!)

**Regel: nur das prüfen, was sich seit dieser Übergabe geändert hat.** Der Sammellauf ist teuer
(rund 7 Minuten) und war beim Schreiben dieser Zeilen grün. Wenn `git log` zeigt, dass seither
**nur Dokumente** dazukamen, ist ein neuer Sammellauf **nicht** nötig — erst nach der ersten
Änderung an `src/`.

```bash
cd /d/Arbeiten/Nebelseetal_Remake
git log --oneline -3     # was kam seit 9bbb3c2 dazu? nur docs/* => nichts nachzuprüfen
git status --short       # leer = sauber (wenn nicht: erst fragen, nicht überschreiben)
```

**Nicht erneut zu prüfen (Beleg steht hier, nicht im Kopf):**

| Sache | Beleg | Stand |
|---|---|---|
| Prüfstand | `run_tests.bat`, Rückgabewert **0** | 04.10.2026, 23:40 — **1651 / 0 Fehler / 9 Befunde**, 23 Dateien |
| Die zehn Kind-Module | je eigener Lauf des Koordinators | 23:16–23:20, Zahlen in der Tabelle oben |
| `.exe` + Passworttor | Startlauf mit Fenster, sauberes Schließen | 22:42; Datei 14.024.744 Byte im Projektordner |
| Papiere gesichert | `MANIFEST.txt` mit SHA256 je Datei | 04.10.2026 nach jeder Änderung, 14 Dateien |

**Erst wenn `src/` angefasst wird:** den betroffenen Einzeltest laufen lassen (nicht den Sammellauf!),
und den Sammellauf einmal am Ende des Schritts.

### Schritt 1 (der einzige nächste Schritt)

`src/speichern.py` einhängen — **`main.py:608-634`**: in `save()` das direkte Schreiben
(Zeile **627-628**: `open(path,"w")` + `json.dump`) durch `speichern.sichere_kopie(path)` +
`speichern.speichere(data, path)` ersetzen (Rückgabe `(ok, grund)` auswerten und bei `ok == False`
über `self._log(...)` melden), in `load()` über `speichern.lade(path)` lesen und bei Fehlschlag
`speichern.wiederherstellen(path)` versuchen. Einzelprüfung danach:
`python -X utf8 tests/test_speichern_robust.py` → **95 grün** · `tests/test_baseline.py` → **40 grün**.
Alles Weitere steht in `docs/UMSETZUNG_EINHAENGEN.md`, Abschnitt 4 und 5.

---

## 1. In zwei Befehlen prüfen

```bash
cd /d/Arbeiten/Nebelseetal_Remake
run_tests.bat
git log --oneline | head -12
```

Erwartet: **1651 bestanden, 0 Fehler, 9 Befunde** über **23** Prüfdateien (gemessen im Sammellauf
`run_tests.bat` am 04.10.2026, 23:40 — Rückgabewert 0). Die neun Befunde sind ehrliche Hinweise, keine
Fehler; sie stehen bei den jeweiligen Modulen (u. a. fehlende Ausbildungsdauer, keine Dateisperre beim
Speichern, Rundung der Gesamtpunkte).
Einzelaufstellung (gemessen): baseline 40 · spieldaten 53 · kampf 42 · gelaende 81 ·
siedlungskarte 33 · kartenansicht 40 · berater 66 · wirtschaft 42 · forschung 68 · welt 42 ·
ertrag_anbindung 21 · gebaeude_wirkung 103 · tor 61 · forschung_wirkung 94 · werkstatt 118 ·
portalraum 69 · punkte 76 · kampfbericht 108 · spielschicht 133 · botkern 90 · auftraege 111 ·
speichern 95 · oberflaeche_original 64.
Die neun **Befunde** sind ehrlich und bekannt, keine Fehler: (1) das Handbuch nennt keine
Ausbildungsdauer, deshalb kann die Stufe einer Ausbildungsstätte die Dauer noch nicht messbar senken
(`bonus_system.UNIT_TRAIN_BASE = 0`); (2) `werkstatt` meldet eine Lücke in den Waren-Regeln, die
das Handbuch offen lässt; (3) weitere ehrliche Hinweise in `punkte` (Rundung, Götterschutz),
`speichern` (keine Dateisperre, Klartext), `auftraege` und `spielschicht` (Kampfverluste,
Ausbildungsdauer, Portal-Mana je Siedlung) — alle dort als Vorschlag gekennzeichnet.

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
| **W4b-5** Die 20 Originalgebäude | **jede** Wirkung kommt aus den bebauten Feldern: Haus +5 Siedler, Bibliothek schaltet Forschung frei, Kriegerakademie/Diebesgilde/Stellmacher bilden aus, Verteidigungswall mit 10 Stufen; die fünf erfundenen globalen Gebäude sind entfallen | `src/gebaeude_wirkung.py` + `data/gebaeude_wirkung.json`, 103 Prüfungen |
| **W4c** Forschung | Stufe steigt erst nach Ablauf · Dauer Stufe² Stunden · Kosten verdoppeln · Bibliothek nötig · Abbruch kostet Rohstoffe | `src/forschung.py`, 68 Prüfungen |
| **W5-1** Weltkarte (Modell) | Limbus mit 20 Dimensionen | `src/welt.py` + `data/welten.json`, 42 Prüfungen |
| **WA** Aufträge/Bots (Entwurf) | Auftragsarten, Ablauf, Bot-Regeln, Beute, drei Scheiterfälle | `docs/ENTWURF_AUFTRAEGE.md`, Seite für Seite nachgeprüft |
| **Auskunft** | Reiter „Chat" antwortet aus den Spieldaten — ohne Netz, ohne Schlüssel | `src/berater.py`, 65 Prüfungen |
| **Karten** | 5 Kartentypen mit eigenen Vorteilen; 2 Mustervorlagen | `docs/MUSTERVORLAGEN.md` |
| **Siedlungskarte ist EIGENER ENTWURF, kein Originalbeleg** (astra-Gutachten 04.10.2026, zweimal unabhängig) | Auf **keinem** der drei GameStar-Fotos ist eine Siedlungskarte zu sehen: Foto 1 ist die Nachrichtenansicht, Foto 2 die **Portal**ansicht (das 20×20-Raster gehört dorthin), Foto 3 das Baumenü. Der Entwurf steht deshalb vollständig als VORSCHLAG in `docs/KARTEN_ENTWURF.md`. **Wer die Karte später als „originalgetreu" ausgibt, erfindet etwas.** | `docs/KARTEN_ENTWURF.md` |
| **Zahlenwiderspruch im Kartenmaß** (von astra gefunden, vom Koordinator nachgerechnet) | `data/gelaende.json` nennt spalten 8 × zeilen 5 = **40** Felder, zugleich **56** Felder („40 Bauplätze, Rest Wege/Wasser"). Beides zusammen ist unmöglich. Auflösung als Frage 12 an Daniel: **8 × 7 = 56**, davon 40 bebaubar. | Frage 12 |
| **Tor & Auslieferung** (Schritt 8+9) | **Passworttor** (PBKDF2, Erststart setzt selbst, Wartezeit nach Fehlversuchen) und die **`.exe`** — gebaut mit PyInstaller, Einzeldatei ohne Konsole, Symbol mit 6 Größen; Start aus einem Pfad mit Leerzeichen belegt | `src/tor.py` + 61 Prüfungen, `tools/build_exe.py`, Startlauf 04.10. 22:42 |
| **Sechs neue Module** (Kinder-Arbeit, je eigene Prüfdatei) | W4b-6 `forschung_wirkung` (94) · W3 `werkstatt` (118) · W5-2 `portalraum` (69) · W6 `punkte` (76) · W2b `kampfbericht` (108) | 465 Prüfungen grün |

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
- **1 Siedler je Stunde**; Siedlergrenze **10 je Siedlung + 5 je Haus** (Handbuch 2009 S. 11 wörtlich;
  die 2005er Fassung nannte 5 — Versionsunterschied). **Seit W4b-5 rechnet das Spiel damit** —
  vorher wuchs die Bevölkerung mit einem erfundenen Wert von 30 Siedlern je Stunde.
- **Bibliothek** nur auf Grasland, Steppe oder Nebelsee, eine je Siedlung — seit W4b-5 als
  Standortregel im Spiel (`data/buildings.json`, Feld `nur_auf`).
- **Ausbildung:** Kriegerakademie → 9 Kampfeinheiten, Diebesgilde → 6 Kundschafter, Stellmacher →
  6 Karren + 7 Belagerungswaffen. Das steht je Einheit in `data/units.json` (Feld `gebaeude`);
  seit W4b-5 bildet das Spiel nur dort aus, wo die Stätte wirklich steht.
- **Verteidigungswall:** 10 Stufen von Erdwall bis Bollwerk; Schwellenwerte der Vorrunde (Stufe 4
  Palisade = 160 Schlagkraft, ab Stufe 5 zusätzlich Belagerungswaffen); Kriegspunkte = Stufe hoch drei.
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
| ~~Die 20 Originalgebäude wirken nur als Anzeige~~ | **erledigt am 04.10.2026 (W4b-5)** — Haus, Bibliothek, die drei Ausbildungsstätten und der Wall wirken jetzt aus den bebauten Feldern | — |
| ~~Haus und Bibliothek gibt es doppelt (global *und* auf der Karte)~~ | **erledigt mit W4b-5** — die fünf erfundenen globalen Gebäude (Haus, Bibliothek, Kaserne, Wachturm, Portal) sind ersatzlos entfallen; `main.BUILDINGS` ist leer | — |
| ~~Forschung wirkt nur auf Holz, Stein, Nahrung~~ | **erledigt am 04.10.2026 (W4b-6)** — `bonus_system.get_production_multiplier` liefert die belegten Faktoren für **alle neun** Rohstoffe; im Spiel stehen jetzt die **21 Originalforschungen** statt 18 erfundener Gebiete | — |
| **Fertig gebaut, aber noch nicht in der Oberfläche** (Stand 23:20) | die Module sind geprüft grün, aber `main.py` ruft sie noch nicht auf: W3 Waren/Werkstätten, W2b Kampfbericht, W6 Punkte, W5-2 Portalraum, W5 Bot-Kern, **W8 robustes Speichern (95)**, **W7 Menü-Vergleich (64)**. **Das Einhängen ist der nächste Schritt** (Fachschicht + Oberfläche). **Noch nicht gebaut:** WA Aufträge (Kind arbeitet) | Einhängen |
| **Forschung im Spiel steigt SOFORT** (neu entdeckt mit W4b-5) | `src/forschung.py` (Dauer = Stufe² Stunden, Stufe steigt erst nach Ablauf) ist fertig, aber **nicht eingehängt**: `_start_research` zieht die Kosten und erhöht die Stufe im selben Klick. Die Bibliothekspflicht greift jetzt — die Wartezeit fehlt | Einhängen (mit der Fachschicht) |
| **Wallstufen wirken noch nicht im Kampf** | die Schwellenwerte sind abrufbar (`gebaeude_wirkung.wall_schwelle`, `kampfbericht.vorrunde`), aber es gibt noch keinen Angriff aus der Oberfläche | Einhängen |
| 17 Waren als Emoji statt Handwerk | das Werkstatt-Modul rechnet Warteschlangen richtig — es erscheint nur noch nicht im Fenster | Einhängen |
| Auftragssystem nur als Entwurf/Modul | keine Missionen auslösbar | Einhängen |
| Kampf nur als Modul | nicht aus dem Spiel auslösbar | Einhängen |
| Weltkarte nur als Rechenmodell | `src/welt.py` + `src/portalraum.py` (20 Dimensionen) sind fertig, im Fenster steckt aber noch das alte `MAPS`-Modell; keine Portalansicht | Einhängen |
| Oberfläche weicht vom Original ab | das Original-Menü ist belegt und wird gerade gegen unsere Liste gestellt | Einhängen |
| **Götterschutz endet laut Handbuch mit dem ersten Kriegspunkt** (neu entdeckt mit W6) | `src/punkte.py` setzt die **7 Tage** richtig um, lässt den Schutz aber nicht vorzeitig enden, wenn der Spieler Kriegspunkte sammelt. Steht in `punkte.vorschlaege()` — Frage 11 an Daniel | Einhängen |
| **Rundung der Gesamtpunkte offen** (W6) | „Gesamt = halbe Summe" ist belegt, die Rundung bei ungerader Summe nicht: das Modul rundet **ab** (VORSCHLAG) — Frage 10 an Daniel | Einhängen |
| kein Passworttor, keine `.exe` | ~~fehlt~~ **beides da** (04.10.2026): `.exe` mit Tor, Start belegt. Es fehlt nur noch der letzte Neubau nach dem Einhängen der Module | Einhängen + Neubau |

## 6. Nächste Schritte (in dieser Reihenfolge)

1. ~~**W4b-4 — Kartenerträge anbinden**~~ **erledigt am 04.10.2026.** `GameState.stundenertrag()`
   speist Zeitlauf und Anzeige aus `wirtschaft.ertrag_gesamt()`; 21 Prüfungen in
   `tests/test_ertrag_anbindung.py` (Holzfäller auf Wald 4/h, Steppe 2/h, zwei Felder 8/h,
   Bergbau Stufe 2 → 4,8/h). **Zwei Befunde dabei, beide behoben:** (a) das Wirtschaftsmodul liefert
   die Kennungen in Lesefassung („Holz") — der Zeitlauf fand sie nicht und schrieb stillschweigend
   nichts gut; jetzt wird an der Grenze umgeschrieben. (b) die fünf rohstofferzeugenden Gebäude
   (Holzfäller, Steinmetz, Jäger, Schmiede, Markt) sind aus der globalen Liste entfernt — sonst
   hätten beide Systeme denselben Rohstoff erzeugt.
2. ~~**Baupreise korrigieren**~~ **erledigt am 04.10.2026 (Commit `4b84544`).**
3. ~~**W4b-5 — die 20 Originalgebäude samt Wirkungen**~~ **erledigt am 04.10.2026 (Commit `a158175`).**
   Jede Wirkung kommt jetzt aus den bebauten Feldern der Siedlungskarten: Haus +5 Siedler je
   Siedlung, 1 neuer Siedler je Stunde (Heilkunde +10 % je Stufe), Bibliothek schaltet die Forschung
   frei und steht nur auf Grasland/Steppe/Nebelsee, Kriegerakademie/Diebesgilde/Stellmacher bilden
   die passenden Einheiten aus (Stufe = Tempo), der Verteidigungswall trägt 10 Stufen samt
   Schwellenwerten und Kriegspunkten. Ausbauen geht auf der Karte (Wall bis 10, Bibliothek und
   Ausbildungsstätten bis 5 — **Vorschlag**, das Handbuch nennt keine Zahl). Die fünf erfundenen
   globalen Gebäude sind entfallen. **103 Prüfungen** in `tests/test_gebaeude_wirkung.py`,
   Gesamtlauf 630 bei 0 Fehlern und 1 bekanntem Befund. **Drei ehrliche Nebenfund:** der
   erfundene Portal-Bau ist weg (weitere Karten schaltet jetzt die Forschung „Vermessung" frei);
   die `max_je_siedlung`-Regel aus dem Original wird nun durchgesetzt; und beim Nachprüfen fiel auf,
   dass `src/forschung.py` und `src/welt.py` zwar fertig, aber im Spiel **nicht eingehängt** sind.
4. **Einhängen — die Reihenfolge** (Hauptagent, in einer neuen Sitzung): `src/spielschicht.py` ist die
   tkinter-freie Fassade für genau diesen Schritt (133 Prüfungen). Ihre ehrlichen Lücken stehen in
   `spielschicht.offene_luecken()` und sind beim Einhängen zu schließen:
   (a) **Kampfverluste**: `kampf.py` ist in der Fassade nicht eingebunden — `angriff()` nutzt
   `kampfbericht`, aber Einzelverluste je Einheit fehlen;
   (b) **Ausbildungsdauer**: das Handbuch nennt keine, deshalb bildet die Fassade sofort aus;
   (c) **Portal-Mana**: der Zustand führt EINEN Mana-Vorrat, das Original verlangt die 5.000 Mana
   **aus einer Siedlung** — je Siedlung nachziehen;
   (d) **`auftrag_starten` fehlt absichtlich**, weil `src/auftraege.py` beim Bau der Fassade noch
   nicht existierte (Kind WA liefert es nach) — nach dem Einbau dort anschließen.
   Achtung bei den Bots: `botkern.handelspreis()` erwartet den **Referenzpreis** und rechnet nur das
   Temperament (±10 %); der Faktor ×1,2 sitzt in `botkern.referenzpreis_aus_beschaffung()`.
5. ~~**W4b-6 — Produktionsfaktor für alle neun Rohstoffe**~~ **erledigt am 04.10.2026 (Commit `c0f4a5d`).**
   `bonus_system.get_production_multiplier` holt die Faktoren aus `forschung_wirkung`; im Spiel stehen
   jetzt die **21 Originalforschungen**. Offen bleibt nur die belegte Bauregel „Baukunst nötig"
   (dafür müsste die Bibliotheksstufe die Baurechte steuern — eigener kleiner Schritt) und die
   Forschungsvoraussetzungen der Einheiten (z. B. Kriegskunst für den Kämpfer).
6. **W4c-Nachtrag — Forschung mit Wartezeit**: `src/forschung.py` (Dauer = Stufe² Stunden, Stufe
   steigt erst nach Ablauf) in die Oberfläche einhängen; die Fassade `spielschicht` rechnet es schon
   richtig, `main._start_research` steigt aber noch sofort.
7. **W5-2 — Portalansicht einhängen**: `src/portalraum.py` (20 Dimensionen, 5.000 Mana, 24-h-Sperre)
   ersetzt das alte `MAPS`-Modell im Portalreiter.
8. **WA — Auftragssystem**: `src/auftraege.py` ist **noch nicht gebaut** (Kind neu gestartet, nachdem
   der erste Lauf abgebrochen wurde). Nach dem Eintreffen einhängen: Reisezeit, Rückkehr, Beute.
9. **W2b — Kampf ins Spiel**: `src/kampfbericht.py` (Vorrunden-Schwellen, Mauerschaden, Beute,
   Bericht) mit einer Angriffs-Schaltfläche verbinden und den Bericht in die Nachrichten legen.
10. **W3 — Waren im Fenster**: `src/werkstatt.py` in einer Ansicht (Warteschlangen, parallele
    Werkstätten) sichtbar machen.
11. **W8 — robustes Speichern**: `src/speichern.py` + `tests/test_speichern_robust.py` sind **fertig und
    von mir nachgerechnet** (95 grün, 5 ehrliche Befunde: keine Dateisperre gegen zwei Schreiber,
    Klartext, kein Verzeichnis-Sync). Jetzt **in `main.py` einhängen** (statt des direkten Schreibens).
12. **W7 — Oberfläche**: `src/oberflaeche_original.py` + `data/menue_original.json` + Prüfdatei sind
    **fertig und nachgerechnet** (64 grün; einen echten Fehler im Kind-Test selbst gefunden und
    behoben — es suchte das Wort „tkinter" auch in der Beschreibung). Danach die Menüordnung nach der
    belegten Liste nachbauen (Netz-Einträge bleiben draußen).
13. **W9 — Auslieferung**: `.exe` **neu bauen** (`tools/build_exe.py`) und erneut startprüfen.
14. **Karten und Weltdaten sichern**: an jedem Paketende `python tools/protokoll_sichern.py --protokoll`.

## 7. Offene Entscheidungen (Daniel)

**Entschärft:** Baupreise — vier Gebäude sind jetzt belegt (Abschnitt 3). Offen bleibt nur die
Bepreisung der übrigen, deren Menüeintrag wir nicht im Bild haben.

**Neu aus W4b-5 (jeweils mit Vorschlag umgesetzt, damit das Spiel läuft — bitte bestätigen oder ändern):**

- **Ausbaustufen von Bibliothek und Ausbildungsstätten**: das Handbuch belegt, *dass* es Stufen
  gibt, nennt aber keine Zahl. Umgesetzt sind **5 Stufen** (wie die Forschungsstufen) — in
  `data/gebaeude_wirkung.json` änderbar. Der Wall hat die belegten **10**.
- **Höhe des Verteidigungsboni**: der Wall trägt jetzt den Bonus, aber die Zahl (+50 % je Stufe)
  stammt aus `bonus_system` und ist **nicht belegt** (vorher hing sie am erfundenen Wachturm).
- **Ausbildungsdauer**: das Handbuch nennt keine. Sie steht deshalb bei 0,5 Minuten, und die Stufe
  der Stätte verändert bisher nichts Messbares. Ohne Daniels Zahl bleibt das so.
- **Weitere Karten**: schaltet jetzt die Forschung **„Vermessung"** frei (der erfundene
  Portal-Bau ist entfallen). Alternative wäre eine eigene Portalmechanik nach `docs/welt.py`.
- **Siedlergrenze**: 10 je Siedlung + 5 je Haus (belegt); **vor** der ersten Siedlung 10
  (Startwert). So ist der Spielstart bewohnbar — bitte bestätigen.

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

## 9. Guthaben (Stand 22:15)

| Konto | Stand | Regel |
|---|---|---|
| OpenAI (astra) | **5,56 USD verfügbar** — 3,33 USD am 04.10. verbraucht (gemessen über `/v1/organization/costs?group_by=line_item`), von Daniel von der Billing-Seite abgelesen; Auto-Recharge aus, keine Schulden möglich | nur noch für Bilddeutung |
| DeepSeek | 3,32 USD (**nicht nachgeprüft** — der Schlüssel liegt nur in Hermes, nicht in der Shell des Agenten) | ein kleiner Rest **muss** bleiben |
| Kosten je Auftrag | v4-pro 0,04–0,12 USD · astra 0,47 USD (3 Bilder). **Größter Posten sind die Cache-Schreibkosten** (3,56 gegen 0,94 USD Ausgabe) → Aufträge kurz halten | `docs/ENTWICKLUNGSPROTOKOLL.md` (Abschnitt Kosten), Skill `kosten-schutzregel` |

**Kosten des Schritts W4b-5 (gemessen, nicht geschätzt):** Tagessumme vor dem Schritt
**8,81 EUR** (9,89 USD), danach **8,87 EUR** (9,96 USD) → **rund 0,06 EUR**
(`tageskosten_check.py --json`, summiert über **alle** Profile; die Differenz enthält jede Nutzung
im selben Zeitfenster). Es wurde **kein** teures Modell eingesetzt: kein `gpt-6-astra` (Bilddeutung
war nicht nötig — alle Angaben stehen in Handbuch und Datendateien) und kein `deepseek-v4-pro`.

**Zur 4-EUR-Regel:** die Tagessumme liegt mit 8,87 EUR über dem normalen Limit von 4 EUR. Für
diesen Auftrag („Nebelseetal Remake so gut wie möglich") hat Daniel die Tagesregel ausgesetzt —
nachzulesen im Skill `kosten-schutzregel` („laufende Ausnahme"). Außerhalb dieses Auftrags gilt die
4-EUR-Regel unverändert.

## 10. Dauerhaftes Arbeitssystem

| Baustein | Wo |
|---|---|
| `docs/PROJEKT_STAND.md` | dieses Dokument — Wiederaufnahme ohne Chatverlauf |
| `docs/AGENTEN_PLAN.md` | **wie die Sitzung ihre Agenten aufteilt und welches Modell wann** — inklusive Auftragsvorlage zum Kopieren |
| `docs/BOARD.md` | **Tagebuch des Koordinators für Daniel** — was die Kinder gemeldet haben. Kein Brett der Kinder (Vorgabe Daniel 04.10.2026) |
| `docs/LEHREN.md` | **ehrliche Nachlese** der Sitzung: 13 Fehler, was gut lief, was dauerhaft gilt |
| `docs/ENTWICKLUNGSPROTOKOLL.md` | **laufendes Protokoll** der groben Arbeitsschritte **mit Kosten** (Daniel schreibt die Entstehung mit) — nach jedem Schritt fortschreiben |
| `docs/ORDNUNG.md` | was wohin gehört |
| `docs/audits/` + `eingaben/` | alle Modelldaten (Abschnitt 4) |
| `tests/` (dreizehn Dateien) + `run_tests.bat` | Wahrheitsquelle „läuft es noch?" — Stand 04.10.2026: **691 Prüfungen, 0 Fehler, 1 Befund** |
| Skills `multi-agent-coding`, `kosten-schutzregel`, `nebelseetal-remake` | Betriebs- und Projektwissen |
| Kanban-Board `nebelseetal` | Paketliste (Verteiler braucht laufendes Gateway) |
| `D:/Arbeiten/_Quarantaene/` | alte Builds (dort: `Nebelsee Memory.exe` mit README) |

## 11. Letzte Commits

| Commit | Inhalt |
|---|---|
| `a1f224a` | **W3 Werkstatt + 17 Originalwaren** eingehängt; Verdrahtungsprüfer und GUI-Fehler-Test aufgenommen (1798/0/15 über 27 Dateien), EXE-Neubau |
| `ff87d75` | **W5-2 Portalraum** eingehängt; astra-Rat gesichert und mit gemessenen Kosten belegt (0,3444 USD) |
| `b14f7f5` | **W6 Punkte + W2/W2b Kampf** eingehängt; zwei Verdrahtungs-Prüfdateien (1734/0/14 über 25 Dateien) |
| `9ec34fb` | **W8 robustes Speichern** eingehängt (Schritt 1 des Umsetzungsplans) |
| `ca6970e` | W4b-5 dokumentiert: Übergabe, Brett und Entwicklungsprotokoll mit Kosten |
| `a158175` | **W4b-5**: die 20 Originalgebäude wirken aus den Siedlungskarten (630 Prüfungen grün) |
| `fb2ec06` | Kosten ins Entwicklungsprotokoll, falsche Kontostände richtiggestellt |
| `26c0149` | Entwicklungsprotokoll eingeführt (Daniel schreibt die Entstehung mit) |
| `472704f` | W4b-4: Kartenerträge liefern wirklich Rohstoffe (526 Prüfungen grün) |
| `4b84544` | Baupreise auf die BELEGTEN Originalwerte korrigiert + Siedler als Baukosten |
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
