"""Pruefung der Ladeansicht (Titelbild) — Paket W4e, 05.10.2026.

Belegt drei Dinge:
  1. Das Titelbild liegt als ABGELEITETE PNG-Fassung bereit, und die beigelegte Originaldatei
     (`Nebelseetal_Loadingpage.jpg`) ist **unveraendert** geblieben (Groesse und Pruefsumme).
  2. Die Ladeansicht **zeichnet wirklich** — und wenn das Bild fehlt oder unlesbar ist, kommt
     eine ehrliche Textzeile statt einer leeren Flaeche oder eines Absturzes.
  3. Sie **raeumt sich selbst weg**: bevor das Passworttor kommt, ist kein Ladefenster mehr da
     (die Ladeansicht darf nie im Spiel haengen bleiben).

Aufruf:  python -X utf8 tests/test_loadingpage.py
"""
from __future__ import annotations

import hashlib
import os
import struct
import sys
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, befund, bericht, check, import_src

ROOT, SRC = import_src()
main = ausnahme("main importieren", lambda: __import__("main"))
if main is None:
    sys.exit(bericht())

ORIGINAL = os.path.join(ROOT, "assets", "quellbilder", "Nebelseetal_Loadingpage.jpg")
BEIGELEGT = os.path.join(ROOT, "assets", "loadingpage", "Nebelseetal_Loadingpage.png")

def alle_text(w):
    """Alle Beschriftungen eines Fensterbaums."""
    treffer = []
    for k in w.winfo_children():
        try:
            treffer.append(str(k.cget("text")))
        except Exception:
            pass
        treffer += alle_text(k)
    return treffer


abschnitt("1. Das Originalbild ist unveraendert geblieben")

check("die beigelegte Originaldatei liegt noch genau so da",
      os.path.exists(ORIGINAL) and os.path.getsize(ORIGINAL) == 32659,
      f"{os.path.getsize(ORIGINAL) if os.path.exists(ORIGINAL) else 'fehlt'} Byte")
with open(ORIGINAL, "rb") as f:
    pruefsumme = hashlib.sha256(f.read()).hexdigest()
check("ihre Pruefsumme ist unveraendert (Dateiinhalt unveraendert, nur in assets/quellbilder einsortiert)",
      pruefsumme == "66956b880e1346bf7c2bda831b0d147e66f7a923b93dff0b0a35eaa71947e12c",
      pruefsumme)

abschnitt("2. Die abgeleitete PNG-Fassung ist da und lesbar")

check("die PNG-Fassung existiert", os.path.exists(BEIGELEGT))
with open(BEIGELEGT, "rb") as f:
    rohdaten = f.read()
check("es ist wirklich ein PNG (Signatur)", rohdaten[:8] == b"\x89PNG\r\n\x1a\n")
breite, hoehe = struct.unpack(">II", rohdaten[16:24]) if len(rohdaten) > 24 else (0, 0)
check("das PNG hat die Masse des Originals (455 x 320)",
      (breite, hoehe) == (455, 320), f"{breite}x{hoehe}")
check("main.ladebild_pfad() zeigt genau auf diese Datei",
      os.path.normcase(os.path.abspath(main.ladebild_pfad()))
      == os.path.normcase(os.path.abspath(BEIGELEGT)), main.ladebild_pfad())
check("das Buendel nimmt den Ordner assets mit (dann reist die PNG in die EXE)",
      '("assets", "assets")' in open(os.path.join(ROOT, "tools", "build_exe.py"),
                                     encoding="utf-8").read())

abschnitt("3. Die Ladeansicht zeichnet wirklich")

root = tk.Tk()
root.withdraw()
gesammelt = []
root.report_callback_exception = lambda *a: gesammelt.append(a)
try:
    bild = main.zeige_loadingpage(root)
    root.update()
    check("das Titelbild wird geladen (kein Rueckfall auf Text)", bild is not None)
    check("es ist ein Tk-Bild mit der Breite des Originals", int(bild.width()) == 455,
          str(bild.width()))
    texte = alle_text(root)
    check("der Hinweis steht in der Ansicht",
          any("Das Tal erwacht" in t for t in texte), str(texte[:3]))
    check("der Fenstertitel nennt den Augenblick",
          "Augenblick" in str(root.title()), root.title())
    check("die Ladeansicht zeigt kein leeres Fenster (Bild ODER Text vorhanden)",
          bild is not None or any(t.strip() for t in texte))
    check("kein stiller tkinter-Fehler in der Ladeansicht", not gesammelt, str(gesammelt[:1]))

    abschnitt("4. Fehlt das Bild, kommt eine ehrliche Textzeile statt eines Absturzes")

    echter_pfad = main.ladebild_pfad
    main.ladebild_pfad = lambda: os.path.join(ROOT, "gibtesnicht.png")
    try:
        ersatz = main.zeige_loadingpage(root)
        root.update()
        texte = alle_text(root)
        b = ersatz
    finally:
        main.ladebild_pfad = echter_pfad
    check("ohne Bild kommt kein Absturz und kein Bildobjekt", b is None)
    check("stattdessen steht der Spielname als Text da",
          any("Nebelseetal" in t for t in texte), str(texte[:3]))
    check("der Hinweis steht auch im Rueckfall",
          any("Das Tal erwacht" in t for t in texte), str(texte[:3]))
    befund("Rueckfall", "ohne Titelbild zeigt die Ladeansicht nur Text — der Start wird nie "
                        "blockiert, es wird nie eine leere Flaeche gezeigt")

    abschnitt("5. Die Ladeansicht raeumt sich selbst weg")

    app = ausnahme("App bauen", lambda: main.NebelseetalApp(root))
    root.update()
    texte_jetzt = alle_text(root)
    check("nach dem Start ist kein Ladehinweis mehr im Fenster",
          not any("Das Tal erwacht" in t for t in texte_jetzt),
          str([t for t in texte_jetzt if t][:3]))
    check("das Passworttor steht stattdessen (Passwort-Feld oder Einrichtung)",
          hasattr(app, "tor_rahmen") and bool(app.tor_rahmen.winfo_children()),
          str(hasattr(app, "tor_rahmen")))
    check("kein stiller tkinter-Fehler beim Uebergang zur Lade-/Toransicht",
          not gesammelt, str(gesammelt[:1]))
finally:
    try:
        root.destroy()
    except Exception:
        pass

sys.exit(bericht())
