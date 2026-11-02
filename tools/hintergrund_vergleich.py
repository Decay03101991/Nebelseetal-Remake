"""Vergleichsblatt: Gebaeudemotiv als Hintergrund statt als Bild oben drueber (02.11.2026).

VORGABE Daniel 02.11.2026 (Screenshot in `docs/eingaben/`): die gemalten Bilder fuer Dorfzentrum,
Stellmacher, Kriegerakademie sollen der HINTERGRUND ihrer Ansicht sein, nicht einfach als Bild oben
drueber - und: "Die texte muessen erkennbar bleiben also kleinere textbloecke die nicht transparent
sind und der rest so transparent das moeglichst viel vom bild durchkommt".

Dieses Werkzeug baut KEINE Spielansicht um, sondern zeigt drei Fassungen als Bild, damit Daniel
vorher entscheidet (Projektregel: Optik erst zeigen, dann einhaengen). Alle Masse und Farben stehen
unten als Zahlen; das Ergebnis liegt unter docs/design/.

Aufruf:  python -X utf8 tools/hintergrund_vergleich.py
"""
from __future__ import annotations

import os
import sys
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import gebaeude_optik  # noqa: E402  (die EINE Stelle fuer Motivpfade)

BREITE, HOEHE = 1100, 760                     # Fenstergroesse der Vergleichsbilder
KASTEN_FARBE = (26, 22, 16, 255)               # deckender Textkasten (dunkles Braun)
KASTEN_RAND = (74, 62, 44, 255)                # feine Kante, damit der Kasten als Kasten lesbar ist
GOLD = (218, 165, 32, 255)                     # Ueberschrift
TEXT = (243, 244, 246, 255)                    # Fliesstext
GEDAEMPFT = (192, 192, 192, 255)               # Hinweiszeilen
ABDUNKELUNG_PROZENT = 25                        # Fassung C: so weit wird das Bild abgedunkelt

# Die Zeilen stammen aus der echten Dorfzentrum-Ansicht (Kurzfassung fuer den Vergleich).
TITEL = "Dorfzentrum"
ZEILEN: List[Tuple[str, str]] = [
    ("Dein naechster Schritt", "Siedlung 1 oeffnen - weiterbauen"),
    ("", "Bevoelkerung: 15 Siedler · Lagerverwaltung dieses Dorfes"),
    ("", "Holz 81 · Stein 116 · Nahrung 24 · Leder 0 · Gold 0"),
    ("Gebaeude", "Dorfzentrum 1 · Holzfeller 3 · Steinmetz 2 · Farm 2"),
    ("Auftraege", "keine unterwegs"),
]


def _schrift(groesse: int, fett: bool = False) -> ImageFont.FreeTypeFont:
    """Eine Windows-Schrift, sonst die eingebaute - das Blatt muss auf jedem Rechner bauen."""
    name = "segoeuib.ttf" if fett else "segoeui.ttf"             # Segoe UI ist auf Windows vorhanden
    pfad = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", name)
    try:
        return ImageFont.truetype(pfad, groesse)                # echte Schrift
    except OSError:
        return ImageFont.load_default()                          # Rueckfall ohne Absturz


def _motiv(gebaeude: str) -> Image.Image:
    """Das gelieferte Motiv als RGBA - fehlt es, ein dunkler Ersatz (kein Absturz)."""
    pfad = gebaeude_optik.pfad_hintergrund(gebaeude)             # Pfad aus der EINEN Quelle
    if pfad and os.path.exists(pfad):
        return Image.open(pfad).convert("RGBA")                 # das echte Bild
    return Image.new("RGBA", (538, 222), (40, 30, 20, 255))     # Ersatzflaeche


def _hintergrund_bild(motiv: Image.Image, abdunkeln: int = 0) -> Image.Image:
    """Das Motiv fuellt die Flaeche (cover), optional abgedunkelt - "moeglichst viel vom Bild"."""
    skala = max(BREITE / motiv.width, HOEHE / motiv.height)      # cover: keine leeren Raender
    gross = motiv.resize((max(1, int(motiv.width * skala)), max(1, int(motiv.height * skala))),
                         Image.LANCZOS)                           # hochskaliert
    links = (gross.width - BREITE) // 2                           # mittig zuschneiden
    oben = (gross.height - HOEHE) // 2
    flaeche = gross.crop((links, oben, links + BREITE, oben + HOEHE)).convert("RGBA")
    if abdunkeln > 0:                                             # Fassung C
        schleier = Image.new("RGBA", flaeche.size, (0, 0, 0, int(255 * abdunkeln / 100)))
        flaeche = Image.alpha_composite(flaeche, schleier)
    return flaeche


def _kasten(draw: ImageDraw.ImageDraw, x: int, y: int, text: str,
            schrift, farbe=TEXT, innen: int = 10) -> Tuple[int, int]:
    """Einen DECKENDEN Kasten um eine Textzeile zeichnen; liefert die naechste y-Position."""
    if not text:
        return (x, y)
    links, oben, rechts, unten = draw.textbbox((0, 0), text, font=schrift)
    breite, hoehe = rechts - links, unten - oben
    draw.rectangle((x, y, x + breite + 2 * innen, y + hoehe + 2 * innen),
                   fill=KASTEN_FARBE, outline=KASTEN_RAND)          # der Kasten ist NICHT transparent
    draw.text((x + innen - links, y + innen - oben), text, font=schrift, fill=farbe)
    return (x, y + hoehe + 2 * innen + 6)                           # Abstand zur naechsten Zeile


def _fassung_a(motiv: Image.Image) -> Image.Image:
    """HEUTE: das Motiv liegt als Bild oben ueber dem Inhalt, alles darunter ist dunkle Flaeche."""
    bild = Image.new("RGBA", (BREITE, HOEHE), (23, 33, 43, 255))    # skin["bg"]
    draw = ImageDraw.Draw(bild)
    draw.text((24, 16), TITEL, font=_schrift(34, True), fill=GOLD)
    bild.alpha_composite(motiv.resize((538, 222), Image.LANCZOS), (24, 66))   # Bild OBEN drueber
    y = 300                                                          # darunter nur Text auf dunkler Flaeche
    for links, rechts in ZEILEN:
        if links:
            y = _kasten(draw, 24, y, links, _schrift(15, True), GOLD)[1]
        if rechts:
            y = _kasten(draw, 24, y, rechts, _schrift(15), TEXT)[1]
    draw.text((24, HOEHE - 34), "Fassung A: Bild oben drueber (heute)", font=_schrift(16, True),
              fill=GEDAEMPFT)
    return bild


def _fassung_b(motiv: Image.Image) -> Image.Image:
    """NEU: das Motiv ist der HINTERGRUND; Text steht in kleinen deckenden Kaesten."""
    bild = _hintergrund_bild(motiv)                                  # das Bild traegt die Ansicht
    draw = ImageDraw.Draw(bild)
    y = 18
    y = _kasten(draw, 24, y, TITEL, _schrift(34, True), GOLD, innen=12)[1]
    for links, rechts in ZEILEN:
        y = _kasten(draw, 24, y, links, _schrift(15, True), GOLD)[1]
        y = _kasten(draw, 24, y, rechts, _schrift(15), TEXT)[1]
    draw.text((24, HOEHE - 34), "Fassung B: Bild als Hintergrund, Text in deckenden Kaesten",
              font=_schrift(16, True), fill=GEDAEMPFT)
    return bild


def _fassung_c(motiv: Image.Image) -> Image.Image:
    """NEU, ruhiger: wie B, aber das Bild ist leicht abgedunkelt - mehr Kontrast fuer den Text."""
    bild = _hintergrund_bild(motiv, abdunkeln=ABDUNKELUNG_PROZENT)
    draw = ImageDraw.Draw(bild)
    y = 18
    y = _kasten(draw, 24, y, TITEL, _schrift(34, True), GOLD, innen=12)[1]
    for links, rechts in ZEILEN:
        y = _kasten(draw, 24, y, links, _schrift(15, True), GOLD)[1]
        y = _kasten(draw, 24, y, rechts, _schrift(15), TEXT)[1]
    draw.text((24, HOEHE - 34),
              "Fassung C: wie B, Bild %d %% abgedunkelt (mehr Kontrast)" % ABDUNKELUNG_PROZENT,
              font=_schrift(16, True), fill=GEDAEMPFT)
    return bild


def blatt_bauen(gebaeude: str = "lager", ziel: str = "") -> str:
    """Die drei Fassungen nebeneinander als EIN Bild speichern und den Pfad zurueckgeben."""
    motiv = _motiv(gebaeude)                                        # das gelieferte Motiv
    fassungen = [_fassung_a(motiv), _fassung_b(motiv), _fassung_c(motiv)]   # A, B, C
    abstand = 14                                                    # Luft zwischen den Fassungen
    blatt = Image.new("RGBA", (3 * BREITE + 4 * abstand, HOEHE + 2 * abstand + 44),
                      (12, 12, 14, 255))                            # dunkler Hintergrund des Blattes
    for i, fassung in enumerate(fassungen):                         # nebeneinander setzen
        blatt.alpha_composite(fassung, (abstand + i * (BREITE + abstand), abstand + 40))
    draw = ImageDraw.Draw(blatt)
    draw.text((abstand, 10), "Gebaeudemotiv als Hintergrund - drei Fassungen (%s)" % gebaeude,
              font=_schrift(20, True), fill=(255, 232, 194, 255))
    ziel = ziel or os.path.join(ROOT, "docs", "design", "HINTERGRUND_VERGLEICH_20261102.png")
    os.makedirs(os.path.dirname(ziel), exist_ok=True)               # Ordner anlegen
    blatt.convert("RGB").save(ziel, "PNG")                           # als PNG ablegen
    return ziel


if __name__ == "__main__":                                          # direkter Aufruf
    pfad = blatt_bauen(sys.argv[1] if len(sys.argv) > 1 else "lager",
                       sys.argv[2] if len(sys.argv) > 2 else "")
    print("Vergleichsblatt:", pfad, os.path.getsize(pfad), "Bytes")
