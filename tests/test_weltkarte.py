"""Pruefung der WELTkarte im Fenster (Tkinter), ohne Hauptschleife.

Was geprueft wird — die Vorgaben des astra-Bildgutachtens vom 05.10.2026, Abschnitt A3:

* Zeichenflaeche mit 48 px je Feld in eigenen waagerechten und senkrechten Scrollbalken,
* Zoomstufen („−  100 %  +"),
* eine kleine Uebersichtskarte oben rechts, die den sichtbaren Ausschnitt als Rechteck zeigt,
* Gebietsleiste OBEN mit ausdruecklich benannten gesperrten Gebieten,
* ein festes Detailpanel (Ort · Koordinate / Gelaende / Status / Gebaeude / Aktion),
* ein einfacher Klick, der NUR auswaehlt — vorher erforschte und erledigte er still Nebenwirkungen.

Aufruf:  python -X utf8 tests/test_weltkarte.py   (braucht einen angemeldeten Windows-Desktop)
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, befund, check, import_src   # noqa: E402

ROOT, SRC = import_src()
import tkinter as tk                                                # noqa: E402
import main as M                                                    # noqa: E402

try:
    root = tk.Tk()
    root.withdraw()
    app = M.NebelseetalApp(root)
    app._build_main_ui()
    root.update_idletasks()
except Exception as fehler:
    print(f"ACHTUNG: kein Fenster moeglich ({type(fehler).__name__}: {fehler}) —")
    print("diese Pruefung braucht einen angemeldeten Windows-Desktop.")
    sys.exit(1)


def tick():
    root.update_idletasks()
    root.update()


def texte(widget, out=None):
    out = [] if out is None else out
    try:
        t = widget.cget("text")
        if t:
            out.append(str(t))
    except Exception:
        pass
    for k in widget.winfo_children():
        texte(k, out)
    return out


def knoepfe(widget, out=None):
    out = [] if out is None else out
    try:
        if widget.winfo_class() == "Button":
            out.append(widget)
    except Exception:
        pass
    for k in widget.winfo_children():
        knoepfe(k, out)
    return out


def zustand():
    """Alles, was ein blosser Auswahlklick NICHT veraendern darf."""
    st = app.state
    return {
        "rohstoffe": tuple(sorted((k, round(v.amount, 3)) for k, v in st.resources.items())),
        "ruf": st.ruf,
        "log": len(st.log),
        "bewegungen": len(st.movements),
        "entdeckt": tuple((t.x, t.y, t.discovered, t.quest_done) for t in st.map_tiles),
    }


# ------------------------------------------------------------------ 1 Aufbau
abschnitt("1. Die Weltkarte baut sich als Zeichenflaeche auf (astra A3)")
if not app.state.map_tiles:
    befund("keine Kartenfelder im Zustand — der Zeitlauf erzeugt sie erst spaeter")
    app.state.generate_map(app.state.current_map)
app._switch_view("Karten")
tick()
check("die Ansicht heisst 'Karten'", app.current_view == "Karten", app.current_view)
check("der Titel nennt die Weltkarte", any("Weltkarte – Orte entdecken" == t for t in texte(app.content)),
      str([t for t in texte(app.content) if "Weltkarte" in t]))
gitter = next(m for m in M.MAPS if m["id"] == app.state.current_map)["size"]
check("die Karte hat 20x20 Felder", gitter == 20 and len(app.state.map_tiles) == 400,
      f"{gitter}x{gitter}, {len(app.state.map_tiles)} Felder")

canvas = getattr(app, "map_canvas", None)
check("die Karte ist eine Zeichenflaeche", canvas is not None)
gezeichnet = len(canvas.find_withtag("weltfeld")) if canvas is not None else 0
check("jedes Feld ist auf der Zeichenflaeche gezeichnet", gezeichnet == 400, f"{gezeichnet} Felder")

# ------------------------------------------------------------------ 2 Scrollbalken
abschnitt("2. Eigene Scrollbalken waagerecht und senkrecht (astra A3)")
xsb = getattr(app, "welt_xsb", None)
ysb = getattr(app, "welt_ysb", None)
check("es gibt eine waagerechte Scrollbar", isinstance(xsb, tk.Scrollbar))
check("es gibt eine senkrechte Scrollbar", isinstance(ysb, tk.Scrollbar))
check("die waagerechte Scrollbar liegt waagerecht",
      xsb is not None and str(xsb.cget("orient")) == "horizontal",
      str(xsb.cget("orient")) if xsb is not None else "")
check("die senkrechte Scrollbar liegt senkrecht",
      ysb is not None and str(ysb.cget("orient")) == "vertical",
      str(ysb.cget("orient")) if ysb is not None else "")
check("der Zeichenbereich ist groesser als das Fenster (die Karte passt absichtlich nicht ganz)",
      canvas is not None and float(canvas.cget("scrollregion").split()[-1]) > 600,
      str(canvas.cget("scrollregion")) if canvas is not None else "")

# ------------------------------------------------------------------ 3 Zoom
abschnitt('3. Zoomstufen — minus, Prozentanzeige, plus (astra A3)')
check("der Standardzoom ist 48 px je Feld", app.welt_zelle == M.WELT_ZOOM_STANDARD == 48,
      str(app.welt_zelle))
check("die Anzeige nennt 100 %", app.welt_zoom_label.cget("text") == "100 %",
      str(app.welt_zoom_label.cget("text")))
zoom_knopf_plus = [k for k in knoepfe(app.content) if str(k.cget("text")) == "+"]
zoom_knopf_minus = [k for k in knoepfe(app.content) if str(k.cget("text")) == "−"]
check("es gibt die Schaltflaechen minus und plus", bool(zoom_knopf_plus) and bool(zoom_knopf_minus))
if zoom_knopf_plus:
    zoom_knopf_plus[0].invoke()
    tick()
check("nach dem Vergroessern ist das Feld 64 px gross", app.welt_zelle == 64, str(app.welt_zelle))
check("die Anzeige nennt 133 %", app.welt_zoom_label.cget("text") == "133 %",
      str(app.welt_zoom_label.cget("text")))
for _ in range(4):
    app._welt_zoom(1)
check("der Zoom ist nach oben begrenzt", app.welt_zelle == max(M.WELT_ZOOM_STUFEN),
      str(app.welt_zelle))
for _ in range(8):
    app._welt_zoom(-1)
check("der Zoom ist nach unten begrenzt", app.welt_zelle == min(M.WELT_ZOOM_STUFEN),
      str(app.welt_zelle))
app._welt_zoom(3)
check("zurueck auf 48 px fuer die weiteren Pruefungen", app.welt_zelle == 48, str(app.welt_zelle))

# ------------------------------------------------------------------ 4 Uebersichtskarte
abschnitt("4. Kleine Uebersichtskarte mit dem sichtbaren Ausschnitt (astra A3)")
uebersicht = getattr(app, "welt_uebersicht", None)
check("die Uebersichtskarte ist da", isinstance(uebersicht, tk.Canvas))
kacheln = [o for o in uebersicht.find_all() if uebersicht.type(o) == "rectangle"] if uebersicht else []
check("sie zeigt alle 400 Felder", len(kacheln) >= 400, f"{len(kacheln)} Rechtecke")
rahmen = getattr(app, "_welt_uebersicht_rahmen", None)
check("sie hat ein Rechteck fuer den sichtbaren Ausschnitt", rahmen is not None)
# Ausgangslage ausdruecklich herstellen: der Zoom hat die Ansicht zwischenzeitlich verschoben.
app.map_canvas.xview_moveto(0.0)
app.map_canvas.yview_moveto(0.0)
app._welt_uebersicht_update()
vorher_rahmen = uebersicht.coords(rahmen) if (uebersicht and rahmen) else []
app.map_canvas.xview_moveto(0.5)
app.map_canvas.yview_moveto(0.5)
app._welt_uebersicht_update()
nachher_rahmen = uebersicht.coords(rahmen) if (uebersicht and rahmen) else []
check("nach dem Scrollen wandert das Rechteck mit", vorher_rahmen != nachher_rahmen,
      f"{vorher_rahmen} -> {nachher_rahmen}")
app.map_canvas.xview_moveto(0.0)
app.map_canvas.yview_moveto(0.0)
app._welt_uebersicht_update()

# ------------------------------------------------------------------ 5 Klick waehlt nur aus
abschnitt("5. Ein einfacher Klick waehlt NUR aus (astra A3)")
vorher = zustand()
zelle = app.welt_zelle
app.map_canvas.event_generate("<Button-1>", x=int(3 * zelle + zelle / 2), y=int(4 * zelle + zelle / 2))
tick()
check("der Klick waehlt genau dieses Feld", app.welt_auswahl == (3, 4), str(app.welt_auswahl))
nachher = zustand()
check("der Klick veraendert KEINE Rohstoffe", vorher["rohstoffe"] == nachher["rohstoffe"])
check("der Klick veraendert den Ruf nicht", vorher["ruf"] == nachher["ruf"])
check("der Klick schreibt nichts ins Protokoll", vorher["log"] == nachher["log"],
      f"{vorher['log']} -> {nachher['log']}")
check("der Klick startet keine Bewegung", vorher["bewegungen"] == nachher["bewegungen"])
check("der Klick erledigt keine Aufgabe still", vorher["entdeckt"] == nachher["entdeckt"])
auswahlrahmen = [o for o in app.map_canvas.find_withtag("welt_auswahl")
                 if app.map_canvas.type(o) == "rectangle"]
check("das gewaehlte Feld hat einen kennzeichnenden Rahmen", bool(auswahlrahmen),
      f"{len(auswahlrahmen)} Rahmen")

# ------------------------------------------------------------------ 6 Detailpanel
abschnitt("6. Festes Detailpanel: Ort, Gelaende, Status, Gebaeude (astra A3)")
daten = app._welt_auswahl_daten()
check("das Detailpanel kennt das gewaehlte Feld", daten is not None and daten["x"] == 3 and daten["y"] == 4,
      str(daten and (daten["x"], daten["y"])))
check("es nennt die Koordinate in Kartenform (z. B. D5)", bool(daten) and daten["koordinate"] == "D5",
      str(daten and daten["koordinate"]))
detail_texte = texte(getattr(app, "welt_detail", app.content))
for begriff in ("Gelände:", "Status:"):
    check(f"das Panel zeigt „{begriff}" + '"', any(begriff in t for t in detail_texte),
          " | ".join(detail_texte[:8]))
check("das Panel nennt den Inhalt mit dem richtigen Wort (Vorkommen statt Gebäude)",
      any(("Vorkommen:" in t) or ("Gebäude:" in t) for t in detail_texte),
      " | ".join(detail_texte[:8]))
check("ein Rohstofffeld heisst im Panel „Vorkommen" + '"',
      daten is not None and (daten["gebaeude_label"] == "Vorkommen" if daten["gebaeude"] != "keine"
                             else daten["gebaeude_label"] == "Gebäude"),
      str(daten and daten["gebaeude_label"]))
check("die Ortsnamen stehen NICHT mehr auf jedem Feld (astra: kein Namensrauschen)",
      not any(app.map_canvas.type(o) == "text" and str(app.map_canvas.itemcget(o, "text")).strip()
              not in ("Hier",) and "weltregion" not in app.map_canvas.gettags(o)
              for o in app.map_canvas.find_all()),
      "es stehen wieder Namen auf den Feldern")

# ------------------------------------------------------------------ 7 Gebietsleiste
abschnitt("7. Gebietsleiste oben — gesperrte Gebiete ausdruecklich benannt (astra A3)")
menu = getattr(app, "welt_gebiet_menu", None)
check("es gibt ein Gebietsmenue", menu is not None)
beschriftungen = [app._welt_gebiet_beschriftung(m["id"]) for m in M.MAPS]
check("das eigene Gebiet ist als „(hier)" + '"' + " benannt",
      any("(hier)" in b for b in beschriftungen), str(beschriftungen))
gesperrt = [b for b in beschriftungen if "gesperrt" in b]
check("gesperrte Gebiete heissen ausdruecklich „– gesperrt" + '"', bool(gesperrt), str(beschriftungen))
gesperrte_id = next((m["id"] for m in M.MAPS
                     if app._welt_gebiet_status(m["id"]) == "gesperrt"), None)
check("es gibt mindestens ein gesperrtes Gebiet am Spielanfang", gesperrte_id is not None)
if gesperrte_id:
    app._welt_gebiet_wechseln(app._welt_gebiet_beschriftung(gesperrte_id))
    tick()
    panel_texte = texte(app.content)
    check("das gesperrte Gebiet wird begruendet",
          any("ist gesperrt" in t for t in panel_texte),
          " | ".join(t for t in panel_texte if "gesperrt" in t))
    knoepfe_texte = [str(k.cget("text")) for k in knoepfe(app.content)]
    check("der Weg zum Portal wird angeboten", "Zum Portal" in knoepfe_texte, str(knoepfe_texte[:6]))
    check("der Weg zur Forschung wird angeboten", "Zur Forschung" in knoepfe_texte, str(knoepfe_texte[:6]))
    app._switch_view("Karten")
    tick()
    app.welt_gebiet = app.state.current_map
    app._render_view()
    tick()
check("zurueck im eigenen Gebiet gibt es wieder eine Zeichenflaeche",
      getattr(app, "map_canvas", None) is not None)

# ------------------------------------------------------------------ 8 Eigener Ort
abschnitt("8. Der eigene Ort: Fahne, „Hier" + '"' + ", Siedlung oeffnen (astra A3)")
siedlung = M.Settlement(name="Testort", map_id=app.state.current_map, x=12, y=12)
app.state.settlements.append(siedlung)
app.welt_auswahl = None
app._draw_map()
tick()
check("der eigene Ort traegt die Fahne mit dem Vermerk „Hier" + '"',
      bool(app.map_canvas.find_withtag("welthier")),
      f"{len(app.map_canvas.find_withtag('welthier'))} Zeichen")
app.map_canvas.event_generate("<Button-1>", x=int(12 * zelle + zelle / 2), y=int(12 * zelle + zelle / 2))
tick()
check("ein Klick auf den eigenen Ort waehlt ihn", app.welt_auswahl == (12, 12), str(app.welt_auswahl))
daten = app._welt_auswahl_daten()
check("das Panel nennt den Ortsnamen", daten is not None and daten["name"] == "Testort",
      str(daten and daten["name"]))
check("das Panel nennt den Status „Eigene Siedlung" + '"',
      daten is not None and daten["status"] == "Eigene Siedlung", str(daten and daten["status"]))
knoepfe_texte = [str(k.cget("text")) for k in knoepfe(getattr(app, "welt_detail", app.content))]
check("die Aktion heisst „Siedlung öffnen" + '"', "Siedlung öffnen" in knoepfe_texte,
      str(knoepfe_texte[:6]))
zum_ort = [k for k in knoepfe(app.content) if str(k.cget("text")) == "Zum aktuellen Ort"]
check("es gibt die Schaltflaeche „Zum aktuellen Ort" + '"', bool(zum_ort))
if zum_ort:
    app.welt_auswahl = None
    app._draw_map()
    zum_ort[0].invoke()
    tick()
    check("sie waehlt den eigenen Ort aus", app.welt_auswahl == (12, 12), str(app.welt_auswahl))
    check("und zieht die Ansicht dorthin (die Karte ist gescrollt)",
          app.map_canvas.xview()[0] > 0.0, str(app.map_canvas.xview()))

# ------------------------------------------------------------------ 9 Legende und Regionen
abschnitt("9. Legende und einmalige Regionsnamen (astra A3: kein Namensrauschen)")
alle_texte = texte(app.content)
for gelaende_name in ("Wald", "Ebene", "Gebirge", "Wasser"):
    check(f"die Legende nennt {gelaende_name}", any(gelaende_name == t for t in alle_texte),
          str([t for t in alle_texte if len(t) < 12][:10]))
regionen = app.map_canvas.find_withtag("weltregion")
check("die Regionen sind einmal gross beschriftet", len(regionen) == 9, f"{len(regionen)} Namen")

# ------------------------------------------------------------------ 10 Ortszeichen ausblenden
abschnitt("10. Ortszeichen lassen sich ausblenden")
vorher_orte = len(app.map_canvas.find_withtag("weltort"))
schalter = [k for k in knoepfe(app.content)
            if "Ortszeichen" in str(k.cget("text"))]
check("es gibt den Schalter fuer die Ortszeichen", bool(schalter), str(
    [str(k.cget("text")) for k in knoepfe(app.content)][:8]))
if schalter:
    schalter[0].invoke()
    tick()
    check("ausgeblendet bleiben keine Ortszeichen stehen",
          len(app.map_canvas.find_withtag("weltort")) == 0,
          f"{vorher_orte} -> {len(app.map_canvas.find_withtag('weltort'))}")
    app._toggle_buildings()
    tick()
    check("wieder eingeblendet sind es so viele wie vorher",
          len(app.map_canvas.find_withtag("weltort")) == vorher_orte,
          f"{len(app.map_canvas.find_withtag('weltort'))} statt {vorher_orte}")

root.destroy()
sys.exit(bericht())
