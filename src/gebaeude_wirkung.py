"""
Nebelseetal Remake — Wirkungen der 20 Originalgebaeude (Paket W4b-5, 04.10.2026).

Bis hierher lagen die Wirkungen in fuenf **erfundenen** Gebaeuden (`main.BUILDINGS`: Haus,
Bibliothek, Kaserne, Wachturm, Portal) und wirkten global. Die 20 belegten Originalgebaeude
standen zwar auf der Siedlungskarte, taten aber ausser der Rohstoffproduktion (Paket W4b-4)
nichts. Dieses Modul leitet ihre Wirkungen aus den bebauten FELDERN der Siedlungskarten ab.

Belegte Regeln (Handbuch 2009, Seiten 7-12):
  * Siedlergrenze **10 je Siedlung, +5 je Haus**; **1 neuer Siedler je Stunde** und Siedlung;
    Heilkunde **+10 % Siedlerproduktion je Stufe**.
  * Forschung braucht eine **Bibliothek**.
  * Ausbildung: **Kriegerakademie** -> Kampfeinheiten, **Diebesgilde** -> Kundschafter,
    **Stellmacher** -> Karren und Belagerungswaffen. Das steht je Einheit in
    `data/units.json` (Feld "gebaeude"); hoehere Stufe = schnellere Ausbildung.
  * **Verteidigungswall**: 10 Stufen mit Schwellenwerten; Kriegspunkte = Stufe hoch drei.

NICHT belegt und darum in `data/gebaeude_wirkung.json` als VORSCHLAG gekennzeichnet:
  * die ANZAHL der Ausbaustufen von Bibliothek und den drei Ausbildungsstaetten,
  * die Hoehe des Verteidigungsboni (kommt weiterhin aus `bonus_system.get_defense_bonus`).

Das Modul zeichnet nichts, erfindet keinen Wert und veraendert kein anderes Modul.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import einheiten
import gelaende

WURZEL = Path(__file__).resolve().parent.parent
WIRKUNGSDATEI = WURZEL / "data" / "gebaeude_wirkung.json"

# Ausbaustufen liegen in der Siedlung je FELD: {"Feldindex": Stufe}. Ein bebautes Feld ohne
# Eintrag gilt als Stufe 1 (so bleiben aeltere Spielstaende lesbar).
STANDARD_STUFE = 1


@lru_cache(maxsize=1)
def regeln() -> Dict[str, Any]:
    """Die belegten Wirkungszahlen aus ``data/gebaeude_wirkung.json``."""
    return json.loads(WIRKUNGSDATEI.read_text(encoding="utf-8"))


def luecken() -> Dict[str, str]:
    """Was an den Wirkungen noch fehlt (ehrliche Liste, fuer Anzeige und Bericht)."""
    return dict(regeln().get("offene_luecken", {}))


# --------------------------------------------------------------------------
# Hilfsgriffe (arbeiten mit Objekten UND dicts — wie wirtschaft.py)
# --------------------------------------------------------------------------

def _feld(objekt, name, vorgabe=None):
    if isinstance(objekt, dict):
        return objekt.get(name, vorgabe)
    return getattr(objekt, name, vorgabe)


def _kennung(gebaeude) -> Optional[str]:
    """Die Kennung eines Gebaeudes — akzeptiert Kennung UND Anzeigename."""
    if not gebaeude:
        return None
    return gelaende.finde_gebaeude(gebaeude)


def _bauten(siedlung) -> Dict[str, str]:
    return dict(_feld(siedlung, "bauten") or {})


# --------------------------------------------------------------------------
# 1. Bestand: was steht auf den Karten?
# --------------------------------------------------------------------------

def bestand(siedlungen) -> Dict[str, int]:
    """Anzahl je Gebaeudeart ueber alle Siedlungen (Kennung -> Anzahl)."""
    zaehlung: Dict[str, int] = {}
    for siedlung in siedlungen or []:
        for _feld_index, gebaut in _bauten(siedlung).items():
            kennung = _kennung(gebaut)
            if kennung:
                zaehlung[kennung] = zaehlung.get(kennung, 0) + 1
    return zaehlung


def anzahl(siedlungen, gebaeude) -> int:
    """Wie oft ein Gebaeude insgesamt steht (0 = nicht gebaut)."""
    kennung = _kennung(gebaeude)
    if not kennung:
        return 0
    return bestand(siedlungen).get(kennung, 0)


def stufe_von_feld(siedlung, feld) -> int:
    """Die Ausbaustufe des Gebaeudes auf einem Feld (fehlender Eintrag = Stufe 1)."""
    stufen = _feld(siedlung, "stufen") or {}
    try:
        return int(stufen.get(str(feld), STANDARD_STUFE))
    except (TypeError, ValueError):
        return STANDARD_STUFE


def gebaeude_stufe(siedlung, gebaeude) -> int:
    """Hoechste Ausbaustufe eines Gebaeudes in EINER Siedlung (0 = nicht gebaut)."""
    kennung = _kennung(gebaeude)
    if not kennung:
        return 0
    beste = 0
    for feld_index, gebaut in _bauten(siedlung).items():
        if _kennung(gebaut) == kennung:
            beste = max(beste, stufe_von_feld(siedlung, feld_index))
    return beste


def max_stufe(gebaeude) -> Optional[int]:
    """Wie weit sich ein Gebaeude ausbauen laesst — None, wenn kein Ausbau belegt ist."""
    kennung = _kennung(gebaeude)
    tabelle = regeln().get("ausbaustufen_hoechstens", {})
    if not kennung:
        return None
    wert = tabelle.get(kennung)
    return int(wert) if isinstance(wert, (int, float)) else None


def stufen_name(gebaeude, stufe: int) -> str:
    """Der Originalname einer Ausbaustufe (beim Wall Erdwall, Steinwall, ...), sonst 'Stufe n'."""
    kennung = _kennung(gebaeude)
    eintrag = _wallstufen().get(int(stufe)) if kennung == "verteidigungswall" else None
    return eintrag["name"] if eintrag and eintrag.get("name") else f"Stufe {int(stufe)}"


# --------------------------------------------------------------------------
# 2. Bevoelkerung: Haus hebt die Siedlergrenze
# --------------------------------------------------------------------------

def siedlergrenze_je_siedlung(siedlung) -> int:
    """10 Siedler je Siedlung + 5 je Haus (Handbuch Seite 11)."""
    r = regeln()["bevoelkerung"]
    return int(r["grund_je_siedlung"]) + int(r["je_haus"]) * anzahl([siedlung], "haus")


def bevoelkerungsgrenze(siedlungen) -> int:
    """Die Gesamtgrenze ueber alle Siedlungen.

    Jede Siedlung traegt 10 Siedler bei, jedes Haus darin 5. Ohne Siedlung gilt der belegte
    Startwert (10 Siedler, Handbuch Seite 7) — sonst waere der Spielstart unbewohnbar.
    """
    liste = list(siedlungen or [])
    if not liste:
        return int(regeln()["bevoelkerung"]["startwert_ohne_siedlung"])
    return sum(siedlergrenze_je_siedlung(s) for s in liste)


def siedler_zuwachs_pro_stunde(siedlungen, forschung_level: Optional[Dict[str, int]] = None) -> float:
    """Neue Siedler je Stunde: 1 je Siedlung, mit Heilkunde +10 % je Stufe."""
    liste = list(siedlungen or [])
    if not liste:
        return 0.0
    r = regeln()["bevoelkerung"]
    stufe = int((forschung_level or {}).get("heilkunde", 0) or 0)
    faktor = 1.0 + int(r["heilkunde_prozent_je_stufe"]) / 100.0 * stufe
    return round(float(r["siedler_je_stunde"]) * len(liste) * faktor, 4)


# --------------------------------------------------------------------------
# 3. Forschung: braucht eine Bibliothek
# --------------------------------------------------------------------------

def bibliothek_stufe(siedlungen) -> int:
    """Hoechste Bibliotheksstufe ueber alle Siedlungen (0 = keine Bibliothek)."""
    return max((gebaeude_stufe(s, "bibliothek") for s in (siedlungen or [])), default=0)


def hat_bibliothek(siedlungen) -> bool:
    return bibliothek_stufe(siedlungen) > 0


def forschung_erlaubt(siedlungen) -> Tuple[bool, str]:
    """(ja/nein, Begruendung) — die Begruendung ist fuer die Anzeige gedacht."""
    stufe = bibliothek_stufe(siedlungen)
    if stufe <= 0:
        return False, "Forschung braucht eine Bibliothek auf einer Siedlungskarte."
    return True, f"Bibliothek vorhanden (Stufe {stufe})."


# --------------------------------------------------------------------------
# 4. Ausbildung: welches Gebaeude bildet welche Einheit aus
# --------------------------------------------------------------------------

def ausbildungsgebaeude(einheit) -> Optional[str]:
    """Die Ausbildungsstaette einer Einheit — aus `data/units.json` (Feld 'gebaeude')."""
    eintrag = einheiten.alle().get(einheit)
    if not eintrag:
        return None
    return _kennung(eintrag.get("gebaeude"))


def ausbildungsstaette(siedlungen, einheit) -> Tuple[bool, Optional[str], int]:
    """(steht die Staette?, Kennung, Stufe) fuer eine Einheit.

    Ohne bekannte Einheit oder ohne Gebaeudeangabe kommt (False, None, 0) zurueck — hier
    wird nichts geschaetzt.
    """
    kennung = ausbildungsgebaeude(einheit)
    if not kennung:
        return False, None, 0
    stufe = max((gebaeude_stufe(s, kennung) for s in (siedlungen or [])), default=0)
    return stufe > 0, kennung, stufe


def ausbildbare_einheiten(siedlungen, forschung_level: Optional[Dict[str, int]] = None
                          ) -> Tuple[List[str], List[str]]:
    """(moegliche, gesperrte) Einheiten nach der Ausbildungsstaette.

    Geprueft wird nur die Staette. Die Forschungsvoraussetzung je Einheit (z. B. Kriegskunst
    fuer den Kaempfer) wird noch NICHT geprueft: im Spiel stehen die 18 erfundenen
    Forschungsgebiete, die Originalnamen fehlen (Paket W4b-6).
    """
    moeglich: List[str] = []
    gesperrt: List[str] = []
    for name in einheiten.namen():
        da, _kennung_, _stufe = ausbildungsstaette(siedlungen, name)
        (moeglich if da else gesperrt).append(name)
    return moeglich, gesperrt


# --------------------------------------------------------------------------
# 5. Verteidigungswall
# --------------------------------------------------------------------------

def wall_stufe(siedlungen) -> int:
    """Die hoechste Wallstufe ueber alle Siedlungen (0 = kein Wall)."""
    return max((gebaeude_stufe(s, "verteidigungswall") for s in (siedlungen or [])), default=0)


@lru_cache(maxsize=1)
def _wallstufen() -> Dict[int, Dict[str, Any]]:
    """Die 10 belegten Wallstufen aus `data/buildings.json`, nach Stufe geordnet."""
    geb = gelaende.alle_gebaeude().get("verteidigungswall") or {}
    out: Dict[int, Dict[str, Any]] = {}
    for eintrag in geb.get("stufen", []):
        try:
            out[int(eintrag["stufe"])] = dict(eintrag)
        except (KeyError, TypeError, ValueError):
            continue
    return out


def wall_eintrag(stufe: int) -> Optional[Dict[str, Any]]:
    return _wallstufen().get(int(stufe))


def wall_name(stufe: int) -> Optional[str]:
    eintrag = wall_eintrag(stufe)
    return eintrag.get("name") if eintrag else None


def wall_schwelle(stufe: int) -> Dict[str, Optional[int]]:
    """Die Schwellenwerte der Vorrunde: {'fusstruppen': x, 'belagerungswaffen': y|None}."""
    eintrag = wall_eintrag(stufe)
    if not eintrag:
        return {"fusstruppen": None, "belagerungswaffen": None}
    return {
        "fusstruppen": eintrag.get("schwellenwert_fussttruppen"),
        "belagerungswaffen": eintrag.get("schwellenwert_belagerungswaffen"),
    }


def wall_kriegspunkte(stufe: int) -> int:
    """Belegte Originalregel: Ausbaustufe hoch drei (Palisade Stufe 4 = 64)."""
    return int(stufe) ** 3


def wall_beschreibung(siedlungen) -> str:
    """Die Verteidigung in Worten — fuer die Anzeige im Spiel."""
    stufe = wall_stufe(siedlungen)
    if stufe <= 0:
        return "kein Verteidigungswall"
    schwelle = wall_schwelle(stufe)
    bel = schwelle["belagerungswaffen"]
    teil = f"{wall_name(stufe)} (Stufe {stufe})"
    teil += f", Schwellenwert Fusstruppen {schwelle['fusstruppen']}"
    if bel is not None:
        teil += f", Belagerungswaffen {bel}"
    teil += f", Kriegspunkte {wall_kriegspunkte(stufe)}"
    return teil


# --------------------------------------------------------------------------
# 6. Anzeige
# --------------------------------------------------------------------------

def wirkung_text(siedlung) -> str:
    """Die Wirkungen EINER Siedlung in einer Zeile (fuer die Uebersicht)."""
    teile = [f"Siedlergrenze {siedlergrenze_je_siedlung(siedlung)}"]
    haeuser = anzahl([siedlung], "haus")
    if haeuser:
        teile.append(f"{haeuser} Haus/Haeuser")
    bib = gebaeude_stufe(siedlung, "bibliothek")
    if bib:
        teile.append(f"Bibliothek Stufe {bib} (Forschung frei)")
    staetten = [gelaende.gebaeude_name(k) for k in ("kriegerakademie", "diebesgilde", "stellmacher")
                if gebaeude_stufe(siedlung, k) > 0]
    if staetten:
        teile.append("Ausbildung: " + ", ".join(staetten))
    wall = gebaeude_stufe(siedlung, "verteidigungswall")
    if wall:
        teile.append(f"Wall {wall_name(wall)} (Stufe {wall})")
    return " · ".join(teile)


def uebersicht(siedlungen) -> Dict[str, Any]:
    """Alles, was das Spiel ueber die Gebaeudewirkungen wissen muss — in einer Struktur."""
    return {
        "bestand": bestand(siedlungen),
        "bevoelkerungsgrenze": bevoelkerungsgrenze(siedlungen),
        "siedler_zuwachs_pro_stunde": siedler_zuwachs_pro_stunde(siedlungen),
        "bibliothek_stufe": bibliothek_stufe(siedlungen),
        "forschung_erlaubt": forschung_erlaubt(siedlungen)[0],
        "wall_stufe": wall_stufe(siedlungen),
        "wall_beschreibung": wall_beschreibung(siedlungen),
        "luecken": luecken(),
    }
