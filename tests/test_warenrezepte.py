"""
Warenrezepte — die eingefrorene Ableitung aus data/warenrezepte.json (Pilotrezepte, Schritt 4).

Beweist, dass tools/warenrezepte_ableiten.py GENAU die im Entwurf beschriebenen Rezepte
erzeugt hat und dass sie als Datendatei unveraendert vorliegen:
  * eine Rezeptangabe je Ware aus data/items.json["waren"],
  * die belegte Schwertdauer (20 Minuten) bleibt unangetastet,
  * der kombinierte Voraussetzungsfall ist vollstaendig zerlegt,
  * eine ungeklaerte Voraussetzung wirft wirklich ValueError.

Aufruf:  python -X utf8 tests/test_warenrezepte.py
"""
from __future__ import annotations

import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, befund, bericht, check, import_src

ROOT, SRC = import_src()
import spieldaten        # noqa: E402
import spieloekonomie    # noqa: E402
import werkstatt         # noqa: E402

_TOOLS = os.path.join(ROOT, "tools")
for _p in (SRC, _TOOLS):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import warenrezepte_ableiten as W     # noqa: E402  (Werkzeug: nur lesen)


# ==========================================================================
# 1. Die Datendatei deckt genau dieselben Waren ab wie items.json
# ==========================================================================

abschnitt("Datengrundlage — data/warenrezepte.json gegen data/items.json['waren']")

_waren = spieldaten.waren()
_pfad = os.path.join(ROOT, "data", "warenrezepte.json")
_rezepte = json.load(open(_pfad, encoding="utf-8"))

check("data/warenrezepte.json ist vorhanden", os.path.exists(_pfad), _pfad)
check(f"die Datendatei hat GENAU die {len(_waren)} Warenschluessel aus items.json",
      set(_rezepte) == set(_waren),
      f"{len(_rezepte)} Schluessel: {sorted(set(_rezepte) ^ set(_waren)) or 'Deckung gleich'}")
check("die Anzahl der Rezepte stimmt (17 Waren)",
      len(_rezepte) == len(_waren) == 17, f"{len(_rezepte)} Rezepte / {len(_waren)} Waren")

check("data/items.json wurde nicht veraendert (17 Waren, bekannte Quelle)",
      len(_waren) == 17 and "ORIGINAL_Einheiten_Waren_Rohstoffe.md" in
      json.load(open(os.path.join(ROOT, "data", "items.json"), encoding="utf-8"))["_quelle"])


# ==========================================================================
# 2. Aufbau jedes Eintrags
# ==========================================================================

abschnitt("Jeder Eintrag — kosten, dauer, voraussetzungen, _herkunft")

_felder = ("kosten", "dauer", "voraussetzungen", "_herkunft")
check("jeder Eintrag hat genau die vier Schluessel kosten/dauer/voraussetzungen/_herkunft",
      all(set(r) == set(_felder) for r in _rezepte.values()),
      str({n: sorted(r) for n, r in _rezepte.items() if set(r) != set(_felder)}))
check("_herkunft nennt ausdruecklich VORSCHLAG",
      all("VORSCHLAG" in r["_herkunft"] for r in _rezepte.values()),
      str({n: r["_herkunft"] for n, r in _rezepte.items() if "VORSCHLAG" not in r["_herkunft"]}))


# ==========================================================================
# 3. Die belegte Dauer bleibt unveraendert
# ==========================================================================

abschnitt("Belegte Dauer — das Schwert bleibt bei 20 Minuten (1200 s)")

check("src/werkstatt.py kennt genau eine belegte Dauer: Schwert 1200 s",
      werkstatt.BELEGTE_DAUER_SEKUNDEN == {"Schwert": 1200},
      str(werkstatt.BELEGTE_DAUER_SEKUNDEN))
check("die Datendatei uebernimmt die Schwertdauer unveraendert (1200 s)",
      _rezepte["Schwert"]["dauer"] == 1200, str(_rezepte["Schwert"]["dauer"]))
check("das abgeleitete Rezept liefert dieselbe Schwertdauer wie die Quelle",
      W.pilotrezept("Schwert")["dauer"] == werkstatt.BELEGTE_DAUER_SEKUNDEN["Schwert"],
      f"{W.pilotrezept('Schwert')['dauer']} gegen {werkstatt.BELEGTE_DAUER_SEKUNDEN['Schwert']}")


# ==========================================================================
# 4. Die drei namentlich zugesagten Rezepte
# ==========================================================================

abschnitt("Einzelrezepte — Wollumhang, Kurzschwert, Lederrüstung")

check("Wollumhang: kosten == {'wolle': 1} und dauer == 1200",
      _rezepte["Wollumhang"]["kosten"] == {"wolle": 1} and _rezepte["Wollumhang"]["dauer"] == 1200,
      f"{_rezepte['Wollumhang']}")
check("Kurzschwert: kosten == {'metall': 4} und dauer == 4800 (80 Minuten)",
      _rezepte["Kurzschwert"]["kosten"] == {"metall": 4}
      and _rezepte["Kurzschwert"]["dauer"] == 4800,
      f"{_rezepte['Kurzschwert']}")
check("Lederrüstung: kosten == {'leder': 4} und dauer == 4800",
      _rezepte["Lederrüstung"]["kosten"] == {"leder": 4}
      and _rezepte["Lederrüstung"]["dauer"] == 4800,
      f"{_rezepte['Lederrüstung']}")


# ==========================================================================
# 5. Kombinierte Voraussetzungen sind vollstaendig
# ==========================================================================

abschnitt("Kombinierte Voraussetzungen — kein '+' geht verloren")

_kombiniert = {n: e["voraussetzung"] for n, e in _waren.items() if "+" in e["voraussetzung"]}
check("es gibt Waren mit kombinierter Voraussetzung (mindestens Lederrüstung)",
      len(_kombiniert) >= 1, str(_kombiniert))

for name, text in _kombiniert.items():
    teile = len(text.split("+"))
    check(f"{name}: {teile} '+'-Teile -> {teile} Schluessel in voraussetzungen",
          len(_rezepte[name]["voraussetzungen"]) == teile,
          f"text {text!r} -> {_rezepte[name]['voraussetzungen']}")

# Woertliches Beispiel mit Werten:
check("Beispiel Lederrüstung woertlich: 'Nähkunst 1 + Rüstungsbau 2' -> "
      "{'Nähkunst': 1, 'Rüstungsbau': 2}",
      _waren["Lederrüstung"]["voraussetzung"] == "Nähkunst 1 + Rüstungsbau 2"
      and _rezepte["Lederrüstung"]["voraussetzungen"] == {"Nähkunst": 1, "Rüstungsbau": 2},
      f"{_waren['Lederrüstung']['voraussetzung']!r} -> {_rezepte['Lederrüstung']['voraussetzungen']}")

# Ein 'keine'-Fall darf keine Voraussetzung erfinden.
_keine = {n for n, e in _waren.items() if e["voraussetzung"] == "keine"}
check("Waren mit Voraussetzung 'keine' bekommen leere voraussetzungen",
      all(_rezepte[n]["voraussetzungen"] == {} for n in _keine),
      f"{sorted(_keine)}: {[(_rezepte[n]['voraussetzungen']) for n in sorted(_keine)]}")

_forschungsschlüssel = set(spieldaten.forschungen())
check("alle genannten Voraussetzungsnamen sind echte Forschungen aus research.json",
      all(set(r["voraussetzungen"]) <= _forschungsschlüssel for r in _rezepte.values()),
      str({n: sorted(set(r['voraussetzungen']) - _forschungsschlüssel)
           for n, r in _rezepte.items() if set(r['voraussetzungen']) - _forschungsschlüssel}))


# ==========================================================================
# 6. Materialmenge: immer >= 1 und ganzzahlig
# ==========================================================================

abschnitt("Materialmenge — kein 0-Rezept, immer ganzzahlig")

check("jede Kostenangabe hat genau einen Rohstoff",
      all(len(r["kosten"]) == 1 for r in _rezepte.values()),
      str({n: r["kosten"] for n, r in _rezepte.items() if len(r["kosten"]) != 1}))
check("jede Materialmenge ist >= 1",
      all(min(r["kosten"].values()) >= 1 for r in _rezepte.values()),
      str({n: r["kosten"] for n, r in _rezepte.items() if min(r["kosten"].values()) < 1}))
check("jede Materialmenge ist ganzzahlig (keine Rundungsreste)",
      all(isinstance(v, int) and v == int(v)
          for r in _rezepte.values() for v in r["kosten"].values()),
      str({n: r["kosten"] for n, r in _rezepte.items()
           if any(not isinstance(v, int) for v in r["kosten"].values())}))
check("die Menge ist der aufgerundete Normertrag waehrend der Dauer",
      all(r["kosten"][k] == math.ceil(spieloekonomie.einzelmaximum()[k] * r["dauer"] / 3600)
          for r in _rezepte.values() for k in r["kosten"]),
      "Stichprobe Schwert "
      + str(_rezepte["Schwert"]["dauer"] and spieloekonomie.einzelmaximum()["metall"]))


# ==========================================================================
# 7. Die eingefrorene Datei entspricht der frischen Ableitung
# ==========================================================================

abschnitt("Eingefrorene Datei — gleich der frischen Ableitung (nur Daten, kein Neurechnen im Spiel)")

_frisch = W.rezepte_ableiten()
check("data/warenrezepte.json stimmt Stueck fuer Stueck mit der frischen Ableitung ueberein",
      _frisch == _rezepte,
      str({n: (r, _rezepte.get(n)) for n, r in _frisch.items() if _rezepte.get(n) != r}))


# ==========================================================================
# 8. Ungeklaerte Voraussetzung wirft wirklich ValueError
# ==========================================================================

abschnitt("Ungeklaerte Voraussetzung — kuenstlicher Fall, items.json bleibt unberuehrt")

_kuenstlich = {"Erfundene Ware": {"voraussetzung": "Zauberkunst 2"}}


def _erwarte_valueerror():
    try:
        W.warenforderungen("Erfundene Ware", _kuenstlich)
    except ValueError as e:
        check("eine erfundene Forschung wirft ValueError", True, str(e))
        return
    check("eine erfundene Forschung wirft ValueError", False,
          "kein ValueError fuer 'Zauberkunst 2'")


_erwarte_valueerror()


def _erwarte_valueerror_unlesbar():
    kaputt = {"Erfundene Ware": {"voraussetzung": "NurGeschwafel"}}
    try:
        W.warenforderungen("Erfundene Ware", kaputt)
    except ValueError as e:
        check("eine unlesbare Voraussetzung (ohne Stufenzahl) wirft ebenfalls ValueError",
              True, str(e))
        return
    check("eine unlesbare Voraussetzung (ohne Stufenzahl) wirft ebenfalls ValueError",
          False, "kein ValueError fuer 'NurGeschwafel'")


_erwarte_valueerror_unlesbar()

check("data/items.json wurde wirklich nicht angefasst (unveraendert 17 Waren)",
      len(spieldaten.waren()) == 17 and len(_waren) == 17)


sys.exit(bericht())
