@echo off
rem ============================================================
rem  Nebelseetal Remake - alle Pruefungen in einem Aufruf
rem  Laeuft ohne sichtbares Spielfenster.
rem ============================================================
title Nebelseetal Remake - Pruefungen
cd /d "%~dp0"
set PYTHONUTF8=1
rem FIX04: Gleiches Windows-Python wie der funktionierende Spielstarter verwenden.
if not defined LOCALAPPDATA set "LOCALAPPDATA=%USERPROFILE%\AppData\Local"
if exist "%LOCALAPPDATA%\Microsoft\WindowsApps" set "PATH=%PATH%;%LOCALAPPDATA%\Microsoft\WindowsApps"
set "PY_RUN="
where py >nul 2>&1
if not errorlevel 1 (
    py -V:Astral/CPython3.11.16 -c "import tkinter" >nul 2>&1
    if not errorlevel 1 set "PY_RUN=py -V:Astral/CPython3.11.16"
)
if not defined PY_RUN (
    where py >nul 2>&1
    if not errorlevel 1 set "PY_RUN=py -3"
)
if not defined PY_RUN (
    where python >nul 2>&1
    if not errorlevel 1 set "PY_RUN=python"
)
if not defined PY_RUN (
    echo FEHLER: Kein verwendbares Windows-Python gefunden.
    pause
    exit /b 1
)
set FEHLER=0
for %%T in (tests\test_originalkarten_only.py tests\test_originalkarten_savegames.py tests\test_gpt_originalkarten_feldklick.py tests\test_gpt_originalkarten_baukasse.py tests\test_gpt_baumenue_kategorien_fix04.py tests\test_gpt_baumenue_standorttipps_fix04b.py tests\test_gpt_spielerhilfe_goetterschutz_fix04c.py tests\test_gpt_admin_spielerhilfe_fix04d.py tests\test_gpt_admin_hilfe_navigation_fix04e.py tests\test_gpt_pflicht_starthilfe_fix04f.py tests\test_gpt_spielstandarchiv_fix04g.py tests\test_gpt_spielstand_gui_fix04h.py tests\test_gpt_schild_nebenfenster_fix04i.py tests\test_public_edition_fix04j.py tests\test_gpt_spielzeit_einstellungen_fix05.py tests\test_fehlbestand.py tests\test_gebaeude_menue_und_meldungen.py tests\test_baseline.py tests\test_spieldaten.py tests\test_kampf.py tests\test_forschung.py tests\test_welt.py tests\test_tor.py tests\test_forschung_wirkung.py tests\test_werkstatt.py tests\test_portalraum.py tests\test_punkte.py tests\test_kampfbericht.py tests\test_spielschicht.py tests\test_botkern.py tests\test_speichern_robust.py tests\test_oberflaeche_original.py tests\test_auftraege.py tests\test_w8_einhaengung.py tests\test_punkte_einhaengung.py tests\test_kampf_einhaengung.py tests\test_gui_fehler.py tests\test_durchspiel.py tests\test_startspiel.py tests\test_zieluebergabe.py tests\test_loadingpage.py tests\test_exe_symbol.py tests\test_protokoll.py tests\test_weltkarte.py tests\test_karten_optik.py tests\test_welt_optik.py tests\test_ausruestung.py tests\test_forschungspfad.py tests\test_karten_optik_fein.py tests\test_welt_optik_fein.py tests\test_warenrezepte.py tests\test_oekonomie_kern_10x10_nachfolger.py tests\test_lokale_lager.py tests\test_warentransport.py tests\test_ausbildungsauftraege.py tests\test_oekonomie_uhr.py tests\test_lokale_forschung.py tests\test_handel_transaktion.py tests\test_gpt_waren_icons.py) do (
    echo.
    echo ########## %%T ##########
    %PY_RUN% "%%T"
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
