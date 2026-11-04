# -*- coding: ascii -*-
"""Geschichte des Spiels (Story 1, 04.11.2026).

Alle Texte stehen in `data/story.json` - dieses Modul liest sie nur. Damit gilt dieselbe Regel wie
fuer jede andere Zahl des Spiels: wer die Geschichte aendern will, aendert die Datendatei, nicht den
Code. Vier Aufgaben:

  intro()            - die vier Saetze, die nach dem Passworttor erscheinen (einmalig)
  chronik(zustand)   - die erreichten Kapitel, nach Fortschritt (Berater-Rubrik "Geschichte")
  ausgang_text(sieg) - der Text bei Sieg oder Niederlage
  intro_gesehen()    - wurde das Intro in dieser Installation schon gezeigt?

Die Merkdatei liegt neben dem Spielstand (`schreibordner()/geschichte.json`), nicht im Spielstand:
das Intro soll beim ersten Start EINMAL kommen und nicht bei jedem alten Spielstand erneut.
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List

import spieldaten


def _datei() -> Dict[str, Any]:
    """`data/story.json` lesen (fehlt sie, ist die Geschichte leer - kein erfundener Text)."""
    pfad = os.path.join(spieldaten.projektwurzel(), "data", "story.json")
    try:
        with open(pfad, encoding="utf-8") as f:
            daten = json.load(f)
    except (OSError, ValueError):
        return {}
    return daten if isinstance(daten, dict) else {}


def intro() -> str:
    """Das Intro als EIN Text (Absaetze mit Leerzeile getrennt)."""
    daten = _datei()
    absaetze = [str(z) for z in (daten.get("intro") or []) if str(z).strip()]
    return "\n\n".join(absaetze)


def intro_titel() -> str:
    """Ueberschrift des Intros."""
    return str(_datei().get("intro_titel") or "Ankunft im Nebelseetal")


def _stufe(zustand: Dict[str, Any]) -> int:
    """Bis zu welcher Chronik-Stufe der Spielstand gekommen ist (0 bis 6)."""
    z = zustand if isinstance(zustand, dict) else {}

    def zahl(schluessel: str) -> int:
        try:
            return int(z.get(schluessel) or 0)
        except (TypeError, ValueError):
            return 0

    if zahl("welten") >= 2:                                    # durch ein Portal gegangen
        return 6
    if zahl("siedlungen") >= 2:                                # zweites Dorf
        return 5
    if zahl("kaempfe") >= 1:                                   # erster Kampf
        return 4
    if zahl("forschungen") >= 1:                               # erste Forschung
        return 3
    if zahl("waren") >= 1 or zahl("werkstaetten") >= 1:        # Ware oder Werkstatt
        return 2
    if zahl("siedlungen") >= 1:                                # erste Siedlung
        return 1
    return 0                                                   # gerade angekommen


def chronik(zustand: Dict[str, Any] = None) -> List[Dict[str, str]]:
    """Die erreichten Kapitel als Liste {stufe, titel, text} - aeltestes zuerst."""
    erreicht = _stufe(zustand or {})
    kapitel = []
    for eintrag in (_datei().get("chronik") or []):
        try:
            stufe = int(eintrag.get("stufe", -1))
        except (TypeError, ValueError):
            continue
        if 0 <= stufe <= erreicht:
            kapitel.append({"stufe": str(stufe), "titel": str(eintrag.get("titel") or ""),
                            "text": str(eintrag.get("text") or "")})
    return kapitel


def ausgang_text(sieg: bool) -> Dict[str, str]:
    """Titel und Text bei Sieg (True) oder Niederlage (False)."""
    daten = _datei()
    eintrag = daten.get("sieg" if sieg else "niederlage") or {}
    return {"titel": str(eintrag.get("titel") or ""), "text": str(eintrag.get("text") or "")}


def _merkdatei() -> str:
    """Pfad der Merkdatei neben dem Spielstand."""
    return os.path.join(spieldaten.schreibordner(), "geschichte.json")


def intro_gesehen() -> bool:
    """Wurde das Intro in dieser Installation schon gezeigt?"""
    try:
        with open(_merkdatei(), encoding="utf-8") as f:
            return bool(json.load(f).get("intro_gesehen"))
    except (OSError, ValueError, AttributeError):
        return False


def intro_merken() -> None:
    """Intro als gezeigt eintragen (Fehler beim Schreiben sind nicht toedlich)."""
    try:
        os.makedirs(os.path.dirname(_merkdatei()), exist_ok=True)
        with open(_merkdatei(), "w", encoding="utf-8") as f:
            json.dump({"intro_gesehen": True}, f)
    except OSError:
        pass
