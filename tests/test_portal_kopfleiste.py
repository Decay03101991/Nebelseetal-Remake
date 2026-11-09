# -*- coding: ascii -*-
"""Wache: das Kopfband ueber dem Portal-Titel (D-5, 09.11.2026).

DANIELS ENTSCHEIDUNG (Register 347, 09.11.2026)
----------------------------------------------
"Band `band_schmiede_dorf_ghule`, 780 x 150 px, 0 % Beschnitt" fuer Platz S1, die Weltkartenliste
bleibt bei der "farbigen Form mit Symbol wie heute", der Goldrahmen kommt erst in D-5b (F-39).
Der Bildplan (`docs/design/DESIGN_D5_BILDPLAN_20261109.md`) nennt dafuer 780 x 150 px bei 0 %
Hoehenbeschnitt; ein Panorama haette 33 bis 45 % seiner Hoehe verloren.

WAS DIESE DATEI PRUEFT
----------------------
1. Die Bilddatei liegt als GESCHNITTENE Kopie unter `assets/bilder/` (nicht das Rohbild aus
   `archiv/`), ist genau 780 x 150 px gross und stimmt mit den Massen im Code ueberein.
2. Mit Bild zeigt die Ansicht das Band ueber dem Titel: die Grafik ist 780 x 150 px, haengt an
   einem Widget derselben Groesse, und der Bildverweis bleibt am Fenster (sonst gibt Tk ihn frei).
3. OHNE Bild bleibt ein leerer Platz in derselben Groesse stehen - kein Absturz, kein erfundenes
   Bild, kein Springen des Fensters.
4. Unter dem Titel laeuft GENAU EINE Trennlinie im gemessenen Rahmengold, und das Gold steht als
   EIN Wert im Code (keine zweite Farbtabelle).
5. Kein zweiter Rahmenstil: das Band sitzt ohne Randleisten; der C2-Rahmen am Gelaendekaestchen
   bleibt, wie er ist (S3 bis S6 unveraendert, F-39 reiht den Goldrahmen nach D-5b).
6. Quellwachen: die Ansicht ruft die Kopfleisten-Methode VOR dem Titel, die Methode liest Pfad und
   Masse aus den Konstanten, laedt mit `tk.PhotoImage` (kein Pillow noetig) und zeigt nie ins
   Archiv.

Aufruf:  .venv/Scripts/python.exe -X utf8 tests/test_portal_kopfleiste.py
"""
from __future__ import annotations

import ast
import inspect
import os
import random
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
import tkinter as tk  # noqa: E402
import main as M  # noqa: E402

BAND = ("assets", "bilder", "portal_kopfband_schmiede_dorf_ghule_780x150.png")
MASSE = (780, 150)                                                  # Platz S1 (F-35/D-5)
GOLD = "#c68b42"                                                    # gemessener Median (D-5)


def _app(seed: int = 11):
    """Frische App mit Siedlung - ohne Fenster auf dem Schirm."""
    random.seed(seed)
    root = tk.Tk()
    root.withdraw()
    app = M.NebelseetalApp(root)
    app._build_main_ui()
    app._erste_siedlung_gruenden()
    root.update_idletasks()
    return root, app


def _rumpf(fn) -> str:
    """Der Quelltext einer Funktion OHNE Docstring - nur die ausgefuehrten Anweisungen.

    Der Docstring wird ueber den Syntaxbaum abgeschnitten (nicht per Textsuche): er darf den
    Pruefgegenstand erklaeren, ohne die Wache selbst zu treffen (Pruefstand-Konvention).
    """
    baum = ast.parse(textwrap.dedent(inspect.getsource(fn)))
    knoten = baum.body[0]
    zeilen = list(getattr(knoten, "body", []))
    while (zeilen and isinstance(zeilen[0], ast.Expr)
           and isinstance(zeilen[0].value, ast.Constant)
           and isinstance(zeilen[0].value.value, str)):
        zeilen = zeilen[1:]
    knoten.body = zeilen or [ast.Pass()]
    return ast.unparse(baum)


def _kinder(widget) -> list:
    """Alle direkten Kinder eines Widgets."""
    return list(widget.winfo_children())


def _bg(widget) -> str:
    """Die Hintergrundfarbe eines Widgets als kleiner Text (leer, wenn es keine hat)."""
    try:
        return str(widget.cget("bg")).lower()
    except Exception:                                                # Widget ohne bg
        return ""


def _bild_name(widget) -> str:
    """Der Name der Tk-Grafik an einem Widget (leer, wenn es keine Bild-Option hat)."""
    try:
        return str(widget.cget("image"))
    except Exception:                                                # Frame hat kein -image
        return ""


def _text(widget) -> str:
    """Der Beschriftungstext eines Widgets (leer, wenn es keine Text-Option hat)."""
    try:
        return str(widget.cget("text"))
    except Exception:                                                # Widget ohne -text
        return ""


def _hoehe(widget) -> int:
    """Die angeforderte Hoehe eines Widgets in px."""
    try:
        return int(widget.winfo_reqheight())
    except Exception:                                                # kein Tk-Widget
        return -1


def _breite(widget) -> int:
    """Die angeforderte Breite eines Widgets in px."""
    try:
        return int(widget.winfo_reqwidth())
    except Exception:                                                # kein Tk-Widget
        return -1


# ==========================================================================
abschnitt("1. Die Bilddatei: geschnittene Kopie in assets, 780 x 150 px")
# ==========================================================================
pfad = os.path.join(ROOT, *BAND)
check("1 die Datei liegt unter assets/bilder", os.path.exists(pfad), pfad)
check("1 der Pfad zeigt NICHT ins Archiv (nur die geschnittene Kopie gehoert ins Spiel)",
      "archiv" not in pfad.lower(), pfad)
check("1 die Konstanten im Code nennen genau diese Datei", tuple(M.PORTAL_KOPFBAND) == BAND,
      str(M.PORTAL_KOPFBAND))
check("1 die Masse im Code sind 780 x 150", tuple(M.PORTAL_KOPFBAND_MASSE) == MASSE,
      str(M.PORTAL_KOPFBAND_MASSE))
if os.path.exists(pfad):
    groesse = os.path.getsize(pfad)
    check("1 die Datei ist 254.385 Byte gross (gemessener Schnitt)", groesse == 254385, str(groesse))
    try:
        from PIL import Image                                        # Groesse wirklich messen
        roh = Image.open(pfad)
        check("1 das Bild ist wirklich 780 x 150 px", roh.size == MASSE, str(roh.size))
    except Exception as e:                                           # ohne Pillow nicht messbar
        befund("1 ohne Pillow ist die Bildgroesse nicht nachgemessen", repr(e))
else:
    befund("1 die Bilddatei fehlt - dann kann auch die Groesse nicht gemessen werden", pfad)

# ==========================================================================
abschnitt("2. Mit Bild: das Band steht ueber dem Titel (Platz S1)")
# ==========================================================================
root, app = _app()
try:
    app._switch_view("Portal")
    root.update_idletasks()
    bild = getattr(app, "portal_kopfband", None)
    check("2 die Ansicht hat ein Bild geladen", bild is not None, str(bild))
    check("2 das Bild ist 780 x 150 px", isinstance(bild, tk.PhotoImage)
          and (bild.width(), bild.height()) == MASSE,
          "-" if bild is None else str((bild.width(), bild.height())))
    flaeche = getattr(app, "portal_kopfleiste", None)
    check("2 das Bild haengt an einem Widget", flaeche is not None, str(flaeche))
    if flaeche is not None:
        check("2 das Widget zeigt genau dieses Bild",
              _bild_name(flaeche) == str(bild), _bild_name(flaeche))
        check("2 das Widget ist 780 x 150 px gross",
              (_breite(flaeche), _hoehe(flaeche)) == MASSE,
              str((_breite(flaeche), _hoehe(flaeche))))
        check("2 das Widget sitzt im Inhaltsbereich", flaeche.winfo_toplevel() is root, "")
    # Lage: Band oben, dann der Titel, darunter die Trennlinie
    kinder = _kinder(app.content)
    y_band = kinder[0].winfo_y() if kinder else -1
    titel = [k for k in kinder if _text(k) == "Portal"]
    y_titel = titel[0].winfo_y() if titel else -1
    linien = [k for k in kinder if _bg(k) == GOLD]
    y_linie = linien[0].winfo_y() if linien else -1
    check("2 das Band steht UEBER dem Titel", 0 <= y_band < y_titel, f"{y_band} < {y_titel}")
    check("2 die Trennlinie steht UNTER dem Titel", y_titel < y_linie, f"{y_titel} < {y_linie}")
    check("2 der Bildverweis bleibt am Fenster (Tk gibt ihn sonst frei)",
          getattr(app, "portal_kopfband", None) is not None, "")
finally:
    root.destroy()

# ==========================================================================
abschnitt("3. Ohne Bild: leerer Platz in derselben Groesse, kein Absturz")
# ==========================================================================
merke = M.PORTAL_KOPFBAND
root, app = _app()
try:
    M.PORTAL_KOPFBAND = ("assets", "bilder", "gibt_es_nicht_D5.png")
    abgestuerzt = ""
    try:
        app._switch_view("Portal")
        root.update_idletasks()
    except Exception as e:                                           # noqa: BLE001
        abgestuerzt = repr(e)
    check("3 die Ansicht stuerzt ohne Bild nicht ab", abgestuerzt == "", abgestuerzt)
    check("3 es wird kein Bild erfunden", getattr(app, "portal_kopfband", None) is None, "")
    flaeche = getattr(app, "portal_kopfleiste", None)
    check("3 es bleibt trotzdem ein Platz stehen", flaeche is not None, str(flaeche))
    if flaeche is not None:
        check("3 der Platz ist 780 x 150 px gross (das Fenster springt nicht)",
              (_breite(flaeche), _hoehe(flaeche)) == MASSE,
              str((_breite(flaeche), _hoehe(flaeche))))
        check("3 der Platz traegt kein Bild", _bild_name(flaeche) == "", _bild_name(flaeche))
    check("3 der Titel steht auch ohne Bild da",
          any(_text(k) == "Portal" for k in _kinder(app.content)), "")
finally:
    M.PORTAL_KOPFBAND = merke
    root.destroy()

# ==========================================================================
abschnitt("4. GENAU EINE Trennlinie im gemessenen Rahmengold")
# ==========================================================================
check("4 das Gold steht als EIN Wert im Code (#C68B42)",
      str(M.PORTAL_TRENNLINIE).lower() == GOLD, str(M.PORTAL_TRENNLINIE))
quelle_datei = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
check("4 das Gold kommt als Zeichenkette nur EINMAL vor (keine zweite Farbtabelle)",
      quelle_datei.count('"#C68B42"') == 1, str(quelle_datei.count('"#C68B42"')))
root, app = _app()
try:
    app._switch_view("Portal")
    root.update_idletasks()
    linien = [k for k in _kinder(app.content) if _bg(k) == GOLD]
    check("4 es gibt genau eine Trennlinie in diesem Gold", len(linien) == 1, str(len(linien)))
    if linien:
        check("4 die Linie ist 2 px hoch", int(linien[0].cget("height")) == 2,
              str(linien[0].cget("height")))
        check("4 die Linie liegt ohne Randleisten im Inhalt",
              int(linien[0].cget("bd")) == 0 and int(linien[0].cget("highlightthickness")) == 0, "")
    check("4 das Band traegt selbst KEIN Gold (kein zweiter Rahmenstil)",
          _bg(getattr(app, "portal_kopfleiste", None)) == str(app.skin["bg"]).lower(),
          _bg(getattr(app, "portal_kopfleiste", None)))
finally:
    root.destroy()

# ==========================================================================
abschnitt("5. Kein zweiter Rahmenstil - S3 bis S6 bleiben, wie sie sind")
# ==========================================================================
root, app = _app()
try:
    app._switch_view("Portal")
    root.update_idletasks()
    flaeche = getattr(app, "portal_kopfleiste", None)
    traeger = flaeche.master if flaeche is not None else None
    check("5 das Band sitzt in einem randlosen Traeger",
          traeger is not None and int(traeger.cget("bd")) == 0
          and int(traeger.cget("highlightthickness")) == 0,
          "" if traeger is None else str((traeger.cget("bd"), traeger.cget("highlightthickness"))))
    check("5 das Band selbst hat keine Randleisten",
          flaeche is not None and int(flaeche.cget("bd")) == 0
          and int(flaeche.cget("highlightthickness")) == 0, "")
    rahmen_code = _rumpf(M.NebelseetalApp._kartenrahmen_bauen)
    check("5 der C2-Rahmen am Kaestchen bleibt der einzige Rahmen (S3)",
          "KACHELRAHMEN" in rahmen_code, "")
    check("5 D-5 laesst das Gelaendekaestchen zeichnen wie vorher",
          getattr(app, "_portal_karte_art", "") in ("gemalt", "flach"),
          str(getattr(app, "_portal_karte_art", "-")))
    flaeche_karte = getattr(app, "portal_zeichenflaeche", None)
    check("5 die Karte hat weiter hoechstens EIN Bild (kein Band auf der Karte)",
          flaeche_karte is not None and len(flaeche_karte.find_withtag("kartenbild")) <= 1,
          "-" if flaeche_karte is None else str(len(flaeche_karte.find_withtag("kartenbild"))))
    befund("5 ehrliche Grenze: der Goldrahmen um das Kaestchen ist NICHT Teil von D-5 - er kommt mit "
           "den Icons in D-5b (F-39). D-5 aendert die Karte, den Portalraum und die Spielregeln nicht.",
           "")
finally:
    root.destroy()

# ==========================================================================
abschnitt("6. Quellwachen")
# ==========================================================================
quelle = _rumpf(M.NebelseetalApp._render_portal)
check("6 die Ansicht ruft die Kopfleisten-Methode", "_portal_kopfleiste" in quelle, "")
check("6 das Band steht VOR dem Titel (Blackletter-Schriftzug)",
      "_portal_kopfleiste" in quelle and "Blackletter" in quelle
      and quelle.index("_portal_kopfleiste") < quelle.index("Blackletter"), "")
check("6 die Trennlinie kommt aus der einen Konstante", "PORTAL_TRENNLINIE" in quelle, "")
check("6 die Ansicht zeigt nicht ins Archiv", "archiv" not in quelle.lower(), "")
hilfe = _rumpf(M.NebelseetalApp._portal_kopfleiste)
check("6 die Methode liest den Pfad aus der Konstante", "PORTAL_KOPFBAND" in hilfe, "")
check("6 die Methode liest die Masse aus der Konstante", "PORTAL_KOPFBAND_MASSE" in hilfe, "")
check("6 das Bild wird mit tk.PhotoImage geladen (kein Pillow noetig)", "PhotoImage" in hilfe, "")
check("6 fehlende Datei wird geprueft, statt zu raten", "os.path.exists" in hilfe, "")
check("6 ohne Bild entsteht ein Platz mit fester Groesse", "pack_propagate" in hilfe, "")
check("6 der Bildverweis wird am Fenster gehalten", "self.portal_kopfband" in hilfe, "")
check("6 die Methode zeigt nicht ins Archiv", "archiv" not in hilfe.lower(), "")
check("6 das Band bekommt keine Randleisten", "highlightthickness=0" in hilfe, "")
check("6 die Weltkartenliste behaelt die farbige Form (kein Kachelausschnitt)",
      "Ausschnitt" not in quelle, "")

sys.exit(bericht())
