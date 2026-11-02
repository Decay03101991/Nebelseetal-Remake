"""Vergleichsblatt: Truppenbewegungen auf der Weltkarte - drei Fassungen (02.11.2026).

VORGABE Daniel 02.11.2026 (Registerpunkt 140): Truppenbewegungen sind auf der Karte sichtbar -
Startfeld, Zielfeld, die Linie und eine GROBE Restlaufzeit; Truppenart, Anzahl, Karren und die
genaue Geschwindigkeit bleiben verborgen ("Ein einzelner handkarren erzeugt das gleiche
bewegungssymbol wie eine ganze armee"). Die Zahlen der drei Fassungen stammen aus dem Entwurf des
starken Modells (`docs/design/MARSCH_ENTWURF_20261102.md`, Abschnitt A) und stehen hier EINMAL als
Tabelle - dieses Werkzeug baut nur das Bild, es aendert keine Spielansicht.

Gezeigt wird je Fassung zweimal dieselbe Szene:
  oben  - doppelt gross (40 px je Feld), damit man Symbol und Linie beurteilen kann,
  unten - in ORIGINALGROESSE wie im Spiel (20 px je Feld, 400 x 400 px), damit man sieht,
          was bei echter Groesse noch lesbar ist.

Aufruf:  python -X utf8 tools/marsch_vergleich.py
"""
# -*- coding: ascii -*-
from __future__ import annotations

import os
import sys
from typing import Dict, List, Tuple

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # Projektwurzel
sys.path.insert(0, os.path.join(ROOT, "src"))                        # src importierbar machen

import bottaktik      # noqa: E402  (feste Dorfpositionen aus Name und Nummer)
import portalraum     # noqa: E402  (Gelaende je Feld - dieselbe Quelle wie das Spiel)

ZIEL = os.path.join(ROOT, "docs", "design", "MARSCH_VERGLEICH_20261102.png")

HINTERGRUND = (12, 12, 14, 255)      # dunkler Rand des Blattes
TITELFARBE = (255, 232, 194, 255)    # warmes Weiss fuer die Ueberschrift
GEDAEMPFT = (192, 192, 192, 255)     # Hinweiszeilen
GOLD = (218, 165, 32, 255)           # Feldbeschriftung
DORF_FUELLUNG = "#B45309"            # fremdes Dorf, wie in main._render_portal
DORF_RAND = "#FFE8C2"                # Rand und Kreuz des Dorfzeichens, wie im Spiel

# Die drei Fassungen des Entwurfs - ALLE Zahlen aus docs/design/MARSCH_ENTWURF_20261102.md A.1-A.3.
FASSUNGEN: Dict[str, Dict[str, object]] = {
    "A": {  # Fassung A: Punkt und Linie, laufender Punkt
        "name": "A - Punkt und Linie (laufender Punkt)",
        "symbol": "kreis",               # Form des Marschzeichens
        "symbol_px": 6,                  # Durchmesser in px
        "symbol_fuellung": "#F59E0B",    # Fuellung
        "symbol_rand": "#7C2D12",        # Rand
        "linie_farbe": "#F59E0B",        # Linienfarbe Hinreise
        "linie_breite": 2,               # Linienbreite in px
        "dash": None,                    # durchgezogen
        "takt_ms": 400,                  # Takt der Bewegung
        "puls": False,                   # kein Puls
    },
    "B": {  # Fassung B: Pfeilspitze zeigt die Richtung
        "name": "B - Pfeil (Richtung ueber die Spitze)",
        "symbol": "pfeil",               # Dreieck in Laufrichtung
        "symbol_px": 6,                  # Spitzenlaenge in px
        "symbol_fuellung": "#EF4444",    # Fuellung
        "symbol_rand": "#000000",        # Rand
        "linie_farbe": "#EF4444",        # Linienfarbe Hinreise
        "linie_breite": 2,               # Linienbreite in px
        "dash": (4, 3),                  # gestrichelt
        "takt_ms": 400,                  # Takt der Bewegung
        "puls": False,                   # kein Puls
    },
    "C": {  # Fassung C: Ameisenstrasse und Puls
        "name": "C - Puls und Ameisenstrasse",
        "symbol": "kreis",               # Kreis mit Puls
        "symbol_px": 8,                  # Durchmesser in px (Radius 4)
        "symbol_fuellung": "#22C55E",    # Fuellung
        "symbol_rand": "#052E16",        # Rand
        "linie_farbe": "#22C55E",        # Linienfarbe Hinreise
        "linie_breite": 3,               # Linienbreite in px
        "dash": (6, 4),                  # gestrichelt, wandernd (dashoffset)
        "takt_ms": 200,                  # Takt der Strichwanderung
        "puls": True,                    # Punkt pulsiert (Radius 4 bis 5 px)
    },
}

MARKER_KANTE = 8                     # hohles Quadrat fuer Start- und Zielfeld (A.1)
MARKER_FARBE = "#DAA520"             # Farbe der beiden Marker
FORTSCHRITT = 0.45                   # gezeigter Stand der Bewegung (45 % der Strecke)
KANTE = 20                           # Rasterweite des Portals in Feldern
FELD_GROSS = 40                      # px je Feld im oberen (doppelt grossen) Bild
FELD_ECHT = 20                       # px je Feld im unteren Bild (wie im Spiel)


def _schrift(groesse: int, fett: bool = False) -> ImageFont.FreeTypeFont:
    """Eine Windows-Schrift, sonst die eingebaute - das Blatt muss auf jedem Rechner bauen."""
    name = "segoeuib.ttf" if fett else "segoeui.ttf"                  # Segoe UI ist auf Windows da
    pfad = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", name)
    try:
        return ImageFont.truetype(pfad, groesse)                      # echte Schrift
    except OSError:
        return ImageFont.load_default()                               # Rueckfall ohne Absturz


def _farbe(wert: str) -> Tuple[int, int, int, int]:
    """'#RRGGBB' in ein RGBA-Tupel - so zeichnet Pillow deckend."""
    wert = str(wert).lstrip("#")                                      # Raute entfernen
    return (int(wert[0:2], 16), int(wert[2:4], 16), int(wert[4:6], 16), 255)


def _szene() -> Tuple[List[dict], Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
    """Gelaende, eigene Siedlung und zwei fremde Doerfer fuer das Beispielbild.

    Die Dorfpositionen kommen aus `bottaktik.dorf_position` (dieselbe Funktion wie im Spiel), das
    Gelaende aus `portalraum.anzeige_raster` (dieselbe Quelle wie das Kaestchen). Nichts erfunden.
    """
    felder = portalraum.anzeige_raster(portalraum.index_von(1), 10, [1])   # Dimension 01, ganzes Raster
    eigen = (10, 10)                                                  # angenommene eigene Siedlung
    kandidaten = [(name, bottaktik.dorf_position(name, 0, KANTE))
                  for name in ("Haug", "Grom", "Vintar", "Brak", "Haldor")]
    # das Dorf nehmen, das 6 bis 11 Felder weit weg liegt - eine lesbare Diagonale
    ziel = next(((n, p) for n, p in kandidaten
                 if 6 <= abs(p[0] - eigen[0]) + abs(p[1] - eigen[1]) <= 11), kandidaten[0])
    zweit = next(((n, p) for n, p in kandidaten
                  if (n, p) != ziel and 4 <= abs(p[0] - eigen[0]) + abs(p[1] - eigen[1]) <= 12),
                 kandidaten[1])
    return felder, eigen, ziel[1], zweit[1]


def _raster_bilden(felder: List[dict], feld: int, kante: int) -> Image.Image:
    """Das Gelaende als Bild - Fuellungen wie im Spiel, Gitterlinien wie im Spiel."""
    bild = Image.new("RGBA", (kante * feld, kante * feld), (23, 33, 43, 255))
    draw = ImageDraw.Draw(bild)
    for eintrag in felder:
        x1, y1 = int(eintrag["x"]) * feld, int(eintrag["y"]) * feld
        draw.rectangle((x1, y1, x1 + feld, y1 + feld),
                       fill=_farbe(eintrag.get("gelaende_farbe") or "#555555"),
                       outline=(17, 17, 17, 255))
    return bild


def _dorf(draw: ImageDraw.ImageDraw, pos: Tuple[int, int], feld: int) -> None:
    """Ein fremdes Dorf zeichnen - Quadrat mit Kreuz, wie `main._render_portal` es heute tut."""
    cx, cy = pos[0] * feld + feld / 2.0, pos[1] * feld + feld / 2.0  # Feldmitte
    halb = max(3.0, feld * 0.24)                                      # halbe Kantenlaenge
    draw.rectangle((cx - halb, cy - halb, cx + halb, cy + halb),
                   fill=_farbe(DORF_FUELLUNG), outline=_farbe(DORF_RAND), width=2)
    draw.line((cx - halb, cy - halb, cx + halb, cy + halb), fill=_farbe(DORF_RAND), width=1)
    draw.line((cx - halb, cy + halb, cx + halb, cy - halb), fill=_farbe(DORF_RAND), width=1)


def _hohl(draw: ImageDraw.ImageDraw, pos: Tuple[int, int], feld: int) -> None:
    """Start- oder Zielfeld: hohles Quadrat, Kante 8 px (Entwurf A.1)."""
    cx, cy = pos[0] * feld + feld / 2.0, pos[1] * feld + feld / 2.0  # Feldmitte
    halb = MARKER_KANTE / 2.0 * (feld / FELD_ECHT)                     # im doppelten Bild mitskalieren
    draw.rectangle((cx - halb, cy - halb, cx + halb, cy + halb),
                   outline=_farbe(MARKER_FARBE), width=1)


def _pfeil(draw: ImageDraw.ImageDraw, mitte: Tuple[float, float], richtung: Tuple[float, float],
           laenge: float) -> None:
    """Eine Pfeilspitze in Laufrichtung - drei Punkte, Spitze in Richtung des Ziels."""
    dx, dy = richtung                                                    # Richtungsvektor
    norm = max(1e-6, (dx * dx + dy * dy) ** 0.5)                         # Laenge des Vektors
    dx, dy = dx / norm, dy / norm                                        # Einheitsvektor
    px, py = -dy, dx                                                     # Senkrechte dazu
    spitze = (mitte[0] + dx * laenge, mitte[1] + dy * laenge)            # vorderste Spitze
    links = (mitte[0] - dx * laenge * 0.6 + px * laenge * 0.7,
             mitte[1] - dy * laenge * 0.6 + py * laenge * 0.7)           # linke Ecke
    rechts = (mitte[0] - dx * laenge * 0.6 - px * laenge * 0.7,
              mitte[1] - dy * laenge * 0.6 - py * laenge * 0.7)          # rechte Ecke
    draw.polygon([spitze, links, rechts], fill=_farbe("#EF4444"), outline=_farbe("#000000"))


def _fassung_bilden(fassung: Dict[str, object], felder: List[dict], start: Tuple[int, int],
                    ziel: Tuple[int, int], zweit: Tuple[int, int], feld: int,
                    skala: float) -> Image.Image:
    """EIN Bild einer Fassung: Gelaende, zwei Doerfer, zwei Maersche mit Linie und Marschzeichen."""
    bild = _raster_bilden(felder, feld, KANTE)                           # Gelaende als Unterlage
    draw = ImageDraw.Draw(bild)
    _dorf(draw, ziel, feld)                                              # das angegriffene Dorf
    _dorf(draw, zweit, feld)                                             # ein zweites Dorf daneben
    breite = max(1, int(round(float(fassung["linie_breite"]) * skala)))  # Linienbreite mitskaliert
    for zielpos, anteil in ((ziel, FORTSCHRITT), (zweit, 0.7)):           # zwei Maersche gleichzeitig
        x1, y1 = start[0] * feld + feld / 2.0, start[1] * feld + feld / 2.0   # Startfeldmitte
        x2, y2 = zielpos[0] * feld + feld / 2.0, zielpos[1] * feld + feld / 2.0  # Zielfeldmitte
        _hohl(draw, start, feld)                                         # Startfeld markieren
        _hohl(draw, zielpos, feld)                                       # Zielfeld markieren
        kwargs = {"fill": _farbe(fassung["linie_farbe"]), "width": breite}   # Linienstil
        if fassung["dash"]:                                              # gestrichelt, wenn vorgesehen
            a, b = fassung["dash"]                                       # Strich- und Lueckenlaenge
            laenge = max(1e-6, ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)  # Laenge der Linie
            pos = 0.0                                                    # Startpunkt des Musters
            while pos < laenge:                                          # Muster Strich fuer Strich
                ende = min(laenge, pos + float(a) * skala)                # Ende des Strichs
                kwargs["width"] = breite
                draw.line((x1 + (x2 - x1) * pos / laenge, y1 + (y2 - y1) * pos / laenge,
                           x1 + (x2 - x1) * ende / laenge, y1 + (y2 - y1) * ende / laenge),
                          **kwargs)                                      # nur die Striche zeichnen
                pos = ende + float(b) * skala                            # Luecke ueberspringen
        else:
            draw.line((x1, y1, x2, y2), **kwargs)                        # durchgezogene Linie
        mx, my = x1 + (x2 - x1) * anteil, y1 + (y2 - y1) * anteil         # Stand nach anteil Strecke
        groesse = float(fassung["symbol_px"]) * skala                     # Symbolgroesse in px
        if fassung["symbol"] == "pfeil":                                  # Fassung B: Pfeilspitze
            _pfeil(draw, (mx, my), (x2 - x1, y2 - y1), groesse)           # Spitze in Laufrichtung
        else:                                                             # A und C: Kreis
            r = groesse / 2.0                                             # Radius aus Durchmesser
            draw.ellipse((mx - r, my - r, mx + r, my + r),
                         fill=_farbe(fassung["symbol_fuellung"]),
                         outline=_farbe(fassung["symbol_rand"]), width=1)
    return bild


def blatt_bauen(ziel_pfad: str = "") -> str:
    """Die drei Fassungen als EIN Blatt speichern (oben doppelt gross, unten in Originalgroesse)."""
    felder, start, ziel, zweit = _szene()                                # eine Szene fuer alle Fassungen
    kachel_gross = KANTE * FELD_GROSS                                    # 800 px
    kachel_echt = KANTE * FELD_ECHT                                      # 400 px
    laenge = max(len(v["name"]) for v in FASSUNGEN.values())             # nur fuer die Kopfzeile
    kopf = 34                                                            # Hoehe der Kopfzeile je Spalte
    fuss = 30                                                            # Hoehe der Fusszeile je Spalte
    abstand = 14                                                         # Luft zwischen den Spalten
    hoehe = kopf + kachel_gross + 26 + kachel_echt + fuss + 2 * abstand   # Gesamthoehe des Blattes
    breite = 3 * kachel_gross + 4 * abstand                              # Gesamtbreite des Blattes
    blatt = Image.new("RGBA", (breite, hoehe + 46), HINTERGRUND)         # dunkles Blatt
    draw = ImageDraw.Draw(blatt)
    draw.text((abstand, 12), "Truppenbewegungen auf der Weltkarte - drei Fassungen "
              "(oben doppelt gross, unten so gross wie im Spiel)", font=_schrift(20, True),
              fill=TITELFARBE)
    for i, (kennung, fassung) in enumerate(sorted(FASSUNGEN.items())):   # je Fassung eine Spalte
        links = abstand + i * (kachel_gross + abstand)                   # linke Kante der Spalte
        oben = 46 + kopf                                                 # Oberkante des grossen Bildes
        gross = _fassung_bilden(fassung, felder, start, ziel, zweit, FELD_GROSS, 2.0)
        blatt.alpha_composite(gross, (links, oben))                      # grosses Bild einsetzen
        draw.text((links, 46 + 10), str(fassung["name"]), font=_schrift(17, True), fill=GOLD)
        klein_oben = oben + kachel_gross + 26                            # Oberkante des echten Bildes
        klein = _fassung_bilden(fassung, felder, start, ziel, zweit, FELD_ECHT, 1.0)
        blatt.alpha_composite(klein, (links, klein_oben))                # Bild in Originalgroesse
        draw.text((links, klein_oben + kachel_echt + 6),
                  "Originalgroesse %d x %d px (%d px je Feld) - Takt %d ms, Symbol %d px%s"
                  % (kachel_echt, kachel_echt, FELD_ECHT, int(fassung["takt_ms"]),
                     int(fassung["symbol_px"]), ", gestrichelt" if fassung["dash"] else ""),
                  font=_schrift(14), fill=GEDAEMPFT)
    draw.text((abstand, hoehe + 18),
              "Eigene Siedlung angenommen bei 10/10; fremde Doerfer fest aus Name und Nummer "
              "(bottaktik.dorf_position); zwei Maersche gleichzeitig gezeigt.",
              font=_schrift(14), fill=GEDAEMPFT)
    ziel_pfad = ziel_pfad or ZIEL                                        # Standardziel
    os.makedirs(os.path.dirname(ziel_pfad), exist_ok=True)               # Ordner anlegen
    blatt.convert("RGB").save(ziel_pfad, "PNG")                          # als PNG ablegen
    return ziel_pfad


if __name__ == "__main__":                                               # direkter Aufruf
    pfad = blatt_bauen(sys.argv[1] if len(sys.argv) > 1 else "")
    print("Vergleichsblatt:", pfad, os.path.getsize(pfad), "Bytes")
