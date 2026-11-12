# -*- coding: ascii -*-
"""Ressourcenleiste im Kopf - seit T2 GEZEICHNET statt gemalt (Daniel 11.11.2026).

ENTSCHEIDUNG GEAENDERT (11.11.2026, T2): Daniel hat im Testbogen D3/B09 gesagt: "ganz schrecklich,
ausserdem wird weder Wolle noch Leder als Ressource angezeigt, das muss komplett neu designed
werden". Am Bild gemessen: das gemalte Leistenbild (1440x140, C2-Lieferung, Register 121) hatte ACHT
Symbolfelder; es wurde auf die volle Fensterbreite gezogen, dazwischen sassen 28 leere goldene
Kreisverzierungen als Fuellung, und Wolle, Leder und Pferde hatten ueberhaupt kein Feld. Der Kopf
zeigte damit weniger, als das Modell hat (`main.RESOURCES` fuehrt neun Rohstoffe).

Die alte Wache nagelte genau diese acht Felder und das Bild fest; sie wird deshalb UMGESTELLT - nicht
der Code zurueckgebogen. Das Bild bleibt als Datei und als `_altes_bild` in der Datendatei erhalten
(Register 119/121 geht nicht verloren), wird aber nicht mehr gezeichnet.

Was diese Datei jetzt beweist
-----------------------------
1. Die Datendatei ist die eine Quelle und fuehrt ELF Felder: Siedler, die neun Rohstoffe (Nahrung,
   Holz, Stein, Metall, Gold, Mana, Wolle, Leder, Pferde) und Punkte. Kein Rohstoff des Modells
   fehlt - das ist die Wache gegen den alten Fehler.
2. Eine Rechenstelle je Feld (`main.leistenwert`): Siedler aus `state.population`, Punkte aus
   `state.punktestand()`, Rohstoffe aus `state.resources`.
3. Keine Zahl doppelt im Kopf: seit alle neun Rohstoffe auf der Leiste stehen, gibt
   `main.kopfzeile_fuer` fuer sie nur noch die RATE aus.
4. Der Streifen hat seit T08 (12.11.2026) ein FESTES RASTER (`main.leiste_layout`, ohne Tk): alle
   Zellen sind gleich breit, die Breite folgt dem Fenster (Formel in `main.leiste_raster`), und
   nichts wird gedehnt. Vorher war die Leiste inhaltsgetrieben und 1446 px breit, egal wie breit das
   Fenster war - in einem 1200-px-Fenster fehlten rechts zwei bis drei Felder. Die Einzelheiten
   (Zellbreiten 127/104/85, Weich-Regel, Zahlenkuerzung, Zustaende) prueft
   `tests/test_ressourcenleiste_t08.py`; diese Datei haelt den Weg vom Spielstand zur Flaeche.
5. Die Leiste steht wirklich im Kopf (echte Tk-Flaeche): elf Felder, jede Zahl stimmt mit dem
   Spielstand ueberein, eine Aenderung kommt an.

Aufruf:  python -X utf8 tests/test_ressourcenleiste.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import main  # noqa: E402

daten = main.RESSOURCENLEISTE
felder = main.leiste_felder()


# ==========================================================================
abschnitt("1. Die Datendatei beschreibt elf Felder - keines des Modells fehlt")

datei = os.path.join(ROOT, "data", "ressourcenleiste.json")
check("1 die Datendatei liegt im Projekt", os.path.exists(datei), datei)
check("1 main hat sie geladen", bool(daten), str(type(daten)))
check("1 die Leiste hat elf Felder", len(felder) == 11, str(len(felder)))
check("1 Reihenfolge: Siedler, neun Rohstoffe, Punkte",
      [f.get("schluessel") for f in felder] ==
      ["siedler", "nahrung", "holz", "stein", "metall", "gold", "mana", "wolle", "leder",
       "pferde", "punkte"],
      str([f.get("schluessel") for f in felder]))
check("1 JEDER Rohstoff des Modells steht auf der Leiste",
      set(main.RESOURCES) <= {str(f.get("quelle")) for f in felder},
      str(sorted(set(main.RESOURCES) - {str(f.get("quelle")) for f in felder})))
check("1 Wolle und Leder sind dabei (Daniels Befund D3)",
      {"wolle", "leder"} <= {str(f.get("schluessel")) for f in felder},
      str([f.get("schluessel") for f in felder]))
check("1 jede Quelle ist bekannt",
      all(str(f.get("quelle")) in (set(main.RESOURCES) | {"bevoelkerung", "punkte"}) for f in felder),
      str([f.get("quelle") for f in felder]))
check("1 jedes Feld traegt eine Beschriftung",
      all(str(f.get("name") or "").strip() for f in felder), str([f.get("name") for f in felder]))
check("1 die Hoehe ist ein Streifen, kein Bild (hoechstens 60 px)",
      0 < int(daten.get("hoehe") or 0) <= 60, str(daten.get("hoehe")))
# T08 (12.11.2026): die Kontur um die Zahl ist entfallen - die Zahl steht rechtsbuendig in einer
# festen Zelle auf dunklem Grund (Kontrast 15,13). Dafuer sind die Farben der Zustaende dazugekommen.
check("1 Zahl-, Namen-, Warn- und Grundfarbe sind eingetragen",
      all((daten.get("farben") or {}).get(k)
          for k in ("zahl", "name", "grund", "warnung", "flaeche_kritisch")),
      str(daten.get("farben")))
check("1 die Masse des Rasters stehen in der Datendatei",
      all(k in (daten.get("masse") or {})
          for k in ("endstueck", "trenner", "zelle_max", "zelle_min", "rate_min", "pad",
                    "schrift_name", "schrift_zahl", "zeile_name", "zeile_zahl")),
      str(sorted((daten.get("masse") or {}).keys())))
check("1 das alte Bild ist dokumentiert, aber nicht mehr die Grundlage",
      isinstance(daten.get("_altes_bild"), dict)
      and len((daten.get("_altes_bild") or {}).get("felder") or []) == 8,
      str(type(daten.get("_altes_bild"))))


# ==========================================================================
abschnitt("2. Eine Rechenstelle je Feld (leistenwert)")

class _Betrag:
    """Was `state.resources[...]` liefert: ein Objekt mit `amount`."""

    def __init__(self, menge):
        self.amount = menge


class _Zustand:
    """Minimaler Spielstand fuer die Wertepruefung."""

    def __init__(self):
        self.population = 12.0
        self.resources = {"holz": _Betrag(1234), "stein": _Betrag(7.5), "nahrung": _Betrag(0)}

    def punktestand(self):
        return {"forschung": 3, "krieg": 4, "gesamt": 12345}


_z = _Zustand()
check("2 Siedler kommen aus state.population",
      main.leistenwert(_z, {"schluessel": "siedler", "quelle": "bevoelkerung"}) == "12", "")
check("2 Punkte kommen aus punktestand() mit Tausenderpunkt",
      main.leistenwert(_z, {"schluessel": "punkte", "quelle": "punkte"}) == "12.345",
      main.leistenwert(_z, {"schluessel": "punkte", "quelle": "punkte"}))
check("2 ein Rohstoff kommt aus state.resources",
      main.leistenwert(_z, {"schluessel": "holz", "quelle": "holz"}) == "1.234",
      main.leistenwert(_z, {"schluessel": "holz", "quelle": "holz"}))
# T08 (12.11.2026): die Zahl wird ABGERUNDET, nicht kaufmaennisch gerundet - es wird nie mehr
# angezeigt als vorhanden ist (Claude Teil C2; vorher stand hier "8" fuer 7,6).
check("2 Kommawerte werden abgerundet (nie mehr anzeigen als vorhanden)",
      main.leistenwert(_z, {"schluessel": "stein", "quelle": "stein"}) == "7",
      main.leistenwert(_z, {"schluessel": "stein", "quelle": "stein"}))
check("2 ein fehlender Rohstoff ergibt 0 statt eines Absturzes",
      main.leistenwert(_z, {"schluessel": "gold", "quelle": "gold"}) == "0", "")


# ==========================================================================
abschnitt("3. Keine Zahl doppelt im Kopf (kopfzeile_fuer)")

check("3 ALLE neun Rohstoffe zeigen in der Detailzeile nur die Rate",
      set(main.LEISTEN_ROHSTOFFE) == set(main.RESOURCES), str(main.LEISTEN_ROHSTOFFE))


class _Leer:
    """Spielstand ohne Siedlungen: keine Ernte, kein Verbrauch."""

    population = 0.0
    resources = {"holz": _Betrag(55), "wolle": _Betrag(40), "leder": _Betrag(3), "pferde": _Betrag(2)}
    settlements = []

    def punktestand(self):
        return {"gesamt": 0}


_leer = _Leer()
ertrag = {"holz": 5.0, "wolle": 1.0}
text_holz, _w = main.kopfzeile_fuer(_leer, "holz", ertrag)
text_wolle, _w2 = main.kopfzeile_fuer(_leer, "wolle", ertrag)
check("3 Holz (auf der Leiste) zeigt die Rate ohne Betrag", "55" not in text_holz and "5/h" in text_holz,
      text_holz)
check("3 Wolle steht jetzt auch auf der Leiste und zeigt deshalb NUR die Rate",
      "40" not in text_wolle and "1/h" in text_wolle, text_wolle)
import inspect as _inspect  # noqa: E402
_rate_code = _inspect.getsource(main.kopf_rate_text)
_zeile_code = _inspect.getsource(main.kopf_zeilen_text)
check("3 Rate und Zeile lesen dieselbe Verbrauchsquelle (spieloekonomie.verbrauch_pro_stunde)",
      "spieloekonomie.verbrauch_pro_stunde" in _rate_code
      and "spieloekonomie.verbrauch_pro_stunde" in _zeile_code, "")
check("3 keine der beiden Stellen baut eine eigene Verbrauchsformel",
      "NAHRUNG_JE_EINHEIT_TAG" not in _rate_code and "NAHRUNG_JE_EINHEIT_TAG" not in _zeile_code, "")


# ==========================================================================
abschnitt("4. Festes Raster: alle Zellen gleich breit, nichts gedehnt (T08)")


# UMGESTELLT 12.11.2026 (T08): hier stand die inhaltsgetriebene Rechnung - Zellenbreite aus dem
# laengsten Text, gleichmaessiges Verkleinern bis `schrift_min_faktor`. Daniel hat die Leiste
# zweimal durchfallen lassen ("ganz schrecklich", "total haesslich, der stil ist jetzt komplett
# weg"); der gemessene Fehler war aber der UEBERLAUF: die Leiste blieb 1446 px breit, in einem
# 1200-px-Fenster fehlten rechts zwei bis drei Felder. Die alte Zusage (Zellenbreite folgt dem
# Inhalt) ist damit abgeloest, nicht der Code zurueckgebogen. Die Zahlen des neuen Rasters prueft
# `tests/test_ressourcenleiste_t08.py`; hier bleibt der Weg vom Spielstand zur Flaeche.
_texte = [(n, "1.234") for n in ("Siedler", "Nahrung", "Holz", "Stein", "Metall", "Gold", "Mana",
                                 "Wolle", "Leder", "Pferde", "Punkte")]
_masse = daten.get("masse") or {}
_L = main.leiste_layout(_texte, None, _masse, 1186)
check("4 elf Zellen entstehen", len(_L["zellen"]) == 11, str(len(_L["zellen"])))
check("4 alle Zellen sind gleich breit (nichts gedehnt)",
      len({z["breite"] for z in _L["zellen"]}) == 1, str(sorted({z["breite"] for z in _L["zellen"]})))
check("4 die Zellen liegen in Anzeigereihenfolge von links nach rechts und ueberlappen nicht",
      all(_L["zellen"][i]["x"] + _L["zellen"][i]["breite"] <= _L["zellen"][i + 1]["x"]
          for i in range(len(_L["zellen"]) - 1)),
      str([(z["x"], z["breite"]) for z in _L["zellen"]][:3]))
check("4 jede Zelle traegt Name und Wert",
      all(z["name"] and z["wert"] for z in _L["zellen"]), str(_L["zellen"][0]))
check("4 die letzte Zelle endet vor dem rechten Endstueck (kein Ueberlauf)",
      _L["zellen"][-1]["x"] + _L["zellen"][-1]["breite"] <= 1186 - 16,
      str(_L["zellen"][-1]["x"] + _L["zellen"][-1]["breite"]))
check("4 die Zahl steht rechtsbuendig, der Name linksbuendig",
      all(z["wert_x"] > z["name_x"] for z in _L["zellen"]), str(_L["zellen"][0]))
check("4 in einem sehr breiten Fenster waechst die Zelle nur bis zum Deckel",
      main.leiste_layout(_texte, None, _masse, 2600)["zellbreite"] == 132,
      str(main.leiste_layout(_texte, None, _masse, 2600)["zellbreite"]))
check("4 in einem sehr schmalen Fenster weichen Felder, statt abgeschnitten zu werden",
      len(main.leiste_auswahl(None, _masse, 620)["sichtbar"]) < 11
      and main.leiste_auswahl(None, _masse, 620)["hinweis"].startswith("+"),
      str(main.leiste_auswahl(None, _masse, 620)["hinweis"]))
check("4 ohne bekannte Fensterbreite gilt die Wuenschgroesse der Zelle",
      main.leiste_layout(_texte, None, _masse, 0)["zellbreite"] == int(_masse.get("zelle_soll") or 127),
      str(main.leiste_layout(_texte, None, _masse, 0)["zellbreite"]))


# ==========================================================================
abschnitt("5. Die Leiste steht wirklich im Kopf (echte Tk-Flaeche)")

import tkinter as tk  # noqa: E402

root = tk.Tk()
root.withdraw()
app = main.NebelseetalApp(root)
app._build_main_ui()
root.update()
canvas = getattr(app, "_leisten_canvas", None)
check("5 es gibt eine Leistenflaeche im Kopf", canvas is not None, str(canvas))
if canvas is not None:
    items = canvas.find_withtag("leiste")
    texte = getattr(app, "_leisten_texte", {})
    check("5 alle elf Felder haben Textkennungen", len(texte) == 11, str(sorted(texte)))
    # T08: je Zelle sechs Teile (Flaeche fuer "kritisch", Name, Zahl, Rate, Unterstrich, Pfeil),
    # dazu das Band, die Goldlinie unten, zwei Endstuecke mit Raute und zehn Trenner.
    check("5 je Zelle sechs Teile, dazu Band, Goldlinie, zwei Endstuecke und zehn Trenner",
          len(items) == 11 * 6 + 1 + 1 + 2 + 2 + 10, str(len(items)))
    stimmt = True
    for feld in felder:
        kennungen = texte.get(str(feld.get("schluessel"))) or []
        soll = main.leistenwert(app.state, feld)
        for kennung in kennungen:
            if canvas.itemcget(kennung, "text") != soll:
                stimmt = False
    check("5 jede Zahl auf der Leiste stimmt mit dem Spielstand ueberein", stimmt, "")
    check("5 kein Bild mehr auf der Flaeche (der Streifen wird gezeichnet)",
          not any(canvas.type(i) == "image" for i in items), "")
    app.state.resources["holz"].amount = 4321
    app._leiste_aktualisieren()
    kennung = (texte.get("holz") or [None])[-1]
    check("5 eine Aenderung des Bestands kommt auf der Leiste an",
          kennung is not None and canvas.itemcget(kennung, "text") == "4.321",
          canvas.itemcget(kennung, "text") if kennung else "keine Kennung")
    check("5 Wolle hat ein eigenes Feld auf der Flaeche", (texte.get("wolle") or None) is not None,
          str(sorted(texte)))
root.destroy()


# ==========================================================================
abschnitt("6. Quelltext-Wachen: eine Rechenstelle, keine zweite Leiste")

quelle = _inspect.getsource(main)
check("6 Aufbau und Neuzeichnen benutzen dieselbe Hilfsfunktion",
      quelle.count("kopfzeile_fuer(self.state, r, ertrag_jetzt)") == 2,
      "Treffer: %d" % quelle.count("kopfzeile_fuer(self.state, r, ertrag_jetzt)"))
check("6 die Leiste wird im Kopf gebaut und im Takt aktualisiert",
      "_leiste_bauen(top)" in quelle and "self._leiste_aktualisieren()" in quelle, "")
check("6 Bau und Zeichnen lesen die Felder aus `leiste_felder()`",
      "leiste_felder()" in _inspect.getsource(main.NebelseetalApp._leiste_bauen)
      and "leiste_felder()" in _inspect.getsource(main.NebelseetalApp._leiste_zeichnen), "")
check("6 die Zahlen kommen aus `leistenwert` und nicht aus einer zweiten Rechnung",
      "leistenwert(self.state, feld)" in _inspect.getsource(main.NebelseetalApp._leiste_aktualisieren),
      "")
befund("Die Vorschau des gezeichneten Streifens liegt unter "
       "docs/audits/ressourcenleiste_vorschau_20261111.png", "")

sys.exit(bericht())
