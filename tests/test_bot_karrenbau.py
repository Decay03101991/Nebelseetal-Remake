# -*- coding: ascii -*-
"""Wache S-6b Teil 2: Ein Bot baut seinen Siedlerkarren wie der Spieler.

Daniels Vorgabe (03.11.2026): "Ein bot muss genau wie der Spieler erstmal einen Siedlerkarren bauen
und die noetigen ressourcen haben bevor er gruenden kann genau wie der spieler mit der abweichung
das er ein bot ist."

Was diese Datei prueft:
  1. MIT Stellmacher, Wagenbau und genug Vorraten baut der Bot einen Karren - und die Vorraete
     sinken um GENAU die Kosten aus dem Kern.
  2. OHNE Wagenbau baut er keinen (Forschung ist Pflicht).
  3. OHNE Stellmacher baut er keinen (Werkstatt ist Pflicht).
  4. OHNE Vorrate baut er keinen und die Vorrate bleiben unangetastet.
  5. Die SIEDLER werden beim Bau NICHT abgezogen (sie steigen erst bei der Gruendung ein) -
     sonst zahlte ein Bot fuenf Siedler zweimal.
  6. Mit `siedlerkarren_pflicht: true` gruendet ein Bot ohne Karren NICHT.
  7. GEGENPROBE: die Kosten stammen aus dem Kern, nicht aus einer Zahl in dieser Datei.

ASCII-only: Umlaute in Anzeigenamen werden aus Zeichencodes gebaut.
"""
from __future__ import annotations

import io
import json
import os
import random
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
sys.path.insert(0, SRC)

import tkinter as tk  # noqa: E402
import main  # noqa: E402
import spieloekonomie  # noqa: E402

KARREN = "Siedlerkarren"                     # Schluessel im Kern (spieloekonomie.U)


def _app(seed=7):
    """Frische App mit einer Spielersiedlung."""
    random.seed(seed)
    root = tk.Tk()
    root.withdraw()
    app = main.NebelseetalApp(root)
    app._build_main_ui()
    app._erste_siedlung_gruenden()
    return root, app


def _dorf_mit_stellmacher(bot):
    """Ein Bot-Dorf, in dem ein Stellmacher steht (die Werkstatt ist Bedingung)."""
    dorf = bot.doerfer[0]
    dorf.bauten = dict(getattr(dorf, "bauten", None) or {})
    dorf.bauten[999] = spieloekonomie.U[KARREN]["gebaeude"]
    return dorf


def abschnitt_1_bauen():
    """1. Mit allen Bedingungen wird gebaut, die Kosten stimmen."""
    abschnitt("1. Karrenbau mit Stellmacher, Wagenbau und Vorrat")
    root, app = _app()
    try:
        gs = app.state
        bot = gs.bots[0]
        dorf = _dorf_mit_stellmacher(bot)
        bot.forschungsstaende = {"Wagenbau": 1}
        kosten = {k: float(v) for k, v in spieloekonomie.U[KARREN]["kosten"].items()
                  if k != "siedler"}                      # Siedler zaehlen hier nicht
        for stoff, menge in kosten.items():                # genug von allem
            dorf.vorraete[stoff] = menge + 100.0
        vorher = dict(dorf.vorraete)
        gebaut = gs.bot_karren_bauen(bot, dorf)
        check("mit Stellmacher, Wagenbau und Vorrat wird gebaut", gebaut is True, str(gebaut))
        check("der Karren steht im Dorf",
              int((dorf.einheiten or {}).get(KARREN, 0) or 0) == 1, str(dorf.einheiten))
        for stoff, menge in kosten.items():
            erwartet = round(vorher.get(stoff, 0.0) - menge, 2)
            check("die Kosten fuer %s werden gebucht" % stoff,
                  abs(float(dorf.vorraete.get(stoff, 0.0)) - erwartet) < 1e-6,
                  "%s statt %s" % (dorf.vorraete.get(stoff), erwartet))
    finally:
        root.destroy()


def abschnitt_2_ohne_forschung():
    """2. Ohne Wagenbau wird nicht gebaut."""
    abschnitt("2. Ohne Wagenbau kein Karren")
    root, app = _app()
    try:
        gs = app.state
        bot = gs.bots[0]
        dorf = _dorf_mit_stellmacher(bot)
        bot.forschungsstaende = {}                          # nichts erforscht
        for stoff in spieloekonomie.U[KARREN]["kosten"]:
            if stoff != "siedler":
                dorf.vorraete[stoff] = 9999.0
        check("ohne Wagenbau wird nicht gebaut", gs.bot_karren_bauen(bot, dorf) is False, "")
        check("der Vorrat bleibt unangetastet", float(dorf.vorraete["leder"]) == 9999.0,
              str(dorf.vorraete.get("leder")))
    finally:
        root.destroy()


def abschnitt_3_ohne_werkstatt():
    """3. Ohne Stellmacher wird nicht gebaut."""
    abschnitt("3. Ohne Stellmacher kein Karren")
    root, app = _app()
    try:
        gs = app.state
        bot = gs.bots[0]
        dorf = bot.doerfer[0]
        dorf.bauten = {i: g for i, g in (getattr(dorf, "bauten", None) or {}).items()
                       if str(g).strip().lower() != "stellmacher"}     # Werkstatt entfernen
        bot.forschungsstaende = {"Wagenbau": 1}
        for stoff in spieloekonomie.U[KARREN]["kosten"]:
            if stoff != "siedler":
                dorf.vorraete[stoff] = 9999.0
        check("ohne Stellmacher wird nicht gebaut", gs.bot_karren_bauen(bot, dorf) is False, "")
    finally:
        root.destroy()


def abschnitt_4_ohne_vorrat():
    """4. Ohne Vorrat wird nicht gebaut, nichts wird abgezogen."""
    abschnitt("4. Ohne Vorrat kein Karren")
    root, app = _app()
    try:
        gs = app.state
        bot = gs.bots[0]
        dorf = _dorf_mit_stellmacher(bot)
        bot.forschungsstaende = {"Wagenbau": 1}
        for stoff in spieloekonomie.U[KARREN]["kosten"]:
            if stoff != "siedler":
                dorf.vorraete[stoff] = 0.0                     # alles leer
        vorher = dict(dorf.vorraete)
        check("ohne Vorrat wird nicht gebaut", gs.bot_karren_bauen(bot, dorf) is False, "")
        check("nichts wird abgezogen", dorf.vorraete == vorher, str(dorf.vorraete))
    finally:
        root.destroy()


def abschnitt_5_siedler():
    """5. Die Siedler werden beim Bau NICHT abgezogen."""
    abschnitt("5. Siedler zahlen erst bei der Gruendung")
    root, app = _app()
    try:
        gs = app.state
        bot = gs.bots[0]
        dorf = _dorf_mit_stellmacher(bot)
        bot.forschungsstaende = {"Wagenbau": 1}
        dorf.bevoelkerung = 40.0
        for stoff in spieloekonomie.U[KARREN]["kosten"]:
            if stoff != "siedler":
                dorf.vorraete[stoff] = 9999.0
        gs.bot_karren_bauen(bot, dorf)
        check("die Siedler bleiben im Dorf", float(dorf.bevoelkerung) == 40.0, str(dorf.bevoelkerung))
    finally:
        root.destroy()


def abschnitt_6_pflicht():
    """6. Mit Karrenpflicht gruendet ein Bot ohne Karren nicht."""
    abschnitt("6. Karrenpflicht gilt")
    root, app = _app()
    try:
        gs = app.state
        bot = gs.bots[0]
        dorf = bot.doerfer[0]
        dorf.einheiten = {}                                # kein Karren da
        einstellungen = dict(main.bot_gruendung_einstellungen())
        check("die Pflicht ist eingeschaltet (Daniel 03.11.2026)",
              bool(einstellungen.get("siedlerkarren_pflicht")), str(einstellungen.get("siedlerkarren_pflicht")))
        vorher = len(bot.doerfer)
        gebaut = gs.bot_dorf_gruenden(bot, 7200.0)
        check("ohne Karren keine Gruendung", gebaut is None, str(gebaut))
        check("die Dorfzahl bleibt", len(bot.doerfer) == vorher, "%d -> %d" % (vorher, len(bot.doerfer)))
    finally:
        root.destroy()


def abschnitt_7_gegenprobe():
    """7. GEGENPROBE: die Kosten kommen aus dem Kern."""
    abschnitt("7. Gegenprobe - Kosten aus dem Kern")
    kern = spieloekonomie.U.get(KARREN) or {}
    check("der Karren steht im Kern", bool(kern), str(bool(kern)))
    check("er kostet Leder", "leder" in (kern.get("kosten") or {}), str(kern.get("kosten")))
    check("er kostet Wolle", "wolle" in (kern.get("kosten") or {}), str(kern.get("kosten")))
    check("er kostet Pferde", "pferde" in (kern.get("kosten") or {}), str(kern.get("kosten")))
    check("er braucht den Stellmacher", str(kern.get("gebaeude") or "") == "Stellmacher",
          str(kern.get("gebaeude")))
    regel = spieloekonomie.REGELN.get("gruendung") or {}
    check("die Gruendung verlangt Wagenbau", str(regel.get("forschung") or "") == "Wagenbau",
          str(regel.get("forschung")))


def main_lauf():
    """Alle Abschnitte ausfuehren und den Schlussstrich ziehen."""
    print("S-6b Teil 2: Siedlerkarren der Bots")
    abschnitt_1_bauen()
    abschnitt_2_ohne_forschung()
    abschnitt_3_ohne_werkstatt()
    abschnitt_4_ohne_vorrat()
    abschnitt_5_siedler()
    abschnitt_6_pflicht()
    abschnitt_7_gegenprobe()
    bericht()
    return 0


if __name__ == "__main__":
    raise SystemExit(main_lauf())
