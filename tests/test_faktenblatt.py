# -*- coding: ascii -*-
"""M11: das Faktenblatt wird aus `data/` GEZAEHLT - die Wache haelt Blatt und Daten zusammen.

Warum (Claude, Antwort Nr. 16, Teil B): drei falsche Zahlen in den Auftraegen Nr. 12 bis 15
("vier Zutaten", "18 Waren", "2148 px Dorfzentrum") kamen aus dem Gedaechtnis. Das Faktenblatt ist
die Antwort: eine Zahl, eine Quelle, maschinell gezaehlt.

Was diese Datei beweist
-----------------------
1. BLATT == DATEN: `zaehlen(data)` ist genau das, was in `docs/faktenblatt.json` steht. Weicht es
   ab, ist das Blatt veraltet - dann nennt die Wache den Befehl, der es neu erzeugt.
2. GEGENPROBE: eine Ware in eine KOPIE von `data/` dazu -> 18 Waren, 17 Rezepte, 1 Ware ohne
   Rezept. Damit ist belegt, dass die Zahlen wirklich aus der Datei kommen und nicht feststehen.
3. ZUTATEN: hoechste Zutatenzahl je Rezept = 1 (die Datenlage seit F-04), nicht 4.
4. AUFTRAGSPRUEFUNG: `auftrag_pruefen` findet "18 Waren" und "4 Zutaten" als Abweichung und laesst
   die richtigen Zahlen stehen (Gegenprobe: der richtige Satz ergibt keinen Fund).
5. AUSGABE: Markdown und JSON entstehen, fest sortiert; zwei Laeufe ergeben dasselbe.
6. QUELLTEXT: die Zahlen entstehen mit `len(...)` aus den Dateien - kein Literal 17/28/21 im Kern.

Aufruf:  python -X utf8 tests/test_faktenblatt.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = []
PRUEF_DATEN = ['buildings.json', 'gelaende.json', 'items.json', 'research.json', 'units.json', 'voelker.json', 'warenrezepte.json', 'welten.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src, messwert

ROOT, SRC = import_src()
sys.path.insert(0, os.path.join(ROOT, "tools"))
import auftrag_pruefen as A  # noqa: E402
import faktenblatt as F  # noqa: E402

DATEN = os.path.join(ROOT, "data")
BLATT = os.path.join(ROOT, "docs", "faktenblatt.json")

# ==========================================================================
abschnitt("1. Blatt == Daten (sonst ist das Blatt veraltet)")
# ==========================================================================
if not os.path.exists(BLATT):
    befund("docs/faktenblatt.json fehlt - mit 'python -X utf8 tools/faktenblatt.py' erzeugen")
else:
    with open(BLATT, encoding="utf-8") as fh:
        blatt = json.load(fh)
    jetzt = F.zaehlen(DATEN)
    soll = blatt.get("zaehlung") or {}
    _abweichungen = []
    for schluessel in ("waren", "einheiten", "forschungen", "gebaeude", "voelker", "welten",
                       "gelaendearten", "werkstaetten"):
        if jetzt.get(schluessel) != soll.get(schluessel):
            _abweichungen.append(schluessel)
    _rezepte_neu = dict(jetzt.get("rezepte") or {})
    _rezepte_alt = dict(soll.get("rezepte") or {})
    if _rezepte_neu != _rezepte_alt:
        _abweichungen.append("rezepte")
    check("Faktenblatt stimmt mit data/ ueberein (sonst: tools/faktenblatt.py laufen lassen)",
          not _abweichungen, str(_abweichungen))
    check("das Blatt nennt den Stand von data/", "data_stand" in blatt,
          str(list(blatt)[:6]))
    messwert("waren", jetzt["waren"]["anzahl"], "Waren")
    messwert("rezepte", jetzt["rezepte"]["anzahl"], "Rezepte")
    messwert("einheiten", jetzt["einheiten"]["anzahl"], "Einheiten")
    messwert("forschungen", jetzt["forschungen"]["anzahl"], "Forschungen")
    messwert("gebaeude", jetzt["gebaeude"]["anzahl"], "Gebaeude")

# ==========================================================================
abschnitt("2. Gegenprobe: eine Ware dazu ergibt 18")
# ==========================================================================
with tempfile.TemporaryDirectory() as ordner:
    kopie = os.path.join(ordner, "data")
    shutil.copytree(DATEN, kopie)
    pfad_items = os.path.join(kopie, "items.json")
    with open(pfad_items, encoding="utf-8") as fh:
        items = json.load(fh)
    items["waren"]["Probeware"] = {"werkstatt": "Schmiede", "voraussetzung": "keine",
                                   "voraussetzung_struktur": None, "icon": "", "benoetigt_von": [],
                                   "anmerkung": "Pruefware der Wache"}
    with open(pfad_items, "w", encoding="utf-8") as fh:
        json.dump(items, fh, ensure_ascii=False, indent=2)
    mit_ware = F.zaehlen(kopie)
    ohne = F.zaehlen(DATEN)
    check("die Kopie hat eine Ware mehr (18 statt 17)",
          mit_ware["waren"]["anzahl"] == ohne["waren"]["anzahl"] + 1 == 18,
          "%d gegen %d" % (mit_ware["waren"]["anzahl"], ohne["waren"]["anzahl"]))
    check("die Rezepte bleiben bei 17 (das Rezept fehlt in der Kopie)",
          mit_ware["rezepte"]["anzahl"] == ohne["rezepte"]["anzahl"],
          str(mit_ware["rezepte"]["anzahl"]))
    check("die neue Ware steht unter 'Waren ohne Rezept'",
          mit_ware["rezepte"]["waren_ohne_rezept"] == ["Probeware"],
          str(mit_ware["rezepte"]["waren_ohne_rezept"]))
    check("die Werkstatt-Zaehlung waechst mit (Schmiede 9)",
          mit_ware["werkstaetten"]["je_werkstatt_anzahl"].get("Schmiede") == 9,
          str(mit_ware["werkstaetten"]["je_werkstatt_anzahl"]))

# ==========================================================================
abschnitt("3. Zutaten: hoechstens eine je Rezept (die Datenlage seit F-04)")
# ==========================================================================
_jetzt = F.zaehlen(DATEN)
check("hoechste Zutatenzahl je Rezept ist 1, nicht 4",
      _jetzt["rezepte"]["hoechste_zutaten_je_rezept"] == 1,
      str(_jetzt["rezepte"]["hoechste_zutaten_je_rezept"]))
check("jede Ware hat ein Rezept (keine Luecke zwischen items.json und warenrezepte.json)",
      _jetzt["rezepte"]["waren_ohne_rezept"] == [],
      str(_jetzt["rezepte"]["waren_ohne_rezept"]))
check("kein Rezept ohne Zutaten", _jetzt["rezepte"]["ohne_kosten"] == [],
      str(_jetzt["rezepte"]["ohne_kosten"]))
check("die Werkstaetten-Zuordnung ergibt 8 / 5 / 4",
      sorted(_jetzt["werkstaetten"]["je_werkstatt_anzahl"].values()) == [4, 5, 8],
      str(_jetzt["werkstaetten"]["je_werkstatt_anzahl"]))

# ==========================================================================
abschnitt("4. Die Auftragspruefung findet falsche Zahlen")
# ==========================================================================
with open(BLATT, encoding="utf-8") as fh:
    _blatt = json.load(fh)
_falsch = "Der Auftrag nennt 18 Waren und 4 Zutaten."
_treffer = A.pruefen(_falsch, _blatt)
check("'18 Waren' wird als Abweichung gemeldet",
      any(t["begriff"] == "waren" and t["genannt"] == 18 and t["richtig"] == 17 for t in _treffer),
      str(_treffer))
check("'4 Zutaten' wird als Abweichung gemeldet",
      any(t["begriff"] == "zutaten" and t["genannt"] == 4 and t["richtig"] == 1 for t in _treffer),
      str(_treffer))
_richtig = "Der Auftrag nennt 17 Waren, 17 Rezepte, 28 Einheiten, 21 Forschungen und 20 Gebaeude."
check("Gegenprobe: ein richtiger Satz ergibt keinen Fund", A.pruefen(_richtig, _blatt) == [],
      str(A.pruefen(_richtig, _blatt)))
check("Zahlen mit Tausenderpunkt werden nicht als Anzahl gelesen (1.000 Siedler)",
      A.pruefen("Es lebten 1.000 Siedler in 3 Waren.", _blatt) == []
      or all(t["genannt"] != 1000 for t in A.pruefen("Es lebten 1.000 Siedler in 3 Waren.", _blatt)))

# ==========================================================================
abschnitt("5. Ausgabe: Markdown und JSON, fest sortiert")
# ==========================================================================
with tempfile.TemporaryDirectory() as ordner:
    md_pfad, json_pfad = F.schreiben(_jetzt, os.path.join(ordner, "F.md"),
                                     os.path.join(ordner, "F.json"),
                                     breiten={"verfuegbar": False, "grund": "Test"},
                                     stand={"hash": "abc", "datum": "12.11.2026"},
                                     erzeugt="Test")
    with open(md_pfad, encoding="utf-8") as fh:
        md = fh.read()
    check("die Markdown-Datei nennt die Warenzahl", "**17**" in md or "17" in md, "")
    check("der Textbreiten-Abschnitt ist als fehlend vermerkt",
          "Fehlt:" in md or "nicht befragt" in md, "")
    with open(json_pfad, encoding="utf-8") as fh:
        geschrieben = json.load(fh)
    check("die JSON-Datei hat die drei Abschnitte stand/data_stand/zaehlung",
          set(geschrieben) >= {"stand", "data_stand", "zaehlung"}, str(sorted(geschrieben)))
    check("zwei Zaehlungen ergeben dasselbe (feste Reihenfolge, kein Zufall)",
          json.dumps(F.zaehlen(DATEN), sort_keys=True)
          == json.dumps(F.zaehlen(DATEN), sort_keys=True), "")

# ==========================================================================
abschnitt("6. Quelltext: die Zahlen werden gezaehlt, nicht gesetzt")
# ==========================================================================
_quelle = open(os.path.join(ROOT, "tools", "faktenblatt.py"), encoding="utf-8",
               errors="replace").read()
import ast as _ast  # noqa: E402
_baum = _ast.parse(_quelle)
_literale = {k.value for k in _ast.walk(_baum)
             if isinstance(k, _ast.Constant) and isinstance(k.value, int)}
_verboten = sorted({17, 28, 21} & _literale)
check("kein Zahlen-Literal 17/28/21 im Code (auch nicht in Kommentaren gerechnet)",
      not _verboten, str(_verboten))
check("die Anzahlen entstehen mit len()", _quelle.count("len(") >= 6, str(_quelle.count("len(")))
check("das Werkzeug liest die acht Datendateien",
      all(name in _quelle for name in ("items.json", "warenrezepte.json", "units.json",
                                       "research.json", "buildings.json", "voelker.json",
                                       "welten.json", "gelaende.json")), "")

bericht()
