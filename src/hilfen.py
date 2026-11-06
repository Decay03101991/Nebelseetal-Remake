"""Kleine, reine Helfer, die mehrere Module brauchen.

Dieses Modul hat **keine** Projekt-Importe. Dadurch kann es jedes Modul benutzen, ohne dass
Importzyklen entstehen.

Belegt durch den Code-Audit vom 31.10.2026 (Befund P3, Vorschlag 1): `_als_zahl`, `_als_int`
und `_aufzaehlung` standen in `auftraege.py` und `kampfbericht.py` doppelt, der Filter fuer
brauchbare Bestaende zusaetzlich in `auftraege._bestand` und in beiden Beutefunktionen.

Die Funktionen sind absichtlich streng gleich wie die bisherigen privaten Fassungen: gleiche
Vorgaben, gleiches Abschneiden statt Runden, gleicher Text bei leerer Aufzaehlung. Es aendert
sich nur der Ort, keine Zahl.
"""

from __future__ import annotations

from typing import Any, Dict


def als_zahl(wert: Any, vorgabe: float = 0.0) -> float:
    """Nimmt Zahlen, Zahlen-als-Text und None; Unbrauchbares wird zur Vorgabe."""
    if wert is None:
        return float(vorgabe)
    try:
        return float(wert)
    except (TypeError, ValueError):
        return float(vorgabe)


def als_int(wert: Any, vorgabe: int = 0) -> int:
    """Wie `als_zahl`, aber ganzzahlig - schneidet ab, rundet nicht."""
    try:
        return int(float(wert))
    except (TypeError, ValueError):
        return int(vorgabe)


def aufzaehlung(werte: Any) -> str:
    """`Holz 5, Stein 3` - alphabetisch sortiert; nichts Brauchbares heisst `keine`."""
    if not isinstance(werte, dict) or not werte:
        return "keine"
    return ", ".join(f"{k} {int(als_zahl(v))}" for k, v in sorted(werte.items()))


def zahl_de(betrag: Any, stellen: int = 2) -> str:
    """Deutsche Anzeige einer Menge: hoechstens `stellen` Nachkommastellen, Komma statt Punkt.

    Daniel 06.11.2026 (Frage 2 der Runde): der KERN bleibt ungerundet - die ANZEIGE rundet auf
    zwei Stellen und schreibt ein Komma. So steht in der Kaserne "0,75 Pferde" statt "0.75
    Pferde" und "262,5 Gold" statt "262.5 Gold". Ganze Zahlen erscheinen ohne Nachkommastellen
    ("16"), damit die Zeile nicht mit Nuellen vollsteht.
    """
    text = ("%." + str(int(stellen)) + "f") % als_zahl(betrag)   # erst auf die Stellen runden
    if "." in text:                                              # nur wenn es Bruchteile gibt
        text = text.rstrip("0").rstrip(".")                      # abschneidende Nullen weg
    return text.replace(".", ",")                                # Punkt wird Komma


def positive_ganze_werte(werte: Any) -> Dict[str, int]:
    """`{name: menge}` ohne alles Unbrauchbare: nur ganze Zahlen groesser 0.

    Wird fuer Bestaende (Einheiten), Vorraete (Rohstoffe) und Lagerstaende gebraucht.
    Text und None zaehlen 0, negative Zahlen fallen weg - genau wie in den bisherigen
    Fassungen `auftraege._bestand` und den Vorratsfiltern in `kampfbericht`.
    """
    out: Dict[str, int] = {}
    if not isinstance(werte, dict):
        return out
    for name, menge in werte.items():
        n = int(max(0.0, als_zahl(menge)))
        if n > 0:
            out[str(name)] = n
    return out
