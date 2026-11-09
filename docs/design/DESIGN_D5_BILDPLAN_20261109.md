# D-5 Bildplan — welches Bild, wohin, wie groß

**Stand:** 09.11.2026, 16:38. Das ist der „Detail“-Teil von D-5: **alle Angaben beisammen** — welches
Bild, an welcher Stelle, in welcher Größe, mit welchem Zuschnitt, und was fehlt.

**Was „Detail“ hier heißt (Daniel, 09.11.2026, zwischen 15:21 und 16:38):** nicht eine Detailansicht im Fenster, sondern
die vollständige Festlegung — „wenn genau klar fest steht wo ein bild hin soll wie groß es sein muss und
welches usw wenn einfach alle benötigten informationen beisammen sind dafür“.

Gemessenes Maßblatt: `archiv/design/20261109_chris_bildpaket/geschnitten/d5_massblatt_20261109.png`
(840 × 2047) — jedes Bild steht dort in der Größe, die es im Fenster bekommt. Die geschnittenen
Dateien liegen daneben im selben Ordner (gitignoriert).

## 1. Grundmaße, am Code gemessen

| Größe | Wert | Beleg |
|---|---|---|
| Fenster beim Start | 1024 × 720 px | `src/main.py:8287` (`self.root.geometry`) |
| Inhaltsbreite (eine Spalte) | **780 px** | alle Portal-Labels: `wraplength=760` + `padx=10` je Seite |
| Weltkartenliste | 6 Zeilen, je ~22 px hoch | `portalraum.weltkarten()`, `tk.Label` `width=3` / `width=14` |
| Geländekästchen | **400 × 400 px** (20 px je Feld, 20 × 20 Felder) | `_portal_zelle`, `portalraum._achsen()` |
| Rahmen um das Kästchen | 9-Slice aus der C2-Lieferung, ohne Bild bleibt das nackte Kästchen | `_kartenrahmen_bauen` |
| Burg auf einem Feld | **18 px** | `WAPPEN_GROESSE = 92` × 20 px (`data/bot_wappen.json`) |
| Wappen auf einem Feld | **8 px** | `WAPPEN_ANTEIL = 40` × 20 px |
| Bannerfarben der Weltliste | grün `#2ecc40`, rot `#e53935` | `PORTAL_BANNER_FARBEN` (`src/main.py:3433`) |
| Legende | 7 Geländearten, je ein Farbfeld + Name + Häufigkeit | `portalraum.legende()` |

**Wichtig für die Größenwahl:** die gelieferten Bilder sind **2,2 bis 2,7 : 1** (Panoramen) und
**5,14 bis 5,21 : 1** (Bänder). Ein Kopf in 780 × 200 px ist 3,9 : 1 — deshalb muss jedes Panorama
**oben und unten beschnitten** werden, und zwar deutlich (Tabelle, Abschnitt 3).

## 2. Die Plätze im Portal

| Platz | Wo im Fenster | Größe | Bildquelle | Stand |
|---|---|---|---|---|
| **S1 Kopfleiste** | über dem Titel „Portal“, volle Spaltenbreite | 780 × 150 px | Band aus der Lieferung | **fehlt im Code**, Vorschlag liegt vor |
| **S2 Weltkartenzeile** | je Zeile das Kennzeichen der Welt | 22 × 30 px | Farbe + Symbol (kein freistehendes Banner in der Lieferung) | heute nur farbiger Text |
| **S3 Kartenrahmen** | 9-Slice um das 400 × 400-Kästchen | Rand je 12–20 px | C2-Rahmen (heute) oder Chris' Goldrahmen | heute C2-Bild |
| **S4 Burg auf dem Feld** | Feldmitte, auf der gemalten Karte | 18 × 18 px | `assets/icons/burgen/burg_01..06.png` (Daniels Grafiken) | gebaut (W-8) |
| **S5 Wappen auf dem Feld** | Feldmitte + 28 % nach unten rechts | 8 × 8 px | `assets/icons/wappen/wappen_01..10.png` | gebaut (W-8) |
| **S6 Legende** | unter der Karte | 20 × 18 px je Feld | Farben aus `data/gelaende.json` | gebaut |
| **S7 Seitenhintergrund** | hinter der ganzen Portalseite | 1024 × 720 px | kein Bild nötig — `skin["bg"]` | nicht geplant |

## 3. Der Bildplan (geschnitten und gemessen)

Alle Angaben in der Tabelle sind **gerechnet und die Dateien liegen bereits vor** (Ordner
`archiv/design/20261109_chris_bildpaket/geschnitten/`). „Beschnitt“ heißt: oben und unten
weggeschnitten, mittig, um auf die Zielhöhe zu kommen.

| Rolle | Bild | Zielgröße | Original | Beschnitt | Datei |
|---|---|---|---|---|---|
| **Kopfleiste (Empfehlung)** | `band_schmiede_dorf_ghule` | **780 × 150** | 3500 × 672 | **0 %** | `band_schmiede_dorf_ghule_780x150.png` |
| Kopfleiste (Alternative) | `band_ghule_lager` | **780 × 152** | 3474 × 676 | **0 %** | `band_ghule_lager_780x152.png` |
| Portal-Kopf | `panorama_wegweiser_burg_im_nebel` | 780 × 200 | 3336 × 1309 | 35 % | `panorama_wegweiser_burg_im_nebel_780x200.png` |
| Portal-Kopf | `panorama_portal_weltensprung` | 780 × 200 | 3486 × 1330 | 33 % | `panorama_portal_weltensprung_780x200.png` |
| Portal-Kopf | `panorama_burg_bruecke_wasserfall` | 780 × 200 | 3396 × 1523 | 43 % | `panorama_burg_bruecke_wasserfall_780x200.png` |
| Portal-Kopf | `panorama_burgtor_fackeln` | 780 × 200 | 3235 × 1497 | 45 % | `panorama_burgtor_fackeln_780x200.png` |
| **Ladeseite** | `panorama_ladeseite_haemmer` | **780 × 287** | 3375 × 1243 | **0 %** | `panorama_ladeseite_haemmer_780x287.png` |
| Marsch-Kopf | `panorama_marsch_bruecke` | 780 × 200 | 3474 × 1335 | 33 % | `panorama_marsch_bruecke_780x200.png` |

**Was daraus folgt:** Ein Band kostet **keinen** Beschnitt (5,15 : 1 paßt auf 780 × 150), ein Panorama
kostet 33 bis 45 % seiner Höhe. Deshalb ist die Empfehlung für S1 das **Band**; die Panoramen sind für
eine **Ladeseite** (780 × 287, 0 %) und für **Portal-Köpfe mit eigener Höhe** geeignet, nicht als flache
Leiste.

**Dateigröße im Spiel:** die geschnittenen PNG liegen zwischen **230 und 390 KB** (gemessen: Band 254 KB,
größtes Panorama 390 KB, das Maßblatt selbst 2,3 MB und bleibt im Archiv). Für S1 reicht das Band mit
254 KB auch für die EXE. Ob beim Einbau zusätzlich als WebP gespart wird, entscheidet die Messung am
Bau, nicht eine Schätzung.

## 4. Farben (gemessen, nicht abgeschrieben)

| Rolle | Gemessener Median | Richtwert des Nachtrags |
|---|---|---|
| Rahmengold | `#C68B42` | `#C9993F` |
| Banner-Rot | `#7E301E` | `#8B2A22` |
| Ghule-Leuchten | `#7AAC4D` | `#7CFF4A` |
| Banner der Weltliste (Code) | `#2ecc40` grün / `#e53935` rot | — (belegt aus portal.php 2005) |

**F-37 (09.11.2026)** sagt: rot mit hellem Symbol wird die neue Quelle für neutrale Banner. Für die
Weltliste bleibt es bei grün = eigene Welt, rot = fremde Welt — diese Bedeutung ist belegt und wird
nicht überschrieben.

## 5. Was fehlt

1. **Kein freistehendes Bannerbild.** Die Banner in der Lieferung sind *in* den Gebäudekacheln gemalt.
   Für S2 gibt es zwei Wege: eine farbige Form mit Symbol (heute) oder einen Ausschnitt aus einer
   Kachel — der Ausschnitt wäre ein Notbehelf mit sichtbarem Rand.
2. **Keine Bilder** für Bibliothek, Bogenbauer, Diebesgilde, Goldmine, Haus, Kriegerakademie, Lager,
   Nähstube, Pferdezucht, Stellmacher.
3. **Keine Fraktionsvarianten** außer den Ghulen.
4. **Kein Bild für die Weltkarte selbst** — die Karte malt `weltkarte_malerei` aus den Geländedaten
   (D-3/D-4). Der Umbau auf Chris' Farben und Tannen ist **D-5a** (F-36), nicht D-5.

## 6. Was D-5 am Code ändert (Vorschlag, noch nicht gebaut)

1. **S1:** ein `tk.Label` mit dem Band-Bild über dem Titel, unter dem Titel eine Trennlinie in
   `#C68B42`. Kein Eingriff in die Karte, keine neue Wache am Zeichner nötig — die Wache prüft nur,
   dass das Bild geladen wird und ohne Bild ein leerer Platz bleibt (kein Absturz).
2. **S2:** Bannerfarbe bleibt die Wahrheit; optional ein 6 px breiter Farbstreifen links in der Zeile.
3. **S3–S6 bleiben unverändert.** Der Goldrahmen (Chris) ist **D-5b** (F-39), nicht D-5.

**Aufwand:** eine `src/main.py`-Änderung, eine neue Wache, ein Sammellauf (~20 min). Kein Eingriff in
`weltkarte_malerei`, `portalraum` oder die Spielregeln.

## 7. Offene Punkte (eine Runde, Empfehlung zuerst)

1. **Kopfleiste:** Band `band_schmiede_dorf_ghule` 780 × 150 (0 % Beschnitt) — oder lieber ein Panorama
   780 × 200 mit 33–45 % Beschnitt? *(Empfehlung: Band.)*
2. **Banner in der Weltliste:** farbige Form mit Symbol wie heute — oder einen Ausschnitt aus einer
   Kachel? *(Empfehlung: farbige Form, kein Kachelausschnitt.)*
3. **Goldrahmen:** in D-5 lassen (C2-Rahmen bleibt) und erst in D-5b mit den Icons zusammen umstellen —
   oder schon in D-5? *(Empfehlung: D-5b, wie F-39 es reiht.)*
## 8. Entschieden (09.11.2026, 16:58 - Register 347)

Die drei Punkte aus Abschnitt 7 sind beantwortet, alle drei wie empfohlen:

1. **Kopfleiste:** Band `band_schmiede_dorf_ghule`, **780 x 150 px, 0 % Beschnitt** - gebaut in D-5.
2. **Banner in der Weltliste:** farbige Form, **kein** Kachelausschnitt - gebaut als 6 x 18 px Farbstreifen je Zeile.
3. **Goldrahmen:** bleibt in D-5 beim C2-Rahmen, Umstellung erst in **D-5b** mit den Icons (F-39).

Damit ist D-5 am Code fertig; die Kette geht mit **D-5a** (Weltkarte auf Chris' Farben und Tannen) und **D-5b**
(Icons und Rahmen) weiter.

**Nachtrag 18:15 (Register 348): die Breite 780 px gilt als OBERE Grenze, nicht als feste Groesse.** Gemessen ist
die Inhaltsspalte im Standardfenster (1024 x 720) nur **630 px** breit; ein festes 780-px-Band wurde dort rechts
abgeschnitten (kein waagerechter Rollbalken). Daniel hat entschieden: bei schmaler Spalte wird das Band
**verkleinert** (Seitenverhaeltnis bleibt, kein Beschnitt, Original 780 x 150 bleibt die Quelle) - im
Standardfenster sind das 610 x 117 px, ab etwa 1280 px Fensterbreite wieder 780 x 150.
