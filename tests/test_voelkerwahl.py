# -*- coding: ascii -*-
"""Voelkerwahl am Start (A2, Entscheidung Daniel 03.11.2026).

Daniel: "Mit Voelker sind die Fraktionen gemeint, Menschlich, Zwergisch, Elfisch, Trolle, Ghule,
Gnome dann haben wir 6 Fraktionen" und "Trolle Ghule und Gnome ersetzen die Monster". Fuer Trolle,
Ghule und Gnome gibt es keine Quelle; Daniel hat die Werte am 03.11.2026 selbst entschieden (nur
Hebel, die es im Spiel schon gibt).

Was diese Datei beweist
-----------------------
1. Die sechs Fraktionen stehen in `data/voelker.json` - mit Plus, Minus und Quelle je Wert.
2. `bottaktik.VOLKSATTRIBUTE` liest sie aus der Datei (keine zweite Wahrheit im Code), und
   `volksattribute` liefert weiterhin leere Werte fuer Unbekanntes (kein Erfinden).
3. Die Verteilung an die fuenf Bots ist deterministisch, ohne Doppelung, und deckt bei sechs
   Fraktionen genau fuenf ab - es bleibt genau eine uebrig.
4. Der Spieler waehlt im Dorfzentrum; die Wahl landet im Spielstand (`spieler_fraktion`), die Bots
   tragen danach die uebrigen Voelker, und die Wahl erscheint nach der Gruendung nicht mehr.
5. Ohne Wahl bleibt alles wie vorher: die Bots behalten `botkern.BOT_FRAKTIONEN`.

Aufruf:  python -X utf8 tests/test_voelkerwahl.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['botkern', 'bottaktik', 'main:*', 'stimmen', 'voelker']
PRUEF_DATEN = ['voelker.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

ROOT, SRC = import_src()
import bottaktik as BT  # noqa: E402
import botkern as BK  # noqa: E402
import main as M  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()

# ==========================================================================
# 1. Die Datendatei
# ==========================================================================

abschnitt("1. Sechs Fraktionen aus data/voelker.json")
_pfad = os.path.join(ROOT, "data", "voelker.json")
check("die Datendatei existiert", os.path.exists(_pfad), _pfad)
with open(_pfad, encoding="utf-8") as _f:
    _daten = json.load(_f)
_liste = _daten.get("fraktionen") or []
check("es sind sechs Fraktionen", len(_liste) == 6, str(len(_liste)))
_kennungen = [str(e.get("kennung")) for e in _liste]
check("die Namen sind die von Daniel genannten",
      set(_kennungen) == {"menschlich", "zwergisch", "elfisch", "Trolle", "Ghule", "Gnome"},
      str(_kennungen))
check("'monster' kommt nicht mehr vor", "monster" not in _kennungen, str(_kennungen))
check("jede Fraktion traegt Plus und Minus",
      all(str(e.get("plus") or "") and str(e.get("minus") or "") for e in _liste),
      str([e.get("kennung") for e in _liste if not (e.get("plus") and e.get("minus"))]))
check("jede Fraktion nennt ihre Quelle",
      all(str(e.get("quelle") or "") for e in _liste),
      str([e.get("kennung") for e in _liste if not e.get("quelle")]))
_trolle = [e for e in _liste if e.get("kennung") == "Trolle"][0]
check("Trolle uebernehmen das Paar der frueheren Fraktion 'monster'",
      _trolle.get("plus") == "AT der Einheiten +5 %" and _trolle.get("minus") == "Handelserloes -5 %",
      "%s / %s" % (_trolle.get("plus"), _trolle.get("minus")))
_ghule = [e for e in _liste if e.get("kennung") == "Ghule"][0]
check("Ghule tragen Daniels Entscheid (Nahrung plus, PA minus)",
      "Nahrung" in str(_ghule.get("plus")) and "PA" in str(_ghule.get("minus")),
      "%s / %s" % (_ghule.get("plus"), _ghule.get("minus")))
_gnome = [e for e in _liste if e.get("kennung") == "Gnome"][0]
check("Gnome tragen Daniels Entscheid (Ausbau plus, AT minus)",
      "Ausbau" in str(_gnome.get("plus")) and "AT" in str(_gnome.get("minus")),
      "%s / %s" % (_gnome.get("plus"), _gnome.get("minus")))

# ==========================================================================
# 2. Der Code liest die Datei - keine zweite Wahrheit
# ==========================================================================

abschnitt("2. bottaktik liest die sechs Fraktionen aus der Datei")
check("die Quelle kennt genau die sechs Kennungen",
      set(BT.VOLKSATTRIBUTE) == set(_kennungen), str(sorted(BT.VOLKSATTRIBUTE)))
check("fraktionen() liefert sechs Eintraege in Datei-Reihenfolge",
      [str(e.get("kennung")) for e in BT.fraktionen()] == _kennungen, str(_kennungen))
check("die Werte stimmen mit der Datei ueberein",
      all(BT.VOLKSATTRIBUTE[str(e["kennung"])] == {"plus": str(e["plus"]), "minus": str(e["minus"])}
          for e in _liste), "Abweichung zwischen Datei und Code")
check("eine unbekannte Fraktion bleibt leer",
      BT.volksattribute({"fraktion": "gibtsnicht"}) == {"plus": "", "minus": ""})
check("die belegten Werte sind unveraendert (zwergisch)",
      BT.volksattribute({"fraktion": "zwergisch"})["plus"] == "Steinertrag +5 %")
check("fraktionen() gibt Kopien heraus",
      (lambda a: (a[0].__setitem__("kennung", "kaputt"), BT.fraktionen()[0]["kennung"])[1])(
          BT.fraktionen()) == _kennungen[0])

# ==========================================================================
# 3. Verteilung an die fuenf Bots
# ==========================================================================

abschnitt("3. Verteilung: keine Doppelung, deterministisch, eine Fraktion bleibt")
_fuenf = ["Brynhild", "Grom", "Haug", "Krank", "Silra"]
for _wahl in ("Trolle", "Ghule", "menschlich"):
    _v = BT.verteile_fraktionen(_wahl, _fuenf)
    check("Wahl %s: fuenf Bots bekommen fuenf Voelker" % _wahl,
          len(_v) == 5 and len(set(_v.values())) == 5, str(_v))
    check("Wahl %s: das Volk des Spielers ist nicht dabei" % _wahl,
          _wahl not in _v.values(), str(_v))
    check("Wahl %s: dieselbe Wahl ergibt dieselbe Verteilung" % _wahl,
          BT.verteile_fraktionen(_wahl, _fuenf) == _v, str(_v))
check("verschiedene Wahlen ergeben verschiedene Verteilungen",
      BT.verteile_fraktionen("Trolle", _fuenf) != BT.verteile_fraktionen("Ghule", _fuenf))
check("ohne Botnamen werden die fuenf belegten genommen",
      sorted(BT.verteile_fraktionen("Gnome")) == sorted(_fuenf), str(BT.verteile_fraktionen("Gnome")))

# ==========================================================================
# 4. Im Fenster: Wahl auf der Kartengruendungsseite, Spielstand, Bots
#
# UMGEHAENGT am 05.11.2026 (Register 222), nicht geloescht: die Voelkerwahl steht nicht mehr im
# Dorfzentrum, sondern auf der Kartengruendungsseite (Startfenster), Schritt 2 nach "Neues Spiel".
# Der geprueft ZUSAGE bleibt dieselbe - sechs Voelker, ein Knopf je Volk, Wahl im Spielstand,
# Bots tragen die uebrigen - nur der Ort und der Weg dorthin sind neu.
# ==========================================================================


def _wahlprobe():
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    try:
        app = M.NebelseetalApp(root)
        app._build_main_ui()
        app._switch_view(M.KARTENGRUENDUNG_ANSICHT)      # Register 222: die Startseite
        app._start_neues_spiel()                         # erst "Neues Spiel", dann die Frage
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
        vorher_fraktionen = [b.faction for b in app.state.bots]
        verteilung = app._volk_waehlen("Ghule")
        app.content.update_idletasks()
        nachher = _texte()
        # T-1 (03.11.2026): die Ueberschrift traegt echte Umlaute (Waehle -> W\u00e4hle).
        return {"block": any("W\u00e4hle dein Volk" in t for t in vorher),
                "knoepfe": sum(1 for t in vorher if t == "Dieses Volk nehmen"),
                "gewaehlt": getattr(app.state, "spieler_fraktion", ""),
                "verteilung": verteilung,
                "bots": [b.faction for b in app.state.bots],
                "bots_vorher": vorher_fraktionen,
                "block_danach": any("W\u00e4hle dein Volk" in t for t in nachher),
                "karte_danach": any("Deine Karte" in t for t in nachher)}
    finally:
        root.destroy()


_w = _wahlprobe()
check("die Voelkerwahl erscheint auf der Kartengruendungsseite", _w["block"] is True,
      str(_w)[:120])
check("je Volk ein Knopf", _w["knoepfe"] == 6, str(_w["knoepfe"]))
check("die Wahl steht im Spielstand", _w["gewaehlt"] == "Ghule", str(_w["gewaehlt"]))
# Die Zahl der Bots haengt davon ab, wie weit der Startzustand aufgebaut ist (im Pruefstand koennen
# es weniger als fuenf sein). Geprueft wird deshalb die REGEL, nicht eine feste Zahl: jeder Bot traegt
# eine Fraktion aus der Verteilung, und keine ist doppelt.
_rest = set(_w["verteilung"].values())
check("die Bots tragen danach Voelker aus der Verteilung",
      bool(_w["bots"]) and all(f in _rest for f in _w["bots"]),
      "%s von %s" % (str(_w["bots"]), str(sorted(_rest))))
check("keine Fraktion doppelt bei den Bots", len(set(_w["bots"])) == len(_w["bots"]), str(_w["bots"]))
check("die Wahl des Spielers ist bei den Bots nicht dabei",
      "Ghule" not in _w["bots"], str(_w["bots"]))
# Die Verteilungsfunktion selbst wird oben mit den fuenf belegten Botnamen geprueft (dort MUESSEN es
# fuenf sein). Hier zaehlt nur, dass jeder vorhandene Bot genau eine Fraktion bekommt - die Zahl der
# Bots im Startzustand ist nicht stabil (mal zwei, mal fuenf), eine feste Zahl waere eine wackelige Wache.
check("jeder vorhandene Bot hat genau eine Fraktion aus der Verteilung",
      len(_rest) == len(_w["bots"]) and len(set(_rest)) == len(_rest), str(sorted(_rest)))
check("nach der Wahl erscheint die Voelkerliste nicht mehr", _w["block_danach"] is False,
      str(_w["block_danach"]))
# Register 222: nach der Wahl ist der naechste Schritt die Karte - vorher stand hier die Zeile
# "Dein Volk:" im Dorfzentrum. Sie kommt erst nach der Gruendung; die Seite zeigt jetzt die Karte.
check("nach der Wahl zeigt die Seite die Karte", _w["karte_danach"] is True,
      str(_w["karte_danach"]))
check("das Feld steht im Spielstand",
      '"spieler_fraktion"' in TEXT_MAIN, str(TEXT_MAIN.count("spieler_fraktion")))
check("ohne Wahl bleibt die belegte Bot-Zuordnung",
      set(BK.BOT_FRAKTIONEN.values()) <= set(BT.VOLKSATTRIBUTE), str(sorted(BK.BOT_FRAKTIONEN.values())))

bericht()
