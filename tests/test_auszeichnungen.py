"""Pruefung der Auszeichnungen (E5) statt eines Sieges - Paket A3 vom 31.10.2026.

Der Sieg ist weg (Register 50). Was bleibt, ist eine BEWERTUNG ueber Kennzahlen, die aus den
belegten Originalformeln kommen:

  Feldherr        Kriegspunkte        Handbuch 2009, S. 5
  Forscher        Forschungspunkte    Handbuch 2009, S. 4
  Haendler        Handelspunkte       NUR Vorversion 2006 (ZUSAMMENFUEHRUNG)
  Gesamtherrscher Gesamtpunkte        Handbuch 2009, S. 5/6

Reine Logik: kein Fenster, keine Uhr, keine Datei. Die Zeit wird uebergeben.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, befund, check, import_src

ROOT, SRC = import_src()
import punkte as P

_STUNDE = 3600


# ==========================================================================
abschnitt("1. Handelspunkte (Vorversion 2006, ZUSAMMENFUEHRUNG)")

check("300 Gold ergeben 3 Handelspunkte (Beispiel der Quelle)",
      P.handelspunkte(300) == 3.0, str(P.handelspunkte(300)))
check("kleine Betraege zaehlen anteilig: 20 Gold = 0,2 Punkte (Beispiel der Quelle)",
      P.handelspunkte(20) == 0.2, str(P.handelspunkte(20)))
check("ohne Erloes gibt es keine Punkte", P.handelspunkte(0) == 0.0)
check("Unsinn ergibt 0 statt Absturz", P.handelspunkte("kaputt") == 0.0)
check("Verfall nach 24 Stunden ohne Handel: ein Punkt weniger",
      P.handelspunkte(300, letzter_handel=0, jetzt=24 * _STUNDE) == 2.0,
      str(P.handelspunkte(300, letzter_handel=0, jetzt=24 * _STUNDE)))
check("nach 3 Tagen ist alles verfallen, aber nie negativ",
      P.handelspunkte(300, letzter_handel=0, jetzt=72 * _STUNDE) == 0.0,
      str(P.handelspunkte(300, letzter_handel=0, jetzt=72 * _STUNDE)))
check("kurz vor Ablauf der 24 Stunden verfaellt noch nichts",
      P.handelspunkte(300, letzter_handel=0, jetzt=23 * _STUNDE) == 3.0)
check("ohne bekannten letzten Handel verfaellt nichts",
      P.handelspunkte(300, letzter_handel=None, jetzt=999 * _STUNDE) == 3.0)


# ==========================================================================
abschnitt("2. Vier Auszeichnungen, Kennzahlen aus den belegten Formeln")

_zustand = {
    "forschungsstaende": {"Holzwirtschaft": 2, "Bogenbau": 1},
    "einheiten": {"Kämpfer": 4, "Ritter": 2},
    "wall_stufe": 3,
    "gold_erloes": 450,
    "letzter_handel": 0,
    "jetzt": 0,
}
_aus = P.auszeichnungen(_zustand)
check("es sind vier Auszeichnungen", len(_aus) == 4, str(len(_aus)))
check("die Namen folgen den drei Spielzielen plus Gesamt (A3)",
      [a["name"] for a in _aus] == ["Feldherr", "Forscher", "Haendler", "Gesamtherrscher"],
      str([a["name"] for a in _aus]))
check("jeder Eintrag nennt Kennzahl, Wert, Rechenweg und Status",
      all(all(k in a for k in ("name", "kennzahl", "wert", "rechenweg", "status")) for a in _aus))

_krieg = P.kriegspunkte({"Kämpfer": 4, "Ritter": 2}, 3)
_forschung = P.forschungspunkte({"Holzwirtschaft": 2, "Bogenbau": 1})
check("Feldherr = Kriegspunkte der belegten Formel", _aus[0]["wert"] == _krieg,
      f"{_aus[0]['wert']} gegen {_krieg}")
check("Forscher = Forschungspunkte der belegten Formel", _aus[1]["wert"] == _forschung,
      f"{_aus[1]['wert']} gegen {_forschung}")
check("Gesamtherrscher = (Krieg + Forschung) // 2 (abgerundet)",
      _aus[3]["wert"] == (_krieg + _forschung) // 2,
      f"{_aus[3]['wert']} gegen {(_krieg + _forschung) // 2}")
check("Haendler = Handelspunkte aus dem Golderloes", _aus[2]["wert"] == 4.5,
      str(_aus[2]["wert"]))
check("die Handelsauszeichnung ist als ZUSAMMENFUEHRUNG gekennzeichnet (nur 2006 belegt)",
      _aus[2]["status"] == "ZUSAMMENFUEHRUNG", _aus[2]["status"])
check("Feldherr, Forscher und Gesamt sind als BELEGT gefuehrt",
      all(a["status"] == "BELEGT" for a in (_aus[0], _aus[1], _aus[3])),
      str([a["status"] for a in (_aus[0], _aus[1], _aus[3])]))
check("die Handelspunkte fliessen NICHT in die Gesamtpunkte (Handbuch 2009 kennt nur zwei Arten)",
      _aus[3]["wert"] == (_aus[0]["wert"] + _aus[1]["wert"]) // 2)
check("leerer Zustand ergibt vier Auszeichnungen mit 0",
      [a["wert"] for a in P.auszeichnungen({})] == [0, 0, 0.0, 0],
      str([a["wert"] for a in P.auszeichnungen({})]))
check("ein Wörterbuch 'forschung' statt 'forschungsstaende' wird ebenfalls gelesen",
      P.auszeichnungen({"forschung": {"Holzwirtschaft": 2}})[1]["wert"] == 8,
      str(P.auszeichnungen({"forschung": {"Holzwirtschaft": 2}})[1]["wert"]))
check("die Auszeichnung ist KEIN Sieg: spielausgang bleibt bei 'weiter'",
      P.spielausgang({"siedlungen": [{"name": "S"}], "einheiten": {"Kämpfer": 1},
                      "punkte": 99999})[0] == "weiter")

befund("Auszeichnungsnamen sind VORSCHLAG, Kennzahlen belegt",
       "Feldherr/Forscher/Haendler/Gesamtherrscher sind Namen aus Paket A3; die Rechenwege "
       "stehen in punkte.belegte_formeln() bzw. in der 2006er Quelle (Handelspunkte)")

sys.exit(bericht())
