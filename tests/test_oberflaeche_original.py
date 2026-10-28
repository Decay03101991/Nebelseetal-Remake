"""
Menue-Vergleich Original gegen Spiel (Paket W7, 04.10.2026).

Prueft `src/oberflaeche_original.py` gegen das belegte Original-Menue
(archiv/analysen/audits/astra_gamestar_antwort.txt, Screenshot 1838855) und gegen das
laufende Menue in `src/main.py`. Beweist ausdruecklich:

  * das Original hat die belegten Eintraege in der belegten Reihenfolge,
  * offline_menue() laesst GENAU die vier Netz-Eintraege weg,
  * aktuelles_menue() liest main.py wirklich als TEXT - die Pruefdatei liest
    MENU_ITEMS SELBST mit einem eigenen Muster und vergleicht auf Gleichheit,
  * fehlend()/zusaetzlich() finden echte Abweichungen und benennen sie,
  * reihenfolge_abweichungen() findet mindestens eine echte Reihenfolge-Abweichung,
  * abweichungsbericht() ist lesbarer Text.

Aufruf:  python -X utf8 tests/test_oberflaeche_original.py
"""
from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

ROOT, SRC = import_src()
import oberflaeche_original as O

# Die belegte Originalreihenfolge, woertlich (ASCII-Transliteration des Umlauts).
BELEGT = [
    "Uebersicht", "Portal", "Diplomatie", "Einstellungen", "Ruhmeshalle",
    "Gildenhalle", "Voraussetzungen", "Nachrichten", "Neuigkeiten", "Anleitung",
    "Schlachtsimulator", "Forum", "Chat", "Spieler werben", "Logout",
]
NETZ = ["Forum", "Chat", "Spieler werben", "Logout"]
OFFLINE_SOLL = [n for n in BELEGT if n not in NETZ]

MUSTER = re.compile(r"MENU_ITEMS\s*=\s*\[(.*?)\]", re.DOTALL)


def haupttext():
    return open(os.path.join(SRC, "main.py"), "r", encoding="utf-8").read()


def selbst_geparst():
    """Die Pruefdatei liest MENU_ITEMS SELBST - Beweis, dass das Modul es auch so macht."""
    treffer = MUSTER.search(haupttext())
    if not treffer:
        return []
    return re.findall(r"\"([^\"]+)\"", treffer.group(1))


# ==========================================================================
# 1. Original-Menue - belegte Eintraege in belegter Reihenfolge
# ==========================================================================

abschnitt("1. Original-Menue - belegte Reihenfolge")

_orig = O.original_menue()
check("original_menue() liefert eine Liste", isinstance(_orig, list), str(type(_orig)))
check("das Original hat 15 Eintraege", len(_orig) == 15, f"{len(_orig)}")

_orig_namen = [e["name"] for e in _orig]
check("die Originalreihenfolge ist woertlich die belegte", _orig_namen == BELEGT, str(_orig_namen))
check("erster Eintrag ist Uebersicht", _orig_namen[0] == "Uebersicht", _orig_namen[0])
check("letzter Eintrag ist Logout", _orig_namen[-1] == "Logout", _orig_namen[-1])
check("die Nummern laufen 1 bis 15", [e["reihenfolge"] for e in _orig] == list(range(1, 16)),
      str([e["reihenfolge"] for e in _orig]))

check("jeder Eintrag hat name, reihenfolge, quelle, offline",
      all({"name", "reihenfolge", "quelle", "offline"} <= set(e) for e in _orig))
check("jeder Eintrag nennt eine Quelle",
      all(bool(e.get("quelle")) for e in _orig))
check("das Offline-Kennzeichen ist ein Wahrheitswert",
      all(isinstance(e.get("offline"), bool) for e in _orig))

# ==========================================================================
# 2. Offline-Regel - genau die vier Netz-Eintraege fallen weg
# ==========================================================================

abschnitt("2. Offline-Regel - genau vier Netz-Eintraege weg")

_offline_namen = [e["name"] for e in _orig if e["offline"]]
check("genau vier Eintraege sind als Netz gekennzeichnet",
      sum(1 for e in _orig if not e["offline"]) == 4,
      str([e["name"] for e in _orig if not e["offline"]]))
check("die vier Netz-Eintraege sind Forum, Chat, Spieler werben, Logout",
      sorted(e["name"] for e in _orig if not e["offline"]) == sorted(NETZ),
      str([e["name"] for e in _orig if not e["offline"]]))
check("jeder Netz-Eintrag nennt einen Grund",
      all(bool(e.get("grund")) for e in _orig if not e["offline"]))

check("netz_eintraege() nennt genau die vier", sorted(O.netz_eintraege()) == sorted(NETZ),
      str(O.netz_eintraege()))

_off = O.offline_menue()
check("offline_menue() liefert eine Liste", isinstance(_off, list))
check("offline_menue() hat 15 minus 4 = 11 Eintraege", len(_off) == 11, f"{len(_off)}")
check("offline_menue() ist genau das Original ohne die vier Netz-Eintraege",
      _off == OFFLINE_SOLL, str(_off))
check("offline_menue() enthaelt keinen der vier Netz-Eintraege",
      not any(n in _off for n in NETZ), str(_off))
check("offline_menue() beginnt mit Uebersicht", _off[0] == "Uebersicht", _off[0])
check("offline_menue() endet mit Schlachtsimulator", _off[-1] == "Schlachtsimulator", _off[-1])

# ==========================================================================
# 3. aktuelles_menue() liest main.py wirklich als TEXT
# ==========================================================================

abschnitt("3. aktuelles_menue() liest main.py als TEXT")

_akt = O.aktuelles_menue()
check("aktuelles_menue() liefert eine Liste", isinstance(_akt, list))
check("aktuelles_menue() ist nicht leer", len(_akt) > 0, f"{len(_akt)}")

_eigene = selbst_geparst()
check("das Modul liefert genau das, was die Pruefdatei selbst aus main.py liest",
      _akt == _eigene, f"Modul {_akt} vs Pruefdatei {_eigene}")
check("die selbst gelesene Liste hat 17 Eintraege", len(_eigene) == 17, f"{len(_eigene)}")
check("das Spiel fuehrt Dorfzentrum", "Dorfzentrum" in _akt)
check("das Spiel fuehrt Spieler werben", "Spieler werben" in _akt)
check("das Spiel fuehrt NICHT Uebersicht - Beweis, dass es wirklich main.py ist",
      "Uebersicht" not in _akt)

_modultext = open(os.path.join(SRC, "oberflaeche_original.py"), "r", encoding="utf-8").read()
check("das Modul importiert main NICHT",
      "import main" not in _modultext and "from main" not in _modultext)
check("das Modul benutzt kein tkinter (kein Import, ein Wort in der Beschreibung zaehlt nicht)",
      "import tkinter" not in _modultext and "from tkinter" not in _modultext)

# ==========================================================================
# 4. fehlend() - echte Fehlstellen benennen
# ==========================================================================

abschnitt("4. fehlend() - echte Fehlstellen benennen")

_fehlt = O.fehlend()
check("fehlend() liefert eine Liste", isinstance(_fehlt, list))
check("fehlend() findet echte Fehlstellen", len(_fehlt) >= 3, f"{len(_fehlt)}")
check("fehlend() benennt Uebersicht", "Uebersicht" in _fehlt, str(_fehlt))
check("fehlend() benennt Gildenhalle", "Gildenhalle" in _fehlt, str(_fehlt))
check("fehlend() benennt Voraussetzungen", "Voraussetzungen" in _fehlt, str(_fehlt))
check("fehlend() benennt Neuigkeiten", "Neuigkeiten" in _fehlt, str(_fehlt))
check("fehlend() benennt Schlachtsimulator", "Schlachtsimulator" in _fehlt, str(_fehlt))
check("fehlend() meldet Nachrichten NICHT (das Spiel hat es)",
      "Nachrichten" not in _fehlt)
check("jede Fehlstelle steht im Offline-Soll und fehlt im Spiel",
      all(n in OFFLINE_SOLL and n not in _akt for n in _fehlt), str(_fehlt))

# ==========================================================================
# 5. zusaetzlich() - echte Zusaetze benennen
# ==========================================================================

abschnitt("5. zusaetzlich() - echte Zusaetze benennen")

_zuviel = O.zusaetzlich()
check("zusaetzlich() liefert eine Liste", isinstance(_zuviel, list))
check("zusaetzlich() findet echte Zusaetze", len(_zuviel) >= 3, f"{len(_zuviel)}")
check("zusaetzlich() benennt Dorfzentrum", "Dorfzentrum" in _zuviel, str(_zuviel))
check("zusaetzlich() benennt Lager", "Lager" in _zuviel, str(_zuviel))
check("zusaetzlich() benennt Kaserne", "Kaserne" in _zuviel, str(_zuviel))
check("zusaetzlich() benennt die Netz-Eintraege Forum/Chat/Spieler werben",
      all(n in _zuviel for n in ("Forum", "Chat", "Spieler werben")), str(_zuviel))
check("zusaetzlich() meldet Portal NICHT (das Spiel hat es)", "Portal" not in _zuviel)
check("jeder Zusatz steht im Spiel und nicht im Offline-Soll",
      all(n in _akt and n not in OFFLINE_SOLL for n in _zuviel), str(_zuviel))

# ==========================================================================
# 6. reihenfolge_abweichungen() - echte Reihenfolge-Abweichung
# ==========================================================================

abschnitt("6. reihenfolge_abweichungen() - echte Reihenfolge-Abweichung")

_reihe = O.reihenfolge_abweichungen()
check("reihenfolge_abweichungen() liefert eine Liste", isinstance(_reihe, list))
check("es gibt mindestens eine echte Reihenfolge-Abweichung", len(_reihe) >= 1,
      f"{len(_reihe)}")
check("Nachrichten steht in einem anderen Rang als im Original",
      any(e["name"] == "Nachrichten" for e in _reihe), str(_reihe))
check("jede Abweichung hat name, soll_stelle, ist_stelle",
      all({"name", "soll_stelle", "ist_stelle"} <= set(e) for e in _reihe))
check("soll_stelle und ist_stelle unterscheiden sich wirklich",
      all(e["soll_stelle"] != e["ist_stelle"] for e in _reihe))
check("jede genannte Abweichung ist ein gemeinsamer Eintrag",
      all(e["name"] in OFFLINE_SOLL and e["name"] in _akt for e in _reihe), str(_reihe))

# ==========================================================================
# 7. punktezeile()
# ==========================================================================

abschnitt("7. punktezeile() - linker Statusblock des Originals")

_punkte = O.punktezeile()
check("punktezeile() liefert ein Verzeichnis", isinstance(_punkte, dict))
check("die Punktezeile heisst Eure Punkte", _punkte.get("titel") == "Eure Punkte",
      str(_punkte.get("titel")))
check("die Punktezeile nennt Forschung, Krieg, Gesamt in dieser Folge",
      _punkte.get("zeilen") == ["Forschung", "Krieg", "Gesamt"], str(_punkte.get("zeilen")))
check("darunter steht Laufende Auftraege:",
      "Laufende Auftraege" in str(_punkte.get("darunter", "")), str(_punkte.get("darunter")))
check("die Punktezeile nennt eine Quelle", bool(_punkte.get("quelle")))

# ==========================================================================
# 8. abweichungsbericht() - lesbarer Text
# ==========================================================================

abschnitt("8. abweichungsbericht() - lesbarer Text")

_bericht = O.abweichungsbericht()
check("abweichungsbericht() liefert eine Zeichenkette", isinstance(_bericht, str))
check("der Bericht ist nicht leer", len(_bericht) > 100, f"{len(_bericht)} Zeichen")
check("der Bericht ist mehrzeilig (lesbar)", _bericht.count("\n") >= 6,
      f"{_bericht.count(chr(10))} Zeilenumbrueche")
check("der Bericht nennt die fehlenden Eintraege", "Uebersicht" in _bericht)
check("der Bericht nennt die Netz-Eintraege", "Forum" in _bericht)
check("der Bericht nennt die Reihenfolge-Abweichung", "Nachrichten" in _bericht)
check("der Bericht nennt die Punktezeile", "Eure Punkte" in _bericht
      and "Laufende Auftraege" in _bericht)
check("der Bericht fasst die zusaetzlichen Eintraege zusammen",
      "Dorfzentrum" in _bericht, _bericht[:200])

sys.exit(bericht())
