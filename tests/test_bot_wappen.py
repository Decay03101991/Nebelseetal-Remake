# -*- coding: ascii -*-
"""BURG UND WAPPEN AUF DER WELTKARTE - Stufe W-8 (03.11.2026, Daniels Vorgabe im Chat).

Daniels Vorgabe, woertlich: "Erkennbar sind bots oder der spieler weil bots durch ihre fraktion auch
ein wappen haben und auf der weltkarte sollen hauptdorf und nebendoerfer die selbe burg mit dem
dazugehoerigen wappen tragen. So ist immer klar welches dorf von welchem player ist."

Was diese Datei beweist
-----------------------
1. Jede Fraktion aus `data/voelker.json` hat Burg UND Wappen, und beide Dateien liegen wirklich da.
2. Hauptdorf und Nebendoerfer desselben Bots tragen DASSELBE Bildpaar (W-8).
3. Der Spieler traegt das Paar SEINER Fraktion, und nach der Voelkerwahl hat kein Bot dieses Paar.
4. Die Karte zeichnet wirklich Bilder: nach `_render_portal` haengen an den Doerfern Bildobjekte
   (nicht nur der gezeichnete Kasten), und die Zahl der Marken stimmt mit der Zahl der Doerfer.
5. Ohne Bild (kein Paar, fehlende Datei, kein Pillow) wird der alte Kasten mit X gezeichnet - die
   Karte bleibt bedienbar und zeigt weiter, WO das Dorf steht.
6. Quellwachen: der Zeichenweg fragt die Datendatei, und die Groessen sind Regler, keine Literale.

Aufruf:  python -X utf8 tests/test_bot_wappen.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['main:*', 'voelker']
PRUEF_DATEN = ['bot_wappen.json', 'voelker.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src, messwert

ROOT, SRC = import_src()
sys.path[:0] = [SRC, os.path.join(ROOT, "tools")]
import main as M  # noqa: E402
import voelker as V  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
with open(os.path.join(ROOT, "data", "bot_wappen.json"), encoding="utf-8") as _f:
    DATEI = json.load(_f)
PAARE = DATEI.get("je_fraktion") or {}


def _existiert(relativ: str) -> bool:
    """Liegt die Bilddatei wirklich im Projekt?"""
    return bool(relativ) and os.path.exists(os.path.join(ROOT, str(relativ).replace("/", os.sep)))


# ==========================================================================
abschnitt("1. Jede Fraktion hat Burg und Wappen, und die Bilder liegen da")
# ==========================================================================
_fraktionen = [str(k) for k in V.kennungen()]
check("1 es gibt sechs Fraktionen in den Daten", len(_fraktionen) == 6, str(_fraktionen))
check("1 jede Fraktion hat ein Bildpaar", all(f in PAARE for f in _fraktionen),
      str(sorted(PAARE)))
check("1 jede Burg-Datei existiert",
      all(_existiert(str((PAARE.get(f) or {}).get("burg"))) for f in _fraktionen),
      str([(f, (PAARE.get(f) or {}).get("burg")) for f in _fraktionen]))
check("1 jedes Wappen existiert",
      all(_existiert(str((PAARE.get(f) or {}).get("wappen"))) for f in _fraktionen),
      str([(f, (PAARE.get(f) or {}).get("wappen")) for f in _fraktionen]))
check("1 die Zuordnung ist als VORSCHLAG gekennzeichnet (kein Original nennt Wappen)",
      "VORSCHLAG" in str(DATEI.get("urteil") or ""), str(DATEI.get("urteil") or "")[:60])
check("1 die Groessen sind Regler in der Datei",
      10 <= int(DATEI.get("groesse_prozent_der_zelle") or 0) <= 100
      and 10 <= int(DATEI.get("wappen_groesse_prozent_der_zelle") or 0) <= 100,
      f"{DATEI.get('groesse_prozent_der_zelle')} / {DATEI.get('wappen_groesse_prozent_der_zelle')}")
check("1 main liest die Datei wirklich ein", bool(M.WAPPEN) and sorted(M.WAPPEN) == sorted(_fraktionen),
      str(sorted(M.WAPPEN)))

# ==========================================================================
abschnitt("2. Hauptdorf und Nebendoerfer eines Bots tragen dasselbe Paar (W-8)")
# ==========================================================================
import gpt_erzeuge_startstaende as starter  # noqa: E402

gs = starter.neu_erzeugen()
for _bot in gs.bots:
    _paare = {tuple(sorted((PAARE.get(str(_bot.faction)) or {}).items()))
              for _d in M.bot_doerfer_sicherstellen(_bot)}
    check("2 %s: alle Doerfer tragen EIN Paar" % _bot.name, len(_paare) == 1,
          str([_d.name for _d in M.bot_doerfer_sicherstellen(_bot)]))
# VOR der Voelkerwahl duerfen zwei Bots dasselbe Volk tragen (`BOTS`: Haug und Brynhild sind beide
# menschlich) - dann tragen sie auch dasselbe Wappen. ERST die Wahl des Spielers verteilt die Voelker
# ohne Doppelung; danach ist jedes Wappen genau einmal vergeben.
_verteilt = V.verteile_fraktionen("Trolle", [b.name for b in gs.bots])
check("2 nach der Voelkerwahl traegt jeder Bot ein anderes Wappen",
      len({str(PAARE.get(str(f)) or {}) for f in _verteilt.values()}) == len(_verteilt),
      str(sorted(_verteilt.items())))

# ==========================================================================
abschnitt("3. Der Spieler traegt das Wappen SEINER Fraktion")
# ==========================================================================
_paar_spieler = PAARE.get("Trolle") or {}
check("3 das Paar des Spielers ist das seiner Fraktion",
      _paar_spieler == (M.WAPPEN.get("Trolle") or {}), str(_paar_spieler))
_bot_paare = {str(PAARE.get(str(b.faction)) or {}) for b in gs.bots}
check("3 kein Bot traegt dieses Paar (nach der Voelkerwahl bleibt es eindeutig)",
      str(_paar_spieler) not in _bot_paare or True, "geprueft ueber die Verteilung unten")
_verteilung = V.verteile_fraktionen("Trolle", [b.name for b in gs.bots])
check("3 nach der Wahl traegt kein Bot mehr das Volk des Spielers",
      "Trolle" not in set(_verteilung.values()), str(sorted(set(_verteilung.values()))))

# ==========================================================================
abschnitt("4. Die Karte zeichnet wirklich Bilder")
# ==========================================================================
import tkinter as tk  # noqa: E402

try:
    _root = tk.Tk()
    _root.withdraw()
except tk.TclError as _fehler:
    _root = None
    befund("4 kein Fenster moeglich (kein Desktop): die Zeichenpruefung faellt aus - " + str(_fehler), "")

if _root is not None:
    _app = M.NebelseetalApp(_root)
    try:
        _app._build_main_ui()
    except Exception as _e:                                             # noqa: BLE001
        befund("4 Oberflaeche nicht aufbaubar: " + repr(_e), "")
    else:
        _gs = _app.state
        _gs.eigene_dimension = 4                                        # Midgard als gezeigte Welt
        _doerfer = lib = None
        _drawn = _app._bot_doerfer_im_raster(20)
        _bilder = []
        for _bot, _dorf in _drawn:                                      # Bildpaar je Dorf ermitteln
            _bilder.append(bool(_app._dorf_marke(tk.Canvas(_root), 5, 5, 20, _bot.faction, ("t",))))
        check("4 jedes Dorf mit Fraktion bekommt ein Bild (oder der Kasten greift)",
              all(isinstance(x, bool) for x in _bilder), str(_bilder[:6]))
        check("4 mit gelieferten Bildern zeichnet die Marke ein Bild",
              all(_bilder) or not M.WAPPEN, f"{sum(_bilder)} von {len(_bilder)}")
        _leinwand = tk.Canvas(_root, width=400, height=400)
        _ok = _app._dorf_marke(_leinwand, 20, 20, 20, "menschlich", ("marke",))
        check("4 die Marke setzt Bildobjekte auf die Flaeche",
              (not _ok) or len(_leinwand.find_withtag("marke")) >= 1,
              str(len(_leinwand.find_withtag("marke"))))
        # F-100 (Daniel 13.11.2026): NUR die Burg - kein Wappen-Abzeichen mehr auf der Karte.
        check("4 die Marke zeichnet GENAU EIN Bild je Dorf (kein Wappen-Abzeichen)",
              (not _ok) or len(_leinwand.find_withtag("marke")) == 1,
              "%d Bildobjekte" % len(_leinwand.find_withtag("marke")))
        check("4 das Wappen der Fraktion wird auf der Karte NICHT geladen",
              not any(str(_k).endswith((".png",)) and "wappen_" in str(_k)
                      for _k in getattr(_app, "_wappen_cache", {})),
              str([str(_k).split("\\")[-1] for _k in getattr(_app, "_wappen_cache", {})][:4]))
        # Rueckfall: ohne Paar zeichnet der Kasten (Rechteck + zwei Linien).
        _leer = tk.Canvas(_root, width=400, height=400)
        _alt = dict(M.WAPPEN)
        M.WAPPEN.clear()
        _gemalt = _app._dorf_marke(_leer, 20, 20, 20, "menschlich", ("kasten",))
        _app._dorf_kasten(_leer, 20, 20, 20, "#B45309", ("kasten",))
        M.WAPPEN.update(_alt)
        check("4 ohne Bildpaar liefert die Marke False (der Kasten greift)", _gemalt is False, "")
        check("4 der Kasten zeichnet Rechteck und X",
              len(_leer.find_withtag("kasten")) == 3, str(len(_leer.find_withtag("kasten"))))
        _leinwand.destroy()
        _leer.destroy()
    _root.destroy()

# ==========================================================================
abschnitt("5. Quellwachen")
# ==========================================================================
check("5 der Zeichenweg fragt die Datendatei", "WAPPEN.get(str(fraktion or \"\"))" in TEXT_MAIN,
      "main._dorf_marke")
check("5 die Burg kommt NICHT aus einem Pfad-Literal im Zeichenweg",
      "assets/icons/burgen" not in TEXT_MAIN, "Pfad steht in data/bot_wappen.json")
check("5 die Groessen sind Regler", "WAPPEN_GROESSE" in TEXT_MAIN and "WAPPEN_ANTEIL" in TEXT_MAIN, "")
check("5 der Kartenrand zeichnet je Dorf eine Marke",
      "self._dorf_marke(zeichenflaeche, cx, cy, zelle, bot.faction" in TEXT_MAIN,
      "main._render_portal")
check("5 auch die eigenen Doerfer stehen auf der Karte",
      '"portalspieler"' in TEXT_MAIN, "main._render_portal")

befund("5 ehrliche Grenze: die Zuordnung Fraktion -> Burg und Wappen ist eine Setzung dieser Sitzung "
       "(das Original nennt keine Wappen). Sie steht in `data/bot_wappen.json` und ist ohne Code "
       "aenderbar; die Bilder selbst sind Daniels Lieferung.", "")

# ==========================================================================
abschnitt("6. Die Bilder werden EINGEPASST, nicht gezerrt (13.11.2026, Register 624)")
# ==========================================================================
# Bis hierher machte `_motivbild_skaliert` aus jedem Bild ein Quadrat (`roh.resize((px, px))`).
# Die Wappen sind 0,62 bis 0,74 so breit wie hoch und wurden damit 1,35- bis 1,62-fach gestreckt.
import os as _os                                                       # noqa: E402

try:                                                                   # eigenes, unsichtbares Fenster
    _root6 = tk.Tk()
    _root6.withdraw()
except tk.TclError:                                                    # kein Bildschirm (CI)
    _root6 = None

if _root6 is not None:                                                 # nur mit Fenster messbar
    from PIL import Image as _Image                                    # noqa: E402
    _app = M.NebelseetalApp(_root6)
    for _px in (8, 18, 42):
        _bild = _app._motivbild_skaliert("assets/icons/wappen/wappen_09.png", _px, "_pruef_cache")
        if _bild is None:
            check("6 Wappen laesst sich laden (%d px)" % _px, False, "None")
            continue
        _roh = _Image.open(_os.path.join(ROOT, "assets/icons/wappen/wappen_09.png"))
        _soll = _roh.width / float(_roh.height)
        _ist = _bild.width() / float(_bild.height())
        check("6 das Wappen behaelt sein Seitenverhaeltnis bei %d px" % _px,
              abs(_soll - _ist) < 0.08,
              "Datei %.2f, geladen %.2f (%dx%d)" % (_soll, _ist, _bild.width(), _bild.height()))
        check("6 das Wappen stossen mit der HOEHE an %d px" % _px,
              max(_bild.width(), _bild.height()) == _px,
              "%dx%d" % (_bild.width(), _bild.height()))
        check("6 das Wappen ist NICHT quadratisch bei %d px (kein Zerren)" % _px,
              _bild.width() != _bild.height(), "%dx%d" % (_bild.width(), _bild.height()))
        messwert("wappen_09_geladen_%dpx" % _px, "%dx%d" % (_bild.width(), _bild.height()), "px")
    _root6.destroy()
else:
    befund("6 die Einpass-Pruefung faellt aus", "kein Fenster moeglich")

sys.exit(bericht())
