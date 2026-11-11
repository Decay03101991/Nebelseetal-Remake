# AUFTRAG Nr. 2 an Claude (Klasse Opus 5.5): Präsentations-Konzept in drei Varianten

**Stand:** 11.11.2026, 17:08. **Auftraggeber:** Daniel Kössl. **Vorbereitet von:** Weltenfresser (Hermes-Agent).
**Zustand:** fertig zum Hochladen. Dieses Dokument ist die einzige Unterlage, die du bekommst.

---

## 0. In einem Satz

Liefere uns **drei durchdachte Konzepte** für den Auftritt des Spiels — keine fertigen Seiten, keinen Code —
und sage, welches du empfiehlst und warum. Was gebaut wird, entscheidet Daniel danach.

## 1. Deine Rolle

Du bist **Konzeptdenker und Prüfer**. Du entwirfst drei Wege, beschreibst sie so genau, dass man sie bauen
kann, und nennst ihre Schwächen ehrlich. Du lieferst **keine** fertige `index.html`, **kein** fertiges
README, keinen Code, keine Bilddateien. Was du nicht nachsehen konntest, nennst du UNBEKANNT (Grund).

## 2. Was seit deiner letzten Lieferung passiert ist — bitte zuerst lesen

Du hast am 11.11.2026 um 14:00 bereits eine Lieferung gemacht (Befunde und zwei Entwürfe). Wir haben sie
**vollständig nachgemessen**:

- **Neun deiner Befunde waren richtig**, zwei deiner Widerlegungen (Web-Logo-Gewicht, PDF unverlinkt) ebenfalls.
  Ein Nebenbefund von dir (der Windows-Workflow erwartet einen Dateinamen, den das Bauwerkzeug nie erzeugt)
  war neu für uns und stimmt.
- **Deine Entwürfe wurden NICHT übernommen.** Daniels Entscheidung, wörtlich: »Nichts übernehmen — erst
  eigenes Konzept«. Das ist kein Urteil über die Qualität, sondern über den Weg: erst die Richtung, dann die
  Ausführung.
- **Vier Sätze deiner Entwürfe waren am Code falsch** und sind inzwischen im echten README berichtigt:
  »20 Limbus-Dimensionen, 14 leer« (die Datei führt 6, keine leer), »Handelspunkte werden nicht gebucht«
  (werden sie), »Diplomatie-Verträge nicht eingebaut« (sind sie), »Beute-Reihenfolge und Mauerreparatur
  fehlen« (sind gebaut). Nimm das als Warnung für die nächste Lieferung: **prüfe Sätze, die du aus einer
  bestehenden Seite übernimmst, gegen den Code**, auch wenn sie plausibel klingen.

**In der Zwischenzeit behoben (von uns gemessen, Stand `628f5aa`):**

| Was war | Was ist jetzt |
|---|---|
| Startseite zeigte die Fassung vom 04.11. (0.5.0-pre.1) | Ursache: Pages stand auf »Deploy über Workflow«, es gab keinen Pages-Workflow. Jetzt Branch `main`, Ordner `/` — **live: 9.972 Byte, Titel »Pre-Release V_0.0.3«** |
| Beschreibung nannte 0.5.0-pre.1, keine Topics | Beschreibung nennt **V_0.0.3**; **zehn Topics** gesetzt (nebelseetal, browsergame-remake, aufbauspiel, singleplayer, offline, python, tkinter, windows, german, remake) |
| README nannte falsche Dateinamen, falschen Speicherordner, behauptete »Werkzeuge und Doku liegen nicht im Repo«, behauptete »Bilder des Originals sind nicht Teil des Projekts« | **Alle vier Stellen berichtigt.** README jetzt **10.488 Byte** |
| Originalquellen lagen im öffentlichen Repo (Handbuch-PDF, 244 Handbuchbilder, Website-Grafiken, 22 GameStar-Bilder, 127 historische Karten, 2 JPGs) | **478 Dateien aus dem öffentlichen Stand genommen** (liegen lokal in einer Ablage). Repo jetzt **1.272 versionierte Dateien** statt 1.741; `assets/` **370 Dateien, 58 MB**. Ein Geschichts-Schnitt (Force-Push) steht noch aus |
| Fünf Prüfdateien wurden rot, weil sie die entfernten Originale prüften | Wachen nachgezogen; **Sammellauf 218 von 218 grün**, 9.449 Prüfungen, 0 Fehler |

**Noch offen:** Lizenz (keine gesetzt), Social Preview (kann die API nicht), ein **Screenshot aus V_0.0.3**
(wird nach Daniels Test aufgenommen, 1600 × 900, ohne Windows-Rahmen).

## 3. Zugang

| Was | Wo |
|---|---|
| Repository | `https://github.com/Decay03101991/Nebelseetal-Remake` (öffentlich) |
| Branch / Stand | `main`, Commit **`628f5aa`** (11.11.2026, 17:03) |
| Rohdateien | `https://raw.githubusercontent.com/Decay03101991/Nebelseetal-Remake/main/<pfad>` |
| Startseite live | `https://decay03101991.github.io/Nebelseetal-Remake/` |
| Releases | `https://github.com/Decay03101991/Nebelseetal-Remake/releases` |
| Neu in dieser Fassung | `README.md` (berichtigt), `docs/audits/GESAMTAUDIT_20261111.md` (32 Befunde) |

## 4. Das Projekt in festen Zahlen

Einzelspieler-Remake eines historischen deutschen Browserspiels (Original 2009, Vorversion 2006).
Python 3 + tkinter, JSON-Spielstand, Windows-Testversion als `.exe`, offline, kostenlos, kein Konto.
Sechs Welten im »Limbus«, fünf KI-Nachbarn mit eigener Wirtschaft, **kein Sieg**, sondern vier
Auszeichnungen. Vollständige Anleitung im Spiel über den Berater.

| Größe | Wert | Beleg |
|---|---|---|
| versionierte Dateien | 1.272 | `git ls-files` |
| davon `docs/` / `tests/` / `tools/` | 468 / 224 / 68 | dito |
| `assets/` | 370 Dateien, 58 MB | `find`, `du` |
| GitHub-Größe | 204.453 KB | API-Feld `size` |
| `README.md` | 10.488 Byte | Dateisystem |
| `index.html` | 10.122 Byte | dito |
| `CHRONIK_DER_WELT.pdf` | 9.770.115 Byte | dito |
| Releases | 4, **alle Vorabversion** | API |
| neueste Fassung | `v_0.0.3`, EXE 102.098.672 / ZIP 101.818.049 Byte | API |
| Sterne / Forks / Issues | 0 / 0 / 1 | API |
| Lizenz | keine | API |
| Register (Prüfzeugnisse) | 409 Einträge, höchste Nummer 412 (Lücken 272, 273, 336) | `docs/PRUEFREGEL_ORIGINAL.md` |

**Bilder, die zur Verfügung stehen (Pfade im Repo):** `assets/bilder/` 13 (Logo als PNG **und** WebP,
Daniels Portrait groß und klein, Drachen, Marktplatz-Kennzeichen, ein Portal-Kopfband),
`assets/icons/` 194 (Menü-Icons, Burgen, Wappen), `assets/karten/` 127 (die aktiven Spielfeldkacheln),
`assets/referenzbilder/` 17 (u. a. das Logo-Original 3500 × 3500, 6,6 MB), `assets/quellbilder/` 10,
`assets/loadingpage/` 1. Die schwersten Dateien: Logo-Original 6.645.755 Byte, Logo-Webfassung 1.324.807,
zwei Fraktions-Panoramen als JPG ≈ 0,8–1,0 MB.

## 5. Die Gestalt des Spiels (gemessen am Code, `src/main.py`, Skin `standard`)

| Rolle | Wert |
|---|---|
| Grund | `#2a0605` |
| Fläche / Panel | `#3e1c1a` |
| Gold | `#FFCC33` |
| Rot (Warnung, Kampf) | `#e53935` (auf Grund nur 4,41 : 1 — als Schrift zu schwach) |
| Text | `#FFFF99` |
| Kopf-/Seitenleiste | `#1a0a09` |
| Knopf / aktiv | `#3e2723` / `#5D4037` |
| Rahmen | `#4a1512` |
| Akzent | `#FF6600` |
| Überschriften | `Blackletter` (im Spiel; **keine Schriftdatei im Repo** — fehlt sie auf dem Rechner, ersetzt Tk sie) |

Dazu im Spiel: goldene Leisten, ein Passworttor als Schwelle, gemalte Panoramen und Gebäudekacheln,
Wappen statt Symbole, das Nebelmeer als Grundstimmung.

## 6. Leitplanken

**Rechte.** Logo und Bildwelt: **Chris Fred Däubner**, unverändert, mit Namensnennung; der Instagram-Link
`https://www.instagram.com/three_ghosts.mp4` steht auf seinen Wunsch im README. Die Quellen des historischen
Originalspiels liegen **nicht mehr** im Repo und dürfen auch nicht als Bildvorschlag zurückkommen.

**Ton.** Das README nennt offen, was fehlt. Diese Ehrlichkeit ist eine Entscheidung. Atmosphäre ja,
Prahlerei nein.

**Technik.** Keine fremden Webfonts, kein CDN, kein Tracking. Bilder nur aus dem Repo oder als klare
Anforderung an einen Illustrator (Chris), nicht als KI-Bildvorschlag.

## 7. Was du prüfen musst, bevor du entwirfst

Jeder Punkt zählt nur, wenn du ihn wirklich gemacht hast; sonst UNBEKANNT (Grund).

1. Die **Startseite live** ansehen (Titel, Version, Download-Ziel, erster Bildschirm bei 360 px).
2. Das **README auf GitHub** ansehen (nicht nur roh): rendert das Logo, sind Tabellen lesbar, funktionieren
   die Sprungmarken `#rechte`, `#bekannte-grenzen`?
3. Den **Dateibaum** ansehen: welche Bilder gibt es jetzt wirklich (`assets/…`)? Was ist seit deiner letzten
   Lieferung verschwunden?
4. Die **Release-Seite**: vier Vorabversionen, ~100 MB, Download in zwei Klicks?
5. **Kontraste rechnen** für jede Palette, die du vorschlägst (WCAG-Formel, Paare unter 4,5 : 1 benennen).
6. **Erster Eindruck ohne Vorwissen:** was versteht ein Fremder in 30 Sekunden, was fehlt ihm?

## 8. Was du lieferst — DREI Varianten, gleicher Aufbau

Jede Variante hat **genau diese sieben Felder**, in dieser Reihenfolge. Halte die Wortgrenzen ein.

**a) Name und Idee** (≤ 80 Wörter): Wie heißt der Auftritt, und was ist sein Gedanke in drei Sätzen?
**b) Erste zehn Sekunden** (Text-Wireframe, Block für Block von oben nach unten): Was sieht der Besucher,
in welcher Reihenfolge, mit welcher Aussage? Nenne für jeden Block, was er leisten soll.
**c) Gestaltung** (≤ 120 Wörter + Wertetabelle): Palette mit Hex-Werten und Herkunft (Spielpalette,
Buchpalette oder eigene), Schrift, Bildsprache, Ecken, Abstände, Grundmaß.
**d) Bilder** (Tabelle): Welche Datei aus dem Repo kommt wohin — **mit Pfad**? Welches Bild fehlt und müsste
gemalt werden (als Anforderung: Motiv, Größe, Format, Zielgewicht)?
**e) Was sie über das Spiel sagt** (≤ 80 Wörter): welcher Satz steht oben, welche Ehrlichkeit bleibt sichtbar?
**f) Stärke / Schwäche / Risiko** (je ein Satz).
**g) Aufwand** (≤ 60 Wörter): grob in Stunden, welche Schritte zuerst, was kann entfallen.

**Danach, außerhalb der Varianten:**

**Empfehlung** (≤ 150 Wörter): Welche der drei, warum, und was wäre der erste Schritt morgen früh?
**Eigenstil-Check** (genau fünf Punkte): Woran erkennt ein Besucher Nebelseetal, **ohne den Namen zu lesen**?
Zu jedem Punkt: gibt es das heute schon, und wenn nein, was fehlt dafür konkret?
**Was du nicht geprüft hast**: Liste mit Grund.

## 9. Verbote (hart)

1. Keine fertigen Seiten (kein HTML, kein Markdown-Entwurf als Ganzes). Du beschreibst, du baust nicht.
2. Keine Erfindungen: kein Dateiname, keine Zahl, keine Farbe ohne Beleg.
3. Keine fremden Bilder, keine Bildgenerierung, kein Stock.
4. Chris' Logo wird nicht verändert, zugeschnitten, umgefärbt oder als Vorlage benutzt.
5. Kein Marketing-Sprech, keine Superlative, keine Werbeflosken.
6. Keine Vorschläge, die eine fremde Webfont, ein CDN oder Tracking brauchen.

## 10. Abgabe

Antworte als Text in einem Stück, auf Deutsch, in dieser Reihenfolge: Variante 1 → Variante 2 → Variante 3 →
Empfehlung → Eigenstil-Check → Was du nicht geprüft hast. Kein Vorwort, keine Zusammenfassung am Anfang,
keine Rückfragen am Ende. Wir prüfen deine Angaben nach und entscheiden dann, welches Konzept gebaut wird.
