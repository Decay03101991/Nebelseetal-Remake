# -*- coding: ascii -*-
"""M12: `tools/rot_historie.py` wertet NUR `docs/audits/laeufe.jsonl` aus.

Was diese Datei beweist
-----------------------
1. KANDIDAT: 31 gruene Allein-Laeufe mit 12 s -> Kandidat. GEGENPROBE: 29 Laeufe -> kein Kandidat,
   und 31 Laeufe mit 9 s -> kein Kandidat (Grenze bei 10 s).
2. NUR ALLEIN GEMESSEN zaehlt: 31 gruene Laeufe mit 12 s unter `parallel 2` ergeben KEINEN
   Kandidaten (unter Last gemessene Dauern sind keine Grundlage).
3. AENDERUNG sperrt: eine BETRIFFT-Datei, die vor 3 Tagen geaendert wurde, nimmt die Datei aus der
   Liste; vor 30 Tagen nicht.
4. WACKELT: im selben Commit einmal rot und einmal gruen -> Wackelkandidat; zwei verschiedene
   Commits (rot, dann gruen) sind KEIN Wackler.
5. NIE AUFGEZEICHNET: eine Pruefdatei ohne Zeile taucht dort auf.
6. TEUER JE FUND: Dauer / (Rotfunde + 1), absteigend, hoechstens zehn.
7. Ausgabe: Markdown und CSV entstehen, die CSV traegt alle vier Listen mit der Spalte `liste`.

Aufruf:  python -X utf8 tests/test_rot_historie.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = []
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src, messwert

ROOT, SRC = import_src()
sys.path.insert(0, os.path.join(ROOT, "tools"))
import rot_historie as R  # noqa: E402


def zeile(datei="test_x.py", commit="c1", bestanden=True, dauer=12.0, allein="ja",
          fehler=0, zeit="2026-11-12T22:00:00"):
    return {"datei": datei, "commit": commit, "bestanden": bestanden, "dauer": dauer,
            "allein": allein, "fehler": fehler, "zeit": zeit, "lauf": zeit, "parallel":
            1 if allein == "ja" else 2, "rc": 0 if bestanden else 1, "befunde": 0,
            "ausgesetzt": False, "stufe": 3}


# ==========================================================================
abschnitt("1. Kandidat ab 30 Laeufen, 0 rot, 10 s allein")
# ==========================================================================
_viel = [zeile(commit="c%d" % i) for i in range(31)]
_e = R.auswerten(_viel)
check("31 gruene Allein-Laeufe mit 12 s ergeben einen Kandidaten",
      len(_e["kandidaten"]) == 1, str(len(_e["kandidaten"])))
check("der Kandidat nennt Datei, Laeufe und Median",
      _e["kandidaten"] and _e["kandidaten"][0]["datei"] == "test_x.py"
      and _e["kandidaten"][0]["laeufe"] == 31
      and _e["kandidaten"][0]["median_allein_s"] == 12.0, str(_e["kandidaten"]))
check("Gegenprobe: 29 Laeufe ergeben keinen Kandidaten",
      R.auswerten(_viel[:29])["kandidaten"] == [], str(R.auswerten(_viel[:29])["kandidaten"]))
_langsam = [zeile(commit="c%d" % i, dauer=9.0) for i in range(31)]
check("Gegenprobe: 31 Laeufe mit 9 s ergeben keinen Kandidaten (Grenze 10 s)",
      R.auswerten(_langsam)["kandidaten"] == [], str(R.auswerten(_langsam)["kandidaten"]))
_rot = _viel + [zeile(commit="rot1", bestanden=False)]
check("Gegenprobe: ein einziger roter Lauf nimmt den Kandidaten weg",
      R.auswerten(_rot)["kandidaten"] == [], str(R.auswerten(_rot)["kandidaten"]))

# ==========================================================================
abschnitt("2. Nur ALLEIN gemessene Dauern zaehlen")
# ==========================================================================
_unter_last = [zeile(commit="c%d" % i, allein="nein") for i in range(40)]
check("40 gruene Laeufe unter Last (parallel 2) ergeben keinen Kandidaten",
      R.auswerten(_unter_last)["kandidaten"] == [], str(R.auswerten(_unter_last)["kandidaten"]))
_gemischt = [zeile(commit="c%d" % i, dauer=12.0) for i in range(3)] + \
            [zeile(commit="d%d" % i, dauer=300.0, allein="nein") for i in range(40)]
_g = R.auswerten(_gemischt)
check("die Last-Laeufe (300 s) gehen NICHT in den Median ein: er bleibt bei den 12 s der "
      "Allein-Laeufe", _g["kandidaten"] and _g["kandidaten"][0]["median_allein_s"] == 12.0,
      str(_g["kandidaten"]))
_schnell_allein = [zeile(commit="c%d" % i, dauer=9.0) for i in range(3)] + \
                  [zeile(commit="d%d" % i, dauer=300.0, allein="nein") for i in range(40)]
check("Gegenprobe: 3 Allein-Laeufe mit 9 s und 40 Last-Laeufe mit 300 s -> kein Kandidat "
      "(der Median kommt nur aus den Allein-Laeufen)",
      R.auswerten(_schnell_allein)["kandidaten"] == [],
      str(R.auswerten(_schnell_allein)["kandidaten"]))
messwert("grenze_kandidat", R.MIN_LAEUFE, "Laeufe")

# ==========================================================================
abschnitt("3. Eine kuerzlich geaenderte BETRIFFT-Datei sperrt")
# ==========================================================================
frisch = R.auswerten(_viel, {"test_x.py": 3.0})
check("Aenderung vor 3 Tagen -> kein Kandidat", frisch["kandidaten"] == [],
      str(frisch["kandidaten"]))
alt = R.auswerten(_viel, {"test_x.py": 30.0})
check("Aenderung vor 30 Tagen -> Kandidat bleibt", len(alt["kandidaten"]) == 1,
      str(len(alt["kandidaten"])))
_unbekannt = R.auswerten(_viel, {"src/welt.py": 1.0})
check("eine andere Datei sperrt nicht", len(_unbekannt["kandidaten"]) == 1,
      str(len(_unbekannt["kandidaten"])))

# ==========================================================================
abschnitt("4. Wackelkandidat: derselbe Commit, einmal rot und einmal gruen")
# ==========================================================================
_wackel = [zeile(commit="abc", bestanden=False), zeile(commit="abc", bestanden=True)]
check("rot und gruen im selben Commit ergibt einen Wackelkandidaten",
      len(R.auswerten(_wackel)["wackler"]) == 1, str(len(R.auswerten(_wackel)["wackler"])))
check("zwei verschiedene Commits (rot, dann gruen) sind kein Wackler",
      R.auswerten([zeile(commit="a", bestanden=False), zeile(commit="b", bestanden=True)])["wackler"]
      == [], "")
check("zwei gruene Laeufe im selben Commit sind kein Wackler",
      R.auswerten([zeile(commit="a"), zeile(commit="a")])["wackler"] == [], "")

# ==========================================================================
abschnitt("5. Nie aufgezeichnet: Pruefdatei ohne Zeile")
# ==========================================================================
_e2 = R.auswerten(_viel, None, ["test_x.py", "test_textqualitaet.py"])
check("die Datei ohne Zeile steht in der Liste 'nie'",
      _e2["nie"] == ["test_textqualitaet.py"], str(_e2["nie"]))
check("eine Datei MIT Zeile steht nicht in 'nie'", "test_x.py" not in _e2["nie"], str(_e2["nie"]))
check("ohne Uebergabe der bekannten Dateien bleibt die Liste leer (keine Erfindung)",
      R.auswerten(_viel)["nie"] == [], "")

# ==========================================================================
abschnitt("6. Teuer je Fund: Dauer / (Rotfunde + 1), hoechstens zehn")
# ==========================================================================
_teuer = [zeile(datei="test_teuer.py", commit="c%d" % i, dauer=100.0) for i in range(3)]
_teuer.append(zeile(datei="test_teuer.py", commit="crot", bestanden=False, dauer=100.0))
_billig = [zeile(datei="test_billig.py", commit="d%d" % i, dauer=1.0) for i in range(3)]
_et = R.auswerten(_teuer + _billig)
_namen = [e["datei"] for e in _et["teuer"]]
check("die teure Datei steht vor der billigen", _namen[0] == "test_teuer.py", str(_namen))
check("400 s bei 1 Rotfund ergeben 200 s je Fund",
      _et["teuer"][0]["je_fund_s"] == 200.0, str(_et["teuer"][0]["je_fund_s"]))
check("hoechstens zehn Eintraege",
      len(R.auswerten([zeile(datei="test_%02d.py" % i) for i in range(20)])["teuer"]) <= 10,
      str(len(R.auswerten([zeile(datei="test_%02d.py" % i) for i in range(20)])["teuer"])))

# ==========================================================================
abschnitt("7. Ausgabe: Markdown und CSV mit allen vier Listen")
# ==========================================================================
_e3 = R.auswerten(_viel, None, ["test_x.py", "test_fehlt.py"])
_md = R.als_markdown(_e3, "12.11.2026 23:50")
check("der Bericht nennt die vier Abschnitte",
      all(t in _md for t in ("## 1. Kandidaten", "## 2. Wackelkandidaten", "## 3. Nie aufgezeichnet",
                             "## 4. Teuer je Fund")), "")
check("der Bericht nennt den Kandidaten", "test_x.py" in _md, "")
check("der Bericht nennt die nie aufgezeichnete Datei", "test_fehlt.py" in _md, "")
_csv = R.als_csv(_e3)
check("die CSV traegt die Spalte liste und die vier Listen",
      _csv.splitlines()[0].startswith("liste;datei") and "kandidat;" in _csv and "nie;" in _csv,
      _csv.splitlines()[0])
with tempfile.TemporaryDirectory() as ordner:
    md_pfad, csv_pfad = R.schreiben(_e3, os.path.join(ordner, "R.md"),
                                    os.path.join(ordner, "R.csv"), stand="Test")
    check("beide Dateien entstehen", os.path.exists(md_pfad) and os.path.exists(csv_pfad))
    check("die Markdown-Datei ist nicht leer", os.path.getsize(md_pfad) > 200,
          str(os.path.getsize(md_pfad)))

# ==========================================================================
abschnitt("8. Lesen: kaputte Zeilen brechen nicht, fehlende Datei ergibt leer")
# ==========================================================================
with tempfile.TemporaryDirectory() as ordner:
    pfad = os.path.join(ordner, "l.jsonl")
    with open(pfad, "w", encoding="utf-8") as fh:
        fh.write('{"datei": "test_a.py", "bestanden": true, "dauer": 1, "allein": "ja"}\n')
        fh.write("das ist kein JSON\n")
        fh.write('{"datei": "test_b.py", "bestanden": false}\n')
    gelesen = R.zeilen_lesen(pfad)
    check("zwei gueltige Zeilen werden gelesen, die kaputte uebersprungen",
          len(gelesen) == 2, str(len(gelesen)))
    check("eine fehlende Ablage ergibt eine leere Liste",
          R.zeilen_lesen(os.path.join(ordner, "gibtsnicht.jsonl")) == [], "")

bericht()
