# -*- coding: ascii -*-
"""Stimmen der fuenf Bots (Story 2, 04.11.2026).

Die Texte stehen in `data/bot_stimmen.json`, dieses Modul liest sie nur - dieselbe Regel wie in
`story.py`: wer eine Stimme aendern will, aendert die Datendatei, nicht den Code. Vier Aufgaben:

  zeile(bot, ereignis, rng) - ein Satz des Bots zu einem Ereignis (Angriff, Verteidigung,
                              Gruendung, Beute); fehlt der Eintrag, kommt der neutrale Satz
  texte(bot, ereignis)      - alle Saetze dieses Bots zu diesem Ereignis (Liste, nie None)
  neutral()                 - der neutrale Satz aus der Datei (leer, wenn die Datei fehlt)
  bots()                    - die Bot-Namen, die eine Stimme haben
  ereignisse()              - die Ereignisse, zu denen ein Bot sprechen kann

Grundsatz: NIE ein Absturz. Ein unbekannter Bot, ein unbekanntes Ereignis, eine kaputte oder
fehlende Datei liefern den neutralen Satz (bzw. einen leeren Text) - die Meldung des Spiels
bleibt lesbar, nur ohne Stimme.
"""
from __future__ import annotations

import json
import os
import random
from typing import Any, Dict, List

import spieldaten

EREIGNISSE = ("angriff", "verteidigung", "gruendung", "beute")   # die vier Anlaesse aus Story 2


def _datei() -> Dict[str, Any]:
    """`data/bot_stimmen.json` lesen; fehlt oder bricht sie, kommt ein leeres Verzeichnis zurueck."""
    pfad = os.path.join(spieldaten.projektwurzel(), "data", "bot_stimmen.json")
    try:
        with open(pfad, encoding="utf-8") as f:
            daten = json.load(f)
    except (OSError, ValueError):
        return {}
    return daten if isinstance(daten, dict) else {}


def _bots_block(daten: Dict[str, Any]) -> Dict[str, Any]:
    """Der Block `bots` als Verzeichnis - ein kaputter Block zaehlt als leer."""
    block = daten.get("bots")
    return block if isinstance(block, dict) else {}


def neutral() -> str:
    """Der neutrale Satz, wenn ein Bot zu einem Ereignis nichts sagt."""
    return str(_datei().get("neutral") or "")


def bots() -> List[str]:
    """Die Bot-Namen mit eigener Stimme, alphabetisch."""
    return sorted(str(name) for name in _bots_block(_datei()))


def ereignisse() -> List[str]:
    """Die Ereignisse, zu denen die Bots sprechen koennen."""
    gemeldet = _datei().get("ereignisse")
    if isinstance(gemeldet, list) and gemeldet:            # die Datei darf die Liste fuehren
        return [str(e) for e in gemeldet]
    return list(EREIGNISSE)                                # sonst gilt die feste Reihenfolge


def texte(bot: str, ereignis: str) -> List[str]:
    """Alle Saetze eines Bots zu einem Ereignis - immer eine Liste, nie None.

    Was hinein geht: Bot-Name und Ereignis (beides beliebig, auch unbekannt).
    Was heraus kommt: die hinterlegten Saetze; unbekannter Bot oder unbekanntes Ereignis
    ergeben eine leere Liste, damit der Aufrufer den neutralen Satz nehmen kann.
    """
    eintrag = _bots_block(_datei()).get(str(bot))
    if not isinstance(eintrag, dict):                      # unbekannter Bot
        return []
    saetze = eintrag.get(str(ereignis))
    if not isinstance(saetze, list):                       # Bot kennt dieses Ereignis nicht
        return []
    return [str(s) for s in saetze if str(s).strip()]      # leere Zeilen zaehlen nicht


def zeile(bot: str, ereignis: str, rng: random.Random = None) -> str:
    """EIN Satz des Bots zum Ereignis - zufaellig aus seinen ein bis zwei Saetzen.

    Was hinein geht: Bot-Name, Ereignis und optional ein Zufallsgenerator (fuer pruefbare Laeufe).
    Was heraus kommt: der Satz; gibt es keinen, der neutrale Satz aus der Datendatei.
    """
    saetze = texte(bot, ereignis)
    if not saetze:                                         # kein Eintrag: neutral, nie ein Fehler
        return neutral()
    wahl = rng.choice(saetze) if rng is not None else random.choice(saetze)
    return str(wahl)


def mit_stimme(bot: str, ereignis: str, meldung: str, rng: random.Random = None) -> str:
    """Die Meldung des Spiels mit der Stimme des Bots davor (eine Zeile, dann der Bericht).

    Was hinein geht: Bot-Name, Ereignis und der sachliche Meldungstext (Zahlen, Orte).
    Was heraus kommt: `<Stimme>\\n<meldung>`; fehlt die Stimme, bleibt die Meldung allein -
    der sachliche Teil geht nie verloren.
    """
    stimme = zeile(bot, ereignis, rng)
    if not stimme:                                         # Datendatei fehlt: nur der Bericht
        return str(meldung)
    if not str(meldung).strip():                           # Aufrufer will nur den Satz
        return stimme
    return stimme + "\n" + str(meldung)
