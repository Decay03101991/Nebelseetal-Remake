# -*- coding: ascii -*-
"""F-63: die Pruefstufen T1 bis T4 sind der Standard (Daniel 12.11.2026).

Entscheidung: die haeufige Stufe bleibt **unter 120 s**, der volle Lauf (T4) ist die Ausnahme -
**vor jeder EXE HART**. Die Stufe steht im Kopf jeder Pruefdatei (M1, `PRUEF_STUFE`).

Was diese Datei beweist
-----------------------
1. `dateien_fuer_stufe` nimmt genau die Dateien BIS zur Stufe: T1 nur Stufe 1, T2 zusaetzlich 2,
   T3 zusaetzlich 3, T4 ALLE. Jede Stufe ist eine Obermenge der vorigen.
2. Ohne Kopf gilt Stufe 3 (Ersatzwert aus M1) - eine neue Datei ohne Kopf laeuft also ab T3 mit.
3. Der Sammellauf nimmt `--stufe N`; ohne Angabe laeuft T4 (der volle Lauf).
4. ECHTER LAUF: `--stufe 1` mit einer Stufe-1-Datei und einer T4-Datei in der Auswahl laesst die
   T4-Datei weg (sie wuerde 301 s kosten) und sagt es.

Aufruf:  python -X utf8 tests/test_stufen_f63.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = []
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src, messwert

ROOT, SRC = import_src()
sys.path.insert(0, os.path.join(ROOT, "tools"))
import sammellauf as S  # noqa: E402

TESTS = os.path.join(ROOT, "tests")
ALLE = sorted(n for n in os.listdir(TESTS) if n.startswith("test_") and n.endswith(".py"))

# ==========================================================================
abschnitt("1. Die Stufen sind geschachtelt: T1 c T2 c T3 c T4 = alle")
# ==========================================================================
_t1 = S.dateien_fuer_stufe(ALLE, 1)
_t2 = S.dateien_fuer_stufe(ALLE, 2)
_t3 = S.dateien_fuer_stufe(ALLE, 3)
_t4 = S.dateien_fuer_stufe(ALLE, 4)
check("T1 ist eine Teilmenge von T2", set(_t1) <= set(_t2), str(len(set(_t1) - set(_t2))))
check("T2 ist eine Teilmenge von T3", set(_t2) <= set(_t3), str(len(set(_t2) - set(_t3))))
check("T3 ist eine Teilmenge von T4", set(_t3) <= set(_t4), str(len(set(_t3) - set(_t4))))
check("T4 ist ALLE Dateien", set(_t4) == set(ALLE), str(len(set(_t4) ^ set(ALLE))))
check("T1 ist echt kleiner als T4", len(_t1) < len(_t4), "%d gegen %d" % (len(_t1), len(_t4)))
check("jede Datei in T1 traegt wirklich Stufe 1",
      all(S.kopf_stufe(os.path.join(TESTS, n)) == 1 for n in _t1), "")
messwert("dateien_t1", len(_t1), "Dateien")
messwert("dateien_t2", len(_t2), "Dateien")
messwert("dateien_t3", len(_t3), "Dateien")
messwert("dateien_t4", len(_t4), "Dateien")
print("  ... T1 %d / T2 %d / T3 %d / T4 %d" % (len(_t1), len(_t2), len(_t3), len(_t4)))
check("die Stufe 3 enthaelt die T4-Dateien NICHT (die laufen nur in T4)",
      not (set(_t3) & set(S.T4 if hasattr(S, "T4") else [])), "")

# ==========================================================================
abschnitt("2. Ohne Kopf gilt Stufe 3")
# ==========================================================================
with tempfile.TemporaryDirectory() as ordner:
    ohne = os.path.join(ordner, "test_ohne_kopf.py")
    with open(ohne, "w", encoding="ascii") as fh:
        fh.write("print('x')\n")
    mit = os.path.join(ordner, "test_mit_kopf.py")
    with open(mit, "w", encoding="ascii") as fh:
        fh.write('PRUEF_STUFE = 1\nprint("x")\n')
    _nur_t1 = S.dateien_fuer_stufe(["test_ohne_kopf.py", "test_mit_kopf.py"], 1, ordner)
    check("ohne Kopf ist die Datei in T1 NICHT dabei", _nur_t1 == ["test_mit_kopf.py"], str(_nur_t1))
    _bis_t3 = S.dateien_fuer_stufe(["test_ohne_kopf.py", "test_mit_kopf.py"], 3, ordner)
    check("ohne Kopf kommt sie ab T3 dazu", set(_bis_t3) == {"test_ohne_kopf.py", "test_mit_kopf.py"},
          str(_bis_t3))

# ==========================================================================
abschnitt("3. Der Sammellauf kennt --stufe, ohne Angabe laeuft T4")
# ==========================================================================
_quelle = open(os.path.join(ROOT, "tools", "sammellauf.py"), encoding="utf-8",
               errors="replace").read()
check("der Schalter --stufe ist eingebaut",
      '"--stufe"' in _quelle and 'a.startswith("--stufe=")' in _quelle, "")
check("ohne Angabe steht stufe = 4 (der volle Lauf)", "stufe = 4" in _quelle, "")
check("die Dateiauswahl laeuft ueber dateien_fuer_stufe", "dateien_fuer_stufe(" in _quelle, "")
check("der Lauf sagt, wenn er beschnitten ist", "Stufe T%d: %d von %d Dateien" in _quelle, "")

# ==========================================================================
abschnitt("4. Echter Lauf: --stufe 1 laesst die T4-Datei weg")
# ==========================================================================
_lauf = subprocess.run([sys.executable, "-X", "utf8", os.path.join(ROOT, "tools", "sammellauf.py"),
                        "--stufe", "1", "test_textqualitaet", "test_produktionskette_ohne_cheats"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace",
                       cwd=ROOT, timeout=300)
_aus = (_lauf.stdout or "") + (_lauf.stderr or "")
check("der Lauf meldet die Bescheidung (Stufe T1: 1 von 2)",
      "Stufe T1: 1 von 2 Dateien" in _aus, _aus.splitlines()[:2].__str__())
check("die Stufe-1-Datei ist gelaufen", "test_textqualitaet.py" in _aus, "")
check("die T4-Datei ist NICHT gelaufen", "test_produktionskette_ohne_cheats" not in _aus, "")
check("der Lauf endet mit Rueckgabewert 0", _lauf.returncode == 0, str(_lauf.returncode))

bericht()
