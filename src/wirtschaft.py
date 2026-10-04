"""
Wirtschaft — stuendlicher Rohstoffertrag der Siedlungen (Remake Nebelseetal).

Rechnet aus den Siedlungskarten (Gelaende + Gebaeude je Feld) aus, was der Spieler je
Stunde erwirtschaftet:

  * siedlung_ertrag(siedlung)   — Ertrag EINER Siedlung je Rohstoff und Stunde
  * ertrag_gesamt(siedlungen)   — Summe ueber alle Siedlungen, optional mit Forschungsfaktor
  * ertrag_text(ertrag)         — lesbare Fassung ('Holz 8/h, Nahrung 4/h, Leder 4/h')
  * kapazitaet(siedlung)        — theoretischer Hoechstertrag der Karte (Anzeige im Spiel)

Alle Zahlen kommen aus ``gelaende.ertrag_pro_stunde`` (den Originalwerten), der
Forschungsfaktor aus ``bonus_system.get_production_multiplier``. Dieses Modul erfindet
keine Werte und veraendert keine der vorhandenen Module.

Besonderheit: ``siedlung_ertrag`` liefert neben den Rohstoffen unter dem Schluessel
``UEBERSPRUNGEN`` ("uebersprungen") eine Liste von Begruendungen, warum ein Feld nicht
mitgerechnet wurde (Siedlung ohne Karte, Sumpf, unbekanntes Gebaeude, kein Ertrag auf
diesem Gelaende). So wird nichts still verschluckt. ``ertrag_gesamt`` und ``ertrag_text``
ignorieren diesen Schluessel.
"""
from __future__ import annotations

from functools import lru_cache

import bonus_system
import gelaende

# Schluessel, unter dem siedlung_ertrag die uebersprungenen Felder samt Begruendung ablegt.
UEBERSPRUNGEN = "uebersprungen"


# --------------------------------------------------------------------------
# Hilfsgriffe
# --------------------------------------------------------------------------

def _feld(objekt, name, vorgabe=None):
    """Liest ein Feld sowohl von einem Objekt (siedlung.karte) als auch aus einem dict."""
    if isinstance(objekt, dict):
        return objekt.get(name, vorgabe)
    return getattr(objekt, name, vorgabe)


def _rohstoff_von(geb_id: str):
    """Der (einzelne) Rohstoff eines Gebaeudes aus den Stammdaten — None, wenn uneindeutig."""
    geb = gelaende.alle_gebaeude().get(geb_id)
    if not geb:
        return None
    roh = geb.get("rohstoff")
    if isinstance(roh, list):           # mehrere Rohstoffe (Jaeger) -> hier nicht eindeutig
        return None
    return roh or None


def _zahl_text(zahl) -> str:
    """Zahl lesbar: 4.0 -> '4', 1.5 -> '1.5', 0 -> '0'."""
    if isinstance(zahl, float) and zahl.is_integer():
        zahl = int(zahl)
    return f"{zahl:g}"


# --------------------------------------------------------------------------
# 1. Ertrag einer Siedlung
# --------------------------------------------------------------------------

def siedlung_ertrag(siedlung) -> dict:
    """
    Stuendlicher Ertrag EINER Siedlung als {Rohstoff: Menge_pro_Stunde}.

    Fuer jedes belegte Feld wird die Gelaendeart aus ``siedlung.karte['raster']`` geholt
    und der Ertrag des Gebaeudes dort aus ``gelaende.ertrag_pro_stunde`` gelesen. Zahlen
    werden addiert, dicts (Jaeger: Nahrung und Leder) einzeln.

    Uebersprungen und begruendet werden Felder ohne Karte, Suempfe, unbekannte Gebaeude
    und Felder, auf denen das Gebaeude nichts liefert. Die Begruendungen stehen in der
    Ergebnis-dict unter dem Schluessel ``UEBERSPRUNGEN`` (Liste); die Liste ist leer, wenn
    nichts uebersprungen wurde.
    """
    ergebnis: dict = {}
    uebersprungen: list = []
    ergebnis[UEBERSPRUNGEN] = uebersprungen

    karte = _feld(siedlung, "karte")
    if not karte:
        uebersprungen.append("Siedlung ohne Karte")
        return ergebnis

    raster = karte.get("raster") if isinstance(karte, dict) else None
    if not raster:
        uebersprungen.append("Karte ohne Raster")
        return ergebnis

    bauten = _feld(siedlung, "bauten")
    if bauten is None:
        uebersprungen.append("keine Bauten gespeichert")
        return ergebnis
    if not bauten:
        return ergebnis

    for feld_text, geb_eintrag in bauten.items():
        # Feldnummer pruefen
        try:
            feld = int(feld_text)
        except (TypeError, ValueError):
            uebersprungen.append(f"Feld '{feld_text}': keine gueltige Feldnummer")
            continue
        if feld < 0 or feld >= len(raster):
            uebersprungen.append(f"Feld {feld}: liegt ausserhalb der Karte")
            continue

        art = raster[feld]
        if art == gelaende.SUMPF:
            uebersprungen.append(f"Feld {feld}: Sumpf ist nicht bebaubar")
            continue

        geb_id = gelaende.finde_gebaeude(geb_eintrag)
        if not geb_id:
            uebersprungen.append(f"Feld {feld}: unbekanntes Gebaeude '{geb_eintrag}'")
            continue

        ertrag = gelaende.ertrag_pro_stunde(geb_id, art)
        if ertrag is None:
            uebersprungen.append(
                f"Feld {feld}: {gelaende.gebaeude_name(geb_id)} liefert auf "
                f"{gelaende.name(art)} nichts")
            continue

        if isinstance(ertrag, dict):
            for roh, menge in ertrag.items():
                ergebnis[roh] = ergebnis.get(roh, 0) + menge
        else:
            roh = _rohstoff_von(geb_id)
            if not roh:
                uebersprungen.append(f"Feld {feld}: kein Rohstoff zu {geb_id} bekannt")
                continue
            ergebnis[roh] = ergebnis.get(roh, 0) + ertrag

    return ergebnis


def uebersprungen_von(ertrag: dict) -> list:
    """Die Begruendungsliste aus einem Ergebnis von ``siedlung_ertrag`` (nie None)."""
    return list(ertrag.get(UEBERSPRUNGEN, []))


# --------------------------------------------------------------------------
# 2. Summe ueber alle Siedlungen
# --------------------------------------------------------------------------

def ertrag_gesamt(siedlungen, forschung_level=None) -> dict:
    """
    Summe des stuendlichen Ertrags ueber mehrere Siedlungen.

    Wird ``forschung_level`` uebergeben (dict der Forschungsstaende, z. B.
    ``{"bergbau": 2, "landwirtschaft": 1}``), so wird jede Rate mit
    ``bonus_system.get_production_multiplier(forschung_level, rohstoff)`` multipliziert.
    Das Ergebnis ist auf zwei Nachkommastellen gerundet.
    """
    gesamt: dict = {}
    for siedlung in siedlungen:
        teil = siedlung_ertrag(siedlung)
        for roh, menge in teil.items():
            if roh == UEBERSPRUNGEN:
                continue
            rate = menge
            if forschung_level:
                rate *= bonus_system.get_production_multiplier(forschung_level, roh.lower())
            gesamt[roh] = gesamt.get(roh, 0.0) + rate
    return {roh: round(menge, 2) for roh, menge in gesamt.items()}


# --------------------------------------------------------------------------
# 3. Lesbare Fassung
# --------------------------------------------------------------------------

def ertrag_text(ertrag: dict) -> str:
    """Lesbarer Text wie 'Holz 8/h, Nahrung 4/h, Leder 4/h' (ohne die Uebersprungenen)."""
    teile = [f"{roh} {_zahl_text(menge)}/h"
             for roh, menge in ertrag.items() if roh != UEBERSPRUNGEN]
    return ", ".join(teile)


# --------------------------------------------------------------------------
# 4. Kapazitaet (theoretischer Hoechstertrag der Karte)
# --------------------------------------------------------------------------

@lru_cache(maxsize=None)
def _beste_je_gelaende(art_id: str) -> dict:
    """Bestes Gebaeude je Rohstoff auf einer Gelaendeart als {Rohstoff: Menge}."""
    beste: dict = {}
    for geb_id, geb in gelaende.alle_gebaeude().items():
        ertrag = gelaende.ertrag_pro_stunde(geb_id, art_id)
        if ertrag is None:
            continue
        if isinstance(ertrag, dict):
            for roh, menge in ertrag.items():
                if menge > beste.get(roh, 0):
                    beste[roh] = menge
        else:
            roh = geb.get("rohstoff")
            if isinstance(roh, str) and roh:
                if ertrag > beste.get(roh, 0):
                    beste[roh] = ertrag
    return beste


def kapazitaet(siedlung) -> dict:
    """
    Was die Karte je Stunde hergeben KANN, wenn jedes passende Feld mit dem jeweils besten
    Gebaeude bebaut wird: {Rohstoff: Menge_pro_Stunde}. Gedacht fuer die Anzeige im Spiel.

    Summfehler der einzelnen Felder: 'bestes Gebaeude' ist je Rohstoff unabhaengig
    bestimmt (Obergrenze), weil ein Feld nur ein Gebaeude tragen kann. Suempfe und
    unbekannte Gelaendearten tragen nichts bei.
    """
    karte = _feld(siedlung, "karte")
    if not isinstance(karte, dict):
        return {}
    raster = karte.get("raster") or []

    gesamt: dict = {}
    for art in raster:
        if art not in gelaende.ARTEN or not gelaende.ist_bebaubar(art):
            continue
        for roh, menge in _beste_je_gelaende(art).items():
            gesamt[roh] = gesamt.get(roh, 0) + menge
    return {roh: round(menge, 2) for roh, menge in gesamt.items()}
