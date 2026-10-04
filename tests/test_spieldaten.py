"""Pruefung der Datenschicht: laedt sie die Originalzahlen vollstaendig und richtig?"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, befund, check, import_src

ROOT, SRC = import_src()
import spieldaten as S

abschnitt("Datenschicht — Bestand")
ue = S.uebersicht()
check("28 Einheiten", ue["einheiten"] == 28, str(ue["einheiten"]))
check("17 Waren", ue["waren"] == 17, str(ue["waren"]))
check("21 Forschungen", ue["forschungen"] == 21, str(ue["forschungen"]))
check("9 Rohstoffe", ue["rohstoffe"] == 9, str(ue["rohstoffe"]))
check("20 Gebaeude", ue["gebaeude"] == 20, str(ue["gebaeude"]))
check("10 Wallstufen", ue["wallstufen"] == 10, str(ue["wallstufen"]))

abschnitt("Datenschicht — Pflichtangaben vollstaendig")
ohne_kosten = [n for n in S.einheiten() if not S.kosten(n) and not S.benoetigte_waren(n)]
check("jede Einheit hat Kosten oder Waren", not ohne_kosten, ", ".join(ohne_kosten))
ohne_icon = [n for n in S.einheiten() if S.icon_pfad(n) is None]
check("jede Einheit hat eine vorhandene Icon-Datei", not ohne_icon, ", ".join(ohne_icon))
waren_ohne_icon = [n for n in S.waren() if S.icon_pfad(n) is None]
check("jede Ware hat eine vorhandene Icon-Datei", not waren_ohne_icon, ", ".join(waren_ohne_icon))
ohne_warenbezug = [n for n, e in S.waren().items() if not e.get("benoetigt_von")]
if ohne_warenbezug:
    befund(f"{len(ohne_warenbezug)} Waren werden von keiner Einheit verlangt",
           ", ".join(ohne_warenbezug))
else:
    check("jede Ware wird von mindestens einer Einheit verlangt", True, f"{len(S.waren())} Waren")

abschnitt("Datenschicht — Originalwerte stimmen (Stichproben aus dem Handbuch)")
for name, feld, soll in [("Bürgerwehr", "LE", 15), ("Paladin", "AT", 85), ("Katapult", "TP_max", 13),
                         ("Großes Katapult", "SK", 55), ("Streuner", "GS", 10),
                         ("Waldläufer", "GS", 35), ("Ramme", "SK", 25)]:
    ist = S.wert(name, feld)
    check(f"{name}.{feld} = {soll}", ist == soll, f"gefunden {ist}")

abschnitt("Datenschicht — Luecken sind ausgewiesen, nicht gefuellt")
luecken = S.luecken()
check("13 Einheiten mit Luecken (Karren/Belagerung)", len(luecken) == 13, str(len(luecken)))
check("MU fehlt genau bei diesen 13",
      all("MU" in felder for felder in luecken.values()) and len(luecken) == 13)
check("Kampfeinheiten haben KEINE Luecken",
      not any(n in luecken for n in
              ["Bürgerwehr", "Kämpfer", "Krieger", "Ritter", "Paladin",
               "Kurzbogenschütze", "Bogenschütze", "Langbogenschütze", "Armbrustschütze"]))

abschnitt("Datenschicht — Originalregeln")
check("Forschungsdauer Stufe 3 = 9 Stunden", S.forschungsdauer_stunden(3) == 9)
check("Forschungsdauer Stufe 5 = 25 Stunden", S.forschungsdauer_stunden(5) == 25)
check("Verteidigung Stufe 4 = 64 Kriegspunkte", S.kriegspunkte_verteidigung(4) == 64)
w = S.wallstufen()
check("Wallstufe 10 = Bollwerk 1000/1000",
      w[9]["name"] == "Bollwerk" and w[9]["schwellenwert_fussttruppen"] == 1000
      and w[9]["schwellenwert_belagerungswaffen"] == 1000)
check("Stufen 1-4 ohne Belagerungsschwelle",
      all(x["schwellenwert_belagerungswaffen"] is None for x in w[:4]))

abschnitt("Datenschicht — Kategorien")
kat = S.einheiten_nach_kategorie()
erwartet = {"Nahkampf": 5, "Fernkampf": 4, "Kundschafter": 6, "Karren": 6, "Belagerung": 7}
for k, n in erwartet.items():
    check(f"{k}: {n} Einheiten", len(kat.get(k, [])) == n, f"{len(kat.get(k, []))} gefunden")

abschnitt("Rohstoffliste des Spiels = die 9 Originalrohstoffe (W4a)")
import main as _main

_soll = [r["id"] for r in S.rohstoffe()]
check("das Spiel kennt genau die 9 Originalrohstoffe", _main.RESOURCES == _soll,
      f"Spiel: {_main.RESOURCES} | Original: {_soll}")
check("keine erfundenen Rohstoffe mehr",
      not (set(_main.RESOURCES) & {"kristall", "stoff", "geld", "wissen", "eisen"}),
      str(sorted(set(_main.RESOURCES) & {"kristall", "stoff", "geld", "wissen", "eisen"})))

_start = _main.GameState()
check("Startwerte des Handbuchs Seite 7 (100 Holz, 100 Stein, 10 Siedler)",
      _start.resources["holz"].amount == 100 and _start.resources["stein"].amount == 100
      and _start.population == 10.0,
      f"Holz {_start.resources['holz'].amount}, Stein {_start.resources['stein'].amount}, "
      f"Siedler {_start.population}")

_kostenfelder = set()
for _u in _main.UNITS.values():
    _kostenfelder |= set(_u.cost) - {"siedler"}     # Siedler zahlt die Bevoelkerung
check("jede Einheit bezahlt nur bekannte Rohstoffe",
      _kostenfelder <= set(_main.RESOURCES), str(sorted(_kostenfelder - set(_main.RESOURCES))))

_waren_felder = set()
for _w in _main.GOODS.values():
    _waren_felder |= set(_w.base_cost)
check("jede Ware kostet nur bekannte Rohstoffe",
      _waren_felder <= set(_main.RESOURCES), str(sorted(_waren_felder - set(_main.RESOURCES))))

abschnitt("Forschungskosten nach Handbuch Seite 13")
_reihe = [S.forschungs_kosten(n)["holz"] for n in (1, 2, 3, 4)]
check("Stufen 1-4 kosten 50, 100, 200, 400 Holz", _reihe == [50, 100, 200, 400], str(_reihe))
check("Stufe 5 kostet 800 Holz (Verdopplung geht weiter)", S.forschungs_kosten(5)["holz"] == 800)
check("Grundbetrag ist als Konstante belegt", S.FORSCHUNG_GRUNDKOSTEN_HOLZ == 50)
check("Stufe 0 kostet nichts", S.forschungs_kosten(0) == {})
check("die Kostenzahl steht auch in data/research.json",
      "50 Holz" in S.forschungsregeln().get("kosten", ""), S.forschungsregeln().get("kosten"))

sys.exit(bericht())
