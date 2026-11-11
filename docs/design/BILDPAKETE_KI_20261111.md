# Bildpakete für Nebelseetal — Tipps und Prompts (11.11.2026)

**Auftrag:** Daniel, 11.11.2026 (Register 434/435), wörtlich: »wir müssen burgen und wappen unserem
spiel und der story entsprechend mit stilreferenzen zu chris bearbeiteten panoramen von einem dafür
geeignetem KI programm entwerfen lassen … um die sich überall wiederholenden roten werkzeuge auf
schild in den bildern nicht zu häufig zu haben, sollten wir wirklich einfach pakete von passenden
bildern für die passenden bereiche von allen fraktionen anfertigen lassen. Tipps und prompts dafür
von dir bitte«.

**Ablage:** diese Datei ist die Quelle im Projekt. Für Daniel liegt dieselbe Fassung als `.txt`
(UTF-8 mit BOM, CRLF) unter `docs/design/BILDPAKETE_KI_20261111.txt`.

**Warum es dieses Paket braucht (gemessen, Register 433):** Burg und Wappen passen bei fünf von
sechs Häusern nicht zusammen — das Ghul-Haus trägt eine Baumfestung, sein Wappen zeigt den Wolf.
Die Bilder sind einzeln gut; sie gehören nur nicht zueinander. Dazu kommt Daniels Beobachtung aus
dem Test: dasselbe rote Banner mit dem Werkzeugsymbol liegt auf zu vielen Bildern.

---

## 1. Welches Programm

| Weg | Kosten | Wofür |
|---|---|---|
| Pollinations (`pollinations.ai`, Bild per Adresse) | nichts, kein Schlüssel | erste Entwürfe, Formulierungen ausprobieren |
| ComfyUI lokal | nichts außer Rechenzeit (20 bis 60 s je Bild) | Endfassungen; das eigene Bild als Stilvorlage (IP-Adapter / img2img) |

**Nicht:** ein Abo ohne API. Und keine Bilder von Chris direkt weiterverwenden, solange seine
schriftliche Erlaubnis fehlt (`DESIGN_LIEFERUNG_CHRIS_20261109.md` Z. 38–40). Als Stilvorlage zum
Nacharbeiten ist etwas anderes als zum Ausliefern — im Zweifel ihn fragen.

## 2. Die Farben stehen schon fest (gemessen)

| Wert | Hex | Herkunft |
|---|---|---|
| Grund | `#1a0a09` | Spiel (Leisten) |
| Rahmengold | `#C68B42` | Chris, Median aus 499.692 Randpixeln |
| Bannerrot | `#7E301E` | Chris, Median aus 127.204 Pixeln |
| Ghul-Leuchten | `#7AAC4D` | Chris, Median aus 21.773 Pixeln |
| Spiel-Gold | `#FFCC33` | Skin `standard` |

Hausfarben aus `data/haeuser.json`: Menschen Weinrot und Gold · Zwerge Nachtblau, Grau und Gold ·
Elfen Dunkelgrün und Gold · Trolle Violett, Schwarz und Gold · Ghule Blau, Silber und Gold ·
Gnome Karminrot, Silber und Gold.

**Regel:** ein Bild trägt höchstens zwei Farben plus Gold.

## 3. Die Pakete

Je Fraktion **sechs** Bilder — das ist der Kern gegen die Wiederholung:

1. Burg (Weltkarte, 512 × 512, freigestellt)
2. Wappen (Dialoge, 256 × 256, freigestellt)
3. Banner (rot mit hellem Symbol, 96 × 160) — **eines** je Fraktion, nicht je Gebäude
4. Gebäudekachel Wirtschaft (Mühle, Hof, Lager)
5. Gebäudekachel Handwerk (Schmiede, Werkstatt)
6. Gebäudekachel Wehr (Mauer, Turm, Tor)

Dazu **ein** gemeinsames Paket für alle: acht Geländekacheln, vier Wegstücke, ein Tor.
Sechs Fraktionen mal sechs Bilder sind 36 Bilder — zwei Abende, nicht zwei Wochen.

## 4. Das Prompt-Gerüst

Reihenfolge immer gleich: Motiv → Ansicht → Licht und Nebel → Farben → Stil → Technik → Verbot.

```
<Motiv>, three-quarter front view from slightly above, warm amber light from the front,
cool blue fog behind, muted earthy palette dominated by <FARBE 1> and <FARBE 2> with aged
gold ornaments, hand-painted 2.5D strategy game asset in the style of a painted medieval
fantasy panorama, visible brush texture, soft edges, no background, centered, 512x512
```

Verbot immer anhängen:

```
no text, no letters, no numbers, no watermark, no logo, no red tool icon on a shield,
no crowd of people, no modern objects, no photorealistic faces, no hard black outlines,
no lens flare, no border, no frame
```

## 5. Die sechs Fraktionen — fertige Prompts

**Menschen (Weinrot und Gold, Krone und Lilie)**
`a sturdy stone keep with tall square towers, deep wine-red banners with a golden crown,
three-quarter front view from slightly above, warm amber light from the front, cool fog behind,
muted earthy palette of wine red and old gold, hand-painted 2.5D strategy game asset, soft brush
texture, no background, centered, 512x512`

**Zwerge (Nachtblau, Grau und Gold, Steinturm)**
`a massive mountain fortress carved into a cliff, one square tower gate, midnight-blue and grey
stone with aged gold fittings, three-quarter front view, warm forge light from the gate, cold fog
behind, hand-painted 2.5D strategy game asset, soft brush texture, no background, centered`

**Elfen (Dunkelgrün und Gold, Hirschkopf)**
`a slender white-and-gold elf citadel grown from living trees, dark green and gold, high arched
windows, three-quarter front view, soft dappled light, mist between the trunks, hand-painted 2.5D
strategy game asset, soft brush texture, no background, centered`

**Trolle (Violett, Schwarz und Gold, Rabe)**
`a jagged black fortress on a rock spire, violet torchlight in the windows, a single dark banner
with a raven, three-quarter front view, warm violet light from within, cold night fog,
hand-painted 2.5D strategy game asset, soft brush texture, no background, centered`

**Ghule (Blau, Silber und Gold, Wolf)**
`a grim fortress of pale blue stone with silver veining, wolf banners, green ghost lights in the
yard, three-quarter front view, cold moonlight, heavy fog, hand-painted 2.5D strategy game asset,
soft brush texture, no background, centered`

**Gnome (Karminrot, Silber und Gold, gekreuzte Schwerter)**
`a crooked but sturdy workshop-town with many small chimneys and red roofs, crimson banners with
crossed silver swords, three-quarter front view, warm afternoon light, light haze, hand-painted
2.5D strategy game asset, soft brush texture, no background, centered`

## 6. Das Symbolsystem (gegen die Wiederholung)

Ein Symbol gehört zu **einem** Bereich, nicht zu jedem Bild: Burgturm = Burg und Verteidigung ·
gekreuzte Hämmer = Bergbau und Steinmetz · gekreuzte Äxte = Holzfäller · Ähre = Farm ·
Schaf und Stierkopf = Tierzucht · Pfote = Jäger · Kreuz = Tempel · Geldsack = Handel ·
Auge = Magie und Weltensicht · Totenkopf = Ghule.

Auf einem Bild steht **höchstens ein** Symbol. Das Banner einer Fraktion trägt das Fraktionszeichen,
nicht das Bereichszeichen.

## 7. Abnahme in einer Minute

- **Freigestellt?** Der Rand ist durchsichtig, keine Kachelkante, kein Rahmen.
- **Farbe?** Der Ton der größten Fläche passt zur Hausfarbe.
- **In klein lesbar?** Auf 64 px verkleinern — bleibt nur ein Fleck, ist es für die Karte zu fein.
- **Kein Text, keine Werkzeuge auf dem Schild, keine Menschenmenge.**
- **Seitenverhältnis:** Burg 1 : 1, Banner 3 : 5, Kachel 1 : 1. Verzerrt wird nie, nur beschnitten.

## 8. Reihenfolge

1. Sechs Wappen (klein, schnell, sie geben die Farben vor).
2. Sechs Burgen darauf abstimmen — Wappen und Burg müssen dieselbe Tinte tragen.
3. Sechs Banner (ein Symbol je Fraktion).
4. Achtzehn Gebäudekacheln, drei Durchgänge je Fraktion.
5. Erst wenn alles da ist: Dateinamen `<fraktion>_<motiv>.png`, dann ins Projekt.

Zwischenschritt: Entwürfe sammeln und **einen** Bogen daraus drucken, bevor etwas eingebaut wird —
sonst stehen sechs Stile nebeneinander.

## 9. Was das kostet

Pollinations: nichts. ComfyUI lokal: nichts außer Rechenzeit. **Keine Abos nötig.**
