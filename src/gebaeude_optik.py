# -*- coding: ascii -*-  # Kennzeichnet die Datei als ASCII-kodiert.
"""Gebaeude-Optik: Menue-Icons und Menue-Hintergruende der 20 Originalgebaeude.

Zugriffsschicht zwischen den gelieferten Bildern und der Oberflaeche - sie zeichnet NICHTS selbst.
Die Gebaeude-ids kommen AUS `data/buildings.json` (nie getippt), die Bilder liegen als Projektassets
unter `assets/icons/gebaeude/menue/` (256 x 256, RGBA, gerahmt) und `.../hintergrund/` (538 x 222,
RGBA). Beide Saetze stammen aus der Gebaeude-Design-Lieferung (Register 115/123).

Entstanden im Auftrag B4 (deepseek-v4-pro, 02.11.2026, `docs/auftraege/B4_paket_20261102.md`); der
Koordinator hat die Pfade auf die Projektassets und die Projektwurzel auf `spieldaten` umgestellt,
weil `archiv/` gitignored ist und in einer Auslieferung fehlt.

Pillow wird ERST in den Bildfunktionen importiert: ohne Pillow startet das Spiel weiter, die
Funktionen liefern dann `None` statt zu werfen.
"""
import json  # Liest JSON-Dateien.
from pathlib import Path  # Bietet Pfadobjekte.
from typing import Dict, List, Optional  # Bietet Typannotationen.

import spieldaten  # Projektwurzel ueber EINE Stelle - findet die Daten auch in der fertigen EXE.

PROJEKT_ROOT = spieldaten.projektwurzel()  # Projektverzeichnis (in der EXE der entpackte Ordner).
DATEN_PFAD = Path(PROJEKT_ROOT) / "data" / "buildings.json"  # Pfad zur Gebaeudedatendatei.
ICON_ORDNER = Path(PROJEKT_ROOT) / "assets" / "icons" / "gebaeude" / "menue"  # gerahmte Menue-Icons.
HINTERGRUND_ORDNER = Path(PROJEKT_ROOT) / "assets" / "icons" / "gebaeude" / "hintergrund"  # Menue-Hintergruende.

def _lese_gebaeude():  # Liest die Gebaeudeliste aus der Datendatei.
    with DATEN_PFAD.open("r", encoding="utf-8") as datei:  # Oeffnet die JSON-Datei im Lesemodus.
        daten = json.load(datei)  # Laedt die JSON-Daten.
    return daten.get("gebaeude", [])  # Liefert die Gebaeudeliste oder eine leere Liste.

_GEBAEUDE = _lese_gebaeude()  # Laedt die Gebaeudeliste.
_IDS = [eintrag["id"] for eintrag in _GEBAEUDE if "id" in eintrag]  # Extrahiert alle vorhandenen Gebaeude-ids.

ICONS: Dict[str, str] = {bid: str(ICON_ORDNER / f"{bid}.png") for bid in _IDS}  # Baut das Woerterbuch der Menue-Icon-Pfade.
HINTERGRUENDE: Dict[str, str] = {bid: str(HINTERGRUND_ORDNER / f"{bid}.png") for bid in _IDS}  # Baut das Woerterbuch der Menue-Hintergrund-Pfade.

def pfad_icon(gebaeude_id: str) -> Optional[str]:  # Liefert den Menue-Icon-Pfad.
    return ICONS.get(gebaeude_id)  # Gibt den Pfad oder None zurueck.

def pfad_hintergrund(gebaeude_id: str) -> Optional[str]:  # Liefert den Menue-Hintergrund-Pfad.
    return HINTERGRUENDE.get(gebaeude_id)  # Gibt den Pfad oder None zurueck.

def fehlende_gebaeude() -> List[str]:  # Liefert sortierte ids fehlender Icons.
    fehlend = []  # Startet eine leere Liste.
    for bid in _IDS:  # Durchlaeuft alle Gebaeude-ids.
        if not Path(ICONS[bid]).is_file():  # Prueft, ob die Icon-Datei fehlt.
            fehlend.append(bid)  # Fuegt die id der Fehlliste hinzu.
    return sorted(fehlend)  # Liefert die sortierte Fehlliste.

def kachel(gebaeude_id: str, breite: int, hoehe: int = None) -> Optional[object]:  # Erstellt eine zentrierte Icon-Kachel.
    try:  # Beginnt den optionalen Pillow-Import.
        from PIL import Image  # Importiert das Bildmodul.
    except ImportError:  # Faengt fehlendes Pillow ab.
        return None  # Liefert None bei fehlendem Pillow.
    pfad = ICONS.get(gebaeude_id)  # Holt den Icon-Pfad.
    if pfad is None:  # Prueft, ob die id unbekannt ist.
        return None  # Liefert None fuer unbekannte id.
    dateipfad = Path(pfad)  # Wandelt den Pfad in ein Path-Objekt.
    if not dateipfad.is_file():  # Prueft, ob die Datei existiert.
        return None  # Liefert None bei fehlender Datei.
    if hoehe is None:  # Setzt eine quadratische Zielhoehe.
        hoehe = breite  # Uebernimmt die Breite als Hoehe.
    try:  # Beginnt die Bildverarbeitung.
        with Image.open(dateipfad) as bild:  # Oeffnet das Icon.
            bild = bild.convert("RGBA")  # Wandelt es in RGBA.
            bild.thumbnail((breite, hoehe), Image.LANCZOS)  # Skaliert das Bild proportional.
            kachel_bild = Image.new("RGBA", (breite, hoehe), (0, 0, 0, 0))  # Erstellt eine transparente Leinwand.
            x = (breite - bild.width) // 2  # Berechnet die horizontale Zentrierung.
            y = (hoehe - bild.height) // 2  # Berechnet die vertikale Zentrierung.
            kachel_bild.paste(bild, (x, y), bild)  # Fuegt das skalierte Bild zentriert ein.
            return kachel_bild  # Liefert die fertige Kachel.
    except Exception:  # Faengt Bildfehler ab.
        return None  # Liefert None bei Verarbeitungsfehlern.

def hintergrund(gebaeude_id: str, breite: int, hoehe: int = None) -> Optional[object]:  # Skaliert einen Menue-Hintergrund.
    try:  # Beginnt den optionalen Pillow-Import.
        from PIL import Image  # Importiert das Bildmodul.
    except ImportError:  # Faengt fehlendes Pillow ab.
        return None  # Liefert None bei fehlendem Pillow.
    pfad = HINTERGRUENDE.get(gebaeude_id)  # Holt den Hintergrund-Pfad.
    if pfad is None:  # Prueft die id.
        return None  # Liefert None fuer unbekannte id.
    dateipfad = Path(pfad)  # Wandelt den Pfad.
    if not dateipfad.is_file():  # Prueft die Datei.
        return None  # Liefert None bei fehlender Datei.
    try:  # Beginnt die Bildverarbeitung.
        with Image.open(dateipfad) as bild:  # Oeffnet den Hintergrund.
            bild = bild.convert("RGB")  # Wandelt in RGB (Hintergrund deckt).
            if hoehe is None:  # Ohne Hoehe folgt sie dem Seitenverhaeltnis.
                hoehe = round(breite * bild.height / bild.width)  # Hoehe aus dem Originalverhaeltnis.
            else:  # Mit vorgegebener Hoehe wird EINGEPASST, nicht verzerrt.
                faktor = min(breite / bild.width, hoehe / bild.height)  # Kleinster gemeinsamer Faktor.
                breite, hoehe = max(1, int(round(bild.width * faktor))), max(1, int(round(bild.height * faktor)))  # Beide Masse aus dem Faktor.
            return bild.resize((int(breite), int(hoehe)), Image.LANCZOS)  # Gleichmaessig skaliert zurueckgeben.
    except Exception:  # Faengt Bildfehler ab.
        return None  # Liefert None bei Verarbeitungsfehlern.


def vorschau_blatt(zielpfad: str, spalten: int = 5) -> str:  # Erstellt ein Kontaktblatt aller Icons.
    try:  # Beginnt den optionalen Pillow-Import.
        from PIL import Image, ImageDraw  # Importiert Bild- und Zeichenfunktionen.
    except ImportError:  # Faengt fehlendes Pillow ab.
        return None  # Liefert None bei fehlendem Pillow.
    spalten = max(1, int(spalten))  # Stellt sicher, dass die Spaltenzahl positiv ist.
    zeilen = -(-len(_IDS) // spalten)  # Berechnet die benoetigte Zeilenzahl.
    erstes_bild = None  # Startet ohne Referenzbild.
    for bid in _IDS:  # Durchlaeuft die Gebaeude-ids.
        dateipfad = Path(ICONS.get(bid, ""))  # Holt den Icon-Pfad.
        if dateipfad.is_file():  # Prueft, ob die Datei existiert.
            with Image.open(dateipfad) as datei_bild:  # Oeffnet das erste vorhandene Icon.
                erstes_bild = datei_bild.convert("RGBA")  # Konvertiert es in RGBA.
            break  # Beendet die Suche.
    if erstes_bild is None:  # Prueft, ob ein Referenzbild gefunden wurde.
        return None  # Liefert None, wenn keine Icons vorhanden sind.
    icon_breite, icon_hoehe = erstes_bild.size  # Uebernimmt die tatsaechliche Icon-Groesse.
    erstes_bild.close()  # Schliesst das Referenzbild.
    blatt_breite = spalten * icon_breite  # Berechnet die Blattbreite.
    blatt_hoehe = zeilen * icon_hoehe  # Berechnet die Blatthoehe.
    blatt = Image.new("RGBA", (blatt_breite, blatt_hoehe), (255, 255, 255, 0))  # Erstellt eine transparente Leinwand.
    zeichner = ImageDraw.Draw(blatt)  # Erstellt einen Zeichenstift fuer das Blatt.
    for idx, bid in enumerate(_IDS):  # Durchlaeuft die ids mit Position.
        dateipfad = Path(ICONS.get(bid, ""))  # Holt den Icon-Pfad.
        if dateipfad.is_file():  # Prueft, ob die Datei existiert.
            with Image.open(dateipfad) as datei_bild:  # Oeffnet das Icon.
                bild = datei_bild.convert("RGBA")  # Konvertiert es in RGBA.
        else:  # Faengt fehlende Dateien ab.
            bild = Image.new("RGBA", (icon_breite, icon_hoehe), (0, 0, 0, 0))  # Erstellt eine leere Zelle.
        x = (idx % spalten) * icon_breite  # Berechnet die x-Position.
        y = (idx // spalten) * icon_hoehe  # Berechnet die y-Position.
        blatt.paste(bild, (x, y), bild)  # Fuegt das Icon ein.
        text = bid  # Nutzt die Gebaeude-id als Beschriftung.
        bbox = zeichner.textbbox((0, 0), text)  # Ermittelt die Textgroesse.
        text_hoehe = bbox[3] - bbox[1]  # Berechnet die Texthoehe.
        overlay = Image.new("RGBA", (icon_breite, text_hoehe), (0, 0, 0, 180))  # Erstellt eine halbtransparente Leiste.
        blatt.paste(overlay, (x, y + icon_hoehe - text_hoehe), overlay)  # Fuegt die Leiste unten ein.
        zeichner.text((x, y + icon_hoehe - text_hoehe), text, fill=(255, 255, 255, 255))  # Zeichnet den Text.
    blatt.save(zielpfad)  # Speichert das Kontaktblatt.
    return str(zielpfad)  # Liefert den Zielpfad als String zurueck.
