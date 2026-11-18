# -*- coding: ascii -*-
"""Wache fuer C1: der Weltensprung kostet 500 Mana PLUS 100 Gold (Register 93/664).

WARUM ES DIESE WACHE GIBT
-------------------------
Daniel hat am 01.11.2026, 18:24 (Register 93) entschieden, dass der Weltensprung im Spiel
500 Mana plus 100 Gold kostet, damit ein Sprung in einer Partie erlebbar ist. Bis zum 18.11.2026
buchte der Code unveraendert den BELEGTEN Originalwert 5.000 Mana (portal.php 2005, Z. 25) und
gar kein Gold. Am 18.11.2026 hat Daniel den Einbau als erste Arbeit gewaehlt ("C1 zuerst").

Die vier Zusagen dieser Wache (so im Auftrag der Uebergabe gefordert):
  (a) der SPIELWERT ist 500 Mana + 100 Gold,
  (b) die 5.000 stehen WEITER in der Datendatei und sind als belegt gekennzeichnet,
  (c) nach einem Wechsel sind Mana UND Gold GENAU EINMAL gebucht,
  (d) ohne Gold gibt es keinen Wechsel, und die Meldung nennt den fehlenden Betrag.

Dazu die Quellwachen: EINE Buchstelle in `_dorf_versetzen`, der zweite Weg in `spielschicht`
bucht dasselbe, und keine der beiden Stellen rechnet den Preis selbst.

Aufruf: python -X utf8 tests/test_wechselpreis_spielwert.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
PRUEF_ART = "rechnen"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['main:*', 'portalraum', 'spielschicht']
PRUEF_DATEN = ['welten.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import inspect
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
os.chdir(SRC)

import main as M            # noqa: E402
import portalraum as P      # noqa: E402
import spielschicht as S    # noqa: E402

DATEN = json.load(open(os.path.join(ROOT, "data", "welten.json"), encoding="utf-8"))
KOORD = DATEN["belegte_regeln"]["koordinatenwechsel"]


class _App:
    """Stellvertreter ohne Fenster: bindet die ECHTEN Methoden der App an einen Spielstand."""

    _siedlung_nach_namen = M.NebelseetalApp._siedlung_nach_namen
    _unterwegs_anzahl = M.NebelseetalApp._unterwegs_anzahl
    _dorf_unterwegs = M.NebelseetalApp._dorf_unterwegs
    _portal_feld_bebaubar = M.NebelseetalApp._portal_feld_bebaubar
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


def _aufbau(mana=20000.0, gold=2000.0):
    """Ein Spielstand mit EINER verorteten Siedlung - ohne Fenster."""
    gs = M.GameState()
    start = int(gs.eigene_dimension)
    gs.resources["mana"].amount = float(mana)
    gs.resources["gold"].amount = float(gold)
    gs.letzter_wechsel = None
    dorf = M.Settlement(name="Eschenhain", map_id="kontinent", x=3, y=3,
                        id=M.siedlung_kennung("spieler", "kontinent", 3, 3),
                        dimension=start, welt_x=5, welt_y=5)
    gs.settlements = [dorf]
    gs.bots = []
    return gs, start, dorf


def _code(fn) -> str:
    """Der Quelltext einer Methode ohne Docstring - Kommentare zaehlen nicht als Code."""
    return inspect.getsource(fn)


# ===========================================================================
abschnitt("(a) Der Spielwert ist 500 Mana + 100 Gold")

check("wechselkosten() liefert 500", P.wechselkosten() == 500, str(P.wechselkosten()))
check("wechselkosten_gold() liefert 100", P.wechselkosten_gold() == 100,
      str(P.wechselkosten_gold()))
check("der Spielwert steht in data/welten.json (Block spielwert)",
      int(KOORD["spielwert"]["kosten_mana"]) == 500
      and int(KOORD["spielwert"]["kosten_gold"]) == 100, str(KOORD.get("spielwert")))
check("das Modul liest den Block (keine zweite Zahl im Code)",
      "spielwert" in inspect.getsource(P) and "_MANA_SPIEL" in inspect.getsource(P))
check("die Beschreibung nennt beide Preise",
      "500 Mana" in P.beschreibung() and "100 Gold" in P.beschreibung(), P.beschreibung())

# ===========================================================================
abschnitt("(b) Die belegten 5.000 bleiben stehen und sind als belegt gekennzeichnet")

check("kosten_mana steht weiter auf 5000", int(KOORD["kosten_mana"]) == 5000,
      str(KOORD.get("kosten_mana")))
check("der Beleg nennt das Original woertlich",
      "portal.php 2005" in str(KOORD.get("_belegt") or "")
      and "5.000 Mana" in str(KOORD.get("_belegt") or ""), str(KOORD.get("_belegt"))[:120])
check("der Spielwert ist als Entscheidung von Daniel gekennzeichnet",
      "Register 93" in str(KOORD["spielwert"].get("_entscheidung") or ""),
      str(KOORD["spielwert"].get("_entscheidung"))[:120])
check("wechselkosten_belegt() liefert weiter 5000", P.wechselkosten_belegt() == 5000,
      str(P.wechselkosten_belegt()))
check("der Docstring von wechselkosten() nennt die Entscheidung",
      "Register 93" in (P.wechselkosten.__doc__ or ""), (P.wechselkosten.__doc__ or "")[:80])

# ===========================================================================
abschnitt("(c) Mana UND Gold werden genau einmal gebucht")

_d = P.nach_wechsel(1000.0, 500.0, 12345.0)
check("Mana: 1000 minus 500 = 500", _d["mana"] == 500.0, str(_d["mana"]))
check("Gold: 500 minus 100 = 400", _d["gold"] == 400.0, str(_d["gold"]))
check("die Meldung des Buches nennt beide Preise",
      _d["kosten"] == 500 and _d["kosten_gold"] == 100, str(_d))
check("der Zeitstempel wird geschrieben", _d["letzter_wechsel"] == 12345.0)


def _wirft(fn):
    """True, wenn fn eine ValueError wirft."""
    try:
        fn()
    except ValueError:
        return True
    except Exception:                                   # noqa: BLE001
        return False
    return False


check("ohne genug Mana bucht nach_wechsel nichts (ValueError)",
      _wirft(lambda: P.nach_wechsel(499.0, 500.0, 0.0)) is True)
check("ohne genug Gold bucht nach_wechsel nichts (ValueError)",
      _wirft(lambda: P.nach_wechsel(1000.0, 99.0, 0.0)) is True)

# Der ECHTE Weg im Spielstand: ein Umzug ueber die EINE Buchstelle.
gs, START, dorf = _aufbau()
app = _App(gs)
mana_vorher = float(gs.resources["mana"].amount)
gold_vorher = float(gs.resources["gold"].amount)
umzug = app._dorf_versetzen("Eschenhain", 7, 12, START)
check("der Umzug wird ausgefuehrt", umzug is True, app.letzte_meldung())
check("Mana ist GENAU einmal gebucht (20000 minus 500)",
      abs(float(gs.resources["mana"].amount) - (mana_vorher - 500.0)) < 1e-9,
      str(gs.resources["mana"].amount))
check("Gold ist GENAU einmal gebucht (2000 minus 100)",
      abs(float(gs.resources["gold"].amount) - (gold_vorher - 100.0)) < 1e-9,
      str(gs.resources["gold"].amount))
check("die Meldung nennt Mana UND Gold",
      "500 Mana" in app.letzte_meldung() and "100 Gold" in app.letzte_meldung(),
      app.letzte_meldung())

# Der zweite Weg (Spielschicht) bucht dieselben zwei Werte.
zpo = S.neuer_zustand()
zpo["ressourcen"]["mana"] = 1000
zpo["ressourcen"]["gold"] = 500
ok, meldung = S.portalwechsel(zpo, 3, 0.0)
check("der Spielschicht-Weg gelingt", ok is True, meldung)
check("der Spielschicht-Weg bucht 500 Mana", zpo["ressourcen"]["mana"] == 500,
      str(zpo["ressourcen"]["mana"]))
check("der Spielschicht-Weg bucht 100 Gold", zpo["ressourcen"]["gold"] == 400,
      str(zpo["ressourcen"]["gold"]))

# ===========================================================================
abschnitt("(d) Ohne Gold kein Wechsel - die Meldung nennt den fehlenden Betrag")

erlaubt, meldung = P.wechsel_erlaubt(0, 1, 100000.0, 0.0)
check("ohne Gold lehnt der Kern ab", erlaubt is False, meldung)
check("die Meldung nennt Gold", "Gold" in meldung, meldung)
check("die Meldung nennt den fehlenden Betrag 100", "100" in meldung, meldung)

erlaubt2, meldung2 = P.wechsel_erlaubt(0, 1, 0.0, 100000.0)
check("ohne Mana lehnt der Kern ab", erlaubt2 is False, meldung2)
check("die Meldung nennt den fehlenden Manabetrag 500", "500" in meldung2, meldung2)
check("mit genau beiden Preisen ist der Wechsel erlaubt",
      P.wechsel_erlaubt(0, 1, 500.0, 100.0)[0] is True)

gs2, START2, dorf2 = _aufbau(mana=20000.0, gold=50.0)
app2 = _App(gs2)
ohne = app2._dorf_versetzen("Eschenhain", 7, 12, START2)
check("im Spiel wird der Umzug ohne Gold abgelehnt", ohne is False, app2.letzte_meldung())
check("die Spielmeldung nennt Gold und den Betrag",
      "Gold" in app2.letzte_meldung() and "100" in app2.letzte_meldung(),
      app2.letzte_meldung())
check("ohne Gold wird KEIN Mana abgebucht",
      float(gs2.resources["mana"].amount) == 20000.0, str(gs2.resources["mana"].amount))
check("ohne Gold bleibt das Dorf am alten Feld",
      (dorf2.welt_x, dorf2.welt_y) == (5, 5), str((dorf2.welt_x, dorf2.welt_y)))

# ===========================================================================
abschnitt("Quellwachen: EINE Buchstelle, keine zweite Preistafel, Anzeige nennt beide Preise")

leib = _code(M.NebelseetalApp._dorf_versetzen)
check("_dorf_versetzen bucht ueber nach_wechsel", "nach_wechsel(" in leib)
check("_dorf_versetzen bucht genau EINMAL", leib.count("nach_wechsel(") == 1,
      str(leib.count("nach_wechsel(")))
check("_dorf_versetzen liest den Goldpreis aus dem Portalmodul",
      "wechselkosten_gold(" in leib)
check("_dorf_versetzen rechnet den Preis NICHT selbst (keine Zahl 5000 mehr)",
      "5000" not in leib, "%d Treffer fuer 5000 im Rumpf" % leib.count("5000"))
schicht = _code(S.portalwechsel)
check("der Spielschicht-Weg bucht ueber nach_wechsel", "nach_wechsel(" in schicht)
check("der Spielschicht-Weg braucht den Goldwert",
      "wechsel_erlaubt(von, nach_dimension, mana, gold)" in schicht)
ansicht = _code(M.NebelseetalApp._render_portal)
check("die Portalansicht zeigt den Goldpreis", "wechselkosten_gold(" in ansicht)
# Der Sperrgrund im Fenster heisst "Gold noetig" - das o mit Umlaut, hier als Escape geschrieben,
# weil jede Pruefdatei ASCII-only sein muss.
check("die Portalansicht sperrt ohne Gold mit Grund", "Gold n\u00f6tig" in ansicht,
      ansicht[-200:])

sys.exit(bericht())
