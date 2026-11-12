# -*- coding: ascii -*-
"""Leisten-Luecken bei sehr breiten Fenstern - P-3, Register 131 (02.11.2026).

BEFUND (Daniel): bei sehr breiten Fenstern wiederholt sich die gemalte Landschaft zwischen den
Symbolen. Am Code gemessen: die festen Teile wachsen nur bis `skala_max` (1,5), die Restbreite
nahmen die LUECKEN vollstaendig auf - bei 2560 px Fensterbreite Faktor 1,86, bei 3000 px 2,81, bei
3440 px 3,75. Jede Luecke ist ein Ausschnitt aus EINEM gemalten Bild; wird sie einzeln so weit
gedehnt, entstehen langgezogene Streifen und an jedem Ausschnittrand eine Naht.

Was diese Datei beweist
-----------------------
1. Die Grenzen stehen als Zahlen in der Datendatei (`luecke_max`, `skala_hart`, `rest_auffuellen`)
   und sind plausibel; `skala_hart` liegt nicht unter `skala_max`.
2. Die Lueckendehnung bleibt bei 2320 / 2560 / 3000 / 3440 px unter `luecke_max` - gemessen an den
   Abstaenden der Symbolmitten gegen die Originalabstaende, nicht am Wortlaut des Codes.
3. Bis zur Grenze fuellt das Band die Breite genau (keine Raender); darueber steht der Rest
   SYMMETRISCH links und rechts (gleiche Raender +-1 px), damit der Abschluss nicht wie ein Fehler
   aussieht.
4. Das Symbolfeld bleibt unverzerrt (Seitenverhaeltnis der Originalkachel +-2 Prozent).
5. GEGENPROBE: mit der alten Regel (`luecke_max` = 99) schlaegt dieselbe Messung bei 3440 px weit
   ueber der Grenze aus (ueber 3,0) - die Wache misst also wirklich.

Aufruf:  python -X utf8 tests/test_leisten_luecken.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['main:*']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

ROOT, SRC = import_src()
import main  # noqa: E402

try:
    from PIL import Image
    _pil = True
except Exception:              # noqa: BLE001 - ohne Pillow gibt es keine Leiste
    Image = None
    _pil = False

# UMGESTELLT 11.11.2026 (T2): die Leiste wird seit Daniels Befund D3 GEZEICHNET (elf Zellen,
# Name plus Zahl). Das gemalte Bild ist nicht mehr die Anzeige - seine Rechenwege
# (`leisten_zusammensetzen`, `_leisten_stuecke`) stehen aber weiter im Code und in der
# Datendatei unter `_altes_bild`. Diese Wache prueft genau diesen Rueckfall, damit die alten
# Grenzen nicht unbemerkt verrotten; die Anzeige selbst prueft `test_ressourcenleiste`.
DATEN = dict(main.RESSOURCENLEISTE.get("_altes_bild") or {})
FELDER = [f for f in (DATEN.get("felder") or []) if f.get("x") is not None]


def _dehnung(bild, mitten, skala):
    """Die tatsaechliche waagerechte Dehnung je LUECKE (1,0 = ungedehnt).

    Der Abstand zweier Symbolmitten besteht aus zwei halben Kacheln (wachsen gleichmaessig mit
    `skala`) und der Luecke dazwischen. Die Kachelbreite wird deshalb ABGEZOGEN, sonst misst man
    eine Mischung aus Skala und Dehnung und unterschaetzt die Dehnung deutlich.
    """
    halb = int(DATEN["kachel_halbbreite"])
    werte = []
    for i in range(len(FELDER) - 1):
        a = str(FELDER[i]["schluessel"])
        b = str(FELDER[i + 1]["schluessel"])
        if a not in mitten or b not in mitten:
            continue
        abstand_orig = int(FELDER[i + 1]["x"]) - int(FELDER[i]["x"])
        luecke_orig = abstand_orig - 2 * halb                # Breite der Luecke im Original
        luecke_neu = (mitten[b][0] - mitten[a][0]) - 2 * halb * skala
        if luecke_orig <= 0 or skala <= 0:
            continue
        werte.append(luecke_neu / (luecke_orig * skala))
    return werte


def _fuellung(bild):
    """(gefuellt_bis, rand_links, rand_rechts) aus dem Alphakanal."""
    bbox = bild.getchannel("A").getbbox()
    if not bbox:
        return 0, bild.width, 0
    return bbox[2], bbox[0], bild.width - bbox[2]


# ==========================================================================
abschnitt("1. Die Grenzen stehen in der Datendatei")
# ==========================================================================
check("1 luecke_max ist eine Zahl zwischen 1,0 und 3,0",
      isinstance(DATEN.get("luecke_max"), (int, float)) and 1.0 < float(DATEN["luecke_max"]) <= 3.0,
      str(DATEN.get("luecke_max")))
# M-3 (Daniels Befund 02.11.2026: "die ressourcen bilder oben [sind] verzerrt"). ENTSCHEIDUNG
# GEAENDERT: neben 'gleichmaessig' und 'leer' gibt es jetzt 'kacheln' - das Band skaliert nie ueber
# 1,0, die zusaetzliche Breite entsteht durch WIEDERHOLUNG der gemalten Luecken. Die alte Zusage
# "gleichmaessig oder leer" nagelte das Wachstum fest und wird deshalb erweitert.
check("1 rest_auffuellen ist gleichmaessig, leer oder kacheln",
      str(DATEN.get("rest_auffuellen")) in ("gleichmaessig", "leer", "kacheln"),
      str(DATEN.get("rest_auffuellen")))
check("1 skala_hart liegt nicht unter skala_max",
      float(DATEN.get("skala_hart") or 0) >= float(DATEN.get("skala_max") or 0),
      f"{DATEN.get('skala_hart')} gegen {DATEN.get('skala_max')}")

if not _pil:
    print("  BEFUND ohne Pillow keine Leiste messbar - Abschnitte 2 bis 4 uebersprungen")
else:
    # ======================================================================
    abschnitt("2. Die Lueckendehnung bleibt gedeckelt")
    # ======================================================================
    grenze = float(DATEN["luecke_max"])
    _stuecke = main._leisten_stuecke(DATEN)
    _luecken = [s for s in _stuecke if s["art"] == "dehnbar"]
    halb0 = int(DATEN["kachel_halbbreite"])
    del _stuecke
    for breite in (2320, 2560, 3000, 3440):
        bild, mitten, skala = main.leiste_zusammensetzen(DATEN, breite)
        check(f"2 bei {breite} px wird die Zielbreite genau getroffen", bild.width == breite,
              f"{bild.width} statt {breite}")
        if str(DATEN.get("rest_auffuellen")) == "kacheln":
            # M-3: die Luecke zwischen dem ersten und zweiten Symbol ist KEINE Dehnung, sondern eine
            # WIEDERHOLUNG des Originals mit unveraenderter Breite. Gemessen wird die Periodizitaet
            # der Bildpunkte: Bild(x) muss gleich Bild(x + Originalbreite) sein.
            if not _luecken:
                continue
            periode = max(s["bis"] - s["von"] for s in _luecken)
            x0 = mitten["siedler"][0] + halb0
            x1 = mitten["nahrung"][0] - halb0
            gleich = all(bild.getpixel((x, y)) == bild.getpixel((x + periode, y))
                         for x in range(x0, max(x0 + 1, x1 - periode), 5)
                         for y in range(0, bild.height, 7))
            check(f"2 bei {breite} px ist die Luecke eine Wiederholung in Originalbreite "
                  f"({periode} px), keine Dehnung", x1 - x0 > periode and gleich,
                  f"Luecke {x1 - x0} px, Periode {periode} px")
        else:
            werte = _dehnung(bild, mitten, skala)
            ist = max(werte) if werte else 0.0
            check(f"2 bei {breite} px bleibt die Lueckendehnung unter {grenze:g}",
                  bool(werte) and ist <= grenze + 0.02, f"groesste Dehnung {ist:.2f}")

    # ======================================================================
    abschnitt("3. Bis zur Grenze gefuellt, darueber symmetrische Raender")
    # ======================================================================
    if str(DATEN.get("rest_auffuellen")) == "kacheln":
        # M-3: im Modus 'kacheln' fuellt das Band JEDE Breite ganz - die Laenge entsteht durch
        # Wiederholung der Luecken, nicht durch Raender und nicht durch Dehnung.
        for breite in (1440, 1920, 2320, 2560, 3440):
            bild, mitten, skala = main.leiste_zusammensetzen(DATEN, breite)
            gefuellt, links, rechts = _fuellung(bild)
            check(f"3 bei {breite} px fuellt das Band die Breite ganz (kacheln)",
                  links == 0 and rechts <= 1, f"gefuellt bis {gefuellt}, Raender {links}/{rechts}")
            check(f"3 bei {breite} px bleiben die Symbole in Originalgroesse (Skala 1,0)",
                  abs(skala - 1.0) < 1e-9 and bild.height == 140,
                  f"Skala {skala:.3f}, Hoehe {bild.height}")
    else:
        for breite in (1440, 1920, 2320, 2560):
            bild, mitten, skala = main.leiste_zusammensetzen(DATEN, breite)
            gefuellt, links, rechts = _fuellung(bild)
            check(f"3 bei {breite} px fuellt das Band die Breite ganz", links == 0 and rechts <= 1,
                  f"gefuellt bis {gefuellt}, Raender {links}/{rechts}")
        bild, mitten, skala = main.leiste_zusammensetzen(DATEN, 3440)
        gefuellt, links, rechts = _fuellung(bild)
        check("3 bei 3440 px stehen die Raender SYMMETRISCH (gleiche Breite +-1 px)",
              links > 0 and abs(links - rechts) <= 1, f"Raender {links}/{rechts}, gefuellt bis {gefuellt}")
        check("3 der Rest wird nicht mit gestreckter Landschaft gefuellt (Band endet vor dem Rand)",
              gefuellt - links <= 2800, f"Band {links} bis {gefuellt} = {gefuellt - links} px bei 3440")

    # ======================================================================
    abschnitt("4. Das Symbol bleibt unverzerrt")
    # ======================================================================
    halb = int(DATEN["kachel_halbbreite"])
    orig = Image.open(os.path.join(ROOT, str(DATEN["datei"]).replace("/", os.sep))).convert("RGBA")
    soll = (2 * halb) / float(orig.height)
    for breite in (2320, 2560, 3440):
        bild, mitten, skala = main.leiste_zusammensetzen(DATEN, breite)
        mx = mitten["siedler"][0]
        kachel = bild.crop((mx - int(halb * skala), 0, mx + int(halb * skala), bild.height))
        verhaeltnis = kachel.width / float(kachel.height)
        check(f"4 bei {breite} px ist das Symbolfeld unverzerrt (+-2 Prozent)",
              abs(verhaeltnis - soll) / soll < 0.02, f"{verhaeltnis:.3f} gegen {soll:.3f}")

    # ======================================================================
    abschnitt("5. Gegenprobe: mit der ALTEN Regel schlaegt die Messung aus")
    # ======================================================================
    alt = dict(DATEN)
    alt["luecke_max"] = 99.0          # alte Regel: die Luecken nehmen die ganze Restbreite
    alt["rest_auffuellen"] = "leer"   # Dehnung statt Wiederholung - die Gegenprobe braucht sie
    alt.pop("kacheln", None)
    bild_alt, mitten_alt, skala_alt = main.leiste_zusammensetzen(alt, 3440)
    werte_alt = _dehnung(bild_alt, mitten_alt, skala_alt)
    check("5 mit luecke_max 99 wird die Landschaft bei 3440 px ueber 3-fach gedehnt",
          bool(werte_alt) and max(werte_alt) > 3.0,
          f"groesste Dehnung {max(werte_alt):.2f}" if werte_alt else "keine Werte")
    bild_neu, mitten_neu, skala_neu = main.leiste_zusammensetzen(DATEN, 3440)
    if str(DATEN.get("rest_auffuellen")) == "kacheln":
        # M-3: im Modus 'kacheln' ist "Dehnung" die falsche Messung - die Luecke ist ABSICHTLICH
        # breiter, aber aus wiederholten Originalstuecken. Gemessen wird deshalb die Periodizitaet:
        # das Bild muss sich nach der Originalbreite der Luecke wiederholen (Abschnitt 2 belegt das
        # fuer vier Breiten). Hier steht nur noch, dass die alte Regel wirklich gedehnt haette.
        check("5 die alte Regel haette bei 3440 px ueber 3-fach gedehnt (Gegenprobe)",
              bool(werte_alt) and max(werte_alt) > 3.0,
              f"ALT {max(werte_alt):.2f}" if werte_alt else "keine Werte")
        check("5 die neue Regel haelt die Symbole in Originalgroesse", abs(skala_neu - 1.0) < 1e-9,
              f"Skala {skala_neu:.3f}")
    else:
        werte_neu = _dehnung(bild_neu, mitten_neu, skala_neu)
        check("5 die neue Regel haelt dieselbe Messung bei gleicher Breite unter der Grenze",
              bool(werte_neu) and max(werte_neu) <= float(DATEN["luecke_max"]) + 0.02,
              f"ALT {max(werte_alt):.2f} gegen NEU {max(werte_neu):.2f}" if werte_neu and werte_alt else "")

sys.exit(bericht())
