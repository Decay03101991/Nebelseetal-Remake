# Aktuelle Windows-EXE erstellen und pruefen

**Status 28.10.2026:** In dieser Arbeitsumgebung laeuft Linux. Es liegt **noch keine neu kompilierte, auf Windows geprüfte EXE** im ZIP. Eine alte EXE aus dem Originalarchiv darf nicht als neue Version ausgegeben werden. Es gibt keine Releasefreigabe.

## Auf deinem Windows-PC (einfachste Methode)

1. Neues ZIP separat entpacken, `Nebelseetal_Remake` oeffnen.
2. Python 3 fuer Windows installieren (falls nicht vorhanden; bei Tkinter Standardinstallation).
3. **`EXE_ERSTELLEN_WINDOWS.bat` doppelklicken**. Das Skript verwendet die aktuell enthaltenen `src/`, `data/`, `assets/`, installiert PyInstaller bei Bedarf in eine lokale virtuelle Umgebung und bricht bei Vorpruefungsfehlern ab. Erstmalig Internet benoetigt.
4. Nach Erfolg entsteht `Nebelseetal_Remake.exe` **direkt im gleichen Hauptordner**, niemals im Archiv.
5. `START_EXE_TEST_WINDOWS.bat` ausfuehren; Erststartpasswort, Spieler-/Adminzugang, Karten, Bau, Rohstoffe, Speichern/Laden, Handel und Kampf einzeln testen. Alle Abweichungen protokollieren. Nur nach erfolgreichen Abnahmetests fuer Tester bereitstellen.

## Optional ohne lokales Build-Werkzeug: GitHub Actions

Die Datei `.github/workflows/windows-test-exe.yml` ist ein **manuell startbarer** Windows-Build. Nach Pruefung und Push des bereinigten Projektstands unter GitHub **Actions -> Windows-Test-EXE bauen -> Run workflow**. Den Windows-Build-Artefakt anschliessend herunterladen. **Nicht** automatisch als offizielles Release veroeffentlicht. Es ist weiter ein GUI-Praxistest erforderlich.

## Wichtige Grenzen

- In dieser Linux-Umgebung ist ein nativer Windows-Build mit PyInstaller nicht moeglich; es wurde keine EXE erstellt oder getestet.
- Der alte Spielstand aus `archiv/` bleibt **nur Nachweis**, keine aktuelle lauffaehige Version.
- Das Passwort wird beim ersten Start vom jeweiligen Benutzer lokal selbst gesetzt; niemals private `tor.json` mitsenden.
- Vor Publikation Sicherheits- und Bildrechtepruefung sowie separate Windows-Spieltests durchfuehren.
