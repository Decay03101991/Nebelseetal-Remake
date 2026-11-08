# -*- coding: ascii -*-
"""Schritt 13 des Ablaufs: Daten und Quellen - jede Zahl hat eine Herkunft, jede Mechanik einen Schalter.

DER AUFTRAG (Ablauf, Schritt 13): "Jede Balance-Zahl liegt in `data/`, jede Mechanik hat einen
Schalter, jede Zahl traegt eine Quelle oder das Wort VORSCHLAG." Drei Abschnitte, ein Bestand:

1. **Balance-Konstanten im Code.** Eine Konstante, deren Name ein Balance-Wort traegt (PREIS, KOSTEN,
   DAUER, RATE, FAKTOR, PROZENT, BONUS, TEMPO, MENGE), muss entweder ein Quellenwort auf ihrer Zeile
   tragen (belegt / VORSCHLAG / Handbuch / gerechnet / ANNAHME / Entscheidung / Register) oder im
   Bestand `tests/daten_quellen_bestand.json` mit Grund stehen. Eine NEUE Zahl ohne beides macht die
   Wache rot - sie kommt dann nicht stillschweigend ins Spiel.
2. **Schalter je Mechanik.** Jede Datendatei mit einem Feld `aktiv` muss im Quelltext gelesen werden;
   ein Schalter, den niemand liest, ist eine Attrappe.
3. **Quelle je Datendatei.** Jede `data/*.json` traegt eine Quellenangabe (`quelle`, `_quelle`,
   `_belegt`, `_herkunft` oder `_hinweis`) oder steht im Bestand. Was im Bestand steht, wird als
   VORSCHLAG gemeldet und NICHT erfunden.

WAS DER BESTAND AM 08.11.2026 ENTHAELT (gemessen, nicht geschaetzt):
  * 51 Datendateien, davon **6 ohne jede Quellenangabe** (bot_bedarf, bot_diebstahl, bot_forschung,
    bot_stimmen, marsch_optik, spionage).
  * 17 Datendateien mit Schalter `aktiv` - alle 17 werden im Quelltext gelesen (0 Attrappen).
  * 15 Balance-Konstanten ohne Quellenwort auf der Zeile, davon **9 echte Werte** und 6 technische
    (Pfad, Weiterleitung, Schalter, 0,0 = aus, Zeichenoptik).

Aufruf:  python -X utf8 tests/test_daten_und_quellen.py
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src, messwert

ROOT, SRC = import_src()
BESTAND_DATEI = os.path.join(ROOT, "tests", "daten_quellen_bestand.json")
MUSTER = re.compile(r"^([A-Z_][A-Z0-9_]*(?:PREIS|KOSTEN|DAUER|RATE|FAKTOR|PROZENT|BONUS|TEMPO|MENGE)"
                    r"[A-Z0-9_]*)\s*=\s*(.+)$", re.M)
QUELLWORTE = ("belegt", "BELEGT", "VORSCHLAG", "Handbuch", "gerechnet", "ANNAHME",
              "Entscheidung", "Register")
DATEI_QUELLEN = ('"quelle"', "_quelle", "_belegt", "_herkunft", "_hinweis")


def bestand() -> dict:
    with open(BESTAND_DATEI, encoding="utf-8") as datei:
        return json.load(datei)


def quelltext() -> str:
    """Der ganze Quelltext als EIN Text (fuer die Schalter-Frage)."""
    teile = []
    for pfad in sorted(glob.glob(os.path.join(SRC, "*.py"))):
        teile.append(open(pfad, encoding="utf-8").read())
    return "\n".join(teile)


_bestand = bestand()
_konstanten_bestand = {(k["datei"], k["name"]): k for k in _bestand.get("balance_konstanten") or []}
_dateien_bestand = {d["datei"]: d for d in _bestand.get("dateien_ohne_quelle") or []}

# ------------------------------------------------ 1. Balance-Zahlen im Code
abschnitt("1. Jede Balance-Konstante hat eine Quelle oder einen Eintrag im Bestand")

_gefunden = []
for pfad in sorted(glob.glob(os.path.join(SRC, "*.py"))):
    text = open(pfad, encoding="utf-8").read()
    name_datei = os.path.basename(pfad)
    for treffer in MUSTER.finditer(text):
        zeile = text[treffer.start():text.find("\n", treffer.start())]
        if any(wort in zeile for wort in QUELLWORTE):        # Quelle steht auf der Zeile
            continue
        _gefunden.append((name_datei, treffer.group(1)))
messwert("balance_konstanten_ohne_quellenwort", len(_gefunden), "Konstanten", "AST-freier Scan src/*.py")
_neu = [k for k in _gefunden if k not in _konstanten_bestand]
check("keine NEUE Balance-Konstante ohne Quelle", not _neu,
      "neu: %s" % ", ".join("%s:%s" % k for k in _neu[:5]))
check("der Bestand ist vollstaendig (jede gefundene Konstante steht drin)",
      all(k in _konstanten_bestand for k in _gefunden),
      str([k for k in _gefunden if k not in _konstanten_bestand][:3]))
_echte_werte = [k for k in _konstanten_bestand.values() if k.get("art") == "balance"]
messwert("balance_werte_ohne_quelle", len(_echte_werte), "Werte", "tests/daten_quellen_bestand.json")
if _echte_werte:
    befund("Balance-Werte OHNE belegte Quelle (VORSCHLAG, Daniel vorlegen): %s"
           % ", ".join("%s:%s" % (k["datei"], k["name"]) for k in _echte_werte), "")
check("jede Bestandszeile nennt einen Grund",
      all(str(k.get("grund") or "").strip() for k in _bestand.get("balance_konstanten") or []))
check("jede Bestandszeile nennt ihre Art (balance/technisch)",
      all(k.get("art") in ("balance", "technisch") for k in _bestand.get("balance_konstanten") or []))

# ------------------------------------------------ 2. Schalter je Mechanik
abschnitt("2. Jeder Schalter `aktiv` wird auch gelesen")

_text = quelltext()
_dateien = sorted(glob.glob(os.path.join(ROOT, "data", "*.json")))
_mit_schalter = []
for pfad in _dateien:
    name = os.path.basename(pfad)
    try:
        daten = json.loads(open(pfad, encoding="utf-8").read())
    except (OSError, ValueError):
        continue
    if isinstance(daten, dict) and "aktiv" in daten:
        _mit_schalter.append(name)
messwert("datendateien", len(_dateien), "Dateien", "data/*.json")
messwert("dateien_mit_schalter", len(_mit_schalter), "Dateien", "Feld aktiv")
_attrappen = [n for n in _mit_schalter if n not in _text]
check("jede Datendatei mit `aktiv` wird im Quelltext gelesen", not _attrappen, str(_attrappen))
check("es gibt ueberhaupt Schalter (sonst waere der Abschnitt leer)", len(_mit_schalter) >= 10,
      str(len(_mit_schalter)))

# ------------------------------------------------ 3. Quelle je Datendatei
abschnitt("3. Jede Datendatei traegt eine Quelle oder steht im Bestand")

_ohne = []
for pfad in _dateien:
    name = os.path.basename(pfad)
    roh = open(pfad, encoding="utf-8").read()
    if not any(marke in roh for marke in DATEI_QUELLEN):
        _ohne.append(name)
messwert("dateien_ohne_quelle", len(_ohne), "Dateien", "data/*.json")
_neu_datei = [n for n in _ohne if n not in _dateien_bestand]
check("keine NEUE Datendatei ohne Quellenangabe", not _neu_datei, str(_neu_datei))
check("der Bestand nennt genau die Dateien, die keine Quelle tragen",
      sorted(_ohne) == sorted(_dateien_bestand), "%s vs %s" % (sorted(_ohne), sorted(_dateien_bestand)))
_unbegruendet = [n for n in _ohne if not str((_dateien_bestand.get(n) or {}).get("grund") or "").strip()]
check("jede quellenlose Datei hat einen Grund im Bestand", not _unbegruendet, str(_unbegruendet))
if _ohne:
    befund("Datendateien OHNE Quellenangabe (VORSCHLAG bzw. Anzeige, Daniel vorlegen): %s"
           % ", ".join(_ohne), "")

_bestand_datei = json.loads(open(BESTAND_DATEI, encoding="utf-8").read())
check("der Bestand traegt ein Datum", bool(_bestand_datei.get("stand")),
      str(_bestand_datei.get("stand")))

befund("Was NICHT geprueft ist: ob eine vorhandene Quellenangabe auch STIMMT (ob die Zahl wirklich "
       "im Handbuch steht). Das prueft `test_gpt_originaltreue` gegen die Quellen; hier geht es "
       "nur darum, dass keine Zahl OHNE Herkunft dazukommt.", "")
befund("Die 9 Balance-Werte ohne Quelle sind als VORSCHLAG in docs/FRAGEN_AN_DANIEL_20261107.md "
       "nachgetragen - sie werden nicht umgerechnet, bis Daniel sie bestaetigt oder korrigiert.", "")
sys.exit(bericht())
