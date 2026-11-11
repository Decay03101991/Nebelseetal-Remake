# Prüfung der Claude-Lieferung zur Präsentation (11.11.2026)

**Was geprüft wird:** die Lieferung von Claude Opus 5.5 zu `AUFTRAG_CLAUDE_DESIGN_20261111.md` (Register 397).
**Ablage der Lieferung:** `docs/eingaenge/LLM_20261111_PRAESENTATION/` — drei Dateien, hashgleich vom Desktop
übernommen:

| Datei | Byte | SHA256 |
|---|---:|---|
| `NEBELSEETAL_PRAESENTATION_BEFUNDE_20261111.md` | 43.380 | `04e3cfc23c2aac56…` |
| `README.md` (Entwurf) | 11.805 | `bf3215e1228fcf5d…` |
| `index.html` (Entwurf) | 15.801 | `2c3543bc83b6a803…` |

**Verfahren:** Auftrag, Befunde, beide Entwürfe gelesen; **jeder Befund, der eine Datei oder Zahl im Projekt
behauptet, selbst nachgemessen.** Nichts aus der Lieferung wurde übernommen — sie liegt als Vorschlag.

---

## 1. Was die Lieferung taugt

Claude hat den Auftrag ernst genommen: keine Erfindungen, jede Behauptung mit Datei und Zeile, eigene
Unsicherheiten offen (`UNBEKANNT`, weil GitHub und Pages aus seiner Sitzung nicht erreichbar waren), zwei
der zehn Verdachte des Auftrags **widerlegt** (V6 Web-Logo-Gewicht, V9 PDF unverlinkt) und einen
**Nebenbefund** gefunden, den wir nicht im Blick hatten (der Windows-Workflow sucht eine Datei, die das
Bauwerkzeug nie erzeugt).

Die zwei Entwürfe sind brauchbar: vollständiges README, vollständige `index.html`, ohne fremde Schriften,
ohne Tracking, mit gerechneten Kontrasten und einem Bildplatz mit klarer Anforderung.

## 2. Meine Nachmessung — was hält, was nicht

### 2.1 Bestätigt (selbst gemessen)

| Befund | Meine Messung |
|---|---|
| Startseite ist veraltet | Pages liefert 7.116 Byte mit Titel »0.5.0-pre.1« und Link auf `releases/latest`; die Repo-Datei hat 10.122 Byte, »V_0.0.3« und den Tag-Link |
| README nennt falsche Dateinamen | `README.md:35/37` nennt `Nebelseetal_Remake_0.5.0-pre.1.zip` und `Nebelseetal_Remake.exe`; `data/version.json` führt `Nebelseetal_Pre_Release_V_0.0.3.exe` |
| Infodateien im ZIP sind alt | `release_vorlage/START_HIER.txt:1/5`, `BEKANNTE_GRENZEN.txt`, `SYSTEMANFORDERUNGEN.txt`: durchgehend `V_0.0.1`, »rund 82 MB« (das ZIP hat 101.818.049 Byte) |
| README behauptet, Werkzeuge/Prüfungen/Doku lägen nicht im Repo | `git ls-files`: `tests/` **224**, `tools/` **68**, `docs/` **811** Dateien — sie liegen drin |
| `VORSCHAU.md` zeigt 12 kaputte Bilder | alle zwölf `src=` zeigen auf `assets/hintergrund_content_20261104/…`; das Verzeichnis existiert nicht mehr |
| 8 Dateien in `assets/original/` sind keine Bilder | je 236 Byte, Inhalt `<!DOCTYPE HTML … <title>404 Not F` |
| Keine Schriftdatei im Repo | 0 Treffer für `*.ttf`, `*.otf`, `*.woff*` bei 1.741 versionierten Dateien — die Blackletter-Überschrift hängt an einer installierten Schrift |
| Windows-Workflow würde scheitern | `windows-test-exe.yml:28` erwartet `release_public\Nebelseetal_Remake_Testversion.exe`, `tools/build_public_exe.py:43/92` erzeugt `<dateiname aus version.json>` = `Nebelseetal_Pre_Release_V_0.0.3.exe/.zip` |
| Web-Gold und Spiel-Gold sind zwei Welten | `index.html:9-11` (`#edce87`/`#12161c`) gegen `main.py:3788-3800` (`#FFCC33`/`#2a0605`) |

### 2.2 Der schwerste Befund: Urheberrecht an den Originalquellen

Claude schreibt, der Rechte-Satz des README (»Die Bilder des historischen Originalspiels sind nicht Teil
dieses Projekts«) halte nicht. **Das ist bestätigt und wiegt schwerer als alles andere in dieser Lieferung.**

Im **öffentlichen** Repository liegen (alle versioniert, alle nachgemessen):

| Was | Wo | Anzahl |
|---|---|---|
| Spielanleitung des Originals von 2009 als PDF | `docs/original/Nebelseetal_Spielanleitung_2009.pdf` | 1 |
| Handbuchbilder | `docs/original/handbuch_bilder/` | 244 |
| Website-Grafiken des Originals | `docs/original/assets_website/`, `karten/`, `karten_sammlung_odt/` | mitgezählt in 424 |
| GameStar-Material | 33 versionierte Dateien mit `gamestar` im Pfad | 33 |
| Historische Spielfeldbilder | `assets/karten/original/` | 127 |
| **Aus ihnen abgeleitete** aktive Spielfeldbilder | `assets/karten/spielfeld/` | 127 |

**Das ist keine Kleinigkeit:** es geht um fremde Handbücher, fremde Website-Grafiken und Material einer
Zeitschrift in einem Repo, das jeder abrufen kann. `docs/BILDINVENTAR.md` sagt es selbst: »Historische
Originalgrafiken möglicherweise urheberrechtlich geschützt – Nutzung/Weitergabe separat klären.«

**Wichtig für die Entscheidung:** ein Entfernen aus dem Arbeitsbaum nimmt die Dateien **nicht** aus der
Git-Historie. Wer sie wirklich aus dem öffentlichen Repo haben will, braucht einen Geschichts-Schnitt
(Force-Push) — das ist ein eigener, großer Schritt und **nicht** Teil dieser Sitzung.

### 2.3 Wo die Lieferung selbst irrt

Das neue README trägt **vier Sätze weiter, die am heutigen Code falsch sind** — genau die, die mein
Gesamtaudit gemessen hat (Register 401) und die Claude selbst als Befund 1 und 2 nannte, aber im Entwurf
stehen ließ:

| Satz im Entwurf | Heute gemessen |
|---|---|
| »20 Limbus-Dimensionen, sechs belegt, 14 leer« | `data/welten.json` führt **6** Dimensionen, **keine** leer |
| »Handelspunkte … werden noch nicht gebucht und stehen auf null« | werden gebucht (`main.py:5376`) |
| »Diplomatie erst zur Hälfte: Verträge, Rache und die drei Ereignisse … nicht eingebaut« | `pakt_anbieten` gebaut (`main.py:14633/14736`), Rache in `diplomatie.py:403-521` |
| »Drei Kampfregeln fehlen: Fluchtformel, Beute-Reihenfolge (Gold zuerst), Mauerreparatur mit Bauzeit« | Beute-Reihenfolge **ist gebaut** (`kampfbericht.beute_staffel`, Gold-Vorrang), Mauerreparatur **ist gebaut** (`main.py:4094/4111`, `reparatur_tick`) — offen bleibt allenfalls die Fluchtformel |

Dazu zwei Kleinigkeiten: der Entwurf nennt `data/resources.json` als Quelle für Siedlungen und Rohstoffe,
obwohl die gelesenen Werte in `data/gebaeude_wirkung.json` stehen (Register 401, D1); und er verlinkt
`VORSCHAU.md` mit dem Vermerk »erst reparieren«. Die eingebundene Datei
`assets/bilder/daniel_portrait_klein.png` **existiert** (14 Einträge in `assets/bilder/`, geprüft) — hier
war meine erste Annahme falsch.

## 3. Was ich übernehmen würde — Vorschlag mit Reihenfolge

**A. Sofort und ohne Risiko (nur Texte, die heute Unwahres sagen):**
1. Die vier falschen Sätze im README durch die gemessenen ersetzen (Register 401).
2. Version und Dateinamen aus `data/version.json` in README, `index.html` und `release_vorlage/*.txt`.
3. Den Speicherordner richtigstellen: `%LOCALAPPDATA%\Nebelseetal_Remake\Demo`.
4. Den Satz über Werkzeuge/Prüfungen/Doku richtigstellen (sie **liegen** im Repo).
5. **Eine Wache bauen**, die README, `index.html` und `release_vorlage/` gegen `data/version.json` prüft —
   das ist Claudes dritte »stärkste Idee« und verhindert genau diese Klasse für immer.

**B. Danach (Gestaltung, gut vorbereitet durch die Lieferung):**
6. Die neue `index.html` mit der **Spielpalette** übernehmen (nach Korrektur der vier Sätze und der
   Portrait-Datei) und neu ausrollen — der größte sichtbare Gewinn.
7. Das neue README übernehmen, ebenfalls korrigiert.
8. `VORSCHAU.md` reparieren oder aus der Verlinkung nehmen; die acht 404-GIFs entfernen.

**C. Nicht in dieser Sitzung:** Pages-Ursache klären (Quelle und letzten Build ansehen — das geht nur in den
Repo-Einstellungen), Social Preview und Topics setzen, Screenshot aufnehmen, Geschichts-Schnitt wegen der
Originalquellen.

## 4. Was Daniel entscheiden muss

1. **Originalquellen im öffentlichen Repo** (Abschnitt 2.2) — die eine Frage, die alles andere überholt.
2. Ob die neue Startseite und das neue README übernommen werden (Vorschlag: ja, korrigiert).
3. Ob ein Screenshot aus V_0.0.3 gemacht werden soll — und von wem.
4. Ob die Beschreibung, die Topics und die Lizenz in den GitHub-Einstellungen gesetzt werden (das kann nur
   Daniel bzw. ein Token mit Schreibrecht auf die Einstellungen).

## 5. Belege

- Lieferung hashgleich: `sha256sum` beider Fassungen (Desktop und `docs/eingaenge/…`) am 11.11.2026, 14:35
- Eigene Messungen: `git ls-files` (Dateizahlen), `grep`/`read` an den genannten Stellen, `ls -la assets/original`
- Prüfung der `VORSCHAU.md`-Ziele: zwölf `src=`, zwölf fehlende Ziele
- Gesamtaudit-Grundlage: `docs/audits/GESAMTAUDIT_20261111.md` (Register 398 bis 402)
