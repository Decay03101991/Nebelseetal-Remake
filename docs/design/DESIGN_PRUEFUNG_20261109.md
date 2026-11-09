# Prüfung des Designpakets vom 09.11.2026 (Opus 5.5)

**Gegenstand:** `archiv/design/20261109_designvorschlag_01/paket.zip`, SHA256
`d0f27a13ac6ff91173c2b9470547c2f10b279ae5978a5f7d77d0781535aa0ed6`, 22.143.040 Byte, 39 Einträge.
**Geprüft:** 09.11.2026, 01:45 bis 01:55, von Weltenfresser. **Nichts davon ist ins Spiel
übernommen** - dieses Dokument ist die Vorarbeit, Daniels Entscheidungen stehen aus.

## 1. Was im Paket liegt (gemessen, nicht behauptet)

| Teil | Inhalt |
|---|---|
| `00_LIES_MICH_HERMES.md` | Auftrag und Inhalt, 30 Zeilen |
| `Designvorschlagspaket.md` | 320 Zeilen: Festlegungen, Malstil, Weltkarte, Burgen, Fraktionsbilder, Drachen, Logo, Marsch, Technik, Arbeitsschritte |
| `daten/design_werte.json` | 7.030 Byte, alle Farben und Maße als Daten |
| `burgen_vorlagen/` | 6 Burgbilder + Übersicht + 64-px-Lesbarkeitstest |
| `drachen_vorlagen/` | 3 Drachenbilder + Kartentest (120 px) |
| `stilreferenzen/` | je Fraktion Panorama und Szene, Oberflächenbilder, `trolle/FEHLT.txt` |
| `logo/` | Original (6.651.525 Byte) und zwei Arbeitskopien, Vorschau auf dunkel und auf hell |
| `vorschau/weltkarte/` | Stilprobe A (gewählt) und B (nur Tannen) |

## 2. Gegen die Datendateien geprüft - was stimmt

| Angabe des Pakets | Befund im Projekt |
|---|---|
| Drachen: Epheus der Weiße d02 / 7,13, Tardas der Grüne d03 / 12,6, Salmur der Rote d05 / 5,17 | **stimmt** (`data/drachen.json`, Feld `drachen`) |
| `figur.groesse_px` ist heute 12, `ruine_platzhalter` ist true | **stimmt** (`data/drachen.json`, Feld `figur`) |
| Farben und Namen der Drachen passen nicht zusammen | **stimmt und ist im Projekt vermerkt** (`figur.hinweis_farben`: Grün und Rot haben noch keine Figur) |
| 125 Karten für den Dörferausbau, im Katalog 127 Dateien | **stimmt in der Größenordnung**: `assets/karten` enthält 254 Dateien (127 Karten in zwei Formaten), `data/originalkarten` die Metadaten |
| 6 Fraktionen, 7 Geländearten, 6 Welten, 20 x 20 Felder | **stimmt** (`data/voelker.json`, `data/gelaende.json`, `data/welten.json`, `portalraum`) |

## 3. Widersprüche und Irrtümer (jeder mit Beleg)

**W-D1 - die Limbus-Ebene ist erfunden.** Das Paket schreibt: „Laut `welten.json` zeigt das Portal
die 6 Welten als Punkte in einer 10 × 10-Ebene (Limbus)". **In `data/welten.json` steht das nicht.**
Belegt sind `belegte_regeln.felder_je_dimension` = 20 und 400 Felder je Weltkarte
(`src/portalraum.py`); die Portalkarte zeichnet heute 20 x 20 Felder **je Welt**, nicht 10 x 10 für
alle. Die Zahl ist für die Planung unschädlich, aber sie darf nicht als Quelle weiterlaufen.

**W-D2 - isometrisch statt flach: das ist ein Umbau, keine Farbänderung.** Das Paket verlangt
Rautenkacheln 128 x 64 px, Bildkoordinaten `(x - y) * 64` / `(x + y) * 32` und eine Karte von etwa
2560 x 1280 px. Der heutige Zeichner (`_render_portal`) malt ein **flaches Quadratraster** mit 20 px
je Feld und Gelaendefarben. Ein Wechsel auf isometrisch berührt Zeichnen, Klick-Trefferflächen
(`_portal_klick`), Marschlinien, Burganker und die Feldauswahl - also alles, was in S-4 gerade
entstanden ist. Das gehört als eigener Schnitt geplant (D-2) und **nicht** nebenbei gemacht.

**W-D3 - Sumpf auf der Weltkarte.** Das Paket schlägt „Sumpf unbesetzbar" vor und markiert es als
Vorschlag. Im Projekt ist der Sumpf auf der **Siedlungskarte** unbebaubar (`data/gelaende.json`);
für die **Weltkarte** gibt es keine belegte Regel - Nebelsee ist dort die einzige belegte Sperre
(Daniel). Entscheidung liegt bei Daniel.

**W-D4 - das Paket widerspricht sich selbst an einer Stelle.** Abschnitt 3.4 verlangt für das
Namensschild „Keine Stufe"; die Stilprobe A zeigt an jeder Burg ein `Lv`-Etikett. Die Stilprobe ist
als Bild gemeint, nicht als Vorgabe - wer sie abzeichnet, baut die Stufe wieder ein.

**W-D5 - drei Fraktionen mit blauem Banner.** Menschlich, zwergisch und Trolle haben laut Tabelle
alle ein blaues Banner (`#2E4A9E`, `#2F4F9A`, `#2A3F8F`). Das Paket erkennt das selbst und schlägt
Zeichen plus Ring als Unterscheidung vor. Ob das im kleinsten Zoom reicht, ist **ungeprüft** und
braucht einen Bildtest, keine Zusage.

## 4. Was ich NICHT geprüft habe

- **Die Bildinhalte der 33 Bilddateien** des Pakets, außer der Stilprobe A. Für die sechs Burgen,
  die drei Drachen und die Fraktionspanoramen steht ein Urteil noch aus.
- **Ob die Stilreferenzen mit `assets/referenzbilder/ReferenzBild_Fraktionen_*` identisch sind.** Das
  Paket sagt „vermutlich"; ein Hash-Vergleich steht aus.
- **Die 15 Zwergen- und Beispielbilder** aus `archiv/design/referenzbilder_20261109/` - nur die
  Dateiliste und die Hashes sind geprüft, nicht der Inhalt.

## 5. Ein Punkt, der für Daniel spricht (Sichtprüfung)

Die Stilprobe A ist **hell und farbig** (Grün und Blau dominant, warme Brauntöne nur als Wege und
Stämme), gemalt mit feinen Konturen und weichen Schatten, isometrisches Rautenraster. Das trifft
genau die Kritik aus Spieltest 1, Note 4 („zu dunkel alles insgesamt von der Bildwahl", „zu wenig
Farbe und zuviel braune Hintergründe"). Der Ton der Vorlage ist damit richtig, auch wenn der
Zeichner dafür umgebaut werden muss (W-D2).

## 6. Was übernehmbar wäre, ohne eine Regel zu ändern

1. `daten/design_werte.json` als **Datengrundlage** für spätere Schnitte (Farben, Maße) - noch nicht
   in `data/` kopieren, solange kein Zeichner sie liest.
2. Die **Logo-Regeln** (dunkler Grund, Mindestbreite, nicht verzerren) in die Projektdoku.
3. Die **Burg- und Drachenbilder** als Vorlagen für skalierte Kopien, Originale unangetastet.
4. Die **Arbeitsreihenfolge D-1 bis D-8** aus `docs/design/DESIGN_ARBEITSWEISE.md` als Fahrplan.

## Nachtrag 09.11.2026, 01:57 - D-1: Abgleich mit den Projektdokumenten

**Anlass:** `docs/design/DESIGN_ARBEITSWEISE.md`, Schritt D-1. **Geprueft:** das Hauptdokument
`Designvorschlagspaket.md` (320 Zeilen) Zeile fuer Zeile gegen `data/*.json`, `docs/design/*.md`,
`src/main.py`, `src/portalraum.py` und die Bildbestaende. **Kein Code und keine Datendatei
geaendert.**

### 1. Selbstkorrektur an W-D1 (die Limbus-Ebene ist NICHT erfunden)

W-D1 oben sagt, die 10 x 10-Limbus-Ebene stehe "NICHT in `welten.json`". **Das ist falsch** und wird
hier berichtigt, nicht geloescht. In `data/welten.json` steht der Schluessel `ebene`: `x_von 0,
x_bis 9, y_von 0, y_bis 9, anzahl 6` mit dem `_hinweis`: "VORSCHLAG: Die sechs Weltkarten werden hier
als je ein Punkt in einer 10x10-Ebene (x/y von 0 bis 9) dargestellt. Im Original ist JEDE Dimension
ein eigenes 20x20-Raster (belegt ...)". **Richtiges Urteil:** die Ebene gibt es, sie ist ein
**VORSCHLAG** und meint nur die **Portal-Uebersicht** (ein Punkt je Welt), nicht das Spielfeld. Das
Paket zitiert sie als "Laut `welten.json`" und laesst den Vorschlagscharakter weg - der Fehler liegt
im Zitat, nicht in der Zahl. Fuer D-3/D-5 heisst das: die Uebersicht darf hoechstens als Skizze
dienen, die Karte selbst bleibt 20 x 20 je Welt.

### 2. Behauptungen des Pakets mit Urteil (gemessen)

| Punkt | Befund im Projekt | Urteil |
|---|---|---|
| 6 Fraktionen, Kennung `Trolle` | `voelker.json` fuehrt `menschlich, zwergisch, elfisch, Trolle, Ghule, Gnome` - **gross geschrieben** | **stimmt, aber Abschnitt 7.3 ist falsch:** dort steht, `{kennung}` sei "in Kleinbuchstaben wie in `voelker.json`" (`trolle`). Dateinamen nach dem Muster `trolle_160.png` passen zu KEINEM Datenschluessel |
| Heimatwelten je Fraktion | `welt_fraktionen.json.zuordnung`: menschlich 4, zwergisch 1, elfisch 5, Trolle 3, Ghule 2, Gnome 6 - genau die Tabelle 3.1; die Datei selbst sagt `quelle: NICHT BELEGT` | **stimmt zeichengenau**; "gelten dort als Vorschlag" trifft es sachlich, das Wort ist aber Daniels, nicht des Projekts |
| Trolle: AT +5 %, Handelserloes -5 % | `voelker.json`: `plus: "AT der Einheiten +5 %"`, `minus: "Handelserloes -5 %"` | **stimmt** |
| Spieler bis 6 Siedlungen, Bot bis 4 Doerfer | `resources.json.max_siedlungen = 6`; `bot_gruendung.json.hoechstens_doerfer = 4` | **stimmt** |
| 125 Karten, im Katalog 127 wegen 038 und 118 | `data/originalkarten/katalog.json`: **127 Eintraege**, darunter `original-038a/b` und `original-118a/b`; `assets/karten/spielfeld` 127 Dateien, `assets/karten` gesamt **254** | **stimmt** |
| 7 Gelaendearten | `data/gelaende.json`: 7 Eintraege (grasland, steppe, wald, huegel, berg, nebelsee, sumpf) | **stimmt** |
| "Jedes Feld hat das Merkmal `besetzbar`; die Platzierungspruefung fragt nur dieses Merkmal ab" | **kein `besetzbar` im Projekt** (0 Treffer in `src/`, `data/`, `tests/`, `tools/`); das Feld heisst `bebaubar` und beschreibt die SIEDLUNGSkarte; auf der Weltkarte prueft niemand Gelaende | **FALSCH als Beschreibung** - das ist ein Bauauftrag (D-3/D-5), kein Ist-Stand |
| `weltkarten_seed` | `data/welten.json.weltkarten_seed` vorhanden | **stimmt** |
| Portal-Banner gruen/rot | `welten.json.belegte_regeln.bannerfarben` (portal.php 2005) | **stimmt** |
| "Manakosten (Formel aus `welten.json`)" | dort steht eine **VORSCHLAG**-Formel (100 + 25 je Schritt); **belegt** ist der Festpreis **5000** (`koordinatenwechsel.kosten_mana`, `portalraum.wechselkosten()`), und Daniel hat F-25 = A entschieden | **nicht uebernehmbar** - das Portal zeigt weiter 5.000, nicht die Formel |
| Logo-Original "identisch mit `assets/referenzbilder/Logo_Nebelseetal_20261106.png`" | Byte-verschieden (6.651.525 gegen 6.645.755), aber **0 abweichende Pixel** bei 3500 x 3500 (Unterschiedsrechteck `None`) | **stimmt im Bild**, nicht in den Bytes |
| Stilreferenzen "vermutlich dieselben Bilder" | 16 Bilddateien: **7 byte-gleich**, **7 weitere pixelgleich** (mittlere Abweichung 0,0 nach Vergleich); neu sind nur `UEBERSICHT_burg_und_referenzen_je_fraktion.jpg` und `oberflaeche/original_logo_alt.png` | **bestaetigt** - 14 von 16 sind vorhandenes Material |
| Burg- und Drachenvorlagen | alle 6 Burgen pixelgleich mit `assets/icons/burgen/burg_01..06.png`, alle 3 Drachen pixelgleich mit `assets/bilder/drache_*.png` | **kein neues Bildmaterial** - das Paket bringt Daniels eigene Bilder zurueck |
| `CODE_P4_Vier_Zeichenmodule_der_Karten.md` | liegt unter `docs/audits/code/` | **stimmt** |
| Schritt 1 nennt `VORGABEN_WELTEN_UND_BOTS_20261103.md` | liegt unter `docs/`, nicht `docs/design/` | **Pfadfehler**, die Datei ist vorhanden |

**Summe der Bilder:** 35 Bilddateien im Paket. **24 davon sind pixelgleich** mit vorhandenen
Projektdateien (6 Burgen, 3 Drachen, 14 Stilreferenzen, 1 Logo), 4 sind Ableitungen des Logos
(1200 px, zugeschnitten, Vorschau dunkel und hell), 7 sind Pruef-, Uebersichts- oder Altbilder.
**Echte neue Gestaltung sind genau zwei Dateien: die Stilproben A und B der Weltkarte.**

### 3. Widersprueche, die erst im Abgleich mit den Dokumenten sichtbar wurden

**W-D6 - Nebelsee auf der Weltkarte ist heute NICHT gesperrt.** Das Paket setzt in Abschnitt 1
"Nebelsee auf der Weltkarte unbesetzbar (Daniel)". Im Projekt steht das Gegenteil fest:
`src/portalraum.py` Z. 408-411 "Das Gelaende auf der Weltkarte hat KEINE Bauplatz-, Rohstoff- oder
Ertragswirkung" (Daniel 01.11.2026, Register 91/92), und `_dorf_versetzen` (S-3/S-4) prueft Dorf,
Auftraege, Welt, Position, Feld frei, Mana, Sperre - **kein Gelaende**. Auf einer Nebelsee-Kachel
kann heute ein Dorf landen. Zwei Aussagen Daniels stehen damit gegeneinander; das ist eine
Entscheidung, keine Reparatur.

**W-D7 - Sumpf: der Paketvorschlag ist eine NEUE Regel.** `data/gelaende.json` fuehrt `sumpf` mit
`bebaubar: false` - das gilt fuer die SIEDLUNGSkarte. Fuer die Weltkarte gibt es keine Regel;
"Sumpf unbesetzbar" ist ein Vorschlag, keine Wiedergabe des Projekts.

**W-D8 - der Preis im Portal.** Siehe Zeile 10 oben: 5000 Mana sind belegt und von Daniel
entschieden, die Formel aus `welten.json` ist ein Vorschlag. Das Paket wuerde im Portal die falsche
Zahl zeigen.

**W-D9 - isometrisch ist teurer als es klingt (Zahlen fuer D-2).** Heute rechnet
`_portal_zelle(kante) = max(4, 400 // kante)` **20 px** je Feld, die Karte ist 400 x 400 px.
Isometrisch nach Paket 7.1 (`bild_x = (x-y)*64`, `bild_y = (x+y)*32`) waere sie **2560 x 1280 px**,
also die 32-fache Flaeche. Betroffen waeren mindestens: `_portal_zelle`, die Kartenzeichnung,
`_portal_klick`, `_feld_im_raster`, `_bot_dorf_an`, `_marsch_an`, `_marsche_zeichnen`, die Dorf- und
Drachenanker (`_ort_feld`) und die Statuszeile aus S-4 - also das, was in S-4 gerade entstanden ist,
plus eine Zoom- oder Rollstufe, die es heute nicht gibt. **113 Zeilen** in `src/main.py` nennen
"portal".

### 4. Was offen bleibt

- Ob die Stilprobe A mit den sieben Gelaendearten als Testkarte traegt, entscheidet erst D-3.
- Ob die drei blauen Banner im kleinsten Zoom unterscheidbar sind (W-D5), bleibt ein Bildtest (D-4).
- Die Bildinhalte der Stilproben sind nur sichtgeprueft, nicht Feld fuer Feld gegen `gelaende.json`.

### 5. Fragen an Daniel (einzeln im Chat gestellt)

1. **D-2 (Raster):** flaches Raster mit gemalten Kacheln behalten, isometrisch umbauen, oder erst
   eine Testkarte flach (D-3) und danach entscheiden.
2. **W-D6 (Gelaende auf der Weltkarte):** Nebelsee sperren (Sumpf frei), Nebelsee und Sumpf sperren,
   oder keine Gelaendesperre (Stand der Entscheidung 01.11.2026).
