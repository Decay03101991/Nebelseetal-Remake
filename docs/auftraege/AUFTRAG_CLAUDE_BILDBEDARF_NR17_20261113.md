# AUFTRAG NR. 17 — Bildbedarf vollständig aufstellen (Bedarfsliste für die Grafikproduktion)

| | |
|---|---|
| **Auftraggeber (Modell)** | Hermes Agent „Weltenfresser“, `deepseek-v4-flash` — **Top-Koordinator des Projekts** |
| **Auftragsnehmer (Modell)** | **Claude Opus 5.5 (Thinking: hoch)** |
| **Rangordnung** | Weltenfresser bleibt der unberührbare Top-Koordinator: er zerlegt die Arbeit, misst, prüft, baut und führt das Register. Der Auftragsnehmer **arbeitet zu** — er gibt keine Anweisungen an den Koordinator und ändert die Rollen nicht. |
| **Pflicht in der Antwort** | Oben in der Antwort dieselben zwei Modelle („Auftrag von …“ / „Antwort von …“) und ein Satz zur eigenen Rolle. |
| **Rückgabe** | Deutsch, mit Zahlen; **gemessen / gerechnet / angenommen** getrennt; Zusatzinformationen in einem eigenen, gekennzeichneten Abschnitt. |

---

## 1. Der Auftrag in einem Satz

Erstelle die **vollständige Bildbedarfsliste** des Spiels: welche Grafikdatei wird **wo** gebraucht, in
welcher **Anzeigegröße**, in welchem **Format und welcher Auflösung**, mit welchem **Zweck** und in
welcher **Priorität** — jede Zeile am Quelltext belegt.

## 2. Lage und warum jetzt

Die Bildproduktion ist **aufgeschoben**: Daniel hat für Meshy erst im Dezember wieder Guthaben, und
selbst erzeugte Bilder über kostenlose Dienste hat er abgelehnt („dafür brauchen wir die richtige KI“).
Damit der Auftrag an das Bildmodell im Dezember **in einem Zug** durchläuft, braucht es vorher die
Liste: **jedes Bild mit Zweck und Maß**, sonst entstehen Bilder, die nirgends hinpassen.

Das ist ausdrücklich **Vorarbeit ohne Bild**: du erzeugst nichts und änderst nichts.

## 3. Was du lieferst — der Aufbau der Liste

**Eine Tabelle**, eine Zeile je benötigtem Bild. Spalten genau so:

| Spalte | Inhalt |
|---|---|
| `kennung` | sprechender Name, z. B. `wappen_menschlich`, `burg_zwergisch`, `portal_kopfband` |
| `zweck` | **welche Ansicht, welches Widget** (z. B. „Portal, Weltkarte 20 × 20, Abzeichen unten rechts am Dorf“) |
| `fundstelle` | `datei.py:Zeile`, wo das Bild geladen oder gezeichnet wird |
| `anzeige_px` | Größe auf dem Schirm in Pixeln, **gemessen** aus dem Code (z. B. „8 × 8“) |
| `datei_px` | empfohlene Dateigröße in Pixeln (begründe den Faktor, z. B. „4× Anzeige für 200 % DPI“) |
| `format` | PNG / JPG / WebP; **Alpha nötig: ja/nein** |
| `anzahl` | wie viele Dateien (z. B. sechs Fraktionen) |
| `status` | `vorhanden` / `vorhanden, aber zu klein` / `fehlt` |
| `pfad_ist` | Pfad der vorhandenen Datei, falls es sie gibt |
| `prio` | **1** = ohne geht keine Ansicht, **2** = wichtig für die Wirkung, **3** = schön zu haben |
| `quelle` | woher die Zahl stammt: `gemessen (Datei:Zeile)` / `gerechnet (Rechnung)` / `angenommen` |

## 4. Messpflicht (der Kern des Auftrags)

1. **Gehe vom Zeichenweg aus, nicht von den Ordnern**: suche im Quelltext, wo Bilder geladen werden
   (`PhotoImage`, `Image.open`, `ladebild`, `_bild`, `create_image`) und was dort als Zielgröße steht.
2. **Nenne für jede Zeile die Fundstelle** (`src/main.py:1234`). Ohne Fundstelle gilt die Zeile als
   **UNBEKANNT** und wird von mir nachgemessen.
3. **Prüfe die vorhandenen Dateien wirklich**: Auflösung und Alpha (`PIL.Image.open(...).size`, `.mode`)
   — nicht annehmen, dass eine Datei passt, weil sie existiert.
4. **Trenne Anzeigegröße und Dateigröße.** Ein Bild, das mit 8 px gezeichnet wird, braucht keine
   1024 px — aber für DPI 2 genügt 4× Anzeige, nicht 100×.
5. **Allgemeine Regel statt Einzelwert**: wenn eine Größe von der Fensterbreite abhängt, gib die
   **Formel** an, nicht den Wert eines Fensters.

## 5. Was es schon gibt (Startpunkte, selbst nachprüfen)

- `assets/icons/burgen/` — sechs Burgen (burg_01..06)
- `assets/icons/wappen/` — zehn Wappen (wappen_01..10), davon sechs im Einsatz
- `assets/icons/` — zwölf weitere Symbole
- `assets/bilder/` (13), `assets/hintergruende/` (1), `assets/karten/` (1), `assets/loadingpage/` (1),
  `assets/quellenbilder/` (4), `assets/original/` (8), `assets/referenzbilder/` (17, davon 9
  Fraktions-/Stil-Referenzen)
- `assets/wappen/` — drei Dateien aus einer Meshy-Lieferung (12.11.), laut früherer Messung von
  `src/` und `data/` **nirgends benutzt** — prüfe das nach und ordne sie in die Liste ein.

Die Zahlen in Klammern sind **gezählt** (Verzeichnisliste vom 13.11.2026), nicht gemessen am Code.

## 6. Entschieden — nicht neu verhandeln

- **Fraktion → Burg/Wappen (Daniel 13.11.2026):** Silberbach `burg_02`+`wappen_04`, Hammerhall
  `burg_01`+`wappen_10`, Sternenwacht `burg_03`+`wappen_09`, Schattenfaust `burg_05`+`wappen_08`
  (roter Drache — **kein Wolf**, Daniel: „es gibt diese Fraktion nicht“), Knochenmoor
  `burg_04`+`wappen_02`, Flickwerk `burg_06`+`wappen_05`.
- **Das Wappen ist ein Abzeichen, keine Szene.** Auf der Weltkarte ist es rund **8 px** groß
  (`docs/AKTUELLER_STAND.md`, Bildplan D-5, Register 345/346: Karte 400 × 400, Burg 18 px, Wappen
  8 px) — daraus folgt: ein Symbol, zwei bis drei Farben, klare Silhouette.
- **Kein Helm, keine Helmzier** in Wappen (Chronik, Teil 5).
- Die Motive der Wappen stehen in `CHRONIK_DER_WELT.md`, Teil 5 — nicht neu erfinden.

## 7. Was du NICHT tust

- keine Bilddatei erzeugen, ändern oder löschen
- keine Datei in `data/`, `src/` oder `tests/` anfassen
- keine Mechanik-Zahlen vorschlagen
- keine Prioritäten „alles ist Prio 1“ — begründe jede 1

## 8. Antwortformat

1. **Kopf zurück** (Auftrag von / Antwort von / ein Satz zur Rolle).
2. **Die Tabelle** aus Abschnitt 3 — vollständig, auch die Zeilen `UNBEKANNT`.
3. **Ein Abschnitt „Was ich nicht prüfen konnte“** — je Punkt, was fehlt und wie ich es messen kann.
4. **Ein Abschnitt „Zusatzinformationen“** (getrennt, damit ich entscheiden kann, ob ich sie nutze).
5. **Eine kurze Zusammenfassung in fünf Zeilen**: wie viele Bilder fehlen, wie viele sind zu klein,
   was ist Prio 1.

## 9. Ablage

Antwort als Markdown an mich zurück; ich lege sie unter `docs/eingaenge/` ab und baue daraus den
Bildauftrag für Dezember. Die Fassung für Daniel liegt als `.txt` (UTF-8 mit BOM) auf dem Desktop.
