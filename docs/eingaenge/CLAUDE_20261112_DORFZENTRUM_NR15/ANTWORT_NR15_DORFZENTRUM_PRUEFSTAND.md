# ANTWORT AUF AUFTRAG NR. 15: Dorfzentrum nach dem DPI-Umbau, Prüfstands-Audit, Konzeptabgleich

| | |
|---|---|
| **Auftrag von** | Hermes Agent „Weltenfresser“, `deepseek-v4-flash`, Top-Koordinator des Projekts |
| **Antwort von** | Claude Opus 5.5 (Thinking: Mittel) |
| **Meine Rolle** | Ich arbeite zu. Ich beantworte G1 bis G6, prüfe den Prüfstand von außen (Teil B) und gleiche mein Design mit dem Konzept ab (Teil C). Weltenfresser rechnet nach und baut, Daniel entscheidet. |
| **Antwort auf** | AUFTRAG NR. 15 AN CLAUDE OPUS 5.5 — DORFZENTRUM NACH DEM DPI-UMBAU, plus ein Prüfstands-Audit (`AUFTRAG_CLAUDE_NR15_DORFZENTRUM_PRUEFSTAND.txt`) |
| **Für** | Daniel Kössl |

**Kennzeichnung:** [g] gemessen (von dir, wenn nicht anders gesagt) · [r] gerechnet · [a] angenommen · HART · Startwert · UNBEKANNT.

**Abkürzungen:**
- **rb** = gemessene Rollbalkenbreite (`reqwidth`).
- **p** = round(8k), **g** = round(6k).
- **ls(…)** = gemessener Zeilenabstand der Schrift.

---

## TEIL A – Dorfzentrum

### Deine Korrekturen an Nr. 14 übernehme ich

**Übernommen:**
- **ls-Werte bei k = 1,2512:** 19 / 22 / 30 statt 19 / 23 / 29. Damit Kopf **74**, Reiterleiste **42**, C1 T_h **83**, Zeile **32**.
- **Paladinharnisch** ist 117 px breit.
- **17 Waren.**
- **Eine Zutat je Rezept.**
- **Rollweg 1280 px.**

**Herkunft (zur Einordnung, nicht zur Abwehr):** Drei dieser Zahlen kamen **aus den Aufträgen selbst** in mein Rezept:
- „jede mit vier Zutaten“ (Auftrag 12, Abschnitt 0),
- „18 Arten im Spielstand“ (Auftrag 13, Abschnitt 0, und Auftrag 14, Abschnitt 2),
- „2148 px … Dorfzentrum“ (Auftrag 13, Abschnitt 3.4).

Das ist kein Vorwurf, sondern ein Befund für Teil B. Die Maßnahme dazu ist **M11 (Faktenblatt)**.

### G1 und G2 – Abstand gleich Rollbalken, nicht 16 und nicht 17

**Entscheidungsvorlage: Der Abstand zwischen Spalte und Arbeitsfläche ist rb, gemessen im laufenden Prozess. Er ist keine Konstante.** Der Rollbalken kommt **nicht** in die Spalte, sonst verliert der Text 21 px.

Die Reihenfolge ist: erst rb messen, dann R, dann S.

| Formel (ersetzt R2 aus Nr. 14) | (1037, 589, k = 1, rb = 17) | (1127, 764, k = 1,2512, rb = 21) |
|---|---|---|
| S_min = round(316k) | 316 | 395 |
| f = min(64, (H − 18) // 10, (W − rb − S_min − 18) // 10) | min(64, 57, 68) = **57** | min(64, 74, 69) = **64** |
| R = 10f + 18 | **588** | **658** |
| **S = W − rb − R** | **432** | **448** |

- `SIEDLUNGS_ABSTAND` und `SIEDLUNGS_ROLLBALKEN` **entfallen** und werden durch **rb** in `ansicht_geruest.py` ersetzt.
- Die Siedlung bekommt damit dieselben 448 wie alle anderen Ansichten. Der 1-px-Unterschied (453 / 452) verschwindet.

### G3 – Werkstätten: Liste rechts, Details links bleiben, aber schlanker

**Liste rechts plus Detailspalte bleiben.** Begründung mit Zahl: Eine Zeile mit eigener Menge und eigenem Knopf hieße **17 Eingabefelder + 17 Knöpfe = 34 Widgets**. Die Zweiteilung braucht **2**. Außerdem gleicht sie der Forschung, und Daniel erkennt das Muster wieder.

**Was sich durch „eine Zutat“ ändert:**
- Die Zutatentabelle mit 4 Zeilen entfällt.
- Die Liste bekommt **statt Bestand eine Zutat-Spalte**: „[Zutat] [vorhanden] / [nötig]“, mit ✓ oder ✕.

**Spalten bei R = 658, k = 1,2512** (Rand p = 10, Lücken p):

| Spalte | Formel | Wert | Inhalt |
|---|---|---|---|
| Name | Rest | 658 − 20 − 30 − (125 + 150 + 105) = **228** | längster „Magischer Paladinharnisch“ 198 [g] ✓ |
| Werkstatt | round(100k) | **125** | Schmiede / Bogenbauer / Nähstube |
| Zutat | round(120k) | **150** | „Wolle 3 / 1 ✓“ |
| Zustand | round(84k) | **105** | „✓ herstellbar“ oder „✕ fehlt“ |

- Bei k = 1, R = 588: Name = 588 − 16 − 24 − (100 + 120 + 84) = **244**.
- Höhe: 30 + 17 × 32 = **574 ≤ 702** ✓ [r, mit deinen ls].
- **Links:** Name, Werkstatt, die eine Zutat, dann Mengenfeld und „Herstellen“ in einer Zeile.

### G4 – Ortsbestand: (c), er bleibt in der Siedlungskarte

**Grund:** Im Dorfzentrum ist er nicht vorhanden (F3 [g]), und dort braucht die Spalte den Platz für die **sieben Knöpfe**. Die hatte ich in Nr. 14 nicht. Hier die **neue Spalte des Dorfzentrums** (bei jedem Reiter gleich bis auf Block 5):

| # | Block | Inhalt | Höhe bei k = 1,2512 [r] |
|---|---|---|---|
| 1 | Kopf (klebt) | „Dorfzentrum“ / [Ortsname] (· Kennzahl, siehe G5) | **74** |
| 2 | **Nächster Schritt** | Knopf 1 (geführter Schritt), volle Breite 448 − 20 = **428** (heute 324 [g]) | 10 + 37 + 10 = **57** |
| 3 | Ort | Eingabefeld (round(150k) = **188**) + „Umbenennen“ in einer Zeile | 2p + 35 = **55** |
| 4 | Aktionen | Zeile 1: „Karte öffnen“ 94 · „Transport“ 75 · „Wall verwalten“ 110 (nur mit Wallstufe), mit Lücken = 299 ≤ 428 ✓. Zeile 2: „Neue Siedlung gründen“ 168 | 2p + 2 × 35 + p = **100** |
| 5 | Auswahl je Reiter | Ware / Rezept / Einheit (Nr. 14 C4) | über `bbox` messen |
| 6 | Hinweis | 1–2 Zeilen | 2p + 2 × 19 = **58** |
| 7 | Technische Hinweise | Knopf 7, **nur im Entwicklerbetrieb**, ganz unten | 2p + 35 = 55 |

Summe der Blöcke 1–4 und 6 mit Lücken: 74 + 57 + 55 + 100 + 58 + 4 × 10 = **384** [r]. Für Block 5 bleiben bei H = 764 **380 px** ohne Rollen.

**Begründung für die Reihenfolge:** **Der „nächste Schritt“ steht direkt unter dem Kopf.** Er ist das einzige Bedienelement, das gegen den gemessenen **Leerlauf von 92 %** arbeitet (Teil C).

### G5 – Kennzahl: Vorschlag an Daniel mit einer Änderung

**Ja, eine Funktion vorschlagen, aber sie liefert Zahlen, keinen Text:** `dorfzentrum_kennzahlen(ort, forschung) -> dict` mit `vorraetig`, `herstellbar` (über `ware_grenzen > 0`) und `einheiten`.
- Die **Ansicht formatiert** den Text, die **Ökonomie zählt**. So bleibt `test_quelle_ast` sauber, und der Text ist änderbar, ohne die Rechenstelle anzufassen.
- Bis die Funktion existiert, zeigt der Kopf **nur den Ortsnamen**.

### G6 – Werkstatt-Zuordnung: Feld `werkstatt` je Rezept in `warenrezepte.json`

- **Wert:** die **Gebäude-ID** aus `buildings.json`, nicht der Anzeigename.
- **Begründung:** Ein Rezept hat genau eine Werkstatt. Mit dem Feld stehen alle Angaben eines Rezepts an **einer** Stelle. Eine eigene Datei bräuchte eine zweite Liste, die bei jeder neuen Ware mitgepflegt werden muss.
- **Wache dazu:**
  - Jede `werkstatt` existiert in `buildings.json`, und jede Werkstatt hat mindestens 1 Rezept (Erwartung 8 / 4 / 5).
  - **Übergangsweise** wird das neue Feld gegen den Fließtext in `wirkung` abgeglichen, bis der Fließtext geändert wird.
- Das ist eine Datenänderung; Daniel entscheidet.

### Restliche Werte nach deiner Nachrechnung

| | (1037, 589, 1) | (1127, 764, 1,2512) |
|---|---|---|
| Kopf | 59 | **74** |
| Reiterleiste | 34 | **42** |
| Inhaltshöhe unter den Reitern | 589 − 34 − 16 = 539 | 764 − 42 − 20 = **702** |
| C1 Lager: T_w / Textbreite / T_h / 6 Reihen | 185 / 99 / 72 / 472 | 206 / 118 / **83** / **548** |
| C2 Einheiten: Zeile / Höhe | 26 / 388 | **32 / 478** |
| C3 Werkstätten: Höhe | 24 + 17 × 26 = 466 | **574** |

**Zwei Regeln für zu lange Namen** (HART; Wörter vorab mit `font.measure` prüfen):

1. **Lager:** „Paladinharnisch“ (117) passt mit **1 px** Luft in 118. Das ist zu knapp. **Regel:** Ist ein Wort breiter als **Textbreite − 4**, kommt der ganze Name in Kleintext (15 px). Paladinharnisch hat dann etwa 110 px [r]. Das betrifft nach deinen Daten nur diese Ware.
2. **Einheiten:** „Großer Belagerungsturm“ (180 [g]) passt **nicht** in die Namensspalte 154. Die Zeile ist einzeilig, ein Umbruch würde z sprengen. **Regel:**
   - Zahlspalten auf round(48k) = **60** (statt 70; „9.999“ in 19 px fett ≈ 47 px [r]). Die Namensspalte wird damit 314 − 120 − 20 = **174**.
   - Ist der Name dann noch zu breit, kommt er in Kleintext 15 px (180 × 15/16 ≈ 169 ≤ 174 ✓) [r].
   - Bei k = 1: 282 − 96 − 16 = **170**; der Name hat dort 146 px [r] ✓.

---

## TEIL B – Prüfstands-Audit

**Ja, ich brauche das Paket Nr. 15b.** Inhalt je Datei: Name, ART (Rechnen / Fenster / Quelltext / Messen), Dauer, Zahl der Prüfungen, genannte `src`-Module, genannte `data`-Dateien und, wichtig, **wie oft die Datei in den letzten N Läufen rot war**. Ohne diese Liste kann ich Doppelungen (4.4, Punkt 7) **nicht** benennen. Alles unten ist so gebaut, dass es **ohne** die Liste startet.

### B1 Der Prüfplan in vier Stufen

| Stufe | Anlass | Läuft | Dauer | Deckt ab | Deckt nicht ab |
|---|---|---|---|---|---|
| **T1** | Tippfehler, Text, Kommentar | Rechen- und Quelltextwachen der **geänderten** Module (M2) + Faktenblatt (M11) + Metawachen (M1, M7) | **< 30 s** (Ziel; UNBEKANNT bis M1 fertig ist) | Formeln, Syntax, Umlaute, Verdrahtung | Fenster, Zusammenspiel |
| **T2** | kleine Ansicht, kleine Mechanik | T1 + **alle Dateien, deren Module von der Änderung betroffen sind** (M2), Fensterwachen eingeschlossen | **< 120 s** (Ziel) | die betroffene Ansicht im echten Fenster | Seiteneffekte in nicht genannten Modulen |
| **T3** | neue Mechanik, Datenänderung, Ende eines Bauabschnitts | alles **außer** den vier T4-Dateien, mit `-j 2` | ≈ (1380 − 260) / 1,39 ≈ **800 s** [r, Faktor 1,39 aus 1380 / 990] | alle Einzelwachen | lange Spielläufe, Balancing |
| **T4** | vor einer EXE, wöchentlich | alles + Balancing-Korridore (M8) + Mutationsprobe (M4) + Befundbericht (M6) | ≈ 990 s + Probe (Startwert 600 s) | alles | – |

Die vier T4-Dateien sind `test_e2e_wege` (134 s), `test_produktionskette_ohne_cheats` (72 s), `test_overlay_ingame` (31 s) und `test_durchspiel` (23 s), zusammen **260 s**. **Ausnahme:** Sie laufen zusätzlich in T2, wenn ihre Module betroffen sind.

**Wer die Stufe wählt:** Der Sammellauf schlägt sie aus `git diff` vor (M2). Weltenfresser darf sie erhöhen, nie senken. **Vor einer EXE gilt immer T4** (HART).

### B2 Die Maßnahmen

Jede Maßnahme mit **(a)** was, **(b)** welcher Mangel verschwindet, **(c)** wie bauen, **(d)** wie prüfen, **(e)** Kosten.

**M1 – Kopfangaben je Prüfdatei**
- (a) Jede Prüfdatei nennt oben `ART`, `STUFE` (1–4), `BETRIFFT` (Liste der `src`-Module) und `DATEN` (Liste der `data`-Dateien).
- (b) Ohne diese Angaben kann keine Stufe und keine Auswahl nach Änderung gebaut werden. Auch die Doppelungen bleiben unsichtbar.
- (c) `tests/harness.py`: Funktion `kopf_lesen(pfad)` liest die Angaben per AST, ohne die Datei zu importieren. `tools/sammellauf.py` bekommt `--stufe N`.
- (d) Metawache `test_pruefstand_kopf.py`: Jede Prüfdatei hat alle vier Angaben. **Anfangs nur als Befund**, nach der Umstellung HART.
- (e) etwa 1 s je Lauf; einmalig 230 Dateien ergänzen, **in Paketen von 20 mit T2 nach jedem Paket**.

**M2 – Auswahl nach Änderung**
- (a) Gelaufen wird nur, was die Änderung betrifft.
- (b) Der 23-Minuten-Lauf nach jeder Kleinigkeit fällt weg.
- (c) Der Sammellauf merkt sich in `index.json` den Commit des **letzten grünen Laufs**. `git diff --name-only <commit>` liefert die geänderten Dateien. Ausgewählt werden alle Dateien, deren `BETRIFFT` oder `DATEN` eine geänderte Datei enthält, **plus eine Stufe Aufrufer** aus `tools/modulkarte_bauen.py`.
- (d) Gegenprobe: Eine Leerzeile in Modul X ändern; die Auswahl enthält dann alle Dateien mit X in `BETRIFFT`. Eine Änderung nur in `docs/` ergibt eine leere Auswahl.
- (e) etwa 2 s für die Auswahl.

**M3 – Rechenwachen in einem gemeinsamen Prozess**
- (a) Alle Dateien mit `ART = rechnen` laufen in **einem** Python-Prozess nacheinander, jede mit ihrem `main()` und eigener Zählung.
- (b) Der Start eines neuen Python-Prozesses je Datei kostet Zeit: Der Median liegt bei 1,8 s, davon ist vermutlich ein großer Teil Interpreter und Importe (UNBEKANNT).
- (c) `tools/sammellauf.py --gebuendelt`. Jede Rechenwache bekommt eine frische Zählung (`harness.zuruecksetzen()`) und denselben `NEBEL_SPIELDATEN_ORDNER`.
- (d) Ergebnis gebündelt gleich Ergebnis einzeln (Bestanden- und Fehlerzahlen je Datei identisch). Gemessener Zeitgewinn als Messwert.
- (e) spart **UNBEKANNT**, geschätzt 0,5–1 s je Datei [a]. Bitte einmal messen.

**M4 – Mutationsprobe gegen Tautologien**
- (a) `tools/mutationsprobe.py` verändert **eine Kopie** eines Moduls absichtlich falsch und lässt die Prüfdateien laufen, deren `BETRIFFT` es enthält. **Bleibt alles grün, ist die Wache blind.** Das wird als Befund mit Datei und Zeile gemeldet.
- (b) Wachen, die ihre eigene Formel spiegeln (dein Punkt 4.3.1), werden sichtbar.
- (c) Nur Standardbibliothek (`ast`), kein Zusatzpaket. Die **drei Mutationen mit dem größten Fund** in eurer Art von Code (Formeln, Maße, Grenzen):
  1. **Zahlkonstante verschieben:** jede Ganzzahl +1, jede Kommazahl × 1,25. Findet festgeschriebene Messwerte, die nichts prüfen, und Off-by-one bei Pixeln (vgl. euren 7-px-Fehler).
  2. **Vergleich kippen:** `<` ↔ `<=`, `min` ↔ `max`, `==` ↔ `!=`. Findet ungeprüfte Grenzen, etwa „passt genau“ gegen „passt nicht“.
  3. **Rückgabe abschneiden:** `return x` → `return 0` bzw. `return None`, und Argumente vertauschen (`f(a, b)` → `f(b, a)`). Findet Wachen, die nur prüfen, dass etwas *läuft*, nicht *was* herauskommt.

  Je Modul höchstens 10 Mutanten. Ausgewählt werden sie **ohne Zufall**: die ersten 10 Stellen in Quelltextreihenfolge, bei jedem Lauf um 10 weiter rotiert (F-55: kein Zufall).
- (d) Gegenprobe: Ein Modul mit einer absichtlich tautologischen Wache muss als „blind“ gemeldet werden.
- (e) je Mutant die Laufzeit der betroffenen Dateien (Median 1,8 s, Fenster mehr). **Nur in T4**, Budget Startwert 600 s pro Woche.

**M4b – Statische Tautologie-Prüfung (billig, jeden Lauf)**
- (a) Eine AST-Prüfung meldet `check(...)`, in dem beide Seiten eines Vergleichs **dieselbe Funktion mit denselben Argumenten** aufrufen.
- (b) Die offensichtlichen Tautologien wie `masse["feld"] == siedlungs_masse(...)["feld"]`.
- (c) `test_pruefstand_tautologie.py`.
- (d) Eine eingebaute Beispieltautologie wird gefunden.
- (e) < 2 s, Stufe T1.

**M5 – Muster, mit denen Wachen mitwachsen** (alle in `tests/harness.py`, damit jede Datei sie erbt):

| Muster | Funktion im harness | Ersetzt | Beispiel |
|---|---|---|---|
| **Formel statt Zahl** | `check_formel(name, ist, formel, **eingaben)`: rechnet die Erwartung aus der Formel und legt Eingaben und Ergebnis als Messwert ab | `== 588` | Feldgröße aus (W, H, k, rb) |
| **Eigenschaft statt Beispiel** | `FENSTER_PROBEN = [(1037, 589, 1.0, 17), (1127, 764, 1.2512, 21), (867, 565, 1.0, 17), (615, 565, 1.0, 17)]` und `fuer_alle_proben(fn)` | ein festes Fenster | „keine `bbox` außerhalb der Fläche“ für alle vier Proben |
| **Grenzwert statt Messwert** | `check_korridor(name, wert, unten, oben, quelle)`; Korridore in `tests/korridore.json` (Prüfdaten, **nicht** `data/`), mit Herkunft und Datum | `== 124 ms` | Schleier-Einrechnen ≤ 250 ms |
| **Vertrag statt Quelltext** | `aufrufe_zaehlen(modul, "funktionsname")`: die Funktion wird umwickelt, die Wache ruft die Ansicht auf und prüft, ob sie gerufen wurde | „Zeichenfolge steht in Funktion X“ | `_nahrungssperre` wird beim Rendern der Siedlungskarte gerufen |
| **Gegenprobe Pflicht** | `check_gegenprobe(name, pruefung, falsche_eingabe)`: dieselbe Prüfung muss bei absichtlich falscher Eingabe **rot** werden | – | deine DPI-Gegenprobe als Standard |

- (b) Wachen werden nicht mehr bei jeder Entscheidung rot (19 Stellen beim DPI-Umbau), und Quelltextwachen brechen nicht mehr bei jedem Umzug.
- (d) Metawache: Anteil der Dateien mit mindestens einer `check_gegenprobe` als Messwert. Er soll steigen.
- (e) etwa 0 s; Umstellung **nur bei Berührung** einer Datei, nicht alle auf einmal.

**M6 – Befunde bewerten ohne Bürokratie**
- (a) `befund(name, detail, entscheidung=None)`. Der harness vergibt eine feste ID (Hash von Datei + Name) und trägt in `index.json` **ersten Tag**, **letzten Tag** und **Anzahl je Woche** ein. `tools/befund_bericht.py` erzeugt **eine Seite** mit drei Listen:
  - **neu** (seit dem letzten Bericht),
  - **wächst** (mehr Treffer als in der Vorwoche),
  - **alt ohne Entscheidung** (älter als 14 Tage, `entscheidung` leer).

  Mit gesetzter `entscheidung` (zum Beispiel „bleibt so, Register 519“) verschwindet ein Befund aus dem Bericht. Ein Feld „Verantwortlicher“ entfällt: Es gibt nur Daniel und Weltenfresser.
- (b) Die 94 Befunde werden gezählt, aber nicht bewertet.
- (d) Ein künstlicher Befund taucht am ersten Tag unter „neu“ auf und nach 15 Tagen unter „alt“; die Zeit wird dabei vorgestellt.
- (e) etwa 1 s, wöchentlich in T4.

**M7 – Blinde Flecken schließen**
- (a) Drei Metawachen:
  1. Jede vom Sammellauf gefundene Datei muss nach dem Lauf einen Eintrag in `index.json` haben, **sonst rot**. Betrifft die **45 Dateien ohne Eintrag**.
  2. Dateien mit dem Muster `_tmp*` oder `*debug*` sind in `tests/` verboten und werden aus `index.json` entfernt (`_tmp_a10_debug.py`).
  3. Jedes `src`-Modul hat mindestens eine Prüfdatei in `BETRIFFT` **oder** steht auf einer Ausnahmeliste mit Begründung (`gildenrangliste_original`).
- (e) < 2 s, T1.

**M8 – Balancing als Korridor statt Prosa**
- (a) `test_balancing_korridore.py` (T4) liest die Ergebnisse von `spieltest_simulation.py` und `balancing_messung.py` und prüft sie mit `check_korridor` gegen `tests/korridore.json`. Erste Einträge, alle **VORSCHLAG** aus deinem Abschnitt 5.7, die Werte setzt Daniel:
  - Leerlaufanteil ≤ 50 %,
  - keine Strecke über 1,5 Spieltage ohne Meilenstein,
  - Handelspunkte > 0 in einem Standardlauf,
  - jedes Volk innerhalb ±X % der Gesamtpunkte des Mittels nach N Tagen (Asymmetrie, nicht Ungleichheit).
- (b) Es gibt Sollwerte, aber keine Abnahme.
- (c) **Anfangs alle als Befund**, denn heute läge der Leerlauf mit 92 % außerhalb und der Lauf wäre sofort rot. HART erst, wenn Daniel einen Korridor freigibt.
- (d) Gegenprobe: Ein Korridor 0–1 % meldet garantiert.
- (e) so lang wie die Simulation (UNBEKANNT), nur T4.

**M9 – Bildschirmabzüge prüfen sich selbst**
- (a) `harness.abzug_pruefen(bild, fenster)`: Bildgröße = Fenstergröße (DPI-bewusst 1 : 1) **und** 3 Stichpixel an bekannten Stellen, zum Beispiel Kopffarbe bei (10, 10) und der Schleier an einer bekannten Stelle.
- (b) Abzüge, die falsch zugeschnitten sind, ohne dass es jemand merkt (zwei in dieser Sitzung).
- (e) < 0,1 s je Abzug.

**M10 – Fensterwachen unabhängig vom Bildschirm**
- (a) Jede Fensterwache setzt ihre Größe selbst (`geometry`) aus `FENSTER_PROBEN` und misst W, H, k und rb, statt den Bildschirm zu übernehmen. Ist kein Bildschirm verfügbar, wird sie **ausgesetzt**, nicht rot.
- (b) Fensterwachen hängen heute vom Bildschirm ab (Fokus, DPI, Bildschirmgröße).
- (e) etwa 0 s.

**M11 – Faktenblatt aus den Daten**
- (a) `tools/faktenblatt.py` erzeugt `docs/FAKTENBLATT.md` **aus `data/`**. Darin stehen die Anzahl der Waren, Rezepte, Zutaten je Rezept (Maximum), Werkstätten mit Waren, Einheiten, Forschungen, Gebäude, Völker, Welten und Heimatwelten, längste Namen in px bei 16 px, sowie Datum und Commit.
  - **Jeder Auftrag an ein Modell hängt das Faktenblatt an**, statt Zahlen von Hand zu schreiben.
  - Metawache: Das Faktenblatt ist nicht älter als der letzte Commit in `data/`.
- (b) Falsche Zahlen in Aufträgen wandern in Antworten und Register („4 Zutaten“, „18 Waren“, „2148 px Dorfzentrum“).
- (d) Gegenprobe: In einer Kopie der Daten eine Ware hinzufügen; das Faktenblatt zeigt 18.
- (e) < 1 s, T1.

**M12 – Rot-Historie: was seltener laufen darf**
- (a) `tools/rot_historie.py` liest alle `docs/audits/messwerte/*.json` und rechnet je Datei Läufe, Rotfunde, letzten Rotfund und mittlere Dauer. **Kandidat für eine höhere Stufe (seltener):** ≥ 30 Läufe ohne Rotfund **und** Dauer ≥ 10 s **und** keine Datei in `BETRIFFT`, die sich in den letzten 14 Tagen geändert hat.
  - Das Ergebnis ist eine **Vorschlagsliste für Daniel**. Es wird nichts automatisch verschoben.
- (b) Es ist unklar, welche Prüfungen ohne Risiko seltener laufen dürfen.
- (e) etwa 2 s, wöchentlich.

### B3 Was seltener laufen darf (ohne Paket 15b)

| Was | Neue Stufe | Begründung | Risiko |
|---|---|---|---|
| Die vier langen Dateien (260 s) | T4, außer wenn ihre Module betroffen sind (T2) | Sie prüfen das Zusammenspiel. Das ändert sich selten ohne Änderung an genau diesen Modulen. | Ein Fehler im Zusammenspiel fällt bis zu 1 Woche bzw. bis zur nächsten EXE später auf. |
| Fensterwachen nicht berührter Ansichten | T3 | Eine Ansicht ändert sich nicht, wenn keines ihrer Module geändert wurde. | Gemeinsame Bausteine (`ansicht_geruest.py`) haben viele Aufrufer. M2 erfasst sie über die Stufe Aufrufer. |
| **Messwachen, die eine Zahl festhalten, die eine Rechenwache schon über die Formel prüft** | **streichen**, nach Umstellung auf M5 | Sie prüfen dasselbe zweimal und werden bei jeder Entscheidung doppelt rot. | keins, wenn die Formelwache eine Gegenprobe hat |
| Quelltextwachen, deren Verhalten eine Fensterwache schon prüft | T3, später durch Vertrag (M5) ersetzt | Sie brechen bei Umzügen, prüfen aber nichts Zusätzliches. | gering |

**Welche Dateien das konkret sind, kann ich erst mit Paket 15b sagen.**

### B4 Was am Prüfstand fehlt und lokal baubar ist

Alles ist enthalten in M1–M12: Stufen, Auswahl nach Änderung, Bündelung, Mutationsprobe, Korridore, Faktenblatt, Rot-Historie. Dazu eine Kleinigkeit:
- **`run_tests.bat` mit Stufenwahl**: `run_tests.bat 2` startet T2. Daniel kann so ohne Konsolenwissen die richtige Stufe starten.

---

## TEIL C – Konzeptabgleich

### (a) Widersprüche zwischen meinem Design und dem Konzept

1. **Haus-Farben gegen Volk-Farben.** Abschnitt 5.3 ordnet Haus und Volk 1 : 1 zu: Silberbach = Menschen und so weiter. Die **Haus-Akzentfarben** aus meinem Handbuch (Teil 1.2) passen aber nicht zu Daniels Burgfarben:
   - Silberbach #e8667a (rot-rosa) gegen Menschen **blau**,
   - Schattenfaust #c39bea (violett) gegen Trolle **weiß-gold**,
   - Knochenmoor #7fb2ea (blau) gegen Ghule **violett**.

   **Vorschlag:** Daniels Burgbilder geben die Farbe vor. Die Haus-Akzente werden daran angeglichen, mit neuer Kontrastrechnung, sobald Daniel das will. Dazu eine Klärung: Auftrag 4 (2.6) verlangte „Häuser und Völker nicht verwechseln“. Wenn sie 1 : 1 gehören, ist der Unterschied nur einer der Rolle (Haus = Spieleridentität mit Bonus), nicht der Farbe.
2. **Bot-Flucht aus (Nr. 11) gegen „Gegner müssen den Aufbau bedrohen“ (5.5.3).** Das ist kein echter Widerspruch: Flucht schwächt Bedrohung eher, statt sie zu stärken. Bedrohung entsteht aber erst durch **Angriffe** der Bots. **Vorschlag:** Die Bot-Angriffe zeigen am Ziel beim Spieler das **Bedroht-Abzeichen aus Nr. 10** und eine Postfachmeldung **beim Start** des Marsches. Das ist die „Vorwarnung“ aus 5.7.
3. **Kopf-Kennzahlen (Nr. 13, Nr. 14) zeigen Bestände statt Entscheidungen.** Gegen den Maßstab „Entscheidungen statt Wartezeit“ wäre die bessere Kopfangabe **„Nächstes Ereignis: [was] in [Zeit]“**: die nächste fertige Forschung, das nächste Gebäude, die nächste Ankunft. **Vorschlag:** als eine weitere Zahl in `dorfzentrum_kennzahlen` (G5); Daniel entscheidet.

### (b) Tote Mechaniken und der größte Hebel

1. **Reisen (Schritt 8) ist tot:** Ein Weltwechsel kostet rund 41,7 Spieltage, also etwa 5,6 Echtstunden bei 8 Minuten je Spieltag [r]. Das wählt niemand. Der Portalsprung der Bots (Nr. 11) bringt das Reisen **zum Spieler**, ohne dass seine eigene Kette repariert sein muss.
2. **Handel ist tot:** Handelspunkte liegen in jedem Lauf bei 0. Die Auszeichnung „Händler“ ist damit unerreichbar, und eine von vier Ruhmesarten fehlt.
3. **Der Leerlauf von 92 % ist der eigentliche Befund.** Wenn 92 % der Zeit nichts zu entscheiden ist, tragen auch gebaute Mechaniken kein Spielerlebnis.

**Größter Hebel:** **Bots, die sichtbar und mit Vorwarnung angreifen** (Spannungsbogen 3). Sie verwandeln Warten in Reagieren und machen Verteidigung (Wall), Ausbildung, Kaserne und Verwundete gleichzeitig wichtig. Der Bau steht zum Teil schon: das Bedroht-Abzeichen (Nr. 10) und die Bot-Taktiken („Haug raubt“). **Messen** lässt es sich mit Korridor M8 „Leerlauf ≤ 50 %“.

---

## Was ich nicht geprüft habe

- Die 230 Dateinamen und ihre Rot-Historie: Paket 15b ist nötig.
- Wie viel Zeit der Prozessstart pro Datei kostet (M3).
- Wie lange die Simulationen für M8 laufen.
- Ob Tk-Arial bei 15 px die angenommenen Breiten hat (Kleintextregeln in Teil A).
- Woher die 41,7 Spieltage kommen. Ich habe sie übernommen.

---

## Anmerkungen an Weltenfresser (zusätzlich, nicht beauftragt)

> Hinweise, keine Anweisungen.

**Z1 Der wichtigste Satz aus Teil B:** M11 (Faktenblatt) ist die billigste Maßnahme mit der größten Wirkung **auf die Zusammenarbeit mit mir**. Drei der fünf Korrekturen in deiner Nachrechnung gingen auf Zahlen zurück, die von Hand in Aufträge geschrieben wurden.

**Z2 Die Umstellung des harness muss rückwärtsverträglich sein.**
- Alle neuen Funktionen sind **zusätzlich**; alte Dateien laufen unverändert weiter.
- Neue Metawachen beginnen als **Befund**, nicht rot. Sonst ist der Prüfstand am ersten Tag rot, und die Versuchung wächst, ihn zu umgehen.

**Z3 Nicht 230 Dateien in einem Zug ändern.** Kleine Modelle neigen bei „füge überall X hinzu“ zu Serienfehlern; ein Umlaut reicht für einen SyntaxError (eure ASCII-Regel). Deshalb Pakete von 20 und T2 nach jedem Paket.

**Z4 rb gilt je Prozess:** Die Rollbalkenbreite wird **im laufenden Prozess** gemessen, nicht einmal festgeschrieben. Auf einem Schirm mit 150 % ist sie wieder anders.

**Z5 Mutationsprobe nie am Original:** Immer an einer Kopie in einem eigenen Ordner, und `sys.path` zeigt auf die Kopie. Danach wird der Ordner gelöscht. Ein Abbruch mitten in der Probe darf `src/` nie verändert zurücklassen. Das prüft man so: `git status` ist vor und nach der Probe gleich.

---

Ende der Antwort auf Auftrag Nr. 15.
