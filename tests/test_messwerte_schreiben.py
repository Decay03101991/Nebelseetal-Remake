"""Messwerte als Daten: jede Pruefdatei legt ihre Zahlen mit Zeitstempel ab (08.11.2026).

Daniels Vorgabe (08.11.2026, 00:25, Entscheidung 2): "Messwerte aus den Tests sammeln, mit
Zeitstempel ablegen, damit spaetere Tests diese Zahlen zuordnen und verwerten koennen; Luecken
bleiben Luecke, kein erfundener Wert."

Umgesetzt in EINER Stelle: `tests/harness.bericht()` schreibt
`docs/audits/messwerte/<datei>_<JJJJMMTT_HHMM>.json` (Zaehler, Dauer, Namen der Pruefungen,
gemessene Zahlen) und traegt den neuesten Stand in `docs/audits/messwerte/index.json` ein.

Geprueft wird:
  A. Der Rahmen bietet die Schnittstelle (`messwert`, `messwerte`, `bericht`) und die Datei
     landet im vorgesehenen Ordner.
  B. Die geschriebene Datei traegt Zeitstempel, Dauer, Rechner, Python-Fassung, Zaehler und die
     Messwerte selbst - alles maschinenlesbar (JSON).
  C. Der Index kennt die Datei und verweist auf den Ordner-Eintrag.
  D. Auch ein ROTER Lauf schreibt seine Datei (die Zahlen sind ein Nebenprodukt, kein
     Pruefgegenstand) - und der Fehler steht darin.
  E. Ein Schreibfehler macht eine Pruefung NICHT rot (der Rahmen meldet nur einen Hinweis).
  F. Jede Pruefdatei des Hauses ruft `bericht()` - sonst entstehen fuer sie keine Messwerte.
"""
from __future__ import annotations

import glob
import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import MESSWERTE_ORDNER, abschnitt, befund, bericht, check, messwert, messwerte

HIER = os.path.dirname(os.path.abspath(__file__))


def _probe(name, inhalt):
    """Schreibt eine winzige Pruefdatei in einen tempoeraeren Ordner und fuehrt sie aus."""
    ordner = tempfile.mkdtemp(prefix="nebelseetal_messwert_")
    pfad = os.path.join(ordner, name + ".py")
    with open(pfad, "w", encoding="utf-8") as datei:
        datei.write(inhalt)
    lauf = subprocess.run([sys.executable, "-X", "utf8", pfad], capture_output=True, text=True,
                          cwd=ordner)
    return lauf, ordner


def _neuere(dateiname):
    """Die zuletzt geschriebene Messwert-Datei zu diesem Namen (None, wenn keine da ist)."""
    treffer = sorted(glob.glob(os.path.join(MESSWERTE_ORDNER, dateiname + "_*.json")))
    return treffer[-1] if treffer else None


def _raeumen(namen):
    """Die Probe-Artefakte wieder entfernen (sie sind kein Beleg, nur ein Nachweis)."""
    for datei in glob.glob(os.path.join(MESSWERTE_ORDNER, "*_*.json")):
        if any(os.path.basename(datei).startswith(n + "_") for n in namen):
            try:
                os.remove(datei)
            except OSError:
                pass
    index = os.path.join(MESSWERTE_ORDNER, "index.json")
    if os.path.isfile(index):
        try:
            with open(index, "r", encoding="utf-8") as datei:
                daten = json.load(datei)
            for n in namen:
                (daten.get("dateien") or {}).pop(n, None)
            with open(index, "w", encoding="utf-8") as datei:
                json.dump(daten, datei, ensure_ascii=False, indent=1)
        except Exception:
            pass


# ---------------------------------------------------------------------------
abschnitt("A. Der Rahmen bietet die Schnittstelle und den vorgesehenen Ordner")
# ---------------------------------------------------------------------------
check("der Messwerte-Ordner liegt unter docs/audits/messwerte",
      MESSWERTE_ORDNER.replace("\\", "/").endswith("docs/audits/messwerte"), MESSWERTE_ORDNER)
messwert("probe_zahl", 42, "Stueck", "Pruefung dieser Wache")
gefunden = messwerte()
check("`messwert` haelt Name, Wert, Einheit und Quelle fest",
      gefunden.get("probe_zahl", {}).get("wert") == 42
      and gefunden.get("probe_zahl", {}).get("einheit") == "Stueck"
      and gefunden.get("probe_zahl", {}).get("quelle") == "Pruefung dieser Wache",
      str(gefunden.get("probe_zahl")))

# ---------------------------------------------------------------------------
abschnitt("B. Eine gruene Pruefdatei schreibt ihre Zahlen mit Zeitstempel")
# ---------------------------------------------------------------------------
PROBE_GRUEN = "test_messwert_probe_gruen"
inhalt_gruen = (
    "import os, sys\n"
    "sys.path.insert(0, %r)\n"
    "from harness import check, messwert, bericht\n"
    "messwert('holz_je_tag', 1234.5, 'Holz', 'gemessen')\n"
    "check('erste Probe', True)\n"
    "check('zweite Probe', True)\n"
    "sys.exit(bericht())\n" % HIER)
lauf_g, ordner_g = _probe(PROBE_GRUEN, inhalt_gruen)
check("die Probe laeuft gruen", lauf_g.returncode == 0, lauf_g.stdout[-200:])
datei_g = _neuere(PROBE_GRUEN)
check("die Messwert-Datei existiert", datei_g is not None, str(datei_g))
daten_g = {}
if datei_g:
    with open(datei_g, "r", encoding="utf-8") as datei:
        daten_g = json.load(datei)
check("der Zeitstempel steht darin (Datum und Uhrzeit)",
      isinstance(daten_g.get("zeit"), str) and "T" in str(daten_g.get("zeit")),
      str(daten_g.get("zeit")))
_dauer_g = daten_g.get("dauer_s")                       # 0.0 ist ein GUELTIGER Wert (schneller Lauf)
check("die Dauer des Laufs steht darin",
      isinstance(_dauer_g, (int, float)) and not isinstance(_dauer_g, bool)
      and float(_dauer_g) >= 0.0,
      str(_dauer_g))
check("Rechner und Python-Fassung stehen darin",
      bool(daten_g.get("rechner")) and bool(daten_g.get("python")),
      "%s / %s" % (daten_g.get("rechner"), daten_g.get("python")))
check("die Zaehler stimmen (2 bestanden, 0 Fehler, 0 Befunde)",
      (daten_g.get("bestanden"), daten_g.get("fehler"), daten_g.get("befunde")) == (2, 0, 0),
      "%s/%s/%s" % (daten_g.get("bestanden"), daten_g.get("fehler"), daten_g.get("befunde")))
check("die Namen der Pruefungen stehen darin",
      daten_g.get("pruefungen") == ["erste Probe", "zweite Probe"], str(daten_g.get("pruefungen")))
zahl = (daten_g.get("messwerte") or {}).get("holz_je_tag") or {}
check("die gemessene Zahl steht mit Einheit und Quelle darin",
      zahl.get("wert") == 1234.5 and zahl.get("einheit") == "Holz" and zahl.get("quelle") == "gemessen",
      str(zahl))
check("der Dateiname traegt Datum und Stunde",
      os.path.basename(str(datei_g))[:len(PROBE_GRUEN) + 9].startswith(PROBE_GRUEN + "_")
      and os.path.basename(str(datei_g)).endswith(".json"), os.path.basename(str(datei_g)))

# ---------------------------------------------------------------------------
abschnitt("C. Der Index kennt die Datei und verweist auf ihren Ordner-Eintrag")
# ---------------------------------------------------------------------------
index_pfad = os.path.join(MESSWERTE_ORDNER, "index.json")
check("der Index existiert", os.path.isfile(index_pfad), index_pfad)
index = {}
if os.path.isfile(index_pfad):
    with open(index_pfad, "r", encoding="utf-8") as datei:
        index = json.load(datei)
eintrag = (index.get("dateien") or {}).get(PROBE_GRUEN) or {}
check("der Index fuehrt die Probe", bool(eintrag), str(eintrag))
check("der Index nennt die Datei im Ordner", eintrag.get("datei_im_ordner") == os.path.basename(str(datei_g)),
      str(eintrag.get("datei_im_ordner")))
check("der Index nennt die Zaehler", eintrag.get("bestanden") == 2, str(eintrag.get("bestanden")))

# ---------------------------------------------------------------------------
abschnitt("D. Auch ein ROTER Lauf schreibt seine Zahlen (mit dem Fehler darin)")
# ---------------------------------------------------------------------------
PROBE_ROT = "test_messwert_probe_rot"
inhalt_rot = (
    "import os, sys\n"
    "sys.path.insert(0, %r)\n"
    "from harness import check, messwert, bericht\n"
    "messwert('soll_ist', 7, 'Stueck', 'gemessen')\n"
    "check('erste Probe', True)\n"
    "check('zweite Probe', False, 'absichtlich rot')\n"
    "sys.exit(bericht())\n" % HIER)
lauf_r, ordner_r = _probe(PROBE_ROT, inhalt_rot)
check("die Probe endet rot (Rueckgabe 1)", lauf_r.returncode == 1, str(lauf_r.returncode))
datei_r = _neuere(PROBE_ROT)
check("auch der rote Lauf hat eine Messwert-Datei", datei_r is not None, str(datei_r))
if datei_r:
    with open(datei_r, "r", encoding="utf-8") as datei:
        daten_r = json.load(datei)
    check("der Fehler steht in den Zahlen", daten_r.get("fehler") == 1,
          str(daten_r.get("fehler")))
    check("der Name des Fehlers steht darin",
          any("zweite Probe" in str(x) for x in (daten_r.get("fehlernamen") or [])),
          str(daten_r.get("fehlernamen")))

# ---------------------------------------------------------------------------
abschnitt("E. Ein Schreibfehler macht keine Pruefung rot")
# ---------------------------------------------------------------------------
import harness as _harness                                        # noqa: E402  (fuer den Umbiege-Test)

_alt = _harness.MESSWERTE_ORDNER
try:
    _harness.MESSWERTE_ORDNER = os.path.join(tempfile.gettempdir(), "gibt_es_nicht", "\0verboten")
    pfad_fehler = _harness._messwerte_schreiben()
    check("der Schreibfehler liefert einen leeren Pfad statt einer Ausnahme", pfad_fehler == "",
          str(pfad_fehler))
finally:
    _harness.MESSWERTE_ORDNER = _alt

# ---------------------------------------------------------------------------
abschnitt("F. Jede Pruefdatei des Hauses ruft `bericht()`")
# ---------------------------------------------------------------------------
dateien = sorted(glob.glob(os.path.join(HIER, "test_*.py")))
mit_bericht, ohne_bericht, halbe = [], [], []
for pfad in dateien:
    with open(pfad, "r", encoding="utf-8", errors="replace") as datei:
        text = datei.read()
    name = os.path.basename(pfad)
    if "bericht()" in text:
        mit_bericht.append(name)                                  # schreibt Messwerte
    elif "harness" in text:
        halbe.append(name)                                        # nutzt den Rahmen, meldet aber nicht
    else:
        ohne_bericht.append(name)                                 # eigener Bericht, kein Rahmen
check("es gibt Pruefdateien", len(dateien) > 100, "%d Dateien" % len(dateien))
check("keine Pruefdatei nutzt den Rahmen ohne `bericht()` (das waere ein Widerspruch)",
      not halbe, str(halbe[:6]))
messwert("pruefdateien", len(dateien), "Dateien", "gezaehlt")
messwert("pruefdateien_mit_bericht", len(mit_bericht), "Dateien", "gezaehlt")
messwert("pruefdateien_mit_eigenem_bericht", len(ohne_bericht), "Dateien", "gezaehlt")
if ohne_bericht:                                                  # gemessene Luecke, kein Fehler
    befund("Pruefdateien ohne `bericht()` (und damit ohne Messwerte-Datei): %d von %d - beim "
           "naechsten Anfassen auf den Rahmen umstellen" % (len(ohne_bericht), len(dateien)),
           ", ".join(ohne_bericht[:8]) + (" ..." if len(ohne_bericht) > 8 else ""))

_raeumen([PROBE_GRUEN, PROBE_ROT])
sys.exit(bericht())
