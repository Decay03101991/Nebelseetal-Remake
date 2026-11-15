# -*- coding: ascii -*-
"""Wache F5: das Schild wird eingepasst statt in Dateigroesse geladen (15.11.2026, Sitzung 46).

WOHER DIE AUFGABE KOMMT
-----------------------
B5 des Bildbedarfs (docs/BILDBEDARF_ENTSCHEIDUNGEN_20261113.md, Abschnitt 2) liefert die
Startbilder im Dezember in 4x: Anzeige 1024 x 720, Datei 4096 x 2880. Fuer das Schild
(`LADEBILD_PNG`) standen dafuer noch ZWEI offene Stellen - die Ladeansicht und der Hintergrund
der Speicher-Nebenfenster. `tk.PhotoImage` skaliert NICHT; ein 4096er-Bild kaeme in Dateigroesse
ins Fenster (gemessen 15.11.2026: Ladeansicht 1024 x 720, Datei 455 x 320).

WAS DIESE DATEI PRUEFT
----------------------
1. Heute aendert sich NICHTS: die 455 x 320-Datei erscheint in beiden Feldern in ihrer Groesse,
   und das Feld des Nebenfensters wird AM Dialog gemessen (980 x 475 -> 490 x 427).
2. Eine 4096 x 2880-Probe (B5-Mass) kommt durch BEIDE Wege auf Feldgroesse (Pillow und
   Tk-subsample), das Seitenverhaeltnis bleibt, das Feld wird nicht ueberschritten.
3. Die echte Ladeansicht bleibt 1024 x 720, das Feld ist dort 512 x 648, und keine Bildflaeche
   ist breiter als das Fenster.
4. Fehlt die Datei, kommt None und die Ladeansicht zeigt ihren Text.
5. Quellwachen: beide Stellen gehen ueber `ladebild_photo(ladebild_feld(...))`.

Aufruf:  python -X utf8 tests/test_f5_ladebild_groesse.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------  # noqa: E501
PRUEF_ART = "fenster"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['main:*']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import inspect
import os
import struct
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src  # noqa: E402

ROOT, SRC = import_src()
import tkinter as tk  # noqa: E402
import main as M  # noqa: E402

DATEI = M.ladebild_pfad()
FELD_LADE = (512, 648)          # 1024 x 720 gemessen x (0.5, 0.9) - Erwartung, nicht Vorgabe
FELD_DIALOG = (490, 427)        # 980 x 475 gemessen x (0.5, 0.9)
B5 = (4096, 2880)               # Dezember-Mass aus dem Bildbedarf


def masse(bild):
    """Die gezeigten Masse eines Tk-Bildes (oder None)."""
    if bild is None:
        return None
    return (int(bild.width()), int(bild.height()))


def png_masse(pfad):
    """Breite und Hoehe direkt aus dem PNG-Kopf - ohne Zusatzpaket."""
    with open(pfad, "rb") as f:
        kopf = f.read(24)
    if kopf[:8] != b"\x89PNG\r\n\x1a\n":
        return (0, 0)
    return struct.unpack(">II", kopf[16:24])


def probe_schreiben(pfad, breite, hoehe):
    """Eine Probebild-Datei erzeugen. False, wenn kein Pillow da ist."""
    try:
        from PIL import Image
        Image.new("RGB", (int(breite), int(hoehe)), (12, 34, 56)).save(pfad)
        return True
    except Exception:                                                 # noqa: BLE001
        return False


def bildflaechen(w):
    """Alle Widgets mit einer Bild-Option im Fensterbaum."""
    treffer = []
    for kind in w.winfo_children():
        try:
            if str(kind.cget("image")):
                treffer.append(kind)
        except Exception:                                             # noqa: BLE001
            pass
        treffer += bildflaechen(kind)
    return treffer


def alle_texte(w):
    """Alle Beschriftungen im Fensterbaum."""
    treffer = []
    for kind in w.winfo_children():
        try:
            treffer.append(str(kind.cget("text")))
        except Exception:                                             # noqa: BLE001
            pass
        treffer += alle_texte(kind)
    return treffer


tmp = tempfile.mkdtemp(prefix="f5_")
GROSS = os.path.join(tmp, "probe_4096x2880.png")
probe_da = probe_schreiben(GROSS, *B5)
echter_pfad = M.ladebild_pfad

root = tk.Tk()
root.withdraw()

# ==========================================================================
abschnitt("1. Heute aendert sich nichts: die 455 x 320-Datei bleibt so gross")
# ==========================================================================
check("1 die Ladebild-Datei liegt im Projekt", os.path.isfile(DATEI), DATEI)
check("1 ihre Masse sind 455 x 320 (gemessen am PNG-Kopf)",
      png_masse(DATEI) == (455, 320), str(png_masse(DATEI)))
heute = masse(M.ladebild_photo(FELD_LADE, master=root))
check("1 die heutige Datei erscheint im Feld der Ladeansicht unveraendert (455 x 320)",
      heute == (455, 320), str(heute))
check("1 der Rueckfall vergroessert nie (kleiner als das Feld bleibt kleiner)",
      heute == (455, 320) and heute != FELD_LADE, str(heute))

dialog = tk.Toplevel(root)
dialog.geometry("980x475")
dialog.update_idletasks()
check("1 das Feld des Nebenfensters wird AM Dialog gemessen (980 x 475 -> 490 x 427)",
      M.ladebild_feld(dialog) == FELD_DIALOG, str(M.ladebild_feld(dialog)))
heute_dialog = masse(M.ladebild_photo(M.ladebild_feld(dialog), master=dialog))
check("1 auch hinter dem Nebenfenster bleibt die heutige Datei 455 x 320",
      heute_dialog == (455, 320), str(heute_dialog))
dialog.destroy()

# ==========================================================================
abschnitt("2. Eine 4096 x 2880-Probe (B5) wird eingepasst - auf beiden Wegen")
# ==========================================================================
if not probe_da:
    check("2 Probebild schreiben (Pillow)", False, "kein Pillow - nicht pruefbar")
else:
    check("2 die Probe ist wirklich 4096 x 2880", png_masse(GROSS) == B5, str(png_masse(GROSS)))
    M.ladebild_pfad = lambda: GROSS
    try:
        gross_lade = masse(M.ladebild_photo(FELD_LADE, master=root))
        gross_dialog = masse(M.ladebild_photo(FELD_DIALOG, master=root))
    finally:
        M.ladebild_pfad = echter_pfad
    check("2 im Feld der Ladeansicht bleibt die 4096er-Datei im Feld (512 x 360)",
          gross_lade == (512, 360), str(gross_lade))
    check("2 im Feld des Nebenfensters bleibt sie im Feld (490 x 345)",
          gross_dialog == (490, 345), str(gross_dialog))
    check("2 beide Ergebnisse liegen INNERHALB ihres Feldes",
          gross_lade[0] <= FELD_LADE[0] and gross_lade[1] <= FELD_LADE[1]
          and gross_dialog[0] <= FELD_DIALOG[0] and gross_dialog[1] <= FELD_DIALOG[1],
          "%s / %s" % (gross_lade, gross_dialog))
    verhaeltnis_datei = B5[0] / float(B5[1])
    verhaeltnis_bild = gross_lade[0] / float(gross_lade[1])
    check("2 das Seitenverhaeltnis bleibt erhalten (kein Zerren)",
          abs(verhaeltnis_datei - verhaeltnis_bild) < 0.01,
          "%.3f gegen %.3f" % (verhaeltnis_datei, verhaeltnis_bild))
    # zweiter Weg: OHNE Pillow (subsample). Der ImportError wird erzwungen, nicht nachgebaut.
    echte_pil = sys.modules.get("PIL")
    sys.modules["PIL"] = None
    try:
        M.ladebild_pfad = lambda: GROSS
        ohne_pil = masse(M.ladebild_photo(FELD_LADE, master=root))
        M.ladebild_pfad = echter_pfad                 # und die ECHTE Datei im selben Zustand
        ohne_pil_heute = masse(M.ladebild_photo(FELD_LADE, master=root))
    finally:
        M.ladebild_pfad = echter_pfad
        if echte_pil is not None:
            sys.modules["PIL"] = echte_pil
        else:
            sys.modules.pop("PIL", None)
    check("2 der Tk-Rueckfall (subsample) bringt die 4096er-Datei auf 512 x 360",
          ohne_pil == (512, 360), str(ohne_pil))
    check("2 der Tk-Rueckfall laesst die heutige Datei unangetastet (455 x 320)",
          ohne_pil_heute == (455, 320), str(ohne_pil_heute))

# ==========================================================================
abschnitt("3. Die echte Ladeansicht sprengt das Fenster nicht")
# ==========================================================================
root.deiconify()                        # gemessen wird am SICHTBAREN Fenster (Tk-Quirk: ein
root.update()                           # verstecktes Fenster meldet 200 x 200, gemessen 15.11.)
erst = masse(M.zeige_loadingpage(root))
root.update()
breite_fenster, hoehe_fenster = int(root.winfo_width()), int(root.winfo_height())
check("3 die Ladeansicht ist 1024 x 720", (breite_fenster, hoehe_fenster) == (1024, 720),
      "%s x %s" % (breite_fenster, hoehe_fenster))
check("3 das Feld der Ladeansicht ist am Fenster gemessen (1024 x 720 -> 512 x 648)",
      M.ladebild_feld(root) == FELD_LADE, str(M.ladebild_feld(root)))
check("3 das Schild der heutigen Datei ist 455 x 320", erst == (455, 320), str(erst))
breiten = [int(k.winfo_width()) for k in bildflaechen(root)]
check("3 keine Bildflaeche ist breiter als das Fenster",
      all(b <= breite_fenster for b in breiten), str(breiten))

if probe_da:
    M.ladebild_pfad = lambda: GROSS
    try:
        gross = masse(M.zeige_loadingpage(root))
        root.update()
        jetzt = (int(root.winfo_width()), int(root.winfo_height()))
        breiten_gross = [int(k.winfo_width()) for k in bildflaechen(root)]
    finally:
        M.ladebild_pfad = echter_pfad
    check("3 mit der 4096er Probe bleibt das Fenster 1024 x 720", jetzt == (1024, 720), str(jetzt))
    check("3 das Schild kommt als 512 x 360 in die Ansicht", gross == (512, 360), str(gross))
    check("3 auch mit der 4096er Probe ist keine Bildflaeche breiter als das Fenster",
          all(b <= 1024 for b in breiten_gross), str(breiten_gross))
    befund("F5", "4096 x 2880 wird auf 512 x 360 eingepasst - ohne diese Wache kaeme das Bild "
                 "in Dateigroesse (4096 px) in ein 1024 px breites Fenster")

# ==========================================================================
abschnitt("4. Fehlt die Datei, bleibt der Text - kein Absturz, kein leeres Fenster")
# ==========================================================================
M.ladebild_pfad = lambda: os.path.join(tmp, "gibtsnicht.png")
try:
    ohne = M.zeige_loadingpage(root)
    root.update()
finally:
    M.ladebild_pfad = echter_pfad
check("4 ohne Datei kommt kein Bildobjekt", ohne is None, str(ohne))
texte = alle_texte(root)
check("4 der Ladehinweis steht weiter im Fenster",
      any("Tal erwacht" in t for t in texte), str(texte[:4]))
check("4 der Spielname steht als Text da",
      any("Nebelseetal" in t for t in texte), str(texte[:4]))
try:
    root.destroy()
except Exception:                                                     # noqa: BLE001
    pass

# ==========================================================================
abschnitt("5. Quellwachen: beide Stellen laden ueber ladebild_photo")
# ==========================================================================
lade_quelle = inspect.getsource(M.zeige_loadingpage)
dialog_quelle = inspect.getsource(M.NebelseetalApp._schild_dialog_inhalt)
check("5 die Ladeansicht gibt die Fenstergroesse mit, statt sie zu raten",
      "ladebild_feld(root, _breit, _hoch)" in lade_quelle, "Fenstergroesse uebergeben")
check("5 die Ladeansicht laedt ueber ladebild_photo",
      "ladebild_photo(feld, master=root)" in lade_quelle, "Aufruf vorhanden")
check("5 die Ladeansicht laedt das Schild nicht mehr roh in Dateigroesse",
      "tk.PhotoImage(file=pfad" not in lade_quelle, "kein Roh-Laden")
check("5 das Nebenfenster ruft ladebild_photo mit ladebild_feld",
      "ladebild_photo(ladebild_feld(fenster)" in dialog_quelle, "Aufruf vorhanden")
check("5 das Nebenfenster laedt das Schild nicht mehr roh in Dateigroesse",
      "tk.PhotoImage(file=pfad" not in dialog_quelle, "kein Roh-Laden")
check("5 jede Stelle laedt genau EINMAL ueber den Helfer",
      lade_quelle.count("ladebild_photo(") == 1 and dialog_quelle.count("ladebild_photo(") == 1,
      "%d / %d" % (lade_quelle.count("ladebild_photo("), dialog_quelle.count("ladebild_photo(")))
check("5 das Feld ist eine Layout-Entscheidung, kein Dateimass (0.5 / 0.9)",
      (M.LADEBILD_FELD_BREITE, M.LADEBILD_FELD_HOEHE) == (0.5, 0.9),
      "%s / %s" % (M.LADEBILD_FELD_BREITE, M.LADEBILD_FELD_HOEHE))
befund("F5", "das Schild geht an beiden Stellen ueber ladebild_photo(ladebild_feld(...)) - "
             "eine Quelle fuer Feld und Einpassen")

sys.exit(bericht())
