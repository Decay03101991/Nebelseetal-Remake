# -*- coding: ascii -*-
"""Pruefung des WARENKANALS des eigenen Transports (Entwurf Z. 504, woertlich):

    'Fuer Waren dieselbe Transportfunktion ueber einen getrennten Bestandskanal
     erweitern: frachtkanal="waren"; Kosten-/Importledger fuer Sieg bleibt nur bei
     Rohstoffen. Vor Aktivierung eigenen test_warentransport.py erstellen, sonst
     Warenhandel nicht anbieten.'

Gegenstand sind ausschliesslich `spieloekonomie.transport_start` und
`spieloekonomie.transport_fortschritt`. Geprueft werden neun Zusagen:

  P1  Eine Ware aus data/warenrezepte.json laesst sich mit frachtkanal='waren'
      verschicken: die Quelle verliert genau diese Ware, die Mission traegt
      frachtkanal 'waren'.
  P2  Bei Ankunft kommen die Waren GENAU EINMAL am Ziel an.
  P3  Der Sieg-Ledger bleibt sauber: kein Eintrag in ziel['importiert'].
  P4  Unbekannter Warenname aus dem Lager ist erlaubt, fehlende Ware nicht.
  P5  Karrenpflicht gilt auch im Warenkanal (Meldung nennt 'Karren').
  P6  Ueberladung gilt auch fuer Waren (Handkarren = 40).
  P7  Rueckkehr bei Zielverlust: Fracht bleibt an der Mission und kommt voll zurueck.
  P8  Der Rohstoffkanal bleibt unveraendert (ziel['importiert'] waechst weiter).
  P9  Ein unbekannter frachtkanal wird mit ValueError abgelehnt.

Nur gelesen, nichts geaendert. Aufruf:
    python -X utf8 tests/test_warentransport.py
"""
from __future__ import annotations

import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src, projektwurzel

ROOT, SRC = import_src()
import spieloekonomie as O  # noqa: E402

DATA = os.path.join(projektwurzel(), "data")

# --------------------------------------------------------------------------
# Hilfswerkzeuge
# --------------------------------------------------------------------------


def ort(oid, besitzer="spieler", x=0, y=0, dimension="welt", vorraete=None,
        waren=None, einheiten=None, importiert=None):
    """Eine Siedlung als dict mit allen Feldern, die der Transport beruehrt."""
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


def laeuft(fn):
    """(Ergebnis, '') bei Erfolg, sonst (None, 'Ausnahme: Text')."""
    try:
        return fn(), ""
    except Exception as e:  # noqa: BLE001
        return None, "%s: %s" % (type(e).__name__, e)


# --------------------------------------------------------------------------
abschnitt("P0: Vorbereitung - Ware aus data/warenrezepte.json")

with open(os.path.join(DATA, "warenrezepte.json"), encoding="utf-8") as fh:
    WERARREZEPTE = json.loads(fh.read())

WARE = "Wollumhang"
check("P0: data/warenrezepte.json ist ein nichtleeres Verzeichnis",
      isinstance(WERARREZEPTE, dict) and len(WERARREZEPTE) > 0,
      "%d Rezepte" % (len(WERARREZEPTE) if isinstance(WERARREZEPTE, dict) else -1))
check("P0: 'Wollumhang' steht in den Warenrezepten", WARE in WERARREZEPTE,
      str(sorted(WERARREZEPTE)[:5]))

# Ein Name, der weder Rohstoff noch Rezept ist: muss allein ueber das Warenlager zaehlen.
UNBEKANNT = "Zaubertrank"
check("P0: der Testwarenname ist kein Rezept (unbekannt)",
      UNBEKANNT not in WERARREZEPTE)


# --------------------------------------------------------------------------
abschnitt("P1: Ware verschicken - Quelle verliert genau die Ware")

_q1 = ort("A", x=0, y=0, waren={WARE: 10, UNBEKANNT: 3}, einheiten={"Handkarren": 1})
_z1 = ort("B", x=4, y=0, waren={WARE: 0})

neu_q1, m1 = O.transport_start(_q1, _z1, {"Handkarren": 1}, {WARE: 4}, 0.0,
                               frachtkanal="waren")

check("P1: Quelle verliert genau die verschickte Ware (10 -> 6)",
      neu_q1["waren"][WARE] == 6, str(neu_q1["waren"]))
check("P1: anderes Gut im Warenlager bleibt unberuehrt",
      neu_q1["waren"][UNBEKANNT] == 3, str(neu_q1["waren"]))
check("P1: Vorraete (Rohstofflager) bleiben unveraendert - getrennter Kanal",
      neu_q1["vorraete"] == _q1["vorraete"], str(neu_q1["vorraete"]))
check("P1: der uebergebene Ausgangsort wird nicht veraendert (tiefe Kopie)",
      _q1["waren"][WARE] == 10, str(_q1["waren"]))
check("P1: die Mission traegt frachtkanal 'waren'", m1["frachtkanal"] == "waren",
      str(m1.get("frachtkanal")))
check("P1: die Mission traegt genau die Fracht", m1["fracht"] == {WARE: 4},
      str(m1["fracht"]))
check("P1: die Mission ist ein Eigentransport von A nach B",
      m1.get("eigentransport") is True and m1["quelle_id"] == "A"
      and m1["ziel_id"] == "B", "%s -> %s" % (m1.get("quelle_id"), m1.get("ziel_id")))
check("P1: der Karren ist von der Quelle abgezogen",
      neu_q1["einheiten"].get("Handkarren", 0) == 0, str(neu_q1["einheiten"]))
check("P1: das Ziel ist noch leer (noch nichts angekommen)",
      _z1["waren"][WARE] == 0, str(_z1["waren"]))


# --------------------------------------------------------------------------
abschnitt("P2: Ankunft - die Ware kommt GENAU EINMAL an")

_ankunft = m1["ankunft"]
check("P2: die Ankunftszeit liegt nach dem Start", _ankunft > 0.0, str(_ankunft))

_orte1, _m1 = O.transport_fortschritt(m1, {"A": neu_q1, "B": _z1}, _ankunft)
check("P2: die Ware ist am Ziel angekommen", _orte1["B"]["waren"].get(WARE, 0) == 4,
      str(_orte1["B"]["waren"]))
check("P2: die Fracht ist aus der Mission abgebucht", _m1["fracht"] == {},
      str(_m1["fracht"]))
check("P2: der Liefermerker ist gesetzt", _m1["geliefert_lokal"] is True)

_orte2, _m2 = O.transport_fortschritt(_m1, _orte1, _ankunft)
check("P2: zweiter Aufruf mit demselben Zeitpunkt bucht NICHTS",
      _orte2["B"]["waren"].get(WARE, 0) == 4, str(_orte2["B"]["waren"]))
_orte3, _m3 = O.transport_fortschritt(_m2, _orte2, _ankunft + 1.0)
check("P2: auch ein weiterer Aufruf am Ziel bucht nicht doppelt",
      _orte3["B"]["waren"].get(WARE, 0) == 4, str(_orte3["B"]["waren"]))


# --------------------------------------------------------------------------
abschnitt("P3: Der Sieg-Ledger bleibt sauber (kein Importeintrag fuer Waren)")

check("P3: Warenankunft erzeugt KEINEN Eintrag in ziel['importiert']",
      _orte1["B"]["importiert"] == {}, str(_orte1["B"]["importiert"]))
check("P3: ziel['importiert'] ist nach der Ankunft unveraendert (leer wie zuvor)",
      _orte1["B"]["importiert"] == _z1["importiert"], str(_orte1["B"]["importiert"]))
check("P3: auch der Ausgangsort bekommt keinen Importeintrag",
      _orte1["A"]["importiert"] == {}, str(_orte1["A"]["importiert"]))

# Gegenprobe mit einem bereits vorhandenen Importeintrag: er darf nicht wachsen.
_z3 = ort("B", x=4, y=0, waren={WARE: 0}, importiert={"holz": 7})
_neu_q3, _m3b = O.transport_start(_q1, _z3, {"Handkarren": 1}, {WARE: 2}, 0.0,
                                  frachtkanal="waren")
_o3, _m3c = O.transport_fortschritt(_m3b, {"A": _neu_q3, "B": _z3}, _m3b["ankunft"])
check("P3: ein vorhandener Importeintrag bleibt Zeichen fuer Zeichen gleich",
      _o3["B"]["importiert"] == {"holz": 7}, str(_o3["B"]["importiert"]))
check("P3: die Ware ist trotzdem angekommen", _o3["B"]["waren"].get(WARE, 0) == 2,
      str(_o3["B"]["waren"]))


# --------------------------------------------------------------------------
abschnitt("P4: unbekannter Warenname aus dem Lager erlaubt, fehlende Ware nicht")

# (4a) Name ist kein Rohstoff und kein Rezept, liegt aber im Warenlager -> erlaubt.
_q4 = ort("A", x=0, y=0, waren={UNBEKANNT: 5, WARE: 1}, einheiten={"Handkarren": 1})
_z4 = ort("B", x=4, y=0, waren={})
_res4, _f4 = laeuft(lambda: O.transport_start(_q4, _z4, {"Handkarren": 1},
                                              {UNBEKANNT: 2}, 0.0, frachtkanal="waren"))
check("P4a: unbekannter Warenname aus dem Lager wird angenommen", _f4 == "", _f4)
if _res4 is not None:
    _nq4, _m4 = _res4
    check("P4a: die unbekannte Ware wird wirklich verschickt (5 -> 3)",
          _nq4["waren"][UNBEKANNT] == 3, str(_nq4["waren"]))
    check("P4a: die Mission bleibt im Warenkanal", _m4["frachtkanal"] == "waren",
          str(_m4.get("frachtkanal")))

# (4b) Ware, die NICHT im Lager liegt -> ValueError.
_q4b = ort("A", x=0, y=0, waren={WARE: 5}, einheiten={"Handkarren": 1})
_name4b, _msg4b = wirft(lambda: O.transport_start(_q4b, _z4, {"Handkarren": 1},
                                                  {"Feenstaub": 1}, 0.0,
                                                  frachtkanal="waren"))
check("P4b: eine Ware, die nicht im Lager liegt, wird abgelehnt",
      _name4b == "ValueError", "%s: %s" % (_name4b, _msg4b))


# --------------------------------------------------------------------------
abschnitt("P5: Karrenpflicht gilt auch im Warenkanal")

_q5 = ort("A", x=0, y=0, waren={WARE: 10}, einheiten={"Krieger": 3})
_z5 = ort("B", x=4, y=0, waren={})
_name5, _msg5 = wirft(lambda: O.transport_start(_q5, _z5, {"Krieger": 1}, {WARE: 1}, 0.0,
                                                frachtkanal="waren"))
check("P5: nur Krieger in der Garnison (ohne Karren) wird abgelehnt",
      _name5 == "ValueError", "%s: %s" % (_name5, _msg5))
check("P5: die Meldung nennt den fehlenden 'Karren'", "Karren" in _msg5, _msg5)


# --------------------------------------------------------------------------
abschnitt("P6: Ueberladung gilt auch fuer Waren (Handkarren = 40)")

_q6 = ort("A", x=0, y=0, waren={WARE: 100}, einheiten={"Handkarren": 1})
_z6 = ort("B", x=4, y=0, waren={})
_res6, _f6 = laeuft(lambda: O.transport_start(_q6, _z6, {"Handkarren": 1}, {WARE: 40},
                                              0.0, frachtkanal="waren"))
check("P6: genau 40 Einheiten (Handkarren-Ladung) sind erlaubt", _f6 == "", _f6)

_name6, _msg6 = wirft(lambda: O.transport_start(_q6, _z6, {"Handkarren": 1}, {WARE: 41},
                                                0.0, frachtkanal="waren"))
check("P6: 41 Einheiten werden als ueberladen abgelehnt",
      _name6 == "ValueError", "%s: %s" % (_name6, _msg6))
check("P6: die Meldung nennt 'Ueberladen' und die 40 Ladeplaetze",
      "Ueberladen" in _msg6 and "40" in _msg6, _msg6)


# --------------------------------------------------------------------------
abschnitt("P7: Rueckkehr bei Zielverlust - Fracht bleibt an der Mission")

_q7 = ort("A", x=0, y=0, waren={WARE: 10}, einheiten={"Handkarren": 1})
_z7 = ort("B", x=4, y=0, waren={WARE: 0})
_neu_q7, _m7 = O.transport_start(_q7, _z7, {"Handkarren": 1}, {WARE: 4}, 0.0,
                                 frachtkanal="waren")
check("P7: die Quelle hat die Ware beim Start abgegeben (10 -> 6)",
      _neu_q7["waren"][WARE] == 6, str(_neu_q7["waren"]))

_z7["besitzer"] = "feind"          # Ziel ist verloren/erobert
_o7a, _m7a = O.transport_fortschritt(_m7, {"A": _neu_q7, "B": _z7}, _m7["ankunft"])
check("P7: bei Zielverlust wird nichts gebucht (Zielware bleibt leer)",
      _o7a["B"]["waren"].get(WARE, 0) == 0, str(_o7a["B"]["waren"]))
check("P7: die Fracht bleibt an der Mission", _m7a["fracht"] == {WARE: 4},
      str(_m7a["fracht"]))
check("P7: der Ausgangsort ist auf der Rueckreise noch leer",
      _o7a["A"]["waren"][WARE] == 6, str(_o7a["A"]["waren"]))

_o7b, _m7b = O.transport_fortschritt(_m7a, _o7a, _m7["rueckkehr"])
check("P7: die Fracht kommt VOLL beim Ausgangsort zurueck (6 + 4 = 10)",
      _o7b["A"]["waren"][WARE] == 10, str(_o7b["A"]["waren"]))
check("P7: die Mission ist danach leer", _m7b["fracht"] == {}, str(_m7b["fracht"]))


# --------------------------------------------------------------------------
abschnitt("P8: Der Rohstoffkanal bleibt unveraendert (Abgrenzung)")

_q8 = ort("A", x=0, y=0, vorraete={"holz": 100}, einheiten={"Handkarren": 1})
_z8 = ort("B", x=4, y=0, vorraete={"holz": 0})
_neu_q8, _m8 = O.transport_start(_q8, _z8, {"Handkarren": 1}, {"holz": 30}, 0.0,
                                 frachtkanal="vorraete")
check("P8: frachtkanal 'vorraete' wird uebernommen", _m8["frachtkanal"] == "vorraete",
      str(_m8.get("frachtkanal")))
check("P8: die Quelle verliert den Rohstoff", _neu_q8["vorraete"]["holz"] == 70,
      str(_neu_q8["vorraete"]))
_o8, _m8b = O.transport_fortschritt(_m8, {"A": _neu_q8, "B": _z8}, _m8["ankunft"])
check("P8: der Rohstoff ist am Ziel", _o8["B"]["vorraete"]["holz"] == 30,
      str(_o8["B"]["vorraete"]))
check("P8: UND es entsteht ein Importeintrag (genau die Abgrenzung zum Warenkanal)",
      _o8["B"]["importiert"].get("holz") == 30, str(_o8["B"]["importiert"]))

# Der Warenkanal bleibt die Ausnahme; der Standard bleibt 'vorraete'.
_m8c = O.transport_start(_q8, _z8, {"Handkarren": 1}, {"holz": 1}, 0.0)[1]
check("P8: ohne Angabe ist der frachtkanal weiterhin 'vorraete'",
      _m8c["frachtkanal"] == "vorraete", str(_m8c.get("frachtkanal")))


# --------------------------------------------------------------------------
abschnitt("P9: Ein unbekannter frachtkanal wird abgelehnt")

_q9 = ort("A", x=0, y=0, waren={WARE: 5}, einheiten={"Handkarren": 1})
_z9 = ort("B", x=4, y=0, waren={})
_name9, _msg9 = wirft(lambda: O.transport_start(_q9, _z9, {"Handkarren": 1}, {WARE: 1},
                                                0.0, frachtkanal="goldbarren"))
check("P9: frachtkanal 'goldbarren' wird mit ValueError abgelehnt",
      _name9 == "ValueError", "%s: %s" % (_name9, _msg9))
check("P9: die Meldung nennt den Frachtkanal", "Frachtkanal" in _msg9, _msg9)


sys.exit(bericht())
