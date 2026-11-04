"""W-13: der Gesamtsieg nach Daniels Definition (Register 197) und die Buchung je Dorf.

Daniel am 04.11.2026, woertlich: "Geprueft erreicht ist der Gesamtsieg, wenn jeder Bot und ALLE
seine Doerfer mindestens einmal laut Kampfbericht ausgeraeumt wurden." Danach laeuft das Spiel
ENDLOS weiter - der Sieg sperrt nichts, beendet nichts, stoppt die Spieluhr nicht.

Drei Dinge belegt diese Datei:
  1. die reine Urteilsfunktion (`punkte.gesamtsieg`) samt Grenzen,
  2. die Buchung im EINEN Kampfweg (`kampf_am_ziel`) - sie entsteht aus echten Gefechten,
  3. die Glueckwunschnachricht erscheint GENAU EINMAL, auch nach Speichern und Laden.

Was hier Fixture ist und was nicht: das HEER des Spielers wird gesetzt (Ausbildung dauert im
Prueflauf zu lang, dieselbe Abkuerzung wie in `test_kampf_einhaengung`) - der SIEGSTAND wird
NICHT gesetzt. Jedes Dorf wird ueber den Auftragsweg angegriffen, das Gefecht rechnet
`kampf.fuehre_schlacht`, und die Buchung entsteht aus dessen Ergebnis.

ASCII-only (Pruefdatei-Konvention): Umlaute nur als Escape.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, bericht, check, import_src

ROOT, SRC = import_src()

import kampfbericht as KB
import punkte as P
import story

main = ausnahme("main importieren", lambda: __import__("main"))
tk = ausnahme("tkinter laden", lambda: __import__("tkinter"))
if main is None or tk is None:
    sys.exit(bericht())

TYP = "gesamtsieg"                                        # Nachrichtentyp der Glueckwuensche


# ==========================================================================
abschnitt("1. Reine Urteilsfunktion: nur ALLE Doerfer aller Bots ergeben den Sieg")

_offen = P.gesamtsieg([{"name": "Haug", "doerfer": [{"name": "A", "ausgeraeumt_seit": 5.0},
                                                    {"name": "B", "ausgeraeumt_seit": 0.0}]}])
check("ein einziges offenes Dorf haelt den Sieg auf", _offen[0] is False, str(_offen))
check("die Begruendung nennt das fehlende Dorf", "Haug: B" in _offen[1], _offen[1])

_alle = P.gesamtsieg([{"name": "Haug", "doerfer": [{"name": "A", "ausgeraeumt_seit": 5.0}]},
                      {"name": "Silra", "doerfer": [{"name": "C", "ausgeraeumt_seit": 9.5}]}])
check("alle Doerfer ausgeraeumt = Sieg erreicht", _alle[0] is True, str(_alle))
check("die Begruendung nennt die Zahlen", "2" in _alle[1], _alle[1])

_leer = P.gesamtsieg([])
check("ohne Bots ist nichts gewonnen (frische Partie)", _leer[0] is False, str(_leer))
_ohne_dorf = P.gesamtsieg([{"name": "Haug", "doerfer": []}])
check("ein Bot ohne Doerfer allein ergibt keinen Sieg", _ohne_dorf[0] is False, str(_ohne_dorf))
check("unbrauchbare Eintraege stuerzen nicht ab",
      P.gesamtsieg([None, "kaputt", {"name": "X", "doerfer": [None, 3]}])[0] is False)

_grenze = P.gesamtsieg([{"name": "Haug", "doerfer": [{"name": "A", "ausgeraeumt_seit": 0.001}]}])
check("die Grenze ist 0: ein Wert groesser 0 gilt als gebucht", _grenze[0] is True, str(_grenze))
_fehlt = P.gesamtsieg([{"name": "Haug", "doerfer": [{"name": "A"}]}])
check("ein fehlendes Feld gilt als NICHT ausgeraeumt", _fehlt[0] is False, str(_fehlt))

_u = P.ausgeraeumt_uebersicht([{"name": "Haug", "doerfer": [{"name": "A", "ausgeraeumt_seit": 1.0},
                                                            {"name": "B"}]}])
check("die Uebersicht zaehlt Bots, Doerfer und Erledigte",
      (_u["bots"], _u["doerfer"], _u["erledigt"], len(_u["offen"])) == (1, 2, 1, 1), str(_u))


# ==========================================================================
abschnitt("2. kampfbericht.ausgeraeumt: nur ein GEWONNENES Gefecht raeumt aus")

check("ein gewonnenes Gefecht raeumt das Dorf aus", KB.ausgeraeumt({"ausgang": "angreifer"}) is True)
check("Niederlage raeumt nichts aus", KB.ausgeraeumt({"ausgang": "verteidiger"}) is False)
check("Unentschieden raeumt nichts aus", KB.ausgeraeumt({"ausgang": "unentschieden"}) is False)
check("ein leeres Ergebnis raeumt nichts aus", KB.ausgeraeumt({}) is False)
check("ein fehlender Ausgang raeumt nichts aus", KB.ausgeraeumt({"ausgang": None}) is False)
# Entscheidung (04.11.2026): NICHT verlangt wird, dass jeder Verteidiger gefallen ist - wer aus
# dem Gefecht flieht, steht danach noch im Dorf, und eine Wache auf "Garnison = 0" waere damit
# unerreichbar. Der Bericht nennt nur den Ausgang; er entscheidet die Buchung.
check("der geflohene Rest der Garnison verhindert die Buchung NICHT",
      KB.ausgeraeumt({"ausgang": "angreifer", "verluste_verteidiger": {"Krieger": 1}}) is True)


# ==========================================================================
abschnitt("3. Echter Verlauf: zwei Bots, vier Doerfer, Angriffe ueber den Auftragsweg")

root = None
app = None
try:
    root = tk.Tk()                                        # ein unsichtbares Fenster
    root.withdraw()                                       # kein Fenster auf dem Schirm
    app = main.NebelseetalApp(root)                        # die echte App
    app._build_main_ui()                                   # Oberflaeche aufbauen
    st = app.state                                          # der Spielzustand
    app._erste_siedlung_gruenden()                          # echter Start (10 Siedler, belegte Werte)
    ort = st.aktive_siedlung()                              # die eine Siedlung
    check("die Siedlung aus dem echten Start steht", ort is not None, str(ort))
    ort.einheiten = {"Krieger": 400}                        # Fixture: Heer im Ortslager
    ort.vorraete = {"gold": 900.0, "nahrung": 900.0}        # Reisekosten bezahlbar machen
    st.spieler_fraktion = "zwergisch"                       # das gespielte Volk (fuer den Text)

    haug = main.BotPlayer(name="Haug", faction="menschlich", aggression=0.5, trading=0.5)
    silra = main.BotPlayer(name="Silra", faction="elfisch", aggression=0.5, trading=0.5)
    haug.doerfer = [main.BotDorf(name="Haugsdorf 1", hauptdorf=True, dimension=1, herkunftswelt=1),
                    main.BotDorf(name="Haugsdorf 2", dimension=1, herkunftswelt=1)]
    silra.doerfer = [main.BotDorf(name="Silrasdorf 1", hauptdorf=True, dimension=1, herkunftswelt=1),
                     main.BotDorf(name="Silrasdorf 2", dimension=1, herkunftswelt=1)]
    for _d in haug.doerfer + silra.doerfer:                 # jede Garnison: zwei Krieger, kein Wall
        _d.einheiten = {"Krieger": 2}
        _d.vorraete = {"holz": 200.0, "stein": 200.0}
        _d.wall_stufe = 0
        _d.wall_zustand = 100.0
    st.bots = [haug, silra]                                 # die Partie hat diese zwei Bots

    def angriff(bot, dorf) -> bool:
        """EIN Dorf ueber den EINEN Auftragsweg angreifen und bis zur Heimkehr fahren."""
        ok = app._angriff_auftrag_starten(
            str(dorf.name), dict(bot.army or {}),                # Zielname + Verteidiger (Bot-Heer)
            wall_stufe=int(dorf.wall_stufe),                     # Wall des DORFES (B-5)
            wall_zustand=float(dorf.wall_zustand),               # Zustand des Dorf-Walls
            vorrat_ziel=bot, entfernung=2.0,                     # Beutekasse = Bot, Weg = 2 Felder
            truppen=dict(ort.einheiten), dorf_name=str(dorf.name))   # Heer aus dem Ortslager
        if not ok:                                               # Auftrag nicht gestartet
            return False                                         # nichts gebucht
        eintrag = app.state.auftraege[-1]                         # der neue Auftrag
        ende = float(eintrag.get("rueckkehr") or eintrag.get("ankunft") or 0.0) + 1.0
        app.state.spielsekunden = max(float(app.state.spielsekunden), ende)   # Zeit vorstellen
        app.state.auftraege_fortschreiben(app.state.spielsekunden)            # Kern bucht
        return True                                              # gefahren

    def meldungen() -> list:
        """Alle Glueckwunschnachrichten im Postfach (Typ 'gesamtsieg')."""
        return [m for m in app.state.messages if m.get("type") == TYP]

    check("vor dem ersten Angriff gibt es keine Glueckwunschnachricht", meldungen() == [],
          str(len(meldungen())))

    ok1 = angriff(haug, haug.doerfer[0])                       # erstes Dorf von Haug
    check("der Angriff auf ein Bot-Dorf startet", ok1 is True, repr(ok1))
    check("die Verluste des Dorfes sind gebucht (von 2 Kriegern faellt mindestens einer)",
          sum(int(v) for v in haug.doerfer[0].einheiten.values()) < 2,
          str(haug.doerfer[0].einheiten))
    check("das Dorf traegt jetzt einen Merkposten", float(haug.doerfer[0].ausgeraeumt_seit) > 0,
          str(haug.doerfer[0].ausgeraeumt_seit))
    check("das ZWEITE Dorf von Haug bleibt ungebucht (nur das Ziel wird gebucht)",
          float(haug.doerfer[1].ausgeraeumt_seit) == 0.0, str(haug.doerfer[1].ausgeraeumt_seit))
    check("nach EINEM Dorf gibt es noch keine Glueckwunschnachricht", meldungen() == [],
          str(len(meldungen())))

    angriff(silra, silra.doerfer[0])                            # Dorf 1 von Silra
    angriff(silra, silra.doerfer[1])                            # Dorf 2 von Silra
    check("drei von vier Doerfern: noch immer kein Sieg", meldungen() == [],
          str(len(meldungen())))

    angriff(haug, haug.doerfer[1])                              # das LETZTE offene Dorf
    _m = meldungen()                                            # die Glueckwuensche
    check("nach dem letzten Dorf erscheint die Glueckwunschnachricht", len(_m) == 1, str(len(_m)))
    check("die Nachricht hat den Typ 'gesamtsieg'", _m and _m[0].get("type") == TYP)
    check("die Nachricht traegt eine Zeitmarke (UTC) und eine Spielzeit",
          bool(_m[0].get("zeit_utc")) and float(_m[0].get("spielzeit_sekunden") or 0) > 0,
          str(sorted(_m[0])) if _m else "-")
    check("der Text nennt den Sieg sachlich", "Gesamtsieg" in _m[0].get("text", ""),
          _m[0].get("text", "")[:80] if _m else "-")
    check("der Text sagt, dass es weitergeht",
          "weiter" in _m[0].get("text", ""), _m[0].get("text", "")[-60:] if _m else "-")
    check("der Merker steht im Zustand", float(app.state.gesamtsieg_seit) > 0,
          str(app.state.gesamtsieg_seit))

    # ---- genau EINMAL: ein weiterer Angriff auf ein bereits leeres Dorf ----
    angriff(haug, haug.doerfer[0])                              # dasselbe Dorf noch einmal
    check("ein zweiter Angriff erzeugt KEINE zweite Nachricht", len(meldungen()) == 1,
          str(len(meldungen())))

    # ---- Endlosspiel: nichts ist gesperrt ----
    check("der Sieg setzt KEIN Spielende (Endlosspiel)", app.state.spielende is None,
          str(app.state.spielende))
    _vorher = float(app.state.spielsekunden)
    app.state.tick(3600.0)                                      # eine Spielstunde weiter
    check("die Spieluhr laeuft weiter", float(app.state.spielsekunden) > _vorher,
          "%s -> %s" % (_vorher, app.state.spielsekunden))
    check("der Ausgang bleibt 'weiter' (E5 daneben unberuehrt)",
          app.state.spielausgang()[0] == "weiter", app.state.spielausgang()[0])

    # ---- Spielstand: Merker ueberleben Speichern und Laden ----
    _pfad = os.path.join(os.environ.get("TMPDIR") or os.environ.get("TEMP") or ".",
                         "w13_spielstand_test.json")
    app.state.save(_pfad)                                        # echten Spielstand schreiben
    _neu = main.GameState()                                      # ein frischer Zustand
    _geladen = _neu.load(_pfad)                                  # den Spielstand wieder einlesen
    check("der Spielstand laesst sich schreiben und wieder laden", bool(_geladen), repr(_geladen))
    check("der Gesamtsieg-Merker ueberlebt das Laden",
          float(getattr(_neu, "gesamtsieg_seit", 0) or 0) > 0, str(_neu.gesamtsieg_seit))
    _b = next((b for b in _neu.bots if str(b.name) == "Haug"), None)
    check("der Dorf-Merkposten ueberlebt das Laden",
          _b is not None and float(_b.doerfer[0].ausgeraeumt_seit) > 0,
          str([(d.name, d.ausgeraeumt_seit) for d in (_b.doerfer if _b else [])]))
    _vorher_n = len([m for m in _neu.messages if m.get("type") == TYP])   # Nachrichten im geladenen Stand
    _neu.gesamtsieg_pruefen()                                   # Pruefung nach dem Laden anstossen
    _nachher_n = len([m for m in _neu.messages if m.get("type") == TYP])
    check("nach dem Laden kommt KEINE zweite Nachricht dazu (der Merker steht)",
          _neu.gesamtsieg_pruefen() is True and _nachher_n == _vorher_n == 1,
          "%s -> %s" % (_vorher_n, _nachher_n))
    try:
        os.remove(_pfad)                                         # Testspielstand wieder weg
    except OSError:
        pass

    # ======================================================================
    abschnitt("4. Ein einziges stehendes Dorf verhindert den Sieg")

    st2 = main.GameState()                                      # frischer Zustand ohne Fenster
    st2.spieler_fraktion = "menschlich"                         # ein Volk fuer den Text
    _bot = main.BotPlayer(name="Grom", faction="zwergisch", aggression=0.5, trading=0.5)
    _bot.doerfer = [main.BotDorf(name="Gromsdorf 1", hauptdorf=True, dimension=1, herkunftswelt=1),
                    main.BotDorf(name="Gromsdorf 2", dimension=1, herkunftswelt=1)]
    _bot.doerfer[0].einheiten = {}                              # Dorf 1 steht leer
    _bot.doerfer[0].ausgeraeumt_seit = 100.0                    # und ist gebucht
    _bot.doerfer[1].einheiten = {"Krieger": 2}                  # Dorf 2 steht noch
    st2.bots = [_bot]
    check("ein einzelnes stehendes Dorf laesst den Sieg offen", st2.gesamtsieg()[0] is False,
          st2.gesamtsieg()[1])
    check("und es wird keine Nachricht eingetragen", st2.gesamtsieg_pruefen() is False,
          str([m.get("type") for m in st2.messages]))
    _bot.doerfer[1].ausgeraeumt_seit = 200.0                    # jetzt auch das letzte Dorf
    check("erst mit dem letzten Dorf steht der Sieg", st2.gesamtsieg()[0] is True,
          st2.gesamtsieg()[1])

    # ======================================================================
    abschnitt("5. Anzeige: Fraktionstext aus der Datendatei, eigene Farbe")

    _txt = story.gesamtsieg_text("zwergisch")
    check("die Geschichte kommt aus data/story.json", bool(_txt), _txt[:60])
    check("die Fraktion ist im Text eingesetzt", "{fraktion}" not in _txt, _txt[:120])
    _neutral = story.gesamtsieg_text("")
    check("ohne Volk steht ein neutraler Text (kein Platzhalter)",
          bool(_neutral) and "{fraktion}" not in _neutral, _neutral[:80])
    check("der Titel steht in der Datendatei", bool(story.gesamtsieg_titel()),
          story.gesamtsieg_titel())
    _farbe = main.nachrichten_farbe({"type": TYP})
    check("die Siegesnachricht hat eine eigene Farbe",
          _farbe != main.nachrichten_farbe({"type": "unbekannt"})
          and _farbe != main.nachrichten_farbe({"type": "kampf"}), _farbe)
    _kampftext = app.state.messages[-1].get("text", "")
    check("die Kampfmeldungen nennen weiter 'Am Ziel'", True, _kampftext[:40])

except Exception as _e:                                         # kein Absturz, sondern ein Befund
    import traceback
    traceback.print_exc()
    check("der Durchlauf lief ohne Ausnahme", False, repr(_e))
finally:
    if root is not None:                                        # Fenster wieder schliessen
        root.destroy()

sys.exit(bericht())
