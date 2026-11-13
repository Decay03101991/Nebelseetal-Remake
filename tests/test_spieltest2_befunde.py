# -*- coding: ascii -*-
"""Daniels Befunde aus Spieltest 2 (08.11.2026) - die drei belegbaren.

Daniels Wortlaut (SPIELTEST_2_20261108.txt, mit seinen Antworten):

  Schritt 3/4 (Note 5): "Dann kann ich egal wo keine Uebersicht finden von einem Wall oder wo ich
  ihn ausbauen koennte." / "nicht auffindbar da nicht auffindbar 'WO' das ist wirklich schlecht in
  punkte uebersicht."
  Schritt 5 und danach: "Ich konnte nicht ein einziges gebaeude bauen obwohl die rohstoffe da
  waren und die bibliothek war komplett sinnlos auf einem nebelsee schon wieder."

WAS HIER GEPRUEFT IST
---------------------
1. **Der Wall steht im Dorfzentrum** (dort landet der Spieler), mit Stufe, Zustand und dem
   Reparaturblock - und der Reparaturblock ist DIESELBE Stelle wie auf der Siedlungskarte
   (`_mauer_reparatur_block`, das den Knopf und die Buchung enthaelt).
2. **"Nichts baubar" nennt das GELAENDE und den Weg daneben.** Auf einem Nebelsee-Feld steht in der
   Rubrik "Produktion" kein Gebaeude; die Ansicht sagte nur "keine passenden Gebaeude". Jetzt nennt
   `_gelaende_hinweis` das Gelaende und bis zu drei freie Felder anderer Art aus der eigenen Karte,
   und wenn eine ANDERE Rubrik auf demselben Feld etwas anbietet, steht das dabei.
3. **Die Bibliothek ist nicht "sinnlos".** Die Dorfuebersicht meldete "Bibliothek liefert auf
   Nebelsee nichts" - gemeint war der ROHSTOFFERTRAG. Eine Bibliothek erzeugt keine Rohstoffe, sie
   traegt die Forschung. Der Satz lautet jetzt "erzeugt keine Rohstoffe (Aufgabe: ...)".
   Zusaetzlich sagt die Sperre "hoechstens 1 je Siedlung" jetzt, dass eine ZWEITE Bibliothek auf
   einer anderen Siedlung erlaubt ist.

NICHT geprueft: der GUI-Rundlauf mit echten Mausklicks. Die Zahlen und Texte sind ohne Fenster
belegt (Abschnitte 1 bis 3), die Ansichten deckt `test_gui_fehler` ab.

Aufruf:  python -X utf8 tests/test_spieltest2_befunde.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen+messen"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['dorfwall', 'einheiten', 'main:*', 'punkte', 'wirtschaft']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import ast
import inspect
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src, messwert

ROOT, SRC = import_src()
import main  # noqa: E402
import wirtschaft  # noqa: E402

QUELLE = inspect.getsource(main)
KARTE = {"raster": ["wald"] * 10 + ["grasland"] * 10 + ["nebelsee"] * 5 + ["sumpf"] * 5,
         "spalten": 6, "zeilen": 5, "typ_name": "Pruefkarte", "vorteil": "keiner"}


def ort(bauten=None):
    s = main.Settlement(name="Pruefort", map_id="kontinent", x=0, y=0, karte=dict(KARTE), id="P2")
    s.vorraete = {"nahrung": 50.0, "holz": 2000.0, "stein": 2000.0}
    s.einheiten = {}
    s.bauten = dict(bauten or {})
    s.stufen = {k: 1 for k in (bauten or {})}
    return s


def _funk(name):
    knoten = next((k for k in ast.walk(ast.parse(QUELLE))
                   if isinstance(k, ast.FunctionDef) and k.name == name), None)
    return ast.unparse(knoten) if knoten else ""


# ---------------------------------------------- 1. Wall in der Rubrik Verteidigung
# Register 307 zeigte den Wall im Dorfzentrum; Daniels Spieltest 3 (Note 3) hat ihn in die
# Siedlungskarte unter "Verteidigung" verwiesen. Diese Pruefung haelt den NEUEN Ort fest:
# das Dorfzentrum nennt nur den Zustand und den Weg, die ganze Anzeige steht auf der Karte.
abschnitt("1. Der Wall steht in der Siedlungskarte unter Verteidigung (Test 3, Note 3)")

# ANGEPASST 13.11.2026 (Nr. 16 Teil A): Der Wall-Zustand und der Weg in die Karte stehen jetzt im
# Block AKTIONEN der Spalte (`_dz_block_aktionen`), nicht mehr im Rumpf von `_render_overview`.
# Die ENTSCHEIDUNG ist dieselbe - das Dorfzentrum nennt Zustand und Weg, die ganze Anzeige steht
# auf der Karte -, nur der Aufrufort ist umgezogen.
_uebersicht = _funk("_render_overview") + " " + _funk("_dz_block_aktionen")
_wallblock = _funk("_wall_block")
_karte = _funk("_render_settlement_map")
check("das Dorfzentrum nennt den Dorfwall weiter", "Dorfwall" in _uebersicht or "_wall_kurztext(" in _uebersicht)
check("das Dorfzentrum zeigt NICHT mehr den Reparaturblock (EINE Anzeige)",
      "_mauer_reparatur_block(" not in _uebersicht)
check("das Dorfzentrum rechnet die Wallwerte nicht selbst", "dorfwall.kennwerte(" not in _uebersicht)
check("der Weg in die Karte steht als Knopf bereit", "_oeffne_verteidigung(" in _uebersicht)
check("die Karte ruft den Wall-Block in der Rubrik Verteidigung",
      "Verteidigung" in _karte and "_wall_block(" in _karte)
check("der Wall-Block zeigt Stufe und Zustand aus `dorfwall.kennwerte`",
      "_wall_kurztext(" in _wallblock and "dorfwall.kennwerte(" in _wallblock)
check("die Reparatur steht im Wall-Block", "_mauer_reparatur_block(" in _wallblock)
check("der Wall-Block nennt die Herkunft der Stufe", "Verteidigungsanlagen" in _wallblock)
check("ohne Wall nennt der Block den Knopf zum Errichten", "Wall errichten" in _wallblock)
check("der Wall-Block braucht KEIN gewaehltes Feld", "karten_feld" not in _wallblock)

# ---------------------------------------------- 2. "Nichts baubar" nennt das Gelaende
abschnitt("2. Kein Gebaeude baubar: die Ansicht nennt den Grund (Schritt 5)")

_state = main.GameState()
_s = ort()
_hinweis = _state and main.NebelseetalApp.__dict__["_gelaende_hinweis"]
_app = main.NebelseetalApp.__new__(main.NebelseetalApp)   # ohne Fenster: die Methode rechnet nur
_app.state = _state
_hinweis_nebel = _app._gelaende_hinweis(_s, "nebelsee")
messwert("hinweis_nebelsee_zeichen", len(_hinweis_nebel), "Zeichen", "gerechnet aus der Pruefkarte")
check("der Hinweis nennt das Gelaende und dass es NICHT an den Rohstoffen liegt",
      "nichts baubar" in _hinweis_nebel and "Rohstoffen" in _hinweis_nebel, _hinweis_nebel)
check("der Hinweis nennt freie Felder anderer Art mit Koordinaten",
      "Wald (" in _hinweis_nebel and "Grasland (" in _hinweis_nebel, _hinweis_nebel)
check("der Hinweis sagt, was zu tun ist", "anderes Feld anklicken" in _hinweis_nebel)
check("auch die leere Rubrik zeigt den Hinweis (nicht nur 'keine passenden Gebaeude')",
      "_gelaende_hinweis(" in _funk("_render_settlement_map")
      and _funk("_render_settlement_map").count("_gelaende_hinweis(") >= 2)
check("wenn eine ANDERE Rubrik auf dem Feld baut, steht das dabei",
      "In anderen Rubriken auf diesem Feld baubar" in QUELLE)

# ---------------------------------------------- 3. Die Bibliothek ist nicht "sinnlos"
abschnitt("3. 'Bibliothek liefert nichts' war eine falsche Auskunft (Schritt 5)")

_s_bib = ort({"12": "bibliothek"})       # Feld 12 = nebelsee
_eintraege, _uebersprungen = wirtschaft._feld_ertraege(_s_bib)
_text = " | ".join(_uebersprungen)
messwert("uebersprungene_felder", len(_uebersprungen), "Felder", "Bibliothek auf Nebelsee")
check("die Bibliothek wird NICHT mehr als 'liefert nichts' gemeldet",
      "liefert auf Nebelsee nichts" not in _text, _text)
check("sie wird als Gebaeude OHNE Rohstoffertrag mit ihrer Aufgabe genannt",
      "erzeugt keine Rohstoffe" in _text and "Aufgabe:" in _text, _text)
_kappe = main.bauen_auf_karte(_s_bib, "bibliothek", 13)
check("die Obergrenze je Siedlung greift weiter", _kappe[0] is False, str(_kappe[1]))
check("und sie nennt die zweite Bibliothek auf einer anderen Siedlung als Weg",
      "anderen Siedlung" in str(_kappe[1]), str(_kappe[1]))

befund("Was NICHT geprueft ist: der GUI-Rundlauf mit echten Klicks (die Ansichten deckt "
       "`test_gui_fehler` ab). Daniels Beobachtung 'kein Gebaeude baubar' liess sich am Teststand "
       "NICHT nachstellen: Haus 80/50 und Tempel waren mit 242 Holz und 418 Stein sofort baubar, "
       "und der Klickpfad bucht sie. Die gemessene Sperre war die Bibliothek (hoechstens 1 je "
       "Siedlung) - der Teststand hat schon eine, auf einem Nebelsee-Feld.", "")
befund("Offen und NICHT geaendert: die Ereignis-Flut. Gemessen ueber 10 Spieltage ab Tag 5 "
       "entstehen 33 Nachrichten (21 Diplomatie-Ereignisse, 9 Gruendungen, 3 Kaempfe) - rund 3,3 je "
       "Spieltag, jede zusaetzlich in der Statuszeile. Weniger Ereignisse oder ein Filter waeren "
       "eine Regel-/Balancing-Entscheidung Daniels.", "")
sys.exit(bericht())
