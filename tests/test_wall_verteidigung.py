"""Der Dorfwall steht an EINER Stelle: Siedlungskarte, Rubrik Verteidigung (Daniel 08.11.2026).

Daniels Wortlaut aus Spieltest 3 (Note 3): der Wall gehoert "in die geoeffnete karte in das
dortige menue, wo man auch Gebaeude baut, bei Verteidigung". Vorher stand der Block im
Dorfzentrum, die Rubrikwahl lag HINTER der Feldpruefung - "Verteidigung" war also nur nach einem
Feldklick erreichbar, obwohl der Wall kein Kartenfeld belegt.

Geprueft wird (a) die Quellstruktur und (b) die sichtbare Folge in einem echten Fenster:
  a1  genau EINE Methode ruft `_mauer_reparatur_block(` - sie heisst `_wall_block`
  a2  `_render_overview` ruft ihn NICHT (kein zweiter Ort)
  a3  die Rubrikwahl steht im Quelltext VOR der Feldpruefung
  b1  mit Wallstufe, `karten_feld = None`, Rubrik Verteidigung: Stufe und Zustand stehen da
  b2  mit Wallstufe steht dort die Reparatur (derselbe Block wie frueher im Dorfzentrum)
  b3  Rubrik Produktion ohne Feld: KEIN Knopf "Wall errichten"
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['baumenue_info', 'dorfwall', 'main:*', 'originalkarten']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import ast
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
import originalkarten                                             # noqa: E402

QUELLE = (WURZEL / "src" / "main.py").read_text(encoding="utf-8")


def _methoden_mit(aufruf: str) -> list:
    """Alle Methodennamen, in deren Rumpf `aufruf` vorkommt (AST, keine Textsuche)."""
    treffer = []
    for knoten in ast.walk(ast.parse(QUELLE)):
        if not isinstance(knoten, ast.FunctionDef):
            continue
        for innen in ast.walk(knoten):
            if isinstance(innen, ast.Call) and isinstance(innen.func, ast.Attribute):
                if innen.func.attr == aufruf:
                    treffer.append(knoten.name)
                    break
    return treffer


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


def _label_mit(widget, anfang: str):
    """Erstes Label unterhalb von `widget`, dessen Text mit `anfang` beginnt (sonst None)."""
    for kind in widget.winfo_children():
        if isinstance(kind, tk.Label) and str(kind.cget("text")).startswith(anfang):
            return kind
        treffer = _label_mit(kind, anfang)
        if treffer is not None:
            return treffer
    return None


def _enthaelt_auswahl(widget) -> bool:
    """Steht im Teilbaum dieses Widgets die Rubrik-Auswahl (OptionMenu)?"""
    for kind in widget.winfo_children():
        if isinstance(kind, tk.OptionMenu) or _enthaelt_auswahl(kind):
            return True
    return False


def _spalte_mit_auswahl(widget):
    """Naechstes Elternteil, in dessen Teilbaum die Baubereich-Auswahl steht (sonst None)."""
    while widget is not None:
        if _enthaelt_auswahl(widget):
            return widget
        widget = getattr(widget, "master", None)
    return None


def _methode(name: str) -> str:
    """Quelltext EINER Methode, ueber die AST-Grenzen geschnitten.

    Ein blankes `QUELLE.index(...)` trifft die ERSTE Fundstelle der ganzen Datei - und
    `feld = getattr(self, "karten_feld", None)` steht auch in drei anderen Ansichten
    (10919, 11060, 11114). Der Vergleich lief deshalb gegen eine fremde Methode
    (gemessen 08.11.2026: 780570 gegen 744521). Die Zusage gilt nur innerhalb von
    `_render_settlement_map`.
    """
    for knoten in ast.walk(ast.parse(QUELLE)):
        if isinstance(knoten, ast.FunctionDef) and knoten.name == name:
            return "\n".join(QUELLE.split("\n")[knoten.lineno - 1:knoten.end_lineno])
    raise AssertionError("Methode fehlt im Quelltext: " + name)


class Quellstruktur(unittest.TestCase):
    def test_genau_eine_anzeige(self):
        rufen = _methoden_mit("_mauer_reparatur_block")
        check("genau EINE Methode zeigt die Reparatur", rufen == ["_wall_block"], str(rufen))

    def test_dorfzentrum_zeigt_sie_nicht(self):
        check("_render_overview ruft den Reparaturblock nicht",
              "_mauer_reparatur_block" not in _methoden_mit("_mauer_reparatur_block"), "ok")

    def test_rubrikwahl_steht_vor_der_feldpruefung(self):
        rumpf = _methode("_render_settlement_map")
        i_wahl = rumpf.index("kategorien = baumenue_info.KATEGORIEN")
        i_feld = rumpf.index('feld = getattr(self, "karten_feld", None)')
        check("die Rubrikwahl steht VOR der Feldpruefung", i_wahl < i_feld,
              "%d gegen %d (in _render_settlement_map)" % (i_wahl, i_feld))


class Fenster(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = M.NebelseetalApp.__new__(M.NebelseetalApp)
        self.app.root = self.root
        self.state = M.GameState()
        self.karte = originalkarten.startkarte("wall-verteidigung", "spieler")
        self.ort = M.Settlement(name="A", map_id="kontinent", karte=self.karte,
                                id="spieler:kontinent:1:1",
                                vorraete={"holz": 200, "stein": 200})
        self.state.settlements = [self.ort]
        self.state.research["Verteidigungsanlagen"].level = 3
        self.ort.mauer_besetzt = True
        # Ein UNBESCHAEDIGTER Wall zeigt an dieser Stelle "Die Mauer ist unbeschaedigt
        # (100 Prozent)." - richtig, aber dann ist die Reparatur-Zusage nicht messbar.
        # Mit Schaden steht der Preis und der Knopf "Mauer reparieren" (dorfwall.
        # reparatur_pruefen, Z. 198 ff.).
        self.ort.mauer_zustand = 55.0
        self.app.state = self.state
        self.app.content = tk.Frame(self.root)
        self.app.content.pack()
        self.app.skin = M.SKINS["standard"]
        self.app.karten_feld = None
        # _render_settlement_map liest `karten_siedlung` (Z. 11425 und oefter), NICHT die
        # Siedlungsliste: ohne diese Zeile landet die Ansicht im fruehen Rueckfall
        # "Noch keine Siedlung gewaehlt" und misst gar nichts (gemessen 08.11.2026).
        self.app.karten_siedlung = self.ort
        self.app._render_view = lambda: None

    def tearDown(self):
        self.root.destroy()

    def test_verteidigung_ohne_feld_zeigt_wall_und_reparatur(self):
        self.app._karten_baukategorie = "Verteidigung"
        self.app._render_settlement_map()
        texte = " | ".join(_texte(self.app.content))
        # Note 3 verlangt den Wall "in das dortige menue ... bei Verteidigung" - also in der
        # Baubereich-Spalte und NICHT mehr als eigene Zeile ueber der Karte. Ein Textvergleich
        # allein genuegt nicht: "Stufe" steht auch in "Ausbaustufe", und die alte Wallzeile
        # ueber der Karte trug denselben Wortlaut (gemessen 08.11.2026, Altstand blieb gruen).
        wall = _label_mit(self.app.content, "Dorfwall:")
        # Frueher lag die Wallzeile in einem eigenen Rahmen ueber der Karte - also war ihr
        # naechstes Elternteil mit Baubereich-Auswahl die ANSICHT selbst. In der Rubrik
        # Verteidigung liegt sie in der Auswahl-Spalte (gemessen 08.11.2026).
        spalte = _spalte_mit_auswahl(wall)
        check("die Wallzeile steht in der Spalte mit der Baubereich-Auswahl",
              spalte is not None and spalte is not self.app.content,
              "spalte=%r" % (spalte,))
        check("die Rubrik Verteidigung nennt Stufe und Zustand",
              wall is not None and "Stufe" in str(wall.cget("text")), texte)
        check("der Reparaturblock steht dort (Zustand und Preis oder Knopf)",
              "Mauer: Stufe" in texte and ("Reparatur" in texte or "reparieren" in texte.lower()),
              texte)
        check("das gewaehlte Feld bleibt leer", self.app.karten_feld is None, str(self.app.karten_feld))

    def test_produktion_ohne_feld_zeigt_keinen_wall_knopf(self):
        self.app._karten_baukategorie = "Produktion"
        self.app._render_settlement_map()
        knoepfe = [str(k.cget("text")) for k in _knoepfe(self.app.content)]
        check("in der Rubrik Produktion gibt es keinen Wall-Knopf",
              not any("Wall errichten" in text for text in knoepfe), str(knoepfe))
        # Die alte Wallzeile stand ueber der Karte und erschien deshalb in JEDER Rubrik;
        # seit dem Umzug darf sie nur noch in Verteidigung auftauchen (Note 3).
        check("in der Rubrik Produktion steht keine Wallzeile",
              _label_mit(self.app.content, "Dorfwall:") is None,
              " | ".join(_texte(self.app.content)))


def main_test():
    """Fuehrt Quell- und Fensterpruefungen aus und meldet das Ergebnis."""
    abschnitt("1. Der Wall steht an EINER Stelle (Quellstruktur)")
    for klasse in (Quellstruktur, Fenster):
        suite = unittest.TestLoader().loadTestsFromTestCase(klasse)
        ergebnis = unittest.TextTestRunner(verbosity=0).run(suite)
        check("keine Ausnahme in " + klasse.__name__, not ergebnis.errors, str(ergebnis.errors))
        check("keine fehlgeschlagene Pruefung in " + klasse.__name__, not ergebnis.failures, str(ergebnis.failures))
    return bericht()


if __name__ == "__main__":
    sys.exit(main_test())
