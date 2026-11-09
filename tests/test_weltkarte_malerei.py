# -*- coding: ascii -*-
"""Wache fuer die gemalte Weltkarte (src/weltkarte_malerei.py, Designschritt D-3, 09.11.2026).

Was diese Datei zusichert und warum:

1. **Sieben Arten aus der Datendatei, keine zweite Farbtabelle.** `arten()` ist die Reihenfolge aus
   `data/gelaende.json`, und die Farben im Bild kommen aus `gelaende.farbe` - geprueft daran, dass
   die Hex-Werte der Datendatei NICHT im Quelltext stehen (sonst gaebe es zwei Wahrheiten).
2. **GEMALT, nicht gefuellt.** Eine Kachel hat weit mehr Farben als eine Flaeche, und ihr Mittelton
   liegt trotzdem an der Gelaendefarbe (die Malerei darf die Art nicht verlieren).
3. **Der Wald traegt TANNEN.** Im Waldbild stehen dunkle Nadelgruen-Pixel mit einer braunen Kontur;
   im Grasland darf dieselbe Dunkelheit nicht in dieser Menge vorkommen.
4. **Ohne Pillow wird nicht gemalt, sondern ein Fehler mit Grund geworfen** (`MalereiFehler`) - kein
   erfundenes Ersatzbild. Das Modul importiert Pillow deshalb NIRGENDS oben, nur in den Funktionen.
5. **Zwischenspeicher und Gleichheit:** derselbe Abruf liefert dasselbe Objekt (Tk gibt Bilder frei,
   die niemand mehr referenziert - Lehre 02.11.2026); eine geaenderte Karte ergibt ein NEUES Bild.
6. **Die ganze Karte ist EIN Bild** in der Groesse Spalten x Kante mal Zeilen x Kante; unbekannte
   Gelaendearten im Raster werden abgelehnt statt still uebergangen.
7. **Gleiche Eingabe, gleiches Bild** (Determinismus): zweimal gemalt ist pixelgleich - wichtig, weil
   das Spiel die Karte zwischenspeichert und zwei Staende sonst verschieden aussaehen.

Aufruf:  .venv/Scripts/python.exe -X utf8 tests/test_weltkarte_malerei.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import gelaende                        # Kennungen und Farben aus data/gelaende.json
import portalraum                      # das echte 20 x 20-Raster einer Weltkarte
import weltkarte_malerei as M          # der gepruefte Gegenstand

QUELLE = os.path.join(SRC, "weltkarte_malerei.py")


def _quelle() -> str:
    with open(QUELLE, encoding="utf-8") as datei:
        return datei.read()


def _farben(bild) -> dict:
    """Wie oft jede Farbe im Bild vorkommt."""
    zaehlung: dict = {}
    for anzahl, farbe in bild.getcolors(maxcolors=1 << 20) or []:   # (Anzahl, Farbe)
        zaehlung[farbe] = anzahl
    return zaehlung


def _mittel(bild) -> tuple:
    """Mittlere Farbe eines Bildes."""
    kleine = bild.resize((1, 1))
    return kleine.getpixel((0, 0))


def _abstand(a, b) -> float:
    return sum(abs(int(x) - int(y)) for x, y in zip(a, b)) / 3.0


def _dunkel_und_gruen(bild) -> int:
    """Pixel, die dunkel sind UND gruenlicher als rot/blau - die Nadelkronen."""
    zahl = 0
    for farbe, anzahl in _farben(bild).items():
        r, g, b = farbe[:3]
        if g < 90 and g >= r and g >= b:
            zahl += anzahl
    return zahl


def main() -> int:
    quelle = _quelle()
    arten = M.arten()

    abschnitt("1. Pillow nur in den Funktionen, nicht oben")
    kopf = quelle.split("def verfuegbar")[0]
    check("kein PIL-Import im Modulkopf", "import PIL" not in kopf and "from PIL" not in kopf)
    # Der Maler darf kein Fenster brauchen - geprueft wird der IMPORT, nicht das Wort (der
    # Modulkopf ERKLAERT, dass tkinter fehlt).
    check("kein tkinter-Import im Modul",
          "import tkinter" not in quelle and "from tkinter" not in quelle,
          "der Maler darf kein Fenster brauchen")
    check("verfuegbar() meldet Pillow", M.verfuegbar() is True)
    check("MalereiFehler nennt Pillow als Grund",
          "Pillow" in (M.MalereiFehler.__doc__ or "") or "Pillow" in quelle)
    check("Fehlertext nennt fehlendes Pillow im Quelltext",
          "Pillow fehlt - es wird nicht gemalt" in quelle)

    abschnitt("2. Arten und Farben aus der Datendatei (keine zweite Tabelle)")
    check("arten() ist die Reihenfolge aus data/gelaende.json",
          tuple(gelaende.GELAENDEARTEN) == arten, repr(arten))
    check("genau sieben Gelaendearten", len(arten) == 7, str(len(arten)))
    check("alle sieben Arten haben einen Maler", set(arten) == set(M._MOTIVE))
    doppelt = [art for art in arten if gelaende.farbe(art).lstrip("#").upper() in quelle.upper()]
    check("keine Gelaendefarbe als zweite Tabelle im Quelltext", not doppelt, repr(doppelt))

    abschnitt("3. Eine Kachel ist gemalt, nicht gefuellt")
    kante = 64
    for art in arten:
        bild = M.kachel(art, kante, 0)
        farben = _farben(bild)
        check("%s: Bild ist %d x %d" % (art, kante, kante), bild.size == (kante, kante),
              str(bild.size))
        check("%s: RGB" % art, bild.mode == "RGB", bild.mode)
        check("%s: mehr als 200 Farben (gemalt, nicht gefuellt)" % art, len(farben) > 200,
              "%d Farben" % len(farben))
        # F-34 (Daniel, 09.11.2026, 09:44): die gemalte Karte wird mit `M.HELLIGKEIT` aufgehellt
        # ("nur etwas heller wie bei Nummer 3"). Der Sollwert wird MITGERECHNET - so bleibt diese
        # Pruefung genauso eng wie vorher, statt sie zu lockern.
        soll = tuple(min(255, int(round(k * M.HELLIGKEIT))) for k in M._rgb(gelaende.farbe(art)))
        ist = _mittel(bild)
        abweichung = _abstand(ist, soll)
        check("%s: Mittelton liegt an der hell gerechneten Gelaendefarbe (Abweichung < 26)" % art,
              abweichung < 26, "%.1f (%s gegen %s)" % (abweichung, ist, soll))

    abschnitt("4. Der Wald traegt Tannen, das Grasland nicht")
    wald = M.kachel("wald", kante, 0)
    gras = M.kachel("grasland", kante, 0)
    dunkel_wald = _dunkel_und_gruen(wald)
    dunkel_gras = _dunkel_und_gruen(gras)
    check("Wald: dunkle Nadelgruen-Flaechen vorhanden", dunkel_wald > 300, str(dunkel_wald))
    check("Grasland: deutlich weniger dunkles Nadelgruen", dunkel_wald > dunkel_gras * 3,
          "%d gegen %d" % (dunkel_wald, dunkel_gras))
    check("Wald ist dunkler als Grasland", sum(_mittel(wald)) < sum(_mittel(gras)),
          "%s gegen %s" % (_mittel(wald), _mittel(gras)))

    abschnitt("5. Varianten, Zwischenspeicher, Determinismus")
    M.leeren()
    erst = M.kachel("wald", kante, 0)
    zweit = M.kachel("wald", kante, 0)
    check("zweiter Abruf liefert DASSELBE Objekt", erst is zweit)
    check("nach dem zweiten Abruf genau EINE gespeicherte Kachel", M.gespeichert() == 1,
          str(M.gespeichert()))
    verschieden = [M.kachel("wald", kante, nummer).tobytes()
                   for nummer in range(M.varianten())]
    check("die %d Varianten sind wirklich verschieden" % M.varianten(),
          len(set(verschieden)) == M.varianten())
    M.leeren()
    neu_eins = M.kachel("wald", kante, 1).tobytes()
    M.leeren()
    neu_zwei = M.kachel("wald", kante, 1).tobytes()
    check("gleiche Eingabe, pixelgleiches Bild (Determinismus)", neu_eins == neu_zwei)
    check("variante_fuer ist eine Zahl im Bereich", all(
        0 <= M.variante_fuer(x, y) < M.varianten() for x in range(20) for y in range(20)))

    abschnitt("6. Unbekannte Art und zu kleine Kante sind Fehler, kein Ersatzbild")
    for name, ruf in (("unbekannte Art in kachel()", lambda: M.kachel("wueste", 32)),
                      ("zu kleine Kante in kachel()", lambda: M.kachel("wald", 2))):
        try:
            ruf()
        except M.MalereiFehler:
            check(name + " -> MalereiFehler", True)
        except Exception as fehler:
            check(name + " -> MalereiFehler", False, "falsche Ausnahme: %r" % (fehler,))
        else:
            check(name + " -> MalereiFehler", False, "es kam gar keine Ausnahme")

    abschnitt("7. Die ganze Karte ist EIN Bild mit den Massen des Rasters")
    raster = portalraum.weltbild("d01")["raster"]
    zeilen, spalten = len(raster), len(raster[0])
    check("Raster ist 20 x 20", (zeilen, spalten) == (20, 20), "%d x %d" % (zeilen, spalten))
    for kante_probe in (20, 48):
        M.leeren()
        karte = M.karte_malen(raster, kante_probe)
        check("Karte bei %d px je Feld ist %d x %d" % (kante_probe, spalten * kante_probe,
                                                       zeilen * kante_probe),
              karte.size == (spalten * kante_probe, zeilen * kante_probe), str(karte.size))
        gleiche = M.karte_malen(raster, kante_probe)
        check("zweiter Aufruf liefert DASSELBE Kartenobjekt (%d px)" % kante_probe,
              gleiche is karte)
        check("alle sieben Arten stehen im Raster",
              set(art for zeile in raster for art in zeile) == set(arten))
        farben = _farben(karte)
        check("Karte bei %d px hat mehr als 1000 Farben (gemalt)" % kante_probe,
              len(farben) > 1000, "%d Farben" % len(farben))
        # Feldmitte muss die Gelaendefarbe treffen - sonst zeigt der Klick ein anderes Feld.
        # F-34 (Daniel, 09.11.2026): die Karte wird mit `M.HELLIGKEIT` aufgehellt; der Sollwert wird
        # mitgerechnet, die Schwelle bleibt bei 60.
        abweichungen = []
        for y in (0, 7, 13, 19):
            for x in (0, 5, 12, 19):
                soll = tuple(min(255, int(round(k * M.HELLIGKEIT)))
                             for k in M._rgb(gelaende.farbe(raster[y][x])))
                ist = karte.getpixel((x * kante_probe + kante_probe // 2,
                                      y * kante_probe + kante_probe // 2))
                abweichungen.append(_abstand(ist, soll))
        check("Feldmitten liegen an ihrer Gelaendefarbe (%d px)" % kante_probe,
              max(abweichungen) < 60, "groesste Abweichung %.1f" % max(abweichungen))

    abschnitt("8. Unbekannte Gelaendeart im Raster wird abgelehnt")
    kaputt = [list(zeile) for zeile in raster]
    kaputt[3][4] = "wueste"
    try:
        M.karte_malen(kaputt, 20)
    except M.MalereiFehler as fehler:
        check("unbekannte Art im Raster -> MalereiFehler", "wueste" in str(fehler), str(fehler))
    except Exception as fehler:
        check("unbekannte Art im Raster -> MalereiFehler", False, "falsche Ausnahme: %r" % (fehler,))
    else:
        check("unbekannte Art im Raster -> MalereiFehler", False, "es kam gar keine Ausnahme")
    try:
        M.karte_malen([], 20)
    except M.MalereiFehler:
        check("leeres Raster -> MalereiFehler", True)
    except Exception as fehler:
        check("leeres Raster -> MalereiFehler", False, "falsche Ausnahme: %r" % (fehler,))
    else:
        check("leeres Raster -> MalereiFehler", False, "es kam gar keine Ausnahme")

    abschnitt("9. Das Werkzeug der Testkarte misst denselben Weg (ohne Fenster)")
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import testkarte_fenster as werkzeug
    messung = werkzeug.messen("d01", 20)
    check("Werkzeug liefert ein Bild in Rastergroesse",
          messung["bild"].size == (20 * 20, 20 * 20), str(messung["bild"].size))
    check("Werkzeug zaehlt alle sieben Gelaendearten",
          len(messung["arten"]) == 7, str(sorted(messung["arten"])))
    check("Werkzeug meldet das zwischengespeicherte Bild als dasselbe Objekt",
          messung["gleiches_bild"] is True)
    check("Werkzeug nennt kalt und warm in Sekunden",
          messung["kalt"] > 0 and 0 <= messung["warm"] <= messung["kalt"],
          "kalt %.3f, warm %.5f" % (messung["kalt"], messung["warm"]))
    text = werkzeug.bericht(messung)
    check("Werkzeugbericht nennt die Weltkarte und die Kantenlaenge",
          "d01" in text and "20 px" in text)

    abschnitt("10. Messwerte (Beleg fuer D-3, kein Urteil)")
    import time
    M.leeren()
    beginn = time.perf_counter()
    M.karte_malen(raster, 20)
    kalt = time.perf_counter() - beginn
    beginn = time.perf_counter()
    M.karte_malen(raster, 20)
    warm = time.perf_counter() - beginn
    check("erste gemalte Karte bei 20 px unter 3 s", kalt < 3.0, "%.3f s" % kalt)
    check("zweiter Abruf unter 20 ms", warm < 0.020, "%.4f s" % warm)
    befund("Malzeit haengt an der Kante: 20 px %.3f s, 48 px gemessen im Werkzeug "
           "(tools/testkarte_fenster.py)" % kalt)
    return bericht()


if __name__ == "__main__":
    raise SystemExit(main())
