# -*- coding: ascii -*-
"""Schnitt S-2b: die Portal-Uebersicht - Weltkartenliste oben, Gelaendekaestchen darunter.

Daniel 01.11.2026 (docs/KONZEPT_WELTKARTEN_UND_BOTS_20261101.md):
  * Frage 26/31: "Es gibt immer die sechs Weltkarten Armageddon, Ragnaroek, Utgard, Midgard,
    Valhalla und Limbus. Sie bilden die gesamte Spielwelt." Bespielbar sind ZUERST Midgard und
    Valhalla, die uebrigen vier folgen spaeter.
  * Frage 22: Startwelt ist Midgard.
  * Frage 30: "oben die Liste der Weltkarten mit Namen, darunter das Gelaendekaestchen der
    aktuellen Welt zum Anklicken".
  * Frage 23: der Dorftransfer beginnt mit einem Klick aufs freie Feld.
  * Anhang 2 ("Umzug mit laufenden Auftraegen"): "ein weltenwechsel ist fuer das dorf gar nicht
    moeglich solange auftraege einheiten truppen oder sonst was unterwegs ist auch handel z. b."

Diese Pruefdatei wacht ueber die Liste, die Zaehlweise (Nummer 1..20 gegen Index 0..19), die
Startwelt, die Sperre bei laufenden Auftraegen und die Anwahl eines Feldes.
Aufruf: python -X utf8 tests/test_portal_uebersicht.py
"""
import ast
import inspect
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
os.chdir(SRC)

import main  # noqa: E402
import portalraum  # noqa: E402
import welt  # noqa: E402
import auftraege  # noqa: E402

WELTNAMEN = ("Armageddon", "Ragnaroek", "Utgard", "Midgard", "Valhalla", "Limbus")


def _code(funktion) -> str:
    """Quelltext einer Funktion OHNE Docstring (ein Docstring darf den alten Begriff erklaeren)."""
    baum = ast.parse(textwrap.dedent(inspect.getsource(inspect.unwrap(funktion))))
    rumpf = baum.body[0].body
    if (rumpf and isinstance(rumpf[0], ast.Expr) and isinstance(rumpf[0].value, ast.Constant)
            and isinstance(rumpf[0].value.value, str)):
        rumpf = rumpf[1:]
    baum.body[0].body = rumpf or [ast.Pass()]
    return ast.unparse(baum)


def _laufender_auftrag(start: float = 0.0, reisezeit: float = 100.0) -> dict:
    """Ein Auftrag, der zur Spielzeit 0 gerade auf der Hinreise ist (kein echter Start noetig)."""
    return {"art": "transport", "start": start, "reisezeit": reisezeit, "aktion_dauer": 0.0,
            "einheiten": {"Krieger": 1}, "von": "A", "nach": "B"}


def _pruefungen_liste():
    # ENTSCHEIDUNG GEAENDERT (Daniel 04.11.2026, 21:0x): alle sechs Welten sind bespielbar.
    # Vorher galt die Regel vom 01.11.2026 "zuerst Midgard und Valhalla".
    abschnitt("1. Die Weltkartenliste: sechs belegte Namen, alle sechs bespielbar")
    zeilen = portalraum.weltkarten([4], 0)
    check("die Liste hat genau sechs Zeilen", len(zeilen) == 6, str(len(zeilen)))
    check("die Namen stehen in der belegten Reihenfolge",
          tuple(z["name"] for z in zeilen) == WELTNAMEN, str([z["name"] for z in zeilen]))
    check("jede Zeile nennt ihre Kennung passend zur Nummer",
          all(z["kennung"] == f"d{z['nummer']:02d}" for z in zeilen),
          str([(z["nummer"], z["kennung"]) for z in zeilen]))
    check("alle sechs Weltkarten sind bespielbar (Daniel 04.11.2026)",
          [z["name"] for z in zeilen if z["spielbar"]] == list(WELTNAMEN),
          str([(z["name"], z["spielbar"]) for z in zeilen]))
    midgard = next(z for z in zeilen if z["name"] == "Midgard")
    check("die eigene Welt ist als eigene Welt gekennzeichnet",
          midgard["status"] == "eigen" and midgard["status_text"] == "eigene Welt",
          str(midgard))
    check("die eigene Welt traegt die belegte Bannerfarbe gruen",
          midgard["farbe"] == "gruen", str(midgard["farbe"]))
    valhalla = next(z for z in zeilen if z["name"] == "Valhalla")
    check("Valhalla ist eine fremde, aber erreichbare Welt",
          valhalla["status"] == "fremd" and valhalla["farbe"] == "rot" and valhalla["waehlbar"],
          str(valhalla))
    # ENTSCHEIDUNG GEAENDERT (Daniel 04.11.2026, 21:0x): es gibt keine gesperrte Weltkarte mehr.
    # Vorher zaehlte diese Wache vier offene Welten mit dem Grund "folgt spaeter".
    offene = [z for z in zeilen if not z["spielbar"]]
    check("keine Weltkarte ist mehr gesperrt", offene == [],
          str([(z["name"], z["status"]) for z in offene]))
    check("kein Grund nennt mehr ein spaeteres Dazukommen",
          all("spaeter" not in z["grund"] for z in zeilen), str([z["grund"] for z in zeilen]))
    check("keine Zeile der Liste nennt das alte Wort",
          all("Dimension" not in z["name"] + z["status_text"] + z["grund"] for z in zeilen),
          "")
    check("ohne belegten Weltnamen entsteht keine Zeile (kein erfundener Name)",
          all("Dimension " not in z["name"] for z in zeilen), str([z["name"] for z in zeilen]))


def _pruefungen_sperre():
    abschnitt("2. Ein laufender Auftrag sperrt jeden Weltensprung (Daniel, Anhang 2)")
    zeilen = portalraum.weltkarten([4], 2)
    check("bei zwei laufenden Auftraegen ist keine Weltkarte waehlbar",
          all(not z["waehlbar"] for z in zeilen), str([(z["name"], z["waehlbar"]) for z in zeilen]))
    gesperrt = [z for z in zeilen if z["spielbar"]]
    check("die Sperre nennt die laufenden Auftraege als Grund",
          all("unterwegs" in z["grund"] and "2" in z["grund"] for z in gesperrt),
          str([z["grund"] for z in gesperrt]))
    check("die Sperre faerbt die Zeile nicht um: eigene Welt bleibt gruen",
          next(z for z in zeilen if z["name"] == "Midgard")["farbe"] == "gruen", "")
    check("ohne laufenden Auftrag sind alle sechs Welten wieder waehlbar",
          all(z["waehlbar"] for z in portalraum.weltkarten([4], 0) if z["spielbar"]), "")

    abschnitt("3. Die Sperre sitzt auch im Wechsel selbst, nicht nur in der Anzeige")
    liste = [_laufender_auftrag()]
    check("auftraege.laufende zaehlt den laufenden Auftrag",
          len(auftraege.laufende(liste, 0.0)) == 1, str(auftraege.laufende(liste, 0.0)))
    check("ein abgeschlossener Auftrag zaehlt nicht mehr",
          len(auftraege.laufende(liste, 10000.0)) == 0, "")
    # S-4b (09.11.2026): die Sperre sitzt jetzt in `_dorf_versetzen` (der EINEN Buchstelle) -
    # `_portal_wechsel` ist entfernt. Die Zusage bleibt dieselbe: der Umzug fragt die Zahl der
    # laufenden Auftraege ab, bevor er etwas bucht.
    check("_dorf_versetzen fragt die Zahl der laufenden Auftraege ab",
          "_unterwegs_anzahl" in _code(main.NebelseetalApp._dorf_versetzen),
          "Aufruf fehlt")
    check("_unterwegs_anzahl liest auftraege.laufende mit der SPIELUHR",
          "auftraege.laufende" in _code(main.NebelseetalApp._unterwegs_anzahl)
          and "spielsekunden" in _code(main.NebelseetalApp._unterwegs_anzahl),
          _code(main.NebelseetalApp._unterwegs_anzahl)[:80])


def _pruefungen_zaehlweise():
    # W-6 (Daniel 04.11.2026): sechs Weltkarten, also Nummer 1..6 gegen Index 0..5.
    abschnitt("4. Zwei Zaehlweisen, EINE Umrechnung (Nummer 1..6 gegen Index 0..5)")
    check("Nummer 4 ist Index 3", portalraum.index_von(4) == 3, str(portalraum.index_von(4)))
    check("Index 3 ist Nummer 4", portalraum.nummer_von_index(3) == 4, "")
    check("Nummer 4 hat die Kennung d04", portalraum.kennung_von(4) == "d04", "")
    check("die Kennung d04 ergibt Nummer 4", portalraum.nummer_von("d04") == 4, "")
    # Grenze n: die letzte Weltkarte ist Nummer 6 = Index 5 (vor W-6 war es 20 = 19).
    check("Nummer 6 ist Index 5 (erreichbar)", portalraum.index_von(6) == 5, "")
    # Grenze n+1 und 0: beides ist keine Weltkarte (vor W-6: 21).
    check("Nummer 7 und 0 sind unbekannt", portalraum.index_von(7) == -1
          and portalraum.index_von(0) == -1, "")
    check("Index 5 ist mit dem Wechselritual erreichbar (die alte Luecke bei Knopf 20)",
          portalraum.wechsel_erlaubt(5, 1, 100000.0, None, 0.0)[0] is True, "")
    check("Index 6 bleibt ungueltig - genau das war der alte Fehler in klein",
          portalraum.wechsel_erlaubt(6, 1, 100000.0, None, 0.0)[0] is False, "")
    # S-4b: die Umrechnung steht in der Buchstelle `_dorf_versetzen` (Nummer 1..6 -> Index 0..5).
    check("_dorf_versetzen rechnet die Nummer ueber portalraum.index_von um",
          "index_von" in _code(main.NebelseetalApp._dorf_versetzen), "")
    check("_render_portal rechnet die Nummer ueber portalraum.index_von um",
          "index_von" in _code(main.NebelseetalApp._render_portal), "")


def _pruefungen_startwelt():
    abschnitt("5. Die Startwelt ist Midgard (Daniel, Anhang 3 Frage 22)")
    zustand = main.GameState()
    check("data/welten.json nennt Midgard als Startwelt", welt.startwelt() == "d04",
          welt.startwelt())
    check("die Startwelt hat die Nummer 4", welt.startwelt_nummer() == 4,
          str(welt.startwelt_nummer()))
    check("ein neues Spiel startet in Midgard", zustand.eigene_dimension == 4,
          str(zustand.eigene_dimension))
    check("Midgard ist zu Beginn die einzige eigene Weltkarte",
          list(zustand.eigene_dimensionen) == [4], str(zustand.eigene_dimensionen))
    check("die Nummer 4 wird als Midgard angezeigt",
          main.NebelseetalApp._dimensionsname(None, 4) == "Midgard",
          main.NebelseetalApp._dimensionsname(None, 4))
    # ENTSCHEIDUNG GEAENDERT (04.11.2026): jede der sechs belegten Welten ist bespielbar.
    check("Armageddon und Valhalla sind beide bespielbar",
          welt.spielbar("Armageddon") is True and welt.spielbar("Valhalla") is True, "")


def _pruefungen_ansicht():
    abschnitt("6. Die Ansicht: Liste oben, Gelaendekaestchen darunter, Feld anwaehlbar")
    quelle = _code(main.NebelseetalApp._render_portal)
    check("die Ansicht baut die Weltkartenliste aus portalraum.weltkarten",
          "weltkarten" in quelle, "")
    check("die Ansicht baut das Gelaendekaestchen aus portalraum.anzeige_raster",
          "anzeige_raster" in quelle, "")
    check("die Liste steht im Quelltext VOR dem K\u00e4stchen (Daniel: Liste oben)",
          quelle.find("weltkarten") < quelle.find("anzeige_raster"),
          str((quelle.find("weltkarten"), quelle.find("anzeige_raster"))))
    # UMGESTELLT 02.11.2026 (Stufe B-5): der Klick laeuft jetzt ueber EINE Weiterleitung, weil auf
    # dem K\u00e4stchen fremde Doerfer liegen (Klick aufs Dorf -> Optionen, sonst Feld anwaehlen). Die
    # Zusage bleibt: ein Klick landet bei genau einer Stelle, und das Anwaehlen selbst bucht nichts.
    check("ein Klick ruft die Weiterleitung _portal_klick", "_portal_klick" in quelle, "")
    check("die Weiterleitung waehlt sonst das Feld an",
          "_portal_feld_waehlen" in _code(main.NebelseetalApp._portal_klick), "")
    check("die Ansicht sagt Weltkarte und K\u00e4stchen",
          "Weltkarte" in quelle and "K\u00e4stchen" in quelle, "")
    for name in ("_render_portal", "_dorf_versetzen", "_portal_feld_waehlen", "_unterwegs_anzahl"):
        text = _code(getattr(main.NebelseetalApp, name))
        check(f"{name} nennt den alten Begriff nicht", "Dimension" not in text,
              [z for z in text.splitlines() if "Dimension" in z][:1])
    felder = portalraum.anzeige_raster(portalraum.index_von(4), 10, [4])
    check("das K\u00e4stchen hat 20 x 20 = 400 Felder", len(felder) == 400, str(len(felder)))
    check("alle Felder des K\u00e4stchens gehoeren zur aktuellen Weltkarte",
          all(f["z"] == 3 for f in felder), str(sorted({f["z"] for f in felder})))

    sql = portalraum.koordinate(3, 7, portalraum.index_von(4))
    check("Feld 3/7 liegt auf der Weltkarte", sql is not None and sql["welt"] == "Midgard",
          str(sql))
    check("Feld 20/5 liegt nicht auf einer 20x20-Weltkarte",
          portalraum.koordinate(20, 5, portalraum.index_von(4)) is None, "")


def _pruefungen_fenster():
    abschnitt("7. Ohne Fenster: anwaehlen, sperren, nichts buchen")
    try:
        import tkinter as tk
    except Exception as e:  # pragma: no cover - tkinter fehlt
        check("tkinter vorhanden", False, repr(e))
        return
    root = tk.Tk()
    root.withdraw()
    try:
        app = main.NebelseetalApp(root)
        app._build_main_ui()
        root.update()
        app._switch_view("Portal")
        root.update_idletasks()
        check("die Portalansicht rendert ohne Ausnahme", app.current_view == "Portal",
              str(app.current_view))
        check("die Ansicht startet ohne Anwahl", getattr(app, "portal_auswahl", None) is None,
              str(getattr(app, "portal_auswahl", None)))

        vorher_mana = float(app.state.resources["mana"].amount)
        check("ein Klick auf Feld 3/7 waehlt es an", app._portal_feld_waehlen(3, 7) is True, "")
        check("die Anwahl steht im Zustand der Ansicht", app.portal_auswahl == (3, 7),
              str(getattr(app, "portal_auswahl", None)))
        check("die Anwahl kostet kein Mana",
              float(app.state.resources["mana"].amount) == vorher_mana, "")
        check("die Anwahl uebertraegt kein Dorf (S-6 fehlt noch)",
              len(app.state.settlements) == 0, str(len(app.state.settlements)))
        check("ein Feld ausserhalb der Weltkarte wird abgelehnt",
              app._portal_feld_waehlen(20, 5) is False, "")
        check("die abgelehnte Anwahl laesst die alte stehen", app.portal_auswahl == (3, 7),
              str(app.portal_auswahl))

        app.state.auftraege.append(_laufender_auftrag(start=0.0, reisezeit=10000.0))
        app.state.spielsekunden = 0.0
        check("mit einem laufenden Auftrag meldet die Ansicht die Sperre",
              app._unterwegs_anzahl() == 1, str(app._unterwegs_anzahl()))
        # S-4b (09.11.2026): `_portal_wechsel` ist entfernt - die Sperre wird an der EINEN
        # Buchstelle `_dorf_versetzen` gemessen (S-3/S-4). Dafuer bekommt der Zustand kurz ein
        # Dorf; der Auftrag oben ist der Grund, aus dem der Umzug abgelehnt werden MUSS.
        dorf = main.Settlement(name="Eschenhain", map_id="kontinent", x=3, y=3,
                               id=main.siedlung_kennung("spieler", "kontinent", 3, 3),
                               dimension=int(app.state.eigene_dimension))
        app.state.settlements.append(dorf)
        gesperrt = app._dorf_versetzen("Eschenhain", 0, 0, 5)
        check("der Umzug wird abgelehnt", gesperrt is False, str(gesperrt))
        check("die Ablehnung nennt den Grund in der letzten Meldung",
              any("gesperrt" in str(n.get("text", "")) for n in app.state.messages[-2:]),
              str([str(n.get("text"))[:60] for n in app.state.messages[-2:]]))
        check("die Sperre kostet kein Mana und wechselt nicht",
              float(app.state.resources["mana"].amount) == vorher_mana
              and int(app.state.eigene_dimension) == 4,
              str((app.state.resources["mana"].amount, app.state.eigene_dimension)))
        check("die alte Buchstelle _portal_wechsel gibt es nicht mehr",
              not hasattr(main.NebelseetalApp, "_portal_wechsel"), "Methode existiert wieder")
        app.state.settlements.remove(dorf)
        app.state.auftraege.clear()
    finally:
        try:
            root.destroy()
        except Exception:
            pass


def main_() -> int:
    _pruefungen_liste()
    _pruefungen_sperre()
    _pruefungen_zaehlweise()
    _pruefungen_startwelt()
    _pruefungen_ansicht()
    _pruefungen_fenster()
    return bericht()


if __name__ == "__main__":
    sys.exit(main_())
