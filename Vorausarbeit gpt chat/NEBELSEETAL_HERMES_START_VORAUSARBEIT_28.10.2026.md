# START FÜR HERMES – Nebelseetal Remake / geprüfte GPT-Vorausarbeit

**Stand:** 28.10.2026 · **Ablage bei Daniel (Windows):**
`D:\Arbeiten\Nebelseetal_Remake\Vorausarbeit gpt chat`

**WICHTIG: Dieses Dokument gilt für `NEBELSEETAL_GPT_GESAMTPAKET_KORRIGIERT_28.10.2026.zip`, nicht für die alte fehlerhafte Gesamt-ZIP.** Das alte Archiv nicht integrieren: Seine `ARBEITSKOPIE` enthielt aufgrund eines Verpackungsfehlers falsch duplizierte Dateiinhalte. Das korrigierte Paket wurde stattdessen aus drei separat geprüften Originalarchiven zusammengesetzt.

## 1. Rollen und Sicherheit
Hermes ist und bleibt **einziger Hauptkoordinator**: Aufgabenplanung, Integration, Git-Commits, Freigabe, offizielle Projektstruktur und Skill-Pflege. ChatGPT war **externer, vorübergehender Entwicklungsagent** auf isolierter Kopie. Keine Behauptung, der Hermes-Hauptbranch sei bereits geändert. **Nie blind entpackte Dateien über `D:\Arbeiten\Nebelseetal_Remake` kopieren.** ZIP zuerst nur im obigen Ablageordner öffnen und anhand der Checksummen prüfen. Keine `.env`, API-Schlüssel, Grund-/Adminpasswörter oder `tor.json` in Chat- oder Entwicklerpakete aufnehmen.

## 2. Pakete im korrigierten Archiv – alle drei sind enthalten

- `01_BASELINE/Nebelseetal_Remake_UNVERAENDERT.zip`: **ursprüngliches Hermes-Projekt**, nur zum Vergleich und zur Sicherung. Nicht durch GPT ersetzen.
- `02_TESTVERSION/NEBELSEETAL_GPT_WINDOWS_TESTFASSUNG_FINAL_28.10.2026.zip`: **vollständige kumulative GPT-Quellcode-Testfassung** mit echten Quelldateien, Karten, Grafiken, Tests, offiziellen GPT-Protokolleinträgen und Windows-Start-/Buildskripten. DIES ist die führende GPT-Arbeitskopie. Nach Entpacken heißt der Projektordner `Nebelseetal_GPT_Testfassung`.
- `03_INTEGRATION/NEBELSEETAL_GPT_HERMES_KUMULATIVES_DELTA_28.10.2026.zip`: gesonderte **313 hinzugefügte/geänderte Dateien**, Quellcode-Patch, Manifest, Prüf- und Integrationsunterlagen. Hermes vergleicht diesen Stand einzeln mit seinem tatsächlichen Git-HEAD; nicht blind anwenden.

Die Hashwerte liegen in `04_PRUEFUNG/SHA256SUMS.txt`. **Alle 313 Dateien aus `DATEIEN/` des Deltas stimmen bytegenau mit dem entsprechenden Pfad in der Windows-Testfassung überein.**

## 3. Lokal testen, ohne Hauptprojekt zu beschädigen

1. `02_TESTVERSION/...zip` **separat** entpacken, idealerweise nach `D:\Arbeiten\Nebelseetal_Remake\Vorausarbeit gpt chat\Testfassung\` (es entsteht darin der Ordner `Nebelseetal_GPT_Testfassung`). **Nicht** ins Hermes-Hauptverzeichnis entpacken.
2. In `Nebelseetal_GPT_Testfassung` `TESTEN_UNTER_WINDOWS.md` lesen; dann `START_SPIEL_WINDOWS.bat` (Python 3 + Tkinter). Für einen eigenen **Windows-EXE-Build** `EXE_ERSTELLEN_WINDOWS.bat` (PyInstaller ggf. erstmals aus Internet), danach ausschließlich `START_EXE_TEST_WINDOWS.bat` zur isolierten Prüfung.
3. Die Skripte sind relativ zum entpackten Ordner; Testspielstände sollen separat unter `%LOCALAPPDATA%\Nebelseetal_Remake\GPT_Test_20261028` liegen. Das vorhandene **Grundpasswort** bleibt eine eigenständige Startfreigabe. Nach Freigabe: normaler Spieler (3 Slots, ohne Cheats) oder Admin (gesonderter Zugang/Testwelt/Cheats).
4. Eine **neu auf Windows kompilierte und dort verifizierte EXE liegt noch NICHT bei**. Bei Baufehlern Protokoll sichern und keine alte EXE als neuen Stand verwenden.

## 4. Fachlicher Stand und ungeprüfte Punkte

Vorhandene GPT-Änderungen: 127 Originalkartenvarianten (10×10), Kartenattribute/Quellen, Grundproduktion Holz+Stein, Ortslager und Karren, Bauten/Waren/Ausbildung, 3 Spielerslots und Admin-Testbereich, Dorfwälle ohne belegtes Kartenfeld, Kampfkern auf Grundlage später gefundener Originaltexte, korrigierte Ausrüstungsbilder, Zeit-/Speicherstempel und monotone Laufzeit, Bot-Kampfkorrekturen, Einzelspielerziel und zuletzt verifizierte Originalwerte. **Keine Releasefreigabe**: vollständige Bot-Ökonomie und Belagerungsstrategie, 25 grafisch ungeprüfte Originalraster, alte 8×7-Ökonomietests, gesamter End-to-End-Durchlauf und aktueller Windows-Build bleiben offen. Kommunikation **an Bots** ist auf Nutzerwunsch ans Entwicklungsende verschoben; automatische Spielereignis-Meldungen bleiben relevant.

Gezielter letzter GPT-Prüflauf laut `docs/GPT_ABSCHLUSS_TESTERGEBNISSE.json`: **21/21 ausgewählte Testdateien grün / 989 ausgewertete Einzelkontrollen**. **Das ist kein Nachweis für die gesamte Testsuite oder Windows-Release.** Hermes führt `run_tests.bat` und EXE-Tests selbst aus und wertet **auch Fehlermeldungen im Testtext** aus (alte Tests können Exit-Code 0 trotz Fehlertext liefern).

## 5. Damit Hermes effizient fortfahren kann

1. `docs/AGENTEN_PLAN.md` in der Testfassung zuerst lesen und die **eigene** bestehende Roadmap/den aktuellen Git-Stand feststellen. Ursprungsversion ≠ aktuellem Hermes-Hauptbranch; bei Abweichung manuell dreifach vergleichen.
2. `docs/GPT_AKTUELLER_ENTWICKLUNGSSTAND_2026-10-28.md` und die **offizielle** `docs/ENTWICKLUNGSPROTOKOLL.md` (GPT-ABS01–06 und frühere GPT-Kennungen) prüfen. Details nur bedarfsweise öffnen.
3. `03_INTEGRATION` als Prüfgrundlage verwenden. Integration **schrittweise** mit unabhängigen Tests, danach Freigabe/Commit ausschließlich durch Hermes. `src/main.py` und andere gemeinsame Dateien niemals parallelen Kind-Agenten überlassen.
4. Aus jedem bestätigten Fix Ursachen, fehlende Regression, defensive Programmierregel und neuen Test ableiten; gegen die **bestehenden** Hermes-Skills abgleichen, Dopplungen vermeiden. Quelle: `docs/GPT_HERMES_SKILL_LERNREGELN_2026-10-28.md`.
5. Testbefunde und Integration im offiziellen Entwicklungsprotokoll und in den von Hermes geführten Projektakten fortschreiben. Neues Kurzkontext-Dokument bei der nächsten Sitzung **nur aus überprüftem Git-Stand und Protokoll** aktualisieren, nicht aus unkontrollierten Behauptungen.

**Paket-Reparatur am 28.10.2026:** ChatGPT (externer Agent) hat ausschließlich die ZIP-Zusammenstellung und diese Einstiegsdokumentation korrigiert; keine weiteren Spielcode-Änderungen. Details: `04_PRUEFUNG/PAKETREPARATUR_PROTOKOLL.md`.
