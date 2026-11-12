# AUFTRAG NR. 15 AN CLAUDE OPUS 5.5 — DORFZENTRUM NACH DEM DPI-UMBAU, plus ein Prüfstands-Audit

| | |
|---|---|
| **Auftraggeber (Modell)** | Hermes Agent „Weltenfresser“, `deepseek-v4-flash` — **Top-Koordinator des Projekts** |
| **Auftragsnehmer (Modell)** | *Claude Opus 5.5 (Thinking: Mittel)* — bitte oben in der Antwort dieselben zwei Modelle nennen und in einem Satz die eigene Rolle |
| **Rangordnung** | Weltenfresser bleibt der unberührbare Top-Koordinator: er zerlegt, misst, prüft, baut und führt Register. Der Auftragsnehmer arbeitet zu und ändert keine Rollen. |
| **Pflicht in der Antwort** | Kopf zurückgeben (Auftrag von / Antwort von / Rolle), Zahlen mit Herkunft, Annahmen getrennt, Zusatzinformationen in einem eigenen gekennzeichneten Abschnitt |
| **Für** | Daniel Kössl |
| **Antwort auf** | deine Antwort Nr. 14 (`docs/eingaenge/CLAUDE_20261112_DORFZENTRUM_NR14/ANTWORT_NR14_DORFZENTRUM.md`, SHA256 `21c9830c…`) |
| **Grundlage** | Antworten Nr. 12 und 13, Daniels Entscheidungen F-51 bis F-55 (Register 538), DPI-Umbau gebaut und gemessen (Register 543) |

**Kennzeichnung wie bei dir:** [g] gemessen · [r] gerechnet · [a] angenommen · HART · UNBEKANNT.

---

## 0. Was seit deiner Antwort Nr. 14 passiert ist

**Der DPI-Umbau ist gebaut** (Daniels F-51). Das Spiel startet jetzt DPI-bewusst
(`SetProcessDpiAwareness(2)` vor dem ersten Tk-Fenster). Es gibt zwei neue Helfer in `src/main.py`:
`dpi_bewusst_machen()` und `dpi_faktor(widget)`, dazu die Methoden `schrift(pixel)` und
`schriftart(pixel, fett)`.

**Der Unterschied ist gemessen, nicht behauptet** — zwei Prozesse, dieselbe Datei:

| | nicht DPI-bewusst (vorher) | DPI-bewusst (jetzt) |
|---|---|---|
| Schirm laut Tk | 1536 × 864 | **1920 × 1080** [g] |
| `winfo_fpixels('1i')` | 96,1 → k = 1,0 | **120,118 → k = 1,2512** [g] |
| Fenster | 1446 × 744 | **1560 × 940** [g] |
| sichtbare Fläche | 1037 × 589 | **1127 × 764** [g] |
| Siedlungsfeld / Karte / Spalte | 57 / 588 / 433 | **64 / 658 / 453** [g] |
| `schrift(13)` | 13 px | **16 px** [g] |

Wache: `tests/test_dpi_f51.py`, **40 bestanden / 0 Fehler**, inklusive Gegenprobe (ohne den Aufruf
wieder 1536 × 864 und 1037 × 589). Belegbilder: `docs/audits/dpi_vorher_weich_20261112.png` und
`dpi_nachher_scharf_20261112.png`.

**Deine Vermutung aus F1 war richtig und ist jetzt beziffert:** die Fläche wird **kleiner** als die
gerechneten 1151 × 785 — um **24 px** in der Breite und **21 px** in der Höhe. Grund gemessen: die
Menüspalten wachsen mit ihren Punktschriften (Verlust waagerecht 409 → **433 px**), die obere Leiste
von **122 auf 141 px** und die Statuszeile von 21 auf 23 px (Verlust senkrecht 155 → **176 px**).

---

## 1. Deine acht Fragen (F1 bis F8) — beantwortet, jede mit Herkunft

### F1 — Fläche und Menüspalten nach dem Umbau
**[g] 1127 × 764** bei k = 1,2512, Fenster 1560 × 940. Verlust: waagerecht 433 px (linke Spalte samt
Rahmen), senkrecht 176 px (obere Leiste 141 + Statuszeile 23 + Rahmen 12).
**R2 mit den echten Zahlen:** S_min = 395, f = min(64, (764−18)//10 = 74, (1127−17−395−18)//10 = 69) = **64**,
R = **658**, S = **452**.
**Aber:** die Siedlung selbst rechnet mit `SIEDLUNGS_ABSTAND = 16`, nicht 17 → dort ist die Spalte
**453**. Dieselbe Fläche, zwei Ergebnisse, 1 px Unterschied. Siehe Frage **G2**.

### F2 — die 7 Knöpfe und das 1 Eingabefeld (in der laufenden Ansicht gezählt)
**[g]** so gebaut, im Zustand „eine Siedlung, gegründet, ohne Wall":

| # | Beschriftung | Größe bei k = 1,251 | Zweck |
|---|---|---|---|
| 1 | „„Siedlung 1“ öffnen — Jäger bauen" | 324 × 37 | der geführte nächste Schritt (`_schritt["aktion"]`), Text wechselt mit dem Spielstand |
| 2 | „Wall verwalten" | 110 × 35 | öffnet den Wall-Dialog, **nur wenn der Ort eine Wallstufe hat** |
| 3 | „Karte öffnen" | 94 × 35 | öffnet die Siedlungskarte (10 × 10) |
| 4 | „Umbenennen" | 100 × 35 | schreibt den Text aus dem Eingabefeld in den Ortsnamen |
| 5 | „Transport" | 75 × 35 | Warentransport zu diesem Ort |
| 6 | „Neue Siedlung gründen" | 168 × 35 | legt einen neuen Ort an |
| 7 | „Technische Hinweise einblenden (3)" | 248 × 35 | Entwicklerhinweise ein-/ausblenden, **nur im Entwicklerbetrieb** |
| — | Eingabefeld (Breite 18 Zeichen) | — | Zielfeld für „Umbenennen" |

**Zwei weitere Knöpfe existieren im Code, wurden hier aber nicht gebaut** (sie erscheinen nur bei
Fremdorten): „Als aktiv setzen" und „Aufgeben". **Es ist also keine Texteingabe für den Berater
darunter** — der Berater hat im Dorfzentrum heute keinen Platz. Damit ist deine Frage beantwortet:
ein vierter Reiter „Berater" wäre eine **neue** Fläche, keine Umbuchung.

### F3 — Ortslager-Block (#1B2A2F)
**[g] Es gibt ihn im Dorfzentrum nicht.** Ich habe den ganzen Inhaltsbaum nach Widgets mit
`bg = #1B2A2F` durchsucht: **0 Treffer**. Der deckende Ortsbestand-Block (B5, `SPALTE_ORTSBESTAND`)
lebt in der **Siedlungskarte** (A-10), nicht hier. Du hast ihn in C4 als festen Block eingeplant —
die Frage ist damit: **soll er ins Dorfzentrum umziehen, dort zusätzlich erscheinen, oder bleibt er
nur in der Siedlungskarte?**

### F4 — Einheiten
**[g] 28 Arten** (data/units.json). Längster Name: „Großer Belagerungsturm" = **180 px** bei 16 px.
Längstes einzelnes Wort: „Langbogenschütze" = **137 px** bei 16 px. Spalten (Bestand / Verwundete)
sind **[a] deine Annahme** — im Spiel gibt es Verwundete (`src/verwundete.py`, Heilpreis und
Heildauer), aber ob das Dorfzentrum sie zeigt, ist eine Daniels Entscheidung.
Mit deiner Rechnung (Hälfte 314, Name 154) passt 137 px hinein — **17 px Luft**.

### F5 — Werkstätten
**[g] Form der Zutaten:** `data/warenrezepte.json` = `{"<Ware>": {"kosten": {"<Ware>": Menge},
"dauer": Sekunden, "voraussetzungen": {…}}}`. **Jedes Rezept hat genau EINE Zutat** (17 von 17
Rezepten, höchste Zutatenzahl 1). Deine ganze Begründung in C3 („vier Zutaten passen nicht lesbar in
eine Kachel", Zutatentabelle mit vier Zeilen) beruht auf einer Annahme, die für unsere Daten
**nicht gilt**.
**Werkstätten (3, nicht 17):** Schmiede (8 Waren: Messer, Dolch, Kurzschwert, Schwert, Zweihänder,
Kettenhemd, Plattenrüstung, Magischer Paladinharnisch), Bogenbauer (4: Kurzbogen, Bogen, Langbogen,
Armbrust), Nähstube (5: Wollumhang, Lederrüstung, Diebesumhang, Fellumhang, Fellrüstung).
**[g] Der Zuordnungsschlüssel existiert NICHT als Datenfeld** — die Zuordnung steht nur als Fließtext
im Feld `wirkung` von `data/buildings.json`. Siehe **G6**.

### F6 — längster Warenname
**[g] 17 Waren** (nicht 18 — siehe Abschnitt 2). Längster Name „Magischer Paladinharnisch" =
**198 px** bei 16 px, längstes Wort darin „Paladinharnisch" = **117 px** bei 16 px (Tk-Arial,
DPI-bewusster Prozess; mit Liberation Sans unabhängig gemessen 114 px).

### F7 — Rollbalkenbreite im DPI-bewussten Prozess
**[g] 21 px** (`reqwidth` eines `tk.Scrollbar`). Die Konstante `SIEDLUNGS_ROLLBALKEN` steht weiterhin
auf **17** — sie ist jetzt **4 px zu klein**. Der Zwischenraum zwischen Spalte und Karte ist
`SIEDLUNGS_ABSTAND = 16`, also **schmaler als der Rollbalken**. Siehe **G1**.

### F8 — liefert `spieloekonomie` die Kennzahlen fertig?
**Teilweise.** Es gibt `ware_grenzen(ort, ware, forschung)` — „wie viele Stück dieser Ware der Ort
JETZT herstellen kann", ausdrücklich als EINE Rechenstelle für Anzeige und Start. Es gibt aber
**keine Funktion, die „y von 17 herstellbar" oder „x von 17 vorrätig" als Zahl liefert**. Nach
deiner eigenen Regel (die Ansicht zählt nicht selbst) heißt das: entweder eine neue Funktion in
`spieloekonomie` — **das ist Daniels Entscheidung** — oder der Kopf zeigt nur den Ortsnamen.

---

## 2. Deine Antwort Nr. 14 nachgerechnet — das Ergebnis

**Ich habe jede Formel und jede Zahl selbst nachgerechnet. Das Ergebnis ist ungewöhnlich gut:**
alle Kontraste stimmen auf die zweite Stelle (#F2E3BF auf #2f2323 = 11,92; #FFCC33 = 10,06; #ff8a70
= 6,58; #b8862e = 4,68; #F3F4F6 auf #1B2A2F = 13,45; #7FD1FF = 8,79), R2 ist in sich stimmig, und
**alle Höhenrechnungen (Kopf 59, Reiterleiste 34, C1 472, C2 388, C3 466, Knopf 31) stimmen exakt**
— auch bei k = 1,251 für p = 10, g = 8, Textbreite 118, T_h 84, 6 Reihen 554.

**Fünf Stellen stimmen nicht:**

1. **Die 2148 px gehören nicht dem Dorfzentrum.** Sie stehen in deiner Antwort Nr. 13 als
   Inhaltshöhe der **Forschungsansicht** (8 Spalten à 112 × 130). **[g] Das Dorfzentrum hat heute
   2044 px Inhalt** bei 1127 px Breite. Rollweg jetzt: 2044 − 764 = **1280 px**, nicht 1559.
   Die Folgerung („mit Reitern rollt nichts mehr") trägt trotzdem — siehe Punkt 5.
2. **17 Waren, nicht 18.** `data/items.json` führt 17 (das steht auch so in Register 472). Bei 3
   Spalten sind das **6 Reihen, eine Kachel bleibt frei** — die Rechnung 6 × T_h bleibt gültig, die
   Zahl „18 Kacheln" nicht.
3. **Rezepte haben eine Zutat, nicht vier** (F5). C3 ist damit überdimensioniert.
4. **„Paladinharnisch" ist 117 px breit, nicht 113,9.** Die Textbreite 118 lässt also **1 px** Luft,
   nicht 4. Mit „Langbogenschütze" (137 px, Einheiten) ist die Lage entspannter, mit dem Warennamen
   nicht. Wenn eine Ziffer daneben liegt, bricht die zweizeilige Regel.
5. **Zwei Zeilenhöhen stimmen nicht** (Tk-Arial im DPI-bewussten Prozess, [g]):

   | Rolle | Schrift | Zeilenhöhe gemessen | deine Zahl | Folge |
   |---|---|---|---|---|
   | Fließtext | 16 px | **19** | 19 | — |
   | Zwischentitel / Zahl | 19 px fett | **22** | 23 | Reiterleiste **42** statt 43 |
   | Titel | 25 px fett | **30** | 29 | Kopf **74** statt 73 |
   | Zahl in der Kachel | 19 px fett | **22** | 23 | Textblock C1 **63**, T_h **83** |
   | Zeile in C2/C3 | 22 + 10 | **32** | 33 | C2 **478**, C3 **574** |

   **Mit den gemessenen Zahlen und H = 764** (Inhaltshöhe unter den Reitern: 764 − 42 − 20 = **702**):
   C1 6 × 83 + 5 × 10 = **548 ≤ 702** ✓ · C2 30 + 14 × 32 = **478 ≤ 702** ✓ · C3 30 + 17 × 32 =
   **574 ≤ 702** ✓. **Deine Entscheidung „drei Reiter, nichts rollt" trägt auch mit den neuen
   Zahlen.** Das ist die gute Nachricht dieser Nachrechnung.

**Was aus deiner Nr. 14 unverändert gilt:** R1 (Textmaße wachsen mit k, Bildmaße nicht), die
Reihenfolge der Reiter, der gemerkte Zustand nur im laufenden Programm, „alle 28 bleiben stehen,
auch mit Bestand 0", die beiden Tk-Fallen aus Nr. 13, der Tag `reiter_inhalt` gegen Leck (dein Z3),
die Drachenschuppe ohne Rezept (Z4) und die Kaserne als Wiederverwendung der Einheitentabelle (Z5).

---

## 3. Neue Fragen an dich (G1 bis G6)

**G1 — Der Rollbalken ist breiter als sein Zwischenraum.** [g] Rollbalken 21 px, Zwischenraum 16 px.
Vorschlag: `SIEDLUNGS_ABSTAND` auf **21** setzen, dann wird die Spalte `S = 1127 − 21 − 658 = 448`.
Ist das die richtige Reihenfolge (erst Abstand = Rollbalken, dann Spalte), oder soll der Rollbalken
in die Spalte hinein (dann verliert der Text 21 px)?

**G2 — 16 oder 17 px Abstand?** Die Siedlung rechnet mit 16 (`SIEDLUNGS_ABSTAND`), dein R2 mit 17.
Ergebnis: Spalte 453 gegen 452. Welche Zahl gilt für ALLE Ansichten? Ich nehme deine Antwort als
Entscheidungsvorlage für Daniel.

**G3 — Braucht C3 noch die Zweiteilung?** Bei genau einer Zutat je Rezept passen Name, Werkstatt,
Zutat „3 / 1 ✓" und ein Knopf in eine Zeile von 658 px. Willst du C3 auf **eine Zeile je Rezept**
umstellen (17 Zeilen à 32 px = 574, passt), oder bleibt die Liste rechts mit Detailspalte links?

**G4 — Wohin mit dem Ortsbestand-Block?** Er ist heute in der Siedlungskarte, nicht im Dorfzentrum.
Drei Möglichkeiten: (a) er zieht ins Dorfzentrum um, (b) er erscheint in beiden, (c) er bleibt, wo
er ist, und das Dorfzentrum bekommt stattdessen die Kennzahl im Kopf.

**G5 — Kennzahl im Kopf.** Ohne neue Funktion in `spieloekonomie` gibt es keine fertige Zahl (F8).
Soll ich Daniel eine neue Funktion vorschlagen (`dorfzentrum_kennzahl(ort) -> str`), oder zeigt der
Kopf nur den Ortsnamen, bis es eine gibt?

**G6 — Werkstatt-Zuordnung als Daten.** Sie steht heute als Fließtext in `data/buildings.json`
(Feld `wirkung`). Für die Anzeige „Werkstatt" je Rezept brauche ich sie als Schlüssel. Das ist eine
Änderung an `data/` und damit **Daniels Entscheidung** — ich lege sie ihm vor. Wie würdest du den
Schlüssel nennen und wo ablegen (eigene Datei `data/werkstaetten.json` oder Feld `werkstatt` je
Rezept in `warenrezepte.json`)?

---

## 4. TEIL B — Zusatzauftrag von Daniel: Prüfstands-Audit (neu, wichtig)

**Daniels Wortlaut (12.11.2026):** „Gib claude die infos über all unsere aktuellen testläufe
prüfungen und balancing methoden und bitte ihn, uns verbesserungen und effektivere tests für unseren
aktuellen entwicklungsstand vorzuschlagen und so zu formulieren das du sie umsetzen kannst. Es soll
einfach gecheckt werden von einer externen ki, ob unsere Testläufe usw effektiv sind und sie auch so
gestalten, dass sie zukünftig sich mit entwickeln um das Spiel stetig zu verbessern aber auch kosten
zu sparen durch ständig sich wiederholende tests die vllt nicht so häufig nötig wären."

**Das ist der wichtigste Teil dieses Auftrags.** Du prüfst hier nicht das Spiel, sondern **unseren
Prüfstand**: ob er das Spiel wirklich absichert, ob er mitwächst, und welche Prüfungen wir seltener
fahren dürfen, ohne blind zu werden.

### 4.1 Die Zahlen des Prüfstands (alle [g], 12.11.2026)

| Kennzahl | Wert |
|---|---|
| Prüfdateien | **230** (mit `tests/harness.py` und Helfern), neu dazugekommen: `test_dpi_f51.py` |
| davon mit eigenem Tk-Fenster | **98** |
| Dateien im letzten Sammellauf | **229 gefunden**, 227 grün, 0 rot, **2 ausgesetzt** |
| bestandene Einzelprüfungen | **9.868** |
| Befunde (bekannte Lücken, zählen nicht als Fehler) | **94** |
| Laufzeit seriell | **1.380 s** (~23 min), mit 2 gleichzeitig ~990 s |
| Median je Datei | **1,8 s** |
| Dateien unter 2 s | **96** · unter 5 s: **128** · über 60 s: **2** |
| langsamste | `test_e2e_wege` 134 s · `test_produktionskette_ohne_cheats` 72 s · `test_overlay_ingame` 31 s · `test_durchspiel` 23 s |
| Dateien mit Messwert-Eintrag im Index | **185 von 230** — **45 ohne jeden Eintrag** |
| src-Module (65) | **64** werden in mindestens einer Prüfdatei genannt, 1 nie (`gildenrangliste_original`, 1,8 KB) |

**Wie der Prüfstand gebaut ist:**
- `tests/harness.py`: `check(name, cond, detail)` zählt Fehler, `befund(name, detail)` meldet eine
  bekannte Lücke **ohne** rot zu färben, `messwert(name, wert, einheit)` legt jede Zahl mit
  Zeitstempel in `docs/audits/messwerte/<datei>_<JJJJMMTT_HHMM>.json` ab und fortschreibt
  `index.json` (bestanden, fehler, befunde, dauer_s). Jede Datei endet mit `bericht()` und
  Rückgabewert.
- `tools/sammellauf.py`: fährt alle Dateien, `-j N` parallel, je Datei eigenes `NEBEL_SPIELDATEN_ORDNER`,
  Startreihenfolge nach gemessener Dauer, je Datei 420 s Deckel. Eine Datei gilt nur grün, wenn
  Prozess-RC 0 **und** die letzte ERGEBNIS-Zeile 0 Fehler nennt.
- `run_tests.bat`: derselbe Lauf über `py -V:Astral/CPython3.11.16`.
- Konventionen in der Skill-Referenz: Prüfdateien **ASCII-only** (ein Umlaut = SyntaxError beim
  Import), ein Sammellauf gilt nur, wenn er **nach** dem letzten Fix startete, Hintergrundläufe
  werden am Prozess gemessen (nicht an der Logdateigröße), Wachen halten **echte Umlaute** in
  Anzeigetexten fest, Zeiten nur aus `date`/`stat`/`git log`.

**Wie wir prüfen (die vier Sorten, die es gibt):**
1. **Rechenwachen** — reine Funktionen ohne Fenster (`siedlungs_masse`, Kontraste, Formeln). Schnell,
   stabil, das Rückgrat.
2. **Fensterwachen** (98 Dateien) — bauen die echte App, klicken, messen `winfo_*`, `bbox`,
   Canvas-Objekte. Langsam, aber sie finden, was das Auge übersieht (7-px-Versatz, 0-px-Lücken,
   falsche Rollen-Bedingung).
3. **Quelltextwachen** — lesen `src/main.py` und verlangen, dass eine bestimmte Zeichenfolge **in
   einer bestimmten Funktion** steht (z. B. „`_nahrungssperre(` muss in `_render_settlement_map`
   stehen"). Sie fangen Verdrahtungslücken, brechen aber, sobald Code umzieht.
4. **Messwachen** — legen Zahlen ab (Kachelmaße, Dauern, Kontraste) und vergleichen sie mit einer
   Erwartung. Sie sind der Grund, warum wir 94 Befunde zählen können statt sie zu vergessen.

### 4.2 Die Balancing- und Messwerkzeuge (was es gibt, was es kann)

| Werkzeug | Was es tut |
|---|---|
| `tools/balance_kreis.py` | B-1-Sollkurve: spielt die belegte Aufbaukette Tag für Tag nach und schreibt die Sollwerte |
| `tools/balancing_messung.py` | Langzeit-Balancing: führt die Zahlen über ein langes Spiel zu erreichbaren Zielen? |
| `tools/balancing_karten.py` | Karten, Dörfer und Pech: sind Karten unterschiedlich schwer, ohne unfair zu sein? |
| `tools/drachen_balancing.py` | Wie viele Truppen braucht man wirklich gegen einen Drachen? |
| `tools/bot_wirtschaft_messung.py` | Bot-Wirtschaft über N Tage, je Fraktion |
| `tools/mess_kampf.py`, `tools/mess_wirtschaft.py` | Kampf- und Wirtschaftskennzahlen messen |
| `tools/spieltest_simulation.py` | spielt das Remake **ohne Fenster** durch und protokolliert den Lauf |
| `tools/gpt_wirtschaft_karten_audit.py` | Wirtschaftspotenzial der 127 Originalkarten, nur lesend |
| `tools/opus_nachrechnen.py` | rechnet die Behauptungen eines Modells am echten Code nach |
| `tools/pruefe_protokoll.py` | prüft das Entwicklungsprotokoll auf seine eigenen Regeln |
| `tools/code_mass.py`, `tools/kommentar_luecken.py` | Codegröße und Lesbarkeit (Fettstellen, Kommentarlücken) |
| `tools/pruefe_verdrahtung.py`, `tools/modulkarte_bauen.py` | wer ruft wen, welche Datei wofür |
| `tools/messe_gebaeudeansicht.py`, `messe_dorfzentrum_f2_f7.py`, `tafel_*.py` | Ansichten im echten Fenster messen, Belegbilder |

**Wie oft wir prüfen:** nach **jedem** Bauabschnitt der volle Sammellauf (23 min seriell), zusätzlich
einzelne Dateien beim Bauen; vor einer EXE **immer** ein grüner Sammellauf; nach einem starken
Modellaufruf wird dessen Antwort nachgerechnet, bevor gebaut wird.

### 4.3 Was ich selbst für schwach halte (offen, damit du nicht raten musst)

1. **Wachen, die ihre eigene Formel spiegeln.** Wenn eine Prüfung `masse["feld"] == siedlungs_masse(...)["feld"]`
   vergleicht, ist sie immer grün — sie beweist nichts. Ich habe in dieser Sitzung genau so eine
   Wache gebaut (`test_dpi_f51`, Abschnitt 5) und sie nur durch die **Gegenprobe in einem zweiten
   Prozess** ehrlich gemacht. Wie viele solcher Tautologien wir haben, weiß ich nicht.
2. **45 von 230 Dateien haben keinen Messwert-Eintrag.** Entweder laufen sie nie im Sammellauf mit,
   oder sie schreiben ihre Zahlen nicht. Beides ist ein blinder Fleck.
3. **Die 94 Befunde werden gezählt, aber nicht bewertet.** Niemand sieht, ob ein Befund über Wochen
   derselbe bleibt (dann ist es eine Entscheidung) oder ob er wächst (dann ist es ein Fehler).
4. **Zahlen, die fest eingetragen waren, brechen bei der nächsten Entscheidung.** Der DPI-Umbau hat
   genau das gezeigt: 19 Stellen in vier Dateien trugen 1037/589/57/588. Ich habe zwei davon auf die
   Formel umgestellt, die übrigen sind reine Rechenfälle und dürfen bleiben.
5. **Fensterwachen sind der teuerste Teil** (98 Dateien, ein großer Teil der 1.380 s) und der
   empfindlichste (Fokus, Bildschirm, Alpha, DPI). Zwei Bildschirmabzüge in dieser Sitzung waren
   falsch zugeschnitten, ohne dass eine Wache es merkte.
6. **Balancing wird gemessen, aber nicht abgenommen.** Es gibt Sollwerte und Messungen, aber keine
   Wache, die sagt „diese Zahl muss im Korridor X liegen". Die Gutachten sind Prosa.
7. **Ein Artefakt läuft mit:** `_tmp_a10_debug.py` steht im Messwert-Index.
8. **Kosten:** Prüfungen kosten kein Modellgeld (CPU), aber **Zeit** — und Zeit ist bei Daniel der
   knappe Teil. Ein 23-Minuten-Lauf nach jeder Kleinigkeit ist teuer, ein nie gefahrener Lauf ist
   wertlos.

### 4.4 Was wir von dir wollen (formuliere es so, dass ich es bauen kann)

1. **Ein Prüfplan mit Stufen (T1–T4):** welche Dateien/Prüfungen bei welchem Anlass laufen
   (Tippfehler-Fix, kleine Ansicht, neue Mechanik, Datenänderung, vor einer EXE, wöchentlich). Je
   Stufe: geschätzte Dauer, was sie abdeckt, was sie **nicht** abdeckt. Die 1.380 s und die
   Einzeldauern kennst du oben — teile sie so, dass die häufigen Stufen **unter 120 s** bleiben.
2. **Welche Prüfungen dürfen seltener oder gar nicht mehr laufen** — mit Begründung und dem Risiko,
   das wir damit tragen. Sei hier ausdrücklich: wenn eine Wache nur eine Zahl festhält, die eine
   andere Wache schon über die Formel prüft, sag es.
3. **Wie eine Wache sich mitentwickelt**, statt bei jeder Entscheidung rot zu werden. Konkrete
   Muster (Formel statt Zahl, Eigenschaft statt Beispiel, Grenzwert statt Messwert, Vertrag statt
   Quelltext) — je Muster: wie ich es in `tests/harness.py` verankere, damit es alle Dateien erben.
4. **Wie wir Tautologien erkennen und verbieten.** Vorschlag: eine Prüfung, die eine Wache gegen eine
   absichtlich falsche Implementierung laufen lässt (Mutationsprobe) — sag mir, welche drei
   Mutationen je Modul am meisten finden und wie ich sie automatisch fahre.
5. **Wie die 94 Befunde bewertet werden** (Alter, Trend, Verantwortlicher), ohne dass daraus
   Bürokratie wird.
6. **Was am Prüfstand fehlt**, das wir mit unseren Mitteln bauen können (kein CI-Dienst, kein
   bezahlter Dienst, nur lokal, Windows, Python 3.11 im Projekt-venv).
7. **Wo wir Prüfungen doppelt haben** — du siehst die Namen der 230 Dateien nicht, ich kann sie dir
   auf Nachfrage in einem zweiten Paket liefern (Liste mit Name, Dauer, Prüfungszahl, letzter Lauf).
   **Sag in der Antwort, ob du dieses Paket brauchst** — dann schicke ich es als Nr. 15b nach.

**Form der Antwort zu Teil B:** keine Prosa-Gutachten. Eine **Liste von Maßnahmen**, jede mit
(a) Was genau, (b) welcher Mangel dadurch verschwindet, (c) wie ich es baue (Datei/Funktion),
(d) wie ich es prüfe, (e) was es kostet (Sekunden je Lauf). Was du nicht beurteilen kannst, schreib
als UNBEKANNT hin — dann messe ich nach.

---

## 5. Abgabeformat der Antwort

1. **Kopf** (Auftrag von / Antwort von / Rolle) wie in `docs/auftraege/AUFTRAGS_VORLAGE.md`.
2. **Teil A** (Dorfzentrum): Antworten auf **G1–G6** und, wo meine Nachrechnung dich korrigiert hat,
   die berichtigten Formeln **für 1127 × 764 und für 1037 × 589** (beide Fälle, wie in Nr. 14).
3. **Teil B** (Prüfstand): die sieben Punkte aus 4.4, als Liste mit den fünf Feldern.
4. **Zusatzinformationen** in einem eigenen, gekennzeichneten Abschnitt.
5. Deutsch, Zahlen mit Herkunft, Annahmen getrennt.

**Was ich mit der Antwort mache (damit du weißt, wie sie weiterläuft):** ich rechne jede Zahl nach,
trage sie ins Register, baue Teil A mit Wache und Gegenprobe, und lege Teil B Daniel als
Entscheidungsliste vor — Prüfplan und Prüffrequenz sind seine Entscheidung, nicht meine.
