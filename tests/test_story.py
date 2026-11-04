# -*- coding: ascii -*-
"""Wache Story 1: Intro, Chronik, Sieg- und Niederlagentext (04.11.2026).

WARUM
-----
Die externe Projektpruefung hat als dritten Kernbefund gemessen: das Spiel hat keine Geschichte -
ein Neuling findet nach zehn Minuten nur Zahlen. Daniels Entscheidungen dazu (04.11.2026): Ton
abenteuerlich und leicht, EIN Intro nach dem Passworttor, Chronik im Berater, die mit dem Fortschritt
waechst, und spaeter sprechende Bots (Story 2).

Was diese Datei beweist
-----------------------
1. Die Texte stehen in `data/story.json`, NICHT im Code (dieselbe Regel wie fuer jede andere Zahl).
2. Das Intro hat vier Absaetze mit echtem Deutsch (Umlaute, kein ASCII-Ersatz) und einen Titel.
3. Die Chronik waechst mit dem Fortschritt: Stufe 0 ohne Siedlung, 1 mit Siedlung, 2 mit Ware oder
   Werkstatt, 3 mit Forschung, 4 mit Kampf, 5 mit zweiter Siedlung, 6 mit zweiter Welt - und sie
   geht nie zurueck.
4. Sieg und Niederlage haben eigene Texte.
5. Das Intro erscheint EINMAL je Installation (Merker neben dem Spielstand), nicht je Spielstand.
6. Der Berater kennt die Rubrik Geschichte und gibt die Chronik aus.
7. Quellwache: `main` zeigt das Intro nach dem Aufbau der Oberflaeche, und im Code steht kein
   Storytext (kein doppeltes Gedaechtnis).

Aufruf:  python -X utf8 tests/test_story.py
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
import berater  # noqa: E402
import story  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
TEXT_BERATER = open(os.path.join(SRC, "berater.py"), encoding="utf-8").read()
ROHDATEN = open(os.path.join(ROOT, "data", "story.json"), encoding="utf-8").read()
DATEN = json.loads(ROHDATEN)

# ==========================================================================
abschnitt("1. Die Texte stehen in der Datendatei, nicht im Code")
check("1 data/story.json ist lesbar und ein Verzeichnis", isinstance(DATEN, dict) and bool(DATEN), "")
check("1 die Datei nennt den Ton (Daniels Entscheidung)", "abenteuerlich" in str(DATEN.get("ton")), "")
check("1 es gibt vier Intro-Absaetze", len(DATEN.get("intro") or []) == 4, str(len(DATEN.get("intro") or [])))
check("1 jeder Absatz ist ein echter Satz", all(len(str(z)) > 40 for z in (DATEN.get("intro") or [])), "")
check("1 die Chronik hat sieben Stufen (0 bis 6)", len(DATEN.get("chronik") or []) == 7,
      str(len(DATEN.get("chronik") or [])))
check("1 Sieg und Niederlage sind getrennt hinterlegt",
      bool((DATEN.get("sieg") or {}).get("text")) and bool((DATEN.get("niederlage") or {}).get("text")), "")

# Echte deutsche Anzeigetexte: Umlaute MUESSEN vorkommen (im Code waeren sie verboten, hier Pflicht).
umlaute = [chr(228), chr(246), chr(252), chr(223)]           # ae, oe, ue, ss
check("1 die Texte tragen echte Umlaute (Anzeigetext, kein ASCII-Ersatz)",
      any(z in ROHDATEN for z in umlaute), "keiner der vier Umlaute gefunden")
check("1 kein ASCII-Ersatz mehr im Text", "Doerfer" not in ROHDATEN and "Fuenf" not in ROHDATEN, "")

# ==========================================================================
abschnitt("2. intro() und intro_titel() liefern den Text")
text = story.intro()
check("2 intro() ist nicht leer", bool(text), "")
check("2 intro() hat vier durch Leerzeile getrennte Absaetze", text.count("\n\n") == 3, str(text.count("\n\n")))
check("2 intro_titel() ist gesetzt", bool(story.intro_titel()), story.intro_titel())
check("2 das Intro nennt die sechs Welten oder die Nachbarn",
      ("Limbus" in text and "Midgard" in text) and ("Haug" in text), "")

# ==========================================================================
abschnitt("3. Die Chronik waechst mit dem Fortschritt")
leer = story.chronik({})
check("3 ohne Siedlung nur Kapitel 0", len(leer) == 1, str(len(leer)))
eins = story.chronik({"siedlungen": 1})
check("3 mit einer Siedlung zwei Kapitel", len(eins) == 2, str(len(eins)))
zwei = story.chronik({"siedlungen": 1, "waren": 1})
check("3 mit einer Ware drei Kapitel", len(zwei) == 3, str(len(zwei)))
drei = story.chronik({"siedlungen": 1, "waren": 1, "forschungen": 1})
check("3 mit Forschung vier Kapitel", len(drei) == 4, str(len(drei)))
vier = story.chronik({"siedlungen": 1, "waren": 1, "forschungen": 1, "kaempfe": 1})
check("3 mit einem Kampf fuenf Kapitel", len(vier) == 5, str(len(vier)))
fuenf = story.chronik({"siedlungen": 2, "welten": 1})
check("3 mit zwei Siedlungen sechs Kapitel", len(fuenf) == 6, str(len(fuenf)))
sechs = story.chronik({"siedlungen": 2, "welten": 2})
check("3 mit zwei Welten alle sieben Kapitel", len(sechs) == 7, str(len(sechs)))
check("3 die Kapitel sind der Reihe nach", [k["stufe"] for k in sechs] == [str(i) for i in range(7)],
      str([k["stufe"] for k in sechs]))
check("3 kein Kapitel ohne Titel und Text",
      all(k["titel"] and k["text"] for k in sechs), "")
check("3 ein kaputter Zustand stuerzt nicht ab", isinstance(story.chronik({"siedlungen": "viel"}), list), "")

# ==========================================================================
abschnitt("4. Sieg und Niederlage")
sieg = story.ausgang_text(True)
niederlage = story.ausgang_text(False)
check("4 der Siegtext ist gesetzt", bool(sieg.get("titel")) and bool(sieg.get("text")), str(sieg)[:60])
check("4 der Niederlagentext ist gesetzt", bool(niederlage.get("titel")) and bool(niederlage.get("text")),
      str(niederlage)[:60])
check("4 beide Texte sind verschieden", sieg != niederlage, "")

# ==========================================================================
abschnitt("5. Das Intro erscheint EINMAL je Installation")
ordner = tempfile.mkdtemp(prefix="story_wache_")
merk = os.path.join(ordner, "geschichte.json")
original_merk = story._merkdatei
story._merkdatei = lambda: merk                     # Merker in den Zwischenspeicher umlenken
try:
    check("5 ohne Merker ist das Intro noch nicht gesehen", story.intro_gesehen() is False, "")
    story.intro_merken()
    check("5 nach dem Merken ist es gesehen", story.intro_gesehen() is True, "")
    check("5 der Merker liegt als eigene Datei neben dem Spielstand", os.path.exists(merk), merk)
finally:
    story._merkdatei = original_merk               # echte Funktion zurueck
    try:
        os.remove(merk)
        os.rmdir(ordner)
    except OSError:
        pass

# ==========================================================================
abschnitt("6. Der Berater kennt die Chronik")
antwort_leer = berater.antwort("erzaehl mir die geschichte")
check("6 der Berater antwortet auf 'geschichte'", "Chronik" in antwort_leer, antwort_leer[:80])
check("6 die Antwort nennt das erste Kapitel", "Ankunft" in antwort_leer, "")
check("6 ohne Spielzustand kommt kein Absturz", isinstance(berater.antwort("chronik"), str), "")


class _Forschung:                                    # winziger Ersatz fuer einen Forschungsstand
    def __init__(self, level):
        self.level = level


class _Zustand:                                      # winziger Ersatz fuer den Spielzustand
    settlements = [1, 2]
    research = {"baukunst": _Forschung(2)}
    eigene_dimensionen = [4]
    kaempfe_gesamt = 0


antwort_voll = berater.antwort("geschichte", _Zustand())
check("6 mit Fortschritt nennt die Antwort mehr Kapitel",
      antwort_voll.count(":") >= antwort_leer.count(":") + 3, str(antwort_voll.count(":")))

# ==========================================================================
abschnitt("7. Quellwache: der Anschluss ist im Code, der Text nicht")
check("7 main.py zeigt das Intro nach dem Aufbau der Oberflaeche",
      "self.root.after(400, self._geschichte_intro_zeigen)" in TEXT_MAIN, "")
check("7 die Intro-Methode nutzt den Merker", "story.intro_merken()" in TEXT_MAIN, "")
check("7 die Intro-Methode prueft, ob es schon gezeigt wurde", "story.intro_gesehen()" in TEXT_MAIN, "")
check("7 das Intro laeuft ueber den Ingame-Dialog (Overlay), kein eigenes Fenster",
      "self._overlay_oeffnen(story.intro_titel(), bauer)" in TEXT_MAIN, "")
check("7 der Berater fragt die Chronik in story.py ab", "story.chronik(" in TEXT_BERATER, "")
erste_zeile = str((DATEN.get("intro") or [""])[0])[:40]
check("7 der erste Intro-Satz steht NICHT im Code (kein zweites Gedaechtnis)", erste_zeile not in TEXT_MAIN,
      erste_zeile)

sys.exit(bericht())
