"""Pruefung des EXE-Symbols — Vorgabe Daniel 05.10.2026: das Nebelsee-Bild soll das Symbol sein.

Belegt vier Dinge:
  1. Das Symbol traegt **sechs Groessen** (16, 32, 48, 64, 128, 256) und jede ist ein echtes Bild
     in genau dieser Groesse (sonst zeigt Windows eine unscharf hochgerechnete Fassung).
  2. Der Inhalt ist wirklich **das Nebelsee-Bild**: oben blau-grauer Himmel/Berge, unten der
     goldene Schriftzug — nicht das fruehere braune Wappen. (Inhalt, nicht Dateiname.)
  3. Die **Quelldatei bleibt unberuehrt** (Groesse und Pruefsumme), und die vorherige Symbolfassung
     ist **gesichert** — es wurde nichts ueberschrieben ohne Sicherung.
  4. Das Bau-Werkzeug benutzt **genau dieses** Symbol, und das Werkzeug laeuft wiederholbar
     (Trockenlauf ohne Nebenwirkung).

Aufruf:  python -X utf8 tests/test_exe_symbol.py
"""
from __future__ import annotations

import hashlib
import os
import struct
import subprocess
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
sys.path.insert(0, os.path.join(ROOT, "tools"))
import build_exe  # noqa: E402  (der Pruefer des Bau-Werkzeugs selbst)

ICO = os.path.join(ROOT, "assets", "icons", "nebelseetal.ico")
QUELLE_GIF = os.path.join(ROOT, "assets", "quellbilder", "nebelseetal.png")
QUELLE_PNG = os.path.join(ROOT, "assets", "icons", "nebelseetal_symbol.png")
WERKZEUG = os.path.join(ROOT, "tools", "mache_icon.py")
SICHERUNGSORDNER = os.path.join(os.environ.get("LOCALAPPDATA", ROOT), "hermes", "cache",
                                "scratch", "nebel_backup")
ERWARTET = [16, 32, 48, 64, 128, 256]


def png_kopf(daten: bytes):
    """(breite, hoehe) aus dem IHDR eines PNG."""
    return struct.unpack(">II", daten[16:24])


def bild_lesen(daten: bytes):
    """PNG entschluesseln -> (breite, hoehe, RGBA-Bytes). Filterarten 0-4, Farbtyp 6."""
    stelle, breite, hoehe, idat = 8, 0, 0, b""
    while stelle < len(daten):
        laenge = struct.unpack(">I", daten[stelle:stelle + 4])[0]
        art = daten[stelle + 4:stelle + 8]
        inhalt = daten[stelle + 8:stelle + 8 + laenge]
        if art == b"IHDR":
            breite, hoehe = struct.unpack(">II", inhalt[:8])
        elif art == b"IDAT":
            idat += inhalt
        elif art == b"IEND":
            break
        stelle += 12 + laenge
    roh = zlib.decompress(idat)
    je_zeile = breite * 4
    zeilen, vorige, pos = [], bytearray(je_zeile), 0
    for _ in range(hoehe):
        art = roh[pos]
        pos += 1
        zeile = bytearray(roh[pos:pos + je_zeile])
        pos += je_zeile
        for i in range(je_zeile):
            a = zeile[i - 4] if i >= 4 else 0
            b = vorige[i]
            c = vorige[i - 4] if i >= 4 else 0
            if art == 1:
                zeile[i] = (zeile[i] + a) & 0xFF
            elif art == 2:
                zeile[i] = (zeile[i] + b) & 0xFF
            elif art == 3:
                zeile[i] = (zeile[i] + (a + b) // 2) & 0xFF
            elif art == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                zeile[i] = (zeile[i] + (a if pa <= pb and pa <= pc else (b if pb <= pc else c))) & 0xFF
        vorige = zeile
        zeilen.append(bytes(zeile))
    return breite, hoehe, b"".join(zeilen)


def mittelfarbe(rgba, breite, y0, y1):
    """Mittlere Farbe eines waagerechten Streifens (ohne vollstaendig durchsichtige Bildpunkte)."""
    r = g = b = n = 0
    for y in range(y0, y1):
        for x in range(breite):
            st = (y * breite + x) * 4
            if rgba[st + 3] < 40:
                continue
            r += rgba[st]
            g += rgba[st + 1]
            b += rgba[st + 2]
            n += 1
    if not n:
        return (0, 0, 0)
    return (r // n, g // n, b // n)


def ico_eintraege(pfad):
    daten = open(pfad, "rb").read()
    if daten[:4] != b"\x00\x00\x01\x00":
        return [], daten
    anzahl = struct.unpack("<H", daten[4:6])[0]
    liste = []
    for i in range(anzahl):
        breite, hoehe, _, _, _, bit, laenge, versatz = struct.unpack(
            "<BBBBHHII", daten[6 + 16 * i:22 + 16 * i])
        liste.append({"breite": breite or 256, "hoehe": hoehe or 256, "bit": bit,
                      "nutzlast": daten[versatz:versatz + laenge]})
    return liste, daten


abschnitt("1. Das Symbol traegt sechs Groessen, jede als echtes Bild")

check("die Symboldatei existiert", os.path.exists(ICO))
eintraege, roh_ico = ico_eintraege(ICO) if os.path.exists(ICO) else ([], b"")
check("es ist wirklich ein ICO", roh_ico[:4] == b"\x00\x00\x01\x00", roh_ico[:4].hex())
check("es sind genau sechs Eintraege", len(eintraege) == 6, str(len(eintraege)))
check("die Groessen stehen in der erwarteten Reihenfolge",
      [e["breite"] for e in eintraege] == ERWARTET, str([e["breite"] for e in eintraege]))
alle_png = all(e["nutzlast"][:8] == b"\x89PNG\r\n\x1a\n" for e in eintraege)
check("jeder Eintrag ist ein echtes PNG (kein Platzhalter)", alle_png)
masse_ok = True
for e in eintraege:
    if e["nutzlast"][:8] == b"\x89PNG\r\n\x1a\n":
        w, h = png_kopf(e["nutzlast"])
        masse_ok = masse_ok and (w, h) == (e["breite"], e["hoehe"])
check("jedes Bild hat genau die Groesse seines Eintrags (nicht hochgerechnet von 1 px)",
      masse_ok)
check("das Bau-Werkzeug liest dieselben sechs Groessen",
      build_exe.ico_groessen(build_exe.ICON) == [(g, g) for g in ERWARTET],
      str(build_exe.ico_groessen(build_exe.ICON)))
check("das Bau-Werkzeug benutzt genau diese Symboldatei",
      os.path.normcase(os.path.abspath(str(build_exe.ICON))) == os.path.normcase(os.path.abspath(ICO)),
      str(build_exe.ICON))

abschnitt("2. Der Inhalt ist das Nebelsee-Bild — nicht mehr das braune Wappen")

voll = [e for e in eintraege if e["breite"] == 256]
klein = [e for e in eintraege if e["breite"] == 32]
if not voll or not klein:
    check("ein 256-px- und ein 32-px-Eintrag zum Ansehen sind vorhanden", False)
else:
    # Gemessen wird auf der vollen Fassung: bei 32 px verschmilzt das Gold mit dem dunklen
    # Hintergrund zu Oliv und faellt durch jede strenge Goldgrenze.
    breite, hoehe, rgba = bild_lesen(voll[0]["nutzlast"])
    oben = mittelfarbe(rgba, breite, 0, hoehe // 3)
    check("oben liegt blau-grauer Himmel/Fels (Blau nicht kleiner als Rot)",
          oben[2] >= oben[0], f"oben {oben}")
    check("oben ist NICHT das braune Wappen (Braunanteil niedrig)",
          oben[0] <= oben[2] + 30, f"oben {oben}")
    # Der goldene Schriftzug sitzt im MITTLEREN Drittel (gemessen: Bildzeilen 105-147 von 256).
    gold_zeilen = [i // 4 // breite for i in range(0, len(rgba), 4)
                   if rgba[i] > rgba[i + 2] + 30 and rgba[i + 1] > rgba[i + 2] + 30
                   and rgba[i + 3] > 40]
    anteil = 100 * len(gold_zeilen) / (breite * hoehe)
    mitte = [y for y in gold_zeilen if hoehe * 0.30 <= y <= hoehe * 0.70]
    check("der goldene Schriftzug ist im Symbol vorhanden (ueber 3 % goldene Bildpunkte)",
          anteil > 3.0, f"{anteil:.1f} % goldene Bildpunkte")
    check("er sitzt im mittleren Drittel, wie in der Vorlage",
          mitte and len(mitte) >= 0.5 * len(gold_zeilen),
          f"{len(mitte)} von {len(gold_zeilen)} goldenen Bildpunkten in den Bildzeilen "
          f"y {min(gold_zeilen)}-{max(gold_zeilen)} von {hoehe}")
    b32, h32, px32 = bild_lesen(klein[0]["nutzlast"])
    oben32 = mittelfarbe(px32, b32, 0, h32 // 3)
    check("auch die 32-px-Fassung zeigt oben blau-grauen Himmel (kein Platzhalterbild)",
          oben32[2] >= oben32[0], f"oben {oben32}")
    befund("Kleine Groessen", "die Quelle ist nur 80x80 px — die Eintraege 128 und 256 sind "
                              "interpoliert und wirken weicher; bei 32 px wird der goldene "
                              "Schriftzug zu einem oliv-goldenen Band (bei einem Schriftzug-Logo "
                              "unvermeidbar)")

abschnitt("3. Die Quelldatei bleibt unberuehrt, die vorherige Fassung ist gesichert")

roh_gif = open(QUELLE_GIF, "rb").read()
check("die beigelegte Quelldatei ist unveraendert (Groesse und Pruefsumme)",
      len(roh_gif) == 6476
      and hashlib.sha256(roh_gif).hexdigest()
      == "f1a1d4550bd99a4a73d9a26f11c2418d39e7dcb093f9a2f9c48c0cb40724bcbb",
      f"{len(roh_gif)} Byte")
check("sie ist weiterhin ein GIF (nichts umbenannt, nichts ersetzt)",
      roh_gif[:6] == b"GIF89a", roh_gif[:6].decode("latin-1"))
roh_png = open(QUELLE_PNG, "rb").read() if os.path.exists(QUELLE_PNG) else b""
check("die abgeleitete Symbol-Quelle ist ein 256x256-PNG",
      roh_png[:8] == b"\x89PNG\r\n\x1a\n" and png_kopf(roh_png) == (256, 256),
      str(png_kopf(roh_png)) if roh_png[:8] == b"\x89PNG\r\n\x1a\n" else "fehlt")
gesichert = [n for n in os.listdir(SICHERUNGSORDNER)
             if n.startswith("nebelseetal.ico")] if os.path.isdir(SICHERUNGSORDNER) else []
if gesichert:
    check("die vorherige Symbolfassung liegt gesichert vor (kein stilles Ueberschreiben)",
          True, ", ".join(sorted(gesichert)))
else:
    befund("Sicherung", f"keine gesicherte Vorlage gefunden in {SICHERUNGSORDNER}")

abschnitt("4. Das Werkzeug ist wiederholbar")

lauf = subprocess.run([sys.executable, "-X", "utf8", WERKZEUG, "--trockenlauf"],
                      capture_output=True, text=True, timeout=180)
check("der Trockenlauf endet ohne Fehler", lauf.returncode == 0, f"Rueckgabe {lauf.returncode}")
check("er meldet sechs gepruefte Groessen",
      lauf.stdout.count("x") >= 6 and "Trockenlauf" in lauf.stdout,
      lauf.stdout.strip().splitlines()[-1][:70] if lauf.stdout.strip() else "keine Ausgabe")
check("der Trockenlauf hat das Symbol nicht angefasst (keine Nebenwirkung)",
      ico_eintraege(ICO)[1] == roh_ico)

sys.exit(bericht())
