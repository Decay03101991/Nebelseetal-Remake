# -*- coding: ascii -*-
"""Messwerkzeug: Wirtschaft der Bots ueber echte Spieltage (S-8, 03.11.2026).

WOFUER
------
Die Bot-Wirtschaft haengt an mehreren Stellschrauben (Ertragsweg, Anlagenzahl, Gruendung). Wer eine
davon anfasst, muss ALLE Zahlen NEU messen - eine aus einer alten Sitzung abgeschriebene Zahl ist
ein geratener Wert. Dieses Werkzeug faehrt eine echte Partie (frische App, echte Bot-Takte) und
schreibt die Messwerte als JSON auf stdout, damit zwei Laeufe verglichen werden koennen.

WAS GEMESSEN WIRD
-----------------
Je Bot: Zahl der Doerfer, je Dorf Karte, Anlagen (Anzahl und Arten), Stundenertrag, Vorraete und die
Bevoelkerung. Dazu die Holzspur des Hauptdorfes je Spieltag (Wachstum, nicht nur Endstand).

WOHER DIE ZAHLEN KOMMEN
-----------------------
Alles aus dem laufenden Spiel: `GameState.bots_fortschreiben` (der EINE Bot-Takt), `main.bot_dorf_ertrag`
(die EINE Ertragslesestelle) und `main.bot_doerfer_sicherstellen`. Nichts wird gesetzt oder geschaetzt.

AUFRUF
------
    python -X utf8 tools/bot_wirtschaft_messung.py [--tage 24]
"""
from __future__ import annotations

import argparse  # Kommandozeile (Tage)
import json  # Ausgabeform
import os  # Pfade
import random  # reproduzierbarer Kartenaufbau
import sys  # Pfade und Rueckgabewert

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Projektwurzel
sys.path.insert(0, os.path.join(WURZEL, "src"))  # Spielmodule
sys.path.insert(0, os.path.join(WURZEL, "tests"))  # (nur fuer gleiche Importreihenfolge)
sys.path.insert(0, WURZEL)  # Projektwurzel (tools/)
for _p in ("src", "tools", "tests"):  # alle drei Modulordner
    _pfad = os.path.join(WURZEL, _p)  # Pfad dieses Ordners
    if _pfad not in sys.path:  # noch nicht eingetragen
        sys.path.insert(0, _pfad)  # dann jetzt

import tkinter as tk  # Spieloberflaeche (auch ohne Fenster startbar)

import main as M  # das Spiel


def _starter(seed: int = 7):
    """Frische App mit einer Spielersiedlung - derselbe Start wie im Spiel."""
    random.seed(seed)                                        # Karte und Startfeld reproduzierbar
    root = tk.Tk()                                           # Tk-Wurzel
    root.withdraw()                                          # unsichtbar (Messung, kein Fenster)
    app = M.NebelseetalApp(root)                             # die App
    app._build_main_ui()                                     # Oberflaeche aufbauen
    app._erste_siedlung_gruenden()                           # erste Siedlung, echte Startwerte
    return root, app                                         # Wurzel und App


def _dorp_stand(dorf, bot) -> dict:
    """Ein Bot-Dorf als Messzeile: Karte, Anlagen, Ertrag, Vorraete.

    Dazu die Angaben, an denen eine GRUENDUNG haengt (Karten, Siedlerkarren im Dorf, Bevoelkerung):
    ohne sie laesst sich ein Rueckgang der Dorfzahl nicht erklaeren, und Raten ist keine Messung.
    """
    ertrag = M.bot_dorf_ertrag(dorf, None, bot)              # EINE Ertragslesestelle
    arten: dict = {}                                         # Anlagen je Art
    for geb in (getattr(dorf, "bauten", None) or {}).values():  # jedes belegte Feld
        arten[str(geb)] = arten.get(str(geb), 0) + 1          # zaehlen
    karren = str((M.spieloekonomie.REGELN.get("gruendung") or {}).get("karren") or "")   # Karrenname des Kerns
    return {"name": str(dorf.name),                         # Dorfname
            "karte": str(getattr(dorf, "karte", "") or ""),   # Kartenkennung
            "anlagen": len(getattr(dorf, "bauten", None) or {}),   # belegte Felder
            "arten": dict(sorted(arten.items())),             # Anlagen je Art
            "ertrag": {k: round(float(v), 2) for k, v in sorted(ertrag.items())},  # je Stunde
            "vorraete": {k: round(float(v), 2)
                         for k, v in sorted((getattr(dorf, "vorraete", None) or {}).items())},  # Lager
            "karren": int((getattr(dorf, "einheiten", None) or {}).get(karren, 0) or 0),   # Siedlerkarren
            "siedler": round(float(getattr(dorf, "bevoelkerung", 0.0) or 0.0), 2)}  # Bevoelkerung


def messen(tage: int, weg: str = "") -> dict:
    """Eine Partie bis `tage` Spieltage fahren und je Bot den Stand festhalten.

    `weg` ueberschreibt den Ertragsweg (`data/bot_wirtschaft.json: ertrag_weg`), damit zwei Wege
    unter SONST gleichen Bedingungen verglichen werden koennen, ohne die Datendatei anzufassen.
    """
    if weg:                                                  # Vergleichslauf gewuenscht
        _original = M.bot_wirtschaft_einstellungen           # echte Lesefunktion merken

        def _mit_weg(*_args, **_kwargs):                     # Huelle mit festem Ertragsweg
            daten = dict(_original())                        # Einstellungen wie immer lesen
            daten["ertrag_weg"] = str(weg)                   # nur diesen einen Wert ersetzen
            return daten                                     # fertig

        M.bot_wirtschaft_einstellungen = _mit_weg            # fuer diese Messung umhaengen
    root, app = _starter()                                   # Partie starten
    try:
        gs = app.state                                       # Spielstand
        schritt = 3600.0 * 6                                 # ein Bot-Takt alle sechs Spielstunden
        zeit = 0.0                                           # Spielzeit
        ende = 86400.0 * float(tage)                         # Zielzeit
        holzspur: dict = {}                                  # Holz des Hauptdorfes je Spieltag
        dorfspur: dict = {}                                  # Dorfzahl je Bot und Spieltag
        while zeit <= ende:                                  # bis zum Ziel
            zeit += schritt                                  # naechster Takt
            gs.bots_fortschreiben(zeit)                      # der EINE Bot-Takt
            if abs(zeit % 86400.0) < 1e-6:                   # Tagesgrenze erreicht
                for bot in gs.bots:                          # je Bot
                    doerfer = M.bot_doerfer_sicherstellen(bot)   # seine Doerfer
                    dorfspur.setdefault(bot.name, []).append(
                        [int(zeit // 86400.0), len(doerfer)])    # Dorfzahl dieses Tages
                    if doerfer:                              # Hauptdorf vorhanden
                        holz = float((doerfer[0].vorraete or {}).get("holz", 0.0))  # Holzstand
                        holzspur.setdefault(bot.name, []).append(
                            [int(zeit // 86400.0), round(holz, 2)])   # Tageswert merken
        bericht = {"tage": int(tage), "bots": [], "holzspur": holzspur, "dorfspur": dorfspur}   # Ergebnis
        for bot in gs.bots:                                  # je Bot der Endstand
            doerfer = M.bot_doerfer_sicherstellen(bot)       # seine Doerfer
            bericht["bots"].append({
                "bot": str(bot.name),                        # Name
                "taktik": str(getattr(bot, "taktik", "") or ""),   # Taktik
                "doerfer": len(doerfer),                     # Zahl der Doerfer
                "forschung": M.bot_forschungsstaende(bot),   # Wissensstand (Wagenbau fuer die Gruendung)
                "gedaechtnis": {k: v for k, v in (getattr(bot, "gedaechtnis", None) or {}).items()
                                if isinstance(v, (int, float, str))},   # Gruendungssperre usw.
                "kasse": {k: round(float(v), 2)
                          for k, v in sorted(M.bot_kasse(bot).items())},   # Gesamtkasse
                "dorfstaende": [_dorp_stand(d, bot) for d in doerfer]})     # je Dorf
        return bericht                                       # fertig
    finally:
        root.destroy()                                       # Fenster wieder schliessen


def main_lauf() -> int:
    """Kommandozeile: Tage lesen, messen, JSON ausgeben.

    Mit `--aus <datei>` geht das JSON in eine DATEI: die App schreibt ihre Meldungen nach stdout
    (Karte, Gruendung, ...), sonst stuende Spieltext mitten in den Messwerten (belegt 03.11.2026).
    """
    parser = argparse.ArgumentParser(description="Bot-Wirtschaft ueber echte Spieltage messen")
    parser.add_argument("--tage", type=int, default=24, help="Spieltage (Vorgabe 24)")
    parser.add_argument("--aus", default="", help="Zieldatei fuer das JSON (leer = stdout)")
    parser.add_argument("--weg", default="", help="Ertragsweg ueberschreiben: anlagen, karte, felder")
    args = parser.parse_args()                               # Argumente
    text = json.dumps(messen(args.tage, args.weg), ensure_ascii=False, indent=1)   # Messwerte als JSON
    if args.aus:                                             # Datei gewuenscht
        with open(args.aus, "w", encoding="utf-8", newline="\n") as datei:
            datei.write(text)                                # dann dorthin schreiben
        print("MESSUNG: %d Spieltage -> %s" % (args.tage, args.aus))   # kurze Quittung
    else:                                                    # ohne Datei
        print(text)                                          # auf stdout
    return 0                                                 # Erfolg


if __name__ == "__main__":
    raise SystemExit(main_lauf())
