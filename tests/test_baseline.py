"""Grundpruefung des Nebelseetal-Remakes: laeuft ohne sichtbares Fenster.

Aufruf:  python tests/test_baseline.py
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, bericht, befund, check, import_src

ROOT, SRC = import_src()
os.chdir(SRC)


# ------------------------------------------------------------------ 1 Aufbau
abschnitt("1. Aufbau und Quelltext")
main = ausnahme("main importieren", lambda: __import__("main"))
bs = ausnahme("bonus_system importieren", lambda: __import__("bonus_system"))
if main is None or bs is None:
    sys.exit(bericht())

check("main.py vorhanden", os.path.exists(os.path.join(SRC, "main.py")))
check("bonus_system.py vorhanden", os.path.exists(os.path.join(SRC, "bonus_system.py")))
check("Originalhandbuch vorhanden",
      os.path.exists(os.path.join(ROOT, "docs", "original",
                                  "Nebelseetal_Spielanleitung_2009.pdf")))
check("Icon-Zuordnungsdatei vorhanden",
      os.path.exists(os.path.join(ROOT, "data", "icon_map.json")))
check("Icon-Index vorhanden", os.path.exists(os.path.join(ROOT, "data", "icons_index.json")))


# ------------------------------------------------------------------ 2 Engine
abschnitt("2. Spielkern")
st = ausnahme("GameState anlegen", lambda: main.GameState())
if st:
    check("Gebaeude angelegt", len(st.buildings) == 10, f"{len(st.buildings)} Stueck")
    check("Forschungen angelegt", len(st.research) == 18, f"{len(st.research)} Stueck")
    check("Waren angelegt", len(st.goods) == 17, f"{len(st.goods)} Stueck")

    def karten():
        for m in main.MAPS:
            st.generate_map(m["id"])
            cfg = next(x for x in main.MAPS if x["id"] == m["id"])
            assert len(st.map_tiles) == cfg["size"] ** 2, f"{m['id']}: falsche Feldzahl"
        return True
    check("alle 5 Karten erzeugbar", bool(ausnahme("Karten erzeugen", karten)))

    st.buildings["holzfäller"].level = 3
    st.buildings["holzfäller"].production = {"holz": 3.6}
    vorher = st.resources["holz"].amount
    st.tick(600)
    check("Produktion laeuft", st.resources["holz"].amount > vorher,
          f"{vorher:.1f} -> {st.resources['holz'].amount:.1f}")

    def speichern():
        p = os.path.join(tempfile.gettempdir(), "nebel_test_save.json")
        st.save(p)
        st2 = main.GameState()
        st2.load(p)
        os.remove(p)
        return len(st2.map_tiles)
    check("Speichern und Laden", bool(ausnahme("Speichern/Laden", speichern)))


# ------------------------------------------------------------------ 3 Daten
abschnitt("3. Einheiten und Icons")
einheiten = main.UNITS
icons = main.UNIT_ICONS
check("Einheiten im Code", len(einheiten) == 36, f"{len(einheiten)} Stueck")
check("jede Einheit hat einen Icon-Eintrag", all(k in icons for k in einheiten))

from collections import Counter
_haeufig = Counter(icons.values())
_doppelt = {p: n for p, n in _haeufig.items() if n > 1}
if _doppelt:
    befund(f"{sum(_doppelt.values())} Einheiten teilen sich {len(_doppelt)} Icon-Dateien",
           "Platzhalter-Zuordnung, wird durch die Originalsymbole ersetzt")
else:
    check("kein Icon doppelt belegt", True)

_fehlend = [k for k, v in icons.items() if not os.path.exists(os.path.join(ROOT, v))]
if _fehlend:
    befund(f"{len(_fehlend)} Icon-Dateien fehlen auf der Platte", ", ".join(_fehlend[:5]))
else:
    check("alle Icon-Dateien vorhanden", True)

_ohne_kampf = [k for k in einheiten if bs.get_combat_power({k: 1}, {}) == 0]
if _ohne_kampf:
    befund(f"{len(_ohne_kampf)} von {len(einheiten)} Einheiten haben Kampfkraft 0",
           "Hauptursache 'kein Kampf moeglich' — wird in W1 behoben")
else:
    check("jede Einheit hat Kampfkraft", True)


if os.path.exists(os.path.join(ROOT, "data", "icons_index.json")):
    abschnitt("4. Icon-Index")
    idx = json.load(open(os.path.join(ROOT, "data", "icons_index.json"), encoding="utf-8"))
    ic = idx.get("icons", {})
    check("Index enthaelt 45 Eintraege", len(ic) == 45, f"{len(ic)} Stueck")
    fehlt = [n for n, e in ic.items()
             if not os.path.exists(os.path.join(ROOT, e["pfad"].replace("/", os.sep)))]
    check("alle Indexdateien vorhanden", not fehlt, ", ".join(fehlt[:4]))
    neu = sum(1 for e in ic.values() if e.get("quelle") == "neu")
    check("neu geschnittene Icons = 28", neu == 28, f"{neu} Stueck")


# ------------------------------------------------------------------ 5 Datengrundlagen
abschnitt("5. Datengrundlagen aus den Originaldaten")
_DATEN = [
    ("data/unit_stats.json", "einheiten", 28),
    ("data/items.json", "waren", 17),
    ("data/research.json", "forschungen", 21),
    ("data/resources.json", "rohstoffe", 9),
    ("data/buildings.json", "gebaeude", 20),
]
for _rel, _key, _soll in _DATEN:
    _p = os.path.join(ROOT, _rel)
    if not os.path.exists(_p):
        befund(f"{_rel} fehlt", "noch nicht erzeugt")
        continue
    _d = json.load(open(_p, encoding="utf-8"))
    _block = _d.get(_key)
    _n = len(_block) if _block is not None else 0
    check(f"{_rel}: {_soll} Eintraege", _n == _soll, f"{_n} gefunden")

# Wallstufen liegen im Gebaeude Verteidigungswall
_bp = os.path.join(ROOT, "data", "buildings.json")
if os.path.exists(_bp):
    _b = json.load(open(_bp, encoding="utf-8"))
    _wall = [e for e in _b.get("gebaeude", []) if e.get("id") == "verteidigungswall"]
    _stufen = _wall[0].get("stufen", []) if _wall else []
    check("Verteidigungswall hat 10 Stufen", len(_stufen) == 10, f"{len(_stufen)} Stufen")
    if len(_stufen) == 10:
        check("Wallstufe 10 ist Bollwerk mit 1000",
              _stufen[9].get("name") == "Bollwerk"
              and _stufen[9].get("schwellenwert_fussttruppen") == 1000)


# ------------------------------------------------------------------ 6 Oberflaeche
abschnitt("6. Oberflaeche (ohne Fenster)")
tk = ausnahme("tkinter laden", lambda: __import__("tkinter"))

if tk is not None:
    def oberflaeche():
        root = tk.Tk()
        root.geometry("1024x720")
        try:
            app = main.NebelseetalApp(root)
            app._build_main_ui()
            root.update()
            fehler = []
            for v in main.MENU_ITEMS + ["Spielerprofile"]:
                try:
                    app._switch_view(v)
                    root.update_idletasks()
                except Exception as e:
                    fehler.append(f"{v}: {e!r}")
            assert not fehler, "; ".join(fehler)
            assert app.lbl_status.winfo_height() > 12, "Statuszeile unsichtbar"
            return True
        finally:
            try:
                root.destroy()
            except Exception:
                pass
    check("alle 17 Ansichten rendern", bool(ausnahme("Ansichten", oberflaeche)))

    def aktionen():
        root = tk.Tk()
        try:
            app = main.NebelseetalApp(root)
            app._build_main_ui()
            root.update()
            app.state.resources["holz"].amount = 5000
            app.state.resources["stein"].amount = 5000
            app.state.resources["eisen"].amount = 5000
            app.state.resources["nahrung"].amount = 5000
            app.state.resources["geld"].amount = 5000
            app.state.resources["wissen"].amount = 5000
            app._upgrade_building("holzfäller")
            app._start_research("landwirtschaft")
            app._train_unit("krieger")
            app._found_settlement()
            app._save()
            root.update_idletasks()
            return True
        finally:
            try:
                root.destroy()
            except Exception:
                pass
            sp = os.path.join(SRC, "savegame.json")
            if os.path.exists(sp):
                os.remove(sp)
    check("Kernaktionen laufen durch", bool(ausnahme("Aktionen", aktionen)))

sys.exit(bericht())
