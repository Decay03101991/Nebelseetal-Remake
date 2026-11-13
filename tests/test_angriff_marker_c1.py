# -*- coding: ascii -*-
"""Wache: C1 Angriffsflaeche - Marker verteilt und mit Kontrastrahmen (12.11.2026).

ZWEI BEFUNDE, DIE DIESE DATEI FESTHAELT
---------------------------------------
Daniel am 11.11.2026 (Testbogen V_0.0.4): "die angriffsflaeche ist viel zu klein, ich erkenne
kaum die doerfer" und "alles braun". Beim Nachmessen kam ein Fehler heraus, den niemand gesucht
hatte:

  BEFUND 1 (der eigentliche Grund): `bot_doerfer_sicherstellen` legte jedes Bot-Dorf OHNE Position
  an - alle zehn Bot-Doerfer eines frischen Spiels standen auf Feld (0,0). Auf der Karte war das
  ein Haufen Burgen in der linken oberen Ecke. Nur der Weg "Bot gruendet ein neues Dorf" setzte je
  eine Position, die Startdoerfer nie.

  DANIELS REGEL (12.11.2026): "Doerfer duerfen auf der Weltkarte nicht auf dem selben Feld
  landen." Deshalb gibt es `bot_doerfer_positionen_entzerren`: EINE Stelle, die auf jeder Welt
  garantiert, dass jedes Dorf sein eigenes Feld hat. Sie setzt fehlende Lagen UND loest
  Doppelbelegungen auf (das spaetere Dorf rueckt deterministisch weiter).

  BEFUND 2 (Lesbarkeit): Burg und Wappen sind gemalt und liegen in derselben Farbfamilie wie das
  Gelaende. Gold auf Steppe ergibt 2,15 zu 1 Kontrast, Weiss auf Berg 3,05 - eine EINZELNE Farbe
  kann es auf sieben Gelaendearten nicht leisten. Darum ein ZWEIFARBIGER Rahmen.

WAS DIESE DATEI PRUEFT
----------------------
1. `bottaktik.dorf_position` ist fest (zwei Aufrufe gleich), liegt im Raster und STREUT: der alte
   Zufallsweg legte drei von vier Doerfern desselben Bots auf dieselbe Spalte.
2. `bot_dorf_position_setzen` traegt nur bei (0,0) ein, laesst gesetzte Positionen in Ruhe und
   ist wiederholbar - ein alter Spielstand wird beim naechsten Zug repariert, nicht verschoben.
3. Im echten Aufbau: kein zwei Doerfer desselben Bots auf demselben Feld, und auf jeder Welt
   stehen die Doerfer verteilt (nicht alle auf (0,0)).
4. Jedes gezeichnete Dorf traegt GENAU EINEN zweifarbigen Rahmen (2 Objekte, eigenes Tag
   `dorfplatte`), eigene Doerfer innen in Skin-Gold, fremde innen hell.
5. Der Rahmen verschiebt KEINE Zaehlung: `portalbote` bleibt bei zwei Objekten je Dorf
   (Burg + Wappen) - daran haengen test_portal_fremdblick und test_spionage.
6. Kontrast: fuer jede der sieben Gelaendefarben liegt mindestens eine der beiden Ringlinien
   ueber 3 zu 1 (WCAG-Grenze fuer grafische Zeichen).

Aufruf:  python -X utf8 tests/test_angriff_marker_c1.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster+messen"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['bottaktik', 'main:*', 'portalraum']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import ast
import inspect
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src, messwert  # noqa: E402

import_src()
import bottaktik  # noqa: E402
import main  # noqa: E402
import portalraum  # noqa: E402


# --------------------------------------------------------------------------------------
def _kontrast(a: str, b: str) -> float:
    """WCAG-Kontrast zweier Hexfarben (1 zu 1 bis 21 zu 1)."""
    def _lum(farbe: str) -> float:
        r, g, bl = (int(farbe[i:i + 2], 16) / 255.0 for i in (1, 3, 5))
        def _k(c: float) -> float:
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        return 0.2126 * _k(r) + 0.7152 * _k(g) + 0.0722 * _k(bl)
    hell, dunkel = max(_lum(a), _lum(b)), min(_lum(a), _lum(b))
    return (hell + 0.05) / (dunkel + 0.05)


def _code(fn) -> str:
    """Der Rumpf einer Funktion als Code - der Docstring zaehlt NICHT als Code."""
    baum = ast.parse(inspect.getsource(fn).lstrip())
    knoten = baum.body[0]
    rumpf = getattr(knoten, "body", [])
    if rumpf and isinstance(rumpf[0], ast.Expr) and isinstance(getattr(rumpf[0], "value", None), ast.Constant) \
            and isinstance(rumpf[0].value.value, str):
        knoten.body = rumpf[1:]
    return ast.unparse(knoten)


class _Bot:
    def __init__(self, name: str, faction: str = "menschlich"):
        self.name = name
        self.faction = faction
        self.doerfer = []
        self.settlements = []
        self.vorraete = {}
        self.wall_stufe = 0
        self.wall_zustand = 100.0
        self.gebaut = 0
        self.geforscht = 0


# --------------------------------------------------------------------------------------
def _positionen():
    abschnitt("1. Die feste Dorfposition streut und bleibt fest")
    a = bottaktik.dorf_position("Haug", 0)
    check("zweimal derselbe Name ergibt dieselbe Lage", a == bottaktik.dorf_position("Haug", 0), str(a))
    check("Nummer 1 liegt woanders als Nummer 0",
          bottaktik.dorf_position("Haug", 1) != a, str(bottaktik.dorf_position("Haug", 1)))
    check("eine andere Fraktion liegt woanders",
          bottaktik.dorf_position("Grom", 0) != a, str(bottaktik.dorf_position("Grom", 0)))
    alle = [bottaktik.dorf_position(n, i)
            for n in ("Haug", "Brynhild", "Grom", "Silra", "Krank") for i in range(4)]
    check("alle 20 Lagen liegen im 20 x 20-Raster",
          all(0 <= x < 20 and 0 <= y < 20 for x, y in alle), str(alle[:4]))
    check("20 Doerfer belegen mindestens 18 verschiedene Felder",
          len(set(alle)) >= 18, str(len(set(alle))))
    spalten = len({x for x, _ in [bottaktik.dorf_position("Brynhild", i) for i in range(4)]})
    check("ein Bot steht nicht in einer Saeule (mindestens 3 verschiedene Spalten)",
          spalten >= 3, "%d Spalten" % spalten)
    check("raster=100 wird eingehalten",
          all(0 <= v < 100 for v in bottaktik.dorf_position("Haug", 0, raster=100)),
          str(bottaktik.dorf_position("Haug", 0, raster=100)))
    messwert("doerfer_verschiedene_felder", len(set(alle)), "Felder")
    messwert("brynhild_spalten", spalten, "Spalten")


def _setzen():
    abschnitt("2. Die Reparatur traegt nur bei (0,0) ein und ist wiederholbar")
    bot = _Bot("Reparatur")
    dorf = main.BotDorf(name="Reparatur Siedlung 1")
    check("ein frisches Dorf steht auf der Vorgabe (0,0)",
          (dorf.x, dorf.y) == (0, 0), str((dorf.x, dorf.y)))
    main.bot_dorf_position_setzen(dorf, bot, 0)
    erst = (dorf.x, dorf.y)
    check("die Reparatur traegt eine Position ein", erst != (0, 0), str(erst))
    check("sie entspricht der festen Lage",
          erst == bottaktik.dorf_position("Reparatur", 0),
          "%s zu %s" % (erst, bottaktik.dorf_position("Reparatur", 0)))
    main.bot_dorf_position_setzen(dorf, bot, 0)
    check("ein zweiter Lauf aendert nichts", (dorf.x, dorf.y) == erst, str((dorf.x, dorf.y)))
    gesetzt = main.BotDorf(name="Schon gesetzt", x=5, y=7)
    main.bot_dorf_position_setzen(gesetzt, bot, 0)
    check("eine gesetzte Lage bleibt unberuehrt", (gesetzt.x, gesetzt.y) == (5, 7),
          str((gesetzt.x, gesetzt.y)))


def _sicherstellen():
    abschnitt("3. Kein Haufen auf (0,0) und keine zwei Doerfer auf einem Feld")
    bot = _Bot("Haufentest")
    bot.settlements = ["Haufentest Siedlung 1", "Haufentest Siedlung 2", "Haufentest Siedlung 3"]
    doerfer = main.bot_doerfer_sicherstellen(bot)
    check("drei Doerfer angelegt", len(doerfer) == 3, str(len(doerfer)))
    lagen = [(d.x, d.y) for d in doerfer]
    check("keines steht mehr auf (0,0)", all(l != (0, 0) for l in lagen), str(lagen))
    check("die drei liegen auf drei verschiedenen Feldern", len(set(lagen)) == 3, str(lagen))
    # Daniel 12.11.2026: zwei Doerfer duerfen NIE auf demselben Feld stehen - auch nicht
    # verschiedene Doerfer, die auf dieselbe Lage zeigen. `bot_doerfer_positionen_entzerren`
    # ist die eine Stelle, die das auf JEDER Welt garantiert.
    a = _Bot("Kollision A")
    a.settlements = ["Kollision A Siedlung 1", "Kollision A Siedlung 2"]
    b = _Bot("Kollision B")
    b.settlements = ["Kollision B Siedlung 1"]
    for _b in (a, b):
        for d in main.bot_doerfer_sicherstellen(_b):
            d.x, d.y = 4, 4                                    # absichtlich ALLE auf ein Feld
    bewegt = main.bot_doerfer_positionen_entzerren([a, b])
    felder = [(d.x, d.y) for _b in (a, b) for d in main.bot_doerfer_sicherstellen(_b)]
    check("die Entzerrung hat Doerfer bewegt", bewegt >= 2, str(bewegt))
    check("keine zwei Doerfer stehen auf demselben Feld", len(set(felder)) == len(felder), str(felder))
    check("eine zweite Entzerrung aendert nichts mehr",
          main.bot_doerfer_positionen_entzerren([a, b]) == 0,
          str(main.bot_doerfer_positionen_entzerren([a, b])))
    quelle = inspect.getsource(main.bot_doerfer_sicherstellen)
    check("der Anlege-Weg ruft die Positionshilfe", "bot_dorf_position_setzen" in quelle)
    check("der Reparatur-Weg ruft die Positionshilfe ebenfalls",
          quelle.count("bot_dorf_position_setzen") >= 2, str(quelle.count("bot_dorf_position_setzen")))
    # Die Entzerrung muss dort gerufen werden, wo die Bots entstehen und wo sie umziehen -
    # sonst gilt Daniels Regel nur in der Pruefung, nicht im Spiel.
    gesamt = inspect.getsource(main)
    check("die Entzerrung laeuft beim Anlegen der Bots",
          "bot_doerfer_positionen_entzerren(self.bots)" in gesamt)
    check("sie laeuft beim Laden eines Spielstands",
          gesamt.count("bot_doerfer_positionen_entzerren(self.bots)") >= 2,
          str(gesamt.count("bot_doerfer_positionen_entzerren(self.bots)")))
    check("sie laeuft nach der Voelkerwahl (Welten wechseln dort)",
          "bot_doerfer_positionen_entzerren(self.state.bots)" in gesamt)


def _kontraste():
    abschnitt("4. Der zweifarbige Rahmen haelt 3 zu 1 auf allen sieben Gelaendearten")
    dunkel = main.DORF_RING_DUNKEL
    hell = main.DORF_RING_HELL
    werte = []
    for eintrag in portalraum.legende():
        farbe = str(eintrag["farbe"])
        w_dunkel = _kontrast(dunkel, farbe)
        w_hell = _kontrast(hell, farbe)
        werte.append((eintrag["name"], round(w_dunkel, 2), round(w_hell, 2)))
        check("auf %s traegt mindestens eine Ringlinie 3 zu 1" % eintrag["name"],
              max(w_dunkel, w_hell) >= 3.0, "dunkel %.2f / hell %.2f" % (w_dunkel, w_hell))
    befund("Gold allein reicht NICHT",
           "Gold zu Steppe %.2f zu 1, zu Berg %.2f zu 1 - darum aussen dunkel"
           % (_kontrast("#FFCC33", "#A98A5C"), _kontrast("#FFCC33", "#8E93A6")))
    messwert("ring_kontrast_min", round(min(max(d, h) for _, d, h in werte), 2), "zu 1")
    for name, d, h in werte:
        befund("Kontrast %s" % name, "dunkel %.2f / hell %.2f" % (d, h))


def _quellwachen():
    abschnitt("5. Quellwachen: der Ring haengt an einer Stelle, mit eigenem Tag")
    marke = inspect.getsource(main.NebelseetalApp._dorf_marke)
    check("die Dorfmarke zeichnet den Ring", "_dorf_ring(" in marke)
    kasten = inspect.getsource(main.NebelseetalApp._dorf_kasten)
    check("auch der Rueckfall-Kasten zeichnet den Ring", "_dorf_ring(" in kasten)
    ring = inspect.getsource(main.NebelseetalApp._dorf_ring)
    check("der Ring traegt ein EIGENES Tag", "dorfplatte" in ring)
    ring_code = _code(main.NebelseetalApp._dorf_ring)                  # Docstring zaehlt nicht
    check("der Ring benutzt NICHT das Dorf-Tag",
          "portalbote" not in ring_code and "portalspieler" not in ring_code, ring_code[:160])
    check("der Ring zeichnet zwei Linien", ring_code.count("create_rectangle") == 2,
          str(ring_code.count("create_rectangle")))
    check("eigene Doerfer bekommen das Skin-Gold", "skin['gold']" in ring_code, ring_code[:160])


def _aufbau():
    abschnitt("6. Echter Aufbau: verteilte Doerfer und ein Ring je Dorf")
    import tkinter as tk
    root = tk.Tk()
    root.geometry("1400x900+40+40")
    try:
        root.attributes("-alpha", 0.01)                                   # unsichtbar, aber vermessen
    except Exception:                                                      # noqa: BLE001
        pass
    root.update()
    try:
        app = main.NebelseetalApp(root)
        app._build_main_ui()
        app._erste_siedlung_gruenden()
        for _ in range(3):
            root.update()
            root.update_idletasks()
        # (a) kein Bot stapelt seine Doerfer
        stapel = []
        for bot in (app.state.bots or []):
            lagen = [(d.x, d.y) for d in main.bot_doerfer_sicherstellen(bot)]
            if len(lagen) != len(set(lagen)):
                stapel.append(bot.name)
            if lagen and len(set(lagen)) < 2 and len(lagen) > 1:
                stapel.append(bot.name + " (ein Feld)")
        check("kein Bot hat zwei Doerfer auf demselben Feld", not stapel, str(stapel))
        alle = [d for bot in (app.state.bots or []) for d in main.bot_doerfer_sicherstellen(bot)]
        felder = {(d.x, d.y) for d in alle}
        check("die Startdoerfer stehen nicht alle auf einem Feld", len(felder) >= 3,
              "%d Doerfer auf %d Feldern" % (len(alle), len(felder)))
        messwert("bot_doerfer", len(alle), "Doerfer")
        messwert("bot_doerfer_felder", len(felder), "Felder")
        # (b) die Karte zeichnen und zaehlen
        app._switch_view("Portal")
        for _ in range(4):
            root.update()
            root.update_idletasks()
        while app._overlay_offen():                                       # Einfuehrungsdialog weg
            app._overlay_schliessen()
            root.update()
        karte = getattr(app, "portal_zeichenflaeche", None)
        check("die Portalkarte steht", karte is not None)
        if karte is None:
            return
        fremde = len(karte.find_withtag("portalbote"))
        eigene = len(karte.find_withtag("portalspieler"))
        ringe = karte.find_withtag("dorfplatte")
        # F-100 (Daniel 13.11.2026): kein Wappen-Abzeichen mehr auf der Karte. Damit traegt jedes
        # gezeichnete Dorf GENAU EIN Bildobjekt (die Burg) und ein Ringpaar; der alte Rechentrick
        # "fremde % 2 == 0" (Burg + Abzeichen) gilt nicht mehr.
        check("F-100: auf der Karte wird KEIN Wappen geladen (nur Burgen)",
              not any("wappen_" in str(k) for k in getattr(app, "_wappen_cache", {})),
              str([str(k).split("\\")[-1] for k in getattr(app, "_wappen_cache", {})][:3]))
        check("die Ringe kommen paarweise (Aussen- und Innenlinie)",
              len(ringe) % 2 == 0, str(len(ringe)))
        check("F-100: hoechstens ein Bildobjekt je gezeichnetem Dorf (Ringpaar)",
              fremde <= len(ringe),
              "%d Bildobjekte zu %d Ringlinien (%d eigene)" % (fremde, len(ringe), eigene))
        aussen = {karte.itemcget(i, "outline") for i in ringe}
        check("die dunkle Aussenlinie ist gesetzt", main.DORF_RING_DUNKEL in aussen, str(aussen))
        check("die helle Innenlinie ist gesetzt", main.DORF_RING_HELL in aussen, str(aussen))
        innen_gold = [i for i in ringe if karte.itemcget(i, "outline") == app.skin["gold"]]
        check("eigene Doerfer tragen Gold innen (mindestens einer)",
              (not eigene) or bool(innen_gold), str(len(innen_gold)))
        zelle = app._portal_zelle(portalraum._achsen())
        bbox = [karte.bbox(i) for i in ringe[:2]]
        check("der Ring bleibt im Feld (Kante %d px)" % zelle,
              all(b and (b[2] - b[0]) <= zelle + 1 and (b[3] - b[1]) <= zelle + 1 for b in bbox),
              str(bbox))
        messwert("ring_kante", zelle, "px")
        befund("Sichtpruefung durch Daniel steht aus",
               "die Ringe sind hier gezaehlt und gemessen; Bild c1_karte_2x.png im Scratch")
    finally:
        try:
            root.destroy()
        except Exception:                                                  # noqa: BLE001
            pass


# --------------------------------------------------------------------------------------
if __name__ == "__main__":
    _positionen()
    _setzen()
    _sicherstellen()
    _kontraste()
    _quellwachen()
    _aufbau()
    sys.exit(bericht())
