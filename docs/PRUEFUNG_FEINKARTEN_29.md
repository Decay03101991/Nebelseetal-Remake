# Pruefung der Feinkarten-Module (Schritt 29, Commit 306a89d)

**Geprueft von:** Unteragent (zweiter Blick), unabhaengig vom Koordinator.
**Wann geprueft:** 05.10.2026, `date` = `Mo, 5. Okt 2026 14:17:14`.
**Was geprueft wurde:** ob Commit `306a89d` (HEAD) die zwei Feinkarten-Module
`src/karten_optik_fein.py` und `src/welt_optik_fein.py` wirklich in `src/main.py`
eingehaengt hat und ob die Modulzahlen mit `docs/audits/ux_astra_karten_feinheit_2026-10-05.txt`
uebereinstimmen.

**Was NICHT geprueft werden konnte (absichtlich ausgelassen):** Es wurde **kein Fenster**
geoeffnet, kein `tkinter.Tk()`, keine `mainloop`, die `.exe` nicht gestartet, `tools/build_exe.py`
nicht aufgerufen, der Sammellauf nicht gestartet und **keine Datei in `tests/` ausgefuehrt**
(der Koordinator baut parallel). Die Zahlen der Pruefdateien (57/0/0, 82/0/0, 84/0/0, 128/0/0)
konnten daher NICHT nachgemessen werden — sie stammen aus dem Protokoll, nicht aus eigenem Lauf.
Es wurde KEINE bestehende Datei geaendert, geloescht oder per git beschrieben. Neue Datei:
nur diese. Pruefskripte lagen ausserhalb des Projekts im Scratch-Ordner.

Vorgehen allgemein:
`git show --stat 306a89d` (liest nur), `grep`/`read_file` in `src/` und `docs/`, sowie zwei
eigene Skripte im Scratch-Ordner (`pruefe_feinkarten.py`, `pruefe_fallen.py`), beide nur mit
Standardbibliothek; sie importieren die Feinmodule (kein tkinter), nicht aber `main.py`.

Bestand: Commit `306a89dd870eb6…`, Autor Daniel, Datum `Mon Oct 5 14:14:39 2026 +0200`,
HEAD; `git show --stat` aendert `src/main.py` und importiert beide Feinmodule. **Der Commit ist
echt und ist HEAD.**

---

## 1. Zahlen des Gutachtens als Modulkonstanten

**Behauptung:** die Zahlen aus `ux_astra_karten_feinheit_2026-10-05.txt` stehen als Konstanten in
`src/karten_optik_fein.py` und `src/welt_optik_fein.py`.

**Vorgehen:** Ich habe die Zahlen aus der Gutachtendatei herausgeschrieben und in
`scratch/pruefe_feinkarten.py` gegen die Modulkonstanten gestellt
(`python C:/Users/saras/AppData/Local/hermes/cache/scratch/pruefe_feinkarten.py`). Ebenso pruefte
`scratch/pruefe_fallen.py` drei Faelle durch Ausfuehren der Plaene.

**Ergebnis (alle 62 Konstanten geprueft, jede mit Gutachten-Zeile):**

| Groesse | aus Gutachten | Modul | Quelle |
|---|---|---|---|
| Baubereich 44 x 46 | 44.0 / 46.0 | `BAU_BREITE` / `BAU_HOEHE` | Z21 |
| Hauptkoerper 30 x 22 | 30.0 / 22.0 | `KOERPER_BREITE` / `KOERPER_HOEHE` | Z21 |
| Dach 38 x 16 | 38.0 / 16.0 | `DACH_BREITE` / `DACH_HOEHE` | Z21 |
| Sockel 36 x 5 | 36.0 / 5.0 | `SOCKEL_BREITE` / `SOCKEL_HOEHE` | Z21 |
| Tuer 6 x 10 | 6.0 / 10.0 | `TUER_BREITE` / `TUER_HOEHE` | Z21 |
| Fenster 4 x 5 | 4.0 / 5.0 | `FENSTER_BREITE` / `FENSTER_HOEHE` | Z21 |
| Farben #875241 / #59382F / #C0AD86 / #8F795C | gleich | `DACH_HELL` / `DACH_DUNKEL` / `WAND_HELL` / `WAND_DUNKEL` | Z21 |
| Gelaende #74805A / #455E43 / #77776C / #416875 | gleich | `EBENE_FARBE` / `WALD_FARBE` / `GEBIRGE_FARBE` / `WASSER_FARBE` | Z27 |
| Ufer #999071, 3–5 px | #999071 / 3.0 / 5.0 | `UFER_FARBE` / `UFER_BREITE_MIN` / `UFER_BREITE_MAX` | Z29 |
| Weg #75674F 8 px, Innen #A28E69 4 px | gleich | `WEG_FARBE` / `WEG_BREITE` / `WEG_INNEN_FARBE` / `WEG_INNEN_BREITE` | Z30 |
| Auswahl #172128 5 px + #E4C77D 2 px + vier 8-px-Winkel | gleich | `AUSWAHL_UNTER_FARBE` / `AUSWAHL_UNTER_BREITE` / `AUSWAHL_GOLD` / `AUSWAHL_GOLD_BREITE` / `AUSWAHL_ECKEN_LAENGE` | Z35 |
| Pips 4 x 4 px, 2 px Abstand | 4.0 / 2.0 | `PIP_KANTE` / `PIP_ABSTAND` | Z36 |
| Leiste 18 px | 18.0 | `KOORDINATEN_BREITE` | Z36 |
| Welt #707B58 / #405A43 / #75766F / #405F70 | gleich | `WELT1_EBENE` / `WELT1_WALD` / `WELT1_GEBIRGE` / `WELT1_WASSER` | Z42 |
| Raster #38433C 1 px | #38433C / 1 | `WELT1_RASTER` / `WELT1_RASTER_BREITE` | Z42 |
| Lichtfarben #637451 / #96958A / #658594 | gleich | `WELT1_LICHT_GRUEN` / `WELT1_LICHT_GEBIRGE` / `WELT1_LICHT_WASSER` | Z43 |
| Ufer #938A70 2–3 px | #938A70 / 2 / 3 | `WELT1_UFER` / `WELT1_UFER_MIN` / `WELT1_UFER_MAX` | Z44 |
| Ortsfarben #B9A582 / #81503F / #969083 / #292B27 | gleich | `WELT2_WAND` / `WELT2_DACH` / `WELT2_RUINE` / `WELT2_KONTUR` | Z49 |
| Fahne #356D98 / #D8D3BD / #F2EEDB | gleich | `WELT2_SOCKEL` / `WELT2_MAST` / `WELT2_FAHNE` | Z50 |
| Regionen #D7CEB4 mit #26312B | gleich | `WELT2_REGION_FARBE` / `WELT2_REGION_SCHATTEN` | Z51 |
| Uebersicht 4 x 4 px | 4 | `WELT3_UEBERSICHT_KACHEL` | Z57 |
| Panel 248 / 12 / 14 / 18 | 248 / 12 / 14 / 18 | `PANEL_BREITE` / `PANEL_INNENABSTAND` / `PANEL_SCHRIFT` / `PANEL_TITEL` | Z58 |

Ausgabe des Skripts: `=== ABWEICHUNGEN: 0`.

**Abweichung: nein.** (Anmerkung, keine Abweichung: die dunkle Unterkontur der WELT-Auswahl
steht im Gutachten ohne Hexwert; `welt_optik_fein` setzt `WELT3_AUSWAHL_DUNKEL = "#17212B"` und
vermerkt selbst, dass die Siedlung `#172128` nennt — eine Ableitung, kein Widerspruch zur Quelle.
Ebenso ist `KOORDINATEN_TEXT = "#EEE2CA"` die Panel-Textfarbe aus „Siedlung 3".)

---

## 2. Ruft `src/main.py` die Feinkarten-Funktionen wirklich auf?

**Behauptung:** `main.py` ruft die Funktionen der beiden Feinmodule auf.

**Vorgehen:** `grep -n "karten_optik_fein\.\|welt_optik_fein\." src/main.py` und `read_file`
der Fundstellen.

**Ergebnis (jede einzeln):**

| Funktion | Zeile(n) in `src/main.py` | Befund |
|---|---|---|
| `karten_optik_fein.gelaende_plan_fein` | 1985 | gefunden |
| `karten_optik_fein.wegabschnitt_plan` | 2009 | gefunden |
| `karten_optik_fein.auswahl_plan_fein` | 2031 | gefunden |
| `karten_optik_fein.gebaeude_baukasten_plan` | 2022 | gefunden |
| `karten_optik_fein.koordinatenleiste_plan` | 2037 | gefunden |
| `welt_optik_fein.gelaende_plan_fein` | 2931 | gefunden |
| `welt_optik_fein.ortsilhouette_plan` | 2958, 2963 | gefunden |
| `welt_optik_fein.fahne_plan_fein` | 2976 | gefunden |
| `welt_optik_fein.auswahl_plan_fein` | 2984 | gefunden |
| `welt_optik_fein.regionen_plan_fein` | 2943 | gefunden |
| `welt_optik_fein.uebersicht_plan_fein` | 2580 | gefunden |
| `welt_optik_fein.detail_masse` | 2715, 2830 | gefunden |

Zusaetzlich: `main.py` importiert beide Module (Zeilen 48/49) und liest Konstanten daraus
(`karten_optik_fein.KOORDINATEN_BREITE` Z1943, `welt_optik_fein.WELT3_UEBERSICHT_KACHEL`
Z2556, `WELT3_SICHT_RAHMEN`/`WELT3_SICHT_RAHMEN_BREITE` Z2583/2584).

**Abweichung: nein.** Alle zwoelf genannten Funktionen sind wirklich aufgerufen.

---

## 3. Die drei Einhänge-Fallen aus PROJEKT_STAND 0c

**Behauptung (Protokoll/Commit):** (a) Steppe/Huegel/Sumpf-Farben kommen aus `gelaende.farbe()`;
(b) `#637451` bleibt Lichtfarbe fuer Ebene UND Wald; (c) `spalten`/`zeilen` kommen vom Aufrufer,
nicht im Modul festgelegt.

**Vorgehen:** `grep` in `PROJEKT_STAND.md` (Abschnitt 0c, Z93–99), `read_file` der Module und
`python scratch/pruefe_fallen.py` (importiert `gelaende` und beide Feinmodule).

**Ergebnis:**
- (a) `karten_optik_fein._flaeche_farbe()` liefert fuer `grasland`/`wald`/`berg`/`nebelsee` die
  astra-Farben, sonst `_G.farbe(art)`. Lauf: `steppe` `#8C7A4A` = `gelaende.farbe("steppe")`,
  `huegel` `#6E5A3C` = … , `sumpf` `#3A3A2A` = … — **dreimal GLEICH**. Die drei Gelaendearten
  bekommen ihre Farbe also wirklich aus `gelaende.farbe()`.
- (b) Lauf bei `zelle=48`: `_ebene_fein` (plains) liefert Farbe `{#637451}`; `_wald_fein`
  (forest) liefert `{#637451, #405A43}`. **`#637451` steckt in Ebene UND Wald.** `offene_luecken()`
  dokumentiert die drei-Lichtfarben-fuer-vier-Arten-Annahme. Wie behauptet **nicht** getrennt.
- (c) `inspect.signature(karten_optik_fein.koordinatenleiste_plan)` = `spalten, zeilen, zelle,
  rand, spaltennamen, zeilennamen`; es gibt **keine** Modulkonstanten `SPALTEN`/`ZEILEN`. Aufruf
  `main.py` Z1938/1939: `spalten = karte.get("spalten") or 8`, `zeilen = karte.get("zeilen") or 5`
  und Uebergabe an die Leiste. Weltseitig `regionen_plan_fein(gitter, …)`,
  `uebersicht_plan_fein(tiles, kante, gitter, …)`. Probe: 8x5 -> 18 Befehle, 8x7 -> 20 Befehle.

**Abweichung: nein.** Die drei Behauptungen stimmen mit dem Code ueberein.

---

## 4. Zweite Wahrheiten / toter Code: alte Plan-Funktionen

**Behauptung (still mitgeprueft):** die alten Fassungen (u. a. `karten_optik.emblem_plan` /
`gebaeude_plan` / `wege_plan`, `welt_optik.gelaende_plan` / `fahne_plan` / `auswahl_plan` /
`uebersicht_plan`) werden in `main.py` nicht mehr benutzt.

**Vorgehen:** `grep -rn "karten_optik\.emblem_plan\|… " --include=*.py .` und
`grep -rn "emblem_plan(\|gebaeude_plan(\|… " --include=*.py .` ueber das ganze Projekt.

**Ergebnis:**
- In `src/main.py` wird **keine** dieser alten Plan-Funktionen aufgerufen. Aus den alten Modulen
  nutzt `main.py` nur noch `karten_optik.zeichne` (Z1983/2007/2020/2030/2035) und
  `welt_optik.zeichne` (Z2580/2936/2938/2944/2946/2957/2962/2975/2983) — den **Renderer**.
- Die alten Bauplan-Funktionen sind aber **nicht voellig tot**: sie werden weiterhin in den alten
  Pruefdateien `tests/test_karten_optik.py` (`emblem_plan`, `gebaeude_plan`, `wege_plan`,
  `raster_plan`) und `tests/test_welt_optik.py` (`gelaende_plan`, `fahne_plan`, `auswahl_plan`,
  `regionen_plan`, `uebersicht_plan`, `ortszeichen_plan`) aufgerufen.
- Einziger Treffer ausserhalb der Definitionen/alter Tests ist ein **Docstring-Verweis** in
  `karten_optik_fein.py` Z616 („feinere Fassung von `karten_optik.emblem_plan`") — kein Aufruf.

**Ehrlicher Befund:** Aus Anwendungssicht (`main.py`) sind die alten Plan-Bauer jetzt **toter
Code** (nur noch durch die alten Testdateien lebendig gehalten). Das ist ein Hinweis, **kein
Fehler** — nichts wurde geaendert oder geloescht.

**Abweichung: nein** zur Behauptung, dass `main.py` sie nicht mehr benutzt.

---

## 5. Genau EIN Objekt mit Tag 'weltfeld' je Feld (400)

**Behauptung:** je Weltfeld traegt genau ein Objekt das Tag `weltfeld`; die Pruefung
`tests/test_weltkarte.py` erwartet 400.

**Vorgehen:** `read_file` der Welt-Zeichenschleife in `main.py` (Z2895–2990) und von
`tests/test_weltkarte.py` (Z90–97, Z341–345) sowie der Rueckgabe von
`welt_optik_fein.gelaende_plan_fein`.

**Ergebnis:**
- `main.py` Z2922: Schleife `for tile in self.state.map_tiles` (400 Felder, 20x20 — Test Z91).
- Z2936: `welt_optik.zeichne(canvas, plan[:1], tags=(feldtag, "weltfeld"))` — **nur das erste**
  Planelement (die Gelaendeflaeche) traegt `weltfeld`.
- Z2937/2938: `welt_optik.zeichne(canvas, plan[1:], tags=(feldtag,))` — der Rest traegt `weltfeld`
  **nicht**.
- `welt_optik_fein.gelaende_plan_fein` liefert garantiert mindestens ein Element: der erste
  Eintrag ist immer das Fuell-Rechteck der Gelaendeflaeche (Z269–273); `plan[:1]` ist also nie leer
  und nie mehr als eins. Regionen (`weltregion`/`weltschatten`/`weltname`), Orte (`weltort`
  usw.), Fahne (`welthier`), Auswahl (`welt_auswahl`), Start (`weltstart`) und Vorkommen
  (`weltvorkommen`) tragen `weltfeld` nicht.

**Testmassstab:** `tests/test_weltkarte.py` Z96/97 `find_withtag("weltfeld") == 400` und Z344/345
dieselbe Zahl. Damit ergibt sich: 400 Felder x genau 1 Objekt = 400. Ich habe die Testdatei nur
**gelesen**, nicht ausgefuehrt.

**Abweichung: nein.** Der Code garantiert genau ein `weltfeld`-Objekt je Feld.

---

## 6. Eigener Kopf: die Zahl 2640 im Entwicklungsprotokoll

**Behauptung:** „Sammellauf 2640 bestanden, 0 Fehler, 21 Befunde ueber 41 Dateien" steht so im
Protokoll.

**Vorgehen:** `grep -n "2640\|21 Befunde\|41 Dateien" docs/ENTWICKLUNGSPROTOKOLL.md`.

**Ergebnis:** Zeile 111, Schritteintrag `14:13 · 29 · Die zwei Feinkarten-Module eingehängt …`,
enthaelt woertlich: „**Sammellauf 2640 bestanden, 0 Fehler, 21 Befunde über 41 Dateien**".

**Abweichung: nein.** Die Zeile steht so in `docs/ENTWICKLUNGSPROTOKOLL.md`. (Das ist die
Protokollzeile selbst — die Zahl wurde NICHT nachgemessen, der Sammellauf lief nicht.)

---

## Abweichungen

**keine Abweichung gefunden.**

Alle geprueften Aussagen des Koordinators stimmen mit dem Code und der Gutachtendatei ueberein:
Commit `306a89d` ist HEAD und haengt die zwei Feinmodule in `main.py` ein; alle zwoelf genannten
Funktionen sind aufgerufen; die Zahlen des Gutachtens stehen ohne Abweichung als Konstanten; die
drei Einhänge-Fallen sind wie beschrieben abgearbeitet; je Weltfeld traegt genau ein Objekt
`weltfeld`; die 2640-Zeile steht im Protokoll.

## Nicht geprueft (und nicht endgueltig auszuschliessen)

- **Kein Fenster/keine Anzeige:** es wurde nicht gesehen, ob die Karten auf dem Bildschirm
  tatsaechlich so aussehen. Geprueft wurde der Code und die erzeugten Plandaten, nicht das Bild.
- **Kein Sammellauf, keine `tests/`-Datei:** die im Commit/Protokoll genannten Zahlen
  (`test_kartenansicht` 57/0/0, `test_weltkarte` 82/0/0, `test_startspiel` 46/0/0,
  `test_karten_optik_fein` 84/0/0, `test_welt_optik_fein` 128/0/0, Sammellauf 2640/0/21/41)
  konnten nicht nachgerechnet werden; sie stammen aus dem Protokoll.
- **`.exe` nicht gestartet und `tools/build_exe.py` nicht aufgerufen:** die Aussage, dass die
  `.exe` die Feinmodule enthaelt, ist nicht gegengeprueft.
- **Laufzeitverhalten von `main.py`:** `main.py` wurde aus den harten Auflagen **nicht
  importiert/ausgefuehrt** (es zieht tkinter und koennte ein Fenster bauen); die Aufrufe wurden
  durch Lesen/Grep belegt, nicht durch Ausfuehren.
- **Toter Code (Punkt 4):** dass `main.py` die alten Funktionen nicht mehr aufruft, ist belegt;
  ob sie absichtlich als Reserve behalten werden, ist eine Entscheidung, keine Messung — deshalb
  nur gemeldet, nicht geaendert.
- **Grafische Feinheiten** (z. B. ob Ufer-/Rasterlinien bei Ueberzeichnung um die halbe
  Strichbreite ueber die Zelle hinausreichen, was `welt_optik_fein.offene_luecken()` selbst
  nennt) sind ohne Anzeige nicht beurteilbar.
