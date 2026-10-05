"""
Spielzeit — der Zeitfaktor (Vorgabe Daniel 05.10.2026, Spielbericht).

**Der Befund:** `tick(dt_seconds)` rechnete Echtzeitsekunden 1:1 als Spielsekunden
(`dt_h = dt_seconds / 3600`). Damit war ein Spieltag = 24 Echtzeitstunden und ein Holzfäller
mit „4 Holz/Stunde" lieferte **4 Holz in einer echten Stunde** — im Spiel war kein regelmäßiger
Rohstoffeingang zu sehen, Forschung und Ausbau waren nicht erlebbar. Genau Daniels Bericht.

**Die Regel:** die **Handbuchformeln bleiben unangetastet** (ein Holzfäller auf Wald bringt
4 Holz je Spielstunde). Nur die Spieluhr läuft schneller — wie auf einem Speedserver im Original
(`docs/PLAN_AUS_HANDBUCH.md`, dort ausdrücklich als Daniels Entscheidung vermerkt).

**Eine Quelle:** dieser Baustein. Der Faktor steht in ``data/spielzeit.json`` und lässt sich in den
Einstellungen umstellen; das Spiel liest ihn an genau einer Stelle (`_tick_loop`).

**Nicht belegt** — das Handbuch kennt keinen Zeitfaktor für eine Einzelspieler-Fassung. Der
Standardwert ist deshalb als VORSCHLAG gekennzeichnet und in den Einstellungen änderbar.
"""
from __future__ import annotations

import io
import json
import os

ORDNER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PFAD = os.path.join(ORDNER, "data", "spielzeit.json")

# VORSCHLAG: 1 Spielstunde = 20 Sekunden. Damit liefert der Holzfäller auf Wald (4 Holz/h)
# 12 Holz in einer echten Minute — sichtbar, und eine Forschung von 3 Stunden dauert 1 Minute.
STANDARD_FAKTOR = 180.0
STUFEN = (1.0, 20.0, 60.0, 180.0, 600.0)

_VORGABE = {
    "faktor": STANDARD_FAKTOR,
    "stufen": list(STUFEN),
    "belegt": False,
    "_hinweis": (
        "Zeitfaktor: so viele Spielsekunden je Echtzeitsekunde. 1 = Originaltempo (1 Spieltag = "
        "24 echte Stunden). 180 = eine Spielstunde in 20 Sekunden. Die Handbuchformeln selbst "
        "bleiben unveraendert, nur die Spieluhr laeuft schneller. Von Daniel aenderbar."
    ),
    "_befund": (
        "05.10.2026, Spielbericht Daniel: der Rohstoffeingang war nicht sichtbar, weil die "
        "Spieluhr im Originaltempo lief (4 Holz je ECHTER Stunde)."
    ),
}

_gemerkt = None


def _laden() -> dict:
    try:
        with io.open(PFAD, encoding="utf-8") as f:
            daten = json.load(f)
        if not isinstance(daten, dict):
            raise ValueError("kein Objekt")
        return daten
    except Exception:
        return dict(_VORGABE)


def daten() -> dict:
    """Die Datei mit allen Werten (fehlende Schlüssel aus der Vorgabe ergänzt)."""
    werte = dict(_VORGABE)
    werte.update(_laden())
    return werte


def faktor() -> float:
    """Spielsekunden je Echtzeitsekunde (nie 0 oder negativ)."""
    global _gemerkt
    if _gemerkt is None:
        try:
            wert = float(daten().get("faktor", STANDARD_FAKTOR))
        except (TypeError, ValueError):
            wert = STANDARD_FAKTOR
        _gemerkt = wert if wert > 0 else STANDARD_FAKTOR
    return _gemerkt


def setzen(wert: float) -> float:
    """Faktor umstellen und in ``data/spielzeit.json`` schreiben. Liefert den neuen Wert."""
    global _gemerkt
    try:
        neu = float(wert)
    except (TypeError, ValueError):
        return faktor()
    if not neu > 0:
        return faktor()
    werte = daten()
    werte["faktor"] = neu
    werte["stufen"] = list(werte.get("stufen") or STUFEN)
    with io.open(PFAD, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(werte, ensure_ascii=False, indent=2))
        f.write("\n")
    _gemerkt = neu
    return neu


def vergessen():
    """Den Zwischenspeicher leeren (Prüfungen und „Laden")."""
    global _gemerkt
    _gemerkt = None


def stufen() -> list:
    """Die anwählbaren Stufen (immer mit dem aktuellen Wert)."""
    werte = [float(s) for s in (daten().get("stufen") or STUFEN) if float(s) > 0]
    if faktor() not in werte:
        werte.append(faktor())
    return sorted(set(werte))


def spielstunden_je_echtsekunde() -> float:
    """Wie viele Spielstunden eine echte Sekunde ergibt."""
    return faktor() / 3600.0


def echtzeit_fuer_spielstunden(stunden: float) -> float:
    """Wie viele echte Sekunden eine Spielstunde dauert (Umkehrung, für Wege und Anzeigen)."""
    return float(stunden) * 3600.0 / faktor()


def text(wert: float = None) -> str:
    """Kurzform für die Anzeige, z. B. „×180 · 1 Std = 20 s"."""
    w = faktor() if wert is None else float(wert)
    sekunden = 3600.0 / w if w > 0 else 0.0
    if abs(w - 1.0) < 1e-9:
        return "×1 · Originaltempo (1 Std = 1 Std)"
    return f"×{w:g} · 1 Std = {sekunden:g} s"
