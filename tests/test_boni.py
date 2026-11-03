# -*- coding: ascii -*-
"""Volks- und Taktikboni als WIRKUNG (V-5, Entscheidungen Daniel 03.11.2026).

Daniels Entscheidungen aus der Fragenrunde V-5:
  1. Ueberschneidung ADDITIV - 5 % + 5 % = glatt +10 % (nicht 10,25 %).
  2. Hoehe bleibt 5 % (Er traege sind Fliesskomma, AT/PA sind Ganzzahlen).
  3. Taktikbonus gilt, solange die Taktik steht; nach einem Taktikwechsel 48 h gesperrt.
  4. Der Spieler bekommt DIESELBEN Volksboni wie ein Bot.
  5. Gnome: "Ausbau +5 %" bleibt, wirkt aber als -5 % Gebaeudepreise beim Ausbau; bei den Bots
     wirkungslos, weil Bots nicht bauen.

Was diese Datei beweist
-----------------------
1. Die ZAHLEN stehen in `data/boni.json`, die ANZEIGETEXTE in `data/voelker.json` - und beide
   tragen dieselben Voelker und dieselben Prozentsaetze (sie koennen nicht auseinanderlaufen).
2. Die Ueberschneidung ist additiv: Silra (Volk elfisch +5 %, Taktik +5 %) ergibt +10 %.
3. Der Schalter `aktiv` in der Datei schaltet die Wirkung ab, ohne Code zu aendern.
4. Der Bot-Ertrag traegt das Volk: menschlich 12,6 Holz / 11,4 Stein je Stunde statt 12/12.
5. Der Spieler-Ertrag traegt es ebenfalls, und Kern (`ertrag_gesamt`) und Anzeige
   (`dorf_uebersicht`) rechnen DASSELBE (eine Wahrheit je Groesse, F-04).
6. Gegenprobe: mit `aktiv: false` kommt genau der alte Wert - die Wirkung kommt aus der Datei.

Aufruf:  python -X utf8 tests/test_boni.py
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

ROOT, SRC = import_src()
import boni as B  # noqa: E402
import bottaktik as BT  # noqa: E402
import main as M  # noqa: E402
import wirtschaft as W  # noqa: E402

DATEN = os.path.join(ROOT, "data", "boni.json")
VOELKER = os.path.join(ROOT, "data", "voelker.json")


def _datei(pfad):
    with open(pfad, encoding="utf-8") as f:
        return json.load(f)


def _prozent_aus_text(text: str):
    """"Holzertrag +5 %" -> ("holz", 5.0); "PA der Einheiten -5 %" -> ("pa", -5.0).

    Nur fuer die Wache: sie liest die ANZEIGE und vergleicht sie mit der ZAHL. Dadurch faellt auf,
    wenn ein Text und eine Zahl auseinanderlaufen.
    """
    text = str(text or "")
    teil = text.split()
    if not teil:
        return "", 0.0
    try:
        zahl = float(teil[-2].replace("+", "").replace("%", ""))
    except (IndexError, ValueError):
        return "", 0.0
    begriff = " ".join(teil[:-2]).strip().lower()
    tabelle = {"holzertrag": "ertrag_holz", "steinertrag": "ertrag_stein",
               "nahrungsertrag": "ertrag_nahrung", "goldertrag": "ertrag_gold",
               "reisegeschwindigkeit": "reise", "at der einheiten": "at",
               "pa der einheiten": "pa", "handelserloes": "handel", "ausbau": "baukosten",
               "beute": "beute", "verteidigung": "verteidigung"}
    return tabelle.get(begriff, ""), zahl


# ==========================================================================
# 1. Die Datendatei und ihre eine Wahrheit
# ==========================================================================
abschnitt("1. Datendatei, Voelker und Texte passen zusammen")
daten = _datei(DATEN)
voelker = _datei(VOELKER)
check("boni.json ist da und eingeschaltet", bool(daten) and daten.get("aktiv") is True,
      f"aktiv={daten.get('aktiv')}")
check("Ueberschneidung ist additiv (Daniel 03.11.2026)", B.ueberschneidung() == "additiv",
      B.ueberschneidung())
check("Sperrzeit steht als Zahl in der Datei (48 h)", abs(B.sperrzeit_sekunden() - 48 * 3600) < 1,
      f"{B.sperrzeit_sekunden() / 3600:g} h")

_namen_datei = sorted(str(e["kennung"]) for e in voelker.get("fraktionen") or [])
_namen_boni = sorted(str(k) for k in (daten.get("voelker") or {}))
check("dieselben sechs Voelker in beiden Dateien", _namen_datei == _namen_boni,
      f"{_namen_boni}")

for eintrag in voelker.get("fraktionen") or []:
    kennung = str(eintrag["kennung"])
    werte = B.volk_werte(kennung)
    check(f"{kennung}: zwei Wirkungen (Plus und Minus)", len(werte) == 2, f"{werte}")
    # Die Zahl muss zum Text passen - Richtung und Hoehe. EINE Ausnahme, und nur eine: Daniels
    # Entscheidung 03.11.2026 liest "Ausbau +5 %" bei den Gnomen als 5 % GUENSTIGEREN Ausbau,
    # deshalb steht dort -5 auf "baukosten". Die Umkehr steht hier als Ausnahme, nicht als Regel.
    _umkehr = {("Gnome", "plus"): -1}
    for feld in ("plus", "minus"):
        groesse_text, zahl_text = _prozent_aus_text(eintrag.get(feld))
        if not groesse_text:
            check(f"{kennung}/{feld}: Begriff erkannt", False, str(eintrag.get(feld)))
            continue
        zahl_text = zahl_text * _umkehr.get((kennung, feld), 1)
        groesse_zahl = str(groesse_text)
        check(f"{kennung}/{feld}: Zahl steht in boni.json ({groesse_zahl} {zahl_text:+g})",
              abs(float(werte.get(groesse_zahl, 0.0)) - zahl_text) < 1e-9,
              f"Text {eintrag.get(feld)!r} -> {werte.get(groesse_zahl)}")

# ==========================================================================
# 2. Die Rechnung: additiv, Grenzfaelle
# ==========================================================================
abschnitt("2. Additive Ueberschneidung und Faktorumrechnung")
check("faktor(5) == 1,05", abs(B.faktor(5) - 1.05) < 1e-9)
check("faktor(-5) == 0,95", abs(B.faktor(-5) - 0.95) < 1e-9)
check("faktor(0) == 1,0", abs(B.faktor(0) - 1.0) < 1e-9)
check("faktor(-100) bleibt >= 0 (kein negativer Ertrag)", B.faktor(-200) == 0.0, str(B.faktor(-200)))
check("faktor(unsinn) == 1,0 (kein Erfinden)", B.faktor("abc") == 1.0)

_silra = BT.modifikatoren({"name": "Silra", "fraktion": "elfisch"}, 0.0)
check("Silra: Reise +10 % (5 Volk + 5 Taktik, ADDITIV)", abs(_silra.get("reise", 0) - 10.0) < 1e-9,
      f"{_silra}")
check("Silra: Reise ist NICHT multiplikativ (10,25 waere falsch)",
      abs(_silra.get("reise", 0) - 10.25) > 1e-9, f"{_silra.get('reise')}")
_krank = BT.modifikatoren({"name": "Krank", "fraktion": "Trolle"}, 0.0)
check("Krank: AT +10 % (5 Volk + 5 Taktik, ADDITIV)", abs(_krank.get("at", 0) - 10.0) < 1e-9,
      f"{_krank}")
_haug = BT.modifikatoren({"name": "Haug", "fraktion": "menschlich"}, 0.0)
check("Haug: Beute +5 % (nur Taktik) und Holz +5 % (nur Volk)",
      abs(_haug.get("beute", 0) - 5.0) < 1e-9 and abs(_haug.get("ertrag_holz", 0) - 5.0) < 1e-9,
      f"{_haug}")
_grom = BT.modifikatoren({"name": "Grom", "fraktion": "zwergisch"}, 0.0)
check("Grom: 'Ausbau +5 %' wird gefuehrt, hat aber keinen Anker",
      abs(_grom.get("ausbau", 0) - 5.0) < 1e-9 and B.groessen().get("ausbau", {}).get("art") == "ohne_anker",
      f"{_grom}")
check("unbekanntes Volk und unbekannter Bot ergeben nichts",
      BT.modifikatoren({"name": "Niemand", "fraktion": "unbekannt"}, 0.0) == {})

# Sperrzeit: ein abgelaufener Bonus schaltet den Taktikanteil ab, ein fehlender gilt als stehend.
check("ohne verhaltensbonus gilt die Taktik als stehend",
      BT.taktik_bonus_aktiv({"name": "Silra"}, 1000.0) is True)
check("abgelaufener verhaltensbonus schaltet den Taktikanteil ab",
      BT.taktik_bonus_aktiv({"name": "Silra", "verhaltensbonus": {"bis": 500.0}}, 1000.0) is False)
check("laufender verhaltensbonus zaehlt",
      BT.taktik_bonus_aktiv({"name": "Silra", "verhaltensbonus": {"bis": 2000.0}}, 1000.0) is True)
_ohne = BT.modifikatoren({"name": "Silra", "fraktion": "elfisch",
                          "verhaltensbonus": {"bis": 500.0}}, 1000.0)
check("abgelaufen: nur noch das Volk (+5 %, nicht +10)", abs(_ohne.get("reise", 0) - 5.0) < 1e-9,
      f"{_ohne}")

# ==========================================================================
# 3. Bot-Ertrag traegt das Volk
# ==========================================================================
abschnitt("3. Bot-Ertrag (main.bot_dorf_ertrag)")
_dorf = M.BotDorf(name="Hof")
_ohne_bot = M.bot_dorf_ertrag(_dorf)
# S-6b (03.11.2026): die drei Rinderfarmen (Bauplan fuer den Siedlerkarren) erzeugen zusaetzlich
# Nahrung - der Rueckfall-Ertrag ist 12 Holz / 12 Stein / 21 Nahrung / 9 Gold plus die Waren.
# S-6b (03.11.2026): nur die vier Grundrohstoffe vergleichen - die Bot-Doerfer ernten zusaetzlich
# Leder, Wolle und Pferde (das prueft tests/test_bot_warenkette.py), und die drei Rinderfarmen
# erzeugen 9 Nahrung mit, also 21 statt 12.
_grund = {k: v for k, v in _ohne_bot.items() if k in ("holz", "stein", "nahrung", "gold")}
# S-6b (03.11.2026): Holz steht seit Daniels Entscheidung auf FUENF Anlagen je Dorf statt drei
# (680 Holz fuer Karren und Gruendung) - der Rueckfall-Ertrag ist 20/12/21/9 statt 12/12/21/9.
check("ohne Bot bleibt der alte Grundertrag (20/12/21/9)",
      _grund == {"holz": 20.0, "stein": 12.0, "nahrung": 21.0, "gold": 9.0}, f"{_grund}")
# Holz 20 mal Volksfaktor: menschlich 1,05 = 21,0 / zwergisch 0,95 = 19,0; Stein bleibt 12.
_erwartet = {"menschlich": (21.0, 11.4), "zwergisch": (19.0, 12.6)}
for fraktion, (holz, stein) in _erwartet.items():
    bot = M.BotPlayer(name="X", faction=fraktion, aggression=0.5, trading=0.5)
    werte = M.bot_dorf_ertrag(_dorf, None, bot)
    check(f"{fraktion}: Holz {holz} / Stein {stein}",
          abs(werte.get("holz", 0) - holz) < 1e-9 and abs(werte.get("stein", 0) - stein) < 1e-9,
          f"{werte}")
_g = M.BotPlayer(name="X", faction="Ghule", aggression=0.5, trading=0.5)
check("Ghule: Nahrung 22,05 (21 mal 1,05)",
      abs(M.bot_dorf_ertrag(_dorf, None, _g).get("nahrung", 0) - 22.05) < 1e-9)
_n = M.BotPlayer(name="X", faction="Gnome", aggression=0.5, trading=0.5)
check("Gnome: kein Ertragsbonus (Ausbau wirkt beim Bauen, nicht beim Ernten)",
      M.bot_dorf_ertrag(_dorf, None, _n) == _ohne_bot, f"{M.bot_dorf_ertrag(_dorf, None, _n)}")
# Der Zwischenspeicher darf den Faktor NICHT mitschleppen (zweiter Bot, andere Fraktion).
_m1 = M.bot_dorf_ertrag(_dorf, None, M.BotPlayer(name="A", faction="menschlich",
                                                aggression=0.5, trading=0.5))
_m2 = M.bot_dorf_ertrag(_dorf, None, M.BotPlayer(name="B", faction="Ghule",
                                                aggression=0.5, trading=0.5))
check("Zwischenspeicher traegt den Volksfaktor nicht mit",
      _m1.get("holz") == 21.0 and _m2.get("holz") == 20.0, f"{_m1} / {_m2}")

# ==========================================================================
# 4. Spieler-Ertrag: Kern und Anzeige DASSELBE
# ==========================================================================
abschnitt("4. Spieler-Ertrag (wirtschaft) - eine Wahrheit je Groesse")
_base = {"karte": {"raster": ["wald", "berg", "grasland", "sumpf"]},
         "bauten": {"0": "holzfaeller", "1": "steinmetz", "2": "farm"}}
_ohne_volk = W.siedlung_ertrag(dict(_base))
check("ohne Volk bleibt es bei 4/4/4",
      _ohne_volk.get("Holz") == 4.0 and _ohne_volk.get("Stein") == 4.0, f"{_ohne_volk}")
_mit = W.siedlung_ertrag(dict(_base, volk="menschlich"))
check("menschlich: Holz 4,2 / Stein 3,8",
      abs(_mit.get("Holz", 0) - 4.2) < 1e-9 and abs(_mit.get("Stein", 0) - 3.8) < 1e-9, f"{_mit}")
_gesamt = W.ertrag_gesamt([dict(_base, volk="menschlich")])
_uebersicht = W.dorf_uebersicht(dict(_base, volk="menschlich"))["summe"]["ertrag"]
check("Kern (ertrag_gesamt) und Anzeige (dorf_uebersicht) stimmen ueberein",
      abs(_gesamt.get("Holz", 0) - _uebersicht.get("Holz", 0)) < 1e-9
      and abs(_gesamt.get("Stein", 0) - _uebersicht.get("Stein", 0)) < 1e-9,
      f"{_gesamt} / {_uebersicht}")
check("die Wirkung steht am ORT (Settlement.volk), nicht in einer zweiten Quelle",
      "volk" in M.Settlement.__dataclass_fields__, str(list(M.Settlement.__dataclass_fields__)[:4]))

# ==========================================================================
# 5. Gegenprobe: Schalter aus -> alter Wert
# ==========================================================================
abschnitt("5. Gegenprobe mit abgeschalteter Wirkung")
_aus = dict(daten)
_aus["aktiv"] = False
_pfad = os.path.join(tempfile.mkdtemp(prefix="boni_"), "boni_aus.json")
with open(_pfad, "w", encoding="utf-8") as f:
    json.dump(_aus, f, ensure_ascii=False)
check("aktiv: false -> keine Prozente (Silra)",
      B.modifikatoren("elfisch", "Silra", True, _pfad) == {},
      f"{B.modifikatoren('elfisch', 'Silra', True, _pfad)}")
check("aktiv: false -> Ertragsfaktor 1,0",
      B.ertragsfaktor("menschlich", "Holz", _pfad) == 1.0 and B.faktor(0) == 1.0)
check("aktiv: false -> Reisezeitfaktor 1,0", B.reisezeitfaktor("elfisch", "Silra", True, _pfad) == 1.0)
_aus_werte = B.modifikatoren("menschlich", "", True, _pfad)
check("Gegenprobe haette den ALTEN Ertrag ergeben (12/12 statt 12,6/11,4)",
      _aus_werte == {} and 12.0 * B.faktor(0) == 12.0, f"{_aus_werte}")

# ==========================================================================
# 6. Grenzfaelle der Prozente (-1 / 0 / Soll / +1)
# ==========================================================================
abschnitt("6. Grenzfaelle um den Sollwert")
for prozent, faktor in ((-1, 0.99), (0, 1.0), (5, 1.05), (6, 1.06)):
    check(f"Prozent {prozent:+d} -> Faktor {faktor}", abs(B.faktor(prozent) - faktor) < 1e-9)
check("12 Holz + 5 % == 12,6 (exakt auf zwei Stellen)",
      round(12.0 * B.faktor(5), 2) == 12.6)
check("12 Holz - 5 % == 11,4", round(12.0 * B.faktor(-5), 2) == 11.4)
check("Reisezeit 100 min mit +10 % == 90,91 min (nicht 90,00)",
      round(100.0 * B.reisezeitfaktor("elfisch", "Silra", True), 2) == 90.91)
check("Reisezeit 100 min mit +5 % == 95,24 min",
      round(100.0 * B.reisezeitfaktor("elfisch", "", True), 2) == 95.24)

# ==========================================================================
# 7. Reise: der Bonus verkuerzt die ZEIT (Spieler und Bot)
# ==========================================================================
abschnitt("7. Reisegeschwindigkeit")
import auftraege as A  # noqa: E402
check("ohne Faktor bleibt die Reisezeit wie bisher (100/10 = 72000 s)",
      A.reisezeit_sekunden(100, 10) == 72000.0)
check("Faktor 1/1,10 macht 72000 s zu 65454,55 s",
      round(A.reisezeit_sekunden(100, 10, 1 / 1.10), 2) == 65454.55,
      str(A.reisezeit_sekunden(100, 10, 1 / 1.10)))
check("kaputter Faktor (0) aendert nichts",
      A.reisezeit_sekunden(100, 10, 0) == A.reisezeit_sekunden(100, 10))
check("negative Entfernung bleibt 0, auch mit Faktor", A.reisezeit_sekunden(-5, 10, 0.5) == 0.0)
_silra_bot = {"name": "Silra", "fraktion": "elfisch"}
_silra_zeit = BT._marsch_reisezeit(5, _silra_bot, 0.0)
_haug_zeit = BT._marsch_reisezeit(5, {"name": "Haug", "fraktion": "menschlich"}, 0.0)
check("Silra marschiert schneller als Haug (Volk + Taktik, additiv 10 %)",
      _silra_zeit < _haug_zeit,
      f"Silra {_silra_zeit:.1f} s / Haug {_haug_zeit:.1f} s")
check("Silra ist genau 1/1,10 so lange unterwegs",
      abs(_silra_zeit - _haug_zeit / 1.10) < 1e-6,
      f"{_silra_zeit:.4f} gegen {_haug_zeit / 1.10:.4f}")

# ==========================================================================
# 8. Kampf: AT, PA und Beute
# ==========================================================================
abschnitt("8. Kampf (AT/PA/Beute)")
import random  # noqa: E402
import kampf as K  # noqa: E402


_FUSS = [n for n in sorted(K.PROFILE) if K.PROFILE[n][4] is None]   # Nahkaempfer
_ANG = _FUSS[-1]                                                     # z. B. Kaempfer
# Ein Verteidiger MIT Ruestung, sonst kann PA gar nichts bewirken (Ruestung 0 mal Faktor = 0).
_VER = next(n for n in _FUSS if K.PROFILE[n][3] > 0)


def _schlacht(angreifer=None, verteidiger=None, **kw):
    return K.fuehre_schlacht(angreifer or {_ANG: 5}, verteidiger or {_VER: 5},
                             rng=random.Random(7), **kw)


_ohne = _schlacht()
_leer = _schlacht(boni_angreifer={"at": 0.0, "pa": 0.0}, boni_verteidiger={"at": 0.0, "pa": 0.0})
check("ohne Boni rechnet die Schlacht wie bisher (Bericht gleich)",
      _ohne.get("bericht") == _leer.get("bericht"))
_mit_at = _schlacht(boni_angreifer={"at": 10.0})
check("AT +10 % veraendert den Kampf (Bericht anders, gleicher Zufall)",
      _mit_at.get("bericht") != _ohne.get("bericht"))
check("AT +10 % wirkt nur, wenn es einen Bonus gibt (Gegenprobe: kein Bonus, kein Unterschied)",
      _mit_at.get("bericht") != _leer.get("bericht"))
_mit_pa = _schlacht(boni_verteidiger={"pa": 5.0})
check("PA +5 % beim Verteidiger veraendert den Kampf", _mit_pa.get("bericht") != _ohne.get("bericht"))
_beute_ohne = K._beute({"Handkarren": 2}, {"holz": 1000})
_beute_mit = K._beute({"Handkarren": 2}, {"holz": 1000}, 1.05)
check("Beute +5 % gibt mehr Platz (80 -> 84), die Karren bleiben dieselben",
      sum(_beute_ohne.values()) == 80 and sum(_beute_mit.values()) == 84,
      f"{sum(_beute_ohne.values())} / {sum(_beute_mit.values())}")
check("Beute ohne Faktor unveraendert (Grenzfall 1,0)",
      sum(K._beute({"Handkarren": 1}, {"holz": 1000}, 1.0).values()) == 40)
check("Beute-Faktor 0 ist unschaedlich (kein Absturz, alter Wert)",
      sum(K._beute({"Handkarren": 1}, {"holz": 1000}, 0).values()) == 40)
check("Beute kann die Karrenladung nicht ueberschreiten (Deckel bleibt)",
      sum(K._beute({"Handkarren": 1}, {"holz": 1000}, 1.05).values()) == 42)
_leer_beute = K._beute({"Handkarren": 1}, {})
check("ohne Vorraete gibt es keine Beute", _leer_beute == {})

# ==========================================================================
# 9. Handel: der Erloes haengt am Volk des Verkaeufers
# ==========================================================================
abschnitt("9. Handelserloes (Trolle -5 %)")
import spieloekonomie as SO  # noqa: E402


def _vertrag(volk: str):
    return ({"kaeufer": "K", "verkaeufer": "V", "kaeufer_owner": "spieler",
             "verkaeufer_owner": "spieler", "ankunft": 10.0, "rueckkehr": 20.0,
             "angenommen": False, "abgerechnet": False, "entscheidung": True,
             "sperrgold": 100.0, "sperrgold_import": 0.0, "kanal": "vorraete",
             "ware": "holz", "menge": 10, "einheiten": {}, "verkauft_import": {}},
            {"K": {"besitzer": "spieler", "vorraete": {}, "importiert": {}},
             "V": {"besitzer": "spieler", "vorraete": {}, "importiert": {}, "volk": volk}})


_ohne_volk, _o1 = _vertrag("")
_mit_volk, _o2 = _vertrag("Trolle")
_o1n, _m1 = SO.handel_abschluss(_ohne_volk, _o1, 10.0)
_o2n, _m2 = SO.handel_abschluss(_mit_volk, _o2, 10.0)
check("ohne Volk kommen 100 Gold an", abs(_o1n["V"]["vorraete"].get("gold", 0) - 100.0) < 1e-9,
      str(_o1n["V"]["vorraete"]))
check("Trolle bekommen 95 Gold (-5 %)",
      abs(_o2n["V"]["vorraete"].get("gold", 0) - 95.0) < 1e-9, str(_o2n["V"]["vorraete"]))
check("der Erloes steht auch am Vertrag (eine Zahl fuer Kern und Bericht)",
      abs(float(_m2.get("erloes", 0)) - 95.0) < 1e-9, str(_m2.get("erloes")))
check("der Kaufpreis bleibt unveraendert gesperrt/abgerechnet",
      _m2.get("angenommen") is True and float(_m2.get("sperrgold", -1)) == 0.0)

# ==========================================================================
# 10. Baukosten: Gnome bauen 5 % guenstiger (nur der Spieler, Bots bauen nicht)
# ==========================================================================
abschnitt("10. Ausbaupreis der Gnome")
_G = M.Settlement(name="Gnomendorf", map_id="kontinent")
_G.volk = "Gnome"
_M = M.Settlement(name="Menschendorf", map_id="kontinent")
_M.volk = "menschlich"
_gnom = M._ausbau_kosten("bibliothek", 2, _G)
_mensch = M._ausbau_kosten("bibliothek", 2, _M)
check("ohne Volk kostet der Ausbau wie bisher (24 Holz / 16 Stein)",
      M._ausbau_kosten("bibliothek", 2, M.Settlement(name="X", map_id="kontinent"))
      == {"holz": 24, "stein": 16})
check("Gnome zahlen 23 Holz / 15 Stein statt 24 / 16",
      _gnom == {"holz": 23, "stein": 15}, str(_gnom))
check("andere Voelker zahlen den vollen Preis", _mensch == {"holz": 24, "stein": 16}, str(_mensch))
_klein_base = M.baukosten("bibliothek", 1)
_klein = M._ausbau_kosten("bibliothek", 1, _G)
check("Grenzfall kleine Preise: Stufe 1 wird ebenfalls 5 % guenstiger",
      _klein == {s: max(0, int(round(v * 0.95))) for s, v in _klein_base.items()},
      f"{_klein} aus {_klein_base}")

bericht()
