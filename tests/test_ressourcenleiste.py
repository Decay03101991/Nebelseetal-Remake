# -*- coding: ascii -*-
"""Ressourcenleiste im Kopf (C2-Lieferung, Register 121).

Die Lieferung bringt ein gemaltes Leistenbild (1440x140) mit acht Symbolen und acht FREIEN
Zahlenplaketten. Das Spiel schreibt die Werte als eigene Textebene darueber - hell, mit dunkler
Kontur (Vorgabe der LIEFERUNG.md). Diese Datei prueft drei Dinge:

1. **Die Datendatei ist die eine Quelle.** `data/ressourcenleiste.json` nennt Bild, Masse, die
   acht Felder mit ihren Mittelpunkten in Pixeln bei 1440x140 und die Farben. Reihenfolge wie in
   der Lieferung: Siedler, Nahrung, Holz, Stein, Erz, Gold, Mana, Kelch (im Spiel: Metall, Punkte).
2. **Eine Rechenstelle je Feld** (`main.leistenwert`): Siedler aus `state.population`, Punkte aus
   `state.punktestand()`, Rohstoffe aus `state.resources`. Kein Feld rechnet selbst.
3. **Keine Zahl doppelt im Kopf.** Seit die Leiste die MENGEN zeigt, gibt `main.kopfzeile_fuer`
   fuer die sechs Leisten-Rohstoffe nur noch die RATE aus; die drei Rohstoffe ohne Leistenfeld
   (Wolle, Leder, Pferde) behalten Menge und Rate.

Aufruf:  python -X utf8 tests/test_ressourcenleiste.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
import main  # noqa: E402

daten = main.RESSOURCENLEISTE
felder = daten.get("felder") or []

# ==========================================================================
abschnitt("1. Die Datendatei beschreibt die Leiste vollstaendig")

datei = os.path.join(ROOT, "data", "ressourcenleiste.json")
check("1 die Datendatei liegt im Projekt", os.path.exists(datei), datei)
check("1 main hat sie geladen", bool(daten), str(type(daten)))
check("1 die Leiste hat genau acht Felder", len(felder) == 8, str(len(felder)))
check("1 Reihenfolge wie in der Lieferung (Siedler, Nahrung, Holz, Stein, Erz, Gold, Mana, Kelch)",
      [f.get("schluessel") for f in felder] ==
      ["siedler", "nahrung", "holz", "stein", "erz", "gold", "mana", "punkte"],
      str([f.get("schluessel") for f in felder]))
check("1 jede Quelle ist ein bekannter Wert",
      all(str(f.get("quelle")) in ("bevoelkerung", "punkte", "holz", "stein", "metall", "mana",
                                   "nahrung", "gold") for f in felder),
      str([f.get("quelle") for f in felder]))
breite = int(daten.get("breite") or 0)
hoehe = int(daten.get("hoehe") or 0)
check("1 Originalmasse 1440x140 stehen in der Datei", (breite, hoehe) == (1440, 140), str((breite, hoehe)))
check("1 alle Mittelpunkte liegen IN der Leiste",
      all(0 < int(f.get("x") or 0) < breite and 0 < int(f.get("y") or 0) < hoehe for f in felder),
      str([(f.get("x"), f.get("y")) for f in felder]))
check("1 die Mittelpunkte sind aufsteigend (links nach rechts)",
      [int(f.get("x") or 0) for f in felder] == sorted(int(f.get("x") or 0) for f in felder),
      str([f.get("x") for f in felder]))
bildpfad = os.path.join(ROOT, str(daten.get("datei") or "").replace("/", os.sep))
check("1 das Leistenbild liegt im Projekt", os.path.exists(bildpfad), bildpfad)
check("1 Zahl- und Konturfarbe sind eingetragen",
      bool((daten.get("farben") or {}).get("zahl")) and bool((daten.get("farben") or {}).get("kontur")),
      str(daten.get("farben")))


# ==========================================================================
abschnitt("2. Eine Rechenstelle je Feld (leistenwert)")

class _Betrag:
    """Was `state.resources[...]` liefert: ein Objekt mit `amount`."""
    def __init__(self, menge):
        self.amount = menge


class _Zustand:
    """Minimaler Spielstand fuer die Wertepruefung."""
    def __init__(self):
        self.population = 12.0
        self.resources = {"holz": _Betrag(1234), "stein": _Betrag(7.5), "nahrung": _Betrag(0)}

    def punktestand(self):
        return {"forschung": 3, "krieg": 4, "gesamt": 12345}


_z = _Zustand()
check("2 Siedler kommen aus state.population",
      main.leistenwert(_z, {"schluessel": "siedler", "quelle": "bevoelkerung"}) == "12", "")
check("2 Punkte kommen aus punktestand()['gesamt'] mit Tausenderpunkt",
      main.leistenwert(_z, {"schluessel": "punkte", "quelle": "punkte"}) == "12.345",
      main.leistenwert(_z, {"schluessel": "punkte", "quelle": "punkte"}))
check("2 ein Rohstoff kommt aus state.resources",
      main.leistenwert(_z, {"schluessel": "holz", "quelle": "holz"}) == "1.234",
      main.leistenwert(_z, {"schluessel": "holz", "quelle": "holz"}))
check("2 Kommawerte werden auf ganze Zahlen gerundet",
      main.leistenwert(_z, {"schluessel": "stein", "quelle": "stein"}) == "8",
      main.leistenwert(_z, {"schluessel": "stein", "quelle": "stein"}))
check("2 ein fehlender Rohstoff ergibt 0 statt eines Absturzes",
      main.leistenwert(_z, {"schluessel": "gold", "quelle": "gold"}) == "0", "")


# ==========================================================================
abschnitt("3. Keine Zahl doppelt im Kopf (kopfzeile_fuer)")

check("3 genau die sechs Leisten-Rohstoffe zeigen nur die Rate",
      set(main.LEISTEN_ROHSTOFFE) == {"holz", "stein", "metall", "mana", "nahrung", "gold"},
      str(main.LEISTEN_ROHSTOFFE))


class _Leer:
    """Spielstand ohne Siedlungen: keine Ernte, kein Verbrauch."""
    population = 0.0
    resources = {"holz": _Betrag(55), "wolle": _Betrag(40), "leder": _Betrag(3), "pferde": _Betrag(2)}
    settlements = []

    def punktestand(self):
        return {"gesamt": 0}


_leer = _Leer()
ertrag = {"holz": 5.0, "wolle": 1.0}
text_holz, _w = main.kopfzeile_fuer(_leer, "holz", ertrag)
text_wolle, _w2 = main.kopfzeile_fuer(_leer, "wolle", ertrag)
check("3 Holz (auf der Leiste) zeigt die Rate ohne Betrag", "55" not in text_holz and "5/h" in text_holz,
      text_holz)
check("3 Wolle (nicht auf der Leiste) zeigt Betrag UND Rate", "40" in text_wolle and "1/h" in text_wolle,
      text_wolle)
import inspect as _inspect  # noqa: E402
_rate_code = _inspect.getsource(main.kopf_rate_text)
_zeile_code = _inspect.getsource(main.kopf_zeilen_text)
check("3 Rate und Zeile lesen dieselbe Verbrauchsquelle (spieloekonomie.verbrauch_pro_stunde)",
      "spieloekonomie.verbrauch_pro_stunde" in _rate_code
      and "spieloekonomie.verbrauch_pro_stunde" in _zeile_code, "")
check("3 keine der beiden Stellen baut eine eigene Verbrauchsformel",
      "NAHRUNG_JE_EINHEIT_TAG" not in _rate_code and "NAHRUNG_JE_EINHEIT_TAG" not in _zeile_code, "")


# ==========================================================================
abschnitt("4. Die Leiste steht wirklich im Kopf (echte Tk-Flaeche)")

import tkinter as tk  # noqa: E402

root = tk.Tk()
root.withdraw()
app = main.NebelseetalApp(root)
app._build_main_ui()
root.update()
canvas = getattr(app, "_leisten_canvas", None)
check("4 es gibt eine Leistenflaeche im Kopf", canvas is not None, str(canvas))
if canvas is not None:
    items = canvas.find_withtag("leiste")
    check("4 Bild und 40 Texte liegen darauf (8 Felder x 5 Texte)", len(items) == 41, str(len(items)))
    check("4 die Flaeche ist so hoch wie die Leiste (proportional)",
          int(canvas.winfo_height()) <= int(daten.get("hoehe") or 140) + 2,
          str(canvas.winfo_height()))
    texte = getattr(app, "_leisten_texte", {})
    check("4 alle acht Felder haben Textkennungen", len(texte) == 8, str(sorted(texte)))
    stimmt = True
    for feld in felder:
        kennungen = texte.get(str(feld.get("schluessel"))) or []
        soll = main.leistenwert(app.state, feld)
        for kennung in kennungen:
            if canvas.itemcget(kennung, "text") != soll:
                stimmt = False
    check("4 jede Zahl auf der Leiste stimmt mit dem Spielstand ueberein", stimmt, "")
    app.state.resources["holz"].amount = 4321
    app._leiste_aktualisieren()
    kennung = (texte.get("holz") or [None])[-1]
    check("4 eine Aenderung des Bestands kommt auf der Leiste an",
          kennung is not None and canvas.itemcget(kennung, "text") == "4.321",
          canvas.itemcget(kennung, "text") if kennung else "keine Kennung")
root.destroy()

# ==========================================================================
abschnitt("6. Der Balken wird laenger, die Symbole bleiben in Form (Befund Daniel 02.11.2026)")

try:
    from PIL import Image as _Image
    _pil = True
except Exception:                                        # noqa: BLE001
    _pil = False
    befund("Pillow fehlt - die Zusammensetzung wird nicht gemessen", "")

stuecke = main._leisten_stuecke(daten)
check("6 die Schnittliste hat feste Kacheln und dehnbare Luecken",
      any(s["art"] == "fest" for s in stuecke) and any(s["art"] == "dehnbar" for s in stuecke),
      str([s["art"] for s in stuecke]))
check("6 neun feste Teile (zwei Ecken und acht Felder)",
      sum(1 for s in stuecke if s["art"] == "fest") == 10,
      str(sum(1 for s in stuecke if s["art"] == "fest")))
check("6 die Stuecke decken die ganze Breite lueckenlos ab",
      stuecke[0]["von"] == 0 and stuecke[-1]["bis"] == breite
      and all(stuecke[i]["bis"] == stuecke[i + 1]["von"] for i in range(len(stuecke) - 1)),
      str([(s["von"], s["bis"]) for s in stuecke]))

if _pil:
    b1440, m1440, s1440 = main.leiste_zusammensetzen(daten, 1440)
    b1920, m1920, s1920 = main.leiste_zusammensetzen(daten, 1920)
    b2560, m2560, s2560 = main.leiste_zusammensetzen(daten, 2560)
    b3440, m3440, s3440 = main.leiste_zusammensetzen(daten, 3440)
    b1000, m1000, s1000 = main.leiste_zusammensetzen(daten, 1000)
    check("6 bei 1440 px gilt Skala 1,0 und die Originalhoehe",
          abs(s1440 - 1.0) < 1e-9 and b1440.height == 140, f"{s1440} / {b1440.height}")
    check("6 die Zielbreite wird immer genau getroffen",
          all(b.width == ziel for b, ziel in ((b1440, 1440), (b1920, 1920), (b2560, 2560), (b3440, 3440))),
          str([b.width for b in (b1440, b1920, b2560, b3440)]))
    # M-3 (Daniels Befund 02.11.2026: "die ressourcen bilder oben [sind] verzerrt"). ENTSCHEIDUNG
    # GEAENDERT, mit Begruendung: seit P-3 wuchs das ganze Band gleichmaessig bis Faktor 1,75. Daniel
    # hat die Symbole im maximierten Fenster trotzdem als verzerrt gesehen - die Symbolbilder sind
    # klein und wirken vergroessert unscharf. Neu (Modus 'kacheln'): das Band skaliert NIE ueber 1,0,
    # die zusaetzliche Breite entsteht durch WIEDERHOLUNG der gemalten Luecken. Die alte Wache nagelte
    # das Wachstum fest und wird deshalb umgestellt - nicht der Code zurueckgebogen.
    check("6 1920 px: die Symbole bleiben in Originalgroesse (Skala 1,0)",
          abs(s1920 - 1.0) < 1e-9 and b1920.height == 140,
          f"{s1920:.3f} / {b1920.height}")
    # P-3 (02.11.2026) - ENTSCHEIDUNG GEAENDERT, mit Begruendung: bis heute galt "oberhalb von
    # `skala_max` waechst NUR die Laenge" - die Luecken nahmen die ganze Restbreite auf und wurden
    # dabei bei 2560 px um Faktor 1,86 und bei 3440 px um 3,75 gestreckt; die gemalte Landschaft
    # zwischen den Symbolen wurde zu Streifen mit harten Naehten (Daniels Befund). Neu: das ganze Band
    # skaliert GLEICHMAESSIG weiter (treue Vergroesserung ohne Naht) bis `skala_hart`, die Luecken
    # bleiben auf `luecke_max` gedeckelt. Die alte Wache nagelte genau die Ursache fest und wird
    # deshalb umgestellt - nicht der Code zurueckgebogen.
    check("6 oberhalb der Originalbreite waechst NICHTS mehr (Skala bleibt 1,0)",
          abs(s2560 - 1.0) < 1e-9 and abs(s3440 - 1.0) < 1e-9,
          f"2560 {s2560:.3f} | 3440 {s3440:.3f}")
    check("6 die Hoehe bleibt die Originalhoehe (140 px)",
          b2560.height == 140 and b3440.height == 140, f"{b2560.height} / {b3440.height}")
    check("6 der Modus ist 'kacheln' (Wiederholung statt Dehnung)",
          str(daten.get("rest_auffuellen")) == "kacheln", str(daten.get("rest_auffuellen")))
    check("6 schmalere Fenster schrumpfen gleichmaessig (keine Dehnung)",
          abs(s1000 - 1000 / 1440) < 1e-6, f"{s1000:.3f}")

    # Verzerrungsprobe: die Kachel um Symbol 1 muss bei 2560 und 3440 IDENTISCH sein
    halb = int(daten["kachel_halbbreite"])
    m1a, m1b = m2560["siedler"], m3440["siedler"]
    ka = b2560.crop((m1a[0] - int(halb * s2560), 0, m1a[0] + int(halb * s2560), b2560.height))
    kb = b3440.crop((m1b[0] - int(halb * s3440), 0, m1b[0] + int(halb * s3440), b3440.height))
    # P-3 (02.11.2026): die alte Zusage "pixelgleich bei 2560 und 3440" gilt nicht mehr - das Band
    # waechst jetzt gleichmaessig weiter (Skala 1,65 bzw. 1,75), damit die Luecken nicht gestreckt
    # werden muessen. Die Zusage lautet jetzt: das Symbolfeld ist bei BEIDEN Breiten eine TREUE,
    # gleichmaessige Vergroesserung der Originalkachel - Seitenverhaeltnis unveraendert, keine
    # waagerechte Verzerrung. Beides wird gegen die Originalkachel gemessen, nicht behauptet.
    orig = _Image.open(os.path.join(ROOT, str(daten["datei"]).replace("/", os.sep))).convert("RGBA")
    x1 = int(daten["felder"][0]["x"])
    soll_seite = (2 * halb) / float(orig.height)                       # Seitenverhaeltnis der Originalkachel
    check("6 ein breites Band ist 140 px hoch und traegt die Kachel in Originalgroesse",
          b3440.height == 140 and abs(s3440 - 1.0) < 1e-9,
          f"{b3440.height} / {s3440:.3f}")
    for name, kachel, hoehe in (("2560", ka, b2560.height), ("3440", kb, b3440.height)):
        verhaeltnis = kachel.width / float(kachel.height)
        check(f"6 das Symbolfeld bei {name} px ist unverzerrt (Seitenverhaeltnis wie im Original)",
              abs(verhaeltnis - soll_seite) / soll_seite < 0.02,
              f"{verhaeltnis:.3f} gegen {soll_seite:.3f}")
        soll = orig.crop((x1 - halb, 0, x1 + halb, orig.height)).resize(kachel.size, _Image.LANCZOS)
        abweichung = sum(abs(p[0] - q[0]) + abs(p[1] - q[1]) + abs(p[2] - q[2])
                         for p, q in zip(soll.convert("RGBA").getdata(), kachel.convert("RGBA").getdata())
                         ) / max(1, kachel.width * kachel.height * 3)
        check(f"6 das Symbolfeld bei {name} px ist die gleichmaessig skalierte Originalkachel (Abweichung < 8)",
              abweichung < 8, f"{abweichung:.2f}")

# Quelltext-Wachen: eine Stelle fuer Aufbau und Neuzeichnen
import inspect  # noqa: E402
quelle = inspect.getsource(main)
check("5 Aufbau und Neuzeichnen benutzen dieselbe Hilfsfunktion",
      quelle.count("kopfzeile_fuer(self.state, r, ertrag_jetzt)") == 2,
      "Treffer: %d" % quelle.count("kopfzeile_fuer(self.state, r, ertrag_jetzt)"))
check("5 die Leiste wird im Kopf gebaut und im Takt aktualisiert",
      "_leiste_bauen(top)" in quelle and "self._leiste_aktualisieren()" in quelle, "")
befund("Die Leiste selbst ist hier nicht gemalt - die Vorschau "
       "docs/audits/ressourcenleiste_vorschau_20261102.png zeigt die Werte in den Plaketten", "")

sys.exit(bericht())
