# -*- coding: ascii -*-
"""Gebaeudemotiv als Ansichts-HINTERGRUND (B-6, Vorgabe Daniel 02.11.2026).

VORGABE Daniel 02.11.2026: "die bilder fuer dorfzentrum oder Stellmacher oder Kriegerakademi sollen die
hintergruende werden von den jeweiligen fenstern und nicht einfach als bild oben drueber" und "Die texte
muessen erkennbar bleiben also kleinere textbloecke die nicht transparent sind und der rest so transparent
das moeglichst viel vom bild durchkommt". Nach dem Vergleichsblatt (docs/design/HINTERGRUND_VERGLEICH_20261102.png)
hat Daniel Fassung B gewaehlt: Bild in voller Helligkeit als Hintergrund, Texte in deckenden Kaesten.

Was diese Datei beweist
-----------------------
1. Die Masse und die Abdunkelung stehen in der Datendatei (`data/gebaeude_motive.json`,
   `ansicht_hintergrund`) - Daniels Wahl B heisst `abdunkeln_prozent` 0.
2. `gebaeude_optik.hintergrund_flaeche` DECKT die Flaeche (cover): das Ergebnis hat genau die
   geforderte Groesse, nichts wird verzerrt, und eine Abdunkelung wirkt messbar auf die Helligkeit.
3. Ohne Bild (unbekannte Kennung, Schalter aus) entsteht KEINE Flaeche - die Ansicht bleibt wie vorher,
   nichts stuerzt ab.
4. Die drei betroffenen Ansichten legen die Flaeche ZUERST an (sonst deckt sie den Titel): die erste
   Flaeche im Inhalt ist die Hintergrund-Leinwand, und die Ueberschrift steht danach.
5. Der alte Kopf (`_gebaeude_kopf`) ist nur noch Rueckfall, wenn kein Bild da ist.

Aufruf:  python -X utf8 tests/test_ansicht_hintergrund.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src

ROOT, SRC = import_src()
import gebaeude_optik as G  # noqa: E402
import main as M  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()


# ==========================================================================
# 1. Die Zahlen stehen in der Datendatei
# ==========================================================================

abschnitt("1. Masse und Abdunkelung kommen aus der Datendatei")
_e = M.hintergrund_einstellungen()
check("der Schalter ist an", _e.get("aktiv") is True, str(_e.get("aktiv")))
# UMGESTELLT 02.11.2026: Daniel hat nach dem ersten Einbau nachgeschaerft - "das hintergrundbild ist
# noch zu sehr blickfangend ... die texte muessen ... der Vordergrund sein". Also ist das Bild jetzt
# zurueckgenommen (abgedunkelt UND weichgezeichnet) statt in voller Helligkeit (Wahl B von vorher).
check("das Bild ist zurueckgenommen (Abdunkelung groesser 0)",
      float(_e.get("abdunkeln_prozent") or 0.0) > 0.0, str(_e.get("abdunkeln_prozent")))
check("das Bild ist weichgezeichnet (nimmt harte Kontraste weg)",
      float(_e.get("weichzeichnen_px") or 0.0) > 0.0, str(_e.get("weichzeichnen_px")))
_k = _e.get("kasten") if isinstance(_e.get("kasten"), dict) else {}
check("die Textfelder sind nahezu deckend (oben mindestens 220 von 255)",
      int(_k.get("oben_deckkraft") or 0) >= 220, str(_k.get("oben_deckkraft")))
check("die Textfelder haben eine warme eigene Farbe",
      isinstance(_k.get("farbe"), (list, tuple)) and len(_k.get("farbe")) == 3, str(_k.get("farbe")))
check("die Textfelder haben abgerundete Ecken (Radius mindestens 8)",
      int(_k.get("radius") or 0) >= 8, str(_k.get("radius")))
check("die Flaeche hat eine Breite", int(_e.get("breite") or 0) > 0, str(_e.get("breite")))
check("die Flaeche hat eine Hoehe", int(_e.get("hoehe") or 0) > 0, str(_e.get("hoehe")))
check("die Datendatei nennt den Grund (Daniels Vorgabe)",
      "hintergrund" in str(_e.get("_zweck") or "").lower(), str(_e.get("_zweck"))[:80])


# ==========================================================================
# 2. Die Flaeche deckt und wird bei Bedarf abgedunkelt
# ==========================================================================

abschnitt("2. Das Bild deckt die Flaeche (cover) statt sie einzupassen")
_flaeche = G.hintergrund_flaeche("lager", 980, 760)
check("eine Flaeche entsteht", _flaeche is not None)
if _flaeche is not None:
    check("die Flaeche hat genau die geforderte Groesse",
          _flaeche.size == (980, 760), str(_flaeche.size))
    check("die Flaeche ist RGB (deckend, kein Alpha)", _flaeche.mode == "RGB", _flaeche.mode)
    _klein = G.hintergrund_flaeche("lager", 200, 500)               # anderes Seitenverhaeltnis
    check("auch ein hochkantiges Mass wird gedeckt, nicht verzerrt",
          _klein is not None and _klein.size == (200, 500), str(_klein.size if _klein else None))


def _helligkeit(bild):
    """Mittlere Helligkeit einer Flaeche - messbar, nicht geschaetzt."""
    grau = bild.convert("L")
    werte = list(grau.getdata())
    return sum(werte) / float(len(werte))


_offen = G.hintergrund_flaeche("lager", 300, 200, 0.0)
_dunkel = G.hintergrund_flaeche("lager", 300, 200, 60.0)
check("ohne Abdunkelung bleibt das Bild hell", _helligkeit(_offen) > 20, str(round(_helligkeit(_offen), 1)))
check("60 % Abdunkelung macht die Flaeche deutlich dunkler",
      _helligkeit(_dunkel) < _helligkeit(_offen) * 0.6,
      "%s -> %s" % (round(_helligkeit(_offen), 1), round(_helligkeit(_dunkel), 1)))
check("100 % Abdunkelung ist fast schwarz", _helligkeit(G.hintergrund_flaeche("lager", 100, 80, 100.0)) < 3)


# ==========================================================================
# 3. Ohne Bild keine Flaeche - und kein Absturz
# ==========================================================================

abschnitt("3. Ohne Bild bleibt die Ansicht, wie sie war")
check("eine unbekannte Kennung liefert keine Flaeche",
      G.hintergrund_flaeche("gibtesnicht", 400, 300) is None)
check("ein fehlendes Bild stuerzt nicht ab",
      G.hintergrund_flaeche("", 400, 300) is None)
check("eine unsinnige Groesse liefert trotzdem ein Bild oder None",
      G.hintergrund_flaeche("lager", 0, 0) is None
      or G.hintergrund_flaeche("lager", 0, 0).size[0] >= 1)


# ==========================================================================
# 4. Die Ansichten legen den Hintergrund ZUERST an
# ==========================================================================

abschnitt("4. Die drei Ansichten: Hintergrund zuerst, dann der Inhalt")
for _name in ("_render_overview", "_render_research", "_render_ausbildung"):
    # Die Methode wird ueber ihren NAMEN aufgerufen - der steht in co_names, nicht in co_consts.
    _namen = M.NebelseetalApp.__dict__[_name].__code__.co_names
    check("%s ruft die Hintergrund-Ebene" % _name, "_ansicht_hintergrund" in _namen, str(_namen[:6]))
check("der alte Kopf ist nur noch Rueckfall",
      TEXT_MAIN.count("if self._ansicht_hintergrund(") == 3, str(TEXT_MAIN.count("if self._ansicht_hintergrund(")))
check("das Dorfzentrum nimmt das Motiv 'lager'", 'self._ansicht_hintergrund("lager")' in TEXT_MAIN)
check("die Forschung nimmt das Motiv 'bibliothek'", 'self._ansicht_hintergrund("bibliothek")' in TEXT_MAIN)
check("die Ausbildungsstaetten nehmen ihr Gebaeude",
      "_ansicht_hintergrund(gelaende.finde_gebaeude(staette))" in TEXT_MAIN)


def _ansichtsprobe():
    """Eine echte Ansicht bauen und pruefen, dass die Hintergrund-Leinwand die ERSTE Flaeche ist."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    try:
        app = M.NebelseetalApp(root)
        app._build_main_ui()
        app._erste_siedlung_gruenden()
        ergebnis = {}
        for name in ("Dorfzentrum", "Forschung"):
            app._switch_view(name)
            app.content.update_idletasks()
            kinder = list(app.content.winfo_children())
            ergebnis[name] = (isinstance(kinder[0], tk.Canvas) if kinder else False,
                              str(kinder[0].cget("width")) if kinder else "",
                              len(kinder))
        return ergebnis
    finally:
        root.destroy()


_probe = _ansichtsprobe()
check("im Dorfzentrum ist die erste Flaeche die Hintergrund-Leinwand",
      _probe.get("Dorfzentrum", (False,))[0] is True, str(_probe.get("Dorfzentrum")))
check("in der Forschung ebenso",
      _probe.get("Forschung", (False,))[0] is True, str(_probe.get("Forschung")))
check("der Inhalt baut weiterhin seine Felder auf",
      _probe.get("Dorfzentrum", (0, 0, 0))[2] > 5, str(_probe.get("Dorfzentrum")))


# ==========================================================================
# 5. M-2: die KAESTENOPTIK gilt auch in Kaserne, Stellmacher und Diebesgilde
# ==========================================================================

abschnitt("5. Die drei Ausbildungsstaetten nutzen die weichen Textfelder (M-2)")
for _name in ("_render_ausbildung", "_siedler_warnung_zeichnen", "_spionage_abschnitt"):
    _namen = M.NebelseetalApp.__dict__[_name].__code__.co_names
    check("%s baut weiche Textfelder" % _name, "_kasten_label" in _namen, str(_namen[:8]))
check("der Titel der Ansicht steht im Kasten", "_kasten_label(titel" in TEXT_MAIN)
check("die Spionage-Ueberschrift steht im Kasten", '_kasten_label("Spionage"' in TEXT_MAIN)
check("die Siedlerwarnung steht im Kasten", '_kasten_label(\n            (f"Freie Siedler: '
      in TEXT_MAIN or 'f"Freie Siedler: {reserve' in TEXT_MAIN)


def _kastenprobe():
    """Die drei Ansichten bauen und zaehlen, wie viele Texte als weiches Feld liegen."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    try:
        app = M.NebelseetalApp(root)
        app._build_main_ui()
        app._erste_siedlung_gruenden()
        ergebnis = {}
        for name in ("Kaserne", "Stellmacher", "Diebesgilde"):
            app._switch_view(name)
            app.content.update_idletasks()
            kinder = list(app.content.winfo_children())
            kaesten = sum(1 for k in kinder if getattr(k, "image", None) is not None)
            texte = []
            for k in kinder:
                try:
                    texte.append(str(k.cget("text")))
                except Exception:                                  # noqa: BLE001
                    continue
            ergebnis[name] = (isinstance(kinder[0], tk.Canvas) if kinder else False,
                              kaesten, " ".join(texte))
        return ergebnis
    finally:
        root.destroy()


_kasten = _kastenprobe()
for _name in ("Kaserne", "Stellmacher", "Diebesgilde"):
    _daten = _kasten.get(_name, (False, 0, ""))
    check("%s legt den Hintergrund als erste Flaeche an" % _name, _daten[0] is True, str(_daten[:2]))
    check("%s hat mindestens zwei weiche Textfelder" % _name, _daten[1] >= 2, str(_daten[:2]))
    check("%s nennt die Ausbildungsstaette noch im Text" % _name,
          "Ausgebildet wird auf der Siedlungskarte" in _daten[2], _daten[2][:120])


# ==========================================================================
# 6. M-3: der Hintergrund folgt der Fenstergroesse (Daniels Befund 02.11.2026)
# ==========================================================================

abschnitt("6. Der Hintergrund waechst mit dem Fenster (M-3)")
check("die Flaeche liegt mit relativer Groesse im Inhalt",
      "relwidth=1.0, relheight=1.0" in TEXT_MAIN)
check("es gibt ein Nachziehen bei Groessenaenderung", "def _hintergrund_anpassen" in TEXT_MAIN)
check("das Bild wird in der Zielgroesse neu gebaut", "def _hintergrund_bauen" in TEXT_MAIN)
check("die Flaeche haengt am Configure-Ereignis", '"<Configure>", lambda _ereignis: self._hintergrund_anpassen()'
      in TEXT_MAIN)


def _hintergrundprobe():
    """Die Ansicht bauen, die Flaeche messen und ein Nachziehen in neuer Groesse pruefen."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    try:
        app = M.NebelseetalApp(root)
        app._build_main_ui()
        app._erste_siedlung_gruenden()
        app._switch_view("Diebesgilde")
        app.content.update_idletasks()
        leinwand = getattr(app, "_hintergrund_flaeche", None)
        if leinwand is None:
            return {"flaeche": False}
        info = leinwand.place_info()
        vorher = getattr(leinwand, "image", None)
        alt = (vorher.width(), vorher.height()) if vorher is not None else (0, 0)
        app._hintergrund_bauen("diebesgilde", 1664, 960, getattr(app, "_hintergrund_einstellung", {}) or {})
        app.content.update_idletasks()
        neu = getattr(leinwand, "image", None)
        return {"flaeche": True, "relwidth": info.get("relwidth"), "relheight": info.get("relheight"),
                "alt": alt, "neu": (neu.width(), neu.height()) if neu is not None else (0, 0),
                "kennung": getattr(app, "_hintergrund_kennung", None),
                "gemerkt": getattr(app, "_hintergrund_groesse", None)}
    finally:
        root.destroy()


_hg = _hintergrundprobe()
check("die Ansicht hat eine Hintergrundflaeche", _hg.get("flaeche") is True, str(_hg))
check("die Flaeche ist relativ gebunden (fuellt den Inhalt)",
      str(_hg.get("relwidth")) in ("1", "1.0") and str(_hg.get("relheight")) in ("1", "1.0"),
      str(_hg))
check("die Flaeche kennt ihr Motiv", _hg.get("kennung") == "diebesgilde", str(_hg.get("kennung")))
check("ein neues Mass baut ein neues Bild in Zielgroesse",
      _hg.get("neu") == (1664, 960), str((_hg.get("alt"), _hg.get("neu"))))
check("die gebaute Groesse wird gemerkt", _hg.get("gemerkt") == (1664, 960), str(_hg.get("gemerkt")))

# ==========================================================================
# 7. M-4: die Warteschlange der Ausbildung liegt als weiches Feld auf dem Bild
# ==========================================================================

abschnitt("7. Die Warteschlange: Kopf und zwei Hinweiszeilen als Kasten, Zeilen deckend (M-4)")
# UMGESTELLT 02.11.2026 (M-4, Vorgabe Daniel: "dann die uebrigen Textfelder", "stueck fuer stueck"):
# Kopfzeile, "Keine Auftraege in Arbeit." und die Reihenfolge-Erklaerung lagen als harte Balken im
# Rahmen. Der Rahmen traegt jetzt NUR noch die Auftragszeilen - er ist die Tabelle und bleibt deckend.
_QUEUE = TEXT_MAIN.split("def _ausbildung_warteschlange_zeichnen")[1].split("\n    def ")[0]
check("die Warteschlange baut weiche Textfelder",
      "_kasten_label" in M.NebelseetalApp.__dict__["_ausbildung_warteschlange_zeichnen"].__code__.co_names,
      str(M.NebelseetalApp.__dict__["_ausbildung_warteschlange_zeichnen"].__code__.co_names[:8]))
check("es sind GENAU die drei Textzeilen (Kopf, Leerfall, Reihenfolge)",
      _QUEUE.count("self._kasten_label(") == 3, str(_QUEUE.count("self._kasten_label(")))
check("die Kopfzeile steht im Kasten", 'f"In Arbeit: {uebersicht' in _QUEUE)
check("der Leerfall steht im Kasten", '"Keine Auftr' in _QUEUE)
check("die Reihenfolge-Erklaerung steht im Kasten", '"Reihenfolge: nacheinander' in _QUEUE)
check("der fruehere harte Balken im Rahmen ist weg", _QUEUE.count("tk.Label(rahmen") == 0,
      str(_QUEUE.count("tk.Label(rahmen")))
check("der Rahmen fuer die Zeilen entsteht nur, wenn Zeilen da sind", "if gruppen:" in _QUEUE)
check("der Rahmen bleibt deckend (Panel-Farbe, nicht der Inhalt)",
      'rahmen = tk.Frame(self.content, bg=self.skin["panel"])' in _QUEUE)


def _warteschlangenprobe(auftraege):
    """Die Kaserne bauen, Auftraege einreihen und die Kindflaechen des Inhalts auszaehlen.

    `auftraege` ist die Liste der Einheiten - VERSCHIEDENE Namen ergeben je eine Zeile
    (gleiche Namen werden gruppiert, siehe `_ausbildung_warteschlange_zeichnen`).
    """
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    try:
        app = M.NebelseetalApp(root)
        app._build_main_ui()
        app._erste_siedlung_gruenden()
        ort = app.state.aktive_siedlung()
        jetzt = float(app.state.spielsekunden)
        ort.ausbildung = [{"einheit": name, "gebaeude": "kriegerakademie", "stufe": 1,
                           "start": jetzt + 3600.0 * n, "ende": jetzt + 3600.0 * (n + 1),
                           "dauer_sekunden": 3600.0} for n, name in enumerate(auftraege)]
        app._switch_view("Kaserne")
        app.content.update_idletasks()
        ergebnis = {"kasten": [], "rahmen": []}
        for k in app.content.winfo_children():
            try:
                text = str(k.cget("text"))
            except Exception:                                  # noqa: BLE001
                text = ""
            if getattr(k, "image", None) is not None:
                ergebnis["kasten"].append(text)
            elif type(k).__name__ == "Frame":
                try:
                    bg = str(k.cget("bg"))
                except Exception:                              # noqa: BLE001
                    bg = ""
                if bg != str(app.skin["bg"]):
                    unter = list(k.winfo_children())
                    rahmen = sum(1 for u in unter if type(u).__name__ == "Frame")
                    ergebnis["rahmen"].append((bg, len(unter), rahmen, text))
        return ergebnis
    finally:
        root.destroy()


_voll = _warteschlangenprobe(["Kaempfer", "Krieger", "Ritter"])
_texte = " | ".join(_voll["kasten"])
check("der Kopf der Warteschlange liegt als Kasten mit Bild",
      any("In Arbeit: 3 Auftrag" in t for t in _voll["kasten"]), _texte[:120])
check("die Reihenfolge-Erklaerung liegt als Kasten mit Bild",
      any("Reihenfolge: nacheinander" in t for t in _voll["kasten"]), _texte[:120])
check("die drei Auftraege stehen in EINEM deckenden Rahmen (ein Zeilenrahmen je Auftrag)",
      any(z[1] == 3 and z[2] == 3 for z in _voll["rahmen"]), str(_voll["rahmen"][:4]))
check("die Auftragszeilen liegen NICHT in einem Kasten",
      not any("Kaempfer" in t for t in _voll["kasten"]), _texte[:160])

_leer = _warteschlangenprobe([])
check("der Leerfall liegt als Kasten mit Bild",
      any("Keine Auftr" in t for t in _leer["kasten"]), str(_leer["kasten"])[:160])
check("ohne Auftraege entsteht kein leerer Zeilenrahmen",
      not any(z[1] == 0 for z in _leer["rahmen"]), str(_leer["rahmen"][:3]))

# ==========================================================================
# 8. M-5: Titel und Einleitung der Forschung liegen als weiches Feld auf dem Bild
# ==========================================================================

abschnitt("8. Die Forschung: Titel und Einleitung als Kasten (M-5)")
# UMGESTELLT 02.11.2026 (M-5): die Bibliothek war hier schon Hintergrund (B-6), Titel und Einleitung
# lagen aber weiter als harte Balken ueber die volle Breite - genau der Zustand, den Daniel an den
# Ausbildungsstaetten bemaengelt hatte.
_FORSCHUNG = TEXT_MAIN.split("def _render_research")[1].split("\n    def ")[0]
check("die Forschungsansicht baut weiche Textfelder",
      "_kasten_label" in M.NebelseetalApp.__dict__["_render_research"].__code__.co_names, "")
check("der Titel steht im Kasten", 'self._kasten_label("Forschung"' in _FORSCHUNG)
check("die Einleitung steht im Kasten", '"Forschung braucht eine Bibliothek und Zeit' in _FORSCHUNG)
check("die Einleitung ist kein harter Balken mehr",
      'bg=self.skin["bg"]' not in _FORSCHUNG, str(_FORSCHUNG.count('bg=self.skin["bg"]')))


def _forschungsprobe():
    """Die Forschung bauen und nachsehen, welche Texte als Kasten mit Bild vorliegen."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    try:
        app = M.NebelseetalApp(root)
        app._build_main_ui()
        app._erste_siedlung_gruenden()
        app._switch_view("Forschung")
        app.content.update_idletasks()
        kinder = list(app.content.winfo_children())
        kaesten = []
        for k in kinder:
            try:
                text = str(k.cget("text"))
            except Exception:                                  # noqa: BLE001
                text = ""
            if getattr(k, "image", None) is not None:
                kaesten.append(text)
        return {"erste": type(kinder[0]).__name__ if kinder else "",
                "kasten": kaesten, "anzahl": len(kaesten)}
    finally:
        root.destroy()


_f = _forschungsprobe()
check("der Hintergrund ist die erste Flaeche", _f["erste"] == "Canvas", _f["erste"])
check("Titel und Einleitung liegen als Kasten mit Bild",
      any(t.strip() == "Forschung" for t in _f["kasten"])
      and any("Stufe zum Quadrat" in t for t in _f["kasten"]), str(_f["kasten"])[:160])
check("die Forschungszeilen bleiben deckend (hoechstens zwei Kasten mehr)",
      _f["anzahl"] <= 3, str(_f["anzahl"]))

bericht()
