"""
Nebelseetal Remake — Kampfablauf nach dem Originalhandbuch (Seiten 20-22).

Vorher verglich das Spiel zwei Zufallszahlen. Hier steht der Ablauf, den das Handbuch
beschreibt: Vorrunde gegen den Wall, Mauerschaden, hoechstens zehn Kampfsequenzen mit
gleichzeitigem Fernkampf und anschliessendem Nahkampf, Zweikaempfe mit AT/PA/RS/TP,
Erschoepfung des Siegers, Flucht ab LE unter 5, Beute nur mit Transportkarren.

Wo das Handbuch schweigt, wird **nichts erfunden**: die Stelle ist im Bericht als
`unsicher` vermerkt und im Code mit `ANNAHME` gekennzeichnet. Belegte Regeln stehen ohne
Kennzeichnung.

Werte kommen ausschliesslich aus `einheiten.py` (also aus `data/units.json`).
"""
from __future__ import annotations

import random
from typing import Any, Dict, List, Optional, Tuple

import einheiten as E
import spieldaten

STAND = "2026-10-04"

# Handbuch Seite 20: Die Vorrunde prueft die Schlagkraft der Fusstruppen; ab der Stufe
# "verstaerkte Palisade" muss zusaetzlich die Schlagkraft der Belagerungswaffen reichen.
# Fusstruppen sind hier Nahkampf- und Fernkampfeinheiten (Kundschafter reiten, Karren und
# Belagerungswaffen stehen nicht in der Schlachtlinie).
ANNAHME_FUSSTRUPPEN = ("Nahkampf", "Fernkampf")


def _eigenschaften(name: str) -> Dict[str, Any]:
    """Ein Kaempfer mit Einzelwerten (das Handbuch rechnet mit einzelnen Einheiten)."""
    w = E.alle()[name]["werte"]
    return {
        "name": name,
        "kategorie": E.alle()[name]["kategorie"],
        "le": float(w.get("LE") or 0),
        "at": float(w.get("AT") or 0),
        "pa": float(w.get("PA") or 0),
        "rs": float(w.get("RS") or 0),
        "tp_min": float(w.get("TP_min") or 0),
        "tp_max": float(w.get("TP_max") or 0),
        "mu": w.get("MU"),
        "sk": float(w.get("SK") or 0),
        "gs": float(w.get("GS") or 0),
        "ladung": E.ladung(name),
        "rolle": E.alle()[name]["rolle"],
        "geflohen": False,
        "tot": False,
    }


def _aufstellen(anzahl: Dict[str, int]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for name, n in (anzahl or {}).items():
        if name not in E.alle() or n <= 0:
            continue
        for _ in range(int(n)):
            out.append(_eigenschaften(name))
    return out


def _lebt(u: Dict[str, Any]) -> bool:
    return not u["tot"] and not u["geflohen"]


def _lebende(truppe: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [u for u in truppe if _lebt(u)]


def _fusstruppen(truppe: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [u for u in _lebende(truppe) if u["kategorie"] in ANNAHME_FUSSTRUPPEN]


def _fernkaempfer(truppe: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [u for u in _lebende(truppe) if u["kategorie"] == "Fernkampf"]


def _nahkaempfer(truppe: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [u for u in _lebende(truppe) if u["kategorie"] == "Nahkampf"]


def _schlagkraft(truppe: List[Dict[str, Any]]) -> float:
    """Handbuch Seite 20: Schlagkraft ist die Summe der SK der genannten Einheiten."""
    return sum(u["sk"] for u in truppe)


def _fluchtprobe(u: Dict[str, Any], rng: random.Random) -> bool:
    """Handbuch Seite 22: Fluchtprobe ueber den Mut (MU).

    Fehlt MU (Karren, Belagerungswaffen), kaempfen diese Einheiten nicht und fliehen auch
    nicht ueber diese Probe — die Regel greift dann nicht.
    """
    if u["mu"] is None:
        return False
    return rng.randint(1, 100) > float(u["mu"])


def _zweikampf(a: Dict[str, Any], b: Dict[str, Any], rng: random.Random,
               bericht: List[str]) -> Optional[Dict[str, Any]]:
    """Handbuch Seite 21/22. Rueckgabe: der Sieger (oder None, wenn keiner Schaden nahm)."""
    # Wer beginnt? Hoeherer MU; bei Gleichstand der Verteidiger (also b).
    if float(a["mu"] or 0) > float(b["mu"] or 0):
        erster, zweiter = a, b
    else:
        erster, zweiter = b, a

    for angreifer, verteidiger in ((erster, zweiter), (zweiter, erster)):
        if not _lebt(angreifer) or not _lebt(verteidiger):
            continue
        wurf = rng.randint(1, 100)
        if wurf > angreifer["at"]:
            bericht.append(f"    {angreifer['name']} greift {verteidiger['name']} an — "
                           f"Wurf {wurf} gegen AT {angreifer['at']:.0f}: Fehlschlag.")
            continue
        parade = rng.randint(1, 100)
        if parade <= verteidiger["pa"]:
            bericht.append(f"    {angreifer['name']} trifft {verteidiger['name']} (Wurf {wurf}), "
                           f"Parade gelingt (Wurf {parade} gegen PA {verteidiger['pa']:.0f}).")
            continue
        schaden = rng.randint(int(angreifer["tp_min"]), int(angreifer["tp_max"]))
        schaden = max(1, schaden - int(verteidiger["rs"]))
        verteidiger["le"] -= schaden
        bericht.append(f"    {angreifer['name']} trifft {verteidiger['name']} (Wurf {wurf}), "
                       f"keine Parade (Wurf {parade} gegen PA {verteidiger['pa']:.0f}): "
                       f"{schaden} Schaden, LE {verteidiger['le']:.0f}")
        if verteidiger["le"] < 1:
            verteidiger["tot"] = True
            bericht.append(f"    {verteidiger['name']} ist gefallen.")
        elif verteidiger["le"] < 5 and _fluchtprobe(verteidiger, rng):
            verteidiger["geflohen"] = True
            bericht.append(f"    {verteidiger['name']} hat LE unter 5 und flieht (Mutprobe verloren).")
        # Erschoepfung: der Sieger dieses Zweikampfs ermattet (Seite 22)
        angreifer["at"] = max(0.0, angreifer["at"] - 1)
        angreifer["pa"] = max(0.0, angreifer["pa"] - 1)
        return angreifer
    return None


def _verluste_zaehlen(vorher: List[Dict[str, Any]], nachher: List[Dict[str, Any]]) -> Dict[str, int]:
    """Gefallene je Einheitenname.

    Geflohene zaehlen NICHT als Verlust: sie kehren nach der Schlacht zurueck
    (Handbuch Seite 22) und stehen im Feld `geflohen`.
    """
    verluste: Dict[str, int] = {}
    for name in {u["name"] for u in vorher}:
        a = len([u for u in vorher if u["name"] == name])
        b = len([u for u in nachher if u["name"] == name and not u["tot"]])
        if a - b:
            verluste[name] = a - b
    return verluste


def fuehre_schlacht(angreifer: Dict[str, int],
                    verteidiger: Dict[str, int],
                    wall_stufe: int = 0,
                    wall_zustand: float = 100.0,
                    angreifer_karren: Optional[Dict[str, int]] = None,
                    verteidiger_karren: Optional[Dict[str, int]] = None,
                    vorraete: Optional[Dict[str, float]] = None,
                    rng: Optional[random.Random] = None) -> Dict[str, Any]:
    """Fuehrt eine Schlacht nach dem Handbuch und liefert den Bericht zurueck.

    angreifer/verteidiger: {einheitenname: anzahl}. Karren und Belagerungswaffen des
    Angreifers werden getrennt uebergeben — sie stehen nicht in der Schlachtlinie, sondern
    brechen Mauern und tragen Beute (Handbuch Seiten 20-22).
    """
    rng = rng or random.Random()
    bericht: List[str] = []
    unsicher: List[str] = []

    A = _aufstellen(angreifer)
    V = _aufstellen(verteidiger)
    AK = _aufstellen(angreifer_karren or {})
    VK = _aufstellen(verteidiger_karren or {})
    A_belagerung = [u for u in AK if u["rolle"] == "belagerung"]
    A_transport = [u for u in AK if u["rolle"] == "karren"]

    stufen = {i + 1: s for i, s in enumerate(spieldaten.wallstufen())}
    wall = stufen.get(int(wall_stufe))
    bericht.append(f"Schlacht um eine Siedlung. Wall: Stufe {wall_stufe} "
                   f"({wall['name'] if wall else 'kein Wall'}), Zustand {wall_zustand:.0f} %.")
    bericht.append(f"Angreifer: {len(A)} Kaempfer, {len(A_belagerung)} Belagerungswaffen, "
                   f"{len(A_transport)} Karren. Verteidiger: {len(V)} Kaempfer.")

    ergebnis: Dict[str, Any] = {
        "ausgang": "unentschieden", "sequenzen": [], "verluste_angreifer": {},
        "verluste_verteidiger": {}, "geflohen": [], "mauer_zustand": float(wall_zustand),
        "beute": {}, "bericht": "", "unsicher": unsicher, "stand": STAND,
    }

    # ---- 1. Vorrunde (Seite 20) ------------------------------------------------------
    if wall is None:
        bericht.append("Kein Wall vorhanden — keine Vorrunde noetig.")
    else:
        schwelle_fuss = float(wall["schwellenwert_fussttruppen"])
        schwelle_bel = wall["schwellenwert_belagerungswaffen"]
        # Beschaedigter Wall verlangt prozentual weniger Schlagkraft (Seite 20).
        faktor = max(0.0, float(wall_zustand)) / 100.0
        schwelle_fuss_eff = schwelle_fuss * faktor
        sk_fuss = _schlagkraft(_fusstruppen(A))
        sk_bel = _schlagkraft(A_belagerung)
        bericht.append(f"Vorrunde: Schlagkraft Fusstruppen {sk_fuss:.0f} gegen Schwelle "
                       f"{schwelle_fuss_eff:.0f} (Stufe {wall_stufe}, Zustand {wall_zustand:.0f} %).")
        if sk_fuss < schwelle_fuss_eff:
            bericht.append("Schwelle nicht erreicht — der Angreifer zieht sich zurueck.")
            ergebnis["bericht"] = "\n".join(bericht)
            ergebnis["ausgang"] = "unentschieden"
            return ergebnis
        if schwelle_bel is not None:
            bericht.append(f"Ab dieser Stufe zusaetzlich Belagerungswaffen: Schlagkraft {sk_bel:.0f} "
                           f"gegen Schwelle {float(schwelle_bel) * faktor:.0f}.")
            if sk_bel < float(schwelle_bel) * faktor:
                bericht.append("Belagerungswaffen reichen nicht — Rueckzug, unentschieden.")
                ergebnis["bericht"] = "\n".join(bericht)
                ergebnis["ausgang"] = "unentschieden"
                return ergebnis
        else:
            bericht.append("Fuer diese Wallstufe nennt das Handbuch keine Schwelle fuer "
                           "Belagerungswaffen.")

    # ---- 2. Mauerschaden (Seite 20) --------------------------------------------------
    if A_belagerung:
        schaden_gesamt = 0
        for waffe in A_belagerung:
            wurf = rng.randint(int(waffe["tp_min"]), int(waffe["tp_max"]))
            rest = max(0, wurf - int(wall_stufe))
            schaden_gesamt += rest
            bericht.append(f"Mauerschaden: {waffe['name']} wuerfelt {wurf} gegen Ausbaustufe "
                           f"{wall_stufe} -> {rest} Schaden.")
        if schaden_gesamt:
            neu = max(0.0, float(wall_zustand) - schaden_gesamt)
            bericht.append(f"Mauerzustand {wall_zustand:.0f} % -> {neu:.0f} % "
                           f"({schaden_gesamt} Punkte, 1 Punkt = 1 Prozent laut Handbuchbeispiel).")
            ergebnis["mauer_zustand"] = neu
        else:
            bericht.append("Keine Waffe verursachte Mauerschaden.")

    # ---- 3. Kampfsequenzen (Seite 21/22) ---------------------------------------------
    A_vorher, V_vorher = list(A), list(V)
    sequenz_nummer = 0
    for sequenz_nummer in range(1, 11):
        if not _fusstruppen(A):
            break
        if not _fusstruppen(V):
            break
        zeile: List[str] = [f"  Sequenz {sequenz_nummer}:"]

        # a) Fernkampf zuerst und gleichzeitig
        for angreifer_fern in _fernkaempfer(A):
            ziele = _fusstruppen(V)
            if not ziele:
                ziele = _fernkaempfer(V)
            if not ziele:
                break
            _zweikampf(angreifer_fern, rng.choice(ziele), rng, zeile)
        for verteidiger_fern in _fernkaempfer(V):
            ziele = _fusstruppen(A)
            if not ziele:
                ziele = _fernkaempfer(A)
            if not ziele:
                break
            _zweikampf(verteidiger_fern, rng.choice(ziele), rng, zeile)

        # b) dann stuermen die Nahkaempfer nacheinander je eine zufaellige Einheit an
        for angreifer_nah in _nahkaempfer(A):
            ziele = _nahkaempfer(V)
            if not ziele:
                break
            _zweikampf(angreifer_nah, rng.choice(ziele), rng, zeile)
        for verteidiger_nah in _nahkaempfer(V):
            ziele = _nahkaempfer(A)
            if not ziele:
                break
            _zweikampf(verteidiger_nah, rng.choice(ziele), rng, zeile)

        bericht.extend(zeile)
        ergebnis["sequenzen"].append("\n".join(zeile))

    if sequenz_nummer == 10 and _fusstruppen(A) and _fusstruppen(V):
        unsicher.append("Nach zehn Kampfsequenzen standen noch Truppen beider Seiten — "
                        "das Handbuch nennt fuer diesen Fall keinen Ausgang (hier: unentschieden).")

    ergebnis["verluste_angreifer"] = _verluste_zaehlen(A_vorher, A)
    ergebnis["verluste_verteidiger"] = _verluste_zaehlen(V_vorher, V)
    ergebnis["geflohen"] = ([f"{u['name']} (Angreifer)" for u in A if u["geflohen"]] +
                            [f"{u['name']} (Verteidiger)" for u in V if u["geflohen"]])

    # ---- 4. Ausgang (Seite 22) -------------------------------------------------------
    angreifer_hat_fusstruppen = bool(_fusstruppen(A))
    verteidiger_hat_fusstruppen = bool(_fusstruppen(V))
    if not verteidiger_hat_fusstruppen and angreifer_hat_fusstruppen:
        ergebnis["ausgang"] = "angreifer"
        bericht.append("Alle Verteidiger tot oder geflohen — der Angreifer siegt.")
    elif not angreifer_hat_fusstruppen and verteidiger_hat_fusstruppen:
        ergebnis["ausgang"] = "verteidiger"
        bericht.append("Alle angreifenden Fusstruppen tot oder geflohen — der Verteidiger siegt.")
    elif not angreifer_hat_fusstruppen and not verteidiger_hat_fusstruppen:
        ergebnis["ausgang"] = "unentschieden"
        bericht.append("Beide Seiten ohne Fusstruppen — unentschieden.")
    else:
        ergebnis["ausgang"] = "unentschieden"
        bericht.append("Keine Seite setzte sich durch — unentschieden.")

    # ---- 5. Beute (Seite 22): nur mit Transportkarren --------------------------------
    if ergebnis["ausgang"] == "angreifer" and A_transport and vorraete:
        kapazitaet = sum(u["ladung"] for u in A_transport if _lebt(u))
        if kapazitaet <= 0:
            bericht.append("Keine Tragekapazitaet — es wird nichts gepluendert.")
        else:
            gesamt = sum(max(0.0, float(v)) for v in vorraete.values())
            genommen: Dict[str, int] = {}
            restplatz = kapazitaet
            for rohstoff, menge in sorted(vorraete.items()):
                if restplatz <= 0 or gesamt <= 0:
                    break
                anteil = max(0.0, float(menge)) / gesamt
                nimm = min(int(anteil * kapazitaet), int(max(0.0, float(menge))), restplatz)
                if nimm > 0:
                    genommen[rohstoff] = nimm
                    restplatz -= nimm
            ergebnis["beute"] = genommen
            bericht.append(f"Beute mit {len(A_transport)} Transportkarren "
                           f"(Kapazitaet {kapazitaet}): {genommen or 'nichts'}.")
    elif ergebnis["ausgang"] == "angreifer":
        bericht.append("Der Angreifer siegt, fuehrt aber keine Transportkarren mit — "
                       "es wird nicht gepluendert (Handbuch Seite 22).")

    # ---- 6. Verluste an Karren und Belagerungswaffen (Seite 22) ----------------------
    if ergebnis["ausgang"] == "verteidiger":
        weiter, verloren = [], []
        for u in AK:
            chance = 40 + 5 * sequenz_nummer
            if rng.randint(1, 100) <= chance:
                weiter.append(u["name"])
            else:
                verloren.append(u["name"])
        if AK:
            bericht.append(f"Der Angreifer verliert Karren und Belagerungswaffen: "
                           f"{len(verloren)} von {len(AK)} bleiben zurueck "
                           f"(Fluchtchance {40 + 5 * sequenz_nummer} % je Einheit).")
        ergebnis["karren_verloren"] = verloren
        ergebnis["karren_erhalten"] = weiter
    elif ergebnis["ausgang"] == "unentschieden" and AK:
        bericht.append("Unentschieden — alle Karren und Belagerungswaffen bleiben beim Angreifer.")

    ergebnis["bericht"] = "\n".join(bericht)
    return ergebnis
