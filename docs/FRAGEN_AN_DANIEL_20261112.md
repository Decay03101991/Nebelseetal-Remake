# Fragen an Daniel — gesammelt in der Nacht 12./13.11.2026 (Sitzung 41)

**Regel:** Fragen werden **gesammelt** und bei Daniels Rückkehr **in EINER Runde** vorgelegt —
nicht einzeln, nicht mit Zeitablauf (Arbeitsregel 7; Daniels Wort seit Sitzung 39).
Je Frage: **Messlage · Auswirkung · Vorschlag zuerst**. Freie Antwort ist immer möglich.

---

## 1. Sichtprüfung des DPI-Umbaus (offen aus Sitzung 40, F-51)

**Messlage:** `docs/audits/dpi_vorher_weich_20261112.png` gegen `dpi_nachher_scharf_20261112.png`.
Bewusst: Schirm 1920 × 1080, k = 1,2512, Fenster 1560 × 940, Fläche 1127 × 764, Feld 64.
Unbewusst: 1536 × 864, Fläche 1037 × 589, Feld 57.

**Auswirkung:** Bleibt der Umbau, ist alles scharf und physisch kleiner. Wird er zurückgenommen,
ist alles weich und größer. Bis zu deinem Urteil wurde **nichts** geändert.

**Vorschlag:** so lassen (scharf), weil Schrift und Kanten bei 125 % Skalierung sonst unscharf
skaliert werden — **deine** Entscheidung nach den zwei Bildern.

**Deine Frage dazu:** scharf und gut · scharf, aber hässlich · zu klein/groß?

## 2. Löschen von Prüfdateien (F-67 erlaubt Umstellen, nicht Löschen)

**Messlage:** 230 Prüfdateien, 9.905 Prüfungen, 1.380 s seriell. 46 Dateien haben keine
Messwert-Historie (34 davon alte `gpt_`-Dateien). Seit heute Nacht schreibt der Sammellauf eine
Zeile je Datei (`docs/audits/laeufe.jsonl`), damit ist die Lücke im Aufzeichnen zu.
Kandidaten für „nur bei Änderung“ oder Zusammenlegen stehen in der Antwort Nr. 16, Punkt 7.

**Auswirkung:** Löschen spart Laufzeit, kann aber eine alte Prüfung mitnehmen, die noch etwas
Gültiges absichert.

**Vorschlag:** **nichts löschen**. Erst eine volle Runde mit der neuen Laufzeilen-Ablage, dann
Antrag je Datei mit Prüfnamen-Abgleich (mindestens 90 % der Eigenschaften muss die neue Datei
abdecken). Ich lege den Antrag vor, du entscheidest.

## 3. Die 46 alten Dateien einmal einzeln sichten (Claudes C10)

**Messlage:** 34 der 46 sind `gpt_`-Dateien aus den Fixrunden vom 31.10. Ob sie noch etwas Gültiges
prüfen, weiß niemand — sie laufen im Sammellauf mit, schreiben aber nichts in den Index.

**Auswirkung:** Sichtung kostet einmalig die Summe ihrer Einzeldauern (unbekannt, geschätzt
5–10 Minuten), bringt danach Klarheit und möglicherweise Streichkandidaten.

**Vorschlag:** Sichtung nach der ersten vollen Runde automatisch mitlaufen lassen
(`tools/einzeln_sichten.py`) und dir eine Tabelle vorlegen — keine Entscheidung ohne dich.

## 4. `main:*` in den Prüfstand-Köpfen (neu durch M1)

**Messlage:** 184 von 230 Dateien nennen `main`. Damit die Auswahl (M2) nicht 184 Dateien zieht,
steht in ihren Köpfen `main:*` = „irgendeine Funktion in `main.py`“. Sobald eine Datei angefasst
wird, wird der Eintrag auf die **echte** Funktion verengt (z. B. `main:_render_settlement_map`).

**Auswirkung:** Solange `main:*` steht, zieht eine Änderung an `main.py` diese Dateien weiterhin
mit — die Auswahl ist also heute schon ehrlich, aber noch nicht fein.

**Vorschlag:** so lassen und beim Anfassen verengen (Claudes C6: „beim Berühren herausziehen“).
Keine Aktion nötig, nur zur Kenntnis — **Widerspruch willkommen**.

## 5. Werkstatt-Zuordnung: zwei Quellen (Befund B4 der Nachrechnung Nr. 16)

**Messlage:** `data/items.json` führt je Ware ein Feld `werkstatt` (Schmiede 8, Nähstube 5,
Bogner 4), und `src/werkstatt.py` liest **nur** diese eine Stelle. `data/warenrezepte.json` hat
das Feld noch nicht. F-64 sagt: Feld je Rezept. Ein Handeintrag dort macht aber
`test_warenrezepte` rot (die Datei muss stückweise der Ableitung entsprechen).

**Auswirkung:** Wird das Feld nur von Hand eingetragen, gibt es zwei Listen, die auseinanderlaufen
können — genau die Fehlerart, die „verbund-konsistenz“ verhindern will.

**Vorschlag:** das Feld **aus der Ableitung** schreiben (`tools/warenrezepte_ableiten.py` kennt die
Werkstatt bereits) **plus** eine Wache, die beide Seiten vergleicht. Damit gibt es eine Quelle und
zwei Ansichten. Sagst du ja, baue ich es so.

## 6. Völkerfarben: Burgbilder oder `FRAKTIONEN_WELTEN.md`?

**Messlage:** Zwei Quellen widersprechen sich. `FRAKTIONEN_WELTEN.md` (unser Projekt) sagt Trolle
dunkelrot/schwarz und Ghule grün/knochenweiß. Claudes Angaben „Trolle weiß-gold, Ghule violett“
stammen nach seiner Auskunft aus **deiner** Beschreibung der Burgbilder.

**Auswirkung:** F-71 sagt bereits „die Burgbilder geben die Farbe vor“ — dann wird
`FRAKTIONEN_WELTEN.md` angepasst, nicht die Bilder. Bestätige bitte, dass das so gemeint war.

**Vorschlag:** Burgbilder führen, Datei anpassen (F-71). Ich baue es erst, wenn du es bestätigst.

---

## Antworten, die ich in der Nacht **nicht** brauche (nur zur Kenntnis)

- **Nachrechnung Nr. 16:** Werteblock vollständig bestätigt, Block 5 = 370 (meine 380 war falsch),
  vier Befunde (B1–B4) — alle vier ändern den Bauweg, keine deiner Entscheidungen.
- **F-57 gebaut:** Abstand = gemessener Rollbalken (21 px), S = 448, Wachen grün.
- **F-60 gebaut:** `dorfzentrum_kennzahlen` in der Ökonomie, Wache 23/0/0.
- **M12.0 gebaut:** der Sammellauf schreibt eine Zeile je Datei — die 46 blinden Flecken sind zu.
- **M11 gebaut:** `docs/FAKTENBLATT.md` aus `data/` (17 Waren, 17 Rezepte mit je 1 Zutat,
  28 Einheiten, 21 Forschungen, 20 Gebäude, Werkstätten 8/5/4) plus Auftragsprüfung.

## 7. Soll `test_e2e_wege` als neunte Datei in die Stufe T4? (neu aus dem vollen Lauf)

**Messlage:** Der volle Lauf 13.11.2026 (seriell, jede Datei allein) zeigt: `test_e2e_wege` braucht **186,2 s** und ist damit die teuerste Prüfdatei überhaupt — teurer als jede der acht T4-Dateien. In Paket 15b stand sie mit 361,7 s unter Last, wurde dort aber nicht zu den T4-Kandidaten gezählt. Die übrigen acht sind allein deutlich schneller als gedacht: `test_produktionskette_ohne_cheats` 81,8 s statt 301,2 s, `test_handelspunkte` 25,7 s statt 109,7 s.

**Auswirkung:** T4 dauert heute rund 20 Minuten (1.216 s für alle 238 Dateien). Mit `test_e2e_wege` als neunter Datei wird der Lauf vor einer EXE kaum länger (die Datei läuft dort ohnehin mit), aber sie wird **bewusst** Teil der verbindlichen Stufe statt „irgendwo in T3“.

**Vorschlag:** `test_e2e_wege` als **neunte** Datei nach T4 (F-67 nennt acht — deshalb frage ich). Die Stufe selbst bleibt HART vor jeder EXE.
