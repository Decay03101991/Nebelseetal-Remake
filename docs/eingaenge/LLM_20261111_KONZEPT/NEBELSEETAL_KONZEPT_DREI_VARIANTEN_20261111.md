# Nebelseetal Remake – Präsentations-Konzept in drei Varianten

*Erarbeitet von Opus 5.5 (Thinking: Mittel), 11.11.2026, 18:15–18:50. Geprüft gegen `main` = `7ba015d`
(17:09, Nachfolger von `628f5aa`). Kein Code, keine Seite – nur Beschreibung.*

**Vorab, weil es alle drei Varianten betrifft (gegen den Code geprüft):**

1. **Burg- und Wappenzuordnung widerspricht der Gestaltungsregel.** `data/haeuser.json` bindet die Ghule an
   `burg_05.png` (grüne Baumburg) und die Trolle an `burg_04.png` (violette Burg); `docs/design/DESIGN_LIEFERUNG_CHRIS_20261109.md`
   Z. 145 sagt „Ghule: Burg bleibt **violett**“. Nach Daniels früherer Vorgabe gehören außerdem Eis und
   Schneeflocke zu den Zwergen (Daten: Gnome → `burg_06`), Rot und Löwe zu den Gnomen (Daten: Zwerge →
   `burg_02`), Baum und Blatt zu den Elfen (Daten: Ghule) und die weiß-goldene Burg zu den Trollen (Daten:
   Elfen → `burg_03`). Fünf von sechs Zuordnungen weichen ab. **Jede Variante, die die sechs Burgen
   beschriftet zeigt, wartet auf diese Klärung.**
2. **Nur drei Bilder im Repo stammen nachweislich von Chris:** das Logo, `portal_kopfband_schmiede_dorf_ghule_780x150.png`
   und `marktplatz_kennzeichen_96.png` (`assets/bilder/README.md`). Seine Panoramen liegen nur im Archiv
   (`archiv/design/20261109_chris_bildpaket/`, gitignoriert). Die Panoramen unter `assets/referenzbilder/`
   sind laut ihrer README Daniels „früherer Bildcontent“ – ein Urheber ist dort nicht genannt. Die
   README-Zeile „die gemalten Panoramen … stammen von Chris“ kann ein Besucher auf diese Dateien beziehen.
3. **Chris’ schriftliche Nutzungsbestätigung ist noch offen** (`DESIGN_LIEFERUNG_CHRIS_20261109.md` Z. 38–40).
   Variante 3 hängt daran, die anderen nur am Logo.

---

## Variante 1 – „Das Tor“

**a) Name und Idee**
„Das Tor“: Die Startseite ist die Schwelle, die das Spiel selbst als ersten Bildschirm hat. Sie trägt
dieselben Farben wie das Spielfenster – Rotbraun, Gold, dunkle Leisten –, damit Seite und `.exe` als ein
Ort erkannt werden. Hinter dem Tor stehen die sechs Burgen; davor steht ehrlich, was man bekommt und was
noch fehlt.

**b) Erste zehn Sekunden (360 px, von oben)**

| Block | Inhalt | Leistung |
|---|---|---|
| 1 Kopfleiste | „Nebelseetal“ links, „Pre-Release V_0.0.3“ rechts, goldene Unterkante | sagt in einer Zeile, dass es eine Vorabversion ist |
| 2 Logo | Chris’ Banner auf Rotbraun, darunter die Urheberzeile | Wiedererkennung, Namensnennung |
| 3 Ein Satz | was man tut: Siedlungen, Forschung, Portale, fünf Nachbarn | Inhalt in einem Satz |
| 4 Eckdaten | Windows 11 · offline · kostenlos · rund 102 MB | die Fragen „läuft das bei mir, was kostet es, wie groß?“ |
| 5 Knopf | „Testversion laden“ (Gold, voll) und „Quellcode“ (Rahmen) | Handlung, ohne Scrollen erreichbar |
| 6 Burgenreihe | sechs Burgen nebeneinander, zwei Reihen am Telefon, je ein Hausname | sichtbar: hier gibt es Häuser, keine Icons von der Stange |

Darunter: Screenshot, „Was steckt drin“ (Zahlen), „Was noch fehlt“, Start in fünf Schritten, Fußzeile.

**c) Gestaltung**
Die Spielpalette aus `src/main.py` (Skin `standard`) wird unverändert übernommen, ergänzt um zwei Web-Werte:
ein ruhigerer Fließtext, weil `#FFFF99` in langen Absätzen blendet, und ein aufgehelltes Warnrot, weil das
Spielrot als Schrift zu schwach ist. Überschriften in der Blackletter-Kette nur lokaler Schriften, sonst
Georgia. Ecken 4 px, Grundmaß 8 px, Seitenrand 16 px. Bildsprache: freigestellte Burgen auf ruhigem Grund,
kein Hintergrundbild hinter Text. Der Nebel entsteht aus zwei weichen Farbverläufen, nicht aus einem Bild.

| Wert | Hex | Herkunft | Kontrast (WCAG) |
|---|---|---|---|
| Grund | `#2a0605` | Spiel | – |
| Fläche | `#3e1c1a` | Spiel | – |
| Leisten | `#1a0a09` | Spiel | – |
| Titel, Links, Hauptknopf | `#FFCC33` | Spiel | 12,37 auf Grund · 10,06 auf Fläche · 12,77 auf Leiste |
| Zahlen | `#FFFF99` | Spiel | 14,44 auf Fläche |
| Fließtext | `#F2E3BF` | eigen | 14,66 auf Grund · 11,92 auf Fläche |
| Nebentext | `#C0C0C0` | Spiel (Passworttor) | 10,24 auf Grund |
| Zweitknopf / darüber | `#3e2723` / `#5D4037` | Spiel | Gold darauf 9,17 / 6,18 |
| Hauptknopf-Schrift | `#2a0605` auf `#FFCC33` | Spiel | 12,37 |
| Akzent | `#FF6600` | Spiel | 6,35 auf Grund · **3,17 auf `#5D4037` – dort nicht verwenden** |
| Rot | `#e53935` | Spiel | **4,41 auf Grund – nur Linien und Marker, keine Schrift** |
| Warnschrift | `#ef6b5b` | eigen | 6,15 auf Grund · 5,00 auf Fläche |

**d) Bilder**

| Datei | wohin | Gewicht | Hinweis |
|---|---|---|---|
| `assets/bilder/logo_nebelseetal_klein.webp` (1600 × 754) | Block 2 | 316.542 Byte | unverändert; PNG nur als Ersatz |
| `assets/icons/burgen/burg_01.png` … `burg_06.png` | Block 6 | zusammen 2.363.491 Byte als PNG | als 200-px-WebP geschätzt rund 103 KB zusammen (Probekodierung); **wartet auf Vorab-Punkt 1** |
| `assets/bilder/daniel_portrait_klein.png` | „Wer dahinter steht“ | 194.338 Byte | erst beim Scrollen laden |
| **fehlt:** Screenshot V_0.0.3 | unter Block 6 | Ziel ≤ 250 KB | 1600 × 900, WebP + PNG, ohne Windows-Rahmen, Dorfzentrum mitten im Spiel |
| **später:** `panorama_burgtor_fackeln` (Chris, Archiv) | Hintergrund von Block 2 auf breiten Bildschirmen | Ziel ≤ 200 KB | unverändert, nur auf ≤ 1600 px verkleinert; Freigabe Chris |

**e) Was sie über das Spiel sagt**
Oben steht ein Satz, der beschreibt, was man tut, nicht wie gut es ist. Die Eckdaten nennen Größe und
Plattform, bevor jemand klickt. „Was noch fehlt“ bleibt ein eigener Kasten im ersten Drittel der Seite und
übernimmt die Liste „Bekannte Grenzen“ aus `README.md` (Z. 113–127) wörtlich, ohne eigene Neuformulierung.

**f) Stärke / Schwäche / Risiko**
Stärke: Seite und Spiel sehen gleich aus, und fast alles dafür liegt schon im Repo.
Schwäche: Ohne installierte Buchschrift trägt nur das Logo die Atmosphäre.
Risiko: Stellt das Spiel später auf Chris’ Farben um (F-39), muss das Web nachziehen.

**g) Aufwand**
Etwa 4–6 Stunden. Zuerst Vorab-Punkt 1 klären, dann Palette und Kopfbereich, dann Burgen als WebP,
zuletzt Screenshot einsetzen. Entfallen kann zunächst das Burgtor-Panorama und das Portrait.

---

## Variante 2 – „Die Chronik“

**a) Name und Idee**
„Die Chronik“: Der Auftritt beginnt mit der Welt, nicht mit dem Spiel. Die Seite ist gestaltet wie das
Vorsatzblatt eines Buches – die bestehende Buchpalette bleibt – und führt in drei kurzen Absätzen durch
den Zerfall der Welt. Erst danach kommt das Spiel als „das, was du in dieser Welt tust“.

**b) Erste zehn Sekunden (360 px, von oben)**

| Block | Inhalt | Leistung |
|---|---|---|
| 1 Logo | Chris’ Banner, Urheberzeile | Wiedererkennung |
| 2 Kapitelkopf | „Die Welt ist zersprungen.“ in Gold, darunter zwei Sätze aus der Chronik | Stimmung durch Text |
| 3 Zweiweg | „Die Chronik lesen“ und „Das Spiel laden“ als gleich große Knöpfe | zwei Leser, zwei Wege |
| 4 Kleiner Hinweis | Vorabversion V_0.0.3 · Windows · offline · kostenlos | Ehrlichkeit vor dem Klick |
| 5 Inhaltsverzeichnis | Welt · Häuser · Spiel · Was fehlt · Entstehung | Orientierung wie in einem Buch |

**c) Gestaltung**
Die Palette der heutigen `index.html` bleibt: dunkles Papier, Buchgold, Kupfer als Linie, Stahlblau als
Fläche. Sie passt zur Chronik als Buch und zum PDF. Schrift Georgia/Palatino für alles; die Blackletter-
Kette nur für den Kapitelkopf. Breite Ränder, eine Spalte, Zeilenlänge höchstens etwa 65 Zeichen.
Kupfer erreicht als Schrift nicht 4,5 : 1 und bleibt Linie. Bildsprache: fast keine Bilder; das Logo und ein
Screenshot. Ecken 3 px wie heute, Grundmaß 8 px.

| Wert | Hex | Herkunft | Kontrast (WCAG) |
|---|---|---|---|
| Papier | `#12161c` | Buch (`index.html` Z. 10) | – |
| Papier tief | `#0b0e12` | Buch | – |
| Text | `#ece1cb` | Buch | 14,00 auf Papier · 14,92 auf Papier tief |
| Gold | `#edce87` | Buch | 11,91 auf Papier · 6,61 auf Stahl |
| Kupfer | `#945c2b` | Buch | **3,31 auf Papier – nur Linien** |
| Stahl | `#2a4556` | Buch | Text darauf 7,77 |
| Leise | `#9fb0ba` | Buch | 8,12 auf Papier |
| Fußzeile | `#7b8b95` | Buch (Z. 39) | 5,50 auf Papier tief |
| Knopf-Schrift | `#12161c` auf `#edce87` | Buch | 11,91 |

**d) Bilder**

| Datei | wohin | Gewicht | Hinweis |
|---|---|---|---|
| `assets/bilder/logo_nebelseetal_klein.webp` | Block 1 | 316.542 Byte | unverändert |
| `CHRONIK_DER_WELT.pdf` | Knopf „Chronik lesen“, mit Größenangabe | 9.770.115 Byte | Hauptweg sollte `CHRONIK_DER_WELT.md` sein, PDF als zweiter Link |
| **fehlt:** Screenshot V_0.0.3 | Kapitel „Spiel“ | Ziel ≤ 250 KB | wie Variante 1 |
| **fehlt, Anforderung an Chris:** Kapitelvignette | Block 2 | Ziel ≤ 60 KB | Weltbruchstück über Nebel mit einem Portal, 800 × 300 px, WebP, dunkler Rand für den Papiergrund |

**e) Was sie über das Spiel sagt**
Oben steht ein Satz aus der Welt, nicht über das Programm. Das macht neugierig, sagt aber erst im zweiten
Bildschirm, dass es ein Aufbauspiel ist. Ehrlichkeit bleibt im Hinweis unter den Knöpfen (Vorabversion)
und im eigenen Kapitel „Was fehlt“, das die README-Liste übernimmt.

**f) Stärke / Schwäche / Risiko**
Stärke: Die Chronik mit 72 KB Text ist das ausgearbeitetste Stück des Projekts und bekommt den Platz, den sie verdient.
Schwäche: Die Palette ist nicht die des Spiels; die `.exe` sieht anders aus als die Seite.
Risiko: Wer ein Spiel sucht, liest „Die Welt ist zersprungen“ und weiß nach zehn Sekunden nicht, was er laden soll.

**g) Aufwand**
Etwa 3–4 Stunden, weil Palette und Gerüst bestehen. Zuerst den Kapitelkopf aus der Chronik auswählen
(Daniels Entscheidung), dann Gliederung, dann Screenshot. Die Vignette kann entfallen.

---

## Variante 3 – „Die Bildwelt“

**a) Name und Idee**
„Die Bildwelt“: Chris’ Bilder sind laut Daniels Entscheidung vom 09.11. der Maßstab für alles (F-39). Der
Auftritt nimmt deshalb seine gemessenen Farben und zeigt seine Panoramen groß, als Fenster ins Tal. Das
Spiel wird als Ort gezeigt, die Zahlen und die ehrliche Liste folgen darunter.

**b) Erste zehn Sekunden (360 px, von oben)**

| Block | Inhalt | Leistung |
|---|---|---|
| 1 Panorama | Chris’ `panorama_wegweiser_burg_im_nebel`, volle Breite, Logo darüber | „hier wurde gemalt“ in der ersten Sekunde |
| 2 Urheberzeile | „Logo und Bild: Chris Fred Däubner“ | Namensnennung direkt am Bild |
| 3 Ein Satz + Eckdaten | was man tut; Windows · offline · kostenlos · rund 102 MB | Inhalt und Rahmen |
| 4 Knöpfe | „Testversion laden“, „Quellcode“ | Handlung |
| 5 Bannerreihe | rote Banner mit hellem Symbol (Chris’ Symbolsystem) als Abschnittsmarken: Ähre, Hämmer, Auge, Turm | Wiederkennung über Symbole |

**c) Gestaltung**
Palette aus Chris’ gemessenen Medianen: Rahmengold, Bannerrot, Ghul-Leuchten, auf dem tiefsten Spielbraun.
Rahmengold ist dunkler als Spielgold und reicht für Schrift auf dem Grund, nicht auf Bannerrot. Kästen
bekommen einen abgerundeten Goldrahmen wie Chris’ Kacheln (Ecke 10 px). Abstände 8-px-Raster, Abschnitte
mit Banner statt Linie. Bildsprache nach Chris’ Stilregeln: warmes Licht vorn, kühler Nebel hinten, kaum
Menschen; Panoramen höchstens 1600 px breit.

| Wert | Hex | Herkunft | Kontrast (WCAG) |
|---|---|---|---|
| Grund | `#1a0a09` | Spiel (Leisten) | – |
| Fläche | `#3e1c1a` | Spiel | – |
| Rahmengold | `#C68B42` | Chris, gemessen (`DESIGN_LIEFERUNG_CHRIS` Z. 107) | 6,57 auf Grund · 5,18 auf Fläche · **3,08 auf Bannerrot – dort nicht als Schrift** |
| Bannerrot | `#7E301E` | Chris, gemessen (Z. 108) | Fläche für Banner; **2,13 gegen Grund – braucht Goldrand zur Abgrenzung** |
| Ghul-Leuchten | `#7AAC4D` | Chris, gemessen (Z. 109) | 7,18 auf Grund – nur Ghul-Abschnitt |
| Text | `#F2E3BF` | eigen | 15,13 auf Grund · 11,92 auf Fläche · 7,09 auf Bannerrot |
| Schrift auf Bannern | `#FFCC33` | Spiel | 5,98 auf Bannerrot |
| Knopf | `#1a0a09` auf `#C68B42` | Spiel/Chris | 6,57 |
| Nebentext | `#C0C0C0` | Spiel | 10,58 auf Grund |

**d) Bilder**

| Datei | wohin | Gewicht | Hinweis |
|---|---|---|---|
| `panorama_wegweiser_burg_im_nebel` (Chris, **Archiv, nicht im Repo**) | Block 1 | Ziel ≤ 220 KB | unverändert, nur auf 1600 px Breite verkleinert, WebP; neu nach `assets/bilder/` mit Eintrag in dessen README; Freigabe Chris |
| `assets/bilder/logo_nebelseetal_klein.webp` | über dem Panorama | 316.542 Byte | unverändert, nicht ins Bild gerechnet, eigene Ebene |
| `assets/bilder/portal_kopfband_schmiede_dorf_ghule_780x150.png` (Chris) | Fußband | 254.385 Byte, als WebP rund 44 KB (Probekodierung) | Inhalt unverändert, nur neu kodiert |
| `assets/bilder/marktplatz_kennzeichen_96.png` (Chris) | Marke beim Abschnitt „Handel“ | 21.317 Byte | unverändert |
| **fehlt:** Screenshot V_0.0.3 | unter Block 5 | Ziel ≤ 250 KB | wie Variante 1 |
| **fehlt, Anforderung an Chris:** vier Abschnittsbanner | Block 5 | je ≤ 15 KB | rotes hängendes Banner mit hellem Symbol (Ähre, gekreuzte Hämmer, Auge, Burgturm), 96 × 160 px, WebP mit Transparenz – nach seinem Symbolsystem (Z. 142–145) |

**e) Was sie über das Spiel sagt**
Das Bild sagt „Ort“, der Satz darunter sagt „Aufbauspiel, Einzelspieler, offline“. Damit das Bild nicht
mehr verspricht als die `.exe` zeigt, steht direkt unter dem Panorama: „Bild aus der Gestaltungslieferung;
das Spiel selbst zeigt der Screenshot weiter unten.“ Die Liste „Bekannte Grenzen“ bleibt als eigener Kasten.

**f) Stärke / Schwäche / Risiko**
Stärke: Den stärksten Eigenstil zeigt diese Variante, weil sie mit gemalten Bildern statt mit Text beginnt.
Schwäche: Sie braucht Bilder, die noch nicht im Repo liegen, und vier neue Banner.
Risiko: Das Panorama zeigt mehr Malerei, als das heutige Spielfenster zeigt – ein Besucher kann sich getäuscht fühlen.

**g) Aufwand**
Etwa 8–12 Stunden plus Wartezeit auf Chris. Zuerst schriftliche Freigabe von Chris, dann Panorama
verkleinern und einbinden, dann Palette, zuletzt Banner. Entfallen können die vier Banner (dann Goldlinien).

---

## Empfehlung

**Variante 1, „Das Tor“** – mit Variante 3 als Ziel, sobald Chris’ Freigabe da ist.

Warum: Ein Besucher, der die Seite verlässt und die `.exe` startet, sieht heute Rotbraun und `#FFCC33`.
Nur Variante 1 hält dieses Versprechen ohne Bruch. Sie braucht bis auf den Screenshot nur Bilder, die im Repo
liegen, und nimmt nichts von Chris, wofür seine Bestätigung noch fehlt. Variante 2 ist schön, aber sie
stellt die Welt vor das Spiel; das verschiebt die wichtigste Frage „was lade ich?“ in den zweiten Bildschirm.
Variante 3 hat den stärksten Eigenstil, hängt aber an drei offenen Punkten (Freigabe, Archivbilder,
Farbumstellung des Spiels nach F-39). Wenn das Spiel auf Chris’ Farben umgestellt ist, tauscht Variante 1
drei Farbwerte und bekommt das Panorama – der Aufbau bleibt.

Erster Schritt morgen früh: die Burg-Zuordnung in `data/haeuser.json` gegen die Gestaltungsregel prüfen
lassen (Vorab-Punkt 1) – sie entscheidet, ob Block 6 gebaut werden kann.

## Eigenstil-Check – woran man Nebelseetal ohne den Namen erkennt

1. **Gold auf Rotbraun.** Heute: im Spiel ja (`#FFCC33` auf `#2a0605`), im Web nein (Gold `#edce87` auf Blaugrau). Fehlt: Palettentausch der Startseite.
2. **Das Nebelbanner von Chris.** Heute: ja, auf README und Startseite. Fehlt: im README die WebP statt der 1,32-MB-PNG (`README.md` Z. 3).
3. **Sechs Burgen mit eigenen Wappen.** Heute: im Spiel ja, im Web nein. Fehlt: die Klärung der Zuordnung (Vorab-Punkt 1) und 200-px-WebP-Fassungen.
4. **Buchschrift in den Überschriften.** Heute: im Spiel nur, wenn „Blackletter“ installiert ist (keine Schriftdatei im Repo); im Web nein. Fehlt: eine Entscheidung, ob eine frei lizenzierte Buchschrift als Datei ins Repo kommt – sie würde lokal mitgeliefert, nicht von fremden Servern geladen.
5. **Rote Banner mit hellem Symbol.** Heute: nur in Chris’ Archivbildern und im Marktplatz-Kennzeichen. Fehlt: Banner als eigene kleine Bilder (Anforderung in Variante 3, d).

## Was ich nicht geprüft habe

| Punkt (Auftrag Abschnitt 7) | Stand | Grund |
|---|---|---|
| 1 Startseite live | **UNBEKANNT** | Pages, github.com und die API sind aus dieser Sitzung nicht erreichbar (Freigabe verweigert); Chrome war nicht verbunden (Liste der Browser leer). Die Repo-Fassung `index.html` (9.972 Byte LF) ist unverändert; mein Rendering bei 360 px von 14:20 gilt weiter: Download-Knopf erst unter dem ersten Bildschirm. |
| 2 README auf GitHub | **teilweise** | Gerendert nicht gesehen. Im Text: Sprungziele `#bekannte-grenzen` (Überschrift Z. 113) und `#rechte` (Z. 129) existieren. |
| 3 Dateibaum | **geprüft** | 1.273 Dateien, `assets/` 370 (bilder 13, icons 194, karten 127, referenzbilder 17, quellbilder 10, original 8, loadingpage 1). Verschwunden: `assets/karten/original/` und 424 Dateien unter `docs/original/`. |
| 4 Release-Seite | **UNBEKANNT** | nicht erreichbar; Tags lokal vorhanden (`v_0.0.3` u. a.). |
| 5 Kontraste | **gerechnet** | für alle drei Paletten, Paare unter 4,5 : 1 in den Tabellen fett. |
| 6 Erster Eindruck | **am README geprüft** | Ein Fremder versteht in 30 Sekunden: Remake, Windows, offline, Vorabversion. Es fehlen: wie es aussieht (kein Bild aus dem Spiel), wie lange eine Partie dauert, und der Download-Schritt steht erst ab Z. 33. |

**Nebenbefunde beim Prüfen, nicht Teil der Konzepte:**

- `docs/original/` enthält am Stand `7ba015d` noch 75 Dateien, darunter `Spielanleitung_2005/` (30 Dateien),
  `Spielanleitung_2009_Textfassung.txt` (46.432 Byte), `website/` (13) und zwei Rangliste-Bilder vom
  31.08.2011. Das README sagt in Z. 134–137, Handbuch und Website-Grafiken seien aus dem öffentlichen Stand
  genommen. Die Tags (z. B. `v_0.0.3`) zeigen außerdem weiter auf Stände mit allen 424 Dateien – ein
  Geschichts-Schnitt nur auf `main` reicht dafür nicht.
- `VORSCHAU.md`: 12 von 12 Bildern weiterhin kaputt, aber in README Z. 31 und Z. 62 verlinkt.
- `release_vorlage/START_HIER.txt` nennt weiter V_0.0.1; der Workflow sucht weiter
  `Nebelseetal_Remake_Testversion.exe` (Z. 28).
- `assets/original/` (8 Dateien) sind weiter gespeicherte 404-Seiten, keine Bilder.
