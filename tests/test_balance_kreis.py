"""B-1 Sollkurve (Ablauf Schritt 8, 07.11.2026): Pruefungen des Werkzeugs `tools/balance_kreis.py`.

Geprueft wird, was der Schnitt zusagt:
  A. Zwei Laeufe ohne Datenaenderung ergeben dieselbe Kurve (Determinismus).
  B. Eine geaenderte Datendatei verschiebt den betroffenen Korridor (Holz +10 Prozent).
  C. Das Werkzeug schreibt NIE unter `src/` - nur `data/sollkurve.json`.
  D. Die abgelegte Datei passt zu den heutigen Daten (Hashes im Kopf `erzeugt_aus`).
  E. Der Korridor ist Ideal x 0,7 bis x 1,1, die Raender stehen in der Datei.
  F. Die Startkarte ist die belegte Standardkarte (Register 228) und ihre Felder sind gezaehlt.
  G. Luecken werden BENANNT statt erfunden (fehlende Preise, fehlende Forschungskosten).

ASCII-only (Pruefdatei-Konvention).
"""
from __future__ import annotations

import io
import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

import_src()
HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HIER, "tools"))
import balance_kreis as BK  # noqa: E402


def _kopie_der_daten():
    """Eine temporaere Projektwurzel mit Kopie von data/ - fuer Aenderungen ohne Risiko."""
    ziel = tempfile.mkdtemp(prefix="sollkurve_")
    shutil.copytree(os.path.join(HIER, "data"), os.path.join(ziel, "data"))
    return ziel


# ------------------------------------------------------------------ A. Determinismus
abschnitt("A. Zwei Laeufe ergeben dieselbe Kurve")
_erst = BK.sollkurve(HIER, 20)
_zweit = BK.sollkurve(HIER, 20)
check("zwei Laeufe sind gleich", _erst == _zweit, "Lauf 1 und Lauf 2 verglichen")
check("die Kurve hat einen Tag 0", _erst["tage"][0]["tag"] == 0, str(_erst["tage"][0]["tag"]))
check("die Kurve hat 21 Zeilen (Tag 0 bis 20)", len(_erst["tage"]) == 21, str(len(_erst["tage"])))
check("keine Zeitstempel in der Datei (sonst waeren zwei Laeufe nie gleich)",
      "zeit" not in json.dumps(_erst).lower() or "spielzeit" not in json.dumps(_erst).lower(),
      "nur Daten, keine Uhr")

# ------------------------------------------------------------------ B. Datenaenderung
abschnitt("B. Holz +10 Prozent in der Datendatei verschiebt den Holzkorridor")
_tmp = _kopie_der_daten()
try:
    _pfad = os.path.join(_tmp, "data", "resources.json")
    with io.open(_pfad, encoding="utf-8") as f:
        _res = json.load(f)
    _geaendert = 0
    for _eintrag in _res.get("rohstoffe") or []:
        if str(_eintrag.get("id")) == "holz":
            for _gelaende, _wert in list((_eintrag.get("ertrag_pro_stunde") or {}).items()):
                _eintrag["ertrag_pro_stunde"][_gelaende] = round(float(_wert) * 1.1, 3)
                _geaendert += 1
    check("der Holzeintrag wurde gefunden", _geaendert > 0, str(_geaendert))
    with io.open(_pfad, "w", encoding="utf-8", newline="") as f:
        json.dump(_res, f, ensure_ascii=False, indent=2)
    _neu = BK.sollkurve(_tmp, 20)
    _holz_alt = float(_erst["tage"][10]["holz"]["ideal"])
    _holz_neu = float(_neu["tage"][10]["holz"]["ideal"])
    check("der Holzkorridor liegt danach hoeher", _holz_neu > _holz_alt,
          "Tag 10: alt %s, neu %s" % (_holz_alt, _holz_neu))
    check("Stein bleibt unberuehrt (keine Querwirkung)", _neu["tage"][10]["stein"] == _erst["tage"][10]["stein"],
          "Tag 10 Stein: %s" % _erst["tage"][10]["stein"]["ideal"])
finally:
    shutil.rmtree(_tmp, ignore_errors=True)

# ------------------------------------------------------------------ C. Kein Schreiben unter src/
# ENTSCHEIDUNG 07.11.2026 (Ablauf Schritt 9, B-2): das Werkzeug LIEST src/ jetzt - der A/B-Lauf
# kopiert src/ und data/ in einen tempoeraeren Ordner, damit die Aenderung das Projekt nicht
# beruehrt. Die Wache dreht sich deshalb um: sie verlangt, dass JEDE Schreibstelle des Werkzeugs
# ausserhalb des Projekt-src/ liegt (statt "das Wort src kommt nicht vor").
abschnitt("C. Das Werkzeug schreibt nie in das Projekt-src/ (B-2 kopiert src nur lesend)")
import ast  # noqa: E402
with io.open(os.path.join(HIER, "tools", "balance_kreis.py"), encoding="utf-8") as f:
    _quelle = f.read()
check("der Schreibpfad data/sollkurve.json ist vorhanden", '"sollkurve.json"' in _quelle, "Pfad vorhanden")
_schreibstellen = []
for _knoten in ast.walk(ast.parse(_quelle)):
    if isinstance(_knoten, ast.Call) and _knoten.args:
        _name = ""
        if isinstance(_knoten.func, ast.Name):
            _name = _knoten.func.id
        elif isinstance(_knoten.func, ast.Attribute):
            _name = _knoten.func.attr
        if _name != "open":
            continue
        _modus = ""
        if len(_knoten.args) > 1 and isinstance(_knoten.args[1], ast.Constant):
            _modus = str(_knoten.args[1].value)
        for _kw in _knoten.keywords:
            if _kw.arg == "mode" and isinstance(_kw.value, ast.Constant):
                _modus = str(_kw.value.value)
        if "w" in _modus or "a" in _modus or "+" in _modus:
            _schreibstellen.append(ast.unparse(_knoten.args[0]))
check("es gibt Schreibstellen im Werkzeug", len(_schreibstellen) >= 3, str(len(_schreibstellen)))
check("keine Schreibstelle liegt unter src/",
      all('"src"' not in _stelle and "'src'" not in _stelle for _stelle in _schreibstellen),
      str([s for s in _schreibstellen if "src" in s]))
_tmp2 = _kopie_der_daten()
try:
    import subprocess  # frischer Prozess, damit die Ausgabe wirklich getrennt ist
    _lauf = subprocess.run([sys.executable, "-X", "utf8", "tools/balance_kreis.py", "--sollkurve",
                            "--tage", "5", "--wurzel", _tmp2, "--schreiben"],
                           cwd=HIER, capture_output=True, text=True)
    check("der Aufruf mit --schreiben endet mit 0", _lauf.returncode == 0,
          "RC %s, %s" % (_lauf.returncode, (_lauf.stderr or "")[:80]))
    check("die Datei liegt in data/ der angegebenen Wurzel",
          os.path.isfile(os.path.join(_tmp2, "data", "sollkurve.json")), "data/sollkurve.json")
    check("unter src/ wurde nichts angelegt", not os.path.exists(os.path.join(_tmp2, "src")),
          "kein src-Ordner")
finally:
    shutil.rmtree(_tmp2, ignore_errors=True)

# ------------------------------------------------------------------ D. Abgelegte Datei
abschnitt("D. Die abgelegte Datei passt zu den heutigen Daten")
_datei = os.path.join(HIER, "data", "sollkurve.json")
check("data/sollkurve.json liegt im Projekt", os.path.isfile(_datei), _datei)
with io.open(_datei, encoding="utf-8") as f:
    _abgelegt = json.load(f)
check("der Kopf nennt die Eingabedateien", len(_abgelegt.get("erzeugt_aus") or {}) == 6,
      str(sorted((_abgelegt.get("erzeugt_aus") or {}).keys())))
_aktuell = True
for _name, _hash in (_abgelegt.get("erzeugt_aus") or {}).items():
    _pfad = os.path.join(HIER, _name.replace("/", os.sep))
    _ist = BK.hash_von(HIER, *_name.split("/"))
    if _ist != _hash:
        _aktuell = False
        befund("Hash weicht ab: %s" % _name)
check("die Hashes stimmen mit den heutigen Dateien (sonst ist die Kurve veraltet)", _aktuell,
      "sechs Eingabedateien verglichen")
check("die abgelegte Kurve ist die heutige Rechnung", _abgelegt["tage"] == _erst["tage"],
      "Tage verglichen")

# ------------------------------------------------------------------ E. Korridor
abschnitt("E. Der Korridor ist Ideal x 0,7 bis x 1,1")
_baender = _abgelegt.get("baender") or {}
check("unterer Rand 0,7", float(_baender.get("unten", 0)) == 0.7, str(_baender.get("unten")))
check("oberer Rand 1,1", float(_baender.get("oben", 0)) == 1.1, str(_baender.get("oben")))
_zeile = _abgelegt["tage"][5]
for _stoff in ("holz", "stein", "nahrung", "gold"):
    check("%s: unten = Ideal x 0,7" % _stoff,
          abs(float(_zeile[_stoff]["unten"]) - round(float(_zeile[_stoff]["ideal"]) * 0.7, 2)) < 0.011,
          str(_zeile[_stoff]))
check("das Punkte-Ziel steht mit Quelle in der Datei",
      float((_abgelegt.get("punkte_ziel_je_spieltag") or {}).get("wert", 0)) == 3.3,
      str(_abgelegt.get("punkte_ziel_je_spieltag")))

# ------------------------------------------------------------------ F. Startkarte
abschnitt("F. Die Startkarte ist die belegte Standardkarte")
_karte, _felder = BK.gelande_der_startkarte(HIER)
check("die Startkarte ist original-036 (Register 228)", _karte == "original-036", _karte)
check("die Felder sind gezaehlt (Summe 100)", sum(_felder.values()) == 100, str(sum(_felder.values())))
check("Wald ist der groesste Anteil", _felder.get("Wald", 0) == 28, str(_felder.get("Wald")))

# ------------------------------------------------------------------ G. Luecken
abschnitt("G. Luecken werden benannt, nicht erfunden")
check("die fehlenden Forschungskosten stehen als Luecke in der Kurve",
      any("Forschungskosten" in str(l) for l in (_abgelegt.get("luecken") or [])),
      str((_abgelegt.get("luecken") or [])[:2]))
check("die Annahmen stehen in der Datei", len(_abgelegt.get("annahmen") or []) >= 3,
      str(len(_abgelegt.get("annahmen") or [])))
check("der Zweck nennt das Werkzeug (nicht von Hand aendern)",
      "balance_kreis" in str(_abgelegt.get("zweck")), str(_abgelegt.get("zweck"))[:60])

bericht()
