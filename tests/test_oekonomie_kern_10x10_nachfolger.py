# -*- coding: ascii -*-
"""10x10-Nachfolger der unabhaengigen Oekonomie-Pruefung (Nebelseetal-Remake).

WARUM DIESE DATEI
  Der Vorgaenger tests/test_oekonomie_kern_unabhaengig.py stammt aus der
  8x7-Zeit und bleibt als Vorgaengerarbeit liegen. Er bricht heute mit
  KeyError: 'kartenmass', weil data/gelaende.json seit der Umstellung auf den
  Originalkarten-Katalog (28.10.2026) weder "kartenmass" noch "kartenvorrat"
  fuehrt. Diese Datei prueft DIESELBEN Zusagen neu, aber auf dem echten Raster -
  mit eigenen Rechenwegen, ohne dem Koordinator zu glauben.

RASTERSTAND (Quelle, nicht geraten)
  data/originalkarten/katalog.json
      "mass":       {"spalten": 10, "zeilen": 10}
      je Karte:     "rastermass": {"spalten": 10, "zeilen": 10}
                    "spielraster": 100 Gelaendefelder
  src/originalkarten.py (_katalog) bricht ab, wenn "mass" nicht 10x10 ist, und
  karte() bricht ab, wenn ein Raster nicht genau 100 Felder hat.
  Also: 10 Spalten x 10 Zeilen = 100 Felder je Karte.

GEPRUEFTE ZUSAGEN (Nachfolger der vier Bloecke des Vorgaengers)
  1  Feldzahl 100 je Karte, Raster gegen Quellzahl, Katalogzaehlung.
  2  Kartenvorrat: Startkarte + Kolonien, eindeutige Kennungen, reproduzierbar -
     und der 8x7-Weg ist wirklich stillgelegt (Ersatz fuer "Mass ist 8x7").
  3  Ertragswerte je Gelaende aus data/buildings.json (Vorgaengerblock B3).
  4  Achsen von Hand (Holz, Gestein, Agrar) gegen spieloekonomie.achsen.
  5  Schattenpreis von Hand gegen spieloekonomie.schattenpreis.
  6  Ertrag JE FELD gegen wirtschaft.ertrag_gesamt und spieloekonomie.ort_tick.
  7  Siedlerzuwachs und Siedlergrenze im Takt.
  8  Ein Ort ohne Kennung faellt nicht aus dem Takt.
  9  Kartenpruefung (Siegfilter) 10x10 gegen eigene Handrechnung.
 10  Ausdrueckliche Befunde (siehe unten).

BEFUNDE (werden im Lauf als BEFUND gemeldet, nicht stillschweigend weggelassen)
  a) Block 2 des Vorgaengers ("Tabelle B woertlich aus dem Entwurfstext") hat
     KEINE 10x10-Entsprechung: der Entwurf
     archiv/analysen/audits/entwurf_spieloekonomie_sol_2026-10-05.txt beschreibt
     ausschliesslich 8x7-Karten (56 Felder, 7 Gelaendespalten, 10 erfundene
     Kontingente). Originalkarten werden niemals gemischt, es gibt keine
     Gewichte mehr. Ersatzpruefung: der 8x7-Weg ist nachweislich gesperrt.
  b) Der Mindestbesatz (wald>=2, berg>=2, grasland>=3, nebelsee>=1) aus
     data/gelaende.json ist eine VORSCHLAG-Regel der 8x7-Zeit. Bei einem Teil
     der 127 Originalkarten ist er nicht erfuellt; die Zahl wird gezaehlt und
     gemeldet, statt eine erfundene Karte zu verlangen.
  c) 10 Karten weichen in den GESCHRIEBENEN Quellzahlen von 100 Feldern ab
     (im Katalog unter "unter_vorbehalt": "originalangaben_abweichend_100"
     deklariert). Gerechnet wird mit dem Bildraster; die Abweichung ist
     Gegenstand einer eigenen Zusage.
  d) Die Portfolioregel des 8x7-Siegfilters (portfoliofaktor 1.0,
     spezialistenfaktor 1.4) wird auf 10x10-Karten nicht mehr angewandt:
     spieloekonomie.kartenqualitaet meldet "original_10x10_versorgung" und
     entscheidet allein ueber die Zahl der Siedlungen (mindestens 4). Geprueft
     wird die neue Zusage plus die Handrechnung der Achsen.

Aufruf:  python -X utf8 tests/test_oekonomie_kern_10x10_nachfolger.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()

DATA = os.path.join(ROOT, "data")
KATALOG_PFAD = os.path.join(DATA, "originalkarten", "katalog.json")
ENTWURF_PFAD = os.path.join(ROOT, "archiv", "analysen", "audits",
                            "entwurf_spieloekonomie_sol_2026-10-05.txt")


def _lade(pfad):
    with open(pfad, encoding="utf-8") as fh:
        return json.loads(fh.read())


KAT = _lade(KATALOG_PFAD)
GJ = _lade(os.path.join(DATA, "gelaende.json"))
GEB = {g["id"]: g for g in _lade(os.path.join(DATA, "buildings.json"))["gebaeude"]}
E = _lade(os.path.join(DATA, "spieloekonomie.json"))

ARTEN = [a["id"] for a in GJ["gelaendearten"]]
NAME = {a["id"]: a["name"] for a in GJ["gelaendearten"]}
BEBAUBAR = [a["id"] for a in GJ["gelaendearten"] if a["bebaubar"]]
GESPERRT = [a["id"] for a in GJ["gelaendearten"] if not a["bebaubar"]]
MINDEST = {k: v for k, v in GJ["regeln"]["mindestbesatz"].items()
           if not str(k).startswith("_")}

SPALTEN = int(KAT["mass"]["spalten"])
ZEILEN = int(KAT["mass"]["zeilen"])
MASS = SPALTEN * ZEILEN

KARTEN_ROH = KAT["karten"]
START_ID = "original-036"

# Module des Projekts (erst nach dem Suchpfad).
import spieloekonomie as O          # noqa: E402
import wirtschaft as W              # noqa: E402
import gebaeude_wirkung as GW       # noqa: E402

GRUNDEINKOMMEN_HOLZ = W.ORIGINAL_GRUNDEINKOMMEN.get("Holz", 0.0)
GRUNDEINKOMMEN_STEIN = W.ORIGINAL_GRUNDEINKOMMEN.get("Stein", 0.0)


# ==========================================================================
# Eigene Werkzeuge (kein Rueckgriff auf die Rechenwege des Kerns)
# ==========================================================================

def zahl(geb_id, art_id):
    """Ertrag eines Gebaeudes auf einer Gelaendeart direkt aus data/buildings.json."""
    tabelle = GEB[geb_id].get("ertrag_pro_stunde") or {}
    wert = tabelle.get(NAME[art_id])
    return wert if isinstance(wert, (int, float)) and not isinstance(wert, bool) else None


def hand_achsen(zaehlung):
    """Die drei Achsen allein aus Feldzaehlung und belegten Ertraegen (4/2)."""
    return (zaehlung["wald"] * zahl("holzfaeller", "wald")
            + zaehlung["steppe"] * zahl("holzfaeller", "steppe"),
            zaehlung["berg"] * zahl("steinmetz", "berg")
            + zaehlung["huegel"] * zahl("steinmetz", "huegel"),
            zaehlung["grasland"] * zahl("farm", "grasland")
            + zaehlung["steppe"] * zahl("farm", "steppe"))


def hand_relativ(zaehlung, basis):
    return tuple(x / b for x, b in zip(hand_achsen(zaehlung), basis))


def begrenzen(wert, grenzen):
    return min(grenzen[1], max(grenzen[0], wert))


def hand_schattenpreis(zaehlung, start_zaehlung, bestand, reserve):
    """Holz-Schattenpreis nach der Entwurfsformel: (bestes Gold / bestes Holz) * k * v."""
    bestes_gold = max(zahl("goldmine", "berg"), zahl("goldmine", "huegel"))
    bestes_holz = max(zahl("holzfaeller", "wald"), zahl("holzfaeller", "steppe"))
    grund = bestes_gold / bestes_holz
    lokal = hand_achsen(zaehlung)[0]
    start = hand_achsen(start_zaehlung)[0]
    k = begrenzen(start / lokal if lokal > 0 else float("inf"), E["kartenpreisgrenzen"])
    v = 1.0 if reserve <= 0 else begrenzen(2 * reserve / (reserve + bestand),
                                           E["vorratspreisgrenzen"])
    return grund * k * v


def zaehle(raster):
    return {art: raster.count(art) for art in ARTEN}


def ort(oid, karte, bauten, bevoelkerung=5.0, vorraete=None):
    """Ein Siedlungs-Ort mit allen Feldern, die ort_tick erwartet."""
    return {
        "id": oid,
        "besitzer": "spieler",
        "dimension": 0,
        "x": 0,
        "y": 0,
        "map_id": "karte1",
        "karte": karte,
        "bauten": dict(bauten),
        "stufen": {},
        "vorraete": dict(vorraete) if vorraete is not None else {},
        "waren": {},
        "einheiten": {},
        "bevoelkerung": bevoelkerung,
        "importiert": {},
        "verbrauchsjournal": [],
        "produktionsjournal": [],
        "fertigjournal": [],
        "werkstaetten": {},
        "ausbildung": [],
    }


# Bauplan je Gelaendeart (jedes bebaubare Feld genau ein Gebaeude, Handrechnung).
PLAN = {"wald": "holzfaeller", "steppe": "farm", "huegel": "steinmetz",
        "berg": "steinmetz", "grasland": "farm", "nebelsee": "tempel"}


# ==========================================================================
abschnitt("1. Rasterstand 10x10: Feldzahl 100 je Karte (Quelle: Originalkarten-Katalog)")

check("1a katalog.json nennt als Mass 10 Spalten und 10 Zeilen",
      SPALTEN == 10 and ZEILEN == 10, "%d x %d" % (SPALTEN, ZEILEN))
check("1b daraus folgen genau 100 Felder je Karte", MASS == 100, "%d Felder" % MASS)
check("1c der Katalog enthaelt 127 Karten (Kopfzahl der Datei)",
      len(KARTEN_ROH) == 127 and KAT["zaehlungen"]["gesamt_varianten"] == 127,
      "%d Karten, Kopfzahl %s" % (len(KARTEN_ROH), KAT["zaehlungen"]["gesamt_varianten"]))
check("1d die Gruppen der Kopfzahl ergeben zusammen 127 Karten",
      (KAT["zaehlungen"]["beste"] + KAT["zaehlungen"]["mittlere"]
       + KAT["zaehlungen"]["schlechte"]) == len(KARTEN_ROH),
      "%d + %d + %d" % (KAT["zaehlungen"]["beste"], KAT["zaehlungen"]["mittlere"],
                        KAT["zaehlungen"]["schlechte"]))

_ids = [k["id"] for k in KARTEN_ROH]
check("1e alle Kartenkennungen sind eindeutig", len(set(_ids)) == len(_ids),
      "%d Kennungen, %d verschieden" % (len(_ids), len(set(_ids))))

_falsches_mass = [k["id"] for k in KARTEN_ROH
                  if k.get("rastermass") != {"spalten": SPALTEN, "zeilen": ZEILEN}]
check("1f jede Karte traegt rastermass 10 x 10 -- 0 Abweichungen",
      not _falsches_mass, "Abweichungen: %s" % _falsches_mass[:5])

_falsche_feldzahl = [k["id"] for k in KARTEN_ROH if len(k.get("spielraster") or []) != MASS]
check("1g jedes spielraster hat genau 100 Felder -- 0 Abweichungen",
      not _falsche_feldzahl,
      "%d Karten mit falscher Feldzahl: %s" % (len(_falsche_feldzahl), _falsche_feldzahl[:5]))

_unbekannt = [k["id"] for k in KARTEN_ROH
              if any(f not in ARTEN for f in k.get("spielraster") or [])]
check("1h jedes Feld traegt eine der sieben bekannten Gelaendearten",
      not _unbekannt, "Karten mit unbekanntem Feld: %s" % _unbekannt[:5])

# Raster gegen die geschriebenen Quellzahlen der Karte.
_quellzahl_abweichend = []
_raster_gegen_quelle = []
for k in KARTEN_ROH:
    quelle = k["original_attribute"]["felder"]
    ist = zaehle(k["spielraster"])
    if sum(int(v) for v in quelle.values()) != MASS:
        _quellzahl_abweichend.append(k["id"])
    if {a: int(quelle.get(a, 0)) for a in ARTEN} != ist:
        _raster_gegen_quelle.append(k["id"])

check("1i die Quellzahlen von 117 Karten ergeben selbst 100 Felder",
      len(_quellzahl_abweichend) == 10,
      "%d Karten mit Quellsumme != 100: %s"
      % (len(_quellzahl_abweichend), _quellzahl_abweichend))
check("1j die Zahl der Quellabweichungen deckt sich mit der Deklaration des Katalogs",
      KAT["unter_vorbehalt"]["originalangaben_abweichend_100"] == len(_quellzahl_abweichend),
      "Katalog %s / gezaehlt %d" % (KAT["unter_vorbehalt"]["originalangaben_abweichend_100"],
                                    len(_quellzahl_abweichend)))

_ohne_warnung = [k["id"] for k in KARTEN_ROH
                 if k["id"] in _raster_gegen_quelle
                 and not (k.get("raster_nachweis") or {}).get("warnung")]
check("1k jede abweichende Karte traegt die Warnung im raster_nachweis",
      not _ohne_warnung, "ohne Warnung: %s" % _ohne_warnung)

check("1l genau sieben Gelaendearten, nur der Sumpf ist gesperrt",
      len(ARTEN) == 7 and set(BEBAUBAR) == set(ARTEN) - {"sumpf"} and GESPERRT == ["sumpf"],
      "bebaubar=%s gesperrt=%s" % (BEBAUBAR, GESPERRT))

# Die Spielkarte selbst: Felder, Bauplaetze, Zeilenraster.
_start_felder = zaehle(O.startkarte("nachfolger", "spieler")["raster"])
check("1m die Felder der Startkarte summieren sich zu 100",
      sum(_start_felder.values()) == MASS, str(sum(_start_felder.values())))


# ==========================================================================
abschnitt("2. Kartenvorrat und stillgelegter 8x7-Weg")

_check_start = O.startkarte("nachfolger", "spieler")
check("2a die Startkarte ist die feste Spielerkarte original-036",
      _check_start["originalkarte_id"] == START_ID, str(_check_start["originalkarte_id"]))
check("2b die Startkarte nennt 10 x 10 Felder und 100 Eintraege",
      _check_start["spalten"] == 10 and _check_start["zeilen"] == 10
      and len(_check_start["raster"]) == 100 and _check_start["felder"] == 100,
      "felder=%s raster=%d" % (_check_start["felder"], len(_check_start["raster"])))
check("2c die Bauplaetze sind 100 minus Sumpffelder",
      _check_start["bauplaetze"] == MASS - _check_start["zaehlung"]["sumpf"],
      "%s = 100 - %s" % (_check_start["bauplaetze"], _check_start["zaehlung"]["sumpf"]))
check("2d das Zeilenraster hat 10 Zeilen zu je 10 Feldern",
      len(_check_start["zeilen_raster"]) == 10
      and all(len(z) == 10 for z in _check_start["zeilen_raster"]),
      "%d Zeilen" % len(_check_start["zeilen_raster"]))

_v = O.vorrat("nachfolger")
check("2e der Kolonievorrat ist der Katalog ohne die Startkarte",
      len(_v) == len(KARTEN_ROH) - 1 and START_ID not in _v,
      "%d Karten, Startkarte enthalten: %s" % (len(_v), START_ID in _v))
check("2f jede Vorratskarte ist eine eigene, unbebaute 10x10-Karte",
      all(e["besitzer"] is None and len(e["karte"]["raster"]) == MASS for e in _v.values())
      and len({e["karte"]["originalkarte_id"] for e in _v.values()}) == len(_v),
      "%d Karten, %d Kennungen" % (len(_v),
                                   len({e["karte"]["originalkarte_id"] for e in _v.values()})))

_r_a = O.startkarte("saat-a", "spieler")["raster"]
_r_b = O.startkarte("saat-b", "spieler")["raster"]
check("2g die Startkarte ist saatenunabhaengig (Originalfelder werden nie gemischt)",
      _r_a == _r_b, "gleich: %s" % (_r_a == _r_b))
_v_raster_a = O.vorrat("saat-a")["original-001"]["karte"]["raster"]
_v_raster_b = O.vorrat("saat-b")["original-001"]["karte"]["raster"]
check("2h auch eine Vorratskarte ist bei zwei Saaten feldgleich",
      _v_raster_a == _v_raster_b, "gleich: %s" % (_v_raster_a == _v_raster_b))

check("2i data/gelaende.json fuehrt kein kartenmass und keinen 8x7-Kartenvorrat mehr",
      "kartenmass" not in GJ and "kartenvorrat" not in GJ,
      "Schluessel vorhanden: %s" % [k for k in ("kartenmass", "kartenvorrat") if k in GJ])


def _value_error(fn):
    try:
        fn()
    except ValueError as e:
        return True, str(e)
    except Exception as e:                                  # noqa: BLE001
        return False, "falsche Ausnahme %s: %s" % (type(e).__name__, e)
    return False, "keine Ausnahme"


_ok, _txt = _value_error(lambda: O.feste_karte("x", {}))
check("2j der alte 8x7-Generator ist stillgelegt (ValueError)", _ok, _txt)

import gelaende as GL                                        # noqa: E402

_ok, _txt = _value_error(lambda: GL.siedlungskarte_erzeugen("x", mass={"spalten": 8, "zeilen": 7}))
check("2k 8x7-Altparameter werden abgewiesen statt still generiert", _ok, _txt)


# ==========================================================================
abschnitt("3. Ertragswerte je Gelaende aus data/buildings.json (Vorgaengerblock B3)")

check("3a holzfaeller liefert auf Wald 4", zahl("holzfaeller", "wald") == 4,
      str(zahl("holzfaeller", "wald")))
check("3b holzfaeller liefert auf Steppe 2", zahl("holzfaeller", "steppe") == 2,
      str(zahl("holzfaeller", "steppe")))
check("3c steinmetz liefert auf Berg 4", zahl("steinmetz", "berg") == 4,
      str(zahl("steinmetz", "berg")))
check("3d steinmetz liefert auf Huegel 2", zahl("steinmetz", "huegel") == 2,
      str(zahl("steinmetz", "huegel")))
check("3e farm liefert auf Grasland 4", zahl("farm", "grasland") == 4,
      str(zahl("farm", "grasland")))
check("3f farm liefert auf Steppe 2", zahl("farm", "steppe") == 2,
      str(zahl("farm", "steppe")))
check("3g goldmine liefert auf Berg 3 (bester Goldertrag)",
      zahl("goldmine", "berg") == 3, str(zahl("goldmine", "berg")))
check("3h tempel liefert auf Nebelsee 5 (bester Manaertrag)",
      zahl("tempel", "nebelsee") == 5, str(zahl("tempel", "nebelsee")))

# Die Datei und der Kern muessen dasselbe sagen.
_gleich, _ungleich, _rueckfall = [], [], []
for art in ARTEN:
    for geb in ("holzfaeller", "steinmetz", "farm", "goldmine", "tempel"):
        mein = zahl(geb, art)
        kern = GL.ertrag_pro_stunde(geb, art)
        if isinstance(kern, dict):
            continue
        if mein is None:
            _rueckfall.append((geb, art, kern))
            continue
        (_gleich if mein == kern else _ungleich).append((geb, art, mein, kern))
check("3i fuer alle ausdruecklich genannten Felder stimmt meine Tabelle mit gelaende.ertrag_pro_stunde",
      not _ungleich, "%d Abweichungen: %s" % (len(_ungleich), _ungleich[:3]))

# Rueckfallschluessel ("alle Gelaende ausser Sumpf", Tempel 1 - Handbuch 2009, Entscheidung 31.10.2026) muss greifen.
_alle_keys = [k for k in (GEB["tempel"].get("ertrag_pro_stunde") or {}) if k.startswith("alle")]
check("3j die Stammdaten nennen fuer den Tempel einen Rueckfall fuer alle Gelaende ausser Sumpf",
      len(_alle_keys) == 1 and GEB["tempel"]["ertrag_pro_stunde"][_alle_keys[0]] == 1,
      str(_alle_keys))
_mit_rueckfall = [(g, a, k) for g, a, k in _rueckfall if k is not None]
_ohne_ertrag = [(g, a) for g, a, k in _rueckfall if k is None]
_hat_alle = {g for g, _a in _ohne_ertrag
             if any(kk.startswith("alle") for kk in (GEB[g].get("ertrag_pro_stunde") or {}))}
check("3k der Rueckfall greift nur ausserhalb des Sumpfs und liefert dort 1",
      bool(_mit_rueckfall) and all(a != "sumpf" and k == 1 for _g, a, k in _mit_rueckfall),
      str(_mit_rueckfall))
check("3l ohne Rueckfall gibt es keinen Ertrag: entweder Sumpf oder die Stammdaten nennen kein 'alle'-Feld",
      all(a == "sumpf" or g not in _hat_alle for g, a in _ohne_ertrag),
      "%s ; Gebaeude mit 'alle'-Feld: %s" % (_ohne_ertrag[:4], sorted(_hat_alle)))


# ==========================================================================
abschnitt("4. Achsen von Hand gegen spieloekonomie.achsen")

_sz = _check_start["zaehlung"]
_H, _S, _A = hand_achsen(_sz)
BASIS = (_H, _S, _A)

check("4a Handachse Holz = 4*Wald + 2*Steppe = %d" % _H, _H == 148, str(_H))
check("4b Handachse Gestein = 4*Berg + 2*Huegel = %d" % _S, _S == 76, str(_S))
check("4c Handachse Agrar = 4*Grasland + 2*Steppe = %d" % _A, _A == 80, str(_A))
check("4d Startachsentripel von Hand = (148, 76, 80)", (_H, _S, _A) == (148, 76, 80),
      str((_H, _S, _A)))
check("4e spieloekonomie.achsen(Start) == Handwert", tuple(O.achsen(_check_start)) == (_H, _S, _A),
      "%s vs %s" % (tuple(O.achsen(_check_start)), (_H, _S, _A)))
_rels = O.relativ(_check_start)
check("4f spieloekonomie.relativ(Start) == (1, 1, 1)",
      all(abs(x - 1.0) < 1e-9 for x in _rels), str(_rels))

# Zweite Karte: original-001 (Bergkreuz), Zaehlung 18/24/16/0/23/0/19.
_k1 = _v["original-001"]["karte"]
_k1z = _k1["zaehlung"]
check("4g Zaehlung von original-001 im Raster = (wald 0, berg 18, huegel 24, grasland 16, steppe 23)",
      (_k1z["wald"], _k1z["berg"], _k1z["huegel"], _k1z["grasland"], _k1z["steppe"])
      == (0, 18, 24, 16, 23),
      "%s" % {a: _k1z[a] for a in ("wald", "berg", "huegel", "grasland", "steppe")})
check("4h Handachsen original-001 = (46, 120, 110)", hand_achsen(_k1z) == (46, 120, 110),
      str(hand_achsen(_k1z)))
check("4i spieloekonomie.achsen(original-001) == Handwert",
      tuple(O.achsen(_k1)) == hand_achsen(_k1z),
      "%s vs %s" % (tuple(O.achsen(_k1)), hand_achsen(_k1z)))
_k1_rel = O.relativ(_k1)
check("4j spieloekonomie.relativ(original-001) == Handverhaeltnis zur Startkarte",
      all(abs(a - b) < 1e-12 for a, b in zip(_k1_rel, hand_relativ(_k1z, BASIS))),
      "%s vs %s" % (tuple(round(x, 4) for x in _k1_rel),
                    tuple(round(x, 4) for x in hand_relativ(_k1z, BASIS))))


# ==========================================================================
abschnitt("5. Schattenpreis von Hand gegen spieloekonomie.schattenpreis")

_gold = max(zahl("goldmine", "berg"), zahl("goldmine", "huegel"))
_holz = max(zahl("holzfaeller", "wald"), zahl("holzfaeller", "steppe"))
check("5a bester Goldertrag = 3 und bester Holzertrag = 4", (_gold, _holz) == (3, 4),
      "%s / %s" % (_gold, _holz))
check("5b Grundpreis Holz = 3 / 4 = 0.75", abs(_gold / _holz - 0.75) < 1e-12,
      "%.10f" % (_gold / _holz))

_faelle = [
    ("Startkarte, Bestand == Reserve (100/100)", _check_start, 100, 100,
     O.schattenpreis(_check_start, "holz", 100, 100), 0.75),
    ("Startkarte, leerer Bestand (0/100)", _check_start, 0, 100,
     O.schattenpreis(_check_start, "holz", 0, 100), 1.5),
    ("original-001, 100/100 (Kartenfaktor 148/46)", _k1, 100, 100,
     O.schattenpreis(_k1, "holz", 100, 100), 0.75 * 148 / 46),
    ("original-001, 0/100 (Vorratsfaktor 2)", _k1, 0, 100,
     O.schattenpreis(_k1, "holz", 0, 100), 0.75 * 148 / 46 * 2.0),
    ("original-001, 100/300 (Vorratsfaktor 1.5)", _k1, 100, 300,
     O.schattenpreis(_k1, "holz", 100, 300), 0.75 * 148 / 46 * 1.5),
]
for _name, _karte, _best, _res, _ist, _soll in _faelle:
    _hand = hand_schattenpreis(_karte["zaehlung"], _sz, _best, _res)
    check("5c %s: Handwert = Kernwert (%.6f)" % (_name, _hand),
          abs(_hand - _ist) < 1e-9 and abs(_hand - _soll) < 1e-9,
          "Hand %.6f / Kern %.6f / Soll %.6f" % (_hand, _ist, _soll))

check("5d Gold hat immer den Preis 1", abs(O.schattenpreis(_check_start, "gold", 5, 5) - 1.0) < 1e-12,
      str(O.schattenpreis(_check_start, "gold", 5, 5)))


# ==========================================================================
abschnitt("6. Ertrag JE FELD gegen wirtschaft.ertrag_gesamt und ort_tick")

_raster = _check_start["raster"]
_bauten = {str(i): PLAN[art] for i, art in enumerate(_raster) if art in PLAN}
check("6a der Bauplan belegt jedes bebaubare Feld genau einmal",
      len(_bauten) == MASS - _sz["sumpf"], "%d von %d Feldern" % (len(_bauten), MASS))

_o = ort("S1", _check_start, _bauten)

# Handsumme: Ertrag jedes Feldes aus der eigenen Tabelle, plus belegtes Grundeinkommen.
_soll_felder = {}
for _feld, _geb in _bauten.items():
    _art = _raster[int(_feld)]
    _menge = zahl(_geb, _art)
    _roh = (GEB[_geb].get("rohstoff") or "").lower()
    _soll_felder[_roh] = _soll_felder.get(_roh, 0) + _menge
_soll_felder["holz"] = _soll_felder.get("holz", 0) + GRUNDEINKOMMEN_HOLZ
_soll_felder["stein"] = _soll_felder.get("stein", 0) + GRUNDEINKOMMEN_STEIN

check("6b Handsumme der 86 Felder = Holz 112, Stein 76, Nahrung 80, Mana 20 (ohne Grundeinkommen; Tempel seit 31.10.2026 = 5/1)",
      (_soll_felder["holz"] - GRUNDEINKOMMEN_HOLZ, _soll_felder["stein"] - GRUNDEINKOMMEN_STEIN,
       _soll_felder["nahrung"], _soll_felder["mana"]) == (112, 76, 80, 20),
      "Holz %s, Stein %s, Nahrung %s, Mana %s"
      % (_soll_felder["holz"] - GRUNDEINKOMMEN_HOLZ,
         _soll_felder["stein"] - GRUNDEINKOMMEN_STEIN,
         _soll_felder["nahrung"], _soll_felder["mana"]))
check("6c das belegte Grundeinkommen der Originalsiedlung ist +1 Holz und +1 Stein je Stunde",
      (GRUNDEINKOMMEN_HOLZ, GRUNDEINKOMMEN_STEIN) == (1.0, 1.0),
      "%s / %s" % (GRUNDEINKOMMEN_HOLZ, GRUNDEINKOMMEN_STEIN))

_w_ertrag = {k.lower(): v for k, v in W.ertrag_gesamt([_o]).items()}
check("6d wirtschaft.ertrag_gesamt == Handsumme (Holz 113, Stein 77, Nahrung 80, Mana 20)",
      _w_ertrag == {"holz": 113.0, "stein": 77.0, "nahrung": 80.0, "mana": 20.0},
      str(_w_ertrag))

_t1 = O.ort_tick(_o, 0, 3600, {})
check("6e nach einer Stunde Spielzeit stehen genau die Stundenertraege im Vorrat",
      all(abs(_t1["vorraete"].get(r, 0) - _w_ertrag[r]) < 1e-9 for r in _w_ertrag)
      and len(_t1["vorraete"]) == len(_w_ertrag),
      str({k: round(v, 4) for k, v in _t1["vorraete"].items()}))

_t2 = O.ort_tick(_o, 0, 7200, {})
check("6f zwei Stunden ergeben genau das Doppelte je Rohstoff",
      all(abs(_t2["vorraete"].get(r, 0) - 2 * _w_ertrag[r]) < 1e-9 for r in _w_ertrag),
      str({k: round(v, 4) for k, v in _t2["vorraete"].items()}))

_t_halb = O.ort_tick(_o, 0, 1800, {})
check("6g eine halbe Stunde ergibt die halbe Menge (linear in der Dauer)",
      all(abs(_t_halb["vorraete"].get(r, 0) - _w_ertrag[r] / 2) < 1e-9 for r in _w_ertrag),
      str({k: round(v, 4) for k, v in _t_halb["vorraete"].items()}))

check("6h kein Feld wird stillschweigend uebersprungen",
      W.uebersprungen_von(W.siedlung_ertrag(_o)) == [],
      str(W.uebersprungen_von(W.siedlung_ertrag(_o))[:3]))

# Einzelfelder: nur ein Feld belegt, der Rest der 100 Felder leer.
for _art_id, _geb_id, _roh in (("wald", "holzfaeller", "holz"), ("berg", "steinmetz", "stein"),
                               ("nebelsee", "tempel", "mana"), ("grasland", "farm", "nahrung")):
    _idx = _raster.index(_art_id)
    _eo = ort("E", _check_start, {str(_idx): _geb_id})
    _et = O.ort_tick(_eo, 0, 3600, {})
    _soll = zahl(_geb_id, _art_id)
    if _roh in ("holz", "stein"):
        _soll += GRUNDEINKOMMEN_HOLZ if _roh == "holz" else GRUNDEINKOMMEN_STEIN
    check("6i Feld %d (%s) mit %s liefert %.1f %s je Stunde"
          % (_idx, NAME[_art_id], _geb_id, _soll, _roh),
          abs(_et["vorraete"].get(_roh, 0) - _soll) < 1e-9,
          str({k: round(v, 4) for k, v in _et["vorraete"].items()}))

# Sumpf: nicht bebaubar, wird begruendet uebersprungen.
_sumpf_idx = _raster.index("sumpf")
_so = ort("SU", _check_start, {str(_sumpf_idx): "holzfaeller"})
_s_ertrag = W.siedlung_ertrag(_so)
_s_grund = W.uebersprungen_von(_s_ertrag)
_s_ressourcen = {k: v for k, v in _s_ertrag.items() if k != W.UEBERSPRUNGEN}
check("6j ein Gebaeude auf Sumpf traegt keinen Feldertrag bei",
      _s_ressourcen == {}, str(_s_ressourcen))
check("6j2 der Ort behaelt nur das belegte Grundeinkommen (Holz 1, Stein 1)",
      W.ertrag_gesamt([_so]) == {"Holz": GRUNDEINKOMMEN_HOLZ, "Stein": GRUNDEINKOMMEN_STEIN},
      str(W.ertrag_gesamt([_so])))
check("6k der Sumpf wird mit Begruendung uebersprungen, nicht verschluckt",
      len(_s_grund) == 1 and "Sumpf" in _s_grund[0], str(_s_grund))

check("6l der Produktionsjournal haelt die Spanne 0..3600 mit den Feldmengen fest",
      len(_t1["produktionsjournal"]) == 1
      and _t1["produktionsjournal"][0]["ab"] == 0
      and _t1["produktionsjournal"][0]["bis"] == 3600
      and all(abs(_t1["produktionsjournal"][0]["mengen"].get(r, 0) - v) < 1e-9
              for r, v in _w_ertrag.items()),
      str(_t1["produktionsjournal"][0]["mengen"]))


# ==========================================================================
abschnitt("7. Siedlerzuwachs und Siedlergrenze im Takt")

check("7a die Regel sagt 1 Siedler je Siedlung und Stunde",
      abs(GW.siedler_zuwachs_pro_stunde([_o]) - 1.0) < 1e-9,
      str(GW.siedler_zuwachs_pro_stunde([_o])))
check("7b ohne Haus liegt die Grenze bei 10 Siedlern",
      GW.bevoelkerungsgrenze([_o]) == 10, str(GW.bevoelkerungsgrenze([_o])))
check("7c nach einer Stunde waechst die Bevoelkerung von 5.0 auf 6.0",
      abs(_t1["bevoelkerung"] - 6.0) < 1e-9, str(_t1["bevoelkerung"]))
check("7d eine halbe Stunde ergibt 5.5 Siedler (linear)",
      abs(_t_halb["bevoelkerung"] - 5.5) < 1e-9, str(_t_halb["bevoelkerung"]))
check("7e Heilkunde Stufe 1 hebt den Zuwachs auf 1.1 je Stunde",
      abs(O.ort_tick(_o, 0, 3600, {"heilkunde": 1})["bevoelkerung"] - 6.1) < 1e-9,
      str(O.ort_tick(_o, 0, 3600, {"heilkunde": 1})["bevoelkerung"]))

_lang = O.ort_tick(_o, 0, 20 * 3600, {})
check("7f nach 20 Stunden steht die Bevoelkerung exakt auf der Grenze 10",
      _lang["bevoelkerung"] == GW.bevoelkerungsgrenze([_lang]) == 10,
      "Ist %s, Grenze %s" % (_lang["bevoelkerung"], GW.bevoelkerungsgrenze([_lang])))
_noch = O.ort_tick(_lang, 20 * 3600, 200 * 3600, {})
check("7g eine weitere lange Spanne hebt sie nicht ueber die Grenze",
      _noch["bevoelkerung"] == 10, str(_noch["bevoelkerung"]))
check("7h die Bevoelkerung ist ueberhaupt gewachsen (Start 5.0)",
      _lang["bevoelkerung"] > 5.0, str(_lang["bevoelkerung"]))

_haus_felder = [i for i, a in enumerate(_raster) if a == "wald"][:2]
_haus_bauten = {str(i): "haus" for i in _haus_felder}
_oh = ort("H", _check_start, _haus_bauten)
check("7i zwei Haeuser heben die Grenze von 10 auf 20 (+5 je Haus)",
      GW.bevoelkerungsgrenze([_oh]) == 20, str(GW.bevoelkerungsgrenze([_oh])))
check("7j mit zwei Haeusern waechst die Siedlung bis 20 und nicht weiter",
      O.ort_tick(_oh, 0, 40 * 3600, {})["bevoelkerung"] == 20,
      str(O.ort_tick(_oh, 0, 40 * 3600, {})["bevoelkerung"]))


# ==========================================================================
abschnitt("8. Ein Ort ohne Kennung faellt nicht aus dem Takt")

_ohne_id = dict(_o)
_ohne_id.pop("id")
_t_ohne_id = O.ort_tick(_ohne_id, 0, 3600, {})
check("8a ein Ort ohne Feld 'id' wird ohne Ausnahme fortgeschrieben",
      isinstance(_t_ohne_id, dict) and _t_ohne_id["produktionsjournal"] == _t1["produktionsjournal"],
      "Journalzeilen %d" % len(_t_ohne_id["produktionsjournal"]))
check("8b Vorrat und Bevoelkerung sind ohne 'id' Feld fuer Feld gleich",
      _t_ohne_id["vorraete"] == _t1["vorraete"]
      and _t_ohne_id["bevoelkerung"] == _t1["bevoelkerung"],
      "%s / %s" % ({k: round(v, 4) for k, v in _t_ohne_id["vorraete"].items()},
                   _t_ohne_id["bevoelkerung"]))
check("8c die Bauten bleiben ohne 'id' vollstaendig erhalten",
      _t_ohne_id["bauten"] == _t1["bauten"] and len(_t_ohne_id["bauten"]) == len(_bauten),
      "%d Bauten" % len(_t_ohne_id["bauten"]))

# Karte OHNE Kennung (kein originalkarte_id): der Takt laeuft weiter, nur das
# belegte Grundeinkommen der Originalsiedlung entfaellt.
_karte_ohne_kennung = {"raster": list(_raster)}
_okK = ort("K", _karte_ohne_kennung, _bauten)
_tK = O.ort_tick(_okK, 0, 3600, {})
_wK = {k.lower(): v for k, v in W.ertrag_gesamt([_okK]).items()}
check("8d ein Ort ohne Kartenkennung wird ohne Ausnahme fortgeschrieben",
      isinstance(_tK, dict) and len(_tK["produktionsjournal"]) == 1,
      "Journalzeilen %d" % len(_tK["produktionsjournal"]))
check("8e ohne Kartenkennung fehlt NUR das Grundeinkommen (Holz 112, Stein 76)",
      _wK == {"holz": 112.0, "stein": 76.0, "nahrung": 80.0, "mana": 20.0},
      str(_wK))
check("8f die Feldertraege selbst bleiben unveraendert (Nahrung und Mana gleich)",
      _wK["nahrung"] == _w_ertrag["nahrung"] and _wK["mana"] == _w_ertrag["mana"],
      "Nahrung %s / Mana %s" % (_wK["nahrung"], _wK["mana"]))
check("8g der Takt laeuft weiter: gleiche Journalmenge wie mit Kennung ausser Holz und Stein",
      abs(_tK["produktionsjournal"][0]["mengen"].get("nahrung", 0)
          - _t1["produktionsjournal"][0]["mengen"].get("nahrung", 0)) < 1e-9,
      str(_tK["produktionsjournal"][0]["mengen"]))


# ==========================================================================
abschnitt("9. Kartenpruefung (Siegfilter) 10x10 gegen eigene Handrechnung")

_q3_karten = [_check_start, _v["original-001"]["karte"], _v["original-002"]["karte"]]
_q3 = O.kartenqualitaet(_q3_karten)
_q4_karten = _q3_karten + [_v["original-003"]["karte"]]
_q4 = O.kartenqualitaet(_q4_karten)

check("9a die Regeldaten nennen mindestens 4 Siedlungen als Grundbedingung",
      E["mindestsiedlungen"] == 4, str(E["mindestsiedlungen"]))
check("9b drei 10x10-Karten erfuellen die Kartenpruefung NICHT",
      _q3["erfuellt"] is False and _q3["siedlungen"] == 3,
      "erfuellt=%s siedlungen=%s" % (_q3["erfuellt"], _q3["siedlungen"]))
check("9c vier 10x10-Karten erfuellen die Kartenpruefung",
      _q4["erfuellt"] is True and _q4["siedlungen"] == 4,
      "erfuellt=%s siedlungen=%s" % (_q4["erfuellt"], _q4["siedlungen"]))
check("9d das Modell ist ausdruecklich der 10x10-Versorgungsweg, nicht das 8x7-Portfolio",
      _q4["modell"] == "original_10x10_versorgung" == _q3["modell"], str(_q4["modell"]))

_gewichte = [k["zaehlung"] for k in _q4_karten]
_hand_mittel = tuple(sum(w[i] for w in [hand_relativ(z, BASIS) for z in _gewichte]) / len(_gewichte)
                     for i in range(3))
_hand_beste = tuple(max(w[i] for w in [hand_relativ(z, BASIS) for z in _gewichte])
                    for i in range(3))
check("9e Handrechnung des Achsenmittels deckt sich mit kartenqualitaet",
      all(abs(a - b) < 5e-12 for a, b in zip(_hand_mittel, _q4["mittel"])),
      "%s vs %s" % (tuple(round(x, 4) for x in _hand_mittel),
                    tuple(round(x, 4) for x in _q4["mittel"])))
check("9f Handrechnung des Bestwerts deckt sich mit kartenqualitaet",
      all(abs(a - b) < 5e-12 for a, b in zip(_hand_beste, _q4["beste"])),
      "%s vs %s" % (tuple(round(x, 4) for x in _hand_beste),
                    tuple(round(x, 4) for x in _q4["beste"])))
check("9g eine einzelne Karte erfuellt die Pruefung nie",
      O.kartenqualitaet([_check_start])["erfuellt"] is False,
      str(O.kartenqualitaet([_check_start])["siedlungen"]))
check("9h 126 Vorratskarten erfuellen die Pruefung ebenfalls",
      O.kartenqualitaet([e["karte"] for e in _v.values()])["erfuellt"] is True,
      str(O.kartenqualitaet([e["karte"] for e in _v.values()])["siedlungen"]))


# ==========================================================================
abschnitt("10. Befunde (ausdruecklich, kein Fehler)")

# b) Mindestbesatz der 8x7-Zeit.
check("10a die Mindestbesatz-Regel steht weiterhin in data/gelaende.json",
      MINDEST == {"wald": 2, "berg": 2, "grasland": 3, "nebelsee": 1}, str(MINDEST))
_verletzt = [k["id"] for k in KARTEN_ROH
             if not all(zaehle(k["spielraster"]).get(a, 0) >= m for a, m in MINDEST.items())]
befund("Mindestbesatz (VORSCHLAG aus der 8x7-Zeit) ist bei %d von %d Originalkarten "
       "nicht erfuellt" % (len(_verletzt), len(KARTEN_ROH)),
       "Beispiele: %s - die Regel wird fuer Originalkarten nicht angewandt, sonst muesste man "
       "Karten erfinden" % _verletzt[:4])

# a) Entwurfstext-Tabelle.
_hat_entwurf = os.path.exists(ENTWURF_PFAD)
check("10b der Entwurfstext liegt weiterhin im Archiv", _hat_entwurf, ENTWURF_PFAD)
if _hat_entwurf:
    with open(ENTWURF_PFAD, encoding="utf-8") as fh:
        _text = fh.read()
    befund("Vorgaengerblock 2 (Gewichtetabelle aus dem Entwurfstext) hat keine "
           "10x10-Entsprechung",
           "Text %d Zeichen, nennt 'Gewichtetabelle' %d mal, '8x7' %d mal, '10x10' %d mal - "
           "die Tabelle beschreibt 56-Felder-Karten mit erfundenen Kontingenten; "
           "Originalkarten werden nie gemischt"
           % (len(_text), _text.count("Gewichtetabelle"), _text.count("8x7"),
              _text.count("10x10")))

# c) Quellzahl-Abweichungen.
befund("%d Karten weichen in den geschriebenen Quellzahlen von 100 Feldern ab "
       "(im Katalog deklariert)" % len(_quellzahl_abweichend),
       "%s - gerechnet wird mit dem Bildraster, nicht mit der Schriftzahl"
       % _quellzahl_abweichend)

# d) 8x7-Siegfilter.
befund("die 8x7-Portfolioregel (portfoliofaktor %.2f, spezialistenfaktor %.2f) wird "
       "auf 10x10-Karten nicht mehr angewandt"
       % (E["portfoliofaktor"], E["spezialistenfaktor"]),
       "kartenqualitaet prueft bei Originalkarten nur noch die Zahl der Siedlungen "
       "(>= %s); Leistung und Spezialisierung belegt erst zielstatus"
       % E["mindestsiedlungen"])


sys.exit(bericht())
