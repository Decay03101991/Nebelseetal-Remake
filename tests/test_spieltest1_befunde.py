# -*- coding: ascii -*-
"""Daniels Befunde aus Spieltest 1 (08.11.2026, Register 305) - die drei belegbaren.

Daniel hat Test 1 nach zwei Schritten abgebrochen ("vorzeitiger test abbruch meiner seits"). Seine
drei Befunde, woertlich aus `archiv/spieltests/20261108_test1/SPIELTEST_ANLEITUNG_20261108_mit_Antworten.txt`:

  1. "Bibliothek ausversehen auf einem nebelsee gebaut und versucht zu forschen aber nichts
     moeglich. Gefuehlter soft lock. Kein Gebaeude bau moeglich obwohl die Ressourcen dafuer da
     sind. Keine Forschung obwohl gruener text. Kein Hinweis darauf was ich tun koennte."
  2. "Der 'Los geht es' Button im Ankunft fenster fuehrt nirgendwo hin ... Er sollte direkt zu
     ersten Fraktionswahl fuehren."
  3. "Das Remake muss da noch weg."

WAS HIER GEMESSEN IST (Abschnitt 1): der Soft Lock kam NICHT von der Bibliothek auf dem Nebelsee -
das ist eine erlaubte Standortregel (`data/buildings.json`, `nur_auf` enthaelt nebelsee). Sein
Spielstand stand in **Nahrungsnot**: Ortslager Nahrung 0,0, Bedarf 8,0 je Tag, eigene Ernte 0,0.
Diese Sperre (Daniels Entscheidung 70/74) blockt Bauen, Ausbauen, Ware, Forschung und Ausbildung.
Die **Anzeige** fragte die Sperre aber nicht - deshalb "gruener text" bei wirkungslosem Klick: die
zweite Rechenstelle, die Daniel beschrieben hat. Abschnitt 2 belegt, dass Anzeige und Klick jetzt
dieselbe Stelle fragen (auch die Gegenprobe: ohne Not ist wieder baubar).

NICHT geprueft: der GUI-Rundlauf (Knopf wirklich gedrueckt) - die Anzeige-Pruefung ist ohne
Fenster belegt, die Ansichten deckt `test_gui_fehler` ab.

DIE ENTSCHEIDUNG (Daniel 08.11.2026, V-3): Karren und Belagerungsgeraete essen nicht mit, UND ein
Nahrungsgebaeude bleibt in der Not baubar und zahlbar. Damit hat der Ort wieder den Ausweg, den
Entscheidung 70 nennt ("eigene Erzeugung ueber den Verbrauch"), und der Sperrtext sagt ihm, welcher
das ist. Abschnitt 2 prueft beides: "haus" gesperrt, "jaeger" erlaubt, im Menue ist in der Not auf
einem Waldfeld NUR `jaeger` baubar (er braucht keine Forschung; `farm` und `rinderfarm` verlangen
Baukunst und sind damit erst nach einer Forschung im Ausland erreichbar).

Aufruf:  python -X utf8 tests/test_spieltest1_befunde.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen+messen"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['baumenue_info', 'einheiten', 'gelaende', 'main:*', 'spieloekonomie', 'story']
PRUEF_DATEN = ['buildings.json', 'nahrungsverbrauch.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import ast
import inspect
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src, messwert

ROOT, SRC = import_src()
import baumenue_info  # noqa: E402
import main  # noqa: E402
import spieloekonomie as O  # noqa: E402

QUELLE = inspect.getsource(main)


def siedlung(nahrung, einheiten=None, raster=None):
    """Ein Ort mit echter Karte (20 Felder) und frei waehlbaren Vorraeten - ohne Fenster."""
    karte = {"raster": list(raster or ["grasland"] * 20), "spalten": 5, "zeilen": 4,
             "typ_name": "Pruefkarte", "vorteil": "keiner"}
    s = main.Settlement(name="Pruefort", map_id="kontinent", x=0, y=0, karte=karte, id="P1")
    s.vorraete = {"nahrung": float(nahrung), "holz": 900.0, "stein": 900.0}
    s.einheiten = dict(einheiten or {})
    s.bauten = {}
    s.stufen = {}
    return s


def angebote(state, s, feld=0, kategorie="Produktion"):
    """Das Baumenue-Angebot wie im Spiel: dieselbe Pruefstelle fuer die Anzeige."""
    art = s.karte["raster"][feld]
    return baumenue_info.angebote(
        feld, art, s,
        regelpruefung=lambda kennung: main.bauanzeige_pruefung(state, s, kennung, feld),
        kostenfunktion=main.baukosten,
        deckungspruefung=lambda preis: state.ortsdeckung(s, preis),
        ertragsfunktion=lambda kennung, gelaende: "",
        kategorie=kategorie,
        wall_ohne_feld=True)


# ---------------------------------------------- 1. Der Soft Lock: die Ursache in Zahlen
abschnitt("1. Soft Lock: die Siedlung stand in Nahrungsnot, nicht die Bibliothek")

_state = main.GameState()
# V-3 (Daniel 08.11.2026): eine Karawane isst NICHT mehr mit - der Fall, der den Teststand
# gesperrt hat, ist damit weg. Der Bedarf kommt jetzt nur noch von echten Truppen.
_karre = siedlung(0.0, {"Handelskarawane": 1})
_not_karre = _state.nahrungsnot(_karre)
messwert("bedarf_je_tag_eine_karawane", _not_karre["bedarf_tag"], "Nahrung/Tag",
         "data/nahrungsverbrauch.json, rollen_ohne_verbrauch")
check("eine Handelskarawane allein setzt den Ort NICHT mehr in Not (V-3)",
      _not_karre["not"] is False, str(_not_karre))

_truppe = siedlung(0.0, {"Krieger": 1})
_not = _state.nahrungsnot(_truppe)
_not_text = str(_not.get("text") or "")
messwert("bedarf_je_tag_ein_krieger", _not["bedarf_tag"], "Nahrung/Tag",
         "data/nahrungsverbrauch.json, je_einheit_pro_tag")
messwert("ernte_je_tag_ohne_nahrungsgebaeude", _not["ernte_tag"], "Nahrung/Tag",
         "gerechnet aus dem leeren Ortslager der Pruefsiedlung")
check("Lager leer + ein Krieger + keine Ernte = NOT (Daniels Schwelle 70/74)",
      _not["not"] is True, str(_not))
check("der Sperrtext nennt Bedarf, Ernte und Fehlbetrag - also den Grund",
      "braucht 8.0 je Tag" in _not_text and "erntet nur 0.0" in _not_text, _not_text)
check("der Sperrtext nennt den AUSWEG (Daniel: 'kein Hinweis darauf was ich tun koennte')",
      "Ausweg" in _not_text and "Nahrungsgeb" in _not_text, _not_text)

# Die Bibliothek auf dem Nebelsee war NICHT die Ursache: die Standortregel erlaubt sie dort.
_erlaubt, _warum = main.gelaende.bau_moeglich("bibliothek", "nebelsee")
check("Bibliothek auf Nebelsee ist eine ERLAUBTE Standortregel (kein Fehler)", _erlaubt is True, _warum)

# ---------------------------------------------- 2. Anzeige und Klick fragen dieselbe Stelle
abschnitt("2. Die Anzeige sagt die Wahrheit - und der Ausweg bleibt offen (V-3)")

_wald = siedlung(0.0, {"Krieger": 1}, raster=["wald"] * 20)
_alle = {(k, a["id"]): a for k in baumenue_info.KATEGORIEN
         for a in angebote(_state, _wald, kategorie=k)}

_frei_not, _grund_not = main.bauanzeige_pruefung(_state, _wald, "haus", 0)
check("Bau-Vorpruefung meldet in Not: nein", _frei_not is False, str(_grund_not))
check("... und nennt die Nahrungsnot als Grund", "Nahrungsnot" in str(_grund_not), str(_grund_not))

_frei_jaeger, _grund_jaeger = main.bauanzeige_pruefung(_state, _wald, "jaeger", 0)
check("V-3: ein NAHRUNGSGEBAEUDE bleibt in Not baubar (der Ausweg Jaeger, ohne Forschung)",
      _frei_jaeger is True, str(_grund_jaeger))

_baubar_ids = sorted({a["id"] for a in _alle.values() if a["baubar"]})
messwert("angebote_im_menue_in_not", len(_alle), "Zeilen", "gezaehlt ueber alle Baumenue-Rubriken")
check("in Not ist im Menue NUR das Nahrungsgebaeude baubar", _baubar_ids == ["jaeger"],
      str(_baubar_ids))
_haus_status = [a["status"] for a in _alle.values() if a["id"] == "haus"]
check("das gesperrte Haus nennt die Nahrungsnot als Grund",
      bool(_haus_status) and all(s.startswith("Gesperrt: Nahrungsnot") for s in _haus_status),
      str(_haus_status))

# Gegenprobe: mit Nahrung im Lager ist dieselbe Pruefung wieder freundlich (keine Dauer-Sperre).
_satt = siedlung(5.0, {"Krieger": 1}, raster=["wald"] * 20)
_frei_ok, _grund_ok = main.bauanzeige_pruefung(_state, _satt, "haus", 0)
_baubar_satt = sum(1 for k in baumenue_info.KATEGORIEN
                   for a in angebote(_state, _satt, kategorie=k) if a["baubar"])
messwert("angebote_baubar_ohne_not", _baubar_satt, "Zeilen", "Gegenprobe mit 5 Nahrung im Lager")
check("Gegenprobe: mit Nahrung ist ein Bau wieder erlaubt", _frei_ok is True, str(_grund_ok))
check("Gegenprobe: das Menue bietet wieder mehr Gebaeude an", _baubar_satt > len(_baubar_ids),
      str(_baubar_satt))

# ---------------------------------------------- 3. Keine vierte Rechenstelle
abschnitt("3. Quelltext-Wachen: alle vier Anzeigestellen fragen die Sperre")

for funktion, name in (("_render_settlement_map", "Baumenue"),
                       ("_render_research", "Forschung"),
                       ("_render_storage", "Werkstatt/Ware"),
                       ("_ausbildungs_hindernis", "Ausbildung")):
    knoten = next((k for k in ast.walk(ast.parse(QUELLE))
                   if isinstance(k, ast.FunctionDef) and k.name == funktion), None)
    rumpf = ast.unparse(knoten) if knoten else ""
    check("%s fragt die Nahrungssperre" % name, "_nahrungssperre(" in rumpf, funktion)
check("das Baumenue fragt die EINE Pruefstelle (nicht die Bauregel allein)",
      "_bauanzeige_pruefung(" in ast.unparse(next(
          k for k in ast.walk(ast.parse(QUELLE))
          if isinstance(k, ast.FunctionDef) and k.name == "_render_settlement_map")))
check("bauanzeige_pruefung ist read-only (kein Schreiben in bauten/stufen)",
      "siedlung.bauten" not in inspect.getsource(main.bauanzeige_pruefung)
      and "siedlung.stufen" not in inspect.getsource(main.bauanzeige_pruefung))

# ---------------------------------------------- 4. Ankunftsfenster fuehrt zur Fraktionswahl
abschnitt("4. 'Los geht es' fuehrt zur Fraktionswahl (Daniels Befund 2)")

_frisch = main.GameState()
_frisch.settlements = []
_frisch.spieler_fraktion = ""
check("frischer Start ohne Volk -> Gruendungsseite, Schritt 2 (Fraktionswahl)",
      main.intro_ziel(_frisch) == (main.KARTENGRUENDUNG_ANSICHT, "volk"), str(main.intro_ziel(_frisch)))
_frisch.spieler_fraktion = "Elfen"
check("Volk gewaehlt, noch kein Dorf -> Schritt 3 (die Karte)",
      main.intro_ziel(_frisch) == (main.KARTENGRUENDUNG_ANSICHT, "karte"), str(main.intro_ziel(_frisch)))
_mit_dorf = main.GameState()
_mit_dorf.settlements = [siedlung(5.0)]
check("geladener Stand mit Dorf -> Dorfzentrum", main.intro_ziel(_mit_dorf) == ("Dorfzentrum", ""),
      str(main.intro_ziel(_mit_dorf)))
check("der Knopf ruft die eine Weiterleitung (nicht mehr nur 'schliessen')",
      "_intro_weiter(schliessen)" in QUELLE and "lam" + "bda: (story.intro_merken(), schliessen())" not in QUELLE)

# ---------------------------------------------- 5. Die Wortmarke ist weg
abschnitt("5. Startbildschirm ohne das Wort 'Remake' (Daniels Befund 3)")

check("keine sichtbare Beschriftung 'Remake' mehr im Quelltext",
      'text="Remake"' not in QUELLE and "text='Remake'" not in QUELLE)
check("das Logo bleibt (Rueckfall-Schriftzug Nebelseetal ist noch da)",
      'text="Nebelseetal"' in QUELLE)

# ---------------------------------------------- 6. U1: die Bibliotheksgrenze steht auch in der Anzeige
# (Gesamtaudit 11.11.2026, Register 399/450): Daniel erlaubt hoechstens ZWEI Bibliotheken je Spieler
# (30.10.2026). Die Grenze stand nur im Klick - das Menue bot eine dritte weiter als baubar an.
abschnitt("6. U1: die dritte Bibliothek ist im Menue gesperrt, nicht erst beim Klick")

_bib1 = siedlung(5.0, {"Krieger": 1}, raster=["nebelsee"] * 20)
_bib2 = siedlung(5.0, {"Krieger": 1}, raster=["nebelsee"] * 20)
_bib1.bauten["0"] = "bibliothek"
_bib1.stufen["0"] = 1
_bib2.bauten["0"] = "bibliothek"
_bib2.stufen["0"] = 1
_state.settlements = [_bib1, _bib2]
_frei_bib, _grund_bib = main.bauanzeige_pruefung(_state, _bib1, "bibliothek", 1)
check("mit zwei Bibliotheken sagt die ANZEIGE nein", _frei_bib is False, str(_grund_bib))
check("... und nennt die Grenze als Grund",
      "Bibliotheken" in str(_grund_bib) and str(main.BIBLIOTHEK_OBERGRENZE) in str(_grund_bib),
      str(_grund_bib))
# Die Bibliothek steht in einer der vorhandenen Rubriken - gesucht wird ueber ALLE.
_angebote_bib = [a for k in baumenue_info.KATEGORIEN
                 for a in angebote(_state, _bib1, kategorie=k)
                 if a["id"].lower().startswith("bibliothek")]
check("das Menue bietet sie NICHT als baubar an",
      bool(_angebote_bib) and not any(a["baubar"] for a in _angebote_bib),
      str([(a["id"], a["baubar"]) for a in _angebote_bib]))
_state.settlements = [_bib1]
_frei_bib1, _grund_bib1 = main.bauanzeige_pruefung(_state, _bib1, "bibliothek", 1)
check("Gegenprobe: mit EINER Bibliothek ist die zweite weiter erlaubt (kein Dauer-Sperre)",
      "Bibliotheken" not in str(_grund_bib1), str(_grund_bib1))

befund("Was NICHT geprueft ist: der GUI-Rundlauf (Knopf wirklich gedrueckt). Die Anzeige-Pruefung "
       "ist ohne Fenster belegt; die Ansichten deckt `test_gui_fehler` ab.", "")
befund("V-3 ist gebaut (Daniel 08.11.2026): Karren/Belagerung essen nicht mit, Nahrungsgebaeude "
       "bleiben in der Not baubar. Die Sperre selbst bleibt unveraendert hart fuer alles andere.", "")
sys.exit(bericht())
