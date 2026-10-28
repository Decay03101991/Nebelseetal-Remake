"""
Nebelseetal Remake — Kampfablauf nach dem Originalhandbuch (Seiten 20-23).

Zweite Fassung nach einem Regelgutachten (gpt-6-astra, 04.10.2026), dessen Befunde alle am
wörtlichen Handbuchtext geprüft wurden. Korrigiert gegenüber der ersten Fassung:

  1. Fernkampf laeuft WIRKLICH gleichzeitig: beide Seiten feuern zuerst, danach werden die
     Verluste auf beiden Seiten berechnet ("ZUERST feuern und ANSCHLIEßEND die Verluste auf
     beiden Seiten berechnet werden").
  2. Im Nahkampf stuermen nur die ANGREIFENDEN Nahkampfeinheiten, nacheinander, je eine
     zufaellige gegnerische Einheit. Der Verteidiger stuermt nicht zusaetzlich.
  3. Ein Zweikampf laeuft in Kampfrunden, bis eine der beiden tot ist oder flieht — nicht
     ein einzelner Schlag.
  4. Ziele des Nahkampfs: zuerst verteidigende Nahkampfeinheiten, sind keine uebrig, die
     verteidigenden Fernkampfeinheiten.
  5. Die Schlacht endet, sobald eine Armee keine NAHKAMPFeinheiten mehr hat oder 10
     Kampfsequenzen vorueber sind.
  6. Der Verlierer verliert Karren und Belagerungswaffen — gleich welche Seite verliert
     ("seiner stationierten bzw. mitgeschickten Karren").
  7. Erschoepfung: der Sieger eines ZWEIKAMPFS verliert 1 AT und 1 PA bis Schlachtende
     (summiert sich ueber mehrere Zweikaempfe), nicht je Schlag.

Wo das Handbuch schweigt, ist es im Bericht als `unsicher` vermerkt und im Code mit
`ANNAHME` gekennzeichnet. Werte kommen ausschliesslich aus `einheiten.py`/`data/units.json`.
"""
from __future__ import annotations

import random
from typing import Any, Dict, List, Optional, Tuple

import einheiten as E
import spieldaten

STAND = "2026-10-04.2"

# ANNAHME: Fuer die Vorrunde sind Fusstruppen Nahkampf- UND Fernkampfeinheiten. Das Handbuch
# benutzt den Begriff, ohne ihn zu definieren; im Fernkampfabschnitt unterscheidet es
# "Fußtruppen" aber ausdruecklich von den eigenen Fernkaempfern des Ziels, was auch fuer eine
# engere Lesart (nur Nahkampf) spricht. An beiden Stellen ausgewiesen.
FUSSTRUPPEN = ("Nahkampf", "Fernkampf")


# --------------------------------------------------------------- Aufbau

def _eigenschaften(name: str) -> Dict[str, Any]:
    w = E.alle()[name]["werte"]
    return {
        "name": name,
        "kategorie": E.alle()[name]["kategorie"],
        "rolle": E.alle()[name]["rolle"],
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
        "geflohen": False,
        "tot": False,
    }


def _aufstellen(anzahl: Optional[Dict[str, int]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for name, n in (anzahl or {}).items():
        if name not in E.alle() or n <= 0:
            continue
        for _ in range(int(n)):
            out.append(_eigenschaften(name))
    return out


def _lebt(u: Dict[str, Any]) -> bool:
    """Im Kampf aktiv. Geflohene zaehlen NICHT — sie kehren erst nach der Schlacht zurueck."""
    return not u["tot"] and not u["geflohen"]


def _aktive(truppe: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [u for u in truppe if _lebt(u)]


def _fusstruppen(truppe: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [u for u in _aktive(truppe) if u["kategorie"] in FUSSTRUPPEN]


def _fernkaempfer(truppe: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [u for u in _aktive(truppe) if u["kategorie"] == "Fernkampf"]


def _nahkaempfer(truppe: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [u for u in _aktive(truppe) if u["kategorie"] == "Nahkampf"]


def _schlagkraft(truppe: List[Dict[str, Any]]) -> float:
    return sum(u["sk"] for u in truppe)


def mu_wert(u: Dict[str, Any]) -> float:
    return float(u["mu"] or 0)


# --------------------------------------------------------------- Einzelner Schlag

def _fluchtprobe(u: Dict[str, Any], rng: random.Random) -> bool:
    """Handbuch Seite 23: unter LE 5 entscheidet der Mutwert ueber Weitermachen oder Flucht.

    ANNAHME zur Form: Wurf 1-100 groesser als MU = geflohen; je kleiner der Mutwert, desto
    wahrscheinlicher die Flucht. Das Handbuch nennt keine Formel.
    """
    if u["mu"] is None:
        return False
    return rng.randint(1, 100) > mu_wert(u)


def _pruefe_tot_oder_flucht(u: Dict[str, Any], rng: random.Random,
                            zeilen: List[str]) -> None:
    if not _lebt(u):
        return
    if u["le"] < 1:
        u["tot"] = True
        zeilen.append(f"      {u['name']} ist gefallen.")
    elif u["le"] < 5 and _fluchtprobe(u, rng):
        u["geflohen"] = True
        zeilen.append(f"      {u['name']} hat LE unter 5 und flieht (Mutprobe verloren).")
    elif u["le"] < 5:
        zeilen.append(f"      {u['name']} hat LE unter 5, bleibt aber (Mutprobe bestanden).")


def _ein_schlag(angreifer: Dict[str, Any], verteidiger: Dict[str, Any],
                rng: random.Random, zeilen: List[str]) -> bool:
    """Ein einzelner Angriff nach Handbuch Seite 22/23. True = es kam Schaden an."""
    wurf = rng.randint(1, 100)
    if wurf > angreifer["at"]:
        zeilen.append(f"      {angreifer['name']} greift {verteidiger['name']} an — "
                      f"Wurf {wurf} gegen AT {angreifer['at']:.0f}: verfehlt.")
        return False
    parade = rng.randint(1, 100)
    if parade <= verteidiger["pa"]:
        zeilen.append(f"      {angreifer['name']} trifft {verteidiger['name']} (Wurf {wurf}), "
                      f"abgewehrt (Wurf {parade} gegen PA {verteidiger['pa']:.0f}).")
        return False
    schaden = rng.randint(int(angreifer["tp_min"]), int(angreifer["tp_max"]))
    schaden = max(1, schaden - int(verteidiger["rs"]))       # mindestens 1 Schadenspunkt
    verteidiger["le"] -= schaden
    zeilen.append(f"      {angreifer['name']} trifft {verteidiger['name']} (Wurf {wurf}), "
                  f"nicht abgewehrt (Wurf {parade} gegen PA {verteidiger['pa']:.0f}): "
                  f"{schaden} Schaden, LE {verteidiger['le']:.0f}")
    _pruefe_tot_oder_flucht(verteidiger, rng, zeilen)
    return True


def _zweikampf(a: Dict[str, Any], b: Dict[str, Any], rng: random.Random,
               zeilen: List[str]) -> Optional[Dict[str, Any]]:
    """Kampfrunden bis einer tot oder geflohen ist (Handbuch Seite 22/23).

    Reihenfolge: hoeherer MU beginnt; bei Gleichstand der Verteidiger (b). Danach ist die
    jeweils andere Einheit an der Reihe. Rueckgabe: Sieger oder None.
    """
    if mu_wert(b) >= mu_wert(a):
        erster, zweiter = b, a
    else:
        erster, zweiter = a, b
    dran, andere = erster, zweiter
    runden = 0
    while _lebt(a) and _lebt(b) and runden < 200:
        runden += 1
        _ein_schlag(dran, andere, rng, zeilen)
        dran, andere = andere, dran                      # "anschliessend ist die andere dran"
    if _lebt(a) and not _lebt(b):
        return a
    if _lebt(b) and not _lebt(a):
        return b
    return None


# --------------------------------------------------------------- Verluste

def _verluste_zaehlen(vorher: List[Dict[str, Any]], nachher: List[Dict[str, Any]]) -> Dict[str, int]:
    """Gefallene je Einheitenname. Geflohene zaehlen nicht (sie kehren zurueck)."""
    verluste: Dict[str, int] = {}
    for name in {u["name"] for u in vorher}:
        a = len([u for u in vorher if u["name"] == name])
        b = len([u for u in nachher if u["name"] == name and not u["tot"]])
        if a - b:
            verluste[name] = a - b
    return verluste


def _geraeteverluste(geraete: List[Dict[str, Any]], sequenzen: int,
                     rng: random.Random) -> Tuple[List[str], List[str]]:
    """Karren und Belagerungswaffen des Verlierers: 40 % + 5 % je Kampfsequenz (Seite 23)."""
    chance = 40 + 5 * sequenzen
    entkommen, geblieben = [], []
    for g in geraete:
        if rng.randint(1, 100) <= chance:
            entkommen.append(g["name"])
        else:
            geblieben.append(g["name"])
    return entkommen, geblieben


# --------------------------------------------------------------- Schlacht

def fuehre_schlacht(angreifer: Dict[str, int],
                    verteidiger: Dict[str, int],
                    wall_stufe: int = 0,
                    wall_zustand: float = 100.0,
                    angreifer_karren: Optional[Dict[str, int]] = None,
                    verteidiger_karren: Optional[Dict[str, int]] = None,
                    vorraete: Optional[Dict[str, float]] = None,
                    rng: Optional[random.Random] = None) -> Dict[str, Any]:
    """Fuehrt eine Schlacht nach Handbuch Seite 20-23 und liefert den Bericht zurueck."""
    rng = rng or random.Random()
    bericht: List[str] = []
    unsicher: List[str] = []

    A = _aufstellen(angreifer)
    V = _aufstellen(verteidiger)
    AK = _aufstellen(angreifer_karren)      # Karren und Belagerungswaffen des Angreifers
    VK = _aufstellen(verteidiger_karren)    # die des Verteidigers (stationiert)
    A_belagerung = [u for u in AK if u["rolle"] == "belagerung"]
    A_transport = [u for u in AK if u["rolle"] == "karren"]

    stufen = {i + 1: s for i, s in enumerate(spieldaten.wallstufen())}
    wall = stufen.get(int(wall_stufe))
    bericht.append(f"Schlacht um eine Siedlung. Wall: Stufe {wall_stufe} "
                   f"({wall['name'] if wall else 'kein Wall'}), Zustand {wall_zustand:.0f} %.")
    bericht.append(f"Angreifer: {len(A)} Kaempfer, {len(A_belagerung)} Belagerungswaffen, "
                   f"{len(A_transport)} Karren. Verteidiger: {len(V)} Kaempfer, "
                   f"{len([u for u in VK if u['rolle'] == 'karren'])} Karren.")

    ergebnis: Dict[str, Any] = {
        "ausgang": "unentschieden", "sequenzen": [], "verluste_angreifer": {},
        "verluste_verteidiger": {}, "geflohen": [], "mauer_zustand": float(wall_zustand),
        "beute": {}, "bericht": "", "unsicher": unsicher, "stand": STAND,
    }

    # ---- 1. Vorrunde (Seite 20/21) ---------------------------------------------------
    if wall is None:
        bericht.append("Kein Wall vorhanden — keine Vorrunde noetig.")
    else:
        schwelle_fuss = float(wall["schwellenwert_fussttruppen"])
        schwelle_bel = wall["schwellenwert_belagerungswaffen"]
        faktor = max(0.0, float(wall_zustand)) / 100.0     # beschaedigter Wall: prozentual weniger
        sk_fuss = _schlagkraft(_fusstruppen(A))
        sk_bel = _schlagkraft(A_belagerung)
        bericht.append(f"Vorrunde: Schlagkraft Fusstruppen {sk_fuss:.0f} gegen Schwelle "
                       f"{schwelle_fuss * faktor:.0f} (Stufe {wall_stufe}, "
                       f"Zustand {wall_zustand:.0f} %).")
        if sk_fuss < schwelle_fuss * faktor:
            bericht.append("Schwelle nicht erreicht — die Truppen ziehen sich zurueck, "
                           "die Schlacht gilt als unentschieden.")
            ergebnis["ausgang"] = "unentschieden"
            ergebnis["bericht"] = "\n".join(bericht)
            return ergebnis
        if schwelle_bel is not None:
            bericht.append(f"Zusaetzlich Belagerungswaffen: Schlagkraft {sk_bel:.0f} gegen "
                           f"Schwelle {float(schwelle_bel) * faktor:.0f}.")
            if sk_bel < float(schwelle_bel) * faktor:
                bericht.append("Belagerungswaffen reichen nicht — Rueckzug, unentschieden.")
                ergebnis["bericht"] = "\n".join(bericht)
                return ergebnis
        else:
            bericht.append("Fuer diese Wallstufe nennt das Handbuch keine Schwelle fuer "
                           "Belagerungswaffen.")

    # ---- 2. Mauerschaden (Seite 21/22) ----------------------------------------------
    if A_belagerung:
        schaden_gesamt = 0
        for waffe in A_belagerung:
            wurf = rng.randint(int(waffe["tp_min"]), int(waffe["tp_max"]))
            rest = max(0, wurf - int(wall_stufe))
            schaden_gesamt += rest
            bericht.append(f"Mauerschaden: {waffe['name']} wuerfelt {wurf}, Ausbaustufe "
                           f"{wall_stufe} abgezogen -> {rest}.")
        neu = max(0.0, float(wall_zustand) - schaden_gesamt)
        bericht.append(f"Mauerzustand {wall_zustand:.0f} % -> {neu:.0f} % "
                       f"(je Belagerungswaffe einzeln ermittelt).")
        ergebnis["mauer_zustand"] = neu
    else:
        bericht.append("Ohne Belagerungswaffen kein Mauerschaden.")

    # ---- 3. Kampfsequenzen (Seite 22) ----------------------------------------------
    A_vorher, V_vorher = list(A), list(V)
    sequenz_nummer = 0
    for sequenz_nummer in range(1, 11):
        # Die Schlacht ist vorbei, sobald eine Armee keine NAHKAMPFeinheiten mehr hat.
        if not _nahkaempfer(A) or not _nahkaempfer(V):
            sequenz_nummer -= 1
            break
        zeile: List[str] = [f"  Sequenz {sequenz_nummer}:"]

        # a) Fernkampf: beide Seiten feuern ZUERST, danach werden die Verluste berechnet.
        schuesse: List[Tuple[Dict[str, Any], Dict[str, Any]]] = []
        for schuetze in _fernkaempfer(A):
            ziele = _fusstruppen(V) or _fernkaempfer(V)
            if ziele:
                schuesse.append((schuetze, rng.choice(ziele)))
        for schuetze in _fernkaempfer(V):
            ziele = _fusstruppen(A) or _fernkaempfer(A)
            if ziele:
                schuesse.append((schuetze, rng.choice(ziele)))
        if schuesse:
            zeile.append(f"    Fernkampf: {len(schuesse)} Schuesse — beide Seiten feuern zuerst.")
        for schuetze, ziel in schuesse:
            if not _lebt(schuetze) or not _lebt(ziel):
                continue                      # Schuetze gefallen oder Ziel schon tot
            _ein_schlag(schuetze, ziel, rng, zeile)

        # b) Nahkampf: nur die ANGREIFENDEN Nahkampfeinheiten stuermen, nacheinander.
        for stuermer in _nahkaempfer(A):
            if not _lebt(stuermer):
                continue
            ziele = _nahkaempfer(V) or _fernkaempfer(V)     # Ausweichen auf Fernkaempfer
            if not ziele:
                break
            ziel = rng.choice(ziele)
            zeile.append(f"    Nahkampf: {stuermer['name']} gegen {ziel['name']}")
            sieger = _zweikampf(stuermer, ziel, rng, zeile)
            if sieger is not None:
                # Erschoepfung je gewonnenem ZWEIKAMPF
                sieger["at"] = max(0.0, sieger["at"] - 1)
                sieger["pa"] = max(0.0, sieger["pa"] - 1)

        bericht.extend(zeile)
        ergebnis["sequenzen"].append("\n".join(zeile))

    if sequenz_nummer == 10 and _aktive(A) and _aktive(V):
        bericht.append("Nach zehn Kampfsequenzen kein Sieger — die Schlacht geht "
                       "unentschieden aus, der Angreifer zieht sich ohne Beute zurueck.")

    ergebnis["verluste_angreifer"] = _verluste_zaehlen(A_vorher, A)
    ergebnis["verluste_verteidiger"] = _verluste_zaehlen(V_vorher, V)
    ergebnis["geflohen"] = ([f"{u['name']} (Angreifer)" for u in A if u["geflohen"]] +
                            [f"{u['name']} (Verteidiger)" for u in V if u["geflohen"]])

    # ---- 4. Ausgang (Seite 23) -------------------------------------------------------
    alle_verteidiger_weg = not _aktive(V)
    alle_angreifer_fuss_weg = not _fusstruppen(A)
    if alle_verteidiger_weg:
        ergebnis["ausgang"] = "angreifer"
        bericht.append("Alle verteidigenden Einheiten tot oder geflohen — der Angreifer siegt.")
    elif alle_angreifer_fuss_weg:
        ergebnis["ausgang"] = "verteidiger"
        bericht.append("Alle angreifenden Fusstruppen tot oder geflohen — der Verteidiger siegt.")
    else:
        ergebnis["ausgang"] = "unentschieden"
        bericht.append("Keine Siegbedingung erfuellt — unentschieden.")
        unsicher.append("Das Handbuch beendet die Schlacht, sobald eine Armee keine "
                        "Nahkampfeinheiten mehr hat, nennt aber keinen Sieger fuer den Fall, "
                        "dass danach noch Einheiten leben (z. B. nur Fernkaempfer). Hier gilt: "
                        "unentschieden. Offene Entscheidung fuer Daniel.")

    # ---- 5. Beute (Seite 23) ---------------------------------------------------------
    if ergebnis["ausgang"] == "angreifer" and A_transport and vorraete:
        kapazitaet = sum(u["ladung"] for u in A_transport if _lebt(u))
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
        bericht.append(f"Pluenderung mit {len(A_transport)} Transportkarren "
                       f"(Kapazitaet {kapazitaet}): {genommen or 'nichts'}.")
    elif ergebnis["ausgang"] == "angreifer":
        bericht.append("Der Angreifer siegt, fuehrt aber keine Transportkarren mit — "
                       "es wird nicht gepluendert.")
    else:
        bericht.append("Kein Angreifersieg — es wird nicht gepluendert.")

    # ---- 6. Karren und Belagerungswaffen des VERLIERERS (Seite 23) --------------------
    if ergebnis["ausgang"] == "verteidiger":
        entkommen, geblieben = _geraeteverluste(AK, sequenz_nummer, rng)
        ergebnis["geraete_verloren"] = geblieben
        ergebnis["geraete_erhalten"] = entkommen
        if AK:
            bericht.append(f"Angreifer verliert Karren und Belagerungswaffen: {len(geblieben)} "
                           f"von {len(AK)} bleiben zurueck "
                           f"(Fluchtchance {40 + 5 * sequenz_nummer} % je Einheit).")
    elif ergebnis["ausgang"] == "angreifer" and VK:
        entkommen, geblieben = _geraeteverluste(VK, sequenz_nummer, rng)
        ergebnis["geraete_verloren_verteidiger"] = geblieben
        ergebnis["geraete_erhalten_verteidiger"] = entkommen
        bericht.append(f"Verteidiger verliert Karren und Belagerungswaffen: {len(geblieben)} "
                       f"von {len(VK)} bleiben zurueck "
                       f"(Fluchtchance {40 + 5 * sequenz_nummer} % je Einheit).")
    elif ergebnis["ausgang"] == "unentschieden" and (AK or VK):
        bericht.append("Unentschieden — alle Karren und Belagerungswaffen bleiben erhalten.")

    ergebnis["bericht"] = "\n".join(bericht)
    return ergebnis
