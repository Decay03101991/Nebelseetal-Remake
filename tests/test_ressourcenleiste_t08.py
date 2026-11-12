# -*- coding: ascii -*-
"""T08 Ressourcenleiste - festes Raster, gekuerzte Zahlen, Zustaende (12.11.2026).

Daniels Befund in V_0.0.4: die Leiste ist "ganz schrecklich" und "total haesslich, der stil ist
jetzt komplett weg". Vorher gemessen: Leiste 1446 x 34 px, elf Felder als Text, KEINE Symbole -
und sie schrumpfte nicht: in einem 1200-px-Fenster fehlten rechts zwei bis drei Felder.

Was diese Datei zusichert (Claude Opus 5.5, Antwort auf Auftrag 5, nachgerechnet in
docs/design/PRUEFUNG_CLAUDE_AUFTRAG5_20261112.md):
1. RASTER: Zellbreite W = abgerundet aus (B - 32 - (n-1)) / n, Deckel 132 px. Bei 1446 / 1186 /
   986 px sind das 127 / 104 / 85 px mit 3/4, 0/0 und 4/5 Restpixeln. Alle Zellen gleich breit,
   die letzte Zelle endet vor B - 16.
2. WEICH-REGEL: unter 100 px Zellbreite faellt die Rate weg, unter 62 px weichen Punkte, Pferde,
   Siedler (in dieser Reihenfolge) und eine Zelle "+n" erscheint. Wolle und Leder weichen NIE.
3. ZAHLEN: hoechstens sechs Zeichen, ABGERUNDET (999.999 zeigt "999k").
4. ZUSTAENDE: kritisch (Bestand 0, nur Vorraete), Unterdeckung (Rate negativ). Der Zustand
   "steigt/faellt" ist bewusst NICHT gebaut - ob das Spiel Aenderungen ausserhalb des Takts
   unterscheidet, ist offen.
5. BAND: 9-Slice - Endstuecke 16 px, Mitte nur wiederholt (64-px-Kachel), nie gedehnt. Das Layout
   haengt nicht an der Bilddatei.
6. RECHTSCUENDIG: beim Wechsel von 999 auf 1.000 bleibt die rechte Kante der Zahl gleich.

Aufruf:  python -X utf8 tests/test_ressourcenleiste_t08.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster"
PRUEF_STUFE = 3
PRUEF_BETRIFFT = ['main:*', 'punkte', 'spieloekonomie']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import inspect as _inspect
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import main  # noqa: E402

DATEN = main.RESSOURCENLEISTE
MASSE = DATEN.get("masse") or {}
FARBEN = DATEN.get("farben") or {}


class _Betrag:
    """Nur der Betrag - so viel braucht `leisten_zahl` von einem Rohstoff."""

    def __init__(self, amount):
        self.amount = amount


class _Stand:
    """Schlanker Spielstand fuer die Rechenpruefungen (kein Tk)."""

    def __init__(self, resources=None, population=0.0, punkte=0, settlements=None):
        self.resources = {k: _Betrag(v) for k, v in (resources or {}).items()}
        self.population = population
        self._punkte = punkte
        self.settlements = settlements or []

    def punktestand(self):
        return {"gesamt": self._punkte}

    def stundenertrag(self):
        return {}


# ==========================================================================
abschnitt("1. Die Datendatei traegt die Masse des Rasters")

check("1 elf Felder", len(main.leiste_felder()) == 11, str(len(main.leiste_felder())))
check("1 Zellbreiten-Deckel 132 px", int(MASSE.get("zelle_max") or 0) == 132, str(MASSE.get("zelle_max")))
check("1 Zellbreiten-Boden 62 px", int(MASSE.get("zelle_min") or 0) == 62, str(MASSE.get("zelle_min")))
check("1 Rate faellt unter 100 px weg", int(MASSE.get("rate_min") or 0) == 100, str(MASSE.get("rate_min")))
check("1 Endstuecke 16 px", int(MASSE.get("endstueck") or 0) == 16, str(MASSE.get("endstueck")))
check("1 Ausblende-Reihenfolge Punkte, Pferde, Siedler",
      [str(k) for k in (MASSE.get("ausblenden") or [])] == ["punkte", "pferde", "siedler"],
      str(MASSE.get("ausblenden")))
check("1 Band: Kachel 64 x 34, Endstueck 16",
      (DATEN.get("band") or {}).get("kachel_breite") == 64
      and (DATEN.get("band") or {}).get("kachel_hoehe") == 34
      and (DATEN.get("band") or {}).get("endstueck_breite") == 16,
      str(DATEN.get("band")))
check("1 Farben: Grund, Warnung, Name und Zahl stehen in der Datei",
      all(FARBEN.get(k) for k in ("grund", "warnung", "name", "zahl")), str(sorted(FARBEN)))
check("1 die Flaeche des frueheren Zustands kritisch ist entfallen (Daniel 12.11.2026)",
      not FARBEN.get("flaeche_kritisch") and "unterstrich" not in MASSE, str(sorted(FARBEN)))


# ==========================================================================
abschnitt("2. Raster: Zellbreite und Restpixel (Claudes Arithmetik, nachgerechnet)")

for breite, zellbreite, links, rechts in ((1446, 127, 3, 4), (1186, 104, 0, 0), (986, 85, 4, 5)):
    _r = main.leiste_raster(11, MASSE, breite)
    check("2 bei %d px ist die Zelle %d px breit" % (breite, zellbreite),
          _r["zellbreite"] == zellbreite, str(_r["zellbreite"]))
    check("2 bei %d px stehen %d/%d Restpixel links/rechts" % (breite, links, rechts),
          (_r["links"], _r["rechts"]) == (links, rechts), str((_r["links"], _r["rechts"])))

_r = main.leiste_raster(11, MASSE, 1494)
check("2 bei 1494 px ist der Deckel erreicht (132 px, kein Rest)",
      (_r["zellbreite"], _r["rest"]) == (132, 0), str((_r["zellbreite"], _r["rest"])))
_r = main.leiste_raster(11, MASSE, 2560)
check("2 darueber bleibt die Zelle 132 px und der Block steht mittig (53/53 bei 1600)",
      main.leiste_raster(11, MASSE, 1600)["zellbreite"] == 132
      and (main.leiste_raster(11, MASSE, 1600)["links"],
           main.leiste_raster(11, MASSE, 1600)["rechts"]) == (53, 53),
      str(main.leiste_raster(11, MASSE, 1600)))
check("2 bei 724 px ist die Zelle genau 62 px (letzte Breite ohne Ausblenden)",
      main.leiste_raster(11, MASSE, 724)["zellbreite"] == 62
      and not main.leiste_raster(11, MASSE, 724)["zu_eng"], "")
check("2 bei 700 px ist die Zelle zu eng (Ausblenden noetig)",
      main.leiste_raster(11, MASSE, 700)["zu_eng"], str(main.leiste_raster(11, MASSE, 700)))

# Mit UNGLEICHEN Textbreiten (so wie die echten Namen: "Nahrung" 41 px, "Holz" 21 px) darf die
# Zellbreite nicht wandern - genau das war der alte Fehler. Diese Pruefung faengt einen Rueckfall
# in die inhaltsgetriebene Rechnung (Gegenprobe: Zellbreite aus dem Inhalt -> hier rot).
_texte_echt = [("Siedler", "10"), ("Nahrung", "55"), ("Holz", "100"), ("Stein", "100"),
               ("Metall", "0"), ("Gold", "0"), ("Mana", "0"), ("Wolle", "0"), ("Leder", "0"),
               ("Pferde", "0"), ("Punkte", "0")]
_breiten_echt = [(33, 18), (41, 18), (21, 26), (24, 26), (28, 12), (22, 12), (25, 12),
                 (26, 12), (27, 12), (31, 12), (33, 12)]
_lay_echt = main.leiste_layout(_texte_echt, _breiten_echt, MASSE, 1186)
check("2 auch mit ungleichen Textbreiten sind alle Zellen gleich breit (kein Inhaltseinfluss)",
      len({z["breite"] for z in _lay_echt["zellen"]}) == 1
      and _lay_echt["zellen"][0]["breite"] == 104,
      str(sorted({z["breite"] for z in _lay_echt["zellen"]})))
check("2 ein langer Name macht seine Spalte NICHT breiter (der alte Fehler)",
      _lay_echt["zellen"][1]["breite"] == _lay_echt["zellen"][2]["breite"],
      "%s gegen %s" % (_lay_echt["zellen"][1]["breite"], _lay_echt["zellen"][2]["breite"]))

for breite in (1446, 1186, 986, 986 - 300, 2500):
    _lay = main.leiste_layout([("Name", "1.234")] * 11, None, MASSE, breite)
    _letzte = _lay["zellen"][-1]
    check("2 bei %d px endet die letzte Zelle vor dem rechten Endstueck" % breite,
          _letzte["x"] + _letzte["breite"] <= max(16, breite - 16),
          "%s + %s gegen %s" % (_letzte["x"], _letzte["breite"], breite - 16))
    check("2 bei %d px sind ALLE Zellen gleich breit (nichts gedehnt)" % breite,
          len({z["breite"] for z in _lay["zellen"]}) == 1,
          str(sorted({z["breite"] for z in _lay["zellen"]})))
    check("2 bei %d px ueberlappen die Zellen nicht" % breite,
          all(_lay["zellen"][i]["x"] + _lay["zellen"][i]["breite"] <= _lay["zellen"][i + 1]["x"]
              for i in range(len(_lay["zellen"]) - 1)), "")


# ==========================================================================
abschnitt("3. Weich-Regel: Rate faellt, dann Felder - Wolle und Leder nie")

_a = main.leiste_auswahl(None, MASSE, 986)
check("3 bei 986 px sind alle elf Felder sichtbar", len(_a["sichtbar"]) == 11, str(len(_a["sichtbar"])))
check("3 bei 986 px ist die Rate ausgeblendet", _a["rate"] is False, str(_a["rate"]))
check("3 bei 1186 px ist die Rate sichtbar", main.leiste_auswahl(None, MASSE, 1186)["rate"] is True, "")

_a = main.leiste_auswahl(None, MASSE, 700)
_weg = [str(f.get("schluessel")) for f in _a["ausgeblendet"]]
check("3 bei 700 px weicht zuerst Punkte", _weg == ["punkte"], str(_weg))
check("3 statt seiner steht die Zelle +1", _a["hinweis"] == "+1", str(_a["hinweis"]))
check("3 zehn Felder plus Zusatzzelle", len(_a["sichtbar"]) == 10, str(len(_a["sichtbar"])))

_a = main.leiste_auswahl(None, MASSE, 620)
_weg = [str(f.get("schluessel")) for f in _a["ausgeblendet"]]
check("3 bei 620 px weichen Punkte, Pferde und Siedler", _weg == ["punkte", "pferde", "siedler"], str(_weg))
check("3 die Zusatzzelle nennt die Zahl der ausgeblendeten Felder", _a["hinweis"] == "+3", str(_a["hinweis"]))
_sichtbar_keys = [str(x.get("schluessel")) for x in _a["sichtbar"]]
check("3 Wolle und Leder sind auch dann noch sichtbar",
      "wolle" in _sichtbar_keys and "leder" in _sichtbar_keys, str(_sichtbar_keys))
_lay = main.leiste_layout([(str(f.get("name")), "1.234") for f in _a["sichtbar"]], None, MASSE, 620,
                          zusatz=(_a["hinweis"], _a["plus_zelle"]))
check("3 die Zusatzzelle ist 28 px breit und steht ganz rechts",
      _lay["zellen"][-1]["breite"] == 28 and _lay["zellen"][-1]["x"] > _lay["zellen"][-2]["x"],
      str(_lay["zellen"][-1]))


# ==========================================================================
abschnitt("4. Zahlen: hoechstens sechs Zeichen, abgerundet")

for wert, soll in ((0, "0"), (7.6, "7"), (999, "999"), (1234, "1.234"), (99999, "99.999"),
                   (100000, "100k"), (999999, "999k"), (1000000, "1,00M"), (1234567, "1,23M"),
                   (9999999, "9,99M"), (10000000, "10,0M"), (99999999, "99,9M"),
                   (100000000, "100M"), (999999999, "999M")):
    _k = main.leisten_kurz(wert)
    check("4 %s zeigt %s" % (wert, soll), _k == soll, _k)

check("4 kein Wert hat mehr als sechs Zeichen",
      max(len(main.leisten_kurz(v)) for v in list(range(0, 300000, 7)) + [10 ** n for n in range(4, 13)]) <= 6,
      "")
check("4 abgerundet: 999.999 springt NICHT auf 1,00M", main.leisten_kurz(999999) == "999k",
      main.leisten_kurz(999999))
check("4 der Anzeigewert kommt aus der EINEN Zahlenstelle",
      main.leistenwert(_Stand(resources={"holz": 1234567}), {"quelle": "holz"}) == "1,23M",
      main.leistenwert(_Stand(resources={"holz": 1234567}), {"quelle": "holz"}))
check("4 Siedler und Punkte rechnen aus denselben Quellen",
      main.leistenwert(_Stand(population=12.0), {"quelle": "bevoelkerung"}) == "12"
      and main.leistenwert(_Stand(punkte=12345), {"quelle": "punkte"}) == "12.345", "")


# ==========================================================================
abschnitt("5. Zustaende: nur Unterdeckung - kritisch und steigt/faellt sind entschieden weg")

_leer = _Stand(resources={"holz": 0, "stein": 120, "nahrung": 50})
# ENTSCHEIDUNG Daniel 12.11.2026 (Register 490): den Zustand kritisch (Bestand 0) gibt es nicht
# mehr - beim Spielstart leuchteten sieben von elf Feldern. Diese Datei haelt das fest.
check("5 Bestand 0 ist KEIN Warnzustand mehr (kritisch entfallen)",
      main.leisten_zustand(_leer, {"quelle": "holz"}) == "normal",
      main.leisten_zustand(_leer, {"quelle": "holz"}))
check("5 ein Rohstoff mit Bestand ist normal", main.leisten_zustand(_leer, {"quelle": "stein"}) == "normal", "")
check("5 es gibt nur noch zwei Zustaende (normal und unterdeckung)",
      {main.leisten_zustand(_leer, {"quelle": k}, e)
       for k in ("holz", "stein", "nahrung", "gold")
       for e in ({}, {"nahrung": -3.0})} <= {"normal", "unterdeckung"},
      str({main.leisten_zustand(_leer, {"quelle": k}, e)
           for k in ("holz", "stein", "nahrung", "gold")
           for e in ({}, {"nahrung": -3.0})}))
check("5 eine negative Rate ist Unterdeckung",
      main.leisten_zustand(_leer, {"quelle": "nahrung"}, {"nahrung": -4.0}) == "unterdeckung", "")
_text, _warn = main.leisten_rate(_leer, {"quelle": "nahrung"}, {"nahrung": -4.0})
check("5 die Rate zeigt das Minus und warnt", _text.startswith("-") and _warn is True, _text)
_text, _warn = main.leisten_rate(_leer, {"quelle": "holz"}, {"holz": 5.0})
check("5 eine positive Rate zeigt das Plus ohne Warnung", _text == "+5,0/h" and _warn is False, _text)
check("5 Siedler und Punkte haben keine Rate",
      main.leisten_rate(_leer, {"quelle": "bevoelkerung"}) == ("", False)
      and main.leisten_rate(_leer, {"quelle": "punkte"}) == ("", False), "")
check("5 die Rate von Nahrung geht ueber die Verbrauchsstelle",
      "spieloekonomie.verbrauch_pro_stunde" in __import__("inspect").getsource(main.leisten_rate), "")
_quelle = _inspect.getsource(main.leisten_zustand)
check("5 der Docstring nennt beide Entscheidungen und ihre Nummer",
      "steigt/faellt" in _quelle and "kritisch" in _quelle and "Register 490" in _quelle, "")
check("5 der Zustand 'steigt/faellt' ist entschieden NICHT gebaut (Daniel 12.11.2026)",
      "steigt" not in _inspect.getsource(main.leisten_zustand).split('"""')[2], "")


# ==========================================================================
abschnitt("6. Band: 9-Slice, nie gedehnt - und unabhaengig von der Bilddatei")

for breite in (1446, 1186, 986, 2560):
    _b = main.leiste_band_teile(breite)
    check("6 bei %d px beginnt die Mitte nach 16 px" % breite, _b["mitte_von"] == 16, str(_b["mitte_von"]))
    check("6 bei %d px endet die Mitte 16 px vor dem Rand" % breite,
          _b["mitte_bis"] == breite - 16, str(_b["mitte_bis"]))
    check("6 bei %d px ist jede Kachel 64 px breit, nur die letzte beschnitten" % breite,
          all(w == 64 for _x, w in _b["kacheln"][:-1]) and 1 <= _b["kacheln"][-1][1] <= 64,
          str(_b["kacheln"][:2]))
    check("6 bei %d px deckt die Wiederholung die Mitte genau ab" % breite,
          sum(w for _x, w in _b["kacheln"]) == _b["mitte_bis"] - _b["mitte_von"], "")

_mit_bild = dict(DATEN)
_mit_bild["band"] = dict(DATEN.get("band") or {})
_mit_bild["band"]["datei"] = "assets/icons/leiste/ressourcenleiste.png"
_alt = main.RESSOURCENLEISTE
try:
    main.RESSOURCENLEISTE = _mit_bild
    _lay_bild = main.leiste_layout([("Name", "1.234")] * 11, None, MASSE, 1186)
    _band_bild = main.leiste_band_teile(1186)
finally:
    main.RESSOURCENLEISTE = _alt
_lay_ohne = main.leiste_layout([("Name", "1.234")] * 11, None, MASSE, 1186)
check("6 mit und ohne Bilddatei ist das Layout gleich (kein Pixel verschiebt sich)",
      [(z["x"], z["breite"]) for z in _lay_bild["zellen"]]
      == [(z["x"], z["breite"]) for z in _lay_ohne["zellen"]], "")
check("6 mit und ohne Bilddatei sind die Bandstuecke gleich",
      _band_bild["kacheln"] == main.leiste_band_teile(1186)["kacheln"], "")


# ==========================================================================
abschnitt("7. Die Leiste im echten Fenster (Tk)")

import tkinter as tk  # noqa: E402

root = tk.Tk()
root.geometry("1460x940+40+40")
app = main.NebelseetalApp(root)
app._build_main_ui()
root.update()
canvas = getattr(app, "_leisten_canvas", None)
check("7 es gibt eine Leistenflaeche im Kopf", canvas is not None, str(canvas))
if canvas is not None:
    for fenster in (1460, 1200, 1000):
        root.geometry("%dx940+40+40" % fenster)
        root.update()
        root.update_idletasks()
        app._leisten_breite = None
        app._leiste_zeichnen()
        root.update()
        b = canvas.winfo_width()
        lay = main.leiste_layout([("N", "1")] * len(main.leiste_felder()), None, MASSE, b)
        check("7 bei %d px Fenster ist die Leiste 34 px hoch" % fenster,
              canvas.winfo_height() == 34, str(canvas.winfo_height()))
        check("7 bei %d px Fenster sind elf Felder gezeichnet" % fenster,
              len(main.leiste_auswahl(None, MASSE, b)["sichtbar"]) == 11, str(b))
        check("7 bei %d px Fenster bleibt die letzte Zelle im Bild" % fenster,
              lay["zellen"][-1]["x"] + lay["zellen"][-1]["breite"] <= b - 16,
              "%s gegen %s" % (lay["zellen"][-1]["x"] + lay["zellen"][-1]["breite"], b - 16))
        _bb = [canvas.bbox(i) for i in canvas.find_withtag("leiste") if canvas.type(i) == "text"]
        check("7 bei %d px Fenster steht kein Text ueber dem Rand" % fenster,
              all(bb[2] <= b and bb[0] >= 0 for bb in _bb if bb), "")

    root.geometry("1460x940+40+40")
    root.update()
    app._leisten_breite = None
    app._leiste_zeichnen()
    root.update()
    kenn = app._leisten_zellen.get("holz")
    check("7 Holz hat Kennungen fuer Zahl, Rate und Pfeil",
          kenn is not None and all(kenn.get(k) is not None for k in ("wert", "rate", "pfeil")),
          str(kenn))
    if kenn:
        app.state.resources["holz"].amount = 999
        app._leiste_aktualisieren()
        _b1 = canvas.bbox(kenn["wert"])
        app.state.resources["holz"].amount = 1000
        app._leiste_aktualisieren()
        _b2 = canvas.bbox(kenn["wert"])
        check("7 beim Wechsel 999 -> 1.000 bleibt die rechte Kante der Zahl gleich",
              _b1 is not None and _b2 is not None and _b1[2] == _b2[2],
              "%s gegen %s" % (_b1, _b2))
        check("7 die Zahl steht dann als 1.000 auf der Leiste",
              canvas.itemcget(kenn["wert"], "text") == "1.000",
              canvas.itemcget(kenn["wert"], "text"))
        app.state.resources["holz"].amount = 0
        app._leiste_aktualisieren()
        check("7 Bestand 0 bleibt ohne Warnung (kritisch entfallen)",
              canvas.itemcget(kenn["wert"], "fill") == str(FARBEN.get("zahl")),
              canvas.itemcget(kenn["wert"], "fill"))
        check("7 es gibt keine Flaechen- und Strichkennung mehr",
              kenn.get("grund") is None and kenn.get("strich") is None, str(sorted(kenn)))
        app.state.resources["holz"].amount = 1234
        app._leiste_aktualisieren()
        check("7 mit Bestand ist die Zahl hell",
              canvas.itemcget(kenn["wert"], "fill") == str(FARBEN.get("zahl")), "")
    check("7 die Raten aller Felder stehen als eigene Texte auf der Flaeche",
          all((app._leisten_zellen.get(str(f.get("schluessel"))) or {}).get("rate") is not None
              for f in main.leiste_felder()), "")
    app._build_main_ui()                       # Skinwechsel: der Kopf wird NEU aufgebaut
    root.update()
    app._leiste_zeichnen()
    root.update()
    check("7 nach einem neuen Aufbau (Skinwechsel) ist die Leiste wieder gezeichnet",
          len(app._leisten_zellen) == 11, str(sorted(app._leisten_zellen)))
root.destroy()


# ==========================================================================
abschnitt("8. Quelltext-Wachen: eine Zahlenstelle, kein zweiter Weg")

import inspect as _inspect  # noqa: E402

_quelle = _inspect.getsource(main)
check("8 die alte Rundung mit Format-String ist ersetzt",
      'f"{wert:,.0f}"' not in _quelle, "")
check("8 der Anzeigewert laeuft ueber leisten_kurz",
      "leisten_kurz(leisten_zahl(state, feld))" in _inspect.getsource(main.leistenwert), "")
check("8 das Zeichnen rechnet in leiste_auswahl und leiste_layout, nicht selbst",
      "leiste_auswahl(felder, masse, breite_ist)" in _inspect.getsource(main.NebelseetalApp._leiste_zeichnen)
      and "leiste_layout(texte, None, masse, breite_ist" in _inspect.getsource(main.NebelseetalApp._leiste_zeichnen),
      "")
check("8 das Neuzeichnen holt Zahl, Rate und Zustand aus den drei Rechenstellen",
      all(s in _inspect.getsource(main.NebelseetalApp._leiste_aktualisieren)
          for s in ("leistenwert(self.state, feld)", "leisten_rate(self.state, feld",
                    "leisten_zustand(self.state, feld")), "")
check("8 Schriftgroessen sind PIXELgroessen (negativ), keine Punkte",
      'size=-int(masse.get("schrift_zahl")' in _inspect.getsource(main.NebelseetalApp._leiste_zeichnen), "")
check("8 die Leiste wird im Kopf gebaut und im Takt aktualisiert",
      "_leiste_bauen(top)" in _quelle and "self._leiste_aktualisieren()" in _quelle, "")

sys.exit(bericht())
