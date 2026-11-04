"""Historische Gildenwertung als reine, inaktive Datenfunktion.

Quelle: TutorialundBeschreibung_einesSpielers(1).odt S. 10,
Ranglisten-Screenshot vom 31.08.2011. Kein Mehrspieler-/Gildensystem
im Remake wird hierdurch aktiviert; dient als prüfbare Basis für UI.
"""
from __future__ import annotations
from decimal import Decimal, InvalidOperation


def _zahl(wert):
    """Nummerischer Punktwert; nur endliche, nichtnegative Werte erlaubt."""
    try:
        z = Decimal(str(wert))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError("Ungültiger Punktewert") from None
    if not z.is_finite() or z < 0:
        raise ValueError("Punkte müssen endlich und nichtnegativ sein")
    return z


def gildenwertung(gesamt, durchschnitt):
    """Original (Gesamt + Durchschnitt)/2, exakter Dezimalwert."""
    return (_zahl(gesamt) + _zahl(durchschnitt)) / Decimal(2)


def gildenrangliste(gilden):
    """Sortierte, NICHT ins Spiel integrierte historische Ranglistendaten.

    Keine Gilde ohne mindestens ein Mitglied bekommt eine echte Wertung.
    Keine Einflussnahme auf Einzelspieler-Siege, Rohstoffe oder Kampf.
    """
    eintraege = []
    for g in gilden:
        name = str(g["name"])
        gesamt = _zahl(g.get("gesamt", 0))
        durchschnitt = _zahl(g.get("durchschnitt", 0))
        mitglieder = int(g.get("mitglieder", 0))
        if mitglieder < 0:
            raise ValueError("Negative Mitgliederzahl")
        wertung = gildenwertung(gesamt, durchschnitt) if mitglieder else Decimal(0)
        eintraege.append(dict(name=name, gesamt=gesamt, durchschnitt=durchschnitt,
                              mitglieder=mitglieder, wertung=wertung))
    eintraege.sort(key=lambda g: (-g["wertung"], g["name"].casefold()))
    for nr, g in enumerate(eintraege, 1):
        g["rang"] = nr
    return eintraege
