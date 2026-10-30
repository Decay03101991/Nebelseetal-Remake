"""
Pruefung des Passworttors (Schritt 8 in `docs/WEG_ZUR_EXE.md`).

Zwei Ebenen:
  1. **Rechenlogik** (`src/tor.py`) — fensterlos: Passwort setzen, pruefen, Fehlversuche mit
     Wartezeit, Aendern, Zuruecksetzen. Dabei wird geprueft, dass das Passwort **nirgends im
     Klartext** liegt und dass zwei gleiche Passwoerter verschiedene Pruefwerte ergeben (Salz).
  2. **Tor im Fenster** (`NebelseetalApp`) — Erststart zeigt "Passwort festlegen", danach
     verlangt es das Passwort; falsches Passwort oeffnet das Spiel **nicht**.

Alle Pruefungen laufen in einem eigenen Ordner (kein Zugriff auf Daniels echtes Tor).

Aufruf:  python tests/test_tor.py
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, ausnahme, befund, bericht, check, import_src

ROOT, SRC = import_src()
import tor as T
import main as M


_tempordner = []


def neuer_pfad(name: str) -> str:
    """Ein frischer Tor-Pfad in einem eigenen Ordner (nie Daniels echter).

    Der Ordner wird am Ende der Pruefung wieder entfernt — sonst bleiben bei jedem Lauf
    Karteileichen im Zwischenspeicher liegen (im Projekt gilt: nach jedem Lauf aufraeumen).
    """
    ordner = tempfile.mkdtemp(prefix="nebel_tor_")
    _tempordner.append(ordner)
    return os.path.join(ordner, name)


# ==========================================================================
# 1. Rechenlogik
# ==========================================================================

abschnitt("Passworttor — Regeln fuer ein neues Passwort")

ok, meldung = T.passwort_pruefen_regeln("", "")
check("leeres Passwort wird abgelehnt", ok is False and "leer" in meldung, meldung)
ok, meldung = T.passwort_pruefen_regeln("ab", "ab")
check("zu kurzes Passwort wird abgelehnt", ok is False and "mindestens" in meldung, meldung)
ok, meldung = T.passwort_pruefen_regeln("geheim", "geheim2")
check("zwei verschiedene Eingaben werden abgelehnt", ok is False and "überein" in meldung, meldung)
ok, meldung = T.passwort_pruefen_regeln("geheim", "geheim")
check("ein gueltiges Passwort wird angenommen", ok is True, meldung)
check("die Mindestlaenge ist als Zahl bekannt", isinstance(T.MIN_LAENGE, int) and T.MIN_LAENGE >= 4,
      str(T.MIN_LAENGE))

abschnitt("Passworttor — Erststart, Setzen und Pruefen")

pfad = neuer_pfad("tor.json")
check("ohne Datei ist kein Passwort gesetzt", T.hat_passwort(pfad) is False)
ok, meldung = T.pruefe_passwort("egal", pfad)
check("ohne gesetztes Passwort gibt es keinen Zugang", ok is False and "kein Passwort" in meldung,
      meldung)

ok, meldung = T.setze_passwort("nurimkopf", "stimmt-nicht", pfad)
check("Setzen mit falscher Wiederholung scheitert", ok is False)
check("und es entsteht keine Tor-Datei", not os.path.exists(pfad))

ok, meldung = T.setze_passwort("nurimkopf", "nurimkopf", pfad)
check("Setzen mit gleicher Wiederholung gelingt", ok is True, meldung)
check("die Tor-Datei liegt danach auf der Platte", os.path.exists(pfad), pfad)
check("jetzt ist ein Passwort gesetzt", T.hat_passwort(pfad) is True)

_rohdaten = open(pfad, encoding="utf-8").read()
check("das Passwort steht NICHT im Klartext in der Datei", "nurimkopf" not in _rohdaten)
_daten = json.loads(_rohdaten)
check("die Datei nennt Verfahren und Rundenzahl",
      "PBKDF2" in str(_daten.get("verfahren")) and _daten.get("runden") == T.RUNDEN,
      f"{_daten.get('verfahren')} / {_daten.get('runden')}")
check("die Datei enthaelt Salz und Pruefwert in Hex",
      len(_daten.get("salz", "")) == 2 * T.SALZ_BYTES
      and all(c in "0123456789abcdef" for c in _daten.get("pruefwert", "")),
      f"Salz {len(_daten.get('salz', ''))} Zeichen, Pruefwert {len(_daten.get('pruefwert', ''))}")
check("der Hinweis auf den Notausgang steht in der Datei", "Hinweis" in _rohdaten or "hinweis" in _daten)
check("das Datum des Setzens ist vermerkt", bool(_daten.get("gesetzt")), str(_daten.get("gesetzt")))

ok, meldung = T.pruefe_passwort("nurimkopf", pfad)
check("das richtige Passwort oeffnet das Tor", ok is True, meldung)
ok, meldung = T.pruefe_passwort("falsch", pfad)
check("ein falsches Passwort wird abgelehnt", ok is False and "Falsches Passwort" in meldung, meldung)

abschnitt("Passworttor — Salz: gleiches Passwort, anderer Pruefwert")

pfad2 = neuer_pfad("tor2.json")
T.setze_passwort("nurimkopf", "nurimkopf", pfad2)
_a = json.loads(open(pfad, encoding="utf-8").read())
_b = json.loads(open(pfad2, encoding="utf-8").read())
check("dasselbe Passwort ergibt zwei verschiedene Pruefwerte",
      _a["pruefwert"] != _b["pruefwert"])
check("und zwei verschiedene Salze", _a["salz"] != _b["salz"])
check("trotzdem oeffnen beide dasselbe Passwort",
      T.pruefe_passwort("nurimkopf", pfad)[0] and T.pruefe_passwort("nurimkopf", pfad2)[0])

abschnitt("Passworttor — Fehlversuche und Wartezeit")

check("ohne Fehlversuche gibt es keine Wartezeit", T.wartezeit_sekunden(0) == 0)
check("ein und zwei Fehlversuche sind noch frei",
      T.wartezeit_sekunden(1) == 0 and T.wartezeit_sekunden(2) == 0)
check("nach drei Fehlversuchen wird gewartet (5 s)", T.wartezeit_sekunden(3) == 5,
      str(T.wartezeit_sekunden(3)))
check("die Wartezeit waechst (nach sechs Versuchen 15 s)", T.wartezeit_sekunden(6) == 15)
check("und ist nach oben gedeckelt (60 s)", T.wartezeit_sekunden(99) == 60)

pfad3 = neuer_pfad("tor3.json")
T.setze_passwort("nurimkopf", "nurimkopf", pfad3)
T.pruefe_passwort("falsch", pfad3)
T.pruefe_passwort("falsch", pfad3)
check("zwei Fehlversuche sind gezaehlt", T.fehlversuche(pfad3) == 2, str(T.fehlversuche(pfad3)))
ok, _ = T.pruefe_passwort("nurimkopf", pfad3)
check("das richtige Passwort setzt den Zaehler zurueck",
      ok is True and T.fehlversuche(pfad3) == 0, str(T.fehlversuche(pfad3)))

# Drei Fehler hintereinander -> Wartezeit, danach das richtige Passwort erst spaeter
T.pruefe_passwort("falsch", pfad3)
T.pruefe_passwort("falsch", pfad3)
T.pruefe_passwort("falsch", pfad3)
check("nach drei Fehlversuchen ist das Tor gesperrt", T.restwartezeit(pfad3) > 0,
      f"{T.restwartezeit(pfad3):.1f} s")
ok, meldung = T.pruefe_passwort("nurimkopf", pfad3)
check("auch das RICHTIGE Passwort wartet die Sperre ab", ok is False and "warten" in meldung, meldung)

# Zeit vorstellen: nach Ablauf der Sperre oeffnet das richtige Passwort wieder
import time as _zeit
ok, meldung = T.pruefe_passwort("nurimkopf", pfad3, jetzt=_zeit.time() + 3600)
check("nach Ablauf der Wartezeit oeffnet das richtige Passwort", ok is True, meldung)
check("und die Sperre ist danach aufgehoben", T.restwartezeit(pfad3) == 0.0)

abschnitt("Passworttor — Aendern und Zuruecksetzen")

ok, meldung = T.aendere_passwort("falschalt", "neu1234", "neu1234", pfad)
check("Aendern mit falschem alten Passwort scheitert", ok is False and "alte Passwort" in meldung, meldung)
ok, meldung = T.aendere_passwort("nurimkopf", "neu1234", "neu1234", pfad)
check("Aendern mit richtigem alten Passwort gelingt", ok is True, meldung)
check("das alte Passwort oeffnet danach nicht mehr", T.pruefe_passwort("nurimkopf", pfad)[0] is False)
check("das neue Passwort oeffnet", T.pruefe_passwort("neu1234", pfad)[0] is True)

ohne = neuer_pfad("gibtsnicht.json")
ok, meldung = T.aendere_passwort("a", "b", "b", ohne)
check("Aendern ohne gesetztes Passwort wird abgelehnt", ok is False, meldung)
ok, meldung = T.zuruecksetzen(ohne)
check("Zuruecksetzen ohne Datei wird ehrlich gemeldet", ok is False and "keine Tor-Datei" in meldung,
      meldung)

ok, meldung = T.zuruecksetzen(pfad)
check("Zuruecksetzen loescht die Tor-Datei", ok is True and not os.path.exists(pfad), meldung)
check("und das Spiel verlangt danach ein neues Passwort", T.hat_passwort(pfad) is False)
ok, meldung = T.setze_passwort("wiederdanach", "wiederdanach", pfad)
check("ein neues Passwort laesst sich danach setzen", ok is True, meldung)

abschnitt("Passworttor — der Bericht enthaelt kein Passwort")

_bericht = T.uebersicht(pfad)
check("der Bericht nennt den Pfad und den Stand",
      _bericht["gesetzt"] is True and _bericht["pfad"] == pfad, str(_bericht))
check("der Bericht enthaelt KEIN Passwort", "wiederdanach" not in json.dumps(_bericht))
check("das Tor liegt ausserhalb des Projektordners",
      not os.path.abspath(T.STANDARD_PFAD).lower().startswith(os.path.abspath(ROOT).lower()),
      T.STANDARD_PFAD)


# ==========================================================================
# 2. Das Tor im Fenster
# ==========================================================================

abschnitt("Passworttor im Fenster — Erststart legt fest, danach wird gefragt")

tk = ausnahme("tkinter laden", lambda: __import__("tkinter"))


def _knoepfe(widget):
    treffer = []
    for kind in widget.winfo_children():
        if isinstance(kind, tk.Button):
            treffer.append(str(kind.cget("text")))
        treffer += _knoepfe(kind)
    return treffer


def _texte(widget):
    treffer = []
    for kind in widget.winfo_children():
        if isinstance(kind, tk.Label):
            treffer.append(str(kind.cget("text")))
        treffer += _texte(kind)
    return treffer


def fenster_probe():
    pfad = neuer_pfad("tor_fenster.json")
    root = tk.Tk()
    root.withdraw()
    try:
        app = M.NebelseetalApp(root, tor_pfad=pfad)
        root.update_idletasks()
        check("der Erststart zeigt das Fenster 'Passwort festlegen'",
              any("festlegen" in t for t in _knoepfe(root)), str(_knoepfe(root)))
        check("das Spiel startet ohne Passwort NICHT",
              not hasattr(app, "menu_buttons"), "Menü wäre schon aufgebaut")

        # zu kurzes Passwort -> Fehlermeldung, kein Weiterkommen
        app.tor_neu1.insert(0, "ab")
        app.tor_neu2.insert(0, "ab")
        app._tor_setzen()
        root.update_idletasks()
        check("ein zu kurzes Passwort wird im Fenster gemeldet",
              "mindestens" in str(app.tor_meldung.cget("text")), str(app.tor_meldung.cget("text")))
        check("und es ist immer noch kein Passwort gesetzt", not T.hat_passwort(pfad))

        # gueltiges Passwort -> Tor eingerichtet, Tor-Datei entsteht
        app.tor_neu1.delete(0, tk.END)
        app.tor_neu2.delete(0, tk.END)
        app.tor_neu1.insert(0, "ganzgeheim")
        app.tor_neu2.insert(0, "ganzgeheim")
        app._tor_setzen()
        root.update_idletasks()
        check("das gueltige Passwort richtet das Tor ein", T.hat_passwort(pfad))
        check("die Meldung bestaetigt es", "gesetzt" in str(app.tor_meldung.cget("text")).lower(),
              str(app.tor_meldung.cget("text")))
    finally:
        root.destroy()

    # Zweiter Start: Tor verlangt das Passwort
    root = tk.Tk()
    root.withdraw()
    try:
        app2 = M.NebelseetalApp(root, tor_pfad=pfad)
        root.update_idletasks()
        check("der zweite Start fragt nach dem Passwort",
              any("Spiel starten" in t for t in _knoepfe(root)), str(_knoepfe(root)))
        check("und nennt den Notausgang (Datei loeschen)", any("Notausgang" in t for t in _texte(root)),
              str([t[:40] for t in _texte(root)]))

        app2.tor_eingabe.insert(0, "verkehrt")
        app2._tor_pruefen()
        root.update_idletasks()
        check("ein falsches Passwort oeffnet das Spiel nicht",
              not hasattr(app2, "menu_buttons"), "Menü wäre schon aufgebaut")
        check("und wird im Fenster gemeldet",
              "Falsches Passwort" in str(app2.tor_meldung.cget("text")),
              str(app2.tor_meldung.cget("text")))

        app2.tor_eingabe.insert(0, "ganzgeheim")
        app2._tor_pruefen()
        root.update_idletasks()
        check("das richtige Passwort meldet den Zugang",
              "Zugang" in str(app2.tor_meldung.cget("text")), str(app2.tor_meldung.cget("text")))
        check("der Weiterlauf ist angestossen (Ladeansicht kommt per after)",
              "Passworttor geoeffnet" in " ".join(app2.state.log)
              or any("Passworttor" in z for z in app2.state.log), str(app2.state.log[-2:]))
        return True
    finally:
        root.destroy()


def app_probe_mit_tor():
    """Das Spiel hinter dem Tor muss unveraendert arbeiten (Hauptfenster baut sich auf)."""
    pfad = neuer_pfad("tor_app.json")
    T.setze_passwort("hinterdemtor", "hinterdemtor", pfad)
    root = tk.Tk()
    root.withdraw()
    try:
        app = M.NebelseetalApp(root, tor_pfad=pfad)
        app._build_main_ui()
        root.update()
        # 30.10.2026: Die Menueleiste ist seit Daniels Vorgabe DYNAMISCH - sie zeigt nur, was
        # freigeschaltet ist (Forschung erst ab Bibliothek, Kaserne erst ab Kriegerakademie).
        # Die Wache vergleicht deshalb gegen DIESELBE Quelle (`menu_sichtbar`) statt gegen eine
        # feste 17. Die Zusage bleibt: nach dem Tor steht die fertige Leiste.
        check("nach dem Tor baut sich das Hauptfenster auf (Menueleiste vollstaendig)",
              list(getattr(app, "menu_buttons", {})) == M.menu_fuer_ebene(
                  app.state.settlements, app.ebene),
              f"{len(getattr(app, 'menu_buttons', {}))} Knoepfe: {sorted(getattr(app, 'menu_buttons', {}))}")
        check("die Statuszeile ist vorhanden und gefüllt",
              bool(app.lbl_status.cget("text")) and app.lbl_status.winfo_reqheight() > 12,
              f"'{app.lbl_status.cget('text')[:30]}' / {app.lbl_status.winfo_reqheight()} px")
        return True
    finally:
        root.destroy()


if tk is not None:
    check("Tor-Fenster laeuft durch", bool(ausnahme("Tor im Fenster", fenster_probe)))
    check("Hauptfenster hinter dem Tor laeuft durch", bool(ausnahme("Hauptfenster", app_probe_mit_tor)))
else:
    befund("Fensterpruefung übersprungen", "kein tkinter verfügbar")

for _ordner in _tempordner:                    # eigene Zwischenordner wieder wegraeumen
    shutil.rmtree(_ordner, ignore_errors=True)

sys.exit(bericht())
