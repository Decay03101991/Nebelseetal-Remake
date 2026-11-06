# -*- coding: ascii -*-
"""Menue-Teilgeschichten - S1b (06.11.2026).

Vier Ansichten haben je eine kurze Geschichte: Forschung (erste Bibliothek), Portal (erster
Weltwechsel), Kaserne (Kriegerakademie steht), Ruhmeshalle (erstes Oeffnen). Daniel hat den Ton in
`data/story.json` festgelegt (leicht, abenteuerlich, kein Pathos) und in Runde 3 Frage 1 entschieden:
die Portal-Geschichte ist reiner Text ohne Antwortknoepfe.

Was diese Datei beweist
-----------------------
1. Alle vier Geschichten stehen in `data/story.json`, mit Titel und hoechstens drei Saetzen.
2. KEIN Text steht im Code (Quellwache ueber `src/main.py` und `src/story.py`) - die Texte gehoeren
   in die Datendatei, sonst gibt es zwei Gedaechtnisse.
3. Jede Geschichte erscheint je Spielstand GENAU EINMAL: das Kennzeichen liegt im Spielstand
   (`menue_geschichten_gesehen`), der zweite Aufruf oeffnet nichts mehr.
4. Ein alter Spielstand ohne das Feld zeigt die Geschichte nach (`.get`-Fallback, keine Migration).
5. Das Kennzeichen ueberlebt Speichern und Laden.
6. Das Portal-Overlay hat KEINE Antwortknoepfe - genau ein Knopf, und der schliesst nur.
7. Ein fehlender Text wirft nicht: `menue_geschichte` liefert dann ein leeres Dict.

Aufruf:  python -X utf8 tests/test_story_menue.py
"""
from __future__ import annotations

import json
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(WURZEL, "src"))
sys.path.insert(0, os.path.join(WURZEL, "tests"))

from harness import abschnitt, bericht, check                      # noqa: E402
import story                                                       # noqa: E402

SCHLUESSEL = ("forschung", "portal", "kaserne", "ruhmeshalle")
ANSICHTEN = {"forschung": "Forschung", "portal": "Portal", "kaserne": "Kaserne",
             "ruhmeshalle": "Ruhmeshalle"}


def saetze(text):
    """Zaehlt die Saetze eines Textes (Punkt, Fragezeichen, Ausrufezeichen als Trenner)."""
    return [s for s in re.split(r"(?<=[.!?])\s+", str(text or "").strip()) if s]


def test_daten():
    """1. Vier Geschichten in der Datendatei, jede mit Titel und hoechstens drei Saetzen."""
    abschnitt("1. Vier Geschichten in data/story.json")
    with open(os.path.join(WURZEL, "data", "story.json"), encoding="utf-8") as f:
        daten = json.load(f)
    bereich = daten.get("menue_geschichten") or {}
    check("der Bereich steht in der Datei", bool(bereich), str(list(bereich.keys())))
    for schluessel in SCHLUESSEL:
        eintrag = bereich.get(schluessel) or {}
        check("Geschichte %s hat einen Titel" % schluessel, bool(str(eintrag.get("titel") or "").strip()),
              str(eintrag.get("titel")))
        text = str(eintrag.get("text") or "").strip()
        check("Geschichte %s hat einen Text" % schluessel, len(text) > 40, "%d Zeichen" % len(text))
        check("Geschichte %s hat hoechstens drei Saetze" % schluessel, len(saetze(text)) <= 3,
              "%d Saetze" % len(saetze(text)))
    check("die Datendatei nennt den Ton", "abenteuerlich" in str(daten.get("ton") or ""))


def test_kein_text_im_code():
    """2. Kein Spieltext im Code."""
    abschnitt("2. Kein Text im Code")
    with open(os.path.join(WURZEL, "src", "main.py"), encoding="utf-8") as f:
        main_text = f.read()
    with open(os.path.join(WURZEL, "src", "story.py"), encoding="utf-8") as f:
        story_text = f.read()
    for schluessel in SCHLUESSEL:
        anfang = story.menue_geschichte(schluessel)["text"][:30]
        check("Text %s steht nicht in main.py" % schluessel, anfang not in main_text)
        check("Text %s steht nicht in story.py" % schluessel, anfang not in story_text)


def test_lesestelle():
    """3. Die Lesestelle liefert Text, unbekannte Schluessel werfen nicht."""
    abschnitt("3. Lesestelle story.menue_geschichte")
    for schluessel in SCHLUESSEL:
        eintrag = story.menue_geschichte(schluessel)
        check("menue_geschichte(%s) liefert Titel und Text" % schluessel,
              bool(eintrag["titel"]) and bool(eintrag["text"]))
    leer = story.menue_geschichte("gibtesnicht")
    check("unbekannter Schluessel liefert leeres Dict", leer == {"titel": "", "text": ""}, str(leer))
    check("auch None wirft nicht", story.menue_geschichte(None) == {"titel": "", "text": ""})


def _app():
    """Baut eine Pruef-App ohne Fenster (Muster test_produktionskette_ohne_cheats)."""
    import tkinter as tk
    import main
    wurzel = tk.Tk()
    wurzel.withdraw()
    app = main.NebelseetalApp(wurzel)
    app._build_main_ui()
    return wurzel, app


def _overlay_abfangen(app):
    """Ersetzt `_overlay_oeffnen` durch einen Mitschnitt: Titel, Knopftexte des Inhalts."""
    gerufen = []

    def mitschnitt(titel, bauen):
        """Baut den Inhalt in einen echten Frame und merkt sich Titel und Knoepfe."""
        import tkinter as tk
        rahmen = tk.Frame(app.content, bg=app.skin["bg"])
        bauen(rahmen, lambda: None)
        knoepfe = []
        labels = []

        def sammeln(widget):
            """Sammelt Knopf- und Labeltexte des Inhalts."""
            for kind in widget.winfo_children():
                if kind.winfo_class() == "Button":
                    knoepfe.append(str(kind.cget("text")))
                if kind.winfo_class() == "Label":
                    labels.append(str(kind.cget("text")))
                sammeln(kind)

        sammeln(rahmen)
        gerufen.append({"titel": titel, "knoepfe": knoepfe, "labels": labels})
        rahmen.destroy()

    app._overlay_oeffnen = mitschnitt
    return gerufen


def test_einmal_je_spielstand():
    """4. Jede Geschichte erscheint genau einmal je Spielstand."""
    abschnitt("4. Genau einmal je Spielstand")
    wurzel, app = _app()
    try:
        gerufen = _overlay_abfangen(app)
        app.state.menue_geschichten_gesehen = {}
        app._switch_view(ANSICHTEN["forschung"])
        check("die Forschungs-Geschichte erscheint", len(gerufen) == 1, str([g["titel"] for g in gerufen]))
        check("das Kennzeichen steht im Spielstand",
              app.state.menue_geschichten_gesehen.get("forschung") is True,
              str(app.state.menue_geschichten_gesehen))
        app._switch_view("Dorfzentrum")
        app._switch_view(ANSICHTEN["forschung"])
        check("beim zweiten Oeffnen erscheint sie nicht mehr", len(gerufen) == 1,
              str([g["titel"] for g in gerufen]))
        for schluessel, ansicht in ANSICHTEN.items():
            app._switch_view(ansicht)
        check("alle vier Geschichten sind danach erzahlt",
              sorted(app.state.menue_geschichten_gesehen) == sorted(SCHLUESSEL),
              str(sorted(app.state.menue_geschichten_gesehen)))
        check("keine Geschichte kam doppelt", len(gerufen) == 4, str(len(gerufen)))
    finally:
        wurzel.destroy()


def test_alter_stand_zeigt_nach():
    """5. Alter Spielstand ohne Kennzeichen zeigt die Geschichte nach."""
    abschnitt("5. Alter Spielstand zeigt nach")
    wurzel, app = _app()
    try:
        gerufen = _overlay_abfangen(app)
        if hasattr(app.state, "menue_geschichten_gesehen"):
            del app.state.menue_geschichten_gesehen                  # wie ein Stand von vor S1b
        app._switch_view(ANSICHTEN["kaserne"])
        check("die Kaserne-Geschichte erscheint nach", len(gerufen) == 1)
        check("das Feld wird dabei angelegt", isinstance(app.state.menue_geschichten_gesehen, dict))
    finally:
        wurzel.destroy()


def test_portal_ohne_antwortknoepfe():
    """6. Portal-Geschichte: reiner Text, ein Knopf, der nur schliesst."""
    abschnitt("6. Portal ohne Antwortknoepfe")
    wurzel, app = _app()
    try:
        gerufen = _overlay_abfangen(app)
        app.state.menue_geschichten_gesehen = {}
        app._switch_view(ANSICHTEN["portal"])
        check("das Portal-Overlay erscheint", len(gerufen) == 1, str(gerufen))
        if gerufen:
            eintrag = gerufen[0]
            check("genau ein Knopf", len(eintrag["knoepfe"]) == 1, str(eintrag["knoepfe"]))
            check("der Knopf heisst Weiter", eintrag["knoepfe"] == ["Weiter"], str(eintrag["knoepfe"]))
            check("der Text steht im Overlay", any("Nebelstein" in t for t in eintrag["labels"]),
                  str(eintrag["labels"])[:120])
            check("der Titel steht im Overlay", "Portal" in eintrag["titel"], eintrag["titel"])
    finally:
        wurzel.destroy()


def test_speichern_und_laden():
    """7. Das Kennzeichen ueberlebt Speichern und Laden."""
    abschnitt("7. Kennzeichen ueberlebt Speichern und Laden")
    import tempfile
    wurzel, app = _app()
    try:
        app.state.menue_geschichten_gesehen = {"forschung": True, "portal": True}
        pfad = os.path.join(tempfile.gettempdir(), "pruef_s1b_spielstand.json")
        app.state.save(pfad)
        with open(pfad, encoding="utf-8") as f:
            gespeichert = json.load(f)
        check("der Spielstand enthaelt das Feld", "menue_geschichten_gesehen" in gespeichert,
              str(list(gespeichert.keys())[:6]))
        app.state.menue_geschichten_gesehen = {}
        app.state.load(pfad)
        check("nach dem Laden stehen beide Kennzeichen",
              app.state.menue_geschichten_gesehen == {"forschung": True, "portal": True},
              str(app.state.menue_geschichten_gesehen))
        os.remove(pfad)
    finally:
        wurzel.destroy()


def main_test():
    """Fuehrt alle Pruefungen aus und meldet das Ergebnis."""
    test_daten()
    test_kein_text_im_code()
    test_lesestelle()
    test_einmal_je_spielstand()
    test_alter_stand_zeigt_nach()
    test_portal_ohne_antwortknoepfe()
    test_speichern_und_laden()
    return bericht()


if __name__ == "__main__":
    sys.exit(main_test())
