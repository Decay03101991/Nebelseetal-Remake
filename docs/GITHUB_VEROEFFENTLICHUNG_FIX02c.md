# Nebelseetal – GitHub-Update und Windows-Testversion (FIX02c)

**Status: NICHT freigegeben; keine aktuelle EXE im gelieferten Stand.**

## Vorher prüfen

- ZIP vom 28.10.2026 enthält alle 1.229 Dateien der FIX02-Fassung unverändert. Zusätzlich sind ein historischer `.git`-Ordner und eine Fortschritts-TXT enthalten. `Alles alte` war nicht Teil des ZIP; vor Ort separat bewahren.
- Spielcode, Originalkarten, 3 Spielerslots, lokales Passworttor, Tests und Dokumentation befinden sich unter `src/`, `assets/`, `data/`, `tests/`, `tools/`, `docs/`.
- **NICHT** auf GitHub: `archiv/`, `Alles alte/`, `.git` aus dem alten Hauptverzeichnis, `.env`, Schlüssel, `tor.json`, private Saves, alte Build-Ausgaben. Ein Ignoriermuster entfernt nie bereits getrackte Geheimnisse aus der Historie.
- **Urheber-/Nutzungsrechte** an historischen Grafiken, Screenshots und Originalunterlagen vor öffentlicher Verteilung separat klären.
- Echte Tests unter Windows vor einem Release: Start, eigenes neues Passwort, 10×10-Karte, Bau-/Ortskasse, Produktion, Save/Load, Adminzugang, Kampf, mehrere Neustarts.

## Vorsichtiges GitHub-Verfahren

1. Nur im vorhandenen GitHub-Clone `D:\Arbeiten\Nebelseetal_Remake_GitHub` arbeiten, nicht den `\.git`-Ordner aus `D:\Arbeiten\Nebelseetal_Remake` übertragen.
2. In GitHub Desktop sicherstellen, dass keine fremden uncommitteten Änderungen bestehen. Vor größerem Merge eine Sicherung oder einen neuen Branch anlegen.
3. Aus der neuen Hauptfassung nach inhaltlicher Freigabe nur **aktive** Ordner `src`, `assets`, `data`, `tests`, `tools`, `docs` und `.github` sowie die aktiven Root-Dateien in den GitHub-Clone übernehmen. Historische, im Remote bislang getrackte Pfade gezielt entfernen; nicht bloß neue Dateien darüberkopieren.
4. In GitHub Desktop das vollständige Änderungsdiff sorgfältig durchsehen, insbesondere `docs/` und entfernte Altpfade. Keinen Ordner `archiv/`, `Alles alte/` oder individuelle Passwort-/Spielstanddateien committen.
5. Erste Veröffentlichung als **Entwicklungsversion** committen/pushen, ohne Windows-Releaseversprechen. Danach online `docs/ENTWICKLUNGSPROTOKOLL.md` und `docs/AKTUELLER_STAND.md` kontrollieren.
6. Für Windows-EXE im GitHub-Repository unter **Actions → Windows-Test-EXE bauen → Run workflow** den vorhandenen manuellen Build starten. Das Workflow-Artefakt `Nebelseetal_Remake_Windows_Test_EXE` ist noch kein Release und kann zeitlich verfallen.
7. Artefakt herunterladen, unter Windows prüfen und Testergebnisse/Hash dokumentieren. Erst **danach** unter **Releases → Draft a new release** eine als *Pre-release* gekennzeichnete Testversion samt geprüfter EXE und Changelog hochladen.
8. Hermes soll künftig nach geprüften Änderungen die öffentliche Version, Issues, README, aktuellen Status und das einzige Entwicklungsprotokoll selbst pflegen. Freigabe und Entscheidungen bleiben bei Hermes.

## Bekannte technische Grenzen

- Vollständige Testsuite und echter Windows-EXE-Start sind noch offen.
- 25 Originalkartenraster nicht manuell validiert; historisches Baumenü, Botökonomie und Belagerung unvollständig.
- Öffentliche Kopie enthält absichtlich nicht das lokale historische Archiv/den alten Git-HEAD. Alte Commits im Protokoll sind daher im öffentlichen Clone möglicherweise nicht verifizierbar; der lokale Hermes-Git-Stand muss für vollständigen historischen Prüfbeleg bewahrt bleiben.
- Die Protokollprüfung meldet 24 historisch anders formulierte Absatzanfänge als Befund; nicht als behoben einstufen.
