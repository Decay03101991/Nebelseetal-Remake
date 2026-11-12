# -*- coding: ascii -*-
"""S4-6c: Handel in der SPIELSCHICHT (07.11.2026, Register 292, docs/ABLAUF_LLM_20261106.md Schritt 6c).

Geprueft wird, was der Schnitt zusagt:
  A. Ein frischer Zustand der Messschicht traegt `handels_erloes`, `letzter_handel` und
     `haendler_gold`; ein ALTER Stand ohne diese Felder wird beim ersten Zugriff nachgezogen.
  B. Ohne Handelskarawane gibt es keinen Handel - und der Zustand bleibt unveraendert.
  C. Ohne Ueberschuss ueber dem Mindestvorrat gibt es keinen Handel (Gold ist nie Handelsgut).
  D. Ein Verkauf bucht nach DENSELBEN Regeln wie das Spiel: Ware nimmt ab, Gold kommt an, die
     Karre ist heim, `handels_erloes` steigt um den Erloes, `letzter_handel` ist der Zeitpunkt
     der ANNAHME, und `punkte.handelspunkte` liefert dieselbe Zahl aus demselben Zaehler.
     Der Erwartungswert wird AUS DER GEPRUEFTEN FUNKTION abgeleitet, nicht hingeschrieben.
  E. Keine Doppelbuchung: der Partner kauft genau einmal, danach ist sein Gold aufgebraucht und
     ein zweiter Verkauf aendert den Zaehler nicht.
  F. EINE Preisfunktion (Muster F-04): die Schwelle der Messschicht ist die Schwelle des Spiels
     (`botkern.BESCHAFFUNGSKOSTEN` -> `botkern.handelspreis`), und die Messschicht enthaelt keine
     eigene Preistafel (Quellwache).
  G. Der Verkauf laeuft im ECHTEN Werkzeug: ein Lauf mit Handelskarawane zeigt Handelspunkte
     groesser 0 im Kennzahlenblatt-Feld `handelspunkte` (Fertig-Kriterium des Ablaufs).

ASCII-only (Pruefdatei-Konvention).
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['botkern', 'einheiten', 'main:*', 'punkte', 'spielschicht']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import inspect
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

import_src()
import botkern
import punkte as PUNKTE
import spielschicht as S

TAG = 86400.0


def _verkaufsreif(saat=7, karawanen=1, holz=1500.0):
    """Einen Zustand herstellen, der verkaufen KANN - ueber den echten Aufbau der Schicht."""
    z = S.neuer_zustand(saat)
    if karawanen:
        z["einheiten"]["Handelskarawane"] = karawanen
    z["ressourcen"]["holz"] = float(holz)
    return z


abschnitt("A. Felder im Spielstand und Ladewache fuer alte Staende")
_z = S.neuer_zustand(7)
check("neuer Zustand traegt handels_erloes 0.0", _z.get("handels_erloes") == 0.0,
      repr(_z.get("handels_erloes")))
check("neuer Zustand traegt letzter_handel 0.0", _z.get("letzter_handel") == 0.0,
      repr(_z.get("letzter_handel")))
check("neuer Zustand traegt Gold des Handelspartners", float(_z.get("haendler_gold") or 0) > 0,
      repr(_z.get("haendler_gold")))
check("das Gold des Partners kommt aus der Datendatei",
      float(_z.get("haendler_gold") or 0) == float(S._handelsregel("haendler_gold", 0)),
      "%s gegen %s" % (_z.get("haendler_gold"), S._handelsregel("haendler_gold", 0)))

_alt = S.neuer_zustand(7)
for _feld in ("handels_erloes", "letzter_handel", "haendler_gold"):
    _alt.pop(_feld, None)
_alt["einheiten"]["Handelskarawane"] = 1
_alt["ressourcen"]["holz"] = 1500.0
_ok_alt, _info_alt = S.verkauf_an_haendler(_alt, TAG)
check("ein alter Stand ohne Felder laedt und verkauft", _ok_alt is True, str(_info_alt.get("grund")))
check("die Ladewache hat handels_erloes nachgezogen", "handels_erloes" in _alt)
check("die Ladewache hat letzter_handel nachgezogen", "letzter_handel" in _alt)

abschnitt("B. Ohne Handelskarawane kein Handel, Zustand unveraendert")
_leer = _verkaufsreif(karawanen=0)
_vorher = dict(_leer["ressourcen"])
_ok, _info = S.verkauf_an_haendler(_leer, TAG)
check("ohne Karawane abgelehnt", _ok is False, str(_info))
check("ohne Karawane bleibt das Lager gleich", _leer["ressourcen"] == _vorher)
check("ohne Karawane steigt kein Zaehler", float(_leer["handels_erloes"]) == 0.0)

abschnitt("C. Ohne Ueberschuss und ohne Gold des Partners kein Handel")
_knapp = _verkaufsreif(holz=float(S._handelsregel("mindestvorrat", 200)))
_ok, _info = S.verkauf_an_haendler(_knapp, TAG)
check("am Mindestvorrat abgelehnt", _ok is False, str(_info.get("grund")))
_leer_gold = _verkaufsreif()
_leer_gold["haendler_gold"] = 1.0
_ok, _info = S.verkauf_an_haendler(_leer_gold, TAG)
check("ein leergekaufter Partner wird abgelehnt", _ok is False, str(_info.get("grund")))

abschnitt("D. Ein Verkauf bucht wie im Spiel (Erwartung aus der geprueften Funktion)")
_z = _verkaufsreif()
_holz_vorher = float(_z["ressourcen"]["holz"])
_gold_vorher = float(_z["ressourcen"].get("gold") or 0.0)
_ok, _info = S.verkauf_an_haendler(_z, TAG)
check("Verkauf gelingt", _ok is True, str(_info))
_menge = int(_info.get("menge") or 0)
_preis = float(_info.get("preis") or 0.0)
check("die Menge ist positiv und gedeckelt", 0 < _menge <= _holz_vorher - 200, str(_menge))
check("Gold wird nie als Ware verkauft", str(_info.get("ware")) != "gold", str(_info.get("ware")))
check("die Ware hat das Lager verlassen",
      abs(float(_z["ressourcen"]["holz"]) - (_holz_vorher - _menge)) < 1e-6,
      "%s nachher, %s vorher, %d verkauft" % (_z["ressourcen"]["holz"], _holz_vorher, _menge))
_erwarteter_erloes = round(_menge * _preis, 2)
check("der Erloes ist Menge x Preis",
      abs(float(_z["handels_erloes"]) - _erwarteter_erloes) < 1e-6,
      "%s gegen %s" % (_z["handels_erloes"], _erwarteter_erloes))
check("das Gold ist im Lager angekommen",
      abs(float(_z["ressourcen"].get("gold") or 0.0) - (_gold_vorher + _erwarteter_erloes)) < 1e-6,
      "%s nachher, %s vorher" % (_z["ressourcen"].get("gold"), _gold_vorher))
check("die Karawane ist wieder im Reichsheer", int(_z["einheiten"].get("Handelskarawane") or 0) == 1)
check("letzter_handel ist der Zeitpunkt der Annahme",
      float(_z["letzter_handel"]) == float(_info.get("ankunft") or -1),
      "%s gegen %s" % (_z["letzter_handel"], _info.get("ankunft")))
_erwartete_punkte = float(PUNKTE.handelspunkte(_z["handels_erloes"], _z["letzter_handel"], TAG))
check("die Handelspunkte kommen aus DEMSELBEN Zaehler und sind groesser 0",
      _erwartete_punkte > 0.0, str(_erwartete_punkte))
check("ein Ereignis steht in den Nachrichten",
      any("verkauft" in str(e.get("text")) for e in (_z.get("ereignisse") or [])))

abschnitt("E. Keine Doppelbuchung - der Partner kauft genau einmal")
_stand_erloes = float(_z["handels_erloes"])
_rest = float(_z["haendler_gold"])
check("das Gold des Partners ist aufgebraucht", _rest < _preis, "%s Gold, Preis %s" % (_rest, _preis))
_ok2, _info2 = S.verkauf_an_haendler(_z, TAG + 60.0)
check("ein zweiter Verkauf wird abgelehnt", _ok2 is False, str(_info2.get("grund")))
check("der Zaehler bleibt unveraendert", float(_z["handels_erloes"]) == _stand_erloes,
      "%s gegen %s" % (_z["handels_erloes"], _stand_erloes))

abschnitt("F. EINE Preisfunktion - die Schwelle des Spiels (F-04)")
_quelle = inspect.getsource(S)
check("die Messschicht liest die Beschaffungskosten aus botkern",
      "botkern.BESCHAFFUNGSKOSTEN" in _quelle)
check("die Schwelle ist botkern.handelspreis(botkern.referenzpreis_aus_beschaffung(...))",
      abs(S._schwellenpreis() - float(botkern.handelspreis(
          botkern.referenzpreis_aus_beschaffung(botkern.BESCHAFFUNGSKOSTEN), 0.0))) < 1e-9,
      str(S._schwellenpreis()))
_verdacht = [z.strip() for z in _quelle.splitlines()
             if z.strip().startswith("BESCHAFFUNGSKOSTEN") or "= 300.0" in z
             or "preis = 300" in z]
check("keine zweite Preistafel in der Messschicht", not _verdacht, str(_verdacht[:3]))
import main  # noqa: E402  - die App liest denselben Wert (eine Quelle, zwei Schichten)
check("die App rechnet mit demselben Beschaffungswert",
      float(main.BOT_BESCHAFFUNGSKOSTEN) == float(botkern.BESCHAFFUNGSKOSTEN),
      "%s gegen %s" % (main.BOT_BESCHAFFUNGSKOSTEN, botkern.BESCHAFFUNGSKOSTEN))
check("die App-Schwelle ist die Schwelle der Messschicht",
      abs(float(S._schwellenpreis())
          - float(botkern.handelspreis(botkern.referenzpreis_aus_beschaffung(
              main.BOT_BESCHAFFUNGSKOSTEN), 0.0))) < 1e-9)

abschnitt("G. Der Verkauf laeuft im Werkzeug (Fertig-Kriterium des Ablaufs)")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))
import spieltest_simulation as SIM  # noqa: E402
_log = SIM.spielen(20.0, 7, "breit")
_ende = _log.get("ende") or {}
check("das Werkzeug zeigt eine ZAHL statt null", _ende.get("handelspunkte") is not None,
      repr(_ende.get("handelspunkte")))
check("die Handelspunkte sind groesser 0", float(_ende.get("handelspunkte") or 0.0) > 0.0,
      repr(_ende.get("handelspunkte")))
check("der Lauf hat wirklich gehandelt", len(_log.get("handel") or []) >= 1,
      str(_log.get("handel")))
_zeile = SIM.kennzahlen(_log, 20.0, 7, "breit")
check("das Kennzahlenblatt traegt die Handelspunkte",
      float(_zeile.get("handelspunkte") or 0.0) > 0.0, repr(_zeile.get("handelspunkte")))

bericht()
