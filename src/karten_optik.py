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
        "(docs/audits/astra_wallpaper_antwort.txt).",
        "Die Zuordnung der Gebaeude zu Familien spiegelt die Spalte 'kategorie' aus "
        "data/buildings.json (20 Gebaeude); ein dort neu ergaenztes Gebaeude fehlt hier und "
        "wuerde einen ValueError ausloesen.",
        "Die Pips zeigen nur die erreichte Stufe (stufe); max_stufe dient allein als Deckel "
        "und wird nicht als Umriss mitgezeichnet.",
    ]
