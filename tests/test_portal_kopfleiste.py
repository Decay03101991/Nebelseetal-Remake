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

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster"
PRUEF_STUFE = 3
PRUEF_BETRIFFT = ['main:*']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

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


def _wraplength(widget) -> int:
    """Die Umbruchbreite eines Widgets in px (0, wenn es keine hat)."""
    try:
        return int(str(widget.cget("wraplength")) or 0)
    except Exception:                                                # Widget ohne wraplength
        return 0


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
        masse = tuple(getattr(app, "portal_kopfband_masse", MASSE))      # gezeigte Masse
        check("2 das Widget hat die gemeldete Masse",
              (_breite(flaeche), _hoehe(flaeche)) == masse,
              str((_breite(flaeche), _hoehe(flaeche))))
        check("2 die gemeldete Masse ist nie breiter als das Original 780 x 150",
              masse[0] <= MASSE[0] and masse[1] <= MASSE[1], str(masse))
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
abschnitt("2b. Schmale Spalte: das Band wird VERKLEINERT, nie beschnitten (Daniel 17:5x)")
# ==========================================================================
# Gemessen: das Standardfenster ist 1024 x 720, die INHALTSSPALTE darin nur 630 px breit
# (vor D-5 wollten die Inhalte 783 px - der Text war dort schon beschnitten). Daniel hat am
# 09.11.2026 entschieden: "Band bei schmalem Fenster auf die Spaltenbreite VERKLEINERN,
# Original 780 x 150 bleibt die Quelle, kein Beschnitt".
_masse = M.NebelseetalApp._kopfband_masse
check("2b 610 px Spalte ergeben 610 x 117 px (proportional)", _masse(610) == (610, 117),
      str(_masse(610)))
check("2b 630 px Spalte (Standardfenster) bleiben unter dem Original",
      _masse(630)[0] < MASSE[0], str(_masse(630)))
check("2b ab 780 px Spalte gilt das Original", _masse(780) == MASSE and _masse(1600) == MASSE,
      str((_masse(780), _masse(1600))))
check("2b eine unvermessene Spalte (0) faellt aufs Original zurueck", _masse(0) == MASSE,
      str(_masse(0)))
_b, _h = _masse(500)
check("2b das Seitenverhaeltnis bleibt erhalten (kein Verzerren)",
      abs((_b / float(_h)) - (MASSE[0] / float(MASSE[1]))) < 0.02,
      str((_b, _h, round(_b / float(_h), 3))))
check("2b verkleinert wird nie groesser als die Spalte", all(_masse(n)[0] <= n
      for n in (200, 400, 610, 779)), "")

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
# ENTSCHEIDUNG GEAENDERT (11.11.2026, Daniels Befund B6): das Band wird jetzt ZWEIMAL gebaut -
# beim Aufbau der Ansicht und kurz danach, wenn das Inhaltsfenster wirklich vermessen ist. Der
# Bildbau liegt darum in `_kopfband_bild`; die Wachen auf das Bauen wandern mit (nicht geloescht).
bild_code = _rumpf(M.NebelseetalApp._kopfband_bild)
check("6 das Bild wird mit tk.PhotoImage geladen (kein Pillow noetig)", "PhotoImage" in bild_code, "")
# Layout-Schnitt (09.11.2026): die Messung liegt jetzt in `_spaltenbreite` - EINE Quelle fuer
# die acht Textzeilen UND das Kopfband. Die Kopfleiste misst nicht mehr selbst, sie liest die
# Zahl; die Wache auf `winfo_width` wandert mit (Entscheidung, nicht Code zurueckgebogen).
check("6 die Kopfleiste nimmt die Textbreite aus EINER Quelle", "_spaltenbreite" in hilfe, "")
spalte_code = _rumpf(M.NebelseetalApp._spaltenbreite)
check("6 die Spaltenbreite wird GEMESSEN, nicht geraten", "winfo_width" in spalte_code, "")
check("6 die Messung geht durch die eine Umrechnung", "_textbreite" in spalte_code, "")
check("6 die Zielmasse kommt aus der einen Hilfsfunktion", "_kopfband_masse" in hilfe, "")
check("6 verkleinert wird mit Pillow und LANCZOS (ohne Beschnitt)",
      "LANCZOS" in bild_code and "resize" in bild_code, "")
check("6 ohne Pillow bleibt das Original als Rueckfall", "except Exception" in hilfe, "")
check("6 fehlende Datei wird geprueft, statt zu raten", "os.path.exists" in bild_code, "")
# NEU (11.11.2026, B6): das Band muss der Fensterbreite folgen - nicht der gedeckelten Textspalte.
check("6 das Band nimmt die GEMESSENE Inhaltsbreite als erste Quelle",
      "content_canvas.winfo_width" in hilfe, "")
check("6 es gibt einen Nachlauf fuer unvermessene Fenster",
      "after" in hilfe and "nachziehen" in hilfe, "")
check("6 ohne Bild entsteht ein Platz mit fester Groesse", "pack_propagate" in hilfe, "")
check("6 der Bildverweis wird am Fenster gehalten", "self.portal_kopfband" in hilfe, "")
check("6 die Methode zeigt nicht ins Archiv", "archiv" not in hilfe.lower(), "")
check("6 das Band bekommt keine Randleisten", "highlightthickness=0" in hilfe, "")
check("6 die gezeigte Masse wird fuer die Wache gemerkt", "portal_kopfband_masse" in hilfe, "")
check("6 die Weltkartenliste behaelt die farbige Form (kein Kachelausschnitt)",
      "Ausschnitt" not in quelle, "")

# ==========================================================================
abschnitt("7. Die Textbreite folgt der Spalte (Layout-Schnitt, Daniel 18:4x)")
# ==========================================================================
# Daniel 09.11.2026: "Layout schnitt ist ein eigenes thema aber kleiner halten und gut anpassen".
# Gemessen (docs/audits, Probe 09.11.2026): das Standardfenster ist 1024 x 720, die Inhaltsspalte
# darin 630 px - die acht Textzeilen des Portals forderten mit `wraplength=760` bis 763 px, der
# Inhalt insgesamt 783 px. Rechts wird abgeschnitten (eine waagerechte Bildlaufleiste gibt es
# nicht). Seit dem Layout-Schnitt liest alles EINE Zahl: `_spaltenbreite()`.
_tb = M.NebelseetalApp._textbreite
check("7 die Standardspalte 630 px ergibt 610 px Textbreite", _tb(630) == 610, str(_tb(630)))
check("7 eine unvermessene Spalte (0) faellt auf die Entwurfsbreite 780 zurueck",
      _tb(0) == 780, str(_tb(0)))
check("7 eine breite Spalte bleibt bei der Entwurfsbreite 780", _tb(1526) == 780, str(_tb(1526)))
check("7 eine sehr schmale Spalte haelt die Untergrenze 320", _tb(200) == 320, str(_tb(200)))
check("7 die Textbreite ist nie breiter als die Spalte",
      all(_tb(n) <= max(n, 320) for n in (400, 630, 700, 780)), "")
check("7 die Textbreite waechst mit der Spalte bis zum Deckel 780",
      _tb(500) < _tb(630) < _tb(700) < _tb(800) == 780,
      str((_tb(500), _tb(630), _tb(700), _tb(800))))

# Fenster wirklich zeigen und messen - nur so ist die Spaltenbreite echt (im `withdrawn`-Fenster
# ist sie 1). Ist kein Schirm da, bleibt es bei einem BEFUND statt bei einem falschen Rot.
random.seed(11)
root = tk.Tk()
app = M.NebelseetalApp(root)
app._build_main_ui()
app._erste_siedlung_gruenden()
# Der Konstruktor setzt seine EIGENE Groesse (waechst mit dem Schirm, hier 1446 x 744).
# Erst danach auf das Standardfenster stellen - sonst misst die Wache den grossen Schirm.
root.geometry("1024x720+30+30")
root.deiconify()
root.update()
app._switch_view("Portal")
root.update()
try:
    spalte = int(app.content_canvas.winfo_width())                   # gemessene Spalte
    if spalte < 120:                                                 # kein Schirm/kein Fenster
        befund("7 das Fenster ist hier nicht vermessen - die Spaltenmessung bleibt offen",
               str(spalte))
    else:
        text = app._spaltenbreite()
        check("7 die gemessene Spalte ergibt die Textbreite (Spalte - 20, Deckel 780)",
              text == max(320, min(780, spalte - 20)), str((spalte, text)))
        # 11.11.2026 (B6): das Band nimmt NICHT mehr die Textspalte (Deckel 780), sondern die
        # gemessene Inhaltsbreite. Gewartet wird auf den Nachlauf, damit das Fenster vermessen ist.
        import time as _zeit
        for _ in range(40):
            root.update()
            _zeit.sleep(0.01)
        check("7 das Kopfband nimmt die gemessene INHALTSbreite",
              abs(int(app.portal_kopfband_masse[0]) - int(app.content_canvas.winfo_width())) <= 1,
              "%s zu %s" % (str(app.portal_kopfband_masse), str(app.content_canvas.winfo_width())))
        # ENTSCHEIDUNG GEAENDERT (12.11.2026, Daniels Befund B5): die Portalansicht ist seit heute
        # ZWEISPALTIG - ein Traeger-Rahmen (`kopf`) haelt links die Weltkartenliste, rechts die
        # Karte. Ein reiner Traeger hat keinen eigenen Text und darf breiter sein als die
        # Textspalte; gemeint war immer "kein TEXT wird abgeschnitten". Darum werden nur Widgets
        # mit eigenem Text oder Umbruchbreite gemessen, reine Rahmen nicht.
        breiten = [(_breite(k), _text(k)[:28]) for k in _kinder(app.content)
                   if _text(k) != "" or int(str(_wraplength(k)) or 0) > 0]
        zu_breit = [paar for paar in breiten if paar[0] > spalte]
        check("7 kein Inhalt ist breiter als die Spalte (kein Beschnitt)",
              not zu_breit, str(zu_breit[:3]))
        # ENTSCHEIDUNG GEAENDERT (11.11.2026, T6): Daniel hat in C11 verlangt, dass das Kopfband
        # im grossen Fenster BIS ZUM RECHTSRAND geht ("ist scharf, muss aber bei grossem Spielfenster
        # auch bis zum rechten Rand gehen"). Damit ist der Inhalt absichtlich breiter als die
        # TEXTSPALTE - das Band nimmt die gemessene Inhaltsbreite, die Textzeilen bleiben in der
        # Spalte (eigene Wachen oben). Die alte Wache nagelte die alte Entscheidung fest.
        _band = int(app.portal_kopfband_masse[0])
        check("7 das Kopfband reicht bis zum Rand (Breite = gemessene Inhaltsbreite)",
              abs(_band - app._kopfband_ziele(int(app.content_canvas.winfo_width()))[0]) <= 1,
              "%d zu %s" % (_band, app._kopfband_ziele(int(app.content_canvas.winfo_width()))))
        check("7 die Textzeilen bleiben weiter in der Spalte (nur das Band ist breiter)",
              all(int(str(_wraplength(k)) or 0) <= text for k in _kinder(app.content)
                  if int(str(_wraplength(k)) or 0) > 0),
              str([int(str(_wraplength(k)) or 0) for k in _kinder(app.content)][:6]))
        zeilen = [k for k in _kinder(app.content)
                  if int(str(_wraplength(k)) or 0) > 0]
        check("7 alle Textzeilen tragen die gemessene Breite, nicht 760",
              zeilen and all(int(str(_wraplength(k))) == text for k in zeilen),
              str(sorted(set(int(str(_wraplength(k))) for k in zeilen))))
        check("7 keine Textzeile fordert mehr als die Textbreite",
              all(_breite(k) <= text for k in zeilen),
              str(max([_breite(k) for k in zeilen] or [0])))
        flaeche = getattr(app, "portal_kopfleiste", None)
        check("7 das Band bleibt in der Spalte",
              flaeche is not None and _breite(flaeche) <= spalte,
              "-" if flaeche is None else str((_breite(flaeche), spalte)))
finally:
    root.destroy()

sys.exit(bericht())
