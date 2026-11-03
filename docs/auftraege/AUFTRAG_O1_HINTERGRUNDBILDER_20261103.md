# Auftrag an das starke Modell: 20 Hintergrundbilder fuer die Gebaeudeansichten (O-1, 03.11.2026)

## Rolle

Du bist Art Director und Prompt-Autor fuer ein lokales Remake des Browserspiels **Nebelseetal**
(Aufbau-Strategiespiel, Mittelalter/Fantasy, Einzelspieler gegen fuenf Bots, deutsch). Du **erzeugst
keine Bilder** - du lieferst fuer jede Gebaeudeansicht einen **fertigen, englischen Bildprompt** samt
Kompositionsangabe, mit dem ein Bildmodell (SDXL/Flux-Klasse) ein passendes Hintergrundbild erzeugt.

## Der Auftrag in einem Satz

Die bisherigen Hintergruende sind **538 x 222 px** und werden auf **980 x 760** gezogen (**3,42 x**) -
dadurch sind sie unscharf und wirken auseinandergezogen (Befund des Auftraggebers). Es sollen **echte
Hintergrundbilder** entstehen, **auf Basis der bisherigen Motive** (gleiche Haeuser, gleiche
Bildsprache), **angepasst an die frei sichtbaren Flaechen** der Ansicht.

## Gemessene Vorgaben (nicht schaetzen)

- **Zielgroesse: 1600 x 1200 px** (4:3), damit auch ein maximiertes Fenster scharf bleibt.
- **Inhaltsbereich der Ansicht: 1052 px breit** (gemessen), Hoehe je Ansicht 816 bis 2057 px.
- **Safe Area (gemessen per Raster ueber den Inhaltsbereich):** das Bild ist **oben** sichtbar und wird
  **unten** von deckenden Textkaesten verdeckt. Bei der Stellmacher-Ansicht sind die **oberen 65 Prozent**
  bildfrei, beim Dorfzentrum die **oberen 37 Prozent**.
  **Folge fuer jedes Bild:** das Motiv (Gebaeude, Hauptgegenstand) steht in den **oberen zwei Dritteln**,
  mittig; das **untere Drittel** darf Himmel, Nebel, Boden oder Wald tragen - dort liegt spaeter Text.
- **Abdunkeln 38 Prozent, Weichzeichnen 2 px** kommen beim Einbau darueber (Zahlen in
  `data/gebaeude_motive.json`). Deshalb: **keine harten Kontraste, keine feinen Muster, keine Schrift** -
  sie gehen im Schleier unter.

## Bildsprache der bisherigen Motive (Vorbild, woertlich aus der Sichtung eines vorhandenen Bildes)

> Mittelalterlich-fantastische **Stellmacher-/Zimmermannswerkstatt** in einem dichten Nadelwald.
> Panorama-Ansicht auf Augenhoehe, Kamera leicht schraeg. **Spaete Abendaemmerung** (goldene Stunde):
> gedaempftes, kuehles Umgebungslicht, dagegen ein **warmes Laternenlicht** unter dem Dachvorsprung
> (Chiaroscuro). Palette: warmes Ocker, Umbra, Sienna, dunkles Nussbaumholz, tiefes Tannengruen,
> Moosgruen, blass-blaugruener Nebel im Hintergrund, leuchtendes Orange-Gelb (Laterne), tiefes Rot
> (Banner), Grau (Steinkamin). **Digitales Concept Art, Fantasy-Realismus**, malerisch mit erkennbaren
> Pinselstrichen, hoher Detailgrad im Vorder-/Mittelgrund, weicher Nebel im Hintergrund
> (atmosphaerische Perspektive). **Keine Personen, keine Tiere, keine Schrift.**

Jedes Bild soll dieselbe Handschrift tragen: **verlassen wirkende, aber bewohnte Werkstatt oder
Aussenansicht**, warmes Licht aus einem Fenster oder einer Laterne, kuehler Nebelwald als Kulisse.

## Die 20 Motive, die es gibt (Kennung, Name, Funktion im Spiel)

- `holzfaeller` (Holzfäller): produziert Holz
- `steinmetz` (Steinmetz): produziert Stein
- `erzmine` (Erzmine): produziert Metall
- `tempel` (Tempel): produziert Mana
- `farm` (Farm): produziert Nahrung
- `goldmine` (Goldmine): produziert Gold
- `schafszucht` (Schafszucht): produziert Wolle
- `rinderfarm` (Rinderfarm): produziert Nahrung und Leder
- `pferdezucht` (Pferdezucht): produziert Pferde
- `jaeger` (Jäger): produziert Nahrung und Leder aus der Jagd
- `schmiede` (Schmiede): stellt Waffen und Rüstungen her (Waren der Schmiede, u. a. Messer, Dolch, Kurzschwert, Schwert, Zweihänder, Ke
- `bogenbauer` (Bogenbauer): stellt Fernwaffen her (Kurzbogen, Bogen, Langbogen, Armbrust; Voraussetzungen über Waffentechnik)
- `naehstube` (Nähstube): stellt Stoff- und Fellkleidung her (Wollumhang, Lederrüstung, Diebesumhang, Fellumhang, Fellrüstung; Vorausset
- `kriegerakademie` (Kriegerakademie): bildet Armee-Einheiten (Kampfeinheiten) aus: Nahkampf (Bürgerwehr, Kämpfer, Krieger, Ritter, Paladin) und Fern
- `diebesgilde` (Diebesgilde): bildet Kundschafter aus (Streuner, Gauner, Dieb, Meisterdieb, Kundschafter, Waldläufer)
- `stellmacher` (Stellmacher): baut Karren (Handkarren, Einspänner, Zweispänner, Handelskarawane, Große Handelskarawane, Siedlerkarren) und B
- `verteidigungswall` (Verteidigungswall): Schutz vor Angriffen. In der Vorrunde einer Schlacht wird geprüft, ob die Schlagkraft (SK) der angreifenden Fu
- `bibliothek` (Bibliothek): ermöglicht Forschung; Ausbau in Stufen erweitert die Forschungsmöglichkeiten; mit jeder Stufe teurer. Nur auf 
- `haus` (Haus): erhöht die Siedlergrenze um 5 Siedler je Haus
- `lager` (Dorfzentrum): Dorfzentrum und Lagerverwaltung des Dorfes: Übersicht über alle Waren, Einheiten und Werkstätten dieses Ortes;

## Was du liefern sollst

Je Motiv:

1. **Englischer Prompt** (60 bis 120 Woerter), SDXL/Flux-tauglich: Motiv, Perspektive, Tageszeit, Licht,
   Palette, Stil, Detailgrad, Bildaufbau Vordergrund/Mittelgrund/Hintergrund.
2. **Kompositionsangabe**: was steht in den oberen zwei Dritteln (das Motiv), was im unteren Drittel
   (Himmel/Nebel/Boden, wird verdeckt).
3. **Negativ-Prompt** (kurz): keine Personen, keine Tiere, keine Schrift, keine UI-Elemente, kein
   Wasserzeichen, keine harten Kontraste, kein reines Schwarz oder Weiss.
4. **Ein Satz** auf Deutsch, warum dieses Motiv zur Funktion des Gebaeudes passt.

## Grenzen

- Keine neue Bildsprache erfinden: die Palette und der Stil oben sind gesetzt.
- Keine Personen, keine Tiere, keine Schrift, keine UI-Elemente im Bild.
- Keine Zahl erfinden: Groesse, Safe Area und Schleier stehen oben.
- Deutsch als Arbeitssprache, die Prompts selbst auf Englisch, Markdown, Tabellen, keine Emojis.

## Antwortformat

Genau eine Markdown-Datei:

1. `## Kurzfassung` (5 Zeilen: Grundsaetze, die fuer ALLE 20 Bilder gelten)
2. `## Stilbaustein` (der gemeinsame Prompt-Teil, den man vor jeden Prompt setzt)
3. `## Die 20 Motive` (Tabelle: Kennung | Prompt | Komposition | Negativ | Begruendung)
4. `## Reihenfolge der Lieferung` (welche zuerst, wenn nicht alle auf einmal gehen)
5. `## Offene Punkte` (was nur der Auftraggeber entscheiden kann, Empfehlung zuerst)
