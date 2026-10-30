#requires -Version 5.1
# NEBELSEETAL GPT-FIX02d-R2: Nur README fuer Spielstart; Hermes-Uebergabe fuer Agent.
# Keine Spielcodeaenderungen, kein Loeschen, kein GitHub-Push.
$ErrorActionPreference = 'Stop'
$utf8 = New-Object System.Text.UTF8Encoding($false)
$root = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$archRel = 'archiv\ordnungsbereinigung_FIX02d_20261028'
$arch = Join-Path $root $archRel
$kennung = 'GPT-FIX02d-R2 - README und Hermes-Uebergabe als einzige Einstiege'

function At([string]$name) { Join-Path $root $name }
function Load([string]$file) { [System.IO.File]::ReadAllText($file, [System.Text.Encoding]::UTF8) }
function Save([string]$file,[string]$value) { [System.IO.File]::WriteAllText($file,$value,$utf8) }
function Digest([string]$file) { (Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash }
function AppendOnce([string]$relative,[string]$content) {
  $path=At $relative; $prev=Load $path
  if (!$prev.Contains($kennung)) { Save $path ($prev.TrimEnd() + "`r`n`r`n" + $content.Trim() + "`r`n") }
}

try {
  Write-Host 'NEBELSEETAL - FIX02d-R2 (README + Hermes-Uebergabe, keine START_HIER.txt)' -ForegroundColor Cyan
  $needed = @(
    'src\main.py','src\originalkarten.py','README.md','START_SPIEL_WINDOWS.bat',
    'EXE_ERSTELLEN_WINDOWS.bat','START_EXE_TEST_WINDOWS.bat','run_tests.bat',
    'docs\AKTUELLER_STAND.md','docs\ORDNUNG.md','docs\WINDOWS_EXE_HERSTELLUNG.md',
    'docs\HERMES_UEBERGABE_AKTUELL.md','docs\HERMES_KONTROLLE_UND_SKILLS.md',
    'docs\ENTWICKLUNGSPROTOKOLL.md'
  )
  foreach ($name in $needed) {
    if (!(Test-Path -LiteralPath (At $name) -PathType Leaf)) { throw "Fehlende Projektdatei: $name. ABBRUCH vor Aenderungen." }
  }
  if (Test-Path -LiteralPath (Join-Path $arch 'DATEIUMZUEGE.json')) {
    throw 'Im Ziel liegt schon ein FIX02d-Umzugsmanifest. Nicht blind erneut ausfuehren; bitte pruefen.'
  }
  $protokoll=At 'docs\ENTWICKLUNGSPROTOKOLL.md'
  if ((Load $protokoll).Contains($kennung) -or (Load $protokoll).Contains('GPT-FIX02d – Bereinigung von Startanleitungen')) {
    throw 'Eine FIX02d-Bereinigung ist bereits protokolliert. Vor weiterem Lauf den Ist-Stand pruefen.'
  }
  $readme=Load (At 'README.md')
  if ($readme -notmatch 'START_SPIEL_WINDOWS\.bat') { throw 'README enthaelt keinen erwarteten Windows-Startpfad. Keine Aenderung.' }
  if ($readme -match '(?m)^## Spiel unter Windows starten\s*$') { throw 'README ist bereits auf die neue Einstiegskonvention umgestellt.' }

  # Alle Aenderungen vorab sichern; fehlende optionale Altdateien einfach vermerken.
  $documents = @(
    'README.md','docs\AKTUELLER_STAND.md','docs\ORDNUNG.md',
    'docs\WINDOWS_EXE_HERSTELLUNG.md','docs\HERMES_UEBERGABE_AKTUELL.md',
    'docs\HERMES_KONTROLLE_UND_SKILLS.md','docs\ENTWICKLUNGSPROTOKOLL.md'
  )
  $moves=@(
    @{from='START_HIER.txt'; to='alte_anleitungen\START_HIER.txt'},
    @{from='PROJEKTUEBERSICHT_WINDOWS.txt'; to='alte_anleitungen\PROJEKTUEBERSICHT_WINDOWS.txt'},
    @{from='NEBELSEETAL_FIX02_FORTSCHRITT_WINDOWS.txt'; to='alte_berichte\NEBELSEETAL_FIX02_FORTSCHRITT_WINDOWS.txt'},
    @{from='NEBELSEETAL_FIX02c_PRUEFBERICHT_WINDOWS.txt'; to='alte_berichte\NEBELSEETAL_FIX02c_PRUEFBERICHT_WINDOWS.txt'},
    @{from='Nebelseetal_Remake.bat'; to='alte_startskripte\Nebelseetal_Remake.bat'},
    @{from='EXE_NEUESTEN_STAND_BAUEN.bat'; to='alte_startskripte\EXE_NEUESTEN_STAND_BAUEN.bat'}
  )
  foreach ($m in $moves) {
    if ((Test-Path -LiteralPath (At $m.from) -PathType Leaf) -and (Test-Path -LiteralPath (Join-Path $arch $m.to))) {
      throw "Archivziel schon vorhanden: $($m.to). Nichts wird ueberschrieben."
    }
  }
  foreach ($d in $documents) {
    if (Test-Path -LiteralPath (Join-Path $arch (Join-Path 'sicherungen_vor_aenderung' $d))) {
      throw "Dokumentensicherung existiert bereits: $d. ABBRUCH."
    }
  }
  Write-Host 'Geplante Aenderungen: 6 optionale Altdateien ins Archiv, 7 Dokumente aktualisieren.' -ForegroundColor Yellow
  Write-Host 'Vorherige Dokumentversionen werden archiviert; kein Spielcode und keine Git-Daten.' -ForegroundColor Yellow
  $freigabe = Read-Host 'Fortfahren? Bitte JA eingeben (alles andere bricht ab)'
  if ($freigabe -cne 'JA') { throw 'Vom Benutzer nicht freigegeben; keine Aenderungen vorgenommen.' }
  New-Item -ItemType Directory -Force -Path $arch | Out-Null
  foreach ($d in $documents) {
    $target=Join-Path $arch (Join-Path 'sicherungen_vor_aenderung' $d)
    New-Item -ItemType Directory -Force -Path (Split-Path $target -Parent) | Out-Null
    Copy-Item -LiteralPath (At $d) -Destination $target
  }
  $moved=@()
  foreach ($m in $moves) {
    $source=At $m.from
    if (Test-Path -LiteralPath $source -PathType Leaf) {
      $target=Join-Path $arch $m.to
      New-Item -ItemType Directory -Force -Path (Split-Path $target -Parent) | Out-Null
      $sha=Digest $source
      Move-Item -LiteralPath $source -Destination $target
      $moved += [pscustomobject]@{alter_pfad=$m.from; neuer_pfad="$archRel\$($m.to)"; sha256=$sha; aktion='Archiviert, nicht geloescht'}
      Write-Host "Archiviert: $($m.from)" -ForegroundColor DarkGray
    } else {
      $moved += [pscustomobject]@{alter_pfad=$m.from; neuer_pfad=$null; sha256=$null; aktion='Nicht vorhanden; keine Aenderung'}
    }
  }

  # README bleibt Benutzer-/GitHub-Einstieg und erklaert das Starten selbst.
  $lines=@($readme -split '\r?\n' | Where-Object { $_ -notmatch '^\s*-\s*`START_HIER\.txt`' })
  $readme=$lines -join "`r`n"
  $section=@'
## Spiel unter Windows starten

1. **Python 3 fuer Windows** mit Tkinter benoetigt (bei der regulaeren Python-Installation dabei).
2. Im Projekt-Hauptordner `START_SPIEL_WINDOWS.bat` doppelklicken. Dadurch startet der **aktuelle Quellcode** aus `src/`, nicht eine alte EXE.
3. Beim ersten Spielstart legt jeder Spieler sein **eigenes lokales Passwort** fest. Keine Passwortdateien aus dem Projekt oder von anderen Personen uebernehmen.
4. Ein neuer, **noch nicht freigegebener Windows-EXE-Build** laesst sich mit `EXE_ERSTELLEN_WINDOWS.bat` erzeugen. Danach unbedingt `START_EXE_TEST_WINDOWS.bat` ausfuehren und den Spielablauf kontrollieren.
5. `run_tests.bat` startet Tests; Exitcodes **und** Fehlermeldungen beachten. Ein erfolgreicher Teiltest ist noch keine Releasefreigabe.

Details: [Windows-Testanleitung](docs/SPIEL_TESTEN.md), [EXE-Erstellung](docs/WINDOWS_EXE_HERSTELLUNG.md).

**Fuer Hermes:** Die einzige aktuelle Agenten-Uebergabe ist [docs/HERMES_UEBERGABE_AKTUELL.md](docs/HERMES_UEBERGABE_AKTUELL.md). Historische Start- und Uebergabetexte liegen im `archiv/`, nicht als zweiter aktiver Einstieg.
'@
  if ($readme.Contains('## Ordner')) {
    $readme=$readme.Replace('## Ordner',$section.TrimEnd() + "`r`n`r`n## Ordner")
  } else {
    $readme=$readme.TrimEnd() + "`r`n`r`n" + $section.Trim() + "`r`n"
  }
  Save (At 'README.md') $readme

  # Gueltige Dokumentation: keine Altstarter-Verweise mehr als Anweisungen.
  foreach ($name in @('docs\AKTUELLER_STAND.md','docs\WINDOWS_EXE_HERSTELLUNG.md','docs\ORDNUNG.md','docs\HERMES_UEBERGABE_AKTUELL.md')) {
    $p=At $name; $content=(Load $p).Replace('EXE_NEUESTEN_STAND_BAUEN.bat','EXE_ERSTELLEN_WINDOWS.bat')
    if ($name -eq 'docs\HERMES_UEBERGABE_AKTUELL.md') {
      $content=$content.Replace('`START_HIER.txt`','`README.md`')
    }
    Save $p $content
  }
  $skill=Load (At 'docs\HERMES_KONTROLLE_UND_SKILLS.md')
  $skill=$skill.Replace('`START_HIER.txt`','`README.md`')
  Save (At 'docs\HERMES_KONTROLLE_UND_SKILLS.md') $skill

  AppendOnce 'docs\ORDNUNG.md' @'
## GPT-FIX02d-R2 - Ein einziger Einstieg je Zielgruppe

`README.md` ist die einzige aktive Anleitung fuer Besucher und Windows-Spielstart. `docs/HERMES_UEBERGABE_AKTUELL.md` ist die einzige aktuelle Anweisung fuer Hermes. `docs/ENTWICKLUNGSPROTOKOLL.md` bleibt die einzige aktive Chronik. Eine separate aktuelle `START_HIER.txt` gibt es **nicht** mehr. Alte Einstiegstexte, zwei Berichte und doppelte .bat-Wrapper liegen mit SHA-256-Nachweisen unter `archiv/ordnungsbereinigung_FIX02d_20261028/`; der alte Stand ist nur historisch. Aktive Starter: `START_SPIEL_WINDOWS.bat`, `EXE_ERSTELLEN_WINDOWS.bat`, `START_EXE_TEST_WINDOWS.bat`, `run_tests.bat`.
'@
  AppendOnce 'docs\HERMES_KONTROLLE_UND_SKILLS.md' @'
## GPT-FIX02d-R2 - Projektordnung als lernender Cleanup-Check

**Ab jetzt keine `START_HIER.txt` und keine zweite aktuelle Projektuebersicht anlegen.** Start-/Testanleitung gehoert in `README.md`, Hermes-Checkliste und Arbeitsauftrag nach `docs/HERMES_UEBERGABE_AKTUELL.md`, Entwicklungen nach `docs/ENTWICKLUNGSPROTOKOLL.md`, spielbereichsbezogener Ist-Stand nach `docs/AKTUELLER_STAND.md`. Kein zweites Statusdokument. Beim Laptop-Cleanup nach **verifizierten** Duplikaten, alten Links und unbenutzten Dateien suchen; nur Belege + Vorschlaege liefern, nicht automatisch verschieben/loeschen. SHA-256 und Alt->Neu-Pfad, Leser/Imports und Testfolgen dokumentieren. `tools/projekt_ordnung_audit.py` ist ein read-only Werkzeug, das Hermes nach Pruefung in seinen bereits bestehenden Cleanup-Cronjob integrieren soll. Noch kein Cronjob und kein Hermes-Skill wurden durch ChatGPT auf Daniels Laptop veraendert.
'@
  AppendOnce 'docs\HERMES_UEBERGABE_AKTUELL.md' @'
## GPT-FIX02d-R2 - Verbindliche aktuelle Einstiegskonvention (28.10.2026)

**Vorrang vor allen aelteren Start-Hier-Hinweisen:** Es gibt **keine aktive `START_HIER.txt`**. Fuer Spieler, technische Nutzer und GitHub gilt `README.md` (enthaelt jetzt Python-Spielstart, Passwort beim Erststart, aktuelle EXE-Bauanleitung und Testhinweise). Fuer dich, Hermes, gilt **dieses Dokument** als einziger Wiedereinstieg. Die einzige aktive Chronik ist `docs/ENTWICKLUNGSPROTOKOLL.md`, der kompakte Ist-Stand ist `docs/AKTUELLER_STAND.md`. Bestehende Roadmap und Skills bleiben bestehen. Historische Anleitungen, Statusfassungen und doppelte .bat-Wrapper liegen mit Alt->Neu-Pfaden und SHA-256 unter `archiv/ordnungsbereinigung_FIX02d_20261028/DATEIUMZUEGE.json`.

**Beim Wiederanlauf:** (1) Diese Uebergabe und `docs/AKTUELLER_STAND.md`, dann das zentrale Protokoll lesen; keine historische Anleitung als aktive Anweisung behandeln. (2) Den lokalen Git-HEAD mit dieser Arbeitskopie und dem GitHub-Remote vergleichen; `Alles alte` bleibt privat und unangetastet. (3) Den bestehenden Laptop-Cleanup-Cronjob und vorhandene Projektordnungs-Skills erst auslesen und sichern; eine **lesende** Pruefung fuer doppelte Einstiege, tote Links und zusammenfassbare Dokumente ergaenzen, NICHT einen neuen Job anlegen. (4) Aenderungen fuer Daniel **proaktiv vorschlagen**: Pfad, Quelle, SHA-256, Abhaengigkeiten, Testauswirkung, Rueckweg. Keine automatische Loeschung oder Verschiebung aktiver Dateien durch Cleanup. (5) Nach Freigabe ordnungsgemaess archivieren, Code-/Test-/Buildreferenzen pruefen, das EINZIGE Protokoll ergaenzen und aus bestaetigten Ursachen neue Skillregeln ableiten; keine doppelten Skills. (6) Aktuelle Windows-EXE ist noch nicht erstellt oder getestet; GitHub bleibt bis zur Freigabe unveraendert. Nach realem Windows-Test und Secret-/Rechtepruefung die neue GitHub-Version pflegen.

**Rollen:** ChatGPT ist voruebergehend Coding-Zuarbeit. Hermes bleibt alleiniger, uneingeschraenkter Head-Koordinator. Die lokale Cronjob-Integration ist **nur beauftragt**, nicht schon umgesetzt.
'@
  AppendOnce 'docs\ENTWICKLUNGSPROTOKOLL.md' @'
## GPT-FIX02d-R2 - Startdokumente vereinheitlicht (28.10.2026)

**Nutzerentscheidung:** Keine eigene `START_HIER.txt`. Nur `README.md` als Spielstart-/GitHub-Einstieg und `docs/HERMES_UEBERGABE_AKTUELL.md` als alleinige aktuelle Hermes-Uebergabe; nur `docs/ENTWICKLUNGSPROTOKOLL.md` als aktives Protokoll. Bisherige Statusdatei `docs/AKTUELLER_STAND.md` bleibt einzige spielbereichsbezogene Kurzuebersicht.

**Durchgefuehrte Aenderungen:** `START_HIER.txt`, `PROJEKTUEBERSICHT_WINDOWS.txt`, historische FIX02/FIX02c-Berichte sowie `Nebelseetal_Remake.bat` und `EXE_NEUESTEN_STAND_BAUEN.bat` wurden, soweit vorhanden, **archiviert statt geloescht**. `README.md` um aktuelle Windows-Spielstart-/Buildhinweise erweitert. Referenzen in `docs/AKTUELLER_STAND.md`, `docs/WINDOWS_EXE_HERSTELLUNG.md`, `docs/ORDNUNG.md`, `docs/HERMES_UEBERGABE_AKTUELL.md` und `docs/HERMES_KONTROLLE_UND_SKILLS.md` an die neue Einstiegsregel und das aktive Buildskript angepasst. Read-only-Ordnungspruefer in `tools/projekt_ordnung_audit.py` aktualisiert. Rueckweg: vollstaendige Sicherungen bearbeiteter Dokumente plus `archiv/ordnungsbereinigung_FIX02d_20261028/DATEIUMZUEGE.json` (Alt->Neu mit SHA256).

**Sicherheitsgrenzen:** Kein aktiver `src`-/`assets`-/`data`-Code geaendert, keine Passwoerter/Spielstaende/Git-Historie geloescht. Kein Github-Push; keine angeblich aktuelle EXE. Hermes-Cronjob/Skills auf Daniels Rechner wurden nicht direkt angepasst: Hermes muss sie spaeter read-only pruefen und als Koordinator nach Uebernahme integrieren. Alte Abschnitte dieser Chronik erwaehnen natuerlich die damals gueltigen `START_HIER`-Wege und bleiben als unveraenderte Historie erhalten.

**Offene Aufgaben:** Vollstaendige Testsuite, Windows-EXE und Praxistest, 25 visuelle Kartenraster, weitere Wirtschaft-/Bot-/UI-Fragen, spaetere freigegebene GitHub-Aktualisierung.
'@

  AppendOnce 'docs\HERMES_KONTROLLE_UND_SKILLS.md' @'
## Hardware-Rahmen fuer ressourcenschonende Entwicklung (GPT-FIX02d-R2)

Daniels Testrechner: Windows 11 Home x64, Windows-Build 26300 (Angabe vom 28.10.2026), Intel 64-Bit-CPU (ca. 2,3 GHz), rund **12 GB RAM**. Bei der Auskunft waren nur ca. **3,1 GB physischer RAM frei**; das ist eine Momentaufnahme, nicht dauerhaft verfuegbarer Speicher. Vor grossem EXE-Build freien RAM und **freien Festplattenspeicher** neu pruefen; letzterer wurde nicht angegeben. Python und PyInstaller in 64 Bit verwenden, Builds/Tests nacheinander statt parallel ausfuehren, unnoetige speicherintensive Programme schliessen. Unter Windows pruefen: Interpreter, Tkinter, Compiler-/Build-Log, Dateipfade, Laufzeitstart, Grafik/Originalkarten, Spielstand. Nichts als Windows-verifiziert bezeichnen, was nur unter Linux geprueft wurde.

**Datenschutz:** E-Mail, Windows-Produkt-ID, Netzwerkadressen, Hostname, exakte BIOS-Kennungen und andere nutzerbezogene Systeminformationen NICHT in Repo, Diagnoselogs oder externe Uebergaben uebernehmen. Nur notwendige, nicht identifizierende System- und Ressourcenangaben sind hier festgehalten. Keine versteckte Telemetrie, keine automatischen Downloads ohne Freigabe. Fuer den bereits bestehenden Laptop-Cleanup zuerst reale Aufgabenplanung/Task-Scheduler/Cron-Definition sowie bestehende Skills feststellen; nur einen read-only Vorschlag fuer Ordnungsscans an passender Stelle integrieren und keinesfalls mehrere redundante Cleanup-Jobs anlegen.
'@
  AppendOnce 'docs\HERMES_UEBERGABE_AKTUELL.md' @'
## GPT-FIX02d-R2 - Technische Windows-Umgebung und sichere Ausfuehrung

Bekannter Zielrechner: Windows 11 Home x64 (Build 26300), Intel 64-Bit-Prozessor ca. 2,3 GHz, 12 GB physischer Speicher; beim Nutzerbericht waren rund 3,1 GB davon frei. Das ist keine dauerhafte Verfuegbarkeitsgarantie. Vor groesseren Tests/EXE-Build Festplattenspeicher und freien RAM neu messen. **Keine parallelen Schwerlast-Builds**. Windows-EXE separat mit 64-Bit-Python und Tkinter erstellen, anschliessend reale GUI-/Save-/Originalkarten-Rauchtests. Den Build nicht automatisch nach GitHub pushen; erst manuelle Freigabe. Nutzeridentifikatoren, E-Mail, Produkt-IDs, IP-Adressen und BIOS-Serien nicht in Projektberichte schreiben.
'@
  AppendOnce 'docs\ENTWICKLUNGSPROTOKOLL.md' @'
### Nachtrag Hardware und Cleanups (GPT-FIX02d-R2)

Fuer kuenftige Windows-Pruefungen: 64-Bit-Windows 11, rund 12 GB RAM, zuletzt ca. 3 GB frei. Darum serielle, ressourcenschonende Builds vorsehen und Systemressourcen zum Zeitpunkt des Builds erneut messen. Keine identifizierenden Rechner-/Kontodaten in Projektdateien uebernehmen. Hermes soll nach Wiederanlauf seinen **bestehenden** Laptop-Cleanup und die vorhandenen Skills pruefen und Vorschlaege zur Erkennung redundanter Projekttexte selbststaendig integrieren; noch keine reale Job-/Skill-Aenderung durch GPT.
'@

  $manifest=[pscustomobject]@{
    kennung='GPT-FIX02d-R2'; datum='2026-10-28'; zweck='README Spielstart, Hermes-Handover Agenteneinstieg; kein START_HIER.txt'
    archivpfad=$archRel; verschoben=$moved; dokumentensicherungen=$documents
    aktiv=@('README.md','docs/AKTUELLER_STAND.md','docs/ENTWICKLUNGSPROTOKOLL.md','docs/HERMES_UEBERGABE_AKTUELL.md','START_SPIEL_WINDOWS.bat','EXE_ERSTELLEN_WINDOWS.bat','START_EXE_TEST_WINDOWS.bat','run_tests.bat')
    codegeaendert=$false; windows_exe_gebaut=$false; github_aktualisiert=$false
    hermes_cleanup='Lernregel beauftragt, Cronjob und Skills nach Wiederanlauf von Hermes pruefen und aktualisieren'
  }
  Save (Join-Path $arch 'DATEIUMZUEGE.json') ($manifest | ConvertTo-Json -Depth 10)
  Write-Host 'ERFOLG: Keine aktive START_HIER.txt. README ist Spielstart, Hermes-Uebergabe Agenteneinstieg.' -ForegroundColor Green
  Write-Host "Archiv / Rueckweg: $arch"
  Write-Host 'Windows-EXE und GitHub-Push sind weiterhin offen.'
  exit 0
} catch {
  Write-Host ('FEHLER: ' + $_.Exception.Message) -ForegroundColor Red
  Write-Host 'Bei einem Fehler NICHT erneut blind ausfuehren. Archiv/Sicherungen kontrollieren.' -ForegroundColor Yellow
  exit 1
}
