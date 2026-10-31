# Code-Audit Nebelseetal Remake — Paket P4: Vier Zeichenmodule der Karten (2.960 Zeilen Optik)

## Deine Rolle

Du bist Software-Architekt und prüfst einen gewachsenen Python-Code (tkinter-Spiel, deutsch
kommentiert, 18.400 Zeilen Prüfcode). Der Code ist über Monate **angebaut** worden: neue Funktionen
kamen dazu, alte blieben, Doppelungen wurden nie zusammengeführt. Deine Aufgabe ist **nicht**,
Eleganz zu predigen, sondern konkrete, umsetzbare Zusammenführungen zu benennen.

## Harte Regeln (daran wird deine Antwort gemessen)

1. **Das Spiel bleibt unser Spiel.** Kein Verhalten darf sich ändern: keine anderen Zahlen, keine
   anderen Regeln, keine andere Bedienung. Reine Struktur- und Lesbarkeitsarbeit.
2. **Jede Funktion bleibt erhalten**, solange sie aufgerufen wird. Was niemand aufruft, nennst du
   ausdrücklich als „entfernbar" mit Begründung.
3. **Der Prüfcode ist der Beweis.** Zu jedem Vorschlag gehört: welche vorhandene Prüfdatei
   (tests/*.py) muss danach grün bleiben? Wenn keine existiert, sagst du das offen.
4. **Deutsch, ASCII in Code-Kommentaren** (das Projekt hält `src/botkern.py` bewusst ASCII).
5. **Keine erfundenen Zeilenzahlen.** Wenn du eine Ersparnis schätzt, schreib „geschätzt".

## Was das Projekt über sich sagt (gemessen, nicht geschätzt)

* `src/`: 49 Dateien, 21.703 Zeilen, 17.406 Codezeilen, 904 Funktionen/Methoden.
* `main.py` allein: 7.375 Zeilen, 240 Methoden, davon 27 `_render_*`-Methoden.
* Funktionen ab 60 Zeilen: 47 (längste 205 Zeilen, `_render_settlement_map`).
* 58 Sechs-Zeilen-Blöcke stehen mehrfach identisch im Code.
* `kampf.py` (398 Z.) und `kampf_alt_handbuch_2009.py` (401 Z.) enthalten je eine
  `fuehre_schlacht` (188 bzw. 194 Zeilen) — `kampf.py` importiert die alte Fassung.
* Oberfläche: tkinter, alles in einer Klasse; Ansichten `_render_*`, Aufbau `_build_main_ui`.
* Prüfcode: `tests/` 18.418 Zeilen, 98 Dateien, Aufruf über `tools/sammellauf.py`.

## Deine Aufgabe

`welt_optik.py`, `welt_optik_fein.py`, `karten_optik.py` und `karten_optik_fein.py` zeichnen Welten und Siedlungen in unterschiedlicher Feinheit. Prüfe: wie viel davon ist gemeinsames Gerüst (Flächen, Pfade, Symbole, Farben), wie viel ist wirklich verschieden? Vorschlag: welche gemeinsamen Bausteine, welche Dateien bleiben, welche fallen weg — ohne dass ein Pixel anders aussieht.

## Der Code

### Datei `src/welt_optik.py` (600 Zeilen)

```python
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

```

### Datei `src/welt_optik_fein.py` (898 Zeilen)

```python
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

```

### Datei `src/karten_optik.py` (599 Zeilen)

```python
"""
Zeichenplaene fuer die Siedlungskarte des Nebelseetal-Remakes (Paket: feinere Kartenoptik).

Dieses Modul liefert NUR DATEN — eine Liste von Zeichenbefehlen ("Plan") je Feld. Es zeichnet
selbst nichts (ausser ``zeichne``, das einen fertigen Plan auf eine beliebige Leinwand
uebertraegt) und braucht daher weder ein Fenster noch tkinter, Pillow oder Emoji. So lassen
sich die Plaene ohne Anzeige pruefen (tests/test_karten_optik.py).

Hintergrund: Bisher zeigte jede 64-px-Zelle eine Gelaendefarbe plus EIN duennes Emblem und je
Gebaeude ein einzelnes Hauszeichen. Dieses Modul gibt den sieben Gelaendearten aus
``gelaende.GELAENDEARTEN`` (grasland, steppe, wald, huegel, berg, nebelsee, sumpf) ein
reicheres Emblem und den 20 Originalgebaeuden aus ``data/buildings.json`` ein Zeichen, das
sich nach Gebaeudefamilie unterscheidet und die Ausbaustufe als Pips zeigt.

Plan-Eintrag (ein dict je Zeichenbefehl):
  'form'   : 'polygon' | 'rectangle' | 'oval' | 'line' | 'text' | 'arc'
  'punkte' : flache [x, y, x, y, ...]-Liste — fuer 'polygon' und 'line'
  'box'    : [x1, y1, x2, y2] — fuer 'rectangle', 'oval' und 'arc'
  'punkt'  : [x, y] — fuer 'text'
  'farbe'  : Fuellfarbe (hex, z. B. '#1B2A1E') — bei 'line' ist das die Linienfarbe
  'rand'   : Umrissfarbe (hex)
  'breite' : Linien-/Randbreite in px (Zahl)
  'text'   : Text fuer 'text'
  'font'   : Schrift als Tupel wie ('TkDefaultFont', 9, 'bold') fuer 'text'
  'anker'  : Verankerung fuer 'text' (z. B. 'nw', 'center')
  'winkel' : Startwinkel fuer 'arc' (Grad, Tk: 0 = Osten, gegen den Uhrzeigersinn)
  'weite'  : Ausdehnung fuer 'arc' (Grad)
  'stil'   : Bogenstil fuer 'arc' ('pieslice' | 'chord' | 'arc')

``zeichne`` uebertraegt je Eintrag GENAU einen Zeichenbefehl (create_polygon/create_rectangle/
create_oval/create_line/create_text/create_arc) per Duck-Typing (kein tkinter-Import) und gibt
die Zahl der gezeichneten Objekte zurueck. Alle Plaene sind deterministisch (kein Zufall).

Alle Koordinaten der Embleme und Gebaeude liegen im Zellenkasten
[x0, x0+zelle] x [y0, y0+zelle] und sind aus ``zelle`` berechnet, damit sie bei 32, 48, 64 und
96 px funktionieren.
"""
from __future__ import annotations

# Hintergrund der Karte (dunkle Oberflaeche, siehe data/gelaende.json "_farbwelt_original").
KARTEN_HINTERGRUND = "#0F1418"

# Die sechs erlaubten Zeichenformen.
FORMEN = ("polygon", "rectangle", "oval", "line", "text", "arc")


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
# Gelaende-Embleme — reicher als die bisherigen wenigen Striche
# --------------------------------------------------------------------------

# Ruhige, gedaempfte Farbwelt (passend zu data/gelaende.json, Hintergrund #0F1418).
_WALD_SCHATTEN = "#141E16"
_WALD_KRONE = "#1B2A1E"
_WALD_KRONE_HELL = "#243B26"
_STAMM = "#4A3A22"

_BERG_DUNKEL = "#3E3E46"
_BERG_HELL = "#565660"
_BERG_SCHNEE = "#E8EEF2"
_BERG_SCHNEE_DUNKEL = "#C8D2DA"
_BERG_GEROELL = "#2E2E34"

_HUEGEL_HINTEN = "#4A3E2A"
_HUEGEL_VORN = "#6E5A3C"
_HUEGEL_BAND = "#57462E"
_HALM_DUNKEL = "#3E3320"

_WASSER_HELL = "#9AB0C4"
_WASSER_MITTEL = "#7E97AA"
_WASSER_DUNKEL = "#6B8296"
_SCHILF = "#3E5A34"
_KOLBEN = "#6E5A3C"

_STEPPE_REIHE = "#6E5F38"
_STEPPE_STEIN = "#8C7A4A"
_STEPPE_STEIN_RAND = "#5A4E30"

_GRAS_HALM = "#48602F"
_GRAS_BLUME = "#E8C15A"


def emblem_plan(art: str, x0: float, y0: float, zelle: float) -> list[dict]:
    """Zeichenplan fuer ein Gelaende-Emblem einer Zelle.

    ``art`` ist eine der sieben Kennungen aus ``gelaende.GELAENDEARTEN``. Jede Art bekommt
    4 bis 16 Formen, alle innerhalb [x0, x0+zelle] x [y0, y0+zelle]. Eine unbekannte
    Gelaendeart wirft einen klaren ValueError.
    """
    if art not in _EMBLEME:
        raise ValueError(
            f"Unbekannte Gelaendeart: {art!r} — erwartet eine von "
            f"{sorted(_EMBLEME)}")
    return _EMBLEME[art](x0, y0, zelle)


def _wald(x0: float, y0: float, zelle: float) -> list[dict]:
    """Wald: drei gestaffelte Baeume (dunkle Krone + Stamm) auf einem Bodenschatten."""
    formen = [{
        "form": "oval",
        "box": _box(x0, y0, zelle, 0.06, 0.78, 0.94, 0.96),
        "farbe": _WALD_SCHATTEN,
    }]
    # drei Baeume: (Mitte u, Kronenspitze v, Kronenfuss v, Stammfuss v)
    for u, spitze, kronfuss, stammfuss in (
            (0.22, 0.30, 0.72, 0.86),
            (0.50, 0.24, 0.68, 0.82),
            (0.78, 0.32, 0.74, 0.88)):
        formen.append({
            "form": "rectangle",
            "box": _box(x0, y0, zelle, u - 0.035, kronfuss - 0.02, u + 0.035, stammfuss),
            "farbe": _STAMM,
        })
        formen.append({
            "form": "polygon",
            "punkte": _punkte(x0, y0, zelle, u - 0.17, kronfuss, u, spitze, u + 0.17, kronfuss),
            "farbe": _WALD_KRONE,
        })
        formen.append({
            "form": "polygon",
            "punkte": _punkte(x0, y0, zelle, u - 0.08, kronfuss - 0.06, u, spitze + 0.08,
                              u + 0.08, kronfuss - 0.06),
            "farbe": _WALD_KRONE_HELL,
        })
    return formen


def _berg(x0: float, y0: float, zelle: float) -> list[dict]:
    """Berg: zwei Gipfel mit Schneehauben und Geröll am Fuss."""
    formen = [
        {"form": "polygon",
         "punkte": _punkte(x0, y0, zelle, 0.32, 0.80, 0.54, 0.24, 0.80, 0.80),
         "farbe": _BERG_DUNKEL},
        {"form": "polygon",
         "punkte": _punkte(x0, y0, zelle, 0.47, 0.43, 0.54, 0.24, 0.61, 0.43),
         "farbe": _BERG_SCHNEE_DUNKEL},
        {"form": "polygon",
         "punkte": _punkte(x0, y0, zelle, 0.12, 0.88, 0.42, 0.32, 0.72, 0.88),
         "farbe": _BERG_HELL},
        {"form": "polygon",
         "punkte": _punkte(x0, y0, zelle, 0.34, 0.48, 0.42, 0.32, 0.50, 0.48),
         "farbe": _BERG_SCHNEE},
    ]
    for u, v in ((0.20, 0.84), (0.30, 0.90), (0.60, 0.86), (0.68, 0.80)):
        formen.append({
            "form": "oval",
            "box": _box(x0, y0, zelle, u - 0.025, v - 0.025, u + 0.025, v + 0.025),
            "farbe": _BERG_GEROELL,
        })
    return formen


def _huegel(x0: float, y0: float, zelle: float) -> list[dict]:
    """Huegel: zwei sich ueberlappende Kuppen mit Schattierungsband und Gras."""
    formen = [
        {"form": "arc",
         "box": _box(x0, y0, zelle, 0.20, 0.28, 0.88, 0.84),
         "winkel": 0, "weite": 180, "stil": "chord", "farbe": _HUEGEL_HINTEN},
        {"form": "arc",
         "box": _box(x0, y0, zelle, 0.06, 0.42, 0.66, 0.86),
         "winkel": 0, "weite": 180, "stil": "chord", "farbe": _HUEGEL_VORN},
        # Schattierungsband am Fuss der vorderen Kuppe (Chord-Fuss liegt bei v = 0.64).
        {"form": "polygon",
         "punkte": _punkte(x0, y0, zelle, 0.16, 0.64, 0.36, 0.50, 0.56, 0.64),
         "farbe": _HUEGEL_BAND},
    ]
    for u in (0.72, 0.80):
        formen.append({
            "form": "line",
            "punkte": _punkte(x0, y0, zelle, u, 0.82, u, 0.68),
            "farbe": _HALM_DUNKEL, "breite": 1,
        })
    return formen


def _nebelsee(x0: float, y0: float, zelle: float) -> list[dict]:
    """Nebelsee: drei Wellenlinien und Schilf am Rand."""
    formen = []
    for v, farbe in ((0.34, _WASSER_HELL), (0.52, _WASSER_MITTEL), (0.70, _WASSER_DUNKEL)):
        formen.append({
            "form": "line",
            "punkte": _punkte(x0, y0, zelle, 0.12, v, 0.30, v - 0.05, 0.50, v,
                              0.70, v - 0.05, 0.88, v),
            "farbe": farbe, "breite": 2,
        })
    for u, oben in ((0.10, 0.20), (0.16, 0.26), (0.22, 0.22)):
        formen.append({
            "form": "line",
            "punkte": _punkte(x0, y0, zelle, u, 0.82, u, oben),
            "farbe": _SCHILF, "breite": 2,
        })
    formen.append({
        "form": "oval",
        "box": _box(x0, y0, zelle, 0.19, 0.20, 0.25, 0.28),
        "farbe": _KOLBEN,
    })
    return formen


def _sumpf(x0: float, y0: float, zelle: float) -> list[dict]:
    """Sumpf: Wasserlinie, Schilf mit Kolben und zwei Blasen."""
    formen = [{
        "form": "line",
        "punkte": _punkte(x0, y0, zelle, 0.06, 0.62, 0.94, 0.62),
        "farbe": _WASSER_DUNKEL, "breite": 2,
    }]
    for u, oben in ((0.18, 0.22), (0.30, 0.16), (0.42, 0.26)):
        formen.append({
            "form": "line",
            "punkte": _punkte(x0, y0, zelle, u, 0.70, u, oben),
            "farbe": _SCHILF, "breite": 2,
        })
        formen.append({
            "form": "oval",
            "box": _box(x0, y0, zelle, u - 0.035, oben, u + 0.035, oben + 0.10),
            "farbe": _KOLBEN,
        })
    for u1, v1, u2, v2 in ((0.60, 0.44, 0.68, 0.52), (0.78, 0.30, 0.84, 0.36)):
        formen.append({
            "form": "oval",
            "box": _box(x0, y0, zelle, u1, v1, u2, v2),
            "rand": _WASSER_HELL, "breite": 1,
        })
    return formen


def _steppe(x0: float, y0: float, zelle: float) -> list[dict]:
    """Steppe: drei Grasreihen, zwei Bueschel und ein Stein."""
    formen = []
    for v in (0.34, 0.50, 0.66):
        formen.append({
            "form": "line",
            "punkte": _punkte(x0, y0, zelle, 0.10, v, 0.34, v - 0.04, 0.58, v,
                              0.82, v - 0.04, 0.92, v),
            "farbe": _STEPPE_REIHE, "breite": 2,
        })
    for u in (0.18, 0.74):
        formen.append({
            "form": "line",
            "punkte": _punkte(x0, y0, zelle, u, 0.44, u - 0.03, 0.30),
            "farbe": _STEPPE_REIHE, "breite": 1,
        })
    formen.append({
        "form": "oval",
        "box": _box(x0, y0, zelle, 0.62, 0.74, 0.80, 0.88),
        "farbe": _STEPPE_STEIN, "rand": _STEPPE_STEIN_RAND,
    })
    return formen


def _grasland(x0: float, y0: float, zelle: float) -> list[dict]:
    """Grasland: vier Grashalme und ein Bluetenpunkt auf einer Wiesenlinie."""
    formen = []
    for u, spitze in ((0.24, 0.30), (0.42, 0.24), (0.60, 0.34), (0.78, 0.28)):
        formen.append({
            "form": "line",
            "punkte": _punkte(x0, y0, zelle, u, 0.78, u - 0.04, spitze),
            "farbe": _GRAS_HALM, "breite": 2,
        })
    formen.append({
        "form": "line",
        "punkte": _punkte(x0, y0, zelle, 0.10, 0.80, 0.90, 0.80),
        "farbe": _GRAS_HALM, "breite": 1,
    })
    formen.append({
        "form": "oval",
        "box": _box(x0, y0, zelle, 0.66, 0.40, 0.74, 0.48),
        "farbe": _GRAS_BLUME,
    })
    return formen


_EMBLEME = {
    "wald": _wald,
    "berg": _berg,
    "huegel": _huegel,
    "nebelsee": _nebelsee,
    "sumpf": _sumpf,
    "steppe": _steppe,
    "grasland": _grasland,
}


# --------------------------------------------------------------------------
# Gebaeudezeichen
# --------------------------------------------------------------------------

# Zuordnung der 20 Gebaeude aus data/buildings.json zu ihren Familien. Vorbild ist die
# Spalte 'kategorie' in buildings.json: 10 Produktion, 3 Werkstatt, 3 Ausbildung, 1
# Verteidigung, 3 Sonstiges (Bibliothek, Haus, Lager).
_FAMILIE = {
    "holzfaeller": "produktion", "steinmetz": "produktion", "erzmine": "produktion",
    "tempel": "produktion", "farm": "produktion", "goldmine": "produktion",
    "schafszucht": "produktion", "rinderfarm": "produktion", "pferdezucht": "produktion",
    "jaeger": "produktion",
    "schmiede": "werkstatt", "bogenbauer": "werkstatt", "naehstube": "werkstatt",
    "kriegerakademie": "ausbildung", "diebesgilde": "ausbildung", "stellmacher": "ausbildung",
    "verteidigungswall": "wall",
    "bibliothek": "bibliothek",
    "haus": "haus",
    "lager": "lager",
}

# Dach-/Koerperfarbe je Familie — das Haus bleibt in der bisherigen Gold-Optik.
_FARBEN = {
    "haus": ("#E8C15A", "#8A6A2A"),
    "produktion": ("#C9A227", "#6E5A2E"),
    "werkstatt": ("#9AA7B0", "#4A5560"),
    "ausbildung": ("#B26A4A", "#6B4F2A"),
    "wall": ("#8A8F98", "#5A5F66"),
    "bibliothek": ("#8E7CC3", "#5A4E7A"),
    "lager": ("#B08968", "#6E5A3C"),
}

_RAND = "#17212B"
_PIP = "#F2C94C"


def gebaeude_plan(gebaeude_key: str, x0: float, y0: float, zelle: float,
                  stufe: int = 1, max_stufe: int | None = None) -> list[dict]:
    """Zeichenplan fuer das Gebaeude auf einer Zelle.

    ``gebaeude_key`` ist eine der 20 Kennungen aus ``gelaende.alle_gebaeude()``. Das Zeichen
    unterscheidet sich nach Gebaeudefamilie (Haus, Produktion, Werkstatt, Ausbildung, Wall,
    Bibliothek, Lager) und behaelt die gewohnte Form aus Dach und Koerper.

    ``stufe`` wird als kleine Pips gezeichnet; ``max_stufe`` ist die Obergrenze und deckelt
    die Pip-Zahl. Ist ``max_stufe`` None, werden KEINE Pips gezeichnet. Eine unbekannte
    Kennung wirft einen klaren ValueError.
    """
    key = str(gebaeude_key).strip().lower()
    if key not in _FAMILIE:
        raise ValueError(
            f"Unbekanntes Gebaeude: {gebaeude_key!r} — erwartet eine der 20 Kennungen aus "
            f"gelaende.alle_gebaeude()")
    familie = _FAMILIE[key]
    dach, koerper = _FARBEN[familie]

    formen: list[dict] = []
    if familie == "wall":
        # Wall: Steinwall mit drei Zinnen statt eines Daches.
        formen.append({"form": "rectangle",
                       "box": _box(x0, y0, zelle, 0.16, 0.42, 0.84, 0.82),
                       "farbe": koerper, "rand": _RAND})
        for u1 in (0.16, 0.43, 0.70):
            formen.append({"form": "rectangle",
                           "box": _box(x0, y0, zelle, u1, 0.30, u1 + 0.14, 0.42),
                           "farbe": dach, "rand": _RAND})
        formen.append({"form": "line",
                       "punkte": _punkte(x0, y0, zelle, 0.16, 0.62, 0.84, 0.62),
                       "farbe": "#3E4249", "breite": 1})
    else:
        formen.append({"form": "polygon",
                       "punkte": _punkte(x0, y0, zelle, 0.20, 0.52, 0.50, 0.20, 0.80, 0.52),
                       "farbe": dach, "rand": _RAND})
        formen.append({"form": "rectangle",
                       "box": _box(x0, y0, zelle, 0.32, 0.52, 0.68, 0.82),
                       "farbe": koerper, "rand": _RAND})

    if familie == "haus":
        formen.append({"form": "rectangle",
                       "box": _box(x0, y0, zelle, 0.45, 0.64, 0.55, 0.82),
                       "farbe": "#3A2A18"})
        formen.append({"form": "rectangle",
                       "box": _box(x0, y0, zelle, 0.58, 0.58, 0.64, 0.64),
                       "farbe": "#17212B"})
    elif familie == "produktion":
        formen.append({"form": "rectangle",
                       "box": _box(x0, y0, zelle, 0.60, 0.28, 0.68, 0.46),
                       "farbe": "#4A3E2A"})
        formen.append({"form": "oval",
                       "box": _box(x0, y0, zelle, 0.24, 0.70, 0.32, 0.78),
                       "farbe": "#9AA7B0"})
    elif familie == "werkstatt":
        formen.append({"form": "rectangle",
                       "box": _box(x0, y0, zelle, 0.30, 0.72, 0.46, 0.80),
                       "farbe": "#2A2F36"})
        formen.append({"form": "line",
                       "punkte": _punkte(x0, y0, zelle, 0.52, 0.66, 0.66, 0.80),
                       "farbe": _STAMM, "breite": 2})
    elif familie == "ausbildung":
        formen.append({"form": "line",
                       "punkte": _punkte(x0, y0, zelle, 0.50, 0.20, 0.50, 0.08),
                       "farbe": "#3A2A18", "breite": 2})
        formen.append({"form": "polygon",
                       "punkte": _punkte(x0, y0, zelle, 0.50, 0.10, 0.66, 0.14, 0.50, 0.18),
                       "farbe": _PIP})
    elif familie == "bibliothek":
        for u in (0.34, 0.50, 0.66):
            formen.append({"form": "line",
                           "punkte": _punkte(x0, y0, zelle, u, 0.54, u, 0.80),
                           "farbe": "#D7D0E8", "breite": 2})
    elif familie == "lager":
        formen.append({"form": "line",
                       "punkte": _punkte(x0, y0, zelle, 0.34, 0.56, 0.66, 0.80),
                       "farbe": "#3A2A18", "breite": 2})
        formen.append({"form": "line",
                       "punkte": _punkte(x0, y0, zelle, 0.66, 0.56, 0.34, 0.80),
                       "farbe": "#3A2A18", "breite": 2})

    # Ausbaustufe als Pips unten im Feld. max_stufe None -> keine Pips; sonst min(stufe, max).
    if max_stufe is not None:
        obergrenze = max(0, int(max_stufe))
        anzahl = max(0, min(int(stufe), obergrenze))
        abstand = 0.09
        for j in range(anzahl):
            u = 0.5 + (j - (anzahl - 1) / 2.0) * abstand
            formen.append({"form": "rectangle",
                           "box": _box(x0, y0, zelle, u - 0.017, 0.90, u + 0.017, 0.96),
                           "farbe": _PIP})
    return formen


# --------------------------------------------------------------------------
# Wege zwischen bebauten Feldern
# --------------------------------------------------------------------------

_WEG_FARBE = "#6B4F2A"   # gedaempftes Erdbraun (data/gelaende.json: Forumlogo-Braun #6B4F2A)


def wege_plan(bauten: dict, spalten: int, zelle: float, x0: float = 0.0,
              y0: float = 0.0) -> list[dict]:
    """Wege zwischen ORTHOGONAL benachbarten bebauten Feldern.

    ``bauten`` ist ein dict {Feldindex als Zeichenkette: Gebaeudekennung}, ``spalten`` die
    Zahl der Spalten je Zeile. Fuer jedes Paar direkt benachbarter bebauter Felder (waagerecht
    oder senkrecht, keine Diagonalen, kein Zeilenumbruch) entsteht GENAU EIN Wegeintrag, der
    von Zellmitte ueber den Mittelpunkt der gemeinsamen Kante zur anderen Zellmitte fuehrt.
    Doppelte Paare werden vermieden.
    """
    spalten = int(spalten)
    if spalten <= 0:
        raise ValueError(f"spalten muss positiv sein, war {spalten!r}")

    belegt: dict = {}
    for schluessel in bauten:
        try:
            belegt[int(schluessel)] = bauten[schluessel]
        except (TypeError, ValueError):
            continue   # unbrauchbare Schluessel werden uebergangen

    def zentrum(index: int):
        zeile, spalte = divmod(index, spalten)
        return (x0 + (spalte + 0.5) * zelle, y0 + (zeile + 0.5) * zelle)

    formen: list[dict] = []
    gesehen: set = set()
    for i in sorted(belegt):
        nachbarn = []
        if (i % spalten) != spalten - 1:
            nachbarn.append(i + 1)          # rechtes Feld in derselben Zeile
        nachbarn.append(i + spalten)        # Feld darunter in derselben Spalte
        for j in nachbarn:
            if j not in belegt:
                continue
            paar = (i, j)
            if paar in gesehen:
                continue
            gesehen.add(paar)
            links_oben = zentrum(i)
            rechts_unten = zentrum(j)
            zeile_i, spalte_i = divmod(i, spalten)
            if j == i + 1:
                kante = (x0 + (spalte_i + 1) * zelle, y0 + (zeile_i + 0.5) * zelle)
            else:
                kante = (x0 + (spalte_i + 0.5) * zelle, y0 + (zeile_i + 1) * zelle)
            formen.append({
                "form": "line",
                "punkte": [links_oben[0], links_oben[1], kante[0], kante[1],
                           rechts_unten[0], rechts_unten[1]],
                "farbe": _WEG_FARBE,
                "breite": max(2.0, zelle * 0.12),
            })
    return formen


# --------------------------------------------------------------------------
# Rasterlinien
# --------------------------------------------------------------------------

def raster_plan(spalten: int, zeilen: int, zelle: float, x0: float = 0.0,
                y0: float = 0.0, farbe: str = "#0B0F12") -> list[dict]:
    """Das Zellenraster als duenne Linien: (spalten+1) senkrechte + (zeilen+1) waagerechte."""
    spalten = int(spalten)
    zeilen = int(zeilen)
    breite = max(1.0, zelle / 32.0)
    breit = x0 + spalten * zelle
    hoch = y0 + zeilen * zelle
    formen: list[dict] = []
    for c in range(spalten + 1):
        xx = x0 + c * zelle
        formen.append({"form": "line", "punkte": [xx, y0, xx, hoch],
                       "farbe": farbe, "breite": breite})
    for r in range(zeilen + 1):
        yy = y0 + r * zelle
        formen.append({"form": "line", "punkte": [x0, yy, breit, yy],
                       "farbe": farbe, "breite": breite})
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
            canvas.create_line(*eintrag["punkte"], tags=tags, **_fuell(eintrag))
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
        "Die 7 Gelaende-Embleme sind Vorschlaege: das Handbuch 2009 nennt keine Vorgabe fuer "
        "die Kartenoptik (nur die 7 Gelaendearten selbst sind belegt).",
        "Die Kartengroesse 8x7 = 56 Felder mit 40 bebaubaren ist Daniel-Entscheidung ",
        "(05.10.2026); das Handbuch nennt keine Kartengroesse.",
        "Die Kartenfarben in data/gelaende.json sind angenaehert, nicht gemessen "
        "(archiv/analysen/audits/astra_wallpaper_antwort.txt).",
        "Die Zuordnung der Gebaeude zu Familien spiegelt die Spalte 'kategorie' aus "
        "data/buildings.json (20 Gebaeude); ein dort neu ergaenztes Gebaeude fehlt hier und "
        "wuerde einen ValueError ausloesen.",
        "Die Pips zeigen nur die erreichte Stufe (stufe); max_stufe dient allein als Deckel "
        "und wird nicht als Umriss mitgezeichnet.",
    ]

```

### Datei `src/karten_optik_fein.py` (863 Zeilen)

```python
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

    archiv/analysen/audits/ux_astra_karten_feinheit_2026-10-05.txt

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
# Quelle: archiv/analysen/audits/ux_astra_karten_feinheit_2026-10-05.txt, Abschnitt "Siedlung 1 – Gebäude":
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
        "archiv/analysen/audits/ux_astra_karten_feinheit_2026-10-05.txt (Vorschlaege, keine belegten "
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

```


## Ausgabeformat (genau so, nichts anderes)

### 1. Befund in fünf Sätzen
Was ist hier wirklich das Problem — mit Zahlen aus dem Code.

### 2. Vorschläge (Tabelle, absteigend nach Nutzen)

| # | Was | Dateien/Funktionen | Zeilen vorher → nachher | Risiko (klein/mittel/groß) | Beweis: welche Prüfdatei | Reihenfolge |
|---|---|---|---|---|---|---|

### 3. Zusammenführung im Detail
Für die zwei wichtigsten Vorschläge: welche Funktionen verschmelzen zu welcher neuen Funktion,
welche Parameter, welcher Rückgabewert, was passiert mit Sonderfällen. Kein vollständiger Code —
nur Signatur plus drei bis fünf Zeilen Kern.

### 4. Was du NICHT anfassen würdest
Und warum. (Beispiel: Zeichencode der Oberfläche, der auf Pixel wirkt.)

### 5. Ordnung
Wie sähe eine saubere Ordner-/Dateistruktur für diesen Teil aus? Namen der Dateien, was in welche
gehört, und **in welcher Reihenfolge man umzieht, ohne dass Importe brechen**.
