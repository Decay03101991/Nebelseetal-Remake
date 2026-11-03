# -*- coding: ascii -*-
"""W-4: BOTS RAUBEN AUCH UNTEREINANDER - Stufe W-4 (03.11.2026, Daniels Vorgabe im Chat).

Daniels Vorgabe, woertlich: Bots, die stark genug sind (Einheiten, neue Doerfer gegruendet),
"beginnen Raubzuege um Ressourcen - nicht nur gegen den Spieler, auch gegeneinander."
Voraussetzung: "Bot und seine Welt sind spielaktiv." Aus den Vorgaben ausserdem: "Ein Bot in
einer anderen Welt ist kein Ziel", "ein starkes Bot greift einen schwaecheren an", "ein Dorf mit
Garnison wird nicht bestohlen" (dieselbe Regel wie S-12).

DAS PROBLEM, GEMESSEN (vor dem Bau)
-----------------------------------
`bot_angriffsplanung.waehle_ziel(self.settlements, ...)` waehlte Ziele ausschliesslich unter den
Siedlungen des SPIELERS. Ein Bot griff nie einen anderen Bot an - obwohl die Armee seit S-5b in
den Doerfern steht und seit S-5a ueber die Warteschlange entsteht.

Was diese Datei beweist
-----------------------
1. Die Kandidaten sind die Doerfer ANDERER Bots in DERSELBEN Welt - nie die eigenen, nie ein Dorf
   einer fremden Welt. Jeder Kandidat traegt Name, Wall, Besatzung und Welt.
2. Die vier Wachen: ein Bot ohne (genug) Einheiten greift nicht an, eine zu starke Besatzung wird
   nicht angegriffen, ein zu hoher Wall nicht, und das Dorf mit Garnison wird weiterhin NICHT
   bestohlen (S-12 unveraendert).
3. Der Raubzug laeuft durch die App: Kampf ueber `kampf.fuehre_schlacht`, Beute ueber
   `kampfbericht.beute_am_ziel` beim Zielort abgebucht, Bericht im Postfach, Beute beim Angreifer.
4. Zwei Regeln bleiben: das Dorf wechselt NICHT den Besitzer (keine Eroberung) und die Truppen
   bleiben nicht am Zielort stehen.
5. Quellwachen: der Angriffsweg fragt die Raubziele ueberhaupt, und die Beute geht ueber die EINE
   Formel.

Aufruf:  python -X utf8 tests/test_bot_raubzug_bot.py
"""
from __future__ import annotations

import ast
import inspect
import os
import random
import sys
import textwrap
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import bot_angriffsplanung as P  # noqa: E402
import main as M  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()


def _dorf(name, welt=4, wall=0, einheiten_=None, vorraete=None, haupt=False):
    """Ein Bot-Dorf fuer die Pruefung - nur die Felder, die die Zielwahl liest."""
    return M.BotDorf(name=name, x=0, y=0, herkunftswelt=welt, dimension=welt,
                     hauptdorf=haupt, wall_stufe=wall, wall_zustand=100.0,
                     einheiten=dict(einheiten_ or {}), vorraete=dict(vorraete or {}))


def _bot(name, doerfer, fraktion="menschlich", aggression=0.0):
    """Ein Bot fuer die Pruefung - name, Fraktion, Aggression, Doerfer."""
    return M.BotPlayer(name, fraktion, aggression, 0.0, doerfer=list(doerfer))


def _code(fn):
    """Der Quelltext einer Funktion OHNE Docstring - ein Kommentar darf keine Wache faerben."""
    baum = ast.parse(textwrap.dedent(inspect.getsource(fn)))
    baum.body[0].body = [s for s in baum.body[0].body
                         if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant))]
    return ast.unparse(baum)


# ==========================================================================
abschnitt("1. Kandidaten: Doerfer ANDERER Bots in DERSELBEN Welt")
# ==========================================================================
haug = _bot("Haug", [_dorf("Haugs Siedlung 1", haupt=True), _dorf("Haugs Siedlung 2")])
brynhild = _bot("Brynhild", [_dorf("Brynhilds Siedlung 1", einheiten_={"Krieger": 2},
                                  vorraete={"holz": 300}, haupt=True)])
grom = _bot("Grom", [_dorf("Groms Siedlung 1", welt=1, haupt=True)], fraktion="zwergisch")
bots = [haug, brynhild, grom]
kandidaten = P.raubziele(haug, bots)

check("1 ein Bot-Dorf derselben Welt ist ein Kandidat",
      [k["name"] for k in kandidaten] == ["Brynhilds Siedlung 1"], str([k["name"] for k in kandidaten]))
check("1 die EIGENEN Doerfer sind nie Ziel",
      all(k["dorf"] is not haug.doerfer[0] and k["dorf"] is not haug.doerfer[1] for k in kandidaten))
check("1 ein Dorf einer ANDEREN Welt ist kein Ziel (Grom in Welt 1)",
      all(k["welt"] == 4 and k["bot"] is brynhild for k in kandidaten), str([(k["name"], k["welt"]) for k in kandidaten]))
check("1 der Kandidat traegt Name, Wall, Besatzung und Welt",
      kandidaten and all(set(("name", "wall", "besatzung", "welt")) <= set(k) for k in kandidaten),
      str(sorted(kandidaten[0]) if kandidaten else "kein Kandidat"))
check("1 die Besatzung ist die Anzahl der Einheiten vor Ort",
      bool(kandidaten) and int(kandidaten[0]["besatzung"]) == 2, str(kandidaten[0]["besatzung"] if kandidaten else 0))
check("1 der Wall steht als (Stufe, Zustand) im Kandidaten",
      bool(kandidaten) and tuple(kandidaten[0]["wall"]) == (0, 100.0), str(kandidaten[0]["wall"] if kandidaten else 0))
# Die Weltgrenze ist ein SCHALTER in den Daten, kein Sonderfall im Code: ausgeschaltet erscheint
# auch das Dorf der fremden Welt - so ist belegt, dass die Bedingung wirklich filtert.
offen = dict(P.raubzug_einstellungen())
offen["nur_eigene_welt"] = False
check("1 ohne Weltgrenze erscheint auch der Bot der fremden Welt",
      "Groms Siedlung 1" in [k["name"] for k in P.raubziele(haug, bots, offen)])
check("1 ist der Raubzug AUS, gibt es keinen Kandidaten",
      P.raubziele(haug, bots, {"aktiv": False}) == [])
ohne_dorf = _bot("OhneDorf", [])
check("1 ein Bot ohne Doerfer (keine bekannte Welt) sammelt keine Kandidaten",
      P.raubziele(ohne_dorf, bots) == [], str(P.raubziele(ohne_dorf, bots)))

# ==========================================================================
abschnitt("2. Die vier Wachen der Zielwahl")
# ==========================================================================
stark = {"Krieger": 20}
schwach = {"Buergerwehr": 3}
ziellein = [{"name": "Brynhilds Siedlung 1", "welt": 4, "wall": (0, 100.0), "besatzung": 0,
             "dorf": _dorf("Brynhilds Siedlung 1", vorraete={"holz": 300}), "bot": brynhild}]

z1, d1 = P.waehle_raubziel(ziellein, {}, {})
check("2 ein Bot OHNE Einheiten greift nicht an", z1 is None, d1.get("grund", ""))
z2, d2 = P.waehle_raubziel(ziellein, schwach, {})
check("2 ein Bot unter der Armee-Schwelle greift nicht an", z2 is None, d2.get("grund", ""))
z3, d3 = P.waehle_raubziel(ziellein, stark, {})
check("2 ein starker Bot gegen ein leeres Dorf DARF rauben", z3 is not None, d3.get("grund", ""))

starke_besatzung = [dict(ziellein[0], besatzung=60,
                         dorf=_dorf("Brynhilds Siedlung 1", einheiten_={"Krieger": 60}))]
z4, d4 = P.waehle_raubziel(starke_besatzung, stark, {})
check("2 eine zu starke Besatzung wird nicht angegriffen (staerke_faktor)", z4 is None, d4.get("grund", ""))
z5, d5 = P.waehle_raubziel(starke_besatzung, {"Krieger": 200}, {})
check("2 mit vierfacher Uebermacht ist dieselbe Besatzung ein Ziel", z5 is not None, d5.get("grund", ""))

hoher_wall = [dict(ziellein[0], wall=(10, 100.0),
                   dorf=_dorf("Brynhilds Siedlung 1", wall=10, vorraete={"holz": 300}))]
z6, d6 = P.waehle_raubziel(hoher_wall, stark, {})
check("2 ein zu hoher Wall wird nicht angegriffen", z6 is None, d6.get("grund", ""))

zwei = [dict(ziellein[0], name="B Wall 2", wall=(2, 100.0),
             dorf=_dorf("B Wall 2", wall=2, vorraete={"holz": 300})),
        dict(ziellein[0], name="A Wall 0", wall=(0, 100.0),
             dorf=_dorf("A Wall 0", vorraete={"holz": 300}))]
z7, d7 = P.waehle_raubziel(zwei, stark, {})
check("2 das SCHWAECHSTE Dorf wird gewaehlt (niedrigster Wall zuerst)",
      z7 is not None and z7["name"] == "A Wall 0", str(z7["name"] if z7 else None))
z8, d8 = P.waehle_raubziel([], stark, {})
check("2 ohne Kandidaten gibt es kein Ziel", z8 is None, d8.get("grund", ""))

# S-12 bleibt unveraendert: ein Dorf MIT Garnison wird nicht bestohlen - wer Truppen zu Hause
# hat, wird angegriffen. Diese Regel gehoert zum Diebstahl und wird vom Raubzug nicht beruehrt.
einst_dieb = M.bot_diebstahl_einstellungen()
duenn = _bot("Klein", [_dorf("Kleins Siedlung 1", haupt=True)])
mit_garnison = _dorf("Spieler-Siedlung", einheiten_={"Krieger": 1}, vorraete={"holz": 100})
ohne_garnison = _dorf("Spieler-Siedlung 2", vorraete={"holz": 100})
check("2 Diebstahl-Einstellungen sind eingeschaltet (sonst prueft dieser Abschnitt nichts)",
      bool(einst_dieb.get("aktiv", False)), str(einst_dieb.get("aktiv")))
check("2 S-12 unveraendert: ein Dorf MIT Garnison wird nicht bestohlen",
      M.bot_diebstahl(duenn, mit_garnison, 1000.0, einst_dieb) is None)
check("2 S-12 unveraendert: ein Dorf OHNE Garnison wird bestohlen",
      isinstance(M.bot_diebstahl(duenn, ohne_garnison, 1000.0, einst_dieb), dict))

# ==========================================================================
abschnitt("3. Der Raubzug laeuft durch die App: Kampf, Beute, Postfach")
# ==========================================================================
root = tk.Tk()
root.withdraw()
app = None
try:
    app = M.NebelseetalApp(root)
    app._build_main_ui()
    st = app.state
    st.noob_protection = False                                   # Goetterschutz aus (Testlage)
    app._erste_siedlung_gruenden()                               # ein echter Spieler-Ort
    spieler_ort = st.aktive_siedlung()
    spieler_ort.einheiten = {"Krieger": 30}                      # Garnison: kein Diebstahlsziel
    haug2 = _bot("Haug", [_dorf("Haugs Siedlung 1", haupt=True)], aggression=1.0)
    ziel_dorf = _dorf("Brynhilds Siedlung 1", vorraete={"holz": 500, "stein": 500}, haupt=True)
    brynhild2 = _bot("Brynhild", [ziel_dorf])
    grom2 = _bot("Grom", [_dorf("Groms Siedlung 1", welt=1, haupt=True)], fraktion="zwergisch")
    st.bots = [haug2, brynhild2, grom2]
    haug2.doerfer[0].einheiten = {"Krieger": 20}                 # Angreifer steht im Hauptdorf
    haug2.lager = {"Handkarren": 5}                              # Wagenpark fuer die Beute
    haug2.naechster_angriff = 0.0                                # Angriffsfenster offen
    haug_vorher = sum(float(v) for v in M.bot_kasse(haug2).values())
    ziel_vorher = float(ziel_dorf.vorraete.get("holz", 0)) + float(ziel_dorf.vorraete.get("stein", 0))
    spieler_holz = float(st.resources["holz"].amount)
    grom_vorher = float(grom2.doerfer[0].vorraete.get("holz", 0) or 0)

    ergebnis = st.bots_fortschreiben(float(M.BOT_TAKT_SEKUNDEN))
    meldungen = list(ergebnis.get("angriffe") or [])
    ziel_nachher = float(ziel_dorf.vorraete.get("holz", 0)) + float(ziel_dorf.vorraete.get("stein", 0))
    haug_nachher = sum(float(v) for v in M.bot_kasse(haug2).values())

    check("3 der Bot greift ein Dorf eines ANDEREN Bots an",
          any("gegen Brynhild" in m for m in meldungen), str(meldungen))
    check("3 der Bericht nennt Dorf und tats\u00e4chliche Beute",
          any("Brynhilds Siedlung 1" in m and "tats\u00e4chliche Beute" in m for m in meldungen),
          str(meldungen))
    check("3 die Beute wird beim ZIELORT abgebucht (kein Rohstoff aus dem Nichts)",
          ziel_nachher < ziel_vorher, "vorher %s, nachher %s" % (ziel_vorher, ziel_nachher))
    check("3 der Angreifer gewinnt dabei Rohstoffe (seine Kasse waechst)",
          haug_nachher > haug_vorher,
          "Angreifer +%s, Ziel -%s" % (round(haug_nachher - haug_vorher, 2),
                                       round(ziel_vorher - ziel_nachher, 2)))
    check("3 der Spieler verliert dabei nichts",
          float(st.resources["holz"].amount) == spieler_holz,
          "%s -> %s" % (spieler_holz, st.resources["holz"].amount))
    check("3 der Bot der ANDEREN Welt bleibt unberuehrt (kein Ziel ueber die Weltgrenze)",
          float(grom2.doerfer[0].vorraete.get("holz", 0) or 0) == grom_vorher,
          "%s -> %s" % (grom_vorher, grom2.doerfer[0].vorraete.get("holz", 0)))
    check("3 der Bericht steht im Postfach (wie beim Angriff auf den Spieler)",
          any(m.get("type") == "kampf" and "gegen Brynhild" in str(m.get("text"))
              for m in st.messages),
          str([m.get("type") for m in st.messages[-3:]]))
    check("3 das Dorf wechselt NICHT den Besitzer (keine Eroberung)",
          ziel_dorf in brynhild2.doerfer and ziel_dorf not in haug2.doerfer)
    check("3 das Dorf bleibt in SEINER Welt",
          int(ziel_dorf.dimension) == 4 and int(ziel_dorf.herkunftswelt) == 4,
          "%s / %s" % (ziel_dorf.dimension, ziel_dorf.herkunftswelt))
    check("3 der Angreifer baut keine Garnison am Zielort auf (keine Stationierung)",
          not any("Stationierung" in str(m) for m in meldungen))

    # Die Buchung GENAU nachrechnen: ein zweiter Raubzug ueber dieselbe Methode, mit einem
    # FRISCHEN Angreifer (0 Punkte) - so misst der Vergleich nur die Beute und nicht die
    # Wirtschaft, die das Ziel im selben Takt nebenher betreibt.
    pruef_bot = _bot("Haug-Kopie", [_dorf("Haugs Siedlung 9", haupt=True)])
    pruef_bot.doerfer[0].einheiten = {"Krieger": 20}
    ziel2 = _dorf("Brynhilds Siedlung 2", vorraete={"holz": 400, "stein": 400})
    brynhild2.doerfer.append(ziel2)
    vorher2 = float(ziel2.vorraete["holz"]) + float(ziel2.vorraete["stein"])
    meldung2, beute2 = st._bots_raubzug(pruef_bot, brynhild2, ziel2, {"Krieger": 20},
                                        {"Handkarren": 5}, random.Random(7))
    nachher2 = float(ziel2.vorraete["holz"]) + float(ziel2.vorraete["stein"])
    check("3 die Beute ist GENAU der Abgang am Zielort (eine Formel, keine zweite Buchung)",
          bool(beute2) and abs((vorher2 - nachher2) - sum(beute2.values())) < 1e-6,
          "Ziel -%s, Beute %s - %s" % (round(vorher2 - nachher2, 2), sum(beute2.values()), meldung2))
    check("3 das Ziel behaelt den Rest seines Lagers (nie negativ)",
          nachher2 >= 0 and nachher2 < vorher2, str(nachher2))
except Exception as fehler:                                      # noqa: BLE001 - Meldung statt Absturz
    # Ein Absturz in diesem Abschnitt ist ein FEHLER, kein Befund: der Raubzug ist der Gegenstand
    # der Datei. Wuerde er nur als Befund gemeldet, bliebe der Lauf gruen, obwohl nichts geprueft
    # wurde (genau diese Falle hat die Gegenprobe am 03.11.2026 aufgedeckt).
    check("3 der App-Lauf laeuft ohne Ausnahme durch", False, repr(fehler))
finally:
    root.destroy()

# ==========================================================================
abschnitt("4. Quellwachen: der Angriffsweg fragt die Raubziele, die Beute geht ueber EINE Formel")
# ==========================================================================
check("4 der Bot-Angriffsweg fragt die Raubziele ueberhaupt",
      "bot_angriffsplanung.raubziele(" in TEXT_MAIN and "bot_angriffsplanung.waehle_raubziel(" in TEXT_MAIN)
check("4 die Raubziel-Wahl bekommt die eigene Armee und den Wagenpark",
      "waehle_raubziel(" in TEXT_MAIN and "_raub_kandidaten, bot_kaempfer, bot_geraet" in TEXT_MAIN)
check("4 der Spieler-Pfad bleibt unveraendert (waehle_ziel auf self.settlements)",
      "waehle_ziel(\n                        self.settlements" in TEXT_MAIN)
check("4 der Raubzug kaempft ueber kampf.fuehre_schlacht",
      "kampf.fuehre_schlacht(" in _code(M.GameState._bots_raubzug))
check("4 der Raubzug bucht die Beute ueber kampfbericht.beute_am_ziel",
      "kampfbericht.beute_am_ziel(" in _code(M.GameState._bots_raubzug))
check("4 der Raubzug schreibt einen Bericht ins Postfach",
      "self.messages.append(" in _code(M.GameState._bots_raubzug))
check("4 die Weltgrenze steht in den Daten, nicht im Code",
      "nur_eigene_welt" in open(os.path.join(ROOT, "data", "bot_raubzug.json"),
                                encoding="utf-8").read())

sys.exit(bericht())
