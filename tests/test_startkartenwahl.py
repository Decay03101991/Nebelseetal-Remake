# -*- coding: ascii -*-
"""Startkartenwahl des Spielers beim ersten Gruenden (A2-Vorstufe, Vorgabe Daniel 02./03.11.2026).

Daniel hat die Kartenwahl am Start in den eingefrorenen Demo-Umfang gelegt ("Kernkreis + Spionage +
Voelker- und Kartenwahl am Start"). Vorher war die Spieler-Startkarte FEST verdrahtet
(`originalkarten.START_ID = original-036`), jetzt waehlt der Spieler aus drei Karten.

Was diese Datei beweist
-----------------------
1. Die Zahlen stehen in `data/startkarte.json` - Anzahl, Kategorien, Standardkarte, Speicherfeld.
2. `startkarte_kandidaten` liefert genau so viele Karten, die Standardkarte ist IMMER dabei, alle
   Kandidaten liegen in der erlaubten Kategorie, und die Auswahl ist je Startsaat reproduzierbar.
3. `startkarte_auswahl_erforderlich` sagt nur beim ersten Start True (keine Siedlung, nichts gewaehlt).
4. Ohne Wahl bleibt es bei der belegten Standardkarte - der stehende Aufruf
   `_erste_siedlung_gruenden()` gruendet weiterhin sofort (16 Pruefdateien haengen daran).
5. Im Dorfzentrum steht die Wahl als Maske mit einem Knopf je Karte; nach der Wahl traegt die neue
   Siedlung GENAU diese Karte.

Aufruf:  python -X utf8 tests/test_startkartenwahl.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

ROOT, SRC = import_src()
import main as M  # noqa: E402
import originalkarten as O  # noqa: E402
import spieloekonomie as S  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()

# ==========================================================================
# 1. Die Zahlen stehen in der Datendatei
# ==========================================================================

abschnitt("1. Anzahl, Kategorien und Standardkarte kommen aus data/startkarte.json")
_pfad = os.path.join(ROOT, "data", "startkarte.json")
check("die Datendatei existiert", os.path.exists(_pfad), _pfad)
with open(_pfad, encoding="utf-8") as _f:
    _cfg = json.load(_f)
check("die Anzahl der Kandidaten ist eine Zahl groesser 1",
      int(_cfg.get("anzahl_kandidaten") or 0) > 1, str(_cfg.get("anzahl_kandidaten")))
check("die erlaubten Kategorien sind eine nichtleere Liste",
      isinstance(_cfg.get("kategorien"), list) and bool(_cfg.get("kategorien")),
      str(_cfg.get("kategorien")))
check("die Standardkarte ist die bisher fest verdrahtete Startkarte",
      _cfg.get("standard_karte") == O.START_ID, "%s / %s" % (_cfg.get("standard_karte"), O.START_ID))
check("das Speicherfeld ist benannt", bool(str(_cfg.get("speicherfeld") or "")),
      str(_cfg.get("speicherfeld")))
check("die Datendatei nennt ihren Grund", "begruendung" in _cfg, str(list(_cfg))[:80])

# ==========================================================================
# 2. Die Kandidaten
# ==========================================================================

abschnitt("2. Kandidaten: richtige Anzahl, Standardkarte dabei, erlaubte Kategorie, reproduzierbar")
_seed = "nebel-probe-20261103"
_kand = S.startkarte_kandidaten(_seed)
check("so viele Kandidaten wie in der Datendatei",
      len(_kand) == int(_cfg.get("anzahl_kandidaten") or 0), str(len(_kand)))
_ids = [k.get("originalkarte_id") for k in _kand]
check("die Standardkarte ist immer dabei", _cfg.get("standard_karte") in _ids, str(_ids))
check("keine Karte doppelt", len(set(_ids)) == len(_ids), str(_ids))
_kat = {e["id"]: e["kategorie"] for e in O.alle()}
check("alle Kandidaten liegen in der erlaubten Kategorie",
      all(_kat.get(i) in _cfg.get("kategorien") for i in _ids),
      str([(i, _kat.get(i)) for i in _ids]))
check("dieselbe Startsaat bietet dieselben Kandidaten",
      [k.get("originalkarte_id") for k in S.startkarte_kandidaten(_seed)] == _ids, str(_ids))
check("eine andere Startsaat bietet andere Karten",
      [k.get("originalkarte_id") for k in S.startkarte_kandidaten("nebel-anders")] != _ids,
      "die Wahl waere sonst nicht vom Start abhaengig")
check("jeder Kandidat ist eine echte Karte mit Feldern",
      all(isinstance(k, dict) and k.get("felder") for k in _kand), str(_ids))

# ==========================================================================
# 3. Wann wird gewaehlt?
# ==========================================================================

abschnitt("3. Die Wahl erscheint nur beim ersten Start")
check("keine Siedlung, nichts gewaehlt -> Wahl", S.startkarte_auswahl_erforderlich(0, 9, "") is True)
check("keine Siedlung, gewaehlt -> keine Wahl",
      S.startkarte_auswahl_erforderlich(0, 9, "original-048") is False)
check("eine Siedlung -> keine Wahl", S.startkarte_auswahl_erforderlich(1, 9, "") is False)
check("Maximum erreicht -> keine Wahl", S.startkarte_auswahl_erforderlich(9, 9, "") is False)

# ==========================================================================
# 4. Rueckfall: ohne Wahl bleibt alles wie vorher
# ==========================================================================

abschnitt("4. Ohne Wahl gilt die belegte Standardkarte")
check("leere Wahl liefert die Standardkarte",
      O.startkarte_gewaehlt("", _seed).get("originalkarte_id") == O.START_ID, "")
check("eine Wahl liefert genau diese Karte",
      O.startkarte_gewaehlt("original-048", _seed).get("originalkarte_id") == "original-048", "")
check("startkarte(spieler) ist unveraendert die Standardkarte",
      O.startkarte(_seed, "spieler").get("originalkarte_id") == O.START_ID, "")
check("die Siedlungsgruendung nimmt die Wahl ueberhaupt zur Kenntnis",
      "spieloekonomie.startkarte_gewaehlt(" in TEXT_MAIN,
      str(TEXT_MAIN.count("spieloekonomie.startkarte_gewaehlt(")))
check("das Speicherfeld steht im Spielstand",
      '"startkarte_gewaehlt"' in TEXT_MAIN, str(TEXT_MAIN.count("startkarte_gewaehlt")))

# ==========================================================================
# 5. Im Fenster: Maske, drei Knoepfe, Gruendung mit der gewaehlten Karte
# ==========================================================================


def _wahlprobe():
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    try:
        app = M.NebelseetalApp(root)
        app._build_main_ui()
        app._switch_view("Dorfzentrum")
        app.content.update_idletasks()

        def _texte():
            gesammelt = []
            for k in app.content.winfo_children():
                for w in [k] + list(k.winfo_children()):
                    try:
                        gesammelt.append(str(w.cget("text")))
                    except Exception:                            # noqa: BLE001
                        continue
            return gesammelt

        vorher = _texte()
        kandidaten = S.startkarte_kandidaten(app.state.kartenvorrat_seed or "nebel")
        ziel = kandidaten[-1].get("originalkarte_id")
        app._startkarte_waehlen(ziel)
        app.content.update_idletasks()
        nachher = _texte()
        return {"maske": any("Waehle deine Startkarte" in t for t in vorher),
                "knoepfe": sum(1 for t in vorher if t == "Diese Karte nehmen"),
                "gewaehlt": getattr(app.state, "startkarte_gewaehlt", ""),
                "ziel": ziel,
                "siedlungen": len(app.state.settlements),
                "karte": (app.state.settlements[0].karte or {}).get("originalkarte_id")
                if app.state.settlements else "",
                "maske_danach": any("Waehle deine Startkarte" in t for t in nachher)}
    finally:
        root.destroy()


_w = _wahlprobe()
check("die Startmaske erscheint im Dorfzentrum", _w["maske"] is True, str(_w))
check("je Kandidat ein Knopf", _w["knoepfe"] == len(_kand), str(_w["knoepfe"]))
check("die Wahl wird gemerkt", _w["gewaehlt"] == _w["ziel"], "%s / %s" % (_w["gewaehlt"], _w["ziel"]))
check("die Siedlung entsteht", _w["siedlungen"] == 1, str(_w["siedlungen"]))
check("die Siedlung traegt die GEWAEHLTE Karte", _w["karte"] == _w["ziel"],
      "%s / %s" % (_w["karte"], _w["ziel"]))
check("danach ist die Maske weg", _w["maske_danach"] is False, str(_w["maske_danach"]))

bericht()
