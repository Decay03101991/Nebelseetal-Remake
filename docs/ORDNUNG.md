# Ordnung im Projekt Nebelseetal Remake

**Grundsatz (Daniel, 04.10.2026):** „sei nur vorsichtig und lass die nebelseetal ordner
strukturen immer schön aufgeräumt". Diese Datei sagt, was wohin gehört — damit nichts mehr
lose herumliegt und niemand raten muss.

## Was wohin gehört

| Ordner | Inhalt | Regel |
|---|---|---|
| `src/` | das laufende Spiel (`main.py`, `gelaende.py`, `kampf.py`, `einheiten.py`, `spieldaten.py`, `bonus_system.py`) | nur Code, der zum Spiel gehört |
| `data/` | die Originalwerte als JSON (`units.json`, `buildings.json`, `resources.json`, `research.json`, `items.json`, `gelaende.json`) | **eine** Quelle je Wert; nichts wird hier geschätzt, fehlende Werte stehen als `null` mit Begründung |
| `tests/` | Prüfdateien (`test_*.py`) + `harness.py` | jede Datei endet mit `sys.exit(bericht())`, Rückgabewert 0 = grün |
| `tools/` | einmalige Werkzeuge (`slice_icons.py`, `clean_icons.py`, `archiv_assets.py` …) | Werkzeuge dürfen Belege erzeugen, aber nie Spielwerte ändern |
| `docs/` | Pläne, Audits, Entwürfe, Abnahmelisten | deutsche Dateinamen, oben der Zweck, unten die offenen Fragen |
| `docs/original/` | **Belegarchiv**: Handbuch-PDF, Textfassung, Website-Seiten, ausgelesene Wertetabellen | unveränderlich; hier wird nichts verändert, nur abgelegt |
| `docs/original/assets_website/` | aus dem Web-Archiv geborgene Originaldateien (Schaltflächen, Logos, Wallpaper) | mit `QUELLEN.md` (Herkunft je Datei) |
| `docs/original/karten/` | geborgene Kartenbilder + `QUELLEN*.md` | Herkunft immer belegen |
| `docs/original/recherche/` | Suchprotokolle (CDX-Listen, geborgene Seiten als HTML/Text) | Rohbelege, nicht löschen |
| `docs/original/handbuch_bilder/` | die 240 aus dem PDF ausgelesenen Bilder (Hintergrundtextur) | Belegmaterial |
| `docs/audits/` | Rohantworten der teuren Modellläufe | unverändert gespeichert, nicht nachbearbeitet |
| `docs/icon_preview/` | Vergleichsblätter zur Icon-Abnahme | für Daniels Sichtprüfung |
| `assets/icons/` | `original_units/` = **Daniels 17 Dateien (unantastbar)**, `units/`, `items/`, `clean/` (freigestellt) | Daniels Dateien niemals umbenennen oder verschieben |
| `assets/original/` | Original-Schaltflächen der alten Website | Belegmaterial |
| `Einheiten Icons/`, `Item Icons/` | die Original-Iconblätter | **unantastbar**, bleiben wie sie sind |
| `_Quarantaene/` | Doppelungen, alte Builds, Unsicheres | nie endgültig löschen — erst hierher |

## Regeln, die sich bewährt haben

1. **Genau eine ausführbare Fassung** im Projekt. Alte Builds (`*.exe`) gehören in die
   Quarantäne — ein alter Build mit demselben Fenstertitel hat am 04.10.2026 für Verwirrung
   gesorgt (Golems und Pikeniere, die der Code längst nicht mehr kannte).
2. **Keine Arbeitsdateien im Wurzelverzeichnis.** Suchläufe und Zwischenergebnisse gehören
   unter `docs/original/recherche/` oder in den Zwischenspeicher, nicht ins Projekt.
3. **Werkzeuge räumen hinter sich auf**: `build/`, `dist/`, `*.spec`, `__pycache__` stehen
   in `.gitignore` und werden nach jedem Erstellen entfernt.
4. **Belege werden nicht verändert.** Wer eine Rohantwort oder ein geborgenes Bild ablegt,
   legt es unverändert ab und schreibt die Herkunft dazu.
5. **Daniels Bilder und Dateien sind unantastbar.** Nicht umbenennen, nicht umsortieren,
   nicht zuschneiden — bei Bedarf fragen und vorher zeigen.

## Offen (Entscheidung Daniel)

Drei Originalbilder liegen noch im Wurzelverzeichnis, weil sie möglicherweise von Daniel
selbst dort abgelegt wurden — sie werden **nicht ohne Rückfrage** verschoben:

- `nebelseetal.png` (6 KB)
- `Nebelseetal_Loadingpage.jpg` (33 KB) — die Ladepage (Holzmaserung, Schild, gekreuzte Schwerter)
- `nebelseetal_optik.jpg` (68 KB) — Siedlungsansicht mit Lager

Vorschlag: nach `docs/original/` verschieben, wo das übrige Originalmaterial liegt.
