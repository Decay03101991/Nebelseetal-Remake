# Code lesbar halten — die Hausregel

**Warum:** Daniel, 31.10.2026: „in den reinen Codes soll kurz beschrieben werden, was die einzelnen
Codes für Aufgaben erfüllen — damit es auch Anfänger verstehen, und in GitHub für andere
nachvollziehbar bleibt.“ Diese Datei hält die Regel fest und sagt, wie man den Fortschritt misst.

## Die vier Regeln

1. **Jede Datei beginnt mit einem Modul-Docstring**, der in ein bis drei Sätzen sagt: wozu ist die
   Datei da, wer ruft sie auf, was rechnet sie. (Stand 31.10.2026: **alle 49 Dateien** in `src/`
   haben einen.)
2. **Jede Funktion und Klasse hat einen Docstring** — eine Zeile genügt, wenn die Funktion klein ist:
   was tut sie, was gibt sie zurück, was tut sie ausdrücklich **nicht**.
   Beispiel:
   ```python
   def tempo_der_gruppe(bestand: Dict[str, int]) -> int:
       """Reisegeschwindigkeit einer Truppe = langsamste mitgefuehrte Einheit."""
   ```
3. **Abschnitte bekommen eine Trennzeile**, damit man beim Scrollen sieht, wo man ist:
   ```python
   # --------------------------------------------------------------- 3. Wallvorrunde
   ```
4. **Herkunft kennzeichnen**, wo eine Zahl nicht aus einer Quelle stammt:
   `BELEGT` (mit Seite/Zeile) · `VORSCHLAG` (mit Begründung) · `ZUSAMMENFUEHRUNG` (Mechanik alt,
   Zahlen neu) · `VERWORFEN`. Das ist im Projekt keine Kosmetik, sondern die Grundlage des
   Prüfregisters (`docs/PRUEFREGEL_ORIGINAL.md`).

## Was NICHT verlangt ist

* Kein Kommentar vor jeder Zeile. `x = x + 1` erklärt sich selbst.
* Kein Roman. Ein Satz, der die Absicht nennt, ist mehr wert als zehn Zeilen Wiederholung.
* Keine englischen Kommentare in deutschem Code (das Projekt ist durchgehend deutsch).

## Wie man den Fortschritt misst

```bash
python -X utf8 tools/kommentar_luecken.py          # Übersicht je Datei
python -X utf8 tools/kommentar_luecken.py --liste  # jede Funktion ohne Docstring
```

Das Werkzeug zählt Zeilen, Kommentare, Docstring-Zeilen und sagt je Datei, wie viele Funktionen
noch ohne Beschreibung sind. Es ändert **nichts** — es zeigt nur, wo Arbeit liegt.

## Stand 31.10.2026 (gemessen, nicht geschätzt)

| Kennzahl | Wert |
|---|---|
| Dateien in `src/` | 49 |
| Funktionen/Klassen | 915 |
| **ohne Docstring** | **206 (22 %)** — vor der Aufräumrunde 267 (29 %) |
| ohne Modul-Docstring | 0 |

In dieser Runde ergänzt (jeweils geprüft, danach Tests grün):

| Datei | ergänzt | wofür die Datei da ist |
|---|---|---|
| `src/einheiten.py` | 13 | Brücke zu `data/units.json` — alle Werte (AT, PA, LE, SK, GS, Ladung, Punkte) an einer Stelle |
| `src/spieldaten.py` | 18 | Zugriff auf alle Stammdaten in `data/` (Einheiten, Waren, Forschungen, Rohstoffe, Gebäude, Wallstufen) |
| `src/berater.py` | 15 | Der Spielberater: beantwortet Fragen des Spielers aus den echten Daten |
| `src/zeitbasis.py` | 1 | Spieluhr: Faktor ×180, monotone Laufzeit, keine Systemzeit-Sprünge |
| `src/dorfwall.py` | 3 | Mauerzustand je Ort (Prozent), Zugriff auf Dict oder Objekt |
| `src/spielstaende.py` | 4 | Speicherslots 1–3, alter Einzelspielstand, Admin-Teststand |
| `src/kampf.py` | 7 | Kern des Kampfmodells: Aufstellung, aktive Einheiten, Fern-/Nahkampf, Forschungsstufe, Beutekapazität |

## Wo noch Arbeit liegt (bewusst liegen gelassen)

| Datei | offen | Einschätzung |
|---|---|---|
| `src/main.py` | 90 von 249 | Die Oberfläche. Viele Ein-Zeilen-Handler (`_on_...`, `_render_...`); sinnvoll ist hier eine Runde **dateiweise** (z. B. nur die Ausbildung-/Kampf-Ansichten), nicht am Stück |
| `src/kampf_alt_handbuch_2009.py` | 9 von 16 | Rückfallmodul, wird im Spiel nicht mehr benutzt; niedrige Priorität |
| `src/admin_oberflaeche.py` | 12 von 13 | Admin-Fenster, nur für die Verwaltung |

**Regel für die nächste Runde:** immer eine Datei vollständig, Docstrings aus dem **gelesenen** Code
schreiben (nicht aus dem Funktionsnamen raten), danach die Prüfdatei der Datei laufen lassen und den
Stand hier fortschreiben.
