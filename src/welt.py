"""
Weltkarte des Limbus fuer das Nebelseetal-Remake.

Belegt (Handbuch 2009, S. 80-83 "Portal"; Portal-Anleitung 2005, portal.php;
alte Website screens.php):
  * Alle Welten in Nebelseetal liegen im magischen Limbus, der sich in 20 Dimensionen
    aufteilt und ueber magische Portale verbunden ist.
  * Die sechs belegten Weltnamen: Armageddon, Ragnaroek, Utgard, Midgard, Valhalla, Limbus.
  * Die Portalkosten haengen von der Entfernung ab; in eine andere Dimension zu reisen
    kostet deutlich mehr Mana.

NICHT belegt (deshalb VORSCHLAG, in data/welten.json aenderbar):
  * die Anordnung der 20 Dimensionen in der Limbus-Ebene (x/y) und die Besetzung der
    Dimensionen mit den sechs Weltnamen
  * die Portalkostenformel (Grundbetrag, Kosten je Schritt)
"""
from __future__ import annotations

import json
from pathlib import Path

import spieldaten

# Wurzel ueber EINE Stelle (spieldaten.projektwurzel) — auch in der fertigen EXE richtig.
WURZEL = Path(spieldaten.projektwurzel())
DATEN = WURZEL / "data"


def _lade(name: str) -> dict:
    return json.loads((DATEN / name).read_text(encoding="utf-8"))


_DATEI = _lade("welten.json")
DIMENSIONEN: list = _DATEI["dimensionen"]
REGEL: dict = _DATEI["portalregel"]
WELTNAMEN: list = _DATEI["welten_belegt"]

_NACH_KENNUNG = {d["kennung"]: d for d in DIMENSIONEN}


def _norm(s) -> str:
    """Vergleichsform eines Namens: klein, ohne Umlaute (akzeptiert 'Ragnaroek' wie 'Ragnarök')."""
    return (str(s).strip().lower().replace("ä", "ae").replace("ö", "oe")
            .replace("ü", "ue").replace("ß", "ss"))


_NACH_NAME: dict = {}
for _d in DIMENSIONEN:
    _NACH_NAME[_norm(_d["kennung"])] = _d["kennung"]
    _NACH_NAME[_norm(_d["name"])] = _d["kennung"]


def finde(kennung_oder_name):
    """Findet die Kennung einer Dimension — akzeptiert Kennung ODER Anzeigename. None, wenn unbekannt."""
    if kennung_oder_name in _NACH_KENNUNG:
        return kennung_oder_name
    return _NACH_NAME.get(_norm(kennung_oder_name))


def dimensionen() -> list:
    """Die 20 Dimensionen des Limbus in Dateireihenfolge."""
    return list(DIMENSIONEN)


def welten() -> list:
    """Nur die Dimensionen, in denen eine der sechs belegten Welten liegt."""
    return [d for d in DIMENSIONEN if d.get("welt")]


def entfernung(a, b):
    """
    Schritte zwischen zwei Dimensionen (symmetrisch).

    Nutzt die in data/welten.json gewaehlte Regel ('manhattan' oder 'euklidisch').
    Rueckgabe: Zahl — oder None, wenn eine der Kennungen unbekannt ist.
    """
    ka, kb = finde(a), finde(b)
    if ka is None or kb is None:
        return None
    da, db = _NACH_KENNUNG[ka], _NACH_KENNUNG[kb]
    if REGEL.get("art") == "euklidisch":
        return round(((da["x"] - db["x"]) ** 2 + (da["y"] - db["y"]) ** 2) ** 0.5, 3)
    return abs(da["x"] - db["x"]) + abs(da["y"] - db["y"])


def portalkosten(von, nach):
    """
    Manakosten des Portals von einer Dimension in die andere.

    Regel aus data/welten.json: mana = grundbetrag + kosten_je_schritt * entfernung.
    Rueckgabe: Zahl — oder None, wenn eine der Kennungen unbekannt ist.
    """
    e = entfernung(von, nach)
    if e is None:
        return None
    return int(round(REGEL["grundbetrag"] + REGEL["kosten_je_schritt"] * e))


def nachbarn(kennung, umkreis=None) -> list:
    """
    Dimensionen im Umkreis einer Dimension, nach Entfernung sortiert, ohne sie selbst.

    `umkreis` = groesste Entfernung in Schritten (Standard aus data/welten.json).
    Unbekannte Kennung ergibt eine leere Liste (kein Absturz).
    Jeder Eintrag traegt die Entfernung als Feld '_entfernung'.
    """
    k = finde(kennung)
    if k is None:
        return []
    if umkreis is None:
        umkreis = REGEL.get("standart_umkreis", 3)
    treffer = []
    for d in DIMENSIONEN:
        if d["kennung"] == k:
            continue
        e = entfernung(k, d["kennung"])
        if e is not None and e <= umkreis:
            treffer.append({**d, "_entfernung": e})
    treffer.sort(key=lambda d: (d["_entfernung"], d["kennung"]))
    return treffer


def beschreibung(kennung) -> str:
    """Lesbarer deutscher Text zu einer Dimension. Meldet Unbekanntes, statt abzustuerzen."""
    k = finde(kennung)
    if k is None:
        return f"Unbekannte Dimension: {kennung}"
    d = _NACH_KENNUNG[k]
    lage = f"liegt auf x={d['x']}, y={d['y']}"
    if d.get("welt"):
        return (f"{d['name']} (Kennung {d['kennung']}) {lage}; "
                f"hier liegt die belegte Welt {d['welt']}.")
    return (f"{d['name']} (Kennung {d['kennung']}) {lage}; "
            f"keine der sechs belegten Welten.")
