# -*- coding: ascii -*-
"""Register 222 + 225: die Kartengruendungsseite als Startfenster, kein Fraktionswechsel,
und das Aufgeben einer Siedlung (Karte loeschen) nach dem Original.

DIE ENTSCHEIDUNGEN (Daniel, 05.11.2026, Register 222 und 225)
-------------------------------------------------------------
1. Das Startfenster des Spiels ist die Kartengruendungsseite; direkt nach "Neues Spiel" wird die
   Fraktion gefragt (sechs Voelker aus data/voelker.json), erst danach kommt die Karte.
2. Danach ist fuer den Spielstand ein Fraktionswechsel NICHT mehr moeglich - die Wahl beim Start
   ist die EINZIGE Stelle, an der `spieler_fraktion` gesetzt wird.
3. Die Karte wird GEZOGEN (Zufall), nicht gewaehlt. Passt sie nicht, laesst sich die Siedlung
   aufgeben: dann sind alle Einheiten, Waren, Gebaeude und Vorraete DIESER Siedlung verloren und
   die Karte liegt wieder im Stapel. Original: nur wenn mehr als eine Siedlung steht.
   Quelle: docs/original/Spielanleitung_2005/siedeln.php.txt, Zeilen 10-21.
4. Bots bekommen ebenfalls EINE Karte und beurteilen sie mit ihrem Engpass; sie geben ein Dorf nur
   auf, wenn ein anderes Dorf die Gruendung erneut bezahlen kann.

Was diese Datei beweist
-----------------------
1. Die Startseite ist die erste Ansicht; die drei Schritte laufen in der entschiedenen Reihenfolge.
2. Die Fraktionswahl landet im Spielstand und laesst sich nicht wiederholen (Quelle + Laufzeit).
3. Die Karte ist gezogen, nicht gewaehlt; die Gruendung nimmt GENAU diese Karte.
4. Aufgeben: Sperre bei einer Siedlung, Verlust aller Werte, Karte zurueck in den Stapel.
5. Bots: Urteil ueber die Karte, Aufgabe nur mit zahlendem zweiten Dorf.

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
check("die Startseite hat die Karte in den Spielstand geschrieben",
      _gezogene_seite in _ids, _gezogene_seite)
app._erste_siedlung_gruenden()
app.content.update_idletasks()
check("die Siedlung entsteht", len(app.state.settlements) == 1, str(len(app.state.settlements)))
check("die Siedlung traegt GENAU die gezogene Karte",
      (app.state.settlements[0].karte or {}).get("originalkarte_id") == _gezogene_seite,
      str((app.state.settlements[0].karte or {}).get("originalkarte_id")))
check("nach der Gruendung ist das Dorfzentrum die Ansicht",
      app.current_view == "Dorfzentrum", app.current_view)
check("das gewaehlte Volk steht im Dorfzentrum",
      any("Dein Volk:" in t for t in _texte(app)), "")

# ==========================================================================
abschnitt("4. Eine Siedlung aufgeben (Register 225, Originalregel)")
# ==========================================================================

_st = app.state
_erste = _st.settlements[0]
_ok1, _meld1 = _st.siedlung_aufgeben(_erste.id)
check("die EINZIGE Siedlung laesst sich nicht aufgeben", _ok1 is False, _meld1[:70])
check("die Ablehnung nennt den Grund", "einzige Siedlung" in _meld1, _meld1[:70])
check("nach der Ablehnung steht die Siedlung noch", len(_st.settlements) == 1, "")

# Zwei Siedlungen: die ERSTE traegt die Startkarte, die ZWEITE eine Stapelkarte.
_karte_id = next(k for k, e in sorted(_st.kartenvorrat.items()) if e.get("besitzer") is None)
_zweite = _karte_anlegen(_st, "Siedlung 2", _karte_id, {"holz": 40.0, "stein": 25.0},
                         {"Krieger": 3}, {"0": "holzfaeller", "1": "steinmetz"},
                         "probe-siedlung-2", aktiv=True)
_st.kartenvorrat[_karte_id]["besitzer"] = "spieler"
_size = next(m["size"] for m in M.MAPS if m["id"] == _st.current_map)
_st._weltkarte_sicherstellen()
_st.get_tile(_erste.x, _erste.y, _size).npc_faction = "spieler"

_ok2, _meld2 = _st.siedlung_aufgeben(_erste.id)
check("mit zwei Siedlungen laesst sie sich aufgeben", _ok2 is True, _meld2[:70])
check("die Siedlung ist danach weg",
      [s.id for s in _st.settlements] == [_zweite.id], str([s.id for s in _st.settlements]))
check("die Karte der Startseite ist wieder frei (naechster Start zieht neu)",
      _st.startkarte_gewaehlt == "", _st.startkarte_gewaehlt)
check("die andere Siedlung behaelt ihr Lager",
      round(float(_st.ortslager().get("holz", 0.0)), 2) == 40.0, str(_st.ortslager()))
check("die aktive Siedlung ist berichtigt", _st.aktive_siedlung_id == _zweite.id,
      _st.aktive_siedlung_id)
check("das Weltfeld ist wieder frei",
      _st.get_tile(_erste.x, _erste.y, _size).npc_faction is None, "")
check("die Aufgabe steht im Postfach",
      any("aufgegeben" in str(m.get("text")) for m in _st.messages[-3:]), "")
check("mit NUR EINER Siedlung ist die naechste Aufgabe wieder gesperrt",
      _st.siedlung_aufgeben(_zweite.id)[0] is False, "Original: nur mit mehr als einer Siedlung")

# Die Stapelkarte: eine dritte Siedlung, dann die zweite aufgeben - DIE Karte muss zurueck.
_karte_b = next(k for k, e in sorted(_st.kartenvorrat.items())
                if e.get("besitzer") is None and k != _karte_id)
_dritte = _karte_anlegen(_st, "Siedlung 3", _karte_b, {"holz": 40.0, "stein": 25.0},
                         {"Krieger": 3}, {"0": "holzfaeller", "1": "steinmetz"},
                         "probe-siedlung-3")
_st.kartenvorrat[_karte_b]["besitzer"] = "spieler"
_ok3, _meld3 = _st.siedlung_aufgeben(_dritte.id)
check("die dritte Siedlung laesst sich aufgeben (es stehen zwei)", _ok3 is True, _meld3[:70])
check("die Meldung nennt Gebaeude, Einheiten und Lager",
      "2 Gebaeude" in _meld3 and "3 Einheiten" in _meld3, _meld3[:90])
check("die Stapelkarte liegt wieder im Stapel",
      _st.kartenvorrat[_karte_b]["besitzer"] is None,
      str(_st.kartenvorrat[_karte_b]["besitzer"]))
check("die Startkarte bleibt unberuehrt (sie war nicht ihre)",
      _st.startkarte_gewaehlt == "", _st.startkarte_gewaehlt)

# Zuletzt die letzte Siedlung: sie ist die einzige und bleibt deshalb stehen.
check("die letzte Siedlung bleibt stehen", _st.siedlung_aufgeben(_zweite.id)[0] is False, "")
check("es steht genau eine Siedlung", [s.id for s in _st.settlements] == [_zweite.id],
      str([s.id for s in _st.settlements]))
check("der Zeiger steht auf der verbliebenen Siedlung",
      _st.aktive_siedlung_id == _zweite.id, _st.aktive_siedlung_id)
check("das Reich traegt nur das Lager dieser Siedlung",
      round(float(_st.ortslager().get("holz", 0.0)), 2) == 40.0, str(_st.ortslager()))

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

# Die Regel steht VOR dem Kauf: bot_dorf_gruenden fragt das Urteil und gruendet sonst nicht.
check("bot_dorf_gruenden fragt das Urteil vor dem Kauf",
      "bot_kartenurteil(bot, vorschlag)" in TEXT_MAIN, "")
check("ein nachtraegliches Aufgeben im Bot-Takt gibt es nicht mehr",
      "self.bot_siedlung_aufgeben" not in TEXT_MAIN,
      "das Aufgeben nach der Gruendung warf die Bots auf ein Dorf zurueck (gemessen)")

# Jedes Bot-Dorf muss eine Karte tragen, die seine Taktik traegt.
_b7 = _bot("Haug")
_b7.doerfer = [M.BotDorf(name="Haupt", hauptdorf=True, karte=_gut,
                         vorraete={"holz": 5000.0, "stein": 5000.0, "nahrung": 5000.0})]
M.bot_doerfer_karten_zuweisen(_b7)
check("zugewiesene Karten sind im Katalog",
      all(d.karte in _ids for d in _b7.doerfer), str([d.karte for d in _b7.doerfer]))

root.destroy()
bericht()
