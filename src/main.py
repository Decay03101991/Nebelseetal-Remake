"""
Nebelseetal Remake — Core Game Engine
Single-player, local, portable Windows desktop app.
Multi-map system, trade, combat, research, bots, stationing.
"""
from __future__ import annotations
import copy
import json
import math
import os
import random
import time
import tkinter as tk
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple

from bonus_system import (
    # Nur noch, was main.py wirklich benutzt. Die erfundenen Kampf- und Preisformeln
    # (`get_combat_power`, `get_unit_stats`, `get_building_cost`, `get_map_switch_cost`,
    # `UNIT_BASE`, `UNIT_TRAIN_BASE`, `BUILDING_BASE_COST`, `TIER_SCALE`) sind hier nicht mehr
    # im Spiel: Kaempfe rechnet src/kampf.py, Preise kommen aus data/*.json, Punkte aus src/punkte.py.
    # `get_training_time` ist am 31.10.2026 ebenfalls entfernt: es wurde nie aufgerufen und lieferte
    # frueher stillschweigend 0,5 Minuten fuer jede Einheit (jetzt None = "nicht belegt").
    get_military_multiplier, get_trade_bonus, get_defense_bonus,
)
import einheiten
import hilfen     # B-5: die eine Schreibweise fuer Mengen (Aufzaehlung der Verluste)
import spieldaten
import gelaende
import baumenue_info  # FIX04: historische Rubriken und begruendete Bauangebote
import spielerhilfe  # FIX04c: eingeblendete Einstiegshilfe und jederzeit erreichbare Fragen
import originalkarten  # GPT-OK01: verifizierbarer Kartenkatalog
import gebaeude_wirkung
import gebaeude_optik  # C2-Gebaeude-Optik: Menue-Icons und Menue-Hintergruende (Register 123)
import berater
import tor
import wirtschaft
import boni  # V-5: Volks- und Taktikboni als Zahlen (Datenschicht src/boni.py)
import spielstaende
import spielstand_archiv  # GPT: drei explizite Spielstands-Slots; Altdaten unveraendert
import ausgabemodus  # FIX04j: separate oeffentliche Spielerversion ohne Admin-Einstieg
import admin_teststand  # GPT: nur hinter gesonderter Admin-Pruefung
import admin_oberflaeche  # GPT: separate Bedienoberflaeche, Regelkern in admin_werkzeuge
import speichern   # W8: robustes Speichern/Laden (atomar, geprueft, mit Sicherung)
import punkte      # W6: Forschungs-, Kriegs- und Gesamtpunkte nach den Originalformeln
import kampf       # W2: Vorrunde, Kampfsequenzen, Flucht, Beute (Handbuch S. 20-23)
import kampfbericht  # W2b: Vorrunden-Pruefung, Mauerschaden, Beute, Bericht
import bot_angriffsplanung  # GPT-B01: Original-SK-Zielwahl und ehrliche Bot-Kampfberichte
import botkern     # W5: Bot-Regeln (hier: die Vorschlagsspannen fuer die Vorraete der Bots)
import bottaktik   # S-7: Bot-Verhalten (Zustandsautomat, Taktiken, Volksattribute, Wechsel)
import portalraum  # W5-2: die 20 Dimensionen des Limbus, Raster, Wechselkosten und -sperre
import werkstatt   # W3: die drei Werkstaetten, die 17 Waren und ihre Warteschlangen
import auftraege   # W7: Auftraege (Missionen) mit Reisezeit, Rueckkehr und Bericht
import spionage    # B-5: Spionagebericht, Abwehr und Nachricht (02.11.2026)
import marsch_optik  # M-1: Truppenbewegungen auf der Weltkarte (02.11.2026, Register 140)
import forschung  # W4c: Forschung braucht Zeit - die Stufe steigt erst nach Ablauf
import welt        # W4d: die Weltkarte des Limbus (20 Dimensionen, sechs belegte Welten)
import zeitbasis  # GPT-Z01: lokale Datumsstempel, monotone Laufzeituhr, Nachrichten
import spielzeit   # Spieluhr: der Zeitfaktor (Vorgabe Daniel 05.10.2026, Spielbericht)
import spieloekonomie  # Oekonomie-Paket Schritt 9: Ortslager, Gruendungskosten, Verbrauch je Ort
import spielschicht  # S-3: der Bau- und Ausbauweg des Spielers (Bots bauen durch dieselbe Funktion)
import versorgungsschutz  # GPT extern: Softlock-Praevention fuer neue lokale Partien
import dorfwall  # GPT extern W-02: ein Wallzustand je Ort, originaltreue Schwellen
# Feinere Kartenoptik (Kinder-Arbeit vom 05.10.2026, vom Koordinator nachgerechnet): beide Module
# liefern Zeichenplaene als DATEN und zeichnen sie ueber `zeichne` auf eine beliebige Leinwand.
# Sie ersetzen die duennen Einzelstriche der ersten Fassung — Siedlungskarte UND Weltkarte.
import karten_optik   # Siedlungskarte: der Renderer (`zeichne`) fuer beide Plan-Fassungen
import welt_optik     # Weltkarte: der Renderer (`zeichne`) fuer beide Plan-Fassungen
# Zweite astra-Auswertung (05.10.2026) — die FEINERE Fassung. Beide Module liefern nur Plaene
# (Daten), gezeichnet werden sie mit `karten_optik.zeichne` bzw. `welt_optik.zeichne`.
import originalkarten_grafik  # Authentische Kartenhintergruende aus 127 Originalbildern
import karten_optik_fein   # Baukoerper 44x46, Ufer nur an echten Grenzen, Wege, Leiste, Pips
import welt_optik_fein     # zusammenhängende Landschaften, Ortssilhouetten, Panelmasse
# Vorgabe Daniel 05.10.2026: Einheiten brauchen ihre AUSRUESTUNG, nicht nur die Forschung.
# `ausruestung` liest den Warenbedarf aus data/units.json und rechnet Fehlmengen und Verbrauch.
import ausruestung
import forschungspfad  # Forschung: was jetzt geht, was blockiert ist und was es freischaltet


# ---------- Data Models ----------

def rueckmarsch_eintrag(bewegung: dict, jetzt: float) -> dict:
    """Baut den Bewegungseintrag fuer den Rueckweg einer Truppe - oder gibt None zurueck.

    Regeln (E3, Daniel 31.10.2026, Frage 14):
      * Der Rueckweg dauert genau so lange wie der Hinweg (Dauer = Ankunft - Start).
      * Start und Ziel werden getauscht, die Truppen bleiben dieselben.
      * Ein Rueckmarsch erzeugt KEINEN weiteren Rueckmarsch (kein Kreislauf).
      * Ohne messbare Dauer (0 oder negativ) gibt es keinen Rueckmarsch - die Truppen sind
        sofort wieder da (dann bucht der Aufrufer sie direkt ein).

    Rueckgabe: neuer Eintrag (dict) oder None.
    """
    if not isinstance(bewegung, dict) or bewegung.get("rueckweg"):
        return None
    try:
        dauer = float(bewegung.get("arrival") or 0.0) - float(bewegung.get("start") or 0.0)
    except (TypeError, ValueError):
        return None
    if dauer <= 0.0:
        return None
    return {
        "from": bewegung.get("to"),
        "to": bewegung.get("from"),
        "units": dict(bewegung.get("units") or {}),
        "start": float(jetzt),
        "arrival": float(jetzt) + dauer,
        "map": bewegung.get("map"),
        "target_bot": None,
        "tile_key": bewegung.get("from"),
        "rueckweg": True,
    }


@dataclass
class Resource:
    name: str
    amount: float = 0.0

@dataclass
class Building:
    id: str
    name: str
    level: int = 0
    base_cost: Dict[str, float] = field(default_factory=dict)
    production: Dict[str, float] = field(default_factory=dict)
    description: str = ""

@dataclass
class Unit:
    id: str
    name: str
    attack: int = 0
    defense: int = 0
    cost: Dict[str, float] = field(default_factory=dict)
    training_time: float = 0.0
    description: str = ""
    count: int = 0
    rolle: str = ""          # kaempfer | kundschafter | karren | belagerung (einheiten.py)

@dataclass
class Research:
    id: str
    name: str
    level: int = 0
    max_level: int = 5
    cost: Dict[str, float] = field(default_factory=dict)
    effect: str = ""

@dataclass
class MapTile:
    x: int
    y: int
    terrain: str
    discovered: bool = False
    resources: Dict[str, float] = field(default_factory=dict)
    npc_faction: Optional[str] = None
    quest: Optional[str] = None
    quest_done: bool = False
    sector: Optional[str] = None
    sector_name: Optional[str] = None

@dataclass
class Goods:
    name: str
    icon: str
    base_cost: Dict[str, int] = field(default_factory=dict)
    description: str = ""


GOODS: Dict[str, Goods] = {
    "brot": Goods("Brot", "🍞", {"nahrung": 20}, "Grundnahrungsmittel."),
    "bier": Goods("Bier", "🍺", {"nahrung": 30}, "Getränk für die Bevölkerung."),
    "holzplanken": Goods("Holzplanken", "🪵", {"holz": 40}, "Baumaterial."),
    "steinblöcke": Goods("Steinblöcke", "🧱", {"stein": 40}, "Baumaterial."),
    "eisenbarren": Goods("Eisenbarren", "🔩", {"metall": 40}, "Metallverarbeitung."),
    "stoffballen": Goods("Stoffballen", "🧶", {"wolle": 30}, "Textil."),
    "glas": Goods("Glas", "🔮", {"mana": 30}, "Magisches Glas."),
    "goldmünzen": Goods("Goldmünzen", "🪙", {"gold": 50}, "Währung."),
    "buch": Goods("Buch", "📕", {"mana": 40}, "Wissen aufschreiben."),
    "zaubertrank": Goods("Zaubertrank", "🧪", {"mana": 50}, "Magisch."),
    "schwert": Goods("Schwert", "⚔️", {"metall": 40, "holz": 20}, "Waffe."),
    "rüstung": Goods("Rüstung", "🛡️", {"metall": 50, "leder": 30}, "Schutz."),
    "pfeil": Goods("Pfeil", "➳", {"holz": 20, "metall": 10}, "Munition."),
    "katapultmunition": Goods("Katapultmunition", "💣", {"stein": 30, "holz": 20}, "Belagerung."),
    "medizin": Goods("Medizin", "💉", {"mana": 35}, "Heilung."),
    "seide": Goods("Seide", "👘", {"wolle": 40, "gold": 30}, "Luxus."),
    "trank": Goods("Trank", "🧪", {"mana": 20, "nahrung": 10}, "Stärkung."),
}

@dataclass
class BotDorf:
    """EIN Dorf eines Bots - Stufe B-1 (02.11.2026, Konzept K-1 Abschnitt 5).

    Bis heute fuehrte ein Bot nur NAMEN seiner Doerfer (`BotPlayer.settlements`) und EINEN
    gemeinsamen Vorrat. Fuer Dorf-Taktiken (jedes Dorf waehlt und wechselt seine Taktik) braucht
    es je Dorf einen eigenen Datensatz. Diese Klasse ist der Traeger; in B-1 haelt sie nur die
    Werte, die der Bot bisher EINMAL hatte (Wall, Ausbaustaende, Taktik-Slot). Die Wirtschaft je
    Dorf und die Kopplung an die Volksboni folgen in den naechsten Schnitten.

    Felder und ihre Herkunft:
      name          - der bisherige Siedlungsname des Bots (nichts erfunden)
      hauptdorf     - True fuer das erste Dorf; es traegt nach Daniels Entscheidung (02.11.2026)
                      die Basiswerte des Volkes und gibt KEINEN Taktik-Punkt
      taktik        - leer = noch keine Taktik gewaehlt (B-2); keine Vorgabe erfinden
      taktik_seit   - Spielsekunden der letzten Wahl, fuer die Sperrzeit (B-2)
      wall_stufe/zustand, gebaut, geforscht - aus dem Bot uebernommen, damit alte Spielstaende
                      verlustfrei weiterlaufen
      vorraete      - SEIT B-3 (02.11.2026) der FUEHRENDE Speicher dieses Dorfes: hier liegen die
                      Rohstoffe, die das Dorf erwirtschaftet hat und die es bezahlen kann. Die
                      Bot-Kasse (`BotPlayer.vorraete`) ist nur noch die SUMME dieser Doerfer.
      ernte_seit    - Spielsekunden der letzten Ernte dieses Dorfes; 0 = noch nie geerntet.
                      Ein alter Spielstand bekommt 0 und damit beim ersten Takt KEINE
                      nachtraegliche Gutschrift fuer die ganze Vergangenheit.
    """
    name: str
    x: int = 0
    y: int = 0
    # W-1 (Daniel 03.11.2026, "mach es in sinnvoller reihenfolge"; docs/VORGABEN_WELTEN_UND_BOTS):
    # `herkunftswelt` ist die Welt, in der das Dorf ENTSTANDEN ist, und wird nie geaendert. Das
    # Hauptdorf bleibt immer dort (W-1); nur ein Nebendorf darf spaeter die Welt wechseln, und dann
    # aendert sich `dimension`, NICHT `herkunftswelt`. 0 heisst "weiss ich nicht" - so laden alte
    # Spielstaende ohne diese Angabe, und die Anzeige filtert dann NICHT (sonst waeren die Doerfer
    # eines alten Standes unsichtbar).
    herkunftswelt: int = 0
    dimension: int = 1
    hauptdorf: bool = False
    taktik: str = ""
    taktik_seit: float = 0.0
    wall_stufe: int = 0
    wall_zustand: float = 100.0
    gebaut: int = 0
    geforscht: int = 0
    vorraete: Dict[str, float] = field(default_factory=dict)
    ernte_seit: float = 0.0
    # B-4 (02.11.2026): die Karte dieses Dorfes. Leer = noch keine Karte vergeben (alter Spielstand) -
    # dann rechnet der Ertrag wie vor B-4 mit der festen Rate, und `bot_doerfer_karten_zuweisen`
    # vergibt beim naechsten Bot-Takt eine.
    karte: str = ""
    # ---------------------------------------------------------------------------------------------
    # S-1 (03.11.2026, Daniels Vorgabe "Bots als echte Gegner"): die Felder eines ORTES.
    # Ein Bot-Dorf soll durch DIESELBEN Funktionen laufen wie eine Spielersiedlung
    # (`wirtschaft.ertrag_gesamt`, `spieloekonomie.ort_tick`, `spielschicht.bauen`/`ausbauen`).
    # Bis hier hatte es nur Vorraete und die Karte als KENNUNG; Bauplaetze, Stufen und
    # Warteschlangen gab es nicht. Alle Felder haben Vorgaben, damit alte Spielstaende laden.
    # `karte` bleibt die KENNUNG (Anzeige, Kartenprofil, Kartenwahl); das RASTER fuer den Kern
    # steht in `karte_daten` und wird von `bot_dorf_als_ort` hineingeschrieben.
    # ---------------------------------------------------------------------------------------------
    karte_daten: dict = field(default_factory=dict)        # 10x10-Raster der Karte (originalkarten.karte)
    bauten: Dict[str, str] = field(default_factory=dict)   # Feld -> Gebaeude, wie beim Spieler
    stufen: Dict[str, int] = field(default_factory=dict)   # Ausbaustufe je Feld
    einheiten: Dict[str, int] = field(default_factory=dict)   # Garnison DIESES Ortes
    bevoelkerung: float = 0.0                              # Siedler des Ortes (Deckel wie beim Spieler)
    waren: Dict[str, int] = field(default_factory=dict)    # Werkstattwaren im Lager
    werkstaetten: Dict[str, dict] = field(default_factory=dict)   # Warteschlangen der Werkstaetten
    ausbildung: list = field(default_factory=list)         # Ausbildungsauftraege dieses Ortes
    forschungsauftrag: Optional[dict] = None               # laufende Forschung dieses Ortes
    produktionsjournal: list = field(default_factory=list) # Erntezeilen (ort_tick)
    fertigjournal: list = field(default_factory=list)      # fertige Waren und Einheiten


@dataclass
class BotPlayer:
    name: str
    faction: str
    aggression: float
    trading: float
    settlements: List[str] = field(default_factory=list)
    army: Dict[str, int] = field(default_factory=dict)
    ruf: int = 0
    noob_protection: bool = True
    last_rename: float = 0.0
    # W5 (botkern): die Felder, mit denen `src/botkern.py` rechnet. Sie sind der EINE Ort, an dem
    # ein Bot Vorräte, Wagenpark und Handels-Temperament führt; `bot_als_dict`/`bot_aus_dict`
    # uebersetzen sie in die dict-Form des Kerns und wieder zurueck (keine zweite Wahrheit).
    temperament: float = 0.0
    # B-3 (02.11.2026): hier stand das Feld `vorraete`. Es ist ENTFALLEN - die Kasse eines Bots ist
    # seit B-3 die SUMME seiner Doerfer (Eigenschaft `vorraete` am Ende dieser Klasse). Ein eigenes
    # Feld waere die zweite Buchfuehrung, die B-1 als Befund festgehalten hat.
    lager: Dict[str, int] = field(default_factory=dict)
    naechster_angriff: float = 0.0
    letzter_angriff: Optional[float] = None
    angriffe: int = 0
    gebaut: int = 0
    geforscht: int = 0
    gehandelt: int = 0
    punkte: int = 0
    # GPT W-03: ein Bot hat derzeit eine abstrakte Hauptsiedlung.
    # Nur als Zwischenstufe; spaeter je Bot-Siedlung in eine eigene Ortsstruktur.
    wall_stufe: int = 0
    wall_zustand: float = 100.0
    # S-7 (bottaktik): der sichtbare Verhaltenszustand je Bot. Alle Felder sind ADDITIV
    # (alte Spielstaende laden ohne sie, Vorgaben greifen). `volksattribute` sind dauerhaft
    # (aus der Fraktion), `verhaltensbonus` befristet (mit Ablaufzeit). Kampf und Punkte
    # bleiben beim botkern-Pfad; hier steht nur, was der Spieler am Bot ERKENNEN kann.
    zustand: str = ""
    gedaechtnis: Dict[str, object] = field(default_factory=dict)
    marsch_ankunft: float = 0.0
    flucht_ende: float = 0.0
    letzter_abstand: Optional[int] = None
    naechster_marsch_h: Optional[float] = None
    wechsel_sperre_bis: float = 0.0
    volksattribute: Dict[str, str] = field(default_factory=dict)
    verhaltensbonus: Dict[str, object] = field(default_factory=dict)
    # B-1 (02.11.2026): je Dorf ein eigener Datensatz (Taktik-Slot, Wall, Ausbau). ADDITIV - alte
    # Spielstaende laden ohne das Feld; `bot_doerfer_sicherstellen` legt es beim Laden aus den
    # bisherigen Siedlungsnamen an, damit nichts verloren geht.
    doerfer: List["BotDorf"] = field(default_factory=list)
    # S-4 (03.11.2026): der WISSENSSTAND des Bots {Gebiet: Stufe} - wie beim Spieler das
    # Reichswissen, waehrend der laufende Auftrag je Dorf haengt (`BotDorf.forschungsauftrag`).
    # ADDITIV: ein alter Spielstand laedt ohne das Feld und forscht ab 0 (kein stiller Vorsprung).
    forschungsstaende: Dict[str, int] = field(default_factory=dict)

    # ---- B-3 (02.11.2026): die Kasse ist KEIN eigenes Feld, sondern die Summe der Doerfer ----

    @property
    def vorraete(self) -> Dict[str, float]:
        """Die Bot-Kasse - gelesen als SUMME der Dorf-Vorrate (B-3, 02.11.2026).

        EINE Wahrheit: Lesen rechnet ueber `bot_kasse`, Schreiben verteilt den neuen Stand ueber
        `bot_kasse_setzen` auf die Doerfer. Ein `bot.vorraete["holz"] -= 10` aendert damit NICHTS
        mehr still (es landet in einem Zwischenergebnis) - gebucht wird ausschliesslich ueber
        `bot_kasse_buchen`. Genau das war der Befund aus B-1: eine zweite Kasse darf es nicht geben.
        """
        return bot_kasse(self)                                            # Summe der Doerfer

    @vorraete.setter
    def vorraete(self, werte) -> None:
        """Setzt die GESAMTkasse eines Bots - gebucht wird dabei auf die Doerfer."""
        bot_kasse_setzen(self, werte)                                     # verteilt, keine zweite Kasse


def bot_doerfer_sicherstellen(bot: "BotPlayer") -> List["BotDorf"]:
    """Legt fuer einen Bot fehlende Dorf-Datensaetze an - einmalig, verlustfrei, idempotent.

    QUELLE der Dorfnamen sind die bisherigen `bot.settlements` (die der Kartenaufbau fuellt). Hat
    ein alter Spielstand keine Namen, entsteht EIN Hauptdorf mit dem bisherigen Standardnamen.
    Uebernommen werden Wall, Wallzustand und die Zaehler, damit ein alter Stand mit Wallstufe 3
    danach dieselbe Wallstufe hat - nur eben an einem Dorf statt am ganzen Bot.
    """
    vorhanden = getattr(bot, "doerfer", None) or []                       # schon angelegte Doerfer
    if vorhanden:                                                         # nichts doppelt anlegen
        sauber = [d if isinstance(d, BotDorf) else BotDorf(**d) for d in vorhanden]   # dict -> Objekt
        bot.doerfer = sauber                                              # eine Form im Speicher
        for dorf in sauber:                                               # S-3: Siedler an EINEM Ort
            bot_siedler_uebernehmen(dorf)                                 # Lagerposten -> Bevoelkerung
        return sauber
    namen = [str(n) for n in (getattr(bot, "settlements", None) or []) if str(n).strip()]  # bisherige Namen
    if not namen:                                                         # alter Stand ohne Namen
        namen = ["%ss Siedlung 1" % bot.name]                             # derselbe Standardname wie bisher
    doerfer: List[BotDorf] = []                                           # Ergebnisliste
    _heimat = int(welt.startwelt_nummer() or 1)                           # W-1: die belegte Heimatwelt
    for i, name in enumerate(namen):                                      # ein Datensatz je Name
        doerfer.append(BotDorf(name=name, hauptdorf=(i == 0),             # das erste Dorf ist das Hauptdorf
                               # W-1/W-2 (Daniel 03.11.2026): ein Bot entsteht in der STARTWELT (Midgard)
                               # und traegt sie als Herkunftswelt. Vorher stand hier die Vorgabe 1
                               # (Armageddon) - die Bots lagen damit in einer Welt, in der niemand
                               # spielte, und die Anzeige zeigte sie trotzdem auf jeder Karte.
                               dimension=_heimat, herkunftswelt=_heimat,
                               wall_stufe=int(getattr(bot, "wall_stufe", 0) or 0),        # Wall uebernehmen
                               wall_zustand=float(getattr(bot, "wall_zustand", 100.0) or 100.0),
                               gebaut=int(getattr(bot, "gebaut", 0) or 0),               # Zaehler uebernehmen
                               geforscht=int(getattr(bot, "geforscht", 0) or 0)))
    bot.doerfer = doerfer                                                 # am Bot festhalten
    return doerfer


def bot_aus_stand(daten: dict) -> "BotPlayer":
    """Baut einen Bot aus einem gespeicherten dict - Doerfer als Objekte, alte Kasse migriert.

    B-1: die Doerfer kommen als dicts aus dem Spielstand und werden wieder Objekte.
    B-3 (02.11.2026): Spielstaende VOR B-3 tragen die Kasse des Bots als eigenes Feld `vorraete`.
    Sie wird hier NICHT verworfen, sondern in die Doerfer uebernommen - ein alter Bot hatte EINE
    Kasse, also landet sie ueber `bot_kasse_setzen` bei seinen Doerfern (Schwerpunkt Hauptdorf).
    Danach fuehrt der Bot kein eigenes Vorratsfeld mehr: `bot.vorraete` liest die Summe.
    """
    werte = dict(daten or {})                                             # Kopie, Eingabe bleibt unberuehrt
    alt_kasse = werte.pop("vorraete", None)                               # die EINE Kasse von vor B-3
    roh = werte.get("doerfer") or []                                      # gespeicherte Doerfer (dicts)
    werte["doerfer"] = [d if isinstance(d, BotDorf) else BotDorf(**d) for d in roh]   # zurueck zu Objekten
    bot = BotPlayer(**werte)                                              # uebrige Felder wie bisher
    if isinstance(alt_kasse, dict) and alt_kasse:                         # alter Stand mit einer Kasse
        bot_kasse_setzen(bot, alt_kasse)                                  # verlustfrei auf die Doerfer
    return bot


# ---------------------------------------------------------------------------------------------------
# B-3 (02.11.2026, Konzept K-1): WIRTSCHAFT JE BOT-DORF
#
# Bis B-2 hatte ein Bot EINE Kasse. Seit B-3 fuehren die DOERFER die Vorrate, die Kasse ist nur noch
# ihre Summe. Diese Funktionen sind die einzigen Stellen, die Bot-Vorrate lesen oder buchen - Kern
# (Ernte, Ausbildung, Handel) und Anzeige (Spionagebericht) gehen durch dieselbe Lesestelle
# (F-04-Muster). Kein zweites Lager, keine zweite Ernteliste.
# ---------------------------------------------------------------------------------------------------

BOT_WIRTSCHAFT_VORGABE: Dict[str, Any] = {                                # Rueckfall ohne Datendatei
    "aktiv": True,                                                        # Wirtschaft eingeschaltet
    "gebaeude_je_dorf": ["holzfaeller", "steinmetz", "farm", "goldmine"],  # je Grundrohstoff eine Art
    "anlagen_je_gebaeude": 3,                                             # Daniels Entscheidung 02.11.2026
    "hoechstvorrat_je_stoff": 20000,                                      # Deckel je Stoff und Dorf
}
_BOT_ERTRAG_CACHE: Dict[tuple, Dict[str, float]] = {}                     # Erträge je Anlagen-Liste


HINTERGRUND_VORGABE: Dict[str, Any] = {          # Rueckfall ohne Datendatei
    "aktiv": True,                                # Bildhintergrund eingeschaltet
    "breite": 980,                                # Flaeche in Pixeln
    "hoehe": 760,                                 # Flaeche in Pixeln
    "abdunkeln_prozent": 25.0,                    # Schleier ueber dem Bild (Vergleichsfassung C)
}


def hintergrund_einstellungen() -> Dict[str, Any]:
    """Masse und Abdunkelung des Bildhintergrunds - die EINE Stelle (B-6, 02.11.2026).

    Gelesen aus `data/gebaeude_motive.json`, Schluessel `ansicht_hintergrund`. Fehlt der Schluessel
    oder die Datei, gilt `HINTERGRUND_VORGABE`; das Spiel laeuft weiter. Daniel stellt die
    Abdunkelung damit ohne Codeaenderung (0 = volle Bildhelligkeit).
    """
    pfad = os.path.join(spieldaten.projektwurzel(), "data", "gebaeude_motive.json")   # Datendatei
    try:                                                                 # Datei lesen
        with open(pfad, encoding="utf-8") as f:                          # UTF-8 wie alle Spieldaten
            daten = json.load(f)                                         # Inhalt als dict
    except (OSError, ValueError):                                        # fehlt oder ist kaputt
        return dict(HINTERGRUND_VORGABE)                                 # dann die Vorgabe
    werte = daten.get("ansicht_hintergrund") if isinstance(daten, dict) else None
    if not isinstance(werte, dict):                                      # Schluessel fehlt
        return dict(HINTERGRUND_VORGABE)                                 # dann die Vorgabe
    ergebnis = dict(HINTERGRUND_VORGABE)                                 # Vorgabe als Grundlage
    ergebnis.update(werte)                                               # Datei hat Vorrang
    return ergebnis                                                      # fertige Einstellungen


def bot_wirtschaft_einstellungen() -> Dict[str, Any]:
    """Liest `data/bot_wirtschaft.json` - die EINE Stelle fuer Schalter, Anlagen und Lagerdeckel.

    Fehlt die Datei oder ist sie kaputt, gilt `BOT_WIRTSCHAFT_VORGABE`; das Spiel laeuft weiter.
    Die ERTRAEGE stehen bewusst nicht in der Datei, sondern kommen aus `data/buildings.json`
    (Handbuch 2009) - sonst gaebe es eine zweite Zahlenliste, die auseinanderlaufen kann.
    """
    pfad = os.path.join(spieldaten.projektwurzel(), "data", "bot_wirtschaft.json")   # Datendatei
    try:                                                                  # Datei lesen
        with open(pfad, encoding="utf-8") as f:                           # UTF-8 wie alle Spieldaten
            daten = json.load(f)                                          # Inhalt als dict
    except (OSError, ValueError):                                         # fehlt oder ist kaputt
        return dict(BOT_WIRTSCHAFT_VORGABE)                               # dann die Vorgabe
    if not isinstance(daten, dict):                                       # unerwarteter Inhalt
        return dict(BOT_WIRTSCHAFT_VORGABE)                               # dann die Vorgabe
    einstellungen = dict(BOT_WIRTSCHAFT_VORGABE)                          # Vorgabe als Grundlage
    einstellungen.update(daten)                                           # Datei hat Vorrang
    if not einstellungen.get("gebaeude_je_dorf"):                         # leere Anlagenliste
        einstellungen["gebaeude_je_dorf"] = list(BOT_WIRTSCHAFT_VORGABE["gebaeude_je_dorf"])
    return einstellungen                                                  # fertige Einstellungen


def _mit_volk(werte: Dict[str, float], bot=None) -> Dict[str, float]:
    """Einen Ertrag mit dem Volksfaktor des Bots skalieren (V-5, 03.11.2026).

    Die Prozente stehen in `data/boni.json` (gelesen von `boni.py`), die Fraktion kommt vom Bot
    (`BotPlayer.faction`). Ohne Bot, ohne Fraktion oder bei abgeschalteter Wirkung bleibt der Wert
    unveraendert - keine geratene Zahl. Kern (Ernte) und Anzeige (Spionagebericht) rufen dieselbe
    Funktion, deshalb wirkt der Bonus in beiden gleich (F-04).
    """
    fraktion = str(getattr(bot, "faction", "") or "")
    if not fraktion:
        return dict(werte)
    return {stoff: round(float(menge) * boni.ertragsfaktor(fraktion, stoff), 2)
            for stoff, menge in werte.items()}


def boni_fuer_ort(ort) -> Dict[str, float]:
    """Die Kampfwerte des Volkes EINES Ortes (V-5) - leer, wenn der Ort kein Volk traegt."""
    return boni.kampf_werte(boni.modifikatoren(str(getattr(ort, "volk", "") or "")))


def boni_fuer_bot(bot, jetzt: float = 0.0) -> Dict[str, float]:
    """Die Kampfwerte eines Bots: Volk + stehende Taktik (V-5, additiv).

    Der Bot geht als dict hinein, weil `bottaktik` nur dicts kennt - Name und Fraktion kommen aus
    `BotPlayer`, der Verhaltensbonus (falls vorhanden) entscheidet ueber die Sperrzeit.
    """
    daten = {"name": str(getattr(bot, "name", "") or ""),
             "fraktion": str(getattr(bot, "faction", "") or ""),
             "verhaltensbonus": getattr(bot, "verhaltensbonus", None)}
    return boni.kampf_werte(bottaktik.modifikatoren(daten, jetzt))


def bot_nahrungsbedarf(bot: "BotPlayer") -> float:
    """Tagesbedarf an Nahrung fuer die Armee eines Bots - DIESELBE Rechnung wie beim Spieler.

    `spieloekonomie.tagesbedarf_nahrung` ist die eine Rechenstelle (8 je Einheit und Spieltag,
    `data/nahrungsverbrauch.json`). Ein Bot hat keine Garnison je Dorf, sondern EINE Armee
    (`bot.army`) - sie steht im Hauptdorf und isst dort.
    """
    return spieloekonomie.tagesbedarf_nahrung(dict(getattr(bot, "army", None) or {}))


def bot_reserve_nahrung(bot: "BotPlayer", zusaetzliche_einheiten: int = 0) -> float:
    """Reserve, die ein Bot fuer seine Armee zurueckhalten muss (Kaufbremse, Daniel 03.11.2026).

    Reserve = Tagesbedarf x `reserve_stunden` / `versorgung_stunden` - dieselbe Formel, mit der
    `botkern.oekonomie_angebot` den Verkauf bremst. Die Stufe steht in `data/bot_wirtschaft.json`
    (`bot_stufe`), die Stunden in `data/spieloekonomie.json`.
    """
    einstellungen = bot_wirtschaft_einstellungen()
    stufe = str(einstellungen.get("bot_stufe") or "schwer").strip().lower()
    regeln = spieloekonomie.REGELN
    profil = (regeln.get("bots") or {}).get(stufe) or {}
    anzahl = sum(max(0, int(v)) for v in (getattr(bot, "army", None) or {}).values())
    bedarf = spieloekonomie.tagesbedarf_nahrung({"einheit": anzahl + max(0, int(zusaetzliche_einheiten))})
    try:
        stunden = float(profil.get("reserve_stunden") or 0)
        versorgung = float(regeln.get("versorgung_stunden") or 0)
    except (TypeError, ValueError):
        return 0.0
    if versorgung <= 0:
        return 0.0
    return round(bedarf + bedarf * stunden / versorgung, 2)


def bot_nahrung_deckt(bot: "BotPlayer", zusaetzliche_einheiten: int = 0) -> bool:
    """Deckt das Bot-Lager Tagesbedarf PLUS Reserve? (Kaufbremse und Kaufstopp)

    Daniel 03.11.2026: "der Bot stellt nur auf, solange die Nahrung im Lager den Tagesbedarf der
    Armee PLUS eine Reserve deckt"; bei Unterdeckung kein Nachkauf. Ohne Armee und ohne Vorrat
    (frischer Bot) ist die Bremse offen, sonst koennte er nie anfangen.
    """
    verfuegbar = float((bot_kasse(bot) or {}).get("nahrung", 0.0) or 0.0)
    if not getattr(bot, "army", None) and verfuegbar <= 0:
        return True                                                    # frischer Bot, kein Futter
    return verfuegbar >= bot_reserve_nahrung(bot, zusaetzliche_einheiten)


def bot_futter_buchen(bot: "BotPlayer", dorf: "BotDorf", ab: float, bis: float,
                      mengen: Optional[dict] = None) -> Dict[str, float]:
    """Bucht den Nahrungsverbrauch der Bot-Armee fuer EINE Erntespanne (S-2, 03.11.2026).

    Dieselbe Rechnung wie beim Spieler (`spieloekonomie.ort_tick`, Register 69): Bedarf =
    `bot_nahrungsbedarf` x Spanne / 86400 Sekunden. Gegessen wird NACH der Ernte, der Bestand
    faellt hoechstens auf 0, der Rest steht als `unterdeckung` im `produktionsjournal` des
    Dorfes - dieselbe Zeilenform wie beim Spieler
    (``{"ab", "bis", "mengen", "verbrauch", "unterdeckung"}``). Eine Strafe gibt es nicht
    (Daniel 03.11.2026: keine Desertion, aber Kaufstopp - den haelt `bot_nahrung_deckt` in
    `GameState.bot_armee_aufstellen`).

    Gebucht wird NUR im Hauptdorf: ein Bot hat EINE Armee (`bot.army`), nicht je Dorf eine
    Garnison. Reicht das Hauptdorf nicht, entsteht Unterdeckung - Nachschub aus den anderen
    Doerfern ist S-7 (Karawanen), nicht dieses Schnittes.

    Rueckgabe: ``{"ab", "bis", "verbrauch", "unterdeckung"}`` (leer, wenn kein Bedarf entstand).
    """
    ab = float(ab)                                                    # Spanne muss vorwaerts laufen
    bis = float(bis)                                                  # sonst wird nichts gebucht
    leer: Dict[str, float] = {"ab": ab, "bis": bis, "verbrauch": 0.0, "unterdeckung": 0.0}
    if bis <= ab:                                                     # leere oder rueckwaerts
        return leer                                                   # laufende Spanne: kein Verbrauch
    bedarf_tag = bot_nahrungsbedarf(bot)                              # 8 je Einheit (Datendatei)
    if bedarf_tag <= 0:                                               # leere Armee oder Verbrauch aus
        return leer                                                   # dann isst niemand
    bedarf = bedarf_tag * (bis - ab) / 86400.0                        # Anteil der Spanne am Spieltag
    if not isinstance(getattr(dorf, "vorraete", None), dict):          # altes Dorf ohne Vorratsfeld
        dorf.vorraete = {}                                            # dann anlegen
    vorher = max(0.0, float(dorf.vorraete.get("nahrung", 0.0) or 0.0))   # Bestand vor dem Essen
    verbrauch = round(min(bedarf, vorher), 2)                         # nie mehr, als da ist
    unterdeckung = round(max(0.0, bedarf - verbrauch), 2)             # Rest = Unterdeckung
    dorf.vorraete["nahrung"] = round(vorher - verbrauch, 2)           # Bestand nie unter 0
    # EINE Zeile je Spanne: hat der Kern (S-2b, `bot_dorf_tick`) fuer DIESELBE Spanne schon eine
    # Journalzeile geschrieben, wird sie ergaenzt statt eine zweite anzulegen - sonst stuenden
    # Ernte und Verbrauch in zwei Zeilen, waehrend der Spieler beides in einer fuehrt.
    zeile = None
    for vorhandene in reversed(dorf.produktionsjournal):              # letzte Zeile zuerst
        if (isinstance(vorhandene, dict) and float(vorhandene.get("ab", -1.0)) == ab
                and float(vorhandene.get("bis", -1.0)) == bis):       # gleiche Spanne?
            zeile = vorhandene                                        # dann diese ergaenzen
            break
    if zeile is None:                                                 # keine Zeile fuer diese Spanne
        zeile = {"ab": ab, "bis": bis, "mengen": dict(mengen or {})}   # neue Zeile wie beim Spieler
        dorf.produktionsjournal.append(zeile)
    elif mengen:                                                      # Kern-Zeile: Ernte nachtragen
        zeile["mengen"] = dict(mengen)
    zeile["verbrauch"] = {"nahrung": verbrauch}                       # Verbrauch als eigener Posten
    zeile["unterdeckung"] = unterdeckung                              # Rest, den das Lager nicht deckte
    # S-11 (Daniels Entscheidung 9): auch der Bot-Weg haelt den Deckel ein. Auf dem Karten-Weg
    # schreibt diese Funktion die Journalzeile selbst (der Kern laeuft dort nicht), deshalb steht
    # der Deckel an BEIDEN Schreibstellen - sonst waere er fuer den Vorgabe-Weg wirkungslos.
    spieloekonomie.journal_deckeln(dorf.produktionsjournal)
    return {"ab": ab, "bis": bis, "verbrauch": verbrauch, "unterdeckung": unterdeckung}



def bot_doerfer_bebauen(dorf: "BotDorf", einstellungen: Optional[dict] = None) -> int:
    """Setzt die Grundanlagen eines Bot-Dorfes auf seine EIGENEN Felder (S-2, 03.11.2026).

    Bis heute rechnete ein Bot-Dorf seinen Ertrag aus dem Kartenprofil (`bot_dorf_ertrag`), ohne
    dass auf seiner Karte etwas stand. Mit dem Kern gilt: was nicht gebaut ist, ertraegt nichts -
    ausser dem Grundeinkommen der Originalsiedlung (1 Holz / 1 Stein). Damit ein Bot-Dorf nicht
    ab morgen hungert, setzt diese Funktion die Grundanlagen aus `data/bot_wirtschaft.json`
    (`gebaeude_je_dorf`, `anlagen_je_gebaeude`) auf die BESTEN freien Felder, auf denen sie stehen
    duerfen - dieselbe Regel, mit der `bot_dorf_ertrag` vorher "bestes Gelaende" gewaehlt hat.
    Rechnet nichts gut und kostet nichts: der Bot hat diese Anlagen bezahlt, als er das Dorf
    gruendete (VORSCHLAG, siehe Register 153).
    Rueckgabe: Zahl der gesetzten Anlagen (0 = es passt nichts mehr oder alles steht schon).
    """
    einstellungen = (einstellungen if einstellungen is not None
                     else bot_wirtschaft_einstellungen())
    karte = dorf.karte_daten or _bot_karte_dict(getattr(dorf, "karte", ""))
    if not karte:
        return 0                                                          # ohne Karte kein Feld
    dorf.karte_daten = karte
    raster = list(karte.get("raster") or [])
    if not raster:
        return 0
    try:
        anzahl = max(1, int(einstellungen.get("anlagen_je_gebaeude") or 1))
    except (TypeError, ValueError):
        anzahl = 1
    gebaeude = [str(g) for g in (einstellungen.get("gebaeude_je_dorf") or [])]
    if not gebaeude:
        return 0
    gesetzt = 0
    for geb in gebaeude:
        steht = sum(1 for g in dorf.bauten.values() if str(g) == geb)      # steht diese Anlage schon?
        offen = max(0, anzahl - steht)                                    # nur der Rest wird gesetzt -
        if not offen:                                                     # sonst legte JEDER Bot-Takt
            continue                                                      # drei weitere Anlagen nach
        frei = [i for i in range(len(raster)) if str(i) not in dorf.bauten]
        for _ in range(offen):
            if not frei:
                break
            passend = [(gelaende.ertrag_pro_stunde(geb, raster[i]) or 0.0, i) for i in frei
                       if gelaende.bau_moeglich(geb, raster[i])[0]]
            if not passend:
                break
            _wert, feld = max(passend)                                    # bestes Feld gewinnt
            dorf.bauten[str(feld)] = geb
            dorf.stufen[str(feld)] = 1
            frei.remove(feld)
            gesetzt += 1
    return gesetzt


def bot_dorf_ertrag(dorf=None, einstellungen: Optional[dict] = None,
                    bot: Optional["BotPlayer"] = None) -> Dict[str, float]:
    """Stundenertrag EINES Bot-Dorfes - die EINE Lesestelle fuer Kern UND Anzeige (F-04).

    Je Grundrohstoff stehen in einem Bot-Dorf `anlagen_je_gebaeude` Anlagen (Daniel 02.11.2026:
    DREI) auf dem BESTEN Gelaende, auf dem sie gebaut werden duerfen; der Stundensatz JE ANLAGE
    kommt aus `data/buildings.json` ueber `gelaende.ertrag_pro_stunde` (Handbuch 2009: Holzfaeller 4
    auf Wald, Steinmetz 4 auf Berg, Farm 4 auf Grasland, Goldmine 3 auf Berg). Mit drei Anlagen
    sind das 12 Holz / 12 Stein / 12 Nahrung / 9 Gold je Stunde und Dorf - die Zahl steht in der
    Datendatei, nicht im Code.
    `dorf` wird heute nicht ausgewertet (jedes Dorf wirtschaftet gleich) - der Parameter steht
    trotzdem da, damit ein spaeterer Ausbau je Dorf KEINE zweite Funktion braucht.
    **V-5 (03.11.2026):** ist `bot` uebergeben, wird jeder Rohstoff mit dem Volksfaktor seiner
    Fraktion skaliert (`_mit_volk`; Zahlen in `data/boni.json`). Ohne `bot` bleibt der Ertrag der
    alte - so laufen alte Aufrufe und Pruefungen unveraendert.
    Rueckgabe: {Rohstoff klein: Menge je Stunde}.
    """
    einstellungen = einstellungen if einstellungen is not None else bot_wirtschaft_einstellungen()
    # S-2b (03.11.2026): WOHER der Ertrag kommt - Schalter `ertrag_weg` in der Datendatei.
    # "karte" (Vorgabe, Daniel B-4): Kartenprofil. "felder": derselbe Kern wie beim Spieler
    # (`wirtschaft.ertrag_gesamt` aus den eigenen Feldern). KEIN `_mit_volk` auf diesem Weg -
    # der Kern rechnet den Volksfaktor schon selbst (Register 149), sonst waere er doppelt.
    if str(einstellungen.get("ertrag_weg") or "karte").strip().lower() == "felder" and dorf is not None:
        try:                                                              # Kern auf dem Ort
            werte = wirtschaft.ertrag_gesamt([bot_dorf_als_ort(dorf, bot)]) or {}
        except (TypeError, ValueError, KeyError):                        # kaputter Datensatz
            werte = {}                                                    # dann keine Zahl erfinden
        return {str(roh).lower(): round(float(menge), 2)                 # Schreibweise der Spielstaende
                for roh, menge in werte.items() if float(menge) > 0}     # nur echte Erntetraege
    # B-4 (02.11.2026): hat das Dorf eine Karte, kommt sein Ertrag aus dem KARTENPROFIL - der starke
    # Rohstoff traegt viel, die schwaecher produzierbaren wenig oder nichts (Vorgabe Daniel).
    karte = str(getattr(dorf, "karte", "") or "")                         # Karte dieses Dorfes
    if karte and einstellungen.get("karten_aktiv", True):                 # Kartenwirtschaft eingeschaltet
        profil = bot_kartenprofil(karte)                                  # Kartenwert je Rohstoff
        if profil:                                                        # Karte bekannt
            try:                                                          # Teiler aus der Datendatei
                teiler = float(einstellungen.get("karten_teiler") or 10.0)   # Kartenwert -> je Stunde
            except (TypeError, ValueError):                               # kaputter Wert
                teiler = 10.0                                             # dann der Vorschlag
            if teiler > 0:                                                # nur mit sinnvollem Teiler
                return _mit_volk({s: round(float(w) / teiler, 2)          # Ertrag je Stunde
                                  for s, w in profil.items() if float(w) > 0},   # nur Rohstoffe mit Wert
                                 bot)                                     # V-5: Volksbonus des Bots
    try:                                                                  # Zahl aus der Datendatei
        anzahl = max(0, int(einstellungen.get("anlagen_je_gebaeude") or 1))   # Anlagen je Grundrohstoff
    except (TypeError, ValueError):                                       # kaputter Wert
        anzahl = 1                                                        # dann eine Anlage
    gebaeude = tuple(str(g) for g in (einstellungen.get("gebaeude_je_dorf") or []))   # Arten je Dorf
    anlagen = (gebaeude, anzahl)                                          # Cache-Schluessel: Arten und Anzahl
    if anlagen in _BOT_ERTRAG_CACHE:                                      # schon einmal gerechnet
        return _mit_volk(dict(_BOT_ERTRAG_CACHE[anlagen]), bot)           # Kopie, V-5: Volksbonus
    ertrag: Dict[str, float] = {}                                         # Ergebnis: Rohstoff -> je Stunde
    stammdaten = gelaende.alle_gebaeude()                                 # Bauwerke aus den Spieldaten
    for geb in gebaeude:                                                  # je Grundrohstoff ein Posten
        eintrag = stammdaten.get(geb) or {}                               # Stammdaten dieses Gebaeudes
        rohstoff = eintrag.get("rohstoff")                                # welcher Rohstoff entsteht
        if not isinstance(rohstoff, str) or not rohstoff:                 # unklar (mehrere Rohstoffe)
            continue                                                      # dann keine Zahl erfinden
        bester = 0.0                                                      # bester belegter Stundensatz
        for art in gelaende.GELAENDEARTEN:                                # jedes Gelaende pruefen
            erlaubt, _grund = gelaende.bau_moeglich(geb, art)             # darf die Anlage dort stehen?
            if not erlaubt:                                               # nein
                continue                                                  # dann zaehlt es nicht
            wert = gelaende.ertrag_pro_stunde(geb, art)                   # Ertrag auf diesem Gelaende
            if isinstance(wert, (int, float)) and float(wert) > bester:    # bester Wert gewinnt
                bester = float(wert)                                      # merken
        if bester > 0:                                                    # nur belegte Erträge
            schluessel = rohstoff.lower()                                 # Schreibweise der Spielstaende
            ertrag[schluessel] = round(ertrag.get(schluessel, 0.0) + bester * anzahl, 2)   # mal Anlagenzahl
    _BOT_ERTRAG_CACHE[anlagen] = dict(ertrag)                             # fuer den naechsten Aufruf merken
    return _mit_volk(dict(ertrag), bot)                                   # frische Kopie, V-5: Volksbonus


# ----------------------------------------------------------------------------------------------
# B-4 (02.11.2026, Konzept Abschnitt 11, Vorgabe Daniel): DIE KARTE BESTIMMT DEN ERTRAG
#
# Bei jeder Gruendung stehen drei Karten zur Wahl; die gewaehlte Karte bestimmt, welchen Rohstoff
# dieses Dorf MAXIMAL traegt und welche Rohstoffe dort schwaecher produzierbar sind - Gold hat
# Vorrang. Karten sind die 127 Originalsiedlungskarten. Ihr Profil wird aus den FELDERN der Karte
# gerechnet (`data/originalkarten/katalog.json`: berg, huegel, grasland, wald, steppe, nebelsee,
# sumpf) und den BELEGTEN Ertraegen je Gebaeude und Gelaende (`data/buildings.json`). Keine Zahl in
# diesem Abschnitt ist erfunden; frei waehlbar ist nur der Teiler in der Datendatei.
# ----------------------------------------------------------------------------------------------

BOT_PROFIL_GEBAEUDE: Dict[str, str] = {                                   # Rohstoff -> Anlage
    "holz": "holzfaeller",                                               # Holz aus dem Wald
    "stein": "steinmetz",                                                # Stein aus Berg und Huegel
    "nahrung": "farm",                                                    # Nahrung aus Grasland und Steppe
    "gold": "goldmine",                                                   # Gold aus Berg und Huegel
    "metall": "erzmine",                                                  # Metall aus Berg und Huegel
}
_BOT_KARTEN_CACHE: Dict[str, Dict[str, float]] = {}                       # Karten-ID -> Profil (Werte)


def bot_karten_katalog() -> Dict[str, dict]:
    """Die 127 Originalsiedlungskarten samt Feldern - gelesen aus den Spieldaten, nichts erfunden.

    Rueckgabe: {Karten-ID: Eintrag}. Fehlt die Datei, ist die Rueckgabe leer und jedes Dorf rechnet
    wie vor B-4 mit der festen Rate (kein Absturz, kein stiller Fehler).
    """
    pfad = os.path.join(spieldaten.projektwurzel(), "data", "originalkarten", "katalog.json")   # Datendatei
    try:                                                                  # Datei lesen
        with open(pfad, encoding="utf-8") as f:                           # UTF-8 wie alle Spieldaten
            daten = json.load(f)                                          # Inhalt als dict
    except (OSError, ValueError):                                         # fehlt oder ist kaputt
        return {}                                                         # dann keine Karten
    karten = daten.get("karten") or []                                    # Liste der Karten
    return {str(k.get("id")): k for k in karten if isinstance(k, dict) and k.get("id")}   # nach ID


def bot_dorf_als_ort(dorf: "BotDorf", bot: "BotPlayer" = None) -> dict:
    """EIN Bot-Dorf in der Form, mit der der KERN rechnet (S-1, 03.11.2026).

    Der Kern (`wirtschaft.ertrag_gesamt`, `spieloekonomie.ort_tick`, `spielschicht.*`) arbeitet mit
    dicts, und dort ist `karte` das 10x10-RASTER - nicht die Kennung. Diese Funktion uebersetzt:
    Raster aus der Kennung ueber `_bot_karte_dict` (gemerkt), Volk aus dem Bot, alles andere
    woertlich. Sie erfindet nichts: ein Feld, das das Dorf nicht hat, bleibt leer.
    """
    dorf.karte_daten = dorf.karte_daten or _bot_karte_dict(getattr(dorf, "karte", ""))
    ort = {"id": str(getattr(dorf, "name", "") or ""), "name": str(dorf.name),
           "karte": dict(dorf.karte_daten or {}),
           "bauten": dict(getattr(dorf, "bauten", None) or {}),
           "stufen": dict(getattr(dorf, "stufen", None) or {}),
           "einheiten": dict(getattr(dorf, "einheiten", None) or {}),
           "vorraete": dict(getattr(dorf, "vorraete", None) or {}),
           "bevoelkerung": float(getattr(dorf, "bevoelkerung", 0.0) or 0.0),
           "waren": dict(getattr(dorf, "waren", None) or {}),
           "werkstaetten": copy.deepcopy(getattr(dorf, "werkstaetten", None) or {}),
           "ausbildung": copy.deepcopy(getattr(dorf, "ausbildung", None) or []),
           "produktionsjournal": copy.deepcopy(getattr(dorf, "produktionsjournal", None) or []),
           "fertigjournal": copy.deepcopy(getattr(dorf, "fertigjournal", None) or []),
           # S-4 (03.11.2026): `spieloekonomie.verbrauchen` (Kosten einer Forschung) und der
           # Transportweg erwarten die Importherkunft. Bots fuehren sie noch nicht (Karawanen
           # kommen mit S-7), also LEER statt erfunden - der Verbrauch wird dann voll aus dem
           # eigenen Bestand gedeckt, und `verbrauchsjournal` bleibt ohne Importzeilen.
           "importiert": {},
           "verbrauchsjournal": [],
           "besitzer": "bot", "volk": str(getattr(bot, "faction", "") or "")}
    if getattr(dorf, "forschungsauftrag", None):
        ort["forschungsauftrag"] = copy.deepcopy(dorf.forschungsauftrag)
    return ort


def bot_dorf_aus_ort(dorf: "BotDorf", ort: dict) -> "BotDorf":
    """Den vom Kern fortgeschriebenen Ort zurueck ins Bot-Dorf schreiben (Gegenstueck zu oben).

    Uebernommen wird nur, was der Ort wirklich traegt - fehlt ein Feld, bleibt der alte Wert des
    Dorfes stehen (kein Loeschen durch Versehen). Die KENNUNG der Karte bleibt unberuehrt, sonst
    verloere das Dorf seine Karte beim ersten Takt.
    """
    ort = ort if isinstance(ort, dict) else {}
    for feld in ("bauten", "stufen", "einheiten", "vorraete", "waren"):
        wert = ort.get(feld)
        if isinstance(wert, dict):
            setattr(dorf, feld, dict(wert))
    for feld in ("werkstaetten", "ausbildung", "produktionsjournal", "fertigjournal"):
        wert = ort.get(feld)
        if isinstance(wert, (dict, list)):
            setattr(dorf, feld, copy.deepcopy(wert))
    if "bevoelkerung" in ort:
        try:
            dorf.bevoelkerung = float(ort.get("bevoelkerung") or 0.0)
        except (TypeError, ValueError):
            pass
    if isinstance(ort.get("forschungsauftrag"), dict):
        dorf.forschungsauftrag = copy.deepcopy(ort["forschungsauftrag"])
    return dorf


def bot_kartenprofil(karte: str) -> Dict[str, float]:
    """Was EINE Karte je Rohstoff hergibt - der Kartenwert, aus ihren Feldern gerechnet.

    Je Rohstoff wird ueber ALLE Gelaendearten der Karte summiert: Anzahl Felder x Ertrag je Stunde,
    aber nur auf Gelaende, auf dem die Anlage stehen DARF (`gelaende.bau_moeglich`). Ein Dorf ohne
    Wald traegt also kein Holz, ein Dorf ohne Berg kaum Gold - genau die Eigenschaft, die Daniel
    beschreibt. Rueckgabe: {Rohstoff klein: Kartenwert}; unbekannte Karte -> leeres dict.
    """
    karte = str(karte or "")                                              # Kennung als Text
    if not karte:                                                         # keine Karte
        return {}                                                         # dann kein Profil
    if karte in _BOT_KARTEN_CACHE:                                        # schon einmal gerechnet
        return dict(_BOT_KARTEN_CACHE[karte])                             # Kopie zurueckgeben
    eintrag = bot_karten_katalog().get(karte) or {}                       # Katalog-Eintrag dieser Karte
    felder = ((eintrag.get("original_attribute") or {}).get("felder") or {})   # Felderzahl je Gelaende
    if not felder:                                                        # Karte ohne Felderangabe
        return {}                                                         # dann kein Profil
    profil: Dict[str, float] = {}                                         # Ergebnis je Rohstoff
    for stoff, geb in BOT_PROFIL_GEBAEUDE.items():                        # je Anlage ein Posten
        wert = 0.0                                                        # Kartenwert dieses Rohstoffs
        for art, anzahl in felder.items():                                # je Gelaendeart der Karte
            erlaubt, _grund = gelaende.bau_moeglich(geb, art)             # darf die Anlage dort stehen?
            if not erlaubt:                                               # nein
                continue                                                  # dann zaehlt das Feld nicht
            ertrag = gelaende.ertrag_pro_stunde(geb, art)                 # BELEGTER Ertrag je Stunde
            if isinstance(ertrag, (int, float)):                          # nur echte Zahlen
                wert += float(anzahl) * float(ertrag)                     # Felder mal Ertrag
        profil[stoff] = round(wert, 2)                                    # Kartenwert festhalten
    _BOT_KARTEN_CACHE[karte] = dict(profil)                               # fuer den naechsten Aufruf merken
    return dict(profil)                                                   # frische Kopie


def bot_karten_staerkster(profil: dict) -> str:
    """Der Rohstoff, den diese Karte am meisten traegt (fuer Anzeige und Pruefung)."""
    werte = {str(k): float(v) for k, v in (profil or {}).items() if float(v) > 0}   # nur echte Werte
    if not werte:                                                         # Karte traegt nichts
        return ""                                                         # dann kein Staerkster
    return max(sorted(werte), key=lambda s: werte[s])                     # hoechster Wert, Gleichstand alphabetisch


_BOT_KARTENDATEN_CACHE: Dict[str, dict] = {}


def _bot_karte_dict(kennung: str) -> dict:
    """Die VOLLE Karte (Raster und Zaehlung) fuer den Kern - gemerkt, weil sie teuer zu bauen ist.

    `botkern.oekonomie_kartenwahl` rechnet mit `spieloekonomie.kartennutzen`, und das braucht die
    echte Karte (Achsen aus ihren Feldern), nicht das Kartenprofil. Unbekannte Kennung: leeres
    Dict - nichts wird erfunden.
    """
    kennung = str(kennung or "")
    if not kennung:
        return {}
    if kennung in _BOT_KARTENDATEN_CACHE:                                 # schon gebaut
        return _BOT_KARTENDATEN_CACHE[kennung]                            # dieselbe Karte
    try:
        daten = originalkarten.karte(kennung)                             # Originalfelder
    except (KeyError, ValueError):                                        # Kennung unbekannt
        daten = {}
    _BOT_KARTENDATEN_CACHE[kennung] = daten                               # merken
    return daten


def bot_kartenwahl(bot: "BotPlayer", index: int, anzahl: int = 3,
                   einstellungen: Optional[dict] = None, stufe: str = "",
                   belegte=None, raten: Optional[dict] = None) -> str:
    """Waehlt fuer EIN Bot-Dorf eine Karte aus drei Kandidaten - Gold hat Vorrang (Vorgabe Daniel).

    Die Kandidaten sind reproduzierbar: derselbe Bot mit derselben Dorfnummer bekommt immer dieselbe
    Auswahl (Zufall aus Name und Nummer, kein Wuerfeln zur Laufzeit). Gewaehlt wird die Karte mit dem
    hoechsten GOLD-Wert; bei Gleichstand entscheidet der Gesamtwert, danach die Kennung. Das ist der
    VORSCHLAG fuer den Bot; beim Spieler waehlt der Kopf.

    **V-6 (03.11.2026): der Anschluss an `botkern.oekonomie_kartenwahl`.** Ist `stufe` gesetzt und
    in `data/spieloekonomie.json` bekannt, entscheidet die REGEL des Kerns unter denselben drei
    Kandidaten - "schwer" nimmt den hoechsten Portfolio-Nutzen (`spieloekonomie.kartennutzen`),
    "leicht" will gar nicht gruenden und liefert None, dann bleibt es bei der Gold-Regel. `belegte`
    sind die Karten, die der Bot schon haelt (sein Portfolio), `raten` seine Stundenertraege.
    Nur die drei Kandidaten werden bewertet, nicht alle 127 Karten: die Wahl kostet sonst Sekunden
    je Dorf, und drei Karten sind die Spielregel (`data/bot_wirtschaft.json`: karten_kandidaten).
    """
    einstellungen = einstellungen if einstellungen is not None else bot_wirtschaft_einstellungen()
    try:                                                                  # Zahl aus der Datendatei
        anzahl = max(1, int(anzahl or einstellungen.get("karten_kandidaten") or 3))   # Karten zur Wahl
    except (TypeError, ValueError):                                       # kaputter Wert
        anzahl = 3                                                        # dann drei Karten
    ids = sorted(bot_karten_katalog())                                    # alle Karten, feste Reihenfolge
    if not ids:                                                           # kein Katalog vorhanden
        return ""                                                         # dann keine Karte
    zufall = random.Random("karte:%s:%d" % (getattr(bot, "name", ""), int(index)))   # reproduzierbare Wahl
    kandidaten = zufall.sample(ids, min(anzahl, len(ids)))                # drei Karten zur Auswahl
    # V-6 (03.11.2026): die REGEL des Kerns entscheidet unter denselben Kandidaten. Bis heute hatte
    # `botkern.oekonomie_kartenwahl` keinen Aufrufer; jetzt waehlt die Stufe aus der Datendatei.
    # Liefert die Regel keine Karte (unbekannte Stufe, "leicht" ohne Gruenden, kein Kandidat mit
    # Nutzen), gilt weiter die Gold-Regel unten - ein Dorf OHNE Karte haette keinen Ertrag.
    if stufe:
        freie = {k: {"besitzer": None, "karte": d}
                 for k, d in ((k, _bot_karte_dict(k)) for k in kandidaten) if d}
        eigene = [d for d in (_bot_karte_dict(k) for k in (belegte or [])) if d]
        try:
            gewaehlt = botkern.oekonomie_kartenwahl(str(stufe).strip().lower(), eigene, freie,
                                                    dict(raten or {}),
                                                    bot_rohstoffbedarf(bot),   # S-10: Bedarf je Rohstoff
                                                    spieloekonomie.REGELN)
        except (KeyError, TypeError, ValueError):                          # Stufe unbekannt
            gewaehlt = None                                                # dann die Gold-Regel
        if gewaehlt:
            return str(gewaehlt)


    def _rang(kennung: str):                                              # Rang einer Karte
        profil = bot_kartenprofil(kennung)                                # ihr Kartenwert
        return (float(profil.get("gold", 0.0)),                           # Gold zuerst (Daniel)
                round(sum(float(v) for v in profil.values()), 2),         # dann der Gesamtwert
                kennung)                                                  # dann die Kennung
    return max(kandidaten, key=_rang)                                     # die beste der drei


def bot_doerfer_karten_zuweisen(bot: "BotPlayer", einstellungen: Optional[dict] = None) -> int:
    """Gibt jedem Dorf ohne Karte seine Karte - einmalig, reproduzierbar, idempotent.

    Ein alter Spielstand (Doerfer ohne Feld `karte`) bekommt die Karte hier beim ersten Bot-Takt;
    der Ertrag rechnet danach aus dem Kartenprofil. Rueckgabe: Zahl der Doerfer, die eine Karte
    bekommen haben (0 = nichts Neues).

    **V-6 (03.11.2026):** welche Karte, entscheidet jetzt die REGEL aus
    `botkern.oekonomie_kartenwahl` (Stufe in `data/bot_wirtschaft.json`: `kartenwahl_stufe`); der
    Bot geht mit seinem eigenen Portfolio (`belegte`) und seinen Stundenertraegen (`raten`) hinein.
    Sagt die Regel nichts, gilt die alte Gold-Regel - kein Dorf bleibt ohne Karte.
    """
    einstellungen = einstellungen if einstellungen is not None else bot_wirtschaft_einstellungen()
    if not einstellungen.get("karten_aktiv", True):                       # Schalter aus
        return 0                                                          # dann keine Karten
    stufe = str(einstellungen.get("kartenwahl_stufe") or "").strip().lower()   # V-6: Regel des Kerns
    doerfer_liste = bot_doerfer_sicherstellen(bot)                        # je Dorf eine Karte
    belegte = [str(getattr(d, "karte", "") or "") for d in doerfer_liste]  # das Portfolio des Bots
    raten: Dict[str, float] = {}                                          # seine Stundenertraege
    for dorf in doerfer_liste:                                            # je Dorf zusammenzaehlen
        for stoff, menge in bot_dorf_ertrag(dorf, einstellungen, bot).items():
            raten[stoff] = round(raten.get(stoff, 0.0) + float(menge), 2)
    neu = 0                                                               # Zaehler fuer den Aufrufer
    for i, dorf in enumerate(doerfer_liste):                              # je Dorf eine Karte
        if str(getattr(dorf, "karte", "") or ""):                         # schon vergeben
            continue                                                      # nichts tun
        karte = bot_kartenwahl(bot, i, einstellungen=einstellungen, stufe=stufe,
                               belegte=[k for k in belegte if k], raten=raten)
        if karte:                                                         # Karte gefunden
            dorf.karte = karte                                            # am Dorf festhalten
            belegte.append(karte)                                         # Portfolio waechst mit
            neu += 1                                                      # zaehlen
    # S-2 (03.11.2026): der Uebergangs-Bauplan. Mit dem Kern gilt: was nicht gebaut ist, ertraegt
    # nichts - ein Dorf mit leerer Karte braechte nur das Grundeinkommen (1 Holz / 1 Stein) und
    # hungerte ab dem Anschluss. Hier werden die Grundanlagen EINMAL gesetzt; die Funktion ist
    # idempotent (setzt je Gebaeude nur den fehlenden Rest) und kostet nichts (Register 153).
    for dorf in doerfer_liste:                                            # je Dorf (auch alte Spielstaende)
        bot_doerfer_bebauen(dorf, einstellungen)                          # Grundanlagen auf die eigenen Felder
    return neu                                                            # wie viele neu sind


def bot_karten_uebersicht(karte: str, einstellungen: Optional[dict] = None,
                          bot: Optional["BotPlayer"] = None) -> dict:
    """Was der Spieler ueber eine Karte erfahren darf - Anzeige und Kern lesen dieselben Werte.

    V-5 (03.11.2026): ist `bot` uebergeben, traegt der gezeigte Stundensatz denselben Volksfaktor
    wie `bot_dorf_ertrag` (`_mit_volk`) - sonst zeigte der Bericht zwei Zahlen fuer dieselbe Sache.
    """
    einstellungen = einstellungen if einstellungen is not None else bot_wirtschaft_einstellungen()
    profil = bot_kartenprofil(karte)                                      # Kartenwert je Rohstoff
    teiler = float(einstellungen.get("karten_teiler") or 10.0)            # Umrechnung in je Stunde
    eintrag = bot_karten_katalog().get(str(karte)) or {}                  # Katalog-Eintrag (Name, Kategorie)
    return {"karte": str(karte), "name": str(eintrag.get("name") or ""),
            "kategorie": str(eintrag.get("kategorie") or ""),
            "staerkster": bot_karten_staerkster(profil),                  # der maximale Rohstoff
            "werte": dict(profil),                                        # Kartenwerte (Felder x Ertrag)
            "ertrag_pro_stunde": _mit_volk(
                {s: round(w / teiler, 2) for s, w in profil.items() if w > 0}, bot)}


def bot_dorf_bericht_teil(dorf, bot: "BotPlayer",
                          einstellungen: Optional[dict] = None) -> dict:
    """Der verdeckte Teil EINES Bot-Dorfes fuer den Spionagebericht - die EINE Lesestelle (F-04).

    Kern (Bot-Takt, Angriff) und Anzeige (Postfach) lesen dieselben Zahlen: der Ertrag kommt aus
    `bot_dorf_ertrag` (B-3/B-4), die Vorraete aus dem Dorflager, Wall und Taktik aus dem
    Dorf-Datensatz. Bewusst eine MODULFUNKTION und keine Methode: sie braucht keinen Spielstand,
    und eine Pruefdatei mit einem schlanken Stellvertreter kann sie so aufrufen (B-5, 02.11.2026).
    """
    einstellungen = (einstellungen if einstellungen is not None
                     else bot_wirtschaft_einstellungen())               # Schalter und Teiler lesen
    karte = str(getattr(dorf, "karte", "") or "")                       # B-4: die Karte dieses Dorfes
    return {"name": dorf.name, "x": int(dorf.x), "y": int(dorf.y),
            "wall_stufe": int(dorf.wall_stufe),                         # Kampfdatum - nur hier
            "wall_zustand": float(dorf.wall_zustand),                   # Kampfdatum - nur hier
            "taktik": str(dorf.taktik or ""),                           # Kampfdatum - nur hier
            "truppen": dict(bot.army or {}),                            # stationierte Truppen
            # B-3: die Vorrate stehen je DORF (jedes Dorf hat ein eigenes Lager).
            "vorraete": {str(k): round(float(v), 2)
                         for k, v in (dorf.vorraete or {}).items()},
            "ertrag_pro_stunde": bot_dorf_ertrag(dorf, einstellungen, bot),   # eine Lesestelle (F-04)
            # B-4: die Karte bestimmt den Ertrag - der Bericht zeigt sie mit ihren Werten.
            "karte": karte,
            "karte_info": (bot_karten_uebersicht(karte, einstellungen, bot)
                           if karte and einstellungen.get("karten_aktiv", True) else {}),
            "ernte_seit": float(dorf.ernte_seit)}                       # Zeitpunkt der letzten Ernte


def bot_kasse(bot: "BotPlayer") -> Dict[str, float]:
    """Die Kasse eines Bots = SUMME seiner Dorf-Vorrate (B-3, die EINE Lesestelle).

    Kein Bot fuehrt daneben ein eigenes Lager: wer die Kasse braucht, ruft diese Funktion (oder
    liest `bot.vorraete`, was dasselbe ist). Leere Doerfer werden vorher ueber
    `bot_doerfer_sicherstellen` angelegt, damit auch ein alter Spielstand sofort eine Kasse hat.
    """
    summe: Dict[str, float] = {}                                          # Ergebnis: Rohstoff -> Menge
    for dorf in bot_doerfer_sicherstellen(bot):                           # je Dorf seine Vorrate
        for stoff, menge in (getattr(dorf, "vorraete", None) or {}).items():   # ein Posten des Dorfes
            summe[str(stoff)] = round(summe.get(str(stoff), 0.0) + float(menge), 2)   # aufsummieren
    return summe                                                          # fertige Kasse


def bot_kasse_setzen(bot: "BotPlayer", kasse) -> None:
    """Setzt die GESAMTkasse eines Bots - verteilt den Stand auf die Doerfer, keine zweite Kasse.

    Verteilung: nach dem ANTEIL, den ein Dorf heute von diesem Rohstoff haelt; haelt kein Dorf
    etwas, zu gleichen Teilen. Gerundet wird auf zwei Stellen, den Rest bekommt das Hauptdorf -
    so ist die Summe der Doerfer EXAKT die gewuenschte Kasse (kein verschwundener Rest).
    Das Hauptdorf ist immer das ERSTE Dorf (`bot_doerfer_sicherstellen`, B-1).
    """
    doerfer = bot_doerfer_sicherstellen(bot)                              # Doerfer, ggf. angelegt
    if not doerfer:                                                       # theoretisch nicht moeglich
        return                                                            # dann nichts buchen
    ziel = {str(k): max(0.0, float(v)) for k, v in (kasse or {}).items() if str(k)}   # Zielbestand
    stoffe = set(ziel)                                                    # alle gewuenschten Rohstoffe
    for dorf in doerfer:                                                  # plus alles, was noch liegt
        stoffe.update(str(k) for k in (getattr(dorf, "vorraete", None) or {}))
    for stoff in sorted(stoffe):                                          # je Rohstoff getrennt
        soll = round(float(ziel.get(stoff, 0.0)), 2)                      # gewuenschte Gesamtmenge
        heute = [float((getattr(d, "vorraete", None) or {}).get(stoff, 0.0)) for d in doerfer]   # Ist je Dorf
        gesamt = round(sum(heute), 2)                                     # Ist gesamt
        anteile = [h / gesamt for h in heute] if gesamt > 0 else [1.0 / len(doerfer)] * len(doerfer)  # Anteile
        neu = [round(soll * a, 2) for a in anteile]                       # Ziel je Dorf
        rest = round(soll - sum(neu), 2)                                  # Rundungsrest
        neu[0] = round(neu[0] + rest, 2)                                  # Hauptdorf traegt den Rest
        if neu[0] < 0:                                                    # Hauptdorf kann nicht negativ
            neu[0] = 0.0                                                  # bei null deckeln
        for dorf, menge in zip(doerfer, neu):                             # Ziel in die Doerfer schreiben
            if not isinstance(getattr(dorf, "vorraete", None), dict):     # altes Dorf ohne Vorratsfeld
                dorf.vorraete = {}                                        # dann anlegen
            dorf.vorraete[stoff] = round(max(0.0, float(menge)), 2)       # Wert buchen


def bot_kasse_buchen(bot: "BotPlayer", stoff: str, menge) -> float:
    """Bucht EINEN Posten auf die Kasse des Bots (positiv = Zugang, negativ = Abgang).

    Gebucht wird ueber `bot_kasse_setzen`, also auf die DOERFER - das ist der einzige Weg, etwas
    abzuziehen oder gutzuschreiben. Rueckgabe: der neue Bestand dieses Rohstoffs (nie unter 0).
    """
    kasse = bot_kasse(bot)                                                # heutige Kasse
    neuer = round(float(kasse.get(str(stoff), 0.0)) + float(menge), 2)    # gewuenschter neuer Stand
    kasse[str(stoff)] = max(0.0, neuer)                                   # nie unter null
    bot_kasse_setzen(bot, kasse)                                          # auf die Doerfer buchen
    return float(kasse[str(stoff)])                                       # neuen Bestand melden


def bot_siedler_uebernehmen(dorf: "BotDorf") -> float:
    """Siedler eines Bot-Dorfes aus dem alten Lagerposten nach `bevoelkerung` ziehen (S-3).

    Bis S-3 fuehrten die Bots Siedler als ROHSTOFF im Dorflager (`vorraete["siedler"]`, Startwert
    10 aus `bot_vorrat_anlegen`), waehrend der Kern sie als Bevoelkerung fuehrt
    (`Siedlung.bevoelkerung`, waechst durch `ort_tick`). Zwei Orte fuer dieselbe Groesse - und die
    belegten Preise (Einheiten, Holzfaeller/Steinmetz/Jaeger) verlangen Siedler. Diese Funktion
    zieht den alten Posten EINMAL in die Bevoelkerung; danach gibt es nur noch eine Stelle.
    Idempotent: der Posten wird entfernt, ein zweiter Aufruf findet nichts mehr.
    Rueckgabe: die Bevoelkerung des Dorfes nach der Uebernahme.
    """
    if not isinstance(getattr(dorf, "vorraete", None), dict):              # Dorf ohne Lager
        return float(getattr(dorf, "bevoelkerung", 0.0) or 0.0)            # dann nur die Bevoelkerung
    alt = float(dorf.vorraete.pop("siedler", 0.0) or 0.0)                  # alter Rohstoffposten
    if alt > 0:                                                           # nur wenn etwas da ist
        dorf.bevoelkerung = round(float(getattr(dorf, "bevoelkerung", 0.0) or 0.0) + alt, 2)
    return float(getattr(dorf, "bevoelkerung", 0.0) or 0.0)


def bot_bauplan() -> Dict[str, Any]:
    """Der Bauplan der Bots aus `data/bot_bauplan.json` (S-3, 03.11.2026) - EINE Quelle.

    Je Taktik eine REIHENFOLGE, dazu Obergrenzen je Gebaeude. Die Preise stehen NICHT hier,
    sondern in `data/baupreise.json` und werden ueber `spielschicht.bauen` gebucht. Fehlt die
    Datei oder ist sie kaputt, ist der Plan leer - dann baut kein Bot (kein erfundener Plan).
    """
    pfad = os.path.join(spieldaten.projektwurzel(), "data", "bot_bauplan.json")
    try:
        with open(pfad, encoding="utf-8") as f:
            daten = json.load(f)
    except (OSError, ValueError):
        return {}
    return daten if isinstance(daten, dict) else {}


# ===================================================================================================
# S-4 (03.11.2026): DIE BOTS FORSCHEN
#
# Daniels Vorgabe, woertlich: die Bots sollen "mit ihren erwirtschafteten ressourcen auch
# forschungsschritte durchlaufen um ihre einheiten und neue gebaeude freizuschalten". Bis hier hatten
# Bots kein Forschungswesen (`dorf.geforscht` blieb 0), und der Kern-Tick bekam ein leeres dict als
# Forschungsstand - jede Forschungsstufe des Bots war wirkungslos.
#
# Aufbau wie in S-3 (Bauen): die REIHENFOLGE steht je Taktik in `data/bot_forschung.json` mit
# Begruendung je Schritt (Daniels Entscheidung 2), die Voraussetzungen kommen aus
# `data/research.json` (`forschungspfad`), Dauer und Kosten aus `spieldaten` - und gestartet wird
# durch DIESELBE Funktion wie beim Spieler (`spieloekonomie.forschung_start`). Der laufende Auftrag
# haengt am ORT (`BotDorf.forschungsauftrag`, seit S-1 vorhanden), die erreichte Stufe am Bot.
#
# Warum NICHT `spielschicht.forschung_starten`: diese Funktion setzt ihren Auftrag in
# `zustand["forschung"]` (Reichsstand) und prueft NUR Bibliothek, Kosten und "keine zweite Forschung".
# Die Voraussetzungskette (`forschungspfad.erfuellt`: Bibliothek 3, Schmiedekunst 1 ...) kennt sie
# nicht - ein Bot haette damit Waffentechnik ohne Schmiedekunst forschen koennen. Der Spieler geht
# seit dem Oekonomie-Paket ueber `spieloekonomie.forschung_start` (main._start_research); die Bots
# gehen denselben Weg.
# ===================================================================================================

def bot_forschungsplan() -> Dict[str, Any]:
    """Der Forschungsplan der Bots aus `data/bot_forschung.json` (S-4) - EINE Quelle.

    Je Taktik eine geordnete Liste von Schritten mit Zielstufe und Begruendung. Die Namen der
    Forschungen und ihre Voraussetzungen stehen NICHT hier, sondern in `data/research.json`.
    Fehlt die Datei oder ist sie kaputt, ist der Plan leer - dann forscht kein Bot (kein
    erfundener Plan, kein Absturz).
    """
    pfad = os.path.join(spieldaten.projektwurzel(), "data", "bot_forschung.json")
    try:
        with open(pfad, encoding="utf-8") as f:
            daten = json.load(f)
    except (OSError, ValueError):
        return {}
    return daten if isinstance(daten, dict) else {}


def bot_forschungsstaende(bot: "BotPlayer") -> Dict[str, int]:
    """Der Wissensstand eines Bots als `{Gebiet: Stufe}` - leer heisst: nichts erforscht.

    EINE Lesestelle: `bot_dorf_forschen` (Voraussetzungen), `bot_dorf_forschung_abschluss`
    (Stufe steigt) und `bot_dorf_tick` (Forschungsboni des Kerns) lesen hier. Ein alter
    Spielstand ohne das Feld liefert ein leeres dict und damit Stufe 0 ueberall.
    """
    roh = getattr(bot, "forschungsstaende", None) or {}
    if not isinstance(roh, dict):
        return {}
    sauber: Dict[str, int] = {}
    for name, stufe in roh.items():
        try:
            sauber[str(name)] = max(0, int(stufe or 0))
        except (TypeError, ValueError):
            continue
    return sauber


def bot_dorf_forschungsliste(bot: "BotPlayer", plan: Optional[dict] = None) -> List[dict]:
    """Die geordnete Forschungsliste der Taktik dieses Bots (nur der Zweig ``jetzt``).

    Gleiche Form wie `bot_dorf_bauen`: der Stil kommt aus `bot_taktik_name` (dieselbe Quelle wie
    der Verhaltensbonus), ein unbekannter Name faellt auf ``Unbekannt`` zurueck. Der Zweig
    ``nach_bibliothek`` enthaelt Schritte, die Bibliothek 2 oder 3 verlangen, und wird bewusst
    NICHT gelesen (der Bot baut seine Bibliothek noch nicht aus).
    """
    plan = plan if isinstance(plan, dict) else bot_forschungsplan()
    if not plan or not plan.get("aktiv", True):
        return []
    zweige = plan.get("plaene") or {}
    zweig = zweige.get(bot_taktik_name(bot)) or zweige.get("Unbekannt") or {}
    return [e for e in (zweig.get("jetzt") or []) if isinstance(e, dict)]


def bot_dorf_forschung_abschluss(dorf: "BotDorf", bot: "BotPlayer",
                                 jetzt: float) -> List[str]:
    """Laesst eine FAELLIGE Forschung dieses Dorfes steigen - genau einmal (S-4).

    Gerufen aus dem Bot-Takt, VOR dem Start der naechsten Forschung. Gebucht wird durch
    `spieloekonomie.forschung_abschluss` (dieselbe Funktion wie beim Spieler): Stufe steigt nur
    nach oben (`max`), der Auftrag verschwindet, die Fertigstellung landet im `fertigjournal` des
    Dorfes. Ist die Zeit noch nicht um, aendert sich NICHTS - Rueckgabe dann leer.

    Der Auftrag wird hier ausdruecklich auch auf ``None`` zurueckgeschrieben: `bot_dorf_aus_ort`
    uebernimmt nur dicts, ein erledigter Auftrag bliebe sonst fuer immer am Dorf stehen.
    """
    if not isinstance(getattr(dorf, "forschungsauftrag", None), dict):
        return []
    ort = bot_dorf_als_ort(dorf, bot)
    wissen = bot_forschungsstaende(bot)
    neu, neues_wissen = spieloekonomie.forschung_abschluss(ort, wissen, float(jetzt))
    if neu.get("forschungsauftrag"):                       # Zeit noch nicht um
        return []
    gebiet = str((dorf.forschungsauftrag or {}).get("gebiet") or "")
    dorf.forschungsauftrag = None                          # Auftrag ist verbucht
    bot_dorf_aus_ort(dorf, neu)                            # fertigjournal usw. uebernehmen
    dorf.forschungsauftrag = None                          # ... aber kein alter Auftrag zurueck
    if neues_wissen != wissen:                             # eine Stufe ist wirklich gestiegen
        bot.forschungsstaende = dict(neues_wissen)
        dorf.geforscht = int(getattr(dorf, "geforscht", 0) or 0) + 1
        bot.geforscht = int(getattr(bot, "geforscht", 0) or 0) + 1
        return [gebiet]
    return []


def bot_dorf_forschen(dorf: "BotDorf", bot: "BotPlayer", jetzt: float = 0.0,
                     plan: Optional[dict] = None) -> List[str]:
    """Startet EINE Forschung dieses Dorfes nach dem Plan seiner Taktik (S-4, 03.11.2026).

    Gesucht wird der ERSTE Schritt der Liste, dessen Zielstufe noch nicht erreicht ist und dessen
    Voraussetzungen mit dem Wissensstand des Bots und der Bibliothek DIESES Ortes erfuellt sind
    (`forschungspfad.erfuellt`). Gestartet wird dann durch `spieloekonomie.forschung_start` -
    dieselbe Funktion wie beim Spieler: sie prueft Voraussetzungskette, Bibliothek, "diese
    Bibliothek forscht schon" und die Rohstoffe im DORFLAGER, und sie bucht die Kosten dort ab.

    Kein Erfinden: ohne Bibliothek, ohne Plan, bei laufendem Auftrag oder wenn nichts erfuellbar
    ist, bleibt die Rueckgabe leer und es wird nichts gebucht.
    Rueckgabe: die gestarteten Gebiete (hoechstens `forschungen_je_takt`).
    """
    plan = plan if isinstance(plan, dict) else bot_forschungsplan()
    if not plan or not plan.get("aktiv", True):
        return []
    if getattr(dorf, "forschungsauftrag", None):            # diese Bibliothek forscht schon
        return []
    liste = bot_dorf_forschungsliste(bot, plan)
    if not liste:
        return []
    try:
        je_takt = max(1, int(plan.get("forschungen_je_takt") or 1))
    except (TypeError, ValueError):
        je_takt = 1
    ort = bot_dorf_als_ort(dorf, bot)
    bibliothek = gebaeude_wirkung.bibliothek_stufe([ort])
    if bibliothek <= 0:                                     # ohne Bibliothek kein Forschungsort
        return []
    weitere = None                                          # erst bei einem echten Start bauen (teuer)
    gestartet: List[str] = []
    for _ in range(je_takt):
        wissen = bot_forschungsstaende(bot)
        ziel = None                                         # naechster erforschbarer Schritt
        for eintrag in liste:
            name = str(eintrag.get("forschung") or "")
            if not name:
                continue
            try:
                bis = max(1, int(eintrag.get("bis_stufe") or 1))
            except (TypeError, ValueError):
                bis = 1
            if wissen.get(name, 0) >= bis:                  # Zielstufe steht schon
                continue
            erfuellt, _grund = forschungspfad.erfuellt(name, wissen, bibliothek)
            if not erfuellt:                                # Voraussetzung fehlt (noch)
                continue
            ziel = name
            break
        if ziel is None:                                    # nichts erfuellbar -> Takt vorbei
            break
        if weitere is None:                                 # erst jetzt die anderen Doerfer uebersetzen
            weitere = [bot_dorf_als_ort(d, bot)         # Doppelforschung derselben Stufe vermeiden
                       for d in bot_doerfer_sicherstellen(bot) if d is not dorf]
        try:
            ort = spieloekonomie.forschung_start(ort, ziel, wissen, float(jetzt), weitere)
        except ValueError:                                  # zu teuer oder Regel verletzt
            break
        gestartet.append(ziel)
        bot_dorf_aus_ort(dorf, ort)                         # Auftrag und Kosten ins Bot-Dorf
    return gestartet


# ===================================================================================================
# S-10 (03.11.2026, Daniels Entscheidung 4): DER BEDARF JE ROHSTOFF
#
# Daniels Entscheidung, woertlich: "\"mittel\" - ich baue dafuer zuerst einen Bedarf je Rohstoff".
# Bis hier kannte das Spiel genau EINEN laufenden Verbrauch: Nahrung fuer die Garnison
# (`spieloekonomie.tagesbedarf_nahrung`, 8 je Einheit und Spieltag). Alles andere (Forschung,
# Ausbildung, Werkstattwaren, Bauten) wird sofort bezahlt - ein Bedarf ueber die ZEIT war nirgends
# gefuehrt. Deshalb konnte die Bot-Kartenwahl nicht auf "mittel": `botkern.oekonomie_kartenwahl`
# nimmt dort die am schlechtesten gedeckte Rohstoffachse, und ohne Bedarf gibt es keine Achse.
#
# Diese Funktion rechnet den Bedarf als PLANUNGSGROESSE je STUNDE - in derselben Einheit wie die
# Erträge der Karten (`bot_dorf_ertrag`, Stundenraten), damit "Deckung = Rate / Bedarf" eine Zahl
# ohne Einheit ist. Das Fenster, auf das einmalige Ausgaben umgelegt werden, steht in
# `data/bot_bedarf.json` (VORSCHLAG-Zahl, das Original nennt keinen Planungshorizont).
# ===================================================================================================

def bot_diebstahl_einstellungen() -> Dict[str, Any]:
    """Die Regeln des Bot-Diebstahls aus `data/bot_diebstahl.json` (S-12) - EINE Quelle.

    Fehlt die Datei oder ist sie kaputt, ist der Diebstahl AUS (`aktiv: False`) - kein stiller
    Standardwert, keine erfundene Zahl.
    """
    pfad = os.path.join(spieldaten.projektwurzel(), "data", "bot_diebstahl.json")
    try:
        with open(pfad, encoding="utf-8") as f:
            daten = json.load(f)
    except (OSError, ValueError):
        return {"aktiv": False}
    return daten if isinstance(daten, dict) else {"aktiv": False}


def bot_ist_duenn(bot: "BotPlayer", einstellungen: dict) -> bool:
    """Hat dieser Bot hoechstens `armee_schwelle` Einheiten? Nur ein duenner Bot stiehlt."""
    try:
        schwelle = int(einstellungen.get("armee_schwelle") or 0)
    except (TypeError, ValueError):
        return False
    if schwelle <= 0:
        return False
    einheiten = sum(max(0, int(v)) for v in (getattr(bot, "army", None) or {}).values())
    return einheiten <= schwelle


def bot_diebstahl(bot: "BotPlayer", ziel, jetzt: float,
                  einstellungen: Optional[dict] = None) -> Optional[dict]:
    """Ein duenner Bot bestiehlt einen WEHRLOSEN Ort - nie still, immer mit Bericht (S-12).

    Daniels Entscheidung 7 vom 03.11.2026, woertlich: "Ja, aber nur mit Bericht im Postfach".
    Bedingungen (jede einzeln geprueft, alle Zahlen aus `data/bot_diebstahl.json`):
      * der Diebstahl ist eingeschaltet,
      * der Bot ist DUENN (`bot_ist_duenn`: hoechstens `armee_schwelle` Einheiten),
      * das Ziel ist ABWESEND (`nur_ohne_garnison`: keine Einheiten vor Ort),
      * die Sperre je Bot (`sperre_stunden`) ist abgelaufen,
      * im Ziel liegt ueberhaupt etwas.
    Gebucht wird je Rohstoff `anteil_prozent` des Zielvorrats, hoechstens
    `hoechstens_je_rohstoff`, in der Summe hoechstens `hoechstens_je_diebstahl`; das Ziel faellt
    nie unter 0, der Bot bekommt genau die genommene Menge in sein Hauptdorf.

    Rueckgabe: der Bericht ``{"bot", "ziel", "zeit", "mengen", "summe"}`` oder ``None``.
    Die Postfach-Nachricht schreibt der Aufrufer (`main.bots_fortschreiben`), damit hier keine
    Anzeige-Logik steckt.
    """
    einstellungen = einstellungen if isinstance(einstellungen, dict) else bot_diebstahl_einstellungen()
    if not einstellungen.get("aktiv", False):
        return None
    if ziel is None or not isinstance(getattr(ziel, "vorraete", None), dict) or not ziel.vorraete:
        return None
    if einstellungen.get("nur_ohne_garnison", True) and (getattr(ziel, "einheiten", None) or {}):
        return None                                          # wer Truppen hat, wird angegriffen
    if not bot_ist_duenn(bot, einstellungen):
        return None                                          # ein starker Bot kaempft
    try:
        anteil = max(0.0, float(einstellungen.get("anteil_prozent") or 0.0)) / 100.0
        je_rohstoff = max(0.0, float(einstellungen.get("hoechstens_je_rohstoff") or 0.0))
        gesamt_deckel = max(0.0, float(einstellungen.get("hoechstens_je_diebstahl") or 0.0))
        sperre = max(0.0, float(einstellungen.get("sperre_stunden") or 0.0)) * 3600.0
    except (TypeError, ValueError):
        return None
    gedaechtnis = bot.gedaechtnis if isinstance(getattr(bot, "gedaechtnis", None), dict) else {}
    letzter = float(gedaechtnis.get("diebstahl_seit") or 0.0)
    if sperre > 0 and letzter > 0 and float(jetzt) - letzter < sperre:
        return None                                          # dieser Bot ist noch gesperrt
    if anteil <= 0 or je_rohstoff <= 0 or gesamt_deckel <= 0:
        return None

    genommen: Dict[str, float] = {}
    summe = 0.0
    for stoff in sorted(ziel.vorraete):
        rest_deckel = gesamt_deckel - summe
        if rest_deckel <= 0:
            break
        try:
            bestand = float(ziel.vorraete.get(stoff) or 0.0)
        except (TypeError, ValueError):
            continue
        if bestand <= 0:
            continue
        menge = min(bestand * anteil, je_rohstoff, rest_deckel)
        menge = round(max(0.0, menge), 2)
        if menge <= 0:
            continue
        ziel.vorraete[stoff] = round(bestand - menge, 2)      # nie unter 0 (menge <= bestand)
        genommen[stoff] = menge
        summe = round(summe + menge, 2)
    if not genommen:
        return None

    hauptdorf = next((d for d in bot_doerfer_sicherstellen(bot)
                      if getattr(d, "hauptdorf", False)), None)
    if hauptdorf is not None:                                # Beute ins eigene Hauptdorf
        if not isinstance(getattr(hauptdorf, "vorraete", None), dict):
            hauptdorf.vorraete = {}
        for stoff, menge in genommen.items():
            hauptdorf.vorraete[stoff] = round(float(hauptdorf.vorraete.get(stoff, 0.0) or 0.0) + menge, 2)
    bot.gedaechtnis = dict(gedaechtnis)
    bot.gedaechtnis["diebstahl_seit"] = float(jetzt)         # Sperre beginnt jetzt
    return {"bot": str(bot.name), "ziel": str(getattr(ziel, "name", "") or ""),
            "zeit": float(jetzt), "mengen": dict(genommen), "summe": summe}


def bot_diebstahl_nachricht(bericht: dict) -> dict:
    """Die Postfach-Nachricht zu einem Diebstahl - wer, wann, was, wieviel (Entscheidung 7)."""
    bericht = bericht if isinstance(bericht, dict) else {}
    teile = ", ".join("%g %s" % (menge, stoff) for stoff, menge in sorted((bericht.get("mengen") or {}).items()))
    text = ("Diebstahl in %s: %s hat %g Einheiten entwendet (%s). Der Ort hatte keine Garnison - "
            "wer Truppen zu Hause haelt, wird nicht bestohlen. Spielzeit %s."
            % (bericht.get("ziel") or "?", bericht.get("bot") or "?", float(bericht.get("summe") or 0.0),
               teile or "nichts", _spielzeit_text(float(bericht.get("zeit") or 0.0))))
    return {"text": text, "type": "diebstahl", "spielzeit_sekunden": float(bericht.get("zeit") or 0.0)}


def _spielzeit_text(sekunden: float) -> str:
    """Spielsekunden als 'Tag X, HH:MM' - dieselbe Form wie im Spielstand."""
    sekunden = max(0.0, float(sekunden or 0.0))
    tage = int(sekunden // 86400)
    stunden = int((sekunden % 86400) // 3600)
    minuten = int((sekunden % 3600) // 60)
    return "Tag %d, %02d:%02d" % (tage, stunden, minuten)


def bot_bedarf_einstellungen() -> Dict[str, Any]:
    """Die Rechenregeln des Bedarfs aus `data/bot_bedarf.json` - EINE Quelle.

    Fehlt die Datei oder ist sie kaputt, gilt der Rueckfall `aktiv: False`: dann wird NUR der
    belegte Nahrungsbedarf gerechnet (kein erfundener Planungshorizont, kein Absturz).
    """
    pfad = os.path.join(spieldaten.projektwurzel(), "data", "bot_bedarf.json")
    try:
        with open(pfad, encoding="utf-8") as f:
            daten = json.load(f)
    except (OSError, ValueError):
        return {"aktiv": False, "fenster_stunden": 24.0}
    if not isinstance(daten, dict):
        return {"aktiv": False, "fenster_stunden": 24.0}
    return daten


def _bot_rezeptkosten(ware: str) -> Dict[str, float]:
    """Was EINE Einheit dieser Werkstattware an Rohstoffen kostet (data/warenrezepte.json)."""
    pfad = os.path.join(spieldaten.projektwurzel(), "data", "warenrezepte.json")
    try:
        with open(pfad, encoding="utf-8") as f:
            rezepte = json.load(f)
    except (OSError, ValueError):
        return {}
    eintrag = (rezepte or {}).get(str(ware)) or {}
    kosten = eintrag.get("kosten") or {}
    return {str(k): float(v) for k, v in kosten.items() if isinstance(v, (int, float))}


def bot_rohstoffbedarf(bot: "BotPlayer", einstellungen: Optional[dict] = None) -> Dict[str, float]:
    """Der Bedarf eines Bots je Rohstoff, in Mengen JE STUNDE (S-10, Daniels Entscheidung 4).

    Gerechnet wird aus dem, was das Spiel schon fuehrt - nichts erfunden:
      * **Nahrung** - `spieloekonomie.tagesbedarf_nahrung(bot.army)` / 24 (der einzige BELEGTE
        laufende Verbrauch, 8 je Einheit und Spieltag).
      * **Ausbildung** - Kosten der noch offenen Ausbildungsauftraege je Dorf, umgelegt auf
        `fenster_stunden`.
      * **Werkstatt** - Rezeptkosten der offenen Werkstattauftraege (`data/warenrezepte.json`),
        ebenfalls umgelegt.
      * **Forschung** - Kosten des NAECHSTEN Schritts im Forschungsplan des Bots; ein laufender
        Auftrag ist bereits bezahlt und zaehlt nicht.
    Bauten zaehlen bewusst NICHT mit (einmalige Ausgabe, siehe `data/bot_bedarf.json`).

    Rueckgabe: `{rohstoff: menge_je_stunde}` - nur Rohstoffe mit Bedarf > 0 (leer, wenn nichts
    laeuft und die Armee leer ist).
    """
    einstellungen = einstellungen if isinstance(einstellungen, dict) else bot_bedarf_einstellungen()
    bedarf: Dict[str, float] = {}

    def dazu(rohstoff: str, menge: float) -> None:
        """Einen Posten addieren - nur endliche, positive Mengen (keine NaN in die Deckung)."""
        if not isinstance(menge, (int, float)) or not math.isfinite(float(menge)) or float(menge) <= 0:
            return
        bedarf[str(rohstoff)] = round(bedarf.get(str(rohstoff), 0.0) + float(menge), 6)

    # 1. Nahrung der Armee - immer, auch ohne Datendatei (belegte Zahl).
    dazu("nahrung", float(spieloekonomie.tagesbedarf_nahrung(dict(getattr(bot, "army", None) or {}))) / 24.0)

    if not einstellungen.get("aktiv", False):
        return bedarf                                   # nur der belegte Verbrauch

    try:
        fenster = max(1.0, float(einstellungen.get("fenster_stunden") or 24.0))
    except (TypeError, ValueError):
        fenster = 24.0

    # 2./3. offene Auftraege je Dorf (Ausbildung und Werkstatt)
    alle_einheiten = einheiten.alle()
    for dorf in bot_doerfer_sicherstellen(bot):
        for auftrag in (getattr(dorf, "ausbildung", None) or []):
            if not isinstance(auftrag, dict) or auftrag.get("gebucht"):
                continue                                # fertige Auftraege sind bezahlt
            name = str(auftrag.get("einheit") or "")
            kosten = ((alle_einheiten.get(name) or {}).get("kosten") or {})
            for stoff, menge in kosten.items():
                dazu(stoff, float(menge) / fenster)
        for schlange in ((getattr(dorf, "werkstaetten", None) or {}).values()):
            for auftrag in ((schlange or {}).get("auftraege") or []):
                ware = str((auftrag or {}).get("ware") or "")
                try:
                    anzahl = max(1, int((auftrag or {}).get("anzahl") or 1))
                except (TypeError, ValueError):
                    anzahl = 1
                for stoff, menge in _bot_rezeptkosten(ware).items():
                    dazu(stoff, float(menge) * anzahl / fenster)

    # 4. naechster Forschungsschritt der Taktik (laufende Auftraege sind bezahlt)
    wissen = bot_forschungsstaende(bot)
    for eintrag in bot_dorf_forschungsliste(bot):
        name = str(eintrag.get("forschung") or "")
        try:
            bis = max(1, int(eintrag.get("bis_stufe") or 1))
        except (TypeError, ValueError):
            bis = 1
        if not name or wissen.get(name, 0) >= bis:
            continue                                    # Zielstufe steht schon
        for stoff, menge in forschung.kosten(max(1, wissen.get(name, 0) + 1)).items():
            dazu(stoff, float(menge) / fenster)
        break                                           # nur der naechste Schritt
    return bedarf


def bot_taktik_name(bot: "BotPlayer") -> str:
    """Der STIL eines Bots (Pluenderer, Waechterin, Bastionier, Spaeherin, Raecher, Unbekannt).

    Dieselbe Quelle wie der Verhaltensbonus: `bottaktik.TAKTIKEN[bot.name]["name"]`. Der Stil
    entscheidet, WAS gebaut wird - das Verhalten (Suchen/Sichern/Wachsen) bleibt davon getrennt.
    """
    return str(bottaktik.taktik_von({"name": getattr(bot, "name", "")}).get("name") or "Unbekannt")


def bot_dorf_bauen(dorf: "BotDorf", bot: "BotPlayer", jetzt: float = 0.0,
                   plan: Optional[dict] = None) -> List[str]:
    """Setzt Gebaeude aus dem Bauplan der Taktik - mit Preisen und Bauplaetzen wie der Spieler.

    Der Bot baut durch DIESELBE Funktion wie der Spieler (`spielschicht.bauen`): freies Feld,
    Eignung des Gelaendes, Obergrenze je Siedlung, Preis aus `data/baupreise.json`, Abbuchung aus
    dem Dorflager. Gebaut wird immer das ERSTE Gebaeude der Taktik-Liste, das noch unter
    `hoechstens` liegt, passt und bezahlbar ist; danach ist der Takt vorbei (`bauten_je_takt`).
    Kein Erfinden: passt nichts, ist die Rueckgabe leer.

    **Forschung:** seit S-4 (03.11.2026) wird der Zweig `nach_baukunst` MITGELESEN - aber nur,
    was die gemeinsame Regel `gebaeude_forschung_erlaubt` durchlaesst (dieselbe Funktion wie im
    Spielerweg `bauen_auf_karte`). Solange der Bot Baukunst nicht erforscht hat, sind Wall, Lager,
    Schmiede, Akademie und Diebesgilde weiter gesperrt; sobald Baukunst 1 steht, baut er sie in der
    Reihenfolge seiner Taktik. Die Forschungsregel wird also BENUTZT, nicht umgangen.

    Rueckgabe: die Namen der gesetzten Gebaeude (leer, wenn nichts gebaut wurde).
    """
    plan = plan if isinstance(plan, dict) else bot_bauplan()
    if not plan or not plan.get("aktiv", True):                              # Schalter aus oder keine Datei
        return []
    zweige = plan.get("bauplaene") or {}                                     # je Taktik eine Liste
    zweig = zweige.get(bot_taktik_name(bot)) or zweige.get("Unbekannt") or {}
    staende = bot_forschungsstaende(bot)                                     # S-4: Wissensstand des Bots
    reihenfolge = [str(g) for g in ((zweig.get("jetzt") or [])
                                    + (zweig.get("nach_baukunst") or [])) if str(g)]
    # Nur was der Wissensstand erlaubt - dieselbe Regel wie beim Spieler, EINE Stelle.
    reihenfolge = [g for g in reihenfolge if gebaeude_forschung_erlaubt(g, staende)[0]]
    if not reihenfolge:
        return []
    hoechstens = plan.get("hoechstens") or {}                                # Obergrenzen je Gebaeude
    try:
        je_takt = max(1, int(plan.get("bauten_je_takt") or 1))               # Gebaeude je Takt
    except (TypeError, ValueError):
        je_takt = 1
    ort = bot_dorf_als_ort(dorf, bot)                                        # Kern-Form des Dorfes
    raster = list((ort.get("karte") or {}).get("raster") or [])              # Felder der Karte
    if not raster:                                                           # ohne Karte kein Bauplatz
        return []
    gebaut: List[str] = []                                                   # was wirklich entstand
    for _ in range(je_takt):                                                 # hoechstens N je Takt
        ziel = None                                                          # Gebaeude und Feld
        for geb in reihenfolge:                                              # Reihenfolge der Taktik
            grenze = hoechstens.get(geb)                                     # Obergrenze der Datei
            steht = sum(1 for g in (ort.get("bauten") or {}).values() if str(g) == geb)
            # S-4 (03.11.2026): zusaetzlich die BELEGTE Obergrenze je Siedlung aus
            # data/buildings.json (`max_je_siedlung`, z. B. Lager und Akademie je 1). Ohne diese
            # Zeile liefe ein bereits gebautes Lager in `spielschicht.bauen` auf "hoechstens 1x"
            # und der Takt braeche ab, statt beim naechsten Gebaeude weiterzumachen - genau der
            # Fehler, der beim ersten Lauf mit `nach_baukunst` auftrat.
            original = (gelaende.alle_gebaeude().get(geb) or {}).get("max_je_siedlung")
            grenzen = [int(grenze)] if isinstance(grenze, int) and grenze > 0 else []
            if isinstance(original, int) and original > 0:
                grenzen.append(original)
            if grenzen and steht >= min(grenzen):                            # genug davon gebaut
                continue                                                     # naechstes Gebaeude
            frei = [i for i in range(len(raster)) if str(i) not in (ort.get("bauten") or {})]
            passend = [(gelaende.ertrag_pro_stunde(geb, raster[i]) or 0.0, i) for i in frei
                       if gelaende.bau_moeglich(geb, raster[i])[0]]          # nur erlaubtes Gelaende
            if not passend:                                                  # nirgends baubar
                continue                                                     # naechstes Gebaeude
            ziel = (geb, max(passend)[1])                                    # bestes Feld gewinnt
            break
        if ziel is None:                                                     # nichts passt oder bezahlbar
            break
        zustand = {"siedlungen": [ort],                                      # der Ort als Siedlung
                   "ressourcen": ort.get("vorraete") or {},                  # SEIN Lager (eine Buchstelle)
                   "bevoelkerung": float(ort.get("bevoelkerung") or 0.0),    # Siedler des Ortes
                   "ereignisse": [], "zeit": float(jetzt)}                   # kein Spielstand noetig
        ok, _meldung = spielschicht.bauen(zustand, 0, ziel[0], ziel[1])      # DIESELBE Funktion
        if not ok:                                                           # zu teuer oder Regel
            break                                                            # dann diesen Takt nichts mehr
        ort["bevoelkerung"] = zustand.get("bevoelkerung", ort.get("bevoelkerung"))   # Siedler zurueck
        gebaut.append(ziel[0])                                               # zaehlen
    if gebaut:                                                               # nur bei Aenderung zurueck
        bot_dorf_aus_ort(dorf, ort)                                          # ins Bot-Dorf schreiben
    return gebaut                                                        # was entstand


def bot_dorf_tick(dorf: "BotDorf", bot: "BotPlayer", ab: float, bis: float,
                  deckel: float = 0.0) -> Dict[str, float]:
    """Laesst EIN Bot-Dorf durch den KERN wirtschaften (S-2b, 03.11.2026) - wie der Spieler.

    `spieloekonomie.ort_tick` ist dieselbe Funktion, die eine Spielersiedlung fortschreibt:
    Ernte aus den Feldern, Siedlerzuwachs, Werkstattwaren, fertige Ausbildungen, Journal. Das
    Bot-Dorf geht ueber `bot_dorf_als_ort` hinein und ueber `bot_dorf_aus_ort` zurueck; die
    Kartenkennung bleibt dabei erhalten (Register 152).

    **Nahrung:** gebucht wird hier NUR fuer eine eigene Garnison des Dorfes (`dorf.einheiten`).
    Ein Bot fuehrt seine Armee in `bot.army`; die isst weiterhin `bot_futter_buchen` im
    Hauptdorf. Solange `dorf.einheiten` leer ist, entsteht also kein doppelter Verbrauch - sobald
    S-5 Einheiten je Ort ausbildet, muss die Armee dort hineinwandern (sonst isst sie zweimal).

    **Deckel:** der Kern kennt keinen Lagerdeckel; `hoechstvorrat_je_stoff` aus der Datendatei
    wird deshalb nach dem Tick gekappt (dieselbe Grenze wie im alten Weg).

    Rueckgabe: {Stoff: Zuwachs} dieser Spanne - nur echte Zugaenge (leer, wenn nichts kam).
    """
    ort = bot_dorf_als_ort(dorf, bot)                                     # Ort in Kern-Form
    vorher = {str(k): float(v) for k, v in (ort.get("vorraete") or {}).items()}   # Bestand vorher
    # S-4 (03.11.2026): der Kern bekommt den WISSENSSTAND des Bots - vorher ging hier ein leeres
    # dict hinein, jede Bot-Forschung war damit fuer den Ertrag wirkungslos (Felderwirtschaft,
    # Forstwirtschaft, Heilkunde ...). Ohne Forschung ist das dict leer, dann aendert sich nichts.
    neu = spieloekonomie.ort_tick(ort, float(ab), float(bis), bot_forschungsstaende(bot))   # EINE Kernfunktion
    bot_dorf_aus_ort(dorf, neu)                                           # zurueck ins Bot-Dorf
    zuwachs: Dict[str, float] = {}                                        # was dazukam
    if not isinstance(getattr(dorf, "vorraete", None), dict):             # Sicherung: altes Dorf
        dorf.vorraete = {}
    for stoff in list(dorf.vorraete):                                     # je Posten nachrechnen
        wert = float(dorf.vorraete.get(stoff, 0.0) or 0.0)
        if deckel > 0 and wert > deckel:                                  # Lagerdeckel der Datendatei
            wert = deckel
            dorf.vorraete[stoff] = round(wert, 2)
        zuwachs_jetzt = round(wert - vorher.get(str(stoff), 0.0), 2)      # Zuwachs dieser Spanne
        if zuwachs_jetzt:                                                 # nur echte Bewegungen melden
            zuwachs[str(stoff)] = zuwachs_jetzt
    return zuwachs


def bot_doerfer_ernten(bot: "BotPlayer", jetzt: float, einstellungen: Optional[dict] = None) -> Dict[str, float]:
    """Laesst die Doerfer eines Bots bis `jetzt` wirtschaften - der EINE Ernteweg (B-3).

    Je Dorf wird die Zeit seit `dorf.ernte_seit` in Stunden umgerechnet und mit dem Stundensatz
    aus `bot_dorf_ertrag` (derselben Funktion, die auch der Spionagebericht zeigt) gutgeschrieben.
    Ein Dorf ohne Erntezeit (`0`, also jeder alte Spielstand und jedes neue Dorf) bekommt beim
    ersten Aufruf nur den Zeitstempel - KEINE Gutschrift fuer die Vergangenheit.
    Rueckgabe: {Rohstoff: tatsaechlich gebuchte Menge} (leer, wenn nichts geerntet wurde).
    """
    einstellungen = einstellungen if einstellungen is not None else bot_wirtschaft_einstellungen()
    ergebnis: Dict[str, float] = {}                                       # was wirklich dazukam
    if not einstellungen.get("aktiv", True):                              # Schalter aus
        return ergebnis                                                    # dann keine Ernte
    jetzt = float(jetzt)                                                  # Spielsekunden
    deckel = float(einstellungen.get("hoechstvorrat_je_stoff") or 0.0)    # Lagerdeckel je Stoff
    kern_weg = (str(einstellungen.get("ertrag_weg") or "karte").strip().lower() == "felder")
    for dorf in bot_doerfer_sicherstellen(bot):                           # je Dorf wirtschaften
        seit = float(getattr(dorf, "ernte_seit", 0.0) or 0.0)             # letzte Ernte dieses Dorfes
        if seit <= 0:                                                     # noch nie geerntet (neues Dorf,
            dorf.ernte_seit = jetzt                                       # alter Spielstand) -> nur den
            continue                                                      # Zeitstempel setzen, nichts buchen
        if jetzt <= seit:                                                 # Uhr steht oder laeuft rueckwaerts
            continue                                                      # nichts buchen, Zeitstempel bleibt
        if kern_weg:                                                      # S-2b: der KERN wirtschaftet
            geerntet = bot_dorf_tick(dorf, bot, seit, jetzt, deckel)      # ort_tick (wie beim Spieler)
            for stoff, menge in geerntet.items():                         # Zuwachs aufsummieren
                ergebnis[stoff] = round(ergebnis.get(stoff, 0.0) + menge, 2)
            dorf.ernte_seit = jetzt                                       # Erntezeit fortschreiben
            if getattr(dorf, "hauptdorf", False):                         # die Armee isst im Hauptdorf
                bot_futter_buchen(bot, dorf, seit, jetzt, geerntet)       # dieselbe Buchstelle
            continue                                                      # naechstes Dorf
        stunden = (jetzt - seit) / 3600.0                                 # vergangene Spielstunden
        if not isinstance(getattr(dorf, "vorraete", None), dict):         # altes Dorf ohne Vorratsfeld
            dorf.vorraete = {}                                            # dann anlegen
        geerntet: Dict[str, float] = {}                                   # was DIESES Dorf einbrachte
        for stoff, rate in bot_dorf_ertrag(dorf, einstellungen, bot).items():   # je Rohstoff die Rate
            vorher = float(dorf.vorraete.get(stoff, 0.0))                 # Bestand vor der Ernte
            nachher = vorher + float(rate) * stunden                      # Zuwachs dieser Zeitspanne
            if deckel > 0:                                                # Deckel gesetzt?
                nachher = min(nachher, deckel)                            # dann nicht darueber hinaus
            dorf.vorraete[stoff] = round(nachher, 2)                      # Dorf bekommt die Ernte
            zuwachs = round(dorf.vorraete[stoff] - vorher, 2)             # tatsaechlicher Zuwachs
            if zuwachs:                                                   # nur echte Zugaenge melden
                ergebnis[stoff] = round(ergebnis.get(stoff, 0.0) + zuwachs, 2)
                geerntet[stoff] = zuwachs                                 # fuer die Journalzeile des Dorfes
        # S-3 (03.11.2026): Siedlerzuwachs auch auf dem KARTEN-Weg - dieselbe Rechnung wie
        # `spieloekonomie.ort_tick` (1 Siedler je Ort und Stunde, Deckel aus den Gebaeuden).
        # Ohne diesen Schritt waechst ein Bot nur im Kern-Modus, und die Haeuser aus dem Bauplan
        # waeren wirkungslos.
        kern_ort = bot_dorf_als_ort(dorf, bot)                            # Ort in Kern-Form
        grenze_bev = gebaeude_wirkung.bevoelkerungsgrenze([kern_ort])     # Deckel dieses Dorfes
        zuwachs_bev = gebaeude_wirkung.siedler_zuwachs_pro_stunde([kern_ort], {}) * stunden
        if zuwachs_bev > 0:                                               # nur wenn etwas dazukommt
            dorf.bevoelkerung = round(min(float(grenze_bev),
                                          float(getattr(dorf, "bevoelkerung", 0.0) or 0.0)
                                          + zuwachs_bev), 2)              # nie ueber den Deckel
        dorf.ernte_seit = jetzt                                           # Erntezeit fortschreiben
        if getattr(dorf, "hauptdorf", False):                             # S-2: die Armee isst im Hauptdorf
            bot_futter_buchen(bot, dorf, seit, jetzt, geerntet)           # nach der Ernte (wie beim Spieler)
    return ergebnis                                                       # was dazukam



@dataclass
class Settlement:
    name: str
    map_id: str
    x: int = 0
    y: int = 0
    buildings: Dict[str, int] = field(default_factory=dict)
    units: Dict[str, int] = field(default_factory=dict)
    garrison: Dict[str, int] = field(default_factory=dict)
    last_rename: float = 0.0
    # Siedlungskarte (Handbuch S. 259/313): jede Siedlung hat eine eigene Geländekarte,
    # niemals zwei eigene Siedlungen dieselbe. bauten ordnet Feld-Index -> Gebäude-Kennung.
    karte: Optional[dict] = None
    # V-5 (03.11.2026): das VOLK dieses Ortes - bei der Gruendung aus `spieler_fraktion` gesetzt.
    # `wirtschaft._volk_faktor` liest es hier, damit der Volksbonus am Ort haengt und nicht an einer
    # zweiten, globalen Quelle. Leer = kein Bonus (alte Spielstaende, fremde Siedlung).
    volk: str = ""
    bauten: Dict[str, str] = field(default_factory=dict)
    # Ausbaustufe je bebautem Feld (W4b-5). Belegt sind Stufen für den Verteidigungswall (10)
    # und die drei Ausbildungsstätten; ein Feld ohne Eintrag gilt als Stufe 1.
    stufen: Dict[str, int] = field(default_factory=dict)
    # Schnitt S-2c-D (Daniel 01.11.2026): Das Dorfzentrum kommt kostenlos mit jeder Gruendung,
    # den PLATZ bestimmt der Spieler ("aber das setzen lassen ist wichtig damit der spieler
    # bestimmt welches feld seiner karte besetzt wird"). Solange `True`, wartet das Gebaeude auf
    # ein Feld; `_dorfzentrum_setzen` traegt es dann Stufe 1 ein und loescht das Kennzeichen.
    # Alte Spielstaende ohne das Feld laden mit `False` - kein Zwangsnachsetzen, keine Migration.
    dorfzentrum_offen: bool = False
    # GPT extern W-02: Ortswall belegt kein Kartenfeld. Die globale Freigabe liegt
    # allein in Forschung 'Verteidigungsanlagen'; Schaden bleibt ortsgebunden.
    mauer_besetzt: bool = False
    mauer_zustand: float = 100.0
    # --- Ökonomie-Paket, Entwurf Schritt 9 (Z. 757-772): die Felder einer LOKALEN Wirtschaft. ---
    # Sie sind bis zur Aktivierung (Schritt 10) leer bzw. auf ihren Vorgabewerten: das Spiel rechnet
    # weiterhin mit den GLOBALEN Beständen (`GameState.resources`, `.waren`, `.population`).
    # Eine zweite führende Wahrheit entsteht damit NICHT — der Neumodus liest später ausschließlich
    # diese Felder, der Altmodus nur die alten. Wer beides gleichzeitig führend führt, erzeugt die
    # Wirkung zweimal (Entwurf Z. 774: „Das bisherige units/garrison nicht gleichzeitig als
    # führende Bestände weiterführen. Altmodus liest alte Felder; Neumodus nur einheiten.").
    id: str = ""
    besitzer: str = "spieler"
    dimension: int = 1
    vorraete: Dict[str, float] = field(default_factory=dict)
    waren: Dict[str, int] = field(default_factory=dict)
    einheiten: Dict[str, int] = field(default_factory=dict)
    bevoelkerung: float = 0.0
    importiert: Dict[str, float] = field(default_factory=dict)
    reserve: Dict[str, float] = field(default_factory=dict)
    werkstaetten: Dict[str, dict] = field(default_factory=dict)
    ausbildung: List[dict] = field(default_factory=list)
    forschungsauftrag: Optional[dict] = None
    produktionsjournal: List[dict] = field(default_factory=list)
    verbrauchsjournal: List[dict] = field(default_factory=list)
    fertigjournal: List[dict] = field(default_factory=list)


# Handbuch S. 313: 'Einer neuen Siedlung wird per Zufall eine Karte zugewiesen. Es werden
# niemals zwei Deiner Siedlungen die gleiche Karte bekommen.' Wie viele Siedlungen erlaubt
# sind, sagt das Handbuch nicht ausdrücklich — sechs ist der belegte Stand (sechs Welten,
# sechs Siedlungen je Spieler laut Konformitäts-Audit).
SIEDLUNGEN_MAXIMUM = 6
KARTENVERSUCHE = 400

# Oekonomie-Paket, Schritt 9, Teil 8b (Entwurf Z. 789, "Migration"): Version und Modus des
# SPIELSTANDS. `STAND_VERSION_ALT = 1` ist der ALTE, unversionierte Stand — erkennbar daran, dass
# das Feld im Spielstand FEHLT. Ab Version 2 schreibt der Spielstand beide Felder mit.
# `mode` ist bis Schritt 10 ein reiner MERKER (Entwurf Z. 1092: "vorher darf der Oekonomiemodus
# NICHT aktiviert werden"): neue Partien laufen als `oeokonomie-1`, ein geladener Altstand als
# `legacy`. Es wird NICHTS umgerechnet — der Altmodus rechnet unveraendert mit den globalen
# Bestaenden (keine automatische Konvertierung ohne Daniels Wort).
STAND_VERSION_ALT = 1
STAND_VERSION = 2
MODUS_NEU = "oeokonomie-1"
MODUS_LEGACY = "legacy"


def siedlung_kennung(besitzer: str, map_id: str, x: int, y: int) -> str:
    """Die stabile Kennung eines Ortes (Ökonomie-Paket, Entwurf Z. 774).

    Wörtlich: „Neue Ort-ID bleibt beim Umbenennen stabil und gehört in jede Mission." Sie hängt
    deshalb an **Besitzer und Weltfeld**, nie am Namen — Umbenennen ändert sie nicht, und eine
    Mission kann ihr Ziel wiederfinden, auch wenn der Ort inzwischen anders heißt.
    """
    return f"{besitzer}:{map_id}:{x}:{y}"


def karten_signatur(karte: dict) -> str:
    """Eine Karte eindeutig beschreiben (Geländeart je Feld)."""
    return "".join(karte["raster"])


def neue_siedlungskarte(vorhandene: List[dict]) -> dict:
    """
    Weist einer neuen Siedlung eine zufällige Karte zu, die keine andere eigene Siedlung hat.

    Handbuch S. 313. Wird kein freies Muster gefunden, wird das ehrlich gemeldet statt eine
    doppelte Karte auszugeben.
    """
    vergeben = {karten_signatur(k) for k in vorhandene if k}
    for _ in range(KARTENVERSUCHE):
        karte = originalkarten.zufalls_originalkarte(random.randrange(1, 10 ** 9),
                      vergeben={k.get("originalkarte_id") for k in vorhandene if k})
        if karten_signatur(karte) not in vergeben:
            return karte
    raise RuntimeError("Keine neue Siedlungskarte gefunden")


def _ausbau_kosten(gebaeude_key: str, stufe: int, siedlung) -> dict:
    """Der AUSBAUPREIS eines Gebaeudes - mit dem Volksrabatt des Ortes (V-5, 03.11.2026).

    Daniel: das "Ausbau +5 %" der Gnome wirkt als 5 % guenstigerer Ausbau. Der Faktor kommt aus
    `boni.preis_faktor` (Zahlen in `data/boni.json`), das Volk steht am Ort (`Siedlung.volk`).
    Gerundet wird auf ganze Rohstoffe; Siedler bleiben unangetastet - sie sind Menschen, keine Ware.
    """
    kosten = baukosten(gebaeude_key, stufe)
    fraktion = str(getattr(siedlung, "volk", "") or "")
    if not fraktion:
        return kosten
    preis_faktor = boni.preis_faktor(fraktion)
    if abs(preis_faktor - 1.0) < 1e-9:
        return kosten
    return {stoff: (wert if str(stoff) == "siedler" else max(0, int(round(float(wert) * preis_faktor))))
            for stoff, wert in kosten.items()}


OHNE_FORSCHUNG_BAUBAR = frozenset({"holzfaeller", "steinmetz", "jaeger", "bibliothek", "haus"})
"""Die fuenf Gebaeude, die OHNE Forschung baubar sind (Handbuch, Siedlungs-Baumenue)."""


def gebaeude_forschung_erlaubt(kennung: str,
                               forschungsstaende: Optional[dict] = None) -> tuple:
    """Darf dieses Gebaeude mit DIESEM Forschungsstand gebaut werden? ``(ja/nein, Begruendung)``.

    EINE Stelle fuer die belegte Baumenue-Regel (Handbuch, Abschnitt Siedlungs-Baumenue; siehe
    `data/buildings.json`, `regeln.ohne_forschung_baubar`): genau fuenf Gebaeude sind ohne
    Forschung baubar - Holzfaeller, Steinmetz, Jaeger, Bibliothek und Haus. Alle uebrigen
    erfordern Kenntnisse in der Forschung **Baukunst** (Stufe 1). Die Mindeststufe 1 ist eine
    dokumentierte Remake-Entscheidung, keine behauptete Originalzahl.

    Seit S-4 (03.11.2026) fragen der Spieler (`bauen_auf_karte`) und der Bot (`bot_dorf_bauen`)
    dieselbe Funktion - vorher stand die Fuenfer-Liste im Code des Spielerwegs, und der Bot bog
    die Regel mit einer eigenen Liste nach. Ohne nachgewiesene Forschung KEIN Freipass.
    """
    if str(kennung) in OHNE_FORSCHUNG_BAUBAR:
        return True, "ohne Forschung baubar (Handbuch, Siedlungs-Baumenue)"
    if int((forschungsstaende or {}).get("Baukunst", 0) or 0) >= 1:
        return True, "Baukunst Stufe 1 vorhanden"
    return False, "Baukunst Stufe 1 wird fuer dieses Gebaeude benoetigt."


def bauen_auf_karte(siedlung: "Settlement", gebaeude_key: str, feld: int,
                   forschungsstaende: Optional[dict] = None,
                   nur_pruefen: bool = False) -> tuple:
    """
    Setzt ein Gebäude auf ein Feld der Siedlungskarte.

    Rückgabe: (ja/nein, Meldung). Prüft zuerst die Eignung (Handbuch S. 7/8: beim Bauen wird
    die Eignung des Geländes angezeigt), dann ob das Feld frei ist, und zuletzt die belegte
    Obergrenze je Siedlung (Kriegerakademie, Diebesgilde, Stellmacher und Bibliothek: je
    höchstens eines — data/buildings.json, Feld 'max_je_siedlung').

    Das neue Feld bekommt die Ausbaustufe 1 (W4b-5).
    """
    if siedlung.karte is None:
        return False, "Diese Siedlung hat noch keine Karte."
    if not (0 <= feld < len(siedlung.karte["raster"])):
        return False, f"Feld {feld} liegt nicht auf der Karte."
    if str(feld) in siedlung.bauten:
        return False, (f"Feld {feld} ist bereits belegt "
                       f"({siedlung.bauten[str(feld)]}).")
    art = siedlung.karte["raster"][feld]
    erlaubt, warum = gelaende.bau_moeglich(gebaeude_key, art)
    if not erlaubt:
        return False, warum

    kennung = gelaende.finde_gebaeude(gebaeude_key) or gebaeude_key
    eintrag = gelaende.alle_gebaeude().get(kennung) or {}
    # Handbuch, Abschnitt Siedlungs-Baumenue: genau fuenf Gebaeude sind ohne Forschung baubar.
    # Alle uebrigen erfordern Kenntnisse in Baukunst. S-4 (03.11.2026): dieselbe Regel steht
    # jetzt EINMAL in `gebaeude_forschung_erlaubt` - der Spieler hier und der Bot in
    # `bot_dorf_bauen` fragen dieselbe Funktion, statt die Liste ein zweites Mal zu fuehren.
    frei, warum_forschung = gebaeude_forschung_erlaubt(kennung, forschungsstaende)
    if not frei:
        return False, warum_forschung
    grenze = eintrag.get("max_je_siedlung")
    if isinstance(grenze, int) and grenze > 0:
        schon_da = gebaeude_wirkung.gebaeude_stufe(siedlung, kennung) > 0
        if schon_da and grenze <= 1:
            return False, (f"{eintrag.get('name', kennung)} gibt es höchstens {grenze}× "
                           f"je Siedlung (belegte Originalregel) — hier steht schon "
                           f"eines. Stattdessen ausbauen.")

    # Das Feld merkt sich die Ausbaustufe 1 (W4b-5); gespeichert wird der uebergebene
    # Gebaeudeschluessel wie bisher — alle Leser (gelaende, wirtschaft, gebaeude_wirkung)
    # verstehen Kennung UND Anzeigename.
    if not nur_pruefen:
        siedlung.bauten[str(feld)] = gebaeude_key
        siedlung.stufen[str(feld)] = 1
    return True, f"{warum} (Feld {feld})"


# ---------- Gruendung bringt drei Startgebaeude mit (Schnitt S-1, Daniel 01.11.2026) ----------
# Der Siedlungskarren liefert bei JEDER Gruendung (erstes Dorf UND jede Kolonie) drei Gebaeude:
# Holzfäller (moeglichst auf Wald), Steinmetz (moeglichst auf Huegel oder Berg) und Tempel
# (moeglichst auf Nebelsee, ohne Nebelsee auf Steppe). Sie kosten nichts, binden keine Siedler,
# und der Tempel braucht bei der GRUENDUNG keine Baukunst (Ausnahme: „der Siedlungskarren bringt
# diesen Tempel quasi schon mit", docs/KONZEPT_SECHS_DOERFER_20261101.md, Anhang 1). Ein spaeterer
# Nachbau bleibt forschungspflichtig (bauen_auf_karte prueft weiter Baukunst).
# Die Platzwahl ist EINE Funktion mit einer Vorlieben-Tabelle (keine if-Kette, kein Zufall); der
# Tempel steht zuerst, damit ein seltenes Nebelsee-Feld nicht verloren geht (die drei
# Wunschgelaende sind disjunkt).

STARTGEBAEUDE_VORLIEBEN = (
    # (Gebaeudekennung, Wunschgelaende in absteigender Prioritaet)
    ("tempel", ("nebelsee", "steppe")),
    ("holzfaeller", ("wald",)),
    ("steinmetz", ("huegel", "berg")),
)


def _startgebaeude_setzen(ort, karte) -> list:
    """Die drei Startgebaeude des Gruendungskarren auf freie Felder setzen.

    EINE Funktion fuer die Platzwahl (Schnitt S-1). Je Gebaeude fuehrt
    ``STARTGEBAEUDE_VORLIEBEN`` das Wunschgelaende; gibt es keines, nimmt die Gruendung das
    beste freie Feld (das erste freie, auf dem das Gebaeude nach ``gelaende.bau_moeglich``
    stehen darf) und meldet das als Ersatz. Zu kleine oder volle Karten setzen so viele Gebaeude
    wie moeglich und nennen die fehlenden - geworfen wird nie.

    Die Gebaeude werden DIREKT in ``ort.bauten``/``ort.stufen`` geschrieben (Stufe 1), nicht
    ueber ``bauen_auf_karte``: so kosten sie nichts, binden keine Siedler, und der Tempel
    braucht keine Baukunst (Gruendungs-Ausnahme). Rueckgabe: je Gebaeude ein dict
    {gebaeude, gelaende, feld, x, y, wunsch, fehlend} - ``feld`` ist None, wenn kein Platz war.
    """
    raster = list((karte or {}).get("raster") or [])
    spalten = int((karte or {}).get("spalten") or 0)
    belegt = {int(k) for k in (getattr(ort, "bauten", None) or {}) if str(k).isdigit()}
    ergebnisse = []
    for gebaeude_key, vorlieben in STARTGEBAEUDE_VORLIEBEN:
        feld = None
        wunsch = False
        for art in vorlieben:
            # Remake-Entscheidung (Schnitt S-1): belegt wird das HOECHSTE freie Wunschfeld, damit
            # die vorderen Felder (die der Spieler auf der Karte zuerst anklickt) frei bleiben.
            for i in range(len(raster) - 1, -1, -1):
                if i in belegt or raster[i] != art:
                    continue
                feld = i
                wunsch = True
                break
            if feld is not None:
                break
        if feld is None:
            # Ersatz: das hoechste freie Feld, auf dem das Gebaeude stehen darf (Gelaenderegel).
            for i in range(len(raster) - 1, -1, -1):
                if i in belegt:
                    continue
                erlaubt, _ = gelaende.bau_moeglich(gebaeude_key, raster[i])
                if erlaubt:
                    feld = i
                    break
        if feld is None:
            ergebnisse.append({"gebaeude": gebaeude_key, "gelaende": None, "feld": None,
                               "x": None, "y": None, "wunsch": False, "fehlend": True})
            continue
        belegt.add(feld)
        ort.bauten[str(feld)] = gebaeude_key
        ort.stufen[str(feld)] = 1
        ergebnisse.append({"gebaeude": gebaeude_key, "gelaende": raster[feld],
                           "feld": feld, "x": feld % spalten if spalten else 0,
                           "y": feld // spalten if spalten else 0,
                           "wunsch": wunsch, "fehlend": False})
    return ergebnisse


def _startgebaeude_meldung(ergebnisse) -> str:
    """Die Gruendungsmeldung der Startgebaeude: ein Satz je Gebaeude mit Gelaende und Feld."""
    saetze = []
    for eintrag in ergebnisse:
        name = gelaende.gebaeude_name(eintrag["gebaeude"])
        if eintrag.get("fehlend"):
            saetze.append(f"kein Bauplatz fuer {name}")
            continue
        gname = gelaende.name(eintrag["gelaende"])
        koordinate = f"({eintrag['x']},{eintrag['y']})"
        if eintrag["wunsch"]:
            saetze.append(f"{name} auf {gname} {koordinate}")
        else:
            vorlieben = dict(STARTGEBAEUDE_VORLIEBEN)[eintrag["gebaeude"]]
            wunsch_text = "/".join(gelaende.name(a) for a in vorlieben)
            saetze.append(f"kein {wunsch_text} frei - Ersatz auf {gname} {koordinate}")
    return " · ".join(saetze)


# ---------- Config ----------

# Icon-Dateien: bevorzugt die freigestellte Fassung aus assets/icons/clean/ — dort ist der
# Blatthintergrund entfernt (tools/clean_icons.py). Fehlt sie, wird die Originaldatei genommen.
# Die Wurzel kommt aus spieldaten: nur so findet die fertige EXE ihre Bilder
# (`__file__` zeigt im Paket nicht auf den entpackten Ordner).
ICON_WURZEL = spieldaten.projektwurzel()


def ist_verpackt() -> bool:
    """Laeuft das Programm als EXE (PyInstaller)?"""
    import sys
    return bool(getattr(sys, "frozen", False))


def schreibordner() -> str:
    """Wohin Spielstand und Sperrdatei gehoeren — NIE in den Programmordner.

    In der fertigen EXE ist der Programmordner oft schreibgeschuetzt, und die Einzeldatei entpackt
    sich in einen Zwischenordner, der beim Beenden verschwindet. Deshalb liegt alles Schreibbare
    unter ``~/.nebelseetal`` — dort liegt auch das Passworttor (`tor.ORDNER`).
    """
    # GPT-ABS05: optionale isolierte Testwelt. Grundpassworttor bleibt GLOBAL
    # bei tor.STANDARD_PFAD; nur Adminfreigabe und Spielstaende werden getrennt.
    testpfad = os.environ.get("NEBEL_SPIELDATEN_ORDNER", "").strip()
    if testpfad:
        os.makedirs(testpfad, exist_ok=True)
        return os.path.abspath(testpfad)
    return tor.ORDNER


def icon_pfad(relativ: str) -> str:
    """Absoluter Pfad zu einem Icon; die freigestellte Fassung hat Vorrang."""
    if not relativ:
        return ""
    rest = relativ.replace("assets/icons/", "").replace("/", os.sep)
    sauber = os.path.join(ICON_WURZEL, "assets", "icons", "clean", rest)
    if os.path.exists(sauber):
        return sauber
    return os.path.join(ICON_WURZEL, relativ.replace("/", os.sep))


# ---------- Baupreise ----------
# VORSCHLAG, nicht belegt: das Handbuch nennt keine Baupreise (geprueft 04.10.2026).
# Die Zahlen stehen in data/baupreise.json und sind dort begruendet; Daniel kann sie dort aendern.

BAUPREISE_DATEI = os.path.join(ICON_WURZEL, "data", "baupreise.json")
# Daniels Entscheidung 31.10.2026 (Frage 5 = B): Bauten binden keine Siedler mehr.
BAUSIEDLER_DATEI = os.path.join(ICON_WURZEL, "data", "bausiedler.json")


def bausiedler_aktiv() -> bool:
    """Binden Bauten Siedler? (Daniels Entscheidung 31.10.2026, Frage 5 = B: NEIN.)

    Die belegten Preise (Holzfäller, Steinmetz, Jäger je 1 Siedler, Screenshot 1838857) bleiben
    in `data/baupreise.json` stehen; der Schalter in `data/bausiedler.json` nimmt nur den
    Siedler-Posten aus der Zahlung. EINE Lesestelle: `wirtschaft.siedler_bindung_aktiv()`.
    """
    return wirtschaft.siedler_bindung_aktiv()


def baukosten(gebaeude_key: str, stufe: int = 0) -> dict:
    """
    Baupreis eines Gebaeudes.

    Enthaelt neben Rohstoffen ggf. den Posten "siedler" (belegt: Holzfäller, Steinmetz und Jäger
    kosten je 1 Siedler, der dann dort arbeitet; Screenshot 1838857). Ausbau auf Stufe n kostet das
    n-fache. Seit Daniels Entscheidung 31.10.2026 (Frage 5 = B) nimmt `bausiedler_aktiv()` diesen
    Posten wieder heraus - die belegten Zahlen in der Datei bleiben unangetastet.
    """
    try:
        with open(BAUPREISE_DATEI, encoding="utf-8") as f:
            daten = json.load(f)["preise"]
    except (OSError, KeyError, ValueError):
        return {}
    kennung = gelaende.finde_gebaeude(gebaeude_key) or gebaeude_key
    eintrag = daten.get(kennung) or {}
    faktor = max(1, stufe)
    # nur Zahlen durchlassen: die Datei traegt auch Begruendungstexte (_belegt, budget)
    kosten = {r: v * faktor for r, v in eintrag.items()
              if (r in RESOURCES or r == "siedler") and isinstance(v, (int, float))}
    if not bausiedler_aktiv():
        kosten.pop("siedler", None)
    return kosten


def kosten_text(kosten: dict) -> str:
    """Kosten als lesbarer Text, z. B. '8 Holz, 4 Stein'."""
    if not kosten:
        return "Preis offen"
    return ", ".join(f"{int(v)} {r.capitalize()}" for r, v in kosten.items())


# ---------- Die zwei Ansichten: "lokal" und "Reich" (Schritt 9, Teil 3b) ----------
# Seit Teil 3a FUEHREN die Ortslager (`Settlement.vorraete`/`.bevoelkerung`); die Gesamtsicht
# (`GameState.resources`/`.population`) ist die Summe aus Uebergangsrest und Ortslagern. Vorher
# zeigten Seitenleiste und Siedlungsliste nur die Gesamtsicht — der Spieler las damit eine Zahl,
# die nicht mehr "Lager dieser Siedlung" bedeutet (KONTEXT_PAKET, Abschnitt 2, Teil 3b). Diese
# beiden Helfer sind die EINE Quelle fuer den Wortlaut, damit Liste und Siedlungskarte nie
# auseinanderlaufen und die Pruefung sie ohne Fenster nachrechnen kann.

def zahl_text(wert) -> str:
    """Eine Zahl lesbar: ganze ohne Nachkommastelle, sonst auf eine Stelle gerundet."""
    z = float(wert)
    return str(int(round(z))) if abs(z - round(z)) < 1e-9 else f"{z:.1f}"


def mengen_text(werte: dict, reihenfolge=None, leer: str = "leer") -> str:
    """Nur die vorhandenen Posten als 'Menge Name', in fester Reihenfolge.

    ``reihenfolge`` ist die Wunschordnung (z. B. ``RESOURCES``); unbekannte Posten folgen
    alphabetisch, damit auch eine Ware aus einem alten Spielstand nicht stillschweigend
    verschwindet.
    """
    posten = {str(k): float(v) for k, v in (werte or {}).items() if float(v) > 1e-9}
    if not posten:
        return leer
    vorne = [k for k in (reihenfolge or []) if k in posten]
    hinten = sorted(k for k in posten if k not in vorne)
    return ", ".join(f"{zahl_text(posten[k])} {k.capitalize()}" for k in vorne + hinten)


NACHRICHTEN_FARBEN = {"kampf": "#e53935", "geschenk": "#7FD1FF", "spionage": "#A97BD6"}


def nachrichten_farbe(nachricht) -> str:
    """Farbe einer Nachricht in der Nachrichtenansicht (EINE Stelle, pruefbar ohne Fenster).

    Rot = Kampf, hellblau = Schenkung/Botschaft von aussen (Portal), sonst Gold. Die Palette ist
    bewusst klein: eine Farbe je BEDEUTUNG, nicht je Absender.
    """
    art = str((nachricht or {}).get("type") or "")
    return NACHRICHTEN_FARBEN.get(art, "#DAA520")


def ortsbestand_text(siedlung) -> str:
    """Der sichtbare Bestand EINES Ortes — das LOKALE Lager (fuehrend seit Teil 3a).

    Liest genau ``Settlement.vorraete``/``Settlement.bevoelkerung``, nie den Reichsbestand.
    Der Gegenpart fuer das ganze Reich ist ``reichsbestand_text``.
    """
    text = mengen_text(getattr(siedlung, "vorraete", None) or {}, RESOURCES)
    return f"{text} \u00b7 {zahl_text(getattr(siedlung, 'bevoelkerung', 0.0))} Siedler"


def reichsbestand_text(state) -> str:
    """Der sichtbare GESAMTBESTAND des Reiches (``GameState.resources``/``.population``).

    Seit Teil 3a ist das die Summe aus Uebergangsrest und Ortslagern; die Anzeige nennt sie
    deshalb ausdruecklich 'Reich', damit sie nicht mit dem Lager EINER Siedlung verwechselt wird.
    """
    werte = {r: res.amount for r, res in (getattr(state, "resources", None) or {}).items()}
    text = mengen_text(werte, RESOURCES)
    return f"{text} \u00b7 {zahl_text(getattr(state, 'population', 0.0))} Siedler"


# Die neun Originalrohstoffe aus data/resources.json (Handbuch Seiten 9-10), in der Reihenfolge
# des Handbuchs. Erfunden waren: kristall, stoff, geld, wissen — eisen hiess im Handbuch Metall.
RESOURCES = ["holz", "stein", "metall", "mana", "nahrung", "gold", "wolle", "leder", "pferde"]
RESOURCE_ICONS = {
    "holz": "🌲", "stein": "🪨", "metall": "⛏️", "mana": "🔮", "nahrung": "🌾",
    "gold": "💰", "wolle": "🧶", "leder": "🦬", "pferde": "🐴",
}


def kopf_zeilen_text(state, rohstoff: str, ertrag_jetzt: dict) -> Tuple[str, bool]:
    """Beschriftung eines Rohstoffs in der Kopfzeile: Bestand und Rate je Spielstunde.

    EINE Stelle fuer Aufbau und Neuzeichnen der Kopfzeile. Bei **Nahrung** ist die Rate NETTO:
    Ernte minus laufender Verbrauch der Garnison aus `spieloekonomie.verbrauch_pro_stunde` -
    dieselbe Funktion, die auch `spieloekonomie.ort_tick` bucht (keine zweite Rechnung).
    Rueckgabe: (Text, Warnfarbe). Warnfarbe bisher = "kein Erzeuger"; neu zusaetzlich bei
    negativer Netto-Rate (die Garnison isst mehr, als der Ort erntet).
    """
    menge = int(getattr(state.resources[rohstoff], "amount", 0))
    ernte = float(ertrag_jetzt.get(rohstoff, 0.0) or 0.0)
    rate = ernte
    if rohstoff == "nahrung":
        rate = ernte - spieloekonomie.verbrauch_pro_stunde(getattr(state, "settlements", []) or [])
    ohne_quelle = ernte <= 0 and rohstoff in ("holz", "stein", "nahrung") and bool(state.settlements)
    if ohne_quelle:
        return f"{RESOURCE_ICONS[rohstoff]} {menge} (\u26a0)", True
    # Vorher stand hier `if rate else "0"` - eine NEGATIVE Rate ergab "+-3/h". Jetzt sauber.
    text = f"+{rate:g}/h" if rate > 0 else (f"{rate:g}/h" if rate < 0 else "0")
    return f"{RESOURCE_ICONS[rohstoff]} {menge} ({text})", rate < 0


def kopf_rate_text(state, rohstoff: str, ertrag_jetzt: dict) -> Tuple[str, bool]:
    """Nur die RATE eines Rohstoffs fuer die Detailzeile unter der Ressourcenleiste.

    Seit die Leiste die MENGEN zeigt (Register 121), steht in der Detailzeile kein Betrag mehr -
    sonst stuende dieselbe Zahl zweimal im Kopf. Gerechnet wird mit DERSELBEN Quelle wie in
    `kopf_zeilen_text`: `spieloekonomie.verbrauch_pro_stunde` liefert bei Nahrung den laufenden
    Verbrauch der Garnison, den auch `ort_tick` bucht. Keine zweite Formel.
    """
    ernte = float(ertrag_jetzt.get(rohstoff, 0.0) or 0.0)                                 # Ernte je Stunde
    rate = ernte                                                                          # Grundwert ist die Ernte
    if rohstoff == "nahrung":                                                             # bei Nahrung zaehlt netto
        rate = ernte - spieloekonomie.verbrauch_pro_stunde(getattr(state, "settlements", []) or [])   # Verbrauch abziehen
    ohne_quelle = ernte <= 0 and rohstoff in ("holz", "stein", "nahrung") and bool(state.settlements)   # kein Erzeuger?
    if ohne_quelle:                                                                       # dann Warnzeichen
        return f"{RESOURCE_ICONS[rohstoff]} (\u26a0)", True                                # Menge steht auf der Leiste
    text = f"+{rate:g}/h" if rate > 0 else (f"{rate:g}/h" if rate < 0 else "0")            # Vorzeichen sauber
    return f"{RESOURCE_ICONS[rohstoff]} {text}", rate < 0                                  # (Rate, Warnfarbe)


def _lade_ressourcenleiste() -> Dict[str, Any]:
    """Die Ressourcenleiste aus `data/ressourcenleiste.json` lesen (Bild, Masse, acht Felder).

    Die Datei ist die EINE Quelle fuer Bildpfad, Feldpositionen und Farben; ohne sie bleibt der
    Kopf wie vorher (kein Absturz, keine erfundene Leiste).
    """
    pfad = os.path.join(ICON_WURZEL, "data", "ressourcenleiste.json")                      # Datendatei
    try:                                                                                  # Datei lesen
        with open(pfad, encoding="utf-8") as f:                                            # UTF-8 wie alle Spieldaten
            daten = json.load(f)                                                           # Inhalt als dict
    except (OSError, ValueError):                                                          # fehlt oder kaputt
        return {}                                                                          # dann kein Leistenbild
    if not daten.get("datei") or not daten.get("felder"):                                  # unvollstaendig
        return {}                                                                          # lieber ohne Leiste
    return daten                                                                           # fertige Beschreibung


RESSOURCENLEISTE: Dict[str, Any] = _lade_ressourcenleiste()                                # einmal beim Import

# Rohstoffe, deren MENGE auf der Leiste steht - ihre Detailzeile zeigt nur die Rate (Register 121).
LEISTEN_ROHSTOFFE = tuple(sorted({str(f.get("quelle")) for f in RESSOURCENLEISTE.get("felder") or []
                                  if str(f.get("quelle")) in ("holz", "stein", "metall", "mana",
                                                              "nahrung", "gold")}))


def _leisten_stuecke(leiste: dict) -> list:
    """Die Leiste in Stuecke zerlegen: feste Ecken und Symbolfelder, dehnbare Luecken dazwischen.

    Ein festes Stueck wird NUR gleichmaessig skaliert (Symbol und Zahlenplakette bleiben in Form),
    eine Luecke wird waagerecht gedehnt - so wird der Balken breiter, ohne dass ein Symbol verzerrt
    (Daniels Befund 02.11.2026: das ganze Bild auf Fensterbreite zu ziehen machte die Symbole haesslich).
    """
    breite = int(leiste.get("breite") or 1440)                                       # Originalbreite
    halb = int(leiste.get("kachel_halbbreite") or 55)                                 # halbe Feldbreite
    felder = [f for f in (leiste.get("felder") or []) if f.get("x") is not None]       # acht Felder mit Position
    if not felder:                                                                    # ohne Felder
        return [{"art": "dehnbar", "von": 0, "bis": breite, "feld": None}]             # bleibt das ganze Bild dehnbar
    stuecke = [{"art": "fest", "von": 0, "bis": max(0, int(felder[0]["x"]) - halb), "feld": None}]   # linke Ecke (Banner)
    for i, feld in enumerate(felder):                                                  # je Feld eine feste Kachel
        x = int(feld["x"])                                                             # Mittelpunkt des Feldes
        stuecke.append({"art": "fest", "von": max(0, x - halb), "bis": min(breite, x + halb),
                        "feld": str(feld.get("schluessel"))})                          # Symbol samt Plakette
        if i + 1 < len(felder):                                                        # Luecke zum naechsten Feld
            naechste = max(0, int(felder[i + 1]["x"]) - halb)                           # Anfang des naechsten Feldes
            stuecke.append({"art": "dehnbar", "von": min(breite, x + halb), "bis": naechste, "feld": None})
    stuecke.append({"art": "fest", "von": min(breite, int(felder[-1]["x"]) + halb), "bis": breite, "feld": None})   # rechte Ecke
    return [s for s in stuecke if s["bis"] > s["von"]]                                   # leere Stuecke weg


def leiste_zusammensetzen(leiste: dict, zielbreite: int):
    """(Bild, Mittelpunkte, Skala) der Leiste fuer eine Zielbreite - ohne Tk, damit pruefbar.

    Feste Stuecke wachsen gleichmaessig (Skala bis `skala_max`), die Luecken bekommen den Rest der
    Breite. Ist das Fenster schmaler als die festen Stuecke, wird die Gesamtskala kleiner, damit
    nichts abgeschnitten wird. Ohne Pillow kommt ``(None, {}, 0.0)`` zurueck.
    """
    try:                                                                              # Pillow nur hier
        from PIL import Image                                                          # Bildverarbeitung
    except Exception:                                                                  # noqa: BLE001
        return None, {}, 0.0                                                           # ohne Pillow keine Leiste
    pfad = icon_pfad(str(leiste.get("datei") or ""))                                    # Originalbild im Projekt
    if not pfad or not os.path.exists(pfad):                                            # Datei fehlt
        return None, {}, 0.0                                                           # dann bleibt der Kopf textbasiert
    quelle = Image.open(pfad).convert("RGBA")                                           # Original mit Alphakanal
    breite = int(leiste.get("breite") or quelle.width)                                  # Bezugsbreite
    skala_max = float(leiste.get("skala_max") or 1.5)                                   # Obergrenze fuer das Wachstum
    # P-3 (02.11.2026): die LUECKEN werden nur noch bis zu dieser Grenze gedehnt. Vorher nahmen sie die
    # gesamte Restbreite auf - bei 2560 px war das Faktor 1,86, bei 3440 px 3,75, und die gemalte
    # Landschaft zwischen den Symbolen wurde zu langgezogenen Streifen mit harten Naehten (Daniels
    # Befund: die Landschaft wiederholt sich). Zahlen in data/ressourcenleiste.json.
    luecke_max = float(leiste.get("luecke_max") or 1.35)                                # Obergrenze der Lueckendehnung
    rest_modus = str(leiste.get("rest_auffuellen") or "gleichmaessig")                  # was mit der Restbreite geschieht
    # M-3 (Daniels Befund 02.11.2026: "die ressourcen bilder oben [sind] verzerrt"): Modus 'kacheln'.
    # Dann skaliert das Band NIE ueber 1,0 - die Symbole bleiben pixelgenau wie im Original - und die
    # zusaetzliche Breite entsteht durch WIEDERHOLUNG der gemalten Luecken (Landschaft) statt durch
    # Dehnen. Vorher wuchs bei breiten Fenstern das ganze Band bis Faktor 1,75; Daniel hat das als
    # verzerrt gesehen, obwohl die Skalierung gleichmaessig war - die Symbolbilder sind klein und
    # wirken vergroessert unscharf.
    kacheln = rest_modus == "kacheln"                                                  # Wiederholung statt Dehnung
    skala_hart = float(leiste.get("skala_hart") or 1.75)                                # Obergrenze, wenn gleichmaessig gefuellt wird
    stuecke = _leisten_stuecke(leiste)                                                  # Schnittliste
    fest = sum(s["bis"] - s["von"] for s in stuecke if s["art"] == "fest")              # Breite aller festen Teile
    dehn = sum(s["bis"] - s["von"] for s in stuecke if s["art"] == "dehnbar")           # Breite aller Luecken
    ziel = max(1, int(zielbreite))                                                      # Zielbreite als Zahl
    skala = min(ziel / float(breite), skala_max)                                        # gleichmaessige Skala
    if kacheln:                                                                         # M-3: nie vergroessern
        skala = min(1.0, ziel / float(breite))                                          # nur schrumpfen, wenn noetig
    rest = ziel - fest * skala                                                          # was die Luecken fuellen muessen
    if rest < 0:                                                                        # Fenster schmaler als die festen Teile
        skala = ziel / float(fest) * 0.995                                              # kleiner skalieren, nichts abschneiden
        rest = 0                                                                        # Luecken schrumpfen auf null
    if kacheln:                                                                         # M-3: Luecken werden WIEDERHOLT
        gap_faktor = 1.0                                                                # keine Dehnung
    else:
        gap_faktor = (rest / (dehn * skala)) if dehn and skala else 1.0                 # Dehnung der Luecken
        if gap_faktor > luecke_max and rest_modus == "gleichmaessig" and fest + dehn * luecke_max > 0:
            # Die Luecken reichen nicht: stattdessen das GANZE Band gleichmaessig groesser skalieren
            # (das bleibt eine treue Vergroesserung ohne Naehte), hoechstens bis `skala_hart`.
            skala = min(ziel / float(fest + dehn * luecke_max), skala_hart)             # neue, groessere Skala
            rest = ziel - fest * skala                                                  # Restbreite neu rechnen
            gap_faktor = min((rest / (dehn * skala)) if dehn and skala else 1.0, luecke_max)  # gedeckelt
        gap_faktor = min(gap_faktor, luecke_max)                                        # nie ueber die Grenze
    hoehe = max(1, int(round(quelle.height * skala)))                                   # Hoehe folgt der Skala
    # Breiten VORAB rechnen: nur so ist die Gesamtbreite bekannt, und ein Rest laesst sich SYMMETRISCH
    # verteilen. Eine linksbuendige Leiste mit Rest am rechten Rand sieht wie ein Fehler aus (eigene
    # Sichtpruefung docs/audits/leisten_vergleich_20261102.png); mittige Raender wirken als Abschluss.
    breiten_stueck = []                                                                 # Breite je Stueck in Pixeln
    for stueck in stuecke:                                                              # Stueck fuer Stueck
        roh = stueck["bis"] - stueck["von"]                                             # Breite im Original
        if stueck["art"] == "fest":                                                     # feste Kachel
            breiten_stueck.append(max(1, int(round(roh * skala))))                      # gleichmaessig skaliert
        elif kacheln:                                                                   # M-3: Anteil der Restbreite
            anteil = (roh / float(dehn)) if dehn else 0.0                               # Anteil dieser Luecke
            breiten_stueck.append(max(1, int(round(max(0.0, rest) * anteil))))          # diesen Anteil bekommt sie
        else:                                                                           # dehnbare Luecke
            breiten_stueck.append(max(1, int(round(roh * skala * gap_faktor))))         # waagerecht gedehnt
    if kacheln and breiten_stueck:                                                      # M-3: Rundungsrest ausgleichen
        fehl = ziel - sum(breiten_stueck)                                               # was noch fehlt
        if fehl != 0:                                                                   # ein paar Pixel
            index = max(range(len(stuecke)), key=lambda i: (stuecke[i]["art"] == "dehnbar",
                                                            breiten_stueck[i]))          # groesste Luecke
            breiten_stueck[index] = max(1, breiten_stueck[index] + fehl)                 # dort dazu
    rand = max(0, (ziel - sum(breiten_stueck)) // 2) if rest_modus != "leer" else 0      # Rest mittig verteilen
    gesamt = Image.new("RGBA", (ziel, hoehe), (0, 0, 0, 0))                             # leere Flaeche
    x = rand                                                                            # Schreibposition (ggf. eingerueckt)
    mitten = {}                                                                        # Feld -> (x, y) im neuen Bild
    for stueck, w in zip(stuecke, breiten_stueck):                                      # Stueck fuer Stueck
        if kacheln and stueck["art"] == "dehnbar":                                      # M-3: Luecke wiederholen
            kachel = quelle.crop((stueck["von"], 0, stueck["bis"], quelle.height))      # ein Stueck Landschaft
            if abs(skala - 1.0) > 1e-6 and kachel.width > 0:                            # nur beim Schrumpfen
                kachel = kachel.resize((max(1, int(round(kachel.width * skala))), hoehe), Image.LANCZOS)
            gelegt = 0                                                                  # schon gefuellte Breite
            while gelegt < w and kachel.width > 0:                                      # so oft, bis die Breite steht
                rest_breite = min(kachel.width, w - gelegt)                              # letztes Stueck wird beschnitten
                teil = kachel.crop((0, 0, rest_breite, hoehe))                          # dieses Stueck
                if x + gelegt + teil.width > gesamt.width:                              # nicht ueber den Rand
                    teil = teil.crop((0, 0, max(1, gesamt.width - x - gelegt), hoehe))  # auf den Rest kuerzen
                gesamt.alpha_composite(teil, (x + gelegt, 0))                           # einsetzen
                gelegt += teil.width                                                    # weiterruecken
                if teil.width <= 0:                                                     # nichts mehr moeglich
                    break                                                               # Abbruch
            x += w                                                                      # Stueck ist fertig
            continue                                                                    # naechstes Stueck
        q = quelle.crop((stueck["von"], 0, stueck["bis"], quelle.height))               # Ausschnitt aus dem Original
        teil = q.resize((w, hoehe), Image.LANCZOS)                                      # auf die vorberechnete Breite
        if x + w > gesamt.width:                                                       # letzte Luecke exakt abschliessen
            w = max(1, gesamt.width - x)                                                # auf den Rest begrenzen
            teil = teil.resize((w, hoehe), Image.LANCZOS)                               # neu schneiden
        gesamt.alpha_composite(teil, (x, 0))                                            # einsetzen
        if stueck.get("feld"):                                                          # Symbolfeld merken
            mitten[str(stueck["feld"])] = (x + w // 2, int(round(float(
                next((f.get("y") for f in leiste.get("felder") or [] if str(f.get("schluessel")) == stueck["feld"]), 105)) * skala)))
        x += w                                                                          # weiterruecken
    return gesamt, mitten, skala                                                        # Bild, Mittelpunkte, Skala


def leistenwert(state, feld: dict) -> str:
    """Den Anzeigewert EINES Leistenfeldes rechnen - eine Stelle fuer Aufbau und Neuzeichnen.

    `quelle` nennt die Rechenquelle: `bevoelkerung` (Reichssiedler), `punkte` (Gesamtpunkte aus
    `state.punktestand()`) oder einen Rohstoff aus `state.resources`. Tausenderpunkte machen die
    Zahl lesbar; gerechnet wird nichts weiter.
    """
    quelle = str(feld.get("quelle") or feld.get("schluessel") or "")                       # Quelle des Wertes
    if quelle == "bevoelkerung":                                                           # Siedler des Reichs
        wert = float(getattr(state, "population", 0.0) or 0.0)                              # Summe der Orte
    elif quelle == "punkte":                                                               # Gesamtpunkte
        wert = float((state.punktestand() or {}).get("gesamt", 0) or 0)                     # aus der Punkteformel
    else:                                                                                  # ein Rohstoff
        eintrag = (getattr(state, "resources", {}) or {}).get(quelle)                       # Reichsbestand
        wert = float(getattr(eintrag, "amount", 0) or 0)                                   # Betrag als Zahl
    return f"{wert:,.0f}".replace(",", ".")                                                # 1234 -> "1.234"


def kopfzeile_fuer(state, rohstoff: str, ertrag_jetzt: dict) -> Tuple[str, bool]:
    """Text der Detailzeile: Menge + Rate, oder nur die Rate, wenn die Menge auf der Leiste steht.

    Diese Funktion ist die EINE Stelle fuer Aufbau UND Neuzeichnen der Kopfzeile (Register 121);
    sie waehlt nur aus, welche der beiden Anzeigeformen gilt.
    """
    if rohstoff in LEISTEN_ROHSTOFFE and RESSOURCENLEISTE:                                 # Menge steht auf der Leiste
        return kopf_rate_text(state, rohstoff, ertrag_jetzt)                                # dann nur die Rate
    return kopf_zeilen_text(state, rohstoff, ertrag_jetzt)                                  # sonst Menge und Rate

# LEER seit W4b-5 (04.10.2026) — und das ist der Punkt.
#
# Hier standen fuenf ERFUNDENE Wirkungsgebaeude (Haus, Bibliothek, Kaserne, Wachturm, Portal).
# Ihre Wirkung lag global, waehrend die 20 belegten Originalgebaeude aus data/buildings.json
# zwar auf der Siedlungskarte standen, aber (ausser der Produktion) nichts taten. Seit W4b-5
# kommt JEDE Gebaeudewirkung aus den bebauten Feldern der Siedlungskarten — die Rechnung dazu
# steht in `gebaeude_wirkung.py`:
#
#   Haus           -> Siedlergrenze +5 Siedler (je Siedlung; Grundwert 10)
#   Bibliothek     -> ermoeglicht Forschung (und nur auf Grasland/Steppe/Nebelsee)
#   Kriegerakademie-> bildet die 9 Kampfeinheiten aus
#   Diebesgilde    -> bildet die 6 Kundschafter aus
#   Stellmacher    -> baut 6 Karren und 7 Belagerungswaffen
#   Verteidigungswall -> Wallstufen, Schwellenwerte der Vorrunde, Kriegspunkte
#   die uebrigen 14 -> Rohstoffertrag (Paket W4b-4, `wirtschaft.py`)
#
# Die erfundene globale Liste ist damit ersatzlos entfallen: sie haette jede Wirkung ein
# zweites Mal erzeugt. Wer hier wieder ein Gebaeude eintraegt, baut den alten Fehler nach.
BUILDINGS: Dict[str, Building] = {}
# Einheiten der Originaldaten (Handbuch Seiten 14-17).
# Vorher standen hier 36 erfundene Einheiten (Worg, Drache, Troll, Golem ...): sie sind
# ersatzlos entfernt, alles kommt aus data/units.json ueber die Bruecke einheiten.py.
# Karren und Belagerungswaffen haben im Handbuch keine LE/AT, weil sie nicht kaempfen —
# attack und defense bleiben dort 0, und `rolle` sagt, wie die Einheit wirkt.
UNIT_ICONS: Dict[str, str] = {}


def _lade_motivdaten() -> tuple:
    """(Gebaeude -> Motivdatei, Rahmenart -> Datei, Rahmen-Deckkraft in Prozent) aus den Spieldaten.

    ENTSCHEIDUNG Daniel 02.11.2026 (Register 119): die Siedlungskarte zeigt die **20 freigestellten
    C2-Motive** (256 x 256 px, RGBA) aus dem Block `c2_motive`. Der Schalter `quelle_der_karte` ist
    die EINE Stelle, die das entscheidet: steht dort nicht "c2", gilt die aeltere Liste `motive`
    (acht Handbuchmotive, Register 113, nur `eingebaut: true`). Beide Listen bleiben in der Datei -
    die Handbuchmotive sind der belegte Rueckfallsatz, nichts wird geloescht.
    """
    pfad = os.path.join(ICON_WURZEL, "data", "gebaeude_motive.json")     # Datendatei im Projekt
    try:                                                                # Datei lesen
        with open(pfad, encoding="utf-8") as f:                          # UTF-8 wie alle Spieldaten
            daten = json.load(f)                                         # Inhalt als dict
    except (OSError, ValueError, KeyError):                              # Datei fehlt oder ist kaputt
        return {}, {}                                                    # dann zeichnet die Karte Baukoerper
    motive: Dict[str, str] = {}                                          # Gebaeude -> Motivdatei
    if str(daten.get("quelle_der_karte") or "") == "c2":                 # der neue Weg (C2-Motive)
        for eintrag in daten.get("c2_motive") or []:                     # je Gebaeude ein Eintrag
            gebaeude = (eintrag or {}).get("gebaeude")                    # Gebaeudekennung aus buildings.json
            datei = (eintrag or {}).get("datei")                          # Bildpfad relativ zum Projekt
            if gebaeude and datei:                                       # nur vollstaendige Eintraege
                motive[str(gebaeude)] = str(datei)                        # Zuordnung uebernehmen
    else:                                                                # Rueckfall: Handbuchmotive
        for eintrag in daten.get("motive") or []:                        # acht Handbuchmotive
            if not isinstance(eintrag, dict) or not eintrag.get("eingebaut"):   # nur belegte Zuordnungen
                continue                                                 # unklare Motive bleiben draussen
            gebaeude = eintrag.get("gebaeude")                            # Gebaeudekennung
            datei = eintrag.get("datei")                                  # Bildpfad
            if gebaeude and datei:                                        # vollstaendig?
                motive[str(gebaeude)] = str(datei)                        # uebernehmen
    rahmen: Dict[str, str] = {}                                           # Rahmenart -> Datei
    for art in ("ruhe", "auswahl"):                                       # zwei Rahmen liefert C2
        datei = (daten.get("kachelrahmen") or {}).get(art)                # Pfad aus der Datendatei
        if datei:                                                         # nur wenn eingetragen
            rahmen[art] = str(datei)                                      # uebernehmen
    try:                                                                  # Deckkraft des Rahmens
        deckkraft = int((daten.get("kachelrahmen") or {}).get("deckkraft_prozent", 100))   # Prozent aus der Datei
    except (TypeError, ValueError):                                        # kaputter Wert
        deckkraft = 100                                                   # dann voll deckend
    try:                                                                  # Deckkraft des AUSWAHLrahmens
        deckkraft_auswahl = int((daten.get("kachelrahmen") or {}).get("deckkraft_auswahl_prozent", 100))   # eigene Zahl
    except (TypeError, ValueError):                                        # kaputter Wert
        deckkraft_auswahl = 100                                            # dann voll deckend
    return (motive, rahmen, max(0, min(100, deckkraft)),                   # Ruherahmen nie ausserhalb 0..100
            max(0, min(100, deckkraft_auswahl)))                           # Auswahlrahmen ebenso


GEBAEUDE_MOTIVE, KACHELRAHMEN, RAHMEN_DECKRAFT, AUSWAHL_DECKRAFT = _lade_motivdaten()
UNITS: Dict[str, Unit] = {}
for _name, _e in einheiten.alle().items():
    if _e["icon"]:
        UNIT_ICONS[_name] = _e["icon"]
    UNITS[_name] = Unit(
        id=_name,
        name=_e["name"],
        attack=einheiten.angriff(_name),
        defense=einheiten.verteidigung(_name),
        cost=dict(_e["kosten"]),
        training_time=0.0,       # das Handbuch nennt keine Ausbildungsdauer
        description=einheiten.beschreibung(_name),
        rolle=_e["rolle"],
    )
del _name, _e

# Die 21 ORIGINALFORSCHUNGEN aus data/research.json (Handbuch 2009, Abschnitt 5).
# Vorher standen hier 18 erfundene Gebiete (alchemie_2, zauberei, logistik, taktik …): sie sind
# ersatzlos entfernt. Grund: die belegten Produktionsfaktoren (`forschung_wirkung.py`) haengen an
# den ORIGINALNAMEN (Felderwirtschaft, Steinbruch, Forstwirtschaft, Tierhaltung, Minenarbeit,
# Goetterkunde, Heilkunde, Mauerbau) — mit erfundenen Namen wirkte keine Forschung.
#
# Obergrenze: das Handbuch nennt KEINE Hoechststufe. Hier steht 10 als VORSCHLAG, weil die Dauer
# Stufe² Stunden betraegt (Stufe 10 = 100 Stunden) — in docs/PROJEKT_STAND.md als offene
# Entscheidung vermerkt.
FORSCHUNG_HOECHSTSTUFE = 10

RESEARCHES: Dict[str, Research] = {}
for _name, _eintrag in spieldaten.forschungen().items():
    RESEARCHES[_name] = Research(
        id=_name,
        name=_name,
        max_level=FORSCHUNG_HOECHSTSTUFE,
        effect=(_eintrag.get("wirkung") or "Wirkung im Handbuch nicht beschrieben")[:90],
    )
del _name, _eintrag

# W3 (Werkstatt): die 17 ORIGINALwaren aus data/items.json. Jede Ware nennt ihre Werkstatt,
# ihre Voraussetzung (Forschung + Stufe) und ihr Original-Icon aus den Icon-Blaettern.
WARE_EINTRAEGE: Dict[str, Dict[str, object]] = spieldaten.waren()
WARE_ICONS: Dict[str, str] = {name: str(eintrag.get("icon") or "")
                              for name, eintrag in WARE_EINTRAEGE.items()}

MAPS = [
    {"id": "kontinent", "name": "Der Kontinent", "size": 20, "difficulty": 1, "bonus": "nahrung", "npcs": ["dorf", "händler"], "quests": ["Erstes Zuhause", "Siedlerzug"], "sectors": True},
    {"id": "wald", "name": "Nebelwald", "size": 8, "difficulty": 2, "bonus": "holz", "npcs": ["jäger", "schamane"], "quests": ["Geister des Waldes", "Verlorenes Artefakt"]},
    {"id": "berge", "name": "Hochfels", "size": 8, "difficulty": 3, "bonus": "stein", "npcs": ["zwerge", "drachen"], "quests": ["Der verborgene Schacht", "Drachenei"]},
    {"id": "sümpfe", "name": "Glimmersümpfe", "size": 7, "difficulty": 2, "bonus": "mana", "npcs": ["hexe", "banditen"], "quests": ["Sumpffieber", "Banditenlager"]},
    {"id": "portalreich", "name": "Portalreich", "size": 10, "difficulty": 4, "bonus": "gold", "npcs": ["wächter", "magier"], "quests": ["Portalwächter", "Arkaner Schlüssel"]},
]
# ---------- Weltkarte: astra-Bildgutachten 05.10.2026, Abschnitt A3 ----------
# astra verlangt ein gedämpftes Farbbild, 48 px je Feld als Standard und Zoomstufen. Die Stufen,
# die Regionsnamen und die Übersichtskarte sind unser VORSCHLAG — das Originalhandbuch nennt
# weder Kachelgrößen noch Regionsnamen; es belegt nur die 20x20-Dimension und grün/rot im Portal.
WELT_ZOOM_STUFEN = (16, 24, 32, 48, 64, 96)
WELT_ZOOM_STANDARD = 48
WELT_GELAENDEFARBEN = {
    "forest": "#2F4A2E", "plains": "#6E7A3A", "mountain": "#5B5F63",
    "water": "#1F4E6E", "village": "#8A6A2A", "ruins": "#4A3B63",
}
WELT_GELAENDENAMEN = {
    "forest": "Wald", "plains": "Ebene", "mountain": "Gebirge",
    "water": "Wasser", "village": "Dorf", "ruins": "Ruine",
}
WELT_GELAENDEREIHENFOLGE = ("forest", "plains", "mountain", "water", "village", "ruins")
WELT_REGIONEN = ("Nordwesten", "Norden", "Nordosten",
                 "Westen", "Zentrum", "Osten",
                 "Südwesten", "Süden", "Südosten")

BOTS = [
    BotPlayer("Haug", "menschlich", aggression=0.3, trading=0.8),
    BotPlayer("Brynhild", "menschlich", aggression=0.5, trading=0.6),
    BotPlayer("Grom", "zwergisch", aggression=0.7, trading=0.4),
    BotPlayer("Silra", "elfisch", aggression=0.2, trading=0.9),
    BotPlayer("Krank", "Trolle", aggression=0.9, trading=0.0),
]
# W5 (botkern): Der Bot-Zug. Der Entwurf nennt den Pruefrhythmus "alle 6 bis 24 Stunden"
# (VORSCHLAG, in botkern.py belegt vermerkt); `botkern.tick` wuerde bei jedem Sekundentakt eine
# Meldung erzeugen, deshalb wird der Bot-Zug stundenweise gefahren.
BOT_TAKT_SEKUNDEN = 3600.0


def bot_takt_punkte(ab: float, bis: float, takt: float = BOT_TAKT_SEKUNDEN) -> List[float]:
    """Die FESTEN Spielzeit-Punkte der Bot-Zuege in der Spanne (ab, bis] (S-13, 03.11.2026).

    Daniels Entscheidung 3 von heute: der Bot-Takt haengt nicht mehr an der Fliesskomma-Differenz
    `jetzt - letzter`, sondern an festen Spielzeit-Punkten (jede volle Stunde Spielzeit). Damit ist
    `1 x 3600 s` GENAU SO VIEL wie `10 x 360 s` - die Zahl der Bot-Aktionen haengt nur an der
    Spielzeit, nicht am Zuschnitt des Takts.

    Was hinein geht: zwei Spielzeiten in Sekunden und der Takt (Vorgabe `BOT_TAKT_SEKUNDEN`).
    Was heraus kommt: alle Vielfachen des Takts, die GROESSER als `ab` und hoechstens `bis` sind -
    in aufsteigender Reihenfolge. Eine leere Spanne (oder ein unbrauchbarer Takt) liefert `[]`.
    """
    takt = float(takt)                                                    # Takt in Spielsekunden
    if not math.isfinite(takt) or takt <= 0:                              # kein gueltiger Takt
        return []                                                         # dann keine Punkte
    if not math.isfinite(float(ab)) or not math.isfinite(float(bis)):     # keine gueltige Spanne
        return []                                                         # dann keine Punkte
    if float(bis) <= float(ab):                                           # leere Spanne
        return []                                                         # dann keine Punkte
    erster = int(math.floor(float(ab) / takt)) + 1                        # erster Punkt NACH ab
    letzter = int(math.floor(float(bis) / takt))                          # letzter Punkt bis einschl. bis
    return [float(k) * takt for k in range(erster, letzter + 1)]          # die Punkte selbst


# W5: Grundlage des Handels-Schwellenpreises. Das Handbuch nennt keinen Warenpreis; die einzige
# BELEGTE Preistafel im Projekt ist der Einheitenpreis (`data/units.json`). Genommen wird der
# Kaempfer (1 Siedler + 250 Gold) -> Referenzpreis 250 x 1,2 = 300 (VORSCHLAG der Wahl).
BOT_BESCHAFFUNGSKOSTEN = 250.0
MENU_ITEMS = [
    "Dorfzentrum", "Lager", "Kaserne", "Marktplatz", "Gilde", "Nachrichten",
    "Portal", "Forschung", "Diplomatie", "Einstellungen",
    "Ruhmeshalle", "Anleitung", "Kampfsimulator", "Forum", "Chat", "Spieler werben"
]
# ENTFERNT am 01.11.2026 (Schnitt S-2, Daniel M-10): der Menuepunkt "Karten" (die alte Weltkarte
# "Weltkarte - Orte entdecken" mit ihren sieben Gebieten) ist weg - Daniels Wortlaut
# ("Die Weltkarte soll weg es wird hier nur noch Platz sein fuer das Dorfzentrum Lager und dessen
# verwaltung und uebersichten", docs/KONZEPT_SECHS_DOERFER_20261101.md, Anhang 1 Abschnitt 2).
# Die Weltkarte kommt als Geländekaestchen ins Portal zurueck (S-5); die alte Ansicht ist
# stillgelegt und nicht mehr verdrahtet. Die Liste hat damit 16 statt 17 Eintraege - das ist eine
# bewusste Abweichung von der belegten Original-Liste und steht als solche im Register.

# Daniel 30.10.2026: "Ab dem Moment wo man einen Stellmacher gebaut hat, sollte links im Menü
# auch ein Stellmacher auftauchen ... genauso mit der Kriegerakademie oder dem Bogenmacher ...
# Forschung soll als Menüpunkt erst existieren, sobald eine Bibliothek errichtet wurde."
# MENU_ITEMS bleibt die BELEGTE Original-Liste (tests/test_oberflaeche_original.py vergleicht sie
# mit dem Original-Muster) — hier wird nur gefiltert, nie etwas hinzu erfunden.
# Menüpunkt -> Gebaeude, das ihn freischaltet.
MENUE_BEDINGUNG = {
    "Kaserne": "kriegerakademie",
    "Forschung": "bibliothek",
    "Stellmacher": "stellmacher",
    "Diebesgilde": "diebesgilde",
}

# Vorgabe Daniel 30.10.2026: hoechstens ZWEI Bibliotheken je Spieler - eine je Karte.
# ACHTUNG, Abgleich 30.10.2026: Das Handbuch setzt diese Gesamtgrenze NICHT. Es sagt woertlich
# (Spielanleitung 2009, Seite 12): "In jeder Siedlung kann nur eine einzige Bibliothek gebaut
# werden." - also eine je Siedlung, ohne Obergrenze ueber das Spiel. Daniels Zwei-Grenze ist
# damit STRENGER als das Original und bleibt als seine Entscheidung stehen, bis er sie kippt.
BIBLIOTHEK_OBERGRENZE = 2


def bibliotheken_im_spiel(settlements) -> int:
    """Zaehlt die stehenden Bibliotheken ueber ALLE Siedlungen des Spielers.

    EINE Quelle fuer die Obergrenze und fuer die Abriss-Sperre ("die letzte bleibt stehen").
    """
    anzahl = 0
    for siedlung in (settlements or []):
        for wert in ((getattr(siedlung, "bauten", None) or {}).values()):
            if str(wert).lower().startswith("bibliothek"):
                anzahl += 1
    return anzahl


# SCHNITT S-2c (Daniel, 01.11.2026): "Das Dorfzentrum IST das Lager" - Menuepunkt UND Gebaeude.
# Der Menuepunkt "Lager" entfaellt damit in der ANZEIGE; die Lagerverwaltung steht ab jetzt im
# Dorfzentrum (`_render_overview` ruft `_render_storage` mit). MENU_ITEMS bleibt unveraendert die
# BELEGTE Original-Liste - `tests/test_oberflaeche_original.py` vergleicht sie mit dem
# Original-Muster, deshalb wird nur in `menu_sichtbar` ausgeblendet und nichts aus der Liste
# geloescht. Die Route "Lager" bleibt erreichbar (tests/test_baseline.py besucht sie) und traegt
# den Vermerk STILLGELEGT. Quelle: docs/KONZEPT_SECHS_DOERFER_20261101.md, Anhang 1.
MENUE_ENTFALLEN = {"Lager"}

# Der Menuepunkt, hinter dem die nachgereichten Gebaeude-Menuepunkte einsortiert werden. Bis S-2c
# war das "Lager"; da dieser Punkt jetzt im Dorfzentrum aufgeht, ist es das Dorfzentrum selbst
# (vorher waeren Stellmacher und Diebesgilde an das ENDE der Leiste gerutscht).
MENUE_ANKER = "Dorfzentrum"

# Menuepunkt -> Gebaeude-id, deren gerahmtes Icon im Menue steht (C2-Lieferung, Register 119/123).
# ABGELEITET, nicht getippt: erst der Anzeigename eines Gebaeudes (`gelaende.finde_gebaeude` erkennt
# Kennung, Anzeigename und alias - "Dorfzentrum" trifft also `lager`), dann die Freischalt-Tabelle
# `MENUE_BEDINGUNG` fuer die Punkte, die anders heissen als ihr Gebaeude ("Kaserne" ->
# `kriegerakademie`, "Forschung" -> `bibliothek`). Punkte ohne Gebaeude (Portal, Chat, Forum ...)
# bekommen bewusst KEIN Icon - ein erfundenes Bild waere keine Quelle.
MENU_GEBAEUDE = {punkt: gelaende.finde_gebaeude(punkt) for punkt in MENU_ITEMS
                 if gelaende.finde_gebaeude(punkt)}
MENU_GEBAEUDE.update(MENUE_BEDINGUNG)


def menu_sichtbar(settlements) -> list:
    """Welche Menuepunkte stehen offen? Haengt nur davon ab, welche Gebaeude stehen.
    Ein Gebaeude-Menuepunkt existiert erst, wenn das Gebaeude auf irgendeiner Siedlung steht.
    Steht die Kaserne nicht, wird auch ein gebauter Stellmacher sichtbar (er wird dann direkt
    hinter dem Dorfzentrum einsortiert) - sonst waere er unerreichbar.
    Menuepunkte aus `MENUE_ENTFALLEN` (S-2c: "Lager") werden ausgeblendet, nicht geloescht.
    """
    gebaut = set()
    for siedlung in (settlements or []):
        gebaut.update(str(v) for v in (getattr(siedlung, "bauten", None) or {}).values())
    sichtbar = []
    for item in MENU_ITEMS:
        if item in MENUE_ENTFALLEN:
            continue
        schluessel = MENUE_BEDINGUNG.get(item)
        if schluessel is not None and schluessel not in gebaut:
            continue
        sichtbar.append(item)
        if item == "Kaserne":
            for extra, bedingung in (("Stellmacher", "stellmacher"),
                                     ("Diebesgilde", "diebesgilde")):
                if bedingung in gebaut:
                    sichtbar.append(extra)
    for extra, bedingung in (("Stellmacher", "stellmacher"), ("Diebesgilde", "diebesgilde")):
        if bedingung in gebaut and extra not in sichtbar:
            sichtbar.insert(sichtbar.index(MENUE_ANKER) + 1 if MENUE_ANKER in sichtbar
                            else len(sichtbar),
                            extra)
    return sichtbar


# Das Original hat ZWEI Navigationsebenen, oben links umschaltbar "Uebersicht" / "Siedlung"
# (GameStar-Screenshots web_1838856 und web_1838857, ausgewertet in
# docs/quellen/ORIGINAL_UI_BEFUNDE.md). Die linke Leiste traegt in beiden Ebenen dieselben
# Punkte - je nach Ebene sind es andere, weil die Siedlungsbereiche nur in der Siedlung stehen.
EBENEN = ("Uebersicht", "Siedlung")

# Menuepunkt -> Ebene, in der er im Original steht.
EBENE_JE_PUNKT = {
    "Dorfzentrum": "Siedlung",
    "Lager": "Siedlung",
    "Kaserne": "Siedlung",
    "Stellmacher": "Siedlung",
    "Diebesgilde": "Siedlung",
    "Marktplatz": "Siedlung",
    "Forschung": "Siedlung",
    "Gilde": "Uebersicht",
    "Nachrichten": "Uebersicht",
    "Portal": "Uebersicht",
    "Diplomatie": "Uebersicht",
    "Einstellungen": "Uebersicht",
    "Ruhmeshalle": "Uebersicht",
    "Anleitung": "Uebersicht",
    "Kampfsimulator": "Uebersicht",
    "Forum": "Uebersicht",
    "Chat": "Uebersicht",
    "Spieler werben": "Uebersicht",
}


# Anzeigenamen an das Original angleichen (Daniel 30.10.2026: "an das Original angleichen, nur die
# Anzeige"). Schluessel = interner Name (wie in MENU_ITEMS), Wert = Anzeige. Die belegte Liste
# MENU_ITEMS bleibt dadurch unveraendert lesbar.
MENU_ANZEIGE = {
    "Gilde": "Gildenhalle",
    "Kampfsimulator": "Schlachtsimulator",
}

# Punkte, die im Original im Hauptmenue stehen, in MENU_ITEMS aber fehlen (Screenshots
# web_1838856/1838857 + Handbuch Seite 12). Sie kommen als Zusatzpunkte dazu, nie in die Liste.
MENU_ZUSATZ = {"Uebersicht": ["Voraussetzungen", "Neuigkeiten"], "Siedlung": []}


def menu_fuer_ebene(settlements, ebene: str) -> list:
    """Die Leiste EINER Ebene — aufgebaut auf `menu_sichtbar()` (eine Quelle fuer die Freigabe).

    Wer einen Punkt ohne Ebene eintraegt, landet in "Uebersicht" (sichere Voreinstellung:
    die Weltpunkte sind immer da, die Siedlungspunkte brauchen ein Gebaeude).
    """
    punkte = [punkt for punkt in menu_sichtbar(settlements)
              if EBENE_JE_PUNKT.get(punkt, "Uebersicht") == ebene]
    for zusatz in MENU_ZUSATZ.get(ebene, []):
        if zusatz in punkte:
            continue
        # "Voraussetzungen" steht im Original hinter der Ruhmeshalle (Handbuch Seite 12).
        if zusatz == "Voraussetzungen" and "Ruhmeshalle" in punkte:
            punkte.insert(punkte.index("Ruhmeshalle") + 1, zusatz)
        else:
            punkte.append(zusatz)
    return punkte

SKINS = {
    "standard": {
        "bg": "#2a0605",
        "panel": "#3e1c1a",
        "gold": "#FFCC33",
        "red": "#e53935",
        "text": "#FFFF99",
        "topbar": "#1a0a09",
        "sidebar": "#1a0a09",
        "button": "#3e2723",
        "button_active": "#5D4037",
        "border": "#4a1512",
        "headline": "#FFCC33",
        "subhead": "#FF6600",
    },
    "wald": {
        "bg": "#0d1f0d",
        "panel": "#1a2e1a",
        "gold": "#8BC34A",
        "red": "#4CAF50",
        "text": "#E8F5E9",
        "topbar": "#0b1a0b",
        "sidebar": "#0b1a0b",
        "button": "#1b3a1b",
        "button_active": "#2E7D32",
        "border": "#2E7D32",
        "headline": "#8BC34A",
        "subhead": "#4CAF50",
    },
    "feuer": {
        "bg": "#1f0d0d",
        "panel": "#2e1a1a",
        "gold": "#FF5722",
        "red": "#FF9800",
        "text": "#FBE9E7",
        "topbar": "#1a0b0b",
        "sidebar": "#1a0b0b",
        "button": "#3e1a1a",
        "button_active": "#D84315",
        "border": "#D84315",
        "headline": "#FF5722",
        "subhead": "#FF9800",
    },
}


# ---------- Helpers ----------

def research_multiplier(state: "GameState", key: str) -> float:
    """Was eine Forschung im Spiel bewirkt — ueber EINE Stelle (`forschung_wirkung`).

    Die Namen sind die des Originals (data/research.json). Der Handeisbonus und der
    Baukostenrabatt der frueheren erfundenen Gebiete gibt es im Original NICHT — dort steht
    ehrlich 1,0 (kein stiller Bonus mehr).
    """
    levels = {k: v.level for k, v in state.research.items()}
    if key in ("Kriegskunst", "militär"):
        # Der Verteidigungsbonus kommt seit W4b-5 vom BELEGTEN Verteidigungswall auf der
        # Siedlungskarte — vorher hing er am erfundenen Wachturm aus main.BUILDINGS.
        return get_military_multiplier(levels, get_defense_bonus(gebaeude_wirkung.wall_stufe(state.settlements)))
    if key in ("Felderwirtschaft", "Steinbruch", "Forstwirtschaft", "Tierhaltung",
               "Minenarbeit", "Götterkunde", "Heilkunde"):
        return 1.0      # diese Forschungen wirken auf den ERTRAG, siehe ertrag_gesamt/stundenertrag
    return 1.0


# ---------- Game State ----------

class GameState:
    def __init__(self):
        self.resources: Dict[str, Resource] = {r: Resource(r) for r in RESOURCES}
        # Startwerte laut Handbuch Seite 7: 10 Siedler, 100 Holz, 100 Steine.
        # Weitere Rohstoffe nennt das Handbuch nicht — sie starten bei 0.
        self.resources["holz"].amount = 100
        self.resources["stein"].amount = 100
        self.buildings: Dict[str, Building] = {k: Building(**asdict(v)) for k, v in BUILDINGS.items()}
        self.units: Dict[str, Unit] = {k: Unit(**asdict(v)) for k, v in UNITS.items()}
        self.research: Dict[str, Research] = {k: Research(**asdict(v)) for k, v in RESEARCHES.items()}
        self.map_tiles: List[MapTile] = []
        self.bots: List[BotPlayer] = []
        self.current_map = "kontinent"
        self.unlocked_maps: List[str] = ["kontinent"]
        self.active_maps: List[str] = ["kontinent"]
        self.map_switch_cost = 150
        self.population = 10.0   # 10 Siedler laut Handbuch Seite 7
        self.max_population = 10
        self.score = 0
        self.day = 1
        self.last_tick = time.time()  # nur noch Kompatibilitaet/Anzeige
        self._laufzeituhr = zeitbasis.Laufzeituhr()
        # W5: Der Bot-Zug laeuft alle BOT_TAKT_SEKUNDEN. Ohne diesen Startwert waere der
        # Abstand beim ersten Tick riesig (- jetzt - 0) und ALLE Bots haetten sofort gezogen —
        # am Spielanfang, mitten im Noobschutz, mit voller Pluenderung.
        # Seit Schritt 10 Teil 3 ist die Bot-Uhr die SPIELUHR: der Takt zaehlt in
        # Spielsekunden (`spielsekunden` beginnt bei 0), nicht mehr in Rechnerzeit.
        self._letzter_bot_takt = 0.0
        self.ruf = 0
        self.log: List[str] = []
        self.map_garrison: Dict[str, Dict[str, int]] = {}
        self.movements: List[dict] = []
        self.messages: List[dict] = zeitbasis.NachrichtenMitZeit(spieluhr=lambda: self.spielsekunden)
        self.settlements: List[Settlement] = []
        # Ökonomie-Paket, Schritt 9, Teil 5 (Entwurf Z. 777): der feste KARTENVORRAT für
        # Neugründungen (Startkarte + zehn Koloniekarten, data/gelaende.json). Der Vorrat ist
        # Spielzustand — eine vergebene Karte bleibt vergeben — und wird deshalb mitgespeichert.
        # Er wird beim ersten Zugriff angelegt (`kartenvorrat_anlegen`), damit ein ALTER Spielstand
        # ihn nachträglich bekommt, ohne dass sich etwas an seinen Siedlungen ändert.
        self.kartenvorrat: Dict[str, dict] = {}
        self.kartenvorrat_seed: str = ""
        # A2-Vorstufe (03.11.2026): die beim ersten Gruenden gewaehlte Startkarte. Leer heisst
        # "noch nicht gewaehlt" - dann gilt die belegte Standardkarte aus data/startkarte.json.
        self.startkarte_gewaehlt: str = ""
        # A2 (03.11.2026): die Fraktion (das Volk) des Spielers. Leer heisst "noch nicht gewaehlt" -
        # dann behalten die Bots ihre belegte Zuordnung aus `botkern.BOT_FRAKTIONEN`.
        self.spieler_fraktion: str = ""
        # Ökonomie-Paket, Schritt 9, Teil 6b — die EINE Uhr der Orte (Entwurf Z. 592-648):
        # `spielsekunden` ist SPIELZEIT, nicht Rechnerzeit. `main._tick_loop` multipliziert genau
        # einmal mit `spielzeit.faktor()`; alles Ökonomische rechnet nur mit dieser Zahl, damit
        # Ernte, Werkstattwaren und Ausbildungen denselben Zeitbegriff benutzen.
        self.spielsekunden: float = 0.0
        # Ökonomie-Paket, Schritt 9, Teil 6 (Entwurf: „aktive_siedlung_id"): auf WELCHEN Ort sich
        # Lager, Kaserne und Forschung beziehen. Bis Teil 5 lasen diese Ansichten den Reichsbestand
        # — ohne diesen Zeiger könnte keine Ware und keine Einheit je im richtigen Lager landen.
        # Er wird mitgespeichert, zeigt er ins Leere, berichtigt ihn `aktive_siedlung()`.
        self.aktive_siedlung_id: str = ""
        # Sieg/Niederlage (Vorgabe Daniel 05.10.2026, Option A): Sieg bei der Zielpunktzahl,
        # Niederlage ohne Siedlung UND ohne Einheit. Das Handbuch nennt keine Bedingung — die
        # Formeln und die Schwelle stehen in src/punkte.py (dort als VORSCHLAG gekennzeichnet).
        # `hatte_siedlung` verhindert, dass das Spiel VOR der ersten Siedlung als verloren gilt.
        self.hatte_siedlung = False
        self.spielende: Optional[str] = None
        self.noob_protection: bool = True
        # Oekonomie-Paket, Schritt 9, Teil 8b (Entwurf Z. 789): Version und Modus des Spielstands.
        # `stand_version` ist die FORM (1 = der alte, unversionierte Stand — dort fehlt das Feld;
        # 2 = mit Versions- und Modusfeld). `mode` ist bis Schritt 10 ein reiner MERKER: eine NEUE
        # Partie laeuft als `oeokonomie-1`, ein geladener Altstand als `legacy`. Der Oekonomiemodus
        # wird dadurch NICHT aktiviert (Entwurf Z. 1092) und nichts wird umgerechnet.
        self.stand_version: int = STAND_VERSION
        self.mode: str = MODUS_NEU
        # Eigenes Aktivierungsmerkmal, nicht mit "mode" verwechseln: die am
        # 06.10. erstellten Version-2-Staende fuehrten diesen Modus nur als MERKER.
        # Fehlendes Feld im geladenen Stand heisst daher: keine stille Konversion.
        self.oekonomie_aktiv: bool = True
        self.admin_teststand: bool = False  # niemals normaler Spielstand
        self.admin_hilfe_modus: str = "auto"  # FIX04d nur Teststand; keine Kampfwirkung
        self.admin_weltkarten: dict = {}  # Admin-only: Weltkarten jenseits der aktuellen Ansicht
        self.goods: Dict[str, int] = {key: 0 for key in GOODS}
        # W5-2 (Portal, src/portalraum.py): die eigene Weltkarte im Limbus-Raster, die Weltkarten,
        # in denen man schon Fuss gefasst hat, und der Zeitpunkt des letzten Weltensprungs.
        # S-2b (Daniel 01.11.2026, Anhang 3 Frage 22): Startwelt ist MIDGARD, nicht mehr Armageddon.
        # Die Nummer ist 1-basiert wie die Kennung (d04 -> 4) und steht so in data/welten.json.
        _startwelt = welt.startwelt_nummer() or 1
        self.eigene_dimension: int = _startwelt
        self.eigene_dimensionen: List[int] = [_startwelt]
        self.letzter_wechsel: Optional[float] = None
        # W3 (Werkstatt, src/werkstatt.py): das Lager der 17 ORIGINALwaren aus data/items.json
        # (vorher stand hier die erfundene GOODS-Liste mit Emoji) und je Werkstatt eine
        # Warteschlange. Die Warteschlangen entstehen beim ersten Zugriff aus den wirklich
        # gebauten Werkstaetten der Siedlungskarten.
        self.waren: Dict[str, int] = {name: 0 for name in WARE_EINTRAEGE}
        self.werkstaetten: Dict[str, dict] = {}
        # W7 (Auftraege, src/auftraege.py): die laufenden Missionen. Jeder Eintrag kennt Art,
        # Einheiten, Start und Ziel, Reisezeit, Fracht und Status (hinreise/am_ziel/rueckreise/
        # abgeschlossen). Die Einheiten sind ab dem Start unterwegs (siehe auftrag_starten).
        self.auftraege: List[dict] = auftraege.neue_liste()
        # W4c (forschung, src/forschung.py): die LAUFENDE Forschung je Gebiet. Die Stufe bleibt
        # EINE Wahrheit in `self.research[...].level`; hier steht nur der Auftrag
        # {'zielstufe','startzeit','dauer_stunden','kosten'}. Der Stand, mit dem das Modul
        # rechnet, wird bei jedem Aufruf daraus frisch gebaut (keine zweite Wahrheit).
        self.forschungsauftraege: Dict[str, dict] = {}

    # Oekonomie-Paket, Schritt 9, Teil 8 (Entwurf Z. 785): HIER stand `GameState._unlock_next_map`.
    # Es hat die Forschung "Vermessung" abgefragt — die es unter den 21 Originalforschungen NICHT
    # gibt (belegt in tests/test_spieloekonomie.py, Z. 198). Der Zweig konnte deshalb nie
    # ausloesen; die Methode hatte keinen einzigen Aufrufer, und sie benutzte `MAX_ACTIVE_MAPS`,
    # das im ganzen Projekt nirgends definiert ist (bei einem Aufruf waere sie mit `NameError`
    # gestorben). Entwurf Z. 785 woertlich: "Vermessung-Abfrage entfaellt im neuen Siedlungspfad.
    # Kartenangebote sind kein MAPS-Regionsunlock. Alte fuenf Weltregionen nicht als neue
    # Siedlungskarten verkaufen."
    # Was stattdessen gilt: die fuenf Weltregionen (MAPS) sind das ALTE Kartensystem und werden
    # nicht durch eine Forschung geoeffnet; neue Siedlungskarten kommen aus dem KARTENVORRAT
    # (Teil 5: Wagenbau + Siedlerkarren, `_found_settlement`). `unlocked_maps`/`active_maps`
    # werden seither nur noch gelesen und aus einem alten Spielstand uebernommen — niemand
    # schaltet hier etwas frei (Wache: P31 in tests/test_oekonomie_einhaengung.py).

    def destroy_map(self, map_id: str):
        if map_id == "kontinent":
            self._log("Der Kontinent kann nicht zerstört werden.")
            return
        if map_id in self.active_maps:
            self.active_maps.remove(map_id)
        if self.current_map == map_id:
            self.current_map = "kontinent"
            self.generate_map("kontinent")
        self._log(f"Karte {map_id} wurde zerstört.")

    def is_defeated(self) -> bool:
        return self.current_map == "kontinent" and len(self.active_maps) == 0

    def alle_einheiten(self) -> Dict[str, int]:
        """Alle ECHTEN Einheiten des Spielers: anwesend **und** unterwegs, jede genau einmal.

        Ökonomie-Paket, Entwurf Schritt 9 (Z. 786): „Einheiten für Originalpunkte ausschließlich als
        Summe örtlicher und unterwegs befindlicher echter Bestände ableiten; unterwegs nicht nochmals
        als Garnison zählen."

        In diesem Modell ist `self.units` der Bestand **zuhause**; unterwegs befindliche Einheiten
        sind beim Start davon abgezogen und stehen in der Mission. Gezählt wird deshalb der Heimat-
        bestand plus jede Mission, die noch **nicht heimgekehrt** ist (`heimgekehrt`) — beim
        Stationieren setzt `auftraege_fortschreiben` diesen Merker sofort, zurückkehrende Truppen
        bekommen ihre Zahl genau in demselben Aufruf zurück. Damit zählt keine Einheit zweimal und
        keine fällt während der Reise aus der Wertung (vorher sanken die Kriegspunkte, solange die
        Armee unterwegs war).
        """
        gesamt = {k: int(v.count) for k, v in self.units.items()}
        # Ökonomie-Paket, Schritt 9, Teil 4: die Karren eines EIGENEN Transports stehen nach der
        # Heimkehr im ORTSLAGER. Entwurf Z. 786 verlangt die Summe „örtlicher und unterwegs
        # befindlicher echter Bestände" — ohne diese Zeile fielen die Karren aus den Kriegspunkten,
        # sobald ein Transport zurück ist (ihr Lager wäre keine der beiden Quellen mehr).
        for siedlung in self.settlements:
            for name, anzahl in (getattr(siedlung, "einheiten", None) or {}).items():
                gesamt[name] = gesamt.get(name, 0) + int(anzahl)
        for eintrag in self.auftraege:
            if eintrag.get("heimgekehrt"):
                continue
            for name, anzahl in (eintrag.get("einheiten") or {}).items():
                gesamt[name] = gesamt.get(name, 0) + int(anzahl)
        return gesamt

    def wall_stufe_am_ort(self, siedlung: Settlement) -> int:
        """Neue Partie: Ortswall, Legacy: historisches Feldgebaeude (ohne Migration)."""
        if self._lokale_kasse_aktiv():
            return dorfwall.stufe(siedlung, self.research)
        return gebaeude_wirkung.gebaeude_stufe(siedlung, "verteidigungswall")

    def wall_kriegspunkte(self) -> int:
        """Jeder aktivierte Dorfwall zaehlt einzeln nach Handbuch: Stufe hoch drei."""
        if self._lokale_kasse_aktiv():
            return sum(self.wall_stufe_am_ort(s) ** 3 for s in self.settlements)
        # Legacy behält seine alte Berechnung exakt bei.
        return gebaeude_wirkung.wall_stufe(self.settlements) ** 3

    def wall_errichten(self, siedlung: Settlement) -> Tuple[bool, str]:
        """Eine Errichtung pro Dorf mit der bestehenden, atomaren Ortskasse.

        Kosten aus data/baupreise.json sind dokumentierte Remake-Vorschlaege.
        Kein Feld belegt; unzureichende Forschung/Rohstoffe ändern nichts.
        """
        if not self._lokale_kasse_aktiv():
            return False, "Ortswaelle stehen nur im neuen Wirtschaftsmodus zur Verfuegung."
        if siedlung not in self.settlements:
            return False, "Siedlung gehoert nicht zum Reich."
        if siedlung.mauer_besetzt:
            return False, "Wall in diesem Dorf bereits errichtet."
        if dorfwall.forschungsstand(self.research) < 1:
            return False, "Zuerst Verteidigungsanlagen erforschen."
        kosten = baukosten("verteidigungswall")
        if not kosten:
            return False, "Kein Baupreis fuer die Dorfmauer hinterlegt."
        if self.ortsdeckung(siedlung, kosten):
            return False, "Zu wenig Rohstoffe im Dorflager fuer den Wall."
        if not self.admin_teststand:
            risiko = versorgungsschutz.risiko_nach_ausgabe(siedlung, kosten, baukosten)
            if risiko:
                return False, risiko[0]
        ok, meldung = self.verbrauche_am_ort(siedlung, kosten)
        if not ok:
            return False, meldung
        siedlung.mauer_besetzt = True
        siedlung.mauer_zustand = 100.0
        return True, (f"Wall in {siedlung.name} errichtet. "
                      f"Stufe {self.wall_stufe_am_ort(siedlung)}; kein Feld belegt.")

    def punktestand(self) -> dict:
        """Forschungs-, Kriegs- und Gesamtpunkte nach den Originalformeln (Handbuch S. 3/5/6).

        EINE Quelle: src/punkte.py. Vorher rechnete die Oberflaeche an mehreren Stellen eigene
        Summen — so entstand nachweislich eine falsche Gesamtzahl.
        Die Einheiten kommen aus `alle_einheiten()`: anwesende **und** unterwegs befindliche,
        jede genau einmal (Entwurf Z. 786).
        """
        staende = {k: v.level for k, v in self.research.items()}
        einheiten = self.alle_einheiten()
        wall = max((self.wall_stufe_am_ort(s) for s in self.settlements), default=0)
        # Mehrere Mauern nicht als einen einzigen Maximalwall abrechnen.
        forschung = punkte.forschungspunkte(staende)
        krieg = punkte.kriegspunkte(einheiten, 0) + self.wall_kriegspunkte()
        return {
            "staende": staende,
            "einheiten": einheiten,
            "wall_stufe": wall,  # Anzeige/Legacy-Schnittstelle; Punkte stehen separat
            "forschung": forschung,
            "krieg": krieg,
            "gesamt": (forschung + krieg) // 2,
        }

    def spielausgang(self) -> Tuple[str, str]:
        """('niederlage'|'weiter', Begruendung) aus src/punkte.py — es gibt keinen Sieg.

        E5 (Daniel, 31.10.2026): KEIN Sieg. Das Handbuch 2009 nennt keine Siegbedingung
        (Seite 3: jeder Spieler hat seine eigenen Ziele), der frueher hier gerechnete
        "Sieg bei 300 Punkten" ist VERWORFEN. Niederlage nur, wenn keine Siedlung UND
        keine Einheit mehr da ist. Vor der ersten Siedlung laeuft nichts — sonst waere
        die Partie in der ersten Sekunde verloren.
        """
        if not self.hatte_siedlung:
            return ("weiter", "Noch keine Siedlung gegruendet — die Partie hat nicht begonnen.")
        stand = self.punktestand()
        return punkte.spielausgang({
            "siedlungen": list(self.settlements),
            "einheiten": stand["einheiten"],
            "punkte": stand["gesamt"],
        })

    def generate_map(self, map_id: str):
        cfg = next(m for m in MAPS if m["id"] == map_id)
        tiles = []
        size = cfg["size"]
        if cfg.get("sectors"):
            # Continent: generate sectors instead of tiles
            sector_names = [
                "Norden", "Nordost", "Osten", "Südost", "Süden", "Südwest", "Westen", "Nordwest",
                "Mitte-N", "Mitte-O", "Mitte-S", "Mitte-W", "Zentrum"
            ]
            for y in range(size):
                for x in range(size):
                    sector = f"{x}:{y}"
                    terrain = random.choice(["forest", "plains", "mountain", "water", "village", "ruins"])
                    tile = MapTile(x=x, y=y, terrain=terrain)
                    tile.sector = sector
                    tile.sector_name = sector_names[min(len(sector_names)-1, (x + y) % len(sector_names))]
                    if terrain == "forest":
                        tile.resources = {"holz": random.randint(50, 150)}
                    elif terrain == "mountain":
                        tile.resources = {"stein": random.randint(50, 150), "metall": random.randint(20, 80)}
                    elif terrain == "ruins":
                        tile.resources = {"mana": random.randint(50, 160)}
                    elif terrain == "village":
                        tile.resources = {"nahrung": random.randint(40, 120), "gold": random.randint(10, 40)}
                    if random.random() < 0.2:
                        tile.npc_faction = random.choice(cfg["npcs"])
                    if random.random() < 0.15:
                        tile.quest = random.choice(cfg["quests"])
                    tiles.append(tile)
        else:
            for y in range(size):
                for x in range(size):
                    terrain = random.choice(["forest", "plains", "mountain", "water", "village", "ruins"])
                    tile = MapTile(x=x, y=y, terrain=terrain)
                    if terrain == "forest":
                        tile.resources = {"holz": random.randint(30, 90)}
                    elif terrain == "mountain":
                        tile.resources = {"stein": random.randint(30, 90), "metall": random.randint(5, 30)}
                    elif terrain == "ruins":
                        tile.resources = {"mana": random.randint(15, 60)}
                    if random.random() < 0.15:
                        tile.npc_faction = random.choice(cfg["npcs"])
                    if random.random() < 0.1:
                        tile.quest = random.choice(cfg["quests"])
                    tiles.append(tile)
        self.map_tiles = tiles
        # Bots bekommen echte Siedlungen + Armee, sonst laufen Bot-Angriffe ins Leere
        active_bots = [b for b in BOTS if random.random() < 0.6]
        if not active_bots:
            active_bots = [BOTS[1]]
        bots = []
        for b in active_bots:
            d = asdict(b)
            n_sett = random.randint(1, 3)
            d["settlements"] = [f"{b.name}s Siedlung {i+1}" for i in range(n_sett)]
            # W5 (botkern): KEINE erfundene Armee mehr. Hier stand `random.randint(20, 120)` JE
            # EINHEIT — damit war jeder Bot-Angriff aussichtslos. Der Bot legt jetzt Vorräte und
            # Wagenpark an und stellt seine Einheiten daraus nach den BELEGTEN Preisen auf.
            d["army"] = {}
            d["ruf"] = random.randint(0, 60)
            bots.append(BotPlayer(**d))
        self.bots = bots
        for b in self.bots:
            self.bot_vorrat_anlegen(b)
            bot_doerfer_sicherstellen(b)          # B-1: je Bot ein Dorf-Datensatz (Hauptdorf aus den Namen)

    def bot_doerfer_auffrischen(self, bot: BotPlayer, jetzt: float, spieler_ort=None) -> int:
        """Positionen einmalig setzen und je Dorf die Taktik aus der Lage waehlen (B-2, 02.11.2026).

        Die Wahl faellt NICHT durch Nachdenken: `bottaktik.dorf_taktik_setzen` rechnet aus vier
        Lagen (Naehe zum Spieler, Staerkeverhaeltnis, Wallzustand, letzte Niederlage) einen
        Punktwert je Verhalten und haelt die Sperrzeit ein. Rueckgabe: Zahl der Doerfer, deren
        Verhalten sich geaendert hat (0 = nichts Neues).

        Die Lage wird aus vorhandenen Werten gebildet, nichts erfunden:
          naehe      - Abstand Mannhattan in Feldern zur aktiven Siedlung des Spielers (Karte 20x20)
          staerke    - eigene Truppenzahl gegen die Truppen des Spielers
          wall       - Wallzustand des Dorfes (100 = heil, 0 = gebrochen)
          niederlage - ein Beuteverlust im Gedaechtnis (juenger als 24 h) gilt als Niederlage
        """
        doerfer = bot_doerfer_sicherstellen(bot)                       # alte Spielstaende nachziehen
        for i, dorf in enumerate(doerfer):                             # Positionen einmalig setzen
            if int(dorf.x) == 0 and int(dorf.y) == 0:                  # 0/0 = noch nicht gesetzt
                dorf.x, dorf.y = bottaktik.dorf_position(bot.name, i)   # fest aus Name und Nummer
        bot_doerfer_karten_zuweisen(bot)                               # B-4: je Dorf eine Karte (drei zur Wahl, Gold zuerst)
        # S-4 (03.11.2026): der Bot FORSCHT - zuerst faellige Auftraege verbuchen, dann den
        # naechsten Schritt seiner Taktik starten (eine Bibliothek je Dorf, ein Auftrag je Takt).
        # Steht VOR dem Bauen, damit ein Dorf, dessen Baukunst heute fertig wird, sie im selben
        # Takt schon nutzen kann (Wall, Lager, Schmiede).
        plan_forschung = bot_forschungsplan()                          # einmal lesen, alle Doerfer nutzen ihn
        for dorf in doerfer:                                           # je Dorf eine Bibliothek
            bot_dorf_forschung_abschluss(dorf, bot, jetzt)             # Stufe steigt genau einmal
            bot_dorf_forschen(dorf, bot, jetzt, plan_forschung)        # EINE Kernfunktion (forschung_start)
        # S-3 (03.11.2026): der Bot BAUT - durch dieselbe Funktion wie der Spieler, aus seinem
        # eigenen Dorflager. Ein Gebaeude je Dorf und Takt (`bauten_je_takt` in der Datendatei),
        # Reihenfolge aus dem Stil der Taktik.
        plan = bot_bauplan()                                           # einmal lesen, alle Doerfer nutzen ihn
        for dorf in doerfer:                                           # je Dorf ein Bauplatz
            gebaut = bot_dorf_bauen(dorf, bot, jetzt, plan)             # EINE Kernfunktion (spielschicht.bauen)
            if gebaut:                                                 # wirklich etwas entstanden?
                dorf.gebaut = int(getattr(dorf, "gebaut", 0) or 0) + len(gebaut)   # Zaehler am Dorf
        eigene = float(sum(int(v) for v in (bot.army or {}).values()))  # Truppen des Bots
        fremde = float(sum(int(v) for s in self.settlements                 # Truppen des Spielers
                           for v in (getattr(s, "units", None) or {}).values()))
        gesamt = eigene + fremde                                       # Bezugsgroesse des Verhaeltnisses
        staerke = 0.0 if gesamt <= 0 else max(-1.0, min(1.0, (eigene - fremde) / gesamt))
        gedaechtnis = bot.gedaechtnis or {}                            # Gedaechtnis des Bots
        verlust = gedaechtnis.get("beute_verloren") if isinstance(gedaechtnis, dict) else None
        niederlage = 0.0
        if isinstance(verlust, dict) and jetzt - float(verlust.get("zeit") or 0.0) < 24 * 3600:
            niederlage = 1.0                                           # gerade verloren = raecht sich eher
        geaendert = 0                                                  # Zaehler fuer den Aufrufer
        for i, dorf in enumerate(doerfer):                             # je Dorf eine eigene Wahl
            lage = {"staerke": staerke, "niederlage": niederlage,     # gleiche Lage fuer alle Doerfer
                    "wall": max(-1.0, min(1.0, float(dorf.wall_zustand) / 50.0 - 1.0))}
            if spieler_ort is not None:                                # Naehe nur mit bekanntem Ort
                abstand = abs(int(dorf.x) - int(spieler_ort.x)) + abs(int(dorf.y) - int(spieler_ort.y))
                lage["naehe"] = max(-1.0, min(1.0, 1.0 - abstand / 20.0))   # 0 Felder = +1, 20 Felder = -1
            daten = asdict(dorf)                                       # dict-Form fuer den Kern
            zufall = random.Random("dorf:%s:%d:wahl" % (bot.name, i))   # Gleichstand reproduzierbar aufloesen
            if bottaktik.dorf_taktik_setzen(daten, jetzt, lage, zufall):     # Sperrzeit beachtet der Kern
                dorf.taktik = str(daten.get("taktik") or "")           # gewaehltes Verhalten uebernehmen
                dorf.taktik_seit = float(daten.get("taktik_seit") or 0.0)
                geaendert += 1                                         # Wechsel zaehlen
        return geaendert

    def bot_doerfer_uebersicht(self, bot: BotPlayer) -> list:
        """Was der Spieler ohne Spionage sieht - die Grenze steht hier, nicht in der Anzeige.

        VORGABE Daniel 02.11.2026: offen sichtbar sind Position, Schild, Fraktion, Name und die
        BEKANNTEN Standardwerte des Volkes (Kontextfenster beim Ueberfahren des Feldes). Alles an
        KAMPFDATEN - Wallstufe, Wallzustand, aktive Taktik, stationierte Truppen, Vorraete - sieht
        der Spieler NUR ueber einen Spionagebericht (eigene Stufe, noch nicht gebaut). Deshalb
        stehen diese Felder hier ausdruecklich NICHT drin.
        """
        werte = bottaktik.volksattribute({"fraktion": bot.faction})    # die bekannten Volkswerte
        return [{"name": d.name, "x": int(d.x), "y": int(d.y), "hauptdorf": bool(d.hauptdorf),
                 "fraktion": str(bot.faction), "volk_plus": str(werte.get("plus") or ""),
                 "volk_minus": str(werte.get("minus") or "")}
                for d in bot_doerfer_sicherstellen(bot)]               # je Dorf eine Zeile

    def bot_doerfer_spionagebericht(self, bot: BotPlayer) -> dict:
        """Der INHALT eines Spionageberichts - alles, was der Spieler sonst nicht wissen darf.

        VORGABE Daniel 02.11.2026 (Vorbild Lords Mobile): erst ein Spionageangriff bringt Wallstufe,
        Wallzustand, die aktive Taktik, stationierte Truppen und Vorraete ins Postfach. Diese
        Funktion liefert die Zahlen fuer ALLE Doerfer eines Bots; wie viel davon in der Nachricht
        sichtbar wird, entscheidet `spionage.bericht_zeilen` anhand des Aufklaerungswerts.
        """
        einstellungen = bot_wirtschaft_einstellungen()                 # Schalter und Teiler EINMAL lesen
        doerfer = [bot_dorf_bericht_teil(d, bot, einstellungen)         # EINE Stelle je Dorf (F-04)
                   for d in bot_doerfer_sicherstellen(bot)]            # je Dorf ein Berichtsteil
        return {"bot": str(bot.name), "fraktion": str(bot.faction), "doerfer": doerfer,
                "kasse": bot_kasse(bot)}                               # Summe der Doerfer, keine zweite Kasse

    def bot_dorf_spionagebericht(self, bot: BotPlayer, dorf_name: str = "",
                                 jetzt: Optional[float] = None) -> dict:
        """Der Spionagebericht EINES Dorfes - Eingabe fuer `spionage.bericht_nachricht`.

        Ohne `dorf_name` gilt das Hauptdorf (das erste Dorf, B-1). `jetzt` ist die SPIELZEIT der
        Ankunft; sie wandert als `zeit_spielsekunden` in den Bericht, damit `spionage.veraltet`
        spaeter messen kann, wie alt er ist. Ein unbekannter Dorfname liefert `dorf` = {} - der
        Aufrufer meldet das, statt einen Bericht zu erfinden.
        """
        teil = None                                                    # der gesuchte Dorfteil
        for d in bot_doerfer_sicherstellen(bot):                       # je Dorf pruefen
            if not dorf_name or str(d.name) == str(dorf_name):         # Name passt (oder Hauptdorf)
                teil = bot_dorf_bericht_teil(d, bot)                   # diesen Teil bauen
                break                                                  # erster Treffer gilt
        return {"bot": str(bot.name), "fraktion": str(bot.faction),
                "dorf": teil or {},                                    # {} = Dorf nicht gefunden
                "kasse": bot_kasse(bot),                               # Summe der Doerfer
                "zeit_spielsekunden": float(jetzt if jetzt is not None else self.spielsekunden)}

    def spionage_starten(self, bot: BotPlayer, dorf_name: str = "",
                         anzahl: Optional[int] = None,
                         truppen: Optional[dict] = None) -> tuple:
        """Einen Spionageauftrag zu EINEM Bot-Dorf entsenden (Stufe B-5, 02.11.2026).

        Quelle ist das ORTSHEER der aktiven Siedlung: es reisen die KUNDSCHAFTER (Diebesgilde) -
        Spionage ist eine Sache der Einheiten, nicht der Kaempfer (Vorgabe Daniel 02.11.2026).
        `anzahl` ist die Zahl je Spionageart, ohne Angabe gilt `data/spionage.json`
        (`kundschafter_anzahl`). Die Entfernung ist der Abstand der beiden Dorfpositionen im
        Raster; Wallstufe und -zustand gehen als ZIELANGABE mit, damit der Kern beim Absenden
        warnen und bei der Ankunft entscheiden kann (Analogie zur Wall-Vorrunde).
        Rueckgabe (ok, Meldung) - der Bericht selbst kommt erst bei Ankunft ins Postfach.
        """
        e = spionage.einstellungen()                                   # Schalter aus der Datendatei
        if not e.get("aktiv", True):                                   # Spionage abgeschaltet
            return False, "Spionage ist in data/spionage.json abgeschaltet."
        doerfer = bot_doerfer_sicherstellen(bot)                       # Doerfer des Bots, ggf. angelegt
        dorf = next((d for d in doerfer if not dorf_name or str(d.name) == str(dorf_name)), None)
        if dorf is None:                                               # Dorf gibt es nicht
            return False, "Dieses Dorf gehoert nicht zu %s." % bot.name
        ort = self.aktive_siedlung()                                   # Startort des Auftrags
        if ort is None:                                                # ohne Siedlung kein Auftrag
            return False, "Ohne eigene Siedlung kann niemand ausspioniert werden."
        vorrat = self._ortsheer(ort) if hasattr(self, "_ortsheer") else dict(ort.einheiten or {})
        kundschafter = {n: int(a) for n, a in vorrat.items()           # nur Spionageeinheiten
                        if einheiten.ist_kundschafter(n) and int(a) > 0}
        if not kundschafter:                                           # keine Kundschafter im Ort
            return False, ("Keine Kundschafter in %s - Spionage braucht die Einheiten der "
                           "Diebesgilde (Streuner, Gauner, Dieb, Meisterdieb, Kundschafter, "
                           "Waldlaeufer)." % ort.name)
        try:                                                           # Anzahl aus der Datendatei
            je_art = max(1, int(e.get("kundschafter_anzahl") or 1))
        except (TypeError, ValueError):                                # kaputter Wert
            je_art = 1                                                 # dann eine Einheit
        if anzahl is not None:                                         # Aufrufer hat eine Zahl genannt
            try:                                                       # sie muss brauchbar sein
                je_art = max(1, int(anzahl))
            except (TypeError, ValueError):                            # kaputte Angabe
                je_art = 1                                             # dann die Vorgabe
        if truppen is not None:                                        # B-5: Auswahl aus dem Fenster
            gewaehlt = {str(n): int(a) for n, a in dict(truppen).items() if int(a) > 0}   # nur > 0
            if not gewaehlt:                                           # leere Auswahl
                return False, "Keine Einheiten ausgewaehlt."
            if any(n not in kundschafter for n in gewaehlt):           # etwas ist keine Spionageeinheit
                return False, ("In der Auswahl steht eine Einheit, die keine Spionageeinheit ist - "
                               "Spionage geht nur mit Kundschaftern der Diebesgilde.")
            if any(gewaehlt[n] > kundschafter[n] for n in gewaehlt):    # mehr als im Dorf steht
                return False, "So viele Einheiten stehen nicht im Dorf."
            einsatz = gewaehlt                                        # die Auswahl gilt
        else:                                                          # ohne Auswahl die Vorgabe
            einsatz = {n: min(int(a), je_art) for n, a in kundschafter.items()}   # je Art hoechstens je_art
        entfernung = float(max(1, abs(int(ort.x) - int(dorf.x)) + abs(int(ort.y) - int(dorf.y))))
        ziel = {"name": str(dorf.name), "fremd": True,                 # fremdes Dorf - kein Bericht ueber eigene
                "bot_name": str(bot.name), "dorf_name": str(dorf.name),
                "wall_stufe": int(dorf.wall_stufe),                    # Zielangabe fuer die Warnung
                "wall_zustand_prozent": float(dorf.wall_zustand)}
        ok, meldung = self.auftrag_starten("spionieren", einsatz, str(ort.name), ziel, entfernung,
                                           quelle_id=str(getattr(ort, "id", "") or ""))
        return ok, meldung

    def bot_doerfer_auffrischen_alle(self, jetzt: float) -> int:
        """Alle Bots in einem Zug auffrischen (Positionen und Dorf-Taktiken)."""
        spieler_ort = self.aktive_siedlung()                          # Bezugspunkt der Naehe
        return sum(self.bot_doerfer_auffrischen(b, jetzt, spieler_ort) for b in self.bots)

    def get_tile(self, x: int, y: int, size: int) -> Optional[MapTile]:
        if 0 <= x < size and 0 <= y < size:
            return self.map_tiles[y * size + x]
        return None

    def stundenertrag(self) -> dict:
        """
        Stuendlicher Rohstoffertrag aus allen Siedlungskarten (Handbuch: Ertrag je Geländeart).

        EINE Quelle für Rechnung UND Anzeige. Die früheren festen Stufenerträge der Gebaeude sind
        entfallen: sie haetten denselben Rohstoff ein zweites Mal erzeugt.

        Das Wirtschaftsmodul liefert seine Kennungen in Lesefassung ("Holz"); hier werden sie auf
        die Schreibweise der Spieldaten gebracht ("holz"), sonst findet der Zeitlauf sie nicht.
        """
        levels = {k: v.level for k, v in self.research.items()}
        roh = wirtschaft.ertrag_gesamt(self.settlements, levels)
        return {k.lower(): v for k, v in roh.items()}

    # ------------- Oekonomie-Paket Schritt 9, Teil 3: die LOKALEN Lager -------------

    def ertrag_je_ort(self, siedlung: Settlement) -> Dict[str, float]:
        """Stundenertrag EINER Siedlung (Kennungen klein - dieselbe Schreibweise wie `tick`)."""
        levels = {k: v.level for k, v in self.research.items()}
        roh = wirtschaft.ertrag_gesamt([siedlung], levels)
        return {k.lower(): float(v) for k, v in roh.items()}

    def aktive_siedlung(self) -> Optional[Settlement]:
        """Die Siedlung, auf die sich Lager, Kaserne und Forschung BEZIEHEN (Teil 6).

        Der Zeiger `aktive_siedlung_id` ist UI-Zustand. Zeigt er ins Leere — frischer Stand, ein
        Spielstand von vor Teil 6, eine inzwischen umbenannte oder fehlende Siedlung —, wird auf die
        ERSTE Siedlung zurückgefallen **und der Zeiger dabei berichtigt**: sonst liefe die nächste
        Buchung wieder ins falsche Lager. Ohne Siedlungen liefert die Hilfe `None`.
        """
        for s in self.settlements:
            if s.id == self.aktive_siedlung_id:
                return s
        if self.settlements:
            self.aktive_siedlung_id = self.settlements[0].id
            return self.settlements[0]
        return None

    def ortslager(self) -> Dict[str, float]:
        """Die Summe der LOKALEN Lager aller eigenen Siedlungen (ohne den Übergangsbestand)."""
        summen: Dict[str, float] = {}
        for s in self.settlements:
            for r, v in (s.vorraete or {}).items():
                summen[r] = round(summen.get(r, 0.0) + float(v), 2)
        return summen

    # ---------------- EINE Einsatzregel: das ORTSHEER ist die Quelle (F-01/F-09/F-10) ----------

    def _siedlung_zu(self, kennung) -> Optional[Settlement]:
        """Die eigene Siedlung mit dieser Kennung - oder ``None``.

        F-09 der externen Spielpruefung (31.10.2026): ein Auftrag muss seine Quelle als
        **Kennung** tragen, nicht als Name und schon gar nicht als feste Position
        (`settlements[0]`). Eine unbekannte Kennung liefert bewusst ``None`` und wird NICHT
        stillschweigend durch eine andere Siedlung ersetzt.
        """
        if not kennung:
            return None
        return next((s for s in self.settlements if s.id == kennung), None)

    def _ortsheer(self, siedlung) -> Dict[str, int]:
        """Das Heer EINER Siedlung als ``{Einheit: Anzahl}`` (nur positive Eintraege)."""
        if siedlung is None:
            return {}
        return {str(k): int(v) for k, v in (getattr(siedlung, "einheiten", None) or {}).items()
                if int(v) > 0}

    def einsatz_ausheben(self, siedlung, truppen: dict) -> Dict[str, int]:
        """Nimmt ``truppen`` aus dem ORTSHEER einer Siedlung. Liefert, was wirklich mitkam.

        Eine Stelle fuer jeden Einsatz (Reiseauftrag UND Sofortangriff): frueher nahm der
        Auftragsweg die Truppen aus `self.units`, der Sofortangriff buchte gar nichts ab
        (F-01/F-10). Gebucht wird nur, was im Ortslager liegt - kein Heer aus dem Nichts.

        Ohne Siedlung (alter Spielstand) nimmt dieselbe Funktion aus dem Reichsbestand - damit
        Abgang und Heimkehr auch dort symmetrisch bleiben.
        """
        mit = {}
        for name, anzahl in (truppen or {}).items():
            name, anzahl = str(name), max(0, int(anzahl))
            if anzahl <= 0:
                continue
            if siedlung is None:
                if name not in self.units:
                    continue
                weg = min(max(0, int(self.units[name].count)), anzahl)
                if weg <= 0:
                    continue
                self.units[name].count = int(self.units[name].count) - weg
                mit[name] = mit.get(name, 0) + weg
                continue
            haben = int((siedlung.einheiten or {}).get(name, 0))
            weg = min(haben, anzahl)
            if weg <= 0:
                continue
            rest = haben - weg
            if rest > 0:
                siedlung.einheiten[name] = rest
            else:
                siedlung.einheiten.pop(name, None)
            mit[name] = mit.get(name, 0) + weg
        return mit

    def einsatz_zurueck(self, quelle_id, truppen: dict) -> Dict[str, int]:
        """Bucht Heimkehrer in das Ortslager IHRER Siedlung (``quelle_id``). Liefert die Summe.

        Ohne Siedlung (alter Spielstand) geht es wie bisher in den Reichsbestand - aber nur
        dann; eine vorhandene Quelle bestimmt den Zielort allein.
        """
        siedlung = self._siedlung_zu(quelle_id)
        zurueck = {}
        for name, anzahl in (truppen or {}).items():
            name, anzahl = str(name), int(anzahl)
            if anzahl <= 0:
                continue
            if siedlung is not None:
                siedlung.einheiten[name] = int((siedlung.einheiten or {}).get(name, 0)) + anzahl
            elif name in self.units:
                self.units[name].count = int(self.units[name].count) + anzahl
            else:
                continue
            zurueck[name] = anzahl
        self._reichsanzeige_aus_orten()
        return zurueck

    def beute_gutschreiben(self, siedlung, beute: dict) -> Dict[str, float]:
        """Schreibt erbeutete Gueter in das Ortslager des HEIMKEHRENDEN Ortes.

        Dieselbe Regel wie beim eigenen Transport: hereinkommende Ware landet in dem Dorf, das
        sie geholt hat - nicht in einer abgeleiteten Reichsanzeige. Ohne Siedlung bleibt der alte
        Weg (Reichsbestand), damit alte Spielstaende nichts verlieren.
        """
        gebucht: Dict[str, float] = {}
        for stoff, menge in (beute or {}).items():
            betrag = float(menge or 0.0)
            if betrag <= 0:
                continue
            if siedlung is not None:
                siedlung.vorraete[stoff] = round(float(siedlung.vorraete.get(stoff, 0.0)) + betrag, 2)
            elif stoff in self.resources:
                self.resources[stoff].amount = round(float(self.resources[stoff].amount) + betrag, 2)
            else:
                continue
            gebucht[stoff] = betrag
        if siedlung is not None:
            self._reichsanzeige_aus_orten()
        return gebucht

    def _lokale_kasse_aktiv(self) -> bool:
        """Neue Partien: Orte sind die einzigen physischen Bestandsquellen.

        Bei unversionierten Legacy-Staenden bleibt die bisherige Uebergangs-
        behandlung erhalten. Die Migration alter Saves ist eine separate Arbeit.
        """
        return (self.mode == MODUS_NEU and bool(self.oekonomie_aktiv)
                and bool(self.settlements))

    def _reichsanzeige_aus_orten(self) -> None:
        """Reichswerte sind NUR eine Summe, niemals eine zweite Kasse."""
        if not self._lokale_kasse_aktiv():
            return
        summen = self.ortslager()
        for name, eintrag in self.resources.items():
            eintrag.amount = round(float(summen.get(name, 0.0)), 2)
        self.population = round(sum(float(s.bevoelkerung)
                                    for s in self.settlements), 4)

    def ortsdeckung(self, siedlung: Settlement, kosten: dict) -> Dict[str, float]:
        """Was FEHLT, wenn auch der Reichsbestand mitzahlen darf. Leer = gedeckt.

        Geprüft wird gegen die zwei Quellen, aus denen `verbrauche_am_ort` wirklich zahlt: das
        LOKALE Lager des Ortes und den Reichsbestand (Übergang). So wird nie halb gebucht.
        """
        fehlt: Dict[str, float] = {}
        for r, v in (kosten or {}).items():
            if r == "siedler":
                haben = float(siedlung.bevoelkerung)
                if not self._lokale_kasse_aktiv():
                    haben += float(self.population)
            else:
                haben = float(siedlung.vorraete.get(r, 0.0))
                if not self._lokale_kasse_aktiv() and r in self.resources:
                    haben += float(self.resources[r].amount)
            if haben + 1e-9 < float(v):
                fehlt[r] = round(float(v) - haben, 2)
        return fehlt

    def verbrauche_am_ort(self, siedlung: Settlement, kosten: dict) -> Tuple[bool, str]:
        """Kosten aus dem LOKALEN Lager EINES Ortes bezahlen. Liefert ``(ok, Meldung)``.

        Ökonomie-Paket, Schritt 9, Teil 3 (Entwurf Z. 779-780: „Kosten aus BP gegen gewählten Ort
        prüfen; mittels verbrauchen buchen; Siedler aus dessen bevoelkerung"). Führend ist das
        lokale Lager des Ortes; erst wenn es nicht reicht, zahlt der **Reichsbestand** dazu.
        Gebucht wird ausschließlich nach erfolgreicher Vorprüfung — eine Ablehnung ändert NICHTS.

        ÜBERGANG, ehrlich benannt (Entwurf Z. 787): alte Spielstände tragen ihre Rohstoffe noch im
        Reichsbestand (`GameState.resources`). Bis auch sie in Ortslagern führen, ist der
        Reichsbestand die zweite Kasse — gezogen wird nur der fehlende Betrag, nie mehr. Die
        Zielform („Globale resources … im Neumodus aus Anzeigen ableiten") erreicht der spätere
        Teil, indem dieser Zuschuss entfällt.
        """
        fehlt = self.ortsdeckung(siedlung, kosten)
        if fehlt:
            return False, "es fehlt " + ", ".join(f"{r} ({w:.2f})" for r, w in sorted(fehlt.items()))
        for stoff, menge in (kosten or {}).items():
            if stoff == "siedler":
                aus_ort = min(float(siedlung.bevoelkerung), float(menge))
                siedlung.bevoelkerung = float(siedlung.bevoelkerung) - aus_ort
                rest = float(menge) - aus_ort
                if rest > 0 and not self._lokale_kasse_aktiv():
                    self.population = max(0.0, float(self.population) - rest)
                continue
            aus_ort = min(float(siedlung.vorraete.get(stoff, 0.0)), float(menge))
            siedlung.vorraete[stoff] = round(float(siedlung.vorraete.get(stoff, 0.0)) - aus_ort, 2)
            rest = float(menge) - aus_ort
            if rest > 0 and not self._lokale_kasse_aktiv() and stoff in self.resources:
                self.resources[stoff].amount = round(float(self.resources[stoff].amount) - rest, 2)
        self._reichsanzeige_aus_orten()
        return True, ""

    def reichsdeckung(self, kosten: dict) -> Dict[str, float]:
        """Was FEHLT, wenn das GANZE Reich zahlt (alle Ortslager + Reichsbestand). Leer = gedeckt.

        Für **globale** Aktionen, die zu keiner einzelnen Siedlung gehören (z. B. der Kartenwechsel
        auf der Weltkarte, Handbuch S. 19).
        """
        fehlt: Dict[str, float] = {}
        for r, v in (kosten or {}).items():
            if r == "siedler":
                haben = sum(float(s.bevoelkerung) for s in self.settlements)
                if not self._lokale_kasse_aktiv():
                    haben += float(self.population)
            else:
                haben = sum(float(s.vorraete.get(r, 0.0)) for s in self.settlements)
                if not self._lokale_kasse_aktiv() and r in self.resources:
                    haben += float(self.resources[r].amount)
            if haben + 1e-9 < float(v):
                fehlt[r] = round(float(v) - haben, 2)
        return fehlt

    def verbrauche_reichsweit(self, kosten: dict) -> Tuple[bool, str]:
        """Kosten für eine GLOBALE Aktion aus dem ganzen Reich bezahlen. ``(ok, Meldung)``.

        Erst der Reichsbestand, dann die Ortslager (nach Kennung, damit es wiederholbar bleibt).
        Nach erfolgreicher Vorprüfung; eine Ablehnung ändert nichts.
        """
        fehlt = self.reichsdeckung(kosten)
        if fehlt:
            return False, "es fehlt " + ", ".join(f"{r} ({w:.2f})" for r, w in sorted(fehlt.items()))
        for stoff, menge in (kosten or {}).items():
            rest = float(menge)
            if stoff == "siedler":
                if not self._lokale_kasse_aktiv():
                    nimm = min(rest, float(self.population))
                    self.population = max(0.0, float(self.population) - nimm)
                    rest -= nimm
                for s in sorted(self.settlements, key=lambda x: x.id):
                    if rest <= 1e-9:
                        break
                    nimm = min(rest, float(s.bevoelkerung))
                    s.bevoelkerung = float(s.bevoelkerung) - nimm
                    rest -= nimm
                continue
            if not self._lokale_kasse_aktiv() and stoff in self.resources:
                nimm = min(rest, float(self.resources[stoff].amount))
                self.resources[stoff].amount = round(float(self.resources[stoff].amount) - nimm, 2)
                rest -= nimm
            for s in sorted(self.settlements, key=lambda x: x.id):
                if rest <= 1e-9:
                    break
                nimm = min(rest, float(s.vorraete.get(stoff, 0.0)))
                s.vorraete[stoff] = round(float(s.vorraete.get(stoff, 0.0)) - nimm, 2)
                rest -= nimm
        self._reichsanzeige_aus_orten()
        return True, ""

    def reich_abzug(self, stoff: str, menge: float) -> float:
        """Eine Abgabe (z. B. Bot-Beute) trifft Reichsbestand UND Ortslager anteilig (Übergang).

        Der Reichsbestand ist die Gesamtsicht aus Übergangsrest und Ortslagern; eine Abgabe, die
        nur ihn trifft, würde die Bücher auseinanderlaufen lassen. Sie nimmt denselben Anteil aus
        den Ortslagern - nie negativ, nie mehr als vorhanden.
        """
        menge = float(menge)
        if menge <= 0:
            return 0.0
        if not self._lokale_kasse_aktiv() and stoff in self.resources:
            self.resources[stoff].amount = max(
                0.0, round(float(self.resources[stoff].amount) - menge, 2))
        verfuegbar = sum(float(s.vorraete.get(stoff, 0.0)) for s in self.settlements)
        if verfuegbar <= 0:
            return menge
        anteil = min(1.0, menge / verfuegbar)
        for s in self.settlements:
            vorher = float(s.vorraete.get(stoff, 0.0))
            s.vorraete[stoff] = round(vorher - vorher * anteil, 2)
        self._reichsanzeige_aus_orten()
        return min(menge, verfuegbar) if self._lokale_kasse_aktiv() else menge

    # ---------------- Ökonomie-Paket, Schritt 9, Teil 4: der EIGENE Transport ----------------
    # Entwurf Z. 779: „_transport_to_settlement: Herkunft separat wählen; Rohstoff/Menge/Karren
    # abfragen; transport_start(asdict(Quelle),asdict(Ziel),…) ausführen, Ergebnis mit
    # Settlement(**neu) ersetzen; mission anhängen. Vorherige Methode mit festem 10 Holz
    # vollständig ersetzen." Der Kern ist `src/spieloekonomie.py` — hier wird nur der Spielstand
    # getauscht und die Auftragsschleife angebunden.

    def _ort_uebernehmen(self, kennung: str, daten: dict) -> bool:
        """Den Stand EINES Ortes aus dem Kern übernehmen (Entwurf: „Settlement(**neu)").

        Der Gegenstand bleibt derselbe: die Oberfläche hält Verweise auf die Siedlung (z. B. die
        geöffnete Siedlungskarte), und ein Austausch in der Liste würde sie still auf einen alten
        Stand zeigen lassen. Übernommen werden ALLE Felder des frischen Standes — und nur dann,
        wenn sich wirklich etwas geändert hat (sonst schreibt jeder Takt alle Orte neu).
        """
        try:
            frisch = Settlement(**daten)
        except TypeError:
            return False
        for siedlung in self.settlements:
            if siedlung.id == kennung:
                if siedlung.__dict__ != frisch.__dict__:
                    siedlung.__dict__.clear()
                    siedlung.__dict__.update(frisch.__dict__)
                    self._reichsanzeige_aus_orten()
                return True
        return False

    def transport_karren_bestand(self, quelle: Settlement) -> Dict[str, int]:
        """Welche Karren für einen Transport von ``quelle`` bereitstehen (Ort zuerst, dann Reich).

        Reine Auswahlhilfe für die Oberfläche: das ORTSLAGER ist führend (Teil 3a), der
        Reichsbestand zählt als Übergang dazu — dieselbe Reihenfolge, in der `transport_an_ort`
        die Truppe wirklich nimmt.
        """
        bestand: Dict[str, int] = {}
        for name, anzahl in (getattr(quelle, "einheiten", None) or {}).items():
            if einheiten.ist_transport(name) and int(anzahl) > 0:
                bestand[name] = int(bestand.get(name, 0)) + int(anzahl)
        if not self._lokale_kasse_aktiv():
            for name, einheit in self.units.items():
                if einheiten.ist_transport(name) and int(einheit.count) > 0:
                    bestand[name] = int(bestand.get(name, 0)) + int(einheit.count)
        return bestand

    def transport_an_ort(self, quelle: Settlement, ziel: Settlement, rohstoff: str, menge,
                         karren: dict, jetzt: float = None) -> Tuple[bool, str]:
        """Einen EIGENEN Transport zwischen zwei Siedlungen starten. Liefert ``(ok, Meldung)``.

        Geprüft und gebucht wird ausschließlich im KERN (`spieloekonomie.transport_start`); hier
        wird nur der Spielstand getauscht (`_ort_uebernehmen`) und die Mission angehängt. Die
        Fracht kommt aus dem **Ortslager des Ausgangsortes** — das ist seit Teil 3a der führende
        Bestand. Reicht der Ort an Karren nicht, kommt der fehlende Teil als **Übergang** aus dem
        Reichsheer (dieselbe Übergangskasse wie beim Bezahlen). Abgelehnt wird VOR jeder Änderung.
        """
        jetzt = float(self.spielsekunden) if jetzt is None else float(jetzt)
        if quelle is None or ziel is None:
            return False, "Herkunft und Ziel müssen gewählt sein."
        if quelle is ziel or quelle.id == ziel.id:
            return False, "Herkunft und Ziel sind dieselbe Siedlung."
        if quelle.map_id != self.current_map or ziel.map_id != self.current_map:
            return False, "Transporte gehen nur innerhalb der gewählten Karte."
        try:
            menge = int(menge)
        except (TypeError, ValueError):
            return False, "Die Menge muss eine ganze Zahl sein."
        if menge <= 0:
            return False, "Die Menge muss größer als 0 sein."
        stoff = str(rohstoff or "").lower()
        if stoff not in self.resources:
            return False, f"Unbekannter Rohstoff '{rohstoff}'."
        karren = {str(n): int(k) for n, k in (karren or {}).items() if int(k) > 0}
        if not karren:
            return False, ("Für einen Transport wird mindestens ein Karren gebraucht "
                           "(Handbuch S. 23).")
        kein_karren = [n for n in karren if not einheiten.ist_transport(n)]
        if kein_karren:
            return False, ("Kein Transportmittel: " + ", ".join(sorted(kein_karren))
                           + " — tragen kann nur ein Karren (Handbuch S. 23).")
        ladung = int(auftraege.ladung_der_mission(karren, self.forschungs_stufen()))
        if menge > ladung:
            return False, (f"Überladen: {menge} passen nicht auf {ladung} Ladeplätze "
                           f"({', '.join(f'{k}x {n}' for n, k in sorted(karren.items()))}).")

        # Übergang, ehrlich benannt: erst das Ortslager, dann das Reichsheer — nur der Fehlbetrag.
        aus_reich: Dict[str, int] = {}
        for name, anzahl in karren.items():
            im_ort = int((getattr(quelle, "einheiten", None) or {}).get(name, 0))
            rest = anzahl - im_ort
            if rest <= 0:
                continue
            verfuegbar = (int(self.units[name].count) if name in self.units
                          else 0) if not self._lokale_kasse_aktiv() else 0
            if verfuegbar < rest:
                return False, (f"Nicht genug {name}: der Ort hat {im_ort}, im Reichsheer stehen "
                               f"{verfuegbar} — gebraucht werden {anzahl}.")
            aus_reich[name] = rest

        im_ort = float((getattr(quelle, "vorraete", None) or {}).get(stoff, 0.0))
        if im_ort + 1e-9 < menge:
            return False, (f"{quelle.name} hat nur {im_ort:g} {stoff.capitalize()} im Ortslager — "
                           f"für {menge} fehlen {menge - im_ort:g}. Transporte bewegen den Bestand "
                           f"DES ORTES (führend seit Teil 3a), nicht den Reichsbestand.")

        quelle_dict = asdict(quelle)
        for name, anzahl in aus_reich.items():
            quelle_dict["einheiten"][name] = int(quelle_dict["einheiten"].get(name, 0)) + anzahl
        try:
            neu, mission = spieloekonomie.transport_start(quelle_dict, asdict(ziel), karren,
                                                          {stoff: menge}, jetzt,
                                                          forschung=self.forschungs_stufen())
        except ValueError as fehler:
            return False, str(fehler)

        # Ab hier ist alles geprüft — erst jetzt wird der Spielstand getauscht (keine halbe Buchung).
        for name, anzahl in aus_reich.items():
            if name in self.units:
                self.units[name].count = max(0, int(self.units[name].count) - anzahl)
        self._ort_uebernehmen(quelle.id, neu)
        mission["von"] = quelle.name
        mission["nach"] = ziel.name
        mission["ziel"] = {"name": ziel.name, "id": ziel.id}
        # GPT-Z01: realer Startzeitpunkt nur fuer Protokoll, nicht die Ankunftsrechnung.
        mission.update(zeitbasis.zeitmarke())
        self.auftraege.append(mission)
        meldung = (f"Transport gestartet: {menge} {stoff.capitalize()} von {quelle.name} nach "
                   f"{ziel.name} ({', '.join(f'{k}x {n}' for n, k in sorted(karren.items()))}); "
                   f"Ankunft in {float(mission.get('reisezeit') or 0.0) / 3600.0:.2f} h.")
        self._log(meldung)
        return True, meldung

    def _eigentransport_buchen(self, eintrag: dict, jetzt: float) -> dict:
        """Einen EIGENEN Transport über den KERN buchen (Ankunft und Rückkehr je genau einmal).

        `spieloekonomie.transport_fortschritt` schreibt die Fracht am Ziel in das ORTSLAGER (samt
        Importherkunft) und lässt die Karren beim Ausgangsort zurück. `auftraege.spieldaten_anwenden`
        darf ihn NIE anwenden (Entwurf Z. 505, dort hart erzwungen); deshalb läuft die Heimkehr hier
        und NICHT über den Reichsbestand. Ist der Ausgangsort verloren, sucht der Kern eine eigene
        Ersatzsiedlung; gibt es keine, bleibt die Fracht am Auftrag — keine Geistergutschrift.
        """
        fracht_vorher = dict(eintrag.get("fracht") or {})
        truppe_vorher = dict(eintrag.get("einheiten") or {})
        vorher_geliefert = bool(eintrag.get("geliefert_lokal"))
        vorher_heim = bool(eintrag.get("heimgekehrt_lokal"))
        orte = {s.id: asdict(s) for s in self.settlements if s.id}
        neu, m = spieloekonomie.transport_fortschritt(dict(eintrag), orte, jetzt)
        for kennung, daten in neu.items():
            self._ort_uebernehmen(kennung, daten)
        if m.get("geliefert_lokal") and not vorher_geliefert:
            self.messages.append({"type": "auftrag",
                                  "spielzeit_sekunden": float(m.get("ankunft", jetzt)),
                                  "text": f"Transport angekommen in {m.get('nach')}: "
                                  + ", ".join(f"{int(v)} {k.capitalize()}"
                                              for k, v in sorted(fracht_vorher.items()))
                                  + " im Ortslager gutgeschrieben."})
        if m.get("heimgekehrt_lokal") and not vorher_heim:
            self.messages.append({"type": "auftrag",
                                  "spielzeit_sekunden": float(m.get("rueckkehr", jetzt)),
                                  "text": f"Transport heimgekehrt nach {m.get('von')}: "
                                  + ", ".join(f"{int(v)} {k}" for k, v in sorted(truppe_vorher.items()))
                                  + " wieder im Ortslager."})
        eintrag.clear()
        eintrag.update(m)
        # Erst wenn die Karren wirklich heim sind, gilt der Auftrag als heimgekehrt: sobald dieser
        # Merker steht, wird die Mission nicht mehr doppelt gezählt (`alle_einheiten`) und am Ende
        # des Takts entfernt. Bleibt die Heimkehr aus (kein eigener Ort mehr), bleibt auch die
        # Mission stehen — der Kern hält die Fracht am Auftrag.
        if m.get("geliefert_lokal") and m.get("heimgekehrt_lokal"):
            eintrag["heimgekehrt"] = True
        return eintrag

    # -------- Ökonomie-Paket, Schritt 9, Teil 7b: der BESTÄTIGTE KAUFVERTRAG (Auditteil 8b) --------
    # Entwurf Z. 779/781 („bestätigtes Angebot … oder eine deutliche noch-nicht-verfügbar-Meldung").
    # Der Spieler ist der KÄUFER, der Bot der VERKÄUFER: der Bot bietet einen Rohstoff aus seinen
    # Vorräten an, der Spieler zahlt Gold aus dem ORTSLAGER und stellt die HANDELSKARAWANE. Belegt
    # (Handbuch S. 20, Abschnitt „Handel"): gehandelt wird nur mit Handelskarawanen, der Preis steht
    # beim Angebot fest, und bei Ablehnung kehrt die Karawane MIT den Waren zurück — Gold wird nie
    # übertragen. Geprüft und gesperrt wird ausschließlich im Kern (`spieloekonomie.handel_start`),
    # gebucht wird die Ankunft von `_fremdvertrag_buchen` (Muster: `_eigentransport_buchen`, Teil 4).

    def handelskarawanen_bestand(self, siedlung: Settlement) -> Dict[str, int]:
        """Die verfügbaren HANDELSKARAWANEN eines Ortes — Ortslager zuerst, dann das Reichsheer.

        Nur ECHTE Handelskarawanen: Handkarren, Einspänner und Zweispänner tragen Fracht, dürfen
        aber nicht handeln (belegt in `auftraege.auftragsarten`: „Nur Handelskarawanen", Handbuch
        S. 20). Fehlt ein Karren im Ortslager, kommt er wie beim Transport als ÜBERGANG aus dem
        Reichsheer — dieselbe ehrlich benannte Übergangskasse.
        """
        bestand: Dict[str, int] = {}
        for name, anzahl in (getattr(siedlung, "einheiten", None) or {}).items():
            if "Handelskarawane" in str(name) and int(anzahl) > 0:
                bestand[name] = int(bestand.get(name, 0)) + int(anzahl)
        for name, einheit in self.units.items():
            if "Handelskarawane" in str(name) and int(einheit.count) > 0:
                bestand[name] = int(bestand.get(name, 0)) + int(einheit.count)
        return bestand

    def bot_standort(self, siedlung: Settlement) -> Tuple[int, int]:
        """Das ANGENOMMENE Weltfeld einer Bot-Siedlung — eine Annahme, ehrlich benannt.

        Bot-Siedlungen führen bei uns KEINE Koordinaten; es gilt dieselbe Annahme wie in
        `_auftrag_entfernung` (Kartenmitte). Läge die eigene Siedlung genau auf diesem Feld, wäre
        die Entfernung 0 und der Auftragskern würde ablehnen — dann rückt die ANNAHME um ein Feld,
        damit die Karawane eine echte Strecke hat. Ein Vorschlag, kein belegter Wert.
        """
        cfg = next((m for m in MAPS if m["id"] == self.current_map), None)
        groesse = int(cfg["size"]) if cfg else 20
        mitte = groesse // 2
        if siedlung is not None and (int(siedlung.x), int(siedlung.y)) == (mitte, mitte):
            mitte = mitte + 1 if mitte + 1 < groesse else max(0, mitte - 1)
        return mitte, mitte

    def bot_als_ort(self, bot: BotPlayer, x: int, y: int, dimension: int) -> Dict[str, object]:
        """Der Bot in der Form, die der HANDELSKERN braucht — ein FREMDER Ort.

        `bot_als_dict` ist die Form für `botkern`; sie führt WEDER `besitzer` NOCH `dimension`,
        `vorraete`, `einheiten` oder `x`/`y` — GEMESSEN, nicht angenommen. Für
        `spieloekonomie.handel_start` fehlen genau diese Felder, deshalb hier die zweite, klar
        benannte Übersetzung: Besitzer `bot:<Name>`, Lager `bot.vorraete`, Wagenpark `bot.lager`.
        `waren` und `importiert` führt ein Bot nicht (keine Warenrezepte, keinen Siegnachweis) —
        sie sind leer und werden nicht zurückgelesen.
        """
        return {"id": "bot:%s" % bot.name, "name": bot.name, "besitzer": "bot:%s" % bot.name,
                "dimension": int(dimension), "x": int(x), "y": int(y), "bevoelkerung": 0.0,
                "vorraete": {str(k): float(v) for k, v in (bot.vorraete or {}).items()},
                "waren": {}, "einheiten": {}, "importiert": {}}

    def bot_vorraete_uebernehmen(self, bot: BotPlayer, ort: dict) -> None:
        """Die VORRÄTE aus einem Bot-Ortsdict zurück in den Spielstand (eine Quelle bleibt botkern).

        Ganze Zahlen bleiben ganze Zahlen; nur ein echter Bruchteil (Gold bei krummem Preis) wird
        als Kommazahl behalten — nicht stillschweigend gerundet, damit dem Bot kein Ganzes
        verschwindet.
        """
        if not isinstance(ort, dict):
            return
        sauber: Dict[str, object] = {}
        for stoff, menge in (ort.get("vorraete") or {}).items():
            zahl = float(menge)
            sauber[str(stoff)] = int(zahl) if zahl.is_integer() else zahl
        bot.vorraete = sauber

    def handel_mit_bot(self, bot: BotPlayer, quelle: Settlement, ware: str, menge, preis,
                       karawane: dict, jetzt: float = None) -> Tuple[bool, str]:
        """Ein BESTÄTIGTES KAUFANGEBOT an einen fremden Bot schicken. Liefert ``(ok, Meldung)``.

        Geprüft und gesperrt wird ausschließlich im KERN (`spieloekonomie.handel_start`): Ware,
        Menge, Preis, fremder Besitzer, gleiche Dimension, Handelskarawane vor Ort, beidseitige
        Deckung (Lager UND Gold) und die Rückladung. Abgelehnt wird VOR jeder Änderung. Fehlt Gold
        oder Karawane im Ortslager, kommt der Fehlbetrag als ÜBERGANG aus dem Reich — der Bot zahlt
        nichts dazu.
        """
        jetzt = float(self.spielsekunden) if jetzt is None else float(jetzt)
        if bot is None:
            return False, "Kein Handelspartner gewählt."
        if quelle is None:
            return False, "Für einen Handel braucht es zuerst eine eigene Siedlung."
        if float(bot.trading) <= 0.3:
            return False, (f"{bot.name} handelt nicht (Handelsneigung "
                           f"{int(float(bot.trading) * 100)} %).")
        try:
            if isinstance(menge, bool):
                raise ValueError
            roh_menge = menge
            menge = int(menge)
            if isinstance(roh_menge, float) and float(roh_menge) != float(menge):
                raise ValueError          # 2,5 Stueck gibt es nicht — nicht stillschweigend kuerzen
        except (TypeError, ValueError):
            return False, "Die Menge muss eine ganze Zahl sein."
        if menge <= 0:
            return False, "Die Menge muss größer als 0 sein."
        try:
            if isinstance(preis, bool):
                raise ValueError
            preis = float(preis)
        except (TypeError, ValueError):
            return False, "Der Preis muss eine Zahl sein."
        if not math.isfinite(preis) or preis <= 0:
            return False, "Der Preis muss eine positive Zahl sein."
        stoff = str(ware or "").lower()
        if stoff == "gold":
            return False, "Gold ist die Gegenleistung und kein Handelsgut."
        if stoff not in RESOURCES or stoff not in (bot.vorraete or {}):
            return False, f"{bot.name} hat kein {ware} im Angebot."
        try:
            karawane = {str(n): int(k) for n, k in (karawane or {}).items() if int(k) > 0}
        except (TypeError, ValueError):
            return False, "Die Karawanen-Anzahl muss eine ganze Zahl sein."
        if not karawane:
            return False, ("Für einen Handel wird eine HANDELSKARAWANE gebraucht (Handbuch S. 20) "
                           "— Handkarren und Einspänner tragen Fracht, handeln aber nicht.")
        kein_handel = [n for n in karawane if "Handelskarawane" not in str(n)]
        if kein_handel:
            return False, ("Handeln ist nur mit Handelskarawanen möglich (Handbuch S. 20): "
                           + ", ".join(sorted(kein_handel)) + " kann nicht handeln.")
        ladung = int(auftraege.ladung_der_mission(karawane, self.forschungs_stufen()))
        if menge > ladung:
            return False, ("Überladen: %d passen nicht auf %d Ladeplätze (%s)."
                           % (menge, ladung, ", ".join("%s x%d" % (n, a)
                                                       for n, a in sorted(karawane.items()))))

        # Übergang, ehrlich benannt: erst das Ortslager, dann das Reich — nur der Fehlbetrag.
        gold_gesamt = menge * preis
        aus_reich_karren: Dict[str, int] = {}
        for name, anzahl in karawane.items():
            im_ort = int((getattr(quelle, "einheiten", None) or {}).get(name, 0))
            rest = anzahl - im_ort
            if rest <= 0:
                continue
            verfuegbar = (int(self.units[name].count) if name in self.units
                          else 0) if not self._lokale_kasse_aktiv() else 0
            if verfuegbar < rest:
                return False, (f"Nicht genug {name}: der Ort hat {im_ort}, im Reichsheer stehen "
                               f"{verfuegbar} — gebraucht werden {anzahl}.")
            aus_reich_karren[name] = rest
        gold_im_ort = float((getattr(quelle, "vorraete", None) or {}).get("gold", 0.0))
        aus_reich_gold = max(0.0, gold_gesamt - gold_im_ort)
        if aus_reich_gold > 0.0 and self._lokale_kasse_aktiv():
            return False, (f"Zu wenig Gold im Ortslager von {quelle.name}: "
                           f"{gold_im_ort:g} vorhanden, {gold_gesamt:g} benoetigt. "
                           "Ohne echten Transport kein Fernzugriff.")
        if aus_reich_gold > 0.0:
            reich_gold = float(self.resources["gold"].amount) if "gold" in self.resources else 0.0
            if reich_gold + 1e-9 < aus_reich_gold:
                return False, (f"Zu wenig Gold: im Ortslager liegen {gold_im_ort:g}, im Reich "
                               f"{reich_gold:g} — der Kauf kostet {gold_gesamt:g} "
                               f"({menge} x {preis:g} je Stück).")

        x, y = self.bot_standort(quelle)
        dimension = int(getattr(quelle, "dimension", 1))
        kaeufer = asdict(quelle)
        for name, anzahl in aus_reich_karren.items():
            kaeufer["einheiten"][name] = int(kaeufer["einheiten"].get(name, 0)) + anzahl
        kaeufer["vorraete"]["gold"] = gold_im_ort + aus_reich_gold
        try:
            kaeufer_neu, verkaeufer_neu, vertrag = spieloekonomie.handel_start(
                kaeufer, self.bot_als_ort(bot, x, y, dimension), karawane, stoff, menge, preis,
                "vorraete", jetzt, forschung=self.forschungs_stufen())
        except ValueError as fehler:
            return False, str(fehler)

        # Ab hier ist alles geprüft — erst jetzt wird gebucht (keine halbe Buchung).
        if aus_reich_gold > 0.0:
            self.resources["gold"].amount = float(self.resources["gold"].amount) - aus_reich_gold
        for name, anzahl in aus_reich_karren.items():
            if name in self.units:
                self.units[name].count = max(0, int(self.units[name].count) - anzahl)
        self._ort_uebernehmen(quelle.id, kaeufer_neu)
        self.bot_vorraete_uebernehmen(bot, verkaeufer_neu)
        vertrag["von"] = quelle.name
        vertrag["nach"] = bot.name
        vertrag["bot"] = bot.name
        vertrag["ziel"] = {"name": bot.name, "fremd": True}
        vertrag["bot_x"], vertrag["bot_y"] = int(x), int(y)
        vertrag["dimension"] = dimension
        vertrag.update(zeitbasis.zeitmarke())
        self.auftraege.append(vertrag)
        meldung = ("Kaufangebot an %s: %d %s für %g Gold (%g je Stück, Karawane %s); Ankunft in "
                   "%.2f h — ob der Handel zustande kommt, entscheidet %s bei der Ankunft."
                   % (bot.name, menge, stoff.capitalize(), gold_gesamt, preis,
                      ", ".join("%s x%d" % (n, a) for n, a in sorted(karawane.items())),
                      float(vertrag.get("reisezeit") or 0.0) / 3600.0, bot.name))
        self._log(meldung)
        self.messages.append({"text": meldung, "type": "handel"})
        return True, meldung

    def _fremdvertrag_buchen(self, eintrag: dict, jetzt: float) -> dict:
        """Einen FREMDVERTRAG über den KERN buchen — die ANKUNFT entscheidet (Auditteil 8b).

        `spieloekonomie.handel_abschluss` bucht Ankunft und Rückkehr genau einmal: nimmt der
        Verkäuferort an, wandert das gesperrte Gold zu ihm und die Ware kommt bei der Rückkehr beim
        Käufer an; lehnt er ab, kehren Gold UND Ware vollständig zurück. Dass abgelehnt werden kann,
        ist belegt (Handbuch S. 20: „Bei Ablehnung kehrt die Karawane MIT den Waren zurück, Gold
        wird nie übertragen"); der GRUND ist es nicht — hier entscheidet der belegte Schwellenpreis
        des Bots (`botkern.handelspreis`), also genau der Preis, den die Meldung aus Teil 7a schon
        nannte. Das ist ein Vorschlag. `auftraege.spieldaten_anwenden` lässt einen Fremdvertrag
        unberührt; gebucht wird ausschließlich hier.
        """
        vertrag = dict(eintrag)
        der_bot = next((b for b in self.bots
                        if ("bot:%s" % b.name) == str(vertrag.get("verkaeufer"))), None)
        if jetzt >= float(vertrag.get("ankunft") or 0.0) and vertrag.get("entscheidung") is None \
                and not vertrag.get("abgerechnet") and der_bot is not None:
            referenz = botkern.referenzpreis_aus_beschaffung(BOT_BESCHAFFUNGSKOSTEN)
            schwelle = float(botkern.handelspreis(referenz, float(der_bot.temperament)))
            try:
                vertrag = spieloekonomie.handel_entscheiden(
                    vertrag, float(vertrag.get("preis") or 0.0) + 1e-9 >= schwelle)
            except ValueError:
                pass
        angenommen_vorher = bool(vertrag.get("angenommen"))
        abgerechnet_vorher = bool(vertrag.get("abgerechnet"))

        orte = {s.id: asdict(s) for s in self.settlements if s.id}
        if der_bot is not None:
            orte[str(vertrag.get("verkaeufer"))] = self.bot_als_ort(
                der_bot, int(vertrag.get("bot_x") or 0), int(vertrag.get("bot_y") or 0),
                int(vertrag.get("dimension") or 1))
        neu, m = spieloekonomie.handel_abschluss(vertrag, orte, jetzt)
        for kennung, daten in neu.items():
            bot_dazu = next((b for b in self.bots if ("bot:%s" % b.name) == kennung), None)
            if bot_dazu is not None:
                self.bot_vorraete_uebernehmen(bot_dazu, daten)
            else:
                self._ort_uebernehmen(kennung, daten)

        menge = int(m.get("menge") or 0)
        stoff = str(m.get("ware") or "").capitalize()
        if m.get("angenommen") and not angenommen_vorher:
            text = ("%s nimmt das Kaufangebot an: %d %s für %g Gold sind unterwegs."
                    % (m.get("nach"), menge, stoff, float(m.get("preis") or 0.0) * menge))
            self.messages.append({"text": text, "type": "handel",
                                  "spielzeit_sekunden": float(m.get("ankunft", jetzt))})
            self._log(text)
        abgerechnet_jetzt = bool(m.get("abgerechnet")) and not abgerechnet_vorher
        if abgerechnet_jetzt:
            if m.get("angenommen"):
                text = ("Handel abgeschlossen: %d %s sind im Ortslager von %s angekommen."
                        % (menge, stoff, m.get("von")))
            else:
                text = ("Handel abgelehnt: %s schickt die Karawane MIT den %d %s zurück — "
                        "Gold wurde nicht übertragen." % (m.get("nach"), menge, stoff))
            self.messages.append({"text": text, "type": "handel",
                                  "spielzeit_sekunden": float(m.get("rueckkehr", jetzt))})
            self._log(text)
        eintrag.clear()
        eintrag.update(m)
        # Der Merker kommt NACH der Übernahme (sonst löscht ihn `update`): erst wenn der Vertrag
        # wirklich abgerechnet ist, gilt er als heimgekehrt — dann entfernt ihn das Ende des Takts,
        # und die Karawane wird nicht noch einmal im Reichsheer gezählt.
        if abgerechnet_jetzt:
            eintrag["heimgekehrt"] = True
        return eintrag

    # ---------------- Ökonomie-Paket, Schritt 9, Teil 5: die Gründung (Entwurf Z. 777) ----------------
    # „_found_settlement: erster Start übernimmt Startbestände genau einmal und startkarte; danach
    # öffnet eine Auswahlliste freier KarteIDs samt kartennutzen/Kapazitäten/Preis/Minimum, ruft
    # absicht statt sofort append auf. Keine zufällige Erstwahl, kein zufälliges Weltfeld nach
    # erfolgreicher Zahlung." Der Kern ist `src/spieloekonomie.py` (absicht/vergabe/vergabe-Regeln).

    def nahrungsnot(self, siedlung) -> Dict[str, object]:
        """Steht DIESER Ort in Nahrungsnot? (Daniels Vorgabe, Register 70/74.)

        Rechnet ausschliesslich ueber `spieloekonomie.nahrungsnot` - dieselbe Funktion, deren
        Schwelle im Register steht (Lager leer UND Verbrauch groesser als die eigene Ernte).
        """
        return spieloekonomie.nahrungsnot(asdict(siedlung), self.forschungs_stufen())

    def forschungs_stufen(self) -> Dict[str, int]:
        """Die erreichten Forschungsstufen als FLACHE Karte `{Gebiet: Stufe}`.

        EINE Lesestelle fuer alles, was mit Forschungsstufen rechnet (Ladung mit Wagenbau-Bonus,
        Kernfunktionen, Anzeigen). Vorher stand `{k: int(v.level) ...}` an sechs Stellen im Code -
        jede davon haette den Wagenbau-Bonus vergessen koennen.
        """
        return {k: int(getattr(v, "level", 0) or 0) for k, v in (self.research or {}).items()}

    def kartenvorrat_anlegen(self, seed: str = "") -> Dict[str, dict]:
        """Den Kartenvorrat für Neugründungen anlegen (die Startkarte bleibt außerhalb).

        Die Saat wird gemerkt: derselbe Spielstand ergibt denselben Vorrat, und ein geladener
        Stand vergibt seine Karten genau so weiter, wie er sie angelegt hat.
        """
        if not seed:
            seed = self.kartenvorrat_seed or "nebel-%d" % random.randrange(1, 10 ** 9)
        self.kartenvorrat_seed = str(seed)
        self.kartenvorrat = spieloekonomie.vorrat(self.kartenvorrat_seed)
        return self.kartenvorrat

    def freie_koloniekarten(self) -> list:
        """Die freien Koloniekarten mit allem, was die Auswahl braucht (Entwurf Z. 777).

        Je Karte: Kennung, Karte, **Nutzen** für unser Portfolio, Stundenkapazitäten,
        **Gründungsgebühr** und **Mindestbestand**. Sortiert nach Nutzen (beste zuerst) — die
        Liste ist damit eine Empfehlung und keine Zufallswahl.
        """
        if not self.kartenvorrat:
            self.kartenvorrat_anlegen()
        vorhandene = [s.karte for s in self.settlements if getattr(s, "karte", None)]
        preis, _paket, minimum = spieloekonomie.gruendungskosten()
        eintraege = []
        for kennung, eintrag in sorted(self.kartenvorrat.items()):
            if eintrag.get("besitzer") is not None:
                continue
            karte = eintrag.get("karte") or {}
            eintraege.append({
                "karte_id": kennung,
                "karte": karte,
                "nutzen": spieloekonomie.kartennutzen(vorhandene, karte),
                "kapazitaeten": spieloekonomie.kapazitaeten(karte),
                "preis": dict(preis),
                "minimum": dict(minimum),
            })
        eintraege.sort(key=lambda e: (-e["nutzen"], e["karte_id"]))
        return eintraege

    def _weltkarte_sicherstellen(self) -> None:
        """Die Weltkarte aufbauen, falls sie noch fehlt (Auswahl UND Gründung brauchen sie).

        `get_tile` greift auf `self.map_tiles` zu; ein frischer Zustand oder eine Prüfung hat die
        Karte noch nicht aufgebaut (die Anwendung erzeugt sie beim Start). Ohne diese Zeile stürzte
        die Auswahl mit `IndexError` ab statt zu arbeiten.
        """
        cfg = next((m for m in MAPS if m["id"] == self.current_map), None)
        if cfg is not None and len(self.map_tiles) < cfg["size"] * cfg["size"]:
            self.generate_map(self.current_map)

    def freie_weltfelder(self, anzahl: int = 6) -> list:
        """Die freien Weltfelder der aktuellen Karte in FESTER Reihenfolge (kein Zufall).

        Entwurf Z. 777: das Weltfeld wird VOR der Zahlung festgelegt („kein zufälliges Weltfeld
        nach erfolgreicher Zahlung"), deshalb eine nachprüfbare Auswahl.
        """
        cfg = next((m for m in MAPS if m["id"] == self.current_map), None)
        if cfg is None:
            return []
        self._weltkarte_sicherstellen()
        felder = []
        for y in range(cfg["size"]):
            for x in range(cfg["size"]):
                feld = self.get_tile(x, y, cfg["size"])
                if feld is None or feld.terrain == "water" or feld.npc_faction:
                    continue
                felder.append((x, y))
                if len(felder) >= anzahl:
                    break
            if len(felder) >= anzahl:
                break
        return felder

    def gruendung_pruefen(self, quelle: Settlement, karte_id: str, feld) -> Tuple[bool, str, dict]:
        """Eine Gründungsabsicht prüfen, OHNE etwas zu buchen. ``(ok, Meldung, Absicht)``.

        Geprüft wird über den KERN (`spieloekonomie.absicht`): freie Karte, Siedlungsgrenze,
        Gründungsforschung, **Siedlerkarren** und **Mindestbestand im Ortslager** der Ausgangs-
        siedlung. Der Siedlerkarren kommt zur Not als Übergang aus dem Reichsheer (wie beim
        Transport) — sonst wäre die Gründung unerreichbar, solange die Ortslager für Einheiten
        noch leer sind (Teil 6 füllt sie).
        """
        if quelle is None:
            return False, "Keine Ausgangssiedlung gewählt.", {}
        if not karte_id:
            return False, "Keine Karte gewählt.", {}
        if not self.kartenvorrat:
            self.kartenvorrat_anlegen()
        karren = spieloekonomie.REGELN["gruendung"]["karren"]
        quelle_dict = asdict(quelle)
        quelle_dict["siedlungsgrenze"] = SIEDLUNGEN_MAXIMUM
        im_ort = int((quelle_dict.get("einheiten") or {}).get(karren, 0))
        aus_reich = max(0, 1 - im_ort)
        if aus_reich and self._lokale_kasse_aktiv():
            return False, (f"Ein {karren} muss in {quelle.name} stationiert sein. "
                           "Karren aus anderen Orten zaehlen erst nach der Ankunft."), {}
        if aus_reich:
            verfuegbar = int(self.units[karren].count) if karren in self.units else 0
            if verfuegbar < aus_reich:
                return False, (f"Für eine Neugründung wird ein {karren} gebraucht — er steht "
                               f"weder im Lager von {quelle.name} noch im Reichsheer "
                               f"(ausgebildet wird er im Stellmacher)."), {}
            quelle_dict["einheiten"][karren] = im_ort + aus_reich
        vorhandene = [s.karte for s in self.settlements if getattr(s, "karte", None)]
        # `absicht` erwartet eine FLACHE Stufenkarte {Gebiet: Stufe} — `forschung_stand()` liefert
        # je Gebiet ein Verzeichnis, das wäre ein Vergleich von Dict und Zahl (TypeError).
        stufen = {k: int(v.level) for k, v in self.research.items()}
        try:
            absicht = spieloekonomie.absicht(quelle_dict, karte_id, vorhandene, self.kartenvorrat,
                                             stufen, 0)
        except ValueError as fehler:
            return False, str(fehler), {}
        absicht["weltfeld"] = list(feld or [])
        absicht["aus_reich"] = aus_reich
        # Die Vergabe kommt ebenfalls aus dem KERN (ein Bewerber: der Spieler).
        entschieden = spieloekonomie.vergabe([absicht], self.kartenvorrat, self.kartenvorrat_seed, 0)
        if not entschieden or not entschieden[0][1]:
            return False, "Diese Karte ist nicht mehr frei.", {}
        return True, "", absicht

    def gruendung_ausfuehren(self, quelle: Settlement, karte_id: str, feld) -> Tuple[bool, str]:
        """Eine geprüfte Gründung buchen. ``(ok, Meldung)`` — vorher wird ALLES erneut geprüft.

        Gebucht wird in dieser Reihenfolge: Sperrgut (Mindestbestand = Gebühr + Startpaket) aus
        dem **Ortslager** der Ausgangssiedlung, der **Siedlerkarren** (er wird für die Gründung
        verbraucht — die Entwurfslesart zu „Sperrgut des Gewinners"), die Karte wird vergeben, und
        die neue Siedlung bekommt **Startpaket + 5 Kolonisten** und ihr gewähltes Weltfeld. Die
        Gebühr ist damit vernichtet (Mindestbestand minus Startpaket), die Gesamtmengen bleiben
        sonst erhalten. Schlägt eine Prüfung fehl, ist NICHTS gebucht.
        """
        ok, meldung, absicht = self.gruendung_pruefen(quelle, karte_id, feld)
        if not ok:
            return False, meldung
        x, y = [int(v) for v in absicht["weltfeld"]]
        self._weltkarte_sicherstellen()
        if not self.get_tile(x, y, next(m for m in MAPS if m["id"] == self.current_map)["size"]):
            return False, "Das gewählte Weltfeld liegt nicht auf der Karte."
        ok_zahlung, meldung_zahlung = self.verbrauche_am_ort(quelle, absicht["sperrgut"])
        if not ok_zahlung:
            return False, meldung_zahlung
        karren = spieloekonomie.REGELN["gruendung"]["karren"]
        if absicht["aus_reich"] and karren in self.units:
            self.units[karren].count = max(0, int(self.units[karren].count) - absicht["aus_reich"])
        im_ort = int((quelle.einheiten or {}).get(karren, 0))
        if im_ort > 0:
            quelle.einheiten[karren] = im_ort - 1
            if quelle.einheiten[karren] <= 0:
                quelle.einheiten.pop(karren, None)
        siedler = int(spieloekonomie.U.get(karren, {}).get("kosten", {}).get("siedler", 0))
        karte = self.kartenvorrat[karte_id]["karte"]
        name = f"Siedlung {len(self.settlements) + 1}"
        neu = Settlement(name=name, map_id=self.current_map, x=x, y=y, karte=karte,
                         id=siedlung_kennung("spieler", self.current_map, x, y),
                         volk=str(getattr(self, "spieler_fraktion", "") or ""))
        neu.vorraete = {r: float(v) for r, v in absicht["paket"].items()}
        neu.bevoelkerung = float(siedler)
        self.settlements.append(neu)
        self._reichsanzeige_aus_orten()
        self.kartenvorrat[karte_id]["besitzer"] = "spieler"
        self.hatte_siedlung = True
        size = next(m for m in MAPS if m["id"] == self.current_map)["size"]
        tile = self.get_tile(x, y, size)
        if tile is not None:
            tile.npc_faction = "spieler"
            tile.sector_name = name
        # Auch eine Kolonie bekommt die drei Startgebaeude des Siedlungskarren (Schnitt S-1).
        _start_ergebnisse = _startgebaeude_setzen(neu, karte)
        # S-2c-D: das Dorfzentrum kommt ebenfalls mit - aber OHNE Platz. Der Spieler setzt es
        # selbst auf ein Feld seiner Karte (`_dorfzentrum_setzen`), kostenlos.
        neu.dorfzentrum_offen = True
        _start_text = _startgebaeude_meldung(_start_ergebnisse)
        if _start_text:
            self.messages.append({"type": "gruendung", "text": _start_text})
            self._log(_start_text)
        meldung = (f"Neue Siedlung '{name}' gegründet ({karte['typ_name']}, Feld {x}/{y}) — "
                   f"{siedler} Kolonisten und das Startpaket sind angekommen; "
                   f"im Ortslager von {quelle.name} ist der Mindestbestand verbraucht.")
        self._log(meldung)
        return True, meldung

    # ---------------- W3: Werkstaetten, Originalwaren, Warteschlangen ----------------

    def werkstatt_schlangen(self) -> Dict[str, dict]:
        """Die Warteschlangen je gebauter Werkstatt.

        Wie viele Werkstaetten es gibt und welcher Art, kommt aus den wirklich **bebauten
        Feldern** der Siedlungskarten (`werkstatt.werkstaetten_bestand`) - nicht aus einer
        zweiten, globalen Gebaeudeliste.
        """
        for kennung, anzahl in werkstatt.werkstaetten_bestand(self.settlements).items():
            if anzahl <= 0:
                continue
            if kennung in self.werkstaetten:
                self.werkstaetten[kennung]["werkstaetten"] = anzahl
                self.werkstaetten[kennung]["kapazitaet"] = werkstatt.kapazitaet(anzahl)
            else:
                self.werkstaetten[kennung] = werkstatt.neue_warteschlange(kennung, anzahl)
        return self.werkstaetten

    def werkstatt_fortschreiben(self, jetzt: float) -> Dict[str, int]:
        """Fertige Waren ins Lager buchen und melden, was diesmal ankam.

        `werkstatt.fertige_waren` merkt sich, was schon gemeldet wurde - jede Ware kommt
        deshalb genau einmal an, auch wenn der Zeitlauf häufig tickt.
        """
        gebucht: Dict[str, int] = {}
        for schlange in self.werkstaetten.values():
            for ware, anzahl in werkstatt.fertige_waren(schlange, jetzt).items():
                self.waren[ware] = int(self.waren.get(ware, 0)) + int(anzahl)
                gebucht[ware] = gebucht.get(ware, 0) + int(anzahl)
        return gebucht

    def _forschungsstufen(self) -> Dict[str, int]:
        """{Gebiet: Stufe} aus dem Forschungsstand — eine Lesestelle fuer Warenpruefungen."""
        return {k: int(v.level) for k, v in self.research.items()}

    def ware_voraussetzung(self, ware: str):
        """Prueft die Voraussetzungen einer Ware — EINE Quelle fuer Kern UND Anzeige (F-04).

        Gelesen wird `data/warenrezepte.json` ueber `spieloekonomie.ware_voraussetzung` — genau
        die Funktion, mit der `ware_start` die Herstellung freigibt. Die fruehere zweite Wahrheit
        (Feld `voraussetzung_struktur` aus `items.json`, bei fehlender Struktur stillschweigend
        `True`) ist weg: Lederrüstung und Magischer Paladinharnisch haben dort GAR KEINE Struktur,
        im Rezept aber je ZWEI Bedingungen (UND) — die Anzeige zeigte sie also als erlaubt, der
        Kern lehnte ab (Register 68).

        Rueckgabe (erfuellt, Begruendung); die Begruendung nennt jede Bedingung.
        """
        return spieloekonomie.ware_voraussetzung(ware, self._forschungsstufen())

    def ware_voraussetzungen(self, ware: str) -> list:
        """Jede Forschungsbedingung EINZELN — fuer die Anzeige, aus derselben Quelle wie der Kern."""
        return spieloekonomie.ware_voraussetzungen_liste(ware, self._forschungsstufen())

    # ---------------- W7: Auftraege (Missionen) ----------------

    def auftrag_starten(self, art: str, mitgenommene: dict, von: str, nach, entfernung: float,
                        fracht: dict = None, ziel_zusatz: dict = None, quelle_id: str = None):
        """Einen Auftrag starten. Rueckgabe (ok, Meldung).

        Quelle ist das **ORTSHEER** der Siedlung ``quelle_id`` (F-01/F-09 der externen
        Spielpruefung 31.10.2026): die Einheiten kommen aus `Settlement.einheiten`, werden dort
        abgebucht und kehren in DENSELBEN Ort zurueck (`einsatz_zurueck`). Der Reichsbestand ist
        reine Anzeige; er traegt nur noch alte Spielstaende ohne Siedlung (Uebergang).

        Die mitgegebenen Einheiten sind ab jetzt **unterwegs**: sie werden hier aus dem Ortslager
        genommen und bei `abgeschlossen` zurueckgegeben - ausser beim **Stationieren**, da bleiben
        sie am Ziel (Handbuch S. 19). Geprueft wird alles ueber `auftraege.starten`; ohne genug
        Truppen im OERTLICHEN Lager (oder bei Ueberladung) wird VOR jeder Aenderung abgelehnt.
        """
        # Ohne Kennung gilt die aktive Siedlung (Rueckwaertsvertraeglichkeit fuer Aufrufer, die
        # noch keine Quelle nennen). Eine GENANNTE, aber unbekannte Kennung ersetzt niemand still.
        quelle = (self._siedlung_zu(quelle_id) if quelle_id
                  else self.aktive_siedlung())
        ziel = dict(ziel_zusatz or {})
        if isinstance(nach, dict):
            ziel.update(nach)
        ziel["name"] = str((nach.get("name") if isinstance(nach, dict) else nach) or "")
        if not ziel["name"]:
            return False, "Kein Ziel benannt."
        bestand = {k: int(v) for k, v in (mitgenommene or {}).items() if int(v) > 0}
        if not bestand:
            return False, "Ohne Einheiten kann kein Auftrag reisen."
        if quelle is not None:
            vorrat = self._ortsheer(quelle)
            zu_wenig = [k for k, v in bestand.items() if int(vorrat.get(k, 0)) < v]
        else:
            zu_wenig = [k for k, v in bestand.items()
                        if k not in self.units or int(self.units[k].count) < v]
        if zu_wenig:
            wo = quelle.name if quelle is not None else "dem Reich"
            return False, f"Nicht genug Einheiten in {wo}: {', '.join(sorted(zu_wenig))}."
        if quelle is not None:
            von = str(quelle.name or von)

        # V-5 (03.11.2026): das Volk des Ortes macht die Truppe schneller (elfisch +5 %). Der
        # Faktor gilt fuer die ZEIT (1/1,05) - dieselbe Groesse, die die Anzeige nennt.
        _volk_reise = str(getattr(quelle, "volk", "")
                          or getattr(self, "spieler_fraktion", "") or "")
        ok, meldung = auftraege.starten(self.auftraege, art, bestand, von, ziel,
                                        float(entfernung), float(self.spielsekunden), fracht,
                                        forschung=self.forschungs_stufen(),
                                        reise_faktor=boni.reisezeitfaktor(_volk_reise))
        if not ok:
            return False, meldung
        # Der Auftrag traegt seine Quelle als KENNUNG - durch ALLE Phasen (F-09). Ohne diese
        # Zeile startete jeder Angriff aus `settlements[0]` und kehrte auch dorthin zurueck.
        eintrag = self.auftraege[-1]
        eintrag["quelle_id"] = quelle.id if quelle is not None else ""
        if quelle is not None:
            eintrag["von"] = str(quelle.name)
            self.einsatz_ausheben(quelle, bestand)
        else:
            for k, v in bestand.items():
                self.units[k].count = max(0, int(self.units[k].count) - v)
        # Reisekosten (Paket A2 vom 31.10.2026; Saetze VORSCHLAG, siehe
        # auftraege.kosten_der_mission): bezahlt wird, was da ist - der Bestand wird nie
        # negativ, und ein Auftrag wird NICHT abgelehnt, solange die Hoehe im Spieltest offen
        # ist. Die Meldung nennt den Betrag, damit die Balance sichtbar bleibt.
        # Gezahlt wird DA, WO GEHANDELT WIRD (Ortslager der Quelle) - dieselbe Regel wie beim
        # Bauen, Forschen und Ausbilden; die Reichsanzeige ist keine Kasse (Entscheidung 11).
        kosten = dict((eintrag or {}).get("kosten") or {})
        bezahlt = {}
        for stoff, betrag in kosten.items():
            if not betrag:
                continue
            if quelle is not None:
                lager = float((quelle.vorraete or {}).get(stoff, 0.0))
                zahlbar = min(float(betrag), lager)
                if zahlbar > 0:
                    quelle.vorraete[stoff] = round(lager - zahlbar, 2)
                    bezahlt[stoff] = round(zahlbar, 2)
            elif stoff in self.resources:
                lager = float(self.resources[stoff].amount)
                zahlbar = min(float(betrag), lager)
                if zahlbar > 0:
                    self.resources[stoff].amount = lager - zahlbar
                    bezahlt[stoff] = round(zahlbar, 2)
        if quelle is not None:
            self._reichsanzeige_aus_orten()
        if bezahlt:
            meldung += (" Kosten: " + ", ".join(f"{menge:g} {stoff}"
                                                for stoff, menge in sorted(bezahlt.items()))
                        + " (VORSCHLAG-Saetze aus A2).")
        self._log(meldung)
        return True, meldung

    def auftraege_fortschreiben(self, jetzt: float) -> dict:
        """Auftraege weiterlaufen lassen und Heimkehrendes gutschreiben.

        Rueckgabe ``{'neu': [Berichtstitel], 'heimgekehrt': {einheit: anzahl}, 'gesamt': n}``.
        Genau einmal: `angekommen` setzt `abgeliefert`, `spieldaten_anwenden` setzt `angewendet`,
        und die Heimkehr merkt sich `heimgekehrt` - dieselbe Fracht zaehlt nie zweimal.
        """
        ergebnis = {"neu": [], "heimgekehrt": {}, "gesamt": 0}
        if not self.auftraege:
            return ergebnis
        auftraege.fortschritt(self.auftraege, jetzt)
        ergebnis["gesamt"] = len(self.auftraege)

        # Ökonomie-Paket, Schritt 9, Teil 4: eigene Transporte bucht der KERN — er schreibt die
        # Fracht am Ziel in das ORTSLAGER und lässt die Karren beim Ausgangsort zurück. Jede
        # Mission wird bei JEDEM Takt geführt (Ankunft und Rückkehr fallen zu verschiedenen Zeiten
        # an), und `auftraege.spieldaten_anwenden` lässt sie absichtlich unberührt (Entwurf Z. 505).
        for eintrag in list(self.auftraege):
            if eintrag.get("eigentransport"):
                self._eigentransport_buchen(eintrag, jetzt)
            # Teil 7b: ein FREMDVERTRAG (Kaufvertrag mit einem Bot) gehört ebenso dem Kern allein —
            # die ANKUNFT entscheidet, `handel_abschluss` bucht Gold, Ware und Heimkehr genau einmal.
            elif eintrag.get("fremdvertrag"):
                self._fremdvertrag_buchen(eintrag, jetzt)

        for eintrag in auftraege.angekommen(self.auftraege, jetzt):
            if eintrag.get("eigentransport") or eintrag.get("fremdvertrag"):
                continue                  # oben gebucht, in den ORTSLAGERN statt im Reichsbestand
            if eintrag.get("art") == "angreifen":
                self.kampf_am_ziel(eintrag)      # W7: der echte Kampf, bevor gebucht wird
            if eintrag.get("art") == "spionieren":
                # B-5 (02.11.2026): Wall-Abwehr pruefen und den Bericht ins Postfach legen -
                # ebenfalls VOR der Buchung, weil ein abgeprallter Auftrag seine Verluste selbst
                # setzt und nur der Rest heimkehrt.
                self.spionage_am_ziel(eintrag)
            # F-01/F-09: gebucht wird in der QUELLE des Auftrags (`quelle_id`), nicht im Reich.
            # Alte Auftraege ohne Quelle behalten den bisherigen Weg ueber den Reichsbestand.
            quelle = self._siedlung_zu(eintrag.get("quelle_id"))
            if quelle is not None:
                vorher = {"ressourcen": dict(quelle.vorraete or {}),
                          "einheiten": dict(quelle.einheiten or {})}
            else:
                vorher = {"ressourcen": {k: v.amount for k, v in self.resources.items()},
                          "einheiten": {k: u.count for k, u in self.units.items()}}
            neu = auftraege.spieldaten_anwenden(vorher, eintrag)
            # Echter Fund beim Ökonomie-Paket, Schritt 9 (Teil 2, 05.10.2026): ein STATIONIERENDER
            # Auftrag verlor seine Truppe ZWEIMAL. `auftrag_starten` nimmt die Einheiten schon beim
            # Start aus dem Bestand (Z. 836, „sie sind ab jetzt unterwegs"); der Auftragskern zieht
            # für die Art „stationieren" bei der Ankunft noch einmal ab (sein Vertrag, in
            # tests/test_auftraege.py belegt: Eingabe „Kämpfer 2" -> 0). Hier wird der Kern-Abzug
            # deshalb aufgehoben: die Truppe bleibt am Ziel, sie geht genau EINMAL ab.
            if eintrag.get("art") == "stationieren":
                neu["einheiten"] = dict(vorher["einheiten"])
            if quelle is not None:
                quelle.vorraete = {k: round(float(v), 2) for k, v in (neu.get("ressourcen") or {}).items()}
                quelle.einheiten = {k: int(v) for k, v in (neu.get("einheiten") or {}).items()
                                    if int(v) > 0}
                self._reichsanzeige_aus_orten()
            else:
                for stoff, menge in (neu.get("ressourcen") or {}).items():
                    if stoff in self.resources:
                        self.resources[stoff].amount = float(menge)
                for name, anzahl in (neu.get("einheiten") or {}).items():
                    if name in self.units:
                        self.units[name].count = max(0, int(anzahl))
            bericht = auftraege.bericht(eintrag)
            self.messages.append({"text": bericht["titel"] + "\n" + "\n".join(bericht["zeilen"]),
                                  "type": "auftrag"})
            ergebnis["neu"].append(bericht["titel"])

        for eintrag in self.auftraege:
            # Ein eigener Transport bringt seine Karren in den ORTSLAGER zurück (oben gebucht),
            # NICHT in den Reichsbestand — sonst stünde dieselbe Truppe zweimal. Für einen
            # Fremdvertrag (Teil 7b) gilt dasselbe: die Handelskarawane kommt über
            # `handel_abschluss` in das Ortslager des Käufers zurück.
            if eintrag.get("eigentransport") or eintrag.get("fremdvertrag"):
                continue
            if eintrag.get("status") != "abgeschlossen" or eintrag.get("heimgekehrt"):
                continue
            eintrag["heimgekehrt"] = True
            if eintrag.get("art") == "stationieren":
                continue                      # bleibt am Ziel: kommt nicht heim
            # F-01/F-09: die Ueberlebenden kehren in den ORT zurueck, aus dem sie kamen.
            zurueck = self.einsatz_zurueck(eintrag.get("quelle_id"),
                                           eintrag.get("einheiten") or {})
            for name, anzahl in zurueck.items():
                ergebnis["heimgekehrt"][name] = ergebnis["heimgekehrt"].get(name, 0) + int(anzahl)
        self.auftraege[:] = [e for e in self.auftraege
                             if not (e.get("status") == "abgeschlossen" and e.get("heimgekehrt"))]
        return ergebnis

    def spionage_am_ziel(self, eintrag: dict) -> dict:
        """Spionage am Ziel: Wall-Abwehr pruefen, dann Bericht ins Postfach ODER Verluste (B-5).

        VORGABE Daniel 02.11.2026: "dann benoetigt es eine gewisse schlagkraft von spionageinheiten
        um einen wall zu ueberwinden und auszuspionieren" - dieselbe Mechanik wie die Wall-Vorrunde
        im Kampf (`kampfbericht.vorrunde`). Entschieden wird hier, bei der ANKUNFT: der Wall kann
        sich seit dem Absenden geaendert haben (dieselbe Begruendung wie Entscheidung 8 vom
        31.10.2026 fuer den Angriff).

        Zwei Ausgaenge:
          * ueberwunden - `spionage.bericht_nachricht` legt den Bericht ins Postfach; wie viel er
            zeigt, entscheidet der Aufklaerungswert der mitgeschickten Spionageeinheiten;
          * abgeprallt - kein Bericht, die Truppe verliert den Anteil aus `data/spionage.json`,
            und die Nachricht nennt ausdruecklich, was fehlt und wie viel Aufklaerung gefehlt hat.
        """
        ziel = eintrag.get("ziel") if isinstance(eintrag.get("ziel"), dict) else {}   # Zielangaben
        bot_name = str(ziel.get("bot_name") or "")                                  # Bot des Dorfes
        dorf_name = str(ziel.get("dorf_name") or ziel.get("name") or "")             # Name des Dorfes
        zeit = float(eintrag.get("ankunft") or self.spielsekunden)                   # Spielzeit der Ankunft
        bot = next((b for b in self.bots if str(b.name) == bot_name), None)          # den Bot suchen
        if bot is None:                                                             # Bot verschwunden
            meldung = ("Spionagebericht nicht erstellt: Bot '%s' ist nicht mehr vorhanden."
                       % (bot_name or "unbekannt"))
            self.messages.append({"text": meldung, "type": "spionage", "spielzeit_sekunden": zeit})
            self._log(meldung)
            return {"bestanden": False, "grund": meldung}
        dorf = next((d for d in bot_doerfer_sicherstellen(bot)                       # Doerfer des Bots
                     if str(d.name) == dorf_name), None)                            # das gesuchte Dorf
        if dorf is None:                                                            # Dorf verschwunden
            meldung = ("Spionagebericht nicht erstellt: Dorf '%s' gehoert nicht mehr zu %s."
                       % (dorf_name or "unbekannt", bot.name))
            self.messages.append({"text": meldung, "type": "spionage", "spielzeit_sekunden": zeit})
            self._log(meldung)
            return {"bestanden": False, "grund": meldung}

        aufklaerung = int(eintrag.get("aufklaerung") or 0)                           # Wert der Truppe
        pruefung = spionage.abwehr_pruefung(aufklaerung, dorf.wall_stufe,             # Wall-Abwehr
                                            dorf.wall_zustand)
        eintrag["abwehr"] = pruefung                                                # Beleg am Auftrag
        if not pruefung.get("bestanden"):                                           # abgeprallt
            vorher = {str(n): int(a) for n, a in (eintrag.get("einheiten") or {}).items()}
            rest = spionage.verlust_der_truppe(vorher)                              # Anteil bleibt
            verluste = {n: int(a) - int(rest.get(n, 0)) for n, a in vorher.items()
                        if int(a) - int(rest.get(n, 0)) > 0}                        # was fehlt
            eintrag["einheiten"] = rest                                             # nur der Rest kehrt heim
            eintrag["abgewehrt"] = True                                             # Merker fuer den Bericht
            eintrag["verluste"] = verluste                                          # Verluste am Auftrag
            text = ("Spionage abgewehrt: %s\n%s\nVerluste: %s. Es gibt KEINEN Bericht - Wallstufe, "
                    "Taktik, Truppen und Vorraete bleiben verdeckt. Ein staerkerer Trupp "
                    "Spionageeinheiten (hoehere Werte SI und HE) schafft den Wall."
                    % (dorf.name, str(pruefung.get("grund") or ""),
                       hilfen.aufzaehlung(verluste)))
            self.messages.append({"text": text, "type": "spionage", "spielzeit_sekunden": zeit})
            self._log("Spionage auf %s abgewehrt (Aufklaerung %d, Abwehr %d)."
                      % (dorf.name, aufklaerung, int(round(pruefung.get("erforderlich") or 0))))
            return pruefung

        bericht = self.bot_dorf_spionagebericht(bot, str(dorf.name), zeit)           # der Bericht
        nachricht = spionage.bericht_nachricht(bericht, aufklaerung)                # die Nachricht
        self.messages.append(nachricht)                                             # ab ins Postfach
        self._log("Spionagebericht fuer %s eingegangen (Aufklaerung %d)."
                  % (dorf.name, aufklaerung))
        return pruefung

    def kampf_am_ziel(self, eintrag: dict, bot_objekt=None) -> dict:
        """Den echten Kampf am Ziel austragen (Handbuch S. 21-23) - W7, Schritt 7 abgeschlossen.

        `auftraege.py` rechnet nur Reisezeit und Beute; es erwartet `vorrunde` und `beute` als
        **Eingabe**. Hier wird deshalb mit `kampf.fuehre_schlacht` gekaempft: die gefallenen
        Einheiten gehen von den Auftrags-Einheiten ab (Heimkehrer sind also die Ueberlebenden),
        und die Beute des Gefechts wird in `eintrag['beute']` uebernommen. Gebucht wird sie
        gleich danach von `auftraege.spieldaten_anwenden` - also GENAU EINMAL.
        """
        ziel = eintrag.get("ziel") or {}
        # Ein ausdruecklich uebergebenes Bot-Objekt gilt als Ziel, auch wenn es (noch) nicht in
        # `self.bots` steht - so bucht der Pruefstand dieselben Gueter ab wie das Spiel.
        bot_ziel = (bot_objekt if isinstance(bot_objekt, BotPlayer) else
                    next((b for b in self.bots if b.name == ziel.get("bot_name")), None))
        # B-5 (02.11.2026): wird ein DORF angegriffen, gilt dessen Wall - nicht der des ganzen Bots.
        # Bis hierher nahm jeder Angriff `bot.wall_stufe`; mit den Dorf-Datensaetzen aus B-1 ist das
        # die falsche Ebene (jedes Dorf hat seinen eigenen Wall und Zustand).
        ziel_dorf = None
        if bot_ziel is not None and ziel.get("dorf_name"):
            ziel_dorf = next((d for d in bot_doerfer_sicherstellen(bot_ziel)
                              if str(d.name) == str(ziel.get("dorf_name"))), None)
        siedlung_ziel = next((ort for ort in self.settlements
                              if ort.id == ziel.get("id")), None) if ziel.get("id") else None
        # Reihenfolge: das ANGEGRIFFENE Dorf (B-5) vor dem Bot vor der Siedlung vor der Zielangabe.
        wall_stufe = (int(ziel_dorf.wall_stufe) if ziel_dorf is not None else
                      int(bot_ziel.wall_stufe) if bot_ziel else
                      self.wall_stufe_am_ort(siedlung_ziel) if siedlung_ziel
                      else int(ziel.get("wall_stufe") or 0))
        wall_zustand = (float(ziel_dorf.wall_zustand) if ziel_dorf is not None else
                        float(bot_ziel.wall_zustand) if bot_ziel else
                        dorfwall.zustand(siedlung_ziel) if siedlung_ziel
                        else float(ziel.get("wall_zustand_prozent", 100.0)))
        ziel_def = (dict(bot_ziel.army) if bot_ziel else
                    dict(siedlung_ziel.einheiten) if siedlung_ziel
                    else dict(ziel.get("verteidiger") or {}))
        truppen = {str(k): int(v) for k, v in (eintrag.get("einheiten") or {}).items()}
        kaempfer, belagerung, karren = {}, {}, {}
        for name, anzahl in truppen.items():
            rolle = einheiten.rolle(name)
            if rolle in ("kaempfer", "kundschafter"):
                kaempfer[name] = anzahl
            elif rolle == "belagerung":
                belagerung[name] = anzahl
            elif rolle == "karren":
                karren[name] = anzahl
        geraet = dict(karren)
        geraet.update(belagerung)          # kampf.py: Karren UND Belagerungswaffen des Angreifers

        ergebnis = kampf.fuehre_schlacht(
            kaempfer, ziel_def,
            wall_stufe, wall_zustand,
            angreifer_karren=geraet or None,
            verteidiger_karren=dict(ziel.get("verteidiger_karren") or {}) or None,
            vorraete=dict(ziel.get("vorraete") or {}), rng=random.Random(),
            forschung_angreifer={k: int(v.level) for k, v in self.research.items()},
            forschung_verteidiger=({k: int(v.level) for k, v in self.research.items()}
                                   if siedlung_ziel is not None else None),
            # V-5 (03.11.2026): Volksboni beider Seiten. Der Spieler traegt sein Volk, der
            # verteidigende Bot Volk + Taktik (bottaktik.modifikatoren, additiv).
            boni_angreifer=boni.kampf_werte(boni.modifikatoren(
                str(getattr(self, "spieler_fraktion", "") or ""))),
            boni_verteidiger=(boni_fuer_bot(bot_ziel, float(self.spielsekunden))
                              if bot_ziel is not None
                              else (boni_fuer_ort(siedlung_ziel) if siedlung_ziel is not None
                                    else None)))

        # Ortsbezogener Mauerschaden nach der wirklichen Belagerung, persistent.
        if siedlung_ziel is not None and self._lokale_kasse_aktiv():
            siedlung_ziel.mauer_zustand = float(ergebnis.get("mauer_zustand", wall_zustand))
        if bot_ziel is not None:
            bot_ziel.wall_zustand = float(ergebnis.get("mauer_zustand", wall_zustand))
        verteidiger = siedlung_ziel.einheiten if siedlung_ziel else (bot_ziel.army if bot_ziel else None)
        if verteidiger is not None:
            for name, anzahl in (ergebnis.get("verluste_verteidiger") or {}).items():
                verteidiger[name] = max(0, int(verteidiger.get(name, 0)) - int(anzahl))
        for name, anzahl in (ergebnis.get("verluste_angreifer") or {}).items():
            rest = int(truppen.get(name, 0)) - int(anzahl)
            if rest > 0:
                truppen[name] = rest
            else:
                truppen.pop(name, None)
        for name in (ergebnis.get("geraete_verloren") or []):
            rest = int(truppen.get(name, 0)) - 1
            if rest > 0:
                truppen[name] = rest
            else:
                truppen.pop(name, None)
        eintrag["einheiten"] = truppen
        # Beute: EINE Formel (`kampfbericht.beute_am_ziel`) fuer Bot-Pfad, Auftrags-Pfad und
        # Direktangriff - und sie bucht beim Ziel ab. Vorher stand hier die Beute aus
        # `kampf._beute` (nur Ladungsgrenze, ohne Staffelung) und das Ziel behielt alles.
        # Das war der Befund Nr. 6 der externen Gegenpruefung vom 31.10.2026.
        # B-3 (02.11.2026): die Kasse eines Bots ist eine Eigenschaft (Summe der Doerfer). Ein
        # `clear()/update()` darauf wuerde in einer KOPIE landen - die Beute kaeme aus dem Nichts.
        # Deshalb wird der Bot-Lagerstand ueber `bot_kasse_setzen` zurueckgebucht, nie direkt.
        vorraete_ziel = (bot_kasse(bot_ziel) if bot_ziel is not None else
                         siedlung_ziel.vorraete if siedlung_ziel is not None else
                         ziel.get("vorraete") if isinstance(ziel.get("vorraete"), dict) else {})
        uebrig = int(sum(max(0, int(v)) for v in (verteidiger or {}).values()))
        beute_gefecht, lager_danach = kampfbericht.beute_am_ziel(
            geraet, dict(vorraete_ziel or {}), ausgang=ergebnis.get("ausgang"),
            wall_zustand_vor=wall_zustand, verteidiger_uebrig=uebrig,
            forschung=self.forschungs_stufen())
        if beute_gefecht and vorraete_ziel is not None:
            if bot_ziel is not None:                                      # Ziel ist ein BOT
                bot_kasse_setzen(bot_ziel, lager_danach)                  # Abzug auf die Doerfer buchen
            else:                                                         # Ziel ist eine Siedlung
                vorraete_ziel.clear()                                     # eigenes Lager leeren
                vorraete_ziel.update(lager_danach)                        # und den Rest setzen
        eintrag["beute"] = beute_gefecht
        eintrag["vorrunde"] = {"bestanden": bool(ergebnis.get("vorrunde_bestanden")),
                               "grund": ergebnis.get("bericht", "")}

        bericht = kampfbericht.bericht(ergebnis)
        self.messages.append({"text": f"Am Ziel {eintrag.get('nach')} — " + bericht["titel"] +
                                      "\n" + "\n".join(bericht["zeilen"]), "type": "kampf",
                              "spielzeit_sekunden": float(eintrag.get("ankunft") or self.spielsekunden)})
        self._log(f"Kampf am Ziel {eintrag.get('nach')}: {ergebnis.get('ausgang')}.")
        return ergebnis

    def forschung_stand(self) -> Dict[str, Dict[str, object]]:
        """Der Stand, mit dem `src/forschung.py` rechnet — aus EINER Wahrheit gebaut.

        `self.research[...].level` ist die Stufe. Seit Teil 6 (Rest) steht der **laufende Auftrag**
        im ORT (`Settlement.forschungsauftrag`) — Entwurf Z. 779: „lokale Bibliothek, lokale
        Mittel, globales Wissen". Hier werden die Aufträge der Orte eingesammelt, damit es keine
        zweite Auftrags-Wahrheit gibt. Ein Spielstand von vor Teil 6 traegt seine Auftraege noch in
        `self.forschungsauftraege`; `load` zieht sie in den ersten Ort um.
        """
        auftraege: Dict[str, dict] = {}
        for siedlung in self.settlements:
            a = getattr(siedlung, "forschungsauftrag", None)
            if a and a.get("gebiet"):
                auftraege[a["gebiet"]] = a
        return {k: {"stufe": int(v.level), "auftrag": auftraege.get(k)}
                for k, v in self.research.items()}

    # `forschung_fortschreiben` (der reichsweite Altpfad, W4c) ist WEG: die Forschung laeuft seit
    # Teil 6 ueber die Spieluhr der ORTE (`spieloekonomie.forschung_abschluss` in `tick`). Zwei
    # Wege fuer dieselbe Stufe waeren eine zweite fuehrende Wahrheit (Entwurf Z. 774) — und die
    # Kosten kaemen aus dem falschen Lager.

    def _forschung_abschluss_buchen(self, wissen: Dict[str, int]) -> List[str]:
        """Gestiegene Forschungsstufen aus dem Kern in den Spielstand uebernehmen (Teil 6 Rest).

        `spieloekonomie.forschung_abschluss` hebt die Stufe nur nach oben (`max`) und loescht den
        Auftrag im Ort; hier wird sie an `self.research` geschrieben und gemeldet. Rueckgabe: die
        gestiegenen Gebiete (fuer die Meldung an der Oberflaeche).
        """
        gestiegen: List[str] = []
        for gebiet, stufe in (wissen or {}).items():
            eintrag = self.research.get(gebiet)
            if eintrag is None or int(stufe) <= int(eintrag.level):
                continue
            eintrag.level = int(stufe)
            gestiegen.append(gebiet)
            meldung = f"Forschung {eintrag.name} auf Stufe {stufe} abgeschlossen."
            self._log(meldung)
            self.messages.append({"text": meldung, "type": "forschung"})
        return gestiegen

    # ---------------- W5: Bots (src/botkern.py) ----------------

    def bot_als_dict(self, bot: BotPlayer) -> Dict[str, object]:
        """Der Bot in der Form, mit der `src/botkern.py` rechnet — aus EINER Quelle.

        Die Werte kommen aus dem `BotPlayer`; der Bot-Kern veraendert die dicts nicht (reine
        Funktionen), `bot_aus_dict` schreibt das Ergebnis zurueck.
        """
        return {"id": bot.name, "name": bot.name, "fraktion": bot.faction,
                "aggression": float(bot.aggression), "trading": float(bot.trading),
                "temperament": float(bot.temperament), "punkte": int(bot.punkte),
                "ruf": int(bot.ruf), "vorraete": dict(bot.vorraete), "lager": dict(bot.lager),
                "armee": dict(bot.army), "letzter_angriff": bot.letzter_angriff,
                "naechster_angriff": float(bot.naechster_angriff), "angriffe": int(bot.angriffe),
                "gebaut": int(bot.gebaut), "geforscht": int(bot.geforscht),
                "gehandelt": int(bot.gehandelt), "wall_stufe": int(bot.wall_stufe),
                "wall_zustand": float(bot.wall_zustand),
                # S-7 (bottaktik): der Verhaltenszustand in der dict-Form des Kerns.
                "zustand": str(bot.zustand), "gedaechtnis": dict(bot.gedaechtnis),
                "marsch_ankunft": float(bot.marsch_ankunft),
                "flucht_ende": float(bot.flucht_ende),
                "letzter_abstand": bot.letzter_abstand,
                "naechster_marsch_h": bot.naechster_marsch_h,
                "wechsel_sperre_bis": float(bot.wechsel_sperre_bis),
                "volksattribute": dict(bot.volksattribute),
                "verhaltensbonus": dict(bot.verhaltensbonus)}

    def bot_aus_dict(self, bot: BotPlayer, daten: dict) -> None:
        """Zurueck in den Spielstand: nur die Felder, die der Bot-Kern fuehrt."""
        if not isinstance(daten, dict):
            return
        bot.vorraete = {str(k): int(v) for k, v in (daten.get("vorraete") or {}).items()}
        bot.lager = {str(k): int(v) for k, v in (daten.get("lager") or {}).items()}
        bot.naechster_angriff = float(daten.get("naechster_angriff") or 0.0)
        bot.letzter_angriff = daten.get("letzter_angriff")
        bot.angriffe = int(daten.get("angriffe") or 0)
        bot.gebaut = int(daten.get("gebaut") or 0)
        bot.geforscht = int(daten.get("geforscht") or 0)
        bot.gehandelt = int(daten.get("gehandelt") or 0)
        # S-7 (bottaktik): der Verhaltenszustand kommt aus derselben dict-Form zurueck.
        bot.zustand = str(daten.get("zustand") or "")
        _ged = daten.get("gedaechtnis")
        bot.gedaechtnis = dict(_ged) if isinstance(_ged, dict) else {}
        bot.marsch_ankunft = float(daten.get("marsch_ankunft") or 0.0)
        bot.flucht_ende = float(daten.get("flucht_ende") or 0.0)
        bot.letzter_abstand = daten.get("letzter_abstand")
        bot.naechster_marsch_h = daten.get("naechster_marsch_h")
        bot.wechsel_sperre_bis = float(daten.get("wechsel_sperre_bis") or 0.0)
        _volk = daten.get("volksattribute")
        bot.volksattribute = dict(_volk) if isinstance(_volk, dict) else {}
        _bonus = daten.get("verhaltensbonus")
        bot.verhaltensbonus = dict(_bonus) if isinstance(_bonus, dict) else {}

    def bot_vorrat_anlegen(self, bot: BotPlayer) -> None:
        """Startvorräte und Wagenpark eines Bots anlegen.

        Die Spannen sind VORSCHLAG (`botkern.VORSCHLAG_START_VORRAETE`; die Vorlage nennt kein
        Bot-Inventar). Zusaetzlich bekommt der Bot die BELEGTEN Startwerte des Spielers
        (Handbuch S. 7: 10 Siedler, 100 Holz, 100 Steine) — ohne sie koennte er keine einzige
        Einheit bezahlen, weil die belegten Preise Siedler nennen.
        """
        if not bot_kasse(bot):                                            # noch keine Kasse vorhanden
            rng = random.Random(f"nebel-bot-vorrat-{bot.name}")           # fester Zufall je Bot
            bot.vorraete = {stoff: rng.randint(lo, hi)                    # Setter verteilt auf die Doerfer
                            for stoff, (lo, hi) in botkern.VORSCHLAG_START_VORRAETE.items()}
        for stoff, menge in (("siedler", 10), ("holz", 100), ("stein", 100)):   # belegte Startwerte
            if stoff not in bot_kasse(bot):                               # fehlt dieser Stoff noch?
                bot_kasse_buchen(bot, stoff, menge)                       # dann ueber die EINE Buchstelle
        if not bot.lager:
            rng = random.Random(f"nebel-bot-lager-{bot.name}")
            karren = sorted((n for n in einheiten.namen()
                             if einheiten.ist_transport(n) and einheiten.ladung(n) > 0),
                            key=lambda n: einheiten.ladung(n))
            if karren:
                bot.lager = {karren[0]: rng.randint(0, int(botkern.VORSCHLAG_START_KARREN[1]))}

    def bot_armee_aufstellen(self, bot: BotPlayer) -> Optional[str]:
        """Der Bot stellt EINE Einheit auf, die er aus SEINEN Vorräten bezahlen kann.

        Die Preise sind BELEGT (`data/units.json`, `einheiten.alle()[name]['kosten']`), bezahlt
        wird aus `bot.vorraete`. Frueher stand hier eine erfundene Armee von **20-120 Stueck je
        Einheit** — damit war ein Bot-Angriff aussichtslos. VORSCHLAG ist nur die Reihenfolge
        (Kaempfer vor Kundschaftern) und dass ein Bot wie auf einem Markt kauft.

        Rueckgabe: Name der aufgestellten Einheit oder ``None``.
        """
        # Daniel 03.11.2026 (S-2): Kaufbremse - aufgestellt wird nur, solange das Lager den
        # Tagesbedarf der Armee PLUS Reserve deckt. Steht die Armee in Unterdeckung, ist hier
        # Schluss (Kaufstopp); der Nachschub ist S-7. Die Rechnung selbst steht in
        # `bot_nahrung_deckt`/`bot_reserve_nahrung` - hier wird nur gefragt, nicht gerechnet.
        if not bot_nahrung_deckt(bot, 1):
            return None
        for name in sorted(einheiten.namen(), key=lambda n: (einheiten.rolle(n) != "kaempfer", n)):
            if einheiten.rolle(name) not in ("kaempfer", "kundschafter"):
                continue
            rohkosten = einheiten.alle()[name].get("kosten") or {}
            kosten = {str(k): int(v) for k, v in rohkosten.items()}
            if not kosten:                                                # ohne Preis keine Zahl erfinden
                continue
            # S-3 (03.11.2026): Siedler sind MENSCHEN, keine Ware. Sie stehen in `bevoelkerung`
            # des Dorfes (vorher lagen sie als Rohstoff im Lager - zwei Stellen fuer dieselbe
            # Groesse). Gekauft wird im Hauptdorf, wo die Armee steht.
            doerfer = bot_doerfer_sicherstellen(bot)                      # Doerfer in einer Form
            haupt = doerfer[0] if doerfer else None                       # das Hauptdorf traegt die Armee
            siedler = int(kosten.pop("siedler", 0))                       # Siedler aus der Bevoelkerung
            if siedler and (haupt is None or float(haupt.bevoelkerung) < siedler):
                continue                                                  # zu wenig Siedler im Hauptdorf
            if not all(bot.vorraete.get(k, 0) >= v for k, v in kosten.items()):
                continue                                                  # Rohstoffe muessen reichen
            for stoff, menge in kosten.items():
                # B-3: gebucht wird auf die DOERFER (eine Buchstelle), nicht auf ein zweites Lager.
                bot_kasse_buchen(bot, stoff, -menge)                      # Kosten abbuchen
            if siedler:                                                   # Siedler gehen vom Hauptdorf
                haupt.bevoelkerung = round(float(haupt.bevoelkerung) - siedler, 2)
            bot.army[name] = bot.army.get(name, 0) + 1                    # Einheit dazustellen
            return name                                                   # fertig
        return None                                                       # nichts bezahlbar

    def bots_fortschreiben(self, jetzt: float) -> dict:
        """Einen Bot-Zug fahren (W5): die Entscheidung kommt aus `botkern`, gebucht wird hier.

        `welt['vorraete']` sind UNSERE Lager: greift ein Bot an, nimmt er davon 50 %, gedeckelt
        durch seinen eigenen Wagenpark (ENTWURF, Abschnitt Bot-KI). Was er nimmt, geht hier
        **genau einmal** ab. `welt['referenzpreis']` ist der belegte Handelspreis
        (Beschaffungskosten x 1,2). Der Zug laeuft nur alle `BOT_TAKT_SEKUNDEN`.
        """
        ergebnis = {"bots": 0, "takt": BOT_TAKT_SEKUNDEN, "aktionen": {}, "angriffe": []}
        if not self.bots:
            return ergebnis
        # S-13 (03.11.2026, Daniels Entscheidung 3): Der Zug haengt an einem FESTEN Spielzeit-Punkt,
        # nicht an der Differenz `jetzt - letzter`. Frueher entschied die Fliesskomma-Summe, ob ein
        # Takt ueberhaupt feuert: 1 x 3600 s und 10 x 360 s auf dieselbe Spielzeit fuhren
        # unterschiedlich viele Bot-Aktionen (gemessen an `test_gpt_fixrunde_ortslager_zeit` und
        # `test_gpt_frischstart`, sobald der Diebstahl das Spielerlager beruehrt).
        jetzt = float(jetzt)                                              # Spielzeit in Sekunden
        if not math.isfinite(jetzt):                                      # keine echte Spielzeit
            return ergebnis                                               # dann kein Zug
        letzter = float(getattr(self, "_letzter_bot_takt", 0.0) or 0.0)    # zuletzt gefahrener PUNKT
        punkt = math.floor(jetzt / BOT_TAKT_SEKUNDEN) * BOT_TAKT_SEKUNDEN  # der faellige feste Punkt
        if punkt <= letzter:                                              # dieser Punkt ist gefahren
            return ergebnis                                               # dann kein zweiter Zug
        self._letzter_bot_takt = punkt                                    # Punkt als gefahren merken
        ergebnis["punkt"] = punkt                                         # Nachweis: WANN der Zug lief
        ergebnis["bots"] = len(self.bots)

        # B-3 (02.11.2026): VOR dem Zug wirtschaften die Doerfer. Jedes Dorf erntet seit seiner
        # letzten Ernte (`dorf.ernte_seit`) mit dem Stundensatz aus `bot_dorf_ertrag` - derselben
        # Funktion, die der Spionagebericht zeigt. Ohne diesen Schritt haette ein Bot nur seine
        # Startvorrate und koennte nach dem ersten Einkauf nie wieder etwas bezahlen.
        ernte: Dict[str, float] = {}                                      # was alle Doerfer zusammen ernteten
        for bot in self.bots:                                             # je Bot seine Doerfer
            for stoff, menge in bot_doerfer_ernten(bot, jetzt).items():    # Ernte dieses Bots
                ernte[stoff] = round(ernte.get(stoff, 0.0) + menge, 2)    # aufsummieren
        ergebnis["ernte"] = ernte                                         # fuer Pruefung und Protokoll

        rng = random.Random()
        welt = {"vorraete": {k: int(v.amount) for k, v in self.resources.items()},
                "referenzpreis": botkern.referenzpreis_aus_beschaffung(BOT_BESCHAFFUNGSKOSTEN)}
        daten = [self.bot_als_dict(b) for b in self.bots]
        stand = botkern.bots_tick(daten, welt, jetzt, rng)
        ergebnis["aktionen"] = dict(stand.get("aktionen") or {})

        # GPT-B01: `botkern` plant nur die ABSICHT. Erfolg, Beute und Meldung
        # duerfen erst nach tatsaechlichem Kampf entschieden werden. Keine
        # irrefuehrenden "erbeutet"-Logzeilen aus dem Bot-Absichtskern.
        # GPT-B02: botkern.bots_tick SORTIERT die Ergebnisse nach Namen.
        # `zip(daten, ergebnisse)` wuerde daher einem fremden Bot dessen
        # Angriff, Wartezeit und Beute zubuchen. Ausschliesslich nach der
        # eindeutigen Bot-Kennung zuordnen; keinen stillen Positional-Fallback.
        start_nach_name = {str(d['name']): d for d in daten}
        bot_nach_name = {b.name: b for b in self.bots}
        for zug in stand.get("ergebnisse") or []:
            name = str(zug.get('bot') or '')
            bot = bot_nach_name.get(name)
            start = start_nach_name.get(name)
            if bot is None or start is None:
                continue
            meldung = str(zug.get("meldung") or "")
            if zug.get("aktion") == "angreifen":
                beute = {}
                if ausgabemodus.ist_oeffentliche_testversion():
                    # S-7 Demo-Regel (Daniel 01.11.2026): in der oeffentlichen
                    # Testversion greifen Bots NICHT an. Das sichtbare Verhalten
                    # (bottaktik) bleibt davon unberuehrt.
                    meldung = f"{bot.name}: Angriff in der Demo nicht freigeschaltet."
                    zug.setdefault("wirkung", {})["angriff_verschoben"] = "Demo"
                elif self.noob_protection:
                    meldung = f"{bot.name}: Angriff abgebrochen (Goetterschutz)."
                else:
                    bot_kaempfer = {n: int(v) for n, v in bot.army.items()
                                     if einheiten.rolle(n) in ("kaempfer", "kundschafter")
                                     and int(v) > 0}
                    bot_geraet = {n: int(v) for n, v in bot.army.items()
                                  if einheiten.rolle(n) == "belagerung" and int(v) > 0}
                    bot_geraet.update({n: int(v) for n, v in (bot.lager or {}).items()
                                      if einheiten.rolle(n) == "karren" and int(v) > 0})
                    zielort, zielplan = bot_angriffsplanung.waehle_ziel(
                        self.settlements, bot_kaempfer, bot_geraet,
                        lambda ort: (self.wall_stufe_am_ort(ort),
                                     dorfwall.zustand(ort) if self._lokale_kasse_aktiv()
                                     else 100.0))
                    if zielort is None:
                        meldung = (f"{bot.name}: Angriff verschoben: "
                                   f"{zielplan['grund']}")
                    else:
                        ws = self.wall_stufe_am_ort(zielort)
                        wz = (dorfwall.zustand(zielort)
                              if self._lokale_kasse_aktiv() else 100.0)
                        # Goetterschutz, eingeschraenkt (belegt: Handbuch 2009, Seite 6;
                        # Registerpunkt 41): anwendbar, SEIT die Bot-Punkte aus der belegten
                        # Formel kommen (`botkern.bot_punkte`). Der volle 7-Tage-Schutz bleibt
                        # `self.noob_protection`; hier geht es um die Grenze 299 und das Band
                        # +/- 20 Prozent. Ein Angriff ueber die Grenze ist in KEINE Richtung
                        # moeglich - auch nicht von einem Bot aus.
                        _erlaubt, _grund = punkte.angreifbar(
                            int(bot.punkte), int(self.punktestand()["gesamt"]))
                        if not _erlaubt:
                            meldung = (f"{bot.name}: Angriff auf {zielort.name} verschoben - "
                                       f"{_grund}")
                            zug.setdefault("wirkung", {})["angriff_verschoben"] = _grund
                        else:
                            kampf_result = kampf.fuehre_schlacht(
                                bot_kaempfer, dict(zielort.einheiten), ws, wz,
                                angreifer_karren=bot_geraet or None,
                                vorraete=dict(zielort.vorraete), rng=rng,
                                forschung_verteidiger={k: int(v.level) for k, v in self.research.items()},
                                # V-5: Angreifer = Bot (Volk + Taktik), Verteidiger = Spielerort (Volk).
                                boni_angreifer=boni_fuer_bot(bot, float(self.spielsekunden)),
                                boni_verteidiger=boni_fuer_ort(zielort))
                            if self._lokale_kasse_aktiv():
                                zielort.mauer_zustand = float(kampf_result.get("mauer_zustand", wz))
                            for name, menge in (kampf_result.get("verluste_angreifer") or {}).items():
                                bot.army[name] = max(0, int(bot.army.get(name, 0)) - int(menge))
                            for name, menge in (kampf_result.get("verluste_verteidiger") or {}).items():
                                zielort.einheiten[name] = max(
                                    0, int(zielort.einheiten.get(name, 0)) - int(menge))
                            if kampf_result.get("ausgang") == "angreifer":
                                # VORGABE Daniel 31.10.2026 (Registerpunkt 45): gestaffelte Beute -
                                # Wallzustand VOR dem Kampf und die ueberlebenden Verteidiger entscheiden
                                # ueber den Anteil; Ladung und Vorrat begrenzen ihn zusaetzlich.
                                # EINE Formel fuer alle drei Pfade: kampfbericht.beute_am_ziel
                                # (rechnet UND bucht beim Ziel ab).
                                _uebrig = int(sum(max(0, int(v)) for v in zielort.einheiten.values()))
                                beute, _lager_danach = kampfbericht.beute_am_ziel(
                                    bot_geraet or {}, dict(zielort.vorraete),
                                    ausgang="angreifer", wall_zustand_vor=wz, verteidiger_uebrig=_uebrig,
                                    forschung=self.forschungs_stufen())
                                if beute:
                                    zielort.vorraete.clear()
                                    zielort.vorraete.update(_lager_danach)
                                self._reichsanzeige_aus_orten()
                            meldung = (f"{bot.name} gegen {zielort.name}: "
                                       f"{kampf_result.get('ausgang')}; "
                                       f"tatsaechliche Beute {beute}.")
                            self.messages.append({"text": meldung, "type": "kampf"})
                zug.setdefault("wirkung", {})["beute"] = beute
                ergebnis["angriffe"].append(meldung)
            self._log(meldung)
            # `bot_aus_dict` darf nie mit der vom Kern nur PROGNOSTIZIERTEN
            # Beute gefuettert werden. Auch nach einer Schlacht gilt nur die
            # durch `kampf.fuehre_schlacht` bestaetigte Menge.
            self.bot_aus_dict(bot, botkern.wirkung_anwenden(start, zug))
            self.bot_armee_aufstellen(bot)

        # S-12 (03.11.2026, Daniels Entscheidung 7): duenne Bots bestehlen einen WEHRLOSEN Ort des
        # Spielers - jeder Fall als Postfach-Nachricht (wer, wann, was, wieviel), kein stiller
        # Verlust. Ein Ort MIT Garnison wird nicht bestohlen; dort greift der Angriffsweg.
        # S-12 (03.11.2026): Die Verdrahtung ist VORBEREITET, aber NICHT eingeschaltet -
        # `data/bot_diebstahl.json` steht auf "aktiv": false. Grund, gemessen: der Bot-Takt feuert
        # je BOT_TAKT_SEKUNDEN, und ob er in einer Zeitspanne genau einmal feuert, haengt am
        # Fliesskomma der Summierung (1 x 3600 gegen 10 x 360). Sobald der Diebstahl das Lager des
        # Spielers beruehrt, laufen dadurch zwei gleiche Spielzeiten auseinander
        # (`test_gpt_fixrunde_ortslager_zeit`: 98,79 gegen 105,0; `test_gpt_frischstart` ebenso).
        # Der Diebstahl braucht deshalb erst ein eigenes, scheiben-unabhaengiges Zeitmodell.
        einst_dieb = bot_diebstahl_einstellungen()
        diebstaehle: List[dict] = []
        # S-7 Demo-Regel (Daniel 01.11.2026) gilt auch hier: in der oeffentlichen Testversion greifen
        # die Bots NICHT an - ein Diebstahl ist ein Angriff auf das Lager des Spielers, also bleibt er
        # dort ebenfalls aus. Sonst waere die Demo-Regel an einer zweiten Stelle still umgangen.
        # GOETTERSCHUTZ (Handbuch 2009, S. 6; Entscheidung 3 vom 01.11.2026): die ersten sieben Tage
        # ist der Spieler unangreifbar - das gilt fuer JEDEN Zugriff auf sein Lager, also auch fuer den
        # Diebstahl. Ohne diese Bedingung pluenderten die Bots einen Anfaenger, der laut Handbuch
        # geschuetzt ist (gefunden von `test_startspiel` Abschnitt 6: 10,64 Holz in 25 Zuegen).
        if (einst_dieb.get("aktiv", False) and not self.noob_protection
                and not ausgabemodus.ist_oeffentliche_testversion()):
            for bot_dieb in self.bots:
                for ort_dieb in self.settlements:
                    bericht_dieb = bot_diebstahl(bot_dieb, ort_dieb, jetzt, einst_dieb)
                    if bericht_dieb:
                        _nachricht = bot_diebstahl_nachricht(bericht_dieb)
                        self.messages.append(_nachricht)                 # ins Postfach
                        self._log(_nachricht["text"])                    # und ins Spiel-Log
                        diebstaehle.append(bericht_dieb)
            if diebstaehle:
                # Die Reichsanzeige ist eine ANZEIGE der Ortslager - ohne diese Zeile zeigten zwei
                # Stellen verschiedene Summen fuer denselben Bestand.
                self._reichsanzeige_aus_orten()
        ergebnis["diebstaehle"] = diebstaehle

        # S-7 (bottaktik): das SICHTBARE Verhalten je Bot. Der Zustandsautomat liefert
        # Zustand, Gedaechtnis, Marsch-/Fluchtzeit und den angekuendigten Wechsel. Gebucht
        # wird hier NUR das Verhalten - Kampf und Punkte bleiben im botkern-Pfad darueber
        # (keine zweite Entscheidungs- oder Kampfwahrheit). Zeitbasis ist `jetzt` (Spielzeit).
        spieler_ort = self.aktive_siedlung()
        welt_taktik = {"spielerdorf": ({"x": int(spieler_ort.x), "y": int(spieler_ort.y),
                                        "name": str(spieler_ort.name)}
                                       if spieler_ort is not None else None)}
        for bot in self.bots:
            if not bot.volksattribute:
                # Dauerhafte Volksattribute EINMALIG aus der Fraktion setzen (eine Quelle).
                bot.volksattribute = bottaktik.volksattribute({"fraktion": bot.faction})
            # B-2 (02.11.2026): je Dorf Position und Verhalten aus der Lage - mit Sperrzeit.
            self.bot_doerfer_auffrischen(bot, jetzt, spieler_ort)
            start_taktik = self.bot_als_dict(bot)
            zug_taktik = bottaktik.tick(start_taktik, welt_taktik, jetzt, rng)
            neu_taktik = bottaktik.wirkung_anwenden(start_taktik, zug_taktik, jetzt)
            ankuendigung = neu_taktik.pop("wechsel_ankuendigung", None)
            neu_taktik.pop("wechsel_blockiert", None)
            self.bot_aus_dict(bot, neu_taktik)
            if ankuendigung:
                # Der Wechsel wird genau EINMAL angekuendigt (hier, nicht je Zug).
                self.messages.append({"text": ankuendigung, "type": "bot"})
                self._log(ankuendigung)

        return ergebnis

    def _orte_abschnitt(self, ab: float, bis: float, wissen: dict,
                        eingetroffen: List[str]) -> dict:
        """Bucht EINEN Zeitabschnitt [ab, bis] auf die Orte und liefert den Wissensstand zurueck.

        Was hinein geht: Anfang und Ende des Abschnitts in Spielsekunden, der Forschungsstand
        `{Gebiet: Stufe}` und die Liste der fertig gewordenen Dinge (wird ergaenzt).
        Was heraus kommt: der ggf. gestiegene Wissensstand.
        Die Orte werden uebernommen, die Reichsanzeige nachgezogen und `self.spielsekunden` auf das
        Abschnittsende gestellt - so steht der Zustand GENAU auf dem Punkt, an dem der Bot danach
        handelt (S-13, Daniels Entscheidung 3 von heute). Vorher stand dieser Block einmal im Takt;
        er ist unveraendert hierher gezogen und wird jetzt je Abschnitt gefahren.
        """
        _vorher_orte = {}
        _schluessel33 = {}
        for _nr33, _s33 in enumerate(self.settlements):
            # Ein Ort OHNE Kennung (kommt in Prüfungen und Hilfsbauten vor) bekommt hier einen
            # Arbeitsplatz-Schlüssel. Wichtig: NICHT nach `id` filtern — sonst fiele so ein Ort
            # stillschweigend aus dem Takt (gefunden von den Wachen P27/P28 am 06.10.2026).
            _k33 = _s33.id or "__ort_ohne_kennung_%d" % _nr33
            _vorher_orte[_k33] = asdict(_s33)
            _schluessel33[_k33] = _s33
        _neu_orte, _keine_missionen, wissen, _zeit, _ereigniszeiten = spieloekonomie.tick_bis(
            _vorher_orte, [], wissen, ab, bis)
        for _kennung, siedlung in _schluessel33.items():
            _neu = _neu_orte.get(_kennung)
            if _neu is None:
                continue
            _alt = _vorher_orte.get(_kennung) or {}
            _vorher_vorrat = {k: float(v) for k, v in (_alt.get("vorraete") or {}).items()}
            _vorher_leute = float(_alt.get("bevoelkerung") or 0.0)
            _journal_vorher = len(_alt.get("fertigjournal") or [])
            if siedlung.id:
                if not self._ort_uebernehmen(siedlung.id, _neu):
                    continue
            else:
                # Ohne Kennung wird DIESER Gegenstand übernommen (über die Kennung könnte
                # `_ort_uebernehmen` den falschen Ort treffen — mehrere könnten leer sein).
                try:
                    _frisch = Settlement(**_neu)
                except TypeError:
                    continue
                if siedlung.__dict__ != _frisch.__dict__:
                    siedlung.__dict__.clear()
                    siedlung.__dict__.update(_frisch.__dict__)
            for _zeile in (_neu.get("fertigjournal") or [])[_journal_vorher:]:
                _was = (f"Forschung {_zeile.get('name')}" if _zeile.get("art") == "forschung"
                        else str(_zeile.get("name")))
                eingetroffen.append(f"{_was} in {siedlung.name}")
            for res, menge in (_neu.get("vorraete") or {}).items():
                zuwachs = float(menge) - _vorher_vorrat.get(res, 0.0)
                if (not self._lokale_kasse_aktiv() and abs(zuwachs) > 1e-12
                        and res in self.resources):
                    self.resources[res].amount = round(float(self.resources[res].amount) + zuwachs, 2)
            zuwachs_leute = float(_neu.get("bevoelkerung", 0.0)) - _vorher_leute
            if abs(zuwachs_leute) > 1e-12 and not self._lokale_kasse_aktiv():
                self.population = float(self.population) + zuwachs_leute
        self._reichsanzeige_aus_orten()
        # Gestiegene Forschungsstufen aus dem Kern in den Spielstand uebernehmen (Teil 6 Rest).
        self._forschung_abschluss_buchen(wissen)
        # Die Uhr steht genau auf dem Ende des Abschnitts (`tick_bis` liefert die erreichte Zeit).
        self.spielsekunden = _zeit
        return wissen

    def tick(self, dt_seconds: float):
        # Die monotone Laufzeituhr kann bei defektem Lieferanten oder einem
        # ungueltigen Tempo keine NaN/Inf-Spielsekunden erzeugen duerfen.
        dt_seconds = float(dt_seconds)
        if not math.isfinite(dt_seconds) or dt_seconds < 0:
            raise ValueError("Spielzeit muss endlich und nichtnegativ sein")
        # Ökonomie-Paket, Schritt 9, Teil 6b: EINE Uhr JE ORT — der Kern rechnet.
        #
        # `spieloekonomie.ort_tick` erntet (aus DERSELBEN Quelle wie die Anzeige,
        # `wirtschaft.ertrag_gesamt`), schreibt den Siedlerzuwachs bis zur Grenze des Ortes fort,
        # holt fertige Werkstattwaren ins LAGER DES ORTES und bucht abgeschlossene Ausbildungen
        # genau einmal. Vorher buchte `tick` die Ernte SELBST — und `ort_tick` tut dasselbe:
        # nebeneinander hätte das JEDE ERNTE VERDOPPELT. Deshalb steht hier jetzt nur der Kern.
        #
        # Die Gesamtsicht (Reich = Übergangsbestand + Summe der Ortslager) wird um genau die
        # Zuwächse nachgeführt, die die Orte WIRKLICH bekommen haben — berechnet aus dem
        # Unterschied vor/nach dem Kern, nicht aus einer zweiten Ertragsformel. Eine zweite
        # Rechnung wäre eine zweite Wahrheit.
        _ab = float(getattr(self, "spielsekunden", 0.0))
        _bis = _ab + dt_seconds
        # Teil 6c: was in diesem Takt WIRKLICH fertig wurde (Ware im Ortslager, ausgebildete
        # Einheit). Die Oberfläche braucht das, um neu zu zeichnen — sonst bliebe die fertige Ware
        # unsichtbar, bis der Spieler die Ansicht wechselt.
        eingetroffen: List[str] = []
        # Teil 6 (Rest): auch die FORSCHUNG laeuft auf dieser Uhr. `forschung_abschluss` hebt die
        # Stufe im WISSEN (global) und loescht den Auftrag im ORT — genau einmal.
        _wissen = {k: int(v.level) for k, v in self.research.items()}
        # Oekonomie-Paket, Schritt 10 Teil 2 (Entwurf Z. 645-648): die ORTSSEITE faehrt jetzt ueber
        # die EREIGNISUHR. `tick_bis` zerlegt den Takt in genau die Spannen, die die Ereignisse
        # vorgeben (Ausbildungsende, Forschungsende, fertige Werkstattware) — ein grosser Takt ist
        # damit GENAU so viel wie viele kleine. Vorher lief EINE Spanne [ab, bis]: eine Forschung,
        # die mitten im Takt fertig wurde, wirkte erst am Spannenende auf die Produktion (belegt in
        # tests/test_oekonomie_uhr.py, 13i: 4.000000 statt 4.372222 Holz).
        _abschnitt = _ab                                                   # Beginn des naechsten Abschnitts
        for _punkt in bot_takt_punkte(_ab, _bis):                          # S-13: je festem Bot-Punkt
            _wissen = self._orte_abschnitt(_abschnitt, _punkt, _wissen, eingetroffen)  # Orte bis dorthin
            self.bots_fortschreiben(_punkt)                                # DANN handelt der Bot - auf DIESEM Stand
            _abschnitt = _punkt                                            # naechster Abschnitt beginnt hier
        # Der Rest des Takts (auch ein Takt von 0 s: dann wird nur Faelliges gebucht).
        _wissen = self._orte_abschnitt(_abschnitt, _bis, _wissen, eingetroffen)
        # FIX 2+3: Tag fortschreiben (86400s = 1 Spieltag) + Götterschutz nach sieben Tagen bzw.
        # beim ersten Kriegspunkt beenden (Handbuch S. 6, KORREKTUR 05.10.2026 — vorher Tag 3).
        # Siedlergrenze und Siedlerzuwachs kommen aus den Haeusern der Siedlungskarten (W4b-5):
        # 10 Siedler je Siedlung, +5 je Haus, 1 neuer Siedler je Stunde (Handbuch Seite 11),
        # mit Heilkunde +10 % je Stufe. Vorher stand hier ein erfundener Zuwachs von 30 je Stunde.
        # Teil 6b: der ZUWACHS wird nicht mehr hier gerechnet — er entsteht in `ort_tick` je Ort
        # (bis zu dessen eigener Grenze) und wird oben als Unterschied in die Gesamtsicht gebucht.
        # Hier bleibt nur die GESAMTGRENZE für die Anzeige, damit keine zweite Zuwachsformel läuft.
        self.max_population = gebaeude_wirkung.bevoelkerungsgrenze(self.settlements)
        self._day_accum = getattr(self, "_day_accum", 0.0) + dt_seconds
        tage, self._day_accum = divmod(self._day_accum, 86400.0)
        self.day += int(tage)
        if self.noob_protection:
            # Götterschutz (Handbuch S. 6, Z. 215-217; KORREKTUR 05.10.2026): neue Spieler sind die
            # ersten SIEBEN Tage geschützt, der Schutz endet früher mit dem ERSTEN Kriegspunkt.
            # Vorher stand hier ein fester Tag 3 — belegter Widerspruch gegen das Handbuch
            # (archiv/analysen/audits/handbuch_abgleich_2026-10-05.txt, Punkt 1). `self.day` startet bei 1,
            # also sind „die ersten sieben Tage“ day 1..7 und der Schutz endet ab day 8.
            krieg = self.punktestand()["krieg"]
            if self.day > punkte.goetterschutz_tage() or krieg > 0:
                self.noob_protection = False
                grund = ("erster Kriegspunkt" if krieg > 0
                         else f"{punkte.goetterschutz_tage()} Tage vorbei")
                self.messages.append({
                    "text": f"Götterschutz beendet ({grund}) - die Welt ist jetzt gefährlich!",
                    "type": "system"})
        # W3: fertige Waren aus den Werkstatt-Warteschlangen ins Lager buchen (genau einmal).
        self.werkstatt_fortschreiben(self.spielsekunden)
        # W7: Auftraege weiterlaufen lassen (Ankunft buchen, Heimkehrer gutschreiben).
        self.auftraege_fortschreiben(self.spielsekunden)
        self.last_tick = time.time()
        # Teil 6c: was in diesem Takt fertig wurde, geht an den Aufrufer ZURÜCK — die Oberfläche
        # zeichnet daraufhin neu (`NebelseetalApp._tick_loop`). `GameState` kennt keine Ansicht.
        for _was in eingetroffen[:4]:
            self._log(f"Fertig: {_was}")
        return eingetroffen

    def save(self, path: str, admin_freigabe: bool = False):
        if self.admin_teststand and not admin_freigabe:
            self._log("Admin-Teststand darf nicht in einen regulaeren Slot gespeichert werden.")
            return False
        self._reichsanzeige_aus_orten()
        data = {
            "resources": {k: asdict(v) for k, v in self.resources.items()},
            "buildings": {k: asdict(v) for k, v in self.buildings.items()},
            "research": {k: asdict(v) for k, v in self.research.items()},
            "population": self.population, "max_population": self.max_population,
            "score": self.score, "day": self.day, "current_map": self.current_map,
            "ruf": self.ruf, "unlocked_maps": self.unlocked_maps, "active_maps": self.active_maps,
            "map_switch_cost": self.map_switch_cost,
            "map_garrison": self.map_garrison,
            "movements": self.movements,
            "messages": self.messages,
            "settlements": [asdict(s) for s in self.settlements],
            # Ökonomie-Paket, Teil 5: der Kartenvorrat ist Spielzustand (eine vergebene Karte
            # bleibt vergeben) — ohne ihn könnte ein geladener Stand Karten doppelt vergeben.
            "kartenvorrat": self.kartenvorrat,
            "kartenvorrat_seed": self.kartenvorrat_seed,
            # A2-Vorstufe: die gewaehlte Startkarte gehoert in den Spielstand, sonst wuerde ein
            # geladener Stand den Spieler erneut waehlen lassen.
            "startkarte_gewaehlt": getattr(self, "startkarte_gewaehlt", ""),
            # A2: das gewaehlte Volk gehoert in den Spielstand - sonst waehlte ein geladener Stand
            # erneut, und die Bots traegen wieder die alte Zuordnung.
            "spieler_fraktion": getattr(self, "spieler_fraktion", ""),
            "aktive_siedlung_id": self.aktive_siedlung_id,
            "spielsekunden": self.spielsekunden,
            "noob_protection": self.noob_protection,
            "goods": self.goods,
            "map_tiles": [asdict(t) for t in self.map_tiles],
            "bots": [asdict(b) for b in self.bots],
            "map_bot_factions": self.map_bot_factions if hasattr(self, "map_bot_factions") else {},
            "eigene_dimension": self.eigene_dimension,
            "eigene_dimensionen": self.eigene_dimensionen,
            "letzter_wechsel": self.letzter_wechsel,
            "waren": self.waren,
            "werkstaetten": self.werkstaetten,
            "auftraege": self.auftraege,
            "forschungsauftraege": self.forschungsauftraege,
            # Fehler, gefunden von der Durchspiel-Pruefung (05.10.2026): die Einheiten wurden
            # NIE mitgespeichert - nach dem Laden stand die Armee auf 0.
            "units": {k: int(u.count) for k, u in self.units.items()},
            # Sieg/Niederlage (Schritt 31): die Partie-Entscheidung gehoert in den Spielstand,
            # sonst gilt ein gewonnenes Spiel nach dem Laden wieder als offen.
            "hatte_siedlung": getattr(self, "hatte_siedlung", False),
            "spielende": getattr(self, "spielende", None),
            # Teil 8b (Entwurf Z. 789): die FORM des Spielstands (Version + Modus) und der
            # Tagesrest. Entwurf woertlich: "_day_accum zusaetzlich sichern statt beim Laden auf 0
            # setzen" — sonst beginnt der Spieltag nach jedem Laden von vorn.
            "stand_version": self.stand_version,
            "mode": self.mode,
            "oekonomie_aktiv": bool(self.oekonomie_aktiv),
            "admin_teststand": bool(self.admin_teststand),
            # Nur fuer getrennte Admin-Saves: niemals in normale Spielerslots schreiben.
            **({"admin_hilfe_modus": self.admin_hilfe_modus} if self.admin_teststand else {}),
            "admin_weltkarten": getattr(self, "admin_weltkarten", {}) if self.admin_teststand else {},
            "_day_accum": getattr(self, "_day_accum", 0.0),
            # GPT-Z01: Archiv-Zeitpunkt, keine Simulations-/Wirtschaftsuhr.
            **zeitbasis.zeitmarke(),
        }
        # W8 (docs/UMSETZUNG_EINHAENGEN.md, Abschnitt 4): erst sichern, dann atomar ueber eine
        # gepruefte Zwischendatei schreiben. Schlaegt etwas fehl, bleibt der alte Spielstand
        # unangetastet - es gibt entweder den alten ODER den neuen Stand, nie eine halbe Datei.
        gesichert, meldung_sicherung = speichern.sichere_kopie(path)
        if gesichert:
            self._log(meldung_sicherung)
        ok, meldung = speichern.speichere(data, path)
        if ok:
            self._log(meldung)
        else:
            self._log(f"Speichern fehlgeschlagen - der alte Spielstand bleibt stehen: {meldung}")
        return ok

    def load(self, path: str, admin_freigabe: bool = False):
        if not os.path.exists(path):
            return False
        # W8: ueber das robuste Modul lesen; ist die Datei beschaedigt, erst die Sicherung
        # (.bak) wiederherstellen, bevor ehrlich abgebrochen wird.
        data, fehler = speichern.lade(path)
        if data is None:
            self._log(f"Spielstand nicht lesbar: {fehler}")
            wieder_ok, meldung = speichern.wiederherstellen(path)
            if wieder_ok:
                self._log(meldung)
                data, fehler = speichern.lade(path)
            else:
                self._log(f"Wiederherstellung nicht moeglich: {meldung}")
            if data is None:
                self._log(f"Laden abgebrochen - der bisherige Stand bleibt stehen: {fehler}")
                return False
        # Neue Hauptfassung: Ein alter 8x7-Spielstand bleibt als Archiv auf Disk,
        # darf aber nicht mehr aktiv geladen oder heimlich in eine andere Karte verwandelt werden.
        for siedlung in data.get("settlements", []):
            karte = siedlung.get("karte") if isinstance(siedlung, dict) else None
            if not karte:
                continue  # Alte leerstehende Verwaltungseintraege noch ohne Landkarte
            try:
                originalkarten_grafik.grafikpfad(karte)
            except (ValueError, FileNotFoundError) as fehler:
                self._log("Archiv-Spielstand nicht ladbar (nur Originalkarten): " + str(fehler))
                return False
        for name, eintrag in (data.get("kartenvorrat") or {}).items():
            karte = eintrag.get("karte") if isinstance(eintrag, dict) else None
            if karte:
                try:
                    originalkarten_grafik.grafikpfad(karte)
                except (ValueError, FileNotFoundError) as fehler:
                    self._log("Alter Kartenvorrat nicht ladbar (" + str(name) + "): " + str(fehler))
                    return False
        # Ablehnung VOR der ersten Zustandsmutation: kein Adminstand im normalen Spiel.
        if data.get("admin_teststand") and not admin_freigabe:
            self._log("Admin-Teststand gesperrt: separate Adminfreigabe erforderlich.")
            return False
        self.admin_teststand = bool(data.get("admin_teststand", False))
        hilfemodus = data.get("admin_hilfe_modus", "auto")
        self.admin_hilfe_modus = (hilfemodus if self.admin_teststand and
                                 hilfemodus in spielerhilfe.ADMIN_HILFE_MODI else "auto")
        self.admin_weltkarten = (dict(data.get("admin_weltkarten") or {})
                               if self.admin_teststand else {})
        for k, v in data.get("resources", {}).items():
            if k in self.resources:
                self.resources[k] = Resource(**v)
        for k, v in data.get("buildings", {}).items():
            if k in self.buildings:
                self.buildings[k] = Building(**v)
        for k, v in data.get("research", {}).items():
            if k in self.research:
                self.research[k] = Research(**v)
        # Die Anzahl je Einheit. Alte Spielstaende kennen das Feld nicht: sie laden weiter und
        # haben dann 0 Einheiten (die Zahlen wurden damals nie geschrieben) - kein Absturz.
        for k, anzahl in (data.get("units") or {}).items():
            if k in self.units:
                self.units[k].count = max(0, int(anzahl))
        self.population = data.get("population", 0)
        self.max_population = data.get("max_population", 10)
        self.score = data.get("score", 0)
        self.day = data.get("day", 1)
        self.current_map = data.get("current_map", "kontinent")
        self.ruf = data.get("ruf", 0)
        self.unlocked_maps = data.get("unlocked_maps", ["kontinent"])
        self.active_maps = data.get("active_maps", ["kontinent"])
        self.map_switch_cost = data.get("map_switch_cost", 150)
        self.map_garrison = data.get("map_garrison", {})
        self.movements = data.get("movements", [])
        self.messages = zeitbasis.NachrichtenMitZeit(data.get("messages", []), spieluhr=lambda: self.spielsekunden)
        self.settlements = [Settlement(**s) for s in data.get("settlements", [])]
        # Ökonomie-Paket Schritt 9: Altspielstände kennen die Ort-Kennung nicht. Sie bekommen sie
        # hier EINMALIG deterministisch aus Besitzer und Weltfeld — nicht aus dem Namen, damit ein
        # späteres Umbenennen die Kennung nie ändert (Entwurf Z. 774).
        for s in self.settlements:
            if not s.id:
                s.id = siedlung_kennung(s.besitzer, s.map_id, s.x, s.y)
        # A2/V-5 (03.11.2026): das gewaehlte Volk wird wieder GELADEN - sonst waehlte ein geladener
        # Stand erneut, und seit V-5 fehlte ihm die Wirkung. Ein Stand ohne das Feld bleibt leer.
        self.spieler_fraktion = str(data.get("spieler_fraktion") or "")
        # V-5: der Volksbonus haengt am ORT (der Ertrag liest `siedlung.volk`). Ein alter Spielstand
        # traegt das Feld nicht - er bekommt es hier aus dem Spielstand, aber nur, wenn dort eines
        # steht (kein Erfinden, und ohne Volk bleibt es beim Faktor 1,0).
        for s in self.settlements:
            if not getattr(s, "volk", "") and self.spieler_fraktion:
                s.volk = self.spieler_fraktion
        # Ökonomie-Paket, Teil 5: den Kartenvorrat laden. Ein ALTER Spielstand kennt ihn nicht —
        # dann wird er nachträglich angelegt (seine bestehenden Siedlungen bleiben unverändert).
        self.kartenvorrat = {k: v for k, v in (data.get("kartenvorrat") or {}).items()
                             if isinstance(v, dict) and v.get("karte")}
        self.kartenvorrat_seed = str(data.get("kartenvorrat_seed") or "")
        # Teil 6: der Zeiger auf den Ort. Ein ALTER Spielstand kennt ihn nicht — dann bleibt er
        # leer und `aktive_siedlung()` faellt auf die erste Siedlung (und berichtigt ihn dort).
        self.aktive_siedlung_id = str(data.get("aktive_siedlung_id") or "")
        # Teil 6b: die Spieluhr. Ein Stand von vor Teil 6 kennt sie nicht — dann beginnt sie bei 0;
        # `ort_tick` verbietet nur ein ZURÜCKLAUFEN der Zeit, nicht den Neubeginn.
        self.spielsekunden = float(data.get("spielsekunden") or 0.0)
        # Teil 8b, MIGRATION (Entwurf Z. 789): ein Spielstand OHNE Versionsfeld ist ein
        # ALTSPIELSTAND. Er laedt als `mode="legacy"` MIT Warnhinweis — seine Regeln und sein
        # Punktziel bleiben unveraendert, und es wird NICHTS umgerechnet ("ohne explizite
        # Daniel-Entscheidung keine automatische Konvertierung alter Ressourcen"). Neue Partien
        # laufen als `oeokonomie-1`. Das Feld ist ein MERKER, keine Schaltung (Entwurf Z. 1092).
        roh_version = data.get("stand_version")
        if roh_version is None:
            self.stand_version = STAND_VERSION_ALT
            self.mode = MODUS_LEGACY
            self._altstand_warnen()
        else:
            self.stand_version = int(roh_version)
            self.mode = str(data.get("mode") or MODUS_NEU)
            if self.mode not in (MODUS_NEU, MODUS_LEGACY):
                # Nicht raten und nicht stillschweigend verbiegen: den fremden Wert uebernehmen
                # und ehrlich vermerken.
                self._log("Warnhinweis: unbekannter Modus '%s' im Spielstand - er wird "
                          "unveraendert uebernommen." % self.mode)
        # Eine alte v2-Datei meldet bereits "oeokonomie-1", hatte diesen Modus
        # aber laut Protokoll noch NICHT aktiviert. Die v2-Bestaende duerfen nicht
        # als rein lokale Kasse neu gedeutet oder stillschweigend geloescht werden.
        self.oekonomie_aktiv = (self.mode == MODUS_NEU
                                and data.get("oekonomie_aktiv") is True)
        if not self.kartenvorrat:
            self.kartenvorrat_anlegen()
        self.hatte_siedlung = bool(data.get("hatte_siedlung", bool(self.settlements)))
        self.spielende = data.get("spielende")
        self.noob_protection = data.get("noob_protection", True)
        # Kein Upgrade alter Legacy-Staende. Fuer neue, lokale Staende ist die
        # globale Anzeige nur eine abgeleitete Summe nach dem Laden.
        self._reichsanzeige_aus_orten()
        self.goods = data.get("goods", {key: 0 for key in GOODS})
        # W5-2: Portalzustand (eigene Weltkarte, bekannte Weltkarten, letzter Weltensprung).
        # S-2b: fehlt der Eintrag, gilt die Startwelt aus data/welten.json (Midgard) - die alte
        # Vorgabe "1" (Armageddon) war ein VORSCHLAG und ist durch Daniels Entscheidung ersetzt.
        _startwelt = welt.startwelt_nummer() or 1
        self.eigene_dimension = int(data.get("eigene_dimension") or _startwelt)
        self.eigene_dimensionen = list(data.get("eigene_dimensionen") or [_startwelt])
        self.letzter_wechsel = data.get("letzter_wechsel")
        # W3: Warenlager (immer alle 17 Originalwaren) und die Werkstatt-Warteschlangen
        geladene_waren = data.get("waren") or {}
        self.waren = {name: int(geladene_waren.get(name, 0) or 0) for name in WARE_EINTRAEGE}
        self.werkstaetten = {k: v for k, v in (data.get("werkstaetten") or {}).items()
                             if isinstance(v, dict)}
        # W7: laufende Auftraege (unterwegs befindliche Einheiten sind hier schon abgezogen)
        self.auftraege = [e for e in (data.get("auftraege") or []) if isinstance(e, dict)]
        # W4c: die laufende Forschung je Gebiet (die Stufe steht in `research`)
        self.forschungsauftraege = {k: v for k, v in (data.get("forschungsauftraege") or {}).items()
                                   if isinstance(v, dict) and k in self.research}
        # Teil 6 (Rest): ein Spielstand von VOR Teil 6 traegt seine Forschungsauftraege noch
        # reichsweit (`forschungsauftraege`). Sie gehoeren jetzt in einen ORT — sonst gaebe es zwei
        # fuehrende Auftrags-Wahrheiten und die Stufe wuerde zweimal bezahlt. Umgezogen wird in den
        # ersten Ort (der Auftrag nennt sein Gebiet selbst); danach ist der Altpfad leer.
        if self.forschungsauftraege and self.settlements:
            _ziel_ort = next((s for s in self.settlements
                              if not getattr(s, "forschungsauftrag", None)), None)
            if _ziel_ort is not None:
                _gebiet, _auftrag = next(iter(self.forschungsauftraege.items()))
                _ziel_ort.forschungsauftrag = dict(_auftrag)
                self._log(f"Forschungsauftrag {_gebiet} aus einem alten Spielstand in "
                          f"{_ziel_ort.name} umgezogen (jetzt forscht der Ort, nicht das Reich).")
            for _g in list(self.forschungsauftraege):
                self.forschungsauftraege.pop(_g, None)
        # FIX 4b: Karte + Bots laden (wurde vorher nicht persistiert)
        saved_tiles = data.get("map_tiles")
        saved_bots = data.get("bots")
        if saved_tiles:
            self.map_tiles = [MapTile(**t) for t in saved_tiles]
        else:
            self.generate_map(self.current_map)
        if saved_bots:
            # B-1: Doerfer kommen als dicts aus dem Spielstand zurueck und werden wieder Objekte;
            # ein Stand von vor B-1 hat kein Feld `doerfer` und bekommt es hier aus den Namen.
            self.bots = [bot_aus_stand(b) for b in saved_bots]
            for _b in self.bots:
                bot_doerfer_sicherstellen(_b)
        # Teil 8b (Entwurf Z. 789: "_day_accum zusaetzlich sichern statt beim Laden auf 0 setzen"):
        # der Tagesrest kommt jetzt aus dem Spielstand. Ein Stand, der das Feld nicht kennt (alles
        # vor Teil 8b), beginnt unveraendert bei 0 — kein Absturz, keine erfundene Zahl.
        self._day_accum = float(data.get("_day_accum") or 0.0)
        # Der Bot-Zug darf nach dem Laden nicht sofort losgehen (sonst pluendern die Bots
        # genau in der Sekunde, in der ein alter Spielstand geoeffnet wird).
        self._letzter_bot_takt = float(self.spielsekunden)
        # Neustart der monotone Echtzeituhr: keine Nachproduktion seit dem Save.
        self._laufzeituhr.neu_ankern()
        self.last_tick = time.time()
        return True

    def _log(self, msg: str):
        self.log.append(msg)
        if len(self.log) > 200:
            self.log = self.log[-200:]

    def _altstand_warnen(self):
        """Den Warnhinweis fuer einen geladenen ALTSPIELSTAND sichtbar machen (Entwurf Z. 789).

        Wörtlich: „Ist ein Altspielstand ohne Versionsfeld vorhanden, mode="legacy", Regeln und
        Punktziel behalten, Warnhinweis anzeigen." Er geht deshalb in die Log-Zeilen UND in die
        sichtbaren Nachrichten (die Nachrichtenansicht zeigt die letzten 20). Mehrfaches Laden
        derselben Datei soll die Liste nicht fluten — der Eintrag kommt deshalb nur EINMAL vor.
        """
        text = ("Altspielstand geladen (ohne Versionsfeld): diese Partie laeuft im Modus 'legacy' "
                "- ihre Regeln und ihr Punktziel bleiben unveraendert. Es wird nichts umgerechnet.")
        self._log("Warnhinweis: " + text)
        eintrag = {"text": "Warnhinweis: " + text, "type": "warnung"}
        if eintrag not in self.messages:
            self.messages.append(eintrag)


# ---------- GUI ----------

class NebelseetalApp:
    def __init__(self, root: tk.Tk, tor_pfad: Optional[str] = None):
        self.root = root
        self.root.title("Nebelseetal Remake")
        self.root.geometry("1024x720")
        # Daniels Layoutwunsch 05.10.2026 (die Bauauswahl steht RECHTS neben der Karte) braucht
        # Breite: die Karte allein ist 8 x 64 + 18 = 530 px breit, die Auswahlspalte rund 330 px.
        # Darum wächst das Fenster mit dem Bildschirm — bleibt aber IMMER innerhalb von ihm.
        try:
            _breit = max(1024, min(1560, int(self.root.winfo_screenwidth()) - 90))
            _hoch = max(720, min(940, int(self.root.winfo_screenheight()) - 120))
            self.root.geometry(f"{_breit}x{_hoch}")
        except Exception:
            pass  # ohne Bildschirmmaße bleibt es beim Vorgabemaß 1024x720
        self.state = GameState()
        self.state.generate_map(self.state.current_map)
        # Spielstand: im Entwicklungsbetrieb neben dem Quelltext, in der EXE im Nutzerordner
        # (der Programmordner kann schreibgeschuetzt sein und wird beim Einzeldatei-Start entpackt).
        if ist_verpackt() or os.environ.get("NEBEL_SPIELDATEN_ORDNER"):
            self.save_path = os.path.join(schreibordner(), "savegame.json")
        else:
            self.save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "savegame.json")
        # W8 (Vorschlag aus docs/UMSETZUNG_EINHAENGEN.md, 4.2): liegengebliebene Zwischendateien
        # eines abgebrochenen Schreibvorgangs entfernen - Zieldatei und Sicherung bleiben unberuehrt.
        speichern.aufraeumen(self.save_path)
        self.slots_ordner = os.path.dirname(self.save_path)
        # FIX04g: Auf private, von GitHub getrennte Spielstand-Archivstruktur achten.
        # Angelegt werden nur Ordner, keine vorhandenen Spielstaende verschoben.
        spielstand_archiv.ordner_anlegen(self.slots_ordner)
        self.admin_tor_pfad = os.path.join(schreibordner(), "admin_tor.json")
        self._admin_sitzung_freigegeben = False  # nur nach Admin-Authentifizierung
        # GPT-PR01: Passworttor, Profil und Savegame sind drei getrennte Schichten.
        self._tor_geoeffnet = False
        self._profil = None  # None bis zur Wahl; "spieler" oder "admin"
        self.current_view = "Dorfzentrum"
        self.skin_name = "standard"
        self.skin = SKINS[self.skin_name]
        self._icon_cache: Dict[str, object] = {}   # haelt Tk-Bilder am Leben (sonst raeumt Tk sie weg)
        # Schritt 8 (docs/WEG_ZUR_EXE.md): erst das Passworttor, dann das Spiel.
        # Public-Test: eigene lokale Passwortdatei; niemals die Entwickler-Tordatei anfassen.
        # Der Build-Einstieg public_start.py setzt einen festen privaten Save-Ordner.
        if ausgabemodus.ist_oeffentliche_testversion():
            self.tor_pfad = tor_pfad or os.path.join(schreibordner(), "tor.json")
        else:
            self.tor_pfad = tor_pfad or tor.STANDARD_PFAD
        self._tor_screen()

    # ---------- Passworttor (Schritt 8) ----------

    def _tor_screen(self):
        """Das Tor vor dem Spielstart: Passwort festlegen (Erststart) oder eingeben."""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg="#2a0605")
        rahmen = tk.Frame(self.root, bg="#2a0605")
        rahmen.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.tor_rahmen = rahmen
        tk.Label(rahmen, text="Nebelseetal", font=("Blackletter", 44, "bold"),
                 fg="#FFCC33", bg="#2a0605").pack(pady=(0, 2))
        tk.Label(rahmen, text="Remake", font=("Blackletter", 20), fg="#FF6600",
                 bg="#2a0605").pack(pady=(0, 16))
        if tor.hat_passwort(self.tor_pfad):
            self._tor_anmelden()
        else:
            self._tor_festlegen()

    def _tor_festlegen(self):
        """Erststart: Daniel setzt das Passwort selbst — zweimal eingeben."""
        tk.Label(self.tor_rahmen, text="Beim ersten Start legst du das Passwort selbst fest.\n"
                                       "Gespeichert wird nur ein Prüfwert davon, nie das Passwort.",
                 fg="#FFFF99", bg="#2a0605", justify=tk.CENTER).pack(pady=(0, 12))
        tk.Label(self.tor_rahmen, text="Passwort", fg="#C0C0C0", bg="#2a0605").pack()
        self.tor_neu1 = tk.Entry(self.tor_rahmen, show="*", width=28, justify=tk.CENTER)
        self.tor_neu1.pack()
        tk.Label(self.tor_rahmen, text="Wiederholung", fg="#C0C0C0", bg="#2a0605").pack(pady=(8, 0))
        self.tor_neu2 = tk.Entry(self.tor_rahmen, show="*", width=28, justify=tk.CENTER)
        self.tor_neu2.pack()
        self.tor_meldung = tk.Label(self.tor_rahmen, text="", fg="#e53935", bg="#2a0605",
                                    wraplength=420, justify=tk.CENTER)
        self.tor_meldung.pack(pady=(8, 0))
        tk.Button(self.tor_rahmen, text="Passwort festlegen und starten", command=self._tor_setzen,
                  bg="#3e2723", fg="#FFCC33", activebackground="#5D4037").pack(pady=10)
        self.tor_neu1.focus_set()
        self.tor_neu2.bind("<Return>", lambda _e: self._tor_setzen())
        tk.Label(self.tor_rahmen,
                 text=f"Notausgang: die Datei „{self.tor_pfad}“ löschen — dann verlangt das Spiel beim\n"
                      f"nächsten Start ein NEUES Passwort. Der Spielstand bleibt erhalten.",
                 fg="#C0C0C0", bg="#2a0605", justify=tk.CENTER, wraplength=460).pack(pady=(10, 0))

    def _tor_setzen(self):
        ok, meldung = tor.setze_passwort(self.tor_neu1.get(), self.tor_neu2.get(), self.tor_pfad)
        if ok:
            self.tor_neu1.delete(0, tk.END)
            self.tor_neu2.delete(0, tk.END)
            self.tor_meldung.config(text="Passwort gesetzt. Das Spiel startet …", fg="#7CFC00")
            self._log(f"Passworttor eingerichtet ({meldung})")
            self._tor_geoeffnet = True
            self.root.after(600, self._profil_auswahl)
        else:
            self.tor_meldung.config(text=meldung, fg="#e53935")

    def _tor_anmelden(self):
        """Jeder weitere Start: Passwort verlangen (mit Wartezeit nach Fehlversuchen)."""
        tk.Label(self.tor_rahmen, text="Dieses Spiel ist passwortgeschützt.\n"
                                       "(Hinweis: in einer Kopie des Ordners steckt dasselbe Passwort.)",
                 fg="#FFFF99", bg="#2a0605", justify=tk.CENTER).pack(pady=(0, 12))
        tk.Label(self.tor_rahmen, text="Passwort", fg="#C0C0C0", bg="#2a0605").pack()
        self.tor_eingabe = tk.Entry(self.tor_rahmen, show="*", width=28, justify=tk.CENTER)
        self.tor_eingabe.pack()
        self.tor_meldung = tk.Label(self.tor_rahmen, text="", fg="#e53935", bg="#2a0605",
                                    wraplength=420, justify=tk.CENTER)
        self.tor_meldung.pack(pady=(8, 0))
        self.tor_knopf = tk.Button(self.tor_rahmen, text="Spiel starten", command=self._tor_pruefen,
                                   bg="#3e2723", fg="#FFCC33", activebackground="#5D4037")
        self.tor_knopf.pack(pady=10)
        self.tor_eingabe.focus_set()
        self.tor_eingabe.bind("<Return>", lambda _e: self._tor_pruefen())
        tk.Label(self.tor_rahmen,
                 text=f"Notausgang: die Datei „{self.tor_pfad}“ löschen setzt das Tor zurück\n"
                      f"(Spielstand bleibt erhalten).",
                 fg="#C0C0C0", bg="#2a0605", justify=tk.CENTER, wraplength=460).pack(pady=(10, 0))
        self._tor_wartezeit_anzeigen()

    def _tor_pruefen(self):
        ok, meldung = tor.pruefe_passwort(self.tor_eingabe.get(), self.tor_pfad)
        self.tor_eingabe.delete(0, tk.END)
        if ok:
            self.tor_meldung.config(text="Zugang gewährt. Das Spiel startet …", fg="#7CFC00")
            self._log("Passworttor geöffnet.")
            self._tor_geoeffnet = True
            self.root.after(400, self._profil_auswahl)
        else:
            self.tor_meldung.config(text=meldung, fg="#e53935")
            self._tor_wartezeit_anzeigen()

    def _tor_wartezeit_anzeigen(self):
        """Nach zu vielen Fehlversuchen bleibt der Knopf so lange gesperrt."""
        rest = tor.restwartezeit(self.tor_pfad)
        if rest > 0:
            self.tor_knopf.config(state=tk.DISABLED)
            self.tor_meldung.config(text=f"Zu viele Fehlversuche. Noch {int(rest) + 1} Sekunden warten.",
                                    fg="#e53935")
            self.root.after(1000, self._tor_wartezeit_anzeigen)
        else:
            try:
                self.tor_knopf.config(state=tk.NORMAL)
            except Exception:
                pass

    # ---------- GPT-PR01: Nach Grundpasswort erst Profil auswaehlen ----------

    def _profil_auswahl(self):
        """Nur nach erfolgreichem Grundpasswort: zwei strikt getrennte Spielwege.

        Das Tor steuert lediglich den Programmstart; es wird nie an ein Profil
        oder einen Save-Slot gebunden. Der Admin besitzt sein EIGENES Passwort.
        """
        if not self._tor_geoeffnet:
            return
        self._profil = None
        self._admin_sitzung_freigegeben = False
        self.state = GameState()  # keine Daten aus der vorigen Sitzung mitnehmen
        if ausgabemodus.ist_oeffentliche_testversion():
            # Oeffentliche EXE: genau der normale Spielweg, ohne Admin-Profilauswahl.
            self._spieler_auswahl()
            return
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg="#2a0605")
        frame = tk.Frame(self.root, bg="#2a0605")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        tk.Label(frame, text="Nebelseetal - Profil waehlen", font=("Arial", 23, "bold"),
                 fg="#FFCC33", bg="#2a0605").pack(pady=(0, 14))
        tk.Label(frame, text="Das Grundpasswort hat den Spielstart freigegeben.\n"
                 "Waehle nun deinen Spielmodus:", fg="#FFFF99", bg="#2a0605",
                 justify=tk.CENTER).pack(pady=(0, 16))
        tk.Button(frame, text="Mein Spielaccount - normal spielen",
                  command=self._spieler_auswahl, width=38, pady=9,
                  fg="#FFCC33", bg="#3e2723").pack(pady=7)
        tk.Label(frame, text="Drei unabhaengige Spielstaende; keine Admin-Befehle.",
                 fg="#C0C0C0", bg="#2a0605").pack()
        tk.Button(frame, text="Mein Adminaccount - Testwelt und Cheats",
                  command=self._admin_dialog, width=38, pady=9,
                  fg="#FFCC33", bg="#3e2723").pack(pady=(19, 7))
        tk.Label(frame, text="Separates Admin-Passwort und eigener Testspielstand.",
                 fg="#C0C0C0", bg="#2a0605").pack()

    def _spieler_auswahl(self):
        """Die drei normalen Slots VOR dem Start des eigentlichen Spiels zeigen."""
        if not self._tor_geoeffnet:
            return
        self._profil = None
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg="#2a0605")
        frame = tk.Frame(self.root, bg="#2a0605")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        tk.Label(frame, text="Mein Spielaccount", font=("Arial", 22, "bold"),
                 fg="#FFCC33", bg="#2a0605").pack(pady=(0, 12))
        tk.Label(frame, text="Einen von drei Spielstaenden waehlen oder neu beginnen:",
                 fg="#FFFF99", bg="#2a0605").pack(pady=(0, 12))
        for nummer in spielstaende.SLOTS:
            zeile = tk.Frame(frame, bg="#2a0605")
            zeile.pack(fill=tk.X, pady=4)
            pfad = spielstaende.slot_pfad(self.slots_ordner, nummer)
            tk.Label(zeile, text=spielstaende.slot_status(self.slots_ordner, nummer),
                     fg="#FFFF99", bg="#2a0605", width=40,
                     anchor=tk.W).pack(side=tk.LEFT)
            tk.Button(zeile, text=f"Slot {nummer} laden", width=16,
                      state=(tk.NORMAL if os.path.isfile(pfad) else tk.DISABLED),
                      command=lambda n=nummer: self._spieler_slot_starten(n),
                      fg="#FFCC33", bg="#3e2723").pack(side=tk.RIGHT)
        tk.Button(frame, text="Spielstaende verwalten / archivieren", width=35,
                  command=lambda: self._spielstand_verwaltung("spieler"),
                  fg="#FFCC33", bg="#3e2723").pack(pady=(12, 2))
        tk.Button(frame, text="Neue Partie beginnen", width=25,
                  command=self._spieler_neu_starten,
                  fg="#FFCC33", bg="#3e2723").pack(pady=(16, 8))
        if not ausgabemodus.ist_oeffentliche_testversion():
            tk.Button(frame, text="Zurueck zur Profilwahl", command=self._profil_auswahl,
                      fg="#C0C0C0", bg="#3e2723").pack(pady=7)

    def _spieler_neu_starten(self):
        if not self._tor_geoeffnet:
            return
        neu = GameState()
        neu.generate_map(neu.current_map)
        self._spiel_starten(neu, "spieler")

    def _spieler_slot_starten(self, nummer: int):
        if not self._tor_geoeffnet:
            return
        from tkinter import messagebox
        neu = GameState()
        # Nie admin_freigabe=True fuer normale Slots!
        if not neu.load(spielstaende.slot_pfad(self.slots_ordner, nummer)):
            messagebox.showerror("Spielstand", f"Slot {nummer} nicht ladbar.", parent=self.root)
            return
        self._spiel_starten(neu, "spieler")

    def _spiel_starten(self, zustand: GameState, profil: str):
        """Eine explizite, validierte Profil- und Spielzustandsbindung."""
        if not self._tor_geoeffnet or profil not in ("spieler", "admin"):
            return False
        if ausgabemodus.ist_oeffentliche_testversion() and profil != "spieler":
            return False
        if profil == "spieler" and zustand.admin_teststand:
            return False
        if profil == "admin" and (not self._admin_sitzung_freigegeben
                                  or not zustand.admin_teststand):
            return False
        self.state = zustand
        self._profil = profil
        self._build_loading_screen()
        return True

    def _profil_zurueck(self):
        """Vor einem Profilwechsel nicht still den aktuellen Stand vernichten."""
        from tkinter import messagebox
        if not self._tor_geoeffnet:
            return
        if self._profil == "spieler":
            if not messagebox.askyesno("Profil wechseln", "Nicht gespeicherte Aenderungen "
                                      "gehen verloren. Erst in Slot 1-3 speichern! "
                                      "Trotzdem zur Profilwahl?", parent=self.root):
                return
        elif self._profil == "admin":
            if not messagebox.askyesno("Profil wechseln", "Admin-Teststand jetzt sichern "
                                      "und zur Profilwahl zurueckkehren?", parent=self.root):
                return
            if not self._admin_speichern():
                return
        if ausgabemodus.ist_oeffentliche_testversion():
            self._spieler_auswahl()
        else:
            self._profil_auswahl()

    def _admin_speichern(self):
        """Admin sichert ausschliesslich die eigene Datei, nie normale Slots."""
        if not (self._tor_geoeffnet and self._profil == "admin"
                and self._admin_sitzung_freigegeben and self.state.admin_teststand):
            return False
        pfad = spielstaende.admin_pfad(schreibordner())
        return bool(self.state.save(pfad, admin_freigabe=True))

    def _admin_laden(self):
        from tkinter import messagebox
        if not (self._tor_geoeffnet and self._profil == "admin"
                and self._admin_sitzung_freigegeben):
            return False
        neu = GameState()
        if not neu.load(spielstaende.admin_pfad(schreibordner()), admin_freigabe=True):
            messagebox.showwarning("Admin", "Admin-Teststand nicht lesbar.", parent=self.root)
            return False
        self.state = neu
        self._build_main_ui()
        self._render_view()
        return True

    def _lade_icon(self, relativ: str, faktor: int = 2):
        """Laedt ein Icon als Tk-Bild. faktor=2 halbiert grosse Icons (~90px -> ~45px)."""
        pfad = icon_pfad(relativ)
        if not pfad or not os.path.exists(pfad):
            return None
        if pfad in self._icon_cache:
            return self._icon_cache[pfad]
        try:
            bild = tk.PhotoImage(file=pfad)
            if faktor > 1:
                bild = bild.subsample(faktor)
        except Exception:
            return None
        self._icon_cache[pfad] = bild
        return bild

    def _motivbild_skaliert(self, relativ: str, px: int, cache: str, deckkraft: int = 100):
        """Ein Bild aus dem Projekt auf `px` Pixel bringen und im Cache halten (Tk-Bild oder None).

        Mit Pillow wird geglaettet skaliert (LANCZOS); fehlt Pillow, wird ganzzahlig per
        `subsample` verkleinert - das Spiel laeuft dann weiter, nur groeber und ohne
        Deckkraft-Absenkung. Der Cache ist Pflicht: Tk gibt Bilder frei, die niemand mehr
        referenziert (dann waeren sie unsichtbar).
        """
        pfad = icon_pfad(relativ)                                    # Projektpfad ueber EINE Stelle
        if not pfad or not os.path.exists(pfad):                     # Datei fehlt
            return None                                              # Aufrufer zeichnet den Baukoerper
        if not hasattr(self, cache):                                 # eigener Cache je Bildart
            setattr(self, cache, {})                                 # beim ersten Bild anlegen
        speicher = getattr(self, cache)                              # dict: (Pfad, Groesse, Deckkraft) -> Bild
        schluessel = (pfad, px, deckkraft)                           # Cache-Schluessel
        if schluessel in speicher:                                   # schon geladen
            return speicher[schluessel]                              # Bild wiederverwenden
        bild = None                                                  # Ergebnis
        try:                                                         # geglaetteter Weg mit Pillow
            from PIL import Image, ImageTk                            # nur hier - das Spiel laeuft auch ohne
            roh = Image.open(pfad).convert("RGBA")                    # PNG mit Alphakanal
            roh = roh.resize((px, px), Image.LANCZOS)                 # auf Zielgroesse verkleinern
            if 0 < deckkraft < 100:                                   # Deckkraft absenken (Rahmen)
                roh.putalpha(roh.getchannel("A").point(lambda a: int(a * deckkraft / 100.0)))   # Alpha skalieren
            bild = ImageTk.PhotoImage(roh)                            # Tk-Grafik daraus
        except Exception:                                            # noqa: BLE001 - kein Pillow, kein Bildschirm
            try:                                                     # Rueckfall ohne Pillow
                bild = tk.PhotoImage(file=pfad)                       # Originalgroesse laden
                faktor = max(1, int(round(bild.width() / float(px))))  # ganzzahliger Verkleinerungsfaktor
                if faktor > 1:                                       # nur verkleinern, nie vergroessern
                    bild = bild.subsample(faktor)                    # 256 px / 6 = 42 px
            except Exception:                                        # noqa: BLE001
                return None                                          # gar kein Bild
        speicher[schluessel] = bild                                   # im Cache halten
        return bild                                                  # an den Aufrufer

    def _lade_gebaeude_motiv(self, gebaeude_key: str, px: int = 44):
        """Das Kartenmotiv eines Gebaeudes als Tk-Bild - oder None, wenn keines vorliegt.

        Gelesen wird `GEBAEUDE_MOTIVE` (aus `data/gebaeude_motive.json`, Schalter
        `quelle_der_karte`): seit dem 02.11.2026 die 20 freigestellten C2-Motive mit 256 x 256 px
        (Daniel, Register 119). `px` ist die Zielgroesse auf der 64-px-Kachel - Vorgabe 44 px.
        """
        relativ = GEBAEUDE_MOTIVE.get(str(gebaeude_key))              # Motivpfad zu diesem Gebaeude
        if not relativ:                                              # kein Motiv hinterlegt
            return None                                              # dann zeichnet der Aufrufer den Baukoerper
        return self._motivbild_skaliert(relativ, px, "_motiv_cache")  # laden, skalieren, cachen

    def _lade_kachelrahmen(self, art: str = "ruhe", px: int = 64):
        """Der Kachelrahmen aus der C2-Lieferung als Tk-Bild (oder None).

        `art` ist "ruhe" (jedes Feld) oder "auswahl" (hervorgehobenes Feld); die Pfade stehen in
        `data/gebaeude_motive.json` unter `kachelrahmen` (`KACHELRAHMEN`).
        """
        relativ = KACHELRAHMEN.get(str(art))                          # Rahmenpfad zur gewuenschten Art
        if not relativ:                                               # kein Rahmen hinterlegt
            return None                                               # Karte bleibt ohne Rahmen
        deckkraft = RAHMEN_DECKRAFT if str(art) == "ruhe" else AUSWAHL_DECKRAFT   # Ruhe gedaempft, Auswahl kraeftig
        return self._motivbild_skaliert(relativ, px, "_rahmen_cache", deckkraft)   # gleicher Weg wie die Motive

    def _optik_bild(self, gebaeude_id, breite: int, hoehe=None, art: str = "kachel"):
        """Icon ("kachel") oder Hintergrund eines Gebaeudes als Tk-Grafik - gecacht, sonst None.

        Die Arbeit macht `gebaeude_optik` (liest die Projektassets, skaliert mit Pillow); hier
        entsteht nur die Tk-Grafik. Der Cache ist Pflicht: Tk gibt Bilder frei, die niemand mehr
        referenziert - ein Menue-Icon ohne Referenz waere unsichtbar (Lehre 02.11.2026).

        OHNE Pillow bleibt das Bild NICHT weg: `_optik_bild_ohne_pillow` laedt die Datei mit Tk und
        verkleinert ganzzahlig (grober, aber sichtbar). Grund (gemessen 02.11.2026, 09:10): der
        Startpfad des Spiels (`START_SPIEL_WINDOWS.bat`, Astral CPython 3.11.16) hat KEIN Pillow -
        ohne diesen Rueckfall waeren Menue-Icons, Bauknopf-Icons und Hintergruende unsichtbar.
        """
        if not gebaeude_id:                                           # Menuepunkt ohne Gebaeude
            return None                                               # dann bleibt es beim Text
        if not hasattr(self, "_optik_cache"):                         # Cache beim ersten Bild
            self._optik_cache = {}                                    # Anfrage -> Tk-Bild (auch None)
        schluessel = (str(gebaeude_id), int(breite), hoehe, str(art))  # gleiche Anfrage, gleiches Bild
        if schluessel in self._optik_cache:                           # schon gebaut
            return self._optik_cache[schluessel]                      # wiederverwenden
        bild = None                                                   # Vorgabe: kein Bild
        try:                                                          # geglaetteter Weg mit Pillow
            if str(art) == "hintergrund":                             # Gebaeudeansicht
                roh = gebaeude_optik.hintergrund(str(gebaeude_id), int(breite), hoehe)   # gemalte Szene
            else:                                                     # Menue und Bauauswahl
                roh = gebaeude_optik.kachel(str(gebaeude_id), int(breite), hoehe)        # gerahmtes Icon
            if roh is not None:                                       # Bild wirklich vorhanden
                from PIL import ImageTk                               # nur hier - das Spiel laeuft auch ohne
                bild = ImageTk.PhotoImage(roh)                        # Tk-Grafik daraus
        except Exception:                                             # noqa: BLE001 - kein Pillow, kein Absturz
            bild = None                                               # dann greift der Rueckfall unten
        if bild is None:                                              # kein Pillow oder kein Bild daraus
            bild = self._optik_bild_ohne_pillow(gebaeude_id, int(breite), str(art))   # groeber, aber sichtbar
        self._optik_cache[schluessel] = bild                          # im Cache halten
        return bild                                                   # an den Aufrufer

    def _optik_bild_ohne_pillow(self, gebaeude_id, breite: int, art: str = "kachel"):
        """Rueckfall ohne Bildverarbeitung: die gelieferte Datei mit Tk laden und ganzzahlig teilen.

        `subsample` verkleinert nur um ganze Faktoren - aus 256 px werden bei 20 px Ziel also
        21 px (Faktor 12). Das ist groeber als LANCZOS, aber es ist da; ohne diesen Weg saehe der
        Spieler bei fehlendem Pillow gar keine Gebaeude-Optik.
        """
        pfad = (gebaeude_optik.pfad_hintergrund(str(gebaeude_id)) if str(art) == "hintergrund"
                else gebaeude_optik.pfad_icon(str(gebaeude_id)))      # passende Datei zur Art
        if not pfad or not os.path.exists(pfad):                      # Datei fehlt
            return None                                               # dann bleibt es beim Text
        try:                                                          # Tk kann PNG selbst lesen
            bild = tk.PhotoImage(file=pfad)                            # Originalgroesse laden
            faktor = max(1, int(round(bild.width() / float(max(1, int(breite))))))   # ganzzahliger Faktor
            if faktor > 1:                                            # nur verkleinern, nie vergroessern
                bild = bild.subsample(faktor)                          # gleichmaessig teilen
            return bild                                                # grobes, aber sichtbares Bild
        except Exception:                                             # noqa: BLE001 - kein Tk-Bild moeglich
            return None                                               # dann bleibt es beim Text

    def _menue_icon(self, punkt: str, px: int = 20):
        """Das gerahmte Gebaeude-Icon eines Menuepunkts (None fuer Weltpunkte ohne Gebaeude)."""
        return self._optik_bild(MENU_GEBAEUDE.get(punkt), px, None, "kachel")

    def _kasten_label(self, text: str, schrift=None, farbe=None, breite: int = None,
                      innen: int = 12, pady: int = 3, anchor: str = "w", umbruch: int = None):
        """Ein Textfeld mit weichem, abgerundetem Kasten vor dem Bildhintergrund (B-6, 02.11.2026).

        Daniel: "Die texte muessen erkennbar bleiben also kleinere textbloecke die nicht transparent
        sind und der rest so transparent das moeglichst viel vom bild durchkommt" - und danach
        "die texte und ihre textfelder ... weil es optisch noch keine schoenen uebergaenge sind".
        Deshalb zeichnet `gebaeude_optik.kasten_bild` einen abgerundeten Kasten mit Verlauf (oben
        fast deckend, unten durchscheinend) und feinem Rand; der Text liegt MITTIG darauf (`compound`).
        Ohne Pillow entsteht ein normales Textfeld - die Ansicht bleibt lesbar.
        """
        schrift = schrift or ("TkDefaultFont", 10)                     # Standardschrift
        farbe = farbe or self.skin["text"]                             # Standardfarbe
        try:
            import tkinter.font as tkfont                              # Schriften messen
            fm = tkfont.Font(font=schrift)                             # Messschrift
            textbreite = fm.measure(str(text))                         # Breite des Textes
            texthoehe = fm.metrics("linespace")                        # Hoehe einer Zeile
        except Exception:                                              # noqa: BLE001
            textbreite, texthoehe = 320, 18                            # grobe Vorgabe
        if umbruch:                                                    # mehrzeilig: feste Breite
            textbreite = min(int(umbruch), max(textbreite, 240))
            texthoehe = texthoehe * max(1, int(len(str(text)) / max(1, textbreite / 7.0)) + 1)
        kaesten_b = int(breite or (textbreite + 2 * innen))            # Breite des Kastens
        kaesten_h = int(texthoehe + 2 * innen)                         # Hoehe des Kastens
        bild = self._kasten_bild(kaesten_b, kaesten_h)                 # der weiche Kasten
        kwargs = {"text": text, "fg": farbe, "font": schrift, "justify": "left",
                  "anchor": anchor, "padx": 0, "pady": 0}
        if umbruch:                                                    # Umbruch nur mit Breite
            kwargs["wraplength"] = int(umbruch)
        if bild is not None:                                           # mit Bild: Text auf dem Kasten
            kwargs.update({"image": bild, "compound": "center", "bg": self.skin["bg"]})
        else:                                                          # ohne Bild: normales Feld
            kwargs["bg"] = self.skin["panel"]
        label = tk.Label(self.content, **kwargs)                       # das Textfeld
        if bild is not None:                                           # Referenz gegen Tk-Freigabe
            label.image = bild
        label.pack(anchor=tk.W, padx=10, pady=(0, pady))
        return label

    def _kasten_bild(self, breite: int, hoehe: int):
        """Der Kastenhintergrund als Tk-Grafik (gecacht nach Groesse) - None ohne Pillow."""
        if not hasattr(self, "_kasten_cache"):                         # Cache beim ersten Kasten
            self._kasten_cache = {}                                    # (Breite, Hoehe) -> Tk-Bild
        schluessel = (int(breite), int(hoehe))                         # gleiche Groesse, gleiches Bild
        if schluessel in self._kasten_cache:                           # schon gebaut
            return self._kasten_cache[schluessel]                      # wiederverwenden
        bild = None                                                    # Vorgabe: kein Bild
        e = hintergrund_einstellungen()                                # Kastenwerte aus der Datendatei
        kasten = e.get("kasten") if isinstance(e.get("kasten"), dict) else {}
        try:                                                           # Pillow-Weg
            roh = gebaeude_optik.kasten_bild(
                int(breite), int(hoehe),
                radius=int(kasten.get("radius") or 12),
                oben_alpha=int(kasten.get("oben_deckkraft") or 245),
                unten_alpha=int(kasten.get("unten_deckkraft") or 200),
                rand_alpha=int(kasten.get("rand_deckkraft") or 90),
                farbe=tuple(kasten.get("farbe") or (22, 17, 12)))
            if roh is not None:                                        # Bild entstanden
                from PIL import ImageTk                                 # nur hier importieren
                bild = ImageTk.PhotoImage(roh)                          # Tk-Grafik daraus
        except Exception:                                               # noqa: BLE001
            bild = None                                                 # dann ohne Bild
        self._kasten_cache[schluessel] = bild                           # im Cache halten
        return bild                                                     # an den Aufrufer

    def _ansicht_hintergrund(self, gebaeude_id, breite: int = None, hoehe: int = None):
        """Das Gebaeudemotiv als HINTERGRUND der ganzen Ansicht (B-6, Vorgabe Daniel 02.11.2026).

        Daniel: "die bilder fuer dorfzentrum oder Stellmacher oder Kriegerakademi sollen die
        hintergruende werden von den jeweiligen fenstern und nicht einfach als bild oben drueber"
        und "die texte muessen erkennbar bleiben also kleinere textbloecke die nicht transparent
        sind und der rest so transparent das moeglichst viel vom bild durchkommt".

        Umgesetzt als eigene Flaeche, die ZUERST in `self.content` erzeugt wird: alles, was danach
        gepackt wird, liegt darueber. Die Texte selbst sind deckende Felder (ihre eigene
        Hintergrundfarbe) - dazwischen bleibt das Bild sichtbar.
        Ohne Bild (kein Pillow, Datei fehlt, Schalter aus) bleibt die Ansicht wie vorher.
        """
        e = hintergrund_einstellungen()                                    # Masse aus der Datendatei
        if not e.get("aktiv", True):                                       # Schalter aus
            return None                                                    # dann keine Ebene
        b = int(breite or e.get("breite") or 980)                          # Breite der Flaeche
        h = int(hoehe or e.get("hoehe") or 760)                            # Hoehe der Flaeche
        bild = self._optik_flaeche(gebaeude_id, b, h, e.get("abdunkeln_prozent") or 0.0,
                                   e.get("weichzeichnen_px") or 0.0)
        if bild is None:                                                   # kein Bild vorhanden
            return None                                                    # Ansicht unveraendert
        leinwand = tk.Canvas(self.content, width=b, height=h, bg=self.skin["bg"],
                             highlightthickness=0, bd=0)                   # die Flaeche
        # M-3 (Daniels Befund 02.11.2026: "die hintergrundbilder werden nicht angepasst"): die
        # Flaeche liegt jetzt mit relativer Breite und Hoehe im Inhaltsbereich und wird bei jeder
        # Groessenaenderung nachgezogen (`_hintergrund_anpassen`). Vorher blieb sie bei 980 x 760
        # stehen - im maximierten Fenster endete das Bild mitten in der Ansicht und rechts davon war
        # nur die Fensterfarbe zu sehen (gemessen: Inhalt 1142 x 1120, Flaeche 980 x 760).
        leinwand.place(x=0, y=0, relwidth=1.0, relheight=1.0)              # fuellt den Inhalt
        leinwand.create_image(0, 0, anchor=tk.NW, image=bild,
                              tags=("hintergrundbild",))                   # Bild einsetzen
        leinwand.image = bild                                              # Referenz gegen Tk-Freigabe
        self._hintergrund_flaeche = leinwand                               # fuer das Nachziehen
        self._hintergrund_kennung = gebaeude_id                            # welches Motiv
        self._hintergrund_einstellung = e                                  # Abdunkeln und Weichzeichnen
        self._hintergrund_groesse = (b, h)                                 # zuletzt gebaute Groesse
        leinwand.bind("<Configure>", lambda _ereignis: self._hintergrund_anpassen())
        self.root.after(60, self._hintergrund_anpassen)                    # nach dem ersten Layout
        return leinwand                                                    # fuer Pruefungen

    def _hintergrund_anpassen(self) -> None:
        """Die Hintergrundflaeche auf die Groesse des Inhalts nachziehen (M-3, 02.11.2026).

        Daniel im maximierten Fenster: "die hintergrundbilder [werden] nicht angepasst" - das Bild
        endete mitten in der Ansicht. Hier wird bei jeder Groessenaenderung ein NEUES Bild in der
        Zielgroesse gebaut (cover, mittig beschnitten, abgedunkelt und weichgezeichnet wie in der
        Datendatei) und in die Leinwand eingesetzt. Gebaut wird erst nach kurzer Ruhe und in
        Schritten von 64 px, damit ein Fensterziehen nicht bei jedem Pixel ein Bild kostet.
        """
        leinwand = getattr(self, "_hintergrund_flaeche", None)              # die Flaeche dieser Ansicht
        if leinwand is None:                                                # keine Flaeche gezeichnet
            return                                                          # nichts zu tun
        try:                                                                # Fenster kann schon weg sein
            if not leinwand.winfo_exists():                                 # Flaeche zerstoert
                return                                                      # dann nichts tun
            breite = int(leinwand.winfo_width())                            # tatsaechliche Breite
            hoehe = int(leinwand.winfo_height())                            # tatsaechliche Hoehe
        except tk.TclError:                                                 # Tk kennt sie nicht mehr
            return                                                          # Abbruch
        if breite < 120 or hoehe < 120:                                     # vor dem ersten Layout
            return                                                          # spaeter noch einmal
        schritt = 64                                                        # Groesse je Bauvorgang
        ziel = (max(schritt, (breite // schritt) * schritt),
                max(schritt, (hoehe // schritt) * schritt))                 # auf 64 px abgerundet
        letzte = getattr(self, "_hintergrund_groesse", None) or (0, 0)      # zuletzt gebaute Groesse
        if abs(int(letzte[0]) - ziel[0]) < schritt and abs(int(letzte[1]) - ziel[1]) < schritt:
            return                                                          # praktisch unveraendert
        kennung = getattr(self, "_hintergrund_kennung", None)               # welches Motiv
        if not kennung:                                                     # ohne Kennung kein Bild
            return                                                          # Abbruch
        e = getattr(self, "_hintergrund_einstellung", None) or {}           # Masse der Datendatei
        # Kurz warten, damit ein laufendes Ziehen nicht jedes Zwischenmass baut.
        alt_auftrag = getattr(self, "_hintergrund_auftrag", None)           # laufender Auftrag?
        if alt_auftrag is not None:                                         # ja: verwerfen
            try:
                self.root.after_cancel(alt_auftrag)                         # nur der letzte zaehlt
            except tk.TclError:
                pass
        self._hintergrund_auftrag = self.root.after(
            120, lambda: self._hintergrund_bauen(kennung, ziel[0], ziel[1], e))

    def _hintergrund_bauen(self, kennung, breite: int, hoehe: int, e: dict) -> None:
        """Das Bild in der Zielgroesse bauen und einsetzen (Teil von `_hintergrund_anpassen`)."""
        self._hintergrund_auftrag = None                                   # Auftrag ist erledigt
        leinwand = getattr(self, "_hintergrund_flaeche", None)             # die Flaeche
        if leinwand is None:                                               # keine Flaeche mehr
            return                                                         # Abbruch
        try:
            if not leinwand.winfo_exists():                                # zerstoert
                return                                                     # Abbruch
        except tk.TclError:
            return
        bild = self._optik_flaeche(kennung, int(breite), int(hoehe),       # cover, abgedunkelt
                                   (e or {}).get("abdunkeln_prozent") or 0.0,
                                   (e or {}).get("weichzeichnen_px") or 0.0)
        if bild is None:                                                   # kein Bild moeglich
            return                                                         # dann bleibt das alte
        try:
            leinwand.itemconfigure("hintergrundbild", image=bild)          # Bild austauschen
        except tk.TclError:                                                # Kennung fehlt
            return
        leinwand.image = bild                                              # Referenz halten
        self._hintergrund_groesse = (int(breite), int(hoehe))              # neue Groesse merken

    def _optik_flaeche(self, gebaeude_id, breite: int, hoehe: int, abdunkeln: float = 0.0,
                       weich: float = 0.0):
        """Die gedeckte Bildflaeche als Tk-Grafik (gecacht) - ohne Pillow grob ueber Tk."""
        if not gebaeude_id:                                                # ohne Kennung kein Bild
            return None                                                    # dann nichts
        if not hasattr(self, "_flaeche_cache"):                            # Cache beim ersten Bild
            self._flaeche_cache = {}                                       # Anfrage -> Tk-Bild
        schluessel = (str(gebaeude_id), int(breite), int(hoehe), float(abdunkeln), float(weich))
        if schluessel in self._flaeche_cache:                              # schon gebaut
            return self._flaeche_cache[schluessel]                         # wiederverwenden
        bild = None                                                        # Vorgabe: kein Bild
        try:                                                               # geglaetteter Weg
            roh = gebaeude_optik.hintergrund_flaeche(str(gebaeude_id), int(breite), int(hoehe),
                                                    float(abdunkeln), float(weich))
            if roh is not None:                                            # Bild vorhanden
                from PIL import ImageTk                                     # nur hier importieren
                bild = ImageTk.PhotoImage(roh)                             # Tk-Grafik daraus
        except Exception:                                                  # noqa: BLE001
            bild = None                                                    # dann Rueckfall unten
        if bild is None:                                                   # ohne Pillow: Tk selbst
            bild = self._optik_bild_ohne_pillow(gebaeude_id, int(breite), "hintergrund")
        self._flaeche_cache[schluessel] = bild                             # im Cache halten
        return bild                                                        # an den Aufrufer

    def _gebaeude_kopf(self, gebaeude_id, breite: int = 538):
        """Die Gebaeudeansicht bekommt den gemalten Hintergrund (538 x 222) unter ihre Ueberschrift.

        Ohne Bild (kein Pillow, Datei fehlt) wird nichts gezeichnet - die Ansicht bleibt dann genau
        wie vorher. Die Masse kommen aus der Lieferung, nicht aus dem Fenster: der Hintergrund ist
        ein Menuebild, kein dehnbarer Balken (Lehre 02.11.2026 zur Ressourcenleiste).
        """
        bild = self._optik_bild(gebaeude_id, breite, None, "hintergrund")   # Szene laden
        if bild is None:                                                    # kein Bild vorhanden
            return None                                                     # Ansicht unveraendert
        leinwand = tk.Canvas(self.content, width=bild.width(), height=bild.height(),
                             bg=self.skin["bg"], highlightthickness=0, bd=0)  # Flaeche in Bildgroesse
        leinwand.pack(anchor=tk.W, padx=10, pady=(0, 6))                     # linksbuendig unter dem Titel
        leinwand.create_image(0, 0, anchor=tk.NW, image=bild)                # Szene oben links einsetzen
        leinwand.image = bild                                                # Referenz gegen Tk-Freigabe
        return leinwand                                                      # fuer Pruefungen

    def _stufenpips_zeichnen(self, canvas, x0: float, y0: float, zelle: float,
                             stufe: float, feld: int) -> None:
        """Die Ausbaustufe als kleine Punkte unter einem Originalmotiv (A-2).

        Bei den gezeichneten Baukoerpern kommen die Punkte aus `karten_optik_fein`; beim
        Handbuchbild fehlen sie, deshalb stehen sie hier - gleiche Bedeutung, gleiche Stelle
        (die Legende sagt: "die Punkte unter einem Gebäude zeigen seine Ausbaustufe").
        """
        try:
            anzahl = max(0, min(5, int(stufe)))
        except (TypeError, ValueError):
            return
        if anzahl <= 0:
            return
        _groesse, _abstand = 4, 6
        _breite = anzahl * _abstand - (_abstand - _groesse)
        _start = x0 + (zelle - _breite) / 2
        _y = y0 + zelle - 7
        for k in range(anzahl):
            px = _start + k * _abstand
            canvas.create_rectangle(px, _y, px + _groesse, _y + _groesse,
                                    fill="#F5D76E", outline="#7a5c14",
                                    tags=(f"feld:{feld}", "stufenpip"))

    def _build_loading_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg="#2a0605")
        frame = tk.Frame(self.root, bg="#2a0605")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        tk.Label(frame, text="Nebelseetal", font=("Blackletter", 48, "bold"), fg="#FFCC33", bg="#2a0605").pack(pady=(0, 10))
        tk.Label(frame, text="Remake", font=("Blackletter", 24), fg="#FF6600", bg="#2a0605").pack(pady=(0, 20))
        self.lbl_loading = tk.Label(frame, text="Lade Spielwelt...", font=("Arial", 12), fg="#FFFF99", bg="#2a0605")
        self.lbl_loading.pack()
        self.root.after(100, self._loading_tick)

    def _loading_tick(self):
        try:
            if not hasattr(self, "_loading_step"):
                self._loading_step = 0
            self._loading_step += 1
            if self._loading_step >= 5:
                self._build_main_ui()
            else:
                self.root.after(100, self._loading_tick)
        except Exception as e:
            print("LOADING_ERROR", e)
            self.root.after(500, self._build_main_ui)

    def _cycle_skin(self):
        names = list(SKINS.keys())
        idx = names.index(self.skin_name)
        self.skin_name = names[(idx + 1) % len(names)]
        self.skin = SKINS[self.skin_name]
        self._build_main_ui()
        self._log(f"Skin gewechselt: {self.skin_name}")

    def _leisten_bild(self, breite: int):
        """Das zusammengesetzte Leistenbild als Tk-Bild (oder None), je Zielbreite zwischengespeichert.

        Die Arbeit macht `leiste_zusammensetzen` (ohne Tk, damit pruefbar): feste Kacheln wachsen
        gleichmaessig, nur die Luecken werden gedehnt. Hier wird daraus nur die Tk-Grafik gebaut und
        im Cache gehalten - Tk gibt Bilder ohne Referenz frei, dann bliebe der Streifen leer.
        """
        if not RESSOURCENLEISTE:                                              # keine Leiste eingetragen
            return None, {}, 0.0                                              # Kopf bleibt wie vorher
        if not hasattr(self, "_leisten_cache"):                               # Cache beim ersten Bild
            self._leisten_cache = {}                                          # Breite -> (Tk-Bild, Masse)
        schluessel = int(breite)                                              # nur die Breite zaehlt
        if schluessel in self._leisten_cache:                                  # schon gebaut
            return self._leisten_cache[schluessel]                            # wiederverwenden
        bild, mitten, skala = leiste_zusammensetzen(RESSOURCENLEISTE, int(breite))   # Stuecke zusammensetzen
        if bild is None:                                                      # kein Bild moeglich (kein Pillow?)
            return None, {}, 0.0                                              # dann bleibt der Kopf textbasiert
        try:                                                                  # Tk-Grafik bauen
            from PIL import ImageTk                                           # nur hier importiert
            tk_bild = ImageTk.PhotoImage(bild)                                # aus dem PIL-Bild
        except Exception:                                                     # noqa: BLE001
            return None, {}, 0.0                                              # ohne Bildschirm keine Leiste
        self._leisten_cache[schluessel] = (tk_bild, mitten, skala)             # im Cache halten
        return tk_bild, mitten, skala                                          # Bild, Mittelpunkte, Skala

    def _leiste_bauen(self, eltern):
        """Die Ressourcenleiste als Canvas in den Kopf haengen (Bild + acht Zahlenfelder)."""
        if not RESSOURCENLEISTE:                                              # keine Leiste eingetragen
            self._leisten_canvas = None                                        # dann nur die Textzeilen
            return None                                                        # nichts zu bauen
        canvas = tk.Canvas(eltern, height=int(RESSOURCENLEISTE.get("hoehe") or 140),   # Hoehe wie im Original
                           bg=self.skin["topbar"], highlightthickness=0, bd=0)          # ohne Rahmen
        canvas.pack(fill=tk.X, pady=(0, 2))                                    # volle Breite, direkt unter dem Titel
        self._leisten_canvas = canvas                                          # Referenz fuer das Neuzeichnen
        self._leisten_texte = {}                                               # Feld -> Canvas-Kennungen
        canvas.bind("<Configure>", lambda _e: self._leiste_zeichnen())          # bei Breitenaenderung neu zeichnen
        self.root.after(30, self._leiste_zeichnen)                              # nach dem ersten Layout zeichnen
        return canvas                                                          # fuer Pruefungen

    def _leiste_zeichnen(self):
        """Die Leiste in der aktuellen Breite zeichnen: zusammengesetztes Bild plus acht Zahlen.

        Die Positionen der Zahlen kommen aus der Zusammensetzung (`leiste_zusammensetzen`), nicht
        aus festen Pixeln - dadurch sitzt jede Zahl auch dann mittig in ihrer Plakette, wenn die
        Luecken gedehnt wurden.
        """
        canvas = getattr(self, "_leisten_canvas", None)                        # Zeichenflaeche
        if canvas is None or not RESSOURCENLEISTE:                             # nichts zu zeichnen
            return                                                             # Abbruch
        try:                                                                   # Fenster kann schon weg sein
            if not canvas.winfo_exists():                                      # Flaeche zerstoert
                return                                                         # dann nichts tun
        except tk.TclError:                                                    # Tk kennt sie nicht mehr
            return                                                             # Abbruch
        breite_ist = int(canvas.winfo_width())                                 # tatsaechliche Breite
        if breite_ist <= 1:                                                    # vor dem ersten Layout
            breite_ist = int(RESSOURCENLEISTE.get("breite") or 1440)           # Originalbreite nehmen
        if getattr(self, "_leisten_breite", None) == breite_ist:               # Breite unveraendert
            return                                                             # kein Neuzeichnen noetig
        bild, mitten, skala = self._leisten_bild(breite_ist)                    # Stuecke zusammensetzen
        if bild is None:                                                       # kein Bild verfuegbar
            return                                                             # dann bleibt der Kopf textbasiert
        canvas.delete("leiste")                                                # alte Zeichnung weg
        canvas.configure(height=bild.height())                                  # Flaeche an das Bild anpassen
        canvas.create_image(0, 0, anchor="nw", image=bild, tags=("leiste",))    # das Bild selbst
        self._leisten_bild_ref = bild                                          # Referenz gegen Garbage Collection
        farben = RESSOURCENLEISTE.get("farben") or {}                           # Farben aus der Datendatei
        zahl_farbe = str(farben.get("zahl") or "#F7E9C8")                      # helle Zahl
        kontur = str(farben.get("kontur") or "#101418")                        # dunkle Kontur
        schrift = ("Arial", max(8, int(round(11 * skala))), "bold")            # mit der Leiste skalieren
        self._leisten_texte = {}                                               # neu aufbauen
        for feld in RESSOURCENLEISTE.get("felder") or []:                      # acht Felder
            mitte = mitten.get(str(feld.get("schluessel")))                    # Mittelpunkt aus der Zusammensetzung
            if not mitte:                                                      # Feld nicht gefunden
                continue                                                       # ueberspringen
            x, y = int(mitte[0]), int(mitte[1])                                # Zahlenmitte in Pixeln
            kennungen = []                                                     # alle Texte dieses Feldes
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):                  # Kontur vierfach versetzt
                kennungen.append(canvas.create_text(x + dx, y + dy, text="0", fill=kontur,
                                                    font=schrift, tags=("leiste",)))   # dunkle Kontur
            kennungen.append(canvas.create_text(x, y, text="0", fill=zahl_farbe,
                                                font=schrift, tags=("leiste",)))   # helle Zahl darueber
            self._leisten_texte[str(feld.get("schluessel"))] = kennungen        # fuer das Aktualisieren merken
        self._leisten_breite = breite_ist                                      # gezeichnete Breite merken
        self._leiste_aktualisieren()                                           # Werte einsetzen

    def _leiste_aktualisieren(self):
        """Die acht Zahlen der Leiste aus dem Spielstand setzen (Rechenstelle: `leistenwert`)."""
        canvas = getattr(self, "_leisten_canvas", None)                        # Zeichenflaeche
        texte = getattr(self, "_leisten_texte", {}) or {}                      # Feld -> Kennungen
        if canvas is None or not texte or not RESSOURCENLEISTE:                # nichts zu tun
            return                                                             # Abbruch
        for feld in RESSOURCENLEISTE.get("felder") or []:                      # acht Felder
            wert = leistenwert(self.state, feld)                               # EINE Rechenstelle
            for kennung in texte.get(str(feld.get("schluessel"))) or []:       # fuenf Texte je Feld
                try:                                                           # Flaeche kann weg sein
                    canvas.itemconfig(kennung, text=wert)                      # neuen Wert setzen
                except tk.TclError:                                            # Flaeche zerstoert
                    return                                                     # Abbruch

    def _build_main_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg=self.skin["bg"])

        # FIX04i: Die fruehere einzelne 40px-Zeile wurde auf kleineren Fenstern
        # von Reichsressourcen und acht Aktionsknopflaechen ueberfuellt.
        # Getrennte Zeilen garantieren die Bedienbarkeit des Admin-Spielstandknopfs,
        # ohne Rohstoffe oder Aktionen zu verbergen. Keine festen Zeilenhoehen:
        # Windows-DPI-Skalierung darf die Beschriftungen nicht abschneiden.
        top = tk.Frame(self.root, bg=self.skin["topbar"])
        top.pack(fill=tk.X, side=tk.TOP)
        # C2-Ressourcenleiste (Register 121): gemaltes Bild mit acht Zahlenfeldern ueber den Textzeilen.
        # Sie zeigt die MENGEN; die Textzeilen darunter zeigen die Raten (keine Zahl doppelt im Kopf).
        self._leiste_bauen(top)
        ressourcen_oben = tk.Frame(top, bg=self.skin["topbar"])
        ressourcen_oben.pack(fill=tk.X)
        ressourcen_unten = tk.Frame(top, bg=self.skin["topbar"])
        ressourcen_unten.pack(fill=tk.X)
        aktionsleiste = tk.Frame(top, bg=self.skin["topbar"])
        aktionsleiste.pack(fill=tk.X, pady=(2, 3))
        self.aktionsleiste = aktionsleiste  # Fuer Layout-Regressionstests.

        tk.Label(ressourcen_oben, text="Nebelseetal", font=("Blackletter", 14, "bold"),
                 fg=self.skin["gold"], bg=self.skin["topbar"]).pack(side=tk.LEFT, padx=(8, 12))
        # Zwei kurze Ressourcenzeilen statt horizontaler Ueberlagerung mit Buttons.
        # Anzeige bleibt Reichsbestand, die Ortslager bleiben Buchungsquelle.
        tk.Label(ressourcen_oben, text="Reich:", fg=self.skin["gold"],
                 bg=self.skin["topbar"], font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=(2, 4))
        self.res_labels_top = {}
        ertrag_jetzt = self.state.stundenertrag()
        for index, r in enumerate(RESOURCES):
            zeile = ressourcen_oben if index < 4 else ressourcen_unten
            text, warnung = kopfzeile_fuer(self.state, r, ertrag_jetzt)
            lbl = tk.Label(zeile, text=text,
                           fg=("#FDBA74" if warnung else self.skin["text"]),
                           bg=self.skin["topbar"], font=("Arial", 9))
            lbl.pack(side=tk.LEFT, padx=5)
            self.res_labels_top[r] = lbl
        self.lbl_day = tk.Label(ressourcen_unten, text=f"Tag {self.state.day}",
                                fg=self.skin["gold"], bg=self.skin["topbar"])
        self.lbl_day.pack(side=tk.RIGHT, padx=10)
        self.lbl_tempo = tk.Label(ressourcen_unten, text=f"Tempo {spielzeit.text()}",
                                  fg=self.skin["text"], bg=self.skin["topbar"],
                                  font=("Arial", 9))
        self.lbl_tempo.pack(side=tk.RIGHT, padx=10)

        # Spielfunktionen und Admin-Funktionen teilen sich ausschliesslich die
        # Aktionszeile, niemals die laengere Ressourcenanzeige.
        aktionsknopfe = [("Spielerhilfe", lambda: self._switch_view("Anleitung")),
                          ("Skin", self._cycle_skin), ("Profil wechseln", self._profil_zurueck),
                          ("Beenden", self.root.quit)]
        if (not ausgabemodus.ist_oeffentliche_testversion() and
                self._profil == "admin" and self._admin_sitzung_freigegeben):
            aktionsknopfe[:0] = [("Admin sichern", self._admin_speichern),
                                 ("Admin laden", self._admin_laden),
                                 ("Admin-Werkzeuge", self._admin_werkzeuge_dialog),
                                 ("Admin-Spielstaende", lambda: self._spielstand_verwaltung("admin"))]
        else:
            aktionsknopfe[:0] = [("Speichern", self._save), ("Laden", self._load),
                                 ("Spielstaende", lambda: self._spielstand_verwaltung("spieler"))]
        self.aktionsknopfe = {}
        for txt, cmd in aktionsknopfe:
            btn = tk.Button(aktionsleiste, text=txt, command=cmd, bg=self.skin["button"],
                            fg=self.skin["gold"], relief=tk.FLAT, padx=7, pady=3)
            btn.pack(side=tk.RIGHT, padx=3)
            self.aktionsknopfe[txt] = btn

        # Statuszeile unten: muss VOR dem expandierenden main-Frame gepackt werden,
        # sonst frisst main den ganzen Platz und die Zeile bleibt 1 px hoch.
        self.lbl_status = tk.Label(self.root, text="Willkommen in Nebelseetal.", fg=self.skin["text"],
                                   bg=self.skin["topbar"], anchor=tk.W, font=("Arial", 9), padx=8)
        self.lbl_status.pack(fill=tk.X, side=tk.BOTTOM)

        main = tk.Frame(self.root, bg=self.skin["bg"])
        main.pack(fill=tk.BOTH, expand=True)

        left = tk.Frame(main, bg=self.skin["sidebar"], width=180)
        left.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame = left
        # Zwei Navigationsebenen wie im Original (GameStar-Screenshots): "Uebersicht" fuer die
        # Welt (Portal, Diplomatie, Punkte) und "Siedlung" fuer die Dorfbereiche.
        self.ebene = getattr(self, "ebene", "Siedlung")
        ebenen_leiste = tk.Frame(left, bg=self.skin["sidebar"])
        ebenen_leiste.pack(fill=tk.X, padx=4, pady=(6, 4))
        self.ebene_buttons = {}
        for ebene in EBENEN:
            knopf = tk.Button(ebenen_leiste, text=ebene, relief=tk.FLAT,
                              fg=self.skin["red"], bg=self.skin["button"],
                              activebackground=self.skin["button_active"],
                              activeforeground=self.skin["gold"],
                              command=lambda e=ebene: self._ebene_wechseln(e))
            knopf.pack(fill=tk.X, pady=1, ipady=2)
            self.ebene_buttons[ebene] = knopf
        tk.Label(left, text="Menü", fg=self.skin["gold"], bg=self.skin["sidebar"], font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=8, pady=(4, 4))
        # Daniel 30.10.2026: Menuepunkte erscheinen erst mit ihrem Gebaeude. Die Knoepfe stehen
        # deshalb in einem eigenen Rahmen, der bei jedem Bau und Abriss neu gefuellt wird.
        self.menu_liste = tk.Frame(left, bg=self.skin["sidebar"])
        self.menu_liste.pack(fill=tk.X)
        self.menu_buttons = {}
        self._menue_auffrischen()
        # "Eure Punkte" steht im Original dauerhaft in der Leiste (Forschung / Krieg / Gesamt).
        self.punkte_leiste = tk.Frame(left, bg=self.skin["sidebar"])
        self.punkte_leiste.pack(fill=tk.X, pady=(12, 2))
        tk.Label(self.punkte_leiste, text="Eure Punkte", fg=self.skin["gold"],
                 bg=self.skin["sidebar"], font=("Arial", 9, "bold")).pack(anchor=tk.W, padx=8)
        self.punkte_labels = {}
        for _name in ("Forschung", "Krieg", "Gesamt"):
            _lbl = tk.Label(self.punkte_leiste, text=f"{_name}: 0", fg=self.skin["red"],
                            bg=self.skin["sidebar"], font=("Arial", 9))
            _lbl.pack(anchor=tk.W, padx=12)
            self.punkte_labels[_name] = _lbl
        # Auszeichnungen statt Siegziel (E5, Paket A3): zwei schmale Zeilen unter den Punkten.
        for _key in ("Auszeichnungen_1", "Auszeichnungen_2"):
            _lbl = tk.Label(self.punkte_leiste, text="-", fg=self.skin["text"],
                            bg=self.skin["sidebar"], font=("Arial", 8))
            _lbl.pack(anchor=tk.W, padx=12)
            self.punkte_labels[_key] = _lbl
        self._punkte_leiste_aktualisieren()

        tk.Frame(left, height=16, bg=self.skin["sidebar"]).pack()
        tk.Label(left, text="Nebelseetal unterstützen", fg=self.skin["gold"], bg=self.skin["sidebar"], font=("Arial", 8)).pack(anchor=tk.W, padx=8)
        tk.Label(left, text="Logout", fg=self.skin["red"], bg=self.skin["sidebar"], font=("Arial", 8)).pack(anchor=tk.W, padx=8, pady=(2, 6))

        # Rollbarer Inhaltsbereich. Gemessen am 04.10.2026: Lager braucht 1152 px, Kaserne 1379 px,
        # das Fenster zeigt nur 720 px — ohne Rollen fehlte die untere Haelfte (Waren waren
        # sichtbar, die Einheiten nicht).
        inhalt_rahmen = tk.Frame(main, bg=self.skin["bg"])
        inhalt_rahmen.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6, pady=6)
        self.content_canvas = tk.Canvas(inhalt_rahmen, bg=self.skin["bg"], highlightthickness=0, bd=0)
        self.content_scroll = tk.Scrollbar(inhalt_rahmen, orient=tk.VERTICAL,
                                           command=self.content_canvas.yview)
        self.content_canvas.configure(yscrollcommand=self.content_scroll.set)
        self.content_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.content_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.content = tk.Frame(self.content_canvas, bg=self.skin["bg"])
        self._content_fenster = self.content_canvas.create_window((0, 0), window=self.content,
                                                                  anchor="nw")
        self.content.bind("<Configure>", lambda e: self.content_canvas.configure(
            scrollregion=self.content_canvas.bbox("all")))
        self.content_canvas.bind("<Configure>", lambda e: self.content_canvas.itemconfigure(
            self._content_fenster, width=e.width))
        self.content_canvas.bind_all("<MouseWheel>", self._rad_rollen)
        self._render_view()

        right = tk.Frame(main, bg=self.skin["sidebar"], width=220)
        right.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Label(right, text="Eure Punkte", fg=self.skin["gold"], bg=self.skin["sidebar"], font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=5, pady=(5, 2))
        self.lbl_forschung = tk.Label(right, text="Forschung: 0", fg=self.skin["text"], bg=self.skin["sidebar"])
        self.lbl_forschung.pack(anchor=tk.W, padx=5)
        self.lbl_krieg = tk.Label(right, text="Krieg: 0", fg=self.skin["text"], bg=self.skin["sidebar"])
        self.lbl_krieg.pack(anchor=tk.W, padx=5)
        self.lbl_gesamt = tk.Label(right, text="Gesamt: 0", fg=self.skin["gold"], bg=self.skin["sidebar"])
        self.lbl_gesamt.pack(anchor=tk.W, padx=5, pady=(0, 10))
        # Punkte statt Siegziel (E5): es gibt keinen Sieg, nur den Stand und die belegte
        # Goetterschutzgrenze. Die Auszeichnungen kommen aus dem Paket A3.
        self.lbl_ziel = tk.Label(right, text="Punkte: 0",
                                 fg=self.skin["text"], bg=self.skin["sidebar"], wraplength=200,
                                 justify=tk.LEFT)
        self.lbl_ziel.pack(anchor=tk.W, padx=5, pady=(0, 10))

        # FIX04c: Eine kleine, nicht-invasive Orientierung nur waehrend des
        # echten Götterschutzes; "Spielerhilfe" und "Anleitung" bleiben immer da.
        self.hilfe_rahmen = tk.Frame(right, bg=self.skin["panel"])
        tk.Label(self.hilfe_rahmen, text="Einstiegshilfe", fg=self.skin["gold"],
                 bg=self.skin["panel"], font=("Arial", 10, "bold")).pack(
                     anchor=tk.W, padx=6, pady=(6, 2))
        self.hilfe_kurztext = tk.Label(self.hilfe_rahmen, text="", fg=self.skin["text"],
                                      bg=self.skin["panel"], wraplength=200,
                                      justify=tk.LEFT, anchor=tk.NW)
        self.hilfe_kurztext.pack(fill=tk.X, padx=6, pady=(0, 4))
        tk.Button(self.hilfe_rahmen, text="Alle Tipps und Fragen",
                  command=lambda: self._switch_view("Anleitung"),
                  bg=self.skin["button"], fg=self.skin["gold"]).pack(
                      anchor=tk.W, padx=6, pady=(0, 6))
        self._spielerhilfe_anzeige_aktualisieren()

        # FIX 1: Tick-Loop starten (Produktion, Tag, Bewegung, Render laufen lassen)
        if not getattr(self, "_tick_started", False):
            self._tick_started = True
            self.root.after(1000, self._tick_loop)

    def _spielerhilfe_begleitend_sichtbar(self) -> bool:
        """Eine Sichtbarkeitsregel fuer alle automatisch angezeigten Hilfekarten.

        Admin-Override gilt ausschliesslich fuer den authentifizierten Teststand;
        der Götterschutz und der manuelle Einstieg zur Hilfe bleiben unveraendert.
        """
        admin_freigabe = (self._profil == "admin" and
                           self._admin_sitzung_freigegeben and
                           getattr(self.state, "admin_teststand", False))
        return spielerhilfe.hilfe_sichtbar(self.state, admin_freigabe=admin_freigabe)

    def _spielerhilfe_aufgabenkarte_sichtbar(self) -> bool:
        """Gruendung + produzierte Grundrohstoffe gehen jeder Ausblendregel vor.

        Diese Pflicht gilt NUR fuer die Dorfzentrum-Karte "Dein naechster Schritt".
        Das rechte allgemeine Hilfepanel bleibt per Admin schaltbar.
        """
        return (spielerhilfe.startaufgabe_pflicht(self.state) or
                self._spielerhilfe_begleitend_sichtbar())

    def _spielerhilfe_anzeige_aktualisieren(self):
        """FIX04e: Seitenleiste UND Dorfzentrum-Hilfekarte synchron steuern."""
        rahmen = getattr(self, "hilfe_rahmen", None)
        if rahmen is None or not rahmen.winfo_exists():
            return
        sichtbar = self._spielerhilfe_begleitend_sichtbar()
        if sichtbar:
            admin_freigabe = (self._profil == "admin" and
                               self._admin_sitzung_freigegeben and
                               getattr(self.state, "admin_teststand", False))
            text = spielerhilfe.kurzinfo(self.state, admin_freigabe=admin_freigabe)
            if self.hilfe_kurztext.cget("text") != text:
                self.hilfe_kurztext.configure(text=text)
            if not rahmen.winfo_manager():
                rahmen.pack(fill=tk.X, padx=5, pady=(2, 8))
        elif rahmen.winfo_manager():
            rahmen.pack_forget()

        # Dorfzentrum-Pflichtkarte hat eine EIGENE Bedingung (Onboarding).
        # Sonst koennte ein Admin mit ausgeblendeter Seitenhilfe die Aufgabe
        # verstecken oder der Tick wuerde bei jeder Sekunde neu rendern.
        aufgabe_sichtbar = self._spielerhilfe_aufgabenkarte_sichtbar()
        if (getattr(self, "current_view", "") == "Dorfzentrum" and
                getattr(self, "_aufgaben_sichtbar_zuletzt", aufgabe_sichtbar) != aufgabe_sichtbar):
            self._render_view()

    def _menue_auffrischen(self):
        """Baut die linke Menueleiste neu — abhaengig von den stehenden Gebaeuden (Daniel 30.10.2026).

        Wird beim Start und nach jedem Bau und Abriss gerufen. EINE Quelle fuer die Auswahl:
        `menu_sichtbar()`; hier steht nur die Darstellung.
        """
        if getattr(self, "menu_liste", None) is None:
            return
        for knopf in (getattr(self, "menu_buttons", None) or {}).values():
            knopf.destroy()
        self.menu_buttons = {}
        ebene = getattr(self, "ebene", "Siedlung")
        for name, knopf in (getattr(self, "ebene_buttons", None) or {}).items():
            try:
                knopf.config(fg=self.skin["gold"] if name == ebene else self.skin["red"],
                             bg=self.skin["button_active"] if name == ebene else self.skin["button"])
            except Exception:
                pass
        for item in menu_fuer_ebene(getattr(self.state, "settlements", None), ebene):
            # C2-Gebaeude-Optik (02.11.2026): das gerahmte Icon links neben dem Text. Nur Punkte,
            # hinter denen ein Gebaeude steht (`MENU_GEBAEUDE`); Weltpunkte wie Portal oder Chat
            # bleiben ohne Bild - ein erfundenes Icon waere keine Quelle.
            _icon = self._menue_icon(item, 20)
            _zusatz = {"image": _icon, "compound": tk.LEFT} if _icon is not None else {}
            btn = tk.Button(self.menu_liste, text=MENU_ANZEIGE.get(item, item), fg=self.skin["red"], bg=self.skin["sidebar"], activebackground=self.skin["button_active"], activeforeground=self.skin["gold"],
                            relief=tk.FLAT, anchor=tk.W, padx=12, command=lambda i=item: self._switch_view(i), **_zusatz)
            btn.pack(fill=tk.X, pady=1, ipady=2)
            self.menu_buttons[item] = btn

    def _punkte_leiste_aktualisieren(self):
        """Zieht "Eure Punkte" in der Seitenleiste nach (EINE Quelle: `state.punktestand()`).

        Seit E5 (Daniel 31.10.2026) haengt darunter die Bewertung: vier Auszeichnungen aus
        `punkte.auszeichnungen` (Paket A3). Es gibt keinen Sieg mehr, also ist das die
        Rueckmeldung, worauf der Lauf zulaeuft - zwei Zeilen, damit die Leiste schmal bleibt.
        """
        labels = getattr(self, "punkte_labels", None)
        if not labels:
            return
        try:
            stand = self.state.punktestand()
        except Exception:
            return
        for name, wert in (("Forschung", stand.get("forschung", 0)),
                           ("Krieg", stand.get("krieg", 0)),
                           ("Gesamt", stand.get("gesamt", 0))):
            knopf = labels.get(name)
            if knopf is not None:
                try:
                    knopf.config(text=f"{name}: {wert}")
                except Exception:
                    pass
        # Auszeichnungen (E5, A3): Kennzahlen belegt, Namen VORSCHLAG. Reine Anzeige.
        zwei = labels.get("Auszeichnungen_1")
        vier = labels.get("Auszeichnungen_2")
        if zwei is None or vier is None:
            return
        try:
            werte = {a["name"]: a["wert"] for a in punkte.auszeichnungen({
                "forschungsstaende": {k: int(v.level) for k, v in self.state.research.items()},
                "einheiten": {k: int(v.count) for k, v in self.state.units.items()},
                "wall_stufe": max([0] + [int(self.wall_stufe_am_ort(o))
                                         for o in self.state.settlements]),
            })}
        except Exception:
            return
        try:
            zwei.config(text=f"Feldherr {werte.get('Feldherr', 0)} · Forscher {werte.get('Forscher', 0)}")
            vier.config(text=f"Händler {werte.get('Händler', 0):g} · Gesamt {werte.get('Gesamtherrscher', 0)}")
        except Exception:
            pass

    def _ebene_wechseln(self, ebene: str):
        """Schaltet zwischen "Uebersicht" und "Siedlung" um (wie das Aufklappmenue im Original).

        Bleibt die bisherige Ansicht in der neuen Ebene nicht vorhanden, wird auf den
        Standardpunkt der Ebene gewechselt — sonst staende der Inhalt ohne Menuepunkt da.
        """
        if ebene not in EBENEN:
            return
        self.ebene = ebene
        self._menue_auffrischen()
        if self.current_view not in self.menu_buttons:
            ziel = "Dorfzentrum" if ebene == "Siedlung" else "Portal"
            if ziel in self.menu_buttons:
                self.current_view = ziel
            elif self.menu_buttons:
                self.current_view = next(iter(self.menu_buttons))
        self._switch_view(self.current_view)

    def _switch_view(self, view: str):
        self.current_view = view
        for item, btn in self.menu_buttons.items():
            btn.config(fg=self.skin["gold"] if item == view else "#e53935")
        self._render_view()
        self._spielerhilfe_anzeige_aktualisieren()

    def _rad_rollen(self, ereignis):
        """Mausrad im Inhaltsbereich — schuetzt sich selbst, falls noch kein Rollbereich da ist."""
        try:
            if self.content_canvas.winfo_exists():
                self.content_canvas.yview_scroll(int(-ereignis.delta / 120), "units")
        except Exception:
            pass

    def _render_view(self):
        # Eine Pruefung darf eine App ohne aufgebaute Oberflaeche benutzen (z. B.
        # tests/test_gebaeude_wirkung.py baut nur den Zustand und ruft Aktionen direkt).
        # Dann gibt es nichts zu zeichnen — die Neuzeichnung ist trotzdem kein Fehler.
        if getattr(self, "content", None) is None:
            return
        for widget in self.content.winfo_children():
            widget.destroy()
        # Punkte stehen im Original dauerhaft in der Leiste (GameStar-Screenshot: "Eure Punkte:
        # Forschung / Krieg / Gesamt"). Sie werden bei jedem Neuzeichnen mitgezogen.
        self._punkte_leiste_aktualisieren()
        # Neue Ansicht immer von oben zeigen, sonst startet sie mitten im Inhalt.
        try:
            self.content_canvas.yview_moveto(0)
        except Exception:
            pass
        mapping = {
            "Dorfzentrum": self._render_overview,
            "Siedlungskarte": self._render_settlement_map,
            "Lager": self._render_storage,
            "Kaserne": self._render_barracks,
            "Voraussetzungen": self._render_voraussetzungen,
            "Neuigkeiten": self._render_neuigkeiten,
            "Stellmacher": self._render_stellmacher,
            "Diebesgilde": self._render_diebesgilde,
            "Marktplatz": self._render_market,
            "Gilde": self._render_guild,
            "Nachrichten": self._render_messages,
            "Portal": self._render_portal,
            # "Karten" ist am 01.11.2026 entfallen (S-2, Daniel M-10) - die alte Weltkarte ist
            # stillgelegt; ihre Aufgabe uebernimmt das Portal (S-5 Geländekaestchen).
            "Forschung": self._render_research,
            "Diplomatie": self._render_diplomacy,
            "Einstellungen": self._render_settings,
            "Ruhmeshalle": self._render_hall_of_fame,
            "Anleitung": self._render_help,
            "Kampfsimulator": self._render_battle_simulator,
            "Forum": self._render_forum,
            "Chat": self._render_chat,
            "Spieler werben": self._render_referral,
            "Spielerprofile": self._render_profiles,
        }
        if self.current_view in mapping:
            mapping[self.current_view]()
        else:
            tk.Label(self.content, text=f"{self.current_view} kommt bald.", fg="#DAA520", bg=self.skin["bg"]).pack(padx=20, pady=20)

    def _render_overview(self):
        # B-6 (02.11.2026, Vorgabe Daniel): das gemalte Dorfzentrum ist der HINTERGRUND der ganzen
        # Ansicht - die Texte liegen als deckende Felder darueber, dazwischen bleibt das Bild sichtbar.
        # Die Flaeche MUSS zuerst entstehen: in Tk liegt, was frueher erzeugt wurde, weiter hinten.
        if self._ansicht_hintergrund("lager") is None:          # kein Bild (Datei/Pillow fehlt)
            self._gebaeude_kopf("lager")                        # dann der alte Kopf ueber dem Inhalt
        # B-6: der Titel steht in einem weichen Kasten (abgerundet, Verlauf) statt in einem harten
        # dunklen Balken - Daniel: "die texte und ihre textfelder ... noch keine schoenen uebergaenge".
        self._kasten_label("Dorfzentrum", ("Blackletter", 20, "bold"), self.skin["gold"],
                           innen=14, pady=6)
        # A2-Vorstufe (03.11.2026): solange keine Siedlung steht und nichts gewaehlt ist, steht hier
        # die Startkartenwahl als eigener Block. Sie ERSETZT das Dorfzentrum NICHT - die Pflichtkarte
        # "Dein naechster Schritt" und der Gruendungsknopf bleiben, wo sie waren (vier Pruefdateien
        # haengen an ihnen).
        self._voelker_wahl_block()          # A2: erst das Volk
        self._startkarte_wahl_block()       # dann das Land
        # A2: das gewaehlte Volk bleibt sichtbar (der Spieler soll wissen, wer er ist) - eine Zeile,
        # die Werte kommen aus `data/voelker.json`, nicht aus dem Code.
        _volk = str(getattr(self.state, "spieler_fraktion", "") or "")
        if _volk:
            _werte = bottaktik.volksattribute({"fraktion": _volk})
            self._kasten_label(
                "Dein Volk: %s - %s / %s" % (_volk, _werte.get("plus") or "-",
                                             _werte.get("minus") or "-"),
                ("TkDefaultFont", 9, "bold"), self.skin["gold"], innen=12, pady=4)

        _grenze = gebaeude_wirkung.bevoelkerungsgrenze(self.state.settlements)

        # FIX04f: "Dein naechster Schritt" ist zwingend, bis die erste
        # Siedlung Holz, Stein und Nahrung durch echte Gebaeude erwirtschaftet.
        # Danach folgen die gewohnten Schutz-/Admin-Anzeigeregeln.
        self._aufgaben_sichtbar_zuletzt = self._spielerhilfe_aufgabenkarte_sichtbar()
        if self._aufgaben_sichtbar_zuletzt:
            _schritt = self.naechster_schritt()
            # B-6: die Aufgabenkarte ist kein harter blauer Balken mehr, sondern zwei weiche
            # Textfelder auf dem Bild - der Knopf bleibt ein Knopf (der ist immer deckend).
            self._kasten_label("Dein nächster Schritt", ("TkDefaultFont", 12, "bold"), "#7FD1FF",
                               innen=14, pady=2)
            self._kasten_label(_schritt["text"], ("TkDefaultFont", 10), "#F3F4F6",
                               breite=790, innen=14, pady=4, umbruch=760)
            tk.Button(self.content, text=_schritt["knopf"], command=_schritt["aktion"], bg="#2563EB",
                      fg="white", activebackground="#1D4ED8", activeforeground="white",
                      font=("TkDefaultFont", 11, "bold")).pack(anchor=tk.W, padx=10, pady=(0, 10))

        # ---- Kennzahlen in Klartext (vorher "Bevölkerung: 60 / 15" ohne Erklärung) ----
        _bewohnt = int(self.state.population)
        _ueber = _bewohnt > _grenze
        self._kasten_label(
            f"Siedler (Reich): {_bewohnt} · Wohnraum: {_grenze}"
            + ("  Überbelegt – es wächst kein Siedler nach, bis ein Haus steht." if _ueber else ""),
            ("TkDefaultFont", 10), ("#FDBA74" if _ueber else "#DAA520"),
            breite=790, innen=14, pady=4, umbruch=760)
        frame = tk.Frame(self.content, bg=self.skin["panel"])
        frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(frame, text="Siedlungen:", fg=self.skin["gold"], bg=self.skin["panel"]).pack(anchor=tk.W, padx=5)
        # Schritt 9, Teil 3b: die Gesamtsicht (Reich) steht VOR der Liste, je Ort darunter sein
        # Lokalbestand. Seit Teil 3a fuehren die Ortslager — vorher las der Spieler hier eine
        # Zahl, die nicht mehr "Lager dieser Siedlung" bedeutet (KONTEXT_PAKET, Abschnitt 2).
        tk.Label(frame, text="Reich: " + reichsbestand_text(self.state),
                 fg="#DAA520", bg=self.skin["panel"], wraplength=780, justify=tk.LEFT,
                 font=("Arial", 9)).pack(anchor=tk.W, padx=5)
        # Teil 6: WELCHER Ort gemeint ist, muss sichtbar sein. Die Hilfe berichtigt einen leeren
        # oder veralteten Zeiger — hier einmal gelesen, damit die Liste und die Buchungen dieselbe
        # Siedlung meinen (eine Quelle, keine zweite Wahrheit in der Anzeige).
        _aktiv = self.state.aktive_siedlung()
        _aktiv_id = _aktiv.id if _aktiv is not None else ""
        for i, s in enumerate(self.state.settlements):
            row = tk.Frame(self.content, bg=self.skin["panel"])
            row.pack(fill=tk.X, padx=10, pady=2)
            tk.Label(row, text=f"{s.name} ({s.map_id})", fg=self.skin["text"], bg=self.skin["panel"], width=20, anchor=tk.W).pack(side=tk.LEFT, padx=5)
            if s.id == _aktiv_id:
                tk.Label(row, text="aktiv", fg="#7FD1FF", bg=self.skin["panel"],
                         font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=4)
            else:
                tk.Button(row, text="Als aktiv setzen",
                          command=lambda ss=s: self._siedlung_aktiv_setzen(ss),
                          bg=self.skin["button"], fg=self.skin["gold"],
                          activebackground="#5D4037").pack(side=tk.LEFT, padx=4)
            tk.Label(row, text=f"Gebäude auf der Karte: {len(getattr(s, 'bauten', {}) or {})}",
                     fg="#DAA520", bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
            if getattr(s, "karte", None):
                tk.Label(row, text=f"{s.karte['typ_name']} · Felder belegt: {len(s.bauten)}",
                         fg=self.skin["text"], bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
                tk.Button(row, text="Karte öffnen", command=lambda ss=s: self._oeffne_siedlungskarte(ss),
                          bg=self.skin["button"], fg=self.skin["gold"],
                          activebackground="#5D4037").pack(side=tk.LEFT, padx=5)
            entry = tk.Entry(row, bg=self.skin["panel"], fg=self.skin["text"], width=18)
            entry.insert(0, s.name)
            entry.pack(side=tk.LEFT, padx=5)
            tk.Button(row, text="Umbenennen", command=lambda ss=s, e=entry: self._rename_settlement(ss, e.get()), bg="#3e2723", fg=self.skin["gold"]).pack(side=tk.RIGHT, padx=5)
            tk.Button(row, text="Transport", command=lambda ss=s: self._transport_to_settlement(ss), bg="#3e2723", fg=self.skin["gold"]).pack(side=tk.RIGHT, padx=5)
            # Schritt 9, Teil 3b: "lokal: …" neben "Reich: …" — das Lager DIESES Ortes, das seit
            # Teil 3a fuehrt (Settlement.vorraete/bevoelkerung), nicht die Gesamtsicht.
            tk.Label(self.content, text="lokal: " + ortsbestand_text(s),
                     fg="#7FD1FF", bg=self.skin["bg"], wraplength=780, justify=tk.LEFT,
                     font=("Arial", 9)).pack(anchor=tk.W, padx=30)
        tk.Button(self.content, text="Neue Siedlung gründen", command=self._found_settlement, bg="#3e2723", fg=self.skin["gold"]).pack(anchor=tk.W, padx=10, pady=10)

        # W7: die laufenden Auftraege (im Original steht unten "Laufende Auftraege"). Die Einheiten
        # sind waehrend der Reise aus dem Bestand genommen; angekommen liefert den Bericht in die
        # Nachrichten. Gezeigt wird nur, was `auftraege.fortschritt` wirklich hergibt.
        tk.Label(self.content, text="Laufende Aufträge:", fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(6, 0))
        if not self.state.auftraege:
            tk.Label(self.content, text="keine — Aufträge startet man in der Diplomatie.",
                     fg="#8a8a8a", bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)
        else:
            # Schritt 10 Teil 3: die Restzeiten der Auftraege stehen auf der SPIELUHR — mit
            # `time.time()` haette die Liste hier eine unsinnige Zahl gezeigt.
            stand = auftraege.fortschritt(self.state.auftraege, float(self.state.spielsekunden))
            for eintrag in stand.get("je", []):
                rest = float(eintrag.get("rest_sekunden") or 0.0)
                tk.Label(self.content,
                         text=f"{str(eintrag.get('art')).capitalize()}: {eintrag.get('von')} → "
                              f"{eintrag.get('nach')} · {eintrag.get('status')} · "
                              f"noch {rest / 60.0:.1f} min",
                         fg=self.skin["text"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=20)

        # Wirkungen der 20 Originalgebaeude (W4b-5). Sie kommen AUSSCHLIESSLICH aus den bebauten
        # Feldern der Siedlungskarten — die frueheren globalen Gebaeude (main.BUILDINGS) sind
        # entfallen, sonst haette jede Wirkung zweimal existiert.
        wirk = tk.Frame(self.content, bg=self.skin["panel"], relief=tk.FLAT, borderwidth=1)
        wirk.pack(fill=tk.X, padx=10, pady=(2, 8))
        tk.Label(wirk, text="Gebäudewirkungen (aus den Siedlungskarten)",
                 fg=self.skin["gold"], bg=self.skin["panel"]).pack(anchor=tk.W, padx=5, pady=(3, 0))
        _haeuser = max(0, (_grenze - 10) // 5)
        # Heilkunde wirkt auf den Zuwachs (Handbuch 2009 Abschnitt 5, +10 % je Stufe). Die Anzeige
        # liest DIESELBE Forschungsstufen-Karte wie der Kern (F-04-Muster: eine Rechenstelle fuer
        # Anzeige und Kern), sonst zeigt sie 1 Siedler/Stunde, waehrend der Takt 1,5 bucht.
        _stufen = self.state.forschungs_stufen()                                                # flache Stufenkarte
        _zuwachs = gebaeude_wirkung.siedler_zuwachs_pro_stunde(self.state.settlements, _stufen)  # inkl. Heilkunde
        _heilkunde = int(_stufen.get("Heilkunde", 0) or 0)                                       # Heilkunde-Stufe
        _bonus_text = (f", inkl. Heilkunde +{_heilkunde * 10} %" if _heilkunde else "")           # Zusatz nur bei Stufe
        tk.Label(wirk, text=f"Siedlergrenze {_grenze} (Grundwert 10 + {_haeuser} Haus/Häuser × 5) · "
                            f"Zuwachs {_zuwachs:g} Siedler/Stunde "
                            f"(1 je Siedlung, Handbuch S. 11{_bonus_text})",
                 fg=self.skin["text"], bg=self.skin["panel"]).pack(anchor=tk.W, padx=5)
        # astra-Nachprüfung: „Zuwachs 1 Siedler/Stunde" widersprach der Überbelegungs-Warnung.
        # Angezeigt wird jetzt, was WIRKLICH passiert, und was möglich wäre.
        _moeglich = _zuwachs
        if _bewohnt >= _grenze and _moeglich > 0:
            tk.Label(wirk, text=f"Aktuelles Wachstum: 0 Siedler/Stunde — der Wohnraum ist voll. "
                                f"Möglich wären +{_moeglich:g}/Stunde, sobald ein Haus steht.",
                     fg="#FDBA74", bg=self.skin["panel"]).pack(anchor=tk.W, padx=5)
        _erlaubt, _meldung = gebaeude_wirkung.forschung_erlaubt(self.state.settlements)
        tk.Label(wirk, text=f"Forschung: {_meldung}", fg=self.skin["text"],
                 bg=self.skin["panel"]).pack(anchor=tk.W, padx=5)
        tk.Label(wirk, text=f"Verteidigung: {gebaeude_wirkung.wall_beschreibung(self.state.settlements)}",
                 fg=self.skin["text"], bg=self.skin["panel"]).pack(anchor=tk.W, padx=5)
        _zaehlung = gebaeude_wirkung.bestand(self.state.settlements)
        if _zaehlung:
            _text = ", ".join(f"{gelaende.gebaeude_name(k)} ×{n}" for k, n in sorted(
                _zaehlung.items(), key=lambda x: gelaende.gebaeude_name(x[0])))
            tk.Label(wirk, text=f"Gebäude auf den Karten: {_text}", fg=self.skin["text"],
                     bg=self.skin["panel"], wraplength=780, justify=tk.LEFT).pack(anchor=tk.W, padx=5, pady=(0, 3))
        # Entwicklerhinweise gehoeren NICHT auf die Spielansicht (astra-Gutachten: „Die
        # Startseite sieht wie eine interne Projektstatusseite aus"). Sie bleiben erreichbar,
        # sind aber standardmaessig zu.
        _luecken = [x for x in (gebaeude_wirkung.luecken().get(k)
                                for k in ("werkstaetten", "baukunst", "lager")) if x]
        if _luecken:
            _offen = bool(getattr(self, "_zeige_technik", False))
            tk.Button(wirk, text=("Technische Hinweise ausblenden" if _offen
                                  else f"Technische Hinweise einblenden ({len(_luecken)})"),
                      command=self._toggle_technik, bg=self.skin["button"],
                      fg="#C0C0C0").pack(anchor=tk.W, padx=5, pady=(3, 3))
            if _offen:
                for _luecke in _luecken:
                    tk.Label(wirk, text=f"Noch offen: {_luecke}", fg="#C0C0C0", bg=self.skin["panel"],
                             wraplength=780, justify=tk.LEFT).pack(anchor=tk.W, padx=5)

        # ---- S-2c: das Dorfzentrum ist Menuepunkt UND Gebaeude -------------------------------
        # Der Menuepunkt "Lager" ist in dieser Ansicht aufgegangen (siehe `MENUE_ENTFALLEN`).
        # Gezeigt wird zuerst, ob das GEBAEUDE Dorfzentrum steht - die Kennung bleibt `lager`
        # (eine Lesestelle: `gebaeude_stufe`), hoechstens eines je Dorf, nicht abreissbar.
        _dz = tk.Frame(self.content, bg=self.skin["panel"], relief=tk.FLAT, borderwidth=1)
        _dz.pack(fill=tk.X, padx=10, pady=(2, 8))
        tk.Label(_dz, text="Dorfzentrum als Gebäude", fg=self.skin["gold"],
                 bg=self.skin["panel"]).pack(anchor=tk.W, padx=5, pady=(3, 0))
        if not self.state.settlements:
            tk.Label(_dz, text="Noch keine Siedlung — ein Dorfzentrum entsteht mit dem Dorf.",
                     fg="#8a8a8a", bg=self.skin["panel"]).pack(anchor=tk.W, padx=5)
        else:
            _mit_dz = [s for s in self.state.settlements
                       if gebaeude_wirkung.gebaeude_stufe(s, "lager") > 0]
            _ohne_dz = [s for s in self.state.settlements
                        if gebaeude_wirkung.gebaeude_stufe(s, "lager") <= 0]
            tk.Label(_dz, text=(f"steht in {len(_mit_dz)} von {len(self.state.settlements)} "
                                f"Dörfern (höchstens eines je Dorf, das einzige ist nicht abreißbar)"),
                     fg=self.skin["text"], bg=self.skin["panel"], wraplength=780,
                     justify=tk.LEFT).pack(anchor=tk.W, padx=5)
            if _ohne_dz:
                # S-2c-D: zwei verschiedene Lagen, zwei verschiedene Wege. Ein Dorf mit offenem
                # Kennzeichen HAT das Dorfzentrum schon (aus dem Gruendungspaket), es fehlt nur
                # der Platz; ein Dorf ohne Kennzeichen muss es kaufen.
                _offen = [s.name for s in _ohne_dz if getattr(s, "dorfzentrum_offen", False)]
                _kaufen = [s.name for s in _ohne_dz
                           if not getattr(s, "dorfzentrum_offen", False)]
                if _offen:
                    tk.Label(_dz, text=("Platz noch offen in: " + ", ".join(_offen)
                                        + " — auf der Siedlungskarte ein freies Feld anklicken "
                                          "und „Dorfzentrum hier setzen“ wählen (kostenlos, "
                                          "kommt aus dem Gründungspaket)."),
                             fg="#7FD1FF", bg=self.skin["panel"], wraplength=780,
                             justify=tk.LEFT).pack(anchor=tk.W, padx=5, pady=(0, 3))
                if _kaufen:
                    tk.Label(_dz, text=("fehlt noch in: " + ", ".join(_kaufen)
                                        + " — auf der Siedlungskarte im Baubereich „Sonstiges“ "
                                          "bauen (Baukunst Stufe 1 nötig)."),
                             fg="#FDBA74", bg=self.skin["panel"], wraplength=780,
                             justify=tk.LEFT).pack(anchor=tk.W, padx=5, pady=(0, 3))
        # Die Verwaltung selbst: EINE Lageransicht (`_render_storage`), kein zweiter Lagerbegriff.
        self._render_storage(eigener_titel=False)

    def _toggle_technik(self):
        """Entwicklerhinweise ein-/ausblenden (stehen nicht ungefragt in der Spielansicht)."""
        self._zeige_technik = not bool(getattr(self, "_zeige_technik", False))
        self._render_view()

    def naechster_schritt(self) -> dict:
        """Der EINE naechste Schritt fuer den Spieler — als Karte oben im Dorfzentrum.

        Beantwortet „Wo fange ich an, wie mache ich weiter?" aus dem Spielzustand.
        Reihenfolge nach Handbuch: Siedlung → Feld bebauen → was Forschung/Ausbildung
        freischaltet → forschen und ausbilden. Rueckgabe: {text, knopf, aktion}.
        Vorbild: astra-Bildgutachten vom 05.10.2026, Abschnitt B.
        """
        st = self.state
        if not st.settlements:
            return {"text": "Gründe zuerst eine Siedlung — sie ist dein Bauplatz. Die "
                            "Siedlungskarte wird dir dabei automatisch zugewiesen (Handbuch "
                            "S. 313); du brauchst kein freies Feld auf der Weltkarte.",
                    "knopf": "Siedlung gründen",
                    "aktion": self._found_settlement}

        pflicht_start = spielerhilfe.startaufgabe_pflicht(st)
        s = st.settlements[0] if pflicht_start else st.settlements[-1]
        gebaut = len(getattr(s, "bauten", {}) or {})
        if gebaut == 0:
            return {"text": f"Deine Siedlung „{s.name}“ hat noch kein Gebäude. Öffne ihre Karte "
                            "und baue einen Holzfäller auf ein Waldfeld — er liefert Holz pro "
                            "Stunde. (Grün/Steppe sind für Farmen, Berge für Minen.)",
                    "knopf": f"„{s.name}“ öffnen — Gebäude bauen",
                    "aktion": (lambda ss=s: self._oeffne_siedlungskarte(ss))}

        # FIX04f: Waehrend des Pflicht-Onboardings stehen aktive
        # PRODUZENTEN vor Wohnraum/Forschung. Die passive Original-Grundrate
        # von 1 Holz und 1 Stein/h zaehlt hier absichtlich NICHT.
        produktionsrate = spielerhilfe.grundproduktion_erste_siedlung(st)
        for stoff, geb_key, felder_text in (
                ("holz", "holzfaeller", "auf Wald 4 Holz/h, auf Steppe 2"),
                ("stein", "steinmetz", "auf Berg 4 Stein/h, auf Huegel 2"),
                ("nahrung", "jaeger", "auf Wald 2 Nahrung/h + Leder (ohne Baukunst)")):
            if float(produktionsrate.get(stoff, 0.0)) > 0:
                continue
            eintrag = gelaende.alle_gebaeude().get(geb_key) or {}
            preis = kosten_text(baukosten(geb_key) or {})
            return {"text": f"Fuer eine abgeschlossene Grundversorgung fehlt eine laufende "
                            f"{stoff.capitalize()}-Produktion in deiner ersten Siedlung. "
                            f"Baue einen {eintrag.get('name', geb_key)} — {felder_text}"
                            + (f" (Kosten: {preis})." if preis else "."),
                    "knopf": f"„{s.name}“ öffnen — {eintrag.get('name', geb_key)} bauen",
                    "aktion": (lambda ss=s: self._oeffne_siedlungskarte(ss))}

        erlaubt, _ = gebaeude_wirkung.forschung_erlaubt(st.settlements)
        # Nach dem Grundaufbau werden wieder Wohnraum und Fortschritt empfohlen.
        if int(st.population) >= gebaeude_wirkung.bevoelkerungsgrenze(st.settlements):
            return {"text": f"Deine Siedlung ist ueberbelegt ({int(st.population)} Siedler, "
                            f"{gebaeude_wirkung.bevoelkerungsgrenze(st.settlements)} Wohnraum). "
                            "Baue ein Haus auf ein freies Feld, damit Siedler nachwachsen.",
                    "knopf": f"„{s.name}“ öffnen — Haus bauen",
                    "aktion": (lambda ss=s: self._oeffne_siedlungskarte(ss))}

        if not erlaubt:
            return {"text": "Baue als Nächstes eine Bibliothek — erst dann kannst du forschen. "
                            "Sie darf nur auf Grasland, Steppe oder Nebelsee stehen.",
                    "knopf": f"„{s.name}“ öffnen — Bibliothek bauen",
                    "aktion": (lambda ss=s: self._oeffne_siedlungskarte(ss))}

        laufend = forschung.fortschritt(st.forschung_stand(), float(st.spielsekunden))
        im_gange = [k for k, v in (laufend or {}).items() if (v or {}).get("laufend")]
        if im_gange:
            key = im_gange[0]
            rest = float((laufend.get(key) or {}).get("reststunden") or 0.0)
            return {"text": f"Die Forschung „{st.research[key].name}“ läuft noch {rest:.1f} Stunden. "
                            "Vertreibe dir die Zeit mit Bauen: jedes Gebäude auf einem Feld erhöht "
                            "deine Rohstoffe pro Stunde.",
                    "knopf": f"„{s.name}“ öffnen — weiterbauen",
                    "aktion": (lambda ss=s: self._oeffne_siedlungskarte(ss))}

        da, _, _ = gebaeude_wirkung.ausbildungsstaette(st.settlements, "Bürgerwehr")
        if not da:
            return {"text": "Baue eine Kriegerakademie — dann kannst du in der Kaserne Truppen "
                            "ausbilden (Bürgerwehr kostet Nahrung, Leder und Wolle, kein Gold).",
                    "knopf": f"„{s.name}“ öffnen — Kriegerakademie bauen",
                    "aktion": (lambda ss=s: self._oeffne_siedlungskarte(ss))}

        return {"text": "Grundgerüst steht: Siedlung, Gebäude, Bibliothek und Akademie. "
                        "Jetzt lohnt sich Ausbauen (Stufe erhöht den Ertrag), Forschen und "
                        "Truppen ausbilden — oder eine zweite Siedlung gründen.",
                "knopf": f"„{s.name}“ öffnen — weiterbauen",
                "aktion": (lambda ss=s: self._oeffne_siedlungskarte(ss))}

    def _upgrade_building(self, key: str):
        """Ausbau eines GLOBALEN Gebaeudes — gibt es seit W4b-5 nicht mehr.

        Die Wirkungen der 20 Originalgebaeude haengen an den bebauten FELDERN der
        Siedlungskarten; ausgebaut wird dort: Siedlungskarte oeffnen, Feld waehlen, "Ausbauen".
        Diese Methode nennt den richtigen Weg, statt still nichts zu tun — alte Aufrufe und
        Spielstaende landen hier.
        """
        self._log(f"'{key}' ist kein globales Gebäude: die Wirkungen kommen aus den bebauten "
                  f"Feldern der Siedlungskarten — dort das Feld wählen und 'Ausbauen' benutzen.")

    def _voelker_wahl_block(self) -> bool:
        """Die Voelkerwahl im Dorfzentrum (A2, 03.11.2026) - True, wenn sie gezeigt wurde.

        Daniel: "Mit Voelker sind die Fraktionen gemeint, Menschlich, Zwergisch, Elfisch, Trolle,
        Ghule, Gnome dann haben wir 6 Fraktionen." Der Spieler waehlt EINE; die fuenf Bots bekommen
        die uebrigen ohne Doppelung (`bottaktik.verteile_fraktionen`, deterministisch). Die Werte
        stehen in `data/voelker.json` - keine Zahl im Code. Die Wahl steht VOR der Kartenwahl
        (Fraktion zuerst, dann das Land), ersetzt das Dorfzentrum aber nicht.
        """
        if self.state.settlements or str(getattr(self.state, "spieler_fraktion", "") or ""):
            return False
        self._kasten_label("Waehle dein Volk", ("Blackletter", 16, "bold"),
                           self.skin["gold"], innen=12, pady=5)
        self._kasten_label(
            "Jedes Volk traegt ein Plus und ein Minus. Die fuenf Gegenspieler bekommen die uebrigen "
            "Voelker - jedes genau einmal. Die Wahl ist endgueltig und wird im Spielstand gespeichert; "
            "die Wirkung der Boni wird im naechsten Schritt verdrahtet.",
            ("TkDefaultFont", 9), "#C0C0C0", breite=810, innen=12, pady=4, umbruch=780)
        for eintrag in bottaktik.fraktionen():
            zeile = tk.Frame(self.content, bg=self.skin["panel"])      # eine Zeile je Volk (Tabelle)
            zeile.pack(fill=tk.X, padx=10, pady=2)
            tk.Label(zeile, text=str(eintrag.get("kennung")), fg=self.skin["text"],
                     bg=self.skin["panel"], width=14, anchor=tk.W).pack(side=tk.LEFT, padx=5)
            tk.Label(zeile, text=str(eintrag.get("plus") or ""), fg="#8FBF7F",
                     bg=self.skin["panel"], width=26, anchor=tk.W).pack(side=tk.LEFT, padx=5)
            tk.Label(zeile, text=str(eintrag.get("minus") or ""), fg="#FDBA74",
                     bg=self.skin["panel"], width=26, anchor=tk.W).pack(side=tk.LEFT, padx=5)
            tk.Label(zeile, text=str(eintrag.get("beschreibung") or "")[:70], fg="#C0C0C0",
                     bg=self.skin["panel"], wraplength=300, justify=tk.LEFT).pack(side=tk.LEFT, padx=5)
            tk.Button(zeile, text="Dieses Volk nehmen",
                      command=lambda k=str(eintrag.get("kennung")): self._volk_waehlen(k),
                      bg="#3e2723", fg=self.skin["gold"]).pack(side=tk.RIGHT, padx=5)
        return True

    def _volk_waehlen(self, kennung: str) -> dict:
        """Das Volk des Spielers merken und die restlichen Voelker auf die Bots verteilen."""
        fraktion = str(kennung or "").strip()
        if fraktion not in [str(e.get("kennung")) for e in bottaktik.fraktionen()]:
            self._log(f"Unbekanntes Volk: {kennung}")
            return {}
        self.state.spieler_fraktion = fraktion
        for _s in getattr(self.state, "settlements", []) or []:       # V-5: der Ort traegt sein Volk
            _s.volk = fraktion
        verteilung = bottaktik.verteile_fraktionen(fraktion, [b.name for b in self.state.bots])
        for bot in self.state.bots:                                    # jede Fraktion genau einmal
            neu = verteilung.get(str(bot.name))
            if not neu:
                continue
            bot.faction = neu
            bot.volksattribute = bottaktik.volksattribute({"fraktion": neu})
        werte = bottaktik.volksattribute({"fraktion": fraktion})
        self._log(f"Volk der Spieler: {fraktion} - {werte.get('plus')} / {werte.get('minus')}. "
                  f"Die fuenf Gegenspieler tragen die uebrigen Voelker.")
        self.state.messages.append({"type": "gruendung",
                                    "text": f"Volk gewaehlt: {fraktion} - {werte.get('plus')} / "
                                            f"{werte.get('minus')}."})
        if hasattr(self, "content"):
            self._render_view()
        return verteilung

    def _startkarte_wahl_block(self) -> bool:
        """Die Startkartenwahl als Block im Dorfzentrum (A2-Vorstufe, 03.11.2026) - True, wenn gezeigt.

        Daniel hat die Kartenwahl am Start in den eingefrorenen Demo-Umfang gelegt. Der Block steht
        NUR, solange keine Siedlung existiert und noch nichts gewaehlt ist; danach nie wieder. Er
        ERSETZT das Dorfzentrum nicht: die Pflichtkarte "Dein naechster Schritt" und der gewohnte
        Gruendungsknopf bleiben stehen - der Knopf gruendet ohne Wahl mit der Standardkarte, ein Klick
        auf "Diese Karte nehmen" gruendet mit genau dieser Karte.

        Kandidaten sind deterministisch je Startsaat, die Standardkarte ist immer dabei, alle Zahlen
        stehen in `data/startkarte.json` (`originalkarten.startkarte_kandidaten`). Die Zeilen sind eine
        Tabelle und bleiben deckend; die Texte darueber liegen als weiche Felder auf dem Motiv.
        """
        gewaehlt = getattr(self.state, "startkarte_gewaehlt", "")
        if not spieloekonomie.startkarte_auswahl_erforderlich(
                len(self.state.settlements), SIEDLUNGEN_MAXIMUM, gewaehlt):
            return False
        self._kasten_label("Waehle deine Startkarte", ("Blackletter", 16, "bold"),
                           self.skin["gold"], innen=12, pady=5)
        self._kasten_label(
            "Drei Karten stehen zur Wahl. Sie unterscheiden sich in Wald, Gestein und Ackerland - "
            "was dein Dorf am schnellsten traegt. Die Wahl ist endgueltig und wird im Spielstand "
            "gespeichert; ohne Wahl gruendet der Knopf unten mit der Standardkarte.",
            ("TkDefaultFont", 9), "#C0C0C0", breite=810, innen=12, pady=4, umbruch=780)
        seed = self.state.kartenvorrat_seed or "nebel"
        for nummer, kandidat in enumerate(spieloekonomie.startkarte_kandidaten(seed), start=1):
            achsen = spieloekonomie.relativ(kandidat)
            zeile = tk.Frame(self.content, bg=self.skin["panel"])   # eine Zeile je Karte (Tabelle)
            zeile.pack(fill=tk.X, padx=10, pady=2)
            tk.Label(zeile, text=f"{nummer}. {kandidat.get('typ_name') or kandidat.get('originalkarte_id')}",
                     fg=self.skin["text"], bg=self.skin["panel"], width=18,
                     anchor=tk.W).pack(side=tk.LEFT, padx=5)
            tk.Label(zeile, text="Holz %.2f / Stein %.2f / Agrar %.2f" % achsen,
                     fg="#DAA520", bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
            tk.Label(zeile, text=str(kandidat.get("vorteil") or "")[:90],
                     fg="#C0C0C0", bg=self.skin["panel"], wraplength=360,
                     justify=tk.LEFT).pack(side=tk.LEFT, padx=5)
            tk.Button(zeile, text="Diese Karte nehmen",
                      command=lambda k=kandidat.get("originalkarte_id"): self._startkarte_waehlen(k),
                      bg="#3e2723", fg=self.skin["gold"]).pack(side=tk.RIGHT, padx=5)
        return True

    def _startkarte_waehlen(self, kennung: str):
        """Die gewaehlte Startkarte merken und die erste Siedlung gruenden."""
        self.state.startkarte_gewaehlt = str(kennung or "")
        self._erste_siedlung_gruenden()

    def _found_settlement(self):
        """Eine Siedlung gründen (Ökonomie-Paket, Schritt 9, Teil 5; Entwurf Z. 777).

        Der ERSTE Start ist belegt und bleibt einfach: er übernimmt die Startbestände genau einmal
        und die **Startkarte** — ohne Gebühr, ohne Auswahl. Jede weitere Siedlung ist eine
        **Kolonie**: sie kommt aus dem **Kartenvorrat**, kostet die Gründungsgebühr und verlangt
        das Mindestguthaben plus einen Siedlerkarren. Geprüft wird über den Kern (`absicht`),
        vergeben mit `vergabe`; die Auswahl zeigt Nutzen, Kapazitäten, Preis und Mindestbestand,
        und das Weltfeld steht VOR der Zahlung fest.
        """
        if len(self.state.settlements) >= SIEDLUNGEN_MAXIMUM:
            self._log(f"Maximale Siedlungsanzahl erreicht ({SIEDLUNGEN_MAXIMUM}).")
            return
        if not self.state.settlements:
            self._erste_siedlung_gruenden()
            return
        self._kolonie_gruenden()

    def _erste_siedlung_gruenden(self):
        """Startkarte und belegte Startwerte (Handbuch S. 7: 10 Siedler · 100 Holz · 100 Stein)."""
        cfg = next(m for m in MAPS if m["id"] == self.state.current_map)
        size = cfg["size"]
        self.state._weltkarte_sicherstellen()      # die Startsiedlung steht auf einem Weltfeld
        if not self.state.kartenvorrat_seed:
            self.state.kartenvorrat_seed = "nebel-%d" % random.randrange(1, 10 ** 9)
        if not self.state.kartenvorrat:
            self.state.kartenvorrat_anlegen(self.state.kartenvorrat_seed)
        # A2-Vorstufe (03.11.2026): hat der Spieler im Startfenster gewaehlt, gilt seine Karte;
        # ohne Wahl bleibt es bei der belegten Standardkarte (original-036). Der Aufruf ohne
        # Argument gruendet deshalb weiterhin sofort - 16 Pruefdateien haengen daran.
        karte = spieloekonomie.startkarte_gewaehlt(
            getattr(self.state, "startkarte_gewaehlt", ""), self.state.kartenvorrat_seed)
        for _ in range(200):
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            tile = self.state.get_tile(x, y, size)
            if not (tile and tile.terrain != "water" and not tile.npc_faction):
                continue
            start = {r: float(res.amount) for r, res in self.state.resources.items()
                     if float(res.amount) > 0}
            bevoelkerung_start = float(self.state.population)
            sett = Settlement(name="Siedlung 1", map_id=self.state.current_map, x=x, y=y,
                              karte=karte,
                              id=siedlung_kennung("spieler", self.state.current_map, x, y),
                              volk=str(getattr(self.state, "spieler_fraktion", "") or ""))
            sett.vorraete = dict(start)
            sett.bevoelkerung = bevoelkerung_start
            self.state.settlements.append(sett)
            # Die Startwerte werden EINMAL übernommen (verschoben, nicht kopiert) — sonst stünden
            # sie doppelt: einmal im Ortslager und einmal im Reichsbestand (Entwurf Z. 775).
            for r in list(start):
                self.state.resources[r].amount = 0.0
            self.state.population = 0.0
            self.state._reichsanzeige_aus_orten()
            self.state.hatte_siedlung = True
            tile.npc_faction = "spieler"
            tile.sector_name = sett.name
            # Der Gruendungskarren bringt die drei Startgebaeude mit (Schnitt S-1). Die Meldung
            # geht in Nachrichten UND Log, aber NICHT ueber `self._log` — sonst wuerde sie die
            # Statuszeile ueberschreiben, die weiterhin "gegruendet" zeigen soll.
            _start_ergebnisse = _startgebaeude_setzen(sett, karte)
            # S-2c-D: das Dorfzentrum wartet auf seinen Platz - der Spieler setzt es selbst.
            sett.dorfzentrum_offen = True
            _start_text = _startgebaeude_meldung(_start_ergebnisse)
            if _start_text:
                self.state.messages.append({"type": "gruendung", "text": _start_text})
                self.state._log(_start_text)
            # Die Hauptmeldung ZULETZT: die Statuszeile zeigt immer die letzte Zeile.
            self._log(f"  Karte: {karte['typ_name']} — {karte['vorteil']}")
            self._log(f"  {gelaende.karte_beschreiben(karte)}")
            self._log(f"Neue Siedlung '{sett.name}' gegründet — im Dorfzentrum steht jetzt "
                      f"„Karte öffnen\": dort Felder bebauen und Rohstoffe fördern.")
            # Ohne Neuzeichnen sieht der Spieler NICHTS: die Siedlungsliste bliebe leer.
            self._render_view()
            return
        self._log("Kein geeigneter Platz für die Startsiedlung gefunden.")
        self._render_view()

    def _kolonie_gruenden(self):
        """Die Auswahlmaske einer Neugründung öffnen: Kartenvorrat, Nutzen, Preis, Weltfeld."""
        karten = self.state.freie_koloniekarten()
        if not karten:
            self._log("Keine freie Koloniekarte mehr im Vorrat — es lässt sich keine Siedlung "
                      "mehr gründen.")
            return
        felder = self.state.freie_weltfelder(6)
        if not felder:
            self._log("Kein freies Weltfeld für eine Gründung gefunden.")
            return
        quellen = sorted(self.state.settlements,
                         key=lambda s: (-sum((s.vorraete or {}).values()), s.id))
        quelle_zu_name = {s.name: s for s in quellen}
        karte_zu_text = {f"{k['karte_id']} · {k['karte']['typ_name']} · Nutzen {k['nutzen']:.2f}": k
                         for k in karten}
        feld_zu_text = {f"Feld {x}/{y}": (x, y) for x, y in felder}

        fenster = tk.Toplevel(self.root)
        fenster.title("Neue Siedlung gründen")
        fenster.configure(bg=self.skin["bg"])

        def _zeile(text, farbe=None, reihe=0, spalte=0, spann=2):
            tk.Label(fenster, text=text, fg=farbe or self.skin["text"], bg=self.skin["bg"],
                     anchor=tk.W, justify=tk.LEFT, wraplength=760).grid(
                row=reihe, column=spalte, columnspan=spann, sticky=tk.W, padx=10,
                pady=(4, 0) if reihe else (10, 4))

        _zeile("Neue Siedlung gründen (Kolonie)", self.skin["gold"], 0)
        var_quelle = tk.StringVar(value=quellen[0].name)
        _zeile("Ausgangssiedlung (zahlt Sperrgut und Karren):", None, 1, 0, 1)
        tk.OptionMenu(fenster, var_quelle, *quelle_zu_name.keys()).grid(
            row=1, column=1, sticky=tk.W, padx=10, pady=(4, 0))
        var_karte = tk.StringVar(value=next(iter(karte_zu_text)))
        _zeile("Karte aus dem Vorrat (Nutzen = Nutzen für unseren Verbund):", None, 2, 0, 1)
        tk.OptionMenu(fenster, var_karte, *karte_zu_text.keys()).grid(
            row=2, column=1, sticky=tk.W, padx=10, pady=(4, 0))
        var_feld = tk.StringVar(value=next(iter(feld_zu_text)))
        _zeile("Weltfeld (steht VOR der Zahlung fest):", None, 3, 0, 1)
        tk.OptionMenu(fenster, var_feld, *feld_zu_text.keys()).grid(
            row=3, column=1, sticky=tk.W, padx=10, pady=(4, 0))

        e_karte = karten[0]
        preis_t = ", ".join(f"{int(v)} {r.capitalize()}" for r, v in sorted(e_karte["preis"].items()))
        min_t = ", ".join(f"{int(v)} {r.capitalize()}" for r, v in sorted(e_karte["minimum"].items()))
        kap_t = ", ".join(f"{r.capitalize()} {v:g}/h" for r, v in
                          sorted(e_karte["kapazitaeten"].items()) if v) or "keine Erzeuger"
        _zeile(f"Gebühr: {preis_t}", None, 4)
        _zeile(f"Mindestbestand im Ortslager der Ausgangssiedlung: {min_t}", None, 5)
        _zeile(f"Erzeugerprofil der erstgenannten Karte: {kap_t}", "#7FD1FF", 6)
        _zeile("Ortslager der Ausgangssiedlung: " + ortsbestand_text(quellen[0]), None, 7)
        _zeile("Verlangt außerdem: Wagenbau (Forschung) und einen Siedlerkarren.", "#FDBA74", 8)

        def _starten():
            gewaehlt = karte_zu_text.get(var_karte.get())
            ok, _meldung = self._gruendung_ausfuehren(quelle_zu_name.get(var_quelle.get()),
                                                      (gewaehlt or {}).get("karte_id"),
                                                      feld_zu_text.get(var_feld.get()))
            if ok:
                fenster.destroy()

        tk.Button(fenster, text="Gründen", command=_starten, bg="#3e2723", fg=self.skin["gold"],
                  activebackground="#5D4037").grid(row=9, column=0, columnspan=2, sticky=tk.W,
                                                   padx=10, pady=10)

    def _gruendung_ausfuehren(self, quelle, karte_id, feld):
        """Die Eingaben der Gründungsmaske ausführen — die EINE Stelle, die bucht. ``(ok, Meldung)``.

        Getrennt von der Maske, damit die Prüfung den ganzen Weg ohne Fenster gehen kann.
        """
        ok, meldung = self.state.gruendung_ausfuehren(quelle, karte_id, feld)
        if not ok:
            self._log(f"Gründung nicht möglich: {meldung}")
            return False, meldung
        neu = self.state.settlements[-1]
        self._log(f"  Karte: {neu.karte['typ_name']} — {neu.karte.get('vorteil', '')}")
        self._render_view()
        return True, meldung

    def _rename_settlement(self, settlement: Settlement, new_name: str):
        now = time.time()
        if now - settlement.last_rename < 86400:
            self._log("Siedlung kann nur alle 24 Stunden umbenannt werden.")
            return
        if not new_name or not new_name.strip():
            self._log("Siedlungsname darf nicht leer sein.")
            return
        allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-+=.<>|öäüÖÄÜß ")
        if any(ch not in allowed for ch in new_name):
            self._log("Siedlungsname enthält unerlaubte Sonderzeichen.")
            return
        if any(s.name == new_name for s in self.state.settlements if s != settlement):
            self._log("Es gibt bereits eine Siedlung mit diesem Namen.")
            return
        settlement.name = new_name.strip()
        settlement.last_rename = now
        self._log(f"Siedlung umbenannt in '{settlement.name}'.")
        self._render_view()

    def _transport_to_settlement(self, ziel: Settlement):
        """Die Transportmaske öffnen (Ökonomie-Paket, Schritt 9, Teil 4; Entwurf Z. 779).

        Hier stand vorher ein fester Transport von **10 Holz**, der den Reichsbestand abzog und
        NICHTS gutschrieb — eine Mechanik gab es damit nicht (so fand es der Handbuch-Abgleich).
        Jetzt werden **Herkunft, Rohstoff, Menge und Karren** abgefragt, und gebucht wird der Kern
        (`state.transport_an_ort` → `spieloekonomie.transport_start`).
        """
        if ziel.map_id != self.state.current_map:
            self._log("Transport nur zur aktuellen Karte möglich.")
            return
        quellen = [s for s in self.state.settlements
                   if s.id != ziel.id and s.map_id == self.state.current_map]
        if not quellen:
            self._log("Für einen Transport braucht es eine ZWEITE eigene Siedlung auf dieser "
                      "Karte — erst gründen, dann transportieren.")
            return
        name_zu_ort = {s.name: s for s in quellen}

        fenster = tk.Toplevel(self.root)
        fenster.title(f"Transport nach {ziel.name}")
        fenster.configure(bg=self.skin["bg"])

        def _zeile(text):
            return tk.Label(fenster, text=text, fg=self.skin["text"], bg=self.skin["bg"],
                            anchor=tk.W, justify=tk.LEFT)

        tk.Label(fenster, text=f"Transport nach {ziel.name}", fg=self.skin["gold"],
                 bg=self.skin["bg"], font=("TkDefaultFont", 11, "bold")).grid(
            row=0, column=0, columnspan=2, sticky=tk.W, padx=10, pady=(10, 4))

        var_quelle = tk.StringVar(value=quellen[0].name)
        _zeile("Herkunft (Ortslager):").grid(row=1, column=0, sticky=tk.W, padx=10)
        tk.OptionMenu(fenster, var_quelle, *name_zu_ort.keys()).grid(
            row=1, column=1, sticky=tk.W, padx=10)

        var_rohstoff = tk.StringVar(value="holz")
        _zeile("Rohstoff:").grid(row=2, column=0, sticky=tk.W, padx=10)
        tk.OptionMenu(fenster, var_rohstoff, *RESOURCES).grid(row=2, column=1, sticky=tk.W, padx=10)

        _zeile("Menge:").grid(row=3, column=0, sticky=tk.W, padx=10)
        e_menge = tk.Entry(fenster, width=10)
        e_menge.insert(0, "10")
        e_menge.grid(row=3, column=1, sticky=tk.W, padx=10)

        # Nur ECHTE Transporteinheiten (Karren) stehen zur Wahl — dieselbe Prüfung wie die Buchung.
        karren_bestand = self.state.transport_karren_bestand(quellen[0])
        var_karren = tk.StringVar(value=next(iter(sorted(karren_bestand)), ""))
        _zeile("Karren (Ort + Reichsheer):").grid(row=4, column=0, sticky=tk.W, padx=10)
        if karren_bestand:
            tk.OptionMenu(fenster, var_karren, *sorted(karren_bestand)).grid(
                row=4, column=1, sticky=tk.W, padx=10)
        else:
            tk.Label(fenster, text="keine — ein Karren wird im Stellmacher ausgebildet",
                     fg="#FDBA74", bg=self.skin["bg"]).grid(row=4, column=1, sticky=tk.W, padx=10)
        _zeile("Karren-Anzahl:").grid(row=5, column=0, sticky=tk.W, padx=10)
        e_karren = tk.Entry(fenster, width=10)
        e_karren.insert(0, "1")
        e_karren.grid(row=5, column=1, sticky=tk.W, padx=10)

        # Was da ist und was passt — offen benannt, statt still abzulehnen.
        _zeile("Im Ortslager der Herkunft: " + ortsbestand_text(quellen[0])).grid(
            row=6, column=0, columnspan=2, sticky=tk.W, padx=10, pady=(6, 0))
        _stufen_karren = self.state.forschungs_stufen()
        _zeile("Ladeplätze: " + (", ".join(f"{k}x {n} ({einheiten.ladung_mit_bonus(n, _stufen_karren)} Plätze)"
                                           for n, k in sorted(karren_bestand.items()))
                                 or "ohne Karren kein Transport (Handbuch S. 23)")).grid(
            row=7, column=0, columnspan=2, sticky=tk.W, padx=10)
        _zeile("Zielbestand: " + ortsbestand_text(ziel)).grid(
            row=8, column=0, columnspan=2, sticky=tk.W, padx=10, pady=(0, 6))

        def _starten():
            ok, _meldung = self._transport_ausfuehren(
                name_zu_ort.get(var_quelle.get()), ziel, var_rohstoff.get(), e_menge.get(),
                var_karren.get(), e_karren.get())
            if ok:
                fenster.destroy()

        knopf = tk.Button(fenster, text="Transport starten", command=_starten, bg="#3e2723",
                          fg=self.skin["gold"], activebackground="#5D4037")
        if not karren_bestand:
            knopf.config(state=tk.DISABLED)
        knopf.grid(row=9, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)

    def _transport_ausfuehren(self, quelle, ziel, rohstoff, menge, karren_name, karren_anzahl):
        """Die Eingaben der Transportmaske ausführen — die EINE Stelle, die bucht.

        Getrennt von der Maske, damit die Prüfung den ganzen Weg ohne Fenster gehen kann.
        Liefert ``(ok, Meldung)``.
        """
        try:
            anzahl = int(karren_anzahl)
        except (TypeError, ValueError):
            meldung = "Die Karren-Anzahl muss eine ganze Zahl sein."
            self._log(meldung)
            return False, meldung
        karren = {str(karren_name): anzahl} if karren_name else {}
        ok, meldung = self.state.transport_an_ort(quelle, ziel, rohstoff, menge, karren)
        if not ok:
            self._log(f"Transport nicht gestartet: {meldung}")
            return False, meldung
        self._render_view()
        return True, meldung

    # ---------- Teil 7b: die Handelsmaske (Ware, Menge, Preis — Entwurf Z. 779/781) ----------

    def _handel_maske(self, bot: BotPlayer):
        """Die Maske des BESTÄTIGTEN KAUFVERTRAGS: Ware, Menge und Preis wählen.

        Muster ist die Transportmaske aus Teil 4: alles, was der Spieler entscheiden muss, steht
        sichtbar da (Angebot und Schwellenpreis des Bots, Ortslager des Käufers, Ladeplätze) — und
        der Knopf bucht über die EINE Stelle `_handel_ausfuehren`, die auch ohne Fenster prüfbar ist.
        """
        quelle = self.state.aktive_siedlung()
        if quelle is None:
            self._log("Für einen Handel braucht es zuerst eine eigene Siedlung.")
            return
        angebot = sorted(k for k, v in (bot.vorraete or {}).items()
                         if k in RESOURCES and k != "gold" and float(v) > 0)
        karawanen = self.state.handelskarawanen_bestand(quelle)
        referenz = botkern.referenzpreis_aus_beschaffung(BOT_BESCHAFFUNGSKOSTEN)
        schwelle = float(botkern.handelspreis(referenz, float(bot.temperament)))
        x, y = self.state.bot_standort(quelle)

        fenster = tk.Toplevel(self.root)
        fenster.title(f"Handel mit {bot.name}")
        fenster.configure(bg=self.skin["bg"])

        def _zeile(text):
            return tk.Label(fenster, text=text, fg=self.skin["text"], bg=self.skin["bg"],
                            anchor=tk.W, justify=tk.LEFT, wraplength=560)

        tk.Label(fenster, text=f"Kaufvertrag mit {bot.name}", fg=self.skin["gold"],
                 bg=self.skin["bg"], font=("TkDefaultFont", 11, "bold")).grid(
            row=0, column=0, columnspan=2, sticky=tk.W, padx=10, pady=(10, 4))
        _zeile("Käufer (aktive Siedlung): " + quelle.name + " — " + ortsbestand_text(quelle)).grid(
            row=1, column=0, columnspan=2, sticky=tk.W, padx=10)
        _zeile(f"Bot-Siedlung: angenommen auf Feld {x}/{y} (Bots führen keine Koordinaten).").grid(
            row=2, column=0, columnspan=2, sticky=tk.W, padx=10, pady=(0, 4))

        var_ware = tk.StringVar(value=angebot[0] if angebot else "")
        _zeile("Ware (Angebot des Bots):").grid(row=3, column=0, sticky=tk.W, padx=10)
        if angebot:
            tk.OptionMenu(fenster, var_ware, *angebot).grid(row=3, column=1, sticky=tk.W, padx=10)
        else:
            tk.Label(fenster, text="kein Rohstoff im Angebot", fg="#FDBA74",
                     bg=self.skin["bg"]).grid(row=3, column=1, sticky=tk.W, padx=10)
        _zeile("Bestand des Bots: " + (", ".join("%s %g" % (k, float(v))
                                                 for k, v in sorted((bot.vorraete or {}).items()))
                                       or "nichts")).grid(
            row=4, column=0, columnspan=2, sticky=tk.W, padx=10)

        _zeile("Menge:").grid(row=5, column=0, sticky=tk.W, padx=10)
        e_menge = tk.Entry(fenster, width=10)
        e_menge.insert(0, "10")
        e_menge.grid(row=5, column=1, sticky=tk.W, padx=10)

        _zeile("Preis je Stück (Gold):").grid(row=6, column=0, sticky=tk.W, padx=10)
        e_preis = tk.Entry(fenster, width=10)
        e_preis.insert(0, ("%.2f" % schwelle).rstrip("0").rstrip("."))
        e_preis.grid(row=6, column=1, sticky=tk.W, padx=10)
        _zeile("Schwellenpreis dieses Bots: %g Gold — darunter lehnt er bei der Ankunft ab "
               "(Handbuch S. 20: bei Ablehnung kehrt die Karawane MIT den Waren zurück, Gold wird "
               "nie übertragen)." % schwelle).grid(
            row=7, column=0, columnspan=2, sticky=tk.W, padx=10)

        var_karawane = tk.StringVar(value=next(iter(sorted(karawanen)), ""))
        _zeile("Handelskarawane (Ortslager + Reichsheer):").grid(row=8, column=0, sticky=tk.W, padx=10)
        if karawanen:
            tk.OptionMenu(fenster, var_karawane, *sorted(karawanen)).grid(
                row=8, column=1, sticky=tk.W, padx=10)
        else:
            tk.Label(fenster, text="keine — sie entsteht im Stellmacher", fg="#FDBA74",
                     bg=self.skin["bg"]).grid(row=8, column=1, sticky=tk.W, padx=10)
        _zeile("Karawanen-Anzahl:").grid(row=9, column=0, sticky=tk.W, padx=10)
        e_karawane = tk.Entry(fenster, width=10)
        e_karawane.insert(0, "1")
        e_karawane.grid(row=9, column=1, sticky=tk.W, padx=10)
        _stufen_karren = self.state.forschungs_stufen()
        _zeile("Ladeplätze: " + (", ".join("%s x%d (%d Plätze)" % (n, a, einheiten.kapazitaet_mit_bonus(n, a, _stufen_karren))
                                          for n, a in sorted(karawanen.items()))
                                or "ohne Handelskarawane kein Handel (Handbuch S. 20)")).grid(
            row=10, column=0, columnspan=2, sticky=tk.W, padx=10, pady=(0, 6))

        def _starten():
            ok, _meldung = self._handel_ausfuehren(bot, quelle, var_ware.get(), e_menge.get(),
                                                   e_preis.get(), var_karawane.get(),
                                                   e_karawane.get())
            if ok:
                fenster.destroy()

        knopf = tk.Button(fenster, text="Kaufvertrag schicken", command=_starten, bg="#3e2723",
                          fg=self.skin["gold"], activebackground="#5D4037")
        if not karawanen or not angebot:
            knopf.config(state=tk.DISABLED)
        knopf.grid(row=11, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)

    def _handel_ausfuehren(self, bot, quelle, ware, menge, preis, karawanen_name, karawanen_anzahl):
        """Die Eingaben der Handelsmaske ausführen — die EINE Stelle, die bucht (Teil 7b).

        Getrennt von der Maske, damit die Prüfung den ganzen Weg ohne Fenster gehen kann.
        Liefert ``(ok, Meldung)``.
        """
        try:
            anzahl = int(karawanen_anzahl)
        except (TypeError, ValueError):
            meldung = "Die Karawanen-Anzahl muss eine ganze Zahl sein."
            self._log(meldung)
            return False, meldung
        karawane = {str(karawanen_name): anzahl} if karawanen_name else {}
        ok, meldung = self.state.handel_mit_bot(bot, quelle, ware, menge, preis, karawane)
        if not ok:
            self._log(f"Handel nicht gestartet: {meldung}")
            return False, meldung
        self._render_view()
        return True, meldung

    # ---------- Siedlungskarte (Handbuch S. 259/283/292/313) ----------

    def _siedlung_aktiv_setzen(self, siedlung):
        """Diesen Ort zum AKTIVEN machen (Teil 6). Lager, Kaserne und Forschung beziehen sich
        danach auf ihn — die eine Quelle bleibt `state.aktive_siedlung()`."""
        self.state.aktive_siedlung_id = getattr(siedlung, "id", "")
        self._log(f"Aktive Siedlung: {siedlung.name} — Lager, Kaserne und Forschung beziehen sich "
                  f"jetzt auf diesen Ort.")
        self._render_view()

    def _nahrungssperre(self, siedlung) -> str:
        """Der Sperrtext fuer diesen Ort - leer heisst: keine Sperre (Register 70/74).

        EINE Stelle fuer alle fuenf Zahlstellen (Bauen, Ausbauen, Ware, Forschung, Ausbildung)
        und fuer die Anzeige. Daniel: keine weitere Produktion und keine Zahlung im Ort, solange
        die Nahrung dort nicht ausgeglichen ist.
        """
        if siedlung is None:
            return ""
        return str((self.state.nahrungsnot(siedlung) or {}).get("text") or "")

    def _oeffne_siedlungskarte(self, siedlung):
        self.karten_siedlung = siedlung
        # Teil 6: wer eine Siedlungskarte öffnet, meint DIESEN Ort — Lager, Kaserne und Forschung
        # beziehen sich von jetzt an darauf (eine Quelle: `state.aktive_siedlung()`).
        if getattr(siedlung, "id", ""):
            self.state.aktive_siedlung_id = siedlung.id
        self.karten_feld = None
        self._switch_view("Siedlungskarte")

    def _dorf_uebersicht_zeichnen(self, eltern, siedlung) -> None:
        """A-3: Dorfuebersicht rechts neben der Siedlungskarte.

        Daniel im Spielbericht 31.10.2026: "welche gebaeude habe ich, wie viele, welcher ertrag".
        Gezeigt wird je Gebaeudeart: **Anzahl · Stufe(n) · Stundenertrag · gebundene Siedler ·
        Anteil am Ortsertrag**, darunter die **Summenzeile**. Alle Zahlen kommen aus
        `wirtschaft.dorf_uebersicht`, also aus derselben Rechnung wie Produktion, Kopfzeile und
        Ortsbestand - kein zweiter Rechenweg.
        """
        if not hasattr(self, "skin"):
            return
        rahmen = tk.Frame(eltern, bg=self.skin["panel"], highlightbackground="#5D4037",
                          highlightthickness=1)
        rahmen.pack(side=tk.LEFT, anchor=tk.N, fill=tk.Y, padx=(12, 0))
        tk.Label(rahmen, text="Dorfübersicht", fg=self.skin["gold"], bg=self.skin["panel"],
                 font=("TkDefaultFont", 11, "bold")).pack(anchor=tk.W, padx=8, pady=(6, 0))
        # A-6: die freie Siedlerreserve steht auch HIER - an der Stelle, an der gebaut wird.
        try:
            _reserve = spieloekonomie.siedler_reserve(
                asdict(siedlung), self.state.forschungs_stufen())
            tk.Label(rahmen,
                     text=(f"Freie Siedler: {_reserve['frei']:.1f} · Nachwuchs "
                           f"{_reserve['zuwachs_stunde']:.1f}/h"
                           + (" · ⚠ " + _reserve["text"] if _reserve["text"] else "")),
                     fg=("#FDBA74" if _reserve["warnung"] else "#C0C0C0"),
                     bg=self.skin["panel"], font=("Arial", 8), wraplength=430,
                     justify=tk.LEFT).pack(anchor=tk.W, padx=8, pady=(0, 2))
        except (AttributeError, KeyError, TypeError, ValueError):
            pass
        try:
            stufen = self.state.forschungs_stufen()
        except (AttributeError, KeyError, TypeError):
            stufen = {}
        try:
            daten = wirtschaft.dorf_uebersicht(siedlung, stufen)
        except (KeyError, TypeError, ValueError):
            daten = None
        if daten is None:
            tk.Label(rahmen, text="Übersicht nicht berechenbar.", fg="#FDBA74",
                     bg=self.skin["panel"]).pack(anchor=tk.W, padx=8, pady=4)
            return
        if not daten["gebaeude"]:
            tk.Label(rahmen, text="Noch kein Gebäude gebaut.", fg="#8a8a8a",
                     bg=self.skin["panel"]).pack(anchor=tk.W, padx=8, pady=6)
            return
        tabelle = tk.Frame(rahmen, bg=self.skin["panel"])
        tabelle.pack(anchor=tk.W, padx=6, pady=(4, 2))
        kopfzeile = [("Gebäude", 140, tk.W), ("Anz.", 34, tk.E), ("Stufe", 56, tk.W),
                     ("je Stunde", 128, tk.W), ("Anteil", 52, tk.E), ("Siedler", 48, tk.E)]
        for spalte, (titel, breite, anker) in enumerate(kopfzeile):
            tk.Label(tabelle, text=titel, fg="#C0C0C0", bg=self.skin["panel"],
                     width=(breite // 8), anchor=anker,
                     font=("Arial", 8, "bold")).grid(row=0, column=spalte, sticky="w")
        for zeile, eintrag in enumerate(daten["gebaeude"][:26], start=1):
            werte = [(eintrag["name"], tk.W, self.skin["text"]),
                     (str(eintrag["anzahl"]), tk.E, self.skin["text"]),
                     (eintrag["stufen_text"].replace("Stufe ", "").replace("Stufen ", ""),
                      tk.W, self.skin["text"]),
                     (eintrag["ertrag_text"] or "—", tk.W, "#DAA520"),
                     (f"{eintrag['anteil'] * 100:.0f} %", tk.E, "#C0C0C0"),
                     (str(eintrag["siedler"]) if eintrag["siedler"] else "—", tk.E, "#C0C0C0")]
            for spalte, (text, anker, farbe) in enumerate(werte):
                tk.Label(tabelle, text=text, fg=farbe, bg=self.skin["panel"],
                         width=(kopfzeile[spalte][1] // 8), anchor=anker,
                         font=("Arial", 8)).grid(row=zeile, column=spalte, sticky="w")
        summe = daten["summe"]
        tk.Frame(rahmen, bg="#5D4037", height=1).pack(fill=tk.X, padx=6, pady=(2, 2))
        tk.Label(rahmen,
                 text=(f"Summe: {summe['anzahl']} Gebäude · "
                       f"{summe['ertrag_text'] or 'kein Ertrag'} · "
                       f"Siedler gebunden: {summe['siedler']}"),
                 fg=self.skin["gold"], bg=self.skin["panel"], font=("Arial", 9, "bold"),
                 wraplength=430, justify=tk.LEFT).pack(anchor=tk.W, padx=8, pady=(0, 2))
        tk.Label(rahmen, text=daten["hinweis"], fg="#8a8a8a", bg=self.skin["panel"],
                 font=("Arial", 8), wraplength=430, justify=tk.LEFT
                 ).pack(anchor=tk.W, padx=8, pady=(0, 2))
        if daten["uebersprungen"]:
            tk.Label(rahmen,
                     text=("Nicht mitgerechnet: " + "; ".join(daten["uebersprungen"][:3])
                           + (" …" if len(daten["uebersprungen"]) > 3 else "")),
                     fg="#FDBA74", bg=self.skin["panel"], font=("Arial", 8),
                     wraplength=430, justify=tk.LEFT).pack(anchor=tk.W, padx=8, pady=(0, 6))
        tk.Label(rahmen,
                 text=("Anteil = Summe aller Rohstoffe dieses Gebäudetyps geteilt durch den "
                       "Gesamtertrag des Ortes (je Stunde)."),
                 fg="#6b7280", bg=self.skin["panel"], font=("Arial", 7),
                 wraplength=430, justify=tk.LEFT).pack(anchor=tk.W, padx=8, pady=(0, 6))

    def _karten_feld_waehlen(self, feld: int):
        self.karten_feld = feld
        self._render_view()

    def _karten_bauen(self, gebaeude_key: str):
        siedlung = getattr(self, "karten_siedlung", None)
        feld = getattr(self, "karten_feld", None)
        if siedlung is None or feld is None:
            return
        _sperre = self._nahrungssperre(siedlung)
        if _sperre:
            self._log(_sperre)
            return
        name = gelaende.gebaeude_name(gebaeude_key)
        # Daniel 30.10.2026: hoechstens ZWEI Bibliotheken je Spieler (eine je Karte). Eine zweite
        # anderswo ist ausdruecklich erlaubt (dort sammeln sich die Rohstoffe besser), eine dritte
        # nicht; die erste im Startdorf darf weg, sobald die zweite steht.
        if str(gebaeude_key).lower().startswith("bibliothek"):
            vorhanden = bibliotheken_im_spiel(self.state.settlements)
            if vorhanden >= BIBLIOTHEK_OBERGRENZE:
                self._log(f"Es sind höchstens {BIBLIOTHEK_OBERGRENZE} Bibliotheken möglich — "
                          "eine je Karte, eine dritte nicht. Reisse zuerst eine ab.")
                return
        if gebaeude_key == "verteidigungswall" and self.state._lokale_kasse_aktiv():
            self._log("Wall belegt kein Baufeld: im Dorfzentrum 'Wall errichten' waehlen.")
            return
        kosten = baukosten(gebaeude_key)
        if not kosten:
            self._log(f"Für {name} ist kein Preis hinterlegt — Bau abgebrochen.")
            return
        # Rohstoff- UND Siedler-Kosten gegen dieselben zwei Quellen prüfen, aus denen
        # `verbrauche_am_ort` gleich zahlt (Ortslager zuerst, dann der Reichsbestand). Vorher las
        # diese Vorprüfung nur den Reichsbestand - seit Teil 3 liegt der Startbestand aber im
        # ORT, und der Bau wurde mit "es fehlt holz" abgelehnt, obwohl die Siedlung es hatte
        # (gefunden vom Sammellauf: test_startspiel, test_durchspiel, test_gui_fehler).
        staende = {k: int(v.level) for k, v in self.state.research.items()}
        baubar, grund = bauen_auf_karte(
            siedlung, gebaeude_key, feld, forschungsstaende=staende, nur_pruefen=True)
        if not baubar:
            self._log(f"Bau nicht moeglich: {grund}")
            return
        fehlt = self.state.ortsdeckung(siedlung, kosten)
        if fehlt:
            self._log(f"Nicht genug Rohstoffe für {name}: es fehlt "
                      f"{', '.join(sorted(fehlt))}.")
            return
        # Oekonomie-Paket, Schritt 9, Teil 3: bezahlt wird aus dem LAGER DIESER Siedlung (Siedler
        # aus ihrer Bevoelkerung). Die Vorpruefung oben und die Buchung hier benutzen dieselben
        # zwei Quellen (Ortslager + Reichsbestand als Uebergang) - deshalb kann die Zahlung nicht
        # mehr halb gelingen.
        if self.state._lokale_kasse_aktiv() and not getattr(self.state, "admin_teststand", False):
            risiko = versorgungsschutz.risiko_nach_ausgabe(
                siedlung, kosten, baukosten, bau=(gebaeude_key, feld))
            if risiko:
                self._log(risiko[0])
                return
        # GPT-OEK03: Zuerst die Feldmutation auf einer KOPIE zu Ende pruefen.
        # Niemals Baukosten abbuchen und danach erst feststellen, dass der Bau
        # scheitert. Der echte Ort wird erst nach erfolgreicher Zahlung belegt.
        bau_probe = copy.deepcopy(siedlung)
        ok, meldung = bauen_auf_karte(bau_probe, gebaeude_key, feld,
                                     forschungsstaende=staende)
        if not ok:
            self._log(f"Bau vor Zahlung abgelehnt: {meldung}")
            return
        ok_zahlung, meldung_zahlung = self.state.verbrauche_am_ort(siedlung, kosten)
        if not ok_zahlung:
            self._log(f"Nicht genug im Lager von {siedlung.name} für {name}: {meldung_zahlung}")
            return
        siedlung.bauten = bau_probe.bauten
        siedlung.stufen = bau_probe.stufen
        self._log(f"{name} gebaut — {meldung}")
        self._menue_auffrischen()
        # astra-Nachprüfung 05.10.2026: „Nach dem Bau bleibt dasselbe Feld ausgewählt und das
        # Panel wechselt zur Gebäudeansicht." Vorher löschte das Spiel hier die Auswahl — der
        # Spieler sah nach dem Bauen kein Ergebnis, nur die Statuszeile.
        self._render_view()

    def _karten_wall_errichten(self):
        siedlung = getattr(self, "karten_siedlung", None)
        if siedlung is None:
            return
        ok, text = self.state.wall_errichten(siedlung)
        self._log(text)
        if ok:
            self._render_view()

    def _dorfzentrum_setzen(self, feld):
        """Setzt das mitgelieferte Dorfzentrum KOSTENLOS auf ein Feld des gewaehlten Dorfes.

        Schnitt S-2c-D, Daniel 01.11.2026 woertlich: "kostenlos bei jeder gruendung mitgesetzt
        aber das setzen lassen ist wichtig damit der spieler bestimmt welches feld seiner karte
        besetzt wird". Deshalb setzt die Gruendung nur das Kennzeichen `dorfzentrum_offen`; die
        Platzwahl trifft der Spieler hier, ohne Kosten, ohne Siedler und ohne Baukunst (wie die
        drei Startgebaeude aus S-1, die ebenfalls direkt in `bauten`/`stufen` schreiben).

        Der bezahlte Bauweg (`_karten_bauen` -> `bauen_auf_karte`) bleibt daneben bestehen und
        verlangt weiter Baukunst und Rohstoffe; `max_je_siedlung: 1` gilt fuer beide Wege.

        Geprueft wird VOR jeder Aenderung: offenes Kennzeichen, noch kein Dorfzentrum, Feld auf
        der Karte, Feld frei, Gelände erlaubt. Bei Ablehnung bleibt der Bestand unveraendert und
        der Grund steht im Log.
        """
        siedlung = getattr(self, "karten_siedlung", None) or self.state.aktive_siedlung()
        if siedlung is None:
            self._log("Kein Dorf gewaehlt — ein Dorfzentrum braucht ein Dorf.")
            return False
        if not getattr(siedlung, "dorfzentrum_offen", False):
            self._log(f"In {siedlung.name} ist kein Dorfzentrum zum Setzen offen.")
            return False
        if gebaeude_wirkung.gebaeude_stufe(siedlung, "lager") > 0:
            siedlung.dorfzentrum_offen = False
            self._log(f"{siedlung.name} hat bereits ein Dorfzentrum — hoechstens eines je Dorf.")
            return False
        try:
            feld = int(feld)
        except (TypeError, ValueError):
            self._log("Ungueltiges Feld — das Dorfzentrum bleibt im Gruendungspaket.")
            return False
        karte = getattr(siedlung, "karte", None) or {}
        raster = list(karte.get("raster") or [])
        if not raster or not (0 <= feld < len(raster)):
            self._log("Dieses Feld liegt nicht auf der Karte des Dorfes.")
            return False
        belegt = (siedlung.bauten or {}).get(str(feld))
        if belegt:
            self._log(f"Feld {feld} ist bereits belegt ({gelaende.gebaeude_name(belegt)}) — "
                      f"ein freies Feld waehlen.")
            return False
        erlaubt, grund = gelaende.bau_moeglich("lager", raster[feld])
        if not erlaubt:
            self._log(grund)
            return False
        siedlung.bauten[str(feld)] = "lager"
        siedlung.stufen[str(feld)] = 1
        siedlung.dorfzentrum_offen = False
        self._log(f"Dorfzentrum in {siedlung.name} auf Feld {feld} gesetzt — kostenlos aus dem "
                  f"Gruendungspaket (das Lager dieses Dorfes ist damit eingerichtet).")
        self._menue_auffrischen()
        self._render_view()
        return True

    def _karten_abreissen(self):
        siedlung = getattr(self, "karten_siedlung", None)
        feld = getattr(self, "karten_feld", None)
        if siedlung is None or feld is None:
            return
        gebaut = siedlung.bauten.get(str(feld))
        if not gebaut:
            return
        # GPT extern 28.10.2026: einen letzten Produzenten nicht unbemerkt
        # abbauen, wenn danach Holz/Stein dauerhaft unerreichbar waeren.
        # Ein bereits blockiertes Dorf darf weiterhin Felder freiraeumen.
        if self.state._lokale_kasse_aktiv() and not getattr(self.state, "admin_teststand", False):
            risiko = versorgungsschutz.risiko_nach_abriss(siedlung, feld, baukosten)
            if risiko:
                self._log(risiko[0])
                return
        # Handbuch: Abriss nach Bestaetigung, keinerlei Erstattung.
        # Daniel 30.10.2026: Die Bibliothek ist essenziell — die LETZTE darf nicht abgerissen
        # werden. Eine zweite woanders bauen und dann die erste abzureissen ist erlaubt.
        # SCHNITT S-2c (Daniel, 01.11.2026): Das Dorfzentrum ist das Lager des Dorfes und traegt
        # seine Lagerverwaltung - das EINE bleibt stehen (D-06). Erkannt wird ueber
        # `gelaende.finde_gebaeude`, damit auch der alte Anzeigename 'Lager' trifft.
        if gelaende.finde_gebaeude(str(gebaut)) == "lager":
            self._log("Das Dorfzentrum ist das Lager dieses Dorfes und kann nicht abgerissen "
                      "werden — es gibt genau eines je Dorf.")
            return
        if str(gebaut) == "bibliothek":
            _bibliotheken = sum(1 for _s in self.state.settlements
                                for _v in ((_s.bauten or {}).values()) if str(_v) == "bibliothek")
            if _bibliotheken <= 1:
                self._log("Die letzte Bibliothek kann nicht abgerissen werden — ohne sie gibt es "
                          "keine Forschung. Baue erst eine zweite, dann kannst du diese abreissen.")
                return
        # Ohne root wird der Weg auch in kopflosen Regeltests nutzbar.
        if getattr(self, 'root', None) is not None:
            from tkinter import messagebox
            if not messagebox.askyesno('Gebaeude abreissen',
                                      f'{gelaende.gebaeude_name(gebaut)} wirklich abreissen?\n'
                                      'Es gibt keine Rohstoffe zurueck.', parent=self.root):
                return
        siedlung.bauten.pop(str(feld), None)
        siedlung.stufen.pop(str(feld), None)
        self._menue_auffrischen()
        self._log(f"{gelaende.gebaeude_name(gebaut)} auf Feld {feld} abgerissen "
                  f"(keine Erstattung der Baustoffe — das Handbuch nennt keine).")
        self.karten_feld = None
        self._render_view()

    def _karten_ausbauen(self):
        """Hebt die Ausbaustufe des Gebaeudes auf dem gewaehlten Feld (W4b-5).

        Handbuch: Der Verteidigungswall hat 10 Stufen (Erdwall … Bollwerk), und die drei
        Ausbildungsstaetten werden stufenweise ausgebaut ('je hoeher die Stufe, desto
        schneller'). Preis: das n-fache des Grundpreises (data/baupreise.json).
        """
        siedlung = getattr(self, "karten_siedlung", None)
        feld = getattr(self, "karten_feld", None)
        if siedlung is None or feld is None:
            return
        _sperre = self._nahrungssperre(siedlung)
        if _sperre:
            self._log(_sperre)
            return
        gebaut = siedlung.bauten.get(str(feld))
        if not gebaut:
            return
        name = gelaende.gebaeude_name(gebaut)
        # GPT-OEK02: Original-Tutorial/Handbuch: Ausbauverbot gilt NUR fuer die
        # Bibliothek der Siedlung, in der gerade geforscht wird. Forschung in
        # Dorf A darf den Ausbau der Bibliothek in Dorf B nicht sperren.
        if gebaut == "bibliothek" and getattr(siedlung, "forschungsauftrag", None):
            laufend = (siedlung.forschungsauftrag or {}).get("gebiet", "")
            self._log(f"{name} kann nicht ausgebaut werden, solange {laufend} erforscht wird "
                      f"(Handbuch S. 12).")
            return
        stufe = gebaeude_wirkung.stufe_von_feld(siedlung, feld)
        grenze = gebaeude_wirkung.max_stufe(gebaut)
        if grenze is None:
            self._log(f"{name} kennt keinen Ausbau — das Handbuch nennt für dieses Gebäude "
                      f"keine Stufen.")
            return
        if stufe >= grenze:
            self._log(f"{name} ist bereits auf der höchsten Stufe ({grenze}).")
            return
        kosten = _ausbau_kosten(gebaut, stufe + 1, siedlung)
        # Dieselbe Deckungsfrage wie beim Bauen: Ortslager zuerst, dann der Reichsbestand.
        fehlt = self.state.ortsdeckung(siedlung, kosten)
        if fehlt:
            self._log(f"Nicht genug Rohstoffe für den Ausbau von {name}: es fehlt "
                      f"{', '.join(sorted(fehlt))}.")
            return
        # Oekonomie-Paket, Schritt 9, Teil 3: der Ausbau zahlt aus dem Lager DIESER Siedlung.
        if self.state._lokale_kasse_aktiv() and not getattr(self.state, "admin_teststand", False):
            risiko = versorgungsschutz.risiko_nach_ausgabe(siedlung, kosten, baukosten)
            if risiko:
                self._log(risiko[0])
                return
        ok_zahlung, meldung_zahlung = self.state.verbrauche_am_ort(siedlung, kosten)
        if not ok_zahlung:
            self._log(f"Nicht genug im Lager von {siedlung.name} für den Ausbau von {name}: "
                      f"{meldung_zahlung}")
            return
        siedlung.stufen[str(feld)] = stufe + 1
        self._log(f"{name} auf {gebaeude_wirkung.stufen_name(gebaut, stufe + 1)} ausgebaut "
                  f"(Stufe {stufe + 1}).")
        self._render_view()

    def _karten_zuwaeisen(self, siedlung):
        """Siedlungen aus alten Spielständen nachträglich eine Karte geben."""
        try:
            siedlung.karte = neue_siedlungskarte(
                [s.karte for s in self.state.settlements if s is not siedlung])
        except RuntimeError as fehler:
            self._log(f"Keine Karte zugewiesen: {fehler}")
            return
        self._log(f"{siedlung.name} hat jetzt eine {siedlung.karte['typ_name']}.")

    @staticmethod
    def _spaltenname(spalte: int) -> str:
        """A, B, C … als Spaltenbeschriftung — statt interner Feldnummern (astra-Gutachten)."""
        return chr(ord("A") + spalte) if 0 <= spalte < 26 else str(spalte)

    @staticmethod
    def _ertrag_kurz(gebaeude_key: str, art: str) -> str:
        """Ertrag eines Gebäudes auf diesem Feld, kurz: „4 Holz/h" oder „kein Rohstoffertrag"."""
        ertrag = gelaende.ertrag_pro_stunde(gebaeude_key, art)
        if isinstance(ertrag, dict):
            return " · ".join(f"{v:g} {k.capitalize()}/h" for k, v in ertrag.items())
        eintrag = gelaende.alle_gebaeude().get(gelaende.finde_gebaeude(gebaeude_key)) or {}
        stoff = str(eintrag.get("rohstoff") or "").strip()
        if ertrag is None:
            return f"+5 Wohnraum" if stoff == "" and "haus" in str(gebaeude_key).lower() else "kein Rohstoffertrag"
        return f"{ertrag:g} {stoff.capitalize()}/h" if stoff else f"{ertrag:g}/h"

    def _zeichne_siedlungskarte(self, siedlung, karte, eltern=None) -> None:
        """Die Siedlungskarte als Zeichenfläche (64-px-Felder), feinere Fassung.

        Vorher war das ein Raster kleiner Knöpfe mit abgeschnittenen Gebäudenamen; laut
        astra-Bildgutachten vom 05.10.2026 sah das „wie eine farbige Tabelle aus". Seit dem
        05.10.2026 kommen die Zeichen aus `src/karten_optik.py`, seit diesem Einhängen aus der
        feineren Fassung `src/karten_optik_fein.py` (zweite astra-Auswertung,
        `archiv/analysen/audits/ux_astra_karten_feinheit_2026-10-05.txt`, Kinder-Arbeit, vom Koordinator
        nachgerechnet): Baukörper 44 × 46 px je Gebäudefamilie mit Dach, Sockel, Tür und
        Stufenpips (4 × 4 px), Gelände mit größeren Strukturformen, Uferband nur an echten
        Land-Wasser-Grenzen, Wege 8 px mit 4 px Innenlinie, und die Koordinaten in einer 18 px breiten
        äußeren Rasterleiste. Der Auswahlrahmen ist seit dem 02.11.2026 das GELIEFERTE Bild
        (`kachelrahmen_auswahl.png`, volle Deckkraft, Register 130); der gezeichnete goldene Rahmen mit vier
        Eckwinkeln aus `karten_optik_fein.auswahl_plan_fein` bleibt Rueckfall, wenn das Bild fehlt.

        Gezeichnet wird in vier Durchgängen: (1) Gelände, Koordinaten · (2) Wege · (3) Gebäude ·
        (4) Auswahlrahmen zuletzt. So liegen die Wege unter den Baukörpern und die Auswahl
        sichtbar über allem.

        Die Beschriftung der Leiste sind die Buchstaben der Siedlungskarte (A–H) — dieselben, die
        das Detailpanel und der Spielstand nennen (`_spaltenname`). Ohne sie zeigte die Leiste
        Ziffern und das Panel daneben „D3": zwei Wahrheiten für dieselbe Koordinate.
        """
        zelle = 64
        spalten = int(karte.get("spalten") or 0)
        zeilen = int(karte.get("zeilen") or 0)
        raster = karte["raster"]
        # astra „Siedlung 3": „Koordinaten in eine 18 px breite beziehungsweise hohe äußere
        # Rasterleiste verlegen" — dieselbe Zahl liefert das Modul als KOORDINATEN_BREITE.
        rand = int(karten_optik_fein.KOORDINATEN_BREITE)
        canvas = tk.Canvas(eltern if eltern is not None else self.content,
                           width=rand + spalten * zelle,
                           height=rand + zeilen * zelle, bg="#17212B",
                           highlightthickness=0, bd=0)
        # Daniels Wunsch 05.10.2026 (rote Stiftskizze): die Bauauswahl steht RECHTS neben der
        # Karte, nicht darunter. Dafür rückt die Karte in einen waagerechten Block (`eltern`)
        # und liegt dort links. Ohne `eltern` bleibt der alte Weg (untereinander) gültig.
        if eltern is not None:
            canvas.pack(side=tk.LEFT, anchor=tk.NW)
        else:
            canvas.pack(anchor=tk.W, padx=10)
        gewaehlt = getattr(self, "karten_feld", None)

        def _feld_ecke(i: int):
            """Linke obere Ecke des Feldes i in Zeichenkoordinaten."""
            return rand + (i % spalten) * zelle, rand + (i // spalten) * zelle

        def _nachbararten(i: int) -> dict:
            """Die Geländearten der echten Nachbarfelder (für Uferband und Innenkanten)."""
            spalte, zeile = i % spalten, i // spalten
            arten: dict = {}
            if zeile > 0:
                arten["norden"] = raster[i - spalten]
            if spalte < spalten - 1:
                arten["osten"] = raster[i + 1]
            if zeile < zeilen - 1:
                arten["sueden"] = raster[i + spalten]
            if spalte > 0:
                arten["westen"] = raster[i - 1]
            return arten

        bauten: dict = {}
        for schluessel, gebaeude in (getattr(siedlung, "bauten", None) or {}).items():
            try:
                bauten[int(schluessel)] = gebaeude
            except (TypeError, ValueError):
                continue

        def _kein_wasser(i: int) -> bool:
            """Wasser trägt keinen Weg (astra: „Keine Wege automatisch durch Wasser")."""
            return 0 <= i < len(raster) and raster[i] not in ("nebelsee", "wasser")

        # ---- Durchgang 1: ECHTE historische 10x10-Kartengrafik -----------------------------
        # Nicht mehr: nachgezaehlte Farben, Fantasie-Baumembleme, vereinfachte Bergformen.
        # Die Positionen fuer Wege/Gebaeude stammen weiterhin aus dem Original-10x10-Raster.
        # Eine alte 8x7-Siedlung darf kein heimliches Ersatzbild bekommen.
        try:
            originalbild = tk.PhotoImage(file=str(originalkarten_grafik.grafikpfad(karte)))
        except (ValueError, FileNotFoundError, tk.TclError) as fehler:
            canvas.create_text(rand + 12, rand + 22, anchor="nw", fill="#FFB7A5",
                               text="Originalkarte nicht darstellbar: " + str(fehler),
                               width=spalten * zelle - 24)
            self.karten_canvas = canvas
            return
        canvas._originalkarten_bild = originalbild  # Tk-Grafikreferenz gegen Garbage Collection
        canvas.create_image(rand, rand, anchor="nw", image=originalbild, tags=("originalkarte",))
        # Die historische Originalkarte liegt als EIN Hintergrundbild im Canvas.
        # Jede der 100 Zellen braucht trotzdem eine eigene semantische Trefferregion,
        # damit GUI-Tests, Auswahlhilfen und zukuenftige barrierearme Bedienung
        # einzelne Felder wiederfinden. Keine Fuellung/Umrandung: Bild bleibt original.
        # Der Mausklick wird weiterhin ueber die Canvas-Koordinaten ausgewertet.
        for i in range(len(raster)):
            x0, y0 = _feld_ecke(i)
            canvas.create_rectangle(x0, y0, x0 + zelle, y0 + zelle,
                                    fill="", outline="", width=0,
                                    tags=("kartenfeld", f"feld:{i}"))

        # ---- Durchgang 1b: Kachelrahmen je Feld (C2-Lieferung, Kartenoptik Variante 2) ------
        # EIN Rahmenbild fuer ALLE Felder: einmal geladen, 100-mal gezeichnet - sonst haelt Tk
        # 100 Kopien derselben 64-px-Grafik im Speicher. Liegt ueber der Originalkarte und unter
        # Wegen und Gebaeuden, damit die Rahmen die Motive nicht anschneiden.
        _rahmen = self._lade_kachelrahmen("ruhe", zelle)             # Ruherahmen, passend zur Kachel
        if _rahmen is not None:                                      # ohne Rahmen bleibt die Karte wie bisher
            for i in range(len(raster)):                             # jedes Feld bekommt seinen Rahmen
                _rx, _ry = _feld_ecke(i)                             # linke obere Ecke des Feldes
                canvas.create_image(_rx, _ry, anchor="nw", image=_rahmen,
                                    tags=("kachelrahmen", f"feld:{i}"))

        # ---- Durchgang 2: Wege zwischen benachbarten bebauten Feldern ----------------------
        # Das Modul kennt weder Wasser noch Gebäude; die Auswahl der Richtungen macht deshalb
        # der Aufrufer: nur zwischen zwei bebauten Feldern, die kein Wasser sind.
        for i in sorted(bauten):
            if not _kein_wasser(i):
                continue
            spalte, zeile = i % spalten, i // spalten
            richtungen = []
            if zeile > 0 and (i - spalten) in bauten and _kein_wasser(i - spalten):
                richtungen.append("norden")
            if spalte < spalten - 1 and (i + 1) in bauten and _kein_wasser(i + 1):
                richtungen.append("osten")
            if zeile < zeilen - 1 and (i + spalten) in bauten and _kein_wasser(i + spalten):
                richtungen.append("sueden")
            if spalte > 0 and (i - 1) in bauten and _kein_wasser(i - 1):
                richtungen.append("westen")
            if richtungen:
                x0, y0 = _feld_ecke(i)
                karten_optik.zeichne(
                    canvas,
                    karten_optik_fein.wegabschnitt_plan(tuple(richtungen), x0, y0, zelle),
                    tags=("weg",))

        # ---- Durchgang 3: Gebäude als Baukörper samt Stufenpips -----------------------------
        # astra „Siedlung 3": Koordinaten UND Stufenanzeigen aus den Gebäudesilhouetten heraus-
        # nehmen; die genaue Stufe nennt der Ausbaubereich unter der Karte („Stufe 2 — …").
        for i, gebaut in sorted(bauten.items()):
            if not 0 <= i < len(raster):
                continue
            x0, y0 = _feld_ecke(i)
            stufe = gebaeude_wirkung.stufe_von_feld(siedlung, i)
            # A-2 (Daniels Spielbericht 31.10.2026: "Platzhalter durch Originalgrafik ersetzen"):
            # fuer Gebaeude mit BELEGTEM Originalmotiv steht das Handbuchbild auf dem Feld, sonst
            # weiter der gezeichnete Baukoerper. Die Ausbaustufe bleibt in beiden Faellen sichtbar.
            _motiv = self._lade_gebaeude_motiv(gebaut, max(28, int(zelle * 0.7)))   # 44 px auf der 64-px-Kachel
            if _motiv is not None:
                _mx, _my = int(x0 + zelle / 2), int(y0 + zelle / 2 + 2)
                canvas.create_image(_mx, _my, image=_motiv, tags=(f"feld:{i}", "motiv"))
                self._stufenpips_zeichnen(canvas, x0, y0, zelle, stufe, i)
            else:
                karten_optik.zeichne(
                    canvas,
                    karten_optik_fein.gebaeude_baukasten_plan(
                        gebaut, x0, y0, zelle, stufe=stufe,
                        max_stufe=gebaeude_wirkung.max_stufe(gebaut)),
                    tags=(f"feld:{i}",))

        # GPT W-02: gezeichneter Ortswall zwischen Baukoerper und Auswahl/Koordinaten.
        # Er belegt kein Feld; Randkoordinaten der Bauplatzklicks bleiben identisch.
        if self.state._lokale_kasse_aktiv():
            wall = dorfwall.kennwerte(siedlung, self.state.research)
            for teil in dorfwall.rahmen_plan(spalten, zeilen, zelle, rand,
                                             wall["stufe"], wall["zustand_prozent"]):
                canvas.create_line(*teil["linie"], fill=teil["farbe"],
                                   width=teil["breite"], tags=("dorfwall",))

        # ---- Durchgang 4: der Auswahlrahmen ZULETZT (liegt über allem) ----------------------
        # C2-Lieferung (02.11.2026, Register 130): auf dem gewaehlten Feld liegt der GELIEFERTE
        # Auswahlrahmen (`kachelrahmen_auswahl.png`, 64 px, volle Deckkraft) - EIN Bildobjekt.
        # Der gezeichnete goldene Rahmen (`auswahl_plan_fein`, astra Siedlung 3) ist nur noch
        # Rueckfall, wenn das Bild fehlt oder nicht ladbar ist; sonst lagen zwei Rahmen uebereinander.
        if gewaehlt is not None and 0 <= int(gewaehlt) < len(raster):
            x0, y0 = _feld_ecke(int(gewaehlt))                       # linke obere Ecke des Feldes
            _auswahl_bild = self._lade_kachelrahmen("auswahl", zelle)  # gelieferter Rahmen, 100 Prozent
            if _auswahl_bild is not None:                            # Bild vorhanden und geladen
                canvas.create_image(x0, y0, anchor="nw", image=_auswahl_bild,
                                    tags=(f"feld:{int(gewaehlt)}", "auswahl", "kachelrahmen_auswahl"))
            else:                                                    # Rueckfall: gezeichnete Fassung
                karten_optik.zeichne(canvas,
                                     karten_optik_fein.auswahl_plan_fein(x0, y0, zelle),
                                     tags=(f"feld:{int(gewaehlt)}", "auswahl"))

        # ---- Die Koordinatenleiste in der 18 px breiten äußeren Leiste ----------------------
        karten_optik.zeichne(
            canvas,
            karten_optik_fein.koordinatenleiste_plan(
                spalten, zeilen, zelle, rand=float(rand),
                spaltennamen=[self._spaltenname(s) for s in range(spalten)],
                zeilennamen=[str(z + 1) for z in range(zeilen)]))

        # Zusätzlich ein Klick auf die GANZE Fläche: die Rechnung aus der Mausposition ist
        # robuster als die Bindung je Objekt (und prüfbar, weil sie auch bei erzeugten
        # Klick-Ereignissen greift).
        def _klick(ereignis):
            spalte = int((ereignis.x - rand) // zelle)
            zeile = int((ereignis.y - rand) // zelle)
            if 0 <= spalte < spalten and 0 <= zeile < zeilen:
                self._karten_feld_waehlen(zeile * spalten + spalte)

        canvas.bind("<Button-1>", _klick)
        self.karten_canvas = canvas

    def _render_settlement_map(self):
        tk.Label(self.content, text="Siedlungskarte", font=("Blackletter", 20, "bold"),
                 fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 2))
        siedlung = getattr(self, "karten_siedlung", None)

        if siedlung is None or not getattr(siedlung, "karte", None):
            tk.Label(self.content, text="Noch keine Siedlung gewählt.", fg=self.skin["text"],
                     bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)
            mit_karte = [s for s in self.state.settlements if getattr(s, "karte", None)]
            if mit_karte:
                for s in mit_karte:
                    tk.Button(self.content, text=f"Karte von {s.name} öffnen",
                              command=lambda ss=s: self._oeffne_siedlungskarte(ss),
                              bg="#3e2723", fg=self.skin["gold"]).pack(anchor=tk.W, padx=10, pady=2)
            tk.Label(self.content, text="Siedlungen ohne Karte (aus älteren Spielständen):",
                     fg=self.skin["text"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(8, 0))
            for s in self.state.settlements:
                if not getattr(s, "karte", None):
                    tk.Button(self.content, text=f"{s.name} eine Karte zuweisen",
                              command=lambda ss=s: (self._karten_zuwaeisen(ss), self._render_view()),
                              bg=self.skin["button"], fg=self.skin["gold"]).pack(anchor=tk.W, padx=10, pady=2)
            if not self.state.settlements:
                tk.Label(self.content, text="Gründe im Dorfzentrum zuerst eine Siedlung.",
                         fg=self.skin["text"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=8)
            return

        karte = siedlung.karte
        tk.Label(self.content, text=f"{siedlung.name} — {karte['typ_name']}",
                 fg=self.skin["gold"], bg=self.skin["bg"],
                 font=("TkDefaultFont", 13, "bold")).pack(anchor=tk.W, padx=10)
        tk.Label(self.content, text="Wähle ein Feld auf der Karte. Rechts daneben steht, was dort "
                                    "gebaut werden kann und was es einbringt.",
                 fg="#F3F4F6", bg=self.skin["bg"], wraplength=800,
                 justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=(0, 2))
        # Schritt 9, Teil 3b: der Ortsbestand DIESER Siedlung steht hervorgehoben ueber der Karte.
        # Die Leiste ganz oben zeigt dagegen das ganze Reich — zwei Ansichten, zwei Zahlen
        # (KONTEXT_PAKET, Abschnitt 2, Teil 3b).
        _bestand = tk.Frame(self.content, bg="#1B2A2F", highlightbackground="#7FD1FF",
                            highlightthickness=1)
        _bestand.pack(fill=tk.X, padx=10, pady=(2, 4))
        tk.Label(_bestand, text="Ortsbestand dieser Siedlung (lokal — fuehrend seit Teil 3a)",
                 fg="#7FD1FF", bg="#1B2A2F", font=("TkDefaultFont", 10, "bold")
                 ).pack(anchor=tk.W, padx=8, pady=(6, 0))
        tk.Label(_bestand, text=ortsbestand_text(siedlung), fg="#F3F4F6", bg="#1B2A2F",
                 wraplength=820, justify=tk.LEFT).pack(anchor=tk.W, padx=8, pady=(0, 6))
        # Register 70/74: steht der Ort in Nahrungsnot, steht der Grund SICHTBAR ueber dem Lager -
        # sonst sucht der Spieler, warum nichts mehr gebaut, hergestellt oder ausgebildet wird.
        _not = self._nahrungssperre(siedlung)
        if _not:
            tk.Label(_bestand, text="⚠ " + _not, fg="#FDBA74", bg="#1B2A2F",
                     wraplength=820, justify=tk.LEFT,
                     font=("Arial", 9, "bold")).pack(anchor=tk.W, padx=8, pady=(0, 6))
        tk.Label(self.content, text="Zum Vergleich das ganze Reich: " + reichsbestand_text(self.state),
                 fg="#DAA520", bg=self.skin["bg"], wraplength=820, justify=tk.LEFT,
                 font=("Arial", 9)).pack(anchor=tk.W, padx=10, pady=(0, 4))
        zaehlung = ", ".join(f"{gelaende.name(a)} {n}" for a, n in karte["zaehlung"].items() if n)
        tk.Label(self.content, text=f"Vorteil: {karte['vorteil']} · {zaehlung}",
                 fg=self.skin["text"], bg=self.skin["bg"], wraplength=800,
                 justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=(0, 4))

        # Daniels Wunsch 05.10.2026 (rote Stiftskizze): Karte LINKS, die Bauauswahl RECHTS
        # daneben — vorher stand die Auswahl unter der Karte und der Platz daneben blieb leer.
        kartenblock = tk.Frame(self.content, bg=self.skin["bg"])
        kartenblock.pack(anchor=tk.W, padx=10)

        # astra-Bildgutachten 05.10.2026: 64-px-Felder mit Gelände-EMBLEM (Farbe allein
        # reicht nicht), Koordinaten statt interner Feldnummern, kräftiger Auswahlrahmen.
        # Vorher: ein Raster kleiner Knöpfe mit abgeschnittenen Namen („Steinm", „Holzfä").
        self._zeichne_siedlungskarte(siedlung, karte, eltern=kartenblock)

        # Dorfmauer ist Zustand der Siedlung, kein Baukoerper im 8x7-Raster.
        if self.state._lokale_kasse_aktiv():
            wall = dorfwall.kennwerte(siedlung, self.state.research)
            wallzeile = tk.Frame(self.content, bg=self.skin["panel"])
            wallzeile.pack(fill=tk.X, padx=10, pady=(4, 4))
            tk.Label(wallzeile,
                     text=(f"Dorfwall: {wall['name']} · Stufe {wall['stufe']} · "
                           f"Zustand {wall['zustand_prozent']:.0f}%"
                           if wall['stufe'] else "Dorfwall: noch nicht errichtet"),
                     fg=self.skin["gold"], bg=self.skin["panel"]).pack(side=tk.LEFT, padx=8)
            if not siedlung.mauer_besetzt:
                preis = kosten_text(baukosten("verteidigungswall"))
                tk.Button(wallzeile, text=f"Wall errichten / Wache besetzen ({preis})",
                          command=self._karten_wall_errichten, bg=self.skin["button"],
                          fg=self.skin["gold"]).pack(side=tk.RIGHT, padx=8, pady=3)

        legende = tk.Frame(self.content, bg=self.skin["bg"])
        legende.pack(anchor=tk.W, padx=10, pady=(4, 2))
        for art in gelaende.GELAENDEARTEN:
            tk.Label(legende, text="   ", bg=gelaende.farbe(art)).pack(side=tk.LEFT, padx=(5, 1))
            tk.Label(legende, text=gelaende.name(art), fg=self.skin["text"],
                     bg=self.skin["bg"]).pack(side=tk.LEFT)
        tk.Label(self.content, text="Sumpf ist nicht bebaubar (Handbuch S. 11). "
                                   "Gold umrandet = gewähltes Feld; die Punkte unter einem "
                                   "Gebäude zeigen seine Ausbaustufe.",
                 fg=self.skin["text"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(2, 4))

        # Daniels Wunsch 05.10.2026 (Stiftskizze): die Auswahl steht RECHTS neben der Karte —
        # als eigene Spalte im Kartenblock, nicht als Streifen unter der Karte.
        info = tk.Frame(kartenblock, bg=self.skin["panel"], highlightbackground="#5D4037",
                        highlightthickness=1)
        info.pack(side=tk.LEFT, anchor=tk.N, fill=tk.Y, padx=(12, 0))
        # A-3 (Daniels Spielbericht 31.10.2026): die Dorfuebersicht steht als dritte Spalte
        # rechts neben der Karte - welche Gebaeude, wie viele, welche Stufe, welcher Ertrag je
        # Stunde, welchen Anteil sie am Ortsertrag haben, und die Summenzeile. Sie steht VOR der
        # Feldauswahl, damit sie auch ohne gewaehltes Feld sichtbar ist.
        self._dorf_uebersicht_zeichnen(kartenblock, siedlung)
        feld = getattr(self, "karten_feld", None)
        if feld is None:
            tk.Label(info, text="Ein Feld auf der Karte anklicken, um dort zu bauen.",
                     fg=self.skin["text"], bg=self.skin["panel"]).pack(anchor=tk.W, padx=6, pady=6)
            # S-2c-D: solange der Platz des Dorfzentrums offen ist, sagt die Ansicht das auch
            # ohne gewaehltes Feld - sonst sucht der Spieler einen Knopf, den er nicht sieht.
            if getattr(siedlung, "dorfzentrum_offen", False) and not \
                    gebaeude_wirkung.gebaeude_stufe(siedlung, "lager"):
                tk.Label(info, text="Dorfzentrum: das Feld ist noch offen. Ein freies Feld "
                                    "anklicken, dann erscheint dort der Knopf zum Setzen.",
                         fg="#7FD1FF", bg=self.skin["panel"], wraplength=280,
                         justify=tk.LEFT).pack(anchor=tk.W, padx=6, pady=(0, 6))
            return

        art = karte["raster"][feld]
        gebaut = siedlung.bauten.get(str(feld))
        _spalten = int(karte["spalten"])
        _koord = f"{self._spaltenname(feld % _spalten)}{feld // _spalten + 1}"
        _bebaubar = gelaende.ist_bebaubar(art)
        _lage = "belegt" if gebaut else ("frei · bebaubar" if _bebaubar else "nicht bebaubar")
        tk.Label(info, text=f"{_koord} · {gelaende.name(art)} — {_lage}", fg=self.skin["gold"],
                 bg=self.skin["panel"], font=("TkDefaultFont", 11, "bold")).pack(anchor=tk.W, padx=6, pady=(6, 2))
        if not _bebaubar and not gebaut:
            tk.Label(info, text="Hier kannst du nicht bauen: Sumpf ist unbebaubar und damit "
                                "wertlos (Handbuch S. 11).",
                     fg="#FDBA74", bg=self.skin["panel"]).pack(anchor=tk.W, padx=6, pady=(0, 6))
            return

        if gebaut:
            stufe = gebaeude_wirkung.stufe_von_feld(siedlung, feld)
            grenze = gebaeude_wirkung.max_stufe(gebaut)
            erlaubt, warum = gelaende.bau_moeglich(gebaut, art)
            tk.Label(info, text=f"Hier steht: {gelaende.gebaeude_name(gebaut)} — "
                                f"{gebaeude_wirkung.stufen_name(gebaut, stufe)} ({warum})",
                     fg=self.skin["text"], bg=self.skin["panel"], wraplength=300,
                     justify=tk.LEFT).pack(anchor=tk.W, padx=6)
            knopfreihe = tk.Frame(info, bg=self.skin["panel"])
            knopfreihe.pack(anchor=tk.W, padx=6, pady=6)
            if grenze is None:
                tk.Label(knopfreihe, text="Kein Ausbau vorgesehen — das Handbuch nennt für "
                                          "dieses Gebäude keine Stufen.",
                         fg=self.skin["text"], bg=self.skin["panel"]).pack(side=tk.LEFT)
            elif stufe >= grenze:
                tk.Label(knopfreihe, text=f"Höchste Stufe erreicht ({grenze}) — "
                                          f"{gebaeude_wirkung.stufen_name(gebaut, grenze)}.",
                         fg=self.skin["text"], bg=self.skin["panel"]).pack(side=tk.LEFT)
            else:
                kosten = _ausbau_kosten(gebaut, stufe + 1, siedlung)
                tk.Button(knopfreihe, text=f"Ausbauen auf Stufe {stufe + 1} ({kosten_text(kosten)})",
                          command=self._karten_ausbauen, bg=self.skin["button"],
                          fg=self.skin["gold"], activebackground="#5D4037").pack(side=tk.LEFT)
            tk.Button(knopfreihe, text="Abreißen", command=self._karten_abreissen, bg="#3e2723",
                      fg=self.skin["gold"]).pack(side=tk.LEFT, padx=6)
            return

        # S-2c-D (Daniel 01.11.2026): Das Dorfzentrum ist mit der Gruendung schon bezahlt, nur der
        # PLATZ fehlt noch - der Spieler bestimmt ihn hier. Bewusst ein eigener Knopf neben dem
        # normalen Bauweg: `_karten_bauen` verlangt weiter Kosten und Baukunst, dieser Weg nicht.
        if getattr(siedlung, "dorfzentrum_offen", False) and not gebaeude_wirkung.gebaeude_stufe(
                siedlung, "lager"):
            _dz_ok, _dz_grund = gelaende.bau_moeglich("lager", art)
            if _dz_ok:
                _dz_rahmen = tk.Frame(info, bg="#1B2A2F", highlightbackground="#7FD1FF",
                                      highlightthickness=1)
                _dz_rahmen.pack(fill=tk.X, padx=6, pady=(6, 2))
                tk.Label(_dz_rahmen, text="Dorfzentrum einplanen", fg="#7FD1FF", bg="#1B2A2F",
                         font=("TkDefaultFont", 10, "bold")).pack(anchor=tk.W, padx=6, pady=(4, 0))
                tk.Label(_dz_rahmen, text="Es kommt kostenlos mit dem Gruendungspaket - du "
                                          "bestimmst das Feld.", fg="#C0C0C0", bg="#1B2A2F",
                         wraplength=280, justify=tk.LEFT).pack(anchor=tk.W, padx=6)
                tk.Button(_dz_rahmen, text="Dorfzentrum hier setzen (kostenlos)",
                          command=lambda f=feld: self._dorfzentrum_setzen(f),
                          bg="#2563EB", fg="white", activebackground="#1D4ED8",
                          activeforeground="white",
                          font=("TkDefaultFont", 10, "bold")).pack(anchor=tk.W, padx=6, pady=(2, 6))

        # FIX04: Der historische Screenshot nennt eigene Bereiche fuer Produktion und
        # Verteidigung; buildings.json hat fuenf Originalrubriken. Statt 20 gleichartigen
        # Knopfzeilen wird jeweils nur eine Rubrik angezeigt. Status, Forschung, Kosten
        # und Ortsdeckung werden aus DENSELBEN Funktionen wie beim wirklichen Bau gelesen.
        kategorien = baumenue_info.KATEGORIEN
        kategorie = getattr(self, "_karten_baukategorie", "Produktion")
        if kategorie not in kategorien:
            kategorie = "Produktion"
        self._karten_baukategorie = kategorie
        tk.Label(info, text=baumenue_info.SPIELERHILFE,
                 fg="#F5D18B", bg=self.skin["panel"], wraplength=310,
                 justify=tk.LEFT).pack(anchor=tk.W, padx=6, pady=(4, 2))
        zeile = tk.Frame(info, bg=self.skin["panel"])
        zeile.pack(anchor=tk.W, fill=tk.X, padx=6, pady=(5, 3))
        tk.Label(zeile, text="Baubereich:", fg=self.skin["text"],
                 bg=self.skin["panel"]).pack(side=tk.LEFT)
        auswahl = tk.StringVar(value=kategorie)
        tk.OptionMenu(zeile, auswahl, *kategorien,
                      command=lambda wert: (setattr(self, "_karten_baukategorie", wert),
                                            self._render_view())).pack(side=tk.LEFT, padx=5)

        if kategorie == "Verteidigung" and self.state._lokale_kasse_aktiv():
            tk.Label(info, text="Der Dorfwall belegt kein Kartenfeld. "
                         "Er wird oberhalb der Karte im Verteidigungsbereich errichtet.",
                     fg=self.skin["text"], bg=self.skin["panel"], wraplength=310,
                     justify=tk.LEFT).pack(anchor=tk.W, padx=6, pady=6)
            return

        staende = {k: int(v.level) for k, v in self.state.research.items()}
        angebote = baumenue_info.angebote(
            feld, art, siedlung,
            regelpruefung=lambda kennung: bauen_auf_karte(
                siedlung, kennung, feld, forschungsstaende=staende, nur_pruefen=True),
            kostenfunktion=baukosten,
            deckungspruefung=lambda preis: self.state.ortsdeckung(siedlung, preis),
            ertragsfunktion=self._ertrag_kurz,
            kategorie=kategorie,
            wall_ohne_feld=self.state._lokale_kasse_aktiv())
        verfuegbar = sum(angebot["baubar"] for angebot in angebote)
        tk.Label(info, text=(f"{kategorie}: {verfuegbar} sofort baubar, "
                             f"{len(angebote) - verfuegbar} gesperrt / nicht finanzierbar."),
                 fg=self.skin["text"], bg=self.skin["panel"], wraplength=310,
                 justify=tk.LEFT).pack(anchor=tk.W, padx=6)
        if not angebote:
            tk.Label(info, text="Keine passenden Gebäude in dieser Rubrik auf diesem Feld.",
                     fg=self.skin["text"], bg=self.skin["panel"], wraplength=310,
                     justify=tk.LEFT).pack(anchor=tk.W, padx=6, pady=6)
            return

        knopfreihe = tk.Frame(info, bg=self.skin["panel"])
        knopfreihe.pack(anchor=tk.W, fill=tk.X, padx=6, pady=6)
        for i, angebot in enumerate(angebote):
            text = (f"{angebot['name']} — {angebot['wirkung']}\n"
                    f"{angebot['ertrag']} · {kosten_text(angebot['kosten'])}\n"
                    f"Voraussetzung: {angebot['voraussetzung']}\n"
                    f"{angebot['status']}\n"
                    f"{angebot['standort_hinweis']}")
            # C2-Gebaeude-Optik (02.11.2026): das gerahmte Icon des Gebaeudes links am Bauknopf.
            # Mit Icon wird der Text um dessen Breite schmaler umbrochen, sonst liefe er darunter.
            _bau_icon = self._optik_bild(angebot["id"], 28, None, "kachel")
            _bau_zusatz = ({"image": _bau_icon, "compound": tk.LEFT, "wraplength": 255}
                           if _bau_icon is not None else {"wraplength": 295})
            tk.Button(knopfreihe, text=text, justify=tk.LEFT, anchor=tk.W,
                      # Gleicher Buchungsweg wie vorher: keine zweite Spiellogik.
                      command=lambda kk=angebot["id"]: self._karten_bauen(kk),
                      bg=self.skin["button"] if angebot["baubar"] else "#40352E",
                      fg=self.skin["gold"], activebackground="#5D4037",
                      **_bau_zusatz).grid(row=i, column=0, padx=2, pady=2, sticky=tk.EW)

    def _dimensionsname(self, z: int) -> str:
        """Der Name einer Dimension aus dem Limbus-Raster (`src/portalraum.py`)."""
        eintraege = portalraum.dimensionen()
        nummer = int(z)
        if 1 <= nummer <= len(eintraege):
            return str(eintraege[nummer - 1].get("name") or f"Weltkarte {nummer:02d}")
        return f"unbekannte Weltkarte {z}"

    def _sperre_text(self) -> str:
        """Restzeit bis zum naechsten Koordinatenwechsel (belegte 24-Stunden-Sperre)."""
        if self.state.letzter_wechsel is None:
            return "noch nie gewechselt"
        reste = 24 * 3600 - (time.time() - float(self.state.letzter_wechsel))
        if reste <= 0:
            return "abgelaufen"
        return f"noch {reste / 3600.0:.2f} h"

    def _portal_wechsel(self, nach_z: int):
        """Ein Weltensprung: erst pruefen, dann GENAU EINMAL abbuchen (W5-2, S-2b).

        Zaehlweise: `nach_z` ist die NUMMER aus der Kennung (4 = d04 = Midgard), so wie sie im
        Spielstand steht. `portalraum` rechnet mit dem INDEX 0..19; umgerechnet wird an EINER
        Stelle (`portalraum.index_von`). Bis S-2a wurden beide Zaehlweisen vermischt - der Knopf
        "20" war damit unerreichbar (Index 20 gibt es nicht) und "01" buchte auf die falsche Welt.

        Gesperrt ist der Sprung ausserdem, solange irgendetwas unterwegs ist (Daniel 01.11.2026,
        Anhang 2: "ein weltenwechsel ist fuer das dorf gar nicht moeglich solange auftraege
        einheiten truppen oder sonst was unterwegs ist auch handel z. b.").
        """
        if self._unterwegs_anzahl() > 0:
            meldung = ("Weltensprung gesperrt: solange Auftraege, Einheiten oder Handel unterwegs "
                       "sind, reist das Dorf nicht (Daniel 01.11.2026, Anhang 2).")
            self._log(meldung)
            self.state.messages.append({"text": meldung, "type": "portal"})
            return False
        von_z = int(self.state.eigene_dimension)
        nach_index = portalraum.index_von(int(nach_z))
        if nach_index < 0:
            meldung = f"Unbekannte Weltkarte: {nach_z}"
            self._log(meldung)
            self.state.messages.append({"text": meldung, "type": "portal"})
            return False
        mana = float(self.state.resources["mana"].amount)
        erlaubt, meldung = portalraum.wechsel_erlaubt(portalraum.index_von(von_z), nach_index,
                                                      mana, self.state.letzter_wechsel, time.time())
        if not erlaubt:
            self._log(meldung)
            self.state.messages.append({"text": meldung, "type": "portal"})
            return False
        gebucht = portalraum.nach_wechsel(mana, time.time())   # Festpreis, genau einmal
        self.state.resources["mana"].amount = float(gebucht["mana"])
        self.state.letzter_wechsel = gebucht["letzter_wechsel"]
        self.state.eigene_dimension = int(nach_z)
        if int(nach_z) not in self.state.eigene_dimensionen:
            self.state.eigene_dimensionen.append(int(nach_z))
        meldung = (f"Weltensprung nach Weltkarte {nach_z:02d} "
                   f"({self._dimensionsname(nach_z)}): {gebucht['kosten']} Mana abgebucht, "
                   f"24 Stunden gesperrt.")
        self._log(meldung)
        self.state.messages.append({"text": meldung, "type": "portal"})
        self._render_view()
        return True
    def _unterwegs_anzahl(self) -> int:
        """Wie viele Auftraege sind gerade unterwegs (Hinreise, am Ziel oder Rueckreise)?

        Daniel 01.11.2026 (docs/KONZEPT_SECHS_DOERFER_20261101.md, Anhang 2 "Umzug mit laufenden
        Auftraegen"): "ein weltenwechsel ist fuer das dorf gar nicht moeglich solange auftraege
        einheiten truppen oder sonst was unterwegs ist auch handel z. b." Handel laeuft im Code
        ebenfalls als Auftrag, deshalb genuegt EINE Liste. Die Uhr ist die SPIELUHR
        (`state.spielsekunden`) - dieselbe, mit der `auftraege.starten` die Reisezeiten stempelt;
        die Rechnerzeit waere hier eine zweite Zeitbasis.
        """
        return len(auftraege.laufende(self.state.auftraege, self.state.spielsekunden))

    # ------------------------------------------------------ Maersche auf der Weltkarte (M-1)
    @staticmethod
    def _portal_zelle(kante: int) -> int:
        """Kantenlaenge eines Feldes im Gelaendekaestchen in px - EINE Stelle fuer Zeichnen und Klick."""
        return max(4, 400 // max(1, int(kante or 20)))

    @staticmethod
    def _punkt_abstand(mx: float, my: float, x1: float, y1: float, x2: float, y2: float) -> float:
        """Abstand eines Punktes zur STRECKE (x1,y1)-(x2,y2) - die Trefferflaeche einer Marschlinie."""
        dx, dy = x2 - x1, y2 - y1                                              # Richtung der Strecke
        laenge2 = dx * dx + dy * dy                                            # Quadrat der Laenge
        if laenge2 <= 1e-9:                                                    # Strecke ist ein Punkt
            return ((mx - x1) ** 2 + (my - y1) ** 2) ** 0.5                    # Abstand zum Punkt
        t = ((mx - x1) * dx + (my - y1) * dy) / laenge2                        # Anteil auf der Strecke
        t = min(1.0, max(0.0, t))                                              # auf die Strecke begrenzen
        nx, ny = x1 + t * dx, y1 + t * dy                                       # naechster Punkt darauf
        return ((mx - nx) ** 2 + (my - ny) ** 2) ** 0.5                        # Abstand dorthin

    def _siedlung_nach_namen(self, name: str):
        """Die EIGENE Siedlung zu einem Namen - oder None. Keine Annahme, kein Ratewert."""
        for siedlung in (self.state.settlements or []):                        # jede eigene Siedlung
            if str(getattr(siedlung, "name", "")) == str(name or ""):           # Name stimmt
                return siedlung                                                # gefunden
        return None                                                            # sonst nichts

    def _feld_im_raster(self, feld, kante: int):
        """Ein Feld als (x, y), wenn es im Raster liegt - sonst None (nichts wird projiziert)."""
        try:                                                                   # Feld lesen
            x, y = int(feld[0]), int(feld[1])                                  # zwei Zahlen
        except (TypeError, ValueError, IndexError, KeyError):                  # unbrauchbares Feld
            return None                                                        # dann kein Feld
        if 0 <= x < int(kante) and 0 <= y < int(kante):                        # innerhalb der Karte
            return (x, y)                                                      # gueltiges Feld
        return None                                                            # ausserhalb -> nichts

    def _ort_feld(self, name: str, botname: str, kante: int):
        """Das Feld eines Ortes auf der Weltkarte: eigene Siedlung zuerst, dann ein fremdes Dorf.

        Die EIGENE Siedlung traegt ihr Weltfeld in `Settlement.x/y` (beim Gruenden aus dem vom
        Spieler gewaehlten Feld gesetzt). VORSCHLAG, offen benannt: dass dieses Feld im Portal-
        Raster dieselbe Bedeutung hat, ist NICHT belegt (zwei Koordinatenraeume, siehe
        `docs/design/MARSCH_ENTWURF_20261102.md` Abschnitt F). Deshalb steht die Aufloesung hier
        an EINER Stelle - eine spaetere Klaerung trifft nur diese Funktion.
        """
        siedlung = self._siedlung_nach_namen(str(name or ""))                  # eigene Siedlung?
        if siedlung is not None:                                               # ja: ihr Weltfeld
            return self._feld_im_raster((getattr(siedlung, "x", None),
                                         getattr(siedlung, "y", None)), kante)
        for bot, dorf in self._bot_doerfer_im_raster(kante):                   # sonst ein fremdes Dorf
            if str(dorf.name) == str(name or "") and (not botname or str(bot.name) == str(botname)):
                return self._feld_im_raster((dorf.x, dorf.y), kante)            # feste Dorfposition
        return None                                                            # nicht aufloesbar

    def _marsch_felder(self, eintrag: dict, kante: int = 20):
        """Start- und Zielfeld EINES Auftrags auf dem Kartenraster - `(von, nach)`, je None-able."""
        eintrag = eintrag if isinstance(eintrag, dict) else {}                 # Auftrag absichern
        ziel = eintrag.get("ziel") if isinstance(eintrag.get("ziel"), dict) else {}
        start = self._ort_feld(str(eintrag.get("von") or ""), "", kante)       # Startort
        zielname = str(ziel.get("dorf_name") or eintrag.get("nach") or "")     # Name des Zielorts
        zielfeld = self._ort_feld(zielname, str(ziel.get("bot_name") or ""), kante)
        return start, zielfeld                                                 # beide Felder

    def _marsch_gemeldet(self, eintrag: dict) -> None:
        """Einen nicht aufloesbaren Marsch EINMAL ins Protokoll schreiben - keine Linie erfinden."""
        merker = getattr(self, "_marsch_gemeldete", None)                      # Merker je Sitzung
        if not isinstance(merker, set):                                        # erster Aufruf
            merker = set()                                                     # neues Verzeichnis
            self._marsch_gemeldete = merker                                    # am Objekt merken
        schluessel = (str(eintrag.get("von") or ""), str(eintrag.get("nach") or ""))
        if schluessel in merker:                                               # schon gemeldet
            return                                                             # nicht wiederholen
        merker.add(schluessel)                                                 # als gemeldet merken
        self._log("Marsch %s -> %s liegt nicht im Kartenraster (Ort unbekannt) - keine Linie "
                  "gezeichnet, damit die Richtung nicht erfunden wird." % schluessel)

    def _marsch_laufend(self, kante: int = 20) -> list:
        """Alle Maersche, die gerade unterwegs sind - mit Phase, Restzeit und beiden Feldern.

        EINE Quelle: `state.auftraege` (keine zweite Auftragsliste) und die Spieluhr
        `state.spielsekunden`. Die Phase kommt aus `auftraege.stand` (oeffentliche Fassung).
        """
        opt = marsch_optik.optik()                                             # Einstellungen
        if not marsch_optik.aktiv(opt):                                        # Anzeige ausgeschaltet
            return []                                                          # dann keine Maersche
        jetzt = float(getattr(self.state, "spielsekunden", 0.0))               # die EINE Spieluhr
        ergebnis = []                                                          # was gezeichnet wird
        for eintrag in auftraege.laufende(getattr(self.state, "auftraege", None), jetzt):
            phase, rest = auftraege.stand(eintrag, jetzt)                      # Phase und Restzeit
            start, ziel = self._marsch_felder(eintrag, kante)                  # beide Felder
            if start is None or ziel is None:                                  # nicht aufloesbar
                self._marsch_gemeldet(eintrag)                                 # einmal melden
                continue                                                       # keine Linie zeichnen
            eigenes_ziel = self._siedlung_nach_namen(str(eintrag.get("nach") or "")) is not None
            ergebnis.append({"eintrag": eintrag, "phase": phase, "rest": float(rest),
                             "von": start, "nach": ziel, "eigenes_ziel": eigenes_ziel})
        return ergebnis                                                        # fertige Liste

    def _marsche_zeichnen(self, zeichenflaeche, zelle: int, kante: int) -> list:
        """Alle laufenden Maersche ins Gelaendekaestchen zeichnen - vier Objekte je Marsch.

        Sichtbar sind NUR Startfeld, Zielfeld, die Linie und die Bewegung (Vorgabe Daniel,
        Registerpunkt 140); Truppenart, Anzahl und Karren erscheinen nicht, und die Groesse des
        Zeichens haengt an KEINEM Auftragswert ("ein Handkarren sieht aus wie eine Armee").
        Jedes Objekt traegt den Sammel-Tag `marsch` und den Tag `marsch_<Nummer>`; die Pruefdatei
        zaehlt darueber. Rueckgabe: die gezeichneten Maersche (fuer die Zeile unter der Karte); die
        Trefferflaechen fuer den Klick stehen in `self._marsch_treffer`.
        """
        opt = marsch_optik.optik()                                             # alle Zahlen aus der Datei
        zeichenflaeche.delete("marsch")                                        # alte Maersche entfernen
        treffer = []                                                           # Trefferflaechen
        gezeichnet = []                                                        # was wirklich gezeichnet wurde
        gezaehlt = {}                                                          # gleiche Strecke zaehlen
        for nummer, marsch in enumerate(self._marsch_laufend(kante)):          # jeder laufende Marsch
            start, ziel = marsch["von"], marsch["nach"]                        # beide Felder
            farbe = str(opt["linie"]["farbe_hin"])                             # Farbe Hinreise
            richtung_von, richtung_nach = start, ziel                          # Laufrichtung
            if str(marsch["phase"]) == "rueckreise":                           # Rueckreise
                farbe = str(opt["linie"]["farbe_rueck"])                       # eigene Farbe
                richtung_von, richtung_nach = ziel, start                      # Richtung gespiegelt
            schluessel = (start, ziel)                                         # gleiche Strecke?
            wieviel = gezaehlt.get(schluessel, 0)                              # wie oft schon gezeichnet
            gezaehlt[schluessel] = wieviel + 1                                 # diesen Marsch mitzaehlen
            x1, y1 = start[0] * zelle + zelle / 2.0, start[1] * zelle + zelle / 2.0
            x2, y2 = ziel[0] * zelle + zelle / 2.0, ziel[1] * zelle + zelle / 2.0
            dx, dy = x2 - x1, y2 - y1                                          # Richtung der Strecke
            laenge = max(1e-6, (dx * dx + dy * dy) ** 0.5)                     # Laenge in px
            abstand = min(float(opt["mehrere"]["max_versatz_px"]),
                          wieviel * float(opt["mehrere"]["versatz_px"]))       # Versatz bei Gleichheit
            ox, oy = (-dy / laenge) * abstand, (dx / laenge) * abstand         # senkrecht zur Linie
            tags = ("marsch", "marsch_%d" % nummer)                            # zwei Tags je Objekt
            zeichenflaeche.create_line(x1 + ox, y1 + oy, x2 + ox, y2 + oy,     # die Linie
                                       fill=farbe, width=int(opt["linie"]["breite_px"]),
                                       dash=(opt["linie"]["dash"] or ()), tags=tags)
            for marker, feld in (("start_marker", start), ("ziel_marker", ziel)):   # Start und Ziel
                kante_px = float(opt[marker]["kante_px"]) / 2.0                # halbe Kantenlaenge
                mx, my = feld[0] * zelle + zelle / 2.0 + ox, feld[1] * zelle + zelle / 2.0 + oy
                zeichenflaeche.create_rectangle(mx - kante_px, my - kante_px,
                                                mx + kante_px, my + kante_px,
                                                outline=str(opt[marker]["farbe"]),
                                                width=int(opt[marker]["linienbreite"]), tags=tags)
            gesamt = max(1e-6, float(marsch["eintrag"].get("reisezeit") or 0.0))   # Dauer je Strecke
            anteil = min(1.0, max(0.0, 1.0 - marsch["rest"] / gesamt))         # Stand der Bewegung
            if str(marsch["phase"]) == "am_ziel":                              # steht am Ziel
                anteil = 1.0                                                   # Punkt genau am Ziel
            ax, ay = richtung_von[0] * zelle + zelle / 2.0 + ox, richtung_von[1] * zelle + zelle / 2.0 + oy
            bx, by = richtung_nach[0] * zelle + zelle / 2.0 + ox, richtung_nach[1] * zelle + zelle / 2.0 + oy
            mx, my = ax + (bx - ax) * anteil, ay + (by - ay) * anteil          # Stand des Zeichens
            groesse = float(opt["symbol"]["durchmesser_px"])                   # Groesse aus der Datei
            if str(opt["symbol"]["form"]) == "pfeil":                          # Fassung B: Pfeilspitze
                px, py = -(by - ay) / max(1e-6, ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5), \
                    (bx - ax) / max(1e-6, ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5)
                dxe, dye = (bx - ax) / max(1e-6, laenge), (by - ay) / max(1e-6, laenge)
                spitze = (mx + dxe * groesse, my + dye * groesse)              # vorderste Spitze
                links = (mx - dxe * groesse * 0.6 + px * groesse * 0.7,
                         my - dye * groesse * 0.6 + py * groesse * 0.7)        # linke Ecke
                rechts = (mx - dxe * groesse * 0.6 - px * groesse * 0.7,
                          my - dye * groesse * 0.6 - py * groesse * 0.7)       # rechte Ecke
                zeichenflaeche.create_polygon(spitze, links, rechts,
                                              fill=str(opt["symbol"]["fuellung"]),
                                              outline=str(opt["symbol"]["rand"]), tags=tags)
            else:                                                              # Fassung A/C: Kreis
                r = groesse / 2.0                                              # Radius aus Durchmesser
                zeichenflaeche.create_oval(mx - r, my - r, mx + r, my + r,
                                           fill=str(opt["symbol"]["fuellung"]),
                                           outline=str(opt["symbol"]["rand"]),
                                           width=int(opt["symbol"]["linienbreite"]), tags=tags)
            treffer.append({"seg": ((x1 + ox, y1 + oy), (x2 + ox, y2 + oy)),  # Strecke fuer den Klick
                            "marsch": marsch, "tag": "marsch_%d" % nummer})
            gezeichnet.append(dict(marsch, tag="marsch_%d" % nummer))       # fuer die Zeile unter der Karte
        self._marsch_treffer = treffer                                         # fuer den Klick merken
        return gezeichnet                                                      # die gezeichneten Maersche

    def _marsch_an(self, x: int, y: int, kante: int = 20):
        """Welcher Marsch liegt unter dem Klick? Das 6-px-Band um die Linie, naechster gewinnt."""
        zelle = self._portal_zelle(kante)                                      # Feldgroesse wie beim Zeichnen
        mx = int(x) * zelle + zelle / 2.0                                      # Klick in px
        my = int(y) * zelle + zelle / 2.0
        opt = marsch_optik.optik()                                             # Einstellungen
        toleranz = float(opt.get("klick", {}).get("toleranz_px") or 6)         # Trefferband in px
        bestes, kuerzeste = None, None                                         # Ergebnis und Abstand
        for eintrag in (getattr(self, "_marsch_treffer", None) or []):         # jede gezeichnete Linie
            (px1, py1), (px2, py2) = eintrag["seg"]                            # ihre beiden Enden
            abstand = self._punkt_abstand(mx, my, px1, py1, px2, py2)          # Abstand zum Klick
            if abstand <= toleranz and (kuerzeste is None or abstand < kuerzeste):
                bestes, kuerzeste = eintrag, abstand                           # naechste Linie gewinnt
        return bestes                                                          # None = keine Linie

    def _marsch_optionen(self, treffer: dict) -> None:
        """Ein Fenster mit dem OEFFENTLICHEN eines Marsches: von, nach, Restzeit.

        KEINE Truppenliste und keine Auftragsart: was unterwegs ist, verraet nichts ueber Art,
        Anzahl oder Geschwindigkeit (Vorgabe Daniel, Registerpunkt 140). Die Einzelheiten stehen im
        Auftragsbuch und im Postfach.
        """
        marsch = (treffer or {}).get("marsch") or {}                           # der getroffene Marsch
        eintrag = marsch.get("eintrag") or {}                                  # sein Auftrag
        opt = marsch_optik.optik()                                             # Einstellungen
        eigenes = bool(marsch.get("eigenes_ziel"))                             # Ziel ein eigenes Dorf?
        rest_text = marsch_optik.restzeit_text(marsch.get("rest") or 0.0, eigenes, opt)
        fenster = tk.Toplevel(self.root)                                       # eigenes Fenster
        fenster.title("Marsch: %s nach %s" % (eintrag.get("von"), eintrag.get("nach")))
        fenster.configure(bg=self.skin["bg"])                                  # Farbe wie das Spiel
        tk.Label(fenster, text="%s nach %s" % (eintrag.get("von"), eintrag.get("nach")),
                 font=("Blackletter", 16, "bold"), fg=self.skin["gold"], bg=self.skin["bg"],
                 wraplength=460, justify=tk.LEFT).pack(anchor=tk.W, padx=12, pady=(12, 2))
        zeilen = ["Restzeit: %s" % rest_text,                                  # grob oder genau
                  "Richtung: %s" % ("Rueckweg" if str(marsch.get("phase")) == "rueckreise"
                                    else "Hinweg")]
        tk.Label(fenster, text="\n".join(zeilen), fg=self.skin["text"], bg=self.skin["bg"],
                 justify=tk.LEFT, wraplength=460).pack(anchor=tk.W, padx=12)
        tk.Label(fenster, text=("Truppenart, Anzahl und Karren bleiben verborgen - ein Handkarren "
                                "sieht aus wie eine Armee. Einzelheiten stehen im Auftragsbuch "
                                "und im Postfach."),
                 fg="#C0C0C0", bg=self.skin["bg"], wraplength=460,
                 justify=tk.LEFT).pack(anchor=tk.W, padx=12, pady=(6, 2))
        tk.Button(fenster, text="Schliessen", bg="#3e2723", fg=self.skin["gold"],
                  command=fenster.destroy).pack(anchor=tk.E, padx=12, pady=10)
        self._log("Marsch %s nach %s: %s (%s)." % (eintrag.get("von"), eintrag.get("nach"),
                                                   rest_text, marsch.get("phase")))

    def _portal_klick(self, x: int, y: int, kante: int = 20):
        """Ein Klick ins Gelaendekaestchen: fremdes Dorf oder freies Feld (B-5, 02.11.2026).

        Steht auf dem Feld ein Bot-Dorf, oeffnen sich direkt die Optionen (Angriff planen /
        Spionage). Sonst gilt das bisherige Verhalten: das Feld wird nur ANGEWAEHLT, nichts
        gebucht (S-2b, Daniel 01.11.2026).
        """
        treffer = self._bot_dorf_an(x, y, kante)                       # steht hier ein fremdes Dorf?
        if treffer is not None:                                        # ja: Optionen anbieten
            self._bot_dorf_optionen(treffer[0], treffer[1])
            return True
        marsch = self._marsch_an(x, y, kante)                          # M-1: liegt hier eine Marschlinie?
        if marsch is not None:                                         # ja: nur das Oeffentliche zeigen
            self._marsch_optionen(marsch)
            return True
        return self._portal_feld_waehlen(x, y)                         # sonst Feld anwaehlen

    def _portal_feld_waehlen(self, x: int, y: int):
        """Ein Feld im Gelaendekaestchen anwaehlen (Schnitt S-2b) - merken, nicht buchen.

        Daniel 01.11.2026 (Anhang 3 Frage 23/30): der Dorftransfer beginnt mit einem Klick aufs
        freie Feld, danach folgt die Auswahl des Dorfes. Der Transfer selbst gehoert zu S-6;
        hier wird AUSDRUECKLICH nichts uebertragen, damit die Anzeige keine Mechanik vortaeuscht.
        """
        nummer = int(self.state.eigene_dimension)
        if portalraum.koordinate(int(x), int(y), portalraum.index_von(nummer)) is None:
            self._log(f"Feld {x}/{y} gehoert nicht zur Weltkarte {nummer:02d} "
                      f"({portalraum._achsen()} x {portalraum._achsen()} Felder).")
            return False
        self.portal_auswahl = (int(x), int(y))
        self._log(f"Feld {int(x)}/{int(y)} auf Weltkarte {nummer:02d} "
                  f"({self._dimensionsname(nummer)}) angewaehlt - der Dorftransfer folgt mit S-6.")
        self._render_view()
        return True

    def _render_portal(self):
        """Portal-Uebersicht (Schnitt S-2b): Weltkartenliste oben, Gelaendekaestchen darunter.

        Daniel 01.11.2026 (docs/KONZEPT_WELTKARTEN_UND_BOTS_20261101.md, Anhang 3 Frage 30):
        "oben die Liste der Weltkarten mit Namen, darunter das Gelaendekaestchen der aktuellen
        Welt zum Anklicken". Die Liste kommt aus `portalraum.weltkarten` (sechs belegte
        Weltnamen, bespielbar zuerst Midgard und Valhalla), die Bannerfarben sind belegt
        (portal.php 2005: "Eure Welt wird durch ein gruenes Banner markiert, fremde Welten durch
        rote"). Ein Klick auf eine Weltkarte ist gesperrt, solange etwas unterwegs ist
        (Daniel, Anhang 2).

        Das Gelaende JE FELD ist seit S-5 gebaut (Daniel 01.11.2026, Register 91/92): sieben
        Gelaendearten aus `data/gelaende.json` als 2x2-Bloecke mit stabilem Seed je Welt
        (`portalraum.weltbild`). Das Handbuch 2009 nennt KEIN Gelaende je Weltkartenfeld - das
        ist eine bewusste Remake-Entscheidung, keine Originalregel. Das Gelaende hat keine
        Bauplatz-, Rohstoff- oder Ertragswirkung; es ist reine Anzeige. Die Bannerfarbe der Welt
        bleibt in der Liste oben sichtbar, die Karte selbst zeigt Gelaende, Gitterlinien, Legende,
        die voruebergehende Feldauswahl und seit B-5 (02.11.2026) die FREMDEN DOERFER als
        anklickbare Zeichen: ein Klick oeffnet Angriff planen oder Spionage. Gezeigt wird nur, was
        offen sichtbar ist - Wall, Taktik, Truppen und Vorraete weiterhin nicht.
        """
        farben = {"gruen": "#2ecc40", "rot": "#e53935"}
        tk.Label(self.content, text="Portal", font=("Blackletter", 20, "bold"),
                 fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        tk.Label(self.content, text=portalraum.beschreibung(), fg="#C0C0C0", bg=self.skin["bg"],
                 wraplength=760, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=(0, 6))

        nummer = int(self.state.eigene_dimension)
        eigene = list(self.state.eigene_dimensionen)
        # Zaehlweisen nicht mischen (S-5, belegt durch die Pruefdatei): der Spielstand fuehrt die
        # NUMMER (1..20, d04 = 4), `portalraum.anzeige_raster`/`portalfarbe` rechnen mit dem INDEX
        # (0..19). Bis hierher wurde die Nummernliste ungefiltert weitergegeben - die eigene
        # Weltkarte erschien dadurch als FREMDE (Bannerfarbe rot). Die Umrechnung liegt an EINER
        # Stelle (`portalraum.index_von`), `weltkarten` bekommt weiter die Nummern.
        eigene_index = [i for i in (portalraum.index_von(n) for n in eigene) if i >= 0]
        laufend = self._unterwegs_anzahl()

        # --- 1. OBEN: die sechs Weltkarten mit Namen und Kennzeichen ---
        tk.Label(self.content, text="Weltkarten", fg=self.skin["gold"], bg=self.skin["bg"],
                 font=("TkDefaultFont", 11, "bold")).pack(anchor=tk.W, padx=10)
        for eintrag in portalraum.weltkarten(eigene, laufend):
            zeile = tk.Frame(self.content, bg=self.skin["panel"])
            zeile.pack(fill=tk.X, padx=10, pady=1)
            tk.Label(zeile, text=f"{eintrag['nummer']:02d}", width=3, anchor=tk.W, fg="#DAA520",
                     bg=self.skin["panel"], font=("TkDefaultFont", 10, "bold")).pack(
                         side=tk.LEFT, padx=(6, 2))
            tk.Label(zeile, text=eintrag["name"], width=14, anchor=tk.W, fg=self.skin["text"],
                     bg=self.skin["panel"]).pack(side=tk.LEFT)
            tk.Label(zeile, text=eintrag["status_text"],
                     fg=farben.get(eintrag["farbe"], "#8a8a8a"), bg=self.skin["panel"]).pack(
                         side=tk.LEFT, padx=8)
            if eintrag["waehlbar"]:
                tk.Button(zeile, text="Weltensprung", bg="#3e2723", fg=self.skin["gold"],
                          command=lambda n=eintrag["nummer"]: self._portal_wechsel(n)).pack(
                              side=tk.RIGHT, padx=6)
            else:
                tk.Label(zeile, text=eintrag["grund"], fg="#8a8a8a", bg=self.skin["panel"],
                         font=("TkDefaultFont", 8)).pack(side=tk.RIGHT, padx=6)

        # --- 2. DARUNTER: das Gelaendekaestchen der aktuellen Welt, Felder anklickbar ---
        kante = portalraum._achsen()
        tk.Label(self.content, text=(f"Gelaendekaestchen der Weltkarte {nummer:02d} - "
                                     f"{self._dimensionsname(nummer)} "
                                     f"({kante} x {kante} = {portalraum.feld_zahl()} Felder, "
                                     f"ein Klick waehlt ein Feld)"),
                 fg="#DAA520", bg=self.skin["bg"], wraplength=760, justify=tk.LEFT).pack(
                     anchor=tk.W, padx=10, pady=(8, 0))
        zelle = self._portal_zelle(kante)
        # M-1 (Vorgabe Daniel 02.11.2026, Register 140): die GROBE Restzeit steht als Zeile UEBER dem
        # Kaestchen - unter der Karte waere sie in diesem Fenster nur nach dem Scrollen zu sehen
        # (gemessen: Leinwand 296..696 px, Fenster 744 px hoch). Truppenart und Anzahl stehen NICHT da.
        laufende_maersche = self._marsch_laufend(kante)
        if laufende_maersche:                                          # wenigstens ein Marsch laeuft
            zeilen = ["%s nach %s: %s" % (marsch["eintrag"].get("von"),
                                          marsch["eintrag"].get("nach"),
                                          marsch_optik.restzeit_text(marsch["rest"],
                                                                     marsch["eigenes_ziel"]))
                      for marsch in laufende_maersche]                 # je Marsch eine kurze Zeile
            tk.Label(self.content, text="Unterwegs: " + " | ".join(zeilen),
                     fg="#DAA520", bg=self.skin["bg"], wraplength=760, justify=tk.LEFT,
                     font=("TkDefaultFont", 9)).pack(anchor=tk.W, padx=10, pady=(2, 0))
        felder = portalraum.anzeige_raster(portalraum.index_von(nummer), 10, eigene_index)
        zeichenflaeche = tk.Canvas(self.content, width=kante * zelle, height=kante * zelle,
                                   bg=self.skin["bg"], highlightthickness=0)
        zeichenflaeche.pack(anchor=tk.W, padx=10, pady=4)
        for feld in felder:
            x1, y1 = feld["x"] * zelle, feld["y"] * zelle
            fuellung = feld.get("gelaende_farbe") or farben.get(feld["farbe"], "#555555")
            zeichenflaeche.create_rectangle(x1, y1, x1 + zelle, y1 + zelle,
                                            fill=fuellung, outline="#111111")
        # B-5 (Vorgabe Daniel 02.11.2026): fremde Doerfer stehen jetzt AUF der Weltkarte und sind
        # anklickbar - der Klick oeffnet Angriff/Spionage. Gezeichnet werden nur oeffentliche
        # Angaben; Wall, Taktik, Truppen und Vorraete kommen ausschliesslich ueber einen Bericht.
        for bot, dorf in self._bot_doerfer_im_raster(kante):
            x1, y1 = int(dorf.x) * zelle, int(dorf.y) * zelle          # linke obere Ecke des Feldes
            cx, cy = x1 + zelle / 2.0, y1 + zelle / 2.0                # Feldmitte
            halb = max(3.0, zelle * 0.24)                              # halbe Kantenlaenge des Zeichens
            zeichenflaeche.create_rectangle(cx - halb, cy - halb, cx + halb, cy + halb,
                                            fill="#B45309", outline="#FFE8C2", width=2,
                                            tags=("portalbote",))      # das fremde Dorf
            zeichenflaeche.create_line(cx - halb, cy - halb, cx + halb, cy + halb,
                                       fill="#FFE8C2", tags=("portalbote",))
            zeichenflaeche.create_line(cx - halb, cy + halb, cx + halb, cy - halb,
                                       fill="#FFE8C2", tags=("portalbote",))
        # M-1 (Vorgabe Daniel 02.11.2026, Register 140): die LAUFENDEN Maersche als Linie mit
        # eigenem Zeichen-Tag. Gespeist aus `state.auftraege` (keine zweite Auftragsliste), vier
        # Objekte je Marsch, KEINE Truppenart und keine Anzahl im Bild. Der Tag `marsch` ist neu;
        # die Dorf-Zaehlwache auf `portalbote` bleibt dadurch unberuehrt.
        self._marsche_zeichnen(zeichenflaeche, zelle, kante)            # Linie, Start, Ziel, Zeichen
        # Legende: die sieben Gelaendearten mit Name und Haeufigkeit, direkt aus den Daten.
        legende = tk.Frame(self.content, bg=self.skin["bg"])
        legende.pack(anchor=tk.W, padx=10, pady=(2, 0))
        tk.Label(legende, text="Gelaende:", fg="#DAA520", bg=self.skin["bg"]).pack(side=tk.LEFT)
        for eintrag in portalraum.legende():
            tk.Label(legende, text="", bg=eintrag["farbe"], width=2).pack(side=tk.LEFT, padx=(6, 2))
            tk.Label(legende, text=f"{eintrag['name']} {eintrag['haeufigkeit']}",
                     fg=self.skin["text"], bg=self.skin["bg"],
                     font=("TkDefaultFont", 8)).pack(side=tk.LEFT)
        hinweis = next((f["gelaende_grund"] for f in felder if f.get("gelaende_grund")), "")
        if hinweis:
            tk.Label(self.content, text=hinweis, fg="#e53935", bg=self.skin["bg"],
                     wraplength=760, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=(2, 0))
        auswahl = getattr(self, "portal_auswahl", None)
        if auswahl:
            ax, ay = int(auswahl[0]), int(auswahl[1])
            x1, y1 = ax * zelle, ay * zelle
            zeichenflaeche.create_rectangle(x1, y1, x1 + zelle, y1 + zelle,
                                            outline="#38BDF8", width=3)
        zeichenflaeche.bind("<Button-1>",
                            lambda ereignis: self._portal_klick(ereignis.x // zelle,
                                                                ereignis.y // zelle, kante))
        if auswahl:
            ax, ay = int(auswahl[0]), int(auswahl[1])
            try:
                gel = portalraum.gelaende_von_feld(nummer, ax, ay)
                gel_text = f" - Gelaende: {gel['name']}"
            except portalraum.WeltbildFehler:
                gel_text = ""
            tk.Label(self.content, text=(f"Angewaehltes Feld: x={ax}, "
                                         f"y={ay}{gel_text} auf Weltkarte {nummer:02d} "
                                         f"({self._dimensionsname(nummer)}). Der Dorftransfer folgt "
                                         f"mit S-6 - hier wird noch nichts uebertragen."),
                     fg="#38BDF8", bg=self.skin["bg"], wraplength=760, justify=tk.LEFT).pack(
                         anchor=tk.W, padx=10)
        else:
            tk.Label(self.content, text="Noch kein Feld gewaehlt: ein Klick ins Kaestchen waehlt es aus.",
                     fg="#8a8a8a", bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)
        tk.Label(self.content, text=("Gelaende je Feld: dazu nennt das Handbuch nichts - das Kaestchen "
                                     "zeigt die belegten Bannerfarben (eigene Welt gruen, fremde Welt "
                                     "rot). Gelaendefarben je Feld kommen mit dem Weltbild (S-5)."),
                 fg="#8a8a8a", bg=self.skin["bg"], wraplength=760, justify=tk.LEFT).pack(
                     anchor=tk.W, padx=10, pady=(2, 6))

        # --- 3. Kosten, Sperre und Mannavorrat (unveraendert aus W5-2) ---
        mana = float(self.state.resources["mana"].amount)
        index = portalraum.index_von(nummer)
        erlaubt, meldung = portalraum.wechsel_erlaubt(index, index, mana,
                                                      self.state.letzter_wechsel, time.time())
        tk.Label(self.content, text=(f"Mana: {int(mana)} · Weltensprung kostet "
                                     f"{portalraum.wechselkosten()} · Sperre: {self._sperre_text()}"),
                 fg=self.skin["text"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(4, 2))
        tk.Label(self.content,
                 text=("Weltensprung moeglich." if erlaubt else f"Zurzeit nicht moeglich: {meldung}"),
                 fg="#DAA520" if erlaubt else self.skin["red"], bg=self.skin["bg"]).pack(
                     anchor=tk.W, padx=10)
        tk.Label(self.content, text=("(Unser Mana liegt in EINEM gemeinsamen Vorrat - das Handbuch "
                                     "verlangt die 5.000 Mana aus einer Siedlung. Vermerkt, noch "
                                     "nicht je Siedlung.)"),
                 fg="#8a8a8a", bg=self.skin["bg"], wraplength=760, justify=tk.LEFT).pack(
                     anchor=tk.W, padx=10, pady=(0, 6))

        tk.Label(self.content, text="Welten anderer Spieler:", fg="#C0C0C0",
                 bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 0))
        for bot in self.state.bots:
            frame = tk.Frame(self.content, bg=self.skin["panel"])
            frame.pack(fill=tk.X, padx=10, pady=2)
            tk.Label(frame, text=bot.name, fg=self.skin["text"], bg=self.skin["panel"], width=15,
                     anchor=tk.W).pack(side=tk.LEFT, padx=5)
            tk.Label(frame, text=f"Fraktion: {bot.faction}", fg="#DAA520",
                     bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
            tk.Button(frame, text="Besuchen", command=lambda b=bot: self._visit_bot(b),
                      bg="#3e2723", fg=self.skin["gold"]).pack(side=tk.RIGHT, padx=5)
    def _visit_bot(self, bot: BotPlayer):
        self._log("Besuche andere Spielerwelten nicht im Singleplayer-Modus.")

    def _render_storage(self, eigener_titel: bool = True):
        """Die LAGERVERWALTUNG des aktiven Ortes — seit S-2c steht sie IM DORFZENTRUM.

        Zwei Aufrufer, EINE Anzeige (F-04-Muster, keine zweite Rechen- oder Lesestelle):
        `_render_overview` (Menuepunkt "Dorfzentrum") ruft sie mit `eigener_titel=False` auf -
        dann kommt nur der Inhalt, die Seitenueberschrift setzt das Dorfzentrum. Die alte Route
        "Lager" gibt es seit S-2c nicht mehr im Menue; sie bleibt technisch erreichbar
        (tests/test_baseline.py besucht JEDE Route) und sagt hier offen, dass sie stillgelegt ist.
        """
        if eigener_titel:
            tk.Label(self.content, text="Lager — stillgelegt", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
            tk.Label(self.content, text="Dieser Menuepunkt ist am 01.11.2026 im Dorfzentrum aufgegangen (Schnitt S-2c: Das Dorfzentrum IST das Lager). Die Verwaltung steht unter „Dorfzentrum“ im Menue; hier bleiben nur die Bestaende sichtbar.", fg="#FDBA74", bg=self.skin["bg"], wraplength=780, justify=tk.LEFT).pack(anchor=tk.W, padx=10)
        else:
            tk.Label(self.content, text="Lagerverwaltung dieses Dorfes:", font=("TkDefaultFont", 12, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(12, 0))
            tk.Label(self.content, text="Bestand, Waren, Einheiten und Werkstaetten des aktiven Ortes — eine Ansicht, keine zweite Kasse.", fg=self.skin["text"], bg=self.skin["bg"], wraplength=780, justify=tk.LEFT).pack(anchor=tk.W, padx=10)
        # Teil 6: das LOKALE Lager des AKTIVEN Ortes — die Felder, die seit Teil 3a führen
        # (`Settlement.vorraete/waren/einheiten/bevoelkerung`). Darunter steht weiter die
        # Gesamtsicht (Reich) aus dem Übergangsbestand. Bis Teil 6 füllen sich diese lokalen
        # Felder nur über Transport und Gründung — das steht hier ehrlich dabei, statt eine
        # leere Liste als Spielinhalt auszugeben.
        _ort = self.state.aktive_siedlung()
        if _ort is not None:
            _bestand = tk.Frame(self.content, bg="#1B2A2F", highlightbackground="#7FD1FF",
                                highlightthickness=1)
            _bestand.pack(fill=tk.X, padx=10, pady=(8, 4))
            tk.Label(_bestand, text=f"Ortslager der aktiven Siedlung: {_ort.name}",
                     fg="#7FD1FF", bg="#1B2A2F", font=("Arial", 10, "bold"),
                     anchor=tk.W).pack(anchor=tk.W, padx=8, pady=(6, 0))
            tk.Label(_bestand, text=ortsbestand_text(_ort), fg="#C0C0C0", bg="#1B2A2F",
                     wraplength=760, justify=tk.LEFT, font=("Arial", 9)).pack(anchor=tk.W, padx=8)
            _waren_lokal = ", ".join(f"{k} {v}" for k, v in sorted((_ort.waren or {}).items())) or "keine"
            _einh_lokal = ", ".join(f"{k} {v}" for k, v in sorted((_ort.einheiten or {}).items())) or "keine"
            tk.Label(_bestand, text=f"Waren vor Ort: {_waren_lokal}", fg="#C0C0C0", bg="#1B2A2F",
                     wraplength=760, justify=tk.LEFT, font=("Arial", 9)).pack(anchor=tk.W, padx=8)
            tk.Label(_bestand, text=f"Einheiten vor Ort: {_einh_lokal}", fg="#C0C0C0", bg="#1B2A2F",
                     wraplength=760, justify=tk.LEFT, font=("Arial", 9)).pack(anchor=tk.W, padx=8, pady=(0, 6))
        else:
            tk.Label(self.content, text="Noch keine Siedlung — es gibt (noch) kein Ortslager.",
                     fg="#8a8a8a", bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)
        tk.Label(self.content, text="Waren (Reich/Übergang — die 17 Originalwaren aus data/items.json):", fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 0))
        tk.Label(self.content, text=werkstatt.lager_text(self.state.waren), fg="#C0C0C0", bg=self.skin["bg"], wraplength=760, justify=tk.LEFT).pack(anchor=tk.W, padx=10)
        goods_frame = tk.Frame(self.content, bg=self.skin["panel"])
        goods_frame.pack(fill=tk.X, padx=10, pady=5)
        cols = 6
        for idx, (key, menge) in enumerate(sorted(self.state.waren.items())):
            row = idx // cols
            col = idx % cols
            cell = tk.Frame(goods_frame, bg=self.skin["panel"], padx=10, pady=10, relief=tk.RIDGE, borderwidth=1)
            cell.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
            goods_frame.grid_columnconfigure(col, weight=1)
            goods_frame.grid_rowconfigure(row, weight=1)
            _ware_bild = self._lade_icon(WARE_ICONS.get(key, ""))
            if _ware_bild is not None:
                tk.Label(cell, image=_ware_bild, bg=self.skin["panel"]).pack(pady=(0, 4))
            else:
                tk.Label(cell, text="?", fg=self.skin["text"], bg=self.skin["panel"], font=("Arial", 16)).pack(pady=(0, 4))
            tk.Label(cell, text=key, fg=self.skin["text"], bg=self.skin["panel"], font=("Arial", 9)).pack()
            tk.Label(cell, text=str(menge), fg=self.skin["gold"], bg=self.skin["panel"], font=("Arial", 11, "bold")).pack(pady=(2, 0))
        tk.Label(self.content, text="Einheiten (Reich/Übergang):", fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 0))
        units_frame = tk.Frame(self.content, bg=self.skin["panel"])
        units_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        ucols = 6
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for idx, (key, u) in enumerate(self.state.units.items()):
            row = idx // ucols
            col = idx % ucols
            cell = tk.Frame(units_frame, bg=self.skin["panel"], padx=8, pady=8, relief=tk.RIDGE, borderwidth=1)
            cell.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
            units_frame.grid_columnconfigure(col, weight=1)
            units_frame.grid_rowconfigure(row, weight=1)
            _bild = self._lade_icon(UNIT_ICONS.get(key, ""))
            if _bild is not None:
                tk.Label(cell, image=_bild, bg=self.skin["panel"]).pack(pady=(0, 4))
            else:
                tk.Label(cell, text="?", fg=self.skin["text"], bg=self.skin["panel"], font=("Arial", 16)).pack(pady=(0, 4))
            tk.Label(cell, text=u.name, fg=self.skin["text"], bg=self.skin["panel"], font=("Arial", 9)).pack()
            tk.Label(cell, text=str(u.count), fg=self.skin["gold"], bg=self.skin["panel"], font=("Arial", 11, "bold")).pack(pady=(2, 0))

        # Teil 6c: die Werkstaetten und ihre Warteschlangen liegen IM ORT
        # (`Settlement.werkstaetten`), nicht mehr in einer reichsweiten Schlange. Gezeigt wird nur,
        # was WIRKLICH auf der Karte DIESER Siedlung steht (`werkstatt.werkstaetten_bestand`), und
        # die Uhr ist die Spieluhr (`state.spielsekunden`), nicht die Rechnerzeit — die Ware kommt
        # in `ort_tick` an.
        tk.Label(self.content, text="Werkstätten vor Ort:", fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 0))
        _bestand_ort = {k: v for k, v in (werkstatt.werkstaetten_bestand([_ort]) if _ort is not None
                                         else {}).items() if v > 0}
        if not _bestand_ort:
            tk.Label(self.content, text="Noch keine Werkstatt gebaut — auf der Siedlungskarte bauen.",
                     fg="#8a8a8a", bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)
        for kennung in sorted(_bestand_ort):
            schlange = ((_ort.werkstaetten or {}) if _ort is not None else {}).get(kennung)
            _name = (schlange or werkstatt.neue_warteschlange(kennung, _bestand_ort[kennung])
                     ).get("werkstatt")
            rahmen = tk.Frame(self.content, bg=self.skin["panel"])
            rahmen.pack(fill=tk.X, padx=10, pady=3)
            tk.Label(rahmen, text=f"{_name} ({_bestand_ort[kennung]} Stück vor Ort)",
                     fg=self.skin["text"], bg=self.skin["panel"], width=28, anchor=tk.W).pack(side=tk.LEFT, padx=5)
            # A-1 (Daniels Spielbericht): EINE Stueckzahl je Werkstatt statt N Einzelklicks.
            # Zahlfeld, -/+, Schieberegler und eine Vorschau, die je Ware dieselbe Zahl nennt,
            # die der Kern annimmt.
            _var = self._ware_menge_var(kennung)
            _leiste = tk.Frame(self.content, bg=self.skin["bg"])
            _leiste.pack(fill=tk.X, padx=18, pady=(0, 2))
            _vorschau = tk.Label(_leiste, text="", fg="#C8A165", bg=self.skin["bg"],
                                 font=("Arial", 9), anchor=tk.W, justify=tk.LEFT, wraplength=900)

            def _neu(k=kennung, v=_var, lab=_vorschau):
                _text, _warn = self._werkstatt_vorschau(
                    k, self._menge_lesen(v, spieloekonomie.MENGEN_HOECHSTMENGE))
                lab.config(text=_text, fg="#FDBA74" if _warn else "#C8A165")

            tk.Label(_leiste, text="Stück:", fg="#C0C0C0", bg=self.skin["bg"],
                     font=("Arial", 9)).pack(side=tk.LEFT)
            self._mengen_feld(_leiste, _var, spieloekonomie.MENGEN_HOECHSTMENGE, _neu)
            _vorschau.pack(side=tk.LEFT, padx=6)
            for ware in werkstatt.waren_der_werkstatt(kennung):
                erfuellt, grund = self.state.ware_voraussetzung(ware)
                knopf = tk.Button(rahmen, text=ware,
                                  command=lambda w=ware, k=kennung: self._ware_herstellen_menge(
                                      w, self._menge_lesen(self._ware_menge_var(k),
                                                           spieloekonomie.MENGEN_HOECHSTMENGE)),
                                  bg="#3e2723" if erfuellt else "#4a4a4a",
                                  fg=self.skin["gold"] if erfuellt else "#9e9e9e")
                if not erfuellt:
                    knopf.config(state=tk.DISABLED)
                knopf.pack(side=tk.LEFT, padx=2)
            _neu()
            # F-04: JEDE Forschungsbedingung einzeln anzeigen (Register 68). Gezeigt werden nur
            # Waren, denen wirklich etwas fehlt — sonst waere die Ansicht eine Litanei.
            for ware in werkstatt.waren_der_werkstatt(kennung):
                bedingungen = self.state.ware_voraussetzungen(ware)
                if not bedingungen or all(b["erfuellt"] for b in bedingungen):
                    continue
                tk.Label(self.content,
                         text="    " + ware + ": " + " · ".join(
                             self._ware_bedingung_text(b) for b in bedingungen),
                         fg="#C8A165", bg=self.skin["bg"], font=("Arial", 9),
                         anchor=tk.W).pack(anchor=tk.W, padx=24)
            if schlange:
                tk.Label(self.content,
                         text="   " + werkstatt.fortschritt(schlange, self.state.spielsekunden)["text"],
                         fg="#C0C0C0", bg=self.skin["bg"]).pack(anchor=tk.W, padx=12)

    def _ware_menge_var(self, kennung: str):
        """Die Stueckzahl-Variable EINER Werkstatt (A-1) - einmal angelegt, dann wiederverwendet."""
        if not hasattr(self, "_ware_mengen"):
            self._ware_mengen = {}
        var = self._ware_mengen.get(kennung)
        if var is None:
            var = tk.StringVar(master=self.root, value="1")
            self._ware_mengen[kennung] = var
        return var

    def _werkstatt_vorschau(self, kennung: str, menge: int) -> tuple:
        """(Text, Warnung?) fuer die gewaehlte Stueckzahl einer Werkstatt - je Ware EINE Zahl.

        Die Zahlen kommen aus `spieloekonomie.ware_grenzen`, also derselben Rechenstelle, die der
        Start benutzt. Kein zweiter Rechenweg, keine geschaetzte Anzeige.
        """
        ort = self.state.aktive_siedlung()
        if ort is None:
            return "", False
        try:
            levels = self.state.forschungs_stufen()
        except (AttributeError, KeyError, TypeError):
            levels = {}
        teile = []
        warnung = False
        for ware in werkstatt.waren_der_werkstatt(kennung):
            try:
                grenzen = spieloekonomie.ware_grenzen(asdict(ort), ware, levels)
            except (ValueError, KeyError, TypeError):
                continue
            if grenzen.get("hindernis"):
                teile.append(f"{ware}: gesperrt")
                continue
            moeglich = int(grenzen.get("moeglich") or 0)
            teile.append(f"{ware} {moeglich}")
            if menge > moeglich:
                warnung = True
        if not teile:
            return "", False
        return (f"{menge} Stueck je Ware · bezahlbar jetzt: " + " · ".join(teile), warnung)

    def _ware_herstellen_menge(self, ware: str, menge: int) -> bool:
        """`menge` Stueck einer Ware in der Werkstatt DIESES Ortes herstellen - EIN Vorgang (A-1).

        Alles oder nichts: reicht das Lager nicht fuer die ganze Menge, bucht der Kern gar nichts
        ab und nennt die Grenze (`spieloekonomie.ware_start_menge`).
        """
        try:
            menge = int(menge)
        except (TypeError, ValueError):
            menge = 0
        if menge < 1:
            self._log("Stueckzahl 0: es wird nichts hergestellt. Bitte eine Zahl ab 1 waehlen.")
            return False
        ort = self.state.aktive_siedlung()
        if ort is None:
            self._log("Keine Siedlung — es gibt keine Werkstatt vor Ort.")
            return False
        _sperre = self._nahrungssperre(ort)
        if _sperre:
            self._log(_sperre)
            return False
        levels = self.state.forschungs_stufen()
        try:
            ergebnis = spieloekonomie.ware_start_menge(asdict(ort), ware, levels,
                                                       self.state.spielsekunden, menge)
        except ValueError as fehler:
            meldung = f"{ware} nicht moeglich: {fehler}"
            self._log(meldung)
            self.state.messages.append({"text": meldung, "type": "werkstatt"})
            self._render_view()
            return False
        self.state._ort_uebernehmen(ort.id, ergebnis["ort"])
        meldung = f"{ergebnis['anzahl']} × {ware} in der Werkstatt von {ort.name} in Arbeit."
        self._log(meldung)
        self.state.messages.append({"text": meldung, "type": "werkstatt"})
        self._render_view()
        return True

    def _ware_herstellen(self, ware: str):
        """Ein Stueck einer Ware herstellen — die Mengenfassung mit Menge 1 (A-1).

        Oekonomie-Paket, Schritt 9, Teil 6c (Entwurf Z. 779: „Herstellung gegen gewaehlten Ort").
        Der Kern prueft: freigegebenes Rezept, Forschungsvoraussetzungen der Ware, **Werkstatt VOR
        ORT** und die **Materialkosten im lokalen Lager**. Abgelehnt wird VOR jeder Aenderung —
        gearbeitet wird auf einer Kopie, uebernommen erst nach Erfolg. Fertig wird die Ware in
        `ort_tick`, und zwar im **Ortslager** (genau einmal).

        Die fruehere reichsweite Warteschlange (`werkstatt_schlangen`) ist damit fuer die
        Herstellung weg: sie hatte EINE Schlange fuer alle Siedlungen und buchte die Ware in den
        GLOBALEN Bestand — die Ware konnte so in einer Stadt entstehen und in einer anderen liegen.
        """
        return self._ware_herstellen_menge(ware, 1)

    @staticmethod
    def _ware_bedingung_text(bedingung: dict) -> str:
        """Eine Forschungsbedingung einer Ware in Worten — erfuellt oder offen (F-04)."""
        if not bedingung["bekannt"]:
            return f"{bedingung['gebiet']} Stufe {bedingung['noetig']}: Forschung unbekannt"
        if bedingung["erfuellt"]:
            return (f"{bedingung['gebiet']} Stufe {bedingung['noetig']}: "
                    f"erfuellt ({bedingung['vorhanden']})")
        return (f"{bedingung['gebiet']} Stufe {bedingung['noetig']}: offen "
                f"({bedingung['vorhanden']} von {bedingung['noetig']})")

    def _render_profiles(self):
        tk.Label(self.content, text="Spielerprofile", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        tk.Label(self.content, text="Erstelle ein Profil über dich oder deinen Charakter.", fg="#C0C0C0", bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)
        tk.Entry(self.content, bg=self.skin["panel"], fg=self.skin["text"], insertbackground="#F5F5DC").pack(anchor=tk.W, padx=10, pady=10)
        tk.Button(self.content, text="Profil speichern", bg="#3e2723", fg=self.skin["gold"], command=self._save_profile).pack(anchor=tk.W, padx=10, pady=5)
        self.lbl_profile = tk.Label(self.content, text="Kein Profil gespeichert.", fg="#DAA520", bg=self.skin["bg"])
        self.lbl_profile.pack(anchor=tk.W, padx=10, pady=5)

    def _save_profile(self):
        self._log("Profil gespeichert. Noch ohne dauerhafte Speicherung.")

    # ---------- Weltkarte (astra-Bildgutachten 05.10.2026, Abschnitt A3) ----------
    #
    # astra wörtlich: „Die Karte ist ein grelles Farbmosaik ohne lesbare räumliche Struktur",
    # „Es fehlen Standort, Auswahl und verständlicher Klickzweck", „Kartenwechsel und
    # Zugangsvoraussetzungen verschwinden am unteren Rand". Umgebaut wurde: eine Zeichenfläche mit
    # 48 px je Feld in EIGENEN Scrollbalken, Zoomstufen („−  100 %  +"), die Gebietsleiste OBEN,
    # eine kleine Übersichtskarte oben rechts, ein festes Detailpanel rechts — und ein einfacher
    # Klick wählt nur aus (vorher erforschte und erledigte er still Nebenwirkungen).

    def _welt_gebiet_status(self, map_id: str) -> str:
        """hier / aktiv / freigeschaltet / gesperrt — dieselbe Einteilung wie in den Spieldaten."""
        if map_id == self.state.current_map:
            return "hier"
        if map_id in self.state.active_maps:
            return "aktiv"
        if map_id in self.state.unlocked_maps:
            return "freigeschaltet"
        return "gesperrt"

    def _welt_gebiet_name(self, map_id: str) -> str:
        cfg = next((m for m in MAPS if m["id"] == map_id), None)
        return str(cfg["name"]) if cfg else str(map_id)

    def _welt_gebiet_beschriftung(self, map_id: str) -> str:
        """Der Text im Gebietsmenü — gesperrte Gebiete ausdrücklich benannt (astra A3)."""
        status = self._welt_gebiet_status(map_id)
        name = self._welt_gebiet_name(map_id)
        if status == "hier":
            return f"{name} (hier)"
        if status == "aktiv":
            return name
        if status == "freigeschaltet":
            return f"{name} – nicht betreten"
        return f"{name} – gesperrt"

    def _welt_gebiet_wechseln(self, beschriftung: str):
        for m in MAPS:
            if self._welt_gebiet_beschriftung(m["id"]) == beschriftung:
                self.welt_gebiet = m["id"]
                self.welt_auswahl = None
                self._render_view()
                return

    def _welt_koordinate(self, x: int, y: int) -> str:
        """A1, G12 — dieselbe Schreibweise wie auf der Siedlungskarte."""
        return f"{self._spaltenname(int(x))}{int(y) + 1}"

    def _welt_zoom_prozent(self) -> int:
        zelle = float(getattr(self, "welt_zelle", WELT_ZOOM_STANDARD))
        return int(round(100.0 * zelle / WELT_ZOOM_STANDARD))

    def _welt_zoom(self, richtung: int):
        """Eine Zoomstufe weiter/zurück; die Mitte der Ansicht bleibt stehen (astra A3)."""
        stufen = list(WELT_ZOOM_STUFEN)
        aktuell = int(getattr(self, "welt_zelle", WELT_ZOOM_STANDARD))
        i = stufen.index(aktuell) if aktuell in stufen else stufen.index(WELT_ZOOM_STANDARD)
        neu = stufen[max(0, min(len(stufen) - 1, i + richtung))]
        if neu == aktuell:
            return
        c = getattr(self, "map_canvas", None)
        mitte = (0.5, 0.5)
        if c is not None and c.winfo_exists():
            alt = max(1.0, self._map_size * aktuell)
            mitte = (c.canvasx(max(1, c.winfo_width()) / 2.0) / alt,
                     c.canvasy(max(1, c.winfo_height()) / 2.0) / alt)
        self.welt_zelle = neu
        self._draw_map()
        beschriftung = getattr(self, "welt_zoom_label", None)
        if beschriftung is not None:
            beschriftung.config(text=f"{self._welt_zoom_prozent()} %")
        if c is not None and c.winfo_exists():
            neu_gesamt = max(1.0, self._map_size * neu)
            c.xview_moveto(max(0.0, min(1.0, mitte[0] - (c.winfo_width() / 2.0) / neu_gesamt)))
            c.yview_moveto(max(0.0, min(1.0, mitte[1] - (c.winfo_height() / 2.0) / neu_gesamt)))
            self._welt_uebersicht_update()

    def _welt_rad(self, ereignis):
        """Mausrad über der Karte scrollt die KARTE, nicht die Seite."""
        c = getattr(self, "map_canvas", None)
        if c is None or not c.winfo_exists():
            return
        c.yview_scroll(int(-ereignis.delta / 120), "units")
        self._welt_uebersicht_update()

    def _welt_mitte(self, x: int, y: int):
        """Die Ansicht auf ein Feld ziehen (für „Zum aktuellen Ort")."""
        c = getattr(self, "map_canvas", None)
        if c is None or not c.winfo_exists():
            return
        gesamt = max(1.0, int(self._map_size or 20) * int(self.welt_zelle))
        bw = float(c.winfo_width() if c.winfo_width() > 10 else 640)
        bh = float(c.winfo_height() if c.winfo_height() > 10 else 470)
        zx = (x + 0.5) * self.welt_zelle - bw / 2.0
        zy = (y + 0.5) * self.welt_zelle - bh / 2.0
        c.xview_moveto(max(0.0, min(1.0, zx / gesamt)))
        c.yview_moveto(max(0.0, min(1.0, zy / gesamt)))
        self._welt_uebersicht_update()

    def _welt_aktueller_ort(self):
        """Der eigene Ort auf der gezeigten Karte (oder None)."""
        return next((s for s in self.state.settlements if s.map_id == self.state.current_map), None)

    def _welt_zum_aktuellen_ort(self):
        ort = self._welt_aktueller_ort()
        if ort is None:
            self._log("Noch kein eigener Ort auf dieser Karte.")
            return
        self.welt_auswahl = (int(ort.x), int(ort.y))
        self._welt_detail_zeichnen()
        self._draw_map()
        self._welt_mitte(int(ort.x), int(ort.y))

    def _welt_uebersicht_update(self):
        """Den SICHTBAREN Ausschnitt als Rechteck in der kleinen Übersichtskarte zeigen."""
        klein = getattr(self, "welt_uebersicht", None)
        rahmen = getattr(self, "_welt_uebersicht_rahmen", None)
        c = getattr(self, "map_canvas", None)
        if klein is None or rahmen is None or c is None:
            return
        try:
            if not klein.winfo_exists() or not c.winfo_exists():
                return
            kante = self._welt_uebersicht_kante()
            gesamt = max(1.0, int(self._map_size or 20) * int(self.welt_zelle))
            x0 = c.canvasx(0) / gesamt * kante
            y0 = c.canvasy(0) / gesamt * kante
            x1 = c.canvasx(max(1, c.winfo_width())) / gesamt * kante
            y1 = c.canvasy(max(1, c.winfo_height())) / gesamt * kante
            klein.coords(rahmen, x0, y0, max(2.0, min(kante, x1)), max(2.0, min(kante, y1)))
            klein.tag_raise(rahmen)
        except Exception:
            pass

    def _welt_uebersicht_kante(self) -> float:
        """Kantenlänge der Übersichtskarte in px (astra Welt 3: „4 × 4 px je Weltfeld").

        Die Zahl kommt aus dem Feinmodul (``WELT3_UEBERSICHT_KACHEL``) und wächst mit dem Raster
        — 20 Felder ergeben 80 px. Vorher war die Übersicht fest 132 px breit, also 6,6 px je
        Feld, und der Sichtrahmen rechnete gegen die Fensterbreite statt gegen die Kachelzahl.
        """
        return float(welt_optik_fein.WELT3_UEBERSICHT_KACHEL * max(1, int(self._map_size or 20)))

    def _welt_uebersicht_zeichnen(self):
        """Die kleine Übersichtskarte (Geländefarben, eigener Ort, aktuelles Feld).

        astra Welt 3: „Übersicht oben rechts mit 4 × 4 px je Weltfeld, ohne Geländeornamente";
        der Sichtausschnitt trägt einen weißen 1-px-Rahmen #F2EEDB. Beides kommt aus
        `src/welt_optik_fein.py` — die Kachelzahl folgt dem Bild (`_welt_uebersicht_kante`).
        """
        klein = getattr(self, "welt_uebersicht", None)
        if klein is None or not klein.winfo_exists():
            return
        klein.delete("all")
        self._welt_uebersicht_rahmen = None
        kante = self._welt_uebersicht_kante()
        if self.welt_gebiet != self.state.current_map or not self.state.map_tiles:
            klein.create_text(kante / 2.0, kante / 2.0, text="nicht betreten", fill="#8A94A0",
                              font=("TkDefaultFont", 8))
            return
        gitter = max(1, int(self._map_size or 20))
        orte = [(int(s.x), int(s.y)) for s in self.state.settlements
                if s.map_id == self.state.current_map]
        # Die Uebersicht zeichnet der Plan aus `src/welt_optik_fein.py` (400 Kacheln + Ortspunkte +
        # Auswahlmarkierung); die Ausschnittsmarke darueber legt `_welt_uebersicht_update` nach.
        welt_optik.zeichne(klein, welt_optik_fein.uebersicht_plan_fein(
            self.state.map_tiles, kante, gitter, orte=orte, auswahl=self.welt_auswahl))
        self._welt_uebersicht_rahmen = klein.create_rectangle(
            0, 0, 0, 0, outline=welt_optik_fein.WELT3_SICHT_RAHMEN,
            width=welt_optik_fein.WELT3_SICHT_RAHMEN_BREITE)
        self._welt_uebersicht_update()

    def _welt_legende(self, eltern):
        """Legende als eigene Beschriftungen — Gelände, Ortszeichen und der eigene Ort."""
        legende = tk.Frame(eltern, bg=self.skin["panel"])
        legende.pack(fill=tk.X, padx=6, pady=(8, 0))
        tk.Label(legende, text="Legende", fg=self.skin["gold"], bg=self.skin["panel"],
                 font=("TkDefaultFont", 10, "bold")).pack(anchor=tk.W)
        for art in WELT_GELAENDEREIHENFOLGE:
            zeile = tk.Frame(legende, bg=self.skin["panel"])
            zeile.pack(anchor=tk.W, fill=tk.X)
            tk.Label(zeile, text="      ", bg=WELT_GELAENDEFARBEN[art]).pack(side=tk.LEFT, padx=(0, 4))
            tk.Label(zeile, text=WELT_GELAENDENAMEN[art], fg="#E6E9EE",
                     bg=self.skin["panel"]).pack(side=tk.LEFT)
        tk.Label(legende, text="●  Vorkommen (Rohstoffe — kein Gebäude)", fg="#E6E9EE",
                 bg=self.skin["panel"]).pack(anchor=tk.W, pady=(4, 0))
        tk.Label(legende, text="▁  Lager eines fremden Volkes", fg="#E6E9EE",
                 bg=self.skin["panel"]).pack(anchor=tk.W)
        tk.Label(legende, text="▨  Ruine (Ort mit Aufgabe)", fg="#E6E9EE",
                 bg=self.skin["panel"]).pack(anchor=tk.W)
        tk.Label(legende, text="⚑  Hier — deine Siedlung", fg="#E6E9EE",
                 bg=self.skin["panel"]).pack(anchor=tk.W)

    def _welt_gebiet_panel(self, eltern, map_id: str):
        """Was rechts vom Gebietsmenü steht, wenn dieses Gebiet nicht die eigene Karte ist."""
        status = self._welt_gebiet_status(map_id)
        name = self._welt_gebiet_name(map_id)
        rahmen = tk.Frame(eltern, bg=self.skin["panel"])
        rahmen.pack(fill=tk.BOTH, expand=True, padx=18, pady=18)
        if status == "gesperrt":
            tk.Label(rahmen, text=f"{name} ist gesperrt.", fg=self.skin["gold"],
                     bg=self.skin["panel"], font=("TkDefaultFont", 13, "bold")).pack(anchor=tk.W)
            # Teil 8 (Entwurf Z. 785): hier stand die Zusage "Zugang: die Forschung „Vermessung“
            # auf Stufe 1". Diese Forschung gibt es unter den 21 Originalforschungen NICHT — die
            # Zusage war also nie erfuellbar. An ihrer Stelle steht jetzt die Wahrheit: die fuenf
            # Weltregionen sind das ALTE Kartensystem, und neue Spielkarten kommen ueber den
            # Kartenvorrat bei der Gruendung (Wagenbau + Siedlerkarren) — die Regionen selbst sind
            # KEINE Siedlungskarten.
            tk.Label(rahmen, text="Dieses Gebiet gehört zum alten Weltkartensystem und wird im "
                                  "Remake nicht freigeschaltet: die Forschung „Vermessung“ gibt "
                                  "es unter den 21 Originalforschungen nicht (Original und "
                                  "Handbuch kennen sie nicht). Neue Spielkarten kommen über den "
                                  "Kartenvorrat bei der Gründung (Wagenbau + Siedlerkarren); die "
                                  "fünf Weltregionen sind keine Siedlungskarten.",
                     fg=self.skin["text"], bg=self.skin["panel"], wraplength=560,
                     justify=tk.LEFT).pack(anchor=tk.W, pady=(2, 10))
            tk.Button(rahmen, text="Zum Portal", command=lambda: self._switch_view("Portal"),
                      bg=self.skin["button"], fg=self.skin["gold"]).pack(anchor=tk.W, pady=2)
            tk.Button(rahmen, text="Zur Forschung", command=lambda: self._switch_view("Forschung"),
                      bg=self.skin["button"], fg=self.skin["gold"]).pack(anchor=tk.W, pady=2)
            return
        tk.Label(rahmen, text=f"{name} — noch nicht betreten.", fg=self.skin["gold"],
                 bg=self.skin["panel"], font=("TkDefaultFont", 13, "bold")).pack(anchor=tk.W)
        besatzung = sum(self.state.map_garrison.get(map_id, {}).values())
        tk.Label(rahmen, text=f"Besatzung: {besatzung} Einheiten.", fg=self.skin["text"],
                 bg=self.skin["panel"]).pack(anchor=tk.W, pady=(2, 10))
        if map_id in self.state.active_maps:
            tk.Button(rahmen, text=f"Betreten ({self.state.map_switch_cost} Gold)",
                      command=lambda mid=map_id: self._enter_map(mid), bg=self.skin["button"],
                      fg=self.skin["gold"]).pack(anchor=tk.W, pady=2)
            # astra A3 verlangt „Stationieren" nur im Detailbereich eines AUSGEWÄHLTEN Ortes.
            # Hier steht bewusst ein anderer Fall: das ganze Gebiet ist noch nicht betreten, es
            # gibt dort also nichts auszuwählen — der Knopf sagt deshalb ausdrücklich, wohin die
            # Truppen gehen (Prüfbericht des Unteragenten vom 05.10.2026, 11:29).
            tk.Button(rahmen, text="Einheiten auf dieses Gebiet stationieren",
                      command=lambda mid=map_id: self._station_on_map(mid),
                      bg=self.skin["button"], fg=self.skin["gold"]).pack(anchor=tk.W, pady=2)
            if map_id != "kontinent":
                # Entscheidung 1 (01.11.2026): auch der Kartenangriff REIST. Der Knopf sagt das
                # jetzt - vorher hiess er "Angreifen" und war sofort fertig.
                tk.Button(rahmen, text="Angriff entsenden (reist)",
                          command=lambda mid=map_id: self._attack_map(mid),
                          bg=self.skin["button"], fg=self.skin["red"]).pack(anchor=tk.W, pady=2)
                tk.Button(rahmen, text="Karte zerstören",
                          command=lambda mid=map_id: self._destroy_map(mid),
                          bg=self.skin["button"], fg=self.skin["red"]).pack(anchor=tk.W, pady=2)
        else:
            tk.Label(rahmen, text="Freigeschaltet, aber noch nicht betreten — der Wechsel "
                                  "kostet Gold.", fg=self.skin["text"], bg=self.skin["panel"],
                     wraplength=560, justify=tk.LEFT).pack(anchor=tk.W)

    def _render_maps(self):
        """STILLGELEGT am 01.11.2026 (Schnitt S-2, Daniel M-10) - nicht mehr im Menue verdrahtet.

        Das war die alte Weltkarte "Weltkarte - Orte entdecken" mit ihren sieben Gebieten aus
        `MAPS`. Daniel: "Die Weltkarte soll weg es wird hier nur noch Platz sein fuer das
        Dorfzentrum Lager und dessen verwaltung und uebersichten" (docs/KONZEPT_SECHS_DOERFER_20261101.md,
        Anhang 1 Abschnitt 2). Die Aufgabe uebernimmt das Portal: dort steht ab S-5 das
        Geländekaestchen der aktuellen Weltkarte, Felder anwaehlbar.

        Der Rumpf bleibt als Beleg stehen, bis das Portal ihn vollstaendig ersetzt; die Methode ist
        ueber keinen Menuepunkt mehr erreichbar (Wache: `tests/test_weltkarten_anzeige.py`).
        """
        tk.Label(self.content, text="Weltkarte – Orte entdecken",
                 font=("Blackletter", 20, "bold"), fg=self.skin["gold"],
                 bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 2))
        tk.Label(self.content, text="Hier erkundest du die Welt. Gebäude, die Rohstoffe liefern, "
                                    "baust du NICHT hier, sondern auf der Karte deiner Siedlung "
                                    "(Dorfzentrum → „Karte öffnen“). Ein Klick wählt ein Feld aus — "
                                    "was dort liegt, steht rechts.",
                 fg="#F3F4F6", bg=self.skin["bg"], wraplength=940,
                 justify=tk.LEFT).pack(anchor=tk.W, padx=10)

        if not hasattr(self, "welt_gebiet") or self.welt_gebiet not in [m["id"] for m in MAPS]:
            self.welt_gebiet = self.state.current_map
        if not hasattr(self, "welt_zelle"):
            self.welt_zelle = WELT_ZOOM_STANDARD
        if not hasattr(self, "welt_auswahl"):
            self.welt_auswahl = None
        if not hasattr(self, "_show_buildings"):
            self._show_buildings = True
        if not hasattr(self, "_welt_start"):
            self._welt_start = None
        self._map_size = next(m for m in MAPS if m["id"] == self.state.current_map)["size"]

        # --- Gebietsleiste OBEN (astra A3: der Kartenwechsel gehört nicht unter die Karte) ---
        leiste = tk.Frame(self.content, bg=self.skin["panel"])
        leiste.pack(fill=tk.X, padx=10, pady=(6, 2))
        tk.Label(leiste, text="Gebiet:", fg=self.skin["gold"], bg=self.skin["panel"],
                 font=("TkDefaultFont", 10, "bold")).pack(side=tk.LEFT, padx=(6, 2))
        werte = [self._welt_gebiet_beschriftung(m["id"]) for m in MAPS]
        self.welt_gebiet_var = tk.StringVar(value=self._welt_gebiet_beschriftung(self.welt_gebiet))
        self.welt_gebiet_menu = tk.OptionMenu(leiste, self.welt_gebiet_var, *werte,
                                             command=self._welt_gebiet_wechseln)
        self.welt_gebiet_menu.config(bg=self.skin["button"], fg=self.skin["gold"],
                                     activebackground="#5D4037", highlightthickness=0,
                                     font=("TkDefaultFont", 10))
        try:
            self.welt_gebiet_menu["menu"].config(bg=self.skin["panel"], fg=self.skin["text"])
        except Exception:
            pass
        self.welt_gebiet_menu.pack(side=tk.LEFT)
        tk.Button(leiste, text="Zum aktuellen Ort", command=self._welt_zum_aktuellen_ort,
                  bg=self.skin["button"], fg=self.skin["gold"]).pack(side=tk.LEFT, padx=8)

        # --- Zoomstufen („−  100 %  +", astra A3) ---
        tk.Label(leiste, text="Zoom:", fg=self.skin["text"], bg=self.skin["panel"]).pack(
            side=tk.LEFT, padx=(14, 2))
        tk.Button(leiste, text="−", width=2, command=lambda: self._welt_zoom(-1),
                  bg=self.skin["button"], fg=self.skin["gold"]).pack(side=tk.LEFT)
        self.welt_zoom_label = tk.Label(leiste, text=f"{self._welt_zoom_prozent()} %",
                                        fg=self.skin["text"], bg=self.skin["panel"], width=6)
        self.welt_zoom_label.pack(side=tk.LEFT)
        tk.Button(leiste, text="+", width=2, command=lambda: self._welt_zoom(1),
                  bg=self.skin["button"], fg=self.skin["gold"]).pack(side=tk.LEFT)
        tk.Button(leiste, text="Ortszeichen ausblenden", command=self._toggle_buildings,
                  bg=self.skin["button"], fg=self.skin["gold"]).pack(side=tk.RIGHT, padx=6)

        # --- Hauptbereich: links die Zeichenfläche, rechts Übersicht + Legende + Detailpanel ---
        haupt = tk.Frame(self.content, bg=self.skin["bg"])
        haupt.pack(fill=tk.BOTH, expand=True, padx=10, pady=(4, 10))
        # astra Welt 3: „Rechtes Detailpanel fest etwa 248 px breit, 12 px Innenabstand, Schrift
        # etwa 14 px, Titel 18 px" — die Maße kommen aus src/welt_optik_fein.py (detail_masse).
        self._panel_masse = welt_optik_fein.detail_masse()
        _panelbreite = int(self._panel_masse["breite"])
        links = tk.Frame(haupt, bg=self.skin["panel"])
        links.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        rechts = tk.Frame(haupt, bg=self.skin["panel"], width=_panelbreite)
        rechts.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        rechts.pack_propagate(False)

        if self.welt_gebiet != self.state.current_map:
            self.map_canvas = None
            self._welt_gebiet_panel(links, self.welt_gebiet)
        else:
            self._welt_zeichnen_aufbau(links)

        # Übersichtskarte oben rechts im Kartenbereich — Kantenlänge astra Welt 3: „4 × 4 px je
        # Weltfeld" (20 Felder = 80 px), nicht mehr die feste Fensterbreite 132.
        _uebersicht_kante = int(self._welt_uebersicht_kante())
        tk.Label(rechts, text="Übersicht", fg=self.skin["gold"], bg=self.skin["panel"]).pack(
            anchor=tk.W, padx=6)
        self.welt_uebersicht = tk.Canvas(rechts, width=_uebersicht_kante,
                                         height=_uebersicht_kante, bg="#0F1418",
                                         highlightthickness=1, highlightbackground="#3A4550")
        self.welt_uebersicht.pack(anchor=tk.W, padx=6, pady=(2, 0))
        self._welt_uebersicht_zeichnen()

        self._welt_legende(rechts)

        # Festes Detailpanel (astra A3: „[Ortsname] · G12 / Gelände / Status / Gebäude / Aktion")
        tk.Label(rechts, text="Ausgewählter Ort", fg=self.skin["gold"], bg=self.skin["panel"]).pack(
            anchor=tk.W, padx=6, pady=(10, 0))
        self.welt_detail = tk.Frame(rechts, bg=self.skin["panel"], bd=1, relief=tk.GROOVE)
        self.welt_detail.pack(fill=tk.X, padx=6, pady=(2, 6))
        self._welt_detail_zeichnen()

    def _welt_zeichnen_aufbau(self, eltern):
        """Die eigentliche Zeichenfläche samt eigener waagerechter und senkrechter Scrollbalken."""
        self.map_canvas = tk.Canvas(eltern, width=720, height=480, bg="#0F1418",
                                    highlightthickness=0)
        xsb = tk.Scrollbar(eltern, orient=tk.HORIZONTAL,
                           command=lambda *a: (self.map_canvas.xview(*a),
                                               self._welt_uebersicht_update()))
        ysb = tk.Scrollbar(eltern, orient=tk.VERTICAL,
                           command=lambda *a: (self.map_canvas.yview(*a),
                                               self._welt_uebersicht_update()))
        self.map_canvas.config(xscrollcommand=xsb.set, yscrollcommand=ysb.set)
        self.welt_xsb, self.welt_ysb = xsb, ysb
        ysb.pack(side=tk.RIGHT, fill=tk.Y)
        xsb.pack(side=tk.BOTTOM, fill=tk.X)
        # FESTE Groesse, nicht expandierend: sonst waechst die Zeichenflaeche auf die Fensterbreite
        # und bei 48 px passt die ganze Karte hinein — die Scrollbalken waeren ohne Wirkung
        # (astra A3: „Die gesamte Karte muss nicht gleichzeitig ins Fenster passen").
        self.map_canvas.pack(side=tk.LEFT)
        self.map_canvas.bind("<Button-1>", self._on_map_click)
        self.map_canvas.bind("<MouseWheel>", self._welt_rad)
        self.map_canvas.bind("<Configure>", lambda _e: self._welt_uebersicht_update())
        self._draw_map()

    def _welt_ort_name(self, tile) -> str:
        """Eindeutiger Ortsname NUR an echten Orten (astra A3: kein Namensrauschen)."""
        eigene = next((s for s in self.state.settlements
                       if s.map_id == self.state.current_map
                       and int(s.x) == int(tile.x) and int(s.y) == int(tile.y)), None)
        if eigene is not None:
            return str(eigene.name)[:16]
        if tile.npc_faction:
            return str(tile.npc_faction)[:16]
        if tile.quest and not tile.quest_done:
            return str(tile.quest)[:18]
        return ""

    def _welt_auswahl_daten(self):
        """Alle Angaben zum ausgewählten Feld für das Detailpanel (eine Quelle)."""
        auswahl = getattr(self, "welt_auswahl", None)
        if not auswahl or self.welt_gebiet != self.state.current_map:
            return None
        x, y = int(auswahl[0]), int(auswahl[1])
        tile = self.state.get_tile(x, y, self._map_size)
        if tile is None:
            return None
        eigene = next((s for s in self.state.settlements
                       if s.map_id == self.state.current_map
                       and int(s.x) == x and int(s.y) == y), None)
        if eigene is not None:
            name = str(eigene.name)
            gebaut = len(getattr(eigene, "bauten", {}) or {})
            inhalt, inhalt_label = (f"{gebaut} Gebäude" if gebaut else "keine"), "Gebäude"
            status = "Eigene Siedlung"
        else:
            name = self._welt_ort_name(tile) or "Unbenannter Ort"
            status = "Unpassierbar (Wasser)" if tile.terrain == "water" else (
                "Zugänglich" if tile.discovered else "Unbetreten")
            stoffe = ", ".join(f"{k} {int(v)}" for k, v in (tile.resources or {}).items())
            # astra (05.10.2026): „Rohstoffvorkommen nicht als Gebäude bezeichnen" — ein
            # Vorkommen ist kein Bauwerk, es steht deshalb unter „Vorkommen".
            inhalt = stoffe if stoffe else "keine"
            inhalt_label = "Vorkommen" if stoffe else "Gebäude"
        return {"x": x, "y": y, "tile": tile, "eigene": eigene, "name": name,
                "koordinate": self._welt_koordinate(x, y),
                "gelaende": WELT_GELAENDENAMEN.get(tile.terrain, str(tile.terrain)),
                "status": status, "gebaeude": inhalt, "gebaeude_label": inhalt_label}

    def _welt_detail_zeichnen(self):
        """Das feste Detailpanel rechts — Ort, Gelände, Status, Gebäude, Aktion."""
        rahmen = getattr(self, "welt_detail", None)
        if rahmen is None:
            return
        try:
            if not rahmen.winfo_exists():
                return
        except Exception:
            return
        for kind in rahmen.winfo_children():
            kind.destroy()
        # astra Welt 3: „12 px Innenabstand" — die Textbreite bleibt INNERHALB des 248-px-Panels,
        # sonst schneidet der Rahmen die Zeilen ab (pack_propagate(False) auf der rechten Spalte).
        _masse = getattr(self, "_panel_masse", None) or welt_optik_fein.detail_masse()
        _umbruch = int(_masse["breite"]) - 2 * int(_masse["innenabstand"])
        daten = self._welt_auswahl_daten()
        if daten is None:
            tk.Label(rahmen, text="Ein Feld auf der Karte anklicken.", fg=self.skin["text"],
                     bg=self.skin["panel"], wraplength=_umbruch, justify=tk.LEFT).pack(
                anchor=tk.W, padx=6, pady=6)
            return
        tk.Label(rahmen, text=f"{daten['name']} · {daten['koordinate']}", fg=self.skin["gold"],
                 bg=self.skin["panel"], font=("TkDefaultFont", 11, "bold"),
                 wraplength=_umbruch, justify=tk.LEFT).pack(anchor=tk.W, padx=6, pady=(6, 2))
        for zeile in (f"Gelände: {daten['gelaende']}",
                      f"Status: {daten['status']}",
                      f"{daten['gebaeude_label']}: {daten['gebaeude']}"):
            tk.Label(rahmen, text=zeile, fg=self.skin["text"], bg=self.skin["panel"],
                     wraplength=_umbruch, justify=tk.LEFT).pack(anchor=tk.W, padx=6)
        eigene = daten["eigene"]
        tile = daten["tile"]
        if eigene is not None:
            tk.Button(rahmen, text="Siedlung öffnen",
                      command=lambda s=eigene: self._oeffne_siedlungskarte(s),
                      bg="#2563EB", fg="#FFFFFF").pack(anchor=tk.W, padx=6, pady=(6, 2))
        elif tile.quest and not tile.quest_done:
            tk.Button(rahmen, text="Ort erkunden",
                      command=lambda x=daten["x"], y=daten["y"]: self._welt_ort_erkunden(x, y),
                      bg=self.skin["button"], fg=self.skin["gold"]).pack(anchor=tk.W, padx=6, pady=(6, 2))
        elif tile.terrain != "water" and not tile.discovered:
            tk.Button(rahmen, text="Ort erkunden",
                      command=lambda x=daten["x"], y=daten["y"]: self._welt_ort_erkunden(x, y),
                      bg=self.skin["button"], fg=self.skin["gold"]).pack(anchor=tk.W, padx=6, pady=(6, 2))
        if self.state.current_map in self.state.active_maps and \
                sum(self.state.units[u].count for u in self.state.units) > 0:
            tk.Button(rahmen, text="Einheiten stationieren",
                      command=lambda: self._station_on_map(self.state.current_map),
                      bg=self.skin["button"], fg=self.skin["gold"]).pack(anchor=tk.W, padx=6, pady=2)
        start = getattr(self, "_welt_start", None)
        if start is None:
            if sum(self.state.units[u].count for u in self.state.units) > 0:
                tk.Button(rahmen, text="Truppen von hier bewegen",
                          command=lambda: self._welt_bewegung_starten(),
                          bg=self.skin["button"], fg=self.skin["gold"]).pack(anchor=tk.W, padx=6, pady=2)
        else:
            tk.Label(rahmen, text=f"Start {self._welt_koordinate(start[0], start[1])}: jetzt ein "
                                  f"Nachbarfeld anklicken.", fg="#FDBA74", bg=self.skin["panel"],
                     wraplength=_umbruch, justify=tk.LEFT).pack(anchor=tk.W, padx=6, pady=(4, 0))
            tk.Button(rahmen, text="Abbrechen", command=self._welt_bewegung_abbrechen,
                      bg=self.skin["button"], fg=self.skin["text"]).pack(anchor=tk.W, padx=6, pady=2)
    def _enter_map(self, map_id: str):
        self._activate_map(map_id)
        self._render_view()

    def _destroy_map(self, map_id: str):
        self.state.destroy_map(map_id)
        self._render_view()

    def _toggle_buildings(self):
        self._show_buildings = not getattr(self, "_show_buildings", True)
        self._draw_map()

    def _draw_map(self, size: int = None):
        """Zeichnet die Weltkarte auf die Zeichenfläche (astra A3: feste Zellgröße, Scrollbereich).

        ``size`` bleibt als Parameter erhalten, weil der Zeitlauf die Methode aufruft; die
        maßgebliche Größe ist die aktuelle Karte (``self._map_size``).
        """
        if self.welt_gebiet != self.state.current_map:
            return
        canvas = getattr(self, "map_canvas", None)
        if canvas is None:
            return
        try:
            if not canvas.winfo_exists():
                return
        except Exception:
            return
        canvas.delete("all")
        gitter = max(1, int(self._map_size or size or 20))
        zelle = int(getattr(self, "welt_zelle", WELT_ZOOM_STANDARD))
        canvas.config(scrollregion=(0, 0, gitter * zelle, gitter * zelle))
        # Nachbararten vorab aus den Feldern (fuer Innenkanten und Ufersaeume, astra Welt 1).
        gelaende_von = {(int(t.x), int(t.y)): t.terrain for t in self.state.map_tiles}

        def _nachbar_gelaende(x: int, y: int) -> dict:
            """Nachbararten des Weltfeldes (x, y) fuer Innenkanten und Ufersaeume."""
            arten: dict = {}
            for richtung, dx, dy in (("norden", 0, -1), ("sueden", 0, 1),
                                     ("westen", -1, 0), ("osten", 1, 0)):
                art = gelaende_von.get((x + dx, y + dy))
                if art is not None:
                    arten[richtung] = art
            return arten

        for tile in self.state.map_tiles:
            x1, y1 = tile.x * zelle, tile.y * zelle
            feldtag = f"weltfeld:{tile.x}:{tile.y}"
            # Feinere Landschaftsmalerei je Feld aus `src/welt_optik_fein.py` (zweite astra-
            # Auswertung, Kinder-Arbeit, nachgerechnet): Flaechenfarbe, 1-px-Rasterlinien nur zu
            # ungleichen Nachbarn, Ufersaum an Land-Wasser-Grenzen und die Gelaendeformen. Die
            # Detailstufe waehlt das Modul selbst (16/24 einfach, 32 reduziert, ab 48 voll), und
            # die Varianten kommen DETERMINISTISCH aus den Feldkoordinaten — nichts springt beim
            # Neuzeichnen.
            plan = welt_optik_fein.gelaende_plan_fein(
                tile.terrain, x1, y1, zelle, feld=(tile.x, tile.y),
                nachbarn=_nachbar_gelaende(int(tile.x), int(tile.y)))
            # Das erste Element ist die Gelaendeflaeche; NUR sie traegt das Sammel-Tag 'weltfeld'
            # — daran haengt die Pruefung „jedes Feld ist gezeichnet" (400 Objekte).
            welt_optik.zeichne(canvas, plan[:1], tags=(feldtag, "weltfeld"))
            if len(plan) > 1:
                welt_optik.zeichne(canvas, plan[1:], tags=(feldtag,))
        if zelle >= 24:
            # Regionsnamen einmal je Region in ~18 px mit 1 px versetztem dunklem Schatten
            # (astra Welt 2). Die Schatten tragen zusaetzlich 'weltschatten', damit die neun
            # NAMEN zaehlbar bleiben (tests/test_weltkarte.py).
            regionen = welt_optik_fein.regionen_plan_fein(gitter, float(zelle), anzahl=3)
            welt_optik.zeichne(canvas, [e for e in regionen if e.get("rolle") == "schatten"],
                               tags=("weltregion", "weltschatten"))
            welt_optik.zeichne(canvas, [e for e in regionen if e.get("rolle") != "schatten"],
                               tags=("weltregion", "weltname"))
        if getattr(self, "_show_buildings", True):
            orte = {(int(s.x), int(s.y)) for s in self.state.settlements
                    if s.map_id == self.state.current_map}
            for tile in self.state.map_tiles:
                if (int(tile.x), int(tile.y)) in orte:
                    continue
                x1, y1 = tile.x * zelle, tile.y * zelle
                if tile.npc_faction:
                    # Lager eines fremden Volkes: niedrige Einfriedung (astra Welt 2).
                    welt_optik.zeichne(
                        canvas, welt_optik_fein.ortsilhouette_plan("lager", x1, y1, zelle),
                        tags=("weltort", "weltlager"))
                elif tile.quest and not tile.quest_done:
                    # Ort mit Aufgabe: gebrochene Mauerlinie.
                    welt_optik.zeichne(
                        canvas, welt_optik_fein.ortsilhouette_plan("ruine", x1, y1, zelle),
                        tags=("weltort", "weltruine"))
                elif tile.resources:
                    # Ein Rohstoffvorkommen ist KEIN Gebaeude (astra Welt 3: „Rohstoffvorkommen
                    # nicht als Gebaeude bezeichnen") — es bekommt keinen Ortsbau, nur einen Punkt.
                    cx, cy = x1 + zelle / 2.0, y1 + zelle / 2.0
                    canvas.create_oval(cx - 4, cy - 4, cx + 4, cy + 4, fill="#F2C94C",
                                       outline="#17212B", tags=("weltort", "weltvorkommen"))
        # Der eigene Ort: weiße Fahne auf blauem Sockel, daneben „Hier" (astra A3)
        for s in self.state.settlements:
            if s.map_id != self.state.current_map:
                continue
            welt_optik.zeichne(canvas,
                               welt_optik_fein.fahne_plan_fein(s.x * zelle, s.y * zelle, zelle),
                               tags=("welthier",))
            canvas.create_text(s.x * zelle + zelle / 2.0, s.y * zelle + zelle * 0.95,
                               text="Hier", fill="#F3F4F6",
                               font=("TkDefaultFont", 8, "bold"), tags="welthier")
        if getattr(self, "welt_auswahl", None):
            ax, ay = int(self.welt_auswahl[0]), int(self.welt_auswahl[1])
            welt_optik.zeichne(canvas,
                               welt_optik_fein.auswahl_plan_fein(ax * zelle, ay * zelle, zelle),
                               tags=("welt_auswahl",))
        start = getattr(self, "_welt_start", None)
        if start:
            sx, sy = int(start[0]), int(start[1])
            canvas.create_rectangle(sx * zelle + 3, sy * zelle + 3,
                                    (sx + 1) * zelle - 3, (sy + 1) * zelle - 3,
                                    outline="#FDBA74", width=2, tags="weltstart")
        jetzt = float(self.state.spielsekunden)
        for m in self.state.movements[:]:
            rest = max(0, int(m["arrival"] - jetzt))
            if rest <= 0:
                continue
            stunden, rest = divmod(rest, 3600)
            minuten, sekunden = divmod(rest, 60)
            try:
                tx, ty = (int(t) for t in str(m["to"]).split(":"))
            except (TypeError, ValueError):
                continue
            cx, cy = tx * zelle + zelle / 2.0, ty * zelle + zelle / 2.0
            canvas.create_text(cx, cy, text=f"{stunden:02d}:{minuten:02d}:{sekunden:02d}",
                               fill="#FFD166", font=("TkDefaultFont", 8, "bold"))
        self._welt_uebersicht_zeichnen()
    # ---------- Angriff: kampf + kampfbericht (Umsetzungsplan, Abschnitte 1.3 und 2) ----------
    #
    # Vorher rechnete die Oberflaeche mit einer eigenen Daumenformel ("mehr Kampfkraft als der
    # Verteidiger") und erfand Beute. Jetzt laeuft JEDER Angriff durch denselben Ablauf:
    # Truppenpruefung -> Vorrunde/Wallschwellen -> bis zu zehn Kampfsequenzen -> Beute nach
    # Karrenladung -> Bericht in den Reiter "Nachrichten" -> Verluste und Beute in den Spielstand.

    def _reichsheer_legacy(self) -> Dict[str, int]:
        """Alter Stand OHNE Siedlung: der Reichsbestand ist dann die einzige Quelle (Uebergang).

        Nur fuer Spielstaende von vor der Ortswirtschaft. Sobald eine Siedlung existiert, gilt
        ausschliesslich ihr Ortsheer - sonst gaebe es wieder zwei Wahrheiten (F-01).
        """
        return {k: int(v.count) for k, v in self.state.units.items() if int(v.count) > 0}

    def _truppen_nach_rolle(self, ort=None):
        """Teilt das ORTSHEER einer Siedlung in die Rollen des Handbuchs (einheiten.py).

        F-01 der externen Spielpruefung (31.10.2026), am Code nachgemessen: hier stand
        `self.state.units` - der Reichsbestand. Lokal ausgebildete Truppen liegen aber im
        ORTSLAGER (`Settlement.einheiten`, gebucht von `spieloekonomie.ort_tick`), also griff
        KEIN Angriff auf sie zu. Der Reichsbestand ist reine Anzeige.

        `ort` ist die Siedlung, deren Heer gemeint ist (Vorgabe: die aktive Siedlung).
        """
        if ort is None:
            ort = self.state.aktive_siedlung()
        bestand = (self.state._ortsheer(ort) if ort is not None
                   else self._reichsheer_legacy())
        kaempfer, belagerung, karren = {}, {}, {}
        for kennung, anzahl in bestand.items():
            if int(anzahl) <= 0:
                continue
            rolle = einheiten.rolle(kennung)
            if rolle in ("kaempfer", "kundschafter"):
                kaempfer[kennung] = int(anzahl)
            elif rolle == "belagerung":
                belagerung[kennung] = int(anzahl)
            elif rolle == "karren":
                karren[kennung] = int(anzahl)
        return kaempfer, belagerung, karren

    def _vorraete_des_ziels(self, ziel) -> dict:
        """Die Vorraete des Angegriffenen.

        Fuehrt das Ziel eigene Vorraete (botkern-Bots tun das), gelten die. Sonst kommen die
        VORSCHLAG-Spannen aus `botkern` (dort ausdruecklich als Vorschlag gekennzeichnet, weil die
        Vorlage kein Startinventar nennt) - der Startwert haengt am Namen, damit derselbe Gegner
        immer dasselbe Lager hat.
        """
        eigene = getattr(ziel, "vorraete", None)
        if isinstance(eigene, dict) and eigene:
            return dict(eigene)
        if isinstance(ziel, dict) and ziel.get("vorraete"):
            return dict(ziel["vorraete"])
        name = getattr(ziel, "name", None) or (ziel.get("name") if isinstance(ziel, dict) else "") or ""
        rng = random.Random(f"nebel-vorraete-{name}")
        return {stoff: rng.randint(lo, hi)
                for stoff, (lo, hi) in botkern.VORSCHLAG_START_VORRAETE.items()}

    def _angriff_auftrag_starten(self, ziel_name: str, verteidiger: dict, wall_stufe: int = 0,
                                 wall_zustand: float = 100.0, vorraete=None,
                                 verteidiger_karren=None, vorrat_ziel=None,
                                 entfernung: float = None,
                                 truppen: Optional[dict] = None,
                                 dorf_name: str = "") -> bool:
        """DER EINE Angriffsweg: ein Auftrag mit Marsch (Entscheidung 1, Daniel 01.11.2026).

        Entscheidung 1 lautet: jeder Angriff REIST. Der Sofortpfad ohne Reisezeit ist damit
        stillgelegt - `_attack`, `_attack_map` und `_auftrag_angriff` starten alle hier einen
        Auftrag der Art "angreifen"; gekaempft wird erst bei Ankunft in `kampf_am_ziel`, gebucht
        wird die Heimkehr in `auftraege_fortschreiben`.

        Was das fuer den Spieler aendert: die Truppen sind waehrend des Marsches abgezogen (sie
        stehen im Auftrag, nicht mehr im Ortslager), es gibt eine Ankunft und eine Rueckkehr, und
        die Beute kommt mit den Ueberlebenden zurueck. Vorher war ein Angriff in derselben
        Sekunde fertig, in der man ihn befahl - ohne Marsch, ohne Gegenwehr, ohne Fenster, in dem
        der Angegriffene reagieren koennte.

        Quelle ist das ORTSHEER der aktiven Siedlung (`_truppen_nach_rolle`); ohne Siedlung
        greift der Uebergangsweg ueber den Reichsbestand - dieselbe Regel wie vorher.
        """
        ort = self.state.aktive_siedlung()
        if truppen is None:             # ohne Auswahl: das ganze Ortsheer (bisheriges Verhalten)
            kaempfer, belagerung, karren = self._truppen_nach_rolle(ort)
            if not kaempfer and not belagerung:
                # Belegter Wortlaut (spielschicht.py:525-526): ohne Schlagkraft kein Angriff.
                meldung = "Keine Kaempfer und keine Belagerungswaffen vorhanden."
                self.state.messages.append({"text": meldung, "type": "kampf"})
                self._log(meldung)
                return False
            truppen = dict(kaempfer)
            truppen.update(belagerung)
            truppen.update(karren)      # Transportkarren tragen die Beute (Handbuch S. 23)
        else:                           # B-5: die Auswahl aus dem Fenster gilt genau so, wie sie ist
            truppen = {str(n): int(a) for n, a in dict(truppen).items() if int(a) > 0}
            if not truppen:
                meldung = "Keine Einheiten ausgewaehlt."
                self.state.messages.append({"text": meldung, "type": "kampf"})
                self._log(meldung)
                return False

        ziel = {"name": str(ziel_name), "verteidiger": dict(verteidiger or {}),
                "wall_stufe": int(wall_stufe), "wall_zustand_prozent": float(wall_zustand),
                "verteidiger_karren": dict(verteidiger_karren or {}), "fremd": True}
        if dorf_name:                   # B-5: das ANGEGRIFFENE Dorf, nicht nur der Bot
            ziel["dorf_name"] = str(dorf_name)
        if isinstance(vorrat_ziel, BotPlayer):
            # Ein echter Bot darf nur seine tatsaechlich gespeicherten Gueter verlieren;
            # keine vom Aufrufer frei vorgegebene Beutekasse akzeptieren.
            ziel["bot_name"] = vorrat_ziel.name
            ziel["vorraete"] = dict(vorrat_ziel.vorraete or {})
            if not dorf_name:           # B-5: bei einem DORF gilt dessen Wall (oben schon gesetzt)
                ziel["wall_stufe"] = int(vorrat_ziel.wall_stufe)
                ziel["wall_zustand_prozent"] = float(vorrat_ziel.wall_zustand)
        elif vorraete is not None:
            ziel["vorraete"] = dict(vorraete or {})
        elif isinstance(vorrat_ziel, dict) and vorrat_ziel.get("id") and isinstance(
                vorrat_ziel.get("vorraete"), dict):
            ziel["id"] = vorrat_ziel["id"]
            ziel["vorraete"] = dict(vorrat_ziel["vorraete"])
        elif vorrat_ziel is not None:
            ziel["vorraete"] = self._vorraete_des_ziels(vorrat_ziel)
        else:
            # Kartenangriff: die Karte fuehrt kein Lager, der Startwert haengt am Namen.
            ziel["vorraete"] = self._vorraete_des_ziels({"name": ziel["name"]})

        if entfernung is None:
            entfernung = self._auftrag_entfernung(ort)
        # Ohne Siedlung gilt der UEBERGANGSWEG ueber den Reichsbestand; dann muss der Start
        # einen Namen tragen ("Reich"), sonst lehnt `auftraege.starten` den Auftrag ab.
        von = str(getattr(ort, "name", "") or "Reich")
        ok, meldung = self.state.auftrag_starten(
            "angreifen", truppen, von, ziel,
            float(entfernung), quelle_id=(str(getattr(ort, "id", "") or "") or None))
        text = meldung if ok else f"Angriff nicht gestartet: {meldung}"
        self.state.messages.append({"text": text, "type": "auftrag" if ok else "kampf"})
        if hasattr(self, "content"):
            self._render_view()
        return ok

    def _attack_map(self, map_id: str):
        """Kartenangriff als AUFTRAG (Entscheidung 1): kein Angriff ohne Marsch mehr.

        Dieses Gegenstueck fehlte: `_attack_map` rief den Sofortpfad, waehrend der Bot-Angriff
        schon einen Auftrag starten konnte. Ziel ist die Karte, Verteidiger ihre Garnison.
        """
        ziel = next((m for m in MAPS if m["id"] == map_id), None)
        garrison = dict(self.state.map_garrison.get(map_id, {}) or {})
        return self._angriff_auftrag_starten(ziel["name"] if ziel else map_id, garrison)


    def _activate_map(self, map_id: str):
        if map_id not in self.state.active_maps:
            self._log("Karte nicht aktiv.")
            return
        if self.state.current_map == map_id:
            self._log("Bereits auf dieser Karte.")
            return
        # Teil 3: Gold liegt im Ort (Goldmine) - eine GLOBALE Aktion zahlt aus dem ganzen Reich.
        ok_zahlung, meldung_zahlung = self.state.verbrauche_reichsweit(
            {"gold": float(self.state.map_switch_cost)})
        if not ok_zahlung:
            self._log(f"Nicht genug Geld für Kartenwechsel: {meldung_zahlung}")
            return
        self.state.current_map = map_id
        self.state.generate_map(map_id)
        self.state.map_switch_cost += 50
        self._log(f"Gewechselt zu {map_id}. Nächster Wechsel: {self.state.map_switch_cost}")
        self._render_view()

    def _station_on_map(self, map_id: str):
        total = sum(self.state.units[u].count for u in self.state.units)
        if total <= 0:
            self._log("Keine Truppen zum Stationieren.")
            return
        move = min(total, 50)
        for u in self.state.units:
            if move <= 0:
                break
            if self.state.units[u].count > 0:
                take = min(self.state.units[u].count, move)
                self.state.units[u].count -= take
                move -= take
                self.state.map_garrison.setdefault(map_id, {})
                self.state.map_garrison[map_id][u] = self.state.map_garrison[map_id].get(u, 0) + take
        self._log(f"Truppen auf {map_id} stationiert.")
        self._render_view()

    def _on_map_click(self, event):
        """Ein Klick WÄHLT NUR AUS (astra A3) — kein stiller Nebenwirkung mehr.

        Erkunden, Bewegen und Stationieren laufen über ausdrücklich benannte Schaltflächen im
        Detailpanel. Ausnahme: Ist ein Zug gestartet („Truppen von hier bewegen"), führt ein Klick
        auf ein NACHBARFELD den Zug aus.
        """
        if self.welt_gebiet != self.state.current_map:
            return
        canvas = getattr(self, "map_canvas", None)
        if canvas is None or not canvas.winfo_exists():
            return
        gitter = max(1, int(self._map_size or 20))
        zelle = int(getattr(self, "welt_zelle", WELT_ZOOM_STANDARD))
        x = int(canvas.canvasx(event.x) // zelle)
        y = int(canvas.canvasy(event.y) // zelle)
        if not (0 <= x < gitter and 0 <= y < gitter):
            return
        start = getattr(self, "_welt_start", None)
        if start is not None:
            if abs(int(start[0]) - x) + abs(int(start[1]) - y) == 1:
                self._welt_bewegen((int(start[0]), int(start[1])), (x, y))
                return
            self._welt_start = None
            self._log("Zug abgebrochen: nur ein Nachbarfeld ist ein Ziel.")
        self.welt_auswahl = (x, y)
        self._welt_detail_zeichnen()
        self._draw_map()

    def _bot_doerfer_im_raster(self, kante: int, welt_nummer: int = 0) -> list:
        """Alle fremden Doerfer, die auf DIESER Weltkarte in ein kante x kante-Raster passen.

        B-5 (02.11.2026): gezeichnet und anklickbar ist nur, was offen sichtbar ist - Name,
        Position, Fraktion, Hauptdorf.

        W-1 (Daniel 03.11.2026): **jedes Dorf steht nur auf SEINER Weltkarte.** Bis hier pruefte die
        Funktion nur `x`/`y` - ein Bot-Dorf aus einer anderen Welt erschien damit auf JEDER Karte,
        und ein Klick startete einen Marsch ueber die Weltgrenze, ohne dass jemand ihn bezahlt haette.
        Gefiltert wird ueber `dorf.dimension` (die Welt, in der das Dorf JETZT steht - ein Nebendorf
        darf spaeter wechseln). Ein Dorf mit `herkunftswelt == 0` kommt aus einem alten Spielstand
        ohne diese Angabe; dort wird NICHT gefiltert, sonst waeren seine Doerfer unsichtbar.
        """
        gitter = max(1, int(kante or 20))                              # Rasterweite der Karte
        welt = int(welt_nummer or 0) or int(getattr(self.state, "eigene_dimension", 0) or 0)
        treffer = []                                                   # Ergebnis: (Bot, Dorf)
        for bot in (getattr(self.state, "bots", None) or []):          # jeder Bot
            for dorf in bot_doerfer_sicherstellen(bot):                # je Dorf ein Eintrag
                if not (0 <= int(dorf.x) < gitter and 0 <= int(dorf.y) < gitter):
                    continue                                           # nur Doerfer auf dieser Karte
                herkunft = int(getattr(dorf, "herkunftswelt", 0) or 0)  # Welt der Entstehung (0 = alt)
                if herkunft and welt and int(dorf.dimension) != welt:   # Dorf steht auf einer anderen Welt
                    continue                                           # dann gehoert es nicht hierher
                treffer.append((bot, dorf))                            # sonst: dieses Dorf zeigen
        return treffer

    def _bot_dorf_an(self, x: int, y: int, kante: int = 20):
        """Welches fremde Dorf steht auf dem Feld (x, y)? None, wenn keines."""
        for bot, dorf in self._bot_doerfer_im_raster(kante):           # alle Doerfer dieser Karte
            if int(dorf.x) == int(x) and int(dorf.y) == int(y):
                return (bot, dorf)                                     # Treffer
        return None

    def _bot_dorf_optionen(self, bot, dorf):
        """Direkte Optionen nach dem Klick auf ein fremdes Dorf (B-5, Vorgabe Daniel 02.11.2026).

        Der Klick fuehrt NICHT sofort zu einem Auftrag: erst die Wahl "Angriff planen" oder
        "Spionage", dann die Truppenauswahl. Angezeigt wird nur, was ohne Spionage offen ist -
        Wallstufe, Taktik, Truppen und Vorraete kommen ausschliesslich ueber einen Bericht.
        """
        fenster = tk.Toplevel(self.root)                               # eigenes Fenster
        fenster.title("Fremdes Dorf: " + str(dorf.name))               # Ueberschrift
        fenster.configure(bg=self.skin["bg"])                          # Farbe wie das Spiel
        tk.Label(fenster, text="%s von %s" % (dorf.name, bot.name),
                 font=("Blackletter", 16, "bold"), fg=self.skin["gold"], bg=self.skin["bg"],
                 wraplength=520, justify=tk.LEFT).pack(anchor=tk.W, padx=12, pady=(12, 2))
        infos = ["Position %d/%d im Raster" % (int(dorf.x), int(dorf.y)),
                 "Fraktion: %s" % bot.faction,
                 "Hauptdorf" if dorf.hauptdorf else "Nebendorf"]        # oeffentliche Angaben
        volk = bottaktik.volksattribute({"fraktion": bot.faction})      # bekannte Volkswerte
        if volk.get("plus") or volk.get("minus"):
            infos.append("Volk: +%s / -%s" % (volk.get("plus") or "-", volk.get("minus") or "-"))
        tk.Label(fenster, text="\n".join(infos), fg=self.skin["text"], bg=self.skin["bg"],
                 justify=tk.LEFT, wraplength=520).pack(anchor=tk.W, padx=12)
        tk.Label(fenster, text="Wallstufe, Taktik, Truppen und Vorraete sind verdeckt - sie kommen "
                               "nur ueber einen Spionagebericht.",
                 fg="#C0C0C0", bg=self.skin["bg"], wraplength=520,
                 justify=tk.LEFT).pack(anchor=tk.W, padx=12, pady=(4, 8))
        leiste = tk.Frame(fenster, bg=self.skin["bg"])                 # Knopfleiste
        leiste.pack(anchor=tk.W, padx=12, pady=(0, 12))

        def _wahl(art: str):
            fenster.destroy()                                          # Optionen schliessen
            self._truppen_auswahl(bot, dorf, art)                      # weiter zur Planung

        tk.Button(leiste, text="Angriff planen", command=lambda: _wahl("angreifen"),
                  bg=self.skin["button"], fg=self.skin["gold"], relief=tk.FLAT,
                  padx=10, pady=3).pack(side=tk.LEFT)
        tk.Button(leiste, text="Spionage", command=lambda: _wahl("spionieren"),
                  bg=self.skin["button"], fg=self.skin["gold"], relief=tk.FLAT,
                  padx=10, pady=3).pack(side=tk.LEFT, padx=8)
        tk.Button(leiste, text="Abbrechen", command=fenster.destroy,
                  bg=self.skin["button"], fg=self.skin["text"], relief=tk.FLAT,
                  padx=10, pady=3).pack(side=tk.LEFT)

    def _truppen_auswahl(self, bot, dorf, art: str):
        """Die Truppenauswahl eines Auftrags (B-5) - der Weg von der Karte zum Auftrag.

        VORGABE Daniel 02.11.2026: "Wenn ich Spionage waehle, komm ich zur Truppenauswahl fuer
        Angriffe. Eine Spionage ist es nur dann, wenn die gesamte Truppenauswahl nur aus
        Spionageeinheiten besteht." Deshalb zeigt die Spionage-Auswahl ausschliesslich die
        Kundschafter der Diebesgilde; alles andere ist ein Angriff. Der Kern prueft dieselbe Regel
        noch einmal (`auftraege.starten`), damit die Anzeige nicht die einzige Wache ist.
        """
        ort = self.state.aktive_siedlung()                             # Quelle des Auftrags
        if ort is None:                                                # ohne Siedlung kein Auftrag
            self._log("Ohne eigene Siedlung kein Auftrag.")
            return
        spion = (art == "spionieren")                                  # Spionage oder Angriff?
        bestand = {n: int(a) for n, a in (getattr(ort, "einheiten", None) or {}).items()
                   if int(a) > 0}                                      # was im Dorf steht
        waehlbar = {n: a for n, a in bestand.items()
                    if (not spion or einheiten.ist_kundschafter(n))}    # Spionage: nur Kundschafter
        fenster = tk.Toplevel(self.root)                               # eigenes Fenster
        fenster.title(("Spionage: " if spion else "Angriff: ") + str(dorf.name))
        fenster.configure(bg=self.skin["bg"])
        tk.Label(fenster, text=("%s - Truppenauswahl" % dorf.name),
                 font=("Blackletter", 15, "bold"), fg=self.skin["gold"], bg=self.skin["bg"],
                 wraplength=520, justify=tk.LEFT).pack(anchor=tk.W, padx=12, pady=(12, 2))
        hinweis = tk.Label(fenster, text="", fg=self.skin["text"], bg=self.skin["bg"],
                           wraplength=520, justify=tk.LEFT)            # zeigt die Wirkung live
        hinweis.pack(anchor=tk.W, padx=12)
        tk.Label(fenster,
                 text=("Spionage: es reisen NUR Spionageeinheiten der Diebesgilde. Mit Kaempfern "
                       "oder Karren in der Auswahl waere es ein Angriff."
                       if spion else
                       "Angriff: alle Einheiten des Dorfes duerfen mitreisen. Karren tragen die Beute."),
                 fg="#C0C0C0", bg=self.skin["bg"], wraplength=520,
                 justify=tk.LEFT).pack(anchor=tk.W, padx=12, pady=(0, 6))
        felder = {}                                                    # Einheit -> (Variable, Bestand)
        if not waehlbar:                                               # nichts auswaehlbar
            tk.Label(fenster,
                     text=("Keine Spionageeinheiten im Dorf - erst in der Diebesgilde ausbilden "
                           "(Streuner genuegt fuer den Anfang)." if spion
                           else "Keine Einheiten im Dorf."),
                     fg="#E5A0A0", bg=self.skin["bg"], wraplength=520,
                     justify=tk.LEFT).pack(anchor=tk.W, padx=12, pady=(0, 8))
        for name, anzahl in sorted(waehlbar.items()):                  # eine Zeile je Einheit
            zeile = tk.Frame(fenster, bg=self.skin["panel"])
            zeile.pack(fill=tk.X, padx=12, pady=1)
            tk.Label(zeile, text="%s (%d im Dorf)" % (name, anzahl), fg=self.skin["text"],
                     bg=self.skin["panel"], anchor=tk.W).pack(side=tk.LEFT, padx=6)
            var = tk.StringVar(value="0")                              # Menge je Einheit
            tk.Spinbox(zeile, from_=0, to=anzahl, width=5, textvariable=var).pack(
                side=tk.RIGHT, padx=6)
            felder[name] = (var, anzahl)                               # fuer das Auslesen

        def _gewaehlt() -> dict:
            """Die aktuelle Auswahl als {Einheit: Menge} - nur brauchbare Zahlen."""
            werte = {}
            for einheit, (var, _a) in felder.items():
                try:
                    menge = int(str(var.get()).strip() or 0)
                except ValueError:
                    menge = 0
                if menge > 0:
                    werte[einheit] = menge
            return werte

        def _aktualisieren(*_args):
            """Die Wirkung der Auswahl anzeigen: Aufklaerung oder Truppenzahl."""
            werte = _gewaehlt()
            if spion:
                text = "Aufklaerung: %d (nur Auswahl aus Spionageeinheiten)" % (
                    spionage.aufklaerungswert(werte))
            else:
                text = "Einheiten in der Auswahl: %d" % sum(werte.values())
            hinweis.config(text=text)
            return text

        for var, _a in felder.values():                                # bei jeder Aenderung neu rechnen
            var.trace_add("write", _aktualisieren)
        _aktualisieren()

        def _starten():
            """Den Auftrag starten - der Kern prueft die Regeln noch einmal."""
            werte = _gewaehlt()
            if not werte:                                              # leere Auswahl
                hinweis.config(text="Keine Einheiten gewaehlt.")
                return
            if spion:                                                  # Spionage: Kern entscheidet
                ok, meldung = self.state.spionage_starten(bot, str(dorf.name), truppen=werte)
            else:                                                      # Angriff: Marsch wie immer
                entfernung = float(max(1, abs(int(ort.x) - int(dorf.x))
                                       + abs(int(ort.y) - int(dorf.y))))
                ok = self._angriff_auftrag_starten(str(dorf.name), dict(bot.army or {}),
                                                   wall_stufe=int(dorf.wall_stufe),
                                                   wall_zustand=float(dorf.wall_zustand),
                                                   vorrat_ziel=bot, entfernung=entfernung,
                                                   truppen=werte, dorf_name=str(dorf.name))
                meldung = ("Angriff auf %s gestartet." % dorf.name if ok
                           else "Angriff nicht gestartet.")
            self.state.messages.append({"text": meldung, "type": "auftrag" if ok else "kampf"})
            self._log(meldung)                                         # Statuszeile
            if getattr(self, "content", None) is not None:             # Ansicht auffrischen
                self._render_view()
            fenster.destroy()                                          # Auswahl schliessen

        leiste = tk.Frame(fenster, bg=self.skin["bg"])                 # Knopfleiste
        leiste.pack(anchor=tk.W, padx=12, pady=(8, 12))
        tk.Button(leiste, text="Auftrag starten", command=_starten,
                  bg=self.skin["button"], fg=self.skin["gold"], relief=tk.FLAT,
                  padx=10, pady=3).pack(side=tk.LEFT)
        tk.Button(leiste, text="Abbrechen", command=fenster.destroy,
                  bg=self.skin["button"], fg=self.skin["text"], relief=tk.FLAT,
                  padx=10, pady=3).pack(side=tk.LEFT, padx=8)

    def _welt_bewegung_starten(self):
        if not getattr(self, "welt_auswahl", None):
            self._log("Erst ein Feld auswählen.")
            return
        self._welt_start = (int(self.welt_auswahl[0]), int(self.welt_auswahl[1]))
        self._log(f"Zug vorbereitet ab {self._welt_koordinate(*self._welt_start)} — "
                  f"jetzt ein Nachbarfeld anklicken.")
        self._welt_detail_zeichnen()
        self._draw_map()

    def _welt_bewegung_abbrechen(self):
        self._welt_start = None
        self._log("Zug abgebrochen.")
        self._welt_detail_zeichnen()
        self._draw_map()

    def _welt_bewegen(self, start, ziel):
        """Truppen von einem Feld auf ein Nachbarfeld schicken (alter Ablauf, ausdrücklich gestartet)."""
        moving = {u: self.state.units[u].count for u in self.state.units
                  if self.state.units[u].count > 0}
        if sum(moving.values()) <= 0:
            self._welt_start = None
            self._log("Keine Truppen zum Bewegen.")
            self._welt_detail_zeichnen()
            self._draw_map()
            return
        abstand = abs(int(start[0]) - int(ziel[0])) + abs(int(start[1]) - int(ziel[1]))
        # E3 (Daniel 31.10.2026, "ein Bewegungssystem"): derselbe Weg wie im Auftrags-Pfad.
        # Vorher stand hier `dauer = max(2, abstand * 5)` MINUTEN - ohne Geschwindigkeit, ohne
        # Rueckweg. Jetzt gilt `auftraege.reisezeit_sekunden` (Faktor 2, GS der langsamsten
        # Einheit); `state.movements` fuehrt Spielsekunden, deshalb keine Umrechnung noetig.
        _gs = auftraege.tempo_der_gruppe(moving)
        # V-5: das Volk des Spielers reist schneller (elfisch +5 %) - Zeitfaktor, nicht Geschwindigkeit.
        _reise_faktor = boni.reisezeitfaktor(
            str(getattr(self.state, "spieler_fraktion", "") or ""))
        dauer_sekunden = (auftraege.reisezeit_sekunden(abstand, _gs, _reise_faktor)
                          if _gs > 0 else 0.0)
        if dauer_sekunden <= 0:
            # Ohne bekannte Geschwindigkeit wird NICHT bewegt (vorher: erfundene 5 Minuten/Feld).
            self._welt_start = None
            self._log("Bewegung abgebrochen: die Geschwindigkeit der Truppe ist unbekannt.")
            self._welt_detail_zeichnen()
            self._draw_map()
            return
        ziel_bot = None
        for bot in self.state.bots:
            if random.random() < 0.3:
                ziel_bot = bot
                break
        self.state.movements.append({
            "from": f"{int(start[0])}:{int(start[1])}",
            "to": f"{int(ziel[0])}:{int(ziel[1])}",
            "units": dict(moving),
            "start": float(self.state.spielsekunden),
            "arrival": float(self.state.spielsekunden) + float(dauer_sekunden),
            "map": self.state.current_map,
            "target_bot": ziel_bot.name if ziel_bot else None,
            "tile_key": f"{int(ziel[0])}:{int(ziel[1])}",
            "rueckweg": False,
        })
        for u, anzahl in moving.items():
            self.state.units[u].count = max(0, self.state.units[u].count - anzahl)
        self._welt_start = None
        self.welt_auswahl = (int(ziel[0]), int(ziel[1]))
        self._log(f"Truppen bewegen nach {self._welt_koordinate(*ziel)}. "
                  f"Ankunft in {dauer_sekunden / 3600.0:.1f} Spielstunden "
                  f"(GS {_gs}, Strecke {abstand}).")
        self._welt_detail_zeichnen()
        self._draw_map()

    def _welt_ort_erkunden(self, x: int, y: int):
        """Den gewählten Ort erforschen — bewusst über eine Schaltfläche, nicht über den Klick."""
        tile = self.state.get_tile(int(x), int(y), self._map_size)
        if tile is None:
            return
        ort = self._welt_koordinate(int(x), int(y))
        tile.discovered = True
        if tile.quest and not tile.quest_done:
            tile.quest_done = True
            self.state.ruf += 15
            self.state.resources["gold"].amount += 20
            self._log(f"Aufgabe abgeschlossen: {tile.quest} ({ort}). Ruf +15, Gold +20")
        elif tile.resources:
            stoffe = ", ".join(f"{k}: {int(v)}" for k, v in tile.resources.items())
            self._log(f"{ort} erkundet ({tile.terrain}): {stoffe}")
        else:
            self._log(f"{ort} erkundet ({tile.terrain}).")
        self.welt_auswahl = (int(x), int(y))
        self._welt_detail_zeichnen()
        self._draw_map()
    def _render_diplomacy(self):
        tk.Label(self.content, text="Diplomatie", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        for bot in self.state.bots:
            frame = tk.Frame(self.content, bg=self.skin["panel"])
            frame.pack(fill=tk.X, padx=10, pady=2)
            tk.Label(frame, text=bot.name, fg=self.skin["text"], bg=self.skin["panel"], width=15, anchor=tk.W).pack(side=tk.LEFT, padx=5)
            tk.Label(frame, text=f"Handel: {int(bot.trading*100)}%", fg="#DAA520", bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
            tk.Label(frame, text=f"Aggression: {int(bot.aggression*100)}%", fg=self.skin["red"], bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
            tk.Button(frame, text="Handeln", command=lambda b=bot: self._trade(b), bg="#3e2723", fg=self.skin["gold"]).pack(side=tk.RIGHT, padx=5)
            # Entscheidung 1 (01.11.2026): es gibt EINEN Angriffsweg, und er reist. Der zweite
            # Knopf "Angreifen" ist entfallen - er tat dasselbe wie "Angriff entsenden" und
            # suggerierte einen Sofortangriff, den es nicht mehr gibt.
            tk.Button(frame, text="Angriff entsenden",
                      command=lambda b=bot: self._auftrag_angriff(b),
                      bg="#3e2723", fg=self.skin["gold"]).pack(side=tk.RIGHT, padx=5)
            # S-7 (bottaktik): die deutsche Verhaltenszeile aus `bottaktik.anzeige`
            # (Zustand, Taktik, Grund) - EINE Funktion fuer Kern und Anzeige.
            zeile = bottaktik.anzeige(self.state.bot_als_dict(bot))
            tk.Label(frame, text=zeile, fg=self.skin["text"], bg=self.skin["panel"],
                     anchor=tk.W).pack(fill=tk.X, padx=5)

    def _trade(self, bot: BotPlayer):
        """Handel mit einem Bot: der BESTÄTIGTE KAUFVERTRAG (Teil 7b, Entwurf Z. 779/781).

        Es gibt genau EINEN Weg: das bestätigte Angebot über `spieloekonomie.handel_start` /
        `handel_entscheiden` / `handel_abschluss`. Der Altpfad, der Ware ohne Gegenleistung schenkte
        (`random.randint`-Mengen direkt ins Lager, kein Gold, Ruf und Handelszähler stiegen mit), ist
        gesperrt (`01fe939`) und kehrt nicht zurück. Ist der Handel wirklich nicht möglich, wird das
        ehrlich gesagt — gebucht wird dann NICHTS (kein Rohstoff, kein Gold, kein Ruf, kein
        Handelszähler am Bot).
        """
        if not self.state.settlements:
            self._log("Für einen Handel braucht es zuerst eine eigene Siedlung.")
            return False
        if float(bot.trading) <= 0.3:
            self._log(f"{bot.name} handelt nicht (Handelsneigung "
                      f"{int(float(bot.trading) * 100)} %).")
            return False
        if getattr(self, "root", None) is None:
            self._log("Handel braucht das Spielfenster (Maske für Ware, Menge und Preis) — "
                      "gebucht wird über `handel_mit_bot`.")
            return False
        self._handel_maske(bot)
        return True

    def _attack(self, bot: BotPlayer):
        """Bot-Angriff: EINE Regel mit dem Reiseauftrag (Entscheidung 1, Daniel 01.11.2026).

        Bis zum 01.11.2026 gab es hier zwei Wege: dieser rief den Sofortpfad ohne Marsch, der
        Knopf daneben startete einen Auftrag. Jetzt ist beides derselbe Weg - der Angriff reist.
        Der Götterschutz bleibt davor: unter Schutz wird nicht angegriffen.
        """
        if self.state.noob_protection and bot.noob_protection:
            self._log(f"{bot.name} steht unter Götterschutz. Angriff nicht möglich.")
            return
        # W2/W2b: kein Daumenvergleich mehr, sondern der Originalablauf. Die Verteidiger sind
        # die Armee des Bots, seine Vorraete liefert `_vorraete_des_ziels` (bis Schritt 8 aus
        # den VORSCHLAG-Spannen in botkern, danach aus dem Bot selbst). Einen Wall hat ein Bot
        # in unseren Daten nicht - also Stufe 0, ehrlich, ohne erfundenen Wert.
        return self._auftrag_angriff(bot)

    # ---------- W7: Auftraege (Missionen) in der Oberflaeche ----------

    def _auftrag_entfernung(self, siedlung=None) -> float:
        """Die Entfernung eines Auftrags in Feldern — vom STARTORT des Auftrags aus.

        Das Modul rechnet 1 Feld = 1 Stunde bei Geschwindigkeit 1 (VORSCHLAG; das Handbuch nennt
        nur Beispielstunden). Bot-Siedlungen fuehren bei uns **keine** Koordinaten — es gilt
        deshalb die Kartenmitte als Zielort. Das ist eine Annahme und steht so im Bericht.

        F-09 (31.10.2026): Vorgabe ist die AKTIVE Siedlung. Vorher fiel die Funktion auf
        `settlements[0]` zurueck - der Angriff startete damit aus dem falschen Dorf.
        """
        cfg = next((m for m in MAPS if m["id"] == self.state.current_map), None)
        mitte = int(cfg["size"]) // 2 if cfg else 10
        start = siedlung if siedlung is not None else self.state.aktive_siedlung()
        if start is None:
            return float(max(1, mitte))
        return float(max(1, abs(int(start.x) - mitte) + abs(int(start.y) - mitte)))

    def _auftrag_angriff(self, bot: BotPlayer):
        """Einen Angriff als AUFTRAG entsenden: mit Reisezeit, Rueckkehr und Bericht (W7).

        Quelle ist das ORTSHEER der aktiven Siedlung (F-01/F-09 der externen Spielpruefung):
        die Truppen kommen aus `Settlement.einheiten` dieses Dorfes, der Auftrag traegt dessen
        Kennung (`quelle_id`), die Reisezeit rechnet von SEINEN Koordinaten, und die Ueberlebenden
        kehren in IHN zurueck.

        Seit Entscheidung 1 (Daniel, 01.11.2026) ist dies der EINZIGE Angriffsweg - der frueher
        getrennte Sofortpfad `_angriff_durchfuehren` ist stillgelegt; hier wird nur noch der
        gemeinsame Kern `_angriff_auftrag_starten` aufgerufen.
        """
        # Kein Siedlungszwang: ohne Siedlung greift der Uebergangsweg ueber das Reichsheer
        # (dieselbe Regel wie in `_angriff_auftrag_starten`). Vorher lehnte dieser Pfad ab.
        ort = self.state.aktive_siedlung()
        entfernung = self._auftrag_entfernung(ort)
        ok = self._angriff_auftrag_starten(bot.name, dict(bot.army or {}),
                                           wall_stufe=bot.wall_stufe,
                                           wall_zustand=bot.wall_zustand,
                                           vorrat_ziel=bot, entfernung=entfernung)
        if ok:
            self.state.messages.append(
                {"text": f"Hinweis: die Entfernung {entfernung:.0f} Felder ist geschätzt "
                         f"(Bot-Siedlung in der Kartenmitte angenommen, {bot.name} führt keine "
                         f"Koordinaten).", "type": "auftrag"})
            if hasattr(self, "content"):
                self._render_view()
        return ok

    def _eigene_schlagkraft(self) -> float:
        """Die Schlagkraft der eigenen Truppen aus `einheiten.kampfstaerke` (Originalwerte).

        Vorher stand hier `get_combat_power` aus `bonus_system` — die erfundene Kampfkraft, die
        mit den Kampfwerten des Handbuchs nichts zu tun hatte.
        """
        kaempfer, belagerung, _karren = self._truppen_nach_rolle()
        summe = 0.0
        for name, anzahl in kaempfer.items():
            summe += einheiten.kampfstaerke(name, int(anzahl))
        for name, anzahl in belagerung.items():
            summe += einheiten.kampfstaerke(name, int(anzahl))
        return summe

    def _zufallsgegner(self):
        """Ein ausgedachter Gegner fuer den Simulator (Rueckgabe (einheiten, wall_stufe)).

        Ausgedacht ist hier erlaubt und noetig: das Handbuch nennt keinen Uebungsgegner. Es wird
        aber nichts in den Spielstand gebucht - der Simulator ist ein Trockenkurs.
        """
        wahl = random.Random()
        kaempfer = sorted(k for k, u in self.state.units.items()
                          if (u.rolle or einheiten.rolle(k)) in ("kaempfer", "kundschafter"))
        gegner = {}
        for name in wahl.sample(kaempfer, min(3, len(kaempfer))) if kaempfer else []:
            gegner[name] = wahl.randint(1, 10)
        return gegner, wahl.randint(0, 3)

    def _render_battle_simulator(self):
        tk.Label(self.content, text="Kampfsimulator", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        tk.Label(self.content, text="Trockenkurs: der Kampf laeuft mit dem echten Schlachtmodell, "
                                    "aendert aber NICHTS im Spielstand.", fg="#C0C0C0", bg=self.skin["bg"],
                 wraplength=760, justify=tk.LEFT).pack(anchor=tk.W, padx=10)
        frame = tk.Frame(self.content, bg=self.skin["panel"])
        frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(frame, text="Eigene Schlagkraft (Fuß- und Belagerungstruppen):", fg=self.skin["text"], bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
        tk.Label(frame, text=f"{int(self._eigene_schlagkraft())}", fg="#DAA520", bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Zufallsangriff", command=self._simulate_random_battle, bg="#3e2723", fg=self.skin["gold"]).pack(side=tk.RIGHT, padx=5)
        kaempfer, belagerung, karren = self._truppen_nach_rolle()
        tk.Label(self.content, text="Kämpfer/Kundschafter: " +
                 (", ".join(f"{n} {a}" for n, a in sorted(kaempfer.items())) or "keine") +
                 " · Belagerung: " + (", ".join(f"{n} {a}" for n, a in sorted(belagerung.items())) or "keine") +
                 " · Karren: " + (", ".join(f"{n} {a}" for n, a in sorted(karren.items())) or "keine"),
                 fg=self.skin["text"], bg=self.skin["bg"], wraplength=760, justify=tk.LEFT).pack(anchor=tk.W, padx=10)

    def _simulate_random_battle(self, gegner=None, wall_stufe=None):
        """Ein Probekampf im Simulator — rechnet wie ein echter Angriff, bucht aber nichts."""
        kaempfer, belagerung, karren = self._truppen_nach_rolle()
        if not kaempfer and not belagerung:
            meldung = "Keine Kaempfer und keine Belagerungswaffen vorhanden."
            self.state.messages.append({"text": meldung, "type": "kampf"})
            self._log(meldung)
            return False
        if gegner is None or wall_stufe is None:
            gegner_auto, wall_auto = self._zufallsgegner()
            gegner = gegner if gegner is not None else gegner_auto
            wall_stufe = wall_stufe if wall_stufe is not None else wall_auto

        angreifer = dict(kaempfer)
        angreifer.update(belagerung)
        ergebnis = kampf.fuehre_schlacht(
            angreifer, dict(gegner or {}), int(wall_stufe), 100.0,
            angreifer_karren=karren or None,
            vorraete=self._vorraete_des_ziels({"name": "Simulator-Gegner"}),
            rng=random.Random(),
            forschung_angreifer={k: int(v.level) for k, v in self.state.research.items()},
            # V-5: der Simulator rechnet mit dem Volk des Spielers - sonst zeigte der Trockenkurs
            # andere Zahlen als der echte Angriff.
            boni_angreifer=boni.kampf_werte(boni.modifikatoren(
                str(getattr(self.state, "spieler_fraktion", "") or ""))))
        bericht = kampfbericht.bericht(ergebnis)
        kopf = f"Simulator (Trockenkurs) gegen Wallstufe {int(wall_stufe)} "
        self.state.messages.append({"text": kopf + "— " + bericht["titel"] + "\n" +
                                            "\n".join(bericht["zeilen"]), "type": "kampf"})
        self._log(f"Simulator: Ausgang {ergebnis.get('ausgang')} — Spielstand unveraendert.")
        if hasattr(self, "content"):
            self._render_view()
        return True

    def _render_hall_of_fame(self):
        # W6: dieselben Originalformeln wie in der Seitenleiste. Vorher stand hier die falsche
        # Gesamtsumme `score + ruf + Kampfkraft aller Einheiten`.
        staende = {k: v.level for k, v in self.state.research.items()}
        einheiten = {k: v.count for k, v in self.state.units.items()}
        wall_stufe = self.state.punktestand()["wall_stufe"]
        total_units = sum(self.state.units[u].count for u in self.state.units)
        tk.Label(self.content, text="Ruhmeshalle", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        tk.Label(self.content, text="Eure Punkte", fg="#C0C0C0", bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)
        tk.Label(self.content, text=f"Forschung: {punkte.forschungspunkte(staende)}", fg="#DAA520", bg=self.skin["bg"]).pack(anchor=tk.W, padx=20)
        tk.Label(self.content, text=f"Krieg: {self.state.punktestand()['krieg']}", fg=self.skin["red"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=20)
        tk.Label(self.content, text=f"Wallstufe: {wall_stufe}", fg=self.skin["text"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=20)
        tk.Label(self.content, text=f"Truppen: {total_units}", fg=self.skin["text"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=20)
        tk.Label(self.content, text=f"Gesamt: {self.state.punktestand()['gesamt']}", fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=20)

    def _render_news(self):
        tk.Label(self.content, text="Neuigkeiten", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        tk.Label(self.content, text="Höret, höret, höret. Der Dorfschreiber verkündet...", fg="#C0C0C0", bg=self.skin["bg"], wraplength=600, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=(0, 10))
        tk.Label(self.content, text=f"Das Volk ehrt Eure Anwesenheit. Aktuelle Rufpunkte: {self.state.ruf}.", fg="#DAA520", bg=self.skin["bg"], wraplength=600, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=(0, 10))
        tk.Label(self.content, text="09.02.2008 — Onlinezeitung für Nebelseetal.", fg="#C0C0C0", bg=self.skin["bg"], wraplength=600, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=(0, 5))
        tk.Label(self.content, text="20.07.2007 — Einheiten Löschen: Über die Kaserne können überflüssige Einheiten entlassen werden. ACHTUNG: Entlassene Einheiten sind unwiederbringlich gelöscht!", fg=self.skin["red"], bg=self.skin["bg"], wraplength=600, justify=tk.LEFT).pack(anchor=tk.W, padx=10)

    def _render_market(self):
        tk.Label(self.content, text="Marktplatz", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        tk.Label(self.content, text="Handle mit anderen Spielern oder Bots.", fg="#C0C0C0", bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)
        for bot in self.state.bots:
            if bot.trading <= 0.3:
                continue
            frame = tk.Frame(self.content, bg=self.skin["panel"])
            frame.pack(fill=tk.X, padx=10, pady=2)
            tk.Label(frame, text=bot.name, fg=self.skin["text"], bg=self.skin["panel"], width=15, anchor=tk.W).pack(side=tk.LEFT, padx=5)
            tk.Button(frame, text="Handeln", command=lambda b=bot: self._trade(b), bg="#3e2723", fg=self.skin["gold"]).pack(side=tk.RIGHT, padx=5)

    def _render_guild(self):
        tk.Label(self.content, text="Gilde", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        tk.Label(self.content, text="Gildenwertung", fg="#C0C0C0", bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 0))
        frame = tk.Frame(self.content, bg=self.skin["panel"])
        frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(frame, text="Platz", fg=self.skin["gold"], bg=self.skin["panel"], width=8).pack(side=tk.LEFT, padx=5)
        tk.Label(frame, text="Gildenname", fg=self.skin["gold"], bg=self.skin["panel"], width=20).pack(side=tk.LEFT, padx=5)
        tk.Label(frame, text="Mitglieder", fg=self.skin["gold"], bg=self.skin["panel"], width=12).pack(side=tk.LEFT, padx=5)
        tk.Label(frame, text="Punkte", fg=self.skin["gold"], bg=self.skin["panel"], width=12).pack(side=tk.LEFT, padx=5)
        guilds = [
            ("1", "Nebelwölfe", "12", "4520"),
            ("2", "Drachenclan", "8", "3890"),
            ("3", "Waldläufer", "15", "3560"),
        ]
        for g in guilds:
            row = tk.Frame(self.content, bg=self.skin["panel"])
            row.pack(fill=tk.X, padx=10, pady=2)
            tk.Label(row, text=g[0], fg=self.skin["text"], bg=self.skin["panel"], width=8).pack(side=tk.LEFT, padx=5)
            tk.Label(row, text=g[1], fg="#DAA520", bg=self.skin["panel"], width=20).pack(side=tk.LEFT, padx=5)
            tk.Label(row, text=g[2], fg=self.skin["text"], bg=self.skin["panel"], width=12).pack(side=tk.LEFT, padx=5)
            tk.Label(row, text=g[3], fg=self.skin["text"], bg=self.skin["panel"], width=12).pack(side=tk.LEFT, padx=5)
        tk.Label(self.content, text="Gildenprofil folgt in einer späteren Version.", fg="#C0C0C0", bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=10)

    def _render_messages(self):
        tk.Label(self.content, text="Nachrichten", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        for msg in reversed(self.state.messages[-20:]):
            color = nachrichten_farbe(msg)
            tk.Label(self.content, text=zeitbasis.zeitstempel_text(msg) + msg["text"],
                     fg=color, bg=self.skin["bg"], wraplength=600,
                     justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=(0, 5))
            # B-5 (02.11.2026): ein Spionagebericht bekommt eine eigene Anzeige - der Spieler
            # oeffnet ihn, statt ihn zwischen allen anderen Nachrichten zu suchen. Ist er aelter
            # als die Frist aus data/spionage.json, steht das ausdruecklich daneben.
            if str(msg.get("type") or "") == "spionage":
                hinweis = spionage.veraltet_text(msg, self.state.spielsekunden)
                if hinweis:
                    tk.Label(self.content, text=hinweis, fg="#C0C0C0", bg=self.skin["bg"],
                             wraplength=600, justify=tk.LEFT).pack(anchor=tk.W, padx=10)
                tk.Button(self.content, text="Spionagebericht oeffnen",
                          command=lambda m=msg: self._spionage_bericht_anzeigen(m),
                          bg=self.skin["button"], fg=self.skin["gold"], relief=tk.FLAT,
                          padx=8, pady=2).pack(anchor=tk.W, padx=10, pady=(0, 6))

    def _spionage_bericht_anzeigen(self, msg):
        """Den Spionagebericht in einem eigenen Fenster zeigen (Postfach, B-5, 02.11.2026).

        Der Text kommt unveraendert aus der Nachricht (`spionage.bericht_nachricht`) - die Anzeige
        rechnet nichts nach. Ist der Bericht aelter als die Frist, steht der Hinweis darueber.
        """
        nachricht = msg if isinstance(msg, dict) else {}                       # Nachricht als dict
        fenster = tk.Toplevel(self.root)                                       # eigenes Fenster
        fenster.title(str(nachricht.get("titel") or "Spionagebericht"))        # Ueberschrift
        fenster.configure(bg=self.skin["bg"])                                  # Farbe wie das Spiel
        tk.Label(fenster, text=str(nachricht.get("titel") or "Spionagebericht"),
                 font=("Blackletter", 16, "bold"), fg=self.skin["gold"],
                 bg=self.skin["bg"], wraplength=640, justify=tk.LEFT).pack(
            anchor=tk.W, padx=10, pady=(10, 4))                                # Titel
        hinweis = spionage.veraltet_text(nachricht, self.state.spielsekunden)  # Frist pruefen
        if hinweis:                                                            # nur wenn zu alt
            tk.Label(fenster, text=hinweis, fg="#C0C0C0", bg=self.skin["bg"],
                     wraplength=640, justify=tk.LEFT).pack(anchor=tk.W, padx=10)
        tk.Label(fenster, text=str(nachricht.get("text") or ""), fg=self.skin["text"],
                 bg=self.skin["bg"], wraplength=640, justify=tk.LEFT).pack(
            anchor=tk.W, padx=10, pady=(2, 8))                                 # der Bericht selbst
        tk.Button(fenster, text="Schliessen", command=fenster.destroy,
                  bg=self.skin["button"], fg=self.skin["gold"], relief=tk.FLAT,
                  padx=8, pady=2).pack(anchor=tk.E, padx=10, pady=(0, 10))     # schliessen

    def _render_settings(self):
        tk.Label(self.content, text="Einstellungen", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        tk.Label(self.content,
                 text="Spielzeit (Zeitfaktor) — die Handbuchformeln bleiben, nur die Spieluhr läuft\n"
                      "schneller. Bei „1 Std = 20 s“ dauert eine Spielstunde 20 echte Sekunden:\n"
                      "ein Holzfäller auf Wald bringt dann 4 Holz alle 20 Sekunden.",
                 fg=self.skin["text"], bg=self.skin["bg"], justify=tk.LEFT,
                 font=("Arial", 9)).pack(anchor=tk.W, padx=10, pady=(4, 6))

        zeile = tk.Frame(self.content, bg=self.skin["bg"])
        zeile.pack(anchor=tk.W, padx=10)
        tk.Label(zeile, text="Tempo:", fg=self.skin["text"], bg=self.skin["bg"],
                 font=("Arial", 9)).pack(side=tk.LEFT, padx=(0, 6))

        def _tempo_setzen(wert):
            try:
                spielzeit.setzen(wert)
            except OSError as exc:
                messagebox.showerror("Spielzeit konnte nicht gespeichert werden", str(exc))
                return
            self._log(f"Spielzeit auf {spielzeit.text()} gestellt.")
            self._render_settings()

        for stufe in spielzeit.stufen():
            ist_gewaehlt = abs(stufe - spielzeit.faktor()) < 1e-9
            tk.Button(zeile, text=spielzeit.text(stufe), command=lambda s=stufe: _tempo_setzen(s),
                      bg=(self.skin["gold"] if ist_gewaehlt else self.skin["button"]),
                      fg=(self.skin["bg"] if ist_gewaehlt else self.skin["gold"]),
                      relief=tk.FLAT, padx=8, pady=2).pack(side=tk.LEFT, padx=3)

        tk.Label(self.content, text="Weitere Spieleinstellungen folgen in einer späteren Version.",
                 fg="#C0C0C0", bg=self.skin["bg"], font=("Arial", 9)).pack(anchor=tk.W, padx=10,
                                                                          pady=(10, 0))

    def _render_help(self):
        """FIX04c: Dauerhaft erreichbare Spielerhilfe mit vorbereiteten Fragen."""
        tk.Label(self.content, text="Spielerhilfe", font=("Blackletter", 20, "bold"),
                 fg=self.skin["gold"], bg=self.skin["bg"]).pack(
                     anchor=tk.W, padx=10, pady=(10, 4))
        hilfe_admin = (self._profil == "admin" and self._admin_sitzung_freigegeben
                       and getattr(self.state, "admin_teststand", False))
        if spielerhilfe.schutz_aktiv(self.state):
            schutztext = ("Götterschutz aktiv: Die Einstiegshilfe steht rechts neben dem Spiel. "
                          "Sie verschwindet nach Schutzende automatisch." if
                          spielerhilfe.hilfe_sichtbar(self.state, admin_freigabe=hilfe_admin)
                          else "Götterschutz aktiv: Die Einstiegshilfe wurde im Admin-Test ausgeblendet.")
        else:
            schutztext = "Götterschutz beendet: Du kannst diese Hilfe weiterhin jederzeit öffnen."
        admin_hinweis = spielerhilfe.admin_hilfe_modus_text(
            self.state, admin_freigabe=(self._profil == "admin" and
                                      self._admin_sitzung_freigegeben))
        if admin_hinweis:
            schutztext += " " + admin_hinweis
        tk.Label(self.content, text=schutztext, fg=self.skin["text"],
                 bg=self.skin["bg"], wraplength=740, justify=tk.LEFT).pack(
                     anchor=tk.W, padx=10, pady=(0, 8))
        tk.Label(self.content, text="Für deinen aktuellen Spielstand:",
                 fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)
        tk.Label(self.content, text=spielerhilfe.naechster_schritt(self.state),
                 fg=self.skin["text"], bg=self.skin["bg"], wraplength=740,
                 justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=(0, 10))
        tk.Label(self.content, text="Häufige Fragen (anklicken):",
                 fg=self.skin["gold"], bg=self.skin["bg"],
                 font=("Arial", 11, "bold")).pack(anchor=tk.W, padx=10, pady=(0, 4))
        for frage in spielerhilfe.FRAGEN:
            tk.Button(self.content, text=frage, anchor=tk.W,
                      command=lambda f=frage: self._spielerhilfe_frage(f),
                      bg=self.skin["button"], fg=self.skin["gold"],
                      relief=tk.FLAT).pack(fill=tk.X, padx=10, pady=2)
        if getattr(self, "_hilfe_letzte_antwort", None):
            tk.Label(self.content, text=self._hilfe_letzte_antwort,
                     fg=self.skin["text"], bg=self.skin["panel"],
                     wraplength=720, justify=tk.LEFT, anchor=tk.NW,
                     padx=12, pady=12).pack(fill=tk.X, padx=10, pady=(8, 8))
        tk.Button(self.content, text="Weitere Fragen im Spielchat stellen",
                  command=lambda: self._switch_view("Chat"),
                  bg=self.skin["button"], fg=self.skin["gold"]).pack(
                      anchor=tk.W, padx=10, pady=(8, 15))

    def _spielerhilfe_frage(self, frage: str):
        """Nur Auskunft, keinerlei Änderung an Ressourcen, Gebäuden oder Schutz."""
        self._hilfe_letzte_antwort = spielerhilfe.antwort(frage, self.state)
        self._render_view()

    def _render_forum(self):
        tk.Label(self.content, text="Forum", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        tk.Label(self.content, text="Forum ist offline.", fg="#C0C0C0", bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)

    def _render_chat(self):
        tk.Label(self.content, text="Auskunft im Spiel", font=("Blackletter", 20, "bold"),
                 fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 2))
        tk.Label(self.content,
                 text="Ich antworte aus dem Originalhandbuch und den Spieldaten — ohne Netz und "
                      "ohne Schlüssel. Bei Zahlen, die das Handbuch nicht nennt, sage ich es dazu.",
                 fg=self.skin["text"], bg=self.skin["bg"], wraplength=780,
                 justify=tk.LEFT).pack(anchor=tk.W, padx=10)

        if not getattr(self, "chat_verlauf", None):
            self.chat_verlauf = [("berater", berater.begruessung())]

        rahmen = tk.Frame(self.content, bg=self.skin["panel"])
        rahmen.pack(fill=tk.X, padx=10, pady=6)
        for wer, text in self.chat_verlauf[-10:]:
            tk.Label(rahmen, text=("Auskunft:  " if wer == "berater" else "Du:  ") + str(text),
                     fg=(self.skin["gold"] if wer == "berater" else "#9FD6FF"),
                     bg=self.skin["panel"], justify=tk.LEFT, anchor=tk.W,
                     wraplength=740).pack(fill=tk.X, padx=6, pady=2)

        zeile = tk.Frame(self.content, bg=self.skin["bg"])
        zeile.pack(fill=tk.X, padx=10, pady=(4, 2))
        self.chat_eingabe = tk.Entry(zeile, bg=self.skin["panel"], fg=self.skin["text"],
                                     insertbackground=self.skin["text"])
        self.chat_eingabe.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        self.chat_eingabe.bind("<Return>", lambda _e: self._chat_fragen())
        tk.Button(zeile, text="Fragen", command=self._chat_fragen, bg=self.skin["button"],
                  fg=self.skin["gold"], activebackground="#5D4037").pack(side=tk.LEFT)
        try:
            self.chat_eingabe.focus_set()
        except Exception:
            pass

        beispiele = tk.Frame(self.content, bg=self.skin["bg"])
        beispiele.pack(anchor=tk.W, padx=10, pady=(2, 8))
        tk.Label(beispiele, text="Zum Antippen:", fg=self.skin["text"],
                 bg=self.skin["bg"]).pack(anchor=tk.W)
        vorschlaege = ["Wie fange ich an?", "Was macht der Holzfäller?",
                       "Welches Gelände braucht der Steinmetz?", "Wie läuft ein Kampf ab?",
                       "Was kostet die Forschung?", "Was kann der Paladin?", "Gib mir einen Tipp"]
        knopfreihe = tk.Frame(beispiele, bg=self.skin["bg"])
        knopfreihe.pack(anchor=tk.W)
        for i, frage in enumerate(vorschlaege):
            tk.Button(knopfreihe, text=frage, command=lambda f=frage: self._chat_fragen(f),
                      bg=self.skin["button"], fg=self.skin["gold"],
                      activebackground="#5D4037").grid(row=i // 4, column=i % 4, padx=3, pady=2,
                                                       sticky=tk.W)

    def _chat_fragen(self, frage: str = None):
        if frage is None:
            try:
                frage = self.chat_eingabe.get()
            except Exception:
                frage = ""
        frage = (frage or "").strip()
        if not frage:
            return
        if not getattr(self, "chat_verlauf", None):
            self.chat_verlauf = []
        self.chat_verlauf.append(("du", frage))
        try:
            antwort = berater.antwort(frage, self.state)
        except Exception as fehler:                     # nie das Spiel zum Absturz bringen
            antwort = (f"Das konnte ich nicht beantworten ({type(fehler).__name__}). "
                       "Frag mich anders, zum Beispiel nach einem Gebäude, einer Einheit "
                       "oder einem Gelände.")
        self.chat_verlauf.append(("berater", antwort))
        self._render_view()

    def _render_referral(self):
        tk.Label(self.content, text="Spieler werben", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        tk.Label(self.content, text="Werben folgt in einer späteren Version.", fg="#C0C0C0", bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)

    def _render_neuigkeiten(self):
        """Neuigkeiten — im Original ein eigener Hauptmenuepunkt (Screenshots web_1838856/57).

        Inhalt bei uns: die letzten Meldungen des Spiels (dieselbe Quelle wie `state.messages`,
        also keine zweite Wahrheit). Personalnachrichten an einzelne Spieler gibt es im
        Einzelspieler-Remake nicht — deshalb steht hier der Spielverlauf.
        """
        tk.Label(self.content, text="Neuigkeiten", font=("Blackletter", 20, "bold"),
                 fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        tk.Label(self.content, text="Was zuletzt im Spiel passiert ist (neueste zuerst).",
                 fg="#C0C0C0", bg=self.skin["bg"], wraplength=780,
                 justify=tk.LEFT).pack(anchor=tk.W, padx=10)
        meldungen = list(getattr(self.state, "messages", None) or [])[-15:]
        if not meldungen:
            tk.Label(self.content, text="Noch keine Meldungen.", fg="#FDBA74",
                     bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=8)
            return
        for eintrag in reversed(meldungen):
            zeile = tk.Frame(self.content, bg=self.skin["panel"])
            zeile.pack(fill=tk.X, padx=10, pady=1)
            zeit = str(eintrag.get("zeit_lokal") or "")[11:19]
            tk.Label(zeile, text=zeit, width=9, anchor=tk.W, fg=self.skin["gold"],
                     bg=self.skin["panel"], font=("Arial", 9)).pack(side=tk.LEFT, padx=4)
            tk.Label(zeile, text=str(eintrag.get("text") or ""), anchor=tk.W, wraplength=640,
                     justify=tk.LEFT, fg=self.skin["text"],
                     bg=self.skin["panel"]).pack(side=tk.LEFT, padx=4)

    def _render_voraussetzungen(self):
        """Zeigt, welche Forschung welche Bedingung hat (Original-Hauptmenue, Handbuch Seite 12).

        Quelle ist `data/research.json` (Feld `voraussetzung`, z. B. "Bibliothek 3" oder
        "Bibliothek 3 + Schmiedekunst 1"). Der erreichte Stand kommt aus `state.research` —
        also dieselbe Quelle, die auch forscht. Nichts wird hier geschaetzt.
        """
        tk.Label(self.content, text="Voraussetzungen", font=("Blackletter", 20, "bold"),
                 fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        tk.Label(self.content, text="Welche Forschung welche Bedingung hat — Handbuch Seite 12: "
                                    "„Welche Voraussetzungen Du für die Forschungen benötigst, "
                                    "kannst Du unter Voraussetzungen im Hauptmenü erfahren.“",
                 fg="#C0C0C0", bg=self.skin["bg"], wraplength=780,
                 justify=tk.LEFT).pack(anchor=tk.W, padx=10)
        pfad = os.path.join(spieldaten.projektwurzel(), "data", "research.json")
        try:
            with open(pfad, encoding="utf-8") as f:
                daten = json.load(f)
        except (OSError, ValueError) as fehler:
            self._log(f"Voraussetzungen nicht lesbar: {fehler}")
            return
        eintraege = daten.get("forschungen") or daten
        kopf = tk.Frame(self.content, bg=self.skin["panel"])
        kopf.pack(fill=tk.X, padx=10, pady=(6, 0))
        for text, breite in (("Forschung", 22), ("Bedingung", 34), ("Stufe", 6)):
            tk.Label(kopf, text=text, width=breite, anchor=tk.W, fg=self.skin["gold"],
                     bg=self.skin["panel"]).pack(side=tk.LEFT, padx=4)
        for name in sorted(eintraege):
            wert = eintraege[name] if isinstance(eintraege[name], dict) else {}
            bedingung = str(wert.get("voraussetzung") or "—")
            eintrag = self.state.research.get(name)
            erreicht = int(getattr(eintrag, "level", 0) or 0)
            zeile = tk.Frame(self.content, bg=self.skin["panel"])
            zeile.pack(fill=tk.X, padx=10, pady=1)
            tk.Label(zeile, text=name, width=22, anchor=tk.W, fg=self.skin["text"],
                     bg=self.skin["panel"]).pack(side=tk.LEFT, padx=4)
            tk.Label(zeile, text=bedingung, width=34, anchor=tk.W, fg="#DAA520",
                     bg=self.skin["panel"]).pack(side=tk.LEFT, padx=4)
            tk.Label(zeile, text=str(erreicht), width=6, anchor=tk.W,
                     fg=self.skin["text"], bg=self.skin["panel"]).pack(side=tk.LEFT, padx=4)

    def _render_research(self):
        # B-6 (02.11.2026, Vorgabe Daniel): die Bibliothek ist der HINTERGRUND dieser Ansicht.
        if self._ansicht_hintergrund("bibliothek") is None:      # kein Bild vorhanden
            self._gebaeude_kopf("bibliothek")                    # dann der alte Kopf
        # M-5 (Vorgabe Daniel 02.11.2026: "dann die uebrigen Textfelder", "stueck fuer stueck"):
        # Titel und Einleitung waren in der Forschung noch harte Balken ueber die volle Breite,
        # obwohl die Bibliothek hier schon der Hintergrund ist. Jetzt liegen sie als weiche Felder
        # auf dem Bild; die Forschungszeilen darunter bleiben ein deckender Block (Tabelle).
        self._kasten_label("Forschung", ("Blackletter", 20, "bold"), self.skin["gold"], innen=14, pady=6)

        self._kasten_label(
            "Forschung braucht eine Bibliothek und Zeit: die Dauer ist die "
            "Stufe zum Quadrat in Stunden (Handbuch S. 12/13). Die Stufe "
            "steigt erst nach Ablauf.",
            ("TkDefaultFont", 9), "#C0C0C0", breite=810, innen=14, pady=5, umbruch=780)
        # W4c: laufende Forschung mit Restzeit. Gezeigt wird, was `forschung.fortschritt` wirklich
        # hergibt (keine eigene Rechnung in der Oberflaeche).
        stand = self.state.forschung_stand()
        # Teil 6 (Rest): die Spieluhr, nicht die Rechnerzeit — die Auftraege rechnen in
        # Spielsekunden (`spieloekonomie.forschung_start`/`forschung_abschluss`).
        laufend = forschung.fortschritt(stand, self.state.spielsekunden)
        # Eine Quelle fuer Sperren, Begruendungen und Freischaltungen (forschungspfad).
        _bib = gebaeude_wirkung.bibliothek_stufe(self.state.settlements)
        _stufen = {k: v.level for k, v in self.state.research.items()}
        for key, r in self.state.research.items():
            frame = tk.Frame(self.content, bg=self.skin["panel"])
            frame.pack(fill=tk.X, padx=10, pady=2)
            # M-6 (Befund aus Register 145, gemessen): die Zeile wurde von LINKS nach rechts gepackt -
            # Name, Stufe, Beschreibung zuerst, Knopf und Sperrgrund danach. Bei langen Beschreibungen
            # schob der Text die rechte Seite aus dem Fenster (14 von 14 Zeilen brauchten 1076 bis 1903
            # px bei 1052 px Inhaltsbreite). Jetzt wird die RECHTE Seite zuerst gepackt - sie behaelt
            # ihren Platz -, und die Beschreibung bekommt eine Umbruchbreite statt die Zeile zu sprengen.
            zustand = laufend.get(key) or {}
            rechts = []                                    # was rechts steht, in Anzeigereihenfolge
            if zustand.get("laufend"):
                rest = float(zustand.get("reststunden") or 0.0)
                rechts.append(tk.Label(frame,
                                       text=f"läuft auf Stufe {zustand.get('zielstufe')} · noch {rest:.1f} h",
                                       fg=self.skin["gold"], bg=self.skin["panel"]))
            elif r.level < r.max_level:
                # Vorgabe Daniel 05.10.2026: eine Forschung ist erst startbar, wenn die
                # Voraussetzungen aus data/research.json erfuellt sind — der Knopf ist sonst
                # gesperrt, der Grund steht mit Soll/Ist daneben, und was die Forschung
                # freischaltet, steht gleich mit dabei (Quelle: `forschungspfad`).
                _frei, _warum = forschungspfad.erfuellt(key, _stufen, _bib)
                kosten = forschung.naechste_kosten(stand, key)
                _knopf = tk.Button(frame, text=f"Forschen ({int(kosten.get('holz', 0))} Holz)",
                                   command=lambda k=key: self._start_research(k), bg="#3e2723",
                                   fg=self.skin["gold"])
                if not _frei:                              # gesperrt: Knopf bleibt, aber grau
                    _knopf.config(state=tk.DISABLED, disabledforeground="#8a8a8a")
                rechts.append(_knopf)                      # der Knopf steht ganz rechts
                if _frei:
                    _was = forschungspfad.schaltet_frei(key)
                    _teile = []
                    if _was.get("waren"):
                        _teile.append("Waren: " + ", ".join(_was["waren"]))
                    # Einheiten, die diese Forschung UNMITTELBAR verlangen (data/units.json,
                    # z. B. Gauner: Heimlichkeit 1). Über den Warenweg allein kommen sie nicht
                    # vor — das hat das Kinder-Modul als Grenze gemeldet (05.10.2026).
                    _direkt = sorted(n for n, e in einheiten.alle().items()
                                     if str((e.get("voraussetzung") or {}).get("forschung") or "") == key)
                    if _direkt:
                        _teile.append("Einheiten: " + ", ".join(_direkt))
                    if _teile:
                        rechts.append(tk.Label(frame, text="schaltet frei — " + " · ".join(_teile),
                                               fg="#8FBF7F", bg=self.skin["panel"],
                                               wraplength=300, justify=tk.LEFT))
                else:
                    rechts.append(tk.Label(frame, text=f"gesperrt: {_warum}", fg="#FDBA74",
                                           bg=self.skin["panel"], wraplength=300, justify=tk.LEFT))
            for _w in rechts:                              # ZUERST die rechte Seite
                _w.pack(side=tk.RIGHT, padx=5)
            tk.Label(frame, text=r.name, fg=self.skin["text"], bg=self.skin["panel"], width=15, anchor=tk.W).pack(side=tk.LEFT, padx=5)
            tk.Label(frame, text=f"Stufe {r.level}/{r.max_level}", fg="#DAA520", bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
            tk.Label(frame, text=r.effect, fg="#C0C0C0", bg=self.skin["panel"],
                     wraplength=380, justify=tk.LEFT).pack(side=tk.LEFT, padx=5)

    def _start_research(self, key: str):
        """Forschung in DIESEM Ort starten — ueber den Kern (`forschung_start`).

        Oekonomie-Paket, Schritt 9, Teil 6 (Rest; Entwurf Z. 779: „lokale Bibliothek, lokale
        Mittel, globales Wissen"). Der Kern prueft: kein zweiter Auftrag in derselben Bibliothek,
        bekanntes Gebiet, die Voraussetzungen aus `forschungspfad` (mit der Bibliotheksstufe DIESES
        Ortes) — und **die Rohstoffe im lokalen Lager**. Abgelehnt wird VOR jeder Aenderung.

        Die Stufe steigt **erst nach Ablauf** der Zeit, gebucht von `tick` ueber
        `spieloekonomie.forschung_abschluss` (Dauer = Stufe zum Quadrat in Stunden, Handbuch
        S. 12/13) — nicht im selben Klick. Der reichsweite Altpfad (`forschung_fortschreiben`) ist
        weg: er haette dieselbe Stufe ein zweites Mal zahlen lassen.
        """
        r = self.state.research.get(key)
        if r is None:
            self._log(f"Unbekanntes Forschungsgebiet: {key}.")
            return False
        ort = self.state.aktive_siedlung()
        if ort is None:
            self._log(f"{r.name} braucht eine Bibliothek auf einer Siedlungskarte — es gibt noch "
                      f"keine Siedlung.")
            return False
        _sperre = self._nahrungssperre(ort)
        if _sperre:
            self._log(_sperre)
            return False
        # Grundbedingung ZUERST und mit Namen (wie bei der Ausbildung): ohne Bibliothek VOR ORT
        # gibt es keinen Ort, an dem geforscht wird.
        if gebaeude_wirkung.bibliothek_stufe([ort]) <= 0:
            self._log(f"{r.name} braucht eine Bibliothek in dieser Siedlung — noch nicht gebaut.")
            return False
        if int(r.level) >= int(r.max_level):
            self._log(f"{r.name} ist mit Stufe {r.level} bereits ausgeforscht.")
            return False
        wissen = {k: int(v.level) for k, v in self.state.research.items()}
        weitere = [asdict(s) for s in self.state.settlements if s.id != ort.id]
        try:
            neu = spieloekonomie.forschung_start(asdict(ort), key, wissen,
                                                 self.state.spielsekunden, weitere)
        except ValueError as fehler:
            meldung = f"Forschung nicht gestartet: {fehler}"
            self._log(meldung)
            self.state.messages.append({"text": f"{r.name} gesperrt — {fehler}",
                                        "type": "forschung"})
            return False
        self.state._ort_uebernehmen(ort.id, neu)
        _a = neu.get("forschungsauftrag") or {}
        self._log(f"{r.name} laeuft jetzt in {ort.name} — Stufe {_a.get('zielstufe')} nach "
                  f"{float(_a.get('dauer_stunden') or 0.0):g} h Spielzeit (Handbuch S. 12).")
        if hasattr(self, "content"):
            self._render_view()
        return True

    def _render_barracks(self):
        """Kaserne = Truppen der Kriegerakademie (Vorgabe Daniel 30.10.2026).

        Daniel: "Truppen werden in der Kriegerakademie ausgebildet" — Karren und
        Belagerungswaffen gehoeren in den Stellmacher, Kundschafter in die Diebesgilde.
        Bis zum 30.10.2026 listete diese Ansicht ALLE 28 Einheiten; deshalb standen Handkarren
        in der Truppenausbildung, obwohl `data/units.json` sie dem Stellmacher zuordnet.
        """
        self._render_ausbildung("Kriegerakademie", "Kaserne")

    def _render_stellmacher(self):
        """Stellmacher: Karren und Belagerungswaffen. Menuepunkt erst ab gebautem Stellmacher."""
        self._render_ausbildung("Stellmacher", "Stellmacher")

    def _render_diebesgilde(self):
        """Diebesgilde: Kundschafter. Menuepunkt erst ab gebauter Diebesgilde."""
        self._render_ausbildung("Diebesgilde", "Diebesgilde")
        self._spionage_abschnitt()          # B-5: von hier aus fremde Doerfer ausspionieren

    def _spionage_abschnitt(self):
        """Spionage starten (B-5, 02.11.2026) - der Einstieg im Fenster.

        Steht in der Diebesgilde, weil die Kundschafter von dort kommen. Gezeigt wird nur, was
        OHNE Spionage offen ist: Name, Position, Fraktion und Hauptdorf eines fremden Dorfes.
        Wallstufe, Taktik, Truppen und Vorraete kommen erst mit dem Bericht ins Postfach - und
        der entsteht erst durch einen Auftrag. Der Knopf nennt vorher, wie viel Aufklaerung die
        Truppe im Dorf hat und welche Schwelle sie schafft.
        """
        self._kasten_label("Spionage", ("Blackletter", 18, "bold"), self.skin["gold"],
                           innen=14, pady=6)
        ort = self.state.aktive_siedlung()                                 # Ausgangsdorf
        if ort is None:                                                    # ohne Siedlung kein Auftrag
            self._kasten_label("Ohne eigene Siedlung gibt es nichts zu entsenden.",
                               ("TkDefaultFont", 10), self.skin["text"], innen=14, pady=5)
            return
        kundschafter = {n: int(a) for n, a in (getattr(ort, "einheiten", None) or {}).items()
                        if einheiten.ist_kundschafter(n) and int(a) > 0}   # die Spionageeinheiten
        if kundschafter:                                                   # Truppe vorhanden
            wert = spionage.aufklaerungswert(kundschafter)                 # ihre Aufklaerung
            text = ("Im Dorf: " + ", ".join("%d %s" % (a, n) for n, a in sorted(kundschafter.items()))
                    + " - Aufklaerung %d." % wert)
        else:                                                              # keine Kundschafter
            text = "Keine Kundschafter im Dorf - erst oben ausbilden lassen."
        self._kasten_label(text, ("TkDefaultFont", 10), self.skin["text"],
                           breite=770, innen=14, pady=5, umbruch=740)
        grenzen = spionage.schwellen()                                     # Schwelle je Berichtsteil
        self._kasten_label(
            ("Ein Bericht zeigt Truppen ab %d, Vorraete ab %d, Wall ab %d, Karte ab %d "
             "und die Taktik ab %d Aufklaerung. Reicht sie nicht fuer den Wall, prallt "
             "der Auftrag ab - mit Verlusten."
             % (grenzen["truppen"], grenzen["vorraete"], grenzen["wall"],
                grenzen["karte"], grenzen["taktik"])),
            ("TkDefaultFont", 9), "#C0C0C0", breite=770, innen=14, pady=5, umbruch=740)
        for bot in self.state.bots:                                        # je Bot seine Doerfer
            for dorf in bot_doerfer_sicherstellen(bot):
                zeile = tk.Frame(self.content, bg=self.skin["panel"])       # eine Zeile je Dorf
                zeile.pack(fill=tk.X, padx=10, pady=1)
                tk.Label(zeile, text="%s - %s (%d/%d)%s" % (
                             bot.name, dorf.name, int(dorf.x), int(dorf.y),
                             " Hauptdorf" if dorf.hauptdorf else ""),
                         fg=self.skin["text"], bg=self.skin["panel"], anchor=tk.W,
                         wraplength=560, justify=tk.LEFT).pack(side=tk.LEFT, padx=6)
                tk.Button(zeile, text="Ausspionieren",
                          command=lambda b=bot, d=dorf: self._spionage_klick(b, d),
                          bg=self.skin["button"], fg=self.skin["gold"], relief=tk.FLAT,
                          padx=6, pady=1).pack(side=tk.RIGHT, padx=6)

    def _spionage_klick(self, bot, dorf):
        """Der Knopf: einen Spionageauftrag starten und das Ergebnis als Nachricht zeigen."""
        ok, meldung = self.state.spionage_starten(bot, str(dorf.name))      # Kern entscheidet
        self.state.messages.append({"text": meldung, "type": "auftrag" if ok else "kampf"})
        self._log(meldung)                                                 # Statuszeile
        self._render_view()                                                # Ansicht neu zeichnen
        return ok

    def _render_ausbildung(self, staette: str, titel: str):
        # B-6 (02.11.2026, Vorgabe Daniel): das Bild der Werkstatt ist der HINTERGRUND der Ansicht
        # (Kaserne -> Kriegerakademie, Stellmacher, Diebesgilde) - Kennung ueber `gelaende`, nie getippt.
        if self._ansicht_hintergrund(gelaende.finde_gebaeude(staette)) is None:   # kein Bild
            self._gebaeude_kopf(gelaende.finde_gebaeude(staette))                 # dann der alte Kopf
        # M-2 (Daniel 02.11.2026, Fragenrunde): die Kastenoptik aus Dorfzentrum und Forschung gilt
        # jetzt auch in den drei Ausbildungsstaetten - Titel und Einleitung als weiche Felder, damit
        # das Gebaeudemotiv zwischen den Bloecken sichtbar bleibt (vorher harte Balken ueber die
        # volle Breite). Die Zahlen kommen weiter aus `data/gebaeude_motive.json`.
        self._kasten_label(titel, ("Blackletter", 20, "bold"), self.skin["gold"], innen=14, pady=6)

        self._kasten_label(
            f"Ausgebildet wird auf der Siedlungskarte (W4b-5). Hier stehen "
            f"ausschliesslich die Einheiten der {staette}; die Stufe des "
            "Gebaeudes bestimmt das Tempo. Steht die Stätte nicht, fehlt "
            "die Schaltfläche und der Grund steht daneben.",
            ("TkDefaultFont", 9), "#C0C0C0", breite=810, innen=14, pady=5, umbruch=780)
        self._ausbildung_warteschlange_zeichnen(staette)
        # A-6 (Daniels Spielbericht 31.10.2026): sechs gescheiterte Ausbildungen, weil die
        # Siedlerreserve unbemerkt auf 3,5 gefallen war. Hier steht sie VOR der ersten Einheit -
        # mit der Zahl, die noch geht, und dem Nachwuchs je Spielstunde.
        self._siedler_warnung_zeichnen()
        _angezeigt = 0
        for key, u in self.state.units.items():
            if str((einheiten.alle().get(key) or {}).get("gebaeude") or "") != staette:
                continue
            _angezeigt += 1
            frame = tk.Frame(self.content, bg=self.skin["panel"])
            frame.pack(fill=tk.X, padx=10, pady=2)
            _bild = self._lade_icon(UNIT_ICONS.get(key, ""))
            if _bild is not None:
                tk.Label(frame, image=_bild, bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
            tk.Label(frame, text=u.name, fg=self.skin["text"], bg=self.skin["panel"], width=15, anchor=tk.W).pack(side=tk.LEFT, padx=5)
            _w = einheiten.alle()[key]["werte"]
            if einheiten.ist_transport(key):
                info = f"Ladung {einheiten.ladung(key)} / GS {einheiten.geschwindigkeit(key)}"
            elif einheiten.ist_belagerung(key):
                _lo, _hi = einheiten.mauer_schaden(key)
                info = f"Schlagkraft {einheiten.schlagkraft(key)} / Mauerschaden {_lo}-{_hi}"
            else:
                info = (f"LE {_w.get('LE')} / AT {_w.get('AT')} / PA {_w.get('PA')} / "
                        f"TP {_w.get('TP_min')}-{_w.get('TP_max')} / SK {_w.get('SK')}")
            tk.Label(frame, text=info, fg="#DAA520", bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
            # Teil 6c: seit die Einheiten VOR ORT entstehen (`ort_tick`), muss die Kaserne BEIDE
            # Zahlen zeigen — sonst stuende hier 0, waehrend im Ortslager Einheiten liegen.
            _ort_k = self.state.aktive_siedlung()
            _lokal_k = int((getattr(_ort_k, "einheiten", None) or {}).get(key, 0)) if _ort_k else 0
            tk.Label(frame, text=f"Anzahl: {_lokal_k} vor Ort · Reich: {u.count}",
                     fg="#C0C0C0", bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
            # W4b-5: Die Ausbildungsstätte steht auf der Siedlungskarte (data/units.json nennt sie
            # je Einheit). Fehlt sie, gibt es keine Schaltfläche — sondern den ehrlichen Grund.
            _da, _staette, _stufe = gebaeude_wirkung.ausbildungsstaette(self.state.settlements, key)
            if _da:
                # Vorgabe Daniel 05.10.2026: ohne Forschung UND ohne Ausrüstung wird nicht
                # ausgebildet — der Knopf ist dann gesperrt und der Grund steht daneben.
                _frei, _grund = self._ausbildungs_hindernis(key)
                if _frei:
                    # A-1 (Daniels Spielbericht 31.10.2026): eine MENGE statt 200 Einzelklicks.
                    # Die Leiste steht unter der Zeile, damit jeder Knopf Platz hat.
                    self._ausbilden_block(key, _staette, _stufe)
                    if ausruestung.bedarf(key):
                        # Teil 6c: die Ausruestung wird VOR ORT verbraucht — also wird auch die
                        # Anzeige gegen das Ortslager gerechnet (dieselbe Quelle wie die Ausbildung).
                        tk.Label(frame, text="Waren: " + ausruestung.bestand_text(
                            ausruestung.fehlende(key, (getattr(_ort_k, "waren", None) or {})
                                                 if _ort_k else self.state.waren)),
                            fg="#C0C0C0", bg=self.skin["panel"]).pack(side=tk.RIGHT, padx=5)
                else:
                    _knopf = tk.Button(frame, text="Ausbilden (gesperrt)", bg="#4a4a4a",
                                       fg="#9e9e9e", state=tk.DISABLED,
                                       disabledforeground="#8a8a8a")
                    _knopf.pack(side=tk.RIGHT, padx=5)
                    tk.Label(frame, text=_grund, fg="#FDBA74", bg=self.skin["panel"],
                             wraplength=380, justify=tk.LEFT).pack(side=tk.RIGHT, padx=5)
            else:
                _fehlt = gelaende.gebaeude_name(_staette) if _staette else "Ausbildungsstätte unbekannt"
                tk.Label(frame, text=f"braucht {_fehlt}", fg="#e53935",
                         bg=self.skin["panel"]).pack(side=tk.RIGHT, padx=5)
        if _angezeigt == 0:
            self._kasten_label(f"Keine Einheit wird in der {staette} ausgebildet.",
                               ("TkDefaultFont", 10), "#FDBA74", innen=14, pady=6)

    def _siedler_warnung_zeichnen(self) -> None:
        """A-6: die freie Siedlerreserve des Ortes sichtbar machen, bevor sie aufgebraucht ist.

        Daniels Spielbericht 31.10.2026: nach 44 Bauten standen 3,5 Siedler, danach **sechs**
        gescheiterte Ausbildungen ("Freie Siedler fehlen vor Ort") - niemand hatte ihn vorher
        gewarnt. Seit seiner Entscheidung (Frage 5 = B) binden Bauten keine Siedler mehr, Siedler
        gehen nur noch bei der Ausbildung weg; deshalb steht die Warnung hier und nicht am Bau.
        Die Zahlen kommen aus `spieloekonomie.siedler_reserve` (dieselbe Quelle wie `bevoelkerung`).
        """
        ort = self.state.aktive_siedlung()
        if ort is None or not hasattr(self, "content"):
            return
        try:
            reserve = spieloekonomie.siedler_reserve(asdict(ort), self.state.forschungs_stufen())
        except (AttributeError, KeyError, TypeError, ValueError):
            return
        _farbe = "#FDBA74" if reserve["warnung"] else "#C0C0C0"
        _einheit, _je = reserve["guenstigste"]
        _noch = reserve["moeglich"].get(_einheit, -1) if _einheit else -1
        _noch_text = (f" · es gehen noch {_noch} × {_einheit}" if _noch >= 0 and _einheit
                      else "")
        # M-2: die Warnung liegt als weiches Feld auf dem Bild statt in einem harten Balken.
        self._kasten_label(
            (f"Freie Siedler: {reserve['frei']:.1f} von {reserve['grenze']} · "
             f"Nachwuchs {reserve['zuwachs_stunde']:.1f} je Spielstunde"
             f"{_noch_text} · "
             f"Bauten binden keine Siedler (Entscheidung 31.10.2026)"),
            ("Arial", 9), self.skin["text"], breite=830, innen=12, pady=4, umbruch=800)
        if reserve["text"]:
            self._kasten_label("⚠ " + reserve["text"], ("Arial", 9, "bold"), _farbe,
                               breite=830, innen=12, pady=4, umbruch=800)

    def _ausbildung_warteschlange_zeichnen(self, staette: str):
        """Die Warteschlange der Ausbildungsstätte sichtbar machen (Daniels Spieltest 31.10.2026).

        Vorher sah der Spieler nur den Knopf „Ausbilden" und danach nichts mehr — die Einheiten
        wirkten „unsichtbar produziert". Hier steht jetzt: was läuft, was wartet, wie lange jeder
        Auftrag noch braucht und wie lange die GESAMTE Schlange dauert (Spielzeit und Echtzeit
        bei ×180). Die Reihenfolge ist echt sequenziell: `ausbildung_start` beginnt jeden neuen
        Auftrag erst am Ende des letzten Auftrags derselben Werkstatt.
        """
        ort = self.state.aktive_siedlung()
        if ort is None:
            return

        def _zeit(sekunden: float) -> str:
            stunden = max(0.0, sekunden) / 3600.0
            echt = int(round(stunden * 20))      # 1 Spielstunde = 20 echte Sekunden bei x180
            minuten, rest = divmod(echt, 60)
            return f"{stunden:.1f} Spielstunden (real {minuten}:{rest:02d})"

        try:
            uebersicht = spieloekonomie.ausbildung_uebersicht(asdict(ort), self.state.spielsekunden)
        except Exception:                                # noqa: BLE001
            return
        # M-4 (Vorgabe Daniel 02.11.2026: "dann die uebrigen Textfelder", "stueck fuer stueck"): der
        # Kopf der Warteschlange und ihre zwei Hinweiszeilen liegen als weiche Felder auf dem
        # Gebaeudemotiv. Die Auftragszeilen selbst bleiben ein DECKENDER Block - sie sind eine
        # Tabelle, und ein Bild unter jeder Zeile macht die Zeilen unlesbar (dieselbe Trennung wie
        # in M-2 fuer die Einheitentabelle).
        self._kasten_label(
            (f"In Arbeit: {uebersicht['anzahl']} Auftrag/Aufträge · "
             f"insgesamt noch {_zeit(uebersicht['gesamt_rest_sekunden'])}"),
            ("Arial", 9, "bold"), self.skin["gold"], innen=12, pady=3)
        if not uebersicht["auftraege"]:
            self._kasten_label("Keine Aufträge in Arbeit.", ("TkDefaultFont", 10), "#C0C0C0",
                               innen=14, pady=5)
        # A-1: Mengen erzeugen viele Einzelauftraege (bis 200). Gezeichnet werden GRUPPEN
        # aufeinanderfolgender gleicher Auftraege ("1.-12. Krieger"), damit die Uebersicht bei
        # einer Mengenausbildung nicht zur Litanei wird. Gestrichen wird weiter je Auftrag, weil
        # der Kern je Auftrag streicht (keine Erstattung).
        gruppen = []
        for auftrag in uebersicht["auftraege"]:
            schluessel = (auftrag["einheit"], auftrag["gebaeude"], auftrag["stufe"],
                          bool(auftrag["laufend"]))
            if gruppen and gruppen[-1]["schluessel"] == schluessel:
                gruppen[-1]["bis"] = auftrag["platz"]
                gruppen[-1]["anzahl"] += 1
                gruppen[-1]["rest_sekunden"] = auftrag["rest_sekunden"]
            else:
                gruppen.append({"schluessel": schluessel, "von": auftrag["platz"],
                                "bis": auftrag["platz"], "anzahl": 1,
                                "einheit": auftrag["einheit"], "gebaeude": auftrag["gebaeude"],
                                "stufe": auftrag["stufe"], "laufend": bool(auftrag["laufend"]),
                                "rest_sekunden": auftrag["rest_sekunden"]})
        rahmen = None                                    # der deckende Block fuer die Auftragszeilen
        if gruppen:                                      # nur wenn Zeilen da sind (sonst kein leerer Balken)
            rahmen = tk.Frame(self.content, bg=self.skin["panel"])
            rahmen.pack(fill=tk.X, padx=10, pady=(4, 2))
        for gruppe in gruppen:
            zeile = tk.Frame(rahmen, bg=self.skin["panel"])
            zeile.pack(fill=tk.X, padx=6, pady=1)
            _platz = (f"{gruppe['von']}. {gruppe['einheit']}" if gruppe["anzahl"] == 1
                      else f"{gruppe['von']}.-{gruppe['bis']}. {gruppe['anzahl']} × {gruppe['einheit']}")
            tk.Label(zeile,
                     text=f"{_platz} "
                          f"({gelaende.gebaeude_name(gruppe['gebaeude'])} Stufe {gruppe['stufe']}) "
                          f"— {'läuft' if gruppe['laufend'] else 'wartet'}",
                     fg=self.skin["text"], bg=self.skin["panel"]).pack(side=tk.LEFT)
            tk.Label(zeile, text=f"fertig in {_zeit(gruppe['rest_sekunden'])}",
                     fg=("#DAA520" if gruppe["laufend"] else "#C0C0C0"),
                     bg=self.skin["panel"]).pack(side=tk.LEFT, padx=8)
            if not gruppe["laufend"]:
                tk.Button(zeile,
                          text=("Streichen (ohne Erstattung)" if gruppe["anzahl"] == 1
                                else f"Letzten streichen (Platz {gruppe['bis']})"),
                          command=lambda p=gruppe["bis"]: self._ausbildung_streichen(p),
                          bg="#3e2723", fg=self.skin["gold"]).pack(side=tk.RIGHT, padx=4)
        # M-4: die Erklaerung zur Reihenfolge ist die zweite Hinweiszeile - auch sie liegt jetzt
        # als weiches Feld auf dem Bild statt als harter Balken ueber die volle Breite.
        self._kasten_label(
            "Reihenfolge: nacheinander. Streichen ist möglich, solange ein Auftrag "
            "wartet — eine Erstattung gibt es nicht, weil die Originale dazu nichts regeln.",
            ("TkDefaultFont", 9), "#8a8a8a", breite=810, innen=12, pady=4, umbruch=780)

    def _ausbildung_streichen(self, platz: int) -> bool:
        """Einen wartenden Ausbildungsauftrag streichen (ohne Erstattung, siehe Kern-Docstring)."""
        ort = self.state.aktive_siedlung()
        if ort is None:
            return False
        ergebnis = spieloekonomie.ausbildung_abbrechen(asdict(ort), platz, self.state.spielsekunden)
        if not ergebnis.get("ok"):
            meldung = "Streichen nicht möglich: " + str(ergebnis.get("grund") or "")
            self._log(meldung)
            self.state.messages.append({"text": meldung, "type": "ausbildung"})
            self._render_view()
            return False
        ort.ausbildung = list(ergebnis.get("ausbildung") or [])
        meldung = (f"{ergebnis.get('einheit')} aus der Warteschlange gestrichen — "
                   f"keine Erstattung (die Originale regeln das nicht).")
        self._log(meldung)
        self.state.messages.append({"text": meldung, "type": "ausbildung"})
        self._render_view()
        return True

    def _ausbildungs_hindernis(self, key: str) -> tuple:
        """Was der Ausbildung im Weg steht — Forschung oder Ausrüstung (Vorgabe Daniel 05.10.2026).

        Rückgabe ``(True, "")``, wenn nichts fehlt, sonst ``(False, Grund)``. Die Begründung nennt
        das Fehlende mit Soll/Ist. EINE Quelle für Ansicht und Ausbildung: die Forschungsstufe aus
        ``data/units.json`` ('voraussetzung') und die Waren aus ``ausruestung``.
        """
        rohdaten = einheiten.alle().get(key) or {}
        vor = rohdaten.get("voraussetzung") or {}
        if vor.get("forschung"):
            f_name = str(vor["forschung"])
            f_stufe = int(vor.get("stufe") or 0)
            eintrag = self.state.research.get(f_name)
            erreicht = int(eintrag.level) if eintrag is not None else 0
            if erreicht < f_stufe:
                return False, f"braucht {f_name} Stufe {f_stufe} (erreicht: {erreicht})"
        # Teil 6c: die Ausruestung liegt VOR ORT (`Settlement.waren`) — dieselbe Quelle, aus der
        # `ausbildung_start` sie verbraucht. Oben, ueber dem Siedlungslager, zaehlt der
        # Reichsbestaand als Uebergang (solange es keine Siedlung gibt, gibt es kein Ortslager).
        _ort_lager = self.state.aktive_siedlung()
        lager = (dict(getattr(_ort_lager, "waren", None) or {}) if _ort_lager is not None
                 else dict(self.state.waren or {}))
        fehlt = ausruestung.fehlende(key, lager)
        if fehlt:
            # Soll/Ist je Ware — so verlangt es das astra-Gutachten. `ausruestung.fehlende`
            # liefert nur die Fehlmenge; Soll = Ist + Fehlmenge (Befund des Kinder-Moduls vom
            # 05.10.2026: `bestand_text` zeigt bei reinen Zahlen nur die Fehlmenge).
            teile = []
            for ware, menge in sorted(fehlt.items()):
                ist = int(lager.get(ware, 0))
                teile.append(f"{ware} {ist}/{ist + int(menge)}")
            return False, ("braucht Ausrüstung — " + " · ".join(teile) +
                           " (Werkstätten: Schmiede, Bogner, Nähstube)")
        return True, ""

    def _menge_schritt(self, var, delta: int, hoechst: int, bei_aenderung=None) -> int:
        """Eine Menge um `delta` verschieben und in 0..hoechst halten (A-1, Schrittknoepfe)."""
        try:
            wert = int(float(str(var.get()).replace(",", ".") or 0))
        except (TypeError, ValueError):
            wert = 1
        wert = max(0, min(max(0, int(hoechst)), wert + int(delta)))
        var.set(str(wert))
        if bei_aenderung is not None:
            bei_aenderung()
        return wert

    def _menge_lesen(self, var, hoechst: int) -> int:
        """Die Menge aus dem Zahlfeld - nie negativ, nie ueber der Grenze, nie ein Absturz."""
        try:
            wert = int(float(str(var.get()).replace(",", ".") or 0))
        except (TypeError, ValueError):
            wert = 0
        return max(0, min(max(0, int(hoechst)), wert))

    def _mengen_feld(self, eltern, var, hoechst: int, bei_aenderung) -> None:
        """Zahlfeld + Schrittknoepfe -/+ + Schieberegler fuer EINE Menge (A-1).

        Daniel im Spielbericht: "200x klicken" ist keine Bedienung. Alle drei Wege schreiben in
        DIESELBE Variable; `bei_aenderung` zeichnet die Vorschau neu. Der Deckel ist derselbe wie
        im Kern (`spieloekonomie.MENGEN_HOECHSTMENGE`) - die Anzeige kann nicht mehr versprechen,
        als der Start annimmt.
        """
        tk.Entry(eltern, textvariable=var, width=5, bg=self.skin["panel"],
                 fg=self.skin["text"], insertbackground="#F5F5DC",
                 justify=tk.CENTER).pack(side=tk.LEFT, padx=(4, 2))
        tk.Button(eltern, text="−", width=2, bg="#3e2723", fg=self.skin["gold"],
                  command=lambda: self._menge_schritt(var, -1, hoechst, bei_aenderung)
                  ).pack(side=tk.LEFT)
        tk.Button(eltern, text="+", width=2, bg="#3e2723", fg=self.skin["gold"],
                  command=lambda: self._menge_schritt(var, +1, hoechst, bei_aenderung)
                  ).pack(side=tk.LEFT, padx=(0, 6))
        tk.Scale(eltern, from_=0, to=max(1, int(hoechst)), orient=tk.HORIZONTAL, length=150,
                 showvalue=0, bg=self.skin["panel"], fg=self.skin["text"],
                 troughcolor="#2a1c14", highlightthickness=0,
                 command=lambda wert: (var.set(str(int(float(wert)))), bei_aenderung())
                 ).pack(side=tk.LEFT, padx=(0, 6))

    @staticmethod
    def _ausbildung_engpass(grenzen: dict) -> str:
        """Welche Grenze zuerst greift - fuer die Vorschau (z. B. "siedler")."""
        einzel = dict(grenzen.get("grenzen") or {})
        if not einzel:
            return ""
        return min(einzel.items(), key=lambda kv: kv[1])[0]

    def _ausbilden_block(self, key: str, staette: str, stufe: int) -> None:
        """Die Mengeneingabe unter einer Einheit der Ausbildungsstaette (A-1).

        Zeigt Kosten, Siedler und Ausruestung fuer die GEWAEHLTE Menge und dieselbe Zahl, die der
        Kern annimmt ("davon bezahlbar: N") - beide kommen aus `spieloekonomie.ausbildung_grenzen`.
        """
        ort = self.state.aktive_siedlung()
        if ort is None or not hasattr(self, "content"):
            return
        try:
            grenzen = spieloekonomie.ausbildung_grenzen(asdict(ort), key,
                                                        self.state.forschungs_stufen())
        except (ValueError, KeyError, TypeError):
            return
        moeglich = int(grenzen.get("moeglich") or 0)
        hoechst = max(1, min(spieloekonomie.MENGEN_HOECHSTMENGE, max(moeglich, 1)))
        block = tk.Frame(self.content, bg=self.skin["bg"])
        block.pack(fill=tk.X, padx=34, pady=(0, 8))
        var = tk.StringVar(value="1")
        vorschau = tk.Label(block, text="", fg="#C8A165", bg=self.skin["bg"],
                            font=("Arial", 9), anchor=tk.W, justify=tk.LEFT, wraplength=840)
        vorschau.pack(anchor=tk.W, pady=(2, 0))
        knopf = tk.Button(block, text="Ausbilden", bg="#3e2723", fg=self.skin["gold"],
                          command=lambda: self._train_unit_menge(
                              key, self._menge_lesen(var, spieloekonomie.MENGEN_HOECHSTMENGE)))

        def vorschau_text() -> tuple:
            n = self._menge_lesen(var, spieloekonomie.MENGEN_HOECHSTMENGE)
            teile = []
            for rohstoff, je in sorted((grenzen.get("kosten_je") or {}).items()):
                teile.append(f"{float(je) * n:g} {rohstoff}")
            if grenzen.get("siedler_je"):
                teile.append(f"{int(grenzen['siedler_je']) * n} Siedler")
            for ware in sorted(grenzen.get("ausruestung_je") or {}):
                teile.append(f"{n} {ware}")
            kosten = " · ".join(teile) if teile else "keine Kosten"
            text = f"{n} × {key} = {kosten} · davon bezahlbar: {moeglich}"
            if n > moeglich:
                engpass = self._ausbildung_engpass(grenzen)
                text += (f" — zu viel: jetzt gehen nur {moeglich}"
                         + (f" ({engpass})" if engpass else "") + ".")
            return n, text

        def zeichnen() -> None:
            n, text = vorschau_text()
            vorschau.config(text=text, fg="#FDBA74" if n > moeglich else "#C8A165")
            knopf.config(text=f"Ausbilden ({n})",
                         state=(tk.DISABLED if moeglich < 1 else tk.NORMAL),
                         disabledforeground="#8a8a8a")

        tk.Label(block, text=f"Menge (1-{hoechst}):", fg="#C0C0C0", bg=self.skin["bg"],
                 font=("Arial", 9)).pack(side=tk.LEFT)
        self._mengen_feld(block, var, hoechst, zeichnen)
        knopf.pack(side=tk.LEFT, padx=(0, 6))
        var.set("1" if moeglich >= 1 else "0")
        zeichnen()

    def _train_unit_menge(self, key: str, menge: int) -> bool:
        """`menge` Einheiten in DIESEM Ort ausbilden - EIN Vorgang, ueber den Kern (A-1).

        Die Pruefungen des Kerns (`ausbildung_grenzen` + `ausbildung_start_menge`) gelten
        unveraendert; die Meldung nennt die TATSAECHLICH gestartete Menge, nicht die gewuenschte.
        """
        try:
            menge = int(menge)
        except (TypeError, ValueError):
            menge = 0
        if menge < 1:
            self._log("Menge 0: es wird nichts ausgebildet. Bitte eine Zahl ab 1 waehlen.")
            return False
        u = self.state.units[key]
        ort = self.state.aktive_siedlung()
        if ort is None:
            _staette = (einheiten.alle().get(key) or {}).get("gebaeude")
            _name = gelaende.gebaeude_name(_staette) if _staette else "Ausbildungsstätte"
            self._log(f"{u.name} braucht {_name} auf einer Siedlungskarte — es gibt noch keine "
                      f"Siedlung.")
            return False
        _sperre = self._nahrungssperre(ort)
        if _sperre:
            self._log(_sperre)
            return False
        _da, _staette, _stufe = gebaeude_wirkung.ausbildungsstaette([ort], key)
        if not _da:
            _name = gelaende.gebaeude_name(_staette) if _staette else "Ausbildungsstätte"
            meldung = f"{u.name} braucht {_name} auf einer Siedlungskarte — noch nicht gebaut."
            self._log(meldung)
            self.state.messages.append({"text": meldung, "type": "ausbildung"})
            self._render_view()
            return False
        levels = {k: int(v.level) for k, v in self.state.research.items()}
        try:
            ergebnis = spieloekonomie.ausbildung_start_menge(asdict(ort), key, levels,
                                                             self.state.spielsekunden, menge)
        except ValueError as fehler:
            grund = str(fehler)
            if "Ausbildungsstätte fehlt vor Ort" in grund:
                _staette = (einheiten.alle().get(key) or {}).get("gebaeude")
                _name = gelaende.gebaeude_name(_staette) if _staette else "Ausbildungsstätte"
                grund = f"es fehlt {_name} in dieser Siedlung"
            meldung = f"{u.name} nicht ausgebildet: {grund}"
            self._log(meldung)
            self.state.messages.append({"text": meldung, "type": "ausbildung"})
            self._render_view()
            return False
        self.state._ort_uebernehmen(ort.id, ergebnis["ort"])
        gestartet = int(ergebnis.get("anzahl") or 0)
        minuten = float(ergebnis.get("rest_sekunden") or 0.0) / 60.0
        meldung = (f"{gestartet} × {u.name} in Ausbildung vor Ort ({ort.name}) — der letzte "
                   f"Auftrag ist in {minuten:.1f} Spielminuten fertig. Die Einheiten entstehen "
                   f"nacheinander im Ortslager.")
        self._log(meldung)
        self.state.messages.append({"text": meldung, "type": "ausbildung"})
        self._render_view()
        return True

    def _train_unit(self, key: str):
        """Eine Einheit in DIESEM Ort ausbilden lassen - die Mengenfassung mit Menge 1 (A-1).

        Der Name bleibt, damit vorhandene Aufrufe und Pruefungen unveraendert weiterlaufen; die
        Logik steht vollstaendig in `_train_unit_menge` (Kern: `ausbildung_start_menge`).
        """
        return self._train_unit_menge(key, 1)

    def _schild_dialog_inhalt(self, fenster):
        """FIX04i: Original-Schildmotiv hinter den Speicher-Nebenfenstern.

        Die Grafik ist dieselbe wie auf dem Start-/Ladebild. Das Motiv wird nicht
        verzerrt oder als neues Artwork dupliziert. Links liegt eine deckende,
        kontrastreiche Bedienflaeche, rechts bleibt das Schild erkennbar.
        Fehlende Grafiken sind kein Grund, das Speichern/Laden zu blockieren.
        """
        fenster.configure(bg="#190a08")
        bild = None
        try:
            pfad = ladebild_pfad()
            if os.path.isfile(pfad):
                bild = tk.PhotoImage(file=pfad, master=fenster)
        except (OSError, tk.TclError):
            pass
        if bild is not None:
            hintergrund = tk.Label(fenster, image=bild, borderwidth=0,
                                  highlightthickness=0, bg="#190a08")
            hintergrund.place(relx=1.0, rely=0.5, anchor=tk.E)
            hintergrund.lower()
            # Tk haelt Grafikobjekte nicht automatisch am Leben.
            fenster._nebelseetal_schild_bild = bild
            fenster._nebelseetal_schild_label = hintergrund
        inhalt = tk.Frame(fenster, bg=self.skin["panel"],
                          highlightbackground="#8c633b", highlightthickness=1)
        inhalt.place(x=12, y=12, relwidth=0.69, relheight=0.94,
                     width=-12, height=-24)
        return inhalt

    def _spielstand_verwaltung(self, bereich: str):
        """FIX04h: Spieler sehen aktive Slots, nie ungefragt geloeschte Archive.

        Archiv-Wiederherstellung liegt in einem getrennten, nur fuer freigegebene
        Admins zugreifbaren Werkzeug. Keine heimlichen Rueckholangebote im Spiel.
        """
        from tkinter import messagebox
        admin_ok = (not ausgabemodus.ist_oeffentliche_testversion() and
                    self._tor_geoeffnet and self._profil == "admin"
                    and self._admin_sitzung_freigegeben and self.state.admin_teststand)
        spieler_ok = (self._tor_geoeffnet and self._profil in (None, "spieler")
                      and not self.state.admin_teststand)
        if (bereich == "admin" and not admin_ok) or (bereich == "spieler" and not spieler_ok):
            return False
        speicherort = (self.slots_ordner if bereich == "spieler" else
                       os.path.dirname(self.admin_tor_pfad))
        fenster = tk.Toplevel(self.root)
        fenster.title("Nebelseetal - Spielstaende verwalten")
        fenster.geometry("980x475" if bereich == "admin" else "980x430")
        fenster.minsize(890, 400)
        inhalt_dialog = self._schild_dialog_inhalt(fenster)
        fenster.transient(self.root)
        fenster.grab_set()
        tk.Label(inhalt_dialog, text="Aktive Spielstaende verwalten", bg=self.skin["panel"],
                 fg=self.skin["gold"], font=("Arial", 14, "bold")).pack(pady=(16, 8))
        tk.Label(inhalt_dialog, bg=self.skin["panel"], fg=self.skin["text"],
                 text="Entfernen legt waehrend der Entwicklung eine private Sicherung ab.\n"
                      "Geloeschte Staende erscheinen hier nicht erneut. Speichern in "
                      "einen belegten Slot ueberschreibt ihn bewusst.",
                 justify=tk.CENTER, wraplength=660).pack(pady=(0, 14))
        inhalt = tk.Frame(inhalt_dialog, bg=self.skin["panel"])
        inhalt.pack(fill=tk.X, padx=18)
        meldung = tk.StringVar(value="")

        def liste_aktualisieren():
            for kind in inhalt.winfo_children():
                kind.destroy()
            nummern = spielstaende.SLOTS if bereich == "spieler" else (None,)
            for n in nummern:
                pfad = (spielstaende.slot_pfad(speicherort, n) if n is not None
                        else spielstaende.admin_pfad(speicherort))
                zeile = tk.Frame(inhalt, bg=self.skin["panel"],
                                 highlightbackground=self.skin["button"],
                                 highlightthickness=1)
                zeile.pack(fill=tk.X, pady=4, ipady=6)
                status = (spielstaende.slot_status(speicherort, n) if n else
                          ("Admin-Teststand: vorhanden" if os.path.isfile(pfad)
                           else "Admin-Teststand: leer"))
                tk.Label(zeile, text=status, anchor=tk.W, padx=12,
                         bg=self.skin["panel"], fg=self.skin["text"],
                         font=("Arial", 10)).pack(side=tk.LEFT, fill=tk.X, expand=True)

                def loeschen(ziel=pfad, slot=n):
                    if not os.path.isfile(ziel):
                        return
                    wort = f"Slot {slot}" if slot else "Admin-Teststand"
                    if not messagebox.askyesno(
                            "Aktiven Spielstand entfernen",
                            f"{wort} aus der aktiven Liste entfernen?\n\n"
                            "Waehrend der Entwicklung wird der Stand vorher privat "
                            "archiviert. Er wird normalen Spielern nicht automatisch "
                            "wieder angeboten.\n\n"
                            "Nicht gespeicherter Spielfortschritt wird nicht uebernommen.",
                            parent=fenster):
                        return
                    ok, info = spielstand_archiv.archiviere(
                        ziel, bereich, "Vom Nutzer in der Spielstandverwaltung entfernt")
                    meldung.set((f"{wort} entfernt und privat gesichert."
                                 if ok else f"Archivieren fehlgeschlagen: {info}"))
                    liste_aktualisieren()

                tk.Button(zeile, text="Loeschen (archivieren)", width=23,
                          state=(tk.NORMAL if os.path.isfile(pfad) else tk.DISABLED),
                          command=loeschen, bg=self.skin["button"],
                          fg=self.skin["gold"]).pack(side=tk.RIGHT, padx=10)
        liste_aktualisieren()
        if admin_ok:
            tk.Button(inhalt_dialog, text="Entwicklerarchiv / Wiederherstellung",
                      command=lambda: self._archiv_wiederherstellung_dialog(
                          "admin", speicherort, fenster, liste_aktualisieren),
                      bg=self.skin["button"], fg=self.skin["gold"]).pack(pady=(11, 2))
            tk.Button(inhalt_dialog, text="Spielerslot-Archive pruefen (Admin)",
                      command=lambda: self._archiv_wiederherstellung_dialog(
                          "spieler", self.slots_ordner, fenster, liste_aktualisieren),
                      bg=self.skin["button"], fg=self.skin["gold"]).pack(pady=(2, 2))
        tk.Label(inhalt_dialog, textvariable=meldung, wraplength=665,
                 bg=self.skin["panel"], fg=self.skin["gold"]).pack(padx=12, pady=(12, 5))
        tk.Button(inhalt_dialog, text="Schliessen", width=18, command=fenster.destroy,
                  bg=self.skin["button"], fg=self.skin["gold"]).pack(pady=(2, 12))
        return True

    def _archiv_wiederherstellung_dialog(self, bereich: str, speicherort: str,
                                          eltern, nachher=None):
        """FIX04h: separater, berechtigter Entwicklerzugang, keine Slot-Verwechslung.

        Normale Spielersitzungen sehen weder Archivliste noch Restore-Aktion.
        Die Funktion kann auch nicht ohne gueltige Admin-Sitzung aufgerufen werden.
        """
        from tkinter import messagebox
        from datetime import datetime
        admin_ok = (not ausgabemodus.ist_oeffentliche_testversion() and
                    self._tor_geoeffnet and self._profil == "admin"
                    and self._admin_sitzung_freigegeben and self.state.admin_teststand)
        if not admin_ok or bereich not in ("spieler", "admin"):
            return False
        eintraege = []
        nummern = spielstaende.SLOTS if bereich == "spieler" else (None,)
        for n in nummern:
            for pfad in spielstand_archiv.archivierte_staende(speicherort, bereich, n):
                zeit = pfad.parent.name[:26]
                try:
                    zeit = datetime.strptime(zeit, "%Y-%m-%d_%H-%M-%S_%f").strftime("%d.%m.%Y %H:%M:%S")
                except ValueError:
                    zeit = "Zeitpunkt unbekannt"
                label = f"{'Slot ' + str(n) if n else 'Admin-Teststand'}  |  {zeit}"
                eintraege.append((label, pfad, n))
        eintraege.sort(key=lambda eintrag: eintrag[1].parent.name, reverse=True)
        dialog = tk.Toplevel(eltern)
        dialog.title("Nebelseetal - Entwicklerarchiv")
        dialog.geometry("980x570")
        dialog.minsize(890, 500)
        inhalt_dialog = self._schild_dialog_inhalt(dialog)
        dialog.transient(eltern)
        dialog.grab_set()
        tk.Label(inhalt_dialog, text="Private Spielstandarchive (Admin)",
                 bg=self.skin["panel"], fg=self.skin["gold"],
                 font=("Arial", 14, "bold")).pack(pady=(16, 8))
        tk.Label(inhalt_dialog, text="Nur fuer Entwicklung und Fehlersuche. Archivierte "
                 "Staende sind kein normales Ladeangebot.\n"
                 "Jeder Eintrag nennt den zugehoerigen Slot; ein leerer Slot ohne "
                 "Archiv hat keinen Wiederherstellen-Eintrag.",
                 justify=tk.CENTER, wraplength=660,
                 bg=self.skin["panel"], fg=self.skin["text"]).pack(pady=(0, 12))
        tk.Label(inhalt_dialog, text=f"Bereich: {'Spielerslots 1-3' if bereich == 'spieler' else 'Admin-Teststand'}",
                 bg=self.skin["panel"], fg=self.skin["gold"]).pack(anchor=tk.W, padx=22)
        liste_rahmen = tk.Frame(inhalt_dialog, bg=self.skin["panel"])
        liste_rahmen.pack(fill=tk.BOTH, expand=True, padx=22, pady=(5, 7))
        liste = tk.Listbox(liste_rahmen, height=10, font=("Arial", 10),
                           bg=self.skin["button"], fg=self.skin["text"],
                           selectbackground="#86572c", selectforeground="#ffffff",
                           exportselection=False)
        rolle = tk.Scrollbar(liste_rahmen, orient=tk.VERTICAL, command=liste.yview)
        liste.configure(yscrollcommand=rolle.set)
        liste.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        rolle.pack(side=tk.RIGHT, fill=tk.Y)
        for label, _, _ in eintraege:
            liste.insert(tk.END, label)
        info = tk.StringVar(value=("Keine archivierten Spielstaende vorhanden."
                                   if not eintraege else "Eintrag auswaehlen, dann bewusst wiederherstellen."))
        tk.Label(inhalt_dialog, textvariable=info, bg=self.skin["panel"],
                 fg=self.skin["gold"], wraplength=660).pack(pady=4)
        dateien, bytes_groesse = spielstand_archiv.archiv_groesse(speicherort)
        hinweis = (f"Archivgroesse: {dateien} Dateien, {bytes_groesse / (1024 * 1024):.1f} MiB. "
                   "Keine automatische Loeschung; Aufbewahrungsregeln vor Release pruefen.")
        if bytes_groesse >= 250 * 1024 * 1024:
            hinweis += " ACHTUNG: Archiv ist ueber 250 MiB gross."
        tk.Label(inhalt_dialog, text=hinweis, bg=self.skin["panel"],
                 fg=self.skin["text"], wraplength=660).pack(pady=(0, 7))

        def zurueck():
            auswahl = liste.curselection()
            if not auswahl:
                info.set("Bitte zuerst einen Archivstand auswaehlen.")
                return
            _, quelle, slot = eintraege[auswahl[0]]
            ziel = (spielstaende.slot_pfad(speicherort, slot) if slot is not None
                    else spielstaende.admin_pfad(speicherort))
            name = f"Slot {slot}" if slot else "Admin-Teststand"
            belegt = os.path.isfile(ziel)
            frage = (f"Archivstand fuer {name} wiederherstellen?\n\n"
                     + ("ACHTUNG: Der aktive Slot wird dabei absichtlich ueberschrieben!"
                        if belegt else "Derzeit ist dieser Slot leer."))
            if not messagebox.askyesno("Entwickler-Wiederherstellung", frage,
                                       parent=dialog):
                return
            ok, text = spielstand_archiv.wiederherstellen(
                str(quelle), ziel, ueberschreiben=belegt)
            info.set((f"{name} wiederhergestellt. Zum Spielen den Stand neu laden."
                      if ok else "Fehler: " + text))
            if ok and callable(nachher):
                nachher()

        unten = tk.Frame(inhalt_dialog, bg=self.skin["panel"])
        unten.pack(pady=(0, 16))
        tk.Button(unten, text="Ausgewaehlten Stand wiederherstellen", command=zurueck,
                  state=(tk.NORMAL if eintraege else tk.DISABLED),
                  bg=self.skin["button"], fg=self.skin["gold"]).pack(side=tk.LEFT, padx=8)
        tk.Button(unten, text="Schliessen", command=dialog.destroy,
                  bg=self.skin["button"], fg=self.skin["gold"]).pack(side=tk.LEFT, padx=8)
        return True

    def _slot_auswahl(self, modus):
        """Drei sichtbar getrennte Slots, ohne automatische Ueberschreibung.

        Der alte savegame.json wird nur beim LADEN gesondert angeboten und nie
        automatisch in einen Slot verschoben oder geloescht.
        """
        if self._profil == "admin" or self.state.admin_teststand:
            return  # keine regulären Slots aus dem Admin-Profil
        from tkinter import messagebox
        fenster = tk.Toplevel(self.root)
        fenster.title("Nebelseetal - Speicherstaende")
        fenster.geometry("980x400")
        fenster.minsize(890, 360)
        inhalt_dialog = self._schild_dialog_inhalt(fenster)
        fenster.transient(self.root)
        fenster.grab_set()
        tk.Label(inhalt_dialog, text=("Spiel speichern" if modus == "save" else "Spiel laden"),
                 bg=self.skin["panel"], fg=self.skin["gold"],
                 font=("Arial", 13, "bold")).pack(padx=18, pady=12)

        def waehle(n):
            pfad = spielstaende.slot_pfad(self.slots_ordner, n)
            if modus == "save":
                if os.path.exists(pfad) and not messagebox.askyesno(
                        "Bestehenden Stand ersetzen?",
                        f"Slot {n} enthaelt bereits einen Spielstand. Wirklich ueberschreiben?",
                        parent=fenster):
                    return
                ok = self.state.save(pfad)
            else:
                # Beim Laden einen FRISCHEN Zustand verwenden: alte Werte und
                # Bots aus dem vorigen Spiel duerfen nicht in den neuen laufen.
                neuer = GameState()
                ok = neuer.load(pfad)
                if ok:
                    self.state = neuer
                    self._admin_sitzung_freigegeben = False
            if ok:
                fenster.destroy()
                self._log(f"Slot {n} {'gespeichert' if modus == 'save' else 'geladen'}.")
                self._build_main_ui()
                self._render_view()
            else:
                messagebox.showwarning("Nicht moeglich", "Aktion nicht moeglich; Spielstand bleibt erhalten.",
                                       parent=fenster)

        for nummer in spielstaende.SLOTS:
            rahmen = tk.Frame(inhalt_dialog, bg=self.skin["panel"])
            rahmen.pack(fill=tk.X, padx=18, pady=4)
            tk.Button(rahmen, text=("Sichern" if modus == "save" else "Laden") + f" #{nummer}",
                      command=lambda n=nummer: waehle(n), width=13,
                      fg=self.skin["gold"], bg=self.skin["button"]).pack(side=tk.RIGHT)
            tk.Label(rahmen, text=spielstaende.slot_status(self.slots_ordner, nummer),
                     fg=self.skin["text"], bg=self.skin["panel"], anchor=tk.W,
                     width=39).pack(side=tk.LEFT)
        # Alte savegame.json bleibt als Datei/Archiv erhalten, aber kein aktiver Ladebutton.
        # Dadurch werden keine veralteten Generator-Karten in die neue Hauptfassung gezogen.
        tk.Button(inhalt_dialog, text="Schliessen", command=fenster.destroy,
                  bg=self.skin["button"], fg=self.skin["gold"]).pack(pady=10)

    def _save(self):
        self._slot_auswahl("save")

    def _load(self):
        self._slot_auswahl("load")

    def _admin_dialog(self):
        """Eigenes Admin-Profil nach dem Grundtor, mit SEPARATEM Admin-Passwort."""
        from tkinter import simpledialog, messagebox
        if ausgabemodus.ist_oeffentliche_testversion():
            return  # Oeffentliche Testversion darf kein Admin-Tor anbieten.
        if not self._tor_geoeffnet or self._profil is not None:
            return  # Admin-Auswahl nur am Profilbildschirm
        # Einmalige lokale Einrichtung direkt aus der EXE heraus: Der Nutzer muss
        # das GRUNDTOR bereits geoeffnet haben. Danach hat Admin ein eigenes Passwort
        # und eigene Datei; beim normalen Spielen wird es NIEMALS abgefragt.
        erstes_passwort = None
        if not tor.hat_passwort(self.admin_tor_pfad):
            if not messagebox.askyesno(
                    "Admin erstmalig einrichten",
                    "Noch kein separates Admin-Passwort vorhanden.\n"
                    "Jetzt einmalig einrichten? (mindestens 12 Zeichen)\n"
                    "Das Grundpasswort bleibt unveraendert.", parent=self.root):
                return
            neu1 = simpledialog.askstring("Admin-Passwort", "Neues Admin-Passwort:",
                                          show="*", parent=self.root)
            if neu1 is None:
                return
            neu2 = simpledialog.askstring("Admin-Passwort", "Admin-Passwort wiederholen:",
                                          show="*", parent=self.root)
            if neu2 is None:
                return
            if len(neu1) < 12:
                messagebox.showerror("Admin-Passwort", "Mindestens 12 Zeichen.", parent=self.root)
                return
            eingerichtet, hinweis = tor.setze_passwort(neu1, neu2, self.admin_tor_pfad)
            if not eingerichtet:
                messagebox.showerror("Admin-Passwort", hinweis, parent=self.root)
                return
            erstes_passwort = neu1  # nur fuer DIESE einmalige Anmeldung
        geheim = (erstes_passwort if erstes_passwort is not None else
                  simpledialog.askstring("Admin-Teststand", "Separates Admin-Passwort:",
                                         show="*", parent=self.root))
        if geheim is None:
            return
        ok, meldung = tor.pruefe_passwort(geheim, self.admin_tor_pfad)
        if not ok:
            messagebox.showerror("Admin-Zugriff verweigert", meldung, parent=self.root)
            return
        admin_pfad = spielstaende.admin_pfad(schreibordner())
        auswahl = messagebox.askyesnocancel(
            "Admin-Teststand", "Ja: frischen Teststand mit sechs Doerfern erzeugen.\n"
            "Nein: bestehenden Admin-Teststand laden.\nAbbrechen: nichts aendern.",
            parent=self.root)
        if auswahl is None:
            return
        if auswahl:
            if not messagebox.askyesno("Admin-Teststand", "Ein neuer Admin-Teststand wird angelegt. Der aktuell GESPEICHERTE "
                                     "Admin-Teststand wird dabei absichtlich ueberschrieben "
                                     "(keine Archivversion). Fortfahren?", parent=self.root):
                return
            neu = GameState()
            neu.generate_map(neu.current_map)
            try:
                admin_teststand.teststand_aufbauen(neu, Settlement, siedlung_kennung)
            except Exception as exc:
                messagebox.showerror("Teststand nicht erzeugt", str(exc), parent=self.root)
                return
            if not neu.save(admin_pfad, admin_freigabe=True):
                messagebox.showerror("Admin-Teststand", "Speichern gescheitert.", parent=self.root)
                return
            self.state = neu
        else:
            neu = GameState()
            if not neu.load(admin_pfad, admin_freigabe=True):
                messagebox.showwarning("Admin-Teststand", "Noch kein lesbarer Admin-Teststand.",
                                       parent=self.root)
                return
            self.state = neu
        self._admin_sitzung_freigegeben = True
        self._log("ADMIN-TESTSTAND geladen (kein regulaerer Spielstand).")
        self._spiel_starten(self.state, "admin")

    def _admin_werkzeuge_dialog(self):
        """Nur nach separater Authentifizierung und im markierten Teststand."""
        from tkinter import messagebox
        if ausgabemodus.ist_oeffentliche_testversion():
            return
        if not (self._tor_geoeffnet and self._profil == "admin" and
                self._admin_sitzung_freigegeben and
                getattr(self.state, "admin_teststand", False) and
                getattr(self.state, "oekonomie_aktiv", False)):
            messagebox.showerror("Admin-Test", "Adminfreigabe fehlt.", parent=self.root)
            return
        admin_pfad = spielstaende.admin_pfad(schreibordner())
        admin_oberflaeche.oeffnen(
            self.root, self.state, MAPS,
            speichern=lambda: self.state.save(admin_pfad, admin_freigabe=True),
            aktualisieren=self._admin_ansicht_aktualisieren,
        )

    def _admin_ansicht_aktualisieren(self):
        """Die normale Anzeige nach Admin-Aktionen aus EINEM Zustand neu aufbauen."""
        self._build_main_ui()
        self._render_view()

    def _log(self, msg: str):
        self.state._log(msg)
        print(msg)
        try:
            if hasattr(self, "lbl_status"):
                self.lbl_status.config(text=msg)
        except Exception:
            pass

    def _pruefe_spielende(self):
        """Sieg/Niederlage pruefen und EINMAL festhalten (Vorgabe Daniel 05.10.2026, Option A).

        Wird aus dem Takt aufgerufen. Ist die Partie entschieden, steht sie im Zustand
        (`state.spielende`), in den Nachrichten und im Log — und die Spieluhr wird danach nicht
        mehr weitergezogen (siehe `_tick_loop`). Rueckgabe: 'sieg', 'niederlage' oder None.
        Die Bedingung selbst kommt aus `src/punkte.py` (dort als VORSCHLAG gekennzeichnet,
        weil das Handbuch keine nennt).
        """
        if getattr(self.state, "admin_teststand", False):
            return None  # Nur Testmodus: keine sofortige Sieg-/Niederlage-Sperre
        if getattr(self.state, "spielende", None):
            return self.state.spielende
        art, grund = self.state.spielausgang()
        if art == "weiter":
            return None
        self.state.spielende = art
        self.state.messages.append({"type": "spielende", "text": grund})
        self._log(grund)
        return art

    def _tick_loop(self):
        # GPT-Z01: Windows-Systemzeit kann springen. Nur monotone Laufzeit fuer Ticks.
        dt = self.state._laufzeituhr.vergangen()
        if dt > 0 and getattr(self.state, "spielende", None) is None:
            # Der Zeitfaktor staucht die Spieluhr, NICHT die Handbuchformeln: `tick` bekommt
            # Spielsekunden. Bei ×180 ist eine echte Sekunde 180 Spielsekunden (eine Spielstunde
            # dauert 20 echte Sekunden) — sonst lieferte ein Holzfäller 4 Holz je ECHTER Stunde.
            _eingetroffen = self.state.tick(dt * spielzeit.faktor())
            # Teil 6c: ist dabei eine Ware oder eine Einheit fertig geworden, wird die Ansicht neu
            # gezeichnet — sonst bliebe sie unsichtbar, bis der Spieler die Ansicht wechselt.
            if _eingetroffen and getattr(self, "content", None) is not None:
                self._render_view()
        # movements arrival
        for m in self.state.movements[:]:
            if float(self.state.spielsekunden) >= m["arrival"]:
                tile_key = m.get("tile_key") or m["to"]
                x_str, y_str = tile_key.split(":")
                x, y = int(x_str), int(y_str)
                cfg = next((mm for mm in MAPS if mm["id"] == m.get("map", self.state.current_map)), None)
                size = cfg["size"] if cfg else 20
                tile = self.state.get_tile(x, y, size)
                target_bot_name = m.get("target_bot")
                if self.state.noob_protection and target_bot_name:
                    report = f"Truppen sind in {m['to']} eingetroffen. Götterschutz aktiv: keine Plünderung gegen {target_bot_name}."
                else:
                    # E3 (Daniel 31.10.2026, "ein Bewegungssystem"): Die Beute am Feld wird
                    # NICHT mehr gewuerfelt (frueher 10-40 Prozent zufaellig, ohne Karren und
                    # ohne Abbuchung - Gueter aus dem Nichts). Jetzt gilt dieselbe Formel wie
                    # im Auftrags-Pfad: kampfbericht.beute_am_ziel (Staffel, Karrenladung,
                    # Vorrat) UND das Feld verliert genau diese Menge.
                    _truppen = {u: int(c) for u, c in (m.get("units") or {}).items() if int(c) > 0}
                    _vorrat_feld = {k: float(v) for k, v in ((tile.resources if tile else None) or {}).items()}
                    loot, _lager_danach = kampfbericht.beute_am_ziel(
                        _truppen, _vorrat_feld, ausgang="angreifer",
                        wall_zustand_vor=100.0, verteidiger_uebrig=0,
                        forschung=self.state.forschungs_stufen())
                    if loot:
                        for res, amount in loot.items():
                            if res in self.state.resources:
                                self.state.resources[res].amount += int(amount)
                        if tile is not None:
                            tile.resources = {str(k): round(max(0.0, float(v)), 2)
                                              for k, v in (_lager_danach or {}).items()}
                    # Kampf und Verluste am Feld: KEIN Muenzenwurf mehr. Ein Bewegungsschritt
                    # auf der Karte ist ein Marsch; Kaempfe laufen ueber Auftraege bzw. den
                    # Direktangriff (E3-Rest, siehe docs/audits/UMBAUPLAN_E3_BEWEGUNG_20261031.md).
                    if target_bot_name and loot:
                        report = (f"Truppen sind in {m['to']} eingetroffen und haben "
                                  f"{target_bot_name} {', '.join(f'{v} {k}' for k, v in loot.items())} "
                                  f"abgenommen.")
                    elif loot:
                        parts = ", ".join(f"+{v} {k}" for k, v in loot.items())
                        report = f"Truppen sind in {m['to']} eingetroffen. Beute: {parts}."
                    else:
                        report = f"Truppen sind in {m['to']} eingetroffen."
                # E3 (Daniel 31.10.2026, Frage 14): Truppen sind nach der Ankunft NICHT sofort
                # wieder verfuegbar - sie marschieren dieselbe Strecke zurueck (gleiche Dauer wie
                # der Hinweg). Erst die Ankunft des Rueckmarsches bucht sie wieder ein.
                _dauer_hin = max(0.0, float(m.get("arrival") or 0.0) - float(m.get("start") or 0.0))
                if m.get("rueckweg") or _dauer_hin <= 0.0:
                    for u, c in m.get("units", {}).items():
                        if u in self.state.units:
                            self.state.units[u].count += c
                    if m.get("rueckweg"):
                        report = (f"Truppen sind von {m['to']} wieder zu Hause "
                                  f"({sum(int(c) for c in (m.get('units') or {}).values())} Einheiten).")
                else:
                    _rueck = rueckmarsch_eintrag(m, float(self.state.spielsekunden))
                    if _rueck:
                        self.state.movements.append(_rueck)
                        report += (f" Rueckmarsch laeuft: Ankunft zu Hause in "
                                   f"{_dauer_hin / 3600.0:.1f} Spielstunden.")
                self.state.messages.append({"text": report, "type": "bewegung"})
                self.state.movements.remove(m)
        self._render()
        if getattr(self, "current_view", "") == "Karten" and hasattr(self, "map_canvas"):
            try:
                if self.map_canvas.winfo_exists():
                    self._draw_map(getattr(self, "_map_size", 20))
            except Exception:
                pass
        self.root.after(1000, self._tick_loop)

    def _render(self):
        ertrag_jetzt = self.state.stundenertrag()
        for r, lbl in self.res_labels_top.items():
            text, warnung = kopfzeile_fuer(self.state, r, ertrag_jetzt)
            lbl.config(text=text,
                       fg=("#FDBA74" if warnung else self.skin["text"]))
        self._leiste_aktualisieren()                       # die acht Zahlen der Leiste nachziehen
        self.lbl_day.config(text=f"Tag {self.state.day}")
        self._spielerhilfe_anzeige_aktualisieren()
        if getattr(self, "lbl_tempo", None) is not None:
            self.lbl_tempo.config(text=f"Tempo {spielzeit.text()}")
        # W6: die Punktanzeige kommt aus den Originalformeln (src/punkte.py, Handbuch S. 3/5/6).
        # Vorher standen hier `score`, `ruf` und eine selbst gebaute Summe - die Gesamtzahl
        # war damit nachweislich falsch.
        staende = {k: v.level for k, v in self.state.research.items()}
        einheiten = {k: v.count for k, v in self.state.units.items()}
        stand_punkte = self.state.punktestand()
        self.lbl_forschung.config(text=f"Forschung: {stand_punkte['forschung']}")
        self.lbl_krieg.config(text=f"Krieg: {stand_punkte['krieg']}")
        self.lbl_gesamt.config(text=f"Gesamt: {stand_punkte['gesamt']}")
        # E5: KEIN Sieg. Angezeigt werden Stand, die belegte Goetterschutzgrenze und - falls
        # eingetreten - die Niederlage. Beendet wird der Lauf nur noch dadurch.
        self._pruefe_spielende()
        stand = self.state.punktestand()
        if getattr(self, "lbl_ziel", None) is not None:
            if self.state.spielende == "niederlage":
                self.lbl_ziel.config(text="NIEDERLAGE — keine Siedlung und keine Einheit mehr.",
                                     fg=self.skin["red"])
            else:
                self.lbl_ziel.config(
                    text=f"Punkte: {stand['gesamt']} · Goetterschutz bis "
                         f"{punkte.GOETTERSCHUTZ_PUNKTGRENZE} · kein Sieg",
                    fg=self.skin["text"])


def _laeuft_schon(lock_path: str) -> bool:
    """Prueft die Sperrdatei — und fasst dabei KEINEN Prozess an.

    Der frueher benutzte Aufruf ``os.kill(pid, 0)`` **beendet** unter Windows den Prozess
    (dort wird Signal 0 als TerminateProcess ausgefuehrt). Steht eine alte Nummer in der Datei und
    ist sie inzwischen an ein fremdes Programm vergeben, traefe es das falsche — deshalb wird hier
    nur gefragt: gibt es diesen Prozess noch?
    """
    try:
        with open(lock_path, encoding="utf-8") as f:
            pid = int(f.read().strip())
    except (OSError, ValueError):
        return False
    if pid <= 0:
        return False
    try:
        import ctypes
        from ctypes import wintypes
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        STILL_ACTIVE = 259
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if not handle:
            return False                      # den Prozess gibt es nicht (mehr): alte Sperre
        try:
            code = wintypes.DWORD()
            if kernel32.GetExitCodeProcess(handle, ctypes.byref(code)):
                return code.value == STILL_ACTIVE
            return True
        finally:
            kernel32.CloseHandle(handle)
    except Exception:
        # Ohne ctypes (theoretisch) lieber NICHT blockieren als das Starten verhindern.
        return False


# --------------------------------------------------------------- Ladeansicht (Titelbild)

# Das Titelbild als ABGELEITETE PNG-Fassung: Tk liest nur PNG/GIF, die beigelegte Originaldatei
# ist ein JPEG. Die Originaldatei bleibt unveraendert im Projektordner liegen (nicht umbenannt,
# nicht verschoben, nicht beschnitten) — die PNG-Fassung liegt daneben in `assets/loadingpage/`
# und wird von dort auch in die EXE gebuendelt (`assets` ist mitgegeben).
LADEBILD_PNG = ("assets", "loadingpage", "Nebelseetal_Loadingpage.png")


def ladebild_pfad() -> str:
    """Der Pfad des Titelbilds — gesucht ueber die Projektwurzel, nicht geraten."""
    return os.path.join(spieldaten.projektwurzel(), *LADEBILD_PNG)


def zeige_loadingpage(root):
    """Die Ladeansicht zeigen: Titelbild + Hinweis, waehrend der Start rechnet.

    Tk liest kein JPEG; fehlt die PNG-Fassung oder kann Tk sie nicht lesen, bleibt es bei einer
    **ehrlichen Textzeile** — der Start wird nie blockiert und nie eine leere Flaeche gezeigt.
    Die Ansicht raeumt sich selbst weg: `NebelseetalApp._tor_screen` zerstoert alle Inhalte des
    Fensters, bevor es das Passworttor aufbaut.

    Rueckgabe: das Bildobjekt (muss am Leben bleiben, sonst raeumt Tk es weg) oder None.
    """
    try:
        for widget in root.winfo_children():
            widget.destroy()
        root.title("Nebelseetal Remake — einen Augenblick")
        root.configure(bg="#1b1109")
        rahmen = tk.Frame(root, bg="#1b1109")
        rahmen.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
        bild = None
        pfad = ladebild_pfad()
        if os.path.exists(pfad):
            try:
                bild = tk.PhotoImage(file=pfad)
            except Exception:
                bild = None
        if bild is not None:
            tk.Label(rahmen, image=bild, bg="#1b1109").pack()
        else:
            tk.Label(rahmen, text="Nebelseetal", font=("Blackletter", 44, "bold"),
                     fg="#FFCC33", bg="#1b1109").pack(pady=20)
        tk.Label(rahmen, text="Das Tal erwacht — die Karte wird gelegt.",
                 font=("Arial", 12), fg="#E8D9B5", bg="#1b1109").pack(pady=(10, 0))
        tk.Label(rahmen, text="Nebelseetal Remake", font=("Arial", 10),
                 fg="#8a7a5c", bg="#1b1109").pack(pady=(2, 0))
        root.update()
        return bild
    except Exception:
        # Ein fehlendes Bild darf den Start nie verhindern.
        return None


def main():
    import sys
    lock_path = os.path.join(schreibordner(), "game.lock")
    if _laeuft_schon(lock_path):
        print("Spiel läuft bereits.")
        sys.exit(0)
    try:
        os.makedirs(os.path.dirname(lock_path), exist_ok=True)
        with open(lock_path, "w") as f:
            f.write(str(os.getpid()))
    except OSError:
        pass
    try:
        root = tk.Tk()
        # Die Ladeansicht steht, waehrend der Start rechnet (Karte legen, Spielstand pruefen,
        # Passworttor). Sie verschwindet von selbst: das Tor raeumt alle Fensterinhalte weg.
        zeige_loadingpage(root)
        app = NebelseetalApp(root)
        root.mainloop()
    finally:
        try:
            os.remove(lock_path)
        except Exception:
            pass


if __name__ == "__main__":
    main()
