# Einhängen der feineren Karten-Module (Schritt 29, 05.10.2026)

Beleg-Dokument zum Protokolleintrag **29**. Kurzfassung des Protokolls; hier stehen die
Einzelheiten, die dort nicht hineinpassen.

## Was eingehängt wurde

| Modul | Wohin | Wirkung |
|---|---|---|
| `src/karten_optik_fein.py` | `main._zeichne_siedlungskarte` | Gelände mit astra-Farben und Strukturformen, Uferband **nur** an echten Land-Wasser-Grenzen, Wege 8 px mit 4 px Innenlinie, Baukörper je Gebäudefamilie mit Stufenpips, goldener Auswahlrahmen zuletzt, Koordinaten in der 18-px-Leiste |
| `src/welt_optik_fein.py` | `main._draw_map`, `_welt_uebersicht_zeichnen`, `_welt_detail_zeichnen`, Spaltenbreite | 1-px-Raster nur zu ungleichen Nachbarn, Ufersaum, deterministische Varianten aus den Feldkoordinaten, Lager/Ruine als Silhouette, Regionsnamen mit Schatten, Übersicht 4 × 4 px je Feld, Panel 248 px / 12 px |

Die vorige Generation (`src/karten_optik.py`, `src/welt_optik.py`) bleibt **als Renderer**
(`zeichne`) im Projekt — die Feinmodule liefern ausdrücklich nur Pläne (Daten), keine Zeichnung.

## Maße in der Oberfläche, die sich dadurch geändert haben

| Was | vorher | jetzt | Quelle |
|---|---|---|---|
| Rand um das Siedlungsraster | 20 px | 18 px | astra „Siedlung 3": äußere Rasterleiste 18 px |
| Koordinaten | im Feldinneren (A1 …) + Achsen | nur in der Leiste | astra: „Koordinaten … verlegen" |
| Stufe auf dem Feld | Text „St. n" | Stufenpips am Baukörper | astra: „Stufenanzeigen aus den Gebäudesilhouetten herausnehmen" |
| Auswahlrahmen | Cyan #38BDF8 | Gold #E4C77D auf #172128 + vier Eckwinkel | astra „Siedlung 3" |
| Auswahl weltweit | Cyan-Rahmen | Gold #E4C77D, 2 px eingerückt, 6-px-Winkel | astra „Welt 3" |
| Übersichtskarte | fest 132 px (6,6 px je Feld) | 80 px (4 × 4 px je Feld) | astra „Welt 3" |
| Sichtrahmen der Übersicht | #F3F4F6, 2 px | #F2EEDB, 1 px | astra „Welt 3" |
| Detailpanel rechts | 300 px, Umbruch 260/270 | 248 px, Umbruch 224 (12 px Innenabstand) | astra „Welt 3" |

## Die drei Einhänge-Fallen aus `docs/PROJEKT_STAND.md` 0c

1. **Geländefarben für Steppe/Hügel/Sumpf** stehen nicht im astra-Bericht. Sie kommen über
   `gelaende.farbe()` — im Modul über `_flaeche_farbe()`; für die vier genannten Arten bleiben die
   astra-Werte maßgeblich. Keine zweite Farbwahrheit.
2. **`#637451` als Lichtfarbe von Ebene UND Wald — von Daniel entschieden (05.10.2026):**
   Er hat auf die Frage „trennen?" geantwortet: *„Trennen: der Wald bekommt eine aus seiner eigenen
   Farbe abgeleitete Lichtfarbe."* Umgesetzt in `src/welt_optik_fein.py`:
   **`WELT1_LICHT_WALD = #6A7E6C = _aufhellen(#405A43, 0.22)`**. Die **Ebene** behält den astra-Wert
   `#637451`. **Der Faktor 0,22 ist gerechnet, nicht erfunden:** astra nennt zu Gebirge und Wasser
   Basis **und** Lichtfarbe; daraus ergibt sich der Aufhellungsgrad Richtung Weiß
   (Gebirge 0,218 · Wasser 0,228 → Mittel 0,223 → gerundet 0,22). Vier neue Prüfungen in
   `tests/test_welt_optik_fein.py` (**128 → 132**); die Entscheidung steht auch in
   `offene_luecken()` des Moduls.
3. **Raster 8×7 (astra) gegen 8×5 = 40 Felder (Projekt).** Die Module nehmen `spalten`/`zeilen` als
   Parameter; der Aufrufer übergibt die Werte der Siedlungskarte. astra hält die 8×7 für
   vorgegeben — **das ist Frage 12 an Daniel**, nicht stillschweigend geändert.

## Eine Modul-Erweiterung, die nötig war

`karten_optik_fein.koordinatenleiste_plan()` bekam die optionalen Parameter `spaltennamen` und
`zeilennamen`. Ohne sie hätte die neue Leiste **Ziffern** gezeigt, während das Detailpanel und der
Spielstand weiter **„D3"** schreiben (zweite Wahrheit für dieselbe Koordinate). Voreinstellung
bleibt die Ziffer; eine zu kurze Namensliste wirft einen `ValueError`, statt still zu mischen.
Vier neue Prüfungen in `tests/test_karten_optik_fein.py` (**80 → 84**).

## Entfernt

`main._welt_regionen` — die Regionsnamen samt Positionen rechnet jetzt
`welt_optik_fein.regionen_plan_fein()`. Zwei Stellen, die dieselben neun Namen auf dieselbe Weise
platzieren, wären eine zweite Wahrheit. Die Prüfdatei zählt die neun **Namen** über das Tag
`weltname` (die neun Schatten tragen `weltschatten`) — die Aussage bleibt „neun Namen, einmal groß".

## Prüfbelege

| Prüfung | Ergebnis |
|---|---|
| `tests/test_kartenansicht.py` | **57 bestanden, 0 Fehler** (vorher 40) |
| `tests/test_weltkarte.py` | **82 bestanden, 0 Fehler** (vorher 58) |
| `tests/test_startspiel.py` | **46 bestanden, 0 Fehler** |
| `tests/test_karten_optik_fein.py` | **84 bestanden, 0 Fehler** (vorher 80) |
| `tests/test_welt_optik_fein.py` | **128 bestanden, 0 Fehler** |
| `tests/test_gui_fehler.py` | 23 bestanden, 0 Fehler, 1 Befund (unverändert) |
| `tools/pruefe_verdrahtung.py` | 17 Module verdrahtet, 0 nur importiert, 0 nicht eingebunden |
| Sammellauf (41 Dateien) | **2640 bestanden, 0 Fehler, 21 Befunde** (vorher 2599/0/21) |
| Tempo (gemessen) | Weltkarte 0,28 s / 4046 Objekte bei 48 px · Siedlungskarte 0,14 s / 494 Objekte |

Zwei alte Prüfannahmen mussten aufgeben — sie prüften die **vorige** Fassung:
`test_startspiel` erwartete den Cyanrahmen (jetzt Gold nach astra) und den Stempel „St. n" auf dem
Feld (jetzt steht dort **kein Text** mehr; Name, Stufe und Ertrag nennt die Zeile unter der Karte).

## Noch offen (Daniel)

Am 05.10.2026 um 14:2x hat Daniel die Fragen vorgelegt bekommen (5 Fragen in einer Liste). Er hat
**eine** beantwortet (die Lichtfarbe, siehe Falle 2) — die folgenden sind **unbeantwortet
übersprungen** und bleiben offen:

1. **Zeitfaktor** ×180 bestätigen oder ändern (`data/spielzeit.json`).
2. **Die neun Geländeregeln** bestätigen oder ändern (eine Zeile je Gebäude in `data/buildings.json`).
3. **Sieg-/Niederlagebedingung** — heute unerreichbar (`is_defeated()`).
4. **Raster 8×7 oder 8×5** (Frage 12).

Beantwortet:

5. **Lichtfarbe `#637451`** — **getrennt** (Wald bekommt `#6A7E6C`, gerechnet).
