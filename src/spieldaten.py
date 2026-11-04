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
    """Wo liegen die Datendateien? Es wird **gesucht**, nicht geraten.

    Als Quelltext ist die Wurzel der Ordner ueber `src/`. In der fertigen EXE stimmt das nicht:
    PyInstaller entpackt die mitgegebenen Ordner und die Module in einen Zwischenordner
    (``sys._MEIPASS``), und ``__file__`` eines gepackten Moduls zeigt nicht dorthin, wo man denkt.
    Deshalb werden die Kandidaten der Reihe nach geprueft — es gilt der erste, in dem wirklich
    ``data/gelaende.json`` liegt. Findet keiner die Dateien, kommt der letzte Kandidat zurueck,
    damit die Fehlermeldung den erwarteten Pfad zeigt.
    """
    import sys
    kandidaten = []
    basis = getattr(sys, "_MEIPASS", None)                    # PyInstaller (Einzeldatei/Ordner)
    if basis:
        kandidaten.append(basis)
    if getattr(sys, "frozen", False):
        kandidaten.append(os.path.dirname(os.path.abspath(sys.executable)))
    kandidaten.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    for kandidat in kandidaten:
        if kandidat and os.path.exists(os.path.join(kandidat, "data", "gelaende.json")):
            return kandidat
    return kandidaten[-1]


def _lade(dateiname: str) -> Dict[str, Any]:
    """Laedt eine Datei aus data/ als JSON - der eine Weg zu den Stammdaten."""
    pfad = os.path.join(projektwurzel(), "data", dateiname)
    with open(pfad, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------- Einheiten

@lru_cache(maxsize=1)
def einheiten() -> Dict[str, Dict[str, Any]]:
    """Die 28 Originaleinheiten, Schluessel = Originalname."""
    return _lade("units.json")["einheiten"]


def einheit(name: str) -> Optional[Dict[str, Any]]:
    """Der Rohdatensatz einer Einheit aus data/units.json (None, wenn unbekannt)."""
    return einheiten().get(name)


def einheiten_nach_kategorie() -> Dict[str, list[str]]:
    """Einheiten gruppiert nach ihrer Kategorie (z. B. 'Armee', 'Karren')."""
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
    """True, wenn ein Originalwert im Datenbestand fehlt (None statt Zahl)."""
    return wert(name, feld) is None


def luecken() -> Dict[str, list[str]]:
    """Welche Werte fehlen je Einheit — fuer Anzeige und Bericht."""
    return {n: [k for k, v in e["werte"].items() if v is None]
            for n, e in einheiten().items() if any(v is None for v in e["werte"].values())}


def kosten(name: str) -> Dict[str, int]:
    """Baukosten der Einheit als Verzeichnis (leer, wenn nichts hinterlegt ist)."""
    return dict(einheit(name)["kosten"]) if einheit(name) else {}


def benoetigte_waren(name: str) -> list[str]:
    """Welche Waren die Einheit bei der Ausbildung verbraucht."""
    return list(einheit(name)["waren"]) if einheit(name) else []


def kriegspunkte(name: str) -> Optional[int]:
    """Punktewert der Einheit fuer die Kriegspunkte laut Daten."""
    return einheit(name)["kriegspunkte"] if einheit(name) else None


def voraussetzung(name: str) -> Optional[Dict[str, Any]]:
    """Forschungsvoraussetzung der Einheit, z. B. {'forschung': 'Wagenbau', 'stufe': 1}."""
    return einheit(name)["voraussetzung"] if einheit(name) else None


def ladung(name: str) -> Optional[int]:
    """Ladeplaetze der Einheit laut Daten (None, wenn nicht angegeben)."""
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
    """Alle Waren aus data/items.json."""
    return _lade("items.json")["waren"]


@lru_cache(maxsize=1)
def waren_icons() -> Dict[str, str]:
    """Ware -> Icon-Pfad, nur fuer Waren, die ein Icon haben."""
    return {n: e["icon"] for n, e in waren().items() if e.get("icon")}


# ---------------------------------------------------------------- Forschung, Rohstoffe, Gebaeude

@lru_cache(maxsize=1)
def forschungen() -> Dict[str, Dict[str, Any]]:
    """Alle Forschungsgebiete aus data/research.json."""
    return _lade("research.json")["forschungen"]


@lru_cache(maxsize=1)
def forschungsregeln() -> Dict[str, str]:
    """Regeln zur Forschung (Dauer, Kosten) aus data/research.json."""
    return _lade("research.json").get("regeln", {})


@lru_cache(maxsize=1)
def rohstoffe() -> Dict[str, Dict[str, Any]]:
    """Alle Rohstoffe aus data/resources.json."""
    return _lade("resources.json")["rohstoffe"]


@lru_cache(maxsize=1)
def gebaeude() -> list[Dict[str, Any]]:
    """Alle Gebaeude aus data/buildings.json."""
    return _lade("buildings.json")["gebaeude"]


def gebaeude_nach_id() -> Dict[str, Dict[str, Any]]:
    """Gebaeude als Verzeichnis id -> Datensatz (schneller Zugriff)."""
    return {g["id"]: g for g in gebaeude() if g.get("id")}


def wallstufen() -> list[Dict[str, Any]]:
    """Die Wallstufen des Verteidigungswalls (Schwellen, Kosten je Stufe)."""
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
    """Kurzstatistik ueber den Datenbestand (Anzahl Einheiten, Waren, Forschungen ...)."""
    return {
        "einheiten": len(einheiten()),
        "waren": len(waren()),
        "forschungen": len(forschungen()),
        "rohstoffe": len(rohstoffe()),
        "gebaeude": len(gebaeude()),
        "wallstufen": len(wallstufen()),
        "einheiten_mit_luecken": len(luecken()),
    }
