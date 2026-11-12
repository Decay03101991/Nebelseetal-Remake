# -*- coding: ascii -*-
"""Schnitt S-2 (Teil a): Menuepunkt "Karten" entfaellt, die Anzeige sagt Weltkarte/Weltensprung.

Daniel 01.11.2026 (docs/KONZEPT_SECHS_DOERFER_20261101.md, Anhang 1 Abschnitt 2 und Anhang 3
Frage 19/25/35):
  * "Die Weltkarte soll weg es wird hier nur noch Platz sein fuer das Dorfzentrum Lager und dessen
    verwaltung und uebersichten" - der Menuepunkt "Karten" (alte Weltkarte "Orte entdecken" mit
    sieben Gebieten) faellt weg, das Portal uebernimmt seine Aufgabe.
  * "Das Wort Dimensionen soll aus dem Spiel verschwinden - es heisst Weltensprunge und
    Weltkarten." Die Umbenennung beginnt in der ANZEIGE (Frage 35); Code und Speicherformat
    folgen schrittweise, deshalb bleiben Schluessel wie `dimension` im Spielstand unangetastet.

Diese Pruefdatei wacht ueber beides. Aufruf: python -X utf8 tests/test_weltkarten_anzeige.py
"""

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['berater', 'main:*', 'portalraum', 'welt']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------
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
import berater  # noqa: E402

WELTNAMEN = ("Armageddon", "Ragnar", "Utgard", "Midgard", "Valhalla", "Limbus")


def _code(funktion) -> str:
    """Quelltext einer Funktion OHNE Docstring (ein Docstring darf den alten Begriff erklaeren)."""
    baum = ast.parse(textwrap.dedent(inspect.getsource(inspect.unwrap(funktion))))
    rumpf = baum.body[0].body
    if (rumpf and isinstance(rumpf[0], ast.Expr) and isinstance(rumpf[0].value, ast.Constant)
            and isinstance(rumpf[0].value.value, str)):
        rumpf = rumpf[1:]
    baum.body[0].body = rumpf or [ast.Pass()]
    return ast.unparse(baum)


def _pruefungen_menue():
    abschnitt("1. Der Menuepunkt Karten ist fort, die Liste hat 16 Eintraege")
    check("MENU_ITEMS enthaelt kein Karten mehr", "Karten" not in main.MENU_ITEMS,
          str(main.MENU_ITEMS))
    check("die Liste hat 16 Eintraege", len(main.MENU_ITEMS) == 16, str(len(main.MENU_ITEMS)))
    check("Dorfzentrum bleibt der Ort fuer Verwaltung und Uebersichten",
          "Dorfzentrum" in main.MENU_ITEMS, str(main.MENU_ITEMS[:3]))
    check("EBENE_JE_PUNKT kennt kein Karten mehr", "Karten" not in main.EBENE_JE_PUNKT,
          str(sorted(set(main.EBENE_JE_PUNKT))[:6]))
    check("jeder Menuepunkt hat weiterhin eine Ebene",
          all(item in main.EBENE_JE_PUNKT for item in main.MENU_ITEMS),
          str([i for i in main.MENU_ITEMS if i not in main.EBENE_JE_PUNKT]))


def _pruefungen_ansicht():
    abschnitt("2. Die alte Weltkarte ist stillgelegt, nicht heimlich verdrahtet")
    quelltext = inspect.getsource(main)
    check("keine Ansicht Karten mehr verdrahtet", '"Karten": self.' not in quelltext,
          "Verdrahtung im Ansichts-Verzeichnis")
    check("die alte Ansicht existiert noch als Beleg", hasattr(main.NebelseetalApp, "_render_maps"),
          "Methode _render_maps")
    doc = (main.NebelseetalApp._render_maps.__doc__ or "")
    check("ihr Docstring sagt STILLGELEGT und nennt die Entscheidung",
          "STILLGELEGT" in doc and "S-2" in doc, doc[:80])
    check("der alte Titel der Ansicht steht weiter im Belegtext",
          "Weltkarte" in _code(main.NebelseetalApp._render_maps),
          "Titel der stillgelegten Ansicht")


def _pruefungen_anzeige():
    abschnitt("3. Die Anzeige sagt Weltkarte und Weltensprung, nicht Dimension")
    # S-4b (09.11.2026): `_portal_wechsel` ist entfernt - die Liste fuehrt nur noch die beiden
    # Methoden, die es gibt. Dass die alte Buchstelle nicht zurueckkommt, prueft die naechste Wache.
    for name in ("_dimensionsname", "_render_portal"):
        funktion = getattr(main.NebelseetalApp, name)
        text = _code(funktion)
        check(f"{name} nennt den alten Begriff nicht mehr", "Dimension" not in text,
              [z for z in text.splitlines() if "Dimension" in z][:2])
    check("_render_portal nennt die Weltkarte", "Weltkarte" in _code(
        main.NebelseetalApp._render_portal), "Portalansicht")
    check("die alte Buchstelle _portal_wechsel ist entfernt (S-4b)",
          not hasattr(main.NebelseetalApp, "_portal_wechsel"), "")
    check("der Weltensprung heisst weiter so (in der Beschreibung des Portals)",
          "Weltensprung" in portalraum.beschreibung(), "")

    text_portal = portalraum.beschreibung()
    check("portalraum.beschreibung nennt Weltkarten", "Weltkarten" in text_portal, text_portal)
    check("portalraum.beschreibung nennt den Weltensprung", "Weltensprung" in text_portal,
          text_portal)
    check("portalraum.beschreibung nennt den alten Begriff nicht", "Dimension" not in text_portal,
          text_portal)

    zeilen = berater._antwort_portal()
    verboten = [z for z in zeilen if "Dimension" in z]
    check("der Berater sagt nicht mehr Dimension", not verboten, str(verboten))
    check("der Berater nennt die Weltkarten", any("Weltkarten" in z for z in zeilen),
          str(zeilen[:2]))

    erlaubt, meldung = portalraum.wechsel_erlaubt(99, 1, 100000.0)
    check("die Ablehnung nennt eine unbekannte Ausgangswelt, keine Dimension",
          erlaubt is False and "Dimension" not in meldung and "welt" in meldung.lower(), meldung)


def _pruefungen_daten():
    abschnitt("4. Die sechs Weltnamen stehen im Datenbestand (Grundlage fuer die Portalliste)")
    namen = [str(e.get("name") or "") for e in portalraum.dimensionen()]
    for welt in WELTNAMEN:
        check(f"Weltname {welt} kommt in den Portal-Daten vor",
              any(welt in name for name in namen), str(namen[:6]))
    # W-6 (Daniel 04.11.2026): sechs Weltkarten statt 20 Dimensionen - hier stand vorher 20.
    check("die Portal-Daten fuehren 6 Eintraege (W-6)", len(namen) == 6, str(len(namen)))


def main_() -> int:
    _pruefungen_menue()
    _pruefungen_ansicht()
    _pruefungen_anzeige()
    _pruefungen_daten()
    return bericht()


if __name__ == "__main__":
    sys.exit(main_())
