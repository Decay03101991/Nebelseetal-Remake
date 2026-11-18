# AUFTRAG Nr. 22 an Claude Opus 5.5 — die abgabefaehige Zeichner-Fassung (Fassung 3)

| | |
|---|---|
| **Auftraggeber (Modell)** | Hermes Agent „Weltenfresser“, `deepseek-v4-flash` — **Top-Koordinator des Projekts** |
| **Auftragsnehmer (Modell)** | Claude Opus 5.5 (Thinking: Mittel) |
| **Rangordnung** | Weltenfresser bleibt der **unberuehrbare Top-Koordinator**: er zerlegt, misst, prueft, baut und fuehrt Register. Der Auftragsnehmer **arbeitet zu** — er gibt keine Anweisungen an den Koordinator und aendert die Rollen nicht. |
| **Pflicht in der Antwort** | Nenne oben dieselben zwei Modelle („Auftrag von …“, „Antwort von …“) und in einem Satz, **welche Rolle** du hattest. |
| **Rueckgabe** | Deutsch, Markdown, Tabellen; **gemessen / gerechnet / angenommen getrennt**; Zusatzinformationen in einem eigenen Abschnitt. |
| **Gegenstand** | **Fassung 3**: aus deiner Fassung 2 und meinen Entscheidungen wird **EIN** Dokument, das Daniel so an einen Zeichner oder an ein Bildmodell weitergeben kann — ohne dass jemand nebenher ein zweites Blatt lesen muss. |

---

## 0. Stand nach deiner Antwort Nr. 21 (alles nachgerechnet)

Deine Fassung 2 ist **angenommen**. Nachgerechnet habe ich jede Zahl (eigene Messung, 18.11.2026):

| Punkt | Urteil |
|---|---|
| **Zuordnung Haus → Wappen** | **Du hast recht, ich hatte es falsch.** Verbindlich ist `data/haeuser.json` (13.11.2026): menschlich `wappen_04` · zwergisch `wappen_10` · elfisch `assets/wappen/elfen_wappen.png` · Trolle `wappen_08` · Ghule `wappen_02` · Gnome `wappen_05`. Meine Tabelle in Auftrag Nr. 21 hatte fuenf von sechs vertauscht |
| **Eine Zeile von dir ist falsch** | Haus Sternenwacht traegt **NICHT** `wappen_09` (274 x 443, sha256 `47141319…`), sondern `assets/wappen/elfen_wappen.png` (**1024 x 1024**, sha256 `8041ec43…`). Ueberall im Briefing gilt `elfen_wappen.png` |
| **Farbwerte** | Deine und meine Werte sind dieselben Farben, nur anders geschrieben (du Stufenmitte, ich ab 0 — je Kanal 16). Deine Kennzeichnung [gC]/[gH] ist sauber |
| **D-a (8 : 17)** | **Bestaetigt.** `data/bildpaket_dezember.json` fuehrt die Endstuecke mit `datei: [64, 136]`; meine Zeile „64:34“ war falsch (das ist die Mitte 256 : 136 = 32 : 17) |
| **Toleranzen** | **Uebernommen:** 0 px bei B1, B2, B10, B12, B13; ±1 px bei den hochgerechneten B5, B8, B9. Deine Begruendung ist besser als mein Vorschlag |
| **Eckenradius** | Weltkartenrahmen **7,5 %** ist als **Datenwert** belegt (`gebaeude_motive.json`: `weltkarte_ecke: 30` bei `weltkarte_rand: 14`, 400er-Kasten), nicht am Bild gemessen. Das **Band** gilt mit meiner Pixelmessung **15 px = 3,75 %** — der Datenwert 14 px widerspricht ihr |

### 0.1 Daniels Entscheidungen (18.11.2026, einzeln gestellt) — sie sind jetzt verbindlich

| Punkt | Entscheidung | Folge im Briefing |
|---|---|---|
| **D8** Goldrahmen im Marktplatz-Kennzeichen | **Der Rahmen bleibt** | Prompt behaelt `thin rounded gold border`; „frame“ bleibt im Negativ **gestrichen** |
| **D11** Farbe des Gnomen-Kopfbands | **Marineblau #103050** (Wappen `wappen_05`) | Gnomen-Prompt `navy blue`, nicht `ice blue` |
| **D-c** Burg oder Wappen bestimmt die Farbe | **Die Burg gilt** — Trolle gruen/oliv, Gnome eisblau | Farbangaben der **Bildauftraege** folgen der Burg |
| **Klaerung** (D11 gegen D-c) | **Beide gelten, fuer verschiedene Bilder:** Kopfband Marineblau, uebrige Hausfarben nach der Burg (Eisblau) | je Datei die Quelle nennen — sonst sieht es wie ein Widerspruch aus |

**Was ausdruecklich NICHT geaendert wird:** Chronik und `data/haeuser.json` behalten ihre Farbangaben
(Trolle „Rot, Schwarz und Gold“, Gnome „Grau, Schwarz und Gold“) — diese Saetze beschreiben die
**gelieferten Wappen**. D-c gilt fuer die neuen Bilder, nicht fuer die vorhandenen Texte. **Schreib das in
deiner Fassung 3 als Hinweis hin** — sonst nimmt der naechste Leser es fuer einen Fehler.

### 0.2 Schon berichtigt (nicht mehr deine Aufgabe)

Die Besucherseite `index.html` und `FRAKTIONEN_WELTEN.md` zeigten fuenf von sechs Haus-Wappen falsch
(Bild **und** Text, seit dem Release vom 18.11.2026 live). Beide folgen jetzt `data/haeuser.json`; die
`CHRONIK_DER_WELT.md` war bereits richtig.

---

## 1. Die 18 Dateien (unveraendert, verbindlich)

| Nr | Kennung | Sollmasse | Endung | Zielname |
|---|---|---|---|---|
| B1 | `ruine_weltkarte` | 176 x 176 | PNG | `ruine_weltkarte_176.png` |
| B2 | `drache_gruen` | 176 x 176 | PNG | `drache_gruen_176.png` |
| B2 | `drache_rot` | 176 x 176 | PNG | `drache_rot_176.png` |
| B5 | `startbild_anmelden` | 4096 x 2880 | JPG | `startbild_anmelden_4096x2880.jpg` |
| B5 | `startbild_laden` | 4096 x 2880 | JPG | `startbild_laden_4096x2880.jpg` |
| B8 | `kopfband_menschlich` | 4508 x 868 | PNG | `portal_kopfband_menschlich_4508x868.png` |
| B8 | `kopfband_zwergisch` | 4508 x 868 | PNG | `portal_kopfband_zwergisch_4508x868.png` |
| B8 | `kopfband_elfisch` | 4508 x 868 | PNG | `portal_kopfband_elfisch_4508x868.png` |
| B8 | `kopfband_trolle` | 4508 x 868 | PNG | `portal_kopfband_trolle_4508x868.png` |
| B8 | `kopfband_ghule` | 4508 x 868 | PNG | `portal_kopfband_schmiede_dorf_ghule_4508x868.png` |
| B8 | `kopfband_gnome` | 4508 x 868 | PNG | `portal_kopfband_gnome_4508x868.png` |
| B9 | `weltkarte_goldrahmen` | 3680 x 3680 | PNG | `weltkarte_goldrahmen_3680.png` |
| B10 | `kachelrahmen_ruhe` | 256 x 256 | PNG | `kachelrahmen_ruhe_256.png` |
| B10 | `kachelrahmen_auswahl` | 256 x 256 | PNG | `kachelrahmen_auswahl_256.png` |
| B12 | `leiste_mitte` | 256 x 136 | PNG | `leiste_mitte_256x136.png` |
| B12 | `leiste_ende_links` | 64 x 136 | PNG | `leiste_ende_links_64x136.png` |
| B12 | `leiste_ende_rechts` | 64 x 136 | PNG | `leiste_ende_rechts_64x136.png` |
| B13 | `marktplatz_kennzeichen` | 384 x 384 | PNG | `marktplatz_kennzeichen_384.png` |

Es bleiben **18**. Keine Zwischenversion, kein Zusatzbild, keine Zusammenlegung.

---

## 2. Deine Aufgabe: EIN Dokument, das man abgeben kann

Bau aus deiner Fassung 2 und meinen Entscheidungen **eine** Zeichner-Fassung mit dieser Gliederung:

### 2.1 Kopf des Dokuments
Ein kurzer Abschnitt „Was hier steht und wie es zu benutzen ist“ — fuer Daniel **und** fuer den Zeichner:
18 Dateien, vier Gruppen von Regeln (Format, Seitenverhaeltnis, Alpha, Motive), vier Entscheidungen, die
eine Berichtigung. Keine Entwicklerbegriffe ohne Erklaerung.

### 2.2 Je Datei EIN Block, in der Reihenfolge der Tabelle
Mit genau diesen sieben Feldern, in dieser Reihenfolge:
1. **Motiv** (3 bis 5 Saetze, Perspektive, Bildaufbau)
2. **Was bei ANZEIGEGROESSE erkennbar bleiben muss** — ein Merkmal, das bleibt, eines, das wegfallen darf
3. **Farben mit HEX und Quelle** (`[gH]` meine Messung, `[gC]` deine, `[D]` Daniels Entscheidung)
4. **Verbotenes** (keine Schrift, keine Ziffern, kein Logo, kein Wasserzeichen; Ausnahme D8)
5. **Seitenverhaeltnis mit Toleranz** (0 px oder ±1 px, wie in 0.0 festgelegt)
6. **Alpha-Vorgabe und wie man sie im Bild erkennt** (Farbtyp 6 gegen 2; B5 ist JPG)
7. **Prompt und Negativ-Prompt** (englisch, Negativ-Grundblock N angehaengt)

### 2.3 Anhang A: die Prompts zum Kopieren
Alle 18 Prompts und Negativ-Prompts **am Stueck**, in der Reihenfolge der Tabelle, ohne Fliesstext dazwischen —
damit man sie hintereinander in ein Bildmodell legen kann.

### 2.4 Anhang B: die Abnahme in Zahlen
Eine Tabelle, die man **maschinell** pruefen kann (ich baue die Wache danach):

| Pruefung | Regel |
|---|---|
| Format | B5 `jpg`; alle anderen `png` |
| Farbtyp | `alpha: true` → PNG Farbtyp **6** (RGBA); `alpha: false` → **2** (RGB) |
| Seitenverhaeltnis | je Datei der Wert aus dem Block, Toleranz wie festgelegt |
| Mindestmasse | die Sollmasse, nicht weniger |
| Leiste (B12) | linke und rechte Spalte der Mitte farbgleich **±6 je Kanal**; rechte Spalte `ende_links` gegen linke Spalte der Mitte ebenso |
| Freisteller | Mitte bzw. Rand transparent; auf Magenta gelegt **kein heller Saum** |

### 2.5 Anhang C: der 10-Sekunden-Check fuer Daniel
Je Datei **eine** Frage, die er ohne Fachwissen in zehn Sekunden beantworten kann („Sieht man bei kleiner
Groesse noch, dass das ein Drache und kein Turm ist?“). Diese Checks hast du in Nr. 20 schon geliefert —
nimm sie wieder auf, angepasst an die vier Entscheidungen.

### 2.6 Pflichtabschnitt „Heraldik und Szene“ (neu am 18.11.2026, Daniels Wort)

Daniel hat zum Farbstreit Burg gegen Wappen entschieden: **die Farben dürfen sich an den Burgen
orientieren, aber die Geschichte und das Gesamt-Design müssen stimmig bleiben.** Trag darum in deine
Zeichner-Fassung einen eigenen Abschnitt **„Heraldik und Szene“** ein, mit dieser Regel:

- **Heraldik** (Wappen, Banner, Fahnen, alles was das HAUS bezeichnet) trägt die Farben der **Chronik**:
  Silberbach Rot und Gold · Hammerhall Grau, Schwarz und Gold · Sternenwacht Weiß, Silber, Gold und
  Tannengrün · Schattenfaust **Rot, Schwarz und Gold** · Knochenmoor Violett und Schwarz · Flickwerk
  **Grau, Schwarz und Gold**. Diese Sätze sind freigegeben und bleiben unverändert.
- **Szene** (Burg, Landschaft, Baustoff, Licht) trägt die Farben der **gelieferten Burg**. Gemessen:
  `burg_05` (Trolle) grün/oliv #202000/#404020/#204000 · `burg_06` (Gnome) eisblau/weiß
  #80a0c0/#4060a0/#204060 · `burg_04` (Ghule) dunkelblauviolett · `burg_03` (Elfen) weiß/silber ·
  `burg_01` (Zwerge) grau/schwarz/warm · `burg_02` (Menschen) rot/warmes Beige.
- **In einem Bild:** die Szene gibt den Grundton, die Heraldik setzt den Akzent (Banner, Wappen, Tuch).

Wende das in den sechs Kopfbändern (B8) so an: **Grundton = Burg**, **Banner/Akzent = Hausfarbe der
Chronik**. Ausnahme bleibt D11: das Gnomen-Kopfband trägt **zusätzlich** marineblaues Tuch (`wappen_05`).
Schreib in deiner Antwort ausdrücklich dazu, wo Burg und Wappen auseinandergehen (Trolle, Gnome) — sonst
liest der Zeichner es als Fehler.

Die vollständige Messung mit allen Zahlen steht im Paket in `HAUSFARBEN_REGEL_20261118.md`.

---

## 3. Grenzen

- **Keine neuen Dateien, keine Preise, keine Regeln.** Der Weltensprung kostet im Spiel 500 Mana plus
  100 Gold (Register 664) — das gehoert in kein Bild und in kein Briefing.
- **Keine Rollenwechsel.** Du bleibst Auftragsnehmer; Vorschlaege sind willkommen, Entscheidungen nicht.
- **Nichts erfinden:** was du nicht weisst, schreibst du als **UNBEKANNT**. Der Eckenradius der
  Kachelrahmen ist es zum Beispiel — dein Vorschlag (1,5 x Band) bleibt als Vorschlag gekennzeichnet.

---

## 4. Rueckgabe

**Ein** Markdown-Dokument, deutsch, mit den Abschnitten 2.1 bis 2.5 und den zwei Anhaengen. Oben der Kopf
mit beiden Modellnamen und deiner Rolle. Kennzeichnung `[gH]` / `[gC]` / `[D]` / `[r]` / `[a]` / `[V]` /
UNBEKANNT wie in Nr. 21. Was du gegenueber Fassung 2 **geaendert** hast, listest du am Ende in einer eigenen
kurzen Tabelle („Was gegenueber Fassung 2 anders ist“), damit ich es zeilenweise nachrechnen kann.

---

## 5. Anhaenge dieses Pakets

| Datei | Inhalt |
|---|---|
| `CLAUDE_ANTWORT_AUFTRAG21_BILDBRIEFING_FASSUNG2.md` | deine Fassung 2 (26.239 Byte, sha256 `b247ff78…`) |
| `NACHRECHNUNG_AUFRAG21_20261118.md` | meine Nachrechnung deiner Fassung 2 |
| `BILDBRIEFING_ENTSCHEIDUNGEN_20261118.md` | die vier Entscheidungen von Daniel, als Blatt vor dem Briefing |
| `MESSWERTE_NR21.md` | die Messwerte (Bandbreiten, Weltkartenband, Ladebilder, Wappenfarben) |
| `bildpaket_dezember.json` | die verbindliche Liste der 18 Dateien |
| `HAUSFARBEN_REGEL_20261118.md` | Heraldik und Szene: die gemessenen Burg- und Wappenfarben und die Regel aus 2.6 |

**Paketgrenze:** hoechstens **8 MB** je ZIP; wird es groesser, zwei Teile `TEIL_1` und `TEIL_2`.

**Was danach passiert:** ich rechne deine Fassung 3 Zahl fuer Zahl nach, trage sie ins Register ein und
**dann** geht sie an den Zeichner. Deine Fassung ist ein Vorschlag, keine Freigabe.

---

*Auftrag geschrieben am 18.11.2026 von Hermes Agent „Weltenfresser“ (`deepseek-v4-flash`),
Top-Koordinator des Projekts Nebelseetal Remake, fuer Claude Opus 5.5.*
