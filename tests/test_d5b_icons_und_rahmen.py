# -*- coding: ascii -*-
"""Wache D-5b: Chris' Menue-Icons, Goldrahmen am Gelaendekaestchen, Marktplatz-Kennzeichen.

DANIELS WORT (09.11.2026, zwei Runden)
--------------------------------------
1. "Ja: die 9 Menue-Icons ersetzen, Gebaeude auf der Karte bleiben" - im Baumenu stehen die
   gelieferten Kacheln, die Siedlungskarte bleibt unangetastet.
2. "Ja, Chris' Goldrahmen einbauen (aus der Schmiede-Kachel geschnitten, als 9-Slice)" - der
   Rahmen um das 400 x 400-Gelaendekaestchen kommt aus der Lieferung, nicht aus dem C2-Satz.
3. "markt_handel wird das Kennzeichen der Marktplatz-Ansicht".

WAS DIESE DATEI PRUEFT
----------------------
1. Die Bilddateien: neun Menue-Icons 256 x 256 RGBA und wirklich ANDERE Bilder als der C2-Satz,
   der Rahmen 400 x 400 mit durchsichtiger Mitte und durchsichtigem Eck, das Kennzeichen 96 x 96.
2. Der Schnitt: `gebaeude_optik.rahmen_kanten` liefert mit Band 14 vier Streifen in Zielmass und
   uebernimmt die Ecke PIXELGLEICH aus der Datei.
3. Die eine Quelle: `main.WELTKARTE_RAHMEN` kommt aus `data/gebaeude_motive.json`, und
   `_kartenrahmen_bauen` nimmt diesen Rahmen - mit dem C2-Rahmen als Rueckfall.
4. Im gebauten Fenster: vier Bildleisten um die 400 x 400-Zeichenflaeche, Bilder im Cache.
5. Marktplatz: das Kennzeichen wird geladen und steht neben dem Titel.

Aufruf:  python -X utf8 tests/test_d5b_icons_und_rahmen.py
"""
from __future__ import annotations

import hashlib
import json
import os
import random
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
ROOT = str(ROOT)
import tkinter as tk  # noqa: E402
import gebaeude_optik as G  # noqa: E402
import main as M  # noqa: E402

RAHMEN = "assets/icons/gebaeude/rahmen/kachelrahmen_chris.png"
KENNZEICHEN = "assets/bilder/marktplatz_kennzeichen_96.png"
MENUE = "assets/icons/gebaeude/menue"
C2 = "assets/icons/gebaeude/c2"
NEUN = ("holzfaeller", "schmiede", "jaeger", "farm", "tempel", "steinmetz", "rinderfarm",
        "schafszucht", "verteidigungswall")


def png_kopf(pfad):
    """(Breite, Hoehe, Farbtyp) aus dem PNG-Kopf - ohne Fremdbibliothek."""
    with open(pfad, "rb") as f:
        kopf = f.read(26)
    if kopf[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    breite, hoehe = struct.unpack(">II", kopf[16:24])
    return breite, hoehe, kopf[25]


def sha(pfad) -> str:
    h = hashlib.sha256()
    with open(pfad, "rb") as f:
        for stueck in iter(lambda: f.read(1 << 20), b""):
            h.update(stueck)
    return h.hexdigest()


def _app(seed: int = 7):
    """Frische App mit Siedlung."""
    random.seed(seed)
    root = tk.Tk()
    root.withdraw()
    app = M.NebelseetalApp(root)
    app._build_main_ui()
    app._erste_siedlung_gruenden()
    root.update_idletasks()
    return root, app


def _alle(widget, sammler=None):
    """Alle Widgets unter `widget` (rekursiv) - fuer die Suche nach Labels."""
    sammler = [] if sammler is None else sammler
    for kind in widget.winfo_children():
        sammler.append(kind)
        _alle(kind, sammler)
    return sammler


# ==========================================================================
abschnitt("1. Die Bilddateien sind da und haben die gelieferte Groesse")
# ==========================================================================
rahmen_pfad = os.path.join(ROOT, RAHMEN)
check("1 der Goldrahmen liegt unter assets/", os.path.isfile(rahmen_pfad), RAHMEN)
kopf = png_kopf(rahmen_pfad) if os.path.isfile(rahmen_pfad) else None
check("1 der Rahmen ist 400 x 400 in RGBA", kopf == (400, 400, 6), str(kopf))

if kopf:
    from PIL import Image  # noqa: E402
    _bild = Image.open(rahmen_pfad).convert("RGBA")
    check("1 das Eck des Rahmens ist durchsichtig (abgerundete Ecke)",
          _bild.getpixel((2, 2))[3] == 0, str(_bild.getpixel((2, 2))[3]))
    check("1 das Goldband ist deckend", _bild.getpixel((200, 6))[3] == 255,
          str(_bild.getpixel((200, 6))[3]))
    check("1 die Mitte ist durchsichtig (die Karte scheint durch)",
          _bild.getpixel((200, 200))[3] == 0, str(_bild.getpixel((200, 200))[3]))

fehlend = [n for n in NEUN if not os.path.isfile(os.path.join(ROOT, MENUE, n + ".png"))]
check("1 alle neun Menue-Icons liegen im Projekt", not fehlend, repr(fehlend))
falsch = [n for n in NEUN if png_kopf(os.path.join(ROOT, MENUE, n + ".png")) != (256, 256, 6)]
check("1 jedes Menue-Icon ist 256 x 256 in RGBA", not falsch, repr(falsch))

gleich = [n for n in NEUN
          if os.path.isfile(os.path.join(ROOT, C2, n + ".png"))
          and sha(os.path.join(ROOT, MENUE, n + ".png")) == sha(os.path.join(ROOT, C2, n + ".png"))]
check("1 die neun Icons sind NICHT die alten C2-Bilder", not gleich, repr(gleich))

kenn_pfad = os.path.join(ROOT, KENNZEICHEN)
check("1 das Marktplatz-Kennzeichen liegt in Anzeigegroesse 96 x 96",
      os.path.isfile(kenn_pfad) and png_kopf(kenn_pfad)[:2] == (96, 96),
      str(png_kopf(kenn_pfad) if os.path.isfile(kenn_pfad) else "fehlt"))

# ==========================================================================
abschnitt("2. Der Schnitt: vier Streifen, Band 14 px, Ecke aus der Datei")
# ==========================================================================
teile = G.rahmen_kanten(RAHMEN, 400, 400, 14)
check("2 vier Streifen entstehen", set(teile) >= {"oben", "unten", "links", "rechts"},
      str(sorted(teile)))
if teile:
    check("2 oben und unten sind 400 x 14", teile["oben"].size == (400, 14)
          and teile["unten"].size == (400, 14), str(teile["oben"].size))
    check("2 links und rechts sind 14 x 372", teile["links"].size == (14, 372)
          and teile["rechts"].size == (14, 372), str(teile["links"].size))
    check("2 der Rand ist das uebergebene Band, nicht ein Viertel der Kante",
          teile["rand"] == 14, str(teile["rand"]))
    if kopf:
        # ENTSCHEIDUNG GEAENDERT (11.11.2026, T5 - dieselbe Umstellung wie in
        # tests/test_weltkarte_rahmen.py): die Originalecke traegt einen Bogen von rund 30 px, der
        # in das Kachelraster hineinlief (Daniels Befund C10). Die Ecke kommt jetzt aus dem GERADEN
        # Kantenstueck und ist rechtwinklig - sie ist damit absichtlich nicht mehr pixelgleich mit
        # der Bogen-Ecke der Datei. Geprueft wird stattdessen, dass die Ecke so deckend ist wie das
        # Band (kein Bogen) und dass das Fenster ein Rechteck bleibt.
        from PIL import Image  # noqa: E402
        _alpha = teile["oben"].convert("RGBA").split()[3]
        _ecke = _alpha.crop((0, 0, 14, 14))
        _band = _alpha.crop((14, 0, 28, 14))
        _leer_ecke = sum(1 for a in _ecke.getdata() if a < 8)
        _leer_band = sum(1 for a in _band.getdata() if a < 8)
        check("2 die linke obere Ecke ist rechtwinklig (so deckend wie das Band, kein Bogen)",
              _leer_ecke <= _leer_band + 4,
              "Ecke %d, Band %d fast durchsichtige Pixel" % (_leer_ecke, _leer_band))
check("2 zu kleine Masse liefern ein leeres dict (kein Absturz)",
      G.rahmen_kanten(RAHMEN, 20, 20, 14) == {}, "")

# ==========================================================================
abschnitt("3. Eine Quelle: die Datendatei nennt Pfad und Band")
# ==========================================================================
with open(os.path.join(ROOT, "data", "gebaeude_motive.json"), encoding="utf-8") as f:
    block = (json.load(f) or {}).get("kachelrahmen") or {}
check("3 die Datendatei nennt den Goldrahmen", block.get("weltkarte") == RAHMEN,
      str(block.get("weltkarte")))
check("3 die Datendatei nennt das Band in px", block.get("weltkarte_rand") == 14,
      str(block.get("weltkarte_rand")))
check("3 der C2-Rahmen bleibt fuer den Rasterweg eingetragen",
      str(block.get("ruhe") or "").endswith("kachelrahmen_ruhe.png"), str(block.get("ruhe")))
check("3 main.WELTKARTE_RAHMEN liest genau diese Angaben",
      M.WELTKARTE_RAHMEN == (RAHMEN, 14, 400), str(M.WELTKARTE_RAHMEN))

# ==========================================================================
abschnitt("4. Im Fenster: vier Bildleisten um die Karte")
# ==========================================================================
root, app = _app()
try:
    app._switch_view("Portal")
    root.update_idletasks()

    def _karte(widget):
        for kind in widget.winfo_children():
            if isinstance(kind, tk.Canvas) and int(kind.cget("width") or 0) == 400:
                return kind
            treffer = _karte(kind)
            if treffer is not None:
                return treffer
        return None

    karte = _karte(app.content)
    check("4 die Zeichenflaeche ist 400 x 400", karte is not None
          and int(karte.cget("height")) == 400, str(karte.cget("height") if karte else "-"))
    rahmen = karte.master.master if karte is not None else None
    leisten = [k for k in rahmen.winfo_children() if isinstance(k, tk.Label)] if rahmen else []
    check("4 vier Bildleisten umrahmen die Karte", len(leisten) == 4, "%d Leisten" % len(leisten))
    masze = sorted((int(root.tk.call("image", "width", str(k.cget("image")))),
                    int(root.tk.call("image", "height", str(k.cget("image"))))) for k in leisten)
    check("4 die Leisten tragen das Band von 14 px",
          masze == sorted([(400, 14), (400, 14), (14, 372), (14, 372)]), str(masze))
    check("4 der Rahmen haelt seine Bilder", bool(getattr(rahmen, "bilder", {})) if rahmen else False,
          str(sorted(getattr(rahmen, "bilder", {}) or {})))
    check("4 der Rahmen ist zwischengespeichert", bool(getattr(app, "_kartenrahmen_cache", {})),
          str(len(getattr(app, "_kartenrahmen_cache", {}))))
finally:
    root.destroy()

# ==========================================================================
abschnitt("5. Marktplatz: das Kennzeichen steht neben dem Titel")
# ==========================================================================
root, app = _app()
try:
    app._switch_view("Marktplatz")
    root.update_idletasks()
    bild = getattr(app, "_kennzeichen_cache", None)
    check("5 das Kennzeichen wird geladen", bild is not None, repr(bild))
    check("5 es ist ein Tk-Bild in Anzeigegroesse", bild is not None
          and int(bild.width()) == 96 and int(bild.height()) == 96,
          "%s x %s" % (getattr(bild, "width", lambda: "-")(), getattr(bild, "height", lambda: "-")()))
    titel = [k for k in _alle(app.content)
             if isinstance(k, tk.Label) and str(k.cget("text")) == "Marktplatz"]
    check("5 der Titel steht weiter in der Ansicht", bool(titel), "%d Treffer" % len(titel))
    mit_bild = [k for k in _alle(app.content) if isinstance(k, tk.Label) and str(k.cget("image"))]
    check("5 das Kennzeichen haengt an einem Bild-Label", bool(mit_bild), "%d Bild-Label" % len(mit_bild))
finally:
    root.destroy()

# ==========================================================================
abschnitt("6. Quellwachen")
# ==========================================================================
import ast  # noqa: E402
import inspect  # noqa: E402
import textwrap  # noqa: E402


def _rumpf(fn) -> str:
    baum = ast.parse(textwrap.dedent(inspect.getsource(fn)))
    baum.body[0].body = [k for k in baum.body[0].body
                         if not (isinstance(k, ast.Expr) and isinstance(k.value, ast.Constant)
                                 and isinstance(k.value.value, str))]
    return ast.unparse(baum)


rahmen_code = _rumpf(M.NebelseetalApp._kartenrahmen_bauen)
check("6 der Rahmen kommt aus WELTKARTE_RAHMEN", "WELTKARTE_RAHMEN" in rahmen_code, "")
check("6 der C2-Rahmen bleibt der Rueckfall", "KACHELRAHMEN" in rahmen_code, "")
check("6 das Band wird mit der Breite mitskaliert", "rahmenrand" in rahmen_code
      and "breite" in rahmen_code, "")
markt = _rumpf(M.NebelseetalApp._render_market)
check("6 die Marktplatz-Ansicht holt das Kennzeichen", "_kennzeichen_bild" in markt, "")
lader = _rumpf(M._lade_weltkarte_rahmen)
check("6 der Lader liest die eine Datendatei", "gebaeude_motive.json" in lader, "")
befund("6 Was NICHT geprueft ist: dass ein Mensch den Rahmen im Betrieb als stimmig empfindet - "
       "das ist die Sichtpruefung am Bildschirmfoto (docs/audits/bilder/), nicht eine Zahl.", "")

sys.exit(bericht())
