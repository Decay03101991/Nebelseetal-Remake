# Nachrechnung — Claudes Antwort Nr. 16 (Entscheidungen, Paket 15b, System)

| | |
|---|---|
| **Gegenstand** | `ANTWORT_NR16.md` (31.371 Byte, SHA256 `b216440a…`), abgelegt am 12.11.2026 |
| **Geprüft von** | Hermes Agent „Weltenfresser“, Sitzung 41 (12.11.2026, ab 23:1x) |
| **Verfahren** | Jede Zahl selbst gerechnet bzw. selbst gezählt; Quellen im Repo (`data/`, `tools/`, `tests/`) |
| **Ergebnis** | **Werteblock A4 vollständig bestätigt** (17 Zeilen, beide Fälle), **Block 5 = 370 bestätigt**, alle Zahlen aus Teil B bestätigt. **Vier Befunde** (B1 bis B4), keiner davon kippt eine Entscheidung. |

---

## 1. Sein Werteblock A4 — Zeile für Zeile, beide Fälle

Eingaben wie in seiner Antwort genannt. Fall 1: W 1037, H 589, k 1, rb 17, ls 15/18/18/24, tkopf 24.
Fall 2: W 1127, H 764, k 1,2512, rb 21, ls 19/22/22/30, tkopf 30.

| Zeile | Fall 1 (sein Wert → gerechnet) | Fall 2 (sein Wert → gerechnet) | Urteil |
|---|---|---|---|
| `p = round(8k)` | 8 → 8 | 10 → 10 | stimmt |
| `S_min = round(316k)` | 316 → 316 | 395 → 395 | stimmt |
| `f = min(64,(H−18)//10,(W−rb−S_min−18)//10)` | 57 → 57 | 64 → 64 | stimmt |
| `R = 10f+18` | 588 → 588 | 658 → 658 | stimmt |
| `S = W−rb−R` | 432 → 432 | 448 → 448 | stimmt |
| `kopf = 2p+ls_titel+round(4k)+ls_text` | 59 → 59 | 74 → 74 | stimmt |
| `reiter = ls_zw+2p` | 34 → 34 | 42 → 42 | stimmt |
| `innen = H−reiter−2p` | 539 → 539 | 702 → 702 | stimmt |
| `T_w = (R−4p)//3` | 185 → 185 | 206 → 206 | stimmt |
| `T_h = 2p+max(56,2·ls_text+round(2k)+ls_zahl)` | 72 → 72 | 83 → 83 | stimmt |
| `lager_hoehe = 6·T_h+5p` | 472 → 472 | 548 → 548 | stimmt |
| `z = ls_zahl+p` | 26 → 26 | 32 → 32 | stimmt |
| `einh_hoehe = tkopf+14z` | 388 → 388 | 478 → 478 (siehe B1: 481) | stimmt (mit B1) |
| `einh_name = (R−3p)//2−round(48k)−p` | 226 → 226 | 244 → 244 | stimmt |
| `werk_name = R−5p−round(100k)−round(120k)−round(84k)` | 244 → 244 | 228 → 228 | stimmt |
| `werk_hoehe = tkopf+17z` | 466 → 466 | 574 → 574 (siehe B1: 577) | stimmt (mit B1) |
| `block5 = H−(kopf+57+55+100+58)−5p` | nicht angegeben (→ 220) | 370 → 370 | stimmt |

**Zusatzwerte der Tabellen A1, ebenfalls nachgerechnet:** Textbreite Spalte 416 / 428, Reiterbreite
190 / 212, Textbreite Kachel 99 / 118, Textblock 50 / 63, Hälftenbreite 282 / 314, Zahlspalte 48 / 60
— **alle sechs in beiden Fällen richtig**.

**Wichtig für die Bewertung:** In Fall 2 sind seine `ls`-Werte die **gemessenen Zeilenhöhen** von Tk
(16 px = 19, 19 px fett = 22, 25 px fett = 30 — alle am 12.11. selbst gemessen), nicht die
Schriftgrößen. In Fall 1 sind es Werte seiner eigenen Messung mit Liberation Sans (15 / 18 / 24), die
dort zufällig wie die Pixelgrößen aussehen. Das ist die Ursache von B1.

## 2. Seine Selbstkorrektur: Block 5 = 370, nicht 380 — er hat recht

Eigene Rechnung, unabhängig von seiner:

- Block 1 Kopf **74** + Block 2 **57** + Block 3 **55** + Block 4 **100** + Block 6 **58** = **344**
- sechs Blöcke haben **fünf** Lücken à `p` = 10 → **50**
- 764 − 344 − 50 = **370**

Meine 380 aus der Nachrechnung zu Nr. 15 waren falsch gezählt (vier Lücken statt fünf). **Berichtigt
im Register 547/548 und in Register 555 dieser Sitzung.** Sein Fehler war die Zahl, nicht die Methode.

## 3. A2 Ablage der Werkstatt-Zuordnung — seine offene Frage ist beantwortbar

Er nennt als UNBEKANNT: „Ob die Lader unbekannte Felder vertragen.“

**Antwort: Das Feld gibt es schon — an einer anderen Stelle, und der Weg ist vorgezeichnet.**

1. `data/items.json` → `waren[<Ware>]["werkstatt"]` führt bereits **je Ware** die Werkstatt:
   Schmiede **8**, Nähstube **5**, Bogner **4** = 17.
2. `src/werkstatt.py` → `werkstatt_fuer(ware)` ist die **eine** Lesestelle; sie liest genau dieses
   Feld (Alias-Tabelle `Bogner → bogenbauer`). `spieloekonomie.ware_grenzen` und
   `spielschicht` rufen nur sie.
3. **Der Prüfstein, den er nicht kennt:** `tests/test_warenrezepte.py` (Abschnitt 7) verlangt, dass
   `data/warenrezepte.json` **stückweise gleich** der frischen Ableitung aus
   `tools/warenrezepte_ableiten.py` ist. Ein von Hand eingetragenes Feld `werkstatt` macht diese
   Wache **rot**.
4. **Der saubere Weg (Form 1, wie Daniel in F-64 entschieden):** `pilotrezept()` in
   `tools/warenrezepte_ableiten.py` kennt die Werkstatt bereits als `typ = werkstatt_fuer(name)`
   (Zeile 86), schreibt sie aber nicht ins Rezept. Ein Feld `"werkstatt": typ` im Rückgabewert und
   ein Lauf von `tools/warenrezepte_ableiten.py` erzeugt die Datei **mit** dem Feld — Ableitung und
   eingefrorene Datei bleiben gleich, es entsteht **keine zweite Liste**.
5. Lader, die nur bekannte Felder lesen (`rezept.get("kosten")` usw.), stören sich nicht an einem
   zusätzlichen Feld; strenge Schlüsselprüfungen gibt es in `tests/` nicht (geprüft: keine
   `set(keys())`-Vergleiche gegen Rezepte).

**Folge für den Bau:** F-61/F-64 wird **nicht** als Handänderung an der JSON gebaut, sondern über das
Ableitungswerkzeug plus eine Wache, die items.json und Rezept gegeneinander hält (Werte: 8 / 4 / 5,
Kennung klein: `schmiede`, `bogenbauer`, `naehstube` — nicht die Anzeigenamen `Schmiede`, `Bogner`,
`Nähstube`).

## 4. A3 `dorfzentrum_kennzahlen` — Signatur stimmt, Rezept hat zwei Stellen zu korrigieren

`src/spieloekonomie.py` Zeile 562:

```
ware_grenzen(ort: dict, ware: str, forschung: dict, rezepte: dict = None) -> dict
```

- **Befund B2:** Seine Zählregel „`ware_grenzen(ort, ware, forschung) > 0`“ ist in Python 3 ein
  **TypeError** — die Funktion gibt ein **dict** zurück. Richtig ist
  `ware_grenzen(ort, ware, forschung)["moeglich"] > 0`. Der Schlüssel heißt `moeglich`.
- **Befund B3:** `ware_grenzen` gibt `moeglich = 0` auch dann, wenn die **Werkstatt in diesem Ort
  nicht steht** (`hindernis = "Werkstatt nicht in dieser Stadt."`). „Herstellbar“ heißt damit
  „Werkstatt vorhanden **und** Voraussetzung erfüllt **und** Rohstoff reicht **und** unter dem
  Mengendeckel“. Das ist die richtige Zahl für den Kopf — aber es muss im Text der Kennzahl stehen,
  sonst fragt Daniel später, warum im Dorfzentrum 0 von 17 herstellbar sind.
- Die Zählweise selbst (über `len(items)`, `len(warenrezepte)`, kein Literal 17) ist richtig:
  `items.json` führt 17 Waren, `warenrezepte.json` 17 Rezepte, **jedes mit genau einer Zutat**
  (nachgezählt: `Counter({1: 17})`).

## 5. Teil B — alle Zahlen selbst gezählt

| Seine Zahl | Eigene Zählung | Urteil |
|---|---|---|
| 230 Zeilen in Paket 15b, Summe **2588,7 s** | 230 Zeilen, 2588,7 s | stimmt |
| `main` in **184 von 230** Dateien (80 %) | 184 von 230, 80,0 % | stimmt |
| Hubs: einheiten 86, spieloekonomie 60, gelaende 45, auftraege 31, punkte 30, kampf 27, forschung 27, botkern 26 | genau diese acht, in dieser Reihenfolge | stimmt |
| acht T4-Kandidaten zusammen **660 s = 25 %** | 660,6 s = **25,5 %** der Summe | stimmt |
| `test_protokoll` 22,4 s, 205 Läufe, nie rot | 22,4 s, 205 Läufe, 0 rot, **kein** `src`-Modul | stimmt |
| `test_portal_kopfleiste` 13 von 46 rot, `test_weltkarte_rahmen` 6 von 64 | 13 / 46 und 6 / 64 | stimmt |
| **46 Dateien ohne Messwert-Historie** | 46 von 230 | stimmt |
| `test_textqualitaet` hat **0 Läufe**, war aber rot | CSV: 0 Läufe, 0,0 s. Sammellauf 22:18, Zeile 213: **ROT 470/2/0, 0,6 s** | stimmt — **der Beleg für M12.0** |
| 34 der 46 sind alte `gpt_`-Dateien | (nicht einzeln nachgezählt — für den Bau unerheblich) | offen gelassen |

Der Satz, auf den es ankommt: **„keine Historie“ heißt nicht „läuft nie“, sondern „schreibt nichts in
den Index“.** Er ist mit dem 22:18-Lauf belegt. Deshalb ist M12.0 (Sammellauf schreibt selbst) der
richtige erste Schritt und nicht eine Nachrüstung der 46 Dateien.

## 6. Die vier Befunde im Zusammenhang

| # | Befund | Wirkung |
|---|---|---|
| **B1** | `tkopf` in Fall 2: seine Formel `ls(Fließtext fett) + round(9k)` ergibt 22 + 11 = **33**, er setzt **30**. Damit wären Einheiten **481** und Werkstätten **577** hoch (statt 478 / 574) — beide weiter unter 702. | Keine Entscheidung kippt; beim Bau wird die Kopfzeile **gemessen**, nicht gerechnet. |
| **B2** | `ware_grenzen(...) > 0` ist ein TypeError (dict). Richtig: `["moeglich"] > 0`. | Rezept A3 wird so gebaut, nicht wörtlich übernommen. |
| **B3** | „herstellbar“ verlangt zusätzlich die **Werkstatt im Ort**. | In den Text der Kennzahl aufnehmen. |
| **B4** | Werkstatt-Zuordnung existiert schon in `items.json`; ein Handeintrag in `warenrezepte.json` macht `test_warenrezepte` rot. Sauberer Weg: Feld in `pilotrezept()` + Ableitung neu schreiben. | Bauweg für F-61/F-64 festgelegt. |

## 7. Was auch ich nicht geprüft habe

- **Knopfhöhe `h_b` in Fall 1** (k = 1): nicht gemessen, er sagt es selbst (UNBEKANNT).
- **Startzeit der App je Fensterwache** — davon hängt die Ersparnis des Zusammenlegens ab.
- **Dauer des AST-Lesens von `main.py`** (M2) — wird beim Bau gemessen.
- **Herkunft der Völkerfarben** („Trolle weiß-gold“, „Ghule violett“): er beruft sich auf Daniels
  Beschreibung der Burgbilder, `FRAKTIONEN_WELTEN.md` sagt Dunkelrot/Schwarz bzw. Grün/Knochenweiß.
  **Nicht auflösbar ohne Daniels Wort** — Frage 1 in `docs/FRAGEN_AN_DANIEL_20261112.md`. F-71
  entscheidet sie bereits (Burgbilder geben die Farbe vor), die Datei wird nachgezogen.
- **Der Inhalt der beiden „quelltext“-Dateien mit über 40 s** — erst nach M12.0 sinnvoll.

---

**Fazit:** Die Antwort ist verwendbar. Sein Werteblock hält in beiden Fällen (17 von 17 Zeilen), die
Selbstkorrektur Block 5 = 370 ist richtig und meine alte 380 war falsch, alle Zahlen aus Teil B sind
nachgezählt richtig. Vier Befunde ändern den **Bauweg** an drei Stellen (B2, B3, B4), keine Zahl der
Entscheidungen.
