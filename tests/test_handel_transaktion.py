# -*- coding: ascii -*-
"""Pruefung des bestaetigten FREMDHANDELS (Oekonomie-Paket, Schritt 8b).

Quelle: `archiv/analysen/audits/entwurf_spieloekonomie_sol_2026-10-05.txt`, Z. 752 und Z. 878-940:

    'Externer Handel vorlaeufig als bestaetigte Einzelangebote mit echter Handelskarawane aus U;
     keine Netzfunktionen. Preis fest bei Angebot, Mengen/Gegenleistung vor Start sperren,
     Abschluss nach Reise, Rueckgabe bei Ablehnung. Es fehlen im vorhandenen Auftragskern
     Gegenlagertransaktion und bestaetigte Angebotsannahme; diese muessen als separates
     handel_start/handel_abschluss-Paar nach dem Muster transport_start entstehen.
     Nicht _trade aufrufen und Gratisgewinne nur anders beschriften.'

Gegenstand sind ausschliesslich `spieloekonomie.handel_start` und
`spieloekonomie.handel_abschluss`. Geprueft werden acht Zusagen:

  P0  Handelskarawane und Ladung sind belegt (data/units.json), beide Funktionen sind da.
  P1  Rohstoffangebot: Gold UND Ware sind ab dem Start gesperrt (beide Lager sinken),
      der Preis steht fest, die Karawane ist abgezogen - nichts wird verschenkt.
  P2  Warenangebot ueber den getrennten Kanal 'waren' (Vorraete bleiben unberuehrt).
  P3  Annahme: Gold wandert bei der Ankunft zum Verkaeufer, die Ware kommt bei der
      Rueckkehr beim Kaeufer an, die Karawane kehrt heim - GENAU EINMAL.
  P4  Ablehnung (belegte Regel, Handbuch S. 20): Gold und Ware kommen vollstaendig
      zurueck, die Karawane ebenso - 'Gold wird nie uebertragen'.
  P5  Zielverlust: verlorener Kaeuferort -> Gut bleibt am Vertrag (keine Geistergutschrift);
      verlorener Verkaeuferort -> Gold zurueck, verlorenes Verkaeufergut nur vermerkt.
  P6  Rueckladung und alle uebrigen Ablehnungen - es wird nichts halb gebucht.
  P7  Der Sieg-Handelsnachweis bleibt den eigenen Transporten vorbehalten: ein Fremdkauf
      erzeugt KEINEN Importeintrag; die Importherkunft reist anteilig mit (Sperrlogik).
  P8  `auftraege.spieldaten_anwenden` laesst einen Fremdvertrag unberuehrt.

Nur gelesen, nichts geaendert. Aufruf:
    python -X utf8 tests/test_handel_transaktion.py
"""
from __future__ import annotations

import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

ROOT, SRC = import_src()
import einheiten as E  # noqa: E402
import auftraege as A  # noqa: E402
import spieloekonomie as O  # noqa: E402

KARAWANE = "Handelskarawane"
MASSE = 1e-9


def ort(oid, besitzer, x=0, y=0, dimension="welt", vorraete=None, waren=None,
        einheiten=None, importiert=None):
    """Eine Siedlung als dict mit allen Feldern, die der Handel beruehrt."""
    return {
        "id": oid,
        "besitzer": besitzer,
        "dimension": dimension,
        "x": x,
        "y": y,
        "vorraete": dict(vorraete or {}),
        "waren": dict(waren or {}),
        "einheiten": dict(einheiten or {}),
        "importiert": dict(importiert or {}),
        "verbrauchsjournal": [],
    }


def wirft(fn):
    """(Name der Ausnahme, Text) oder ('', '') wenn nichts geworfen wurde."""
    try:
        fn()
    except Exception as e:  # noqa: BLE001
        return type(e).__name__, str(e)
    return "", ""


def nah(a, b):
    return abs(float(a) - float(b)) < MASSE


# --------------------------------------------------------------------------
abschnitt("P0: Vorbereitung - Handelskarawane, Ladung, beide Funktionen")

check("P0: 'Handelskarawane' ist eine bekannte Einheit", KARAWANE in E.alle())
check("P0: die Ladung einer Handelskarawane ist belegt (1000)",
      A.ladung_der_mission({KARAWANE: 1}) == 1000,
      str(A.ladung_der_mission({KARAWANE: 1})))
check("P0: spieloekonomie.handel_start ist vorhanden", callable(getattr(O, "handel_start", None)))
check("P0: spieloekonomie.handel_abschluss ist vorhanden",
      callable(getattr(O, "handel_abschluss", None)))
check("P0: spieloekonomie.handel_entscheiden ist vorhanden",
      callable(getattr(O, "handel_entscheiden", None)))


# --------------------------------------------------------------------------
abschnitt("P1: Rohstoffangebot - Gold UND Ware sind ab dem Start gesperrt")

K1 = ort("K1", "kaeufer", x=0, y=0, vorraete={"gold": 1000.0},
         einheiten={KARAWANE: 1})
V1 = ort("V1", "verkaeufer", x=4, y=0, vorraete={"holz": 500.0})
_k1, _v1, _m1 = O.handel_start(K1, V1, {KARAWANE: 1}, "holz", 100, 5.0, "vorraete", 0.0)

check("P1: der Vertrag ist ein Fremdvertrag", _m1.get("fremdvertrag") is True)
check("P1: der Vertrag ist die Auftragsart 'handeln'", _m1.get("art") == "handeln",
      str(_m1.get("art")))
check("P1: der Preis steht FEST im Vertrag (5.0)", _m1.get("preis") == 5.0,
      str(_m1.get("preis")))
check("P1: die Menge steht fest im Vertrag (100)", _m1.get("menge") == 100,
      str(_m1.get("menge")))
check("P1: der Kanal ist 'vorraete'", _m1.get("kanal") == "vorraete", str(_m1.get("kanal")))
check("P1: der Sperrbetrag ist Menge x Preis = 500", nah(_m1.get("sperrgold", 0), 500.0),
      str(_m1.get("sperrgold")))
check("P1: Kaeufer und Verkaeufer stehen mit ihren Besitzern im Vertrag",
      _m1.get("kaeufer") == "K1" and _m1.get("verkaeufer") == "V1"
      and _m1.get("kaeufer_owner") == "kaeufer"
      and _m1.get("verkaeufer_owner") == "verkaeufer",
      "%s/%s" % (_m1.get("kaeufer"), _m1.get("verkaeufer")))
check("P1: noch nicht angenommen, noch nicht abgerechnet",
      _m1.get("angenommen") is False and _m1.get("abgerechnet") is False)
check("P1: das Gold des Kaeufers ist gesperrt (1000 -> 500)",
      nah(_k1["vorraete"]["gold"], 500.0), str(_k1["vorraete"]["gold"]))
check("P1: die Ware des Verkaeufers ist gesperrt (500 -> 400)",
      nah(_v1["vorraete"]["holz"], 400.0), str(_v1["vorraete"]["holz"]))
check("P1: die Karawane ist vom Kaeufer abgezogen",
      _k1["einheiten"].get(KARAWANE, 0) == 0, str(_k1["einheiten"]))
check("P1: die uebergebenen Orte bleiben unveraendert (tiefe Kopie)",
      nah(K1["vorraete"]["gold"], 1000.0) and nah(V1["vorraete"]["holz"], 500.0),
      "%s / %s" % (K1["vorraete"]["gold"], V1["vorraete"]["holz"]))
check("P1: die Ankunft liegt nach dem Start", _m1["ankunft"] > 0.0, str(_m1["ankunft"]))
check("P1: die Rueckkehr liegt nach der Ankunft",
      _m1["rueckkehr"] > _m1["ankunft"], str(_m1["rueckkehr"]))
# Keine Gratisgewinne: das Gold ist nicht verschwunden, es liegt am Vertrag.
check("P1: Gold-Erhaltung - Lager des Kaeufers + Sperrbetrag = vorher",
      nah(_k1["vorraete"]["gold"] + _m1["sperrgold"], 1000.0),
      str(_k1["vorraete"]["gold"] + _m1["sperrgold"]))


# --------------------------------------------------------------------------
abschnitt("P2: Warenangebot ueber den getrennten Kanal 'waren'")

K2 = ort("K2", "kaeufer", x=0, y=0, vorraete={"gold": 100.0},
         einheiten={KARAWANE: 1})
V2 = ort("V2", "verkaeufer", x=2, y=0, vorraete={"holz": 77.0}, waren={"Wollumhang": 10})
_k2, _v2, _m2 = O.handel_start(K2, V2, {KARAWANE: 1}, "Wollumhang", 4, 3.0, "waren", 0.0)

check("P2: der Kanal ist 'waren'", _m2.get("kanal") == "waren", str(_m2.get("kanal")))
check("P2: die Ware ist aus dem Warenlager abgezogen (10 -> 6)",
      _v2["waren"]["Wollumhang"] == 6, str(_v2["waren"]))
check("P2: das Rohstofflager des Verkaeufers bleibt unberuehrt",
      nah(_v2["vorraete"]["holz"], 77.0), str(_v2["vorraete"]))
check("P2: das Gold ist gesperrt (100 -> 88)",
      nah(_k2["vorraete"]["gold"], 88.0), str(_k2["vorraete"]["gold"]))

# Ankunft und Rueckkehr im Warenkanal: die Ware kommt beim Kaeufer an.
_o2a, _m2a = O.handel_abschluss(_m2, {"K2": _k2, "V2": _v2}, _m2["ankunft"])
check("P2: bei der Ankunft bekommt der Verkaeufer das Gold (88 + 12 = 100)",
      nah(_o2a["V2"]["vorraete"].get("gold", 0), 12.0),
      str(_o2a["V2"]["vorraete"].get("gold")))
_o2b, _m2b = O.handel_abschluss(_m2a, _o2a, _m2["rueckkehr"])
check("P2: bei der Rueckkehr liegen 4 Wollumhaenge beim Kaeufer",
      _o2b["K2"]["waren"].get("Wollumhang", 0) == 4, str(_o2b["K2"]["waren"]))
check("P2: die Ware liegt NICHT in den Vorraeten (getrennter Kanal)",
      "Wollumhang" not in _o2b["K2"]["vorraete"], str(_o2b["K2"]["vorraete"]))
check("P2: die Karawane ist heimgekehrt",
      _o2b["K2"]["einheiten"].get(KARAWANE, 0) == 1, str(_o2b["K2"]["einheiten"]))


# --------------------------------------------------------------------------
abschnitt("P3: Annahme - Gold bei der Ankunft, Ware bei der Rueckkehr, genau einmal")

_o3a, _m3a = O.handel_abschluss(_m1, {"K1": _k1, "V1": _v1}, _m1["ankunft"])
check("P3: die Ankunft nimmt das Angebot an", _m3a.get("angenommen") is True)
check("P3: der Verkaeufer hat das Gold (500)",
      nah(_o3a["V1"]["vorraete"].get("gold", 0), 500.0),
      str(_o3a["V1"]["vorraete"].get("gold")))
check("P3: der Sperrbetrag ist ausgeglichen (0)", nah(_m3a.get("sperrgold", 1), 0.0),
      str(_m3a.get("sperrgold")))
check("P3: die Ware liegt noch NICHT beim Kaeufer",
      nah(_o3a["K1"]["vorraete"].get("holz", 0), 0.0), str(_o3a["K1"]["vorraete"]))
check("P3: die Rueckkehr ist noch nicht abgerechnet", _m3a.get("abgerechnet") is False)

_o3b, _m3b = O.handel_abschluss(_m3a, _o3a, _m1["rueckkehr"])
check("P3: die Ware ist beim Kaeufer angekommen (100)",
      nah(_o3b["K1"]["vorraete"].get("holz", 0), 100.0), str(_o3b["K1"]["vorraete"]))
check("P3: der Vertrag ist abgerechnet", _m3b.get("abgerechnet") is True)
check("P3: die Karawane ist heimgekehrt",
      _o3b["K1"]["einheiten"].get(KARAWANE, 0) == 1, str(_o3b["K1"]["einheiten"]))

_o3c, _m3c = O.handel_abschluss(_m3b, _o3b, _m1["rueckkehr"] + 5000.0)
check("P3: kein doppelter Abschluss - die Ware waechst nicht weiter",
      nah(_o3c["K1"]["vorraete"].get("holz", 0), 100.0), str(_o3c["K1"]["vorraete"]))
check("P3: kein doppelter Abschluss - die Karawane wird nicht vermehrt",
      _o3c["K1"]["einheiten"].get(KARAWANE, 0) == 1, str(_o3c["K1"]["einheiten"]))
check("P3: kein doppelter Abschluss - das Gold des Verkaeufers bleibt 500",
      nah(_o3c["V1"]["vorraete"].get("gold", 0), 500.0),
      str(_o3c["V1"]["vorraete"].get("gold")))
check("P3: Gesamterhaltung - beide Goldlager zusammen sind 1000",
      nah(_o3c["K1"]["vorraete"]["gold"] + _o3c["V1"]["vorraete"]["gold"], 1000.0),
      str(_o3c["K1"]["vorraete"]["gold"] + _o3c["V1"]["vorraete"]["gold"]))
check("P3: der Kaeufer zahlt wirklich (500 Gold weg, 100 Holz her)",
      nah(_o3c["K1"]["vorraete"]["gold"], 500.0) and nah(_o3c["K1"]["vorraete"]["holz"], 100.0))


# --------------------------------------------------------------------------
abschnitt("P4: Ablehnung - Gold und Ware kommen vollstaendig zurueck")

K4 = ort("K4", "kaeufer", x=0, y=0, vorraete={"gold": 1000.0},
         importiert={"gold": 300.0}, einheiten={KARAWANE: 1})
V4 = ort("V4", "verkaeufer", x=3, y=0, vorraete={"holz": 500.0},
         importiert={"holz": 100.0})
_k4, _v4, _m4 = O.handel_start(K4, V4, {KARAWANE: 1}, "holz", 100, 5.0, "vorraete", 0.0)
check("P4: Sperranteil der Ware = 100/500 mal 100 = 20",
      nah(_m4["verkauft_import"]["holz"], 20.0), str(_m4.get("verkauft_import")))
check("P4: die Importherkunft der Ware ist mitgesperrt (100 -> 80)",
      nah(_v4["importiert"]["holz"], 80.0), str(_v4["importiert"]))
check("P4: die Importherkunft des Goldes ist mitgesperrt (300 -> 150)",
      nah(_k4["importiert"]["gold"], 150.0), str(_k4["importiert"]))
check("P4: die Entscheidung ist beim Start offen (None)", _m4.get("entscheidung") is None,
      str(_m4.get("entscheidung")))

# BELEGT (Handbuch S. 20): bei Ablehnung kehrt die Karawane MIT den Waren zurueck.
_m4_ab = O.handel_entscheiden(_m4, False)
check("P4: die Ablehnung steht im Vertrag", _m4_ab.get("entscheidung") is False)
check("P4: handel_entscheiden laesst den uebergebenen Vertrag unveraendert",
      _m4.get("entscheidung") is None)
check("P4: eine Entscheidung bucht nichts (Gold bleibt gesperrt)",
      nah(_k4["vorraete"]["gold"], 500.0), str(_k4["vorraete"]))

_o4a, _m4a = O.handel_abschluss(_m4_ab, {"K4": _k4, "V4": _v4}, _m4["ankunft"])
check("P4: bei Ablehnung kommt keine Annahme zustande", _m4a.get("angenommen") is False)
check("P4: das Gold bleibt gesperrt (500)", nah(_m4a.get("sperrgold", 0), 500.0),
      str(_m4a.get("sperrgold")))
check("P4: der Verkaeufer bekommt kein Gold (abgelehnt heisst: Gold wird nie uebertragen)",
      nah(_o4a["V4"]["vorraete"].get("gold", 0), 0.0),
      str(_o4a["V4"]["vorraete"].get("gold")))

_o4b, _m4b = O.handel_abschluss(_m4a, _o4a, _m4["rueckkehr"])
check("P4: abgerechnet", _m4b.get("abgerechnet") is True)
check("P4: das Gold ist zum Kaeufer zurueck (1000)",
      nah(_o4b["K4"]["vorraete"]["gold"], 1000.0), str(_o4b["K4"]["vorraete"]))
check("P4: die Importherkunft des Goldes ist vollstaendig zurueck (300)",
      nah(_o4b["K4"]["importiert"]["gold"], 300.0), str(_o4b["K4"]["importiert"]))
check("P4: die Ware ist NICHT beim Kaeufer",
      nah(_o4b["K4"]["vorraete"].get("holz", 0), 0.0), str(_o4b["K4"]["vorraete"]))
check("P4: die Ware ist vollstaendig zum Verkaeufer zurueck (400 + 100 = 500)",
      nah(_o4b["V4"]["vorraete"]["holz"], 500.0), str(_o4b["V4"]["vorraete"]))
check("P4: auch die Importherkunft der Ware ist zurueck (80 + 20 = 100)",
      nah(_o4b["V4"]["importiert"]["holz"], 100.0), str(_o4b["V4"]["importiert"]))
check("P4: die Karawane ist heimgekehrt",
      _o4b["K4"]["einheiten"].get(KARAWANE, 0) == 1, str(_o4b["K4"]["einheiten"]))
# Kein doppelter Abschluss: ein weiterer Aufruf bucht nichts mehr.
_o4c, _m4c = O.handel_abschluss(_m4b, _o4b, _m4["rueckkehr"] + 5000.0)
check("P4: kein doppelter Abschluss - Ware und Karawane bleiben, wo sie sind",
      nah(_o4c["V4"]["vorraete"]["holz"], 500.0)
      and _o4c["K4"]["einheiten"].get(KARAWANE, 0) == 1
      and nah(_o4c["K4"]["vorraete"]["gold"], 1000.0),
      str(_o4c["K4"]["vorraete"]))
_n, _msg = wirft(lambda: O.handel_entscheiden(_m4b, True))
check("P4: ein abgerechneter Vertrag laesst sich nicht mehr entscheiden",
      _n == "ValueError" and "abgerechnet" in _msg, "%s: %s" % (_n, _msg))


# --------------------------------------------------------------------------
abschnitt("P5: Zielverlust - verlorener Kaeufer- und Verkaeuferort")

# (5a) Verkaeuferort beim Eintreffen verloren, Kaeufer lebt -> Gold zurueck, Gut nur vermerkt.
K5 = ort("K5", "kaeufer", x=0, y=0, vorraete={"gold": 1000.0},
         einheiten={KARAWANE: 1})
V5 = ort("V5", "verkaeufer", x=5, y=0, vorraete={"holz": 500.0})
_k5, _v5, _m5 = O.handel_start(K5, V5, {KARAWANE: 1}, "holz", 100, 5.0, "vorraete", 0.0)
check("P5a: die Ware ist beim Verkaeufer gesperrt (500 -> 400)",
      nah(_v5["vorraete"]["holz"], 400.0), str(_v5["vorraete"]))
_v5_verloren = copy.deepcopy(_v5)
_v5_verloren["besitzer"] = "feind"
_o5a, _m5a = O.handel_abschluss(_m5, {"K5": _k5, "V5": _v5_verloren}, _m5["rueckkehr"])
check("P5a: das Gold ist zum Kaeufer zurueck",
      nah(_o5a["K5"]["vorraete"]["gold"], 1000.0), str(_o5a["K5"]["vorraete"]))
check("P5a: die Ware ist NICHT beim Kaeufer",
      nah(_o5a["K5"]["vorraete"].get("holz", 0), 0.0), str(_o5a["K5"]["vorraete"]))
check("P5a: das verlorene Verkaeufergut bleibt vermerkt, nicht verschenkt",
      _m5a.get("verlorenes_sperrgut") == {"holz": 100}, str(_m5a.get("verlorenes_sperrgut")))
check("P5a: der neue Besitzer des Verkaeuferorts bekommt die Ware NICHT",
      nah(_o5a["V5"]["vorraete"]["holz"], 400.0), str(_o5a["V5"]["vorraete"]))
check("P5a: abgerechnet", _m5a.get("abgerechnet") is True)

# (5b) Kaeuferort bei der Rueckkehr verloren -> Gut bleibt am Vertrag.
K6 = ort("K6", "kaeufer", x=0, y=0, vorraete={"gold": 1000.0},
         einheiten={KARAWANE: 1})
V6 = ort("V6", "verkaeufer", x=6, y=0, vorraete={"holz": 500.0})
_k6, _v6, _m6 = O.handel_start(K6, V6, {KARAWANE: 1}, "holz", 100, 5.0, "vorraete", 0.0)
_o6a, _m6a = O.handel_abschluss(_m6, {"K6": _k6, "V6": _v6}, _m6["ankunft"])
check("P5b: angenommen (der Verkaeufer hat sein Gold)",
      _m6a.get("angenommen") is True and nah(_o6a["V6"]["vorraete"]["gold"], 500.0),
      str(_o6a["V6"]["vorraete"].get("gold")))
_k6_verloren = copy.deepcopy(_o6a["K6"])
_k6_verloren["besitzer"] = "feind"
_o6b, _m6b = O.handel_abschluss(_m6a, {"K6": _k6_verloren, "V6": _o6a["V6"]},
                                _m6["rueckkehr"])
check("P5b: bei verlorenem Kaeuferort wird NICHT abgerechnet - das Gut bleibt am Vertrag",
      _m6b.get("abgerechnet") is False)
check("P5b: keine Geistergutschrift fuer den neuen Besitzer",
      nah(_o6b["K6"]["vorraete"].get("holz", 0), 0.0), str(_o6b["K6"]["vorraete"]))
check("P5b: die Karawane bleibt beim Vertrag (nicht beim neuen Besitzer)",
      _o6b["K6"]["einheiten"].get(KARAWANE, 0) == 0, str(_o6b["K6"]["einheiten"]))
check("P5b: auch die Vorraete des neuen Besitzers bleiben unberuehrt",
      nah(_o6b["K6"]["vorraete"]["gold"], 500.0), str(_o6b["K6"]["vorraete"]))


# --------------------------------------------------------------------------
abschnitt("P6: Rueckladung und die uebrigen Ablehnungen - nichts halb gebucht")

K7 = ort("K7", "kaeufer", x=0, y=0, vorraete={"gold": 100000.0},
         einheiten={KARAWANE: 1})
V7 = ort("V7", "verkaeufer", x=4, y=0, vorraete={"holz": 100000.0})

_name6a, _msg6a = wirft(lambda: O.handel_start(K7, V7, {KARAWANE: 1}, "holz", 1001, 1.0,
                                               "vorraete", 0.0))
check("P6a: mehr als die Rueckladung (1000) wird abgelehnt", _name6a == "ValueError",
      "%s: %s" % (_name6a, _msg6a))
check("P6a: die Meldung nennt die Kaufmenge", "Kaufmenge" in _msg6a, _msg6a)
_res6a, _err6a = wirft(lambda: O.handel_start(K7, V7, {KARAWANE: 1}, "holz", 1000, 1.0,
                                              "vorraete", 0.0))
check("P6a: genau die Rueckladung (1000) ist erlaubt", _res6a == "" and _err6a == "",
      _err6a)

K8 = ort("K8", "kaeufer", x=0, y=0, vorraete={"gold": 1000.0},
         einheiten={KARAWANE: 1})
V8 = ort("V8", "verkaeufer", x=4, y=0, vorraete={"holz": 100.0}, waren={"Wollumhang": 5})

_name8, _msg8 = wirft(lambda: O.handel_start(K8, V8, {KARAWANE: 1}, "holz", 10, 1.0,
                                             "goldbarren", 0.0))
check("P6b: ein unbekannter Frachtkanal wird abgelehnt",
      _name8 == "ValueError" and "Frachtkanal" in _msg8, "%s: %s" % (_name8, _msg8))

for _t in (0, -3, 3.5, True):
    _n, _m = wirft(lambda t=_t: O.handel_start(K8, V8, {KARAWANE: 1}, "holz", t, 1.0,
                                               "vorraete", 0.0))
    check("P6c: Handelsmenge %r wird abgelehnt" % (_t,),
          _n == "ValueError" and "Handelsmenge" in _m, "%s: %s" % (_n, _m))

for _p in (0, -1.0, float("inf"), True):
    _n, _m = wirft(lambda p=_p: O.handel_start(K8, V8, {KARAWANE: 1}, "holz", 10, p,
                                               "vorraete", 0.0))
    check("P6d: Preis %r wird abgelehnt" % (_p,),
          _n == "ValueError" and "Preis" in _m, "%s: %s" % (_n, _m))

_n, _m = wirft(lambda: O.handel_start(K8, V8, {KARAWANE: 1}, "gold", 10, 1.0, "vorraete", 0.0))
check("P6e: Gold ist kein Handelsgut", _n == "ValueError" and "Handelsgut" in _m,
      "%s: %s" % (_n, _m))

V8_eigen = copy.deepcopy(V8)
V8_eigen["besitzer"] = "kaeufer"
_n, _m = wirft(lambda: O.handel_start(K8, V8_eigen, {KARAWANE: 1}, "holz", 10, 1.0,
                                      "vorraete", 0.0))
check("P6f: ein eigener Ort braucht keinen Kaufvertrag",
      _n == "ValueError" and "Kaufvertrag" in _m, "%s: %s" % (_n, _m))

V8_dim = copy.deepcopy(V8)
V8_dim["dimension"] = "anderes"
_n, _m = wirft(lambda: O.handel_start(K8, V8_dim, {KARAWANE: 1}, "holz", 10, 1.0,
                                      "vorraete", 0.0))
check("P6g: eine fremde Dimension wird abgelehnt",
      _n == "ValueError" and "Dimension" in _m, "%s: %s" % (_n, _m))

K8_ohne = ort("K8", "kaeufer", x=0, y=0, vorraete={"gold": 1000.0}, einheiten={"Krieger": 3})
_n, _m = wirft(lambda: O.handel_start(K8_ohne, V8, {"Krieger": 1}, "holz", 10, 1.0,
                                      "vorraete", 0.0))
check("P6h: ohne Handelskarawane kein Fremdhandel (Auftragskern entscheidet)",
      _n == "ValueError" and "Handelskarawanen" in _m, "%s: %s" % (_n, _m))

_n, _m = wirft(lambda: O.handel_start(K8, V8, {KARAWANE: 2}, "holz", 10, 1.0, "vorraete", 0.0))
check("P6i: eine Karawane, die nicht vor Ort ist, wird abgelehnt",
      _n == "ValueError" and "Karawane" in _m, "%s: %s" % (_n, _m))

_n, _m = wirft(lambda: O.handel_start(K8, V8, {KARAWANE: 1}, "holz", 101, 1.0, "vorraete", 0.0))
check("P6j: eine nicht gedeckte Ware wird abgelehnt",
      _n == "ValueError" and "gedeckt" in _m, "%s: %s" % (_n, _m))

K8_arm = ort("K8", "kaeufer", x=0, y=0, vorraete={"gold": 5.0}, einheiten={KARAWANE: 1})
_n, _m = wirft(lambda: O.handel_start(K8_arm, V8, {KARAWANE: 1}, "holz", 10, 1.0,
                                      "vorraete", 0.0))
check("P6k: fehlendes Gold wird abgelehnt", _n == "ValueError" and "gedeckt" in _m,
      "%s: %s" % (_n, _m))

_n, _m = wirft(lambda: O.handel_start(K8, V8, {}, "holz", 10, 1.0, "vorraete", 0.0))
check("P6l: eine leere Karawanentruppe wird abgelehnt",
      _n == "ValueError" and "Karawanentruppe" in _m, "%s: %s" % (_n, _m))

check("P6m: nach allen Ablehnungen ist nichts gebucht (Gold unveraendert)",
      nah(K8["vorraete"]["gold"], 1000.0) and nah(V8["vorraete"]["holz"], 100.0)
      and V8["waren"]["Wollumhang"] == 5,
      "%s / %s / %s" % (K8["vorraete"]["gold"], V8["vorraete"]["holz"],
                        V8["waren"]["Wollumhang"]))


# --------------------------------------------------------------------------
abschnitt("P7: Fremdkauf ist kein eigener Handelsnachweis; Herkunft reist anteilig")

check("P7: die Ankunft beim Kaeufer erzeugt KEINEN Importeintrag fuer die Ware",
      _o3b["K1"]["importiert"].get("holz") is None, str(_o3b["K1"]["importiert"]))
check("P7: das Verbrauchsjournal des Kaeufers bleibt leer",
      _o3b["K1"]["verbrauchsjournal"] == [], str(_o3b["K1"]["verbrauchsjournal"]))

# Gegenprobe mit eigenen Zahlen: ein gekaufter Rohstoff erzeugt beim Verbrauch keinen Beleg.
K9 = ort("K9", "kaeufer", x=0, y=0, vorraete={"gold": 100.0},
         einheiten={KARAWANE: 1})
V9 = ort("V9", "verkaeufer", x=2, y=0, vorraete={"holz": 200.0})
_k9, _v9, _m9 = O.handel_start(K9, V9, {KARAWANE: 1}, "holz", 100, 1.0, "vorraete", 0.0)
_o9a, _m9a = O.handel_abschluss(_m9, {"K9": _k9, "V9": _v9}, _m9["ankunft"])
_o9b, _m9b = O.handel_abschluss(_m9a, _o9a, _m9["rueckkehr"])
check("P7: der gekaufte Rohstoff liegt im lokalen Lager (100)",
      nah(_o9b["K9"]["vorraete"].get("holz", 0), 100.0), str(_o9b["K9"]["vorraete"]))
_verbraucht = O.verbrauchen(_o9b["K9"], {"holz": 50.0}, 99.0)
check("P7: sein Verbrauch erzeugt KEINEN Handelsbeleg (kein Importeintrag)",
      _verbraucht["verbrauchsjournal"] == [], str(_verbraucht["verbrauchsjournal"]))
check("P7: der Bestand sinkt trotzdem (100 -> 50)",
      nah(_verbraucht["vorraete"]["holz"], 50.0), str(_verbraucht["vorraete"]))

# Die Importherkunft des Verkaeufers reist mit der Ware (Sperrlogik aus transport_start).
V10 = ort("V10", "verkaeufer", x=2, y=0, vorraete={"holz": 500.0},
          importiert={"holz": 100.0})
K10 = ort("K10", "kaeufer", x=0, y=0, vorraete={"gold": 100.0},
          einheiten={KARAWANE: 1})
_k10, _v10, _m10 = O.handel_start(K10, V10, {KARAWANE: 1}, "holz", 100, 1.0, "vorraete", 0.0)
_o10, _m10a = O.handel_abschluss(_m10, {"K10": _k10, "V10": _v10}, _m10["rueckkehr"])
check("P7: beim Verkauf sinkt die Importherkunft des Verkaeufers mit (100 -> 80)",
      nah(_o10["V10"]["importiert"]["holz"], 80.0), str(_o10["V10"]["importiert"]))


# --------------------------------------------------------------------------
abschnitt("P8: spieldaten_anwenden laesst einen Fremdvertrag unberuehrt")

_zustand = {"ressourcen": {"gold": 0.0, "holz": 0.0}, "einheiten": {}}
_vertrag = copy.deepcopy(_m1)
_nach = A.spieldaten_anwenden(_zustand, _vertrag)
check("P8: der Stand bleibt Zeichen fuer Zeichen gleich", _nach == _zustand,
      str(_nach))
check("P8: der Vertrag wird NICHT als angewendet markiert",
      not _vertrag.get("angewendet"))
check("P8: der Fremdvertrag traegt sein Merkmal fuer die Ereignisschleife",
      _vertrag.get("fremdvertrag") is True)


sys.exit(bericht())
