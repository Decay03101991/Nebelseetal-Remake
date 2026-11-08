# -*- coding: ascii -*-
"""Wache fuer den Dorfumzug im Portalraum (Schnitt S-3, 08.11.2026).

Daniels Entscheidungen: F-25 = A (nur die 5.000 Mana, kein Gold, keine Waren), F-26 = A (ein
belegtes Feld wird abgelehnt, auch ein Bot-Dorf), F-27 = A (alles reist mit - Bauten, Stufen,
Garnison, Waren, Karawanen), F-28 = C (keine Sperre mehr; bis S-5 gilt noch die belegte
24-Stunden-Regel). Belege: docs/design/PORTAL_MODELL_20261108.md Abschnitte 6 und 9.

Geprueft wird die EINE Buchstelle `NebelseetalApp._dorf_versetzen` samt der Uebersetzung
Spielstand -> Felder (`_portal_belegte_felder`): erst pruefen, dann genau einmal abbuchen.
Dazu die Zusage, die den teuersten Punkt des Schnitts (W-1) erledigt: die Kennung bleibt
unveraendert, weil der Umzug nur welt_x/welt_y und die Welt setzt, nicht x/y.

Aufruf: python -X utf8 tests/test_dorf_versetzen.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
os.chdir(SRC)

import main as M            # noqa: E402
import portalraum as P      # noqa: E402


class _App:
    """Stellvertreter ohne Fenster: bindet die ECHTEN Methoden der App an einen Spielstand."""

    _siedlung_nach_namen = M.NebelseetalApp._siedlung_nach_namen
    _unterwegs_anzahl = M.NebelseetalApp._unterwegs_anzahl
    _bot_doerfer_im_raster = M.NebelseetalApp._bot_doerfer_im_raster
    _portal_belegte_felder = M.NebelseetalApp._portal_belegte_felder
    _dorf_versetzen = M.NebelseetalApp._dorf_versetzen
    _feld_im_raster = M.NebelseetalApp._feld_im_raster
    _ort_feld = M.NebelseetalApp._ort_feld

    def __init__(self, state):
        self.state = state
        self.logs = []

    def _log(self, text):
        self.logs.append(str(text))

    def _render_view(self):
        """Kein Fenster: die Buchstelle darf neu zeichnen, hier gibt es nichts zu zeichnen."""

    def letzte_meldung(self):
        return str((self.state.messages or [{}])[-1].get("text") or "")

    def portalmeldungen(self):
        return [m for m in (self.state.messages or []) if m.get("type") == "portal"]


def _aufbau():
    """Ein Spielstand mit einem eigenen Dorf, einem zweiten Dorf und einem Bot-Dorf."""
    gs = M.GameState()
    start = int(gs.eigene_dimension)
    gs.resources["mana"].amount = 20000.0
    gs.letzter_wechsel = None
    dorf = M.Settlement(name="Eschenhain", map_id="kontinent", x=3, y=3,
                        id=M.siedlung_kennung("spieler", "kontinent", 3, 3),
                        dimension=start, bauten={"0": "dorfzentrum"},
                        garrison={"bogenschuetze": 4})
    zweit = M.Settlement(name="Zweithauch", map_id="wald", x=4, y=5,
                         id=M.siedlung_kennung("spieler", "wald", 4, 5), dimension=start,
                         welt_x=2, welt_y=2)
    bot = M.BotPlayer(name="Grom", faction="Ghule", aggression=0.5, trading=0.5,
                      settlements=["Gromlager"])
    doerfer = M.bot_doerfer_sicherstellen(bot)
    bot.doerfer = doerfer
    gs.bots = [bot]
    gs.settlements = [dorf, zweit]
    return gs, start, dorf, zweit, doerfer[0]


def main_() -> int:
    gs, START, dorf, zweit, botdorf = _aufbau()
    app = _App(gs)

    # -----------------------------------------------------------------------
    abschnitt("Uebersetzung Spielstand -> Felder")
    felder = app._portal_belegte_felder()
    arten = sorted({e["art"] for e in felder})
    check("nur das verortete Dorf und die Bot-Doerfer belegen Felder",
          len(felder) == 1 + len(M.bot_doerfer_sicherstellen(gs.bots[0])),
          "%d Eintraege, Arten %s" % (len(felder), arten))
    check("die noch nicht verortete Siedlung steht NICHT in der Karte",
          not any(e["name"] == "Eschenhain" for e in felder))
    check("das verortete Dorf steht an seinem Feld",
          any((e["name"], e["x"], e["y"]) == ("Zweithauch", 2, 2) for e in felder))
    check("das Bot-Dorf steht mit seiner festen Position drin",
          any((e["name"], e["x"], e["y"]) == (botdorf.name, botdorf.x, botdorf.y)
              for e in felder))

    # -----------------------------------------------------------------------
    abschnitt("Ein freies Feld: GENAU EINE Buchung")
    vorher = float(gs.resources["mana"].amount)
    kosten = float(P.wechselkosten())
    ok = app._dorf_versetzen("Eschenhain", 7, 12, START)
    check("der Umzug wird ausgefuehrt", ok is True, app.letzte_meldung())
    check("welt_x/welt_y stehen auf dem Zielfeld",
          (dorf.welt_x, dorf.welt_y) == (7, 12), str((dorf.welt_x, dorf.welt_y)))
    check("die Welt des Dorfes ist die Zielwelt", int(dorf.dimension) == START,
          str(dorf.dimension))
    check("die gezeigte Welt folgt dem Dorf", int(gs.eigene_dimension) == START,
          str(gs.eigene_dimension))
    check("GENAU der Festpreis ist abgebucht",
          abs(float(gs.resources["mana"].amount) - (vorher - kosten)) < 1e-6,
          "%g -> %g" % (vorher, gs.resources["mana"].amount))
    check("die Sperre ist gesetzt", gs.letzter_wechsel is not None, str(gs.letzter_wechsel))
    check("die Kennung bleibt unveraendert (W-1 entschaerft durch S-2)",
          dorf.id == "spieler:kontinent:3:3", dorf.id)
    check("die Siedlungskarte bleibt unberuehrt (x/y unveraendert)",
          (dorf.x, dorf.y) == (3, 3), str((dorf.x, dorf.y)))
    check("alles reist mit: Bauten und Garnison unveraendert (F-27 = A)",
          dorf.bauten == {"0": "dorfzentrum"} and dorf.garrison == {"bogenschuetze": 4},
          str((dorf.bauten, dorf.garrison)))
    check("die Meldung steht im Postfach und nennt das Feld",
          bool(app.portalmeldungen()) and "7/12" in app.letzte_meldung(),
          app.letzte_meldung())
    check("die Anzeige findet das Dorf jetzt auf dem neuen Feld (S-2)",
          app._ort_feld("Eschenhain", "", 20) == (7, 12),
          str(app._ort_feld("Eschenhain", "", 20)))
    check("das Dorf steht danach in der Belegungskarte",
          any((e["name"], e["x"], e["y"]) == ("Eschenhain", 7, 12)
              for e in app._portal_belegte_felder()))

    # -----------------------------------------------------------------------
    abschnitt("Die Sperre haelt den zweiten Sprung auf (bis S-5)")
    mana_nach = float(gs.resources["mana"].amount)
    zweiter = app._dorf_versetzen("Eschenhain", 8, 12, START)
    check("ein zweiter Umzug sofort wird abgelehnt", zweiter is False, app.letzte_meldung())
    check("die Meldung nennt die 24-Stunden-Regel", "Stunden" in app.letzte_meldung(),
          app.letzte_meldung())
    check("und es wurde nichts abgebucht",
          abs(float(gs.resources["mana"].amount) - mana_nach) < 1e-6,
          str(gs.resources["mana"].amount))
    check("und die Position ist unveraendert", (dorf.welt_x, dorf.welt_y) == (7, 12))

    # -----------------------------------------------------------------------
    abschnitt("Belegte Felder werden abgelehnt (F-26 = A)")
    gs.letzter_wechsel = None                                   # Sperre fuer diese Pruefungen weg
    bot_welt = int(getattr(botdorf, "dimension", 0) or START)
    belegt = app._dorf_versetzen("Eschenhain", int(botdorf.x), int(botdorf.y), bot_welt)
    check("ein Bot-Dorf blockiert sein Feld", belegt is False, app.letzte_meldung())
    check("der Grund nennt das Bot-Dorf", botdorf.name in app.letzte_meldung(),
          app.letzte_meldung())
    eigen = app._dorf_versetzen("Eschenhain", 2, 2, START)
    check("das Feld der EIGENEN zweiten Siedlung ist belegt", eigen is False,
          app.letzte_meldung())
    check("der Grund nennt das andere Dorf", "Zweithauch" in app.letzte_meldung(),
          app.letzte_meldung())
    gleich = app._dorf_versetzen("Eschenhain", 7, 12, START)
    check("das eigene Feld gilt nicht als belegt, wird aber als 'steht schon dort' abgelehnt",
          gleich is False and "steht bereits" in app.letzte_meldung(), app.letzte_meldung())

    # -----------------------------------------------------------------------
    abschnitt("Grenzen: Raster, Welt, Mana, laufende Auftraege, Name")
    gs.letzter_wechsel = None
    check("ein Feld ausserhalb des Rasters wird abgelehnt",
          app._dorf_versetzen("Eschenhain", 20, 0, START) is False, app.letzte_meldung())
    check("eine unbekannte Weltkarte wird abgelehnt",
          app._dorf_versetzen("Eschenhain", 1, 1, 9) is False, app.letzte_meldung())
    gs.resources["mana"].amount = 100.0
    knapp = app._dorf_versetzen("Eschenhain", 1, 1, START)
    check("zu wenig Mana wird abgelehnt", knapp is False, app.letzte_meldung())
    check("die Meldung nennt Soll und Ist", "5000" in app.letzte_meldung(),
          app.letzte_meldung())
    gs.resources["mana"].amount = 20000.0
    check("ein unbekannter Dorfname wird abgelehnt",
          app._dorf_versetzen("Gibt es nicht", 1, 1, START) is False, app.letzte_meldung())
    echt = app._unterwegs_anzahl
    app._unterwegs_anzahl = lambda: 1                            # ein Auftrag ist unterwegs
    laufend = app._dorf_versetzen("Eschenhain", 1, 1, START)
    app._unterwegs_anzahl = echt
    check("solange etwas unterwegs ist, reist das Dorf nicht", laufend is False,
          app.letzte_meldung())
    check("die Meldung nennt den Grund (Anhang 2)", "unterwegs" in app.letzte_meldung(),
          app.letzte_meldung())
    check("die Position ist nach allen Ablehnungen unveraendert",
          (dorf.welt_x, dorf.welt_y) == (7, 12), str((dorf.welt_x, dorf.welt_y)))

    # -----------------------------------------------------------------------
    abschnitt("Nach der Sperre: ein zweiter Umzug in eine ANDERE Welt")
    gs.letzter_wechsel = None
    ziel = next((int(P.nummer_von(d.get("kennung"))) for d in P.dimensionen()
                 if int(P.nummer_von(d.get("kennung"))) != START), 0)
    if ziel:
        frei_auf_ziel = None
        for x in range(20):
            for y in range(20):
                st = P.feld_status(P.index_von(ziel), x, y, app._portal_belegte_felder(),
                                   ausschluss="Eschenhain")
                if st.get("frei"):
                    frei_auf_ziel = (x, y)
                    break
            if frei_auf_ziel:
                break
        mana = float(gs.resources["mana"].amount)
        umzug = app._dorf_versetzen("Eschenhain", frei_auf_ziel[0], frei_auf_ziel[1], ziel)
        check("der Umzug in eine andere Welt gelingt", umzug is True, app.letzte_meldung())
        check("die Welt des Dorfes ist die neue", int(dorf.dimension) == ziel,
              str(dorf.dimension))
        check("wieder GENAU ein Festpreis abgebucht",
              abs(float(gs.resources["mana"].amount) - (mana - kosten)) < 1e-6,
              "%g -> %g" % (mana, gs.resources["mana"].amount))
        check("die neue Welt steht in eigene_dimensionen",
              ziel in [int(z) for z in gs.eigene_dimensionen], str(gs.eigene_dimensionen))
        check("die Kennung bleibt auch beim Weltwechsel stabil",
              dorf.id == "spieler:kontinent:3:3", dorf.id)

    return bericht()


if __name__ == "__main__":
    sys.exit(main_())
