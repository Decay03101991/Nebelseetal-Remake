# -*- coding: ascii -*-
"""S4-6: Handelspunkte aus dem VERKAUF (06.11.2026, Register 290, docs/ABLAUF_LLM_20261106.md Schritt 6).

Geprueft wird, was der Schnitt zusagt - nach Daniels Entscheidung F-12 (A, Verkaufsrichtung):
  A. Die Quelle 2006: 1 Punkt je 100 Gold, 20 Gold = 0.2, Verfall 1 Punkt je 24 Spielstunden.
  B. Verfall faellt nicht unter 0 und `letzter_handel = None` heisst "nie gehandelt".
  C. Echter Verlauf: der Spieler verkauft Ware an einen Bot, das Gold kommt an, der Erloes wird
     GENAU EINMAL gebucht, die Karre kehrt zum Ort zurueck, die Handelspunkte stehen ueber 0.
  D. Keine Doppelbuchung: weiterer Takt, Speichern und Laden aendern den Zaehler nicht.
  E. Ein alter Spielstand ohne `handels_erloes` laedt mit 0.0.
  F. Anzeige und Kern lesen DENSELBEN Zaehler (Quellwache, Muster F-04), und der KAUF bucht nichts
     (die Quelle bepunktet nur eingenommenes Gold).

Gesetzt wird im Verlauf nur die Handelskarawane (eine echte Ausbildung kostet 500 Holz, 250 Metall,
200 Gold, 50 Wolle, 500 Leder, 10 Siedler und 15 Pferde - das sind 20+ Spieltage) und der Bot selbst;
alles andere laeuft ueber den echten Weg des Spiels.
ASCII-only (Pruefdatei-Konvention).
"""
from __future__ import annotations

import inspect
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

import_src()
import main
import punkte

STUNDE = 3600.0
TAG = 24 * STUNDE


HAENDLER = "Haendler"        # der SCHLUESSEL aus punkte.auszeichnungen (ASCII, wie die Datei)


def _auszeichnung(werte: dict, name: str):
    """Den Wert EINER Auszeichnung aus `punkte.auszeichnungen` holen (dieselbe Funktion wie die App)."""
    for eintrag in punkte.auszeichnungen(werte):
        if eintrag.get("name") == name:
            return eintrag.get("wert")
    return None


def _bot(name="Haug", trading=0.6, gold=500.0):
    """Ein Bot, wie ihn das Spiel fuehrt - mit Gold im Lager und einem Dorf."""
    b = main.BotPlayer(name=name, faction="menschlich", aggression=0.5, trading=trading)
    b.doerfer = [main.BotDorf(name="H1", hauptdorf=True, dimension=1, herkunftswelt=1)]
    b.vorraete = {"holz": 500.0, "gold": float(gold), "nahrung": 500000.0}
    return b


abschnitt("A. Quelle 2006: 1 Punkt je 100 Gold, 20 Gold = 0.2")
check("100 Gold ergeben genau 1.0 Punkte",
      punkte.handelspunkte(100, None, 0.0) == 1.0, str(punkte.handelspunkte(100, None, 0.0)))
check("20 Gold ergeben genau 0.2 Punkte",
      punkte.handelspunkte(20, None, 0.0) == 0.2, str(punkte.handelspunkte(20, None, 0.0)))
check("250 Gold ergeben 2.5 Punkte (anteilig)",
      punkte.handelspunkte(250, None, 0.0) == 2.5, str(punkte.handelspunkte(250, None, 0.0)))
check("negativer Erloes zaehlt nicht (kein Minuspunkt)",
      punkte.handelspunkte(-500, None, 0.0) == 0.0, str(punkte.handelspunkte(-500, None, 0.0)))

abschnitt("B. Verfall: 1 Punkt je 24 Spielstunden, nicht unter 0")
check("nach 23 Stunden steht der Punkt noch",
      punkte.handelspunkte(300, 0.0, 23 * STUNDE) == 3.0,
      str(punkte.handelspunkte(300, 0.0, 23 * STUNDE)))
check("nach 24 Stunden ist genau ein Punkt weg",
      punkte.handelspunkte(300, 0.0, 24 * STUNDE) == 2.0,
      str(punkte.handelspunkte(300, 0.0, 24 * STUNDE)))
check("nach 72 Stunden ist alles verfallen, nicht negativ",
      punkte.handelspunkte(300, 0.0, 72 * STUNDE) == 0.0,
      str(punkte.handelspunkte(300, 0.0, 72 * STUNDE)))
check("letzter_handel None heisst nie gehandelt - kein Verfall",
      punkte.handelspunkte(300, None, 999 * STUNDE) == 3.0,
      str(punkte.handelspunkte(300, None, 999 * STUNDE)))

abschnitt("C. Echter Verlauf: verkaufen, Erloes gebucht, Karre kehrt zurueck")
root = None
app = None
st = None
vertrag = None
try:
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    app = main.NebelseetalApp(root)
    app._build_main_ui()
    st = app.state
    app._erste_siedlung_gruenden()                     # der echte Start: 100 Holz, 10 Siedler
    ort = st.aktive_siedlung()
    ort.vorraete["holz"] = 200.0                       # Bestand fuer den Verkauf
    ort.vorraete["gold"] = 0.0                         # kein Gold im Ort - es kommt erst durch den Verkauf
    ort.einheiten["Handelskarawane"] = 1               # die EINE gesetzte Zustaendigkeit (siehe Kopf)
    haug = _bot()
    st.bots = [haug]
    st.noob_protection = True                          # kein Bot-Angriff waehrend der Probe
    st.auftraege[:] = []
    st.handels_erloes = 0.0
    st.letzter_handel = 0.0

    _gold_vor = float(ort.vorraete.get("gold") or 0.0)
    _karre_vor = int(ort.einheiten.get("Handelskarawane") or 0)
    # E1 (Register 323): der Preis kommt aus der EINEN Preisfunktion je Rohstoff - vorher stand hier
    # die getippte 1,0, die seit dem Rohstoffpreis UEBER der Kaufschwelle des Bots lag.
    _preis = float(main.bot_handelpreis(haug, "holz", getattr(ort, "karte", None),
                                        "verkauf").get("preis") or 0.0)
    check("die Preisfunktion liefert einen Preis", _preis > 0.0, str(_preis))
    ok, meldung = st.verkauf_an_bot(haug, ort, "holz", 100, _preis, {"Handelskarawane": 1})
    check("der Verkauf wird angenommen", ok is True, str(meldung))
    check("die Karre faehrt los (nicht mehr im Ort)",
          int(ort.einheiten.get("Handelskarawane") or 0) == _karre_vor - 1,
          str(ort.einheiten.get("Handelskarawane")))
    check("das Gold des Bots ist bis zur Entscheidung gesperrt",
          float(haug.vorraete.get("gold") or 0.0) < 500.0, str(haug.vorraete.get("gold")))
    vertrag = st.auftraege[-1]
    check("der Vertrag traegt die Richtung verkauf",
          vertrag.get("richtung") == "verkauf", str(vertrag.get("richtung")))
    check("die Karawane laeuft auf der Verkaeuferseite (Spieler)",
          vertrag.get("karawane_seite") == "verkaeufer", str(vertrag.get("karawane_seite")))

    st.tick(float(vertrag.get("rueckkehr") or 0.0) + 60.0)
    check("der Handel ist abgerechnet", vertrag.get("abgerechnet") is True,
          str(vertrag.get("abgerechnet")))
    check("der Erloes ist 100 x Preis", abs(float(vertrag.get("erloes") or 0.0) - 100.0 * _preis) < 1e-6,
          str(vertrag.get("erloes")))
    check("der Zaehler steht auf 100 x Preis",
          abs(float(st.handels_erloes) - 100.0 * _preis) < 1e-6, str(st.handels_erloes))
    check("letzter_handel ist der Zeitpunkt der Annahme",
          float(st.letzter_handel) > 0.0, str(st.letzter_handel))
    check("das Gold ist beim Spieler angekommen",
          float(ort.vorraete.get("gold") or 0.0) >= _gold_vor + 100.0 * _preis,
          "%g nachher, %g vorher" % (float(ort.vorraete.get("gold") or 0.0), _gold_vor))
    check("die Karre ist zum Ort zurueckgekehrt",
          int(ort.einheiten.get("Handelskarawane") or 0) == _karre_vor,
          str(ort.einheiten.get("Handelskarawane")))
    _punkte = punkte.handelspunkte(st.handels_erloes, st.letzter_handel, st.spielsekunden)
    check("die Handelspunkte stehen ueber 0", _punkte > 0.0, str(_punkte))
except Exception as fehler:                            # noqa: BLE001 - Befund statt Absturz
    befund("C", "der Verlauf lief nicht durch", "%s: %s" % (type(fehler).__name__, fehler))

abschnitt("D. Keine Doppelbuchung (weiterer Takt, Speichern und Laden)")
if st is not None and vertrag is not None:
    _vorher = float(st.handels_erloes)
    st.tick(float(st.spielsekunden) + 3 * TAG)
    check("ein weiterer Takt bucht nichts nach", float(st.handels_erloes) == _vorher,
          "%s nachher, %s vorher" % (st.handels_erloes, _vorher))
    _pfad = os.path.join(tempfile.gettempdir(), "wache_s46_handelspunkte.json")
    st.save(_pfad)
    st.handels_erloes = -1.0
    st.letzter_handel = -1.0
    st.load(_pfad)
    check("Speichern und Laden erhalten den Zaehler", float(st.handels_erloes) == _vorher,
          str(st.handels_erloes))
    _vor_laden = float(st.handels_erloes)
    st.tick(float(st.spielsekunden) + TAG)
    check("auch nach dem Laden wird nicht nachgebucht",
          float(st.handels_erloes) == _vor_laden,
          "%s nachher, %s vorher" % (st.handels_erloes, _vor_laden))
    if os.path.exists(_pfad):
        os.remove(_pfad)

abschnitt("E. Alter Spielstand ohne handels_erloes laedt mit 0.0")
if st is not None:
    _pfad = os.path.join(tempfile.gettempdir(), "wache_s46_altstand.json")
    st.save(_pfad)
    with open(_pfad, "r", encoding="utf-8") as f:
        daten = json.load(f)
    daten.pop("handels_erloes", None)                  # genau der Stand von vor S4-6
    daten.pop("letzter_handel", None)
    with open(_pfad, "w", encoding="utf-8") as f:
        json.dump(daten, f, ensure_ascii=False)
    st.handels_erloes = 777.0
    st.letzter_handel = 999.0
    st.load(_pfad)
    check("ohne Feld steht der Zaehler auf 0", float(st.handels_erloes) == 0.0, str(st.handels_erloes))
    check("ohne Feld steht der Zeitpunkt auf 0", float(st.letzter_handel) == 0.0, str(st.letzter_handel))
    if os.path.exists(_pfad):
        os.remove(_pfad)

abschnitt("F. Anzeige und Kern lesen denselben Zaehler; der KAUF bucht nichts")
if st is not None:
    st.handels_erloes = 250.0
    st.letzter_handel = 0.0
    _werte = {
        "forschungsstaende": {k: int(v.level) for k, v in st.research.items()},
        "einheiten": {k: int(v.count) for k, v in st.units.items()},
        "wall_stufe": 0,
        "gold_erloes": float(st.handels_erloes),
        "letzter_handel": (float(st.letzter_handel) if float(st.letzter_handel) > 0.0 else None),
        "jetzt": float(st.spielsekunden),
    }
    _kern = punkte.handelspunkte(_werte["gold_erloes"], _werte["letzter_handel"], _werte["jetzt"])
    check("Auszeichnung Haendler und punkte.handelspunkte sind gleich",
          _auszeichnung(_werte, HAENDLER) == _kern,
          "%s gegen %s" % (_auszeichnung(_werte, HAENDLER), _kern))
    _quelle = inspect.getsource(main.NebelseetalApp)
    for _wort in ('"gold_erloes"', '"letzter_handel"', '"jetzt"'):
        check("die Anzeige uebergibt %s" % _wort, _wort in _quelle, _wort)
    _anfrage = inspect.getsource(st.verkauf_an_bot)
    check("der Verkauf uebergibt karawane_seite=verkaeufer",
          'karawane_seite="verkaeufer"' in _anfrage, "gefunden" if 'karawane_seite="verkaeufer"'
          in _anfrage else "fehlt")
    check("die Buchstelle steht NICHT im Verkaufspfad (sie gehoert in _fremdvertrag_buchen)",
          "handels_erloes =" not in _anfrage, "Buchstelle nur an einer Stelle")

abschnitt("G. Der Verkauf ist ueber die Oberflaeche erreichbar (Maske und App-Weg)")
if app is not None and st is not None:
    check("die Verkaufsmaske existiert", hasattr(app, "_verkauf_maske"), "gefunden"
          if hasattr(app, "_verkauf_maske") else "fehlt")
    check("der Verkaufspfad der App existiert", hasattr(app, "_verkauf_ausfuehren"), "gefunden"
          if hasattr(app, "_verkauf_ausfuehren") else "fehlt")
    _quelle_app = inspect.getsource(main.NebelseetalApp)
    check("die Kaufmaske traegt den Knopf zum Verkauf",
          'Verkauf anbieten (eigene Ware)' in _quelle_app, "Knopf im Quelltext")
    _vorher_app = float(st.handels_erloes)
    ok_app, meldung_app = app._verkauf_ausfuehren(haug, ort, "holz", 10, _preis,
                                                 "Handelskarawane", "1")
    check("die App startet den Verkauf ohne Fenster", ok_app is True, str(meldung_app))
    _neu_app = st.auftraege[-1] if st.auftraege else {}
    check("der Vertrag der App traegt die Richtung verkauf",
          _neu_app.get("richtung") == "verkauf", str(_neu_app.get("richtung")))
    st.tick(float(_neu_app.get("rueckkehr") or 0.0) + 60.0)
    check("der Erloes der App wird gebucht",
          float(st.handels_erloes) > _vorher_app, "%s nachher, %s vorher"
          % (st.handels_erloes, _vorher_app))

if root is not None:
    try:
        root.destroy()
    except Exception:                                   # noqa: BLE001 - ein kaputtes Fenster stoert nicht
        pass

bericht()
