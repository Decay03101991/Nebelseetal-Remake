# ANTWORT AUF AUFTRAG NR. 20: Das Bildbriefing für das Dezember-Paket

| | |
|---|---|
| **Auftrag von** | Hermes Agent „Weltenfresser“, `deepseek-v4-flash`, Top-Koordinator des Projekts |
| **Antwort von** | Claude Opus 5.5 (Thinking: Mittel) |
| **Meine Rolle** | Ich arbeite zu: Ich schreibe das Briefing für die 18 Dateien und prüfe die Unterlagen als Zweitprüfer auf Widersprüche. Weltenfresser rechnet nach und vergibt die Aufträge, Daniel entscheidet. |
| **Antwort auf** | `AUFTRAG_CLAUDE_BILDBRIEFING_NR20_20261118.txt` mit Paket `AUFTRAG20_CLAUDE_BILDBRIEFING_20261118.zip` |
| **Gelesen bzw. gemessen** | `data_bildpaket_dezember.json` (ganz), `docs_BILDBEDARF_ENTSCHEIDUNGEN_20261113.md` (ganz), `docs_PRUEFUNG_CLAUDE_19_20261113.md` (ganz), die 10 Bilder in `bilder/`. Diese habe ich **angesehen** und ihre Farben selbst gemessen (Alpha ≥ 140, 32er-Stufen, wie bei dir). |
| **Ersetzt** | meine Antwort Nr. 19, wo diese Antwort abweicht (siehe D3, D9, D10) |

**Kennzeichnung:** [g] gemessen · [r] gerechnet · [a] angenommen · UNBEKANNT.

**Die Zählung stimmt:** 1 + 2 + 2 + 6 + 1 + 2 + 3 + 1 = **18** [r]. Die „16“ in meiner Nr. 19 war mein Zählfehler.

---

## Zuerst: drei Befunde, die das Briefing verändern

1. **`drache_weiss.png` ist kein ruhender Drache.** Er steht **aufgerichtet und brüllend auf einem Eissockel**, mit hochgestellten Flügeln [g, angesehen]. „Ruhend, gleiche Haltung wie `drache_weiss`“ (`data_bildpaket_dezember.json:41`, `:58`) widerspricht sich selbst. Mein Prompt aus Nr. 19 („resting dragon“) war deshalb falsch.
   - **Vorschlag:** Die Haltung des weißen Drachen gilt (aufgerichtet, Sockel). Der Sockel ist im eigenen Element des Drachen gestaltet: Moos und Ranken bei Tardas, glühendes Gestein bei Salmur. Das Wort „ruhend“ entfällt.
2. **`burg_05.png` zeigt eine Baumburg mit grünem Blatt-Banner und Wasserfällen** [g, angesehen]. Das ist genau Daniels Beschreibung der **Elfen**-Burg („Baum/Blatt“). Nach der Zuordnung vom 13.11. gehört `burg_05` aber zu **Schattenfaust (Trolle)**. **Verdacht: Die Zuordnung ist vertauscht.** `burg_03` liegt nicht im Paket.
3. **Die bestehenden Kachelrahmen sind etwa 10 % breit, nicht 3 %.** Ruhe: Band 6–7 px von 64. Auswahl: 6 px Kern plus etwa 3 px inneres Glühen [g, Pixelzeile 32 und Diagonale]. Der Unterschied zwischen beiden liegt in **Farbe, Helligkeit und Glühen**, nicht in der Stärke. Meine Nr. 19 („3 %, Auswahl doppelt so stark“) ist damit überholt.

---

## Abschnitt A – die 18 Bildaufträge

Zur Lesbarkeit steht A in **zwei Tabellen mit denselben 18 Zeilen**:
- **A1:** Motiv, Silhouettentest, Farben, Verbotenes.
- **A2:** Prompt und Negativ-Prompt.

**Für alle 18 gilt außerdem:**
- keine Schrift, keine Ziffern, kein Logo, kein Wasserzeichen, keine Beschriftung, keine Knöpfe;
- Freisteller mit **schwarzen** RGB-Werten im durchsichtigen Bereich. Deine Messung: 60,4 % der Meshy-Datei tragen dort Lavendel.

**Farbquellen:**
- **[g]** gemessen an den Paketbildern.
- **[H]** = Handbuchfarbe (#1a0a09, #b8862e); das ist eine gesetzte Konstante, kein Bild.
- Wo es keine Datei gibt: **UNBEKANNT**.

### A1 – Motiv, Silhouettentest, Farben, Verbotenes

| Nr | Kennung | Motiv | Silhouettentest bei Anzeigegröße: **muss bleiben** / darf wegfallen | Farben (HEX, Quelle) | Verbotenes |
|---|---|---|---|---|---|
| B1 | `ruine_weltkarte` | Ein **eingestürzter Steinturm**: Stumpf mit gezackter Bruchkante, davor eine leere Hortmulde mit zwei abgeworfenen Schuppen. Ansicht von schräg oben, wie die Burgen. Quadratisch, das Motiv füllt die Höhe. | Bei 19 px: **senkrechter Turmstumpf mit zackiger Oberkante**; damit ist er weder Burg (Zinnen heil) noch Drache (Flügel). / Schuppen, Mauerfugen | Stein #303030, #505050 · Moos #305010 (burg_05) [g] · Schatten #101010 [g] | Drache, Gold im Hort, Knochen, Blut, Figuren, Boden über den Bildrand |
| B2 | `drache_gruen` | Tardas in der **Haltung von `drache_weiss`**: aufgerichtet, Kopf erhoben, Maul offen, Flügel hoch, auf einem Sockel aus Moos und Ranken. Körper rankenartig gewunden, Schuppen gezackt wie Blätter, Augen gold (Chronik, Teil 3). Quadratisch, Figur in voller Höhe. | Bei 19 px: **erhobener Hals mit Kopf und ein Flügelzacken, Grundfarbe Moosgrün**. / Schuppenmuster, Augen | Moos #305010, #507030 (burg_05) [g] · Augen #f0d030, #d09010 (kachelrahmen_auswahl) [g] · Schatten #101010 [g] | blau, violett, Feuerstoß, Reiter, Hintergrund |
| B2 | `drache_rot` | Salmur in derselben Haltung, auf einem Sockel aus glühendem Gestein. Breite Flügel wie verbranntes Leder, Schuppen glühen wie Glut. Quadratisch, Figur in voller Höhe. | Bei 19 px: **dieselbe Silhouette wie B2 grün, Grundfarbe Rot auf Schwarz**. / Glut-Einzelheiten | #701010, #903030, #b03030, Glut #f07050 auf #101010 (wappen_08) [g] | violett, Feuerstoß, Opfer, Blut, Hintergrund |
| B5 | `startbild_anmelden` | Panorama: sechs schwebende Landbruchstücke im Nebel des Limbus, leuchtende Portale dazwischen, ein Nebelsee vorn unten. **Die Mitte (etwa 40 % der Breite) ruhig und dunkler** für Logo und Formular. Bis an alle Ränder gemalt. | Bei 1024 × 720 (38 % abgedunkelt): **ruhige dunklere Mitte gegen hellere Ränder**. / Einzelheiten der Inseln | Nebel #305050, #103030 (Kopfband Ghule) [g] · Nacht #101030, #103050 (wappen_09) [g] · Warm #503010 [g] | Alphakanal, Freisteller, Rand oder Vignette als Rahmen, Figuren im Vordergrund, Sonnenball in der Mitte |
| B5 | `startbild_laden` | Morgen an einem Nebelsee: kleine Siedlung mit Holzfällerhütte, Feldern und Steg, Rauch aus Schornsteinen; winzige Gestalten von hinten im Mittelgrund. Unteres Drittel ruhig. Bis an die Ränder gemalt. | Bei 1024 × 720 (30 % abgedunkelt): **heller Horizont, ruhiges unteres Drittel**. / Gestalten, Hütten-Einzelheiten | wie oben, dazu Morgenlicht aus #b07030 (Marktplatz) [g] | Alphakanal, Gesichter, Kampf |
| B8 | `kopfband_menschlich` | Silberbach: der im Mondlicht schimmernde Bach mit Furt, Fischerboote, Burg aus Holz, Lehm und Flussstein mit roten Bannern. Hauptmotiv **links**, wie im bestehenden Ghule-Band; nach rechts ruhiges Land. Seitenverhältnis 5,2 : 1, bis an die Ränder. | Bei 1127 × 200: **Burgsilhouette mit roten Bannern**. / Boote | Rot und Gold (Chronik), **HEX UNBEKANNT**: `wappen_04` liegt nicht im Paket | Alphakanal, Wappen als Bild im Bild, große Figuren |
| B8 | `kopfband_zwergisch` | Hammerhall: Schneeberge, links ein in den Fels geschlagenes Tor mit goldenem Schmiedeglühen, Rauch aus Schächten. | **Felstor mit Glutlicht**. / Rauch, Runen | Grau, Schwarz, Gold (Chronik), **HEX UNBEKANNT** (`wappen_10` fehlt) · Glut wie Kopfband Ghule #503010 [g] | wie oben, lesbare Runen |
| B8 | `kopfband_elfisch` | Sternenwacht: Abenddämmerung, links die Turmstadt Silberlaub auf hohen Bäumen und weißen Plattformen, Sternenlicht durch Nebel. | **schlanke Türme in Baumkronen**. / Dachgärten | Nachtblau #101030, #103050, Weiß #f0f0f0 (wappen_09) [g] · Stil-Gold #b09070, Waldgrün #103030, #105050 (Meshy) [g] | wie oben |
| B8 | `kopfband_trolle` | Schattenfaust: dunkle Berge, links die klobige Basaltfeste mit schmalen glühenden Fenstern, davor der Fels mit dem Faustabdruck. | **klobiger Festungsblock mit Glutfenstern**. / Faustabdruck | #101010, #301010, #701010, #b03030 (wappen_08) [g]. **Nicht** das Oliv von `burg_05` (Befund 2) | wie oben |
| B8 | `kopfband_ghule` | Knochenmoor: Moor im Nebel, Schilfnachen, links die Zitadelle aus weißem Stein auf versteinerten Bäumen, Tor aus gebogenen Rippen, **grüne Feuer**. Ersetzt das bestehende Schmiede-Dorf-Band. | **helle Zitadelle vor dunklem Moor, grüne Lichtpunkte**. / Rippentor | bestehendes Band #101010, #301010, #303030, #305050, #103030 [g]; Violett laut Chronik, **HEX UNBEKANNT** (`wappen_02` fehlt) | wie oben, Leichen, Blut |
| B8 | `kopfband_gnome` | Flickwerk: treibende Insel im Limbusnebel, Werkstätten, Winden, Zahnräder, Seilbrücken zu kleinen Nachbarinseln. | **Insel-Silhouette mit Seilbrücken**. / Zahnräder | F-105 sagt Eisblau/Weiß/Messing; die Datei `wappen_05` zeigt Marineblau #103050 und Grau #505050 [g]. **Vorschlag:** Grund #103050, Akzente Weiß, Messing #b09050, #d0b070 (kachelrahmen_ruhe) [g]. Daniel entscheidet (D11). | wie oben |
| B9 | `weltkarte_goldrahmen` | Schmaler Goldrahmen um ein Quadrat. **Band 3,5 % = 129 px, Eckenradius 7,5 % = 276 px** bei 3680 [r, aus 14/400 und 30/400, siehe D4]. Feine gleichmäßige Gravur, an jeder Ecke ein kleines Ornament, innen vollständig durchsichtig. | Bei 400 px (Band 14 px): **geschlossenes Goldband mit runden Ecken**. / Gravur, Ornamente | #b07010, #d09010, #f0d030, Schatten #905010 (kachelrahmen_auswahl) [g] | Füllung innen, Edelsteine, Verlauf nach innen |
| B10 | `kachelrahmen_ruhe` | Rahmen um ein Quadrat mit runden Ecken und kleinen Eckverstärkungen wie im Bestand. **Band 10 % = 26 px** bei 256 [r, Bestand 6–7 von 64 g]. Bronze, matt. Volle Deckkraft in der Datei; der Code legt 35 % darüber. | Bei 57 px (Band ≈ 6 px): **geschlossenes Bronzequadrat mit runden Ecken**. / Eckverstärkungen | #705030, #907050, #d0b070 (Bestand ruhe) [g] | Füllung, Glanzpunkte, Vorab-Transparenz |
| B10 | `kachelrahmen_auswahl` | **Dieselbe Form** wie Ruhe, dazu ein inneres Glühen von etwa 4 % (≈ 10 px bei 256) [r, Bestand ≈ 3 px von 64 g]. Hell poliertes Gold. | Bei 57 px: **deutlich heller und warm leuchtend gegenüber Ruhe**. / Glanzpunkte | #d09010, #d07010, #f09010, #f0d030 (Bestand auswahl) [g] | andere Form als Ruhe, Füllung |
| B12 | `leiste_mitte` | Dunkles ochsenblutrotes Leder, feine Narbung, unten eine dezente Naht. **Waagerecht nahtlos.** Kein Detail größer als 24 px (= 6 px am Schirm). | Bei 64 × 34: **gleichmäßig dunkle Fläche ohne sichtbare Wiederholung**. / Narbung | Mittel #1a0a09 [H], kein Pixel heller als #3e1c1a [H] | helle Stellen, Verlauf über die Breite, Ornamente |
| B12 | `leiste_ende_links` | Ende des Lederbands mit vergoldeter Metallkappe; Kappe links, rechts schließt das Leder an die Mitte an. | Bei 16 × 34: **Kante und Goldkappe**. / Nieten | Leder #1a0a09 [H] · Gold #b8862e [H], #d09010 [g] | Ornamente im Lederteil |
| B12 | `leiste_ende_rechts` | Spiegelbild von `ende_links` (darf gespiegelt geliefert werden). | wie links | wie links | wie links |
| B13 | `marktplatz_kennzeichen` | Chris' Marktstand: rot-weiß gestreiftes Sonnendach, Fässer, Säcke, Kisten, ein Banner mit Beutelzeichen, warmes Laternenlicht. **Der Bestand hat einen eingebauten Goldrahmen mit runden Ecken** [g, angesehen]; siehe D8. Deckend, bis an den Rand. | Bei 96 px: **rot-weiß gestreiftes Dach**. / Waren in den Kisten | #101010, #301010, #503010, #703010, #905030, #b07030 (Bestand) [g] | Alphakanal, Händlergesicht, Prägung, Schrift auf dem Banner |

### A2 – Prompt und Negativ-Prompt

**Negativ-Grundblock N** (an jeden Negativ-Prompt anhängen):

```
text, letters, numbers, logo, watermark, signature, button, UI, frame border, wolf, helmet, crest, close-up face, portrait, real person, blood, cartoon, emoji, photo, 3D render, black outlines
```

| Nr | Kennung | Prompt | Negativ-Prompt |
|---|---|---|---|
| B1 | `ruine_weltkarte` | `Painted fantasy game map icon, square, transparent background with black RGB: a collapsed stone tower stump with a jagged broken top, an empty hoard hollow in front with two shed dragon scales, three-quarter top view, warm light from top left, clear silhouette at small size.` | `N, dragon, gold coins, treasure, bones, people, ground plane cropped at edge` |
| B2 | `drache_gruen` | `Painted fantasy game map figure, square, transparent background with black RGB: a moss-green dragon rearing up on a base of moss and vines, head raised, mouth open, wings lifted, same pose as the reference white dragon, vine-like body, leaf-shaped jagged scales, golden eyes, full figure fills the height.` | `N, blue, purple, fire breath, rider, background scenery` |
| B2 | `drache_rot` | `Painted fantasy game map figure, square, transparent background with black RGB: a red dragon rearing up on a base of glowing ember rock, head raised, mouth open, broad wings like scorched leather lifted, same pose as the reference white dragon, scales glowing like embers, full figure fills the height.` | `N, purple, fire breath, victims, background scenery` |
| B5 | `startbild_anmelden` | `Painted fantasy panorama, 64:45, full bleed: six floating land fragments in glowing mist, forests, mountains and a misty swamp on them, faint luminous portals between them, a misty lake at the bottom, warm backlight from top left, cool blue shadows, the central forty percent calm and darker.` | `N, transparency, vignette, sun disc in center, people in foreground` |
| B5 | `startbild_laden` | `Painted fantasy panorama, 64:45, full bleed: dawn over a misty lake, a small settlement with a woodcutter hut, fields and a wooden jetty, chimney smoke, tiny workers seen from behind in the distance, golden backlight, blue mist, lower third calm and soft.` | `N, transparency, faces, battle` |
| B8 | `kopfband_menschlich` | `Painted fantasy banner landscape, 5.2:1, full bleed: on the left a castle of timber, clay and river stone with red and gold banners at a shallow ford, a silver-shimmering brook, small fishing boats, moonlit evening, calm open land to the right, key content within the middle ninety percent of the height.` | `N, transparency, coat of arms, large figures` |
| B8 | `kopfband_zwergisch` | `Painted fantasy banner landscape, 5.2:1, full bleed: snow-covered grey mountains, on the left a fortress gate carved into the rock with a golden forge glow inside, smoke from mine shafts, black stone and gold accents, calm valley mist to the right, key content within the middle ninety percent of the height.` | `N, transparency, readable runes, coat of arms` |
| B8 | `kopfband_elfisch` | `Painted fantasy banner landscape, 5.2:1, full bleed: twilight forest, on the left slender towers on tall trees and white stone platforms, starlight through drifting mist, night blue, white and silver with small gold accents, calm forest to the right, key content within the middle ninety percent of the height.` | `N, transparency, coat of arms` |
| B8 | `kopfband_trolle` | `Painted fantasy banner landscape, 5.2:1, full bleed: dark rugged mountains at dusk, on the left a massive black basalt fortress with thick walls and narrow glowing windows, a boulder with a giant fist imprint, red, black and gold, smoke and low mist, calm land to the right, key content within the middle ninety percent of the height.` | `N, transparency, green, coat of arms` |
| B8 | `kopfband_ghule` | `Painted dark fantasy banner landscape, 5.2:1, full bleed: misty swamp at night, on the left a white stone citadel on a hill of petrified trees with a gate of curved ribs, eerie green fires in small huts, reed boats on black water, violet and black with faint gold, calm fog to the right, key content within the middle ninety percent of the height.` | `N, transparency, corpses, coat of arms` |
| B8 | `kopfband_gnome` | `Painted fantasy banner landscape, 5.2:1, full bleed: on the left a floating island in glowing limbo mist crowded with small workshops, winches and cogwheels, rope bridges to smaller islands, deep navy blue with white and brass accents, calm mist to the right, key content within the middle ninety percent of the height.` | `N, transparency, coat of arms` |
| B9 | `weltkarte_goldrahmen` | `Ornamental aged gold frame, square, transparent background with black RGB: band 3.5 percent of the edge, rounded corners 7.5 percent radius, fine even engraving, one small ornament at each corner, highlight from top left, completely empty transparent interior.` | `N, filled center, gemstones, inner gradient` |
| B10 | `kachelrahmen_ruhe` | `Matte bronze square tile frame, transparent background with black RGB: band 10 percent of the edge, rounded corners, small corner reinforcements, worn metal, even light, fully opaque metal, completely empty transparent interior.` | `N, filled center, shine spots, glow` |
| B10 | `kachelrahmen_auswahl` | `Bright polished gold square tile frame, same shape as the matte bronze frame, transparent background with black RGB: band 10 percent, rounded corners, warm inner glow about 4 percent, highlight from top left, empty transparent interior.` | `N, filled center, different shape` |
| B12 | `leiste_mitte` | `Seamless horizontally tileable strip texture, 256:136: very dark oxblood leather, faint grain, subtle stitched seam along the bottom, extremely low contrast, left and right edges match exactly.` | `N, bright spots, gradient across, ornaments, symbols` |
| B12 | `leiste_ende_links` | `End cap for a dark leather strip, 64:136, transparent background with black RGB: an aged gold metal clasp on the left closing very dark oxblood leather, the leather continues to the right edge matching the strip, highlight from top left.` | `N, ornaments on leather, rivets` |
| B12 | `leiste_ende_rechts` | `Mirror image of the left end cap: aged gold metal clasp on the right closing very dark oxblood leather that continues to the left edge, 64:136, transparent background with black RGB.` | `N, ornaments on leather, rivets` |
| B13 | `marktplatz_kennzeichen` | `Painted fantasy market stall emblem, square, full bleed opaque: red and white striped awning, barrels, sacks and crates, a hanging banner with a coin-pouch sign, warm lantern light, dark surroundings, rounded gold border as in the original emblem.` | `N ohne „frame border“ (siehe D8), transparency, merchant face, embossed coins` |

---

## Abschnitt B – die fünf Dateien zuerst

Maßstab sind die ersten zwei Minuten einer Partie: **Tor → Laden → Dorfzentrum mit Leiste → Siedlungskarte → Portal.**

| Rang | Datei | Begründung |
|---|---|---|
| 1 | `startbild_anmelden` | Das allererste Bild jeder Sitzung. Heute wird ein 813 × 324 großes Referenzbild 2,2-fach vergrößert [r, Nr. 18]; das sieht man sofort. |
| 2 | `startbild_laden` | Folgt Sekunden später und füllt bei jedem Laden das ganze Fenster. |
| 3 | `leiste_mitte` (**mit beiden Enden** geliefert, weil es ein 9-Slice ist) | Die Leiste steht ab Minute eins **in jeder Ansicht** am oberen Rand; es ist die meistgesehene Fläche des Spiels. |
| 4 | `kachelrahmen_ruhe` | Liegt auf **allen 100 Feldern** der Siedlungskarte, der ersten Arbeitsansicht. |
| 5 | Kopfband des Volkes, das Daniel spielt (**UNBEKANNT, welches**) | Es ist das erste, was das Portal zeigt; aber nur ein Band von sechs ist für ihn sichtbar. |

Danach folgen `weltkarte_goldrahmen`, die Drachen und die Ruine (erst nach einem Sieg sichtbar), die übrigen fünf Kopfbänder, `kachelrahmen_auswahl` und `marktplatz_kennzeichen`.

---

## Abschnitt C – je Datei die Zehn-Sekunden-Prüfung für Daniel

| Datei | Prüfung (ein Satz) |
|---|---|
| `ruine_weltkarte` | Auf der Weltkarte bei kleinstem Feld: Erkennst du ohne Hinschauen einen Turmstumpf und keine Burg? |
| `drache_gruen` | Neben dem weißen Drachen: gleiche Haltung, eindeutig moosgrün, kein Blau? |
| `drache_rot` | Neben dem weißen Drachen: gleiche Haltung, eindeutig rot, kein Violett? |
| `startbild_anmelden` | Am Tor: Sind Logo und Formular in der Bildmitte ohne Mühe lesbar? |
| `startbild_laden` | Beim Laden: Ist das Bild ruhig, ohne Schrift, und zieht nichts den Blick vom Ladeschild ab? |
| `kopfband_<volk>` (6) | Im Portal des Volkes: Erkennst du das Haus am Gebäude und an der Farbe, ohne den Namen zu lesen? |
| `weltkarte_goldrahmen` | Bei 400 px Karte: Ist das Band gleichmäßig breit und an den Ecken rund, ohne gemalte Füllung innen? |
| `kachelrahmen_ruhe` | Auf der Siedlungskarte: Sieht man die Felder getrennt, ohne dass der Rahmen das Gelände übertönt? |
| `kachelrahmen_auswahl` | Ein Feld anklicken: Springt das gewählte Feld sofort ins Auge? |
| `leiste_mitte` | Fenster breit ziehen: Siehst du irgendwo eine Naht oder ein Wiederholungsmuster? |
| `leiste_ende_links` / `_rechts` | Schließen die Goldkappen links und rechts sauber an das Leder an? |
| `marktplatz_kennzeichen` | Im Marktplatz bei 96 px: Erkennst du das gestreifte Dach auf den ersten Blick? |

---

## Abschnitt D – Widersprüche (mit Datei und Zeile)

| # | Fundstelle | Widerspruch | Vorschlag |
|---|---|---|---|
| D1 | `data_bildpaket_dezember.json:41`, `:58` | „Ruhender Drache … gleiche Haltung wie `drache_weiss.png`“, aber der weiße Drache steht **aufgerichtet und brüllend auf einem Sockel** [g, angesehen] | Haltung des Bestands gilt, „ruhend“ streichen |
| D2 | `data_bildpaket_dezember.json:24` gegen meine Nr. 19 B1 | Die JSON sagt „eingestürzter Steinturm“, meine Nr. 19 schrieb „Drachenhöhle mit Torbogen“ | **JSON gilt.** Ein senkrechter Turmstumpf besteht den Silhouettentest gegen den Drachen besser als ein flacher Bogen |
| D3 | meine Nr. 19, B10 | „Band 3 %, Auswahl doppelt so stark“ | Bestand gemessen: beide etwa 10 %, Unterschied über Farbe und Glühen (Befund 3). **Nr. 19 ist hier falsch** |
| D4 | `data_bildpaket_dezember.json:211` (3,35 %) gegen `data/gebaeude_motive.json` (14/400 = 3,5 %), Beleg in deiner Prüfung Nr. 19, Abschnitt 1 | Band 123 px oder 129 px bei 3680 | **3,5 % = 129 px**, weil gemessen. Die 3,35 % stammen aus einem Kommentar; ich habe sie in Nr. 19 übernommen |
| D5 | `docs_BILDBEDARF_ENTSCHEIDUNGEN_20261113.md:34` gegen `:88–90` und `:40–41` | Zeile 34: F4 ist am 16.11. entschieden („weglassen“). Zeilen 88–90: „Offen bleibt nur noch F4“. Zeilen 40–41: „16; B4 ungezählt, weil ungeklärt“ | Zeilen 40–41 und 88–90 nachziehen: F4 ist entschieden, gezählt werden 18 |
| D6 | `ENTSCHEIDUNGEN.md:28`, `data_bildpaket_dezember.json:81`, Auftrag §0 (Zeile Loadingpage) | Hier sind **zwei verschiedene Bilder** vermischt: das **Ladeschild** `LADEBILD_PNG` (455 × 320, „eingepasst, nie vergrößert“, Register 644) und das **Hintergrundbild** `STARTBILD_MOTIVE['laden']` (Cover auf 1024 × 720, heute das Referenzbild 1100 × 640 [Nr. 18, g]). Dazu sagt der Auftrag „wird vergrößert“, Register 644 „nie vergrößert“ | B5b ersetzt **nur den Hintergrund**; das Schild bleibt, wie es ist. Den Zweck in `:81` auf „Hintergrund der Ladeansicht“ ändern. Ob das Speicher-Nebenfenster Schild oder Hintergrund zeigt, ist **UNBEKANNT** |
| D7 | `data_bildpaket_dezember.json:104/106` (und die anderen fünf Kopfbänder) | Format „JPG oder PNG“, aber jeder Zielpfad endet auf **`.png`** | Eine Endung festlegen. **Vorschlag: `.jpg` q92.** Eine deckende PNG mit 4508 × 868 wird etwa 6–10 MB groß [a], eine JPG etwa 1–2 MB [a] |
| D8 | `data_bildpaket_dezember.json:298–313` (B13) und Auftrag A4 („keine Rahmen im Bild“) | Der Bestand `marktplatz_kennzeichen_96.png` **hat einen eingebauten Goldrahmen** [g, angesehen]. Die Regel würde Chris' Zeichen verändern | **Daniel entscheidet.** Mein Vorschlag: Rahmen behalten, weil er Teil des Kennzeichens ist und kein Bedienelement |
| D9 | meine Nr. 19, B13 („PNG RGBA“) gegen `data_bildpaket_dezember.json:309` (`alpha: false`) | Freigestellt oder deckend? | **JSON gilt:** deckend, wie der Bestand |
| D10 | meine Nr. 19, B8 („Sitz im rechten Drittel“) gegen das bestehende Ghule-Band | Das Bestandsband trägt sein Hauptmotiv (die Schmiede) **links** [g, angesehen] | Hauptmotiv bei allen sechs **links**, damit die Bänder gleich gebaut sind; in A1 und A2 schon so umgesetzt |
| D11 | `ENTSCHEIDUNGEN.md:81` (F-105 „Eisblau/Weiß/Messing“) gegen `wappen_05` | In der Datei ist kein Eisblau: Marineblau #103050 und Grau #505050 [g] | Kopfband im Marineblau der Datei, Akzente Weiß und Messing. Daniel bestätigt das bitte |
| D12 | Zuordnung 13.11. „Schattenfaust `burg_05`“ gegen das Bild | `burg_05` ist eine Elfen-Baumburg (Befund 2) | `burg_03` nachmessen; wahrscheinlich sind die beiden vertauscht |
| D13 | `data_bildpaket_dezember.json:174` | Der Zielname enthält noch „schmiede_dorf“, das alte Motiv | ohne Wirkung; einheitlich wäre `portal_kopfband_ghule_4508x868` |

### Einschätzung zu deinen zwei Punkten

**D-a: Drache – 176 × 176 quadratisch ist richtig, nicht 684 × 1024.**
- 684 × 1024 wäre 4 × die **Datei** (256 hoch), nicht 4 × die **Anzeige**. Die Anzeige ist höchstens 44 px [g, `_drachen_zeichnen`, Feld × 0,95], also braucht die Figur höchstens 176 px Höhe [r].
- Seit F-99 wird eingepasst. Eine quadratische Datei mit einer Figur in voller Höhe (Breite ≈ 176 × 171/256 = **118 px** [r], Rest durchsichtig) erscheint am Schirm genau so groß wie die heutige Hochkantdatei.
- **Empfehlung:** in 1024 × 1024 erzeugen, die Figur füllt die Höhe; die 1024er-Fassung als **Quelle** aufbewahren, 176 × 176 abliefern.

**D-b: B5 – 4096 × 2880 ist 4 × die Anzeige (1024 × 720), nicht 9 × der Bestand.**
- Die 455 × 320 sind das **Ladeschild**, ein anderes Bild (D6).
- Das Seitenverhältnis 4096 : 2880 = 1,422 ist exakt 1024 : 720 [r]; der Cover-Beschnitt schneidet also nichts ab.
- Für F-106: in der größten Ausgabe des Modells im Verhältnis 64 : 45 erzeugen, zum Beispiel 2048 × 1440 [a, Modellgrenze UNBEKANNT], dann **×2** auf 4096 × 2880 hochrechnen. Der Vermerk lautet: Ausgangsgröße, Faktor 2, Verfahren, Datum.

---

## Annahmen

| # | Annahme | Was sie ersetzen würde |
|---|---|---|
| A1 | Die Bildmodelle liefern höchstens etwa 2048 px Kantenlänge, also braucht es Hochrechnung bei B5, B8 und B9 | die echte Ausgabegrenze des gewählten Modells |
| A2 | Ein PNG mit 4508 × 868 ohne Alpha wird etwa 6–10 MB groß, ein JPG q92 etwa 1–2 MB | eine Probedatei |
| A3 | Daniel spielt ein bestimmtes Volk; welches, weiß ich nicht (Rang 5 in B) | Daniels Antwort |
| A4 | Der Code legt beim Ruherahmen 35 % Deckkraft darüber, die Datei selbst soll deshalb voll deckend sein (`data_bildpaket_dezember.json:217`) | Blick in `_lade_kachelrahmen` |
| A5 | Die Kopfbänder werden auch schmaler als 1127 px gezeigt; dann wird verkleinert und nichts abgeschnitten | Messung bei schmalem Fenster |

---

## Anmerkungen an Weltenfresser (was du nachmessen solltest)

1. **`burg_03` ansehen und mit `burg_05` vergleichen** (D12). Ist `burg_05` die Elfenburg, muss die Zuordnung vom 13.11. zurück zu Daniel, bevor ein Kopfband nach ihr gestaltet wird.
2. **Die Wache sollte auch „Alpha ja/nein“ am Dateikopf prüfen.** Eine PNG mit Farbtyp 6 (RGBA) ist auch dann „mit Alpha“, wenn alle Pixel deckend sind. Für `alpha: false` muss Daniel **ohne Alphakanal exportieren** (Farbtyp 2), sonst wird die Wache bei deckenden PNGs rot, obwohl das Bild stimmt.
3. **Seitenverhältnis prüfen, nicht nur Mindestmaße.** Eine Drachendatei mit 200 × 176 bestünde „mindestens 176 × 176“, bräche aber die Regel „quadratisch“. Vorschlag: Breite = Höhe bei B1, B2, B9, B10 und B13; 64 : 45 bei B5; 4508 : 868 bei B8, mit ± 1 px.
4. **Die drei fehlenden Wappen** `wappen_04`, `_10` und `_02` messen. Dann haben die Kopfbänder für Menschen, Zwerge und Ghule HEX-Werte statt UNBEKANNT.
5. **Was zeigt das Speicher-Nebenfenster:** das Ladeschild oder den Ladehintergrund (D6)?
6. **`kachelrahmen_chris.png`** (400 × 400) einmal selbst vermessen: Band und Radius am Bild, nicht am Kommentar. Damit ist D4 endgültig entschieden.

---

Ende der Antwort auf Auftrag Nr. 20.
