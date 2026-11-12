"""Der Marktplatz sagt, was er ist: verkaufen, Karawane als Bedingung, JEDER Bot (Spieltest 3, Note 5).

Daniels Befund (Spieltest 3, Schritt 10, Note 5): "Davon sehe ich als spieler nichts im ersten
Eindruck. Ich suche danach zuerst in Diplomatie ... nichts darueber auffindbar." Vorher zeigte
`_render_market` nur "Handle mit anderen Spielern oder Bots.", versteckte jeden Bot mit
Handelsneigung <= 0,3 und nannte die Handelskarawane NIRGENDS - die eine Bedingung, ohne die jeder
Handel abgelehnt wird (Handbuch S. 20).

Geprueft wird (a) die Quellstruktur und (b) die sichtbare Folge in einem echten Fenster:
  a1  `_render_market` fragt `handelt_bot(` und `handelskarawanen_bestand(`
  a2  die Grenze 0,3 wird NIRGENDS mehr getippt (`<= 0.3` kommt im Quelltext nicht vor)
  a3  Kern und Anzeige lesen dieselbe Funktion (`handelt_bot` viermal, `handelt_grund` dreimal)
  b1  zwei Bots (0,9 und 0,1): BEIDE Namen stehen da, nur der handelnde hat einen Knopf
  b2  der nicht handelnde Bot nennt Grund und Prozent
  b3  mit Karawane steht der Zustand da, ohne Karawane die Bedingung
  b4  ohne Siedlung kommt ein Hinweis statt eines Absturzes
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['einheiten', 'main:*']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import sys
import tkinter as tk
import unittest
from pathlib import Path

WURZEL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WURZEL / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness import abschnitt, bericht, check                     # noqa: E402
import main as M                                                  # noqa: E402

QUELLE = (WURZEL / "src" / "main.py").read_text(encoding="utf-8")


def _methode(name: str) -> str:
    """Quelltext EINER Methode, ueber Zeilengrenzen geschnitten (kein Textfund irgendwo)."""
    import ast
    for knoten in ast.walk(ast.parse(QUELLE)):
        if isinstance(knoten, ast.FunctionDef) and knoten.name == name:
            return "\n".join(QUELLE.split("\n")[knoten.lineno - 1:knoten.end_lineno])
    raise AssertionError("Methode fehlt im Quelltext: " + name)


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


class Quellstruktur(unittest.TestCase):
    def test_ansicht_liest_karawane_und_urteil(self):
        rumpf = _methode("_render_market")
        check("der Marktplatz fragt den Karawanen-Zustand ab", "handelskarawanen_bestand(" in rumpf, rumpf[:200])
        check("der Marktplatz fragt das Handels-Urteil ab", "handelt_bot(" in rumpf, rumpf[:200])

    def test_grenze_wird_nicht_mehr_getippt(self):
        check("die Handelsgrenze 0,3 steht nicht mehr als Zahl im Vergleich",
              "<= 0.3" not in QUELLE and "> 0.3" not in QUELLE, "Fundstelle vorhanden")
        check("die Grenze hat EINE benannte Stelle",
              QUELLE.count("HANDELSNEIGUNG_MIN = ") == 1, str(QUELLE.count("HANDELSNEIGUNG_MIN = ")))

    def test_kern_und_anzeige_teilen_das_urteil(self):
        # Definition plus Aufrufe: zwei Pruefungen im Kern, `_trade` und der Marktplatz. Der Satz
        # kommt an vier Stellen (zwei Kernpruefungen, `_trade`, Marktplatz) - keine zweite Fassung
        # in der Anzeige (F-04).
        check("Kern, Maske und Marktplatz nutzen handelt_bot",
              QUELLE.count("handelt_bot(") >= 4, str(QUELLE.count("handelt_bot(")))
        check("der Satz kommt aus EINER Funktion",
              QUELLE.count("handelt_grund(") >= 4, str(QUELLE.count("handelt_grund(")))


class Fenster(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = M.NebelseetalApp.__new__(M.NebelseetalApp)
        self.app.root = self.root
        self.state = M.GameState()
        self.state.units = {}
        self.ort = M.Settlement(name="A", map_id="kontinent", id="spieler:kontinent:1:1",
                                vorraete={"holz": 50, "stein": 50})
        self.state.settlements = [self.ort]
        self.state.bots = [M.BotPlayer("Haug", "menschlich", aggression=0.3, trading=0.9),
                           M.BotPlayer("Viona", "menschlich", aggression=0.3, trading=0.1)]
        self.app.state = self.state
        self.app.content = tk.Frame(self.root)
        self.app.content.pack()
        self.app.skin = M.SKINS["standard"]
        self.app._render_view = lambda: None

    def tearDown(self):
        self.root.destroy()

    def test_jeder_bot_steht_da(self):
        self.app._render_market()
        texte = " | ".join(_texte(self.app.content))
        check("der handelnde Bot steht da", "Haug" in texte, texte)
        check("der NICHT handelnde Bot steht auch da (vorher versteckt)", "Viona" in texte, texte)
        knoepfe = [str(k.cget("text")) for k in _knoepfe(self.app.content)]
        check("genau EIN Handelsknopf", knoepfe.count("Handeln") == 1, str(knoepfe))

    def test_grund_und_prozent_stehen_beim_bot(self):
        self.app._render_market()
        texte = " | ".join(_texte(self.app.content))
        check("der Grund steht im Klartext", "handelt nicht" in texte, texte)
        check("die Handelsneigung steht in Prozent", "10 %" in texte, texte)

    def test_karawane_ist_bedingung_und_zustand(self):
        self.app._render_market()
        ohne = " | ".join(_texte(self.app.content))
        check("ohne Karawane steht die Bedingung da",
              "Keine Handelskarawane" in ohne and "Handbuch S. 20" in ohne, ohne)
        self.ort.einheiten = {"Handelskarawane": 1}
        for kind in self.app.content.winfo_children():
            kind.destroy()
        self.app._render_market()
        mit = " | ".join(_texte(self.app.content))
        check("mit Karawane steht der Zustand da",
              "Handelskarawane im Ortslager von A" in mit and ": 1" in mit, mit)
        check("die Bedingung ist dann weg", "Keine Handelskarawane" not in mit, mit)

    def test_ohne_siedlung_ein_hinweis(self):
        self.state.settlements = []
        self.state.aktive_siedlung_id = ""
        self.app._render_market()
        texte = " | ".join(_texte(self.app.content))
        check("ohne Siedlung steht ein Hinweis", "zuerst eine eigene Siedlung" in texte, texte)


def main_test():
    """Fuehrt Quell- und Fensterpruefungen aus und meldet das Ergebnis."""
    abschnitt("1. Der Marktplatz nennt Karawane und Urteil (Quellstruktur)")
    for klasse in (Quellstruktur, Fenster):
        suite = unittest.TestLoader().loadTestsFromTestCase(klasse)
        ergebnis = unittest.TextTestRunner(verbosity=0).run(suite)
        check("keine Ausnahme in " + klasse.__name__, not ergebnis.errors, str(ergebnis.errors))
        check("keine fehlgeschlagene Pruefung in " + klasse.__name__, not ergebnis.failures, str(ergebnis.failures))
    return bericht()


if __name__ == "__main__":
    sys.exit(main_test())
