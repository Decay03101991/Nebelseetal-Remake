@echo off
setlocal EnableExtensions
cd /d "%~dp0" || (echo FEHLER: Projektordner nicht erreichbar. & pause & exit /b 1)
title Nebelseetal Remake - aktuelle Hauptfassung

rem Testspielstaende lokal und getrennt vom historischen Hauptstand verwalten.
if not defined LOCALAPPDATA set "LOCALAPPDATA=%USERPROFILE%\AppData\Local"
set "NEBEL_SPIELDATEN_ORDNER=%LOCALAPPDATA%\Nebelseetal_Remake\KONSOLIDIERT_20261028"

rem Der Windows-Python-Manager liegt ggf. in WindowsApps, ohne globalen PATH-Eintrag.
rem PATH wird nur fuer dieses Batchfenster ergaenzt.
if exist "%LOCALAPPDATA%\Microsoft\WindowsApps" set "PATH=%PATH%;%LOCALAPPDATA%\Microsoft\WindowsApps"

rem Bevorzugt die bereits gepruefte lokale Windows-Python-Version mit Tkinter.
where py >nul 2>&1
if not errorlevel 1 (
    py -V:Astral/CPython3.11.16 -c "import tkinter" >nul 2>&1
    if not errorlevel 1 goto :start_astral
    py -3 -c "import tkinter" >nul 2>&1
    if not errorlevel 1 goto :start_py
)
where python >nul 2>&1
if not errorlevel 1 (
    python -c "import tkinter" >nul 2>&1
    if not errorlevel 1 goto :start_python
)
echo FEHLER: Keine verwendbare Windows-Python-Installation mit Tkinter gefunden.
echo Getestet: Astral CPython 3.11.16, py -3 und python.
echo Hermes-Python unter WSL ist fuer diesen Windows-Start nicht erforderlich.
pause
exit /b 1

:start_astral
echo Starte mit Windows-Python 3.11.16 ^(Astral^) ...
py -V:Astral/CPython3.11.16 "%~dp0src\main.py"
goto :ende

:start_py
echo Starte mit Windows-Python via py -3 ...
py -3 "%~dp0src\main.py"
goto :ende

:start_python
echo Starte mit Windows-Python via python ...
python "%~dp0src\main.py"
goto :ende

:ende
if errorlevel 1 (
    echo.
    echo FEHLER: Spiel mit Fehlercode beendet. Meldung oben beachten.
    pause
    exit /b 1
)
exit /b 0
