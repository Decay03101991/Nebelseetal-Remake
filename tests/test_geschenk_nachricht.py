# -*- coding: ascii -*-
"""Die Schenkungs-Botschaft im Nachrichtenmenue (Daniel 31.10.2026).

Daniels Wunsch: "als einmalige schenkung vom spiel auch im nachrichtenslot darf eine nachricht zum
test auftauchen das mir das ein grosser Herrscher sinnvoll der Geschichte nachempfunden eine grosse
schenkung zukommen liess ... Einmal diese menge an Ressourcen als einmalige schenkung die diesem
Spielstand auch wirklich bleibt und dann die Gestaltung der Nachricht im bezug auf die
Nebelseetal geschichte."

Was diese Datei beweist
-----------------------
1. Die Nachrichtenansicht faerbt ueber EINE pruefbare Funktion (`main.nachrichten_farbe`):
   Kampf rot, Schenkung hellblau, alles andere Gold - keine Farbe im Zeichencode versteckt.
2. Der Spielstand auf DIESEM Rechner traegt die Botschaft: Art `geschenk`, Zeitmarke vorhanden,
   Text nennt Absender, Spieltag und Betraege.
3. Die Botschaft LUEGT NICHT: die genannten Mengen stehen wirklich im Ortslager - der Test
   vergleicht Text und Bestand, statt der Nachricht zu glauben.
4. Die Erzaehlung haengt an belegten Namen (Midgard, Portal, Nebelsee), nicht an erfundenen Welten.

Aufruf:  python -X utf8 tests/test_geschenk_nachricht.py
"""
from __future__ import annotations

import json
import os
import pathlib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import main  # noqa: E402

SLOT = pathlib.Path.home() / ".nebelseetal" / "savegame_slot1.json"


def _zahl(text: str) -> float:
    """'2.000.000' -> 2000000.0 (deutsche Tausenderpunkte)."""
    return float(text.replace(".", "").replace(",", "."))


# ------------------------------------------------------ 1. Farbe in der Ansicht
print("\n=== 1. Eine pruefbare Farbregel fuer die Nachrichtenansicht ===")
check("Kampf ist rot", main.nachrichten_farbe({"type": "kampf"}) == "#e53935")
check("Schenkung ist hellblau", main.nachrichten_farbe({"type": "geschenk"}) == "#7FD1FF")
check("alles andere bleibt gold", main.nachrichten_farbe({"type": "forschung"}) == "#DAA520")
check("ohne Art bleibt gold", main.nachrichten_farbe({}) == "#DAA520")
check("None stuerzt nicht ab", main.nachrichten_farbe(None) == "#DAA520")
quelle = main.__dict__["__loader__"].get_source("main") if hasattr(main.__dict__.get("__loader__"), "get_source") else ""
if not quelle:
    import inspect
    quelle = inspect.getsource(main)
check("die Ansicht nutzt die Funktion (keine zweite Farbregel im Code)",
      "color = nachrichten_farbe(msg)" in quelle)

# ------------------------------------------------- 2. Die Botschaft im Spielstand
print("\n=== 2. Die Botschaft in Daniels Spielstand (Slot 1) ===")
if not SLOT.exists():
    befund("Spielstand %s fehlt auf diesem Rechner - Botschaft kann nicht geprueft werden" % SLOT, "")
    sys.exit(bericht())

daten = json.loads(SLOT.read_text(encoding="utf-8"))
botschaften = [m for m in (daten.get("messages") or []) if m.get("type") == "geschenk"]
check("mindestens eine Botschaft der Art 'geschenk' liegt im Spielstand", bool(botschaften),
      "Arten: %s" % sorted({m.get("type") for m in (daten.get("messages") or [])}))
if botschaften:
    b = botschaften[-1]
    text = str(b.get("text") or "")
    check("Zeitmarke gesetzt (UTC und lokal)", bool(b.get("zeit_utc")) and bool(b.get("zeit_lokal")))
    check("Spielzeit-Sekunde gesetzt", isinstance(b.get("spielzeit_sekunden"), (int, float)))
    check("Absender ist der Hochkoenig von Midgard (belegte Welt)", "Midgard" in text)
    check("das Portal kommt vor (belegter Weg zwischen den Welten)", "Portal" in text)
    check("der Nebelsee kommt vor (Titel des Spiels)", "Nebelsee" in text)
    check("die Einmaligkeit steht ausdruecklich drin", "EINMALIG" in text.upper())
    spieltag = int(daten.get("day") or 0)
    check("der genannte Spieltag ist der echte Spieltag (%d)" % spieltag,
          ("%d. Spieltag" % spieltag) in text, text[-60:])

    # 3. Text gegen Bestand: die Botschaft darf nicht mehr versprechen, als da ist
    print("\n=== 3. Die Botschaft luegt nicht: Betraege gegen den Bestand ===")
    ort = (daten.get("settlements") or [{}])[0]
    lager = {k.lower(): float(v) for k, v in (ort.get("vorraete") or {}).items()}
    versprochen = {
        "holz": "2.000.000 Holz", "stein": "1.000.000 Stein", "metall": "500.000 Metall",
        "gold": "500.000 Gold", "nahrung": "500.000 Nahrung", "wolle": "200.000 Wolle",
        "leder": "200.000 Leder", "mana": "200.000 Mana", "pferde": "20.000 Pferde",
    }
    for stoff, satz in versprochen.items():
        if satz not in text:
            check("%s steht im Text" % stoff, False, satz)
            continue
        betrag = _zahl(satz.split()[0])
        check("%s: Text nennt %.0f, Lager hat %.0f" % (stoff, betrag, lager.get(stoff, 0)),
              lager.get(stoff, 0) >= betrag, "Lager %.2f" % lager.get(stoff, 0))
    waren = ort.get("waren") or {}
    check("Werkstattwaren sind aufgefuellt (mindestens 17 Arten)", len(waren) >= 17,
          "Arten: %d" % len(waren))
    check("je Ware mindestens 500 Stueck", all(float(n) >= 500 for n in waren.values()))
    check("Forschung: 1.074.150 Holz fuer alle 21 Gebiete stehen im Text",
          "1.074.150" in text)
    check("das Holz im Lager deckt die Forschung (>= 1.074.150)", lager.get("holz", 0) >= 1074150)

sys.exit(bericht())
