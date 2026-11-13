# ANTWORT AUF AUFTRAG NR. 19: Die Bildliste für den Dezember (Design-Briefs)

| | |
|---|---|
| **Auftrag von** | Hermes Agent „Weltenfresser“, `deepseek-v4-flash`, Top-Koordinator des Projekts |
| **Antwort von** | Claude Opus 5.5 (Thinking: hoch) |
| **Meine Rolle** | Ich arbeite zu: Ich schreibe die 16 Bildaufträge so, dass man sie ohne Rückfrage an ein Bildmodell geben kann. Weltenfresser prüft, bündelt und vergibt sie, und Daniel entscheidet. |
| **Antwort auf** | AUFTRAG NR. 19 — Die Bildliste für den Dezember (`AUFTRAG_CLAUDE_BILDAUFTRAG_NR19.txt`) mit den Anlagen `BILDBEDARF_ENTSCHEIDUNGEN_20261113.txt`, `CHRONIK_DER_WELT_20261104.txt` (Teil 3 und Teil 5 gelesen), `elfen_wappen.png` (gesehen) und `BILDBESTAND_MESSUNG_20261113.txt` |
| **Es gilt** | F-99 bis F-104. Insbesondere **4 × überall (F-101)**; mein Z2 aus Nr. 18 ist damit überstimmt. |

**Kennzeichnung:** [g] gemessen oder gelesen · [r] gerechnet · [a] angenommen · UNBEKANNT.

---

## Teil A – Stilblatt (gilt für alle 16)

| Regel | Festlegung |
|---|---|
| **Stil** | Gemalte digitale Illustration, „stylized realism“, episch und ruhig, so wie die Meshy-Waldelfen (F-103): klare Silhouette, hoher Materialdetailgrad, **Gold als Akzent**, nie als Fläche. Keine schwarzen Konturen, kein 3D-Render, keine Fotorealistik, kein Cartoon. |
| **Licht und Nebel** | Warmes Gegenlicht, kühle Schatten, **Nebel in Bodennähe** (der Nebelsee ist die Grundstimmung). Lichtquelle oben links, bei allen Bildern gleich. |
| **Schrift** | In **keinem** Bild Schrift, Zahlen, Runen als lesbare Zeichen, Logos oder Wasserzeichen. |
| **Anlage** | Kartenbilder (B1, B2) und Rahmen (B9, B10, B13) **quadratisch**, Motiv mittig, Rest durchsichtig. Flächen (B5, B8, B12) im angegebenen Seitenverhältnis. |
| **Format** | Freigestellte Bilder als **PNG RGBA**. Szenen ohne Transparenz als **JPG q92 RGB**, wie die vorhandenen Panoramen. |
| **Alpha** | Saubere Kante ohne grauen oder weißen Saum. Halbtransparenz nur an Nebel und Glanz. |
| **Größe** | Dateigröße = **4 × Anzeigegröße** (F-101). Erzeugt wird in der größten Auflösung, die das Bildmodell kann; verkleinert wird erst danach (siehe F2). |
| **Farben der Häuser** | Silberbach Rot / Gold (Grau) · Hammerhall Grau / Schwarz / Gold · Sternenwacht Weiß / Silber / Nachtblau · Schattenfaust Rot / Schwarz / Gold · Knochenmoor Violett / Schwarz (Gold-Akzente), grüne Feuer · Flickwerk siehe F1 (Widerspruch in den Quellen) |
| **Verbote** | Teil E, in jedem Prompt als Negativ-Block |

**Negativ-Block (an jeden Prompt anhängen):**

```
no text, no letters, no numbers, no logo, no watermark, no wolves, no helmet, no crest, no human faces in close-up, no portraits, no real persons, no blood, no cartoon, no emoji style, no photorealism, no 3D render, no black outlines
```

---

## Teil B – Die 16 Einzelaufträge

**Hinweis zu allen Prompts:** Der Negativ-Block aus Teil A wird **angehängt**. Er ist in der Wortzahl (40–80) nicht mitgezählt.

### B1 `B1_ruine`

| Feld | Inhalt |
|---|---|
| Zweck | Feld eines besiegten Drachen auf der Weltkarte; ersetzt den Platzhalter aus Ellipsen |
| Ansicht / Code | Portal, Weltkarte; `src/main.py:16480` (Zeichenweg der Drachenfiguren), `data/drachen.json` (`ruine_bild` leer, `ruine_platzhalter` true) [g] |
| Anzeigegröße | 19–44 px (Feld × 0,95) [g/r] |
| Dateigröße bei 4× | **176 × 176** [r] |
| Format | PNG RGBA |
| Anzahl | 1 |
| Was zu sehen sein muss | Die eingestürzte steinerne Höhle eines Drachen: ein gebrochener Torbogen über einer leeren Hortmulde, daneben zwei oder drei abgeworfene große Schuppen. Von schräg oben, wie die Burgen. |
| Was NICHT zu sehen sein darf | ein Drache, Gold oder Schätze im Hort (der Hort ist leer, `drachen.json`), Knochen oder Blut, Figuren |
| Prompt | `Painted digital illustration, stylized realism, isometric three-quarter top view of a collapsed stone dragon lair: a broken rock arch over an empty hoard hollow, two large shed dragon scales lying beside it, low ground mist, warm rim light from top left, cool shadows, clear readable silhouette for a small map icon, centered on a square transparent background, gold only as tiny accents.` |

### B2a `B2_drache_gruen` (Tardas der Grüne)

| Feld | Inhalt |
|---|---|
| Zweck | Figur von Tardas auf der Weltkarte; ersetzt `drache_blau.png` (Name und Farbe passen heute nicht zusammen) |
| Ansicht / Code | Portal, Weltkarte; `src/main.py:16480`, `data/drachen.json:93` [g] |
| Anzeigegröße | 19–44 px |
| Dateigröße bei 4× | **176 × 176** |
| Format | PNG RGBA |
| Anzahl | 1 |
| Was zu sehen sein muss | Ein ruhender Drache in der Farbe von **nassem Moos** mit glänzenden **goldenen Augen**. Der Körper windet sich wie eine Ranke, die Schuppen sind leicht gezackt wie geschnittene Blätter (Chronik, Teil 3). Gleiche Haltung und gleicher Bildausschnitt wie `drache_weiss.png`. |
| Was NICHT zu sehen sein darf | Feuer oder Kampfszene, Reiter, Hintergrund, blaue oder violette Töne |
| Prompt | `Painted digital illustration, stylized realism, a resting dragon the colour of wet moss with glossy golden eyes, body coiled like a winding vine, scales slightly jagged like cut leaves, same pose and framing as the reference white dragon, full body visible, three-quarter top view, warm rim light from top left, cool green shadows, clear silhouette readable at icon size, centered on a square transparent background.` |

### B2b `B2_drache_rot` (Salmur der Rote)

| Feld | Inhalt |
|---|---|
| Zweck | Figur von Salmur auf der Weltkarte; ersetzt `drache_lila.png` |
| Ansicht / Code | Portal, Weltkarte; `src/main.py:16480`, `data/drachen.json:138` [g] |
| Anzeigegröße | 19–44 px |
| Dateigröße bei 4× | **176 × 176** |
| Format | PNG RGBA |
| Anzahl | 1 |
| Was zu sehen sein muss | Ein ruhender roter Drache mit **breiten Flügeln wie verbranntes Leder** und Schuppen, die wie in der Dämmerung von innen glühen (Chronik, Teil 3). Gleiche Haltung wie `drache_weiss.png`. |
| Was NICHT zu sehen sein darf | ausgestoßenes Feuer, Opfer, Blut, violette Töne |
| Prompt | `Painted digital illustration, stylized realism, a resting red dragon with broad wings like scorched leather, scales faintly glowing from within like embers at dusk, heavy oppressive presence, same pose and framing as the reference white dragon, full body visible, three-quarter top view, warm rim light from top left, cool dark shadows, clear silhouette readable at icon size, centered on a square transparent background.` |

### B5a `B5_startbild_anmelden`

| Feld | Inhalt |
|---|---|
| Zweck | Hintergrund des Anmeldetors. Darauf liegen das Logo (460 px breit) und das Formular. |
| Ansicht / Code | Tor; `src/main.py:8851` (`startbild_photo("anmelden", 1024, 720, 38.0)`), Cover-Beschnitt mittig (`_cover`) [g] |
| Anzeigegröße | 1024 × 720 (der Code dunkelt um 38 % ab) [g] |
| Dateigröße bei 4× | **4096 × 2880** [r] |
| Format | JPG q92 RGB |
| Anzahl | 1 |
| Was zu sehen sein muss | Die zersprungene Welt: sechs schwebende Landbruchstücke im Nebel des Limbus, auf einigen Wald, Berg oder Moor, dazwischen leuchtende Portale. **Die Mitte (etwa 40 % der Breite) bleibt ruhig und dunkler**, dort liegen Logo und Formular. |
| Was NICHT zu sehen sein darf | Schrift, Figuren im Vordergrund, ein Drache als Hauptmotiv, ein Sonnenball in der Mitte |
| Prompt | `Epic painted digital illustration, stylized realism, wide panorama of a shattered world: six floating land fragments drifting in a sea of glowing mist, forests, mountains and a misty swamp on them, faint luminous portals between the islands, warm backlight from top left, cool blue shadows, the central forty percent of the image kept calm, darker and empty for a logo and a login panel, aspect ratio 64:45.` |

### B5b `B5_startbild_laden`

| Feld | Inhalt |
|---|---|
| Zweck | Hintergrund des Ladebilds |
| Ansicht / Code | `src/main.py:19103` (`startbild_photo("laden", 1024, 720, 30.0)`) [g] |
| Anzeigegröße | 1024 × 720 (der Code dunkelt um 30 % ab) |
| Dateigröße bei 4× | **4096 × 2880** |
| Format | JPG q92 RGB |
| Anzahl | 1 |
| Was zu sehen sein muss | Morgen an einem Nebelsee: eine kleine Siedlung mit Holzfäller, Feldern und einem Steg erwacht, Rauch aus den Schornsteinen. Ganz klein im Mittelgrund arbeitende Gestalten **von hinten**. Unteres Drittel ruhig (Ladebalken). |
| Was NICHT zu sehen sein darf | Gesichter, Schrift, Kampf |
| Prompt | `Epic painted digital illustration, stylized realism, dawn over a misty lake, a small settlement waking up with a woodcutter hut, fields, a wooden jetty and smoke from chimneys, a few tiny workers seen from behind in the middle distance, warm golden backlight, cool blue mist on the water, lower third of the image calm and soft for a loading bar, aspect ratio 64:45.` |

### B8 `B8_kopfband_<haus>` (6 Stück; die Motive stehen in Teil C)

| Feld | Inhalt |
|---|---|
| Zweck | Kopfband der Portalansicht, eines je Volk. Heute gibt es nur eines, mit Ghule-Motiv. |
| Ansicht / Code | Portal; `src/main.py:3760` (Datei), `3764` (`PORTAL_KOPFBAND_MASSE = (780, 150)`), `14257–14275` (Breite = Inhaltsbreite, Höhe gedeckelt auf 200, dann mittig beschnitten) [g] |
| Anzeigegröße | Breite bis 1127, Höhe ≤ 200 [g] |
| Dateigröße bei 4× | **4508 × 868** [r]: 4 × 1127 im heutigen Seitenverhältnis 780 : 150 = 5,2 : 1. Bei 1127 px Breite schneidet der Code die natürliche Höhe von 217 auf 200 zu. Die Tabelle im Auftrag nennt 4508 × 800; das wäre ein anderes Verhältnis (5,635 : 1), und dafür müsste die Konstante geändert werden (F3). |
| Format | JPG q92 RGB |
| Anzahl | 6 |
| Was zu sehen sein muss | siehe Teil C. **Gemeinsam:** ein ruhiger Dorfstreifen, der Herrschaftssitz im rechten Drittel, **alles Wichtige im mittleren 90 % der Höhe**, weil der Code oben und unten bis zu 4 % abschneidet [r: 17 von 217 px]. |
| Was NICHT zu sehen sein darf | Schrift, Wappen als Bild im Bild, Figuren groß im Vordergrund |
| Prompt | je Haus in Teil C |

### B9 `B9_weltkarte_goldrahmen`

| Feld | Inhalt |
|---|---|
| Zweck | Goldrahmen um die Weltkarte |
| Ansicht / Code | `data/gebaeude_motive.json:212` (`weltkarte`), heute `kachelrahmen_chris.png` 400 × 400 [g] |
| Anzeigegröße | 400–920 px (20 Felder × 20 bis 46 px) [r] |
| Dateigröße bei 4× | **3680 × 3680** [r] |
| Format | PNG RGBA, Innenfläche **vollständig durchsichtig** |
| Anzahl | 1 |
| Was zu sehen sein muss | Ein schmaler Goldrahmen: Band **3,35 % der Kante = 123 px**, Eckenradius **7,5 % = 276 px** [r, aus `gebaeude_motive.json:215`]. Feine, gleichmäßige Gravur, an den vier Ecken je ein kleines Ornament. |
| Was NICHT zu sehen sein darf | Bild im Inneren, Schrift, Wappen, große Edelsteine, Verlauf nach innen |
| Prompt | `Painted digital illustration, a thin ornamental gold frame for a square game map, band width about 3.4 percent of the edge, rounded corners about 7.5 percent radius, finely engraved even pattern along the band, a small restrained ornament at each corner, aged gold with warm highlights from top left, completely transparent empty interior, square, centered, clean alpha edges.` |

### B10a `B10_kachelrahmen_ruhe`

| Feld | Inhalt |
|---|---|
| Zweck | Rahmen auf jedem Feld der Siedlungskarte, gedämpft |
| Ansicht / Code | `src/main.py:9177` (`_lade_kachelrahmen`, `px=64`), `data/gebaeude_motive.json:207`; der Code senkt die Deckkraft zusätzlich ab (`RAHMEN_DECKRAFT`) [g] |
| Anzeigegröße | 57–64 px [g] |
| Dateigröße bei 4× | **256 × 256** |
| Format | PNG RGBA |
| Anzahl | 1 |
| Was zu sehen sein muss | Eine dünne Bronzelinie am Rand des Quadrats mit leicht gerundeten Ecken. Bei 4× etwa 8 px stark, ergibt am Schirm etwa 2 px [r]. |
| Was NICHT zu sehen sein darf | Füllung, Ornamente, die bei 64 px Rauschen ergeben, Glanzpunkte |
| Prompt | `Minimal painted game UI tile frame, a thin muted bronze line along the edge of a square with slightly rounded corners, line about three percent of the tile width, subtle worn metal texture, soft even light, completely transparent interior, no ornaments, square, clean alpha edges, designed to stay calm and readable at 64 pixels.` |

### B10b `B10_kachelrahmen_auswahl`

| Feld | Inhalt |
|---|---|
| Zweck | Rahmen des gewählten Feldes, kräftig |
| Ansicht / Code | `data/gebaeude_motive.json:208`; Deckkraft `AUSWAHL_DECKRAFT` [g] |
| Anzeigegröße | 57–64 px |
| Dateigröße bei 4× | **256 × 256** |
| Format | PNG RGBA |
| Anzahl | 1 |
| Was zu sehen sein muss | Dieselbe Form wie B10a, aber **doppelt so stark** (etwa 16 px bei 4×), helles Gold mit schwachem Leuchten nach außen. |
| Was NICHT zu sehen sein darf | Füllung, andere Form als B10a |
| Prompt | `Painted game UI selection frame matching a thin tile frame, same square shape with slightly rounded corners but twice as thick, bright polished gold with a faint warm outer glow, highlight from top left, completely transparent interior, square, clean alpha edges, clearly stronger than the resting frame and readable at 64 pixels.` |

### B12 `B12_leiste_mitte`, `B12_leiste_ende_links`, `B12_leiste_ende_rechts`

| Feld | Inhalt |
|---|---|
| Zweck | Ressourcenleiste. Heute ist sie ohne Bild gebaut (T08 D3); das Band wird **gekachelt, nie gedehnt**. |
| Ansicht / Code | `data/ressourcenleiste.json` (Höhe 34), `src/main.py:9853` (`_leiste_kachel_bild`) [g] |
| Anzeigegröße | Mitte **64 × 34**, Enden **16 × 34** [g, T08] |
| Dateigröße bei 4× | Mitte **256 × 136**, Enden **64 × 136** |
| Format | PNG RGBA |
| Anzahl | 3 (das rechte Ende als Spiegelung des linken erlaubt) |
| Was zu sehen sein muss | Dunkles ochsenblutrotes Leder (Mittelwert **#1a0a09**), feine Narbung, unten eine dezente Naht. Die Mitte ist **waagerecht nahtlos**. Die Enden zeigen eine kleine vergoldete Metallkappe. Kein Detail größer als 24 px bei 4× (= 6 px am Schirm). |
| Was NICHT zu sehen sein darf | helle Stellen (kein Pixel heller als #3e1c1a, T08 D1), Symbole, Verlauf über die Breite, Ornamente in der Mitte |
| Prompt Mitte | `Seamless horizontally tileable game UI strip texture, very dark oxblood leather with faint embossed grain and a subtle stitched seam along the bottom, average colour very dark brown, extremely low contrast, soft warm light, no ornaments, no gradient across the strip, left and right edges match perfectly, aspect ratio 256:136.` |
| Prompt Enden | `Small end cap for a dark leather game UI strip, a gilded aged-gold metal clasp closing the end of very dark oxblood leather with faint grain, warm highlight from top left, low contrast, matching the tileable middle strip exactly in height and colour, transparent background outside the cap, aspect ratio 64:136.` |

### B13 `B13_marktplatz_kennzeichen`

| Feld | Inhalt |
|---|---|
| Zweck | Kennzeichen der Marktplatz-Ansicht |
| Ansicht / Code | `src/main.py:3763` (Datei), `9189` (`_kennzeichen_bild`, 1:1 ohne Skalierung) [g] |
| Anzeigegröße | 96 × 96 [g] |
| Dateigröße bei 4× | **384 × 384**. **Achtung:** Der Code lädt das Bild ohne Pillow in Originalgröße; für 4× muss er verkleinern (F3). |
| Format | PNG RGBA (heute RGB ohne Alpha) |
| Anzahl | 1 |
| Was zu sehen sein muss | Ein einzelner Marktstand mit gestreiftem Sonnendach, Kisten mit Waren und einer Balkenwaage, schräg von vorn, freigestellt. |
| Was NICHT zu sehen sein darf | Händlerfigur mit Gesicht, Münzen mit Prägung, Schrift auf Schildern |
| Prompt | `Painted digital illustration, stylized realism, a single medieval market stall with a striped canvas awning, wooden crates of goods and a balance scale on the counter, three-quarter front view, warm light from top left, cool shadows, clear silhouette as a small UI emblem, centered on a square transparent background, gold only as small accents.` |

---

## Teil C – Die sechs Kopfbänder (B8)

Gemeinsam für alle sechs:
- **4508 × 868**, JPG q92, Seitenverhältnis 5,2 : 1.
- Sitz im rechten Drittel, links ruhiges Land, alles Wichtige im mittleren 90 % der Höhe.
- Negativ-Block aus Teil A anhängen.

**Quellen:** Motive und Sitze aus der **Chronik, Teil 5** [g]. Farben aus der Chronik; wo `bot_wappen.json` (F-78) abweicht, steht es in F1.

| Haus | Volk / Welt | Farben | Wappenmotiv (Chronik) | Herrschaftssitz (Chronik) | Auf dem Band |
|---|---|---|---|---|---|
| **Silberbach** | Menschen / Midgard | Rot, Gold | goldene Krone über rotem Banner, goldener Lorbeer, roter Grund | Burg aus Holz, Lehm und Flussstein an einer Furt | Der im Mondlicht schimmernde Silberbach mit Furt, Fischerboote, die Burg mit roten Bannern rechts |
| **Hammerhall** | Zwerge / Armageddon | Grau, Schwarz, Gold | Schmiedehammer über schneebedeckten Bergen, Knotenmuster, schwarzer Grund | Tiefenfeste, in einen Berg geschlagen, Tore mit Runen | Schneeberge, rechts ein Felsportal mit goldenem Schmiedeglühen, Rauch aus Schächten |
| **Sternenwacht** | Elfen / Valhalla | Weiß, Silber, Nachtblau | silberne Mondsichel mit achtzackigem goldenem Stern, kleine Sterne, Wolken, nachtblauer Grund | Turmstadt Silberlaub auf hohen Bäumen und Steinplattformen, Glimmerfenster, Dachgärten | Abenddämmerung, schlanke Türme in Baumkronen, Sternenlicht durch Nebel |
| **Schattenfaust** | Trolle / Utgard | Rot, Schwarz, Gold | aufgerichteter roter Drache mit goldenen Krallen, Flügelspitzen und Augen, schwarzer Grund | klobige Felsfeste aus Basalt und Geröll, dicke Mauern, schmale Fenster | Dunkle Berge, rechts die Basaltfeste, davor der Fels mit dem Faustabdruck, Glut aus den Fenstern |
| **Knochenmoor** | Ghule / Ragnarök | Violett, Schwarz, Gold-Akzente | Rabe auf einem Ast vor einer Mondsichel, gotisch gerahmt | Sumpfzitadelle auf einem Hügel aus versteinerten Bäumen, weiße Mauern, Tor aus gebogenen Rippen | Moor im Nebel, Schilfnachen, rechts die Zitadelle, **grüne Feuer** in den Hütten, düster |
| **Flickwerk** | Gnome / Limbus | **F1:** Chronik Grau/Schwarz/Gold, F-78 Eisblau/Weiß/Messing | steinerne Zinnenburg vor Bergen, goldener Rahmen | schwimmende Insel mit Werkstätten, Winden, Seilbrücken, Gärten | Treibende Insel im Limbusnebel, Seilbrücken zu kleinen Nachbarinseln, Zahnräder und Winden |

**Prompts** (je etwa 60–75 Wörter, ohne Negativ-Block):

**Silberbach**
```
Epic painted digital illustration, stylized realism, very wide calm banner landscape, aspect ratio 5.2 to 1: a silver-shimmering brook with a shallow ford under moonlit evening sky, small fishing boats, a modest castle of timber, clay and river stone with red and gold banners on the right third, soft mist over the water, warm backlight from top left, cool blue shadows, all important content within the middle ninety percent of the height.
```

**Hammerhall**
```
Epic painted digital illustration, stylized realism, very wide calm banner landscape, aspect ratio 5.2 to 1: snow-covered grey mountains, on the right third a fortress gate carved deep into the rock with plain rune-like engravings and a golden forge glow from within, thin smoke rising from mine shafts, black stone and gold accents, low mist in the valley, warm backlight from top left, cool shadows, important content within the middle ninety percent of the height.
```

**Sternenwacht**
```
Epic painted digital illustration, stylized realism, very wide calm banner landscape, aspect ratio 5.2 to 1: twilight over an ancient forest, on the right third a slender tower city built on tall trees and white stone platforms with glimmering mica windows and small roof gardens, starlight breaking through drifting mist, white, silver and night-blue palette with small gold accents, warm backlight from top left, important content within the middle ninety percent of the height.
```

**Schattenfaust**
```
Epic painted digital illustration, stylized realism, very wide calm banner landscape, aspect ratio 5.2 to 1: dark rugged mountains at dusk, on the right third a massive clumsy fortress of black basalt and rubble with thick walls and narrow glowing windows, in front a large boulder bearing the imprint of a giant fist, red, black and gold palette, smoke and low mist, warm ember backlight, important content within the middle ninety percent of the height.
```

**Knochenmoor**
```
Epic painted digital illustration, stylized realism, very wide gloomy banner landscape, aspect ratio 5.2 to 1: a misty swamp at night, reed boats on dark water, on the right third a citadel of white stone on a hill of petrified trees with a gate shaped from curved ribs, eerie green fires in small huts, violet and black palette with faint gold accents, thick low fog, cool moonlight, important content within the middle ninety percent of the height.
```

**Flickwerk** (Farben nach F-78; bei anderer Entscheidung in F1 nur die Farbangabe tauschen)
```
Epic painted digital illustration, stylized realism, very wide calm banner landscape, aspect ratio 5.2 to 1: a floating island drifting in glowing limbo mist, crowded with small workshops, winches, cogwheels and little gardens, rope bridges leading to smaller neighbouring islands, ice-blue, white and brass palette, warm backlight from top left, cool shadows, important content within the middle ninety percent of the height.
```

---

## Teil D – Reihenfolge und Bündel

**Grundsatz:** Erst der **Stilanker**, also ein großes Bild, das Licht, Farbe und Pinselart festlegt. Danach wird jedes weitere Bild mit dem Stilanker **und** der Meshy-Vorlage als Bildreferenz erzeugt.

| Schritt | Auftrag | Bilder | Blatt / Seitenverhältnis | Begründung |
|---|---|---|---|---|
| 1 | **B5a** Startbild Anmelden | 1 | einzeln, 64 : 45 | Stilanker: zeigt alle sechs Welten, legt Licht und Nebel fest |
| 2 | **B8** sechs Kopfbänder | 6 | **einzeln**, je 5,2 : 1 | Auf einem Blatt käme jedes Band nur auf etwa ein Sechstel der Höhe; für 4508 px Breite wäre das zu wenig [r]. Reihenfolge Silberbach → Hammerhall → Sternenwacht → Schattenfaust → Knochenmoor → Flickwerk; Flickwerk zuletzt wegen F1 |
| 3 | **B5b** Startbild Laden | 1 | einzeln, 64 : 45 | nutzt Schritt 1 als Referenz |
| 4 | **Drachenblatt:** B2a, B2b, B1 | 3 | **ein Blatt, 3 : 1**, drei Quadrate nebeneinander, mit `drache_weiss.png` als Haltungsvorlage | Gleiche Haltung, gleiches Licht, gleicher Maßstab. Geschnitten mit `tools/burgen_wappen_schneiden.py` |
| 5 | **Rahmenblatt:** B9, B10a, B10b | 3 | **ein Blatt, 3 : 1**, drei Quadrate | gleiches Gold, gleiche Gravur. B9 braucht danach die höchste Vergrößerung (F2) |
| 6 | **Leistenblatt:** B12 Mitte, Ende links, Ende rechts | 3 | **ein Blatt, etwa 4 : 1**: Mitte 256 : 136 und zwei Enden 64 : 136 in einer Zeile | gleiches Leder, gleiche Kappe; die Naht der Mitte danach prüfen (T08 D1) |
| 7 | **B13** Marktplatz | 1 | einzeln, quadratisch | Einzelstück |

**Summe:** 16 Bilder in **12 Aufträgen**: 3 Blätter mit je 3 Bildern und 9 Einzelaufträge (B5a, B5b, sechs Kopfbänder, B13). Das Kopfband für Flickwerk wartet auf F1.

---

## Teil E – Was in keinem Bild vorkommt

Steht als Negativ-Block in Teil A und gilt für alle 16:
- keine Wölfe,
- kein Helm, keine Helmzier,
- keine Schrift, keine Zahlen, kein Logo, kein Wasserzeichen,
- keine Emoji-Optik, kein Cartoon, keine Fotorealistik, kein 3D-Render,
- keine Gesichter als Hauptmotiv, keine Porträts, keine echte Person,
- kein Blut.

**Zusätzlich aus der Chronik:**
- **Wappen werden nicht als Bild im Bild gemalt.** Die Kopfbänder zeigen Farben und Sitze, nicht das Wappen.
- **Der Hort der Ruine ist leer.**

---

## Teil F – Was offen bleibt

**F1 – Farbwidersprüche zwischen Chronik und `bot_wappen.json` (F-78).** Daniel muss entscheiden:
- **Flickwerk:** Die Chronik sagt **Grau / Schwarz / Gold**, genau die Farben von Hammerhall. F-78 sagt **Eisblau / Weiß / Messing**. Zwei Häuser mit denselben Farben wären auf jedem Kopfband verwechselbar. **Empfehlung: F-78.** Daniels Regel „Geschichte und Stil folgen den Burgbildern“ ist jünger als die Chronik.
- **Schattenfaust:** Die Chronik sagt **Rot / Schwarz / Gold**. `bot_wappen.json` beschreibt `burg_05` als **Grün / Schwarz / Gold**. Das Kopfband ist nach der Chronik geschrieben, passend zum roten Drachen in `wappen_08`. **Bitte prüfen, ob die Burg dazu passt.**
- **Sternenwacht:** Chronik und F-78 sagen **Weiß / Silber / Nachtblau**. Die Meshy-Vorlage zeigt **Grün / Weiß / Gold** (Waldelfen). Nach F-103 ist Meshy die **Stilvorlage**. Ich habe die Farben deshalb aus der Chronik genommen. **Bitte bestätigen.**

**F2 – Können die Bildmodelle 4× überhaupt liefern?** 4096 × 2880, 4508 × 868 und 3680 × 3680 liegen vermutlich über dem, was ein Bildmodell direkt erzeugt; viele liefern um 1024 bis 2048 px. Was Meshy kann, ist **UNBEKANNT**.
- Ein **hochgerechnetes** Bild hat die Pixel von 4×, aber nicht die Schärfe.
- Für B5, B8 und B9 braucht es deshalb entweder ein Modell mit großer Ausgabe oder einen KI-Hochrechner.
- **Daniel entscheidet**, ob „hochgerechnet“ F-101 erfüllt.

**F3 – Drei Codestellen, die zu den neuen Dateien passen müssen** (Weltenfresser):
- `PORTAL_KOPFBAND_MASSE = (780, 150)` und **eine** feste Datei (`main.py:3760–3764`). Für sechs Bänder je Volk braucht es eine Auswahl nach Volk und die neuen Maße.
- `_kennzeichen_bild` lädt ohne Verkleinerung (`main.py:9189`). Eine 384er-Datei würde sonst 384 px groß angezeigt.
- Die Kartenbilder gehen über `_motivbild_skaliert` und werden seit F-99 eingepasst; dort ist nichts zu tun.

**F4 – B4 (Einzelansichten der Gebäude, 1142 × 1120): Ich halte sie für den Dezember nicht für nötig.** Nach der Vorlage aus Nr. 12 (A2) fällt jede Ansicht ohne Motivbild auf das Panorama des Volkes zurück, und alle sechs Panoramen existieren. Die 15 fehlenden Bilder würden die Wirkung verbessern, aber keine Ansicht ermöglichen. **Prio 3, nach den 16.**

**F5 – `drache_weiss.png` habe ich nicht gesehen.** Die Prompts B2a und B2b verlangen „gleiche Haltung wie der weiße Drache“. Das Bild muss deshalb als **Bildreferenz** mitgegeben werden.

---

## Zusammenfassung in fünf Zeilen

1. **16 Bilder in 12 Aufträgen**, jedes mit allen Feldern und einem fertigen englischen Prompt samt Negativ-Block.
2. **3 Blätter:** Drachen und Ruine, Rahmen, Leiste. Dazu 9 Einzelaufträge: zwei Startbilder, sechs Kopfbänder (Flickwerk erst nach der Farbklärung) und das Marktplatz-Kennzeichen.
3. **Zuerst das Startbild „Anmelden“ als Stilanker**, dann die sechs Kopfbänder, dann die Blätter.
4. **Daniel muss vorab entscheiden:** die Farbe von Flickwerk (F1), ob hochgerechnete Bilder als 4× gelten (F2) und die Farben von Schattenfaust und Sternenwacht.
5. **Nicht beurteilen kann ich:** die Ausgabegrenzen von Meshy, die Haltung von `drache_weiss.png` und die Farbe von `burg_05`.

---

## Zusatzinformationen (nicht beauftragt)

> Hinweise, keine Anweisungen.

**Z1 Die Meshy-Vorlage hat „Müll“ im durchsichtigen Bereich.** Das gesehene `elfen_wappen.png` zeigt im Hintergrund buntes Rauschen. Das sind die Farbwerte der Pixel mit Alpha = 0; jedes Bildprogramm, das den Alphakanal nicht beachtet, zeigt sie so. Im Spiel stört das nicht, **solange** jedes Verkleinern vormultipliziert läuft (`RGBa`, Nr. 6).
- **Prüfung für alle neuen Freisteller:** einmal ohne Alpha (`convert("RGB")`) und einmal auf Magenta ansehen. An den Kanten darf kein Farbsaum entstehen.
- Für die Dezemberbilder lohnt die Bitte an das Modell: „transparent pixels black“.

**Z2 Die Wappen der Chronik und die Bilder `wappen_01–10` decken sich nicht überall.** Die Chronik beschreibt zum Beispiel für Sternenwacht eine Mondsichel mit Stern, für Knochenmoor einen Raben. Ob `wappen_09` und `wappen_02` diese Motive zeigen, konnte ich nicht sehen. Da die Abzeichen von der Karte verschwunden sind (F-100), betrifft das nur noch Kopf und Einzelansicht. Ein Abgleich lohnt trotzdem, bevor die Kopfbänder entstehen.

**Z3 Werteblock zum Nachrechnen** (wie in Nr. 16 angeboten):

```
name;formel;wert
ruine;4*44;176
drache;4*44;176
startbild;4*1024 x 4*720;4096x2880
kopfband_b;4*1127;4508
kopfband_h;round(4508*150/780);867
goldrahmen;4*920;3680
goldrahmen_band;round(3680*0.0335);123
goldrahmen_radius;round(3680*0.075);276
kachelrahmen;4*64;256
leiste_mitte;4*64 x 4*34;256x136
leiste_ende;4*16 x 4*34;64x136
markt;4*96;384
kopfband_schnitt;round(1127*150/780)-200;17
```

**Korrektur meiner eigenen Angabe:** 4508 × 150 / 780 = 866,9, gerundet also **867**, nicht 868. Die Anlage 2 nennt 868 und meine Tabellen oben übernehmen das. Weil Bildmodelle gerade Kantenlängen bevorzugen, empfehle ich **868**; die Abweichung von 1 px ist im Mittelschnitt ohne Wirkung.

---

Ende der Antwort auf Auftrag Nr. 19.
