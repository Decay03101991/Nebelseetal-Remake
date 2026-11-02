# -*- coding: ascii -*-
"""Truppenbewegungen auf der Weltkarte - Stufe M-1 (02.11.2026, Vorgabe Daniel, Register 140).

VORGABE Daniel 02.11.2026 im Wortlaut: "Truppen kann man sehen von wo nach wo sie laufen auch wie
lange sie laufen aber eine sich bewegende einheit kann ich weder ausspionieren noch weiss ich welche
art truppen. Ein einzelner handkarren erzeugt das gleiche bewegungssymbol wie eine ganze armee. Damit
ich aufgrund der laufgeschwindigkeit nicht weiss welche einheit es wohl sein wird, sieht man nur die
grobe Wegzeit von einheiten bewegungen." Nachtrag: laeuft ein Marsch auf eine EIGENE Siedlung zu,
steht die Wegzeit GENAU da (Verteidigung planbar); Art und Anzahl bleiben auch dann verborgen.

Was diese Datei beweist
-----------------------
1. Sichtbar ist nur das Oeffentliche: je Marsch eine Linie, ein Start- und ein Zielfeld und ein
   Marschzeichen - vier Canvas-Objekte, eigener Sammel-Tag `marsch` und je Marsch `marsch_<n>`.
2. Die Anzeige wird aus `state.auftraege` gespeist (KEINE zweite Auftragsliste) und aus der Spieluhr
   `state.spielsekunden` - nicht aus der Rechnerzeit.
3. Kein Auftrag = keine Linie; nach der Rueckkehr ist die Linie weg.
4. Zwei Maersche gleichzeitig sind zwei Linien (zwei Ziele) und acht Objekte.
5. Uhr rueckwaerts: die Restzeit wird nie negativ, das Zeichen bleibt auf dem Startfeld.
6. Ein Zielname, der nicht im Raster liegt, ergibt KEINE Linie (die Richtung waere erfunden) und
   genau EINE Meldung im Protokoll.
7. Das Klickfenster eines Marsches zeigt von, nach, Restzeit - und KEINE Truppenliste, keine
   Auftragsart, keine Anzahl.
8. Die grobe Restzeit kommt aus Stufen der Datendatei; beim eigenen Ziel steht die GENAUe Zeit.

Aufruf:  python -X utf8 tests/test_marsch_optik.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, bericht, check, import_src

ROOT, SRC = import_src()
import auftraege      # noqa: E402  (der Kern der Auftraege)
import main as M      # noqa: E402  (die Anwendung mit dem Gelaendekaestchen)
import marsch_optik   # noqa: E402  (die Zahlen der Anzeige)

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()      # Quelltext der App
KANTE = 20                                                                   # Rasterweite des Portals

# ==========================================================================
# 1. Quelltext-Wachen: die Anzeige haengt an den vereinbarten Stellen
# ==========================================================================

abschnitt("1. Die Anzeige steht dort, wo die Karte gezeichnet wird")
check("das Zeichnen der Maersche existiert", "def _marsche_zeichnen" in TEXT_MAIN)
check("die Felder werden an EINER Stelle aufgeloest", "def _marsch_felder" in TEXT_MAIN)
check("der Klick findet eine Marschlinie", "def _marsch_an" in TEXT_MAIN)
check("der Klick oeffnet das Marschfenster", "def _marsch_optionen" in TEXT_MAIN)
check("die Karte ruft das Zeichnen auf", "_marsche_zeichnen(zeichenflaeche" in TEXT_MAIN)
check("der Klick prueft erst Dorf, dann Marsch, dann Feld",
      TEXT_MAIN.index("self._bot_dorf_optionen(treffer[0], treffer[1])")
      < TEXT_MAIN.index("marsch = self._marsch_an(x, y, kante)")
      < TEXT_MAIN.index("return self._portal_feld_waehlen(x, y)"))
check("die Maersche haben einen eigenen Sammel-Tag", 'zeichenflaeche.delete("marsch")' in TEXT_MAIN)
check("je Marsch gibt es einen eigenen Tag", '"marsch_%d" % nummer' in TEXT_MAIN)
check("die Anzeige liest die Datendatei", "marsch_optik.optik()" in TEXT_MAIN)
check("die Anzeige liest die EINE Auftragsliste", "auftraege.laufende(self.state.auftraege" in TEXT_MAIN
      or "auftraege.laufende(getattr(self.state, \"auftraege\"" in TEXT_MAIN)
check("das Marschfenster verspricht keine Truppenliste",
      "Truppenart, Anzahl und Karren bleiben verborgen" in TEXT_MAIN)
check("die Restzeit kommt aus dem Kern, nicht aus der Uhr",
      "auftraege.stand(eintrag, jetzt)" in TEXT_MAIN)

# ==========================================================================
# 2. Die Zahlen der Anzeige (Datendatei plus Vorgabe im Code)
# ==========================================================================

abschnitt("2. Die Zahlen der Anzeige stehen in der Datendatei")
OPTIK = marsch_optik.optik()
check("die Datendatei ist vorhanden und lesbar", isinstance(OPTIK, dict) and bool(OPTIK))
check("die Fassung ist benannt", str(OPTIK.get("fassung")) in ("A", "B", "C"), str(OPTIK.get("fassung")))
check("die Linie hat eine Breite in px", int(OPTIK["linie"]["breite_px"]) >= 1)
check("die Hinreise hat eine eigene Farbe", str(OPTIK["linie"]["farbe_hin"]).startswith("#"))
check("die Rueckreise hat eine eigene Farbe", str(OPTIK["linie"]["farbe_rueck"]).startswith("#"))
check("das Marschzeichen hat eine feste Groesse", int(OPTIK["symbol"]["durchmesser_px"]) >= 4)
check("die Groesse ist ausdruecklich konstant", str(OPTIK.get("groesse")) == "konstant")
check("die Restzeit hat vier Stufen", len(OPTIK["restzeit"]["stufen"]) == 4)
check("die Toleranz des Klicks ist gesetzt", float(OPTIK["klick"]["toleranz_px"]) > 0)
check("die Anzeige ist eingeschaltet", marsch_optik.aktiv(OPTIK) is True)
check("fehlende Werte fallen auf die Vorgabe zurueck",
      marsch_optik.restzeit_stufe(10, {"restzeit": {}}) == "unter 1 h")

abschnitt("3. Die grobe und die genaue Restzeit")
for sekunden, erwartet in ((0, "unter 1 h"), (3599, "unter 1 h"), (3600, "1-3 h"),
                           (10800, "3-6 h"), (21599, "3-6 h"), (21600, "ueber 6 h"),
                           (999999, "ueber 6 h"), (-500, "unter 1 h")):
    check("Restzeit %s s ergibt '%s'" % (sekunden, erwartet),
          marsch_optik.restzeit_stufe(sekunden, OPTIK) == erwartet,
          marsch_optik.restzeit_stufe(sekunden, OPTIK))
check("ein fremdes Ziel zeigt die GROBE Stufe",
      marsch_optik.restzeit_text(8100, False, OPTIK) == "1-3 h")
check("ein eigenes Ziel zeigt die GENAUe Zeit",
      marsch_optik.restzeit_text(8100, True, OPTIK) == "2 h 15 min",
      marsch_optik.restzeit_text(8100, True, OPTIK))
check("die genaue Zeit hat immer Stunden und Minuten",
      marsch_optik.restzeit_genau(59, OPTIK) == "0 h 0 min"
      and marsch_optik.restzeit_genau(3600, OPTIK) == "1 h 0 min")
check("keine negative Restzeit in der Anzeige",
      marsch_optik.restzeit_genau(-3600, OPTIK) == "0 h 0 min")

# ==========================================================================
# 4. Geometrie: Trefferband um die Linie
# ==========================================================================

abschnitt("4. Der Klick trifft die Linie, nicht das ganze Feld")
check("ein Punkt AUF der Strecke hat Abstand 0",
      M.NebelseetalApp._punkt_abstand(50, 10, 0, 10, 100, 10) == 0)
check("ein Punkt 5 px daneben hat Abstand 5",
      abs(M.NebelseetalApp._punkt_abstand(50, 15, 0, 10, 100, 10) - 5.0) < 0.001)
check("hinter dem Ende zaehlt der Endpunkt",
      abs(M.NebelseetalApp._punkt_abstand(110, 10, 0, 10, 100, 10) - 10.0) < 0.001)
check("eine Strecke der Laenge 0 ist ein Punkt",
      abs(M.NebelseetalApp._punkt_abstand(3, 4, 0, 0, 0, 0) - 5.0) < 0.001)
check("die Feldgroesse folgt der Rasterweite",
      M.NebelseetalApp._portal_zelle(20) == 20 and M.NebelseetalApp._portal_zelle(10) == 40)

# ==========================================================================
# 5. Die Anwendung: zeichnen, ankommen, zwei Maersche, Uhr rueckwaerts
# ==========================================================================


def _leinwand(app):
    """Die Zeichenflaeche des Gelaendekaestchens (sie traegt die Dorfzeichen)."""
    import tkinter as tk
    for kind in app.content.winfo_children():
        if isinstance(kind, tk.Canvas) and kind.find_withtag("portalbote"):
            return kind
    return None


def _zaehlen(app):
    """Wie viele Marsch-Objekte stehen auf der Karte?"""
    leinwand = _leinwand(app)
    return len(leinwand.find_withtag("marsch")) if leinwand is not None else -1


def _starten(app, dorf, bot, anzahl=5):
    """Einen Angriff als AUFTRAG starten - ueber den Kern, mit echter Entfernung."""
    siedlung = app.state.settlements[0]
    ziel = {"name": str(dorf.name), "fremd": True, "dorf_name": str(dorf.name),
            "bot_name": str(bot.name), "wall_stufe": 0, "wall_zustand_prozent": 100.0}
    ok, meldung = auftraege.starten(app.state.auftraege, "angreifen", {"Krieger": anzahl},
                                    siedlung.name, ziel, 3, float(app.state.spielsekunden))
    return ok, meldung, (app.state.auftraege[-1] if ok else None)


def _probe():
    """Die ganze Szene einmal aufbauen und messen - ohne Fenster sichtbar zu machen."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    try:
        app = M.NebelseetalApp(root)
        app._build_main_ui()
        app._erste_siedlung_gruenden()
        # Die Doerfer tragen ihre Position erst nach dem Auffrischen (0/0 = noch nicht gesetzt).
        # Ohne diesen Schritt liegen ALLE auf einem Feld und die Pruefung waere wertlos.
        app.state.bot_doerfer_auffrischen_alle(float(app.state.spielsekunden))
        doerfer = app._bot_doerfer_im_raster(KANTE)
        if not doerfer:
            return {"zu_wenig_doerfer": 0}
        siedlung = app.state.settlements[0]
        ergebnis: dict = {"doerfer": len(doerfer)}
        start = float(app.state.spielsekunden)

        # (1) ohne Auftrag: keine Linie
        app._switch_view("Portal")
        ergebnis["ohne"] = _zaehlen(app)

        # (2) ein Marsch: vier Objekte, Felder stimmen mit den Positionen ueberein
        bot, dorf = doerfer[0]
        ok, meldung, eintrag = _starten(app, dorf, bot)
        ergebnis["ok"] = ok
        ergebnis["meldung"] = meldung
        ergebnis["felder"] = app._marsch_felder(eintrag, KANTE)
        ergebnis["erwartet"] = ((int(siedlung.x), int(siedlung.y)), (int(dorf.x), int(dorf.y)))
        app._switch_view("Portal")
        ergebnis["einer"] = _zaehlen(app)
        ergebnis["hin_farbe"] = _linienfarbe(app)
        ergebnis["unterwegs"] = _unterwegs_zeile(app)
        ergebnis["reihenfolge"] = _reihenfolge(app)

        # (3) Ankunft: Punkt genau am Ziel, Richtung dreht (Rueckreise)
        app.state.spielsekunden = float(eintrag["ankunft"]) + 1.0
        app._switch_view("Portal")
        ergebnis["rueckreise"] = _zaehlen(app)
        ergebnis["rueck_farbe"] = _linienfarbe(app)

        # (4) nach der Rueckkehr: die Linie ist weg
        app.state.spielsekunden = float(eintrag["rueckkehr"]) + 1.0
        app._switch_view("Portal")
        ergebnis["danach"] = _zaehlen(app)

        # (5) zwei Maersche gleichzeitig auf zwei Ziele - mit LEERER Liste, damit die Zahl eindeutig ist
        app.state.spielsekunden = start
        app.state.auftraege = []                                            # leere Liste fuer den Zaehlfall
        # ZWEI Maersche auf DASSELBE Ziel - der haertere Fall: sie muessen sich versetzen statt
        # deckungsgleich zu liegen. Damit haengt die Pruefung nicht an der Zahl der Bot-Doerfer.
        ok2, _, _ = _starten(app, doerfer[0][1], doerfer[0][0])
        ok3, _, _ = _starten(app, doerfer[0][1], doerfer[0][0])
        app._switch_view("Portal")
        ergebnis["zwei"] = _zaehlen(app)
        ergebnis["zwei_ok"] = (ok2, ok3)
        ergebnis["versatz"] = _linienkoordinaten(app)

        # (6) Uhr rueckwaerts: Restzeit nie negativ, Zeichen bleibt auf dem Startfeld
        vorher = app._marsch_laufend(KANTE)
        app.state.spielsekunden = start - 5000.0
        app._switch_view("Portal")
        ergebnis["rueckwaerts"] = _zaehlen(app)
        ergebnis["rest_nie_negativ"] = all(m["rest"] >= 0.0 for m in app._marsch_laufend(KANTE))
        ergebnis["maersche"] = len(vorher)

        # (7) nicht aufloesbarer Ort: keine Linie, EINE Meldung
        app.state.spielsekunden = start
        fremd = {"art": "angreifen", "von": "Gibt Es Nicht", "nach": "Auch Nicht",
                 "reisezeit": 100.0, "start": start, "ankunft": start + 100.0,
                 "aktion_dauer": 0.0, "rueckkehr": start + 200.0, "ziel": {}, "status": "hinreise"}
        ergebnis["fremd_felder"] = app._marsch_felder(fremd, KANTE)
        vorher_log = len(app.state.log)
        app._marsch_gemeldet(fremd)
        app._marsch_gemeldet(fremd)
        ergebnis["meldungen"] = len(app.state.log) - vorher_log
        ergebnis["meldung_text"] = app.state.log[-1] if len(app.state.log) > vorher_log else ""

        # (8) das Klickfenster zeigt nur das Oeffentliche
        app._switch_view("Portal")
        laufend = app._marsch_laufend(KANTE)
        ergebnis["fenster"] = _fenstertexte(app, laufend[0]) if laufend else []
        return ergebnis
    finally:
        root.destroy()


def _linienkoordinaten(app):
    """Die Koordinaten der gezeichneten Marschlinien - fuer die Versatzpruefung."""
    leinwand = _leinwand(app)
    if leinwand is None:
        return []
    return [tuple(round(float(v), 1) for v in leinwand.coords(objekt))
            for objekt in leinwand.find_withtag("marsch") if leinwand.type(objekt) == "line"]


def _unterwegs_zeile(app):
    """Die Zeile mit der GROBEN Restzeit ueber der Karte (leer, wenn keine da ist)."""
    import tkinter as tk
    for kind in app.content.winfo_children():
        if isinstance(kind, tk.Label) and str(kind.cget("text")).startswith("Unterwegs:"):
            return str(kind.cget("text"))
    return ""


def _reihenfolge(app):
    """Wo steht die Restzeit-Zeile gegenueber der Karte? (Index im Inhaltsbereich, -1 = fehlt)."""
    import tkinter as tk
    kinder = list(app.content.winfo_children())
    zeile = next((i for i, k in enumerate(kinder)
                  if isinstance(k, tk.Label) and str(k.cget("text")).startswith("Unterwegs:")), -1)
    karte = next((i for i, k in enumerate(kinder)
                  if isinstance(k, tk.Canvas) and k.find_withtag("portalbote")), -1)
    return (zeile, karte)


def _linienfarbe(app):
    """Die Farbe der gezeichneten Marschlinie (oder '-')."""
    leinwand = _leinwand(app)
    if leinwand is None:
        return "-"
    for objekt in leinwand.find_withtag("marsch"):
        if leinwand.type(objekt) == "line":
            return str(leinwand.itemcget(objekt, "fill"))
    return "-"


def _fenstertexte(app, marsch):
    """Das Klickfenster bauen und alle Label-Texte zurueckgeben (Fenster sofort wieder zu)."""
    import tkinter as tk
    treffer = {"seg": ((0, 0), (10, 10)), "marsch": marsch, "tag": "marsch_0"}
    vorher = set(app.root.winfo_children())
    app._marsch_optionen(treffer)
    texte = []
    for kind in app.root.winfo_children():
        if isinstance(kind, tk.Toplevel) and kind not in vorher:
            for innen in kind.winfo_children():
                if isinstance(innen, tk.Label):
                    texte.append(str(innen.cget("text")))
            kind.destroy()
    return texte


ERGEBNIS = ausnahme("Szene aufbauen", _probe) or {}

if ERGEBNIS.get("zu_wenig_doerfer"):
    check("die Karte hat genug fremde Doerfer", False, str(ERGEBNIS))
else:
    abschnitt("5. Zeichnen, Ankommen, Rueckkehr")
    check("ohne Auftrag steht keine Linie auf der Karte", ERGEBNIS.get("ohne") == 0,
          str(ERGEBNIS.get("ohne")))
    check("der Marsch startet", ERGEBNIS.get("ok") is True, str(ERGEBNIS.get("meldung")))
    check("ein Marsch zeichnet vier Objekte", ERGEBNIS.get("einer") == 4, str(ERGEBNIS.get("einer")))
    check("die Felder sind Start- und Zielfeld",
          ERGEBNIS.get("felder") == ERGEBNIS.get("erwartet"),
          str((ERGEBNIS.get("felder"), ERGEBNIS.get("erwartet"))))
    check("die grobe Restzeit steht als Zeile ueber der Karte",
          ERGEBNIS.get("unterwegs", "").startswith("Unterwegs:")
          and ("h" in ERGEBNIS.get("unterwegs", "")), str(ERGEBNIS.get("unterwegs")))
    check("die Zeile steht VOR der Karte (ohne Scrollen sichtbar)",
          0 <= ERGEBNIS.get("reihenfolge", (-1, -1))[0] < ERGEBNIS.get("reihenfolge", (-1, -1))[1] < 999,
          str(ERGEBNIS.get("reihenfolge")))
    check("die Zeile nennt keine Truppenart",
          "Krieger" not in ERGEBNIS.get("unterwegs", ""), str(ERGEBNIS.get("unterwegs")))
    check("die Hinreise hat die Farbe der Hinreise",
          ERGEBNIS.get("hin_farbe") == OPTIK["linie"]["farbe_hin"], str(ERGEBNIS.get("hin_farbe")))
    check("auf der Rueckreise steht die Linie weiter", ERGEBNIS.get("rueckreise") == 4,
          str(ERGEBNIS.get("rueckreise")))
    check("die Rueckreise hat ihre eigene Farbe",
          ERGEBNIS.get("rueck_farbe") == OPTIK["linie"]["farbe_rueck"], str(ERGEBNIS.get("rueck_farbe")))
    check("nach der Rueckkehr ist die Linie weg", ERGEBNIS.get("danach") == 0,
          str(ERGEBNIS.get("danach")))

    abschnitt("6. Zwei Maersche, Uhr rueckwaerts, unbekannter Ort")
    check("zwei Maersche starten", ERGEBNIS.get("zwei_ok") == (True, True),
          str(ERGEBNIS.get("zwei_ok")))
    check("zwei Maersche zeichnen acht Objekte", ERGEBNIS.get("zwei") == 8, str(ERGEBNIS.get("zwei")))
    linien = ERGEBNIS.get("versatz") or []
    check("zwei Maersche auf demselben Weg liegen NICHT deckungsgleich",
          len(linien) == 2 and linien[0] != linien[1], str(linien))
    check("bei rueckwaerts laufender Uhr bleiben die Maersche stehen",
          ERGEBNIS.get("rueckwaerts") == 8, str(ERGEBNIS.get("rueckwaerts")))
    check("die Restzeit wird nie negativ", ERGEBNIS.get("rest_nie_negativ") is True)
    check("ein unbekannter Ort ergibt KEINE Felder", ERGEBNIS.get("fremd_felder") == (None, None),
          str(ERGEBNIS.get("fremd_felder")))
    check("der unbekannte Ort wird genau EINMAL gemeldet", ERGEBNIS.get("meldungen") == 1,
          str(ERGEBNIS.get("meldungen")))
    check("die Meldung nennt den Grund",
          "nicht im Kartenraster" in str(ERGEBNIS.get("meldung_text")),
          str(ERGEBNIS.get("meldung_text")))

    abschnitt("7. Das Klickfenster zeigt nur das Oeffentliche")
    texte = " | ".join(ERGEBNIS.get("fenster") or [])
    check("das Fenster nennt eine Restzeit", "Restzeit" in texte, texte)
    check("das Fenster nennt KEINE Truppenliste",
          "Krieger" not in texte and "Einheiten:" not in texte, texte)
    check("das Fenster nennt KEINE Auftragsart", "angreifen" not in texte.lower(), texte)
    check("das Fenster nennt KEINE Anzahl", "5 " not in texte and "5x" not in texte, texte)

bericht()
