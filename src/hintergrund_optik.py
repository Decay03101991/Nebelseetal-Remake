"""Die neun Meshy-Bilder als Ansichts-Hintergrund - EINE Stelle fuer Pfad, Ausschnitt und Groesse.

Daniels Entscheidungen vom 12.11.2026 (Register 502, F-44 und F-45):

  * F-44: die sechs Voelker-Panoramen sind der Hintergrund der SIEDLUNGSANSICHT, die drei
    Elfen-Gebaeude (Bibliothek, Kriegerakademie, Stellmacher) gehoeren in die EINZELANSICHT
    des jeweiligen Gebaeudes.
  * F-45: die Bilder bleiben 1142 x 1120, gezeigt wird der MITTIGE 1:1-AUSSCHNITT und es wird
    NIE skaliert. Ist die Flaeche groesser als das Bild, steht das Bild mittig und der Rest
    wird mit der Fensterfarbe gefuellt.

Warum das hier steht und nicht in `main.py`: der Ausschnitt ist eine reine Rechnung
(versatz() -> (links, oben)) und wird von der Pruefdatei ohne Fenster nachgerechnet. Der
Bildaufbau selbst braucht Pillow; ohne Pillow gibt es None und die Ansicht bleibt wie vorher.
"""
import os
from typing import Optional, Tuple

# Die gelieferte Bildgroesse - Daniel, Register 469/502. Wer ein neues Bild baut, liest das hier.
BILD_BREITE = 1142
BILD_HOEHE = 1120

# Der Fuellton, wenn die Flaeche groesser ist als das Bild (Fensterfarbe des Spiels).
FUELLTON = "#17212B"

# Der Schleier (F-48, Register 507): 80 Prozent `#1a0a09` ueber dem Bild. A-10 rechnet ihn in das
# Bild der linken Spalte ein (Register 518).
SCHLEIER_FARBE = "#1a0a09"
SCHLEIER_DECKUNG = 80.0

ORDNER = os.path.join("assets", "hintergruende", "meshy_1zu1")

# Fraktionskennung -> Bilddatei der Siedlungsansicht. Die Kennungen sind die aus `data/voelker.json`
# (Achtung: Trolle, Ghule und Gnome stehen dort GROSS - ein Vergleich mit "trolle" trifft nie).
PANORAMEN = {
    "menschlich": "panorama_menschlich_1142x1120.jpg",
    "zwergisch": "panorama_zwergisch_1142x1120.jpg",
    "elfisch": "panorama_elfisch_1142x1120.jpg",
    "Trolle": "panorama_trolle_1142x1120.jpg",
    "Ghule": "panorama_ghule_1142x1120.jpg",
    "Gnome": "panorama_gnome_1142x1120.jpg",
}

# Gebaeudekennung -> Bilddatei der Einzelansicht (nur die drei Elfen-Gebaeude sind geliefert).
GEBAEUDE = {
    "bibliothek": "elfen_bibliothek_1142x1120.jpg",
    "kriegerakademie": "elfen_kriegerakademie_1142x1120.jpg",
    "stellmacher": "elfen_stellmacher_1142x1120.jpg",
}


def projektwurzel() -> str:
    """Der Projektordner (zwei Ebenen ueber dieser Datei: src/ -> Wurzel)."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _pfad(dateiname: str) -> str:
    """Voller Pfad einer gelieferten Bilddatei."""
    return os.path.join(projektwurzel(), ORDNER, dateiname)


def pfad_panorama(fraktion: str) -> Optional[str]:
    """Bilddatei der Siedlungsansicht fuer eine Fraktion - None, wenn keine gemalt ist.

    Gesucht wird zuerst genau (auch gross geschrieben), dann klein. Eine unbekannte oder leere
    Fraktion ergibt None: dann bleibt die Ansicht ohne Bild, statt ein fremdes Volk zu zeigen.
    """
    name = str(fraktion or "").strip()
    if not name:
        return None
    datei = PANORAMEN.get(name)
    if datei is None:
        for kennung, wert in PANORAMEN.items():
            if kennung.lower() == name.lower():
                datei = wert
                break
    if datei is None:
        return None
    voll = _pfad(datei)
    return voll if os.path.isfile(voll) else None


def pfad_gebaeude(gebaeude_id: str) -> Optional[str]:
    """Bilddatei der Einzelansicht fuer ein Gebaeude - None, wenn es keine gibt."""
    datei = GEBAEUDE.get(str(gebaeude_id or "").strip().lower())
    if datei is None:
        return None
    voll = _pfad(datei)
    return voll if os.path.isfile(voll) else None


def versatz(breite: int, hoehe: int) -> Tuple[int, int]:
    """Der mittige 1:1-Ausschnitt als (links, oben) im Bild - abgerundet, wie Claudes Teil A.

    Bei 1037 x 589 ergibt das (52, 265): 1142 - 1037 = 105, halbiert 52,5 -> 52; und
    1120 - 589 = 531, halbiert 265,5 -> 265. Ist die Flaeche groesser als das Bild, ist der
    Versatz 0 (dann wird das ganze Bild gezeigt und der Rest gefuellt).
    """
    links = max(0, (BILD_BREITE - int(breite)) // 2)
    oben = max(0, (BILD_HOEHE - int(hoehe)) // 2)
    return links, oben


def rgb(farbe: str) -> Tuple[int, int, int]:
    """'#1a0a09' -> (26, 10, 9). Eine unbekannte Angabe ergibt Schwarz (kein Absturz)."""
    text = str(farbe or "").strip().lstrip("#")
    if len(text) == 3:                                                    # Kurzform #abc
        text = "".join(zeichen * 2 for zeichen in text)
    if len(text) != 6:
        return (0, 0, 0)
    try:
        return (int(text[0:2], 16), int(text[2:4], 16), int(text[4:6], 16))
    except ValueError:
        return (0, 0, 0)


def _hex(dreier) -> str:
    """(26, 10, 9) -> '#1a0a09' (immer klein geschrieben, wie die Skin-Farben)."""
    r, g, b = (max(0, min(255, int(round(w)))) for w in dreier)
    return "#%02x%02x%02x" % (r, g, b)


def mittel_farbe(bild, rechteck=None) -> Tuple[int, int, int]:
    """Die mittlere Farbe eines Bildes oder eines Rechtecks darin (RGB, gerundet).

    Gemessen wird mit `ImageStat`, also ueber ALLE Pixel - kein Stichprobenverfahren. Ein fehlendes
    Bild ergibt Schwarz; ein Rechteck ausserhalb wird auf das Bild beschnitten.
    """
    if bild is None:
        return (0, 0, 0)
    teil = bild
    if rechteck is not None:
        x, y, breite, hoehe = (int(w) for w in list(rechteck)[:4])
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(bild.width, x + breite), min(bild.height, y + hoehe)
        if x1 <= x0 or y1 <= y0:                                          # leerer Ausschnitt
            return (0, 0, 0)
        teil = bild.crop((x0, y0, x1, y1))
    try:
        from PIL import ImageStat
        werte = ImageStat.Stat(teil.convert("RGB")).mean
    except Exception:                                                     # noqa: BLE001
        return (0, 0, 0)
    return (int(round(werte[0])), int(round(werte[1])), int(round(werte[2])))


def schleier_ton(bild, rechteck=None, farbe: str = SCHLEIER_FARBE,
                 deckung: float = SCHLEIER_DECKUNG) -> str:
    """Der Schleier-Ton als EINZELFARBE: `deckung` x `farbe` + Rest x Bildfarbe.

    Genau die Rechnung, die auch im Bild passiert (Claudes `0,8 x #1a0a09 + 0,2 x Bildfarbe`,
    Register 518) - damit koennen bedienbare Widgets (Knoepfe, Tabellen) denselben Ton tragen,
    obwohl Tk-Widgets keine Transparenz koennen. Bei 80 Prozent ueber einem weissen Bild ergibt
    das `#483b3a`, den Ton aus Register 507/518.
    """
    k = max(0.0, min(1.0, float(deckung) / 100.0))
    fr, fg, fb = rgb(farbe)
    br, bg, bb = mittel_farbe(bild, rechteck)
    return _hex((k * fr + (1.0 - k) * br, k * fg + (1.0 - k) * bg, k * fb + (1.0 - k) * bb))


def _bild_oeffnen(dateipfad: str):
    """Die Datei als RGBA-Bild - None ohne Pillow, ohne Datei oder bei kaputtem Bild."""
    if not dateipfad:
        return None
    try:
        from PIL import Image
    except ImportError:
        return None
    if not os.path.isfile(dateipfad):
        return None
    try:
        with Image.open(dateipfad) as roh:
            return roh.convert("RGBA")
    except (OSError, ValueError):
        return None


def _schneiden(bild, links: int, oben: int, breite: int, hoehe: int):
    """1:1 ausschneiden; passt die Flaeche nicht ins Bild, wird sie mittig eingesetzt und gefuellt."""
    from PIL import Image
    if breite <= bild.width and hoehe <= bild.height:                     # Flaeche passt: schneiden
        return bild.crop((links, oben, links + breite, oben + hoehe))
    flaeche = Image.new("RGBA", (breite, hoehe), FUELLTON)                 # Fuellton als Rest
    teil = bild.crop((0, 0, min(breite, bild.width), min(hoehe, bild.height)))
    flaeche.paste(teil, (max(0, (breite - bild.width) // 2),
                         max(0, (hoehe - bild.height) // 2)))
    return flaeche


def _schleier_auf(flaeche, rechtecke, farbe: str = SCHLEIER_FARBE,
                  deckung: float = SCHLEIER_DECKUNG):
    """Je Rechteck `deckung` Prozent `farbe` ueber das Bild legen (0,8 x Farbe + 0,2 x Bild).

    Die Rechtecke sind (x, y, Breite, Hoehe) in Zielkoordinaten; was ueber den Rand ragt, wird
    beschnitten statt zu werfen. Ohne Rechtecke kommt das Bild UNVERAENDERT zurueck.
    """
    from PIL import Image
    if not rechtecke:
        return flaeche
    k = max(0.0, min(1.0, float(deckung) / 100.0))
    voll_farbe = rgb(farbe) + (255,)
    for eintrag in rechtecke:
        try:
            x, y, breite, hoehe = (int(w) for w in list(eintrag)[:4])
        except (TypeError, ValueError):                                   # unbrauchbarer Eintrag
            continue
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(flaeche.width, x + breite), min(flaeche.height, y + hoehe)
        if x1 <= x0 or y1 <= y0:                                          # leerer Ausschnitt
            continue
        teil = flaeche.crop((x0, y0, x1, y1))
        voll = Image.new("RGBA", teil.size, voll_farbe)
        flaeche.paste(Image.blend(teil, voll, k), (x0, y0))
    return flaeche


def bereich(dateipfad: str, links: int, oben: int, breite: int, hoehe: int,
            weichzeichnen_px: float = 0.0, schleier=None,
            schleier_farbe: str = SCHLEIER_FARBE,
            schleier_deckung: float = SCHLEIER_DECKUNG,
            abdunkeln_prozent: float = 0.0):
    """Ein Ausschnitt an FREIER Stelle (links, oben) als RGBA-Bild von `breite` x `hoehe`.

    A-10 (Register 518): die linke Spalte beginnt am linken Rand des Inhalts, nicht in der Mitte
    des Panoramas - darum wird hier NICHT `versatz` benutzt, sondern der Aufrufer nennt die Stelle.
    Reihenfolge wie in `ausschnitt`: schneiden (nie skalieren), dann weichzeichnen, dann die
    Schleierfelder, zuletzt ein gleichmaessiges Abdunkeln. Ohne Pillow, ohne Datei oder bei
    unsinnigen Massen kommt None zurueck.
    """
    breite, hoehe = int(breite), int(hoehe)
    links, oben = max(0, int(links)), max(0, int(oben))
    if breite < 1 or hoehe < 1:
        return None
    bild = _bild_oeffnen(dateipfad)
    if bild is None:
        return None
    flaeche = _schneiden(bild, links, oben, breite, hoehe)
    if float(weichzeichnen_px or 0) > 0:                                  # Weichzeichnen auf Wunsch
        try:
            from PIL import ImageFilter
            flaeche = flaeche.filter(ImageFilter.GaussianBlur(float(weichzeichnen_px)))
        except Exception:                                                 # noqa: BLE001
            pass
    flaeche = _schleier_auf(flaeche, schleier, schleier_farbe, schleier_deckung)
    if float(abdunkeln_prozent or 0) > 0:                                 # Abdunkeln auf Wunsch
        from PIL import Image
        deckkraft = int(round(255 * min(100.0, float(abdunkeln_prozent)) / 100.0))
        dunkel = Image.new("RGBA", flaeche.size, (0, 0, 0, deckkraft))
        flaeche = Image.alpha_composite(flaeche, dunkel)
    return flaeche


def ausschnitt(dateipfad: str, breite: int, hoehe: int, abdunkeln_prozent: float = 0.0,
               weichzeichnen_px: float = 0.0, schleier=None,
               schleier_farbe: str = SCHLEIER_FARBE,
               schleier_deckung: float = SCHLEIER_DECKUNG):
    """Das Bild als Flaeche in Zielgroesse: mittig beschnitten, NIE skaliert (Pillow-Bild).

    Rueckgabe ist ein RGBA-Bild von genau `breite` x `hoehe`. Ohne Pillow, ohne Datei oder bei
    unsinnigen Massen kommt None zurueck - der Aufrufer laesst die Ansicht dann unveraendert.
    Die optionalen Schleierfelder (A-10) werden an `bereich` durchgereicht; ohne sie ist das
    Ergebnis dasselbe wie vor dem 12.11.2026.
    """
    breite, hoehe = int(breite), int(hoehe)
    if breite < 1 or hoehe < 1 or not dateipfad:
        return None
    links, oben = versatz(breite, hoehe)
    return bereich(dateipfad, links, oben, breite, hoehe,
                   weichzeichnen_px=weichzeichnen_px, schleier=schleier,
                   schleier_farbe=schleier_farbe, schleier_deckung=schleier_deckung,
                   abdunkeln_prozent=abdunkeln_prozent)
