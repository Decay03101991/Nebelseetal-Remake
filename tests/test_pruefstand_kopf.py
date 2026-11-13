# -*- coding: ascii -*-
"""M1-Metawache: jede Pruefdatei traegt Art, Stufe, BETRIFFT und DATEN im Kopf.

Claudes Begruendung (Antwort Nr. 16, Teil B, M1): ohne diese vier Angaben gibt es keine Stufenwahl
und keine gezielte Auswahl - und 184 von 230 Dateien haengen heute an `main`, weshalb eine Auswahl
nach Modul wertlos ist.

Was diese Datei beweist
-----------------------
1. LESEN: `harness.kopf_lesen` liest die vier Angaben mit `ast.literal_eval` - ohne die Datei zu
   importieren; fehlt der Kopf, gelten die Ersatzwerte (Art aus `tkinter` im Text, Stufe 3,
   BETRIFFT aus den Modulnamen im Text, DATEN aus den *.json-Namen im Text) und `kopf_fehlt` ist
   True. Das ist die Rueckwaertsvertraeglichkeit.
2. BESTAND: die Zahl der Dateien OHNE Kopf wird als Messwert gefuehrt und soll fallen. Sie ist
   heute ein BEFUND, kein Fehler - alte Dateien werden nicht ueber Nacht rot.
3. HART nur fuer Dateien, die NACH dem Stichtag angelegt wurden (`git log --diff-filter=A`):
   eine neue Pruefdatei ohne Kopf ist ein Fehler.
4. GEGENPROBE: eine Probedatei ohne Kopf, die nach dem Stichtag angelegt wurde, wird als Fehler
   erkannt; dieselbe Datei MIT Kopf nicht.
5. Der Vorschlag kommt aus den Daten: `tools/kopf_vorschlag.py` liest Paket 15b, die Stufe folgt
   der Startregel (T4 = 4, rechnen unter 2 s = 1, fenster bis 20 s = 2, Rest 3).

Aufruf:  python -X utf8 tests/test_pruefstand_kopf.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['harness']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import datetime
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src, kopf_lesen, messwert

ROOT, SRC = import_src()
sys.path.insert(0, os.path.join(ROOT, "tools"))
import kopf_vorschlag as K  # noqa: E402

# Stichtag ist der Zeitpunkt, an dem M1 eingefuehrt wurde (Register 561, 12.11.2026 23:4x).
# Aeltere Dateien duerfen ohne Kopf bleiben (Rueckwaertsvertraeglichkeit) - NEUE nicht.
STICHTAG = datetime.datetime(2026, 11, 12, 23, 40, 0).timestamp()


def anlagedatum(pfad: str):
    """Wann die Datei angelegt wurde: aus git (erster Commit), sonst aus dem Dateidatum."""
    try:
        rel = os.path.relpath(pfad, ROOT).replace("\\", "/")
    except ValueError:                     # anderes Laufwerk (Temp auf C:, Repo auf D:)
        rel = ""
    if rel and not rel.startswith(".."):
        try:
            p = subprocess.run(["git", "log", "--diff-filter=A", "--format=%ct", "--", rel],
                               capture_output=True, text=True, cwd=ROOT, timeout=30)
            if p.returncode == 0 and (p.stdout or "").strip():
                return float(p.stdout.strip().splitlines()[-1])
        except (OSError, subprocess.SubprocessError, ValueError):
            pass
    try:
        return os.path.getmtime(pfad)
    except OSError:
        return 0.0


DATEIEN = sorted(n for n in os.listdir(os.path.join(ROOT, "tests"))
                 if n.startswith("test_") and n.endswith(".py"))

# ==========================================================================
abschnitt("1. Lesen ohne Import: Kopf, Ersatzwerte, kaputte Angaben")
# ==========================================================================
with tempfile.TemporaryDirectory() as ordner:
    mit = os.path.join(ordner, "test_mit_kopf.py")
    with open(mit, "w", encoding="ascii") as fh:
        fh.write('"""Docstring.\n\nNoch ein Absatz.\n"""\n'
                 'PRUEF_ART = "fenster+messen"\nPRUEF_STUFE = 2\n'
                 'PRUEF_BETRIFFT = ["main:_render_settlement_map", "hintergrund_optik"]\n'
                 'PRUEF_DATEN = ["gelaende.json"]\n')
    _k = kopf_lesen(mit)
    check("der Kopf wird gelesen (art)", _k["art"] == "fenster+messen", str(_k["art"]))
    check("der Kopf wird gelesen (stufe)", _k["stufe"] == 2, str(_k["stufe"]))
    check("der Kopf wird gelesen (betrifft)",
          _k["betrifft"] == ["main:_render_settlement_map", "hintergrund_optik"],
          str(_k["betrifft"]))
    check("der Kopf wird gelesen (daten)", _k["daten"] == ["gelaende.json"], str(_k["daten"]))
    check("kopf_fehlt ist False", _k["kopf_fehlt"] is False, str(_k["kopf_fehlt"]))

    ohne = os.path.join(ordner, "test_ohne_kopf.py")
    with open(ohne, "w", encoding="ascii") as fh:
        fh.write('"""Prueft main.py und liest data/gelaende.json."""\nimport main\n')
    _o = kopf_lesen(ohne)
    check("ohne Kopf ist kopf_fehlt True", _o["kopf_fehlt"] is True, str(_o["kopf_fehlt"]))
    check("Ersatzstufe ist 3", _o["stufe"] == 3, str(_o["stufe"]))
    check("Ersatzart ist 'rechnen' (kein tkinter im Text)", _o["art"] == "rechnen", str(_o["art"]))
    check("Ersatz-BETRIFFT nennt das Modul aus dem Text", "main" in _o["betrifft"],
          str(_o["betrifft"]))
    check("Ersatz-DATEN nennt die Datei aus dem Text", "gelaende.json" in _o["daten"],
          str(_o["daten"]))

    kaputt = os.path.join(ordner, "test_kaputt.py")
    with open(kaputt, "w", encoding="ascii") as fh:
        fh.write('PRUEF_ART = "fenster"\nPRUEF_STUFE = 9\nimport tkinter\n')
    _kap = kopf_lesen(kaputt)
    check("eine unmoegliche Stufe wird auf 3 gesetzt", _kap["stufe"] == 3, str(_kap["stufe"]))
    check("die gueltige Art bleibt erhalten", _kap["art"] == "fenster", str(_kap["art"]))

# ==========================================================================
abschnitt("2. Bestand: wie viele Pruefdateien tragen schon einen Kopf?")
# ==========================================================================
_fehlend, _mit_kopf, _hart = [], 0, []
for name in DATEIEN:
    pfad = os.path.join(ROOT, "tests", name)
    kopf = kopf_lesen(pfad)
    if kopf["kopf_fehlt"]:
        _fehlend.append(name)
        if anlagedatum(pfad) >= STICHTAG:
            _hart.append(name)
    else:
        _mit_kopf += 1
messwert("dateien_mit_kopf", _mit_kopf, "Dateien")
messwert("dateien_ohne_kopf", len(_fehlend), "Dateien")
print("  ... %d von %d Pruefdateien tragen einen Kopf" % (_mit_kopf, len(DATEIEN)))
if _fehlend:
    befund("%d Pruefdateien ohne Kopf (soll fallen; Pakete zu 20 mit tools/kopf_vorschlag.py)"
           % len(_fehlend), ", ".join(_fehlend[:12]) + (" ..." if len(_fehlend) > 12 else ""))
check("HART: keine NACH dem Stichtag angelegte Pruefdatei ohne Kopf", not _hart, str(_hart))
check("mindestens eine Datei traegt einen Kopf (das Format wird benutzt)",
      _mit_kopf >= 1, str(_mit_kopf))

# ==========================================================================
abschnitt("3. Gegenprobe: eine neue Datei ohne Kopf ist ein Fehler")
# ==========================================================================
with tempfile.TemporaryDirectory() as ordner:
    neu = os.path.join(ordner, "test_neu_ohne_kopf.py")
    with open(neu, "w", encoding="ascii") as fh:
        fh.write("print('hallo')\n")
    check("die Probedatei gilt als neu (Dateidatum nach dem Stichtag)",
          anlagedatum(neu) >= STICHTAG, str(anlagedatum(neu)))
    check("die Probedatei ohne Kopf wuerde als HART gemeldet",
          kopf_lesen(neu)["kopf_fehlt"] and anlagedatum(neu) >= STICHTAG, "")
    mit = os.path.join(ordner, "test_neu_mit_kopf.py")
    with open(mit, "w", encoding="ascii") as fh:
        fh.write('PRUEF_ART = "rechnen"\nPRUEF_STUFE = 1\nPRUEF_BETRIFFT = []\n'
                 'PRUEF_DATEN = []\nprint("hallo")\n')
    check("dieselbe Datei MIT Kopf ist nicht mehr auffaellig",
          kopf_lesen(mit)["kopf_fehlt"] is False, "")

# ==========================================================================
abschnitt("4. Der Vorschlag kommt aus den Daten (Paket 15b), nicht aus dem Gefuehl")
# ==========================================================================
_paket = K.paket_lesen()
check("Paket 15b hat 230 Zeilen", len(_paket) == 230, str(len(_paket)))
_probe = {"datei": "test_produktionskette_ohne_cheats", "art": "rechnen", "dauer_s": "301.2"}
check("die langste Datei bekommt T4 (Stufe 4)", K.stufe_fuer(_probe) == 4,
      str(K.stufe_fuer(_probe)))
check("rechnen unter 2 s ergibt Stufe 1",
      K.stufe_fuer({"datei": "test_a", "art": "rechnen", "dauer_s": "0.6"}) == 1,
      str(K.stufe_fuer({"datei": "test_a", "art": "rechnen", "dauer_s": "0.6"})))
check("rechnen ab 2 s ergibt Stufe 2",
      K.stufe_fuer({"datei": "test_b", "art": "quelltext", "dauer_s": "3.5"}) == 2,
      str(K.stufe_fuer({"datei": "test_b", "art": "quelltext", "dauer_s": "3.5"})))
check("fenster bis 20 s ergibt Stufe 2",
      K.stufe_fuer({"datei": "test_c", "art": "fenster", "dauer_s": "12.0"}) == 2,
      str(K.stufe_fuer({"datei": "test_c", "art": "fenster", "dauer_s": "12.0"})))
check("fenster ueber 20 s ergibt Stufe 3",
      K.stufe_fuer({"datei": "test_d", "art": "fenster", "dauer_s": "41.4"}) == 3,
      str(K.stufe_fuer({"datei": "test_d", "art": "fenster", "dauer_s": "41.4"})))
check("'main' in BETRIFFT wird zu 'main:*' (ehrliche Uebergangsform)",
      K.betrifft_fuer({"src_module": "main gelaende"}) == ["gelaende", "main:*"],
      str(K.betrifft_fuer({"src_module": "main gelaende"})))
_stufen = {}
for zeile in _paket:
    stufe = K.stufe_fuer(zeile)
    _stufen[stufe] = _stufen.get(stufe, 0) + 1
print("  ... Startstufen ueber 230 Dateien: %s" % _stufen)
check("es gibt Dateien in jeder Stufe 1 bis 4",
      all(_stufen.get(s, 0) > 0 for s in (1, 2, 3, 4)), str(_stufen))
check("Stufe 4 hat genau die neun T4-Dateien (F-79: e2e_wege dazu)", _stufen.get(4) == 9,
      str(_stufen.get(4)))
messwert("stufe_1", _stufen.get(1, 0), "Dateien")
messwert("stufe_2", _stufen.get(2, 0), "Dateien")
messwert("stufe_3", _stufen.get(3, 0), "Dateien")
messwert("stufe_4", _stufen.get(4, 0), "Dateien")

# ==========================================================================
abschnitt("5. Schreiben: der Kopf landet nach dem Docstring, Zeilenenden bleiben")
# ==========================================================================
with tempfile.TemporaryDirectory() as ordner:
    pfad = os.path.join(ordner, "test_schreiben.py")
    with open(pfad, "wb") as fh:
        fh.write(b'# -*- coding: ascii -*-\r\n"""Docstring.\r\n\r\nMehr Text.\r\n"""\r\n'
                 b'import sys\r\nprint("x")\r\n')
    zeile = {"datei": "test_schreiben", "art": "rechnen", "dauer_s": "0.5",
             "src_module": "main spieloekonomie", "daten": "items.json"}
    K.kopf_schreiben(pfad, zeile)
    with open(pfad, "rb") as fh:
        inhalt = fh.read()
    _kopf = kopf_lesen(pfad)
    check("nach dem Schreiben ist ein Kopf da", _kopf["kopf_fehlt"] is False, "")
    check("Stufe 1 ist eingetragen (rechnen, 0,5 s)", _kopf["stufe"] == 1, str(_kopf["stufe"]))
    check("BETRIFFT traegt main:* und spieloekonomie",
          _kopf["betrifft"] == ["main:*", "spieloekonomie"], str(_kopf["betrifft"]))
    check("DATEN traegt items.json", _kopf["daten"] == ["items.json"], str(_kopf["daten"]))
    check("die Datei bleibt CRLF (Zeilenenden unveraendert)", b"\r\n" in inhalt and
          inhalt.count(b"\n") == inhalt.count(b"\r\n"), "")
    check("der Kopf steht NACH dem Docstring, nicht davor",
          inhalt.index(b"PRUEF_ART") > inhalt.index(b"Mehr Text"), "")
    _text = inhalt.decode("ascii")                     # ASCII-Pflicht: kein Umlaut im Kopf
    check("der Kopf ist reines ASCII", isinstance(_text, str), "")

bericht()
