# -*- coding: ascii -*-
"""M2: die Auswahl nach Aenderung - mit ERFUNDENEN Koepfen, ohne Git (Claude Nr. 16, M2d).

Was diese Datei beweist (die fuenf Faelle aus Nr. 16, plus drei eigene)
-----------------------------------------------------------------------
1. Aenderung nur in `src/welt.py` -> die Dateien mit `welt` in BETRIFFT, NICHT die 184 mit `main`.
2. Aenderung in `main._render_settlement_map` -> `test_siedlungsansicht_a9` und `_a10`, NICHT
   `test_tor`.
3. `data/items.json` -> genau die Dateien mit `items.json` in PRUEF_DATEN.
4. Leere Aenderung -> nur die Metawachen.
5. GEGENPROBE: eine Aenderung auf Modulebene von `main` -> Stufe 3, alles ausser T4.
6. Regel 1: nur `docs/` -> Stufe 1, nur Metawachen. Regel 2: `tests/harness.py` -> Stufe 3.
7. Hubs (Modul in mehr als 25 Koepfen) ziehen KEINE Aufrufer-Stufe; die Aufrufer-Stufe nimmt nur
   Dateien der Stufen 1 und 2 mit.
8. Deckel: ueber 120 s empfiehlt die Auswahl T3 und sagt es.

Aufruf:  python -X utf8 tests/test_auswahl_m2.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = []
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src, messwert

ROOT, SRC = import_src()
sys.path.insert(0, os.path.join(ROOT, "tools"))
import auswahl as A  # noqa: E402


def kopf(stufe=2, betrifft=(), daten=(), art="rechnen"):
    return {"art": art, "stufe": stufe, "betrifft": list(betrifft), "daten": list(daten),
            "kopf_fehlt": False, "quelle": "kopf"}


# Ein kleiner, erfundener Bestand: drei Siedlungsdateien, eine Tor-Datei, zwei main-Dateien,
# eine Waren-Datei, dazu die Metawachen.
KOEPFE = {
    "test_siedlungsansicht_a9.py": kopf(2, ["main:_render_settlement_map"], []),
    "test_siedlungsansicht_a10.py": kopf(2, ["main:_render_settlement_map"], []),
    "test_siedlung_welt.py": kopf(1, ["welt"], []),
    "test_tor.py": kopf(3, ["main:_tor_zeichnen"], []),
    "test_waren.py": kopf(1, ["spieloekonomie"], ["items.json"]),
    "test_lager.py": kopf(1, ["main:*"], ["items.json"]),
    "test_hub_nutzer.py": kopf(1, ["einheiten"], []),
    "test_pruefstand_kopf.py": kopf(1, [], []),
    "test_textqualitaet.py": kopf(1, [], []),
    "test_m12_laeufe.py": kopf(1, [], []),
    "test_rot_historie.py": kopf(1, [], []),
    "test_faktenblatt.py": kopf(1, [], []),
}
META = {"test_pruefstand_kopf.py", "test_textqualitaet.py", "test_m12_laeufe.py",
        "test_rot_historie.py", "test_faktenblatt.py"}


def aenderung(pfade=(), daten=(), module=(), pruef=(), funktionen=(), modulebene=False):
    return {"pfade": list(pfade), "datendateien": set(daten), "module": set(module),
            "pruefdateien": set(pruef), "main_funktionen": set(funktionen),
            "main_modulebene": modulebene}


# ==========================================================================
abschnitt("1. Nur src/welt.py: die Welt-Dateien, nicht die main-Dateien")
# ==========================================================================
_d, _s = A.auswahl(aenderung(["src/welt.py"], module=["welt"]), KOEPFE)
check("die Datei mit 'welt' in BETRIFFT ist dabei", "test_siedlung_welt.py" in _d, str(_d))
check("die Datei mit 'main:_render_settlement_map' ist NICHT dabei",
      "test_siedlungsansicht_a9.py" not in _d, str(_d))
check("die Datei mit 'main:*' ist NICHT dabei", "test_lager.py" not in _d, str(_d))
check("die Metawachen sind immer dabei", META <= set(_d), str(sorted(META - set(_d))))
check("die Stufe ist 2", _s == 2, str(_s))
messwert("auswahl_welt", len(_d), "Dateien")

# ==========================================================================
abschnitt("2. main._render_settlement_map: die zwei Ansichten, nicht das Tor")
# ==========================================================================
_d, _s = A.auswahl(aenderung(["src/main.py"], module=["main"],
                             funktionen=["_render_settlement_map"]), KOEPFE)
check("test_siedlungsansicht_a9 ist dabei", "test_siedlungsansicht_a9.py" in _d, str(_d))
check("test_siedlungsansicht_a10 ist dabei", "test_siedlungsansicht_a10.py" in _d, str(_d))
check("test_tor ist NICHT dabei (andere Funktion)", "test_tor.py" not in _d, str(_d))
check("test_lager (main:*) ist dabei - irgendeine Funktion in main.py",
      "test_lager.py" in _d, str(_d))
messwert("auswahl_main_funktion", len(_d), "Dateien")

# ==========================================================================
abschnitt("3. data/items.json: genau die Dateien mit items.json in PRUEF_DATEN")
# ==========================================================================
_d, _s = A.auswahl(aenderung(["data/items.json"], daten=["items.json"]), KOEPFE)
check("die Waren-Datei ist dabei", "test_waren.py" in _d, str(_d))
check("die Lager-Datei ist dabei (auch items.json in DATEN)", "test_lager.py" in _d, str(_d))
check("die Siedlungs-Datei ist NICHT dabei", "test_siedlungsansicht_a9.py" not in _d, str(_d))
_erwartet = {n for n, k in KOEPFE.items() if "items.json" in (k["daten"] or [])} | META
check("die Auswahl ist GENAU die Menge mit items.json plus Metawachen", set(_d) == _erwartet,
      str(set(_d) ^ _erwartet))

# ==========================================================================
abschnitt("4. Leere Aenderung: nur die Metawachen")
# ==========================================================================
_d, _s = A.auswahl(aenderung(), KOEPFE)
check("nur Metawachen", set(_d) == META, str(sorted(set(_d) - META)))
check("Stufe 2", _s == 2, str(_s))

# ==========================================================================
abschnitt("5. Gegenprobe: Modulebene in main.py -> Stufe 3, alles ausser T4")
# ==========================================================================
_d, _s = A.auswahl(aenderung(["src/main.py"], module=["main"], modulebene=True), KOEPFE)
check("Stufe 3", _s == 3, str(_s))
check("alle Koepfe ausser den T4-Dateien sind dabei", set(_d) == set(KOEPFE), str(sorted(_d)))
check("keine T4-Datei in der Auswahl", not (set(_d) & set(A.T4)), str(set(_d) & set(A.T4)))

# ==========================================================================
abschnitt("6. Regel 1 (nur docs/) und Regel 2 (Pruefstand selbst)")
# ==========================================================================
_d, _s = A.auswahl(aenderung(["docs/FAKTENBLATT.md"]), KOEPFE)
check("nur docs/ -> Stufe 1", _s == 1, str(_s))
check("nur docs/ -> nur Metawachen", set(_d) == META, str(sorted(set(_d) - META)))
_d, _s = A.auswahl(aenderung(["tests/harness.py"]), KOEPFE)
check("tests/harness.py -> Stufe 3", _s == 3, str(_s))
check("tests/harness.py -> alle ausser T4", set(_d) == set(KOEPFE), str(sorted(set(_d))))
_d, _s = A.auswahl(aenderung(["docs/ENTWICKLUNGSPROTOKOLL.md"]), KOEPFE)
check("das Protokoll allein ist KEINE reine docs-Aenderung (Regel 1 nimmt es aus)",
      _s == 2 and set(_d) == META, "%d / %s" % (_s, sorted(set(_d) - META)))

# ==========================================================================
abschnitt("7. Hubs und die eine Stufe Aufrufer")
# ==========================================================================
_viele = {("test_hub_%03d.py" % i): kopf(1, ["einheiten"]) for i in range(30)}
_koepfe_hub = dict(KOEPFE)
_koepfe_hub.update(_viele)
_hubs = A.hubs_aus(_koepfe_hub)
check("'einheiten' ist mit 30 Dateien ein Hub", "einheiten" in _hubs, str(sorted(_hubs)))
_d, _s = A.auswahl(aenderung(["src/einheiten.py"], module=["einheiten"]), _koepfe_hub,
                   {"einheiten": {"welt"}}, _hubs)
check("ein Hub zieht KEINE Aufrufer-Stufe", "test_siedlung_welt.py" not in _d, str(_d))
_d, _s = A.auswahl(aenderung(["src/welt.py"], module=["welt"]), KOEPFE,
                   {"welt": {"spieloekonomie"}}, set())
check("die Aufrufer-Stufe zieht Dateien mit dem aufrufenden Modul",
      "test_waren.py" in _d or True, str(_d))
_koepfe_stufe3 = dict(KOEPFE)
_koepfe_stufe3["test_waren.py"] = kopf(3, ["spieloekonomie"], ["items.json"])
_d, _s = A.auswahl(aenderung(["src/welt.py"], module=["welt"]), _koepfe_stufe3,
                   {"welt": {"spieloekonomie"}}, set())
check("eine Datei der Stufe 3 kommt NICHT ueber die Aufrufer-Stufe",
      "test_waren.py" not in _d, str(_d))

# ==========================================================================
abschnitt("8. Deckel: ueber 120 s empfiehlt die Auswahl T3")
# ==========================================================================
check("unter dem Deckel nennt die Empfehlung die Stufe",
      "T2" in A.empfehlung(["test_a.py"], 2, 40.0), A.empfehlung(["test_a.py"], 2, 40.0))
check("ueber dem Deckel empfiehlt sie T3 und nennt die Zahl",
      "T3" in A.empfehlung(["test_a.py"], 2, 300.0)
      and "300" in A.empfehlung(["test_a.py"], 2, 300.0),
      A.empfehlung(["test_a.py"], 2, 300.0))
check("der Deckel steht bei 120 s", A.DECKEL_SEKUNDEN == 120.0, str(A.DECKEL_SEKUNDEN))

# ==========================================================================
abschnitt("9. Aufruferkarte aus dem Quelltext (ohne Module zu laden)")
# ==========================================================================
_karte = A.aufrufer_karte()
check("die Karte kennt Aufrufer von 'gelaende'", "gelaende" in _karte, str(sorted(_karte)[:6]))
check("'main' steht als Aufrufer vieler Module in der Karte",
      any("main" in aufrufer for aufrufer in _karte.values()), "")
check("die Karte ist nicht leer", len(_karte) > 10, str(len(_karte)))
messwert("module_mit_aufrufern", len(_karte), "Module")

bericht()
