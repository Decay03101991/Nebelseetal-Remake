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
2. Der Spielstand auf DIESEM Rechner traegt die Botschaft: Art `geschenk`, Zeitmarke vorhanden, Text
   nennt Absender, Spieltag und Betraege.
3. Die Botschaft LUEGT NICHT - geprueft wird gegen den **Schnappschuss von der Schenkung**
   (`~/.nebelseetal/archiv/SPIELBASIS_*.json`), NICHT gegen das heutige Lager. Grund (belegt
   31.10.2026): die erste Fassung verglich mit dem Live-Lager; sobald Daniel spielte und baute, sank
   der Bestand und die Pruefung wurde rot - sie mass den Spielverlauf, nicht die Botschaft.
4. Die Erzaehlung haengt an belegten Namen (Midgard, Portal, Nebelsee), nicht an erfundenen Welten.

Aufruf:  python -X utf8 tests/test_geschenk_nachricht.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['forschung', 'kampf', 'main:*']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import json
import os
import pathlib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import main  # noqa: E402

SLOT = pathlib.Path.home() / ".nebelseetal" / "savegame_slot1.json"
ARCHIV = pathlib.Path.home() / ".nebelseetal" / "archiv"


def _zahl(text: str) -> float:
    """'2.000.000' -> 2000000.0 (deutsche Tausenderpunkte)."""
    return float(text.replace(".", "").replace(",", "."))


def _schnappschuss() -> dict:
    """Die Aufnahme von der Schenkung: Tag und Ortslager unmittelbar danach."""
    for pfad in sorted(ARCHIV.glob("SPIELBASIS_*.json"), reverse=True):
        try:
            roh = json.loads(pfad.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if roh.get("vorraete"):
            return {"tag": roh.get("tag"),
                    "vorraete": {str(k).lower(): float(v) for k, v in roh["vorraete"].items()},
                    "waren": roh.get("waren"), "datei": pfad.name}
    return {}


# ------------------------------------------------------ 1. Farbe in der Ansicht
print("\n=== 1. Eine pruefbare Farbregel fuer die Nachrichtenansicht ===")
check("Kampf ist rot", main.nachrichten_farbe({"type": "kampf"}) == "#e53935")
check("Schenkung ist hellblau", main.nachrichten_farbe({"type": "geschenk"}) == "#7FD1FF")
check("alles andere bleibt gold", main.nachrichten_farbe({"type": "forschung"}) == "#DAA520")
check("ohne Art bleibt gold", main.nachrichten_farbe({}) == "#DAA520")
check("None stuerzt nicht ab", main.nachrichten_farbe(None) == "#DAA520")
import inspect  # noqa: E402
quelle = inspect.getsource(main)
check("die Ansicht nutzt die Funktion (keine zweite Farbregel im Code)",
      "color = nachrichten_farbe(msg)" in quelle)

# ------------------------------------------------- 2. Die Botschaft im Spielstand
print("\n=== 2. Die Botschaft in einem lokalen Spielstand ===")
# WARUM ALLE SLOTS UND NICHT NUR SLOT 1 (geaendert 08.11.2026): diese Pruefung hing an EINEM Slot,
# den Daniel beim Spielen ueberschreibt. Beim Spieltest 1 passierte genau das - Slot 1 bekam um
# 12:56 einen Stand ohne die Botschaft, und die Pruefung wurde ROT, obwohl am Code nichts kaputt
# war (die Schenkung wurde am 31.10.2026 einmalig eingespielt; nichts im Code erzeugt sie neu).
# Ein Nachweis darf nicht rot werden, weil jemand spielt.
SPEICHER = pathlib.Path.home() / ".nebelseetal"
KANDIDATEN = sorted(SPEICHER.glob("savegame_slot*.json")) + [SLOT]
daten, botschaften, quelle_datei = {}, [], ""
for pfad in KANDIDATEN:
    if not pfad.exists() or botschaften:
        continue
    try:
        roh = json.loads(pfad.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        continue
    treffer = [m for m in (roh.get("messages") or []) if m.get("type") == "geschenk"]
    if treffer:
        daten, botschaften, quelle_datei = roh, treffer, pfad.name

if not botschaften:
    befund("KEIN lokaler Spielstand traegt die Schenkungs-Botschaft mehr - der Nachweis am echten "
           "Stand fehlt (der Code ist davon unberuehrt, die Farb- und Regelpruefungen oben laufen). "
           "Ursache, belegt: Daniel hat beim Spieltest 1 am 08.11.2026 um 12:56 Slot 1 mit einem "
           "Stand ohne diese Botschaft ueberschrieben; die Schenkung wurde am 31.10.2026 EINMALIG "
           "eingespielt, und kein Code erzeugt sie neu. Fuer den vollen Nachweis braucht es einen "
           "Stand mit der Botschaft (Archivkopie oder neue Einspielung).", "")
    sys.exit(bericht())

check("die Botschaft liegt in einem lokalen Spielstand (%s)" % quelle_datei, bool(botschaften),
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
    check("kein erfundener Weltname",
          all(w not in text for w in ("Avalon", "Narnia", "Zephyria")))

    print("\n=== 3. Die Botschaft luegt nicht: Betraege gegen den Stand BEI DER SCHENKUNG ===")
    schnapp = _schnappschuss()
    if not schnapp:
        befund("kein Schnappschuss der Schenkung gefunden (SPIELBASIS_*.json fehlt)", "")
        sys.exit(bericht())
    check("Schnappschuss der Schenkung gefunden", bool(schnapp), schnapp.get("datei", ""))
    lager = schnapp["vorraete"]
    check("genannter Spieltag == Spieltag bei der Schenkung (%s)" % schnapp.get("tag"),
          ("%s. Spieltag" % schnapp.get("tag")) in text, text[-60:])
    versprochen = {
        "holz": "2.000.000 Holz", "stein": "1.000.000 Stein", "metall": "500.000 Metall",
        "gold": "500.000 Gold", "nahrung": "500.000 Nahrung", "wolle": "200.000 Wolle",
        "leder": "200.000 Leder", "mana": "200.000 Mana", "pferde": "20.000 Pferde",
    }
    for stoff, satz in versprochen.items():
        betrag = _zahl(satz.split()[0])
        check("%s: Text nennt %.0f, Schenkung hatte %.0f" % (stoff, betrag, lager.get(stoff, 0)),
              (satz in text) and lager.get(stoff, 0) >= betrag,
              "Lager %.2f" % lager.get(stoff, 0))
    check("Forschung: 1.074.150 Holz fuer alle 21 Gebiete stehen im Text", "1.074.150" in text)
    check("das geschenkte Holz deckt die Forschung (>= 1.074.150)", lager.get("holz", 0) >= 1074150)
    check("die Schenkung umfasste alle 17 Werkstattwaren", int(schnapp.get("waren") or 0) >= 17,
          "Arten: %s" % schnapp.get("waren"))

    heute = {k.lower(): float(v) for k, v in
             ((daten.get("settlements") or [{}])[0].get("vorraete") or {}).items()}
    abweichung = {k: round(heute.get(k, 0) - v, 1) for k, v in lager.items()
                  if abs(heute.get(k, 0) - v) > 1}
    if abweichung:
        befund("heutiges Lager weicht von der Schenkung ab (gespielt/gebaut): "
               + ", ".join("%s %+.0f" % (k, v) for k, v in sorted(abweichung.items())), "")

sys.exit(bericht())
