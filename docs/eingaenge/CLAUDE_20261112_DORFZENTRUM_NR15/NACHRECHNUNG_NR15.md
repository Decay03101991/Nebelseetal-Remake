# Nachrechnung der Antwort Nr. 15 (Claude Opus 5.5)

**Nachgerechnet:** 12.11.2026, Sitzung 40, Weltenfresser (`deepseek-v4-flash`).
**Antwort:** `ANTWORT_NR15_DORFZENTRUM_PRUEFSTAND.md`, SHA256 `c8d2a921…`, 26.049 Byte.
**Regel:** erst nachrechnen, dann bauen (Arbeitsvereinbarung mit Claude, Register 531/544).

---

## 1. Was stimmt (jede Zahl einzeln nachgerechnet)

### Teil A — Formeln und Maße

| Prüfpunkt | Ergebnis |
|---|---|
| Neue Formel `f = min(64, (H−18)//10, (W−rb−S_min−18)//10)`, `R = 10f+18`, `S = W−rb−R` | **(1037, 589, rb 17): 395/57/588/432** und **(1127, 764, rb 21): 395/64/658/448** — beide Fälle exakt |
| G3-Spalten bei R = 658 | Name 658−20−30−(125+150+105) = **228** ✓ · bei R = 588: 588−16−24−304 = **244** ✓ |
| G3-Höhe | 30 + 17 × 32 = **574 ≤ 702** ✓ |
| G4-Spaltenblöcke | 74 + 57 + 55 + 100 + 58 + 4 × 10 = **384** ✓ → Block 5 hat **380 px** |
| G4-Aktionszeile | 94 + 75 + 110 + 2 × 10 = **299 ≤ 428** ✓ |
| G4-Eingabefeld | round(150 × 1,2512) = **188** ✓ |
| Tabelle „Restliche Werte" | 59/74, 34/42, 539/702, C1 185/99/72/472 und 206/118/83/548, C2 26/388 und 32/478, C3 466/574 — **alle zwölf Werte stimmen** |
| G6 Erwartung 8 / 4 / 5 Rezepte je Werkstatt | **17 Rezepte** ✓ (eigene Messung: Schmiede 8, Bogenbauer 4, Nähstube 5) |
| Einheiten-Namensspalte | 314 − 120 − 20 = **174** ✓ · bei k = 1: 282 − 96 − 16 = **170** ✓ |
| „9.999" in 19 px fett | gemessen **45 px**, passt in 60 ✓ |

### Teil B — Rechnungen

| Prüfpunkt | Ergebnis |
|---|---|
| Die vier langen Dateien | 134 + 72 + 31 + 23 = **260 s** ✓ |
| T3-Schätzung | (1380 − 260) / 1,39 = **806 s** ✓ (seine 800 sind gerundet) |
| Beschleunigungsfaktor 1,39 | aus 1380 / 990 ✓ — **aber [a]**: unter Last gemessen, nicht belastbar (siehe Sammellauf 22:18, der unter Nebenlast deutlich langsamer läuft) |

### Teil C — Rechnungen

| Prüfpunkt | Ergebnis |
|---|---|
| „41,7 Spieltage = 5,6 Echtstunden" | 41,7 × 8 min = 333,6 min = **5,56 h** ✓ |

---

## 2. Was NICHT stimmt

### 2a. Die Kleintext-Regeln gehen von der falschen Schriftgröße aus

**Der Befund:** Tk rechnet eine **Pixel**-Schriftgroesse intern in **ganze Punkte** um und wieder
zurück. Im DPI-bewussten Prozess ist `tk scaling` = **1,6683**; `-16` px wird zu **10 pt** = 16,68 px
und damit wie **17 px** gerendert. Gemessen (bewusster Prozess, echte Tk-Schrift):

| Angefragt | Tk rendert | „Paladinharnisch" | „Großer Belagerungsturm" |
|---|---|---|---|
| `-15` px | 15 px | **104** | 162 |
| `-16` px | 17 px | **117** | 180 |
| `-19` px (= `schrift(15)`) | 18 px | **128** | 198 |
| `-25` px (= `schrift(20)`) | 25 px | 181 | 278 |

**Was daraus folgt:** Seine Regel „Kleintext 15 px, Paladinharnisch dann etwa 110 px" stimmt nur, wenn
die 15 px **absolut** gesetzt werden (gemessen 104 ✓). Geht der Kleintext durch `schrift(15)`, sind es
**19 px und 128 px** — und die Lager-Textbreite ist 118, also **10 px zu breit**. Für die Einheiten
dasselbe: absolut 15 px = **162 ≤ 174 ✓**, über `schrift(15)` = **198 > 174 ✗**.
**Entscheidung noetig:** Ist „Kleintext" eine feste Pixelgroesse (dann skaliert sie nicht mit dem
Bildschirm) oder eine mitwachsende Stufe (dann braucht sie eine andere Textbreite)?

### 2b. Zwei Farbangaben zu unseren Völkern sind falsch

Er schreibt, unsere Farben seien „Trolle weiß-gold" und „Ghule violett". **Belegt** in
`FRAKTIONEN_WELTEN.md`: Schattenfaust (Trolle) = **Dunkelrot und Schwarz**, Knochenmoor (Ghule) =
**Grün und Knochenweiß**. Nur Silberbach (Menschen, Blau und Silber) nennt er richtig. Der Widerspruch,
den er in Teil C (a) 1 beschreibt, besteht also für **eine** von drei Stellen — die anderen zwei sind
erfunden. Sein Vorschlag („Daniels Burgbilder geben die Farbe vor") bleibt richtig, die Begründung muss
berichtigt werden.

### 2c. Die Herkunft der falschen Zahlen stimmt — und ist mein Fehler

Er hat recht: „vier Zutaten" (Auftrag 12), „18 Arten" (Auftrag 13/14) und „2148 px Dorfzentrum"
(Auftrag 13) standen **in meinen Aufträgen**. Damit ist M11 (Faktenblatt aus `data/`) die beste
Einzelmaßnahme des ganzen Pakets, denn sie schließt genau diese Fehlerquelle.

---

## 3. Was das Bauen kostet (Schätzung, damit Daniel entscheiden kann)

| Teil | Umfang | Dauer |
|---|---|---|
| G1/G2 (Abstand = gemessener Rollbalken) | `siedlungs_masse` + 2 Wachen (`siedlungsansicht_a9`, `dpi_f51`) + Siedlungsansicht | ~1 h |
| G3 (Werkstätten schlanker) | Teil des Dorfzentrum-Baus | mit dem Dorfzentrum |
| G4 (Spalte in 7 Blöcken) | Teil des Dorfzentrum-Baus | mit dem Dorfzentrum |
| G5 (Kennzahl-Funktion) | `spieloekonomie` + Wache | ~30 min |
| G6 (Feld `werkstatt`) | `data/`-Änderung + Abgleich gegen den Fließtext + Wache | ~45 min |
| Teil B M1–M12 | 12 Maßnahmen, jede mit eigener Wache | **mehrere Sitzungen** — Vorschlag: M11 zuerst, dann M1, M2, M12, dann der Rest |

**Reihenfolge-Vorschlag:** M11 → M1 → M2 → M12 (billig, sofort Nutzen), dann Dorfzentrum bauen, M4/M5
beim Berühren der Dateien, M8 erst wenn Daniel Korridore freigibt.
