# -*- coding: ascii -*-
"""Messprobe fuer Auftrag Nr. 15 an Claude: die UNBEKANNT-Fragen F2 bis F7 beantworten.

Laeuft im DPI-BEWUSSTEN Prozess, weil alle Masse bei k = 1,251 gefragt sind.

Aufruf:  python -X utf8 tools/messe_dorfzentrum_f2_f7.py
"""
from __future__ import annotations

import json
import os
import sys
import tkinter as tk
import tkinter.font as tkfont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _pfad in (ROOT, os.path.join(ROOT, "src")):
    if _pfad not in sys.path:
        sys.path.insert(0, _pfad)

import main  # noqa: E402
import spieloekonomie  # noqa: E402

main.dpi_bewusst_machen()

daten = {}

# --- F2: die Bedienelemente des Dorfzentrums ---
root = tk.Tk()
root.geometry("1024x720+20+20")
try:
    root.attributes("-alpha", 0.01)
except Exception:
    pass
root.update()
app = main.NebelseetalApp(root)
app._build_main_ui()
app._erste_siedlung_gruenden()
for _ in range(3):
    root.update()
    root.update_idletasks()
app._switch_view("Dorfzentrum")
for _ in range(5):
    root.update()
    root.update_idletasks()

daten["k"] = round(app.dpi_k, 4)
daten["flaeche"] = [app.content_canvas.winfo_width(), app.content_canvas.winfo_height()]

knoepfe = []
eintraege = []


def sammeln(w):
    for kind in w.winfo_children():
        klasse = kind.winfo_class()
        if klasse == "Button":
            try:
                knoepfe.append({"text": kind.cget("text"), "w": kind.winfo_width(),
                                "h": kind.winfo_height()})
            except Exception:
                pass
        elif klasse == "Entry":
            try:
                eintraege.append({"w": kind.winfo_width(), "h": kind.winfo_height()})
            except Exception:
                pass
        sammeln(kind)


sammeln(app.content)
daten["knoepfe"] = knoepfe
daten["eintraege"] = eintraege
daten["anzahl_knoepfe"] = len(knoepfe)
daten["anzahl_eintraege"] = len(eintraege)

# --- F3: Ortsbestand-Block (Flaeche #1B2A2F) ---
bloecke = []


def bloecke_suchen(w):
    for kind in w.winfo_children():
        try:
            if kind.winfo_class() in ("Frame", "Canvas") and \
                    str(kind.cget("bg")).upper() == main.SPIEDLUNGS_ORTSBESTAND:
                bloecke.append({"klasse": kind.winfo_class(), "w": kind.winfo_width(),
                                "h": kind.winfo_height(), "text": kind.winfo_class()})
        except Exception:
            pass
        bloecke_suchen(kind)


bloecke_suchen(app.content)
daten["ortsbestand_bloecke"] = bloecke

# --- F7: Rollbalkenbreite im bewussten Prozess ---
sb = tk.Scrollbar(root, orient=tk.VERTICAL)
root.update_idletasks()
daten["rollbalken"] = {"reqwidth": sb.winfo_reqwidth(), "reqheight": sb.winfo_reqheight()}
sb.destroy()

# --- F4/F5/F6: laengste Namen in echter Tk-Schrift bei 16 px ---
waren = json.load(open(os.path.join(ROOT, "data", "items.json"), encoding="utf-8"))["waren"]
einheiten = json.load(open(os.path.join(ROOT, "data", "units.json"), encoding="utf-8"))
schrift16 = tkfont.Font(font=("Arial", -app.schrift(13)))


def laengster(namen):
    bester = max(namen, key=lambda n: schrift16.measure(n))
    wort = max(namen, key=lambda n: max(schrift16.measure(t) for t in n.split()))
    return {"name": bester, "px": schrift16.measure(bester),
            "wort": wort, "wort_px": max(schrift16.measure(t) for t in wort.split())}


waren_namen = []
if isinstance(waren, dict):
    waren_namen = [str(v.get("name") or k) for k, v in waren.items()]
else:
    waren_namen = [str(w.get("name") or w) for w in waren]
daten["waren_anzahl"] = len(waren_namen)
daten["waren_laengster"] = laengster(waren_namen)

ein_namen = []
for e in (einheiten.get("einheiten") or []):
    ein_namen.append(str(e.get("name") if isinstance(e, dict) else e))
daten["einheiten_anzahl"] = len(ein_namen)
daten["einheiten_laengster"] = laengster(ein_namen) if ein_namen else None

# Rezepte: was gibt es?
rez = getattr(spieloekonomie, "REZEPTE", None)
daten["rezepte_typ"] = type(rez).__name__ if rez is not None else "fehlt"
if isinstance(rez, dict):
    namen = [str(v.get("name") or k) for k, v in rez.items()]
    daten["rezepte_anzahl"] = len(namen)
    daten["rezepte_laengster"] = laengster(namen) if namen else None
    erstes = list(rez.items())[0]
    daten["rezept_beispiel"] = {erstes[0]: erstes[1]}

# --- F8: liefert spieloekonomie Kennzahlen fertig? ---
funktionen = [n for n in dir(spieloekonomie) if not n.startswith("_") and callable(
    getattr(spieloekonomie, n))]
daten["spieloekonomie_funktionen"] = funktionen

print(json.dumps(daten, indent=1, ensure_ascii=False, default=str))
root.destroy()
