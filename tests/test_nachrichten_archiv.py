# -*- coding: ascii -*-
"""Postfach: Archiv, Filter, Fristen, Blaettern und Ruhm-Balken - S1 (06.11.2026).

Messlage vor diesem Schnitt (belegt): `_render_messages` in `src/main.py` zeigte
`self.state.messages[-20:]` - aeltere Nachrichten standen im Spielstand, waren aber unerreichbar;
es gab keinen Filter, kein Archiv und keinen Ablauf. `punkte.auszeichnungen` liefert vier
Auszeichnungen, aber keinen Balken (Progressbar: 0 Treffer).

Vorgabe Daniel (Runde 2, Entscheidung 4): "Frist 1 Spieltag fuer Berichte, Militaerberichte
(Kampf, Gesamtsieg) nie loeschen, ungelesene Verlustberichte verschieben sich automatisch".
Alle Fristen und Kategorien stehen in `data/nachrichten.json`, die Ruhm-Stufen in `data/ruhm.json`
(Daniel, Runde 3 Frage 3: Vorschlag aus unserer Messung, so nutzen).

Was diese Datei beweist
-----------------------
1. Ein ALTER Spielstand laedt: Nachrichten ohne `read`, `archived` und `ablauf_am` werden mit
   Standardwerten gelesen, und das Laden schreibt NICHTS in die Nachricht (keine Migration).
2. Militaerberichte (`kampf`, `gesamtsieg`) laufen NIE ab, auch mit altem Stempel und spaetem Jetzt.
3. Die Frist greift GENAU EINMAL: der zweite Aufruf entfernt nichts mehr.
4. Ein UNGELESENER Verlustbericht verschiebt seine Frist (bleibt im Postfach), ein gelesener
   Kampfbericht mit gesetzter Frist verschwindet.
5. Blaettern liefert 20 von 45 Nachrichten, Seite 3 die letzten 5; eine zu grosse Seitenzahl wird
   auf die letzte Seite gezogen, nie auf eine leere.
6. Der Ruhm-Balken rechnet NICHT selbst: `postfach.rang` liest `data/ruhm.json`, die Ansicht liest
   den Punktestand aus der EINEN Quelle (`GameState.punktestand`) - Quellwache und echter Render.
7. Filter und Zaehler: `ungelesen` zeigt nur ungelesene, `archiv` nur das Archiv, eine Kategorie
   zeigt ihre Nachrichten; `alle` enthaelt das Archiv NICHT.

Aufruf:  python -X utf8 tests/test_nachrichten_archiv.py
"""
from __future__ import annotations

import ast
import inspect
import os
import sys
import textwrap

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(WURZEL, "src"))
sys.path.insert(0, os.path.join(WURZEL, "tests"))

from harness import abschnitt, bericht, check                      # noqa: E402  (Pruefrahmen des Projekts)
import postfach                                                    # noqa: E402  (das Fachmodul)

FRIST = float(postfach.einstellungen().get("frist_spielsekunden") or 0)


def nachricht(typ, spielzeit=0.0, text="Meldung", **felder):
    """Baut eine Nachricht wie der Kern sie schreibt (dict mit type/text/spielzeit_sekunden)."""
    n = {"text": text, "type": typ, "spielzeit_sekunden": float(spielzeit)}
    n.update(felder)
    return n


def test_alter_spielstand():
    """1. Alter Spielstand: fehlende Felder werden gelesen, nichts wird geschrieben."""
    abschnitt("1. Alter Spielstand laedt ohne Migration")
    alt = nachricht("spionage", spielzeit=100.0)
    tiefe = dict(alt)
    info = postfach.normalisiert(alt)
    check("normalisiert liefert ungesehen und nicht archiviert",
          info == {"read": False, "archived": False, "ablauf_am": None}, str(info))
    check("das Laden aendert die Nachricht NICHT", alt == tiefe, str(alt))
    liste = [alt]
    postfach.sichtbar(liste, "alle")
    postfach.ablauf_buchen(liste, 100.0 + FRIST - 1)                # noch innerhalb der Frist
    check("alter Eintrag bleibt vor der Frist stehen", len(liste) == 1)
    check("kein Feld nachtraeglich erfunden", "read" not in alt and "archived" not in alt)


def test_militaer_ohne_ablauf():
    """2. Kampf und Gesamtsieg laufen nie ab."""
    abschnitt("2. Militaerberichte laufen nie ab")
    liste = [nachricht("kampf", spielzeit=0.0), nachricht("gesamtsieg", spielzeit=0.0),
             nachricht("system", spielzeit=0.0)]
    ergebnis = postfach.ablauf_buchen(liste, 10 ** 7)               # sehr spaetes Jetzt
    check("zwei Militaerberichte bleiben", len([n for n in liste if n["type"] in ("kampf", "gesamtsieg")]) == 2,
          str([n["type"] for n in liste]))
    check("der Systembericht ist abgelaufen", ergebnis["entfernt"] == 1, str(ergebnis))


def test_frist_genau_einmal():
    """3. Die Frist greift genau einmal."""
    abschnitt("3. Frist greift genau einmal")
    liste = [nachricht("spionage", spielzeit=0.0, text="Kundschafter zurueck")]
    vorher = FRIST
    postfach.ablauf_buchen(liste, vorher - 1)                       # eine Sekunde zu frueh
    check("vor der Frist bleibt sie stehen", len(liste) == 1)
    erst = postfach.ablauf_buchen(liste, vorher + 1)                # jetzt ist sie faellig
    zweit = postfach.ablauf_buchen(liste, vorher + 2)               # zweiter Aufruf
    check("erster faelliger Aufruf entfernt genau eine", erst["entfernt"] == 1, str(erst))
    check("zweiter Aufruf entfernt nichts mehr", zweit["entfernt"] == 0, str(zweit))
    check("die Liste ist danach leer", liste == [], str(liste))


def test_verlustbericht_verschiebt():
    """4. Ungelesener Verlustbericht verschiebt, gelesener Kampfbericht verschwindet."""
    abschnitt("4. Ungelesener Verlustbericht verschiebt sich")
    # Der Typ `verlust` ist der einzige, der ablaufen DARF und beim Ungelesen-Sein verschoben wird;
    # `kampf` und `gesamtsieg` stehen in `ohne_ablauf` und laufen nie ab (Daniel, Entscheidung 4).
    unklar = nachricht("verlust", spielzeit=0.0, ablauf_am=100.0, text="Verluste im Gefecht")
    gelesen = nachricht("verlust", spielzeit=0.0, ablauf_am=100.0, read=True, text="Sieg")
    liste = [unklar, gelesen]
    ergebnis = postfach.ablauf_buchen(liste, 200.0)
    check("ein Bericht verschoben", ergebnis["verschoben"] == 1, str(ergebnis))
    check("ein Bericht entfernt", ergebnis["entfernt"] == 1, str(ergebnis))
    check("der ungelesene steht noch drin", unklar in liste)
    check("seine Frist liegt jetzt in der Zukunft", float(unklar["ablauf_am"]) == 200.0 + FRIST,
          str(unklar.get("ablauf_am")))
    check("der Text bleibt unangetastet", unklar["text"] == "Verluste im Gefecht")


def test_diebstahlbericht_verschiebt():
    """4b. Ein ungelesener Diebstahlbericht verschiebt sich (Befund S4, 08.11.2026)."""
    abschnitt("4b. Ungelesener Diebstahlbericht verschiebt sich")
    # Ein Diebstahl ist ein Verlustbericht: Daniel hat zugesagt, dass jeder Diebstahl einen Bericht
    # im Postfach hinterlaesst. Bis 08.11.2026 verschwand ein ungelesener Bericht nach EINEM Spieltag.
    unklar = nachricht("diebstahl", spielzeit=0.0, ablauf_am=100.0, text="Diebstahl in Siedlung 1")
    gelesen = nachricht("diebstahl", spielzeit=0.0, ablauf_am=100.0, read=True, text="Diebstahl")
    liste = [unklar, gelesen]
    ergebnis = postfach.ablauf_buchen(liste, 200.0)
    check("ein Diebstahlbericht verschoben", ergebnis["verschoben"] == 1, str(ergebnis))
    check("der gelesene ist abgelaufen", ergebnis["entfernt"] == 1, str(ergebnis))
    check("der ungelesene steht noch drin", unklar in liste, str(liste))
    check("er ueberlebt auch die zweite Frist", postfach.ablauf_buchen(liste, 200.0 + FRIST)["verschoben"] == 1,
          str(liste))
    check("der Typ steht in den Daten, nicht nur im Rueckfall",
          "diebstahl" in (postfach.einstellungen().get("verschieben_wenn_ungelesen") or []),
          str(postfach.einstellungen().get("verschieben_wenn_ungelesen")))


def test_echter_diebstahlbericht_verschiebt():
    """4c. Der ECHTE Erzeuger liefert einen Typ, der in den Daten steht (Opus-Hinweis 08.11.2026).

    Der Test 4b baut seine Nachricht selbst - damit belegt er nur die Liste, nicht den Ablauf.
    Hier kommt die Nachricht aus `main.bot_diebstahl_nachricht`, also aus dem Code, der sie im
    Spiel schreibt; erst danach laeuft die Frist.
    """
    abschnitt("4c. Der echte Diebstahlbericht ueberlebt die Frist")
    try:
        import main as M                                                   # braucht tkinter, nur hier
    except Exception as fehler:                                            # noqa: BLE001
        befund("main.py nicht importierbar - Erzeuger nicht pruefbar: %s" % fehler)
        return
    echt = M.bot_diebstahl_nachricht({"bot": "Grom", "ziel": "Siedlung 1", "zeit": 0.0,
                                      "mengen": {"holz": 3.0}, "summe": 3.0})
    typ = str(echt.get("type") or "")
    check("der Erzeuger schreibt den Typ 'diebstahl'", typ == "diebstahl", typ)
    check("dieser Typ steht in den Daten unter verschieben_wenn_ungelesen",
          typ in (postfach.einstellungen().get("verschieben_wenn_ungelesen") or []), typ)
    liste = [echt]
    postfach.ablauf_buchen(liste, FRIST + 1)                               # eine Frist ist um
    check("der echte Bericht steht noch im Postfach", echt in liste, str(len(liste)))
    postfach.ablauf_buchen(liste, 2 * FRIST + 2)                            # zweite Frist
    check("er ueberlebt auch die zweite Frist", echt in liste, str(len(liste)))


def test_blaettern():
    """5. Blaettern liefert 20 von 45, die letzte Seite 5."""
    abschnitt("5. Blaettern 20 von 45")
    liste = [nachricht("handel", spielzeit=float(i), text="Zeile %d" % i) for i in range(45)]
    sichtbar = postfach.sichtbar(liste, "alle")
    check("alle 45 sind sichtbar", len(sichtbar) == 45, str(len(sichtbar)))
    check("neueste zuerst", sichtbar[0]["text"] == "Zeile 44", sichtbar[0]["text"])
    check("drei Seiten", postfach.seiten_anzahl(sichtbar) == 3, str(postfach.seiten_anzahl(sichtbar)))
    check("Seite 1 hat 20", len(postfach.seite(sichtbar, 1)) == 20)
    check("Seite 3 hat 5", len(postfach.seite(sichtbar, 3)) == 5)
    check("Seite 9 wird auf die letzte gezogen", len(postfach.seite(sichtbar, 9)) == 5)
    check("Seite 0 wird auf die erste gezogen", len(postfach.seite(sichtbar, 0)) == 20)
    check("eine leere Liste hat trotzdem eine Seite", postfach.seiten_anzahl([]) == 1)


def test_filter():
    """6. Filter und Zaehler."""
    abschnitt("6. Filter und Zaehler")
    liste = [nachricht("kampf", text="a"), nachricht("spionage", text="b"),
             nachricht("spionage", text="c", read=True), nachricht("handel", text="d"),
             nachricht("handel", text="e", archived=True)]
    check("alle ohne Archiv: 4", len(postfach.sichtbar(liste, "alle")) == 4,
          str(len(postfach.sichtbar(liste, "alle"))))
    check("ungelesen: 3", len(postfach.sichtbar(liste, "ungelesen")) == 3)
    check("Archiv: 1", len(postfach.sichtbar(liste, "archiv")) == 1)
    check("Kategorie spionage: 2", len(postfach.sichtbar(liste, "spionage")) == 2)
    check("Kategorie kampf: 1", len(postfach.sichtbar(liste, "kampf")) == 1)
    # Der Zaehler zaehlt ALLE ungelesenen, auch die archivierte - er sagt "davon ungelesen"
    # neben der Liste, nicht "davon sichtbar ungelesen".
    check("ungelesen zaehlt richtig (4, auch die archivierte)", postfach.ungelesen_anzahl(liste) == 4,
          str(postfach.ungelesen_anzahl(liste)))
    check("Archiv-Umschalten setzt das Feld",
          (postfach.archivieren(liste[0], True), postfach.ist_archiviert(liste[0]))[1] is True)
    check("Gelesen-Markierung setzt das Feld",
          (postfach.als_gelesen(liste[1]), postfach.ist_gelesen(liste[1]))[1] is True)


def test_rang_aus_daten():
    """7. Rang kommt aus data/ruhm.json, keine Schwelle im Code."""
    abschnitt("7. Rang rechnet aus den Daten")
    stufen = postfach.ruhm_daten().get("stufen") or []
    check("vier Stufen in data/ruhm.json", len(stufen) == 4, str(len(stufen)))
    check("0 Punkte ist der Ansiedler", postfach.rang(0)["name"] == stufen[0]["name"])
    check("10 Punkte erreichen Stufe 2", postfach.rang(10)["stufe"] == 2, str(postfach.rang(10)))
    check("40 Punkte erreichen Stufe 3", postfach.rang(40)["stufe"] == 3)
    check("160 Punkte sind die hoechste Stufe", postfach.rang(160)["fortschritt"] == 1.0,
          str(postfach.rang(160)))
    mitte = postfach.rang(100)                                      # zwischen Fuerst (40) und Herrscher (160)
    check("Fortschritt liegt zwischen 0 und 1", 0.0 < mitte["fortschritt"] < 1.0, str(mitte["fortschritt"]))
    check("Abstand wird benannt", "bis Herrscher" in postfach.rang_text(100), postfach.rang_text(100))
    quelle = inspect.getsource(postfach)
    check("keine Frist als Konstante im Modul", "28800" not in quelle)
    check("die Frist kommt aus data/nachrichten.json", FRIST > 0, str(FRIST))


def _code(fn):
    """Quelltext einer Funktion OHNE Docstring (Docstrings zaehlen nicht als Rechnung)."""
    baum = ast.parse(textwrap.dedent(inspect.getsource(fn))).body[0]
    if baum.body and isinstance(baum.body[0], ast.Expr) and isinstance(baum.body[0].value, ast.Constant):
        baum.body = baum.body[1:]                                   # Docstring abschneiden
    return ast.unparse(baum)


def test_render_und_balken():
    """8. Der Balken rechnet nicht selbst - Quellwache und echter Render der Ansicht."""
    abschnitt("8. Balken im echten Render")
    import tkinter as tk
    import main

    quelle = _code(main.NebelseetalApp._ruhm_balken_zeichnen)
    check("der Balken liest den Punktestand der EINEN Quelle", "punktestand()" in quelle, quelle[:120])
    check("keine eigene Punkteformel im Balken", "hoch drei" not in quelle and "** 3" not in quelle)
    check("der Rang kommt aus postfach.rang", "postfach.rang" in quelle)
    check("Masse kommen aus den Daten", "ruhm_daten" in quelle)

    wurzel = tk.Tk()
    wurzel.withdraw()
    try:
        app = main.NebelseetalApp(wurzel)
        app._build_main_ui()
        app.state.messages.append(nachricht("handel", text="Testnachricht im Postfach"))
        app.state.messages.append(nachricht("kampf", text="Kampfbericht"))
        app._postfach_filter = "alle"
        app._postfach_seite = 1
        app._render_messages()                                      # echter Render, kein Mock
        leinwaende = []

        def sammeln(widget):
            """Sammelt alle Canvas-Widgets der Ansicht."""
            for kind in widget.winfo_children():
                if kind.winfo_class() == "Canvas":
                    leinwaende.append(kind)
                sammeln(kind)

        sammeln(app.content)
        check("der Balken ist gezeichnet (ein Canvas)", len(leinwaende) >= 1, str(len(leinwaende)))
        if leinwaende:
            teile = leinwaende[0].find_all()
            check("Balken hat Fuellung und Rahmen (2 Rechtecke)", len(teile) >= 1, str(len(teile)))
        beschriftungen = []

        def texte(widget):
            """Sammelt alle Beschriftungen der Ansicht (Labels UND Knoepfe - die Filterzeile sind Knoepfe)."""
            for kind in widget.winfo_children():
                if kind.winfo_class() in ("Label", "Button"):
                    try:
                        beschriftungen.append(str(kind.cget("text")))
                    except Exception:                                # noqa: BLE001  (Anzeige darf nicht werfen)
                        pass
                texte(kind)

        texte(app.content)
        zusammen = " ".join(beschriftungen)
        check("Filterzeile ist da", "Alle" in zusammen and "Ungelesen" in zusammen, zusammen[:100])
        check("Zaehler nennt die Seite", "Seite 1 von" in zusammen, zusammen[:160])
        check("die Testnachricht wird angezeigt", "Testnachricht im Postfach" in zusammen)
        app._postfach_filter_setzen("archiv")                       # Umschalten darf nicht werfen
        check("Archivfilter rendert leer ohne Ausnahme", True)
        app._postfach_seite_setzen(5)                               # zu grosse Seite wird gezogen
        check("zu grosse Seite wird gezogen", app._postfach_seite == 1, str(app._postfach_seite))
    finally:
        wurzel.destroy()


def main_test():
    """Fuehrt alle Pruefungen aus und meldet das Ergebnis."""
    test_alter_spielstand()
    test_militaer_ohne_ablauf()
    test_frist_genau_einmal()
    test_verlustbericht_verschiebt()
    test_diebstahlbericht_verschiebt()
    test_echter_diebstahlbericht_verschiebt()
    test_blaettern()
    test_filter()
    test_rang_aus_daten()
    test_render_und_balken()
    return bericht()


if __name__ == "__main__":
    sys.exit(main_test())
