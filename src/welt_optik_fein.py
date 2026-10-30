"""
FEINERE Zeichenplaene fuer die WELTkarte des Nebelseetal-Remakes (naechste Ausbaustufe).

Dieses Modul ist die feinere Nachfolgegeneration von ``src/welt_optik.py`` und aendert dieses
NICHT. Es liefert NUR DATEN — eine Liste von Zeichenbefehlen ("Plan") je Element — und zeichnet
selbst nichts. Es braucht daher weder ein Fenster noch tkinter, Pillow, Emoji oder Zufall; die
Plaene sind ohne Anzeige pruefbar (tests/test_welt_optik_fein.py).

Quelle ALLER Zahlen:
  archiv/analysen/audits/ux_astra_karten_feinheit_2026-10-05.txt
  Abschnitte "Welt 1 – Landschaft", "Welt 2 – Orte und Beschriftung", "Welt 3 – Orientierung".
Jede Modulkonstante nennt die Fundstelle im Kommentar. Die dort genannten Grundmaße gelten bei
48 px je Feld (``MASS_PX``); alle anderen Zoomstufen werden daraus mit ``zelle / 48`` skaliert.
Zusaetzlich stammen die Gelaendefarben der Uebersichtskarte und die Regionsnamen read-only aus
``src/main.py`` (WELT_GELAENDEFARBEN / WELT_REGIONEN).

Plan-Eintrag (ein dict je Zeichenbefehl) — gleiches Format wie ``src/welt_optik.py``:
  'form'   : 'polygon' | 'rectangle' | 'oval' | 'line' | 'text' | 'arc'
  'punkte' : flache [x, y, x, y, ...]-Liste — fuer 'polygon' und 'line'
  'box'    : [x1, y1, x2, y2] — fuer 'rectangle', 'oval' und 'arc'
  'punkt'  : [x, y] — fuer 'text' (Textposition)
  'farbe'  : Fuellfarbe (hex) — bei 'line' und 'text' die Linien-/Textfarbe
  'rand'   : Umrissfarbe (hex)
  'breite' : Linien-/Randbreite in px
  'text'   : Text fuer 'text'
  'font'   : Schrift als Tupel, z. B. ('TkDefaultFont', 18, 'bold') fuer 'text'
  'anker'  : Verankerung fuer 'text'
  'winkel' / 'weite' / 'stil' / 'glatt' : wie in src/welt_optik.py

Zusaetzliche Kennschluessel dieses Moduls (aendern die Zeichnung NICHT, nur die Pruefung):
  'kante'    : 'norden' | 'sueden' | 'westen' | 'osten' an einer 1-px-Rasterlinie
  'ufersaum' : Himmelsrichtung des Ufersaums (Land/Wasser-Grenze, Band #938A70)
  'ortszeichen' : 'dorf' | 'ruine' | 'lager' bzw. 'eigen' an Silhouetten/Fahne

Alle Plaene sind DETERMINISTISCH: gleiche Feldkoordinaten ergeben byte-identische Plaene. Alle
Koordinaten liegen im Zellenkasten [x0, x0+zelle] x [y0, y0+zelle].
"""
from __future__ import annotations

# --------------------------------------------------------------------------
# Grundmaße und erlaubte Formen
# --------------------------------------------------------------------------

# astra: alle Zahlen gelten "bei 48 px" je Feld (Welt 1/2/3 durchgaengig).
MASS_PX = 48.0

# Die sechs erlaubten Zeichenformen (identisch zu src/welt_optik.py).
FORMEN = ("polygon", "rectangle", "oval", "line", "text", "arc")

# Die sechs Gelaendearten der WELTkarte (Reihenfolge wie main.WELT_GELAENDEREIHENFOLGE,
# read-only uebernommen am 05.10.2026).
GELAENDEARTEN = ("forest", "plains", "mountain", "water", "village", "ruins")

# --------------------------------------------------------------------------
# WELT 1 – Landschaft (astra, Abschnitt "Welt 1 – Landschaft")
# --------------------------------------------------------------------------

WELT1_EBENE = "#707B58"            # astra: "Ebene #707B58"
WELT1_WALD = "#405A43"             # astra: "Wald #405A43"
WELT1_GEBIRGE = "#75766F"          # astra: "Gebirge #75766F"
WELT1_WASSER = "#405F70"           # astra: "Wasser #405F70"

WELT1_RASTER = "#38433C"           # astra: "Rasterlinien nur 1 px in #38433C"
WELT1_RASTER_BREITE = 1            # astra: "1 px"

# astra: "Lichtfarben #637451, #96958A und #658594 verwenden." (drei Lichtfarben fuer vier
# Gelaendearten)
WELT1_LICHT_GRUEN = "#637451"      # astra Lichtfarbe — gilt fuer die EBENE
WELT1_LICHT_GEBIRGE = "#96958A"    # astra Lichtfarbe (Gebirge)
WELT1_LICHT_WASSER = "#658594"     # astra Lichtfarbe (Wasser)

# Der WALD bekommt eine EIGENE Lichtfarbe — Vorgabe Daniel 05.10.2026 ("trennen: der Wald
# bekommt eine aus seiner eigenen Farbe abgeleitete Lichtfarbe"). astra nennt nur drei
# Lichtfarben fuer vier Gelaendearten, deshalb lag #637451 sonst auf Ebene UND Wald.
# Die Ableitung ist GERECHNET, nicht erfunden: astra gibt zu zwei Gelaendearten Basis UND
# Lichtfarbe; daraus laesst sich der Aufhellungsgrad ablesen (heller Richtung Weiss, Faktor f):
#   Gebirge #75766F -> #96958A:  f = 0.239 / 0.226 / 0.188 -> Mittel 0.218
#   Wasser  #405F70 -> #658594:  f = 0.194 / 0.238 / 0.252 -> Mittel 0.228
# Mittel aus beiden Paaren: 0.223 -> gerundet 0.22. Diesen Faktor bekommt der Wald auf SEINE
# eigene Grundfarbe #405A43 angewandt.
LICHT_ABLEITUNG_FAKTOR = 0.22


def _aufhellen(farbe: str, faktor: float) -> str:
    """Hellere Ableitung einer vorhandenen Farbe — GERECHNET, kein erfundener Farbwert."""
    roh = str(farbe).lstrip("#")
    teile = [int(roh[i:i + 2], 16) for i in (0, 2, 4)]
    hell = [round(v + (255 - v) * faktor) for v in teile]
    return "#" + "".join(f"{max(0, min(255, v)):02X}" for v in hell)


WELT1_LICHT_WALD = _aufhellen(WELT1_WALD, LICHT_ABLEITUNG_FAKTOR)

WELT1_UFER = "#938A70"             # astra: "an Ufern ein 2–3 px breites Band #938A70"
WELT1_UFER_MIN = 2                 # astra: "2–3 px breit"
WELT1_UFER_MAX = 3

WELT1_WALD_GRUPPEN_MIN = 2         # astra: "Wald mit zwei bis drei ... Baumgruppen"
WELT1_WALD_GRUPPEN_MAX = 3
WELT1_WALD_BREITE_MIN = 10         # astra: "10–16 px breit"
WELT1_WALD_BREITE_MAX = 16

WELT1_GRAT_ANZAHL = 2              # astra: "Gebirge mit zwei ... Gratpolygonen"
WELT1_GRAT_BREITE_MIN = 16         # astra: "16–22 px"
WELT1_GRAT_BREITE_MAX = 22

WELT1_WELLE_MIN = 2                # astra: "Wasser mit zwei ... Wellenlinien"
WELT1_WELLE_MAX = 3
WELT1_WELLE_LAENGE_MIN = 12        # astra: "12–18 px lang"
WELT1_WELLE_LAENGE_MAX = 18

WELT1_BEFEHLE_MIN = 4              # astra: "Etwa 4–11 Befehle je Feld, bei Wald bis etwa 14."
WELT1_BEFEHLE_MAX = 11
WELT1_BEFEHLE_WALD_MAX = 14

# --------------------------------------------------------------------------
# WELT 2 – Orte und Beschriftung (astra, Abschnitt "Welt 2 – Orte und Beschriftung")
# --------------------------------------------------------------------------

WELT2_ORTSZEICHEN_BREITE = 24      # astra: "Ortszeichen auf etwa 24 x 28 px begrenzen"
WELT2_ORTSZEICHEN_HOEHE = 28

WELT2_WAND = "#B9A582"             # astra: "Wände #B9A582"
WELT2_DACH = "#81503F"             # astra: "Dächer #81503F"
WELT2_RUINE = "#969083"            # astra: "Ruinen #969083"
WELT2_KONTUR = "#292B27"           # astra: "dunkle Konturen #292B27"

WELT2_SOCKEL = "#356D98"           # astra: "blauer Sockel ... in #356D98"
WELT2_SOCKEL_BREITE = 20           # astra: "20 x 6 px"
WELT2_SOCKEL_HOEHE = 6
WELT2_MAST = "#D8D3BD"             # astra: "Mast 2 x 21 px in #D8D3BD"
WELT2_MAST_BREITE = 2
WELT2_MAST_HOEHE = 21
WELT2_FAHNE = "#F2EEDB"            # astra: "weiße Fahne 12 x 8 px in #F2EEDB"
WELT2_FAHNE_BREITE = 12
WELT2_FAHNE_HOEHE = 8

WELT2_REGION_FARBE = "#D7CEB4"     # astra: "Regionsnamen ... #D7CEB4"
WELT2_REGION_SCHATTEN = "#26312B"  # astra: "um 1 px versetztem dunklem Textschatten #26312B"
WELT2_REGION_SCHRIFT = 18          # astra: "etwa 18 px Schriftgröße"
WELT2_REGION_VERSATZ = 1           # astra: "um 1 px versetzt"

WELT2_ORT_BEFEHLE_MIN = 7          # astra: "etwa 7–13 Befehle je Ort"
WELT2_ORT_BEFEHLE_MAX = 13
WELT2_FAHNE_BEFEHLE_MIN = 4        # astra: "etwa 4–5 für die eigene Fahne"
WELT2_FAHNE_BEFEHLE_MAX = 5

# --------------------------------------------------------------------------
# WELT 3 – Orientierung, Auswahl, Panel (astra, Abschnitt "Welt 3 – Orientierung")
# --------------------------------------------------------------------------

WELT3_AUSWAHL_GOLD = "#E4C77D"     # astra: "goldene Markierung #E4C77D"
WELT3_AUSWAHL_DUNKEL = "#17212B"   # astra: "dunkle Unterkontur" (Siedlung nennt #172128)
WELT3_AUSWAHL_EINRUECKUNG = 2      # astra: "aber 2 px eingerückt"
WELT3_AUSWAHL_ECKE = 6             # astra: "mit 6 px langen Eckwinkeln"

WELT3_UEBERSICHT_KACHEL = 4        # astra: "Übersicht ... mit 4 x 4 px je Weltfeld"
WELT3_SICHT_RAHMEN = "#F2EEDB"     # astra: "Sichtausschnitt mit weißem 1-px-Rahmen #F2EEDB"
WELT3_SICHT_RAHMEN_BREITE = 1      # astra: "1-px-Rahmen"

# astra: "Rechtes Detailpanel fest etwa 248 px breit, 12 px Innenabstand, Schrift etwa 14 px,
#         Titel 18 px"
PANEL_BREITE = 248
PANEL_INNENABSTAND = 12
PANEL_SCHRIFT = 14
PANEL_TITEL = 18

# Uebersichtsfarben je Gelaende. Quelle: src/main.py, Konstante WELT_GELAENDEFARBEN
# (read-only kopiert am 05.10.2026). Unbekannte Gelaendearten bekommen KEINE Fuellung.
_GELAENDEFARBEN = {
    "forest": "#2F4A2E", "plains": "#6E7A3A", "mountain": "#5B5F63",
    "water": "#1F4E6E", "village": "#8A6A2A", "ruins": "#4A3B63",
}

# Regionsnamen der 3x3-Einteilung. Quelle: src/main.py, Konstante WELT_REGIONEN
# (read-only kopiert am 05.10.2026; Reihenfolge Nordwest..Suedost).
_REGIONNAMEN = ("Nordwesten", "Norden", "Nordosten",
                "Westen", "Zentrum", "Osten",
                "Südwesten", "Süden", "Südosten")

# Deutsche Kurznamen fuer die Nachbarpruefung (astra-Beispiel nennt {'norden':'wald'}).
_NACHBAR_ALIAS = {
    "wald": "forest", "forst": "forest",
    "ebene": "plains", "wiese": "plains",
    "gebirge": "mountain", "berg": "mountain",
    "wasser": "water", "see": "water",
    "dorf": "village", "siedlung": "village",
    "ruine": "ruins", "ruinen": "ruins",
}

# Himmelsrichtungen der Nachbarfelder, im Uhrzeigersinn.
_HIMMEL = ("norden", "sueden", "westen", "osten")


# --------------------------------------------------------------------------
# Kleine Hilfen
# --------------------------------------------------------------------------

def _skala(zelle: float) -> float:
    """Skalenfaktor gegenueber den astra-Grundmassen bei 48 px."""
    return float(zelle) / MASS_PX


def _p(x0: float, y0: float, zelle: float, u: float, v: float) -> list:
    """[x, y] aus relativen Zellenkoordinaten (0..1)."""
    return [x0 + u * zelle, y0 + v * zelle]


def _flaech(zelle: float, rel: float) -> float:
    """Relative Breite/Hoehe (0..1) in px umrechnen."""
    return rel * zelle


def _norm_art(art) -> str | None:
    """Gelaendekuerzel vereinheitlichen (englische und deutsche Schreibweise)."""
    if art is None:
        return None
    k = str(art).lower()
    return _NACHBAR_ALIAS.get(k, k)


def _ist_wasser(art: str | None) -> bool:
    return art == "water"


def _variante(feld: tuple) -> tuple:
    """DETERMINISTISCHE Variante aus den Feldkoordinaten (astra: 'nichts springt beim Neuzeichnen').

    Rueckgabe: (spiegeln, verschiebung) — spiegeln, wenn (x+y) ungerade; Verschiebung
    (x*7 + y*13) % 3 (0, 1 oder 2 Schritte). Gleiche Koordinaten -> immer gleiche Variante.
    """
    x, y = int(feld[0]), int(feld[1])
    return ((x + y) % 2, (x * 7 + y * 13) % 3)


def _uv(feld: tuple, u: float, v: float) -> tuple:
    """Ornamentkoordinate (0..1) mit der Feldvariante spiegeln/verschieben."""
    spiegeln, schieb = _variante(feld)
    if spiegeln:
        u = 1.0 - u
    u = u + schieb * 0.03
    return u, v


def zoom_detail(zelle: int) -> str:
    """Detailstufe zu einer Zellgroesse (astra Welt 2: 'bei 16/24 ... bei 32 ... ab 48').

    'einfach' fuer zelle <= 24, 'reduziert' fuer 32 (und bis unter 48), 'voll' fuer >= 48.
    """
    z = int(zelle)
    if z <= 24:
        return "einfach"
    if z < 48:
        return "reduziert"
    return "voll"


def detail_masse() -> dict:
    """Maße des rechten Detailpanels (astra Welt 3: "248 px breit, 12 px Innenabstand,
    Schrift etwa 14 px, Titel 18 px")."""
    return {"breite": PANEL_BREITE, "innenabstand": PANEL_INNENABSTAND,
            "schrift": PANEL_SCHRIFT, "titel": PANEL_TITEL}


# --------------------------------------------------------------------------
# WELT 1 – Gelaendezeichen EINES Feldes (mit Nachbarschaft und zoomabhaengigen Details)
# --------------------------------------------------------------------------

def gelaende_plan_fein(art: str, x0: float, y0: float, zelle: float,
                       feld: tuple = (0, 0), nachbarn: dict | None = None) -> list[dict]:
    """Zeichenplan fuer EIN Gelaendefeld der Weltkarte.

    ``art`` ist eine der sechs Kennungen aus ``GELAENDEARTEN`` ('forest', 'plains', 'mountain',
    'water', 'village', 'ruins'); eine unbekannte Art wirft ValueError mit diesen sechs
    Schluesseln. ``feld`` = (x, y) waehlt die DETERMINISTISCHE Variante: gleiche Feldkoordinaten
    ergeben byte-identische Plaene. ``nachbarn`` ist ein dict wie {'norden': 'wald'} (englische
    oder deutsche Kuerzel): bei einem gleichartigen Nachbarn entfaellt die Innenkante
    (astra Welt 1: 'keine zusätzliche Innenkante'), an einer Land/Wasser-Grenze erscheint der
    2–3 px breite Ufersaum #938A70. Der Plan enthaelt die Gelaendefläche, die noetigen
    1-px-Rasterlinien (#38433C), Ufersaeume und je Gelaendeart 2 bis 6 Strukturformen; bei
    kleiner Zelle (zoom_detail 'einfach'/'reduziert') fallen Formen weg.
    """
    if art not in GELAENDEARTEN:
        raise ValueError(
            f"Unbekannte Gelaendeart der Weltkarte: {art!r} — erwartet eine von "
            f"{', '.join(GELAENDEARTEN)}")
    stufe = zoom_detail(int(zelle))
    farben = {"forest": WELT1_WALD, "plains": WELT1_EBENE, "mountain": WELT1_GEBIRGE,
              "water": WELT1_WASSER, "village": WELT2_WAND, "ruins": WELT2_RUINE}
    # Gelaendeflaeche: ein Rechteck ohne Umriss (die Innenkanten macht _kanten).
    formen: list[dict] = [{
        "form": "rectangle",
        "box": [x0, y0, x0 + zelle, y0 + zelle],
        "farbe": farben[art],
    }]
    formen += _kanten(art, x0, y0, zelle, feld, nachbarn)
    formen += _schmuck(art, x0, y0, zelle, feld, stufe)
    return formen


def _kanten(art: str, x0: float, y0: float, zelle: float, feld: tuple,
            nachbarn: dict | None) -> list[dict]:
    """1-px-Rasterlinien und Ufersaeume abhaengig von den Nachbarfeldern."""
    nb_dict = nachbarn or {}
    x, y = int(feld[0]), int(feld[1])
    breite = WELT1_UFER_MIN + ((x + y) % 2)     # astra 2–3 px, deterministisch
    formen: list[dict] = []
    for kante in _HIMMEL:
        nb = _norm_art(nb_dict.get(kante))
        if nb == art:
            continue                            # gleichartiger Nachbar: KEINE Innenkante
        if nb is not None and nb in GELAENDEARTEN and (_ist_wasser(nb) != _ist_wasser(art)):
            formen.append(_ufersaum(kante, x0, y0, zelle, breite))
        else:
            formen.append(_rasterlinie(kante, x0, y0, zelle))
    return formen


def _rasterlinie(kante: str, x0: float, y0: float, zelle: float) -> dict:
    """1-px-Rasterlinie #38433C entlang einer Zellkante."""
    if kante == "norden":
        punkte = [x0, y0, x0 + zelle, y0]
    elif kante == "sueden":
        punkte = [x0, y0 + zelle, x0 + zelle, y0 + zelle]
    elif kante == "westen":
        punkte = [x0, y0, x0, y0 + zelle]
    else:
        punkte = [x0 + zelle, y0, x0 + zelle, y0 + zelle]
    return {"form": "line", "punkte": punkte, "farbe": WELT1_RASTER,
            "breite": WELT1_RASTER_BREITE, "kante": kante}


def _ufersaum(kante: str, x0: float, y0: float, zelle: float, breite: float) -> dict:
    """2–3 px breites Band #938A70 an einer Land/Wasser-Grenze (innen in der Zelle)."""
    if kante == "norden":
        box = [x0, y0, x0 + zelle, y0 + breite]
    elif kante == "sueden":
        box = [x0, y0 + zelle - breite, x0 + zelle, y0 + zelle]
    elif kante == "westen":
        box = [x0, y0, x0 + breite, y0 + zelle]
    else:
        box = [x0 + zelle - breite, y0, x0 + zelle, y0 + zelle]
    return {"form": "rectangle", "box": box, "farbe": WELT1_UFER, "ufersaum": kante}


def _schmuck(art: str, x0: float, y0: float, zelle: float, feld: tuple,
             stufe: str) -> list[dict]:
    """Gelaendeformen je Art; Anzahl haengt von der Detailstufe ab."""
    if art == "plains":
        return _ebene_fein(x0, y0, zelle, feld, stufe)
    if art == "forest":
        return _wald_fein(x0, y0, zelle, feld, stufe)
    if art == "mountain":
        return _gebirge_fein(x0, y0, zelle, feld, stufe)
    if art == "water":
        return _wasser_fein(x0, y0, zelle, feld, stufe)
    if art == "village":
        return _dorf_feld_fein(x0, y0, zelle, feld, stufe)
    return _ruine_feld_fein(x0, y0, zelle, feld, stufe)


def _ebene_fein(x0: float, y0: float, zelle: float, feld: tuple, stufe: str) -> list[dict]:
    """Ebene: Halmlinien (#637451). astra Welt 1 nennt nur Farbe und Befehlszahl."""
    anzahl = {"voll": 3, "reduziert": 2, "einfach": 1}[stufe]
    formen: list[dict] = []
    for u, v in ((0.20, 0.46), (0.50, 0.40), (0.80, 0.48))[:anzahl]:
        uu, vv = _uv(feld, u, v)
        formen.append({
            "form": "line",
            "punkte": [x0 + uu * zelle, y0 + vv * zelle,
                       x0 + uu * zelle, y0 + (vv - 0.14) * zelle],
            "farbe": WELT1_LICHT_GRUEN, "breite": max(1.0, _skala(zelle))})
    return formen


def _wald_fein(x0: float, y0: float, zelle: float, feld: tuple, stufe: str) -> list[dict]:
    """Wald: zwei bis drei Baumgruppen 10–16 px breit (dunkle Krone + Lichtkrone)."""
    x, y = int(feld[0]), int(feld[1])
    if stufe == "einfach":
        uu, vv = _uv(feld, 0.50, 0.60)
        return [{"form": "polygon",
                 "punkte": _p(x0, y0, zelle, uu - 0.15, vv) + _p(x0, y0, zelle, uu, vv - 0.30)
                 + _p(x0, y0, zelle, uu + 0.15, vv),
                 "farbe": WELT1_WALD}]
    if stufe == "reduziert":
        gruppen = 1
    else:
        gruppen = WELT1_WALD_GRUPPEN_MIN + ((x * 3 + y * 5) % 2)   # 2 oder 3
    zentren = ((0.26, 0.60), (0.53, 0.56), (0.79, 0.62))
    breiten = (12.0, 10.0, 14.0)                                    # px, innerhalb 10–16
    formen: list[dict] = []
    for i in range(gruppen):
        u, v = zentren[i]
        hw = (breiten[i] / 2.0) / MASS_PX
        uu, vv = _uv(feld, u, v)
        formen.append({"form": "polygon",
                       "punkte": _p(x0, y0, zelle, uu - hw, vv)
                       + _p(x0, y0, zelle, uu, vv - 0.30)
                       + _p(x0, y0, zelle, uu + hw, vv),
                       "farbe": WELT1_WALD})
        formen.append({"form": "polygon",
                       "punkte": _p(x0, y0, zelle, uu - hw * 0.55, vv - 0.05)
                       + _p(x0, y0, zelle, uu, vv - 0.24)
                       + _p(x0, y0, zelle, uu + hw * 0.55, vv - 0.05),
                       "farbe": WELT1_LICHT_WALD})
    return formen


def _gebirge_fein(x0: float, y0: float, zelle: float, feld: tuple, stufe: str) -> list[dict]:
    """Gebirge: bis zu zwei Gratpolygone 16–22 px breit mit Lichtflaeche #96958A."""
    if stufe == "einfach":
        uu, vv = _uv(feld, 0.50, 0.78)
        return [{"form": "polygon",
                 "punkte": _p(x0, y0, zelle, uu - 0.20, vv) + _p(x0, y0, zelle, uu, vv - 0.46)
                 + _p(x0, y0, zelle, uu + 0.20, vv),
                 "farbe": WELT1_GEBIRGE}]
    anz = WELT1_GRAT_ANZAHL if stufe == "voll" else 1
    grats = ((0.36, 0.78, 0.32, 16.0), (0.64, 0.80, 0.38, 18.0))    # px, innerhalb 16–22
    formen: list[dict] = []
    for i in range(anz):
        u, v, spitze, wpx = grats[i]
        hw = (wpx / 2.0) / MASS_PX
        uu, vv = _uv(feld, u, v)
        formen.append({"form": "polygon",
                       "punkte": _p(x0, y0, zelle, uu - hw, vv)
                       + _p(x0, y0, zelle, uu, spitze)
                       + _p(x0, y0, zelle, uu + hw, vv),
                       "farbe": WELT1_GEBIRGE})
        formen.append({"form": "polygon",
                       "punkte": _p(x0, y0, zelle, uu - hw * 0.45, vv - 0.06)
                       + _p(x0, y0, zelle, uu, spitze)
                       + _p(x0, y0, zelle, uu + hw * 0.05, vv - 0.06),
                       "farbe": WELT1_LICHT_GEBIRGE})
    return formen


def _wasser_fein(x0: float, y0: float, zelle: float, feld: tuple, stufe: str) -> list[dict]:
    """Wasser: zwei bis drei Wellenlinien 12–18 px lang in #658594."""
    x, y = int(feld[0]), int(feld[1])
    if stufe == "einfach":
        anzahl = 1
    elif stufe == "reduziert":
        anzahl = 2
    else:
        anzahl = WELT1_WELLE_MIN + ((x * 7 + y * 13) % 2)           # 2 oder 3
    halb = (16.0 / 2.0) / MASS_PX                                   # 16 px lang (12–18)
    formen: list[dict] = []
    for v in (0.42, 0.56, 0.70)[:anzahl]:
        uu, vv = _uv(feld, 0.50, v)
        formen.append({
            "form": "line",
            "punkte": [x0 + (uu - halb) * zelle, y0 + vv * zelle,
                       x0 + uu * zelle, y0 + (vv - 0.05) * zelle,
                       x0 + (uu + halb) * zelle, y0 + vv * zelle],
            "farbe": WELT1_LICHT_WASSER, "breite": max(1.0, 2.0 * _skala(zelle))})
    return formen


def _dorf_feld_fein(x0: float, y0: float, zelle: float, feld: tuple, stufe: str) -> list[dict]:
    """Dorf-Feld: Wand- und Dachkoerper in den WELT-2-Farben."""
    if stufe == "einfach":
        return [{"form": "polygon",
                 "punkte": _p(x0, y0, zelle, 0.34, 0.66) + _p(x0, y0, zelle, 0.50, 0.36)
                 + _p(x0, y0, zelle, 0.66, 0.66), "farbe": WELT2_DACH, "rand": WELT2_KONTUR}]
    return [
        {"form": "rectangle", "box": [x0 + 0.32 * zelle, y0 + 0.54 * zelle,
                                      x0 + 0.68 * zelle, y0 + 0.82 * zelle],
         "farbe": WELT2_WAND, "rand": WELT2_KONTUR},
        {"form": "polygon",
         "punkte": _p(x0, y0, zelle, 0.28, 0.54) + _p(x0, y0, zelle, 0.50, 0.34)
         + _p(x0, y0, zelle, 0.72, 0.54), "farbe": WELT2_DACH, "rand": WELT2_KONTUR},
    ]


def _ruine_feld_fein(x0: float, y0: float, zelle: float, feld: tuple, stufe: str) -> list[dict]:
    """Ruinen-Feld: Mauerblock und gebrochene Mauerlinie in #969083."""
    block = {"form": "rectangle",
             "box": [x0 + 0.30 * zelle, y0 + 0.50 * zelle,
                     x0 + 0.70 * zelle, y0 + 0.84 * zelle],
             "farbe": WELT2_RUINE, "rand": WELT2_KONTUR}
    bruch = {"form": "line",
             "punkte": _p(x0, y0, zelle, 0.30, 0.50) + _p(x0, y0, zelle, 0.40, 0.40)
             + _p(x0, y0, zelle, 0.50, 0.50) + _p(x0, y0, zelle, 0.60, 0.38)
             + _p(x0, y0, zelle, 0.70, 0.50),
             "farbe": WELT2_KONTUR, "breite": max(1.0, 2.0 * _skala(zelle))}
    if stufe == "einfach":
        return [block]
    return [block, bruch]


# --------------------------------------------------------------------------
# WELT 2 – Ortsilhouetten (Dorf, Ruine, Lager)
# --------------------------------------------------------------------------

def ortsilhouette_plan(art: str, x0: float, y0: float, zelle: float) -> list[dict]:
    """Zeichenplan fuer ein Ortszeichen ('dorf', 'ruine' oder 'lager').

    Das Zeichen ist auf etwa 24 x 28 px (bei 48 px) begrenzt und mittig in der Zelle. Ein Dorf
    hat zwei Dachkoerper, eine Ruine eine gebrochene Mauerlinie, ein Lager eine niedrige
    Einfriedung. Bei 16/24 px entsteht ein einfaches Zeichen, bei 32 px eine reduzierte
    Silhouette, ab 48 px die volle Form (astra Welt 2). Eine unbekannte Art wirft ValueError.
    """
    if art not in ("dorf", "ruine", "lager"):
        raise ValueError(
            f"Unbekanntes Ortszeichen: {art!r} — erwartet 'dorf', 'ruine' oder 'lager'")
    bx, by, bweite, bhoehe = _ortskasten(x0, y0, zelle)
    stufe = zoom_detail(int(zelle))
    if art == "dorf":
        return _silhouette_dorf(bx, by, bweite, bhoehe, zelle, stufe)
    if art == "ruine":
        return _silhouette_ruine(bx, by, bweite, bhoehe, zelle, stufe)
    return _silhouette_lager(bx, by, bweite, bhoehe, zelle, stufe)


def _ortskasten(x0: float, y0: float, zelle: float) -> tuple:
    """Mittiger Zeichenkasten von etwa 24 x 28 px (bei 48 px)."""
    bweite = zelle * (WELT2_ORTSZEICHEN_BREITE / MASS_PX)
    bhoehe = zelle * (WELT2_ORTSZEICHEN_HOEHE / MASS_PX)
    return x0 + (zelle - bweite) / 2.0, y0 + (zelle - bhoehe) / 2.0, bweite, bhoehe


def _op(bx: float, by: float, bweite: float, bhoehe: float, u: float, v: float) -> list:
    """[x, y] aus relativen Koordinaten im Ortskasten (0..1)."""
    return [bx + u * bweite, by + v * bhoehe]


def _silhouette_dorf(bx, by, bweite, bhoehe, zelle, stufe) -> list[dict]:
    """Dorf mit zwei Dachkoerpern (Wände #B9A582, Dächer #81503F, Konturen #292B27)."""
    if stufe == "einfach":
        return [
            {"form": "polygon", "punkte": _op(bx, by, bweite, bhoehe, 0.10, 0.60)
             + _op(bx, by, bweite, bhoehe, 0.50, 0.24)
             + _op(bx, by, bweite, bhoehe, 0.90, 0.60), "farbe": WELT2_DACH,
             "rand": WELT2_KONTUR},
            {"form": "line", "punkte": _op(bx, by, bweite, bhoehe, 0.06, 0.92)
             + _op(bx, by, bweite, bhoehe, 0.94, 0.92), "farbe": WELT2_KONTUR,
             "breite": max(1.0, 2.0 * _skala(zelle))},
        ]
    if stufe == "reduziert":
        return [
            {"form": "rectangle", "box": _op(bx, by, bweite, bhoehe, 0.12, 0.52)
             + _op(bx, by, bweite, bhoehe, 0.62, 0.92), "farbe": WELT2_WAND,
             "rand": WELT2_KONTUR},
            {"form": "polygon", "punkte": _op(bx, by, bweite, bhoehe, 0.06, 0.52)
             + _op(bx, by, bweite, bhoehe, 0.37, 0.20)
             + _op(bx, by, bweite, bhoehe, 0.68, 0.52), "farbe": WELT2_DACH,
             "rand": WELT2_KONTUR},
            {"form": "line", "punkte": _op(bx, by, bweite, bhoehe, 0.04, 0.96)
             + _op(bx, by, bweite, bhoehe, 0.96, 0.96), "farbe": WELT2_KONTUR,
             "breite": max(1.0, 2.0 * _skala(zelle))},
        ]
    return [
        # Haus 1: Wand + Dach
        {"form": "rectangle", "box": _op(bx, by, bweite, bhoehe, 0.10, 0.52)
         + _op(bx, by, bweite, bhoehe, 0.60, 0.90), "farbe": WELT2_WAND, "rand": WELT2_KONTUR},
        {"form": "polygon", "punkte": _op(bx, by, bweite, bhoehe, 0.05, 0.52)
         + _op(bx, by, bweite, bhoehe, 0.35, 0.20)
         + _op(bx, by, bweite, bhoehe, 0.65, 0.52), "farbe": WELT2_DACH, "rand": WELT2_KONTUR},
        # Haus 2: Wand + Dach (zweiter Dachkoerper)
        {"form": "rectangle", "box": _op(bx, by, bweite, bhoehe, 0.56, 0.62)
         + _op(bx, by, bweite, bhoehe, 0.96, 0.94), "farbe": WELT2_WAND, "rand": WELT2_KONTUR},
        {"form": "polygon", "punkte": _op(bx, by, bweite, bhoehe, 0.52, 0.62)
         + _op(bx, by, bweite, bhoehe, 0.76, 0.42)
         + _op(bx, by, bweite, bhoehe, 0.99, 0.62), "farbe": WELT2_DACH, "rand": WELT2_KONTUR},
        # Tür und Fenster
        {"form": "rectangle", "box": _op(bx, by, bweite, bhoehe, 0.30, 0.68)
         + _op(bx, by, bweite, bhoehe, 0.42, 0.90), "farbe": WELT2_KONTUR},
        {"form": "rectangle", "box": _op(bx, by, bweite, bhoehe, 0.72, 0.74)
         + _op(bx, by, bweite, bhoehe, 0.84, 0.84), "farbe": WELT2_KONTUR},
        # Bodenlinie
        {"form": "line", "punkte": _op(bx, by, bweite, bhoehe, 0.04, 0.96)
         + _op(bx, by, bweite, bhoehe, 0.96, 0.96), "farbe": WELT2_KONTUR,
         "breite": max(1.0, 2.0 * _skala(zelle))},
    ]


def _silhouette_ruine(bx, by, bweite, bhoehe, zelle, stufe) -> list[dict]:
    """Ruine mit gebrochener Mauerlinie (#969083, Konturen #292B27)."""
    if stufe == "einfach":
        return [
            {"form": "rectangle", "box": _op(bx, by, bweite, bhoehe, 0.16, 0.42)
             + _op(bx, by, bweite, bhoehe, 0.84, 0.90), "farbe": WELT2_RUINE,
             "rand": WELT2_KONTUR},
            {"form": "line", "punkte": _op(bx, by, bweite, bhoehe, 0.04, 0.94)
             + _op(bx, by, bweite, bhoehe, 0.96, 0.94), "farbe": WELT2_KONTUR,
             "breite": max(1.0, 2.0 * _skala(zelle))},
        ]
    if stufe == "reduziert":
        return [
            {"form": "polygon", "punkte": _op(bx, by, bweite, bhoehe, 0.08, 0.86)
             + _op(bx, by, bweite, bhoehe, 0.24, 0.34)
             + _op(bx, by, bweite, bhoehe, 0.42, 0.60)
             + _op(bx, by, bweite, bhoehe, 0.60, 0.24)
             + _op(bx, by, bweite, bhoehe, 0.80, 0.66)
             + _op(bx, by, bweite, bhoehe, 0.94, 0.86), "farbe": WELT2_RUINE,
             "rand": WELT2_KONTUR},
            {"form": "rectangle", "box": _op(bx, by, bweite, bhoehe, 0.24, 0.66)
             + _op(bx, by, bweite, bhoehe, 0.56, 0.90), "farbe": WELT2_RUINE},
            {"form": "line", "punkte": _op(bx, by, bweite, bhoehe, 0.04, 0.94)
             + _op(bx, by, bweite, bhoehe, 0.96, 0.94), "farbe": WELT2_KONTUR,
             "breite": max(1.0, 2.0 * _skala(zelle))},
        ]
    return [
        # gebrochene Mauerlinie
        {"form": "line", "punkte": _op(bx, by, bweite, bhoehe, 0.06, 0.84)
         + _op(bx, by, bweite, bhoehe, 0.22, 0.30)
         + _op(bx, by, bweite, bhoehe, 0.40, 0.56)
         + _op(bx, by, bweite, bhoehe, 0.58, 0.20)
         + _op(bx, by, bweite, bhoehe, 0.78, 0.62)
         + _op(bx, by, bweite, bhoehe, 0.94, 0.82), "farbe": WELT2_KONTUR,
         "breite": max(1.0, 2.0 * _skala(zelle))},
        # Mauerbloecke
        {"form": "rectangle", "box": _op(bx, by, bweite, bhoehe, 0.20, 0.64)
         + _op(bx, by, bweite, bhoehe, 0.44, 0.90), "farbe": WELT2_RUINE,
         "rand": WELT2_KONTUR},
        {"form": "rectangle", "box": _op(bx, by, bweite, bhoehe, 0.54, 0.70)
         + _op(bx, by, bweite, bhoehe, 0.78, 0.92), "farbe": WELT2_RUINE,
         "rand": WELT2_KONTUR},
        {"form": "rectangle", "box": _op(bx, by, bweite, bhoehe, 0.80, 0.78)
         + _op(bx, by, bweite, bhoehe, 0.96, 0.92), "farbe": WELT2_RUINE},
        # Mauerzacken
        {"form": "polygon", "punkte": _op(bx, by, bweite, bhoehe, 0.22, 0.64)
         + _op(bx, by, bweite, bhoehe, 0.30, 0.52)
         + _op(bx, by, bweite, bhoehe, 0.44, 0.64), "farbe": WELT2_RUINE},
        # Schutt
        {"form": "oval", "box": _op(bx, by, bweite, bhoehe, 0.10, 0.86)
         + _op(bx, by, bweite, bhoehe, 0.30, 0.96), "farbe": WELT2_RUINE},
        # Bodenlinie
        {"form": "line", "punkte": _op(bx, by, bweite, bhoehe, 0.04, 0.96)
         + _op(bx, by, bweite, bhoehe, 0.96, 0.96), "farbe": WELT2_KONTUR,
         "breite": max(1.0, 2.0 * _skala(zelle))},
    ]


def _silhouette_lager(bx, by, bweite, bhoehe, zelle, stufe) -> list[dict]:
    """Lager mit niedriger Einfriedung (Wände #B9A582, Konturen #292B27)."""
    if stufe == "einfach":
        return [
            {"form": "rectangle", "box": _op(bx, by, bweite, bhoehe, 0.14, 0.62)
             + _op(bx, by, bweite, bhoehe, 0.86, 0.90), "farbe": WELT2_WAND,
             "rand": WELT2_KONTUR},
            {"form": "line", "punkte": _op(bx, by, bweite, bhoehe, 0.04, 0.94)
             + _op(bx, by, bweite, bhoehe, 0.96, 0.94), "farbe": WELT2_KONTUR,
             "breite": max(1.0, 2.0 * _skala(zelle))},
        ]
    if stufe == "reduziert":
        return [
            {"form": "line", "punkte": _op(bx, by, bweite, bhoehe, 0.06, 0.86)
             + _op(bx, by, bweite, bhoehe, 0.06, 0.52)
             + _op(bx, by, bweite, bhoehe, 0.94, 0.52), "farbe": WELT2_KONTUR,
             "breite": max(1.0, 2.0 * _skala(zelle))},
            {"form": "polygon", "punkte": _op(bx, by, bweite, bhoehe, 0.26, 0.52)
             + _op(bx, by, bweite, bhoehe, 0.50, 0.16)
             + _op(bx, by, bweite, bhoehe, 0.74, 0.52), "farbe": WELT2_WAND,
             "rand": WELT2_KONTUR},
            {"form": "line", "punkte": _op(bx, by, bweite, bhoehe, 0.04, 0.94)
             + _op(bx, by, bweite, bhoehe, 0.96, 0.94), "farbe": WELT2_KONTUR,
             "breite": max(1.0, 2.0 * _skala(zelle))},
        ]
    return [
        # niedrige Einfriedung (offene Vorderseite = Eingang)
        {"form": "line", "punkte": _op(bx, by, bweite, bhoehe, 0.06, 0.88)
         + _op(bx, by, bweite, bhoehe, 0.06, 0.46)
         + _op(bx, by, bweite, bhoehe, 0.94, 0.46)
         + _op(bx, by, bweite, bhoehe, 0.94, 0.88), "farbe": WELT2_KONTUR,
         "breite": max(1.0, 2.0 * _skala(zelle))},
        # Zaunpfosten
        {"form": "line", "punkte": _op(bx, by, bweite, bhoehe, 0.30, 0.46)
         + _op(bx, by, bweite, bhoehe, 0.30, 0.60), "farbe": WELT2_KONTUR,
         "breite": max(1.0, 1.0 * _skala(zelle))},
        {"form": "line", "punkte": _op(bx, by, bweite, bhoehe, 0.70, 0.46)
         + _op(bx, by, bweite, bhoehe, 0.70, 0.60), "farbe": WELT2_KONTUR,
         "breite": max(1.0, 1.0 * _skala(zelle))},
        # zwei Zelte
        {"form": "polygon", "punkte": _op(bx, by, bweite, bhoehe, 0.14, 0.60)
         + _op(bx, by, bweite, bhoehe, 0.32, 0.24)
         + _op(bx, by, bweite, bhoehe, 0.50, 0.60), "farbe": WELT2_WAND,
         "rand": WELT2_KONTUR},
        {"form": "polygon", "punkte": _op(bx, by, bweite, bhoehe, 0.54, 0.62)
         + _op(bx, by, bweite, bhoehe, 0.72, 0.30)
         + _op(bx, by, bweite, bhoehe, 0.90, 0.62), "farbe": WELT2_WAND,
         "rand": WELT2_KONTUR},
        # Feuerstelle
        {"form": "oval", "box": _op(bx, by, bweite, bhoehe, 0.40, 0.74)
         + _op(bx, by, bweite, bhoehe, 0.60, 0.88), "farbe": WELT2_DACH},
        # Bodenlinie
        {"form": "line", "punkte": _op(bx, by, bweite, bhoehe, 0.04, 0.94)
         + _op(bx, by, bweite, bhoehe, 0.96, 0.94), "farbe": WELT2_KONTUR,
         "breite": max(1.0, 2.0 * _skala(zelle))},
    ]


# --------------------------------------------------------------------------
# Eigene Fahne (blauer Sockel, Mast, weisse Fahne)
# --------------------------------------------------------------------------

def fahne_plan_fein(x0: float, y0: float, zelle: float) -> list[dict]:
    """Zeichenplan fuer die Fahne des eigenen Ortes (astra Welt 2).

    Blauer Sockel 20 x 6 px #356D98, Mast 2 x 21 px #D8D3BD, weisse Fahne 12 x 8 px #F2EEDB —
    vier bis fuenf Befehle, mittig in der Zelle und vollstaendig innerhalb [x0, x0+zelle].
    """
    s = _skala(zelle)
    cx = x0 + zelle / 2.0
    sockel_b = y0 + zelle * 0.86
    sockel_w = WELT2_SOCKEL_BREITE * s
    sockel_h = WELT2_SOCKEL_HOEHE * s
    mast_h = WELT2_MAST_HOEHE * s
    fahne_w = WELT2_FAHNE_BREITE * s
    fahne_h = WELT2_FAHNE_HOEHE * s
    mast_oben = sockel_b - sockel_h - mast_h
    return [
        # blauer Sockel
        {"form": "rectangle",
         "box": [cx - sockel_w / 2.0, sockel_b - sockel_h, cx + sockel_w / 2.0, sockel_b],
         "farbe": WELT2_SOCKEL, "rand": WELT2_KONTUR, "ortszeichen": "eigen"},
        # Mast
        {"form": "line",
         "punkte": [cx, sockel_b - sockel_h, cx, mast_oben],
         "farbe": WELT2_MAST, "breite": WELT2_MAST_BREITE * s},
        # weisse Fahne (Dreieck 12 x 8 px)
        {"form": "polygon",
         "punkte": [cx, mast_oben, cx + fahne_w, mast_oben + fahne_h / 2.0,
                    cx, mast_oben + fahne_h],
         "farbe": WELT2_FAHNE, "ortszeichen": "eigen"},
        # dunkle Sockelkante (Standflaeche)
        {"form": "rectangle",
         "box": [cx - sockel_w / 2.0, sockel_b, cx + sockel_w / 2.0, sockel_b + sockel_h * 0.6],
         "farbe": WELT2_KONTUR},
    ]


# --------------------------------------------------------------------------
# WELT 3 – Auswahlrahmen (golden, 2 px eingerueckt, 6 px Eckwinkel)
# --------------------------------------------------------------------------

def auswahl_plan_fein(x0: float, y0: float, zelle: float) -> list[dict]:
    """Zeichenplan fuer die Auswahl eines Hauptkartenfeldes (astra Welt 3: "wie in der Siedlung,
    aber 2 px eingerückt und mit 6 px langen Eckwinkeln").

    Dunkle Unterkontur #17212B, darueber die goldene Markierung #E4C77D, dazu vier 6 px lange
    Eckwinkel — insgesamt sechs Befehle.
    """
    s = _skala(zelle)
    abstand = WELT3_AUSWAHL_EINRUECKUNG * s
    ecke = WELT3_AUSWAHL_ECKE * s
    x1, y1 = x0 + abstand, y0 + abstand
    x2, y2 = x0 + zelle - abstand, y0 + zelle - abstand
    formen: list[dict] = [
        {"form": "rectangle", "box": [x1, y1, x2, y2], "rand": WELT3_AUSWAHL_DUNKEL,
         "breite": 5.0 * s},
        {"form": "rectangle", "box": [x1, y1, x2, y2], "rand": WELT3_AUSWAHL_GOLD,
         "breite": 2.0 * s},
    ]
    # vier Eckwinkel als kurze Winkel (je 6 px in beide Richtungen)
    ecken = ((x1, y1, 1, 1), (x2, y1, -1, 1), (x1, y2, 1, -1), (x2, y2, -1, -1))
    for ex, ey, sx, sy in ecken:
        formen.append({
            "form": "line",
            "punkte": [ex + sx * ecke, ey, ex, ey, ex, ey + sy * ecke],
            "farbe": WELT3_AUSWAHL_GOLD, "breite": 2.0 * s})
    return formen


# --------------------------------------------------------------------------
# Regionen (WELT 2: Regionsnamen mit Schatten)
# --------------------------------------------------------------------------

def regionen_plan_fein(gitter: int, zelle: float, anzahl: int = 3) -> list[dict]:
    """Regionsbeschriftung als Zeichenplan — ZWEI Textbefehle je Regionsname (astra Welt 2).

    Je Region entsteht ein Text in #D7CEB4 (Schriftgroesse ~18 px bei 48 px) und ein um 1 px
    versetzter dunkler Schatten in #26312B. ``anzahl=3`` (3x3) ergibt also 9 Regionsnamen und
    9 Schatten (= 18 Textbefehle). Die Namen stammen read-only aus ``main.WELT_REGIONEN``.
    """
    gitter = int(gitter)
    anzahl = int(anzahl)
    if gitter <= 0:
        raise ValueError(f"gitter muss positiv sein, war {gitter!r}")
    if anzahl <= 0:
        raise ValueError(f"anzahl muss positiv sein, war {anzahl!r}")
    s = _skala(zelle)
    groesse = max(8, int(round(WELT2_REGION_SCHRIFT * s)))
    versatz = WELT2_REGION_VERSATZ * s
    kanten = [int(gitter * i / anzahl) for i in range(anzahl + 1)]
    formen: list[dict] = []
    for z in range(anzahl):
        for spalte in range(anzahl):
            xa, xb = kanten[spalte], kanten[spalte + 1]
            ya, yb = kanten[z], kanten[z + 1]
            if xb <= xa or yb <= ya:
                continue
            cx = (xa + xb) / 2.0 * zelle
            cy = (ya + yb) / 2.0 * zelle
            index = z * anzahl + spalte
            name = _REGIONNAMEN[index] if 0 <= index < len(_REGIONNAMEN) else f"Region {index + 1}"
            formen.append({
                "form": "text", "punkt": [cx + versatz, cy + versatz], "text": name,
                "farbe": WELT2_REGION_SCHATTEN, "font": ("TkDefaultFont", groesse, "bold"),
                "region": name, "rolle": "schatten"})
            formen.append({
                "form": "text", "punkt": [cx, cy], "text": name,
                "farbe": WELT2_REGION_FARBE, "font": ("TkDefaultFont", groesse, "bold"),
                "region": name, "rolle": "name"})
    return formen


# --------------------------------------------------------------------------
# Kleine Uebersichtskarte (WELT 3: 4 x 4 px je Weltfeld, ohne Gelaendeornamente)
# --------------------------------------------------------------------------

def _feld(tile, name: str, standard=None):
    """Liest einen Wert aus einem dict- oder objektfoermigen Feldeintrag (Duck-Typing)."""
    if isinstance(tile, dict):
        return tile.get(name, standard)
    return getattr(tile, name, standard)


def uebersicht_plan_fein(tiles: list, kante: float, gitter: int, orte: list = (),
                         auswahl: tuple | None = None) -> list[dict]:
    """Die kleine Uebersichtskarte als Zeichenplan (astra Welt 3: 4 x 4 px je Weltfeld).

    Je Eintrag in ``tiles`` entsteht GENAU EIN Rechteck der Kantenlaenge ``kante / gitter``
    (bei ``kante = 4 * gitter`` also 4 x 4 px), OHNE Gelaendeornamente. Die Fuellfarbe kommt aus
    dem Eintrag ('farbe') oder aus der read-only Kopie von ``main.WELT_GELAENDEFARBEN``
    ('terrain'); eine unbekannte Gelaendeart bekommt KEINE Fuellung. Zu jedem Tupel in ``orte``
    kommt ein goldener Punkt, fuer ``auswahl`` (x, y) ein goldener Rahmen mit dunkler Unterkontur.
    """
    gitter = int(gitter)
    if gitter <= 0:
        raise ValueError(f"gitter muss positiv sein, war {gitter!r}")
    kante = float(kante)
    kachel = kante / gitter
    formen: list[dict] = []
    for i, tile in enumerate(tiles):
        x = _feld(tile, "x")
        y = _feld(tile, "y")
        try:
            x = int(x)
            y = int(y)
        except (TypeError, ValueError):
            x = i % gitter
            y = i // gitter
        farbe = _feld(tile, "farbe")
        if farbe is None:
            farbe = _GELAENDEFARBEN.get(_norm_art(_feld(tile, "terrain")))
        eintrag = {"form": "rectangle",
                   "box": [x * kachel, y * kachel, (x + 1) * kachel, (y + 1) * kachel]}
        if farbe is not None:
            eintrag["farbe"] = farbe
        else:
            eintrag["rand"] = "#0B0F12"
        formen.append(eintrag)
    radius = max(1.0, kachel * 0.5)
    for ort in orte:
        try:
            ox, oy = float(ort[0]), float(ort[1])
        except (TypeError, ValueError, IndexError):
            continue
        cx, cy = (ox + 0.5) * kachel, (oy + 0.5) * kachel
        formen.append({"form": "oval", "box": [cx - radius, cy - radius, cx + radius, cy + radius],
                       "farbe": WELT3_AUSWAHL_GOLD, "ortszeichen": "ort"})
    if auswahl is not None:
        ax, ay = int(auswahl[0]), int(auswahl[1])
        rand = max(1.0, kachel * 0.15)
        x1, y1 = ax * kachel + rand, ay * kachel + rand
        x2, y2 = (ax + 1) * kachel - rand, (ay + 1) * kachel - rand
        rahmen = [x1, y1, x2, y1, x2, y2, x1, y2, x1, y1]
        formen.append({"form": "line", "punkte": rahmen, "farbe": WELT3_AUSWAHL_DUNKEL,
                       "breite": max(1.0, kachel * 0.35)})
        formen.append({"form": "line", "punkte": rahmen, "farbe": WELT3_AUSWAHL_GOLD,
                       "breite": max(1.0, kachel * 0.15), "ortszeichen": "auswahl"})
    return formen


# --------------------------------------------------------------------------
# Offene Luecken
# --------------------------------------------------------------------------

def offene_luecken() -> list[str]:
    """Was dieses Modul bewusst NICHT aus den Quellen belegen kann (ehrlich gemeldet)."""
    return [
        "astra nennt DREI Lichtfarben (#637451, #96958A, #658594) fuer VIER Gelaendearten. Die "
        "Ebene behaelt den astra-Wert #637451; der Wald bekommt eine aus SEINER Grundfarbe "
        "#405A43 GERECHNETE Lichtfarbe (Faktor 0.22 aus den beiden astra-Paaren Gebirge und "
        "Wasser) — Vorgabe Daniel 05.10.2026, kein astra-Wert.",
        "Das Handbuch 2009 nennt KEINE Regionsnamen; die neun Namen in regionen_plan_fein "
        "stammen aus der read-only Kopie von main.WELT_REGIONEN und sind ein Vorschlag.",
        "Das Handbuch nennt KEINE Zoomstufen und keine Kachelgroessen. Die Stufen und der "
        "Standard 48 stammen aus main.WELT_ZOOM_STUFEN/WELT_ZOOM_STANDARD und sind ein "
        "Vorschlag; die Detailstufen selbst stehen in astra Welt 2.",
        "Die Rasterlinien sind 1 px breit; die Umrissbreite von Auswahl und Ufersaum kann beim "
        "Zeichnen rechnerisch um die halbe Strichbreite ueber den Plan-Kasten hinausreichen.",
        "orte und auswahl der Uebersichtskarte spiegeln nur, was der Aufrufer uebergibt; dieses "
        "Modul kennt weder Siedlungen noch die aktuelle Ansicht.",
        "Die Panelmaße (248/12/14/18) sind der astra-Vorschlag aus Welt 3, keine Messung.",
    ]
