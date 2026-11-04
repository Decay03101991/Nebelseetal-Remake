"""GPT-B01: konservative Bot-Zielwahl nach den Wallregeln der Originalanleitung.

Keine eigenen Kampfwerte, keine Magieressourcen, keine Mutation. Der Bot greift nur
Orte an, deren belegte Wall-SK-Schwelle er aktuell erreichen kann. Er darf trotzdem
im eigentlichen Kampf verlieren: die Vorpruefung garantiert KEINEN Sieg.

Entwurfsregel (nicht Original): unter geeigneten Orten wird derjenige mit dem
niedrigsten Wall, dann den wenigsten stationierten Verteidigern, dann dem Namen
gewaehlt. Hermes kann diese Gewichtung spaeter ersetzen.
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional, Tuple

import einheiten
import gebaeude_wirkung
import spieldaten


def _anzahl(x):
    try:
        return max(0, int(x))
    except (ValueError, TypeError, OverflowError):
        return 0


def _stufe(x):
    try:
        return max(0, min(10, int(x)))
    except (TypeError, ValueError, OverflowError):
        return 0


def _zustand(x):
    try:
        return max(0.0, min(100.0, float(x)))
    except (TypeError, ValueError, OverflowError):
        return 100.0


def schlagkraft(truppen, geraete=None):
    """Summiert nur die Rollen, die das Original in der Vorrunde vorsieht.

    Fusstruppen = Nah- und Fernkampf (entspricht `kampf.FUSSTRUPPEN`).
    Belagerungs-SK nur von echten Belagerungswaffen, nicht von Karren.
    """
    fuss = 0
    bel = 0
    for inventar in (truppen or {}, geraete or {}):
        for name, menge in inventar.items():
            eintrag = einheiten.alle().get(name)
            if not eintrag:
                continue
            anzahl = _anzahl(menge)
            if eintrag['kategorie'] in ('Nahkampf', 'Fernkampf'):
                fuss += einheiten.schlagkraft(name) * anzahl
            elif eintrag['rolle'] == 'belagerung':
                bel += einheiten.schlagkraft(name) * anzahl
    return {'fusstruppen': fuss, 'belagerungswaffen': bel}


def pruefe_vorrunde(truppen, geraete, stufe, zustand=100.0):
    """Beurteilung der Wall-Vorrunde mit den ORIGINAL-Schwellen aus den Daten.

    Ausgabe 'moeglich' bezieht sich ausschliesslich auf die Vorrunde, nicht
    Kampf-/Siegwahrscheinlichkeit. Abgewehrte und wehrlose Truppen erhalten keine
    Gratisbeute und keinen Kassenabzug.
    """
    sk = schlagkraft(truppen, geraete)
    stufe = _stufe(stufe)
    faktor = _zustand(zustand) / 100.0
    schwelle = gebaeude_wirkung.wall_schwelle(stufe)
    fuss_noetig = float(schwelle['fusstruppen'] or 0) * faktor
    bel_noetig = (float(schwelle['belagerungswaffen']) * faktor
                  if schwelle['belagerungswaffen'] is not None else 0.0)
    gruende = []
    if not any(einheiten.alle().get(n, {}).get('kategorie') in ('Nahkampf', 'Fernkampf') and _anzahl(v) > 0
               for n, v in (truppen or {}).items()):
        gruende.append('Keine Fußkampftruppen vorhanden.')
    if sk['fusstruppen'] < fuss_noetig:
        gruende.append('Schlagkraft der Fußtruppen reicht für den Wall nicht.')
    if sk['belagerungswaffen'] < bel_noetig:
        gruende.append('Belagerungswaffen reichen für diese Wallstufe nicht.')
    return {'moeglich': not gruende, 'grund': ' '.join(gruende),
            'sk': sk, 'schwelle': {'fusstruppen': fuss_noetig,
                                'belagerungswaffen': bel_noetig}}


def waehle_ziel(orte, truppen, geraete, wallzustand):
    """Rueckgabe (Ort|None, Diagnose). `wallzustand(ort)` -> (Stufe, Zustand).

    Nicht geeignete Orte werden NICHT angegriffen. Strategische Auswahl unter
    moeglichen Zielen ist Vorschlag, Originalhandbuch hat keine Bot-Zielwahl.
    """
    machbare = []
    gesperrt = []
    for ort in (orte or []):
        stufe, zustand = wallzustand(ort)
        pruefung = pruefe_vorrunde(truppen, geraete, stufe, zustand)
        if pruefung['moeglich']:
            verteidiger = sum(_anzahl(v) for v in (getattr(ort, 'einheiten', {}) or {}).values())
            machbare.append((_stufe(stufe), verteidiger, str(getattr(ort, 'name', '')), ort))
        else:
            gesperrt.append((str(getattr(ort, 'name', '')), pruefung['grund']))
    if not machbare:
        return None, {'moeglich': False, 'gesperrt': gesperrt,
                      'grund': 'Kein mit der aktuellen Armee überwindbarer Dorfwall.'}
    machbare.sort(key=lambda entry: entry[:3])
    return machbare[0][3], {'moeglich': True, 'gesperrt': gesperrt,
                            'grund': 'Vorrunde erreichbar, Kampfausgang offen.'}


# ---------------------------------------------------------------------------------------------
# W-4 (Daniel 03.11.2026): Bot gegen Bot - ein starker Bot raubt ein Dorf eines ANDEREN Bots aus.
#
# Daniels Vorgabe, woertlich: Bots, die stark genug sind, "beginnen Raubzuege um Ressourcen - nicht
# nur gegen den Spieler, auch gegeneinander. Voraussetzung: Bot und seine Welt sind spielaktiv."
#
# Diese drei Funktionen sind die ZIELWAHL. Sie kaempfen NICHT und buchen nichts: der Kampf laeuft
# ueber denselben Weg wie beim Angriff auf den Spieler (`kampf.fuehre_schlacht`), und die Beute
# bucht `kampfbericht.beute_am_ziel` - EINE Formel, keine zweite. Gebucht wird im Aufrufer
# (`main.NebelseetalApp._bots_raubzug`), damit hier keine Buchungs- oder Anzeigelogik steckt.
#
# Alle Zahlen stehen in `data/bot_raubzug.json` (VORSCHLAG, NICHT BELEGT) - nicht im Code.
# ---------------------------------------------------------------------------------------------

def raubzug_einstellungen() -> Dict[str, Any]:
    """Die Regeln eines Raubzugs Bot gegen Bot aus `data/bot_raubzug.json` (W-4) - EINE Quelle.

    Fehlt die Datei oder ist sie kaputt, ist der Raubzug AUS (`aktiv: False`) - kein stiller
    Standardwert, keine erfundene Zahl.
    """
    pfad = os.path.join(spieldaten.projektwurzel(), 'data', 'bot_raubzug.json')   # feste Datendatei
    try:                                                                         # Datei lesen
        with open(pfad, encoding='utf-8') as f:                                  # UTF-8, wie alle Daten
            daten = json.load(f)                                                 # Inhalt als dict
    except (OSError, ValueError):                                                # fehlt oder kaputt
        return {'aktiv': False}                                                  # dann ist er AUS
    return daten if isinstance(daten, dict) else {'aktiv': False}                # nur ein dict gilt


def _welt_von(bot) -> int:
    """Die Welt, in der ein Bot STEHT - aus seinem Hauptdorf (W-1: das bleibt in seiner Welt).

    Rueckgabe 0 heisst 'keine Welt bekannt' (alter Spielstand ohne Doerfer). Dann wird nicht
    geraubt: ein Ziel ohne bekannte Welt waere geraten.
    """
    doerfer = list(getattr(bot, 'doerfer', None) or [])                          # Doerfer des Bots
    if not doerfer:                                                              # gar keine Doerfer
        return 0                                                                 # dann keine Welt
    haupt = next((d for d in doerfer if getattr(d, 'hauptdorf', False)), None)   # das Hauptdorf
    if haupt is not None:                                                        # Hauptdorf gefunden
        return _anzahl(getattr(haupt, 'dimension', 0))                           # Welt des Hauptdorfs
    return _anzahl(getattr(doerfer[0], 'dimension', 0))                          # sonst die des ersten


def raubziele(bot, bots, einstellungen: Optional[dict] = None) -> List[Dict[str, Any]]:
    """Die Doerfer ANDERER Bots in DERSELBEN Welt - die Kandidaten eines Raubzugs (W-4).

    Jeder Kandidat traegt, was die Wahl und der Bericht brauchen: `name`, `wall` (Stufe, Zustand),
    `besatzung` (Anzahl Einheiten vor Ort), `welt`, dazu die Objekte `dorf` und `bot`.

    Was hier NICHT passiert: pruefen, ob der Wall ueberwindbar ist (`waehle_raubziel`) oder ob der
    Bot ueberhaupt stark genug ist (das tut ebenfalls `waehle_raubziel`). Diese Funktion sammelt nur.
    """
    einstellungen = einstellungen if isinstance(einstellungen, dict) else raubzug_einstellungen()
    if not einstellungen.get('aktiv', False):                                     # Raubzug aus
        return []                                                                 # dann kein Ziel
    eigene_welt = _welt_von(bot)                                                 # Welt des Angreifers
    if eigene_welt <= 0:                                                         # Welt unbekannt
        return []                                                                 # dann kein Ziel
    try:                                                                         # Doerfer-Schwelle
        doerfer_schwelle = int(einstellungen.get('doerfer_schwelle') or 0)       # Zahl aus den Daten
    except (TypeError, ValueError):                                              # kaputter Wert
        doerfer_schwelle = 0                                                     # dann keine Schwelle
    eigene_doerfer = list(getattr(bot, 'doerfer', None) or [])                    # eigene Doerfer
    if len(eigene_doerfer) < max(1, doerfer_schwelle):                           # zu wenige eigene
        return []                                                                 # dann kein Raubzug
    kandidaten: List[Dict[str, Any]] = []                                        # Ergebnisliste
    for anderer in (bots or []):                                                 # jeder andere Bot
        if anderer is bot:                                                       # der Angreifer selbst
            continue                                                             # nie sein eigenes Ziel
        for dorf in list(getattr(anderer, 'doerfer', None) or []):               # jedes seiner Doerfer
            welt = _anzahl(getattr(dorf, 'dimension', 0))                        # Welt dieses Dorfes
            if bool(einstellungen.get('nur_eigene_welt', True)) and welt != eigene_welt:
                continue                                                         # fremde Welt = kein Ziel
            kandidaten.append({                                                  # Kandidat beschreiben
                'name': str(getattr(dorf, 'name', '') or ''),                    # Name des Dorfes
                'welt': welt,                                                    # Welt des Dorfes
                'wall': (_stufe(getattr(dorf, 'wall_stufe', 0)),                 # Wallstufe
                         _zustand(getattr(dorf, 'wall_zustand', 100.0))),        # Wallzustand
                'besatzung': sum(_anzahl(v) for v in                             # Einheiten vor Ort
                                 (getattr(dorf, 'einheiten', None) or {}).values()),
                'dorf': dorf,                                                    # das Dorf-Objekt
                'bot': anderer})                                                 # der Besitzer
    return kandidaten                                                            # alle Kandidaten


def waehle_raubziel(kandidaten, truppen, geraete,
                    einstellungen: Optional[dict] = None) -> Tuple[Optional[dict], Dict[str, Any]]:
    """Das SCHWAECHSTE erreichbare Bot-Dorf als Raubziel - Rueckgabe (Kandidat|None, Diagnose).

    Drei Bedingungen, jede mit den Zahlen aus `data/bot_raubzug.json`:
      * der Bot ist stark genug (`armee_schwelle`: so viele Kampfeinheiten muss er haben),
      * der Wall ist mit der Vorrunde ueberwindbar (`pruefe_vorrunde`, Original-Schwellen),
      * die eigene Schlagkraft ist `staerke_faktor` mal so gross wie die der Besatzung
        ('ein starker Bot greift einen schwaecheren Bot an').
    Rang wie in `waehle_ziel`: niedrigster Wall, dann wenigste Besatzung, dann Name. Kein Wurf.
    """
    einstellungen = einstellungen if isinstance(einstellungen, dict) else raubzug_einstellungen()
    kandidaten = list(kandidaten or [])                                          # Kopie, nie die Eingabe
    if not kandidaten:                                                           # kein Kandidat
        return None, {'moeglich': False, 'gesperrt': [], 'geprueft': 0,
                      'grund': 'Kein Dorf eines anderen Bots in dieser Welt.'}   # dann kein Ziel
    try:                                                                         # Armee-Schwelle
        schwelle = int(einstellungen.get('armee_schwelle') or 0)                 # Zahl aus den Daten
    except (TypeError, ValueError):                                              # kaputter Wert
        schwelle = 0                                                             # dann keine Schwelle
    anzahl = sum(_anzahl(v) for v in (truppen or {}).values())                    # eigene Kampfeinheiten
    if anzahl <= 0 or anzahl < max(1, schwelle):                                 # zu schwach oder leer
        return None, {'moeglich': False, 'gesperrt': [], 'geprueft': len(kandidaten),
                      'grund': 'Bot ohne (genug) Einheiten - kein Raubzug.'}     # dann kein Ziel
    try:                                                                         # Staerke-Faktor
        faktor = float(einstellungen.get('staerke_faktor') or 1.0)                # Zahl aus den Daten
    except (TypeError, ValueError):                                              # kaputter Wert
        faktor = 1.0                                                             # dann 1:1
    meine_sk = schlagkraft(truppen, geraete)['fusstruppen']                      # eigene Schlagkraft
    machbare, gesperrt = [], []                                                  # zwei Listen
    for kandidat in kandidaten:                                                  # jeder Kandidat
        stufe, zustand = kandidat['wall']                                        # Wall des Ziels
        pruefung = pruefe_vorrunde(truppen, geraete, stufe, zustand)             # Original-Vorrunde
        if not pruefung['moeglich']:                                             # Wall zu hoch
            gesperrt.append((kandidat['name'], pruefung['grund']))               # Grund merken
            continue                                                             # naechster Kandidat
        ihre_sk = schlagkraft(getattr(kandidat['dorf'], 'einheiten', None) or {})['fusstruppen']
        if meine_sk < faktor * ihre_sk:                                          # nicht stark genug
            gesperrt.append((kandidat['name'],                                   # Grund merken
                             'Besatzung zu stark: eigene Schlagkraft %d gegen nötig %d.'
                             % (int(meine_sk), int(faktor * ihre_sk))))
            continue                                                             # naechster Kandidat
        machbare.append((_stufe(stufe), _anzahl(kandidat['besatzung']),          # (Wall, Besatzung)
                         str(kandidat['name']), kandidat))                       # (Name, Kandidat)
    if not machbare:                                                             # nichts erreichbar
        return None, {'moeglich': False, 'gesperrt': gesperrt,                   # Diagnose
                      'geprueft': len(kandidaten),
                      'grund': 'Kein Bot-Dorf mit der aktuellen Armee überwindbar.'}
    machbare.sort(key=lambda entry: entry[:3])                                   # schwaechstes zuerst
    return machbare[0][3], {'moeglich': True, 'gesperrt': gesperrt,              # Ziel und Diagnose
                            'geprueft': len(kandidaten),
                            'grund': 'Vorrunde erreichbar, Kampfausgang offen.'}

