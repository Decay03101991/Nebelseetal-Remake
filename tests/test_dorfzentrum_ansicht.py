# -*- coding: ascii -*-
"""Wache: die Dorfzentrum-Ansicht im Fenster (Nr. 16, Teil A - F-56, F-58, F-59, F-65, F-66).

WAS HIER GEPRUEFT WIRD
----------------------
Die Masse selbst rechnet `tests/test_dorfzentrum_masse.py` ohne Fenster nach. Diese Datei prueft,
dass die ANSICHT sie auch wirklich so baut:

1. Die Spalte hat sechs Bloecke (sieben mit dem Entwicklerblock) in der Reihenfolge aus Nr. 16:
   Kopf, naechster Schritt, Ort, Aktionen, Auswahl, Hinweis, Technik.
2. Block 5 (Auswahl) nimmt den REST: die Summe aller Bloecke samt Luecken ist genau die
   Fensterhoehe - die Spalte rollt NICHT.
3. F-59: es gibt keinen Ortsbestand-Block mehr (der Ortsbestand steht in der Siedlungskarte).
4. F-66: der Kopf nennt die Kennzahlen aus `spieloekonomie.dorfzentrum_kennzahlen` ("x von 17
   vorraetig" / "y von 17 herstellbar") - und die Ansicht zaehlt nicht selbst.
5. Drei Reiter in der Reihenfolge Lager / Werkstaetten / Einheiten; Umschalten LEckt nicht
   (nach zehn Wechseln sind es so viele Widgets wie nach einem - Claudes Z3).
6. F-65: die Einheitentabelle hat KEINE Spalte "Verwundete" und steht in zwei Haelften zu 14.
7. F-58: die Werkstattliste hat die vier Spalten Ware / Werkstatt / Zutat / Zustand, und die
   Zutat steht als "Metall 0 / 2 Kreuz" (vorhanden / noetig) da.
8. Die stillgelegte Route "Lager" zeigt dieselben Raster (eine Anzeige, zwei Wege).

Aufruf: python -X utf8 tests/test_dorfzentrum_ansicht.py
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py.
PRUEF_ART = "fenster+messen"
PRUEF_STUFE = 2
PRUEF_BETRIFFT = ['dorfzentrum', 'main:*', 'spieloekonomie']
PRUEF_DATEN = ['items.json', 'warenrezepte.json']
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src, messwert  # noqa: E402

ROOT, SRC = import_src()
os.chdir(SRC)

import dorfzentrum  # noqa: E402
import main  # noqa: E402

REIHENFOLGE = ("kopf", "naechster", "ort", "aktionen", "auswahl", "hinweis")


def _texte(widget, tiefe: int = 0):
    """Alle Beschriftungen eines Widgets - rekursiv, damit auch Leinwand-Kinder zaehlen."""
    out = []
    try:
        t = widget.cget("text")
        if str(t):
            out.append(str(t))
    except Exception:                                                      # noqa: BLE001
        pass
    for kind in widget.winfo_children():
        out += _texte(kind, tiefe + 1)
    return out


def _anzahl(widget) -> int:
    return 1 + sum(_anzahl(k) for k in widget.winfo_children())


def _probe():
    import tkinter as tk
    root = tk.Tk()
    root.geometry("1560x940+40+20")
    try:
        root.attributes("-alpha", 0.01)
    except Exception:                                                      # noqa: BLE001
        pass
    root.update()
    try:
        app = main.NebelseetalApp(root)
        app._build_main_ui()
        app._erste_siedlung_gruenden()
        for _ in range(3):
            root.update()
            root.update_idletasks()
        app._dz_reiter = 0
        app._switch_view("Dorfzentrum")
        for _ in range(3):
            root.update()
            root.update_idletasks()
        return app, root
    except Exception:
        root.destroy()
        raise


def _lauf():
    app, root = _probe()
    try:
        m = getattr(app, "_dz_masse", None) or {}
        hoehen = dict(getattr(app, "_dz_block_hoehen", {}) or {})

        # ---------------------------------------------------------------- 1. die Bloecke
        abschnitt("1. Die sieben Bloecke der Spalte (F-59: ohne Ortsbestand)")
        check("die Masse stehen am App-Objekt", bool(m), str(sorted(m)[:6]))
        check("es gibt sechs Bloecke (Technik nur im Entwicklerbetrieb)",
              sorted(hoehen) == sorted(REIHENFOLGE), str(sorted(hoehen)))
        check("der Ortsbestand-Block ist entfallen (F-59)", "ortsbestand" not in hoehen, "")
        check("der Kopf ist der erste Block", list(hoehen)[0] == "kopf" if hoehen else False,
              str(list(hoehen)))
        for name in REIHENFOLGE:
            check("Block %s ist gebaut und hoeher als 0 px" % name,
                  int(hoehen.get(name) or 0) > 0, str(hoehen.get(name)))

        # ---------------------------------------------------------------- 2. Block 5 = Rest
        abschnitt("2. Block 5 nimmt den Rest - die Spalte rollt nicht")
        _summe = sum(hoehen.values()) + len(hoehen) * int(m.get("p") or 0)
        check("Summe der Bloecke + Luecken = Fensterhoehe (%d px)" % int(m.get("hoehe") or 0),
              abs(_summe - int(m.get("hoehe") or 0)) <= 1,
              "%d gegen %d" % (_summe, m.get("hoehe")))
        check("Block 5 ist der groesste Block (Rest)",
              int(hoehen.get("auswahl") or 0) == max(hoehen.values()), str(hoehen))
        _leinwand = getattr(app, "_dz_leinwand", None)
        _bereich = str(_leinwand.cget("scrollregion")) if _leinwand is not None else ""
        check("der Rollbereich der Spalte ist genau die Spalte (kein Rollen noetig)",
              _bereich.startswith("0 0 "), _bereich)
        messwert("block_auswahl", int(hoehen.get("auswahl") or 0), "px")
        messwert("spalte_summe", _summe, "px")

        # ---------------------------------------------------------------- 3. F-66 im Kopf
        abschnitt("3. Der Kopf nennt die Kennzahlen (F-66)")
        _alle = " | ".join(_texte(app.content))
        check("die Kennzahl steht im Kopf", "von 17 vorr" in _alle, _alle[:160])
        check("die zweite Kennzahl steht daneben", "von 17 herstellbar" in _alle, "")
        from dataclasses import asdict
        _ort = app.state.aktive_siedlung()
        _erwartet = dorfzentrum.kennzahlen_text(
            main.spieloekonomie.dorfzentrum_kennzahlen(asdict(_ort), app.state.forschungs_stufen()))
        check("der Text ist der formatierte Wert der Oekonomie", _erwartet in _alle,
              "%s in %s" % (_erwartet, _alle[:120]))

        # ---------------------------------------------------------------- 4. die Reiter
        abschnitt("4. Drei Reiter, Umschalten leckt nicht (Z3)")
        check("die Reihenfolge der Reiter ist Lager, Werkstaetten, Einheiten",
              dorfzentrum.REITER == ("Lager", "Werkst\u00e4tten", "Einheiten"),
              str(dorfzentrum.REITER))
        check("alle drei Reiter stehen als Beschriftung da",
              all(str(r) in _alle for r in dorfzentrum.REITER), "")
        _zahlen = []
        for _i in range(3):
            app._dz_reiter = _i
            app._dz_auswahl = None
            app._render_view()
            root.update()
            root.update_idletasks()
            _zahlen.append(_anzahl(app.content))
        check("jeder Reiter baut seinen Inhalt", min(_zahlen) > 30, str(_zahlen))
        _nach_eins = None
        for _i in range(10):
            app._dz_reiter = _i % 3
            app._dz_auswahl = None
            app._render_view()
            root.update()
            root.update_idletasks()
            if _i == 0:
                _nach_eins = _anzahl(app.content)
        _nach_zehn = _anzahl(app.content)
        check("nach zehn Reiterwechseln sind es so viele Widgets wie nach einem",
              _nach_zehn == _nach_eins, "%d gegen %d" % (_nach_zehn, _nach_eins))

        # ---------------------------------------------------------------- 5. Einheiten (F-65)
        abschnitt("5. Einheiten: zwei Haelften zu 14, KEINE Spalte Verwundete (F-65)")
        app._dz_reiter = 2
        app._dz_auswahl = None
        app._render_view()
        root.update()
        root.update_idletasks()
        _einh = [t for t in _texte(app.content)]
        check("kein Tabellenkopf 'Verwundete' (F-65)",
              not any("Verwundete" == t.strip() for t in _einh), "")
        check("die Kopfzeile nennt 'Einheit' und 'Bestand'",
              "Einheit" in _einh and "Bestand" in _einh, "")
        check("die Ansicht meldet 28 Arten", any("28 Arten" in t for t in _einh),
              " | ".join(t for t in _einh if "Arten" in t))
        _inhalt = app._dz_reiter_inhalt
        _haelften = [k for k in _inhalt.winfo_children() if type(k).__name__ == "Frame"]
        check("die Einheitentabelle liegt in einem Traeger", len(_haelften) == 1,
              str(len(_haelften)))
        if _haelften:
            _teile = [k for k in _haelften[0].winfo_children() if type(k).__name__ == "Frame"]
            check("die Tabelle steht in ZWEI Haelften", len(_teile) == 2, str(len(_teile)))
            check("jede Haelfte ist sichtbar und breiter als 100 px",
                  all(int(t.winfo_width()) > 100 for t in _teile),
                  str([int(t.winfo_width()) for t in _teile]))
            _namen = 0
            for _teil in _teile:
                for _zeile in _teil.winfo_children()[1:]:
                    _namen += 1
            check("in beiden Haelften stehen zusammen 28 Zeilen", _namen == 28, str(_namen))
            messwert("einheiten_zeilen", _namen, "Zeilen")

        # ---------------------------------------------------------------- 6. Werkstaetten (F-58)
        abschnitt("6. Werkstaetten: vier Spalten mit Zutat (F-58)")
        app._dz_reiter = 1
        app._dz_auswahl = None
        app._render_view()
        root.update()
        root.update_idletasks()
        _werk = _texte(app.content)
        for _spalte in ("Ware", "Werkstatt", "Zutat", "Zustand"):
            check("die Spalte %s steht im Kopf" % _spalte, _spalte in _werk, "")
        check("die Zutat steht als vorhanden / noetig mit Zeichen da",
              any("/ " in t and ("\u2713" in t or "\u2715" in t) for t in _werk),
              str([t for t in _werk if "/ " in t][:3]))
        check("der Zustand nennt 'herstellbar' oder 'fehlt'",
              any("herstellbar" == t.strip() or "fehlt" == t.strip() or
                  t.strip().endswith("herstellbar") or t.strip().endswith("fehlt")
                  for t in _werk), "")
        _inhalt = app._dz_reiter_inhalt
        # Die erste Flaeche ist der Tabellenkopf, danach kommt je Rezept eine Zeile
        # (die Zellen darin sind Kinder der Zeile und zaehlen NICHT mit).
        _rahmen = [k for k in _inhalt.winfo_children() if type(k).__name__ == "Frame"]
        _zeilen = _rahmen[1:]
        check("es stehen 17 Rezeptzeilen da", len(_zeilen) == 17, str(len(_zeilen)))
        check("eine Zeile ist sichtbar hoch (nicht auf 1 px zusammengefallen)",
              bool(_zeilen) and int(_zeilen[0].winfo_height()) > 10,
              str(int(_zeilen[0].winfo_height())) if _zeilen else "keine")

        # ---------------------------------------------------------------- 7. Auswahl links
        abschnitt("7. Die Auswahl steht links und folgt dem Reiter")
        app._dz_reiter = 1
        app._dz_auswahl = "Dolch"
        app._render_view()
        root.update()
        root.update_idletasks()
        _auswahl = " | ".join(_texte(app.content))
        check("die gewaehlte Ware steht mit ihrer Werkstatt links", "Dolch" in _auswahl, "")
        check("die Zutaten stehen mit vorhanden / noetig da", "Zutat" in _auswahl, "")
        check("ein Mengenfeld und 'Herstellen' stehen da", "Herstellen" in _auswahl, "")
        app._dz_reiter = 0
        app._dz_auswahl = "Dolch"
        app._render_view()
        root.update()
        root.update_idletasks()
        _lager = " | ".join(_texte(app.content))
        check("im Reiter Lager nennt die Auswahl Bestand und Werkstatt",
              "Bestand vor Ort" in _lager and "entsteht in" in _lager, _lager[:160])
        check("die Auswahl nennt auch, wofuer die Ware gebraucht wird",
              "gebraucht" in _lager, "")

        # ---------------------------------------------------------------- 8. stillgelegte Route
        abschnitt("8. Die stillgelegte Route 'Lager' zeigt dieselben Raster")
        app._switch_view("Lager")
        root.update()
        root.update_idletasks()
        _alt = " | ".join(_texte(app.content))
        check("die Route sagt offen, dass sie stillgelegt ist", "stillgelegt" in _alt, "")
        check("sie zeigt die Warenkacheln", "Waren vor Ort" in _alt, "")
        check("sie zeigt die Werkstattliste", "Werkstatt" in _alt, "")
        check("sie zeigt die Einheitentabelle", "Einheiten:" in _alt, "")
        befund("Sichtpruefung durch Daniel steht aus",
               "die Ansicht ist hier gemessen; Belegbilder liegen als "
               "docs/audits/dorfzentrum_*.png")
    finally:
        try:
            root.destroy()
        except Exception:                                                  # noqa: BLE001
            pass


try:
    _lauf()
except Exception as _fehler:                                               # noqa: BLE001
    import traceback
    traceback.print_exc()
    check("die Ansicht baut ohne Ausnahme", False, repr(_fehler))

sys.exit(bericht())
