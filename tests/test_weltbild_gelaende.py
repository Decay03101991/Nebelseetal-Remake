# -*- coding: ascii -*-
"""Schnitt S-5: das Weltbild als Gelaende (Register 91 Vorgabe, 92 Freigabe).

Daniel 01.11.2026, Antwort auf die gesammelte Frage:
"A: sieben vorhandene Gelaendearten mit ihren Gewichten aus data/gelaende.json,
als 2x2-Bloecke mit stabilem Seed je Welt".

Was diese Pruefdatei belegt:
  1. EINE Quelle: die sieben Gelaendearten und ihre Haeufigkeit kommen aus
     data/gelaende.json (Summe 100); es gibt keine zweite Gewichtstabelle.
  2. Je Weltkarte 400 gueltige Gelaende-IDs auf 20 x 20 Feldern.
  3. Exakt 4 x haeufigkeit Felder je Art (20 -> 80, 7 -> 28, ...).
  4. Die Felder stehen in 2 x 2-Bloecken: 100 Gruppen, jede gleichartig.
  5. Gleicher Weltname und gleicher Seed ergeben ein BYTEGLEICHES Raster - auch
     in einem frischen Interpreter (Neustart); andere Welt oder anderer Seed
     ergeben ein anderes Raster.
  6. Keine dauerhaften Markierungen: die Felder tragen nur Gelaende, Bannerfarbe
     und Status - keine Orte, Doerfer, Gegner oder Nummern.
  7. Ungueltige Welt, ungueltiger Index, Feld ausserhalb, bool als Koordinate,
     leerer Seed und eine kaputte Verteilung werden ERKLAERT ABGELEHNT; es wird
     kein Ersatzraster erfunden.
  8. Ein Feldklick bucht nichts (kein Mana, kein Gold, kein Dorf).
  9. Das Gelaende hat KEINE Ertragswirkung: die Produktion ist vor und nach einem
     Weltwechsel gleich, und ausser portalraum/main liest kein Modul das Weltbild.

Aufruf: python -X utf8 tests/test_weltbild_gelaende.py
"""
import hashlib
import json
import os
import random
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
os.chdir(SRC)

import gelaende  # noqa: E402
import main  # noqa: E402
import portalraum  # noqa: E402

BLOCK = 2
KANTE = 20
FELDER = 400
GRUPPEN = (KANTE // BLOCK) ** 2

FELD_SCHLUESSEL = {"x", "y", "z", "eigen", "status", "farbe", "gelaende",
                   "gelaende_name", "gelaende_farbe", "gelaende_bebaubar", "gelaende_grund"}
WELTNAMEN = ("Armageddon", "Ragnaroek", "Utgard", "Midgard", "Valhalla", "Limbus")


def _datei() -> dict:
    with open(os.path.join(ROOT, "data", "gelaende.json"), encoding="utf-8") as f:
        return json.load(f)


def _raster_hash(raster) -> str:
    return hashlib.sha256(repr(raster).encode("utf-8")).hexdigest()


def _pruefungen_quelle():
    abschnitt("1. EINE Quelle: data/gelaende.json, sieben Arten, Summe 100")
    daten = _datei()
    arten = daten["gelaendearten"]
    check("data/gelaende.json fuehrt genau sieben Gelaendearten",
          len(arten) == 7, str(len(arten)))
    check("jede Art hat eine Kennung, einen Namen, eine Haeufigkeit und eine Farbe",
          all(a.get("id") and a.get("name") and int(a.get("haeufigkeit", 0)) > 0
              and str(a.get("farbe", "")).startswith("#") for a in arten),
          str([a.get("id") for a in arten]))
    summe = sum(int(a["haeufigkeit"]) for a in arten)
    check("die Haeufigkeiten summieren sich auf 100 Gruppen", summe == 100, str(summe))
    aus_datei = {a["id"]: int(a["haeufigkeit"]) for a in arten}
    aus_modul = dict(portalraum.gelaendeverteilung())
    check("portalraum.gelaendeverteilung liest dieselben Werte wie die Datei",
          aus_modul == aus_datei, str(aus_modul))
    check("die Verteilung nennt Grasland 20, Steppe 20, Wald 18, Huegel 13, Berg 12, "
          "Nebelsee 7, Sumpf 10",
          aus_modul == {"grasland": 20, "steppe": 20, "wald": 18, "huegel": 13,
                        "berg": 12, "nebelsee": 7, "sumpf": 10}, str(aus_modul))
    check("der Block ist 2 x 2 Felder und es gibt 100 Gruppen",
          portalraum.GELAENDE_BLOCK == 2 and portalraum._GRUPPEN == 100,
          str((portalraum.GELAENDE_BLOCK, portalraum._GRUPPEN)))
    check("der Seed steht als Konfigurationswert in data/welten.json",
          isinstance(portalraum.weltkarten_seed(), str) and len(portalraum.weltkarten_seed()) > 0,
          portalraum.weltkarten_seed())


def _pruefungen_raster():
    abschnitt("2. Je Weltkarte 20 x 20 = 400 gueltige Gelaende-IDs")
    gueltig = set(gelaende.GELAENDEARTEN)
    for nummer in range(1, portalraum.dim_zahl() + 1):
        bild = portalraum.weltbild(nummer)
        raster = bild["raster"]
        kennung = bild["kennung"]
        check(f"{kennung}: 20 Zeilen mit je 20 Feldern",
              len(raster) == KANTE and all(len(z) == KANTE for z in raster),
              str((len(raster), sorted({len(z) for z in raster}))))
        flach = [art for z in raster for art in z]
        check(f"{kennung}: genau 400 Felder", len(flach) == FELDER, str(len(flach)))
        fremd = sorted({art for art in flach if art not in gueltig})
        check(f"{kennung}: jede Feld-ID stammt aus data/gelaende.json", not fremd, str(fremd))
    check("alle 20 Weltkarten sind baubar (kein Zufallsersatz noetig)",
          portalraum.dim_zahl() == 20, str(portalraum.dim_zahl()))


def _pruefungen_verteilung():
    abschnitt("3. Exakt 4 x haeufigkeit Felder je Art")
    verteilung = dict(portalraum.gelaendeverteilung())
    for welt in WELTNAMEN:
        bild = portalraum.weltbild(welt)
        zaehlung = bild["zaehlung"]
        soll = {art: BLOCK * BLOCK * haeufig for art, haeufig in verteilung.items()}
        check(f"{welt}: jede Art hat genau 4 x ihre Haeufigkeit an Feldern",
              zaehlung == soll, str(zaehlung))
        check(f"{welt}: die Zaehlung summiert sich auf 400",
              sum(zaehlung.values()) == FELDER, str(sum(zaehlung.values())))
    bild = portalraum.weltbild("Midgard")
    check("Grasland 20 Gruppen ergibt 80 Felder", bild["zaehlung"]["grasland"] == 80,
          str(bild["zaehlung"]["grasland"]))
    check("Nebelsee 7 Gruppen ergibt 28 Felder", bild["zaehlung"]["nebelsee"] == 28,
          str(bild["zaehlung"]["nebelsee"]))


def _pruefungen_bloecke():
    abschnitt("4. Die Felder stehen in 2 x 2-Bloecken (100 Gruppen, je gleichartig)")
    bild = portalraum.weltbild("Midgard")
    raster = bild["raster"]
    ungleich = []
    gruppen_je_art = {}
    for gy in range(0, KANTE, BLOCK):
        for gx in range(0, KANTE, BLOCK):
            arten = {raster[y][x] for y in range(gy, gy + BLOCK) for x in range(gx, gx + BLOCK)}
            if len(arten) != 1:
                ungleich.append((gx, gy, sorted(arten)))
            else:
                art = arten.pop()
                gruppen_je_art[art] = gruppen_je_art.get(art, 0) + 1
    check("kein 2 x 2-Block ist gemischt", not ungleich, str(ungleich[:3]))
    check("es gibt genau 100 Gruppen", sum(gruppen_je_art.values()) == GRUPPEN,
          str(sum(gruppen_je_art.values())))
    check("die Gruppenanzahl je Art ist die Haeufigkeit aus der Datei",
          gruppen_je_art == dict(portalraum.gelaendeverteilung()), str(gruppen_je_art))


def _pruefungen_stabilitaet():
    abschnitt("5. Stabiler Seed: gleiche Welt gleich, andere Welt anders, auch nach Neustart")
    a = portalraum.weltbild("Midgard")
    b = portalraum.weltbild("Midgard")
    check("zwei Aufrufe mit gleichem Namen und gleichem Seed sind bytegleich",
          repr(a["raster"]) == repr(b["raster"]), _raster_hash(a["raster"]))
    check("die Kennung d04 ergibt dasselbe Raster wie der Name Midgard",
          repr(portalraum.weltbild("d04")["raster"]) == repr(a["raster"]), "")
    check("die Nummer 4 ergibt dasselbe Raster wie der Name Midgard",
          repr(portalraum.weltbild(4)["raster"]) == repr(a["raster"]), "")
    check("dasselbe Raster kommt auch ohne Zwischenspeicher heraus",
          repr(portalraum.weltbild("Midgard", seed=a["seed"])["raster"]) == repr(a["raster"]), "")

    skript = ("import sys;sys.path.insert(0,%r);import hashlib,portalraum as P;"
              "print(hashlib.sha256(repr(P.weltbild('Midgard')['raster']).encode()).hexdigest())"
              % SRC)
    lauf = subprocess.run([sys.executable, "-X", "utf8", "-c", skript],
                          capture_output=True, text=True, cwd=SRC)
    frisch = (lauf.stdout or "").strip()
    check("ein FRISCHER Interpreter baut dasselbe Raster (Seed haengt nicht am Prozess)",
          frisch == _raster_hash(a["raster"]), repr((frisch, lauf.stderr[-120:] if lauf.stderr else "")))

    andere = portalraum.weltbild("Valhalla")
    check("eine andere Welt ergibt ein anderes Raster",
          repr(andere["raster"]) != repr(a["raster"]), _raster_hash(andere["raster"]))
    hashes = {_raster_hash(portalraum.weltbild(n)["raster"]) for n in WELTNAMEN}
    check("alle sechs belegten Weltnamen haben verschiedene Raster", len(hashes) == 6,
          str(len(hashes)))
    anderer_seed = portalraum.weltbild("Midgard", seed="ein-anderer-seed")
    check("ein anderer Seed ergibt ein anderes Raster",
          repr(anderer_seed["raster"]) != repr(a["raster"]), _raster_hash(anderer_seed["raster"]))
    check("das Raster ist ein reines Gelaende-Raster - gleiche Verteilung, andere Lage",
          anderer_seed["zaehlung"] == a["zaehlung"], str(anderer_seed["zaehlung"]))

    quelle = portalraum._seed_zahl.__code__.co_names
    check("der Seed wird aus SHA-256 abgeleitet", "sha256" in quelle and "digest" in quelle,
          str(quelle))
    check("hash() kommt in der Seed-Ableitung nicht vor", "hash" not in quelle, str(quelle))
    namen = set(portalraum.weltbild.__code__.co_names) | set(quelle)
    check("die Uhrzeit geht in das Raster nicht ein",
          not ({"time", "now", "datetime", "today"} & namen), str(sorted(namen)))
    check("zwei Aufrufe kurz hintereinander bleiben gleich",
          repr(portalraum.weltbild("Utgard")["raster"]) == repr(portalraum.weltbild("Utgard")["raster"]),
          "")
    with open(os.path.join(ROOT, "data", "welten.json"), encoding="utf-8") as f:
        datei_seed = json.load(f)["weltkarten_seed"]
    check("der gelesene Seed ist genau der Wert aus data/welten.json",
          portalraum.weltkarten_seed() == str(datei_seed),
          str((portalraum.weltkarten_seed(), datei_seed)))


def _pruefungen_keine_markierungen():
    abschnitt("6. Keine dauerhaften Markierungen im Raster")
    eigener_index = portalraum.index_von(4)
    felder = portalraum.anzeige_raster(eigener_index, 10, [eigener_index])
    check("das Raster hat 400 Felder", len(felder) == FELDER, str(len(felder)))
    schluessel = set(felder[0])
    check("die Felder tragen genau die dokumentierten Schluessel",
          schluessel == FELD_SCHLUESSEL, str(sorted(schluessel)))
    verboten = ("ort", "dorf", "gegner", "bot", "nummer", "marker", "besitzer", "welt_id")
    treffer = sorted(k for k in schluessel if any(w in k for w in verboten))
    check("kein Feld traegt Orte, Doerfer, Gegner, Nummern oder Markierungen", not treffer,
          str(treffer))
    check("jedes Feld traegt ein Gelaende", all(f["gelaende"] for f in felder), "")
    check("jedes Feld nennt Namen und Farbe seines Gelaendes",
          all(f["gelaende_name"] and f["gelaende_farbe"] for f in felder), "")
    check("die Bannerfarbe bleibt die belegte Originalanzeige",
          all(f["farbe"] == "gruen" for f in felder), str({f["farbe"] for f in felder}))
    arten = {f["gelaende"] for f in felder}
    check("im Raster kommen nur Arten aus data/gelaende.json vor",
          arten <= set(gelaende.GELAENDEARTEN), str(sorted(arten)))
    check("kein Feld meldet einen Ablehnungsgrund", all(not f["gelaende_grund"] for f in felder),
          "")


def _pruefungen_ablehnung():
    abschnitt("7. Ungueltige Eingaben werden erklaert abgelehnt, nichts wird erfunden")

    def _grund(fn, *a, **k):
        try:
            fn(*a, **k)
        except portalraum.WeltbildFehler as fehler:
            return str(fehler)
        except Exception as fehler:  # falsche Fehlerart ist auch ein Befund
            return "FALSCHE ART: " + repr(fehler)
        return ""

    text = _grund(portalraum.weltbild, "Nirgendwo")
    check("eine unbekannte Welt wird abgelehnt", bool(text) and "Unbekannte Weltkarte" in text,
          text)
    check("die Ablehnung nennt die bekannten Kennungen",
          "d01" in text and "d20" in text, text)
    check("ein Index ausserhalb 0..19 wird beim Bau abgelehnt",
          "Unbekannte Weltkarte" in _grund(portalraum.weltbild, 21), _grund(portalraum.weltbild, 21))
    check("ein Feld ausserhalb des Rasters wird abgelehnt",
          "ausserhalb" in _grund(portalraum.gelaende_von_feld, "Midgard", 20, 5),
          _grund(portalraum.gelaende_von_feld, "Midgard", 20, 5))
    check("ein negatives Feld wird abgelehnt",
          "ausserhalb" in _grund(portalraum.gelaende_von_feld, "Midgard", -1, 0), "")
    check("True als Koordinate wird abgelehnt (bool ist keine Zahl)",
          "ganze Zahlen" in _grund(portalraum.gelaende_von_feld, "Midgard", True, 0),
          _grund(portalraum.gelaende_von_feld, "Midgard", True, 0))
    check("ein leerer Seed wird abgelehnt",
          "Leerer Seed" in _grund(portalraum.weltbild, "Midgard", ""), "")
    echt_seed = portalraum._DATEN.get("weltkarten_seed")
    portalraum._DATEN.pop("weltkarten_seed", None)
    portalraum._WELTBILDER.clear()
    try:
        meldung = _grund(portalraum.weltbild, "Midgard")
    finally:
        portalraum._DATEN["weltkarten_seed"] = echt_seed
        portalraum._WELTBILDER.clear()
    check("ein fehlender weltkarten_seed wird erklaert abgelehnt",
          "weltkarten_seed" in meldung, meldung)

    felder = portalraum.anzeige_raster(99)
    check("ein ungueltiger Index liefert Felder OHNE Gelaende",
          all(f["gelaende"] is None for f in felder), str({f["gelaende"] for f in felder}))
    check("dazu nennt jedes Feld den Grund",
          all("Unbekannte Weltkarte" in f["gelaende_grund"] for f in felder),
          felder[0]["gelaende_grund"])

    kaputt = [("grasland", 20), ("steppe", 20)]
    echt = portalraum.gelaendeverteilung
    portalraum.gelaendeverteilung = lambda: kaputt
    portalraum._WELTBILDER.clear()
    try:
        meldung = _grund(portalraum.weltbild, "Ragnaroek", "kaputt")
    finally:
        portalraum.gelaendeverteilung = echt
        portalraum._WELTBILDER.clear()
    check("eine Verteilung, die nicht 100 Gruppen ergibt, wird abgelehnt",
          "40 Gruppen" in meldung and "100" in meldung, meldung)


def _pruefungen_fenster():
    abschnitt("8. Fenster: der Feldklick bucht nichts, die Ansicht zeigt Gelaende")
    import inspect
    quelle = inspect.getsource(main.NebelseetalApp._render_portal)
    check("die Ansicht faerbt jedes Feld mit seiner Gelaendefarbe",
          "gelaende_farbe" in quelle, "")
    check("die Ansicht baut die Legende aus portalraum.legende",
          "portalraum.legende()" in quelle, "")
    check("die Ansicht nennt einen Ablehnungsgrund, statt Gelaende zu erfinden",
          "gelaende_grund" in quelle, "")
    text = main.NebelseetalApp._render_portal.__doc__ or ""
    check("die Ansicht nennt die Herkunft des Gelaendes (S-5)",
          "S-5" in text and "Gelaende" in text, "")
    check("die Legende hat sieben Eintraege", len(portalraum.legende()) == 7,
          str(len(portalraum.legende())))
    check("die Legende nennt Namen und Farbe aus der Datei",
          all(e["name"] and str(e["farbe"]).startswith("#") for e in portalraum.legende()),
          str(portalraum.legende()))
    try:
        import tkinter as tk
    except Exception as fehler:
        check("tkinter vorhanden", False, repr(fehler))
        return
    random.seed(20261101)
    root = tk.Tk()
    root.withdraw()
    try:
        app = main.NebelseetalApp(root)
        app._build_main_ui()
        root.update()
        app._switch_view("Portal")
        root.update_idletasks()
        check("die Portalansicht rendert mit Gelaende", app.current_view == "Portal",
              str(app.current_view))
        vorher = (float(app.state.resources["mana"].amount),
                  float(app.state.resources["gold"].amount),
                  len(app.state.settlements), len(app.state.auftraege))
        gel = portalraum.gelaende_von_feld(int(app.state.eigene_dimension), 3, 7)
        check("das Feld 3/7 der Startwelt hat ein Gelaende", bool(gel["gelaende"]), str(gel))
        check("ein Klick auf Feld 3/7 waehlt es an", app._portal_feld_waehlen(3, 7) is True, "")
        nachher = (float(app.state.resources["mana"].amount),
                   float(app.state.resources["gold"].amount),
                   len(app.state.settlements), len(app.state.auftraege))
        check("der Klick bucht kein Mana, kein Gold, kein Dorf und keinen Auftrag",
              vorher == nachher, str((vorher, nachher)))
        check("die Anwahl selbst steht nur in der Ansicht",
              getattr(app, "portal_auswahl", None) == (3, 7), str(app.portal_auswahl))
        # Zaehlweisen: der Spielstand fuehrt Nummern (d04 = 4), das Raster Indizes (0..19).
        nummer = int(app.state.eigene_dimension)
        felder = portalraum.anzeige_raster(
            portalraum.index_von(nummer), 10,
            [portalraum.index_von(n) for n in app.state.eigene_dimensionen])
        check("die EIGENE Weltkarte ist im Kaestchen als eigene markiert",
              all(f["status"] == "eigen" for f in felder), str({f["status"] for f in felder}))
        check("die Ansicht rechnet die Nummern vor dem Raster in Indizes um",
              "index_von" in quelle, "")
    finally:
        try:
            root.destroy()
        except Exception:
            pass


def _pruefungen_ertrag():
    abschnitt("9. Keine Ertragswirkung: Produktion vor und nach dem Weltwechsel gleich")
    try:
        import tkinter as tk
    except Exception as fehler:
        check("tkinter vorhanden", False, repr(fehler))
        return
    random.seed(20261101)
    root = tk.Tk()
    root.withdraw()
    try:
        app = main.NebelseetalApp(root)
        app._build_main_ui()
        root.update()
        app._erste_siedlung_gruenden()
        root.update()
        ort = app.state.settlements[0]

        def stand():
            return {k: round(float(v), 4) for k, v in (ort.vorraete or {}).items()}

        app.state.tick(3600.0)
        a = stand()
        app.state.tick(3600.0)
        b = stand()
        alt = int(app.state.eigene_dimension)
        andere = 5 if alt != 5 else 4
        app.state.eigene_dimension = andere
        app.state.tick(3600.0)
        c = stand()
        delta1 = {k: round(b.get(k, 0.0) - a.get(k, 0.0), 4) for k in set(a) | set(b)}
        delta2 = {k: round(c.get(k, 0.0) - b.get(k, 0.0), 4) for k in set(b) | set(c)}
        check("der Weltwechsel aendert die Ernte je Stunde nicht", delta1 == delta2,
              str([(k, delta1.get(k), delta2.get(k)) for k in delta1 if delta1.get(k) != delta2.get(k)]))
        check("die Weltkarte ist wirklich gewechselt",
              int(app.state.eigene_dimension) == andere,
              str((alt, app.state.eigene_dimension)))
        check("die Siedlung bleibt dieselbe", len(app.state.settlements) == 1,
              str(len(app.state.settlements)))

        leser = []
        for name in sorted(os.listdir(SRC)):
            if not name.endswith(".py"):
                continue
            pfad = os.path.join(SRC, name)
            with open(pfad, encoding="utf-8") as f:
                text = f.read()
            for wort in ("weltbild(", "gelaende_von_feld(", "portalraum.legende("):
                if wort in text and name not in ("portalraum.py", "main.py"):
                    leser.append((name, wort))
        check("ausser portalraum und main liest kein Modul das Weltbild", not leser, str(leser))
    finally:
        try:
            root.destroy()
        except Exception:
            pass


def main_lauf() -> int:
    _pruefungen_quelle()
    _pruefungen_raster()
    _pruefungen_verteilung()
    _pruefungen_bloecke()
    _pruefungen_stabilitaet()
    _pruefungen_keine_markierungen()
    _pruefungen_ablehnung()
    _pruefungen_fenster()
    _pruefungen_ertrag()
    return bericht()


if __name__ == "__main__":
    sys.exit(main_lauf())
