# Bildbedarf — was Daniel entschieden hat (13.11.2026, Sitzung 44)

**Grundlage:** Claudes Antwort auf Auftrag Nr. 18 (`docs/eingaenge/CLAUDE_20261113_ANTWORT_AUFTRAG18_BILDBEDARF.md`),
nachgerechnet in Register 622, und fünf Einzelentscheidungen von Daniel (F-100 bis F-104), gefragt nach
Arbeitsregel 7. **Diese Datei ersetzt die Vorschlagsliste B1–B13, soweit Daniel entschieden hat.**

---

## 1. Die Entscheidungen im Wortlaut

| Frage | Daniels Antwort (wörtlich) | Was daraus folgt |
|---|---|---|
| **F-99** Verzerrung | „Code reparieren: `_motivbild_skaliert` passt ein statt zu zerren (wie `_lager_symbol`), mit Wache und vorher/nachher gemessen“ | **gebaut** (Register 624): 18×18 → 11×18, Wache, T4 235/235 |
| **F-100** Abzeichen auf der Karte | „Abzeichen ganz weg von der Weltkarte — die Fraktion erkennt man an der Burg“ | **gebaut** (Register 627): nur noch die Burg; Wache „genau ein Bild je Dorf“ |
| **F-101** Dateigrößen | „4× überall — scharf auch auf 200-%-Schirmen, dafür große Dateien“ | **Vorgabe für Dezember**: 4 × Anzeigegröße, auch bei großen Flächen |
| **F-102** Portraitfoto | „Ja, aus dem Paketbau ausschließen, die Datei aber im Projekt lassen“ | **gebaut** (Register 627): `tools/paket_ausschluss.py`, beide Bauwege, Wache 14/0/1 |
| **F-103** Meshy-Bilder | „Die Bilder von Meshy sind quasi die Referenz zum Spiel … benutz sie vor allem auch als Referenz dafür, was wir für Designs brauchen“ | **Stilvorlage**, kein Spielinhalt; Maßstab für die Waldelfen-Fraktion |
| **F-104** Waren/Einheiten/Gebäude | „Waren und Einheiten behalten ihre Icons, das bleibt fix, genau wie die Gebäude, die auf der Siedlungskarte erscheinen und produzieren“ | **B6, B7 und B11 fallen weg** — es werden keine neuen Waren-, Einheiten- oder Gebäude-Icons gebraucht |

---

## 2. Was von Claudes Liste übrig bleibt

| # | Was | Anzeige | Datei bei 4× (F-101) | Stand |
|---|---|---|---|---|
| B1 | Ruine auf der Weltkarte (Feld eines besiegten Drachen) | 19–44 px | 176 × 176 | **offen** |
| B2 | Drache in Grün und in Rot (heute zeigen Tardas/Salmur blau und lila) | 19–44 px | 176 × 176 | **offen** |
| B5 | Startbilder Anmelden/Laden | 1024 × 720 | **4096 × 2880** | offen |
| B8 | Kopfband je Volk (heute nur eines, Motiv Ghule) | bis 1127 px breit | 4508 × 868 | offen |
| B9 | Goldrahmen der Weltkarte | 400–920 px | 3680 × 3680 | offen |
| B10 | Kachelrahmen Ruhe/Auswahl der Siedlungskarte | 57–64 px | 256 × 256 | offen |
| B12 | Ressourcenleiste (drei Stücke) | 64 × 34 / 16 × 34 | 256 × 136 / 64 × 136 | offen |
| B13 | Marktplatz-Kennzeichen | 96 px | 384 × 384 | offen |
| B4 | Einzelansicht der Gebäude (Motiv vor Panorama) | 1:1, 1142 × 1120 | 1:1 bleibt | **Zuordnung ungeklärt**: das sind keine Karten-Icons; F-104 nennt nur die Gebäude, die auf der Karte erscheinen und produzieren. Bleibt bis zur Klärung auf der Liste |
| ~~B3~~ | ~~Kartenabzeichen~~ | — | — | **entfällt** (F-100) |
| ~~B6~~ | ~~18 Warensymbole~~ | — | — | **entfällt** (F-104) |
| ~~B7~~ | ~~28 Einheitensymbole~~ | — | — | **entfällt** (F-104) |
| ~~B11~~ | ~~20 Gebäudeköpfe~~ | — | — | **entfällt** (F-104) |

**Damit schrumpft der Dezember-Bedarf von 105 Bildern auf 16** (B1, B2 ×2, B5 ×2, B8 ×6, B9, B10 ×2,
B12 ×3, B13 = 16; B4 ungezählt, weil ungeklärt).

---

## 3. Was das Portraitfoto betrifft (F-102, gebaut)

- `tools/paket_ausschluss.py` führt die Liste `PRIVAT` (beide Portraitdateien).
- `tools/build_exe.py` und `tools/build_public_exe.py` kopieren `assets` **gefiltert** in einen
  Zwischenordner; gemessen: **380 statt 382 Dateien**, beide Portraitdateien fehlen, Wappen und Burgen
  sind da.
- Die Dateien bleiben im Projekt (612.608 und 194.338 Byte).
- **Grenze:** geprüft ist der Filter, nicht die gebaute EXE — das steht als Befund in der Wache.

---

## 4. Was für den Dezember als Regel gilt

1. **4 × Anzeigegröße** bei allen Bildern (F-101); bei 1:1-Bildern (Register 502) bleibt Datei = Anzeige.
2. **Alle Kartenbilder quadratisch anlegen**, auch wenn das Motiv hochkant ist (Motiv mittig, Rest
   durchsichtig) — seit F-99 wird zwar eingepasst, aber quadratisch bleibt die robustere Zusage.
3. **Stilvorlage ist die Meshy-Lieferung** (`assets/wappen/elfen_wappen.png`, Waldelfen) — sie zeigt,
   was gebraucht wird, und ist kein Spielinhalt (F-103).
4. **Waren, Einheiten und Karten-Gebäude behalten ihre Icons** (F-104) — dafür wird nichts neu gezeichnet.


---

## 5. Nachträglich entschieden (nach Claudes Antwort Nr. 19, 13.11.2026)

| Frage | Daniels Antwort (wörtlich) | Folge |
|---|---|---|
| **F-105 = F1** Farbe Haus Flickwerk | „F-78 behalten (Eisblau / Weiß / Messing) — die gemessene Datei ist dunkelblau-grau mit Messing-Akzent, das passt am ehesten“ | Das sechste Kopfband entsteht in **Eisblau/Weiß/Messing**; die Chronik-Fassung (Grau/Schwarz/Gold) ist damit überstimmt, weil sie Hammerhall farbgleich machen würde |
| **F-106 = F2** hochgerechnet = 4×? | „Ja: in der größten Ausgabe erzeugen, danach mit gutem Verfahren hochrechnen — die 4×-Datei zählt, Qualität wird dokumentiert“ | F-101 bleibt in Kraft; **jede** hochgerechnete Datei bekommt einen Vermerk (Ausgangsgröße, Verfahren, Datum) in `docs/BILDPAKET_202612*.md` |

**Damit sind Schattenfaust (Rot/Schwarz/Gold, Wappen `wappen_08` gemessen schwarz-rot) und Sternenwacht
(Weiß/Silber/Nachtblau, `wappen_09` gemessen nachtblau-weiß) durch die Dateien gedeckt** — Messung in
`docs/PRUEFUNG_CLAUDE_19_20261113.md`, Abschnitt 5.

**Offen bleibt nur noch F4** (B4, Einzelansichten der Gebäude, 1142 × 1120): Claude hält sie für den
Dezember nicht für nötig, weil jede Ansicht ohne Motivbild auf das Volkspanorama zurückfällt und alle
sechs Panoramen existieren.
