# PRUEFUNG: Claudes Designpaket-Handbuch (Opus 5.5) - 12.11.2026

Regel dieser Projektlinie: **Ein Modellurteil ist eine Behauptung, bis es nachgerechnet ist.**
Geprueft gegen `main` = `f6bb9e6`. Jede Zeile hier ist eine eigene Messung, kein Zitat.

## 1. Die Zahlen: 86 von 86 Kontrastwerten stimmen

Eigene WCAG-Rechnung (relative Leuchtdichte nach 2.x, `(L1+0,05)/(L2+0,05)`), alle 15
Paarungen mal sieben Paletten (Standard + sechs Haeuser) = **86 Werte**.
**Abweichung ueber 0,05: 0.** Auch die drei Kniffligen stimmen: Silberbach Akzent/Flaeche
**5,16** (der schwaechste Schriftwert im ganzen Paket, wie er sagt), Standard Rahmen/Grund
**5,76**, Knochenmoor Rahmen/Grund **10,42** (Silberrahmen statt Gold).

## 2. Die drei Vorab-Befunde: alle drei bestaetigt

| Befund | Behauptung | Eigene Messung | Urteil |
|---|---|---|---|
| V-1 Unschaerfe im Code | `gebaeude_optik.py` Z. 105-125: Band **538 x 222** wird auf **1142 x 1120** gebracht, LANCZOS + Spiegelung + Weichzeichner | Wortlaut im Code: "Bei einer 538x222-Band auf 1142x1120 waren das gemessen 86 Prozent Flaeche ohne jedes Bild"; `Image.LANCZOS` fuer die Szene, zweite Lage gespiegelt | **bestaetigt** |
| V-2 keine DPI-Angabe | kein `SetProcessDpiAwareness`, kein `tk scaling`, kein Manifest | `grep -rniE` ueber `src/` und `tools/`: **keine Treffer**; fuenf `.bat`-Dateien, keine DPI-Angabe darin | **bestaetigt** |
| V-3 mehr als neun Menuepunkte | `MENU_ITEMS` 16 Eintraege, Z. 3695; "Lager" entfaellt | `MENU_ITEMS` steht auf **Z. 3695** und hat **16** Eintraege; `MENUE_ENTFALLEN = {"Lager"}` auf **Z. 3749** | **bestaetigt** |

## 3. Die Belege aus dem Repo: geprueft, alle vorhanden

| Behauptung | Eigene Messung |
|---|---|
| `assets/icons/leiste/ressourcenleiste.png` ist 1440 x 140 | **1440 x 140** (Pillow) |
| acht Zahlenfelder im gemalten Band | Wortlaut `main.py` Z. 9362: "gemaltes Bild mit **acht** Zahlenfeldern" |
| 20 Gebaeude-Hintergruende | **20** Dateien in `assets/icons/gebaeude/hintergrund/` |
| 28 Einheiten | `data/units.json` -> `einheiten`: **28** |
| sieben Gelaendearten | `data/gelaende.json` -> `gelaendearten`: **7** |
| sechs Welten, Startwelt Midgard | `welten_belegt`: 6 Namen; `startwelt`: **Midgard** |
| vier Ruhm-Stufen, vier Auszeichnungen | `data/ruhm.json` -> `stufen`: 4; `README.md` Z. 27 nennt Feldherr, Forscher, Haendler, Gesamtherrscher |
| Fensterdeckel 1560 px | `min(1560, ...)` steht im Code |
| 18 Gegenstands-Bilder | **18** Dateien in `assets/icons/items/` |
| Forum offline | `main.py` Z. 15831: "Forum ist offline." |
| Sperrgrund steht schon im Menue | `bauanzeige_pruefung` Z. 2776-2801, Docstring nennt genau den Fall "gruen angezeigt, Wirkung null" |
| Farben bei Chris gemessen | `DESIGN_LIEFERUNG_CHRIS` Z. **107-109**: #C68B42, #7E301E, #7AAC4D - alle drei so |
| Chris' Stilregeln Z. 137-149 | Z. **137-149** tragen Malstil, Gebaeudekachel, Symbolsystem, "kaum Menschen" - so zitiert |
| zwei Rahmenstile im Fenster | Z. **176-177** sagt das woertlich |
| "ab 09.11.2026 sind Chris' Bilder der Massstab" | `DESIGN_ARBEITSWEISE` Z. **58-59**, F-39 |
| Burgbilder und 125 Siedlungskarten bleiben | `DESIGN_ARBEITSWEISE` Z. **54-55** |

## 4. KEINE Abweichung - und hier lag ICH falsch

**Berichtigung vom 12.11.2026, 03:0x, noch vor Daniels Entscheidung.**
Ich hatte geschrieben, Claudes Hausblock Schattenfaust nenne den Sitz "Felsen**feste**
Schattenfaust", waehrend `data/haeuser.json` "Fels**feste** Schattenfaust" sagt. **Das war falsch.**
Die abgelegte Fassung des Handbuchs enthaelt "Felsen..." **null** mal und "Felsfeste" **einmal**
(`grep -c` in `docs/eingaenge/CLAUDE_20261112_DESIGNPAKET/`, SHA256 `cf143076ed59625d…`).
Ich hatte aus der Darstellung im Chat gelesen, statt die Datei zu pruefen - genau der Fehler, den
diese Projektlinie anderen Modellen vorhaelt.

**Folge:** alle sechs Sitze stimmen woertlich mit `data/haeuser.json` ueberein. Es gibt nichts zu
berichtigen, und die von Daniel erteilte Korrektur entfaellt.

## 5. Was ich NICHT pruefen kann (und was er selbst offenlegt)

- **Ob die Bildgeneratoren Boegen (2x2, 3x3, 4x3, 5x2) gleich gross liefern.** Er sagt selbst:
  haengt vom Modell ab, die Abnahme A-SYM faengt es. Zustimmung: das ist der richtige Weg.
- **Die echten Flaechenmasse von Portal, Angriffsflaeche, Marktplatz, Ruhmeshalle und Forschung
  im laufenden Fenster.** Er setzt 1280 x 720 bzw. 1600 x 900 an und schreibt dazu "vor der
  Erzeugung einmal im Spiel messen". Das ist ehrlich - und es ist unsere Arbeit, nicht seine.
- **T04 mit 1152 x 1120** ist 10 px breiter als die Flaeche im Code (1142). **ENTSCHIEDEN am
  12.11.2026 (Register 469): 1142 x 1120, 1:1.** Der Vergleich (Register 468) zeigt, dass die
  10 px nichts entscheiden (Schaerfe 5,4 bis 5,6 in allen drei Wegen); das Vielfache von 8 wirkt
  in Tkinter nicht. Wer ein Gebaeudebild baut, nimmt **1142 x 1120**.
- Seine vier nicht belegten Punkte (Skins "wald"/"feuer" Nutzung, Einheiten je Haus anders,
  Chat/"Spieler werben" offline, 17 Waren) sind als "weiss ich nicht" markiert. Richtig so.

## 6. Urteil

**Das Handbuch ist brauchbar und in den Zahlen sauber.** 86 von 86 Kontrastwerten, alle
zwoelf nachpruefbaren Repo-Belege, alle drei Vorab-Befunde bestaetigt, **keine falsche Angabe
gefunden** (der eine behauptete Fehler war meiner, siehe Abschnitt 4).
Die drei Entscheidungen, die er selbst getroffen hat, sind begruendet und vertretbar:
Rahmen immer als 9-Slice vom Spiel (R-4), KopfbAender der Hausansichten als Ausschnitt (1.4),
Standardteile einmal statt je Skin (1.2).

**Was vor dem ersten Bild entschieden werden muss** (Daniel, nicht ich):
1. **Bildpaket-Reihenfolge:** seine ersten zwoelf Bilder (Knoepfe, Ressourcenleiste, Menue-Icons,
   Tor, Dorfzentrum Silberbach, Portal, Kaserne, Marker, Kartenrahmen, Statusleisten) - das ist
   genau der Bereich, den er in V_0.0.4 als "haesslich" bezeichnet hat. Zustimmung von hier.
2. **Ein Haus zuerst** (er schlaegt Silberbach vor, weil Midgard Startwelt ist - belegt).
3. **1152 oder 1142** fuer die Gebaeudeflaeche (Punkt 5).
4. **Der Sitzname** wird berichtigt (Punkt 4) - das mache ich, sobald du es sagst.
