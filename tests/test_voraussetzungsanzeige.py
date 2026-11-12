# -*- coding: ascii -*-
"""Wache A1: Voraussetzungen stehen im Spiel - ALLE, nicht nur die erste (05.11.2026).

Daniels Auftrag (Uebergabe 05.11.2026, Abschnitt 4): "Voraussetzungen im Spiel sichtbar machen"
- der einzige Punkt, den alle vier Spieltest-Urteile unabhaengig nennen. Gemessen war damals:

  * die Kaserne nannte je gesperrter Einheit nur die ERSTE offene Bedingung (die Forschung).
    Die Ausruestung blieb unsichtbar, bis die Forschung lief - bei einem Kaempfer kam die zweite
    Sperre also erst NACH der ersten Forschung ans Licht (L3/L4: 283+156+82 Fehlversuche an
    Kurzschwertern, 488 blockierte Ausbildungen).
  * der gesperrte Knopf in der Werkstatt war nur grau; sein Grund stand erst im Sammelblock.

Was diese Datei prueft:
  1. `spieloekonomie.einheit_bedingungen` liefert JEDE Bedingung einzeln (Forschung, Staette,
     Ausruestung, Siedler) mit Text, Urteil und naechstem Schritt.
  2. Der naechste Schritt nennt Kosten und Dauer aus DENSELBEN Funktionen wie der Kern
     (`forschung.kosten`, `forschung.dauer_stunden`) - keine zweite Zahlenquelle.
  3. Ist alles erfuellt, bleibt keine offene Bedingung uebrig.
  4. `ware_bedingungen` nennt Forschung UND Werkstatt einer Ware.
  5. Quelltext-Wachen: das Hindernis sammelt ALLE offenen Bedingungen, es gibt keinen zweiten
     Rechenweg mehr (`ausruestung.fehlende` im Hindernis ist weg).
  6. Die ANSICHT zeigt die Schritte (Kaserne) und den Grund am Knopf (Werkstatt).
  7. GEGENPROBE: ohne Bedingungen ist der Knopf frei und kein "fehlt:" zu lesen - sonst wuerde
     die Wache nur ihren eigenen Text pruefen.

Aufruf: python -X utf8 tests/test_voraussetzungsanzeige.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster"
PRUEF_STUFE = 3
PRUEF_BETRIFFT = ['ausruestung', 'einheiten', 'forschung', 'gelaende', 'main:*', 'spieloekonomie', 'werkstatt']
PRUEF_DATEN = ['units.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import ast
import inspect
import os
import sys
import textwrap
import tkinter as tk
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
os.chdir(SRC)

import ausruestung  # noqa: E402
import einheiten  # noqa: E402
import forschung  # noqa: E402
import gelaende  # noqa: E402
import main  # noqa: E402
import spieloekonomie as O  # noqa: E402


def _code(funktion) -> str:
    """Quelltext einer Methode OHNE Docstring (Docstrings zaehlen nicht als Code)."""
    baum = ast.parse(textwrap.dedent(inspect.getsource(funktion)))
    rumpf = baum.body[0].body
    if rumpf and isinstance(rumpf[0], ast.Expr) and isinstance(rumpf[0].value, ast.Constant):
        rumpf = rumpf[1:]
    return "\n".join(ast.unparse(knoten) for knoten in rumpf)


def _einheit_mit_zwei_waren():
    """Die Kennung der Einheit, die zwei Ausruestungswaren braucht (Kaempfer) - aus den Daten."""
    for key in einheiten.alle():
        # data/units.json nennt das Gebaeude im ANZEIGENAMEN ("Kriegerakademie"), nicht als
        # Kennung - deshalb der Vergleich in Kleinschreibung.
        if str((einheiten.alle()[key] or {}).get("gebaeude") or "").lower() == "kriegerakademie":
            if len(ausruestung.bedarf(key)) >= 2 and "Kurzschwert" in ausruestung.bedarf(key):
                return key
    return None


def _app_mit_ort():
    """Die echte App ohne Fenster, erste Siedlung gegruendet, Baukunst 1 und Waffentechnik 2."""
    root = tk.Tk()
    root.withdraw()
    app = main.NebelseetalApp(root)
    app._build_main_ui()
    root.update()
    app._erste_siedlung_gruenden()
    gs = app.state
    for name, stufe in (("Baukunst", 1), ("Waffentechnik", 2)):
        if name in gs.research:
            gs.research[name].level = stufe
    return root, app, gs, gs.aktive_siedlung()


def _bauen(app, ort, gebaeude):
    """Ein Gebaeude auf das erste Feld stellen, das die Standortregel zulaesst."""
    for feld, terrain in enumerate(ort.karte["raster"]):
        if str(feld) in ort.bauten:
            continue
        erlaubt, _grund = gelaende.bau_moeglich(gebaeude, terrain)
        if not erlaubt:
            continue
        app._oeffne_siedlungskarte(ort)
        app._karten_feld_waehlen(feld)
        vorher = len(ort.bauten)
        app._karten_bauen(gebaeude)
        if len(ort.bauten) > vorher:
            return feld
    return None


def _texte(app) -> list:
    """Alle Anzeigetexte der aktuellen Ansicht (Label und Button) in Baumreihenfolge."""
    gesammelt = []

    def lauf(w):
        try:
            text = w.cget("text")
        except Exception:
            text = None
        if text and w.winfo_class() in ("Label", "Button"):
            gesammelt.append(str(text))
        for kind in w.winfo_children():
            lauf(kind)

    lauf(app.content)
    return gesammelt


def _lauf():
    kaempfer = _einheit_mit_zwei_waren()
    root, app, gs, ort = _app_mit_ort()
    for gebaeude in ("bibliothek", "kriegerakademie", "schmiede"):
        _bauen(app, ort, gebaeude)
    stufen = gs.forschungs_stufen()
    try:
        # ---------------------------------------------------------------- 1. Alle Bedingungen
        abschnitt("1. Alle Bedingungen einer Einheit stehen einzeln da")
        check("die Pruefeinheit ist gefunden (Kaempfer: Akademie, zwei Waren)",
              kaempfer is not None, str(kaempfer))
        bedingungen = O.einheit_bedingungen(ort, kaempfer, stufen)
        check("einheit_bedingungen liefert eine Liste mit Eintraegen", bool(bedingungen),
              str(bedingungen))
        check("jeder Eintrag hat art, text, erfuellt und schritt",
              all({"art", "text", "erfuellt", "schritt"} <= set(b) for b in bedingungen),
              str(bedingungen[:1]))
        arten = {b["art"] for b in bedingungen}
        check("Forschung UND Ausruestung kommen vor (vorher war nur die Forschung zu sehen)",
              "forschung" in arten and "ausruestung" in arten, str(sorted(arten)))
        offen = [b for b in bedingungen if not b["erfuellt"]]
        check("in der Lage Waffentechnik 2 sind mindestens drei Bedingungen offen "
              "(Forschung, beide Waren)", len(offen) >= 3, str([b["text"] for b in offen]))
        check("die zweite Ware steht EINZELN da (nicht in der ersten versteckt)",
              len([b for b in offen if b["art"] == "ausruestung"]) >= 2,
              str([b["text"] for b in offen if b["art"] == "ausruestung"]))
        check("jede offene Bedingung nennt einen naechsten Schritt",
              all(b["schritt"] for b in offen), str([(b["text"], b["schritt"]) for b in offen]))
        ware_fehlt = [b for b in offen if b["art"] == "ausruestung"][0]
        check("der Schritt zur Ware nennt die Werkstatt und den Grund der Ware",
              "Werkstatt" in ware_fehlt["schritt"] and "fehlt" in ware_fehlt["schritt"],
              ware_fehlt["schritt"])

        # ------------------------------------------------------- 2. Kosten und Dauer aus den Daten
        abschnitt("2. Der naechste Forschungsschritt nennt Kosten und Dauer aus den Daten")
        schritt = O.forschung_schritt("Kriegskunst", 2, ort)
        kosten = forschung.kosten(2)
        holz = int(kosten.get("holz", 0))
        check("die Kosten stehen im Schritt (Holz aus forschung.kosten)",
              f"{holz:g} Holz" in schritt or f"{holz} Holz" in schritt, schritt)
        stunden = forschung.dauer_stunden(2)
        check("die Dauer steht im Schritt (Stufe zum Quadrat, aus forschung.dauer_stunden)",
              f"{stunden:g} Spielstunde" in schritt, schritt)
        check("ohne Bibliothek im Ort sagt der Schritt das ehrlich",
              "Bibliothek" in O.forschung_schritt("Kriegskunst", 1, {}), "")

        # ------------------------------------------------------------- 3. Erfuellte Lage
        abschnitt("3. Ist alles erfuellt, bleibt keine offene Bedingung")
        for ware in ausruestung.bedarf(kaempfer):
            ort.waren[ware] = 5
        for name in ("Kriegskunst",):
            if name in gs.research:
                gs.research[name].level = 1
        stufen2 = gs.forschungs_stufen()
        offen2 = [b for b in O.einheit_bedingungen(ort, kaempfer, stufen2) if not b["erfuellt"]]
        check("mit Forschung und Ausruestung ist nichts mehr offen", not offen2,
              str([b["text"] for b in offen2]))

        # ------------------------------------------------------------------- 4. Waren
        abschnitt("4. ware_bedingungen nennt Forschung und Werkstatt")
        ware = "Kurzschwert"
        gs.research["Waffentechnik"].level = 2
        stufen3 = gs.forschungs_stufen()
        wb = O.ware_bedingungen(ort, ware, stufen3)
        check("die Forschungsbedingung der Ware steht da",
              any(b["art"] == "forschung" and not b["erfuellt"] for b in wb), str(wb))
        schmiede_da = [b for b in wb if b["art"] == "werkstatt"]
        check("bei gebauter Schmiede fehlt keine Werkstatt", not schmiede_da,
              str([b["text"] for b in schmiede_da]))

        # ------------------------------------------------------------ 5. Quelltext-Wachen
        abschnitt("5. Quelltext-Wachen: eine Lesestelle, kein zweiter Rechenweg")
        hindernis = _code(main.NebelseetalApp._ausbildungs_hindernis)
        check("das Hindernis sammelt ueber _ausbildungs_bedingungen",
              "_ausbildungs_bedingungen(" in hindernis, hindernis[:160])
        check("es nennt ALLE offenen Bedingungen (join ueber die offene Liste)",
              "join(" in hindernis and "if not b['erfuellt']" in hindernis.replace('"', "'"),
              hindernis[:200])
        check("der alte zweite Rechenweg (ausruestung.fehlende im Hindernis) ist weg",
              "ausruestung.fehlende(" not in hindernis, hindernis[:200])
        check("die Bedingungen selbst kommen aus spieloekonomie",
              "spieloekonomie.einheit_bedingungen(" in _code(
                  main.NebelseetalApp._ausbildungs_bedingungen), "")
        liste_code = _code(O.einheit_bedingungen)
        check("die Lesestelle liest die Daten, nicht die Oberflaeche",
              "U.get(" in liste_code and "ausruestung.bedarf(" in liste_code, liste_code[:160])

        # --------------------------------------------------------------- 6. Die Ansicht
        abschnitt("6. Die Ansicht zeigt die Schritte und den Grund am Knopf")
        gs.research["Waffentechnik"].level = 2
        for ware in ausruestung.bedarf(kaempfer):
            ort.waren.pop(ware, None)
        if "Kriegskunst" in gs.research:
            gs.research["Kriegskunst"].level = 0
        app._switch_view("Kaserne")
        root.update()
        texte = _texte(app)
        check("die Kaserne zeigt eine Zeile je offener Bedingung mit Schritt",
              any("Bibliothek" in t and "Holz" in t for t in texte),
              str([t for t in texte if "Bibliothek" in t][:2]))
        check("der gesperrte Knopf nennt den Grund im Text",
              any(t.startswith("fehlt:") for t in texte),
              str([t for t in texte if t.startswith("fehlt:")][:1]))
        app._switch_view("Lager")
        root.update()
        texte_lager = _texte(app)
        check("der Werkstatt-Knopf traegt seinen Grund (Ware: Bedingung)",
              any(t.startswith(ware + ":") for t in texte_lager for ware in ("Kurzschwert",)),
              str([t for t in texte_lager if "Kurzschwert" in t][:2]))

        # ------------------------------------------------------------- 7. Gegenprobe
        abschnitt("7. Gegenprobe: ohne Bedingungen ist der Knopf frei")
        with mock.patch.object(main.NebelseetalApp, "_ausbildungs_bedingungen",
                               lambda self, key: []):
            frei, grund = app._ausbildungs_hindernis(kaempfer)
        check("ohne Bedingungen meldet das Hindernis frei", frei is True and not grund,
              f"{frei} / {grund}")
        mit = app._ausbildungs_hindernis(kaempfer)
        check("mit Bedingungen meldet es gesperrt und nennt sie", mit[0] is False and
              "fehlt:" in mit[1], str(mit))
    finally:
        root.destroy()
    return bericht()


sys.exit(_lauf())
