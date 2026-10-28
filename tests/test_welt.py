"""Pruefung der Weltkarte des Limbus (data/welten.json, src/welt.py)."""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, befund, check, import_src

ROOT, SRC = import_src()
import welt as W

with open(os.path.join(ROOT, "data", "welten.json"), encoding="utf-8") as _f:
    _roh = json.load(_f)

DIM = W.dimensionen()
WELTNAMEN = ["Armageddon", "Ragnaroek", "Utgard", "Midgard", "Valhalla", "Limbus"]

abschnitt("Datei — Aufbau")
check("genau 20 Dimensionen", len(DIM) == 20, str(len(DIM)))
check("jede Dimension hat kennung, name, x, y und welt",
      all({"kennung", "name", "x", "y", "welt"} <= set(d) for d in DIM))
check("x liegt zwischen 0 und 9", all(0 <= d["x"] <= 9 for d in DIM))
check("y liegt zwischen 0 und 9", all(0 <= d["y"] <= 9 for d in DIM))
check("alle Kennungen sind verschieden", len({d["kennung"] for d in DIM}) == len(DIM))
check("keine zwei Dimensionen teilen denselben Punkt",
      len({(d["x"], d["y"]) for d in DIM}) == len(DIM))

abschnitt("Datei — Belege und Vorschlaege sind gekennzeichnet")
check("die Datei nennt Quellen", bool(_roh.get("_quelle")))
check("belegte Angaben sind als _belegt gelistet", bool(_roh.get("_belegt")))
check("nicht belegte Angaben sind als _nicht_belegt gelistet", bool(_roh.get("_nicht_belegt")))
check("die Portalkostenregel traegt einen _vorschlag-Hinweis",
      bool(_roh["portalregel"].get("_vorschlag")))
check("die Portalkostenregel traegt einen _belegt-Hinweis",
      bool(_roh["portalregel"].get("_belegt")))
check("die sechs Weltnamen sind in welten_belegt aufgelistet",
      set(_roh["welten_belegt"]) == set(WELTNAMEN), str(_roh.get("welten_belegt")))
check("jede Dimension nennt ihren _vorschlag oder _belegt",
      all(d.get("_vorschlag") or d.get("_belegt") for d in DIM))

abschnitt("Weltnamen — die sechs belegten Welten")
for name in WELTNAMEN:
    anzahl = sum(1 for d in DIM if d.get("welt") == name)
    check(f"{name} liegt in genau einer Dimension", anzahl == 1, f"{anzahl}x")
check("welten() liefert genau sechs Dimensionen", len(W.welten()) == 6, str(len(W.welten())))
check("welten() liefert nur Dimensionen mit Weltnamen",
      all(d.get("welt") for d in W.welten()))
check("der Anzeigename der belegten Welt stimmt mit dem Weltnamen",
      all(d["name"] == d["welt"] for d in W.welten()))

abschnitt("Entfernung")
check("Entfernung zu sich selbst ist 0",
      all(W.entfernung(d["kennung"], d["kennung"]) == 0 for d in DIM))
check("Entfernung ist symmetrisch",
      all(W.entfernung(a["kennung"], b["kennung"]) == W.entfernung(b["kennung"], a["kennung"])
          for a in DIM for b in DIM))
check("Entfernung ist nie negativ",
      all(W.entfernung(a["kennung"], b["kennung"]) >= 0 for a in DIM for b in DIM))
check("Entfernung akzeptiert auch den Anzeigenamen",
      W.entfernung("Armageddon", "d01") == 0,
      str(W.entfernung("Armageddon", "d01")))

abschnitt("Portalkosten")
grund = _roh["portalregel"]["grundbetrag"]
check("Portalkosten zu sich selbst sind der Grundbetrag",
      all(W.portalkosten(d["kennung"], d["kennung"]) == grund for d in DIM),
      f"Grundbetrag {grund}")
check("Portalkosten sind nie negativ",
      all(W.portalkosten(a["kennung"], b["kennung"]) >= 0 for a in DIM for b in DIM))

_kosten_je_entfernung: dict = {}
for d in DIM:
    e = W.entfernung("d01", d["kennung"])
    _kosten_je_entfernung.setdefault(e, set()).add(W.portalkosten("d01", d["kennung"]))
check("gleiche Entfernung ergibt gleiche Kosten",
      all(len(v) == 1 for v in _kosten_je_entfernung.values()),
      str({e: sorted(v) for e, v in _kosten_je_entfernung.items()}))
_kosten = [next(iter(_kosten_je_entfernung[e])) for e in sorted(_kosten_je_entfernung)]
check("Portalkosten steigen mit der Entfernung",
      all(_kosten[i] < _kosten[i + 1] for i in range(len(_kosten) - 1)),
      str(_kosten))

abschnitt("Nachbarn")
n = W.nachbarn("d01", 4)
check("Nachbarn liegen im Umkreis", all(d["_entfernung"] <= 4 for d in n),
      str([d["_entfernung"] for d in n]))
check("Nachbarn sind nach Entfernung sortiert",
      [d["_entfernung"] for d in n] == sorted(d["_entfernung"] for d in n),
      str([d["_entfernung"] for d in n]))
check("Nachbarn enthalten die eigene Dimension nicht",
      all(d["kennung"] != "d01" for d in n))
check("Umkreis 0 ergibt keine Nachbarn", W.nachbarn("d01", 0) == [])
check("grosser Umkreis findet alle 19 anderen", len(W.nachbarn("d01", 99)) == 19,
      str(len(W.nachbarn("d01", 99))))

abschnitt("Unbekannte Kennungen — sauber gemeldet, kein Absturz")
check("entfernung(unbekannt) ist None", W.entfernung("gibtsnicht", "d01") is None)
check("portalkosten(unbekannt) ist None", W.portalkosten("d01", "gibtsnicht") is None)
check("nachbarn(unbekannt) ist leer", W.nachbarn("gibtsnicht", 5) == [])
_txt = W.beschreibung("gibtsnicht")
check("beschreibung(unbekannt) meldet unbekannt", "Unbekannt" in _txt, _txt)

abschnitt("Beschreibung")
_b = W.beschreibung("d02")
check("Beschreibung nennt den Namen", "Ragnaroek" in _b, _b)
check("Beschreibung nennt die Koordinaten", "x=" in _b and "y=" in _b, _b)
_b2 = W.beschreibung("d07")
check("Dimension ohne belegte Welt sagt das", "keine der sechs" in _b2, _b2)

sys.exit(bericht())
