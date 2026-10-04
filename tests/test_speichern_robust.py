"""
Pruefung: robustes Speichern (Paket W8).

Beweist, dass das neue Modul ``speichern`` einen Spielstand atomar, geprueft und
wiederherstellbar ablegt - und zwar ehrlich: ein Fehler beim Serialisieren laesst die ALTE
Datei unberuehrt, eine kaputte Datei wird gemeldet statt zu werfen.

Bewiesen wird unter anderem:
  * normaler Rundlauf: geparste Daten nach dem Laden identisch zu den gespeicherten
  * Umlaute und verschachtelte Listen ueberstehen den Rundlauf
  * scheiternde Serialisierung laesst die alte Datei unveraendert
  * kaputtes JSON wird ehrlich gemeldet (kein Absturz)
  * liegengebliebene .tmp-Datei wird aufgeraeumt
  * .bak wird VOR dem Ueberschreiben angelegt; wiederherstellen() bringt sie zurueck
  * nach einem erfolgreichen Speichern bleibt keine .tmp liegen

Aufruf:  python -X utf8 tests/test_speichern_robust.py
"""
from __future__ import annotations

import json
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import speichern as SP

ORDNER = tempfile.mkdtemp(prefix="nebel_w8_")


def pfad(name: str) -> str:
    return os.path.join(ORDNER, name)


def roh(p: str) -> str:
    with open(p, "r", encoding="utf-8") as f:
        return f.read()


def gibt_es(p: str) -> bool:
    return os.path.exists(p)


# ==========================================================================
# 1. Modul-Vertrag - die geforderten Namen und Regeln
# ==========================================================================

abschnitt("Modul-Vertrag - die geforderten Namen aus Paket W8")

check("speichere ist aufrufbar", callable(getattr(SP, "speichere", None)))
check("lade ist aufrufbar", callable(getattr(SP, "lade", None)))
check("sichere_kopie ist aufrufbar", callable(getattr(SP, "sichere_kopie", None)))
check("pruefe_datei ist aufrufbar", callable(getattr(SP, "pruefe_datei", None)))
check("wiederherstellen ist aufrufbar", callable(getattr(SP, "wiederherstellen", None)))
check("aufraeumen ist aufrufbar", callable(getattr(SP, "aufraeumen", None)))
check("offene_luecken ist aufrufbar", callable(getattr(SP, "offene_luecken", None)))

SP_QUELLE = os.path.join(SRC, "speichern.py")
with open(SP_QUELLE, "rb") as f:
    _bytes = f.read()
check("das Modul speichern.py liegt unter src/", gibt_es(SP_QUELLE), SP_QUELLE)
check("der Quelltext ist reines ASCII (Umlaute nur als ae/oe/ue/ss)",
      all(b < 128 for b in _bytes))
_quelltext = _bytes.decode("ascii")
check("das Modul laedt main.py NICHT (keine GUI-Abhaengigkeit)",
      re.search(r"^\s*(import|from)\s+main\b", _quelltext, re.M) is None)
check("das Modul laedt kein tkinter",
      re.search(r"^\s*(import|from)\s+tkinter\b", _quelltext, re.M) is None)
_std = set(re.findall(r"^\s*import\s+([a-zA-Z_][\w]*)", _quelltext, re.M))
check("das Modul nutzt nur die Standardbibliothek",
      _std <= {"json", "os", "time", "sys"}, str(sorted(_std)))

_luecken = SP.offene_luecken()
check("offene_luecken() liefert ein dict", isinstance(_luecken, dict), str(type(_luecken)))
check("offene_luecken() benennt mindestens eine Grenze ehrlich", len(_luecken) >= 3,
      f"{len(_luecken)} Punkte")
check("jede Luecke hat eine Begruendung als Text",
      all(isinstance(k, str) and isinstance(v, str) and v for k, v in _luecken.items()))


# ==========================================================================
# 2. Normaler Rundlauf - geparste Daten identisch
# ==========================================================================

abschnitt("Rundlauf - normaler Spielstand")

DATEN = {
    "siedlung": "Nebelseetal",
    "tag": 7,
    "resources": {"holz": 100.5, "stein": 42, "mana": 0},
    "flags": [True, False, None],
    "einheiten": {"Schwert": 3, "Bogen": 2},
    "notiz": "Alles in Ordnung",
}
P1 = pfad("rundlauf.json")

ok, meldung = SP.speichere(DATEN, P1)
check("speichere() meldet Erfolg", ok is True, meldung)
check("die Meldung ist ein nicht-leerer Text", bool(meldung) and isinstance(meldung, str))
check("die Zieldatei existiert danach", gibt_es(P1), P1)
check("nach dem Speichern bleibt KEINE .tmp liegen", not gibt_es(P1 + ".tmp"))

geladen, meldung2 = SP.lade(P1)
check("lade() liefert ein dict", isinstance(geladen, dict), str(type(geladen)))
check("die geparsten Daten sind identisch mit den gespeicherten", geladen == DATEN)
check("lade() meldet 'in Ordnung'", meldung2 == "in Ordnung", meldung2)
check("die Rohdatei ist gueltiges JSON", json.loads(roh(P1)) == DATEN)

_p = SP.pruefe_datei(P1)
check("pruefe_datei kennt genau die geforderten Schluessel",
      set(_p) == {"existiert", "groesse", "lesbar", "json_ok", "stand"}, str(sorted(_p)))
check("pruefe_datei: existiert = Wahr", _p["existiert"] is True)
check("pruefe_datei: lesbar = Wahr", _p["lesbar"] is True)
check("pruefe_datei: json_ok = Wahr", _p["json_ok"] is True)
check("pruefe_datei: groesse groesser 0", _p["groesse"] > 0, str(_p["groesse"]))
check("pruefe_datei: stand ist ein Text", isinstance(_p["stand"], str), str(_p["stand"]))
check("pruefe_datei: stand nennt den Zustand 'in Ordnung'", "in Ordnung" in _p["stand"])

# Zweiter Rundlauf auf denselben Pfad: ueberschreiben muss klappen.
DATEN2 = dict(DATEN, tag=8)
ok2, _ = SP.speichere(DATEN2, P1)
neu, _ = SP.lade(P1)
check("erneutes Speichern ueberschreibt sauber", ok2 is True and neu == DATEN2)
check("nach dem Ueberschreiben liegt wieder keine .tmp", not gibt_es(P1 + ".tmp"))


# ==========================================================================
# 3. Umlaute und verschachtelte Listen ueberstehen den Rundlauf
# ==========================================================================

abschnitt("Umlaute und verschachtelte Listen")

UMDATEN = {
    "name": "Nebelwölfe",
    "gruss": "Grüße aus dem Süden",
    "strasse": "Straße",
    "karte": {
        "raster": ["wald", "berg", "nebelsee"],
        "listen": [[1, 2], [3, [4, "ö"]]],
        "tief": {"a": [{"b": ["ü", "ä", "ß"]}]},
    },
}
P2 = pfad("umlaut.json")
ok3, m3 = SP.speichere(UMDATEN, P2)
check("Umlaut-Datensatz speichert", ok3 is True, m3)
_zurueck, _ = SP.lade(P2)
check("Umlaute ueberstehen den Rundlauf unveraendert", _zurueck == UMDATEN)
check("der Name mit Umlaut stimmt", _zurueck["name"] == "Nebelwölfe")
check("die verschachtelte Liste stimmt", _zurueck["karte"]["listen"] == [[1, 2], [3, [4, "ö"]]])
check("die tiefe Struktur mit Umlauten stimmt",
      _zurueck["karte"]["tief"] == {"a": [{"b": ["ü", "ä", "ß"]}]})
check("Umlaute stehen lesbar in der Datei (ensure_ascii=False)", "ö" in roh(P2))
check("kein \\u-Escape im Umlaut-Feld", "\\u00f6" not in roh(P2))


# ==========================================================================
# 4. Scheiternde Serialisierung laesst die ALTE Datei unberuehrt
# ==========================================================================

abschnitt("Scheiternde Serialisierung - alte Datei bleibt unangetastet")

class Krach(dict):
    """Ein dict, dessen Serialisierung mitten im Lauf eine Ausnahme wirft."""

    def items(self):
        raise RuntimeError("kaputt beim Serialisieren")


P3 = pfad("serial.json")
ALTDATEN = {"stand": "alt", "wert": 1}
ok_alt, _ = SP.speichere(ALTDATEN, P3)
check("alte Datei liegt vor dem Fehlversuch", ok_alt is True and gibt_es(P3))
alt_bytes = roh(P3)

ok_bad, meld_bad = SP.speichere(Krach(stand="neu"), P3)
check("speichere() meldet bei schreiender Serialisierung ehrlich Fehlschlag", ok_bad is False)
check("die Meldung nennt die Serialisierung", "Serialisierung" in meld_bad, meld_bad)
check("die alte Datei ist bytegleich unveraendert", roh(P3) == alt_bytes)
_alt_zurueck, _ = SP.lade(P3)
check("die alte Datei laedt weiterhin ihren alten Inhalt", _alt_zurueck == ALTDATEN)
check("nach dem Fehlschlag liegt keine .tmp herum", not gibt_es(P3 + ".tmp"))

# Ein nicht serialisierbarer Wert (Menge) muss ebenfalls ehrlich abgelehnt werden.
ok_set, meld_set = SP.speichere({"menge": {1, 2, 3}}, P3)
check("eine nicht serialisierbare Menge wird abgelehnt", ok_set is False)
check("die Menge-Meldung ist ein Text", isinstance(meld_set, str) and bool(meld_set))
check("die alte Datei blieb auch beim Mengen-Fehler gleich", roh(P3) == alt_bytes)

# Ein unmoeglicher Zielpfad darf nicht werfen, sondern melden.
P3B = os.path.join(ORDNER, "gibtesnicht", "tief.json")
ok_ort, meld_ort = SP.speichere({"a": 1}, P3B)
check("ein unmoeglicher Zielordner wird ehrlich abgelehnt", ok_ort is False)
check("und die Zieldatei entsteht dabei nicht", not gibt_es(P3B))


# ==========================================================================
# 5. Kaputtes JSON wird ehrlich gemeldet statt zu werfen
# ==========================================================================

abschnitt("Kaputtes JSON - ehrliche Meldung, kein Absturz")

P4 = pfad("kaputt.json")
with open(P4, "w", encoding="utf-8") as f:
    f.write("{ das ist kein json ")
check("kaputte Datei liegt vor", gibt_es(P4))

try:
    _d, _m = SP.lade(P4)
    check("lade() wirft bei kaputtem JSON NICHT", True)
except Exception as e:                                    # pragma: no cover
    check("lade() wirft bei kaputtem JSON NICHT", False, repr(e))
    _d, _m = None, ""
check("lade() liefert None als Daten", _d is None)
check("lade() liefert einen nicht-leeren Grund als Text", isinstance(_m, str) and bool(_m), _m)
check("der Grund nennt die Beschaedigung", "beschaedigt" in _m or "JSON" in _m, _m)

_pk = SP.pruefe_datei(P4)
check("pruefe_datei: die kaputte Datei existiert", _pk["existiert"] is True)
check("pruefe_datei: sie ist lesbar (nur der Inhalt ist kaputt)", _pk["lesbar"] is True)
check("pruefe_datei: json_ok ist Unwahr", _pk["json_ok"] is False)
check("pruefe_datei: stand nennt die Beschaedigung", "beschaedigt" in _pk["stand"],
      _pk["stand"])


# ==========================================================================
# 6. Fehlende Datei wird ehrlich gemeldet
# ==========================================================================

abschnitt("Fehlende Datei - keine Ausnahme, klare Meldung")

P5 = pfad("fehlt.json")
check("die Datei gibt es wirklich nicht", not gibt_es(P5))
try:
    _df, _mf = SP.lade(P5)
    check("lade() wirft bei fehlender Datei NICHT", True)
except Exception as e:                                    # pragma: no cover
    check("lade() wirft bei fehlender Datei NICHT", False, repr(e))
    _df, _mf = None, ""
check("lade() liefert None bei fehlender Datei", _df is None)
check("lade() nennt einen Grund", isinstance(_mf, str) and bool(_mf), _mf)

_pf = SP.pruefe_datei(P5)
check("pruefe_datei: existiert = Unwahr bei fehlender Datei", _pf["existiert"] is False)
check("pruefe_datei: groesse = 0 bei fehlender Datei", _pf["groesse"] == 0)
check("pruefe_datei: json_ok = Unwahr bei fehlender Datei", _pf["json_ok"] is False)
check("pruefe_datei: stand ist trotzdem ein Text", isinstance(_pf["stand"], str))


# ==========================================================================
# 7. .bak VOR dem Ueberschreiben - und wiederherstellen()
# ==========================================================================

abschnitt("Sicherung .bak und Wiederherstellung")

P6 = pfad("bak.json")
V1 = {"spiel": "Version 1", "tag": 1, "rohstoffe": {"holz": 10}}
V2 = {"spiel": "Version 2", "tag": 2, "rohstoffe": {"holz": 20}}

ok_v1, _ = SP.speichere(V1, P6)
check("Version 1 wurde gespeichert", ok_v1 is True)

ok_bak, meld_bak = SP.sichere_kopie(P6)
check("sichere_kopie() meldet Erfolg", ok_bak is True, meld_bak)
check("die Sicherung .bak existiert", gibt_es(P6 + ".bak"))
check("die Sicherung enthaelt Version 1", SP.lade(P6 + ".bak")[0] == V1)

# Jetzt ueberschreiben - die Sicherung darf sich NICHT aendern.
ok_v2, _ = SP.speichere(V2, P6)
check("Version 2 ueberschreibt die Datei", ok_v2 is True)
check("die Datei traegt jetzt Version 2", SP.lade(P6)[0] == V2)
check("die Sicherung traegt weiterhin Version 1 (vor dem Ueberschreiben)",
      SP.lade(P6 + ".bak")[0] == V1)

# Kaputt machen, dann wiederherstellen.
with open(P6, "w", encoding="utf-8") as f:
    f.write("{} kaputt")
check("die Hauptdatei ist nun kaputt", SP.pruefe_datei(P6)["json_ok"] is False)

ok_rest, meld_rest = SP.wiederherstellen(P6)
check("wiederherstellen() meldet Erfolg", ok_rest is True, meld_rest)
check("die Meldung nennt die Sicherung .bak", ".bak" in meld_rest, meld_rest)
check("nach der Wiederherstellung traegt die Datei wieder Version 1", SP.lade(P6)[0] == V1)
check("die wiederhergestellte Datei ist gueltiges JSON",
      SP.pruefe_datei(P6)["json_ok"] is True)
check("die Wiederherstellung laesst keine .tmp liegen", not gibt_es(P6 + ".tmp"))


# ==========================================================================
# 8. Aufraeumen - liegengebliebene .tmp-Dateien
# ==========================================================================

abschnitt("Aufraeumen - liegengebliebene Zwischendateien")

P7 = pfad("tmpraum.json")
SP.speichere({"x": 1}, P7)
# Ein abgebrochener Lauf simuliert zwei Reste:
_rest1 = P7 + ".tmp"
_rest2 = P7 + ".abgebrochen.tmp"
with open(_rest1, "w", encoding="utf-8") as f:
    f.write("halb")
with open(_rest2, "w", encoding="utf-8") as f:
    f.write("auch halb")
# Eine fremde Datei, die NICHT angetastet werden darf:
_fremd = pfad("tmpraum_anderes.json")
with open(_fremd, "w", encoding="utf-8") as f:
    f.write("{}")

check("die Reste .tmp liegen vor", gibt_es(_rest1) and gibt_es(_rest2))
_entfernt = SP.aufraeumen(P7)
check("aufraeumen() liefert eine Liste", isinstance(_entfernt, list), str(type(_entfernt)))
check("aufraeumen() meldet beide entfernten Reste", len(_entfernt) == 2, str(_entfernt))
check("die .tmp-Reste sind danach weg", not gibt_es(_rest1) and not gibt_es(_rest2))
check("die Zieldatei selbst bleibt erhalten", gibt_es(P7))
check("die Zieldatei ist danach weiterhin lesbar", SP.lade(P7)[0] == {"x": 1})
check("eine fremde Datei wird nicht angetastet", gibt_es(_fremd))

_keine = SP.aufraeumen(P7)
check("ein zweiter Aufraeumlauf findet nichts mehr", _keine == [], str(_keine))


# ==========================================================================
# 9. Sicherung/Wiederherstellung ohne Vorlage - ehrlich statt Absturz
# ==========================================================================

abschnitt("Ohne Vorlage - ehrliche Ablehnung")

P8 = pfad("ohne.json")
check("ohne Datei gibt es nichts zu sichern", not gibt_es(P8))
_ok_s, _m_s = SP.sichere_kopie(P8)
check("sichere_kopie() ohne Datei meldet Fehlschlag", _ok_s is False, _m_s)
check("sichere_kopie() legt dabei keine .bak an", not gibt_es(P8 + ".bak"))

_ok_w, _m_w = SP.wiederherstellen(P8)
check("wiederherstellen() ohne .bak meldet Fehlschlag", _ok_w is False, _m_w)
check("wiederherstellen() legt ohne Vorlage keine Datei an", not gibt_es(P8))

# .bak ohne .tmp-Rest: aufraeumen faellt die .bak nicht an.
SP.speichere({"a": 1}, P8)
SP.sichere_kopie(P8)
SP.aufraeumen(P8)
check("aufraeumen() laesst die .bak-Sicherung unangetastet", gibt_es(P8 + ".bak"))


# ==========================================================================
# 10. Abschluss - ehrliche Luecken benannt, Bericht ausgeben
# ==========================================================================

abschnitt("Ehrliche Luecken des Verfahrens")

check("offene_luecken() ist keine leere Behauptung", bool(_luecken))
for _k in sorted(_luecken):
    befund(f"Grenze: {_k}", _luecken[_k][:90])

sys.exit(bericht())
