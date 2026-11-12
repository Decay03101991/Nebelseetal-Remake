"""Befund S5 (Opus-Pruefung 08.11.2026): die Ausbildungs-Vorschau zeigt IMMER einen Preis.

Vorher setzte `_ausbilden_block` die Menge auf 0, wenn nichts bezahlbar war - dann stand in der
Vorschau "0 x Buergerwehr = 0 leder ...  -  davon bezahlbar: 0" und der Preis fehlte genau in dem
Moment, in dem der Spieler wissen muss, WAS ihm fehlt. Jetzt rechnet die Vorschau mit Menge 1;
der Knopf bleibt gesperrt.

Geprueft wird die Anzeige gegen eine gestellte Rechnung (der Kern wird ersetzt), damit der Test
kein Dorf mit Kaserne aufbauen muss - die Zahlen des Kerns pruefen `test_ausbildung_uebersicht`.
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['main:*', 'spieloekonomie']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import sys
import tkinter as tk
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness import abschnitt, bericht, check                     # noqa: E402
import main as M                                                  # noqa: E402


def _knoepfe(widget):
    """Alle Knoepfe unterhalb eines Widgets (rekursiv)."""
    for kind in widget.winfo_children():
        if isinstance(kind, tk.Button):
            yield kind
        yield from _knoepfe(kind)


def _texte(widget):
    """Alle Label-Texte unterhalb eines Widgets (rekursiv)."""
    for kind in widget.winfo_children():
        if isinstance(kind, tk.Label):
            yield str(kind.cget("text"))
        yield from _texte(kind)


class VorschauTest(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = M.NebelseetalApp.__new__(M.NebelseetalApp)
        self.app.root = self.root
        self.app.state = M.GameState()
        self.app.state.settlements = [M.Settlement(name="A", map_id="kontinent",
                                                   id="spieler:kontinent:1:1")]
        self.app.content = tk.Frame(self.root)
        self.app.content.pack()
        self.app.skin = M.SKINS["standard"]

    def tearDown(self):
        self.root.destroy()

    def _stellen(self, moeglich):
        """Ersetzt die Rechenstelle des Kerns durch eine feste Lage."""
        lage = {"moeglich": moeglich, "kosten_je": {"wolle": 50.0}, "siedler_je": 1,
                "ausruestung_je": {}, "grenzen": {"wolle": moeglich},
                "dauer_je": 600.0, "freie_zeit": 0.0}
        self._alt = M.spieloekonomie.ausbildung_grenzen
        M.spieloekonomie.ausbildung_grenzen = lambda *a, **k: dict(lage)
        try:
            self.app._ausbilden_block("Buergerwehr", "kaserne", 1)
        finally:
            M.spieloekonomie.ausbildung_grenzen = self._alt

    def test_preis_steht_auch_wenn_nichts_bezahlbar_ist(self):
        self._stellen(0)
        texte = " | ".join(_texte(self.app.content))
        check("die Vorschau nennt die Menge 1", ("1 \u00d7" in texte), texte)
        check("die Vorschau nennt den fehlenden Preis", "50 wolle" in texte, texte)
        check("die Vorschau nennt weiter 'davon bezahlbar: 0'", "bezahlbar: 0" in texte, texte)

    def test_knopf_bleibt_gesperrt(self):
        self._stellen(0)
        knoepfe = [k for k in _knoepfe(self.app.content) if "Ausbilden" in str(k.cget("text"))]
        check("es gibt genau einen Ausbilden-Knopf", len(knoepfe) == 1, str(len(knoepfe)))
        check("der Knopf ist gesperrt", str(knoepfe[0].cget("state")) == "disabled",
              str(knoepfe[0].cget("state")))

    def test_bezahlbare_lage_bleibt_unveraendert(self):
        self._stellen(3)
        texte = " | ".join(_texte(self.app.content))
        check("bei bezahlbarer Lage steht die Menge 1 da", ("1 \u00d7" in texte), texte)
        knoepfe = [k for k in _knoepfe(self.app.content) if "Ausbilden" in str(k.cget("text"))]
        check("der Knopf ist offen", str(knoepfe[0].cget("state")) == "normal",
              str(knoepfe[0].cget("state")))


def main_test():
    """Fuehrt die Fensterpruefungen aus und meldet das Ergebnis."""
    abschnitt("1. Vorschau der Ausbildung (Befund S5)")
    suite = unittest.TestLoader().loadTestsFromTestCase(VorschauTest)
    ergebnis = unittest.TextTestRunner(verbosity=0).run(suite)
    check("keine Ausnahme in der Vorschau", not ergebnis.errors, str(ergebnis.errors))
    check("keine fehlgeschlagene Fensterpruefung", not ergebnis.failures, str(ergebnis.failures))
    return bericht()


if __name__ == "__main__":
    sys.exit(main_test())
