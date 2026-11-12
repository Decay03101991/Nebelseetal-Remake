# -*- coding: ascii -*-
"""Frage 2: die zweite Atemphase - 20 % unter halber Wache (Register 217, 05.11.2026).

Daniels Entscheidung: "20 % unter halber Wache ansetzen - vorher messen". Die Messung steht in
`docs/SPIELBALANCING_TEST.md` Abschnitt 10 und im Rohlauf
`docs/audits/drachen_balancing_zweite_phase_20261105.log`.

Was diese Datei beweist
-----------------------
1. Die Regel steht in den DATEN (`data/drachen.json` -> `verteidigung.zweite_phase`) und wird
   ueber EINE Lesestelle (`drachen.zweite_phase`) gelesen - keine Zahl im Code.
2. In der echten Schlacht (`kampf.fuehre_schlacht`) schlaegt die Phase GENAU EINMAL zu, und
   zwar erst, wenn die Wache unter die Haelfte gefallen ist; die Zahl der Getroffenen ist
   20 % der angetretenen Nahkaempfer.
3. Ohne Phase rechnet die Schlacht Zeile fuer Zeile wie vorher (gleicher Keim, gleiche Verluste,
   kein zusaetzlicher Schluessel im Ergebnis) - der Schalter ist echt und nicht nur ein Kommentar.
4. GEGENPROBE: mit Phase weichen Verluste und Ausgang ab; die Phase steht im Bericht.
5. Der Kampfweg im Spiel gibt die Regel mit (`main._drachen_kampf` -> `zweite_phase=`).

ASCII-only (Pruefdatei-Konvention): Umlaute nur als Escape.

Aufruf:  python -X utf8 tests/test_drachen_zweite_phase.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "quelltext"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['drachen', 'einheiten', 'kampf', 'main:*']
PRUEF_DATEN = ['drachen.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import drachen  # noqa: E402
import einheiten  # noqa: E402
import kampf  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
DRACHE = drachen.finde_id("drache_d02")
KRIEGER = next(n for n in einheiten.alle() if str(n).startswith("Krieger"))
KATAPULT = next(n for n in einheiten.alle() if str(n).startswith("Katapult"))


def _schlacht(truppen: dict, zweite_phase, saat: int = 4711, verteidiger: dict = None) -> dict:
    """Eine Drachenschlacht mit dem ECHTEN Kampfweg - gleicher Keim bei jedem Aufruf."""
    return kampf.fuehre_schlacht(
        dict(truppen), dict(verteidiger or drachen.verteidiger(DRACHE)), 0, 100.0,
        angreifer_karren={KATAPULT: int(truppen.get(KATAPULT, 0))} if truppen.get(KATAPULT) else None,
        forschung_angreifer={}, forschung_verteidiger={},
        rng=random.Random(saat), schwellen=drachen.schwellen(DRACHE),
        zweite_phase=zweite_phase)


def _verluste(ergebnis: dict) -> int:
    """Die eigenen Verluste einer Schlacht als eine Zahl."""
    return sum(int(v) for v in (ergebnis.get("verluste_angreifer") or {}).values())


def haupt() -> int:
    # ------------------------------------------------------------------ 1. Die Regel steht in den Daten
    abschnitt("1. Die Regel steht in data/drachen.json, nicht im Code")
    regeln = drachen.zweite_phase(DRACHE)
    check("1 jeder Drache kennt eine zweite Phase", bool(regeln), str(regeln))
    check("1 der Anteil ist 20 Prozent", float(regeln.get("atem_prozent") or 0) == 20.0,
          str(regeln.get("atem_prozent")))
    check("1 der Ausloeser ist die halbe Wache", float(regeln.get("unter_anteil") or 0) == 0.5,
          str(regeln.get("unter_anteil")))
    check("1 die Phase ist eingeschaltet", regeln.get("aktiv") is True, str(regeln.get("aktiv")))
    check("1 alle drei Drachen tragen die Regel",
          all(drachen.zweite_phase(e) for e in drachen.alle()),
          str([drachen.zweite_phase(e) for e in drachen.alle()]))
    check("1 ein Eintrag ohne Block liefert ein leeres dict",
          drachen.zweite_phase({"verteidigung": {}}) == {}, str(drachen.zweite_phase({"verteidigung": {}})))
    check("1 ein kaputter Eintrag stuerzt nicht",
          drachen.zweite_phase(None) == {} and drachen.zweite_phase("x") == {})
    check("1 der Kampfweg im Spiel gibt die Regel mit",
          "zweite_phase=drachen.zweite_phase(drache)" in TEXT_MAIN, "Aufruf in main.py")

    # ------------------------------------------------------------------ 2. Sie schlaegt genau einmal zu
    abschnitt("2. Genau EINMAL, erst unter der halben Wache, 20 Prozent der Nahkaempfer")
    truppen = {KRIEGER: 400, KATAPULT: 22}
    mit = _schlacht(truppen, regeln)
    zp = mit.get("zweite_phase") or {}
    check("2 die Phase wurde ausgeloest", zp.get("ausgeloest") is True, str(zp))
    fuss = 400
    erwartet = int(round(fuss * 20 / 100.0))
    check("2 die Getroffenen sind 20 Prozent der Nahkaempfer (%d)" % erwartet,
          int(zp.get("verluste") or 0) == erwartet, str(zp.get("verluste")))
    zeilen = [z for z in (mit.get("sequenzen") or []) if "Zweiter Feueratem" in str(z)]
    check("2 die Phase steht genau einmal im Kampfprotokoll", len(zeilen) == 1, str(len(zeilen)))
    check("2 das Protokoll nennt die halbe Wache", zeilen and "unter" in zeilen[0], str(zeilen))
    check("2 der Kampf ging trotzdem gewonnen", mit.get("ausgang") == "angreifer",
          str(mit.get("ausgang")))

    # ------------------------------------------------------------------ 3. Ohne Phase alles wie vorher
    abschnitt("3. Ohne Phase rechnet die Schlacht wie vorher (Schalter statt Behauptung)")
    ohne = _schlacht(truppen, None)
    leer = _schlacht(truppen, {})
    aus = _schlacht(truppen, {"atem_prozent": 20, "unter_anteil": 0.5, "aktiv": False})
    check("3 ohne Angabe gibt es keinen Phasen-Schluessel im Ergebnis",
          "zweite_phase" not in ohne, str(sorted(ohne)))
    check("3 ein leerer Block aendert nichts", "zweite_phase" not in leer)
    check("3 aktiv=false aendert nichts", "zweite_phase" not in aus)
    check("3 gleiche Verluste bei allen drei Aufrufen",
          _verluste(ohne) == _verluste(leer) == _verluste(aus),
          "%d / %d / %d" % (_verluste(ohne), _verluste(leer), _verluste(aus)))
    check("3 gleicher Ausgang bei allen drei Aufrufen",
          ohne.get("ausgang") == leer.get("ausgang") == aus.get("ausgang"))

    # ------------------------------------------------------------------ 4. Gegenprobe: messbar anders
    abschnitt("4. GEGENPROBE: mit Phase kosten dieselben Truppen mehr")
    check("4 mit Phase mehr eigene Verluste", _verluste(mit) > _verluste(ohne),
          "%d mit / %d ohne" % (_verluste(mit), _verluste(ohne)))
    check("4 der Unterschied ist die zweite Atemwelle",
          _verluste(mit) - _verluste(ohne) >= erwartet,
          "%+d eigene Verluste" % (_verluste(mit) - _verluste(ohne)))

    # ------------------------------------------------------------------ 5. Nicht ausgeloest, wenn sie nicht faellt
    abschnitt("5. Bleibt die Wache ueber der Haelfte, schlaegt nichts zu")
    # Eine ZEHNFACHE Wache: 2040 Verteidiger gegen 250 Krieger. Die Vorrunde wird bestanden
    # (750 SK gegen die Schwelle 700), aber die Wache faellt nicht unter die Haelfte.
    grosse_wache = {k: int(v) * 10 for k, v in drachen.verteidiger(DRACHE).items()}
    schwach = {KRIEGER: 250, KATAPULT: 22}
    proben = []
    gekaempft = []
    for saat in range(1200, 1212):                  # zwoelf Keime, nicht ein Gluecksfall
        r = _schlacht(schwach, regeln, saat=saat, verteidiger=grosse_wache)
        zp_ = r.get("zweite_phase") or {}
        proben.append(bool(zp_.get("ausgeloest")))
        gekaempft.append(bool(r.get("kampf_stattgefunden")))
    check("5 es wurde wirklich gekaempft (sonst waere die Probe wertlos)", all(gekaempft),
          "%d von %d" % (sum(gekaempft), len(gekaempft)))
    check("5 in diesen Laeufen wird die halbe Wache nicht erreicht",
          not any(proben), "%d von %d ausgeloest" % (sum(proben), len(proben)))

    befund("Die zweite Phase macht die Verluste VON DER TRUPPENGROESSE abhaengig (20 % je "
           "Gefecht): gemessen 162 -> 221 bei 300, 154 -> 228 bei 400, 154 -> 338 bei 1000. "
           "Der frueher belegte Satz 'die eigenen Verluste sind groessenunabhaengig' gilt damit "
           "nur noch ohne Phase.")

    return bericht()


if __name__ == "__main__":
    sys.exit(haupt())
