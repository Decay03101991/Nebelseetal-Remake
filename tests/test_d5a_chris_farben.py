# -*- coding: ascii -*-
"""Wache: die Gelaendefarben der Weltkarte stehen auf Chris' Palette (D-5a, Register 356).

DANIELS ENTSCHEIDUNG (09.11.2026, 20:0x, eine Runde mit Bildvergleich)
----------------------------------------------------------------------
Drei Fassungen lagen vor: "heute (D-4)", "A - Chris woertlich" (Median je Gelaendeart aus den
gelieferten Bildern gemessen) und "B - Chris' Farbton, lesbar". Daniel hat **B** gewaehlt: Chris'
Farbton, Helligkeit fuer die 20-px-Felder angehoben. Die Tannen bleiben, wie sie sind
("nur die Farben in data/gelaende.json, Zeichner unangetastet").

WAS DIESE DATEI PRUEFT
----------------------
1. Die sieben Farben kommen aus `data/gelaende.json` - der EINEN Quelle - und stehen NICHT als
   zweite Tabelle im Quelltext.
2. Jede Farbe liegt in einem lesbaren Helligkeitsband (A waere hier durchgefallen: Wald #182315
   hat Helligkeit 30, Berg #B6B6C6 liegt bei 182).
3. Die Ordnung der Farben bleibt erkennbar: Wald am dunkelsten, Berg am hellsten, Nebelsee
   deutlich blau (b > r).
4. Die sieben Farben liegen weit genug auseinander, um sie auf 20 px zu unterscheiden; der Rand
   ist ueberall dunkler als die Flaeche.

Aufruf:  .venv/Scripts/python.exe -X utf8 tests/test_d5a_chris_farben.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
import gelaende  # noqa: E402

ARTEN = ("grasland", "steppe", "wald", "huegel", "berg", "nebelsee", "sumpf")


def _rgb(text: str) -> tuple:
    """'#RRGGBB' -> (r, g, b)."""
    rein = str(text).strip().lstrip("#")
    return tuple(int(rein[i:i + 2], 16) for i in (0, 2, 4))


def _helligkeit(rgb) -> float:
    """Wahrgenommene Helligkeit (ITU-R BT.601) - dieselbe Formel wie im Pruefbericht."""
    return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]


def _abstand(a, b) -> float:
    return sum((a[i] - b[i]) ** 2 for i in range(3)) ** 0.5


# ==========================================================================
abschnitt("1. Eine Quelle: data/gelaende.json, keine zweite Farbtabelle")
# ==========================================================================
pfad = os.path.join(ROOT, "data", "gelaende.json")
check("1 data/gelaende.json liegt da", os.path.exists(pfad), pfad)
with open(pfad, encoding="utf-8") as f:
    daten = json.load(f)
farben = {a["id"]: str(a["farbe"]) for a in daten["gelaendearten"]}
raender = {a["id"]: str(a["farbe_rand"]) for a in daten["gelaendearten"]}
check("1 genau die sieben Gelaendearten", tuple(farben) == ARTEN, repr(tuple(farben)))
check("1 alle sieben Farben sind #RRGGBB", all(len(v) == 7 and v.startswith("#") for v in farben.values()),
      repr(sorted(set(farben.values()))))
check("1 gelaende.farbe liefert genau diese Werte",
      all(gelaende.farbe(art).upper() == farben[art].upper() for art in ARTEN), "")
for name in ("main.py", "weltkarte_malerei.py"):
    with open(os.path.join(SRC, name), encoding="utf-8") as f:
        quelle = f.read().upper()
    doppelt = [art for art in ARTEN if farben[art].lstrip("#").upper() in quelle]
    check("1 %s fuehrt keine zweite Farbtabelle" % name, not doppelt, repr(doppelt))

# ==========================================================================
abschnitt("2. Lesbares Helligkeitsband (A waere hier durchgefallen)")
# ==========================================================================
hell = {art: _helligkeit(_rgb(farben[art])) for art in ARTEN}
zu_dunkel = [art for art in ARTEN if hell[art] < 50]
zu_hell = [art for art in ARTEN if hell[art] > 185]
check("2 keine Gelaendefarbe ist zu dunkel (< 50)", not zu_dunkel,
      repr([(art, round(hell[art])) for art in zu_dunkel]))
check("2 keine Gelaendefarbe ist zu hell (> 185)", not zu_hell,
      repr([(art, round(hell[art])) for art in zu_hell]))
befund("2 gemessene Helligkeiten (Daniels Fassung B)",
       ", ".join("%s %.0f" % (art, hell[art]) for art in ARTEN))

# ==========================================================================
abschnitt("3. Die Ordnung bleibt erkennbar")
# ==========================================================================
check("3 Wald ist die dunkelste Gelaendeart", hell["wald"] == min(hell.values()),
      "Wald %.0f gegen Minimum %.0f" % (hell["wald"], min(hell.values())))
check("3 Berg ist heller als jede andere Art", hell["berg"] == max(hell.values()),
      "Berg %.0f gegen Maximum %.0f" % (hell["berg"], max(hell.values())))
check("3 Grasland ist heller als Wald (Gruen gegen Nadelgruen)",
      hell["grasland"] > hell["wald"], "%.0f gegen %.0f" % (hell["grasland"], hell["wald"]))
check("3 Steppe ist heller als Huegel", hell["steppe"] > hell["huegel"],
      "%.0f gegen %.0f" % (hell["steppe"], hell["huegel"]))
_r, _g, _b = _rgb(farben["nebelsee"])
check("3 Nebelsee ist blau (b liegt deutlich ueber r)", _b > _r + 20, "r=%d b=%d" % (_r, _b))

# ==========================================================================
abschnitt("4. Die sieben Farben liegen auseinander, der Rand ist dunkler")
# ==========================================================================
paare = []
for i, art in enumerate(ARTEN):
    for andere in ARTEN[i + 1:]:
        paare.append((_abstand(_rgb(farben[art]), _rgb(farben[andere])), art, andere))
engste = min(paare)
check("4 je zwei Gelaendefarben liegen mindestens 20 auseinander",
      all(d >= 20 for d, _a, _b in paare),
      "engstes Paar %s/%s bei %.1f" % (engste[1], engste[2], engste[0]))
schlecht = [art for art in ARTEN
            if _helligkeit(_rgb(raender[art])) >= _helligkeit(_rgb(farben[art]))]
check("4 der Rand ist bei jeder Art dunkler als die Flaeche", not schlecht, repr(schlecht))

# ==========================================================================
abschnitt("5. Die Malerei liest die Farben (kein Sonderfall fuer D-5a)")
# ==========================================================================
with open(os.path.join(SRC, "weltkarte_malerei.py"), encoding="utf-8") as f:
    maler = f.read()
check("5 der Maler holt jede Farbe ueber gelaende.farbe",
      maler.count("gelaende.farbe(") >= 7, str(maler.count("gelaende.farbe(")))
check("5 der Maler kennt weiter genau sieben Motive",
      maler.count('"grasland"') + maler.count('"steppe"') + maler.count('"wald"')
      + maler.count('"huegel"') + maler.count('"berg"') + maler.count('"nebelsee"')
      + maler.count('"sumpf"') >= 7, "")

sys.exit(bericht())
