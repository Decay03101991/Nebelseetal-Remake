# AUFTRAG NR. 18 — Bildbedarfsliste (Fassung ohne Rechnerzugriff)

| | |
|---|---|
| **Auftraggeber (Modell)** | Hermes Agent „Weltenfresser“, `deepseek-v4-flash` — **Top-Koordinator des Projekts** |
| **Auftragsnehmer (Modell)** | **Claude Opus 5.5 (Thinking: hoch)** |
| **Rangordnung** | Weltenfresser bleibt der unberührbare Top-Koordinator: er zerlegt, misst, prüft, baut, führt das Register. Der Auftragsnehmer **arbeitet zu**. |
| **Pflicht in der Antwort** | Oben dieselben zwei Modelle („Auftrag von …“ / „Antwort von …“) und ein Satz zur eigenen Rolle. |
| **Rückgabe** | Deutsch, mit Zahlen; **gemessen / gerechnet / angenommen** getrennt; Zusatzinformationen in einem eigenen Abschnitt. |

---

## 1. Warum diese Fassung

Auftrag Nr. 17 verlangte, jede Zeile am Quelltext zu belegen — **das setzt Rechnerzugriff voraus, den du
nicht hast.** Nr. 17 ist damit erledigt und ersetzt. **In dieser Fassung musst du nichts öffnen und
nichts messen:** die Messungen sind gemacht und liegen bei. Du **urteilst und ordnest**, nicht messen.

## 2. Was dir vorliegt (Anlagen)

| Anlage | Inhalt |
|---|---|
| **`BILDBESTAND_MESSUNG_20261113.txt`** | **370 Bilddateien**: Pfad, Pixelmaße, Farbmodus (Alpha ja/nein), Dateigröße in KB und die **erste Fundstelle** im Quelltext oder in den Daten (`datei:zeile`). Gemessen am 13.11.2026. |
| `nebel_src_data_20261113.zip` (3,2 MB) | `src/` (8 MB Quelltext) und `data/` (943 KB) — falls du eine Stelle im Code selbst nachlesen willst. |
| `nebel_assets_wappen_icons_20261113.zip` (22 MB) | `assets/icons/` (210 Dateien inkl. Burgen und Wappen), `assets/wappen/` (Meshy-Lieferung), `assets/bilder/`. |

Nicht dabei sind `assets/karten/` (27 MB Weltkarten-Quellbilder) und `assets/hintergruende/` — die sind
für diese Aufgabe nicht nötig; wenn du sie doch brauchst, sag es, dann liefere ich nach.

## 3. Die Aufgabe

Baue aus dem Messblatt die **Bildbedarfsliste** des Spiels. Vier Teile:

### Teil A — Ist-Stand prüfen
Gehe das Messblatt durch und teile jede Datei in eine der vier Klassen:
`ausreichend` · `zu klein für ihren Zweck` · `unbenutzt` · `doppelt/fragwürdig`.
Für „zu klein“ gilt als Maßstab: **eine Bilddatei sollte mindestens das Vierfache der Anzeigegröße
haben** (DPI 2 und Spielraum). Die Anzeigegrößen, die ich kenne, stehen in Abschnitt 5.

### Teil B — fehlende Bilder benennen
Alles, was im Messblatt **nirgends genannt** ist oder ganz fehlt, gehört in die Lücke. Für jedes neue
Bild: Zweck, Ansicht/Widget, Anzeigegröße, empfohlene Dateigröße, Format und Alpha, Anzahl, Priorität
(1 = ohne geht eine Ansicht nicht, 2 = wichtig für die Wirkung, 3 = schön), und **was darauf zu sehen
sein muss** (ein Satz, gegenständlich).

### Teil C — die sechs Wappen
Für die sechs Fraktionen gilt verbindlich (Daniel 13.11.2026): Silberbach `burg_02`+`wappen_04`,
Hammerhall `burg_01`+`wappen_10`, Sternenwacht `burg_03`+`wappen_09`, Schattenfaust `burg_05`+
**`wappen_08` (roter Drache)**, Knochenmoor `burg_04`+`wappen_02`, Flickwerk `burg_06`+`wappen_05`.
Das Abzeichen ist auf der Weltkarte rund **8 px** groß. Prüfe an den Dateien im ZIP (Maße stehen im
Messblatt): reicht die Auflösung, ist der Alphakanal sauber, ist das Motiv bei 8 px unterscheidbar?
Sage je Wappen **eine** klare Empfehlung: behalten, ersetzen oder neu zeichnen — mit Begründung.

### Teil D — die drei unbenutzten Meshy-Wappen
In `assets/wappen/` liegen `elfen_wappen.png` und zwei kleinere Fassungen (`_128`, `_64`). Laut
früherer Messung werden sie von `src/` und `data/` **nirgends** benutzt. Entscheide: einbinden (wo?),
als Vorlage behalten oder verwerfen — mit Begründung.

## 4. Antwortformat

1. Kopf zurück (Auftrag von / Antwort von / Rolle).
2. **Tabelle A** (Ist-Stand, 370 Zeilen sind zu viel — fasse je Ordner zusammen und nenne die
   Ausnahmen einzeln).
3. **Tabelle B** (fehlende Bilder, vollständig).
4. **Abschnitt C** (sechs Wappen, je ein Satz Empfehlung).
5. **Abschnitt D** (drei Meshy-Dateien).
6. **„Was ich nicht beurteilen kann“** — offen benennen, nicht schätzen.
7. **Zusammenfassung in fünf Zeilen**: wie viele Bilder fehlen, wie viele sind zu klein, was ist Prio 1.

## 5. Was ich als Anzeigegröße schon gemessen habe

| Ort | Größe | Quelle |
|---|---|---|
| Weltkarte, Feld | 20 px | `docs/AKTUELLER_STAND.md` (Portal 20 × 20 Felder) |
| Weltkarte, Burg am Feld | 18 px | Bildplan D-5, Register 345/346 |
| Weltkarte, Wappen (Abzeichen) | **8 px** | ebenda |
| Worldkarte gesamt | 400 × 400 px | ebenda |
| Fenster (Referenz) | 1024 × 720 px | ebenda |

Alles andere steht **nicht** in dieser Liste und ist damit für dich **UNBEKANNT** — du darfst es aus dem
Messblatt ableiten, aber nicht erfinden.

## 6. Was du NICHT tust

keine Datei ändern, nichts löschen, keine Mechanik-Zahlen vorschlagen, keine Priorität „alles ist 1“.
