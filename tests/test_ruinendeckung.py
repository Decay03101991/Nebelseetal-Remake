# -*- coding: ascii -*-
"""Frage 9: die besiegte Ruine deckt ihre Seite (Register 216, 05.11.2026).

Daniels Entscheidung: "Die besiegte Ruine sperrt ihre Seite - kein Angriff aus dieser Richtung."
Woertlich-nah aus derselben Runde: der Spieler soll "von einer seite nicht angegriffen werden,
wenn er neben sich eine bereits besiegte ruine stellt". Die Ruine ist damit ein TAKTISCHER PUNKT
(Frage 3: keine Regeneration, kein Erwachen) und eine wichtige Beute (Frage 1: Bots raeumen sie).

Was diese Datei beweist
-----------------------
1. Die Geometrie stimmt: acht Himmelsrichtungen, die Grenzen liegen bei 22,5 Grad, derselbe
   Punkt hat keine Richtung (kein erfundener Sektor).
2. Eine Ruine deckt genau den Sektor, in dem sie liegt - gemessen vom verteidigten Ort aus.
   Eine Ruine im Nachbarsektor deckt NICHT, und die naechstgelegene Ruine gewinnt den Namen.
3. Im Spielstand zaehlen NUR besiegte Drachen DERSELBEN Welt; ein stehender Drache deckt nichts.
4. Der Kampfweg fragt die Deckung, BEVOR er kaempft (Quellwache in der richtigen Reihenfolge).
5. Die Anzeige zeigt die Deckung in der Uebersicht - und nur dann, wenn es eine gibt.
6. Gegenprobe: ohne Deckung bleibt der Text leer und der Angriff erlaubt (die Wache ist nicht
   blind gruen).

ASCII-only (Pruefdatei-Konvention): Umlaute nur als Escape.

Aufruf:  python -X utf8 tests/test_ruinendeckung.py
"""
from __future__ import annotations

import os
import sys
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, ausnahme, import_src

ROOT, SRC = import_src()
import drachen  # noqa: E402
import main as M  # noqa: E402
import ruinendeckung as R  # noqa: E402

TEXT_MAIN = open(os.path.join(SRC, "main.py"), encoding="utf-8").read()
S = (10, 10)                                    # der verteidigte Ort in allen Rechenproben


def _labels(widget) -> list:
    """Alle Texte der Labels unter einem Widget - fuer die Anzeigepruefung."""
    texte = []
    for kind in widget.winfo_children():
        try:
            if isinstance(kind, tk.Label):
                texte.append(str(kind.cget("text")))
            texte.extend(_labels(kind))
        except Exception:
            continue
    return texte


def haupt() -> int:
    # ------------------------------------------------------------------ 1. Geometrie
    abschnitt("1. Acht Richtungen, klare Grenzen, kein Sektor ohne Richtung")
    proben = {(10, 5): "N", (15, 5): "NO", (15, 10): "O", (15, 15): "SO",
              (10, 15): "S", (5, 15): "SW", (5, 10): "W", (5, 5): "NW"}
    for ziel, soll in proben.items():
        ist = R.richtung(S, ziel)
        check("1 Richtung nach %s ist %s" % (ziel, soll), ist == soll, ist)
    check("1 derselbe Punkt hat keine Richtung", R.richtung(S, S) == "", R.richtung(S, S))
    check("1 unbrauchbare Angabe gibt keine Richtung", R.richtung(S, None) == "", R.richtung(S, None))
    check("1 die Grenze bei 22,5 Grad kippt nicht falsch", R.richtung(S, (10, 9)) == "N",
          R.richtung(S, (10, 9)))
    check("1 acht Richtungen sind bekannt", len(R.RICHTUNGEN) == 8, str(R.RICHTUNGEN))
    check("1 jede Richtung hat einen ausgeschriebenen Namen",
          all(R.richtung_text(k) for k in R.RICHTUNGEN), str([R.richtung_text(k) for k in R.RICHTUNGEN]))
    check("1 'NO' heisst ausgeschrieben Nordosten", R.richtung_text("NO") == "Nordosten",
          R.richtung_text("NO"))

    # ------------------------------------------------------------------ 2. Deckung
    abschnitt("2. Eine Ruine deckt ihren Sektor - und nur ihren")
    nord = [{"name": "Ruine Nord", "position": (10, 6)}]                 # direkt im Norden
    check("2 Angriff aus Norden wird gedeckt", bool(R.deckung(S, (10, 1), nord)),
          str(R.deckung(S, (10, 1), nord)))
    check("2 die Deckung nennt die Richtung", (R.deckung(S, (10, 1), nord) or {}).get("richtung") == "N",
          str(R.deckung(S, (10, 1), nord)))
    check("2 die Deckung nennt die Ruine", (R.deckung(S, (10, 1), nord) or {}).get("ruine") == "Ruine Nord")
    check("2 Angriff aus Sueden wird NICHT gedeckt", R.deckung(S, (10, 19), nord) == {},
          str(R.deckung(S, (10, 19), nord)))
    check("2 Angriff aus Osten wird NICHT gedeckt (Nachbarsektor)", R.deckung(S, (19, 10), nord) == {},
          str(R.deckung(S, (19, 10), nord)))
    zwei = [{"name": "fern", "position": (4, 4)}, {"name": "nah", "position": (9, 9)}]
    check("2 bei zwei Ruinen im Sektor gewinnt die naechste",
          (R.deckung(S, (5, 5), zwei) or {}).get("ruine") == "nah", str(R.deckung(S, (5, 5), zwei)))
    check("2 ohne Ruine keine Deckung", R.deckung(S, (10, 1), []) == {}, str(R.deckung(S, (10, 1), [])))
    check("2 unbekannte Angreiferposition deckt nichts", R.deckung(S, None, nord) == {},
          str(R.deckung(S, None, nord)))
    check("2 kaputte Ruineneintraege werden uebergangen",
          R.deckung(S, (10, 1), [None, "x", {"name": "ohne Lage"}]) == {},
          str(R.deckung(S, (10, 1), [None, "x", {"name": "ohne Lage"}])))

    # ------------------------------------------------------------------ 3. Anzeigetexte
    abschnitt("3. Die Anzeige nennt Richtung und Ruine - und schweigt ohne Deckung")
    liste = R.deckungen(S, nord)
    check("3 eine Deckung wird gelistet", len(liste) == 1, str(liste))
    text = R.deckung_text("Burg Silberbach", liste)
    check("3 der Text nennt den Ort", "Burg Silberbach" in text, text)
    check("3 der Text nennt die Richtung", "Norden" in text, text)
    check("3 der Text nennt die Ruine", "Ruine Nord" in text, text)
    check("3 ohne Deckung kommt der LEERE Text", R.deckung_text("Burg Silberbach", []) == "",
          R.deckung_text("Burg Silberbach", []))
    zwei_liste = R.deckungen(S, [{"name": "a", "position": (10, 6)},
                                 {"name": "b", "position": (15, 10)}])
    check("3 zwei Richtungen, nach Norden zuerst", [e["richtung"] for e in zwei_liste] == ["N", "O"],
          str([e["richtung"] for e in zwei_liste]))

    # ------------------------------------------------------------------ 4. Im Spielstand
    abschnitt("4. Im Spielstand zaehlen nur BESIEGTE Drachen derselben Welt")
    st = M.GameState()
    drache = drachen.finde_id("drache_d02")
    kennung = str(drache.get("id"))
    welt = int(str(drache.get("welt")).lstrip("d"))
    st.drachen_positionen = {kennung: [7, 3]}                            # die Ruine liegt im Norden
    st.drachen_besiegt = []                                              # steht noch
    check("4 ein stehender Drache deckt nichts", st.ruinen_der_welt(welt) == [],
          str(st.ruinen_der_welt(welt)))
    st.drachen_besiegt = [kennung]                                       # jetzt eine Ruine
    ruinen = st.ruinen_der_welt(welt)
    check("4 die besiegte Ruine steht mit Lage bereit", len(ruinen) == 1 and ruinen[0]["position"] == (7, 3),
          str(ruinen))
    check("4 auf einer anderen Welt gibt es sie nicht", st.ruinen_der_welt((welt % 6) + 1) == [],
          str(st.ruinen_der_welt((welt % 6) + 1)))
    angreifer_nord = (7, 1)                                              # kommt aus dem Norden
    angreifer_sued = (7, 9)                                              # kommt aus dem Sueden
    deckung = st.ruine_deckt_angriff(_ort(M, 7, 9, welt), angreifer_nord)
    check("4 der Angriff aus dem Norden wird abgewiesen", bool(deckung), str(deckung))
    check("4 der Angriff aus dem Sueden bleibt erlaubt",
          st.ruine_deckt_angriff(_ort(M, 7, 9, welt), angreifer_sued) == {},
          str(st.ruine_deckt_angriff(_ort(M, 7, 9, welt), angreifer_sued)))
    check("4 ohne Ort keine Deckung", st.ruine_deckt_angriff(None, angreifer_nord) == {})

    # ------------------------------------------------------------------ 5. Kampfweg
    abschnitt("5. Der Kampfweg fragt die Deckung, bevor er kaempft")
    stelle_deckung = TEXT_MAIN.find("self.ruine_deckt_angriff(")
    stelle_kampf = TEXT_MAIN.find("kampf.fuehre_schlacht(\n                                bot_kaempfer")
    check("5 die Deckungspruefung steht im Code", stelle_deckung > 0, str(stelle_deckung))
    check("5 sie steht VOR dem Kampf gegen den Spieler-Ort",
          0 < stelle_deckung < stelle_kampf, "%d < %d" % (stelle_deckung, stelle_kampf))
    check("5 die Meldung nennt die Richtung",
          "kein Angriff aus dieser Richtung" in TEXT_MAIN, "Meldung vorhanden")
    check("5 die Entscheidung ist im Code benannt", "Frage 9" in TEXT_MAIN)

    # ------------------------------------------------------------------ 6. Anzeige in der Uebersicht
    abschnitt("6. Die Uebersicht zeigt die Deckung - und nur, wenn es eine gibt")
    root = None
    try:
        root = tk.Tk()
        root.withdraw()
        app = M.NebelseetalApp(root)
        app._build_main_ui()
        app._erste_siedlung_gruenden()
        ort = app.state.aktive_siedlung()
        app.state.eigene_dimension = welt
        ort.dimension = welt                                             # der Ort liegt auf der Drachenwelt
        app.state.drachen_besiegt = []                                   # erst KEINE Ruine
        app.state.drachen_positionen = {kennung: [int(ort.x), int(ort.y) - 3]}
        ohne = ausnahme("Uebersicht ohne Ruine", lambda: (app._render_overview(), _labels(app.content))[1])
        check("6 ohne Ruine steht keine Deckungszeile da",
              not any("ist gedeckt" in t for t in (ohne or [])),
              str([t for t in (ohne or []) if "gedeckt" in t]))
        app.state.drachen_besiegt = [kennung]                            # jetzt eine Ruine im Norden
        check("6 der Spielstand kennt die Deckung", bool(app.state.ruinendeckungen(ort)),
              str(app.state.ruinendeckungen(ort)))
        mit = ausnahme("Uebersicht mit Ruine", lambda: (app._render_overview(), _labels(app.content))[1])
        zeilen = [t for t in (mit or []) if "ist gedeckt" in t]
        check("6 die Uebersicht zeigt eine Deckungszeile", len(zeilen) == 1, str(zeilen))
        check("6 die Zeile nennt die Richtung Norden", zeilen and "Norden" in zeilen[0], str(zeilen))
    finally:
        if root is not None:
            try:
                root.destroy()
            except Exception:
                pass

    befund("Die Deckung gilt fuer den GANZEN Sektor bis zum Kartenrand - eine REICHWEITE nennt "
           "das Original nicht. Das ist eine gesetzte Regel (VORSCHLAG), keine belegte Zahl; eine "
           "Reichweite waere Daniels Entscheidung.")

    return bericht()


def _ort(modul, x: int, y: int, welt: int):
    """Eine Siedlung mit Lage - nur die Felder, die die Deckungsrechnung liest."""
    ort = modul.Settlement(name="Probeort", map_id="probe")
    ort.x, ort.y, ort.dimension = int(x), int(y), int(welt)
    return ort


if __name__ == "__main__":
    sys.exit(haupt())
