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
from typing import Any, Dict, Optional, Tuple

import einheiten as E
import gebaeude_wirkung as GW
import hilfen

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


# Die Umrechner standen hier UND in `auftraege.py` doppelt (Code-Audit 31.10.2026, Befund P3
# Vorschlag 1). Eine Fassung an einem Ort: `hilfen.py`; die privaten Namen bleiben als Verweis.
_als_zahl = hilfen.als_zahl
_als_int = hilfen.als_int
_aufzaehlung = hilfen.aufzaehlung


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
        grund = ("Kein Wall vorhanden - die Vorrunde entfällt, der Angreifer kann "
                 "vorrücken.")
        if stufe >= 1 and fuss_nenn is None:
            grund = (f"Für Wallstufe {stufe} nennt das Handbuch keine Schwelle - "
                     "die Vorrunde entfällt (kein Wert erfunden).")
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
        grund = (f"Die Schlagkraft der Fußtruppen {fuss_sk:.0f} erreicht die Schwelle "
                 f"{fuss_erf:.0f} nicht - Rückzug, keine Beute.")
        bestanden = False
    elif bel_ok is False:
        grund = (f"Fußtruppen erreichen die Schwelle {fuss_erf:.0f}, aber die Schlagkraft "
                 f"der Belagerungswaffen {bel_sk:.0f} erreicht {bel_erf:.0f} nicht - "
                 "Rückzug, keine Beute.")
        bestanden = False
    else:
        teile = [f"Fußtruppen {fuss_sk:.0f} >= {fuss_erf:.0f}"]
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

# Beute-VORRANG (Daniels Entscheidung, Frage 8, 05.11.2026 - "Gold bevorzugen, Rest anteilig
# auffuellen"). Die Bemessung selbst bleibt gestaffelt; hier kommt nur die Reihenfolge der
# Verladung dazu: Gold darf zuerst bis zu einem Hoechstanteil laden, der Rest wird wie bisher
# anteilig verteilt. Die Regeln stehen in data/beute_vorrang.json (aktiv / gold /
# vorrang_anteil_prozent), damit eine Aenderung keine Codeaenderung ist.
VORRANG: Dict[str, Any] = E.lade_regel("beute_vorrang.json")   # EINE Lesestelle der Regeln
VORRANG_AKTIV = bool(VORRANG.get("aktiv", True))               # Schalter: false = altes Modell
VORRANG_GOLD = str(VORRANG.get("gold") or "gold")              # Schluessel des Vorrangstoffs
VORRANG_ANTEIL = float(VORRANG.get("vorrang_anteil_prozent") or 0.0)  # Hoechstanteil in Prozent


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
                  verteidiger_uebrig: Any = None,
                  forschung: Any = None) -> Dict[str, int]:
    """Beute nach Daniels Staffelung (Registerpunkt 45), mit Gold-Vorrang (Register 214).

    Anteil = BEUTE_STAFFEL_PROZENT[beute_lage(...)], zusaetzlich begrenzt durch
      * die Gesamtladung der mitgefuehrten Karren und
      * den tatsaechlich vorhandenen Vorrat je Rohstoff.
    Die Verteilung auf die Rohstoffe geschieht in ZWEI Schritten (Daniels Entscheidung zur
    Frage 8, 05.11.2026): **Gold laedt zuerst** bis zu `vorrang_anteil_prozent` der
    mitnehmbaren Menge (data/beute_vorrang.json), **der Rest wird anteilig** nach Vorratsmenge
    verteilt. Ohne den Vorrang war es die reine anteilige Verteilung - und die ist es wieder,
    wenn `aktiv` in der Datendatei false ist (dann nimmt dieser Code denselben Weg wie vorher).

    Beispiele (Vorschlagswerte): Wall heil, 1.000 je Rohstoff, Handkarren (Ladung 40)
    -> 10 Prozent = 100, aber nur 40 passen hinein. Ohne Verteidiger -> 100 Prozent,
    begrenzt durch Ladung. Kein Karren -> keine Beute (belegt).
    """
    kapazitaet = E.ladung_der_gruppe(einheiten_des_siegers, forschung)
    if kapazitaet <= 0:
        return {}

    vorhanden: Dict[str, int] = hilfen.positive_ganze_werte(vorraete)
    gesamt = sum(vorhanden.values())
    if gesamt <= 0:
        return {}

    anteil = BEUTE_STAFFEL_PROZENT[beute_lage(wall_zustand_vor, verteidiger_uebrig)] / 100.0
    # Anteilig heisst: gegen die WIRKLICH mitnehmbare Menge rechnen, nicht gegen die ideale.
    # Bisher stand hier `int(anteil_stoff * ziel_menge)` und danach ein Deckel `restplatz` -
    # dadurch frass der alphabetisch erste Rohstoff die ganze Ladung (Befund 31.10.2026 aus
    # `test_kampf_einhaengung`: erwartet Holz 50 / Stein 30, geliefert Holz 80 / Stein 0).
    ziel = min(kapazitaet, int(gesamt * anteil))
    if ziel <= 0:
        return {}
    genommen: Dict[str, int] = {}

    # --- Schritt 1: Gold zuerst, aber nur bis zum Hoechstanteil (Frage 8, Register 214) ---
    # Ohne diese Zeilen gilt sofort der alte Weg: `vorrang` bleibt 0, `uebrig` ist der ganze
    # Vorrat, und Schritt 2 verteilt genau wie vorher. Deshalb bleibt `aktiv=false` der alte Stand.
    vorrang = 0
    if VORRANG_AKTIV and VORRANG_ANTEIL > 0 and VORRANG_GOLD in vorhanden:
        vorrang = min(int(vorhanden[VORRANG_GOLD]), int(ziel * VORRANG_ANTEIL / 100.0))
    if vorrang > 0:
        genommen[VORRANG_GOLD] = vorrang                                 # Gold ist geladen
    uebrig = ({s: m for s, m in vorhanden.items() if s != VORRANG_GOLD}
              if vorrang > 0 else vorhanden)                             # Restvorrat zum Verteilen
    summe_uebrig = sum(uebrig.values())
    rest_ziel = ziel - sum(genommen.values())                            # was noch Platz hat
    if rest_ziel > 0 and summe_uebrig > 0:
        for stoff in sorted(uebrig):
            nimm = min(int(uebrig[stoff] / summe_uebrig * rest_ziel), uebrig[stoff])
            if nimm > 0:
                genommen[stoff] = genommen.get(stoff, 0) + nimm
    # Die alten Zeilen (anteilig ueber ALLE Rohstoffe, nach Vorratsmenge):
    #   for stoff in sorted(vorhanden):
    #       nimm = min(int(vorhanden[stoff] / gesamt * ziel), vorhanden[stoff])
    # Sie stehen hier als Beleg des Vorzustands; mit `aktiv=false` rechnet der Code genauso.
    # Rest, der durch das Abrunden liegen bleibt, nach dem groessten Bestand auffuellen -
    # nie ueber den vorhandenen Vorrat hinaus. So ist die Summe exakt und die Verteilung fair.
    rest = ziel - sum(genommen.values())
    for stoff in sorted(vorhanden, key=lambda s: (-vorhanden[s], s)):
        if rest <= 0:
            break
        platz = vorhanden[stoff] - genommen.get(stoff, 0)
        nimm = min(rest, platz)
        if nimm > 0:
            genommen[stoff] = genommen.get(stoff, 0) + nimm
            rest -= nimm
    return genommen


def _anteil_verladen(anteil: Dict[str, int], lager: Dict[str, float],
                     karren: Dict[str, int], forschung: Any = None) -> Dict[str, int]:
    """Einen bereits berechneten Beuteanteil auf die Karren laden (W-14 Teil 2).

    Warum es diese Funktion gibt: der Drachen-Anteil entsteht in `drachen.beute_anteil` (nach
    Leistung), die TRANSPORTGRENZE gilt aber ueberall gleich. Deshalb wird hier nur noch
    begrenzt: erst die Gesamtladung der Karren, dann je Stoff der vorhandene Vorrat.
    Was nicht hineinpasst, bleibt liegen und steht danach noch im Hort.
    """
    kapazitaet = E.ladung_der_gruppe(karren or {}, forschung)
    if kapazitaet <= 0:
        return {}
    gewuenscht: Dict[str, int] = hilfen.positive_ganze_werte(anteil or {})
    gesamt = sum(gewuenscht.values())
    if gesamt <= 0:
        return {}
    vorhanden: Dict[str, int] = hilfen.positive_ganze_werte(lager or {})
    ziel = min(int(kapazitaet), int(gesamt))
    genommen: Dict[str, int] = {}
    for stoff in sorted(gewuenscht):
        nimm = min(int(gewuenscht[stoff] / float(gesamt) * ziel), gewuenscht[stoff],
                   int(vorhanden.get(stoff, 0)))
        if nimm > 0:
            genommen[stoff] = nimm
    rest = ziel - sum(genommen.values())
    for stoff in sorted(gewuenscht, key=lambda s: (-gewuenscht[s], s)):
        if rest <= 0:
            break
        platz = min(gewuenscht[stoff], int(vorhanden.get(stoff, 0))) - genommen.get(stoff, 0)
        nimm = min(rest, platz)
        if nimm > 0:
            genommen[stoff] = genommen.get(stoff, 0) + nimm
            rest -= nimm
    return genommen


def beute_am_ziel(einheiten_des_siegers: Dict[str, int],
                  vorraete: Dict[str, float],
                  ausgang: Any = "angreifer",
                  wall_zustand_vor: Any = None,
                  verteidiger_uebrig: Any = None,
                  forschung: Any = None,
                  beute_override: Optional[Dict[str, int]] = None
                  ) -> Tuple[Dict[str, int], Dict[str, float]]:
    """Beute berechnen UND beim Ziel abbuchen - Rueckgabe (beute, vorraete_danach).

    Warum es diese Funktion gibt (Befund der externen Gegenpruefung, 31.10.2026, Nr. 6):
    Der Auftrags-Pfad schrieb die Beute dem Spieler gut, ohne sie beim Ziel abzuziehen -
    Gueter aus dem Nichts. Der Bot-Pfad zog ab, rechnete die Menge aber mit einer anderen
    Formel (`kampf._beute`: nur Ladungsgrenze). Jetzt gilt an EINER Stelle:

      * Beute nur bei Angreifersieg (belegt: Handbuch S. 23, Z. 1307-1315),
      * der Anteil kommt aus `beute_staffel` (Wallzustand VOR dem Kampf, ueberlebende
        Verteidiger, Ladung, vorhandener Vorrat),
      * was gutgeschrieben wird, wird beim Ziel abgebucht; kein Bestand wird negativ.
    """
    lager: Dict[str, float] = {}
    for stoff, menge in (vorraete or {}).items():
        wert = _als_zahl(menge)
        lager[str(stoff)] = max(0.0, wert)

    if str(ausgang or "") != "angreifer":
        return {}, lager

    if beute_override is not None:
        # W-14 Teil 2 (05.11.2026): der Drache hat eine EIGENE Beute-Regel (Anteil nach
        # Leistung, `drachen.beute_anteil`). Sie kommt als fertiger Anteil herein und wird hier
        # nur noch auf die Karren geladen und beim Ziel abgebucht - EINE Buchstelle bleibt.
        beute_werte = _anteil_verladen(beute_override, lager, einheiten_des_siegers, forschung)
    else:
        beute_werte = dict(beute_staffel(einheiten_des_siegers, lager,
                                        wall_zustand_vor=wall_zustand_vor,
                                        verteidiger_uebrig=verteidiger_uebrig,
                                        forschung=forschung))
    for stoff, menge in beute_werte.items():
        lager[stoff] = round(max(0.0, lager.get(stoff, 0.0) - float(menge)), 2)
    return beute_werte, lager


def beute(einheiten_des_siegers: Dict[str, int],
          vorraete: Dict[str, float],
          rng: Optional[random.Random] = None,
          forschung: Any = None) -> Dict[str, int]:
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

    kapazitaet = E.ladung_der_gruppe(einheiten_des_siegers, forschung)

    vorhanden: Dict[str, int] = hilfen.positive_ganze_werte(vorraete)

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


# --------------------------------------------------- 3b. Ist das Dorf ausgeraeumt?

def ausgeraeumt(ergebnis: Dict[str, Any]) -> bool:
    """Hat DIESES Gefecht das angegriffene Dorf ausgeraeumt? (Daniel 04.11.2026, Register 197)

    Daniels Definition des Gesamtsiegs, woertlich: "Geprueft erreicht ist der Gesamtsieg, wenn
    jeder Bot und ALLE seine Doerfer mindestens einmal laut Kampfbericht ausgeraeumt wurden."
    "Laut Kampfbericht" heisst: der Bericht, den der Spieler liest, muss den Angriff gewonnen
    haben - der Ausgang ist das einzige, was er ueber den Ort aussagt.

    Deshalb gilt: **`ausgang == "angreifer"`**. NICHT verlangt wird, dass jeder Verteidiger
    gefallen ist: `kampf.fuehre_schlacht` zaehlt als Verlust nur die Toten, wer aus dem Gefecht
    flieht oder erschoepft ausscheidet, steht danach noch im Ort. Eine Bedingung "Garnison muss
    auf 0 stehen" waere damit in der Praxis unerreichbar (gemessen 04.11.2026: 400 Angreifer
    gegen 2 Verteidiger, Ausgang "angreifer", ein Verteidiger geflohen und weiter im Dorf).

    Was hier NICHT steht: wie oft ein Dorf angegriffen werden darf, ob es sich erholt und was
    nach dem Ausraeumen passiert. Daniel: "mindestens einmal" - die Buchung ist ein Merkposten.
    """
    e = ergebnis or {}                                                  # fehlendes Ergebnis = kein Gefecht
    return str(e.get("ausgang") or "") == "angreifer"                    # nur der Sieger raeumt aus


# ---------------------------------------------------------------------------- 4. Bericht

def _aufzaehlung(werte: Dict[str, int]) -> str:
    return hilfen.aufzaehlung(werte)


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
        zeilen.append("Vom Angreifer zurückgelassen: " +
                      ", ".join(str(x) for x in e["geraete_verloren"]) + ".")
    if e.get("geraete_verloren_verteidiger"):
        zeilen.append("Vom Verteidiger zurückgelassen: " +
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
            "kampf.py zählt Nahkampf- UND Fernkampfeinheiten dazu; die engere Lesart "
            "(nur Nahkampf) ist nicht ausgeschlossen.",
        "flucht_formel":
            "Zum Fliehen unter LE 5 nennt das Handbuch nur 'je niedriger der MU, desto "
            "wahrscheinlicher', aber keine Formel.",
        "beute_verteilung":
            "Die Beute ist auf die Karrenladung begrenzt, eine Aufteilung auf die Rohstoffe "
            "ist nicht geregelt. Hier gilt Daniels Entscheidung zur Frage 8 (05.11.2026): "
            "Gold zuerst, der Rest anteilig nach Vorratsmenge.",
        "beute_reihenfolge":
            "In welcher Reihenfolge Rohstoffe verladen werden, ist nicht geregelt. Hier gilt "
            "Daniels Entscheidung zur Frage 8 (05.11.2026, Register 214): Gold zuerst, begrenzt "
            "auf einen Anteil der mitnehmbaren Menge, danach anteilig. Der Anteil steht in "
            "data/beute_vorrang.json.",
        "belagerungsturm_mauerschaden":
            "Belagerungsturm und Großer Belagerungsturm haben Mauerschaden 0-0: sie brechen "
            "keine Mauer, tragen aber Schlagkraft zur Vorrunde bei.",
        "mauer_reparatur":
            "Ob und wie sich eine beschädigte oder eroberte Mauer erholt, sagt das Handbuch "
            "nicht.",
        "vorrunde_wiederholung":
            "Wie viele Versuche ein Angreifer gegen den Wall hat, ist offen.",
        "geraetebeute":
            "Ob erbeutete Karren und Belagerungswaffen mitgenommen werden können, ist nicht "
            "geregelt.",
    }
