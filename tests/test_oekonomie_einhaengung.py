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
from harness import abschnitt, befund, bericht, check, import_src, projektwurzel  # noqa: E402

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


# --------------------------------------------------------------------------
abschnitt("P6: Anwesende UND unterwegs befindliche Einheiten - jede genau einmal (Entwurf Z. 786)")

st2 = M.GameState()
st2.units["Krieger"].count = 5
st2.units["Handkarren"].count = 3
vorher = dict(st2.alle_einheiten())
check("P6: ohne Auftrag zaehlt der Heimatbestand",
      vorher.get("Krieger") == 5 and vorher.get("Handkarren") == 3, str(vorher))

ok, meldung = st2.auftrag_starten("transportieren", {"Krieger": 2, "Handkarren": 1},
                                 "Siedlung 1", {"name": "Siedlung 2"}, 4.0)
check("P6: der Transport startet", ok, meldung)
check("P6: zuhause sind die Einheiten abgezogen",
      st2.units["Krieger"].count == 3 and st2.units["Handkarren"].count == 2,
      "%s / %s" % (st2.units["Krieger"].count, st2.units["Handkarren"].count))
check("P6: unterwegs zaehlen sie weiter - die Summe bleibt gleich",
      st2.alle_einheiten() == vorher, str(st2.alle_einheiten()))

ps = st2.punktestand()
check("P7: der Punktestand nennt anwesende UND unterwegs",
      ps["einheiten"].get("Krieger") == 5, str(ps["einheiten"]))
import punkte as PU  # noqa: E402
check("P7: die Kriegspunkte kommen aus der EINEN Quelle src/punkte.py",
      ps["krieg"] == PU.kriegspunkte(st2.alle_einheiten(), ps["wall_stufe"]),
      "%r / %r" % (ps["krieg"], PU.kriegspunkte(st2.alle_einheiten(), ps["wall_stufe"])))
# Gegenprobe: mit NUR den anwesenden Einheiten waeren die Punkte kleiner - die Pruefung ist
# also nicht leer (sie faellt auf der alten Fassung durch).
nur_zuhause = PU.kriegspunkte({k: int(v.count) for k, v in st2.units.items()}, ps["wall_stufe"])
check("P7: Gegenprobe - 'nur zuhause' waere wirklich weniger",
      nur_zuhause < ps["krieg"], "%r < %r" % (nur_zuhause, ps["krieg"]))

_m = st2.auftraege[0]
st2.auftraege_fortschreiben(_m["rueckkehr"] + 1.0)
check("P8: die Truppe ist wieder zuhause",
      st2.units["Krieger"].count == 5 and st2.units["Handkarren"].count == 3,
      "%s / %s" % (st2.units["Krieger"].count, st2.units["Handkarren"].count))
check("P8: der Auftrag ist aus der Liste", st2.auftraege == [], str(st2.auftraege))
check("P8: die Summe bleibt gleich - keine Doppelzaehlung, kein Verlust",
      st2.alle_einheiten() == vorher, str(st2.alle_einheiten()))


# --------------------------------------------------------------------------
abschnitt("P9: Die Kriegspunkte brechen waehrend der Reise nicht ein")

st3 = M.GameState()
st3.units["Krieger"].count = 5
st3.units["Handkarren"].count = 3
k_vorher = st3.punktestand()["krieg"]
st3.auftrag_starten("transportieren", {"Krieger": 2, "Handkarren": 1},
                    "Siedlung 1", {"name": "Siedlung 2"}, 4.0)
k_unterwegs = st3.punktestand()["krieg"]
check("P9: die Kriegspunkte sind unterwegs dieselben", k_unterwegs == k_vorher,
      "%r / %r" % (k_vorher, k_unterwegs))


# --------------------------------------------------------------------------
abschnitt("P10: Stationieren - die Truppe verlaesst den Bestand genau einmal")

st4 = M.GameState()
st4.units["Krieger"].count = 5
st4.units["Handkarren"].count = 3
st4.auftrag_starten("stationieren", {"Krieger": 2}, "Siedlung 1", {"name": "Siedlung 2"}, 4.0)
check("P10: unterwegs zaehlt die Truppe noch", st4.alle_einheiten().get("Krieger") == 5,
      str(st4.alle_einheiten()))
_m4 = st4.auftraege[0]
st4.auftraege_fortschreiben(_m4["rueckkehr"] + 1.0)
check("P10: danach ist sie aus dem Bestand (kein Doppelzaehlen)",
      st4.alle_einheiten().get("Krieger") == 3, str(st4.alle_einheiten()))
check("P10: der Auftrag ist beendet", st4.auftraege == [], str(st4.auftraege))
# Ehrlich benannt: bis es je Ort eigene Einheitenbestaende gibt (Schritt 9, spaeterer Teil), steht
# eine stationierte Truppe in KEINEM Lager - sie ist weder zuhause noch unterwegs.
befund("P10: stationierte Truppen haben noch kein eigenes Lager (bis zur per-Ort-Umstellung)",
       "2 Krieger stehen nach dem Stationieren in keinem Bestand - das oertliche Feld "
       "'einheiten' ist bis zur Aktivierung leer (Entwurf Z. 774).")



# --------------------------------------------------------------------------
abschnitt("P11: Produktion je Ort - der Ertrag landet im LOKALEN Lager (Entwurf Schritt 9, Teil 3)")

# Karte und Bauhilfe: die Karten-Suche steht in tests/test_ertrag_anbindung.py. Diese Datei fuehrt
# sich beim Import SELBST aus (`sys.exit(bericht())`) und steht dann nicht in `sys.modules` - der
# belegte Weg im Projekt ist deshalb: eigene Hilfsdaten bauen statt eine Pruefdatei umzubauen.
def karte_und_felder(art, anzahl=1):
    """Eine Siedlungskarte mit mindestens ``anzahl`` Feldern der Gelaendeart samt Feldindizes."""
    import gelaende as G
    for typ in ("waldreich", "gemischt", "bergreich", "weideland", "nebelseeufer"):
        for s in range(500):
            karte = G.siedlungskarte_erzeugen(s, typ_id=typ)
            felder = [i for i, a in enumerate(karte["raster"]) if a == art]
            if len(felder) >= anzahl:
                return karte, felder
    return None, []


_karte, _wald = karte_und_felder("wald")
check("P11: eine Waldkarte ist gefunden", _karte is not None and bool(_wald))

st5 = M.GameState()
ort5 = M.Settlement(name="Waldort", map_id="test", karte=_karte,
                    id=M.siedlung_kennung("spieler", "test", 0, 0))
st5.settlements.append(ort5)
ok, meldung = M.bauen_auf_karte(ort5, "holzfaeller", _wald[0])
check("P11: der Holzfaeller steht auf dem Waldfeld", ok, meldung)
check("P11: der Ertrag DIESES Ortes ist 4 Holz je Stunde",
      abs(st5.ertrag_je_ort(ort5).get("holz", 0.0) - 4.0) < 1e-9, str(st5.ertrag_je_ort(ort5)))
check("P11: die Gesamtsicht nennt denselben Wert",
      abs(float(st5.stundenertrag().get("holz", 0.0)) - 4.0) < 1e-9, str(st5.stundenertrag()))

_global_vorher = float(st5.resources["holz"].amount)
st5.tick(3600)
check("P11: nach einer Stunde liegen 4 Holz im LOKALEN Lager des Ortes",
      abs(float(ort5.vorraete.get("holz", 0.0)) - 4.0) < 1e-9, str(ort5.vorraete))
check("P11: die Gesamtsicht waechst um dieselben 4 Holz (eine Wahrheit, zwei Ansichten)",
      abs(float(st5.resources["holz"].amount) - _global_vorher - 4.0) < 1e-9,
      "%r -> %r" % (_global_vorher, st5.resources["holz"].amount))
check("P11: die Summe der Ortslager nennt genau diese 4 Holz",
      abs(float(st5.ortslager().get("holz", 0.0)) - 4.0) < 1e-9, str(st5.ortslager()))


# --------------------------------------------------------------------------
abschnitt("P12: Bezahlt wird aus dem Lager DIESES Ortes (verbrauche_am_ort)")

ort5.vorraete["holz"] = 100.0
ort5.vorraete["stein"] = 100.0
_reich_holz = float(st5.resources["holz"].amount)
ok, meldung = st5.verbrauche_am_ort(ort5, {"holz": 30.0})
check("P12: die Zahlung aus dem Ortslager gelingt", ok, meldung)
check("P12: das Ortslager sinkt (100 -> 70)", abs(ort5.vorraete["holz"] - 70.0) < 1e-9,
      str(ort5.vorraete))
check("P12: der Reichsbestand bleibt unberuehrt, weil der Ort zahlen konnte",
      abs(float(st5.resources["holz"].amount) - _reich_holz) < 1e-9,
      "%r -> %r" % (_reich_holz, st5.resources["holz"].amount))

# Uebergangskasse: reicht der Ort nicht, zahlt der Reichsbestand genau den REST dazu.
ort5.vorraete["stein"] = 0.0
st5.resources["stein"].amount = 50.0
ok, meldung = st5.verbrauche_am_ort(ort5, {"stein": 20.0})
check("P12: Stein kommt dann ganz aus dem Reichsbestand (50 -> 30)", ok, meldung)
check("P12: der Reichsbestand Stein ist 30",
      abs(float(st5.resources["stein"].amount) - 30.0) < 1e-9,
      str(st5.resources["stein"].amount))
ok, meldung = st5.verbrauche_am_ort(ort5, {"holz": 40.0})
check("P12: Holz kommt ganz aus dem Ortslager, solange es reicht (70 -> 30)", ok, meldung)
check("P12: das Ortslager Holz ist 30", abs(ort5.vorraete["holz"] - 30.0) < 1e-9,
      str(ort5.vorraete))

# Ablehnung: NICHTS wird gebucht (Vergleich gegen Kopien).
import copy as _copy  # noqa: E402
st5.resources["stein"].amount = 1.0
_ort_kopie = _copy.deepcopy(ort5.vorraete)
_reich_kopie = {k: float(v.amount) for k, v in st5.resources.items()}
ok, meldung = st5.verbrauche_am_ort(ort5, {"stein": 999.0})
check("P12: eine ungedeckte Zahlung wird abgelehnt", not ok, meldung)
check("P12: die Meldung nennt das Fehlende", "stein" in meldung, meldung)
check("P12: das Ortslager bleibt unveraendert", ort5.vorraete == _ort_kopie, str(ort5.vorraete))
check("P12: der Reichsbestand bleibt unveraendert",
      {k: float(v.amount) for k, v in st5.resources.items()} == _reich_kopie,
      str({k: float(v.amount) for k, v in st5.resources.items()}))
check("P12: ortsdeckung nennt genau den fehlenden Betrag (999 - 0 - 1)",
      abs(st5.ortsdeckung(ort5, {"stein": 999.0})["stein"] - 998.0) < 1e-9,
      str(st5.ortsdeckung(ort5, {"stein": 999.0})))

# Siedler: erst aus der Bevoelkerung des Ortes, dann aus dem Reich.
ort5.bevoelkerung = 3.0
st5.population = 5.0
ok, meldung = st5.verbrauche_am_ort(ort5, {"siedler": 4.0})
check("P12: Siedler werden am Ort und dann im Reich genommen", ok, meldung)
check("P12: der Ort hat danach 0 Siedler", abs(ort5.bevoelkerung) < 1e-9, str(ort5.bevoelkerung))
check("P12: das Reich hat danach 4 Siedler", abs(float(st5.population) - 4.0) < 1e-9,
      str(st5.population))


# --------------------------------------------------------------------------
abschnitt("P13: Ein Abzug trifft Reichsbestand UND Ortslager (Uebergangs-Invariante)")

st6 = M.GameState()
o_a = M.Settlement(name="A", map_id="test", id="spieler:test:0:0")
o_b = M.Settlement(name="B", map_id="test", id="spieler:test:1:0")
o_a.vorraete = {"holz": 60.0}
o_b.vorraete = {"holz": 40.0}
st6.settlements = [o_a, o_b]
st6.resources["holz"].amount = 150.0
st6.reich_abzug("holz", 50.0)
check("P13: der Reichsbestand sinkt um 50 (150 -> 100)",
      abs(float(st6.resources["holz"].amount) - 100.0) < 1e-9,
      str(st6.resources["holz"].amount))
check("P13: die Ortslager sinken anteilig (60 -> 30, 40 -> 20)",
      abs(o_a.vorraete["holz"] - 30.0) < 1e-9 and abs(o_b.vorraete["holz"] - 20.0) < 1e-9,
      "%r / %r" % (o_a.vorraete["holz"], o_b.vorraete["holz"]))
st6.reich_abzug("holz", 10000.0)
check("P13: ein zu grosser Abzug macht nichts negativ",
      float(st6.resources["holz"].amount) >= 0.0 and o_a.vorraete["holz"] >= 0.0
      and o_b.vorraete["holz"] >= 0.0,
      "%r / %r / %r" % (st6.resources["holz"].amount, o_a.vorraete["holz"], o_b.vorraete["holz"]))
check("P13: ein Abzug von 0 aendert nichts",
      abs(st6.reich_abzug("holz", 0.0)) < 1e-9)


# --------------------------------------------------------------------------
abschnitt("P14: Die Rueckrufe zahlen wirklich am Ort (Quelltextwachen)")

_q2 = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
check("P14: _karten_bauen zahlt ueber verbrauche_am_ort",
      "ok_zahlung, meldung_zahlung = self.state.verbrauche_am_ort(siedlung, kosten)" in _q2)
check("P14: _karten_ausbauen zahlt ueber verbrauche_am_ort",
      _q2.count("verbrauche_am_ort(siedlung, kosten)") >= 2,
      str(_q2.count("verbrauche_am_ort(siedlung, kosten)")))
check("P14: tick bucht die Produktion je Ort (ertrag_je_ort)",
      "for res, rate_pro_stunde in self.ertrag_je_ort(siedlung).items():" in _q2)
check("P14: die Gruendung uebernimmt die Startwerte in das Ortslager",
      "sett.vorraete = dict(start)" in _q2 and "self.state.population = 0.0" in _q2)
check("P14: eine Kolonie zahlt ihr Startpaket aus dem Lager der Mutter",
      'verbrauche_am_ort(quelle, absicht["sperrgut"])' in _q2)
check("P14: die Bot-Beute trifft beide Buecher (reich_abzug)",
      "self.reich_abzug(stoff, float(menge))" in _q2)
check("P14: das Oekonomie-Modul ist jetzt wirklich eingebunden (Schritt 9)",
      "import spieloekonomie" in _q2)


# --------------------------------------------------------------------------
abschnitt("P15: Die zwei Ansichten sind getrennt - 'lokal' gegen 'Reich' (Teil 3b)")

# Belegte Startwerte (Handbuch S. 7): 10 Siedler, 100 Holz, 100 Stein.
st7 = M.GameState()
ort7 = M.Settlement(name="Startort", map_id="kontinent", x=0, y=0,
                    id=M.siedlung_kennung("spieler", "kontinent", 0, 0))
ort7.vorraete = {"holz": 100.0, "stein": 100.0}
ort7.bevoelkerung = 10.0
st7.settlements.append(ort7)

lokal7 = M.ortsbestand_text(ort7)
reich7 = M.reichsbestand_text(st7)
check("P15: der Ortsbestand nennt die belegten Startwerte",
      "100 Holz" in lokal7 and "100 Stein" in lokal7 and "10 Siedler" in lokal7, lokal7)
check("P15: der Reichsbestand nennt die Gesamtsicht",
      "100 Holz" in reich7 and "10 Siedler" in reich7, reich7)

# Die Trennung ist nur echt, wenn beide Zahlen auseinanderlaufen koennen.
ort7.vorraete = {"holz": 137.5, "stein": 42.0}
ort7.bevoelkerung = 8.0
st7.resources["holz"].amount = 777.0
st7.resources["stein"].amount = 300.0
st7.population = 21.0
lokal7 = M.ortsbestand_text(ort7)
reich7 = M.reichsbestand_text(st7)
check("P15: 'lokal' liest NUR das Ortslager (137.5 Holz / 8 Siedler)",
      "137.5 Holz" in lokal7 and "42 Stein" in lokal7 and "8 Siedler" in lokal7, lokal7)
check("P15: 'lokal' zeigt den Reichsbestand NICHT (kein 777)",
      "777" not in lokal7, lokal7)
check("P15: 'Reich' liest die Gesamtsicht (777 Holz / 21 Siedler)",
      "777 Holz" in reich7 and "300 Stein" in reich7 and "21 Siedler" in reich7, reich7)
check("P15: 'Reich' zeigt das Ortslager NICHT als eigene Zahl (kein 137.5)",
      "137.5" not in reich7, reich7)
check("P15: die zwei Ansichten sind wirklich verschieden", lokal7 != reich7,
      "%r vs %r" % (lokal7, reich7))
check("P15: gerade Zahlen ohne Nachkommastelle, krumme mit einer",
      M.zahl_text(7.0) == "7" and M.zahl_text(137.5) == "137.5" and M.zahl_text(0) == "0")
check("P15: ein leerer Ort wird ehrlich als leer gemeldet",
      M.ortsbestand_text(M.Settlement(name="Leer", map_id="x")) == "leer \u00b7 0 Siedler",
      M.ortsbestand_text(M.Settlement(name="Leer", map_id="x")))
check("P15: ein unbekannter Posten verschwindet nicht (alte Spielstaende)",
      "5 Kristall" in M.mengen_text({"kristall": 5.0}), M.mengen_text({"kristall": 5.0}))


# --------------------------------------------------------------------------
abschnitt("P16: Beide Ansichten ueberleben Speichern und Laden (Rundlauf, Teil 3b)")

pfad_b = temp("ansichten_rundlauf.json")
st8 = M.GameState()
ort8 = M.Settlement(name="Beideo", map_id="kontinent", x=2, y=5,
                    id=M.siedlung_kennung("spieler", "kontinent", 2, 5))
ort8.vorraete = {"holz": 61.5, "stein": 12.0}
ort8.bevoelkerung = 4.0
st8.settlements.append(ort8)
st8.resources["holz"].amount = 900.0
st8.resources["stein"].amount = 55.0
st8.population = 33.0
vorher_lokal = M.ortsbestand_text(ort8)
vorher_reich = M.reichsbestand_text(st8)
check("P16: der Spielstand wird geschrieben", bool(st8.save(pfad_b)))

zweit8 = M.GameState()
check("P16: der Spielstand wird geladen", zweit8.load(pfad_b) is True)
geladen8 = zweit8.settlements[0] if zweit8.settlements else M.Settlement(name="?", map_id="?")
check("P16: die LOKALE Ansicht ist nach dem Laden gleich",
      M.ortsbestand_text(geladen8) == vorher_lokal,
      "%r != %r" % (M.ortsbestand_text(geladen8), vorher_lokal))
check("P16: die REICHS-Ansicht ist nach dem Laden gleich",
      M.reichsbestand_text(zweit8) == vorher_reich,
      "%r != %r" % (M.reichsbestand_text(zweit8), vorher_reich))
check("P16: die zwei Ansichten sind auch nach dem Laden noch verschieden",
      M.ortsbestand_text(geladen8) != M.reichsbestand_text(zweit8))
# Gegenprobe: waeren beide Ansichten dieselbe Quelle, faellt dieser Vergleich durch.
check("P16: Gegenprobe - Ortslager und Reichsbestand sind wirklich zwei Zahlen",
      float(geladen8.vorraete.get("holz", 0.0)) != float(zweit8.resources["holz"].amount),
      "%r vs %r" % (geladen8.vorraete.get("holz"), zweit8.resources["holz"].amount))


# --------------------------------------------------------------------------
abschnitt("P17: Die Anzeigen rufen wirklich die zwei Ansichten (Quelltextwachen)")

_q3 = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
check("P17: die Siedlungsliste zeigt 'Reich: '",
      '"Reich: " + reichsbestand_text(self.state)' in _q3)
check("P17: jede Siedlungszeile zeigt 'lokal: '",
      '"lokal: " + ortsbestand_text(s)' in _q3)
check("P17: die Siedlungskarte hebt den Ortsbestand hervor",
      "ortsbestand_text(siedlung)" in _q3)
check("P17: die Kopfleiste nennt die Gesamtsicht 'Reich'", 'text="Reich:"' in _q3)
check("P17: die Bevoelkerung im Dorfzentrum ist als Reichs-Zahl gekennzeichnet",
      '"Siedler (Reich):' in _q3)
check("P17: der Wortlaut kommt aus EINER Quelle (kein zweiter Text im Aufrufer)",
      _q3.count("def ortsbestand_text") == 1 and _q3.count("def reichsbestand_text") == 1)


# --------------------------------------------------------------------------
abschnitt("P18: Teil 4 - der EIGENE Transport geht den ganzen Weg (Kern + Auftragsschleife)")

st9 = M.GameState()
q9 = M.Settlement(name="Waldheim", map_id="test", x=0, y=0, id="spieler:test:0:0")
z9 = M.Settlement(name="Steinberg", map_id="test", x=2, y=0, id="spieler:test:2:0")
q9.vorraete = {"holz": 100.0, "stein": 100.0}
q9.bevoelkerung = 10.0
z9.vorraete = {"holz": 0.0}
z9.bevoelkerung = 10.0
st9.settlements = [q9, z9]
st9.current_map = "test"
st9.units["Handkarren"].count = 1
_reich_holz = float(st9.resources["holz"].amount)

ok, meldung = st9.transport_an_ort(q9, z9, "holz", 20, {"Handkarren": 1}, jetzt=1000.0)
check("P18: der Transport startet", ok, meldung)
check("P18: genau EINE Mission haengt in der Auftragsliste", len(st9.auftraege) == 1,
      str(len(st9.auftraege)))
_m9 = st9.auftraege[0]
check("P18: die Mission ist ein EIGENTRANSPORT (der Altpfad darf sie nie buchen)",
      _m9.get("eigentransport") is True, str(_m9.get("eigentransport")))
check("P18: die Fracht steht an der Mission", _m9.get("fracht") == {"holz": 20},
      str(_m9.get("fracht")))
check("P18: der Karren reist mit", _m9.get("einheiten") == {"Handkarren": 1},
      str(_m9.get("einheiten")))
check("P18: die Fracht ist aus dem ORTSLAGER abgebucht (100 -> 80)",
      abs(q9.vorraete["holz"] - 80.0) < 1e-9, str(q9.vorraete))
check("P18: der Reichsbestand bleibt unberuehrt (ein Transport ist eine Bewegung, keine Produktion)",
      abs(float(st9.resources["holz"].amount) - _reich_holz) < 1e-9,
      str(st9.resources["holz"].amount))
check("P18: der Karren ist aus dem Reichsheer in die Mission gewandert",
      int(st9.units["Handkarren"].count) == 0, str(st9.units["Handkarren"].count))
check("P18: der Karren faellt nicht aus der Wertung (unterwegs zaehlt weiter)",
      st9.alle_einheiten().get("Handkarren") == 1, str(st9.alle_einheiten()))

st9.auftraege_fortschreiben(float(_m9["ankunft"]) + 1.0)
check("P18: nach der Ankunft liegen 20 Holz im ORTSLAGER des Ziels",
      abs(float(z9.vorraete.get("holz", 0.0)) - 20.0) < 1e-9, str(z9.vorraete))
check("P18: die Importherkunft ist mitgebucht (Siegnachweis, Schritt 7)",
      abs(float(z9.importiert.get("holz", 0.0)) - 20.0) < 1e-9, str(z9.importiert))
check("P18: der Reichsbestand hat die Fracht NICHT noch einmal bekommen",
      abs(float(st9.resources["holz"].amount) - _reich_holz) < 1e-9,
      str(st9.resources["holz"].amount))

st9.auftraege_fortschreiben(float(_m9["rueckkehr"]) + 1.0)
check("P18: der Karren steht wieder im ORTSLAGER der Herkunft",
      int(q9.einheiten.get("Handkarren", 0)) == 1, str(q9.einheiten))
check("P18: der Auftrag ist beendet", st9.auftraege == [], str(st9.auftraege))
check("P18: der Karren steht NICHT doppelt (Ort ODER Reich, nie beides)",
      int(q9.einheiten.get("Handkarren", 0)) + int(st9.units["Handkarren"].count) == 1,
      str(q9.einheiten) + " / " + str(st9.units["Handkarren"].count))
check("P18: die Wertung bleibt gleich (alle_einheiten nennt den ORT mit)",
      st9.alle_einheiten().get("Handkarren") == 1, str(st9.alle_einheiten()))
_weitere = st9.auftraege_fortschreiben(float(_m9["rueckkehr"]) + 5.0)
check("P18: Fracht kommt genau EINMAL an (zweiter Aufruf aendert nichts)",
      abs(float(z9.vorraete.get("holz", 0.0)) - 20.0) < 1e-9, str(z9.vorraete))
check("P18: Ankunft UND Heimkehr stehen als Bericht in den Nachrichten",
      len([m for m in st9.messages if "Transport" in str(m.get("text"))]) >= 2,
      str(len(st9.messages)))


# --------------------------------------------------------------------------
abschnitt("P19: Teil 4 - jede Ablehnung aendert NICHTS")

import copy as _copy4  # noqa: E402

st10 = M.GameState()
q10 = M.Settlement(name="A", map_id="test", x=0, y=0, id="spieler:test:0:0")
z10 = M.Settlement(name="B", map_id="test", x=1, y=0, id="spieler:test:1:0")
q10.vorraete = {"holz": 50.0}
z10.vorraete = {"holz": 0.0}
st10.settlements = [q10, z10]
st10.current_map = "test"
st10.units["Handkarren"].count = 2


def unveraendert(name, args):
    """Eine Ablehnung darf den Spielstand nicht anfassen (Vergleich gegen Kopien)."""
    _q = _copy4.deepcopy(q10.vorraete)
    _qe = _copy4.deepcopy(q10.einheiten)
    _z = _copy4.deepcopy(z10.vorraete)
    _karren = int(st10.units["Handkarren"].count)
    _auftraege = len(st10.auftraege)
    ok, meldung = st10.transport_an_ort(*args)
    check("P19: %s wird abgelehnt" % name, not ok, meldung)
    check("P19: %s laesst Ortslager, Ziel, Karren und Auftraege unveraendert" % name,
          q10.vorraete == _q and q10.einheiten == _qe and z10.vorraete == _z
          and int(st10.units["Handkarren"].count) == _karren
          and len(st10.auftraege) == _auftraege,
          "%r / %r / %r" % (q10.vorraete, z10.vorraete, st10.units["Handkarren"].count))


unveraendert("ohne Karren", (q10, z10, "holz", 10, {}, 1.0))
unveraendert("Herkunft gleich Ziel", (q10, q10, "holz", 10, {"Handkarren": 1}, 1.0))
unveraendert("Menge 0", (q10, z10, "holz", 0, {"Handkarren": 1}, 1.0))
unveraendert("unbekannter Rohstoff", (q10, z10, "kristall", 10, {"Handkarren": 1}, 1.0))
unveraendert("Ueberladung (5000 auf 40 Plaetze)", (q10, z10, "holz", 5000, {"Handkarren": 1}, 1.0))
unveraendert("Fracht fehlt im Ortslager", (q10, z10, "holz", 500, {"Handkarren": 1}, 1.0))
unveraendert("kein Transportmittel (Krieger)", (q10, z10, "holz", 10, {"Krieger": 1}, 1.0))
unveraendert("zu viele Karren", (q10, z10, "holz", 10, {"Handkarren": 9}, 1.0))
unveraendert("andere Karte", (q10, M.Settlement(name="Weit", map_id="kontinent", x=1, y=1,
                                                id="spieler:kontinent:1:1"),
                              "holz", 10, {"Handkarren": 1}, 1.0))
ok, meldung = st10.transport_an_ort(q10, z10, "holz", 10, {"Handkarren": 1}, 1.0)
check("P19: die Gegenprobe - ein gueltiger Transport geht durch", ok, meldung)


# --------------------------------------------------------------------------
abschnitt("P20: Teil 4 - ein laufender Transport ueberlebt Speichern und Laden")

pfad_t = temp("transport_rundlauf.json")
st11 = M.GameState()
# Echte Karten-Kennung, sonst kann `load` die Karte nicht aufbauen (`generate_map` kennt "test" nicht).
q11 = M.Settlement(name="Quelle", map_id=st11.current_map, x=0, y=0,
                   id="spieler:%s:0:0" % st11.current_map)
z11 = M.Settlement(name="Ziel", map_id=st11.current_map, x=3, y=0,
                   id="spieler:%s:3:0" % st11.current_map)
q11.vorraete = {"holz": 40.0}
z11.vorraete = {}
st11.settlements = [q11, z11]
st11.units["Handkarren"].count = 1
ok, meldung = st11.transport_an_ort(q11, z11, "holz", 25, {"Handkarren": 1}, jetzt=2000.0)
check("P20: der Transport startet", ok, meldung)
check("P20: der Spielstand wird geschrieben", bool(st11.save(pfad_t)))

zweit11 = M.GameState()
check("P20: der Spielstand wird geladen", zweit11.load(pfad_t) is True)
check("P20: der Auftrag ist noch da", len(zweit11.auftraege) == 1, str(len(zweit11.auftraege)))
_a11 = zweit11.auftraege[0] if zweit11.auftraege else {}
check("P20: er ist immer noch ein Eigentransport", _a11.get("eigentransport") is True)
check("P20: die Fracht steht noch an der Mission", _a11.get("fracht") == {"holz": 25},
      str(_a11.get("fracht")))
check("P20: das abgebuchte Ortslager ist erhalten (40 -> 15)",
      abs(float(zweit11.settlements[0].vorraete.get("holz", 0.0)) - 15.0) < 1e-9,
      str(zweit11.settlements[0].vorraete))
zweit11.auftraege_fortschreiben(float(_a11["ankunft"]) + 1.0)
check("P20: nach dem Laden kommt die Fracht am Ziel an",
      abs(float(zweit11.settlements[1].vorraete.get("holz", 0.0)) - 25.0) < 1e-9,
      str(zweit11.settlements[1].vorraete))
zweit11.auftraege_fortschreiben(float(_a11["rueckkehr"]) + 1.0)
check("P20: und der Karren kommt heim",
      int(zweit11.settlements[0].einheiten.get("Handkarren", 0)) == 1,
      str(zweit11.settlements[0].einheiten))


# --------------------------------------------------------------------------
abschnitt("P21: Teil 4 - die Anbindung im Quelltext (Wachen)")

_q4 = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
check("P21: die alte Methode mit festem 10 Holz ist vollstaendig ersetzt",
      'amount = 10\n        resource' not in _q4 and 'resource = "holz"' not in _q4,
      "noch vorhanden")
check("P21: die Maske bucht ueber den Kern",
      "transport_an_ort(quelle, ziel, rohstoff, menge, karren)" in _q4)
check("P21: die Auftragsschleife fuehrt Eigentransporte ueber den Kern",
      "self._eigentransport_buchen(eintrag, jetzt)" in _q4)
check("P21: die Auftragsschleife ueberspringt sie auch beim Ankunftsbericht",
      _q4.count('if eintrag.get("eigentransport"):') >= 3,
      str(_q4.count('if eintrag.get("eigentransport"):')))
check("P21: alle_einheiten nennt auch die ORTSLAGER (Entwurf Z. 786)",
      'for name, anzahl in (getattr(siedlung, "einheiten", None) or {}).items():' in _q4)
check("P21: der Kern transport_start wird wirklich benutzt",
      "spieloekonomie.transport_start(quelle_dict, asdict(ziel), karren," in _q4)
check("P21: der Kern transport_fortschritt wird wirklich benutzt",
      "spieloekonomie.transport_fortschritt(dict(eintrag), orte, jetzt)" in _q4)


# --------------------------------------------------------------------------
abschnitt("P22: Teil 5 - Kartenvorrat und Auswahlliste (Entwurf Z. 777)")

st12 = M.GameState()
check("P22: ein frischer Zustand hat noch keinen Vorrat", st12.kartenvorrat == {})
check("P22: Anlegen liefert die Koloniekarten", len(st12.kartenvorrat_anlegen("probe")) == 9,
      str(len(st12.kartenvorrat)))
check("P22: die Saat wird gemerkt (derselbe Stand vergibt dieselben Karten)",
      st12.kartenvorrat_seed == "probe")
check("P22: alle Karten sind frei",
      all(v.get("besitzer") is None for v in st12.kartenvorrat.values()))

q12 = M.Settlement(name="Haupt", map_id=st12.current_map, x=0, y=0,
                   id=M.siedlung_kennung("spieler", st12.current_map, 0, 0),
                   karte=M.spieloekonomie.startkarte("probe", "spieler"))
st12.settlements = [q12]
_liste = st12.freie_koloniekarten()
check("P22: die Auswahlliste nennt alle freien Karten", len(_liste) == 9, str(len(_liste)))
check("P22: jeder Eintrag traegt Nutzen, Kapazitaeten, Gebuehr und Mindestbestand",
      all({"nutzen", "kapazitaeten", "preis", "minimum"} <= set(e) for e in _liste))
check("P22: die Liste ist nach Nutzen sortiert (beste zuerst)",
      all(_liste[i]["nutzen"] >= _liste[i + 1]["nutzen"] for i in range(len(_liste) - 1)),
      str([round(e["nutzen"], 2) for e in _liste]))
check("P22: die Gebuehr ist die belegte (320/200/150)",
      abs(_liste[0]["preis"]["holz"] - 320.0) < 1e-9 and abs(_liste[0]["preis"]["stein"] - 200.0) < 1e-9
      and abs(_liste[0]["preis"]["nahrung"] - 150.0) < 1e-9, str(_liste[0]["preis"]))
check("P22: der Mindestbestand ist die belegte Summe (480/300/250)",
      abs(_liste[0]["minimum"]["holz"] - 480.0) < 1e-9
      and abs(_liste[0]["minimum"]["stein"] - 300.0) < 1e-9
      and abs(_liste[0]["minimum"]["nahrung"] - 250.0) < 1e-9, str(_liste[0]["minimum"]))
check("P22: das Erzeugerprofil nennt Stundenertraege",
      isinstance(_liste[0]["kapazitaeten"], dict) and bool(_liste[0]["kapazitaeten"]))

_f1 = st12.freie_weltfelder(4)
_f2 = st12.freie_weltfelder(4)
check("P22: die Weltfelder sind in fester Reihenfolge (kein Zufall)", _f1 == _f2, str(_f1))
check("P22: es sind vier Felder", len(_f1) == 4, str(len(_f1)))
check("P22: kein Feld ist Wasser oder schon vergeben",
      all((st12.get_tile(x, y, 20) is not None
           and st12.get_tile(x, y, 20).terrain != "water"
           and not st12.get_tile(x, y, 20).npc_faction) for x, y in _f1), str(_f1))


# --------------------------------------------------------------------------
abschnitt("P23: Teil 5 - die Gruendung geht ueber den Kern (absicht) und bucht richtig")

pfad_g = temp("gruendung_rundlauf.json")
st13 = M.GameState()
st13.kartenvorrat_anlegen("probe")
q13 = M.Settlement(name="Haupt", map_id=st13.current_map, x=0, y=0,
                   id=M.siedlung_kennung("spieler", st13.current_map, 0, 0),
                   karte=M.spieloekonomie.startkarte("probe", "spieler"))
q13.vorraete = {"holz": 700.0, "stein": 450.0, "nahrung": 350.0}
q13.bevoelkerung = 20.0
st13.settlements = [q13]
st13.units["Siedlerkarren"].count = 1


def nichts_geaendert(name, karte_id="ausgleich_a", feld=(3, 0)):
    """Eine Ablehnung darf weder Vorrat noch Lager noch Siedlungen anfassen."""
    _v = {k: dict(v) for k, v in st13.kartenvorrat.items()}
    _q = _copy4.deepcopy(q13.vorraete)
    _k = int(st13.units["Siedlerkarren"].count)
    _n = len(st13.settlements)
    ok, meldung, _a = st13.gruendung_pruefen(q13, karte_id, feld)
    check("P23: %s wird abgelehnt" % name, not ok, meldung)
    check("P23: %s laesst Vorrat, Ortslager, Karren und Siedlungen unveraendert" % name,
          st13.kartenvorrat == _v and q13.vorraete == _q
          and int(st13.units["Siedlerkarren"].count) == _k
          and len(st13.settlements) == _n, meldung)


nichts_geaendert("ohne Wagenbau", "ausgleich_a")
st13.research["Wagenbau"].level = 1
st13.units["Siedlerkarren"].count = 0
nichts_geaendert("ohne Siedlerkarren", "ausgleich_a")
st13.units["Siedlerkarren"].count = 1
_kopie_lager = _copy4.deepcopy(q13.vorraete)
q13.vorraete = {"holz": 100.0, "stein": 100.0, "nahrung": 100.0}
nichts_geaendert("ohne Mindestbestand", "ausgleich_a")
q13.vorraete = _kopie_lager
nichts_geaendert("unbekannte Karte", "gibtsnicht")

ok, meldung, _a = st13.gruendung_pruefen(q13, "ausgleich_a", (3, 0))
check("P23: mit Forschung, Karren und Mindestbestand ist die Absicht gueltig", ok, meldung)
check("P23: die Absicht nennt Sperrgut, Gebuehr und Paket",
      abs(_a.get("sperrgut", {}).get("holz", 0) - 480.0) < 1e-9
      and abs(_a.get("preis", {}).get("holz", 0) - 320.0) < 1e-9
      and abs(_a.get("paket", {}).get("holz", 0) - 160.0) < 1e-9, str(_a.get("sperrgut")))
check("P23: die Absicht traegt das gewaehlte Weltfeld", _a.get("weltfeld") == [3, 0],
      str(_a.get("weltfeld")))

_karren_vorher = int(st13.units["Siedlerkarren"].count)
ok, meldung = st13.gruendung_ausfuehren(q13, "ausgleich_a", (3, 0))
check("P23: die Gruendung gelingt", ok, meldung)
check("P23: es gibt jetzt ZWEI Siedlungen", len(st13.settlements) == 2, str(len(st13.settlements)))
_g = st13.settlements[-1]
check("P23: die neue Siedlung steht auf dem gewaehlten Weltfeld", (_g.x, _g.y) == (3, 0),
      "%s/%s" % (_g.x, _g.y))
check("P23: sie bekommt das Startpaket (160/100/100)",
      abs(_g.vorraete.get("holz", 0) - 160.0) < 1e-9 and abs(_g.vorraete.get("stein", 0) - 100.0) < 1e-9
      and abs(_g.vorraete.get("nahrung", 0) - 100.0) < 1e-9, str(_g.vorraete))
check("P23: und die 5 Kolonisten aus dem Siedlerkarren", abs(_g.bevoelkerung - 5.0) < 1e-9,
      str(_g.bevoelkerung))
check("P23: die Ausgangssiedlung hat den Mindestbestand verloren (700 -> 220)",
      abs(q13.vorraete.get("holz", 0) - 220.0) < 1e-9
      and abs(q13.vorraete.get("stein", 0) - 150.0) < 1e-9
      and abs(q13.vorraete.get("nahrung", 0) - 100.0) < 1e-9, str(q13.vorraete))
check("P23: die Gebuehr ist vernichtet (Mindestbestand minus Paket), nichts doppelt",
      abs(q13.vorraete["holz"] + _g.vorraete["holz"] - 380.0) < 1e-9,
      "%s + %s" % (q13.vorraete["holz"], _g.vorraete["holz"]))
check("P23: der Siedlerkarren ist verbraucht",
      int(st13.units["Siedlerkarren"].count) == _karren_vorher - 1, str(st13.units["Siedlerkarren"].count))
check("P23: die Karte ist aus dem Vorrat vergeben",
      st13.kartenvorrat["ausgleich_a"]["besitzer"] == "spieler",
      str(st13.kartenvorrat["ausgleich_a"]["besitzer"]))
check("P23: sie steht nicht mehr in der Auswahlliste",
      all(e["karte_id"] != "ausgleich_a" for e in st13.freie_koloniekarten()))
check("P23: das Weltfeld gehoert jetzt dem Spieler",
      st13.get_tile(3, 0, 20).npc_faction == "spieler", str(st13.get_tile(3, 0, 20).npc_faction))
check("P23: die Siedlung traegt eine stabile Kennung",
      _g.id == M.siedlung_kennung("spieler", st13.current_map, 3, 0), _g.id)

check("P23: der Spielstand wird geschrieben", bool(st13.save(pfad_g)))
zweit13 = M.GameState()
check("P23: der Spielstand wird geladen", zweit13.load(pfad_g) is True)
check("P23: der Vorrat kennt die vergebene Karte nach dem Laden",
      zweit13.kartenvorrat.get("ausgleich_a", {}).get("besitzer") == "spieler",
      str(zweit13.kartenvorrat.get("ausgleich_a", {}).get("besitzer")))
check("P23: kein ALTSPIELSTAND ohne Vorrat stuerzt ab",
      len(zweit13.freie_koloniekarten()) == 8, str(len(zweit13.freie_koloniekarten())))
# Gegenprobe: eine schon vergebene Karte ist nicht mehr zu haben.
check("P23: dieselbe Karte laesst sich nicht zweimal vergeben",
      not zweit13.gruendung_pruefen(zweit13.settlements[0], "ausgleich_a", (5, 0))[0])


# --------------------------------------------------------------------------
abschnitt("P24: Teil 5 - die Startgruendung und die Anbindung im Quelltext")

st14 = M.GameState()
app_vierzehn = M.NebelseetalApp.__new__(M.NebelseetalApp)   # ohne Fenster: nur die Methoden
app_vierzehn.state = st14
app_vierzehn.content = None
app_vierzehn._log = lambda msg: st14.log.append(msg)
app_vierzehn._render_view = lambda: None
app_vierzehn._found_settlement()
check("P24: die erste Siedlung entsteht", len(st14.settlements) == 1, str(len(st14.settlements)))
_start = st14.settlements[0]
check("P24: sie traegt die STARTKARTE (keine zufaellige Erstwahl)",
      _start.karte["typ"] == M.spieloekonomie.G["kartenvorrat"]["start"]["id"],
      str(_start.karte.get("typ")))
check("P24: sie uebernimmt die belegten Startwerte (10 Siedler, 100 Holz, 100 Stein)",
      abs(_start.bevoelkerung - 10.0) < 1e-9 and abs(_start.vorraete.get("holz", 0) - 100.0) < 1e-9
      and abs(_start.vorraete.get("stein", 0) - 100.0) < 1e-9, str(_start.vorraete))
check("P24: die Startwerte werden GENAU EINMAL uebernommen (Reich ist leer)",
      float(st14.resources["holz"].amount) == 0.0 and float(st14.population) == 0.0,
      "%s / %s" % (st14.resources["holz"].amount, st14.population))
check("P24: der Kartenvorrat wurde dabei angelegt", len(st14.kartenvorrat) == 9,
      str(len(st14.kartenvorrat)))

import inspect as _inspect5  # noqa: E402
_q5 = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
check("P24: die Gruendung ruft den Kern absicht", "spieloekonomie.absicht(" in _q5)
check("P24: die Gruendung ruft den Kern vergabe", "spieloekonomie.vergabe([" in _q5)
check("P24: die Startkarte kommt aus dem Kern", "spieloekonomie.startkarte(" in _q5)
_quelle_found = _inspect5.getsource(M.NebelseetalApp._found_settlement)
check("P24: _found_settlement ist nur noch die Weiche (Erststart oder Kolonie)",
      "_erste_siedlung_gruenden()" in _quelle_found and "_kolonie_gruenden()" in _quelle_found)
check("P24: die Zufallskarte ist aus der Gruendung verschwunden",
      "neue_siedlungskarte" not in _q5.split("def _kolonie_gruenden")[1].split("def _gruendung")[0])
_quelle_kolonie = _inspect5.getsource(M.NebelseetalApp._kolonie_gruenden)
check("P24: die Maske zeigt die Auswahlliste und die Weltfelder",
      "freie_koloniekarten()" in _quelle_kolonie and "freie_weltfelder(" in _quelle_kolonie)
check("P24: der Knopf heisst Gruenden und bucht ueber die eine Stelle",
      "Gr\u00fcnden" in _quelle_kolonie and "_gruendung_ausfuehren(" in _quelle_kolonie)


abschnitt("P25: Teil 6a - der Zeiger auf den AKTIVEN Ort")

st15 = M.GameState()
check("P25: ein frischer Zustand hat keinen Ort gewaehlt", st15.aktive_siedlung_id == "")
check("P25: ohne Siedlung gibt es keine aktive Siedlung", st15.aktive_siedlung() is None)

q15a = M.Settlement(name="Erste", map_id=st15.current_map, x=0, y=0,
                    id=M.siedlung_kennung("spieler", st15.current_map, 0, 0))
q15b = M.Settlement(name="Zweite", map_id=st15.current_map, x=1, y=0,
                    id=M.siedlung_kennung("spieler", st15.current_map, 1, 0))
st15.settlements = [q15a, q15b]
check("P25: ohne Wahl faellt sie auf die ERSTE und berichtigt den Zeiger",
      st15.aktive_siedlung() is q15a and st15.aktive_siedlung_id == q15a.id,
      st15.aktive_siedlung_id)
st15.aktive_siedlung_id = q15b.id
check("P25: eine getroffene Wahl bleibt stehen", st15.aktive_siedlung() is q15b)
st15.aktive_siedlung_id = "gibtsnicht"
check("P25: ein veralteter Zeiger wird berichtigt statt abzustuerzen",
      st15.aktive_siedlung() is q15a and st15.aktive_siedlung_id == q15a.id,
      st15.aktive_siedlung_id)

pfad_a = temp("aktiv_rundlauf.json")
st15.aktive_siedlung_id = q15b.id
check("P25: der Stand wird geschrieben", bool(st15.save(pfad_a)))
st16 = M.GameState()
check("P25: der Stand wird geladen", st16.load(pfad_a) is True)
check("P25: der aktive Ort ueberlebt Speichern und Laden",
      st16.aktive_siedlung_id == q15b.id, st16.aktive_siedlung_id)
check("P25: und er zeigt auf DIESE der beiden Siedlungen",
      st16.aktive_siedlung() is not None and st16.aktive_siedlung().id == q15b.id,
      str(getattr(st16.aktive_siedlung(), "name", None)))

import json as _json6  # noqa: E402
_roh = _json6.load(open(pfad_a, encoding="utf-8"))
_roh.pop("aktive_siedlung_id", None)
_json6.dump(_roh, open(pfad_a, "w", encoding="utf-8"))
st17 = M.GameState()
check("P25: ein Spielstand OHNE das Feld laedt weiter (kein Absturz)", st17.load(pfad_a) is True)
check("P25: ... und faellt dann auf die erste Siedlung",
      st17.aktive_siedlung_id == "" and st17.settlements
      and st17.aktive_siedlung().id == st17.settlements[0].id, st17.aktive_siedlung_id)

_q6 = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
check("P25: die Liste zeigt den aktiven Ort und laesst ihn setzen",
      "Als aktiv setzen" in _q6 and "def _siedlung_aktiv_setzen" in _q6)
check("P25: die geoeffnete Siedlungskarte wird zum aktiven Ort",
      "self.state.aktive_siedlung_id = siedlung.id" in _q6)
check("P25: die Lageransicht zeigt das Ortslager der aktiven Siedlung",
      "Ortslager der aktiven Siedlung" in _q6 and "Waren vor Ort:" in _q6
      and "Einheiten vor Ort:" in _q6)
check("P25: die bisherigen Listen heissen jetzt ehrlich Reich/Uebergang",
      "Waren (Reich" in _q6 and "Einheiten (Reich" in _q6)


sys.exit(bericht())
