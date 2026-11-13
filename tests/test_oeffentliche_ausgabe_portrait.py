"""Wache: das private Portraitfoto reist NICHT in ein Paket (Daniel 13.11.2026, F-102, Register 627).

**Der Gegenstand:** In `assets/bilder/` liegen `daniel_portrait.png` und `daniel_portrait_klein.png` -
ein Foto einer echten Person, im Spiel unbenutzt. Daniels Wort: **"aus dem Paketbau ausschliessen, die
Datei aber im Projekt lassen"**.

**Was hier geprueft wird (gemessen, nicht gezaehlt):**
1. der Filter nennt genau diese beiden Dateien;
2. eine ECHTE Kopie von `assets` in einen Zwischenordner laesst sie weg - und nur sie (Dateizahl und
   Stichproben stimmen sonst);
3. beide Bauwege (`build_exe.py`, `build_public_exe.py`) benutzen diesen Filter;
4. die Dateien liegen im Projekt noch da (die Entscheidung war "im Projekt lassen", nicht "loeschen").

Der Test kopiert rund 64 MB - das dauert wenige Sekunden und raeumt hinterher auf.
"""

from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['build_exe', 'build_public_exe', 'paket_ausschluss']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import shutil
import sys
import tempfile

from harness import abschnitt, befund, bericht, check, messwert

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import paket_ausschluss as P  # noqa: E402

# ==========================================================================
abschnitt("1. Der Filter nennt, was zurueckbleibt")
# ==========================================================================
check("1 PRIVAT existiert und ist nicht leer", isinstance(P.PRIVAT, frozenset) and len(P.PRIVAT) >= 2,
      str(sorted(P.PRIVAT)))
for _name in ("daniel_portrait.png", "daniel_portrait_klein.png"):
    check("1 %s steht im Filter" % _name, _name in P.PRIVAT, str(sorted(P.PRIVAT)))

# ==========================================================================
abschnitt("2. Eine echte Kopie laesst genau diese Dateien weg")
# ==========================================================================
_quelle = os.path.join(ROOT, "assets")
_ziel = os.path.join(tempfile.mkdtemp(prefix="paketprobe_"), "assets")
_weg = P.kopiere_assets(_quelle, _ziel)
try:
    check("2 beide Portraitdateien werden gemeldet", _weg == ["bilder/daniel_portrait.png",
                                                             "bilder/daniel_portrait_klein.png"],
          str(_weg))
    check("2 die Portraitdatei liegt NICHT in der Kopie",
          not os.path.exists(os.path.join(_ziel, "bilder", "daniel_portrait.png")), "")
    check("2 die kleine Fassung liegt NICHT in der Kopie",
          not os.path.exists(os.path.join(_ziel, "bilder", "daniel_portrait_klein.png")), "")
    check("2 die uebrigen Bilder sind da (Stichprobe: ein Wappen und eine Burg)",
          os.path.exists(os.path.join(_ziel, "icons", "wappen", "wappen_04.png"))
          and os.path.exists(os.path.join(_ziel, "icons", "burgen", "burg_02.png")), "")

    def _zaehle(wurzel):
        summe = 0
        for ordner, _unter, namen in os.walk(wurzel):
            summe += len([n for n in namen if not n.startswith(".")])
        return summe

    _soll = _zaehle(_quelle) - 2
    _ist = _zaehle(_ziel)
    check("2 die Kopie hat genau zwei Dateien weniger", _ist == _soll, "%d statt %d" % (_ist, _soll))
    messwert("dateien_quelle", str(_zaehle(_quelle)), "Dateien")
    messwert("dateien_paket", str(_ist), "Dateien")
finally:
    shutil.rmtree(os.path.dirname(_ziel), ignore_errors=True)

# ==========================================================================
abschnitt("3. Beide Bauwege benutzen den Filter")
# ==========================================================================
for _datei in ("tools/build_exe.py", "tools/build_public_exe.py"):
    _text = open(os.path.join(ROOT, _datei), encoding="utf-8", errors="replace").read()
    check("3 %s zieht den Filter heran" % _datei, "kopiere_assets" in _text and "paket_ausschluss" in _text, "")
    check("3 %s gibt NICHT mehr den rohen assets-Ordner mit" % _datei,
          'ROOT/"assets")+os.pathsep+"assets"' not in _text
          and 'f"{WURZEL / quelle}{os.pathsep}{ziel}"' not in _text, "")

# ==========================================================================
abschnitt("4. Im Projekt liegen die Dateien weiter (Entscheidung F-102)")
# ==========================================================================
for _name in ("daniel_portrait.png", "daniel_portrait_klein.png"):
    _pfad = os.path.join(_quelle, "bilder", _name)
    check("4 %s ist im Projekt vorhanden" % _name, os.path.exists(_pfad),
          "%d Byte" % (os.path.getsize(_pfad) if os.path.exists(_pfad) else 0))
befund("4 ehrliche Grenze: geprueft ist der FILTER, nicht die gebaute EXE",
       "ob das Paket wirklich frei ist, zeigt erst ein Bau mit anschliessender Pruefung der EXE")

sys.exit(bericht())
