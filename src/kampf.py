"""Nebelseetal – Kampfsystem des späteren Original-Forumstexts.

Quelle: docs/quellen/Das_Kampfsystem_Neu_Original.odt (Spielerfund 28.10.2026).
NICHT mit dem früheren Handbuchmodell LE/AT/PA verwechseln!
Frühere Implementierung: kampf_alt_handbuch_2009.py (Rückfallsicherung).

Nur der Kampf wird berechnet; die Spielschicht verbucht Verluste, Beute und Wallzustand.
Einzige Quellen für 15 Kampfprofile: die neue Forumsvorlage unten; für SK,
Belagerungs-Schadensintervalle, Ladung, Wall-Schwellen: einheiten/spieldaten.

Neue Parameter für Bogenbau und Schmiedekunst können je Seite übergeben werden.
Fehlende Bot-Forschung ist bewusst Stufe 0 (nicht ohne Beleg verschenken).
"""
from __future__ import annotations

from collections import Counter
import math
import random
from typing import Any, Dict, Optional

import einheiten as E
import spieldaten

STAND = "2026-10-28.GPT-NE01.wissenswertes"

# (Konstitution %, Kampfwert-Min, Kampfwert-Max, Rüstung, Fernkampfchance %, 
#  Erschöpfung durch Treffer, Schwelle zur Kampfunfähigkeit)
# Basis aus 'Das Kampfsystem.odt'; Kampfwert-Spannen nach dem neueren
# 'WeitereWerteKampfsystem.odt' (Tabelle Einheitenwerte, S. 5/6).
# Konflikt Handbuch 2009 (LE/AT/PA) gegen dieses Forum-Original: Registerpunkt 40 in
# docs/PRUEFREGEL_ORIGINAL.md und docs/PRUEFUNG_ENTWURF_WEGZEIT_KAMPF_20261031.md §3.1.
# (Der frueher hier genannte Ort docs/GPT_NE01_*.md existiert nicht - geprueft 31.10.2026.)
PROFILE = {
    "Bürgerwehr": (5, 1, 12, 0, None, 0, 1),
    "Kämpfer": (15, 4, 22, 2, None, 0, 3),
    "Krieger": (25, 7, 29, 4, None, 0, 5),
    "Ritter": (50, 9, 43, 8, None, 0, 7),
    "Paladin": (70, 17, 57, 12, None, 0, 9),
    "Kurzbogenschütze": (15, 1, 12, 0, 20, 1, 1),
    "Bogenschütze": (25, 1, 12, 0, 30, 2, 2),
    "Langbogenschütze": (35, 1, 12, 0, 55, 3, 3),
    "Armbrustschütze": (45, 3, 14, 2, 70, 4, 4),
    "Streuner": (5, 2, 15, 0, None, 0, 1),
    "Gauner": (15, 2, 20, 0, None, 0, 2),
    "Dieb": (25, 2, 25, 0, None, 0, 3),
    "Meisterdieb": (35, 2, 30, 0, None, 0, 4),
    "Kundschafter": (45, 4, 37, 2, None, 0, 5),
    "Waldläufer": (55, 6, 44, 4, None, 0, 6),
}


def _einheiten(aufstellung: Optional[dict], seite: str) -> list:
    result = []
    for name, anzahl in (aufstellung or {}).items():
        if name not in PROFILE:
            continue  # Karren/Belagerung sind keine Kämpfer
        try:
            n = int(anzahl)
        except (ValueError, TypeError, OverflowError):
            continue
        if n <= 0:
            continue
        kon, lo, hi, ruestung, fern, schaden, schwelle = PROFILE[name]
        for _ in range(n):
            result.append({"name": name, "seite": seite, "kon": kon, "lo": lo,
                           "hi": hi, "ruestung": ruestung, "fern": fern,
                           "fern_schaden": schaden, "schwelle": schwelle,
                           "erschoepfung": 0, "tot": False, "inaktiv": False,
                           "rueckzug": False})
    return result


def _aktiv(u):
    return not u["tot"] and not u["inaktiv"] and not u["rueckzug"]


def _nah(truppe):
    return [u for u in truppe if _aktiv(u) and u["fern"] is None]


def _fern(truppe):
    return [u for u in truppe if _aktiv(u) and u["fern"] is not None]


def _alle(truppe):
    return [u for u in truppe if _aktiv(u)]


def _forschungsstufe(forschung: Optional[dict], name: str) -> int:
    w = (forschung or {}).get(name, 0)
    if isinstance(w, dict):
        w = w.get("level", 0)
    elif hasattr(w, "level"):
        w = w.level
    try:
        return max(0, min(10, int(w)))
    except (TypeError, ValueError, OverflowError):
        return 0


def _ausgeschieden(u, rng, protokoll):
    """Konstitutionsprobe (1..100 <= Konstitution => überlebt, aber inaktiv)."""
    if not _aktiv(u) or u["erschoepfung"] < u["schwelle"]:
        return
    u["inaktiv"] = True
    u["tot"] = rng.randint(1, 100) > u["kon"]
    protokoll.append(f"{u['name']}: kampfunfähig durch Erschöpfung "
                     f"({u['erschoepfung']}/{u['schwelle']}), "
                     f"{'gefallen' if u['tot'] else 'überlebt'}")


def _sieggeraete(geraete, sequenzen, rng):
    """Älteres Handbuch: entkommt mit 40% + 5% je Sequenz, unverändert."""
    entkommen, verloren = [], []
    for name, anzahl in (geraete or {}).items():
        if name not in E.alle() or E.rolle(name) not in ("belagerung", "karren"):
            continue
        for _ in range(max(0, int(anzahl))):
            (entkommen if rng.randint(1, 100) <= min(100, 40 + 5 * sequenzen)
             else verloren).append(name)
    return entkommen, verloren


def _beute(karren, vorraete):
    kap = sum(E.ladung(name) * max(0, int(n)) for name, n in (karren or {}).items()
              if E.rolle(name) == "karren")
    lager = {n: max(0.0, float(v)) for n, v in (vorraete or {}).items() if v is not None}
    gesamt = sum(lager.values())
    if kap <= 0 or gesamt <= 0:
        return {}
    entnommen = {}
    rest = kap
    for name in sorted(lager):
        x = min(int(lager[name]), int(kap * lager[name] / gesamt), rest)
        if x > 0:
            entnommen[name] = x
            rest -= x
    return entnommen


def fuehre_schlacht(angreifer: Dict[str, int], verteidiger: Dict[str, int],
                    wall_stufe: int = 0, wall_zustand: float = 100.0,
                    angreifer_karren: Optional[Dict[str, int]] = None,
                    verteidiger_karren: Optional[Dict[str, int]] = None,
                    vorraete: Optional[Dict[str, float]] = None,
                    rng: Optional[random.Random] = None,
                    forschung_angreifer: Optional[dict] = None,
                    forschung_verteidiger: Optional[dict] = None) -> Dict[str, Any]:
    """Führt reproduzierbar eine Schlacht nach der späteren Originalbeschreibung aus.

    Nicht im Dokument geregelte Gerätelager- und Beutemechanik bleibt aus dem
    älteren Handbuch erhalten; siehe GPT-KA01 Quell-/Abweichungsregister.
    """
    if rng is None:
        rng = random.Random()
    stufe = max(0, min(10, int(wall_stufe)))
    zustand = max(0.0, min(100.0, float(wall_zustand)))
    A, V = _einheiten(angreifer, "Angreifer"), _einheiten(verteidiger, "Verteidiger")
    a_wissen = forschung_angreifer or {}
    v_wissen = forschung_verteidiger or {}
    geraet = dict(angreifer_karren or {})
    for n, k in (angreifer or {}).items():
        if E.rolle(n) == "belagerung":
            # Beide Aufrufkonventionen sind erlaubt: Gerät kann im Angreifer-
            # Dict ODER separat übergeben werden. Kein doppeltes Belagerungsgerät.
            geraet.setdefault(n, max(0, int(k)))
    belagerung = {n: k for n, k in geraet.items() if E.rolle(n) == "belagerung"}
    logs = [f"Kampfmodell {STAND}; Wall Stufe {stufe} Zustand {zustand:.1f}%"]
    unsicher = ["Forschungsstand nicht übergeben: Wert 0 statt fiktiver Bot-Forschung"] if (
        forschung_angreifer is None or forschung_verteidiger is None) else []
    result = {"stand": STAND, "ausgang": "unentschieden",
              "kampf_stattgefunden": False, "vorrunde_bestanden": False,
              "sequenzen": [],
              "verluste_angreifer": {}, "verluste_verteidiger": {},
              "geflohen": [], "mauer_zustand": zustand, "beute": {},
              "bericht": "", "unsicher": unsicher}
    def fertig(ausgang):
        result["ausgang"] = ausgang
        result["verluste_angreifer"] = dict(Counter(u["name"] for u in A if u["tot"]))
        result["verluste_verteidiger"] = dict(Counter(u["name"] for u in V if u["tot"]))
        result["geflohen"] = [f"{u['name']} (Angreifer)" for u in A if u["rueckzug"]]
        result["bericht"] = "\n".join(logs)
        return result

    # Ohne Nahkampfeinheiten darf es weder automatischen Sieg noch Beute geben.
    # Ein reiner Fernkampftrupp darf schiessen, erobert aber nichts im Nahkampf.
    if not A:
        logs.append("Keine eigenen Kampfeinheiten: kein Kampf, keine Beute")
        return fertig("unentschieden")

    # Wallvoraussetzung vor der Schlacht; SK und Intervalle bleiben Originaldaten.
    if stufe:
        wall = spieldaten.wallstufen()[stufe - 1]
        # Neu gefundenes Originalforum: die Fußtruppen-Schwelle wird von
        # NAHKAMPFeinheiten überwunden. Fernkämpfer zählen nicht dazu;
        # sonst könnten reine Bogenschützen ohne Sturmtruppen Wall 1 öffnen.
        foot_sk = sum(E.schlagkraft(u["name"]) for u in _nah(A))
        siege_sk = sum(E.schlagkraft(n) * int(k) for n, k in belagerung.items())
        faktor = zustand / 100.0
        if foot_sk < float(wall["schwellenwert_fussttruppen"]) * faktor:
            logs.append("Fußtruppen: Schwelle nicht erreicht; die Truppen ziehen sich zurueck; kein Kampf")
            return fertig("unentschieden")
        schwelle_bel = wall.get("schwellenwert_belagerungswaffen")
        if schwelle_bel is not None and siege_sk < float(schwelle_bel) * faktor:
            logs.append("Belagerungs-Schlagkraft zu gering: Schwelle nicht erreicht; die Truppen ziehen sich zurueck; kein Kampf")
            return fertig("unentschieden")

    result["vorrunde_bestanden"] = True
    result["kampf_stattgefunden"] = True

    # Schutz in Türmen: jeweils beste 10/30 Nahkämpfer des Angreifers.
    schutz = 10 * int(belagerung.get("Belagerungsturm", 0)) + \
             30 * int(belagerung.get("Großer Belagerungsturm", 0))
    geschuetzt = {id(u) for u in sorted(_nah(A),
                 key=lambda u: (u["hi"], u["kon"]), reverse=True)[:max(0, schutz)]}

    # Mauerstufe + 1 echte Vorrunden – selbst ohne Mauer genau eine.
    # Beide Seiten treffen Entscheidungen vor Verrechnung der Rundenerschöpfung.
    for runde in range(stufe + 1):
        schuesse = []
        for schuetze_seite, gegner, wissen, abzug in (
            (A, V, a_wissen, 0.05 * stufe * (zustand / 100.0)),
            (V, A, v_wissen, 0.0),
        ):
            for schuetze in _fern(schuetze_seite):
                ziele = _nah(gegner) or _fern(gegner)
                if not ziele:
                    continue
                ziel = rng.choice(ziele)
                chance = schuetze["fern"] / 100.0 + \
                         0.02 * _forschungsstufe(wissen, "Bogenbau") - abzug
                if schuetze_seite is V and id(ziel) in geschuetzt:
                    chance -= 0.30
                chance = max(0.0, min(1.0, chance))
                if rng.random() < chance:
                    schuesse.append((ziel, schuetze["fern_schaden"]))
        for ziel, schaden in schuesse:
            ziel["erschoepfung"] += schaden
        zeilen = [f"Fernkampf-Vorrunde {runde + 1}/{stufe + 1}: {len(schuesse)} Treffer"]
        for u in A + V:
            _ausgeschieden(u, rng, zeilen)
        logs.extend(zeilen)
        result["sequenzen"].append("\n".join(zeilen))

    # Mauerschaden erst NACH sämtlichen Schussvorrunden: beeinflusst nächsten Kampf.
    mauerschaden = 0
    for name, menge in (belagerung.items() if stufe else ()):
        minimum, maximum = E.mauer_schaden(name)
        for _ in range(max(0, int(menge))):
            if maximum > 0:
                mauerschaden += max(0, rng.randint(minimum, maximum) - stufe)
    result["mauer_zustand"] = max(0.0, zustand - mauerschaden)
    logs.append(f"Mauerschaden nach Fernkampf: {mauerschaden}; Zustand {result['mauer_zustand']:.1f}%")

    ursprung_fern = len(_fern(A))
    rueckzug_je_runde = math.ceil(ursprung_fern * 0.2)
    nahkampf_sequenzen = 0
    for seq in range(1, 11):
        if not _nah(A) or not _alle(V):
            break
        nahkampf_sequenzen = seq
        protokoll = [f"Nahkampf-Sequenz {seq}"]
        # 20 % der ursprünglich vorhandenen angreifenden Schützen ziehen
        # sich je Sequenz zurück, die stärksten zuerst.
        for u in sorted(_fern(A), key=lambda x: (x["fern"], x["kon"]), reverse=True)[:rueckzug_je_runde]:
            u["rueckzug"] = True
            protokoll.append(f"{u['name']} zieht sich zurück")
        for kaempfer in sorted(_nah(A), key=lambda u: (u["hi"], u["kon"])):
            if not _aktiv(kaempfer):
                continue
            ziele = _nah(V) or _fern(V)
            if not ziele:
                break
            ziel = rng.choice(ziele)
            a_wurf = rng.randint(kaempfer["lo"], kaempfer["hi"])
            v_wurf = rng.randint(ziel["lo"], ziel["hi"])
            a_kampf = (a_wurf * (1 + 0.10 * _forschungsstufe(a_wissen, "Schmiedekunst"))
                       - ziel["ruestung"] * (1 + 0.10 * _forschungsstufe(v_wissen, "Schmiedekunst"))
                       - kaempfer["erschoepfung"])
            v_kampf = (v_wurf * (1 + 0.10 * _forschungsstufe(v_wissen, "Schmiedekunst"))
                       - kaempfer["ruestung"] * (1 + 0.10 * _forschungsstufe(a_wissen, "Schmiedekunst"))
                       - ziel["erschoepfung"])
            protokoll.append(f"{kaempfer['name']} {a_kampf:.2f} gegen {ziel['name']} {v_kampf:.2f}")
            loser = [ziel] if a_kampf > v_kampf else ([kaempfer] if a_kampf < v_kampf
                                                       else [kaempfer, ziel])
            for u in loser:
                u["erschoepfung"] = max(u["erschoepfung"], u["schwelle"])
                _ausgeschieden(u, rng, protokoll)
            if len(loser) == 1:
                sieger = kaempfer if loser[0] is ziel else ziel
                if _aktiv(sieger):
                    sieger["erschoepfung"] += 2
                    _ausgeschieden(sieger, rng, protokoll)
        result["sequenzen"].append("\n".join(protokoll))
        logs.extend(protokoll)
        if not _alle(V) or not _nah(A):
            break

    if not _alle(V) and not _nah(A):
        # Kein Sieger, wenn beide Nahkampfseiten gleichzeitig ausscheiden.
        ausgang = "unentschieden"
    elif not _alle(V) and _alle(A):
        ausgang = "angreifer"
    elif not _nah(A):
        ausgang = "verteidiger"
    else:
        ausgang = "unentschieden"
    # Nicht zurückgezogene Schützen werden bei Niederlage überrannt und
    # müssen wie im Forumstext die Konstitutionsprobe bestehen.
    if ausgang == "verteidiger":
        for u in _fern(A):
            u["inaktiv"] = True
            u["tot"] = rng.randint(1, 100) > u["kon"]
            logs.append(f"{u['name']} überrannt: {'gefallen' if u['tot'] else 'entkommen'}")

    if ausgang == "angreifer":
        result["beute"] = _beute(geraet, vorraete)
        ent, verl = _sieggeraete(verteidiger_karren, nahkampf_sequenzen, rng)
        if verteidiger_karren:
            result["geraete_erhalten_verteidiger"] = ent
            result["geraete_verloren_verteidiger"] = verl
    elif ausgang == "verteidiger":
        ent, verl = _sieggeraete(geraet, nahkampf_sequenzen, rng)
        if geraet:
            result["geraete_erhalten"] = ent
            result["geraete_verloren"] = verl
    logs.append(f"Ausgang: {ausgang}; Nahkampf-Sequenzen: {nahkampf_sequenzen}")
    return fertig(ausgang)
