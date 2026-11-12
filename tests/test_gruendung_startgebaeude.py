# -*- coding: ascii -*-
"""Schnitt S-1: die Gruendung bringt Tempel, Holzfaeller und Steinmetz mit.

Vorgabe Daniel 01.11.2026 (docs/KONZEPT_SECHS_DOERFER_20261101.md, Abschnitt 1 und
Anhang 1): Der Siedlungskarren liefert bei JEDER Gruendung (erstes Dorf UND jede Kolonie)
Siedler, Grundrohstoffe und drei Gebaeude - Holzfaeller (moeglichst auf Wald), Steinmetz
(moeglichst auf Huegel oder Berg), Tempel (moeglichst auf Nebelsee, ohne Nebelsee auf
Steppe). Diese drei kosten nichts, binden keine Siedler und der Tempel wird bei der
GRUENDUNG ohne Baukunst gesetzt (Ausnahme); ein spaeterer Nachbau bleibt forschungspflichtig.

Entscheidung und Quelle (ersetzt die fruehere Annahme "nach der Gruendung steht noch kein
Gebaeude" in tests/test_startspiel.py): Seit diesem Schnitt stehen nach einer Gruendung
bereits Holz- und Steinproduktion. Die Platzwahl ist Gelaendevorliebe, kein Zufall.

Aufruf: python -X utf8 tests/test_gruendung_startgebaeude.py
"""

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['einheiten', 'gelaende', 'main:*', 'originalkarten']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------
import inspect
import os
import sys
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
os.chdir(SRC)

import main  # noqa: E402


def _karte(raster, spalten):
    """Eine minimale Karte fuer _startgebaeude_setzen (nur Raster und Spalten)."""
    spalten = int(spalten)
    return {"raster": list(raster), "spalten": spalten,
            "zeilen": (len(raster) + spalten - 1) // spalten}


def _dorf(raster, spalten):
    return main.Settlement(name="Test", map_id="kontinent", x=0, y=0,
                           karte=_karte(raster, spalten), id="test:0:0:0")


def _kennungen(ort):
    return {main.gelaende.finde_gebaeude(b) for b in (ort.bauten or {}).values()}


def _kern_pruefungen():
    # ---------------------------------------------------------------- 2 Wunschgelaende
    abschnitt("2. Wunschgelaende auf einer echten Originalkarte")
    karte = main.originalkarten.karte("original-036")
    ort = main.Settlement(name="T", map_id="k", x=0, y=0, karte=karte, id="t:0:0:0")
    erg = main._startgebaeude_setzen(ort, karte)
    nach = {e["gebaeude"]: e for e in erg}
    check("die Karte hat wirklich Wald (echte Kartendaten)",
          karte["zaehlung"]["wald"] > 0, str(karte["zaehlung"]["wald"]))
    check("der Holzfaeller steht auf Wald", nach["holzfaeller"]["gelaende"] == "wald",
          "Gelaende " + str(nach["holzfaeller"]["gelaende"])
          + ", Feld " + str(nach["holzfaeller"]["feld"]))
    check("der Tempel steht auf Nebelsee", nach["tempel"]["gelaende"] == "nebelsee",
          "Gelaende " + str(nach["tempel"]["gelaende"])
          + ", Feld " + str(nach["tempel"]["feld"]))
    check("Holzfaeller und Tempel sind Wunschgelaende (kein Ersatz)",
          nach["holzfaeller"]["wunsch"] and nach["tempel"]["wunsch"],
          str((nach["holzfaeller"]["wunsch"], nach["tempel"]["wunsch"])))
    feld_h = nach["holzfaeller"]["feld"]
    check("das Holzfaeller-Feld ist wirklich Wald im Raster",
          karte["raster"][feld_h] == "wald",
          "Feld " + str(feld_h) + " = " + str(karte["raster"][feld_h]))
    check("der Steinmetz steht auf Huegel oder Berg",
          nach["steinmetz"]["gelaende"] in ("huegel", "berg"),
          str(nach["steinmetz"]["gelaende"]) + ", Feld " + str(nach["steinmetz"]["feld"]))

    # ---------------------------------------------------------------- 3 Ersatzfall
    abschnitt("3. Ersatzfall: eine Karte ohne Nebelsee")
    karte2 = main.originalkarten.karte("original-085")
    check("die Ersatzkarte hat wirklich keinen Nebelsee",
          karte2["zaehlung"]["nebelsee"] == 0, str(karte2["zaehlung"]["nebelsee"]))
    ort2 = main.Settlement(name="T2", map_id="k", x=0, y=0, karte=karte2, id="t2:0:0:0")
    erg2 = main._startgebaeude_setzen(ort2, karte2)
    nach2 = {e["gebaeude"]: e for e in erg2}
    meldung2 = main._startgebaeude_meldung(erg2)
    check("der Tempel steht trotzdem", nach2["tempel"]["feld"] is not None,
          "Feld " + str(nach2["tempel"]["feld"]))
    check("die Meldung nennt das Gelaende, das es wurde",
          main.gelaende.name(nach2["tempel"]["gelaende"]) in meldung2, meldung2)

    # ---------------------------------------------------------------- 8 kleine/volle Karte
    abschnitt("8. Kleine oder volle Karte: kein Wurf, Fehlende werden genannt")
    klein = ["grasland", "sumpf", "grasland", "grasland"]
    ort8 = _dorf(klein, 2)
    erg8 = ausnahme("kleine Karte setzen",
                    lambda: main._startgebaeude_setzen(ort8, _karte(klein, 2)))
    check("die kleine Karte wirft nicht", erg8 is not None, str(erg8))
    nach8 = {e["gebaeude"]: e for e in (erg8 or [])}
    meldung8 = main._startgebaeude_meldung(erg8 or [])
    check("es werden so viele Gebaeude wie moeglich gesetzt",
          len([e for e in (erg8 or []) if not e.get("fehlend")]) == 1,
          str(erg8))
    check("Holzfaeller fehlt und wird genannt",
          nach8["holzfaeller"]["fehlend"]
          and main.gelaende.gebaeude_name("holzfaeller") in meldung8, meldung8)
    check("Steinmetz fehlt und wird genannt",
          nach8["steinmetz"]["fehlend"]
          and main.gelaende.gebaeude_name("steinmetz") in meldung8, meldung8)

    voll_ort = _dorf(["grasland"], 1)
    voll_ort.bauten = {"0": "haus"}
    voll_erg = ausnahme("volle Karte setzen",
                        lambda: main._startgebaeude_setzen(voll_ort, _karte(["grasland"], 1)))
    check("die volle Karte wirft nicht", voll_erg is not None, str(voll_erg))
    check("auf einer vollen Karte fehlen alle drei",
          all(e.get("fehlend") for e in (voll_erg or [])), str(voll_erg))

    # ---------------------------------------------------------------- 9 Quelltext-Wachen
    abschnitt("9. Quelltext-Wachen: EINE Platzfunktion, Vorlieben-Tabelle, kein Zufall")
    quelle_code = inspect.getsource(main._startgebaeude_setzen)
    check("die Platzwahl ist EINE Funktion und nutzt kein random",
          "random" not in quelle_code, str(len(quelle_code)) + " Zeichen Quelltext")
    check("die drei Gebaeude kommen aus einer Vorlieben-Tabelle",
          isinstance(main.STARTGEBAEUDE_VORLIEBEN, (tuple, list))
          and {e[0] for e in main.STARTGEBAEUDE_VORLIEBEN}
          == {"tempel", "holzfaeller", "steinmetz"},
          str([e[0] for e in main.STARTGEBAEUDE_VORLIEBEN]))
    check("die Funktion liest genau diese Tabelle",
          "STARTGEBAEUDE_VORLIEBEN" in quelle_code, "Tabelle referenziert")
    check("beide Gruendungswege rufen die Platzfunktion auf",
          "_startgebaeude_setzen" in inspect.getsource(main.NebelseetalApp._erste_siedlung_gruenden)
          and "_startgebaeude_setzen" in inspect.getsource(main.GameState.gruendung_ausfuehren),
          "erste Siedlung und Kolonie")


def _gruendungs_pruefungen(root):
    # ---------------------------------------------------------------- 1 erste Gruendung
    abschnitt("1. Erste Gruendung setzt genau drei Startgebaeude (je Stufe 1)")
    app = ausnahme("App aufbauen", lambda: main.NebelseetalApp(root))
    if app is None:
        return
    app._found_settlement()
    sett = app.state.settlements[0]
    kennungen = _kennungen(sett)
    check("genau drei Gebaeude stehen danach auf der Karte",
          len(sett.bauten) == 3, str(len(sett.bauten)))
    check("es sind Holzfaeller, Steinmetz und Tempel",
          kennungen == {"holzfaeller", "steinmetz", "tempel"}, str(sorted(kennungen)))
    check("jedes Gebaeude hat Stufe 1",
          all(int(sett.stufen.get(f, 0)) == 1 for f in sett.bauten), str(sett.stufen))

    # ---------------------------------------------------------------- 4 Startressourcen
    abschnitt("4. Startressourcen bleiben unveraendert (die Gebaeude kosten nichts)")
    check("10 Siedler bleiben erhalten", sett.bevoelkerung == 10, str(sett.bevoelkerung))
    check("100 Holz bleiben erhalten",
          abs(float(sett.vorraete.get("holz", 0.0)) - 100.0) < 1e-9,
          str(sett.vorraete.get("holz")))
    check("100 Stein bleiben erhalten",
          abs(float(sett.vorraete.get("stein", 0.0)) - 100.0) < 1e-9,
          str(sett.vorraete.get("stein")))

    # ---------------------------------------------------------------- 5 Tempel ohne Baukunst
    abschnitt("5. Tempel ohne Baukunst: Gruendung setzt ihn, Nachbau bleibt gesperrt")
    check("Baukunst ist zu Beginn Stufe 0",
          int(app.state.research["Baukunst"].level) == 0,
          str(app.state.research["Baukunst"].level))
    check("der Tempel steht trotz Baukunst Stufe 0", "tempel" in kennungen,
          str(sorted(kennungen)))
    frei = next((i for i, a in enumerate(sett.karte["raster"])
                 if str(i) not in sett.bauten
                 and main.gelaende.bau_moeglich("tempel", a)[0]), None)
    if frei is not None:
        ok, meldung = main.bauen_auf_karte(sett, "tempel", frei,
                                           forschungsstaende={"Baukunst": 0},
                                           nur_pruefen=True)
        check("ein Nachbau ueber den Bauweg bleibt ohne Baukunst abgelehnt",
              ok is False and "Baukunst" in meldung, meldung)

    # ---------------------------------------------------------------- 7 Meldung
    abschnitt("7. Die Meldung nennt alle drei Gebaeude und steht in Nachrichten und Log")
    gr = [m for m in app.state.messages if m.get("type") == "gruendung"]
    check("es gibt genau eine Gruendungsmeldung in den Nachrichten",
          len(gr) == 1, str(len(gr)))
    if gr:
        text = gr[0]["text"]
        n_holzf = main.gelaende.gebaeude_name("holzfaeller")
        n_stein = main.gelaende.gebaeude_name("steinmetz")
        n_tempel = main.gelaende.gebaeude_name("tempel")
        check("die Meldung nennt Tempel, Holzfaeller und Steinmetz",
              n_tempel in text and n_holzf in text and n_stein in text, text)
        check("die Meldung nennt drei Feldkoordinaten", text.count("(") == 3, text)
        check("dieselbe Meldung steht im Log", text in app.state.log,
              str(app.state.log[-3:]))

    # ---------------------------------------------------------------- 6 Kolonie
    abschnitt("6. Eine Kolonie bekommt dieselben drei Gebaeude")
    st = app.state
    quelle = st.settlements[0]
    for r in st.resources:
        quelle.vorraete[r] = 10000.0
    quelle.bevoelkerung = 100.0
    quelle.einheiten["Siedlerkarren"] = 1
    st.research["Wagenbau"].level = 1
    karten = st.freie_koloniekarten()
    karte_id = karten[0]["karte_id"]
    feld = st.freie_weltfelder(6)[0]
    ok, meldung = st.gruendung_ausfuehren(quelle, karte_id, feld)
    check("die Kolonie wird gegruendet", ok is True, meldung)
    if ok:
        neu = st.settlements[-1]
        kenn2 = _kennungen(neu)
        check("auch die Kolonie hat genau drei Startgebaeude",
              len(neu.bauten) == 3, str(len(neu.bauten)))
        check("Holzfaeller, Steinmetz und Tempel",
              kenn2 == {"holzfaeller", "steinmetz", "tempel"}, str(sorted(kenn2)))


def main_() -> int:
    _kern_pruefungen()

    try:
        root = tk.Tk()
    except tk.TclError as fehler:
        print("Kein Fenster moeglich (kein Desktop): " + str(fehler))
        return bericht()
    root.withdraw()
    try:
        _gruendungs_pruefungen(root)
    finally:
        try:
            root.destroy()
        except Exception:
            pass
    return bericht()


if __name__ == "__main__":
    sys.exit(main_())
