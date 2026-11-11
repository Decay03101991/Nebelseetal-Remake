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
            # T1 (Daniels Befund 11.11.2026, Bogen B09/E1: "deren Hintergruende waren nicht zu sehen",
            # "Hintergrundbilder ganz ganz schwer im Hintergrund, kaum erkennbar"): der alte Weg deckte
            # die Flaeche nur bis 1,25x und fuellte den Rest mit dem flachen Ton (18,16,13). Bei einer
            # 538x222-Band auf 1142x1120 waren das gemessen 86 Prozent Flaeche ohne jedes Bild - Daniels
            # "dunkler, konturloser Verlauf". Neu sind es ZWEI Lagen aus DEMSELBEN Bild:
            #   1. Szene: das Motiv in voller Breite und unbeschnitten oben, scharf, am unteren Rand
            #      ueber einen langen Verlauf abgeblendet.
            #   2. Grund: dieselbe Szene, senkrecht gespiegelt, auf die Flaeche gestreckt, kraeftig
            #      weichgezeichnet und abgedunkelt - sie traegt Farbe und Licht des Motivs weiter und
            #      liest sich wie Nebel ueber dem Tal (daher kein fremder Fuellton mehr).
            # Die Abdunkelung der Gesamtflaeche kommt weiter aus der Datendatei (Daniel stellt sie dort).
            szene_b = int(ziel_b)                          # volle Breite
            szene_h = max(1, int(round(bild.height * (szene_b / float(bild.width)))))   # Seitenverhaeltnis
            szene = bild.resize((szene_b, szene_h), Image.LANCZOS)    # hochskaliert
            from PIL import ImageFilter                     # Filtermodul nur hier
            szene = szene.filter(ImageFilter.UnsharpMask(radius=1.4, percent=90, threshold=3))
            # Der Grund: das Bild gespiegelt (die Unterkante zeigt nach oben, also setzt sie die Szene
            # fort), auf die Zielflaeche gestreckt - die Streckung ist unsichtbar, weil stark
            # weichgezeichnet wird - und dunkler als die Szene.
            grund = szene.transpose(Image.Transpose.FLIP_TOP_BOTTOM).resize((ziel_b, ziel_h), Image.Resampling.BILINEAR)
            grund_weich = max(10.0, min(ziel_b, ziel_h) / 22.0)      # Radius an der Flaeche gemessen
            grund_weich += max(0.0, float(weichzeichnen_px or 0.0))  # Daniels Zugabe aus der Datendatei
            grund = grund.filter(ImageFilter.GaussianBlur(grund_weich))
            grund = Image.blend(grund.convert("RGB"),
                                Image.new("RGB", grund.size, (0, 0, 0)), 0.42)
            flaeche = grund                               # das Ergebnis beginnt mit dem Grund
            # Der untere Rand der Szene blendet ueber einen langen Weg in den Grund ueber - keine Kante
            # quer durch die Ansicht (Daniel 02.11.2026: "weil es optisch noch keine schoenen
            # uebergaenge sind"). 45 Prozent der Szenenhoehe, mindestens 120 Pixel.
            uebergang = max(120, int(szene_h * 0.45))                # Hoehe des Uebergangs
            uebergang = min(uebergang, szene_h)                     # nie laenger als die Szene
            maske = Image.new("L", (szene_b, szene_h), 255)          # ueberall deckend
            for y in range(uebergang):                               # die letzten Zeilen abblenden
                anteil = 1.0 - (y / float(uebergang))                # 1 oben, 0 unten
                zeile = szene_h - uebergang + y                      # Zeile von oben gezaehlt
                maske.paste(int(255 * anteil), (0, zeile, szene_b, zeile + 1))
            if szene_h > ziel_h:                                     # Szene hoeher als die Flaeche
                maske = maske.crop((0, 0, szene_b, ziel_h))          # dann unten abschneiden
                szene = szene.crop((0, 0, szene_b, ziel_h))          # Bild dazu passend
            flaeche.paste(szene.convert("RGB"), (0, 0), maske)        # Szene oben auf den Grund
            anteil = max(0.0, min(100.0, float(abdunkeln_prozent or 0.0)))           # Prozent
            if anteil > 0:                                  # nur wenn abgedunkelt wird
                schleier = Image.new("RGBA", flaeche.size, (0, 0, 0, int(255 * anteil / 100)))
                flaeche = Image.alpha_composite(flaeche.convert("RGBA"), schleier)   # Schleier darueber
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


def rahmen_kanten(quelle: str, breite: int, hoehe: int, rand: int = None) -> Dict[str, object]:  # Baut vier Randstreifen aus einem 9-Slice-Rahmenbild.
    """Vier Randstreifen (oben, unten, links, rechts) fuer einen Kasten beliebiger Groesse.

    Das Rahmenbild ist quadratisch (C2-Lieferung: 64 x 64, aussen geschnitzt, innen durchsichtig).
    Fuer ein Kaestchen von 400 px werden die vier KANTEN GEKACHELT - gedehnt wuerde das geschnitzte
    Muster langgezogen (dieselbe Lehre wie bei der Bildleiste am 02.11.2026). Die vier ECKEN sind
    seit T5 (11.11.2026) RECHTWINKLIG und aus den geraden Kantenstuecken gebaut: die Originalecken
    tragen einen Bogen von rund 30 px, der in das Kachelraster hineinlief (Daniels Befund C10).
    Rueckgabe: dict mit "oben", "unten", "links", "rechts" als RGBA-Bilder; ohne Pillow oder ohne
    Datei kommt ein leeres dict zurueck.
    """
    try:  # Beginnt den optionalen Pillow-Import.
        from PIL import Image  # Importiert das Bildmodul.
    except ImportError:  # Faengt fehlendes Pillow ab.
        return {}  # Ohne Pillow kein Rahmen.
    pfad = Path(str(quelle or ""))  # Pfad aus der Datendatei.
    if not pfad.is_absolute():  # Relative Angabe wie in allen assets-Pfaden.
        pfad = Path(PROJEKT_ROOT) / pfad  # Auf die Projektwurzel beziehen.
    if not pfad.exists():  # Datei fehlt.
        return {}  # Dann bleibt es beim nackten Kaestchen.
    bild = Image.open(pfad).convert("RGBA")  # Original mit Alphakanal.
    w, h = bild.size  # Masse des Rahmenbildes.
    rand = int(rand or max(4, min(w, h) // 4))  # Randbreite: Vorgabe ein Viertel der Kantenlaenge.
    rand = max(2, min(rand, min(w, h) // 2))  # Nie mehr als die halbe Kante.
    breite, hoehe = int(breite), int(hoehe)  # Zielmasse des Kastens.
    if breite < 2 * rand + 2 or hoehe < 2 * rand + 2:  # Zu klein fuer diesen Rand.
        return {}  # Dann kein Rahmen (der Aufrufer zeichnet ohne).
    kanten = {"oben": bild.crop((rand, 0, w - rand, rand)),  # obere Kante ohne Ecken.
              "unten": bild.crop((rand, h - rand, w - rand, h)),  # untere Kante ohne Ecken.
              "links": bild.crop((0, rand, rand, h - rand)),  # linke Kante ohne Ecken.
              "rechts": bild.crop((w - rand, rand, w, h - rand))}  # rechte Kante ohne Ecken.
    # T5 (Daniel 11.11.2026, Bogen C10: "die Gelaendeecken ueber den Rahmen ... das sieht wirklich
    # schlecht aus"; nachgemessen war es umgekehrt - die abgerundete Innenseite des Rahmens deckte
    # die Ecken der vier Eckkacheln): die vier ECKEN kommen jetzt aus den GERADEN Kantenstuecken.
    # Vorher wurden die Originalecken mit ihrem Bogen benutzt (oder gar nicht) - dadurch lief die
    # Rundung in das Kachelfeld hinein. Der Rahmen schliesst jetzt mit vier rechtwinkligen Ecken
    # ab, und das Fenster fuer das Raster ist ein sauberes Rechteck: Rahmen und Kachelraster
    # treffen sich auf derselben Linie.
    ecken = {"ol": kanten["oben"].crop((kanten["oben"].width - rand, 0,
                                        kanten["oben"].width, rand)),      # Ecke oben links
             "or": kanten["oben"].crop((0, 0, rand, rand)),                 # Ecke oben rechts
             "ul": kanten["unten"].crop((kanten["unten"].width - rand, 0,
                                         kanten["unten"].width, rand)),     # Ecke unten links
             "ur": kanten["unten"].crop((0, 0, rand, rand))}                # Ecke unten rechts

    def _kacheln(stueck, laenge: int, waagerecht: bool):  # Wiederholt ein Kantenstueck bis zur Laenge.
        from PIL import Image as _Image  # Bildmodul (im Import oben schon geladen).
        if waagerecht:  # Waagerechte Kante.
            flaeche = _Image.new("RGBA", (max(1, laenge), stueck.size[1]), (0, 0, 0, 0))  # leere Flaeche
        else:  # Senkrechte Kante.
            flaeche = _Image.new("RGBA", (stueck.size[0], max(1, laenge)), (0, 0, 0, 0))  # leere Flaeche
        x = y = 0  # Startpunkt der Wiederholung.
        while (x < laenge) if waagerecht else (y < laenge):  # Solange noch Platz ist.
            flaeche.paste(stueck, (x, 0) if waagerecht else (0, y))  # Stueck einsetzen.
            if waagerecht:  # Waagerecht weiterzaehlen.
                x += stueck.size[0]  # um die Stueckbreite.
            else:  # Senkrecht weiterzaehlen.
                y += stueck.size[1]  # um die Stueckhoehe.
        return flaeche  # Fertige Kante.

    from PIL import Image as _Bild  # Bildmodul fuer die Zusammensetzung.
    oben = _Bild.new("RGBA", (breite, rand), (0, 0, 0, 0))  # Leere obere Leiste.
    oben.paste(ecken["ol"], (0, 0))  # rechtwinklige Ecke links (T5).
    oben.paste(_kacheln(kanten["oben"], breite - 2 * rand, True), (rand, 0))  # Kante dazwischen.
    oben.paste(ecken["or"], (breite - rand, 0))  # rechtwinklige Ecke rechts (T5).
    unten = _Bild.new("RGBA", (breite, rand), (0, 0, 0, 0))  # Leere untere Leiste.
    unten.paste(ecken["ul"], (0, 0))  # rechtwinklige Ecke links (T5).
    unten.paste(_kacheln(kanten["unten"], breite - 2 * rand, True), (rand, 0))  # Kante dazwischen.
    unten.paste(ecken["ur"], (breite - rand, 0))  # rechtwinklige Ecke rechts (T5).
    links = _kacheln(kanten["links"], hoehe - 2 * rand, False)  # Linke Kante in Zielhoehe.
    rechts = _kacheln(kanten["rechts"], hoehe - 2 * rand, False)  # Rechte Kante in Zielhoehe.
    return {"oben": oben, "unten": unten, "links": links, "rechts": rechts, "rand": rand}  # Fertige Teile.


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
