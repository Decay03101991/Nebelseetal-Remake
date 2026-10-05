"""Pruefung der Siedlungskarte im Fenster (Tkinter), ohne Hauptschleife.

Geprueft wird das, was Daniel sehen wird: Ansicht oeffnen, Feld waehlen, Eignung lesen,
bauen (mit Kostenabzug), Sumpf gesperrt, abreissen, und die Schaltflaechen der Uebersicht.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, befund, check, import_src

ROOT, SRC = import_src()
import tkinter as tk
import gelaende as G
import main as M


def neuen_app():
    """Fenster aufbauen, aber nicht anzeigen (kein mainloop)."""
    root = tk.Tk()
    root.withdraw()
    app = M.NebelseetalApp(root)
    # Die Ladepage wartet auf after()-Rueckrufe; ohne mainloop feuern die nie.
    app._build_main_ui()
    return root, app


try:
    root, app = neuen_app()
except Exception as fehler:                     # kein Bildschirm vorhanden
    print(f"ACHTUNG: kein Fenster moeglich ({type(fehler).__name__}: {fehler}) —")
    print("diese Pruefung braucht einen angemeldeten Windows-Desktop.")
    sys.exit(1)


def sammle_knoepfe(widget):
    """Alle Schaltflaechen unterhalb eines Elements (rekursiv)."""
    treffer = []
    for kind in widget.winfo_children():
        if isinstance(kind, tk.Button):
            treffer.append(kind)
        treffer += sammle_knoepfe(kind)
    return treffer


def sammle_texte(widget):
    """Alle Beschriftungen unterhalb eines Elements (rekursiv)."""
    treffer = []
    for kind in widget.winfo_children():
        if isinstance(kind, tk.Label):
            treffer.append(str(kind.cget("text")))
        treffer += sammle_texte(kind)
    return treffer

abschnitt("Siedlungskarte im Fenster — Ansicht oeffnen")
siedlung = M.Settlement(name="Probesiedlung", map_id=app.state.current_map,
                        karte=G.siedlungskarte_erzeugen(31, typ_id="weideland"))
app.state.settlements.append(siedlung)

app._oeffne_siedlungskarte(siedlung)
check("Ansicht heisst 'Siedlungskarte'", app.current_view == "Siedlungskarte", app.current_view)
kinder = app.content.winfo_children()
check("die Ansicht hat Inhalte aufgebaut", len(kinder) > 3, f"{len(kinder)} Elemente")
check("die gewaehlte Siedlung ist gesetzt", app.karten_siedlung is siedlung)

# Die Karte ist eine Zeichenfläche (astra-Gutachten 05.10.2026): jedes Feld ist ein Objekt
# mit dem Tag 'feld:i' und anklickbar. Vorher waren es 40 kleine Knöpfe im Raster.
canvas = getattr(app, "karten_canvas", None)
check("die Karte ist eine Zeichenfläche", canvas is not None)
felder_da = ([i for i in range(len(siedlung.karte["raster"]))
              if canvas.find_withtag(f"feld:{i}")] if canvas is not None else [])
check("56 anklickbare Felder auf der Karte", len(felder_da) == 56, f"{len(felder_da)} Felder")
farben = ({canvas.itemcget(o, "fill") for i in range(len(siedlung.karte["raster"]))
           for o in canvas.find_withtag(f"feld:{i}")
           if canvas.type(o) == "rectangle" and canvas.itemcget(o, "fill")} if canvas is not None else set())
check("die Kacheln tragen die Gelaendefarben", len(farben) >= 4, f"{len(farben)} Farben")

abschnitt("Siedlungskarte im Fenster — Feld waehlen und Eignung lesen")
raster = siedlung.karte["raster"]
wald = raster.index("wald")
app._karten_feld_waehlen(wald)
check("das gewaehlte Feld ist gemerkt", app.karten_feld == wald, str(app.karten_feld))
namen = [b.cget("text") for b in sammle_knoepfe(app.content)]
check("auf Wald wird der Holzfäller angeboten",
      any("Holzfäller" in n for n in namen), str(namen[:6]))
check("und der Steinmetz NICHT (liefert auf Wald nichts)",
      not any("Steinmetz" in n for n in namen), str(namen[:6]))
check("die Kosten stehen an der Schaltfläche",
      any("Holz" in n and "Stein" in n for n in namen),
      str([n for n in namen if "Holzfäller" in n]))
check("die Ausbildungsstätten haben einen Geländebezug (Vorgabe Daniel 05.10.2026)",
      not any("Kriegerakademie" in n for n in namen),
      str([n for n in namen if "akademie" in n.lower()]))
# Auf einem Graslandfeld muss sie dagegen angeboten werden — die Regel gilt je Gelände.
_grasfeld = raster.index("grasland")
app._karten_feld_waehlen(_grasfeld)
_namen_gras = [b.cget("text") for b in sammle_knoepfe(app.content)]
check("auf Grasland wird die Kriegerakademie angeboten",
      any("Kriegerakademie" in n for n in _namen_gras),
      str([n for n in _namen_gras if "akademie" in n.lower()]))

abschnitt("Siedlungskarte im Fenster — Sumpf ist gesperrt")
sumpf = raster.index("sumpf")
app._karten_feld_waehlen(sumpf)
namen = [b.cget("text") for b in sammle_knoepfe(app.content)]
check("auf Sumpf wird kein Bauvorschlag gemacht",
      not any("(" in n for n in namen), str(namen[:6]))
check("die Meldung nennt das Feld als Sumpf",
      any("Sumpf" in t for t in sammle_texte(app.content)), str(sammle_texte(app.content)[:6]))

abschnitt("Siedlungskarte im Fenster — Bauen kostet Rohstoffe und belegt das Feld")
app.state.resources["holz"].amount = 500
app.state.resources["stein"].amount = 500
vorher_holz = app.state.resources["holz"].amount
vorher_stein = app.state.resources["stein"].amount
vorher_siedler = app.state.population
kosten = M.baukosten("holzfaeller")
check("Holzfäller-Preis ist der belegte Originalpreis (10 Holz, 5 Stein, 1 Siedler)",
      kosten == {"holz": 10, "stein": 5, "siedler": 1}, str(kosten))
check("Haus kostet 80 Holz und 50 Stein und KEINEN Siedler (es beherbergt welche)",
      M.baukosten("haus") == {"holz": 80, "stein": 50}, str(M.baukosten("haus")))
check("der Siedler erscheint lesbar in der Kostenzeile",
      "Siedler" in M.kosten_text(kosten), M.kosten_text(kosten))

app._karten_feld_waehlen(wald)
app._karten_bauen("holzfaeller")
check("das Feld ist belegt", siedlung.bauten.get(str(wald)) == "holzfaeller", str(siedlung.bauten))
check(f"Holz wurde abgezogen ({kosten['holz']})",
      app.state.resources["holz"].amount == vorher_holz - kosten["holz"],
      f"{vorher_holz} -> {app.state.resources['holz'].amount}")
check(f"Stein wurde abgezogen ({kosten['stein']})",
      app.state.resources["stein"].amount == vorher_stein - kosten["stein"],
      f"{vorher_stein} -> {app.state.resources['stein'].amount}")
check("ein Siedler arbeitet jetzt im Gebäude (Bevölkerung sinkt)",
      app.state.population == vorher_siedler - 1,
      f"{vorher_siedler} -> {app.state.population}")
check("das Feld bleibt ausgewählt und zeigt das neue Gebäude (astra-Nachprüfung 05.10.2026)",
      app.karten_feld == wald, f"karten_feld={app.karten_feld}")

abschnitt("Siedlungskarte — die feinere Fassung aus src/karten_optik_fein.py ist eingehängt")
import karten_optik_fein as KF                                       # noqa: E402
canvas = app.karten_canvas
check("die Siedlungskarte ist noch die Zeichenfläche", canvas is not None)
_fuell = {canvas.itemcget(o, "fill") for o in canvas.find_all()
          if canvas.type(o) == "rectangle" and canvas.itemcget(o, "fill")}
check("das Gelände trägt die astra-Farben (Ebene #74805A, Wald #455E43)",
      {"#74805A", "#455E43"} <= _fuell, str(sorted(_fuell)))
_raender = {canvas.itemcget(o, "outline") for o in canvas.find_all()
            if canvas.type(o) in ("rectangle", "oval")}
check("die alte blaue Feldmarkierung #38BDF8 ist verschwunden",
      "#38BDF8" not in (_fuell | _raender), str(sorted(_raender)))
_text = [str(canvas.itemcget(o, "text")) for o in canvas.find_all() if canvas.type(o) == "text"]
check("die Koordinatenleiste zeigt die Buchstaben des Panels (A–H)",
      _text[:8] == list("ABCDEFGH"), str(_text))
check("und darunter die Zeilen 1..5 — sonst stehen keine Zahlen im Feld",
      _text[8:13] == ["1", "2", "3", "4", "5"], str(_text))
check("kein Feld trägt mehr einen Stempel 'St. n' (astra: Stufenanzeige aus der Silhouette)",
      not any(t.startswith("St.") for t in _text), str(_text))
_auswahl = canvas.find_withtag("auswahl")
check("das gewählte Feld trägt den Auswahlrahmen des Feinplans (Gold + Unterkontur + 4 Winkel)",
      len(_auswahl) == 6, f"{len(_auswahl)} Objekte")
check("unter dem Gold liegt die dunkle Unterkontur #172128",
      any(canvas.itemcget(o, "outline") == KF.AUSWAHL_GOLD for o in _auswahl
          if canvas.type(o) == "rectangle")
      and any(canvas.itemcget(o, "outline") == KF.AUSWAHL_UNTER_FARBE for o in _auswahl
              if canvas.type(o) == "rectangle"),
      str([canvas.itemcget(o, "outline") for o in _auswahl if canvas.type(o) == "rectangle"]))

abschnitt("Siedlungskarte im Fenster — zu wenig Rohstoffe wird gemeldet")
app.state.resources["holz"].amount = 1
app.state.resources["stein"].amount = 1
freies_waldfeld = [i for i, a in enumerate(raster) if a == "wald" and str(i) not in siedlung.bauten][0]
app._karten_feld_waehlen(freies_waldfeld)
app._karten_bauen("holzfaeller")
check("ohne Rohstoffe wird nicht gebaut", str(freies_waldfeld) not in siedlung.bauten,
      str(siedlung.bauten))
check("und der Grund steht im Spielprotokoll",
      any("Nicht genug Rohstoffe" in z for z in app.state.log[-3:]), str(app.state.log[-2:]))

abschnitt("Siedlungskarte im Fenster — abreissen (Handbuch S. 292)")
app._karten_feld_waehlen(wald)
app._karten_abreissen()
check("das Feld ist wieder frei", str(wald) not in siedlung.bauten, str(siedlung.bauten))
check("das Abreissen steht im Protokoll",
      any("abgerissen" in z for z in app.state.log[-3:]), str(app.state.log[-2:]))

abschnitt("Siedlungskarte im Fenster — Uebersicht zeigt den Weg zur Karte")
app._switch_view("Dorfzentrum")
uebersicht_texte = sammle_texte(app.content)
knopf_texte = [b.cget("text") for b in sammle_knoepfe(app.content)]
check("die Siedlung nennt ihren Kartentyp",
      any("Weideland" in str(t) for t in uebersicht_texte), str(uebersicht_texte[:4]))
check("und hat eine Schaltfläche 'Karte öffnen'",
      any("Karte öffnen" == str(t) for t in knopf_texte), str(knopf_texte[:4]))

abschnitt("Auskunft im Spiel — der Reiter Chat")
app._switch_view("Chat")
check("die Ansicht heißt Chat", app.current_view == "Chat", app.current_view)
texte = sammle_texte(app.content)
check("die Begrüßung steht da", any("Auskunft" in t for t in texte),
      str(texte[:3]))
check("das Eingabefeld ist da", hasattr(app, "chat_eingabe")
      and app.chat_eingabe.winfo_exists())
knopf_texte = [b.cget("text") for b in sammle_knoepfe(app.content)]
check("es gibt Vorschlagsfragen zum Antippen", any("Holzfäller" in t for t in knopf_texte),
      str(knopf_texte[:4]))

vorher = len(getattr(app, "chat_verlauf", []))
app._chat_fragen("Was macht der Holzfäller?")
check("die Frage und die Antwort landen im Verlauf", len(app.chat_verlauf) == vorher + 2,
      str(len(app.chat_verlauf)))
letzte_frage, letzte_antwort = app.chat_verlauf[-2], app.chat_verlauf[-1]
check("die Frage ist gespeichert", letzte_frage == ("du", "Was macht der Holzfäller?"),
      str(letzte_frage))
check("die Antwort nennt den Wald und 4 pro Stunde",
      "Wald" in letzte_antwort[1] and "4" in letzte_antwort[1], letzte_antwort[1][:120])
check("und wieder ist die Ansicht aufgebaut", len(app.content.winfo_children()) > 3)

app._chat_fragen("Wie wird das Wetter?")
check("unbekannte Frage wird ehrlich verneint", "Das weiß ich nicht" in app.chat_verlauf[-1][1],
      app.chat_verlauf[-1][1][:90])

app._chat_fragen("Paladin")
check("Einzelfrage nach einer Einheit funktioniert", "Paladin" in app.chat_verlauf[-1][1],
      app.chat_verlauf[-1][1][:80])

app._chat_fragen("")
check("eine leere Frage ändert nichts", len(app.chat_verlauf) == vorher + 6,
      str(len(app.chat_verlauf)))

abschnitt("Siedlungskarte — Wege und Stufenpips im Feinplan (astra Siedlung 2 und 3)")
weg = M.Settlement(name="Wegprobe", map_id=app.state.current_map,
                   karte=G.siedlungskarte_erzeugen(77, typ_id="weideland"))
app.state.settlements.append(weg)
app.state.resources["holz"].amount = 400
app.state.resources["stein"].amount = 400
app._oeffne_siedlungskarte(weg)
_raster_w = weg.karte["raster"]
_spalten_w = int(weg.karte["spalten"])


def _graslandpaar(raster, spalten):
    """Zwei ORTHOGONAL benachbarte Graslandfelder (dort ist ein Haus erlaubt)."""
    for i, a in enumerate(raster):
        if a != "grasland":
            continue
        if (i % spalten) != spalten - 1 and raster[i + 1] == "grasland":
            return i, i + 1
        if i + spalten < len(raster) and raster[i + spalten] == "grasland":
            return i, i + spalten
    return None


_paar = _graslandpaar(_raster_w, _spalten_w)
check("die Probekarte hat zwei aneinander grenzende Graslandfelder", _paar is not None, str(_paar))
if _paar:
    _a, _b = _paar
    app._karten_feld_waehlen(_a)
    app._karten_bauen("haus")
    app._karten_feld_waehlen(_b)
    app._karten_bauen("haus")
    check("beide Häuser stehen auf benachbarten Feldern",
          weg.bauten.get(str(_a)) == "haus" and weg.bauten.get(str(_b)) == "haus",
          str(weg.bauten))
    _cw = app.karten_canvas
    _wege = _cw.find_withtag("weg")
    check("zwischen zwei bebauten Nachbarfeldern liegt ein Wegabschnitt",
          len(_wege) == 4, f"{len(_wege)} Objekte (2 Felder x 2 Linien)")
    check("der Weg ist #75674F mit 4-px-Innenlinie #A28E69 (astra Siedlung 2)",
          {_cw.itemcget(o, "fill") for o in _wege} == {KF.WEG_FARBE, KF.WEG_INNEN_FARBE},
          str(sorted({_cw.itemcget(o, "fill") for o in _wege})))
    _pips = [o for o in _cw.find_withtag(f"feld:{_a}") if _cw.type(o) == "rectangle"
             and _cw.itemcget(o, "fill") == KF.PIP_FARBE]
    check("das Haus zeigt seine erreichte Stufe als goldenen Pip", bool(_pips), f"{len(_pips)} Pips")
    if _pips:
        _pk = _cw.coords(_pips[0])
        check("ein Pip ist 4 × 4 px (astra Siedlung 3)",
              abs((_pk[2] - _pk[0]) - 4.0) < 0.01 and abs((_pk[3] - _pk[1]) - 4.0) < 0.01,
              str(_pk))
    # Die Pips sind 4 x 4 px; der Bodenschatten des Baukörpers nutzt dieselbe dunkle Farbe und
    # wird deshalb über die Größe ausgeschlossen (PIP_LEER == BODENSCHATTEN == #343B30).
    _alle_pips = [o for o in _cw.find_withtag(f"feld:{_a}") if _cw.type(o) == "rectangle"
                  and _cw.itemcget(o, "fill") in (KF.PIP_FARBE, KF.PIP_LEER)
                  and abs((_cw.coords(o)[2] - _cw.coords(o)[0]) - 4.0) < 0.01]
    check("die Zahl der Pips ist die Höchststufe des Hauses (4)",
          len(_alle_pips) == 4, f"{len(_alle_pips)} Pips")

abschnitt("Siedlungskarte im Fenster — Siedlung ohne Karte (alter Spielstand)")
alt = M.Settlement(name="Alte Siedlung", map_id=app.state.current_map)
app.state.settlements.append(alt)
app._oeffne_siedlungskarte(alt)
check("ohne Karte zeigt die Ansicht keinen Bauplan", app.karten_feld is None)
app._karten_zuwaeisen(alt)
check("der alten Siedlung wurde eine Karte zugewiesen",
      alt.karte is not None and bool(alt.karte["typ_name"]), str(alt.karte and alt.karte["typ_name"]))
check("und sie ist nicht dieselbe wie die der anderen Siedlung",
      M.karten_signatur(alt.karte) != M.karten_signatur(siedlung.karte))

root.destroy()
sys.exit(bericht())
