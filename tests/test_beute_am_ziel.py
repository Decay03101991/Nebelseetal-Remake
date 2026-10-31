"""Pruefung von `kampfbericht.beute_am_ziel` - Beute rechnen UND beim Ziel abbuchen.

Hintergrund: Die externe Gegenpruefung vom 31.10.2026 (Befund Nr. 6) hat einen echten Fehler
gefunden - der Auftrags-Pfad schrieb die Beute dem Spieler gut, ohne sie beim Ziel abzuziehen.
Der Bot-Pfad zog ab, rechnete aber mit einer anderen Formel (`kampf._beute`: nur Ladungsgrenze).
Seit dem Umbau gilt an EINER Stelle:

  * Beute nur bei Angreifersieg (Handbuch S. 23, Z. 1307-1315),
  * Anteil aus `beute_staffel` (Registerpunkt 45, Werte VORSCHLAG),
  * was der Sieger bekommt, fehlt beim Ziel - und kein Bestand wird negativ.

Reine Logik: kein Fenster, keine Uhr, keine Datei.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, befund, check, import_src

ROOT, SRC = import_src()
import kampfbericht as KB


def _lager():
    return {"holz": 1000.0, "stein": 1000.0, "nahrung": 1000.0}


# ==========================================================================
abschnitt("1. Beute nur bei Angreifersieg")

_lager_vor = _lager()
_beute, _nach = KB.beute_am_ziel({"Handkarren": 10}, _lager_vor, ausgang="verteidiger",
                                 wall_zustand_vor=100.0, verteidiger_uebrig=5)
check("bei einer Niederlage gibt es keine Beute", _beute == {}, str(_beute))
check("bei einer Niederlage bleibt das Lager unveraendert",
      _nach == _lager_vor, str(_nach))

_beute, _nach = KB.beute_am_ziel({"Handkarren": 10}, _lager_vor, ausgang="unentschieden",
                                 wall_zustand_vor=100.0, verteidiger_uebrig=5)
check("auch 'unentschieden' bringt keine Beute", _beute == {}, str(_beute))


# ==========================================================================
abschnitt("2. Was gutgeschrieben wird, fehlt beim Ziel")

_beute, _nach = KB.beute_am_ziel({"Handkarren": 10}, _lager(), ausgang="angreifer",
                                 wall_zustand_vor=100.0, verteidiger_uebrig=5)
check("der Sieg gegen einen heilen Wall bringt Beute", sum(_beute.values()) > 0, str(_beute))
check("die Abnahme beim Ziel entspricht genau der Beute",
      sum(_lager().values()) - sum(_nach.values()) == sum(_beute.values()),
      f"{sum(_lager().values()) - sum(_nach.values())} gegen {sum(_beute.values())}")
check("jeder einzelne Rohstoff ist abgebucht",
      all(round(_nach[s], 2) == round(1000.0 - _beute.get(s, 0), 2) for s in _lager()),
      str(_nach))
check("kein Bestand wird negativ", all(v >= 0 for v in _nach.values()), str(_nach))


# ==========================================================================
abschnitt("3. Staffelung nach Wallzustand (Registerpunkt 45, Werte VORSCHLAG)")

_heil, _ = KB.beute_am_ziel({"Handkarren": 10}, _lager(), ausgang="angreifer",
                            wall_zustand_vor=100.0, verteidiger_uebrig=5)
_beschaedigt, _ = KB.beute_am_ziel({"Handkarren": 10}, _lager(), ausgang="angreifer",
                                   wall_zustand_vor=50.0, verteidiger_uebrig=5)
_gebrochen, _ = KB.beute_am_ziel({"Handkarren": 10}, _lager(), ausgang="angreifer",
                                 wall_zustand_vor=0.0, verteidiger_uebrig=5)
_ohne_verteidiger, _ = KB.beute_am_ziel({"Handkarren": 10}, _lager(), ausgang="angreifer",
                                        wall_zustand_vor=100.0, verteidiger_uebrig=0)
check("heil = 10 Prozent von 3.000 = 300", sum(_heil.values()) == 300, str(_heil))
check("beschaedigt = 30 Prozent, aber durch die Ladung (400) begrenzt",
      sum(_beschaedigt.values()) == 400, str(_beschaedigt))
check("gebrochen = 60 Prozent, ebenfalls ladungsbegrenzt",
      sum(_gebrochen.values()) == 400, str(_gebrochen))
check("ohne Verteidiger darf alles mit, ladungsbegrenzt",
      sum(_ohne_verteidiger.values()) == 400, str(_ohne_verteidiger))
check("die Staffel ist monoton: heil <= beschaedigt <= gebrochen <= ohne Verteidiger",
      sum(_heil.values()) <= sum(_beschaedigt.values()) <= sum(_gebrochen.values())
      <= sum(_ohne_verteidiger.values()),
      f"{sum(_heil.values())}/{sum(_beschaedigt.values())}/{sum(_gebrochen.values())}/"
      f"{sum(_ohne_verteidiger.values())}")


# ==========================================================================
abschnitt("4. Grenzen: Karrenladung und vorhandener Vorrat")

_beute, _nach = KB.beute_am_ziel({"Handkarren": 1}, _lager(), ausgang="angreifer",
                                 wall_zustand_vor=0.0, verteidiger_uebrig=7)
check("mehr als die Ladung (40) geht nicht in einen Handkarren",
      sum(_beute.values()) <= 40, str(sum(_beute.values())))

_beute, _nach = KB.beute_am_ziel({"Handkarren": 10}, {"holz": 5.0}, ausgang="angreifer",
                                 wall_zustand_vor=0.0, verteidiger_uebrig=7)
check("mehr als der Vorrat geht nicht", sum(_beute.values()) <= 5, str(_beute))
check("bei gebrochenem Wall sind es 60 Prozent von 5 = 3", _beute == {"holz": 3}, str(_beute))
check("der Rest bleibt liegen, nichts wird negativ", _nach.get("holz") == 2.0, str(_nach))

_beute, _nach = KB.beute_am_ziel({"Handkarren": 10}, {"holz": 5.0}, ausgang="angreifer",
                                 wall_zustand_vor=100.0, verteidiger_uebrig=0)
check("ohne Verteidiger geht der ganze Vorrat mit, wenn er in die Karren passt",
      _beute == {"holz": 5}, str(_beute))
check("ein leerer Bestand wird zu 0, nicht negativ", _nach.get("holz") == 0.0, str(_nach))

_beute, _nach = KB.beute_am_ziel({}, _lager(), ausgang="angreifer",
                                 wall_zustand_vor=0.0, verteidiger_uebrig=0)
check("ohne Karren gibt es keine Beute (belegt)", _beute == {}, str(_beute))
check("ohne Karren bleibt das Lager voll", _nach == _lager(), str(_nach))

_beute, _nach = KB.beute_am_ziel({"Handkarren": 10}, {}, ausgang="angreifer",
                                 wall_zustand_vor=100.0, verteidiger_uebrig=3)
check("ein leeres Ziel bringt keine Beute", _beute == {}, str(_beute))


# ==========================================================================
abschnitt("5. Robustheit")

_beute, _nach = KB.beute_am_ziel({"Handkarren": 10}, {"holz": None, "stein": "kaputt"},
                                 ausgang="angreifer", wall_zustand_vor=100.0,
                                 verteidiger_uebrig=3)
check("unbrauchbare Vorratsangaben werden zu 0 statt zu einem Absturz",
      _beute == {}, str(_beute))

_beute, _nach = KB.beute_am_ziel({"Handkarren": 10}, _lager(), ausgang=None,
                                 wall_zustand_vor=None, verteidiger_uebrig=None)
check("ohne Ausgang gibt es keine Beute", _beute == {}, str(_beute))
check("unbekannter Wallzustand gilt als heil (vorsichtigster Fall)",
      KB.beute_lage(None, None) == "mauer_heil", KB.beute_lage(None, None))

sys.exit(bericht())
