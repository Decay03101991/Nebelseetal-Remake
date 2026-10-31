"""
Nebelseetal Remake - Kampfbericht (Paket W2b, 04.10.2026).

Ergaenzt den fertigen Kampfablauf (`src/kampf.py`) um die vier Teile des Handbuchs
(Seiten 20-23), die dort noch keine eigene, einzeln pruefbare Funktion hatten:

  1. Vorrunde      - erreicht die Schlagkraft der Fusstruppen (ab der verstaerkten Palisade,
                     Stufe 5, zusaetzlich die der Belagerungswaffen) die Schwelle des Walls?
                     Eine beschaedigte Mauer verlangt prozentual weniger.
  2. Mauerschaden  - je Belagerungswaffe ein Zufallswert aus ihrem Schadensbereich minus
                     Ausbaustufe der Mauer, vom Zustand der Mauer abgezogen.
  3. Beute         - nur so viel, wie die Karren wirklich tragen koennen.
  4. Bericht       - der Schlachtbericht fuer den Reiter 'Nachrichten'.

Es wird NICHTS erfunden: die Schwellen kommen aus `gebaeude_wirkung.wall_schwelle`,
Mauerschaden und Ladung aus `einheiten` / `data/units.json`. Wo das Handbuch schweigt,
steht das in `offene_luecken()` und im Code als ANNAHME gekennzeichnet.

Alle Funktionen sind rein: kein globaler Zustand, keine Datei wird geschrieben oder
veraendert; `spieldaten_anwenden` gibt einen NEUEN Zustand zurueck.

`kampf.py` wird NICHT nachgebaut - die Schlacht selbst bleibt dort. Dieses Modul nimmt
deren Ergebnis entgegen und bereitet es auf.
"""
from __future__ import annotations

import copy
import random
from typing import Any, Dict, Optional

import einheiten as E
import gebaeude_wirkung as GW

STAND = "2026-10-04.1"

# ANNAHME: Das Handbuch nennt in der Vorrunde den Begriff "Fußtruppen", definiert ihn aber
# nicht. Diese Funktionen bekommen die fertige Schlagkraft uebergeben; welche Einheiten das
# sind, entscheidet der Aufrufer (in `kampf.py` sind es Nahkampf UND Fernkampf). Die engere
# Lesart (nur Nahkampf) ist damit nicht ausgeschlossen und steht in `offene_luecken()`.

AUSGANG_TEXT = {
    "angreifer": "Der Angreifer siegt",
    "verteidiger": "Der Verteidiger siegt",
    "unentschieden": "Unentschieden",
}


def _als_zahl(wert: Any, vorgabe: float = 0.0) -> float:
    """Nimmt Zahlen, Numerisches-als-Text und None; Unbrauchbares wird zur Vorgabe."""
    if wert is None:
        return float(vorgabe)
    try:
        return float(wert)
    except (TypeError, ValueError):
        return float(vorgabe)


def _als_int(wert: Any, vorgabe: int = 0) -> int:
    try:
        return int(float(wert))
    except (TypeError, ValueError):
        return int(vorgabe)


def _schwelle_wall(wall_stufe: int) -> Dict[str, Optional[int]]:
    """Die belegten Schwellenwerte einer Wallstufe (aus `gebaeude_wirkung`)."""
    if int(wall_stufe) < 1:
        return {"fusstruppen": None, "belagerungswaffen": None}
    return GW.wall_schwelle(int(wall_stufe))


# ---------------------------------------------------------------------------- 1. Vorrunde

def vorrunde(angreifer_fussttruppen_sk: float,
             angreifer_belagerung_sk: float,
             wall_stufe: int,
             wall_zustand_prozent: float = 100.0) -> Dict[str, Any]:
    """Prueft die Vorrunde nach Handbuch Seite 20/21.

    `wall_zustand_prozent` ist optional und stand nicht im geforderten Aufruf; ohne Angabe
    gilt der volle Zustand (100 %). Eine beschaedigte Mauer verlangt laut Handbuch
    "prozentual weniger" Schlagkraft - der Faktor ist Zustand/100.

    Rueckgabe:
      {'bestanden': bool, 'schwelle': {...}, 'grund': text}
      schwelle = {
        'fusstruppen':        {'nennwert', 'erforderlich', 'vorhanden', 'erreicht'},
        'belagerungswaffen':  {'nennwert', 'erforderlich', 'vorhanden', 'erreicht'|None},
        'wall_stufe', 'wall_name', 'wall_zustand_prozent', 'faktor',
      }
    """
    stufe = int(wall_stufe)
    zustand = _als_zahl(wall_zustand_prozent, 100.0)
    faktor = max(0.0, zustand) / 100.0
    fuss_sk = _als_zahl(angreifer_fussttruppen_sk)
    bel_sk = _als_zahl(angreifer_belagerung_sk)

    werte = _schwelle_wall(stufe)
    fuss_nenn = werte.get("fusstruppen")
    bel_nenn = werte.get("belagerungswaffen")

    schwelle: Dict[str, Any] = {
        "fusstruppen": {"nennwert": fuss_nenn, "erforderlich": None,
                        "vorhanden": fuss_sk, "erreicht": None},
        "belagerungswaffen": {"nennwert": bel_nenn, "erforderlich": None,
                              "vorhanden": bel_sk, "erreicht": None},
        "wall_stufe": stufe,
        "wall_name": GW.wall_name(stufe) if stufe >= 1 else None,
        "wall_zustand_prozent": zustand,
        "faktor": faktor,
    }

    if stufe < 1 or fuss_nenn is None:
        grund = ("Kein Wall vorhanden - die Vorrunde entfaellt, der Angreifer kann "
                 "vorruecken.")
        if stufe >= 1 and fuss_nenn is None:
            grund = (f"Fuer Wallstufe {stufe} nennt das Handbuch keine Schwelle - "
                     "die Vorrunde entfaellt (kein Wert erfunden).")
        return {"bestanden": True, "schwelle": schwelle, "grund": grund}

    fuss_erf = float(fuss_nenn) * faktor
    fuss_ok = fuss_sk >= fuss_erf
    schwelle["fusstruppen"]["erforderlich"] = fuss_erf
    schwelle["fusstruppen"]["erreicht"] = fuss_ok

    if bel_nenn is None:
        bel_erf = None
        bel_ok: Optional[bool] = None
    else:
        bel_erf = float(bel_nenn) * faktor
        bel_ok = bel_sk >= bel_erf
        schwelle["belagerungswaffen"]["erforderlich"] = bel_erf
        schwelle["belagerungswaffen"]["erreicht"] = bel_ok

    if not fuss_ok:
        grund = (f"Die Schlagkraft der Fusstruppen {fuss_sk:.0f} erreicht die Schwelle "
                 f"{fuss_erf:.0f} nicht - Rueckzug, keine Beute.")
        bestanden = False
    elif bel_ok is False:
        grund = (f"Fusstruppen erreichen die Schwelle {fuss_erf:.0f}, aber die Schlagkraft "
                 f"der Belagerungswaffen {bel_sk:.0f} erreicht {bel_erf:.0f} nicht - "
                 "Rueckzug, keine Beute.")
        bestanden = False
    else:
        teile = [f"Fusstruppen {fuss_sk:.0f} >= {fuss_erf:.0f}"]
        if bel_erf is not None:
            teile.append(f"Belagerungswaffen {bel_sk:.0f} >= {bel_erf:.0f}")
        grund = "Vorrunde bestanden (" + ", ".join(teile) + ")."
        bestanden = True

    return {"bestanden": bestanden, "schwelle": schwelle, "grund": grund}


# ------------------------------------------------------------------------ 2. Mauerschaden

def mauer_schaden(belagerung: Dict[str, int],
                  wall_stufe: int,
                  wall_zustand_prozent: float,
                  rng: Optional[random.Random] = None) -> Dict[str, Any]:
    """Mauerschaden nach Handbuch Seite 21/22.

    Je mitgefuehrter Belagerungswaffe wird EINZELN gewuerfelt: Zufallswert im Schadensbereich
    der Waffe minus Ausbaustufe der Mauer; ein positiver Rest geht vom Zustand ab. Der
    Zustand faellt nie unter 0 %.

    Rueckgabe:
      {'mauer_zustand_prozent', 'vorher_prozent', 'schaden_gesamt',
       'wall_stufe', 'je_waffe': {name: {'anzahl', 'wuerfe', 'rest', 'schaden'}}}
    """
    rng = rng or random.Random()
    stufe = int(wall_stufe)
    vorher = max(0.0, _als_zahl(wall_zustand_prozent, 100.0))

    je_waffe: Dict[str, Dict[str, Any]] = {}
    gesamt = 0
    for name, anzahl in (belagerung or {}).items():
        n = max(0, _als_int(anzahl))
        lo, hi = E.mauer_schaden(name)
        wuerfe, rest = [], []
        for _ in range(n):
            wurf = rng.randint(int(lo), int(hi))
            r = max(0, int(wurf) - stufe)
            wuerfe.append(int(wurf))
            rest.append(int(r))
            gesamt += int(r)
        if name not in je_waffe:
            je_waffe[name] = {"anzahl": n, "wuerfe": wuerfe, "rest": rest,
                              "schaden": sum(rest)}

    neu = max(0.0, vorher - gesamt)
    return {
        "mauer_zustand_prozent": neu,
        "vorher_prozent": vorher,
        "schaden_gesamt": gesamt,
        "wall_stufe": stufe,
        "je_waffe": je_waffe,
    }


# ------------------------------------------------------------------------------ 3. Beute

# VORGABE DANIEL 31.10.2026 (Registerpunkt 45): Die Beute wird GESTAFFELT, nicht pauschal.
# Belegt ist nur: "nur Transportkarren pluendern" (Handbuch S. 23) und "Beute ist durch die
# Ladung begrenzt". Die Prozentwerte sind VORSCHLAG und werden im Spieltest balanciert.
# Reihenfolge der Pruefung: keine Verteidiger > Wall gebrochen > Wall beschaedigt > Wall heil.
BEUTE_STAFFEL_PROZENT: Dict[str, int] = {
    "keine_verteidiger": 100,   # niemand verteidigt mehr -> der ganze Bestand darf mit
    "mauer_gebrochen": 60,      # Wall war beim Angriff schon bei 0 Prozent
    "mauer_beschaedigt": 30,    # Wall bereits (teilweise) eingerissen
    "mauer_heil": 10,           # erster erfolgreicher Angriff, Wall steht noch
}


def beute_lage(wall_zustand_vor: Any, verteidiger_uebrig: Any) -> str:
    """Welche Lage gilt fuer die Staffelung? (VORGABE Daniel, Prozentwerte VORSCHLAG)

    Keine Verteidiger mehr -> 'keine_verteidiger'; Wall bei 0 -> 'mauer_gebrochen';
    Wall unter 100 (aber ueber 0) -> 'mauer_beschaedigt'; sonst 'mauer_heil'.
    Unbekannte Angaben (None) gelten als "Wall heil, Verteidiger vorhanden" - der
    vorsichtigste Fall, damit nichts verschenkt wird.
    """
    if verteidiger_uebrig is not None:
        try:
            if int(verteidiger_uebrig) <= 0:
                return "keine_verteidiger"
        except (TypeError, ValueError):
            pass
    zustand = _als_zahl(wall_zustand_vor, 100.0)
    if zustand <= 0.0:
        return "mauer_gebrochen"
    if zustand < 99.5:          # alles unter "unversehrt" gilt als eingerissen
        return "mauer_beschaedigt"
    return "mauer_heil"


def beute_staffel(einheiten_des_siegers: Dict[str, int],
                  vorraete: Dict[str, float],
                  wall_zustand_vor: Any = None,
                  verteidiger_uebrig: Any = None) -> Dict[str, int]:
    """Beute nach Daniels Staffelung (Registerpunkt 45).

    Anteil = BEUTE_STAFFEL_PROZENT[beute_lage(...)], zusaetzlich begrenzt durch
      * die Gesamtladung der mitgefuehrten Karren und
      * den tatsaechlich vorhandenen Vorrat je Rohstoff.
    Die Verteilung auf die Rohstoffe ist anteilig nach Vorratsmenge (das Handbuch
    regelt die Aufteilung nicht).

    Beispiele (Vorschlagswerte): Wall heil, 1.000 je Rohstoff, Handkarren (Ladung 40)
    -> 10 Prozent = 100, aber nur 40 passen hinein. Ohne Verteidiger -> 100 Prozent,
    begrenzt durch Ladung. Kein Karren -> keine Beute (belegt).
    """
    kapazitaet = 0
    for name, anzahl in (einheiten_des_siegers or {}).items():
        kapazitaet += E.kapazitaet(name, max(0, _als_int(anzahl)))
    if kapazitaet <= 0:
        return {}

    vorhanden: Dict[str, int] = {}
    for stoff, menge in (vorraete or {}).items():
        m = int(max(0.0, _als_zahl(menge)))
        if m > 0:
            vorhanden[stoff] = m
    gesamt = sum(vorhanden.values())
    if gesamt <= 0:
        return {}

    anteil = BEUTE_STAFFEL_PROZENT[beute_lage(wall_zustand_vor, verteidiger_uebrig)] / 100.0
    ziel_menge = int(gesamt * anteil)
    restplatz = min(kapazitaet, ziel_menge)
    genommen: Dict[str, int] = {}
    for stoff in sorted(vorhanden):
        if restplatz <= 0:
            break
        anteil_stoff = vorhanden[stoff] / gesamt
        nimm = min(int(anteil_stoff * ziel_menge), vorhanden[stoff], restplatz)
        if nimm > 0:
            genommen[stoff] = nimm
            restplatz -= nimm
    return genommen


def beute(einheiten_des_siegers: Dict[str, int],
          vorraete: Dict[str, float],
          rng: Optional[random.Random] = None) -> Dict[str, int]:
    """Was die Karren des Siegers tragen koennen (Handbuch Seite 22/23).

    Nur Transporteinheiten (Karren) tragen; Belagerungswaffen und Kaempfer tragen nichts.
    Die Beute ist ehrlich begrenzt: sie ueberschreitet weder die Gesamtkapazitaet der Karren
    noch den vorhandenen Vorrat je Rohstoff.

    ANNAHME zur Verteilung: Das Handbuch begrenzt die Beute auf die Karrenladung, nennt aber
    keine Aufteilung auf die Rohstoffe. Hier wird anteilig nach Vorratsmenge verladen
    (dieselbe Regel wie in `kampf.py.ergebnis['beute']`). `rng` wird angenommen, aber nicht
    gebraucht - die Aufteilung ist bewusst nachvollziehbar und nicht zufaellig.
    """
    del rng  # bewusst ungenutzt: die Verteilung ist nicht im Handbuch geregelt -> anteilig

    kapazitaet = 0
    for name, anzahl in (einheiten_des_siegers or {}).items():
        kapazitaet += E.kapazitaet(name, max(0, _als_int(anzahl)))

    vorhanden: Dict[str, int] = {}
    for stoff, menge in (vorraete or {}).items():
        m = int(max(0.0, _als_zahl(menge)))
        if m > 0:
            vorhanden[stoff] = m

    gesamt = sum(vorhanden.values())
    if kapazitaet <= 0 or gesamt <= 0:
        return {}

    genommen: Dict[str, int] = {}
    restplatz = kapazitaet
    for stoff in sorted(vorhanden):
        if restplatz <= 0:
            break
        anteil = vorhanden[stoff] / gesamt
        nimm = min(int(anteil * kapazitaet), vorhanden[stoff], restplatz)
        if nimm > 0:
            genommen[stoff] = nimm
            restplatz -= nimm
    return genommen


# ---------------------------------------------------------------------------- 4. Bericht

def _aufzaehlung(werte: Dict[str, int]) -> str:
    teile = [f"{name} {int(_als_zahl(anzahl))}" for name, anzahl in sorted((werte or {}).items())]
    return ", ".join(teile) if teile else "keine"


def bericht(ergebnis: Dict[str, Any]) -> Dict[str, str]:
    """Baut den Schlachtbericht fuer den Reiter 'Nachrichten'.

    Nimmt das Ergebnis aus `kampf.fuehre_schlacht` entgegen und liefert:
      {'titel': str, 'zeilen': [str, ...], 'typ': 'kampf'}
    Es wird nichts erfunden: fehlen Felder, werden sie uebergangen.
    """
    e = ergebnis or {}
    ausgang = str(e.get("ausgang", "unentschieden"))
    ausgang_text = AUSGANG_TEXT.get(ausgang, ausgang)
    titel = "Schlachtbericht: " + ausgang_text

    zeilen = [f"Ausgang: {ausgang_text}."]
    if "mauer_zustand" in e:
        zeilen.append(f"Mauerzustand danach: {_als_zahl(e.get('mauer_zustand')):.0f} %.")
    zeilen.append("Verluste Angreifer: " + _aufzaehlung(e.get("verluste_angreifer") or {}))
    zeilen.append("Verluste Verteidiger: " + _aufzaehlung(e.get("verluste_verteidiger") or {}))

    if e.get("geflohen"):
        zeilen.append("Geflohen: " + ", ".join(str(x) for x in e["geflohen"]) + ".")

    beute_ = e.get("beute") or {}
    if beute_:
        zeilen.append("Beute: " + _aufzaehlung(beute_) + ".")
    else:
        zeilen.append("Beute: keine.")

    if e.get("geraete_verloren"):
        zeilen.append("Vom Angreifer zurueckgelassen: " +
                      ", ".join(str(x) for x in e["geraete_verloren"]) + ".")
    if e.get("geraete_verloren_verteidiger"):
        zeilen.append("Vom Verteidiger zurueckgelassen: " +
                      ", ".join(str(x) for x in e["geraete_verloren_verteidiger"]) + ".")

    if e.get("unsicher"):
        zeilen.append("Offene Punkte: " + " ".join(str(x) for x in e["unsicher"]))

    for z in str(e.get("bericht") or "").split("\n"):
        if z.strip():
            zeilen.append(z.rstrip())

    return {"titel": titel, "zeilen": zeilen, "typ": "kampf"}


# ------------------------------------------------------------------ 5. Spieldaten anwenden

def spieldaten_anwenden(zustand_vorher: Dict[str, Any],
                        ergebnis: Dict[str, Any]) -> Dict[str, Any]:
    """Wendet ein Schlachtergebnis auf den Spielstand an und gibt einen NEUEN Stand zurueck.

    Der Stand gehoert dem ANGREIFER (der den Bericht liest):
      * gefundene Beute kommt zu `ressourcen`,
      * die eigenen Verluste (`verluste_angreifer`) und zurueckgelassene Geraete
        (`geraete_verloren`) gehen von `einheiten` ab,
      * der `mauer_zustand` wird als `wall_zustand_prozent` uebernommen.

    Erwartet: {'ressourcen': {stoff: menge}, 'einheiten': {name: anzahl}, ...}
    Der Eingabestand wird NICHT veraendert (tiefe Kopie).
    """
    neu = copy.deepcopy(zustand_vorher) if zustand_vorher else {}
    if not isinstance(neu.get("ressourcen"), dict):
        neu["ressourcen"] = {}
    if not isinstance(neu.get("einheiten"), dict):
        neu["einheiten"] = {}

    e = ergebnis or {}

    for stoff, menge in (e.get("beute") or {}).items():
        alt = neu["ressourcen"].get(stoff, 0) or 0
        neu["ressourcen"][stoff] = alt + int(_als_zahl(menge))

    verluste: Dict[str, int] = dict(e.get("verluste_angreifer") or {})
    for einheit in (e.get("geraete_verloren") or []):
        verluste[einheit] = _als_int(verluste.get(einheit, 0)) + 1

    for einheit, anzahl in verluste.items():
        alt = _als_int(neu["einheiten"].get(einheit, 0))
        neu["einheiten"][einheit] = max(0, alt - _als_int(anzahl))

    if "mauer_zustand" in e:
        neu["wall_zustand_prozent"] = _als_zahl(e.get("mauer_zustand"))

    return neu


# ------------------------------------------------------------------------ 6. Offene Luecken

def offene_luecken() -> Dict[str, str]:
    """Was das Handbuch zum Kampf nicht sagt - ehrliche Liste, kein erfundener Wert."""
    return {
        "fusstruppen_begriff":
            "Der Begriff 'Fußtruppen' der Vorrunde ist im Handbuch nicht definiert. "
            "kampf.py zaehlt Nahkampf- UND Fernkampfeinheiten dazu; die engere Lesart "
            "(nur Nahkampf) ist nicht ausgeschlossen.",
        "flucht_formel":
            "Zum Fliehen unter LE 5 nennt das Handbuch nur 'je niedriger der MU, desto "
            "wahrscheinlicher', aber keine Formel.",
        "beute_verteilung":
            "Die Beute ist auf die Karrenladung begrenzt, eine Aufteilung auf die Rohstoffe "
            "ist nicht geregelt. Hier gilt: anteilig nach Vorratsmenge.",
        "beute_reihenfolge":
            "In welcher Reihenfolge Rohstoffe verladen werden, ist nicht geregelt "
            "(hier alphabetisch).",
        "belagerungsturm_mauerschaden":
            "Belagerungsturm und Grosser Belagerungsturm haben Mauerschaden 0-0: sie brechen "
            "keine Mauer, tragen aber Schlagkraft zur Vorrunde bei.",
        "mauer_reparatur":
            "Ob und wie sich eine beschaedigte oder eroberte Mauer erholt, sagt das Handbuch "
            "nicht.",
        "vorrunde_wiederholung":
            "Wie viele Versuche ein Angreifer gegen den Wall hat, ist offen.",
        "geraetebeute":
            "Ob erbeutete Karren und Belagerungswaffen mitgenommen werden koennen, ist nicht "
            "geregelt.",
    }
