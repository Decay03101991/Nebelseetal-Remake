@echo off
rem ============================================================
rem  Nebelseetal Remake - alle Pruefungen in einem Aufruf
rem  Laeuft ohne sichtbares Spielfenster.
rem ============================================================
title Nebelseetal Remake - Pruefungen
cd /d "%~dp0"
set PYTHONUTF8=1
set FEHLER=0
for %%T in (tests\test_baseline.py tests\test_spieldaten.py tests\test_kampf.py tests\test_gelaende.py tests\test_siedlungskarte.py tests\test_kartenansicht.py tests\test_berater.py tests\test_wirtschaft.py tests\test_forschung.py tests\test_welt.py tests\test_ertrag_anbindung.py tests\test_gebaeude_wirkung.py tests\test_tor.py tests\test_forschung_wirkung.py tests\test_werkstatt.py tests\test_portalraum.py tests\test_punkte.py tests\test_kampfbericht.py tests\test_spielschicht.py tests\test_botkern.py tests\test_speichern_robust.py tests\test_oberflaeche_original.py tests\test_auftraege.py tests\test_w8_einhaengung.py tests\test_punkte_einhaengung.py tests\test_kampf_einhaengung.py tests\test_gui_fehler.py) do (
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
