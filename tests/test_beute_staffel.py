"""Beute nach Daniels Staffelung (Registerpunkt 45) - VORGABE, Prozentwerte VORSCHLAG.

Geprueft wird die reine Rechenfunktion `kampfbericht.beute_staffel`:
  * Wall heil            -> 10 % (erster Angriff reisst die Mauer ein, wenig Beute)
  * Wall beschaedigt     -> 30 %
  * Wall gebrochen (0 %) -> 60 %
  * keine Verteidiger    -> 100 % des Bestands
und in JEDEM Fall: nie mehr als die Karrenladung, nie mehr als der Vorrat,
ohne Karren gar keine Beute (belegt: nur Transportkarren pluendern, Handbuch S. 23).
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

import_src()
import kampfbericht as KB
import einheiten as E

abschnitt("A. Die vier Lagen und ihre Anteile")
check("Wall heil heisst 'mauer_heil'", KB.beute_lage(100.0, 5) == "mauer_heil",
      KB.beute_lage(100.0, 5))
check("Wall leicht beschaedigt heisst 'mauer_beschaedigt'",
      KB.beute_lage(99.0, 5) == "mauer_beschaedigt", KB.beute_lage(99.0, 5))
check("Wall bei 50 Prozent heisst 'mauer_beschaedigt'",
      KB.beute_lage(50.0, 5) == "mauer_beschaedigt", KB.beute_lage(50.0, 5))
check("Wall bei 0 Prozent heisst 'mauer_gebrochen'",
      KB.beute_lage(0.0, 5) == "mauer_gebrochen", KB.beute_lage(0.0, 5))
check("keine Verteidiger schlaegt jeden Wallzustand",
      KB.beute_lage(100.0, 0) == "keine_verteidiger", KB.beute_lage(100.0, 0))
check("unbekannte Angaben gelten als 'mauer_heil' (vorsichtigster Fall)",
      KB.beute_lage(None, None) == "mauer_heil", KB.beute_lage(None, None))
check("Anteile: 10 / 30 / 60 / 100 Prozent",
      KB.BEUTE_STAFFEL_PROZENT == {"mauer_heil": 10, "mauer_beschaedigt": 30,
                                   "mauer_gebrochen": 60, "keine_verteidiger": 100},
      str(KB.BEUTE_STAFFEL_PROZENT))

abschnitt("B. Rechnung: Ladung, Vorrat und Anteil greifen nacheinander")
LAGER = {"holz": 1000, "stein": 1000, "gold": 1000}          # 3000 gesamt
KARREN = {"Handkarren": 10}                                   # Ladung 10 * 40 = 400

_b_heil = KB.beute_staffel(KARREN, LAGER, wall_zustand_vor=100.0, verteidiger_uebrig=4)
check("Wall heil: Anteil 10 Prozent = 300, passt in 400 Ladeplatz -> 300",
      sum(_b_heil.values()) == 300, str(_b_heil))
check("Wall heil: je Rohstoff ein Drittel des Anteils (100)",
      _b_heil.get("holz") == 100 and _b_heil.get("stein") == 100, str(_b_heil))

_b_besch = KB.beute_staffel(KARREN, LAGER, wall_zustand_vor=40.0, verteidiger_uebrig=2)
check("Wall beschaedigt: 30 Prozent = 900, aber nur 400 Ladeplatz -> 400",
      sum(_b_besch.values()) == 400, str(_b_besch))

_b_gebr = KB.beute_staffel({"Einspänner": 10}, LAGER, wall_zustand_vor=0.0, verteidiger_uebrig=1)
check("Wall gebrochen mit 1.000 Ladeplatz: 60 Prozent = 1.800 -> nur 1.000 passen",
      sum(_b_gebr.values()) == 1000, str(_b_gebr))

_b_frei = KB.beute_staffel({"Zweispänner": 20}, LAGER, wall_zustand_vor=100.0, verteidiger_uebrig=0)
check("keine Verteidiger, 5.000 Ladeplatz: ganzer Bestand (3.000) darf mit",
      sum(_b_frei.values()) == 3000, str(_b_frei))

abschnitt("C. Harte Grenzen (belegt)")
check("ohne Karren keine Beute (nur Transportkarren pluendern)",
      KB.beute_staffel({"Bürgerwehr": 20}, LAGER, 100.0, 3) == {})
check("leeres Lager ergibt keine Beute",
      KB.beute_staffel(KARREN, {}, 100.0, 3) == {})
check("Beute ueberschreitet nie den Vorrat je Rohstoff",
      all(v <= LAGER[k] for k, v in _b_frei.items()), str(_b_frei))
check("Beute ueberschreitet nie die Karrenladung",
      all(sum(x.values()) <= 400 for x in (_b_heil, _b_besch)), "heil/beschaedigt")
check("negative oder unsinnige Mengen werden ignoriert",
      KB.beute_staffel(KARREN, {"holz": -50, "stein": 0}, 100.0, 3) == {})

abschnitt("D. Abwaertskompatibel: beute() bleibt unveraendert (alte Regel)")
_alt = KB.beute(KARREN, LAGER)
check("beute() nimmt weiterhin nur die Ladung, anteilig je Rohstoff (je 133 von 400)",
      _alt == {"gold": 133, "holz": 133, "stein": 133}, str(_alt))

befund("Die Prozentwerte der Staffelung sind VORSCHLAG (Vorgabe Daniel 31.10.2026, "
       "Registerpunkt 45) und werden im Spieltest balanciert; belegt ist nur "
       "'nur Transportkarren pluendern' und 'Ladung begrenzt' (Handbuch S. 23).")
bericht()
