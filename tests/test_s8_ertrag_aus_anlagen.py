# -*- coding: ascii -*-
"""Wache S-8 Stufe 1: der Ertrag eines Bot-Dorfes kommt aus seinen GEBAUTEN ANLAGEN.

DAS PROBLEM, GEMESSEN (vor dem Umbau)
-------------------------------------
`bot_dorf_ertrag` rechnete `bot_kartenprofil(karte)`: Summe ueber die FELDER der Karte, egal ob dort
etwas stand. Ein Dorf mit 48 Holzfaellern erntete damit genau so viel wie eines mit 5 (Silra 13,6
Holz/h in beiden Faellen) - jede Bauplan-Logik war wirkungslos, und Daniel konnte seinen Wunsch (der
Bot nutzt seine Karte mit Gebaeuden sinnvoll) nicht greifen.

Was diese Datei beweist
-----------------------
1. Der Ertrag wird GERECHNET, nicht erfunden: je belegtem Feld die Anlage und das Gelaende, auf dem
   sie steht (`gelaende.ertrag_pro_stunde`), plus Grundeinkommen der Originalsiedlung - dieselbe
   Kernfunktion wie beim Spieler (`wirtschaft.ertrag_gesamt`). Die Handrechnung steht daneben.
2. Wer MEHR Anlagen baut, erntet MEHR (5 gegen 12 Holzfaeller auf derselben Karte) - die Pruefzusage
   aus `docs/KONZEPT_BOT_BAUPLAN_20261103.md`, Stufe 1.
3. Ein Dorf ganz OHNE Anlagen faellt auf das Kartenprofil zurueck (alter Spielstand) und stuerzt
   nicht ab; ohne Karte gilt der Bauplan-Rueckfall.
4. Das Kartenprofil ist nur noch VORSCHAU - es ist NICHT der Ertrag.
5. REGRESSION: ein Dorf, das schon einen Siedlerkarren hat, wird nicht noch einmal belastet (vorher
   wurden je Takt 200 Holz abgebucht und danach abgelehnt - der ungeklaerte Holzschwund).
6. REGRESSION: bei Karrenpflicht ist nur ein Dorf MIT Karren Ausgangsdorf einer Gruendung.
7. Quellwache: `bot_dorf_ertrag` rechnet ueber `wirtschaft.ertrag_gesamt` (EINE Wahrheit fuer Kern
   und Anzeige, F-04).

Aufruf:  python -X utf8 tests/test_s8_ertrag_aus_anlagen.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "quelltext"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['einheiten', 'gelaende', 'main:*', 'wirtschaft']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
import gelaende  # noqa: E402
import main as M  # noqa: E402
import wirtschaft  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
EINST = M.bot_wirtschaft_einstellungen()
KARTE = "original-001"                                     # feste Karte fuer den Grundaufbau
WALDKARTE = "original-125"                                 # 50 Wald-Felder: Platz fuer zwoelf Holzfaeller


def _stand():
    """Ein leerer Spielstand - nur damit eine GameState-Methode aufrufbar ist."""
    return M.GameState()


def _dorf(name: str, karte: str = KARTE, bauen: bool = True):
    """Ein Bot-Dorf mit bebauten Feldern (oder ohne, wenn `bauen` aus ist)."""
    dorf = M.BotDorf(name=name, karte=karte)               # Bot-Dorf mit dieser Karte
    if bauen:                                              # Grundanlagen aus dem Bauplan setzen
        M.bot_doerfer_bebauen(dorf, EINST)                 # dieselbe Funktion wie im Bot-Takt
    return dorf


def _raster(dorf):
    """Das 10x10-Raster der Karte eines Dorfes (aus den Spieldaten, nicht getippt)."""
    return list((M._bot_karte_dict(dorf.karte) or {}).get("raster") or [])


def _mehr_holzfaeller(dorf, soll: int) -> int:
    """Setzt Holzfaeller, bis `soll` davon stehen - nur auf freie WALD-Felder."""
    raster = _raster(dorf)
    steht = sum(1 for g in dorf.bauten.values() if str(g) == "holzfaeller")
    frei = [i for i in range(len(raster)) if str(i) not in dorf.bauten]
    for i in frei:                                          # jedes freie Feld ansehen
        if steht >= soll:                                   # genug
            break
        if not gelaende.bau_moeglich("holzfaeller", raster[i])[0]:   # darf er dort stehen?
            continue
        if raster[i] != "wald":                             # nur Wald belegen (bester Ertrag)
            continue
        dorf.bauten[str(i)] = "holzfaeller"
        dorf.stufen[str(i)] = 1
        steht += 1
    return steht


# ==========================================================================
abschnitt("1. Der Ertrag wird aus den Feldern GERECHNET (Handrechnung daneben)")
# ==========================================================================
dorf = _dorf("Handrechnung")
raster = _raster(dorf)
erwartet = {}
for feld, geb in dorf.bauten.items():                      # jedes belegte Feld einzeln
    art = raster[int(feld)]                                # Gelaende dieses Feldes
    wert = gelaende.ertrag_pro_stunde(geb, art)            # Ertrag der Anlage dort
    if isinstance(wert, dict):                             # mehrere Rohstoffe (Rinderfarm)
        for roh, menge in wert.items():
            erwartet[str(roh).lower()] = round(erwartet.get(str(roh).lower(), 0.0) + float(menge), 2)
    elif isinstance(wert, (int, float)):                   # ein Rohstoff
        eintrag = gelaende.alle_gebaeude().get(geb) or {}
        roh = str(eintrag.get("rohstoff") or "").lower()
        if roh:
            erwartet[roh] = round(erwartet.get(roh, 0.0) + float(wert), 2)
for roh, menge in wirtschaft.ORIGINAL_GRUNDEINKOMMEN.items():   # Grundeinkommen der Originalsiedlung
    erwartet[str(roh).lower()] = round(erwartet.get(str(roh).lower(), 0.0) + float(menge), 2)
gemessen = M.bot_dorf_ertrag(dorf)
check("1 die Handrechnung ueber die Felder trifft den gemessenen Ertrag",
      {k: round(float(v), 2) for k, v in gemessen.items() if k in erwartet}
      == {k: round(float(v), 2) for k, v in erwartet.items() if k in gemessen},
      "%s / %s" % (gemessen, erwartet))
check("1 die Anlagen sind die Ursache: ohne sie gaebe es diese Zahlen nicht",
      len(dorf.bauten) > 10 and float(gemessen.get("holz", 0)) > 10, str(gemessen))

# ==========================================================================
abschnitt("2. Mehr Anlagen = mehr Ertrag (die Pruefzusage der Stufe 1)")
# ==========================================================================
klein = _dorf("Fuenf", karte=WALDKARTE, bauen=False)      # nur Holzfaeller, kein Grundaufbau
gross = _dorf("Zwoelf", karte=WALDKARTE, bauen=False)
_fuenf = _mehr_holzfaeller(klein, 5)                       # genau fuenf Holzfaeller
_zwoelf = _mehr_holzfaeller(gross, 12)                     # zwoelf Holzfaeller
check("2 das kleine Dorf hat fuenf Holzfaeller", _fuenf == 5, str(_fuenf))
check("2 das grosse Dorf hat zwoelf Holzfaeller", _zwoelf == 12, str(_zwoelf))
e_klein = M.bot_dorf_ertrag(klein)
e_gross = M.bot_dorf_ertrag(gross)
check("2 dieselbe Karte, verschiedene Anlagen: die Erntetraege unterscheiden sich",
      e_klein.get("holz") != e_gross.get("holz"), "%s / %s" % (e_klein, e_gross))
check("2 zwoelf Holzfaeller ernten mehr Holz als fuenf",
      float(e_gross.get("holz", 0)) > float(e_klein.get("holz", 0)),
      "%s / %s" % (e_gross.get("holz"), e_klein.get("holz")))
# Sieben Holzfaeller mehr, jeder 4 Holz auf Wald = 28 Holz je Stunde Unterschied.
check("2 der Unterschied ist die Anlagenzahl mal Gelaeendeertrag (7 x 4 = 28)",
      abs((float(e_gross.get("holz", 0)) - float(e_klein.get("holz", 0))) - 28.0) < 1e-6,
      str(float(e_gross.get("holz", 0)) - float(e_klein.get("holz", 0))))

# ==========================================================================
abschnitt("3. Doerfer ohne Anlagen: Rueckfall, kein Absturz")
# ==========================================================================
alt = M.BotDorf(name="Alter Stand", karte=KARTE)           # alter Spielstand: Karte, aber nichts gebaut
ohne_bauten = M.bot_dorf_ertrag(alt)
profil = M.bot_kartenprofil(KARTE)                         # das Kartenprofil
teiler = float(EINST.get("karten_teiler") or 10.0)
check("3 ein Dorf ohne Anlagen rechnet aus dem Kartenprofil (Vorschau als Rueckfall)",
      {k: round(float(v), 2) for k, v in ohne_bauten.items()}
      == {k: round(float(v) / teiler, 2) for k, v in profil.items() if float(v) > 0},
      str(ohne_bauten))
leer = M.BotDorf(name="Ohne alles")                        # voelliger Altstand: keine Karte, nichts gebaut
try:
    rueckfall = M.bot_dorf_ertrag(leer)
    fehler = ""
except Exception as e:                                     # noqa: BLE001 - Absturz waere der Befund
    rueckfall, fehler = None, repr(e)
check("3 ein voelliger Altstand stuerzt nicht ab und rechnet den Bauplan-Rueckfall",
      bool(rueckfall) and float(rueckfall.get("holz", 0)) > 0, "%s %s" % (rueckfall, fehler))
nur_lager = M.BotDorf(name="Nur Dorfzentrum", karte=KARTE)
nur_lager.bauten = {"0": "lager"}                          # ein Gebaeude ohne Ernte
nur_lager.stufen = {"0": 1}
wert_lager = M.bot_dorf_ertrag(nur_lager)
check("3 ein Dorf mit einer ertragslosen Anlage erntet nur das Grundeinkommen (1 Holz, 1 Stein)",
      abs(float(wert_lager.get("holz", 0)) - 1.0) < 1e-6
      and abs(float(wert_lager.get("stein", 0)) - 1.0) < 1e-6,
      str(wert_lager))

# ==========================================================================
abschnitt("4. Das Kartenprofil ist VORSCHAU, nicht Ertrag")
# ==========================================================================
vorschau = {s: round(float(w) / teiler, 2) for s, w in M.bot_kartenprofil(KARTE).items() if w > 0}
check("4 Vorschau und Ertrag sind NICHT dieselbe Zahl",
      vorschau != M.bot_dorf_ertrag(dorf), "%s / %s" % (vorschau, M.bot_dorf_ertrag(dorf)))
check("4 die Vorschau steht weiter in der Kartenuebersicht (Anzeige bleibt bedienbar)",
      bool((M.bot_karten_uebersicht(KARTE) or {}).get("ertrag_pro_stunde")), "")

# ==========================================================================
abschnitt("5. REGRESSION: ein vorhandener Karren kostet kein Holz mehr")
# ==========================================================================
bot = M.BotPlayer(name="Probe", faction="menschlich", aggression=0.5, trading=0.5,
                  settlements=["K1"], forschungsstaende={"Wagenbau": 1})
karren_dorf = M.BotDorf(name="Mit Karren", karte=KARTE)
M.bot_doerfer_bebauen(karren_dorf, EINST)
karren_dorf.einheiten = {"Siedlerkarren": 1}               # der Karren steht schon
karren_dorf.vorraete = {"holz": 1000.0, "metall": 500.0, "leder": 500.0,
                        "wolle": 500.0, "pferde": 50.0, "nahrung": 1000.0}
vorher = dict(karren_dorf.vorraete)
gebaut = None                                              # Ergebnis der Methode
try:                                                       # Methode ohne Spielstand aufrufen
    gebaut = M.GameState.bot_karren_bauen(_stand(), bot, karren_dorf)
    fehler = ""
except Exception as e:                                     # noqa: BLE001
    gebaut, fehler = None, repr(e)
check("5 ein zweiter Karren wird abgelehnt", gebaut is False, "%s %s" % (gebaut, fehler))
check("5 dabei wird KEIN Holz abgebucht (der alte Buchungsfehler)",
      karren_dorf.vorraete == vorher, "%s / %s" % (vorher, karren_dorf.vorraete))
ohne_karren = M.BotDorf(name="Ohne Karren", karte=KARTE)
M.bot_doerfer_bebauen(ohne_karren, EINST)
ohne_karren.vorraete = dict(vorher)
M.GameState.bot_karren_bauen(_stand(), bot, ohne_karren)
check("5 ohne Karren wird einer gebaut und bezahlt",
      int((ohne_karren.einheiten or {}).get("Siedlerkarren", 0)) == 1
      and float(ohne_karren.vorraete.get("holz", 0)) < float(vorher["holz"]),
      str(ohne_karren.vorraete))

# ==========================================================================
abschnitt("6. REGRESSION: Ausgangsdorf einer Gruendung braucht einen Karren")
# ==========================================================================
check("6 die Karrenpflicht ist eingeschaltet", bool(M.bot_gruendung_einstellungen()
                                                    .get("siedlerkarren_pflicht")), "")
check("6 die Quelle wird nur unter Doerfern MIT Karren gesucht",
      "karren_pflicht and int((getattr(dorf, \"einheiten\"" in TEXT_MAIN, "")
check("6 der Karren wird VOR der Buchung geprueft (kein Holzschwund)",
      TEXT_MAIN.index("if int(einheiten.get(\"Siedlerkarren\", 0) or 0) >= 1:")
      < TEXT_MAIN.index("vorraete[str(stoff)] = round(max(0.0"), "")

# ==========================================================================
abschnitt("7. Quellwache: EINE Rechnung fuer Spieler und Bot (F-04)")
# ==========================================================================
import inspect  # noqa: E402
import textwrap  # noqa: E402
import ast  # noqa: E402


def _code(fn) -> str:
    """Quelltext einer Funktion ohne Docstring (Kommentare zaehlen nicht als Code)."""
    baum = ast.parse(textwrap.dedent(inspect.getsource(fn)))   # Funktion parsen
    baum.body[0].body = [k for k in baum.body[0].body            # Docstring abschneiden
                         if not (isinstance(k, ast.Expr) and isinstance(k.value, ast.Constant)
                                 and isinstance(k.value.value, str))]
    return ast.unparse(baum)


quelltext = _code(M.bot_dorf_ertrag)
check("7 bot_dorf_ertrag rechnet ueber wirtschaft.ertrag_gesamt", "wirtschaft.ertrag_gesamt" in quelltext, "")
check("7 es gibt keinen zweiten Ertragsweg ueber eine getippte Zahl",
      "Grundertrag" not in quelltext, "")
check("7 der Rueckfall auf das Kartenprofil ist ausdruecklich kommentiert",
      "Rueckfall Kartenprofil" in inspect.getsource(M.bot_dorf_ertrag), "")

sys.exit(bericht())
