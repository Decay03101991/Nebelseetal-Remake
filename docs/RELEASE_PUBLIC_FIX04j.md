# Öffentliche Windows-Testfassung FIX04j – Veröffentlichungsplan

**Keine Freigabe und noch kein hochgeladenes Release.** Die vorhandene lokale Entwickler-EXE bleibt unangetastet.

## Zwei Fassungen – ein vollständiges GitHub-Repository

GitHub enthält `src/` einschließlich `admin_oberflaeche.py`, `admin_werkzeuge.py`, `admin_teststand.py`, sämtliche anderen relevanten Spielquellen, Tests, Karten, aktive Dokumente, einziges `docs/ENTWICKLUNGSPROTOKOLL.md` und `docs/HERMES_UEBERGABE_AKTUELL.md`. **Die Admin-Module dürfen nicht aus GitHub herausgenommen werden.**

Die öffentliche EXE wird **ausschließlich** aus `src/public_start.py` erzeugt. Dieser Start aktiviert den öffentlichen Spielermodus, verhindert die Auswahl von Admin-Profilen und sperrt direkt auch die Admin-Dialoge. Der öffentliche Test nutzt eigene lokale Spielstands- und Passwortdateien (nicht die Entwicklerdaten). Im gebündelten Python-Programm können technische Teile der Admin-Implementierung weiterhin als Bytecode vorhanden sein; die Sperre ist **keine Sicherheitsgrenze**. Für vollständige technische Entfernung wären größere Refaktorisierungen nötig.

## Windows lokal bauen

1. FIX04j-Patch in das GitHub-arbeitende Projekt (nicht in `Alles alte`) übernehmen. Keine alten Archive oder privaten Laufzeitdaten mitkopieren.
2. Zunächst die vorhandenen Entwickler-EXE/Savegames unverändert lassen. `PUBLIC_TEST_EXE_BAUEN_WINDOWS.bat` vom Projekt-Hauptordner starten. Funktionierender Rechner: Windows 11 x64, vorhandenes Astral CPython 3.11.16+Tkinter; isoliertes PyInstaller 6.x in `%LOCALAPPDATA%`.
3. Das Skript testet den Public-Modus und baut `release_public/Nebelseetal_Remake_Testversion.exe` plus `release_public/Nebelseetal_Remake_Testversion_FIX04j.zip`. Nicht `EXE_ERSTELLEN_WINDOWS.bat` für die öffentliche Fassung verwenden (dieser baut die Admin-Entwicklerversion).
4. EXE **aus dem fertigen ZIP in einen frischen Ordner entpacken** und manuell prüfen: Passwort-Erststart, drei Slots, Karten, Bau, Speichern, Laden, Spielstandverwaltung, **kein Admin-Einstieg**, Fenstergröße/DPI und Fehlerfreiheit. Den lokalen Entwicklermodus gesondert mit `START_SPIEL_WINDOWS.bat` oder der Entwickler-EXE testen.
5. `SHA256SUMS.txt` gegen die EXE prüfen; Größe und Windows-PE-Header werden automatisch kontrolliert. Build ist erst mit manueller EXE-Abnahme testfähig. Exe enthält keine bekannten festen Passwörter.
6. GitHub Desktop: nur aktiven Code, benötigte Assets, Tests, README, docs und Workflow aktualisieren. `archiv/`, `Alles alte`, `.git`, `.env`, `tor.json`, Savegames, Build-EXEs und `release_public/` **nicht** in den Commit aufnehmen. Bereits veröffentlichte Historie separat auf Geheimnisse prüfen.
7. Erst **nach** Klärung der Veröffentlichungsrechte für Originalmaterialien: Änderungen pushen, Commit/Release-Tag dokumentieren; Release über GitHub Releases als **Pre-release** mit dem Public-ZIP und Anforderungs-/Fehlerhinweisen veröffentlichen. Nicht automatisch releasen. Hermes hält das Repository danach laufend aktuell.

## Tester-Info

`release_vorlage/START_HIER.txt` ist ausschließlich eine Beilage im fertigen Test-ZIP, **keine zweite Projekt-Startanleitung**. Hinzu kommen `SYSTEMANFORDERUNGEN.txt`, `BEKANNTE_GRENZEN.txt`, `FEHLER_MELDEN.txt` und `SHA256SUMS.txt`. Vorläufige Systemanforderungen: Windows 11 x64 erprobt, 8 GB RAM nur empfohlener Versuchswert und nicht als echte Mindestanforderung nachgewiesen; ältere Windows-Versionen und ARM ungeprüft. Python für Endnutzer nicht erforderlich, falls die EXE korrekt gebaut wurde.

## Noch offene Entscheidungen

- 25 Kartengrafikraster manuell visuell prüfen, Bot-Ökonomie/Belagerungen fertigstellen, Langzeit-/Volltests.
- Öffentliches Spielstand-Archiv: langfristige Speichergrenze, Aufbewahrungsregel oder Deaktivierung vor regulärem Release entscheiden, **keine unautorisierte automatische Löschung**.
- Lizenz und Rechte für historische Spielgrafiken und Originaldokumente vor öffentlicher Downloadweitergabe nachweisbar freigeben.
- Test auf echten zusätzlichen Windows-Rechnern/DPI und Windows-EXE-Sicherheit.

## Nachweise / Zuständigkeit

ChatGPT: temporärer Coding-Agent in isolierter Kopie, mit Tests, Dokumentation und Buildvorlage. Hermes: alleiniger Head-Koordinator, Prüfer und späterer Pfleger des öffentlichen GitHub-Repositories. Kein automatischer Push, keine automatische Freigabe.
