# Plan: Siedlungskarten-Raster 8x5 (40 Felder) -> 8x7 (56 Felder, davon 40 bebaubar)

Stand: 05.10.2026. Dieses Dokument ist eine **Vorlage fuer den Koordinator**; es aendert
**keinen Code**. Jede Zahl hat eine Fundstelle (Datei + Zeile). Unsichere Punkte stehen als
`unklar` im letzten Abschnitt.

Grundlage der Aenderung: Daniels Entscheidung vom 05.10.2026, 14:24 (woertlich angekreuzt):
**8 Spalten x 7 Zeilen = 56 Felder, davon 40 bebaubar**. Die Frage war als "Frage 12" offen
(`docs/FRAGEN_FUER_MORGEN.md` Z. 43-47).

---

## 0. Entscheidung in Zahlen

| Groesse | Heute (Code) | Ziel |
|---|---|---|
| Spalten | 8 | 8 |
| Zeilen | 5 | 7 |
| Felder im Raster | 40 | 56 |
| bebaubare Felder | nicht getrennt gefuehrt | 40 |
| nicht bebaubare Felder | ergibt sich aus Sumpf | 16 |

Heute stehen `spalten`/`zeilen` in `data/gelaende.json` Z. 5-6 (**8** und **5**). Die Datei
nennt daneben bereits `bauplaetze: 40` (Z. 7) und `felder: 56` (Z. 9) — beide Werte werden vom
Code **nicht gelesen** (siehe 1.1). Damit ist der Widerspruch in der Datei schon vorhanden
(`docs/PROJEKT_STAND.md` Z. 250).

---

## 1. Bestandsaufnahme (gemessen)

### 1.1 Woher kommt das Mass, wer liest es?

| Fundstelle | Was steht dort | Wirkung |
|---|---|---|
| `data/gelaende.json` Z. 4-11 | `kartenmass`: `spalten: 8`, `zeilen: 5`, `bauplaetze: 40`, `felder: 56` | **einzige** Quelle der Rastermasse |
| `src/gelaende.py` Z. 192 | `mass = mass or _GELAENDE["kartenmass"]` | liest den Block als Vorgabe |
| `src/gelaende.py` Z. 194 | `spalten, zeilen = mass["spalten"], mass["zeilen"]` | liest **nur** diese zwei Schluessel |
| `src/gelaende.py` Z. 195 | `plaetze = spalten * zeilen` | Gesamtfelder = 8*5 = 40 |
| `src/gelaende.py` Z. 251 | `"bauplaetze": plaetze` | **Befund:** `bauplaetze` in der erzeugten Karte = Gesamtfelder, **nicht** "bebaubare Felder". Der JSON-Wert `bauplaetze: 40` und `felder: 56` werden ignoriert. |

`mass` wird nirgends sonst mit einem eigenen Wert aufgerufen (nur `gelaende.py` Z. 192; Aufrufer
`src/main.py` Z. 201, `src/spielschicht.py` Z. 162, Tests). Es gibt keinen zweiten Ort mit 8x5.

### 1.2 Wie wird eine Karte erzeugt?

`gelaende.siedlungskarte_erzeugen(seed, mass=None, typ_id=None)`, `src/gelaende.py` Z. 182-260:

| Schritt | Zeile |
|---|---|
| Saat + Gewichte des Kartentyps waehlen | Z. 191-198 |
| `plaetze = spalten * zeilen` Felder per Gewicht ziehen | Z. 195, 211 |
| Mindestbesatz erzwingen (wald 2, berg 2, grasland 3, nebelsee 1) | Z. 213-237, Regel Z. 139-145 |
| Sumpf auf `sumpf_hoechstens` (6) deckeln | Z. 240-243, Regel Z. 146 |
| Zeilenraster, Zaehlung, Profil bauen | Z. 245-259 |
| Rueckgabe | Z. 247-260 |

Rueckgabe-Schluessel der Karte: `seed`, `spalten`, `zeilen`, `bauplaetze`, `raster`,
`zeilen_raster`, `zaehlung`, `typ`, `typ_name`, `vorteil`, `beschreibung`, `profil`
(`src/gelaende.py` Z. 248-259).

### 1.3 "niemals zwei gleiche Karten" (Handbuch S. 313)

| Fundstelle | Was |
|---|---|
| `src/main.py` Z. 187-189 | `karten_signatur(karte) = "".join(karte["raster"])` — die Signatur ist die Aneinanderreihung aller Feldarten; Laenge = Feldzahl (heute 40). |
| `src/main.py` Z. 192-204 | `neue_siedlungskarte(vorhandene)`: bis zu `KARTENVERSUCHE = 400` (Z. 184) neue Karten ziehen; verwerfen, wenn Signatur schon vergeben (Z. 202); sonst `RuntimeError` (Z. 204). |
| `src/main.py` Z. 1735 | Aufruf beim Siedlung gruenden. |
| `src/main.py` Z. 1892 | Aufruf in `_karten_zuwaeisen` (nur fuer Siedlungen **ohne** Karte). |

Die Signaturpruefung kennt nur die eigene Siedlungsliste — ein Sig-Längenwechsel 40 -> 56 ist fuer
den Vergleich unkritisch, weil nur Karten desselben Formats direkt verglichen werden.

### 1.4 Wer liest `spalten` / `zeilen` zur Anzeige und Rechnung?

| Fundstelle | Was |
|---|---|
| `src/main.py` Z. 1938-1939 | `spalten = int(karte.get("spalten") or 8)`, `zeilen = int(karte.get("zeilen") or 5)` — **harte Fallbacks 8 und 5**. |
| `src/main.py` Z. 1944-1945 | Canvas-Groesse `rand + spalten*zelle` mal `rand + zeilen*zelle` (zelle = 64, rand = 18). |
| `src/main.py` Z. 1950-1965 | Feld-Ecke (`i % spalten`, `i // spalten`) und Nachbararten. |
| `src/main.py` Z. 1995-2003 | Wege zwischen bebauten Nachbarfeldern. |
| `src/main.py` Z. 2038-2040 | `koordinatenleiste_plan(spalten, zeilen, ...)` mit A-H und 1..N. |
| `src/main.py` Z. 2045-2049 | **Klickrechnung**: `spalte=(x-rand)//zelle`, `zeile=(y-rand)//zelle`, Feld = `zeile*spalten+spalte`. |
| `src/main.py` Z. 2119-2120 | Detailpanel: `_spalten = int(karte.get("spalten") or 8)`, Koordinate `A1`. |
| `src/karten_optik_fein.py` Z. 776 | `koordinatenleiste_plan(spalten, zeilen, zelle, rand, spaltennamen, zeilennamen)` — nimmt das Mass als Parameter. |
| `src/karten_optik_fein.py` Z. 614 | `gelaende_plan_fein(art, x0, y0, zelle, nachbarn)` — kennt kein Mass, nur eine Feldart. |

`src/karten_optik_fein.py` ist damit **groessenneutral**. Der Test dafuer arbeitet bereits mit
8x7: `tests/test_karten_optik_fein.py` Z. 326, 344-346, 356. Kein Modulumbau fuer die 7 Zeilen
noetig.

### 1.5 Was ist heute nicht bebaubar?

| Geländeart | `bebaubar` | Fundstelle |
|---|---|---|
| grasland, steppe, wald, huegel, berg | true | `data/gelaende.json` Z. 16, 25, 34, 43, 52 |
| nebelsee | **true** | `data/gelaende.json` Z. 61 (Tempel dort, Handbuch S. 10) |
| sumpf | **false** | `data/gelaende.json` Z. 70; Regel Z. 137; `src/gelaende.py` Z. 147-148 |

Belegt ist nur der Sumpf: "Suempfe sind unbebaubar" (`docs/original/Spielanleitung_2009_Textfassung.txt`
Z. 380-381). Der Nebelsee ist **bebaubar** — Bibliothek und Tempel stehen dort
(`...Textfassung.txt` Z. 403; `tests/test_gelaende.py` Z. 86-88).

> **Widerspruch zur Auftragsannahme (wichtig, nicht aufloesen, nur melden):** Der Auftrag nennt
> "Sumpf und Nebelsee sind nicht bebaubar". Daten und Handbuch sagen: nur Sumpf ist nicht
> bebaubar, der Nebelsee ist es. Fuer die Zaehlung "40 bebaubar" muss daher **vor** der Umsetzung
> entschieden werden, ob der Nebelsee zu den 40 zaehlt oder nicht (siehe Abschnitt 6). Der Plan
> rechnet im Folgenden mit der Datenlage: **Nebelsee zaehlt zu den bebaubaren Feldern** (sonst
> waere der Tempel nicht baubar).

Heute entstehen 40 Felder, von denen zufaellig 0..6 Sumpf sind — die Zahl der bebaubaren Felder
ist also **nicht fest**. Fuer "genau 40 bebaubar" muss der Erzeuger die Sperrfelder gezielt
setzen.

---

## 2. Die 16 nicht bebaubaren Felder — zwei Varianten (VORSCHLAG)

Gemeinsam: `data/gelaende.json` Z. 6 `zeilen` 5 -> 7, Gesamtfelder 56. Zusaetzlich muss eine
**neue Regel** dafuer sorgen, dass genau 16 Felder gesperrt sind. Heute deckelt nur
`sumpf_hoechstens: 6` (Z. 146) — das ergibt nie eine feste 16.

**Nichts von beidem ist belegt.** Die 56/40-Aufteilung ist Daniels Entscheidung (VORSCHLAG); das
Handbuch nennt keine Kartengroesse (`data/gelaende.json` Z. 8; `docs/audits/astra_karten.txt` Z. 30).

### Variante A — neue achte Art "wasser" (Wege/Wasser)  *(empfohlen)*

Anschlussfaehig an die bereits vorhandene Notiz in `data/gelaende.json` Z. 10: "die uebrigen sind
Wege/Wasser (VORSCHLAG)".

| Aenderung | Fundstelle |
|---|---|
| neue Geländeart `wasser` mit `bebaubar: false` | `data/gelaende.json` Z. 12-75 (neuer Eintrag) |
| `wasser` in alle fuenf Kartentyp-Gewichte aufnehmen | `data/gelaende.json` Z. 100, 108, 116, 124, 132 |
| neue Regel, z. B. `nicht_bebaubar: 16`; `sumpf_hoechstens` bleibt 6 | `data/gelaende.json` Z. 136-148 |
| Erzeuger: sumpf + wasser gemeinsam auf 16 bringen (sumpf 0..6, wasser fuellt auf) | `src/gelaende.py` Z. 240-243 (neue Stufe) |

- **Bebaubar (40):** grasland, steppe, wald, huegel, berg, nebelsee.
- **Gesperrt (16):** sumpf + wasser.
- **Folge fuer den Kartencharakter:** zusammenhaengende Wasser-/Wegbaender, Seen und Ufer; die
  Weglogik trennt Wasser bereits aus (`src/main.py` Z. 1975-1977 `_kein_wasser` kennt schon
  `"wasser"`). Der Zeichner behandelt `wasser` wie `nebelsee`
  (`src/karten_optik_fein.py` Z. 159-182 `_WASSER_ALIASE`, `_normal`), also **ohne** Modulumbau
  sichtbar — ein eigenes Wasserbild waere eine spaetere Aufgabe.
- **Nicht belegt / VORSCHLAG:** dass das Original Wasserfelder im Siedlungsraster hatte; die
  Verteilung sumpf/wasser; die 16.

### Variante B — nur Sumpf, Menge auf 16

| Aenderung | Fundstelle |
|---|---|
| `sumpf_hoechstens: 6` -> `16` (oder eine neue Regel "genau 16 Sumpf") | `data/gelaende.json` Z. 146 |
| Erzeuger: Sumpf gezielt auf 16 bringen | `src/gelaende.py` Z. 240-243 |

- **Bebaubar (40):** die uebrigen sechs Arten (inkl. Nebelsee).
- **Gesperrt (16):** sumpf.
- **Folge fuer den Kartencharakter:** viele tote Sumpfecken, eintoeniger; Sumpf traegt auch keine
  Wege. Dafuer **keine** neue Geländeart, keine Gewichts-, Profil- oder Zeichner-Aenderung.
- **Nicht belegt / VORSCHLAG:** die Zahl 16 (die Werte `haeufigkeit: 10`, Z. 71, und
  `sumpf_hoechstens: 6`, Z. 146, waren selbst nur Vorschlag). `sumpf_hoechstens` gilt ausserdem in
  `tests/test_gelaende.py` Z. 119, 171 als gepruefter Wert und muesste mitwandern.

**Empfehlung:** Variante A — sie passt zur vorhandenen Datennotiz "Wege/Wasser" und erhaelt ein
abwechslungsreiches Kartenbild. Variante B ist der kleinere Eingriff, aendert den Kartencharakter
aber stark und macht 16 Felder wertlos.

---

## 3. Was alles beruehrt wird (Checkliste mit Fundstelle)

| Datei | Ort | Zu tun | Grund |
|---|---|---|---|
| `data/gelaende.json` | Z. 6 | `zeilen` 5 -> 7 | Zielmass |
| `data/gelaende.json` | Z. 7, 9 | `bauplaetze`/`felder` bleiben 40/56, sind aber kuenftig Code-Wahrheit | heute ignoriert (`src/gelaende.py` Z. 194) |
| `data/gelaende.json` | Z. 12-75 | nur Variante A: Art `wasser` (`bebaubar: false`) ergaenzen | 16 Sperrfelder |
| `data/gelaende.json` | Z. 100, 108, 116, 124, 132 | nur Variante A: `wasser` in alle fuenf `gewichte` | sonst Fallback auf `haeufigkeit` (`src/gelaende.py` Z. 202, 206) |
| `data/gelaende.json` | Z. 146 | Variante A: neue 16-Regel, Sumpfdeckel bleibt; Variante B: Deckel 6 -> 16 | genau 16 Sperrfelder |
| `src/gelaende.py` | Z. 194-195, 245 | Mass 8x7 verarbeiten | erzeugt 56 Felder |
| `src/gelaende.py` | Z. 240-243 | Sperrfelder sumpf (+ wasser) auf 16 bringen | 40 bebaubar |
| `src/gelaende.py` | Z. 251-253 | **`bauplaetze` = Anzahl `bebaubar`-Felder; neuer Schluessel `felder` = Gesamt** | heute `bauplaetze` = Gesamt |
| `src/gelaende.py` | Z. 279-282 | nicht bebaubare Arten aus dem Profil ausschliessen (nicht nur `SUMPF`) | sonst ueberzaehlt `karte_profil` bei `wasser` |
| `src/gelaende.py` | Z. 312-313 | nur Variante A: Kuerzel fuer `wasser` in `karte_als_text` | sonst `KeyError` |
| `src/gelaende.py` | Z. 306-307 | Text "8x7 (40 Plaetze)" | `karte_beschreiben` |
| `src/main.py` | Z. 1938-1939 | Fallback `zeilen ... or 5` -> `or 7` | alte/halb gefuellte Karten |
| `src/main.py` | Z. 1944-1949, 2045-2049 | Zeichenflaeche/Klick: Masse kommen aus `karte`, nur Hoehe waechst | 7 Zeilen = 466 px hoch |
| `src/main.py` | Z. 2100-2103 | Legende laeuft ueber `GELAENDEARTEN` — `wasser` erscheint automatisch, Farbe muss in JSON stehen | Legende |
| `src/main.py` | Z. 2104, 2126 | Hinweistext um "und Wasser" ergaenzen (nur Variante A) | Anzeige |
| `src/main.py` | Z. 2119 | Fallback `or 8` bleibt (nur Spalten) | Detailpanel |
| `src/main.py` | Z. 1063-1103 / 1105-1178 | Speichern/Laden: Karte steckt als `dict` in `Settlement` (Z. 1075 / 1148) | **alte Staende behalten 40 Felder** |
| `src/karten_optik_fein.py` | Z. 776, 614 | keine Aenderung noetig (Parameter) | 8x7 bereits getestet |
| `tests/test_gelaende.py` | Z. 95-98, 131-134, 187 | 8x5/40 -> 8x7/56; Z. 187 `40*` -> `56*` | harte 40er-Annahmen |
| `tests/test_kartenansicht.py` | Z. 74 | "40 anklickbare Felder" -> 56 | harte 40 |
| `tests/test_durchspiel.py` | Z. 112-113 | "40 Felder" -> 56 | harte 40 |
| `tests/test_spielschicht.py` | Z. 108 | "40 Bauplaetze" -> 40 bebaubare / 56 Felder | harte 40 |
| `tests/test_startspiel.py` | Z. 222-223 | Fallback `or 8` -> `or 7` (nur Lesbarkeit) | Klickrechnung im Test |
| `tests/test_wirtschaft.py` | Z. 180-183 | Mana-Formel `bauplaetze - sumpf - nebelsee` neu ableiten | `bauplaetze`-Bedeutung aendert sich |
| `tests/test_karten_optik_fein.py` | Z. 326-361 | **nichts** | prueft schon 8x7 |
| `docs/audits/ux_astra_karten_feinheit_2026-10-05.txt` | Z. 36 | Quelle der 8x7-Annahme (VORSCHLAG), nicht aendern | Dokumentation |

Nicht betroffen: `src/welt_optik*.py`, `src/welt_optik_fein.py` (20x20-Weltkarte), `src/portalraum.py`
(20x20 Limbus) — anderes Raster.

---

## 4. Reihenfolge der Umsetzung (kleine, einzeln pruefbare Schritte)

Jeder Schritt nennt **genau einen** Test. `run_tests.bat` erst am Ende.

| # | Aenderung | Einzeltest |
|---|---|---|
| 1 | `data/gelaende.json` Z. 6: `zeilen` 5 -> 7. Sonst nichts. | `python tests\test_gelaende.py` — **muss jetzt rot sein** (Z. 96/97/98/131/133/134/187). Das dokumentiert die Abweichung, kein Fehler. |
| 2 | `tests/test_gelaende.py`: Z. 96 `5`->`7`, Z. 98 `40`->`56`, Z. 131 `"8x5"`->`"8x7"`, Z. 133 `5`->`7`, Z. 134 `8`->bleibt, Z. 187 `40*`->`56*`. | `python tests\test_gelaende.py` — gruen bis auf Z. 97 (`bauplaetze`, Schritt 3). |
| 3 | `src/gelaende.py`: `bauplaetze` = Anzahl `bebaubar`-Felder, neuer Karte-Schluessel `felder` = `spalten*zeilen`; `karte_beschreiben` (Z. 306-307) anpassen. Test Z. 97 auf `40`/`56` erweitern. | `python tests\test_gelaende.py` — gruen. |
| 4 | Sperrfelder fest auf 16 (Variante A oder B) in `src/gelaende.py` Z. 240-243 + Regel in `data/gelaende.json` Z. 136-148 (und bei A Art/Gewichte). Neue Pruefung in `test_gelaende.py`: `zaehlung[sumpf]+zaehlung[wasser]==16` und `bauplaetze==40` ueber viele Saaten. | `python tests\test_gelaende.py` — gruen, inkl. Mindestbesatz (Z. 111-122) und Vielfalt (Z. 124-127). |
| 5 | `src/gelaende.py`: `karte_profil` (Z. 279-282) schliesst **alle** nicht bebaubaren Arten aus; `karte_als_text` (Z. 312) um Kuerzel `wasser` ergaenzen (nur Variante A). | `python tests\test_gebaeude_wirkung.py` und `python tests\test_ertrag_anbindung.py` — gruen. |
| 6 | `tests/test_wirtschaft.py` Z. 180-183: Mana-Formel auf die neue `bauplaetze`-Bedeutung umstellen. | `python tests\test_wirtschaft.py` — gruen. |
| 7 | GUI-nahe Tests anpassen: `test_kartenansicht.py` Z. 74, `test_spielschicht.py` Z. 108, `test_durchspiel.py` Z. 112-113, `test_startspiel.py` Z. 222-223. | je einzeln: `python tests\test_kartenansicht.py`, `...test_spielschicht.py`, `...test_durchspiel.py`, `...test_startspiel.py`. |
| 8 | `src/main.py`: Z. 1939 Fallback `or 5`->`or 7`; Z. 2104/2126 Text ergaenzen (nur A). | `python tests\test_gui_fehler.py` und `python tests\test_startspiel.py` — gruen. |
| 9 | Speichern/Laden alter 40er-Karten pruefen (Abschnitt 5, Risiko 1); Entscheidung dokumentieren. | `python tests\test_speichern_robust.py` und `python tests\test_baseline.py` — gruen. |
| 10 | Gesamtlauf. | `run_tests.bat` — Rueckgabewert 0. |

Erst nach Schritt 10 `.exe` neu bauen (macht der Koordinator; nicht Teil dieses Plans).

---

## 5. Risiken und Fallen

1. **Alte Spielstaende.** Siedlungen speichern ihre Karte als `dict` mit (`src/main.py` Z. 1075
   `asdict(s)`; Laden Z. 1148 `Settlement(**s)`). Ein alter Stand hat **weiter 40 Felder**; es gibt
   keinen Umbau. Folgen: gemischte Kartenformate; `bauplaetze` im alten Stand = 40 (Gesamt), im neuen
   = 40 (bebaubar) — zufaellig gleich, aber unterschiedlich gemeint. `_karten_zuwaeisen` (Z. 1889)
   hilft nur Siedlungen **ohne** Karte, nicht alten Karten. **Vor Schritt 9 entscheiden:** alten
   Stand belassen (empfohlen, ehrlich) oder dem Spieler anbieten, die Karte neu zu ziehen.
2. **"niemals zwei gleiche Karten".** Signatur = `"".join(raster)` (`src/main.py` Z. 187-189),
   Laenge wechselt 40 -> 56. Mit 56 Feldern gibt es mehr Muster, `KARTENVERSUCHE = 400` (Z. 184)
   bleibt ausreichend. Der Vergleich mischt Formate nur, wenn alte 40er- und neue 56er-Karten
   derselben Siedlungsliste angehoeren — dann sind sie ohnehin verschieden lang. `unklar`:
   tatsaechliche Kollisionsrate erst nach einem Lauf messbar (hier kein Test ausgefuehrt).
3. **Klickrechnung / Zeichenflaeche.** `_klick` rechnet `spalte=(x-rand)//zelle`,
   `zeile=(y-rand)//zelle` (`src/main.py` Z. 2045-2049) und `_feld_ecke` analog (Z. 1950-1952).
   Beide nutzen die Kartenmasse, sind also fuer 7 Zeilen korrekt. Aber die Flaeche wird hoeher:
   `18 + 7*64 = 466 px` gegen heute `18 + 5*64 = 338 px` (Z. 1944-1945). In
   `_zeichne_siedlungskarte` gibt es **keine Bildlaufleiste** — auf kleinen Fenstern kann die
   unterste Zeile abgeschnitten werden. Vor dem Einhaengen die Fensterhoehe pruefen.
4. **astra-Gutachten mit 8x7-Annahme.** `docs/audits/ux_astra_karten_feinheit_2026-10-05.txt` Z. 36
   schreibt "das vorgegebene 8×7-Raster bleibt bestehen". Das ist ein **VORSCHLAG** des
   Bildmodells, **kein** Originalbeleg (dieselbe Datei Z. 3). Nicht als Originaltreue ausgeben.
5. **`karte_profil` / "alle außer Sumpf".** `src/gelaende.py` Z. 279-282 schliesst beim Profil nur
   `SUMPF` aus. Eine neue nicht bebaubare Art `wasser` wuerde sonst als ertragsfaehig gezaehlt
   (Mana/Holz zu hoch). Den Ausschluss ueber das Feld `bebaubar` fahren, nicht ueber den Namen.
6. **Fehlende Gewichte.** Nimmt man `wasser` nicht in alle fuenf `gewichte` auf
   (`data/gelaende.json` Z. 100-132), faellt der Erzeuger auf `haftigkeit` zurueck
   (`src/gelaende.py` Z. 202, 206), und `tests/test_gelaende.py` Z. 143-144 ("Gewichte fuer alle
   Geländearten") wird rot.
7. **Versteckte 40 in Tests.** Besonders `tests/test_gelaende.py` Z. 187 (`40 * g[art] / summe`)
   ist leicht zu uebersehen: der Erwartungswert skaliert mit der **Feldzahl**, nicht mit 40.
8. **`bauplaetze`-Bedeutung.** Wechsel von "Gesamtfelder" (Z. 251 heute) zu "bebaubare Felder"
   beruehrt `karte_beschreiben` (Z. 307) und `tests/test_wirtschaft.py` Z. 180-183. Beide Stellen
   muessen mitziehen, sonst rechnet die Mana-Kapazitaet falsch.
9. **Nebelsee-Annahme.** Solange nicht entschieden ist, ob der Nebelsee zu den 40 zaehlt, ist die
   Zahl "40 bebaubar" nicht eindeutig (siehe 1.5 und Abschnitt 6).
10. **Kein Testlauf in diesem Auftrag.** Dieser Plan wurde ohne Ausfuehrung der `tests/` erstellt
    (Auflage). Alle "gruen"-Angaben in Abschnitt 4 sind Erwartungen, keine Messungen.

---

## 6. Was dieser Plan NICHT klaeren konnte (Liste)

1. **Nebelsee bebaubar oder nicht.** Daten (`data/gelaende.json` Z. 61) und Handbuch
   (`...Textfassung.txt` Z. 403) sagen bebaubar; der Auftragstext nennt ihn nicht bebaubar. Das
   entscheidet mit, welche 16 Felder gesperrt sind.
2. **Aufteilung der 16** zwischen Sumpf und Wasser (z. B. Sumpf 6 / Wasser 10) — Daniel hat nur
   56/40 entschieden, nicht die Verteilung.
3. **Wege oder Wasser.** Die Datennotiz sagt "Wege/Wasser" (`data/gelaende.json` Z. 10); ob die 16
   Felder begehbare Wege oder gesperrte Wasserflaechen sind, ist offen.
4. **Umgang mit alten 40er-Spielstaenden** (belassen oder Karte neu ziehen) — Produktentscheidung.
5. **Fenster-/Bildschirmhoehe** fuer die 466-px-Zeichenflaeche ohne Bildlaufleiste — nicht gemessen.
6. **Eigenes Wasserbild.** `karten_optik_fein` zeichnet `wasser` derzeit wie `nebelsee`
   (Z. 159-182); ob eine eigene Darstellung gewuenscht ist, ist offen.
7. **Kollisionsrate der "niemals zwei gleiche"-Pruefung** bei 56 Feldern — erst nach einem
   Testlauf messbar.
