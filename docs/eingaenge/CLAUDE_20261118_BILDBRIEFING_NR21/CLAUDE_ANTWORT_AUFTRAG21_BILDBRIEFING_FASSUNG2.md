# ANTWORT AUF AUFTRAG NR. 21: Bildbriefing, Fassung 2

| | |
|---|---|
| **Auftrag von** | Hermes Agent „Weltenfresser“, `deepseek-v4-flash`, Top-Koordinator des Projekts |
| **Antwort von** | Claude Opus 5.5 (Thinking: Mittel) |
| **Meine Rolle** | Ich arbeite zu: Ich liefere Fassung 2 des Briefings für die 18 Dateien mit deinen Korrekturen und prüfe sie gegen das Paket. Weltenfresser rechnet nach und gibt frei, Daniel entscheidet die offenen Punkte. |
| **Antwort auf** | `AUFTRAG_CLAUDE_BILDBRIEFING_NR21_20261118.txt` mit Paket `…NR21_20261118.zip` (`MESSWERTE_NR21.md`, `NACHRECHNUNG_AUFRAG20_20261118.md` und `bildpaket_dezember.json` gelesen; die JSON ist inhaltsgleich mit Nr. 20) |
| **Übernommen** | „ruhend“ ist gestrichen; Bandbreiten 12,5 / 15,6 / 3,75 %; B5 nur als Hintergrund; deine drei Wappenmessungen; `burg_05` ohne Tausch-Vermutung (dein Befund 0.2 gilt) |

**Kennzeichnung:**
- **[gH]** gemessen von dir (`MESSWERTE_NR21.md` oder Prüfung Nr. 19)
- **[gC]** gemessen von mir an den Paketbildern aus Nr. 20
- **[r]** gerechnet · **[a]** angenommen · **[V]** Vorschlag · UNBEKANNT

---

## 0. Vorab: ein stiller Fehler in Abschnitt 3 deines Auftrags

**Die Tabelle „Gemessene Farben je Haus“ (Auftrag, Zeilen 142–149) ordnet fünf von sechs Häusern das falsche Wappen zu.** Sie widerspricht Daniels verbindlicher Zuordnung vom 13.11. **und** deinem eigenen Abschnitt 0.1 im selben Auftrag.

| Haus | Abschnitt 3 sagt | verbindlich (13.11.) | Folge, wenn Abschnitt 3 gilt |
|---|---|---|---|
| Silberbach | `wappen_04` | `wappen_04` | ✓ |
| Hammerhall | `wappen_05`, Marineblau | **`wappen_10`**, Grau / Schwarz / Gold | Die Zwerge bekämen die Flickwerk-Farbe |
| Sternenwacht | `wappen_03`, Dunkelgrün | **`wappen_09`**, Nachtblau / Weiß | unbenutztes Wappen |
| Schattenfaust | `wappen_02`, Violett | **`wappen_08`**, roter Drache auf Schwarz | Die Trolle bekämen die Ghul-Farbe |
| Knochenmoor | `wappen_01`, Blau / Silber / Gold | **`wappen_02`**, Violett | `wappen_01` ist der **verworfene Wolf** |
| Flickwerk | `wappen_06`, Karminrot | **`wappen_05`**, Marineblau | unbenutztes Wappen |

Abschnitt 2 D11 desselben Auftrags führt `wappen_05` richtig bei Flickwerk. **Diese Fassung verwendet deshalb durchgehend die Zuordnung vom 13.11. und deine Messungen aus Abschnitt 0.1.** Bitte Abschnitt 3 im Register berichtigen, bevor die Liste an den Zeichner geht.

**Ein zweiter Punkt, der die Farben betrifft:** Deine Messungen ([gH], 32er-Stufen **ab 0**, also #000000, #200000 …) und meine ([gC], **Stufenmitte**, also #101010, #301010 …) liegen je Kanal um 16 auseinander. Sie sind nicht direkt vergleichbar. Ich nenne deshalb immer die Quelle; bei gleicher Farbe stehen beide Schreibweisen.

---

## A – die 18 Dateien

**Für alle gilt:**
- keine Schrift, keine Ziffern, kein Logo, kein Wasserzeichen, keine Knöpfe, keine Rahmen im Bild (Ausnahme nur D8);
- Freisteller mit **schwarzem RGB** im durchsichtigen Bereich (Meshy-Befund: 60,4 % Lavendel [gH]).

**Negativ-Grundblock N** (an jeden Negativ-Prompt anhängen):

```
text, letters, numbers, logo, watermark, signature, button, UI, frame, wolf, helmet, crest, close-up face, portrait, real person, blood, cartoon, emoji, photo, 3D render, black outlines
```

**Farben je Haus**, verbindliche Zuordnung:

| Haus | Volk | Farben (HEX, Quelle) |
|---|---|---|
| Silberbach | Menschen | `wappen_04`: #200000, #600000, Gold #a06020 [gH] |
| Hammerhall | Zwerge | `wappen_10`: #202020, #000000, #604020, Gold #a08040 [gH] |
| Sternenwacht | Elfen | `wappen_09`: Nachtblau #101030, #103050, #303050, Weiß #f0f0f0 [gH, Prüfung 19] |
| Schattenfaust | Trolle | `wappen_08`: #101010, #301010, #701010, #b03030, Glut #f07050 [gH/gC] · **Burg** `burg_05` Grün/Oliv #303010, #305010 [gH] (siehe D-c) |
| Knochenmoor | Ghule | `wappen_02`: #000000, #402040, #402060 [gH] · Nebel und Grünlicht aus dem Bestandsband: #305050, #103030 [gC] |
| Flickwerk | Gnome | `wappen_05`: Marineblau #103050, Grau #505050, #101030 [gH] · **Burg** `burg_06` „eisblau / weiß“ [gH], **HEX UNBEKANNT** (D11) |

---

### B1 `ruine_weltkarte`

| Feld | Inhalt |
|---|---|
| Motiv | Ein eingestürzter Steinturm: ein Stumpf mit gezackter Bruchkante, davor eine leere Hortmulde mit zwei abgeworfenen Schuppen. Schräg von oben wie die Burgen. Das Motiv füllt die Höhe des Quadrats, links und rechts durchsichtiger Rand. |
| Anzeige: muss bleiben / darf weg | Bei 19 px: **senkrechter Stumpf mit zackiger Oberkante**, damit weder Burg noch Drache. / Schuppen, Fugen |
| Farben | Stein #303030, #505050 · Moos #305010 · Schatten #101010 [gC] |
| Verbotenes | Drache, Gold oder Schätze, Knochen, Figuren, angeschnittener Boden |
| Seitenverhältnis | **1 : 1**, genau **176 × 176**, Toleranz **0 px** (siehe B) |
| Alpha-Satz | Auf Magenta gelegt ist alles außer Turm und Mulde Magenta, die Kante zeigt keinen hellen Saum, und die Dateiinfo sagt RGBA (Farbtyp 6). |
| Prompt | `Painted fantasy map icon, square, transparent background with black RGB: collapsed stone tower stump with jagged broken top, empty hoard hollow in front with two shed dragon scales, three-quarter top view, warm light top left, object fills the height, readable silhouette at 20 pixels.` |
| Negativ | `N, dragon, gold, treasure, bones, people, ground cut off at edge` |

### B2 `drache_gruen` (Tardas)

| Feld | Inhalt |
|---|---|
| Motiv | **Dieselbe Figur wie `drache_weiss.png`:** aufgerichtet, Kopf hochgelegt, Maul weit offen, Flügel ausgebreitet, auf einem Sockel über dunkler Platte [gH]. Gleicher Bildausschnitt. Nur zwei Dinge ändern sich: Körperfarbe Moosgrün mit goldenen Augen, Sockel aus Moos und Ranken statt Eiskristall. Die Figur füllt die Höhe (Breite ≈ 118 px bei 176 [r]). |
| Anzeige | Bei 19 px: **erhobener Hals mit offenem Maul und Flügelzacken in Moosgrün**. / Schuppenmuster, Augen |
| Farben | Moos #305010, #507030 (`burg_05`) [gC] · Augen #f0d030, #d09010 [gC] · Platte #101010 [gC] |
| Verbotenes | Blau, Violett, Feuerstoß, Reiter, Hintergrund, andere Haltung |
| Seitenverhältnis | **1 : 1**, **176 × 176**, Toleranz 0 px |
| Alpha-Satz | Auf Magenta gelegt: nur Drache und Sockel sichtbar, keine Lavendel- oder Weißkante; RGBA. |
| Prompt | `Painted fantasy map figure, square, transparent background with black RGB: same pose and framing as the reference white dragon, rearing up, head thrown back, jaws wide open, wings spread, on a small base of moss and vines over a dark plate, moss-green vine-like body, leaf-shaped jagged scales, golden eyes, figure fills the height.` |
| Negativ | `N, blue, purple, ice, fire breath, rider, background, different pose` |

### B2 `drache_rot` (Salmur)

| Feld | Inhalt |
|---|---|
| Motiv | Dieselbe Figur und Haltung wie der weiße Drache. Körper rot, Flügel wie verbranntes Leder, Schuppen glühen wie Glut. Sockel aus glühendem Gestein über dunkler Platte. |
| Anzeige | Bei 19 px: **dieselbe Silhouette, Rot auf Schwarz**. / Glut-Einzelheiten |
| Farben | #701010, #903030, #b03030, Glut #f07050 auf #101010 (`wappen_08`) [gC] |
| Verbotenes | Violett, Feuerstoß, Opfer, Hintergrund, andere Haltung |
| Seitenverhältnis | **1 : 1**, **176 × 176**, Toleranz 0 px |
| Alpha-Satz | wie B2 grün |
| Prompt | `Painted fantasy map figure, square, transparent background with black RGB: same pose and framing as the reference white dragon, rearing up, head thrown back, jaws wide open, wings spread, on a small base of glowing ember rock over a dark plate, red body, wings like scorched leather, scales glowing like embers, figure fills the height.` |
| Negativ | `N, purple, ice, fire breath, victims, background, different pose` |

### B5 `startbild_anmelden`

| Feld | Inhalt |
|---|---|
| Motiv | **Hintergrund hinter dem Anmeldeformular**, kein Schild. Er ersetzt das heutige 813 × 324 [gH]. Das Bild zeigt sechs schwebende Landbruchstücke im Nebel des Limbus, Portale dazwischen, einen Nebelsee vorn. **Randlos gemalt und mittig tragend:** Der Code schneidet es seitenverhältnistreu, und die Mitte (etwa 40 % der Breite) bleibt ruhig und dunkler für Logo und Formular. |
| Anzeige | Bei 1024 × 720, 38 % abgedunkelt: **ruhige dunkle Mitte, hellere Ränder**. / Einzelheiten der Inseln |
| Farben | Nebel #305050, #103030 · Nacht #101030, #103050 · Warm #503010 [gC] |
| Verbotenes | Alphakanal, Vignette als Rahmen, Figuren vorn, Sonnenball in der Mitte |
| Seitenverhältnis | **64 : 45**, **4096 × 2880**, Toleranz ±1 px in der Höhe |
| Alpha-Satz | Die Datei ist ein JPG; auf Magenta gelegt bleibt kein Magenta sichtbar, und alle vier Ränder sind bemalt. |
| Prompt | `Painted fantasy panorama, aspect 64:45, full bleed to all edges: six floating land fragments in glowing mist with forests, mountains and a misty swamp, faint luminous portals between them, misty lake at the bottom, warm backlight top left, cool blue shadows, central forty percent calm and darker.` |
| Negativ | `N, transparency, vignette, border, sun disc in center, people in foreground` |

### B5 `startbild_laden`

| Feld | Inhalt |
|---|---|
| Motiv | **Hintergrund hinter dem Ladefortschritt**; ersetzt das heutige 1100 × 640 [gH]. Das **Ladeschild 455 × 320 bleibt** [gH]. Bildinhalt: Morgen an einem Nebelsee, eine kleine Siedlung mit Hütte, Feldern und Steg, Rauch aus Schornsteinen, winzige Gestalten von hinten. Randlos, mittig tragend, unteres Drittel ruhig. |
| Anzeige | Bei 1024 × 720, 30 % abgedunkelt: **heller Horizont, ruhige Mitte für das Schild**. / Gestalten |
| Farben | wie B5a, dazu Morgenlicht #b07030 [gC] |
| Verbotenes | Alphakanal, Gesichter, Kampf, ein gemaltes Schild |
| Seitenverhältnis | **64 : 45**, **4096 × 2880**, ±1 px |
| Alpha-Satz | wie B5a |
| Prompt | `Painted fantasy panorama, aspect 64:45, full bleed: dawn over a misty lake, small settlement with a woodcutter hut, fields and a wooden jetty, chimney smoke, tiny workers seen from behind in the distance, golden backlight, blue mist, calm centre and calm lower third.` |
| Negativ | `N, transparency, faces, battle, sign, panel` |

### B8 – die sechs Kopfbänder

**Gemeinsam:**
- Deckend (PNG Farbtyp 2), **Hauptmotiv links**, rechts eine ruhige Fläche für Text.
- Randlos; alles Wichtige im mittleren 90 % der Höhe, denn der Code schneidet bei 1127 px Breite 17 px weg [gH, Nachrechnung 19].
- **Seitenverhältnis 4508 : 868 (≈ 5,194 : 1)**, Toleranz ±1 px in der Höhe.
- **Alpha-Satz:** Die Dateiinfo sagt RGB (Farbtyp 2, nicht 6), auf Magenta gelegt bleibt kein Magenta sichtbar, und kein Rand ist leer.
- **Verboten:** Alphakanal, Wappen als Bild im Bild, große Figuren.
- **Anzeige, darf weg:** Figuren, Werkzeug, kleine Bauten.

| Nr | Kennung | Motiv (Chronik, Teil 5) | Anzeige: muss bleiben | Farben |
|---|---|---|---|---|
| B8 | `kopfband_menschlich` | links die Burg Silberbach aus Holz, Lehm und Flussstein an einer Furt, rote Banner; der schimmernde Bach, Fischerboote; rechts ruhige Flussaue | Burgsilhouette mit roten Bannern | #200000, #600000, Gold #a06020 [gH] |
| B8 | `kopfband_zwergisch` | links ein in den Fels geschlagenes Tor mit goldenem Schmiedeglühen, Rauch aus Schächten; rechts ruhige Schneeberge | Felstor mit Glutlicht | #202020, #000000, #604020, #a08040 [gH] |
| B8 | `kopfband_elfisch` | links die Turmstadt Silberlaub auf hohen Bäumen und weißen Plattformen; Sternenlicht durch Nebel; rechts ruhiger Wald | schlanke Türme in Baumkronen | #101030, #103050, #f0f0f0 [gH]; Stil-Gold #b09070 (Meshy) [gC] |
| B8 | `kopfband_trolle` | links die klobige Basaltfeste mit glühenden schmalen Fenstern, davor der Fels mit Faustabdruck; rechts dunkle Berge | Festungsblock mit Glutfenstern | #101010, #301010, #701010, #b03030 [gH/gC] (D-c) |
| B8 | `kopfband_ghule` | links die weiße Zitadelle auf versteinerten Bäumen, Rippentor, grüne Feuer, Schilfnachen; rechts Moor im Nebel | helle Zitadelle vor dunklem Moor, grüne Lichtpunkte | #000000, #402040, #402060 [gH] · Nebel #305050, #103030 [gC] |
| B8 | `kopfband_gnome` | links die treibende Insel mit Werkstätten, Winden, Zahnrädern und Seilbrücken; rechts Limbusnebel | Insel-Silhouette mit Seilbrücken | **offen (D11):** Marineblau #103050 und Grau #505050 [gH] **oder** Eisblau (HEX UNBEKANNT) · Messing #b09050, #d0b070 [gC] |

**Prompts** (alle beginnen mit `Painted fantasy banner landscape, aspect 4508:868, full bleed, opaque:`):

| Kennung | Prompt-Rest | Negativ |
|---|---|---|
| menschlich | `on the left a castle of timber, clay and river stone with deep red and gold banners at a shallow ford, a silver-shimmering brook, small fishing boats, moonlit evening; calm open river meadow on the right; key content in the middle ninety percent of the height.` | `N, transparency, coat of arms, large figures` |
| zwergisch | `on the left a fortress gate carved into grey rock with a golden forge glow inside, smoke from mine shafts, black stone and gold accents; calm snowy mountains on the right; key content in the middle ninety percent of the height.` | `N, transparency, readable runes, coat of arms` |
| elfisch | `on the left slender towers on tall trees and white stone platforms, starlight through drifting mist, night blue, white and silver with small gold accents; calm forest on the right; key content in the middle ninety percent of the height.` | `N, transparency, coat of arms` |
| trolle | `on the left a massive black basalt fortress with narrow glowing windows, a boulder with a giant fist imprint, black and deep red with gold; calm dark mountains on the right; key content in the middle ninety percent of the height.` | `N, transparency, coat of arms` |
| ghule | `on the left a white stone citadel on a hill of petrified trees with a gate of curved ribs, eerie green fires, reed boats on black water, violet and black; calm foggy swamp on the right; key content in the middle ninety percent of the height.` | `N, transparency, corpses, coat of arms` |
| gnome | `on the left a floating island crowded with small workshops, winches and cogwheels, rope bridges to smaller islands, [navy blue | ice blue] with white and brass; calm limbo mist on the right; key content in the middle ninety percent of the height.` | `N, transparency, coat of arms` |

### B9 `weltkarte_goldrahmen`

| Feld | Inhalt |
|---|---|
| Motiv | Ein schmaler Goldrahmen um ein Quadrat, innen vollständig durchsichtig. **Band 3,75 % = 138 px** bei 3680 [gH]; 15 px bei 400 und 34 px bei 920 Anzeige [gH]. **Eckenradius 7,5 % = 276 px.** Der Radius stammt aus dem Kommentar in `gebaeude_motive.json` (30/400), **nicht am Bild gemessen**. Feine Gravur, an den Ecken ein kleines Ornament. |
| Anzeige | Bei 400 px: **geschlossenes Goldband mit runden Ecken**. / Gravur, Ornament |
| Farben | #b07010, #d09010, #f0d030, Schatten #905010 (Bestand `kachelrahmen_auswahl`) [gC] |
| Verbotenes | Füllung innen, Edelsteine, Verlauf nach innen |
| Seitenverhältnis | **1 : 1**, **3680 × 3680**, ±1 px (wird hochgerechnet) |
| Alpha-Satz | Der Mittelpunkt hat Alpha 0, das Band ist deckend, auf Magenta ist innen alles Magenta; RGBA. |
| Prompt | `Ornamental aged gold frame, square, transparent background with black RGB: band 3.75 percent of the edge, rounded corners 7.5 percent radius, fine even engraving, small ornament at each corner, highlight top left, completely empty transparent interior.` |
| Negativ | `N, filled centre, gemstones, inner gradient` |

### B10 `kachelrahmen_ruhe`

| Feld | Inhalt |
|---|---|
| Motiv | Ein matter Bronzerahmen um ein Quadrat, mit kleinen **Eckverstärkungen, die nach außen über die Kante stehen** (wie im Bestand [gC], siehe unten). **Band 12,5 % = 32 px** bei 256 [gH]. Volle Deckkraft in der Datei; der Code legt 35 % darüber. |
| Eckenradius | **UNBEKANNT am Bestand.** Eine Kreisanpassung an die Außenkante gelingt nicht, weil die Eckverstärkungen bis an die Bildkante reichen (Profil: Kante bei x = 2, an den Ecken x = 0 [gC]). **[V]:** Außenradius **18,75 % = 48 px** (1,5 × Band). Dann bleibt innen eine sichtbar gerundete Öffnung von 6,25 % = 16 px. |
| Anzeige | Bei 57 px (Band ≈ 7 px): **geschlossenes Bronzequadrat**. / Verstärkungen |
| Farben | #705030, #907050, #d0b070 [gC] |
| Verbotenes | Füllung, Glanzpunkte, vorab eingebaute Transparenz |
| Seitenverhältnis | **1 : 1**, **256 × 256**, 0 px |
| Alpha-Satz | Mitte Alpha 0, Band Alpha 255 (nicht 35 %), RGBA. |
| Prompt | `Matte bronze square tile frame, transparent background with black RGB: band 12.5 percent of the edge, rounded corners about 19 percent radius, small corner reinforcements protruding slightly, worn metal, even light, fully opaque metal, empty transparent interior.` |
| Negativ | `N, filled centre, shine spots, glow, semi-transparent metal` |

### B10 `kachelrahmen_auswahl`

| Feld | Inhalt |
|---|---|
| Motiv | **Dieselbe Form** wie Ruhe, **Band 15,6 % = 40 px** bei 256 [gH]; der Mehrbetrag ist das innere Glühen. Hell poliertes Gold. |
| Eckenradius | **UNBEKANNT**, aus demselben Grund wie bei Ruhe. **[V]:** wie Ruhe, also 48 px außen, damit beide Rahmen deckungsgleich bleiben. |
| Anzeige | Bei 57 px: **deutlich heller und warm leuchtend gegenüber Ruhe**. / Glanzpunkte |
| Farben | #d09010, #d07010, #f09010, #f0d030 [gC] |
| Verbotenes | andere Form oder anderer Radius als Ruhe, Füllung |
| Seitenverhältnis | **1 : 1**, **256 × 256**, 0 px |
| Alpha-Satz | Mitte Alpha 0, das Glühen nach innen halbtransparent auslaufend, RGBA. |
| Prompt | `Bright polished gold square tile frame, same shape and corner radius as the matte bronze frame, transparent background with black RGB: band 15.6 percent including a warm inner glow, highlight top left, empty transparent interior.` |
| Negativ | `N, filled centre, different shape` |

### B12 `leiste_mitte`

| Feld | Inhalt |
|---|---|
| Motiv | Dunkles ochsenblutrotes Leder mit feiner Narbung, unten eine dezente Naht. **Waagerecht nahtlos.** Kein Detail größer als 24 px. |
| Anzeige | Bei 64 × 34: **gleichmäßig dunkle Fläche ohne sichtbare Wiederholung**. / Narbung |
| Farben | Mittel #1a0a09, kein Pixel heller als #3e1c1a (Handbuch, T08) |
| Verbotenes | helle Stellen, Verlauf über die Breite, Symbole |
| Seitenverhältnis | **256 : 136 = 32 : 17**, genau 256 × 136, 0 px |
| Alpha-Satz | RGBA (Farbtyp 6) ist Vorschrift. Inhaltlich darf das Leder überall deckend sein; die linke und die rechte Pixelspalte sind farbgleich (±6 je Kanal, T08). |
| Prompt | `Seamless horizontally tileable strip texture, aspect 256:136: very dark oxblood leather, faint grain, subtle stitched seam along the bottom, extremely low contrast, left and right edges match exactly.` |
| Negativ | `N, bright spots, gradient across, ornaments, symbols` |

### B12 `leiste_ende_links`

| Feld | Inhalt |
|---|---|
| Motiv | Eine vergoldete Metallkappe **links**. Rechts läuft das Leder in Höhe und Farbe passend zur Mitte bis an die Kante. |
| Anzeige | Bei 16 × 34: **Kante und Goldkappe**. / Nieten |
| Farben | Leder #1a0a09; Gold #b8862e (Handbuch) und #d09010 [gC] |
| Verbotenes | Ornamente im Lederteil |
| Seitenverhältnis | **64 : 136 = 8 : 17**, genau 64 × 136, 0 px. **Nicht 64 : 34**, siehe D-a. |
| Alpha-Satz | Links von der Kappe Alpha 0, die rechte Pixelspalte deckend und farbgleich mit der linken Spalte der Mitte; RGBA. |
| Prompt | `End cap for a dark leather strip, aspect 64:136, transparent background with black RGB: aged gold metal clasp on the left closing very dark oxblood leather that runs to the right edge matching the tiled strip, highlight top left.` |
| Negativ | `N, ornaments on leather, rivets` |

### B12 `leiste_ende_rechts`

| Feld | Inhalt |
|---|---|
| Motiv | Spiegelbild von `ende_links`; darf gespiegelt geliefert werden. |
| Anzeige / Farben / Verbotenes | wie `ende_links` |
| Seitenverhältnis | **8 : 17**, 64 × 136, 0 px |
| Alpha-Satz | Rechts von der Kappe Alpha 0, die linke Pixelspalte deckend; RGBA. |
| Prompt | `Mirror image of the left end cap, aspect 64:136, transparent background with black RGB: aged gold clasp on the right closing very dark oxblood leather that runs to the left edge.` |
| Negativ | `N, ornaments on leather, rivets` |

### B13 `marktplatz_kennzeichen`

| Feld | Inhalt |
|---|---|
| Motiv | Chris' Marktstand: rot-weiß gestreiftes Sonnendach, Fässer, Säcke und Kisten, ein Banner mit Beutelzeichen, Laternenlicht. Deckend, bis an den Rand. **Goldrahmen offen (D8).** |
| Anzeige | Bei 96 px: **rot-weiß gestreiftes Dach**. / Waren |
| Farben | Bild #101010, #301010, #503010, #703010, #905030, #b07030 [gC]. **Bestandsrahmen:** außen etwa 3 px (≈ 3 % von 96), Gold #b8a270, Lichtkante #eee6b6, dunkle Seite #a27239 [gC, an Rand-Pixeln gemessen] |
| Verbotenes | Alphakanal, Händlergesicht, Schrift auf dem Banner |
| Seitenverhältnis | **1 : 1**, **384 × 384**, 0 px |
| Alpha-Satz | RGB (Farbtyp 2), kein leerer Rand, auf Magenta bleibt nichts Magenta. |
| Prompt | `Painted fantasy market stall emblem, square, opaque, full bleed: red and white striped awning, barrels, sacks and crates, hanging banner with a coin-pouch sign, warm lantern light, dark surroundings[, thin rounded gold border].` |
| Negativ | `N` (ohne „frame“, wenn D8 = Rahmen bleibt), `transparency, merchant face, embossed coins` |

---

## B – Seitenverhältnis und Toleranz (Übersicht)

| Dateien | Verhältnis | Sollmaße | Toleranz | Begründung |
|---|---|---|---|---|
| B1, B2 ×2, B10 ×2, B13 | 1 : 1 | 176 / 256 / 384 | **0 px** | Kleine Dateien werden ohnehin auf das **genaue** Maß verkleinert. Eine Abweichung zeigt an, dass die Vorgabe nicht befolgt wurde, und nicht eine Rundung. |
| B9 | 1 : 1 | 3680 × 3680 | ±1 px | wird hochgerechnet (F-106), Rundung möglich |
| B5 ×2 | 64 : 45 | 4096 × 2880 | ±1 px (Höhe zur Breite) | wird hochgerechnet |
| B8 ×6 | 4508 : 868 | 4508 × 868 | ±1 px (Höhe zur Breite) | wird hochgerechnet |
| B12 Mitte | 256 : 136 = 32 : 17 | 256 × 136 | 0 px | genaue Verkleinerung, kachelbar |
| B12 Enden ×2 | **64 : 136 = 8 : 17** | 64 × 136 | 0 px | wie oben |

**Dein Vorschlag ±1 px überall** ist für die hochgerechneten Dateien richtig. Bei den kleinen würde er eine 177 × 176 große Datei durchlassen, die beim Einpassen eine Spalte verliert. Die Entscheidung bleibt bei dir.

---

## C – Alpha-Test (Zusammenfassung)

| Vorgabe | Dateien | Woran man es erkennt |
|---|---|---|
| `alpha: true` = Farbtyp 6 | B1, B2 ×2, B9, B10 ×2, B12 ×3 | Die Dateiinfo sagt RGBA, und auf Magenta gelegt ist alles außerhalb des Motivs Magenta, **ohne hellen Saum**. |
| `alpha: false` = Farbtyp 2 bzw. JPG | B5 ×2 (JPG), B8 ×6, B13 (PNG) | Die Dateiinfo sagt RGB, und auf Magenta gelegt bleibt **nichts** Magenta; alle Ränder sind bemalt. |

---

## D – offen, mit Empfehlung (Daniel entscheidet)

| Punkt | Lage | Empfehlung | Umentscheiden in einer Zeile |
|---|---|---|---|
| **D8** Goldrahmen im Marktplatz-Kennzeichen (B13) | Der Bestand hat einen Rahmen von etwa 3 px aus Gold #b8a270 / #a27239 [gC]. Zum Vergleich das Silberbach-Gold #a06020 [gH]. | **offen, Empfehlung: Rahmen bleibt** (Teil von Chris' Zeichnung, passt zum Auswahlrahmen) | Prompt: „thin rounded gold border“ streichen; Negativ: „frame“ wieder aufnehmen |
| **D11** Farbe Kopfband Flickwerk (B8 Gnome) | Wappen `wappen_05` Marineblau #103050 [gH]; Burg `burg_06` „eisblau / weiß“ [gH], **HEX UNBEKANNT**; F-105 nennt Eisblau / Weiß / Messing | **offen, Empfehlung: Marineblau #103050** der Wappendatei | im Gnome-Prompt `navy blue` durch `ice blue` ersetzen |

### Drei Widersprüche, die ich zusätzlich melde

| # | Fundstelle | Widerspruch | Vorschlag |
|---|---|---|---|
| **D-a** | Auftrag Nr. 21, Abschnitt 2B (Zeile 116): „64:34 bei den beiden Leisten-Endstücken“ | 64 : 34 ist das Anzeigeverhältnis der **Mitte**. Die Enden sind 16 × 34 bzw. 64 × 136, also **8 : 17** [r]. Mit 64 : 34 würde die Wache jedes richtige Endstück ablehnen. | Ende = 8 : 17 |
| **D-b** | Auftrag Nr. 21, Abschnitt 3 (Zeilen 142–149) | Die Zuordnung Haus → Wappen ist vertauscht (Abschnitt 0 oben) | berichtigen nach 13.11. |
| **D-c** | Auftrag 0.2 („`burg_05` grün passt zu Schattenfaust“) gegen Prüfung Nr. 19, Abschnitt 5 („Hausfarbe folgt dem **Wappen**“, Regel 05.11.) | Bei **zwei** Häusern widersprechen sich Burg und Wappen: Schattenfaust (Burg grün, Wappen rot) und Flickwerk (Burg eisblau, Wappen marineblau). „Farbe folgt dem Bild“ (Auftrag Zeile 152) sagt nicht, **welchem** Bild. | Eine Regel für beide Fälle. Nach der Regel vom 05.11. folgt die Farbe dem **Wappen**; dann sind Trolle Rot / Schwarz und Gnome Marineblau. **Daniel bestätigt das bitte einmal für beide.** |

---

## Annahmen

| # | Annahme |
|---|---|
| A1 | Bildmodelle liefern höchstens etwa 2048 px; B5, B8 und B9 werden hochgerechnet (F-106, Vermerk nötig). |
| A2 | Der Code legt beim Ruherahmen 35 % Deckkraft darüber (Liste, `zweck`); die Datei selbst ist deshalb voll deckend. |
| A3 | Der Eckenradius 7,5 % des Weltkartenrahmens stimmt mit dem Bild überein. Er steht nur im Kommentar und wurde nicht gemessen. |
| A4 | Der Vorschlag für den Radius der Kachelrahmen (1,5 × Band) ist eine Gestaltungsannahme und keine Messung. |

---

## Zusatzinformationen (nicht beauftragt)

> Hinweise, keine Anweisungen.

**Z1 Eckenradius am Bild messen, ohne Kreisanpassung.** Am Bestand stören die Eckverstärkungen. Messbar ist aber die **Innenöffnung**: das erste deckende Pixel entlang der Diagonalen von der Bildmitte zur Ecke. Daraus ergibt sich der Innenradius, und Innenradius + Band ergibt den Außenradius. Das gilt auch für `kachelrahmen_chris.png` (A3).

**Z2 Die Wache sollte die Kanten der Leistenstücke prüfen.** Linke Spalte der Mitte gegen rechte Spalte der Mitte (Nahtlosigkeit) und rechte Spalte von `ende_links` gegen linke Spalte der Mitte, je ≤ 6 pro Kanal (T08 D1). Das ist reine Pixelrechnung und braucht kein Auge.

**Z3 Tests ohne Pillow.** `bildpaket_pruefen.py` liest PNG- und JPEG-Kopf ohne Pillow. Die Prüfungen aus Z2 und der Magenta-Test brauchen dagegen Pixel. Sie gehören deshalb in eine **zweite** Wache mit Pillow. Die erste bleibt so, wie sie ist.

---

Ende der Antwort auf Auftrag Nr. 21.
