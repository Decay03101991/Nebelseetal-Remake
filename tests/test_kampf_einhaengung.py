"""
Pruefung: Ist der Kampf (src/kampf.py + src/kampfbericht.py) WIRKLICH in den
Angriffspfad von src/main.py einghaengt?

Nicht die Module allein werden geprueft (das tun tests/test_kampf.py und
tests/test_kampfbericht.py), sondern die EINHAENGUNG: laeuft NebelseetalApp._angriff_durchfuehren
wirklich durch kampf.fuehre_schlacht und schreibt kampfbericht.spieldaten_anwenden die Verluste
und die Beute in den Spielstand? Rufen _attack und _attack_map denselben Weg auf?

Bewiesen wird am echten, unsichtbaren Fenster (root.withdraw(), kein mainloop) und mit echten
Schlachten — kampf/kampfbericht werden NICHT nachgebaut und NICHT ersetzt:
  1. ohne Kaempfer/Belagerung: Rueckgabe False, Ressourcen unveraendert, Meldung 'Keine Kaempfer'
  2. Kaempfer ohne Karren: Sieg gegen leeren Verteidiger aendert KEINE Ressource (Beute braucht Karren)
  3. mit Karren: die Beute landet wirklich in state.resources, der Bericht nennt 'Beute:'
  4. die Berichtsmeldung liegt mit type 'kampf' in state.messages und nennt 'Schlachtbericht'/'Ausgang:'
  5. Verluste senken state.units wirklich (2 Kaempfer gegen eine Uebermacht)
  6. ein zu hoher Wall (Stufe 4) fuehrt zum echten Rueckzug-Wortlaut aus kampf/kampfbericht
  7. _vorraete_des_ziels ist je Name deterministisch, unterscheidet Namen, nutzt eigene Vorraete
  8. _truppen_nach_rolle trennt die drei Rollen des Handbuchs
und die eigene Methode pruefe_einhaengung(): main laedt beide Module, und alle drei Aufrufer
(_angriff_durchfuehren, _attack, _attack_map) rufen den gemeinsamen Weg.

Aufruf:  python -X utf8 tests/test_kampf_einhaengung.py
"""
from __future__ import annotations

import inspect
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, bericht, check, import_src

ROOT, SRC = import_src()
os.chdir(SRC)

import botkern
import einheiten as E
import kampf
import kampfbericht as KB

# ==========================================================================
# Aufbau: das echte, unsichtbare Fenster
# ==========================================================================

main = ausnahme("main importieren", lambda: __import__("main"))
tk = ausnahme("tkinter laden", lambda: __import__("tkinter"))

if main is None or tk is None:
    sys.exit(bericht())


def nur_code(quelle: str) -> str:
    """Nur ausfuehrbare Zeilen — Kommentarzeilen fliegen raus.

    Die Kommentare in main.py nennen absichtlich die alte Daumenformel, um zu erklaeren, was
    ersetzt wurde. Sie sind kein Code und duerfen die Pruefung nicht verfaelschen.
    """
    return "\n".join(z for z in quelle.splitlines() if not z.strip().startswith("#"))


# ==========================================================================
# 1. Einhaengung — die eigene Nachweismethode
# ==========================================================================

abschnitt("1. Einhaengung: main.py benutzt wirklich src/kampf.py + src/kampfbericht.py")


def pruefe_einhaengung():
    """Eigene Methode: main laedt beide Module, und alle Aufrufer gehen den gemeinsamen Weg."""
    check("main.py hat das Modul kampf geladen", getattr(main, "kampf", None) is not None)
    check("main.kampf ist DASSELBE Modul wie src/kampf.py (kein Nachbau)",
          getattr(main, "kampf", None) is kampf)
    check("main.kampfbericht ist DASSELBE Modul wie src/kampfbericht.py (kein Nachbau)",
          getattr(main, "kampfbericht", None) is KB)

    quelle = inspect.getsource(main.NebelseetalApp._angriff_durchfuehren)
    check("_angriff_durchfuehren ruft kampf.fuehre_schlacht",
          "kampf.fuehre_schlacht" in quelle)
    check("_angriff_durchfuehren bucht ueber kampfbericht.spieldaten_anwenden",
          "kampfbericht.spieldaten_anwenden" in quelle)
    check("_angriff_durchfuehren baut die Meldung ueber kampfbericht.bericht",
          "kampfbericht.bericht" in quelle)
    check("_angriff_durchfuehren benutzt _truppen_nach_rolle",
          "_truppen_nach_rolle" in quelle)

    check("_attack (Bot) geht durch _angriff_durchfuehren",
          "_angriff_durchfuehren" in inspect.getsource(main.NebelseetalApp._attack))
    check("_attack_map (Karte) geht durch _angriff_durchfuehren",
          "_angriff_durchfuehren" in inspect.getsource(main.NebelseetalApp._attack_map))

    alt = (nur_code(inspect.getsource(main.NebelseetalApp._attack))
           + nur_code(inspect.getsource(main.NebelseetalApp._attack_map)))
    check("die alte Daumenformel (player_power/get_combat_power) ist aus _attack/_attack_map weg",
          "player_power" not in alt and "get_combat_power" not in alt,
          "kein 'player_power', kein 'get_combat_power' in den Rechenzeilen")


ausnahme("Einhaengung pruefen", pruefe_einhaengung)


# ==========================================================================
# Fenster aufbauen und die Szenarien durchspielen
# ==========================================================================

root = None
app = None


def setze_truppen(app_objekt, kaempfer=0, belagerung=0, karren=0):
    """Alle Zaehler auf 0, dann genau die gewuenschten Rollen setzen."""
    for u in app_objekt.state.units.values():
        u.count = 0
    if kaempfer:
        app_objekt.state.units["Krieger"].count = kaempfer
    if belagerung:
        app_objekt.state.units["Katapult"].count = belagerung
    if karren:
        app_objekt.state.units["Handkarren"].count = karren


def ressourcen_stand(app_objekt) -> dict:
    return {k: r.amount for k, r in app_objekt.state.resources.items()}


def letzte_nachricht(app_objekt) -> dict:
    return app_objekt.state.messages[-1] if app_objekt.state.messages else {}


try:
    root = tk.Tk()
    root.withdraw()                 # kein sichtbares Fenster
    app = main.NebelseetalApp(root)
    app._build_main_ui()
    root.update_idletasks()

    # ======================================================================
    # 2. Ohne Truppen: gar kein Kampf
    # ======================================================================

    abschnitt("2. Ohne Kaempfer und ohne Belagerung wird gar nicht gekaempft")

    setze_truppen(app)
    app.state.messages.clear()
    vor = ressourcen_stand(app)
    ergebnis = ausnahme("Angriff ohne Truppen", lambda: app._angriff_durchfuehren(
        "Ziel", {"Krieger": 3}))
    nach = ressourcen_stand(app)
    check("_angriff_durchfuehren gibt False zurueck (nicht gekaempft)", ergebnis is False,
          repr(ergebnis))
    check("die Ressourcen bleiben unveraendert", vor == nach, f"{vor} -> {nach}")
    check("eine Meldung mit 'Keine Kaempfer' liegt in state.messages",
          any("Keine Kaempfer" in m.get("text", "") for m in app.state.messages),
          str([m.get("text") for m in app.state.messages]))
    check("die Meldung hat den Typ 'kampf'", letzte_nachricht(app).get("type") == "kampf",
          str(letzte_nachricht(app).get("type")))
    check("auch die Einheiten bleiben unveraendert (alle 0)",
          all(u.count == 0 for u in app.state.units.values()))

    # ======================================================================
    # 3. _truppen_nach_rolle trennt die Rollen wirklich
    # ======================================================================

    abschnitt("3. _truppen_nach_rolle trennt kaempfer / belagerung / karren")

    setze_truppen(app, kaempfer=2, belagerung=1, karren=3)
    kaempfer, belagerung, karren = app._truppen_nach_rolle()
    check("Kaempfer: genau {'Krieger': 2}", kaempfer == {"Krieger": 2}, str(kaempfer))
    check("Belagerung: genau {'Katapult': 1}", belagerung == {"Katapult": 1}, str(belagerung))
    check("Karren: genau {'Handkarren': 3}", karren == {"Handkarren": 3}, str(karren))
    check("die drei Rollen ueberschneiden sich nicht",
          not (set(kaempfer) & set(belagerung)) and not (set(kaempfer) & set(karren))
          and not (set(belagerung) & set(karren)))

    # ======================================================================
    # 4. _vorraete_des_ziels: deterministisch je Name, eigene Vorraete verbatim
    # ======================================================================

    abschnitt("4. _vorraete_des_ziels: Name entscheidet, eigene Vorraete gelten wortgetreu")

    a1 = app._vorraete_des_ziels({"name": "Alpha"})
    a2 = app._vorraete_des_ziels({"name": "Alpha"})
    b = app._vorraete_des_ziels({"name": "Beta"})
    check("gleicher Name -> immer dasselbe Lager", a1 == a2, f"{a1} == {a2}")
    check("verschiedene Namen -> verschiedene Lager, stabil", a1 != b, f"{a1} != {b}")
    check("die Stoffe sind genau die VORSCHLAG-Spannen aus botkern",
          set(a1) == set(botkern.VORSCHLAG_START_VORRAETE),
          f"{sorted(a1)}")
    eigene = {"holz": 5.0, "stein": 3.0}
    check("ein Ziel mit eigenem 'vorraete'-dict wird wortgetreu uebernommen",
          app._vorraete_des_ziels({"name": "Burg", "vorraete": eigene}) == eigene)
    check("auch das Attribut .vorraete eines Objekts gilt wortgetreu",
          app._vorraete_des_ziels(type("Z", (), {"name": "Z", "vorraete": {"gold": 7.0}})())
          == {"gold": 7.0})

    # ======================================================================
    # 5. Sieg ohne Karren: es wird nicht gepluendert
    # ======================================================================

    abschnitt("5. Kaempfer ohne Karren: Sieg gegen leeren Verteidiger, aber keine Beute")

    setze_truppen(app, kaempfer=30)
    app.state.messages.clear()
    vor = ressourcen_stand(app)
    ergebnis = app._angriff_durchfuehren("Ziel", {}, vorraete={"holz": 500.0, "stein": 300.0})
    nach = ressourcen_stand(app)
    check("_angriff_durchfuehren gibt True zurueck (gekaempft)", ergebnis is True, repr(ergebnis))
    check("ohne Karren aendert der Sieg KEINE Ressource", vor == nach, f"{vor} -> {nach}")
    check("der Bericht sagt ausdruecklich 'Beute: keine'",
          "Beute: keine" in letzte_nachricht(app).get("text", ""),
          str([z for z in letzte_nachricht(app).get("text", "").split("\n") if "Beute" in z]))

    # ======================================================================
    # 6. Mit Karren: die Beute landet wirklich in state.resources
    # ======================================================================

    abschnitt("6. Mit Karren: die Beute landet wirklich im Spielstand")

    setze_truppen(app, kaempfer=30, karren=2)
    app.state.messages.clear()
    vor = ressourcen_stand(app)
    ergebnis = app._angriff_durchfuehren("Ziel", {}, vorraete={"holz": 500.0, "stein": 300.0})
    nach = ressourcen_stand(app)
    diff = {k: nach[k] - vor[k] for k in vor if nach[k] != vor[k]}
    check("die Beute kommt in state.resources an: holz +50, stein +30",
          diff == {"holz": 50.0, "stein": 30.0}, str(diff))
    check("der Bericht nennt die Beute: 'Beute: holz 50, stein 30'",
          "Beute: holz 50, stein 30" in letzte_nachricht(app).get("text", ""),
          str([z for z in letzte_nachricht(app).get("text", "").split("\n") if "Beute" in z]))

    # ======================================================================
    # 7. Die Berichtsmeldung hat die richtige Form
    # ======================================================================

    abschnitt("7. Die Meldung liegt als 'kampf' in state.messages")

    meldung = letzte_nachricht(app)
    text = meldung.get("text", "")
    check("die letzte Meldung hat den Typ 'kampf'", meldung.get("type") == "kampf")
    # Seit 05.10.2026 nennt die Meldung ZUERST das Ziel: im Reiter „Nachrichten" war bisher nicht
    # zu sehen, wozu der Bericht gehoert (offener Punkt aus Schritt 3, dort als Verbesserung notiert).
    check("der Text nennt erst das Ziel und dann den Schlachtbericht",
          text.startswith("Ziel ") and "Schlachtbericht" in text, text[:60])
    check("der Text enthaelt 'Ausgang:'", "Ausgang:" in text)
    check("der Text ist die Zusammenfassung aus kampfbericht.bericht (Titel + Zeilen)",
          "\n" in text and "Verluste Angreifer:" in text)

    # ======================================================================
    # 8. Verluste senken state.units wirklich
    # ======================================================================

    abschnitt("8. Verluste senken state.units wirklich (2 Kaempfer gegen Uebermacht)")

    setze_truppen(app, kaempfer=2)
    app.state.messages.clear()
    vor_count = app.state.units["Krieger"].count
    ergebnis = app._angriff_durchfuehren("Ziel", {"Paladin": 200})
    nach_count = app.state.units["Krieger"].count
    check("der Angreifer verliert Einheiten (2 -> 0)", nach_count < vor_count,
          f"{vor_count} -> {nach_count}")
    check("der Kampf endet mit einem Verteidigersieg", "Der Verteidiger siegt" in
          letzte_nachricht(app).get("text", ""), letzte_nachricht(app).get("text", "")[:60])

    # ======================================================================
    # 9. Zu hoher Wall: der echte Rueckzug-Wortlaut
    # ======================================================================

    abschnitt("9. Wall Stufe 4 mit 2 Kaempfern: echter Rueckzug aus kampf/kampfbericht")

    setze_truppen(app, kaempfer=2)
    app.state.messages.clear()
    app._angriff_durchfuehren("Ziel", {"Krieger": 1}, wall_stufe=4)
    text = letzte_nachricht(app).get("text", "")
    check("der Bericht nennt 'Schwelle nicht erreicht'", "Schwelle nicht erreicht" in text,
          text[:80])
    check("der Bericht nennt 'die Truppen ziehen sich zurueck'",
          "die Truppen ziehen sich zurueck" in text,
          str([z for z in text.split("\n") if "zurueck" in z.lower()]))
    check("der Ausgang ist Unentschieden (Rueckzug ohne Beute)",
          "Schlachtbericht: Unentschieden" in text, text[:60])

    # ======================================================================
    # 10. _attack und _attack_map laufen wirklich durch denselben Weg
    # ======================================================================

    abschnitt("10. _attack (Bot) und _attack_map (Karte) erzeugen echte Kampfmeldungen")

    setze_truppen(app, kaempfer=30)
    app.state.map_garrison["wald"] = {"Bürgerwehr": 2}
    app.state.active_maps = ["kontinent", "wald"]
    app.state.messages.clear()
    app._attack_map("wald")
    m1 = letzte_nachricht(app)
    check("_attack_map erzeugt eine 'kampf'-Meldung", m1.get("type") == "kampf")
    check("_attack_map protokolliert das Ziel 'Nebelwald'", "Ziel Nebelwald" in app.state.log[-1],
          app.state.log[-1])

    setze_truppen(app, kaempfer=30)
    app.state.noob_protection = False
    bot = main.BotPlayer("Testbot", "menschlich", 0.5, 0.5, army={"Bürgerwehr": 2})
    bot.noob_protection = False
    app.state.messages.clear()
    app._attack(bot)
    m2 = letzte_nachricht(app)
    check("_attack erzeugt eine 'kampf'-Meldung", m2.get("type") == "kampf")
    check("_attack protokolliert den Bot als Ziel 'Testbot'", "Ziel Testbot" in app.state.log[-1],
          app.state.log[-1])

finally:
    if root is not None:
        try:
            root.destroy()
        except Exception:
            pass

sys.exit(bericht())
