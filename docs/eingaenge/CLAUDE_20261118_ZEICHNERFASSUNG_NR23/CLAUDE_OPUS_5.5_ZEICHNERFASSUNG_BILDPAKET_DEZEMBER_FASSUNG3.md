# Bildpaket Dezember 2026 – Zeichner-Fassung (Fassung 3)

| | |
|---|---|
| **Auftrag von** | Hermes Agent „Weltenfresser“, `deepseek-v4-flash`, Top-Koordinator des Projekts |
| **Antwort von** | Claude Opus 5.5 (Thinking: Mittel) |
| **Meine Rolle** | Ich arbeite zu: Ich habe aus meiner Fassung 2 und Daniels Entscheidungen vom 18.11.2026 dieses eine Dokument gebaut. Weltenfresser rechnet es nach und gibt es frei; erst dann geht es an den Zeichner. |
| **Antwort auf** | `AUFTRAG_CLAUDE_ZEICHNERFASSUNG_NR22_20261118` mit Paket. Gelesen: Auftrag, `HAUSFARBEN_REGEL_20261118.md`, `BILDBRIEFING_ENTSCHEIDUNGEN_20261118.md`, `NACHRECHNUNG_AUFRAG21_20261118.md`, `MESSWERTE_NR21.md`; `bildpaket_dezember.json` ist inhaltsgleich mit Nr. 21. |

---

## 1. Was hier steht und wie es zu benutzen ist

**Für Daniel und für den Zeichner (oder das Bildmodell):**

- **18 Bilddateien** für das Spiel. Jede hat unten **einen Block** mit sieben Feldern: Motiv · was in Spielgröße erkennbar bleiben muss · Farben · Verbotenes · Seitenverhältnis · Transparenz · Prompt.
- **Vier Regelgruppen:**
  1. **Format:** Die beiden Startbilder (B5) sind JPG, alle anderen 16 sind PNG.
  2. **Seitenverhältnis:** Jede Datei hat ein festes Verhältnis. Kleine Dateien müssen das Maß **genau** treffen; die drei großen, hochgerechneten Gruppen (B5, B8, B9) dürfen **1 Pixel** abweichen.
  3. **Transparenz:** „Freisteller“ (Motiv auf durchsichtigem Grund) werden als PNG **mit** Alphakanal gespeichert. „Deckend“ heißt PNG **ohne** Alphakanal, also RGB, nicht RGBA mit lauter undurchsichtigen Pixeln.
  4. **Motive:** Kein Bild enthält Schrift, Ziffern, Logo oder Wasserzeichen. Die Hausfarben folgen der Regel in Abschnitt 2.
- **Größen:** Jede Datei ist **4-mal so groß wie im Spiel** (Daniel, F-101). Wer kleiner erzeugt, rechnet hoch und notiert Ausgangsgröße, Verfahren und Datum (F-106).
- **Vier Entscheidungen von Daniel (18.11.2026):**
  - **D8:** Das Marktplatz-Kennzeichen behält seinen Goldrahmen.
  - **D11:** Das Gnomen-Kopfband trägt zusätzlich marineblaues Tuch (#103050).
  - **D-c:** Für die neuen Bilder bestimmt die **Burg** die Grundfarbe.
  - **Klärung:** Heraldik und Szene sind zwei Ebenen (Abschnitt 2).
- **Eine Berichtigung:** Das Wappen von Haus Sternenwacht ist `assets/wappen/elfen_wappen.png`, nicht `wappen_09`.
- **Hinweis zu Chronik und `data/haeuser.json`:** Ihre Farbsätze (zum Beispiel „Trolle: Rot, Schwarz und Gold“, „Gnome: Grau, Schwarz und Gold“) **bleiben unverändert und sind kein Fehler**. Sie beschreiben die gelieferten **Wappen**. Die Burgfarben gelten nur für die **Szene** der neuen Bilder.

**Kennzeichnung der Zahlen:**
- **[gH]** von Weltenfresser gemessen (32er-Stufen ab 0, zum Beispiel #200000)
- **[gC]** von Claude gemessen (Stufenmitte, zum Beispiel #301010; je Kanal 16 höher als [gH] und dieselbe Farbe)
- **[D]** Daniels Entscheidung · **[r]** gerechnet · **[a]** angenommen · **[V]** Vorschlag · **UNBEKANNT**

**Was nicht an den Zeichner geht:** Abschnitt 8 („Für Weltenfresser“) und die Änderungstabelle (Abschnitt 7).

---

## 2. Heraldik und Szene (Pflichtabschnitt, Daniel 18.11.2026)

> „ja die farben dürfen sich an den burgen orientieren aber achte darauf das es mit der geschichte stimmig ist und unser gesamt designkonzept stimmig ist“ (Daniel)

| Ebene | Was dazu gehört | Woher die Farbe kommt |
|---|---|---|
| **Heraldik** | Wappen, Banner, Fahnen, Wappenrock, alles, was das **Haus** bezeichnet | **Chronik** (freigegeben, unverändert) |
| **Szene** | Burg, Landschaft, Baustoff, Licht | **gelieferte Burg** |
| **In einem Bild** | Die Szene gibt den **Grundton**, die Heraldik setzt den **Akzent** (Banner, Tuch). | – |

| Haus | Volk | **Heraldik (Chronik)** + Wappenfarben [gH] | **Szene (Burg)** [gH] | Gehen Burg und Wappen auseinander? |
|---|---|---|---|---|
| Silberbach | Menschen | Rot, Gold · `wappen_04` #200000, #600000, Gold #a06020 | `burg_02` Beige #e0c0a0, #c0a080, Rot #600000, #404020 | nein |
| Hammerhall | Zwerge | Grau, Schwarz, Gold · `wappen_10` #202020, #000000, #604020 | `burg_01` #404040, #202020, warm #c0a0a0, #c0a080 | nein |
| Sternenwacht | Elfen | Weiß, Silber, Gold, Tannengrün · `elfen_wappen.png` #002020, #004040, Silber #a0a0a0, Gold #806040 | `burg_03` #e0e0e0, #e0e0c0, #808080 | nein (der Burg fehlt nur das Tannengrün) |
| **Schattenfaust** | **Trolle** | **Rot, Schwarz, Gold** · `wappen_08` #000000, #200000, #400000, #600000, #802020 | `burg_05` **Grün/Oliv** #202000, #404020, #204000, #402000 | **JA**: grüne Szene, rot-schwarze Banner. **So gewollt, kein Fehler.** |
| Knochenmoor | Ghule | Violett, Schwarz · `wappen_02` #000000, #402060, #402040 | `burg_04` #202040, #404060, #000020; dazu grüne Feuer (Daniel) | nein |
| **Flickwerk** | **Gnome** | **Grau, Schwarz, Gold** · `wappen_05` #002040, #404040, #202040 | `burg_06` **Eisblau/Weiß** #e0e0e0, #80a0c0, #4060a0, #204060 | **JA**: eisblaue Szene, grau-schwarz-goldene Banner, **zusätzlich** marineblaues Tuch #103050 (D11). **So gewollt.** |

**Für die sechs Kopfbänder (B8) heißt das:** Grundton = Burg · Banner und Akzent = Chronik · bei den Gnomen zusätzlich Marineblau. **Alle anderen Dateien** (B1, B2, B5, B9, B10, B12, B13) sind keinem Haus zugeordnet und folgen nur ihrem Block.

---

## 3. Gemeinsame Vorgaben

**Für alle 18 Dateien:**
- keine Schrift, keine Ziffern, kein Logo, kein Wasserzeichen, keine Beschriftung, keine Knöpfe;
- keine Rahmen im Bild, außer bei B13 (D8);
- keine Wölfe, kein Helm und keine Helmzier, keine Gesichter als Hauptmotiv, keine echte Person, kein Blut.

**Freisteller:** Im durchsichtigen Bereich müssen die Farbwerte **schwarz** sein (RGB 0, 0, 0). Sonst entsteht beim Verkleinern ein heller Saum; die Meshy-Vorlage hatte dort zu 60,4 % Lavendel [gH].

**Negativ-Grundblock N:**

```
text, letters, numbers, logo, watermark, signature, button, UI, frame, wolf, helmet, crest, close-up face, portrait, real person, blood, cartoon, emoji, photo, 3D render, black outlines
```

---

## 4. Die 18 Blöcke

### B1 · `ruine_weltkarte_176.png`

1. **Motiv:** Ein eingestürzter Steinturm: ein Stumpf mit gezackter Bruchkante, davor eine leere Hortmulde mit zwei abgeworfenen Drachenschuppen. Ansicht schräg von oben, wie die Burgen auf der Weltkarte. Das Motiv füllt die Höhe des Quadrats, links und rechts bleibt es durchsichtig.
2. **In Spielgröße (19–44 px):** bleibt der **senkrechte Stumpf mit zackiger Oberkante**, damit er weder Burg noch Drache ist. / Darf wegfallen: Schuppen, Mauerfugen.
3. **Farben:** Stein #303030, #505050 · Moos #305010 · Schatten #101010 [gC]
4. **Verboten:** Drache, Gold oder Schätze, Knochen, Figuren, angeschnittener Boden
5. **Seitenverhältnis:** 1 : 1, **176 × 176**, Toleranz **0 px**
6. **Transparenz:** PNG mit Alpha (Farbtyp 6). Auf Magenta gelegt ist alles außer Turm und Mulde Magenta, ohne hellen Saum.
7. **Prompt / Negativ:** Anhang A, Nr. 1

### B2 · `drache_gruen_176.png` (Tardas der Grüne)

1. **Motiv:** **Dieselbe Figur wie `drache_weiss.png`:** aufgerichtet, Kopf hochgelegt, Maul weit offen, Flügel ausgebreitet, auf einem Sockel über dunkler Platte [gH]. Gleicher Bildausschnitt. Anders sind nur zwei Dinge: Der Körper ist moosgrün mit goldenen Augen, und der Sockel besteht aus Moos und Ranken statt aus Eiskristall. Die Figur füllt die Höhe; die Breite beträgt etwa 118 px [r: 176 × 171 / 256].
2. **In Spielgröße:** bleibt der **erhobene Hals mit offenem Maul und Flügelzacken in Moosgrün**. / Darf wegfallen: Schuppenmuster, Augen.
3. **Farben:** Moos #305010, #507030 [gC] · Augen #f0d030, #d09010 [gC] · Platte #101010 [gC]
4. **Verboten:** Blau, Violett, Eis, Feuerstoß, Reiter, Hintergrund, andere Haltung
5. **Seitenverhältnis:** 1 : 1, **176 × 176**, 0 px
6. **Transparenz:** PNG mit Alpha (Farbtyp 6). Auf Magenta sind nur Drache und Sockel sichtbar, ohne Lavendel- oder Weißkante.
7. **Prompt / Negativ:** Anhang A, Nr. 2

### B2 · `drache_rot_176.png` (Salmur der Rote)

1. **Motiv:** Dieselbe Figur und Haltung wie der weiße Drache. Der Körper ist rot, die Flügel sehen aus wie verbranntes Leder, die Schuppen glühen wie Glut. Der Sockel besteht aus glühendem Gestein über dunkler Platte.
2. **In Spielgröße:** bleibt **dieselbe Silhouette, Rot auf Schwarz**. / Darf wegfallen: Einzelheiten der Glut.
3. **Farben:** #701010, #903030, #b03030, Glut #f07050 auf #101010 [gC, `wappen_08`]
4. **Verboten:** Violett, Eis, Feuerstoß, Opfer, Hintergrund, andere Haltung
5. **Seitenverhältnis:** 1 : 1, **176 × 176**, 0 px
6. **Transparenz:** wie beim grünen Drachen
7. **Prompt / Negativ:** Anhang A, Nr. 3

### B5 · `startbild_anmelden_4096x2880.jpg`

1. **Motiv:** Das Bild ist ein **Hintergrund hinter dem Anmeldeformular**, kein Schild. Es ersetzt das heutige Bild mit 813 × 324 [gH]. Zu sehen sind sechs schwebende Landbruchstücke im Nebel des Limbus, leuchtende Portale dazwischen und vorn unten ein Nebelsee. **Randlos gemalt und in der Mitte tragend**, denn das Spiel schneidet das Bild unter Wahrung des Seitenverhältnisses zu. Die Mitte (etwa 40 % der Breite) ist ruhig und dunkler; dort liegen Logo und Formular.
2. **In Spielgröße (1024 × 720, um 38 % abgedunkelt):** bleiben die **ruhige dunkle Mitte und die helleren Ränder**. / Darf wegfallen: Einzelheiten der Inseln.
3. **Farben:** Nebel #305050, #103030 · Nacht #101030, #103050 · Warm #503010 [gC]
4. **Verboten:** Alphakanal, Vignette als Rahmen, Figuren im Vordergrund, eine Sonnenscheibe in der Mitte, ein gemaltes Formular
5. **Seitenverhältnis:** 64 : 45, **4096 × 2880**, ±1 px
6. **Transparenz:** JPG, deckend. Auf Magenta gelegt bleibt kein Magenta sichtbar, alle vier Ränder sind bemalt.
7. **Prompt / Negativ:** Anhang A, Nr. 4

### B5 · `startbild_laden_4096x2880.jpg`

1. **Motiv:** **Hintergrund hinter dem Ladefortschritt.** Er ersetzt das heutige Bild mit 1100 × 640 [gH]. **Das Ladeschild (455 × 320) bleibt, wie es ist, und wird nicht neu gezeichnet.** Zu sehen ist ein Morgen an einem Nebelsee: eine kleine Siedlung mit Hütte, Feldern und Steg, Rauch aus den Schornsteinen, winzige Gestalten von hinten. Randlos gemalt, in der Mitte tragend, die Mitte und das untere Drittel ruhig.
2. **In Spielgröße (1024 × 720, um 30 % abgedunkelt):** bleiben der **helle Horizont und die ruhige Mitte** für das Schild. / Darf wegfallen: Gestalten.
3. **Farben:** wie das Startbild „Anmelden“, dazu Morgenlicht #b07030 [gC]
4. **Verboten:** Alphakanal, Gesichter, Kampf, ein gemaltes Schild oder Panel
5. **Seitenverhältnis:** 64 : 45, **4096 × 2880**, ±1 px
6. **Transparenz:** wie beim Startbild „Anmelden“
7. **Prompt / Negativ:** Anhang A, Nr. 5

### B8 · die sechs Kopfbänder (gemeinsame Felder)

**Gemeinsam gilt für alle sechs:**

- **Bildaufbau:** Hauptmotiv **links**, rechts eine ruhige Fläche für Text. Das Bild ist randlos gemalt. Alles Wichtige liegt im mittleren 90 % der Höhe, weil das Spiel bei 1127 px Breite 17 px wegschneidet [gH].
- **Banner:** Sie tragen die Hausfarben der Chronik als einfache Fahnen, **ohne ausgearbeitetes Wappen**.
- **Verboten:** Alphakanal, ein ausgearbeitetes Wappen im Bild, große Figuren.
- **In Spielgröße darf wegfallen:** Figuren, Werkzeug, kleine Bauten.
- **Seitenverhältnis:** 4508 : 868 (≈ 5,194 : 1), **4508 × 868**, ±1 px.
- **Transparenz:** PNG **ohne** Alpha (Farbtyp 2, RGB). Auf Magenta gelegt bleibt kein Magenta sichtbar, und kein Rand ist leer.

| Datei | 1. Motiv (Herrschaftssitz nach Chronik) | 2. In Spielgröße muss bleiben | 3. Grundton (Burg) [gH] | 3. Akzent (Heraldik) |
|---|---|---|---|---|
| `portal_kopfband_menschlich_4508x868.png` | links die Burg Silberbach aus Holz, Lehm und Flussstein an einer Furt; der schimmernde Bach, Fischerboote; rechts ruhige Flussaue | Burgsilhouette mit roten Bannern | Beige #e0c0a0, #c0a080, #404020 | rot-goldene Banner #600000, #a06020 |
| `portal_kopfband_zwergisch_4508x868.png` | links die Tiefenfeste, ein in den Fels geschlagenes Tor mit goldenem Schmiedeglühen, Rauch aus Schächten; rechts ruhige Schneeberge | Felstor mit Glutlicht | Grau #404040, #202020, warm #c0a0a0 | grau-schwarz-goldene Banner #202020, #000000, #604020 |
| `portal_kopfband_elfisch_4508x868.png` | links die Turmstadt Silberlaub auf hohen Bäumen und weißen Plattformen; Sternenlicht durch Nebel; rechts ruhiger Wald | schlanke Türme in Baumkronen | Weiß und Silber #e0e0e0, #e0e0c0, #808080 | tannengrün-silber-goldene Banner #002020, #004040, #a0a0a0, #806040 |
| `portal_kopfband_trolle_4508x868.png` | links die Felsfeste aus **moosbewachsenem** Basalt und Geröll, dicke Mauern, schmale glühende Fenster, davor der Fels mit dem Faustabdruck; rechts ein ruhiges grün-olives Bergland **[V]** (siehe 8.3) | Festungsblock mit roten Bannern vor grünem Land | Grün/Oliv #202000, #404020, #204000, #402000 | rot-schwarz-goldene Banner #000000, #400000, #802020 |
| `portal_kopfband_schmiede_dorf_ghule_4508x868.png` | links die Sumpfzitadelle aus weißem Stein auf versteinerten Bäumen, Rippentor, **grüne Feuer** in den Hütten, Schilfnachen; rechts Moor im Nebel | helle Zitadelle vor dunklem Moor, grüne Lichtpunkte | Blauviolett #202040, #404060, #000020 | violett-schwarze Banner #402060, #402040, #000000 |
| `portal_kopfband_gnome_4508x868.png` | links die treibende Insel Flickwerk mit Werkstätten, Winden, Zahnrädern und Seilbrücken zu kleinen Nachbarinseln; rechts Limbusnebel | Insel-Silhouette mit Seilbrücken | Eisblau/Weiß #e0e0e0, #80a0c0, #4060a0, #204060 | grau-schwarz-goldene Banner #404040, #202040, dazu **marineblaues Tuch #103050 [D11]** |

7. **Prompt / Negativ:** Anhang A, Nr. 6 bis 11

### B9 · `weltkarte_goldrahmen_3680.png`

1. **Motiv:** Ein schmaler Goldrahmen um ein Quadrat, innen vollständig durchsichtig. Das **Band** ist **3,75 % = 138 px** breit [gH, am Bestand 15 px von 400]; im Spiel sind das 15 px bei 400 und 34 px bei 920 Breite. Der **Eckenradius** beträgt **7,5 % = 276 px** [Datenwert `weltkarte_ecke: 30` von 400, nicht am Bild gemessen]. Feine, gleichmäßige Gravur, an jeder Ecke ein kleines Ornament.
2. **In Spielgröße (400 px):** bleibt das **geschlossene Goldband mit runden Ecken**. / Darf wegfallen: Gravur, Ornament.
3. **Farben:** #b07010, #d09010, #f0d030, Schatten #905010 [gC]
4. **Verboten:** Füllung innen, Edelsteine, Verlauf nach innen
5. **Seitenverhältnis:** 1 : 1, **3680 × 3680**, ±1 px
6. **Transparenz:** PNG mit Alpha (Farbtyp 6). Der Mittelpunkt ist durchsichtig, das Band deckend; auf Magenta ist das Innere ganz Magenta.
7. **Prompt / Negativ:** Anhang A, Nr. 12

### B10 · `kachelrahmen_ruhe_256.png`

1. **Motiv:** Ein matter Bronzerahmen um ein Quadrat, mit kleinen Eckverstärkungen, die leicht über die Kante stehen, wie im Bestand [gC]. **Band 12,5 % = 32 px** [gH]. In der Datei ist das Metall voll deckend; das Spiel legt selbst 35 % Deckkraft darüber.
2. **In Spielgröße (57–64 px, Band ≈ 7 px):** bleibt das **geschlossene Bronzequadrat**. / Darf wegfallen: Eckverstärkungen.
3. **Farben:** #705030, #907050, #d0b070 [gC]
4. **Verboten:** Füllung, Glanzpunkte, halbdurchsichtiges Metall
5. **Seitenverhältnis:** 1 : 1, **256 × 256**, 0 px
6. **Transparenz:** PNG mit Alpha (Farbtyp 6). Die Mitte ist durchsichtig, das Band voll deckend (nicht 35 %).
7. **Prompt / Negativ:** Anhang A, Nr. 13
- **Eckenradius:** **UNBEKANNT** am Bestand. **[V]** Außenradius 1,5 × Band = **18,75 % = 48 px**; dann bleibt innen eine gerundete Öffnung von 6,25 % = 16 px [r].

### B10 · `kachelrahmen_auswahl_256.png`

1. **Motiv:** **Dieselbe Form** und derselbe Eckenradius wie der Ruherahmen. Das **Band ist 15,6 % = 40 px** breit, einschließlich eines warmen inneren Glühens [gH]. Hell poliertes Gold.
2. **In Spielgröße:** bleibt **deutlich heller und warm leuchtend gegenüber dem Ruherahmen**. / Darf wegfallen: Glanzpunkte.
3. **Farben:** #d09010, #d07010, #f09010, #f0d030 [gC]
4. **Verboten:** andere Form oder anderer Radius als der Ruherahmen, Füllung
5. **Seitenverhältnis:** 1 : 1, **256 × 256**, 0 px
6. **Transparenz:** PNG mit Alpha (Farbtyp 6). Die Mitte ist durchsichtig, das Glühen läuft nach innen halbdurchsichtig aus.
7. **Prompt / Negativ:** Anhang A, Nr. 14
- **Eckenradius:** wie beim Ruherahmen **[V]** 48 px, damit beide deckungsgleich sind.

### B12 · `leiste_mitte_256x136.png`

1. **Motiv:** Dunkles ochsenblutrotes Leder mit feiner Narbung, unten eine dezente Naht. **Waagerecht nahtlos**, denn das Stück wird im Spiel wiederholt, nie gedehnt. Kein Detail größer als 24 px.
2. **In Spielgröße (64 × 34):** bleibt eine **gleichmäßig dunkle Fläche ohne sichtbare Wiederholung**. / Darf wegfallen: Narbung.
3. **Farben:** Mittel #1a0a09, kein Pixel heller als #3e1c1a (Handbuch, T08)
4. **Verboten:** helle Stellen, Verlauf über die Breite, Symbole
5. **Seitenverhältnis:** 32 : 17, **256 × 136**, 0 px
6. **Transparenz:** PNG mit Alpha (Farbtyp 6); das Leder darf überall deckend sein. Linke und rechte Pixelspalte sind farbgleich (±6 je Kanal).
7. **Prompt / Negativ:** Anhang A, Nr. 15

### B12 · `leiste_ende_links_64x136.png`

1. **Motiv:** Links eine vergoldete Metallkappe. Rechts läuft das Leder in Höhe und Farbe passend zur Mitte bis an die Kante.
2. **In Spielgröße (16 × 34):** bleiben die **Kante und die Goldkappe**. / Darf wegfallen: Nieten.
3. **Farben:** Leder #1a0a09 · Gold #b8862e (Handbuch), #d09010 [gC]
4. **Verboten:** Ornamente im Lederteil
5. **Seitenverhältnis:** **8 : 17**, **64 × 136**, 0 px
6. **Transparenz:** PNG mit Alpha (Farbtyp 6). Links von der Kappe ist alles durchsichtig; die rechte Pixelspalte ist deckend und farbgleich mit der linken Spalte der Mitte (±6).
7. **Prompt / Negativ:** Anhang A, Nr. 16

### B12 · `leiste_ende_rechts_64x136.png`

1. **Motiv:** Spiegelbild des linken Endstücks; darf gespiegelt geliefert werden.
2. **In Spielgröße / 3. Farben / 4. Verboten:** wie beim linken Endstück
5. **Seitenverhältnis:** **8 : 17**, **64 × 136**, 0 px
6. **Transparenz:** PNG mit Alpha (Farbtyp 6). Rechts von der Kappe ist alles durchsichtig; die linke Pixelspalte ist deckend und farbgleich mit der rechten Spalte der Mitte (±6).
7. **Prompt / Negativ:** Anhang A, Nr. 17

### B13 · `marktplatz_kennzeichen_384.png`

1. **Motiv:** Chris' Marktstand: rot-weiß gestreiftes Sonnendach, Fässer, Säcke und Kisten, ein Banner mit Beutelzeichen, Laternenlicht, dunkle Umgebung. **Mit dem schmalen, abgerundeten Goldrahmen wie im Bestand [D8].** Deckend, bis an den Rand gemalt.
2. **In Spielgröße (96 px):** bleibt das **rot-weiß gestreifte Dach**. / Darf wegfallen: die Waren in den Kisten.
3. **Farben:** Bild #101010, #301010, #503010, #703010, #905030, #b07030 [gC]. **Rahmen** außen etwa 3 % (≈ 12 px bei 384 [r]), Gold #b8a270, Lichtkante #eee6b6, dunkle Seite #a27239 [gC].
4. **Verboten:** Alphakanal, Gesicht eines Händlers, Schrift auf dem Banner. **„frame“ ist hier erlaubt (D8).**
5. **Seitenverhältnis:** 1 : 1, **384 × 384**, 0 px
6. **Transparenz:** PNG **ohne** Alpha (Farbtyp 2, RGB). Auf Magenta gelegt bleibt nichts Magenta.
7. **Prompt / Negativ:** Anhang A, Nr. 18

---

## Anhang A – die Prompts zum Kopieren

Jeder Negativ-Prompt ist **vollständig ausgeschrieben** (mit Grundblock N), damit man ihn ohne Nachschlagen kopieren kann.

**1 · ruine_weltkarte_176.png**
```
Painted fantasy map icon, square, transparent background with black RGB: collapsed stone tower stump with jagged broken top, empty hoard hollow in front with two shed dragon scales, three-quarter top view, warm light top left, object fills the height, readable silhouette at 20 pixels.
```
```
text, letters, numbers, logo, watermark, signature, button, UI, frame, wolf, helmet, crest, close-up face, portrait, real person, blood, cartoon, emoji, photo, 3D render, black outlines, dragon, gold, treasure, bones, people, ground cut off at edge
```

**2 · drache_gruen_176.png**
```
Painted fantasy map figure, square, transparent background with black RGB: same pose and framing as the reference white dragon, rearing up, head thrown back, jaws wide open, wings spread, on a small base of moss and vines over a dark plate, moss-green vine-like body, leaf-shaped jagged scales, golden eyes, figure fills the height.
```
```
text, letters, numbers, logo, watermark, signature, button, UI, frame, wolf, helmet, crest, close-up face, portrait, real person, blood, cartoon, emoji, photo, 3D render, black outlines, blue, purple, ice, fire breath, rider, background, different pose
```

**3 · drache_rot_176.png**
```
Painted fantasy map figure, square, transparent background with black RGB: same pose and framing as the reference white dragon, rearing up, head thrown back, jaws wide open, wings spread, on a small base of glowing ember rock over a dark plate, red body, wings like scorched leather, scales glowing like embers, figure fills the height.
```
```
text, letters, numbers, logo, watermark, signature, button, UI, frame, wolf, helmet, crest, close-up face, portrait, real person, blood, cartoon, emoji, photo, 3D render, black outlines, purple, ice, fire breath, victims, background, different pose
```

**4 · startbild_anmelden_4096x2880.jpg**
```
Painted fantasy panorama, aspect 64:45, full bleed to all edges: six floating land fragments in glowing mist with forests, mountains and a misty swamp, faint luminous portals between them, misty lake at the bottom, warm backlight top left, cool blue shadows, central forty percent calm and darker.
```
```
text, letters, numbers, logo, watermark, signature, button, UI, frame, wolf, helmet, crest, close-up face, portrait, real person, blood, cartoon, emoji, photo, 3D render, black outlines, transparency, vignette, border, sun disc in center, people in foreground, login panel
```

**5 · startbild_laden_4096x2880.jpg**
```
Painted fantasy panorama, aspect 64:45, full bleed: dawn over a misty lake, small settlement with a woodcutter hut, fields and a wooden jetty, chimney smoke, tiny workers seen from behind in the distance, golden backlight, blue mist, calm centre and calm lower third.
```
```
text, letters, numbers, logo, watermark, signature, button, UI, frame, wolf, helmet, crest, close-up face, portrait, real person, blood, cartoon, emoji, photo, 3D render, black outlines, transparency, faces, battle, sign, panel
```

**6 · portal_kopfband_menschlich_4508x868.png**
```
Painted fantasy banner landscape, aspect 4508:868, full bleed, opaque: on the left a castle of timber, clay and river stone at a shallow ford, warm beige stone and timber tones, simple deep red and gold banners, a silver-shimmering brook, small fishing boats, moonlit evening; calm open river meadow on the right; key content in the middle ninety percent of the height.
```
```
text, letters, numbers, logo, watermark, signature, button, UI, frame, wolf, helmet, crest, close-up face, portrait, real person, blood, cartoon, emoji, photo, 3D render, black outlines, transparency, detailed coat of arms, large figures
```

**7 · portal_kopfband_zwergisch_4508x868.png**
```
Painted fantasy banner landscape, aspect 4508:868, full bleed, opaque: on the left a fortress gate carved into grey rock with a golden forge glow inside, smoke from mine shafts, grey and black stone with warm light, simple grey, black and gold banners; calm snowy mountains on the right; key content in the middle ninety percent of the height.
```
```
text, letters, numbers, logo, watermark, signature, button, UI, frame, wolf, helmet, crest, close-up face, portrait, real person, blood, cartoon, emoji, photo, 3D render, black outlines, transparency, readable runes, detailed coat of arms, large figures
```

**8 · portal_kopfband_elfisch_4508x868.png**
```
Painted fantasy banner landscape, aspect 4508:868, full bleed, opaque: on the left slender towers on tall trees and white stone platforms, white and silver architecture, simple fir-green banners with silver and gold, starlight through drifting mist; calm forest on the right; key content in the middle ninety percent of the height.
```
```
text, letters, numbers, logo, watermark, signature, button, UI, frame, wolf, helmet, crest, close-up face, portrait, real person, blood, cartoon, emoji, photo, 3D render, black outlines, transparency, detailed coat of arms, large figures
```

**9 · portal_kopfband_trolle_4508x868.png**
```
Painted fantasy banner landscape, aspect 4508:868, full bleed, opaque: on the left a massive fortress of moss-covered basalt and rubble with narrow glowing windows, a boulder with a giant fist imprint, green and olive landscape tones, simple red, black and gold banners; calm green-olive mountains on the right; key content in the middle ninety percent of the height.
```
```
text, letters, numbers, logo, watermark, signature, button, UI, frame, wolf, helmet, crest, close-up face, portrait, real person, blood, cartoon, emoji, photo, 3D render, black outlines, transparency, detailed coat of arms, large figures
```

**10 · portal_kopfband_schmiede_dorf_ghule_4508x868.png**
```
Painted dark fantasy banner landscape, aspect 4508:868, full bleed, opaque: on the left a white stone citadel on a hill of petrified trees with a gate of curved ribs, eerie green fires in small huts, reed boats on black water, deep blue-violet night tones, simple violet and black banners; calm foggy swamp on the right; key content in the middle ninety percent of the height.
```
```
text, letters, numbers, logo, watermark, signature, button, UI, frame, wolf, helmet, crest, close-up face, portrait, real person, blood, cartoon, emoji, photo, 3D render, black outlines, transparency, corpses, detailed coat of arms, large figures
```

**11 · portal_kopfband_gnome_4508x868.png**
```
Painted fantasy banner landscape, aspect 4508:868, full bleed, opaque: on the left a floating island crowded with small workshops, winches and cogwheels, rope bridges to smaller islands, ice-blue and white scene tones, simple grey, black and gold banners and navy blue cloth awnings; calm limbo mist on the right; key content in the middle ninety percent of the height.
```
```
text, letters, numbers, logo, watermark, signature, button, UI, frame, wolf, helmet, crest, close-up face, portrait, real person, blood, cartoon, emoji, photo, 3D render, black outlines, transparency, detailed coat of arms, large figures
```

**12 · weltkarte_goldrahmen_3680.png**
```
Ornamental aged gold frame, square, transparent background with black RGB: band 3.75 percent of the edge, rounded corners 7.5 percent radius, fine even engraving, small ornament at each corner, highlight top left, completely empty transparent interior.
```
```
text, letters, numbers, logo, watermark, signature, button, UI, wolf, helmet, crest, close-up face, portrait, real person, blood, cartoon, emoji, photo, 3D render, black outlines, filled centre, gemstones, inner gradient
```

**13 · kachelrahmen_ruhe_256.png**
```
Matte bronze square tile frame, transparent background with black RGB: band 12.5 percent of the edge, rounded corners about 19 percent radius, small corner reinforcements protruding slightly, worn metal, even light, fully opaque metal, empty transparent interior.
```
```
text, letters, numbers, logo, watermark, signature, button, UI, wolf, helmet, crest, close-up face, portrait, real person, blood, cartoon, emoji, photo, 3D render, black outlines, filled centre, shine spots, glow, semi-transparent metal
```

**14 · kachelrahmen_auswahl_256.png**
```
Bright polished gold square tile frame, same shape and corner radius as the matte bronze frame, transparent background with black RGB: band 15.6 percent including a warm inner glow, highlight top left, empty transparent interior.
```
```
text, letters, numbers, logo, watermark, signature, button, UI, wolf, helmet, crest, close-up face, portrait, real person, blood, cartoon, emoji, photo, 3D render, black outlines, filled centre, different shape
```

**15 · leiste_mitte_256x136.png**
```
Seamless horizontally tileable strip texture, aspect 256:136: very dark oxblood leather, faint grain, subtle stitched seam along the bottom, extremely low contrast, left and right edges match exactly.
```
```
text, letters, numbers, logo, watermark, signature, button, UI, frame, wolf, helmet, crest, close-up face, portrait, real person, blood, cartoon, emoji, photo, 3D render, black outlines, bright spots, gradient across, ornaments, symbols
```

**16 · leiste_ende_links_64x136.png**
```
End cap for a dark leather strip, aspect 64:136, transparent background with black RGB: aged gold metal clasp on the left closing very dark oxblood leather that runs to the right edge matching the tiled strip, highlight top left.
```
```
text, letters, numbers, logo, watermark, signature, button, UI, frame, wolf, helmet, crest, close-up face, portrait, real person, blood, cartoon, emoji, photo, 3D render, black outlines, ornaments on leather, rivets
```

**17 · leiste_ende_rechts_64x136.png**
```
Mirror image of the left end cap, aspect 64:136, transparent background with black RGB: aged gold clasp on the right closing very dark oxblood leather that runs to the left edge.
```
```
text, letters, numbers, logo, watermark, signature, button, UI, frame, wolf, helmet, crest, close-up face, portrait, real person, blood, cartoon, emoji, photo, 3D render, black outlines, ornaments on leather, rivets
```

**18 · marktplatz_kennzeichen_384.png**
```
Painted fantasy market stall emblem, square, opaque, full bleed: red and white striped awning, barrels, sacks and crates, hanging banner with a coin-pouch sign, warm lantern light, dark surroundings, thin rounded gold border.
```
```
text, letters, numbers, logo, watermark, signature, button, UI, wolf, helmet, crest, close-up face, portrait, real person, blood, cartoon, emoji, photo, 3D render, black outlines, transparency, merchant face, embossed coins
```

---

## Anhang B – Abnahme in Zahlen (maschinell prüfbar)

| Nr | Datei | Format | Farbtyp | Mindestmaß | Verhältnis | Toleranz |
|---|---|---|---|---|---|---|
| 1 | `ruine_weltkarte_176.png` | png | 6 | 176 × 176 | 1 : 1 | 0 |
| 2 | `drache_gruen_176.png` | png | 6 | 176 × 176 | 1 : 1 | 0 |
| 3 | `drache_rot_176.png` | png | 6 | 176 × 176 | 1 : 1 | 0 |
| 4 | `startbild_anmelden_4096x2880.jpg` | jpg | – | 4096 × 2880 | 64 : 45 | ±1 |
| 5 | `startbild_laden_4096x2880.jpg` | jpg | – | 4096 × 2880 | 64 : 45 | ±1 |
| 6–11 | `portal_kopfband_*_4508x868.png` (6) | png | **2** | 4508 × 868 | 4508 : 868 | ±1 |
| 12 | `weltkarte_goldrahmen_3680.png` | png | 6 | 3680 × 3680 | 1 : 1 | ±1 |
| 13 | `kachelrahmen_ruhe_256.png` | png | 6 | 256 × 256 | 1 : 1 | 0 |
| 14 | `kachelrahmen_auswahl_256.png` | png | 6 | 256 × 256 | 1 : 1 | 0 |
| 15 | `leiste_mitte_256x136.png` | png | 6 | 256 × 136 | 32 : 17 | 0 |
| 16 | `leiste_ende_links_64x136.png` | png | 6 | 64 × 136 | 8 : 17 | 0 |
| 17 | `leiste_ende_rechts_64x136.png` | png | 6 | 64 × 136 | 8 : 17 | 0 |
| 18 | `marktplatz_kennzeichen_384.png` | png | **2** | 384 × 384 | 1 : 1 | 0 |

**Regeln dazu:**
- **Toleranz:** Die Höhe gilt relativ zur Breite, also |H − round(B × Verhältnis)| ≤ Toleranz.
- **Toleranz 0** bedeutet: Das Maß ist genau das Mindestmaß.
- **Leiste:** Zwei Spaltenpaare müssen je Kanal auf ±6 farbgleich sein:
  1. Spalte 0 und Spalte 255 der Mitte;
  2. Spalte 63 von `ende_links` und Spalte 0 der Mitte, ebenso Spalte 0 von `ende_rechts` und Spalte 255 der Mitte.
- **Freisteller (Farbtyp 6):**
  - Bei Nr. 12–14 hat der Mittelpunkt Alpha 0; bei Nr. 1–3 gilt das für die linke und die rechte Randspalte.
  - Pixel mit Alpha 0 sind RGB (0, 0, 0).
  - Kein heller Saum: Pixel mit 0 < Alpha < 255 haben keine Helligkeit über der der deckenden Nachbarn. Dafür braucht es eine zweite Wache mit Pillow.

---

## Anhang C – der Zehn-Sekunden-Check für Daniel

| Nr | Datei | Frage |
|---|---|---|
| 1 | Ruine | Auf der Weltkarte bei kleinstem Feld: Siehst du einen Turmstumpf und keine Burg und keinen Drachen? |
| 2 | Drache grün | Neben dem weißen Drachen: gleiche Haltung, eindeutig moosgrün, kein Blau? |
| 3 | Drache rot | Neben dem weißen Drachen: gleiche Haltung, eindeutig rot, kein Violett? |
| 4 | Startbild Anmelden | Sind Logo und Formular in der Mitte ohne Mühe lesbar? |
| 5 | Startbild Laden | Ist das Bild ruhig, ohne Schrift, und zieht nichts den Blick vom Ladeschild ab? |
| 6–11 | Kopfbänder | Erkennst du das Haus am Gebäude und an den Bannerfarben, ohne den Namen zu lesen? (Trolle: grünes Land, **rote** Banner; Gnome: eisblau, mit **marineblauem** Tuch) |
| 12 | Goldrahmen | Ist das Band bei 400 px gleichmäßig, mit runden Ecken und ohne Füllung innen? |
| 13 | Ruherahmen | Sind auf der Siedlungskarte die Felder getrennt zu sehen, ohne dass der Rahmen das Gelände übertönt? |
| 14 | Auswahlrahmen | Springt beim Anklicken das gewählte Feld sofort ins Auge? |
| 15 | Leiste Mitte | Siehst du beim Breitziehen des Fensters eine Naht oder ein Wiederholungsmuster? |
| 16–17 | Leiste Enden | Schließen die Goldkappen links und rechts sauber an das Leder an? |
| 18 | Marktplatz | Erkennst du bei 96 px das gestreifte Dach und den Goldrahmen auf den ersten Blick? |

---

## 7. Was gegenüber Fassung 2 anders ist (zum zeilenweisen Nachrechnen)

| # | Stelle | Fassung 2 | Fassung 3 | Grund |
|---|---|---|---|---|
| 1 | Sternenwacht-Wappen | `wappen_09`, #101030 / #103050 / #f0f0f0 | **`elfen_wappen.png`**, #002020 / #004040 / #a0a0a0 / #806040 [gH] | Berichtigung (Nachrechnung 21, Abschnitt 2) |
| 2 | Hausfarben der Kopfbänder | nur Wappenfarben | **Grundton = Burg [gH], Akzent = Chronik**, eigener Abschnitt 2 | Daniel 18.11. (D-c, Klärung, „Heraldik und Szene“) |
| 3 | Trolle-Kopfband | Basalt in Rot und Schwarz | **moosbewachsener Basalt im grün-oliven Land, rot-schwarz-goldene Banner [V]** | D-c, Abschnitt 2 |
| 4 | Gnome-Kopfband | offen: navy oder ice | **eisblaue Szene, grau-schwarz-goldene Banner, marineblaues Tuch** | D-c + D11 + Klärung |
| 5 | Elfen-Kopfband | Nachtblau-Weiß-Silber | **Weiß und Silber (Burg), Banner tannengrün, silber, gold** | Berichtigung 1 + Abschnitt 2 |
| 6 | Menschen-, Zwergen- und Ghule-Kopfband | nur Wappenfarben | Burgfarben als Grundton ergänzt (#e0c0a0 / #404040 / #202040 …) | Abschnitt 2 |
| 7 | B13 Goldrahmen | offen | **bleibt**; Prompt mit „thin rounded gold border“, „frame“ nicht im Negativ | D8 |
| 8 | B13 Rahmenbreite | ≈ 3 px bei 96 | zusätzlich **≈ 12 px bei 384** [r] | Umrechnung auf 4× |
| 9 | Toleranzen | 0 / ±1 als Vorschlag | **festgelegt** (Anhang B) | Nachrechnung 21, Abschnitt 1.5 |
| 10 | Kopfband-Prompts | „no coat of arms“ | „**simple banners** in house colours, no **detailed** coat of arms“ | Banner sind jetzt erwünscht (Heraldik als Akzent) |
| 11 | Negativ-Prompts | Verweis „N, …“ | **vollständig ausgeschrieben** (Anhang A) | zum Kopieren |
| 12 | Leistenprüfung | nur Mitte | zusätzlich **beide Endstücke gegen die Mitte** (Anhang B) | Anhang B des Auftrags |

---

## 8. Für Weltenfresser (nicht an den Zeichner, Zusatzinformationen)

> Hinweise, keine Anweisungen.

**8.1 Sternenwacht: drei Quellen, die nicht übereinstimmen.**
- Die Zuordnung, die Daniel am 13.11. bestätigt hat (Auftrag 17, Abschnitt 6; Auftrag 18, Teil C), lautete wörtlich „Sternenwacht `burg_03` + **`wappen_09`**“.
- F-103 sagt: „Meshy-Bilder sind **Stilvorlage, kein Spielinhalt**“.
- `data/haeuser.json` führt laut deiner Messung `elfen_wappen.png`, also das Meshy-Bild als **Spielinhalt**.

Ich habe deine Berichtigung übernommen, weil `haeuser.json` die verbindliche Quelle ist. **Bitte im Register festhalten, wann und von wem auf `elfen_wappen.png` umgestellt wurde, und F-103 entsprechend einschränken.** Sonst liest das der nächste Leser als Widerspruch.

**8.2 Sternenwacht in der Chronik.** Meine Kopie `CHRONIK_DER_WELT_20261104.txt` (Zeile 236) sagt: „Die Farben des Hauses sind Weiß, Silber und **Nachtblau** … silberne Mondsichel mit einem achtzackigen goldenen Stern … auf nachtblauem Grund“. Dein Auftrag (Abschnitt 2.6) zitiert die Chronik als „Weiß, Silber, Gold und **Tannengrün**“ und sagt, sie sei „unverändert“. **Eins von beiden ist veraltet.** Die Stern-Fahne von `burg_03` [gH] passt zur Fassung vom 04.11., das Tannengrün zum Meshy-Wappen. Dieses Dokument folgt deiner Fassung. **Bitte die aktuelle Chronikzeile mit Datum ins Register.**

**8.3 Trolle: Baumburg gegen Basaltfeste.** `burg_05` zeigt eine **Baumburg mit Wasserfällen und grünem Blatt-Banner** [gC, angesehen]; die Chronik beschreibt eine **klobige Basaltfeste**. Mein Kopfband-Motiv „moosbewachsener Basalt im grünen Land“ ist ein **Vorschlag [V]**: Es verbindet die Geschichte (Basalt) mit der Burgfarbe (Grün/Oliv), so wie Daniel es verlangt hat („stimmig mit der Geschichte“). Die Stilfrage selbst (Baumburg für Trolle?) liegt weiter bei Daniel.

**8.4 D11 und der Gnomen-Prompt.** In 0.1 deines Auftrags steht „Gnomen-Prompt `navy blue`, nicht `ice blue`“; Abschnitt 2.6 und die Hausfarben-Regel sagen „eisblaue Szene, marineblaues Tuch zusätzlich“. Ich bin dem jüngeren Text gefolgt (2.6, 22:4x): Der Prompt enthält **beide** Farben, jede mit ihrer Rolle. **Bitte im Register die Zeile in 0.1 so nachziehen**, sonst prüft jemand den Prompt gegen die alte Zeile.

**8.5 Weltkartenband 15 px gegen Datenwert 14 px.** Nach dem Austausch des Bildes muss `weltkarte_rand` in `gebaeude_motive.json` neu gesetzt werden. Das steht schon in der Aktivierung der Liste; ich erinnere nur daran, weil sonst der Code mit 14 px rechnet, während das Bild 15 px zeigt.

---

Ende der Zeichner-Fassung (Fassung 3).
