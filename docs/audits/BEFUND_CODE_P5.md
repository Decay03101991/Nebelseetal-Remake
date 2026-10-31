### 1. Befund in fünf Sätzen

Das Projekt ist organisch angewachsen: 49 Dateien mit 21.703 Zeilen, davon 7.375 Zeilen und 240 Methoden allein in `main.py`, inklusive 27 `_render_*`-Methoden. Es gibt mindestens drei echte Duplikatpaare: je eine `fuehre_schlacht` in `kampf.py` (188 Zeilen) und `kampf_alt_handbuch_2009.py` (194 Zeilen) sowie die Render-Paare `karten_optik.py`/`_fein.py` (599/863) und `welt_optik.py`/`_fein.py` (600/898). 47 Funktionen sind 60 oder mehr Zeilen lang, längste ist `_render_settlement_map` mit 205 Zeilen. 58 identische 6-Zeilen-Blöcke belegen fehlende gemeinsame Helfer und erhöhen das Risiko inkonsistenter Fixes. Die Prüfbasis ist mit 98 Dateien und 18.418 Zeilen grundsätzlich vorhanden, aber die konkreten Testdateinamen sind nicht mitgeliefert; deshalb muss `tools/sammellauf.py` als Gesamtbeweis dienen.

---

### 2. Vorschläge

Da die konkreten Testdateinamen in der Aufgabenstellung fehlen, kennzeichne ich erwartbare Testgruppen mit `*`. Der harte Beweis ist immer ein vollständig grüner `tools/sammellauf.py`.

| # | Was | Dateien/Funktionen | Zeilen vorher → nachher | Risiko | Beweis: welche Prüfdatei | Reihenfolge |
|---|---|---|---|---|---|---|
| 1 | Kampf-Duplikat vereinigen | `kampf.py` (398), `kampf_alt_handbuch_2009.py` (401); beide `fuehre_schlacht` | 799 → geschätzt 500–560 | mittel | Offen: erwartbar `tests/test_kampf*.py`; sonst Sammellauf | 1 |
| 2 | `main.py` in UI-Paket entflechten | `main.py` (7375), 27 `_render_*`, `_build_main_ui` | 7375 → geschätzt 2500–3500 in `main.py`/Orchestrierung plus 5–7 Ansichtsmodule | groß | Sammellauf; UI-/Render-Tests, soweit vorhanden | 6 |
| 3 | Karten-/Welt-Optik-Paare vereinigen | `karten_optik.py` (599) + `_fein.py` (863); `welt_optik.py` (600) + `_fein.py` (898) | 2960 → geschätzt 2200–2400 | mittel/groß | Offen: erwartbar `tests/test_karten_optik*.py`, `tests/test_welt_optik*.py`; sonst Sammellauf | 3 |
| 4 | Alt-Original-Dateien stilllegen | `oberflaeche_original.py` (185), `gildenrangliste_original.py` (48), `originalkarten.py` (128), `originalkarten_grafik.py` (36) | 397 → 0, falls nachweislich ungenutzt | klein/mittel | Grep auf Importe + Sammellauf; konkrete Tests offen | 2 |
| 5 | Paketstruktur `kern`, `kampfsystem`, `bot`, `persistenz`, `ui`, `admin`, `alt` einführen | 49 Dateien | keine Zeilenänderung | klein/mittel | Sammellauf und `tools/build_exe.py` | 0 |
| 6 | Wiederholte 6-Zeilen-Blöcke als gemeinsame Helfer | 58 Fundstellen | 348 Rohzeilen; geschätzt 150–220 Ersparnis | mittel | Sammellauf; spezifische Tests je Fundstelle nicht benannt | 5 |
| 7 | `spieloekonomie.py` thematisch splitten | `spieloekonomie.py` (1072) | 1072 → geschätzt 3×300–400 | mittel | Offen: erwartbar `tests/test_spieloekonomie*.py`; sonst Sammellauf | 4 |
| 8 | Tests nach Modulgruppen spiegeln | 98 Testdateien | keine Zeilenänderung | klein | `tools/sammellauf.py` bleibt grün | 7 |

---

### 3. Zusammenführung im Detail

#### 3.1 Kampf-Duplikat vereinigen

Bestand: `kampf.py` und `kampf_alt_handbuch_2009.py` enthalten je eine `fuehre_schlacht`; `kampf.py` importiert zusätzlich die alte Fassung.

Neue zentrale Funktion in `src/kampfsystem/kampf.py`:

```python
def fuehre_schlacht(
    angreifer: dict,
    verteidiger: dict,
    *,
    regelwerk: str = "aktuell",
    optionen: dict | None = None,
) -> dict:
```

Kernidee:

- Rückgabe ist immer ein `dict` mit mindestens `gewinner`, `verluste`, `bericht`, `runden`.
- `regelwerk="aktuell"` nutzt den bisherigen Kampfpfad aus `kampf.py`.
- `regelwerk="handbuch_2009"` nutzt die alte Funktion als private `_fuehre_schlacht_handbuch_2009`.
- Weichen Alt und Aktuell in Tests nicht voneinander ab, kann die alte private Fassung später fallen.
- `kampf_alt_handbuch_2009.py` bleibt bis auf Weiteres als dünner Alias-Modul erhalten:

```python
def fuehre_schlacht(*args, **kwargs):
    return kampfsystem.kampf.fuehre_schlacht(*args, regelwerk="handbuch_2009", **kwargs)
```

Sonderfälle: Leere Armeen, fehlende Optionen und Spezialfälle müssen exakt dieselben Dict-Schlüssel liefern wie bisher. Positionsaufrufe werden über eine Kompatibilitätshülle erhalten.

#### 3.2 `main.py`-Rendermethoden entflechten

Bestand: 27 `_render_*`-Methoden in `main.py`; längste ist `_render_settlement_map` mit 205 Zeilen.

Neue Zielaufteilung: `src/ui/hauptfenster.py` für die Fensterklasse, `src/ui/ansichten/` für die Rendermethoden.

Signatur für die neuen Siedlungszeichner:

```python
def zeichne_siedlung(
    canvas: tk.Canvas,
    spiel: object,
    ausschnitt: tuple[int, int, int, int],
    *,
    modus: str = "normal",
    cache: dict | None = None,
) -> None:
```

Kernidee:

- `canvas` ist das Zeichenziel, `spiel` der Zustand, `ausschnitt` der sichtbare Bereich.
- `modus="normal|fein"` schaltet zwischen bisheriger Normal- und Feinzeichnung um.
- `cache=None` bewahrt das bisherige Drawing-Order-Verhalten, wenn keine Cache-Mechanik existierte.
- In `main.py` bleiben die alten `_render_*`-Namen vorerst als dünne Wrapper erhalten, damit Tests und Aufrufer unverändert funktionieren.
- Pixelgleiches Verhalten hat Priorität; die Aufteilung erfolgt entlang der bestehenden Render-Schritte, nicht durch Neuzeichnen.

---

### 4. Was du NICHT anfassen würdest

- **Pixelgenaue Karten- und Weltzeichner**: `karten_optik_fein.py`, `welt_optik_fein.py`. Solange es keine Bild- oder Screenshort-Tests gibt, ist jede Zeichenreihenfolge ein Risiko.
- **Berechnungsreihenfolge in `spieloekonomie.py`**: Rundungen, Multiplikations- und Additionsreihenfolge können Zahlenwerte verändern; besser nur aufteilen, nicht neu sortieren.
- **Speicherformat in `speichern.py`, `spieldaten.py`, `spielstaende.py`**: Alte Spielstände müssen lesbar bleiben.
- **Bot-Heuristiken in `botkern.py`**: Verhalten ist schwer testbar; der bewusst ASCII-gehaltene Code sollte nicht ohne gezielte Bot-Tests angefasst werden.
- **`_build_main_ui`-Layout**: tkinter-Geometrie, Pixelabstände und Pack/Grid-Reihenfolge wirken direkt auf die Bedienung.

---

### 5. Ordnung

Ich würde flach bleiben: sechs Themenpakete unter `src/`, keine tiefen Verschachtelungen. Die bisherigen Top-Level-Modulnamen bleiben als einzeilige Kompat-Shims erhalten, bis Tests und Imports umgestellt sind.

```text
src/
  main.py                         # Einstieg; bleibt zunächst Top-Level
  public_start.py                 # Start-/Pfad-Helfer; bleibt Top-Level

  kern/
    __init__.py
    auftraege.py
    ausruestung.py
    bonus_system.py
    dorfwall.py
    einheiten.py
    fehlbestand.py
    forschung.py
    forschung_wirkung.py
    forschungspfad.py
    gebaeude_wirkung.py
    gelaende.py
    portalraum.py
    punkte.py
    spieloekonomie.py
    spielschicht.py
    spielzeit.py
    tor.py
    versorgungsschutz.py
    welt.py
    wirtschaft.py
    zeitbasis.py

  kampfsystem/
    __init__.py
    kampf.py                       # fusioniert aus kampf.py + kampf_alt_handbuch_2009.py
    kampfbericht.py

  bot/
    __init__.py
    botkern.py
    bot_angriffsplanung.py
    gpt_versorgungsdiagnose.py

  persistenz/
    __init__.py
    speichern.py
    spieldaten.py
    spielstaende.py
    spielstand_archiv.py

  ui/
    __init__.py
    hauptfenster.py                # später aus main.py
    ansichten/
      __init__.py
      siedlung.py
      welt.py
      karte.py
      overlay.py
    ausgabemodus.py
    baumenue_info.py
    berater.py
    spielerhilfe.py
    karten_optik.py                # fusioniert aus karten_optik.py + _fein.py
    welt_optik.py                  # fusioniert aus welt_optik.py + _fein.py

  admin/
    __init__.py
    admin_oberflaeche.py
    admin_teststand.py
    admin_werkzeuge.py

  alt/
    __init__.py
    kampf_alt_handbuch_2009.py     # Alias, solange Imports existieren
    oberflaeche_original.py
    gildenrangliste_original.py
    originalkarten.py
    originalkarten_grafik.py

  # Einzeilige Kompat-Shims, z. B.:
  # kampf.py              -> from kampfsystem.kampf import *
  # karten_optik_fein.py  -> from ui.karten_optik import *
  # welt_optik_fein.py    -> from ui.welt_optik import *
```

```text
tests/
  kern/
    test_*.py
  kampfsystem/
    test_kampf.py
    test_kampfbericht.py
  bot/
    test_botkern.py
    test_bot_angriffplanung.py
  persistenz/
    test_speichern.py
    test_spielstaende.py
  ui/
    test_hauptfenster.py
    test_karten_optik.py
    test_welt_optik.py
  integration/
```

```text
tools/
  sammellauf.py
  build_exe.py
  # optional: tools/import_check.py für unbenutzte Importe/Funktionen
```

#### Umzugsreihenfolge, nach jedem Schritt lauffähig

1. **Basiszustand sichern**: `tools/sammellauf.py` grün dokumentieren.
2. **Paketgerüst anlegen**: `kern`, `kampfsystem`, `bot`, `persistenz`, `ui`, `ui/ansichten`, `admin`, `alt` mit `__init__.py`; noch keine Dateien verschieben.
3. **Kampf-Duplikat bereinigen vor allen Umzügen**: `kampf.py` in `kampfsystem/kampf.py` fusionieren; alte Datei als Alias/Shim erhalten. Sammellauf grün.
4. **Alt-Dateien stilllegen**: `oberflaeche_original.py`, `gildenrangliste_original.py`, `originalkarten.py`, `originalkarten_grafik.py` nach `alt/` verschieben; Root-Shims erhalten. Bei sauberem Grep und grünem Sammellauf entfernbar.
5. **Kernlogik verschieben**: erst abhängigkeitsarme Module wie `zeitbasis.py`, `gelaende.py`, `einheiten.py`, `fehlbestand.py`, dann größere wie `spieloekonomie.py`. Je Welle Root-Shims und Sammellauf.
6. **Kampfsystem, Bot, Persistenz verschieben**: analog in eigene Pakete; Shims.
7. **UI-Rendermodule verschieben und Paare fusionieren**: `karten_optik`/`_fein` und `welt_optik`/`_fein`; Shims für alte Namen.
8. **`main.py` entflechten**: `_render_*`-Methoden nach `ui/ansichten/` extrahieren; alte Methoden als Wrapper in `main.py` belassen.
9. **Tests spiegeln**: 98 Testdateien in passende Pakete verschieben; nur Importpfade anpassen, keine Assertions ändern. Danach Shims bei Bedarf entfernen.
10. **PyInstaller aktualisieren**: `tools/build_exe.py` um `pathex` und `collect_submodules('kern', 'kampfsystem', 'bot', 'persistenz', 'ui', 'admin')` erweitern; Build testen.