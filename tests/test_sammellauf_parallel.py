# -*- coding: ascii -*-
"""Wache fuer den Parallelbetrieb des Sammellaufs (Schritt 12, Daniel 08.11.2026).

Was hier zugesichert wird:
  1. Die Startreihenfolge stellt die laengsten Pruefdateien nach vorn (Dauern aus der
     Messwerte-Ablage), Unbekannte laufen zuletzt, und das Ergebnis ist deterministisch.
  2. Jede Pruefdatei bekommt einen EIGENEN Spielordner - der Grund, warum parallele Laeufe
     einander nicht mehr den Spielstand wegraeumen.
  3. `fahre()` setzt `NEBEL_SPIELDATEN_ORDNER` wirklich im Kindprozess (nicht nur im Kopf).
  4. Die Index-Sperre haelt: acht gleichzeitige Schreiber verlieren keinen Eintrag.
     Ohne Sperre ist der Index ein read-modify-write und der letzte Schreiber loescht die
     Eintraege der anderen - gemessen beim Bau dieser Wache.
  5. Die Auswertung einer Zeile (`deute`) bleibt unveraendert: gruen nur bei RC 0 UND 0 Fehlern.
"""

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = []
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------
import json
import os
import shutil
import sys
import tempfile
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
sys.path.insert(0, os.path.join(ROOT, "tools"))
import sammellauf  # noqa: E402
import harness  # noqa: E402

PROBE = '''import os, sys
ordner = os.environ.get("NEBEL_SPIELDATEN_ORDNER", "")
if not ordner:
    print("kein NEBEL_SPIELDATEN_ORDNER")
    sys.exit(3)
with open(os.path.join(ordner, "probe.txt"), "w", encoding="ascii") as f:
    f.write("geschrieben")
print("ERGEBNIS: 1 bestanden, 0 Fehler, 0 Befunde")
sys.exit(0)
'''


def _tmp(prefix):
    ordner = tempfile.mkdtemp(prefix=prefix)
    return ordner


# ---------------------------------------------------------------- 1. Startreihenfolge
abschnitt("1. Die laengsten Dateien laufen zuerst")

schaetzung = {"test_langsam.py": 210.0, "test_mittel.py": 35.0, "test_kurz.py": 1.3}
ordnung = sammellauf.startreihenfolge(
    ["test_kurz.py", "test_unbekannt.py", "test_langsam.py", "test_mittel.py"], schaetzung)
check("die laengste Datei steht vorn", ordnung[0] == "test_langsam.py", str(ordnung))
check("danach die naechstlaengste", ordnung[1] == "test_mittel.py", str(ordnung))
check("unbekannte Dateien laufen zuletzt", ordnung[-1] == "test_unbekannt.py", str(ordnung))
check("dieselbe Eingabe ergibt dieselbe Reihenfolge",
      sammellauf.startreihenfolge(
          ["test_kurz.py", "test_unbekannt.py", "test_langsam.py", "test_mittel.py"],
          schaetzung) == ordnung)
check("Gleichstand wird alphabetisch entschieden",
      sammellauf.startreihenfolge(["b.py", "a.py"], {}) == ["a.py", "b.py"])

# ---------------------------------------------------------------- 2. Dauern aus dem Index
abschnitt("2. Die Dauern kommen aus der Messwerte-Ablage, nicht aus einer Liste im Code")

ordner_ix = _tmp("nebel_ix_")
pfad_ix = os.path.join(ordner_ix, "index.json")
with open(pfad_ix, "w", encoding="utf-8") as datei:
    json.dump({"dateien": {"test_a": {"dauer_s": 12.5}, "test_b": {"dauer_s": "7.5"},
                           "test_kaputt": {"dauer_s": None}}}, datei)
gemessen = sammellauf.dauer_schaetzung(pfad_ix)
check("bekannte Dauer wird gelesen", gemessen.get("test_a.py") == 12.5, str(gemessen))
check("Dauer als Text wird in eine Zahl gebracht", gemessen.get("test_b.py") == 7.5, str(gemessen))
check("fehlender Wert wird zu 0.0 statt zum Absturz",
      gemessen.get("test_kaputt.py") == 0.0, str(gemessen.get("test_kaputt")))
check("ein fehlender Index ergibt eine leere Schaetzung",
      sammellauf.dauer_schaetzung(os.path.join(ordner_ix, "gibtesnicht.json")) == {})
shutil.rmtree(ordner_ix, ignore_errors=True)

# ---------------------------------------------------------------- 3. Eigener Spielordner
abschnitt("3. Jede Pruefdatei bekommt ihren eigenen Spielordner")

wurzel = _tmp("nebel_spiel_")
oa = sammellauf.spielordner_fuer(wurzel, "test_alpha.py")
ob = sammellauf.spielordner_fuer(wurzel, "test_beta.py")
check("zwei Dateien bekommen zwei verschiedene Ordner", oa != ob, oa + " / " + ob)
check("beide Ordner existieren", os.path.isdir(oa) and os.path.isdir(ob))
check("der Ordnername traegt den Dateinamen (Diagnose)", oa.endswith("test_alpha"), oa)
check("derselbe Name ergibt denselben Ordner",
      sammellauf.spielordner_fuer(wurzel, "test_alpha.py") == oa)
shutil.rmtree(wurzel, ignore_errors=True)

# ---------------------------------------------------------------- 4. fahre() setzt die Variable
abschnitt("4. fahre() setzt NEBEL_SPIELDATEN_ORDNER im Kindprozess")

probe_dir = _tmp("nebel_probe_")
probe_pfad = os.path.join(probe_dir, "test_probe.py")
with open(probe_pfad, "w", encoding="ascii") as datei:
    datei.write(PROBE)
spiel = _tmp("nebel_probe_spiel_")
alt_tests = sammellauf.TESTS
sammellauf.TESTS = probe_dir                      # nur fuer diesen Aufruf umbiegen
try:
    ergebnis = sammellauf.fahre("test_probe.py", spiel)
finally:
    sammellauf.TESTS = alt_tests
check("die Probe laeuft gruen durch", ergebnis["gruen"] is True, ergebnis["kurz"])
check("die Auswertung liest 1 bestandene Pruefung", ergebnis["bestanden"] == 1,
      str(ergebnis["bestanden"]))
check("die Probe hat in den EIGENEN Ordner geschrieben",
      os.path.isfile(os.path.join(spiel, "probe.txt")))
check("im Projektordner ist dabei nichts entstanden",
      not os.path.isfile(os.path.join(ROOT, "src", "savegame.json")))
check("die Dauer wird gemessen", ergebnis["dauer"] > 0)
shutil.rmtree(probe_dir, ignore_errors=True)
shutil.rmtree(spiel, ignore_errors=True)

# ---------------------------------------------------------------- 5. Auswertung unveraendert
abschnitt("5. Die Auswertung einer Zeile bleibt streng")

check("RC 0 mit 0 Fehlern ist gruen",
      sammellauf.deute("ERGEBNIS: 5 bestanden, 0 Fehler, 1 Befunde", 0)[0] is True)
check("RC 0 mit einem Fehler ist ROT",
      sammellauf.deute("ERGEBNIS: 5 bestanden, 1 Fehler, 0 Befunde", 0)[0] is False)
check("RC 1 mit 0 Fehlern ist ROT",
      sammellauf.deute("ERGEBNIS: 5 bestanden, 0 Fehler, 0 Befunde", 1)[0] is False)
check("eine Ausgabe ohne ERGEBNIS-Zeile zaehlt nach dem Rueckgabewert",
      sammellauf.deute("irgendwas", 0)[4].startswith("ohne ERGEBNIS-Zeile"))
check("die letzte ERGEBNIS-Zeile gilt",
      sammellauf.deute("ERGEBNIS: 1 bestanden, 1 Fehler, 0 Befunde\n"
                       "ERGEBNIS: 9 bestanden, 0 Fehler, 0 Befunde", 0)[0] is True)
# Zwei Pruefdateien (test_projektpfade, test_textqualitaet) schreiben kein Befunde-Feld.
# Ohne Toleranz wertete der Sammellauf sie als "ohne ERGEBNIS-Zeile" und zaehlte ihre 573
# bestandenen Pruefungen nicht mit - gruen war dann nur der Rueckgabewert.
_ohne = sammellauf.deute("ERGEBNIS: 129 bestanden, 0 Fehler (63 Quelldateien)", 0)
check("eine Zeile ohne Befunde-Feld wird ausgewertet", _ohne[0] is True and _ohne[1] == 129,
      str(_ohne))
check("und ein Fehler darin ist trotzdem ROT",
      sammellauf.deute("ERGEBNIS: 444 bestanden, 3 Fehler (134 Dokumente)", 0)[0] is False)

# ---------------------------------------------------------------- 6. Index-Sperre haelt
abschnitt("6. Acht gleichzeitige Schreiber verlieren keinen Index-Eintrag")

spiegel = _tmp("nebel_index_")
alt_ordner = harness.MESSWERTE_ORDNER
harness.MESSWERTE_ORDNER = spiegel
try:
    def schreibe(nr):
        harness._index_fortschreiben(
            "test_nr%d_00000000_0000.json" % nr,
            {"datei": "test_nr%d" % nr, "zeit": "2026-11-08T12:00:00", "bestanden": nr,
             "fehler": 0, "befunde": 0, "dauer_s": 1.0})

    faeden = [threading.Thread(target=schreibe, args=(nr,)) for nr in range(8)]
    for f in faeden:
        f.start()
    for f in faeden:
        f.join()
    with open(os.path.join(spiegel, "index.json"), encoding="utf-8") as datei:
        stand = json.load(datei)
    eintraege = stand.get("dateien") or {}
    check("alle acht Eintraege stehen im Index", len(eintraege) == 8, str(sorted(eintraege)))
    check("kein Eintrag wurde von einem anderen ueberschrieben",
          all(eintraege.get("test_nr%d" % nr, {}).get("bestanden") == nr for nr in range(8)),
          str(eintraege))
    check("die Sperrdatei ist danach wieder weg",
          not os.path.exists(os.path.join(spiegel, "index.sperre")))
    befund("Ohne Sperre verliert der Index Eintraege: das Schreiben ist ein read-modify-write "
           "(Index lesen, ergaenzen, atomar ersetzen). Die Sperre ist eine eigene Datei mit "
           "O_EXCL; eine liegengebliebene Sperre wird nach 15 s uebernommen.")
finally:
    harness.MESSWERTE_ORDNER = alt_ordner
    shutil.rmtree(spiegel, ignore_errors=True)

sys.exit(bericht())
