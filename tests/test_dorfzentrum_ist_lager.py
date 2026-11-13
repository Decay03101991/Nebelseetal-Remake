# -*- coding: ascii -*-
"""Schnitt S-2c: Das Dorfzentrum IST das Lager - Menuepunkt UND Gebaeude.

Entscheidung Daniel 01.11.2026 (docs/KONZEPT_SECHS_DOERFER_20261101.md, Anhang 1):
"Das Dorfzentrum IST das Lager" - dort liegen Lagerverwaltung und Uebersichten, und es ist
zugleich ein Gebaeude (hoechstens eines je Dorf, nicht abreissbar).

Umgesetzt:
  * D-01  Die Kennung bleibt `lager` (Speicherformat), der Anzeigename heisst `Dorfzentrum`;
          der alte Name `Lager` steht als `alias` und wird weiter erkannt (keine Migration).
  * D-05  `max_je_siedlung: 1` in data/buildings.json - ein zweites Dorfzentrum je Dorf ist
          gesperrt. Durchgesetzt wird die Grenze im vorhandenen Kern (`bauen_auf_karte`),
          KEINE zweite Bestandszahl.
  * D-06  Das einzige Dorfzentrum kann nicht abgerissen werden.
  * D-07  EINE Lageransicht: `_render_overview` (Menuepunkt "Dorfzentrum") ruft
          `_render_storage(eigener_titel=False)` auf.
  * D-08  Der Menuepunkt "Lager" erscheint nicht mehr (`MENUE_ENTFALLEN`); MENU_ITEMS bleibt
          als BELEGTE Original-Liste unveraendert, die Route "Lager" bleibt erreichbar und
          traegt den Vermerk STILLGELEGT.

Offen und NICHT hier entschieden: ob das Dorfzentrum bei jeder Gruendung kostenlos mitgesetzt
wird (dann vier Startgebaeude statt drei, S-1 zieht mit). Das ist eine Entscheidung von Daniel
und steht gesammelt in der Uebergabe - dieser Schnitt funktioniert in beiden Faellen.

Aufruf: python -X utf8 tests/test_dorfzentrum_ist_lager.py
"""

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['admin_teststand', 'gebaeude_wirkung', 'gelaende', 'main:*']
PRUEF_DATEN = ['buildings.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------
import ast
import inspect
import os
import sys
import textwrap
import types

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
os.chdir(SRC)

import main  # noqa: E402
import gelaende  # noqa: E402
import gebaeude_wirkung  # noqa: E402


def _karte(raster, spalten=10):
    spalten = int(spalten)
    return {"raster": list(raster), "spalten": spalten,
            "zeilen": (len(raster) + spalten - 1) // spalten}


def _dorf(raster, spalten=10):
    return main.Settlement(name="Testdorf", map_id="kontinent", x=0, y=0,
                           karte=_karte(raster, spalten), id="test:0:0:0")


def _code(funktion) -> str:
    """Quelltext einer Methode OHNE Docstring (Docstrings zaehlen nicht als Code)."""
    baum = ast.parse(textwrap.dedent(inspect.getsource(funktion)))
    rumpf = baum.body[0].body
    if rumpf and isinstance(rumpf[0], ast.Expr) and isinstance(rumpf[0].value, ast.Constant):
        rumpf = rumpf[1:]
    return "\n".join(ast.unparse(knoten) for knoten in rumpf)


# --------------------------------------------------------------------------------------
def _daten():
    abschnitt("1. D-01: Kennung bleibt lager, Anzeigename ist Dorfzentrum")
    alle = gelaende.alle_gebaeude()
    eintrag = alle.get("lager") or {}
    check("der Datensatz 'lager' existiert genau einmal",
          [k for k in alle if k == "lager"] == ["lager"], str([k for k in alle if "lager" in k]))
    check("es gibt KEINEN zweiten Datensatz 'dorfzentrum'", "dorfzentrum" not in alle,
          str(sorted(alle)))
    check("der Anzeigename ist Dorfzentrum", eintrag.get("name") == "Dorfzentrum",
          str(eintrag.get("name")))
    check("die Kennung bleibt lager", eintrag.get("id") == "lager", str(eintrag.get("id")))
    check("der alte Name steht als Alias", "Lager" in (eintrag.get("alias") or []),
          str(eintrag.get("alias")))
    check("die Kategorie bleibt Sonstiges (der Baubereich ist erreichbar)",
          eintrag.get("kategorie") == "Sonstiges", str(eintrag.get("kategorie")))
    check("die Standortregel bleibt erhalten (kein Bau im Sumpf oder auf Berg)",
          eintrag.get("nur_auf") == ["grasland", "steppe", "wald", "huegel"],
          str(eintrag.get("nur_auf")))

    abschnitt("2. D-05: hoechstens ein Dorfzentrum je Dorf")
    check("max_je_siedlung steht auf 1", eintrag.get("max_je_siedlung") == 1,
          str(eintrag.get("max_je_siedlung")))
    check("die Grenze wird NICHT im Code nachgezogen, sondern aus den Daten gelesen",
          "max_je_siedlung" in inspect.getsource(main.bauen_auf_karte), "fehlt im Kern")

    abschnitt("3. Alias: alte Spielstaende mit 'Lager' erkennen dasselbe Gebaeude")
    check('finde_gebaeude("lager") ist lager', gelaende.finde_gebaeude("lager") == "lager",
          str(gelaende.finde_gebaeude("lager")))
    check('finde_gebaeude("Dorfzentrum") ist lager',
          gelaende.finde_gebaeude("Dorfzentrum") == "lager",
          str(gelaende.finde_gebaeude("Dorfzentrum")))
    check('finde_gebaeude("Lager") ist lager (alter Anzeigename)',
          gelaende.finde_gebaeude("Lager") == "lager", str(gelaende.finde_gebaeude("Lager")))
    check("gebaeude_name nennt das Dorfzentrum", gelaende.gebaeude_name("lager") == "Dorfzentrum",
          gelaende.gebaeude_name("lager"))
    check("eine unbekannte Kennung wird nicht zum Dorfzentrum",
          gelaende.finde_gebaeude("Rathaus") is None, str(gelaende.finde_gebaeude("Rathaus")))

    alt = main.Settlement(name="Altstand", map_id="k", x=0, y=0,
                          karte=_karte(["wald"] * 100), id="alt:0:0:0")
    alt.bauten["5"] = "Lager"
    alt.stufen["5"] = 1
    check("ein Altstand mit 'Lager' in bauten zaehlt als Dorfzentrum",
          gebaeude_wirkung.gebaeude_stufe(alt, "lager") == 1,
          str(gebaeude_wirkung.gebaeude_stufe(alt, "lager")))
    neu = _dorf(["wald"] * 100)
    neu.bauten["5"] = "Dorfzentrum"
    neu.stufen["5"] = 1
    check("ein Neustand mit 'Dorfzentrum' zaehlt ebenfalls",
          gebaeude_wirkung.gebaeude_stufe(neu, "lager") == 1,
          str(gebaeude_wirkung.gebaeude_stufe(neu, "lager")))


# --------------------------------------------------------------------------------------
def _menue():
    abschnitt("4. D-08: der Menuepunkt Lager ist ausgeblendet, die Belegliste bleibt")
    check("MENU_ITEMS ist die belegte Original-Liste mit 16 Eintraegen",
          len(main.MENU_ITEMS) == 16, str(len(main.MENU_ITEMS)))
    check("in MENU_ITEMS steht 'Lager' weiterhin (nichts geloescht)", "Lager" in main.MENU_ITEMS,
          str(main.MENU_ITEMS))
    check("MENUE_ENTFALLEN nennt Lager", main.MENUE_ENTFALLEN == {"Lager"},
          str(main.MENUE_ENTFALLEN))
    leer = main.menu_sichtbar([])
    check("ohne Siedlung steht Dorfzentrum in der Leiste", "Dorfzentrum" in leer, str(leer))
    check("ohne Siedlung steht Lager NICHT in der Leiste", "Lager" not in leer, str(leer))
    check("kein ausgeblendeter Punkt taucht je wieder auf",
          all(p not in main.MENUE_ENTFALLEN for p in leer), str(leer))

    class Ort:
        def __init__(self, bauten):
            self.bauten = {str(i): b for i, b in enumerate(bauten)}

    ohne_kaserne = main.menu_sichtbar([Ort(["stellmacher"])])
    check("Stellmacher ohne Kaserne bleibt sichtbar", "Stellmacher" in ohne_kaserne,
          str(ohne_kaserne))
    check("Stellmacher steht direkt hinter dem Dorfzentrum",
          ohne_kaserne.index("Stellmacher") == ohne_kaserne.index("Dorfzentrum") + 1,
          str(ohne_kaserne))
    mit_gilde = main.menu_sichtbar([Ort(["diebesgilde"])])
    check("Diebesgilde steht direkt hinter dem Dorfzentrum",
          mit_gilde.index("Diebesgilde") == mit_gilde.index("Dorfzentrum") + 1, str(mit_gilde))
    check("der Anker MENUE_ANKER zeigt auf Dorfzentrum", main.MENUE_ANKER == "Dorfzentrum",
          str(main.MENUE_ANKER))
    check("jeder sichtbare Punkt hat weiterhin eine Ebene",
          all(p in main.EBENE_JE_PUNKT for p in main.menu_sichtbar(
              [Ort(["kriegerakademie", "stellmacher", "bibliothek", "diebesgilde"])])),
          str([p for p in main.menu_sichtbar([]) if p not in main.EBENE_JE_PUNKT]))


# --------------------------------------------------------------------------------------
def _bauen():
    abschnitt("5. D-05: ein zweites Dorfzentrum wird vom Kern abgelehnt")
    raster = ["wald"] * 100
    siedlung = _dorf(raster)
    stufen = {"Baukunst": 1}
    ok1, text1 = main.bauen_auf_karte(siedlung, "lager", 10, forschungsstaende=stufen)
    check("das erste Dorfzentrum laesst sich bauen", ok1 and "Dorfzentrum" in text1, text1)
    check("es steht auf Feld 10 mit Stufe 1", siedlung.bauten.get("10") == "lager",
          str(siedlung.bauten.get("10")))
    vorher = (dict(siedlung.bauten), dict(siedlung.stufen))
    ok2, text2 = main.bauen_auf_karte(siedlung, "lager", 11, forschungsstaende=stufen)
    check("das zweite wird abgelehnt", ok2 is False, str(ok2))
    check("die Ablehnung nennt das Dorfzentrum", "Dorfzentrum" in text2, text2)
    check("die Ablehnung nennt die Grenze 1", "1" in text2, text2)
    check("die Ablehnung aendert nichts am Bestand (Snapshot vorher = nachher)",
          (dict(siedlung.bauten), dict(siedlung.stufen)) == vorher,
          str((siedlung.bauten, siedlung.stufen)))
    check("Feld 11 bleibt frei", "11" not in siedlung.bauten, str(sorted(siedlung.bauten)))

    # Negativprobe: derselbe Weg mit einem Gebaeude OHNE Grenze laesst sich wiederholen.
    zwei = _dorf(raster)
    a, _ = main.bauen_auf_karte(zwei, "haus", 20, forschungsstaende=stufen)
    b, _ = main.bauen_auf_karte(zwei, "haus", 21, forschungsstaende=stufen)
    check("Gegenprobe: zwei Haeuser sind erlaubt (die Wache prueft die Grenze, nicht das Bauen)",
          a and b, str((a, b)))

    abschnitt("6. Standortregel und Baukunst gelten unveraendert")
    berg = _dorf(["berg"] * 100)
    ok3, text3 = main.bauen_auf_karte(berg, "lager", 0, forschungsstaende=stufen)
    check("auf Berg wird das Dorfzentrum abgelehnt", ok3 is False, text3)
    check("die Ablehnung nennt die erlaubten Gelaendearten", "Grasland" in text3, text3)
    ohne = _dorf(raster)
    ok4, text4 = main.bauen_auf_karte(ohne, "lager", 0)
    check("ohne Baukunst Stufe 1 wird es abgelehnt (kein Freipass)", ok4 is False, text4)
    check("die Ablehnung nennt Baukunst", "Baukunst" in text4, text4)


# --------------------------------------------------------------------------------------
class _AbrissAttrappe:
    """Minimaler Aufrufer fuer die ECHTE Methode `_karten_abreissen` (kein Fenster)."""

    def __init__(self, siedlung, feld):
        self.karten_siedlung = siedlung
        self.karten_feld = feld
        self.state = types.SimpleNamespace(_lokale_kasse_aktiv=lambda: False,
                                           admin_teststand=False,
                                           settlements=[siedlung])
        self.root = None
        self.log = []

    def _log(self, text):
        self.log.append(text)


def _abriss():
    abschnitt("7. D-06: das einzige Dorfzentrum ist nicht abreissbar")
    siedlung = _dorf(["wald"] * 100)
    siedlung.bauten["10"] = "lager"
    siedlung.stufen["10"] = 1
    attrappe = _AbrissAttrappe(siedlung, 10)
    main.NebelseetalApp._karten_abreissen(attrappe)
    check("das Dorfzentrum steht nach dem Abrissversuch noch",
          siedlung.bauten.get("10") == "lager", str(siedlung.bauten))
    check("die Meldung nennt das Dorfzentrum",
          any("Dorfzentrum" in t for t in attrappe.log), str(attrappe.log))
    check("die Meldung nennt den Grund (Lager des Dorfes)",
          any("Lager" in t for t in attrappe.log), str(attrappe.log))

    # Gegenprobe: ein normales Gebaeude laesst sich im selben Weg abtragen.
    zweite = _dorf(["wald"] * 100)
    zweite.bauten["12"] = "haus"
    zweite.stufen["12"] = 1
    zweite.karten_feld = None
    att2 = _AbrissAttrappe(zweite, 12)
    att2._menue_auffrischen = lambda: None
    att2._render_view = lambda: None
    main.NebelseetalApp._karten_abreissen(att2)
    check("Gegenprobe: ein Haus wird abgerissen (die Wache sperrt nur das Dorfzentrum)",
          "12" not in zweite.bauten, str(zweite.bauten))

    # Auch der alte Anzeigename 'Lager' ist geschuetzt (Altstand).
    dritte = _dorf(["wald"] * 100)
    dritte.bauten["13"] = "Lager"
    dritte.stufen["13"] = 1
    att3 = _AbrissAttrappe(dritte, 13)
    main.NebelseetalApp._karten_abreissen(att3)
    check("auch ein Altstand mit dem Namen 'Lager' ist geschuetzt",
          dritte.bauten.get("13") == "Lager", str(dritte.bauten))


# --------------------------------------------------------------------------------------
def _ansicht():
    abschnitt("8. D-07: EINE Lageransicht im Dorfzentrum")
    signatur = inspect.signature(main.NebelseetalApp._render_storage)
    check("_render_storage hat den Schalter eigener_titel",
          "eigener_titel" in signatur.parameters, str(signatur))
    check("der Vorgabewert ist True (direkter Aufruf zeigt den Vermerk)",
          signatur.parameters["eigener_titel"].default is True, str(signatur))
    # ANGEPASST 13.11.2026 (Nr. 16, Teil A): Die Dorfzentrum-Ansicht ist jetzt eine Spalte mit
    # sieben Bloecken und einer Arbeitsflaeche mit drei Reitern; der Reiter "Lager" zeigt die
    # Lagerverwaltung ueber `_dz_lager`. Die ENTSCHEIDUNG D-07 (EINE Lageransicht) gilt
    # unveraendert - darum wird geprueft, dass BEIDE Wege dieselbe Rasterfunktion benutzen,
    # statt dass eine Methode die andere aufruft.
    rumpf = _code(main.NebelseetalApp._render_overview)
    _bau = " ".join(_code(getattr(main.NebelseetalApp, _n))
                    for _n in ("_render_overview", "_dz_arbeitsflaeche", "_dz_lager"))
    check("das Dorfzentrum zeigt die Lagerverwaltung ueber `_dz_lager`",
          "_dz_lager" in _bau, rumpf[-400:])
    _lager_rumpf = _code(main.NebelseetalApp._render_storage)
    check("die stillgelegte Route benutzt DIESELBE Rasterfunktion (eine Anzeige, zwei Wege)",
          "_dz_lager" in _lager_rumpf and "_dz_werkstaetten" in _lager_rumpf, _lager_rumpf[-400:])
    _ort_rumpf = " ".join(_code(getattr(main.NebelseetalApp, _n))
                          for _n in ("_dz_block_ort", "_dz_block_aktionen"))
    check("die Dorfzentrum-Ansicht liest den Gebaeudestand ueber gebaeude_stufe",
          'gebaeude_stufe' in _ort_rumpf, _ort_rumpf[-600:])
    check("kein zweiter Lagerbestand: die Ansicht rechnet keine Vorraete selbst",
          "vorraete" not in rumpf, rumpf[-400:])
    quelle = inspect.getsource(main.NebelseetalApp._render_storage)
    check("der alte Debug-Ausdruck ist entfernt",
          "[DEBUG] _render_storage" not in inspect.getsource(main), "der Ausdruck steht noch in main.py")
    check("die stillgelegte Route sagt es offen", "stillgelegt" in quelle, quelle[:400])


# --------------------------------------------------------------------------------------
def _gui():
    abschnitt("9. Echter Aufbau: Dorfzentrum zeigt die Lagerverwaltung im Fenster")
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    try:
        app = main.NebelseetalApp(root)
        app._build_main_ui()
        app._erste_siedlung_gruenden()
        check("die Gruendung hat eine Siedlung erzeugt", len(app.state.settlements) == 1,
              str(len(app.state.settlements)))

        def texte(sammler=None):
            sammler = [] if sammler is None else sammler
            for kind in app.content.winfo_children():
                _sammle(kind, sammler)
            return sammler

        def _sammle(widget, sammler):
            try:
                t = widget.cget("text")
            except Exception:
                t = ""
            if t:
                sammler.append(str(t))
            for kind in widget.winfo_children():
                _sammle(kind, sammler)

        app._switch_view("Dorfzentrum")
        gesamt = " | ".join(t for t in texte())
        check("die Dorfzentrum-Ansicht zeichnet", len(gesamt) > 100, str(len(gesamt)) + " Zeichen")
        check("die Lagerverwaltung steht im Dorfzentrum",
              "Lagerverwaltung dieses Dorfes" in gesamt, "Text: " + gesamt[:120])
        check("die Waren des Ortes stehen dort", "Waren vor Ort" in gesamt)
        check("die Werkstaetten stehen dort", "Werkst" in gesamt)
        check("der Gebaeudestand des Dorfzentrums wird genannt",
              "Dorfzentrum als Geb" in gesamt)
        check("die Ansicht behauptet NICHT, Lager sei noch ein Menuepunkt",
              "stillgelegt" not in gesamt)

        app._switch_view("Lager")
        alt = " | ".join(t for t in texte())
        check("die alte Route bleibt erreichbar und nennt sich stillgelegt",
              "stillgelegt" in alt, alt[:120])
        check("die alte Route zeigt weiterhin Bestaende (kein Absturz)",
              "Waren" in alt or "Ortslager" in alt)
    finally:
        try:
            root.destroy()
        except Exception:
            pass



# --------------------------------------------------------------------------------------
def _platzwahl():
    abschnitt("10. S-2c-D: das Dorfzentrum kommt mit, den PLATZ bestimmt der Spieler")
    from dataclasses import asdict
    leer = main.Settlement(name="X", map_id="k", x=0, y=0)
    check("ein Ort traegt das Kennzeichen dorfzentrum_offen",
          hasattr(leer, "dorfzentrum_offen"), "Feld fehlt")
    check("der Vorgabewert ist False", leer.dorfzentrum_offen is False,
          str(leer.dorfzentrum_offen))
    alt = {k: v for k, v in asdict(leer).items() if k != "dorfzentrum_offen"}
    wieder = main.Settlement(**alt)
    check("ein Altstand OHNE das Feld laedt mit False (keine Migration)",
          wieder.dorfzentrum_offen is False, str(wieder.dorfzentrum_offen))

    rumpf = _code(main.NebelseetalApp._render_settlement_map)
    check("die Siedlungskarte bietet das Setzen an", "_dorfzentrum_setzen" in rumpf,
          "Aufruf fehlt in der Kartenansicht")
    check("der kostenlose Weg verlangt keine Baukunst (kein bauen_auf_karte)",
          "bauen_auf_karte" not in _code(main.NebelseetalApp._dorfzentrum_setzen),
          "der freie Weg darf nicht ueber den bezahlten laufen")

    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    try:
        app = main.NebelseetalApp(root)
        app._build_main_ui()
        app._erste_siedlung_gruenden()
        ort = app.state.settlements[0]
        check("die Gruendung liefert das Dorfzentrum als offenen Platz",
              ort.dorfzentrum_offen is True, str(ort.dorfzentrum_offen))
        check("die Gruendung setzt es NICHT selbst auf ein Feld",
              gebaeude_wirkung.gebaeude_stufe(ort, "lager") == 0,
              str(sorted((ort.bauten or {}).values())))
        check("die drei Startgebaeude aus S-1 stehen unveraendert",
              len(ort.bauten) == 3, str(len(ort.bauten)))

        raster = list(ort.karte["raster"])
        frei = next((i for i, art in enumerate(raster)
                     if str(i) not in ort.bauten
                     and gelaende.bau_moeglich("lager", art)[0]), None)
        sperr = next((i for i, art in enumerate(raster)
                      if str(i) not in ort.bauten
                      and not gelaende.bau_moeglich("lager", art)[0]), None)
        belegt = next(iter(sorted(ort.bauten)), None)
        check("die Testkarte hat ein freies, erlaubtes Feld", frei is not None, str(raster))
        vorher_vorr = dict(ort.vorraete)
        vorher_bev = float(ort.bevoelkerung)
        app.karten_siedlung = ort
        app.karten_feld = frei

        if belegt is not None:
            ok_belegt = app._dorfzentrum_setzen(int(belegt))
            check("auf einem belegten Feld wird es abgelehnt", ok_belegt is False, str(ok_belegt))
            check("die Ablehnung aendert nichts",
                  ort.dorfzentrum_offen is True and gebaeude_wirkung.gebaeude_stufe(
                      ort, "lager") == 0, str(ort.bauten))

        if sperr is not None:
            ok_sperr = app._dorfzentrum_setzen(int(sperr))
            check("auf unzulaessigem Gelaende wird es abgelehnt (Standortregel)",
                  ok_sperr is False, str(ok_sperr))
            check("auch dort bleibt alles offen", ort.dorfzentrum_offen is True,
                  str(ort.dorfzentrum_offen))

        ok = app._dorfzentrum_setzen(int(frei))
        check("auf dem gewaehlten freien Feld wird es gesetzt", ok is True, str(ok))
        check("es steht Stufe 1 auf genau diesem Feld",
              ort.bauten.get(str(frei)) == "lager" and ort.stufen.get(str(frei)) == 1,
              str((frei, ort.bauten.get(str(frei)), ort.stufen.get(str(frei)))))
        check("das Kennzeichen ist danach geloescht", ort.dorfzentrum_offen is False,
              str(ort.dorfzentrum_offen))
        check("das Setzen kostet NICHTS (Startvorraete unveraendert)",
              dict(ort.vorraete) == vorher_vorr, str(ort.vorraete))
        check("es bindet keine Siedler", float(ort.bevoelkerung) == vorher_bev,
              str(ort.bevoelkerung))
        check("genau ein Dorfzentrum im Dorf",
              sum(1 for g in ort.bauten.values() if gelaende.finde_gebaeude(g) == "lager") == 1,
              str(ort.bauten))
        ok2 = app._dorfzentrum_setzen(int(frei))
        check("ein zweiter Aufruf wird abgelehnt", ok2 is False, str(ok2))
        check("es bleibt bei genau einem Dorfzentrum",
              sum(1 for g in ort.bauten.values() if gelaende.finde_gebaeude(g) == "lager") == 1,
              str(ort.bauten))
    finally:
        try:
            root.destroy()
        except Exception:
            pass


def main_lauf():
    for teil in (_daten, _menue, _bauen, _abriss, _ansicht, _platzwahl):
        try:
            teil()
        except Exception as fehler:  # noqa: BLE001
            ausnahme(f"Abschnitt {teil.__name__}", fehler)
    try:
        _gui()
    except Exception as fehler:  # noqa: BLE001
        ausnahme("Abschnitt GUI", fehler)
    return bericht()


if __name__ == "__main__":
    sys.exit(main_lauf())
