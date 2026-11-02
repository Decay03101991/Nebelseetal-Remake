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

bericht()
