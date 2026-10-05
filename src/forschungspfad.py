"""Forschungspfad -- die fachliche Frageschicht rund um die 21 Originalforschungen.

Dieses Modul ist die reine Datenschicht fuer die Frage, die Daniel am Forschungspanel
vermisst hat: **Was schaltet eine Forschung sichtbar frei, was ist jetzt erreichbar, was
ist gesperrt und warum, und in welcher Reihenfolge lohnt es sich?**

Es zeichnet nichts, oeffnet kein Fenster, wuerfelt nicht und importiert nur die
Standardbibliothek. Alle Werte kommen aus den vorhandenen Datendateien:

  * ``data/research.json`` -- je Forschung ``wirkung``, ``wirkung_struktur`` und
    ``voraussetzung`` (z. B. ``"Bibliothek 3 + Schmiedekunst 1"``).
  * ``data/items.json``    -- je Ware ``voraussetzung`` (z. B. ``"Waffentechnik 5"``)
    und ``benoetigt_von``.
  * ``data/units.json``    -- je Einheit ``gebaeude`` und ``waren``.
  * ``data/buildings.json``-- je Gebaeude ``voraussetzung`` (u. a. ``"Baukunst"``).

Was das Handbuch 2009 NICHT sagt (die empfohlene Reihenfolge, die Zahl fuer zwoelf der 21
Forschungen), steht ehrlich in :func:`offene_luecken` und wird nirgends erfunden.

Schreibweisen der Voraussetzungs-Begruendungen (beide wortgetreu aus dem Auftrag):
  * Gebaeude-Voraussetzung als ``Bedarf/Bestand``, z. B. ``"Bibliothek 3/1"``.
  * Forschungs-Voraussetzung als ``Bestand/Bedarf``, z. B. ``"Schmiedekunst 0/1"``.
  * :func:`blockiert` nennt dagegen nur den Bedarf, z. B. ``"Verteidigungsanlagen 5"``.
"""
from __future__ import annotations

import json
import re
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Der Gebaeudename der Bibliothek in der Vorlage (Gebaeude-Voraussetzung der Forschung).
_BIBLIO = "Bibliothek"

# Wortgrenzen fuer den exakten Namenstreffer (deutsche Umlaute inbegriffen, damit
# "Nähen" nicht in "Nähkunst" trifft).
_WORTZEICHEN = "0-9A-Za-z\u00c4\u00d6\u00dc\u00e4\u00f6\u00fc\u00df"
_RAND_VOR = "(?<![" + _WORTZEICHEN + "])"
_RAND_NACH = "(?![" + _WORTZEICHEN + "])"


# ------------------------------------------------------------------------------ Daten

def _wurzel() -> Path:
    """Projektwurzel finden -- im Quelltext und in der gepackten EXE.

    Es wird gesucht (erster Ort mit ``data/research.json`` gilt), nicht geraten.
    """
    kandidaten: List[Path] = []
    basis = getattr(sys, "_MEIPASS", None)
    if basis:
        kandidaten.append(Path(basis))
    kandidaten.append(Path(__file__).resolve().parent.parent)
    for kandidat in kandidaten:
        if (kandidat / "data" / "research.json").exists():
            return kandidat
    return kandidaten[-1]


def _lade(dateiname: str) -> Dict[str, Any]:
    return json.loads((_wurzel() / "data" / dateiname).read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def _forschungen() -> Dict[str, Dict[str, Any]]:
    return _lade("research.json").get("forschungen", {})


@lru_cache(maxsize=1)
def _waren() -> Dict[str, Dict[str, Any]]:
    return _lade("items.json").get("waren", {})


@lru_cache(maxsize=1)
def _einheiten() -> Dict[str, Dict[str, Any]]:
    return _lade("units.json").get("einheiten", {})


@lru_cache(maxsize=1)
def _gebaeude() -> List[Dict[str, Any]]:
    return _lade("buildings.json").get("gebaeude", [])


# -------------------------------------------------------------------------- Hilfsgriffe

def _pruefe_name(name: str) -> str:
    if name not in _forschungen():
        raise ValueError(f"Unbekannte Forschung: {name!r}")
    return name


def _stufe(staende: Dict[str, Any], name: str) -> int:
    """Stufe einer Forschung aus ``staende`` -- fehlend oder ungueltig zaehlt als 0."""
    if not isinstance(staende, dict):
        return 0
    roh = staende.get(name, 0)
    if isinstance(roh, dict):
        roh = roh.get("stufe", roh.get("level", 0))
    elif hasattr(roh, "stufe"):
        roh = roh.stufe
    elif hasattr(roh, "level"):
        roh = roh.level
    try:
        n = int(roh)
    except (TypeError, ValueError):
        return 0
    return n if n > 0 else 0


def _parse_voraussetzung(text: Any, for_name: str) -> List[Dict[str, Any]]:
    """Zerlegt ``"Bibliothek 3 + Schmiedekunst 1"`` in Einzelvoraussetzungen."""
    if text is None:
        return []
    text = str(text).strip()
    if text == "" or text.lower() in ("keine", "null", "-"):
        return []
    ausgabe: List[Dict[str, Any]] = []
    for teil in text.split("+"):
        teil = teil.strip()
        if not teil:
            continue
        treffer = re.match(r"^(?P<name>.+?)\s+(?P<stufe>\d+)$", teil)
        if not treffer:
            raise ValueError(f"Voraussetzung {teil!r} von {for_name!r} nicht lesbar.")
        pname = treffer.group("name").strip()
        stufe = int(treffer.group("stufe"))
        art = "bibliothek" if pname == _BIBLIO else "forschung"
        ausgabe.append({"art": art, "was": pname, "stufe": stufe})
    return ausgabe


def _nennt(text: Any, name: str) -> bool:
    """True, wenn ``name`` als eigenstaendiges Wort in ``text`` steht (kein Teiltreffer)."""
    if not text:
        return False
    return re.search(_RAND_VOR + re.escape(name) + _RAND_NACH, str(text)) is not None


@lru_cache(maxsize=None)
def _bib_bedarf(name: str) -> int:
    """Niedrigste Bibliotheksstufe, ab der ``name`` ueberhaupt erreichbar ist.

    Beruecksichtigt auch Forschungsvoraussetzungen (z. B. Kampfmagie -> Magiekunde 4 ->
    Bibliothek 6). So sortiert die Empfehlung sinnvoll und nicht nur nach dem direkten Wert.
    """
    bedarf = 0
    for p in voraussetzung(name):
        if p["art"] == "bibliothek":
            bedarf = max(bedarf, int(p["stufe"]))
        else:
            bedarf = max(bedarf, _bib_bedarf(p["was"]))
    return bedarf


# ------------------------------------------------------------------ oeffentliche Schicht

def voraussetzung(name: str) -> List[Dict[str, Any]]:
    """Die Voraussetzungen einer Forschung als Liste von Einzelbedingungen.

    Je Bedingung ein Woerterbuch ``{'art': 'bibliothek'|'forschung', 'was': Name, 'stufe': int}``.
    ``"Bibliothek 3 + Schmiedekunst 1"`` ergibt zwei Eintraege. Eine leere Voraussetzung
    ergibt eine leere Liste. Ein unbekannter Forschungsname loest ``ValueError`` aus.
    """
    _pruefe_name(name)
    eintrag = _forschungen()[name]
    text = eintrag.get("voraussetzung")
    if text is None:
        struktur = eintrag.get("voraussetzung_struktur") or []
        ausgabe: List[Dict[str, Any]] = []
        for p in struktur:
            art = "bibliothek" if p.get("art") == "gebaeude" else "forschung"
            ausgabe.append({"art": art, "was": p.get("name"), "stufe": int(p.get("stufe", 0))})
        return ausgabe
    return _parse_voraussetzung(text, name)


def erfuellt(name: str, staende: Dict[str, Any], bibliothek_stufe: int
             ) -> Tuple[bool, str]:
    """Sind die Voraussetzungen erfuellt? ``(ja/nein, Begruendung)``.

    ``staende`` ist ``{Forschungsname: Stufe}``. Bei ``False`` nennt die Begruendung **jede**
    unerfuellte Bedingung mit Soll und Ist -- Gebaeude als ``Bedarf/Bestand``
    (z. B. ``"Bibliothek 3/1"``), Forschung als ``Bestand/Bedarf`` (z. B. ``"Schmiedekunst 0/1"``).
    """
    _pruefe_name(name)
    bib = int(bibliothek_stufe or 0)
    fehlt: List[str] = []
    for p in voraussetzung(name):
        soll = int(p["stufe"])
        if p["art"] == "bibliothek":
            ist = bib
            if ist < soll:
                fehlt.append(f"Bibliothek {soll}/{ist}")
        else:
            ist = _stufe(staende, p["was"])
            if ist < soll:
                fehlt.append(f"{p['was']} {ist}/{soll}")
    if not fehlt:
        return True, f"{name} ist erforschbar: alle Voraussetzungen erfuellt."
    return False, f"{name} ist gesperrt: es fehlen " + ", ".join(fehlt) + "."


def jetzt_moeglich(staende: Dict[str, Any], bibliothek_stufe: int) -> List[str]:
    """Forschungen, deren Voraussetzungen erfuellt sind und die noch auf Stufe 0 stehen.

    Sortiert nach noetiger Bibliotheksstufe, dann nach Name.
    """
    bib = int(bibliothek_stufe or 0)
    moeglich: List[str] = []
    for name in _forschungen():
        if _stufe(staende, name) != 0:
            continue
        ok, _grund = erfuellt(name, staende, bib)
        if ok:
            moeglich.append(name)
    moeglich.sort(key=lambda n: (_bib_bedarf(n), n))
    return moeglich


def blockiert(staende: Dict[str, Any], bibliothek_stufe: int) -> List[Dict[str, Any]]:
    """Jede noch nicht erforschte Forschung, die noch gesperrt ist.

    Je Eintrag ``{'name': ..., 'fehlt': [Begruendungen]}`` -- jede Begruendung nennt eine
    unerfuellte Voraussetzung mit ihrem Bedarf, z. B. ``"Verteidigungsanlagen 5"``.
    """
    bib = int(bibliothek_stufe or 0)
    ausgabe: List[Dict[str, Any]] = []
    for name in _forschungen():
        if _stufe(staende, name) != 0:
            continue
        ok, _grund = erfuellt(name, staende, bib)
        if ok:
            continue
        fehlt: List[str] = []
        for p in voraussetzung(name):
            soll = int(p["stufe"])
            if p["art"] == "bibliothek":
                if bib < soll:
                    fehlt.append(f"Bibliothek {soll}")
            elif _stufe(staende, p["was"]) < soll:
                fehlt.append(f"{p['was']} {soll}")
        ausgabe.append({"name": name, "fehlt": fehlt})
    ausgabe.sort(key=lambda e: (_bib_bedarf(e["name"]), e["name"]))
    return ausgabe


def wirkung_text(name: str) -> str:
    """Die sichtbare Wirkung als deutscher Satz.

    Wortlaut aus ``data/research.json`` (Feld ``wirkung``). Wo die Struktur einen Wert
    ``pro_stufe_prozent`` hat, wird die gemessene Zahl angehaengt (``"... +10 % je Stufe"``).
    Wo das Handbuch keine Zahl nennt, bleibt der Satz unveraendert -- es wird nichts erfunden.
    """
    _pruefe_name(name)
    eintrag = _forschungen()[name]
    wirkung = (eintrag.get("wirkung") or "").strip()
    struktur = eintrag.get("wirkung_struktur") or {}
    prozent = struktur.get("pro_stufe_prozent")
    if prozent is None:
        return wirkung
    return f"{wirkung} +{int(prozent)} % je Stufe"


def schaltet_frei(name: str) -> Dict[str, List[str]]:
    """Was diese Forschung sichtbar freischaltet -- nur aus den Datendateien abgeleitet.

    * ``waren``    -- Waren, die ``name`` als Voraussetzung nennen (z. B. ``"Waffentechnik 5"``).
    * ``einheiten``-- Einheiten, die eine dieser Waren brauchen (Feld ``waren``).
    * ``gebaeude`` -- Gebaeude, die ``name`` als Voraussetzung nennen (z. B. ``"Baukunst"``).

    Der Abgleich ist ein exakter Namenstreffer auf den Forschungsnamen; es wird nichts geraten.
    """
    _pruefe_name(name)
    waren = sorted(w for w, e in _waren().items() if _nennt(e.get("voraussetzung"), name))
    einheiten = sorted(
        e for e, daten in _einheiten().items()
        if any(w in waren for w in (daten.get("waren") or []))
    )
    gebaeude = sorted(
        g.get("name") for g in _gebaeude()
        if g.get("name") and _nennt(g.get("voraussetzung"), name)
    )
    return {"waren": waren, "einheiten": einheiten, "gebaeude": gebaeude}


# Empfohlene Reihenfolge -- NICHT im Handbuch belegt, sondern eine begruendete Setzung.
# Die ersten fuenf sind bewusst Wirtschaft und Tuer-Oeffner zuerst, Kampf danach:
#   1 Baukunst         -- schaltet laut buildings.json.regeln fast alle Gebaeude frei und
#                         ist die Voraussetzung der Verteidigungsforschung.
#   2 Felderwirtschaft -- belegter Dauerbrenner: +10 % Nahrung je Stufe.
#   3 Schmiedekunst    -- belegte +5 % auf Waffen/Ruestungen UND Tor zu Waffentechnik/Ruestungsbau.
#   4 Kriegskunst      -- schaltet laut units.json die Kampfeinheiten frei (Kaempfer ab Stufe 1).
#   5 Heimlichkeit     -- schaltet laut units.json die Kundschafter frei (Gauner ab Stufe 1).
_PRIORITAET: List[str] = [
    "Baukunst",
    "Felderwirtschaft",
    "Schmiedekunst",
    "Kriegskunst",
    "Heimlichkeit",
    "Forstwirtschaft",
    "Steinbruch",
    "Minenarbeit",
    "Tierhaltung",
    "G\u00f6tterkunde",
    "N\u00e4hkunst",
    "Waffentechnik",
    "R\u00fcstungsbau",
    "Bogenbau",
    "N\u00e4hen",
    "Wagenbau",
    "Heilkunde",
    "Verteidigungsanlagen",
    "Mauerbau",
    "Magiekunde",
    "Kampfmagie",
]


def empfohlene_reihenfolge(bibliothek_stufe: int) -> List[str]:
    """Ein sinnvoller Forschungsplan fuer die gegebene Bibliotheksstufe.

    Enthaelt alle Forschungen, deren Bibliothekstor (auch ueber Forschungsvoraussetzungen,
    z. B. Kampfmagie -> Magiekunde 4) offen ist -- Vorbedingungen stehen vor ihren Folgen.
    **VORSCHLAG**, nicht im Handbuch belegt (siehe :func:`offene_luecken`).
    """
    bib = int(bibliothek_stufe or 0)
    return [n for n in _PRIORITAET if n in _forschungen() and _bib_bedarf(n) <= bib]


def offene_luecken() -> List[str]:
    """Alles, wovon das Handbuch schweigt -- ehrlich benannt statt erfunden."""
    luecken: List[str] = [
        "VORSCHLAG: Die Reihenfolge aus empfohlene_reihenfolge() ist NICHT im Handbuch "
        "belegt. Sie ist eine begruendete Setzung des Remakes; die Gruende fuer die ersten "
        "fuenf stehen als Kommentar an _PRIORITAET.",
        "VORSCHLAG: schaltet_frei() leitet Einheiten NUR ueber die freigeschalteten Waren ab. "
        "Einheiten, die eine Forschung direkt nennen (z. B. Gauner: Heimlichkeit 1 in "
        "data/units.json), erscheinen hier nicht.",
    ]
    for name in _forschungen():
        struktur = _forschungen()[name].get("wirkung_struktur") or {}
        if struktur.get("pro_stufe_prozent") is None:
            luecken.append(
                f"Fuer '{name}' nennt das Handbuch keine Zahl; wirkung_text() zeigt nur den "
                "Wortlaut und erfindet keinen Prozentwert."
            )
    return luecken
