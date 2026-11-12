# -*- coding: ascii -*-
"""Spielertexte tragen keine internen Kennzeichnungen (Befund C-6 der externen Pruefung).

DER BEFUND (dritte Modellrunde 07.11.2026, bestaetigt, Register 311): `punkte.spielausgang` gab dem
Spieler den Satz "VORSCHLAG: keine Siedlung und keine Einheit mehr ...". "VORSCHLAG" ist eine
Kennzeichnung fuer uns (nicht belegt, gesetzt) - auf dem Bildschirm hat sie nichts zu suchen. Der
Grund gehoert in den Kommentar, der Satz zum Spieler.

Aufruf:  python -X utf8 tests/test_spielertexte.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['berater', 'einheiten', 'punkte']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import punkte  # noqa: E402

abschnitt("1. Der Niederlage-Text ist ein Spielertext")
_art, _text = punkte.spielausgang({"siedlungen": [], "einheiten": {}})
check("der Ausgang ist 'niederlage'", _art == "niederlage", str(_art))
check("der Text beginnt NICHT mit einer internen Kennzeichnung",
      not _text.upper().startswith("VORSCHLAG"), _text)
_klein = _text.lower()
check("der Text nennt den Grund in Spielersprache",
      "keine siedlung" in _klein and "keine einheit" in _klein, _text)
check("der Text nennt das Handbuch als Grundlage der Setzung",
      "Handbuch" in _text, _text)

abschnitt("2. Auch der Sieg-Text bleibt saubere Spielersprache")
_art2, _text2 = punkte.spielausgang({"siedlungen": [{"name": "A"}], "einheiten": {}})
check("mit Siedlung ist der Ausgang 'weiter'", _art2 == "weiter", str(_art2))
check("auch dieser Text traegt keine Kennzeichnung",
      not _text2.upper().startswith("VORSCHLAG"), _text2)

befund("Nicht geaendert und offen: `berater.py` zeigt beim Baupreis weiter den Zusatz "
       "'VORSCHLAG - fuer dieses Gebaeude nennt keine Quelle einen Preis'. Das ist dieselbe Klasse "
       "(interne Kennzeichnung in einem Spielertext), aber die Aussage ist dort inhaltlich wichtig; "
       "eine Umformulierung ist eine Textentscheidung und steht in der Uebergabe.", "")
sys.exit(bericht())
