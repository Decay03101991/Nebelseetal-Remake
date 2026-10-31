"""
Nebelseetal Remake - Bot-Kern (Paket W5, 05.10.2026).

Was ein Computergegner ueber die Zeit tut: bauen, forschen, handeln, angreifen, warten.
Reine Logik - kein Fenster, keine Uhr, keine Datei. Die Zeit (`jetzt`, in Sekunden) wird
IMMER uebergeben; alles Zufaellige zieht aus einem uebergebenen `random.Random(seed)`, damit
ein Lauf wiederholbar ist.

Belegte Regeln (ENTWURF_AUFTRAEGE.md, Abschnitt "Bot-KI"; dort als VORSCHLAG aus dem
Design-Entwurf gefuehrt und im Entwurf gegen das Handbuch geprueft):

  * Verhaltenswerte existieren im Spiel: `aggression` und `trading`, je 0.0 bis 1.0
    (BELEGT in `src/main.py`, Klasse `BotPlayer` samt fuenf Beispielgegnern).
  * Angriffstakt: "Pruefung alle 6 bis 24 Stunden." (VORSCHLAG; Konstanten unten).
  * Beute: "50 % der lagernden Rohstoffe, gedeckelt durch die Ladekapazitaet der Karren."
    Die Karrenladungen (40 / 100 / 250 / ...) stehen belegt in `data/units.json`.
  * Handel: Referenzpreis = Beschaffungskosten x 1,2; ein Haendler-Temperament verschiebt
    die Schwelle um +-10 %.

Nichts wird erfunden: jede eigene Zahl ist im Code als VORSCHLAG gekennzeichnet und steht
in `offene_luecken()`. Alle Funktionen sind rein - uebergebene Strukturen werden NICHT
veraendert; `wirkung_anwenden` gibt zu einem Zug einen NEUEN Bot zurueck.
"""
from __future__ import annotations

import copy
import math
import random
from typing import Any, Dict, List, Optional

import einheiten as E
import punkte

STAND = "2026-10-05.1"

# ------------------------------------------------------------------ Konstanten
SEKUNDEN_JE_STUNDE = 3600
SEKUNDEN_JE_TAG = 86400

# ENTWURF_AUFTRAEGE.md "Bot-KI", VORSCHLAG: "Angriffstakt: Pruefung alle 6 bis 24 Stunden."
ANGRIFF_MIN_STUNDEN = 6.0
ANGRIFF_MAX_STUNDEN = 24.0

# ENTWURF_AUFTRAEGE.md, Beutemenge (VORSCHLAG; Handbuch beziffert sie nicht):
# "50 % der lagernden Rohstoffe, gedeckelt durch die Ladekapazitaet der Karren."
BEUTE_ANTEIL = 0.5

# ENTWURF_AUFTRAEGE.md, Handel (VORSCHLAG): Referenzpreis = Beschaffungskosten x 1,2,
# Temperament verschiebt die Schwelle um +-10 %.
HANDEL_AUFSCHLAG = 1.2
TEMPERAMENT_SPANNE = 0.10

# BELEGT in `src/main.py` (`BOTS`): fuenf Gegner mit Fraktion und aggression/trading.
BOT_NAMEN = ["Haug", "Brynhild", "Grom", "Silra", "Krank"]
BOT_FRAKTIONEN = {
    "Haug": "menschlich",
    "Brynhild": "menschlich",
    "Grom": "zwergisch",
    "Silra": "elfisch",
    "Krank": "monster",
}

# VORSCHLAG: Startvorraete und Wagenpark eines frischen Bots. Die Vorlage nennt fuer die
# Bot-Siedlung kein Startinventar; die Spannen sind frei gewaehlt (siehe offene_luecken).
VORSCHLAG_START_VORRAETE = {
    "holz": (100, 600),
    "stein": (50, 400),
    "nahrung": (100, 600),
    "metall": (0, 150),
    "gold": (0, 300),
}
VORSCHLAG_START_KARREN = (0, 3)   # Anzahl des kleinsten Karrens

# VORSCHLAG: Gewichte fuer wirtschaftliche Aktionen, wenn kein Angriff faellig ist.
# Nur der Handelsanteil haengt am belegten `trading`; der Rest ist frei gewaehlt.
_VORSCHLAG_FORSCHEN_ANTEIL = 0.5
_VORSCHLAG_BAUEN_ANTEIL = 0.3    # kumuliert bis 0.8; darueber 'warten'


# ------------------------------------------------------------------ kleine Griffe

def _zahl(wert: Any, vorgabe: float = 0.0) -> float:
    try:
        return float(wert)
    except (TypeError, ValueError):
        return float(vorgabe)


def _ganzzahl(wert: Any, vorgabe: int = 0) -> int:
    try:
        return int(float(wert))
    except (TypeError, ValueError):
        return int(vorgabe)


def _klemme(wert: Any, lo: float = 0.0, hi: float = 1.0) -> float:
    w = _zahl(wert, lo)
    if w < lo:
        return lo
    if w > hi:
        return hi
    return w


def _karren_nach_ladung() -> List[str]:
    """Alle Karren mit Ladung > 0, aufsteigend - Namen kommen aus den Spieldaten."""
    return sorted([n for n in E.nach_rolle("karren") if E.ladung(n) > 0], key=E.ladung)


def _kurz(werte: Optional[dict]) -> str:
    return ", ".join(f"{k} {v}" for k, v in sorted((werte or {}).items()))


# ------------------------------------------------------------------ 1. neue Bots

def bot_punkte(bot: dict) -> int:
    """GESAMTPUNKTE eines Bots nach den belegten Formeln - dieselbe Skala wie beim Spieler.

    BELEGT (Handbuch 2009, Seiten 4-6; Registerpunkte 31/32): Kriegspunkte = Summe der
    Einheitenwerte + Wallstufe hoch drei; Forschungspunkte = Summe der Forschungsstufen hoch
    drei; Gesamtpunkte = (Krieg + Forschung) / 2, abgerundet.

    Warum Gesamtpunkte und nicht Kriegspunkte (Entscheidung Daniel 31.10.2026, Frage 10):
    die Ruhmeshalle und das Goetterschutz-Band vergleichen mit `punktestand()['gesamt']` des
    Spielers. Solange der Bot nur Kriegspunkte fuehrte, wurde Krieg gegen Gesamt verglichen -
    der Bot erschien doppelt so stark, wie er ist.

    Forschung des Bots: hat er `forschung_stufen` (Stufe je Linie), gilt die belegte Formel
    direkt. Sonst zaehlt sein Zaehler `geforscht` als EINE Forschungslinie - VORSCHLAG, weil
    das Handbuch die Bot-Forschung nicht regelt (Bots haben im Remake keine Forschungsstaende).

    Vorher war `punkte` ein WUERFELWERT (`rng.randint(0, 300)`): Rangliste, Ruhmeshalle und
    Schutzband waren Zufall. Diese Funktion ist die EINE Stelle, an der Bot-Punkte entstehen;
    `wirkung_anwenden` schreibt sie nach jeder Aenderung fort.
    """
    bot = bot or {}
    armee = bot.get("armee") if isinstance(bot.get("armee"), dict) else {}
    wall = bot.get("wall_stufe", 0)
    stufen = bot.get("forschung_stufen")
    if not isinstance(stufen, dict):
        versuche = bot.get("geforscht", 0)
        try:
            versuche = int(versuche)
        except (TypeError, ValueError):
            versuche = 0
        stufen = {"Forschung": versuche} if versuche > 0 else {}
    try:
        krieg = int(punkte.kriegspunkte(armee, wall))
        forschung = int(punkte.forschungspunkte(stufen))
    except (TypeError, ValueError):
        return 0
    return (krieg + forschung) // 2


def neue_bots(anzahl: int, rng: Optional[random.Random] = None) -> List[Dict[str, Any]]:
    """Erzeugt `anzahl` neue Bots mit plausiblen, belegten Wertebereichen.

    `aggression` und `trading` stammen gleichverteilt aus [0.0, 1.0] (belegter Bereich),
    `temperament` gleichverteilt aus [-1.0, 1.0] (die Vorlage nennt nur +-10 %, nicht die
    Verteilung - VORSCHLAG). Alles Zufaellige zieht aus `rng`; gleicher Seed -> gleiche Bots.

    `punkte` ist KEIN Zufallswert mehr: jeder Bot startet mit leerer Armee bei 0 Punkten
    (wie der Spieler) und waechst ueber `bot_armee_aufstellen` und `wirkung_anwenden`.
    """
    rng = rng or random.Random()
    try:
        n = int(anzahl)
    except (TypeError, ValueError):
        n = 0
    n = max(0, n)

    karren = _karren_nach_ladung()
    bots: List[Dict[str, Any]] = []
    for i in range(n):
        basis = BOT_NAMEN[i % len(BOT_NAMEN)]
        name = basis if i < len(BOT_NAMEN) else f"{basis}-{i // len(BOT_NAMEN) + 1}"
        vorraete = {}
        for stoff, (lo, hi) in VORSCHLAG_START_VORRAETE.items():
            vorraete[stoff] = rng.randint(lo, hi)
        lager: Dict[str, int] = {}
        if karren:
            lager[karren[0]] = rng.randint(0, VORSCHLAG_START_KARREN[1])
        if len(karren) > 1:
            lager[karren[1]] = rng.randint(0, 1)

        bots.append({
            "id": f"bot-{i + 1}",
            "name": name,
            "fraktion": BOT_FRAKTIONEN.get(basis, "menschlich"),
            "aggression": round(rng.random(), 2),
            "trading": round(rng.random(), 2),
            "temperament": round(rng.uniform(-1.0, 1.0), 2),
            "punkte": 0,          # belegte Formel, siehe `bot_punkte`; waechst mit der Armee
            "wall_stufe": 0,      # Bots haben im Remake keinen eigenen Wall (dokumentiert)
            "ruf": rng.randint(0, 60),
            "vorraete": vorraete,
            "lager": lager,
            "armee": {},
            "letzter_angriff": None,
            "naechster_angriff": 0.0,
            "angriffe": 0,
            "gebaut": 0,
            "geforscht": 0,
            "gehandelt": 0,
        })
    return bots


# ------------------------------------------------------------------ 2. Uebersicht

def bot_uebersicht(bot: dict) -> dict:
    """Ein lesbarer Steckbrief eines Bots fuer die Anzeige. Rein, ohne Zeitbezug."""
    bot = bot or {}
    aggr = _klemme(bot.get("aggression", 0.0))
    trad = _klemme(bot.get("trading", 0.0))
    temp = max(-1.0, min(1.0, _zahl(bot.get("temperament", 0.0))))

    if aggr >= 0.66:
        haltung = "kriegerisch"
    elif aggr >= 0.33:
        haltung = "ausgeglichen"
    else:
        haltung = "friedlich"

    if trad >= 0.66:
        handelsneigung = "kauffreudig"
    elif trad >= 0.33:
        handelsneigung = "mittel"
    else:
        handelsneigung = "zurueckhaltend"

    return {
        "name": bot.get("name"),
        "fraktion": bot.get("fraktion"),
        "aggression": aggr,
        "trading": trad,
        "temperament": round(temp, 2),
        "temperament_prozent": round(temp * TEMPERAMENT_SPANNE * 100.0, 1),
        "haltung": haltung,
        "handelsneigung": handelsneigung,
        "punkte": _ganzzahl(bot.get("punkte", 0)),
        "ruf": _ganzzahl(bot.get("ruf", 0)),
        "naechster_angriff": _zahl(bot.get("naechster_angriff", 0.0)),
        "angriffe": _ganzzahl(bot.get("angriffe", 0)),
        "vorraete": dict(bot.get("vorraete") or {}),
        "lager": dict(bot.get("lager") or {}),
    }


# ------------------------------------------------------------------ 3. Handelspreis

def referenzpreis_aus_beschaffung(beschaffungskosten: float) -> float:
    """Der belegte Referenzpreis: Beschaffungskosten x 1,2 (ENTWURF_AUFTRAEGE.md)."""
    return round(_zahl(beschaffungskosten, 0.0) * HANDEL_AUFSCHLAG, 2)


def handelspreis(referenzpreis: float, temperament: float) -> float:
    """Der Handels-Schwellwert: Referenzpreis mit dem Temperament um +-10 % verschoben.

    `temperament` ist auf [-1.0, 1.0] normiert; +1 entspricht +10 %, -1 entspricht -10 %
    (ENTWURF_AUFTRAEGE.md: "Je Siedlung ein Haendler-Temperament, das die Schwelle um
    +-10 % verschiebt."). Der Referenzpreis selbst (x 1,2) kommt aus
    `referenzpreis_aus_beschaffung`. Werte ausserhalb [-1, 1] werden geklemmt.
    """
    temp = max(-1.0, min(1.0, _zahl(temperament, 0.0)))
    return round(_zahl(referenzpreis, 0.0) * (1.0 + TEMPERAMENT_SPANNE * temp), 2)


# ------------------------------------------------------------------ 4. Beute

def _lagerkapazitaet(lager: Optional[dict]) -> int:
    """Die Tragfaehigkeit des Wagenparks.

    `lager` ist entweder {Karrenname: Anzahl} oder - kurz - {"kapazitaet": Zahl} oder
    {"karren": {...}}. Die Ladungen kommen belegt aus `data/units.json` (40 / 100 / 250 ...).
    """
    if not lager:
        return 0
    l = lager
    if isinstance(l.get("kapazitaet"), (int, float)):
        return max(0, _ganzzahl(l.get("kapazitaet")))
    if isinstance(l.get("karren"), dict):
        l = l.get("karren")
    gesamt = 0
    for name, anzahl in l.items():
        gesamt += E.kapazitaet(name, max(0, _ganzzahl(anzahl)))
    return gesamt


def beute_begrenzen(vorraete: dict, lager: dict, rng: Optional[random.Random] = None) -> dict:
    """Beute = 50 % der Vorraete, gedeckelt durch die Karrenladung (ENTWURF_AUFTRAEGE.md).

    - Von jedem Rohstoff werden 50 % genommen (abgerundet).
    - Zusammen darf das nie mehr sein als die Ladekapazitaet des Wagenparks (`lager`).
    - Reicht die Kapazitaet nicht, wird anteilig nach Vorratsmenge verladen; kein Rohstoff
      bekommt mehr als seine 50 %.

    `rng` wird ausdruecklich NICHT gebraucht: die anteilige Verteilung ist nachvollziehbar
    und nicht zufaellig (dieselbe Regel wie `kampfbericht.beute`). Die Aufteilung auf die
    Rohstoffe ist im Design nicht geregelt - siehe `offene_luecken`.
    """
    del rng  # bewusst ungenutzt: Verteilung ist nicht geregelt -> anteilig, nicht zufaellig
    vorraete = vorraete or {}

    ziel: Dict[str, int] = {}
    for stoff, menge in vorraete.items():
        m = max(0, _ganzzahl(menge))
        if m > 0:
            ziel[stoff] = int(m * BEUTE_ANTEIL)  # 50 %, abgerundet
    gesamt = sum(ziel.values())
    if gesamt <= 0:
        return {}

    kapazitaet = _lagerkapazitaet(lager)
    if kapazitaet <= 0:
        return {}
    if kapazitaet >= gesamt:
        return ziel

    genommen: Dict[str, int] = {}
    rest = kapazitaet
    for stoff in sorted(ziel):
        if rest <= 0:
            break
        anteil = ziel[stoff] / gesamt
        nimm = min(int(anteil * kapazitaet), ziel[stoff], rest)
        if nimm > 0:
            genommen[stoff] = nimm
            rest -= nimm
    return genommen


# ------------------------------------------------------------------ 5. Angriffstakt

def naechster_angriff_moeglich(bot: dict, jetzt: float) -> bool:
    """Darf dieser Bot jetzt angreifen? Nur wenn das Angriffsfenster offen ist.

    `bot['naechster_angriff']` ist ein Zeitstempel in Sekunden. Zu Beginn (0.0) ist das
    Fenster sofort offen. Nach einem Versuch wird es um 6 bis 24 Stunden verschoben.
    """
    bot = bot or {}
    n = _zahl(bot.get("naechster_angriff", 0.0), 0.0)
    j = _zahl(jetzt, 0.0)
    return j >= n


def _naechste_wartezeit(rng: random.Random) -> float:
    """VORSCHLAG-Regel: naechstes Angriffsfenster 6 bis 24 Stunden spaeter."""
    stunden = rng.uniform(ANGRIFF_MIN_STUNDEN, ANGRIFF_MAX_STUNDEN)
    return stunden * SEKUNDEN_JE_STUNDE


# ------------------------------------------------------------------ 6. Ein Zug

def _wirtschaftliche_aktion(trading: float, rng: random.Random) -> str:
    """Waehlt ohne Angriff eine wirtschaftliche Aktion.

    VORSCHLAG: die Wahrscheinlichkeit fuer 'handeln' ist genau das belegte `trading`; der
    Rest verteilt sich frei auf forschen / bauen / warten (`offene_luecken`).
    """
    if rng.random() < _klemme(trading):
        return "handeln"
    r = rng.random()
    if r < _VORSCHLAG_FORSCHEN_ANTEIL:
        return "forschen"
    if r < _VORSCHLAG_FORSCHEN_ANTEIL + _VORSCHLAG_BAUEN_ANTEIL:
        return "bauen"
    return "warten"


def tick(bot: dict, welt: dict, jetzt: float,
         rng: Optional[random.Random] = None) -> Dict[str, Any]:
    """Was dieser Bot jetzt tut.

    Rueckgabe: {'aktion': 'bauen'|'forschen'|'handeln'|'angreifen'|'warten',
                'meldung': str, 'wirkung': {...}}

    `welt` beschreibt die Umgebung; erwartet werden optional:
      'vorraete'       {stoff: menge}   - was beim Ziel zu holen ist (Angriff),
      'referenzpreis'  float            - Grundlage fuer den Handelspreis,
      'lager'          {Karren: Anzahl} - falls der Bot selbst keinen Wagenpark hat.

    Der uebergebene `bot` und `welt` werden NICHT veraendert. Die Aenderungen stehen in
    `wirkung`; `wirkung_anwenden` uebertraegt sie in einen neuen Bot.
    """
    rng = rng or random.Random()
    bot = bot or {}
    welt = welt or {}
    jetzt = _zahl(jetzt, 0.0)

    aggr = _klemme(bot.get("aggression", 0.0))
    trad = _klemme(bot.get("trading", 0.0))
    temp = max(-1.0, min(1.0, _zahl(bot.get("temperament", 0.0))))
    name = bot.get("name") or "Bot"
    wirkung: Dict[str, Any] = {}

    if naechster_angriff_moeglich(bot, jetzt):
        if rng.random() < aggr:
            beute = beute_begrenzen(welt.get("vorraete") or {},
                                    bot.get("lager") or welt.get("lager") or {}, rng)
            wirkung["beute"] = beute
            wirkung["naechster_angriff"] = jetzt + _naechste_wartezeit(rng)
            wirkung["letzter_angriff"] = jetzt
            wirkung["angriffe"] = 1
            if beute:
                meldung = (f"{name} greift an und erbeutet {sum(beute.values())} "
                           f"Einheiten ({_kurz(beute)}).")
            else:
                meldung = f"{name} greift an, findet aber nichts zum Erbeuten."
            return {"aktion": "angreifen", "meldung": meldung, "wirkung": wirkung}

        # Versuch gescheitert: das Fenster weiter schieben, dann wirtschaften.
        wirkung["naechster_angriff"] = jetzt + _naechste_wartezeit(rng)
        grund = "Angriff geprueft, aber nicht zugeschlagen"
    else:
        grund = "Angriffsfenster noch nicht offen"

    aktion = _wirtschaftliche_aktion(trad, rng)
    if aktion == "handeln":
        preis = handelspreis(_zahl(welt.get("referenzpreis", 0.0)), temp)
        wirkung["handelspreis"] = preis
        meldung = f"{name} handelt zum Schwellenpreis {preis}."
    elif aktion == "forschen":
        wirkung["forschung"] = 1
        meldung = f"{name} forscht weiter."
    elif aktion == "bauen":
        wirkung["bau"] = 1
        meldung = f"{name} baut aus."
    else:
        meldung = f"{name} wartet ab ({grund})."

    return {"aktion": aktion, "meldung": meldung, "wirkung": wirkung}


def wirkung_anwenden(bot: dict, ergebnis: dict) -> dict:
    """Schreibt die `wirkung` eines Zuges in einen NEUEN Bot fort (Eingabe bleibt unberuehrt).

    Beute wandert in die Vorraete, Angriffe werden gezaehlt und das naechste Angriffsfenster
    uebernommen. Das ist der einzige Ort, an dem sich ein Bot aendert.
    """
    neu = copy.deepcopy(bot) if bot else {}
    w = (ergebnis or {}).get("wirkung") or {}

    for stoff, menge in (w.get("beute") or {}).items():
        if not isinstance(neu.get("vorraete"), dict):
            neu["vorraete"] = {}
        neu["vorraete"][stoff] = _ganzzahl(neu["vorraete"].get(stoff, 0)) + _ganzzahl(menge)
    if "naechster_angriff" in w:
        neu["naechster_angriff"] = _zahl(w["naechster_angriff"])
    if "letzter_angriff" in w:
        neu["letzter_angriff"] = w["letzter_angriff"]
    if w.get("angriffe"):
        neu["angriffe"] = _ganzzahl(neu.get("angriffe", 0)) + _ganzzahl(w["angriffe"])
    if w.get("forschung"):
        neu["geforscht"] = _ganzzahl(neu.get("geforscht", 0)) + 1
    if w.get("bau"):
        neu["gebaut"] = _ganzzahl(neu.get("gebaut", 0)) + 1
    # Punkte werden NICHT fortgeschrieben, sondern nach jeder Aenderung neu gerechnet
    # (belegte Formel aus Einheiten und Wall, `bot_punkte`). Damit kann `punkte` nie
    # von der Armee abweichen - die alte Wuerfelzahl konnte das dauerhaft.
    neu["punkte"] = bot_punkte(neu)
    return neu


# ------------------------------------------------------------------ 7. Alle Bots

def bots_tick(bots: list, welt: dict, jetzt: float,
              rng: Optional[random.Random] = None) -> dict:
    """Laesst alle Bots einen Zug machen - sortiert, mit Kurzfassung fuer 'Nachrichten'.

    Rueckgabe:
      {'anzahl', 'ergebnisse' (nach Name/Fraktion sortiert),
       'nachrichten' (Liste der Meldungen), 'aktionen' (Zaehler je Aktion), 'text'}
    """
    rng = rng or random.Random()
    liste = list(bots or [])
    ergebnisse: List[Dict[str, Any]] = []
    for bot in liste:
        e = tick(bot, welt, jetzt, rng)
        e["bot"] = (bot or {}).get("name") or "Bot"
        e["fraktion"] = (bot or {}).get("fraktion")
        ergebnisse.append(e)

    ergebnisse.sort(key=lambda e: (str(e.get("bot")), str(e.get("fraktion") or "")))

    zaehler: Dict[str, int] = {}
    for e in ergebnisse:
        zaehler[e["aktion"]] = zaehler.get(e["aktion"], 0) + 1

    nachrichten = [e["meldung"] for e in ergebnisse]
    return {
        "anzahl": len(liste),
        "ergebnisse": ergebnisse,
        "nachrichten": nachrichten,
        "aktionen": zaehler,
        "text": "\n".join(nachrichten),
    }


# ------------------------------------------------------------------ 8. Offene Luecken

def offene_luecken() -> Dict[str, str]:
    """Was der Design-Entwurf NICHT regelt - jede hier gesetzte Zahl ist ein Vorschlag."""
    return {
        "angriffswahrscheinlichkeit":
            "VORSCHLAG: Bei offenem Fenster schlaegt der Bot mit Wahrscheinlichkeit = "
            "`aggression` zu. Der Entwurf nennt nur den Pruefrhythmus (6-24 h), keine "
            "Trefferwahrscheinlichkeit.",
        "angriffsintervall":
            "VORSCHLAG aus dem Entwurf: Pruefung alle 6 bis 24 Stunden; die genaue Wartezeit "
            "wird je Versuch gleichverteilt gezogen. Das Handbuch beziffert sie nicht.",
        "aktionsgewichte":
            "VORSCHLAG: ohne Angriff ist P(handeln) = `trading`; der Rest verteilt sich "
            "50/30/20 auf forschen / bauen / warten. Der Entwurf nennt keine Gewichte.",
        "startinventar":
            "VORSCHLAG: Startvorraete und Wagenpark eines neuen Bots (siehe "
            "VORSCHLAG_START_VORRAETE / VORSCHLAG_START_KARREN). Der Entwurf nennt kein "
            "Startinventar.",
        "temperament_verteilung":
            "VORSCHLAG: Temperament gleichverteilt aus [-1, 1] (+-10 %). Der Entwurf nennt "
            "nur die Spanne, nicht die Verteilung.",
        "namen_ab_sechs":
            "VORSCHLAG: nur fuenf Gegnernamen sind belegt (main.BOTS). Ab dem sechsten Bot "
            "wird der Name mit einer laufenden Nummer ergaenzt.",
        "naechster_angriff_startwert":
            "VORSCHLAG: ein frischer Bot hat 'naechster_angriff' = 0, sein erstes Fenster ist "
            "also sofort offen. Der Entwurf nennt keinen Startzeitpunkt.",
        "beute_rundung":
            "VORSCHLAG: die 50 % werden abgerundet (ganzzahlig). Der Entwurf nennt keine "
            "Rundung.",
        "beute_aufteilung":
            "Nicht geregelt: wie die 50 % auf die einzelnen Rohstoffe und in welcher "
            "Reihenfolge verladen werden. Hier: anteilig, Reihung alphabetisch.",
        "lager_erkennung":
            "Nicht geregelt: welcher Wagenpark einem Bot gehoert. `lager` wird als "
            "{Karrenname: Anzahl}, {'kapazitaet': Zahl} oder {'karren': {...}} gelesen.",
        "referenzpreis_quelle":
            "Nicht geregelt: woher der Beschaffungspreis eines Bots stammt. `tick` nutzt "
            "welt['referenzpreis'], sonst 0.",
    }


# ------------------------------------------------------------------ 9. Oekonomie: Kartenwahl und Angebot
# Entwurf Schritt 8 (Z. 717-753). Reine Funktionen: sie rechnen nur und veraendern nichts.
# `spieloekonomie` wird ERST in der Funktion geladen, damit dieser Kern ohne den
# Oekonomiekern importierbar bleibt (und umgekehrt kein Ring entsteht).
#
# Preisregel des Entwurfs (Z. 750): der Preis gilt fuer die KONKRET angebotene Ware, nicht als
# pauschaler Preis fuer alle Rohstoffe. Er kommt aus dem LOKALEN Schattenpreis dieses Ortes
# (`spieloekonomie.schattenpreis`), wird auf den Beschaffungspreis umgerechnet und erst dann mit
# dem Temperament des Bots gewichtet.
#
# Keine Zugaben: was hier herauskommt, ist ein ANGEBOT (Kennung / Menge / Preis). Gebucht wird
# nichts - das tun die bestaetigten Auftraege (`transport_start` und das Handels-Paar).


def oekonomie_kartenwahl(stufe: str, eigene_karten: list, freie_karten: dict,
                         raten: dict, bedarf: dict, regeln: dict):
    """Welche freie Karte soll dieser Bot bilden? Liefert die Kennung oder ``None``.

    ``regeln['bots'][stufe]`` entscheidet: **leicht** gruendet nie (``gruenden`` False -> None).
    **mittel** nimmt die Karte, die den aktuell SCHLECHTEST gedeckten Rohstoff am besten traegt
    (kleinster Wert ``raten/bedarf``; bei Gleichstand entscheidet die Kennung, weil sortiert
    wird). **schwer** nimmt den hoechsten Portfolio-Nutzen ueber die vollstaendige
    Kandidatenliste. Karten mit Besitzer und Karten unter ``ablehnungsnutzen`` fallen weg.
    """
    import spieloekonomie as O

    profil = regeln["bots"][stufe]
    if not profil["gruenden"]:
        return None
    # Der Bot darf bei fehlendem/Null-Bedarf keine Karte "auf Verdacht" nehmen.
    # 0/0 und fehlende Werte fuehrten bisher im Mittel-Modus zum Absturz.
    deckung = {}
    if stufe == "mittel":
        for rohstoff, wert in (bedarf or {}).items():
            try:
                soll = float(wert)
                ist = float((raten or {}).get(rohstoff, 0))
            except (ValueError, TypeError, OverflowError):
                continue
            if not math.isfinite(soll) or soll <= 0:
                continue
            if not math.isfinite(ist) or ist < 0:
                ist = 0.0
            deckung[rohstoff] = ist / soll
        if not deckung:
            return None
        mangel_rohstoff = min(sorted(deckung), key=deckung.get)

    kandidaten = []
    for kennung, eintrag in sorted(freie_karten.items()):
        if eintrag["besitzer"] is not None:
            continue
        nutzen = O.kartennutzen(eigene_karten, eintrag["karte"])
        if stufe == "mittel":
            # Aktuell schwaechste Deckung priorisieren, bei Gleichstand Kennung.
            nutzen = O.kapazitaeten(eintrag["karte"]).get(mangel_rohstoff, 0)
        if nutzen > profil["ablehnungsnutzen"]:
            kandidaten.append((-nutzen, kennung))
    return min(kandidaten)[1] if kandidaten else None


def oekonomie_angebot(stufe: str, karte: dict, rohstoff: str, bestand: float,
                      tagesbedarf: float, temperament: float, regeln: dict) -> dict:
    """Was darf der Bot von ``rohstoff`` anbieten, und zu welchem Preis?

    Der Bot haelt zuerst seine Reserve: ``tagesbedarf * reserve_stunden / versorgung_stunden``.
    Reicht der Bestand nicht darueber hinaus, ist nichts verkaufbar (``verkaufbar`` 0,
    ``preis`` None) - **kein Gratisverkauf auf Kosten der Versorgung**.
    """
    import spieloekonomie as O

    h = regeln["bots"][stufe]["reserve_stunden"]
    reserve = tagesbedarf * h / regeln["versorgung_stunden"]
    if bestand <= reserve:
        return {"verkaufbar": 0, "preis": None, "reserve": reserve}
    p = O.schattenpreis(karte, rohstoff, bestand, reserve)
    ref = referenzpreis_aus_beschaffung(p)
    return {"verkaufbar": math.floor(bestand - reserve),
            "preis": handelspreis(ref, temperament), "reserve": reserve}
