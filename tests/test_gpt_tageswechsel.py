# -*- coding: utf-8 -*-
"""Unabhaengige Regression: Tagesgrenzen und Goetterschutz bei grossen Zeitspruengen.

Neue Datei, keine Aenderung am Hauptcode. Verwendet den originalen tests/harness.py.

    python -X utf8 tests/test_gpt_tageswechsel.py
    python -X utf8 tests/test_gpt_tageswechsel.py --strict

Standard: bereits bekannte Abweichungen als BEFUND (nicht als scheinbar gruenen Test).
--strict: Abweichungen als FEHLER; erst nach Hermes' Reparatur gruen zu erwarten.
Quelle: src/main.py, GameState.tick; Handbuch Götterschutz / Projektregel 7 Tage.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Wie die Projekt-Pruefdateien: tests/harness.py, src/main.py
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import abschnitt, befund, bericht, check, import_src  # noqa: E402

import_src()
import main as M  # noqa: E402

STRICT = "--strict" in sys.argv[1:]
SEK_TAG = 86400.0


def neuer_stand():
    """Nicht die GUI starten; keine Orte oder Bots als Nebeneffekte."""
    stand = M.GameState()
    stand.settlements = []
    stand.bots = []
    return stand


def erwartung(name, ok, erwartet, beobachtet):
    detail = f"erwartet={erwartet!r}, ist={beobachtet!r}"
    if ok or STRICT:
        check(name, ok, detail)
    else:
        befund(name, detail)


abschnitt("GPT-001: Tageswechsel und Restzeit, unabhaengige Uhrwache")

for titel, delta, tage, rest in (
    ("Nullschritt", 0.0, 1, 0.0),
    ("1 voller Tag", SEK_TAG, 2, 0.0),
    ("1.5 Tage", 1.5 * SEK_TAG, 2, 0.5 * SEK_TAG),
    ("2 volle Tage in einem Tick", 2 * SEK_TAG, 3, 0.0),
    ("3 Tage + 2 Stunden in einem Tick", 3 * SEK_TAG + 7200, 4, 7200.0),
):
    st = neuer_stand()
    st.tick(delta)
    check(titel + ": Spielsekunden korrekt", abs(st.spielsekunden - delta) < 1e-7,
          f"erwartet={delta}, ist={st.spielsekunden}")
    erwartung(titel + ": Kalendertag", st.day == tage, tage, st.day)
    erwartung(titel + ": Tagesrest", abs(st._day_accum - rest) < 1e-7,
              rest, st._day_accum)

abschnitt("GPT-001: Götterschutz nach sieben Tagen")
# Mit keiner Einheit, Mauer oder anderem Kriegspunkt darf der Schutz NICHT frueher enden.
gross = neuer_stand()
gross.tick(7 * SEK_TAG)
erwartung("7 Tage in einem Tick: Tag 8", gross.day == 8, 8, gross.day)
erwartung("7 Tage in einem Tick: Götterschutz aus", gross.noob_protection is False,
          False, gross.noob_protection)

klein = neuer_stand()
for _ in range(7):
    klein.tick(SEK_TAG)
check("7 einzelne Tages-Ticks: Tag 8", klein.day == 8, str(klein.day))
check("7 einzelne Tages-Ticks: Götterschutz endet", klein.noob_protection is False,
      str(klein.noob_protection))
erwartung("Ein grosser und sieben kleine Ticks liefern denselben Tagesstand",
          gross.day == klein.day, klein.day, gross.day)
erwartung("Ein grosser und sieben kleine Ticks liefern denselben Schutz",
          gross.noob_protection == klein.noob_protection,
          klein.noob_protection, gross.noob_protection)

sys.exit(bericht())
