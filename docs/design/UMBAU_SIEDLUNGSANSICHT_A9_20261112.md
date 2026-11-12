# A-9: Umbau der Siedlungsansicht — Karte rechts, Spalte links, Schleier im Bild

Stand 12.11.2026, 19:3x. Grundlage: Claudes Antwort auf Auftrag Nr. 8 (abgelegt unter
`docs/eingaenge/CLAUDE_20261112_GEBAEUDEANSICHT_NR8/`, SHA256 `112f752d30d0e18f…`) und Daniels
Entscheidungen F-46, F-47 und F-48 (Register 507).

## 1. Die drei Entscheidungen

| # | Entscheidung | Folge |
|---|---|---|
| F-46 | **Feldgroesse 57 px** | `zelle = min(64, (H − 18) // 10)`; bei H = 589 → 57; Karte **588 x 588**; alle 100 Felder sichtbar, nichts rollt |
| F-47 | **Karte rechts, Spalte links** | Spalte x 0..433, 16 px Abstand, Karte x 449..1037; das Wahrzeichen (Inhalts-x 609) liegt ganz unter der Karte |
| F-48 | **Schleier 80 Prozent `#1a0a09`** je Textblock | Text 8,42 · Gold 7,10 · Erfolg 6,37 · Warnung 4,65 · Rahmen 3,31 gegen den schlimmsten Fall |

## 2. Der Plan in Schritten

**S-1 Feldgroesse und Karte (reine Rechnung).** Neue Funktion `_siedlungs_zelle()` liefert
`min(64, (sichtbare_hoehe − 18) // 10)`, mindestens 20 und hoechstens 64. `_zeichne_siedlungskarte`
nimmt die Zahl als Parameter statt der festen 64. Die Masse in `karten_optik_fein` skalieren sich
selbst mit `zelle / 64` — dort ist nichts zu aendern.

**S-2 Historisches Kartenbild.** `originalkarten_grafik` liefert EIN Bitmap (heute 640 x 640). Bei
`zelle != 64` wird es einmal mit LANCZOS auf `10 * zelle` verkleinert (bei 57: 570 x 570) und im
Cache gehalten. Bei 64 bleibt es **byte-gleich** (kein Resize, kein neuer Pfad).

**S-3 Spalte links.** Neuer Aufbau von `_render_settlement_map`: ein Rahmen mit zwei Kindern —
links die Spalte (Breite 433, **rollend** ueber eine eigene Leinwand), rechts die Karte
(588 x 588). Die Spalte enthaelt von oben nach unten: Titel und Name in EINER Zeile (38 px),
Ortsbestand (57), Bauauswahl (218), Dorfuebersicht (240), Legende mit Erklaerung (42), am Ende
Hinweis, Reichsvergleich und Vorteil (57). Summe **652 px** gegen 589 sichtbar → die Spalte rollt,
die Karte nie.

**S-4 Schleier im Bild.** `hintergrund_optik.ausschnitt` bekommt einen optionalen Parameter
`schleier` (Liste von Rechtecken in Inhaltskoordinaten). Jedes Rechteck wird mit
`#1a0a09` zu 80 Prozent ueber den Ausschnitt gelegt (`Image.composite`), **einmal je Neuschnitt**.
Die Rechtecke sind die gemessenen Blocklagen der Spalte — nach dem Layout aus `winfo_y` und
`winfo_height` gelesen, nicht geschaetzt.

**S-5 Textfarben.** Unveraendert; die Kontraste sind gemessen (siehe Tabelle oben). Die Legende
behaelt ihre Geländefarben; das Textfeld darunter bekommt denselben Schleier.

## 3. Was dabei NICHT angefasst wird

- Die Geodaesie des Panoramas: mittiger 1:1-Ausschnitt, nie skalieren (F-45). Mit dem neuen Aufbau
  ist der Inhalt genau 589 px hoch, der Ausschnitt bleibt `(52, 265)`.
- Die Elfen-Gebaeude in der Einzelansicht (A-8) und ihre Zahlen `abdunkeln_prozent_1zu1` /
  `weichzeichnen_px_1zu1` (beide 0).
- `data/` — A-9 braucht keinen neuen Datenschluessel; die 80 Prozent stehen als Konstante mit
  Docstring, damit sie an EINER Stelle auffindbar sind.
- Die Klickauswertung: der Klick gehoert weiter dem Feld, nicht dem Bild.

## 4. Abnahme (messbar, wird Pruefdatei)

| # | Kriterium | Pruefweg |
|---|---|---|
| 1 | Bei H = 589 ist die Karte 588 x 588 und ganz sichtbar | Messung im Fenster: Kartenkante gegen Inhaltshoehe |
| 2 | Das Kartenbild ist bei 57 px 570 x 570 (einmal verkleinert), bei 64 px unveraendert 640 x 640 | Messung am geladenen Bild |
| 3 | Die Spalte rollt, die Karte nicht | Rollbereich der Spalte = 652, Karte steht |
| 4 | Jeder Textblock liegt auf einem Schleierfeld von 80 Prozent, zwischen den Feldern ist das Bild sichtbar | Messung der Rechtecke + Sicht |
| 5 | Jedes sichtbare Bildpixel ausserhalb der Schleierfelder entspricht dem Quellpixel am Ausschnitt (52, 265) | Stichpixel, wie in `test_gebaeudeansicht_a7` |
| 6 | Klick auf ein Feld trifft das Feld (nicht das Bild) | Klickpruefung im Fenster |
| 7 | Das Wahrzeichen liegt unter der Karte (nicht zerschnitten) | Rechnung: 609 < 449? nein — 609 liegt IM Kartenbereich 449..1037, also verdeckt |

## 5. Offen

- Ob die Bauauswahl in 433 px Breite unveraendert passt (heute 300 px) — messen, nicht schaetzen.
- Ob die Dorfuebersicht bei 433 px ihre acht Spalten behaelt (`_lager_spalten`-Muster).
- Daniels Auge auf die leicht weichere Karte bei 57 px (bewusst angenommener Preis, F-46).
