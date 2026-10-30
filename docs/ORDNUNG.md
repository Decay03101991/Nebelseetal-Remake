# Verbindliche Projektordnung

1. **Nur ein aktives Spiel** (`src/`), **nur ein aktives Protokoll** (`docs/ENTWICKLUNGSPROTOKOLL.md`), **nur ein aktuelles Handover** (`docs/HERMES_UEBERGABE_AKTUELL.md`).
2. `assets/` nur fuer Spielgrafiken und originale Bildquellen; `data/` nur fuer Regeldaten; `tests/` und `tools/` separat.
3. Historische Fassungen, Screenshotvergleiche, alte Berichte, Uebergaben: `archiv/`. Nicht unkontrolliert wieder aktivieren. Alle Dateiumzuege in `archiv/manifeste/ORDNER_UMZUGSPLAN.json`.
4. Historische Hauptprojektfassung: `archiv/altstaende/HERMES_HAUPTSTAND_VOR_GPT_KONSOLIDIERUNG_2026-10-28.zip` (ohne .git, EXE und erkannte Zugangsdaten).
5. GitHub: `archiv/` ist lokal und in `.gitignore` ausgeschlossen. Ob Quelltexte, Originalbilder und Dokumente veroeffentlicht werden duerfen, VOR jedem Push gesondert pruefen.
6. Hermes muss echten Git-HEAD und Deltas vergleichen, Tests durchfuehren, freigeben, Protokoll und Status aktualisieren. Keine automatische GitHub-Synchronisation aus einem ungetesteten ZIP.
7. Keine zweiten Kopien des aktuellen Protokolls im aktiven Bereich anlegen. Archivfassungen bleiben archiviert und werden nie von Werkzeugen als aktuell behandelt.

8. Neues Windows-EXE-Testprogramm ist erst nach einem nachweislich erfolgreichen Build vorhanden; `EXE_ERSTELLEN_WINDOWS.bat` erstellt es auf Windows im Hauptordner, NICHT im Archiv.
9. Vorhandene Dokumente/Quellen: `docs/QUELLEN_UND_DOKUMENTE.md`, maschinenlesbarer Vollindex unter `archiv/manifeste/DOKUMENTE_VOLLINVENTAR.json`.

## GPT-FIX02d-R2 - Ein einziger Einstieg je Zielgruppe

`README.md` ist die einzige aktive Anleitung fuer Besucher und Windows-Spielstart. `docs/HERMES_UEBERGABE_AKTUELL.md` ist die einzige aktuelle Anweisung fuer Hermes. `docs/ENTWICKLUNGSPROTOKOLL.md` bleibt die einzige aktive Chronik. Eine separate aktuelle `START_HIER.txt` gibt es **nicht** mehr. Alte Einstiegstexte, zwei Berichte und doppelte .bat-Wrapper liegen mit SHA-256-Nachweisen unter `archiv/ordnungsbereinigung_FIX02d_20261028/`; der alte Stand ist nur historisch. Aktive Starter: `START_SPIEL_WINDOWS.bat`, `EXE_ERSTELLEN_WINDOWS.bat`, `START_EXE_TEST_WINDOWS.bat`, `run_tests.bat`.
