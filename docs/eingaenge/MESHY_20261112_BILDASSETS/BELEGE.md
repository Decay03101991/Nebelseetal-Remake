# Meshy-Bildassets vom 12.11.2026 — Ablage und Einordnung

**Quelle:** Daniels Meshy-AI-Chat (Bildgenerierung), Rohordner `C:\Users\saras\Desktop\meshy`.
**Abgelegt:** 12.11.2026. **Verfahren:** kopiert und hashgleich geprueft, nichts umbenannt ohne Zuordnung
(siehe Tabelle), Originale bleiben auf dem Desktop, bis Daniel sie raeumt.

## 1. Was da ist (14 Dateien, alle hashgleich)

### Panoramen der sechs Voelker (je 1536 x 864, 16:9, RGB ohne Alpha)

| Datei | Volk | Byte | SHA256 |
|---|---|---|---|
| `panorama/ref_panorama_menschlich.png` | menschlich | 2.869.091 | `f8353206baf8` |
| `panorama/ref_panorama_zwergisch.png` | zwergisch | 2.852.315 | `27d4bc146ba8` |
| `panorama/ref_panorama_elfisch.png` | elfisch | 3.002.368 | `ae4bbf52b4cc` |
| `panorama/ref_panorama_trolle.png` | Trolle | 2.649.668 | `f849d789d81b` |
| `panorama/ref_panorama_ghule.png` | Ghule | 2.576.286 | `9aea465ac1de` |
| `panorama/ref_panorama_gnome.png` | Gnome | 2.861.114 | `331429607da4` |

### Elfen: Wappen, Banner und drei Gebaeude (das ist der vollstaendige Satz fuer EIN Volk)

| Datei | Was zu sehen ist | Maße | Byte | SHA256 |
|---|---|---|---|---|
| `elfen/ref_elfen_wappen_und_banner.png` | **Wappenschild UND Banner** mit demselben Motiv (Stern, silbernes Blatt, Goldranken, blaue Edelsteine) auf **einfarbig grauem Studiohintergrund** | 1024 x 1024 | 1.486.366 | `159189578fb7` |
| `elfen/ref_elfen_bibliothek.png` | Bibliothek im Baum: Armillarsphaere, Regale, blaue Kristalle, Blick auf Wasserfaelle | 1536 x 864 | 2.676.294 | `f4d28ab3062d` |
| `elfen/ref_elfen_kriegerakademie.png` | Kriegerakademie | 1536 x 864 | 2.587.529 | `b2729685b697` |
| `elfen/ref_elfen_stellmacher.png` | Stellmacher-Werkstatt | 1536 x 864 | 2.788.933 | `b5dcaf6494ad` |

**Geprueft (eigene Sicht):** die drei Elfen-Gebaeudebilder enthalten **keinen Text und keine
Bedienelemente** — reine Hintergruende. Das Wappenbild ist ein **Satz aus zwei Gegenstaenden**
(Schild links, Banner rechts), nicht ein einzelnes Wappen.

### Die Vorgaben, mit denen Meshy gefuettert wurde (Daniels eigene Referenzen)

| Datei | Maße | Byte |
|---|---|---|
| `vorgabe/ref_vorgabe_gnome_panorama.jpg` | 830 x 335 | 119.921 |
| `vorgabe/ref_vorgabe_gnome_werkstatt.jpg` | 400 x 293 | 54.612 |
| `vorgabe/ref_vorgabe_ghule_festung.jpg` | 402 x 294 | 48.381 |
| `vorgabe/ref_vorgabe_zwerge_festung.jpg` | 407 x 298 | 49.598 |

## 2. Wofuer sie taugen — und wo die Luecke ist

**Gemessen, nicht geschaetzt:** die Gebaeudeflaeche im Spiel ist **1142 x 1120 px (1:1)**
(Daniels Entscheidung, Register 469). Die Meshy-Bilder sind **1536 x 864 (16:9)**.

Das heisst: als **Referenz und Stilvorgabe** sind sie sofort brauchbar, als **fertiges
Hintergrundbild** nicht. Ein 16:9-Bild auf 1:1 zu bringen kostet **rund 45 Prozent der Breite**
oder es muss oben und unten ergaenzt werden. Zwei Wege, beide vertretbar:

1. **Malen lassen:** Meshy noch einmal mit dem Auftrag 1:1 (1142 x 1120) — dann passt es ohne Beschnitt.
2. **Beschneiden und ergaenzen:** Mitte 1142 breit herausschneiden, oben/unten mit Himmel und
   Gelaende in derselben Palette fortsetzen. Aufwand pro Bild, aber die Komposition bleibt.

**Das Elfen-Wappen** ist ein Satz aus zwei Gegenstaenden auf grauem Grund. Fuer den Spieler-Marker
brauchen wir **ein** Wappen, freigestellt (Alpha) in 256 x 256 (Master) und 128 x 128 (Abzeichen);
das Banner ist ein eigener Gegenstand und im Spiel bisher nicht vorgesehen.

## 3. Was noch fehlt (gemessen am Auftrag in `docs/auftraege/`)

- **fuenf Voelker ohne Wappen und ohne Gebaeude** (menschlich, zwergisch, Trolle, Ghule, Gnome)
- **siebzehn weitere Gebaeude** je Volk (20 Gebaeude insgesamt, fuer Elfen sind drei da plus Panorama)
- **sieben Gelaendekacheln 64 x 64 nahtlos** — fuer die Weltkarte, das wichtigste fehlende Stueck
- **Icons**: 28 Einheiten, 18 Waren, neun Menuepunkte
- **Leistenband** (64 x 34 wiederholbar plus zwei Endstuecke 16 x 34) und **Knoepfe** 48 x 48
- **Tor, Ladebild, Kopfband** je Volk

## 4. Regeln fuer die Weiterverwendung

- Die Panoramen sind **Stilvorgabe** — wer neue Bilder baut, haelt sich an Lichtrichtung
  (warm von links oben), Nebel im Tal und die gedaempfte Palette.
- Der Wappen-Satz ist **nicht** freigestellt: vor jeder Verwendung im Spiel muss ein Alpha-Schnitt
  her, und der graue Grund darf nicht mitwandern.
- Keine Datei ohne Eintrag hier und ohne Hash in den Bestand — sonst ist nicht nachvollziehbar,
  welche Fassung im Spiel landet.
