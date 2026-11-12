# Prüfung: Claudes Antwort auf Auftrag Nr. 5 (Ressourcenleiste T08)

**Gegenstand:** `Claude_Opus_5.5_Antwort_Auftrag5_Ressourcenleiste.md`, Daniels Abo-Lauf im Browser.
**Geprüft:** 12.11.2026, 12:1x, von Hermes (Weltenfresser). **Verfahren:** eigene Rechnung, kein Modell.
**Formeln:** WCAG 2.x (relative Leuchtdichte, sRGB-Linearisierung bei 0,04045) — dieselben, die er nennt.

## 1. Ergebnis in einer Zeile

**9 von 9 Kontrastwerten stimmen** (Abweichung über 0,05: **0**), die **Leuchtdichte-Werte exakt**
(#3e1c1a = 0,0193; Grenze für 4,5 : 1 = 0,0221), und die **gesamte Raster-Arithmetik exakt**.

## 2. Kontraste (alle nachgerechnet)

| Element | Antwort | gerechnet |
|---|---|---|
| Zahl/Rate #F2E3BF auf Leiste #1a0a09 | 15,13 | **15,13** |
| Zahl/Rate auf Fläche #3e1c1a (Zustand »kritisch«) | 11,92 | **11,92** |
| Name #b8862e auf Leiste | 5,94 | **5,94** |
| Name #b8862e auf Fläche | 4,68 | **4,68** (genau 4,681) |
| Warnung #ff8a70 auf Leiste | 8,36 | **8,36** |
| Warnung #ff8a70 auf Fläche | 6,58 | **6,58** |
| Erfolg #a5d67a auf Leiste | 11,45 | **11,45** |
| Erfolg #a5d67a auf Fläche | 9,02 | **9,02** |
| Gold #FFCC33 auf Leiste (nur Endstücke) | 12,77 | **12,77** |

Seine Herleitung der Grenze ist ebenfalls richtig: bei der Namensfarbe #b8862e (Leuchtdichte
0,2743) liegt die 4,5-zu-1-Schwelle bei Grund-Leuchtdichte **0,0221** — deshalb darf kein Pixel
der Mittelkachel heller als #3e1c1a (0,0193) sein.

## 3. Raster (Arithmetik exakt)

Formel W = abgerundet aus (B − 32 − (n−1)) / n mit n = 11:

| Leiste | Zellbreite | Rest | links/rechts |
|---|---|---|---|
| 1446 px (Fenster 1460) | **127 px** | 7 | 3 / 4 |
| 1186 px (Fenster 1200) | **104 px** | 0 | 0 / 0 |
| 986 px (Fenster 1000) | **85 px** | 9 | 4 / 5 |

Weitere Rechnungen, alle bestätigt:
- Deckel bei 132 px Zellbreite: 11 × 132 + 10 + 32 = **1494 px** Leiste.
- Erstes Feld fällt unter 62 px Zellbreite: 11 × 62 + 10 + 32 = **724 px** Leiste = **738 px Fenster**
  (die Leiste ist Fensterbreite minus 14, selbst gemessen).
- Schwelle 100 px: 41,1 (Nahrung) + 6 + 39,2 (+1.234/h) + 12 = **98,3 px**.
- Schwelle 62 px: 50,0 (999,9M) + 12 = **62,0 px**.
- Nebeneinander statt untereinander bräuchte 41,1 + 50,0 + 12 = **103,1 px**.

**Damit ist der gemessene Überlauf gelöst:** die Zellen passen sich an, statt rechts
abgeschnitten zu werden. Bei 986 px bleiben alle elf Felder sichtbar.

## 4. Zahlenkürzung (C2) — Regel geprüft, nicht nur gelesen

| Bereich | Anzeige | Zeichen | Probe |
|---|---|---|---|
| 0 bis 99.999 | ganz mit Tausenderpunkt | höchstens 6 (»99.999«) | ✓ |
| 100.000 bis 999.999 | »100k« bis »999k« | 4 | ✓ |
| ab 1 Million | »1,00M« … »9,99M«, dann »10,0M«, dann »100M« | 4 bis 5 | ✓ |

Das Kürzen ist **abgerundet** (999.999 → »999k«), also wird nie mehr angezeigt als vorhanden —
dieselbe Regel, die unser Haus für Anzeigen hat.

## 5. Was er als UNBEKANNT markiert — und was ich davon beantworten kann

| Seine offene Frage | Stand |
|---|---|
| Wie rechnet Tkinter Punkt in Pixel bei 125 %? (er misst in Pixel, Tk kennt Punkte) | **messbar** — ich messe es im laufenden Fenster nach (Arial 10 fett: »Nahrung« soll 41 px breit sein) |
| Liefert das Spiel eine Rate je Stunde? | **ja** — die Leiste hat sie schon gezeigt (»+250/h« im Lage-Band); ob sie in der Leiste selbst steht, ist offen |
| Unterscheidet das Spiel Änderungen außerhalb des Takts? | offen, im Code prüfbar |
| Obergrenzen der Ressourcen | im Originalhandbuch nachzusehen |

## 6. Was mir an seiner Antwort fehlt (ehrlich)

1. **Der Zustand »steigt/fällt« ist ohne Mechanik nicht baubar.** Er sagt selbst: ob das Spiel
   Änderungen außerhalb des Takts unterscheidet, weiß er nicht. Solange das offen ist, bleiben
   drei Zustände (normal, kritisch, Unterdeckung) — der vierte ist ein Vorschlag ohne Grundlage.
2. **»▼« als Schriftzeichen** muss in Tkinter geprüft werden, nicht in Liberation Sans. Er sagt das
   selbst; ich prüfe es beim Bau.
3. **Die Farbe des Namens (#b8862e) ist das Rahmengold des Handbuchs**, nicht unser Skin-Gold
   (#FFCC33). Das ist zulässig (seine Palette), heißt aber: die Leiste sieht anders aus als die
   übrige Oberfläche, solange der Skin nicht mitzieht. Das ist eine Entscheidung für Daniel.

## 7. Empfehlung für den Bau

Bauen, aber in dieser Reihenfolge:
1. Raster mit den drei Breiten und der Weich-Regel (das löst den gemessenen Fehler),
2. Zahlenkürzung und rechtsbündige Ziffern,
3. Zustände normal/kritisch/Unterdeckung,
4. Band als 9-Slice mit Rückfall ohne Bild,
5. »steigt/fällt« erst, wenn Daniel entscheidet, ob es Änderungen außerhalb des Takts gibt.

Der Bildteil (D1) kann warten — die Leiste funktioniert ohne Bilddatei vollständig.

## 8. Was gebaut wurde (T08, 12.11.2026)

Gebaut nach der Reihenfolge aus Abschnitt 7. Alle Rechenwege liegen OHNE Tk in `src/main.py`,
damit sie pruefbar sind; gezeichnet wird nur in `NebelseetalApp._leiste_zeichnen`.

| Teil | Umsetzung | Rechenstelle |
|---|---|---|
| 1 Raster | Zellbreite W = abgerundet aus (B - 32 - (n-1)) / n, Deckel 132 px; Restpixel links/rechts | `leiste_raster` |
| 2 Weich-Regel | unter 100 px faellt die Rate weg, unter 62 px weichen Punkte, Pferde, Siedler; Zelle „+n“ (28 px) | `leiste_auswahl` |
| 3 Zahlen | hoechstens sechs Zeichen, abgerundet: 99.999 / 100k / 1,23M / 10,0M / 100M | `leisten_kurz`, `leisten_zahl`, `leistenwert` |
| 4 Rate | Ertrag je Stunde, Nahrung netto (dieselbe Verbrauchsstelle wie die Detailzeile) | `leisten_rate` |
| 5 Zustaende | `kritisch` (Bestand 0, nur Vorraete): Flaeche #3e1c1a, Unterstrich 2 px, Zahl in Warnung; `unterdeckung` (Rate negativ): Pfeil links vor der Zahl | `leisten_zustand` |
| 6 Band | 9-Slice: Endstuecke 16 px, Mittelkachel 64 px nur wiederholt, nie gedehnt; ohne Bild glatte Flaeche | `leiste_band_teile` |
| 7 Zeichnen | 34 px hoch, Name 10 px fett, Zahl 15 px fett rechtsbuendig, Rate 10 px | `_leiste_zeichnen`, `_leiste_aktualisieren` |

**Gemessen im laufenden Fenster** (1460 / 1200 / 1000 px Fenster): Leiste **34 px** hoch, Zellbreite
**127 / 104 / 85 px**, rechte Kante der letzten Zelle **immer vor B - 16**, kein Text ueber dem Rand,
elf Felder sichtbar. Bei 700 px Fenster weicht **Punkte** und die Zelle „+1“ steht rechts.

**Was NICHT gebaut wurde - und warum:**
1. **Der Zustand „steigt/faellt“.** Ob das Spiel Aenderungen ausserhalb des Takts unterscheidet, ist
   offen (Abschnitt 5). Ein Zustand ohne Grundlage waere geraten.
2. **Der Tooltip der Zelle „+n“.** Sie nennt die Zahl der ausgeblendeten Felder, nicht ihre Namen -
   das waere ein eigenes kleines Fenster. Unter 738 px Fensterbreite, also im Betrieb selten.
3. **Die Namensfarbe ist offen.** Gebaut ist #b8862e aus dem Handbuch (Kontrast 5,94). Unser
   Skin-Gold #FFCC33 haette 12,77 - die Wahl steht in `farben.name` der Datendatei, ohne Code.

**Ehrlich dazu:** beim Spielstart stehen sieben von elf Feldern auf „kritisch“, weil alle Rohstoffe
0 sind. Das ist die Regel „Bestand 0“ woertlich genommen und sieht nach Alarm aus; ob kritisch erst
ab einer Schwelle gelten soll, ist eine Entscheidung fuer Daniel, keine Rechnung.
