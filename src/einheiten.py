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

import json
import math
import os
from functools import lru_cache
from typing import Any, Dict, List, Optional, Tuple

import spieldaten
import hilfen


def lade_regel(dateiname: str) -> Dict[str, Any]:
    """Eine Regeldatendatei aus `data/` laden (oeffentlicher Weg, keine privaten Helfer)."""
    with open(os.path.join(spieldaten.projektwurzel(), "data", dateiname), encoding="utf-8") as f:
        return json.load(f)

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


def ist_kundschafter(name: str) -> bool:
    """Ist die Einheit ein Kundschafter (Diebesgilde)?

    B-5 (02.11.2026): Spionage braucht Kundschafter - sechs Stufen von Streuner bis Waldlaeufer
    (data/units.json, Kategorie Kundschafter). Eigene Funktion statt Namensvergleich, damit
    Umbenennungen und neue Stufen nicht still die Spionage abschalten.
    """
    return rolle(name) == "kundschafter"



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
    """Tragfaehigkeit fuer Beute (nur Karren) - BASISWERT ohne Forschungsbonus."""
    return ladung(name) * anzahl if ist_transport(name) else 0


# Wagenbau-Bonus auf die Karrenladung (Daniels Entscheidung 2, 31.10.2026): die belegten Werte
# aus data/units.json bleiben die BASIS, der Bonus kommt obendrauf. BELEGT ist nur die Richtung
# (Wagenbau schaltet neue Karren frei), der Prozentwert ist VORSCHLAG - siehe
# data/karrenkapazitaet.json. `aktiv=false` nimmt ihn vollstaendig heraus.
KARREN = lade_regel("karrenkapazitaet.json")
KARREN_BONUS_AKTIV = bool(KARREN.get("aktiv", True))
KARREN_FORSCHUNG = str(KARREN.get("forschung") or "Wagenbau")
KARREN_PRO_STUFE = float(KARREN.get("pro_stufe_prozent") or 0.0)
KARREN_HOECHSTSTUFE = int(KARREN.get("hoechststufe") or 10)


def stufe_von(forschung: Any, gebiet: str = None) -> int:
    """Forschungsstufe eines Gebiets aus einer flachen Karte `{Gebiet: Stufe}` (0 = unbekannt)."""
    if not isinstance(forschung, dict):
        return 0
    gebiet = gebiet or KARREN_FORSCHUNG
    for name, wert in forschung.items():
        if str(name) == gebiet:
            n = hilfen.als_int(wert, 0)
            return max(0, min(n, KARREN_HOECHSTSTUFE))
    return 0


def ladungs_bonus(forschung: Any) -> float:
    """Faktor auf die Karrenladung: 1.0 ohne Forschung, +pro_stufe_prozent je Wagenbau-Stufe."""
    if not KARREN_BONUS_AKTIV or KARREN_PRO_STUFE <= 0:
        return 1.0
    stufe = stufe_von(forschung)
    return 1.0 + (KARREN_PRO_STUFE / 100.0) * stufe


def ladung_mit_bonus(name: str, forschung: Any = None) -> int:
    """Ladeplaetze EINER Einheit MIT Wagenbau-Bonus (ganzzahlig, nie kleiner als der Basiswert)."""
    basis = ladung(name)
    if basis <= 0:
        return 0
    return max(basis, int(math.floor(basis * ladungs_bonus(forschung) + 1e-9)))


def kapazitaet_mit_bonus(name: str, anzahl: int = 1, forschung: Any = None) -> int:
    """Tragfaehigkeit einer Gruppe MIT Bonus (Basis * Anzahl, dann der Faktor)."""
    if not ist_transport(name) or isinstance(anzahl, bool):
        return 0
    n = hilfen.als_int(anzahl, 0)
    if n <= 0:
        return 0
    return max(kapazitaet(name, n), int(math.floor(kapazitaet(name, n) * ladungs_bonus(forschung) + 1e-9)))


def ladung_der_gruppe(bestand: Any, forschung: Any = None) -> int:
    """Gesamte Tragfaehigkeit einer Gruppe `{name: anzahl}` - MIT Wagenbau-Bonus.

    Nur Karren tragen; Kaempfer, Kundschafter und Belagerungswaffen zaehlen 0. Angaben, die
    keine ganze Zahl groesser 0 ergeben, werden uebergangen. Negative Ergebnisse sind
    ausgeschlossen.

    **EINE Stelle fuer die Karrenladung** (Code-Audit 31.10.2026, Befund P3 Vorschlag 2):
    vorher summierten `auftraege.ladung_der_mission`, `kampfbericht.beute` und
    `kampfbericht.beute_staffel` dieselbe Rechnung je fuer sich. Seit Daniels Entscheidung 2
    (31.10.2026) kommt der Wagenbau-Bonus hier dazu - wer die Ladung rechnet, MUSS die
    Forschungsstufen mitgeben (`{Gebiet: Stufe}`), sonst rechnet er ohne Bonus.
    """
    if not isinstance(bestand, dict):
        return 0
    gesamt = 0
    factor = ladungs_bonus(forschung)
    for name, anzahl in bestand.items():
        n = hilfen.als_int(anzahl, 0)
        if n > 0:
            basis = kapazitaet(str(name), n)
            gesamt += max(basis, int(math.floor(basis * factor + 1e-9)))
    return max(0, gesamt)


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
