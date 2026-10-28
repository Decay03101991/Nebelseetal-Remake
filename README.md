# Nebelseetal Remake

Entwicklungsprojekt: Einzelspieler-Remake des historischen Browserspiels *Nebelseetal*.

> **Status:** In Entwicklung; kein freigegebener Windows-Release. Funktionsfaehigkeit, Vollstaendigkeit und grafische Abnahme sind noch nicht abschliessend belegt.

## Aktueller Entwicklungsstand

- [Projektstatus und Stand der Spielbereiche](docs/PROJEKT_STAND.md)
- [Offizielles Entwicklungsprotokoll](docs/ENTWICKLUNGSPROTOKOLL.md)
- [Projektplanung und Aufgabenverteilung](docs/AGENTEN_PLAN.md)
- [Projektordnung](docs/ORDNUNG.md)
- [Test- und Auslieferungsanforderungen](docs/WEG_ZUR_EXE.md)

Diese Dokumente stammen aus dem lokalen Projekt. Bei jeder veroeffentlichten Aenderung
muessen sie mit dem tatsaechlich eingecheckten Code abgeglichen werden.

## Verzeichnisuebersicht

- `src/` – Spielcode
- `data/` – Spielwerte und Konfiguration ohne Geheimnisse
- `assets/` – benoetigte Grafiken
- `tests/` – automatisierte Pruefungen
- `tools/` – Entwicklungswerkzeuge
- `docs/` – Protokolle, Planung, Herkunft und Forschungsbelege

## Start / Test

**Festgelegtes Verhalten:** Jeder Nutzer richtet beim ersten Start sein eigenes lokales Passwort ein.
Er ist keine zentrale Zugangsbeschraenkung fuer eine oeffentliche Quellcodeveroeffentlichung.
Das Projekt ist noch kein allgemein freigegebener Spiel-Release.

Auf Windows kann der Entwicklungsstand nach Pruefung der Abhaengigkeiten ueber
`Nebelseetal_Remake.bat` gestartet werden; die Auslieferung als EXE ist gesondert zu testen.

## Entwicklung und Protokollierung

Die offizielle Projektkoordination, Integration und Git-Freigabe liegt bei Hermes.
Die GitHub-Kopie soll die freigegebenen Arbeitsdateien spiegeln, nicht automatisch
ungetestete GPT-Vorausarbeit in den Hauptbranch uebernehmen.

Sensible Dateien wie `tor.json`, lokale `.env`-Dateien, Schluessel, Spielstaende,
Build-Ausgaben und persoenliche Zugangsdaten gehoeren nicht ins Repository.
