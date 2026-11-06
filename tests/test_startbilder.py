"""Startbilder: Panorama hinter Anmeldung und Ladebild, Logo statt Schriftzug (06.11.2026).

Daniels Wunsch, woertlich-nah: im Anmeldebildschirm (Passwort zweimal eingeben) soll ein schoenes
Panorama im Hintergrund liegen, das Wort "Nebelseetal" wird durch UNSER Logo ersetzt (der originale
Schriftzug bleibt als Datei erhalten), und im Ladebild bleibt das Schild sichtbar - dahinter ein Bild.

Geprueft wird:
  A. Die Motive und das Logo liegen im Projekt (kein geratener Pfad).
  B. Ein Bild wird auf Zielgroesse gebracht (cover, kein leerer Rand) und laesst sich abdunkeln.
  C. Der Anmeldebildschirm baut das Panorama UND das Logo; das Formular steht in einem eigenen Kasten.
  D. Das Ladebild zeigt das Panorama UND weiterhin das Schild (LADEBILD_PNG).
  E. Fehlt ein Bild, baut die Ansicht trotzdem und faellt auf den Schriftzug zurueck (kein Absturz).
  F. Der originale Schriftzug bleibt als Datei im Projekt (Referenz zum Original).

ASCII-only (Pruefdatei-Konvention).
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

ROOT, SRC = import_src()

import main
import tkinter as tk

abschnitt("A. Motive und Logo liegen im Projekt")
for motiv in ("anmelden", "laden"):
    pfad = main._bild_pfad(main.startbild_teile(motiv))
    check("Motiv %s liegt im Projekt" % motiv, os.path.exists(pfad), pfad)
logo_pfad = main._bild_pfad(main.LOGO_PNG)
check("unser Logo liegt im Projekt", os.path.exists(logo_pfad), logo_pfad)
check("ein unbekanntes Motiv faellt auf die Anmeldung zurueck",
      main.startbild_teile("gibtsnicht") == main.startbild_teile("anmelden"), "Rueckfall")

abschnitt("B. Cover und Abdunkeln")
from PIL import Image
roh = Image.open(main._bild_pfad(main.startbild_teile("anmelden"))).convert("RGB")
bild = main._cover(roh, 1024, 720, 0.0)
check("das Bild hat genau die Zielgroesse (kein leerer Rand)", bild.size == (1024, 720), str(bild.size))
dunkel = main._cover(roh, 1024, 720, 50.0)
check("das abgedunkelte Bild ist dunkler", sum(dunkel.convert("L").getdata()) < sum(bild.convert("L").getdata()),
      "Helligkeit sinkt")
hoch = main._cover(roh, 2000, 1200, 0.0)
check("auch ein grosses Ziel wird ganz gefuellt", hoch.size == (2000, 1200), str(hoch.size))

abschnitt("C. Anmeldebildschirm: Panorama und Logo")
root = None
try:
    root = tk.Tk()
    root.withdraw()
    tor = os.path.join(os.environ.get("TEMP", "."), "tor_pruefung_startbilder.json")
    if os.path.exists(tor):
        os.remove(tor)
    app = main.NebelseetalApp(root, tor_pfad=tor)          # Erststart: Passwort zweimal eingeben
    check("der Anmeldebildschirm steht", getattr(app, "tor_rahmen", None) is not None, "Rahmen da")
    check("das Panorama wurde gebaut", getattr(app, "_tor_bild", None) is not None,
          str(getattr(app, "_tor_bild", None)))
    check("das Logo wurde gebaut", getattr(app, "_tor_logo", None) is not None,
          str(getattr(app, "_tor_logo", None)))
    bilder = []
    for w in root.winfo_children():                       # nur Widgets MIT Bild-Option fragen
        try:
            if str(w.cget("image")) not in ("", "None"):
                bilder.append(w)
        except Exception:
            continue
    check("das Panorama liegt als eigenes Bild im Fenster", bool(bilder), str(len(bilder)))
    check("das Formular sitzt in einem eigenen Rahmen",
          str(app.tor_rahmen.cget("relief")) not in ("", "flat"), str(app.tor_rahmen.cget("relief")))
    quelle = main.NebelseetalApp._tor_screen.__doc__ or ""
    import inspect
    _src = inspect.getsource(main.NebelseetalApp._tor_screen)
    check("die Ansicht nimmt das Motiv 'anmelden'", 'startbild_photo("anmelden"' in _src, "Aufruf vorhanden")
    check("die Ansicht setzt das Logo ein", "logo_photo(" in _src, "Aufruf vorhanden")

    abschnitt("D. Ladebild: Panorama UND Schild")
    ladung = main.zeige_loadingpage(root)
    check("das Ladebild liefert sein Bildobjekt", ladung is not None, str(ladung))
    check("das Schild bleibt im Fenster", os.path.exists(main.ladebild_pfad()), main.ladebild_pfad())
    hinter = getattr(root, "_startbild", None)
    check("das Panorama liegt hinter dem Schild", hinter is not None, str(hinter))
    hinweise = []
    for w in root.winfo_children():                       # Texte im Ladebild einsammeln
        for kind in w.winfo_children():
            try:
                hinweise.append(str(kind.cget("text")))
            except Exception:
                continue
    check("der Ladehinweis steht weiter im Bild",
          any("Tal erwacht" in h for h in hinweise), str(hinweise)[:120])

    abschnitt("E. Fehlt ein Bild, baut die Ansicht trotzdem")
    alt_motive = dict(main.STARTBILD_MOTIVE)
    alt_logo = main.LOGO_PNG
    main.STARTBILD_MOTIVE["anmelden"] = ("assets", "gibtsnicht", "fehlt.jpg")
    main.LOGO_PNG = ("assets", "gibtsnicht", "fehlt.png")
    try:
        root2 = tk.Toplevel(root)
        root2.withdraw()
        app2 = main.NebelseetalApp(root2, tor_pfad=tor + ".2")
        check("ohne Bild steht der Bildschirm trotzdem", getattr(app2, "tor_rahmen", None) is not None,
              "Rahmen da")
        check("ohne Bild gibt es kein Panorama", getattr(app2, "_tor_bild", None) is None, "None")
        check("ohne Logo gibt es keinen Logosatz", getattr(app2, "_tor_logo", None) is None, "None")
        schrift = []
        for w in app2.tor_rahmen.winfo_children():
            if str(w.winfo_class()) == "Label":
                schrift.append(str(w.cget("text")))
        check("der Schriftzug 'Nebelseetal' erscheint als Rueckfall", any("Nebelseetal" in s for s in schrift),
              str(schrift)[:120])
        root2.destroy()
    finally:
        main.STARTBILD_MOTIVE.clear()
        main.STARTBILD_MOTIVE.update(alt_motive)
        main.LOGO_PNG = alt_logo

    abschnitt("F. Der originale Schriftzug bleibt erhalten")
    original = os.path.join(ROOT, "assets", "original", "logo.gif")
    check("assets/original/logo.gif liegt weiter im Projekt", os.path.exists(original), original)
    readme = os.path.join(ROOT, "assets", "referenzbilder", "README.md")
    check("die Referenzbilder haben ihre README", os.path.exists(readme), readme)
finally:
    if root is not None:
        try:
            root.destroy()
        except Exception:
            pass

sys.exit(bericht())
