"""
Pruefung: Ist src/punkte.py WIRKLICH in die Punktanzeige von src/main.py einghaengt?

Nicht das Modul allein wird geprueft (das tut tests/test_punkte.py), sondern die
EINHAENGUNG: zeigen die Seitenleiste (NebelseetalApp._render) und die Ruhmeshalle
(NebelseetalApp._render_hall_of_fame) tatsaechlich genau die Zahlen, die
punkte.forschungspunkte / punkte.kriegspunkte / punkte.gesamtpunkte liefern?

Bewiesen wird am echten, unsichtbaren Fenster (root.withdraw(), kein mainloop):
  * eigene Methode pruefe_einhaengung(): main.punkte IST src/punkte.py, und der
    Quelltext von _render/_render_hall_of_fame ruft die drei Formeln und wall_stufe
  * bei lauter Nullen zeigen die drei Etiketten exakt 0/0/0
  * zwei Forschungsstufen 3 -> 'Forschung: 54' == punkte.forschungspunkte(...)
  * die alten Felder (score = 999, ruf = 777) tauchen NICHT mehr auf
  * Einheit Krieger = 2 -> 'Krieg:' == punkte.kriegspunkte(...), 'Gesamt:' == punkte.gesamtpunkte(...)
  * ein gebauter Wall (Stufe 4) wirkt echt durch: 'Krieg: 72', 'Gesamt: 63'
  * die Ruhmeshalle zeigt dieselben drei Zahlen plus 'Wallstufe: 4'
  * die alte, falsche Gesamtsumme (score + ruf + Summe der Einheitenzahlen) taucht nirgends auf
  * nach erneuter Aenderung bleiben die Etiketten EXAKT synchron zu punkte.*

Nichts wird nachgebaut oder ersetzt: es laeuft der echte Code aus main.py und punkte.py.

Aufruf:  python -X utf8 tests/test_punkte_einhaengung.py
"""
from __future__ import annotations

import inspect
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, bericht, check, import_src

ROOT, SRC = import_src()
os.chdir(SRC)

import punkte as P


# ==========================================================================
# Aufbau: das echte, unsichtbare Fenster
# ==========================================================================

main = ausnahme("main importieren", lambda: __import__("main"))
tk = ausnahme("tkinter laden", lambda: __import__("tkinter"))

if main is None or tk is None:
    sys.exit(bericht())


def beschriftung(widget) -> str:
    """Den Text eines Tk-Widgets lesen; leere Zeichenkette, wenn es keinen hat."""
    try:
        return str(widget.cget("text"))
    except Exception:
        return ""


def alle_texte(widget) -> list:
    """Alle beschrifteten Widgets unterhalb von ``widget`` (rekursiv) einsammeln."""
    gesammelt = []
    for kind in widget.winfo_children():
        text = beschriftung(kind)
        if text:
            gesammelt.append(text)
        gesammelt.extend(alle_texte(kind))
    return gesammelt


def app_werte(app):
    """Genau die Groessen, aus denen main.py die Punkte rechnet: Staende, Einheiten, Wall."""
    staende = {k: v.level for k, v in app.state.research.items()}
    einheiten = {k: v.count for k, v in app.state.units.items()}
    wall_stufe = main.gebaeude_wirkung.wall_stufe(app.state.settlements)
    return staende, einheiten, wall_stufe


def setze_still(app):
    """Ein stilles Fenster bauen; der Aufrufer schliesst es in einem finally."""
    root = tk.Tk()
    root.withdraw()            # kein sichtbares Fenster
    app_objekt = main.NebelseetalApp(root)
    app_objekt._build_main_ui()
    root.update_idletasks()
    return root, app_objekt


# ==========================================================================
# 1. Einhaengung — die eigene Nachweismethode
# ==========================================================================

abschnitt("1. Einhaengung: main.py benutzt wirklich src/punkte.py")


def nur_code(quelle: str) -> str:
    """Nur die ausfuehrbaren Zeilen: Kommentarzeilen fliegen raus.

    Die Kommentare in main.py nennen absichtlich die alten Felder (``score``, ``ruf``),
    um zu erklaeren, was ersetzt wurde — sie sind Code, aber keine Rechnung.
    """
    return "\n".join(z for z in quelle.splitlines() if not z.strip().startswith("#"))


def pruefe_einhaengung():
    """Eigene Methode: main laedt punkte, und beide Anzeigen rufen die Originalformeln."""
    check("main.py hat das Modul punkte importiert", getattr(main, "punkte", None) is not None)
    check("main.punkte ist DASSELBE Modul wie src/punkte.py (kein Nachbau)",
          getattr(main, "punkte", None) is P)

    quelle_render = inspect.getsource(main.NebelseetalApp._render)
    check("_render (Seitenleiste) ruft punkte.forschungspunkte",
          "punkte.forschungspunkte" in quelle_render)
    check("_render (Seitenleiste) ruft punkte.kriegspunkte",
          "punkte.kriegspunkte" in quelle_render)
    check("_render (Seitenleiste) ruft punkte.gesamtpunkte",
          "punkte.gesamtpunkte" in quelle_render)
    check("_render holt die Wallstufe aus gebaeude_wirkung.wall_stufe",
          "gebaeude_wirkung.wall_stufe" in quelle_render)
    check("_render kennt die alten Felder score/ruf NICHT mehr (nur Codezeilen)",
          "score" not in nur_code(quelle_render) and "ruf" not in nur_code(quelle_render),
          "kein 'score', kein 'ruf' in den Rechenzeilen")

    quelle_hof = inspect.getsource(main.NebelseetalApp._render_hall_of_fame)
    check("_render_hall_of_fame ruft alle drei Originalformeln",
          all(f"punkte.{f}" in quelle_hof
              for f in ("forschungspunkte", "kriegspunkte", "gesamtpunkte")))
    check("_render_hall_of_fame nennt eine 'Wallstufe'-Zeile",
          "Wallstufe" in quelle_hof)
    check("_render_hall_of_fame holt die Wallstufe aus gebaeude_wirkung.wall_stufe",
          "gebaeude_wirkung.wall_stufe" in quelle_hof)


ausnahme("Einhaengung pruefen", pruefe_einhaengung)


# ==========================================================================
# 2. Alles auf Null — die drei Etiketten lesen exakt 0
# ==========================================================================

abschnitt("2. Alles auf Null — Forschung/Krieg/Gesamt lesen exakt 0")

root = None
app = None
try:
    root, app = setze_still(app)

    # Alte, falsche Felder absichtlich auf auffaellige Werte setzen — sie duerfen NICHT wirken.
    app.state.score = 999
    app.state.ruf = 777
    for f in app.state.research.values():
        f.level = 0
    for u in app.state.units.values():
        u.count = 0
    app.state.settlements = []

    app._render()
    root.update_idletasks()

    staende, einheiten, wall = app_werte(app)
    check("punktemodul: leere Staende geben Forschung 0", P.forschungspunkte(staende) == 0)
    check("punktemodul: leere Einheiten und Wall 0 geben Krieg 0",
          P.kriegspunkte(einheiten, wall) == 0)
    check("Seitenleiste: lbl_forschung zeigt 'Forschung: 0'",
          beschriftung(app.lbl_forschung) == "Forschung: 0",
          repr(beschriftung(app.lbl_forschung)))
    check("Seitenleiste: lbl_krieg zeigt 'Krieg: 0'",
          beschriftung(app.lbl_krieg) == "Krieg: 0", repr(beschriftung(app.lbl_krieg)))
    check("Seitenleiste: lbl_gesamt zeigt 'Gesamt: 0'",
          beschriftung(app.lbl_gesamt) == "Gesamt: 0", repr(beschriftung(app.lbl_gesamt)))

    # ======================================================================
    # 3. Zwei Forschungsstufen 3 -> Forschung 54, alte 999 verschwindet
    # ======================================================================

    abschnitt("3. Zwei Forschungsstufen 3 -> 'Forschung: 54', score/ruf unwirksam")

    app.state.research["Felderwirtschaft"].level = 3
    app.state.research["Minenarbeit"].level = 3
    app._render()
    root.update_idletasks()

    staende, einheiten, wall = app_werte(app)
    fp = P.forschungspunkte(staende)
    check("punktemodul: zwei Stufen 3 ergeben 54 (27 + 27)", fp == 54, f"fp = {fp}")
    check("Seitenleiste: lbl_forschung zeigt 'Forschung: 54'",
          beschriftung(app.lbl_forschung) == "Forschung: 54",
          repr(beschriftung(app.lbl_forschung)))
    check("Seitenleiste: lbl_forschung == punkte.forschungspunkte (synchron)",
          beschriftung(app.lbl_forschung) == f"Forschung: {P.forschungspunkte(staende)}")
    check("die alte Feldzahl 999 taucht im Forschungsetikett NICHT auf",
          "999" not in beschriftung(app.lbl_forschung),
          repr(beschriftung(app.lbl_forschung)))

    # ======================================================================
    # 4. Eine Einheit mit Anzahl -> Krieg und Gesamt aus punkte.*
    # ======================================================================

    abschnitt("4. Krieger = 2 -> 'Krieg:' und 'Gesamt:' aus den Originalformeln")

    app.state.units["Krieger"].count = 2
    app._render()
    root.update_idletasks()

    staende, einheiten, wall = app_werte(app)
    kp = P.kriegspunkte(einheiten, wall)
    gp = P.gesamtpunkte(staende, einheiten, wall)
    check("punktemodul: Krieger=2 ohne Wall ergeben 8 Kriegspunkte (4 je Stueck)",
          kp == 8, f"kp = {kp}, wall = {wall}")
    check("Seitenleiste: lbl_krieg zeigt 'Krieg: 8'",
          beschriftung(app.lbl_krieg) == "Krieg: 8", repr(beschriftung(app.lbl_krieg)))
    check("Seitenleiste: lbl_krieg == punkte.kriegspunkte (mit echter Wallstufe)",
          beschriftung(app.lbl_krieg) == f"Krieg: {P.kriegspunkte(einheiten, wall)}")
    check("Seitenleiste: lbl_gesamt zeigt 'Gesamt: 31' ((54 + 8) // 2)",
          beschriftung(app.lbl_gesamt) == "Gesamt: 31", repr(beschriftung(app.lbl_gesamt)))
    check("Seitenleiste: lbl_gesamt == punkte.gesamtpunkte",
          beschriftung(app.lbl_gesamt) == f"Gesamt: {P.gesamtpunkte(staende, einheiten, wall)}")

    # Die alte, falsche Summe: score + ruf + Summe aller Einheitenzahlen.
    alte_summe = app.state.score + app.state.ruf + sum(u.count for u in app.state.units.values())
    check("die alte Formel (score + ruf + Einheiten) ergibt hier 1778",
          alte_summe == 1778, f"alte_summe = {alte_summe}")
    check("die alte Zahl 1778 steht NICHT im Gesamtetiketten",
          str(alte_summe) not in beschriftung(app.lbl_gesamt),
          repr(beschriftung(app.lbl_gesamt)))
    check("auch score 999 und ruf 777 stehen NICHT im Gesamtetiketten",
          "999" not in beschriftung(app.lbl_gesamt) and "777" not in beschriftung(app.lbl_gesamt),
          repr(beschriftung(app.lbl_gesamt)))

    # ======================================================================
    # 5. Ein gebauter Wall wirkt echt durch (Stufe 4)
    # ======================================================================

    abschnitt("5. Gebauter Verteidigungswall Stufe 4 wirkt echt durch")

    siedlung = main.Settlement(name="Wallprobe", map_id="kontinent")
    siedlung.bauten = {"0": "verteidigungswall"}
    siedlung.stufen = {"0": 4}
    app.state.settlements = [siedlung]
    app._render()
    root.update_idletasks()

    staende, einheiten, wall = app_werte(app)
    check("gebaeude_wirkung.wall_stufe liest die gebaute Stufe 4", wall == 4, f"wall = {wall}")
    check("Seitenleiste: lbl_krieg zeigt 'Krieg: 72' (8 + 4*4*4)",
          beschriftung(app.lbl_krieg) == "Krieg: 72", repr(beschriftung(app.lbl_krieg)))
    check("Seitenleiste: lbl_gesamt zeigt 'Gesamt: 63' ((54 + 72) // 2)",
          beschriftung(app.lbl_gesamt) == "Gesamt: 63", repr(beschriftung(app.lbl_gesamt)))
    check("Seitenleiste: lbl_krieg == punkte.kriegspunkte mit Wall",
          beschriftung(app.lbl_krieg) == f"Krieg: {P.kriegspunkte(einheiten, wall)}")
    check("Seitenleiste: lbl_gesamt == punkte.gesamtpunkte mit Wall",
          beschriftung(app.lbl_gesamt) == f"Gesamt: {P.gesamtpunkte(staende, einheiten, wall)}")

    # ======================================================================
    # 6. Ruhmeshalle zeigt dieselben Zahlen plus die Wallstufe
    # ======================================================================

    abschnitt("6. Ruhmeshalle zeigt dieselben Zahlen plus 'Wallstufe: 4'")

    app._switch_view("Ruhmeshalle")
    root.update_idletasks()
    texte = alle_texte(app.content)

    check("Ruhmeshalle enthaelt die Zeile 'Forschung: 54'", "Forschung: 54" in texte, str(texte))
    check("Ruhmeshalle enthaelt die Zeile 'Krieg: 72'", "Krieg: 72" in texte, str(texte))
    check("Ruhmeshalle enthaelt die Zeile 'Gesamt: 63'", "Gesamt: 63" in texte, str(texte))
    check("Ruhmeshalle enthaelt die Zeile 'Wallstufe: 4'", "Wallstufe: 4" in texte, str(texte))
    check("Ruhmeshalle zeigt dieselbe Gesamtzahl wie die Seitenleiste",
          f"Gesamt: {P.gesamtpunkte(staende, einheiten, wall)}" in texte
          and beschriftung(app.lbl_gesamt) in texte,
          f"Seitenleiste {beschriftung(app.lbl_gesamt)!r}")
    check("die alte Zahl 1778 taucht in der Ruhmeshalle NICHT auf",
          str(alte_summe) not in texte, str(texte))

    # ======================================================================
    # 7. Erneut aendern — die Etiketten bleiben exakt synchron zu punkte.*
    # ======================================================================

    abschnitt("7. Aenderung erneut — Etiketten bleiben exakt synchron zu punkte.*")

    app.state.research["Felderwirtschaft"].level = 4
    app.state.research["Minenarbeit"].level = 1
    app.state.research["Tierhaltung"].level = 2
    app.state.units["Krieger"].count = 5
    app.state.units["Paladin"].count = 3
    siedlung.stufen = {"0": 2}          # Wall jetzt Stufe 2
    app._render()
    root.update_idletasks()

    staende, einheiten, wall = app_werte(app)
    check("punktemodul: neue Staende ergeben 64 + 1 + 8 = 73 Forschung",
          P.forschungspunkte(staende) == 73, f"fp = {P.forschungspunkte(staende)}")
    check("Seitenleiste: lbl_forschung == punkte.forschungspunkte (nach Aenderung)",
          beschriftung(app.lbl_forschung) == f"Forschung: {P.forschungspunkte(staende)}",
          repr(beschriftung(app.lbl_forschung)))
    check("Seitenleiste: lbl_krieg == punkte.kriegspunkte (nach Aenderung)",
          beschriftung(app.lbl_krieg) == f"Krieg: {P.kriegspunkte(einheiten, wall)}",
          repr(beschriftung(app.lbl_krieg)))
    check("Seitenleiste: lbl_gesamt == punkte.gesamtpunkte (nach Aenderung)",
          beschriftung(app.lbl_gesamt) == f"Gesamt: {P.gesamtpunkte(staende, einheiten, wall)}",
          repr(beschriftung(app.lbl_gesamt)))

    app._switch_view("Ruhmeshalle")
    root.update_idletasks()
    texte = alle_texte(app.content)
    check("Ruhmeshalle zeigt die neuen Zahlen ebenfalls synchron",
          f"Forschung: {P.forschungspunkte(staende)}" in texte
          and f"Krieg: {P.kriegspunkte(einheiten, wall)}" in texte
          and f"Gesamt: {P.gesamtpunkte(staende, einheiten, wall)}" in texte
          and f"Wallstufe: {wall}" in texte,
          str(texte))
    check("Ruhmeshalle hat die alte Zahl 1778 auch jetzt nicht",
          str(alte_summe) not in texte, str(texte))

finally:
    if root is not None:
        try:
            root.destroy()
        except Exception:
            pass

# ==========================================================================
# 5. Sieg und Niederlage (Schritt 31, Vorgabe Daniel 05.10.2026: Option A)
# ==========================================================================

abschnitt("Sieg und Niederlage — Zielzahl 300, Niederlage ohne Siedlung und Einheit")

check("die Zielzahl steht im Punktemodul (300)", P.VORSCHLAG_ZIEL_PUNKTE == 300,
      str(P.VORSCHLAG_ZIEL_PUNKTE))
check("die Zielzahl ist als VORSCHLAG gekennzeichnet (das Handbuch nennt keine)",
      P.vorschlaege().get("ziel_punkte", {}).get("status") == "VORSCHLAG",
      str(P.vorschlaege().get("ziel_punkte")))

root = None
try:
    root, app = setze_still(None)
    zustand = app.state
    check("die Seitenleiste hat eine Ziel-Zeile",
          beschriftung(getattr(app, "lbl_ziel", None)).startswith("Ziel:"),
          repr(beschriftung(getattr(app, "lbl_ziel", None))))

    check("vor der ersten Siedlung gilt die Partie NICHT als verloren",
          zustand.spielausgang()[0] == "weiter", zustand.spielausgang()[1])

    app._found_settlement()
    check("nach dem Gruenden laeuft die Partie", zustand.spielausgang()[0] == "weiter",
          zustand.spielausgang()[1])
    check("die Gruendung setzt das Kennzeichen hatte_siedlung", zustand.hatte_siedlung is True)

    # Sieg ueber die Zielpunktzahl: eine Forschung auf Stufe 9 ergibt 729 Forschungspunkte.
    gebiet = sorted(zustand.research)[0]
    zustand.research[gebiet].level = 9
    check("Stufe 9 gibt 729 Forschungspunkte (9 hoch 3)",
          P.forschungspunkte({gebiet: 9}) == 729, str(P.forschungspunkte({gebiet: 9})))
    stand = zustand.punktestand()
    check("die Gesamtpunktzahl liegt ueber dem Ziel von 300",
          stand["gesamt"] >= P.VORSCHLAG_ZIEL_PUNKTE, str(stand["gesamt"]))
    art, grund = zustand.spielausgang()
    check("erreichte Zielpunktzahl ergibt Sieg", art == "sieg", f"{art}: {grund}")

    app._render()
    check("die Ziel-Zeile meldet den Sieg",
          beschriftung(app.lbl_ziel).startswith("SIEG"), repr(beschriftung(app.lbl_ziel)))
    check("der Ausgang steht im Zustand", zustand.spielende == "sieg")
    check("und als Nachricht in den Meldungen",
          any(m.get("type") == "spielende" for m in zustand.messages), str(zustand.messages[-2:]))
    check("ein zweiter Aufruf aendert nichts (keine doppelte Meldung)",
          app._pruefe_spielende() == "sieg"
          and len([m for m in zustand.messages if m.get("type") == "spielende"]) == 1,
          str([m for m in zustand.messages if m.get("type") == "spielende"]))

    # Niederlage: keine Siedlung und keine Einheit mehr.
    zustand.spielende = None
    zustand.settlements = []
    for einheit in zustand.units.values():
        einheit.count = 0
    art, grund = zustand.spielausgang()
    check("ohne Siedlung und ohne Einheit ist die Partie verloren", art == "niederlage",
          f"{art}: {grund}")
    app._render()
    check("die Ziel-Zeile meldet die Niederlage",
          beschriftung(app.lbl_ziel).startswith("NIEDERLAGE"), repr(beschriftung(app.lbl_ziel)))
    check("der Ausgang steht im Zustand", zustand.spielende == "niederlage")
finally:
    if root is not None:
        try:
            root.destroy()
        except Exception:
            pass

sys.exit(bericht())
