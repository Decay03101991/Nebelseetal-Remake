# -*- coding: utf-8 -*-  # ANZEIGETEXTE tragen echte Umlaute (Schnitt T-1, Daniel 03.11.2026);
#                          Code, Kennungen und Kommentare bleiben ASCII.
"""Die sechs Haeuser der Welt als eigene Datenschicht - Name, Sitz, Farben, Burg und Wappen (W-15).

Warum ein eigenes Modul: Hausname und Wappenbeschreibung sind ANZEIGETEXT, keine Logik. Sie
gehoeren in eine Datendatei, nicht in `main.py` ("keine Zahl ohne Quelle", hier: kein Text ohne
Quelle). `data/haeuser.json` ist die EINE Quelle; die Chronik traegt dieselben Saetze, und
`tests/test_haeuser_wappen.py` belegt, dass beide Fassungen und die Karte dasselbe Wappen zeigen.

Daniels Auftrag 05.11.2026 (woertlich-nah): "Hausnamen und Wappenbeschreibungen auf die
gelieferten Bilder umschreiben." Die Bilder sind seine Lieferung vom 01.11.2026; die frueheren
Beschreibungen nannten Motive, die auf keinem Bild stehen, und einen Helm, den es nicht gibt.

Fehlt die Datei oder ist sie kaputt, kommt ein leeres Dict zurueck - dann zeigt das Spiel den
blossen Voelkernamen und stuerzt nicht ab (dieselbe Regel wie in `voelker.py`).
"""
from __future__ import annotations

import json
import os

DATEI = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "data", "haeuser.json")


def lade(pfad: str = None) -> dict:
    """Die Rohdaten der Hausdatei (leeres Dict, wenn sie fehlt oder nicht lesbar ist)."""
    ziel = pfad or DATEI                                       # ohne Pfad gilt die Projektdatei
    try:
        with open(ziel, encoding="utf-8") as f:                # UTF-8, weil Umlaute im Text stehen
            daten = json.load(f)                               # eine Datei, ein Aufruf
        return daten if isinstance(daten, dict) else {}        # nur ein Dict ist brauchbar
    except (OSError, ValueError):                              # fehlt oder kaputt
        return {}                                              # dann gibt es keine Hausdaten


def alle(pfad: str = None) -> dict:
    """Alle Haeuser als {Fraktionskennung: Angaben} - die eine Lesestelle fuer Anzeigetexte."""
    roh = (lade(pfad) or {}).get("je_haus") or {}              # die Haeuser stehen unter "je_haus"
    return {str(k): v for k, v in roh.items() if isinstance(v, dict)}  # nur echte Eintraege


def haus_von_fraktion(kennung: str, pfad: str = None) -> dict:
    """Die Angaben zu EINER Fraktion (leeres Dict, wenn es dazu kein Haus gibt)."""
    return dict(alle(pfad).get(str(kennung or "").strip(), {}) or {})  # Kopie, nie die Quelle


def hausname(kennung: str, pfad: str = None) -> str:
    """Der Anzeigename des Hauses ('Haus Silberbach') oder ein leerer Text, wenn unbekannt."""
    return str(haus_von_fraktion(kennung, pfad).get("haus") or "").strip()  # nie raten


def wappen(kennung: str, pfad: str = None) -> str:
    """Der Bildpfad des Wappens relativ zur Projektwurzel (leer, wenn unbekannt)."""
    return str(haus_von_fraktion(kennung, pfad).get("wappen") or "").strip()  # Pfad, kein Bild


def wappen_kurz(kennung: str, pfad: str = None) -> str:
    """Die einzeilige Wappenbeschreibung fuer schmale Anzeigen (leer, wenn unbekannt)."""
    return str(haus_von_fraktion(kennung, pfad).get("wappen_kurz") or "").strip()  # Kurzform
