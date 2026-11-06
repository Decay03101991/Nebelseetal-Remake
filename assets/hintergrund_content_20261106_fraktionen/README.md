# Fraktions-Panoramen (Design Content Nr. 3, 06.11.2026)

Daniel hat am 06.11.2026 zwischen 04:53 und 05:07 **fuenf fertig geschnittene Bilder** geliefert
(Generator, Ablage auf dem Desktop) - **Panoramen je Fraktion** plus eine Collage aller sechs
Fraktionen. Sie liegen hier als **Vorlagen fuer Design-Auftraege**: Fraktionsseiten, Menuehintergruende,
Kapitelauftakte, Bildtafeln. **Nichts davon ist im Spiel verdrahtet** - kein Code liest diesen Ordner.

| Datei | Masse | Bytes | Thema |
|---|---|---|---|
| `Gemini_Collage_aller_6_Fraktionen_Nebelseetal_Hintergrundbilder.jpg` | 1637x640 | 1.009.102 | alle sechs Fraktionen nebeneinander |
| `Ghule_Panorama_Nebelseetal_Vorlage.jpg` | 1637x640 | 837.907 | Fraktion Ghule |
| `Gnome_Panorama_Nebelseetal_Vorlage.jpg` | 1637x640 | 974.763 | Fraktion Gnome |
| `Menschen_Panorama_Nebelseetal_Vorlage.jpg` | 1637x640 | 904.146 | Fraktion Menschen |
| `Zwerge_Panorama_Nebelseetal_Vorlage.jpg` | 1637x640 | 992.620 | Fraktion Zwerge |

Alle fuenf sind **hashgleich mit der Lieferung** (SHA256 in `VERZEICHNIS.json`), Namen und Bildinhalte
unveraendert - kein Schnitt, keine Skalierung, kein Umbenennen.

## Wie sie einzuordnen sind (gemessen)

- **Alle fuenf sind Szenen ohne Freistellung** (RGB ohne Alphakanal). Damit gilt die Lehre vom
  04.11.2026: Menue- und Dialogware (Panorama, Bildtafel, Titel), **kein Kartenmotiv**. Was auf das
  Spielfeld soll, braucht freigestellte Einzelmotive.
- **Einheitliches Format 1637x640** - die fuenf Blaetter passen ohne Skalierung nebeneinander und in
  einen breiten Kopfbereich.
- **Die Collage ist eine Uebersicht, kein Einzelbild**: fuer einen Fraktionswechsel den passenden
  Einzel-Panoramastreifen nehmen, nicht die Collage.

## Abgrenzung zu den anderen Bildordnern

| Ordner | Inhalt |
|---|---|
| `assets/hintergrund_content_20261104/` | 12 Uebersichten mit mehreren Kacheln (ungeschnitten), 1998x1859 |
| `assets/hintergrund_content_20261106/` | 14 Einzelbilder (Ghule, Gnome, Zwerge, Elfenwalddorf, Vorlagen), 1168x784 bis 2752x1536 |
| **`assets/hintergrund_content_20261106_fraktionen/`** | **diese fuenf Fraktionspanoramen, 1637x640** |

## Was hier NICHT passiert ist

- Kein Einbau in Menues, Overlays oder Fraktionsseiten (kein Design-Auftrag dazu - Daniel: "Einbau
  spaeter, sobald Designauftraege anstehen").
- Keine Aenderung an `assets/original/` oder `assets/icons/original_units/`.
