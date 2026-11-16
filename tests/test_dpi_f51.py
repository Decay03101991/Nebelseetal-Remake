# -*- coding: ascii -*-
"""DPI-Umbau (F-51, Register 538/543) - das Spiel laeuft DPI-BEWUSST.

Daniels Entscheidung vom 12.11.2026 (Register 538, F-51): das Spiel startet mit
`SetProcessDpiAwareness(2)`. Damit ist 1 Tk-Pixel = 1 Bildpunkt, alles ist scharf, und das Fenster
ist physisch kleiner als vorher.

Was diese Datei beweist
-----------------------
1. QUELLE: `dpi_bewusst_machen()` steht in `main()` VOR dem ersten `tk.Tk()` - die einzige
   Reihenfolge, in der Windows die Skalierung abschaltet (spaeter gerufen wirkt sie nicht).
2. BEWUSST GEMESSEN (eigener Prozess): der Schirm meldet seine PHYSISCHE Groesse, und `k` ist
   genau die gemessene Skalierung (Schirm bewusst / Schirm weich). Das Fenster bleibt 1560 x 940
   (feste Formel), die Flaeche bleibt kleiner als das Fenster, und die linke Spalte waechst mit
   ihren Punktschriften. Die konkreten Zahlen sind MOMENTAUFNAHMEN der Skalierung (13.11.2026,
   125 %: 1920 x 1080, k = 1,251, Flaeche 1127 x 764; 16.11.2026, 150 %: 3840 x 2160, k = 1,5007,
   Flaeche 1099 x 740) und stehen darum NICHT mehr als Sollwert in der Wache.
3. GEGENPROBE (eigener Prozess OHNE den Aufruf): k = 1,0, der Schirm meldet die VIRTUELLE Groesse
   (kleiner als im bewussten Prozess), und die Flaeche ist eine andere. Damit ist belegt, dass die
   Zahlen aus 2 von der DPI-Zeile kommen und nicht von der Fensterformel.
4. SCHRIFTEN: `schrift(13)` ist bei k = 1,251 **16** px, bei k = 1,0 **13** px - und im bewussten
   Prozess genau `round(13 x gemessenes k)`; `schriftart` liefert die negative Tk-Pixelgroesse.
5. FOLGEN: nach F-57 ist der Abstand Spalte/Karte der GEMESSENE Rollbalken. `siedlungs_masse`
   ergibt mit rb 21 bei (1127, 764) Feld 64, Karte 658, Spalte **448**; mit rb 17 bei
   (1037, 589) 57 / 588 / **432**. Damit gilt S = W - rb - R und Spalte + Rollbalken fuellen den
   Platz bis zur Karte genau. Die alten Konstanten `SIEDLUNGS_ABSTAND` und
   `SIEDLUNGS_ROLLBALKEN` gibt es nicht mehr; ohne Messung gilt der gekennzeichnete Startwert.

ENTSCHEIDUNG F6 (Daniel 16.11.2026, Register 645): Bildschirmgroesse und k werden zur LAUFZEIT
gemessen; die Rechnung bleibt die Zusage. Ein fester Sollwert waere an Daniels Skalierung gebunden
und faerbt den Sammellauf rot, sobald er den Schirm umstellt (genau das war am 15./16.11.2026 der
Fall: 9 Fehler, ohne dass am Spiel etwas kaputt war).

Aufruf:  python -X utf8 tests/test_dpi_f51.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------  # noqa: E501
PRUEF_ART = "fenster+messen"
PRUEF_STUFE = 3
PRUEF_BETRIFFT = ['main:*']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src, messwert  # noqa: E402

ROOT, SRC = import_src()
import main  # noqa: E402

# Der Unterprozess misst in einem FRISCHEN Prozess - DPI-Bewusstsein gilt prozessweit und laesst
# sich im laufenden Prozess nicht zuruecknehmen. Darum zwei Laeufe.
PROBE = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
import main
modus = sys.argv[2]
if modus == "aware":
    main.dpi_bewusst_machen()
import tkinter as tk
root = tk.Tk()
root.geometry("1024x720+20+20")
try:
    root.attributes("-alpha", 0.01)
except Exception:
    pass
root.update()
d = {}
d["schirm"] = [root.winfo_screenwidth(), root.winfo_screenheight()]
d["fpixels"] = root.winfo_fpixels("1i")
d["k"] = main.dpi_faktor(root)
app = main.NebelseetalApp(root)
for _ in range(3):
    root.update()
    root.update_idletasks()
d["fenster"] = [root.winfo_width(), root.winfo_height()]
d["dpi_k"] = app.dpi_k
app._build_main_ui()
for _ in range(4):
    root.update()
    root.update_idletasks()
d["fenster_nach_ui"] = [root.winfo_width(), root.winfo_height()]
d["flaeche"] = [app.content_canvas.winfo_width(), app.content_canvas.winfo_height()]
# F6: der Abstand der Flaeche zum Fensterrand ist die linke Spalte (Menuespalten) plus Leisten -
# er waechst mit den Punktschriften und wird darum gemessen, nicht festgeschrieben.
d["spalte_breite"] = int(app.content_canvas.winfo_rootx() - root.winfo_rootx())
d["leiste_hoehe"] = int(app.content_canvas.winfo_rooty() - root.winfo_rooty())
d["schrift13"] = app.schrift(13)
d["schriftart13"] = list(app.schriftart(13))
d["schrift20fett"] = list(app.schriftart(20, fett=True))
# F-57: die Breite des Tk-Rollbalkens in DIESEM Prozess (er ist der Abstand Spalte/Karte).
_probe_rb = tk.Scrollbar(root, orient=tk.VERTICAL)
_probe_rb.pack()
root.update_idletasks()
d["rollbalken"] = int(_probe_rb.winfo_reqwidth())
_probe_rb.destroy()
print("PROBE" + json.dumps(d))
root.destroy()
'''


def probe(modus):
    """Den Unterprozess starten und seine Zahlen zurueckgeben (None bei Fehlschlag)."""
    pfad = os.path.join(tempfile.gettempdir(), "nebelseetal_dpi_probe_%s.py" % modus)
    with open(pfad, "w", encoding="ascii") as datei:
        datei.write(PROBE)
    umgebung = dict(os.environ)
    umgebung["PYTHONUTF8"] = "1"
    try:
        lauf = subprocess.run([sys.executable, "-X", "utf8", pfad, SRC, modus],
                              capture_output=True, text=True, timeout=180, env=umgebung)
    except Exception as e:                                          # noqa: BLE001
        befund("Unterprozess %s nicht startbar" % modus, repr(e))
        return None
    for zeile in (lauf.stdout or "").splitlines():
        if zeile.startswith("PROBE"):
            return json.loads(zeile[5:])
    befund("Unterprozess %s lieferte keine Messung" % modus, (lauf.stderr or "")[-400:])
    return None


# ==========================================================================
abschnitt("1. Die Quelle: der Aufruf steht VOR dem ersten Fenster")
# ==========================================================================
with open(os.path.join(SRC, "main.py"), "r", encoding="utf-8", errors="replace") as f:
    quelle = f.read()
check("main.dpi_bewusst_machen ist vorhanden", callable(getattr(main, "dpi_bewusst_machen", None)))
check("main.dpi_faktor ist vorhanden", callable(getattr(main, "dpi_faktor", None)))
_start = quelle.find("def main():")
check("main() steht in der Quelle", _start > 0, str(_start))
_teil = quelle[_start:_start + 4000] if _start > 0 else ""
_i_aufruf = _teil.find("dpi_bewusst_machen()")
_i_fenster = _teil.find("tk.Tk()")
check("main() ruft dpi_bewusst_machen() auf", _i_aufruf >= 0, str(_i_aufruf))
check("der Aufruf steht VOR tk.Tk() (sonst wirkt er nicht)",
      0 <= _i_aufruf < _i_fenster, "%d < %d" % (_i_aufruf, _i_fenster))

# Beide Prozesse einmal messen - die Vergleiche unten brauchen sie zusammen.
bewusst = probe("aware")
weich = probe("unaware")

# ==========================================================================
abschnitt("2. Bewusst gemessen: k ist die Skalierung, Flaeche und Schriften folgen aus k")
# ==========================================================================
if bewusst is None:
    befund("ohne Messung im bewussten Prozess nicht pruefbar")
else:
    for schluessel, wert in (("schirm", bewusst["schirm"]), ("fenster", bewusst["fenster"]),
                             ("flaeche", bewusst["flaeche"]), ("k", round(bewusst["k"], 4)),
                             ("schrift13", bewusst["schrift13"]),
                             ("spalte_breite", bewusst.get("spalte_breite")),
                             ("leiste_hoehe", bewusst.get("leiste_hoehe"))):
        messwert("dpi_" + schluessel, wert, "px" if schluessel != "k" else "Faktor")
    check("die App misst ihren DPI-Faktor selbst (dpi_k == gemessenes k)",
          abs(bewusst["dpi_k"] - bewusst["k"]) < 0.01,
          "dpi_k %.4f, k %.4f" % (bewusst["dpi_k"], bewusst["k"]))
    # Die Skalierung wird GEMESSEN: der bewusste Prozess sieht den physischen Schirm, der
    # unbewusste den virtuellen. Ihr Verhaeltnis IST k - keine Zahl aus alten Laeufen.
    if weich is None:
        befund("ohne die Gegenprobe ist die Skalierung nicht messbar")
    else:
        skalierung = bewusst["schirm"][0] / float(max(1, weich["schirm"][0]))
        messwert("skalierung", round(skalierung, 4), "Faktor")
        check("k im bewussten Prozess ist die gemessene Skalierung (Schirm bewusst / Schirm weich)",
              abs(bewusst["k"] - skalierung) < 0.01,
              "k %.4f gegen Skalierung %.4f" % (bewusst["k"], skalierung))
        _erwartet = [int(round(weich["schirm"][0] * skalierung)),
                     int(round(weich["schirm"][1] * skalierung))]
        check("der bewusste Schirm ist das k-fache des unbewussten (physisch statt virtuell)",
              abs(bewusst["schirm"][0] - _erwartet[0]) <= 2
              and abs(bewusst["schirm"][1] - _erwartet[1]) <= 2,
              "%s gegen %s x %.4f = %s" % (bewusst["schirm"], weich["schirm"], skalierung, _erwartet))
    # Die Fensterformel steht in main.py: breite = max(1024, min(1560, Schirm - 90)),
    # hoehe = max(720, min(940, Schirm - 120)). Der Sollwert kommt aus dem GEMESSENEN Schirm.
    _soll_fenster = [max(1024, min(1560, bewusst["schirm"][0] - 90)),
                     max(720, min(940, bewusst["schirm"][1] - 120))]
    check("das Fenster folgt der Formel aus dem gemessenen Schirm (max 1560 x 940)",
          bewusst["fenster"] == _soll_fenster,
          "%s, erwartet %s" % (bewusst["fenster"], _soll_fenster))
    check("das Fenster bleibt nach dem Aufbau gleich gross",
          bewusst["fenster_nach_ui"] == bewusst["fenster"],
          "%s / %s" % (bewusst["fenster_nach_ui"], bewusst["fenster"]))
    # Was NICHT aus k folgt, ist die Fensterformel - aber die Flaeche muss kleiner sein als das
    # Fenster, sonst liegen Leisten und Spalte ausserhalb.
    check("die sichtbare Flaeche ist kleiner als das Fenster (Leisten und Spalte bleiben)",
          bewusst["flaeche"][0] < bewusst["fenster"][0]
          and bewusst["flaeche"][1] < bewusst["fenster"][1],
          "%s in %s" % (bewusst["flaeche"], bewusst["fenster"]))
    if weich is not None and bewusst.get("spalte_breite") and weich.get("spalte_breite"):
        if abs(bewusst["k"] - weich["k"]) < 0.01:
            befund("keine Skalierung messbar (k bewusst %.4f, weich %.4f) - die Spalte kann nicht "
                   "wachsen" % (bewusst["k"], weich["k"]))
        else:
            check("die linke Spalte waechst mit den Punktschriften (bewusst breiter als weich)",
                  bewusst["spalte_breite"] > weich["spalte_breite"],
                  "%d gegen %d px" % (bewusst["spalte_breite"], weich["spalte_breite"]))
    # F-57: der Abstand Spalte/Karte IST der Rollbalken - darum wird er hier gemessen.
    messwert("rollbalken_bewusst", bewusst.get("rollbalken"), "px")
    if weich is not None:
        check("der Tk-Rollbalken ist im bewussten Prozess nicht schmaler als im weichen",
              int(bewusst.get("rollbalken") or 0) >= int(weich.get("rollbalken") or 0),
              "%s gegen %s" % (bewusst.get("rollbalken"), weich.get("rollbalken")))

# ==========================================================================
abschnitt("3. Gegenprobe: OHNE den Aufruf ist k = 1,0 und der Schirm virtuell")
# ==========================================================================
if weich is None:
    befund("ohne Messung im nicht-bewussten Prozess nicht pruefbar")
else:
    for schluessel in ("schirm", "fenster", "flaeche"):
        messwert("weich_" + schluessel, weich[schluessel], "px")
    messwert("weich_k", round(weich["k"], 4), "Faktor")
    check("ohne den Aufruf ist k = 1,0", abs(weich["k"] - 1.0) < 0.001, "%.4f" % weich["k"])
    check("ohne den Aufruf ist die Flaeche kleiner als das Fenster",
          weich["flaeche"][0] < weich["fenster"][0] and weich["flaeche"][1] < weich["fenster"][1],
          "%s in %s" % (weich["flaeche"], weich["fenster"]))
    if bewusst is not None:
        check("ohne den Aufruf ist der Schirm nie groesser als im bewussten Prozess",
              weich["schirm"][0] <= bewusst["schirm"][0]
              and weich["schirm"][1] <= bewusst["schirm"][1],
              "%s gegen %s" % (weich["schirm"], bewusst["schirm"]))
        if weich["schirm"] == bewusst["schirm"]:
            befund("kein Unterschied zwischen bewusst und weich (Schirm %s) - ohne Skalierung ist "
                   "das richtig" % (bewusst["schirm"],))
        if abs(bewusst["k"] - weich["k"]) < 0.01:
            befund("ohne Skalierung sind die Flaechen gleich (%s) - die DPI-Zeile ist dann "
                   "wirkungslos, das ist kein Fehler" % (bewusst["flaeche"],))
        else:
            check("die DPI-Zeile ist die Ursache: Flaeche bewusst != Flaeche weich",
                  bewusst["flaeche"] != weich["flaeche"],
                  "%s gegen %s" % (bewusst["flaeche"], weich["flaeche"]))

# ==========================================================================
abschnitt("4. Schriften: folgen k (Tabelle bei k = 1,251 und k = 1,0, dazu das gemessene k)")
# ==========================================================================


class _Stellvertreter:
    """Nur `dpi_k` - die Rechnung von `schrift` braucht kein Fenster."""

    def __init__(self, k):
        self.dpi_k = k

    schrift = main.NebelseetalApp.schrift
    schriftart = main.NebelseetalApp.schriftart


_gross = _Stellvertreter(1.251231527093596)
_klein = _Stellvertreter(1.0)
for pixel, soll_gross, soll_klein in ((12, 15, 12), (13, 16, 13), (15, 19, 15),
                                       (20, 25, 20), (25, 31, 25)):
    check("schrift(%d) bei k = 1,251 ist %d" % (pixel, soll_gross),
          _gross.schrift(pixel) == soll_gross, str(_gross.schrift(pixel)))
    check("schrift(%d) bei k = 1,0 ist %d" % (pixel, soll_klein),
          _klein.schrift(pixel) == soll_klein, str(_klein.schrift(pixel)))
check("schriftart(13) ist eine negative Pixelgroesse", _gross.schriftart(13) == ("Arial", -16),
      str(_gross.schriftart(13)))
check("schriftart(20, fett=True) traegt bold", _gross.schriftart(20, fett=True) ==
      ("Arial", -25, "bold"), str(_gross.schriftart(20, fett=True)))
if bewusst is not None:
    # F6: der Sollwert ist die RECHNUNG mit dem gemessenen k, nicht die Zahl von damals.
    _soll13 = int(round(13 * bewusst["k"]))
    check("die App rechnet im bewussten Prozess mit schrift(13) = round(13 x k)",
          bewusst["schrift13"] == _soll13,
          "gemessen %s, erwartet %d (k %.4f)" % (bewusst["schrift13"], _soll13, bewusst["k"]))
    check("schriftart(13) traegt genau diese Pixelgroesse",
          list(bewusst["schriftart13"]) == ["Arial", -_soll13],
          str(bewusst["schriftart13"]))
    messwert("schriftart_13_bewusst", bewusst["schriftart13"], "-")
    messwert("schriftart_20_fett_bewusst", bewusst["schrift20fett"], "-")

# ==========================================================================
abschnitt("5. Folgen fuer die Siedlung: S = W - rb - R (F-57)")
# ==========================================================================
# F-57 (Daniel 12.11.2026): der Abstand Spalte/Karte ist der GEMESSENE Rollbalken. Mit rb 21 ist
# die Spalte bei (1127, 764) 448 breit, mit rb 17 bei (1037, 589) 432 - nicht mehr 453 / 433.
# Diese Rechnung ist reine Arithmetik mit festen Eingaben und darum unabhaengig vom Schirm.
for (breite, hoehe, rb), soll in (((1127, 764, 21), {"feld": 64, "karte": 658, "spalte": 448}),
                                  ((1037, 589, 17), {"feld": 57, "karte": 588, "spalte": 432})):
    masse = main.siedlungs_masse(breite, hoehe, rollbalken=rb)
    for schluessel, wert in soll.items():
        check("%d x %d (rb %d): %s = %d" % (breite, hoehe, rb, schluessel, wert),
              masse[schluessel] == wert, str(masse[schluessel]))
    check("%d x %d: Spalte + Rollbalken + Karte fuellen die Breite genau" % (breite, hoehe),
          masse["spalte"] + rb + masse["karte"] == breite,
          "%d + %d + %d" % (masse["spalte"], rb, masse["karte"]))
    messwert("siedlung_%dx%d" % (breite, hoehe), masse["feld"], "px Feld")
_neu = main.siedlungs_masse(1127, 764, rollbalken=21)
check("bei der neuen Flaeche ist das Feld auf dem Originalmass 64 gedeckelt",
      _neu["feld"] == main.SIEDLUNGS_FELD_MAX, str(_neu["feld"]))
check("das historische Kartenbild wird dann NICHT mehr verkleinert (10 x 64 = 640)",
      10 * _neu["feld"] == 640, str(10 * _neu["feld"]))
# Und mit dem GEMESSENEN Rollbalken aus dem bewussten Prozess muss die Rechnung genauso aufgehen.
if bewusst is not None and bewusst.get("rollbalken") and bewusst.get("flaeche"):
    _gemessen = main.siedlungs_masse(bewusst["flaeche"][0], bewusst["flaeche"][1],
                                     rollbalken=int(bewusst["rollbalken"]))
    # F6 (16.11.2026): die Identitaet gilt nur im NEBENEINANDER. Ist die Flaeche zu klein, steht die
    # Karte uebereinander und nimmt die volle Breite - dann ist die Zusage eine andere.
    if _gemessen.get("uebereinander"):
        befund("Flaeche %s zu klein fuer Spalte und Karte nebeneinander - die Ansicht ist gestapelt"
               % (bewusst["flaeche"],))
        check("gestapelt: die Spalte nimmt die volle Breite, die Karte steht darueber",
              _gemessen["spalte"] == bewusst["flaeche"][0]
              and _gemessen["karte"] <= bewusst["flaeche"][0],
              "spalte %d, karte %d, Flaeche %d" % (_gemessen["spalte"], _gemessen["karte"],
                                                   bewusst["flaeche"][0]))
    else:
        check("mit dem gemessenen Rollbalken (rb %s) fuellen Spalte + Rollbalken + Karte die Flaeche"
              % bewusst.get("rollbalken"),
              _gemessen["spalte"] + int(bewusst["rollbalken"]) + _gemessen["karte"]
              == bewusst["flaeche"][0],
              "%d + %d + %d gegen %d" % (_gemessen["spalte"], int(bewusst["rollbalken"]),
                                         _gemessen["karte"], bewusst["flaeche"][0]))
# Quelltext-Wache: die beiden von Hand gesetzten Konstanten sind weg (F-57).
check("SIEDLUNGS_ABSTAND gibt es nicht mehr",
      not hasattr(main, "SIEDLUNGS_ABSTAND"), str(getattr(main, "SIEDLUNGS_ABSTAND", "-")))
check("SIEDLUNGS_ROLLBALKEN gibt es nicht mehr",
      not hasattr(main, "SIEDLUNGS_ROLLBALKEN"), str(getattr(main, "SIEDLUNGS_ROLLBALKEN", "-")))
check("der Startwert ist als solcher gekennzeichnet und 17",
      main.SIEDLUNGS_ROLLBALKEN_ERWARTET == 17, str(main.SIEDLUNGS_ROLLBALKEN_ERWARTET))
check("rollbalken_breite() liefert ohne Messung den Startwert",
      main.rollbalken_breite() in (17, getattr(main, "_ROLLBALKEN_GEMESSEN", None)),
      str(main.rollbalken_breite()))
# GEGENPROBE: ohne Rollbalken waere die Spalte um genau rb breiter - die Zahl kommt also aus rb.
_ohne = main.siedlungs_masse(1127, 764, rollbalken=0)
check("Gegenprobe: mit rb 0 ist die Spalte 21 px breiter (469 statt 448)",
      _ohne["spalte"] == 469, str(_ohne["spalte"]))

bericht()
