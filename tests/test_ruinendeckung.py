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
2. Eine Ruine deckt NUR ihr eigenes Feld (Daniels Nachschaerfung: "deckt nur ihre eigene
   koordinate ... theoretisch sonst nichts"). Eine Siedlung daneben ist nicht geschuetzt.
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
    abschnitt("2. Eine Ruine deckt NUR ihr eigenes Feld (Daniels Nachschaerfung 05.11.2026)")
    # Woertlich: "Die ruine deckt nur ihre eigene koordinate und stellt somit eine seite da von der
    # man nicht angegriffen werden kann theoretisch sonst nichts." Deshalb: gedeckt ist nur ein
    # Angriff, der von GENAU dem Ruinenfeld kommt. Eine Siedlung daneben ist NICHT geschuetzt.
    nord = [{"name": "Ruine Nord", "position": (10, 6)}]                 # im Norden der Siedlung
    check("2 dieselbe Koordinate wie die Ruine wird gedeckt", bool(R.deckung(S, (10, 6), nord)),
          str(R.deckung(S, (10, 6), nord)))
    check("2 die Deckung nennt die Ruine", (R.deckung(S, (10, 6), nord) or {}).get("ruine") == "Ruine Nord",
          str(R.deckung(S, (10, 6), nord)))
    check("2 ein Angriff aus Norden (ein Feld daneben) wird NICHT gedeckt - die Siedlung nicht geschuetzt",
          R.deckung(S, (10, 1), nord) == {}, str(R.deckung(S, (10, 1), nord)))
    check("2 ein Angriff aus Sueden wird NICHT gedeckt", R.deckung(S, (10, 19), nord) == {},
          str(R.deckung(S, (10, 19), nord)))
    check("2 ein Angriff aus Osten wird NICHT gedeckt", R.deckung(S, (19, 10), nord) == {},
          str(R.deckung(S, (19, 10), nord)))
    # Die Ruine liegt direkt neben der Siedlung - ein Angriff, der NICHT von ihrem Feld kommt,
    # geht trotzdem durch: die Siedlung ist ungeschuetzt.
    check("2 eine Ruine neben der Siedlung schuetzt sie nicht",
          R.deckung(S, (10, 1), [{"name": "nah", "position": (10, 9)}]) == {},
          str(R.deckung(S, (10, 1), [{"name": "nah", "position": (10, 9)}])))
    check("2 die Deckweite steht als EINE Zahl im Modul (0 = eigenes Feld)",
          R.DECKWEITE_FELDER == 0, str(R.DECKWEITE_FELDER))
    check("2 ohne Ruine keine Deckung", R.deckung(S, (10, 6), []) == {}, str(R.deckung(S, (10, 6), [])))
    check("2 unbekannte Angreiferposition deckt nichts", R.deckung(S, None, nord) == {},
          str(R.deckung(S, None, nord)))
    check("2 kaputte Ruineneintraege werden uebergangen",
          R.deckung(S, (10, 6), [None, "x", {"name": "ohne Lage"}]) == {},
          str(R.deckung(S, (10, 6), [None, "x", {"name": "ohne Lage"}])))

    # ------------------------------------------------------------------ 3. Anzeigetexte
    abschnitt("3. Die Anzeige nennt Richtung und Ruine - und schweigt ohne Deckung")
    liste = R.deckungen(S, nord)
    check("3 eine Ruine wird gelistet", len(liste) == 1, str(liste))
    text = R.deckung_text("Burg Silberbach", liste)
    check("3 der Text nennt den Ort", "Burg Silberbach" in text, text)
    check("3 der Text nennt die Lage der Ruine", "im Norden" in text, text)
    check("3 der Text nennt die Ruine", "Ruine Nord" in text, text)
    check("3 der Text sagt ausdruecklich, dass nur das eigene Feld gedeckt ist",
          "deckt nur ihr eigenes Feld" in text, text)
    check("3 ohne Ruine kommt der LEERE Text", R.deckung_text("Burg Silberbach", []) == "",
          R.deckung_text("Burg Silberbach", []))
    zwei_liste = R.deckungen(S, [{"name": "a", "position": (10, 6)},
                                 {"name": "b", "position": (15, 10)}])
    check("3 zwei Ruinen, nach Norden zuerst", [e["richtung"] for e in zwei_liste] == ["N", "O"],
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
    angreifer_auf_ruine = (7, 3)                                        # genau das Ruinenfeld
    angreifer_nord = (7, 1)                                             # ein Feld daneben
    deckung = st.ruine_deckt_angriff(_ort(M, 7, 9, welt), angreifer_auf_ruine)
    check("4 ein Angriff vom Ruinenfeld selbst wird abgewiesen", bool(deckung), str(deckung))
    check("4 ein Angriff daneben bleibt erlaubt",
          st.ruine_deckt_angriff(_ort(M, 7, 9, welt), angreifer_nord) == {},
          str(st.ruine_deckt_angriff(_ort(M, 7, 9, welt), angreifer_nord)))
    check("4 ohne Ort keine Deckung", st.ruine_deckt_angriff(None, angreifer_auf_ruine) == {})

    # ------------------------------------------------------------------ 5. Kampfweg
    abschnitt("5. Der Kampfweg fragt die Deckung, bevor er kaempft")
    stelle_deckung = TEXT_MAIN.find("self.ruine_deckt_angriff(")
    stelle_kampf = TEXT_MAIN.find("kampf.fuehre_schlacht(\n                                bot_kaempfer")
    check("5 die Deckungspruefung steht im Code", stelle_deckung > 0, str(stelle_deckung))
    check("5 sie steht VOR dem Kampf gegen den Spieler-Ort",
          0 < stelle_deckung < stelle_kampf, "%d < %d" % (stelle_deckung, stelle_kampf))
    check("5 die Meldung sagt, dass von dort kein Angriff kommt",
          "kein Angriff" in TEXT_MAIN and "deckt genau dieses Feld" in TEXT_MAIN, "Meldung vorhanden")
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
              not any("deckt nur ihr eigenes Feld" in t for t in (ohne or [])),
              str([t for t in (ohne or []) if "deckt" in t]))
        app.state.drachen_besiegt = [kennung]                            # jetzt eine Ruine im Norden
        check("6 der Spielstand kennt die Ruine", bool(app.state.ruinendeckungen(ort)),
              str(app.state.ruinendeckungen(ort)))
        mit = ausnahme("Uebersicht mit Ruine", lambda: (app._render_overview(), _labels(app.content))[1])
        zeilen = [t for t in (mit or []) if "deckt nur ihr eigenes Feld" in t]
        check("6 die Uebersicht zeigt eine Deckungszeile", len(zeilen) == 1, str(zeilen))
        check("6 die Zeile nennt die Lage Norden", zeilen and "Norden" in zeilen[0], str(zeilen))
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
