"""
Feinere Zeichenplaene fuer die Siedlungskarte des Nebelseetal-Remakes
(``src/karten_optik_fein.py``) — die naechste, FEINERE Generation neben
``src/karten_optik.py``.

Dieses Modul gibt den sieben Gelaendearten aus ``gelaende.GELAENDEARTEN`` groessere
Strukturformen, baut die 20 Originalgebaeude aus ``data/buildings.json`` als kleine Baukoerper
mit Dachflaechen, Sockel, Tuer, Fenstern und gebaeudetypischen Anbauten, zieht Ufer nur an
echten Land-Wasser-Grenzen, setzt Wege auf die Feldkanten, rahmt die Auswahl golden, zeigt die
Ausbaustufe als Pips und legt die Koordinaten in eine aeussere Rasterleiste.

Grundlage ALLER Zahlen ist die Auswertung eines Bildmodells (gpt-6-astra) an zwei echten
Bildschirmfotos:

    docs/audits/ux_astra_karten_feinheit_2026-10-05.txt

  * Abschnitt "Siedlung 1 – Gebäude"          -> Gebaeude (Baukasten)
  * Abschnitt "Siedlung 2 – Gelände und Wege" -> Gelaende, Wege
  * Abschnitt "Siedlung 3 – Auswahl und Anzeigen" -> Auswahl, Pips, Koordinaten

Die dort genannten Zahlen stehen unten als benannte Konstanten; jede traegt die Quelle im
Kommentar. Keine Zahl ist erfunden — was nicht in der Datei steht, ist aus ``zelle`` abgeleitet
(die Zahlen gelten fuer 64 px Feldgroesse und werden mit ``zelle / 64`` skaliert).

Dieses Modul liefert NUR DATEN — eine Liste von Zeichenbefehlen ("Plan") je Feld. Es zeichnet
selbst nichts und braucht daher weder ein Fenster noch tkinter, Pillow oder Emoji. Es wird auch
nichts geschrieben und kein Zufall benutzt: gleicher Aufruf -> gleicher Plan.

Plan-Eintrag (ein dict je Zeichenbefehl), wie in ``src/karten_optik.py``:
  'form'   : 'polygon' | 'rectangle' | 'oval' | 'line' | 'text' | 'arc'
  'punkte' : flache [x, y, x, y, ...]-Liste — fuer 'polygon' und 'line'
  'box'    : [x1, y1, x2, y2] — fuer 'rectangle', 'oval' und 'arc'
  'punkt'  : [x, y] — fuer 'text'
  'farbe'  : Fuellfarbe (hex, z. B. '#875241') — bei 'line' die Linienfarbe
  'rand'   : Umrissfarbe (hex)
  'breite' : Linien-/Randbreite in px (Zahl)
  'text'   : Text fuer 'text'
  'font'   : Schrift als Tupel wie ('TkDefaultFont', 9) fuer 'text'
  'anker'  : Verankerung fuer 'text' (z. B. 'nw', 'center')
  'winkel' : Startwinkel fuer 'arc' (Grad)
  'weite'  : Ausdehnung fuer 'arc' (Grad)
  'stil'   : Bogenstil fuer 'arc' ('pieslice' | 'chord' | 'arc')

Alle Koordinaten liegen im Zellenkasten [x0, x0+zelle] x [y0, y0+zelle] und sind aus ``zelle``
berechnet, damit sie bei 32, 48, 64 und 96 px funktionieren (Toleranz 1 px).
"""
from __future__ import annotations

import gelaende as _G

# --------------------------------------------------------------------------
# Die sechs erlaubten Zeichenformen (Planformat wie src/karten_optik.py).
# --------------------------------------------------------------------------
FORMEN = ("polygon", "rectangle", "oval", "line", "text", "arc")

# --------------------------------------------------------------------------
# Astra-Masse, Siedlung 1 — Gebaeude (bei 64 px Feldgroesse).
# Quelle: docs/audits/ux_astra_karten_feinheit_2026-10-05.txt, Abschnitt "Siedlung 1 – Gebäude":
#   "Bei 64 px Feldgröße einen Bereich von 44 × 46 px für Gebäude reservieren.
#    Hauptkörper etwa 30 × 22 px, Dach 38 × 16 px, Sockel 36 × 5 px; Tür 6 × 10 px,
#    Fenster 4 × 5 px."
# --------------------------------------------------------------------------
BAU_BREITE = 44.0        # "Baubereich 44 × 46 px"
BAU_HOEHE = 46.0
KOERPER_BREITE = 30.0    # "Hauptkörper etwa 30 × 22 px"
KOERPER_HOEHE = 22.0
DACH_BREITE = 38.0       # "Dach 38 × 16 px"
DACH_HOEHE = 16.0
SOCKEL_BREITE = 36.0     # "Sockel 36 × 5 px"
SOCKEL_HOEHE = 5.0
TUER_BREITE = 6.0        # "Tür 6 × 10 px"
TUER_HOEHE = 10.0
FENSTER_BREITE = 4.0     # "Fenster 4 × 5 px"
FENSTER_HOEHE = 5.0
ANBAU_BREITE = 10.0      # "Lager mit seitlichem 10 × 14-px-Anbau"
ANBAU_HOEHE = 14.0

# Farben aus demselben Abschnitt:
DACH_HELL = "#875241"        # "Dach in zwei Flächen #875241 und #59382F"
DACH_DUNKEL = "#59382F"
WAND_HELL = "#C0AD86"        # "Wände #C0AD86 und #8F795C"
WAND_DUNKEL = "#8F795C"
KONTUR = "#302924"           # "Kontur #302924"
BODENSCHATTEN = "#343B30"    # "versetzter Bodenschatten #343B30"
# "Einheitlicher Lichteinfall von links oben" -> helle Flaeche links, dunkle rechts.

# --------------------------------------------------------------------------
# Astra-Masse, Siedlung 2 — Gelaende (bei 64 px Feldgroesse).
# Quelle: ... Abschnitt "Siedlung 2 – Gelände und Wege":
#   "Ebene #74805A, Wald #455E43, Gebirge #77776C, Wasser #416875"
#   "Ebene: drei bis fünf 3–6 px lange Halmlinien."
#   "Wald: drei versetzte Baumgruppen von etwa 14 × 20 px mit Kronen #344C38 und #60734B."
#   "Gebirge: zwei 18–28 px breite Felsformen mit Lichtfläche #969385."
#   "Wasser: zwei bis drei 12–22 px lange Linien in #6D9296."
#   "Ufer ... als 3–5 px breites Polygonband #999071."
# --------------------------------------------------------------------------
EBENE_FARBE = "#74805A"
WALD_FARBE = "#455E43"
GEBIRGE_FARBE = "#77776C"
WASSER_FARBE = "#416875"

HALM_MINDEST = 3              # "drei bis fünf ... Halmlinien"
HALM_HOECHST = 5
HALM_LAENGE_MIN = 3.0         # "3–6 px lange Halmlinien"
HALM_LAENGE_MAX = 6.0
WALD_GRUPPEN = 3              # "drei versetzte Baumgruppen"
WALD_GRUPPE_BREITE = 14.0     # "etwa 14 × 20 px"
WALD_GRUPPE_HOEHE = 20.0
WALD_KRONE_DUNKEL = "#344C38"  # "Kronen #344C38 und #60734B"
WALD_KRONE_HELL = "#60734B"
FELS_FORMEN = 2               # "zwei ... Felsformen"
FELS_BREITE_MIN = 18.0        # "18–28 px breite Felsformen"
FELS_BREITE_MAX = 28.0
GEBIRGE_LICHT = "#969385"     # "Lichtfläche #969385"
WASSER_LINIEN_MIN = 2         # "zwei bis drei 12–22 px lange Linien in #6D9296"
WASSER_LINIEN_MAX = 3
WASSER_LINIE_MIN = 12.0
WASSER_LINIE_MAX = 22.0
WASSER_LINIE = "#6D9296"
UFER_BREITE_MIN = 3.0         # "3–5 px breites Polygonband #999071"
UFER_BREITE_MAX = 5.0
UFER_FARBE = "#999071"
UFER_BREITE = 4.0             # gewaehlt innerhalb 3–5 px

# --------------------------------------------------------------------------
# Astra-Masse, Siedlung 3 — Wege, Auswahl, Anzeigen (bei 64 px Feldgroesse).
# Quelle: ... Abschnitt "Siedlung 3 – Auswahl und Anzeigen":
#   "Weg 8 px breite Linie #75674F mit 4 px breiter Innenlinie #A28E69, an gemeinsamen
#    Feldkanten exakt anschließen. Keine Wege automatisch durch Wasser oder Gebäude."
#   "Bei 64 px Auswahlrechteck 3 px nach innen setzen: dunkle Unterkontur #172128 mit 5 px
#    Strichbreite, darüber #E4C77D mit 2 px. Vier 8 px lange Eckwinkel ..."
#   "Koordinaten in eine 18 px breite beziehungsweise hohe äußere Rasterleiste verlegen."
#   "Stufenpips als 4 × 4-px-Quadrate mit 2 px Abstand auf einem dunklen Streifen unter dem
#    Gebäude ..."
# --------------------------------------------------------------------------
WEG_FARBE = "#75674F"        # "8 px breite Linie #75674F"
WEG_BREITE = 8.0
WEG_INNEN_FARBE = "#A28E69"  # "4 px breite Innenlinie #A28E69"
WEG_INNEN_BREITE = 4.0

AUSWAHL_EINZUG = 3.0          # "Auswahlrechteck 3 px nach innen setzen"
AUSWAHL_UNTER_FARBE = "#172128"  # "dunkle Unterkontur #172128"
AUSWAHL_UNTER_BREITE = 5.0       # "mit 5 px Strichbreite"
AUSWAHL_GOLD = "#E4C77D"         # "darüber #E4C77D mit 2 px"
AUSWAHL_GOLD_BREITE = 2.0
AUSWAHL_ECKEN_LAENGE = 8.0       # "Vier 8 px lange Eckwinkel"

PIP_KANTE = 4.0               # "Stufenpips als 4 × 4-px-Quadrate"
PIP_ABSTAND = 2.0             # "mit 2 px Abstand"
PIP_FARBE = AUSWAHL_GOLD      # erreichte Stufe in Astra-Gold
PIP_LEER = BODENSCHATTEN      # noch nicht erreichte Stufe gedaempft

KOORDINATEN_BREITE = 18.0     # "18 px breite beziehungsweise hohe äußere Rasterleiste"
KOORDINATEN_TEXT = "#EEE2CA"  # Panel-Textfarbe aus "Siedlung 3" (Detailpanel #EEE2CA)

# Die vier Himmelsrichtungen in fester Reihenfolge (deterministisch).
RICHTUNGEN = ("norden", "osten", "sueden", "westen")

# Wasser: das Bildmodell nennt die Gelaendeart "Wasser"; im Projekt heisst sie "nebelsee".
# Beide Schreibweisen werden als Wasser erkannt.
_WASSER_ALIASE = ("wasser", "nebelsee")


# --------------------------------------------------------------------------
# Koordinaten- und Farbhilfen (alles aus zelle bzw. aus einer Astra-Farbe abgeleitet).
# --------------------------------------------------------------------------

def _randlinien(x0: float, y0: float, zelle: float) -> dict:
    """Die vier Feldkanten als {Richtung: [x1, y1, x2, y2]}."""
    return {
        "norden": [x0, y0, x0 + zelle, y0],
        "osten": [x0 + zelle, y0, x0 + zelle, y0 + zelle],
        "sueden": [x0, y0 + zelle, x0 + zelle, y0 + zelle],
        "westen": [x0, y0, x0, y0 + zelle],
    }


def _normal(art) -> object:
    """Vergleichsform einer Gelaendeart: 'wasser' und 'nebelsee' gelten als dasselbe."""
    if art in _WASSER_ALIASE:
        return "nebelsee"
    return art


def _rgb(farbe: str):
    """Hex-Farbe -> [r, g, b]."""
    f = str(farbe).lstrip("#")
    return [int(f[i:i + 2], 16) for i in (0, 2, 4)]


def _hex(rgb) -> str:
    """[r, g, b] -> Hex-Farbe (Werte auf 0..255 begrenzt)."""
    return "#" + "".join(f"{max(0, min(255, int(round(v)))):02X}" for v in rgb)


def _abdunkeln(farbe: str, faktor: float) -> str:
    """Dunklere Ableitung einer vorhandenen Farbe (kein erfundener Farbwert)."""
    return _hex([v * faktor for v in _rgb(farbe)])


def _aufhellen(farbe: str, faktor: float) -> str:
    """Hellere Ableitung einer vorhandenen Farbe (kein erfundener Farbwert)."""
    r, g, b = _rgb(farbe)
    return _hex([r + (255 - r) * faktor, g + (255 - g) * faktor, b + (255 - b) * faktor])


def _flaeche_farbe(art: str) -> str:
    """Fuellfarbe des Feldes: die vier Astra-Farben, sonst die Farbe aus data/gelaende.json."""
    if art == "grasland":
        return EBENE_FARBE
    if art == "wald":
        return WALD_FARBE
    if art == "berg":
        return GEBIRGE_FARBE
    if art == "nebelsee":
        return WASSER_FARBE
    return _G.farbe(art)


# --------------------------------------------------------------------------
# Gebaeude — Baukasten mit sieben sichtbar verschiedenen Silhouettenfamilien.
# --------------------------------------------------------------------------

# Zuordnung der 20 Gebaeude aus data/buildings.json zu den sieben Familien. Die Familie haengt
# nur von der Kennung ab (deterministisch). Die Kategorie aus buildings.json ist die Grundlage:
# 10 Produktion + 3 Werkstatt -> "produktion" (Werkstaetten zeigen dasselbe Arbeitsdetail),
# kriegerakademie -> "kaserne" (breite Front mit zwei Pfosten), diebesgilde/stellmacher ->
# "ausbildungsstaette", verteidigungswall -> "wall", bibliothek -> "bibliothek",
# haus -> "haus", lager -> "lager" (mit seitlichem Anbau).
_FAMILIE = {
    "holzfaeller": "produktion", "steinmetz": "produktion", "erzmine": "produktion",
    "tempel": "produktion", "farm": "produktion", "goldmine": "produktion",
    "schafszucht": "produktion", "rinderfarm": "produktion", "pferdezucht": "produktion",
    "jaeger": "produktion",
    "schmiede": "produktion", "bogenbauer": "produktion", "naehstube": "produktion",
    "kriegerakademie": "kaserne",
    "diebesgilde": "ausbildungsstaette", "stellmacher": "ausbildungsstaette",
    "verteidigungswall": "wall",
    "bibliothek": "bibliothek",
    "haus": "haus",
    "lager": "lager",
}

# Die sieben Familien — jede zeichnet eine andere Silhouette.
FAMILIEN = ("lager", "kaserne", "produktion", "ausbildungsstaette", "wall", "haus", "bibliothek")


def _bau_koordinaten(x0: float, y0: float, zelle: float) -> dict:
    """Hoehen und Mittellinie eines Baukoerpers.

    Der Sockel steht so hoch, dass unter dem Gebaeude noch Platz fuer den Pip-Streifen bleibt
    (Siedlung 3: "Streifen unter dem Gebäude").
    """
    s = zelle / 64.0
    cx = x0 + zelle / 2.0
    sockel_unten = y0 + 0.84 * zelle
    sockel_oben = sockel_unten - SOCKEL_HOEHE * s
    wand_oben = sockel_oben - KOERPER_HOEHE * s
    dach_oben = wand_oben - DACH_HOEHE * s
    return {"s": s, "cx": cx, "sockel_unten": sockel_unten, "sockel_oben": sockel_oben,
            "wand_oben": wand_oben, "dach_oben": dach_oben}


def _basis_bau(x0: float, y0: float, zelle: float,
               mit_tuer: bool = True, mit_fenster: bool = True) -> list[dict]:
    """Der gemeinsame Baukoerper: Bodenschatten, Sockel, zwei Wandflaechen, Dach, Tür, Fenster.

    Licht von links oben: die linke Wandflaeche und die linke Dachflaeche sind hell, die rechte
    Seite dunkel. Genau die Formen aus "Siedlung 1 – Gebäude".
    """
    k = _bau_koordinaten(x0, y0, zelle)
    s, cx = k["s"], k["cx"]
    hu = KOERPER_BREITE / 2.0     # halbe Koerperbreite in Astra-px
    hd = DACH_BREITE / 2.0        # halbe Dachbreite in Astra-px
    formen: list[dict] = []

    # versetzter Bodenschatten (nach rechts unten versetzt, 0.03*zelle ~ 2 px bei 64 px)
    versatz = 0.03 * zelle
    formen.append({"form": "rectangle", "farbe": BODENSCHATTEN,
                   "box": [cx - SOCKEL_BREITE / 2.0 * s + versatz, k["sockel_oben"],
                           cx + SOCKEL_BREITE / 2.0 * s + versatz, k["sockel_unten"] + versatz]})
    # Sockel 36 x 5
    formen.append({"form": "rectangle", "farbe": WAND_DUNKEL, "rand": KONTUR,
                   "box": [cx - SOCKEL_BREITE / 2.0 * s, k["sockel_oben"],
                           cx + SOCKEL_BREITE / 2.0 * s, k["sockel_unten"]]})
    # Wand links hell / rechts dunkel (Licht von links oben)
    formen.append({"form": "rectangle", "farbe": WAND_HELL,
                   "box": [cx - hu * s, k["wand_oben"], cx, k["sockel_oben"]]})
    formen.append({"form": "rectangle", "farbe": WAND_DUNKEL,
                   "box": [cx, k["wand_oben"], cx + hu * s, k["sockel_oben"]]})
    # Wandkontur
    formen.append({"form": "rectangle", "rand": KONTUR,
                   "box": [cx - hu * s, k["wand_oben"], cx + hu * s, k["sockel_oben"]]})
    # Dach links hell / rechts dunkel (Satteldach, First in der Mitte)
    formen.append({"form": "polygon", "farbe": DACH_HELL,
                   "punkte": [cx - hd * s, k["wand_oben"], cx, k["dach_oben"],
                              cx, k["wand_oben"]]})
    formen.append({"form": "polygon", "farbe": DACH_DUNKEL,
                   "punkte": [cx, k["dach_oben"], cx + hd * s, k["wand_oben"],
                              cx, k["wand_oben"]]})
    # Firstlinie
    formen.append({"form": "line", "farbe": KONTUR, "breite": max(1.0, 1.0 * s),
                   "punkte": [cx, k["dach_oben"], cx, k["wand_oben"]]})
    if mit_tuer:
        # Tür 6 x 10 in der Wandmitte
        formen.append({"form": "rectangle", "farbe": KONTUR, "rand": KONTUR,
                       "box": [cx - TUER_BREITE / 2.0 * s, k["sockel_oben"] - TUER_HOEHE * s,
                               cx + TUER_BREITE / 2.0 * s, k["sockel_oben"]]})
    if mit_fenster:
        # zwei Fenster 4 x 5 (links und rechts der Tür)
        for u in (-11.0, 7.0):
            formen.append({"form": "rectangle", "farbe": KONTUR,
                           "box": [cx + u * s, k["wand_oben"] + 5.0 * s,
                                   cx + (u + FENSTER_BREITE) * s, k["wand_oben"] + 10.0 * s]})
    return formen


def _familie_detail(familie: str, x0: float, y0: float, zelle: float) -> list[dict]:
    """Die gebaeudetypische Ergaenzung, die die Silhouettenfamilie sichtbar macht."""
    k = _bau_koordinaten(x0, y0, zelle)
    s, cx = k["s"], k["cx"]
    formen: list[dict] = []

    if familie == "haus":
        # Kamin und Giebelluke — das Wohnhaus
        formen.append({"form": "rectangle", "farbe": KONTUR,
                       "box": [cx + 8.0 * s, k["dach_oben"] - 3.0 * s,
                               cx + 11.0 * s, k["dach_oben"] + 3.0 * s]})
        formen.append({"form": "oval", "farbe": WAND_DUNKEL,
                       "box": [cx - 4.0 * s, k["dach_oben"] + 6.0 * s,
                               cx + 4.0 * s, k["dach_oben"] + 12.0 * s]})
    elif familie == "produktion":
        # Kamin + kleines Arbeitsdetail (Werkbank und Kiste) — "passendem kleinen Arbeitsdetail"
        formen.append({"form": "rectangle", "farbe": KONTUR,
                       "box": [cx + 6.0 * s, k["dach_oben"] - 4.0 * s,
                               cx + 10.0 * s, k["dach_oben"] + 4.0 * s]})
        formen.append({"form": "rectangle", "farbe": WAND_DUNKEL, "rand": KONTUR,
                       "box": [cx + 17.0 * s, k["sockel_oben"] + 2.0 * s,
                               cx + 25.0 * s, k["sockel_oben"] + 8.0 * s]})
        formen.append({"form": "rectangle", "farbe": WAND_HELL, "rand": KONTUR,
                       "box": [cx - 25.0 * s, k["sockel_oben"] + 2.0 * s,
                               cx - 19.0 * s, k["sockel_oben"] + 7.0 * s]})
    elif familie == "lager":
        # seitlicher Anbau 10 x 14 px mit eigenem Dach
        formen.append({"form": "rectangle", "farbe": WAND_HELL, "rand": KONTUR,
                       "box": [cx + 15.0 * s, k["sockel_unten"] - ANBAU_HOEHE * s,
                               cx + 15.0 * s + ANBAU_BREITE * s, k["sockel_unten"]]})
        formen.append({"form": "polygon", "farbe": DACH_DUNKEL,
                       "punkte": [cx + 15.0 * s, k["sockel_unten"] - ANBAU_HOEHE * s,
                                  cx + 20.0 * s, k["sockel_unten"] - (ANBAU_HOEHE + 6.0) * s,
                                  cx + 25.0 * s, k["sockel_unten"] - ANBAU_HOEHE * s]})
        formen.append({"form": "rectangle", "farbe": KONTUR,
                       "box": [cx + 19.0 * s, k["sockel_unten"] - 6.0 * s,
                               cx + 21.0 * s, k["sockel_unten"]]})
    elif familie == "kaserne":
        # breite Front mit zwei Pfosten
        formen.append({"form": "rectangle", "farbe": WAND_HELL, "rand": KONTUR,
                       "box": [cx - 16.0 * s, k["wand_oben"], cx + 16.0 * s,
                               k["wand_oben"] + 4.0 * s]})
        for u in (-13.0, 10.0):
            formen.append({"form": "rectangle", "farbe": KONTUR,
                           "box": [cx + u * s, k["sockel_unten"] - 20.0 * s,
                                   cx + (u + 3.0) * s, k["sockel_unten"]]})
    elif familie == "ausbildungsstaette":
        # Mast mit Fahne und Stufen — unterscheidet sich klar von der Kaserne
        formen.append({"form": "line", "farbe": KONTUR, "breite": max(1.0, 1.0 * s),
                       "punkte": [cx + 14.0 * s, k["sockel_unten"],
                                  cx + 14.0 * s, k["dach_oben"] - 6.0 * s]})
        formen.append({"form": "polygon", "farbe": PIP_FARBE,
                       "punkte": [cx + 14.0 * s, k["dach_oben"] - 6.0 * s,
                                  cx + 22.0 * s, k["dach_oben"] - 3.0 * s,
                                  cx + 14.0 * s, k["dach_oben"]]})
        formen.append({"form": "rectangle", "farbe": WAND_DUNKEL, "rand": KONTUR,
                       "box": [cx - 14.0 * s, k["sockel_unten"],
                               cx + 14.0 * s, k["sockel_unten"] + 3.0 * s]})
    elif familie == "bibliothek":
        # drei Saeulen und ein Giebel statt Tür — der Tempel/Bibliotheksbau
        for u in (-12.0, 0.0, 12.0):
            formen.append({"form": "rectangle", "farbe": WAND_HELL, "rand": KONTUR,
                           "box": [cx + (u - 2.0) * s, k["wand_oben"] + 3.0 * s,
                                   cx + (u + 2.0) * s, k["sockel_oben"]]})
        formen.append({"form": "polygon", "farbe": DACH_HELL,
                       "punkte": [cx - 13.0 * s, k["wand_oben"], cx, k["dach_oben"],
                                  cx + 13.0 * s, k["wand_oben"]]})
        formen.append({"form": "line", "farbe": KONTUR, "breite": max(1.0, 1.0 * s),
                       "punkte": [cx - 13.0 * s, k["wand_oben"], cx + 13.0 * s, k["wand_oben"]]})
    return formen


def _wall_bau(x0: float, y0: float, zelle: float) -> list[dict]:
    """Verteidigungswall: Mauerblock mit vier Zinnen, Tor und Steinreihen (kein Dach)."""
    k = _bau_koordinaten(x0, y0, zelle)
    s, cx = k["s"], k["cx"]
    unten = k["sockel_unten"]
    oben = unten - 30.0 * s          # Mauer 30 px hoch (Astra-Koerperhoehe 22 + Sockelnaehe)
    formen: list[dict] = []
    versatz = 0.03 * zelle
    formen.append({"form": "rectangle", "farbe": BODENSCHATTEN,
                   "box": [cx - 18.0 * s + versatz, oben, cx + 18.0 * s + versatz, unten + versatz]})
    formen.append({"form": "rectangle", "farbe": WAND_DUNKEL, "rand": KONTUR,
                   "box": [cx - 18.0 * s, oben, cx + 18.0 * s, unten]})
    for i in range(4):
        u = -18.0 + i * 9.0
        formen.append({"form": "rectangle", "farbe": WAND_HELL, "rand": KONTUR,
                       "box": [cx + u * s, oben - 5.0 * s, cx + (u + 6.0) * s, oben]})
    for v in (7.0, 15.0, 23.0):
        formen.append({"form": "line", "farbe": KONTUR, "breite": max(1.0, 1.0 * s),
                       "punkte": [cx - 16.0 * s, unten - v * s, cx + 16.0 * s, unten - v * s]})
    formen.append({"form": "rectangle", "farbe": KONTUR,
                   "box": [cx - TUER_BREITE / 2.0 * s, unten - TUER_HOEHE * s,
                           cx + TUER_BREITE / 2.0 * s, unten]})
    return formen


def gebaeude_baukasten_plan(gebaeude_key: str, x0: float, y0: float, zelle: float,
                            stufe: int = 1, max_stufe: int | None = None) -> list[dict]:
    """Zeichenplan fuer ein Gebaeude als kleiner Baukoerper auf einer Zelle.

    ``gebaeude_key`` ist eine der Kennungen aus ``gelaende.alle_gebaeude()``. Eine unbekannte
    Kennung wirft einen ValueError, der die Kennung nennt und die bekannten Kennungen auflistet.

    Die Silhouettenfamilie wird NUR aus der Kennung gewaehlt und ist damit deterministisch.
    Sieben Familien unterscheiden sich sichtbar: Lager (seitlicher Anbau), Kaserne (breite Front
    mit zwei Pfosten), Produktionsgebaeude (kleines Arbeitsdetail), Ausbildungsstaette (Mast mit
    Fahne), Wall (Zinnenmauer), Haus (Kamin und Giebelluke) und Bibliothek (Saeulen und Giebel).

    ``stufe`` und ``max_stufe`` fuegen NUR die Stufenpips hinzu (siehe ``stufenpips_plan``),
    nichts sonst. Ist ``max_stufe`` None, kommen keine Pips vor.
    """
    key = str(gebaeude_key).strip().lower()
    bekannt = _G.alle_gebaeude()
    if key not in bekannt:
        raise ValueError(
            f"Unbekanntes Gebaeude: {gebaeude_key!r} — erwartet eine der {len(bekannt)} "
            f"Kennungen aus gelaende.alle_gebaeude(): {', '.join(sorted(bekannt))}")
    familie = _FAMILIE[key]
    if familie == "wall":
        formen = _wall_bau(x0, y0, zelle)
    else:
        formen = _basis_bau(x0, y0, zelle, mit_tuer=(familie != "bibliothek"))
        formen += _familie_detail(familie, x0, y0, zelle)
    if max_stufe is not None:
        formen += stufenpips_plan(x0, y0, zelle, stufe, max_stufe)
    return formen


# --------------------------------------------------------------------------
# Gelaende — groessere Strukturformen, Ufer nur an echten Grenzen.
# --------------------------------------------------------------------------

def _ebene(x0: float, y0: float, zelle: float) -> list[dict]:
    """Ebene (Grasland): drei bis fuenf 3-6 px lange Halmlinien."""
    s = zelle / 64.0
    halm = _abdunkeln(_flaeche_farbe("grasland"), 0.72)
    formen: list[dict] = []
    for i, (u, laenge) in enumerate(((0.22, HALM_LAENGE_MIN), (0.42, 5.0),
                                     (0.62, HALM_LAENGE_MAX), (0.80, 4.0))):
        formen.append({"form": "line", "farbe": halm, "breite": max(1.0, 1.0 * s),
                       "punkte": [x0 + u * zelle, y0 + 0.80 * zelle,
                                  x0 + u * zelle, y0 + 0.80 * zelle - laenge * s]})
    return formen


def _steppe(x0: float, y0: float, zelle: float) -> list[dict]:
    """Steppe: drei Grasreihen, zwei Bueschel und ein Stein (Farbe aus data/gelaende.json)."""
    s = zelle / 64.0
    basis = _flaeche_farbe("steppe")
    dunkel = _abdunkeln(basis, 0.75)
    stein = _aufhellen(basis, 0.22)
    formen: list[dict] = []
    for v in (0.34, 0.50, 0.66):
        formen.append({"form": "line", "farbe": dunkel, "breite": max(1.0, 2.0 * s),
                       "punkte": [x0 + 0.10 * zelle, y0 + v * zelle,
                                  x0 + 0.34 * zelle, y0 + (v - 0.04) * zelle,
                                  x0 + 0.58 * zelle, y0 + v * zelle,
                                  x0 + 0.92 * zelle, y0 + (v - 0.04) * zelle]})
    for u in (0.20, 0.74):
        formen.append({"form": "line", "farbe": dunkel, "breite": max(1.0, 1.0 * s),
                       "punkte": [x0 + u * zelle, y0 + 0.46 * zelle,
                                  x0 + (u - 0.03) * zelle, y0 + 0.30 * zelle]})
    formen.append({"form": "oval", "farbe": stein, "rand": dunkel,
                   "box": [x0 + 0.62 * zelle, y0 + 0.74 * zelle,
                           x0 + 0.80 * zelle, y0 + 0.88 * zelle]})
    return formen


def _wald(x0: float, y0: float, zelle: float) -> list[dict]:
    """Wald: drei versetzte Baumgruppen ~14 x 20 px mit zwei Kronenfarben."""
    s = zelle / 64.0
    hb = WALD_GRUPPE_BREITE / 2.0 / 64.0    # halbe Gruppenbreite als Zellanteil
    hh = WALD_GRUPPE_HOEHE / 64.0           # Gruppentiefe als Zellanteil
    formen: list[dict] = []
    # drei versetzte Gruppen: (Mitte u, Fuss v) — unterschiedlich hoch gestaffelt
    for u, fuss in ((0.26, 0.86), (0.50, 0.90), (0.74, 0.84)):
        spitze = fuss - hh
        formen.append({"form": "polygon", "farbe": WALD_KRONE_DUNKEL,
                       "punkte": [x0 + (u - hb) * zelle, y0 + fuss * zelle,
                                  x0 + u * zelle, y0 + spitze * zelle,
                                  x0 + (u + hb) * zelle, y0 + fuss * zelle]})
        formen.append({"form": "polygon", "farbe": WALD_KRONE_HELL,
                       "punkte": [x0 + (u - hb * 0.6) * zelle, y0 + (fuss - 0.06) * zelle,
                                  x0 + u * zelle, y0 + (spitze + 0.05) * zelle,
                                  x0 + (u - 0.01) * zelle, y0 + (fuss - 0.06) * zelle]})
        formen.append({"form": "rectangle", "farbe": _abdunkeln(WALD_KRONE_DUNKEL, 0.6),
                       "box": [x0 + (u - 0.02) * zelle, y0 + fuss * zelle,
                               x0 + (u + 0.02) * zelle, y0 + (fuss + 0.06) * zelle]})
    formen.append({"form": "oval", "farbe": _abdunkeln(WALD_FARBE, 0.7),
                   "box": [x0 + 0.04 * zelle, y0 + 0.84 * zelle,
                           x0 + 0.96 * zelle, y0 + 0.98 * zelle]})
    return formen


def _huegel(x0: float, y0: float, zelle: float) -> list[dict]:
    """Huegel: zwei Kuppen, ein Schattierungsband und zwei Halme (Farbe aus data/gelaende.json)."""
    s = zelle / 64.0
    basis = _flaeche_farbe("huegel")
    hinten = _abdunkeln(basis, 0.72)
    vorn = _aufhellen(basis, 0.12)
    band = _abdunkeln(basis, 0.55)
    formen: list[dict] = [
        {"form": "arc", "farbe": hinten, "winkel": 0, "weite": 180, "stil": "chord",
         "box": [x0 + 0.20 * zelle, y0 + 0.28 * zelle, x0 + 0.88 * zelle, y0 + 0.84 * zelle]},
        {"form": "arc", "farbe": vorn, "winkel": 0, "weite": 180, "stil": "chord",
         "box": [x0 + 0.06 * zelle, y0 + 0.42 * zelle, x0 + 0.66 * zelle, y0 + 0.86 * zelle]},
        {"form": "polygon", "farbe": band,
         "punkte": [x0 + 0.16 * zelle, y0 + 0.64 * zelle, x0 + 0.36 * zelle, y0 + 0.50 * zelle,
                    x0 + 0.56 * zelle, y0 + 0.64 * zelle]},
    ]
    for u in (0.72, 0.80):
        formen.append({"form": "line", "farbe": band, "breite": max(1.0, 1.0 * s),
                       "punkte": [x0 + u * zelle, y0 + 0.82 * zelle,
                                  x0 + u * zelle, y0 + 0.68 * zelle]})
    return formen


def _berg(x0: float, y0: float, zelle: float) -> list[dict]:
    """Gebirge: zwei 18-28 px breite Felsformen mit heller Lichtflaeche #969385."""
    s = zelle / 64.0
    dunkel = _abdunkeln(GEBIRGE_FARBE, 0.75)
    formen: list[dict] = []
    for u, breite in ((0.30, (FELS_BREITE_MIN + FELS_BREITE_MAX) / 2.0),
                      (0.70, 20.0)):
        b = breite * s
        basis_v, top_v = 0.82, 0.48
        formen.append({"form": "polygon", "farbe": dunkel, "rand": KONTUR,
                       "punkte": [x0 + u * zelle - b / 2.0, y0 + basis_v * zelle,
                                  x0 + u * zelle, y0 + top_v * zelle,
                                  x0 + u * zelle + b / 2.0, y0 + basis_v * zelle]})
        formen.append({"form": "polygon", "farbe": GEBIRGE_LICHT,
                       "punkte": [x0 + u * zelle - b / 4.0, y0 + basis_v * zelle,
                                  x0 + u * zelle, y0 + top_v * zelle,
                                  x0 + u * zelle, y0 + basis_v * zelle]})
    return formen


def _wasser(x0: float, y0: float, zelle: float) -> list[dict]:
    """Wasser (Nebelsee): zwei bis drei 12-22 px lange Linien in #6D9296."""
    s = zelle / 64.0
    formen: list[dict] = []
    for v, laenge in ((0.36, 14.0), (0.54, WASSER_LINIE_MAX), (0.70, WASSER_LINIE_MIN)):
        formen.append({"form": "line", "farbe": WASSER_LINIE, "breite": max(1.0, 2.0 * s),
                       "punkte": [x0 + 0.16 * zelle, y0 + v * zelle,
                                  x0 + 0.16 * zelle + laenge * s, y0 + v * zelle]})
    return formen


def _sumpf(x0: float, y0: float, zelle: float) -> list[dict]:
    """Sumpf: Wasserlinie, drei Schilfhalme mit Kolben (Farbe aus data/gelaende.json)."""
    s = zelle / 64.0
    basis = _flaeche_farbe("sumpf")
    wasser = _abdunkeln(basis, 0.6)
    schilf = _aufhellen(basis, 0.24)
    formen: list[dict] = [
        {"form": "line", "farbe": wasser, "breite": max(1.0, 2.0 * s),
         "punkte": [x0 + 0.06 * zelle, y0 + 0.62 * zelle, x0 + 0.94 * zelle, y0 + 0.62 * zelle]},
    ]
    for u, oben in ((0.18, 0.22), (0.30, 0.16), (0.42, 0.26)):
        formen.append({"form": "line", "farbe": schilf, "breite": max(1.0, 2.0 * s),
                       "punkte": [x0 + u * zelle, y0 + 0.70 * zelle, x0 + u * zelle,
                                  y0 + (oben - 0.02) * zelle]})
        formen.append({"form": "oval", "farbe": schilf,
                       "box": [x0 + (u - 0.035) * zelle, y0 + (oben - 0.02) * zelle,
                               x0 + (u + 0.035) * zelle, y0 + (oben + 0.08) * zelle]})
    return formen


_GELAENDE_DETAIL = {
    "grasland": _ebene,
    "steppe": _steppe,
    "wald": _wald,
    "huegel": _huegel,
    "berg": _berg,
    "nebelsee": _wasser,
    "sumpf": _sumpf,
}


def _uferband(richtung: str, x0: float, y0: float, zelle: float) -> dict:
    """Ein 3-5 px breites Polygonband #999071 entlang EINER Feldkante."""
    b = UFER_BREITE * (zelle / 64.0)
    if richtung == "norden":
        punkte = [x0, y0, x0 + zelle, y0, x0 + zelle, y0 + b, x0, y0 + b]
    elif richtung == "osten":
        punkte = [x0 + zelle - b, y0, x0 + zelle, y0, x0 + zelle, y0 + zelle,
                  x0 + zelle - b, y0 + zelle]
    elif richtung == "sueden":
        punkte = [x0, y0 + zelle - b, x0 + zelle, y0 + zelle - b, x0 + zelle, y0 + zelle,
                  x0, y0 + zelle]
    else:  # westen
        punkte = [x0, y0, x0 + b, y0, x0 + b, y0 + zelle, x0, y0 + zelle]
    return {"form": "polygon", "farbe": UFER_FARBE, "punkte": punkte}


def gelaende_plan_fein(art: str, x0: float, y0: float, zelle: float,
                       nachbarn: dict | None = None) -> list[dict]:
    """Zeichenplan fuer ein Gelaendefeld (feinere Fassung von ``karten_optik.emblem_plan``).

    ``art`` ist eine der sieben Kennungen aus ``gelaende.GELAENDEARTEN``; eine unbekannte
    Gelaendeart wirft einen ValueError mit klarer Begruendung.

    ``nachbarn`` ist optional ein dict wie {'norden': 'wasser', 'osten': 'wald'} (oder None).
    Es wird NUR fuer zwei Dinge benutzt: (1) das Uferband an echten Land-Wasser-Grenzen und
    (2) das Unterdruecken der Innenkante zum gleichartigen Nachbarfeld. Fuer dieselbe Gelaendeart
    ('wasser' gilt wie 'nebelsee') wird die gemeinsame Kante nicht doppelt gezeichnet.

    Das Feld wird zuerst flaechig gefuellt (die vier Astra-Farben fuer Ebene, Wald, Gebirge und
    Wasser; sonst die Farbe aus data/gelaende.json) und bekommt darueber die Strukturformen der
    Art plus ein Uferband #999071, wenn ein Nachbar Wasser ist.
    """
    if art not in _G.GELAENDEARTEN:
        raise ValueError(
            f"Unbekannte Geländeart: {art!r} — erwartet eine von {sorted(_G.GELAENDEARTEN)}")
    s = zelle / 64.0
    nb = dict(nachbarn) if nachbarn else {}
    fuell = _flaeche_farbe(art)
    kante = _abdunkeln(fuell, 0.55)
    formen: list[dict] = [
        {"form": "rectangle", "farbe": fuell, "box": [x0, y0, x0 + zelle, y0 + zelle]},
    ]
    for richtung, linie in _randlinien(x0, y0, zelle).items():
        if _normal(nb.get(richtung)) == _normal(art):
            continue
        formen.append({"form": "line", "farbe": kante, "breite": max(1.0, 1.0 * s),
                       "punkte": list(linie)})
    formen += _GELAENDE_DETAIL[art](x0, y0, zelle)
    if _normal(art) != "nebelsee":
        for richtung in RICHTUNGEN:
            if _normal(nb.get(richtung)) == "nebelsee":
                formen.append(_uferband(richtung, x0, y0, zelle))
    return formen


# --------------------------------------------------------------------------
# Wege zwischen Feldern — ein Segment je Richtung, exakt bis an die Feldkante.
# --------------------------------------------------------------------------

def _richtungs_ende(richtung: str, x0: float, y0: float, zelle: float):
    """Der Punkt auf der geteilten Feldkante fuer eine Richtung."""
    cx = x0 + zelle / 2.0
    cy = y0 + zelle / 2.0
    if richtung == "norden":
        return [cx, y0]
    if richtung == "osten":
        return [x0 + zelle, cy]
    if richtung == "sueden":
        return [cx, y0 + zelle]
    return [x0, cy]      # westen


def wegabschnitt_plan(richtungen: tuple, x0: float, y0: float, zelle: float) -> list[dict]:
    """Wegeplan EINES Feldes: je Richtung ein Wegabschnitt von der Feldmitte zur Feldkante.

    ``richtungen`` ist ein Tupel, das die Werte 'norden', 'osten', 'sueden' und 'westen'
    enthalten darf. Jede Richtung zeichnet GENAU einen Wegabschnitt von der Feldmitte bis zur
    geteilten Kante (Endpunkt exakt auf der Kante), damit zwei benachbarte Felder einen
    durchgehenden Weg bilden. Der Weg ist eine 8 px breite Linie #75674F mit einer 4 px breiten
    Innenlinie #A28E69. Ein leeres Tupel ergibt einen leeren Plan. Eine unbekannte Richtung wirft
    einen ValueError.

    Wasser und Gebaeude kennt dieser Plan NICHT: der Aufrufer darf Wege nicht durch Wasser oder
    Gebaeude fuehren (Vorgabe "Siedlung 3": "Keine Wege automatisch durch Wasser oder Gebäude").
    """
    s = zelle / 64.0
    cx = x0 + zelle / 2.0
    cy = y0 + zelle / 2.0
    formen: list[dict] = []
    for richtung in richtungen:
        if richtung not in RICHTUNGEN:
            raise ValueError(
                f"Unbekannte Richtung: {richtung!r} — erwartet eine von {RICHTUNGEN}")
        ende = _richtungs_ende(richtung, x0, y0, zelle)
        mitte = [cx, cy]
        formen.append({"form": "line", "farbe": WEG_FARBE, "breite": max(1.0, WEG_BREITE * s),
                       "punkte": [mitte[0], mitte[1], ende[0], ende[1]]})
        formen.append({"form": "line", "farbe": WEG_INNEN_FARBE,
                       "breite": max(1.0, WEG_INNEN_BREITE * s),
                       "punkte": [mitte[0], mitte[1], ende[0], ende[1]]})
    return formen


# --------------------------------------------------------------------------
# Auswahl — goldener Rahmen, drei Pixel eingerueckt, mit vier Eckwinkeln.
# --------------------------------------------------------------------------

def auswahl_plan_fein(x0: float, y0: float, zelle: float) -> list[dict]:
    """Der goldene Auswahlrahmen eines Feldes.

    Auswahlrechteck 3 px nach innen: dunkle Unterkontur #172128 mit 5 px Strichbreite, darueber
    #E4C77D mit 2 px. Vier 8 px lange Eckwinkel verstaerken die Markierung, ohne das Feld zu
    ueberdecken. Alle Formen liegen im Feld.
    """
    s = zelle / 64.0
    e = AUSWAHL_EINZUG * s
    x1, y1 = x0 + e, y0 + e
    x2, y2 = x0 + zelle - e, y0 + zelle - e
    gold = AUSWAHL_GOLD_BREITE * s
    formen: list[dict] = [
        {"form": "rectangle", "rand": AUSWAHL_UNTER_FARBE, "breite": AUSWAHL_UNTER_BREITE * s,
         "box": [x1, y1, x2, y2]},
        {"form": "rectangle", "rand": AUSWAHL_GOLD, "breite": gold, "box": [x1, y1, x2, y2]},
    ]
    l = AUSWAHL_ECKEN_LAENGE * s
    ecken = (
        [x1, y1 + l, x1, y1, x1 + l, y1],   # oben links
        [x2 - l, y1, x2, y1, x2, y1 + l],   # oben rechts
        [x2, y2 - l, x2, y2, x2 - l, y2],   # unten rechts
        [x1 + l, y2, x1, y2, x1, y2 - l],   # unten links
    )
    for punkte in ecken:
        formen.append({"form": "line", "farbe": AUSWAHL_GOLD, "breite": gold, "punkte": punkte})
    return formen


# --------------------------------------------------------------------------
# Stufenpips — Quadrate auf einem dunklen Streifen unter dem Gebaeude.
# --------------------------------------------------------------------------

def stufenpips_plan(x0: float, y0: float, zelle: float, stufe: int,
                    max_stufe: int | None) -> list[dict]:
    """Stufenanzeige: ein dunkler Streifen unter dem Gebaeude und je Stufe ein Quadrat.

    Es werden genau ``max_stufe`` Quadrate von 4 x 4 px mit 2 px Abstand gezeichnet; die
    erreichten (``stufe``) in Gold, die uebrigen gedaempft. Ist ``max_stufe`` None, ist der Plan
    LEER (kein Streifen, keine Pips). Ein Streifen plus ``max_stufe`` Quadrate bleiben im Feld.
    """
    if max_stufe is None:
        return []
    n = max(0, int(max_stufe))
    erreicht = max(0, int(stufe))
    s = zelle / 64.0
    cx = x0 + zelle / 2.0
    kante = PIP_KANTE * s
    abstand = PIP_ABSTAND * s
    breite = n * kante + max(0, n - 1) * abstand
    strip_y1 = y0 + 0.87 * zelle
    strip_y2 = y0 + 0.93 * zelle
    formen: list[dict] = [{
        "form": "rectangle", "farbe": KONTUR,
        "box": [max(x0, cx - breite / 2.0 - abstand), strip_y1,
                min(x0 + zelle, cx + breite / 2.0 + abstand), strip_y2],
    }]
    start = cx - breite / 2.0
    py1 = strip_y1 + (strip_y2 - strip_y1 - kante) / 2.0
    for j in range(n):
        px1 = start + j * (kante + abstand)
        formen.append({"form": "rectangle",
                       "farbe": PIP_FARBE if j < erreicht else PIP_LEER,
                       "box": [px1, py1, px1 + kante, py1 + kante]})
    return formen


# --------------------------------------------------------------------------
# Koordinatenleiste — 18 px breite bzw. hohe aeussere Rasterleiste.
# --------------------------------------------------------------------------

def koordinatenleiste_plan(spalten: int, zeilen: int, zelle: float,
                           rand: float = 18.0,
                           spaltennamen: list | None = None,
                           zeilennamen: list | None = None) -> list[dict]:
    """Die aeussere Rasterleiste mit Koordinaten (Spalten und Zeilen).

    Die Leiste ist ``rand`` px breit beziehungsweise hoch (Vorgabe 18 px aus "Siedlung 3") und
    legt sich als Winkel ueber und links neben das Raster. Jede Spalte und jede Zeile bekommt
    eine Beschriftung (Spalten oben, Zeilen links) in der Panel-Textfarbe #EEE2CA.

    Ohne ``spaltennamen``/``zeilennamen`` steht dort die Ziffer der Spalte bzw. Zeile. Sind die
    Listen angegeben, werden IHRE Eintraege benutzt — die Siedlungskarte schreibt damit die im
    Spiel ueblichen Buchstaben A-H (``main._spaltenname``), damit die Leiste und das Detailpanel
    dieselbe Koordinate nennen. Eine zu kurze Liste wirft einen ValueError (keine stille
    Mischung aus Buchstabe und Ziffer).
    """
    spalten = int(spalten)
    zeilen = int(zeilen)
    if spaltennamen is not None and len(list(spaltennamen)) < spalten:
        raise ValueError(
            f"spaltennamen hat {len(list(spaltennamen))} Eintraege, erwartet {spalten}")
    if zeilennamen is not None and len(list(zeilennamen)) < zeilen:
        raise ValueError(
            f"zeilennamen hat {len(list(zeilennamen))} Eintraege, erwartet {zeilen}")
    breit = spalten * zelle
    hoch = zeilen * zelle
    x0r, y0r = rand, rand          # das Raster beginnt hinter der Leiste
    font = ("TkDefaultFont", int(max(7.0, rand * 0.5)))
    formen: list[dict] = [
        {"form": "rectangle", "farbe": KONTUR, "box": [0.0, 0.0, rand, rand]},
        {"form": "rectangle", "farbe": KONTUR, "box": [x0r, 0.0, x0r + breit, rand]},
        {"form": "rectangle", "farbe": KONTUR, "box": [0.0, y0r, rand, y0r + hoch]},
        {"form": "line", "farbe": WAND_DUNKEL, "breite": max(1.0, zelle / 64.0),
         "punkte": [x0r, y0r, x0r + breit, y0r]},
        {"form": "line", "farbe": WAND_DUNKEL, "breite": max(1.0, zelle / 64.0),
         "punkte": [x0r, y0r, x0r, y0r + hoch]},
    ]
    for c in range(1, spalten + 1):
        beschriftung = str(list(spaltennamen)[c - 1]) if spaltennamen is not None else str(c)
        formen.append({"form": "text", "farbe": KOORDINATEN_TEXT, "font": font, "anker": "center",
                       "punkt": [x0r + (c - 0.5) * zelle, rand / 2.0], "text": beschriftung})
    for r in range(1, zeilen + 1):
        beschriftung = str(list(zeilennamen)[r - 1]) if zeilennamen is not None else str(r)
        formen.append({"form": "text", "farbe": KOORDINATEN_TEXT, "font": font, "anker": "center",
                       "punkt": [rand / 2.0, y0r + (r - 0.5) * zelle], "text": beschriftung})
    return formen


# --------------------------------------------------------------------------
# Farben und offene Luecken.
# --------------------------------------------------------------------------

def farben() -> dict:
    """Die im Modul benutzten Farben als Namen -> Hexwert (alle aus der Astra-Datei)."""
    return {
        "dach_hell": DACH_HELL, "dach_dunkel": DACH_DUNKEL,
        "wand_hell": WAND_HELL, "wand_dunkel": WAND_DUNKEL,
        "kontur": KONTUR, "bodenschatten": BODENSCHATTEN,
        "ebene": EBENE_FARBE, "wald": WALD_FARBE, "gebirge": GEBIRGE_FARBE, "wasser": WASSER_FARBE,
        "wald_krone_dunkel": WALD_KRONE_DUNKEL, "wald_krone_hell": WALD_KRONE_HELL,
        "gebirge_licht": GEBIRGE_LICHT, "wasser_linie": WASSER_LINIE, "ufer": UFER_FARBE,
        "weg": WEG_FARBE, "weg_innen": WEG_INNEN_FARBE,
        "auswahl_unter": AUSWAHL_UNTER_FARBE, "auswahl_gold": AUSWAHL_GOLD,
        "pip": PIP_FARBE, "koordinaten_text": KOORDINATEN_TEXT,
    }


def offene_luecken() -> list[str]:
    """Was dieses Modul bewusst NICHT belegen kann (ehrlich gemeldet)."""
    return [
        "Alle Masszahlen stammen aus der Bildmodell-Auswertung "
        "docs/audits/ux_astra_karten_feinheit_2026-10-05.txt (Vorschlaege, keine belegten "
        "Eigenschaften des Originals); das Handbuch 2009 nennt keine Kartenoptik.",
        "Das Bildmodell nennt die Gelaendeart 'Wasser'; im Projekt heisst sie 'nebelsee' — beide "
        "Schreibweisen werden als Wasser behandelt.",
        "Die Familie eines Gebaeudes wird aus der Kennung gewaehlt (Ableitung aus der Kategorie "
        "in data/buildings.json). Ein dort neu ergaenztes Gebaeude mit unbekannter Kennung wuerde "
        "einen ValueError ausloesen.",
        "Ufer und Innenkanten haengen an der Uebergabe von 'nachbarn'; ohne Nachbarangabe zeichnet "
        "das Feld alle vier Kanten und kein Ufer.",
        "Die Koordinatenleiste zeichnet von sich aus Ziffern; Buchstaben oder ein fester Ausschnitt "
        "sind in der Vorlage nicht genannt. Der Aufrufer kann mit 'spaltennamen'/'zeilennamen' die "
        "im Spiel ueblichen Buchstaben A-H uebergeben (main._spaltenname), damit Leiste und Panel "
        "dieselbe Koordinate nennen.",
        "Wege und Auswahl kennen weder Wasser noch Gebaeude: der Aufrufer muss Wege aus Wasser "
        "und Gebaeuden heraushalten (so in 'Siedlung 3' gefordert).",
    ]
