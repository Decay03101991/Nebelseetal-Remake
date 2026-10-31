### 1. Befund in fünf Sätzen

`main.py` bündelt mit 7.375 Zeilen und 240 Methoden fünf getrennte Verantwortlichkeiten: Datenmodelle, Spielzustand, UI-Aufbau, Ansichten und Kartenzeichnung. Die Klasse `GameState` allein hat über 60 Methoden, darunter `tick()`, `save()`, `load()`, gesamte Ökonomie-, Bot-, Auftrags- und Forschungslogik, und müsste dringend in einen eigenen Kern. Die 27 `_render_*`-Methoden wiederholen nahezu alle denselben Aufbau: `content` leeren, Titel-Label setzen, Scrollposition zurücksetzen — das sind schätzungsweise 150–200 redundante Zeilen. Einige Methoden sind ungenutzt, etwa `_render_news` (im Mapping läuft `_render_neuigkeiten`), und `_upgrade_building` ist nur noch eine Umleitungs-Meldung ohne Aufrufer. Die Prüfungen hängen stark an der bestehenden Struktur: Mindestens `tests/test_oberflaeche_original.py`, `tests/test_weltkarte.py`, `tests/test_startspiel.py`, `tests/test_durchspiel.py`, `tests/test_oekonomie_uhr.py` und `tests/test_auftraege.py` müssen nach jedem Schritt grün bleiben; der Gesamtlauf erfolgt über `tools/sammellauf.py`.

### 2. Vorschläge (Tabelle, absteigend nach Nutzen)

| # | Was | Dateien/Funktionen | Zeilen vorher → nachher | Risiko (klein/mittel/groß) | Beweis: welche Prüfdatei | Reihenfolge |
|---|---|---|---|---|---|---|
| 1 | **Spielkern auslagern: Datenmodelle, Konstanten, GameState** – größter Hebel, trennt Logik von UI | `src/spielkern/modelle.py` (Resource, Building, Unit, Research, MapTile, Goods, BotPlayer, Settlement, GOODS, RESOURCES, MAPS, BOTS, etc.) · `src/spielkern/game_state.py` (GameState mit allen Methoden) · `src/spielkern/baupreise.py` (baukosten, kosten_text) · `src/spielkern/menue.py` (menu_sichtbar, menu_fuer_ebene, EBENE_JE_PUNKT, etc.) | ca. 2.600 Zeilen aus `main.py` entfernt (geschätzt) | mittel | `tests/test_oekonomie_uhr.py`, `tests/test_auftraege.py`, `tests/test_spieloekonomie.py`, `tests/test_oekonomie_einhaengung.py`, `tests/test_startspiel.py`, `tests/test_durchspiel.py`; Gesamtlauf `tools/sammellauf.py` | 1 |
| 2 | **GUI-Ansichten als Mixins auslagern** – 27 `_render_*`-Methoden verteilen | `src/gui/ansichten/uebersicht.py`, `siedlung.py`, `welt.py`, `lager.py`, `diplomatie.py`, `forschung.py`, `nachrichten.py`, `simulator.py`, `hilfe.py`, `admin_dialoge.py` | ca. 3.000 Zeilen aus `main.py` entfernt (geschätzt) | mittel | `tests/test_oberflaeche_original.py`, `tests/test_weltkarte.py`, `tests/test_gui_fehler.py`, `tests/test_startspiel.py`, `tests/test_durchspiel.py` | 2 |
| 3 | **Gemeinsamer Render-Helfer einführen** – ersetzt identisches Gerüst der `_render_*`-Methoden | `src/gui/seitenhelfer.py` mit `seite_aufbauen(titel, untertitel, content, reset_scroll=True)` | ca. 150–200 Zeilen gespart (geschätzt) | klein | `tests/test_oberflaeche_original.py`, `tests/test_gui_fehler.py` | 3 |
| 4 | **Weltkarten-Zeichnung auslagern** – `_draw_map`, `_welt_uebersicht_*`, `_welt_zoom`, `_welt_mitte` | `src/gui/welt_zeichnung.py` | ca. 600 Zeilen aus `main.py` entfernt (geschätzt) | mittel | `tests/test_weltkarte.py`, `tests/test_oberflaeche_original.py` | 4 |
| 5 | **Weltkarten-Gebiets-/Detailpanel auslagern** – `_render_maps`, `_welt_gebiet_panel`, `_welt_detail_zeichnen` | `src/gui/ansichten/welt.py` | ca. 450 Zeilen entfernt (geschätzt) | mittel | `tests/test_weltkarte.py`, `tests/test_oberflaeche_original.py` | 5 |
| 6 | **Siedlungskarten-Zeichnung auslagern** – `_zeichne_siedlungskarte`, `_karten_*`-Aktionen | `src/gui/siedlung_zeichnung.py` | ca. 250 Zeilen entfernt (geschätzt) | mittel | `tests/test_oberflaeche_original.py`, `tests/test_gui_fehler.py`, falls vorhanden `tests/test_karten_optik*` | 6 |
| 7 | **Admin-, Tor-, Profil- und Slot-Dialoge auslagern** – `_admin_dialog`, `_spielstand_verwaltung`, `_archiv_wiederherstellung_dialog`, `_slot_auswahl`, `_profil_*` | `src/gui/admin_dialoge.py` | ca. 700 Zeilen entfernt (geschätzt) | klein–mittel | `tests/test_oberflaeche_original.py`, `tests/test_startspiel.py` | 7 |
| 8 | **Tote/veraltete Methoden entfernen bzw. kennzeichnen** – `_render_news` (ungenutzt), `_upgrade_building` (nur Meldung), ggf. weitere ohne Aufrufer | `main.py`/spätere Views | ca. 30–50 Zeilen (geschätzt) | klein | `tests/test_oberflaeche_original.py`; vorher `rg "_render_news|_upgrade_building"` prüfen | 8 |
| 9 | **Menülogik separieren** – `menu_sichtbar`, `menu_fuer_ebene`, `MENU_ANZEIGE`, `MENU_ZUSATZ`, `EBENEN` | `src/gui/menue_helfer.py` | ca. 120 Zeilen entfernt (geschätzt) | klein | `tests/test_oberflaeche_original.py` | 9 |
| 10 | **Kleinere UI-Helfer auslagern** – `_lade_icon`, `_schild_dialog_inhalt`, `_spaltenname`, `_ertrag_kurz` | `src/gui/ui_helfer.py` | ca. 90 Zeilen entfernt (geschätzt) | klein | `tests/test_oberflaeche_original.py`, `tests/test_gui_fehler.py` | 10 |

### 3. Zusammenführung im Detail

#### 3.1 Spielkern auslagern: `GameState` und Datenmodelle

**Ziel:** `main.py` behält nur noch den Einstieg (`main()`, Ladeansicht) und die App-Komposition.  
**Wohin:**

- `src/spielkern/modelle.py`  
  Alle Dataclasses: `Resource`, `Building`, `Unit`, `Research`, `MapTile`, `Goods`, `BotPlayer`, `Settlement`  
  Alle Konstanten: `GOODS`, `SIEDLUNGEN_MAXIMUM`, `KARTENVERSUCHE`, `STAND_VERSION_ALT`, `STAND_VERSION`, `MODUS_NEU`, `MODUS_LEGACY`, `RESOURCES`, `RESOURCE_ICONS`, `BUILDINGS`, `UNIT_ICONS`, `UNITS`, `RESEARCHES`, `WARE_EINTRAEGE`, `WARE_ICONS`, `MAPS`, `BOTS`, `BOT_TAKT_SEKUNDEN`, `BOT_BESCHAFFUNGSKOSTEN`  
  Zusätzlich pure Hilfsfunktionen: `siedlung_kennung`, `karten_signatur`, `neue_siedlungskarte`, `bauen_auf_karte`, `research_multiplier`, `bibliotheken_im_spiel`

- `src/spielkern/game_state.py`  
  Die gesamte Klasse `GameState` unverändert, inklusive `__init__`, `tick`, `save`, `load`, `spielausgang`, `punktestand`, `bots_fortschreiben`, `auftraege_fortschreiben`, `transport_an_ort`, `handel_mit_bot`, `gründen`, `forschungsabschluss`, etc.  
  Importiert nur `src/spielkern/modelle.py` und bestehende Fachmodule (`wirtschaft`, `einheiten`, `botkern`, `kampf`, `spieloekonomie`, …). **Niemals** GUI-Module.

- `src/spielkern/baupreise.py`  
  `baukosten`, `kosten_text` aus `main.py` verschieben.

**Signatur der zentralen Klasse bleibt identisch:**

```python
class GameState:
    def __init__(self): ...
    def tick(self, dt_seconds: float): ...
    def save(self, path: str, admin_freigabe: bool = False): ...
    def load(self, path: str, admin_freigabe: bool = False): ...
```

**Sonderfälle:**  
- Beim Verschieben von `GameState` muss der Import in `main.py` ersetzt werden: `from spielkern.game_state import GameState`.  
- Andere Module, die bisher aus `main` importieren (falls vorhanden), müssen zuerst auf `modelle` umgestellt werden, um Zyklen zu vermeiden.  
- `save`/`load` berühren weiterhin `self.admin_teststand` und `self.messages`; diese Logik nicht ändern, nur verschieben.  
- `menu_sichtbar`, `menu_fuer_ebene` kommen nach `src/spielkern/menue.py`, weil sie von UI und Spielstand gemeinsam genutzt werden, aber keine Tkinter-Abhängigkeit haben.

**Prüfung:**  
Alle Core-Tests (`tests/test_oekonomie_uhr.py`, `tests/test_auftraege.py`, `tests/test_spieloekonomie.py`, `tests/test_oekonomie_einhaengung.py`, `tests/test_startspiel.py`, `tests/test_durchspiel.py`) müssen grün bleiben. Danach `tools/sammellauf.py`.

#### 3.2 Render-Ansichten mit gemeinsamem Helfer

**Ziel:** Die 27 `_render_*`-Methoden verlieren ihr identisches Vorab-Gerüst und werden zu schlanken, lokalen Ansichten.

**Welcher Helfer:**

```python
# src/gui/seitenhelfer.py
def seite_aufbauen(app, titel: str, untertitel: str = None, *, reset_scroll: bool = True) -> tk.Frame:
    """Leert content, setzt Scrollposition, erzeugt Titel und optional Untertitel.
    Rückgabe: der Content-Frame, in dem die Ansicht weiter aufbaut."""
    content = app.content
    for widget in content.winfo_children():
        widget.destroy()
    if reset_scroll:
        try:
            app.content_canvas.yview_moveto(0)
        except Exception:
            pass
    tk.Label(content, text=titel, font=("Blackletter", 20, "bold"),
             fg=app.skin["gold"], bg=app.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 2))
    if untertitel:
        tk.Label(content, text=untertitel, fg="#F3F4F6", bg=app.skin["bg"],
                 wraplength=820, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=(0, 4))
    return content
```

**Parameter:**  
- `app`: die `NebelseetalApp`-Instanz, damit `content`, `skin`, `content_canvas` erreichbar bleiben.  
- `titel`: Überschrift der Seite.  
- `untertitel`: optionaler erklärender Text.  
- `reset_scroll`: ob die Scrollposition auf 0 zurückgesetzt wird; in Dialogen/Unteransichten oft `False`.

**Wirkung:**  
Jede `_render_*`-Methode beginnt künftig z. B. so:

```python
def _render_storage(self):
    content = seite_aufbauen(self, "Lager", "Waren und Einheiten in dieser Siedlung.")
    # ... bestehende Logik, aber content statt self.content verwenden
```

**Sonderfälle:**  
- `_render_view` bleibt Dispatcher und leert den Content selbst; er ruft dann die einzelnen Render-Methoden auf.  
- `_render_maps`, `_render_settlement_map`, `_render_portal` erzeugen zusätzliche Canvas-/Toplevel-Widgets; der Helfer wird nur für den Kopfbereich genutzt und dann `self.content` weiter verwendet.  
- `_render` (Tick-Update) baut keine Seite neu auf und bleibt unverändert.  

**Ersparnis:**  
27 Methoden × ca. 5–8 Zeilen Gerüst ≈ 150–200 Zeilen (geschätzt).

### 4. Was du NICHT anfassen würdest

**Pixel- und Zeichencode in `karten_optik*`, `welt_optik*`, `originalkarten_grafik`**  
Jede Änderung an den Koordinaten, Linien oder Farben kann visuelle Regressionsprüfungen brechen. Die Zeichnung ist kinderarbeit-geprüft und wird über `tests/test_weltkarte.py` sowie fortlaufende Bildschirmfoto-Abnahmen abgesichert.

**Kampf- und Wirtschaftsformeln**  
`kampf.py`, `kampfbericht.py`, `wirtschaft.py`, `punkte.py`, `spieloekonomie.py` sind bereits fachlich separiert und werden von vielen Tests direkt geprüft. Eine Zusammenführung oder „Vereinfachung“ dort würde Zahlen/Regeln ändern.

**`GameState.tick()` inhaltlich**  
Die Methode ist lang und verzweigt, aber sie ist der einzige Ort, an dem Ökonomie-, Bot-, Auftrags- und Forschungslogik in exakt der dokumentierten Reihenfolge laufen. Beim Auslagern **nur verschieben, nicht refaktorieren**.

**Die konkreten Zahlen in `_render_settings` und `_render_battle_simulator`**  
Zeitfaktor-Stufen, Goetterschutzgrenzen, Simulator-Texte sind bewusst als VORSCHLAG oder belegt markiert. Eine Umbenennung oder Verschiebung darf den Zahlenwert nicht verändern.

### 5. Ordnung

**Zielstruktur:**

```
src/
  spielkern/
    modelle.py              # Dataclasses und Konstanten
    game_state.py           # GameState vollständig
    baupreise.py            # baukosten, kosten_text
    menue.py                # menu_sichtbar, menu_fuer_ebene, EBENE_JE_PUNKT, MENU_*
  gui/
    app.py                  # NebelseetalApp-Klasse, Tick-Loop, Basis-UI
    seitenhelfer.py         # seite_aufbauen, ggf. abschnitts_helfer
    menue_helfer.py         # Menü-Buttons bauen
    ui_helfer.py            # _lade_icon, _schild_dialog_inhalt, _spaltenname, _ertrag_kurz
    ansichten/
      uebersicht.py         # _render_overview, _toggle_technik, naechster_schritt
      siedlung.py           # _render_settlement_map, _karten_*
      welt.py               # _render_maps, _welt_*
      lager.py              # _render_storage, _ware_herstellen, _render_barracks, _render_stellmacher, _render_diebesgilde, _render_ausbildung
      forschung.py          # _render_research, _start_research
      diplomatie.py         # _render_diplomacy, _trade, _attack, _handel_*
      nachrichten.py        # _render_messages, _render_neuigkeiten, _render_news? (letzterer entfernen)
      simulator.py          # _render_battle_simulator, _simulate_random_battle
      hilfe.py              # _render_help, _spielerhilfe_*
      profile.py            # _render_profiles, _save_profile
      admin_dialoge.py      # _admin_*, _spielstand_verwaltung, _slot_auswahl
  main.py                   # Einstieg, Ladeansicht, Lock-Datei
```

**Reihenfolge ohne Importbrüche:**

1. **`src/spielkern/modelle.py` anlegen**  
   Alle Dataclasses und Konstanten aus `main.py` dorthin verschieben.  
   `main.py` importiert ab jetzt `from spielkern.modelle import *` (oder gezielt).  
   Andere Module, die bisher `main.Settlement` etc. referenzieren, müssen auf `spielkern.modelle` umgestellt werden.  
   **Danach:** `tests/test_gebaeude_wirkung.py`, `tests/test_auftraege.py`, `tests/test_spieloekonomie.py` und Sammellauf grün.

2. **`src/spielkern/baupreise.py` und `src/spielkern/menue.py` auslagern**  
   Reine Helfer ohne GUI-Abhängigkeit.  
   **Danach:** `tests/test_oberflaeche_original.py` (Menüprüfung) und Ökonomietests grün.

3. **`src/spielkern/game_state.py` anlegen**  
   `GameState` komplett verschieben.  
   `main.py` importiert `GameState` aus dem neuen Ort.  
   **Danach:** komplette Kern-Tests grün, insbesondere `tests/test_oekonomie_uhr.py`, `tests/test_auftraege.py`, `tests/test_startspiel.py`.

4. **`src/gui/app.py` erstellen**  
   Die `NebelseetalApp`-Klasse und Basis-UI (Tor, Profil, Slots, Tick-Rahmen) dorthin verschieben.  
   Die Render-Methoden können vorerst noch als Mixins aus `src/gui/ansichten/*` eingebunden werden.

5. **`src/gui/seitenhelfer.py` einführen**  
   Das Render-Gerüst vereinheitlichen, aber noch keine Ansicht verschieben.  
   **Danach:** `tests/test_oberflaeche_original.py` und `tests/test_gui_fehler.py` grün.

6. **Einfache Ansichten zuerst verschieben**  
   `_render_forum`, `_render_chat`, `_render_referral`, `_render_help`, `_render_profiles`, `_render_messages`, `_render_neuigkeiten`.  
   Jede Verschiebung einzeln mit gezielten Prüfungen absichern.

7. **Komplexe Ansichten verschieben**  
   `_render_overview`, `_render_storage`, `_render_barracks`, `_render_stellmacher`, `_render_diebesgilde`, `_render_research`, `_render_diplomacy`, `_render_battle_simulator`.

8. **Kartenansichten und Zeichnung verschieben**  
   `_render_maps`, `_render_settlement_map`, `_draw_map`, `_zeichne_siedlungskarte` etc. nach `gui/ansichten/welt.py`, `gui/ansichten/siedlung.py`, `gui/welt_zeichnung.py`, `gui/siedlung_zeichnung.py`.  
   **Danach:** `tests/test_weltkarte.py` bis zum Schluss grün.

9. **Admin- und Dialog-Methoden verschieben**  
   `_admin_dialog`, `_spielstand_verwaltung`, `_archiv_wiederherstellung_dialog`, `_slot_auswahl`, `_profil_*` nach `src/gui/admin_dialoge.py`.

10. **Tote Methoden entfernen**  
    `rg "_render_news|_upgrade_building"` prüfen; wenn es keine Aufrufer gibt, löschen bzw. als `@deprecated` markieren.  
    **Danach:** finaler `tools/sammellauf.py` über alle 98 Prüfdateien.

**Wichtig:**  
Alle Importe laufen strikt von `gui` → `spielkern` → Fachmodule; `spielkern` importiert niemals `gui` oder `main`. Das verhindert Zyklen und hält die EXE-fähige Struktur stabil.