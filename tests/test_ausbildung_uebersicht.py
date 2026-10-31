"""Pruefung der Ausbildungs-Uebersicht und des Streichens (Daniels Spieltest 31.10.2026).

Damit ist die Frage beantwortet, ob die Auftraege wirklich NACHEINANDER laufen und wie lange
die ganze Schlange dauert - bisher war das nirgends sichtbar. Reine Logik, keine Uhr, kein Fenster.

Zu den Quellen: Das Handbuch 2009 kennt nur "Forschung abbrechen" (Z. 442). Fuer Ausbildung
nennt weder Handbuch 2009 noch Vorversion 2006 eine Regel zu Abbruch oder Erstattung - deshalb
streichen OHNE Erstattung, und das steht so im Docstring des Kerns.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, befund, check, import_src

ROOT, SRC = import_src()
import spieloekonomie as O


def _ort(auftraege):
    return {"ausbildung": auftraege}


def _auftrag(einheit, gebaeude, start, ende, stufe=1, gebucht=False):
    return {"einheit": einheit, "gebaeude": gebaeude, "start": start, "ende": ende,
            "dauer_sekunden": ende - start, "stufe": stufe, "gebucht": gebucht}


# ==========================================================================
abschnitt("1. Die Warteschlange laeuft nacheinander (kein Parallelbetrieb)")

_ort1 = _ort([_auftrag("Handkarren", "stellmacher", 0, 1200),
              _auftrag("Handkarren", "stellmacher", 1200, 2400)])
_u1 = O.ausbildung_uebersicht(_ort1, 0)
check("zwei Auftraege stehen in der Uebersicht", _u1["anzahl"] == 2, str(_u1["anzahl"]))
check("der zweite beginnt GENAU am Ende des ersten (sequenziell)",
      _u1["auftraege"][1]["start"] == _u1["auftraege"][0]["ende"],
      f"{_u1['auftraege'][1]['start']} gegen {_u1['auftraege'][0]['ende']}")
check("keine Ueberlappung: Start2 >= Ende1",
      _u1["auftraege"][1]["start"] >= _u1["auftraege"][0]["ende"])
check("die Gesamtdauer ist das Ende des LETZTEN Auftrags",
      _u1["gesamt_rest_sekunden"] == 2400, str(_u1["gesamt_rest_sekunden"]))
check("der erste Auftrag laeuft, der zweite wartet",
      _u1["auftraege"][0]["laufend"] is True and _u1["auftraege"][1]["laufend"] is False)
check("die Plaetze sind fortlaufend numeriert",
      [a["platz"] for a in _u1["auftraege"]] == [1, 2],
      str([a["platz"] for a in _u1["auftraege"]]))

_u2 = O.ausbildung_uebersicht(_ort1, 1200)
check("nach dem ersten Auftrag ist der zweite der laufende",
      _u2["auftraege"][1]["laufend"] is True and _u2["auftraege"][0]["laufend"] is False)
check("die Restzeit des zweiten ist dann eine volle Dauer",
      _u2["auftraege"][1]["rest_sekunden"] == 1200, str(_u2["auftraege"][1]["rest_sekunden"]))
check("die Restzeit wird nie negativ",
      O.ausbildung_uebersicht(_ort1, 99_999)["gesamt_rest_sekunden"] == 0.0)


# ==========================================================================
abschnitt("2. Leere und gebuchte Eintraege")

_leer = O.ausbildung_uebersicht(_ort([]), 0)
check("leere Schlange ergibt 0 Auftraege", _leer["anzahl"] == 0)
check("leere Schlange ergibt 0 Restzeit", _leer["gesamt_rest_sekunden"] == 0.0)
_gebucht = O.ausbildung_uebersicht(_ort([_auftrag("Handkarren", "stellmacher", 0, 600, gebucht=True)]), 0)
check("bereits gebuchte Auftraege zaehlen nicht mehr", _gebucht["anzahl"] == 0)
_schief = O.ausbildung_uebersicht(_ort([{"einheit": "X", "ende": "kaputt"}]), 0)
check("unbrauchbare Eintraege werden uebersprungen, kein Absturz", _schief["anzahl"] == 0)


# ==========================================================================
abschnitt("3. Streichen: nur wartende Auftraege, ohne Erstattung")

_ort3 = _ort([_auftrag("Handkarren", "stellmacher", 0, 1200),
              _auftrag("Handkarren", "stellmacher", 1200, 2400)])
_laufend = O.ausbildung_abbrechen(_ort3, 1, 100)
check("ein LAUFENDER Auftrag laesst sich nicht streichen", _laufend["ok"] is False,
      str(_laufend.get("grund")))
check("der Grund nennt 'laeuft gerade'", "laeuft gerade" in _laufend.get("grund", ""),
      _laufend.get("grund"))
_wartend = O.ausbildung_abbrechen(_ort3, 2, 100)
check("ein WARTENDER Auftrag laesst sich streichen", _wartend["ok"] is True, str(_wartend))
check("gestrichen wird der richtige Auftrag (Platz 2 = der zweite)",
      _wartend["einheit"] == "Handkarren")
check("danach steht nur noch ein Auftrag in der Schlange", len(_wartend["ausbildung"]) == 1)
check("es gibt KEINE Erstattung (die Quellen regeln das nicht)",
      _wartend["erstattung"] == {}, str(_wartend["erstattung"]))
check("der Hinweis sagt das ausdruecklich", "Keine Erstattung" in _wartend["hinweis"],
      _wartend["hinweis"])
check("ein ungueltiger Platz wird abgelehnt", O.ausbildung_abbrechen(_ort3, 5, 100)["ok"] is False)
check("Platz 0 wird abgelehnt", O.ausbildung_abbrechen(_ort3, 0, 100)["ok"] is False)

befund("Streichen ohne Erstattung ist eine Auslegung, keine Originalregel",
       "belegt ist nur 'Forschung abbrechen' (Handbuch 2009, Z. 442); fuer Ausbildung schweigen "
       "beide Fassungen - deshalb streichen ja, erstatten nein")

sys.exit(bericht())
