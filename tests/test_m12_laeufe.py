# -*- coding: ascii -*-
"""M12.0: der Sammellauf schreibt eine Zeile je Datei und Lauf (`docs/audits/laeufe.jsonl`).

Claudes Befund aus Paket 15b (Antwort Nr. 16, Teil B): `test_textqualitaet` hatte **0 Laeufe** in
der Messwerte-Ablage und war im Lauf 22:18 trotzdem **rot** (470/2/0). "Keine Historie" heisst also
nicht "laeuft nie", sondern "schreibt nichts in den Index". Die 46 Dateien ohne Messwert-Eintrag
waren eine Luecke im Aufzeichnen - nicht im Pruefen.

Was diese Datei beweist
-----------------------
1. REINE FUNKTION: `zeilen_fuer_lauf` erzeugt je Datei genau eine Zeile mit allen Feldern aus
   Nr. 16 (datei, zeit, lauf, commit, stufe, rc, bestanden, fehler, befunde, dauer, parallel,
   allein, ausgesetzt); `bestanden` ist None, wenn die Datei ausgesetzt war.
2. ANHAENGEN, NICHT UEBERSCHREIBEN: zwei Laeufe ergeben zwei Zeilen je Datei; die erste bleibt.
3. STUFE: ohne Kopf gilt 3 (M1-Ersatzwert); mit `PRUEF_STUFE = 1` im Kopf gilt 1.
4. QUELLTEXT: `tools/sammellauf.py` schreibt die Zeilen nach dem Lauf, aus dem Prozessergebnis,
   und der Pfad ist `docs/audits/laeufe.jsonl`.
5. IST-STAND: liegt die Datei vor, ist JEDE Zeile gueltiges JSON mit den Pflichtfeldern (das ist
   die Ablage, aus der `tools/rot_historie.py` liest).

Aufruf:  python -X utf8 tests/test_m12_laeufe.py
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

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src, messwert

ROOT, SRC = import_src()
sys.path.insert(0, os.path.join(ROOT, "tools"))
import sammellauf as S  # noqa: E402

PFLICHT = ("datei", "zeit", "lauf", "commit", "stufe", "rc", "bestanden", "fehler", "befunde",
           "dauer", "parallel", "allein", "ausgesetzt")

# Zwei erfundene Ergebnisse: eine gruene, eine rote, eine ausgesetzte Datei.
ERFUNDEN = {
    "test_a.py": {"gruen": True, "ausgesetzt": False, "bestanden": 10, "fehler": 0, "befunde": 1,
                  "dauer": 1.2345, "rc": 0},
    "test_b.py": {"gruen": False, "ausgesetzt": False, "bestanden": 7, "fehler": 2, "befunde": 0,
                  "dauer": 0.5, "rc": 1},
    "test_c.py": {"gruen": False, "ausgesetzt": True, "bestanden": 0, "fehler": 0, "befunde": 0,
                  "dauer": 0.0, "rc": None},
}

# ==========================================================================
abschnitt("1. Eine Zeile je Datei mit allen Feldern aus Nr. 16")
# ==========================================================================
zeilen = S.zeilen_fuer_lauf(ERFUNDEN, "2026-11-13T00:10:00", "abc1234", 2)
check("drei Dateien ergeben drei Zeilen", len(zeilen) == 3, str(len(zeilen)))
check("die Zeilen stehen in Namensreihenfolge",
      [z["datei"] for z in zeilen] == ["test_a.py", "test_b.py", "test_c.py"],
      str([z["datei"] for z in zeilen]))
for z in zeilen:
    fehlend = [f for f in PFLICHT if f not in z]
    check("%s traegt alle Pflichtfelder" % z["datei"], not fehlend, str(fehlend))
_a, _b, _c = zeilen
check("gruene Datei: bestanden True, rc 0", _a["bestanden"] is True and _a["rc"] == 0,
      "%r / %r" % (_a["bestanden"], _a["rc"]))
check("rote Datei: bestanden False, 2 Fehler", _b["bestanden"] is False and _b["fehler"] == 2,
      "%r / %r" % (_b["bestanden"], _b["fehler"]))
check("ausgesetzte Datei: bestanden ist None (nicht gelaufen, nicht rot)",
      _c["bestanden"] is None and _c["ausgesetzt"] is True,
      "%r / %r" % (_c["bestanden"], _c["ausgesetzt"]))
check("die Dauer wird auf zwei Stellen gerundet", _a["dauer"] == 1.23, str(_a["dauer"]))
check("parallel 2 heisst allein = nein", _a["parallel"] == 2 and _a["allein"] == "nein",
      "%r / %r" % (_a["parallel"], _a["allein"]))
check("parallel 1 heisst allein = ja",
      S.zeilen_fuer_lauf(ERFUNDEN, "x", "y", 1)[0]["allein"] == "ja")
check("jede Zeile ist JSON-serialisierbar (eine Zeile je Datei, keine Mehrzeiler)",
      all("\n" not in json.dumps(z) for z in zeilen))

# ==========================================================================
abschnitt("2. Anhaengen statt ueberschreiben: zwei Laeufe, zwei Zeilen je Datei")
# ==========================================================================
with tempfile.TemporaryDirectory() as ordner:
    ziel = os.path.join(ordner, "laeufe.jsonl")
    S.zeilen_schreiben(zeilen, ziel)
    S.zeilen_schreiben(S.zeilen_fuer_lauf(ERFUNDEN, "2026-11-13T01:00:00", "def5678", 1), ziel)
    with open(ziel, encoding="utf-8") as fh:
        inhalt = [json.loads(z) for z in fh if z.strip()]
    check("zwei Laeufe ergeben sechs Zeilen", len(inhalt) == 6, str(len(inhalt)))
    check("die Zeilen des ersten Laufs sind noch da",
          sum(1 for z in inhalt if z["zeit"] == "2026-11-13T00:10:00") == 3,
          str([z["zeit"] for z in inhalt]))
    check("der zweite Lauf traegt seinen eigenen Commit",
          {z["commit"] for z in inhalt if z["zeit"] == "2026-11-13T01:00:00"} == {"def5678"})
    messwert("zeilen_je_datei_je_lauf", 1, "Zeilen")

# ==========================================================================
abschnitt("3. Stufe: ohne Kopf 3, mit Kopf die Zahl aus dem Kopf")
# ==========================================================================
with tempfile.TemporaryDirectory() as ordner:
    ohne = os.path.join(ordner, "test_ohne.py")
    with open(ohne, "w", encoding="ascii") as fh:
        fh.write("# -*- coding: ascii -*-\nprint('hallo')\n")
    check("ohne Kopf gilt Stufe 3", S.kopf_stufe(ohne) == 3, str(S.kopf_stufe(ohne)))
    mit = os.path.join(ordner, "test_mit.py")
    with open(mit, "w", encoding="ascii") as fh:
        fh.write("# -*- coding: ascii -*-\nPRUEF_STUFE = 1\n")
    check("mit PRUEF_STUFE = 1 gilt 1", S.kopf_stufe(mit) == 1, str(S.kopf_stufe(mit)))
    kaputt = os.path.join(ordner, "test_kaputt.py")
    with open(kaputt, "w", encoding="ascii") as fh:
        fh.write("PRUEF_STUFE = 9\n")
    check("eine unmoegliche Stufe faellt auf 3 zurueck", S.kopf_stufe(kaputt) == 3,
          str(S.kopf_stufe(kaputt)))
    check("eine fehlende Datei ergibt 3", S.kopf_stufe(os.path.join(ordner, "gibtsnicht.py")) == 3)

# ==========================================================================
abschnitt("4. Quelltext: der Sammellauf schreibt selbst, nach dem Lauf")
# ==========================================================================
_quelle = open(os.path.join(ROOT, "tools", "sammellauf.py"), encoding="utf-8",
               errors="replace").read()
check("der Pfad ist docs/audits/laeufe.jsonl",
      all(teil in _quelle for teil in ('"docs"', '"audits"', '"laeufe.jsonl"')), "")
check("die Zeilen entstehen aus dem Prozessergebnis (zeilen_fuer_lauf mit ergebnisse)",
      "zeilen_fuer_lauf(ergebnisse" in _quelle)
check("geschrieben wird mit zeilen_schreiben", "zeilen_schreiben(" in _quelle)
_haupt = _quelle[_quelle.find("def main():"):]
check("das Schreiben steht in main(), nicht im harness",
      _haupt.find("zeilen_schreiben(") > _haupt.find("pool.map"))
check("ein Schreibfehler kippt den Lauf nicht (OSError wird gefangen)",
      "except OSError as fehler" in _haupt)

# ==========================================================================
abschnitt("5. Ist-Stand der Ablage")
# ==========================================================================
ist = os.path.join(ROOT, "docs", "audits", "laeufe.jsonl")
if not os.path.exists(ist):
    befund("docs/audits/laeufe.jsonl gibt es noch nicht - der naechste Sammellauf legt sie an")
else:
    with open(ist, encoding="utf-8") as fh:
        alle = [json.loads(z) for z in fh if z.strip()]
    check("jede Zeile der Ablage ist gueltiges JSON", True, str(len(alle)))
    unvollstaendig = [z.get("datei") for z in alle if any(f not in z for f in PFLICHT)]
    check("jede Zeile traegt die Pflichtfelder", not unvollstaendig, str(unvollstaendig[:5]))
    check("mindestens eine Zeile je Datei vorhanden", len(alle) >= 1, str(len(alle)))
    messwert("zeilen_in_laeufe_jsonl", len(alle), "Zeilen")
    messwert("dateien_in_laeufe_jsonl", len({z["datei"] for z in alle}), "Dateien")

bericht()
