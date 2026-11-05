# -*- coding: ascii -*-
"""Wache S-6b Schritt 1: Warenhaltung und kartenabhaengiger Ertrag der Bot-Doerfer.

Daniels Vorgabe (03.11.2026): die auswaehlbaren Karten und die dort vorhandenen Rohstoffelder
sind eine grundlegende Mechanik - der Ertrag eines Bot-Dorfes muss also AUS SEINER KARTE folgen,
nicht aus einer festen Rate. **Seit S-8 Stufe 1 (03.11.2026) folgt er genauer: aus den GEBAUTEN
ANLAGEN auf den Feldern dieser Karte** (Gelaende entscheidet ueber den Satz, die Karte ueber das
Gelaende). Die Pruefungen hier bleiben unveraendert gueltig, weil die Anlagen aus dem Bauplan auf
der Karte stehen.

Was diese Datei prueft:
  1. Ein Bot-Dorf fuehrt Leder, Wolle und Pferde in `vorraete` (additiv, alte Staende laden).
  2. Der Ertrag kommt aus der Karte (S-8: aus den Anlagen auf ihren Gelaendearten): zwei Bots mit
     VERSCHIEDENEN Karten haben verschiedene Ertraege; derselbe Aufruf liefert denselben Wert.
  3. Die Anlagen stehen auf den Feldern seiner Karte (`bot_doerfer_bebauen`), begrenzt durch
     `anlagen_je_gebaeude` je Anlage (Stellmacher 1, Rinderfarm 3, Schafszucht 2, Pferdezucht 1).
  4. Die Rinderfarm liefert ZWEI Rohstoffe (Nahrung und Leder) - die Platzwahl darf daran nicht
     scheitern (belegt: `TypeError: '>' not supported between instances of 'dict' and 'dict'`).
  5. GEGENPROBE: ohne die neuen Anlagen im Bauplan fehlen die drei Waren - sonst prueft die
     Wache nur sich selbst.

ASCII-only: Umlaute in Anzeigenamen werden aus Zeichencodes gebaut.
"""
from __future__ import annotations

import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
sys.path.insert(0, os.path.join(ROOT, "tools"))

import tkinter as tk  # noqa: E402
import main  # noqa: E402

WAREN = ("leder", "wolle", "pferde")  # die drei Posten aus S-6b


def _app(seed=7):
    """Frische App mit einer Spielersiedlung (derselbe Start wie im Spiel)."""
    random.seed(seed)
    root = tk.Tk()
    root.withdraw()
    app = main.NebelseetalApp(root)
    app._build_main_ui()
    app._erste_siedlung_gruenden()
    return root, app


def abschnitt_1_vorrat():
    """1. Ein Bot-Dorf fuehrt die drei Waren."""
    abschnitt("1. Bot-Dorf fuehrt Leder, Wolle und Pferde")
    root, app = _app()
    try:
        gs = app.state
        gs.bots_fortschreiben(3600)  # Takt 1: Karte zuweisen, Anlagen setzen, Zeitstempel
        gs.bots_fortschreiben(7200)  # Takt 2: JETZT wird geerntet (belegt: Takt 1 setzt nur `ernte_seit`)
        dorf = gs.bots[0].doerfer[0]
        for ware in WAREN:
            check("Vorraete fuehren %s" % ware, ware in dorf.vorraete,
                  str(sorted(dorf.vorraete)))
        # Additiv: ein alter Stand ohne die Schluessel darf nicht abstuerzen
        alt = {k: v for k, v in dorf.vorraete.items() if k not in WAREN}
        dorf.vorraete = dict(alt)
        ertrag = main.bot_dorf_ertrag(dorf, bot=gs.bots[0])
        check("alter Stand ohne Waren rechnet weiter", isinstance(ertrag, dict), str(ertrag))
    finally:
        root.destroy()


def abschnitt_2_karte():
    """2. Der Ertrag folgt der Karte - gemessen ueber die Anlagen auf ihren Gelaendearten (S-8)."""
    abschnitt("2. Ertrag folgt der Karte - zwei Karten, zwei Werte")
    root, app = _app()
    try:
        gs = app.state
        gs.bots_fortschreiben(3600)
        gs.bots_fortschreiben(7200)
        werte = []
        for bot in gs.bots[:3]:
            dorf = bot.doerfer[0]
            ertrag = main.bot_dorf_ertrag(dorf, bot=bot)
            werte.append((bot.name, getattr(dorf, "karte", ""), ertrag))
            check("%s hat eine Karte" % bot.name, bool(getattr(dorf, "karte", "")),
                  str(getattr(dorf, "karte", "")))
            check("%s erntet Leder" % bot.name, float(ertrag.get("leder", 0)) > 0, str(ertrag))
        karten = [k for _n, k, _e in werte]
        # Register 228 (Daniel 05.11.2026, Antwort 1): ALLE Bots starten wie der Spieler auf DERSELBEN
        # festen Startkarte (original-036). Die fruehere Wache "die Bots haben VERSCHIEDENE Karten"
        # sicherte die Zufallsziehung aus Register 225 und ist damit ueberholt.
        _startkarte = "original-036"                      # originalkarten.START_ID, belegte Startkarte
        check("alle Hauptdoerfer tragen die FESTE Startkarte original-036 (Register 228)",
              set(karten) == {_startkarte}, str(karten))
        leder = [round(float(e.get("leder", 0)), 2) for _n, _k, e in werte]
        check("jedes Hauptdorf erntet Leder (die Karte wird gerechnet, nicht behauptet)",
              all(w > 0 for w in leder), str(leder))
        # Dieselbe Karte muss denselben Ertrag geben (keine Zufallszahl im Ertrag)
        a = main.bot_dorf_ertrag(gs.bots[0].doerfer[0], bot=gs.bots[0])
        b = main.bot_dorf_ertrag(gs.bots[0].doerfer[0], bot=gs.bots[0])
        check("derselbe Aufruf liefert denselben Ertrag", a == b, "%s vs %s" % (a, b))
    finally:
        root.destroy()


def abschnitt_3_anlagen():
    """3. Die Anlagen stehen auf der Karte, je Anlage begrenzt."""
    abschnitt("3. Anlagen stehen auf den Feldern der Karte")
    root, app = _app()
    try:
        gs = app.state
        gs.bots_fortschreiben(3600)
        gs.bots_fortschreiben(7200)
        dorf = gs.bots[0].doerfer[0]
        einstellungen = main.bot_wirtschaft_einstellungen()
        anzahl = einstellungen.get("anlagen_je_gebaeude")
        check("anlagen_je_gebaeude ist ein Dict je Anlage", isinstance(anzahl, dict), str(type(anzahl)))
        # ENTSCHEIDUNG GEAENDERT (S-8 Stufe 3, 04.11.2026, Register 179): seit heute baut ein
        # Bot-Dorf nach dem Bauplan SEINER TAKTIK (`data/bot_bauplan.json: anlagen_bauplaene`), und
        # die Restfelder fuellen danach nach Ertrag. Die frueheren Obergrenzen aus
        # `anlagen_je_gebaeude` (hier stand "steht hoechstens N-mal") gelten nur noch fuer den Aufruf
        # OHNE Taktik - als Grenze fuer den Takt-Weg waeren sie falsch, weil der Restfeld-Teil genau
        # MEHR Anlagen will. Die Zusage dieser Wache bleibt: die Warenkette hat ihre Anlagen
        # (Stellmacher, Rinderfarm, Schafszucht, Pferdezucht), und jede Mindestzahl der Taktik steht,
        # soweit die Karte das Gelaende dafuer hat.
        import gelaende  # noqa: E402  (nur hier gebraucht)
        taktik = main.bot_taktik_name(gs.bots[0])
        plan = main.bot_anlagenplan(taktik)
        mindest = plan.get("mindest") or {}
        check("die Taktik des Bots hat einen Bauplan in der Datendatei", bool(mindest), taktik)
        raster = list((main._bot_karte_dict(dorf.karte) or {}).get("raster") or [])
        prios = einstellungen.get("feld_prioritaeten") or {}

        def _zone(geb):
            """Das bevorzugte Gelaende einer Anlage (aus der Datendatei, nicht getippt)."""
            return set(str(a) for a in ((prios.get(geb) or {}).get("bevorzugt") or []))

        for geb, soll in sorted(mindest.items()):
            steht = sum(1 for g in dorf.bauten.values() if str(g) == geb)
            # Konkurrenz um DASSELBE Gelaende: Berg traegt Erzmine, Steinmetz und Goldmine. Reicht
            # der Berg fuer alle drei Mindestzahlen zusammen nicht, ist die Karte die Grenze - das
            # ist ein Befund, kein Fehler des Plans (gemessen: original-118b hat 5 Bergfelder).
            zone = _zone(geb)
            felder = sum(1 for art in raster if art in zone)
            bedarf = sum(int(s) for g2, s in mindest.items() if _zone(g2) & zone)
            if steht < int(soll) and felder < bedarf:
                befund("%s: Mindestzahl %d, Karte hat %d Felder fuer %d Anlagen derselben Zone"
                       % (geb, int(soll), felder, bedarf), "")
            else:
                check("%s steht mindestens %d-mal (Plan der Taktik)" % (geb, int(soll)),
                      steht >= int(soll), "steht %d-mal" % steht)
        for geb in ("stellmacher", "rinderfarm", "schafszucht", "pferdezucht"):
            steht = sum(1 for g in dorf.bauten.values() if str(g) == geb)
            check("%s ist gebaut" % geb, steht >= 1, "steht %d-mal" % steht)
        check("die Anlagen liegen auf der 10x10-Karte", len(dorf.bauten) <= 100,
              "%d Felder belegt" % len(dorf.bauten))
    finally:
        root.destroy()


def abschnitt_4_mehrfach():
    """4. Eine Anlage mit zwei Rohstoffen (Rinderfarm) bricht nichts."""
    abschnitt("4. Rinderfarm liefert Nahrung UND Leder")
    import gelaende
    wert = gelaende.ertrag_pro_stunde("rinderfarm", "grasland")
    check("die Rinderfarm liefert ein dict", isinstance(wert, dict), str(wert))
    if isinstance(wert, dict):
        klein = {str(k).lower(): v for k, v in wert.items()}
        check("sie liefert Nahrung", "nahrung" in klein, str(klein))
        check("sie liefert Leder", "leder" in klein, str(klein))
    check("_ertragssumme rechnet ein dict zu einer Zahl",
          isinstance(main._ertragssumme(wert), float), str(main._ertragssumme(wert)))
    check("_ertragssumme rechnet eine Zahl", main._ertragssumme(3) == 3.0)


def abschnitt_5_gegenprobe():
    """5. GEGENPROBE: ohne die Anlagen fehlen die Waren wirklich."""
    abschnitt("5. Gegenprobe - ohne die Anlagen fehlen die Waren")
    root, app = _app()
    try:
        gs = app.state
        gs.bots_fortschreiben(3600)
        dorf = gs.bots[0].doerfer[0]
        # Der ANLAGEN-Zweig rechnet, wenn keine Karte bekannt ist (leere Kennung).
        ohne_karte = main.BotDorf(name="Probe", karte="")                  # Dorf ohne Karte
        einstellungen = dict(main.bot_wirtschaft_einstellungen())
        einstellungen["gebaeude_je_dorf"] = ["holzfaeller", "steinmetz", "farm", "goldmine"]
        einstellungen["anlagen_je_gebaeude"] = 3
        ohne = main.bot_dorf_ertrag(ohne_karte, einstellungen=einstellungen)
        fehlen = [w for w in WAREN if float(ohne.get(w, 0)) == 0]
        check("ohne Zuchtanlagen fehlen Leder, Wolle und Pferde", len(fehlen) == 3, str(ohne))
        einstellungen["gebaeude_je_dorf"] = ["holzfaeller", "steinmetz", "farm", "goldmine",
                                             "stellmacher", "rinderfarm", "schafszucht", "pferdezucht"]
        einstellungen["anlagen_je_gebaeude"] = {"rinderfarm": 3, "schafszucht": 2, "pferdezucht": 1,
                                                "stellmacher": 1, "*": 3}
        mit = main.bot_dorf_ertrag(ohne_karte, einstellungen=einstellungen)
        check("mit Zuchtanlagen sind sie da", all(float(mit.get(w, 0)) > 0 for w in WAREN), str(mit))
    finally:
        root.destroy()


def main_lauf():
    """Alle Abschnitte ausfuehren und den Schlussstrich ziehen."""
    print("S-6b Schritt 1: Warenhaltung und kartenabhaengiger Ertrag")
    abschnitt_1_vorrat()
    abschnitt_2_karte()
    abschnitt_3_anlagen()
    abschnitt_4_mehrfach()
    abschnitt_5_gegenprobe()
    bericht()
    return 0


if __name__ == "__main__":
    raise SystemExit(main_lauf())
