# Prüfung der Ökonomie-Regeldaten (Entwurf Schritt 1–2)

## 1. Zeitstempel und Stand
- Stand: **2026-10-05 17:38** (geholt mit `date '+%Y-%m-%d %H:%M'`).
- Gegenstand: `data/gelaende.json` → `kartenvorrat`; `data/spieloekonomie.json`; `src/spieloekonomie.py`. Richtschnur: `docs/audits/entwurf_spieloekonomie_sol_2026-10-05.txt` (i.F. „Entwurf").
- Nur gelesen; die Zahlen zusätzlich mit einem Standalone-Skript (Scratch, ohne Projektimport) aus den JSON-Werten nachgerechnet. Keine Projektdatei geändert, kein git, kein Test, kein Spielstart.
- Nicht geprüft: ob die Karten spielbar/balanciert sind, Laufzeit der Kernfunktionen, die spätere main-Anbindung.

## 2. Vollständigkeit
Der JSON-Block Z.214–231 nennt: `version`, `baukunst_mindeststufe`, `gruendung`, `vergabe_stunden`, `versorgung_stunden`, `mindestsiedlungen`, `spezialistenfaktor`, `portfoliofaktor`, `plan`, `kartenpreisgrenzen`, `vorratspreisgrenzen`, `pilot_ausbildung_minuten`, `pilot_waren_minuten`, `bots`, `_herkunft` (Entwurf Z.214–231).
- **Fehlt keiner.** `data/spieloekonomie.json` Z.4–40 enthält alle; automatischer Abgleich: „Entwurfs-Block Keys fehlen in Daten: []".
- **Zusätzlicher Schlüssel:** `bot_startplan` (spieloekonomie.json Z.41–45, plus `_hinweis` Z.2). Im Block Z.214–231 NICHT genannt.
  - Im Entwurf sonst belegt: Code-Nutzung `REGELN["bot_startplan"]` Z.1036, Definition Z.1073. Werte stimmen exakt: `grundbau`/`ausbau` = Z.1073 (nachgerechnet: OK). → dokumentierte, gedeckte Ergänzung (Schritt 8), kein Fremdschlüssel.
- `src/spieloekonomie.py` Z.36–242 setzt **genau die 18 Funktionen** des Blocks Z.251–413 um (`lade` … `vergabe`); keine fehlt, keine zusätzlich (Funktionsabgleich Z.251–413 ↔ Datei: identisch).

## 3. Zahlenabgleich Soll/Ist
| Wert | Soll (Entwurf) | Ist (spieloekonomie.json) | Beleg |
|---|---|---|---|
| version | oekonomie-1 | oekonomie-1 | Z.215 / Z.4 |
| baukunst_mindeststufe | 1 | 1 | Z.215 / Z.5 |
| gruendung.hausmultiplikator | 4 | 4 | Z.216 / Z.8 |
| gruendung.reserve_hausmultiplikator | 2 | 2 | Z.216 / Z.9 |
| gruendung.nahrung_karrenanteil | 0.5 | 0.5 | Z.216 / Z.10 |
| gruendung.reserve_nahrung_einheit | "Streuner" | "Streuner" | Z.217 / Z.11 |
| gruendung.karren | "Siedlerkarren" | "Siedlerkarren" | Z.218 / Z.12 |
| gruendung.forschung | "Wagenbau" | "Wagenbau" | Z.218 / Z.13 |
| gruendung.stufe | 1 | 1 | Z.218 / Z.14 |
| vergabe_stunden | 24 | 24 | Z.219 / Z.16 |
| versorgung_stunden | 24 | 24 | Z.219 / Z.17 |
| mindestsiedlungen | 4 | 4 | Z.219 / Z.18 |
| spezialistenfaktor | 1.4 | 1.4 | Z.220 / Z.19 |
| portfoliofaktor | 1.0 | 1.0 | Z.220 / Z.20 |
| plan (9 Werte) | 180/50/100/300/6/6/6/1/5 | idem | Z.221–222 / Z.21–31 |
| kartenpreisgrenzen | [0.5,4.0] | [0.5,4.0] | Z.223 / Z.32 |
| vorratspreisgrenzen | [0.5,2.0] | [0.5,2.0] | Z.223 / Z.33 |
| pilot_ausbildung_minuten | 20 | 20 | Z.224 / Z.34 |
| pilot_waren_minuten | 20 | 20 | Z.224 / Z.35 |
| bots.leicht | false/24/6/0.0 | idem | Z.226 / Z.37 |
| bots.mittel | true/6/12/0.0 | idem | Z.227 / Z.38 |
| bots.schwer | true/1/24/0.0 | idem | Z.228 / Z.39 |
- **Ergebnis: 0 Abweichungen.** Alle Skalare, `plan`, `gruendung`, `bots` stimmen (Skriptausgabe „… OK", keine „ABWEICHUNG").

## 4. Tabelle B gegen `data/gelaende.json`
Spaltenreihenfolge Entwurf Z.69 = Grasland, Steppe, Wald, Hügel, Berg, Nebelsee, Sumpf; gleiche Reihenfolge in gelaende.json Z.142/145–153.
| Kennung | Entwurf Z.70–79 | gelaende.json | sum6/sum7 |
|---|---|---|---|
| start | 8,8,8,7,7,2,16 | Z.142 identisch | 40/56 |
| ausgleich_a | 9,7,8,6,8,2,16 | Z.145 identisch | 40/56 |
| ausgleich_b | 7,9,9,7,6,2,16 | Z.146 identisch | 40/56 |
| ausgleich_c | 8,8,7,8,7,2,16 | Z.147 identisch | 40/56 |
| holz | 3,2,28,2,4,1,16 | Z.148 identisch | 40/56 |
| minen | 3,2,2,10,22,1,16 | Z.149 identisch | 40/56 |
| farmen | 27,6,2,2,2,1,16 | Z.150 identisch | 40/56 |
| holz_minen | 3,2,16,5,13,1,16 | Z.151 identisch | 40/56 |
| holz_farmen | 17,2,16,2,2,1,16 | Z.152 identisch | 40/56 |
| minen_farmen | 17,2,2,5,13,1,16 | Z.153 identisch | 40/56 |
- **Alle zehn Zeilen exakt gleich; jede Summe 56, davon 40 bebaubar** — deckt die Behauptung Entwurf Z.80 (nachgerechnet). Mindestbesatz (Wald≥2, Berg≥2, Grasland≥3, Nebelsee≥1) in allen Karten erfüllt (gelaende.json Z.159–165).
- Kennungen (IDs) exakt wie Entwurf Z.70–79. Namen: Entwurf fordert Deutsch (Z.212), gibt aber keine Zeichenkette je Zeile vor; die deutschen Namen in gelaende.json Z.141/145–153 sind daher **nicht gegen den Entwurf** prüfbar (nur gegen die Forderung „Deutsch").

## 5. Ableitung der vier Daniel-Zahlen
Grundwerte gelesen: Haus = 80 Holz/50 Stein (baupreise.json Z.34); Siedlerkarren-Nahrung 300 (units.json Z.724); Streuner-Nahrung 100 (units.json Z.306).
- Gebühr = Haus × 4: **320 Holz / 200 Stein**; + Siedlerkarren-Nahrung 300 × 0,5 = **150 Nahrung** → **320/200/150** (Entwurf Z.110). Nachgerechnet: GEBUEHR {holz:320, stein:200, nahrung:150} ✓
- Startpaket = Haus × 2: **160 Holz / 100 Stein**; + Streuner-Nahrung = **100 Nahrung** → **160/100/100** (Entwurf Z.111). ✓
- Mindestbestand = Gebühr + Paket: **480 / 300 / 250** (Entwurf Z.112). ✓
- ein **Siedlerkarren**: `gruendung.karren="Siedlerkarren"` (Z.12), `absicht` erzwingt ≥1 Karren (src Z.212–213) → genau ein Karren (Entwurf Z.108/114/115). ✓
- **Alle vier Werte sind aus den Daten ableitbar und die Ableitung ergibt exakt die bestätigten Zahlen.** Die Literale 320/160/480 stehen NICHT im JSON (nur Multiplikatoren 4/2) — die Daten sind quellentreu abgeleitet, nicht hartkodiert.

## 6. Unbelegte Zahlen ohne VORSCHLAG-Kennzeichnung
- Handbuch-Beleg: `docs/original/Spielanleitung_2009_Textfassung.txt`. Die vier Daniel-Zahlen sind dort **nicht** belegt: „320", „480", „160 Holz", „150 Holz", „300 Stein", „200 Stein" — alle Suchen: nicht im Handbuch. (Die Treffer 160/250 in HB Z.1233/1236 sind Mauer-Preise, keine Gründungskosten.)
- Kennzeichnung im Datenstand: spieloekonomie.json trägt `_herkunft` = „VORSCHLAG…" (Z.3, dateiweit) und `bot_startplan._hinweis` = „VORSCHLAG" (Z.42); gelaende.json `kartenvorrat._hinweis`/`._herkunft` = „VORSCHLAG" (Z.137/138).
- **Befund: keine.** Keine Zahl steht ohne Vorschlag-Kennzeichnung. Nebenbefund (kein Fehler): Die Datei markiert auch die im Entwurf als „BELEGT als Planposten" geführten Werte (Stein 50, Nahrung 100, Gold 300, Entwurf Z.44–46) pauschal als VORSCHLAG — sie behauptet damit weniger Beleg als der Entwurf, nie mehr.

## 7. Offene Lücken für die Umsetzung
Der Entwurf nennt je Schritt 1–10 einen neuen Test (F): test_spieloekonomie.py (Z.232), test_siedlungskarte.py-Saatliste (Z.415), test_lokale_lager.py + test_warentransport.py (Z.505/504), test_warenrezepte.py + test_ausbildungsauftraege.py (Z.590), test_oekonomie_uhr.py (Z.648), test_lokale_forschung.py (Z.686), test_versorgungsziel.py (Z.715), test_bot_oekonomie.py + test_handel_transaktion.py (Z.753/1074), test_gui_fehler.py (Z.1089), test_gruendung_transaktion.py (Z.876).
- Vorhanden: `tests/test_spieloekonomie.py`, `tests/test_warenrezepte.py`, `tests/test_gui_fehler.py` (Verzeichnis geprüft, 45 Dateien).
- **Fehlen noch (noch nicht Teil von Schritt 1–2):** test_warentransport, test_lokale_lager, test_ausbildungsauftraege, test_oekonomie_uhr, test_lokale_forschung, test_versorgungsziel, test_bot_oekonomie, test_handel_transaktion, test_gruendung_transaktion.
- Nicht umgesetzt (bewusst, Entwurf Z.206/417–1089): Schritte 3–10 (Transport, Rezepte, Uhr, lokale Forschung, Versorgungsziel, Bot/Handel, main-Anbindung). Nichts ruft `src/spieloekonomie.py` auf — der Altmodus läuft unverändert (Entwurf Z.206; src Z.11–12). Aktivierung erst nach Schritt 9/10 (Entwurf Z.1092).
- **Nicht prüfbar in diesem Auftrag:** Laufzeitverhalten der 18 Kernfunktionen und das Bestehen der vorhandenen drei Tests (kein Testausführung erlaubt).
