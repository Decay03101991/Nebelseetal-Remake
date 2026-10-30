@echo off
setlocal
chcp 65001 >nul
echo NEBELSEETAL - STARTDOKUMENTE VEREINHEITLICHEN (FIX02d-R2)
echo README = Spielstart, Hermes-Uebergabe = Agenteneinstieg.
echo Kein Loeschen, kein Spielcode, kein GitHub-Push.
echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0ORDNUNG_FIX02d.ps1"
set "RC=%ERRORLEVEL%"
echo.
if "%RC%"=="0" (echo Erfolgreich abgeschlossen.) else (echo Fehler. Bitte Meldung sichern und nichts erneut blind starten.)
pause
exit /b %RC%
