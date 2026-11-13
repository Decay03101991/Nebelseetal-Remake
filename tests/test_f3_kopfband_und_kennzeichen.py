# -*- coding: ascii -*-
"""Wache F3: Kopfband je Volk und Kennzeichen auf 96 px (13.11.2026, Sitzung 45).

WOHER DIE AUFGABE KOMMT
-----------------------
Claudes Antwort Nr. 19 (Bildauftrag, Bildbedarf B8): heute gibt es EIN Kopfband mit Ghule-Motiv
fuer alle sechs Voelker; gebraucht werden sechs, je 4508 x 868. Zugleich ist die neue Kennzeichen-
Datei 384 x 384 - und `tk.PhotoImage` skaliert von sich aus nicht. Beides macht nur den Weg frei
fuer die Dezember-Bilder; es aendert kein Bild im Spiel und keine Groesse.

WAS DIESE DATEI PRUEFT
----------------------
1. Die Zuordnung steht in `data/portal_kopfbaender.json`: sechs Voelker, sechs VERSCHIEDENE
   Dateien, ein Standard (das Ghule-Band). Kein Bandpfad im Quelltext.
2. Auswahl: sechs Voelker -> sechs verschiedene Dateien; fehlender Eintrag oder fehlende Datei
   -> Ghule-Band; gar kein Band -> None (leerer Platz, kein Absturz).
3. Die Groessenlogik bleibt: Breite folgt der Spalte, Hoehe nie ueber KOPFBAND_HOECHSTHOEHE,
   Beschnitt statt Verzerrung.
4. Kennzeichen: eine 384er-Testdatei kommt durch BEIDE Wege (Pillow und Tk-subsample) auf 96 px.
5. Quellwachen: die alte Einzelkonstante ist weg, das Volk kommt aus `spieler_fraktion`.

Aufruf:  .venv/Scripts/python.exe -X utf8 tests/test_f3_kopfband_und_kennzeichen.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------  # noqa: E501
PRUEF_ART = "fenster"
PRUEF_STUFE = 3
PRUEF_BETRIFFT = ['main:*']
PRUEF_DATEN = ['data/portal_kopfbaender.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import ast
import inspect
import json
import os
import random
import shutil
import sys
import tempfile
import textwrap
import types

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
import tkinter as tk  # noqa: E402
import main as M  # noqa: E402

DATEI = os.path.join(ROOT, "data", "portal_kopfbaender.json")
VOELKER = ["menschlich", "zwergisch", "elfisch", "Trolle", "Ghule", "Gnome"]
BAND = "assets/bilder/portal_kopfband_schmiede_dorf_ghule_780x150.png"
MASSE = (780, 150)


def _app(seed: int = 11):
    """Frische App ohne Fenster auf dem Schirm."""
    random.seed(seed)
    root = tk.Tk()
    root.withdraw()
    app = M.NebelseetalApp(root)
    app._build_main_ui()
    app._erste_siedlung_gruenden()
    root.update_idletasks()
    return root, app


def _rumpf(fn) -> str:
    """Der Quelltext einer Funktion OHNE Docstring (Pruefstand-Konvention)."""
    baum = ast.parse(textwrap.dedent(inspect.getsource(fn)))
    knoten = baum.body[0]
    zeilen = list(getattr(knoten, "body", []))
    while (zeilen and isinstance(zeilen[0], ast.Expr)
           and isinstance(zeilen[0].value, ast.Constant)
           and isinstance(zeilen[0].value.value, str)):
        zeilen = zeilen[1:]
    knoten.body = zeilen or [ast.Pass()]
    return ast.unparse(baum)


def _png(pfad: str, breite: int, hoehe: int) -> bool:
    """Eine Testdatei schreiben (Pillow). False, wenn kein Pillow da ist."""
    try:
        from PIL import Image
        Image.new("RGB", (int(breite), int(hoehe)), (12, 34, 56)).save(pfad)
        return True
    except Exception:                                                 # noqa: BLE001
        return False


# ==========================================================================
abschnitt("1. Die Zuordnung in data/portal_kopfbaender.json")
# ==========================================================================
check("1 die Zuordnungsdatei liegt in data/", os.path.exists(DATEI), DATEI)
_standard, _zuordnung = M._lade_portal_kopfbaender()
check("1 der Standard ist das Ghule-Band (Rueckfall fuer alle)", _standard == BAND, _standard)
check("1 es gibt genau sechs Eintraege", len(_zuordnung) == 6, str(sorted(_zuordnung)))
check("1 die Kennungen sind die aus data/voelker.json (kein zweiter Volksbegriff)",
      sorted(_zuordnung) == sorted(VOELKER), str(sorted(_zuordnung)))
check("1 die sechs Eintraege sind sechs VERSCHIEDENE Dateien",
      len(set(_zuordnung.values())) == 6, str(len(set(_zuordnung.values()))))
check("1 kein Eintrag zeigt ins Archiv", all("archiv" not in v.lower()
      for v in _zuordnung.values()), str(_zuordnung))
check("1 die Eintraege sind Pfade unter assets/", all(v.startswith("assets/")
      for v in _zuordnung.values()), str(_zuordnung))
with open(DATEI, encoding="utf-8") as f:                              # Rohform pruefen
    _roh = json.load(f)
check("1 die Datei nennt Zweck, Quelle und Pflegeregel",
      all(_roh.get(k) for k in ("_zweck", "_quelle", "_regel", "_pflege")), str(sorted(_roh)))
check("1 die Datei traegt KEINE Bildmasse (die Masse steht EINMAL im Code)",
      "masse" not in _roh and "masse_px" not in _roh, str(sorted(_roh)))

# ==========================================================================
abschnitt("2. Auswahl: sechs Voelker, sechs Dateien, Ghule-Rueckfall")
# ==========================================================================
# Heute (13.11.2026) fehlen die sechs Dezember-Baender: dann muss ueberall das Ghule-Band kommen.
_ghule = os.path.normcase(M.portal_kopfband_pfad("Ghule"))
check("2 heute liefert jedes Volk ein Band (das Ghule-Band), keines ist leer",
      all(M.portal_kopfband_pfad(v) for v in VOELKER), "-")
check("2 heute spielt ueberall das Ghule-Band (die Dezember-Dateien fehlen noch)",
      all(os.path.normcase(M.portal_kopfband_pfad(v)) == _ghule for v in VOELKER), _ghule)

# Jetzt mit sechs vorhandenen Testdateien + eigener Zuordnungsdatei.
_tmp = tempfile.mkdtemp(prefix="f3_kopfband_")
merke_datei = M.PORTAL_KOPFBAENDER_DATEI
try:
    _anlage = {"standard": BAND, "voelker": {}}
    _geschrieben = []
    for i, volk in enumerate(VOELKER):
        rel = "assets/bilder/f3_probe_%d_%d.png" % (i, os.getpid())
        ziel = os.path.join(ROOT, rel.replace("/", os.sep))
        if _png(ziel, 4508 if i == 0 else 900, 868 if i == 0 else 174):
            _geschrieben.append(ziel)
            _anlage["voelker"][volk] = rel
    _probe_datei = os.path.join(_tmp, "kopfbaender_probe.json")
    with open(_probe_datei, "w", encoding="utf-8") as f:
        json.dump(_anlage, f, ensure_ascii=False)
    M.PORTAL_KOPFBAENDER_DATEI = _probe_datei
    _pfade = [os.path.normcase(M.portal_kopfband_pfad(v)) for v in VOELKER]
    if not _geschrieben:                                             # ohne Pillow keine Probebilder
        befund("2 ohne Pillow sind keine Probebilder zu schreiben - Auswahl bleibt hier ungemessen",
               "")
    else:
        check("2 sechs Voelker liefern sechs verschiedene Dateien",
              len(set(_pfade)) == 6, str(len(set(_pfade))))
        check("2 jedes gelieferte Band ist die Datei SEINES Volkes",
              all(M.portal_kopfband_pfad(v) == os.path.join(ROOT, _anlage["voelker"][v]
                                                            .replace("/", os.sep))
                  for v in VOELKER), str(_pfade[:2]))
        check("2 das 4508er-Band wird angenommen, nicht auf 780 gekuerzt (F3)",
              M.portal_kopfband_pfad(VOELKER[0]).endswith("f3_probe_0_%d.png" % os.getpid()),
              M.portal_kopfband_pfad(VOELKER[0]))
    # Volk ohne Eintrag, Volk mit fehlender Datei -> Ghule-Band
    check("2 ein unbekanntes Volk bekommt das Ghule-Band",
          os.path.normcase(M.portal_kopfband_pfad("Wolpertinger")) == _ghule, "-")
    _anlage2 = dict(_anlage)
    _anlage2["voelker"] = dict(_anlage["voelker"])
    _anlage2["voelker"]["Trolle"] = "assets/bilder/gibt_es_nicht_f3.png"
    with open(_probe_datei, "w", encoding="utf-8") as f:
        json.dump(_anlage2, f, ensure_ascii=False)
    _ohne = M.portal_kopfband_pfad("Trolle")
    _erwartet = os.path.join(ROOT, *_anlage["voelker"]["Trolle"].split("/")) \
        if _anlage["voelker"].get("Trolle") else ""
    check("2 eine fehlende Datei faellt auf das Ghule-Band zurueck (kein Absturz)",
          os.path.normcase(_ohne) == _ghule, _ohne)
    # Standard selbst fehlt -> gar kein Bild, die Ansicht bleibt beim leeren Platz
    with open(_probe_datei, "w", encoding="utf-8") as f:
        json.dump({"standard": "assets/bilder/gibt_es_nicht_f3.png",
                   "voelker": {"Trolle": "assets/bilder/gibt_es_nicht_f3b.png"}}, f)
    check("2 fehlt auch der Standard, kommt ein leerer Pfad (kein geratener Pfad)",
          M.portal_kopfband_pfad("Trolle") == "", M.portal_kopfband_pfad("Trolle"))
    # Kaputte/fehlende Zuordnungsdatei -> kein Bild, keine Ausnahme
    M.PORTAL_KOPFBAENDER_DATEI = os.path.join(_tmp, "gibt_es_nicht.json")
    check("2 ohne Zuordnungsdatei kommt ein leerer Pfad (keine Ausnahme)",
          M.portal_kopfband_pfad("Ghule") == "", M.portal_kopfband_pfad("Ghule"))
finally:
    M.PORTAL_KOPFBAENDER_DATEI = merke_datei
    for _p in locals().get("_geschrieben", []):
        try:
            os.remove(_p)
        except OSError:
            pass
    shutil.rmtree(_tmp, ignore_errors=True)

# ==========================================================================
abschnitt("3. Die Groessenlogik bleibt unangetastet (T6, D-5)")
# ==========================================================================
_ziele = M.NebelseetalApp._kopfband_ziele
_b, _h, _s = _ziele(630)
check("3 die Breite folgt der Spalte", _b == 630, str((_b, _h, _s)))
check("3 die Hoehe folgt dem Verhaeltnis 780 : 150", abs(_h - round(150 * 630 / 780.0)) <= 1,
      str(_h))
_b, _h, _s = _ziele(2000)
check("3 die Hoehe wird nie ueber KOPFBAND_HOECHSTHOEHE gedeckelt",
      _h == int(M.KOPFBAND_HOECHSTHOEHE), str(_h))
check("3 bei Deckelung wird BESCHNITTEN, nicht verzerrt", _s is True, str(_s))
check("3 die Masse stehen EINMAL im Code (780 x 150)", tuple(M.PORTAL_KOPFBAND_MASSE) == MASSE,
      str(M.PORTAL_KOPFBAND_MASSE))
check("3 die unvermessene Spalte faellt aufs Original", _ziele(1)[:2] == MASSE, str(_ziele(1)))
# Ein 4508er-Band laeuft durch dieselbe Logik (kein eigener Rechenweg fuer die neuen Dateien).
check("3 ein Band in 5,2 : 1 ergibt bei 1127 px Spalte 217 px natuerliche Hoehe",
      _ziele(1127)[0] == 1127 and _ziele(1127)[1] == int(M.KOPFBAND_HOECHSTHOEHE)
      and _ziele(1127)[2] is True, str(_ziele(1127)))

# ==========================================================================
abschnitt("4. Kennzeichen: 384 px hinein, 96 px heraus - auf BEIDEN Wegen")
# ==========================================================================
check("4 die Anzeigegroesse ist fest 96 px (D-5b)", int(M.MARKTPLATZ_KENNZEICHEN_PX) == 96,
      str(M.MARKTPLATZ_KENNZEICHEN_PX))
_tmp2 = tempfile.mkdtemp(prefix="f3_kennzeichen_")
_gross = os.path.join(_tmp2, "kennzeichen_384.png")
_merke_konst = M.MARKTPLATZ_KENNZEICHEN
_merke_pillow = sys.modules.get("PIL")
try:
    if not _png(_gross, 384, 384):                                   # ohne Pillow kein Probebild
        befund("4 ohne Pillow ist die 384er-Probe nicht zu schreiben", "")
    else:
        from PIL import Image                                        # Groesse nachmessen
        check("4 die Probdatei ist wirklich 384 x 384", Image.open(_gross).size == (384, 384),
              str(Image.open(_gross).size))
        # (a) Pillow-Weg ueber _motivbild_skaliert
        M.MARKTPLATZ_KENNZEICHEN = tuple(os.path.join(_tmp2, "kennzeichen_384.png").split(os.sep))
        root, app = _app()
        try:
            for _merk in ("_kennzeichen_cache", "_kennzeichen_cache2"):
                if hasattr(app, _merk):
                    delattr(app, _merk)
            bild = app._kennzeichen_bild()
            check("4 (a) mit Pillow wird die 384er-Datei auf 96 px eingepasst",
                  bild is not None and (int(bild.width()), int(bild.height())) == (96, 96),
                  "-" if bild is None else str((bild.width(), bild.height())))
        finally:
            root.destroy()
        # (b) OHNE Pillow: PIL-Import scheitern lassen -> Tk + subsample
        sys.modules["PIL"] = types.ModuleType("PIL")                 # kein Untermodul Image
        root, app = _app()
        try:
            for _merk in ("_kennzeichen_cache", "_kennzeichen_cache2"):
                if hasattr(app, _merk):
                    delattr(app, _merk)
            bild = app._kennzeichen_bild()
            check("4 (b) ohne Pillow kommt dieselbe Groesse heraus (Tk subsample)",
                  bild is not None and (int(bild.width()), int(bild.height())) == (96, 96),
                  "-" if bild is None else str((bild.width(), bild.height())))
        finally:
            root.destroy()
            if _merke_pillow is not None:
                sys.modules["PIL"] = _merke_pillow
            else:
                sys.modules.pop("PIL", None)
    # (c) fehlende Kennzeichen-Datei -> None, die Ansicht bleibt wie vorher
    M.MARKTPLATZ_KENNZEICHEN = ("assets", "bilder", "gibt_es_nicht_f3.png")
    root, app = _app()
    try:
        abgestuerzt = ""
        try:
            bild = app._kennzeichen_bild()
        except Exception as e:                                       # noqa: BLE001
            abgestuerzt = repr(e)
            bild = "ABSTURZ"
        check("4 (c) eine fehlende Datei ergibt None und keinen Absturz",
              bild is None and abgestuerzt == "", str(bild))
    finally:
        root.destroy()
finally:
    M.MARKTPLATZ_KENNZEICHEN = _merke_konst
    shutil.rmtree(_tmp2, ignore_errors=True)

# ==========================================================================
abschnitt("5. Die Ansicht zeigt das Band des Volkes (mit Bild, ohne Fenster)")
# ==========================================================================
_tmp3 = tempfile.mkdtemp(prefix="f3_band_")
merke_datei3 = M.PORTAL_KOPFBAENDER_DATEI
try:
    _probe = os.path.join(_tmp3, "band_trolle_4508x868.png")
    if _png(_probe, 4508, 868):
        _rel = "assets/bilder/f3_band_probe_%d.png" % os.getpid()
        _ziel = os.path.join(ROOT, _rel.replace("/", os.sep))
        shutil.copyfile(_probe, _ziel)
        _jd = os.path.join(_tmp3, "zuordnung.json")
        with open(_jd, "w", encoding="utf-8") as f:
            json.dump({"standard": BAND, "voelker": {"Trolle": _rel}}, f)
        M.PORTAL_KOPFBAENDER_DATEI = _jd
        root, app = _app()
        try:
            app.state.spieler_fraktion = "Trolle"                    # Volk des Spielers
            check("5 die Ansicht liest das Volk aus spieler_fraktion",
                  app._kopfband_volk() == "Trolle", app._kopfband_volk())
            bild = app._kopfband_bild(*MASSE, False)                 # Zielmasse = Entwurf
            check("5 das 4508er-Band wird NICHT sechsfach zu gross geladen",
                  bild is not None and int(bild.width()) <= MASSE[0],
                  "-" if bild is None else str((bild.width(), bild.height())))
            check("5 die Hoehe bleibt im Verhaeltnis 5,2 : 1",
                  bild is not None and abs(int(bild.height()) - round(150 * 780 / 780.0)) <= 3,
                  "-" if bild is None else str(bild.height()))
            app.state.spieler_fraktion = "Gnome"                     # Volk ohne eigene Datei
            check("5 ein Volk ohne eigene Datei spielt das Ghule-Band",
                  os.path.normcase(M.portal_kopfband_pfad(app._kopfband_volk())) == _ghule,
                  M.portal_kopfband_pfad("Gnome"))
        finally:
            root.destroy()
            try:
                os.remove(_ziel)
            except OSError:
                pass
    else:
        befund("5 ohne Pillow ist die 4508er-Probe nicht zu schreiben", "")
finally:
    M.PORTAL_KOPFBAENDER_DATEI = merke_datei3
    shutil.rmtree(_tmp3, ignore_errors=True)

# ==========================================================================
abschnitt("6. Quellwachen")
# ==========================================================================
quelle = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
check("6 es gibt keine Einzelkonstante PORTAL_KOPFBAND mehr",
      "PORTAL_KOPFBAND =" not in quelle and "PORTAL_KOPFBAND)" not in quelle
      and "_bild_pfad(PORTAL_KOPFBAND" not in quelle, "")
check("6 die Zuordnung wird aus data/portal_kopfbaender.json gelesen",
      "portal_kopfbaender.json" in quelle, "")
check("6 der Bandpfad kommt aus EINER Funktion", "def portal_kopfband_pfad" in quelle, "")
check("6 die Auswahl liest das Volk des Spielers", "spieler_fraktion" in _rumpf(
      M.NebelseetalApp._kopfband_volk), "")
_hilfe = _rumpf(M.NebelseetalApp._portal_kopfleiste)
check("6 die Kopfleiste holt das Band ueber die Zuordnung",
      "portal_kopfband_pfad" in _hilfe and "_kopfband_volk" in _hilfe, "")
_bildcode = _rumpf(M.NebelseetalApp._kopfband_bild)
check("6 der Bildbau nutzt dieselbe Zuordnung",
      "portal_kopfband_pfad" in _bildcode and "_kopfband_volk" in _bildcode, "")
check("6 der Bildbau prueft die GELADENE Groesse, statt sie anzunehmen", "width()" in _bildcode, "")
check("6 ohne Pillow wird ganzzahlig verkleinert (subsample), nicht zu gross gezeigt",
      "subsample" in _bildcode, "")
check("6 das Kennzeichen wird eingepasst, nicht in Anzeigegroesse geladen",
      "_motivbild_skaliert" in _rumpf(M.NebelseetalApp._kennzeichen_bild), "")
check("6 die Zielgroesse des Kennzeichens ist EIN Wert",
      quelle.count("MARKTPLATZ_KENNZEICHEN_PX = 96") == 1, "")

sys.exit(bericht())
