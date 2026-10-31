# Ausbildungsdauer je Einheit — was die Originalquellen belegen

**Datum:** 31.10.2026
**Zweck:** Zusammenstellen, was die Originalquellen über die **Dauer der Einheitenausbildung** und
über die **Abhängigkeit dieser Dauer von der Gebäudestufe** sagen. Dieses Papier belegt nur, es
ändert keinen Code und keine Daten. Wo eine Zahl nicht in den Quellen steht, steht hier
ausdrücklich **nicht belegt**; es wird nichts geschätzt.

**Geprüfte Dateien:**

| Datei | Gelesen | Ergebnis für die Frage |
|---|---|---|
| `docs/original/Spielanleitung_2005/einheiten.php.txt` (22 Zeilen) | vollständig | **eine** Richtungsaussage (Z. 12–15), keine Zahl |
| `docs/original/Spielanleitung_2009_Textfassung.txt` (1366 Zeilen) | Ausbildungsteile + grep über alle 1366 Zeilen | **eine** Richtungsaussage (Z. 501–506), keine Zahl |
| `docs/original/Spielanleitung_2005/einheitentabelle.php.txt` | vollständig | Spalten: Bezeichnung, Beschreibung, Voraussetzung — **keine Zeitspalte** |
| `docs/original/Spielanleitung_2005/einheiteninfo.php.txt` | vollständig | keine Treffer für "Ausbild", "Minuten", "Dauer", "Stufe" |
| `docs/original/Spielanleitung_2005/anleitung.php.txt` | vollständig | keine Treffer für "Ausbild", "Minuten", "Dauer", "Stufe" |
| `docs/original/ORIGINAL_Einheiten_Waren_Rohstoffe.md` | vollständig | Z. 23 fasst die Richtung zusammen, keine Zahl |
| `docs/original/ORIGINAL_Werte_Einheiten.md` | vollständig | keine Treffer für "Dauer", "Minuten", "Ausbild" |
| `docs/quellen/ABWEICHUNGEN_2006_zu_2009.md` | Z. 85–130 | Z. 94, 123: Richtung belegt, **Zahl offen** |
| `docs/quellen/ORIGINAL_GEBAEUDE_UND_FREISCHALTUNG.md` | grep "Dauer" | Z. 56/84: Dauer **nur für Forschung** belegt (Stufe²) |
| `docs/ENTWURF_AUSBILDUNG_HERSTELLER_20261030.md` | Z. 95–125, 140–155, 210–300 | Z. 107–112, 296: "Handbuch nennt KEINE Ausbildungsdauer" |
| `data/units.json` (28 Einheiten) | Struktur aller 28 Einträge geprüft | **kein Feld** für Dauer/Zeit (Felder: kategorie, gebaeude, kosten, waren, voraussetzung, kriegspunkte, werte, icon, ladung, nicht_original) |
| `data/buildings.json` | drei Ausbildungsstätten | `stufen`: "wird stufenweise ausgebaut; je höher die Stufe, desto schneller …" |
| `data/gebaeude_wirkung.json` | Z. 24–42 | Stufen **5** ist als VORSCHLAG markiert |
| `src/spieloekonomie.py` | Z. 460–500 | Z. 493–496: feste Pilotdauer, Stufe wirkt **nicht** |
| `src/bonus_system.py` | Z. 25–45, 75–100, 140–152 | Z. 33–36: `UNIT_TRAIN_BASE` = 0.0 ("nicht angegeben") |
| `data/spieloekonomie.json` | grep "ausbildung" | Z. 34: `pilot_ausbildung_minuten: 20` |

---

## 2. Belegstellen und Tabelle

### 2.1 Die beiden einzigen Belegstellen zur Ausbildungsdauer

**B1 — Spielanleitung 2005, `einheiten.php.txt` Z. 12–15:**
> "Zum Bau von Karren benötigt Ihr einen Stellmacher, zum Ausbilden von Kundschaftern eine Diebesgilde und
> Armee-Einheiten werden in der Kriegerakademie ausgebildet. In jeder Eurer Siedlungen kann jeweils nur eine
> Kriegerakademie, eine Diebesgilde und ein Stellmacher errichtet werden. Diese Gebäude werden stufenweise
> ausgebaut. **Je höher die Stufe, desto schneller werden die entsprechenden Einheiten ausgebildet.**"

**B2 — Handbuch 2009, `Spielanleitung_2009_Textfassung.txt` Z. 501–506:**
> "Zum Bau von Karren und Belagerungswaffen benötigst Du einen Stellmacher, zum Ausbilden
> von Kundschaftern eine Diebesgilde und Armee-Einheiten werden in der Kriegerakademie
> ausgebildet.
> In jeder Deiner Siedlungen kann jeweils nur eine Kriegerakademie, eine Diebesgilde und ein
> Stellmacher gebaut werden. Die Gebäude werden stufenweise ausgebaut. Je höher die Stufe,
> **desto schneller werden dort Einheiten ausgebildet.**"

Beide Quellen stimmen überein: **die Stufe wirkt, aber keine Quelle nennt eine Zahl, eine Einheit
(Minuten/Stunden) oder eine Steigung.** Ein Satz wie "Dauer je Stufe halbiert" steht in **keiner**
der geprüften Dateien. `grep -rn -i "halbier\|je Stufe" docs/original/` trifft nur **andere**
Systeme — `ORIGINAL_Einheiten_Waren_Rohstoffe.md:183-196` (Mauerbau +10 %, Forschungseffekte
"+10 % je Stufe", Rohstoffkosten "verdoppeln sich je Stufe") — und **nichts** zur Ausbildung.

### 2.2 Tabelle: 28 Einheiten

"keine Zahl" heißt: die Quelle nennt für diese Einheit **keinen** Zeitwert (Wortlaut siehe B1/B2 —
er gilt für alle Einheiten der jeweiligen Stätte, nicht je Einheit). Die Zuordnung Einheit → Stätte
steht in `data/units.json` (Feld `gebaeude`), belegt durch B1/B2.

| Einheit | Ausbildungsdauer laut Quelle (Wortlaut) | Datei:Zeile | Gebäudestufe als Faktor? | Urteil (BELEGT / NICHT BELEGT) |
|---|---|---|---|---|
| Bürgerwehr | keine Zahl — nur "Je höher die Stufe, desto schneller" | `einheiten.php.txt:12-15`; `Spielanleitung_2009_Textfassung.txt:501-506` | JA, Richtung (schneller); Höhe/Formel nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Kämpfer | keine Zahl | `einheiten.php.txt:12-15`; `…2009…:501-506` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Krieger | keine Zahl | `einheiten.php.txt:12-15`; `…2009…:501-506` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Ritter | keine Zahl | `einheiten.php.txt:12-15`; `…2009…:501-506` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Paladin | keine Zahl | `einheiten.php.txt:12-15`; `…2009…:501-506` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Kurzbogenschütze | keine Zahl | `einheiten.php.txt:12-15`; `…2009…:501-506` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Bogenschütze | keine Zahl | `einheiten.php.txt:12-15`; `…2009…:501-506` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Langbogenschütze | keine Zahl | `einheiten.php.txt:12-15`; `…2009…:501-506` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Armbrustschütze | keine Zahl | `einheiten.php.txt:12-15`; `…2009…:501-506` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Streuner | keine Zahl | `einheiten.php.txt:12-15`; `…2009…:501-506` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Gauner | keine Zahl | `einheiten.php.txt:12-15`; `…2009…:501-506` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Dieb | keine Zahl | `einheiten.php.txt:12-15`; `…2009…:501-506` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Meisterdieb | keine Zahl | `einheiten.php.txt:12-15`; `…2009…:501-506` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Kundschafter | keine Zahl | `einheiten.php.txt:12-15`; `…2009…:501-506` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Waldläufer | keine Zahl | `einheiten.php.txt:12-15`; `…2009…:501-506` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Handkarren | keine Zahl — "Zum Bau von Karren … benötigst Du einen Stellmacher" | `…2009…:501`; `einheiten.php.txt:12` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Einspänner | keine Zahl | `…2009…:501`; `einheiten.php.txt:12` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Zweispänner | keine Zahl | `…2009…:501`; `einheiten.php.txt:12` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Handelskarawane | keine Zahl | `…2009…:501`; `einheiten.php.txt:12` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Große Handelskarawane | keine Zahl | `…2009…:501`; `einheiten.php.txt:12` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Siedlerkarren | keine Zahl | `…2009…:501`; `einheiten.php.txt:12` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Belagerungsturm | keine Zahl — "Karren und Belagerungswaffen" | `…2009…:501`; `…2009…:824` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Ramme | keine Zahl | `…2009…:501`; `…2009…:824` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Großer Belagerungsturm | keine Zahl | `…2009…:501`; `…2009…:824` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Große Ramme | keine Zahl | `…2009…:501`; `…2009…:824` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Balliste | keine Zahl | `…2009…:501`; `…2009…:824` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Katapult | keine Zahl | `…2009…:501`; `…2009…:824` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |
| Großes Katapult | keine Zahl | `…2009…:501`; `…2009…:824` | JA, Richtung; Höhe nein | Stufenfaktor BELEGT · Dauer NICHT BELEGT |

**Ergebnis in einem Satz:** 0 von 28 Einheiten haben in den Quellen eine Ausbildungsdauer; 28 von
28 haben die belegte **Richtung** "höhere Gebäudestufe = schneller", aber **keine** belegte Zahl.

### 2.3 Kontrast: was sehr wohl eine belegte Zeitformel hat

Nur die **Forschung** hat eine Formel im Handbuch — `…2009…:422-423`:
> "Ein Forschungsauftrag dauert (Neue Stufe*Neue Stufe) in Stunden."

Das ist eine andere Baustelle (`src/forschung.dauer_stunden()`) und **kein** Beleg für die
Ausbildungsdauer. Ebenso hat nur die **Warenfertigung** einen Beispielwert —
`…2009…:471-475`: "Für ein Schwert benötigt Dein Schmied 20 Minuten" (Werkstatt, nicht Ausbildung).

### 2.4 Fallstricke, die wie ein Dauer-Beleg aussehen, aber keiner sind

- `…2009…:1349`: "Je besser die Spionageeinheit, desto schneller kann sie andere Siedlungen
  erreichen." → **Reisegeschwindigkeit** (Feld `GS` in `data/units.json`), nicht Ausbildungszeit.
- `…2009…:29`: "Eine Forschung die 2 Tage und 10 Stunden dauert" → Forschung.
- `…2009…:1139`: "Wenn also 2 Stunden angegeben sind, benötigen Deine Einheiten 2 Stunden" → Marschzeit.
- `src/bonus_system.py:83-89`: `get_training_time_multiplier` **erhöht** das Tempo mit der Stufe,
  aber `UNIT_TRAIN_BASE` ist `0.0` (Z. 36, Kommentar: "Das Handbuch nennt … KEINE
  Ausbildungsdauer. Deshalb 0.0 = 'nicht angegeben' statt eines erfundenen Werts"). Ein Aufruf
  liefert über `max(0.5, …)` (Z. 149) still **0,5 Minuten** — ein erfundener Wert, kein Beleg.

---

## 3. Was die Quelle NICHT regelt

1. **Keine Dauer je Einheit** — kein Minuten-, Stunden- oder Tageswert für irgendeine der 28 Einheiten.
2. **Keine Steigung/Formel** — "desto schneller" ohne Faktor; weder linear, noch halbierend, noch
   "Dauer je Stufe halbiert" irgendwo belegt.
3. **Keine Anzahl der Ausbaustufen** der drei Stätten. Die `5` in `data/gebaeude_wirkung.json:25`
   ist dort selbst als **VORSCHLAG** markiert.
4. **Kein Unterschied zwischen Einheiten derselben Stätte** — ob ein Paladin länger als eine
   Bürgerwehr braucht, sagt keine Quelle (die Einheitentabelle `…2009…:517-518` hat die Spalten
   LE/AT/PA/SI/HE/RS/TP/GS/MU/SK und **keine** Zeitspalte; `einheitentabelle.php.txt` hat nur
   Bezeichnung/Beschreibung/Voraussetzung).
5. **Keine Wirkung von Forschung auf die Ausbildungsdauer** — Forschung erscheint in
   `data/units.json` nur als `voraussetzung` (z. B. "Kriegskunst 1"), nie als Tempo-Hebel.
6. **Keine Aussage zur Parallelität** — im Gegenteil: "in eine Warteschlange gestellt und
   nacheinander ausgebildet" (`einheiten.php.txt:21`, `…2009…:512-513`). Ob mehrere Stätten
   derselben Art (in verschiedenen Siedlungen) parallel ausbilden, regelt keine Quelle.
7. **Keine Aussage, welche Stufe gilt**, wenn während der Ausbildung ausgebaut wird (Stufe bei
   Auftragserteilung oder bei Fertigstellung?) — nicht geregelt.
8. **Keine Rundungs- oder Mindestdauer** (kein "mindestens 1 Minute" o. Ä.).
9. **Kein Originalwort "Kaserne"** — `grep -rn -i "kaserne" docs/original/` liefert **0 Treffer**;
   die Stätte heißt in beiden Quellen **Kriegerakademie**. "Kaserne" ist nur der Remake-Menütitel
   (`src/main.py:6385`).
10. **Keine Aussage zur Dauer bei Stufe 0** (Stätte nicht gebaut) — dann ist Ausbildung ohnehin
    gesperrt (`src/spieloekonomie.py:480-481`: "Ausbildungsstätte fehlt vor Ort.").

---

## 4. Vorschlag für die Umsetzung

**VORSCHLAG — nicht belegt.** Belegt ist nur die Richtung "streng fallend mit der Stufe"; jede
streng monoton fallende Funktion erfüllt die Quelle. Die folgenden Zeilen sind eine Wahl, keine
Ableitung.

- Basis bleibt `pilot_ausbildung_minuten` = 20 (`data/spieloekonomie.json:34`) für **Stufe 1** —
  damit ändert sich das heutige Spielgefühl auf Stufe 1 nicht.
- Neue Funktion `ausbildungsdauer_sekunden(einheit, stufe)` in `src/spieloekonomie.py`, in
  `ausbildung_start` (Z. 495) statt des festen `* 60` aufrufen:
  `dauer_s = pilot_ausbildung_minuten * 60 / max(1, stufe)` (linear) — Alternative:
  `* 0.5 ** (stufe - 1)` (halbierend).
- `stufe` kommt aus `gebaeude_wirkung.ausbildungsstaette(...)` (nicht neu erfinden); `max(1, stufe)`
  schützt gegen Stufe 0.
- Begründung der linearen Wahl: kleinste Annahme, monoton fallend, Stufe 5 = 1/5 der Zeit — und sie
  ist ohne Codeänderung korrigierbar, wenn Daniel eine andere Steigung will.
- `bonus_system.get_training_time` (Z. 146-150) **nicht** verwenden: `UNIT_TRAIN_BASE` = 0.0
  (Z. 36) macht daraus still 0,5 Minuten.
- Formel als `_vorschlag`-Feld in `data/spieloekonomie.json` dokumentieren, damit die Zahl ohne
  Codeänderung änderbar ist und der VORSCHLAG-Status sichtbar bleibt.
