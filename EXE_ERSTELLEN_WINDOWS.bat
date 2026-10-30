@echo off
setlocal EnableExtensions DisableDelayedExpansion
cd /d "%~dp0" || (echo FEHLER: Projektordner nicht erreichbar. & pause & exit /b 1)
title Nebelseetal Remake - aktuelle Windows-EXE erstellen

rem FIX03: Bereits lokal bestaetigte Astral Python 3.11.16 (64 Bit) verwenden.
rem WindowsApps-PATH nur fuer dieses Fenster ergaenzen; Hermes/WSL unangetastet.
if not defined LOCALAPPDATA set "LOCALAPPDATA=%USERPROFILE%\AppData\Local"
if exist "%LOCALAPPDATA%\Microsoft\WindowsApps" set "PATH=%PATH%;%LOCALAPPDATA%\Microsoft\WindowsApps"
set "PY_LAUNCHER=py -V:Astral/CPython3.11.16"
set "PYTHONUTF8=1"

if not exist "src\main.py" (echo FEHLER: src\main.py fehlt. & goto :fehler)
where py >nul 2>&1
if errorlevel 1 (
  echo FEHLER: Python Installation Manager ^(py^) nicht erreichbar.
  echo Bitte den funktionierenden Python-Start zuerst pruefen.
  goto :fehler
)
%PY_LAUNCHER% -c "import sys, tkinter, venv; assert sys.platform == 'win32'; assert sys.maxsize > 2**32; print('Python OK:', sys.version.split()[0], sys.executable)" || goto :fehler

rem Build-Umgebung getrennt von Spielcode und Hermes unter LOCALAPPDATA.
set "BUILD_HOME=%LOCALAPPDATA%\Nebelseetal_Remake\gpt_build_20261028"
set "BUILD_PY=%BUILD_HOME%\Scripts\python.exe"
if not exist "%BUILD_PY%" (
  echo Erstelle isolierte Windows-Bauumgebung...
  %PY_LAUNCHER% -m venv "%BUILD_HOME%" || goto :fehler
)
"%BUILD_PY%" -c "import sys, tkinter; assert sys.platform == 'win32'; print('Bauumgebung OK:', sys.version.split()[0])" || (
  echo FEHLER: Vorhandene Bauumgebung nicht verwendbar.
  echo Bitte nicht blind loeschen. Bauumgebung pruefen: "%BUILD_HOME%"
  goto :fehler
)
"%BUILD_PY%" -m pip --version >nul 2>&1
if errorlevel 1 (
  echo Richte pip nur in der isolierten Bauumgebung ein...
  "%BUILD_PY%" -m ensurepip --upgrade || goto :fehler
)
"%BUILD_PY%" -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
  echo PyInstaller fehlt. Installation nur in lokaler Bauumgebung ^(Internet erforderlich^)...
  "%BUILD_PY%" -m pip install --disable-pip-version-check "pyinstaller>=6.22,<7" || goto :fehler
)

echo.
echo Pruefe zuerst die wichtigsten Spieltests...
"%BUILD_PY%" "tools\gpt_windows_vorpruefung.py" || goto :fehler
echo Pruefe EXE-Bauvoraussetzungen...
"%BUILD_PY%" "tools\build_exe.py" --pruefen || goto :fehler
echo Baue jetzt die aktuelle Windows-EXE...
"%BUILD_PY%" "tools\build_exe.py" --python "%BUILD_PY%" || goto :fehler
if not exist "%~dp0Nebelseetal_Remake.exe" (echo FEHLER: Keine neue EXE vorhanden. & goto :fehler)

echo.
echo ERFOLG: Aktuelle Test-EXE liegt im Spiel-Hauptordner.
echo Jetzt START_EXE_TEST_WINDOWS.bat ausfuehren und den Ablauf manuell testen.
echo Keine automatische Releasefreigabe und kein automatischer GitHub-Upload.
pause
exit /b 0

:fehler
echo.
echo BUILD ABGEBROCHEN. Das Spiel und Hermes wurden nicht veraendert.
echo Bitte die gesamte Fehlermeldung sichern. Eine alte EXE nicht als neuen Build ausgeben.
pause
exit /b 1
