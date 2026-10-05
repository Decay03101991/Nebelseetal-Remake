# -*- coding: ascii -*-
"""Unabhaengige Nachpruefung des oekonomischen Kerns (EIGENE Rechenwege).

Dieses Skript glaubt dem Koordinator NICHT: es liest die Daten selbst
(data/gelaende.json, data/buildings.json, data/spieloekonomie.json und den
Entwurfstext) und rechnet Kontingente, Achsen und Schattenpreis mit eigenem
Code nach. Nur der Siegfilter (Block 4) wird bewusst ueber
spieloekonomie.kartenqualitaet aufgerufen und gegen eigene Handrechnungen
gestellt.

Vier Bloecke:
  (1) Kartenvorrat massell: 2000 feste Saaten x 10 Karten = 20000 Karten.
  (2) Tabelle B woertlich aus dem Entwurfstext gegen die JSON.
  (3) Achsen und Schattenpreis von Hand (Startkarte).
  (4) Gegenprobe der Siegfilter-Aussagen aus Abschnitt A/B.

Aufruf:  python -X utf8 tests/test_oekonomie_kern_unabhaengig.py
"""
from __future__ import annotations

import json
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src, projektwurzel

ROOT, SRC = import_src()

DATA = os.path.join(projektwurzel(), "data")
TEXT = os.path.join(projektwurzel(), "docs", "audits",
                    "entwurf_spieloekonomie_sol_2026-10-05.txt")


def _lade_json(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as fh:
        return json.loads(fh.read())


G = _lade_json("gelaende.json")
B = _lade_json("buildings.json")["gebaeude"]
E = _lade_json("spieloekonomie.json")

GEB = {g["id"]: g for g in B}
NAME = {a["id"]: a["name"] for a in G["gelaendearten"]}
ARTEN = [a["id"] for a in G["gelaendearten"]]
BEBAUBAR = [a["id"] for a in G["gelaendearten"] if a["bebaubar"]]
GESPERRT = [a["id"] for a in G["gelaendearten"] if not a["bebaubar"]]
MINDEST = {k: v for k, v in G["regeln"]["mindestbesatz"].items() if not k.startswith("_")}
SPERR = int(G["regeln"]["sperrfelder"])
MASS = int(G["kartenmass"]["spalten"]) * int(G["kartenmass"]["zeilen"])

VORRAT = G["kartenvorrat"]
KARTEN = [VORRAT["start"]] + list(VORRAT["kolonien"])
KENNUNGEN = [k["id"] for k in KARTEN]
GEW = {k["id"]: k["gewichte"] for k in KARTEN}

# Feste Erwartung aus dem Entwurf (Abschnitt A): Startreferenz der Achsen.
BASIS = (48, 42, 48)


# ==========================================================================
# Eigene Werkzeuge (kein Rueckgriff auf src/spieloekonomie.py)
# ==========================================================================

def meine_karte(saat, gewichte):
    """Eigener Kartengenerator: Kontingente aus der Datei, Positionen per Saat gemischt."""
    raster = []
    for art in ARTEN:
        raster.extend([art] * int(gewichte[art]))
    random.Random(str(saat)).shuffle(raster)
    return raster


def hand_achsen(gewichte):
    """Die drei Achsen allein aus Zaehlung und belegten Ertraegen (4/2)."""
    h = 4 * int(gewichte["wald"]) + 2 * int(gewichte["steppe"])
    s = 4 * int(gewichte["berg"]) + 2 * int(gewichte["huegel"])
    a = 4 * int(gewichte["grasland"]) + 2 * int(gewichte["steppe"])
    return (h, s, a)


def hand_relativ(gewichte):
    achsen = hand_achsen(gewichte)
    return tuple(x / b for x, b in zip(achsen, BASIS))


def ertrag_von(geb_id):
    return GEB[geb_id].get("ertrag_pro_stunde") or {}


def zahl(geb_id, art_id):
    """Ertrag eines Gebaeudes auf einer Gelaendeart direkt aus data/buildings.json."""
    return ertrag_von(geb_id).get(NAME[art_id])


def begrenzen(wert, grenzen):
    return min(grenzen[1], max(grenzen[0], wert))


# ==========================================================================
abschnitt("Block 1: Kartenvorrat massell (20000 Karten aus festen Saaten)")

check("B1: kartenvorrat ist Startkarte + 9 Kolonien",
      len(KARTEN) == 10 and len(VORRAT.get("kolonien") or []) == 9,
      "%d Karten" % len(KARTEN))
check("B1: die zehn Kennungen sind eindeutig und vollstaendig",
      len(set(KENNUNGEN)) == 10, str(KENNUNGEN))
check("B1: Kartenmass der Datei ist 8 x 7 = 56 Felder",
      G["kartenmass"]["spalten"] == 8 and G["kartenmass"]["zeilen"] == 7
      and G["kartenmass"]["felder"] == 56, str(G["kartenmass"]))
check("B1: Datei nennt 40 Bauplaetze und 16 Sperrfelder",
      G["kartenmass"]["bauplaetze"] == 40 and SPERR == 16,
      "bauplaetze=%s sperrfelder=%s" % (G["kartenmass"]["bauplaetze"], SPERR))
check("B1: genau sechs bebaubare Gelaendearten, nur der Sumpf gesperrt",
      len(BEBAUBAR) == 6 and GESPERRT == ["sumpf"], "bebaubar=%s" % BEBAUBAR)

# 2000 zufaellig wirkende, aber fest aufgeschriebene Saaten.
_rng = random.Random("oekonomie-masse-fix-2026-10-05")
SAATEN = ["masse-%04d-%09d" % (i, _rng.randrange(10 ** 9)) for i in range(2000)]

gesamt = 0
v_felder = v_bebau = v_sumpf = v_mindest = 0
v_id = {kid: 0 for kid in KENNUNGEN}

for saat in SAATEN:
    for eintrag in KARTEN:
        kid = eintrag["id"]
        raster = meine_karte("%s:%s" % (saat, kid), eintrag["gewichte"])
        gesamt += 1
        z = {art: raster.count(art) for art in ARTEN}
        ok_felder = len(raster) == MASS
        ok_bebau = sum(z[a] for a in BEBAUBAR) == MASS - SPERR
        ok_sumpf = sum(z[a] for a in GESPERRT) == SPERR
        ok_mindest = all(z.get(a, 0) >= m for a, m in MINDEST.items())
        if not ok_felder:
            v_felder += 1
        if not ok_bebau:
            v_bebau += 1
        if not ok_sumpf:
            v_sumpf += 1
        if not ok_mindest:
            v_mindest += 1
        if not (ok_felder and ok_bebau and ok_sumpf and ok_mindest):
            v_id[kid] += 1

check("B1: mindestens 2000 feste Saaten verwendet", len(SAATEN) >= 2000,
      "%d Saaten" % len(SAATEN))
check("B1: Gesamtzahl gepruefter Karten", gesamt == len(SAATEN) * len(KARTEN),
      "%d Karten (10 je Saat)" % gesamt)
check("B1: jede Karte hat 56 Felder -- 0 Verstoesse", v_felder == 0,
      "%d Verstoesse von %d Karten" % (v_felder, gesamt))
check("B1: jede Karte hat 40 bebaubare Felder -- 0 Verstoesse", v_bebau == 0,
      "%d Verstoesse von %d Karten" % (v_bebau, gesamt))
check("B1: jede Karte hat 16 Sumpf -- 0 Verstoesse", v_sumpf == 0,
      "%d Verstoesse von %d Karten" % (v_sumpf, gesamt))
check("B1: Mindestbesatz (wald>=2, berg>=2, grasland>=3, nebelsee>=1) -- 0 Verstoesse",
      v_mindest == 0, "%d Verstoesse von %d Karten" % (v_mindest, gesamt))

for kid in KENNUNGEN:
    check("B1: Karte '%s' in allen %d Saaten fehlerfrei" % (kid, len(SAATEN)),
          v_id[kid] == 0, "%d Verstoesse der Karte" % v_id[kid])

_r1 = meine_karte("wiederholung", GEW["start"])
_r2 = meine_karte("wiederholung", GEW["start"])
_r3 = meine_karte("anders", GEW["start"])
check("B1: gleiche Saat ergibt dasselbe Raster", _r1 == _r2)
check("B1: andere Saat ergibt ein anderes Raster (Permutation wirkt wirklich)",
      _r1 != _r3)

# Auch die Kontingente der Datei selbst werden geprueft (nicht nur die Karten).
for kid in KENNUNGEN:
    w = GEW[kid]
    check("B1: Kontingent '%s' hat genau die sieben Gelaendearten" % kid,
          set(w) == set(ARTEN), str(sorted(w)))
    check("B1: Kontingent '%s' summiert sich zu 56" % kid, sum(int(w[a]) for a in ARTEN) == MASS,
          str(sum(int(w[a]) for a in ARTEN)))
    check("B1: Kontingent '%s' hat 40 bebaubar und 16 Sumpf" % kid,
          sum(int(w[a]) for a in BEBAUBAR) == 40 and int(w["sumpf"]) == 16,
          "bebaubar=%d sumpf=%d" % (sum(int(w[a]) for a in BEBAUBAR), int(w["sumpf"])))
    check("B1: Kontingent '%s' erfuellt den Mindestbesatz" % kid,
          all(int(w[a]) >= m for a, m in MINDEST.items()), str(MINDEST))


# ==========================================================================
abschnitt("Block 2: Tabelle B woertlich aus dem Entwurfstext gegen die JSON")

with open(TEXT, encoding="utf-8") as fh:
    ZEILEN = fh.read().splitlines()

_gew_idx = next((i for i, l in enumerate(ZEILEN) if "Gewichtetabelle" in l), None)
check("B2: Textblock 'Vollstaendige Gewichtetabelle' gefunden", _gew_idx is not None,
      "Zeile %s" % (None if _gew_idx is None else _gew_idx + 1))

_kopf_idx = None
if _gew_idx is not None:
    _kopf_idx = next((i for i in range(_gew_idx, len(ZEILEN)) if "Kennung" in ZEILEN[i]), None)
check("B2: Kopfzeile mit 'Kennung' gefunden", _kopf_idx is not None,
      "Zeile %s" % (None if _kopf_idx is None else _kopf_idx + 1))

TEXT_TAB = {}
if _kopf_idx is not None:
    for l in ZEILEN[_kopf_idx + 1:]:
        zellen = [c.strip() for c in l.split("|")]
        if (len(zellen) == 8 and zellen[0] in KENNUNGEN
                and all(re.fullmatch(r"\d+", c) for c in zellen[1:])):
            TEXT_TAB[zellen[0]] = tuple(int(c) for c in zellen[1:])
        if len(TEXT_TAB) == 10:
            break

check("B2: genau 10 Datenzeilen aus dem Text gelesen", len(TEXT_TAB) == 10,
      "%d Zeilen" % len(TEXT_TAB))
check("B2: Zeilenreihenfolge = Startkarte + 9 Kolonien", list(TEXT_TAB.keys()) == KENNUNGEN,
      str(list(TEXT_TAB.keys())))

if _kopf_idx is not None:
    kopf = ZEILEN[_kopf_idx]
    _pos = [kopf.find(NAME[a]) for a in ARTEN]
    check("B2: Spaltenkoepfe stehen in der Reihenfolge Grasland..Sumpf",
          all(p >= 0 for p in _pos) and all(_pos[i] < _pos[i + 1] for i in range(len(_pos) - 1)),
          str(_pos))

JSON_TAB = {kid: tuple(int(GEW[kid][a]) for a in ARTEN) for kid in KENNUNGEN}

for kid in KENNUNGEN:
    nums = TEXT_TAB.get(kid)
    hat7 = nums is not None and len(nums) == 7
    check("B2/%s: Zeile hat genau 7 Zahlen" % kid, hat7, str(nums))
    if not hat7:
        check("B2/%s: erste sechs summieren zu 40" % kid, False, "Zeile fehlt")
        check("B2/%s: Summe aller sieben = 56" % kid, False, "Zeile fehlt")
        check("B2/%s: JSON == Text Zeichen fuer Zeichen" % kid, False, "Zeile fehlt")
        continue
    check("B2/%s: erste sechs Spalten summieren zu 40" % kid, sum(nums[:6]) == 40,
          str(sum(nums[:6])))
    check("B2/%s: Summe aller sieben Spalten = 56" % kid, sum(nums) == 56, str(sum(nums)))
    j = JSON_TAB[kid]
    jt = "|".join(str(x) for x in j)
    tt = "|".join(str(x) for x in nums)
    check("B2/%s: JSON == Text Zeichen fuer Zeichen" % kid, j == nums and jt == tt,
          "JSON %s / Text %s" % (jt, tt))

for kid in KENNUNGEN:
    check("B2: JSON-Kontingent '%s' hat genau die sieben Spalten" % kid,
          set(GEW[kid]) == set(ARTEN), str(sorted(GEW[kid])))


# ==========================================================================
abschnitt("Block 3: Achsen und Schattenpreis von Hand (Startkarte)")

check("B3: holzfaeller liefert auf Wald 4", zahl("holzfaeller", "wald") == 4,
      str(zahl("holzfaeller", "wald")))
check("B3: holzfaeller liefert auf Steppe 2", zahl("holzfaeller", "steppe") == 2,
      str(zahl("holzfaeller", "steppe")))
check("B3: steinmetz liefert auf Berg 4", zahl("steinmetz", "berg") == 4,
      str(zahl("steinmetz", "berg")))
check("B3: steinmetz liefert auf Huegel 2", zahl("steinmetz", "huegel") == 2,
      str(zahl("steinmetz", "huegel")))
check("B3: farm liefert auf Grasland 4", zahl("farm", "grasland") == 4,
      str(zahl("farm", "grasland")))
check("B3: farm liefert auf Steppe 2", zahl("farm", "steppe") == 2,
      str(zahl("farm", "steppe")))
check("B3: goldmine liefert auf Berg 3 (bester Goldertrag)", zahl("goldmine", "berg") == 3,
      str(zahl("goldmine", "berg")))

_s = GEW["start"]
_H = 4 * int(_s["wald"]) + 2 * int(_s["steppe"])
_S = 4 * int(_s["berg"]) + 2 * int(_s["huegel"])
_A = 4 * int(_s["grasland"]) + 2 * int(_s["steppe"])
check("B3: Handachse H = 4*Wald + 2*Steppe = 48", _H == 48, str(_H))
check("B3: Handachse Gestein = 4*Berg + 2*Huegel = 42", _S == 42, str(_S))
check("B3: Handachse Agrar = 4*Grasland + 2*Steppe = 48", _A == 48, str(_A))
check("B3: Startachsentripel von Hand = (48, 42, 48)", (_H, _S, _A) == BASIS,
      str((_H, _S, _A)))

# Handrechnung einzelner Karten gegen die Ertragsobergrenzen-Tabelle (Entwurf A).
_erwartet = {"holz": (116, 20, 16), "minen": (12, 108, 16), "farmen": (20, 12, 120)}
for kid, soll in _erwartet.items():
    ist = hand_achsen(GEW[kid])
    check("B3: Handachsen '%s' = (Holz, Stein, Agrar) %s" % (kid, soll), ist == soll,
          "ist %s" % str(ist))

# Schattenpreis von Holz auf der STARTKARTE, von Hand.
_best_gold = max(zahl("goldmine", "berg"), zahl("goldmine", "huegel"))
_best_holz = max(zahl("holzfaeller", "wald"), zahl("holzfaeller", "steppe"))
_grund = _best_gold / _best_holz
_hand_start_kap = (int(_s["wald"]) * zahl("holzfaeller", "wald")
                   + int(_s["steppe"]) * zahl("holzfaeller", "steppe"))
_kartenfaktor = begrenzen(_hand_start_kap / _hand_start_kap, E["kartenpreisgrenzen"])
_vorratsfaktor = begrenzen(2 * 100 / (100 + 100), E["vorratspreisgrenzen"])
_hand_preis = _grund * _kartenfaktor * _vorratsfaktor

check("B3: bester Goldertrag = 3", _best_gold == 3, str(_best_gold))
check("B3: bester Holzertrag = 4", _best_holz == 4, str(_best_holz))
check("B3: Grundpreis Holz = bester Goldertrag / bester Holzertrag = 3/4 = 0.75",
      abs(_grund - 0.75) < 1e-12, "%.10f" % _grund)
check("B3: Kartenfaktor Start/Start = 1.0", abs(_kartenfaktor - 1.0) < 1e-12, str(_kartenfaktor))
check("B3: Vorratsfaktor bei Bestand == Reserve = 1.0", abs(_vorratsfaktor - 1.0) < 1e-12,
      str(_vorratsfaktor))
check("B3: Handschattenpreis Holz auf Startkarte = 0.7500", abs(_hand_preis - 0.75) < 1e-9,
      "%.10f" % _hand_preis)

# Vergleich mit dem Kern.
import spieloekonomie as O
_start = O.startkarte("unabhaengig", "spieler")
check("B3: spieloekonomie.achsen(Start) == Handwert (48, 42, 48)",
      tuple(O.achsen(_start)) == (_H, _S, _A), str(O.achsen(_start)))
check("B3: spieloekonomie.relativ(Start) == (1, 1, 1)",
      all(abs(x - 1.0) < 1e-9 for x in O.relativ(_start)), str(O.relativ(_start)))
check("B3: spieloekonomie.schattenpreis(Start, holz, 100, 100) == Handwert 0.7500",
      abs(O.schattenpreis(_start, "holz", 100, 100) - _hand_preis) < 1e-9,
      str(O.schattenpreis(_start, "holz", 100, 100)))


# ==========================================================================
abschnitt("Block 4: Gegenprobe der Siegfilter-Aussagen (Entwurf Abschnitt A/B)")

_start4 = O.startkarte("sieg", "spieler")
_vorrat4 = O.vorrat("sieg")
_kk = {kid: _vorrat4[kid]["karte"] for kid in _vorrat4}


def _hand_beste(gewichte_liste):
    werte = [hand_relativ(w) for w in gewichte_liste]
    return tuple(max(w[i] for w in werte) for i in range(3))


def _hand_mittel(gewichte_liste):
    werte = [hand_relativ(w) for w in gewichte_liste]
    return tuple(sum(w[i] for w in werte) / len(werte) for i in range(3))


# --- Aussage A: Start + nur ausgeglichene Karten kann nie gewinnen ----------
_setA = [_start4, _kk["ausgleich_a"], _kk["ausgleich_b"], _kk["ausgleich_c"]]
_qA = O.kartenqualitaet(_setA)
check("B4: Start + NUR ausgeglichene Karten erfuellt den Siegfilter NICHT",
      _qA["erfuellt"] is False, str(_qA["beste"]))
check("B4: bester Holzfaktor = 1.1250", round(_qA["beste"][0], 4) == 1.125,
      "%.4f" % _qA["beste"][0])
check("B4: bester Gesteinsfaktor = 1.0476 (Entwurf: hoechstens 1,0476)",
      round(_qA["beste"][1], 4) == 1.0476, "%.4f" % _qA["beste"][1])
check("B4: bester Agrarfaktor = 1.0417", round(_qA["beste"][2], 4) == 1.0417,
      "%.4f" % _qA["beste"][2])
check("B4: min(beste) liegt unter der Spezialistenschwelle 1.4",
      min(_qA["beste"]) < E["spezialistenfaktor"], "%.4f < %.4f"
      % (min(_qA["beste"]), E["spezialistenfaktor"]))

_gewA = [GEW["start"], GEW["ausgleich_a"], GEW["ausgleich_b"], GEW["ausgleich_c"]]
check("B4: Handrechnung bester Holzfaktor = 1.1250", round(_hand_beste(_gewA)[0], 4) == 1.125,
      "%.4f" % _hand_beste(_gewA)[0])
check("B4: Handrechnung (beste) deckt sich mit kartenqualitaet",
      all(abs(a - b) < 5e-5 for a, b in zip(_hand_beste(_gewA), _qA["beste"])),
      "%s vs %s" % (tuple(round(x, 4) for x in _hand_beste(_gewA)),
                    tuple(round(x, 4) for x in _qA["beste"])))
check("B4: Handrechnung (mittel) deckt sich mit kartenqualitaet",
      all(abs(a - b) < 5e-5 for a, b in zip(_hand_mittel(_gewA), _qA["mittel"])),
      "%s vs %s" % (tuple(round(x, 4) for x in _hand_mittel(_gewA)),
                    tuple(round(x, 4) for x in _qA["mittel"])))

# --- Aussage B: Start + Holz + Minen + Farmen besteht ----------------------
_setB = [_start4, _kk["holz"], _kk["minen"], _kk["farmen"]]
_qB = O.kartenqualitaet(_setB)
check("B4: Start + Holz + Minen + Farmen besteht die Kartenpruefung",
      _qB["erfuellt"] is True, str(_qB["beste"]))
check("B4: Achsenmittel = (1.0208; 1.0833; 1.0417)",
      all(round(a, 4) == b for a, b in zip(_qB["mittel"], (1.0208, 1.0833, 1.0417))),
      str(tuple(round(a, 4) for a in _qB["mittel"])))
check("B4: beste Einzelwerte = (2.4167; 2.5714; 2.5000)",
      all(round(a, 4) == b for a, b in zip(_qB["beste"], (2.4167, 2.5714, 2.5000))),
      str(tuple(round(a, 4) for a in _qB["beste"])))
check("B4: Spezialistennachweis erfuellt (min(beste) >= 1.4)",
      min(_qB["beste"]) >= E["spezialistenfaktor"],
      "%.4f >= %.4f" % (min(_qB["beste"]), E["spezialistenfaktor"]))

_gewB = [GEW["start"], GEW["holz"], GEW["minen"], GEW["farmen"]]
check("B4: Handmittel (Holz, Stein, Agrar) deckt sich mit kartenqualitaet",
      all(abs(a - b) < 5e-5 for a, b in zip(_hand_mittel(_gewB), _qB["mittel"])),
      "%s vs %s" % (tuple(round(x, 4) for x in _hand_mittel(_gewB)),
                    tuple(round(x, 4) for x in _qB["mittel"])))
check("B4: Handbeste deckt sich mit kartenqualitaet",
      all(abs(a - b) < 5e-5 for a, b in zip(_hand_beste(_gewB), _qB["beste"])),
      "%s vs %s" % (tuple(round(x, 4) for x in _hand_beste(_gewB)),
                    tuple(round(x, 4) for x in _qB["beste"])))

# --- Zusatz: Start + die drei Mischungen besteht (Entwurf Z. 101) ----------
_setC = [_start4, _kk["holz_minen"], _kk["holz_farmen"], _kk["minen_farmen"]]
_qC = O.kartenqualitaet(_setC)
check("B4: Start + die drei Mischungen besteht die Kartenpruefung",
      _qC["erfuellt"] is True, str(_qC["beste"]))
check("B4: Spezialistennachweise der Mischungen = (1.4167; 1.4762; 1.5000)",
      all(round(a, 4) == b for a, b in zip(_qC["beste"], (1.4167, 1.4762, 1.5))),
      str(tuple(round(a, 4) for a in _qC["beste"])))
_setD = [_kk["holz"], _kk["minen"], _kk["farmen"]]
_qD = O.kartenqualitaet(_setD)
check("B4: die drei reinen Karten allein bestehen NICHT (nur 3 < mindestsiedlungen 4)",
      _qD["erfuellt"] is False and len(_setD) < E["mindestsiedlungen"],
      "erfuellt=%s, %d Karten" % (_qD["erfuellt"], len(_setD)))


sys.exit(bericht())
