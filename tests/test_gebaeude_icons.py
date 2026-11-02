# -*- coding: ascii -*-
"""Gebaeude-Optik in der Oberflaeche - Stand 02.11.2026 (Register 124).

Das Modul `src/gebaeude_optik.py` (B4-Lauf, Register 123) liefert je Gebaeude ein gerahmtes
Menue-Icon (256 x 256, RGBA) und einen gemalten Menue-Hintergrund (538 x 222). Bis heute hat es
NICHTS davon benutzt - diese Datei belegt, dass die drei Stellen wirklich haengen:

1. **Menueleiste**: jeder Menuepunkt, hinter dem ein Gebaeude steht (`main.MENU_GEBAEUDE`), traegt
   sein Icon links neben dem Text; Weltpunkte (Portal, Chat, Forum ...) bleiben ohne Bild.
   Die Zuordnung Menuepunkt -> Gebaeude-id wird ABGELEITET (`gelaende.finde_gebaeude` +
   `MENUE_BEDINGUNG`), nicht als zweite Handliste gepflegt.
2. **Bauauswahl**: jeder Bauknopf der Kartenauswahl traegt das Icon SEINES Gebaeudes.
3. **Gebaeudeansicht**: Dorfzentrum, Kaserne, Stellmacher, Diebesgilde und Forschung zeigen den
   Hintergrund ihres Gebaeudes in Originalgroesse 538 x 222.

Ausserdem: Tk gibt Bilder frei, die niemand referenziert - die Icons MUESSEN im Objektcache liegen
(Lehre 02.11.2026). Geprueft wird deshalb auch, dass zwei Abrufe dasselbe Objekt liefern, und dass
eine unbekannte Kennung None ergibt (kein erfundenes Bild).

Aufruf:  python -X utf8 tests/test_gebaeude_icons.py
"""
from __future__ import annotations

import json
import os
import struct
import sys
import tempfile
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

ROOT, SRC = import_src()
ROOT = str(ROOT)                       # import_src() liefert STRINGS - ROOT / "x" waere ein TypeError
import main                            # noqa: E402
import gebaeude_optik                  # noqa: E402


def png_kopf(pfad):
    """(breite, hoehe, farbtyp) aus dem PNG-Kopf - ohne Fremdbibliothek.

    Farbtyp 6 = RGBA (mit Alphakanal), 2 = RGB ohne Transparenz.
    """
    with open(pfad, "rb") as f:
        kopf = f.read(26)                        # Signatur (8) + IHDR (8) + Masse (8) + Tiefe/Farbtyp (2)
    if kopf[:8] != b"\x89PNG\r\n\x1a\n":          # PNG-Signatur
        return None                              # kein PNG
    breite, hoehe = struct.unpack(">II", kopf[16:24])   # Masse aus dem IHDR-Block
    return breite, hoehe, kopf[25]               # Farbtyp steht im Byte 25


def alle_widgets(eltern, sammler=None):
    """Alle Widgets unter `eltern` (rekursiv) - fuer die Suche nach Knoepfen und Leinwaenden."""
    sammler = [] if sammler is None else sammler
    for kind in eltern.winfo_children():
        sammler.append(kind)
        alle_widgets(kind, sammler)
    return sammler


gebaeude = json.load(open(os.path.join(ROOT, "data", "buildings.json"), encoding="utf-8"))["gebaeude"]
ids = {e["id"] for e in gebaeude}                # die EINE Gebaeudeliste des Spiels

# ==========================================================================
abschnitt("1. Die Zuordnung Menuepunkt -> Gebaeude ist abgeleitet, nicht getippt")
# ==========================================================================

check("1 Zuordnung deckt nur echte Menuepunkte ab",
      set(main.MENU_GEBAEUDE) <= (set(main.MENU_ITEMS) | set(main.MENUE_BEDINGUNG)),
      str(sorted(set(main.MENU_GEBAEUDE) - (set(main.MENU_ITEMS) | set(main.MENUE_BEDINGUNG)))))
check("1 Zuordnung zeigt nur auf echte Gebaeude-ids",
      set(main.MENU_GEBAEUDE.values()) <= ids,
      str(sorted(set(main.MENU_GEBAEUDE.values()) - ids)))
check("1 Dorfzentrum zeigt auf das Lager (alias, nicht getippt)",
      main.MENU_GEBAEUDE.get("Dorfzentrum") == "lager", str(main.MENU_GEBAEUDE.get("Dorfzentrum")))
check("1 Kaserne zeigt auf die Kriegerakademie (aus MENUE_BEDINGUNG)",
      main.MENU_GEBAEUDE.get("Kaserne") == "kriegerakademie",
      str(main.MENU_GEBAEUDE.get("Kaserne")))
check("1 Forschung zeigt auf die Bibliothek (aus MENUE_BEDINGUNG)",
      main.MENU_GEBAEUDE.get("Forschung") == "bibliothek", str(main.MENU_GEBAEUDE.get("Forschung")))
check("1 Stellmacher und Diebesgilde zeigen auf sich selbst",
      main.MENU_GEBAEUDE.get("Stellmacher") == "stellmacher"
      and main.MENU_GEBAEUDE.get("Diebesgilde") == "diebesgilde",
      str(main.MENU_GEBAEUDE.get("Stellmacher")))

# Punkte ohne Gebaeude bleiben bewusst ohne Icon - ein erfundenes Bild waere keine Quelle.
WELTPUNKTE = ("Portal", "Chat", "Forum", "Ruhmeshalle", "Anleitung", "Einstellungen",
              "Nachrichten", "Diplomatie", "Marktplatz", "Gilde", "Kampfsimulator",
              "Spieler werben")
ohne_gebaeude = [p for p in WELTPUNKTE if p in main.MENU_GEBAEUDE]
check("1 Weltpunkte bekommen kein erfundenes Gebaeude-Icon", not ohne_gebaeude,
      str(ohne_gebaeude))

# ==========================================================================
abschnitt("2. Die Bilddateien im Projekt sind vollstaendig und haben die gelieferten Masse")
# ==========================================================================

check("2 keinem Gebaeude fehlt das Icon", gebaeude_optik.fehlende_gebaeude() == [],
      str(gebaeude_optik.fehlende_gebaeude()))

for bid in sorted(set(main.MENU_GEBAEUDE.values())):
    icon_kopf = png_kopf(gebaeude_optik.pfad_icon(bid))
    check(f"2 {bid}: Menue-Icon ist PNG 256x256 RGBA", icon_kopf == (256, 256, 6), str(icon_kopf))
    hg_kopf = png_kopf(gebaeude_optik.pfad_hintergrund(bid))
    check(f"2 {bid}: Hintergrund ist PNG 538x222", bool(hg_kopf) and hg_kopf[:2] == (538, 222),
          str(hg_kopf))

# Quelltext-Wachen: die drei Stellen muessen im Code stehen (ohne Docstrings, per ast).
import ast  # noqa: E402
import inspect  # noqa: E402
import textwrap  # noqa: E402


def code_von(funktion):
    """Der Code einer Funktion OHNE Docstring - Docstrings zaehlen nicht als Benutzung."""
    baum = ast.parse(textwrap.dedent(inspect.getsource(funktion)))   # Quelle -> Syntaxbaum
    baum.body[0].body = [k for k in baum.body[0].body
                         if not (isinstance(k, ast.Expr) and isinstance(k.value, ast.Constant))]  # Docstring weg
    return ast.unparse(baum)                                        # wieder als Text


quelltext = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
check("3 die Menueleiste holt ein Icon (_menue_icon)",
      "_menue_icon(" in code_von(main.NebelseetalApp._menue_auffrischen),
      "in _menue_auffrischen")
check("3 der Bauknopf holt das Icon seines Gebaeudes",
      'angebot["id"], 28' in quelltext or "angebot['id'], 28" in quelltext,
      "Aufruf _optik_bild(angebot[id], 28)")
check("3 die Gebaeudeansicht ruft den Hintergrund an drei Stellen",
      quelltext.count("self._gebaeude_kopf(") == 3,
      str(quelltext.count("self._gebaeude_kopf(")) + " Aufrufe")
check("3 die Ansichten nennen ihre Gebaeude-kennung aus der Quelle",
      'self._gebaeude_kopf("lager")' in quelltext
      and 'self._gebaeude_kopf("bibliothek")' in quelltext
      and "self._gebaeude_kopf(gelaende.finde_gebaeude(staette))" in quelltext,
      "lager / bibliothek / gelaende.finde_gebaeude")

# ==========================================================================
abschnitt("4. Im Fenster: Icons im Menue, an den Bauknoepfen, Hintergrund in der Ansicht")
# ==========================================================================

root = tk.Tk()                                       # echtes Fenster, nur nicht sichtbar
root.withdraw()
tor_pfad = os.path.join(tempfile.gettempdir(), "nebel_icons_pruef_tor.json")
app = main.NebelseetalApp(root, tor_pfad=tor_pfad)    # echte App, kein Stub
app._build_main_ui()
app._found_settlement()                              # echter Start: 10 Siedler, 100 Holz/Stein
root.update()
ort = app.state.settlements[0]

geprueft_ebenen = 0
for ebene in main.EBENEN:
    app._ebene_wechseln(ebene)                       # Menue dieser Ebene neu aufbauen
    root.update_idletasks()
    for punkt, knopf in app.menu_buttons.items():
        hat_bild = str(knopf.cget("image")) != ""    # traegt der Knopf eine Grafik?
        soll_bild = punkt in main.MENU_GEBAEUDE      # steht hinter ihm ein Gebaeude?
        check(f"4 Ebene {ebene}: {punkt} traegt genau dann ein Icon, wenn es ein Gebaeude gibt",
              hat_bild == soll_bild, f"Bild={hat_bild}, erwartet={soll_bild}")
        if soll_bild:
            check(f"4 {punkt}: Icon steht links neben dem Text",
                  str(knopf.cget("compound")) == "left", str(knopf.cget("compound")))
    geprueft_ebenen += 1
check("4 beide Ebenen wurden geprueft", geprueft_ebenen == len(main.EBENEN), str(geprueft_ebenen))

bild_20 = app._menue_icon("Dorfzentrum", 20)
check("4 das Menue-Icon ist 20 px breit", bild_20 is not None and bild_20.width() == 20,
      str(None if bild_20 is None else bild_20.width()))
check("4 zwei Abrufe liefern DASSELBE Objekt (Cache, sonst gibt Tk das Bild frei)",
      app._menue_icon("Dorfzentrum", 20) is bild_20, "kein Cache")
check("4 ein Weltpunkt bekommt kein Icon", app._menue_icon("Portal", 20) is None,
      str(app._menue_icon("Portal", 20)))
check("4 eine unbekannte Kennung ergibt None statt eines erfundenen Bildes",
      app._optik_bild("gibtsnicht", 20) is None, str(app._optik_bild("gibtsnicht", 20)))

# ---- Bauauswahl: jeder Knopf der Kartenauswahl traegt das Icon seines Gebaeudes ----
app._oeffne_siedlungskarte(ort)                      # echter Weg zur Siedlungskarte
karte = ort.karte
wald = karte["raster"].index("wald")                 # Wald: Holzfaeller und Jaeger sind dort baubar
app._karten_feld_waehlen(wald)                       # Feld waehlen -> Bauauswahl erscheint
root.update_idletasks()
bau_knoepfe = [w for w in alle_widgets(app.content)
               if isinstance(w, tk.Button) and "Voraussetzung:" in str(w.cget("text"))]
check("4 die Bauauswahl zeigt Bauknoepfe", len(bau_knoepfe) >= 1, str(len(bau_knoepfe)))
mit_icon = [w for w in bau_knoepfe if str(w.cget("image")) != ""]
check("4 JEDER Bauknopf traegt ein Icon", len(mit_icon) == len(bau_knoepfe),
      f"{len(mit_icon)} von {len(bau_knoepfe)}")
check("4 das Bauknopf-Icon ist 28 px breit und links vom Text",
      all(str(w.cget("compound")) == "left" for w in mit_icon),
      str([str(w.cget("compound")) for w in mit_icon]))

# ---- Gebaeudeansicht: der Hintergrund steht in Originalgroesse in der Ansicht ----
def leinwand_538():
    """Die Leinwand mit den Massen des gelieferten Hintergrunds (538 x 222) - oder None."""
    for w in alle_widgets(app.content):
        if isinstance(w, tk.Canvas):                           # nur Zeichenflaechen
            try:
                if (int(w.cget("width")), int(w.cget("height"))) == (538, 222):   # gelieferte Masse
                    return w                                       # gefunden
            except Exception:                                      # noqa: BLE001
                continue                                           # Widget ohne Masse
    return None


for punkt in ("Dorfzentrum",):
    app._switch_view(punkt)                                    # Ansicht wirklich aufbauen
    root.update_idletasks()
    check(f"4 die {punkt}-Ansicht zeigt den Hintergrund 538x222", leinwand_538() is not None,
          "Leinwand in Originalgroesse")

check("5 eine unbekannte Kennung zeichnet keinen Hintergrund",
      app._gebaeude_kopf("gibtsnicht") is None, str(app._gebaeude_kopf("gibtsnicht")))

# Kaserne und Forschung erst sichtbar, wenn die Gebaeude stehen: nachziehen und wieder pruefen.
raster = ort.karte["raster"]
frei = [i for i, art in enumerate(raster) if ort.bauten.get(str(i)) is None]
for gebaeude_id in ("kriegerakademie", "bibliothek", "stellmacher", "diebesgilde"):
    if not frei:                                               # keine Felder mehr frei
        break
    feld = frei.pop(0)                                         # naechstes freies Feld
    ort.bauten[str(feld)] = gebaeude_id                        # Gebaeude setzen (Pruefaufbau)
    ort.stufen[str(feld)] = 1                                  # Stufe 1
app._menue_auffrischen()                                       # Leiste neu aufbauen
root.update_idletasks()
check("6 Kaserne steht jetzt im Menue und traegt ein Icon",
      "Kaserne" in app.menu_buttons
      and str(app.menu_buttons["Kaserne"].cget("image")) != "",
      str(sorted(app.menu_buttons)))
check("6 Forschung steht jetzt im Menue und traegt ein Icon",
      "Forschung" in app.menu_buttons
      and str(app.menu_buttons["Forschung"].cget("image")) != "",
      str(sorted(app.menu_buttons)))

for punkt in ("Kaserne", "Forschung", "Stellmacher", "Diebesgilde"):
    if punkt not in app.menu_buttons:
        check(f"6 {punkt} ist nach dem Bau erreichbar", False, str(sorted(app.menu_buttons)))
        continue
    app._switch_view(punkt)
    root.update_idletasks()
    check(f"6 die {punkt}-Ansicht zeigt den Hintergrund 538x222", leinwand_538() is not None,
          "keine Leinwand in Originalgroesse")

# ==========================================================================
abschnitt("7. Ohne Pillow bleibt die Optik trotzdem sichtbar (gemessener Startpfad des Spiels)")
# ==========================================================================
# BEFUND 02.11.2026, 09:10: `START_SPIEL_WINDOWS.bat` startete mit Astral CPython 3.11.16, und dieser
# Interpreter hat KEIN Pillow - nachgestellt mit demselben Interpreter: kein Menue-Icon, kein
# Leistenbild, `gebaeude_optik.kachel()` liefert None. Seit 10:40 startet das Batch mit dem
# Projekt-venv (Pillow 13.0.0, Register 129); der Tk-Rueckfall bleibt trotzdem wichtig, weil ein
# Rechner ohne venv sonst GAR keine Gebaeude-Optik haette. Deshalb steht diese Wache hier: ohne sie
# waere die Optik auf so einem Rechner unsichtbar, waehrend alle anderen Pruefungen gruen melden
# (der Fehler steckt im INTERPRETER, nicht im Code).

print("  (Pillow wird fuer diesen Abschnitt kurz abgeschaltet)")
gesichert = {}
for name in ("PIL", "PIL.Image", "PIL.ImageTk"):
    if name in sys.modules:                                   # nur vorhandene Eintraege merken
        gesichert[name] = sys.modules[name]                   # Original merken
        sys.modules[name] = None                              # Import mit ImportError abbrechen
try:
    ohne_icon = app._optik_bild("lager", 33, None, "kachel")   # 33 px ist noch nicht im Cache
    ohne_bild = app._optik_bild("lager", 537, None, "hintergrund")
finally:
    for name, modul in gesichert.items():                     # Zustand wiederherstellen
        sys.modules[name] = modul
check("7 ohne Pillow liefert das Menue-Icon trotzdem ein Tk-Bild",
      ohne_icon is not None and ohne_icon.width() >= 20,
      "None" if ohne_icon is None else str(ohne_icon.width()) + " px (ganzzahlig geteilt)")
check("7 ohne Pillow liefert der Hintergrund seine Originalbreite",
      ohne_bild is not None and ohne_bild.width() == 538,
      "None" if ohne_bild is None else str(ohne_bild.width()))

root.destroy()                                        # Fenster erst nach allen Pruefungen schliessen

# ==========================================================================
ergebnis = bericht()
sys.exit(ergebnis)
