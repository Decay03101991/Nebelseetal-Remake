# -*- coding: ascii -*-
"""Schritt 11 des Ablaufs: die AST-Quellwache - Ansichten zeigen, sie rechnen nicht.

DANIELS BEFUND AUS SPIELTEST 1 UND 2 (Uebergabe 08.11.2026, Abschnitt 3): die Anzeige rechnete an
mehreren Stellen selbst und wich damit vom Kern ab ("gruener Text, Wirkung null"). Diese Wache liest
den QUELLTEXT (ueber `ast`) und sucht in den Methoden von `NebelseetalApp`, deren Name mit `_zeige`,
`_zeichne` oder `_render` beginnt, zwei Dinge:

  * jede Multiplikation oder Division (`kante * zelle`, `rest / 60`),
  * jeden Vergleich gegen eine Ganzzahl groesser 1 (`if stufe >= 3`).

Docstrings und Kommentare zaehlen NICHT als Code - `ast` kennt nur ausfuehrbaren Code, Kommentare
stehen dort gar nicht. Ein Treffer ist ein Befund, AUSSER die Methode steht mit Grund in
`tests/quelle_ast_ausnahmen.json` (Pixel-/Zeichengeometrie im Canvas). Fehlt der Eintrag, ist die
Wache rot.

WAS DIESE WACHE SCHON GEFUNDEN HAT (gemessen, Register 309):
  * `_render_overview`: `_heilkunde * 10` - die Handbuchzahl "10 % je Stufe" stand ein ZWEITES Mal in
    der Anzeige, obwohl der echte Wert aus `gebaeude_wirkung.siedler_zuwachs_pro_stunde` kommt.
    Jetzt liefert `forschung_wirkung.siedler_bonus_prozent` die Prozentzahl.
  * `_render_overview`: `rest / 60.0` - Sekunden-zu-Minuten-Umrechnung in der Ansicht. Jetzt
    `main.minuten_text`.
  * `_render_diplomacy` (2x) und drei Handelssaetze: `int(bot.trading * 100)`. Jetzt
    `main.prozent_text`.
Damit bleiben genau die zwei Pixelmethoden als begruendete Ausnahme.

Aufruf:  python -X utf8 tests/test_quelle_ast.py
"""
from __future__ import annotations

import ast
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src, messwert

ROOT, SRC = import_src()
AUSNAHMEN_DATEI = os.path.join(ROOT, "tests", "quelle_ast_ausnahmen.json")
PRAEFIXE = ("_zeige", "_zeichne", "_render")


def ausnahmen() -> dict:
    """Die begruendeten Ausnahmen als {Methode: {erlaubt, grund}}."""
    with open(AUSNAHMEN_DATEI, encoding="utf-8") as datei:
        daten = json.load(datei)
    return {str(e.get("methode")): {"erlaubt": int(e.get("erlaubt") or 0),
                                    "grund": str(e.get("grund") or "")}
            for e in (daten.get("ausnahmen") or [])}


def stellen(methode: ast.FunctionDef) -> list:
    """Alle Rechen- und Vergleichsstellen EINER Methode als [(Zeile, Text)]."""
    treffer = []
    for knoten in ast.walk(methode):
        if isinstance(knoten, ast.BinOp) and isinstance(knoten.op, (ast.Mult, ast.Div)):
            treffer.append((knoten.lineno, ast.unparse(knoten)))
        if isinstance(knoten, ast.Compare):
            for seite in [knoten.left] + list(knoten.comparators):
                if (isinstance(seite, ast.Constant) and isinstance(seite.value, int)
                        and not isinstance(seite.value, bool) and seite.value > 1):
                    treffer.append((knoten.lineno, ast.unparse(knoten)))
                    break
    return sorted(treffer)


def ansichts_methoden(quelle: str, klassenname: str = "NebelseetalApp"):
    """{Methodenname: Stellen} fuer alle Ansichts-Methoden der Klasse."""
    baum = ast.parse(quelle, filename="src/main.py")
    klasse = next((k for k in baum.body
                   if isinstance(k, ast.ClassDef) and k.name == klassenname), None)
    if klasse is None:                                     # Klasse umbenannt: nichts erfinden
        return {}
    ergebnis = {}
    for knoten in klasse.body:
        if isinstance(knoten, ast.FunctionDef) and knoten.name.startswith(PRAEFIXE):
            ergebnis[knoten.name] = stellen(knoten)
    return ergebnis


_quelle = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
_methoden = ansichts_methoden(_quelle)
_erlaubt = ausnahmen()

abschnitt("1. Die Wache liest den Quelltext, nicht die Anzeige")
check("NebelseetalApp gefunden", bool(_methoden))
check("Ansichts-Methoden gefunden (_zeige/_zeichne/_render)", bool(_methoden),
      "%d Methoden" % len(_methoden or {}))
messwert("ansichtsmethoden", len(_methoden or {}), "Methoden", "AST-Lauf ueber src/main.py")
messwert("ausnahmen", len(_erlaubt), "Methoden", "tests/quelle_ast_ausnahmen.json")

abschnitt("2. Keine unbegruendete Rechnung in einer Ansicht")
_verstoesse = []
_stellen_gesamt = 0
for name, treffer in sorted((_methoden or {}).items()):
    _stellen_gesamt += len(treffer)
    grenze = int((_erlaubt.get(name) or {}).get("erlaubt") or 0)
    if len(treffer) > grenze:
        _verstoesse.append((name, len(treffer), grenze, treffer[:3]))
messwert("stellen_gesamt", _stellen_gesamt, "Stellen", "Multiplikationen/Divisionen/Vergleiche")
check("jede Stelle ist gedeckt (Ausnahme mit Grund oder gar keine Rechnung)",
      not _verstoesse, str(_verstoesse[:2]))
check("beide Pixelmethoden sind als Ausnahme eingetragen und begruendet",
      all(_erlaubt.get(n, {}).get("grund") for n in ("_render_portal", "_zeichne_siedlungskarte")),
      str(sorted(_erlaubt)))

abschnitt("3. Die Ausnahme ist kein Freibrief")
# Eine Ausnahme, die auf eine Methode OHNE Treffer zeigt, ist veraltet -> BEFUND, nicht Fehler.
_veraltet = [n for n in _erlaubt if not (_methoden or {}).get(n)]
check("jede Ausnahme nennt eine vorhandene Ansichts-Methode", not _veraltet, str(_veraltet))
_zu_weit = [n for n in _erlaubt
            if len((_methoden or {}).get(n) or []) < int(_erlaubt[n]["erlaubt"])]
if _zu_weit:
    befund("Ausnahmen decken mehr Stellen ab als vorhanden (darf enger gefasst werden): %s"
           % ", ".join("%s %d<%d" % (n, len(_methoden[n]), _erlaubt[n]["erlaubt"]) for n in _zu_weit), "")
check("die Ausnahmen decken genau die Pixelmethoden ab",
      sorted(_erlaubt) == ["_render_portal", "_zeichne_siedlungskarte"], str(sorted(_erlaubt)))

abschnitt("4. Die drei gefundenen Stellen sind an EINER Stelle gelandet")
import forschung_wirkung  # noqa: E402
import main  # noqa: E402
check("Heilkunde-Prozent kommt aus `forschung_wirkung.siedler_bonus_prozent`",
      forschung_wirkung.siedler_bonus_prozent({"Heilkunde": 3}) == 30.0,
      str(forschung_wirkung.siedler_bonus_prozent({"Heilkunde": 3})))
check("ohne Heilkunde ist der Bonus 0", forschung_wirkung.siedler_bonus_prozent({}) == 0.0)
check("Handelsneigung kommt aus `main.prozent_text`", main.prozent_text(0.8) == "80 %",
      main.prozent_text(0.8))
check("Minuten kommen aus `main.minuten_text`", main.minuten_text(750) == "12.5 min",
      main.minuten_text(750))
check("die Handelsneigung wird in keiner Ansicht mehr mit 100 multipliziert",
      all("trading" not in text for treffer in (_methoden or {}).values() for _, text in treffer),
      str([t for treffer in (_methoden or {}).values() for _, t in treffer if "trading" in t][:3]))

abschnitt("5. Gegenprobe: eine neue Rechnung in einer Ansicht wird gemeldet")
# Die Gegenprobe laeuft auf einem ERFUNDENEN Quelltext - kein Umbau am echten Spiel, keine
# Nebenwirkung auf den Arbeitsbaum.
_probe = ("class NebelseetalApp:\n"
          "    def _render_probe(self):\n"
          "        return stufe * 2 + 1\n"
          "    def _render_sauber(self):\n"
          "        return 'nur Text'\n")
_ergebnis = ansichts_methoden(_probe)
check("die Probe-Methode mit Rechnung wird erkannt", bool(_ergebnis.get("_render_probe")),
      str(_ergebnis.get("_render_probe")))
check("die Methode ohne Rechnung bleibt leer", not _ergebnis.get("_render_sauber"),
      str(_ergebnis.get("_render_sauber")))
_probe_vergleich = ("class NebelseetalApp:\n"
                    "    def _zeichne_probe(self):\n"
                    "        if stufe >= 3:\n"
                    "            return 1\n")
check("auch ein Vergleich gegen eine Ganzzahl groesser 1 wird erkannt",
      bool(ansichts_methoden(_probe_vergleich).get("_zeichne_probe")),
      str(ansichts_methoden(_probe_vergleich)))
check("ein Vergleich gegen 0 oder 1 ist KEIN Befund",
      not ansichts_methoden("class NebelseetalApp:\n"
                            "    def _render_x(self):\n"
                            "        return 1 if a > 1 else 0\n")["_render_x"])


befund("Was NICHT geprueft ist: die Wache liest nur `src/main.py`. Die Ansichten der Messschicht "
       "(`src/spielschicht.py`) und reine Rechenmodule sind absichtlich aussen vor - dort gehoert "
       "Rechnung hin.", "")
befund("Die Pixelausnahmen sind Zahlen aus der Zeichengeometrie. Aendert jemand die Kachelgroesse, "
       "bleibt die Zahl der Stellen meist gleich; neu hinzukommende Pixelrechnungen machen die "
       "Wache rot und muessen begruendet werden.", "")
sys.exit(bericht())
