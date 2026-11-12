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


def ausschnitt(dateipfad: str, breite: int, hoehe: int, abdunkeln_prozent: float = 0.0,
               weichzeichnen_px: float = 0.0):
    """Das Bild als Flaeche in Zielgroesse: mittig beschnitten, NIE skaliert (Pillow-Bild).

    Rueckgabe ist ein RGBA-Bild von genau `breite` x `hoehe`. Ohne Pillow, ohne Datei oder bei
    unsinnigen Massen kommt None zurueck - der Aufrufer laesst die Ansicht dann unveraendert.
    """
    breite, hoehe = int(breite), int(hoehe)
    if breite < 1 or hoehe < 1 or not dateipfad:
        return None
    try:
        from PIL import Image
    except ImportError:
        return None
    if not os.path.isfile(dateipfad):
        return None
    try:
        with Image.open(dateipfad) as roh:
            bild = roh.convert("RGBA")
    except (OSError, ValueError):
        return None
    links, oben = versatz(breite, hoehe)
    if breite <= bild.width and hoehe <= bild.height:            # Flaeche passt ins Bild: schneiden
        flaeche = bild.crop((links, oben, links + breite, oben + hoehe))
    else:                                                         # Flaeche groesser: 1:1 in die Mitte
        flaeche = Image.new("RGBA", (breite, hoehe), FUELLTON)
        teil = bild.crop((0, 0, min(breite, bild.width), min(hoehe, bild.height)))
        flaeche.paste(teil, (max(0, (breite - bild.width) // 2),
                             max(0, (hoehe - bild.height) // 2)))
    if float(weichzeichnen_px or 0) > 0:                          # Weichzeichnen nur auf Wunsch
        try:
            from PIL import ImageFilter
            flaeche = flaeche.filter(ImageFilter.GaussianBlur(float(weichzeichnen_px)))
        except Exception:                                         # noqa: BLE001 - Filter fehlt
            pass
    if float(abdunkeln_prozent or 0) > 0:                          # Schleier nur auf Wunsch
        deckkraft = int(round(255 * min(100.0, float(abdunkeln_prozent)) / 100.0))
        schleier = Image.new("RGBA", flaeche.size, (0, 0, 0, deckkraft))
        flaeche = Image.alpha_composite(flaeche, schleier)
    return flaeche
