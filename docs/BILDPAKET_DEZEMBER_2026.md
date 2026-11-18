# Dezember-Bildpaket - Bestellliste und Abnahme (Stand 18.11.2026, Sitzung 49)

**Wozu diese Datei.** Sie sagt in EINER Tabelle, welche Bilddateien der Dezember braucht, wie gross
sie sein muessen, wohin sie gehoeren und welche Stelle im Spiel sie aktiviert. Sie ist aus
`docs/BILDBEDARF_ENTSCHEIDUNGEN_20261113.md` (Daniels Entscheidungen F-101, F-104, F-106 und F4) und
Claudes Antwort Nr. 19 abgeleitet - **nichts davon ist neu entschieden**, nur zusammengefuehrt und
nachgerechnet.

**Die maschinenlesbare Fassung steht in `data/bildpaket_dezember.json`** (die EINE Quelle der
Sollwerte). Die Tabelle unten wird aus dieser Datei erzeugt, damit beide nicht auseinanderlaufen.
Geprueft wird mit `python -X utf8 tools/bildpaket_pruefen.py`; die Wache ist
`tests/test_bildpaket_dezember.py`.

## 1. Eine Zahl korrigiert: es sind 18 Dateien, nicht 16

In `docs/BILDBEDARF_ENTSCHEIDUNGEN_20261113.md` und in `docs/FRAGEN_AN_DANIEL_20261112.md` steht,
der Dezember-Bedarf sei von 105 auf **16** Bilder geschrumpft. Die Aufzaehlung daneben ergibt etwas
anderes:

| Gruppe | B1 | B2 | B5 | B8 | B9 | B10 | B12 | B13 | Summe |
|---|---|---|---|---|---|---|---|---|---|
| Dateien | 1 | 2 | 2 | 6 | 1 | 2 | 3 | 1 | **18** |

Nachgerechnet am 18.11.2026: 1 + 2 + 2 + 6 + 1 + 2 + 3 + 1 = **18**. Die Gruppen bleiben acht; die
Zahl 16 war ein Zaehlfehler. Kein Bild kommt hinzu und keines faellt weg - die Lieferung ist nur
zwei Dateien groesser als notiert.

## 2. Die 18 Dateien

| Nr | Kennung | Was / wohin | Anzeige | Datei (4x, F-101) | Format | Zielpfad | Wer sie aktiviert |
|---|---|---|---|---|---|---|---|
| B1 | `ruine_weltkarte` | Feld eines besiegten Drachen (Portal, Weltkarte) | 19-44 px, quadratisch | **176 x 176** | PNG, Alpha | `assets/bilder/ruine_weltkarte_176.png` | data/drachen.json: figur.ruine_bild auf den Dateinamen setzen und figur.ruine_platzhalter auf false |
| B2 | `drache_gruen` | Tardas der Gruene (Portal, Weltkarte) - heute zeigt er drache_blau.png | 19-44 px | **176 x 176** | PNG, Alpha | `assets/bilder/drache_gruen_176.png` | data/drachen.json: drachen[drache_d03].bild auf den Dateinamen setzen |
| B2 | `drache_rot` | Salmur der Rote (Portal, Weltkarte) - heute zeigt er drache_lila.png | 19-44 px | **176 x 176** | PNG, Alpha | `assets/bilder/drache_rot_176.png` | data/drachen.json: drachen[drache_d05].bild auf den Dateinamen setzen |
| B5 | `startbild_anmelden` | Tor (Passwortschutz) - das Panorama liegt hinter dem Formular | 1024 x 720 | **4096 x 2880** | JPG, deckend | `assets/referenzbilder/startbild_anmelden_4096x2880.jpg` | src/main.py: STARTBILD_MOTIVE['anmelden'] auf den Dateinamen setzen |
| B5 | `startbild_laden` | Ladeansicht und Speicher-Nebenfenster (F5, Register 644: eingepasst, nie vergroessert) | 1024 x 720 | **4096 x 2880** | JPG, deckend | `assets/referenzbilder/startbild_laden_4096x2880.jpg` | src/main.py: STARTBILD_MOTIVE['laden'] auf den Dateinamen setzen |
| B8 | `kopfband_menschlich` | Kopfband der Portal-Uebersicht (Volk der Spielersiedlung) | bis 1127 px breit, Hoehe bis 200 px | **4508 x 868** | JPG oder PNG, deckend | `assets/bilder/portal_kopfband_menschlich_4508x868.png` | nichts umstellen - Datei ablegen, dann spielt sie das Band |
| B8 | `kopfband_zwergisch` | Kopfband der Portal-Uebersicht | bis 1127 px breit, Hoehe bis 200 px | **4508 x 868** | JPG oder PNG, deckend | `assets/bilder/portal_kopfband_zwergisch_4508x868.png` | nichts umstellen - Datei ablegen |
| B8 | `kopfband_elfisch` | Kopfband der Portal-Uebersicht (Stilvorlage: Meshy-Waldelfen, F-103) | bis 1127 px breit, Hoehe bis 200 px | **4508 x 868** | JPG oder PNG, deckend | `assets/bilder/portal_kopfband_elfisch_4508x868.png` | nichts umstellen - Datei ablegen |
| B8 | `kopfband_trolle` | Kopfband der Portal-Uebersicht | bis 1127 px breit, Hoehe bis 200 px | **4508 x 868** | JPG oder PNG, deckend | `assets/bilder/portal_kopfband_trolle_4508x868.png` | nichts umstellen - Datei ablegen |
| B8 | `kopfband_ghule` | Kopfband der Portal-Uebersicht (heute das einzige vorhandene Band, 780 x 150) | bis 1127 px breit, Hoehe bis 200 px | **4508 x 868** | JPG oder PNG, deckend | `assets/bilder/portal_kopfband_schmiede_dorf_ghule_4508x868.png` | nichts umstellen - Datei ablegen |
| B8 | `kopfband_gnome` | Kopfband der Portal-Uebersicht | bis 1127 px breit, Hoehe bis 200 px | **4508 x 868** | JPG oder PNG, deckend | `assets/bilder/portal_kopfband_gnome_4508x868.png` | nichts umstellen - Datei ablegen |
| B9 | `weltkarte_goldrahmen` | Rahmen um das Gelaendekaestchen der Weltkarte (D-5b) | 400-920 px | **3680 x 3680** | PNG, Alpha | `assets/icons/gebaeude/rahmen/weltkarte_goldrahmen_3680.png` | data/gebaeude_motive.json: kachelrahmen.weltkarte auf den Dateinamen setzen; kachelrahmen.weltkarte_rand danach NEU messen (Bandbreite bei 400 px Bezug) |
| B10 | `kachelrahmen_ruhe` | Feldrahmen der Siedlungskarte, liegt auf jedem Feld (Deckkraft 35 Prozent) | 57-64 px | **256 x 256** | PNG, Alpha | `assets/icons/gebaeude/rahmen/kachelrahmen_ruhe_256.png` | data/gebaeude_motive.json: kachelrahmen.ruhe auf den Dateinamen setzen |
| B10 | `kachelrahmen_auswahl` | Hervorgehobener Feldrahmen der Siedlungskarte (Deckkraft 100 Prozent) | 57-64 px | **256 x 256** | PNG, Alpha | `assets/icons/gebaeude/rahmen/kachelrahmen_auswahl_256.png` | data/gebaeude_motive.json: kachelrahmen.auswahl auf den Dateinamen setzen |
| B12 | `leiste_mitte` | Mittelkachel des 9-Slice-Bandes der Ressourcenleiste (wird wiederholt, nie gedehnt) | 64 x 34 | **256 x 136** | PNG, Alpha | `assets/bilder/leiste_mitte_256x136.png` | data/ressourcenleiste.json: band.datei auf den Dateinamen setzen |
| B12 | `leiste_ende_links` | Linkes Endstueck des Bandes | 16 x 34 | **64 x 136** | PNG, Alpha | `assets/bilder/leiste_ende_links_64x136.png` | data/ressourcenleiste.json: band.ende_links auf den Dateinamen setzen - kein Code noetig |
| B12 | `leiste_ende_rechts` | Rechtes Endstueck des Bandes | 16 x 34 | **64 x 136** | PNG, Alpha | `assets/bilder/leiste_ende_rechts_64x136.png` | data/ressourcenleiste.json: band.ende_rechts auf den Dateinamen setzen - kein Code noetig |
| B13 | `marktplatz_kennzeichen` | Kennzeichen der Marktplatz-Ansicht (F3a, Register 639: auf 96 px eingepasst) | 96 x 96 | **384 x 384** | PNG, deckend | `assets/bilder/marktplatz_kennzeichen_384.png` | src/main.py: MARKTPLATZ_KENNZEICHEN auf den Dateinamen setzen (MARKTPLATZ_KENNZEICHEN_PX bleibt 96) |

## 3. Wo die Bilder andocken (alle 18 haben eine Stelle, gemessen 18.11.2026)

- **B12 Endstuecke links und rechts:** die Felder `band.ende_links` und `band.ende_rechts` sind am
  18.11.2026 gebaut worden (`main._leiste_ende_bild`, Register 658). Ist ein Pfad eingetragen und die
  Datei da, zeichnet sie das Endstueck - **auf genau 16 x 34 eingepasst, nie verzerrt**; fehlt die
  Datei, bleibt die gezeichnete Flaeche mit Goldrand und Goldraute stehen, kein Pixel verschiebt sich.
  Geprueft: `tests/test_ressourcenleiste_t08.py` Abschnitt 9 (mit 4x-Datei und mit quer geliefertem
  Bild, beides 16 x 34), im Lauf 130/0/0.
- **B8 ist der bequemste Teil:** die sechs Zielpfade stehen schon in `data/portal_kopfbaender.json` -
  Datei ablegen genuegt, nichts umstellen.
- **Die uebrigen 16 Dateien** haengen an `data/drachen.json` (B1, B2), an `src/main.py` ->
  `STARTBILD_MOTIVE` (B5) und `MARKTPLATZ_KENNZEICHEN` (B13), an `data/gebaeude_motive.json` ->
  `kachelrahmen` (B9, B10) und an `data/ressourcenleiste.json` -> `band.datei` (B12 Mitte).

## 4. Regeln fuer die Lieferung (Daniels Entscheidungen)

1. **4x der groessten Anzeige** (F-101) - auch bei grossen Flaechen. Eine 4508 x 868-Datei ist damit
   in Ordnung, auch wenn sie einige MB gross wird.
2. **Hochrechnen ist erlaubt** (F-106): in der groessten Ausgabe erzeugen, danach mit gutem Verfahren
   hochrechnen. **Jede** hochgerechnete Datei bekommt einen Vermerk mit Ausgangsgroesse, Verfahren und
   Datum - die Vorlage steht in Abschnitt 6.
3. **Keine Schrift im Bild.** Die Beschriftung macht das Spiel; Text im Bild waere bei jeder
   Fenstergroesse falsch.
4. **Kartenbilder quadratisch anlegen**, auch wenn das Motiv hochkant ist (Motiv mittig, Rest
   durchsichtig).
5. **Transparenz nur, wo sie verlangt ist:** Spalte Alpha in der Tabelle. Die Fuellbilder (B5, B8)
   sind deckend, die Zeichen (B1, B2, B9, B10, B12) brauchen Alpha. Bei PNG heisst deckend Farbtyp 2
   (RGB) und mit Alpha Farbtyp 6 (RGBA) - das prueft das Werkzeug seit 18.11.2026 (Abschnitt 5).
6. **Waren, Einheiten und Karten-Gebaeude behalten ihre Icons** (F-104) - dafuer wird nichts
   gezeichnet.

## 5. Abnahme: ein Befehl, eine Tabelle

```
python -X utf8 tools/bildpaket_pruefen.py
```

Das Werkzeug misst jede Datei am Dateikopf (PNG und JPEG, ohne Pillow) und urteilt je Datei:
`fehlt` / `zu klein` / `zu gross` / `kein Alpha` / `Farbtyp` / `Format` / `kaputt` / `ok`. Ein
abgeschnittenes Bild faellt auf (PNG ohne IEND, JPEG ohne EOI), damit keine halbe Datei als Lieferung
durchgeht. Mit `--streng` liefert der Aufruf den Code 1, solange etwas fehlt - so kann ein spaeterer
Lauf ihn als Wache nutzen.

**Farbtyp (seit 18.11.2026, Register 676):** `alpha: true` verlangt bei PNG Farbtyp 6 (RGBA),
`alpha: false` Farbtyp 2 (RGB). Ein RGBA-Bild, das deckend bestellt ist, faellt damit auf; vorher
galt es ohne Pruefung als Bild mit Transparenz. Nicht geprueft wird, ob die Bildpunkte eines
RGBA-Bildes wirklich Transparenz tragen - dafuer muesste das Bild entpackt werden (offene Luecke).

**Massgenauigkeit (seit 18.11.2026, Register 676):** `toleranz_px` je Eintrag in
`data/bildpaket_dezember.json`. 0 px (B1, B2, B10, B12, B13) heisst: jedes Mass muss exakt stimmen,
sonst kippt das Seitenverhaeltnis; 1 px (B5, B8, B9) heisst: eine Seite darf um einen Bildpunkt
abweichen (bei 4508 px Breite sind das 0,02 Prozent). Geprueft werden BEIDE Seiten. Die
Leisten-Endstuecke sind 8 : 17 (64 x 136), die Mittelkachel 32 : 17 (256 x 136) - die Wache rechnet
beides nach.

**Stand 18.11.2026:** 0 von 18 Dateien vorhanden (das ist der ehrliche Ist-Stand, nicht der Wunsch).

## 6. Vorlage fuer den Vermerk einer hochgerechneten Datei (F-106)

```
| Datei | Ausgangsgroesse | Verfahren | Datum | Bearbeiter |
|---|---|---|---|---|
| (Zielpfad) | (z. B. 1024 x 720) | (z. B. Lanczos 4x, danach leicht nachgeschaerft) | (Datum) | (wer) |
```

Der Vermerk gehoert unter diese Datei (oder in eine eigene `docs/BILDPAKET_202612*.md`), sobald die
erste hochgerechnete Datei ins Projekt kommt.

## 7. Woher die Zahlen kommen

| Angabe | Quelle |
|---|---|
| 4x Anzeige, hochrechnen erlaubt | Daniels Antworten F-101 und F-106 (`docs/BILDBEDARF_ENTSCHEIDUNGEN_20261113.md`, Abschnitte 1 und 5) |
| welche Bilder ueberhaupt | Claudes Antwort Nr. 19 (`docs/eingaenge/CLAUDE_20261113_ANTWORT_AUFTRAG18_BILDBEDARF.md`), nachgerechnet in Register 622 |
| dass B4 nicht dazugehoert | Daniels Antwort 16.11.2026 in `docs/FRAGEN_AN_DANIEL_20261112.md` (F4) |
| die Anzeigegroessen | im Code gemessen: `PORTAL_KOPFBAND_MASSE` 780 x 150, `MARKTPLATZ_KENNZEICHEN_PX` 96, `kachelrahmen.px` 64, `band` 64 x 34 und 16 x 34, `KOPFBAND_HOECHSTHOEHE` 200 |
