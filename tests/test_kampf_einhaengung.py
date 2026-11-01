"""
Pruefung: Ist der Kampf (src/kampf.py + src/kampfbericht.py) WIRKLICH in den
Angriffspfad von src/main.py einghaengt?

Nicht die Module allein werden geprueft (das tun tests/test_kampf.py und
tests/test_kampfbericht.py), sondern die EINHAENGUNG: laeuft der Angriff wirklich durch
kampf.fuehre_schlacht und schreibt kampfbericht.spieldaten_anwenden die Verluste und die
Beute in den Spielstand?

ENTSCHEIDUNG 1 (Daniel, 01.11.2026): JEDER Angriff REIST. Es gibt keinen Sofortpfad mehr.
Damit wandert der Anker dieser Pruefung: angreifen -> Auftrag starten -> Marsch -> Ankunft
(`kampf_am_ziel`) -> Rueckkehr (`einsatz_zurueck`). Die frueheren Szenarien bleiben inhaltlich
dieselben, laufen aber ueber den Auftragsweg:

  1. ohne Kaempfer/Belagerung: Rueckgabe False, Ressourcen unveraendert, Meldung 'Keine Kaempfer'
  2. Kaempfer ohne Karren: Sieg gegen leeren Verteidiger, aber KEINE Beute (Beute braucht Karren)
  3. mit Karren: die Beute kommt mit den Ueberlebenden zurueck, der Bericht nennt 'Beute:'
  4. die Berichtsmeldung liegt mit type 'kampf' in state.messages und nennt das Ziel zuerst
  5. bei Niederlage erzaehlt der Bericht ehrlich und erzeugt keine Einheiten
  6. Mauer Stufe 5 ohne Belagerung erzwingt einen Rueckzug laut neuer Quelle
  7. _vorraete_des_ziels ist je Name deterministisch, unterscheidet Namen, nutzt eigene Vorraete
  8. _truppen_nach_rolle trennt die drei Rollen des Handbuchs
  9. NEU: kein Pfad ohne Marsch - _angriff_durchfuehren ist fort, _attack und _attack_map starten
     Auftraege, und waehrend des Marsches sind die Truppen NICHT doppelt verfuegbar

Aufruf:  python -X utf8 tests/test_kampf_einhaengung.py
"""
from __future__ import annotations

import inspect
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import (abschnitt, angriff_mit_marsch, ausnahme, bericht, check,
                     import_src)

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
    """Nur ausfuehrbare Zeilen - Kommentarzeilen fliegen raus.

    Die Kommentare in main.py nennen absichtlich die alte Daumenformel, um zu erklaeren, was
    ersetzt wurde. Sie sind kein Code und duerfen die Pruefung nicht verfaelschen.
    """
    return "\n".join(z for z in quelle.splitlines() if not z.strip().startswith("#"))


# ==========================================================================
# 1. Einhaengung - die eigene Nachweismethode
# ==========================================================================

abschnitt("1. Einhaengung: main.py benutzt wirklich src/kampf.py + src/kampfbericht.py")


def pruefe_einhaengung():
    """Eigene Methode: main laedt beide Module, und alle Aufrufer gehen den EINEN Weg."""
    check("main.py hat das Modul kampf geladen", getattr(main, "kampf", None) is not None)
    check("main.kampf ist DASSELBE Modul wie src/kampf.py (kein Nachbau)",
          getattr(main, "kampf", None) is kampf)
    check("main.kampfbericht ist DASSELBE Modul wie src/kampfbericht.py (kein Nachbau)",
          getattr(main, "kampfbericht", None) is KB)

    # ENTSCHEIDUNG Daniel 31.10.2026 (Frage 17) und 01.11.2026 (Entscheidung 1): es gibt EINEN
    # Kampfweg, und er ist ein REISEAUFTRAG. Der Kampf selbst (Schlacht, Beute, Bericht) liegt
    # in `kampf_am_ziel`; der Sofortpfad `_angriff_durchfuehren` ist stillgelegt.
    kern = inspect.getsource(main.NebelseetalApp._angriff_auftrag_starten)
    kampfweg = inspect.getsource(main.GameState.kampf_am_ziel)
    check("der eine Angriffsweg startet einen AUFTRAG (auftrag_starten)",
          "auftrag_starten" in kern)
    check("der Kampf ruft kampf.fuehre_schlacht (in kampf_am_ziel)",
          "kampf.fuehre_schlacht" in kampfweg)
    check("die Beute kommt aus kampfbericht.beute_am_ziel (in kampf_am_ziel)",
          "kampfbericht.beute_am_ziel" in kampfweg)
    check("der Sofortpfad _angriff_durchfuehren ist fort (kein zweiter Kampfweg)",
          not hasattr(main.NebelseetalApp, "_angriff_durchfuehren"))
    check("der eine Angriffsweg nimmt die Truppen aus _truppen_nach_rolle",
          "_truppen_nach_rolle" in kern)

    check("_attack (Bot) geht in den Auftragsweg",
          "_auftrag_angriff" in inspect.getsource(main.NebelseetalApp._attack))
    check("_attack_map (Karte) geht in den Auftragsweg",
          "_angriff_auftrag_starten" in inspect.getsource(main.NebelseetalApp._attack_map))
    check("_attack_map kaempft NICHT mehr selbst (kein kampf_am_ziel im Aufrufer)",
          "kampf_am_ziel" not in inspect.getsource(main.NebelseetalApp._attack_map))

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


def letzte_nachricht(app_objekt, typ=None) -> dict:
    """Die letzte Meldung - wahlweise nur die eines Typs ('kampf', 'auftrag')."""
    texte = [m for m in app_objekt.state.messages if typ is None or m.get("type") == typ]
    return texte[-1] if texte else {}


def marsch_zu_ende(app_objekt):
    """Den laufenden Auftrag bis zur Rueckkehr laufen lassen (ohne Zeit zu raten)."""
    if not app_objekt.state.auftraege:
        return
    eintrag = app_objekt.state.auftraege[-1]
    ende = float(eintrag.get("rueckkehr") or eintrag.get("ankunft") or 0.0) + 1.0
    app_objekt.state.spielsekunden = max(float(app_objekt.state.spielsekunden), ende)
    app_objekt.state.auftraege_fortschreiben(app_objekt.state.spielsekunden)


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
    ergebnis = ausnahme("Angriff ohne Truppen", lambda: app._angriff_auftrag_starten(
        "Ziel", {"Krieger": 3}))
    nach = ressourcen_stand(app)
    check("der Angriffsweg gibt False zurueck (nicht gestartet)", ergebnis is False,
          repr(ergebnis))
    check("die Ressourcen bleiben unveraendert", vor == nach, f"{vor} -> {nach}")
    check("eine Meldung mit 'Keine Kaempfer' liegt in state.messages",
          any("Keine Kaempfer" in m.get("text", "") for m in app.state.messages),
          str([m.get("text") for m in app.state.messages]))
    check("die Meldung hat den Typ 'kampf'", letzte_nachricht(app).get("type") == "kampf",
          str(letzte_nachricht(app).get("type")))
    check("auch die Einheiten bleiben unveraendert (alle 0)",
          all(u.count == 0 for u in app.state.units.values()))
    check("ohne Truppen wird KEIN Auftrag angelegt", not app.state.auftraege,
          str(len(app.state.auftraege)))

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
    app.state.auftraege.clear()
    vor = ressourcen_stand(app)
    ergebnis = angriff_mit_marsch(app, "Ziel", {}, vorraete={"holz": 500.0, "stein": 300.0})
    nach = ressourcen_stand(app)
    check("der Aufruf meldet den gestarteten Auftrag (True)", ergebnis is True, repr(ergebnis))
    check("ohne Karren aendert der Sieg KEINE Beute (holz/stein unveraendert)",
          nach.get("holz") == vor.get("holz") and nach.get("stein") == vor.get("stein"),
          f"{vor} -> {nach}")
    check("der Bericht sagt ausdruecklich 'Beute: keine'",
          "Beute: keine" in letzte_nachricht(app, "kampf").get("text", ""),
          str([z for z in letzte_nachricht(app, "kampf").get("text", "").split("\n")
               if "Beute" in z]))

    # ======================================================================
    # 6. Mit Karren: die Beute landet wirklich im Spielstand
    # ======================================================================

    abschnitt("6. Mit Karren: die Beute kommt mit den Ueberlebenden zurueck")

    setze_truppen(app, kaempfer=30, karren=2)
    app.state.messages.clear()
    app.state.auftraege.clear()
    vor = ressourcen_stand(app)
    ergebnis = angriff_mit_marsch(app, "Ziel", {}, vorraete={"holz": 500.0, "stein": 300.0})
    nach = ressourcen_stand(app)
    diff = {k: round(nach[k] - vor[k], 2) for k in vor if nach[k] != vor[k]}
    check("die Beute kommt im Lager an: holz +50, stein +30",
          diff.get("holz") == 50.0 and diff.get("stein") == 30.0, str(diff))
    check("der Bericht nennt die Beute: 'Beute: holz 50, stein 30'",
          "Beute: holz 50, stein 30" in letzte_nachricht(app, "kampf").get("text", ""),
          str([z for z in letzte_nachricht(app, "kampf").get("text", "").split("\n")
               if "Beute" in z]))
    check("die Reise kostet Gold/Nahrung/Mana, aber kein Holz und keinen Stein",
          all(diff.get(k, 0.0) >= 0.0 for k in ("holz", "stein")), str(diff))

    # ======================================================================
    # 7. Die Berichtsmeldung hat die richtige Form
    # ======================================================================

    abschnitt("7. Die Meldung liegt als 'kampf' in state.messages")

    meldung = letzte_nachricht(app, "kampf")
    text = meldung.get("text", "")
    check("die letzte Kampfmeldung hat den Typ 'kampf'", meldung.get("type") == "kampf")
    check("der Text nennt erst das Ziel und dann den Schlachtbericht",
          text.startswith("Am Ziel ") and "Schlachtbericht" in text, text[:60])
    check("der Text enthaelt 'Ausgang:'", "Ausgang:" in text)
    check("der Text ist die Zusammenfassung aus kampfbericht.bericht (Titel + Zeilen)",
          "\n" in text and "Verluste Angreifer:" in text)

    # ======================================================================
    # 8. Verluste senken den Bestand wirklich
    # ======================================================================

    abschnitt("8. Verluste senken den Bestand wirklich (2 Kaempfer gegen Uebermacht)")

    setze_truppen(app, kaempfer=2)
    app.state.messages.clear()
    app.state.auftraege.clear()
    vor_count = app.state.units["Krieger"].count
    ergebnis = angriff_mit_marsch(app, "Ziel", {"Paladin": 200})
    nach_count = app.state.units["Krieger"].count
    # Neues Originalmodell: Unterlegene Einheiten koennen nach einer
    # Konstitutionsprobe ueberleben. Eine Niederlage ist kein Totalverlust.
    check("der Angriff startet auch gegen Uebermacht", ergebnis is True, repr(ergebnis))
    check("der Bestand waechst durch eine Niederlage nicht",
          0 <= nach_count <= vor_count, f"{vor_count} -> {nach_count}")
    check("der Kampf endet mit einem Verteidigersieg", "Der Verteidiger siegt" in
          letzte_nachricht(app, "kampf").get("text", ""),
          letzte_nachricht(app, "kampf").get("text", "")[:60])

    # ======================================================================
    # 9. Zu hoher Wall: der echte Rueckzug-Wortlaut
    # ======================================================================

    abschnitt("9. Wall Stufe 5 ohne Belagerung: zwingender Rueckzug")

    setze_truppen(app, kaempfer=2)
    app.state.messages.clear()
    app.state.auftraege.clear()
    angriff_mit_marsch(app, "Ziel", {"Krieger": 1}, wall_stufe=5)
    text = letzte_nachricht(app, "kampf").get("text", "")
    check("der Bericht nennt 'Schwelle nicht erreicht'", "Schwelle nicht erreicht" in text,
          text[:80])
    check("der Bericht nennt 'die Truppen ziehen sich zurueck'",
          "die Truppen ziehen sich zurueck" in text,
          str([z for z in text.split("\n") if "zurueck" in z.lower()]))
    check("der Ausgang ist Unentschieden (Rueckzug ohne Beute)",
          "Schlachtbericht: Unentschieden" in text, text[:60])

    # ======================================================================
    # 10. _attack und _attack_map starten Auftraege mit Marsch
    # ======================================================================

    abschnitt("10. _attack (Bot) und _attack_map (Karte) starten einen REISEAUFTRAG")

    setze_truppen(app, kaempfer=30)
    app.state.map_garrison["wald"] = {"Bürgerwehr": 2}
    app.state.active_maps = ["kontinent", "wald"]
    app.state.messages.clear()
    app.state.auftraege.clear()
    gestartet = app._attack_map("wald")
    check("_attack_map startet einen Auftrag der Art 'angreifen'",
          bool(gestartet) and bool(app.state.auftraege)
          and app.state.auftraege[-1].get("art") == "angreifen",
          str([e.get("art") for e in app.state.auftraege]))
    check("_attack_map erzeugt NOCH keine Kampfmeldung (der Angriff reist erst)",
          not [m for m in app.state.messages if m.get("type") == "kampf"],
          str([m.get("type") for m in app.state.messages]))
    marsch_zu_ende(app)
    m1 = letzte_nachricht(app, "kampf")
    check("nach der Ankunft liegt eine 'kampf'-Meldung vor", m1.get("type") == "kampf")
    check("_attack_map protokolliert das Ziel 'Nebelwald'",
          any("Kampf am Ziel Nebelwald" in z for z in app.state.log), str(app.state.log[-1]))
    check("der Auftrag ist nach der Heimkehr aus der Liste", not app.state.auftraege,
          str(app.state.auftraege))

    setze_truppen(app, kaempfer=30)
    app.state.noob_protection = False
    bot = main.BotPlayer("Testbot", "menschlich", 0.5, 0.5, army={"Bürgerwehr": 2})
    bot.noob_protection = False
    app.state.messages.clear()
    gestartet = app._attack(bot)
    check("_attack (Bot) startet einen Auftrag", bool(gestartet) and bool(app.state.auftraege),
          str(len(app.state.auftraege)))
    marsch_zu_ende(app)
    check("_attack erzeugt nach der Ankunft eine 'kampf'-Meldung",
          letzte_nachricht(app, "kampf").get("type") == "kampf")
    check("_attack protokolliert den Bot als Ziel 'Testbot'",
          any("Kampf am Ziel Testbot" in z for z in app.state.log), str(app.state.log[-1]))

    # ======================================================================
    # 11. NEU: kein Pfad ohne Marsch, keine doppelt verfuegbaren Truppen
    # ======================================================================

    abschnitt("11. Der Marsch ist Pflicht: Truppen sind unterwegs NICHT doppelt verfuegbar")

    setze_truppen(app, kaempfer=10)
    app.state.messages.clear()
    app.state.auftraege.clear()
    start = float(app.state.spielsekunden)
    erster = app._angriff_auftrag_starten("Ziel A", {})
    check("der erste Angriff startet", erster is True, repr(erster))
    eintrag = app.state.auftraege[-1] if app.state.auftraege else {}
    check("der Auftrag traegt eine Ankunft NACH dem Start",
          float(eintrag.get("ankunft") or 0) > start,
          f"start={start} ankunft={eintrag.get('ankunft')}")
    check("der Auftrag traegt eine Rueckkehr NACH der Ankunft",
          float(eintrag.get("rueckkehr") or 0) > float(eintrag.get("ankunft") or 0),
          f"ankunft={eintrag.get('ankunft')} rueckkehr={eintrag.get('rueckkehr')}")
    check("die Truppen stehen waehrend des Marsches nicht mehr im Lager",
          sum(u.count for u in app.state.units.values()) == 0,
          str({k: u.count for k, u in app.state.units.items() if u.count}))
    zweiter = app._angriff_auftrag_starten("Ziel B", {})
    check("ein zweiter Angriff mit denselben Truppen wird abgelehnt", zweiter is False,
          repr(zweiter))
    check("es laeuft genau EIN Auftrag", len(app.state.auftraege) == 1,
          str(len(app.state.auftraege)))
    marsch_zu_ende(app)
    check("nach der Heimkehr sind die Truppen wieder da",
          sum(u.count for u in app.state.units.values()) > 0,
          str({k: u.count for k, u in app.state.units.items() if u.count}))

finally:
    if root is not None:
        try:
            root.destroy()
        except Exception:
            pass

sys.exit(bericht())
