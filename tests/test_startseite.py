# -*- coding: ascii -*-
"""Register 222 + 225 + 228: die Kartengruendungsseite als Startfenster, kein Fraktionswechsel,
und das Aufgeben einer Siedlung (Karte loeschen) nach dem Original.

DIE ENTSCHEIDUNGEN (Daniel, 05.11.2026, Register 222, 225 und 228)
------------------------------------------------------------------
1. Das Startfenster des Spiels ist die Kartengruendungsseite; direkt nach "Neues Spiel" wird die
   Fraktion gefragt (sechs Voelker aus data/voelker.json), erst danach kommt die Karte.
2. Danach ist fuer den Spielstand ein Fraktionswechsel NICHT mehr moeglich - die Wahl beim Start
   ist die EINZIGE Stelle, an der `spieler_fraktion` gesetzt wird.
3. Register 228: die ERSTE Siedlung bekommt die FESTE Standardkarte (`original-036`) - fuer Spieler
   und Bots gleich. Gezogen wird nur bei NEUgruendungen. Passt eine Karte nicht, laesst sich die
   Siedlung aufgeben: dann sind alle Einheiten, Waren, Gebaeude und Vorraete DIESER Siedlung
   verloren (Original, siedeln.php Zeilen 10-21).
4. Register 228: das ERSTE Dorf (Index 0) ist erst aufgebenbar, wenn SECHS Siedlungen stehen; jedes
   andere Dorf weiterhin, sobald mehr als eine Siedlung steht.
5. Bots gruenden, beurteilen und geben auf, wenn die Karte ihre Taktik nicht traegt - mit Ruecklage
   der Gebuehr (`data/bot_gruendung.json`, Block `aufgeben`).

Was diese Datei beweist
-----------------------
1. Die Startseite ist die erste Ansicht; die drei Schritte laufen in der entschiedenen Reihenfolge.
2. Die Fraktionswahl landet im Spielstand und laesst sich nicht wiederholen (Quelle + Laufzeit).
3. Die erste Siedlung traegt die FESTE Startkarte (Register 228).
4. Aufgeben: Sperre bei einer Siedlung, Freischaltung des ersten Dorfes ab sechs Siedlungen,
   Verlust aller Werte, Karte zurueck in den Stapel - Kern und Anzeige fragen DIESELBE Funktion.
5. Bots: Aufgabe nur mit Ruecklage, Sperre und Erinnerung (Register 228).

Aufruf:  python -X utf8 tests/test_startseite.py
"""
from __future__ import annotations

import ast
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
import main as M  # noqa: E402
import originalkarten as O  # noqa: E402
import spieloekonomie as S  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()


def _texte(app):
    """Alle Texte der aktuellen Ansicht (auch in Kind-Rahmen)."""
    gesammelt = []

    def _durch(w):
        try:
            gesammelt.append(str(w.cget("text")))
        except Exception:                                            # noqa: BLE001
            pass
        for k in w.winfo_children():
            _durch(k)

    for k in app.content.winfo_children():
        _durch(k)
    return gesammelt


def _karte_anlegen(state, name, kartenkennung, vorraete, einheiten, bauten, kennung, aktiv=False):
    """Eine zweite Siedlung von Hand bauen (die echte Gruendung braucht Karren und Forschung)."""
    felder = state.freie_weltfelder(1)
    neu = M.Settlement(name=name, map_id=state.current_map, x=felder[0][0], y=felder[0][1],
                       karte=O.karte(kartenkennung), dimension=1, id=kennung,
                       volk=state.spieler_fraktion)
    neu.vorraete = dict(vorraete)
    neu.einheiten = dict(einheiten)
    neu.bauten = dict(bauten)
    state.settlements.append(neu)
    if aktiv:
        state.aktive_siedlung_id = kennung
    return neu


# ==========================================================================
abschnitt("1. Die Startseite ist die erste Ansicht (Register 222)")
# ==========================================================================

check("der Ansichtsname steht als EINE Konstante im Code",
      "KARTENGRUENDUNG_ANSICHT = " in TEXT_MAIN, M.KARTENGRUENDUNG_ANSICHT)
check("die Ansicht ist in der Ansichts-Tabelle eingetragen",
      "KARTENGRUENDUNG_ANSICHT: self._render_kartengruendung" in TEXT_MAIN, "")
check("der Spielstart zeigt ohne Siedlung die Startseite",
      "if not zustand.settlements:" in TEXT_MAIN
      and "self.current_view = KARTENGRUENDUNG_ANSICHT" in TEXT_MAIN, "")
check("ein geladener Spielstand startet weiter im Dorfzentrum",
      'self.current_view = "Dorfzentrum"' in TEXT_MAIN, "")
check("das Dorfzentrum zeigt die Voelkerwahl NICHT mehr",
      "_voelker_wahl_block()" not in TEXT_MAIN and "_startkarte_wahl_block()" not in TEXT_MAIN,
      "alte Bloecke stehen noch im Code")

import tkinter as tk  # noqa: E402  (erst hier: die Textpruefungen brauchen kein Fenster)

root = tk.Tk()
root.withdraw()
app = M.NebelseetalApp(root)
app._build_main_ui()
app._switch_view(M.KARTENGRUENDUNG_ANSICHT)
app.content.update_idletasks()
_t1 = _texte(app)
check("Schritt 1 zeigt die Ueberschrift", any("Kartengr\u00fcndung" in t for t in _t1),
      str(_t1[:4]))
check("Schritt 1 nennt die Schrittfolge", any("Schritt 1 von 3" in t for t in _t1), "")
check("Schritt 1 hat den Knopf Neues Spiel", any(t == "Neues Spiel" for t in _t1), "")
check("Schritt 1 zeigt noch KEINE Voelker",
      not any(t == "Dieses Volk nehmen" for t in _t1), "")

app._start_neues_spiel()
app.content.update_idletasks()
_t2 = _texte(app)
check("Schritt 2 ist die Fraktionsfrage", any("Schritt 2 von 3" in t for t in _t2), "")
check("Schritt 2 nennt die Ueberschrift der Voelkerwahl",
      any("W\u00e4hle dein Volk" in t for t in _t2), "")
check("Schritt 2 hat je Volk einen Knopf (sechs)",
      sum(1 for t in _t2 if t == "Dieses Volk nehmen") == 6,
      str(sum(1 for t in _t2 if t == "Dieses Volk nehmen")))

_vert = app._volk_waehlen("Ghule")
app.content.update_idletasks()
_t3 = _texte(app)
check("Schritt 3 ist die Karte", any("Schritt 3 von 3" in t for t in _t3), "")
check("Schritt 3 zeigt die gezogene Karte", any("Deine Karte" in t for t in _t3), "")
check("Schritt 3 bietet die Gruendung an", any("Auf dieser Karte gr" in t for t in _t3), "")
check("die Voelkerliste ist danach weg",
      not any(t == "Dieses Volk nehmen" for t in _t3), "")
check("die Wahl steht im Spielstand", app.state.spieler_fraktion == "Ghule",
      app.state.spieler_fraktion)
check("die Bots tragen Voelker aus der Verteilung",
      bool(_vert) and all(b.faction in set(_vert.values()) for b in app.state.bots),
      str([b.faction for b in app.state.bots]))
check("das Volk des Spielers ist bei den Bots nicht dabei",
      "Ghule" not in [b.faction for b in app.state.bots],
      str([b.faction for b in app.state.bots]))
check("die Startseite fragt die Fraktion VOR der Karte",
      TEXT_MAIN.find("self._volk_wahl_zeilen()") < TEXT_MAIN.find("self._startkarte_zeigen()"), "")

# ==========================================================================
abschnitt("2. Kein Fraktionswechsel (Register 222)")
# ==========================================================================

_zweit = app._volk_waehlen("Trolle")
check("ein zweiter Aufruf aendert die Fraktion nicht",
      app.state.spieler_fraktion == "Ghule", app.state.spieler_fraktion)
check("ein zweiter Aufruf liefert nichts zurueck", _zweit == {}, str(_zweit))
check("die Ablehnung steht im Code", "Das Volk steht bereits" in TEXT_MAIN, "")

# Quellwache: genau EINE Zuweisung an state.spieler_fraktion (die Wahl beim Start).
_zuweisungen = []
for _knoten in ast.walk(ast.parse(TEXT_MAIN)):
    _ziele = []
    if isinstance(_knoten, ast.Assign):
        _ziele = list(_knoten.targets)
    elif isinstance(_knoten, ast.AnnAssign):
        _ziele = [_knoten.target]
    for _ziel in _ziele:
        if (isinstance(_ziel, ast.Attribute) and _ziel.attr == "spieler_fraktion"
                and isinstance(_ziel.value, ast.Attribute) and _ziel.value.attr == "state"):
            _zuweisungen.append(_knoten.lineno)
check("genau EINE Stelle setzt state.spieler_fraktion", len(_zuweisungen) == 1,
      "Zeilen: " + str(_zuweisungen))

# ==========================================================================
abschnitt("3. Die Karte wird gezogen, nicht gewaehlt (Register 225)")
# ==========================================================================

_ids = set(O.kennungen())
_k1 = O.startkarte_ziehung("probe-225")
check("die Ziehung liefert eine echte Katalogkarte",
      _k1.get("originalkarte_id") in _ids, str(_k1.get("originalkarte_id")))
check("dieselbe Saat zieht dieselbe Karte",
      O.startkarte_ziehung("probe-225").get("originalkarte_id") == _k1.get("originalkarte_id"), "")
check("eine andere Saat zieht eine andere Karte",
      O.startkarte_ziehung("probe-anderes").get("originalkarte_id") != _k1.get("originalkarte_id"),
      "")
check("eine vergebene Karte wird NICHT wieder gezogen",
      O.startkarte_ziehung("probe-225", [_k1.get("originalkarte_id")]).get("originalkarte_id")
      != _k1.get("originalkarte_id"), "")
_gezogen = {O.startkarte_ziehung("saat-%d" % i).get("originalkarte_id") for i in range(60)}
check("die Ziehung ist nicht auf eine Karte festgelegt (60 Saaten, viele Karten)",
      len(_gezogen) > 20, "%d verschiedene Karten" % len(_gezogen))
check("spieloekonomie reicht die Ziehung durch (EINE Lesestelle)",
      S.startkarte_ziehung("probe-225").get("originalkarte_id") == _k1.get("originalkarte_id"), "")

_gezogene_seite = app.state.startkarte_gewaehlt
check("die Startseite meldet die FESTE Startkarte (Register 228, leeres Merkfeld)",
      _gezogene_seite == "", _gezogene_seite)
app._erste_siedlung_gruenden()
app.content.update_idletasks()
check("die Siedlung entsteht", len(app.state.settlements) == 1, str(len(app.state.settlements)))
check("die Siedlung traegt die FESTE Startkarte original-036",
      (app.state.settlements[0].karte or {}).get("originalkarte_id") == O.START_ID,
      str((app.state.settlements[0].karte or {}).get("originalkarte_id")))
check("nach der Gruendung ist das Dorfzentrum die Ansicht",
      app.current_view == "Dorfzentrum", app.current_view)
check("das gewaehlte Volk steht im Dorfzentrum",
      any("Dein Volk:" in t for t in _texte(app)), "")

# ==========================================================================
abschnitt("4. Aufgeben: Originalregel und die Freischaltung ab sechs Siedlungen (Register 228)")
# ==========================================================================

_st = app.state
_erste = _st.settlements[0]
_ok1, _meld1 = _st.siedlung_aufgeben(_erste.id)
check("die EINZIGE Siedlung laesst sich nicht aufgeben", _ok1 is False, _meld1[:70])
check("die Ablehnung nennt den Grund", "einzige Siedlung" in _meld1, _meld1[:70])
check("nach der Ablehnung steht die Siedlung noch", len(_st.settlements) == 1, "")

# Zwei Siedlungen: das ERSTE Dorf ist gesperrt, ein anderes nicht (Register 228).
_karte_id = next(k for k, e in sorted(_st.kartenvorrat.items()) if e.get("besitzer") is None)
_zweite = _karte_anlegen(_st, "Siedlung 2", _karte_id, {"holz": 40.0, "stein": 25.0},
                         {"Krieger": 3}, {"0": "holzfaeller", "1": "steinmetz"},
                         "probe-siedlung-2", aktiv=True)
_st.kartenvorrat[_karte_id]["besitzer"] = "spieler"
_size = next(m["size"] for m in M.MAPS if m["id"] == _st.current_map)
_st._weltkarte_sicherstellen()
_st.get_tile(_erste.x, _erste.y, _size).npc_faction = "spieler"

check("mit zwei Siedlungen ist das ERSTE Dorf noch gesperrt (Register 228)",
      _st.aufgeben_grund(_erste.id) != "", _st.aufgeben_grund(_erste.id)[:80])
check("der Grund nennt die sechs Siedlungen",
      "wenn 6 Siedlungen stehen" in _st.aufgeben_grund(_erste.id), _st.aufgeben_grund(_erste.id)[:90])
_ok_gesperrt, _meld_gesperrt = _st.siedlung_aufgeben(_erste.id)
check("der Kern gibt denselben Grund wie die Anzeige (EINE Quelle, F-04)",
      _ok_gesperrt is False and _meld_gesperrt == _st.aufgeben_grund(_erste.id), _meld_gesperrt[:80])
check("eine Ablehnung aendert nichts", len(_st.settlements) == 2, str(len(_st.settlements)))

_ok2, _meld2 = _st.siedlung_aufgeben(_zweite.id)
check("ein ANDERES Dorf laesst sich mit zwei Siedlungen aufgeben", _ok2 is True, _meld2[:70])
check("die Stapelkarte liegt wieder im Stapel", _st.kartenvorrat[_karte_id]["besitzer"] is None,
      str(_st.kartenvorrat[_karte_id]["besitzer"]))
check("die Startkarte bleibt unberuehrt", _st.startkarte_gewaehlt == "", _st.startkarte_gewaehlt)
check("die verbliebene Siedlung behaelt ihr Lager",
      round(float(_st.ortslager().get("holz", 0.0)), 2) == 100.0, str(_st.ortslager()))
check("mit NUR EINER Siedlung ist die naechste Aufgabe wieder gesperrt",
      _st.siedlung_aufgeben(_erste.id)[0] is False, "Original: nur mit mehr als einer Siedlung")

# Register 228: bis zur sechsten Siedlung bleibt das erste Dorf gesperrt - dann wird es frei.
for _nummer in range(2, 7):                                       # Siedlung 2 bis 6 (die alte 2 ist weg)
    _kid = next(k for k, e in sorted(_st.kartenvorrat.items()) if e.get("besitzer") is None)
    _karte_anlegen(_st, "Siedlung %d" % _nummer, _kid, {"holz": 40.0, "stein": 25.0},
                   {"Krieger": 3}, {"0": "holzfaeller", "1": "steinmetz"},
                   "probe-siedlung-%d" % _nummer)
    _st.kartenvorrat[_kid]["besitzer"] = "spieler"
check("es stehen sechs Siedlungen", len(_st.settlements) == 6, str(len(_st.settlements)))
check("mit sechs Siedlungen ist das ERSTE Dorf aufgebenbar",
      _st.aufgeben_grund(_erste.id) == "", _st.aufgeben_grund(_erste.id))
_ok3, _meld3 = _st.siedlung_aufgeben(_erste.id)
check("das erste Dorf laesst sich mit sechs Siedlungen aufgeben", _ok3 is True, _meld3[:70])
check("die Meldung nennt Geb\u00e4ude, Einheiten und Lager",
      "Geb\u00e4ude" in _meld3 and "Einheiten" in _meld3 and "Lager" in _meld3, _meld3[:90])
check("die Meldung sagt, dass die Startkarte fest bleibt",
      "Startkarte bleibt die feste Standardkarte" in _meld3, _meld3[:150])
check("die Siedlung ist danach weg", len(_st.settlements) == 5, str(len(_st.settlements)))
check("die Aufgabe steht im Postfach",
      any("aufgegeben" in str(m.get("text")) for m in _st.messages[-3:]), "")
check("die verbliebenen Doerfer behalten je ihr Lager",
      all(round(float((s.vorraete or {}).get("holz", 0.0)), 2) == 40.0 for s in _st.settlements),
      str([(s.vorraete or {}).get("holz") for s in _st.settlements]))
check("mit fuenf Siedlungen ist das NAECHSTE erste Dorf wieder gesperrt",
      _st.aufgeben_grund(_st.settlements[0].id) != "",
      _st.aufgeben_grund(_st.settlements[0].id)[:70])

# ==========================================================================
abschnitt("5. Bots: Urteil ueber die Karte und Aufgabe nur mit zahlendem zweiten Dorf")
# ==========================================================================

_DATEN = json.load(open(os.path.join(ROOT, "data", "bot_wirtschaft.json"), encoding="utf-8"))
check("ein Bot zieht EINE Karte (karten_kandidaten = 1)",
      int(_DATEN.get("karten_kandidaten") or 0) == 1, str(_DATEN.get("karten_kandidaten")))
check("die Datendatei nennt den Grund",
      "Register 225" in str(_DATEN.get("karten_kandidaten_hinweis") or ""), "")


def _bot(name="Haug"):
    b = M.BotPlayer(name, "menschlich", 0.3, 0.5)
    b.doerfer = []
    b.gedaechtnis = {}
    return b


_b = _bot()
_gut, _schlecht = "", ""
for _kennung in sorted(O.kennungen()):
    _u = M.bot_kartenurteil(_b, _kennung)
    if _u["gut_genug"] and not _gut:
        _gut = _kennung
    if (not _u["gut_genug"]) and not _schlecht:
        _schlecht = _kennung
    if _gut and _schlecht:
        break
check("es gibt Karten ueber und unter dem Durchschnitt der Taktik",
      bool(_gut) and bool(_schlecht), "%s / %s" % (_gut, _schlecht))
check("das Urteil nennt Punktzahl und Durchschnitt",
      M.bot_kartenurteil(_b, _gut).get("durchschnitt") > 0, str(M.bot_kartenurteil(_b, _gut)))
check("dasselbe Urteil ist reproduzierbar",
      M.bot_kartenurteil(_b, _gut) == M.bot_kartenurteil(_b, _gut), "")
check("ohne Karte ist das Urteil negativ",
      M.bot_kartenurteil(_b, "").get("gut_genug") is False, "")

_gs = app.state
_gs.messages = []
_b4 = _bot("Haug")
_b4.doerfer = [M.BotDorf(name="Haupt", hauptdorf=True, karte=_gut,
                         vorraete={"holz": 5000.0, "stein": 5000.0, "nahrung": 5000.0})]
check("der Bot bekommt in bot_dorf_gruenden eine Karte vorgeschlagen",
      bool(M.bot_kartenwahl(_b4, 0)), "")

# Register 228 (Daniel 05.11.2026, Antwort 3): der Bot gruendet, BEURTEILT danach und gibt auf.
# Die fruehere Wache "kein Aufgeben nach der Gruendung" ist damit ueberholt - sie sicherte die
# Uebergangsloesung aus Register 225, in der die Bots VOR dem Kauf urteilten.
check("der Bot-Takt ruft die Aufgabe nach der Gruendung",
      "self.bot_siedlung_aufgeben(" in TEXT_MAIN, "")
check("die Gruendung kauft keine bereits abgelehnte Karte wieder",
      "abgelehnte_karten" in TEXT_MAIN and "erinnerung_max" in TEXT_MAIN, "")
check("die Aufgabe hat Ruecklage, Sperre und Abbruchregel",
      all(wort in TEXT_MAIN for wort in ("RUECKLAGE", "aufgabe_seit", "aufgaben_max")), "")
check("die Bedingungen der Aufgabe stehen in der Datendatei",
      all(schluessel in open(os.path.join(ROOT, "data", "bot_gruendung.json"),
                             encoding="utf-8").read()
          for schluessel in ("aufgeben", "sperre_stunden", "erinnerung_max", "aufgaben_max")), "")

# Jedes Bot-Dorf muss eine Karte tragen, die seine Taktik traegt.
_b7 = _bot("Haug")
_b7.doerfer = [M.BotDorf(name="Haupt", hauptdorf=True, karte=_gut,
                         vorraete={"holz": 5000.0, "stein": 5000.0, "nahrung": 5000.0})]
M.bot_doerfer_karten_zuweisen(_b7)
check("zugewiesene Karten sind im Katalog",
      all(d.karte in _ids for d in _b7.doerfer), str([d.karte for d in _b7.doerfer]))

root.destroy()
bericht()
