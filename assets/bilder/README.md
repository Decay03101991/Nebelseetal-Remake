# Assets in `assets/bilder/`

Hier stehen die Bilder, die im Spiel benutzt werden (Regel: `docs/design/DESIGN_ARBEITSWEISE.md`,
Abschnitt 1 - "erst mit dem Einbau wandert die gebrauchte Datei nach `assets/...` und bekommt dort
eine Zeile in der README, wo sie eingesetzt wird"). Rohbilder und Stilvorlagen liegen weiter unter
`archiv/design/` und sind gitignoriert.

Das vollständige Inventar aller Bilddateien des Projekts steht in `docs/BILDINVENTAR.md`.

| Datei | Maße | Herkunft | Wird eingesetzt in |
|---|---|---|---|
| `portal_kopfband_schmiede_dorf_ghule_780x150.png` | 780 x 150 px, 254.385 Byte, SHA256 `3f5a0c693ce7f66b784c0268f3991a12377c2d8c8002455d068e099bbfa97649` | Chris Fred Däubner, Lieferung "NEBELSEETAL png's" (Ablage: `archiv/design/20261109_chris_bildpaket/`, Schnitt `geschnitten/band_schmiede_dorf_ghule_780x150.png`, byte-gleich übernommen) | Portal-Übersicht, Platz S1: Kopfband über dem Titel "Portal" (`src/main.py`, `PORTAL_KOPFBAND`), D-5 vom 09.11.2026 |

| `marktplatz_kennzeichen_96.png` | 96 x 96 px, 21.317 Byte | Chris Fred Däubner, Lieferung „NEBELSEETAL png's“, Kachel `markt_handel`, auf Anzeigegröße verkleinert (Pillow, LANCZOS) | Marktplatz-Ansicht, links neben dem Titel (`src/main.py`, `MARKTPLATZ_KENNZEICHEN`), D-5b vom 09.11.2026 |

**Warum nur eine Zeile:** die älteren Bilder dieses Ordners (`daniel_portrait*`, `drache_*`,
`logo_nebelseetal_klein*`) sind vor dieser README entstanden; ihre Herkunft und Verwendung stehen in
`docs/BILDINVENTAR.md`. Sie werden hier nicht nachgetragen, um keine zweite, abweichende Quelle zu
erzeugen.
