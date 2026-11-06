# Bildcontent Nr. 2 (Daniel, 06.11.2026)

Daniel hat am 06.11.2026 zwischen 02:38 und 03:04 **14 fertige Einzelbilder** liefern lassen (Generator,
auf dem Desktop abgelegt) und sie thematisch benannt. Sie liegen hier als **Vorlagen fuer Design-
Auftraege** - Menue- und Overlay-Hintergruende, Fraktionsseiten, Bildtafeln, Kapitelauftakte.
**Nichts davon ist im Spiel verdrahtet.** Kein Code liest diesen Ordner.

## Wo was liegt

`fraktionen/` - zehn Bilder zu den Voelkern (Elfen, Ghule, Gnome, Zwerge), je Szene mit Namen der
Umgebung im Dateinamen (Stadt, Minen). `vorlagen/` - vier Blaetter mit Vorlagen: Haeuser, Burgumgebung,
zwei Hintergrundblaetter.

| Datei | Ordner | Masse | Bytes |
|---|---|---|---|
| `Elfenwalddorf_Hintergrund_Nebelseetal.jpg` | fraktionen | 2752x1536 | 1523602 |
| `Ghule1_Hintergrund_Nebelseetal.jpg` | fraktionen | 1168x784 | 526124 |
| `Ghule2_Hintergrund_Nebelseetal.jpg` | fraktionen | 1168x784 | 480487 |
| `Ghule3_Hintergrund_Nebelseetal.jpg` | fraktionen | 1168x784 | 481328 |
| `Ghule4_Hintergrund_Minen_Nebelseetal.jpg` | fraktionen | 1168x784 | 476983 |
| `Ghule4_Hintergrund_Nebelseetal.jpg` | fraktionen | 1168x784 | 451186 |
| `Ghule5_Hintergrund_Stadt_Nebelseetal.jpg` | fraktionen | 1168x784 | 451745 |
| `Gnome1_Hintergrund_Minen_Nebelseetal.jpg` | fraktionen | 1168x784 | 375229 |
| `Gnome1_Hintergrund_Stadt_Nebelseetal.jpg` | fraktionen | 1168x784 | 473668 |
| `Hintergrundcontent_Nebelseetal.jpg` | vorlagen | 1000x558 | 319806 |
| `Hintergrundcontent_Nebelseetal1.jpg` | vorlagen | 1000x560 | 175761 |
| `Häuservorlagen_Nebelseetal.jpg` | vorlagen | 1637x640 | 882977 |
| `Stilvorlagen_BurgumgebungsVorschläge_Nebelseetal.jpg` | vorlagen | 1376x768 | 1030106 |
| `Zwerge_im_Nebelseetal_Hintergründe.png` | fraktionen | 2010x787 | 3115931 |

Alle 14 Dateien sind **hashgleich mit der Lieferung** (SHA256 in `VERZEICHNIS.json`), Namen und
Bildinhalte unveraendert - kein Schnitt, keine Skalierung, kein Umbenennen.

## Wie sie einzuordnen sind (gemessen, nicht angenommen)

- **Alle 14 sind Szenen im Rahmen, keine freigestellten Motive.** 13 sind RGB ohne Alphakanal; das eine
  PNG (`Zwerge_im_Nebelseetal_Hintergründe.png`, RGBA) hat **0,0 Prozent Transparenz**. Damit gilt die
  Lehre vom 04.11.2026: solche Blaetter sind Menue- und Dialogware (Hintergrund, Bildtafel, Titel),
  **kein** Kartenmotiv. Was auf das Spielfeld soll, braucht freigestellte Einzelmotive aus dem
  Generator - das ist ein eigener Auftrag.
- **Gross genug fuer den Vollbild-Einsatz:** das Elfenwalddorf-Bild misst 2752x1536, das Zwerge-Blatt
  2010x787. Fuer Menuehintergruende ist damit nichts hochskaliert.
- **Die Ghule- und Gnome-Bilder gibt es in zwei Fassungen je Thema** (einmal neutral, einmal mit
  Umgebung im Namen) - beim Einbau das passende waehlen, nicht beide nebeneinander legen.

## Was hier NICHT passiert ist

- Kein Einbau in Menues, Overlays oder Karten (kein Design-Konzept, kein Auftrag dazu).
- Keine Alpha-Messung als Freistellung: das Zwerge-PNG ist deckend (0,0 Prozent transparent).
- Keine Aenderung an `assets/original/` oder `assets/icons/original_units/` - Nutzerbilder bleiben
  unantastbar.
