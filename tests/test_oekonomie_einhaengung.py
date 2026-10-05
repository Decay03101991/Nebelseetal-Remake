# -*- coding: ascii -*-
"""Pruefung der main-Anbindung des Oekonomie-Pakets (Entwurf Schritt 9, Z. 755-789).

Dies ist die Wache des ERSTEN Teils: die Felder einer lokalen Wirtschaft in der
`Settlement`-Dataclass, die stabile Ort-Kennung und der Spielstand. Geprueft werden sechs Zusagen:

  P0  Alle fuenfzehn Felder aus Entwurf Z. 757-772 sind da und haben die dokumentierten Vorgaben.
  P1  `main.siedlung_kennung` haengt an Besitzer und Weltfeld, nie am Namen - und
      `_found_settlement` vergibt sie wirklich (Quelltextpruefung).
  P2  Speichern und Laden tragen ALLE neuen Felder (Rundlauf mit echten Werten).
  P3  Ein ALTSPIELSTAND ohne die neuen Felder laedt weiter und bekommt seine Kennung.
  P4  Die Kennung ueberlebt ein Umbenennen (sie wird beim Laden NICHT aus dem Namen gebaut).
  P5  Bis zur Aktivierung (Schritt 10) entsteht KEINE zweite fuehrende Wahrheit: die lokalen
      Felder starten leer, das Spiel rechnet weiter mit den globalen Bestaenden.

Aufruf:
    python -X utf8 tests/test_oekonomie_einhaengung.py
"""
from __future__ import annotations

import dataclasses
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src, projektwurzel  # noqa: E402

ROOT, SRC = import_src()
import main as M  # noqa: E402

ST = M.Settlement

# Name: Vorgabewert
NEU: dict = {
    "id": "",
    "besitzer": "spieler",
    "dimension": 1,
    "vorraete": {},
    "waren": {},
    "einheiten": {},
    "bevoelkerung": 0.0,
    "importiert": {},
    "reserve": {},
    "werkstaetten": {},
    "ausbildung": [],
    "forschungsauftrag": None,
    "produktionsjournal": [],
    "verbrauchsjournal": [],
    "fertigjournal": [],
}


def temp(name: str) -> str:
    ordner = os.path.join(os.environ.get("TMPDIR") or os.environ["TEMP"], "oek_einhaengung")
    os.makedirs(ordner, exist_ok=True)
    return os.path.join(ordner, name)


# --------------------------------------------------------------------------
abschnitt("P0: Die fuenfzehn Felder der lokalen Wirtschaft (Entwurf Z. 757-772)")

feldnamen = {f.name for f in dataclasses.fields(ST)}
for name, vorgabe in NEU.items():
    check("P0: Feld '%s' ist vorhanden" % name, name in feldnamen)
    if name in feldnamen:
        wert = getattr(ST(name="X", map_id="kontinent"), name)
        check("P0: '%s' hat die Vorgabe %r" % (name, vorgabe), wert == vorgabe, repr(wert))

check("P0: die alten Felder sind unveraendert da",
      {"name", "map_id", "x", "y", "buildings", "units", "garrison", "last_rename",
       "karte", "bauten", "stufen"} <= feldnamen,
      str(sorted(feldnamen)))


# --------------------------------------------------------------------------
abschnitt("P1: Die stabile Ort-Kennung")

k = M.siedlung_kennung("spieler", "kontinent", 3, 7)
check("P1: die Kennung nennt Besitzer und Weltfeld", k == "spieler:kontinent:3:7", k)
check("P1: sie ist deterministisch", M.siedlung_kennung("spieler", "kontinent", 3, 7) == k)
check("P1: zwei Felder ergeben verschiedene Kennungen",
      M.siedlung_kennung("spieler", "kontinent", 4, 7) != k)
check("P1: ein anderer Besitzer ergibt eine andere Kennung",
      M.siedlung_kennung("bot1", "kontinent", 3, 7) != k)
check("P1: der Name kommt in der Kennung nicht vor (Umbenennen aendert sie nie)",
      "X" not in k and "name" not in k.lower(), k)

_quelle = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
check("P1: main._found_settlement vergibt die Kennung wirklich",
      'id=siedlung_kennung("spieler", self.state.current_map, x, y)' in _quelle)
check("P1: main.load setzt fehlende Kennungen nach",
      "s.id = siedlung_kennung(s.besitzer, s.map_id, s.x, s.y)" in _quelle)
check("P1: die Dataclass leitet die Kennung NICHT aus dem Namen ab",
      not hasattr(ST, "__post_init__"))


# --------------------------------------------------------------------------
abschnitt("P2: Speichern und Laden tragen alle neuen Felder (Rundlauf)")

pfad = temp("rundlauf.json")
st = M.GameState()
d = ST(name="Testort", map_id="kontinent", x=3, y=7, karte=None, id=k)
d.vorraete = {"holz": 123.5, "stein": 20.0}
d.waren = {"Wollumhang": 2}
d.einheiten = {"Handkarren": 1}
d.bevoelkerung = 7.5
d.importiert = {"holz": 12.0}
d.reserve = {"holz": 50.0}
d.werkstaetten = {"Schmiede": {"kapazitaet": 1, "einheiten": []}}
d.ausbildung = [{"einheit": "Kaempfer", "gebaeude": "Kriegerakademie", "start": 0.0,
                 "ende": 600.0, "gebucht": False}]
d.forschungsauftrag = {"gebiet": "Kriegskunst", "zielstufe": 1, "startzeit": 0.0,
                       "dauer_stunden": 1.0}
d.produktionsjournal = [{"ab": 0.0, "bis": 3600.0, "mengen": {"holz": 4.0}}]
d.verbrauchsjournal = [{"zeit": 1.0, "rohstoff": "holz", "menge": 2.0, "ziel": "Testort"}]
d.fertigjournal = [{"zeit": 2.0, "art": "ware", "name": "Wollumhang"}]
st.settlements.append(d)

ok = st.save(pfad)
check("P2: der Spielstand wurde geschrieben", bool(ok) and os.path.exists(pfad))

zweit = M.GameState()
check("P2: der Spielstand wurde geladen", zweit.load(pfad) is True)
geladen = zweit.settlements[0] if zweit.settlements else ST(name="?", map_id="?")
for name in NEU:
    if name == "id":
        continue
    check("P2: '%s' ueberlebt den Rundlauf" % name,
          getattr(geladen, name) == getattr(d, name),
          "%r != %r" % (getattr(geladen, name), getattr(d, name)))
check("P2: die Kennung ueberlebt den Rundlauf", geladen.id == k, geladen.id)
check("P2: die Siedlung hat ihren Namen behalten", geladen.name == "Testort", geladen.name)


# --------------------------------------------------------------------------
abschnitt("P3: Ein Altspielstand ohne die neuen Felder laedt weiter")

pfad_alt = temp("altstand.json")
daten = json.load(open(pfad, encoding="utf-8"))
alt = {kk: vv for kk, vv in daten["settlements"][0].items() if kk not in NEU}
check("P3: der Altstand kennt die neuen Felder wirklich nicht",
      not (set(alt) & set(NEU)), str(sorted(set(alt) & set(NEU))))
daten["settlements"] = [alt]
with open(pfad_alt, "w", encoding="utf-8") as fh:
    json.dump(daten, fh)

dritt = M.GameState()
check("P3: der Altstand laedt", dritt.load(pfad_alt) is True)
s_alt = dritt.settlements[0] if dritt.settlements else ST(name="?", map_id="?")
check("P3: die lokalen Felder starten leer",
      s_alt.vorraete == {} and s_alt.waren == {} and s_alt.einheiten == {}
      and s_alt.bevoelkerung == 0.0 and s_alt.forschungsauftrag is None,
      "%r / %r / %r" % (s_alt.vorraete, s_alt.waren, s_alt.forschungsauftrag))
check("P3: die Kennung wird nachgesetzt", s_alt.id == k, s_alt.id)
check("P3: die Kennung nennt Besitzer und Weltfeld des Altstandes",
      s_alt.id == M.siedlung_kennung(s_alt.besitzer, s_alt.map_id, s_alt.x, s_alt.y))


# --------------------------------------------------------------------------
abschnitt("P4: Die Kennung ueberlebt ein Umbenennen")

pfad_neu = temp("umbenannt.json")
daten["settlements"][0]["name"] = "Ganz anders"
daten["settlements"][0]["id"] = k
with open(pfad_neu, "w", encoding="utf-8") as fh:
    json.dump(daten, fh)

viert = M.GameState()
check("P4: der umbenannte Stand laedt", viert.load(pfad_neu) is True)
s_neu = viert.settlements[0] if viert.settlements else ST(name="?", map_id="?")
check("P4: der neue Name steht da", s_neu.name == "Ganz anders", s_neu.name)
check("P4: die Kennung ist unveraendert", s_neu.id == k, s_neu.id)
check("P4: der Name taucht in der Kennung nicht auf", "Ganz anders" not in s_neu.id, s_neu.id)
# Gegenprobe: dieselbe Kennung, anderer Name -> keine neue Kennung beim Laden
check("P4: Laden erfindet keine zweite Kennung",
      s_neu.id == M.siedlung_kennung(s_neu.besitzer, s_neu.map_id, s_neu.x, s_neu.y))


# --------------------------------------------------------------------------
abschnitt("P5: Keine zweite fuehrende Wahrheit bis zur Aktivierung")

leer = M.GameState()
check("P5: ein frischer GameState hat keine Siedlungen", leer.settlements == [])
check("P5: der globale Rohstoffbestand bleibt der fuehrende (Handbuch S. 7: 100 Holz)",
      leer.resources["holz"].amount == 100, str(leer.resources["holz"].amount))
check("P5: 10 Siedler stehen global (Handbuch S. 7)", leer.population == 10.0,
      str(leer.population))
neu_ort = ST(name="Ort", map_id="kontinent", x=1, y=1)
check("P5: ein neuer Ort erbt KEINE globalen Bestaende (sonst zweimal gefuehrt)",
      neu_ort.vorraete == {} and neu_ort.bevoelkerung == 0.0 and neu_ort.einheiten == {},
      "%r / %r" % (neu_ort.vorraete, neu_ort.bevoelkerung))
check("P5: die Journale starten leer",
      neu_ort.produktionsjournal == [] and neu_ort.verbrauchsjournal == []
      and neu_ort.fertigjournal == [], str(neu_ort.produktionsjournal))
check("P5: der Besitzer eines Spielerortes ist 'spieler'", neu_ort.besitzer == "spieler")
check("P5: Dimension 1 ist die Startdimension (Vorschlag, Handbuch schweigt)",
      neu_ort.dimension == 1)

sys.exit(bericht())
