# -*- coding: utf-8 -*-
"""Baut den Symbolkatalog des Spiels als PDF.

Alle Icons kommen aus dem Projekt (assets/icons/...), alle Zahlen aus data/*.json.
Rohstoffe haben KEINE Originalgrafik - fuer sie zeichnet dieses Werkzeug ein Emblem
und schreibt das im PDF ausdruecklich dazu (nichts wird als Original ausgegeben).

Aufruf: python -X utf8 tools/icons_katalog_pdf.py
Ergebnis: docs/SYMBOLKATALOG_Nebelseetal_20261101.pdf
"""
import json
import math
import os
from datetime import date

from PIL import Image, ImageDraw, ImageFont

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DPI = 200
SEITE = (2339, 1654)            # A4 quer bei 200 dpi
RAND = 110
ZIEL = os.path.join(WURZEL, "docs", "SYMBOLKATALOG_Nebelseetal_20261101.pdf")

FARBE_HG = (13, 17, 23)
FARBE_HG2 = (23, 28, 37)
FARBE_PANEL = (22, 27, 34)
FARBE_RAND = (48, 56, 68)
FARBE_GOLD = (217, 164, 65)
FARBE_TEXT = (232, 234, 237)
FARBE_STILL = (154, 164, 178)
FARBE_AKZENT = (91, 148, 148)

SCHRIFT = "C:/Windows/Fonts/segoeui.ttf"
SCHRIFT_FETT = "C:/Windows/Fonts/segoeuib.ttf"
SCHRIFT_HALB = "C:/Windows/Fonts/seguisb.ttf"


def s(pfad, groesse):
    return ImageFont.truetype(pfad, groesse)


def lade(pfad):
    with open(os.path.join(WURZEL, pfad), "r", encoding="utf-8") as f:
        return json.load(f)


def hintergrund():
    """Dunkler Verlauf mit feinem Raster - die Buehne fuer alle Seiten."""
    bild = Image.new("RGB", SEITE, FARBE_HG)
    zeichner = ImageDraw.Draw(bild)
    for y in range(SEITE[1]):
        anteil = y / SEITE[1]
        r = int(FARBE_HG[0] + (FARBE_HG2[0] - FARBE_HG[0]) * anteil)
        g = int(FARBE_HG[1] + (FARBE_HG2[1] - FARBE_HG[1]) * anteil)
        b = int(FARBE_HG[2] + (FARBE_HG2[2] - FARBE_HG[2]) * anteil)
        zeichner.line([(0, y), (SEITE[0], y)], fill=(r, g, b))
    for x in range(0, SEITE[0], 80):
        zeichner.line([(x, 0), (x, SEITE[1])], fill=(20, 25, 33))
    for y in range(0, SEITE[1], 80):
        zeichner.line([(0, y), (SEITE[0], y)], fill=(20, 25, 33))
    return bild


def kopf(zeichner, titel, unter, seite, seiten):
    """Seitenkopf: Titel links, Zaehler rechts, goldene Linie darunter."""
    zeichner.text((RAND, 92), "NEBELSEETAL REMAKE", font=s(SCHRIFT_HALB, 26), fill=FARBE_GOLD)
    zeichner.text((RAND, 126), titel, font=s(SCHRIFT_FETT, 62), fill=FARBE_TEXT)
    if unter:
        zeichner.text((RAND, 208), unter, font=s(SCHRIFT, 28), fill=FARBE_STILL)
    zeichner.text((SEITE[0] - RAND, 100), "%d / %d" % (seite, seiten),
                  font=s(SCHRIFT, 26), fill=FARBE_STILL, anchor="ra")
    zeichner.line([(RAND, 268), (SEITE[0] - RAND, 268)], fill=FARBE_GOLD, width=3)
    zeichner.text((RAND, SEITE[1] - 66),
                  "Symbolkatalog - Stand %s - Zahlen aus data/*.json, Bilder aus assets/icons/"
                  % date.today().strftime("%d.%m.%Y"),
                  font=s(SCHRIFT, 23), fill=(168, 176, 188))


def karte(zeichner, kasten, titel, zeilen, farbe=FARBE_AKZENT):
    """Eine Karte mit farbigem Rand links, Titel und bis zu drei Zeilen."""
    x0, y0, x1, y1 = kasten
    zeichner.rounded_rectangle(kasten, radius=18, fill=FARBE_PANEL, outline=FARBE_RAND, width=2)
    zeichner.rounded_rectangle([x0, y0, x0 + 7, y1], radius=3, fill=farbe)
    zeichner.text((x0 + 26, y0 + 16), titel, font=s(SCHRIFT_HALB, 25), fill=FARBE_TEXT)
    y = y0 + 52
    for z in zeilen:
        if y > y1 - 18:
            break
        zeichner.text((x0 + 26, y), z, font=s(SCHRIFT, 20), fill=FARBE_STILL)
        y += 27


def hintergrund_normalisieren(pfad, schwelle=0.55, saettigung_max=0.12):
    """Hintergrund eines Motivs auf reines Weiss ziehen (Flutfuellung von den Raendern).

    Motiv 3, 6 und 7 tragen ein hellgraues Schachbrett als Grund - auf einer weissen
    Katalogtafel sieht das wie ein Fehler aus. Gefuellt wird nur, was von aussen
    erreichbar und hell ist; helle Stellen INNERHALB des Gebaeudes bleiben unberuehrt.
    """
    from collections import deque
    voll = os.path.join(WURZEL, pfad)
    if not os.path.exists(voll):
        return None
    bild = Image.open(voll).convert("RGBA")
    pixel = bild.load()
    breite, hoehe = bild.size

    def hell_und_grau(x, y):
        r, g, b, a = pixel[x, y]
        hoechster, tiefster = max(r, g, b), min(r, g, b)
        if hoechster == 0:
            return False
        return hoechster / 255.0 >= schwelle and (hoechster - tiefster) / hoechster <= saettigung_max

    gesehen = set()
    schlange = deque()
    for x in range(breite):
        for y in (0, hoehe - 1):
            schlange.append((x, y))
    for y in range(hoehe):
        for x in (0, breite - 1):
            schlange.append((x, y))
    while schlange:
        x, y = schlange.popleft()
        if (x, y) in gesehen or not (0 <= x < breite and 0 <= y < hoehe):
            continue
        if not hell_und_grau(x, y):
            continue
        gesehen.add((x, y))
        pixel[x, y] = (255, 255, 255, 255)
        schlange.append((x + 1, y))
        schlange.append((x - 1, y))
        schlange.append((x, y + 1))
        schlange.append((x, y - 1))
    return bild


def freistellen(pfad, weich_ab=0.86, voll_weg=0.95):
    """Weissen Hintergrund der Handbuchmotive weich entfernen und den Leerrand abschneiden.

    Die Motive sind JPEG-Ausschnitte mit weissem Grund; ein harter Zauberstab-Schnitt
    hinterlaesst einen hellen Saum. Deshalb bekommt jeder Randpixel eine Zwischen-
    Deckkraft: ab `weich_ab` wird er durchsichtig, ab `voll_weg` ganz.
    """
    voll = os.path.join(WURZEL, pfad)
    if not os.path.exists(voll):
        return None
    bild = Image.open(voll).convert("RGBA")
    pixel = bild.load()
    for y in range(bild.height):
        for x in range(bild.width):
            r, g, b, a = pixel[x, y]
            helligkeit = min(r, g, b) / 255.0
            if helligkeit >= voll_weg:
                pixel[x, y] = (r, g, b, 0)
            elif helligkeit > weich_ab:
                anteil = (voll_weg - helligkeit) / (voll_weg - weich_ab)
                pixel[x, y] = (int(r * 0.96), int(g * 0.96), int(b * 0.96), int(255 * anteil))
    kasten = bild.getbbox()
    if kasten:
        bild = bild.crop(kasten)
    return bild


def bild_einsetzen(bild, quelle, kasten, abstand=6):
    """Ein bereits geladenes RGBA-Bild in einen Kasten setzen, ohne Verzerrung."""
    if quelle is None:
        return False
    breite, hoehe = kasten[2] - kasten[0], kasten[3] - kasten[1]
    faktor = min((breite - 2 * abstand) / quelle.width, (hoehe - 2 * abstand) / quelle.height)
    neu = (max(1, int(quelle.width * faktor)), max(1, int(quelle.height * faktor)))
    stueck = quelle.resize(neu, Image.LANCZOS)
    x = kasten[0] + (breite - neu[0]) // 2
    y = kasten[1] + (hoehe - neu[1]) // 2
    bild.paste(stueck, (x, y), stueck)
    return True


def kuerzen(zeichner, text, schrift, breite):
    """Text auf eine Breite kuerzen, damit er nicht aus der Karte laeuft."""
    if zeichner.textlength(text, font=schrift) <= breite:
        return text
    while text and zeichner.textlength(text + "...", font=schrift) > breite:
        text = text[:-1]
    return text.rstrip() + "..."


def icon_einsetzen(bild, pfad, kasten, rand_abstand=8):
    """Ein Icon mit Alpha weich in einen Kasten setzen, ohne Verzerrung."""
    voll = os.path.join(WURZEL, pfad)
    if not os.path.exists(voll):
        return False
    symbol = Image.open(voll).convert("RGBA")
    breite, hoehe = kasten[2] - kasten[0], kasten[3] - kasten[1]
    faktor = min((breite - 2 * rand_abstand) / symbol.width,
                 (hoehe - 2 * rand_abstand) / symbol.height)
    neu = (max(1, int(symbol.width * faktor)), max(1, int(symbol.height * faktor)))
    symbol = symbol.resize(neu, Image.LANCZOS)
    x = kasten[0] + (breite - neu[0]) // 2
    y = kasten[1] + (hoehe - neu[1]) // 2
    bild.paste(symbol, (x, y), symbol)
    return True


# --------------------------------------------------------------- Rohstoff-Embleme
# Die neun Rohstoffe haben im Projekt KEINE Grafik. Hier wird je Rohstoff ein eigenes
# Emblem aus Grundformen gezeichnet; das PDF sagt dazu, dass es keine Originalgrafik ist.

ROHSTOFF_FARBEN = {
    "holz": (124, 82, 45), "stein": (120, 122, 126), "metall": (150, 158, 170),
    "gold": (206, 160, 60), "mana": (86, 122, 214), "nahrung": (176, 150, 70),
    "wolle": (214, 208, 196), "leder": (150, 96, 62), "pferde": (110, 74, 52),
}


def emblem(rohstoff_id, groesse=190):
    """Zeichnet ein Emblem je Rohstoff: farbige Scheibe plus ein einfaches Zeichen."""
    bild = Image.new("RGBA", (groesse, groesse), (0, 0, 0, 0))
    z = ImageDraw.Draw(bild)
    farbe = ROHSTOFF_FARBEN.get(rohstoff_id, (120, 120, 120))
    dunkel = tuple(max(0, int(c * 0.55)) for c in farbe)
    hell = tuple(min(255, int(c * 1.25)) for c in farbe)
    z.ellipse([4, 4, groesse - 4, groesse - 4], fill=dunkel, outline=hell, width=4)
    z.ellipse([18, 18, groesse - 18, groesse - 18], outline=(0, 0, 0, 60), width=2)
    m = groesse / 2.0
    k = groesse / 190.0
    if rohstoff_id == "holz":
        for i, dy in enumerate((-22, 4, 30)):
            z.rounded_rectangle([m - 52 * k, m + dy * k - 12 * k, m + 52 * k, m + dy * k + 12 * k],
                                radius=10, fill=farbe, outline=hell, width=2)
            z.ellipse([m + 40 * k, m + dy * k - 12 * k, m + 64 * k, m + dy * k + 12 * k],
                      fill=dunkel, outline=hell, width=2)
    elif rohstoff_id == "stein":
        z.polygon([(m - 52 * k, m + 30 * k), (m - 20 * k, m - 40 * k), (m + 22 * k, m - 34 * k),
                   (m + 54 * k, m + 6 * k), (m + 28 * k, m + 40 * k), (m - 28 * k, m + 44 * k)],
                  fill=farbe, outline=hell)
    elif rohstoff_id == "metall":
        z.polygon([(m - 58 * k, m + 26 * k), (m - 40 * k, m - 12 * k), (m + 40 * k, m - 12 * k),
                   (m + 58 * k, m + 26 * k)], fill=farbe, outline=hell)
        z.polygon([(m - 34 * k, m - 12 * k), (m - 20 * k, m - 40 * k), (m + 20 * k, m - 40 * k),
                   (m + 34 * k, m - 12 * k)], fill=hell, outline=hell)
    elif rohstoff_id == "gold":
        z.ellipse([m - 46 * k, m - 46 * k, m + 46 * k, m + 46 * k], fill=farbe, outline=hell, width=4)
        z.ellipse([m - 26 * k, m - 26 * k, m + 26 * k, m + 26 * k], outline=dunkel, width=5)
        z.text((m, m), "G", font=s(SCHRIFT_FETT, int(34 * k)), fill=dunkel, anchor="mm")
    elif rohstoff_id == "mana":
        z.polygon([(m, m - 56 * k), (m + 40 * k, m + 12 * k), (m, m + 52 * k), (m - 40 * k, m + 12 * k)],
                  fill=farbe, outline=hell)
        z.ellipse([m - 14 * k, m - 6 * k, m + 4 * k, m + 14 * k], fill=(255, 255, 255, 120))
    elif rohstoff_id == "nahrung":
        for dx, dy in ((-26, 8), (0, -18), (26, 8)):
            z.ellipse([m + dx * k - 20 * k, m + dy * k - 26 * k, m + dx * k + 20 * k, m + dy * k + 26 * k],
                      fill=farbe, outline=hell, width=2)
    elif rohstoff_id == "wolle":
        for dx, dy in ((-28, -8), (14, -14), (0, 20)):
            z.ellipse([m + dx * k - 26 * k, m + dy * k - 26 * k, m + dx * k + 26 * k, m + dy * k + 26 * k],
                      fill=farbe, outline=hell, width=2)
    elif rohstoff_id == "leder":
        z.rounded_rectangle([m - 52 * k, m - 38 * k, m + 52 * k, m + 38 * k], radius=16,
                            fill=farbe, outline=hell, width=3)
        for i in range(-3, 4):
            z.ellipse([m + i * 14 * k - 3 * k, m - 4 * k, m + i * 14 * k + 3 * k, m + 2 * k],
                      fill=dunkel)
    elif rohstoff_id == "pferde":
        z.rounded_rectangle([m - 44 * k, m - 8 * k, m + 30 * k, m + 22 * k], radius=12,
                            fill=farbe, outline=hell, width=2)
        z.polygon([(m + 20 * k, m - 8 * k), (m + 34 * k, m - 44 * k), (m + 52 * k, m - 40 * k),
                   (m + 46 * k, m - 6 * k)], fill=farbe, outline=hell)
        for dx in (-36, -20, 6, 22):
            z.line([(m + dx * k, m + 20 * k), (m + dx * k, m + 46 * k)], fill=hell, width=6)
    return bild


# --------------------------------------------------------------- Seiten

def seite_titel(zahlen):
    bild = hintergrund()
    z = ImageDraw.Draw(bild)
    z.text((RAND, 250), "NEBELSEETAL REMAKE", font=s(SCHRIFT_HALB, 40), fill=FARBE_GOLD)
    z.text((RAND, 300), "SYMBOLKATALOG", font=s(SCHRIFT_FETT, 150), fill=FARBE_TEXT)
    z.text((RAND, 470), "Einheiten, Waren, Rohstoffe und Gebäude in Bild und Zahl",
           font=s(SCHRIFT, 40), fill=FARBE_STILL)
    z.line([(RAND, 560), (RAND + 900, 560)], fill=FARBE_GOLD, width=4)
    symbol = os.path.join(WURZEL, "assets", "icons", "nebelseetal_symbol.png")
    if os.path.exists(symbol):
        icon_einsetzen(bild, "assets/icons/nebelseetal_symbol.png",
                       (SEITE[0] - 780, 200, SEITE[0] - 140, 840), rand_abstand=0)
    y = 650
    for wert, bezeichnung in zahlen:
        z.text((RAND, y), wert, font=s(SCHRIFT_FETT, 72), fill=FARBE_GOLD)
        z.text((RAND + 190, y + 26), bezeichnung, font=s(SCHRIFT, 32), fill=FARBE_TEXT)
        y += 100
    z.text((RAND, SEITE[1] - 300),
           "Alle Bilder stammen aus dem Projekt. Die Rohstoffe haben keine Originalgrafik -",
           font=s(SCHRIFT, 24), fill=FARBE_STILL)
    z.text((RAND, SEITE[1] - 262),
           "für sie zeichnet tools/icons_katalog_pdf.py ein Emblem; das ist keine Originalvorlage.",
           font=s(SCHRIFT, 24), fill=FARBE_STILL)
    z.text((RAND, SEITE[1] - 200), "Stand %s" % date.today().strftime("%d.%m.%Y"),
           font=s(SCHRIFT, 24), fill=(110, 118, 130))
    return bild


def seite_rohstoffe(rohstoffe, gebaeude, seite, seiten):
    bild = hintergrund()
    z = ImageDraw.Draw(bild)
    kopf(z, "Rohstoffe", "neun Rohstoffe - Ertrag je Stunde auf dem besten Gelände", seite, seiten)
    spalten, zeilen = 3, 3
    flaeche_x = SEITE[0] - 2 * RAND
    flaeche_y = SEITE[1] - 268 - 120
    bw = flaeche_x // spalten
    bh = flaeche_y // zeilen
    for i, roh in enumerate(rohstoffe):
        sx, sy = i % spalten, i // spalten
        x0 = RAND + sx * bw + 6
        y0 = 300 + sy * bh + 6
        x1 = x0 + bw - 12
        y1 = y0 + bh - 14
        z.rounded_rectangle([x0, y0, x1, y1], radius=20, fill=FARBE_PANEL,
                            outline=FARBE_RAND, width=2)
        em = emblem(roh["id"], 230)
        bild.paste(em, (x0 + 24, y0 + (y1 - y0 - 230) // 2), em)
        ertrag = roh.get("ertrag_pro_stunde") or {}
        text = ", ".join("%s %s/h" % (k, v) for k, v in ertrag.items())
        erzeuger = ", ".join(roh.get("erzeugendes_gebaeude") or []) or "-"
        z.text((x0 + 286, y0 + 26), roh["name"], font=s(SCHRIFT_FETT, 40), fill=FARBE_TEXT)
        erzeuger_zeile = kuerzen(z, "Gebäude: " + erzeuger, s(SCHRIFT, 22), x1 - x0 - 306)
        z.text((x0 + 286, y0 + 84), erzeuger_zeile, font=s(SCHRIFT, 22), fill=FARBE_GOLD)
        y = y0 + 122
        for stueck in _umbrechen(text, 46):
            z.text((x0 + 286, y), stueck, font=s(SCHRIFT, 22), fill=FARBE_STILL)
            y += 28
        z.text((x0 + 286, y1 - 42), "Emblem: eigene Zeichnung, keine Originalgrafik",
               font=s(SCHRIFT, 18), fill=(110, 118, 130))
    return bild


def _umbrechen(text, breite):
    """Bricht einen Text an Wortgrenzen - fuer die Karten in den Rastern."""
    woerter, zeilen, aktuell = text.split(), [], ""
    for w in woerter:
        if len(aktuell) + len(w) + 1 <= breite:
            aktuell = (aktuell + " " + w).strip()
        else:
            zeilen.append(aktuell)
            aktuell = w
    if aktuell:
        zeilen.append(aktuell)
    return zeilen


def raster_seite(titel, unter, eintraege, seite, seiten, spalten=6, karten_hoehe=None):
    """Ein Raster aus Karten: Icon gross, Name, Kategorie, zwei Kennzahlen."""
    bild = hintergrund()
    z = ImageDraw.Draw(bild)
    kopf(z, titel, unter, seite, seiten)
    flaeche_x = SEITE[0] - 2 * RAND
    bw = flaeche_x // spalten
    bh = karten_hoehe or 476
    for i, e in enumerate(eintraege):
        sx, sy = i % spalten, i // spalten
        x0 = RAND + sx * bw + 7
        y0 = 300 + sy * bh + 7
        x1 = x0 + bw - 14
        y1 = y0 + bh - 16
        z.rounded_rectangle([x0, y0, x1, y1], radius=18, fill=FARBE_PANEL,
                            outline=FARBE_RAND, width=2)
        icon_einsetzen(bild, e["icon"], (x0 + 10, y0 + 10, x1 - 10, y0 + 226), rand_abstand=4)
        innen = x1 - x0 - 40
        z.text((x0 + 20, y0 + 238), kuerzen(z, e["name"], s(SCHRIFT_HALB, 26), innen),
               font=s(SCHRIFT_HALB, 26), fill=FARBE_TEXT)
        z.text((x0 + 20, y0 + 276), kuerzen(z, e["zeile1"], s(SCHRIFT, 19), innen),
               font=s(SCHRIFT, 19), fill=FARBE_GOLD)
        y = y0 + 312
        for zeile in e["zeilen"][:4]:
            z.text((x0 + 20, y), kuerzen(z, zeile, s(SCHRIFT, 18), innen),
                   font=s(SCHRIFT, 18), fill=FARBE_STILL)
            y += 24
        if e.get("fuss"):
            z.text((x0 + 20, y1 - 38), kuerzen(z, e["fuss"], s(SCHRIFT, 16), innen),
                   font=s(SCHRIFT, 16), fill=(120, 128, 140))
    return bild


def seite_motive(motive, gebaeude_namen, seite, seiten):
    """Die acht Original-Gebaeudemotive gross - die epischste Seite des Hefts."""
    bild = hintergrund()
    z = ImageDraw.Draw(bild)
    kopf(z, "Gebäudemotive", "acht Originalmotive aus dem Handbuch 2009, Seite 1", seite, seiten)
    spalten, zeilen = 4, 2
    flaeche_x = SEITE[0] - 2 * RAND
    flaeche_y = SEITE[1] - 268 - 120
    bw, bh = flaeche_x // spalten, flaeche_y // zeilen
    for i, m in enumerate(motive):
        sx, sy = i % spalten, i // spalten
        x0 = RAND + sx * bw + 10
        y0 = 300 + sy * bh + 10
        x1 = x0 + bw - 20
        y1 = y0 + bh - 24
        z.rounded_rectangle([x0, y0, x1, y1], radius=22, fill=FARBE_PANEL,
                            outline=FARBE_GOLD if m.get("eingebaut") else FARBE_RAND, width=3)
        platte = [x0 + 16, y0 + 16, x1 - 16, y0 + 326]
        z.rounded_rectangle(platte, radius=14, fill=(250, 248, 242))
        motiv = hintergrund_normalisieren(m["datei"])
        if motiv is not None:
            grenze = int(motiv.width * 2.5)
            kasten = (platte[0], platte[1], platte[2], platte[1] + grenze)
            zentriert = (kasten[0], platte[1] + (platte[3] - platte[1] - grenze) // 2,
                         kasten[2], platte[1] + (platte[3] - platte[1] + grenze) // 2)
            bild_einsetzen(bild, motiv, zentriert, abstand=6)
        else:
            icon_einsetzen(bild, m["datei"], tuple(platte), rand_abstand=10)
        z.rounded_rectangle(platte, radius=14, outline=(220, 204, 168), width=2)
        name = gebaeude_namen.get(m.get("gebaeude") or "", "Zuordnung offen")
        z.text((x0 + 24, y0 + 334), "Motiv %d" % m["motiv"], font=s(SCHRIFT_FETT, 34), fill=FARBE_GOLD)
        z.text((x0 + 24, y0 + 378), kuerzen(z, name, s(SCHRIFT_HALB, 26), x1 - x0 - 48),
               font=s(SCHRIFT_HALB, 26), fill=FARBE_TEXT)
        y = y0 + 416
        for stueck in _umbrechen(m.get("beschreibung") or "", 32)[:3]:
            z.text((x0 + 24, y), stueck, font=s(SCHRIFT, 20), fill=FARBE_STILL)
            y += 26
        zustand = "eingebaut" if m.get("eingebaut") else "Zuordnung offen"
        z.text((x0 + 24, y1 - 46), zustand, font=s(SCHRIFT_HALB, 20),
               fill=FARBE_AKZENT if m.get("eingebaut") else (168, 132, 96))
    return bild


def seite_gebaeude(gebaeude, seite, seiten):
    bild = hintergrund()
    z = ImageDraw.Draw(bild)
    kopf(z, "Gebaeudeverzeichnis", "die 20 Gebäude mit Ertrag und Voraussetzung", seite, seiten)
    y = 310
    kopfhoehe = 44
    z.rectangle([RAND, y, SEITE[0] - RAND, y + kopfhoehe], fill=(32, 39, 50))
    z.text((RAND + 16, y + 10), "Gebäude", font=s(SCHRIFT_HALB, 24), fill=FARBE_GOLD)
    z.text((RAND + 520, y + 10), "Kategorie", font=s(SCHRIFT_HALB, 24), fill=FARBE_GOLD)
    z.text((RAND + 900, y + 10), "Ertrag je Stunde", font=s(SCHRIFT_HALB, 24), fill=FARBE_GOLD)
    z.text((RAND + 1600, y + 10), "Voraussetzung", font=s(SCHRIFT_HALB, 24), fill=FARBE_GOLD)
    y += kopfhoehe
    for i, g in enumerate(gebaeude):
        hoehe = 56
        if i % 2 == 0:
            z.rectangle([RAND, y, SEITE[0] - RAND, y + hoehe], fill=(19, 24, 31))
        ertrag = g.get("ertrag_pro_stunde") or {}
        if ertrag and all(isinstance(v, (int, float)) for v in ertrag.values()):
            ertragstext = ", ".join("%s %s" % (k, v) for k, v in ertrag.items())
        elif ertrag:
            ertragstext = ", ".join("%s %s" % (k, v) for k, v in ertrag.items())
        else:
            ertragstext = "-"
        z.text((RAND + 16, y + 14), g["name"], font=s(SCHRIFT, 24), fill=FARBE_TEXT)
        z.text((RAND + 520, y + 14), g.get("kategorie") or "-", font=s(SCHRIFT, 22), fill=FARBE_STILL)
        z.text((RAND + 900, y + 14), ertragstext[:58], font=s(SCHRIFT, 22), fill=FARBE_TEXT)
        z.text((RAND + 1600, y + 14), (g.get("voraussetzung") or "-")[:46],
               font=s(SCHRIFT, 19), fill=FARBE_STILL)
        y += hoehe
    return bild


def baue():
    einheiten = lade("data/units.json")["einheiten"]
    waren = lade("data/items.json")["waren"]
    rohstoffe = lade("data/resources.json")["rohstoffe"]
    gebaeude_liste = lade("data/buildings.json")["gebaeude"]
    motive = lade("data/gebaeude_motive.json")["motive"]
    gebaeude_namen = {g["id"]: g["name"] for g in gebaeude_liste}

    nah = [(k, v) for k, v in einheiten.items() if v.get("kategorie") in ("Nahkampf", "Fernkampf")]
    rest = [(k, v) for k, v in einheiten.items() if v.get("kategorie") not in ("Nahkampf", "Fernkampf")]

    def einheit_karte(name, d):
        w = d.get("werte") or {}
        k = d.get("kosten") or {}
        kosten = ", ".join("%s %s" % (kk, vv) for kk, vv in list(k.items())[:2]) or "-"
        return {
            "name": name,
            "icon": d.get("icon") or "",
            "zeile1": d.get("kategorie") or "-",
            "zeilen": ["AT %s / SK %s" % (w.get("AT", "-"), w.get("SK", "-")),
                       "LE %s / PA %s" % (w.get("LE", "-"), w.get("PA", "-")),
                       kosten],
            "fuss": d.get("gebaeude") or "",
        }

    def ware_karte(name, d):
        return {
            "name": name,
            "icon": d.get("icon") or "",
            "zeile1": d.get("werkstatt") or "-",
            "zeilen": ["Voraussetzung: %s" % (d.get("voraussetzung") or "-"),
                       "gebraucht von: %s" % ", ".join(d.get("benoetigt_von") or [])],
            "fuss": "",
        }

    seiten = []
    seiten.append(seite_titel([
        (str(len(einheiten)), "Einheiten in vier Kategorien"),
        (str(len(waren)), "Waren aus drei Werkstaetten"),
        (str(len(rohstoffe)), "Rohstoffe mit Ertrag je Gelaende"),
        (str(len(gebaeude_liste)), "Gebaeude, davon %d Originalmotive" % len(motive)),
    ]))
    seiten.append(seite_rohstoffe(rohstoffe, gebaeude_liste, 2, 8))
    seiten.append(raster_seite("Waren", "alles, was in Schmiede, Bogenbauer und Nähstube entsteht",
                               [ware_karte(k, v) for k, v in waren.items()], 3, 8, spalten=6))
    seiten.append(raster_seite("Einheiten - Kampf", "Nahkampf und Fernkampf, Werte aus data/units.json",
                               [einheit_karte(k, v) for k, v in nah], 4, 8, spalten=5))
    seiten.append(raster_seite("Einheiten - Spezial", "Diebe, Späher, Belagerung und Karren",
                               [einheit_karte(k, v) for k, v in rest], 5, 8, spalten=5))
    seiten.append(seite_motive(motive, gebaeude_namen, 6, 8))
    seiten.append(seite_gebaeude(gebaeude_liste[:13], 7, 8))
    seiten.append(seite_gebaeude(gebaeude_liste[13:], 8, 8))

    erste = seiten[0].convert("RGB")
    weitere = [b.convert("RGB") for b in seiten[1:]]
    erste.save(ZIEL, "PDF", resolution=DPI, save_all=True, append_images=weitere)
    print("PDF: %s" % ZIEL)
    print("Seiten: %d, Groesse: %d Byte" % (len(seiten), os.path.getsize(ZIEL)))
    print("Einheiten: %d (Kampf %d, Spezial %d), Waren: %d, Rohstoffe: %d, Gebaeude: %d, Motive: %d"
          % (len(einheiten), len(nah), len(rest), len(waren), len(rohstoffe),
             len(gebaeude_liste), len(motive)))
    return ZIEL


if __name__ == "__main__":
    baue()
