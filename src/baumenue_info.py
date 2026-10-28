"""FIX04 – Datenmodell fuer das historische Baumenue der Siedlungskarte.

Keine zweite Bau-/Zahlungslogik: alle Entscheidungen kommen aus main.bauen_auf_karte,
main.baukosten und GameState.ortsdeckung. Alle Bezeichnungen aus buildings.json.
"""
from __future__ import annotations

import gelaende

KATEGORIEN = ("Produktion", "Werkstatt", "Ausbildung", "Verteidigung", "Sonstiges")


# FIX04b: Tipps sind NUR Lesehilfen. Keine Bauregel, keine Aenderung an Kosten
# oder Produktion; alle Werte stammen aus der bereits aktiven Gelaendedatei.
def _gesamt_ertrag(ertrag) -> float:
    """Vergleich der Mengen (bei mehreren Rohstoffen keine Wertgewichtung)."""
    if isinstance(ertrag, dict):
        return sum(float(wert) for wert in ertrag.values())
    return float(ertrag or 0)


def _rate_text(ertrag) -> str:
    if isinstance(ertrag, dict):
        return ", ".join(f"{name} {zahl:g}" for name, zahl in ertrag.items())
    return f"{float(ertrag):g}"


def standort_hinweis(kennung: str, art: str) -> str:
    """Datenbasierter Standorttipp zum angeklickten Originalkartenfeld.

    Rein beratend: weder Bauvoraussetzung noch neue Ertragsberechnung. Die
    Eignung folgt ausschliesslich `gelaende.bau_moeglich`, die Ertraege folgen
    `gelaende.ertrag_pro_stunde`; freie Felder werden nicht vorausgesetzt.
    """
    geb = gelaende.alle_gebaeude().get(kennung)
    erlaubt, _ = gelaende.bau_moeglich(kennung, art)
    if not geb or not erlaubt:
        return ""
    if geb.get("ertrag_pro_stunde"):
        kandidaten = [(gel, gelaende.ertrag_pro_stunde(kennung, gel))
                      for gel in gelaende.GELAENDEARTEN
                      if gelaende.bau_moeglich(kennung, gel)[0]]
        kandidaten = [(gel, wert) for gel, wert in kandidaten if wert is not None]
        if not kandidaten:
            return ""
        optimal_art, optimal_ertrag = max(kandidaten, key=lambda x: _gesamt_ertrag(x[1]))
        hier = gelaende.ertrag_pro_stunde(kennung, art)
        if hier is None:
            return ""
        if _gesamt_ertrag(hier) >= _gesamt_ertrag(optimal_ertrag):
            return (f"Standorttipp: {gelaende.name(art)} bringt hier den Hoechstertrag "
                    f"({_rate_text(hier)} pro Stunde).")
        return (f"Standorttipp: Auf {gelaende.name(optimal_art)} sind "
                f"{_rate_text(optimal_ertrag)} pro Stunde moeglich, "
                f"hier nur {_rate_text(hier)}. Ergiebigere Felder bevorzugen.")
    # Funktionsgebaeude liefern keinen direkten Gelaendeertrag. Empfehlung
    # NUR bei Gebaeuden, die auf Steppe tatsaechlich gebaut werden duerfen.
    steppe_ok, _ = gelaende.bau_moeglich(kennung, "steppe")
    if steppe_ok and art == "steppe":
        return ("Standorttipp: Steppe ist fuer dieses Gebaeude oft sinnvoll. "
                "So bleiben Wald, Berg, Grasland und Nebelsee fuer passende "
                "Rohstoffgebaeude frei.")
    if steppe_ok:
        return ("Standorttipp: Wenn freie Steppe vorhanden ist, dieses "
                "Funktionsgebaeude lieber dort errichten und ergiebige "
                "Rohstofffelder freihalten.")
    return ("Standorttipp: Auch Funktionsgebaeude belegen ein Feld. "
            "Moeglichst keine knappen Produktionsstandorte verbrauchen.")


SPIELERHILFE = (
    "Spieltipp: Holzfaeller im Wald, Minen/Steinmetze am Berg, "
    "Landwirtschaft auf Grasland und Tempel am Nebelsee sind meist "
    "ertragreicher. Gebaeude ohne direkten Ertrag (z. B. Bibliothek) "
    "moeglichst auf freie Steppe setzen. Steppe kann aber ebenfalls "
    "Rohstoffe liefern: auf die lokalen Ertraege achten."
)


def angebote(feld: int, art: str, siedlung, *,
             regelpruefung, kostenfunktion, deckungspruefung, ertragsfunktion,
             kategorie: str, wall_ohne_feld: bool = True) -> list[dict]:
    """Aktuelle Rubrik auf einem Feld, mit echten Voraussetzungen und Fehlmengen.

    Die Argumente ``regelpruefung``, ``kostenfunktion``, ``deckungspruefung`` und
    ``ertragsfunktion`` werden vom realen Spiel uebergeben; keine Kopie der Regeln.
    Die Anzeige ist read-only und aendert weder Geld noch Gebaeude noch Forschung.
    """
    if kategorie not in KATEGORIEN:
        raise ValueError(f"Unbekannte Baumenue-Rubrik: {kategorie!r}")
    if not isinstance(feld, int) or not 0 <= feld < len(siedlung.karte["raster"]):
        raise ValueError("Ungueltiges Kartenfeld")
    if siedlung.karte["raster"][feld] != art:
        raise ValueError("Gelaende passt nicht zum Kartenfeld")
    ausgabe = []
    for kennung, daten in sorted(gelaende.alle_gebaeude().items(),
                                 key=lambda eintrag: eintrag[1]["name"]):
        if daten.get("kategorie") != kategorie:
            continue
        if wall_ohne_feld and kennung == "verteidigungswall":
            continue
        erlaubt, _ = gelaende.bau_moeglich(kennung, art)
        if not erlaubt:
            continue
        # Fuer jede Zeile dieselbe Pruefung wie beim Bauen, ohne Mutation.
        regel_ok, grund = regelpruefung(kennung)
        preis = kostenfunktion(kennung) or {}
        fehlt = deckungspruefung(preis) if preis else {}
        if not preis:
            status = "Gesperrt: kein Baupreis hinterlegt"
        elif not regel_ok:
            status = f"Gesperrt: {grund}"
        elif fehlt:
            betraege = ", ".join(f"{name} {menge:g}" for name, menge in sorted(fehlt.items()))
            status = f"Fehlt im Ortslager: {betraege}"
        else:
            status = "Baubar – Rohstoffe vorhanden"
        ausgabe.append({
            "id": kennung,
            "name": daten["name"],
            "kategorie": kategorie,
            "wirkung": daten.get("wirkung") or "Keine Wirkung angegeben",
            "voraussetzung": daten.get("voraussetzung") or "Nicht angegeben",
            "ertrag": ertragsfunktion(kennung, art),
            "kosten": preis,
            "fehlt": fehlt,
            "regel_ok": bool(regel_ok),
            "baubar": bool(preis and regel_ok and not fehlt),
            "status": status,
            "standort_hinweis": standort_hinweis(kennung, art),
        })
    return ausgabe
