@echo off
setlocal EnableExtensions DisableDelayedExpansion
cd /d "%~dp0" || (echo Fehler: Projektordner nicht erreichbar & pause & exit /b 1)
title Nebelseetal - OEFFENTLICHE Windows-Test-EXE (OHNE Admin)
if not defined LOCALAPPDATA set "LOCALAPPDATA=%USERPROFILE%\AppData\Local"
if exist "%LOCALAPPDATA%\Microsoft\WindowsApps" set "PATH=%PATH%;%LOCALAPPDATA%\Microsoft\WindowsApps"
set "PY=py -V:Astral/CPython3.11.16"
set "BUILD_PY=%LOCALAPPDATA%\Nebelseetal_Remake\gpt_build_20261028\Scripts\python.exe"
set "PYTHONUTF8=1"
if not exist "%BUILD_PY%" (
  echo Erzeuge isolierte Bauumgebung...
  %PY% -m venv "%LOCALAPPDATA%\Nebelseetal_Remake\gpt_build_20261028" || goto :error
)
"%BUILD_PY%" -c "import tkinter, sys; assert sys.platform == 'win32'" || goto :error
"%BUILD_PY%" -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
  echo Installiere PyInstaller in die isolierte Bauumgebung...
  "%BUILD_PY%" -m pip install --disable-pip-version-check "pyinstaller>=6.22,<7" || goto :error
)
echo Pruefe den oeffentlichen Build...
"%BUILD_PY%" tools\build_public_exe.py --pruefen || goto :error
"%BUILD_PY%" tests\test_public_edition_fix04j.py || goto :error
echo Baue oeffentliche Test-EXE...
"%BUILD_PY%" tools\build_public_exe.py || goto :error
echo.
echo BUILD ERFOLGREICH. Ergebnisse in release_public\
echo WICHTIG: Test-EXE noch starten, Slots und fehlenden Adminzugang pruefen!
echo Erst danach als GitHub-VORABVERSION veroeffentlichen.
pause
exit /b 0
:error
echo.
echo ABBRUCH: kein Freigabenachweis. Fehlermeldung aufheben.
pause
exit /b 1
