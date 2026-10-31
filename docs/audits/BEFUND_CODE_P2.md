### 1. Befund in fünf Sätzen
Zwei vollständige Schlachtfunktionen existieren parallel: `kampf.py::fuehre_schlacht` (188 Zeilen, neues Forumsmodell mit 15 festen PROFILE, Forschungs-Boni) und `kampf_alt_handbuch_2009.py::fuehre_schlacht` (194 Zeilen, älteres Handbuchmodell mit LE/AT/PA). Beide liefern unterschiedliche Kampfergebnisse, z. B. zählt die alte Funktion bei der Wall-Vorprüfung Fernkämpfer zur „Fußtruppen”-Schwelle, die neue nur Nahkämpfer; der Nahkampf läuft in der alten als Mehrrunden-Zweikampf, in der neuen als einzelner Schlag pro Begegnung. Laut gezeigtem Code importiert `kampf.py` die alte Datei nicht, sondern erwähnt sie nur als „Rückfallsicherung”; trotzdem existieren beide Dateien mit insgesamt 799 Zeilen. Die neue `fuehre_schlacht` ist mit 188 Zeilen, sechs verschachtelten Schleifen und mehreren Ausgangsbedingungen zu lang und unübersichtlich, was Änderungen riskant macht. Ziel ist deshalb: die alte Datei entfernen (oder Aufrufer umstellen) und die verbleibende Funktion in klare Hilfsfunktionen zerlegen, ohne die Berechnungsreihenfolge zu verändern.

### 2. Vorschläge (Tabelle, absteigend nach Nutzen)

| # | Was | Dateien/Funktionen | Zeilen vorher → nachher | Risiko (klein/mittel/groß) | Beweis: welche Prüfdatei | Reihenfolge |
|---|---|---|---|---|---|---|
| 1 | `kampf_alt_handbuch_2009.py` ersatzlos entfernen und alle Aufrufer auf `kampf.fuehre_schlacht` umstellen | `src/kampf_alt_handbuch_2009.py` (komplett) | 401 → 0 (geschätzt) | mittel – falls doch noch externe Aufrufer existieren, brechen diese | `tests/test_kampf.py` (sofern vorhanden) muss grün bleiben; alte Tests für `kampf_alt_handbuch_2009` entfernen | 1 |
| 2 | Die neue `fuehre_schlacht` in fünf bis sieben private Hilfsfunktionen zerlegen (Wall-Vorprüfung, Fernkampf-Vorrunden, Nahkampf-Sequenzen, Ausgang, Beute/Geräte) | `src/kampf.py` – Funktion `fuehre_schlacht` und neue `_*`-Funktionen | Hauptfunktion 188 → ca. 60 (geschätzt); Hilfsfunktionen ca. 80–120 zusätzlich; Netto­ersparnis gering, aber Lesbarkeit deutlich besser | klein | `tests/test_kampf.py` muss unverändert grün bleiben | 2 |
| 3 | (Optional, nur falls alte Funktion vorerst bleiben muss) Gemeinsame Beute- und Geräteverlust­logik in eine gemeinsame Hilfsdatei extrahieren, um die Duplikate zu beseitigen | `src/kampf.py` `_beute` / `_sieggeraete`, `src/kampf_alt_handbuch_2009.py` `_geraeteverluste` | Duplikate ca. 40 Zeilen; nach Extraktion reduzierte Doppelung | mittel – wenn alte Funktion doch wieder aktiviert wird, muss Verhalten exakt identisch sein | `tests/test_kampf.py` (neu), `tests/test_kampf_alt_handbuch_2009.py` (falls vorhanden) | 3 |

### 3. Zusammenführung im Detail

**Vorschlag 1 – Alte Funktion entfernen und Aufrufer umstellen**  
Die alte `fuehre_schlacht` verschmilzt nicht mit der neuen, sondern wird gelöscht.  
Alle Stellen, die `kampf_alt_handbuch_2009.fuehre_schlacht` importieren oder aufrufen, werden auf `kampf.fuehre_schlacht` geändert.  
Signatur der verbleibenden Funktion bleibt unverändert:  
`fuehre_schlacht(angreifer: Dict[str, int], verteidiger: Dict[str, int], wall_stufe: int = 0, wall_zustand: float = 100.0, angreifer_karren: Optional[Dict[str, int]] = None, verteidiger_karren: Optional[Dict[str, int]] = None, vorraete: Optional[Dict[str, float]] = None, rng: Optional[random.Random] = None, forschung_angreifer: Optional[dict] = None, forschung_verteidiger: Optional[dict] = None) -> Dict[str, Any]`  
Kern:  
- Aufrufer, die keine Forschungs­parameter übergeben, erhalten `forschung_angreifer=None, forschung_verteidiger=None` – das verhindert fiktive Boni und erhält dessen Verhalten so weit wie möglich.  
- Sonderfall „Fernkämpfer zählen bei der Wall-Schwelle zur Fußtruppe” wird **nicht** übernommen; die neue Regel (nur Nahkampf) ist bewusst restriktiver und wird dokumentiert.  
- Falls eine alte Aufrufstelle zwingend das alte Verhalten benötigt, muss diese Stelle separat bewertet und ggf. ein Konfigurationsparameter eingeführt werden – das ist aber nicht Teil der Standard­zusammenführung.

**Vorschlag 2 – Neue `fuehre_schlacht` in Hilfsfunktionen zerlegen**  
Die Hauptfunktion wird in logische Blöcke zerlegt, die jeweils als private Funktionen in `kampf.py` verbleiben.  
Die Signatur von `fuehre_schlacht` bleibt exakt gleich; nur der Rumpf ruft nacheinander:  
`_init_ergebnis(...)` → `_pruefe_wallvoraussetzung(...)` → `_fuehre_fernkampfvorrunden(...)` → `_fuehre_nahkampfsequenzen(...)` → `_ermittle_ausgang(...)` → `_beute_und_geraete(...)` → `_fertig(...)`  
Jede Hilfsfunktion erhält die nötigen Objekte (Einheiten, Wallwerte, Forschung, rng, Protokoll) und gibt Teilergebnisse oder mutierte Zustände zurück.  
Sonderfälle wie „geschützte Nahkämpfer durch Belagerungstürme” und „Rückzugsquote der Fernkämpfer” bleiben in ihrer jeweiligen Hilfsfunktion, die exakt dieselbe Berechnung wie bisher durchführt.  
Rückgabewert bleibt das Ergebnis-Dict mit allen bisherigen Schlüsseln; keine neuen Schlüssel werden eingeführt.

### 4. Was du NICHT anfassen würdest

- **PROFILE-Werte und Wall-Schwellen** (`PROFILE` in `kampf.py`, `spieldaten.wallstufen()`): Änderungen würden die Spielbalance und alle gespeicherten Kampfergebnisse verändern.  
- **Reihenfolge der `rng`-Aufrufe**: Jede Umstellung der Zufalls­reihenfolge macht reproduzierbare Tests (mit festem `rng`) sofort rot und verändert unvorhersehbar die Spielergebnisse.  
- **Ausgabeschlüssel des Ergebnis-Dicts** (`ausgang`, `verluste_*`, `mauer_zustand`, `beute`, `unsicher`): Das UI und die Speicher­logik verlassen sich auf diese Namen; ein Umbenennen wäre eine unnötige Bruch­stelle.  
- **ASCII-Kommentar­konvention**: Die vorhandenen ASCII-Kommentare in `kampf.py` bleiben unangetastet, auch wenn die Antwort hier Umlaute verwendet.  

### 5. Ordnung

**Zieldateistruktur für den Kampfteil:**  
- `src/kampf.py` – enthält die einzige `fuehre_schlacht`, `PROFILE`, und alle Hilfsfunktionen.  
- `tests/test_kampf.py` – Tests für die neue Schlachtfunktion.  
- `src/kampf_alt_handbuch_2009.py` wird gelöscht.  

**Reihenfolge des Umzugs ohne Import­brüche:**  
1. **Aufrufer identifizieren**: Mit `grep -r "kampf_alt_handbuch_2009" src tests` alle Importe/Aufrufe finden.  
2. **Aufrufe umstellen**: Jede Aufrufstelle auf `from kampf import fuehre_schlacht` ändern; Parameter `forschung_*` als `None` übergeben, falls nicht vorhanden.  
3. **Tests anpassen**: Falls eine eigene Testdatei für die alte Funktion existiert, wird sie entfernt oder auf die neue Funktion umgeschrieben.  
4. **Neue Funktion refaktorisieren** (Vorschlag 2): Erst nachdem alle Aufrufer auf die neue Funktion zeigen und die Tests grün sind, wird die lange Funktion zerlegt.  
5. **Alte Datei löschen**: Erst wenn keine Importe mehr darauf verweisen und der Sammellauf (`tools/sammellauf.py`) grün ist, wird `src/kampf_alt_handbuch_2009.py` entfernt.