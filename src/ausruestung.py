"""Nebelseetal Remake — Ausruestung: welche Waren eine Einheit zur Ausbildung braucht.

Beobachtung: manche Einheiten sind erst ausbildbar, wenn die noetigen Waren (Waffen,
Ruestungen, Umhaenge) im Lager liegen — auch wenn die Truppe schon erforscht ist. Die
Daten sagen das bereits (``data/units.json``, Feld ``waren``), aber bisher hat es niemand
geprueft. Dieses Modul ist die FACHLICHE Schicht dafuer: reine Datenfunktionen, kein
Fenster, keine Zeichenlogik.

Belegte Angaben (Handbuch 2009, ``data/units.json``, ``data/items.json``):
  * Genau 14 der 28 Einheiten nennen in ``waren`` die Waren, die zu ihrer Ausbildung
    gebraucht werden; die uebrigen 14 brauchen keine Ware.
  * Jede Ware entsteht in einer Werkstatt (``data/items.json`` Feld ``werkstatt``:
    Schmiede, Bogner, Naehstube) und hat eine Forschungsvoraussetzung (Feld
    ``voraussetzung``, z. B. 'Waffentechnik 5').
  * Jede Einheit hat eine Ausbildungsstaette (``data/units.json`` Feld ``gebaeude``).

Das Modul nutzt nur die Standardbibliothek und die Projektdaten (``spieldaten``). Es
schreibt keine Datei, oeffnet kein Fenster, wuerfelt nicht und kennt keine Farbe/kein Emoji.
Werte, die die Vorlage nicht hergibt, werden NICHT geschaetzt — sie stehen in
``offene_luecken()``.
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

import spieldaten

# Die vier Arten von Schritten der Ausruestungs-Kette (siehe `kette`).
ARTEN = ("forschung", "werkstatt", "ware", "einheit")


# --------------------------------------------------------------------------
# Hilfsgriffe auf die Datenlage
# --------------------------------------------------------------------------

def _einheiten() -> Dict[str, Dict[str, Any]]:
    """Die 28 Einheiten aus data/units.json (Schluessel = Originalname)."""
    return spieldaten.einheiten()


def _waren() -> Dict[str, Dict[str, Any]]:
    """Die 17 Waren aus data/items.json."""
    return spieldaten.waren()


def _einheit_oder_fehler(einheit: str) -> Dict[str, Any]:
    """Der Datensatz einer Einheit oder ein ValueError, der die bekannten Namen nennt."""
    daten = _einheiten()
    if einheit not in daten:
        bekannt = ", ".join(sorted(daten))
        raise ValueError(f"Unbekannte Einheit {einheit!r}. Bekannte Einheiten sind: {bekannt}.")
    return daten[einheit]


def _zahl(wert: Any) -> int:
    """Ein Lagerbestand als ganze Zahl; alles Unbrauchbare gilt als 0."""
    try:
        return int(wert)
    except (TypeError, ValueError):
        return 0


def _anzahl(anzahl: Any) -> int:
    """Prueft die gewuenschte Stueckzahl: ganze Zahl, mindestens 1."""
    try:
        n = int(anzahl)
    except (TypeError, ValueError):
        raise ValueError(f"Die Anzahl muss eine ganze Zahl sein, war {anzahl!r}.")
    if n < 1:
        raise ValueError(f"Die Anzahl muss mindestens 1 sein, war {n}.")
    return n


def _werkstatt_von(ware: str) -> str:
    """Die Werkstatt einer Ware (Feld 'werkstatt' aus data/items.json), sonst ''."""
    return str((_waren().get(ware) or {}).get("werkstatt") or "")


def _voraussetzungen_von(ware: str) -> List[str]:
    """Die Voraussetzungen einer Ware als Liste, direkt aus dem Textfeld abgeleitet.

    Das Handbuch nennt sie als Text ('Waffentechnik 5' oder 'Naehkunst 1 + Ruestungsbau 2').
    Kombinierte Voraussetzungen haben kein Strukturfeld — sie werden deshalb am '+' getrennt.
    Fehlt die Angabe oder lautet sie 'keine', ist die Liste leer.
    """
    text = str((_waren().get(ware) or {}).get("voraussetzung") or "").strip()
    if not text or text.lower() == "keine":
        return []
    return [teil.strip() for teil in text.split("+") if teil.strip()]


# --------------------------------------------------------------------------
# 1. Warenbedarf einer Einheit
# --------------------------------------------------------------------------

def bedarf(einheit: str) -> list[str]:
    """Die Waren, die eine Einheit zur Ausbildung braucht.

    Liest das Feld ``waren`` aus ``data/units.json`` in der Reihenfolge der Datei.
    Einheiten ohne Warenbedarf liefern eine leere Liste. Ist der Name unbekannt, wird ein
    ``ValueError`` ausgeloest, der den Namen UND die bekannten Schluessel nennt — hier wird
    nichts geraten.
    """
    eintrag = _einheit_oder_fehler(einheit)
    return list(eintrag.get("waren") or [])


def fehlende(einheit: str, waren: dict, anzahl: int = 1) -> dict:
    """Je Ware die Fehlmenge fuer ``anzahl`` Einheiten: ``{Ware: Fehlmenge}``.

    Nur Waren mit Fehlmenge groesser 0 stehen im Ergebnis; ein leeres dict heisst 'nichts
    fehlt'. Waren, die die Einheit nicht braucht, werden nicht betrachtet. ``anzahl`` muss
    mindestens 1 sein.
    """
    menge = _anzahl(anzahl)
    _einheit_oder_fehler(einheit)
    lager = waren or {}
    fehlt: Dict[str, int] = {}
    for ware in bedarf(einheit):
        ist = _zahl(lager.get(ware, 0))
        if ist < menge:
            fehlt[ware] = menge - ist
    return fehlt


def ausbildbar(einheit: str, waren: dict, anzahl: int = 1) -> tuple[bool, str]:
    """(ausbildbar?, Begruendung) fuer ``anzahl`` Einheiten.

    Ist jede benoetigte Ware ausreichend im Lager, kommt ``(True, kurze Begruendung)``
    zurueck. Fehlt Ware, nennt die Begruendung JEDE fehlende Ware mit Soll/Ist (z. B.
    'Kurzschwert 1/0', gelesen als Soll/Ist). ``anzahl`` muss mindestens 1 sein, sonst
    ``ValueError``.
    """
    menge = _anzahl(anzahl)
    _einheit_oder_fehler(einheit)
    lager = waren or {}
    fehlt = fehlende(einheit, lager, menge)
    if not fehlt:
        return True, f"{einheit} kann ausgebildet werden, alle Waren sind im Lager."
    teile: List[str] = []
    for ware in bedarf(einheit):
        if ware in fehlt:
            teile.append(f"{ware} {menge}/{_zahl(lager.get(ware, 0))}")
    return False, f"Es fehlen: {' · '.join(teile)}."


def verbrauchen(waren: dict, einheit: str, anzahl: int = 1) -> dict:
    """Ein NEUES Lager-dict, in dem die Waren fuer ``anzahl`` Einheiten abgezogen sind.

    Das uebergebene dict wird NICHT veraendert. Reicht der Bestand fuer auch nur eine
    benoetigte Ware nicht, kommt ein unveraendertes Abbild zurueck und es wird gar nichts
    abgezogen (kein Teilverbrauch) — der Bestand geht nie unter 0. ``anzahl`` muss
    mindestens 1 sein.
    """
    menge = _anzahl(anzahl)
    _einheit_oder_fehler(einheit)
    lager = waren or {}
    neu: Dict[str, Any] = dict(lager)
    for ware in bedarf(einheit):
        if _zahl(neu.get(ware, 0)) < menge:
            return dict(lager)                     # nicht genug: unveraendert zurueck
    for ware in bedarf(einheit):
        neu[ware] = _zahl(neu.get(ware, 0)) - menge
    return neu


# --------------------------------------------------------------------------
# 2. Die Kette: von der Forschung ueber Werkstatt und Ware zur Einheit
# --------------------------------------------------------------------------

def _schritt(nr: int, art: str, was: str, wo: str, hinweis: str) -> Dict[str, Any]:
    return {"schritt": nr, "art": art, "was": was, "wo": wo, "hinweis": hinweis}


def kette(einheit: str) -> list[dict]:
    """Die Ausruestungs-Kette einer Einheit als Liste von Schritten.

    Jeder Schritt ist ein dict mit:
      ``schritt``  1-basiert fortlaufend,
      ``art``      'forschung', 'werkstatt', 'ware' oder 'einheit',
      ``was``      der Name (Forschung/Werkstatt/Ware/Einheit),
      ``wo``       die Werkstatt oder die Ausbildungsstaette,
      ``hinweis``  ein deutscher Satz.

    Alles wird aus ``data/units.json`` + ``data/items.json`` abgeleitet; es werden KEINE
    Voraussetzungen erfunden, die nicht in den Daten stehen. Eine Einheit ohne Warenbedarf
    hat genau einen Schritt: die Ausbildung.
    """
    eintrag = _einheit_oder_fehler(einheit)
    staette = str(eintrag.get("gebaeude") or "")
    waren_liste = list(eintrag.get("waren") or [])

    if not waren_liste:
        return [_schritt(1, "einheit", einheit, staette,
                         f"{einheit} in {staette} ausbilden, es wird keine Ware gebraucht.")]

    schritte: List[Dict[str, Any]] = []

    # 1. Die Werkstaetten, in denen die Waren entstehen (Reihenfolge des ersten Auftretens).
    werkstaetten: List[str] = []
    for ware in waren_liste:
        w = _werkstatt_von(ware)
        if w and w not in werkstaetten:
            werkstaetten.append(w)
    nr = 1
    for w in werkstaetten:
        schritte.append(_schritt(nr, "werkstatt", w, w,
                                 f"Werkstatt {w} bauen oder ausbauen, dort wird die "
                                 f"benoetigte Ware gefertigt."))
        nr += 1

    # 2. Je Ware: erst die Forschungsvoraussetzungen, dann die Ware selbst.
    for ware in waren_liste:
        w = _werkstatt_von(ware)
        for voraussetzung in _voraussetzungen_von(ware):
            schritte.append(_schritt(nr, "forschung", voraussetzung, w,
                                     f"{voraussetzung} erforschen, damit {ware} gefertigt "
                                     f"werden kann."))
            nr += 1
        schritte.append(_schritt(nr, "ware", ware, w,
                                 f"{ware} in {w} fertigen und ins Lager legen."))
        nr += 1

    # 3. Die Ausbildung der Einheit.
    schritte.append(_schritt(nr, "einheit", einheit, staette,
                             f"{einheit} in {staette} ausbilden, sobald die Waren im "
                             f"Lager sind."))
    return schritte


# --------------------------------------------------------------------------
# 3. Anzeige und offene Luecken
# --------------------------------------------------------------------------

def bestand_text(fehlt: dict) -> str:
    """Eine kurze deutsche Zeile fuer die Anzeige des Lagerbedarfs.

    Ein leeres (oder fehlendes) dict ergibt 'alles im Lager'. Sonst beginnt die Zeile mit
    'fehlt:' und nennt je Ware Soll/Ist (z. B. 'Kurzschwert 1/0'); ein reiner Zahlenwert
    gilt als Fehlmenge. Reiner Text, kein Fenster.
    """
    if not fehlt:
        return "alles im Lager"
    teile: List[str] = []
    for ware, wert in fehlt.items():
        if isinstance(wert, dict):
            teile.append(f"{ware} {_zahl(wert.get('soll', 0))}/{_zahl(wert.get('ist', 0))}")
        elif isinstance(wert, (tuple, list)) and len(wert) == 2:
            teile.append(f"{ware} {_zahl(wert[0])}/{_zahl(wert[1])}")
        else:
            teile.append(f"{ware} {_zahl(wert)}")
    return "fehlt: " + " · ".join(teile)


def offene_luecken() -> list[str]:
    """Was in der Datenlage fuer die Ausruestung noch fehlt (ehrliche Liste).

    Hier steht nur, wozu die Vorlage keinen Wert hergibt; es wird nichts geschaetzt. Der
    Warenweg selbst ist vollstaendig, daher betrifft es die Forschungsvoraussetzungen.
    """
    luecken: List[str] = []
    for ware, eintrag in _waren().items():
        text = str(eintrag.get("voraussetzung") or "")
        if "+" in text and not eintrag.get("voraussetzung_struktur"):
            luecken.append(
                f"Kombinierte Voraussetzung ohne Strukturfeld: {ware} verlangt {text}; "
                f"die Forschungsstufen werden aus dem Textfeld 'voraussetzung' gelesen.")
    luecken.append(
        "Die Forschungsvoraussetzung der Einheit selbst (data/units.json Feld "
        "'voraussetzung', z. B. 'Kriegskunst 3' fuer den Krieger) ist nicht Teil der "
        "Warenkette; sie gehoert zur Forschungspruefung.")
    return luecken
