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

def _effektive_rate(geb_id, roh, menge, forschung_level):
    """Ertrag eines Gebaeudes mit Forschungsfaktor - die EINE Stelle, die den Bonus anwendet.

    Nur die Produktion des konkreten Gebaeudes wird erforscht; diese Quelle dokumentiert zwei
    Ausnahmen: Jaeger komplett, Rinderfarm nur Nahrung. Das verhindert einen unberechtigten
    globalen Bonus im gemischten Lager.
    """
    if (not forschung_level or geb_id == "jaeger"
            or (geb_id == "rinderfarm" and roh.lower() == "nahrung")):
        return menge
    return menge * bonus_system.get_production_multiplier(forschung_level, roh.lower())


def _feld_ertraege(siedlung, forschung_level=None):
    """Alle bebauten Felder mit ihrem Ertrag: ``([(geb_id, {roh: menge})], uebersprungen)``.

    A-3 (Dorfuebersicht, 31.10.2026): `siedlung_ertrag` und `dorf_uebersicht` rechnen BEIDE hier
    hinein - sonst gaebe es zwei Wahrheiten ueber denselben Ertrag.
    """
    eintraege = []
    uebersprungen = []

    karte = _feld(siedlung, "karte")
    if not karte:
        uebersprungen.append("Siedlung ohne Karte")
        return eintraege, uebersprungen

    raster = karte.get("raster") if isinstance(karte, dict) else None
    if not raster:
        uebersprungen.append("Karte ohne Raster")
        return eintraege, uebersprungen

    bauten = _feld(siedlung, "bauten")
    if bauten is None:
        uebersprungen.append("keine Bauten gespeichert")
        return eintraege, uebersprungen
    if not bauten:
        return eintraege, uebersprungen

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
            eintraege.append((geb_id, {roh: _effektive_rate(geb_id, roh, menge, forschung_level)
                                       for roh, menge in ertrag.items()}))
        else:
            roh = _rohstoff_von(geb_id)
            if not roh:
                uebersprungen.append(f"Feld {feld}: kein Rohstoff zu {geb_id} bekannt")
                continue
            eintraege.append((geb_id, {roh: _effektive_rate(geb_id, roh, ertrag, forschung_level)}))
    return eintraege, uebersprungen


def siedlung_ertrag(siedlung, forschung_level=None) -> dict:
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
    eintraege, uebersprungen = _feld_ertraege(siedlung, forschung_level)
    ergebnis: dict = {UEBERSPRUNGEN: uebersprungen}
    for _geb_id, ertrag in eintraege:
        for roh, menge in ertrag.items():
            ergebnis[roh] = ergebnis.get(roh, 0) + menge
    return ergebnis


def uebersprungen_von(ertrag: dict) -> list:
    """Die Begruendungsliste aus einem Ergebnis von ``siedlung_ertrag`` (nie None)."""
    return list(ertrag.get(UEBERSPRUNGEN, []))


# --------------------------------------------------------------------------
# 1b. Dorfuebersicht: welche Gebaeude, wie viele, welcher Ertrag (A-3)
# --------------------------------------------------------------------------

def _lade_json(name: str) -> dict:
    """Eine Datendatei aus ``data/`` lesen; fehlt sie, kommt ein leeres dict (kein Absturz)."""
    import json
    import os
    try:
        import spieldaten
        wurzel = spieldaten.projektwurzel()
        with open(os.path.join(wurzel, "data", name), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError, KeyError):
        return {}


def siedler_bindung_aktiv() -> bool:
    """Binden Bauten Siedler? Die EINE Lesestelle fuer `data/bausiedler.json`.

    Daniels Entscheidung 31.10.2026 (Auswahlformular Frage 5 = B): NEIN. Die BELEGTEN Preise
    (Holzfaeller, Steinmetz, Jaeger je 1 Siedler; Screenshot 1838857) bleiben in
    `data/baupreise.json` stehen - der Schalter nimmt nur den Siedler-Posten aus der Zahlung.
    Fehlt die Datei, gilt das Original (True): im Zweifel keine stille Abweichung.
    """
    daten = _lade_json("bausiedler.json")
    return bool(daten.get("aktiv", True))


def siedler_je_bau(geb_id: str) -> int:
    """Belegter Siedler-Preis eines Gebaeudes (0, wenn die Quelle keinen nennt).

    Gelesen wird die belegte Datei `data/baupreise.json` - NICHT der Schalter. So bleibt die
    Herkunft sichtbar, auch wenn der Schalter die Zahlung gerade abstellt.
    """
    preise = _lade_json("baupreise.json").get("preise") or {}
    eintrag = preise.get(geb_id) or {}
    wert = eintrag.get("siedler")
    if isinstance(wert, bool) or not isinstance(wert, (int, float)):
        return 0
    return int(wert)


def dorf_uebersicht(siedlung, forschung_level=None, siedler_bindend=None) -> dict:
    """Was steht in diesem Dorf, wie viel bringt es je Stunde, welchen Anteil hat es? (A-3)

    Daniels Spielbericht 31.10.2026: "welche gebaeude habe ich, wie viele, welcher ertrag" - die
    Siedlungskarte zeigte nur Felder, keine Summe. Gerechnet wird ueber `_feld_ertraege`, also
    GENAU wie `siedlung_ertrag` und damit wie Produktion und Kopfzeile.

    Rueckgabe::

        {"gebaeude": [{"gebaeude", "name", "anzahl", "stufen", "stufen_text",
                       "ertrag": {roh: menge}, "ertrag_text", "summe", "anteil",
                       "siedler_je", "siedler"}],
         "summe": {"anzahl", "ertrag", "ertrag_text", "summe", "siedler"},
         "uebersprungen": [ ... ],
         "siedler_bindend": bool,
         "hinweis": str}
    """
    if siedler_bindend is None:
        siedler_bindend = siedler_bindung_aktiv()
    eintraege, uebersprungen = _feld_ertraege(siedlung, forschung_level)
    stufen = _feld(siedlung, "stufen") or {}
    bauten = _feld(siedlung, "bauten") or {}

    gruppen: dict = {}
    for feld_text, geb_eintrag in bauten.items():
        geb_id = gelaende.finde_gebaeude(geb_eintrag)
        if not geb_id:
            continue
        gruppe = gruppen.setdefault(geb_id, {"gebaeude": geb_id,
                                             "name": gelaende.gebaeude_name(geb_id),
                                             "anzahl": 0, "stufen": [], "ertrag": {}})
        gruppe["anzahl"] += 1
        try:
            gruppe["stufen"].append(int(stufen.get(str(feld_text), stufen.get(feld_text, 1)) or 1))
        except (TypeError, ValueError):
            gruppe["stufen"].append(1)
    for geb_id, ertrag in eintraege:
        gruppe = gruppen.get(geb_id)
        if gruppe is None:
            continue
        for roh, menge in ertrag.items():
            gruppe["ertrag"][roh] = gruppe["ertrag"].get(roh, 0.0) + menge

    gesamt_summe = 0.0
    gesamt_ertrag: dict = {}
    for gruppe in gruppen.values():
        gruppe["summe"] = round(sum(gruppe["ertrag"].values()), 2)
        gesamt_summe += gruppe["summe"]
        for roh, menge in gruppe["ertrag"].items():
            gesamt_ertrag[roh] = gesamt_ertrag.get(roh, 0.0) + menge

    liste = []
    gesamt_anzahl = 0
    gesamt_siedler = 0
    for geb_id, gruppe in gruppen.items():
        stufen_liste = sorted(set(gruppe["stufen"]))
        stufen_text = ("Stufe " + ", ".join(str(s) for s in stufen_liste)
                       if len(stufen_liste) == 1
                       else "Stufen " + ", ".join(str(s) for s in stufen_liste))
        siedler_je = siedler_je_bau(geb_id)
        gesamt_anzahl += gruppe["anzahl"]
        gesamt_siedler += siedler_je * gruppe["anzahl"] if siedler_bindend else 0
        liste.append({**gruppe,
                      "ertrag": {roh: round(menge, 2) for roh, menge in gruppe["ertrag"].items()},
                      "ertrag_text": ertrag_text(gruppe["ertrag"]),
                      "stufen": stufen_liste,
                      "stufen_text": stufen_text,
                      "anteil": (round(gruppe["summe"] / gesamt_summe, 4)
                                 if gesamt_summe > 0 else 0.0),
                      "siedler_je": siedler_je,
                      "siedler": (siedler_je * gruppe["anzahl"] if siedler_bindend else 0)})
    liste.sort(key=lambda g: (-g["summe"], g["name"]))
    if not siedler_bindend:
        hinweis = ("Bauten binden keine Siedler (Daniels Entscheidung 31.10.2026). Die belegten "
                   f"Preise nennen fuer {', '.join(sorted({g['name'] for g in liste if g['siedler_je']}))}"
                   " je 1 Siedler — er wird derzeit nicht abgezogen.")
        if not any(g["siedler_je"] for g in liste):
            hinweis = "Bauten binden keine Siedler (Daniels Entscheidung 31.10.2026)."
    else:
        hinweis = "Bauten binden Siedler nach data/baupreise.json (belegt: Screenshot 1838857)."
    return {"gebaeude": liste,
            "summe": {"anzahl": gesamt_anzahl,
                      "ertrag": {roh: round(menge, 2) for roh, menge in gesamt_ertrag.items()},
                      "ertrag_text": ertrag_text(gesamt_ertrag),
                      "summe": round(gesamt_summe, 2), "siedler": gesamt_siedler},
            "uebersprungen": uebersprungen,
            "siedler_bindend": bool(siedler_bindend),
            "hinweis": hinweis}


# --------------------------------------------------------------------------
# 2. Summe ueber alle Siedlungen
# --------------------------------------------------------------------------

# Jolly Rogers Original-Tutorial, Seite 3: 1 Holz und 1 Stein pro Stunde als
# "Grundeinkommen" ZUSAETZLICH zum Gebaeudeertrag. Das gilt fuer neu angelegte
# Partien mit den historischen Originalkarten. Die fruehere generierte 8x7-Welt
# bleibt aus Kompatibilitaetsgruenden unveraendert (Legacy-Bestand nicht migrieren).
# Die Grundversorgung wird NACH dem Forschungsbonus gebucht, damit eine Forschung
# auf Holzfaeller/Steinmetze nicht versehentlich das Grundeinkommen vervielfacht.
ORIGINAL_GRUNDEINKOMMEN = {"Holz": 1.0, "Stein": 1.0}


def _ist_neue_originalsiedlung(siedlung) -> bool:
    karte = _feld(siedlung, "karte")
    return bool(isinstance(karte, dict) and karte.get("originalkarte_id")
                and karte.get("spalten") == 10 and karte.get("zeilen") == 10
                and len(karte.get("raster") or []) == 100)


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
        teil = siedlung_ertrag(siedlung, forschung_level=forschung_level)
        for roh, menge in teil.items():
            if roh == UEBERSPRUNGEN:
                continue
            gesamt[roh] = gesamt.get(roh, 0.0) + menge
        if _ist_neue_originalsiedlung(siedlung):
            for roh, grundrate in ORIGINAL_GRUNDEINKOMMEN.items():
                gesamt[roh] = gesamt.get(roh, 0.0) + grundrate
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
