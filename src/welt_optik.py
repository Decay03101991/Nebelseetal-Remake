"""
Zeichenplaene fuer die WELTkarte des Nebelseetal-Remakes (Paket: feinere Weltkartenoptik).

Dieses Modul liefert NUR DATEN — eine Liste von Zeichenbefehlen ("Plan") je Element. Es zeichnet
selbst nichts (ausser ``zeichne``, das einen fertigen Plan auf eine beliebige Leinwand
uebertraegt) und braucht daher weder ein Fenster noch tkinter, Pillow oder Emoji. So lassen sich
die Plaene ohne Anzeige pruefen (tests/test_welt_optik.py).

Hintergrund: Die bisherige Weltkarte zeigte je Feld eine Gelaendefarbe plus WENIGE Striche
(``main._welt_gelaende_zeichen``). Dieses Modul gibt den SECHS Gelaendearten der Weltkarte
('forest', 'plains', 'mountain', 'water', 'village', 'ruins') ein reicheres Zeichen aus 4 bis 16
Formen und liefert dazu die Zeichenplaene fuer die Regionsbeschriftung, die kleine
Uebersichtskarte, die Fahne des eigenen Ortes, den Auswahlrahmen und das Ortszeichen.

Hinweis zur Herkunft der Namen/Farben: Die Regionsnamen sind read-only aus ``src/main.py``
(Konstante ``WELT_REGIONEN``) uebernommen, die Gelaendefarben aus ``main.WELT_GELAENDEFARBEN``.
Das Handbuch nennt weder Regionsnamen noch Zoomstufen (siehe ``offene_luecken``).

Plan-Eintrag (ein dict je Zeichenbefehl):
  'form'   : 'polygon' | 'rectangle' | 'oval' | 'line' | 'text' | 'arc'
  'punkte' : flache [x, y, x, y, ...]-Liste — fuer 'polygon' und 'line'
  'box'    : [x1, y1, x2, y2] — fuer 'rectangle', 'oval' und 'arc'
  'punkt'  : [x, y] — fuer 'text' (Textposition)
  'farbe'  : Fuellfarbe (hex, z. B. '#2F4A2E') — bei 'line' und 'text' die Linien-/Textfarbe
  'rand'   : Umrissfarbe (hex)
  'breite' : Linien-/Randbreite in px
  'text'   : Text fuer 'text'
  'font'   : Schrift als Tupel, z. B. ('TkDefaultFont', 10, 'bold') fuer 'text'
  'anker'  : Verankerung fuer 'text' (z. B. 'center', 'nw')
  'winkel' : Startwinkel fuer 'arc' (Grad, Tk: 0 = Osten, gegen den Uhrzeigersinn)
  'weite'  : Ausdehnung fuer 'arc' (Grad)
  'stil'   : Bogenstil fuer 'arc' ('pieslice' | 'chord' | 'arc')
  'glatt'  : True -> weiche Linie (smooth=True) fuer 'line'

``zeichne`` uebertraegt je Eintrag GENAU einen Zeichenbefehl (create_polygon/create_rectangle/
create_oval/create_line/create_text/create_arc) per Duck-Typing (kein tkinter-Import) und gibt
die Zahl der gezeichneten Objekte zurueck. Alle Plaene sind deterministisch (kein Zufall).

Alle Koordinaten der Gelaendezeichen liegen im Zellenkasten
[x0, x0+zelle] x [y0, y0+zelle] und sind aus ``zelle`` berechnet, damit sie bei 24, 32, 48, 64
und 96 px funktionieren. Farben sind gedaempfte Hex-Werte (Hintergrund der Karte: #0F1418).
"""
from __future__ import annotations

# Hintergrund der Karte (dunkle Oberflaeche, siehe main.py und karten_optik.py).
KARTEN_HINTERGRUND = "#0F1418"

# Die sechs erlaubten Zeichenformen.
FORMEN = ("polygon", "rectangle", "oval", "line", "text", "arc")

# Die sechs Gelaendearten der WELTkarte (Reihenfolge wie main.WELT_GELAENDEREIHENFOLGE,
# read-only uebernommen am 05.10.2026).
GELAENDEARTEN = ("forest", "plains", "mountain", "water", "village", "ruins")

# Gelaendefarben der Uebersichtskarte. Quelle: src/main.py, Konstante WELT_GELAENDEFARBEN
# (read-only kopiert am 05.10.2026). Unbekannte Gelaendearten bekommen KEINE Farbe —
# es wird nichts erfunden (siehe uebersicht_plan).
_GELAENDEFARBEN = {
    "forest": "#2F4A2E", "plains": "#6E7A3A", "mountain": "#5B5F63",
    "water": "#1F4E6E", "village": "#8A6A2A", "ruins": "#4A3B63",
}

# Regionsnamen der 3x3-Einteilung. Quelle: src/main.py, Konstante WELT_REGIONEN
# (read-only kopiert am 05.10.2026; Reihenfolge Nordwest..Suedost). Das Handbuch nennt KEINE
# Regionsnamen — die Namen sind ein Vorschlag (siehe offene_luecken).
_REGIONNAMEN = ("Nordwesten", "Norden", "Nordosten",
                "Westen", "Zentrum", "Osten",
                "Südwesten", "Süden", "Südosten")


# --------------------------------------------------------------------------
# Koordinatenhilfen
# --------------------------------------------------------------------------

def _punkte(x0: float, y0: float, zelle: float, *paare: float) -> list:
    """Flache [x, y, ...]-Liste aus relativen Zellenkoordinaten (0..1)."""
    werte: list = []
    for i in range(0, len(paare), 2):
        werte.append(x0 + paare[i] * zelle)
        werte.append(y0 + paare[i + 1] * zelle)
    return werte


def _box(x0: float, y0: float, zelle: float, u1: float, v1: float, u2: float, v2: float) -> list:
    """[x1, y1, x2, y2] aus relativen Zellenkoordinaten (0..1)."""
    return [x0 + u1 * zelle, y0 + v1 * zelle, x0 + u2 * zelle, y0 + v2 * zelle]


# --------------------------------------------------------------------------
# Gelaendezeichen der WELTkarte — reicher als die bisherigen wenigen Striche
# --------------------------------------------------------------------------

# Gedaempfte Welt-PALETTE (Hintergrund #0F1418).
_WALD_SCHATTEN = "#101A12"
_WALD_DUNKEL = "#1B2E1C"
_WALD_HELL = "#274424"
_WALD_STAMM = "#4A3A22"

_BERG_DUNKEL = "#3E4249"
_BERG_HELL = "#5B5F63"
_BERG_SCHNEE = "#E8EEF2"
_BERG_SCHNEE_DUNKEL = "#C8D2DA"
_BERG_GEROELL = "#2E3238"

_WELLE_HELL = "#9AB0C4"
_WELLE_MITTEL = "#7E97AA"
_WELLE_DUNKEL = "#6B8296"
_SCHILF = "#3E5A34"
_KOLBEN = "#6E5A3C"

_EBENE_REIHE = "#7E8A44"
_EBENE_STEIN = "#8C7A4A"
_EBENE_STEIN_RAND = "#5A4E30"

_DORF_WAND = "#B08968"
_DORF_DACH = "#8A6A2A"
_DORF_FIRST = "#6E5220"
_DORF_TUER = "#3A2A18"
_ZAUN = "#6E5A3C"

_RUINE_SAEULE = "#B9AEE0"
_RUINE_KAPPE = "#8A7FB0"
_RUINE_BLOCK = "#6E6388"

_RAND_DUNKEL = "#17212B"


def gelaende_plan(art: str, x0: float, y0: float, zelle: float) -> list[dict]:
    """Zeichenplan fuer ein Gelaendezeichen EINER Zelle der Weltkarte.

    ``art`` ist eine der sechs Kennungen aus ``GELAENDEARTEN``. Jede Art bekommt 4 bis 16
    Formen, alle aus ``zelle`` berechnet und innerhalb [x0, x0+zelle] x [y0, y0+zelle]. Eine
    unbekannte Gelaendeart wirft einen klaren ValueError.
    """
    if art not in _GELAENDE:
        raise ValueError(
            f"Unbekannte Gelaendeart der Weltkarte: {art!r} — erwartet eine von "
            f"{sorted(_GELAENDE)}")
    return _GELAENDE[art](x0, y0, zelle)


def _wald(x0: float, y0: float, zelle: float) -> list[dict]:
    """Wald: drei gestaffelte Nadelbaeume (zwei Kronenreihen je Baum, Stamm) auf Bodenschatten."""
    formen: list[dict] = [{
        "form": "oval",
        "box": _box(x0, y0, zelle, 0.06, 0.80, 0.94, 0.96),
        "farbe": _WALD_SCHATTEN,
    }]
    # (Mitte u, obere Reihenbasis v, Spitze v) — unterschiedlich hoch = gestaffelt.
    for u, ober_basis, spitze in ((0.22, 0.42, 0.18), (0.50, 0.38, 0.14), (0.78, 0.44, 0.20)):
        formen.append({
            "form": "rectangle",
            "box": _box(x0, y0, zelle, u - 0.030, 0.68, u + 0.030, 0.88),
            "farbe": _WALD_STAMM,
        })
        formen.append({
            "form": "polygon",
            "punkte": _punkte(x0, y0, zelle, u - 0.170, 0.68, u, 0.40, u + 0.170, 0.68),
            "farbe": _WALD_DUNKEL,
        })
        formen.append({
            "form": "polygon",
            "punkte": _punkte(x0, y0, zelle, u - 0.110, ober_basis, u, spitze,
                              u + 0.110, ober_basis),
            "farbe": _WALD_HELL,
        })
    return formen


def _gebirge(x0: float, y0: float, zelle: float) -> list[dict]:
    """Gebirge: zwei Gipfel mit Schneehauben und Geröll am Fuss."""
    formen = [
        {"form": "polygon",
         "punkte": _punkte(x0, y0, zelle, 0.36, 0.78, 0.56, 0.28, 0.76, 0.78),
         "farbe": _BERG_DUNKEL},
        {"form": "polygon",
         "punkte": _punkte(x0, y0, zelle, 0.50, 0.42, 0.56, 0.28, 0.62, 0.42),
         "farbe": _BERG_SCHNEE_DUNKEL},
        {"form": "polygon",
         "punkte": _punkte(x0, y0, zelle, 0.12, 0.86, 0.42, 0.34, 0.72, 0.86),
         "farbe": _BERG_HELL},
        {"form": "polygon",
         "punkte": _punkte(x0, y0, zelle, 0.34, 0.50, 0.42, 0.34, 0.50, 0.50),
         "farbe": _BERG_SCHNEE},
    ]
    for u, v in ((0.16, 0.80), (0.30, 0.88), (0.62, 0.82)):
        formen.append({
            "form": "oval",
            "box": _box(x0, y0, zelle, u - 0.030, v - 0.030, u + 0.030, v + 0.030),
            "farbe": _BERG_GEROELL,
        })
    return formen


def _wasser(x0: float, y0: float, zelle: float) -> list[dict]:
    """Wasser: drei weiche Wellenlinien und zwei Schilfhalme mit Kolben."""
    formen: list[dict] = []
    for v, farbe in ((0.34, _WELLE_HELL), (0.52, _WELLE_MITTEL), (0.70, _WELLE_DUNKEL)):
        formen.append({
            "form": "line",
            "punkte": _punkte(x0, y0, zelle, 0.12, v, 0.30, v - 0.05, 0.50, v,
                              0.70, v - 0.05, 0.88, v),
            "farbe": farbe, "breite": 2, "glatt": True,
        })
    for u, oben in ((0.16, 0.30), (0.24, 0.24)):
        formen.append({
            "form": "line",
            "punkte": _punkte(x0, y0, zelle, u, 0.84, u, oben),
            "farbe": _SCHILF, "breite": 2,
        })
        formen.append({
            "form": "oval",
            "box": _box(x0, y0, zelle, u - 0.030, oben, u + 0.030, oben + 0.10),
            "farbe": _KOLBEN,
        })
    return formen


def _ebene(x0: float, y0: float, zelle: float) -> list[dict]:
    """Ebene: drei Grasreihen, zwei kurze Halme und ein Stein."""
    formen: list[dict] = []
    for v in (0.36, 0.52, 0.68):
        formen.append({
            "form": "line",
            "punkte": _punkte(x0, y0, zelle, 0.10, v, 0.35, v - 0.03, 0.60, v,
                              0.90, v - 0.03),
            "farbe": _EBENE_REIHE, "breite": 2,
        })
    for u, spitze in ((0.20, 0.66), (0.82, 0.68)):
        formen.append({
            "form": "line",
            "punkte": _punkte(x0, y0, zelle, u, 0.80, u - 0.03, spitze),
            "farbe": _EBENE_REIHE, "breite": 1,
        })
    formen.append({
        "form": "oval",
        "box": _box(x0, y0, zelle, 0.56, 0.72, 0.76, 0.86),
        "farbe": _EBENE_STEIN, "rand": _EBENE_STEIN_RAND,
    })
    return formen


def _dorf(x0: float, y0: float, zelle: float) -> list[dict]:
    """Dorf: Haus mit Dachfirst, Tuer und einem Zaunpfosten-Paar samt Querbalken."""
    return [
        # Hauskoerper
        {"form": "rectangle",
         "box": _box(x0, y0, zelle, 0.32, 0.52, 0.68, 0.82),
         "farbe": _DORF_WAND, "rand": _RAND_DUNKEL},
        # Dach als Trapez ...
        {"form": "polygon",
         "punkte": _punkte(x0, y0, zelle, 0.24, 0.52, 0.38, 0.30, 0.62, 0.30, 0.76, 0.52),
         "farbe": _DORF_DACH, "rand": _RAND_DUNKEL},
        # ... mit Dachfirst (obere Kante)
        {"form": "line",
         "punkte": _punkte(x0, y0, zelle, 0.38, 0.30, 0.62, 0.30),
         "farbe": _DORF_FIRST, "breite": 2},
        # Tuer
        {"form": "rectangle",
         "box": _box(x0, y0, zelle, 0.45, 0.62, 0.55, 0.82),
         "farbe": _DORF_TUER},
        # Zaunpfosten-Paar mit Querbalken
        {"form": "line",
         "punkte": _punkte(x0, y0, zelle, 0.10, 0.60, 0.10, 0.84),
         "farbe": _ZAUN, "breite": 2},
        {"form": "line",
         "punkte": _punkte(x0, y0, zelle, 0.20, 0.60, 0.20, 0.84),
         "farbe": _ZAUN, "breite": 2},
        {"form": "line",
         "punkte": _punkte(x0, y0, zelle, 0.10, 0.70, 0.20, 0.70),
         "farbe": _ZAUN, "breite": 1},
    ]


def _ruine(x0: float, y0: float, zelle: float) -> list[dict]:
    """Ruine: drei unterschiedlich hohe, gebrochene Saeulen plus zwei herabgestuerzte Bloecke."""
    formen: list[dict] = []
    # (Mitte u, Oberkante v) — drei verschiedene Hoehen; Fuss jeweils bei 0.82.
    for u, oben in ((0.22, 0.40), (0.50, 0.30), (0.78, 0.52)):
        formen.append({
            "form": "rectangle",
            "box": _box(x0, y0, zelle, u - 0.055, oben, u + 0.055, 0.82),
            "farbe": _RUINE_SAEULE,
        })
        # gebrochene Kappe (leicht schraeg = abgeplatzt)
        formen.append({
            "form": "polygon",
            "punkte": _punkte(x0, y0, zelle, u - 0.055, oben, u + 0.010, oben - 0.05,
                              u + 0.055, oben + 0.02),
            "farbe": _RUINE_KAPPE,
        })
    formen.append({
        "form": "rectangle",
        "box": _box(x0, y0, zelle, 0.30, 0.84, 0.46, 0.92),
        "farbe": _RUINE_BLOCK,
    })
    formen.append({
        "form": "rectangle",
        "box": _box(x0, y0, zelle, 0.60, 0.84, 0.72, 0.90),
        "farbe": _RUINE_BLOCK,
    })
    return formen


_GELAENDE = {
    "forest": _wald,
    "plains": _ebene,
    "mountain": _gebirge,
    "water": _wasser,
    "village": _dorf,
    "ruins": _ruine,
}


# --------------------------------------------------------------------------
# Fahne des eigenen Ortes ("Hier"): weisse Fahne auf blauem Sockel
# --------------------------------------------------------------------------

def fahne_plan(x0: float, y0: float, zelle: float) -> list[dict]:
    """Zeichenplan fuer die Fahne des eigenen Ortes: weisse Fahne auf blauem Sockel."""
    cx, cy = x0 + zelle / 2.0, y0 + zelle / 2.0
    return [
        {"form": "rectangle",
         "box": [cx - 0.16 * zelle, cy + 0.06 * zelle, cx + 0.16 * zelle, cy + 0.26 * zelle],
         "farbe": "#2563EB", "rand": "#0B0F12"},
        {"form": "line",
         "punkte": [cx, cy + 0.06 * zelle, cx, cy - 0.30 * zelle],
         "farbe": "#F3F4F6", "breite": max(1.0, zelle * 0.045)},
        {"form": "polygon",
         "punkte": [cx, cy - 0.30 * zelle, cx + 0.30 * zelle, cy - 0.18 * zelle,
                    cx, cy - 0.06 * zelle],
         "farbe": "#F3F4F6"},
        {"form": "oval",
         "box": [cx - 0.10 * zelle, cy + 0.24 * zelle, cx + 0.10 * zelle, cy + 0.28 * zelle],
         "farbe": "#0B0F12"},
    ]


# --------------------------------------------------------------------------
# Auswahlrahmen (starker Cyan-Rand)
# --------------------------------------------------------------------------

def auswahl_plan(x0: float, y0: float, zelle: float, farbe: str = "#38BDF8") -> list[dict]:
    """Zeichenplan fuer den Auswahlrahmen eines Feldes (nur Umriss, Fuellung leer)."""
    abstand = max(1.0, zelle * 0.03)
    return [{
        "form": "rectangle",
        "box": [x0 + abstand, y0 + abstand, x0 + zelle - abstand, y0 + zelle - abstand],
        "rand": farbe,
        "breite": max(2.0, zelle * 0.06),
    }]


# --------------------------------------------------------------------------
# Regionsbeschriftung (3x3)
# --------------------------------------------------------------------------

def regionen_plan(gitter: int, zelle: float, anzahl: int = 3) -> list[dict]:
    """Je Region GENAU ein TEXT-Eintrag, in der Mitte des Blocks, in Leinwandkoordinaten.

    ``gitter`` ist die Kantenlaenge des Rasters in Feldern, ``zelle`` die Feldgroesse in px.
    Eine 3x3-Einteilung (``anzahl=3``) ergibt genau 9 Eintraege. Die Namen stammen aus der
    read-only Kopie von ``main.WELT_REGIONEN``.
    """
    gitter = int(gitter)
    anzahl = int(anzahl)
    if gitter <= 0:
        raise ValueError(f"gitter muss positiv sein, war {gitter!r}")
    if anzahl <= 0:
        raise ValueError(f"anzahl muss positiv sein, war {anzahl!r}")
    kanten = [int(gitter * i / anzahl) for i in range(anzahl + 1)]
    formen: list[dict] = []
    for z in range(anzahl):
        for s in range(anzahl):
            x0, x1 = kanten[s], kanten[s + 1]
            y0, y1 = kanten[z], kanten[z + 1]
            if x1 <= x0 or y1 <= y0:
                continue
            cx = (x0 + x1) / 2.0 * zelle
            cy = (y0 + y1) / 2.0 * zelle
            index = z * anzahl + s
            name = _REGIONNAMEN[index] if 0 <= index < len(_REGIONNAMEN) else f"Region {index + 1}"
            formen.append({
                "form": "text",
                "punkt": [cx, cy],
                "text": name,
                "farbe": "#8A94A0",
                "font": ("TkDefaultFont", 10, "bold"),
            })
    return formen


# --------------------------------------------------------------------------
# Kleine Uebersichtskarte (ganzes Raster in ein Quadrat der Kantenlaenge 'kante')
# --------------------------------------------------------------------------

def _feld(tile, name: str, standard=None):
    """Liest einen Wert aus einem dict- oder objektfoermigen Feldeintrag (Duck-Typing)."""
    if isinstance(tile, dict):
        return tile.get(name, standard)
    return getattr(tile, name, standard)


def uebersicht_plan(tiles: list[dict], kante: float, gitter: int, orte: list = (),
                    auswahl: tuple | None = None) -> list[dict]:
    """Die kleine Uebersichtskarte als Zeichenplan.

    Je Eintrag in ``tiles`` entsteht GENAU EIN Rechteck. Die Fuellfarbe kommt aus dem Eintrag
    ('farbe') oder — falls nur 'terrain' gesetzt ist — aus der read-only Kopie der
    Gelaendefarben (Quelle ``main.WELT_GELAENDEFARBEN``). Eine unbekannte Gelaendeart bekommt
    KEINE Fuellung (es wird keine Farbe erfunden). Fehlen 'x'/'y', wird die Lage aus der
    Reihenfolge abgeleitet (Reihe fuer Reihe).

    Zu jedem Tupel in ``orte`` kommt ein kleiner Punkt (Oval), fuer ``auswahl`` (x, y) ein
    einzelner Cyan-Rahmen (Linienzug). Rueckgabe: Rechtecke + Punkte + (hoechstens) ein Rahmen.
    """
    gitter = int(gitter)
    if gitter <= 0:
        raise ValueError(f"gitter muss positiv sein, war {gitter!r}")
    kante = float(kante)
    kachel = kante / gitter
    formen: list[dict] = []
    for i, tile in enumerate(tiles):
        try:
            x = int(_feld(tile, "x"))
            y = int(_feld(tile, "y"))
        except (TypeError, ValueError):
            x = i % gitter
            y = i // gitter
        farbe = _feld(tile, "farbe")
        if farbe is None:
            farbe = _GELAENDEFARBEN.get(_feld(tile, "terrain"))
        eintrag = {
            "form": "rectangle",
            "box": [x * kachel, y * kachel, (x + 1) * kachel, (y + 1) * kachel],
        }
        if farbe is not None:
            eintrag["farbe"] = farbe
        else:
            eintrag["rand"] = "#0B0F12"
        formen.append(eintrag)
    radius = max(1.5, min(3.0, kachel * 0.5))
    for ort in orte:
        try:
            ox, oy = float(ort[0]), float(ort[1])
        except (TypeError, ValueError, IndexError):
            continue
        cx, cy = (ox + 0.5) * kachel, (oy + 0.5) * kachel
        formen.append({
            "form": "oval",
            "box": [cx - radius, cy - radius, cx + radius, cy + radius],
            "farbe": "#F2C94C",
        })
    if auswahl is not None:
        ax, ay = int(auswahl[0]), int(auswahl[1])
        rand = max(1.0, kachel * 0.15)
        x1, y1 = ax * kachel + rand, ay * kachel + rand
        x2, y2 = (ax + 1) * kachel - rand, (ay + 1) * kachel - rand
        formen.append({
            "form": "line",
            "punkte": [x1, y1, x2, y1, x2, y2, x1, y2, x1, y1],
            "farbe": "#38BDF8",
            "breite": max(1.0, kante * 0.02),
        })
    return formen


# --------------------------------------------------------------------------
# Ortszeichen fuer einen echten Ort (Kreis + winziger Gelaendehinweis)
# --------------------------------------------------------------------------

def ortszeichen_plan(x0: float, y0: float, zelle: float,
                     gelaende: str = "plains") -> list[dict]:
    """Kleines Ortszeichen: goldener Kreis plus winziger Gelaendehinweis (kein Emoji).

    Der Hinweis ist ein kurzes Zeichen (Dreieck, Strich, Saeule ...) passend zum Gelaende; ein
    unbekannter Gelaendeschluessel faellt auf einen Punkt zurueck (kein Fehler).
    """
    cx, cy = x0 + zelle / 2.0, y0 + zelle / 2.0
    formen: list[dict] = [{
        "form": "oval",
        "box": [cx - 0.22 * zelle, cy - 0.22 * zelle, cx + 0.22 * zelle, cy + 0.22 * zelle],
        "farbe": "#F2C94C", "rand": _RAND_DUNKEL,
    }]
    farbe = _RAND_DUNKEL
    if gelaende in ("forest", "plains", "village", "mountain"):
        # kleines Dreieck (Baum/Dach/Berg) in der Kreismitte
        formen.append({
            "form": "polygon",
            "punkte": [cx, cy - 0.11 * zelle, cx - 0.10 * zelle, cy + 0.09 * zelle,
                       cx + 0.10 * zelle, cy + 0.09 * zelle],
            "farbe": farbe,
        })
    elif gelaende == "water":
        formen.append({
            "form": "line",
            "punkte": [cx - 0.11 * zelle, cy, cx - 0.04 * zelle, cy - 0.05 * zelle,
                       cx + 0.04 * zelle, cy, cx + 0.11 * zelle, cy - 0.05 * zelle],
            "farbe": farbe, "breite": 2, "glatt": True,
        })
    elif gelaende == "ruins":
        formen.append({
            "form": "rectangle",
            "box": [cx - 0.05 * zelle, cy - 0.08 * zelle, cx + 0.05 * zelle, cy + 0.10 * zelle],
            "farbe": farbe,
        })
    else:
        formen.append({
            "form": "oval",
            "box": [cx - 0.05 * zelle, cy - 0.05 * zelle, cx + 0.05 * zelle, cy + 0.05 * zelle],
            "farbe": farbe,
        })
    return formen


# --------------------------------------------------------------------------
# Zeichnen (Duck-Typing, ohne tkinter-Import)
# --------------------------------------------------------------------------

def zeichne(canvas, plan: list[dict], tags: tuple = ()) -> int:
    """Uebertraegt jeden Plan-Eintrag als GENAU ein Objekt auf ``canvas``.

    ``canvas`` ist eine beliebige Leinwand mit den tkinter-Methoden create_polygon,
    create_rectangle, create_oval, create_line, create_text und create_arc (Duck-Typing — es
    wird kein tkinter importiert). ``tags`` wird an jeden create_*-Aufruf weitergegeben.
    Rueckgabe: Zahl der gezeichneten Objekte.
    """
    anzahl = 0
    for eintrag in plan:
        form = eintrag.get("form")
        if form not in FORMEN:
            raise ValueError(f"Unbekannte Zeichenform: {form!r} — erwartet eine von {FORMEN}")
        if form == "polygon":
            canvas.create_polygon(*eintrag["punkte"], tags=tags, **_fuell(eintrag))
        elif form == "line":
            kw = _fuell(eintrag)
            if eintrag.get("glatt"):
                kw["smooth"] = True
            canvas.create_line(*eintrag["punkte"], tags=tags, **kw)
        elif form == "rectangle":
            canvas.create_rectangle(*eintrag["box"], tags=tags, **_fuell(eintrag))
        elif form == "oval":
            canvas.create_oval(*eintrag["box"], tags=tags, **_fuell(eintrag))
        elif form == "arc":
            kw = _fuell(eintrag)
            if "winkel" in eintrag:
                kw["start"] = eintrag["winkel"]
            if "weite" in eintrag:
                kw["extent"] = eintrag["weite"]
            if "stil" in eintrag:
                kw["style"] = eintrag["stil"]
            canvas.create_arc(*eintrag["box"], tags=tags, **kw)
        elif form == "text":
            kw = {}
            if "farbe" in eintrag:
                kw["fill"] = eintrag["farbe"]
            if "text" in eintrag:
                kw["text"] = eintrag["text"]
            if "font" in eintrag:
                kw["font"] = eintrag["font"]
            if "anker" in eintrag:
                kw["anchor"] = eintrag["anker"]
            punkt = eintrag.get("punkt") or [0, 0]
            canvas.create_text(punkt[0], punkt[1], tags=tags, **kw)
        anzahl += 1
    return anzahl


def _fuell(eintrag: dict) -> dict:
    """Baut die gemeinsamen tkinter-Optionen aus einem Plan-Eintrag."""
    kw: dict = {}
    if "farbe" in eintrag:
        kw["fill"] = eintrag["farbe"]
    if "rand" in eintrag:
        kw["outline"] = eintrag["rand"]
    if "breite" in eintrag:
        kw["width"] = eintrag["breite"]
    return kw


# --------------------------------------------------------------------------
# Offene Luecken
# --------------------------------------------------------------------------

def offene_luecken() -> list[str]:
    """Was dieses Modul bewusst NICHT aus den Quellen belegen kann (ehrlich gemeldet)."""
    return [
        "Das Handbuch 2009 nennt KEINE Regionsnamen. Die neun Namen in regionen_plan stammen "
        "aus der read-only Kopie von main.WELT_REGIONEN und sind ein Vorschlag.",
        "Das Handbuch nennt KEINE Zoomstufen und keine Kachelgroessen. Die Stufen "
        "(16, 24, 32, 48, 64, 96) und der Standard 48 stammen aus main.WELT_ZOOM_STUFEN/"
        "WELT_ZOOM_STANDARD und sind ein Vorschlag.",
        "Die sechs Gelaendezeichen der Weltkarte sind Vorschlaege: belegt sind nur die "
        "Gelaendearten selbst (main.WELT_GELAENDEREIHENFOLGE), nicht ihre Zeichenform.",
        "Die Gelaendefarben der Uebersichtskarte sind angenaehert, nicht gemessen (read-only "
        "aus main.WELT_GELAENDEFARBEN).",
        "orte und auswahl der Uebersichtskarte spiegeln nur, was der Aufrufer uebergibt; dieses "
        "Modul kennt weder Siedlungen noch die aktuelle Ansicht.",
    ]
