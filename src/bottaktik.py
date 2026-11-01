"""
Nebelseetal Remake - Bot-Taktik (Paket BT, 01.11.2026).

Gibt jedem Gegner feste Koordinaten, 1-3 Doerfer, eine Taktik, ein Gedaechtnis
und sichtbare Vorzeichen vor einem Angriff. ERGAENZUNG zu `botkern.py`, kein
Ersatz. Keine KI (Zustandsautomat mit Schwellen), keine Pfadsuche, keine Uhr,
keine Datei - `jetzt` wird uebergeben, Zufall aus `random.Random(seed)`; kein
Fenster, kein main-Import. Schwellen aus dem Entwurf D/G ([VORSCHLAG]-Werte in
`offene_luecken()` benannt, Belegtes als BELEGT markiert). Alle Funktionen sind
rein: `wirkung_anwenden` gibt einen NEUEN Bot zurueck.
"""
from __future__ import annotations

import copy
import random
from typing import Any, Dict, List, Optional

STAND = "2026-11-01.1"

# ------------------------------------------------------------------ Zustaende
SAMMELN, WACHSEN, SICHERN, SUCHEN = "SAMMELN", "WACHSEN", "SICHERN", "SUCHEN"
MARSCHIEREN, RAUBERN, FLIEHEN, RAECHEN = "MARSCHIEREN", "RAUBERN", "FLIEHEN", "RAECHEN"

ZUSTAENDE = {
    SAMMELN: "Rohstoffe aufbauen", WACHSEN: "Dorf ausbauen",
    SICHERN: "Wall und Truppen aufstellen", SUCHEN: "Naehe zum Spieler aufbauen",
    MARSCHIEREN: "Truppen verschieben", RAUBERN: "Angriff",
    FLIEHEN: "Rueckzug nach Niederlage", RAECHEN: "gezielter Gegenschlag",
}

ZUSTANDS_AKTION = {
    SAMMELN: "sammeln", WACHSEN: "wachsen", SICHERN: "sichern", SUCHEN: "suchen",
    MARSCHIEREN: "marschieren", RAUBERN: "raeubern", FLIEHEN: "fliehen",
    RAECHEN: "raechen",
}

# --- Schwellen: VORSCHLAG-Werte siehe offene_luecken; BELEGT nur 20x20 (MAPS).
RASTER = 20
SCHWELLE_SAMMELN_HOLZ = 150        # VORSCHLAG D.1: 1,5x Startspanne 100
SCHWELLE_WACHSEN_PUNKTE = 100      # VORSCHLAG: Entwurf nennt keine Zahl
SCHWELLE_SICHERN_ARMEE = 50        # VORSCHLAG: Staerke = Summe der Truppen
NAHGRENZE_SUCHEN = 5               # VORSCHLAG D.1: Abstand <= 5
RUHE_ZEIT_FLIEHEN = 24 * 3600      # BELEGT: 24-h-Takt (botkern)
AGGRESSION_ZUWACHS_BEI_NIEDERLAGE = 0.1   # VORSCHLAG: nach Niederlage aggressiver
MARSCH_GESCHWINDIGKEIT = 5         # VORSCHLAG: Bot-Tempo, Formel aus auftraege

# ------------------------------------------------------------------ Taktiken
# BELEGT (main.BOTS, botkern.BOT_NAMEN): fuenf Gegner. Daten je Taktik: naehe
# (Naehe/Abstand), abstand_grenze, angriff_schwelle, rueckzug_schwelle,
# zielwahl, erstes_zeichen, blitz (Angriff ohne Ankuendigung), startzustand.
TAKTIKEN: Dict[str, Dict[str, Any]] = {
    "Haug": {"name": "Pluenderer", "naehe": True, "abstand_grenze": 3,
             "angriff_schwelle": 0.4, "rueckzug_schwelle": 0.40,
             "zielwahl": "naechstes schwaches Dorf", "erstes_zeichen": "Spaeher am Rand",
             "blitz": False, "startzustand": SUCHEN},
    "Brynhild": {"name": "Waechterin", "naehe": False, "abstand_grenze": 8,
                 "angriff_schwelle": 0.7, "rueckzug_schwelle": 0.25,
                 "zielwahl": "das Dorf, das ihr zu nah kam",
                 "erstes_zeichen": "sie bleibt fern, kein Spaeher",
                 "blitz": False, "startzustand": SICHERN},
    "Grom": {"name": "Bastionier", "naehe": False, "abstand_grenze": 8,
             "angriff_schwelle": 0.85, "rueckzug_schwelle": 0.15,
             "zielwahl": "Verteidiger, nie Angreifer", "erstes_zeichen": "dauerhaft ruhig",
             "blitz": False, "startzustand": WACHSEN},
    "Silra": {"name": "Spaeherin", "naehe": True, "abstand_grenze": 5,
              "angriff_schwelle": 0.5, "rueckzug_schwelle": 0.60,
              "zielwahl": "erkundet, greift nur bei Schwaeche",
              "erstes_zeichen": "Spaeher und Staubwolke mit Vorlauf",
              "blitz": False, "startzustand": SUCHEN},
    "Krank": {"name": "Raecher", "naehe": False, "abstand_grenze": 0,
              "angriff_schwelle": 0.0, "rueckzug_schwelle": 0.50,
              "zielwahl": "der Schlaeger", "erstes_zeichen": "Nachricht: erzuernt",
              "blitz": True, "startzustand": RAECHEN},
}

_TAKTIK_NEUTRAL: Dict[str, Any] = {"name": "Unbekannt", "naehe": True,
                                   "abstand_grenze": 5, "angriff_schwelle": 0.5,
                                   "rueckzug_schwelle": 0.40, "zielwahl": "naechstes Dorf",
                                   "erstes_zeichen": "Spaeher am Rand", "blitz": False,
                                   "startzustand": SUCHEN}


def taktik_von(bot: Optional[dict]) -> Dict[str, Any]:
    bot = bot if isinstance(bot, dict) else {}
    return TAKTIKEN.get(str(bot.get("name") or "")) or _TAKTIK_NEUTRAL


# ------------------------------------------------------------------ Gedaechtnis
# Entwurf D.3: vier Merker je Bot, mit Defaults fuer alte Spielstaende.
GEDAECHTNIS_DEFAULT: Dict[str, Any] = {"geschlagen_von": None,
                                       "beute_verloren": None,
                                       "staerke_zuletzt": None,
                                       "letzter_kontakt": None}


def gedaechtnis(bot: Optional[dict]) -> Dict[str, Any]:
    bot = bot if isinstance(bot, dict) else {}
    roh = bot.get("gedaechtnis")
    ged = dict(roh) if isinstance(roh, dict) else {}
    for schluessel, wert in GEDAECHTNIS_DEFAULT.items():
        ged.setdefault(schluessel, wert)
    return ged


# ------------------------------------------------------------------ Koordinaten
def _ganzzahl(wert: Any, vorgabe: int = 0) -> int:
    try:
        return int(float(wert))
    except (TypeError, ValueError):
        return int(vorgabe)


def _zahl(wert: Any, vorgabe: float = 0.0) -> float:
    try:
        return float(wert)
    except (TypeError, ValueError):
        return float(vorgabe)


def _klemme(wert: Any, lo: float = 0.0, hi: float = 1.0) -> float:
    w = _zahl(wert, lo)
    return lo if w < lo else (hi if w > hi else w)


def _koordinate(wert: Any) -> Optional[Dict[str, int]]:
    if isinstance(wert, dict):
        if "x" not in wert or "y" not in wert:
            return None
        return {"x": _ganzzahl(wert.get("x"), 0), "y": _ganzzahl(wert.get("y"), 0)}
    if isinstance(wert, (list, tuple)) and len(wert) >= 2:
        return {"x": _ganzzahl(wert[0], 0), "y": _ganzzahl(wert[1], 0)}
    return None


def dorf_positionen(bot: dict, welt: Optional[dict] = None) -> List[Dict[str, int]]:
    """Feste Koordinaten der 1-3 Doerfer, deterministisch aus
    `random.Random("nebel-bot-<name>-<n>")`; gleicher Bot, gleiche Lage."""
    del welt
    bot = bot if isinstance(bot, dict) else {}
    name = str(bot.get("name") or "Bot")
    anzahl = random.Random("nebel-bot-" + name + "-anzahl").randint(1, 3)
    out: List[Dict[str, int]] = []
    for n in range(anzahl):
        rng = random.Random("nebel-bot-" + name + "-" + str(n))
        out.append({"x": rng.randint(0, RASTER - 1), "y": rng.randint(0, RASTER - 1)})
    return out


def bot_position(bot: dict, welt: Optional[dict] = None) -> Optional[Dict[str, int]]:
    """Ein gespeichertes x/y schlaegt die feste Dorflage (fuer Pruefungen)."""
    bot = bot if isinstance(bot, dict) else {}
    fest = _koordinate({"x": bot.get("x"), "y": bot.get("y")})
    if fest is not None:
        return fest
    doerfer = dorf_positionen(bot, welt)
    return doerfer[0] if doerfer else None


def entfernung(a: Any, b: Any) -> int:
    """Manhattan-Abstand |x1-x2| + |y1-y2| - Ersatz fuer die Kartenmitte."""
    pa, pb = _koordinate(a), _koordinate(b)
    if pa is None or pb is None:
        return 0
    return abs(pa["x"] - pb["x"]) + abs(pa["y"] - pb["y"])


def _dorf_name(spielerdorf: Any) -> str:
    if isinstance(spielerdorf, dict) and spielerdorf.get("name"):
        return str(spielerdorf.get("name"))
    return "Spielerdorf"


def _armee_staerke(bot: dict) -> int:
    """VORSCHLAG: Staerke = Summe der Truppen (Bot-Armee ist nicht belegt)."""
    armee = bot.get("armee") if isinstance(bot, dict) else {}
    return sum(max(0, _ganzzahl(k, 0)) for k in armee.values()) if isinstance(armee, dict) else 0


def _marsch_reisezeit(abstand: int, bot: dict) -> float:
    """Reisezeit EINER Strecke mit derselben Formel wie der Spieler (D.5)."""
    import auftraege as A
    tempo = _ganzzahl(bot.get("marsch_geschwindigkeit", 0), 0)
    return A.reisezeit_sekunden(abstand, tempo if tempo > 0 else MARSCH_GESCHWINDIGKEIT)


# ------------------------------------------------------------------ Entscheidung
def _entscheidung(zustand: str, taktik: Dict[str, Any], aktion: str, ziel: Any,
                  signal: Any, grund: str, naechster_zustand: Optional[str] = None,
                  abstand: Optional[int] = None, reisezeit: Optional[float] = None,
                  meldung: str = "", wirkung: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {"zustand": zustand, "taktik": taktik["name"], "aktion": aktion,
            "ziel": ziel, "signal": signal, "grund": grund,
            "naechster_zustand": naechster_zustand or zustand, "abstand": abstand,
            "reisezeit": reisezeit, "meldung": meldung,
            "wirkung": wirkung if wirkung is not None else {}}


def tick(bot: dict, welt: dict, jetzt: float,
         rng: Optional[random.Random] = None) -> Dict[str, Any]:
    """EINE Entscheidung: Aktionen sammeln..raechen/warten; Angriff nur nach
    angekuendigtem Marsch, Ausnahme Raecher (signal = "rache")."""
    rng = rng or random.Random()
    bot = bot if isinstance(bot, dict) else {}
    jetzt = _zahl(jetzt, 0.0)
    taktik = taktik_von(bot)
    name = str(bot.get("name") or "Bot")
    ged = gedaechtnis(bot)

    if not isinstance(welt, dict):
        return _entscheidung(bot.get("zustand") or taktik["startzustand"], taktik,
                             "warten", None, None, "Welt fehlt")

    zustand = bot.get("zustand") or taktik["startzustand"]
    if zustand not in ZUSTAENDE:
        zustand = taktik["startzustand"]

    spielerdorf = _koordinate(welt.get("spielerdorf"))
    spieler_name = _dorf_name(welt.get("spielerdorf"))

    if zustand == RAECHEN:
        if taktik.get("blitz") and ged["geschlagen_von"]:
            ziel = str(ged["geschlagen_von"])
            return _entscheidung(RAECHEN, taktik, "raechen", ziel, "rache",
                                 "gemerkter Schlaeger", SICHERN,
                                 meldung=f"{name} ist erzuernt und greift {ziel} an.")
        return _entscheidung(RAECHEN, taktik, "warten", None, None, "kein Schlaeger gemerkt")

    if spielerdorf is None:
        return _entscheidung(zustand, taktik, "warten", None, None,
                             "kein Spielerdorf in der Welt")

    pos = bot_position(bot, welt)
    abstand = entfernung(pos, spielerdorf) if pos is not None else NAHGRENZE_SUCHEN
    aggr = _klemme(bot.get("aggression", 0.0))

    if zustand == SAMMELN:
        vorraete = bot.get("vorraete") if isinstance(bot.get("vorraete"), dict) else {}
        if _ganzzahl(vorraete.get("holz", 0), 0) >= SCHWELLE_SAMMELN_HOLZ:
            return _entscheidung(SAMMELN, taktik, "sammeln", None, None,
                                 "Vorrat erreicht, wachsen", WACHSEN,
                                 meldung=f"{name} hat genug Holz und waechst.")
        return _entscheidung(SAMMELN, taktik, "sammeln", None, None,
                             "Rohstoffe aufbauen", SAMMELN,
                             meldung=f"{name} sammelt Rohstoffe.")

    if zustand == WACHSEN:
        if _ganzzahl(bot.get("punkte", 0), 0) >= SCHWELLE_WACHSEN_PUNKTE:
            return _entscheidung(WACHSEN, taktik, "wachsen", None, None,
                                 "Punkte erreicht, sichern", SICHERN,
                                 meldung=f"{name} ist ausgebaut und sichert sich.")
        return _entscheidung(WACHSEN, taktik, "wachsen", None, None,
                             "Dorf ausbauen", WACHSEN, meldung=f"{name} baut aus.")

    if zustand == SICHERN:
        if _armee_staerke(bot) >= SCHWELLE_SICHERN_ARMEE and abstand > taktik["abstand_grenze"]:
            return _entscheidung(SICHERN, taktik, "sichern", None,
                                 taktik["erstes_zeichen"], "Armee steht, suchen",
                                 SUCHEN, abstand=abstand,
                                 meldung=f"{name} sichert sich und sucht Naehe.")
        return _entscheidung(SICHERN, taktik, "sichern", None, None,
                             "Wall und Truppen aufstellen", SICHERN, abstand=abstand,
                             meldung=f"{name} sichert sein Dorf.")

    if zustand == SUCHEN:
        if taktik["naehe"]:
            if (abstand <= taktik["abstand_grenze"]
                    and aggr >= taktik["angriff_schwelle"]):
                reisezeit = _marsch_reisezeit(abstand, bot)
                return _entscheidung(SUCHEN, taktik, "marschieren", spieler_name,
                                     "Staubwolke Richtung Ziel", "Schwelle erreicht, Marsch",
                                     MARSCHIEREN, abstand=abstand, reisezeit=reisezeit,
                                     meldung=f"{name} marschiert auf {spieler_name} zu.",
                                     wirkung={"marsch_ankunft": jetzt + reisezeit})
            return _entscheidung(SUCHEN, taktik, "suchen", spieler_name,
                                 taktik["erstes_zeichen"], "Naehe aufbauen", SUCHEN,
                                 abstand=abstand, meldung=f"{name} sucht die Naehe des Spielers.")
        ziel_zustand = taktik["startzustand"]
        if ziel_zustand == RAECHEN:
            return _entscheidung(SUCHEN, taktik, "warten", None, None,
                                 "kein Grund zu suchen", RAECHEN, abstand=abstand,
                                 meldung=f"{name} wartet auf einen Grund.")
        return _entscheidung(SUCHEN, taktik, ZUSTANDS_AKTION.get(ziel_zustand, "warten"),
                             None, None, "Abstand halten", ziel_zustand, abstand=abstand,
                             meldung=f"{name} haelt Abstand ({taktik['name']}).")

    if zustand == MARSCHIEREN:
        ankunft = _zahl(bot.get("marsch_ankunft"), 0.0)
        if ankunft and jetzt >= ankunft:
            return _entscheidung(MARSCHIEREN, taktik, "raeubern", spieler_name,
                                 "Kampfbericht", "Marsch angekommen", RAUBERN,
                                 abstand=abstand,
                                 meldung=f"{name} trifft ein und greift {spieler_name} an.")
        return _entscheidung(MARSCHIEREN, taktik, "marschieren", spieler_name,
                             "Staubwolke Richtung Ziel", "Truppen unterwegs",
                             MARSCHIEREN, abstand=abstand, meldung=f"{name} ist unterwegs.")

    if zustand == RAUBERN:
        if rng.random() > taktik["rueckzug_schwelle"]:
            vorraete = bot.get("vorraete") if isinstance(bot.get("vorraete"), dict) else {}
            return _entscheidung(RAUBERN, taktik, "raeubern", spieler_name, "Kampfbericht",
                                 "Verluste zu hoch, fliehen", FLIEHEN, abstand=abstand,
                                 meldung=f"{name} erleidet Verluste und flieht.",
                                 wirkung={"flucht_ende": jetzt + RUHE_ZEIT_FLIEHEN,
                                          "geschlagen_von": spieler_name,
                                          "beute_verloren": _ganzzahl(
                                              vorraete.get("holz", 0) * 0.5, 0),
                                          "aggression_delta":
                                              AGGRESSION_ZUWACHS_BEI_NIEDERLAGE})
        return _entscheidung(RAUBERN, taktik, "raeubern", spieler_name, "Kampfbericht",
                             "Beute gemacht, heimkehren", SICHERN, abstand=abstand,
                             meldung=f"{name} pluendert und kehrt heim.")

    if zustand == FLIEHEN:
        flucht_ende = _zahl(bot.get("flucht_ende"), 0.0)
        if flucht_ende and jetzt >= flucht_ende:
            return _entscheidung(FLIEHEN, taktik, "fliehen", ged["geschlagen_von"], None,
                                 "Ruhe beendet, sichern", SICHERN, abstand=abstand,
                                 meldung=f"{name} erholt sich und sichert sich.")
        return _entscheidung(FLIEHEN, taktik, "fliehen", ged["geschlagen_von"], None,
                             "Rueckzug nach Niederlage", FLIEHEN, abstand=abstand,
                             meldung=f"{name} zieht sich zurueck.")

    return _entscheidung(zustand, taktik, "warten", None, None, "unbekannter Zustand")


def wirkung_anwenden(bot: dict, entscheidung: dict, jetzt: float) -> dict:
    """Schreibt eine Entscheidung in einen NEUEN Bot fort (Eingabe unveraendert,
    tiefe Kopie): naechster Zustand, Marsch-/Flucht-Zeitstempel, letzter Abstand
    und das Gedaechtnis. Nach einer Niederlage wird der Bot aggressiver."""
    neu = copy.deepcopy(bot) if isinstance(bot, dict) else {}
    e = entscheidung if isinstance(entscheidung, dict) else {}
    w = e.get("wirkung") if isinstance(e.get("wirkung"), dict) else {}
    jetzt = _zahl(jetzt, 0.0)

    ged = dict(neu.get("gedaechtnis")) if isinstance(neu.get("gedaechtnis"), dict) else {}
    for schluessel, wert in GEDAECHTNIS_DEFAULT.items():
        ged.setdefault(schluessel, wert)

    naechster = w.get("naechster_zustand") or e.get("naechster_zustand")
    if naechster in ZUSTAENDE:
        neu["zustand"] = naechster

    if "marsch_ankunft" in w:
        ankunft = _zahl(w["marsch_ankunft"], 0.0)
        neu["marsch_ankunft"] = ankunft
        if ankunft > jetzt:
            neu["naechster_marsch_h"] = round((ankunft - jetzt) / 3600.0, 1)
    if "flucht_ende" in w:
        neu["flucht_ende"] = _zahl(w["flucht_ende"], 0.0)
    if e.get("abstand") is not None:
        neu["letzter_abstand"] = _ganzzahl(e["abstand"], 0)

    schlaeger = e.get("geschlagen_von") or w.get("geschlagen_von")
    if schlaeger:
        ged["geschlagen_von"] = str(schlaeger)
        delta = _zahl(w.get("aggression_delta"), AGGRESSION_ZUWACHS_BEI_NIEDERLAGE)
        neu["aggression"] = round(min(1.0, _klemme(neu.get("aggression", 0.0)) + delta), 2)

    beute_weg = e.get("beute_verloren") or w.get("beute_verloren")
    if beute_weg is not None:
        ged["beute_verloren"] = {"menge": _ganzzahl(beute_weg, 0), "zeit": jetzt}
    staerke = e.get("staerke_zuletzt") or w.get("staerke_zuletzt")
    if staerke is not None:
        ged["staerke_zuletzt"] = {"punkte": _ganzzahl(staerke, 0), "zeit": jetzt}
    if e.get("aktion") in ("raeubern", "raechen", "fliehen", "marschieren", "suchen"):
        ged["letzter_kontakt"] = jetzt

    neu["gedaechtnis"] = ged
    return neu


def anzeige(bot: dict) -> str:
    """Eine kurze deutsche Zeile fuer die Oberflaeche, ohne Zahlenwueste."""
    bot = bot if isinstance(bot, dict) else {}
    taktik = taktik_von(bot)
    zustand = bot.get("zustand") or taktik["startzustand"]
    text = f"{taktik['name']} {ZUSTAENDE.get(zustand, zustand)}"
    if bot.get("letzter_abstand") is not None:
        text += f" (Abstand {_ganzzahl(bot['letzter_abstand'])})"
    if bot.get("naechster_marsch_h") is not None:
        text += f", naechster Marsch in {_zahl(bot['naechster_marsch_h']):g} h"
    return text


def pruefe_taktik() -> List[str]:
    """Selbstpruefung ohne Fremdimport: Liste der Verstoesse, leer = gut."""
    verstoesse: List[str] = []
    welt_voll = {"spielerdorf": {"x": 10, "y": 10, "name": "Spielerdorf"}}
    pflicht = ("name", "naehe", "abstand_grenze", "angriff_schwelle",
               "rueckzug_schwelle", "zielwahl", "erstes_zeichen", "blitz",
               "startzustand")
    for bot_name, taktik in TAKTIKEN.items():
        for feld in pflicht:
            if feld not in taktik:
                verstoesse.append(f"Taktik {bot_name} ohne Feld {feld}")

    aktionen = [tick({"name": n, "aggression": 0.6, "x": 10, "y": 6,
                      "zustand": SUCHEN, "gedaechtnis": dict(GEDAECHTNIS_DEFAULT)},
                     welt_voll, 0.0, random.Random(1))["aktion"] for n in TAKTIKEN]
    if len(set(aktionen)) != len(aktionen):
        verstoesse.append(f"Taktiken entscheiden nicht verschieden: {aktionen}")

    if dorf_positionen({"name": "Haug"}, {}) != dorf_positionen({"name": "Haug"}, {}):
        verstoesse.append("dorf_positionen ist nicht deterministisch")
    if dorf_positionen({"name": "Haug"}, {}) == dorf_positionen({"name": "Grom"}, {}):
        verstoesse.append("dorf_positionen zweier Bots sind gleich")

    for bot_name, taktik in TAKTIKEN.items():
        bot = {"name": bot_name, "aggression": 1.0, "x": 0, "y": 0,
               "zustand": taktik["startzustand"], "gedaechtnis": dict(GEDAECHTNIS_DEFAULT)}
        e = tick(bot, {"spielerdorf": {"x": 0, "y": 0, "name": "Spielerdorf"}},
                 0.0, random.Random(9))
        if e["aktion"] in ("raeubern", "raechen") and not taktik["blitz"]:
            verstoesse.append(f"{bot_name}: Blitzangriff ohne Ankuendigung: {e['aktion']}")
    e = tick({"name": "Krank", "aggression": 0.9, "zustand": RAECHEN,
              "gedaechtnis": {"geschlagen_von": "MeinDorf"}}, welt_voll, 0.0, random.Random(9))
    if e["aktion"] != "raechen" or e["signal"] != "rache":
        verstoesse.append(f"Raecher-Ausnahme fehlt: {e}")

    for probe in (None, {}):
        try:
            tick({"name": "Haug"}, probe, 0.0, random.Random(4))
        except Exception as ausnahme:
            verstoesse.append(f"tick wirft bei welt={probe!r}: {ausnahme!r}")

    bot = {"name": "Haug", "aggression": 0.5, "gedaechtnis": dict(GEDAECHTNIS_DEFAULT)}
    vorher = copy.deepcopy(bot)
    wirkung_anwenden(bot, {"aktion": "fliehen", "geschlagen_von": "X",
                           "wirkung": {"aggression_delta": 0.1}}, 1.0)
    if bot != vorher:
        verstoesse.append("wirkung_anwenden veraendert die Eingabe")

    return verstoesse


def offene_luecken() -> Dict[str, str]:
    """Jeder eigene Wert mit Grund - keine Originalzahl wird erfunden."""
    return {
        "taktik_schwellen": "VORSCHLAG (D.2/D.7): Schwellen 0,4/0,7/0,85/0,5 und 15-60 % frei; nur aggression/trading (0-1) belegt.",
        "abstand_grenzen": "VORSCHLAG (D.1/D.2): Nah-/Fern-Grenzen 3/5/8 frei; belegt nur 20x20.",
        "sammel_schwelle": f"VORSCHLAG: SAMMELN-Holz = {SCHWELLE_SAMMELN_HOLZ} (1,5x Startspanne 100).",
        "wachsen_schwelle": f"VORSCHLAG: WACHSEN-Punkte = {SCHWELLE_WACHSEN_PUNKTE}; Entwurf ohne Zahl.",
        "sichern_schwelle": f"VORSCHLAG: SICHERN-Armee = {SCHWELLE_SICHERN_ARMEE} (Truppensumme).",
        "gedaechtnis": "VORSCHLAG (D.3): Rache, Beuteverlust, Staerke-Vergleich = Erfindung fuer Lesbarkeit.",
        "signale": "VORSCHLAG (D.4): Spaeher, Staubwolke, 'erzuernt' = Mechanik der Ankuendigung.",
        "aggression_zuwachs": f"VORSCHLAG: Niederlage +{AGGRESSION_ZUWACHS_BEI_NIEDERLAGE} Aggression; Richtung belegt, Zahl nicht.",
        "marsch_tempo": f"VORSCHLAG: Tempo = {MARSCH_GESCHWINDIGKEIT}; Formel aus auftraege, Bot-Tempo unbelegt.",
        "dorf_anzahl": "VORSCHLAG: 1-3 Doerfer je Bot, deterministisch per Seed.",
    }
