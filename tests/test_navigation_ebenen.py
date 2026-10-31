"""Pruefdatei: beide Navigationsebenen rendern JEDEN Punkt ihrer Leiste ohne Fehler.

Deckt die Punkte ab, die in MENU_ITEMS (der belegten Original-Liste) nicht stehen und deshalb von
tests/test_gui_fehler.py nicht besucht werden: Voraussetzungen, Neuigkeiten, Stellmacher,
Diebesgilde. Ausserdem: der Ebenenwechsel laesst immer eine sichtbare Ansicht stehen.

Aufruf: python -X utf8 tests/test_navigation_ebenen.py
"""
import os
import sys
import tempfile
import tkinter as tk

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(WURZEL, "src"))

import main  # noqa: E402

bestanden = []
fehler = []


def check(name, bedingung, detail=""):
    if bedingung:
        bestanden.append(name)
    else:
        fehler.append(f"{name} — {detail}")


def siedlung_mit(gebaeude=()):
    """Echte Settlement + echte Karte aus dem Projekt — kein Stub.

    Ein eigener Stub ist hier verboten: die Ansichten lesen `s.name`, `s.karte['typ_name']`,
    `s.karte['raster']` und mehr. Mit einem Stub faellt der Test mit AttributeError/KeyError um
    (am 31.10. zweimal selbst erlebt) und prueft dann gar nichts. Die Karte kommt deshalb aus
    `spieloekonomie.startkarte()` — derselbe Weg wie im Spiel.
    """
    import spieloekonomie
    ort = main.Settlement(name="Testdorf", map_id="kontinent", x=5, y=5,
                          id="test:kontinent:5:5")
    karte = spieloekonomie.startkarte("pruefseed-navigation", "spieler")
    if isinstance(karte, dict) and "karte" in karte and isinstance(karte["karte"], dict):
        karte = karte["karte"]
    ort.karte = dict(karte)
    raster = ort.karte.get("raster") or []
    for i, gebaeude_key in enumerate(gebaeude):
        if i >= len(raster):
            break
        ort.bauten[str(i)] = gebaeude_key
        ort.stufen[str(i)] = 1
    return ort


print("=" * 70)
print("1. Beide Ebenen: jeder Menuepunkt rendert")
print("=" * 70)
tor = os.path.join(tempfile.gettempdir(), "nebel_nav_pruef_tor.json")
root = tk.Tk()
root.withdraw()
try:
    app = main.NebelseetalApp(root, tor_pfad=tor)
    # Eine Siedlung MIT den drei Gebaeuden, damit alle bedingten Punkte erscheinen.
    app.state.settlements.append(siedlung_mit(["bibliothek", "kriegerakademie", "stellmacher",
                                               "diebesgilde", "lager", "haus"]))
    app._build_main_ui()
    root.update()

    for ebene in main.EBENEN:
        app._ebene_wechseln(ebene)
        root.update()
        punkte = list(app.menu_buttons)
        check(f"Ebene {ebene}: Leiste ist gefuellt", bool(punkte), str(punkte))
        for punkt in punkte:
            try:
                app._switch_view(punkt)
                root.update()
                gezeichnet = len(app.content.winfo_children()) > 0
            except Exception as ausnahme:  # noqa: BLE001 - genau das soll auffallen
                check(f"Ebene {ebene} / {punkt}: rendert ohne Fehler", False, repr(ausnahme))
                continue
            check(f"Ebene {ebene} / {punkt}: rendert ohne Fehler und mit Inhalt", gezeichnet,
                  f"{len(app.content.winfo_children())} Bereiche")

    print()
    print("=" * 70)
    print("2. Die bedingten Punkte sind wirklich erreichbar")
    print("=" * 70)
    for ebene, punkt in (("Uebersicht", "Voraussetzungen"), ("Uebersicht", "Neuigkeiten"),
                         ("Siedlung", "Stellmacher"), ("Siedlung", "Diebesgilde"),
                         ("Siedlung", "Kaserne"), ("Siedlung", "Forschung")):
        app._ebene_wechseln(ebene)
        root.update()
        check(f"{punkt} steht in Ebene {ebene}", punkt in app.menu_buttons,
              str(sorted(app.menu_buttons)))

    print()
    print("=" * 70)
    print("3. Ebenenwechsel laesst nie eine leere Ansicht stehen")
    print("=" * 70)
    for ebene in ("Uebersicht", "Siedlung", "Uebersicht", "Siedlung"):
        app._ebene_wechseln(ebene)
        root.update()
        check(f"nach Wechsel auf {ebene} ist eine Ansicht aktiv",
              app.current_view in app.menu_buttons, f"{app.current_view} / {ebene}")
finally:
    try:
        root.destroy()
    except Exception:
        pass
    if os.path.exists(tor):
        os.remove(tor)

print()
print("=" * 70)
print(f"ERGEBNIS: {len(bestanden)} bestanden, {len(fehler)} Fehler, 0 Befunde")
print("=" * 70)
for f in fehler:
    print("  FEHLER:", f)
sys.exit(0 if not fehler else 1)
