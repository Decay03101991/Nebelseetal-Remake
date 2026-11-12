# NACHTPLAN Sitzung 41 — 12.11.2026 ab 23:1x

> **Wozu diese Datei:** Sie ist die kurze Fassung der Übergabe `UEBERGABE_NEBELSEETAL_20261112_2302.md`.
> Wenn der Kontext in Sitzung 41 volläuft, ist **diese** Datei der Einstieg: klein, vollständig,
> ohne Verweis auf den Sitzungsverlauf. Nach **jedem** abgeschlossenen Schritt wird sie abgehakt
> (`[x]` + Register + Commit), damit ein Neustart nie mehr als einen Schritt verliert.

**Auftrag Daniel (12.11.2026, 23:0x):** „die antwort von claude ist bereits da, einfach an die neue
session übergeben das zu bearbeiten und abzulegen“ und „In der kommenden Session muss möglichst viel
durchgearbeitet werden, da ich mich jetzt schlafen lege und erst morgen um 7.55 Uhr zurück am pc bin.“
**Fragen an ihn werden gesammelt** (`docs/FRAGEN_AN_DANIEL_20261112.md`), nicht gestellt.

**Skill-Freigabe:** Daniel hat sie der Sitzung 41 erteilt — **vorsichtig** anwenden (Abschnitt 5).

---

## 0. Reihenfolge (nicht umstellen)

| | Schritt | Fertig, wenn |
|---|---|---|
| **0** | Übergabe + diese Datei lesen, Hash prüfen, Desktop-Kopie räumen, Sitzung umbenennen | ein Satz an Daniel, Registerzeile |
| **1** | **Antwort Nr. 16 ablegen und nachrechnen** (`ANTWORT_NR16_CLAUDE.md` im Übergabe-Ordner) | `docs/eingaenge/CLAUDE_20261112_ENTSCHEIDUNGEN_NR16/` mit Antwort + `NACHRECHNUNG_NR16.md`, zwei Registerzeilen, gepusht |
| **2** | **F-57** Abstand = gemessener Rollbalken → **S = 448** | `siedlungs_masse` liefert 448 bei (1127, 764); `test_siedlungsansicht_a9` **und** `test_dpi_f51` nachgezogen und grün; Gegenprobe rot |
| **3** | **F-60** `dorfzentrum_kennzahlen(ort, forschung)` (Rezept: Nr. 16, A3) | Funktion + `test_dorfzentrum_kennzahlen` grün, ohne Tautologie (erwartete Zahlen von Hand), Gegenprobe rot |
| **4** | **M12.0** Sammellauf schreibt `docs/audits/laeufe.jsonl` (eine Zeile je Datei/Lauf) | nach einem kleinen Lauf hat **jede** gefundene Datei eine Zeile — die 46 blinden Flecken sind zu |
| **5** | **M11** `tools/faktenblatt.py` → `docs/FAKTENBLATT.md` + `.json` | Wache `test_faktenblatt` grün; Gegenprobe (Ware dazu) meldet 18 |
| **6** | **M1** Kopfangaben je Prüfdatei, **in Paketen von 20** | Metawache meldet anfangs nur einen **Befund**; nach jedem Paket die betroffenen Wachen grün |
| **7** | **M2** Auswahl nach `git diff` (Regel 6: `main.py` nach **Funktionen**) → danach **F-63** Stufen T1–T4 | `test_auswahl_m2` grün mit den fünf Fällen aus Nr. 16; ein echter Lauf wählt sichtbar weniger als 230 |
| **8** | **Dorfzentrum** nach Nr. 16 Teil A (F-56 absolut 15 px, F-58 Zutat-Spalte, F-59 kein Ortsbestand) | neue Dorfzentrumswache grün, Belegbild unter `docs/audits/` |

**Zwischen jedem Schritt:** Registerzeile, Commit, Push, und **diese Datei abhaken**. Vor dem Morgen
**ein voller Sammellauf** (T3/T4), damit Daniel einen belegten Stand vorfindet.

---

## 1. Die Entscheidungen, die gebaut werden (Kurzfassung, F-56 bis F-72)

- **F-56** Kleintext = **15 px absolut** (nicht `schrift(15)`; das wären 19 px und zu breit).
- **F-57** `SIEDLUNGS_ABSTAND` und `SIEDLUNGS_ROLLBALKEN` entfallen, `rb` wird gemessen: **S = 448** / 432.
- **F-58** Werkstätten zweigeteilt, statt „Bestand“ eine **Zutat-Spalte** (228 / 125 / 150 / 105).
- **F-59** Ortsbestand bleibt in der Siedlungskarte; das Dorfzentrum bekommt die sieben Blöcke.
- **F-60** `dorfzentrum_kennzahlen` — Ökonomie zählt, Ansicht formatiert.
- **F-61** Werkstatt = Schmiede, Bogenbauer, Nähstube; **Pferde, Wolle, Leder sind Rohstoffe**.
- **F-62** Prüfstand-Kern M11, M1, M2, M12 zuerst.
- **F-63** Stufen T1–T4 nach M1/M2; **T4 vor jeder EXE ist HART**.
- **F-64** Werkstatt-Zuordnung als **Feld `werkstatt` je Rezept** in `warenrezepte.json` (Gebäude-ID).
- **F-65** Einheitentabelle **ohne Spalte „Verwundete“** (Namensspalte 244, kein Kleintext nötig).
- **F-66** Kopf-Kennzahl = **beide Warenzahlen** („x von 17 vorrätig · y von 17 herstellbar“).
- **F-67** Prüfstand entschlacken: 8 lange Dateien nach T4, `test_protokoll` nur bei Änderung, vier
  Startdateien zusammenlegen — **Löschen nur mit Daniels Wort**.
- **F-68** Rollbalken **in den Skin-Ton** einfärben (nicht mehr `#f0f0f0`).
- **F-69** Panel-Farbe bleibt **`#291b18`**.
- **F-70** Portalsprung-Zahlen **später**.
- **F-71** **Burgbilder geben die Farbe vor**; `FRAKTIONEN_WELTEN.md` wird angepasst.
- **F-72** **C7 und C3 freigegeben** (Regel 2 ergänzen, `SKILL.md` teilen) — mit Protokoll nach Regel 9.

**Offen (kein F):** Daniels **eigene Sichtprüfung** der zwei DPI-Belegbilder — bis dahin nichts ändern.

## 2. Zahlen, die NICHT neu gemessen werden müssen

| Größe | Wert | Beleg |
|---|---|---|
| k (DPI-bewusst) | **1,2512** | `test_dpi_f51` |
| Fenster / Fläche | **1560 × 940** / **1127 × 764** | dieselbe Wache |
| Feld / Karte / Spalte | 64 / 658 / 453 (nach F-57: **448**) | `siedlungs_masse` |
| Rollbalken | **21 px** | eigene Messung |
| Zeilenhöhen | 16 px = 19 · 19 px fett = 22 · 25 px fett = 30 | eigene Messung |
| Textbreiten | Paladinharnisch 117 (16 px) / **104** (15 px) · Belagerungsturm 180 / **162** | eigene Messung |
| Waren / Rezepte / Zutaten je Rezept | 17 / 17 / **1** | `data/items.json`, `warenrezepte.json` |
| Werkstätten | 3 (Schmiede 8, Bogenbauer 4, Nähstube 5) | `buildings.json` |
| Dorfzentrum-Inhalt heute | **2044 px** | `dpi_probe_s40.py` |
| Knöpfe / Eingabefelder | 7 / 1 | `messe_dorfzentrum_f2_f7.py` |

---

## 3. Was NICHT getan wird

- **Keine** Fragen an Daniel in der Nacht — sammeln, eine Runde bei seiner Rückkehr.
- **Kein** Umbau der Völkerfarben ohne Daniels Sichtprüfung (F-71 sagt: Burgbilder führen).
- **Keine** Streichung von Prüfdateien ohne Daniels Wort (Regel 4).
- **Kein** „alle 230 Köpfe auf einmal“ — Pakete von 20, wie Claude es begründet.
- **Keine** Entscheidung mit Zeitablauf (Formular).

---

## 4. Wenn der Kontext volläuft

1. **Sofort** diese Datei abhaken, was fertig ist, und `docs/AKTUELLER_STAND.md` (oberster Block)
   auf den Stand bringen — beides committen und pushen, **bevor** weitergearbeitet wird.
2. Reicht der Kontext nicht mehr für einen Schritt: **Schritt nicht anfangen.** Lieber einen sauberen
   Stand als einen halben Umbau.
3. Der nächste Start liest: **diese Datei zuerst**, dann `docs/AKTUELLER_STAND.md`, dann das Register
   ab der letzten Zeile.

---

## 5. Skill-Freigabe: was erlaubt ist und was nicht

**Erlaubt (ohne Rückfrage, weil Daniel sie der Sitzung 41 erteilt hat):**
- **Ergänzen** von belegten Bedienhinweisen, Pitfalls und erprobten Reihenfolgen in der passenden
  Referenzdatei (wie am 12.11. zweimal geschehen: DPI-Abschnitt, Tk-Punkterundung).
- **Neue** Referenzdatei anlegen, wenn ein Thema sonst keine Heimat hat.
- **Korrigieren** eines sachlich falschen Satzes, wenn die Messung ihn widerlegt.

**Nicht erlaubt ohne Daniels Wort:**
- eine bestehende **Handlungsregel abschwächen, ersetzen oder löschen**;
- `SOUL.md`, die neun Arbeitsregeln, Kosten-/Sicherheits-/Datenschutzregeln anfassen;
- `SKILL.md` umbauen oder teilen (Claudes **C3**) — das ist eine Regeländerung;
- Regel 2 um „gekennzeichnete Startwerte“ ergänzen (Claudes **C7**) — ebenfalls Regeländerung.

**Pflicht bei jeder Skill-Änderung (Regel 9):** eine Zeile in
`C:\Users\saras\AppData\Local\hermes\SKILL_UND_REGEL_PROTOKOLL.md` mit Zeit, Datei und Abschnitt,
**Hash vorher → nachher**, Grund, Freigabe („Daniel 12.11.2026, Skill-Freigabe für Sitzung 41“) und
Rückrollweg samt Sicherung. Ohne Eintrag gilt die Änderung als nicht geschehen.

**Technischer Hinweis:** `skills.write_approval` ist **an** — ein `skill_manage`-Schreiben landet als
Vormerkposten unter `…\hermes\pending\skills\<id>.json`. Mit erteilter Freigabe wird der Posten
angewandt (Inhalt aus dem Posten in die Zieldatei, Sicherung vorher nach
`…\hermes\pending\<datei>_vor_<thema>.md`, danach Posten löschen) und protokolliert. **Nie** die
Freigabe stillschweigend umgehen und **nie** `config.yaml` dafür ändern.
