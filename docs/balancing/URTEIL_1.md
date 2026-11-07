# Urteil B-2 - A/B-Lauf des Regelkreises

Erzeugt von `tools/balance_kreis.py --urteil` (Ablauf Schritt 9). Das Urteil ist eine Rechnung ueber zwei Messungen, keine Meinung: dieselben Startwerte, dieselbe Laenge, einmal mit und einmal ohne Aenderung.

## Messumfang

| Feld | Wert |
|---|---|
| Startwerte | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 |
| Laenge | 12 Spieltage |
| Stil | breit |
| Laeufe je Seite | 10 |
| Wurzel der Aenderung | tempoeraere Kopie von `src/` und `data/` |

## Der gepruefte Vorschlag

| Feld | Wert |
|---|---|
| Datendatei | `data/baupreise.json` |
| Gebaeude | kriegerakademie |
| Groesse | holz (senken) |
| Wert | 32 -> **29** |
| Schrittweite | 9.38 Prozent |
| Fehlbetrag vorher | 0.8368 |

## Zielgroesse (Punkte je Spieltag, Zielwert 3.3)

| | vorher | nachher |
|---|---|---|
| Punkte je Spieltag | 3.5 | 3.5 |
| Abweichung vom Ziel | 6.06 Prozent | 6.06 Prozent |
| gefordert | mindestens 20 Prozent besser | |

## Korridore (Sollkurve, `data/sollkurve.json`)

| Groesse | Fehlbetrag vorher | Fehlbetrag nachher | Tage draussen vorher | nachher |
|---|---|---|---|---|
| holz | 0.8368 | 0.8379 | 12 | 12 |
| stein | 0.7432 | 0.7438 | 11 | 11 |
| nahrung | 0.5216 | 0.5215 | 12 | 12 |
| gold | 0.5827 | 0.5827 | 11 | 11 |

## Erstes Gefecht

Tag 2.0 vorher, Tag 2.0 nachher (`null` = in keinem Lauf gemessen, nicht Tag 0).

## Urteil

**ABGELEHNT**

- Zielabweichung verbessert sich nur um 0.0 Prozentpunkte (6.06 -> 6.06 Prozent), gefordert sind mindestens 20.0 Prozent
- holz wird schlechter (0.8379 statt 0.8368 Fehlbetrag)
- stein wird schlechter (0.7438 statt 0.7432 Fehlbetrag)
- Beobachtung: nahrung bleibt ausserhalb des Korridors (0.5216 -> 0.5215)
- Beobachtung: gold bleibt ausserhalb des Korridors (0.5827 -> 0.5827)

**Nichts wurde uebernommen.** Ein angenommenes Urteil ist eine Freigabe fuer Daniel, kein Schreibvorgang: `data/` bleibt unveraendert, bis er den Wert setzt.
