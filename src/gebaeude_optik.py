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
BESCHRIFTUNGSBAND = 18  # Hoehe des Beschriftungsbandes im Kontaktblatt (Pixel).
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

def hintergrund_flaeche(gebaeude_id: str, breite: int, hoehe: int,
                        abdunkeln_prozent: float = 0.0,
                        weichzeichnen_px: float = 0.0) -> Optional[object]:
    """Ein Menuebild als FLACHEN-Hintergrund (B-6, Vorgabe Daniel 02.11.2026).

    Anders als `hintergrund()` wird hier nicht eingepasst, sondern GEDECKT: das Bild wird so weit
    vergroessert, dass die Flaeche vollstaendig gefuellt ist, und mittig beschnitten. So kommt
    "moeglichst viel vom Bild durch", ohne leere Raender oder Verzerrung.
    `abdunkeln_prozent` legt einen schwarzen Schleier darueber - der Wert ist eine Zahl in der
    Datendatei, damit Daniel die Lesbarkeit ohne Codeaenderung stellen kann.
    """
    try:                                                    # optionaler Pillow-Import
        from PIL import Image                               # Bildmodul
    except ImportError:                                     # kein Pillow
        return None                                         # dann None (Rueckfall greift)
    pfad = HINTERGRUENDE.get(gebaeude_id)                   # Hintergrundpfad der Kennung
    if pfad is None:                                        # unbekannte Kennung
        return None                                         # dann None
    dateipfad = Path(pfad)                                  # Pfad als Path
    if not dateipfad.is_file():                             # Datei fehlt
        return None                                         # dann None
    try:                                                    # Bildverarbeitung
        with Image.open(dateipfad) as bild:                 # Datei oeffnen
            bild = bild.convert("RGBA")                     # RGBA fuer den Schleier
            ziel_b, ziel_h = max(1, int(breite)), max(1, int(hoehe))     # Zielflaeche
            faktor = max(ziel_b / bild.width, ziel_h / bild.height)       # cover: groesserer Faktor
            # O-1 (03.11.2026, Befund Daniel "verzerrt und unscharf"): NICHT beliebig hochskalieren.
            # Die Menuebilder sind 538x222; auf 980x760 waeren das 3,42x - das Bild wird dabei weich
            # und wirkt auseinandergezogen. Grenze 1,25x: es bleibt scharf, der Rest der Flaeche wird
            # mit einem dunklen Grund gefuellt (derselbe Ton wie die Kaesten, damit es nicht auffaellt).
            HOECHSTENS = 1.25                               # harte Obergrenze der Vergroesserung
            if faktor > HOECHSTENS:                         # droht Unschaerfe
                faktor = HOECHSTENS                        # dann begrenzen
            gross = bild.resize((max(1, int(bild.width * faktor)),
                                 max(1, int(bild.height * faktor))), Image.LANCZOS)   # hochskaliert
            if gross.width < ziel_b or gross.height < ziel_h:                     # passt nicht mehr ganz
                leinwand = Image.new("RGBA", (ziel_b, ziel_h), (18, 16, 13, 255))  # dunkler Grund
                leinwand.paste(gross, (max(0, (ziel_b - gross.width) // 2),           # mittig
                                       max(0, (ziel_h - gross.height) // 2)))         # einsetzen
                flaeche = leinwand                                                    # die Flaeche
            else:                                                                     # deckt weiterhin
                links = max(0, (gross.width - ziel_b) // 2)     # mittig beschneiden
                oben = max(0, (gross.height - ziel_h) // 2)     # mittig beschneiden
                flaeche = gross.crop((links, oben, links + ziel_b, oben + ziel_h))    # die Flaeche
            # Weichzeichnen nimmt dem Bild die harten Kontraste: es bleibt erkennbar, draengt sich
            # aber nicht vor die Texte (Vorgabe Daniel 02.11.2026: "noch zu sehr blickfangend").
            weich = max(0.0, float(weichzeichnen_px or 0.0))                      # Radius in Pixeln
            if weich > 0:                                   # nur wenn eingestellt
                from PIL import ImageFilter                 # Filtermodul nur hier
                flaeche = flaeche.filter(ImageFilter.GaussianBlur(weich))         # weichzeichnen
            anteil = max(0.0, min(100.0, float(abdunkeln_prozent or 0.0)))           # Prozent
            if anteil > 0:                                  # nur wenn abgedunkelt wird
                schleier = Image.new("RGBA", flaeche.size, (0, 0, 0, int(255 * anteil / 100)))
                flaeche = Image.alpha_composite(flaeche, schleier)   # Schleier darueber
            return flaeche.convert("RGB")                   # fertige Flaeche
    except Exception:                                       # noqa: BLE001 - Bildfehler
        return None                                         # dann None


def kasten_bild(breite: int, hoehe: int, radius: int = 12,
                oben_alpha: int = 245, unten_alpha: int = 200,
                rand_alpha: int = 90, farbe=(22, 17, 12)) -> Optional[object]:
    """Ein weiches, abgerundetes Textfeld-Bild fuer den Bildhintergrund (B-6, 02.11.2026).

    Vorgabe Daniel: "Die texte muessen erkennbar bleiben also kleinere textbloecke die nicht
    transparent sind und der rest so transparent das moeglichst viel vom bild durchkommt" und
    danach "die texte und ihre textfelder ... weil es optisch noch keine schoenen uebergaenge sind".
    Deshalb kein hartes Rechteck, sondern: abgerundete Ecken, ein senkrechter Verlauf von fast
    deckend (oben) zu deutlich durchscheinend (unten) und ein feiner heller Rand. Gezeichnet wird
    vierfach vergroessert und dann verkleinert - so sind die Kanten glatt (Antialiasing).
    Rueckgabe: RGBA-Bild oder None (ohne Pillow, bei unsinnigen Massen).
    """
    try:                                                        # optionaler Pillow-Import
        from PIL import Image, ImageDraw                        # Bildmodul
    except ImportError:                                         # kein Pillow
        return None                                             # dann None (Rueckfall im Aufrufer)
    b, h = int(breite), int(hoehe)                              # Zielmasse
    if b < 8 or h < 8:                                          # unsinnige Masse
        return None                                             # dann None
    faktor = 4                                                  # vierfach zeichnen = glatte Kanten
    gross = Image.new("RGBA", (b * faktor, h * faktor), (0, 0, 0, 0))          # leere Flaeche
    zeichner = ImageDraw.Draw(gross)                            # Zeichenwerkzeug
    r = max(0, min(int(radius), min(b, h) // 2)) * faktor       # Radius, nie groesser als die Flaeche
    # Verlauf: je Zeile ein Streifen mit eigenem Alpha (oben deckender als unten).
    for y in range(h * faktor):
        anteil = y / float(max(1, h * faktor - 1))              # 0 oben, 1 unten
        alpha = int(round(oben_alpha + (unten_alpha - oben_alpha) * anteil))  # Alpha dieser Zeile
        zeichner.line([(0, y), (b * faktor, y)],
                      fill=(int(farbe[0]), int(farbe[1]), int(farbe[2]), alpha))   # warmes Dunkelbraun
    maske = Image.new("L", (b * faktor, h * faktor), 0)          # Maske: was zum Kasten gehoert
    ImageDraw.Draw(maske).rounded_rectangle((0, 0, b * faktor - 1, h * faktor - 1),
                                           radius=r, fill=255)  # abgerundetes Rechteck
    kasten = Image.new("RGBA", (b * faktor, h * faktor), (0, 0, 0, 0))         # Ergebnis
    kasten.paste(gross, (0, 0), maske)                          # nur innerhalb der Maske einsetzen
    rand = ImageDraw.Draw(kasten)                               # Rand zeichnen
    rand.rounded_rectangle((0, 0, b * faktor - 1, h * faktor - 1), radius=r,
                           outline=(196, 164, 110, int(rand_alpha)),
                           width=max(1, faktor // 2))          # feiner Goldrand
    return kasten.resize((b, h), Image.LANCZOS)                 # glatt verkleinert zurueckgeben


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


def vorschau_blatt(zielpfad: str, spalten: int = 5) -> Optional[str]:  # Erstellt ein Kontaktblatt aller Icons.
    """Kontaktblatt aller Menue-Icons mit Beschriftung - fuer die Sichtpruefung durch Daniel.

    Jede Zelle ist um ein Beschriftungsband HOEHER als das Icon; der Text steht IM Band, nicht
    ueber dem Bild. Vorher lag die Beschriftung auf dem unteren Iconrand und wurde in der letzten
    Zeile abgeschnitten (Befund der eigenen Sichtpruefung 02.11.2026).
    """
    try:  # Beginnt den optionalen Pillow-Import.
        from PIL import Image, ImageDraw  # Importiert Bild- und Zeichenfunktionen.
    except ImportError:  # Faengt fehlendes Pillow ab.
        return None  # Liefert None bei fehlendem Pillow.
    spalten = max(1, int(spalten))  # Stellt sicher, dass die Spaltenzahl positiv ist.
    band = BESCHRIFTUNGSBAND  # Hoehe des Beschriftungsbandes je Zelle in Pixeln.
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
    zeilen = -(-len(_IDS) // spalten)  # Berechnet die benoetigte Zeilenzahl.
    zelle_hoehe = icon_hoehe + band  # Zellhoehe = Icon plus Beschriftungsband.
    blatt = Image.new("RGBA", (spalten * icon_breite, zeilen * zelle_hoehe), (28, 34, 40, 255))  # Dunkle Leinwand.
    zeichner = ImageDraw.Draw(blatt)  # Erstellt einen Zeichenstift fuer das Blatt.
    for idx, bid in enumerate(_IDS):  # Durchlaeuft die ids mit Position.
        dateipfad = Path(ICONS.get(bid, ""))  # Holt den Icon-Pfad.
        if dateipfad.is_file():  # Prueft, ob die Datei existiert.
            with Image.open(dateipfad) as datei_bild:  # Oeffnet das Icon.
                bild = datei_bild.convert("RGBA")  # Konvertiert es in RGBA.
        else:  # Faengt fehlende Dateien ab.
            bild = Image.new("RGBA", (icon_breite, icon_hoehe), (0, 0, 0, 0))  # Erstellt eine leere Zelle.
        x = (idx % spalten) * icon_breite  # Berechnet die x-Position.
        y = (idx // spalten) * zelle_hoehe  # Berechnet die y-Position der Zelle.
        blatt.paste(bild, (x, y), bild)  # Fuegt das Icon oben in die Zelle ein.
        zeichner.text((x + 4, y + icon_hoehe + 3), bid, fill=(240, 240, 240, 255))  # Schreibt die id ins Band.
    blatt.save(zielpfad)  # Speichert das Kontaktblatt.
    return str(zielpfad)  # Liefert den Zielpfad als String zurueck.
