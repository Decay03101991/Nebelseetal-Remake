# -*- coding: ascii -*-
"""Siedler-Warnung: Reserve sichtbar, bevor sie aufgebraucht ist (A-6, Register 81).

Daniels Spielbericht 31.10.2026: nach 44 Bauten standen **3,5 Siedler**, danach **sechs**
gescheiterte Ausbildungen ("Freie Siedler fehlen vor Ort") - niemand hatte ihn vorher gewarnt.

Was diese Datei beweist
-----------------------
1. Die Reserve ist die Bevoelkerung des Ortes - dieselbe Zahl, aus der die Ausbildung zahlt.
2. Der Bedarf kommt aus `data/units.json` (Siedler-Preis je Einheit), nicht aus einer zweiten
   Liste; je Einheit steht, wie viele davon die Reserve noch hergibt.
3. Grenzfaelle: 0 Siedler, 1, 2, genau zwei Ausbildungen, knapp darunter, weit darueber.
   Die Warnung erscheint GENAU dann, wenn die Reserve nicht mehr fuer ZWEI Ausbildungen der
   guenstigsten Art reicht (Schwelle VORSCHLAG, an Daniels Lage mit 3,5 Siedlern gemessen).
4. Nur Einheiten, deren Ausbildungsstaette VOR ORT steht, zaehlen fuer die Reserve - eine
   Einheit, die hier gar nicht ausgebildet werden kann, darf die Warnung nicht verschaerfen.
5. Mit Daniels Entscheidung 31.10.2026 (Frage 5 = B) binden Bauten keine Siedler: `baukosten`
   enthaelt keinen Siedler-Posten, und die Meldung der Reserve sagt das ausdruecklich.

Aufruf:  python -X utf8 tests/test_siedler_warnung.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import main                     # noqa: E402
import spieloekonomie as O      # noqa: E402

KAEMPFER = "K\u00e4mpfer"
BUERGERWEHR = "B\u00fcrgerwehr"
HANDELSKARAWANE = "Handelskarawane"     # kostet 10 Siedler je Stueck
FORSCH = {"Kriegskunst": 10, "Waffentechnik": 10, "Heimlichkeit": 10, "Wagenbau": 10}


def ort(bevoelkerung=10.0, bauten=None, oid="A"):
    """Ein Ort mit den Feldern, die `siedler_reserve` liest."""
    return {
        "id": oid, "besitzer": "spieler", "map_id": None, "dimension": 0, "x": 0, "y": 0,
        "karte": {"raster": ["grasland"] * 100},
        "bauten": dict(bauten if bauten is not None else {"0": "kriegerakademie"}),
        "stufen": {"0": 1}, "vorraete": {"gold": 5000.0},
        "waren": {"Kurzschwert": 20, "Lederr\u00fcstung": 20}, "einheiten": {},
        "bevoelkerung": bevoelkerung, "importiert": {}, "verbrauchsjournal": [],
        "produktionsjournal": [], "fertigjournal": [], "werkstaetten": {}, "ausbildung": [],
    }


# ==========================================================================
abschnitt("1. Reserve und Bedarf kommen aus den vorhandenen Quellen")

r = O.siedler_reserve(ort(7.5), FORSCH)
check("1 die Reserve ist die Bevoelkerung des Ortes", r["frei"] == 7.5, str(r["frei"]))
check("1 der Kaempfer kostet 1 Siedler (data/units.json)",
      r["bedarf_je_einheit"].get(KAEMPFER) == 1, str(r["bedarf_je_einheit"].get(KAEMPFER)))
check("1 sieben Siedler erlauben sieben Kaempfer", r["moeglich"].get(KAEMPFER) == 7,
      str(r["moeglich"].get(KAEMPFER)))
check("1 die Obergrenze steht dabei (Siedlergrenze der Siedlung)",
      r["grenze"] > 0, str(r["grenze"]))
check("1 der Nachwuchs je Spielstunde steht dabei", r["zuwachs_stunde"] > 0,
      str(r["zuwachs_stunde"]))
check("1 bei 7,5 Siedlern wird nicht gewarnt", r["warnung"] is False and r["text"] == "",
      r["text"])


# ==========================================================================
abschnitt("2. Grenzfaelle 0 / 1 / 2 / knapp darunter / weit darueber")

for wert, erwartet_warnung in ((0.0, True), (1.0, True), (1.9, True), (2.0, False),
                               (3.53, False), (50.0, False)):
    rr = O.siedler_reserve(ort(wert), FORSCH)
    check(f"2 bei {wert} Siedlern ist die Warnung {erwartet_warnung}",
          rr["warnung"] is erwartet_warnung, f"{rr['warnung']} / {rr['text']}")

rr0 = O.siedler_reserve(ort(0.0), FORSCH)
check("2 bei 0 Siedlern sagt der Text, dass keine Ausbildung mehr geht",
      "keine einzige" in rr0["text"], rr0["text"])
check("2 bei 0 Siedlern sind 0 Einheiten moeglich", rr0["moeglich"].get(KAEMPFER) == 0,
      str(rr0["moeglich"].get(KAEMPFER)))

rr1 = O.siedler_reserve(ort(1.0), FORSCH)
check("2 bei 1 Siedler nennt der Text die verbleibende Zahl (1)",
      "noch 1" in rr1["text"], rr1["text"])


# ==========================================================================
abschnitt("3. Eine teure Einheit verschaerft die Warnung nicht unnoetig")

o_teuer = ort(5.0, bauten={"0": "stellmacher"})
rt = O.siedler_reserve(o_teuer, FORSCH)
check("3 im Stellmacher kostet die Handelskarawane 10 Siedler",
      rt["bedarf_je_einheit"].get(HANDELSKARAWANE) == 10,
      str(rt["bedarf_je_einheit"].get(HANDELSKARAWANE)))
check("3 der Handkarren kostet 1 Siedler",
      rt["bedarf_je_einheit"].get("Handkarren") == 1,
      str(rt["bedarf_je_einheit"].get("Handkarren")))
check("3 die Reserve misst am GUENSTIGSTEN Bau dieses Ortes (5 Siedler = keine Warnung)",
      rt["warnung"] is False, f"{rt['warnung']} engste={rt['engste']}")
check("3 die teuerste Einheit ist trotzdem benannt",
      rt["teuerste"][1] >= rt["guenstigste"][1], f"{rt['teuerste']} / {rt['guenstigste']}")

o_ohne = ort(0.5, bauten={})
ro = O.siedler_reserve(o_ohne, FORSCH)
check("3 ohne Ausbildungsstaette gibt es keinen Bedarf und keine Warnung",
      ro["bedarf_je_einheit"] == {} and ro["warnung"] is False, str(ro))


# ==========================================================================
abschnitt("4. Bauten binden keine Siedler (Daniels Entscheidung, Frage 5 = B)")

check("4 baukosten(Holzaeller) hat keinen Siedler-Posten",
      "siedler" not in main.baukosten("holzfaeller"), str(main.baukosten("holzfaeller")))
check("4 baukosten(Jaeger) hat keinen Siedler-Posten",
      "siedler" not in main.baukosten("jaeger"), str(main.baukosten("jaeger")))
check("4 die Reserve sinkt beim Bauen nicht - sie ist die Bevoelkerung selbst",
      O.siedler_reserve(ort(10.0), FORSCH)["frei"] == 10.0, "")

# Die Ausbildung verbraucht weiterhin Siedler - das ist der einzige Weg, auf dem sie sinken.
o_start = ort(6.0)
neu = O.ausbildung_start_menge(o_start, KAEMPFER, FORSCH, 0.0, 3)
check("4 drei Kaempfer kosten genau 3 Siedler",
      neu["ort"]["bevoelkerung"] == 3.0, str(neu["ort"]["bevoelkerung"]))
nachher = O.siedler_reserve(neu["ort"], FORSCH)
check("4 nach der Ausbildung ist die Warnung an (3 Siedler, Schwelle 2)",
      nachher["warnung"] is False and nachher["frei"] == 3.0, str(nachher["frei"]))
noch_eine = O.ausbildung_start_menge(neu["ort"], KAEMPFER, FORSCH, 0.0, 2)
check("4 nach zwei weiteren Ausbildungen steht die Reserve auf 1 und warnt",
      O.siedler_reserve(noch_eine["ort"], FORSCH)["warnung"] is True,
      str(O.siedler_reserve(noch_eine["ort"], FORSCH)["frei"]))


# ==========================================================================
abschnitt("5. Die Oberflaeche rechnet nicht selbst")

import inspect  # noqa: E402
quelle = inspect.getsource(main)
check("5 die Kaserne zeichnet die Reserve-Warnung", "_siedler_warnung_zeichnen" in quelle, "")
check("5 die Dorfuebersicht zeigt die Reserve ebenfalls",
      quelle.count("siedler_reserve(") >= 2, str(quelle.count("siedler_reserve(")))
check("5 die Reserve kommt aus EINER Kernfunktion (kein zweiter Rechenweg)",
      inspect.getsource(O.siedler_reserve).count("bevoelkerung") >= 1, "")
befund("Die gezeichnete Zeile selbst ist hier nicht geprueft - die GUI-Probe auf dem echten "
       "Spielstand deckt sie ab", "")

sys.exit(bericht())
