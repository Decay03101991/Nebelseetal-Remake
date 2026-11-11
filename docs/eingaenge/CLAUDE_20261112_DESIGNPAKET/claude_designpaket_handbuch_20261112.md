# NEBELSEETAL - DESIGNPAKET: GESTALTUNGS-HANDBUCH FÜR EIN VOLLSTÄNDIGES BILDPAKET
Antwort auf Auftrag Nr. 3 (Hermes für Daniel Kössl, 12.11.2026, 00:2x)
Von Opus 5.5 (Thinking: Mittel) erarbeitet, 12.11.2026. Geprüft gegen main = f6bb9e6 (12.11.2026, 00:24).
Kein Code, keine Bilder, keine Änderung am Repo.

Lesehilfe
- "belegt: &lt;Datei&gt; Z. n" = im Repo nachgesehen, Stand f6bb9e6.
- "Vorschlag:" = von mir, nicht belegt.
- "Entscheidung:" = der Auftrag ließ etwas offen oder widerspricht dem Repo; ich habe entschieden und begründe es.
- "weiß ich nicht" = nicht prüfbar aus dem Repo.
- Alle Maße in px gelten für 100 % Windows-Skalierung, wenn nichts anderes steht.

## VORAB: DREI BEFUNDE, DIE DAS GANZE PAKET BETREFFEN

**V-1**  Unschärfe hat eine zweite Ursache im Code, nicht nur im Bild.  
belegt: src/gebaeude_optik.py Z. 105-125. Das Gebäude-Hintergrundbild ist 538 x 222 px (assets/icons/gebaeude/hintergrund/, 20 Dateien) und wird laut Kommentar auf eine Fläche von 1142 x 1120 px gebracht: einmal mit LANCZOS hochskaliert und nachgeschärft (UnsharpMask), einmal gespiegelt, gestreckt und mit GaussianBlur weichgezeichnet. Das ist genau Daniels "gut gewählt aber leider unscharf".  
Folge für dieses Paket: Jedes neue Bild wird in der Größe erzeugt, in der es gezeigt wird, und das Spiel zeigt es 1 : 1 (siehe 1.3, Regel R-1). Neue Bilder brauchen keinen Spiegel- und keinen Weichzeichner-Füllgrund mehr, weil sie die ganze Fläche selbst malen.

**V-2**  Windows-Skalierung: weiß ich nicht, ob das Fenster gestreckt wird.  
belegt: In src/, tools/ und den .bat-Dateien steht kein SetProcessDpiAwareness, kein SetProcessDPIAware, kein "tk scaling" und kein Manifest mit dpiAware (grep, Stand f6bb9e6).  
Ohne diese Angabe kann Windows ein Programm bei 125 % und 150 % als Bitmap hochziehen; dann wird auch ein perfekt scharfes neues Bild unscharf. Am Gerät gesehen habe ich das nicht.  
Vorschlag: vor dem ersten Bild einen Bildschirmfoto-Vergleich bei 100 % und 150 % machen. Ist die Schrift bei 150 % weich, liegt es an der Skalierung, nicht an den Bildern.

**V-3**  Die Menüleiste hat mehr als neun Punkte.  
belegt: src/main.py Z. 3695-3699 (MENU_ITEMS, 16 Einträge), Z. 3714-3719 (Kaserne, Forschung, Stellmacher, Diebesgilde erst nach Bau), Z. 3749 ("Lager" ausgeblendet), Z. 3840 (Zusatzpunkte "Voraussetzungen", "Neuigkeiten"), Z. 3833-3836 (Anzeige "Gildenhalle", "Schlachtsimulator").  
Sichtbar werden können 19 Punkte, dazu die zwei Ebenen "Übersicht" / "Siedlung" (Z. 3805).  
Entscheidung: T09 liefert 9 Kern-Icons (die Punkte ohne Baubedingung, die immer stehen) und 10 weitere in einer zweiten Welle. Begründung in T09.

## TEIL 1 - DAS SYSTEM

### 1.1 STILDEFINITION

Grundlage (belegt): docs/design/DESIGN_LIEFERUNG_CHRIS_20261109.md Z. 137-149 (Stilregeln aus Chris'
Lieferung), Z. 107-109 (gemessene Farben: Rahmengold #C68B42, Bannerrot #7E301E, Ghul-Leuchten #7AAC4D),
docs/design/DESIGN_ARBEITSWEISE.md Z. 58-59 (Chris' Bilder sind seit 09.11.2026 der Maßstab, F-39),
docs/design/PROMPT_GNOM_KRIEGER_20261112.txt (Hermes' Stil-Block für Figuren).

In Worten:
- Malerei, nicht Foto und nicht 3D. Sichtbarer, aber sauberer Pinselstrich, weiche Kanten, KEINE
```text
schwarze Kontur. Formen entstehen aus Licht und Schatten.
```
- Licht: warm vorn (Fackeln, Laternen, Feuerschalen, Essen), kühl hinten (Nebel, blaue Berge,
```text
Tannen). Ein klarer Lichtkegel je Bild, kräftiger Kontrast zwischen Hell und Dunkel.
```
- Farbe: kräftig, gesättigt, warm. Nie "braun in braun": jede dunkle Fläche hat einen Farbton
```text
(Rotbraun, Nachtblau, Tannengrün), und jedes Bild hat mindestens einen gesättigten Akzent.
```
- Perspektive: Szenen leicht von vorn oben (etwa 20-30 Grad), Gebäude mittig und ganz im Bild.
```text
Innenräume aus Augenhöhe oder leicht unten.
```
- Materialien: Holz grob und rissig mit warmer Maserung; Stein behauen, mit Kanten, Moos und
```text
Schmauch; Eisen geschmiedet, dunkel, an den Kanten blank gerieben; Gold antik, nicht spiegelnd;
Stoff dicht gewebt, Banner mit Saum und Fransen; Leder gefärbt und abgewetzt.
```
- Leben: Karren, Fässer, Säcke, Tiere, Werkzeug. Kaum Menschen, keine Gesichter im Vordergrund
```text
(Chris Z. 141: "kaum Menschen"; dazu die harte Regel "keine bekannten Gesichter").
```
- Banner: hängend, mit hellem Symbol, das die Funktion nennt (Chris Z. 142-145). Neutrale Banner rot
```text
mit hellem Symbol (F-37).
```
- Korn: feines Malkorn erlaubt, kein Bildrauschen, keine JPEG-Blöcke.
- Rahmen werden NICHT ins Bild gemalt, wenn das Spiel einen Rahmen setzt (siehe 1.3, R-4).

**STIL-BLOCK** (wörtlich in jeden Prompt, vor das Motiv):

```text
Digital painting in a painterly high-fantasy style, visible clean brushwork, soft painted edges,
no black outlines, forms modeled only by light and shadow. Warm light in the foreground from
torches, lanterns, fire bowls and forge glow; cool blue-violet mist, blue mountains and dark pine
forest in the background. Strong value contrast, rich saturated warm colours, every dark area
tinted, never flat brown. Materials: rough cracked timber with warm grain, chiselled stone with
moss and soot, dark forged iron with worn bright edges, antique matte gold, thick woven cloth
banners with hems and fringes, dyed worn leather. Lively details such as carts, barrels, sacks,
tools and animals, almost no people and no visible faces. Crisp focus on the main subject.
```

**Zwei Zusätze**, je nach Bildart (Vorschlag):

```text
SZENEN-ZUSATZ (für Hintergründe, Panoramen, Innenräume):
Wide establishing view, slightly elevated three-quarter angle, the main subject fully inside the
frame, a calm darker area left free where interface text will sit.

OBJEKT-ZUSATZ (für Symbole, Icons, Kacheln):
A single object centred on a plain flat dark background, strong readable silhouette, simple
shapes, bold light-dark contrast, front or slight three-quarter view, generous even padding, no
scene, no ground shadow cast outside the object.
```

**NEG-BASIS** (wörtlich in jeden negativen Prompt):

```text
text, letters, words, numbers, runes, signature, watermark, logo, brand, emoji, photograph,
photorealistic, 3d render, CGI, plastic look, anime, chibi, cartoon, comic outlines, black
outlines, cel shading, flat vector, blurry, out of focus, soft focus, motion blur, jpeg artifacts,
noise, low contrast, washed out, muddy brown, monochrome, frame, border, vignette, user interface,
modern objects, firearms, science fiction, neon, real person, celebrity, portrait close-up,
deformed, duplicated objects
```

**HAUSBLÖCKE** (für alles, was je Fraktion anders ist; nach dem STIL-BLOCK einsetzen).
belegt: data/haeuser.json (Haus, Volk, Welt, Farben, Sitz). Die Architektur ist Vorschlag, aus dem
Namen des Sitzes abgeleitet. Kein Hausblock enthält das Wappenmotiv (Auftrag: "nicht nachbauen").

```text
HAUS-SILBERBACH (Menschen, Midgard, Sitz "Burg Silberbach", Weinrot und Gold):
Human realm of Midgard: grey stone castle walls and timber-framed houses beside a clear silver
river, green meadows, wine-red banners with gold trim, gold-painted wooden details, warm lantern
light. Dominant colours wine red, warm gold, fresh green.

HAUS-HAMMERHALL (Zwerge, Armageddon, Sitz "Tiefenfeste Hammerhall", Nachtblau, Grau und Gold):
Dwarven deep fortress of Armageddon carved into dark grey mountain rock: massive stone halls,
heavy iron doors, glowing forges deep inside, night-blue banners with gold trim, snow on the high
ridges outside. Dominant colours night blue, slate grey, forge orange, gold.

HAUS-STERNENWACHT (Elfen, Valhalla, Sitz "Turmstadt Silberlaub", Dunkelgrün und Gold):
Elven tower city of Valhalla: slender pale stone towers grown together with ancient trees, silver
leaves, waterfalls, dark green banners with gold trim, soft golden light through foliage.
Dominant colours deep green, pale stone, gold, silver leaf.

HAUS-SCHATTENFAUST (Trolle, Utgard, Sitz "Felsfeste Schattenfaust", Violett, Schwarz und Gold):
Troll rock fortress of Utgard built from huge black boulders and rough-hewn beams: crude but
mighty walls, violet banners with gold trim, purple dusk sky, braziers with orange fire.
Dominant colours violet, black rock, ember orange, gold.

HAUS-KNOCHENMOOR (Ghule, Ragnaroek, Sitz "Sumpfzitadelle Knochenmoor", Blau, Silber und Gold):
Ghoul swamp citadel of Ragnaroek: dark stone on misty marsh, bone fences, cages, rope bridges,
blue banners with silver trim, eerie green fires in camps and villages, gloomy and grim.
Dominant colours cold blue, silver, swamp green glow, touches of gold.
(belegt: grüne Feuer und "düster", DESIGN_LIEFERUNG_CHRIS Z. 145-146; Blau/Silber aus
data/haeuser.json. Entscheidung: Z. 145 sagt außerdem "Burg bleibt violett"; die Zuordnung Burg ->
Haus ist laut Auftrag offen, deshalb kommt Violett hier NICHT vor. Wird die Zuordnung anders
entschieden, wird nur dieser Block geändert.)

HAUS-FLICKWERK (Gnome, Limbus, Sitz "schwimmende Insel Flickwerk", Karminrot, Silber und Gold):
Gnome floating island of Limbus drifting in the mist: patchwork houses of mixed timber and riveted
metal plates, cogwheels, brass pipes, small workshops, carmine-red banners with silver trim, warm
forge light. Dominant colours carmine red, silver, brass gold, mist blue.
```

**STANDARD-BLOCK** (fraktionsneutral, für alles unter "Standard" in 1.4):

```text
Neutral realm of the Fog Lake valley: warm dark red-brown wood, old stone, antique gold fittings,
red banners with a light symbol, a misty lake in the distance. Dominant colours deep red-brown
#2a0605 tones, warm gold, ember orange, cool mist blue.
```

### 1.2 PALETTEN (Vorschlag), MIT KONTRAST NACH WCAG 2.x

Rechnung: relative Leuchtdichte nach WCAG 2.x, (L1 + 0,05) / (L2 + 0,05), mit einem Skript
nachgerechnet. Regel: jede Schrift &gt;= 4,5 : 1. Rahmen und Flächen sind keine Schrift; für Rahmen gegen
Grund gilt als Ziel &gt;= 3 : 1 (Nicht-Text-Kontrast, WCAG 1.4.11).

Rollen: Grund = tiefster Ton (Fensterfläche); Fläche = Panel, Kasten; Rahmen = Leisten und 9-Slice-
Kanten; Akzent = aufgehellte Wappentinktur für Titel und aktive Elemente; Gold = Zahlen, Hervorhebung;
Text = Fließtext; Warnung, Erfolg = Statusschrift.

**STANDARD (Tor, Menüleiste, Ressourcenleiste, Dialoge) - aus dem Skin "standard"** (src/main.py
Z. 3862-3875), drei Werte neu:
```text
Grund #2a0605 (Skin)   Fläche #3e1c1a (Skin)   Leiste #1a0a09 (Skin)   Akzent/Gold #FFCC33 (Skin)
Rahmen #b8862e (neu, Vorschlag: zwischen Chris' Rahmengold #C68B42 und Skin-Gold, damit der Rahmen
nicht mit Titelgold konkurriert)
Text #F2E3BF (neu; Skin-Text #FFFF99 hat 14,44 auf Fläche, ist aber in langen Texten grell)
Warnung #ff8a70 (neu; Skin-Rot #e53935 hat auf Grund nur 4,41 und bleibt für Linien und Marker)
Erfolg #a5d67a (neu)
Kontraste: Text/Grund 14,66; Text/Fläche 11,92; Text/Leiste 15,13; Akzent/Grund 12,37;
Akzent/Fläche 10,06; Akzent/Leiste 12,77; Warnung/Grund 8,10; Warnung/Fläche 6,58;
Warnung/Leiste 8,36; Erfolg/Grund 11,09; Erfolg/Fläche 9,02; Erfolg/Leiste 11,45;
Knopfschrift Grund auf Akzent 12,37; Rahmen/Grund 5,76 (Nicht-Text).
```

**HAUS SILBERBACH (Menschen; Tinktur Weinrot, Gold)**
```text
Grund #1c0709  Fläche #3b111a  Rahmen #c9a24a  Akzent #e8667a  Gold #f2c94c  Text #f6e8cf
Warnung #ffa25c  Erfolg #9fd77e
Text/Grund 16,02; Text/Fläche 13,55; Akzent/Grund 6,10; Akzent/Fläche 5,16; Gold/Grund 12,21;
Gold/Fläche 10,33; Warnung/Grund 9,76; Warnung/Fläche 8,25; Erfolg/Grund 11,53; Erfolg/Fläche 9,75;
Knopfschrift Grund auf Akzent 6,10; Rahmen/Grund 8,07.
Warnung ist orange statt rot, damit sie sich vom roten Akzent abhebt.
```

**HAUS HAMMERHALL (Zwerge; Tinktur Nachtblau, Grau, Gold)**
```text
Grund #0b1220  Fläche #1a2638  Rahmen #c9a24a  Akzent #9fb3c8  Gold #e9c46a  Text #eef1f5
Warnung #ff8a70  Erfolg #8fd694
Text/Grund 16,53; Text/Fläche 13,45; Akzent/Grund 8,70; Akzent/Fläche 7,08; Gold/Grund 11,21;
Gold/Fläche 9,12; Warnung/Grund 8,13; Warnung/Fläche 6,62; Erfolg/Grund 10,89; Erfolg/Fläche 8,86;
Knopfschrift Grund auf Akzent 8,70; Rahmen/Grund 7,80.
```

**HAUS STERNENWACHT (Elfen; Tinktur Dunkelgrün, Gold)**
```text
Grund #08160f  Fläche #143222  Rahmen #c9a24a  Akzent #7fcf8f  Gold #e9c46a  Text #eef3e4
Warnung #ff8a70  Erfolg #b5e38a
Text/Grund 16,41; Text/Fläche 12,31; Akzent/Grund 9,92; Akzent/Fläche 7,44; Gold/Grund 11,10;
Gold/Fläche 8,33; Warnung/Grund 8,06; Warnung/Fläche 6,04; Erfolg/Grund 12,65; Erfolg/Fläche 9,49;
Knopfschrift Grund auf Akzent 9,92; Rahmen/Grund 7,73.
Erfolg ist gelbgrün statt grün, damit es sich vom grünen Akzent abhebt.
```

**HAUS SCHATTENFAUST (Trolle; Tinktur Violett, Schwarz, Gold)**
```text
Grund #110a18  Fläche #2a1838  Rahmen #c9a24a  Akzent #c39bea  Gold #e9c46a  Text #f1eaf7
Warnung #ff8a70  Erfolg #8fd694
Text/Grund 16,52; Text/Fläche 13,88; Akzent/Grund 8,51; Akzent/Fläche 7,15; Gold/Grund 11,63;
Gold/Fläche 9,77; Warnung/Grund 8,44; Warnung/Fläche 7,09; Erfolg/Grund 11,30; Erfolg/Fläche 9,50;
Knopfschrift Grund auf Akzent 8,51; Rahmen/Grund 8,10.
```

**HAUS KNOCHENMOOR (Ghule; Tinktur Blau, Silber, Gold)**
```text
Grund #0a1322  Fläche #17283f  Rahmen #b9c3cf (Silber)  Akzent #7fb2ea  Gold #e9c46a
Text #eef2f7  Warnung #ff8a70  Erfolg #8fd694
Text/Grund 16,54; Text/Fläche 13,23; Akzent/Grund 8,38; Akzent/Fläche 6,70; Gold/Grund 11,13;
Gold/Fläche 8,90; Warnung/Grund 8,08; Warnung/Fläche 6,46; Erfolg/Grund 10,82; Erfolg/Fläche 8,65;
Knopfschrift Grund auf Akzent 8,38; Rahmen/Grund 10,42.
Zusatz nur für Bildinhalte (keine Schrift): Ghul-Leuchten #7AAC4D (Chris, gemessen).
```

**HAUS FLICKWERK (Gnome; Tinktur Karminrot, Silber, Gold)**
```text
Grund #1d0608  Fläche #3d0f16  Rahmen #c2c8cf (Silber)  Akzent #ff6b6b  Gold #f2c94c
Text #f7ece4  Warnung #ffb35c  Erfolg #9fd77e
Text/Grund 16,71; Text/Fläche 14,14; Akzent/Grund 7,00; Akzent/Fläche 5,92; Gold/Grund 12,23;
Gold/Fläche 10,35; Warnung/Grund 10,96; Warnung/Fläche 9,27; Erfolg/Grund 11,55; Erfolg/Fläche 9,77;
Knopfschrift Grund auf Akzent 7,00; Rahmen/Grund 11,51.
```

Kein Schrift-Paar liegt unter 4,5 : 1; das schwächste ist Akzent auf Fläche bei Silberbach mit 5,16.

Zwei Paare sind sich ähnlich, weil die Tinkturen es sind (belegt: data/haeuser.json):
- Hammerhall und Knochenmoor sind beide blau (Farbton 211 Grad). Unterschieden werden sie durch die
```text
Sättigung (Hammerhall grau-stählern #9fb3c8, Knochenmoor kräftig #7fb2ea), den Rahmen (Gold gegen
Silber) und das Ghul-Grün in den Bildern.
```
- Silberbach und Flickwerk sind beide rot (351 und 0 Grad). Unterschieden werden sie durch den Ton
```text
(Weinrot ins Violette gegen Karmin), den Rahmen (Gold gegen Silber) und die Architektur.
```

Die Skins "wald" und "feuer" (belegt: src/main.py Z. 3876-3903). Gerechnet:
```text
wald:  Text/Panel 12,88; Gold/Grund 8,21; "red" (#4CAF50, im Skin grün) /Grund 6,20; Subhead/Panel 5,21
feuer: Text/Panel 14,01; Gold/Grund 5,92; "red" (#FF9800)/Grund 8,69;
       Gold #FF5722 auf button_active #D84315 nur 1,40.
Ob das Spiel Gold-Schrift auf button_active zeichnet: weiß ich nicht. Falls ja, ist "feuer" dort unlesbar.
Entscheidung für die Skins: Gemalte Standardteile (T03, T08, T09, T17, T18) werden EINMAL erzeugt, in
neutralem Gold-Bronze auf dunklem Grund. Die Skins färben nur, was der Code zeichnet (Flächen, Schrift,
Ränder um die Bilder). Begründung: drei gemalte Sätze verdreifachen die Arbeit für Skins, deren
Nutzungshäufigkeit ich nicht kenne. Abnahme dafür in 3.1 (A-SKIN).
```

### 1.3 REGELWERK FÜR RAHMEN UND FLÄCHEN

**R-1** Größe und Schärfe (gegen V-1)
- Jedes Bild wird in drei Fassungen geliefert: 100 %, 125 %, 150 % (Faktor 1,0 / 1,25 / 1,5 der Maße aus Teil 2). Das Spiel wählt die Fassung nach der Windows-Skalierung und zeigt sie 1 : 1.
- Vorschlag zum Ablauf: im Generator in der nächstgelegenen Eigengröße erzeugen (SDXL und Flux arbeiten um 1 Megapixel, z. B. 1344 x 768 für 16:9), dann mit einem KI-Detail-Upscaler (nicht bilinear, nicht Lanczos) auf mindestens die 150-%-Fassung, dann daraus auf 125 % und 100 % verkleinern. Nie im Spiel hochskalieren, nie im Spiel weichzeichnen.
- Freistellen: Pollinations, SDXL und Flux liefern in der Grundform kein Alpha. Objekte und Icons darum auf flachem, dunklem Grund erzeugen (OBJEKT-ZUSATZ) und nachträglich freistellen.

**R-2** Ecken
- Panel, Dialog, Kasten: Radius 6 px (100 %). Knopf: 4 px. Icon-Kachel und Gebäudekachel: 10 px.
- Vorschlag, begründet: Chris' Kacheln haben einen "abgerundeten Goldrahmen" (Z. 139); 10 px trägt das bei 256 px, 4-6 px halten Knöpfe und Panels nahe an der kantigen Tk-Oberfläche.

**R-3** Randbreiten (100 %)
- Großer Rahmen (Fenster, Portalkarte, Kaserne): 8 px gemaltes Gold + 2 px dunkle Außenkante (Grund des Hauses). 9-Slice-Ecke 32 x 32.
- Panel/Dialog: 4 px Gold + 1 px dunkle Außenkante. 9-Slice-Ecke 16 x 16.
- Knopf: 2 px Gold. 9-Slice-Ecke 12 x 12.
- Trennlinie: 1 px Rahmenfarbe des Hauses.

**R-4** Rahmen ins Bild oder nicht
- Entscheidung: Rahmen setzt IMMER das Spiel (9-Slice). Kein Bild in Teil 2 hat einen gemalten Rahmen. Begründung: belegt DESIGN_LIEFERUNG_CHRIS Z. 176-177 und Z. 189: zwei Rahmenstile (gemalt im Bild gegen eigener Rahmen) sollen zusammengeführt werden. Ein einziger 9-Slice-Rahmen im Look von Chris' Goldrahmen löst das für alle neuen Bilder.

**R-5** Innenabstand
- Grundmaß 8 px. Panel-Innenabstand 16 px, Dialog 24 px, Knopf 8 x 16 px (senkrecht x waagerecht), Abstand zwischen Kacheln 8 px, zwischen Abschnitten 24 px.

**R-6** Bild unter Text (damit Text lesbar bleibt)
- Jedes Hintergrundbild hat in Teil 2 eine benannte TEXTZONE (z. B. "untere 35 %").
- In der Textzone darf die relative Leuchtdichte im 95. Perzentil höchstens 0,13 betragen. Dann hat der Standardtext #F2E3BF dort mindestens 4,5 : 1 (gerechnet: L(Text) = 0,776; (0,776 + 0,05) / 4,5 - 0,05 = 0,134). Für die Haus-Texte liegt die Grenze etwas höher; 0,13 gilt einheitlich.
- Reicht das Bild selbst nicht, legt das Spiel einen Schleier darunter: Verlauf von 0 auf 72 % Deckkraft in der Farbe "Grund" des Hauses, über 64 px eingeblendet. Kein Weichzeichnen.
- Text nie auf ein Bild ohne Textzone setzen.

**R-7** Tote Fläche
- Daniel: "braunes, flaches Feld ohne Tiefe". Messbar: ein 32 x 32-Block gilt als "tot", wenn seine Helligkeit eine Standardabweichung unter 0,02 und eine mittlere Sättigung unter 0,15 hat (Werte 0-1). Grenzen je Bildart in 3.1.

### 1.4 STANDARD ODER JE FRAKTION

Wie im Auftrag, mit drei Entscheidungen:

```text
STANDARD (ein Satz für alle Häuser)
  Tor/Hauptmenü (T01), linke Menüleiste (T09), Ressourcenleiste (T08), Dialoge, Knöpfe (T17),
  Statusleisten (T18), Kopfbänder der neutralen Ansichten (T03), Forschung (T11), Gildenhalle (T15),
  Schlachtsimulator (T16), Sieg/Niederlage (T19), Feldmarkierungen und Einheitenfiguren (T07-F, T07-E),
  Geländekacheln der Weltkarte (T05-G).
JE FRAKTION (sechs Fassungen)
  Ladebild (T02), Dorfansicht/Gebäudehintergründe (T04), Kartenrahmen (T05-R), Portal (T06),
  Kaserne/Angriffsfläche (T07-K), Plakettengrund (T07-P), Kampfbericht-Kopf (T12-K),
  Marktplatz (T13), Ruhmeshalle (T14).

Entscheidung 1: Forschung, Gildenhalle und Schlachtsimulator stehen im Auftrag in keiner der zwei
  Listen. Sie werden Standard, weil sie keinen Ort des Hauses zeigen.
Entscheidung 2: Kopfbänder (T03) der Hausansichten werden NICHT eigens erzeugt, sondern aus dem
  Hintergrund dieser Ansicht oben herausgeschnitten (gleiche Malerei, kein Bruch, keine Extra-Arbeit).
Entscheidung 3: Einheitenfiguren sind Standard. belegt: data/units.json führt EINE Liste mit 28
  Einheiten für alle Häuser. Ob Einheiten je Haus anders aussehen sollen: weiß ich nicht. Daniels
  Wunsch nach "Kampfreihen in einer Kaserne" erfüllt T07-K je Haus.
```

## TEIL 2 - INVENTARLISTE

Spalten: ID | Ort im Spiel | Dateiname-Vorschlag | Maße in px (100 %) | Zweck | NICHT drauf |
Prompt (englisch) | negativer Prompt

Kürzel in den Prompts:
```text
[STIL] = STIL-BLOCK, [SZENE] = SZENEN-ZUSATZ, [OBJEKT] = OBJEKT-ZUSATZ, [STANDARD] = STANDARD-BLOCK,
[HAUS] = der Hausblock der jeweiligen Fassung, [NEG] = NEG-BASIS.
```
Platzhalter: {haus} im Dateinamen = silberbach, hammerhall, sternenwacht, schattenfaust, knochenmoor,
```text
flickwerk. Eine Zeile mit {haus} steht für SECHS Bilder.
```
Dateinamen: Vorschlag, Endung .png (Pillow liest PNG im Spiel; belegt src/gebaeude_optik.py Z. 54).
```text
Fassungen: Endung _100, _125, _150 vor .png.
```
Für jede Zeile gilt zusätzlich: keine Schrift, keine Emojis, kein Wasserzeichen, kein gemalter Rahmen
```text
(R-4), kein Wappenmotiv eines Hauses (Krone/Lilie, Turm vor Gipfeln, Hirschkopf, Rabe vor Mond,
Wolfskopf, gekreuzte Schwerter mit Stern; belegt data/haeuser.json "wappen_kurz").
```

#### T01 TOR / STARTBILD (Standard)

| ID | Ort im Spiel | Dateiname-Vorschlag | Maße (100 %) | Zweck | NICHT drauf | Prompt (englisch) | negativer Prompt |
|---|---|---|---|---|---|---|---|
| T01 | Passworttor, erster Bildschirm | `t01_tor` | 1600 x 900 | Schwelle ins Spiel; trägt später das Logo und das Passwortfeld | Logo, Schrift, Torwächter mit Gesicht, Burg eines bestimmten Hauses | [STIL] [SZENE] [STANDARD] A massive closed gate of dark timber and iron set into an old stone arch at the edge of the Fog Lake, two fire bowls burning on either side, mist rolling over the water behind. The upper middle third stays calm dark sky with soft mist for the logo, the lower middle stays darker stone for an input field. | [NEG], open gate, people, castle of a specific faction, sunset glare |

#### T02 LADEBILD (je Haus)

| ID | Ort im Spiel | Dateiname-Vorschlag | Maße (100 %) | Zweck | NICHT drauf | Prompt (englisch) | negativer Prompt |
|---|---|---|---|---|---|---|---|
| T02 | Ladebildschirm nach der Hauswahl | `t02_laden_{haus}` | 1600 x 900 | zeigt beim Laden die Heimat des gewählten Hauses | Schrift, Ladebalken, Wappen, Gesichter | [STIL] [SZENE] [HAUS] A wide view of the house seat at dawn seen from a hill path, a wayside lantern in the foreground, the settlement and its banners in the middle distance, mist filling the valley. Lower 25 percent is a dark calm hillside where the loading bar will sit. | [NEG], crest, coat of arms, heraldic animal, people in foreground |

#### T03 KOPFBÄNDER (Standard für neutrale Ansichten; Hausansichten: Ausschnitt aus deren Hintergrund)

Maß: 1920 x 150 (100 %). Entscheidung: Das Fenster ist höchstens 1560 px breit (belegt src/main.py
Z. 8419-8420, min(1560, Bildschirmbreite - 90)); 1920 gibt Reserve. Das Spiel schneidet mittig zu,
darum muss die Mitte (1024 px) das Motiv tragen, die Ränder laufen ruhig aus.

| ID | Ort im Spiel | Dateiname-Vorschlag | Maße (100 %) | Zweck | NICHT drauf | Prompt (englisch) | negativer Prompt |
|---|---|---|---|---|---|---|---|
| T03-01 | Kopf Gildenhalle | `t03_kopf_gildenhalle` | 1920 x 150 | Kopf der Ansicht | Schrift, Personen | [STIL] [STANDARD] A very wide horizontal strip of a long wooden guild hall interior, rows of hanging red banners with light symbols, warm lantern light in the centre fading to dark wood at both ends. | [NEG], tall composition, people |
| T03-02 | Kopf Nachrichten | `t03_kopf_nachrichten` | 1920 x 150 | Kopf der Ansicht | Schrift auf Papier, Siegel mit Zeichen | [STIL] [STANDARD] A very wide horizontal strip of a writing desk seen from above: sealed letters, a quill, wax, a lantern in the centre, dark wood fading at both ends. | [NEG], readable writing, letters on paper |
| T03-03 | Kopf Diplomatie | `t03_kopf_diplomatie` | 1920 x 150 | Kopf der Ansicht | Flaggen echter Länder, Gesichter | [STIL] [STANDARD] A very wide horizontal strip of a long negotiation table with six plain banners in wine red, night blue, dark green, violet, blue and carmine hanging above, candles in the centre. | [NEG], flags of real countries, faces |
| T03-04 | Kopf Einstellungen | `t03_kopf_einstellungen` | 1920 x 150 | Kopf der Ansicht | Zahnräder einer echten Marke, Technik | [STIL] [STANDARD] A very wide horizontal strip of a craftsman's workbench with brass tools, a small brass mechanism and an oil lamp in the centre, dark wood fading at both ends. | [NEG], modern tools, screws, electronics |
| T03-05 | Kopf Anleitung | `t03_kopf_anleitung` | 1920 x 150 | Kopf der Ansicht | lesbare Schrift in Büchern | [STIL] [STANDARD] A very wide horizontal strip of an old open book lying on a lectern beside a lantern, pages blank and glowing, dark library shelves fading at both ends. | [NEG], readable text on pages |
| T03-06 | Kopf Schlachtsimulator | `t03_kopf_simulator` | 1920 x 150 | Kopf der Ansicht | Schachfiguren, echte Spiele | [STIL] [STANDARD] A very wide horizontal strip of a sand table with small carved wooden army markers and painted hills, lit by a lantern in the centre. | [NEG], chess pieces, board game brand |
| T03-07 | Kopf Forschung | `t03_kopf_forschung` | 1920 x 150 | Kopf der Ansicht | Schrift auf Buchrücken | [STIL] [STANDARD] A very wide horizontal strip of tall bookshelves with leather spines, scrolls and a glowing blue-violet mana crystal in the centre. | [NEG], titles on book spines |
| T03-08 | Kopf Stellmacher | `t03_kopf_stellmacher` | 1920 x 150 | Kopf der Ansicht | Personen | [STIL] [STANDARD] A very wide horizontal strip of a wheelwright's workshop with large wooden wheels, axles and a half-built cart in warm light. | [NEG], people |
| T03-09 | Kopf Diebesgilde | `t03_kopf_diebesgilde` | 1920 x 150 | Kopf der Ansicht | Gesichter, Waffen gegen Personen | [STIL] [STANDARD] A very wide horizontal strip of a dim cellar with hooded cloaks on hooks, lockpicks on a cloth, a single candle in the centre, deep shadows at both ends. | [NEG], faces, violence |
| T03-10 | Kopf Voraussetzungen und Neuigkeiten | `t03_kopf_aushang` | 1920 x 150 | Kopf beider Ansichten | lesbare Aushänge | [STIL] [STANDARD] A very wide horizontal strip of a wooden notice board under a small roof with pinned blank parchments and a lantern, mist behind. | [NEG], readable notices |

Hausansichten (Dorfzentrum, Portal, Kaserne, Marktplatz, Ruhmeshalle, Kampfbericht): kein eigenes Band,
oberer Ausschnitt 1920 x 150 aus T04, T06, T07-K, T13, T14, T12-K. Darum haben diese Bilder oben eine
ruhige, aber bemalte Zone (siehe dort).

#### T04 DORFANSICHT / GEBÄUDEHINTERGRUND (je Haus, je Gebäude: 20 x 6 = 120 Bilder)

Maß: 1152 x 1120 (100 %). Entscheidung: belegt src/gebaeude_optik.py Z. 105: die Fläche misst 1142 x
1120; aufgerundet auf ein Vielfaches von 8 in der Breite. Ein Bild füllt die ganze Fläche, kein
Spiegelgrund mehr. Zusatznutzen: die Gebäudekachel 256 x 256 (Lager, Baumenü) ist der mittige
quadratische Ausschnitt dieses Bildes (Abnahme in 3.1, A-T04).
Komposition für alle T04: Gebäude im oberen Bildteil (obere 55 %), ganz im Bild, mittig; die unteren
40 % sind dunkler Boden oder Vorplatz = TEXTZONE; das obere Bildende (150 px) ist ruhiger Himmel oder
Nebel = Kopfband-Ausschnitt.
Symbole auf den Bannern: belegt Chris Z. 142-145 (Turm, Hämmer/Hacken, Äxte, Ähre, Schaf, Stierkopf,
Pfote, Kreuz, Geldsack, Auge); mit "Vorschlag" markierte Symbole sind von mir.

| ID | Ort im Spiel | Dateiname-Vorschlag | Maße (100 %) | Zweck | NICHT drauf | Prompt (englisch) | negativer Prompt |
|---|---|---|---|---|---|---|---|
| T04-01 | Dorfansicht Holzfäller | `t04_holzfaeller_{haus}` | 1152 x 1120 | Hintergrund des Gebäudemenüs | Personen beim Fällen, Wappen | [STIL] [SZENE] [HAUS] A woodcutter's shed with stacked logs, a chopping block and a hand cart, a hanging banner with a light crossed-axes symbol, forest edge behind. | [NEG], people, crest |
| T04-02 | Dorfansicht Steinmetz | `t04_steinmetz_{haus}` | 1152 x 1120 | wie oben | Wappen | [STIL] [SZENE] [HAUS] A stone quarry with a wooden crane, cut stone blocks and chisels, a hanging banner with a light crossed-pickaxes symbol. | [NEG], people, crest |
| T04-03 | Dorfansicht Erzmine | `t04_erzmine_{haus}` | 1152 x 1120 | wie oben | Skelette außer bei knochenmoor | [STIL] [SZENE] [HAUS] A mine entrance braced with heavy beams, an ore cart on rails, lanterns inside the tunnel, a hanging banner with a light crossed-hammers symbol. | [NEG], people, crest |
| T04-04 | Dorfansicht Tempel | `t04_tempel_{haus}` | 1152 x 1120 | wie oben | religiöse Symbole echter Religionen außer dem schlichten Kreuz aus Chris' Regel | [STIL] [SZENE] [HAUS] A small stone temple beside a misty lake shore, glowing blue-violet mist rising from the water, a hanging banner with a simple light cross symbol. | [NEG], people, crest, real religious icons |
| T04-05 | Dorfansicht Farm | `t04_farm_{haus}` | 1152 x 1120 | wie oben | Wappen | [STIL] [SZENE] [HAUS] A farmhouse with a golden wheat field, sheaves and a windmill, a hanging banner with a light wheat-ear symbol. | [NEG], people, crest |
| T04-06 | Dorfansicht Goldmine | `t04_goldmine_{haus}` | 1152 x 1120 | wie oben | Münzen mit Prägung | [STIL] [SZENE] [HAUS] A narrow mine entrance in yellow rock with a sluice and baskets of glittering ore, a hanging banner with a light coin symbol (Vorschlag). | [NEG], people, crest, minted text |
| T04-07 | Dorfansicht Schafszucht | `t04_schafszucht_{haus}` | 1152 x 1120 | wie oben | Wappen | [STIL] [SZENE] [HAUS] A sheep stable with a fenced pen, woolly sheep and a wool cart, a hanging banner with a light sheep symbol. | [NEG], people, crest |
| T04-08 | Dorfansicht Rinderfarm | `t04_rinderfarm_{haus}` | 1152 x 1120 | wie oben | Wappen | [STIL] [SZENE] [HAUS] A cattle barn with a cow at a trough and stacked hides, a hanging banner with a light bull-head symbol. | [NEG], people, crest |
| T04-09 | Dorfansicht Pferdezucht | `t04_pferdezucht_{haus}` | 1152 x 1120 | wie oben | Reiter | [STIL] [SZENE] [HAUS] A horse stable with paddock, two horses and saddles on a rail, a hanging banner with a light horseshoe symbol (Vorschlag). | [NEG], riders, people, crest |
| T04-10 | Dorfansicht Jäger | `t04_jaeger_{haus}` | 1152 x 1120 | wie oben | getötete Tiere im Vordergrund | [STIL] [SZENE] [HAUS] A hunter's lodge with antlers over the door, bows on the wall and drying furs, a hanging banner with a light paw symbol. | [NEG], people, crest, gore |
| T04-11 | Dorfansicht Schmiede | `t04_schmiede_{haus}` | 1152 x 1120 | wie oben | Wappen | [STIL] [SZENE] [HAUS] An open smithy with a glowing forge, anvil and racks of tools, a hanging banner with a light anvil symbol (Vorschlag). | [NEG], people, crest |
| T04-12 | Dorfansicht Bogenbauer | `t04_bogenbauer_{haus}` | 1152 x 1120 | wie oben | Wappen | [STIL] [SZENE] [HAUS] A bowyer's workshop with bow staves drying under the eaves and bundles of arrows, a hanging banner with a light bow symbol (Vorschlag). | [NEG], people, crest |
| T04-13 | Dorfansicht Nähstube | `t04_naehstube_{haus}` | 1152 x 1120 | wie oben | Wappen | [STIL] [SZENE] [HAUS] A tailor's house with bolts of dyed cloth, a loom by the window and leather pieces, a hanging banner with a light needle-and-thread symbol (Vorschlag). | [NEG], people, crest |
| T04-14 | Dorfansicht Kriegerakademie | `t04_kriegerakademie_{haus}` | 1152 x 1120 | wie oben | gekreuzte Schwerter (Gnomenwappen) | [STIL] [SZENE] [HAUS] A training yard with straw dummies, weapon racks and a stone hall behind, a hanging banner with a light helmet symbol (Vorschlag). | [NEG], people, crest, crossed swords |
| T04-15 | Dorfansicht Diebesgilde | `t04_diebesgilde_{haus}` | 1152 x 1120 | wie oben | Gesichter | [STIL] [SZENE] [HAUS] A crooked house in a dark alley with shuttered windows, a single lantern and a cellar door, a hanging banner with a light key symbol (Vorschlag). | [NEG], people, faces, crest |
| T04-16 | Dorfansicht Stellmacher | `t04_stellmacher_{haus}` | 1152 x 1120 | wie oben | Wappen | [STIL] [SZENE] [HAUS] A wheelwright's workshop with large wooden wheels leaning on the wall and a half-built wagon, a hanging banner with a light wagon-wheel symbol (Vorschlag). | [NEG], people, crest |
| T04-17 | Dorfansicht Verteidigungswall | `t04_wall_{haus}` | 1152 x 1120 | wie oben | Kampfszene | [STIL] [SZENE] [HAUS] A defensive wall with a gate and a watchtower, braziers on the parapet, a hanging banner with a light tower symbol. | [NEG], battle, people, crest |
| T04-18 | Dorfansicht Bibliothek | `t04_bibliothek_{haus}` | 1152 x 1120 | wie oben | lesbare Schrift | [STIL] [SZENE] [HAUS] A library building with tall arched windows glowing warmly, stacks of books visible inside, a hanging banner with a light open-book symbol (Vorschlag). | [NEG], readable text, people, crest |
| T04-19 | Dorfansicht Haus | `t04_haus_{haus}` | 1152 x 1120 | wie oben | Personen | [STIL] [SZENE] [HAUS] A cosy dwelling house typical for the realm with smoke from the chimney, firewood and a bench by the door, a hanging banner with a light house-gable symbol (Vorschlag). | [NEG], people, crest |
| T04-20 | Dorfansicht Dorfzentrum | `t04_dorfzentrum_{haus}` | 1152 x 1120 | wie oben; zugleich Bild der Ansicht "Dorfzentrum" | Wappen, Burg eines anderen Hauses | [STIL] [SZENE] [HAUS] A village square with a well and a market cross, the main hall of the settlement behind it, banners in the house colours, a hanging banner with a light bell symbol (Vorschlag). | [NEG], people, crest |

#### T05 KARTE

| ID | Ort im Spiel | Dateiname-Vorschlag | Maße (100 %) | Zweck | NICHT drauf | Prompt (englisch) | negativer Prompt |
|---|---|---|---|---|---|---|---|
| T05-R | Kartenrahmen Weltkarte | `t05_rahmen_{haus}` | 192 x 192 (9-Slice: Ecken 32 x 32, Kanten kachelbar) | gemalter Rahmen um die Weltkarte | Motive in den Kanten, die sich beim Kacheln wiederholen | [STIL] [OBJEKT] [HAUS] A square ornamental frame of antique metal in the house colours, rounded inner corners, a dark outer edge, the middle completely empty and flat dark, the four edges straight and evenly patterned so they can tile. | [NEG], picture inside frame, uneven edges, perspective |
| T05-G1 | Weltkarte Grasland | `t05_feld_grasland` | 64 x 64 (Master 128) | Geländekachel, nahtlos | Häuser, Wege | [STIL] Seamless top-down tile of lush meadow grass with small flowers, painted, even lighting. | [NEG], perspective, horizon, objects, seams |
| T05-G2 | Weltkarte Steppe | `t05_feld_steppe` | 64 x 64 | Geländekachel | Häuser | [STIL] Seamless top-down tile of dry golden steppe grass with sandy patches, even lighting. | [NEG], perspective, horizon, objects, seams |
| T05-G3 | Weltkarte Wald | `t05_feld_wald` | 64 x 64 | Geländekachel | einzelne große Bäume | [STIL] Seamless top-down tile of dense dark pine forest canopy, small evenly spaced crowns. | [NEG], perspective, horizon, single big tree, seams |
| T05-G4 | Weltkarte Hügel | `t05_feld_huegel` | 64 x 64 | Geländekachel | Häuser | [STIL] Seamless top-down tile of rolling green-brown hills with soft painted shading. | [NEG], perspective, horizon, seams |
| T05-G5 | Weltkarte Berg | `t05_feld_berg` | 64 x 64 | Geländekachel | Gipfel über den Kachelrand | [STIL] Seamless top-down tile of grey rocky mountain ground with small snow patches. | [NEG], perspective, horizon, seams |
| T05-G6 | Weltkarte Nebelsee | `t05_feld_nebelsee` | 64 x 64 | Geländekachel | Boote | [STIL] Seamless top-down tile of dark blue water covered by drifting pale blue-violet mist. | [NEG], perspective, horizon, boats, seams |
| T05-G7 | Weltkarte Sumpf | `t05_feld_sumpf` | 64 x 64 | Geländekachel | Knochen | [STIL] Seamless top-down tile of murky green swamp with reeds and small pools. | [NEG], perspective, horizon, bones, seams |

(belegt: sieben Geländearten, data/gelaende.json. Entscheidung: Geländekacheln Standard, nur der Rahmen
je Haus. Belegt docs/design/DESIGN_ARBEITSWEISE.md Z. 58-59 und DESIGN_LIEFERUNG_CHRIS Z. 187: Karten-Umbau
"auf Chris' Farben und Tannen" ist ein eigener Schnitt nach D-5; diese Zeilen sind dafür gedacht.)

#### T06 PORTAL

| ID | Ort im Spiel | Dateiname-Vorschlag | Maße (100 %) | Zweck | NICHT drauf | Prompt (englisch) | negativer Prompt |
|---|---|---|---|---|---|---|---|
| T06-H | Portal, Hintergrund um die Karte | `t06_portal_{haus}` | 1600 x 900 | Rahmenbild, in dessen Mitte die Weltkarte liegt; Daniel: Karte "in die mitte", "die angaben drumherum gestaltet" | Karte oder Felder im Bild, Schrift | [STIL] [SZENE] [HAUS] A grand portal chamber of the house seen from the front: a tall stone archway with a swirling blue-violet mist portal fills the centre, painted pillars, banners and braziers frame the left and right sides. The centre 60 percent of the width is a dark calm misty area for the map, the left and right 20 percent hold the painted details. | [NEG], map, grid, people, crest |
| T06-W | Weltenliste, Medaillon je Welt | `t06_welt_{welt} (midgard, armageddon, valhalla, utgard, ragnaroek, limbus)` | 160 x 160 | Eintrag der Welt in der Liste | Schrift, Wappen | [STIL] [OBJEKT] A round painted medallion showing a small floating fragment of land in mist, landscape of {welt}: Midgard green meadows and river / Armageddon dark mountains with forge glow / Valhalla tower city among great trees / Utgard black boulders under violet dusk / Ragnaroek misty marsh with green fires / Limbus a patchwork floating island. | [NEG], crest, letters, frame ring with text |

(Die Welt-Hausbindung ist belegt: data/haeuser.json "welt". Je Medaillon nur den Satzteil der Welt verwenden.)

#### T07 ANGRIFFSFLÄCHE

| ID | Ort im Spiel | Dateiname-Vorschlag | Maße (100 %) | Zweck | NICHT drauf | Prompt (englisch) | negativer Prompt |
|---|---|---|---|---|---|---|---|
| T07-K | Kaserne / Angriffsfläche Hintergrund | `t07_kaserne_{haus}` | 1280 x 720 | Daniel: "kampfreihen in einer Kaserne ... mit den kräftigen farben"; darauf liegen Dörfer/Bots als Marker | Gesichter im Vordergrund, Wappen, Blut | [STIL] [SZENE] [HAUS] Wide interior of the house barracks: rows of soldiers of this people in tabards of the house colours stand in formation along both side walls and in the back, weapons raised, shafts of warm light from tall windows. The central area is an open dark stone floor with a large painted campaign table, kept calm for markers. | [NEG], close-up faces, blood, gore, crest, crowded centre |

Zusätze für T07-K je Haus (Vorschlag; Satz an den Prompt hängen):
```text
silberbach: human soldiers in wine-red tabards over mail, spears and shields.
hammerhall: stout dwarf warriors in night-blue tabards over heavy plate, axes and hammers.
sternenwacht: slender elf archers and spearmen in dark-green tabards, longbows, silver-leaf armour.
schattenfaust: huge troll warriors in violet rags over crude plates, clubs and boulders.
knochenmoor: gaunt ghoul warriors in blue-and-silver rags, bone weapons, green fire in braziers.
flickwerk: compact gnome soldiers in carmine tabards over silver-grey mail, geared war hammers.
(Gnome deckungsgleich mit Hermes' Paket PROMPT_GNOM_KRIEGER_20261112.txt, Abschnitt C.)
```

| ID | Ort im Spiel | Dateiname-Vorschlag | Maße (100 %) | Zweck | NICHT drauf | Prompt (englisch) | negativer Prompt |
|---|---|---|---|---|---|---|---|
| T07-F | Feldmarkierungen | `t07_marker_eigen / _bot / _ziel / _gesperrt` | 96 x 96 je Zustand (Master: ein Bogen 2 x 2) | Dörfer und Bots groß und klar erkennbar (Daniel: "ich erkenne kaum die dörfer oder bots") | Wappenbilder (die legt das Spiel aus assets/icons/wappen/ darauf), Schrift | [STIL] [OBJEKT] A 2x2 sheet of four round bronze map tokens on dark background: one with a bright gold ring, one with a red ring, one with a glowing orange target ring, one dull grey and cracked. Each token has an empty dark centre. | [NEG], symbols in the centre, crest, letters |
| T07-P | Plakettengrund je Haus | `t07_plakette_{haus}` | 128 x 128 | Grund, auf dem eine Einheitenfigur steht | Figur, Wappen | [STIL] [OBJEKT] [HAUS] An empty round medallion plate in the house colours with a raised metal rim, dark centre with subtle texture. | [NEG], figure, crest, letters |
| T07-E1 bis T07-E7 | Einheitenfiguren (Standard), 7 Bögen à 4 | `t07_einheit_<name>` | 128 x 128 je Figur | Figur auf der Plakette, bei 64 px erkennbar | Gesichter im Detail, Wappen | [STIL] [OBJEKT] A 2x2 sheet of four full-figure fantasy units on dark background, each in a neutral red-brown and gold outfit, clear silhouettes: &lt;vier Namen aus der Liste unten&gt;. | [NEG], detailed faces, crest, background scenery |

```text
Bögen (belegt: data/units.json, 28 Einheiten):
E1 militia man with pitchfork / fighter with short sword / warrior with axe and shield / knight in plate
E2 paladin with mace and glowing shield / short-bow archer / archer / longbow archer
E3 crossbowman / rogue in hooded cloak / swindler with dagger / thief with lockpicks
E4 master thief / scout with horn / ranger with bow and cloak / hand cart
E5 one-horse cart / two-horse cart / trade caravan / large trade caravan
E6 settler cart with bundles / siege tower / battering ram / large siege tower
E7 large battering ram / ballista / catapult / large catapult
(Reihenfolge wie units.json: Bürgerwehr, Kämpfer, Krieger, Ritter, Paladin, Kurzbogenschütze,
Bogenschütze, Langbogenschütze, Armbrustschütze, Streuner, Gauner, Dieb, Meisterdieb, Kundschafter,
Waldläufer, Handkarren, Einspänner, Zweispänner, Handelskarawane, Große Handelskarawane,
Siedlerkarren, Belagerungsturm, Ramme, Großer Belagerungsturm, Große Ramme, Balliste, Katapult,
Großes Katapult. "Streuner" als "rogue" ist meine Übersetzung.)
```

#### T08 RESSOURCENLEISTE (Standard)

belegt: assets/icons/leiste/ressourcenleiste.png 1440 x 140, Symbole 96 x 96 für acht Werte (erz, gold,
holz, mana, nahrung, punkte, siedler, stein); es fehlen Wolle, Leder, Pferde. src/main.py Z. 9362 nennt
"acht Zahlenfeldern". Daniel: "total hässlich, der stil ist jetzt komplett weg".
Entscheidung: Das Band wird ohne Fächer gemalt; die elf Fächer setzt das Spiel als 11 gleiche Kopien
von T08-F darauf. Begründung: Bild-KIs zählen unzuverlässig; elf gleich breite Fächer im Bild wären
Glückssache.

| ID | Ort im Spiel | Dateiname-Vorschlag | Maße (100 %) | Zweck | NICHT drauf | Prompt (englisch) | negativer Prompt |
|---|---|---|---|---|---|---|---|
| T08-B | Ressourcenleiste, Band | `t08_band` | 1920 x 96 | gemalter Grund der Leiste oben | Fächer, Zahlen, Symbole | [STIL] [STANDARD] A very wide horizontal carved wooden beam with antique gold fittings and rivets along the top and bottom edge, warm lantern light in the middle fading to darker wood at both ends, evenly patterned so the ends can be cropped. | [NEG], compartments, icons, numbers, perspective |
| T08-F | Ressourcenleiste, Fach | `t08_fach` | 160 x 72 (9-Slice, Ecken 12) | ein Fach für Symbol und Zahl | Symbol, Zahl | [STIL] [OBJEKT] A small recessed panel of dark polished wood with a thin antique gold rim and rounded corners, the inside flat and dark for a number. | [NEG], symbol, number, perspective |
| T08-S | Ressourcensymbole, ein Bogen | `t08_sym_<name> (holz, stein, metall, mana, nahrung, gold, wolle, leder, pferde, siedler, punkte)` | 32 x 32 (Master 512 je Zelle, Bogen 4 x 3) | Symbol im Fach; bei 32 px erkennbar | Schrift, Hintergrund, Schatten außerhalb | [STIL] [OBJEKT] A 4x3 sheet of eleven bold game resource icons on flat dark background, each centred in its cell with equal padding, same lighting and same size: stack of logs, cut stone blocks, iron ingots, glowing blue-violet mist in a glass vial, loaf of bread with wheat, pile of gold coins, skein of wool, rolled leather hide, horse head in profile, small settler hand cart with a bundle, golden laurel wreath around a star; the twelfth cell empty. | [NEG], minted letters on coins, background scene, tiny details, thin lines |

(Mana-Motiv: Vorschlag. belegt docs/design/DESIGN_ARBEITSWEISE.md Z. 60: Tempel liefert Mana auf
Nebelsee - daher Nebel im Glas.)

#### T09 MENÜ-ICONS LINKS (Standard)

Daniel: "relativ gut aber leider sind sie verschoben". Die Ursache im Bild: ungleicher Rand. Darum für
alle Icons derselbe Bogen, dieselbe Zelle, dieselbe Polsterung (Abnahme A-T09).
Entscheidung zur Anzahl (V-3): Bogen A = 9 Kern-Icons (Punkte ohne Baubedingung), Bogen B = 10 weitere.
Symbole: Chris' System wo es passt (Geldsack = Handel, Auge = Weltensicht, Turm = Verteidigung), sonst
Vorschlag.

| ID | Ort im Spiel | Dateiname-Vorschlag | Maße (100 %) | Zweck | NICHT drauf | Prompt (englisch) | negativer Prompt |
|---|---|---|---|---|---|---|---|
| T09-A | Menü-Icons Kernsatz | `t09_<punkt> (dorfzentrum, marktplatz, gildenhalle, nachrichten, portal, diplomatie, ruhmeshalle, anleitung, einstellungen)` | 32 x 32 (Master 512 je Zelle, Bogen 3 x 3) | Menüpunkt links | Schrift, Hintergrund | [STIL] [OBJEKT] A 3x3 sheet of nine bold menu icons in antique gold and warm colours on flat dark background, identical size and padding: village well with roof, money sack, guild banner on a pole, sealed letter, swirling portal with an eye, two hands shaking, golden goblet, open book, brass gear. | [NEG], letters, thin lines, background scene, uneven sizes |
| T09-B | Menü-Icons zweite Welle | `t09_<punkt> (kaserne, forschung, stellmacher, diebesgilde, simulator, voraussetzungen, neuigkeiten, gesperrt, ebene_uebersicht, ebene_siedlung)` | 32 x 32 (Master 512 je Zelle, Bogen 5 x 2) | weitere Menüpunkte und Ebenen-Umschalter | Schrift, gekreuzte Schwerter | [STIL] [OBJEKT] A 5x2 sheet of ten bold menu icons in antique gold and warm colours on flat dark background, identical size and padding: helmet, glowing crystal on a book, wagon wheel, key with hood, wooden army marker on a hill, checklist scroll without writing, bell, padlock, small map with compass, small house with fence. | [NEG], letters, thin lines, background scene, crossed swords |

("gesperrt" dient Forum, Chat und "Spieler werben"; belegt src/main.py Z. 15831: "Forum ist offline.")

#### T10 LAGER

| ID | Ort im Spiel | Dateiname-Vorschlag | Maße (100 %) | Zweck | NICHT drauf | Prompt (englisch) | negativer Prompt |
|---|---|---|---|---|---|---|---|
| T10-K | Lagerkachel, Grund | `t10_kachel` | 96 x 96 (9-Slice, Ecken 10) | Grund jeder Lagerkachel; darauf das T08-Symbol in 64 px | Symbol | [STIL] [OBJEKT] [STANDARD] A small square wooden crate lid with a rounded antique gold rim, the centre flat and dark for an icon. | [NEG], icon, letters |

Rohstoffkacheln = T10-K + T08-S (Master verkleinert auf 64). Gebäudekacheln = mittiger Ausschnitt
aus T04 (256 x 256). Keine eigenen Bilder.

#### T11 FORSCHUNG (Standard)

| ID | Ort im Spiel | Dateiname-Vorschlag | Maße (100 %) | Zweck | NICHT drauf | Prompt (englisch) | negativer Prompt |
|---|---|---|---|---|---|---|---|
| T11-H | Forschung, Regal-Hintergrund | `t11_regal` | 1280 x 720 | Hintergrund der Ansicht | Schrift auf Buchrücken | [STIL] [SZENE] [STANDARD] A tall library wall of dark wooden shelves with leather-bound books and scrolls, a reading desk with a glowing blue-violet crystal in the foreground; the middle 50 percent of the shelves stays darker and less detailed for the research list. | [NEG], readable titles, people |
| T11-R | Buchrücken | `t11_ruecken_<zustand> (erforscht, laufend, gesperrt)` | 48 x 192 (Bogen 3 x 1) | ein Eintrag der Forschungsliste | Schrift, Zahlen | [STIL] [OBJEKT] A 3x1 sheet of three upright blank book spines: deep red leather with bright gold bands, the same with warm glowing edges, the same faded grey and dusty. | [NEG], titles, letters, numbers |
| T11-F | Fortschrittsband | `t11_fortschritt` | 256 x 24 (9-Slice, Ecken 8) | Rinne und Füllung für Forschung | Zahlen | [STIL] [OBJEKT] A horizontal empty groove of dark wood with a thin gold rim, and below it a separate glowing amber liquid fill strip of the same size. | [NEG], numbers, percent sign |

#### T12 KAMPFBERICHT

| ID | Ort im Spiel | Dateiname-Vorschlag | Maße (100 %) | Zweck | NICHT drauf | Prompt (englisch) | negativer Prompt |
|---|---|---|---|---|---|---|---|
| T12-K | Bericht-Kopf je Haus | `t12_kopf_{haus}` | 1200 x 150 | Kopf eines Kampfberichts | Schrift, Leichen | [STIL] [HAUS] A very wide strip of a battlefield after combat in the realm of the house: smoke, broken shields, banners in the house colours still standing, warm sunset light in the centre. | [NEG], corpses, blood, gore, crest |
| T12-S | Siegel Sieg | `t12_sieg` | 192 x 192 | Zeichen "Sieg" | Schrift | [STIL] [OBJEKT] A large gold wax seal with a laurel wreath, glowing warm. | [NEG], letters, crest |
| T12-N | Siegel Niederlage | `t12_niederlage` | 192 x 192 | Zeichen "Niederlage" | Schrift, Totenkopf | [STIL] [OBJEKT] A cracked dark red wax seal with a broken laurel wreath, dull light. | [NEG], letters, skull |
| T12-B | Beutezeile | `t12_beute` | 512 x 48 (9-Slice, Ecken 12) | Zeile für Beute (Symbole und Zahlen setzt das Spiel) | Symbole, Zahlen | [STIL] [OBJEKT] A long low wooden tray with a gold rim and rounded corners, inside dark and empty. | [NEG], objects inside, numbers |

#### T13 MARKTPLATZ (je Haus)

| ID | Ort im Spiel | Dateiname-Vorschlag | Maße (100 %) | Zweck | NICHT drauf | Prompt (englisch) | negativer Prompt |
|---|---|---|---|---|---|---|---|
| T13 | Marktplatz Hintergrund | `t13_markt_{haus}` | 1280 x 720 | Hintergrund der Handelsansicht | Schrift, Preisschilder, Gesichter | [STIL] [SZENE] [HAUS] A busy market square of the house with striped awnings, crates, sacks of grain, wool bales, barrels and a weighing scale, banners in the house colours; lower 40 percent is darker cobblestone for the trade table. | [NEG], price tags, letters, faces, crest |

#### T14 RUHMESHALLE (je Haus)

| ID | Ort im Spiel | Dateiname-Vorschlag | Maße (100 %) | Zweck | NICHT drauf | Prompt (englisch) | negativer Prompt |
|---|---|---|---|---|---|---|---|
| T14-H | Ruhmeshalle Hintergrund | `t14_ruhm_{haus}` | 1280 x 720 | Hintergrund der Rangliste | Statuen mit Gesichtern bekannter Personen, Schrift | [STIL] [SZENE] [HAUS] A high hall of honour of the house with tall banners, trophies on pedestals and golden light falling from high windows; the middle 50 percent is a darker wall area for the ranking list. | [NEG], letters, recognisable faces, crest |
| T14-A | Auszeichnungen, ein Bogen | `t14_auszeichnung_<name> (feldherr, forscher, haendler, gesamtherrscher)` | 128 x 128 (Bogen 2 x 2) | die vier Auszeichnungen | Schrift | [STIL] [OBJEKT] A 2x2 sheet of four gold medals on dark background: a medal with a sword and laurel, a medal with an open book and star, a medal with a money sack and scales, a large medal with a crown of laurel. | [NEG], letters, crest |

(belegt: vier Auszeichnungen Feldherr, Forscher, Händler, Gesamtherrscher - README.md Z. 27; data/ruhm.json führt 4 Stufen.)

#### T15 GILDENHALLE (Standard)

| ID | Ort im Spiel | Dateiname-Vorschlag | Maße (100 %) | Zweck | NICHT drauf | Prompt (englisch) | negativer Prompt |
|---|---|---|---|---|---|---|---|
| T15 | Gildenhalle Hintergrund | `t15_gilde` | 1280 x 720 | Hintergrund der Ansicht | Schrift, Gesichter | [STIL] [SZENE] [STANDARD] A long timber guild hall with a large round table, many chairs and red banners with light symbols on the walls, a hearth at the far end; middle area calm and dark. | [NEG], letters, faces |

#### T16 SCHLACHTSIMULATOR (Standard)

| ID | Ort im Spiel | Dateiname-Vorschlag | Maße (100 %) | Zweck | NICHT drauf | Prompt (englisch) | negativer Prompt |
|---|---|---|---|---|---|---|---|
| T16 | Schlachtsimulator Hintergrund | `t16_simulator` | 1280 x 720 | Hintergrund der Ansicht | Schachfiguren, Schrift | [STIL] [SZENE] [STANDARD] A war room with a large sand table showing painted hills, a river and small carved wooden markers, lanterns hanging above; the sand table occupies the lower middle, upper area dark wood. | [NEG], chess pieces, letters |

#### T17 KNÖPFE (Standard, 9-Slice)

| ID | Ort im Spiel | Dateiname-Vorschlag | Maße (100 %) | Zweck | NICHT drauf | Prompt (englisch) | negativer Prompt |
|---|---|---|---|---|---|---|---|
| T17 | Knopf, drei Zustände | `t17_knopf_<zustand> (normal, gedrueckt, gesperrt)` | 192 x 48 je Zustand (9-Slice, Ecken 12; Bogen 1 x 3) | jeder Knopf im Spiel; Schrift setzt das Spiel | Schrift, Symbole | [STIL] [OBJEKT] A 1x3 vertical sheet of three wide empty rectangular buttons with 4 px rounded corners and a thin antique gold rim on dark red-brown wood: first raised and warmly lit, second pressed in and darker with inner shadow, third flat, desaturated grey-brown with a dull rim. | [NEG], letters, icons, perspective |

("gesperrt mit Grund": den Grund schreibt das Spiel neben oder unter den Knopf. belegt src/main.py
Z. 2778-2801: der Sperrgrund wird schon heute im Menü angezeigt.)

#### T18 PUNKTE-/STATUSLEISTEN (Standard, 9-Slice)

| ID | Ort im Spiel | Dateiname-Vorschlag | Maße (100 %) | Zweck | NICHT drauf | Prompt (englisch) | negativer Prompt |
|---|---|---|---|---|---|---|---|
| T18 | Statusleiste | `t18_rinne, t18_fuell_gold, t18_fuell_rot, t18_fuell_gruen` | 256 x 20 (9-Slice, Ecken 8; Bogen 1 x 4) | Punkte, Lebenspunkte, Fortschritt | Zahlen | [STIL] [OBJEKT] A 1x4 vertical sheet: an empty dark groove with thin gold rim, then a glowing gold fill bar, a glowing red fill bar and a glowing green fill bar of the same size. | [NEG], numbers, letters |

#### T19 SIEG UND NIEDERLAGE (Standard)

| ID | Ort im Spiel | Dateiname-Vorschlag | Maße (100 %) | Zweck | NICHT drauf | Prompt (englisch) | negativer Prompt |
|---|---|---|---|---|---|---|---|
| T19-S | Siegbild | `t19_sieg` | 1600 x 900 | Bild bei gewonnener Schlacht/Auszeichnung | Gesichter, Wappen | [STIL] [SZENE] [STANDARD] A hilltop at sunrise with many banners raised in celebration, golden light breaking through the mist over the Fog Lake valley; lower third calm for text. | [NEG], faces, crest, letters |
| T19-N | Niederlagebild | `t19_niederlage` | 1600 x 900 | Bild bei verlorener Schlacht | Leichen, Blut | [STIL] [SZENE] [STANDARD] A burned-out gate in grey drizzle, fallen banners in the mud, a single brazier still glowing; lower third calm for text. | [NEG], corpses, blood, gore, letters |

Summe (Bildgenerierungen, ohne Fassungen 100/125/150):
```text
T01 1, T02 6, T03 10, T04 120, T05 13 (6 Rahmen + 7 Gelände), T06 12 (6 + 6), T07 6 + 1 + 6 + 7 = 20,
T08 3, T09 2, T10 1, T11 3, T12 6 + 3 = 9, T13 6, T14 6 + 1 = 7, T15 1, T16 1, T17 1, T18 1, T19 2.
Zusammen 229. Davon T04 allein 120.
```

## TEIL 3 - DIE PRÜFUNG

### 3.1 ABNAHMEKRITERIEN (messbar)

Für JEDES Bild (A-ALLE):
```text
a) Maße exakt wie Teil 2, in allen drei Fassungen (100/125/150).
b) Keine Schrift: Texterkennung (z. B. Tesseract) findet kein Wort mit Konfidenz über 60.
c) Schärfe: Varianz des Laplace-Filters auf der 100-%-Fassung (Graustufen 0-255) mindestens 100.
   Vorschlag; der Wert ist eine übliche Faustregel für "nicht verwischt", am ersten Bild abstimmen.
d) Kein Hochskalieren im Spiel: die gelieferte Fassung ist mindestens so groß wie die Anzeige.
e) Hausfarbe (nur je-Haus-Bilder): der mittlere Farbton der 20 % am stärksten gesättigten Pixel liegt
   innerhalb von +/- 25 Grad des Akzent-Farbtons des Hauses (Silberbach 351, Hammerhall 211,
   Sternenwacht 132, Schattenfaust 270, Knochenmoor 211, Flickwerk 0; Standard 45 bzw. Grund 3).
   Für Hammerhall/Knochenmoor zusätzlich: mittlere Sättigung dieser Pixel bei Hammerhall unter, bei
   Knochenmoor über 0,45 (Vorschlag).
```

**A-HG** Hintergründe (T01, T02, T04, T06-H, T07-K, T11-H, T13, T14-H, T15, T16, T19):
- Textzone (in Teil 2 benannt): 95. Perzentil der relativen Leuchtdichte höchstens 0,13 (R-6).
- Tote Fläche (R-7) außerhalb der Textzone höchstens 15 % der Blöcke; im ganzen Bild höchstens 30 %.
- Mindestens ein gesättigter Akzent: mindestens 2 % der Pixel mit Sättigung über 0,6.
- T06-H: mittlere 60 % der Breite dunkler als die Seitenstreifen (mittlere Leuchtdichte Mitte höchstens 0,6 x Seiten), damit die Karte dort klar steht.
- T07-K: im Mittelfeld (mittlere 50 % x 50 %) Standardabweichung der Helligkeit höchstens 0,08 (ruhig für Marker); in den Seiten- und Hintergrundstreifen sind Figuren zu erkennen (Sichtprüfung: mindestens sechs Figuren zählbar).

**A-T04** Gebäudebilder zusätzlich:
- Das Gebäude liegt vollständig im mittigen Quadrat 1120 x 1120 (wird zur 256er-Kachel).
- Obere 150 px als Kopfband nutzbar: kein Gebäudeteil schneidet die Linie bei 150 px.
- Banner mit Symbol vorhanden und bei der 256er-Kachel noch erkennbar (Sichtprüfung).

**A-KOPF** Kopfbänder (T03, T12-K und Ausschnitte):
- Die mittleren 1024 px tragen das Motiv; die äußeren 448 px je Seite haben eine Helligkeits- Standardabweichung unter 0,10 (ruhig beim Zuschnitt).

**A-9** 9-Slice-Teile (T05-R, T08-F, T10-K, T11-F, T12-B, T17, T18):
- Kanten kachelbar: an jeder Stoßstelle mittlere absolute Pixeldifferenz höchstens 8 (von 255).
- Ecke genau so groß wie in Teil 2; die Mitte einfarbig genug, dass Text darauf 4,5 : 1 erreicht (gleiche Rechnung wie R-6).
- T17: der Zustand "gesperrt" ist von "normal" unterscheidbar: mittlere Sättigung höchstens halb so hoch wie bei "normal".

**A-SYM** Symbole und Icons (T08-S, T09, T14-A, T07-E, T07-F):
- Bei Zielgröße (32 px bzw. 64 px für Einheiten) füllt die Silhouette 60-80 % der Höhe der Zelle.
- Schwerpunkt der Silhouette höchstens 1 px vom Zellmittelpunkt (gegen "verschoben").
- Gleiche Polsterung: Abstand Silhouette-Zellrand je Seite zwischen allen Icons eines Bogens höchstens 2 px Unterschied (bei 32 px).
- Kontrast Symbol gegen Fach-/Leistengrund mindestens 3 : 1 (Nicht-Text).
- Erkennbarkeit: Blindtest bei 32 px - eine Person (oder Hermes per Bildauswertung) nennt ohne Liste mindestens 10 von 11 Ressourcen richtig; bei den Menü-Icons 8 von 9.
- Freistellung: am Rand kein heller Saum; Prüfung auf Grund #2a0605, kein Randpixel heller als Leuchtdichte 0,5, das nicht zum Motiv gehört.

**A-KACHEL** Geländekacheln (T05-G):
- Nahtlos: 3 x 3 nebeneinander gelegt, Stoßstellen-Differenz höchstens 8.
- Die sieben Arten sind bei 64 px unterscheidbar: mittlere Farbe je Paar mindestens 20 Delta-E (CIE76) auseinander (Vorschlag).

**A-SKIN** Skins:
- Jedes Standardteil wird je einmal mit den Skins "standard", "wald" und "feuer" im Spiel abfotografiert; Schrift auf den Teilen erreicht in allen drei mindestens 4,5 : 1.

### 3.2 REIHENFOLGE: DIE ERSTEN 12 BILDER

Ziel: nach einer Stunde ist jeder Bildschirm, den man ständig sieht, neu. Entscheidung: für die je-Haus-
Bilder zuerst nur EIN Haus. Vorschlag: Silberbach, weil Midgard Startwelt ist (belegt data/welten.json
"startwelt": "Midgard") und Silberbach dort sitzt.

```text
 1  T17   Knopf, drei Zustände        - auf jedem Bildschirm
 2  T08-B Ressourcenleiste Band        - immer sichtbar, Daniels deutlichste Kritik
 3  T08-F Ressourcenleiste Fach        - dazu
 4  T08-S Ressourcensymbole (Bogen)    - dazu; ein Bild, elf Symbole
 5  T09-A Menü-Icons Kernsatz (Bogen)  - immer sichtbar
 6  T01   Tor                          - erster Bildschirm
 7  T04-20 Dorfzentrum silberbach      - erste Spielansicht
 8  T06-H Portal silberbach            - Daniels Kritik "sehr viel braun"
 9  T07-K Kaserne silberbach           - Daniels Kritik "viel zu klein ... lieblos"
10  T07-F Feldmarkierungen             - dazu, Dörfer und Bots erkennbar
11  T05-R Kartenrahmen silberbach      - Rahmen um die Karte im Portal
12  T18   Statusleisten                - Lage-Band und Fortschritt
```

Nicht unter den ersten zwölf, mit Grund: das "Lage-Band (Forschung/Götterschutz/Wallbau)", das rechts
über den Hintergrund hinauslief - das ist ein Problem der Breite im Code, kein Bild. Mit T18 und dem
9-Slice wächst es mit dem Fenster mit; den Überlauf selbst muss der Code lösen.

Danach: die übrigen 19 Bilder von T04 für Silberbach, dann T02/T13/T14 für Silberbach, dann die anderen
fünf Häuser Haus für Haus (je Haus 20 + 7 = 27 Bilder), zuletzt T03, T11, T12, T15, T16, T19, T07-E.

### 3.3 DAS WIRD NICHT GEBRAUCHT

- Die 125 Siedlungskarten für den Dörferausbau: bleiben, wie sie sind (belegt docs/design/DESIGN_ARBEITSWEISE.md Z. 55).
- Burgen und Drachen: sind Daniels Grafiken, Originale unangetastet (belegt ebd. Z. 54). Keine neuen Burgbilder in diesem Paket; die Zuordnung Burg -&gt; Haus ist laut Auftrag offen.
- Ausbaustufen für Burgen, Gebäude oder Felder (belegt ebd. Z. 56).
- Wappen: werden nicht neu gemalt (Auftrag), das Spiel legt die vorhandenen Dateien aus assets/icons/wappen/ auf Marker und Plaketten.
- Das Logo von Chris Fred Däubner: wird nicht erzeugt, nicht nachgebaut; es liegt über T01/T02.
- Gemalte Sätze für die Skins "wald" und "feuer" (Entscheidung in 1.2).
- Eigene Kopfbänder für Hausansichten (Ausschnitt statt Extra-Bild, 1.4).
- Eigene Rohstoff- und Gebäudekacheln im Lager (T10: Symbol + Grund, Ausschnitt aus T04).
- Einheitenfiguren je Haus (1.4, Entscheidung 3).
- Eigene Icons für Forum, Chat, "Spieler werben": ein gemeinsames "gesperrt" (belegt Forum offline, src/main.py Z. 15831; Chat und "Spieler werben": weiß ich nicht, ob sie ebenfalls offline sind).
- Ein Icon für "Lager" in der Leiste: der Punkt ist ausgeblendet (belegt src/main.py Z. 3749).
- Bilder für die 14 entfernten Limbus-Dimensionen: es gibt sechs Welten (belegt data/welten.json, "_schnitt_w6").
- Die 17 Waren (Ausrüstung) aus data/items.json: der Auftrag nennt unter T10 nur die neun Rohstoffe; die vorhandenen Bilder in assets/icons/items/ (18 Dateien) bleiben, bis Daniel entscheidet.
- Animationen, Tag/Nacht-Fassungen, Jahreszeiten: kein Ort im Spiel verlangt sie.
- Bilder mit Gesichtern bekannter Personen, Marken, Bilder aus dem Netz: harte Regel des Auftrags.

### WAS ICH NICHT GEPRÜFT HABE

- Das Spiel laufen sehen, bei 100/125/150 % (V-2): kein Windows-Rechner in dieser Sitzung.
- Die genauen Flächenmaße von Portal, Angriffsfläche, Marktplatz, Ruhmeshalle, Forschung im laufenden Fenster: weiß ich nicht. Ich habe 1280 x 720 bzw. 1600 x 900 angesetzt; vor der Erzeugung einmal im Spiel messen und Teil 2 anpassen.
- Ob die Generatoren die Bögen (2 x 2, 3 x 3, 4 x 3, 5 x 2) sauber gleich groß liefern: hängt vom Modell ab. Fällt ein Bogen ungleich aus, einzeln erzeugen; die Abnahme A-SYM fängt es.
- Chris' Panoramen im Archiv (archiv/design/20261109_chris_bildpaket/, gitignoriert) habe ich nicht gesehen; die Stilbeschreibung stützt sich auf seine Regeln in DESIGN_LIEFERUNG_CHRIS und auf die drei Bilder von ihm im Repo (Logo, portal_kopfband_schmiede_dorf_ghule_780x150.png, marktplatz_kennzeichen_96.png).
