# -*- coding: ascii -*-
"""Der Umzug steht in der Portalansicht: Feld anklicken, Dorf waehlen, springen (Schnitt S-4).

Daniels Auftrag (Spieltest 3, Note 4): "die Auswahl wohin ich springen will sollte auch nicht per
dropdown Feld sein sondern indem ich ein freies Feld auf der entsprechenden Weltkarte auswaehle,
gecheckt wird ob das Feld frei ist und ich die Voraussetzungen habe und mich dann dort hin springen
lassen." Entscheidungen: F-26 = A (belegtes Feld abgelehnt), F-25 = A (nur 5.000 Mana), F-27 = A
(alles reist mit); Antwort A vom 08.11.2026: der alte Knopf "Weltensprung" ist WEG, der Umzug ist
der EINZIGE Weg.

Geprueft wird (a) die Quellstruktur und (b) was im echten Fenster steht:
  a1  `_render_portal` ruft KEIN `_portal_wechsel(` mehr - der alte Knopf ist entfernt
  a2  der Umzug laeuft ueber `_portal_dorf_springen` -> `_dorf_versetzen` (EINE Buchstelle)
  a3  eigene Doerfer werden ueber `_ort_feld` gezeichnet, nicht ueber die Siedlungskarte
  a4  `_portal_feld_waehlen` prueft gegen die ANGESEHENE Welt (`_portal_blick`)
  b1  Dorf-Auswahl, Feldstatus und Knopf nennen Dorf, Feld und Preis
  b2  ein belegtes Feld nennt den Grund und sperrt den Knopf
  b3  ohne Feld ist der Knopf gesperrt und der Grund steht da
  b4  der Klick bucht ueber `_dorf_versetzen`: Dorf sitzt, Mana minus 5.000, Auswahl leer
  b5  das eigene Dorf steht auf seinem PORTALFELD, nicht auf seiner Siedlungskarte
  b6  der Knopf "Weltensprung" kommt nicht mehr vor

Aufruf: python -X utf8 tests/test_portal_ansicht_umzug.py
"""
from __future__ import annotations

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
import portalraum as P                                            # noqa: E402

QUELLE = (WURZEL / "src" / "main.py").read_text(encoding="utf-8")


def _methode(name: str) -> str:
    """Quelltext EINER Methode (ueber Zeilengrenzen geschnitten, kein Textfund irgendwo)."""
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
    def test_alter_knopf_ist_weg(self):
        rumpf = _methode("_render_portal")
        check("die Ansicht nennt _portal_wechsel nicht mehr",
              "_portal_wechsel" not in rumpf, "Name steht noch drin")
        # S-4b (09.11.2026): die Methode selbst ist entfernt, nicht nur ihr Aufruf - ein
        # Wiederauftauchen als Methode macht die Wache genauso rot.
        check("die alte Buchstelle _portal_wechsel gibt es nicht mehr",
              not hasattr(M.NebelseetalApp, "_portal_wechsel"), "Methode existiert wieder")
        check("der Umzug laeuft ueber die Buchstelle",
              "_portal_dorf_springen(" in rumpf, rumpf[:200])

    def test_eine_buchstelle(self):
        rumpf = _methode("_portal_dorf_springen")
        check("die Ansicht bucht ueber _dorf_versetzen", "_dorf_versetzen(" in rumpf, rumpf)
        check("die Ansicht rechnet den Preis nicht selbst",
              "wechselkosten(" not in rumpf, "zweite Preisrechnung in der Ansicht")
        knopf = _methode("_portal_dorf_waehlen")
        check("die Dorf-Wahl bucht nichts", "_dorf_versetzen(" not in knopf)

    def test_eigene_doerfer_ueber_die_eine_aufloesung(self):
        rumpf = _methode("_render_portal")
        check("die Karte fragt _ort_feld fuer die eigenen Doerfer", "_ort_feld(" in rumpf)
        check("die Karte liest nicht mehr _ort.x direkt fuer das Feld",
              "(int(getattr(_ort, \"x\", 0)) + 0.5) * zelle" not in rumpf)

    def test_feldwahl_prueft_die_angeshene_welt(self):
        rumpf = _methode("_portal_feld_waehlen")
        check("die Feldwahl nimmt die angesehene Welt", "\"_portal_blick\"" in rumpf, rumpf[:200])


class Fenster(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = M.NebelseetalApp.__new__(M.NebelseetalApp)
        self.app.root = self.root
        self.state = M.GameState()
        self.start = int(self.state.eigene_dimension)
        self.state.resources["mana"].amount = 20000.0
        self.state.letzter_wechsel = None
        self.dorf = M.Settlement(name="Eschenhain", map_id="kontinent", x=0, y=0,
                                 id=M.siedlung_kennung("spieler", "kontinent", 0, 0),
                                 dimension=self.start, welt_x=5, welt_y=5)
        self.zweit = M.Settlement(name="Zweithauch", map_id="wald", x=4, y=5,
                                  id=M.siedlung_kennung("spieler", "wald", 4, 5),
                                  dimension=self.start, welt_x=2, welt_y=2)
        self.state.settlements = [self.dorf, self.zweit]
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

    def test_kein_weltensprung_knopf_mehr(self):
        self._neu()
        knoepfe = [str(k.cget("text")) for k in _knoepfe(self.app.content)]
        check("kein Knopf heisst mehr Weltensprung", "Weltensprung" not in knoepfe, str(knoepfe))

    def test_dorfwahl_und_gesperrter_knopf_ohne_feld(self):
        self._neu()
        knoepfe = [str(k.cget("text")) for k in _knoepfe(self.app.content)]
        check("beide Doerfer stehen zur Wahl",
              any("Eschenhain" in t for t in knoepfe) and any("Zweithauch" in t for t in knoepfe),
              str(knoepfe))
        umzug = [k for k in _knoepfe(self.app.content) if "hierher versetzen" in str(k.cget("text"))]
        check("genau EIN Umzug-Knopf", len(umzug) == 1, str(len(umzug)))
        if umzug:
            check("ohne Feld ist der Knopf gesperrt",
                  str(umzug[0].cget("state")) == str(tk.DISABLED), str(umzug[0].cget("state")))
        texte = " | ".join(_texte(self.app.content))
        check("der Grund steht im Klartext", "kein Feld" in texte, texte)

    def test_freies_feld_nennt_dorf_feld_preis(self):
        self.app.portal_auswahl = (7, 12)
        self._neu()
        umzug = [k for k in _knoepfe(self.app.content) if "hierher versetzen" in str(k.cget("text"))]
        check("der Knopf ist frei, wenn alles passt", bool(umzug)
              and str(umzug[0].cget("state")) != str(tk.DISABLED), str(umzug))
        if umzug:
            text = str(umzug[0].cget("text"))
            check("der Knopf nennt das Dorf und den Preis",
                  "Eschenhain" in text and "5000" in text, text)
        texte = " | ".join(_texte(self.app.content))
        check("die Zeile nennt Feld und Weltkarte", "x=7" in texte and "y=12" in texte, texte)
        check("das Feld gilt als frei", "ist frei" in texte, texte)

    def test_belegtes_feld_nennt_grund_und_sperrt(self):
        self.app.portal_auswahl = (2, 2)                       # Feld des zweiten eigenen Dorfes
        self._neu()
        texte = " | ".join(_texte(self.app.content))
        check("der Grund nennt das andere Dorf", "Zweithauch" in texte, texte)
        umzug = [k for k in _knoepfe(self.app.content) if "hierher versetzen" in str(k.cget("text"))]
        check("der Knopf ist gesperrt", bool(umzug)
              and str(umzug[0].cget("state")) == str(tk.DISABLED), str(umzug))
        check("der Sperrgrund steht dabei", "Feld nicht frei" in texte, texte)

    def test_klick_bucht_ueber_die_buchstelle(self):
        self.app.portal_auswahl = (7, 12)
        self.app.portal_dorf = "Eschenhain"
        vorher = float(self.state.resources["mana"].amount)
        ok = self.app._portal_dorf_springen(self.start)
        check("der Umzug wird gebucht", ok is True, str(ok))
        check("das Dorf sitzt auf dem Feld", (self.dorf.welt_x, self.dorf.welt_y) == (7, 12),
              str((self.dorf.welt_x, self.dorf.welt_y)))
        check("GENAU der Festpreis ist weg",
              abs(float(self.state.resources["mana"].amount)
                  - (vorher - float(P.wechselkosten()))) < 1e-6,
              str(self.state.resources["mana"].amount))
        check("die Auswahl ist danach leer (der Goldrand haengt nicht am alten Feld)",
              self.app.portal_auswahl is None, str(self.app.portal_auswahl))

    def test_eigenes_dorf_steht_auf_dem_portalfeld(self):
        self._neu()
        flaeche = self.app.portal_zeichenflaeche
        teile = flaeche.find_withtag("portalspieler")           # die gezeichneten eigenen Doerfer
        check("die eigenen Doerfer sind gezeichnet", len(teile) >= 1, str(len(teile)))
        zelle = self.app._portal_zelle(P._achsen())
        erwartet = (int(self.dorf.welt_x) + 0.5) * zelle        # Portalposition 5/5, NICHT x/y 0/0
        # Toleranz 2 px: die Marke wird MITTIG ins Feld gezeichnet. Ein weiter Toleranzrahmen war
        # zu schwach - die Gegenprobe (Zeichnung wieder auf x/y) blieb gruen, weil das ZWEITE Dorf
        # mit seiner Siedlungskarte 4/5 zufaellig in die Naehe des erwarteten Feldes fiel.
        treffer = False
        alten_platz = False
        alt_mitte = (int(self.dorf.x) + 0.5) * zelle            # wo die SIEDLUNGSKARTE liegt (0/0)
        for teil in teile:
            x1, y1, x2, y2 = flaeche.bbox(teil) or (0, 0, 0, 0)
            cx, cy = (x1 + x2) / 2.0, (y1 + y2) / 2.0
            if abs(cx - erwartet) <= 2.0 and abs(cy - erwartet) <= 2.0:
                treffer = True
            if abs(cx - alt_mitte) <= 2.0 and abs(cy - alt_mitte) <= 2.0:
                alten_platz = True
        check("das Dorf sitzt auf seinem PORTALFELD (5/5), nicht auf der Siedlungskarte (0/0)",
              treffer and not alten_platz, "erwartet %.1f, Marken %d" % (erwartet, len(teile)))


def main_() -> int:
    abschnitt("Quellstruktur")
    for klasse in (Quellstruktur, Fenster):
        erg = unittest.TextTestRunner(verbosity=0).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(klasse))
        if erg.errors or erg.failures:                       # Ausnahmen sind Fehler, keine Befunde
            for fall, spur in list(erg.errors) + list(erg.failures):
                check("%s laeuft durch" % fall, False, spur.strip().splitlines()[-1])
    return bericht()


if __name__ == "__main__":
    sys.exit(main_())
