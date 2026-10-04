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
    check("keine globalen Wirkungsgebaeude mehr — W4b-5: alle Wirkungen kommen aus den "
          "bebauten Feldern der Siedlungskarten",
          len(st.buildings) == 0, f"{len(st.buildings)} Stueck: {sorted(st.buildings)}")
    check("Forschungen angelegt", len(st.research) == 18, f"{len(st.research)} Stueck")
    check("Waren angelegt", len(st.goods) == 17, f"{len(st.goods)} Stueck")

    def karten():
        for m in main.MAPS:
            st.generate_map(m["id"])
            cfg = next(x for x in main.MAPS if x["id"] == m["id"])
            assert len(st.map_tiles) == cfg["size"] ** 2, f"{m['id']}: falsche Feldzahl"
        return True
    check("alle 5 Karten erzeugbar", bool(ausnahme("Karten erzeugen", karten)))

    # Die Rohstoffe kommen seit W4b-4 aus den BEBauten FELDERN der Siedlungskarten.
    # Ohne Bebauung darf nichts wachsen: kein Gebaeude erzeugt mehr von sich aus Rohstoffe.
    vorher = st.resources["holz"].amount
    st.tick(600)
    check("ohne bebaute Karte waechst kein Rohstoff", st.resources["holz"].amount == vorher,
          f"{vorher:.1f} -> {st.resources['holz'].amount:.1f}")
    check("kein Gebaeude erzeugt von sich aus Rohstoffe",
          all(not getattr(b, "production", {}) for b in st.buildings.values()),
          str({k: b.production for k, b in st.buildings.items() if b.production}))

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
check("Einheiten im Code = 28 Originaleinheiten", len(einheiten) == 28, f"{len(einheiten)} Stueck")
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

# Kampfkraft rollenbewusst: Karren und Belagerungswaffen kaempfen im Original nicht und
# haben darum zu Recht keine Kampfkraft — sie wirken ueber Ladung bzw. Schlagkraft.
import einheiten as _ein
_kaempfer = [k for k in einheiten if _ein.ist_kaempfer(k)]
_ohne_kampf = [k for k in _kaempfer if bs.get_combat_power({k: 1}, {}) == 0]
check(f"alle {len(_kaempfer)} Kaempfer und Kundschafter haben Kampfkraft", not _ohne_kampf,
      ", ".join(_ohne_kampf))
_nichtkaempfer = [k for k in einheiten if not _ein.ist_kaempfer(k)]
check("Nichtkaempfer sind vollzaehlig vorhanden (Karren 6, Belagerung 7)",
      len(_nichtkaempfer) == 13, f"{len(_nichtkaempfer)} Stueck")


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
            app.state.resources["metall"].amount = 5000
            app.state.resources["nahrung"].amount = 5000
            app.state.resources["gold"].amount = 5000
            app.state.resources["mana"].amount = 5000
            app.state.population = 5000.0   # Siedler sind Bevoelkerung, keine Ressource
            app._found_settlement()
            assert app.state.settlements, "keine Siedlung gegruendet"

            # W4b-5: Die Wirkungen kommen aus den bebauten FELDERN. Ein Haus hebt die
            # Siedlergrenze um 5 (Handbuch S. 11) — vorher hing sie an einer globalen Liste.
            siedlung = app.state.settlements[-1]
            grenze_vorher = main.gebaeude_wirkung.bevoelkerungsgrenze(app.state.settlements)
            feld = next(i for i, a in enumerate(siedlung.karte["raster"]) if a != "sumpf")
            app._oeffne_siedlungskarte(siedlung)
            app._karten_feld_waehlen(feld)
            app._karten_bauen("haus")
            grenze_nachher = main.gebaeude_wirkung.bevoelkerungsgrenze(app.state.settlements)
            assert grenze_nachher == grenze_vorher + 5, f"{grenze_vorher} -> {grenze_nachher}"

            # Ohne Bibliothek keine Forschung, ohne Ausbildungsstaette keine Ausbildung.
            app._start_research("landwirtschaft")
            assert any("Bibliothek" in z for z in app.state.log[-3:]), app.state.log[-3:]
            app._train_unit("Krieger")
            assert any("Kriegerakademie" in z for z in app.state.log[-3:]), app.state.log[-3:]
            app._upgrade_building("haus")      # altes globales Gebaeude: wird ehrlich abgewiesen
            assert any("kein globales" in z for z in app.state.log[-3:]), app.state.log[-3:]
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


abschnitt("6. Icons laden wirklich (nicht nur: Dateien sind da)")


def icon_probe():
    root = tk.Tk()
    root.withdraw()
    try:
        app = main.NebelseetalApp(root)
        fehlend = []
        for k, rel in main.UNIT_ICONS.items():
            if app._lade_icon(rel) is None:
                fehlend.append(k)
        check(f"alle {len(main.UNIT_ICONS)} Einheiten-Icons laden als Tk-Bild",
              not fehlend, ", ".join(fehlend))
        probe = main.icon_pfad(list(main.UNIT_ICONS.values())[0])
        check("die freigestellte Fassung hat Vorrang",
              "clean" in probe.replace("\\", "/"), probe)
        check("dieselbe Datei wird nur einmal geladen (Zwischenspeicher)",
              app._lade_icon(list(main.UNIT_ICONS.values())[0]) is
              app._lade_icon(list(main.UNIT_ICONS.values())[0]))
        return True
    finally:
        root.destroy()


check("Icon-Probe laeuft durch", bool(ausnahme("Icons", icon_probe)))


abschnitt("7. Rollbereich — lange Ansichten vollstaendig erreichbar")


def roll_probe():
    root = tk.Tk()
    root.withdraw()
    try:
        app = main.NebelseetalApp(root)
        app._build_main_ui()
        root.update()
        for u in app.state.units.values():
            u.count = 3                      # realistisch lange Listen
        for k in app.state.goods:
            app.state.goods[k] = 7
        app._switch_view("Lager")
        root.update()
        app.content_canvas.update_idletasks()
        bbox = app.content_canvas.bbox("all")
        gepackt = app.content_canvas.cget("scrollregion")
        check("Rollbereich ist gesetzt", gepackt not in ("", None), str(gepackt))
        check("Inhalt ist vollstaendig im Rollbereich",
              (bbox[3] - bbox[1]) >= app.content.winfo_reqheight(),
              f"{bbox[3] - bbox[1]} px Rollbereich gegen {app.content.winfo_reqheight()} px Inhalt")
        app.content_canvas.yview_moveto(1.0)
        root.update()
        check("bis ans Ende rollbar", app.content_canvas.yview()[1] >= 0.99,
              str(tuple(round(v, 2) for v in app.content_canvas.yview())))
        check("Lager baut Waren- und Einheitenbereich auf",
              len(app.content.winfo_children()) >= 4,
              f"{len(app.content.winfo_children())} Bereiche")
        return True
    finally:
        root.destroy()


check("Rollbereich-Probe laeuft durch", bool(ausnahme("Rollbereich", roll_probe)))

sys.exit(bericht())
