# -*- coding: ascii -*-
"""Wache fuer S-5: der Weltensprung hat KEINE Wartezeit mehr (F-28 = C, Register 332).

WARUM ES DIESE WACHE GIBT (Schnitt S-6 aus docs/design/PORTAL_MODELL_20261108.md)
--------------------------------------------------------------------------------
S-5 (09.11.2026, 08:07) hat die belegte 24-Stunden-Sperre auf Daniels Entscheid F-28 = C
entfernt: `portalraum.wechsel_erlaubt` fragt nur noch Weltkarte und Mana, der Zeitstempel
`letzter_wechsel` wird weiter geschrieben, sperrt aber nichts. Die vorhandenen Wachen
(`test_portalraum`, `test_dorf_versetzen`, `test_e2e_wege`, `test_spielschicht`) pruefen das
am KERN. Was fehlte, ist die Wache am FENSTER: dass die Portalansicht wirklich "zuletzt
gewechselt" sagt statt einer Restzeit, und dass der Spieler im ECHTEN Fenster zweimal
hintereinander springen kann.

Geprueft wird:
  a1  `main.py` enthaelt `_sperre_text` nicht mehr (die Restzeit-Methode ist umbenannt)
  a2  `_render_portal` nennt `_letzter_wechsel_text` und die Beschriftung "zuletzt gewechselt"
  a3  `_dorf_versetzen` ruft `wechsel_erlaubt` mit genau DREI Werten (AST, kein Textfund)
  b1  die Kernfunktion nimmt drei Werte; `_STUNDEN_SPERRE` existiert nicht mehr
  b2  ein Wechsel von gerade eben ist mit genug Mana erlaubt (der Kern sagt nicht mehr Nein)
  b3  ein Altaufruf mit Zeitstempel wirft TypeError (kein stilles Ignorieren)
  c1  im echten Fenster steht "zuletzt gewechselt:" und NICHT mehr "Sperre:"
  c2  ohne Wechsel steht "noch nie gewechselt", nach einem Wechsel "vor wenigen Minuten"
  c3  ein alter Zeitstempel wird als "vor 3.0 h" angezeigt, ein Zukunftsstempel benannt
  c4  ZWEI Umzuege hintereinander gelingen im Fenster, jeder mit GENAU einem Festpreis

Aufruf: python -X utf8 tests/test_portal_s5_keine_wartezeit.py
"""
from __future__ import annotations

import ast
import inspect
import os
import sys
import textwrap
import time
import tkinter as tk
import unittest
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WURZEL / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness import abschnitt, bericht, check                     # noqa: E402
import main as M                                                  # noqa: E402
import portalraum as P                                            # noqa: E402

QUELLE = (WURZEL / "src" / "main.py").read_text(encoding="utf-8")


def _methode(name: str) -> str:
    """Quelltext EINER Methode (ueber Zeilengrenzen geschnitten, kein Textfund irgendwo)."""
    for knoten in ast.walk(ast.parse(QUELLE)):
        if isinstance(knoten, ast.FunctionDef) and knoten.name == name:
            return "\n".join(QUELLE.split("\n")[knoten.lineno - 1:knoten.end_lineno])
    raise AssertionError("Methode fehlt im Quelltext: " + name)


def _aufrufe_mit_argumenten(quelle: str, funktion: str) -> list:
    """Wie viele Werte bekommt jeder Aufruf von `funktion`? (AST, zaehlt Positional + Keyword.)"""
    zahlen = []
    for knoten in ast.walk(ast.parse(textwrap.dedent(quelle))):
        if not isinstance(knoten, ast.Call):
            continue
        ziel = knoten.func
        name = getattr(ziel, "attr", None) or getattr(ziel, "id", None)
        if name != funktion:
            continue
        zahlen.append(len(knoten.args) + len(knoten.keywords))
    return zahlen


def _texte(widget):
    """Alle Label-Texte unterhalb eines Widgets (rekursiv)."""
    for kind in widget.winfo_children():
        if isinstance(kind, tk.Label):
            yield str(kind.cget("text"))
        yield from _texte(kind)


def _knoepfe(widget):
    """Alle Knoepfe unterhalb eines Widgets (rekursiv)."""
    for kind in widget.winfo_children():
        if isinstance(kind, tk.Button):
            yield kind
        yield from _knoepfe(kind)


class Quelle(unittest.TestCase):
    """(a) Die Umstellung steht im Quelltext, nicht nur im Verhalten."""

    def test_a1_restzeit_methode_ist_weg(self):
        check("die Restzeit-Methode _sperre_text kommt in main.py nicht mehr vor",
              "_sperre_text" not in QUELLE)

    def test_a2_portalzeile_sagt_zuletzt_gewechselt(self):
        leib = _methode("_render_portal")
        check("_render_portal nennt _letzter_wechsel_text", "_letzter_wechsel_text" in leib)
        check("die Portalzeile ist mit 'zuletzt gewechselt' beschriftet",
              "zuletzt gewechselt" in leib, leib[-400:])
        check("die alte Beschriftung 'Sperre:' steht nicht mehr in _render_portal",
              "Sperre:" not in leib)

    def test_a3_buchstelle_reicht_drei_werte(self):
        leib = _methode("_dorf_versetzen")
        zahlen = _aufrufe_mit_argumenten(leib, "wechsel_erlaubt")
        check("die Buchstelle ruft wechsel_erlaubt genau einmal", len(zahlen) == 1, str(zahlen))
        check("und zwar mit genau DREI Werten (kein Zeitstempel, keine Uhr)",
              zahlen == [3], str(zahlen))

    def test_a4_kernmodul_liest_keine_stundensperre(self):
        quelle = (WURZEL / "src" / "portalraum.py").read_text(encoding="utf-8")
        check("portalraum nennt die Konstante _STUNDEN_SPERRE nicht mehr",
              "_STUNDEN_SPERRE" not in quelle.replace("`_STUNDEN_SPERRE`", ""),
              "nur der Kommentar darf sie nennen")
        zahlen = _aufrufe_mit_argumenten(quelle, "wechsel_erlaubt")
        check("portalraum ruft sich selbst nicht mit Zeitstempel", all(z == 3 for z in zahlen),
              str(zahlen))


class Kern(unittest.TestCase):
    """(b) Der Kern sagt Ja, wo er vor S-5 Nein sagen musste."""

    def test_b1_signatur(self):
        werte = list(inspect.signature(P.wechsel_erlaubt).parameters)
        check("wechsel_erlaubt nimmt genau drei Werte", werte == ["von_z", "nach_z", "mana"],
              str(werte))
        check("die alte Sperrkonstante gibt es nicht mehr",
              not hasattr(P, "_STUNDEN_SPERRE"), "STUNDEN_SPERRE existiert wieder")

    def test_b2_wechsel_von_gerade_eben_ist_erlaubt(self):
        # Bis Register 331 war derselbe Aufruf mit einem Stempel von vor einer Sekunde verboten.
        erlaubt, meldung = P.wechsel_erlaubt(0, 1, 100000.0)
        check("mit genug Mana ist der Wechsel ERLAUBT (keine Wartezeit)", erlaubt is True, meldung)
        gebucht = P.nach_wechsel(10000.0, 1000.0)
        check("nach_wechsel schreibt den Zeitstempel weiter", gebucht["letzter_wechsel"] == 1000.0,
              str(gebucht))
        erlaubt2, meldung2 = P.wechsel_erlaubt(1, 0, 100000.0)      # eine Sekunde spaeter, egal
        check("und ein zweiter Wechsel bleibt erlaubt", erlaubt2 is True, meldung2)

    def test_b3_altaufruf_bricht(self):
        try:
            P.wechsel_erlaubt(0, 1, 5000, None, 0.0)
        except TypeError:
            check("ein Altaufruf mit Zeitstempel ist ein Fehler", True)
        except Exception as fehler:                                  # noqa: BLE001
            check("ein Altaufruf mit Zeitstempel ist ein Fehler", False, repr(fehler))
        else:
            check("ein Altaufruf mit Zeitstempel ist ein Fehler", False,
                  "der vierte Wert wurde angenommen")


class Fenster(unittest.TestCase):
    """(c) Die Anzeige und der echte Weg im Fenster."""

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = M.NebelseetalApp.__new__(M.NebelseetalApp)
        self.app.root = self.root
        self.state = M.GameState()
        self.start = int(self.state.eigene_dimension)
        self.state.resources["mana"].amount = 30000.0
        self.state.letzter_wechsel = None
        self.dorf = M.Settlement(name="Eschenhain", map_id="kontinent", x=0, y=0,
                                 id=M.siedlung_kennung("spieler", "kontinent", 0, 0),
                                 dimension=self.start, welt_x=5, welt_y=5)
        self.state.settlements = [self.dorf]
        self.state.bots = []
        self.app.state = self.state
        self.app.content = tk.Frame(self.root)
        self.app.content.pack()
        self.app.skin = M.SKINS["standard"]
        self.app.portal_auswahl = None
        self.app.portal_dorf = ""
        self.app._portal_blick = self.start
        self.app._render_view = lambda: None
        self.app._switch_view = lambda name: None

    def tearDown(self):
        self.root.destroy()

    def _neu(self):
        for kind in self.app.content.winfo_children():
            kind.destroy()
        self.app._render_portal()

    def test_c1_und_c2_beschriftung_und_erster_wechsel(self):
        self._neu()
        texte = " | ".join(_texte(self.app.content))
        check("die Zeile traegt die Beschriftung 'zuletzt gewechselt:'",
              "zuletzt gewechselt:" in texte, texte)
        check("es steht keine Sperre mehr in der Zeile", "Sperre:" not in texte, texte)
        check("ohne Wechsel steht 'noch nie gewechselt'", "noch nie gewechselt" in texte, texte)
        self.app.portal_auswahl = (7, 12)
        self.app.portal_dorf = "Eschenhain"
        ok = self.app._portal_dorf_springen(self.start)
        check("der erste Umzug wird gebucht", ok is True, str(ok))
        self._neu()
        texte2 = " | ".join(_texte(self.app.content))
        check("nach dem Wechsel steht 'vor wenigen Minuten'", "vor wenigen Minuten" in texte2, texte2)

    def test_c3_alte_und_kaputte_stempel(self):
        self.state.letzter_wechsel = time.time() - 3 * 3600
        self._neu()
        texte = " | ".join(_texte(self.app.content))
        check("ein Wechsel von vor drei Stunden wird als 'vor 3.0 h' angezeigt",
              "vor 3.0 h" in texte, texte)
        self.state.letzter_wechsel = time.time() + 3600
        self._neu()
        texte2 = " | ".join(_texte(self.app.content))
        check("ein Zeitstempel aus der Zukunft wird benannt, nicht verschwiegen",
              "Zukunft" in texte2, texte2)

    def test_c4_zwei_umzuege_hintereinander(self):
        kosten = float(P.wechselkosten())
        self.app.portal_auswahl = (7, 12)
        self.app.portal_dorf = "Eschenhain"
        vorher = float(self.state.resources["mana"].amount)
        erster = self.app._portal_dorf_springen(self.start)
        check("der erste Umzug gelingt", erster is True, str(erster))
        check("GENAU ein Festpreis ist abgebucht",
              abs(float(self.state.resources["mana"].amount) - (vorher - kosten)) < 1e-6,
              str(self.state.resources["mana"].amount))
        # SOFORT der zweite Sprung - bis Register 331 hielt hier die 24-Stunden-Sperre an.
        self.app.portal_auswahl = (9, 12)
        self.app.portal_dorf = "Eschenhain"
        mitte = float(self.state.resources["mana"].amount)
        zweiter = self.app._portal_dorf_springen(self.start)
        check("der ZWEITE Umzug sofort gelingt (keine Wartezeit)", zweiter is True, str(zweiter))
        check("und wieder ist GENAU ein Festpreis weg",
              abs(float(self.state.resources["mana"].amount) - (mitte - kosten)) < 1e-6,
              str(self.state.resources["mana"].amount))
        check("das Dorf steht auf dem zweiten Feld",
              (self.dorf.welt_x, self.dorf.welt_y) == (9, 12),
              str((self.dorf.welt_x, self.dorf.welt_y)))
        check("kein Knopf heisst mehr Weltensprung",
              "Weltensprung" not in " | ".join(str(k.cget("text")) for k in _knoepfe(self.app.content)))


def main_() -> int:
    abschnitt("S-6: S-5 am Kern UND am Fenster belegt (F-28 = C, Register 332)")
    for klasse in (Quelle, Kern, Fenster):
        erg = unittest.TextTestRunner(verbosity=0).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(klasse))
        if erg.errors or erg.failures:               # Ausnahmen sind Fehler, keine Befunde
            for fall, spur in list(erg.errors) + list(erg.failures):
                check("%s laeuft durch" % fall, False, spur.strip().splitlines()[-1])
    return bericht()


if __name__ == "__main__":
    sys.exit(main_())
