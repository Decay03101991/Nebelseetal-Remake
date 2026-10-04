@echo off
rem ============================================================
rem  Nebelseetal Remake - alle Pruefungen in einem Aufruf
rem  Laeuft ohne sichtbares Spielfenster.
rem ============================================================
title Nebelseetal Remake - Pruefungen
cd /d "%~dp0"
set PYTHONUTF8=1
set FEHLER=0
for %%T in (tests\test_baseline.py tests\test_spieldaten.py) do (
    echo.
    echo ########## %%T ##########
    python "%%T"
    if errorlevel 1 set FEHLER=1
)
echo.
if "%FEHLER%"=="0" (
    echo GESAMT: keine Fehler.
) else (
    echo GESAMT: FEHLER vorhanden - siehe oben.
)
echo Rueckgabewert: %FEHLER% ^(0 = keine Fehler^)
pause
exit /b %FEHLER%
