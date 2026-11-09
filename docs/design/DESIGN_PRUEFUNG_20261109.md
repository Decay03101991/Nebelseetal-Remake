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
