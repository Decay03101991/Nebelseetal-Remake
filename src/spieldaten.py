"""
Nebelseetal Remake — Datenschicht.

EINE Stelle, an der die Originaldaten aus `data/*.json` geladen werden. Alles, was vorher
eigene Tabellen im Code hatte (Einheiten, Waren, Forschungen, Rohstoffe, Gebaeude), kommt
ab hier aus den Originaldateien. Damit gibt es keine zweite, widersprechende Wertequelle mehr.

Grundsaetze:
  * Fehlt ein Wert in der Vorlage, ist er `None` — hier wird **nichts** erfunden.
  * Pfade werden relativ zur Projektwurzel gebildet, damit es auch verpackt funktioniert.
"""
from __future__ import annotations

import json
import os
from functools import lru_cache
from typing import Any, Dict, Optional

STAND = "2026-10-04"


def projektwurzel() -> str:
    """Projektwurzel — funktioniert als Skript und in einer gepackten Anwendung.

    In der EXE (PyInstaller) liegen die Datendateien NICHT neben der Exe, sondern im
    entpackten Zwischenordner ``sys._MEIPASS``; genau dort sucht PyInstaller sie auch fuer
    ``__file__``. Ohne diesen Zweig findet die fertige EXE ihre ``data/*.json`` nicht.
    """
    import sys
    if getattr(sys, "frozen", False):                     # PyInstaller
        return getattr(sys, "_MEIPASS", None) or os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _lade(dateiname: str) -> Dict[str, Any]:
    pfad = os.path.join(projektwurzel(), "data", dateiname)
    with open(pfad, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------- Einheiten

@lru_cache(maxsize=1)
def einheiten() -> Dict[str, Dict[str, Any]]:
    """Die 28 Originaleinheiten, Schluessel = Originalname."""
    return _lade("units.json")["einheiten"]


def einheit(name: str) -> Optional[Dict[str, Any]]:
    return einheiten().get(name)


def einheiten_nach_kategorie() -> Dict[str, list[str]]:
    out: Dict[str, list[str]] = {}
    for name, e in einheiten().items():
        out.setdefault(e["kategorie"], []).append(name)
    return out


def wert(name: str, feld: str) -> Optional[float]:
    """Ein Kampfwert (LE, AT, PA, SI, HE, RS, TP_min, TP_max, GS, MU, SK).

    Gibt None zurueck, wenn die Vorlage den Wert nicht hergibt — bewusst nicht 0,
    damit 'kein Wert' und 'Wert ist null' unterscheidbar bleiben.
    """
    e = einheit(name)
    if not e:
        return None
    return e["werte"].get(feld)


def wert_fehlt(name: str, feld: str) -> bool:
    return wert(name, feld) is None


def luecken() -> Dict[str, list[str]]:
    """Welche Werte fehlen je Einheit — fuer Anzeige und Bericht."""
    return {n: [k for k, v in e["werte"].items() if v is None]
            for n, e in einheiten().items() if any(v is None for v in e["werte"].values())}


def kosten(name: str) -> Dict[str, int]:
    return dict(einheit(name)["kosten"]) if einheit(name) else {}


def benoetigte_waren(name: str) -> list[str]:
    return list(einheit(name)["waren"]) if einheit(name) else []


def kriegspunkte(name: str) -> Optional[int]:
    return einheit(name)["kriegspunkte"] if einheit(name) else None


def voraussetzung(name: str) -> Optional[Dict[str, Any]]:
    return einheit(name)["voraussetzung"] if einheit(name) else None


def ladung(name: str) -> Optional[int]:
    return einheit(name)["ladung"] if einheit(name) else None


def icon_pfad(name: str) -> Optional[str]:
    """Absoluter Pfad zur Icon-Datei einer Einheit oder Ware."""
    e = einheit(name)
    rel = e["icon"] if e else waren_icons().get(name)
    if not rel:
        return None
    p = os.path.join(projektwurzel(), rel.replace("/", os.sep))
    return p if os.path.exists(p) else None


# ---------------------------------------------------------------- Waren

@lru_cache(maxsize=1)
def waren() -> Dict[str, Dict[str, Any]]:
    return _lade("items.json")["waren"]


@lru_cache(maxsize=1)
def waren_icons() -> Dict[str, str]:
    return {n: e["icon"] for n, e in waren().items() if e.get("icon")}


# ---------------------------------------------------------------- Forschung, Rohstoffe, Gebaeude

@lru_cache(maxsize=1)
def forschungen() -> Dict[str, Dict[str, Any]]:
    return _lade("research.json")["forschungen"]


@lru_cache(maxsize=1)
def forschungsregeln() -> Dict[str, str]:
    return _lade("research.json").get("regeln", {})


@lru_cache(maxsize=1)
def rohstoffe() -> Dict[str, Dict[str, Any]]:
    return _lade("resources.json")["rohstoffe"]


@lru_cache(maxsize=1)
def gebaeude() -> list[Dict[str, Any]]:
    return _lade("buildings.json")["gebaeude"]


def gebaeude_nach_id() -> Dict[str, Dict[str, Any]]:
    return {g["id"]: g for g in gebaeude() if g.get("id")}


def wallstufen() -> list[Dict[str, Any]]:
    for g in gebaeude():
        if g.get("id") == "verteidigungswall":
            return g.get("stufen", [])
    return []


def forschungsdauer_stunden(neue_stufe: int) -> Optional[int]:
    """Originalregel: neue Stufe zum Quadrat, in Stunden. Ohne Vorlage kein Wert."""
    for text in forschungsregeln().values():
        if "Quadrat" in text:
            return neue_stufe ** 2
    return None


# Handbuch Seite 12/13, woertlich:
#   "Die Rohstoffkosten die zum Forschen aufgebracht werden muessen, verdoppeln sich pro Stufe.
#    Das bedeutet, wenn Du fuer eine Forschung Stufe1 50 Holz benoetigst, benoetigst Du fuer
#    Stufe2 100 Holz, fuer Stufe3 200 Holz, fuer Stufe4 400 Holz usw."
# Daraus: Grundbetrag 50 Holz auf Stufe 1, je weitere Stufe das Doppelte.
FORSCHUNG_GRUNDKOSTEN_HOLZ = 50


def forschungs_kosten(neue_stufe: int, rohstoff: str = "holz") -> Dict[str, int]:
    """Rohstoffkosten, um eine Forschung auf `neue_stufe` zu bringen (Handbuch Seite 13).

    Stufe 1 = 50, Stufe 2 = 100, Stufe 3 = 200, Stufe 4 = 400 … — genau die Zahlenreihe des
    Handbuchbeispiels. Das Handbuch nennt als Beispiel Holz; fuer die uebrigen Forschungen
    ist dort kein eigener Rohstoff abgedruckt.
    """
    if neue_stufe < 1:
        return {}
    return {rohstoff: FORSCHUNG_GRUNDKOSTEN_HOLZ * 2 ** (neue_stufe - 1)}


def kriegspunkte_verteidigung(ausbaustufe: int) -> int:
    """Originalregel: Ausbaustufe hoch drei."""
    return ausbaustufe ** 3


def uebersicht() -> Dict[str, int]:
    return {
        "einheiten": len(einheiten()),
        "waren": len(waren()),
        "forschungen": len(forschungen()),
        "rohstoffe": len(rohstoffe()),
        "gebaeude": len(gebaeude()),
        "wallstufen": len(wallstufen()),
        "einheiten_mit_luecken": len(luecken()),
    }
