# -*- coding: ascii -*-
"""Die sechs Fraktionen (Voelker) als eigene Datenschicht - Lesen, Pruefen, Verteilen (A2, 03.11.2026).

Warum ein eigenes Modul: `bottaktik.py` ist reine Logik (eine Wache verbietet dort jedes `open(`).
Die Werte gehoeren aber in eine Datendatei, nicht in den Code ("keine Zahl ohne Quelle"). Also liest
DIESES Modul `data/voelker.json`, und `bottaktik` fragt hier nach - eine Quelle, zwei Zustaendigkeiten.

Entscheidung Daniel 03.11.2026: "Mit Voelker sind die Fraktionen gemeint, Menschlich, Zwergisch,
Elfisch, Trolle, Ghule, Gnome dann haben wir 6 Fraktionen" und "Trolle Ghule und Gnome ersetzen die
Monster". Trolle uebernehmen das Paar der frueheren Fraktion "monster" (AT +5 % / Handelserloes -5 %);
Ghule und Gnome tragen Daniels eigene Werte.
"""
from __future__ import annotations

import json
import os

# Der alte Satz aus `bottaktik.py` - er gilt nur, wenn die Datendatei fehlt oder kaputt ist. So bleibt
# das Spiel bedienbar, und keine Pruefung stuerzt an einer fehlenden Datei ab.
RUECKFALL = [
    {"kennung": "menschlich", "plus": "Holzertrag +5 %", "minus": "Steinertrag -5 %",
     "beschreibung": "", "quelle": "bottaktik.py (Rueckfall)"},
    {"kennung": "zwergisch", "plus": "Steinertrag +5 %", "minus": "Holzertrag -5 %",
     "beschreibung": "", "quelle": "bottaktik.py (Rueckfall)"},
    {"kennung": "elfisch", "plus": "Reisegeschwindigkeit +5 %", "minus": "PA der Einheiten -5 %",
     "beschreibung": "", "quelle": "bottaktik.py (Rueckfall)"},
    {"kennung": "Trolle", "plus": "AT der Einheiten +5 %", "minus": "Handelserloes -5 %",
     "beschreibung": "", "quelle": "bottaktik.py (Rueckfall)"},
]

DATEI = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "data", "voelker.json")


def lade(pfad: str = None) -> dict:
    """Die Rohdaten der Datendatei (leeres Dict, wenn sie fehlt oder nicht lesbar ist)."""
    ziel = pfad or DATEI
    try:
        with open(ziel, encoding="utf-8") as f:
            daten = json.load(f)
        return daten if isinstance(daten, dict) else {}
    except (OSError, ValueError):
        return {}


def fraktionen(pfad: str = None) -> list:
    """Die Fraktionen in Verteilungsreihenfolge - aus der Datendatei, sonst der alte Satz.

    Jeder Eintrag traegt `kennung`, `plus`, `minus`, `beschreibung` und `quelle`. Es wird nichts
    ergaenzt und nichts erfunden: fehlt ein Feld, bleibt es leer.
    """
    daten = lade(pfad)
    roh = [e for e in (daten.get("fraktionen") or [])
           if isinstance(e, dict) and str(e.get("kennung") or "").strip()]
    if not roh:
        return [dict(e) for e in RUECKFALL]
    return [dict(e) for e in roh]


def kennungen(pfad: str = None) -> list:
    """Nur die Namen der Fraktionen in Verteilungsreihenfolge."""
    return [str(e["kennung"]) for e in fraktionen(pfad)]


def attribute(kennung: str, pfad: str = None) -> dict:
    """Plus und Minus EINER Fraktion; eine unbekannte Fraktion liefert leere Werte."""
    gesucht = str(kennung or "").strip()
    for eintrag in fraktionen(pfad):
        if str(eintrag.get("kennung")) == gesucht:
            return {"plus": str(eintrag.get("plus") or ""), "minus": str(eintrag.get("minus") or "")}
    return {"plus": "", "minus": ""}


def verteile_fraktionen(spieler_fraktion: str, botnamen=None, pfad: str = None) -> dict:
    """Die uebrigen Fraktionen an die Bots verteilen - ohne Doppelung, ohne Wuerfeln.

    Die Bots kommen in Namensreihenfolge dran, die Fraktionen in der Reihenfolge der Datendatei,
    ohne die des Spielers. Bei sechs Fraktionen und fuenf Bots bleibt genau eine uebrig.
    """
    namen = sorted(botnamen or ["Brynhild", "Grom", "Haug", "Krank", "Silra"])
    gewaehlt = str(spieler_fraktion or "").strip()
    reihe = [k for k in kennungen(pfad) if k != gewaehlt]
    return {name: reihe[i] for i, name in enumerate(namen) if i < len(reihe)}
