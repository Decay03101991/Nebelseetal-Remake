## 1. Befund in fünf Sätzen

1. Die vier Dateien bilden zwei parallel gewachsene Optik-Generationen für Welt und Siedlung: `welt_optik.py` (600 Z.) und `karten_optik.py` (599 Z.) als grobe Fassung, `welt_optik_fein.py` (898 Z.) und `karten_optik_fein.py` (863 Z.) als feine, aber nicht ersetzende Fassung.
2. Gemeinsames Gerüst sind das identische Plan-Dict-Format, der identische Renderer `zeichne` mit Helfer `_fuell` (in `welt_optik.py` und `karten_optik.py` je ca. 55 Zeilen) sowie identische Geometriehelfer `_punkte`/`_box` (je ca. 15 Zeilen) und der identische Feldleser `_feld` (je 6 Zeilen), zusammen über 200 Zeilen reine Duplikate.
3. Die fein-Module duplizieren zusätzlich Farbhelfer (`_aufhellen` in `welt_optik_fein.py` und `karten_optik_fein.py`), Skalierungslogik (`_skala` bzw. `zelle / 64.0`) und teils die Struktur der Planfunktionen für Regionen, Übersicht, Auswahl und Fahne.
4. Es gibt keinen gemeinsamen Import- oder Basisbaustein; jede Datei definiert eigene Konstanten und Helfer, obwohl viele identisch oder nur durch wenige Parameter (Detailstufe, Stil) unterschieden sind.
5. Da alle vier Dateien eigene Tests besitzen, kann keine Datei ohne Aufruferprüfung entfallen; die Zusammenführung muss zuerst gemeinsame Bausteine extrahieren, um Pixelverhalten unverändert zu lassen.

## 2. Vorschläge (Tabelle, absteigend nach Nutzen)

| # | Was | Dateien/Funktionen | Zeilen vorher → nachher | Risiko (klein/mittel/groß) | Beweis: welche Prüfdatei | Reihenfolge |
|---|---|---|---|---|---|---|
| 1 | Gemeinsamen Renderer extrahieren: `zeichne`, `_fuell`, `FORMEN` aus `welt_optik.py` und `karten_optik.py` in neues Modul `src/plan_renderer.py`; alte Module importieren nur noch | `welt_optik.py`, `karten_optik.py` – `zeichne`, `_fuell`, `FORMEN` | ~110 → ~60 (geschätzt) | klein | `tests/test_welt_optik.py`, `tests/test_karten_optik.py` | 1 |
| 2 | Gemeinsame Geometrie-/Farbhelfer extrahieren: `_punkte`, `_box`, `_feld`, `_p`, `_skala`, `_aufhellen`, `_abdunkeln`, `_rgb`, `_hex` in `src/plan_helfer.py`; vier Dateien importieren | `welt_optik.py`, `karten_optik.py`, `welt_optik_fein.py`, `karten_optik_fein.py` – private Helfer | ~180 → ~100 (geschätzt) | klein | `tests/test_welt_optik.py`, `tests/test_karten_optik.py`, `tests/test_welt_optik_fein.py`, `tests/test_karten_optik_fein.py` | 2 |
| 3 | Grobe und feine Planfunktionen pro Karte über gemeinsame interne Kernfunktionen mit Stilparameter zusammenführen (Regionen, Übersicht, Auswahl, Fahne) | `welt_optik.py`/`welt_optik_fein.py` und `karten_optik.py`/`karten_optik_fein.py` – `regionen_plan`, `uebersicht_plan`, `auswahl_plan`, `fahne_plan` | ~200 → ~100 (geschätzt) | mittel | `tests/test_welt_optik.py`, `tests/test_welt_optik_fein.py`, `tests/test_karten_optik.py`, `tests/test_karten_optik_fein.py` | 3 |
| 4 | Alte grobe Dateien entfernen, falls keine Aufrufer mehr existieren (nach Aufruferprüfung) | `welt_optik.py`, `karten_optik.py` komplett | 1.199 → 0 (geschätzt) | groß | Grep nach Aufrufern; `tests/test_welt_optik.py`/`test_karten_optik.py` müssten entfallen/angepasst werden | 4 |
| 5 | Gemeinsame Konstanten `FORMEN`, `KARTEN_HINTERGRUND` (identisch in `welt_optik.py`, `karten_optik.py`) in `src/plan_basis.py` ablegen | `welt_optik.py`, `karten_optik.py` – Konstanten | ~10 → ~5 (geschätzt) | klein | `tests/test_welt_optik.py`, `tests/test_karten_optik.py` | 5 |

## 3. Zusammenführung im Detail

### Vorschlag 1: Gemeinsamer Renderer (`zeichne`/`_fuell`)

**Neue Datei:** `src/plan_renderer.py`  
**Enthaltene Funktionen:**
```python
def zeichne(canvas, plan: list[dict], tags: tuple = ()) -> int:
def _fuell(eintrag: dict) -> dict:
```
**Parameter:** `canvas` (Duck-Typing mit tkinter-`create_*`-Methoden), `plan` (Liste der Planeinträge), `tags` (optional, wird an jedes Objekt weitergereicht).  
**Rückgabewert:** Anzahl der gezeichneten Objekte (`int`).  
**Kern:**  
- Jeder Eintrag wird anhand `form` genau einem `create_polygon`/`create_rectangle`/`create_oval`/`create_line`/`create_text`/`create_arc` zugeordnet.  
- `_fuell` übersetzt `farbe` → `fill`, `rand` → `outline`, `breite` → `width`.  
- Für `line` wird `glatt` als `smooth=True` übergeben; für `arc` werden `winkel`/`weite`/`stil` als `start`/`extent`/`style` übernommen; für `text` werden `farbe`, `text`, `font`, `anker` verarbeitet.  
**Sonderfälle:** Unbekannte `form` wirft `ValueError` wie bisher.  
**Einbindung:** In `welt_optik.py` und `karten_optik.py` wird die lokale Definition entfernt und stattdessen `from plan_renderer import zeichne` gesetzt – so bleiben `welt_optik.zeichne` und `karten_optik.zeichne` als Attributnamen erhalten.

### Vorschlag 2: Gemeinsame Geometrie-/Farbhelfer

**Neue Datei:** `src/plan_helfer.py`  
**Enthaltene Funktionen:**
```python
def punkte(x0, y0, zelle, *paare) -> list[float]:
def box(x0, y0, zelle, u1, v1, u2, v2) -> list[float]:
def punkt(x0, y0, zelle, u, v) -> list[float]:
def skala(zelle, mass_px=48.0) -> float:
def aufhellen(farbe, faktor) -> str:
def abdunkeln(farbe, faktor) -> str:
def rgb(farbe) -> list[int]:
def hex(rgb) -> str:
def feld_wert(tile, name, standard=None):
```
**Parameter:** Koordinaten/Ursprung, Zellgröße, relative Koordinaten, Farbwert, Faktor; `skala` erhält einen zusätzlichen Parameter `mass_px`, damit `welt_optik_fein` (48) und `karten_optik_fein` (64) denselben Helfer nutzen.  
**Rückgabewerte:** Flache Listen, Hex-Strings, Zahlen, Feldwert (identisch zu bisherigen privaten Helfern).  
**Kern:**  
- `punkte`/`box`/`punkt` rechnen relative Zellkoordinaten in absolute Leinwandkoordinaten um.  
- `aufhellen`/`abdunkeln` verändern einen Hex-Farbwert deterministisch in Richtung Weiß/Schwarz.  
- `feld_wert` liest Werte aus dict- oder objektförmigen Feldeinträgen.  
**Sonderfälle:** Die Alias-Normalisierung (`_norm_art` vs. `_normal`) wird **nicht** vereinheitlicht, weil Welt zu `water` und Siedlung zu `nebelsee` normalisiert; das bleibt in den jeweiligen Modulen.  
**Einbindung:** Die vier Dateien importieren die benötigten Helfer und binden sie unter den bisherigen privaten Namen ein, z. B. `_punkte = plan_helfer.punkte` – die öffentliche API und die erzeugten Pläne bleiben unverändert.

## 4. Was du NICHT anfassen würdest

- **Die konkreten Planfunktionen** (`gelaende_plan`, `emblem_plan`, `gebaeude_plan`, `ortsilhouette_plan`, `fahne_plan`, `auswahl_plan`, `regionen_plan`, `uebersicht_plan` usw.) mit ihren exakten Koordinaten, Farbwerten und Formreihenfolgen – die Tests prüfen diese Ausgaben pixelgenau; jede Änderung wäre sichtbar.  
- **Die aus Quellen abgeleiteten Farbkonstanten und Ableitungsfaktoren** (z. B. `LICHT_ABLEITUNG_FAKTOR = 0.