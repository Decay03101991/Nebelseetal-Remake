# -*- coding: ascii -*-
"""Nahrungsverbrauch je Einheit - Daniels Entscheidung 7 vom 31.10.2026.

Daniels Wortlaut: "Keine Lagerlimits, kein Unterhalt - ABER: Einheiten verbrauchen laufend
Nahrung." Der BETRAG ist ein VORSCHLAG (Rechnung in data/nahrungsverbrauch.json und
docs/SPIELBALANCING_TEST.md): 8 Nahrung je Einheit und SPIELTAG.

Was diese Datei beweist
-----------------------
1. Datenlage: die Datei existiert, nennt Version, Betrag, Herkunft der Rechnung und den Schalter;
   der Code liest den Schalter aus der DATEI (keine zweite Wahrheit im Quelltext).
2. Bedarfsfunktion mit Grenzfaellen -1 / 0 / +1 je Einheit und je Spanne: negative und
   nicht-numerische Mengen zaehlen nicht, 1 Einheit = 8/Tag, 0 Einheiten = 0.
3. Kern: `spieloekonomie.ort_tick` bucht den Verbrauch NACH der Ernte, genau EINMAL je Spanne -
   zwei halbe Takte ergeben denselben Bestand wie ein ganzer (Snapshot vorher/nachher).
4. `mengen` im produktionsjournal bleibt die REINE Ernte (das Versorgungsfenster rechnet damit
   weiter); der Verbrauch steht als eigener Posten daneben.
5. Unterdeckung: der Bestand faellt nie unter 0, der Rest steht als `unterdeckung` im Journal,
   und es gibt KEINE Strafe (Einheiten bleiben, wie sie sind) - eine Strafe waere eine eigene
   Entscheidung Daniels und ist bewusst nicht erfunden.
6. Anzeige == Kern: die Kopfzeile rechnet netto ueber `spieloekonomie.verbrauch_pro_stunde` ->
   `tagesbedarf_nahrung`, also ueber DIESELBE Funktion, die `ort_tick` bucht.

Aufruf:  python -X utf8 tests/test_nahrungsverbrauch.py
"""
from __future__ import annotations

import ast
import inspect
import json
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

ROOT, SRC = import_src()
import main  # noqa: E402
import spieloekonomie as O  # noqa: E402


def _daten(datei):
    with open(os.path.join(ROOT, "data", datei), encoding="utf-8") as f:
        return json.load(f)


DATEN = _daten("nahrungsverbrauch.json")
RATE = float(DATEN["je_einheit_pro_tag"])


def _code(funktion):
    """Quelltext einer Funktion OHNE Docstring (ein Docstring ist kein ausgefuehrter Code)."""
    quelle = textwrap.dedent(inspect.getsource(funktion))
    baum = ast.parse(quelle)
    knoten = baum.body[0]
    rumpf = getattr(knoten, "body", [])
    if rumpf and isinstance(rumpf[0], ast.Expr) and isinstance(rumpf[0].value, ast.Constant) \
            and isinstance(rumpf[0].value.value, str):
        knoten.body = rumpf[1:]
    return ast.unparse(baum)


def ort(vorraete=None, einheiten=None, bevoelkerung=5.0, produktionsjournal=None):
    """Ein Siedlungs-Ort mit allen Feldern, die ort_tick erwartet (ohne Ertrag)."""
    return {
        "id": "N",
        "besitzer": "spieler",
        "dimension": 0,
        "x": 0,
        "y": 0,
        "map_id": "karte1",
        "karte": {"raster": ["sumpf"]},
        "bauten": {},
        "stufen": {},
        "vorraete": dict(vorraete) if vorraete is not None else {},
        "waren": {},
        "einheiten": dict(einheiten) if einheiten is not None else {},
        "bevoelkerung": bevoelkerung,
        "importiert": {},
        "verbrauchsjournal": [],
        "produktionsjournal": list(produktionsjournal) if produktionsjournal else [],
        "fertigjournal": [],
        "werkstaetten": {},
        "ausbildung": [],
    }


def ohne(n, einheiten="Krieger"):
    return ort(vorraete={"nahrung": 1000.0}, einheiten={einheiten: n})


# ---------------------------------------------------------------- 1. Datenlage
print("\n=== 1. Datenlage: Betrag, Herkunft, Schalter ===")
check("data/nahrungsverbrauch.json vorhanden", bool(DATEN))
check("Version gesetzt", DATEN.get("version") == "nahrung-1", str(DATEN.get("version")))
check("je_einheit_pro_tag ist eine positive Zahl", isinstance(RATE, float) and RATE > 0,
      str(DATEN.get("je_einheit_pro_tag")))
check("Betrag ist 8 je Einheit und Spieltag (Vorschlag)", RATE == 8.0, str(RATE))
check("Code liest den Betrag AUS DER DATEI (keine zweite Zahl im Quelltext)",
      O.NAHRUNG_JE_EINHEIT_TAG == RATE, "%r gegen %r" % (O.NAHRUNG_JE_EINHEIT_TAG, RATE))
check("Code liest den Schalter AUS DER DATEI", O.NAHRUNGSVERBRAUCH_AKTIV == bool(DATEN.get("aktiv")),
      str(O.NAHRUNGSVERBRAUCH_AKTIV))
check("Schalter ist heute EIN", O.NAHRUNGSVERBRAUCH_AKTIV is True)
herkunft = str(DATEN.get("_herkunft", ""))
check("Herkunft nennt die Rechnung aus dem Reichsertrag",
      "5.542" in herkunft and "VORSCHLAG" in str(DATEN.get("_hinweis", "")), herkunft[:60])
check("Geltungsbereich dokumentiert (Ortslager, Auftraege zahlen Reisekosten)",
      "ORTSLAGER" in str(DATEN.get("_geltungsbereich", "")))
check("Unterdeckung ohne Strafe dokumentiert", "KEINE Strafe" in str(DATEN.get("_unterdeckung", "")))

# ------------------------------------------------- 2. Bedarf je Gruppe (Grenzfaelle)
print("\n=== 2. Bedarf einer Einheitengruppe: Grenzfaelle -1 / 0 / +1 ===")
check("0 Einheiten = 0 Bedarf", O.tagesbedarf_nahrung({}) == 0.0)
check("-1 Einheit zaehlt nicht (negative Menge)",
      O.tagesbedarf_nahrung({"Krieger": -1}) == 0.0)
check("0 Einheiten in der Gruppe = 0", O.tagesbedarf_nahrung({"Krieger": 0}) == 0.0)
check("+1 Einheit = 8 je Tag", O.tagesbedarf_nahrung({"Krieger": 1}) == RATE,
      str(O.tagesbedarf_nahrung({"Krieger": 1})))
check("100 Krieger = 800 je Tag", O.tagesbedarf_nahrung({"Krieger": 100}) == 100 * RATE)
check("Karren zaehlen mit (2 Handkarren = 16)", O.tagesbedarf_nahrung({"Handkarren": 2}) == 2 * RATE)
check("Summe ueber Arten (3 + 5 = 8 Einheiten)",
      O.tagesbedarf_nahrung({"Krieger": 3, "Handkarren": 5}) == 8 * RATE)
check("True (bool) zaehlt NICHT als Einheit", O.tagesbedarf_nahrung({"Krieger": True}) == 0.0)
check("Text zaehlt NICHT als Einheit", O.tagesbedarf_nahrung({"Krieger": "3"}) == 0.0)
check("None als Gruppe = 0 Bedarf", O.tagesbedarf_nahrung(None) == 0.0)
check("Schalter aus = 0 Bedarf, auch mit 100 Einheiten",
      O.tagesbedarf_nahrung({"Krieger": 100}, aktiv=False) == 0.0)
check("Reichsverbrauch je Stunde = Tagesbedarf / 24",
      abs(O.verbrauch_pro_stunde([{"einheiten": {"Krieger": 120}}]) - 120 * RATE / 24) < 1e-12,
      str(O.verbrauch_pro_stunde([{"einheiten": {"Krieger": 120}}])))


class _Stub:
    einheiten = {"Krieger": 24}


check("Anzeige-Hilfe akzeptiert Siedlungsobjekte (Settlement.einheiten)",
      abs(O.verbrauch_pro_stunde([_Stub()]) - 24 * RATE / 24) < 1e-12)

# ------------------------------------------------------ 3. Spanne (Grenzfaelle)
print("\n=== 3. Spanne: -1 / 0 / +1 Sekunde ===")
try:
    O.ort_tick(ohne(10), 100.0, 99.0, {})
    ruecklauf = False
except ValueError:
    ruecklauf = True
check("Spanne rueckwaerts (-1 s) = ValueError", ruecklauf)

o0 = O.ort_tick(ohne(100), 50.0, 50.0, {})  # Spanne 0
check("Spanne 0: kein Verbrauch", o0["vorraete"]["nahrung"] == 1000.0,
      str(o0["vorraete"]["nahrung"]))
check("Spanne 0: Journalzeile unveraendert (keine neue Zeile, kein Verbrauchsposten)",
      o0["produktionsjournal"] == [], str(o0["produktionsjournal"]))

o1 = O.ort_tick(ohne(1), 0.0, 1.0, {})  # 1 Sekunde, 1 Einheit
erwartet = 1000.0 - RATE / 86400.0
check("Spanne +1 s: genau 8/86400 je Einheit", abs(o1["vorraete"]["nahrung"] - erwartet) < 1e-12,
      str(o1["vorraete"]["nahrung"]))
check("Spanne +1 s: Verbrauch steht im Journal",
      abs(o1["produktionsjournal"][-1]["verbrauch"]["nahrung"] - RATE / 86400.0) < 1e-12,
      str(o1["produktionsjournal"][-1]["verbrauch"]))

oTag = O.ort_tick(ohne(100), 0.0, 86400.0, {})
check("Ein Spieltag, 100 Krieger = 800 Nahrung", abs(oTag["vorraete"]["nahrung"] - 200.0) < 1e-9,
      str(oTag["vorraete"]["nahrung"]))
oLeer = O.ort_tick(ort(vorraete={"nahrung": 500.0}, einheiten={}), 0.0, 86400.0, {})
check("Leeres Ortsheer: kein Verbrauch, Bestand bleibt",
      oLeer["vorraete"]["nahrung"] == 500.0, str(oLeer["vorraete"]["nahrung"]))
check("Leeres Ortsheer: Journalzeile unveraendert (nur ab/bis/mengen)",
      sorted(oLeer["produktionsjournal"][-1]) == ["ab", "bis", "mengen"],
      str(sorted(oLeer["produktionsjournal"][-1])))

# ------------------------------- 4. Genau einmal: ein Takt == zwei halbe Takte
print("\n=== 4. Genau EINMAL je Spanne (Snapshot vorher/nachher) ===")
start = ohne(100)
snapshot = json.dumps(start, sort_keys=True)
einer = O.ort_tick(start, 0.0, 3600.0, {})
halb = O.ort_tick(O.ort_tick(start, 0.0, 1800.0, {}), 1800.0, 3600.0, {})
check("Eingabe-Ort bleibt unveraendert (Snapshot)",
      json.dumps(start, sort_keys=True) == snapshot)
check("Ein Takt und zwei halbe Takte ergeben denselben Bestand",
      abs(einer["vorraete"]["nahrung"] - halb["vorraete"]["nahrung"]) < 1e-12,
      "%r gegen %r" % (einer["vorraete"]["nahrung"], halb["vorraete"]["nahrung"]))
check("Zwei halbe Takte ergeben zwei Journalzeilen, jede mit Verbrauch",
      len(halb["produktionsjournal"]) == 2
      and all("verbrauch" in z for z in halb["produktionsjournal"]),
      str(len(halb["produktionsjournal"])))
andere = {k: v for k, v in einer["vorraete"].items() if k != "nahrung"}
check("Nur die Nahrung sinkt, andere Vorraete bleiben",
      andere == {k: v for k, v in start["vorraete"].items() if k != "nahrung"}, str(andere))
check("Einheiten bleiben unangetastet (kein Sterben, keine Flucht)",
      einer["einheiten"] == start["einheiten"], str(einer["einheiten"]))

# --------------------------------------- 5. Ernte bleibt Ernte, Verbrauch daneben
print("\n=== 5. `mengen` bleibt die REINE Ernte ===")
mit = O.ort_tick(ohne(100), 0.0, 86400.0, {})
ohne_einheiten = O.ort_tick(ort(vorraete={"nahrung": 1000.0}), 0.0, 86400.0, {})
check("Erntemengen mit und ohne Garnison gleich",
      mit["produktionsjournal"][-1]["mengen"] == ohne_einheiten["produktionsjournal"][-1]["mengen"],
      str(mit["produktionsjournal"][-1]["mengen"]))
check("Verbrauch steht NEBEN den Mengen, nicht darin",
      "nahrung" not in mit["produktionsjournal"][-1]["mengen"]
      or mit["produktionsjournal"][-1]["mengen"]["nahrung"] >= 0,
      str(mit["produktionsjournal"][-1]["mengen"]))

# ------------------------------------------------------------ 6. Unterdeckung
print("\n=== 6. Unterdeckung: nie negativ, keine Strafe ===")
oNull = O.ort_tick(ohne(100, ) | {"vorraete": {"nahrung": 0.0}}, 0.0, 86400.0, {})
check("Bestand 0 bleibt 0 (nie negativ)", oNull["vorraete"]["nahrung"] == 0.0,
      str(oNull["vorraete"]["nahrung"]))
check("Bestand 0: ganzer Bedarf steht als Unterdeckung",
      abs(oNull["produktionsjournal"][-1]["unterdeckung"] - 800.0) < 1e-9,
      str(oNull["produktionsjournal"][-1]["unterdeckung"]))
oWenig = O.ort_tick(ohne(100) | {"vorraete": {"nahrung": 100.0}}, 0.0, 86400.0, {})
check("Bestand 100 bei Bedarf 800: Bestand 0, 700 fehlen",
      oWenig["vorraete"]["nahrung"] == 0.0
      and abs(oWenig["produktionsjournal"][-1]["unterdeckung"] - 700.0) < 1e-9,
      str(oWenig["produktionsjournal"][-1]["unterdeckung"]))
oGenau = O.ort_tick(ohne(100) | {"vorraete": {"nahrung": 800.0}}, 0.0, 86400.0, {})
check("Bestand exakt Bedarf: 0 Uebrig und 0 Unterdeckung",
      oGenau["vorraete"]["nahrung"] == 0.0
      and abs(oGenau["produktionsjournal"][-1]["unterdeckung"]) < 1e-12,
      str(oGenau["produktionsjournal"][-1]["unterdeckung"]))
oPlus = O.ort_tick(ohne(100) | {"vorraete": {"nahrung": 801.0}}, 0.0, 86400.0, {})
check("Bestand Bedarf + 1: genau 1 bleibt, keine Unterdeckung",
      abs(oPlus["vorraete"]["nahrung"] - 1.0) < 1e-9
      and abs(oPlus["produktionsjournal"][-1]["unterdeckung"]) < 1e-12,
      str(oPlus["vorraete"]["nahrung"]))
check("Unterdeckung toetet keine Einheit", oWenig["einheiten"] == {"Krieger": 100},
      str(oWenig["einheiten"]))

# ------------------------------------------------- 7. Anzeige == Kern (Wachen)
print("\n=== 7. EINE Rechnung fuer Kern UND Anzeige ===")
kern = _code(O.ort_tick)
check("ort_tick bucht ueber tagesbedarf_nahrung", "tagesbedarf_nahrung(" in kern)
check("ort_tick rechnet den Bedarf NICHT selbst (keine zweite Formel)",
      "86400" in kern and kern.count("tagesbedarf_nahrung(") == 1,
      "Aufrufe: %d" % kern.count("tagesbedarf_nahrung("))
bedarf_code = _code(O.tagesbedarf_nahrung)
check("tagesbedarf_nahrung liest den Betrag aus der Konstante",
      "NAHRUNG_JE_EINHEIT_TAG" in bedarf_code)
stunde_code = _code(O.verbrauch_pro_stunde)
check("verbrauch_pro_stunde ruft tagesbedarf_nahrung", "tagesbedarf_nahrung(" in stunde_code)
kopf_code = _code(main.kopf_zeilen_text)
check("Kopfzeile rechnet NETTO ueber spieloekonomie.verbrauch_pro_stunde",
      "verbrauch_pro_stunde" in kopf_code)
check("Kopfzeile baut keine eigene Verbrauchsformel",
      "je_einheit_pro_tag" not in kopf_code and "NAHRUNG_JE_EINHEIT_TAG" not in kopf_code)
quelle_main = inspect.getsource(main)
# Register 121: die Mengen stehen jetzt auf der C2-Ressourcenleiste, die Detailzeile zeigt fuer
# diese Rohstoffe nur die Rate. Die EINE Hilfsfunktion heisst deshalb `kopfzeile_fuer`; sie waehlt
# zwischen `kopf_rate_text` und `kopf_zeilen_text`. Beide Wege lesen dieselbe Verbrauchsquelle
# (`spieloekonomie.verbrauch_pro_stunde`), was die zwei Pruefungen darunter belegen.
check("Kopfzeilen-Hilfe wird an BEIDEN Stellen benutzt (Aufbau und Neuzeichnen)",
      quelle_main.count("kopfzeile_fuer(self.state, r, ertrag_jetzt)") == 2,
      "Treffer: %d" % quelle_main.count("kopfzeile_fuer(self.state, r, ertrag_jetzt)"))
check("kopfzeile_fuer waehlt zwischen Rate und voller Zeile",
      "kopf_rate_text(" in _code(main.kopfzeile_fuer)
      and "kopf_zeilen_text(" in _code(main.kopfzeile_fuer), "")
check("Negative Rate wird sauber angezeigt (kein '+-3/h')",
      "if rate > 0 else" in kopf_code, kopf_code[:80])

sys.exit(bericht())
