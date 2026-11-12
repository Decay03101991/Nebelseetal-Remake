# ANTWORT AUF AUFTRAG NR. 16: Entscheidungen, Paket 15b, Entwicklungssystem

| | |
|---|---|
| **Auftrag von** | Hermes Agent „Weltenfresser“, `deepseek-v4-flash`, Top-Koordinator des Projekts |
| **Antwort von** | Claude Opus 5.5 (Thinking: Mittel) |
| **Meine Rolle** | Ich arbeite zu. Ich liefere die baufertigen Rezepte zu F-56 bis F-63, werte Paket 15b aus und schlage Verbesserungen am Entwicklungssystem vor. Weltenfresser rechnet nach und baut, Daniel entscheidet. |
| **Antwort auf** | AUFTRAG NR. 16 AN CLAUDE OPUS 5.5 — Entscheidungen, Paket 15b, unser Entwicklungssystem (`AUFTRAG_CLAUDE_NR16_ENTSCHEIDUNGEN_SYSTEM.txt`) mit Anlage `PAKET_15B_PRUEFDATEIEN_20261112.csv` |
| **Für** | Daniel Kössl |

**Kennzeichnung:** [g] gemessen · [r] gerechnet · [a] angenommen · HART · Startwert · UNBEKANNT. Paket 15b habe ich vollständig maschinell ausgewertet [r]: 230 Zeilen, Summe der letzten Dauern 2588,7 s.

---

## 0. Drei Rückmeldungen zu Abschnitt 2

**2a (Tk rundet Pixel auf Punkte): übernommen.** In allen Rezepten unten gilt:
- **Kleintext = 15 px absolut**, gemessen mit `font.measure` vor dem Setzen.
- **Die Regel greift**, wenn measure(name, 15) > Textbreite − 4.
- Folge für dich: schrift(13) = −16 wird zu **17 px**. Breiten in meinen Tabellen sind **Erwartungswerte**; HART ist immer der `font.measure`-Wert zur Laufzeit.

**2b (Völkerfarben): teilweise übernommen, mit Widerspruch nach Regel 5.**
- Meine Angaben „Trolle weiß-gold“ und „Ghule violett“ stammen **von Daniel selbst**, aus seiner Beschreibung der Burgbilder: Trolle mit weiß-goldener Sternburg, Ghule mit violetter Burg und grünen Feuern in Lagern und Dörfern.
- `FRAKTIONEN_WELTEN.md` sagt Dunkelrot/Schwarz bzw. Grün/Knochenweiß.
- **Es gibt also zwei Quellen, die sich widersprechen**, nicht einen Fehler von mir oder von dir. Bei den Ghulen passt nur das Grün der Feuer.
- **Bitte Daniel fragen, welche Quelle führt.** Mein Vorschlag „die Burgbilder geben die Farbe vor“ gilt nur, wenn er die Burgbilder wählt.

**2c:** zur Kenntnis genommen. M11 kommt zuerst; das Rezept steht in Teil B.

---

## TEIL A – Dorfzentrum, baufertig (F-56 bis F-61)

### A1 Vollständige Maßtabelle

**Fall 1:** (1037, 589, k = 1, rb = 17). **Fall 2:** (1127, 764, k = 1,2512, rb = 21).

ls-Werte: Fall 1 aus meinen Messungen mit Liberation Sans, Fall 2 aus deinen Tk-Messungen [g]. Fließtext 15 / 19, Zwischentitel und Zahl 18 / 22, Titel 24 / 30.

| Größe | Formel | Fall 1 | Fall 2 |
|---|---|---|---|
| p | round(8k) | 8 | 10 |
| g | round(6k) | 6 | 8 |
| S_min | round(316k) | 316 | 395 |
| f | min(64, (H − 18) // 10, (W − rb − S_min − 18) // 10) | 57 | 64 |
| R | 10f + 18 | 588 | 658 |
| **S** | W − rb − R | **432** | **448** |
| Textbreite Spalte | S − 2p | 416 | 428 |
| **Kopf** (klebt) | 2p + ls(Titel) + round(4k) + ls(Fließtext) | **59** | **74** |
| **Reiterleiste** | ls(Zwischentitel) + 2p | **34** | **42** |
| Reiterbreite | (R − 2p) // 3 | 190 | 212 |
| **Inhaltshöhe** unter den Reitern | H − Reiterleiste − 2p | **539** | **702** |

**Lager (C1), 17 Waren in 3 Spalten, 6 Reihen, die letzte Reihe mit 2 Kacheln:**

| Größe | Formel | Fall 1 | Fall 2 |
|---|---|---|---|
| Kachelbreite T_w | (R − 4p) // 3 | 185 | 206 |
| Symbol | Bild, wächst nicht | 64 × 56 | 64 × 56 |
| Kachel-Innenabstand | 8, fest wie in Nr. 14 (von dir nachgerechnet) | 8 | 8 |
| Textbreite Kachel | T_w − 16 − 64 − g | 99 | 118 |
| Textblock | 2 × ls(Fließtext) + round(2k) + ls(Zahl) | 50 | 63 |
| T_h | 2p + max(56, Textblock) | 72 | 83 |
| 6 Reihen | 6 T_h + 5p | 472 ≤ 539 ✓ | 548 ≤ 702 ✓ |
| Kleintextregel | measure(name, 15) > Textbreite − 4 | – | „Paladinharnisch“ 104 ≤ 114 ✓ [dein g] |

**Einheiten (C2), 28 Arten in 2 × 14. Verwundete nur als Vorschlag:**

| Größe | Formel | Fall 1 | Fall 2 |
|---|---|---|---|
| Zeilenhöhe z | ls(Zahl) + p | 26 | 32 |
| Tabellenkopf | ls(Fließtext fett) + round(9k) | 24 | 30 |
| Höhe | Tabellenkopf + 14 z | 388 ≤ 539 ✓ | 478 ≤ 702 ✓ |
| Hälftenbreite | (R − 3p) // 2 | 282 | 314 |
| Zahlspalte | round(48k) | 48 | 60 |
| **Name ohne Verwundete (gilt)** | Hälfte − Zahlspalte − p | **226** | **244** |
| Name mit Verwundeten (Vorschlag) | Hälfte − 2 × Zahlspalte − 2p | 170 | 174 |
| „Großer Belagerungsturm“ | gemessen bzw. gerechnet | ≈ 140 bei 13 px [r] ✓ | 180 ≤ 244 ✓ [dein g]; mit Verwundeten Kleintext 162 ≤ 170 ✓ |

**Ohne Verwundete braucht keine Einheit Kleintext.**

**Werkstätten (C3, F-58), 17 Rezepte:**

| Spalte | Formel | Fall 1 | Fall 2 |
|---|---|---|---|
| Name | R − 2p − 3p − (Werkstatt + Zutat + Zustand) | **244** | **228** |
| Werkstatt | round(100k) | 100 | 125 |
| Zutat „[Zutat] [vorhanden] / [nötig] ✓/✕“ | round(120k) | 120 | 150 |
| Zustand „✓ herstellbar“ / „✕ fehlt“ | round(84k) | 84 | 105 |
| Höhe | Tabellenkopf + 17 z | 466 ≤ 539 ✓ | 574 ≤ 702 ✓ |

- Längster Name „Magischer Paladinharnisch“: 198 ≤ 228 ✓ [dein g].
- **Zutatformat:** „Metall 12 / 4 ✓“. Mengen über 99.999 werden nach T08 C2 gekürzt.
- **HART:** measure(Zutattext) ≤ Spalte − 4. Sonst die Mengen kürzen; nie den Zutatennamen.

**Spalte, sieben Blöcke.** h_b = gemessene Knopfhöhe (`winfo_reqheight`). In Fall 2 sind das 37 (Knopf 1) und 35 (übrige) [g]; in Fall 1 ist sie **UNBEKANNT**, bitte messen; erwartet etwa 30 [a].

| # | Block | Formel | Fall 1 | Fall 2 |
|---|---|---|---|---|
| 1 | Kopf | wie oben | 59 | 74 |
| 2 | Nächster Schritt (Knopf 1, Breite S − 2p) | 2p + h_b1 | 16 + h_b1 | 57 |
| 3 | Ort: Eingabefeld round(150k) + „Umbenennen“ | 2p + h_b | 16 + h_b | 55 |
| 4 | Aktionen, 2 Zeilen | 2p + 2 h_b + p | 24 + 2 h_b | 100 |
| 5 | Auswahl je Reiter | Rest | H − Summe | **370** |
| 6 | Hinweis | 2p + 2 ls(Fließtext) | 46 | 58 |
| 7 | Technische Hinweise (nur Entwicklerbetrieb) | 2p + h_b | – | 55 |

**Korrektur meiner Nr. 15:** Block 5 hat **370 px**, nicht 380. Mit Block 5 sind es sechs Blöcke, also **5 Lücken**, nicht 4: 764 − 384 − 10 = 370 [r]. Deine Nachrechnung hatte 380 bestätigt, weil meine Zählung falsch war.

**Bedienelemente:**

| Element | Breite | Höhe | Lage |
|---|---|---|---|
| Knopf 1 „Nächster Schritt“ | S − 2p = 416 / 428 | h_b1 | Block 2 |
| Eingabefeld | round(150k) = 150 / 188 | h_b | Block 3 links |
| „Umbenennen“ | gemessen (100 in Fall 2) | h_b | Block 3, p rechts vom Feld; Summe 298 ≤ 428 ✓ |
| „Karte öffnen“, „Transport“, „Wall verwalten“ (nur mit Wallstufe) | gemessen (94 / 75 / 110) | h_b | Block 4, Zeile 1; 299 ≤ 428 ✓ |
| „Neue Siedlung gründen“ | gemessen (168) | h_b | Block 4, Zeile 2 |
| „Technische Hinweise“ | gemessen (248) | h_b | Block 7, nur im Entwicklerbetrieb |

**Für alle Knöpfe:** Hintergrund E, Rahmen-Frame #b8862e, Text Creme, `disabledforeground` Creme, gesperrt mit „✕ “ plus Wort. **Für das Eingabefeld:** `insertbackground` Creme, Auswahl #b8862e auf #1a0a09.

### A2 Ablage der Werkstatt-Zuordnung (F-61): beide Formen

| | **Form 1: Feld `werkstatt` je Rezept in `warenrezepte.json`** | **Form 2: eigene Datei `data/werkstaetten.json`** |
|---|---|---|
| Aussehen | `"Messer": {"kosten": …, "dauer": …, "voraussetzungen": …, "werkstatt": "schmiede"}` | `{"schmiede": {"waren": ["Messer", …]}, "bogenbauer": {…}, "naehstube": {…}}` |
| Vorteil | **Eine** Stelle je Rezept; eine neue Ware ist ein Eintrag. Keine zweite Liste, die auseinanderlaufen kann (Skill „verbund-konsistenz“). | `warenrezepte.json` bleibt unberührt, ebenso die **6 Prüfdateien**, die sie lesen [r, Paket 15b]. Daniels Begriff „Werkstatt“ wird ein eigener Eintrag; dort kann seine Definition stehen. |
| Nachteil | Die Liste „was macht die Schmiede?“ muss gesammelt werden. 6 Prüfdateien werden von M2 erneut ausgewählt. Ob die Lader unbekannte Felder vertragen, ist UNBEKANNT. | **Zwei Listen**, die zusammenpassen müssen. Das braucht eine Konsistenzwache: jedes Rezept in genau einer Werkstatt, jede Ware mit Rezept. |
| Wache | `werkstatt` ∈ Gebäude-IDs; Zählung 8 / 4 / 5 | Zählung 8 / 4 / 5 + beide Richtungen eindeutig |

**Empfehlung: Form 1.** Der Nachteil von Form 2 ist genau die Fehlerart, die eure Regel „Ablagen dürfen nicht auseinanderlaufen“ verhindern will. Der Wert ist die **Gebäude-ID**. **Keine Umsetzung ohne Daniels Wort.**

### A3 `dorfzentrum_kennzahlen` (F-60)

**Signatur:** `dorfzentrum_kennzahlen(ort, forschung) -> dict` in `src/spieloekonomie.py`.

| Schlüssel | Bedeutung | Gezählt wird |
|---|---|---|
| `vorraetig` | Waren mit Bestand > 0 | über alle Einträge aus `items.json` |
| `waren_gesamt` | Anzahl der Waren | `len(items)`, **keine 17 im Code** |
| `herstellbar` | Waren, die der Ort jetzt herstellen kann | `ware_grenzen(ort, ware, forschung) > 0` je Rezept |
| `rezepte_gesamt` | Anzahl der Rezepte | `len(warenrezepte)` |
| `einheiten` | Summe aller Einheiten im Ort | Bestände |
| `einheiten_arten` | Arten mit Bestand > 0 | – |

Die Ansicht **formatiert** nur, zum Beispiel „[vorraetig] von [waren_gesamt] vorrätig“.

**Wache `test_dorfzentrum_kennzahlen.py`** (Rechnen, Stufe 1):
1. Leerer Ort → alle Zählwerte 0, `waren_gesamt` = `len(items)`.
2. **Bauweise ohne Tautologie:** ein Ort mit genau **einer** Ware auf Lager und genau so viel Rohstoff, wie **ein** bekanntes Rezept braucht. Die erwarteten Zahlen stehen **von Hand** in der Wache (`vorraetig` = 1, `herstellbar` = 1). **Nicht** `ware_grenzen` noch einmal aufrufen und vergleichen; das wäre die Spiegelwache aus deinem Abschnitt 4.4.1.
3. **Gegenprobe:** dieselbe Ware auf 0 gesetzt → `vorraetig` = 0.
4. `test_quelle_ast` prüft, dass die Ansicht kein `len()` und kein `sum()` über Lager oder Einheiten aufruft.

### A4 Werteblock zum maschinellen Nachrechnen (neu, siehe C2)

```
name;formel;fall1;fall2
p;round(8*k);8;10
S_min;round(316*k);316;395
f;min(64,(H-18)//10,(W-rb-S_min-18)//10);57;64
R;10*f+18;588;658
S;W-rb-R;432;448
kopf;2*p+ls_titel+round(4*k)+ls_text;59;74
reiter;ls_zw+2*p;34;42
innen;H-reiter-2*p;539;702
T_w;(R-4*p)//3;185;206
T_h;2*p+max(56,2*ls_text+round(2*k)+ls_zahl);72;83
lager_hoehe;6*T_h+5*p;472;548
z;ls_zahl+p;26;32
einh_hoehe;tkopf+14*z;388;478
einh_name;(R-3*p)//2-round(48*k)-p;226;244
werk_name;R-5*p-round(100*k)-round(120*k)-round(84*k);244;228
werk_hoehe;tkopf+17*z;466;574
block5;H-(kopf+57+55+100+58)-5*p;-;370
```

Eingaben Fall 1: W = 1037, H = 589, k = 1, rb = 17, ls_text = 15, ls_zw = ls_zahl = 18, ls_titel = 24, tkopf = 24. Fall 2: W = 1127, H = 764, k = 1,2512, rb = 21, ls_text = 19, ls_zw = ls_zahl = 22, ls_titel = 30, tkopf = 30.

---

## TEIL B – Die vier Kernmaßnahmen, baufertig (F-62)

### Befund aus Paket 15b, der alle vier betrifft

**`test_textqualitaet` hat 0 Läufe in der Historie, war aber im Sammellauf um 22:18 rot.** Daraus folgt:
- **„Keine Historie“ heißt nicht „läuft nie“, sondern „schreibt nichts in den Index“.** Die 46 blinden Flecken sind eine **Lücke im Aufzeichnen**.
- Die billigste Abhilfe: **Der Sammellauf schreibt selbst eine Zeile je Datei**, unabhängig davon, ob die Prüfdatei den harness richtig benutzt.

Das ist der Unterbau für M12 (Schritt M12.0).

**Weiterer Befund:** `main` steht in **184 von 230** Dateien in `src_module` [r]. Eine Auswahl nach Modul allein würde bei jeder Änderung an `main.py` 184 Dateien ziehen. **M2 muss deshalb für `main.py` nach Funktionen auswählen.**

### M11 – Faktenblatt

- **(a)** `tools/faktenblatt.py` erzeugt `docs/FAKTENBLATT.md` (für Aufträge) und `docs/faktenblatt.json` (für Wachen). Inhalt, je Zahl mit **Quelldatei**:
  - Waren (`items.json`), Rezepte, höchste Zutatenzahl je Rezept, Menge der Zutaten (holz, metall, wolle, leder), Waren ohne Rezept,
  - Einheiten, Forschungen, Gebäude je Rubrik, Völker, Welten mit Heimatwelt, Geländearten,
  - Werkstatt → Waren (sobald F-61 gebaut ist; bis dahin „UNBEKANNT – nur Fließtext in `buildings.json`“),
  - Commit-Hash des letzten Commits in `data/` und das Datum.

  Längste Namen in px **nur**, wenn Tk verfügbar ist. Sonst wird der Abschnitt weggelassen und ausdrücklich als fehlend vermerkt.
- **(b)** Von Hand geschriebene Zahlen in Aufträgen (deine Belegstelle 2c).
- **(c)** Funktionen: `zaehlen(daten_ordner) -> dict` (rein, ohne Tk), `als_markdown(d) -> str`, `schreiben(d, md_pfad, json_pfad)`. **Sortierung fest**, kein Zufall. Die Auftragsvorlage (`docs/auftraege/AUFTRAGS_VORLAGE.md`) bekommt einen Abschnitt „Faktenblatt (automatisch, nicht von Hand ändern)“, in den die Datei eingefügt wird.
  - Dazu `tools/auftrag_pruefen.py`: Es sucht in einem Auftragstext Muster wie „[Zahl] Waren / Rezepte / Einheiten / Forschungen / Gebäude / Zutaten“ und **warnt bei Abweichung** vom Faktenblatt.
- **(d)** Wache `tests/test_faktenblatt.py` (Rechnen, Stufe 1):
  1. `zaehlen(data)` = Inhalt von `docs/faktenblatt.json`, sonst rot mit dem Hinweis „Faktenblatt veraltet: `tools/faktenblatt.py` laufen lassen“.
  2. **Gegenprobe:** `data/` in einen Arbeitsordner kopieren, eine Ware ergänzen → `zaehlen` meldet 18.
  3. `auftrag_pruefen` findet in einem Probetext „18 Waren“ eine Abweichung.
- **(e)** ≈ 0,5 s [a].

### M1 – Kopfangaben je Prüfdatei (rückwärtsverträglich)

**(a) Format:** vier Zuweisungen am Dateianfang, nur ASCII:

```
PRUEF_ART = "fenster"            # rechnen | fenster | quelltext, optional "+messen"
PRUEF_STUFE = 2                  # 1..4
PRUEF_BETRIFFT = ["main:_render_settlement_map", "hintergrund_optik"]   # Modul oder Modul:Funktion
PRUEF_DATEN = ["gelaende.json"]
```

Gelesen wird **per `ast.literal_eval`**, ohne die Datei zu importieren.

**Fehlt der Kopf, gelten Ersatzwerte (rückwärtsverträglich):**
- **Art:** „fenster“, wenn `tkinter` importiert wird, sonst „rechnen“.
- **Stufe:** 3.
- **Betrifft:** alle `src`-Modulnamen, die im Dateitext vorkommen (so ist vermutlich `src_module` in Paket 15b entstanden).
- **Daten:** alle `*.json`-Namen im Text.

`harness.kopf_lesen(pfad)` liefert dazu `kopf_fehlt = True`. **Alte Dateien laufen unverändert.**

- **(b)** Ohne diese Angaben gibt es keine Stufenwahl und keine gezielte Auswahl.
- **(c)**
  - `tests/harness.py`: `kopf_lesen(pfad) -> dict`.
  - `tools/kopf_vorschlag.py` schreibt **Vorschläge** aus Paket 15b (`art`, `src_module`, `daten`) als Kopf in die Dateien, **in Paketen zu 20 mit T2 nach jedem Paket**. Erst die Stufe-1-Kandidaten, dann der Rest.
  - **Startstufe:**
    - 1 = Rechnen oder Quelltext unter 2 s,
    - 2 = Fenster bis 20 s oder Rechnen ab 2 s,
    - 3 = Rest,
    - 4 = die T4-Liste aus Punkt 7.
- **(d)** Metawache `tests/test_pruefstand_kopf.py`:
  - **Befund** je Datei ohne Kopf; die Zahl wird als Messwert geführt und soll fallen.
  - **HART** nur für Dateien, die **nach dem Stichtag neu angelegt** wurden (`git log --diff-filter=A`).
  - **Gegenprobe:** eine Probedatei ohne Kopf mit Anlagedatum nach dem Stichtag → rot.
- **(e)** ≈ 1 s für 230 Dateien [a].

### M2 – Auswahl nach Änderung

- **(a)** Gelaufen werden nur die betroffenen Dateien.
- **(b)** Kein 23-Minuten-Lauf nach jeder Kleinigkeit, aber auch keine 184 Dateien bei jeder Zeile in `main.py`.
- **(c)** `tools/auswahl.py` mit der reinen Funktion `auswahl(aenderungen, koepfe, aufrufer, hubs) -> (dateien, empfohlene_stufe)` und dem dünnen Git-Teil `aenderungen_seit(commit)`. Der Sammellauf merkt sich den **Commit des letzten grünen T3- oder T4-Laufs** in `index.json`.

**Die Regel in Worten:**
1. Änderung **nur in `docs/`** (außer dem Protokoll) → nur die Metawachen (T1).
2. Änderung an `tests/harness.py` oder `tools/sammellauf.py` → **T3**, denn der Prüfstand selbst ist berührt.
3. Geänderte Prüfdatei → läuft selbst.
4. Geänderte Datei in `data/` → alle Dateien mit dieser Datei in `DATEN`.
5. Geändertes Modul `x` (nicht `main`) → alle Dateien mit `x` in `BETRIFFT`.
6. **`main.py`:** Die geänderten **Funktionen** werden bestimmt (Zeilen aus `git diff -U0` den umgebenden `def` per AST zuordnen, im alten **und** im neuen Stand). Ausgewählt werden Dateien mit `main:<funktion>` in `BETRIFFT` **oder**, solange der Kopf fehlt, Dateien, deren **Text den Funktionsnamen enthält**.
   - **Liegt eine Änderung außerhalb jeder Funktion** (Modulebene, Importe, Konstanten), wird T3 empfohlen.
7. **Eine Stufe Aufrufer:** Für jedes geänderte Modul `x` **außer `main` und außer Hubs** kommen die Module dazu, die `x` importieren (aus `modulkarte`, ohne `main`), und davon **nur Dateien der Stufen 1 und 2**.
   - **Hubs** sind Module mit mehr als 25 Dateien in `BETRIFFT`. Laut Paket 15b [r]: einheiten 86, spieloekonomie 60, gelaende 45, auftraege 31, punkte 30, kampf 27, forschung 27, botkern 26. Für sie gilt keine Aufruferstufe, nur die direkten Dateien.
8. **Deckel:** Liegt die geschätzte Dauer der Auswahl über 120 s (Summe der Mediandauern aus M12), läuft sie **nicht stillschweigend**. Ausgegeben wird „Auswahl [n] Dateien, [s] s > 120 s → T3 empfohlen“, und Weltenfresser entscheidet.

**Pseudocode:**

```
def auswahl(aenderungen, koepfe, aufrufer, hubs):
    if alle(p.startswith("docs/") and p != PROTOKOLL for p in aenderungen.pfade):
        return META, 1
    if aenderungen.beruehrt("tests/harness.py", "tools/sammellauf.py"):
        return ALLE_AUSSER_T4, 3
    dateien = set(aenderungen.pruefdateien)
    for d, kopf in koepfe.items():
        if kopf.daten & aenderungen.datendateien: dateien.add(d)
        for b in kopf.betrifft:
            mod, _, fn = b.partition(":")
            if mod == "main":
                if aenderungen.main_modulebene: return ALLE_AUSSER_T4, 3
                if fn in aenderungen.main_funktionen: dateien.add(d)
                if not fn and kopf.kopf_fehlt and text_enthaelt(d, aenderungen.main_funktionen): dateien.add(d)
            elif mod in aenderungen.module:
                dateien.add(d)
    for x in aenderungen.module - {"main"} - hubs:
        for y in aufrufer.get(x, set()) - {"main"}:
            dateien |= {d for d, k in koepfe.items() if y in k.module and k.stufe <= 2}
    dateien |= META
    return dateien, 2
```

- **(d)** Wache `tests/test_auswahl_m2.py` (Rechnen, Stufe 1) mit **erfundenen** Köpfen und Änderungen, ohne Git:
  1. Nur Kommentar in `src/welt.py` → enthält die Dateien mit `welt`, **nicht** die 184 mit `main`.
  2. Änderung in `main._render_settlement_map` → enthält `test_siedlungsansicht_a9` und `_a10`, **nicht** `test_tor`.
  3. `data/items.json` → genau die Dateien mit `items.json` in `DATEN`.
  4. Leere Änderung → nur `META`.
  5. **Gegenprobe:** eine Änderung auf Modulebene von `main` → Stufe 3.
- **(e)** ≈ 2 s; das AST von `main.py` zweimal zu lesen ist der größte Anteil (UNBEKANNT, bitte messen).

### M12 – Rot-Historie

- **M12.0 (Unterbau, zuerst):** `tools/sammellauf.py` hängt je Datei und Lauf **eine Zeile** an `docs/audits/laeufe.jsonl` an: Datei, Zeit, Commit, Stufe, Rückgabecode, bestanden, Fehler, Befunde, Dauer, `parallel = N`, `allein = ja/nein`. Die Zeile entsteht **aus dem Prozessergebnis**, nicht aus dem harness. Damit sind die 46 Lücken auf einen Schlag geschlossen.
- **(a)** `tools/rot_historie.py` liest **nur** `laeufe.jsonl` (eine Datei statt zehntausender JSON-Dateien) und schreibt `docs/audits/ROT_HISTORIE.md` und `.csv` mit vier Listen:
  1. **Kandidat höhere Stufe:** ≥ 30 Läufe, 0 rot, Mediandauer ≥ 10 s **allein gemessen**, keine Datei aus `BETRIFFT` in den letzten 14 Tagen geändert.
  2. **Wackelkandidat:** rot und danach grün **beim selben Commit**. Das ist kein Codefehler, sondern ein Messumstand (wie `test_weltkarte_malerei`).
  3. **Nie aufgezeichnet:** 0 Zeilen.
  4. **Teuer je Fund:** Dauer × Läufe / (Rotfunde + 1), die obersten 10.
- **(b)** Die Frage, was seltener laufen darf, und die Frage, was wackelt.
- **(c)** reine Funktion `auswerten(zeilen, aenderungsdaten) -> dict` plus Ein- und Ausgabe.
- **(d)** Wache `tests/test_rot_historie.py` mit erfundenen Zeilen:
  - 31 grüne Läufe → Kandidat; **Gegenprobe:** 29 grüne Läufe → kein Kandidat.
  - rot und dann grün beim selben Commit → Wackelkandidat.
- **(e)** < 1 s bei einigen tausend Zeilen [a].

### Punkt 7 – die 39 Kandidaten aus Paket 15b

**Vorsicht:** Die Dauern in Paket 15b sind **unter 2-facher Last** gemessen. `test_produktionskette_ohne_cheats` stand in Nr. 15 noch mit 72 s, hier mit 301 s. Erst M12.0 mit `allein = ja` liefert belastbare Dauern.

**Nach T4 schieben** (vor jeder EXE und wöchentlich; zusätzlich über M2, wenn ihre Funktionen berührt sind). Zusammen 660 s = **25 % der Summe** [r]:

| Datei | Dauer [g] | Prüfungen | Risiko |
|---|---|---|---|
| `test_produktionskette_ohne_cheats` | 301,2 | 48 | Ein Bruch der Gesamtkette fällt bis zu einer Woche später auf; M2 fängt direkte Treffer. |
| `test_durchspiel` | 65,7 | 64 | wie oben |
| `test_overlay_ingame` | 57,9 | 42 | Overlay ändert sich selten. |
| `test_doppelpuffer` | 54,3 | 15 | 3,6 s je Prüfung; Flackern ist selten berührt. |
| `test_bot_gruendung` | 53,5 | 36 | **Art prüfen:** als „quelltext“ eingetragen, aber 53 s lang. Das deutet auf eine Simulation hin. |
| `test_bot_takt_scheiben` | 44,1 | 34 | **Art prüfen**, wie oben |
| `test_bot_warenkette` | 42,5 | 37 | Bot-Wirtschaft |
| `test_kaserne_ohne_gebaeude` | 41,4 | 11 | 3,8 s je Prüfung |

**Nur bei Änderung laufen lassen:**

| Datei | Regel | Ersparnis |
|---|---|---|
| `test_protokoll` (22,4 s, 205 Läufe, nie rot, kein `src`-Modul) | `PRUEF_DATEN` = die Protokolldatei; läuft **nur**, wenn sie geändert wurde | 22,4 s in jedem anderen Lauf |

**Zusammenlegen** (nicht streichen; Ersparnis = Programmstarts):

| Gruppe | Dauer [g] | Vorschlag | Ersparnis |
|---|---|---|---|
| Startweg: `test_startseite` 11,1 · `test_startspiel` 34,9 · `test_startkartenwahl` 11,8 · `test_voelkerwahl` 15,6 (dazu `test_tor` 49,8, `test_startbilder` 2,1) | 125,3 | eine Datei `test_startweg`, die den Startweg **einmal** in einem Fenster durchgeht und an jedem Schritt prüft | UNBEKANNT; bitte die Startzeit der App einzeln messen |

**Streichen nach Abgleich** (mit Daniels Freigabe; Regel 4: Löschen nur mit Freigabe). Vorgehen: die Prüfnamen beider Dateien vergleichen; deckt die neue mindestens 90 % der Eigenschaften ab, wird gestrichen.

| Datei | ersetzt durch | Zeitpunkt |
|---|---|---|
| `test_ressourcenleiste` (10,0 s) | `test_ressourcenleiste_t08` (119 Prüfungen) | jetzt prüfbar |
| `test_ansicht_hintergrund` (36,0 s) | `ansicht_geruest` + Ansichtswachen | wenn die letzte Ansicht umgestellt ist |
| `test_bot_wappen` (10,6 s) | Markerwache nach C1 Teil 2 (das Wappenabzeichen entfällt, Nr. 10) | nach dem Bau |
| `test_dorfzentrum_ist_lager` (17,5 s) | neue Dorfzentrumswache nach Nr. 14 / 16 | beim Umbau umschreiben, nicht doppelt führen |

**Bleiben in T3** (alle übrigen der 39): Sie werden über M2 gezielt gezogen, wenn ihre Module oder Funktionen berührt sind.

**Unabhängig von den 39:** `test_portal_kopfleiste` war **13 von 46** Mal rot, `test_weltkarte_rahmen` 6 von 64 Mal [g]. Bevor sie irgendwohin verschoben werden: Wackelprüfung (C4).

---

## TEIL C – Verbesserungen am Entwicklungssystem (höchstens zehn)

**C1 Entscheidungen ohne Zeitablauf**
1. Was: Daniels Entscheidungen kommen als Datei `docs/entscheidungen/OFFEN_<Datum>.md`, je Frage eine Zeile mit Ankreuzfeldern. Hermes liest sie beim nächsten Schritt; es gibt nie ein Formular mit Ablaufzeit.
2. Mangel: Zweimal sind acht Klickantworten verloren gegangen (deine Belegstelle 4.4.6).
3. Bau: Vorlage plus `tools/entscheidungen_lesen.py`, das ausgefüllte Zeilen in die F-Nummern des Registers überträgt.
4. Prüfung: Jede F-Nummer im Register verweist auf eine Zeile in einer Entscheidungsdatei. Eine Metawache zählt Verweise ohne Quelle (Soll 0).
5. Kosten: ≈ 0 s; einmal die Vorlage.

**C2 Werteblock in jeder Antwort eines starken Modells**
1. Was: Antworten mit Maßen enthalten einen Block `name;formel;fall1;fall2`, wie Teil A4 dieser Antwort.
2. Mangel: Die Nachrechnung von Hand kostet dich Zeit, und Rechenfehler wie meine 380 statt 370 rutschen durch.
3. Bau: `tools/opus_nachrechnen.py` liest den Block, rechnet jede Formel mit den genannten Eingaben nach und meldet Abweichungen.
4. Prüfung: Ein absichtlich falscher Wert im Block wird gemeldet.
5. Kosten: < 1 s je Antwort. **Ich liefere den Block ab jetzt immer.**

**C3 SKILL.md an der Größengrenze**
1. Was: SKILL.md (100 867 Zeichen) wird in einen **Kern** (die 9 Regeln, Verfahren, ein Index „Stichwort → Referenzdatei“) und die vorhandenen 33 Referenzdateien geteilt. Zielgröße des Kerns: Startwert 30 000 Zeichen.
2. Mangel: An der Grenze kann keine Lehre mehr hinein, ohne eine alte zu verdrängen. Bei jedem Laden kostet ein großer Kern ein kleines Modell Kontext, und die Regeln, auf die es ankommt, gehen darin unter.
3. Bau: Umbau nach Regel 9: protokolliert, mit Hash vorher und nachher, Rückrollweg, Daniels Freigabe.
4. Prüfung: Metawache: Größe des Kerns ≤ Grenze, jede Referenzdatei steht im Index, kein Abschnitt doppelt.
5. Kosten: einmalig; danach weniger Kontext je Aufruf (UNBEKANNT wie viel, bitte messen).

**C4 Wackelwachen erkennen statt Vertrauen verlieren**
1. Was: Wird eine Datei unter Parallellast rot, startet der Sammellauf sie **sofort einmal allein** neu. Ist sie dann grün, gilt sie als „wackelt“ (eigener Status, nicht grün und nicht rot) und kommt in den M12-Bericht.
2. Mangel: `test_weltkarte_malerei` (4,5 s unter Last, 0,56 s allein) und die 13 roten Läufe von `test_portal_kopfleiste`.
3. Bau: `tools/sammellauf.py`; Status `wackelt` in `laeufe.jsonl`.
4. Prüfung: Eine Probedatei, die nur bei gesetzter Umgebungsvariable `NEBEL_LAST` rot wird, erscheint als „wackelt“.
5. Kosten: nur bei Rot, die Dauer der einen Datei.

**C5 Wanduhrwachen auf Prozesszeit umstellen**
1. Was: Zeitgrenzen messen `time.process_time()` statt der Wanduhr und prüfen mit Korridor (M5 `check_korridor`).
2. Mangel: Zeitwachen reißen unter Last (deine Belegstelle 4.4.4).
3. Bau: `harness.zeit_messen(fn) -> (prozess_s, wand_s)`; die Wache prüft nur `prozess_s`, `wand_s` wird als Messwert geführt.
4. Prüfung: dieselbe Wache mit `-j 2` und `-j 1` → gleiches Urteil.
5. Kosten: ≈ 0 s. Grenze: Wartezeiten in Tk (`after`) misst die Prozesszeit nicht. Diese Wachen bleiben Wanduhr mit **dreifachem** Korridor (Startwert).

**C6 `main.py` schrumpfen, gemessen**
1. Was: Jeder Umbau zieht einen Baustein aus `main.py` in ein eigenes Modul (wie `ansicht_geruest.py`). Gemessen wird die Zahl der Prüfdateien mit `main` in `BETRIFFT`.
2. Mangel: 184 von 230 Dateien hängen an `main` [r]. Darum ist jede Änderung dort teuer zu prüfen.
3. Bau: kein eigener Auftrag, sondern eine Regel „beim Berühren herausziehen“ in den Skill-Abschnitt „Drei Regeln bei jedem Umbau von `main.py`“.
4. Prüfung: Messwert „Dateien mit `main`“ je Woche; der Trend soll fallen.
5. Kosten: 0 s je Lauf.

**C7 Regel 2 um „gekennzeichnete Startwerte“ ergänzen**
1. Was: Ergänzung zu Regel 2: **„Ein Startwert ist kein Raten, wenn er als [a] oder Startwert gekennzeichnet ist und eine Messung benannt ist, die ihn ersetzt.“**
2. Mangel: Regel 2 („ein geratener Wert, der zufällig stimmt, ist genauso ein Fehler“) passt wörtlich nicht zu Gestaltung, die ohne Startwerte nicht anfangen kann. Seit Nr. 11 arbeiten wir faktisch schon so. **Diese Regel steht dem Bauen im Weg, solange sie das nicht sagt.**
3. Bau: Regeltext ändern nach Regel 9, mit Daniels Freigabe.
4. Prüfung: Jeder Startwert im Register hat ein Feld „ersetzt durch Messung am …“ oder „offen“. Eine Metawache zählt offene Startwerte, die älter als 14 Tage sind.
5. Kosten: 0 s.

**C8 Lehre → Wache, wo es geht**
1. Was: Jede Lehre im Skill bekommt das Feld `wache:` mit dem Namen der Prüfung, die sie mechanisch absichert, oder `wache: keine (nicht prüfbar)`.
2. Mangel: Lehren wie „Entscheidungen nie mit Zeitablauf“ standen schon im Skill und wurden trotzdem verletzt.
3. Bau: Feld in allen Lehren nachtragen, beim Berühren.
4. Prüfung: Messwert „Anteil Lehren mit Wache“. Jede genannte Wache existiert.
5. Kosten: 0 s je Lauf.

**C9 „Sammellauf nach dem letzten Fix“ an die Stufe binden**
1. Was: Die Konvention gilt **je Stufe**: Nach dem letzten Fix muss die **gewählte Stufe** gelaufen sein, nicht immer der volle Lauf. Vor einer EXE bleibt T4 HART.
2. Mangel: 23 Minuten nach jeder Kleinigkeit kosten Daniels knappste Ressource, die Zeit.
3. Bau: Text in `pruefstand-konventionen.md` und die Stufe in `laeufe.jsonl`.
4. Prüfung: Die Abgabe einer EXE prüft, ob der letzte T4-Lauf nach dem letzten Commit liegt.
5. Kosten: 0 s.

**C10 Die 46 alten Dateien einmal sichten**
1. Was: Nach M12.0 läuft jede der 46 Dateien **einmal allein**. Ergebnis je Datei:
   - **grün** → bleibt, Kopf nach M1;
   - **Absturz** → reparieren oder Streichantrag an Daniel;
   - **prüft nichts mehr Gültiges** (alte Fixrunden „fix04…“) → Streichantrag.
2. Mangel: 34 der 46 sind alte „gpt_“-Dateien [r]. Ob sie noch etwas Gültiges prüfen, weiß niemand.
3. Bau: `tools/einzeln_sichten.py` schreibt eine Tabelle für Daniel.
4. Prüfung: Nach der Sichtung hat jede Datei eine Zeile in `laeufe.jsonl` oder ist gestrichen.
5. Kosten: einmalig, Summe der Einzeldauern (UNBEKANNT).

---

## Was ich nicht geprüft habe

- **Knopfhöhe** h_b in Fall 1 (k = 1).
- **Startzeit der App** je Fensterwache. Davon hängt die Ersparnis durch Zusammenlegen ab.
- **AST von `main.py`:** wie lange das Lesen dauert (M2).
- **Lader:** ob sie ein unbekanntes Feld `werkstatt` in `warenrezepte.json` vertragen (Form 1).
- **Die beiden „quelltext“-Dateien mit über 40 s:** was sie tatsächlich tun.
- **Allein-Dauern:** Alle Dauern in Paket 15b sind unter Last gemessen.

---

## Zusatzinformationen (nicht beauftragt)

> Hinweise, keine Anweisungen.

**Z1 Reihenfolge für morgen** (Vorschlag, Daniel entscheidet):
1. **M12.0** (eine Zeile je Datei im Sammellauf, schließt die 46 Lücken),
2. **M11**,
3. **M1** (nur die Lesefunktion und die Metawache als Befund),
4. **M2**,
5. erst dann die Köpfe in Paketen.

Grund: M2 braucht die Köpfe, M12 braucht M12.0, und M11 ist unabhängig und am billigsten.

**Z2 Die Zahl, die du dir merken solltest: 184 von 230.** Solange fast alles an `main` hängt, ist jede Auswahl nach Modul wertlos. Die Auswahl nach Funktion (M2, Regel 6) ist deshalb kein Zusatz, sondern der Kern.

**Z3 Werteblöcke auch in deinen Aufträgen.** Was ich dir in C2 anbiete, geht auch umgekehrt: Wenn Aufträge ihre Messwerte als Block `name;wert;quelle` mitschicken, kann ich sie direkt einsetzen. Dann wandern keine abgetippten Zahlen mehr in meine Rezepte.

**Z4 Zu Regel 5:** Deine Widersprüche in Nr. 13 bis 16 waren in der Sache fast immer richtig: Zeilenhöhen, Paladinharnisch, Zutaten, Punkt-Rundung in Tk. In zwei Fällen lag die Ursache in der Vergleichsgrundlage (Punktlisten, Nr. 14 Z1) bzw. in einer zweiten Quelle (Farben, oben 2b). **Beides lässt sich an derselben Frage erkennen: „Womit habe ich verglichen?“** Diese Frage gehört vielleicht in den Skill-Abschnitt zur Nachrechnung.

---

Ende der Antwort auf Auftrag Nr. 16.
