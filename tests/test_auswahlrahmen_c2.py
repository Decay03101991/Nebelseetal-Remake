# -*- coding: ascii -*-
"""Auswahlrahmen der C2-Lieferung auf der Siedlungskarte - Register 130 (02.11.2026).

BEFUND (Uebergabe 02.11.2026, Abschnitt 3): `kachelrahmen_auswahl.png` steht seit der C2-Lieferung
in `data/gebaeude_motive.json` und wird auch geladen - GEZEICHNET hat die Karte aber weiter den
gezeichneten goldenen Rahmen aus `karten_optik_fein.auswahl_plan_fein` (astra "Siedlung 3"), und
zwar darueber. Der gelieferte Rahmen war damit toter Vorrat. Seit diesem Schritt liegt der
gelieferte Rahmen voll deckend auf dem gewaehlten Feld; die gezeichnete Fassung ist nur noch
Rueckfall, wenn das Bild fehlt oder nicht ladbar ist.

Was diese Datei beweist
-----------------------
1. Das Bild ist da und passt: Datei 64 x 64 px mit Alphakanal, Pfad in `main.KACHELRAHMEN`.
2. Volle Deckkraft als MESSWERT, nicht als Wortlaut: der Auswahlrahmen landet mit Deckkraft 100 im
   Bildcache, der Ruherahmen mit `main.RAHMEN_DECKRAFT` (35) - gemessen an den Cache-Schluesseln.
3. In einer ECHTEN Tk-Zeichenflaeche liegt auf dem gewaehlten Feld GENAU EIN Auswahlobjekt, und es
   ist ein Bild - kein gezeichnetes Rechteck (nie beides).
4. Das Bild sitzt auf der linken oberen Ecke des gewaehlten Feldes.
5. Es liegt ueber Ruherahmen, Wegen, Gebaeudemotiven und Dorfwall (Durchgang 4 zeichnet zuletzt).
6. Rueckfall: liefert `_lade_kachelrahmen("auswahl")` None, erscheint die gezeichnete Fassung
   (zwei Rechtecke + vier Eckwinkel = 6 Objekte) mit Gold und dunkler Unterkontur.
7. Auch OHNE Pillow bleibt der Rahmen sichtbar (Tk-Rueckfall per `subsample`, Faktor 1 bei 64 px).

Aufruf:  python -X utf8 tests/test_auswahlrahmen_c2.py
"""
from __future__ import annotations

import inspect
import os
import struct
import sys
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, bericht, check, import_src

ROOT, SRC = import_src()
import main               # noqa: E402
import karten_optik_fein  # noqa: E402


def png_kopf(pfad):
    """(breite, hoehe, farbtyp) aus dem PNG-Kopf - ohne Fremdbibliothek."""
    with open(pfad, "rb") as datei:
        kopf = datei.read(33)
    if kopf[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    breite, hoehe = struct.unpack(">II", kopf[16:24])
    return breite, hoehe, kopf[25]


# ==========================================================================
abschnitt("1. Der gelieferte Auswahlrahmen ist eingetragen und vollstaendig")
# ==========================================================================

_relativ = str((main.KACHELRAHMEN or {}).get("auswahl") or "")
check("1 main.KACHELRAHMEN kennt einen Auswahlrahmen", bool(_relativ), _relativ or "(leer)")
_pfad = os.path.join(ROOT, _relativ.replace("/", os.sep))
check("1 die Datei liegt im Projekt (nicht in einem gitignorten Ordner)", os.path.exists(_pfad), _pfad)
if os.path.exists(_pfad):
    _kopf = png_kopf(_pfad)
    check("1 der Rahmen ist 64 x 64 px mit Alphakanal (Farbtyp 6)",
          _kopf is not None and _kopf[0] == 64 and _kopf[1] == 64 and _kopf[2] == 6, str(_kopf))


# ==========================================================================
abschnitt("2. Auswahlrahmen voll deckend, Ruherahmen gedaempft (gemessen)")
# ==========================================================================

_quelle = inspect.getsource(main.NebelseetalApp._zeichne_siedlungskarte)
_i_ruhe = _quelle.find('_lade_kachelrahmen("ruhe"')
_i_wall = _quelle.find("dorfwall.rahmen_plan")
_i_ausw = _quelle.find('_lade_kachelrahmen("auswahl"')
check("2 die Karte laedt BEIDE Rahmenarten", _i_ruhe >= 0 and _i_ausw >= 0,
      f"ruhe={_i_ruhe}, auswahl={_i_ausw}")
check("2 der Auswahlrahmen kommt NACH dem Dorfwall (Durchgang 4, liegt zuletzt auf)",
      _i_ruhe >= 0 and _i_ausw > _i_wall >= 0, f"ruhe={_i_ruhe}, wall={_i_wall}, auswahl={_i_ausw}")
check("2 der gezeichnete Rahmen bleibt als Rueckfall im Code",
      "auswahl_plan_fein(" in _quelle, "")


# ==========================================================================
abschnitt("3. Echte Zeichenflaeche: genau EIN Auswahlrahmen, und zwar das Bild")
# ==========================================================================

try:
    _root = tk.Tk()
except tk.TclError as _fehler:
    print(f"Kein Fenster moeglich (kein Desktop): {_fehler}")
    print("Diese Pruefung braucht einen angemeldeten Windows-Desktop.")
    sys.exit(bericht())

_root.withdraw()
_app = ausnahme("App aufbauen", lambda: main.NebelseetalApp(_root))
if _app is None:
    _root.destroy()
    sys.exit(bericht())
ausnahme("Hauptoberflaeche aufbauen", _app._build_main_ui)
ausnahme("Siedlung gruenden", _app._erste_siedlung_gruenden)

_siedlung = _app.state.settlements[-1] if _app.state.settlements else None
check("3 eine Siedlung mit Karte ist vorhanden",
      _siedlung is not None and bool(getattr(_siedlung, "karte", None)), "")

if _siedlung is not None and getattr(_siedlung, "karte", None):
    ausnahme("Siedlungskarte oeffnen", lambda: _app._oeffne_siedlungskarte(_siedlung))

    # ---- Deckkraft aus dem Bildcache MESSEN (dieselbe Quelle wie das Zeichnen) ---------------
    _app._rahmen_cache = {}                                        # frischer Cache je Rahmenart
    _bild_ruhe = ausnahme("Ruherahmen laden", lambda: _app._lade_kachelrahmen("ruhe", 64))
    _bild_auswahl = ausnahme("Auswahlrahmen laden", lambda: _app._lade_kachelrahmen("auswahl", 64))
    _schluessel = [k for k in getattr(_app, "_rahmen_cache", {})]  # (Pfad, px, Deckkraft)
    _deckkraft = {}
    for _pfad_key, _px, _dk in _schluessel:
        _deckkraft[os.path.basename(_pfad_key)] = _dk
    check("3 der Auswahlrahmen wird mit der Deckkraft aus der Datendatei geladen (Vorgabe 100)",
          _deckkraft.get(os.path.basename(_pfad)) == main.AUSWAHL_DECKRAFT
          and main.AUSWAHL_DECKRAFT == 100, f"{_deckkraft} / AUSWAHL_DECKRAFT={main.AUSWAHL_DECKRAFT}")
    check("3 der Ruherahmen behaelt die gedaempfte Deckkraft aus der Datendatei",
          None not in (_bild_ruhe, _bild_auswahl)
          and main.RAHMEN_DECKRAFT in _deckkraft.values(), str(_deckkraft))

    _feld = 12 if len(_siedlung.karte["raster"]) > 12 else 0
    ausnahme("Feld waehlen", lambda: _app._karten_feld_waehlen(_feld))
    _canvas = _app.karten_canvas
    _auswahl = _canvas.find_withtag("auswahl")
    check("3 genau EIN Auswahlobjekt auf dem gewaehlten Feld", len(_auswahl) == 1,
          f"{len(_auswahl)} Objekte: {[_canvas.type(o) for o in _auswahl]}")
    check("3 der Auswahlrahmen ist das GELIEFERTE BILD, kein gezeichnetes Rechteck",
          len(_auswahl) == 1 and _canvas.type(_auswahl[0]) == "image",
          str([_canvas.type(o) for o in _auswahl]))

    if len(_auswahl) == 1:
        _rand = int(karten_optik_fein.KOORDINATEN_BREITE)
        _zelle = 64
        _spalten = int(_siedlung.karte["spalten"])
        _x0 = _rand + (_feld % _spalten) * _zelle
        _y0 = _rand + (_feld // _spalten) * _zelle
        check("3 das Bild sitzt auf der linken oberen Ecke des gewaehlten Feldes",
              [int(v) for v in _canvas.coords(_auswahl[0])[:2]] == [_x0, _y0],
              f"{_canvas.coords(_auswahl[0])} statt [{_x0}, {_y0}]")

        _alle = _canvas.find_all()
        _stelle = _alle.index(_auswahl[0])

        def _letzte(marke: str) -> int:
            """Stapelindex des obersten Objekts dieser Marke (-1, wenn keine da ist)."""
            _ids = _canvas.find_withtag(marke)
            return max((_alle.index(i) for i in _ids), default=-1)

        _darunter = max(_letzte("kachelrahmen"), _letzte("weg"), _letzte("motiv"), _letzte("dorfwall"))
        check("3 das Auswahlbild liegt UEBER Ruherahmen, Wegen, Motiven und Dorfwall",
              _stelle > _darunter, f"Auswahl bei {_stelle}, oberstes anderes bei {_darunter}")
        check("3 das Auswahlbild traegt die Feldmarke (Feld bleibt anklickbar)",
              bool(_canvas.find_withtag(f"feld:{_feld}")), "")

    # ---- Rueckfall: kein Bild -> gezeichnete Fassung, und NICHT beides ---------------------
    _echt = _app._lade_kachelrahmen
    _app._lade_kachelrahmen = lambda art="ruhe", px=64: None   # Bild absichtlich weg
    ausnahme("Feld ohne Bild waehlen", lambda: _app._karten_feld_waehlen(_feld))
    _canvas2 = _app.karten_canvas
    _auswahl2 = _canvas2.find_withtag("auswahl")
    check("3 ohne Bild erscheint die gezeichnete Fassung (6 Objekte)",
          len(_auswahl2) == 6, f"{len(_auswahl2)} Objekte: {[_canvas2.type(o) for o in _auswahl2]}")
    check("3 die Rueckfall-Fassung traegt Gold und dunkle Unterkontur",
          any(_canvas2.itemcget(o, "outline") == karten_optik_fein.AUSWAHL_GOLD
              for o in _auswahl2 if _canvas2.type(o) == "rectangle")
          and any(_canvas2.itemcget(o, "outline") == karten_optik_fein.AUSWAHL_UNTER_FARBE
                  for o in _auswahl2 if _canvas2.type(o) == "rectangle"), "")
    _app._lade_kachelrahmen = _echt

    # ---- Ohne Pillow: Tk-Rueckfall haelt den Rahmen sichtbar ------------------------------
    _app._rahmen_cache = {}
    _alt_pil = sys.modules.get("PIL", "fehlt")
    sys.modules["PIL"] = None                                  # `from PIL import ...` schlaegt fehl
    try:
        _ohne_pillow = ausnahme("Auswahlrahmen ohne Pillow laden",
                                lambda: _app._lade_kachelrahmen("auswahl", 64))
    finally:
        if _alt_pil == "fehlt":
            sys.modules.pop("PIL", None)
        else:
            sys.modules["PIL"] = _alt_pil
    check("3 auch ohne Pillow kommt der Rahmen (Tk-Rueckfall statt None)",
          _ohne_pillow is not None, str(_ohne_pillow))

_root.destroy()
sys.exit(bericht())
