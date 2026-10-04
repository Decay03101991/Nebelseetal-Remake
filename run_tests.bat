@echo off
rem ============================================================
rem  Nebelseetal Remake - alle Pruefungen in einem Aufruf
rem  Laeuft ohne sichtbares Spielfenster.
rem ============================================================
title Nebelseetal Remake - Pruefungen
cd /d "%~dp0"
set PYTHONUTF8=1
python "tests\test_baseline.py"
echo.
echo Rueckgabewert: %ERRORLEVEL%  (0 = keine Fehler)
pause
