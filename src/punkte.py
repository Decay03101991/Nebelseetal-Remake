"""
Nebelseetal Remake — Punkte, Rangliste, Goetterschutz und Sieg/Niederlage (Paket W6, 04.10.2026).

Belegte Originalregeln (Handbuch 2009, Seiten 3-6, nachgeprueft in
``docs/original/ORIGINAL_Kampf_und_Punkte.md``):

  * Forschungspunkte = Summe aller Forschungsstufen **hoch drei**
    ("Fuer jede Forschung die Du erlangt hast, wird die Forschungsstufe hoch drei genommen.
     Die so gewonnenen Werte werden anschliessend addiert." — Handbuch S. 3).
  * Kriegspunkte = fester Punktewert je Einheit (Handbuch S. 5)
    **plus** Verteidigungsanlagen: **Ausbaustufe hoch drei**
    ("Palisade (Ausbaustufe 4) = 64 Kriegspunkte (4*4*4=64)" — Handbuch S. 5).
  * Gesamtpunktzahl = **(Kriegspunkte + Forschungspunkte) / 2**
    ("Die Gesamtpunktzahl besteht aus der Summe von den Kriegs- und Forschungspunkten.
     Das Ergebnis wird dann durch zwei geteilt." — Handbuch S. 5/6).
  * Rufpunkte gehen **nicht** in die Gesamtpunktzahl ein; sie entscheiden nur bei
    Punktgleichheit (hoeherer Ruf zuerst, danach frueheres Anmeldedatum — Handbuch S. 6).
  * Goetterschutz: neue Spieler sind die **ersten sieben Tage** geschuetzt und nicht
    angreifbar (Handbuch S. 6). Der Schutz endet frueher mit dem ersten Kriegspunkt — das
    bildet dieser Baustein NICHT ab (Vorschlag, siehe unten).

NICHT belegt — als VORSCHLAG gekennzeichnet (siehe ``vorschlaege()``):
  * die Rundung der Gesamtpunktzahl bei ungerader Summe,
  * eine Sieg- und eine Niederlagebedingung (das Handbuch nennt **keine**),
  * der Startzeitpunkt des Goetterschutzes.

Das Modul rechnet nur, zeichnet nichts und aendert keine andere Datei.
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple

import einheiten as _einheiten

# --------------------------------------------------------------------------
# Belegte Konstanten
# --------------------------------------------------------------------------

# Handbuch S. 6: "die ersten sieben Tage".
GOETTERSCHUTZ_TAGE = 7
SEKUNDEN_JE_TAG = 86400

# VORSCHLAG: Zielpunktzahl fuer den Sieg. Das Handbuch nennt keine Siegbedingung; 300 ist die
# belegte Schutzgrenze (Handbuch S. 6 "Spieler ueber 300 Punkten befinden sich ausserhalb des
# Goetterschutzes") und darum ein sichtbarer Meilenstein.
VORSCHLAG_ZIEL_PUNKTE = 300


# --------------------------------------------------------------------------
# Kleine Griffe
# --------------------------------------------------------------------------

def _stufe(wert) -> int:
    """Eine nicht-negative Ausbaustufe; alles Unbrauchbare gilt als 0."""
    try:
        return max(0, int(wert))
    except (TypeError, ValueError):
        return 0


def _anzahl(wert) -> int:
    try:
        return max(0, int(wert))
    except (TypeError, ValueError):
        return 0


def _ke_einheit(name) -> int:
    """Kriegspunkte je Stueck aus `data/units.json` (None = gibt keine, z. B. Karren)."""
    wert = _einheiten.kriegspunkte(name)
    return int(wert) if wert is not None else 0


# --------------------------------------------------------------------------
# 1. Forschungspunkte
# --------------------------------------------------------------------------

def forschungspunkte(forschungsstaende: Optional[dict]) -> int:
    """Summe der Forschungsstufen hoch drei (Handbuch S. 3).

    ``forschungsstaende`` bildet Forschungsgebiet -> Stufe ab. Fehlende oder
    unbrauchbare Stufen zaehlen als 0. Stufe 0..3 ergeben 0, 1, 8, 27.
    """
    summe = 0
    for stufe in (forschungsstaende or {}).values():
        summe += _stufe(stufe) ** 3
    return summe


# --------------------------------------------------------------------------
# 2. Kriegspunkte
# --------------------------------------------------------------------------

def kriegspunkte(einheiten: Optional[dict], wall_stufe: int) -> int:
    """Punkte aus Einheiten (fester Wert je Einheit) plus Wall (Stufe hoch drei).

    ``einheiten`` bildet Einheitenname -> Anzahl ab. Einheiten ohne Punktewert
    (Handelskarawanen, Siedlerkarren — Handbuch: "Punktewert: -") zaehlen 0.
    """
    summe = 0
    for name, anzahl in (einheiten or {}).items():
        summe += _ke_einheit(name) * _anzahl(anzahl)
    summe += _stufe(wall_stufe) ** 3
    return summe


# --------------------------------------------------------------------------
# 3. Gesamtpunktzahl
# --------------------------------------------------------------------------

def gesamtpunkte(forschungsstaende: Optional[dict], einheiten: Optional[dict],
                 wall_stufe: int) -> int:
    """(Kriegspunkte + Forschungspunkte) / 2 (Handbuch S. 5/6).

    VORSCHLAG: Das Handbuch nennt keine Rundung. Bei ungerader Summe wird
    **abgerundet** (``// 2``); der Rest 0.5 faellt weg. Begruendung in ``vorschlaege()``.
    """
    fp = forschungspunkte(forschungsstaende)
    kp = kriegspunkte(einheiten, wall_stufe)
    return (fp + kp) // 2


# --------------------------------------------------------------------------
# 4. Rufpunkte
# --------------------------------------------------------------------------

def rufpunkte(ruf) -> int:
    """Der Ruf als Zahl. Er geht NICHT in die Gesamtpunktzahl ein (Handbuch S. 6)."""
    return _stufe(ruf)


# --------------------------------------------------------------------------
# 5. Rangliste
# --------------------------------------------------------------------------

def _hole(eintrag, namen, vorgabe=0):
    if isinstance(eintrag, dict):
        for name in namen:
            if eintrag.get(name) is not None:
                return eintrag.get(name)
    return vorgabe


def rangliste(spieler: Optional[list], jetzt: Optional[float] = None) -> List[Dict[str, Any]]:
    """Sortierte Ruhmeshalle.

    Reihenfolge nach Handbuch S. 6: hoechste Gesamtpunktzahl zuerst, bei
    Gleichstand der hoehere Ruf, danach das fruehere Anmeldedatum. ``jetzt`` wird
    angenommen, aendert die belegte Rangfolge aber nicht (nur fuer kuenftige
    Schutzanzeige vorhanden). Jeder Eintrag traegt mindestens ``name`` und ``punkte``.
    """
    liste = [p for p in (spieler or []) if p is not None]

    def schluessel(p):
        punkte = _anzahl(_hole(p, ("punkte", "gesamtpunkte", "gesamt")))
        ruf = _anzahl(_hole(p, ("rufpunkte", "ruf")))
        angemeldet = _hole(p, ("angemeldet", "seit", "registriert"), vorgabe=0.0)
        try:
            angemeldet = float(angemeldet)
        except (TypeError, ValueError):
            angemeldet = 0.0
        name = (_hole(p, ("name",), vorgabe="") or "")
        # Punkte absteigend, Ruf absteigend, Anmeldedatum aufsteigend (frueher oben); der Name
        # macht die Ordnung stabil, wenn alles gleich ist.
        return (-punkte, -ruf, angemeldet, str(name))

    ergebnis: List[Dict[str, Any]] = []
    for index, p in enumerate(sorted(liste, key=schluessel), start=1):
        punkte = _anzahl(_hole(p, ("punkte", "gesamtpunkte", "gesamt")))
        ruf = _anzahl(_hole(p, ("rufpunkte", "ruf")))
        angemeldet = _hole(p, ("angemeldet", "seit", "registriert"), vorgabe=None)
        ergebnis.append({
            "rang": index,
            "name": _hole(p, ("name",), vorgabe=str(p)),
            "punkte": punkte,
            "ruf": ruf,
            "angemeldet": angemeldet,
        })
    return ergebnis


# --------------------------------------------------------------------------
# 6. Goetterschutz
# --------------------------------------------------------------------------

def goetterschutz_tage() -> int:
    """Die belegten sieben Tage Schutz (Handbuch S. 6)."""
    return GOETTERSCHUTZ_TAGE


def goetterschutz_aktiv(seit: float, jetzt: float) -> bool:
    """Laeuft der Schutz noch? ``seit`` und ``jetzt`` sind Zeitstempel in Sekunden.

    Aktiv, solange weniger als sieben mal 86400 Sekunden vergangen sind. Mit
    Ablauf der siebten Tage (oder spaeter) ist der Schutz vorbei. Ein
    Startzeitpunkt in der Zukunft gilt als nicht aktiv.
    """
    try:
        seit = float(seit)
        jetzt = float(jetzt)
    except (TypeError, ValueError):
        return False
    alter = jetzt - seit
    if alter < 0:
        return False
    return alter < GOETTERSCHUTZ_TAGE * SEKUNDEN_JE_TAG


# BELEGT (Handbuch 2009, Seite 6, Z. 221-228; Registerpunkt 41): Der EINGESCHRAENKTE
# Goetterschutz bis 299 Punkte. Woertlich: "Spieler bis maximal 299 Punkte befinden sich im
# eingeschraenkten Goetterschutz. Innerhalb des eingeschraenkten Goetterschutzes kannst Du nur
# Spieler angreifen, die im Bereich 'eigene Punktzahl +/- 20%' liegen." Und: "Ein Angriff ueber
# die Goetterschutzgrenze von 299 Punkten hinweg ist in keine Richtung moeglich!"
def _als_zahl(wert: Any, vorgabe: float = 0.0) -> float:
    """Robuster Zahlwert (None, Text, Bool -> vorgabe), wie in den anderen Modulen."""
    try:
        return float(wert)
    except (TypeError, ValueError):
        return float(vorgabe)


GOETTERSCHUTZ_PUNKTGRENZE = 299
GOETTERSCHUTZ_BANDBREITE = 0.20


def goetterschutz_band(punkte_eigene: Any) -> Tuple[int, int]:
    """Erlaubter Zielbereich der eigenen Punktzahl (belegt: +/- 20 Prozent, hoechstens 299).

    Untergrenze aufgerundet, Obergrenze abgerundet - so trifft das Beispiel des Handbuchs:
    299 Punkte duerfen 240 bis 299 angreifen. Wer selbst ueber 299 liegt, hat keinen Schutz
    und keinen Band (dann entscheidet allein die Grenze in `angreifbar`).
    """
    eigene = max(0.0, _als_zahl(punkte_eigene))
    unten = int(math.ceil(eigene * (1.0 - GOETTERSCHUTZ_BANDBREITE)))
    oben = int(math.floor(eigene * (1.0 + GOETTERSCHUTZ_BANDBREITE)))
    return unten, min(oben, GOETTERSCHUTZ_PUNKTGRENZE)


def angreifbar(punkte_angreifer: Any, punkte_ziel: Any) -> Tuple[bool, str]:
    """Darf A den B angreifen? (belegt, Handbuch Seite 6, Z. 221-228; Registerpunkt 41)

    Regeln, in dieser Reihenfolge:
      1. Liegt einer der beiden ueber 299 und der andere nicht, ist KEIN Angriff moeglich -
         in keine Richtung (die Grenze darf nicht ueberschritten werden).
      2. Sind BEIDE ueber 299, gibt es keinen Schutz; der Angriff ist erlaubt.
      3. Sind beide bei 299 oder darunter, muss das Ziel im Band +/- 20 Prozent der eigenen
         Punktzahl liegen.

    Rueckgabe: (erlaubt, Begruendung). Die Begruendung ist leer, wenn der Angriff erlaubt ist.
    """
    a = max(0.0, _als_zahl(punkte_angreifer))
    z = max(0.0, _als_zahl(punkte_ziel))
    ueber_a = a > GOETTERSCHUTZ_PUNKTGRENZE
    ueber_z = z > GOETTERSCHUTZ_PUNKTGRENZE
    if ueber_a != ueber_z:
        return False, (f"Goetterschutzgrenze {GOETTERSCHUTZ_PUNKTGRENZE}: ein Angriff ueber die "
                       f"Grenze hinweg ist in keine Richtung moeglich "
                       f"(Angreifer {a:.0f}, Ziel {z:.0f}).")
    if ueber_a and ueber_z:
        return True, ""
    unten, oben = goetterschutz_band(a)
    if unten <= z <= oben:
        return True, ""
    return False, (f"Eingeschraenkter Goetterschutz: Ziel mit {z:.0f} Punkten liegt ausserhalb "
                   f"von {unten}-{oben} (eigene {a:.0f} +/- 20 %).")


# --------------------------------------------------------------------------
# 7. Sieg oder Niederlage (VORSCHLAG — das Handbuch nennt keine Bedingung)
# --------------------------------------------------------------------------

def sieg_oder_niederlage(zustand: dict) -> Tuple[str, str]:
    """('sieg'|'niederlage'|'weiter', Begruendung).

    VORSCHLAG: Das Handbuch nennt **keine** Sieg- oder Niederlagebedingung. Dieser
    Baustein denkt sich zwei aus und markiert sie im Text ausdruecklich als Vorschlag:

      * Niederlage, sobald der Spieler keine Siedlung und keine Einheit mehr hat,
      * Sieg, sobald die Zielpunktzahl erreicht ist (``ziel_punkte``, sonst 300).

    Erwartete Schluessel in ``zustand``: ``siedlungen`` (Liste), ``einheiten``
    (Name -> Anzahl), ``punkte`` und wahlweise ``ziel_punkte``.
    """
    z = zustand or {}
    siedlungen = z.get("siedlungen") or []
    anzahl_einheiten = 0
    for wert in (z.get("einheiten") or {}).values():
        anzahl_einheiten += _anzahl(wert)
    punkte = _stufe(z.get("punkte", z.get("gesamtpunkte", 0)))
    ziel = _stufe(z.get("ziel_punkte", VORSCHLAG_ZIEL_PUNKTE))

    if not siedlungen and anzahl_einheiten == 0:
        return ("niederlage",
                "VORSCHLAG: keine Siedlung und keine Einheit mehr — das Handbuch nennt keine "
                "Niederlagebedingung.")
    if ziel > 0 and punkte >= ziel:
        return ("sieg",
                f"VORSCHLAG: Zielpunktzahl {ziel} erreicht — das Handbuch nennt keine Siegbedingung.")
    return ("weiter",
            "weder Sieg noch Niederlage nach dem Vorschlag erreicht — das Handbuch nennt keine "
            "Siegbedingung.")


# --------------------------------------------------------------------------
# 8. Belege und Vorschlaege
# --------------------------------------------------------------------------

def belegte_formeln() -> Dict[str, str]:
    """Jede belegte Formel mit ihrem woertlichen Beleg (Formel -> Quelle)."""
    return {
        "forschungspunkte": (
            "Summe der Forschungsstufen hoch drei — Handbuch S. 3: \u201eFuer jede Forschung die "
            "Du erlangt hast, wird die Forschungsstufe hoch drei genommen. Die so gewonnenen "
            "Werte werden anschliessend addiert.\u201c"),
        "kriegspunkte_einheiten": (
            "fester Punktewert je Einheit — Handbuch S. 5: \u201eFuer jede Militaer- und "
            "Spionageeinheit die Du ausbildest, bekommst Du Kriegspunkte.\u201c"),
        "kriegspunkte_wall": (
            "Ausbaustufe hoch drei — Handbuch S. 5: \u201ePalisade (Ausbaustufe 4) = 64 "
            "Kriegspunkte (4*4*4=64)\u201c"),
        "gesamtpunkte": (
            "(Kriegspunkte + Forschungspunkte) / 2 — Handbuch S. 5/6: \u201eDie Gesamtpunktzahl "
            "besteht aus der Summe von den Kriegs- und Forschungspunkten. Das Ergebnis wird dann "
            "durch zwei geteilt.\u201c"),
        "rufpunkte": (
            "Ruf geht NICHT in die Gesamtpunkte ein — Handbuch S. 6: \u201eDiese fliessen nicht "
            "mit in die Gesamtpunktzahl ein sondern koennen gegen Boni ... eingetauscht werden.\u201c"),
        "rangfolge": (
            "Punkte, dann hoeherer Ruf, dann frueheres Anmeldedatum — Handbuch S. 6: \u201eDer "
            "Spieler, der den hoeheren Ruf besitzt steht dann weiter oben. Haben beide Spieler "
            "ebenfalls die gleiche Anzahl an Rufpunkten, steht der Spieler oben, der schon laenger "
            "auf dem Server angemeldet ist.\u201c"),
        "goetterschutz": (
            "sieben Tage — Handbuch S. 6: \u201eAlle neuen Spieler befinden sich die ersten sieben "
            "Tage im so genannten Goetterschutz und koennen nicht angegriffen werden.\u201c"),
        "goetterschutz_endet": (
            "vorzeitig mit dem ersten Kriegspunkt — Handbuch S. 6: \u201eDieser Schutz haelt "
            "allerdings nur so lange an, bis der entsprechende Spieler seinen ersten Kriegspunkt "
            "bekommt.\u201c (in diesem Baustein NICHT abgebildet)"),
    }


def vorschlaege() -> Dict[str, Dict[str, str]]:
    """Jede selbst gesetzte Zahl mit Begruendung und Status — nichts davon ist belegt."""
    return {
        "gesamt_rundung": {
            "wert": "abrunden (ganzzahlig; der Rest 0.5 faellt weg)",
            "grund": "das Handbuch nennt keine Rundung, (Kriegs+Forschungs)/2 kann ungerade sein",
            "status": "VORSCHLAG",
        },
        "ziel_punkte": {
            "wert": str(VORSCHLAG_ZIEL_PUNKTE),
            "grund": "das Handbuch nennt keine Siegbedingung; 300 ist die belegte Schutzgrenze",
            "status": "VORSCHLAG",
        },
        "siegbedingung": {
            "wert": "Zielpunktzahl erreicht",
            "grund": "das Handbuch nennt keine Siegbedingung",
            "status": "VORSCHLAG",
        },
        "niederlagebedingung": {
            "wert": "keine Siedlung und keine Einheit",
            "grund": "das Handbuch nennt keine Niederlagebedingung",
            "status": "VORSCHLAG",
        },
        "goetterschutz_startzeitpunkt": {
            "wert": "0 (Schutz ab der ersten Sekunde Spielzeit)",
            "grund": "das Handbuch nennt nur ganze Tage, keinen Startzeitpunkt",
            "status": "VORSCHLAG",
        },
    }
