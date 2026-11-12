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
