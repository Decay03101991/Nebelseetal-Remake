"""Misst die Siedlungsansicht im ECHTEN Fenster - Auftrag Nr. 7 (Antwort von Claude, 12.11.2026).

Warum es dieses Werkzeug gibt: Claudes Antwort auf Auftrag Nr. 7 rechnet mit einer sichtbaren
Flaeche von 1037 x 589 und mit 22-px-Feldern auf der Siedlungskarte. Beides sind Angaben von MIR
(Register 496/497) - die Felder der Siedlungskarte sind aber 64 px gross. Vor dem Einbau muss
gemessen sein, was wirklich im Fenster steht.

Gemessen wird je Fenstergroesse:
  * sichtbare Inhaltsflaeche (der scrollbare Rahmen) und die Hoehe seines Inhalts,
  * die Siedlungskarte (Wunschmass und gemessenes Mass, Feldgroesse, Raster),
  * jeder Block im Inhalt mit y-Lage und Hoehe - damit ist belegt, was UEBER und UNTER der
    Karte steht (Claudes offene Frage: "Was unter der Flaeche steht, ist UNBEKANNT"),
  * Kopfzeile, Menuespalte und Statuszeile mit Hoehe und Hintergrundfarbe.

Aufruf:
    python -X utf8 tools/messe_gebaeudeansicht.py                # 1460x940, 1560x1040, 1000x940
    python -X utf8 tools/messe_gebaeudeansicht.py 1300x900       # eigene Groesse
Ergebnis: Klartext auf der Konsole (keine Datei, kein Netz, keine Kosten).
"""
import os
import sys
import tkinter as tk

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HIER, "..", "src"))

import main  # noqa: E402  (Pfad muss vorher stehen)


def _bedienung(widget):
    """Kurzbeschreibung eines Widgets fuer den Bericht (Klasse + Text)."""
    klasse = widget.winfo_class()
    text = ""
    try:
        text = str(widget.cget("text"))
    except Exception:  # noqa: BLE001 - Canvas/Frame haben keinen Text
        text = ""
    text = " ".join(text.split())[:48]
    return klasse, text


def messen(breite, hoehe):
    """Baut das Fenster in der gewuenschten Groesse, oeffnet die Siedlungskarte und misst."""
    root = tk.Tk()
    root.geometry("%dx%d+20+20" % (breite, hoehe))
    try:
        root.attributes("-alpha", 0.01)          # unsichtbar, aber vermessbar
    except Exception:  # noqa: BLE001
        pass
    root.update()
    app = main.NebelseetalApp(root)
    app._build_main_ui()
    app._erste_siedlung_gruenden()
    for _ in range(3):
        root.update()
        root.update_idletasks()
    siedlung = next((s for s in app.state.settlements if getattr(s, "karte", None)), None)
    if siedlung is None:
        print("KEINE Siedlung mit Karte - Abbruch")
        root.destroy()
        return
    app._oeffne_siedlungskarte(siedlung)
    for _ in range(6):
        root.update()
        root.update_idletasks()

    print("=" * 78)
    print("FENSTER %dx%d  (root gemessen %dx%d)" % (
        breite, hoehe, root.winfo_width(), root.winfo_height()))
    print("=" * 78)

    inhalt = app.content_canvas
    print("sichtbare Inhaltsflaeche (content_canvas): %d x %d px" % (
        inhalt.winfo_width(), inhalt.winfo_height()))
    bbox = inhalt.bbox("all")
    if bbox:
        print("Inhalt im Rollbereich: x %d..%d  y %d..%d  -> Hoehe %d px" % (
            bbox[0], bbox[2], bbox[1], bbox[3], bbox[3] - bbox[1]))
    if app._content_fenster is not None:
        try:
            print("Inhaltsrahmen (Fenster im Canvas): %d x %d px" % (
                int(inhalt.itemcget(app._content_fenster, "width") or 0),
                app.content.winfo_height()))
        except Exception:  # noqa: BLE001
            pass

    # ---- Kopfzeile, Menuespalte, Statuszeile: die drei festen Bereiche -------------
    print("\n-- feste Bereiche (Kinder des Hauptfensters) --")
    for kind in root.winfo_children():
        klasse, text = _bedienung(kind)
        print("  %-22s %4d x %4d  bei (%4d,%4d)  bg=%s" % (
            klasse, kind.winfo_width(), kind.winfo_height(),
            kind.winfo_x(), kind.winfo_y(), _bg(kind)))
        if klasse in ("Frame", "Panedwindow") and kind.winfo_height() > 40:
            for enkel in kind.winfo_children():
                ek, et = _bedienung(enkel)
                if ek in ("Frame", "Canvas", "Label") and enkel.winfo_width() > 20:
                    print("     %-19s %4d x %4d  bei (%4d,%4d)  bg=%s  %s" % (
                        ek, enkel.winfo_width(), enkel.winfo_height(),
                        enkel.winfo_x(), enkel.winfo_y(), _bg(enkel), et))

    # ---- die Siedlungskarte selbst -------------------------------------------------
    print("\n-- Siedlungskarte --")
    karte = siedlung.karte
    print("  Raster laut Spielstand: %s x %s Felder" % (karte.get("spalten"), karte.get("zeilen")))
    zelle = getattr(app, "_letzte_zelle", None)
    canv = None
    for kind in app.content.winfo_children():
        canv = _tiefste_leinwand(kind, mindest_breite=300)
        if canv is not None:
            break
    if canv is not None:
        print("  Zeichenflaeche: Wunsch %d x %d px, gemessen %d x %d px" % (
            int(float(canv.cget("width") or 0)), int(float(canv.cget("height") or 0)),
            canv.winfo_width(), canv.winfo_height()))
        print("  Lage im Inhalt: y = %d px (Kartenoberkante)" % _lage_im_content(canv, app))
        print("  Objekte auf der Flaeche: %d" % len(canv.find_all()))
    else:
        print("  KEINE Zeichenflaeche gefunden")

    # ---- jeder Block im Inhalt: was steht ueber, was unter der Karte ----------------
    print("\n-- Bloecke im Inhalt (Reihenfolge von oben nach unten) --")
    bloecke = []
    for kind in app.content.winfo_children():
        klasse, text = _bedienung(kind)
        bloecke.append((kind.winfo_y(), kind.winfo_height(), kind.winfo_width(),
                        klasse, text, kind))
    bloecke.sort()
    for y, h, w, klasse, text, kind in bloecke:
        print("  y=%4d  h=%4d  w=%4d  %-8s %s" % (y, h, w, klasse, text or _kurz(kind)))
    if bloecke:
        print("  Summe der Hoehen im Inhalt: %d px" % sum(b[1] for b in bloecke))

    # ---- Mechanik: traegt jedes Feld eine Gelaendeart? ------------------------------
    print("\n-- Mechanik-Fragen aus Claudes Antwort --")
    raster = karte.get("raster") or {}
    werte = list(raster.values()) if isinstance(raster, dict) else list(raster)
    print("  Felder im Raster: %d, davon mit Gelaendeart: %d" % (
        len(werte), sum(1 for w in werte if w not in (None, ""))))
    arten = sorted({str(w) for w in werte})
    print("  vorkommende Gelaendearten: %s" % ", ".join(arten[:9]))
    # Wie viele Felder belegt ein Bauwerk? GEMESSEN am Spielstand: `bauten` ist ein Woerterbuch
    # mit dem FELDSCHLUESSEL als Schluessel - ein Bauwerk hat also genau einen Eintrag.
    bauten = dict(getattr(siedlung, "bauten", None) or {})
    gueltig = 0
    for schluessel in bauten:
        try:
            int(str(schluessel).split(",")[0])
            gueltig += 1
        except ValueError:
            continue
    print("  Bauwerke im Spielstand: %d, davon mit Feldkoordinate als Schluessel: %d -> "
          "je Bauwerk 1 Feld" % (len(bauten), gueltig))
    print("  Bildschirm des Rechners: %d x %d px (Tk, logisch)" % (
        root.winfo_screenwidth(), root.winfo_screenheight()))
    root.destroy()


def _bg(widget):
    """Hintergrundfarbe eines Widgets (leer, wenn es keine hat)."""
    try:
        return str(widget.cget("bg"))
    except Exception:  # noqa: BLE001
        return "-"


def _kurz(widget):
    """Kurzhinweis fuer Widgets ohne Text (z. B. Canvas mit Kindern)."""
    try:
        return "%d Kinder" % len(widget.winfo_children())
    except Exception:  # noqa: BLE001
        return ""


def _tiefste_leinwand(widget, mindest_breite=300, tiefe=0):
    """Sucht die grosse Zeichenflaeche (die Siedlungskarte) im Baum."""
    if widget.winfo_class() == "Canvas" and widget.winfo_width() >= mindest_breite:
        return widget
    if tiefe > 3:
        return None
    for kind in widget.winfo_children():
        treffer = _tiefste_leinwand(kind, mindest_breite, tiefe + 1)
        if treffer is not None:
            return treffer
    return None


def _lage_im_content(widget, app):
    """y-Abstand der Oberkante im Inhaltsrahmen (ueber alle Eltern zusammengezaehlt)."""
    y = 0
    knoten = widget
    while knoten is not None and knoten is not app.content:
        y += knoten.winfo_y()
        knoten = knoten.master
    return y


if __name__ == "__main__":
    groessen = []
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            b, h = arg.lower().split("x")
            groessen.append((int(b), int(h)))
    else:
        groessen = [(1460, 940), (1560, 1040), (1000, 940)]
    for b, h in groessen:
        messen(b, h)
