"""S4 Teil 1: Gunst und Status (06.11.2026, Register 272, docs/ABLAUF_LLM_20261106.md Schritt 1).

Geprueft wird, was der Schnitt zusagt:
  A. Die Grenzen gelten an ihren Raendern (-5 / 0 / 50 / 100 / 130) und der Status an 39/40 und 59/60.
  B. Die Grenzen und Stufen kommen aus `data/diplomatie.json` - eine Aenderung in den Daten aendert
     das Urteil, ohne dass Code angefasst wird (A-7).
  C. Ein alter Spielstand ohne das Feld laedt mit dem Startwert, und ein Rueckschreiben ohne das Feld
     setzt einen laufenden Wert NICHT zurueck.
  D. Die dict-Form des Kerns (`bot_als_dict` / `bot_aus_dict`) traegt die Gunst hin und zurueck.
  E. Quellwache: die Ansicht rechnet nicht selbst - keine Grenze, kein Vergleich, nur der Aufruf der
     gemeinsamen Funktion (Regel F-04).
  F. Die Gunst aendert nichts anderes: nur das Feld selbst.
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['diplomatie', 'main:*', 'punkte']
PRUEF_DATEN = ['diplomatie.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import ast
import inspect
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

import_src()
import diplomatie as D


def _code(funktion) -> str:
    """Quelltext einer Funktion OHNE Docstring - Docstrings zaehlen nicht als Code."""
    baum = ast.parse(textwrap.dedent(inspect.getsource(funktion)))  # Funktion in einen Baum wandeln
    kopf = baum.body[0]  # der FunctionDef-Knoten
    if kopf.body and isinstance(kopf.body[0], ast.Expr) and isinstance(kopf.body[0].value, ast.Constant):
        kopf.body = kopf.body[1:]  # einen fuehrenden Docstring abschneiden
    return ast.unparse(baum)  # Rest als Text


abschnitt("A. Grenzen und Status an ihren Raendern")
check("Kleinstwert -5 wird zu 0", D.klemmen(-5) == 0, str(D.klemmen(-5)))
check("0 bleibt 0", D.klemmen(0) == 0, str(D.klemmen(0)))
check("50 bleibt 50", D.klemmen(50) == 50, str(D.klemmen(50)))
check("100 bleibt 100", D.klemmen(100) == 100, str(D.klemmen(100)))
check("130 wird zu 100", D.klemmen(130) == 100, str(D.klemmen(130)))
check("Unbrauchbares (True) faellt auf die Untergrenze", D.klemmen(True) == 0, str(D.klemmen(True)))
check("Status 0 ist feindselig", D.status(0) == "feindselig", D.status(0))
check("Status 39 ist feindselig", D.status(39) == "feindselig", D.status(39))
check("Status 40 ist wachsam", D.status(40) == "wachsam", D.status(40))
check("Status 59 ist wachsam", D.status(59) == "wachsam", D.status(59))
check("Status 60 ist freundlich", D.status(60) == "freundlich", D.status(60))
check("Status 100 ist freundlich", D.status(100) == "freundlich", D.status(100))

abschnitt("B. Die Zahlen kommen aus der Datendatei (A-7)")
datei = D.daten()  # die echte Projektdatei lesen
check("data/diplomatie.json ist lesbar", isinstance(datei, dict) and bool(datei), str(list(datei)[:4]))
check("Schalter aktiv ist gesetzt", D.aktiv(datei) is True, str(datei.get("aktiv")))
check("Startwert 50 kommt aus der Datei", D.startwert(datei) == int(datei["gunst"]["start"]),
      str(D.startwert(datei)))
eigene = {"aktiv": True,
          "gunst": {"min": 0, "max": 100, "start": 50,
                    "status": [{"bis": 20, "schluessel": "a", "text": "a"},
                               {"bis": 90, "schluessel": "b", "text": "b"},
                               {"bis": 100, "schluessel": "c", "text": "c"}]}}
check("geaenderte Grenzen in den Daten aendern den Status (20 -> a, 21 -> b)",
      D.status(20, eigene) == "a" and D.status(21, eigene) == "b",
      f"{D.status(20, eigene)} / {D.status(21, eigene)}")
check("ohne Stufen gibt es kein erfundenes Wort", D.status(50, {"gunst": {"min": 0, "max": 100}}) == "",
      repr(D.status(50, {"gunst": {"min": 0, "max": 100}})))
check("ausgeschalteter Schalter meldet False", D.aktiv({"aktiv": False}) is False)

abschnitt("C. Alter Spielstand ohne Feld")
import main  # erst hier importieren: die Oberflaeche zieht tkinter mit
bot = main.BotPlayer(name="Testbot", faction="Mensch", aggression=0.5, trading=0.5)  # neuer Bot
check("neuer Bot startet mit dem Startwert aus der Datei", bot.gunst == D.startwert(), str(bot.gunst))
bot.gunst = 71  # ein laufender Wert
main.GameState.bot_aus_dict(object(), bot, {"angriffe": 1})  # Rueckschreiben OHNE das Feld
check("Rueckschreiben ohne das Feld laesst 71 stehen", bot.gunst == 71, str(bot.gunst))
main.GameState.bot_aus_dict(object(), bot, {"gunst": 130})  # Rueckschreiben MIT zu grossem Wert
check("Rueckschreiben mit 130 klemmt auf 100", bot.gunst == 100, str(bot.gunst))

abschnitt("D. Die dict-Form des Kerns traegt die Gunst")
bot.gunst = 33  # Wert setzen
daten = main.GameState.bot_als_dict(object(), bot)  # hin
check("bot_als_dict enthaelt die Gunst", daten.get("gunst") == 33, str(daten.get("gunst")))
main.GameState.bot_aus_dict(object(), bot, daten)  # und zurueck
check("Rundlauf hin und zurueck ergibt denselben Wert", bot.gunst == 33, str(bot.gunst))
check("die dict-Form enthaelt KEINEN Status (nichts wird doppelt gespeichert)",
      "status" not in daten, str(sorted(k for k in daten if "status" in k)))

abschnitt("E. Quellwache: die Ansicht rechnet nicht selbst")
quelle = _code(main.NebelseetalApp._render_diplomacy)  # Code ohne Docstring
check("die Ansicht ruft diplomatie.status auf", "diplomatie.status(" in quelle, "Aufruf vorhanden")
check("keine Statusgrenze 39 in der Ansicht", "39" not in quelle, "kein 39")
check("keine Statusgrenze 40 in der Ansicht", "40" not in quelle, "kein 40")
check("keine Statusgrenze 59 in der Ansicht", "59" not in quelle, "kein 59")
check("keine Statusgrenze 60 in der Ansicht", "60" not in quelle, "kein 60")
check("kein Vergleich auf die Gunst in der Ansicht", "gunst" not in quelle.replace("bot.gunst", ""),
      "nur das Feld wird gelesen")
modul = _code(D.status)  # der Kern
check("der Kern enthaelt keine Grenze als Zahl", not any(z in modul for z in ("39", "59")),
      "Grenzen stehen in der Datei")

abschnitt("F. Die Gunst aendert nichts anderes")
probe = {"id": "x", "punkte": 5, "angriffe": 2}  # fremde Felder in der dict-Form
D.gunst_aendern(probe, 15)  # Gunst erhoehen
check("nur das Feld gunst entsteht", sorted(probe) == ["angriffe", "gunst", "id", "punkte"], str(sorted(probe)))
check("fremde Felder bleiben unveraendert", probe["punkte"] == 5 and probe["angriffe"] == 2, str(probe))

bericht()
