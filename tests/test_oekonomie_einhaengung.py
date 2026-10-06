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
check("P14: tick laesst die Ernte JE ORT vom Kern buchen (Teil 6b, genau einmal)",
      "spieloekonomie.ort_tick(asdict(siedlung), _ab, _bis, levels)" in _q2
      and "for res, rate_pro_stunde in self.ertrag_je_ort(siedlung).items():" not in _q2)
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
      _q4.count('if eintrag.get("eigentransport") or eintrag.get("fremdvertrag"):') >= 2
      and "self._eigentransport_buchen(eintrag, jetzt)" in _q4,
      str(_q4.count('if eintrag.get("eigentransport") or eintrag.get("fremdvertrag"):')))
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


abschnitt("P26: Teil 6b - EINE Uhr je Ort (kein Doppelertrag)")

_karte26, _wald26 = karte_und_felder("wald")
st26 = M.GameState()
ort26 = M.Settlement(name="Waldort", map_id="kontinent", karte=_karte26,
                     id=M.siedlung_kennung("spieler", "kontinent", 4, 4))
st26.settlements.append(ort26)
_bau_ok, _bau_meldung = M.bauen_auf_karte(ort26, "holzfaeller", _wald26[0])
check("P26: der Holzfaeller steht (Vorbedingung)", _bau_ok, _bau_meldung)
_rate26 = st26.ertrag_je_ort(ort26).get("holz", 0.0)
check("P26: der Ort erzeugt 4 Holz je Stunde", abs(_rate26 - 4.0) < 1e-9, str(_rate26))
check("P26: die Spieluhr startet bei 0", abs(float(st26.spielsekunden)) < 1e-9,
      str(st26.spielsekunden))
_reich26 = float(st26.resources["holz"].amount)
_leute26 = float(st26.population)

st26.tick(3600)
check("P26: eine Stunde Spielzeit ist genau eine Stunde auf der Uhr",
      abs(float(st26.spielsekunden) - 3600.0) < 1e-9, str(st26.spielsekunden))
check("P26: die Ernte kommt GENAU EINMAL an (nicht doppelt)",
      abs(float(ort26.vorraete.get("holz", 0.0)) - _rate26) < 1e-9, str(ort26.vorraete))
check("P26: die Gesamtsicht waechst um DIESELBE Menge (keine zweite Rechnung)",
      abs(float(st26.resources["holz"].amount) - _reich26 - _rate26) < 1e-9,
      "%r -> %r" % (_reich26, st26.resources["holz"].amount))
check("P26: das Produktionsjournal hat genau EINE Zeile je Takt",
      len(ort26.produktionsjournal) == 1, str(len(ort26.produktionsjournal)))
check("P26: ... und die Zeile nennt das Fenster der Uhr",
      abs(ort26.produktionsjournal[0]["ab"]) < 1e-9
      and abs(ort26.produktionsjournal[0]["bis"] - 3600.0) < 1e-9,
      str(ort26.produktionsjournal[0]))
check("P26: der Siedlerzuwachs kommt einmal je Stunde (Handbuch: 1 je Siedlung)",
      abs(float(ort26.bevoelkerung) - 1.0) < 1e-9, str(ort26.bevoelkerung))
check("P26: die Gesamtsicht waechst um denselben Siedler (kein zweiter Zuwachs)",
      abs(float(st26.population) - _leute26 - 1.0) < 1e-9,
      "%r -> %r" % (_leute26, st26.population))

st26.tick(1800)
st26.tick(1800)
check("P26: zwei halbe Takte ernten dasselbe wie ein ganzer",
      abs(float(ort26.vorraete.get("holz", 0.0)) - 2 * _rate26) < 1e-9, str(ort26.vorraete))
check("P26: das Journal hat jetzt drei Zeilen (ein Eintrag je Takt)",
      len(ort26.produktionsjournal) == 3, str(len(ort26.produktionsjournal)))
check("P26: die Uhr steht auf zwei Stunden",
      abs(float(st26.spielsekunden) - 7200.0) < 1e-9, str(st26.spielsekunden))

pfad_u = temp("uhr_rundlauf.json")
check("P26: der Stand wird geschrieben", bool(st26.save(pfad_u)))
st27 = M.GameState()
check("P26: der Stand wird geladen", st27.load(pfad_u) is True)
check("P26: die Spieluhr ueberlebt Speichern und Laden",
      abs(float(st27.spielsekunden) - 7200.0) < 1e-9, str(st27.spielsekunden))
check("P26: das Journal des Ortes ueberlebt es ebenfalls",
      len(st27.settlements[0].produktionsjournal) == 3,
      str(len(st27.settlements[0].produktionsjournal)))

import json as _json7  # noqa: E402
_roh7 = _json7.load(open(pfad_u, encoding="utf-8"))
_roh7.pop("spielsekunden", None)
_json7.dump(_roh7, open(pfad_u, "w", encoding="utf-8"))
st28 = M.GameState()
check("P26: ein Spielstand OHNE die Uhr laedt weiter (kein Absturz)", st28.load(pfad_u) is True)
check("P26: ... und beginnt dann bei 0", abs(float(st28.spielsekunden)) < 1e-9,
      str(st28.spielsekunden))

check("P26: `tick` bucht die Ernte nicht mehr selbst (eine Formel statt zweier)",
      "rate_pro_stunde * dt_h" not in _q6)
check("P26: der Siedlerzuwachs wird nicht mehr in `tick` gerechnet",
      "siedler_zuwachs_pro_stunde(self.settlements, levels) * dt_h" not in _q6)
check("P26: der Kern ist die Quelle der Ernte im Takt",
      "spieloekonomie.ort_tick(asdict(siedlung), _ab, _bis, levels)" in _q6)


abschnitt("P27: Teil 6c - Ware und Ausbildung VOR ORT (der Kern rechnet, nicht mehr das Reich)")

_karte27, _ = karte_und_felder("grasland", anzahl=3)
check("P27: eine Karte fuer die Werkstatt ist da", _karte27 is not None)
st29 = M.GameState()
ort29 = M.Settlement(name="Werkdorf", map_id="kontinent", karte=_karte27,
                     id=M.siedlung_kennung("spieler", "kontinent", 6, 6))
st29.settlements.append(ort29)
_feld29 = next((i for i, a in enumerate(_karte27["raster"])
                if M.gelaende.bau_moeglich("schmiede", a)[0]), None)
check("P27: es gibt ein Feld fuer die Schmiede", _feld29 is not None, str(_feld29))
_bau29, _meld29 = M.bauen_auf_karte(ort29, "schmiede", _feld29)
check("P27: die Schmiede steht VOR ORT", _bau29, _meld29)
ort29.vorraete = {r: 5000.0 for r in M.RESOURCES}
# Die Waren-Voraussetzungen (Forschung) sind hier nicht der Pruefgegenstand - dieser Test prueft
# Warteschlange und Ankunft VOR ORT. Deshalb die Forschung freischalten, damit das Schwert (die
# EINZIGE Ware mit belegter Dauer: 1200 s) wirklich herstellbar ist.
for _r29 in st29.research.values():
    _r29.level = int(_r29.max_level)

app29 = M.NebelseetalApp.__new__(M.NebelseetalApp)
app29.state = st29
app29.content = None
app29._log = lambda msg: st29.log.append(msg)
app29._render_view = lambda: None

# Das Handbuch belegt die Dauer nur fuer EINE Ware - eine Ware ohne Dauer bleibt ehrlich wartend.
_kand29 = [w for w in M.werkstatt.waren_der_werkstatt("schmiede")
           if st29.ware_voraussetzung(w)[0]]
ware29 = next((w for w in _kand29 if M.werkstatt.dauer_sekunden(w, 1)), None)
check("P27: es gibt eine Ware mit erfuellter Voraussetzung UND belegter Dauer",
      ware29 is not None, str(_kand29))
_waren_reich_vorher = {k: int(v) for k, v in (st29.waren or {}).items()}
check("P27: sie laesst sich VOR ORT einreihen", app29._ware_herstellen(ware29) is True)
check("P27: ... und steht in der Warteschlange DIESES Ortes",
      any(a.get("ware") == ware29 for s in (ort29.werkstaetten or {}).values()
          for a in (s.get("auftraege") or [])), str(ort29.werkstaetten))

_ort29_vorher = int((ort29.waren or {}).get(ware29, 0))
st29.spielsekunden = float(st29.spielsekunden) + float(M.werkstatt.dauer_sekunden(ware29, 1)) + 1.0
st29.tick(0.0)
check("P27: nach der Rezeptzeit liegt die Ware im ORTSLAGER",
      int((ort29.waren or {}).get(ware29, 0)) == _ort29_vorher + 1, str(ort29.waren))
check("P27: der Takt meldet sie zurueck (dafuer wird neu gezeichnet)",
      any(ware29 in z for z in st29.log[-3:]), str(st29.log[-3:]))
check("P27: das Warenlager des REICHS bleibt unberuehrt (nur der Ort arbeitet)",
      {k: int(v) for k, v in (st29.waren or {}).items()} == _waren_reich_vorher,
      str(st29.waren))
st29.tick(0.0)
check("P27: ein zweiter Takt bucht die Ware NICHT noch einmal",
      int((ort29.waren or {}).get(ware29, 0)) == _ort29_vorher + 1, str(ort29.waren))

_q7 = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
check("P27: die Herstellung geht ueber den Kern (ware_start)", "spieloekonomie.ware_start(" in _q7)
check("P27: die Ausbildung geht ueber den Kern (ausbildung_start)",
      "spieloekonomie.ausbildung_start(" in _q7)
check("P27: der Altpfad 'sofort hochzaehlen' ist verschwunden", "u.count += 1" not in _q7)
check("P27: die Herstellung nutzt NICHT mehr die reichsweite Schlange",
      "self.state.werkstatt_schlangen().get(kennung)" not in _q7)
check("P27: die Kaserne zeigt beide Zahlen (vor Ort UND Reich)",
      "Anzahl: {_lokal_k} vor Ort \u00b7 Reich: {u.count}" in _q7)


abschnitt("P28: Teil 6 (Rest) - die Forschung forscht IM ORT")

_q8 = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
check("P28: der Start geht ueber den Kern (forschung_start)",
      "spieloekonomie.forschung_start(" in _q8)
check("P28: der Abschluss laeuft ueber den Kern (forschung_abschluss)",
      "spieloekonomie.forschung_abschluss(" in _q8)
check("P28: der reichsweite Altpfad ist verschwunden",
      "def forschung_fortschreiben" not in _q8)

st30 = M.GameState()
q30 = M.Settlement(name="Denkort", map_id=st30.current_map, x=0, y=0, id="ort-d",
                   forschungsauftrag={"gebiet": "Felderwirtschaft", "zielstufe": 1,
                                      "startzeit": 0.0, "dauer_stunden": 1.0})
st30.settlements = [q30]
_stand30 = st30.forschung_stand()
check("P28: der Stand holt den Auftrag aus dem ORT",
      (_stand30.get("Felderwirtschaft") or {}).get("auftrag") is not None,
      str((_stand30.get("Felderwirtschaft") or {}).get("auftrag")))
check("P28: ein Gebiet ohne Auftrag hat auch keinen im Stand",
      (_stand30.get("Kriegskunst") or {}).get("auftrag") is None)

_stufe30 = int(st30.research["Felderwirtschaft"].level)
st30.spielsekunden = 3601.0
st30.tick(0.0)
check("P28: nach Ablauf steigt die Stufe und der Auftrag ist weg",
      int(st30.research["Felderwirtschaft"].level) == _stufe30 + 1
      and q30.forschungsauftrag is None,
      "%s / %r" % (st30.research["Felderwirtschaft"].level, q30.forschungsauftrag))
check("P28: die Fertigstellung steht im Journal des Ortes",
      any(z.get("art") == "forschung" for z in (q30.fertigjournal or [])),
      str((q30.fertigjournal or [])[-2:]))
st30.tick(0.0)
check("P28: ein zweiter Takt hebt die Stufe NICHT weiter",
      int(st30.research["Felderwirtschaft"].level) == _stufe30 + 1,
      str(st30.research["Felderwirtschaft"].level))

# Ein Spielstand von VOR Teil 6 traegt seine Auftraege reichsweit - sie muessen in einen Ort.
pfad30 = temp("forschung_alt.json")
st31 = M.GameState()
st31.settlements = [M.Settlement(name="Altort", map_id=st31.current_map, id="ort-alt")]
check("P28: der Stand wird geschrieben", bool(st31.save(pfad30)))
import json as _json8  # noqa: E402
_roh8 = _json8.load(open(pfad30, encoding="utf-8"))
_roh8["forschungsauftraege"] = {"Felderwirtschaft": {"gebiet": "Felderwirtschaft", "zielstufe": 1,
                                                     "startzeit": 0.0, "dauer_stunden": 1.0}}
_json8.dump(_roh8, open(pfad30, "w", encoding="utf-8"))
st32 = M.GameState()
check("P28: der alte Stand laedt weiter (kein Absturz)", st32.load(pfad30) is True)
check("P28: der reichsweite Auftrag ist in den ORT umgezogen",
      bool((st32.settlements[0].forschungsauftrag or {}).get("gebiet"))
      and st32.forschungsauftraege == {},
      "%r / %r" % (st32.settlements[0].forschungsauftrag, st32.forschungsauftraege))


abschnitt("P29: Teil 7 - der Gratisgewinn beim Handel ist GESPERRT")

_q9 = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
check("P29: die erfundene Gratis-Menge ist verschwunden",
      "random.randint(15, 35)" not in _q9 and "gains[res] * bonus" not in _q9)
check("P29: der Handel laeuft jetzt ueber die EINE Maske (Ware, Menge, Preis)",
      '"type": "handel"' in _q9 and "def _handel_maske" in _q9 and "def handel_mit_bot" in _q9)
_kern9 = open(os.path.join(SRC, "spieloekonomie.py"), encoding="utf-8").read()
check("P29: der Kern hat den bestaetigten Kaufvertrag (der naechste Schritt)",
      all(("def %s(" % f) in _kern9 for f in ("handel_start", "handel_entscheiden",
                                              "handel_abschluss")))

st33 = M.GameState()
# Ein Bot wie im Spiel gebaut (ein frischer Zustand hat noch keine Weltkarte und damit keine Bots).
_roh_bot33 = M.asdict(M.BOTS[0])
_roh_bot33.update({"name": "Probe-Bot", "trading": 0.9, "gehandelt": 0})
_bot33 = M.BotPlayer(**_roh_bot33)
check("P29: der Probe-Bot handelt gern (Handelsneigung 90 %)", float(_bot33.trading) == 0.9,
      str(_bot33.trading))
app33 = M.NebelseetalApp.__new__(M.NebelseetalApp)
app33.state = st33
app33.content = None
app33._log = lambda msg: st33.log.append(msg)
app33._render_view = lambda: None
_roh33 = {k: float(v.amount) for k, v in st33.resources.items()}
_ruf33 = int(st33.ruf)
check("P29: ohne eigene Siedlung wird der Handel ehrlich abgelehnt",
      app33._trade(_bot33) is False)
check("P29: NICHTS wird gebucht (kein Rohstoff, kein Ruf, kein Handelszaehler)",
      {k: float(v.amount) for k, v in st33.resources.items()} == _roh33
      and int(st33.ruf) == _ruf33 and int(_bot33.gehandelt) == 0,
      "Ruf %s, gehandelt %s" % (st33.ruf, _bot33.gehandelt))
check("P29: die Meldung nennt den Grund",
      any("eigene Siedlung" in z for z in st33.log[-2:]), str(st33.log[-2:]))


# --------------------------------------------------------------------------
abschnitt("P30: Teil 7b - der BESTAETIGTE KAUFVERTRAG (Auditteil 8b)")

_schwelle30 = float(M.botkern.handelspreis(
    M.botkern.referenzpreis_aus_beschaffung(M.BOT_BESCHAFFUNGSKOSTEN), 0.0))
check("P30: der Schwellenpreis ist die belegte Formel (250 x 1,2)",
      abs(_schwelle30 - 300.0) < 1e-9, str(_schwelle30))


def neuer_handel(gold_ort=0.0, gold_reich=2000.0, karren_ort=1, karren_reich=0,
                 bot_vorraete=None, trading=0.9, temperament=0.0, x=3, y=7):
    """Ein Spielstand mit EINEM Ort (Kaeufer) und EINEM Bot (Verkaeufer)."""
    z = M.GameState()
    ort = M.Settlement(name="Waldort", map_id=z.current_map, x=x, y=y,
                       id=M.siedlung_kennung("spieler", z.current_map, x, y),
                       vorraete={"holz": 10.0, "gold": float(gold_ort)},
                       einheiten=({"Handelskarawane": int(karren_ort)} if karren_ort else {}),
                       importiert={})
    z.settlements = [ort]
    z.aktive_siedlung_id = ort.id
    z.resources["gold"].amount = float(gold_reich)
    if karren_reich and "Handelskarawane" in z.units:
        z.units["Handelskarawane"].count = int(karren_reich)
    bot = M.BotPlayer(name="Probe-Bot", faction="nord", aggression=0.5, trading=trading,
                      temperament=temperament,
                      vorraete=dict(bot_vorraete if bot_vorraete is not None
                                    else {"holz": 500, "gold": 100}))
    z.bots = [bot]
    return z, ort, bot


def spielergold(z, ort):
    """Das Gold des Spielers: Reich + Ortslager + das AM VERTRAG gesperrte Kaufgold."""
    summe = float(z.resources["gold"].amount) + float(ort.vorraete.get("gold", 0.0))
    for e in z.auftraege:
        if e.get("fremdvertrag") and e.get("kaeufer_owner") == "spieler":
            summe += float(e.get("sperrgold") or 0.0)
    return summe


# (a) Der Bot als ORTSDICT: bot_als_dict fuehrt die Handelsfelder wirklich nicht.
_z30, _o30, _b30 = neuer_handel()
check("P30: das Reichsheer kennt die Handelskarawane", "Handelskarawane" in _z30.units,
      str(sorted(_z30.units)))
_d30 = _z30.bot_als_dict(_b30)
check("P30: bot_als_dict fuehrt die Handelsfelder NICHT (gemessen, nicht angenommen)",
      not ({"besitzer", "dimension", "einheiten", "x", "y"} & set(_d30)),
      "unerwartet vorhanden: %s" % sorted({"besitzer", "dimension", "einheiten", "x", "y"} & set(_d30)))
_ort30 = _z30.bot_als_ort(_b30, 10, 10, 1)
check("P30: bot_als_ort ist ein FREMDER Ort mit Besitzer, Dimension, Lage und Lager",
      _ort30["besitzer"] != "spieler" and int(_ort30["dimension"]) == 1
      and int(_ort30["x"]) == 10 and int(_ort30["y"]) == 10
      and isinstance(_ort30["vorraete"], dict) and float(_ort30["vorraete"].get("holz", 0)) == 500.0,
      str(sorted(_ort30)))
check("P30: Karawanen kommen aus Ortslager UND Reichsheer",
      _z30.handelskarawanen_bestand(_o30) == {"Handelskarawane": 1},
      str(_z30.handelskarawanen_bestand(_o30)))
_z30.units["Handelskarawane"].count = 2
if "Handkarren" in _z30.units:
    _z30.units["Handkarren"].count = 7
check("P30: Handkarren handeln NICHT (Handbuch S. 20)",
      _z30.handelskarawanen_bestand(_o30) == {"Handelskarawane": 3},
      str(_z30.handelskarawanen_bestand(_o30)))

_cfg30 = next((m for m in M.MAPS if m["id"] == _z30.current_map), None)
_mitte30 = int(_cfg30["size"]) // 2 if _cfg30 else 10
check("P30: der Bot-Standort ist die Kartenmitte (Bots fuehren keine Koordinaten)",
      _z30.bot_standort(_o30) == (_mitte30, _mitte30), str(_z30.bot_standort(_o30)))
_z30b, _o30b, _b30b = neuer_handel(x=_mitte30, y=_mitte30)
check("P30: die ANNAHME rueckt um ein Feld, damit die Strecke nicht 0 ist",
      _z30b.bot_standort(_o30b) != (_mitte30, _mitte30)
      and _z30b.handel_mit_bot(_b30b, _o30b, "holz", 3, _schwelle30, {"Handelskarawane": 1})[0] is True,
      str(_z30b.bot_standort(_o30b)))

# (b) Ehrliche Ablehnungen - ohne jede Buchung.
_z31, _o31, _b31 = neuer_handel(gold_reich=0.0)
_spur31 = json.dumps({"roh": {k: float(v.amount) for k, v in _z31.resources.items()},
                      "ort": _o31.vorraete, "ein": _o31.einheiten, "bot": _b31.vorraete},
                     sort_keys=True)
_weiger31 = [
    _z31.handel_mit_bot(_b31, _o31, "holz", 3, _schwelle30, {"Handelskarawane": 1}),      # 0 Gold
    _z31.handel_mit_bot(_b31, _o31, "holz", 3, _schwelle30, {}),                          # keine Karawane
    _z31.handel_mit_bot(_b31, _o31, "holz", 3, _schwelle30, {"Handkarren": 1}),           # falscher Karren
    _z31.handel_mit_bot(_b31, _o31, "gold", 3, _schwelle30, {"Handelskarawane": 1}),      # Gold als Ware
    _z31.handel_mit_bot(_b31, _o31, "metall", 3, _schwelle30, {"Handelskarawane": 1}),    # nicht im Angebot
    _z31.handel_mit_bot(_b31, _o31, "holz", 0, _schwelle30, {"Handelskarawane": 1}),      # Menge 0
    _z31.handel_mit_bot(_b31, _o31, "holz", -3, _schwelle30, {"Handelskarawane": 1}),     # Menge negativ
    _z31.handel_mit_bot(_b31, _o31, "holz", 2.5, _schwelle30, {"Handelskarawane": 1}),    # halbe Stuecke
    _z31.handel_mit_bot(_b31, _o31, "holz", 3, 0.0, {"Handelskarawane": 1}),              # Preis 0
    _z31.handel_mit_bot(_b31, _o31, "holz", 3, -1.0, {"Handelskarawane": 1}),             # Preis negativ
    _z31.handel_mit_bot(_b31, _o31, "holz", 99999, _schwelle30, {"Handelskarawane": 1}),  # ueberladen
    _z31.handel_mit_bot(_b31, _o31, "holz", 3, _schwelle30, {"Handelskarawane": "x"}),    # keine Zahl
]
check("P30: zwoelf ehrliche Ablehnungen", all(o is False for o, _m in _weiger31)
      and len(_weiger31) == 12, str([o for o, _m in _weiger31]))
check("P30: jede Ablehnung nennt einen Grund", all(str(_m).strip() for _o, _m in _weiger31),
      str([_m for _o, _m in _weiger31 if not str(_m).strip()]))
check("P30: keine Ablehnung bucht irgendetwas (Ort, Reich, Bot, Auftraege)",
      json.dumps({"roh": {k: float(v.amount) for k, v in _z31.resources.items()},
                  "ort": _o31.vorraete, "ein": _o31.einheiten, "bot": _b31.vorraete},
                 sort_keys=True) == _spur31 and _z31.auftraege == [],
      str(_z31.auftraege))
_z31b, _o31b, _b31b = neuer_handel(trading=0.1)
check("P30: ein Bot ohne Handelsneigung handelt nicht",
      _z31b.handel_mit_bot(_b31b, _o31b, "holz", 3, _schwelle30, {"Handelskarawane": 1})[0] is False
      and _z31b.auftraege == [])
_z32, _o32, _b32 = neuer_handel(gold_reich=100000.0)
_gedeckt32 = _z32.handel_mit_bot(_b32, _o32, "holz", 600, 1.0, {"Handelskarawane": 1})
check("P30: der Kern lehnt ein nicht gedecktes Angebot ab (Ware des Verkaeufers)",
      _gedeckt32[0] is False and "gedeckt" in str(_gedeckt32[1]) and _z32.auftraege == [],
      str(_gedeckt32))

# (c) Start sperrt beidseitig; der Uebergang aus dem Reich liefert nur den Fehlbetrag.
_z33, _o33, _b33 = neuer_handel(gold_ort=100.0, gold_reich=2000.0, karren_ort=0, karren_reich=1)
_gold33 = spielergold(_z33, _o33)
_ok33, _m33 = _z33.handel_mit_bot(_b33, _o33, "holz", 3, _schwelle30, {"Handelskarawane": 1}, 0.0)
check("P30: das Kaufangebot wird gestartet", _ok33 is True, str(_m33))
_v33 = _z33.auftraege[0] if _z33.auftraege else {}
check("P30: es liegt EIN Fremdvertrag in den Auftraegen",
      len(_z33.auftraege) == 1 and _v33.get("fremdvertrag") is True, str(_z33.auftraege))
check("P30: Ware UND Gold sind gesperrt (beide Seiten verlassen ihre Lager)",
      float(_b33.vorraete.get("holz", 0)) == 497.0 and float(_b33.vorraete.get("gold", 0)) == 100.0
      and float(_o33.vorraete.get("gold", 0)) == 0.0
      and abs(float(_v33.get("sperrgold") or 0) - 900.0) < 1e-9,
      "Bot-Holz %s, Bot-Gold %s, Ort-Gold %s, Sperrgold %s"
      % (_b33.vorraete.get("holz"), _b33.vorraete.get("gold"), _o33.vorraete.get("gold"),
         _v33.get("sperrgold")))
check("P30: die Karawane ist aus dem Ortslager weg", int(_o33.einheiten.get("Handelskarawane", 0)) == 0,
      str(_o33.einheiten))
check("P30: das Reich liefert nur den FEHLBETRAG (Karawane und Gold)",
      int(_z33.units["Handelskarawane"].count) == 0
      and abs(float(_z33.resources["gold"].amount) - 1200.0) < 1e-9,
      "Karren %s, Reichsgold %s" % (_z33.units["Handelskarawane"].count,
                                    _z33.resources["gold"].amount))
check("P30: der Gesamtbestand ist beim Start unveraendert (nichts verschenkt)",
      abs(spielergold(_z33, _o33) - _gold33) < 1e-9, str(spielergold(_z33, _o33)))

# (d) Ankunft und Rueckkehr - der ganze Weg ueber die Auftragsschleife.
_z34, _o34, _b34 = neuer_handel()
_ok34, _m34 = _z34.handel_mit_bot(_b34, _o34, "holz", 3, _schwelle30, {"Handelskarawane": 1}, 0.0)
_v34 = _z34.auftraege[0]
_gold34 = spielergold(_z34, _o34)
_z34.auftraege_fortschreiben(float(_v34["ankunft"]))
check("P30: bei der Ankunft nimmt der Bot an (der Preis erreicht seinen Schwellenpreis)",
      bool(_z34.auftraege) and _z34.auftraege[0].get("entscheidung") is True
      and _z34.auftraege[0].get("angenommen") is True,
      str(_z34.auftraege[0].get("entscheidung")))
check("P30: das gesperrte Gold liegt danach beim Verkaeufer",
      float(_b34.vorraete.get("gold", 0)) == 1000.0, str(_b34.vorraete.get("gold")))
check("P30: bezahlt ist genau der Preis (900 Gold)",
      abs((_gold34 - spielergold(_z34, _o34)) - 900.0) < 1e-9,
      str(_gold34 - spielergold(_z34, _o34)))
_z34.auftraege_fortschreiben(float(_v34["rueckkehr"]))
check("P30: bei der Rueckkehr kommt die Ware ins ORTSLAGER und die Karawane heim",
      float(_o34.vorraete.get("holz", 0)) == 13.0
      and int(_o34.einheiten.get("Handelskarawane", 0)) == 1 and _z34.auftraege == [],
      "Holz %s, Karawane %s, Auftraege %s" % (_o34.vorraete.get("holz"),
                                              _o34.einheiten.get("Handelskarawane"),
                                              len(_z34.auftraege)))
check("P30: das Reichsheer hat die Karawane NICHT zurueckbekommen (sie liegt im Ort)",
      int(_z34.units["Handelskarawane"].count) == 0, str(_z34.units["Handelskarawane"].count))

# (e) Ablehnung: Gold wird nie uebertragen, die Karawane kehrt MIT den Waren zurueck.
_z35, _o35, _b35 = neuer_handel()
_z35.handel_mit_bot(_b35, _o35, "holz", 3, 1.0, {"Handelskarawane": 1}, 0.0)
_v35 = _z35.auftraege[0]
_gold35 = spielergold(_z35, _o35)
_holz35 = float(_o35.vorraete.get("holz", 0))
_z35.auftraege_fortschreiben(float(_v35["rueckkehr"]))
check("P30: ein zu niedriger Preis wird bei der Ankunft ABGELEHNT (belegte Regel)",
      _v35.get("entscheidung") is False and _v35.get("angenommen") is False,
      str(_v35.get("entscheidung")))
check("P30: Gold wurde NIE uebertragen", float(_b35.vorraete.get("gold", 0)) == 100.0,
      str(_b35.vorraete.get("gold")))
check("P30: die Ware des Verkaeufers ist unversehrt zurueck",
      float(_b35.vorraete.get("holz", 0)) == 500.0, str(_b35.vorraete.get("holz")))
check("P30: der Kaeufer hat Gold und Karawane vollstaendig zurueck",
      abs(spielergold(_z35, _o35) - _gold35) < 1e-9
      and int(_o35.einheiten.get("Handelskarawane", 0)) == 1
      and float(_o35.vorraete.get("holz", 0)) == _holz35 and _z35.auftraege == [],
      "Gold %s, Karawane %s, Holz %s" % (spielergold(_z35, _o35),
                                         _o35.einheiten.get("Handelskarawane"),
                                         _o35.vorraete.get("holz")))

# (f) Kein doppelter Abschluss.
_z36, _o36, _b36 = neuer_handel()
_z36.handel_mit_bot(_b36, _o36, "holz", 3, _schwelle30, {"Handelskarawane": 1}, 0.0)
_v36 = _z36.auftraege[0]
_z36._fremdvertrag_buchen(_v36, float(_v36["rueckkehr"]))
_h36 = float(_o36.vorraete.get("holz", 0))
_g36 = float(_b36.vorraete.get("gold", 0))
for _i in range(3):
    _z36._fremdvertrag_buchen(_v36, float(_v36["rueckkehr"]) + 1000.0 * (_i + 1))
check("P30: dreimal nachbuchen doppelt nichts",
      float(_o36.vorraete.get("holz", 0)) == _h36 and float(_b36.vorraete.get("gold", 0)) == _g36
      and int(_o36.einheiten.get("Handelskarawane", 0)) == 1,
      "Holz %s, Bot-Gold %s" % (_o36.vorraete.get("holz"), _b36.vorraete.get("gold")))

# (g) Quelltextwachen.
check("P30: die Auftragsschleife bucht den Fremdvertrag und laesst ihn nicht im Reich landen",
      "self._fremdvertrag_buchen(eintrag, jetzt)" in _q9
      and 'if eintrag.get("eigentransport") or eintrag.get("fremdvertrag")' in _q9)
check("P30: der Gratisgewinn ist und bleibt weg",
      "random.randint(15, 35)" not in _q9 and "gains[res]" not in _q9)
check("P30: die Maske laesst Ware, Menge und Preis waehlen",
      all(m in _q9 for m in ("def _handel_maske", "var_ware", "e_menge", "e_preis",
                             "def _handel_ausfuehren")))
check("P30: der Auftragskern wendet einen Fremdvertrag nicht an (eine Buchung)",
      'e.get("eigentransport") or e.get("fremdvertrag")'
      in open(os.path.join(SRC, "auftraege.py"), encoding="utf-8").read())


# --------------------------------------------------------------------------
abschnitt("P31: Teil 8a - die Kartenfreischaltung ist ehrlich (die Vermessung entfaellt)")

# Entwurf Z. 785 woertlich: "Vermessung-Abfrage entfaellt im neuen Siedlungspfad. Kartenangebote
# sind kein MAPS-Regionsunlock. Alte fuenf Weltregionen nicht als neue Siedlungskarten verkaufen."
# Gemessen (nicht angenommen): `_unlock_next_map` hatte KEINEN Aufrufer und benutzte
# `MAX_ACTIVE_MAPS`, das im ganzen Projekt nirgends definiert ist - ein Aufruf waere mit
# `NameError` gestorben. Und die abgefragte Forschung "vermessung" gibt es unter den 21
# Originalforschungen nicht (Wache: tests/test_spieloekonomie.py, Z. 198).
_q10 = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
check("P31: die Methode _unlock_next_map ist fort (sie hatte keinen Aufrufer)",
      "def _unlock_next_map" not in _q10)
check("P31: keine Abfrage einer Forschung 'vermessung' mehr",
      '"vermessung"' not in _q10)
check("P31: die tote Konstante MAX_ACTIVE_MAPS wird nicht mehr benutzt",
      ">= MAX_ACTIVE_MAPS" not in _q10)
check("P31: niemand schaltet eine Weltregion frei (kein unlocked_maps.append)",
      "unlocked_maps.append" not in _q10 and "active_maps.append" not in _q10)
check("P31: die falsche Zusage im Gebietspanel ('Zugang: die Forschung ...') ist weg",
      'text="Zugang: die Forschung' not in _q10)
check("P31: an ihrer Stelle steht die ehrliche Begruendung",
      "21 Originalforschungen" in _q10 and "sind keine Siedlungskarten" in _q10,
      "Originalforschungen: %s / Siedlungskarten: %s"
      % ("21 Originalforschungen" in _q10, "sind keine Siedlungskarten" in _q10))
check("P31: der Weg zu neuen Karten bleibt der Kartenvorrat (Teil 5)",
      "spieloekonomie.absicht(" in _q10 and "freie_koloniekarten()" in _q10)

# (a) Eine Gruendung schaltet KEINE Weltregion frei (kein Regionsunlock durch Kartenangebote).
st18 = M.GameState()
app18 = M.NebelseetalApp.__new__(M.NebelseetalApp)   # ohne Fenster: nur die Methoden
app18.state = st18
app18.content = None
app18._log = lambda msg: st18.log.append(msg)
app18._render_view = lambda: None
app18._found_settlement()
check("P31: die erste Gruendung laeuft (Vorbedingung)", len(st18.settlements) == 1,
      str(len(st18.settlements)))
check("P31: sie schaltet KEINE Weltregion frei",
      (list(st18.unlocked_maps), list(st18.active_maps)) == (["kontinent"], ["kontinent"]),
      str((st18.unlocked_maps, st18.active_maps)))
check("P31: die Gruendungswege fassen die Sperrliste nicht an (keine Region wird freigeschaltet)",
      all("unlocked_maps" not in _inspect5.getsource(_fn18)
          and "active_maps" not in _inspect5.getsource(_fn18)
          for _fn18 in (M.NebelseetalApp._found_settlement, M.NebelseetalApp._kolonie_gruenden,
                        M.NebelseetalApp._gruendung_ausfuehren)))

# (c) Ein KARTENANGEBOT (Kolonie) ist kein Regionsunlock - der ganze Weg mit echten Werten.
st19 = M.GameState()
st19.kartenvorrat_anlegen("probe18")
q19 = M.Settlement(name="Mutter", map_id=st19.current_map, x=0, y=0,
                   id=M.siedlung_kennung("spieler", st19.current_map, 0, 0),
                   karte=M.spieloekonomie.startkarte("probe18", "spieler"))
q19.vorraete = {"holz": 700.0, "stein": 450.0, "nahrung": 350.0}
q19.bevoelkerung = 20.0
st19.settlements = [q19]
st19.research["Wagenbau"].level = 1
st19.units["Siedlerkarren"].count = 1
_regionen19 = (list(st19.unlocked_maps), list(st19.active_maps))
_ok19, _meldung19, _a19 = st19.gruendung_pruefen(q19, "ausgleich_a", (3, 0))
check("P31: eine Kolonie ist mit Wagenbau, Karren und Mindestbestand moeglich (Vorbedingung)",
      _ok19, _meldung19)
_ok19b, _meldung19b = st19.gruendung_ausfuehren(q19, "ausgleich_a", (3, 0))
check("P31: die Kolonie wird gegruendet (Vorbedingung)", _ok19b, _meldung19b)
check("P31: die zweite Siedlung steht (die Karte kam aus dem Kartenvorrat)",
      len(st19.settlements) == 2, str(len(st19.settlements)))
check("P31: das Kartenangebot ist KEIN Regionsunlock (Sperrliste unveraendert)",
      (list(st19.unlocked_maps), list(st19.active_maps)) == _regionen19,
      str((st19.unlocked_maps, st19.active_maps)))

# (b) Die fuenf Weltregionen sind keine Siedlungskarten.
_regions_ids18 = {str(m["id"]) for m in M.MAPS}
_karten_ids18 = set(st18.kartenvorrat)
check("P31: es sind fuenf Weltregionen", len(_regions_ids18) == 5, str(sorted(_regions_ids18)))
check("P31: die Kartenvorrats-IDs sind keine Regions-IDs",
      not (_karten_ids18 & _regions_ids18), str(sorted(_karten_ids18 & _regions_ids18)))
_regions_namen18 = _regions_ids18 | {str(m["name"]) for m in M.MAPS}
_kartennamen18 = {str(v["karte"].get("typ_name", "")) for v in st18.kartenvorrat.values()}
check("P31: keine Karte traegt einen Regionsnamen (keine Region wird als Karte verkauft)",
      bool(_kartennamen18) and not (_kartennamen18 & _regions_namen18),
      str(sorted(_kartennamen18)))


# --------------------------------------------------------------------------
abschnitt("P32: Teil 8b - Speicherung und Migration (Version, Modus, Warnhinweis)")

# Entwurf Z. 789 woertlich: "Ist ein Altspielstand ohne Versionsfeld vorhanden, mode=\"legacy\",
# Regeln und Punktziel behalten, Warnhinweis anzeigen. Neue Partien mode=\"oeokonomie-1\"."
# "Ohne explizite Daniel-Entscheidung keine automatische Konvertierung alter Ressourcen."
check("P32: die Konstanten sind da (2 = neue Form, 1 = der alte unversionierte Stand)",
      M.STAND_VERSION == 2 and M.STAND_VERSION_ALT == 1,
      "%s / %s" % (M.STAND_VERSION, M.STAND_VERSION_ALT))
check("P32: die Modi heissen wie in der Uebergabe",
      M.MODUS_NEU == "oeokonomie-1" and M.MODUS_LEGACY == "legacy",
      "%r / %r" % (M.MODUS_NEU, M.MODUS_LEGACY))

# (a) Eine NEUE Partie laeuft als oeokonomie-1 (Version 2).
_st20 = M.GameState()
check("P32: eine neue Partie ist Version 2 und Modus oeokonomie-1",
      _st20.stand_version == 2 and _st20.mode == "oeokonomie-1",
      "%s / %s" % (_st20.stand_version, _st20.mode))

# (b) Der Spielstand traegt beide Felder - und den Tagesrest.
_pfad20 = temp("migration_neu.json")
_st20._day_accum = 3600.0 * 13 + 42.0
check("P32: der neue Spielstand wird geschrieben", bool(_st20.save(_pfad20)))
_roh20 = json.load(open(_pfad20, encoding="utf-8"))
check("P32: der Spielstand traegt stand_version und mode",
      _roh20.get("stand_version") == 2 and _roh20.get("mode") == "oeokonomie-1",
      "%r / %r" % (_roh20.get("stand_version"), _roh20.get("mode")))
check("P32: der Tagesrest wird mitgesichert (Entwurf: 'statt beim Laden auf 0 setzen')",
      abs(float(_roh20.get("_day_accum") or 0.0) - _st20._day_accum) < 1e-9,
      str(_roh20.get("_day_accum")))
_st21 = M.GameState()
check("P32: der Stand wird geladen", _st21.load(_pfad20) is True)
check("P32: Version, Modus und Tagesrest ueberleben den Rundlauf",
      _st21.stand_version == 2 and _st21.mode == "oeokonomie-1"
      and abs(_st21._day_accum - _st20._day_accum) < 1e-9,
      "%s / %s / %s" % (_st21.stand_version, _st21.mode, _st21._day_accum))
check("P32: ein Stand MIT Versionsfeld warnt NICHT",
      not any("Altspielstand" in str(m.get("text")) for m in _st21.messages))

# (c) Ein ALTSPIELSTAND (ohne Versionsfeld) laedt als legacy MIT Warnhinweis - und OHNE Umrechnung.
_pfad21 = temp("migration_alt.json")
_daten21 = dict(_roh20)
for _f in ("stand_version", "mode", "_day_accum"):
    _daten21.pop(_f, None)
check("P32: der Altstand kennt die neuen Felder wirklich nicht",
      not ({"stand_version", "mode", "_day_accum"} & set(_daten21)), str(sorted(_daten21)))
_daten21["resources"]["holz"]["amount"] = 123.5
_daten21["population"] = 7.0
with open(_pfad21, "w", encoding="utf-8") as fh:
    json.dump(_daten21, fh)
_st22 = M.GameState()
check("P32: der Altstand laedt", _st22.load(_pfad21) is True)
check("P32: er laeuft als Modus 'legacy' auf der alten Form (Version 1)",
      _st22.mode == "legacy" and _st22.stand_version == 1,
      "%s / %s" % (_st22.mode, _st22.stand_version))
check("P32: der Warnhinweis ist SICHTBAR (in den Nachrichten, Art 'warnung')",
      any("Altspielstand" in str(m.get("text")) and m.get("type") == "warnung"
          for m in _st22.messages), str(_st22.messages[-2:]))
check("P32: und er steht auch in den Log-Zeilen",
      any("Altspielstand" in str(z) for z in _st22.log), str(_st22.log[-2:]))
check("P32: NICHTS wird umgerechnet (Bestand und Bevoelkerung bleiben, wie sie waren)",
      float(_st22.resources["holz"].amount) == 123.5 and float(_st22.population) == 7.0,
      "%s / %s" % (_st22.resources["holz"].amount, _st22.population))
check("P32: der Tagesrest eines Altstandes beginnt bei 0 (keine erfundene Zahl)",
      abs(float(_st22._day_accum)) < 1e-9, str(_st22._day_accum))
_st22b = M.GameState()
_st22b.load(_pfad21)
check("P32: der Warnhinweis steht genau EINMAL in den Nachrichten (kein Fluten beim Laden)",
      sum(1 for m in _st22b.messages if "Altspielstand" in str(m.get("text"))) == 1,
      str(sum(1 for m in _st22b.messages if "Altspielstand" in str(m.get("text")))))

# (d) Quelltextwachen: das Feld ist ein MERKER, keine Schaltung (Entwurf Z. 1092).
_q11 = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
check("P32: der Spielstand schreibt beide Felder",
      '"stand_version": self.stand_version' in _q11 and '"mode": self.mode' in _q11)
check("P32: das Laden liest sie und kennt den Altstand",
      'data.get("stand_version")' in _q11 and "self.mode = MODUS_LEGACY" in _q11
      and '"type": "warnung"' in _q11)
check("P32: der Modus schaltet NOCH NICHTS - er wird nur gesetzt, gesichert, geladen, gemeldet",
      'self.mode: str = MODUS_NEU' in _q11 and '"mode": self.mode' in _q11
      and 'self.mode = MODUS_LEGACY' in _q11
      and 'self.mode = str(data.get("mode") or MODUS_NEU)' in _q11
      and 'self.mode ==' not in _q11 and "== MODUS_NEU" not in _q11
      and "== MODUS_LEGACY" not in _q11,
      "kein Vergleich auf den Modus - nur Setzen, Sichern, Laden, Melden")
check("P32: die Aktivierung steht nicht im Oekonomiekern",
      "oeokonomie-1" not in open(os.path.join(SRC, "spieloekonomie.py"),
                                 encoding="utf-8").read())


sys.exit(bericht())
