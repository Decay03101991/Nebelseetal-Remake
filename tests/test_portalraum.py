"""Pruefung des Portal-/Limbus-Raums (src/portalraum.py, Paket W5-2).

Deckt ab: 20 Dimensionen mit je 20x20 = 400 Feldern, Koordinaten (X, Y, Z)
samt Randwerten, den SPIELWERT des Weltensprungs 500 Mana plus 100 Gold (C1, Register 664)
NEBEN dem belegten Originalwert 5.000 Mana aus einer Siedlung,
das Ende der 24-Stunden-Sperre (F-28 = C, S-5), die Portalanzeige mit 400 Feldern
und Bannerfarben
sowie die sechs belegten Weltnamen als Dimensionen.
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['portalraum', 'welt']
PRUEF_DATEN = ['welten.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import inspect
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

ROOT, SRC = import_src()
import portalraum as P
import welt as W

SECHS = ["Armageddon", "Ragnaroek", "Utgard", "Midgard", "Valhalla", "Limbus"]
DIM = P.dimensionen()
NAMEN = {d["name"] for d in DIM}

# ---------------------------------------------------------------------------
# ENTSCHEIDUNG GEAENDERT (W-6, Daniel 04.11.2026): das Remake fuehrt SECHS Welten; die 14
# leeren Platzhalter-Dimensionen sind aus data/welten.json entfernt. Vorher stand hier 20.
abschnitt("Limbus und die sechs Weltkarten")

check("dim_zahl() liefert genau 6", P.dim_zahl() == 6, str(P.dim_zahl()))
check("dimensionen() liefert genau 6 Eintraege", len(DIM) == 6, str(len(DIM)))
check("dimensionen() gibt eine Liste zurueck", isinstance(DIM, list))
check("jede Dimension hat kennung und name",
      all({"kennung", "name"} <= set(d) for d in DIM))
check("alle Kennungen sind verschieden",
      len({d["kennung"] for d in DIM}) == len(DIM))
check("die sechs belegten Weltnamen sind Dimensionen",
      all(name in NAMEN for name in SECHS),
      f"fehlt: {[n for n in SECHS if n not in NAMEN]}")
check("jeder der sechs Weltnamen liegt in genau einer Dimension",
      all(sum(1 for d in DIM if d.get("welt") == n) == 1 for n in SECHS))
check("welten() nennt genau sechs Dimensionen mit belegter Welt",
      len(W.welten()) == 6, str(len(W.welten())))

# ---------------------------------------------------------------------------
abschnitt("Raster: 20 x 20 = 400 Felder je Dimension")

check("feld_zahl() liefert genau 400", P.feld_zahl() == 400, str(P.feld_zahl()))
check("20 mal 20 ergibt 400", P.dim_zahl() is not None and 20 * 20 == P.feld_zahl())

_gueltige = sum(1 for x in range(20) for y in range(20) if P.ist_gueltig(x, y, 0))
check("in Dimension 0 sind genau 400 Felder gueltig", _gueltige == 400, str(_gueltige))

check("jede der sechs Weltkarten hat 400 Felder",
      all(len(P.anzeige_raster(z)) == 400 for z in range(P.dim_zahl())))

# ---------------------------------------------------------------------------
abschnitt("Koordinaten (X, Y, Z): gueltig und ungueltig")

check("koordinate(0, 0, 0) ist gueltig", P.koordinate(0, 0, 0) is not None)
check("koordinate(19, 19, 0) ist gueltig", P.koordinate(19, 19, 0) is not None)
check("x = -1 ist ungueltig", P.koordinate(-1, 0, 0) is None)
check("x = 20 ist ungueltig", P.koordinate(20, 0, 0) is None)
check("y = -1 ist ungueltig", P.koordinate(0, -1, 0) is None)
check("y = 20 ist ungueltig", P.koordinate(0, 20, 0) is None)
check("z = -1 ist ungueltig", P.koordinate(0, 0, -1) is None)
check("z = 20 ist ungueltig", P.koordinate(0, 0, 20) is None)
check("z = 0 ist gueltig", P.koordinate(0, 0, 0) is not None)
# Grenzen der Zaehlweise (W-6): 0 und 5 sind gueltig, 6 ist die erste ungueltige Weltkarte.
check("z = 5 ist gueltig", P.koordinate(0, 0, 5) is not None)
check("alle vier Ecken sind gueltig",
      all(P.koordinate(x, y, 4) is not None for x in (0, 19) for y in (0, 19)))
check("ist_gueltig(0, 0, 0) ist True", P.ist_gueltig(0, 0, 0) is True)
check("ist_gueltig(-1, 0, 0) ist False", P.ist_gueltig(-1, 0, 0) is False)
check("ist_gueltig(20, 20, 0) ist False", P.ist_gueltig(20, 20, 0) is False)
check("ist_gueltig stimmt an den Raendern mit koordinate ueberein",
      all(P.ist_gueltig(x, y, 0) == (P.koordinate(x, y, 0) is not None)
          for x in (-1, 0, 19, 20) for y in (-1, 0, 19, 20)))
check("koordinate gibt x, y und z unveraendert zurueck",
      (lambda k: k["x"] == 7 and k["y"] == 13 and k["z"] == 3)(P.koordinate(7, 13, 3)))
check("koordinate nennt die Dimensionskennung",
      P.koordinate(0, 0, 0)["dimension"] == DIM[0]["kennung"])
check("koordinate nennt die Dimension als Name",
      P.koordinate(0, 0, 0)["name"] == DIM[0]["name"])
check("koordinate traegt den belegten Weltnamen",
      P.koordinate(0, 0, 0)["welt"] == "Armageddon")
# ENTSCHEIDUNG GEAENDERT (W-6): es gibt keine freie Dimension mehr. Die alte Wache las den
# Weltnamen von Index 6 (damals d07, leer); heute ist Index 6 hinter der letzten Weltkarte.
check("Index 6 ist keine Weltkarte mehr (W-6)", P.koordinate(0, 0, 6) is None,
      str(P.koordinate(0, 0, 6)))
check("unbekannte Dimension hat kein Feld", P.koordinate(0, 0, 99) is None)

# ---------------------------------------------------------------------------
# ENTSCHEIDUNG GEAENDERT (C1, 18.11.2026, Register 664): der Weltensprung kostet im SPIEL
# 500 Mana plus 100 Gold (Register 93, Daniel 01.11.2026). Bis hierher prueften diese Wachen
# 5.000 Mana. Die 5.000 bleiben als BELEGTER Originalwert stehen und werden weiter geprueft -
# aber in `data/welten.json` und ueber `wechselkosten_belegt()`, nicht als Spielpreis.
abschnitt("Koordinatenwechsel: Spielwert 500 Mana + 100 Gold (C1), Beleg 5.000 bleibt")

check("ein Wechsel kostet im Spiel genau 500 Mana", P.wechselkosten() == 500,
      str(P.wechselkosten()))
check("ein Wechsel kostet im Spiel genau 100 Gold", P.wechselkosten_gold() == 100,
      str(P.wechselkosten_gold()))
check("der BELEGTE Originalwert 5000 bleibt lesbar", P.wechselkosten_belegt() == 5000,
      str(P.wechselkosten_belegt()))
check("der belegte Wert steht weiter in data/welten.json (keine Loeschung)",
      int(W._DATEI["belegte_regeln"]["koordinatenwechsel"]["kosten_mana"]) == 5000,
      str(W._DATEI["belegte_regeln"]["koordinatenwechsel"].get("kosten_mana")))
check("der Spielwert steht als eigener Block daneben",
      int(W._DATEI["belegte_regeln"]["koordinatenwechsel"]["spielwert"]["kosten_mana"]) == 500
      and int(W._DATEI["belegte_regeln"]["koordinatenwechsel"]["spielwert"]["kosten_gold"]) == 100,
      str(W._DATEI["belegte_regeln"]["koordinatenwechsel"].get("spielwert")))
check("genau 500 Mana und 100 Gold reichen", P.wechsel_erlaubt(0, 1, 500, 100)[0] is True)
check("mehr als der Spielpreis ist erlaubt", P.wechsel_erlaubt(0, 1, 9999, 9999)[0] is True)
_ab, _grund = P.wechsel_erlaubt(0, 1, 499, 1000)
check("zu wenig Mana wird abgelehnt", _ab is False)
check("die Ablehnung nennt Mana als Grund", "Mana" in _grund, _grund)
check("die Ablehnung nennt den fehlenden Betrag", "500" in _grund, _grund)
_ab_gold, _grund_gold = P.wechsel_erlaubt(0, 1, 1000, 99)
check("ohne genug Gold wird abgelehnt (C1)", _ab_gold is False)
check("die Gold-Ablehnung nennt Gold und den Betrag",
      "Gold" in _grund_gold and "100" in _grund_gold, _grund_gold)

# ---------------------------------------------------------------------------
# S-5 (09.11.2026, Register 332): Daniel hat F-28 = C entschieden - KEINE Wartezeit mehr.
# Die frueheren Wachen forderten die belegte 24-Stunden-Sperre; sie sind umgedreht, nicht
# geloescht: derselbe Aufruf mit demselben alten Zeitstempel muss jetzt ERLAUBT sein.
abschnitt("Koordinatenwechsel: KEINE Wartezeit mehr (F-28 = C, S-5)")

LETZT = 100000.0
_werte = list(inspect.signature(P.wechsel_erlaubt).parameters)
# C1 (18.11.2026, Register 664): der Goldanteil ist ein PFLICHTWERT, damit ihn kein Aufrufer
# stillschweigend weglassen kann. Aus drei Werten wurden vier.
check("der Aufruf nimmt vier Werte (kein Zeitstempel, aber Gold ist Pflicht)",
      _werte == ["von_z", "nach_z", "mana", "gold"], str(_werte))
try:                                                  # ein Altaufruf OHNE Gold MUSS brechen
    P.wechsel_erlaubt(0, 1, 500.0)
except TypeError:
    check("ein Altaufruf ohne Gold ist ein Fehler, kein stilles Ignorieren", True)
except Exception as _f:
    check("ein Altaufruf ohne Gold ist ein Fehler, kein stilles Ignorieren", False, repr(_f))
else:
    check("ein Altaufruf ohne Gold ist ein Fehler, kein stilles Ignorieren", False,
          "der Aufruf ohne Gold wurde angenommen")
check("ein Wechsel kurz nach dem letzten ist erlaubt", P.wechsel_erlaubt(0, 1, 500, 1000)[0] is True)
check("die Entscheidung steht im Docstring (F-28 = C)",
      "F-28 = C" in (P.wechsel_erlaubt.__doc__ or ""), (P.wechsel_erlaubt.__doc__ or "")[:80])
check("die alte Sperrkonstante liest das Modul nicht mehr",
      not hasattr(P, "_STUNDEN_SPERRE"), "STUNDEN_SPERRE existiert wieder")
check("die Beschreibung nennt keine Wartezeit mehr",
      "keine Wartezeit" in P.beschreibung() and "24 Stunden" not in P.beschreibung(),
      P.beschreibung())
check("unbekannte Ausgangs-Dimension wird abgelehnt",
      P.wechsel_erlaubt(-1, 1, 500, 1000)[0] is False)
# W-6: 6 ist jetzt die erste unbekannte Zielwelt (vorher war 20 die erste hinter 0..19).
check("unbekannte Ziel-Dimension wird abgelehnt",
      P.wechsel_erlaubt(0, 6, 500, 1000)[0] is False)
check("Wechsel in dieselbe Dimension ist nicht verboten (Quelle schweigt)",
      P.wechsel_erlaubt(0, 0, 500, 1000)[0] is True)

# ---------------------------------------------------------------------------
abschnitt("Abbuchung: Mana UND Gold werden genau einmal abgezogen (C1)")

_d = P.nach_wechsel(10000.0, 1000.0, LETZT)
check("nach_wechsel zieht genau 500 Mana ab", _d["mana"] == 9500.0, str(_d["mana"]))
check("nach_wechsel zieht genau 100 Gold ab", _d["gold"] == 900.0, str(_d["gold"]))
check("die Mana-Differenz betraegt genau einen Manapreis",
      10000.0 - _d["mana"] == P.wechselkosten())
check("die Gold-Differenz betraegt genau einen Goldpreis",
      1000.0 - _d["gold"] == P.wechselkosten_gold())
check("nach_wechsel schreibt den Zeitstempel des Wechsels (Aufzeichnung, sperrt nicht)",
      _d["letzter_wechsel"] == LETZT)
check("nach_wechsel meldet die abgezogenen Kosten (Mana und Gold)",
      _d["kosten"] == P.wechselkosten() and _d["kosten_gold"] == P.wechselkosten_gold())
check("eine zweite Abbuchung zieht erneut genau einmal ab",
      P.nach_wechsel(_d["mana"], _d["gold"], LETZT)["mana"] == 9000.0)


def _zu_wenig():
    """True, wenn nach_wechsel bei zu wenig Mana ValueError wirft (ohne Abbuchung)."""
    try:
        P.nach_wechsel(499.0, 1000.0, LETZT)
    except ValueError:
        return True
    except Exception:
        return False
    return False


def _zu_wenig_gold():
    """True, wenn nach_wechsel bei zu wenig GOLD ValueError wirft (C1, ohne Abbuchung)."""
    try:
        P.nach_wechsel(10000.0, 99.0, LETZT)
    except ValueError:
        return True
    except Exception:
        return False
    return False


check("nach_wechsel verweigert bei zu wenig Mana (ValueError)", _zu_wenig() is True)
check("nach_wechsel verweigert bei zu wenig Gold (ValueError)", _zu_wenig_gold() is True)

# ---------------------------------------------------------------------------
abschnitt("Portalanzeige: 400 Felder, gruen fuer eigen, rot fuer fremd")

_raster = P.anzeige_raster(0)
check("die Portalanzeige hat 400 Felder", len(_raster) == 400, str(len(_raster)))
check("die Anzeige ist 20 breit und 20 hoch",
      len({f["x"] for f in _raster}) == 20 and len({f["y"] for f in _raster}) == 20)
check("alle Felder liegen in x = 0..19 und y = 0..19",
      all(0 <= f["x"] < 20 and 0 <= f["y"] < 20 for f in _raster))
check("kein Feld kommt doppelt vor",
      len({(f["x"], f["y"]) for f in _raster}) == 400)
check("portalfarbe der eigenen Dimension ist gruen", P.portalfarbe(3, [3]) == "gruen")
check("portalfarbe einer fremden Dimension ist rot", P.portalfarbe(3, []) == "rot")
_eigen = P.anzeige_raster(3, eigene_dimensionen=[3])
check("eigene Dimension faerbt alle Felder gruen",
      all(f["farbe"] == "gruen" for f in _eigen))
check("eigene Felder tragen das Flag eigen",
      all(f["eigen"] is True and f["status"] == "eigen" for f in _eigen))
_fremd = P.anzeige_raster(3)
check("fremde Dimension faerbt alle Felder rot",
      all(f["farbe"] == "rot" for f in _fremd))
check("fremde Felder tragen das Flag fremd",
      all(f["eigen"] is False and f["status"] == "fremd" for f in _fremd))
check("ein kleinerer Radius zeigt weniger Felder",
      len(P.anzeige_raster(0, radius=5)) == 100,
      str(len(P.anzeige_raster(0, radius=5))))

# ---------------------------------------------------------------------------
abschnitt("Beschreibung")

_b = P.beschreibung()
# W-6: sechs Weltkarten statt 20 Dimensionen.
check("die Beschreibung nennt 6 Weltkarten", "6 Weltkarten" in _b, _b)
# Vorher "20 Dimensionen". SCHNITT S-2, Daniel 01.11.2026: das Wort Dimensionen verschwindet aus
# der Anzeige, es heisst Weltkarten und Weltensprung (Anhang 3, Fragen 19 und 35). Der Zusatz
# "Dimension" im Satz waere ein Rueckfall - deshalb zusaetzlich die Gegenprobe.
check("die Beschreibung nennt keine Dimension mehr", "Dimension" not in _b, _b)
check("die Beschreibung nennt 400 Felder", "400" in _b, _b)
# C1 (18.11.2026, Register 664): die Beschreibung nennt die SPIELPREISE, nicht mehr den Belegwert.
check("die Beschreibung nennt 500 Mana", "500 Mana" in _b, _b)
check("die Beschreibung nennt 100 Gold", "100 Gold" in _b, _b)
check("die Beschreibung nennt NICHT mehr die 5.000 als Spielpreis", "5.000 Mana" not in _b, _b)
# S-5 (09.11.2026, Register 332): die 24 Stunden sind auf Daniels Entscheid F-28 = C entfallen.
check("die Beschreibung nennt KEINE 24 Stunden mehr", "24 Stunden" not in _b, _b)
check("die Beschreibung nennt die Entscheidung", "keine Wartezeit" in _b, _b)
check("die Beschreibung ist eine nicht leere Zeile",
      isinstance(_b, str) and len(_b) > 20)

sys.exit(bericht())
