# AUFTRAG an Claude (Klasse Opus 5.5): Präsentation und Eigenstil des Nebelseetal-Remakes

**Stand:** 11.11.2026, 13:47. **Auftraggeber:** Daniel Kössl. **Vorbereitet von:** Weltenfresser (Hermes-Agent).
**Zustand:** fertig zum Hochladen. Dieses Dokument ist die einzige Unterlage, die du bekommst — alles Weitere
holst du dir selbst aus dem Repository.

---

## 0. In einem Satz

Sieh dir das öffentliche Repository unseres Spiels an, prüfe seine Präsentation so weit du Zugang hast, und
liefere uns **einen fertigen, einbaubaren Entwurf** (README und Startseite) im eigenen Stil des Spiels —
mit belegten Befunden, gemessenen Zahlen und ohne Erfindungen.

## 1. Deine Rolle

Du bist **Gestalter und Prüfer**, nicht Erfüllungsgehilfe. Was du nicht nachsehen konntest, nennst du
UNBEKANNT. Was du gemessen hast, nennst du mit Zahl und Quelle. Du lobst nicht und schreibst keine
Einleitung — du lieferst Befunde und Entwürfe.

Du arbeitest **nur lesend** am Repository. Du änderst nichts, du schlägst vor. Was wir übernehmen, entscheiden
wir.

## 2. Verbote (hart)

1. **Keine Erfindungen.** Keine Dateinamen, Pfade, Zeilennummern, Bildnamen, Farben oder Zahlen, die du
   nicht abgerufen oder gerechnet hast. Jede Behauptung über das Repository trägt ihre URL.
2. **Kein Marketing-Sprech.** Keine Superlative, kein »revolutionär«, keine Werbetexte. Dieses Projekt wirbt
   nicht mit Lautstärke, sondern mit Genauigkeit und Atmosphäre.
3. **Keine Rechteverletzung.** Das Logo und die Bildwelt stammen von **Chris Fred Däubner** und stehen unter
   seinem Urheberrecht. Du darfst sie **verwenden wie sie sind** und ihre Einbindung vorschlagen — aber
   **nicht** verändern, zuschneiden, umfärben, neu generieren oder als Vorlage für ein neues Logo nehmen.
   Ebenso unantastbar: der Hinweis auf seine Instagram-Seite und die Nennung seines Namens.
4. **Keine fremden Bilder als Ersatz.** Kein Stock-Foto, kein KI-Bild als Vorschlag, das nicht im Repository
   liegt. Wenn du eine Bildidee hast, beschreibst du sie als Anforderung an einen Illustrator.
5. **Nichts behaupten, was du nicht geprüft hast.** Wenn du eine Seite nicht öffnen konntest, steht dort
   UNBEKANNT (Grund) — nicht »sieht gut aus«.

## 3. Zugang: das öffentliche Repository

| Was | Wo |
|---|---|
| Repository | `https://github.com/Decay03101991/Nebelseetal-Remake` (öffentlich, keine Anmeldung nötig) |
| Branch | `main` |
| Stand, den dieser Auftrag beschreibt | Commit `b35ac2e` (11.11.2026) — falls `main` weiter ist, prüfe den neuen Kopf und sag es |
| Rohdateien (maschinenlesbar) | `https://raw.githubusercontent.com/Decay03101991/Nebelseetal-Remake/main/<pfad>` |
| Veröffentlichte Startseite | `https://decay03101991.github.io/Nebelseetal-Remake/` |
| Releases | `https://github.com/Decay03101991/Nebelseetal-Remake/releases` |
| Docker/CI | `.github/workflows/windows-test-exe.yml` (manueller Windows-Bau), `.github/ISSUE_TEMPLATE/fehlerbericht.md` |

Arbeite **über die URLs**, nicht über Vermutungen. Wenn du Dateien nicht abrufen kannst, sag es.

## 4. Das Projekt in Zahlen (von uns gemessen am genannten Commit)

**Was das Spiel ist:** Einzelspieler-Remake eines historischen deutschen Browserspiels (Original 2009,
Vorversion 2006). Python 3 + tkinter, JSON-Spielstand, Windows-Testversion als `.exe`, offline, kostenlos,
kein Konto. Sechs Welten im »Limbus«, fünf KI-Nachbarn mit eigener Wirtschaft, kein Sieg, sondern vier
Auszeichnungen. Vollständige Anleitung im Spiel.

**Repository (gemessen):**

| Größe | Wert |
|---|---|
| Versionierte Dateien | 1.741 |
| GitHub-Größe | 201.421 KB (≈ 197 MB) |
| Sprache | Python |
| Angelegt | 04.11.2026 |
| Sterne / Forks / offene Issues | 0 / 0 / 1 |
| Lizenz | **keine** (`license: null`) |
| Topics | **leer** (`topics: []`) |
| Beschreibung | »Einzelspieler-Remake des historischen Browsergames Nebelseetal - erster Pre-Release **0.5.0-pre.1** (Windows-Testversion)« |
| Homepage-Feld | `https://decay03101991.github.io/Nebelseetal-Remake/` |
| Wiki | aus |

**Dateien, die die Präsentation tragen (Byte, gemessen):**

| Datei | Byte | Rolle |
|---|---|---|
| `README.md` | 9.545 | die Hauptseite des Repos |
| `index.html` | 10.122 | die veröffentlichte Startseite (GitHub Pages) |
| `SPIEL_ERKLAERUNG.md` | 3.531 | »was das Spiel ist — und was es nicht ist« |
| `BESUCHER.md` | 5.880 | Entstehung, Arbeitsweise, Sicherheit |
| `FRAKTIONEN_WELTEN.md` | 6.413 | sechs Häuser, sechs Welten |
| `VORSCHAU.md` | 3.322 | erste Eindrücke einer späteren Version |
| `CHRONIK_DER_WELT.md` | 72.781 | die Geschichte der Welt als Buch |
| `CHRONIK_DER_WELT.pdf` | 9.770.115 | dieselbe Chronik als PDF |
| `.nojekyll` | — | GitHub Pages ohne Jekyll |

**Bilder im Repository (gemessen):** `assets/` = 497 Dateien, 63 MB, in sieben Ordnern:
`icons/` 194 (davon `icons/burgen/` mit Burg- und Wappenbildern), `karten/` 254, `bilder/` 13,
`referenzbilder/` 17, `quellbilder/` 10, `original/` 8, `loadingpage/` 1. Die schwersten Dateien:
`assets/referenzbilder/Logo_Nebelseetal_20261106.png` 6.645.755 Byte (3500 × 3500, freigestellt),
`assets/bilder/logo_nebelseetal_klein.png` 1.324.807, zwei Fraktions-Panoramen als JPG ≈ 0,8–1,0 MB,
`assets/bilder/daniel_portrait.png` 612.608, Burg-Kacheln ≈ 0,4–0,5 MB je Stück.

**Releases (über die API gemessen):** vier Stück, **alle als Vorabversion markiert**
(`prerelease: true`), also auf der Releases-Seite erst nach Einblenden sichtbar:

| Tag | veröffentlicht | Assets |
|---|---|---|
| `v0.5.0-pre.1` | 04.11.2026 | `Nebelseetal_Remake_0.5.0-pre.1.zip` 85.516.122 Byte |
| `v_0.0.1` | 05.11.2026 | `.exe` 86.983.205 / `.zip` 86.701.024 |
| `v_0.0.2` | 05.11.2026 | `.exe` 86.984.365 / `.zip` 86.702.517 |
| `v_0.0.3` | 06.11.2026 | `.exe` **102.098.672** / `.zip` **101.818.049** |

## 5. Der heutige Präsentationsstand

### 5.1 Die veröffentlichte Startseite ist NICHT die Fassung aus dem Repository

Das ist der wichtigste gemessene Befund, bitte selbst nachprüfen:

- Ausgeliefert wird `https://decay03101991.github.io/Nebelseetal-Remake/` mit **7.116 Byte**, Titel
  `Nebelseetal Remake — Pre-Release 0.5.0-pre.1`, Unterzeile »Pre-Release **0.5.0-pre.1**«, Download-Knopf
  auf `…/releases/latest`.
- Im Repository liegt `index.html` mit **10.122 Byte**, Titel `… — Pre-Release V_0.0.3`, Unterzeile
  »Pre-Release **V_0.0.3** (06.11.2026)«, Download-Knopf auf `…/releases/tag/v_0.0.3`. Letzte Änderung an
  dieser Datei: 06.11.2026, 14:17 (Commit `c2e66dd`).
- **Folge:** Besucher sehen eine zwei Versionen alte Seite. Ob GitHub Pages nur nicht neu gebaut hat oder
  aus einer anderen Quelle liest, ist von außen nicht entscheidbar — **nimm es als Befund auf und nenne die
  möglichen Ursachen**, ohne eine zu behaupten.

### 5.2 Der Aufbau der Startseite (Fassung im Repository)

Dunkles Papier (`#12161c` / `#0b0e12`), Gold `#edce87`, Kupfer `#945c2b`, Stahl `#2a4556`, Text `#ece1cb`,
Fließtext in `Georgia, "Palatino Linotype", serif`, Überschriften mit Gold-Verlauf, goldene Leiste oben
(64 px), Kästen mit Kupfer-Rahmen und Schatten, zwei Knöpfe (»Testversion herunterladen« / »Quellcode
ansehen«), Abschnitte: Was das Spiel will · Was in dieser Vorabversion steckt · Was noch fehlt — ehrlich ·
Weiterlesen (Tabelle) · Fußzeile. Der vollständige Quelltext:
`https://raw.githubusercontent.com/Decay03101991/Nebelseetal-Remake/main/index.html`

### 5.3 Das README

Aufbau: Titel · Logo (`assets/bilder/logo_nebelseetal_klein.png`, Breite 720) · Ein-Satz-Beschreibung ·
Vorabversions-Hinweis · **Was das Spiel ist** · **Diese Version herunterladen und starten** (fünf Schritte) ·
**Was in diesem Repository liegt** (Tabelle Ordner/Inhalt) · **Herkunft und Transparenz** (welche KI wofür,
Gesamtausgaben rund 52 US-Dollar, Rolle des Agenten »Weltenfresser«) · **Bekannte Grenzen** · **Rechte** ·
**Fehler melden**. Kein Badge, kein Screenshot des Spiels, keine Inhaltsleiste, kein englischer Text.

### 5.4 Woran man den Eigenstil heute erkennt

Schwarze Buchschrift (Blackletter) für Überschriften im Spiel, Gold auf dunklem Rot-Braun, das Nebelmeer als
Grundstimmung, gemalte Panoramen und Kacheln, Wappen statt Symbole, ein Passworttor als erster Bildschirm.
**Im Web ist davon fast nichts angekommen:** die Startseite ist eine saubere, dunkle Textseite in
Serifenschrift — sie könnte zu jedem Fantasy-Projekt gehören.

## 6. Was die Gestalt des SPIELS vorgibt (gemessen am Code)

Diese Werte sind die Farbwelt, gegen die ein Web-Auftritt stimmig sein muss (`src/main.py`, Skin `standard`):

| Rolle | Wert |
|---|---|
| Grund | `#2a0605` (sehr dunkles Rotbraun) |
| Fläche / Panel | `#3e1c1a` |
| Gold (Schrift, Rahmen) | `#FFCC33` |
| Rot (Warnung, Kampf) | `#e53935` |
| Text | `#FFFF99` |
| Kopf-/Seitenleiste | `#1a0a09` |
| Knopf | `#3e2723`, aktiv `#5D4037` |
| Rahmen | `#4a1512` |
| Unterzeile / Akzent | `#FF6600` |
| Schrift der Überschriften | `Blackletter` (im Spiel); Fließtext Systemschrift |
| Weitere Skins im Spiel | ein grüner (`#0d1f0d` / `#8BC34A`) und ein roter (`#1f0d0d` / `#FF5722`) |

Die Web-Fassung benutzt heute eine **andere** Palette (Gold `#edce87`, Kupfer `#945c2b`, Papier `#12161c`) —
näher an einem edlen Buch als am Spiel. Ob das bleiben soll oder ob Web und Spiel dieselbe Palette tragen
sollen, ist **eine deiner Kernfragen**.

## 7. Die zwei Leitplanken

**Rechte.** Logo und Bildwelt: Chris Fred Däubner (unverändert, mit Namensnennung; Instagram-Link
`https://www.instagram.com/three_ghosts.mp4` steht auf seinen Wunsch im README und ist die einzige Stelle,
die auf seine Seite führt). Bilder des historischen Originalspiels sind **nicht** Teil des Projekts.

**Ton.** Das README nennt offen, was fehlt (fehlende Kampfregeln, kein Ton, nur Windows getestet, keine
macOS-Fassung). Diese Ehrlichkeit ist eine Entscheidung, kein Zufall — **ein Vorschlag, der sie durch Werbung
ersetzt, ist unbrauchbar.** Atmosphäre darf sein, Prahlerei nicht.

## 8. Was du prüfen und testen sollst

Jeder Punkt zählt nur, wenn du ihn wirklich gemacht hast. Schreib hinter jeden Punkt, was du gefunden hast
oder UNBEKANNT (Grund).

1. **Startseite aufrufen** (Pages-URL) und mit `index.html` aus dem Repo vergleichen — Titel, Version,
   Download-Ziel, Abschnitte. Wie groß ist der Unterschied? Was fehlt Besuchern?
2. **README auf GitHub ansehen** (nicht nur roh): rendert das Logo in der richtigen Breite? Sind Tabellen
   lesbar? Gibt es Sprungmarken, die ins Leere zeigen?
3. **Alle Links prüfen**, die in `README.md` und `index.html` stehen: erreichbar (HTTP-Status), richtiges
   Ziel (Tag, Datei)? Besonders die Download-Ziele.
4. **Release-Seite prüfen:** Wirken vier Vorabversionen ohne stabile Fassung? Ist der Download in zwei Klicks
   erreichbar? Wie wirkt die Dateigröße von rund 100 MB?
5. **Gewicht der Bilder:** Summe der Bilder, die eine Startseite laden müsste; welches Bild ist zu schwer für
   Web (Logo 6,6 MB Original, 1,3 MB Web-Fassung)? Welche Formate fehlen (WebP/AVIF)?
6. **Kontrast messen:** Für die vorgeschlagene Palette je Schrift/Hintergrund-Paar das
   Kontrastverhältnis rechnen (WCAG-Formel) und Paare unter 4,5 : 1 benennen.
7. **Mobil:** Startseite und README bei 360 px Breite beurteilen (Umbruch, Knöpfe, Tabellen, Lesbarkeit).
8. **Deutsch und Typografie:** Umlaute, Anführungszeichen, Gedankenstriche, Zahlenformate, Einheiten.
9. **GitHub-Metadaten:** Beschreibung, Topics, Lizenz, Homepage-Feld, Social-Preview — was fehlt, was
   widerspricht sich? (Die Beschreibung nennt 0.5.0-pre.1, aktuell ist V_0.0.3 — prüfe, ob das noch stimmt.)
10. **Namen und Wege:** README nennt `Nebelseetal_Remake.exe` und `Nebelseetal_Remake_0.5.0-pre.1.zip`; die
    Release-Dateien heißen `Nebelseetal_Pre_Release_V_0.0.3.exe` / `.zip`. README nennt den Speicherordner
    `%LOCALAPPDATA%\Nebelseetal_Remake\`. Prüfe jede dieser Angaben gegen das, was du im Repo findest
    (z. B. `release_vorlage/`, `data/version.json`, `tools/build_public_exe.py`) und sag, was nicht
    zusammenpasst.
11. **Erster Eindruck ohne Vorwissen:** Stell dir vor, du kennst das Spiel nicht. Was verstehst du nach 30
    Sekunden? Was fehlt dir (Screenshot? Ein-Satz-Pitch? »wie groß ist das?«)? Nenne die drei Fragen, die
    offenbleiben.
12. **Wiedererkennung:** Wodurch unterscheidet sich diese Präsentation heute von jedem anderen
    Indie-Fantasy-Repo? Wenn die Antwort »kaum« ist, sag es und begründe es.

## 9. Verdachtsliste (ausdrücklich Sichtung, nicht Urteil)

Diese Punkte sind uns beim Zusammenschreiben aufgefallen. Bestätige oder widerlege sie — **eigene Prüfung
schlägt unsere Vermutung:**

| # | Verdacht | Woher |
|---|---|---|
| V1 | Die veröffentlichte Startseite ist veraltet (0.5.0-pre.1 statt V_0.0.3) | Pages 7.116 Byte gegen `index.html` 10.122 Byte |
| V2 | Das README verweist auf Dateinamen, die es im aktuellen Release nicht gibt | README gegen Release-Assets |
| V3 | Die GitHub-Beschreibung nennt eine alte Version | API-Feld `description` |
| V4 | Topics und Lizenz fehlen, also findet und zitiert das Repo niemand | API-Felder `topics`, `license` |
| V5 | Vier Vorabversionen ohne stabile Fassung verwirren beim ersten Besuch | Release-API |
| V6 | Das Web-Logo ist mit 1,3 MB zu schwer (Original 6,6 MB) | Dateigrößen |
| V7 | Es gibt keinen einzigen Screenshot des Spiels in README oder Startseite | beide Dateien |
| V8 | Die Web-Palette (Gold `#edce87`) und die Spiel-Palette (Gold `#FFCC33`) sind zwei verschiedene Welten | Code gegen CSS |
| V9 | Die Chronik als PDF ist 9,7 MB schwer und liegt unverlinkt im Repo | Dateigröße, Links |
| V10 | Auf der GitHub-Seite fehlt jede soziale Vorschaukarte (Social Preview) | Seitenquelltext |

## 10. Pflicht-Ausgabeformat

Antworte **genau** in diesen sechs Teilen, in dieser Reihenfolge, auf Deutsch. Halte die Grenzen ein — sie
sind Absicht, damit die Antwort benutzbar bleibt.

**Teil A — Ist-Stand, 10 Zeilen.** Was ein Besucher heute sieht, in der Reihenfolge seines Weges
(Suche → Repo-Seite → README → Startseite → Release → Download). Je Zeile: was da ist, was fehlt.

**Teil B — Befunde, höchstens 15, als Tabelle.** Spalten: `Nr` · `Befund` (ein Satz) · `Beleg` (URL oder
Datei, bei Zahlen die Zahl) · `Wirkung` (was der Besucher dadurch verliert) · `Aufwand` (S/M/L) ·
`Priorität` (1 = sofort, 2 = bald, 3 = später). Kein Befund ohne Beleg. Verdachte aus Abschnitt 9, die du
widerlegst, erscheinen hier als »widerlegt« mit Beleg.

**Teil C — Der Entwurf: README, vollständig.** Eine Fassung, die Daniel Zeile für Zeile einsetzen kann:
Markdown, deutsche Sprache, gleiche ehrliche Haltung, aber mit Eigenstil. Muss enthalten: Logo-Einbindung
(mit Urheber-Zeile), Ein-Satz-Pitch, die fünf Startsätze, eine Tabelle »was steckt drin« mit den belegten
Zahlen, die ehrlichen Grenzen, Rechte, Fehler-melden. **Keine** Angaben, die du nicht belegen kannst — im
Zweifel schreibst du `PRÜFEN: <was>` in eckigen Klammern, damit wir es ersetzen.

**Teil D — Der Entwurf: Startseite, vollständig.** Eine einzelne `index.html`, ohne externe Abhängigkeiten
(kein CDN, keine Webfonts von fremden Servern, kein Tracking), die die Spielpalette aufnimmt oder begründet,
warum sie die Buchpalette behält. Mit: Kopfbereich mit Logo, ein Satz, was das Spiel ist, zwei Knöpfe,
»was steckt drin« in Zahlen, »was fehlt« ehrlich, ein Bildplatz für einen Screenshot mit klarer Anforderung
(Größe, Ausschnitt, was zu sehen sein muss), Fußzeile mit Rechten und Chris-Nennung. Responsiv ab 360 px,
Kontraste nach WCAG geprüft (Werte im Kommentar je Farbpaar).

**Teil E — Gestalt-Spezifikation.** Eine Tabelle mit Werten, die für Web und Spiel zusammenpassen:
Farbe (Hex), Rolle, wo sie gilt; Schrift (mit Begründung, warum keine fremde Webfont nötig ist); Abstände;
Ecken; Bildformate und Zielgewichte; Bildsprache in drei Sätzen. Je Wert ein Satz Begründung.

**Teil F — Was du nicht geprüft hast.** Jeder Punkt aus Abschnitt 8, den du nicht oder nur teilweise
machen konntest, mit Grund. Dazu: die drei stärksten Ideen in je einem Satz, und die eine Sache, die du
zuerst tun würdest.

## 11. Maßstab: was hier »Eigenstil« heißt

Nebelseetal ist ein Ort, kein Produkt: Nebelmeer, zersprungene Welt, Portale, sechs Häuser mit eigenen
Wappen, gemalte Panoramen, ein Passworttor als Schwelle, Gold auf dunklem Rotbraun, Buchschrift für Titel.
Ein Besucher soll nach zehn Sekunden wissen: **hier wurde etwas gemalt, nicht zusammengeklickt** — und nach
einer Minute wissen, was er bekommt, was fehlt und wo er klickt.

Ein Vorschlag ist gut, wenn er (1) mit den Bildern auskommt, die da sind, (2) die ehrliche Haltung behält,
(3) auf einem 360-px-Telefon funktioniert, (4) ohne fremde Schriften und ohne Tracking auskommt, und
(5) so konkret ist, dass Daniel ihn in einer halben Stunde einsetzen kann.

## 12. Abgabe

Antworte als Text in einem Stück (Abschnitte A bis F). Kein Vorwort, keine Zusammenfassung am Anfang, keine
Fragen an uns am Ende — wenn etwas fehlt, steht es in Teil F. Wir rechnen deine Befunde nach und melden
zurück, was wir übernehmen.
