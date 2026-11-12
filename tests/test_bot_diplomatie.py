"""S4-7: Bot-Luecken - Drache, Spionage, Reaktion (07.11.2026, docs/ABLAUF_LLM_20261106.md Schritt 7).

Geprueft wird, was der Schnitt zusagt:
  A. Die Zahlen stehen in `data/bot_diplomatie.json` (A-7) - und die DRACHEN-Regel steht NICHT
     doppelt hier, sondern weiter in `data/drachen.json` (W-14, F-04).
  B. Die Reaktionsstufe kommt aus der Taktik des Bots (1,0 = Standard fuer Unbekannte).
  C. Der Spieler-Vorsprung macht den Bot vorsichtiger; ohne Vorsprung aendert sich nichts.
  D. Die Reaktionsstufe TEILT die vorhandenen Raubzug-Schwellen - die Eingabe bleibt unveraendert,
     bei `aktiv: false` oder Faktor 1,0 kommt die Datei unveraendert zurueck.
  E. Die Spaehung vor dem Raubzug: GENAU EINE je Ziel (Daniel 02.11.2026: ein Bericht wird nicht
     alt), der Bericht ueberlebt den Takt im Spielstand, und danach greift der Bot an.
  F. Quellwachen: das Drachen-Urteil bleibt `drachen.bot_entscheidung`, die Wall-Vorpruefung der
     Spaehung bleibt `spionage.abwehr_pruefung` - keine zweite Rechnung in `main.py`.
  G. Echter Verlauf in der App: Spaehung im ersten Takt, Angriff im spaeteren - keine Dauerspaehung.
  H. Ein alter Spielstand ohne `aufklaerung` laedt mit leerem dict (additiv).

ASCII-only (Pruefdatei-Konvention).
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['bottaktik', 'diplomatie', 'drachen', 'einheiten', 'kampf', 'main:*', 'spionage', 'welt', 'zeitbasis']
PRUEF_DATEN = ['bot_diplomatie.json', 'diplomatie.json', 'drachen.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import ast
import inspect
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

import_src()
import bottaktik as B
import diplomatie as D
import main
import spionage
import zeitbasis

TAG = float(zeitbasis.SEKUNDEN_JE_TAG)  # ein Spieltag (R3-1: die EINE Quelle, src/zeitbasis.py)
# Der Anzeigetext selbst steht in der Datendatei; hier wird nur nach ihm gesucht. Damit diese
# Pruefdatei ASCII bleibt, entsteht der Umlaut aus seinem Zeichencode.
SPAEHER = "Sp" + chr(0xE4) + "her"  # "Spaeher" mit echtem Umlaut, wie in data/bot_diplomatie.json


def _code(funktion) -> str:
    """Quelltext einer Funktion ohne Docstring (Docstrings zaehlen nicht als Code)."""
    baum = ast.parse(textwrap.dedent(inspect.getsource(funktion)))  # Funktion in einen Baum wandeln
    kopf = baum.body[0]  # der FunctionDef-Knoten
    if kopf.body and isinstance(kopf.body[0], ast.Expr) and isinstance(kopf.body[0].value, ast.Constant):
        kopf.body = kopf.body[1:]  # fuehrenden Docstring abschneiden
    return ast.unparse(baum)  # Rest als Text


def _bot(name="Haug", aufklaerung=None, kundschafter=3, krieger=40):
    """Ein Bot mit einem Dorf und Truppen - so, wie ihn der Kern fuehrt."""
    bot = main.BotPlayer(name=name, faction="menschlich", aggression=0.8, trading=0.5)
    bot.doerfer = [main.BotDorf(name=name + "dorf 1", hauptdorf=True, dimension=1, herkunftswelt=1)]
    bot.doerfer[0].einheiten = {"Krieger": krieger, "Kundschafter": kundschafter}
    bot.doerfer[0].vorraete = {"holz": 500.0, "stein": 500.0, "nahrung": 500.0}
    bot.doerfer[0].wall_stufe = 0
    bot.doerfer[0].wall_zustand = 100.0
    if isinstance(aufklaerung, dict):
        bot.aufklaerung = dict(aufklaerung)
    return bot


# ------------------------------------------------------------------ A. Datendatei
abschnitt("A. Die Zahlen stehen in der Datendatei (A-7), der Drache nicht doppelt (F-04)")
daten = D.botdaten()
check("data/bot_diplomatie.json wird gelesen", bool(daten), str(sorted(daten.keys())))
check("Schalter aktiv ist gesetzt", daten.get("aktiv") is True, str(daten.get("aktiv")))
check("Block spionage vorhanden", isinstance(daten.get("spionage"), dict), str(type(daten.get("spionage"))))
check("Block reaktion vorhanden", isinstance(daten.get("reaktion"), dict), str(type(daten.get("reaktion"))))
def _schluessel(wert, name="schlagkraft_faktor"):
    """Sucht einen Schluessel in einer verschachtelten Struktur - Texte zaehlen nicht mit."""
    if isinstance(wert, dict):
        return any(str(k) == name or _schluessel(v, name) for k, v in wert.items())
    if isinstance(wert, list):
        return any(_schluessel(v, name) for v in wert)
    return False


check("KEINE Drachen-Schwelle als ZAHL in dieser Datei (sie steht in data/drachen.json)",
      not _schluessel(daten), "Drache steht in data/drachen.json")
check("die Drachen-Regel liegt weiter in data/drachen.json",
      float(__import__("drachen").bot_regeln().get("schlagkraft_faktor", 0)) > 0,
      str(__import__("drachen").bot_regeln().get("schlagkraft_faktor")))
_sp = D.bot_spionage_regeln()
check("Spionage-Schalter ist gesetzt", _sp.get("aktiv") is True, str(_sp.get("aktiv")))
check("Anzeigetext fuer die Sichtung kommt aus der Datei",
      "{dorf}" in str(_sp.get("text_gesichtet", "")), str(_sp.get("text_gesichtet"))[:40])
check("Anzeigetext fuer die Abwehr kommt aus der Datei",
      "{dorf}" in str(_sp.get("text_abgewehrt", "")), str(_sp.get("text_abgewehrt"))[:40])

# ------------------------------------------------------------------ B. Reaktionsstufe
abschnitt("B. Die Reaktionsstufe kommt aus der Taktik des Bots")
_stufen = (daten.get("reaktion") or {}).get("stufen") or {}
for _name, _taktik in (("Haug", "Pluenderer"), ("Brynhild", "Waechterin"),
                       ("Grom", "Bastionier"), ("Silra", "Spaeherin")):
    _erwartet = float(_stufen.get(_taktik))
    _ist = B.reaktionsstufe({"name": _name}, daten)
    check("%s (%s) hat die Stufe aus der Datei" % (_name, _taktik), _ist == _erwartet,
          "erwartet %s, ist %s" % (_erwartet, _ist))
_neutral = float((daten.get("reaktion") or {}).get("standard"))
check("eine unbekannte Taktik bekommt den Standard",
      B.reaktionsstufe({"name": "Niemand"}, daten) == _neutral, str(_neutral))
check("ohne Datendatei gilt der Standard 1,0",
      B.reaktionsstufe({"name": "Haug"}, None) == B.REAKTION_STANDARD, str(B.REAKTION_STANDARD))

# ------------------------------------------------------------------ C. Spielerfortschritt
abschnitt("C. Ein deutlich ueberlegener Spieler macht den Bot vorsichtiger")
_reaktion = daten.get("reaktion") or {}
_vorsprung = float(_reaktion.get("vorsprung_prozent"))
_vorfaktor = float(_reaktion.get("vorsprung_faktor"))
_basis = B.reaktionsstufe({"name": "Haug"}, daten)
check("ohne Punkte auf beiden Seiten bleibt die Stufe",
      B.reaktionsfaktor({"name": "Haug"}, daten, 0, 0) == _basis, str(_basis))
check("bei gleichem Stand bleibt die Stufe",
      B.reaktionsfaktor({"name": "Haug"}, daten, 100, 100) == _basis, str(_basis))
_knapp = int(100 * (1.0 + _vorsprung / 100.0)) - 1
check("knapp unter der Vorsprung-Schwelle aendert sich nichts",
      B.reaktionsfaktor({"name": "Haug"}, daten, 100, _knapp) == _basis,
      "Spieler %d gegen Bot 100" % _knapp)
check("ab der Schwelle wird der Bot vorsichtiger",
      B.reaktionsfaktor({"name": "Haug"}, daten, 100, int(100 * (1.0 + _vorsprung / 100.0)))
      == round(_basis * _vorfaktor, 3), "Faktor %s" % _vorfaktor)
check("der Faktor bleibt in seiner Spanne",
      B.REAKTION_GRENZEN[0] <= B.reaktionsfaktor({"name": "Grom"}, daten, 0, 10 ** 9)
      <= B.REAKTION_GRENZEN[1], str(B.reaktionsfaktor({"name": "Grom"}, daten, 0, 10 ** 9)))

# ------------------------------------------------------------------ D. Schwellen
abschnitt("D. Die Stufe TEILT die vorhandenen Raubzug-Schwellen")
_regeln = {"aktiv": True, "armee_schwelle": 6, "staerke_faktor": 1.5}
_kopie = dict(_regeln)
_gierig = B.reaktions_schwellen(_regeln, 1.2)
check("gierig senkt die Armee-Schwelle", _gierig["armee_schwelle"] < _regeln["armee_schwelle"],
      "%s gegen %s" % (_gierig["armee_schwelle"], _regeln["armee_schwelle"]))
check("gierig senkt den Staerke-Faktor", _gierig["staerke_faktor"] < _regeln["staerke_faktor"],
      "%s gegen %s" % (_gierig["staerke_faktor"], _regeln["staerke_faktor"]))
check("der Faktor steht als Beleg im Ergebnis", _gierig.get("reaktionsfaktor") == 1.2,
      str(_gierig.get("reaktionsfaktor")))
check("vorsichtig hebt die Armee-Schwelle",
      B.reaktions_schwellen(_regeln, 0.8)["armee_schwelle"] > _regeln["armee_schwelle"],
      str(B.reaktions_schwellen(_regeln, 0.8)["armee_schwelle"]))
check("die Eingabe bleibt unveraendert (Kopie, keine zweite Wahrheit)", _regeln == _kopie, str(_regeln))
check("bei Faktor 1,0 kommt die Datei unveraendert zurueck",
      B.reaktions_schwellen(_regeln, 1.0) == _regeln, str(B.reaktions_schwellen(_regeln, 1.0)))
check("bei aktiv false wird nichts verschoben",
      B.reaktions_schwellen(dict(_regeln, aktiv=False), 1.2) == dict(_kopie, aktiv=False),
      str(B.reaktions_schwellen(dict(_regeln, aktiv=False), 1.2)))
check("die Schwelle faellt nie unter 1",
      B.reaktions_schwellen({"aktiv": True, "armee_schwelle": 1, "staerke_faktor": 1.5}, 2.0)
      ["armee_schwelle"] >= 1, "1 / 2,0")

# ------------------------------------------------------------------ E. Leseweg
abschnitt("E. Der Spaehbericht ueberlebt den Takt (additiv, Ladewache)")
_b1 = _bot(aufklaerung={"Siedlung 1": 1234.0})
_d1 = main.GameState.bot_als_dict(None, _b1)
check("bot_als_dict traegt die Berichte", _d1.get("aufklaerung") == {"Siedlung 1": 1234.0},
      str(_d1.get("aufklaerung")))
_b2 = main.BotPlayer(name="Haug", faction="menschlich", aggression=0.5, trading=0.5)
_b2.aufklaerung = {"alt": 1.0}
main.GameState.bot_aus_dict(None, _b2, {"name": "Haug"})
check("ohne das Feld bleiben die Berichte stehen (kein Loeschen)", _b2.aufklaerung == {"alt": 1.0},
      str(_b2.aufklaerung))
main.GameState.bot_aus_dict(None, _b2, {"name": "Haug", "aufklaerung": {"neu": 5.0}})
check("mit dem Feld werden die Berichte uebernommen", _b2.aufklaerung == {"neu": 5.0},
      str(_b2.aufklaerung))
_b3 = main.BotPlayer(name="Silra", faction="elfisch", aggression=0.5, trading=0.5)
check("ein alter Spielstand laedt mit leerem dict", _b3.aufklaerung == {}, str(_b3.aufklaerung))

# ------------------------------------------------------------------ F. Quellwachen
abschnitt("F. Keine zweite Rechnung: Drache und Wall bleiben die vorhandenen Stellen")
_takt_code = _code(main.GameState._bots_spaehung)
check("die Spaehung prueft den Wall ueber spionage.abwehr_pruefung",
      "spionage.abwehr_pruefung" in _takt_code, "Aufruf vorhanden")
check("die Spaehung rechnet keinen zweiten Aufklaerungswert",
      "aufklaerungswert" in _takt_code and "+" not in _takt_code.split("aufklaerungswert")[1][:40],
      "Aufklaerung kommt aus spionage.aufklaerungswert")
_drache_code = _code(main.GameState._bots_drachenzug)
check("der Drachenzug fragt drachen.bot_entscheidung (EIN Urteil)",
      "drachen.bot_entscheidung" in _drache_code, "Aufruf vorhanden")
check("der Drachenzug multipliziert keine eigene Schwelle",
      "schlagkraft_faktor" not in _drache_code, "kein zweiter Faktor im Code")
check("drachen.py oeffnet die Datendatei (EINE Lesestelle der Drachenzahl)",
      "daten(" in _code(__import__("drachen").bot_regeln), "bot_regeln liest die Datei")
main_code = _code(main.GameState.bots_fortschreiben)
check("der Aufruf der Spaehung steht im Raubzug-Pfad", "_bots_spaehung" in main_code, "Aufruf vorhanden")
check("die Reaktionsstufe wird dort angewandt", "reaktions_schwellen" in main_code, "Aufruf vorhanden")
check("vor dem Kampf wird gespaeht (Reihenfolge im Quelltext)",
      main_code.index("_bots_spaehung(") < main_code.index("kampf.fuehre_schlacht("),
      "Spaehung vor dem Kampfweg")
check("kein Spieltext im Code: die Meldung kommt aus der Datendatei",
      SPAEHER not in _takt_code, "Texte stehen in data/bot_diplomatie.json")

# ------------------------------------------------------------------ G. Echter Verlauf
abschnitt("G. Echter Verlauf: eine Spaehung, dann ein Angriff - keine Dauerspaehung")
root = None
app = None
# Ein Wuerfel im Prueffall macht den Sammellauf unzuverlaessig (Regel aus 05.11.2026):
# `bots_fortschreiben` baut ohne Saat ein `random.Random()` - der Angriff kann ausbleiben.
# Fuer die Dauer dieses Abschnitts bekommt jeder Generator denselben festen Startwert.
import random as _random  # noqa: E402

_echter_zufall = _random.Random
_random.Random = lambda *a, **k: _echter_zufall(4711)  # feste Saat fuer den Verlauf
try:
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    app = main.NebelseetalApp(root)
    app._build_main_ui()
    st = app.state
    app._erste_siedlung_gruenden()
    haug = _bot()
    st.bots = [haug]
    st.noob_protection = False
    st._letzter_bot_takt = 0.0
    _spaehungen = []
    _angriffe = []
    for _tag in range(1, 11):  # zehn Takte: der Angriff kommt nicht in jedem Lauf beim sechsten
        _erg = st.bots_fortschreiben(TAG * _tag)
        for _meldung in _erg.get("angriffe") or []:
            if SPAEHER in _meldung:
                _spaehungen.append(_meldung)
        _angriffe = [m for m in st.messages if m.get("type") == "kampf"]
        if _angriffe:
            break
    _berichte = [m for m in st.messages if m.get("type") == "spaehung"]
    check("es gibt GENAU EINE Spaehungs-Meldung", len(_berichte) == 1, str(len(_berichte)))
    check("der Bericht steht im Spielstand des Bots",
          "Siedlung 1" in (haug.aufklaerung or {}), str(haug.aufklaerung))
    check("nach der Spaehung greift der Bot an (keine Dauerspaehung)", bool(_angriffe),
          str([m.get("text")[:60] for m in _angriffe]))
    check("die Spaehungs-Meldung nennt den Bot und das Dorf",
          ("Haug" in str(_berichte[0].get("text"))) and ("Siedlung 1" in str(_berichte[0].get("text"))),
          str(_berichte[0].get("text"))[:70])
    check("die Spaehungs-Meldung bietet keinen Spionagebericht-Knopf (eigene Art)",
          str(_berichte[0].get("type")) == "spaehung", str(_berichte[0].get("type")))
    check("die neue Meldungsart hat eine eigene Farbe",
          main.nachrichten_farbe({"type": "spaehung"}) != main.nachrichten_farbe({"type": ""}),
          main.nachrichten_farbe({"type": "spaehung"}))
    # Zwei Takte spaeter ist der Bericht immer noch da und es wird NICHT erneut gespaeht.
    st.bots_fortschreiben(TAG * 8)
    check("ein vorhandener Bericht wird nicht durch eine zweite Spaehung ersetzt",
          len([m for m in st.messages if m.get("type") == "spaehung"]) == 1,
          str(len([m for m in st.messages if m.get("type") == "spaehung"])))
finally:
    _random.Random = _echter_zufall  # Saat wieder ausbauen
    if root is not None:
        try:
            root.destroy()
        except Exception:
            pass

# ------------------------------------------------------------------ H. Abwehr
abschnitt("H. Eine Spaehung am Wall kann abprallen - dann kostet sie Einheiten")
_pruefung = spionage.abwehr_pruefung(10, 3, 100.0)
check("eine schwache Truppe besteht die Vorpruefung nicht", _pruefung.get("bestanden") is False,
      str(_pruefung.get("grund")))
check("eine starke Truppe besteht sie", spionage.abwehr_pruefung(10 ** 6, 3, 100.0).get("bestanden") is True,
      "Aufklaerung 1.000.000 gegen Wall 3")
check("der Verlust wird aus der Datendatei gerechnet (keine Zahl im Code)",
      spionage.verlust_der_truppe({"Kundschafter": 10}) != {"Kundschafter": 10},
      str(spionage.verlust_der_truppe({"Kundschafter": 10})))

# ------------------------------------------------------------------ I. Drachen-Anzeige (F-14 = B)
abschnitt("I. F-14 = B: drachen.bedrohung ist eine ANZEIGE, keine Meidung")
import drachen as DR  # noqa: E402  - erst hier, damit der Aufbau oben schlank bleibt

_drache = None
for _eintrag in DR.alle():  # der erste offene Drache der Datendatei
    _drache = _eintrag  # merken
    break
check("die Datendatei nennt einen Drachen", _drache is not None, str(_drache))
_block = (DR.daten().get("bots") or {})
check("Reichweite steht in der Datei (nicht im Code)", int(_block.get("bedrohung_reichweite", 0)) > 0,
      str(_block.get("bedrohung_reichweite")))
check("der Anzeigetext steht in der Datei", "{abstand}" in str(_block.get("text_bedrohung", "")),
      str(_block.get("text_bedrohung"))[:40])
_welt = str(_drache.get("welt") or "")
_dimension = int(_welt[1:]) if _welt[1:].isdigit() else 0  # "d02" -> 2
_lage = {"x": int(_drache.get("x")), "y": int(_drache.get("y")), "dimension": _dimension}
_direkt = DR.bedrohung(_lage)
check("steht der Drache am Dorf, nennt die Meldung ihn", str(_drache.get("name")) in _direkt.get("text", ""),
      _direkt.get("text"))
check("auf demselben Feld gilt der Direkt-Satz", _direkt.get("text") == str(
    _block.get("text_bedrohung_direkt")).replace("{name}", str(_drache.get("name")))
    .replace("{abstand}", str(_direkt.get("abstand"))), _direkt.get("text"))
# Zwei Felder daneben: der Abstand wird gerechnet, der Erwartungswert kommt aus derselben Formel.
_lage2 = {"x": int(_drache.get("x")), "y": int(_drache.get("y")) + 2, "dimension": _dimension}
_erwartet_abstand = abs(_lage2["x"] - int(_drache.get("x"))) + abs(_lage2["y"] - int(_drache.get("y")))
_zwei = DR.bedrohung(_lage2)
check("der Abstand ist der Manhattan-Abstand", _zwei.get("abstand") == _erwartet_abstand,
      "erwartet %s, ist %s" % (_erwartet_abstand, _zwei.get("abstand")))
check("der Satz nennt den Abstand", str(_erwartet_abstand) in str(_zwei.get("text")), _zwei.get("text"))
_reichweite = int(_block.get("bedrohung_reichweite"))
_farne = {"x": int(_drache.get("x")) + _reichweite + 5, "y": int(_drache.get("y")), "dimension": _dimension}
_weit = DR.bedrohung(_farne)
check("ausserhalb der Reichweite schweigt die Meldung", _weit.get("text") == "",
      "Abstand %s, Reichweite %s" % (_weit.get("abstand"), _reichweite))
check("die Lage wird trotzdem genannt (fuer die Anzeige)", _weit.get("name") == str(_drache.get("name")),
      str(_weit.get("name")))
check("in einer anderen Welt gibt es keine Meldung",
      DR.bedrohung({"x": 0, "y": 0, "dimension": 99}) == {}, "Welt 99")
check("ein besiegter Drache zaehlt nicht",
      DR.bedrohung(_lage, (str(_drache.get("id")),)).get("text", "") in ("", None)
      or "Epheus" not in str(DR.bedrohung(_lage, (str(_drache.get("id")),)).get("text")),
      str(DR.bedrohung(_lage, (str(_drache.get("id")),))))
check("ein Ort ohne Lage ergibt keine Meldung", DR.bedrohung({"name": "nirgends"}) == {}, "ohne x/y")
_bedrohung_code = _code(DR.bedrohung)
check("die Meldung bucht nichts (keine Buchstelle im Code)",
      "buchen" not in _bedrohung_code and "vorraete" not in _bedrohung_code,
      "keine Buchung, keine Vorraete")
_drache_code2 = _code(main.GameState._bots_drachenzug)
check("der Drachenzug ruft die Meldung im Zweig 'zu stark'",
      "_drohung = drachen.bedrohung(" in _drache_code2, "Aufruf vorhanden")
check("die Entscheidung selbst bleibt drachen.bot_entscheidung",
      "drachen.bot_entscheidung" in _drache_code2, "kein zweites Urteil")
# Nur der Abschnitt ZWISCHEN Aufruf und continue darf nichts buchen - der Rest der Methode
# bucht Absichten des Kerns und enthaelt deshalb das Wort "buchen".
_stelle = _drache_code2.find("_drohung = drachen.bedrohung(")
_abschnitt = _drache_code2[_stelle:_drache_code2.find("continue", _stelle)]
check("die Meldung wird nur angehaengt, nicht gebucht",
      "_zusatz" in _abschnitt and "buchen" not in _abschnitt and "vorraete" not in _abschnitt,
      "Abschnitt zwischen Aufruf und continue: %d Zeichen" % len(_abschnitt))

bericht()
