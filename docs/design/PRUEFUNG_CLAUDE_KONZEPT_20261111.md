# Prüfung von Claudes Konzept-Antwort (11.11.2026)

**Was geprüft wird:** Claudes Antwort auf `AUFTRAG_CLAUDE_KONZEPT.txt` (Register 413) — drei
Präsentations-Konzepte zur Wahl, ohne Code und ohne Seite.
**Ablage:** `docs/eingaenge/LLM_20261111_KONZEPT/` — hashgleich vom Desktop übernommen; zweite,
hashgleiche Fassung unter `D:\Arbeiten\Hermes\Desktop_Ablage\20261111_Claude_Konzept\`.

| Datei | Byte | SHA256 |
|---|---:|---|
| `AUFTRAG_CLAUDE_KONZEPT.txt` | 11.932 | `af8069ab1d6fbf33…` |
| `NEBELSEETAL_KONZEPT_DREI_VARIANTEN_20261111.md` | 18.340 | `4f7de45d5bcb0134…` |

**Verfahren:** Die Konzepte vollständig gelesen; **jede Behauptung, die eine Datei, eine Zahl, eine
Farbe oder einen Bildinhalt im Projekt nennt, selbst nachgemessen.** Kontraste mit eigener
WCAG-Rechnung, Paletten gegen die Quelldateien, Bildgewichte mit `ls -l`, Bildinhalte mit eigener
Sichtprüfung (`vision_analyze` auf zwei Montagen), Register- und Git-Stände mit `git ls-tree`.
Nichts aus der Lieferung wurde übernommen.

---

## 0. Kurzurteil

Das ist die beste Lieferung, die bisher aus dieser Projektlinie kam, was **Zahlen** angeht: alle
**35** Kontrastwerte stimmen auf zwei Nachkommastellen, alle **sechs** Bildgewichte und alle
**sieben** Dateizahlen in `assets/` stimmen auf das Byte. Die drei Paletten sind quellentreu
zugeordnet (Spiel, Buch, Chris).

**Zwei von drei Punkten seines Vorab-Kapitels halten im Kern und sind falsch belegt.** Der
Burg-Widerspruch ist **real und messbar** (5 von 6 Zuordnungen passen nicht), aber er stammt **nicht
aus einer Vorgabe von Daniel**, sondern aus einem archivierten Gestaltungsentwurf; das Protokoll
sagt an der entscheidenden Stelle das Gegenteil. Und die Fundstelle für die drei Chris-Bilder ist
falsch — die genannte README dokumentiert zwei und verweist für das Logo auf ein Inventar, das Chris
gar nicht nennt.

**Folge:** Die Konzepte sind als Grundlage brauchbar. **Gebaut wird nichts** — weder die Seite noch
Block 6 der Burgenreihe — bis Daniel die Variante und die Burg-Zuordnung entschieden hat.

---

## 1. Was hält (selbst gemessen)

### 1.1 Kontraste — 35 von 35

| Variante | geprüfte Paare | Abweichung zur Behauptung |
|---|---:|---|
| 1 „Das Tor“ | 15 | keine (größte Abweichung 0,00) |
| 2 „Die Chronik“ | 9 | keine |
| 3 „Die Bildwelt“ | 11 | keine |

Auch die **Warnhinweise** stimmen: `#FF6600` auf `#5D4037` = **3,17** (unter 4,5 : 1), `#e53935`
auf `#2a0605` = **4,41** (unter 4,5 : 1), Kupfer `#945c2b` auf Papier = **3,31**, Rahmengold auf
Bannerrot = **3,08**, Bannerrot gegen Grund = **2,13**. Wer diese Werte als Schrift einsetzt, liest
schlecht — die Tabelle sagt das selbst.

### 1.2 Paletten — alle drei quellentreu

| Variante | behauptete Herkunft | meine Messung |
|---|---|---|
| 1 | Spiel, Skin `standard`, `src/main.py` | `SKINS["standard"]` (Z. 3786–3801) führt `bg #2a0605`, `panel #3e1c1a`, `gold #FFCC33`, `text #FFFF99`, `topbar`/`sidebar #1a0a09`, `button #3e2723`, `button_active #5D4037`, `red #e53935`, `subhead #FF6600` — **alle zehn deckungsgleich**, `#C0C0C0` steht als Passworttor-Nebentext in `main.py:8409` |
| 2 | Buch, `index.html` Z. 10 | `--papier #12161c`, `--papier2 #0b0e12`, `--gold #edce87`, `--kupfer #945c2b`, `--stahl #2a4556`, `--text #ece1cb`, `--leise #9fb0ba` — **alle sieben deckungsgleich**; `#7b8b95` steht in Z. 39 (Fußzeile) |
| 3 | Chris, gemessene Mediane | `DESIGN_LIEFERUNG_CHRIS_20261109.md` Z. 106–108: Rahmengold `#C68B42` (Median aus 499.692 Randpixeln), Bannerrot `#7E301E` (127.204), Ghule-Leuchten `#7AAC4D` (21.773) — **alle drei deckungsgleich** |

Die **Varianten 1 und 3 teilen sich Grund und Fläche** (`#2a0605`/`#1a0a09`, `#3e1c1a`) — das ist
kein Fehler, sondern genau der Punkt, an dem Variante 3 über Variante 1 hinauswächst.

### 1.3 Bildgewichte und Dateizahlen — auf das Byte

| Behauptung | meine Messung |
|---|---|
| `logo_nebelseetal_klein.webp` 316.542 Byte | 316.542 |
| `burg_01`…`burg_06` zusammen 2.363.491 Byte | 2.363.491 (344.565 + 344.968 + 389.369 + 364.757 + 513.942 + 405.890) |
| `daniel_portrait_klein.png` 194.338 Byte | 194.338 |
| `portal_kopfband_…_780x150.png` 254.385 Byte | 254.385 |
| `marktplatz_kennzeichen_96.png` 21.317 Byte | 21.317 |
| `CHRONIK_DER_WELT.pdf` 9.770.115 Byte | 9.770.115 |
| Chronik-Text „72 KB“ | `CHRONIK_DER_WELT.md` 72.781 Byte |
| `assets/` 370 Dateien, bilder 13, icons 194, karten 127, referenzbilder 17, quellbilder 10, original 8, loadingpage 1 | **exakt diese acht Zahlen** |
| Repo 1.273 Dateien | 1.273 bei `7ba015d` (seinem Prüfstand) — **am Kopf `3d14ef8` sind es 1.284** |

### 1.4 README-Zeilen, Wortlaut und Nebenbefunde

| Behauptung | meine Messung |
|---|---|
| Liste „Bekannte Grenzen“ in `README.md` Z. 113–127 | Kapitel in Z. 113, Liste Z. 115–127 — **stimmt** |
| Sprungziel `#rechte` in Z. 129 | `## Rechte` steht in Z. 129 — **stimmt** |
| README Z. 134–137 sagt, die Originalquellen seien draußen | Wortlaut dort: Handbuch, Handbuchbilder, Website-Grafiken, Zeitschriftenmaterial — **stimmt** |
| README Z. 3 lädt die 1,32-MB-PNG statt der WebP | Z. 3 ist das `<img>` auf `logo_nebelseetal_klein.png`, die Datei hat **1.324.807 Byte** — **stimmt** |
| README Z. 62 verlinkt `VORSCHAU.md` | **stimmt** (Tabellenzeile) |
| `VORSCHAU.md`: 12 von 12 Bildern kaputt | 12 Verweise, alle auf `assets/hintergrund_content_20261104/…`, **Verzeichnis existiert nicht** — **stimmt** |
| `docs/original/` hat am Stand `7ba015d` noch 75 Dateien | **75, auch am Kopf `3d14ef8`**; darunter `Spielanleitung_2005/` (30), `website/` (13), `Spielanleitung_2009_Textfassung.txt` (Git-Blob 46.432 Byte), zwei Rangliste-PNG vom 31.08.2011, zwei ODT |
| Tags zeigen weiter auf Stände mit allen 424 Dateien | `v_0.0.1`, `v_0.0.2`, `v_0.0.3` zeigen je auf Commits mit **424** Dateien in `docs/original` — **stimmt** |
| `assets/original/` sind 8 gespeicherte 404-Seiten | 8 × 236 Byte, Inhalt `<!DOCTYPE HTML … <title>404 Not Found</title>` — **stimmt** |
| `release_vorlage/START_HIER.txt` nennt V_0.0.1 | Z. 1: `OEFFENTLICHE WINDOWS-TESTVERSION V_0.0.1` — **stimmt** |
| Der Workflow sucht `Nebelseetal_Remake_Testversion.exe` (Z. 28) | `.github/workflows/*.yml` Z. 28 — **stimmt** |
| Keine Schriftdatei im Repo | `git ls-files` findet keine `.ttf/.otf/.woff/.woff2/.eot`; `index.html` setzt nur Georgia/Palatino — **stimmt** |
| Eigenstil 1: im Web kein Gold auf Rotbraun | Die **live** ausgelieferte Seite enthält `#12161c` und `#edce87`, aber **kein** `#2a0605` und **kein** `#FFCC33` — **stimmt** |

---

## 2. Was nicht hält

### 2.1 Vorab-Punkt 1: der Widerspruch ist real — die Herkunft ist falsch

Claude schreibt: „Nach Daniels früherer Vorgabe gehören außerdem Eis und Schneeflocke zu den Zwergen,
Rot und Löwe zu den Gnomen, Baum und Blatt zu den Elfen und die weiß-goldene Burg zu den Trollen.“

**Diese Vorgabe gibt es in keiner Datei des Projekts.** Die Zuordnung, die er meint, steht in
`archiv/design/20261109_designvorschlag_01/entpackt/Nebelseetal_Designvorschlagspaket_Hermes/Designvorschlagspaket.md`
§ 3.1 — einem **Entwurfspaket im Archiv**, dessen eigene Einleitung die Heimatwelten als „Vorschlag“
führt und die Farbwerte als „Startwerte … aus den Originalbildern nachmessen“ bezeichnet.

Was **belegt** ist, sagt etwas anderes:

| Beleg | Wortlaut |
|---|---|
| `docs/archiv/ENTWICKLUNGSPROTOKOLL_VOR_VERDICHTUNG_20261104.md` Z. 303 (Register 187, 04.11.2026, 16:26) | Daniels Anweisung betraf **nur die Wappen**: „zwergisches Wappen zu den Trollen, Trollwappen zu den Menschen, Menschenwappen zu den Ghulen, Ghulwappen zu den Zwergen“. Und ausdrücklich: „Die **Burgen** blieben, weil dazu keine Anweisung vorliegt und Raten verboten ist“ |
| `data/bot_wappen.json`, Feld `aenderung_2026_11_04` | derselbe Satz als Datenkommentar: „Die BURGEN blieben bei ihrer Fraktion; eine Anweisung fuer die Burgen gibt es nicht.“ |
| `data/bot_wappen.json`, Feld `warum_diese_zuordnung` | „die Wappen sind also nicht mehr deckungsgleich mit den Burgen. Wer eines von beiden anders will, aendert hier den Dateinamen“ |
| `FRAKTIONEN_WELTEN.md` Z. 114–115 | „Die Zuordnung von Wappen und Burgen zu den Häusern ist eine Setzung dieses Projekts — das Originalspiel nannte keine Wappen.“ |

**Was daran trotzdem stimmt und wichtig ist:** Die Wappen sind seit dem Ringtausch vom 04.11. die
Kennung eines Hauses, und die **Hausfarben folgen den Wappen** (so steht es in `data/haeuser.json`,
Feld `ehrliche_grenze`, Frage 6 / Register 213). Verglichen damit stehen **5 von 6 Burgen am falschen
Haus** — das ist mein eigenes Ergebnis, unabhängig von Claudes Begründung (Abschnitt 3).

### 2.2 Vorab-Punkt 2: die Fundstelle ist falsch, und der Verweis läuft ins Leere

Claude schreibt, die drei Chris-Bilder stünden „(`assets/bilder/README.md`)“. Gemessen:

- `assets/bilder/README.md` führt **zwei** Zeilen mit Chris als Urheber: `portal_kopfband_…` und
  `marktplatz_kennzeichen_96.png`.
- Für das Logo sagt dieselbe README ausdrücklich, es werde **nicht** nachgetragen: „ihre Herkunft und
  Verwendung stehen in `docs/BILDINVENTAR.md`“.
- `docs/BILDINVENTAR.md` (Stand 28.10.2026, also **vor** dem Logo vom 06.11.) nennt Chris mit **keinem
  Wort** (`grep -i chris`: null Treffer) und führt keine Burgen und keine Wappen.

**Neuer Befund (nicht von Claude):** dieser Verweis ist seit dem 06.11. **tot**. Die Herkunft des
Logos steht tatsächlich in `README.md` Z. 5 und 143 sowie in `assets/referenzbilder/README.md` — nur
nicht dort, wohin die Asset-README zeigt. Das ist eine Zeile Arbeit und gehört in den nächsten
Dokumentlauf.

Der **Kern** seiner Aussage hält: im Repo liegen genau **drei** Bildmotive von Chris (Logo — dazu
`assets/referenzbilder/Logo_Nebelseetal_20261106.png` als Original und zwei Web-Fassungen —,
Portal-Kopfband, Marktplatz-Kennzeichen); seine Panoramen liegen nur im gitignorierten
`archiv/design/20261109_chris_bildpaket/` (`git check-ignore` bestätigt).

### 2.3 Kleinere Ungenauigkeiten

| Behauptung | gemessen | Wirkung |
|---|---|---|
| Farbwerte in `DESIGN_LIEFERUNG_CHRIS` „Z. 107/108/109“ | **Z. 106/107/108** | keine, die Werte stimmen |
| „Ghule: Burg bleibt violett“ in Z. 145 | **Z. 146** | keine |
| „Tags lokal vorhanden (`v_0.0.3` u. a.)“ | lokal sind **3** Tags vorhanden (`v_0.0.1`, `v0.5.0-pre.1`, `vor-nullzustand-20261105`); `v_0.0.2` und `v_0.0.3` stehen **nur auf dem Remote** (`git ls-remote --tags`) | keine für den Befund — die 424 Dateien sind über beide erreichbar |
| „Download-Schritt erst ab Z. 33“ | Kapitel `## Diese Version herunterladen` in Z. 33, der erste Schritt in **Z. 35** | keine |
| Repo „1.273 Dateien“ | 1.273 bei `7ba015d`; am Kopf **1.284** | keine — sein Prüfstand war ein anderer |

---

## 3. Die Burg-Frage selbst nachgemessen

Claude hat die Motive richtig benannt. Ich habe sie nicht übernommen, sondern die sechs Burgen und die
sechs zugeordneten Wappen selbst angesehen (zwei Montagen, `vision_analyze`, 11.11.2026).

| Haus (Daten) | Burg laut `data/haeuser.json` | Motiv der Burg (gesehen) | Wappen des Hauses | Motiv des Wappens (gesehen) | Hausfarben laut Daten | Burg passt zu den Farben? |
|---|---|---|---|---|---|---|
| menschlich | `burg_01` | blaue Banner, **goldene Lilie**, grauer Stein | `wappen_04` | **Krone** mit Lilie, rot/gold | Weinrot und Gold | **nein** (blau) |
| zwergisch | `burg_02` | weiße Burg, **rote Dächer**, goldener **Löwe** | `wappen_05` | **Steinturm** mit Zinnen, blau/grau | Nachtblau, Grau und Gold | **nein** (rot) |
| elfisch | `burg_03` | **weiß-goldene** Zitadelle, Stern, Engelsfiguren | `wappen_03` | **Hirschkopf**, grün/gold | Dunkelgrün und Gold | **nein** (weiß) |
| Trolle | `burg_04` | **violette** Festung, Dreizack, Nacht | `wappen_02` | **Rabe** vor Mond, violett/schwarz | Violett, Schwarz und Gold | **ja** |
| Ghule | `burg_05` | **grüne Baumfestung**, goldenes Blatt | `wappen_01` | **Wolf** vor Schneebergen, blau/silber | Blau, Silber und Gold | **nein** (grün) |
| Gnome | `burg_06` | **eisblaue** Kristallburg, Schneeflocke | `wappen_06` | **gekreuzte Schwerter**, rot/silber | Karminrot, Silber und Gold | **nein** (eisblau) |

**Ergebnis:** 5 von 6 Burgen passen weder zur Tinktur ihres Hauses noch zum Motiv seines Wappens.
Claudes Zahl ist damit **bestätigt** — nur sein Weg dorthin („Daniels Vorgabe“) nicht.

**Die Zuordnung, die er vorschlägt, ist selbst nur eine Setzung** und löst den Widerspruch nicht
sauber: Er will die weiß-goldene Burg `burg_03` den **Trollen** geben, deren Farbe Violett ist — dann
passt die Burg zwar zum Entwurfspaket, aber nicht mehr zu den Hausfarben, die seit Register 213 an
den Wappen hängen. **Es gibt drei Wege, und alle drei sind Daniels Entscheidung:**

1. **Burgen an die Wappen anpassen** (5 Dateinamen in `data/haeuser.json` und `data/bot_wappen.json`
   ändern, kein Code) — dann stimmen Burg, Wappen und Farbe je Haus überein.
2. **Burgen lassen, Wappen zurücktauschen** — dann steht die Weltkarte wieder wie vor dem 04.11.
3. **Burgen und Wappen bleiben, die Hausfarben folgen den Burgen** — dann müssen sechs Wappen-Sätze
   der Chronik neu geschrieben werden, weil sie aus den Bildern gelesen sind (W-15).

Was **nicht** geht: eine Beschriftung der sechs Burgen mit Hausnamen bauen (Block 6 in Variante 1),
solange das offen ist. Dann steht neben dem Wappen des Wolfes eine Baumfestung.

---

## 4. Was ich zusätzlich gemessen habe

| Punkt | Claudes Stand | meine Messung (11.11.2026, 18:4x) |
|---|---|---|
| Startseite live | **UNBEKANNT** (Pages aus seiner Sitzung nicht erreichbar) | `https://decay03101991.github.io/Nebelseetal-Remake/` → **HTTP 200, 9.972 Byte**, Titel `Nebelseetal Remake — Pre-Release V_0.0.3`, Logo lädt, zwei Links auf `releases/tag/v_0.0.3` und `releases` |
| Release-Seite | **UNBEKANNT** | API: `v_0.0.3` vorhanden mit `Nebelseetal_Pre_Release_V_0.0.3.exe` **und** `.zip`; daneben `v_0.0.2`, `v_0.0.1` |
| Repo-Beschreibung | nicht geprüft | „… Vorabversion V_0.0.3 fuer Windows, offline und kostenlos“, Homepage = Pages-URL |
| Repo-Dateizahl | 1.273 | **1.284** am Kopf `3d14ef8` (1.273 bei `7ba015d`) |

**Nebenbefund zur eigenen Übergabe (Sitzung 34):** dort steht in der Belegtabelle „Repo-Dateien
**1.272**“. Gemessen sind es am Kopf `3d14ef8` **1.284** und bei `7ba015d` 1.273. Die Zahl 1.272 ist
falsch; richtig ist 1.284 (Versionen: 1.741 vor der Entfernung der Originalquellen).

---

## 5. Was jetzt entschieden werden muss

| Nr | Frage | Warum sie blockiert |
|---|---|---|
| A | **Welche Variante wird gebaut** — 1 „Das Tor“, 2 „Die Chronik“, 3 „Die Bildwelt“? | ohne sie kein Anfang; Empfehlung des Verfassers: 1 mit 3 als Ziel |
| B | **Burg-Zuordnung** (Abschnitt 3, Wege 1–3) | ohne sie entfällt Block 6 in Variante 1; betrifft außerdem Weltkarte, Chronik-Sätze und den Test `test_haeuser_wappen` |
| C | **Darf der Bau der Spiel-Oberfläche jetzt beginnen** (T1–T7, G8, G9, Wall-Punkte, Stufe-1-Fehler)? | Daniel sagte „Sag go, dann fange ich mit den Hintergründen an“ — ein Go kam nicht mehr |

**Nicht zu entscheiden, weil noch nicht entscheidbar:** Chris’ schriftliche Nutzungsbestätigung
(`DESIGN_LIEFERUNG_CHRIS` Z. 38–40) und der Screenshot der V_0.0.3 (Register 409, Daniel nimmt ihn
selbst auf).

---

## 6. Belege

| Messung | Befehl / Quelle |
|---|---|
| Kontraste | eigene WCAG-Rechnung (Relative Luminanz, 0,03928-Schwelle), 35 Paare, Abweichung 0,00 |
| Palette Spiel | `src/main.py` Z. 3786–3801 (`SKINS["standard"]`) |
| Palette Buch | `index.html` Z. 10, 11, 39 |
| Palette Chris | `docs/design/DESIGN_LIEFERUNG_CHRIS_20261109.md` Z. 106–108 |
| Bildgewichte | `ls -l` auf die genannten Dateien, 11.11.2026 |
| Dateizahlen | `find assets -type f`, je Unterordner |
| Burg- und Wappenmotive | zwei Montagen (`burgen_montage.png`, `wappen_montage.png`) aus den Originaldateien, gesichtet mit `vision_analyze` |
| Burg-Bindung | `data/haeuser.json` (`je_haus`), `data/bot_wappen.json` (`je_fraktion`, `warum_diese_zuordnung`, `aenderung_2026_11_04`) |
| Herkunft der vorgeschlagenen Zuordnung | `archiv/design/20261109_designvorschlag_01/entpackt/…/Designvorschlagspaket.md` § 3.1 |
| Register 187 | `docs/archiv/ENTWICKLUNGSPROTOKOLL_VOR_VERDICHTUNG_20261104.md` Z. 303 |
| Tags | `git ls-remote --tags origin`, `git ls-tree -r <commit> docs/original \| wc -l` |
| Startseite live | `curl` auf die Pages-URL (9.972 Byte), Titel und Farbwerte im HTML geprüft |
| Release | GitHub-API `/releases` (öffentlich, ohne Anmeldung) |
