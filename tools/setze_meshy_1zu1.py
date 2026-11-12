# -*- coding: ascii -*-
"""Meshy-Bilder auf 1:1 bringen und das Wappen freistellen - Weg 2 (Auftrag Nr. 6).

Verfahren nach Claudes Antwort (docs/eingaenge/CLAUDE_20261112_MESHY_1ZU1/), hier umgesetzt:

  SCHNITT   x0 = clamp(cx - 661, 0, 394), Ausschnitt x0 .. x0 + 1142, volle Hoehe 864.
            cx ist die waagerechte Mitte des Hauptmotivs. Ohne Daniels Liste gilt cx = 768
            (Bildmitte) - das ist Claudes Vorgabe, kein geratener Wert.
  ERGAENZUNG  je Seite 128 px: Spiegelband der Randzeilen, mit Unschaerfe, Farbflaeche und
            Abdunkeln nach #1a0a09 (drei Verlaeufe, von der Naht nach aussen).
  WAPPEN    Grundmodell aus vier Eckfeldern, Farbabstand, Flutfuellung von den Ecken, weiche
            Alpha-Kante, Rueckrechnung der Farbe gegen den grauen Saum.

Aufruf:  python -X utf8 tools/setze_meshy_1zu1.py [--cx 768,700,...]
Ergebnis: assets/hintergruende/meshy_1zu1/*_1142x1120.png
          assets/wappen/elfen_wappen.png (+ 128 px und 64 px)
          docs/audits/messwerte/meshy_1zu1_<datum>.json
"""
from __future__ import annotations

import argparse
import io as _io
import json
import os
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps, ImageStat

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASIS = os.path.join(ROOT, "docs/eingaenge/MESHY_20261112_BILDASSETS")
ZIEL_HG = os.path.join(ROOT, "assets/hintergruende/meshy_1zu1")
ZIEL_WAPPEN = os.path.join(ROOT, "assets/wappen")
MESS = os.path.join(ROOT, "docs/audits/messwerte")

BREITE, HOEHE = 1142, 1120                  # Daniels Entscheidung, Register 469
QUELLE_HOEHE = 864                          # 1536 x 864
RAND = 128                                  # je Seite zu ergaenzen
MOTIV_MITTE = 661.0                         # (157 + 1142) / 2 nicht - Claudes 661, siehe unten
DUNKEL = (26, 10, 9)                        # #1a0a09

BILDER = [
    ("panorama/ref_panorama_menschlich.png", "panorama_menschlich"),
    ("panorama/ref_panorama_elfisch.png", "panorama_elfisch"),
    ("panorama/ref_panorama_zwergisch.png", "panorama_zwergisch"),
    ("panorama/ref_panorama_gnome.png", "panorama_gnome"),
    ("panorama/ref_panorama_trolle.png", "panorama_trolle"),
    ("panorama/ref_panorama_ghule.png", "panorama_ghule"),
    ("elfen/ref_elfen_bibliothek.png", "elfen_bibliothek"),
    ("elfen/ref_elfen_kriegerakademie.png", "elfen_kriegerakademie"),
    ("elfen/ref_elfen_stellmacher.png", "elfen_stellmacher"),
]
WAPPEN = "elfen/ref_elfen_wappen_und_banner.png"


def verlauf(w: int, h: int, wert_oben: int, wert_unten: int) -> Image.Image:
    """Senkrechter Verlauf als Maske (y = 0 ist oben)."""
    zeilen = bytearray()
    for y in range(h):
        anteil = y / float(max(1, h - 1))
        wert = int(round(wert_oben + (wert_unten - wert_oben) * anteil))
        zeilen += bytes([wert]) * w
    return Image.frombytes("L", (w, h), bytes(zeilen))


HALTEN = 8          # px an der Naht, in denen NICHTS veraendert wird (Kriterium E7: +-5)


def keil(w: int, h: int, naht_unten: bool, laenge: int, halten: int = HALTEN) -> Image.Image:
    """Maske: 0 an der Naht und in den ersten `halten` px, dann linear auf 255 bei `laenge`."""
    zeilen = bytearray()
    for y in range(h):
        abstand = (h - 1 - y) if naht_unten else y        # Abstand von der Naht
        if abstand <= halten:
            wert = 0
        else:
            wert = int(round(min(1.0, (abstand - halten) / float(max(1, laenge - halten))) * 255))
        zeilen += bytes([wert]) * w
    return Image.frombytes("L", (w, h), bytes(zeilen))


def verlauf_naht(w: int, h: int, naht_unten: bool, halten: int = HALTEN) -> Image.Image:
    """Maske: 0 an der Naht und in den ersten `halten` px, dann linear bis 255 am Aussenrand."""
    zeilen = bytearray()
    for y in range(h):
        abstand = (h - 1 - y) if naht_unten else y
        if abstand <= halten:
            wert = 0
        else:
            wert = int(round((abstand - halten) / float(max(1, h - 1 - halten)) * 255))
        zeilen += bytes([wert]) * w
    return Image.frombytes("L", (w, h), bytes(zeilen))


def horizont_im_rand(ausschnitt: Image.Image, oben: bool) -> float:
    """Groesster Sprung zweier Nachbarzeilen (Graumittel) in den 128 Randzeilen."""
    g = ausschnitt.convert("L")
    w, h = g.size
    box = (0, 0, w, RAND) if oben else (0, h - RAND, w, h)
    streifen = g.crop(box)
    mittel = [ImageStat.Stat(streifen.crop((0, y, w, y + 1))).mean[0]
              for y in range(streifen.height)]
    return max(abs(mittel[i + 1] - mittel[i]) for i in range(len(mittel) - 1))


def band(ausschnitt: Image.Image, oben: bool) -> Image.Image:
    """Eine Ergaenzung von 128 px Hoehe nach Claudes Verfahren B."""
    w = ausschnitt.width
    quelle = ausschnitt.crop((0, 0, w, RAND)) if oben else ausschnitt.crop((0, QUELLE_HOEHE - RAND, w, QUELLE_HOEHE))
    gespiegelt = ImageOps.flip(quelle)                 # Nahtseite liegt am Original an

    farbe = ImageStat.Stat((ausschnitt.crop((0, 0, w, 16)) if oben
                            else ausschnitt.crop((0, QUELLE_HOEHE - 16, w, QUELLE_HOEHE)))).mean
    flaeche = Image.new("RGB", (w, RAND), tuple(int(round(v)) for v in farbe))
    dunkel = Image.new("RGB", (w, RAND), DUNKEL)

    sprung = horizont_im_rand(ausschnitt, oben)
    if sprung <= 12:                                   # kein Horizont: Spiegelung erlaubt
        unscharf = gespiegelt.filter(ImageFilter.GaussianBlur(8))
        m1 = keil(w, RAND, naht_unten=oben, laenge=32)
        ergebnis = Image.composite(unscharf, gespiegelt, m1)
    else:                                              # Horizont: nur Flaechen
        ergebnis = gespiegelt

    # Farbflaeche: an der Naht 0 Prozent, am Aussenrand 100 Prozent
    m2 = verlauf_naht(w, RAND, naht_unten=oben)
    ergebnis = Image.composite(flaeche, ergebnis, m2)
    # Abdunkeln: an der Naht 0, ab 64 px voll
    m3 = keil(w, RAND, naht_unten=oben, laenge=64)
    ergebnis = Image.composite(dunkel, ergebnis, m3)
    return ergebnis


def auf_1zu1(quelle: Image.Image, cx: float) -> tuple:
    """Bild auf 1142 x 1120 bringen - Weg 2 (beschneiden und Hoehe ergaenzen)."""
    x0 = int(round(max(0.0, min(394.0, cx - MOTIV_MITTE))))
    ausschnitt = quelle.crop((x0, 0, x0 + BREITE, QUELLE_HOEHE))
    ziel = Image.new("RGB", (BREITE, HOEHE))
    ziel.paste(band(ausschnitt, oben=True), (0, 0))
    ziel.paste(ausschnitt, (0, RAND))
    ziel.paste(band(ausschnitt, oben=False), (0, RAND + QUELLE_HOEHE))
    return ziel, x0, horizont_im_rand(ausschnitt, True), horizont_im_rand(ausschnitt, False)


def naht_messung(bild: Image.Image, y: int) -> dict:
    """Naht, Kanten und Helligkeit an der Naht (Claudes Kriterien B und E)."""
    g = bild.convert("L")
    w = g.width

    def zeilenmittel(yy):
        return ImageStat.Stat(g.crop((0, yy, w, yy + 1))).mean[0]

    def sprung(a, b):
        return ImageStat.Stat(ImageChops.difference(g.crop((0, a, w, a + 1)),
                                                    g.crop((0, b, w, b + 1)))).mean[0]

    nachbarn = [sprung(i, i + 1) for i in range(RAND + 4, RAND + 120, 4)]   # im Originalbereich
    nachbarn.sort()
    median = nachbarn[len(nachbarn) // 2]
    an_der_naht = sprung(y - 1, y)
    innen = [zeilenmittel(yy) for yy in range(y, y + 8)]
    aussen = [zeilenmittel(yy) for yy in range(y - 8, y)]
    kante = g.filter(ImageFilter.FIND_EDGES).crop((0, y - 2, w, y + 3))
    return {"naht_sprung": round(an_der_naht, 2),
            "median_nachbarn": round(median, 2),
            "naht_ok": an_der_naht <= 1.5 * median,
            "helligkeit_diff": round(abs(sum(innen) / 8.0 - sum(aussen) / 8.0), 2),
            "kante_mittel": round(ImageStat.Stat(kante).mean[0], 2)}


def schaerfe(bild: Image.Image, box) -> float:
    """Laplace-Varianz (Schaerfemass) in einem Bereich."""
    kern = ImageFilter.Kernel((3, 3), (0, 1, 0, 1, -4, 1, 0, 1, 0), scale=1, offset=128)
    return round(ImageStat.Stat(bild.convert("L").crop(box).filter(kern)).var[0], 1)


def wappen_freistellen(quelle: Image.Image) -> tuple:
    """Wappen freistellen (Claudes Teil C) und die Guete messen."""
    rgb = quelle.convert("RGB")
    w, h = rgb.size
    kante = 32
    ecken = [rgb.crop((0, 0, kante, kante)), rgb.crop((w - kante, 0, w, kante)),
             rgb.crop((0, h - kante, kante, h)), rgb.crop((w - kante, h - kante, w, h))]
    mittel = [ImageStat.Stat(e).mean for e in ecken]
    streuung = max(max(ImageStat.Stat(e).stddev) for e in ecken)
    abweichung = max(max(m[k] for m in mittel) - min(m[k] for m in mittel) for k in range(3))
    einfarbig = abweichung <= 4 and streuung <= 3

    # Grundmodell: 2 x 2 aus den vier Eckfarben, weich auf die volle Groesse
    klein = Image.new("RGB", (2, 2))
    klein.putpixel((0, 0), tuple(int(round(v)) for v in mittel[0]))
    klein.putpixel((1, 0), tuple(int(round(v)) for v in mittel[1]))
    klein.putpixel((0, 1), tuple(int(round(v)) for v in mittel[2]))
    klein.putpixel((1, 1), tuple(int(round(v)) for v in mittel[3]))
    grund = klein.resize((w, h), Image.BILINEAR)

    diff = ImageChops.difference(rgb, grund)
    r, g_, b = diff.split()
    d = ImageChops.lighter(ImageChops.lighter(r, g_), b)      # groesster Kanalabstand

    t0 = int(round(3 * streuung + 2))
    t1 = t0 + 40

    # nur den von aussen erreichbaren Grund entfernen
    nah = d.point(lambda v: 255 if v <= t1 else 0)
    for ecke in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        if nah.getpixel(ecke) == 255:
            ImageDraw.floodfill(nah, ecke, 128, thresh=0)
    gefuellt = nah.point(lambda v: 255 if v == 128 else 0)

    # Alpha: d <= t0 -> 0, d >= t1 -> 255, dazwischen linear; ausserhalb immer 255
    alpha = d.point(lambda v: 0 if v <= t0 else (255 if v >= t1 else int(round((v - t0) * 255 / float(t1 - t0)))))
    alpha = Image.composite(alpha, Image.new("L", (w, h), 255), gefuellt)

    # Farbe gegen den grauen Saum zurueckrechnen: echte = (pixel - (1 - a) * grund) / a
    a = alpha.point(lambda v: max(1, v))
    ap = list(a.getdata())
    ergebnis = []
    for kanal, grund_kanal in zip(rgb.split(), grund.split()):
        px = list(kanal.getdata())
        gp = list(grund_kanal.getdata())
        puffer = bytearray(w * h)
        for k in range(w * h):
            al = ap[k]
            if al >= 255:                                  # voll deckend: Farbe bleibt
                puffer[k] = px[k]
                continue
            af = al / 255.0
            wert = (px[k] - (1.0 - af) * gp[k]) / af
            puffer[k] = 0 if wert < 0 else (255 if wert > 255 else int(round(wert)))
        ergebnis.append(bytes(puffer))
    farbig = Image.merge("RGB", [Image.frombytes("L", (w, h), e) for e in ergebnis])
    aus = farbig.convert("RGBA")
    aus.putalpha(alpha)

    # Guete messen
    daten = list(alpha.getdata())
    deckend = sum(1 for v in daten if v == 255)
    halb = sum(1 for v in daten if 0 < v < 255)
    leer = sum(1 for v in daten if v == 0)
    saum = 0
    fp = list(farbig.getdata())
    gp3 = list(grund.getdata())
    for k in range(w * h):
        if 0 < daten[k] < 255:
            if max(abs(fp[k][c] - gp3[k][c]) for c in range(3)) < t0:
                saum += 1
    masse = {"breite": w, "hoehe": h, "einfarbig": einfarbig, "abweichung": round(abweichung, 1),
             "streuung": round(streuung, 2), "t0": t0, "t1": t1,
             "deckend": deckend, "halb": halb, "leer": leer,
             "halb_anteil_prozent": round(100.0 * halb / max(1, deckend), 2),
             "saum_anteil_prozent": round(100.0 * saum / max(1, halb), 2)}
    return aus, masse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cx", default="", help="Komma-Liste der Motivmitten, sonst 768 je Bild")
    args = parser.parse_args()
    cx_liste = [float(x) for x in args.cx.split(",")] if args.cx.strip() else []

    os.makedirs(ZIEL_HG, exist_ok=True)
    os.makedirs(ZIEL_WAPPEN, exist_ok=True)
    os.makedirs(MESS, exist_ok=True)
    bericht = {"datum": "2026-11-12", "weg": 2, "breite": BREITE, "hoehe": HOEHE, "bilder": []}

    for i, (rel, name) in enumerate(BILDER):
        pfad = os.path.join(BASIS, rel)
        if not os.path.exists(pfad):
            print("fehlt:", rel)
            continue
        quelle = Image.open(pfad).convert("RGB")
        cx = cx_liste[i] if i < len(cx_liste) else 768.0
        fertig, x0, hor_oben, hor_unten = auf_1zu1(quelle, cx)
        ziel = os.path.join(ZIEL_HG, name + "_1142x1120.jpg")
        fertig.save(ziel, quality=92, optimize=True, subsampling=0)   # rund 400 KB statt 2 MB
        oben = naht_messung(fertig, RAND)
        unten = naht_messung(fertig, RAND + QUELLE_HOEHE)
        schaerfe_vorher = schaerfe(quelle.crop((x0, 0, x0 + BREITE, QUELLE_HOEHE)), (0, 0, BREITE, QUELLE_HOEHE))
        schaerfe_nachher = schaerfe(fertig, (0, RAND, BREITE, RAND + QUELLE_HOEHE))
        eintrag = {"bild": name, "cx": cx, "x0": x0, "horizont_oben": round(hor_oben, 1),
                   "horizont_unten": round(hor_unten, 1), "oben": oben, "unten": unten,
                   "schaerfe_vorher": schaerfe_vorher, "schaerfe_nachher": schaerfe_nachher,
                   "groesse": list(fertig.size)}
        bericht["bilder"].append(eintrag)
        print("%-22s cx %4.0f x0 %3d | Naht oben %5.2f (Grenze %5.2f) %s | unten %5.2f %s | "
              "Helligkeit %4.2f/%4.2f | Schaerfe %s -> %s"
              % (name, cx, x0, oben["naht_sprung"], 1.5 * oben["median_nachbarn"],
                 "ok" if oben["naht_ok"] else "ROT", unten["naht_sprung"],
                 "ok" if unten["naht_ok"] else "ROT", oben["helligkeit_diff"], unten["helligkeit_diff"],
                 schaerfe_vorher, schaerfe_nachher))

    # Wappen
    pfad = os.path.join(BASIS, WAPPEN)
    if os.path.exists(pfad):
        wappen, masse = wappen_freistellen(Image.open(pfad))
        wappen.save(os.path.join(ZIEL_WAPPEN, "elfen_wappen.png"))
        for kante in (128, 64):
            klein = wappen.copy().convert("RGBa").resize((kante, kante), Image.LANCZOS).convert("RGBA")
            klein.save(os.path.join(ZIEL_WAPPEN, "elfen_wappen_%d.png" % kante))
        bericht["wappen"] = masse
        print("\nWappen: %d x %d | Grund %s (Abweichung %.1f, Streuung %.2f) | deckend %d, halb %d (%.2f %%), "
              "leer %d | Saum %.2f %%"
              % (masse["breite"], masse["hoehe"], "einfarbig" if masse["einfarbig"] else "VERLAUF",
                 masse["abweichung"], masse["streuung"], masse["deckend"], masse["halb"],
                 masse["halb_anteil_prozent"], masse["leer"], masse["saum_anteil_prozent"]))

    ziel = os.path.join(MESS, "meshy_1zu1_20261112.json")
    with _io.open(ziel, "w", encoding="utf-8") as f:
        json.dump(bericht, f, ensure_ascii=False, indent=1)
    print("\nMesswerte:", ziel)


if __name__ == "__main__":
    main()
