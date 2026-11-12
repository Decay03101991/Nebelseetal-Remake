# -*- coding: ascii -*-
"""Wagenbau-Kapazitaet (Daniels Entscheidung 2, 31.10.2026).

Daniels Wortlaut (Uebergabe 31.10.2026): "Karren-Kapazitaet waechst mit Forschung 'Wagenbau' -
die belegten Einheitenwerte (data/units.json) bleiben die Basis, Bonus obendrauf."

Was diese Datei beweist
-----------------------
1. Datenlage: `data/karrenkapazitaet.json` nennt Forschung, Prozentsatz, Hoechststufe und Schalter;
   der Code liest ALLES aus dieser Datei (keine zweite Zahl im Quelltext).
2. Die BASISWERTE bleiben unveraendert: ohne Forschung ist die Ladung genau der Wert aus
   `data/units.json` (40/100/250/1000/2500) - der Bonus kommt nur obendrauf.
3. Grenzfaelle -1 / 0 / +1 und ueber die Hoechststufe: Stufe -1 und 0 = Basis, 1 = +10 %,
   10 = doppelt, 11 wird auf 10 gedeckelt; fremde Forschungen geben KEINEN Bonus.
4. EINE Rechnung: `ladung_der_gruppe` ist die Summe der Einzelkapazitaeten aus derselben Funktion.
5. Der Bonus wirkt im KERN, nicht nur in der Anzeige: `auftraege.ladung_der_mission`,
   `kampfbericht.beute_staffel` und `beute_am_ziel` rechnen mit den uebergebenen Forschungsstufen.
6. Quelltext-Wachen: JEDE Stelle in `src/`, die eine Kapazitaet ausrechnet, gibt die Stufen mit -
   sonst gaebe es eine Anzeige mit Bonus und einen Kern ohne (das Muster des F-04-Befunds).

Aufruf:  python -X utf8 tests/test_wagenbau_kapazitaet.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "quelltext"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['auftraege', 'einheiten', 'forschung', 'kampfbericht', 'main:*']
PRUEF_DATEN = ['karrenkapazitaet.json', 'units.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import ast
import inspect
import json
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import auftraege  # noqa: E402
import einheiten as E  # noqa: E402
import kampfbericht as KB  # noqa: E402


def _daten(datei):
    with open(os.path.join(ROOT, "data", datei), encoding="utf-8") as f:
        return json.load(f)


DATEN = _daten("karrenkapazitaet.json")
UNITS = _daten("units.json")["einheiten"]
PRO_STUFE = float(DATEN["pro_stufe_prozent"])
HOECHST = int(DATEN["hoechststufe"])

# Namen aus den DATEN lesen - die Dateien enthalten Umlaute, diese Pruefdatei ist ASCII.
ZWEISP = next(n for n in E.alle() if n.startswith("Zweisp"))
HANDKARREN = next(n for n in E.alle() if n.startswith("Handkarren"))
KRIEGER = next(n for n in E.alle() if n == "Krieger")
BASIS = {n: E.alle()[n]["ladung"] for n in (ZWEISP, HANDKARREN) if E.alle()[n]["ladung"]}


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


# ---------------------------------------------------------------- 1. Datenlage
print("\n=== 1. Datenlage: Forschung, Prozentsatz, Schalter ===")
check("data/karrenkapazitaet.json vorhanden", bool(DATEN))
check("Version gesetzt", DATEN.get("version") == "karren-1", str(DATEN.get("version")))
check("Forschung ist Wagenbau", DATEN.get("forschung") == "Wagenbau", str(DATEN.get("forschung")))
check("Prozentsatz ist eine positive Zahl", PRO_STUFE > 0, str(PRO_STUFE))
check("Hoechststufe gesetzt", HOECHST >= 1, str(HOECHST))
check("Code liest den Prozentsatz AUS DER DATEI", E.KARREN_PRO_STUFE == PRO_STUFE,
      "%r gegen %r" % (E.KARREN_PRO_STUFE, PRO_STUFE))
check("Code liest die Hoechststufe AUS DER DATEI", E.KARREN_HOECHSTSTUFE == HOECHST)
check("Code liest den Schalter AUS DER DATEI", E.KARREN_BONUS_AKTIV == bool(DATEN.get("aktiv")))
check("Hinweis kennzeichnet den Wert als VORSCHLAG",
      "VORSCHLAG" in str(DATEN.get("_hinweis", "")))
check("Geltungsbereich: nur Ladung, nicht Tempo/Preis",
      "TRAGFAEHIGKEIT" in str(DATEN.get("_geltungsbereich", "")))

# ------------------------------------------------- 2. Basiswerte bleiben die Basis
print("\n=== 2. Die belegten Werte bleiben die BASIS ===")
for name, wert in BASIS.items():
    check("%s: Ladung aus data/units.json unveraendert (%s)" % (name, wert),
          E.ladung(name) == int(UNITS[name]["ladung"]) == int(wert), str(E.ladung(name)))
check("ohne Forschungsangabe: Basiswert 1:1",
      E.ladung_der_gruppe({ZWEISP: 1}) == int(BASIS[ZWEISP]),
      str(E.ladung_der_gruppe({ZWEISP: 1})))
check("leere Forschungsangabe: Basiswert 1:1",
      E.ladung_der_gruppe({ZWEISP: 1}, {}) == int(BASIS[ZWEISP]))
check("None als Forschungsangabe: Basiswert 1:1",
      E.ladung_der_gruppe({ZWEISP: 1}, None) == int(BASIS[ZWEISP]))
check("Krieger tragen nichts, auch mit Bonus",
      E.ladung_der_gruppe({KRIEGER: 10}, {"Wagenbau": 10}) == 0)

# ------------------------------------------------ 3. Grenzfaelle und Deckelung
print("\n=== 3. Grenzfaelle -1 / 0 / +1 und ueber die Hoechststufe ===")
basis = int(BASIS[ZWEISP])


def mit(stufe):
    return E.ladung_der_gruppe({ZWEISP: 1}, {"Wagenbau": stufe})


check("Stufe -1 wirkt NICHT (kein Minus-Bonus)", mit(-1) == basis, str(mit(-1)))
check("Stufe 0 = Basis", mit(0) == basis, str(mit(0)))
check("Stufe +1 = Basis + Prozentsatz", mit(1) == basis + int(basis * PRO_STUFE / 100.0),
      "%s (Basis %s)" % (mit(1), basis))
check("Stufe %d = doppelte Ladung" % HOECHST, mit(HOECHST) == basis * 2, str(mit(HOECHST)))
check("Stufe %d wird auf %d gedeckelt" % (HOECHST + 1, HOECHST), mit(HOECHST + 1) == mit(HOECHST))
check("fremde Forschung (Baukunst) gibt KEINEN Bonus", mit(0) == basis
      and E.ladung_der_gruppe({ZWEISP: 1}, {"Baukunst": 10}) == basis)
check("Text als Stufe zaehlt nicht", E.ladung_der_gruppe({ZWEISP: 1}, {"Wagenbau": "viel"}) == basis)
check("doppelte Ladung bleibt ganzzahlig",
      isinstance(mit(HOECHST), int), str(type(mit(HOECHST))))
stufen = [(s, mit(s)) for s in range(0, HOECHST + 1)]
check("Ladung steigt mit jeder Stufe (monoton)", all(a[1] <= b[1] for a, b in zip(stufen, stufen[1:])),
      str(stufen))

# ------------------------------------------------------------ 4. EINE Rechnung
print("\n=== 4. EINE Rechnung fuer die ganze Gruppe ===")
gruppe = {ZWEISP: 3, HANDKARREN: 5}
einzeln = (E.kapazitaet_mit_bonus(ZWEISP, 3, {"Wagenbau": 4})
           + E.kapazitaet_mit_bonus(HANDKARREN, 5, {"Wagenbau": 4}))
check("Summe der Einzelkapazitaeten == Gruppenkapazitaet",
      E.ladung_der_gruppe(gruppe, {"Wagenbau": 4}) == einzeln,
      "%s gegen %s" % (E.ladung_der_gruppe(gruppe, {"Wagenbau": 4}), einzeln))
check("Basisweg (ohne Bonus) bleibt daneben bestehen",
      E.ladung_der_gruppe(gruppe) == 3 * basis + 5 * int(BASIS[HANDKARREN]))
check("negative Anzahl zaehlt nicht", E.kapazitaet_mit_bonus(ZWEISP, -3, {"Wagenbau": 10}) == 0)
check("bool zaehlt nicht als Anzahl", E.kapazitaet_mit_bonus(ZWEISP, True, {"Wagenbau": 10}) == 0)

# ------------------------------------------------------- 5. Schalter und Kern
print("\n=== 5. Schalter aus, Bonus weg - im KERN, nicht nur in der Anzeige ===")
_alt = E.KARREN_BONUS_AKTIV
try:
    E.KARREN_BONUS_AKTIV = False
    check("Schalter aus: Gruppenladung = Basis",
          E.ladung_der_gruppe({ZWEISP: 2}, {"Wagenbau": 10}) == 2 * basis)
    check("Schalter aus: Faktor genau 1.0", E.ladungs_bonus({"Wagenbau": 10}) == 1.0)
finally:
    E.KARREN_BONUS_AKTIV = _alt

kern = _code(auftraege.ladung_der_mission)
check("auftraege.ladung_der_mission gibt die Stufen an den Kern weiter",
      "ladung_der_gruppe(einheiten, forschung)" in kern, kern[:80])

starten = _code(auftraege.starten)
check("auftraege.starten prueft die Fracht MIT Stufen",
      "ladung_der_mission(bestand, forschung)" in starten)
check("auftraege.starten gibt die Stufen an die Beutevorschau weiter",
      "forschung=forschung" in starten)

staffel = _code(KB.beute_staffel)
check("beute_staffel rechnet die Kapazitaet MIT Stufen",
      "ladung_der_gruppe(einheiten_des_siegers, forschung)" in staffel)
am_ziel = _code(KB.beute_am_ziel)
check("beute_am_ziel gibt die Stufen an die Staffel weiter", "forschung=forschung" in am_ziel)

# Die Beute ist die Probe aufs Exempel: 10 Zweispaenner tragen ohne Forschung 2.500,
# mit Wagenbau 5 genau das 1,5-fache.
vorrat = {"holz": 100000, "stein": 100000, "nahrung": 100000}
ohne = KB.beute_staffel({ZWEISP: 10}, dict(vorrat), wall_zustand_vor=100.0, verteidiger_uebrig=1)
mit_bonus = KB.beute_staffel({ZWEISP: 10}, dict(vorrat), wall_zustand_vor=100.0,
                             verteidiger_uebrig=1, forschung={"Wagenbau": 5})
check("Beute ohne Forschung voll ausgelastet (Ladung ist der Deckel)",
      sum(ohne.values()) == 10 * basis, str(sum(ohne.values())))
check("Beute mit Wagenbau 5 ist groesser als ohne",
      sum(mit_bonus.values()) > sum(ohne.values()),
      "%s gegen %s" % (sum(mit_bonus.values()), sum(ohne.values())))
check("Beute mit Wagenbau 5 genau das 1,5-fache",
      sum(mit_bonus.values()) == int(sum(ohne.values()) * 1.5),
      "%s erwartet %s" % (sum(mit_bonus.values()), int(sum(ohne.values()) * 1.5)))

# ------------------------------------------- 6. Quelltext-Wachen ueber ganz src/
print("\n=== 6. Jede Kapazitaetsstelle gibt die Stufen mit ===")
ohne_stufen = []
for datei in sorted(os.listdir(SRC)):
    if not datei.endswith(".py"):
        continue
    with open(os.path.join(SRC, datei), encoding="utf-8") as f:
        baum = ast.parse(f.read())
    for knoten in ast.walk(baum):
        if not isinstance(knoten, ast.Call):
            continue
        name = getattr(knoten.func, "attr", None) or getattr(knoten.func, "id", None)
        if name in ("ladung_der_gruppe", "ladung_der_mission"):
            if len(knoten.args) < 2 and not any(k.arg == "forschung" for k in knoten.keywords):
                ohne_stufen.append("%s:%d %s" % (datei, knoten.lineno, name))
check("keine Kapazitaetsrechnung ohne Forschungsstufen", not ohne_stufen,
      ", ".join(ohne_stufen[:6]))
mit_stufen_anzeige = _code(__import__("main").kopf_zeilen_text) if False else ""
import main  # noqa: E402
quelle_main = inspect.getsource(main)
check("GameState hat EINE Lesestelle fuer die Stufen", "def forschungs_stufen(" in quelle_main)
_stellen = (quelle_main.count("forschung=self.state.forschungs_stufen()")
            + quelle_main.count("forschung=self.forschungs_stufen()"))
check("Main gibt die Stufen an Auftrag, Beute, Transport und Handel (mindestens 6 Stellen)",
      _stellen >= 6, "Treffer: %d" % _stellen)


def _self_state_in_klasse(klasse: str):
    """Jede Methode einer Klasse, die `self.state` benutzt - im GameState ist das ein Fehler."""
    baum = ast.parse(quelle_main)
    for knoten in baum.body:
        if isinstance(knoten, ast.ClassDef) and knoten.name == klasse:
            return [n.lineno for n in ast.walk(knoten)
                    if isinstance(n, ast.Attribute) and n.attr == "state"
                    and isinstance(n.value, ast.Name) and n.value.id == "self"]
    return []


check("GameState greift NIRGENDS auf self.state zu (sonst AttributeError)",
      not _self_state_in_klasse("GameState"), str(_self_state_in_klasse("GameState")[:5]))
check("NebelseetalApp benutzt self.state (Gegenprobe)",
      len(_self_state_in_klasse("NebelseetalApp")) > 100)
befund("Anzeige der Ladeplaetze nutzt ladung_mit_bonus/kapazitaet_mit_bonus - "
       "eine Wache darauf waere nur ein Textvergleich", "")

sys.exit(bericht())
