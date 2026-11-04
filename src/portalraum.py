"""
Portal- und Limbus-Raum fuer das Nebelseetal-Remake (Paket W5-2).

Belegt (Portal-Anleitung 2005, portal.php; Handbuch 2009, S. 80-83):
  * Jede Spielerwelt liegt im magischen Limbus auf Koordinaten (X, Y, Z):
    X und Y sind die Position im Raster der EIGENEN Dimension, Z ist die
    Dimension selbst.
  * Es gibt 20 Dimensionen; in jeder Dimension sind 20 x 20 = 400 Felder
    frei fuer Spielerwelten. Das ist der ORIGINAL-Stand.
  * SCHNITT W-6 (Daniel 04.11.2026): das Remake fuehrt SECHS Welten - die 14
    leeren Platzhalter-Dimensionen sind aus data/welten.json entfernt. Die
    Kennungen d01..d06 und die 400 Felder je Weltkarte bleiben unveraendert.
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

import hashlib
import random

import gelaende
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
    """Die sechs Weltkarten des Limbus (unveraendert aus src/welt.py, W-6)."""
    return welt.dimensionen()


def dim_zahl() -> int:
    """Anzahl der Weltkarten im Limbus (seit W-6: 6; im Original 20)."""
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
    """True, wenn z der Index einer bekannten Weltkarte ist (0..5, seit W-6)."""
    return _ist_ganz(z) and 0 <= z < dim_zahl()


# ---------------------------------------------------------------------------
# Zwei Zaehlweisen, EINE Umrechnung (Schnitt S-2b, 01.11.2026)
#
# Die Funktionen dieses Moduls rechnen mit dem INDEX 0..5 (welt.dimensionen()
# in Dateireihenfolge). Die Anzeige und der Spielstand fuehren dagegen die
# 1-basierte NUMMER aus der Kennung: d04 -> 4. Bis S-2a wurden beide vermischt -
# der Knopf "20" war damit unerreichbar (Index 20 gibt es nicht) und "01" zeigte
# Armageddon, waehrend der Wechsel auf Ragnaroek ging. Die Umrechnung steht
# deshalb ab jetzt an EINER Stelle.
# ---------------------------------------------------------------------------

def nummer_von(kennung) -> int:
    """1-basierte Nummer einer Weltkarte aus ihrer Kennung ('d04' -> 4). 0, wenn unbekannt."""
    text = str(kennung or "").strip().lower()
    if text.startswith("d"):
        text = text[1:]
    if not text.isdigit():
        return 0
    zahl = int(text)
    return zahl if 1 <= zahl <= dim_zahl() else 0


def kennung_von(nummer) -> str:
    """Kennung aus einer 1-basierten Nummer (4 -> 'd04'). Leer, wenn unbekannt."""
    if not _ist_ganz(nummer) or not (1 <= nummer <= dim_zahl()):
        return ""
    return str(dimensionen()[nummer - 1]["kennung"])


def index_von(nummer) -> int:
    """Index 0..5 aus einer 1-basierten Nummer (4 -> 3). -1, wenn unbekannt."""
    if not _ist_ganz(nummer) or not (1 <= nummer <= dim_zahl()):
        return -1
    return int(nummer) - 1


def nummer_von_index(index) -> int:
    """1-basierte Nummer aus einem Index (3 -> 4). 0, wenn unbekannt."""
    if not _ist_ganz(index) or not (0 <= index < dim_zahl()):
        return 0
    return int(index) + 1


def koordinate(x: int, y: int, z: int):
    """
    Beschreibt das Feld (x, y) in Dimension z — oder None.

    None, wenn x oder y ausserhalb 0..19 liegen oder z keine bekannte
    Weltkarte ist (Index 0..5 in welt.dimensionen(); die 0..19 betreffen das
    Feldraster, nicht die Zahl der Weltkarten). Das Feld traegt
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
        return (False, f"Unbekannte Ausgangswelt: {von_z}")
    if not _ist_dimension(nach_z):
        return (False, f"Unbekannte Zielwelt: {nach_z}")
    kosten = wechselkosten()
    if mana < kosten:
        return (False, f"Zu wenig Mana in einer Siedlung: {kosten} benötigt, "
                       f"{mana} vorhanden.")
    if letzter_wechsel is not None:
        sperre = _STUNDEN_SPERRE * 3600
        wartete = jetzt - letzter_wechsel
        if wartete < sperre:
            rest_h = (sperre - wartete) / 3600.0
            return (False, f"Erst nach {_STUNDEN_SPERRE} Stunden wieder möglich; "
                           f"noch {rest_h:.2f} h warten.")
    return (True, f"Koordinatenwechsel möglich: {kosten} Mana aus einer Siedlung.")


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
        raise ValueError(f"Zu wenig Mana in einer Siedlung: {kosten} benötigt, "
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


def weltkarten(eigene_nummern=(), unterwegs: int = 0) -> list:
    """
    Die SECHS belegten Weltkarten als Zeilen fuer die Portal-Uebersicht (S-2b).

    Grundlage ist Daniels Vorgabe vom 01.11.2026 (docs/KONZEPT_WELTKARTEN_UND_BOTS_20261101.md,
    Anhang 3 Frage 26/30/31): es gibt immer die sechs Weltkarten Armageddon, Ragnaroek, Utgard,
    Midgard, Valhalla und Limbus; bespielbar sind zuerst Midgard und Valhalla; die Anzeige listet
    sie mit Namen, darunter steht das Gelaendekaestchen der aktuellen Welt.

    Jede Zeile traegt:
      'nummer'      1-basierte Nummer wie im Spielstand (4 = d04)
      'kennung'     Kennung der Weltkarte ('d04')
      'name'        belegter Weltname ('Midgard')
      'spielbar'    True, wenn Daniel sie fuer bespielbar erklaert hat
      'status'      'eigen' | 'fremd' | 'nicht bespielbar'
      'status_text' deutsche Anzeige dazu
      'farbe'       Bannerfarbe als WORT ('gruen'/'rot') oder None - Tk-Farben macht die Anzeige
      'waehlbar'    True, wenn ein Weltensprung jetzt erlaubt waere
      'grund'       warum nicht waehlbar ('' wenn waehlbar)

    'unterwegs' ist die Zahl der laufenden Auftraege. Daniel, Anhang 2 (Umzug mit laufenden
    Auftraegen): "ein weltenwechsel ist fuer das dorf gar nicht moeglich solange auftraege
    einheiten truppen oder sonst was unterwegs ist auch handel z. b." Deshalb sperrt jede Zahl
    groesser 0 ALLE Weltenspruenge - nicht nur den in die eigene Welt.
    """
    eigene = set()
    for n in (eigene_nummern or ()):
        try:
            eigene.add(int(n))
        except (TypeError, ValueError):
            continue                      # unbekannte Angabe zaehlt nicht als eigene Welt
    try:
        laufend = int(unterwegs or 0)
    except (TypeError, ValueError):
        laufend = 0
    zeilen = []
    for index, eintrag in enumerate(dimensionen()):
        name = eintrag.get("welt")
        if not name:
            continue                      # ohne belegten Weltnamen ist es keine Weltkarte
        nummer = nummer_von_index(index)
        moeglich = welt.spielbar(name)
        if nummer in eigene:
            status, farbe = "eigen", _BANNER["eigene_welt"]
            status_text = "eigene Welt"
        elif moeglich:
            status, farbe = "fremd", _BANNER["fremde_welten"]
            status_text = "fremde Welt"
        else:
            status, farbe = "nicht bespielbar", None
            status_text = "noch nicht bespielbar"
        grund = ""
        if not moeglich:
            grund = "folgt später (Daniel 01.11.2026: zuerst Midgard und Valhalla)"
        elif laufend > 0:
            grund = (f"gesperrt: {laufend} Auftrag/Auftraege unterwegs "
                     f"(Daniel 01.11.2026, Anhang 2)")
        zeilen.append({
            "nummer": nummer,
            "kennung": str(eintrag.get("kennung") or ""),
            "name": str(name),
            "spielbar": moeglich,
            "status": status,
            "status_text": status_text,
            "farbe": farbe,
            "waehlbar": bool(moeglich and laufend == 0),
            "grund": grund,
        })
    return zeilen


# ---------------------------------------------------------------------------
# Das Weltbild als Gelaende (Schnitt S-5, Daniel 01.11.2026, Register 91 und 92)
#
# Vorgabe: die 20 x 20 = 400 Felder einer Weltkarte werden in 10 x 10 Gruppen von
# je 2 x 2 gleichartigem Gelaende geteilt. Die 100 Gruppen erhalten die sieben
# Gelaende-IDs in der Stueckzahl ihrer Haeufigkeit aus data/gelaende.json
# (Grasland 20, Steppe 20, Wald 18, Huegel 13, Berg 12, Nebelsee 7, Sumpf 10 = 100)
# und werden dann mit random.Random aus einem aus SHA-256 abgeleiteten Seed
# gemischt - NIE mit hash(), das ist je Prozessstart verschieden. Der Seed haengt
# an Weltkennung plus dem Konfigurationswert weltkarten_seed in data/welten.json,
# nie an der Uhrzeit; gleicher Name und gleicher Seed ergeben deshalb immer
# dasselbe Raster, auch nach einem Neustart.
#
# Das Gelaende auf der Weltkarte hat KEINE Bauplatz-, Rohstoff- oder
# Ertragswirkung - gerechnet wird ausschliesslich auf der 10 x 10-Siedlungskarte.
# Die Kartenansicht zeigt nur Gelaende, Gitterlinien, Legende und die
# voruebergehende Feldauswahl: keine Orte, Doerfer, Gegner oder Nummern.
# ---------------------------------------------------------------------------

GELAENDE_BLOCK = 2                                    # 2 x 2 Felder je Gruppe
_BLOCK_KANTE = _FELDER_AXIS // GELAENDE_BLOCK         # 10 Gruppen je Kante
_GRUPPEN = _BLOCK_KANTE * _BLOCK_KANTE                # 100 Gruppen


class WeltbildFehler(ValueError):
    """Das Weltbild laesst sich nicht bilden - mit erklaerendem Grund, nie mit Ersatzwerten."""


def gelaendeverteilung() -> list:
    """Die sieben Gelaendearten mit ihrer Haeufigkeit - EINE Quelle (data/gelaende.json)."""
    return [(aid, int(gelaende.ARTEN[aid]["haeufigkeit"])) for aid in gelaende.GELAENDEARTEN]


def weltkarten_seed() -> str:
    """Der Konfigurationswert `weltkarten_seed` aus data/welten.json (S-5, Register 94)."""
    wert = str(_DATEN.get("weltkarten_seed") or "").strip()
    if not wert:
        raise WeltbildFehler("Kein weltkarten_seed in data/welten.json - ohne Seed wird kein "
                             "Weltbild gebaut (kein Zufallsersatz).")
    return wert


def _dimension_finden(welt_arg):
    """Findet eine Dimension ueber Kennung ('d04'), Nummer (4) oder Weltnamen ('Midgard')."""
    text = str(welt_arg).strip().lower()
    for d in dimensionen():
        if text in (str(d["kennung"]).lower(), str(d["name"]).lower(),
                    str(d.get("welt") or "").lower()):
            return d
    nummer = nummer_von(text)
    if nummer:
        return dimensionen()[nummer - 1]
    if _ist_ganz(welt_arg) and 1 <= welt_arg <= dim_zahl():
        return dimensionen()[welt_arg - 1]
    return None


def _seed_zahl(kennung: str, seed: str) -> int:
    """Zahl aus SHA-256 von 'Kennung|Seed' - stabil ueber Prozessgrenzen hinweg."""
    roh = hashlib.sha256(f"{kennung}|{seed}".encode("utf-8")).digest()
    return int.from_bytes(roh[:8], "big")


_WELTBILDER = {}


def weltbild(welt_arg, seed=None) -> dict:
    """
    Das Gelaende-Raster einer Weltkarte.

    Rueckgabe: dict mit 'kennung', 'welt', 'name', 'seed', 'kantenlaenge',
    'block', 'gruppen', 'verteilung' ({art: haeufigkeit}), 'zaehlung'
    ({art: felder}) und 'raster' (20 Zeilen mit je 20 Gelaende-IDs).

    Wirft WeltbildFehler, wenn die Welt unbekannt ist, der Seed fehlt oder die
    Haeufigkeiten in data/gelaende.json nicht genau 100 Gruppen ergeben - dann
    wird NICHTS erfunden und kein Ersatzraster geliefert.
    """
    d = _dimension_finden(welt_arg)
    if d is None:
        raise WeltbildFehler(f"Unbekannte Weltkarte: {welt_arg!r}. Bekannt sind die Kennungen "
                             f"d01 bis d{dim_zahl():02d} und die sechs belegten Weltnamen.")
    seed_text = weltkarten_seed() if seed is None else str(seed).strip()
    if not seed_text:
        raise WeltbildFehler("Leerer Seed - ohne Seed wird kein Weltbild gebaut.")
    schluessel = (str(d["kennung"]), seed_text)
    if schluessel in _WELTBILDER:
        return _WELTBILDER[schluessel]

    verteilung = gelaendeverteilung()
    ids = [aid for aid, haeufig in verteilung for _ in range(haeufig)]
    if len(ids) != _GRUPPEN:
        raise WeltbildFehler(f"Die Haeufigkeiten in data/gelaende.json ergeben {len(ids)} Gruppen, "
                             f"das Raster braucht genau {_GRUPPEN} (Summe 100).")
    mischer = random.Random(_seed_zahl(str(d["kennung"]), seed_text))
    mischer.shuffle(ids)

    raster = []
    for gy in range(_BLOCK_KANTE):
        zeile = []
        for gx in range(_BLOCK_KANTE):
            zeile.extend([ids[gy * _BLOCK_KANTE + gx]] * GELAENDE_BLOCK)
        raster.append(list(zeile))
        raster.append(list(zeile))                    # eine Gruppe ist 2 x 2 Felder hoch

    zaehlung = {}
    for zeile in raster:
        for art in zeile:
            zaehlung[art] = zaehlung.get(art, 0) + 1
    bild = {
        "kennung": str(d["kennung"]),
        "welt": d.get("welt"),
        "name": d["name"],
        "seed": seed_text,
        "kantenlaenge": _FELDER_AXIS,
        "block": GELAENDE_BLOCK,
        "gruppen": _GRUPPEN,
        "verteilung": {aid: haeufig for aid, haeufig in verteilung},
        "zaehlung": zaehlung,
        "raster": raster,
    }
    _WELTBILDER[schluessel] = bild
    return {**bild, "raster": [list(z) for z in raster]}


def gelaende_von_feld(welt_arg, x, y, seed=None) -> dict:
    """
    Das Gelaende EINES Feldes - oder ein erklaerter Grund statt eines Ersatzwertes.

    Rueckgabe: dict mit x, y, welt, gelaende (ID), name, farbe und bebaubar
    (rein beschreibend - auf der Weltkarte wird nichts gebaut).
    """
    bild = weltbild(welt_arg, seed)
    if not (_ist_ganz(x) and _ist_ganz(y)):
        raise WeltbildFehler(f"Feldkoordinaten müssen ganze Zahlen sein, bekam x={x!r}, y={y!r}.")
    if not (0 <= x < _FELDER_AXIS) or not (0 <= y < _FELDER_AXIS):
        raise WeltbildFehler(f"Feld ({x}, {y}) liegt ausserhalb des Rasters 0..{_FELDER_AXIS - 1}.")
    art = bild["raster"][y][x]
    return {"x": int(x), "y": int(y), "welt": bild["welt"], "gelaende": art,
            "name": gelaende.name(art), "farbe": gelaende.farbe(art),
            "bebaubar": bool(gelaende.ist_bebaubar(art))}


def legende() -> list:
    """Die sieben Gelaendearten mit Name, Farbe und Haeufigkeit - fuer die Anzeige unter der Karte."""
    return [{"gelaende": aid, "name": gelaende.name(aid), "farbe": gelaende.farbe(aid),
             "haeufigkeit": haeufig} for aid, haeufig in gelaendeverteilung()]


def anzeige_raster(z: int, radius: int = 10, eigene_dimensionen=()) -> list:
    """
    Die Portalanzeige fuer Dimension z als Liste ihrer Felder.

    radius = halbe Kantenlaenge des gezeigten Ausschnitts; der Standard 10
    zeigt das ganze Raster (x/y von 0 bis 19) mit genau 20 x 20 = 400
    Feldern. Jedes Feld traegt x, y, z, 'eigen' (bool), 'status'
    ('eigen'/'fremd') und 'farbe' (Bannerfarbe aus data/welten.json).
    Ohne Spielerwelt-Daten wird grob je Dimension gefaerbt.

    Seit S-5 (01.11.2026, Register 91) kommt das Gelaende JE FELD dazu:
    'gelaende' (ID aus data/gelaende.json), 'gelaende_name', 'gelaende_farbe'
    und 'gelaende_bebaubar'. Die Bannerfarbe 'farbe' bleibt unveraendert, damit
    die belegte Originalanzeige (eigene Welt gruen, fremde rot) erhalten bleibt.
    Laesst sich kein Weltbild bilden, steht der Grund in 'gelaende_grund' und
    'gelaende' bleibt None - es wird kein Gelaende erfunden.
    """
    farbe = portalfarbe(z, eigene_dimensionen)
    eigene = farbe == _BANNER["eigene_welt"]
    bild = None
    grund = ""
    if _ist_dimension(z):
        try:
            bild = weltbild(dimensionen()[z]["kennung"])
        except WeltbildFehler as fehler:
            bild, grund = None, str(fehler)
    else:
        grund = (f"Unbekannte Weltkarte: {z!r} ist kein Index von 0 bis {dim_zahl() - 1} - "
                 f"es wird kein Gelände erfunden.")
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
            art = bild["raster"][y][x] if bild else None
            felder.append({
                "x": x,
                "y": y,
                "z": z,
                "eigen": eigene,
                "status": "eigen" if eigene else "fremd",
                "farbe": farbe,
                "gelaende": art,
                "gelaende_name": gelaende.name(art) if art else None,
                "gelaende_farbe": gelaende.farbe(art) if art else None,
                "gelaende_bebaubar": bool(gelaende.ist_bebaubar(art)) if art else None,
                "gelaende_grund": grund,
            })
    return felder


def beschreibung() -> str:
    """Eine lesbare Zeile ueber Limbus, Dimensionen, Raster, Kosten und Sperre."""
    kosten = wechselkosten()
    kosten_txt = f"{kosten:,}".replace(",", ".")
    return (f"Der Limbus umfasst {dim_zahl()} Weltkarten mit je "
            f"{_FELDER_AXIS} x {_FELDER_AXIS} = {feld_zahl()} Feldern; "
            f"ein Weltensprung kostet {kosten_txt} Mana aus einer Siedlung "
            f"und ist höchstens einmal je {_STUNDEN_SPERRE} Stunden möglich.")
