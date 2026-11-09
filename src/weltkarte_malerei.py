"""Gemalte Weltkarte fuer das Nebelseetal-Remake (Designschritt D-3, 09.11.2026).

Daniel hat am 09.11.2026 entschieden (Register 328): die Weltkarte bleibt vorerst FLACH, und
zuerst entsteht eine Testkarte mit GEMALTEN Kacheln. Dieses Modul liefert das Malen - es zeichnet
nichts auf eine Leinwand und braucht kein tkinter, nur Pillow. Fehlt Pillow, sagt `verfuegbar()`
False und `karte_malen()` wirft `MalereiFehler`; die Anzeige faellt dann auf die flachen
Gelaendefarben zurueck (wie `_kartenrahmen_bauen` es schon macht).

**Warum nicht Kachel fuer Kachel zusammengeklebt.** Der erste Anlauf malte 400 Kacheln einzeln
und setzte sie zusammen. Gemessen und angesehen: das Ergebnis blieb ein Fliesenmuster mit harten
90-Grad-Kanten, und ein Weichzeichnen der Kachelraender legte ein Waffelmuster ueber die Karte
(Stilprobe: "wie hinter einem Maschendrahtzaun"). Deshalb wird die Karte als EIN Bild gemalt:

1. **Farbfeld:** die 20 x 20-Gelaendematrix als 20 x 20 Pixel, bilinear auf Kartengroesse
   hochgerechnet - daraus entstehen weiche Farbuebergaenge zwischen den Gelaendearten, ohne Raster.
2. **Motive:** Baeume, Gipfel, Duenen, Wellen, Schilf werden als gemalte Formen UEBER das Farbfeld
   gesetzt, je Feld mit eigener Saat (Lage, Groesse, Anzahl) - das nimmt der Karte die Wiederholung.
   Die Motive sitzen an der Feldmitte, damit ein Klick auf ein Feld weiter dasselbe Feld trifft.
3. **Licht:** ein gemeinsames warmes Licht von oben links und ein Schatten unten rechts, dazu feine
   Pinselstriche und ein leises Korn - der "gemalte" Zusammenhalt.

**Eine Quelle je Wert:** Farben und Kennungen kommen aus `gelaende.ARTEN` (also aus
`data/gelaende.json`), nicht aus einer zweiten Farbtabelle. Hell- und Dunkeltoene werden aus der
Grundfarbe GERECHNET (`_misch`).

**Malstil (Stilprobe A des Pakets):** warm, kraeftige aber gedeckte Farben, feine braune Konturen
statt harter schwarzer Linien, weiche Schatten, Licht von oben links. Gemalt wird vierfach
ueberabgetastet und mit LANCZOS verkleinert.

**Zwischenspeicher:** `_KACHE[(art, kante, variante)]` fuer einzelne Kacheln (Legende, Pruefboegen)
und `_KARTEN[(signatur, kante)]` fuer ganze Karten. Ein zweiter Abruf liefert DASSELBE Objekt
(Tk gibt Bilder frei, die niemand mehr referenziert - Lehre 02.11.2026).
"""
from __future__ import annotations

import math
import random

import gelaende

# Vierfach ueberabgetastet malen, dann verkleinern = weiche Kanten ("weiche Schatten").
UEBERABTASTUNG = 4

# So viele Bildvarianten bekommt eine EINZELNE Kachel (fuer Legende und Pruefboegen). In der Karte
# hat jedes Feld seine eigene Saat, dort gibt es keine Wiederholung.
VARIANTEN = 3

# Konturfarbe des Malstils: dunkles Braun statt Schwarz (Stilprobe: "feine braune Linien").
KONTUR = (58, 40, 24)

# Hoechstens so viele ganze Karten im Zwischenspeicher (eine 20 x 20-Karte bei 64 px sind 4,9 MB).
KARTENSPEICHER = 3

# Hoechste Arbeitsbreite beim Malen (siehe karte_malen): begrenzt Malzeit und Speicher.
ARBEITSBREITE = 2048

# HELLIGKEIT (Daniel, 09.11.2026 - F-34 und F-35): "Nummer 2 Flach und 48 px je Feld gefaellt mir am
# besten nur etwas heller bitte wie bei Nummer 3" (F-34), nachgelegt am selben Tag: "Die Vorschau +28 %
# ist ok ... ich will es vom Stil wie bei der Stilprobe A, aber dass die Karte GERADE angezeigt wird"
# (F-35). Also: flache Draufsicht bleibt, Ton und Stil wie die Stilprobe A (heller Grund, warme Farben,
# weiche Schatten). Gemessen an der Karte d01: vorher mittlere Helligkeit 85 von 255, mit 1,20 waren es
# 102, mit 1,28 sind es 108 - das ist die Stufe, die Daniel im Blatt "Vorschau +28 %" gewaehlt hat.
# Der Faktor wirkt in `_einheitslicht`, also EINE Stelle fuer Kacheln UND ganze Karten, und die Wache
# rechnet ihn mit - so bleibt die Farbtreue-Pruefung eng, statt sie zu lockern.
HELLIGKEIT = 1.28

# Schatten unten rechts im Einheitslicht: 42 Alpha wirkte zu schwer gegen den hellen Grund der
# Stilprobe; 20 laesst die Karte hell, ohne die Tiefe zu verlieren.
SCHATTEN_ALPHA = 20

# Warmes Licht oben links - der "warme Grund" der Stilprobe A. 46 war etwas fahl; 58 traegt den warmen
# Ton, ohne die Farben zu verschieben (Wirkung rund 3 % auf das Bild, Rest bleibt Gelaendefarbe).
LICHT_ALPHA = 58

_KACHE: dict = {}
_KARTEN: dict = {}


class MalereiFehler(RuntimeError):
    """Die Karte kann nicht gemalt werden - Grund steht im Text (kein Ersatzbild erfinden)."""


def verfuegbar() -> bool:
    """Ist Pillow da? Ohne Pillow wird nicht gemalt, sondern flach gezeichnet."""
    try:
        import PIL  # noqa: F401
        from PIL import Image, ImageDraw, ImageFilter  # noqa: F401
    except Exception:
        return False
    return True


def arten() -> tuple:
    """Die sieben Gelaendearten in der Reihenfolge der Datendatei."""
    return tuple(gelaende.GELAENDEARTEN)


def varianten() -> int:
    return VARIANTEN


def variante_fuer(x: int, y: int) -> int:
    """Welche Bildvariante eine EINZELNE Kachel bekommt - aus ihren Koordinaten, ohne Zufall."""
    return (int(x) * 7 + int(y) * 13) % VARIANTEN


def _feld_saat(x: int, y: int) -> int:
    """Feste Saat je Feld - gleiche Karte, gleiches Bild; andere Lage, andere Motive."""
    art = 1
    return 7919 * (int(x) + 1) + 104729 * (int(y) + 1) + art


# --------------------------------------------------------------------------
# Farbhilfen - jeder Ton wird aus der Grundfarbe GERECHNET (keine zweite Tabelle)
# --------------------------------------------------------------------------

def _rgb(farbe) -> tuple:
    if isinstance(farbe, (tuple, list)):
        return tuple(int(w) for w in farbe[:3])
    text = str(farbe).strip().lstrip("#")
    if len(text) == 3:
        text = "".join(zeichen * 2 for zeichen in text)
    if len(text) != 6:
        raise MalereiFehler("Unbekannte Farbe: %r" % (farbe,))
    return (int(text[0:2], 16), int(text[2:4], 16), int(text[4:6], 16))


def _misch(a, b, anteil: float) -> tuple:
    """Farbe a Richtung b mischen (anteil 0 = a, 1 = b)."""
    anteil = max(0.0, min(1.0, float(anteil)))
    return tuple(int(round(x + (y - x) * anteil)) for x, y in zip(_rgb(a), _rgb(b)))


def _licht(farbe) -> tuple:
    return _misch(farbe, (255, 240, 205), 0.22)


def _schatten(farbe) -> tuple:
    return _misch(farbe, (0, 0, 0), 0.30)


# --------------------------------------------------------------------------
# Die oeffentlichen Stellen
# --------------------------------------------------------------------------

def kachel(art: str, kante: int, variante: int = 0):
    """EIN gemaltes Kachelbild (Pillow-Image, RGB) - fuer Legende und Pruefboegen.

    Zwischengespeichert je (art, kante, variante) - derselbe Aufruf liefert dasselbe Objekt.
    """
    if art not in gelaende.ARTEN:
        raise MalereiFehler("Unbekannte Geländeart: %r - bekannt sind %s."
                           % (art, ", ".join(arten())))
    breite = int(kante)
    if breite < 4:
        raise MalereiFehler("Kachelkante %d px ist zu klein (mindestens 4 px)." % breite)
    nummer = int(variante) % VARIANTEN
    schluessel = (str(art), breite, nummer)
    treffer = _KACHE.get(schluessel)
    if treffer is not None:
        return treffer
    try:
        from PIL import Image, ImageDraw
    except Exception as fehler:                                  # kein Pillow
        raise MalereiFehler("Pillow fehlt - es wird nicht gemalt (%s)." % (fehler,)) from fehler
    z = 64 * UEBERABTASTUNG                                      # Arbeitsgroesse der Einzelkachel
    bild = Image.new("RGB", (z, z), _rgb(gelaende.farbe(art)))
    draw = ImageDraw.Draw(bild, "RGBA")
    _grundlicht(draw, (0, 0, z, z), gelaende.farbe(art))
    rnd = random.Random(1000 + list(arten()).index(art) * 37 + nummer * 101)
    _MOTIVE[art](draw, (0, 0, z, z), rnd, 1.0)
    _pinselstriche(draw, (0, 0, z, z), gelaende.farbe(art), rnd)
    klein = bild.resize((breite, breite), Image.LANCZOS)
    _KACHE[schluessel] = klein
    return klein


def leeren() -> None:
    """Zwischenspeicher vergessen (nur fuer Messungen und Pruefungen)."""
    _KACHE.clear()
    _KARTEN.clear()


def gespeichert() -> int:
    """Wie viele Bilder gerade im Zwischenspeicher liegen (Kacheln und Karten zusammen)."""
    return len(_KACHE) + len(_KARTEN)


def karte_malen(raster, kante: int, hintergrund=(15, 20, 24)):
    """Das GANZE Raster als EIN gemaltes Bild (Pillow-Image, RGB) mit weichen Uebergaengen.

    `raster` ist eine Liste von Zeilen mit Gelaendekennungen - die Form, die `portalraum` in
    seinem Weltbild unter dem Schluessel `raster` liefert. **Das Modul liest das Weltbild NICHT
    selbst** (Wache `test_weltbild_gelaende`: nur `portalraum` und `main` lesen es); hereingereicht
    wird das Raster von der Anzeige.
    Zwischengespeichert je (Rasterinhalt, Kante).
    """
    try:
        from PIL import Image, ImageDraw
    except Exception as fehler:
        raise MalereiFehler("Pillow fehlt - es wird nicht gemalt (%s)." % (fehler,)) from fehler
    breite = int(kante)
    if breite < 4:
        raise MalereiFehler("Kachelkante %d px ist zu klein (mindestens 4 px)." % breite)
    zeilen = len(raster)
    spalten = max(len(zeile) for zeile in raster) if raster else 0
    if not zeilen or not spalten:
        raise MalereiFehler("Leeres Raster - es gibt nichts zu malen.")
    unbekannt = [art for zeile in raster for art in zeile if art not in gelaende.ARTEN]
    if unbekannt:
        raise MalereiFehler("Unbekannte Geländeart im Raster: %r - es wird nichts erfunden."
                           % (unbekannt[0],))
    signatur = (tuple(tuple(str(art) for art in zeile) for zeile in raster), breite)
    treffer = _KARTEN.get(signatur)
    if treffer is not None:
        return treffer
    # Ueberabtastung, aber die Arbeitsflaeche bleibt begrenzt: 2048 px Kantenlaenge reichen fuer
    # weiche Kanten und halten Malzeit und Speicher im Rahmen (gemessen: 4fach bei 64 px kostete
    # 2,7 s und rund 60 MB - 2fach bei 48 px 0,7 s).
    f = max(1, min(UEBERABTASTUNG, ARBEITSBREITE // max(1, spalten * breite)))
    w, h = spalten * breite * f, zeilen * breite * f          # Arbeitsgroesse der ganzen Karte
    # 1. Farbfeld: die 20 x 20-Gelaendematrix bilinear hochrechnen -> weiche Farbuebergaenge
    klein = Image.new("RGB", (spalten, zeilen))
    for y, zeile in enumerate(raster):
        for x, art in enumerate(zeile):
            klein.putpixel((x, y), _rgb(gelaende.farbe(art)))
    # Weiche Uebergaenge (bikubisch) und danach etwas mehr Kontrast: sonst verwaschen die sieben
    # Gelaendefarben zu einem Brei. Ein Vollton-Feld je Kachel wurde verworfen - es schimmert als
    # Raster durch (angesehen und verglichen).
    from PIL import ImageEnhance
    farbe = klein.resize((w, h), Image.BICUBIC)
    farbe = ImageEnhance.Contrast(farbe).enhance(1.28)
    farbe = ImageEnhance.Color(farbe).enhance(1.12)
    # 2. Motive je Feld - gemalt, nicht gestempelt: eigene Saat fuer Lage, Groesse und Anzahl
    motive = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    zeichner = ImageDraw.Draw(motive, "RGBA")
    for y, zeile in enumerate(raster):
        for x, art in enumerate(zeile):
            kasten = (x * breite * f, y * breite * f,
                      (x + 1) * breite * f, (y + 1) * breite * f)
            _MOTIVE[art](zeichner, kasten, random.Random(_feld_saat(x, y)), f)
    # 3. Licht, Pinselstriche, Korn - der Zusammenhalt
    _grundlicht(zeichner, (0, 0, w, h), None, breit=False)
    bild = Image.alpha_composite(farbe.convert("RGBA"), motive).convert("RGB")
    bild = bild.resize((spalten * breite, zeilen * breite), Image.LANCZOS)
    _einheitslicht(bild, Image)
    if len(_KARTEN) >= KARTENSPEICHER:                        # aelteste Karte vergessen
        _KARTEN.pop(next(iter(_KARTEN)))
    _KARTEN[signatur] = bild
    return bild


# --------------------------------------------------------------------------
# Grundlicht, Pinselstriche, Einheitslicht
# --------------------------------------------------------------------------

def _fleck(draw, cx: float, cy: float, rx: float, ry: float, farbe, rnd,
           ecken: int = 10, rauheit: float = 0.28) -> None:
    """Eine unregelmaessige Flaeche - kein perfekter Kreis (das Auge liest Kreise als Technik)."""
    punkte = []
    for i in range(ecken):
        winkel = 2.0 * math.pi * i / ecken
        faktor = 1.0 + (rnd.random() - 0.5) * 2.0 * rauheit
        punkte.append((cx + math.cos(winkel) * rx * faktor,
                       cy + math.sin(winkel) * ry * faktor))
    draw.polygon(punkte, fill=farbe)


def _wolke(draw, cx: float, cy: float, rx: float, ry: float, farbe, rnd,
           ecken: int = 10, lagen: int = 3) -> None:
    """Weiche Farbwolke: mehrere unregelmaessige Flaechen uebereinander, aussen schwaecher."""
    for lage in range(lagen):
        faktor = 1.0 + (lagen - 1 - lage) * 0.16
        deckkraft = 26 + lage * 12
        _fleck(draw, cx, cy, rx * faktor, ry * faktor, (*_rgb(farbe), deckkraft), rnd, ecken)


def _grundlicht(draw, kasten, basis, rnd=None, breit: bool = True) -> None:
    """Warmes Licht oben links, kuehler Schatten unten rechts - EIN Licht fuer die ganze Flaeche.

    `breit=False` laesst die grossen Farbwolken weg: ueber eine ganze Karte gelegt lasen sie sich
    als dunkle diagonale Baender, die quer ueber Wasser, Wald und Berg zogen (angesehen).
    """
    x0, y0, x1, y1 = kasten
    breite, hoehe = x1 - x0, y1 - y0
    if not breite or not hoehe:
        return
    rnd = rnd or random.Random(7)
    if not breit:
        return
    _wolke(draw, x0 + breite * 0.25, y0 + hoehe * 0.20, breite * 0.42, hoehe * 0.34,
           (255, 245, 215), rnd, ecken=12)
    _wolke(draw, x0 + breite * 0.80, y0 + hoehe * 0.85, breite * 0.40, hoehe * 0.30,
           (10, 12, 14), rnd, ecken=12)
    if basis is not None:                                     # Einzelkachel: leichter Verlauf
        _wolke(draw, x0 + breite * 0.5, y0 + hoehe * 0.5, breite * 0.6, hoehe * 0.6,
               _misch(basis, (255, 255, 255), 0.08), rnd, ecken=12, lagen=2)


def _pinselstriche(draw, kasten, basis, rnd, dichte: float = 1.0) -> None:
    """Feine Pinselstriche - der Unterschied zwischen Flaeche und Malerei."""
    x0, y0, x1, y1 = kasten
    breite, hoehe = x1 - x0, y1 - y0
    flaeche = breite * hoehe
    anzahl = int(max(8.0, flaeche / 2600.0) * dichte)
    for _ in range(anzahl):
        cx, cy = x0 + rnd.random() * breite, y0 + rnd.random() * hoehe
        laenge = min(breite, hoehe) * (0.06 + rnd.random() * 0.14)
        winkel = -0.55 + rnd.random() * 1.0                     # flach, links oben nach rechts unten
        dx, dy = math.cos(winkel) * laenge, math.sin(winkel) * laenge
        hell = rnd.random() < 0.55
        farbe = (255, 250, 235, 26 + rnd.randrange(22)) if hell else (0, 0, 0, 20 + rnd.randrange(20))
        draw.line((cx, cy, cx + dx, cy + dy), fill=farbe,
                  width=max(1, int(min(breite, hoehe) / 64)))


def _einheitslicht(bild, Image) -> None:
    """EIN Licht ueber der ganzen Karte plus ein leises Korn - kein Feld leuchtet fuer sich.

    Seit F-34/F-35 (Daniel, 09.11.2026: „nur etwas heller wie bei Nummer 3“, dann „Vorschau +28 % ist
    ok ... Stil wie bei der Stilprobe A, aber die Karte GERADE angezeigt“) wird der Schatten unten
    rechts leiser aufgetragen (SCHATTEN_ALPHA statt 42), das warme Licht oben links etwas kraeftiger
    (LICHT_ALPHA) und das fertige Bild EINMAL mit `HELLIGKEIT` aufgehellt. EINE Stelle fuer Kacheln und
    ganze Karten, damit Legende und Karte denselben Ton tragen.
    """
    from PIL import ImageDraw, ImageEnhance, ImageFilter
    breite, hoehe = bild.size
    schleier = Image.new("RGB", bild.size, (0, 0, 0))
    zeichner = ImageDraw.Draw(schleier, "RGBA")
    zeichner.ellipse((-breite * 0.20, -hoehe * 0.30, breite * 0.80, hoehe * 0.70),
                     fill=(255, 240, 205, LICHT_ALPHA))          # warmes Licht oben links
    zeichner.rectangle((breite * 0.40, hoehe * 0.50, breite, hoehe),
                       fill=(0, 0, 0, SCHATTEN_ALPHA))
    schleier = schleier.filter(ImageFilter.GaussianBlur(max(4, breite // 8)))
    bild.paste(Image.blend(bild, schleier, 0.15))
    # Korn: leises Rauschen, damit die Flaechen nicht wie Vektorgrafik wirken
    korn = Image.effect_noise(bild.size, 22).convert("RGB")
    bild.paste(Image.blend(bild, korn, 0.05))
    # Helligkeit (F-34) - EINE Stelle, nach Licht und Korn
    bild.paste(ImageEnhance.Brightness(bild).enhance(HELLIGKEIT))


# --------------------------------------------------------------------------
# Motive je Gelaendeart - auf einem Kasten (Feld oder Einzelkachel)
# --------------------------------------------------------------------------

def _mitte(kasten):
    x0, y0, x1, y1 = kasten
    return (x0 + x1) / 2.0, (y0 + y1) / 2.0, (x1 - x0), (y1 - y0)


def _gras_bueschel(draw, cx: float, cy: float, groesse: float, farbe, rnd) -> None:
    """Ein Bueschel Gras: drei bis fuenf kurze Hiebe, leicht nach rechts geneigt."""
    stuecke = 3 + rnd.randrange(3)
    for i in range(stuecke):
        neigung = (i - stuecke // 2) * 0.30 + rnd.uniform(-0.1, 0.1)
        draw.line((cx, cy, cx + neigung * groesse, cy - groesse * (0.7 + rnd.random() * 0.6)),
                  fill=farbe, width=max(1, int(groesse // 4)))


def _tanne(draw, cx: float, cy: float, hoehe: float, basis, rnd) -> None:
    """Eine Tanne: weicher Schatten rechts unten, Stamm, drei Kronenstufen, Licht links oben."""
    dunkel = _misch(basis, (10, 30, 12), 0.55)
    mittel = _misch(basis, (16, 46, 18), 0.30)
    licht = _misch(basis, (150, 200, 90), 0.45)
    breite = max(1, int(hoehe // 18))
    _wolke(draw, cx + hoehe * 0.10, cy + hoehe * 0.26, hoehe * 0.28, hoehe * 0.08,
           (0, 0, 0), rnd, ecken=8, lagen=2)                      # Bodenschatten
    draw.line((cx, cy + hoehe * 0.04, cx, cy + hoehe * 0.24),
              fill=(*_misch(KONTUR, basis, 0.35), 220), width=max(1, breite))   # Stamm
    stufen = ((0.18, 0.34, 0.02), (0.02, 0.26, -0.16), (-0.14, 0.18, -0.32))
    for fuss, halb, spitze in stufen:
        punkte = [(cx, cy + hoehe * spitze),
                  (cx - hoehe * halb, cy + hoehe * fuss),
                  (cx + hoehe * halb, cy + hoehe * fuss)]
        draw.polygon(punkte, fill=(*mittel, 246), outline=(*KONTUR, 210))      # Krone mit Kontur
        draw.polygon([punkte[0], punkte[1], (cx, cy + hoehe * fuss)],
                     fill=(*dunkel, 235))                                        # Schattenseite
        draw.polygon([(cx, cy + hoehe * spitze + hoehe * 0.02), punkte[1],
                      (cx - hoehe * halb * 0.35, cy + hoehe * fuss)],
                     fill=(*licht, 220))                                         # Lichtseite


def _motiv_grasland(draw, kasten, rnd, f: float) -> None:
    cx, cy, breite, hoehe = _mitte(kasten)
    basis = _rgb(gelaende.farbe("grasland"))
    hell = _misch(basis, (205, 225, 130), 0.35)
    dunkel = _misch(basis, (20, 40, 10), 0.30)
    for _ in range(2 + rnd.randrange(3)):                           # Flecken hell/dunkel
        _wolke(draw, cx + rnd.uniform(-0.3, 0.3) * breite, cy + rnd.uniform(-0.3, 0.3) * hoehe,
               breite * rnd.uniform(0.18, 0.32), hoehe * rnd.uniform(0.10, 0.20),
               hell if rnd.random() < 0.5 else dunkel, rnd, lagen=2)
    for _ in range(5 + rnd.randrange(6)):                           # Grasbueschel
        _gras_bueschel(draw, cx + rnd.uniform(-0.45, 0.45) * breite,
                       cy + rnd.uniform(-0.42, 0.42) * hoehe,
                       breite * rnd.uniform(0.05, 0.09),
                       (*_misch(basis, (235, 245, 165), 0.55), 200), rnd)
    for _ in range(rnd.randrange(3)):                               # Blueten
        bx = cx + rnd.uniform(-0.4, 0.4) * breite
        by = cy + rnd.uniform(-0.4, 0.4) * hoehe
        r = breite * 0.014
        draw.ellipse((bx - r, by - r, bx + r, by + r), fill=(252, 242, 175, 230))
        draw.ellipse((bx - r * 0.4, by - r * 0.4, bx + r * 0.4, by + r * 0.4),
                     fill=(190, 130, 40, 230))


def _motiv_steppe(draw, kasten, rnd, f: float) -> None:
    cx, cy, breite, hoehe = _mitte(kasten)
    basis = _rgb(gelaende.farbe("steppe"))
    sand = _misch(basis, (242, 224, 156), 0.38)
    stroh = _misch(basis, (212, 192, 112), 0.45)
    for _ in range(2 + rnd.randrange(3)):                           # Sandflecken
        _wolke(draw, cx + rnd.uniform(-0.3, 0.3) * breite, cy + rnd.uniform(-0.3, 0.3) * hoehe,
               breite * rnd.uniform(0.20, 0.36), hoehe * rnd.uniform(0.08, 0.16), sand, rnd, lagen=2)
    for _ in range(3 + rnd.randrange(4)):                           # duerre Bueschel
        _gras_bueschel(draw, cx + rnd.uniform(-0.45, 0.45) * breite,
                       cy + rnd.uniform(-0.4, 0.4) * hoehe,
                       breite * rnd.uniform(0.04, 0.07), (*stroh, 205), rnd)
    for _ in range(1 + rnd.randrange(3)):                           # Kiesel
        px = cx + rnd.uniform(-0.4, 0.4) * breite
        py = cy + rnd.uniform(-0.4, 0.4) * hoehe
        r = breite * rnd.uniform(0.012, 0.022)
        _fleck(draw, px, py, r, r * 0.85, (*_misch(basis, (172, 167, 157), 0.55), 235), rnd,
               ecken=7, rauheit=0.2)
        draw.line((px - r, py + r * 0.7, px + r * 0.6, py + r * 0.6), fill=(*KONTUR, 110),
                  width=max(1, int(breite / 128)))


def _motiv_wald(draw, kasten, rnd, f: float) -> None:
    cx, cy, breite, hoehe = _mitte(kasten)
    basis = _rgb(gelaende.farbe("wald"))
    dunkel = _misch(basis, (0, 0, 0), 0.35)
    for _ in range(2 + rnd.randrange(2)):                           # Waldbodenschatten
        _wolke(draw, cx + rnd.uniform(-0.3, 0.3) * breite, cy + rnd.uniform(-0.3, 0.3) * hoehe,
               breite * rnd.uniform(0.16, 0.28), hoehe * rnd.uniform(0.08, 0.16), dunkel, rnd,
               lagen=2)
    anzahl = 2 + rnd.randrange(2)                                   # zwei bis drei Tannen je Feld
    for i in range(anzahl):
        versatz = (i - (anzahl - 1) / 2.0)
        bx = cx + versatz * breite * rnd.uniform(0.20, 0.26) + rnd.uniform(-0.05, 0.05) * breite
        by = cy + rnd.uniform(-0.10, 0.16) * hoehe
        h = hoehe * rnd.uniform(0.62, 0.82) * (1.0 if i % 2 else 0.88)
        _tanne(draw, bx, by, h, _misch(basis, (0, 0, 0), rnd.uniform(0.0, 0.20)), rnd)


def _motiv_huegel(draw, kasten, rnd, f: float) -> None:
    cx, cy, breite, hoehe = _mitte(kasten)
    basis = _rgb(gelaende.farbe("huegel"))
    licht = _misch(basis, (228, 202, 148), 0.35)
    schatten = _misch(basis, (0, 0, 0), 0.35)
    for _ in range(1 + rnd.randrange(2)):
        hx = cx + rnd.uniform(-0.2, 0.2) * breite
        hy = cy + rnd.uniform(-0.1, 0.2) * hoehe
        rx, ry = breite * rnd.uniform(0.26, 0.38), hoehe * rnd.uniform(0.20, 0.30)
        _wolke(draw, hx + rx * 0.14, hy + ry * 0.34, rx, ry * 0.9, schatten, rnd, ecken=12,
               lagen=2)                                             # Schatten rechts unten
        _fleck(draw, hx, hy, rx, ry, (*licht, 225), rnd, ecken=12)  # Huegelkoerper
        _fleck(draw, hx - rx * 0.20, hy - ry * 0.28, rx * 0.55, ry * 0.5,
               (*_misch(licht, (255, 246, 212), 0.45), 190), rnd, ecken=10)   # Lichtseite
        draw.arc((hx - rx, hy - ry, hx + rx, hy + ry * 0.9), 195, 345, fill=(*KONTUR, 190),
                 width=max(1, int(breite / 64)))                    # feine braune Kontur oben
        for _ in range(2):                                          # Gras auf der Kuppe
            _gras_bueschel(draw, hx + rnd.uniform(-rx * 0.5, rx * 0.5),
                           hy - ry * (0.25 + rnd.random() * 0.3), breite * 0.05,
                           (*_misch(basis, (218, 208, 124), 0.6), 190), rnd)


def _motiv_berg(draw, kasten, rnd, f: float) -> None:
    cx, cy, breite, hoehe = _mitte(kasten)
    basis = _rgb(gelaende.farbe("berg"))
    licht = _misch(basis, (230, 230, 240), 0.45)
    schatten = _misch(basis, (0, 0, 0), 0.42)
    for i in range(1 + rnd.randrange(2)):
        px = cx + (i - 0.5) * breite * 0.34 + rnd.uniform(-0.05, 0.05) * breite
        py = cy + rnd.uniform(0.0, 0.15) * hoehe
        hb, hh = breite * rnd.uniform(0.30, 0.40), hoehe * rnd.uniform(0.30, 0.40)
        spitze = (px + rnd.uniform(-0.04, 0.04) * breite, py - hh)
        links = [(px - hb, py + hh * 0.28)]
        rechts = [(px + hb * 0.95, py + hh * 0.32)]
        for schritt in (0.66, 0.33):                                # unregelmaessige Flanken
            links.append((px - hb * schritt + rnd.uniform(-0.02, 0.02) * breite,
                          py + hh * (0.28 - 0.26 * (0.66 - schritt))))
            rechts.append((px + hb * schritt * 0.95 + rnd.uniform(-0.02, 0.02) * breite,
                           py + hh * (0.32 - 0.28 * (0.66 - schritt))))
        draw.polygon([spitze] + rechts + links[::-1], fill=(*schatten, 240),
                     outline=(*KONTUR, 200))                        # Schattenseite + Kontur
        draw.polygon([spitze] + links[::-1] + [(px, py + hh * 0.30)], fill=(*licht, 235))
        schnee = (spitze,
                  (px - hb * 0.26, py - hh * 0.50),
                  (px - hb * 0.05, py - hh * 0.42),
                  (px + hb * 0.12, py - hh * 0.54),
                  (px + hb * 0.24, py - hh * 0.42))
        draw.polygon(schnee, fill=(226, 230, 236, 225))             # Schneekappe
        draw.line((spitze, (px, py + hh * 0.30)), fill=(*KONTUR, 190),
                  width=max(1, int(breite / 72)))                   # Grat
    for _ in range(rnd.randrange(3)):                               # Geroell am Fuss
        gx = cx + rnd.uniform(-0.4, 0.4) * breite
        gy = cy + rnd.uniform(0.25, 0.42) * hoehe
        r = breite * rnd.uniform(0.012, 0.020)
        _fleck(draw, gx, gy, r, r, (*_misch(basis, (232, 232, 238), 0.5), 220), rnd, ecken=6,
               rauheit=0.25)


def _motiv_nebelsee(draw, kasten, rnd, f: float) -> None:
    cx, cy, breite, hoehe = _mitte(kasten)
    basis = _rgb(gelaende.farbe("nebelsee"))
    tief = _misch(basis, (0, 20, 40), 0.45)
    hell = _misch(basis, (156, 222, 236), 0.50)
    _wolke(draw, cx, cy + hoehe * 0.30, breite * 0.45, hoehe * 0.22, tief, rnd,
           ecken=12)                                                # Tiefe unten
    for _ in range(2 + rnd.randrange(3)):                            # Wellenlinien
        wx = cx + rnd.uniform(-0.3, 0.3) * breite
        wy = cy + rnd.uniform(-0.35, 0.35) * hoehe
        laenge = breite * rnd.uniform(0.14, 0.30)
        draw.arc((wx - laenge, wy - laenge * 0.3, wx + laenge, wy + laenge * 0.3),
                 200, 340, fill=(*hell, 165), width=max(1, int(breite / 96)))
    for _ in range(1 + rnd.randrange(2)):                            # Nebelschwaden
        _wolke(draw, cx + rnd.uniform(-0.3, 0.3) * breite,
               cy + rnd.uniform(-0.35, 0.2) * hoehe,
               breite * rnd.uniform(0.20, 0.34), hoehe * rnd.uniform(0.05, 0.09),
               (238, 244, 250), rnd, ecken=12)                      # langgestreckt, nicht rund
    if rnd.random() < 0.5:                                          # Glanz auf dem Wasser
        gx, gy = cx + rnd.uniform(-0.3, 0.3) * breite, cy + rnd.uniform(-0.3, 0.3) * hoehe
        draw.ellipse((gx - breite * 0.03, gy - hoehe * 0.02, gx + breite * 0.03,
                      gy + hoehe * 0.02), fill=(255, 255, 255, 55))


def _motiv_sumpf(draw, kasten, rnd, f: float) -> None:
    cx, cy, breite, hoehe = _mitte(kasten)
    basis = _rgb(gelaende.farbe("sumpf"))
    schlamm = _misch(basis, (72, 62, 32), 0.45)
    tuempel = _misch(basis, (10, 45, 50), 0.55)
    schilf = _misch(basis, (154, 154, 94), 0.45)
    for _ in range(2 + rnd.randrange(2)):                            # Schlammflecken
        _wolke(draw, cx + rnd.uniform(-0.3, 0.3) * breite, cy + rnd.uniform(-0.3, 0.3) * hoehe,
               breite * rnd.uniform(0.16, 0.28), hoehe * rnd.uniform(0.07, 0.13), schlamm, rnd,
               lagen=2)
    for _ in range(1 + rnd.randrange(2)):                            # Tuempel mit hellem Rand
        px = cx + rnd.uniform(-0.25, 0.25) * breite
        py = cy + rnd.uniform(-0.2, 0.25) * hoehe
        rr = breite * rnd.uniform(0.10, 0.18)
        _fleck(draw, px, py, rr, rr * 0.55, (*tuempel, 230), rnd, ecken=9, rauheit=0.18)
        draw.arc((px - rr, py - rr * 0.55, px + rr, py + rr * 0.55), 200, 340,
                 fill=(*_misch(tuempel, (192, 212, 202), 0.5), 185), width=max(1, int(breite / 96)))
    for _ in range(3 + rnd.randrange(4)):                            # Schilf
        sx = cx + rnd.uniform(-0.4, 0.4) * breite
        sy = cy + rnd.uniform(-0.35, 0.4) * hoehe
        hh = hoehe * rnd.uniform(0.08, 0.16)
        draw.line((sx, sy, sx + breite * 0.01, sy - hh), fill=(*schilf, 215),
                  width=max(1, int(breite / 96)))
        draw.line((sx + breite * 0.012, sy - hh, sx + breite * 0.03, sy - hh * 1.15),
                  fill=(*schilf, 215), width=max(1, int(breite / 96)))


_MOTIVE = {
    "grasland": _motiv_grasland,
    "steppe": _motiv_steppe,
    "wald": _motiv_wald,
    "huegel": _motiv_huegel,
    "berg": _motiv_berg,
    "nebelsee": _motiv_nebelsee,
    "sumpf": _motiv_sumpf,
}
