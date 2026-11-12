# -*- coding: ascii -*-
"""Start mit Pillow: das Projekt-venv hat Vorrang vor der python-Kette - Register 129.

BEFUND 02.11.2026, 09:10: `START_SPIEL_WINDOWS.bat` startete mit Astral CPython 3.11.16, und dieser
Interpreter hat KEIN Pillow. Damit fehlten Ressourcenleiste, Kartenmotive in voller Qualitaet,
Menue-Icons und Gebaeude-Hintergruende. Daniels Entscheidung 02.11.2026: ein Projekt-venv mit
Pillow anlegen und das Start-Batch darauf umstellen; die alte Kette bleibt als Rueckfall.

Was diese Datei beweist
-----------------------
1. Das Batch versucht ZUERST das Projekt-venv (`.venv\\Scripts\\python.exe`) - nicht erst danach.
2. Die alte Kette (`py -V:Astral...`, `py -3`, `python`) steht vollstaendig weiter im Batch.
3. Liegt das venv im Projekt, kann es tkinter und Pillow wirklich importieren.
4. `.venv` ist in `.gitignore` - es wandert nicht ins Repo und nicht in ein Paket.

Aufruf:  python -X utf8 tests/test_start_mit_pillow.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "fenster"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = []
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
ROOT = str(ROOT)                                   # import_src() liefert STRINGS

START = os.path.join(ROOT, "START_SPIEL_WINDOWS.bat")
VENV_PY = os.path.join(ROOT, ".venv", "Scripts", "python.exe")

# ==========================================================================
abschnitt("1. Das Batch nimmt das venv zuerst - und laesst die alte Kette stehen")
# ==========================================================================

bat = open(START, encoding="utf-8").read()
bat_klein = bat.lower()
check("1 das Batch nennt das Projekt-venv", ".venv\\scripts\\python.exe" in bat_klein,
      "venv-Verweis im Batch")
stelle_venv = bat_klein.find('.venv\\scripts\\python.exe')
stelle_py = bat_klein.find('py -v:astral')
check("1 das venv steht VOR der python-Kette", 0 <= stelle_venv < stelle_py,
      "venv bei %d, py-Kette bei %d" % (stelle_venv, stelle_py))
check("1 die alte Kette ist als Rueckfall noch da (py -V:Astral, py -3, python)",
      "py -v:astral" in bat_klein and "py -3" in bat_klein and "python -c \"import tkinter\"" in bat_klein,
      "drei Stufen im Rueckfall")
check("1 die Marke fuer den venv-Start existiert", ":start_venv" in bat.lower(),
      "Marke im Batch")
check("1 das Batch prueft tkinter UND Pillow, bevor es dem venv traut",
      "import tkinter, pil" in bat_klein, "tkinter, PIL")
check("1 das Batch arbeitet mit eigenen Pfaden (portabel)",
      "%~dp0" in bat and "D:\\Arbeiten\\Nebelseetal_Remake" not in bat, "nur %~dp0")

# ==========================================================================
abschnitt("2. Das venv im Projekt kann wirklich tkinter und Pillow")
# ==========================================================================

if os.path.exists(VENV_PY):
    lauf = subprocess.run([VENV_PY, "-c", "import tkinter, PIL; print(PIL.__version__)"],
                          capture_output=True, text=True)
    check("2 das venv importiert tkinter und Pillow", lauf.returncode == 0,
          (lauf.stderr or lauf.stdout or "").strip()[:160])
    check("2 die Pillow-Fassung wird genannt", bool(lauf.stdout.strip()), lauf.stdout.strip())
else:
    befund("2 kein Projekt-venv vorhanden",
           "Start faellt auf die alte Kette zurueck - dort fehlt Pillow (nur Tk-Rueckfall)")

# ==========================================================================
abschnitt("3. Das venv bleibt aussen vor (git und Paket)")
# ==========================================================================

ignor = open(os.path.join(ROOT, ".gitignore"), encoding="utf-8").read()
check("3 .venv ist in .gitignore eingetragen", ".venv/" in ignor or ".venv" in ignor,
      ".venv in .gitignore")
git = subprocess.run(["git", "-C", ROOT, "check-ignore", "-q", ".venv"], capture_output=True)
check("3 git ignoriert .venv wirklich", git.returncode == 0, "git check-ignore Rueckgabe %d" % git.returncode)

# ==========================================================================
sys.exit(bericht())
