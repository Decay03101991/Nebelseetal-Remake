### 1. Befund in fünf Sätzen

1. In den vier geprüften Dateien (`auftraege.py` 638, `spieloekonomie.py` 1072, `werkstatt.py` 422, `kampfbericht.py` 492 Zeilen) gibt es mindestens acht doppelte Rechenwege; `_als_zahl`, `_als_int` und `_aufzaehlung` erscheinen in `auftraege.py` und `kampfbericht.py` doppelt, und die Karrenladung wird an drei Stellen unabhängig summiert (`auftraege.ladung_der_mission`, `kampfbericht.beute_staffel`, `kampfbericht.beute`).  
2. `auftraege.py` rechnet die Reisezeit-Spalte doppelt: `starten` und `_status_zeiten` berechnen identisch `ankunft = start + reisezeit`, `abreise = ankunft + aktion_dauer`, `rueck = abreise + reisezeit`.  
3. `spieloekonomie.py` kopiert die Manhattan-Distanz (`abs(a["x"]-b["x"]) + abs(a["y"]-b["y"])`) in `transport_start` und `handel_start` sowie die Importanteilsformel (`menge * importiert / lager`, 0 bei leerem Lager) in `verbrauchen`, `transport_start` und `handel_start`.  
4. Die zwei Beutefunktionen in `kampfbericht.py` teilen Kapazitäts- und Vorratsfilter; ihre Verteilungsrechnung ist nur ähnlich: `beute` füllt alphabetisch nach reiner Ladung, `beute_staffel` rechnet erst einen Staffelanteil und füllt den Rest fair auf.  
5. Die Bestandsanwendung ähnelt sich in `auftraege.spieldaten_anwenden`, `kampfbericht.spieldaten_anwenden` und `spieloekonomie.buchen`, ist aber nicht identisch: die einen kappen still mit `max(0, ...)`, `buchen` wirft eine Exception bei negativem Bestand.

### 2. Vorschläge

| # | Was | Dateien/Funktionen | Zeilen vorher → nachher | Risiko | Beweis: welche Prüfdatei | Reihenfolge |
|---|---|---|---|---|---|---|
| 1 | Zentrale Helfer `als_zahl`, `als_int`, `aufzaehlung`, `positive_ganze_werte` in neuem `hilfen.py` | `auftraege._als_zahl`, `_als_int`, `_aufzaehlung`; `kampfbericht._als_zahl`, `_als_int`, `_aufzaehlung` | geschätzt 38 → 8 | klein | `tests/test_auftraege.py`, `tests/test_kampfbericht.py`; `tests/test_kampf_einhaengung.py` ist im Code erwähnt | 1 |
| 2 | Gemeinsame Ladungsberechnung in `einheiten.py`: `ladung_der_gruppe(bestand)` | `auftraege.ladung_der_mission`; Kapazitätsteile in `kampfbericht.beute_staffel` und `kampfbericht.beute` | geschätzt 20 → 5 | klein | `tests/test_auftraege.py`, `tests/test_kampfbericht.py`, `tests/test_kampf_einhaengung.py` | 2 |
| 3 | Private `_reise_zeiten(start, reisezeit, aktion_dauer)` in `auftraege.py` | `auftraege.starten`, `auftraege._status_zeiten` | geschätzt 12 → 6 | klein | `tests/test_auftraege.py` | 3 |
| 4 | Private `_distanz` und `_import_anteil` in `spieloekonomie.py` | `transport_start`, `handel_start`, `verbrauchen`, `transport_fortschritt`, `handel_abschluss` | geschätzt 24 → 12 | klein/mittel | `tests/test_spieloekonomie.py` (nicht im Code benannt, daher offen); alle vorhandenen Transport-/Handelsprüfungen | 4 |
| 5 | `positive_ganze_werte` für Vorrats-/Bestandsfilter nutzen | `auftraege._bestand`; Vorratsfilter in `kampfbericht.beute`, `beute_staffel`, `beute_am_ziel` | geschätzt 15 → 5 | klein | wie Vorschlag 2 | 5 |
| 6 | `werkstatt._stufe_wert` auf zentrales `als_int` stützen | `werkstatt._stufe_wert` | geschätzt 5 → 1 | klein | `tests/test_werkstatt.py` (falls vorhanden, sonst offen) | 6 |
| 7 | Gekappte Bestandsaddition/-subtraktion als Helfer | `auftraege.spieldaten_anwenden`, `kampfbericht.spieldaten_anwenden` (nur ähnlich) | geschätzt 14 → 8 | mittel | `tests/test_auftraege.py`, `tests/test_kampfbericht.py` | 7 |

Hinweis: Die genannten Prüfdateien sind aus dem vorgelegten Code nicht vollständig abzulesen. `test_kampf_einhaengung` ist im Kommentar von `kampfbericht.py` erwähnt; die übrigen Namen sind die nach dem Projektaufbau zu erwartenden Prüfdateien und vor Umsetzung zu verifizieren.

### 3. Zusammenführung im Detail

#### 3.1 Gemeinsame Ladungsberechnung (Vorschlag 2)

Verschmilzt:  
- `auftraege.ladung_der_mission`  
- Kapazitätsschleifen in `kampfbericht.beute_staffel`  
- Kapazitätsschleife in `kampfbericht.beute`

Neue Funktion in `einheiten.py`:  
```python
def ladung_der_gruppe(einheiten_bestand: dict) -> int:
```

Parameter:  
- `einheiten_bestand`: `{name: anzahl}`; Anzahl kann `int`, `float` oder String sein.

Rückgabe:  
- Ganze Ladeplätze als `int`.

Kern:  
```python
gesamt = 0
for name, anzahl in einheiten_bestand.items():
    n = hilfen.als_int(anzahl, 0)
    if n > 0:
        gesamt += kapazitaet(name, n)
return max(0, gesamt)
```

Sonderfälle:  
- Negative, ungültige oder unbekannte Einheiten zählen 0.  
- Nicht-Transporteinheiten liefert `kapazitaet` 0.  
- Die Formeln sind heute wirklich identisch, weil alle drei Stellen `_als_int` bzw. `_bestand` mit positiver Filterung verwenden.

#### 3.2 Distanz und Importanteil (Vorschlag 4)

Verschmilzt:  
- Distanzberechnung in `transport_start` und `handel_start`.  
- Importanteilsberechnung in `verbrauchen`, `transport_start` und `handel_start`.

Neue Funktionen in `spieloekonomie.py`:  
```python
def _distanz(a: dict, b: dict) -> int:
    return abs(a["x"] - b["x"]) + abs(a["y"] - b["y"])

def _import_anteil(lager: float, importiert: float, menge: float) -> float:
    if lager <= 0:
        return 0.0
    return menge * importiert / lager
```

Parameter:  
- `_distanz`: zwei Orts-Dicts mit `x` und `y`.  
- `_import_anteil`: Bestand (`lager`), bereits importierte Menge (`importiert`), abzubuchende Menge (`menge`).

Rückgabe:  
- `_distanz`: ganzzahlige Entfernung.  
- `_import_anteil`: `float`, exakt wie die bisherige Formel.

Ersetzung:  
- `transport_start`: `d = _distanz(quelle, ziel)` und `anteil[r] = 0 if frachtkanal != "vorraete" else _import_anteil(v, importiert, m)`.  
- `handel_start`: `d = _distanz(kaeufer, verkaeufer)` und `sperrgold_import = min(importiert, _import_anteil(goldbestand, importiert, gold))`.  
- `verbrauchen`: `genutzt = _import_anteil(v, importiert, m)`.

Sonderfälle:  
- `frachtkanal != "vorraete"` bleibt beim Aufrufer.  
- `lager == 0` liefert 0, wie bisher.  
- Die Formeln sind heute wirklich identisch; die Deckungsprüfung stellt sicher, dass `menge <= lager`.

### 4. Was du NICHT anfassen würdest

- **Beuteverteilung in `kampfbericht.beute` vs. `beute_staffel`:** Die eigentliche Verteilungslogik ist nur ähnlich, nicht identisch. `beute` arbeitet alphabetisch und verschenkt durch Rundung eventuell Restplätze; `beute_staffel` füllt fair nach größtem Bestand auf. Eine Verschmelzung würde Zahlen verändern. Nur gemeinsame Kapazitäts- und Vorratsfilter herausziehen.  
- **`spieloekonomie.buchen` nicht als Ersatz für `spieldaten_anwenden`:** `buchen` wirft bei negativem Bestand eine Exception, die `spieldaten_anwenden`-Varianten kappen still mit `max(0, ...)`. Das sind verschiedene Regeln.  
- **Oberflächencode `_render_*` und `_build_main_ui`:** Pixel- und Anzeigeverhalten darf nicht durch Refactoring brechen.  
- **Feldnamen und Vertragsstrukturen** wie `fremdvertrag`, `wall_zustand_prozent`, `abgeliefert`, `angewendet` unverändert lassen.  
- **`auftraege.kosten_der_mission` nicht mit anderen Kostenmodulen mischen:** Die Sätze sind ausdrücklich VORSCHLAG und bewusst offen; eine zentrale Kostenfunktion würde Scheingenauigkeit erzeugen.

### 5. Ordnung

Saubere Struktur für diesen Teil:

- `src/hilfen.py`  
  Enthält nur reine Helfer: `als_zahl`, `als_int`, `aufzaehlung`, `positive_ganze_werte`, optional `bestand_erhoehen_gekappt`/`bestand_abziehen_gekappt`.  
  Keine Spiel-Imports, damit keine Zyklen entstehen.

- `src/einheiten.py`  
  Erhält `ladung_der_gruppe(bestand)` zusätzlich zu `kapazitaet`.

- `src/auftraege.py`  
  Nutzt `hilfen`, `einheiten.ladung_der_gruppe` und bekommt private `_reise_zeiten`.  
  `ladung_der_mission` bleibt als schmale öffentliche Wrapper-Funktion erhalten.

- `src/kampfbericht.py`  
  Nutzt `hilfen`, `einheiten.ladung_der_gruppe`.  
  Die zwei Beutefunktionen bleiben getrennt, verwenden aber gemeinsame Ladungs- und Vorratsfilter.

- `src/spieloekonomie.py`  
  Private `_distanz` und `_import_anteil`; Transport/Handel/Verbrauch rufen diese auf.  
  Zusätzlich kann `hilfen.als_int` verwendet werden.

- `src/werkstatt.py`  
  `_stufe_wert` wird `max(1, hilfen.als_int(stufe, 1))`; `lager_text` kann `hilfen.aufzaehlung` nutzen, falls das Verhalten exakt passt.

Reihenfolge des Umzugs ohne Importbruch:

1. `src/hilfen.py` neu anlegen und direkt mit einem kleinen Test prüfen.  
2. `auftraege.py` und `kampfbericht.py` auf `hilfen` umstellen; `tests/test_auftraege.py`, `tests/test_kampfbericht.py` grün halten.  
3. `einheiten.ladung_der_gruppe` ergänzen, dann `auftraege.ladung_der_mission` als Wrapper umbauen und die Kapazitätsschleifen in `kampfbericht` ersetzen.  
4. `auftraege._reise_zeiten` einführen und in `starten`/`_status_zeiten` verwenden.  
5. `spieloekonomie._distanz` und `_import_anteil` refaktorieren; alle Transport- und Handelsprüfungen grün halten.  
6. `werkstatt._stufe_wert` auf `hilfen.als_int` stützen.

Diese Reihenfolge verhindert zirkuläre Abhängigkeiten: `hilfen` hat keine Projekt-Imports, `einheiten` darf `hilfen` importieren, `auftraege` und `kampfbericht` importieren `einheiten` und `hilfen`, `spieloekonomie` importiert weiterhin `auftraege`, `werkstatt` importiert `hilfen`.