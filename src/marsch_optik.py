# -*- coding: utf-8 -*-  # ANZEIGETEXTE tragen echte Umlaute (Schnitt T-1, Daniel 03.11.2026);
#                          Code, Kennungen und Kommentare bleiben ASCII.
"""
Nebelseetal Remake - Optik der Truppenbewegungen auf der Weltkarte (Stufe M-1, 02.11.2026).

VORGABE Daniel 02.11.2026 (Registerpunkt 140): Truppen kann man sehen, von wo nach wo sie laufen
und GROB wie lange sie laufen. NICHT sichtbar sind Truppenart, Anzahl, Karren, Ausruestung und die
genaue Geschwindigkeit - "Ein einzelner handkarren erzeugt das gleiche bewegungssymbol wie eine
ganze armee". Ein marschierender Verband ist kein Spionageziel. Ausnahme (Nachtrag Daniel): laeuft
ein Marsch auf eine EIGENE Siedlung zu, steht die Wegzeit GENAU da, weil der Spieler selbst
betroffen ist und die Zeit einschaetzen koennen muss.

Dieses Modul ist REIN: es zeichnet nichts, kennt kein tkinter und liest nur `data/marsch_optik.json`.
Die Zahlen (Form, Groesse, Farben, Takt, Restzeit-Stufen) stehen ALLE in der Datei; der Zeichner in
`main.py` liest sie hier ein. Ein Fassungswechsel (A Punkt, B Pfeil, C Puls) ist damit eine
Aenderung an der Datendatei und kein Umbau am Code.

Entwurf und Begruendung: `docs/design/MARSCH_ENTWURF_20261102.md` (Abschnitt A.1 bis A.3, D.2);
Vergleichsbild der drei Fassungen: `docs/design/MARSCH_VERGLEICH_20261102.png`.
"""
from __future__ import annotations

import json                                # Datendatei lesen
import os                                  # Pfad zusammensetzen
from typing import Any, Dict              # Typen der Rueckgaben

import spieldaten                          # EINE Stelle fuer die Projektwurzel

STAND = "2026-11-02.1"                    # Stand dieser Fassung

# Die Vorgabe im Code - sie gilt, wenn `data/marsch_optik.json` fehlt oder kaputt ist.
# Die Zahlen sind VORSCHLAG aus dem Entwurf (A.1), nicht belegt: das Handbuch 2009 kennt keine
# Marschgrafik, weil Nebelseetal keine begehbare Weltkarte hatte.
VORGABE: Dict[str, Any] = {
    "aktiv": True,                                            # Schalter fuer die ganze Anzeige
    "fassung": "A",                                           # A Punkt, B Pfeil, C Puls
    "symbol": {"form": "kreis", "durchmesser_px": 6,          # das Marschzeichen selbst
               "fuellung": "#F59E0B", "rand": "#7C2D12", "linienbreite": 1},
    "start_marker": {"form": "quadrat_hohl", "kante_px": 8,   # hohles Quadrat am Startfeld
                     "farbe": "#DAA520", "linienbreite": 1},
    "ziel_marker": {"form": "quadrat_hohl", "kante_px": 8,    # hohles Quadrat am Zielfeld
                    "farbe": "#DAA520", "linienbreite": 1},
    "linie": {"farbe_hin": "#F59E0B", "farbe_rueck": "#38BDF8",   # Hin- und Rueckweg getrennt
              "breite_px": 2, "muster": "durchgezogen", "dash": None},
    "bewegung": {"art": "laufender_punkt", "takt_ms": 400},   # wie die Bewegung gezeigt wird
    "groesse": "konstant",                                    # KEINE Groesse nach Truppenzahl
    "restzeit": {"ort": "popup_und_zeile_unter_der_karte",    # wo die grobe Zeit steht
                 "stufen": [{"bis_sekunden": 3600, "text": "unter 1 h"},
                            {"bis_sekunden": 10800, "text": "1-3 h"},
                            {"bis_sekunden": 21600, "text": "3-6 h"},
                            {"bis_sekunden": None, "text": "über 6 h"}],
                 "eigenes_ziel_genau": True,                  # eigenes Ziel: GENAU statt grob
                 "genau_format": "{h} h {m} min"},
    "rueckreise": {"farbe": "#38BDF8", "richtung_gespiegelt": True},
    "mehrere": {"versatz_px": 2, "max_versatz_px": 4},        # Versatz bei gleichem Start und Ziel
    "klick": {"toleranz_px": 6,                               # Trefferband um die Linie
              "reihenfolge": ["dorf", "marsch", "feld"]},     # Dorf hat Vorrang vor der Linie
}


def _pfad() -> str:
    """Der Pfad der Datendatei - ueber die EINE Projektwurzel, nie relativ zum Arbeitsverzeichnis."""
    return os.path.join(spieldaten.projektwurzel(), "data", "marsch_optik.json")


def optik() -> Dict[str, Any]:
    """Die Einstellungen der Marsch-Anzeige: Vorgabe, ueberschrieben von `data/marsch_optik.json`.

    Fehlt die Datei oder ist sie kaputt, gilt die Vorgabe im Code - das Spiel laeuft weiter.
    Die Datei hat Vorrang, unbekannte Schluessel bleiben erhalten.
    """
    werte: Dict[str, Any] = dict(VORGABE)                                        # Vorgabe als Grundlage
    for feld, wert in VORGABE.items():                                           # je Abschnitt kopieren
        if isinstance(wert, dict):                                               # Abschnitt ist ein Verzeichnis
            werte[feld] = dict(wert)                                             # tiefe Kopie, kein Teilen
    try:                                                                         # Datei lesen
        with open(_pfad(), encoding="utf-8") as f:                               # UTF-8 wie alle Spieldaten
            daten = json.load(f)                                                 # Inhalt als dict
    except (OSError, ValueError):                                                # fehlt oder ist kaputt
        return werte                                                             # dann die Vorgabe
    if not isinstance(daten, dict):                                              # unerwarteter Inhalt
        return werte                                                             # dann die Vorgabe
    for feld, wert in daten.items():                                             # Datei hat Vorrang
        if isinstance(wert, dict) and isinstance(werte.get(feld), dict):          # Abschnitt ergaenzen
            werte[feld].update(wert)                                             # nur die genannten Schluessel
        else:
            werte[feld] = wert                                                   # ganzer Wert ersetzt
    stufen = werte.get("restzeit", {}).get("stufen")                             # Restzeit-Stufen pruefen
    if not isinstance(stufen, list) or not stufen:                               # kaputte oder leere Stufen
        werte["restzeit"]["stufen"] = list(VORGABE["restzeit"]["stufen"])         # dann die Vorgabe
    return werte


def _als_zahl(wert: Any) -> float:
    """Eine Zahl roh und sicher - alles Unbrauchbare zaehlt 0, nie ein Absturz."""
    try:
        return float(wert)                                                   # Zahl (auch "12.0")
    except (TypeError, ValueError):                                          # Text oder None
        return 0.0                                                           # dann 0


def restzeit_stufe(rest_sekunden: Any, einstellungen: Any = None) -> str:
    """Die GROBE Restzeit als Text - die Stufe aus `restzeit.stufen`, nie die genaue Zahl.

    Die Stufen sind die Sichtbarkeitsregel: aus der groben Wegzeit darf sich die Einheit nicht
    erraten lassen (Vorgabe Daniel). Eine negative Restzeit (Uhr rueckwaerts) wird auf 0 gezogen,
    damit nie eine Zahl unter null angezeigt wird.
    """
    werte = einstellungen if isinstance(einstellungen, dict) else optik()    # Einstellungen
    stufen = werte.get("restzeit", {}).get("stufen") or VORGABE["restzeit"]["stufen"]
    rest = max(0.0, _als_zahl(rest_sekunden))                                # nie negativ anzeigen
    for stufe in stufen:                                                     # von klein nach gross
        if not isinstance(stufe, dict):                                      # unbrauchbarer Eintrag
            continue                                                         # ueberspringen
        grenze = stufe.get("bis_sekunden")                                    # Obergrenze der Stufe
        if grenze is None or rest < _als_zahl(grenze):                       # passt (None = offen)
            return str(stufe.get("text") or "unterwegs")                      # Text der Stufe
    return "unterwegs"                                                       # Rueckfall ohne Absturz


def restzeit_genau(rest_sekunden: Any, einstellungen: Any = None) -> str:
    """Die GENAUe Restzeit als Text - nur fuer ein EIGENES Ziel (Nachtrag Daniel).

    Format aus `restzeit.genau_format`; gerechnet wird in vollen Stunden und Minuten.
    """
    werte = einstellungen if isinstance(einstellungen, dict) else optik()    # Einstellungen
    muster = str(werte.get("restzeit", {}).get("genau_format") or "{h} h {m} min")
    rest = max(0.0, _als_zahl(rest_sekunden))                                # nie negativ anzeigen
    gesamt_minuten = int(rest // 60)                                         # ganze Minuten
    stunden, minuten = divmod(gesamt_minuten, 60)                             # in h und min
    return muster.format(h=stunden, m=minuten)                               # fertiger Text


def restzeit_text(rest_sekunden: Any, genau: bool = False, einstellungen: Any = None) -> str:
    """Die Restzeit als Anzeige: GENAU beim eigenen Ziel, sonst die grobe Stufe.

    `genau` kommt vom Ziel des Auftrags (eigene Siedlung) - nicht von der Truppe und nicht von der
    Geschwindigkeit; die Stufe bleibt fuer fremde Ziele immer grob (Vorgabe Daniel, Register 140).
    """
    werte = einstellungen if isinstance(einstellungen, dict) else optik()    # Einstellungen
    if genau and werte.get("restzeit", {}).get("eigenes_ziel_genau", True):   # eigenes Ziel: genau
        return restzeit_genau(rest_sekunden, werte)                           # genaue Wegzeit
    return restzeit_stufe(rest_sekunden, werte)                               # sonst die grobe Stufe


def aktiv(einstellungen: Any = None) -> bool:
    """Ist die Marsch-Anzeige eingeschaltet? (Schalter `aktiv` in der Datendatei.)"""
    werte = einstellungen if isinstance(einstellungen, dict) else optik()    # Einstellungen
    return bool(werte.get("aktiv", True))                                    # Vorgabe: an
