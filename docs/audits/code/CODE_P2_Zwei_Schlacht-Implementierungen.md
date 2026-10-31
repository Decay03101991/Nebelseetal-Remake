# Code-Audit Nebelseetal Remake — Paket P2: Zwei Schlacht-Implementierungen (kampf.py und kampf_alt_handbuch_2009.py)

## Deine Rolle

Du bist Software-Architekt und prüfst einen gewachsenen Python-Code (tkinter-Spiel, deutsch
kommentiert, 18.400 Zeilen Prüfcode). Der Code ist über Monate **angebaut** worden: neue Funktionen
kamen dazu, alte blieben, Doppelungen wurden nie zusammengeführt. Deine Aufgabe ist **nicht**,
Eleganz zu predigen, sondern konkrete, umsetzbare Zusammenführungen zu benennen.

## Harte Regeln (daran wird deine Antwort gemessen)

1. **Das Spiel bleibt unser Spiel.** Kein Verhalten darf sich ändern: keine anderen Zahlen, keine
   anderen Regeln, keine andere Bedienung. Reine Struktur- und Lesbarkeitsarbeit.
2. **Jede Funktion bleibt erhalten**, solange sie aufgerufen wird. Was niemand aufruft, nennst du
   ausdrücklich als „entfernbar" mit Begründung.
3. **Der Prüfcode ist der Beweis.** Zu jedem Vorschlag gehört: welche vorhandene Prüfdatei
   (tests/*.py) muss danach grün bleiben? Wenn keine existiert, sagst du das offen.
4. **Deutsch, ASCII in Code-Kommentaren** (das Projekt hält `src/botkern.py` bewusst ASCII).
5. **Keine erfundenen Zeilenzahlen.** Wenn du eine Ersparnis schätzt, schreib „geschätzt".

## Was das Projekt über sich sagt (gemessen, nicht geschätzt)

* `src/`: 49 Dateien, 21.703 Zeilen, 17.406 Codezeilen, 904 Funktionen/Methoden.
* `main.py` allein: 7.375 Zeilen, 240 Methoden, davon 27 `_render_*`-Methoden.
* Funktionen ab 60 Zeilen: 47 (längste 205 Zeilen, `_render_settlement_map`).
* 58 Sechs-Zeilen-Blöcke stehen mehrfach identisch im Code.
* `kampf.py` (398 Z.) und `kampf_alt_handbuch_2009.py` (401 Z.) enthalten je eine
  `fuehre_schlacht` (188 bzw. 194 Zeilen) — `kampf.py` importiert die alte Fassung.
* Oberfläche: tkinter, alles in einer Klasse; Ansichten `_render_*`, Aufbau `_build_main_ui`.
* Prüfcode: `tests/` 18.418 Zeilen, 98 Dateien, Aufruf über `tools/sammellauf.py`.

## Deine Aufgabe

Es gibt zwei `fuehre_schlacht` (188 und 194 Zeilen) und `kampf.py` importiert die alte Fassung. Stelle fest: was ist in der alten Fassung anders, was wird davon noch gebraucht, und was kann ersatzlos weg? Ziel: **eine** Schlachtfunktion, ohne dass sich das Ergebnis der Kämpfe ändert. Wenn die alte Fassung einen Sonderfall abdeckt, den die neue nicht kennt, benenne ihn genau.

## Der Code

### Datei `src/kampf.py` (398 Zeilen)

```python
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


    """Baut aus der Aufstellungs-Liste die Kaempfer einer Seite; Karren und Belagerung bleiben draussen."""
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


    """Kampffaehig? False, wenn tot, inaktiv (Erschoepfung) oder im Rueckzug."""
    return not u["tot"] and not u["inaktiv"] and not u["rueckzug"]


def _nah(truppe):


    """Alle aktiven Nahkaempfer einer Truppe."""
    return [u for u in truppe if _aktiv(u) and u["fern"] is None]


def _fern(truppe):


    """Alle aktiven Fernkaempfer (mit Fernkampfwaffe) einer Truppe."""
    return [u for u in truppe if _aktiv(u) and u["fern"] is not None]


def _alle(truppe):


    """Alle aktiven Einheiten einer Truppe, egal ob nah oder fern."""
    return [u for u in truppe if _aktiv(u)]


def _forschungsstufe(forschung: Optional[dict], name: str) -> int:


    """Forschungsstufe eines Gebiets - gleich ob als Zahl, Verzeichnis oder Objekt abgelegt."""
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


    """Wie viel Beute die mitgefuehrten Karren aus dem Vorrat tragen koennen (Ladeplaetze mal Anzahl)."""
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


# --------------------------------------------------------------------------------------------
# Was hier NICHT aus der Quelle stammt - jede Zahl mit Ort und Grund (Befunde der externen
# Gegenpruefung vom 31.10.2026, Nr. 9/10/11; vorher standen diese Werte unkommentiert im Code).
# --------------------------------------------------------------------------------------------

def vorschlaege() -> Dict[str, Dict[str, str]]:
    """Selbst gesetzte Werte des Kampfmodells - nichts davon steht so in einer Quelle."""
    return {
        "mauerabzug": {
            "wert": "5 Prozentpunkte Fernkampf-Abzug je Wallstufe, gewichtet mit dem Wallzustand "
                    "(abzug = 0.05 * stufe * zustand/100)",
            "grund": "das Forum nennt einen Mauerabzug, aber KEINE Formel; die lineare "
                     "Interpolation ist eine Auslegung",
            "status": "VORSCHLAG",
            "stelle": "fuehre_schlacht, Zeile mit 'abzug = 0.05 * stufe'",
        },
        "turmschutz": {
            "wert": "ein Belagerungsturm schuetzt 10, ein Grosser 30 Nahkaempfer des Angreifers",
            "grund": "das Forum nennt 'Schutz in Tuermen' ohne Zahl und ohne Bezugsgroesse "
                     "(Prozent oder Stueckzahl) - hier als Stueckzahl gedeutet",
            "status": "VORSCHLAG",
            "stelle": "fuehre_schlacht, Block 'Schutz in Tuermen'",
        },
        "rueckzug_rundung": {
            "wert": "20 Prozent der URSPRUENGLICHEN angreifenden Schuetzen je Vorrunde, aufgerundet "
                    "(math.ceil)",
            "grund": "das Forum nennt '20 Prozent' je Sequenz, aber keine Rundung und keine "
                     "Bezugsbasis",
            "status": "VORSCHLAG",
            "stelle": "fuehre_schlacht, 'rueckzug_je_runde = math.ceil(...)'",
        },
        "kampfwert_spannen": {
            "wert": "PROFILE-Spannen (z. B. Kaempfer 4-22) aus 'WeitereWerteKampfsystem'",
            "grund": "die aeltere Forumstabelle nennt 2-20; der Konflikt ist als Registerpunkt 40 "
                     "gefuehrt, die neuere Tabelle gewinnt (E1)",
            "status": "ZUSAMMENFUEHRUNG",
            "stelle": "PROFILE (Modulkopf)",
        },
        "beute_anteil": {
            "wert": "gestaffelt 10/30/60/100 Prozent nach Wallzustand und ueberlebenden Verteidigern",
            "grund": "das Original kennt nur '100 Prozent, begrenzt durch die Karrenladung'; die "
                     "Staffelung ist Daniels Entscheidung E4 (Hausregel, bewusste Abweichung)",
            "status": "VORSCHLAG",
            "stelle": "kampfbericht.BEUTE_STAFFEL_PROZENT",
        },
    }

```

### Datei `src/kampf_alt_handbuch_2009.py` (401 Zeilen)

```python
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

```


## Ausgabeformat (genau so, nichts anderes)

### 1. Befund in fünf Sätzen
Was ist hier wirklich das Problem — mit Zahlen aus dem Code.

### 2. Vorschläge (Tabelle, absteigend nach Nutzen)

| # | Was | Dateien/Funktionen | Zeilen vorher → nachher | Risiko (klein/mittel/groß) | Beweis: welche Prüfdatei | Reihenfolge |
|---|---|---|---|---|---|---|

### 3. Zusammenführung im Detail
Für die zwei wichtigsten Vorschläge: welche Funktionen verschmelzen zu welcher neuen Funktion,
welche Parameter, welcher Rückgabewert, was passiert mit Sonderfällen. Kein vollständiger Code —
nur Signatur plus drei bis fünf Zeilen Kern.

### 4. Was du NICHT anfassen würdest
Und warum. (Beispiel: Zeichencode der Oberfläche, der auf Pixel wirkt.)

### 5. Ordnung
Wie sähe eine saubere Ordner-/Dateistruktur für diesen Teil aus? Namen der Dateien, was in welche
gehört, und **in welcher Reihenfolge man umzieht, ohne dass Importe brechen**.
