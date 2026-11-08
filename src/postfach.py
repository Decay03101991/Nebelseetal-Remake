# -*- coding: ascii -*-
"""Postfach: Fristen, Archiv, Blaettern und Ruhm-Rang - die EINE Rechenstelle (S1, 06.11.2026).

Warum ein eigenes Fachmodul: die Ansicht `_render_messages` zeigt bisher nur die letzten 20
Nachrichten (`main.py`), aeltere sind im Spielstand vorhanden, aber unerreichbar; es gibt keinen
Filter, kein Archiv und keinen Ablauf. Alles davon ist reine Rechnung ueber die Nachrichtenliste
und darum ohne Fenster pruefbar (Muster `spionage.py`/`story.py`).

Regeln, die hier gelten:
  * Fristen, Kategorien und Seitengroesse stehen in `data/nachrichten.json` - NICHTS davon im Code.
  * Alte Spielstaende laden ohne Migration: jedes Feld wird mit `.get` und Standardwert gelesen,
    geschrieben wird nur, was der Spieler wirklich tut (gelesen, archiviert).
  * Militaerberichte (`kampf`, `gesamtsieg`) laufen NIE ab; ungelesene Verlustberichte verschieben
    ihre Frist, statt zu verschwinden (Daniel, Entscheidung 4).
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, Iterable, List, Tuple

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PFAD_NACHRICHTEN = os.path.join(WURZEL, "data", "nachrichten.json")
PFAD_RUHM = os.path.join(WURZEL, "data", "ruhm.json")

# Rueckfall, falls eine Datendatei fehlt: die Werte sind DANN nicht belegt und werden als
# leerer Satz behandelt - das Modul wirft nie, damit ein kaputtes Datenverzeichnis das Spiel
# nicht an der Nachrichtenansicht scheitern laesst.
_LEER_NACHRICHTEN: Dict[str, Any] = {
    "je_seite": 20, "frist_spielsekunden": 0, "ohne_ablauf": ["kampf", "gesamtsieg"],
    "verschieben_wenn_ungelesen": ["verlust", "diebstahl"], "kategorien": {"alle": "Alle"},
    "kategorie_je_typ": {},
}
_LEER_RUHM: Dict[str, Any] = {"kennzahl": "gesamtpunkte", "stufen": [], "balken": {}}


def _laden(pfad: str, leer: Dict[str, Any]) -> Dict[str, Any]:
    """Liest eine JSON-Datei; fehlt sie oder ist sie kaputt, kommt der leere Satz zurueck."""
    try:
        with open(pfad, encoding="utf-8") as f:
            daten = json.load(f)
    except (OSError, ValueError):
        return dict(leer)
    return daten if isinstance(daten, dict) else dict(leer)


def einstellungen() -> Dict[str, Any]:
    """Die Postfach-Regeln aus `data/nachrichten.json` (je Aufruf gelesen, damit Aenderungen wirken)."""
    daten = _laden(PFAD_NACHRICHTEN, _LEER_NACHRICHTEN)
    ergaenzt = dict(_LEER_NACHRICHTEN)
    ergaenzt.update(daten)
    return ergaenzt


def ruhm_daten() -> Dict[str, Any]:
    """Die Ruhm-Stufen aus `data/ruhm.json` (VORSCHLAG, siehe Datei-Kopf)."""
    daten = _laden(PFAD_RUHM, _LEER_RUHM)
    ergaenzt = dict(_LEER_RUHM)
    ergaenzt.update(daten)
    return ergaenzt


def _typ(nachricht: Any) -> str:
    """Der Typ einer Nachricht als kleiner Text, nie None."""
    return str((nachricht or {}).get("type") or "").strip().lower()


def _als_zahl(wert: Any, standard: float = 0.0) -> float:
    """Zahl aus einem beliebigen Feld, ohne Ausnahme (alte Spielstaende haben Text statt Zahl)."""
    try:
        zahl = float(wert)
    except (TypeError, ValueError):
        return standard
    return zahl if zahl == zahl and abs(zahl) != float("inf") else standard


def normalisiert(nachricht: Any) -> Dict[str, Any]:
    """Die drei neuen Felder einer Nachricht, ohne den Spielstand zu veraendern.

    Ein alter Spielstand kennt `read`, `archived` und `ablauf_am` nicht - hier bekommen sie
    Standardwerte (ungelesen, nicht archiviert, kein Ablauf), damit Anzeige und Ablauf rechnen
    koennen, ohne die Liste umzuschreiben.
    """
    n = nachricht if isinstance(nachricht, dict) else {}
    return {
        "read": bool(n.get("read", False)),
        "archived": bool(n.get("archived", False)),
        "ablauf_am": (None if n.get("ablauf_am") in (None, "") else _als_zahl(n.get("ablauf_am"), 0.0)),
    }


def ist_gelesen(nachricht: Any) -> bool:
    """Ist die Nachricht gelesen? (Feld `read`, Standard ungelesen.)"""
    return normalisiert(nachricht)["read"]


def ist_archiviert(nachricht: Any) -> bool:
    """Liegt die Nachricht im Archiv? (Feld `archived`, Standard nein.)"""
    return normalisiert(nachricht)["archived"]


def als_gelesen(nachricht: Any) -> None:
    """Markiert eine Nachricht im Spielstand als gelesen (aendert genau dieses dict)."""
    if isinstance(nachricht, dict):
        nachricht["read"] = True


def archivieren(nachricht: Any, wert: bool = True) -> None:
    """Legt eine Nachricht ins Archiv oder holt sie zurueck."""
    if isinstance(nachricht, dict):
        nachricht["archived"] = bool(wert)


def kategorie(nachricht: Any) -> str:
    """Die Kategorie einer Nachricht aus der Zuordnung in den Daten (Standard: ihr Typ)."""
    typ = _typ(nachricht)
    zuordnung = einstellungen().get("kategorie_je_typ") or {}
    return str(zuordnung.get(typ) or typ or "system")


def frist_am(nachricht: Any) -> float:
    """Der Ablaufzeitpunkt einer Nachricht in Spielsekunden (0.0 = laeuft nie ab)."""
    daten = einstellungen()
    typ = _typ(nachricht)
    if typ in {str(t).lower() for t in (daten.get("ohne_ablauf") or [])}:
        return 0.0
    bekannt = normalisiert(nachricht)["ablauf_am"]
    if bekannt:
        return bekannt
    roh = (nachricht or {}).get("spielzeit_sekunden")
    if roh in (None, ""):
        return 0.0                                               # kein Stempel: keine Frist behaupten
    gestempelt = _als_zahl(roh, -1.0)
    frist = _als_zahl(daten.get("frist_spielsekunden"), 0.0)      # 0 = keine Frist bekannt = laeuft nie ab
    if gestempelt < 0 or frist <= 0:
        return 0.0
    return gestempelt + frist                                    # Stempel 0 ist der Spielbeginn und zaehlt


def ablauf_buchen(nachrichten: List[Any], jetzt: float) -> Dict[str, int]:
    """Laesst abgelaufene Nachrichten verschwinden - und verschiebt ungelesene Verlustberichte.

    Rueckgabe::  {"entfernt": int, "verschoben": int}
    Die Frist greift GENAU EINMAL: entfernte Nachrichten stehen danach nicht mehr in der Liste,
    ein zweiter Aufruf zaehlt also nichts mehr. Militaerberichte und Nachrichten ohne Stempel
    bleiben unberuehrt.
    """
    daten = einstellungen()
    verschieben = {str(t).lower() for t in (daten.get("verschieben_wenn_ungelesen") or [])}
    frist = _als_zahl(daten.get("frist_spielsekunden"), 0.0)
    entfernt, verschoben, behalten = 0, 0, []
    for nachricht in nachrichten or []:
        ablauf = frist_am(nachricht)
        if not ablauf or _als_zahl(jetzt, 0.0) < ablauf:
            behalten.append(nachricht)                       # laeuft nicht ab oder noch nicht faellig
            continue
        if _typ(nachricht) in verschieben and not ist_gelesen(nachricht):
            if isinstance(nachricht, dict):
                nachricht["ablauf_am"] = _als_zahl(jetzt, 0.0) + frist   # Frist neu setzen, nichts verlieren
            behalten.append(nachricht)
            verschoben += 1
            continue
        entfernt += 1                                        # abgelaufen: raus aus dem Postfach
    if isinstance(nachrichten, list):
        nachrichten[:] = behalten                            # an Ort und Stelle ersetzen (Liste bleibt dieselbe)
    return {"entfernt": entfernt, "verschoben": verschoben}


def sichtbar(nachrichten: Iterable[Any], filter_key: str = "alle") -> List[Any]:
    """Die Nachrichten einer Filterzeile - neueste zuerst.

    Filter: `alle` (alles ausser Archiv), `ungelesen`, `archiv` (nur das Archiv) oder eine
    Kategorie aus `data/nachrichten.json` (`kampf`, `spionage`, `handel`, ...).
    """
    schluessel = str(filter_key or "alle").strip().lower()
    treffer = []
    for nachricht in nachrichten or []:
        archiviert = ist_archiviert(nachricht)
        if schluessel == "archiv":
            if archiviert:
                treffer.append(nachricht)
            continue
        if archiviert:
            continue                                         # Archiv nur unter dem eigenen Filter
        if schluessel == "alle":
            treffer.append(nachricht)
        elif schluessel == "ungelesen":
            if not ist_gelesen(nachricht):
                treffer.append(nachricht)
        elif kategorie(nachricht) == schluessel or _typ(nachricht) == schluessel:
            treffer.append(nachricht)
    treffer.reverse()                                        # neueste zuerst
    return treffer


def seiten_anzahl(nachrichten: Iterable[Any], je_seite: int = 0) -> int:
    """Wie viele Seiten es fuer diese Liste gibt (mindestens eine, auch bei leerer Liste)."""
    grenze = je_seite or int(einstellungen().get("je_seite") or 20)
    anzahl = len(list(nachrichten or []))
    return max(1, (anzahl + grenze - 1) // grenze)


def seite(nachrichten: Iterable[Any], nummer: int = 1, je_seite: int = 0) -> List[Any]:
    """Die Nachrichten EINER Seite; die Seitennummer wird auf den gueltigen Bereich gezogen."""
    liste = list(nachrichten or [])
    grenze = je_seite or int(einstellungen().get("je_seite") or 20)
    gesamt = seiten_anzahl(liste, grenze)
    seite_nr = min(max(1, int(nummer or 1)), gesamt)
    anfang = (seite_nr - 1) * grenze
    return liste[anfang:anfang + grenze]


def ungelesen_anzahl(nachrichten: Iterable[Any]) -> int:
    """Wie viele Nachrichten ungelesen sind (Zahl an der Filterzeile)."""
    return sum(1 for n in (nachrichten or []) if not ist_gelesen(n))


def rang(punkte_wert: Any) -> Dict[str, Any]:
    """Der Ruhm-Rang zu einem Punktestand (Stufen aus `data/ruhm.json`).

    Rueckgabe:: {"stufe", "name", "ab", "naechste_ab", "naechster_name", "fortschritt"}
    `fortschritt` ist der Anteil 0..1 bis zur naechsten Stufe; auf der hoechsten Stufe 1.0.
    Ohne Stufen in der Datei bleibt alles leer - es wird KEINE Schwelle erfunden.
    """
    daten = ruhm_daten()
    stufen = sorted(daten.get("stufen") or [], key=lambda s: _als_zahl(s.get("ab"), 0.0))
    wert = _als_zahl(punkte_wert, 0.0)
    ergebnis = {"stufe": 0, "name": "", "ab": 0.0, "naechste_ab": None,
                "naechster_name": "", "fortschritt": 0.0, "punkte": wert}
    if not stufen:
        return ergebnis
    erreicht = [s for s in stufen if wert >= _als_zahl(s.get("ab"), 0.0)]
    aktuell = erreicht[-1] if erreicht else stufen[0]
    ergebnis.update({"stufe": int(_als_zahl(aktuell.get("stufe"), 0)), "name": str(aktuell.get("name") or ""),
                     "ab": _als_zahl(aktuell.get("ab"), 0.0)})
    spaeter = [s for s in stufen if _als_zahl(s.get("ab"), 0.0) > wert]
    if not spaeter:
        ergebnis["fortschritt"] = 1.0                        # hoechste Stufe erreicht
        return ergebnis
    naechste = spaeter[0]
    unten = ergebnis["ab"]
    oben = _als_zahl(naechste.get("ab"), 0.0)
    ergebnis["naechste_ab"] = oben
    ergebnis["naechster_name"] = str(naechste.get("name") or "")
    if oben > unten:
        ergebnis["fortschritt"] = max(0.0, min(1.0, (wert - unten) / (oben - unten)))
    return ergebnis


def rang_text(punkte_wert: Any) -> str:
    """Ein Satz fuer die Anzeige: Rang, Punkte und Abstand zur naechsten Stufe."""
    info = rang(punkte_wert)
    if not info["name"]:
        return ""                                            # keine Stufen in den Daten: nichts behaupten
    if info["naechste_ab"] is None:
        # Anzeigetext mit ECHTEM Umlaut (Escape, damit die Datei ASCII bleibt - Wache test_anzeigetexte_umlaute)
        return "%s - h\u00f6chste Stufe erreicht (%d Punkte)." % (info["name"], int(info["punkte"]))
    fehlt = max(0, int(round(info["naechste_ab"] - info["punkte"])))
    return "%s - %d Punkte, noch %d bis %s." % (info["name"], int(info["punkte"]), fehlt,
                                                info["naechster_name"])
