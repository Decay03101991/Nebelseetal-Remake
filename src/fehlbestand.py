"""Fehlbestand: welche Rohstoffe fehlen und um wieviel.

Reine Standardbibliothek, keine Importe aus dem uebrigen Projekt - der Baustein
laeuft damit auch in Werkzeugen, Bots und Einzelpruefungen ohne Spielkontext.

Oeffentliche Schnittstelle (nicht umbenennen, sie ist verdrahtet):

    fehlbestand(vorrat, kosten) -> dict
    text(fehlt, vorrat, kosten)  -> str

Lesart der Eingaben:
  * `kosten` ist die Bedarfsliste {rohstoff: menge}; nur diese Schluessel werden
    gerechnet. Ein Rohstoff, der nicht in `kosten` steht, wird nie als fehlend
    gemeldet (kein Bedarf).
  * `vorrat` ist der Bestand {rohstoff: menge}. Ein Bedarf ohne Eintrag im
    Vorrat zaehlt als voll fehlend.
  * Reihenfolge: es gilt die Reihenfolge der Schluessel aus `kosten` (dict-
    Einfuegereihenfolge, in Python stabil). Damit ist dieselbe Eingabe immer
    gleich sortiert - ohne alphabetisches Umsortieren, das die Anzeige im Spiel
    gegen die Rezeptur verdrehen wuerde.

Robustheit (bewusst entschieden, nicht stillschweigend):
  * fehlender Eintrag, None, NaN/inf, Text ohne Zahl -> 0.
  * Zahl als Text ("100", " 37.5 ") wird gelesen, nicht verworfen; ein Komma
    als Dezimaltrennzeichen ("37,5" aus deutschen Anzeigen) wird ebenfalls
    gelesen. Text, der keine Zahl ist ("viel"), zaehlt als 0.
  * bool zaehlt als 0: True ist keine Menge, und `float(True) == 1.0` wuerde
    stillschweigend einen Rohstoff erfinden.
  * negative Werte zaehlen als 0 (Vorrat) bzw. 0 Bedarf (Kosten). Ein negativer
    Vorrat erzeugt nie einen Fehlbestand groesser als der volle Bedarf.

Gerundet wird auf 2 Stellen (`_zwei`), damit 100 - 37.2 nicht als
62.800000000000004 in Meldung oder Spielstand landet.
"""
from __future__ import annotations

import math

# So viele Stellen stehen in Meldung und Rueckgabe.
STELLEN = 2


def _zahl(wert, standard: float = 0.0) -> float:
    """Wandelt einen beliebigen Wert in eine brauchbare Zahl um.

    Nicht-Zahlen, NaN, Unendlich und bool werden zu `standard`. Texte werden
    als Zahl gelesen, wenn es geht (auch mit Komma).
    """
    if wert is None or isinstance(wert, bool):
        return float(standard)
    if isinstance(wert, (int, float)):
        zahl = float(wert)
    elif isinstance(wert, str):
        roh = wert.strip().replace(",", ".")
        if not roh:
            return float(standard)
        try:
            zahl = float(roh)
        except ValueError:
            return float(standard)
    else:
        return float(standard)
    if not math.isfinite(zahl):
        return float(standard)
    return zahl


def _bestand(vorrat: dict, name) -> float:
    """Vorrat eines Rohstoffs, nie negativ."""
    if not isinstance(vorrat, dict):
        return 0.0
    return max(0.0, _zahl(vorrat.get(name, 0)))


def _bedarf(kosten: dict, name) -> float:
    """Bedarf eines Rohstoffs, nie negativ."""
    if not isinstance(kosten, dict):
        return 0.0
    return max(0.0, _zahl(kosten.get(name, 0)))


def _zwei(wert: float) -> float:
    """Auf 2 Stellen runden und -0.0 vermeiden."""
    gerundet = round(float(wert) + 0.0, STELLEN)
    return 0.0 if gerundet == 0 else gerundet


def _menge(wert: float) -> str:
    """Mengentext: ganze Zahl ohne Nachkommastellen, sonst 2 Stellen (37.20)."""
    zahl = _zwei(wert)
    if zahl == int(zahl):
        return str(int(zahl))
    return f"{zahl:.{STELLEN}f}"


def _betrag(wert: float) -> str:
    """Fehlmenge immer mit 2 Stellen (62.80)."""
    return f"{_zwei(wert):.{STELLEN}f}"


def fehlbestand(vorrat: dict, kosten: dict) -> dict:
    """Was FEHLT: {rohstoff: fehlmenge>0}. Reihenfolge stabil, Werte auf 2 Stellen gerundet.

    Kosten ohne Vorrat zaehlen als voll fehlend. Negative oder fehlende Vorraete = 0.
    """
    if not isinstance(kosten, dict):
        return {}
    fehlt: dict = {}
    for name in kosten:
        bedarf = _bedarf(kosten, name)
        if bedarf <= 0:
            continue
        rest = bedarf - _bestand(vorrat, name)
        if rest <= 0:
            continue
        menge = _zwei(rest)
        if menge <= 0:  # Rest kleiner als die Rundungsstelle: nichts fehlt
            continue
        fehlt[name] = menge
    return fehlt


def text(fehlt: dict, vorrat: dict, kosten: dict) -> str:
    """Kurztext fuer Meldungen, z. B.: 'holz fehlt 62.80 (37.20 von 100)', mehrere durch ', '.

    Bei leerem fehlt: ''. Keine Umlaute in Schluesselnamen, Rohstoffnamen so uebernehmen wie im dict.
    """
    if not isinstance(fehlt, dict) or not fehlt:
        return ""
    teile = []
    for name, menge in fehlt.items():
        fehlmenge = _zwei(max(0.0, _zahl(menge)))
        if fehlmenge <= 0:
            continue
        teile.append(
            f"{name} fehlt {_betrag(fehlmenge)}"
            f" ({_menge(_bestand(vorrat, name))} von {_menge(_bedarf(kosten, name))})"
        )
    return ", ".join(teile)
