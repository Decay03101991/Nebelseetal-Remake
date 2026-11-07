# -*- coding: ascii -*-
"""R3-2: Die Ereignisart haengt am BOTNAMEN, nicht an seiner Position (07.11.2026, Befund I-1).

Der Befund der dritten Modellrunde, am Code bestaetigt: `src/main.py` waehlte die Art ueber
`_arten[_index % len(_arten)]`. Der zweite Bot bekam damit die zweite Art - die Meldung las
"Brynhild: Grom braucht Messer". Geprueft wird jetzt:

  A. Die Zuordnung kommt aus der Datendatei: Haug -> haug, Grom -> grom, Silra -> silra.
  B. Ein Bot OHNE Art bekommt KEIN Ereignis (Brynhild und Krank) - nichts erfinden, keine
     Ersatzart, kein Rueckfall auf die Position.
  C. Der Titel einer Art nennt genau den Bot, dem die Art gehoert (kein fremder Name im Postfach).
  D. Quellwache: der Bot-Takt enthaelt keine Index-Rotation mehr und fragt `ereignis_art_fuer_bot`.
  E. Echter Verlauf in der App: fuenf Bots in der Reihenfolge Haug, Brynhild, Grom, Silra, Krank -
     es entstehen genau DREI Ereignisse, und JEDE Meldung nennt den Bot, dessen Titel sie traegt.
  F. GEGENPROBE: derselbe Verlauf mit der alten Index-Rotation wuerde einen fremden Namen melden -
     die Wache prueft, dass die Zuordnungsfunktion das NICHT tut (Bot an Position 2 ist nicht Grom).

ASCII-only (Pruefdatei-Konvention).
"""
from __future__ import annotations

import ast
import inspect
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, befund, bericht, check, import_src

WURZEL, SRC = import_src()
import diplomatie as D  # noqa: E402
import main  # noqa: E402
import story  # noqa: E402
import zeitbasis  # noqa: E402

TAG = float(zeitbasis.SEKUNDEN_JE_TAG)  # ein Spieltag (R3-1: die EINE Quelle)
DREI_TAGE = 3 * TAG                     # Haeufigkeit: das erste Ereignis wartet sie ebenfalls ab


def _code(funktion) -> str:
    """Quelltext einer Funktion ohne Docstring (Docstrings zaehlen nicht als Code)."""
    baum = ast.parse(textwrap.dedent(inspect.getsource(funktion)))  # Funktion in einen Baum wandeln
    kopf = baum.body[0]  # der FunctionDef-Knoten
    if kopf.body and isinstance(kopf.body[0], ast.Expr) and isinstance(kopf.body[0].value, ast.Constant):
        kopf.body = kopf.body[1:]  # fuehrenden Docstring abschneiden
    return ast.unparse(baum)  # Rest als Text


def _daten() -> dict:
    """Die echte Datendatei."""
    return D.daten()


abschnitt("A. Die Zuordnung kommt aus der Datendatei")
datei = _daten()
arten = (datei.get("ereignisse") or {}).get("arten") or {}
check("die Datei fuehrt drei Ereignisarten", len(arten) == 3, str(sorted(arten)))
check("jede Art traegt ihren Botnamen", all(str(v.get("name") or "") for v in arten.values()),
      str({k: v.get("name") for k, v in arten.items()}))
for erwartet, name in (("haug", "Haug"), ("grom", "Grom"), ("silra", "Silra")):  # drei Zuordnungen
    gefunden = D.ereignis_art_fuer_bot({"name": name})  # Zuordnung fragen
    check("%s bekommt die Art %s" % (name, erwartet), gefunden == erwartet, str(gefunden))

abschnitt("B. Ein Bot ohne Art bekommt KEIN Ereignis")
for name in ("Brynhild", "Krank", "Fremder", ""):  # vier Bots ohne eigene Art
    check("%r bekommt keine Art" % name, D.ereignis_art_fuer_bot({"name": name}) == "",
          str(D.ereignis_art_fuer_bot({"name": name})))
check("auch ohne Namen im dict keine Art", D.ereignis_art_fuer_bot({}) == "", "leeres dict")
check("auch ein Objekt statt dict wird gelesen",
      D.ereignis_art_fuer_bot(type("B", (), {"name": "Silra"})()) == "silra", "Objektform")
check("Gross- und Kleinschreibung und Leerraum sind egal",
      D.ereignis_art_fuer_bot({"name": "  gROM "}) == "grom", "gROM")
eigene = {"ereignisse": {"aktiv": True, "arten": {"x": {"name": "Testbot", "zahlungen": []}}}}  # eigene Datei
check("die Zuordnung liest die UEBERGEBENE Datei",
      D.ereignis_art_fuer_bot({"name": "Testbot"}, eigene) == "x", "Testbot -> x")
check("ohne Arten in der Datei keine Zuordnung",
      D.ereignis_art_fuer_bot({"name": "Testbot"}, {"ereignisse": {"aktiv": True}}) == "", "leer")
ohne_name = {"ereignisse": {"arten": {"haug": {"zahlungen": []}}}}  # Art OHNE Namensfeld
check("fehlt der Name, gilt der Schluessel",
      D.ereignis_art_fuer_bot({"name": "Haug"}, ohne_name) == "haug", "Rueckfall Schluessel")

abschnitt("C. Der Titel einer Art nennt den eigenen Bot")
for art, angaben in arten.items():  # jede Art ansehen
    titel = story.ereignis_text(art, "titel")  # Ueberschrift aus story.json
    check("Titel von %s nennt %s" % (art, angaben.get("name")),
          str(angaben.get("name")) in str(titel), str(titel))
    fremd = [n for n in ("Haug", "Grom", "Silra") if n != str(angaben.get("name")) and n in str(titel)]
    check("Titel von %s nennt keinen fremden Bot" % art, fremd == [], str(fremd))

abschnitt("D. Quellwache: keine Index-Rotation mehr im Bot-Takt")
quelle_takt = _code(main.GameState.bots_fortschreiben)
check("keine Rotation ueber den Bot-Index", "% len(_arten)" not in quelle_takt, "kein Modulo")
check("der Takt fragt die Zuordnung nach dem Namen",
      "diplomatie.ereignis_art_fuer_bot(" in quelle_takt, "Aufruf vorhanden")
check("der Takt ueberspringt Bots ohne Art", "if not _art:" in quelle_takt, "continue-Weg")
check("ereignis_art_fuer_bot liest den Namen (Quellwache)",
      "get('name')" in _code(D.ereignis_art_fuer_bot) or 'get("name")' in _code(D.ereignis_art_fuer_bot),
      "liest den Botnamen")

abschnitt("E. Echter Verlauf: fuenf Bots, drei Ereignisse, kein fremder Name")
root = None
app = None
try:
    import tkinter as tk  # Oberflaeche nur fuer diesen Abschnitt
    root = tk.Tk()  # unsichtbares Fenster
    root.withdraw()  # nichts auf dem Schirm
    app = main.NebelseetalApp(root)  # die echte App
    app._build_main_ui()  # Oberflaeche aufbauen
    st = app.state  # der Spielzustand
    app._erste_siedlung_gruenden()  # echter Start mit den belegten Werten
    st.bots = []  # fuenf Bots in der Reihenfolge, in der der Fehler auftrat
    for _name in ("Haug", "Brynhild", "Grom", "Silra", "Krank"):  # Brynhild steht auf Position 1
        _b = main.BotPlayer(name=_name, faction="menschlich", aggression=0.5, trading=0.5)
        _b.doerfer = [main.BotDorf(name=_name + "sdorf", hauptdorf=True, dimension=1, herkunftswelt=1)]
        _b.doerfer[0].vorraete = {"holz": 500.0, "stein": 500.0, "nahrung": 500.0}
        _b.doerfer[0].wall_stufe = 0
        _b.doerfer[0].wall_zustand = 100.0
        st.bots.append(_b)
    st.noob_protection = True  # kein Bot-Angriff in dieser Probe
    st.ereignisse = []  # sauberer Anfang
    st._letzter_bot_takt = 0.0
    st.bots_fortschreiben(DREI_TAGE)  # erster Takt nach drei Spieltagen
    check("es entstehen genau drei Ereignisse (nur Haug, Grom, Silra)",
          len(st.ereignisse) == 3, str([e.get("bot") for e in st.ereignisse]))
    bot_je_art = {e["art"]: e["bot"] for e in st.ereignisse}  # Art -> Botname
    check("Haug traegt die Art haug", bot_je_art.get("haug") == "Haug", str(bot_je_art))
    check("Grom traegt die Art grom", bot_je_art.get("grom") == "Grom", str(bot_je_art))
    check("Silra traegt die Art silra", bot_je_art.get("silra") == "Silra", str(bot_je_art))
    check("Brynhild und Krank bekommen kein Ereignis",
          not any(e.get("bot") in ("Brynhild", "Krank") for e in st.ereignisse),
          str([e.get("bot") for e in st.ereignisse]))
    meldungen = [m.get("text") for m in st.messages if m.get("type") == "ereignis"]  # Postfach
    check("drei Meldungen im Postfach", len(meldungen) == 3, str(meldungen))
    fremd = []  # Meldungen, deren Titel nicht zum genannten Bot gehoert
    for text in meldungen:  # jede Meldung ansehen
        if ":" not in str(text):  # unerwartete Form
            fremd.append(text)
            continue  # dann als Befund fuehren
        links, rechts = str(text).split(":", 1)  # "Bot: Titel"
        if links.strip() not in rechts:  # Titel nennt einen anderen Bot
            fremd.append(text)
    check("keine Meldung nennt einen fremden Bot", fremd == [], str(fremd))
    check("die alte Fehlerform kommt nicht vor",
          not any(str(t).startswith("Brynhild: Grom") for t in meldungen), "kein Brynhild/Grom")
finally:
    if root is not None:
        try:
            root.destroy()
        except Exception:
            pass

abschnitt("F. GEGENPROBE: der Bot an Position 2 ist NICHT Grom")
reihenfolge = ["Haug", "Brynhild", "Grom", "Silra", "Krank"]  # dieselbe Reihenfolge wie oben
alte_art = arten and list(arten)[2 % len(arten)]  # was die ALTE Rotation an Position 2 gewaehlt haette
check("die alte Rotation haette an Position 2 die dritte Art gewaehlt", alte_art == "silra",
      str(alte_art))
check("die neue Zuordnung gibt Brynhild trotzdem keine Art",
      D.ereignis_art_fuer_bot({"name": reihenfolge[1]}) == "", "kein Positionsbezug")
check("Grom bekommt seine Art unabhaengig von der Position",
      D.ereignis_art_fuer_bot({"name": "Grom"}) == "grom", "namensbasiert")

sys.exit(bericht())
