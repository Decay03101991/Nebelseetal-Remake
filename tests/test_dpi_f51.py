# -*- coding: ascii -*-
"""DPI-Umbau (F-51, Register 538/543) - das Spiel laeuft DPI-BEWUSST.

Daniels Entscheidung vom 12.11.2026 (Register 538, F-51): das Spiel startet mit
`SetProcessDpiAwareness(2)`. Damit ist 1 Tk-Pixel = 1 Bildpunkt, alles ist scharf, und das Fenster
ist physisch kleiner als vorher.

Was diese Datei beweist
-----------------------
1. QUELLE: `dpi_bewusst_machen()` steht in `main()` VOR dem ersten `tk.Tk()` - die einzige
   Reihenfolge, in der Windows die Skalierung abschaltet (spaeter gerufen wirkt sie nicht).
2. BEWUSST GEMESSEN (eigener Prozess): Schirm 1920 x 1080, `winfo_fpixels('1i')` = 120,1,
   k = 1,251, Fenster 1560 x 940, sichtbare Flaeche 1127 x 764.
3. GEGENPROBE (eigener Prozess OHNE den Aufruf): Schirm meldet 1536 x 864, k = 1,0, Fenster
   1446 x 744, sichtbare Flaeche 1037 x 589. Damit ist belegt, dass die Zahlen aus 2 von der
   DPI-Zeile kommen und nicht von der Fensterformel.
4. SCHRIFTEN: `schrift(13)` ist bei k = 1,251 **16** px und bei k = 1,0 **13** px; `schriftart`
   liefert die negative Tk-Pixelgroesse.
5. FOLGEN: `siedlungs_masse(1127, 764)` ergibt Feld 64, Karte 658, Spalte 453 - und fuer die alte
   Flaeche weiter 57 / 588 / 433. Die Spalte ist 1 px breiter als in Claudes R2, weil der
   Siedlungsabstand 16 px ist und R2 mit 17 px rechnet (im Auftrag Nr. 15 gefragt).

Aufruf:  python -X utf8 tests/test_dpi_f51.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src, messwert

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
d["schrift13"] = app.schrift(13)
d["schriftart13"] = list(app.schriftart(13))
d["schrift20fett"] = list(app.schriftart(20, fett=True))
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

# ==========================================================================
abschnitt("2. Bewusst gemessen: 1920 x 1080, k = 1,251, Fenster 1560 x 940, Flaeche 1127 x 764")
# ==========================================================================
bewusst = probe("aware")
if bewusst is None:
    befund("ohne Messung im bewussten Prozess nicht pruefbar")
else:
    for schluessel, wert in (("schirm", bewusst["schirm"]), ("fenster", bewusst["fenster"]),
                             ("flaeche", bewusst["flaeche"]), ("k", round(bewusst["k"], 4)),
                             ("schrift13", bewusst["schrift13"])):
        messwert("dpi_" + schluessel, wert, "px" if schluessel != "k" else "Faktor")
    check("DPI-Bewusstsein ist im Unterprozess gesetzt", bewusst["dpi_k"] > 1.2,
          str(round(bewusst["dpi_k"], 4)))
    check("der Schirm meldet die physische Groesse 1920 x 1080",
          bewusst["schirm"] == [1920, 1080], str(bewusst["schirm"]))
    check("k = winfo_fpixels('1i') / 96 ist 1,251 (gemessen, nicht gerechnet)",
          abs(bewusst["k"] - 1.2513) < 0.002, "%.4f" % bewusst["k"])
    check("das Fenster ist 1560 x 940 Tk-px (Formel, nicht fest)",
          bewusst["fenster"] == [1560, 940], str(bewusst["fenster"]))
    check("das Fenster bleibt nach dem Aufbau 1560 x 940",
          bewusst["fenster_nach_ui"] == bewusst["fenster"],
          "%s / %s" % (bewusst["fenster_nach_ui"], bewusst["fenster"]))
    # ENTSCHEIDUNG (F-51): die MENUESPALTEN wachsen mit ihren Punktschriften um 24 px, die obere
    # Leiste um 19 px. Darum ist die Flaeche 1127 x 764 und NICHT die gerechneten 1151 x 785
    # (Claudes F1 aus Nr. 14 hat genau das vermutet).
    check("die sichtbare Flaeche ist 1127 x 764 (Menuespalten wachsen mit)",
          bewusst["flaeche"] == [1127, 764], str(bewusst["flaeche"]))
    check("senkrecht: 940 - 176 = 764 (Leiste 141 + Status 23 + Rahmen 12)",
          940 - bewusst["flaeche"][1] == 176, str(940 - bewusst["flaeche"][1]))
    check("waagerecht: 1560 - 433 = 1127 (linke Spalte mit DPI-Schriften)",
          1560 - bewusst["flaeche"][0] == 433, str(1560 - bewusst["flaeche"][0]))

# ==========================================================================
abschnitt("3. Gegenprobe: OHNE den Aufruf bleibt es weich (1536 x 864, k = 1,0, 1037 x 589)")
# ==========================================================================
weich = probe("unaware")
if weich is None:
    befund("ohne Messung im nicht-bewussten Prozess nicht pruefbar")
else:
    for schluessel in ("schirm", "fenster", "flaeche"):
        messwert("weich_" + schluessel, weich[schluessel], "px")
    messwert("weich_k", round(weich["k"], 4), "Faktor")
    check("ohne den Aufruf ist k = 1,0", abs(weich["k"] - 1.0) < 0.001, "%.4f" % weich["k"])
    check("ohne den Aufruf meldet der Schirm nur 1536 x 864",
          weich["schirm"] == [1536, 864], str(weich["schirm"]))
    check("ohne den Aufruf ist die Flaeche 1037 x 589 (der alte Zustand)",
          weich["flaeche"] == [1037, 589], str(weich["flaeche"]))
    check("die DPI-Zeile ist die Ursache: Flaeche bewusst != Flaeche weich",
          bewusst is None or bewusst["flaeche"] != weich["flaeche"],
          "%s gegen %s" % (bewusst["flaeche"] if bewusst else "?", weich["flaeche"]))

# ==========================================================================
abschnitt("4. Schriften: schrift(13) ist 16 bei k = 1,251 und 13 bei k = 1,0")
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
    check("die App rechnet im bewussten Prozess mit schrift(13) = 16",
          bewusst["schrift13"] == 16, str(bewusst["schrift13"]))
    messwert("schriftart_13_bewusst", bewusst["schriftart13"], "-")
    messwert("schriftart_20_fett_bewusst", bewusst["schrift20fett"], "-")

# ==========================================================================
abschnitt("5. Folgen fuer die Siedlung: Feld 64, Karte 658, Spalte 453 bei 1127 x 764")
# ==========================================================================
for (breite, hoehe), soll in (((1127, 764), {"feld": 64, "karte": 658, "spalte": 453}),
                              ((1037, 589), {"feld": 57, "karte": 588, "spalte": 433})):
    masse = main.siedlungs_masse(breite, hoehe)
    for schluessel, wert in soll.items():
        check("%d x %d: %s = %d" % (breite, hoehe, schluessel, wert),
              masse[schluessel] == wert, str(masse[schluessel]))
    messwert("siedlung_%dx%d" % (breite, hoehe), masse["feld"], "px Feld")
_neu = main.siedlungs_masse(1127, 764)
check("bei der neuen Flaeche ist das Feld auf dem Originalmass 64 gedeckelt",
      _neu["feld"] == main.SIEDLUNGS_FELD_MAX, str(_neu["feld"]))
check("das historische Kartenbild wird dann NICHT mehr verkleinert (10 x 64 = 640)",
      10 * _neu["feld"] == 640, str(10 * _neu["feld"]))
# Claudes R2 (Nr. 14) rechnet S = W - 17 - R; die Siedlung nimmt SIEDLUNGS_ABSTAND = 16.
check("die Siedlungsspalte ist 1 px breiter als Claudes R2 (16 gegen 17 px Abstand)",
      _neu["spalte"] == 1127 - main.SIEDLUNGS_ABSTAND - _neu["karte"],
      "%d gegen %d" % (_neu["spalte"], 1127 - main.SIEDLUNGS_ROLLBALKEN - _neu["karte"]))
check("im Abstand steht der gemessene Rollbalken von 17 px",
      main.SIEDLUNGS_ROLLBALKEN == 17, str(main.SIEDLUNGS_ROLLBALKEN))

bericht()
