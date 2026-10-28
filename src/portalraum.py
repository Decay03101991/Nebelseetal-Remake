"""
Portal- und Limbus-Raum fuer das Nebelseetal-Remake (Paket W5-2).

Belegt (Portal-Anleitung 2005, portal.php; Handbuch 2009, S. 80-83):
  * Jede Spielerwelt liegt im magischen Limbus auf Koordinaten (X, Y, Z):
    X und Y sind die Position im Raster der EIGENEN Dimension, Z ist die
    Dimension selbst.
  * Es gibt 20 Dimensionen; in jeder Dimension sind 20 x 20 = 400 Felder
    frei fuer Spielerwelten.
  * Einen Koordinatenwechsel (Verschiebungsritual) fuehrt EINE einzelne
    Siedlung durch; er kostet 5.000 Mana und ist hoechstens einmal je
    24 Stunden erlaubt.
  * In der Portalanzeige ist die eigene Welt gruen, fremde Welten sind rot.

Verhaeltnis zu src/welt.py (WICHTIG, die beiden Kosten NICHT vermischen):
  * wechselkosten() liefert den BELEGTEN Festpreis von 5.000 Mana fuer einen
    Koordinatenwechsel. Der Wert steht in data/welten.json unter
    belegte_regeln.koordinatenwechsel.kosten_mana und wird hier nur gelesen.
  * welt.portalkosten(von, nach) ist dagegen ein VORSCHLAG: eine
    entfernungsabhaengige Formel fuer Reisen bzw. das Aktivieren des Portals
    (Grundbetrag + Kosten je Schritt). Diese Formel ist NICHT belegt.
  * Der dokumentierte Koordinatenwechsel kostet deshalb immer genau 5.000
    Mana aus einer Siedlung und benutzt NICHT die Vorschlagsformel aus
    welt.portalkosten().

Nicht belegt und hier bewusst NICHT erfunden:
  * Welches Feld eine konkrete Spielerwelt belegt — es gibt in diesem Projekt
    keine Spielerwelt-Daten. Deshalb faerben anzeige_raster()/portalfarbe()
    grob je Dimension: eigene Dimensionen gruen, fremde rot. Die feinere
    Feldfaerbung (nur das EIGENE Feld gruen) folgt, sobald Weltdaten da sind.
  * Ob ein Wechsel in dieselbe Dimension erlaubt ist; die Quelle schweigt
    dazu, daher wird nur geprueft, dass beide Dimensionen bekannt sind.

Nur Standardbibliothek; die Weltdaten werden ueber src/welt.py gelesen.
"""
from __future__ import annotations

import welt

# Rohdaten aus src/welt.py (dort bereits aus data/welten.json geladen) —
# nicht erneut einlesen, damit es nur EINE Datenquelle gibt.
_DATEN = welt._DATEI
_BELEGT = _DATEN["belegte_regeln"]
_KOORD = _BELEGT["koordinatenwechsel"]

_FELDER_AXIS = int(_BELEGT["felder_je_dimension"])           # 20
_FELDER_GESAMT = int(_BELEGT["felder_je_dimension_gesamt"])  # 400
_STUNDEN_SPERRE = int(_KOORD["hoechstens_je_stunden"])       # 24
_MANA_WECHSEL = int(_KOORD["kosten_mana"])                   # 5000
_BANNER = _BELEGT["bannerfarben"]                            # gruen / rot


def dimensionen() -> list:
    """Die 20 Dimensionen des Limbus (unveraendert aus src/welt.py)."""
    return welt.dimensionen()


def dim_zahl() -> int:
    """Anzahl der Dimensionen des Limbus (belegt: 20)."""
    return len(dimensionen())


def feld_zahl() -> int:
    """Felder je Dimension (belegt: 20 x 20 = 400)."""
    return _FELDER_GESAMT


def _achsen() -> int:
    """Kantenlaenge des Rasters je Dimension (belegt: 20)."""
    return _FELDER_AXIS


def _ist_ganz(v) -> bool:
    """True nur fuer echte Ganzzahlen (bool zaehlt nicht als Koordinate)."""
    return isinstance(v, int) and not isinstance(v, bool)


def _ist_dimension(z) -> bool:
    """True, wenn z der Index einer bekannten Dimension ist (0..19)."""
    return _ist_ganz(z) and 0 <= z < dim_zahl()


def koordinate(x: int, y: int, z: int):
    """
    Beschreibt das Feld (x, y) in Dimension z — oder None.

    None, wenn x oder y ausserhalb 0..19 liegen oder z keine bekannte
    Dimension ist (Index 0..19 in welt.dimensionen()). Das Feld traegt
    x, y, z, die Dimensionskennung ('dimension'), den Anzeigenamen ('name')
    und den belegten Weltnamen der Dimension ('welt' — oder None).
    """
    if not _ist_dimension(z):
        return None
    if not (_ist_ganz(x) and _ist_ganz(y)):
        return None
    if not (0 <= x < _FELDER_AXIS) or not (0 <= y < _FELDER_AXIS):
        return None
    d = dimensionen()[z]
    return {
        "x": x,
        "y": y,
        "z": z,
        "dimension": d["kennung"],
        "name": d["name"],
        "welt": d.get("welt"),
    }


def ist_gueltig(x, y, z) -> bool:
    """True, wenn (x, y, z) ein Feld im Raster einer bekannten Dimension ist."""
    return koordinate(x, y, z) is not None


def wechselkosten() -> int:
    """Belegter Festpreis eines Koordinatenwechsels (data/welten.json: 5000 Mana)."""
    return _MANA_WECHSEL


def wechsel_erlaubt(von_z: int, nach_z: int, mana: float,
                    letzter_wechsel, jetzt: float):
    """
    Prueft ein Verschiebungsritual. Rueckgabe: (erlaubt: bool, meldung: str).

    Verlangt: beide Dimensionen bekannt, genug Mana in EINER Siedlung und
    seit dem letzten Wechsel mindestens 24 Stunden Abstand. 'letzter_wechsel'
    ist ein Zeitstempel in Sekunden oder None (noch nie gewechselt); 'jetzt'
    ist die aktuelle Zeit in Sekunden.
    """
    if not _ist_dimension(von_z):
        return (False, f"Unbekannte Ausgangs-Dimension: {von_z}")
    if not _ist_dimension(nach_z):
        return (False, f"Unbekannte Ziel-Dimension: {nach_z}")
    kosten = wechselkosten()
    if mana < kosten:
        return (False, f"Zu wenig Mana in einer Siedlung: {kosten} benoetigt, "
                       f"{mana} vorhanden.")
    if letzter_wechsel is not None:
        sperre = _STUNDEN_SPERRE * 3600
        wartete = jetzt - letzter_wechsel
        if wartete < sperre:
            rest_h = (sperre - wartete) / 3600.0
            return (False, f"Erst nach {_STUNDEN_SPERRE} Stunden wieder moeglich; "
                           f"noch {rest_h:.2f} h warten.")
    return (True, f"Koordinatenwechsel moeglich: {kosten} Mana aus einer Siedlung.")


def nach_wechsel(mana: float, jetzt: float) -> dict:
    """
    Bucht den Wechsel ab: neues Mana und neuer Sperr-Zeitstempel.

    Der Festpreis wird GENAU EINMAL abgezogen. Rueckgabe:
    {'mana': alter Wert minus Festpreis, 'letzter_wechsel': jetzt,
     'kosten': der abgezogene Festpreis}.
    Wirft ValueError, wenn in der Siedlung zu wenig Mana liegt — dann wurde
    nichts abgebucht.
    """
    kosten = wechselkosten()
    if mana < kosten:
        raise ValueError(f"Zu wenig Mana in einer Siedlung: {kosten} benoetigt, "
                         f"{mana} vorhanden.")
    return {"mana": mana - kosten, "letzter_wechsel": jetzt, "kosten": kosten}


def portalfarbe(z, eigene_dimensionen=()) -> str:
    """
    'gruen', wenn Dimension z eine eigene ist, sonst 'rot'.

    Nutzt die belegten Bannerfarben aus data/welten.json. Ohne Spielerwelt-
    Daten wird je Dimension gefaerbt, nicht je Feld (siehe Modulkopf).
    """
    eigene = set(eigene_dimensionen)
    return _BANNER["eigene_welt"] if z in eigene else _BANNER["fremde_welten"]


def anzeige_raster(z: int, radius: int = 10, eigene_dimensionen=()) -> list:
    """
    Die Portalanzeige fuer Dimension z als Liste ihrer Felder.

    radius = halbe Kantenlaenge des gezeigten Ausschnitts; der Standard 10
    zeigt das ganze Raster (x/y von 0 bis 19) mit genau 20 x 20 = 400
    Feldern. Jedes Feld traegt x, y, z, 'eigen' (bool), 'status'
    ('eigen'/'fremd') und 'farbe' (Bannerfarbe aus data/welten.json).
    Ohne Spielerwelt-Daten wird grob je Dimension gefaerbt.
    """
    farbe = portalfarbe(z, eigene_dimensionen)
    eigene = farbe == _BANNER["eigene_welt"]
    kante = _FELDER_AXIS
    halb = int(radius)
    if halb < 0:
        halb = 0
    mitte = kante // 2                       # 10
    von = max(0, mitte - halb)
    bis = min(kante, mitte + halb)
    felder = []
    for y in range(von, bis):
        for x in range(von, bis):
            felder.append({
                "x": x,
                "y": y,
                "z": z,
                "eigen": eigene,
                "status": "eigen" if eigene else "fremd",
                "farbe": farbe,
            })
    return felder


def beschreibung() -> str:
    """Eine lesbare Zeile ueber Limbus, Dimensionen, Raster, Kosten und Sperre."""
    kosten = wechselkosten()
    kosten_txt = f"{kosten:,}".replace(",", ".")
    return (f"Der Limbus umfasst {dim_zahl()} Dimensionen mit je "
            f"{_FELDER_AXIS} x {_FELDER_AXIS} = {feld_zahl()} Feldern; "
            f"ein Koordinatenwechsel kostet {kosten_txt} Mana aus einer Siedlung "
            f"und ist hoechstens einmal je {_STUNDEN_SPERRE} Stunden moeglich.")
