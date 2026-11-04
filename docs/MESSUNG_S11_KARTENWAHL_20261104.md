# Messung S-11: Kartenwahl mit Feldverstaendnis (04.11.2026)

**Wozu:** S-11 verlangt (Konzept, woertlich): "zwei Bots mit derselben Kandidatenliste und
verschiedenen Taktiken waehlen nachweislich verschiedene Karten; die gewaehlte Karte traegt den
Engpass-Rohstoff der Taktik am besten von den dreien". Bis heute kannte die Kartenwahl die Taktik
nicht - entschieden `botkern.oekonomie_kartenwahl` (Stufe `mittel`: am schlechtesten gedeckte
Rohstoffachse) oder die alte Gold-Regel.

**Entwurf des starken Modells:** `deepseek-v4-pro`, 04.11.2026, 8.449 Zeichen, 21.543 Token
(davon 15.377 Denk-Token), 276 Sekunden. Die Erntetabelle des Entwurfs wurde Zeile fuer Zeile gegen
die Mindestzahlen und `data/buildings.json` nachgerechnet und stimmt in allen 40 Werten. **Eine
Aussage wurde berichtigt:** der Entwurf nahm die "zwei kleinsten Ernten" als Engpass (Wolle, Pferde).
Das ist falsch, weil der Bedarf fehlt: ein Siedlerkarren braucht 4 Pferde (0,4 Stunden) und 100
Wolle, aber 150 Leder und 80 Metall, und eine Gruendung 480 Holz. Der Engpass wird deshalb aus
BEDARF / ERTRAAG gerechnet.

## 1. Der Bedarf eines Wachstumszyklus (aus dem Kern, nicht getippt)

| Rohstoff | Siedlerkarren | Gruendung (Gebuehr + Startpaket) | zusammen | Quelle |
|---|---|---|---|---|
| Holz | 200 | 480 | **680** | `spieloekonomie.U["Siedlerkarren"]`, `spieloekonomie.gruendungskosten()` |
| Nahrung | 300 | 250 | **550** | dieselbe Quelle |
| Stein | - | 300 | **300** | dieselbe Quelle |
| Leder | 150 | - | **150** | dieselbe Quelle |
| Wolle | 100 | - | **100** | dieselbe Quelle |
| Metall | 80 | - | **80** | dieselbe Quelle |
| Pferde | 4 | - | **4** | dieselbe Quelle |

## 2. Engpass je Taktik (Stunden = Bedarf / Ertrag der Mindestanlagen)

| Taktik | engster Rohstoff | zweiter | dritter | vierter |
|---|---|---|---|---|
| Pluenderer | Holz 52,3 h | Stein 33,3 h | Nahrung 29,0 h | Wolle 16,7 h |
| Waechterin | Holz 40,0 h | Wolle 33,3 h | Nahrung 27,5 h | Leder 18,8 h |
| Bastionier | Holz 52,3 h | Nahrung 34,4 h | Stein 23,1 h | Leder 18,8 h |
| Spaeherin | Holz 52,3 h | Stein 33,3 h | Wolle 33,3 h | Nahrung 29,0 h |
| Raecher | Holz 52,3 h | Nahrung 34,4 h | Stein 33,3 h | Wolle 33,3 h |

**Pferde sind bei KEINER Taktik ein Engpass** (unter 2 Stunden) - genau der Punkt, an dem der Entwurf
daneben lag.

## 3. Die Bewertung (S-11b, `botkern.taktik_kartenscore`)

    Punkte_Taktik(Karte) = Profil[Engpass 1] * Stunden[Engpass 1]
                         + Profil[Engpass 2] * Stunden[Engpass 2]

`Profil` ist `main.bot_kartenprofil` (Felder x Ertrag je Rohstoff, nur auf Gelaende, auf dem die
Anlage stehen darf). Bewertet werden nur die DREI Kandidaten der Spielregel. Gleichstand entscheidet
der groessere Wert beim engsten Rohstoff, dann beim zweiten, dann die Kennung - die Wahl ist damit
reproduzierbar.

## 4. Die Pruefzusage, gemessen (fuenf Kandidaten, fuenf Taktiken)

| Taktik | Engpass-Paar | gewaehlte Karte | Punkte |
|---|---|---|---|
| Pluenderer | holz / stein | `original-006` | 13.995,0 |
| Waechterin | holz / wolle | `original-118b` | 10.179,8 |
| Bastionier | holz / nahrung | `original-118b` | 15.180,9 |
| Spaeherin | holz / stein | `original-006` | 13.995,0 |
| Raecher | holz / nahrung | `original-118b` | 15.180,9 |

**Pluenderer und Waechterin waehlen bei DERSELBEN Kandidatenliste verschiedene Karten** - die
Pruefzusage ist erfuellt. Taktiken mit demselben Engpass-Paar waehlen mit Absicht dieselbe Karte
(Bastionier und Raecher, Pluenderer und Spaeherin); das ist die Folge der Rechnung, kein Fehler.

## 5. Messung: 24 Spieltage

| Bot | Doerfer | Anlagen je Dorf | Karten |
|---|---|---|---|
| Haug (Pluenderer) | 4 | 73 / 73 / 73 / 80 | 118b, 092, 111, 007 |
| Brynhild (Waechterin) | 4 | 97 / 82 / 85 / 66 | 102, 110, 105, 016 |
| Grom (Bastionier) | 4 | 74 / 73 / 88 / 92 | 108, 118b, 049, 005 |
| Silra (Spaeherin) | 4 | 90 / 90 / 82 / 63 | 018, 015, 031, 042 |
| Krank (Raecher) | 4 | 90 / 97 / 95 / 77 | 014, 078, 019, 041 |

**Dorfzahl 4/4/4/4/4 wie vor dem Schnitt.** Zwei Doerfer bekamen eine andere Karte als mit der Stufe
`mittel` (Brynhild Siedlung 2, Krank Siedlung 2), die Anlagenzahlen verschieben sich entsprechend
leicht.

## 6. Schalter und Pruefstand

- Die Stufe steht in `data/bot_wirtschaft.json`: `"kartenwahl_stufe": "engpass"`. Die alten Stufen
  `mittel`, `schwer` und `leicht` bleiben waehlbar - ein Wort in der Datendatei, kein Code.
- Wache `tests/test_s11_kartenwahl_engpass.py` **102/0/0**.
- Gegenprobe: Taktik in `bot_kartenwahl_nach_engpass` ignoriert (immer Pluenderer) - **5 Pruefungen
  rot**, `src/main.py` per SHA256 unveraendert zurueck.
