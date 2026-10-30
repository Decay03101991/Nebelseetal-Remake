@echo off
setlocal EnableExtensions
cd /d "%~dp0" || exit /b 1
if not exist "%~dp0Nebelseetal_Remake.exe" (
  echo Noch keine aktuelle EXE. Bitte EXE_ERSTELLEN_WINDOWS.bat zuerst ausfuehren.
  pause
  exit /b 1
)
if not defined LOCALAPPDATA set "LOCALAPPDATA=%USERPROFILE%\AppData\Local"
set "NEBEL_SPIELDATEN_ORDNER=%LOCALAPPDATA%\Nebelseetal_Remake\KONSOLIDIERT_20261028"
"%~dp0Nebelseetal_Remake.exe"
if errorlevel 1 (echo Die Test-EXE endete mit einem Fehler. & pause & exit /b 1)
