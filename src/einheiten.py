"""
Nebelseetal Remake — Einheiten-Bruecke.

Verbindet die Originaldaten (`data/units.json`) mit dem Spiel. Vorher gab es **zwei**
widersprechende Tabellen: `main.UNITS` (36 Einheiten, nur Anzeige) und
`bonus_system.UNIT_BASE` (7 Einheiten, rechnete). Einheiten, die nur in der ersten standen,
rechneten mit 0 — 29 von 36.

Hier gilt: **eine** Quelle, und jede Einheit bekommt eine **Rolle**. Karren und
Belagerungswaffen sind im Original *keine* Kaempfer — sie haben keine LE/AT/PA. Das ist kein
fehlender Wert, sondern ihre Rolle. Genau darum gibt es `rolle` und nicht nur `attack`.
"""
from __future__ import annotations

from functools import lru_cache
from typing import Any, Dict, List, Optional, Tuple

import spieldaten

# Handbuch Seite 14: vier Typen — Karren, Belagerungswaffen, Kundschafter, Kampfeinheiten.
ROLLEN: Dict[str, str] = {
    "Nahkampf": "kaempfer",
    "Fernkampf": "kaempfer",
    "Kundschafter": "kundschafter",   # kaempfen mit, ihr Zweck ist aber Aufklaerung
    "Karren": "karren",              # tragen Beute und Ausruestung, kaempfen nicht
    "Belagerung": "belagerung",      # brechen Mauern, kaempfen nicht
}

ROLLEN_TEXT: Dict[str, str] = {
    "kaempfer": "Kampfeinheit",
    "kundschafter": "Kundschafter",
    "karren": "Karren",
    "belagerung": "Belagerungswaffe",
}


@lru_cache(maxsize=1)
def alle() -> Dict[str, Dict[str, Any]]:
    """Alle 28 Originaleinheiten, angereichert um Rolle und Icon-Pfad."""
    out: Dict[str, Dict[str, Any]] = {}
    for name, e in spieldaten.einheiten().items():
        rolle = ROLLEN[e["kategorie"]]
        out[name] = {
            "id": name,
            "name": name,
            "kategorie": e["kategorie"],
            "rolle": rolle,
            "rollen_text": ROLLEN_TEXT[rolle],
            "gebaeude": e.get("gebaeude"),
            "kosten": e.get("kosten") or {},
            "waren": e.get("waren") or [],
            "voraussetzung": e.get("voraussetzung"),
            "kriegspunkte": e.get("kriegspunkte"),
            "werte": e.get("werte") or {},
            "icon": e.get("icon"),
            "icon_pfad": spieldaten.icon_pfad(name),
            "ladung": e.get("ladung"),
            "nicht_original": e.get("nicht_original") or [],
        }
    return out


def namen() -> List[str]:
    """Alle Einheitennamen aus data/units.json, in Dateireihenfolge."""
    return list(alle().keys())


def nach_rolle(rolle: str) -> List[str]:
    """Alle Einheiten einer Rolle ('kaempfer', 'karren', 'belagerung', 'kundschafter')."""
    return [n for n, e in alle().items() if e["rolle"] == rolle]


def rolle(name: str) -> Optional[str]:
    """Die Rolle einer Einheit oder None, wenn der Name unbekannt ist."""
    e = alle().get(name)
    return e["rolle"] if e else None


def ist_kaempfer(name: str) -> bool:
    """Kaempft in der Schlacht (Kampfeinheiten und Kundschafter)."""
    return rolle(name) in ("kaempfer", "kundschafter")


def ist_transport(name: str) -> bool:
    """Kann Beute und Ausruestung tragen (Karren) — Handbuch Seite 22."""
    return rolle(name) == "karren"


def ist_belagerung(name: str) -> bool:
    """Ist die Einheit eine Belagerungswaffe (Ramme, Katapult, Turm)?"""
    return rolle(name) == "belagerung"


# --------------------------------------------------------------- Originalwerte

def _w(name: str, feld: str) -> Any:
    """Ein Originalwert roh aus den Daten (AT, PA, LE, SK, GS ...); None, wenn das Handbuch ihn nicht druckt."""
    e = alle().get(name)
    return e["werte"].get(feld) if e else None


def angriff(name: str) -> int:
    """Angriffswert (AT) - im Handbuch die Chance, mit der Waffe zu treffen."""
    return int(_w(name, "AT") or 0)


def verteidigung(name: str) -> int:
    """Verteidigungswert (PA) - die Chance, einen Treffer abzuwehren."""
    return int(_w(name, "PA") or 0)


def leben(name: str) -> int:
    """Lebensenergie (LE) - wie viel Schaden die Einheit verkraftet."""
    return int(_w(name, "LE") or 0)


def schlagkraft(name: str) -> int:
    """Schlagkraft (SK) - die Kennzahl, die die Wallschwelle prueft (nicht AT!)."""
    return int(_w(name, "SK") or 0)


def mut(name: str) -> Optional[int]:
    """None = im Handbuch fuer diese Einheit nicht abgedruckt (Karren, Belagerung)."""
    return _w(name, "MU")


def geschwindigkeit(name: str) -> int:
    """Reisegeschwindigkeit (GS); die langsamste Einheit bestimmt das Tempo der Gruppe."""
    return int(_w(name, "GS") or 0)


def mauer_schaden(name: str) -> Tuple[int, int]:
    """Schadensbereich gegen Mauern (Handbuch Seite 20). (0, 0) = keine Belagerungswaffe."""
    lo, hi = _w(name, "TP_min"), _w(name, "TP_max")
    return (int(lo or 0), int(hi or 0))


def ladung(name: str) -> int:
    """Ladeplaetze als Karren (0 fuer Kaempfer und Belagerungswaffen)."""
    return int(alle()[name]["ladung"] or 0) if name in alle() else 0


def kriegspunkte(name: str) -> Optional[int]:
    """Fester Punktewert der Einheit fuer die Kriegspunkte (None = 'Punktewert -')."""
    e = alle().get(name)
    return e["kriegspunkte"] if e else None


def fehlende_werte(name: str) -> List[str]:
    """Welche Werte das Handbuch fuer diese Einheit nicht nennt."""
    e = alle().get(name)
    return [k for k, v in e["werte"].items() if v is None] if e else []


# --------------------------------------------------------------- Kampfstaerke

def kampfstaerke(name: str, anzahl: int = 1) -> float:
    """Ein ehrlicher Wert je Rolle — nicht alles ist ein Kaempfer.

    kaempfer/kundschafter -> Angriffswert AT (so kaempft die Einheit laut Handbuch)
    belagerung           -> Schlagkraft SK (so bricht sie Mauern, Seite 20)
    karren               -> 0; Karren kaempfen nicht, sie tragen (siehe `ladung`)
    """
    r = rolle(name)
    if r in ("kaempfer", "kundschafter"):
        return angriff(name) * anzahl
    if r == "belagerung":
        return schlagkraft(name) * anzahl
    return 0.0


def kapazitaet(name: str, anzahl: int = 1) -> int:
    """Tragfaehigkeit fuer Beute (nur Karren)."""
    return ladung(name) * anzahl if ist_transport(name) else 0


def beschreibung(name: str) -> str:
    """Kurze, sachliche Beschreibung — ausschliesslich aus den Originalangaben."""
    e = alle().get(name)
    if not e:
        return ""
    teile = [e["rollen_text"]]
    if e["gebaeude"]:
        teile.append(f"aus {e['gebaeude']}")
    if e["werte"].get("LE") is not None:
        teile.append(f"LE {e['werte']['LE']}")
    if e["werte"].get("AT") is not None:
        teile.append(f"AT {e['werte']['AT']}")
    if e["werte"].get("SK") is not None:
        teile.append(f"SK {e['werte']['SK']}")
    if ist_transport(name):
        teile.append(f"Ladung {ladung(name)}")
    if ist_belagerung(name):
        lo, hi = mauer_schaden(name)
        teile.append(f"Mauerschaden {lo}-{hi}")
    return ", ".join(teile) + "."


def uebersicht() -> Dict[str, int]:
    """Kurzstatistik: wie viele Einheiten je Rolle, wie viele Originalwerte fehlen."""
    d = {"gesamt": len(alle())}
    for r in ROLLEN_TEXT:
        d[r] = len(nach_rolle(r))
    d["mit_fehlenden_werten"] = len([n for n in alle() if fehlende_werte(n)])
    return d
