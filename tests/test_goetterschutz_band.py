"""Eingeschraenkter Goetterschutz (belegt, Handbuch 2009, Seite 6, Z. 221-228; Registerpunkt 41).

Belegt sind: bis 299 Punkte gilt grundsaetzlich Schutz; angegriffen werden darf nur, wer im
Bereich "eigene Punktzahl +/- 20 %" liegt; ueber die Grenze 299 hinweg ist KEIN Angriff moeglich,
in keine Richtung. Das Beispiel des Handbuchs (299 darf 240-299 angreifen) ist hier nachgerechnet.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

import_src()
import punkte as P

abschnitt("A. Grenze und Bandbreite sind belegt")
check("Grenze 299 Punkte", P.GOETTERSCHUTZ_PUNKTGRENZE == 299, str(P.GOETTERSCHUTZ_PUNKTGRENZE))
check("Bandbreite 20 Prozent", abs(P.GOETTERSCHUTZ_BANDBREITE - 0.20) < 1e-9,
      str(P.GOETTERSCHUTZ_BANDBREITE))
check("Band bei 299 ist 240 bis 299 (Beispiel des Handbuchs)",
      P.goetterschutz_band(299) == (240, 299), str(P.goetterschutz_band(299)))
check("Band bei 100 ist 80 bis 120", P.goetterschutz_band(100) == (80, 120),
      str(P.goetterschutz_band(100)))
check("Band wird nie ueber 299 hinaus geoeffnet",
      P.goetterschutz_band(299)[1] <= 299 and P.goetterschutz_band(290)[1] <= 299,
      str(P.goetterschutz_band(290)))

abschnitt("B. Das Beispiel des Handbuchs")
check("299 darf 240 angreifen", P.angreifbar(299, 240)[0] is True)
check("299 darf 239 NICHT angreifen", P.angreifbar(299, 239)[0] is False)
check("299 darf 299 angreifen", P.angreifbar(299, 299)[0] is True)
check("100 darf 120 angreifen", P.angreifbar(100, 120)[0] is True)
check("100 darf 121 NICHT angreifen", P.angreifbar(100, 121)[0] is False)
check("100 darf 80 angreifen", P.angreifbar(100, 80)[0] is True)
check("100 darf 79 NICHT angreifen", P.angreifbar(100, 79)[0] is False)

abschnitt("C. Die Grenze 299 darf in KEINE Richtung ueberschritten werden")
check("299 darf 300 nicht angreifen", P.angreifbar(299, 300)[0] is False)
check("300 darf 299 nicht angreifen", P.angreifbar(300, 299)[0] is False)
check("400 darf 100 nicht angreifen", P.angreifbar(400, 100)[0] is False)
check("100 darf 400 nicht angreifen", P.angreifbar(100, 400)[0] is False)

abschnitt("D. Ueber 299 auf beiden Seiten: kein Schutz mehr")
check("400 darf 300 angreifen", P.angreifbar(400, 300)[0] is True)
check("300 darf 1.000 angreifen", P.angreifbar(300, 1000)[0] is True)
check("1.000 darf 300 angreifen", P.angreifbar(1000, 300)[0] is True)

abschnitt("E. Begruendung und robuste Eingaben")
_ok, _grund = P.angreifbar(299, 100)
check("bei Ablehnung nennt die Begruendung den Grund",
      _grund and ("Goetterschutz" in _grund or "ausserhalb" in _grund), _grund)
check("erlaubter Angriff liefert leere Begruendung", P.angreifbar(299, 250) == (True, ""))
check("None-Punkte gelten als 0 und blockieren nicht hart",
      P.angreifbar(None, None)[0] is True, str(P.angreifbar(None, None)))
check("Text statt Zahl wird als 0 gelesen", P.angreifbar("keine Zahl", 0)[0] is True)

befund("Die Regel ist im Code als reine Funktion vorhanden; die VERDRAHTUNG in die "
       "Bot-Angriffsentscheidung (main.py, Zweig 'angreifen') ist noch offen - dort wird "
       "bisher nur das globale Schutz-Flag geprueft.")

bericht()
