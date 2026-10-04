"""
Nebelseetal Remake — Core Game Engine
Single-player, local, portable Windows desktop app.
Multi-map system, trade, combat, research, bots, stationing.
"""
from __future__ import annotations
import json
import os
import random
import time
import tkinter as tk
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional

from bonus_system import (
    # Nur noch, was main.py wirklich benutzt. Die erfundenen Kampf- und Preisformeln
    # (`get_combat_power`, `get_unit_stats`, `get_building_cost`, `get_map_switch_cost`,
    # `UNIT_BASE`, `UNIT_TRAIN_BASE`, `BUILDING_BASE_COST`, `TIER_SCALE`) sind hier nicht mehr
    # im Spiel: Kaempfe rechnet src/kampf.py, Preise kommen aus data/*.json, Punkte aus src/punkte.py.
    get_military_multiplier, get_trade_bonus, get_defense_bonus, get_medic_redution,
    get_training_time,
)
import einheiten
import spieldaten
import gelaende
import gebaeude_wirkung
import berater
import tor
import wirtschaft
import speichern   # W8: robustes Speichern/Laden (atomar, geprueft, mit Sicherung)
import punkte      # W6: Forschungs-, Kriegs- und Gesamtpunkte nach den Originalformeln
import kampf       # W2: Vorrunde, Kampfsequenzen, Flucht, Beute (Handbuch S. 20-23)
import kampfbericht  # W2b: Vorrunden-Pruefung, Mauerschaden, Beute, Bericht
import botkern     # W5: Bot-Regeln (hier: die Vorschlagsspannen fuer die Vorraete der Bots)
import portalraum  # W5-2: die 20 Dimensionen des Limbus, Raster, Wechselkosten und -sperre
import werkstatt   # W3: die drei Werkstaetten, die 17 Waren und ihre Warteschlangen
import auftraege   # W7: Auftraege (Missionen) mit Reisezeit, Rueckkehr und Bericht


# ---------- Data Models ----------

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
    bauten: Dict[str, str] = field(default_factory=dict)
    # Ausbaustufe je bebautem Feld (W4b-5). Belegt sind Stufen für den Verteidigungswall (10)
    # und die drei Ausbildungsstätten; ein Feld ohne Eintrag gilt als Stufe 1.
    stufen: Dict[str, int] = field(default_factory=dict)


# Handbuch S. 313: 'Einer neuen Siedlung wird per Zufall eine Karte zugewiesen. Es werden
# niemals zwei Deiner Siedlungen die gleiche Karte bekommen.' Wie viele Siedlungen erlaubt
# sind, sagt das Handbuch nicht ausdrücklich — sechs ist der belegte Stand (sechs Welten,
# sechs Siedlungen je Spieler laut Konformitäts-Audit).
SIEDLUNGEN_MAXIMUM = 6
KARTENVERSUCHE = 400


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
        karte = gelaende.siedlungskarte_erzeugen(random.randrange(1, 10 ** 9))
        if karten_signatur(karte) not in vergeben:
            return karte
    raise RuntimeError("Keine neue Siedlungskarte gefunden")


def bauen_auf_karte(siedlung: "Settlement", gebaeude_key: str, feld: int) -> tuple:
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
    siedlung.bauten[str(feld)] = gebaeude_key
    siedlung.stufen[str(feld)] = 1
    return True, f"{warum} (Feld {feld})"


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


def baukosten(gebaeude_key: str, stufe: int = 0) -> dict:
    """
    Baupreis eines Gebaeudes.

    Enthaelt neben Rohstoffen ggf. den Posten "siedler" (belegt: Holzfäller, Steinmetz und Jäger
    kosten je 1 Siedler, der dann dort arbeitet). Ausbau auf Stufe n kostet das n-fache.
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
    return {r: v * faktor for r, v in eintrag.items()
            if (r in RESOURCES or r == "siedler") and isinstance(v, (int, float))}


def kosten_text(kosten: dict) -> str:
    """Kosten als lesbarer Text, z. B. '8 Holz, 4 Stein'."""
    if not kosten:
        return "Preis offen"
    return ", ".join(f"{int(v)} {r.capitalize()}" for r, v in kosten.items())


# Die neun Originalrohstoffe aus data/resources.json (Handbuch Seiten 9-10), in der Reihenfolge
# des Handbuchs. Erfunden waren: kristall, stoff, geld, wissen — eisen hiess im Handbuch Metall.
RESOURCES = ["holz", "stein", "metall", "mana", "nahrung", "gold", "wolle", "leder", "pferde"]
RESOURCE_ICONS = {
    "holz": "🌲", "stein": "🪨", "metall": "⛏️", "mana": "🔮", "nahrung": "🌾",
    "gold": "💰", "wolle": "🧶", "leder": "🦬", "pferde": "🐴",
}
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
BOTS = [
    BotPlayer("Haug", "menschlich", aggression=0.3, trading=0.8),
    BotPlayer("Brynhild", "menschlich", aggression=0.5, trading=0.6),
    BotPlayer("Grom", "zwergisch", aggression=0.7, trading=0.4),
    BotPlayer("Silra", "elfisch", aggression=0.2, trading=0.9),
    BotPlayer("Krank", "monster", aggression=0.9, trading=0.0),
]
MENU_ITEMS = [
    "Dorfzentrum", "Lager", "Kaserne", "Marktplatz", "Gilde", "Nachrichten",
    "Portal", "Karten", "Forschung", "Diplomatie", "Einstellungen",
    "Ruhmeshalle", "Anleitung", "Kampfsimulator", "Forum", "Chat", "Spieler werben"
]

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
        self.last_tick = time.time()
        self.ruf = 0
        self.log: List[str] = []
        self.map_garrison: Dict[str, Dict[str, int]] = {}
        self.movements: List[dict] = []
        self.messages: List[dict] = []
        self.settlements: List[Settlement] = []
        self.noob_protection: bool = True
        self.goods: Dict[str, int] = {key: 0 for key in GOODS}
        # W5-2 (Portal, src/portalraum.py): die eigene Dimension im Limbus-Raster, die Dimensionen,
        # in denen man schon Fuss gefasst hat, und der Zeitpunkt des letzten Koordinatenwechsels.
        # Start in Dimension 1 - VORSCHLAG, das Handbuch nennt keine Startdimension.
        self.eigene_dimension: int = 1
        self.eigene_dimensionen: List[int] = [1]
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

    def _unlock_next_map(self):
        if len(self.active_maps) >= MAX_ACTIVE_MAPS:
            return
        candidates = [m for m in MAPS if m["id"] not in self.unlocked_maps]
        if not candidates:
            return
        verm = self.research.get("vermessung")
        # W4b-5: Der erfundene Gebaeude-Eintrag "Portal" ist entfallen (er steht nicht unter den
        # 20 Originalgebaeuden). Weitere Karten schaltet die Forschung "Vermessung" frei —
        # mehr Karteninformationen (Handbuch Seite 12).
        if verm and verm.level >= 1:
            next_map = candidates[0]
            self.unlocked_maps.append(next_map["id"])
            self.active_maps.append(next_map["id"])
            self._log(f"Neue Karte entdeckt: {next_map['name']}")

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
            pool = random.sample(list(UNITS.keys()), min(5, len(UNITS)))
            d["army"] = {u: random.randint(20, 120) for u in pool}
            d["ruf"] = random.randint(0, 60)
            bots.append(BotPlayer(**d))
        self.bots = bots

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

    def ware_voraussetzung(self, ware: str):
        """Prueft die belegte Voraussetzung einer Ware (Forschung + Stufe) gegen diesen Stand.

        Rueckgabe (erfuellt, Begruendung). Eine Forschung, die wir nicht kennen, gilt als NICHT
        erfuellt - es wird nichts erfunden und nichts stillschweigend durchgelassen.
        """
        eintrag = WARE_EINTRAEGE.get(ware) or {}
        struktur = eintrag.get("voraussetzung_struktur")
        if not isinstance(struktur, dict):
            return True, "keine Voraussetzung belegt"
        gebiet = str(struktur.get("forschung") or "")
        if not gebiet:
            return True, "keine Voraussetzung belegt"
        try:
            noetig = int(struktur.get("stufe") or 0)
        except (TypeError, ValueError):
            noetig = 0
        forschung = self.research.get(gebiet)
        if forschung is None:
            return False, f"die Forschung '{gebiet}' kennen wir nicht - nicht erfuellbar"
        if int(forschung.level) < noetig:
            return False, f"{gebiet} Stufe {noetig} noetig, vorhanden ist Stufe {int(forschung.level)}"
        return True, f"{gebiet} Stufe {noetig} vorhanden"

    # ---------------- W7: Auftraege (Missionen) ----------------

    def auftrag_starten(self, art: str, mitgenommene: dict, von: str, nach, entfernung: float,
                        fracht: dict = None, ziel_zusatz: dict = None):
        """Einen Auftrag starten. Rueckgabe (ok, Meldung).

        Die mitgegebenen Einheiten sind ab jetzt **unterwegs**: sie werden hier aus dem Bestand
        genommen und bei `abgeschlossen` zurueckgegeben - ausser beim **Stationieren**, da bleiben
        sie am Ziel (Handbuch S. 19). Geprueft wird alles ueber `auftraege.starten`; ohne genug
        Einheiten (oder bei Ueberladung) wird VOR jeder Aenderung abgelehnt.
        """
        ziel = dict(ziel_zusatz or {})
        if isinstance(nach, dict):
            ziel.update(nach)
        ziel["name"] = str((nach.get("name") if isinstance(nach, dict) else nach) or "")
        if not ziel["name"]:
            return False, "Kein Ziel benannt."
        bestand = {k: int(v) for k, v in (mitgenommene or {}).items() if int(v) > 0}
        if not bestand:
            return False, "Ohne Einheiten kann kein Auftrag reisen."
        zu_wenig = [k for k, v in bestand.items() if k not in self.units or int(self.units[k].count) < v]
        if zu_wenig:
            return False, f"Nicht genug Einheiten anwesend: {', '.join(sorted(zu_wenig))}."

        ok, meldung = auftraege.starten(self.auftraege, art, bestand, von, ziel,
                                        float(entfernung), time.time(), fracht)
        if not ok:
            return False, meldung
        for k, v in bestand.items():
            self.units[k].count = max(0, int(self.units[k].count) - v)
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

        for eintrag in auftraege.angekommen(self.auftraege, jetzt):
            vorher = {"ressourcen": {k: v.amount for k, v in self.resources.items()},
                      "einheiten": {k: u.count for k, u in self.units.items()}}
            neu = auftraege.spieldaten_anwenden(vorher, eintrag)
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
            if eintrag.get("status") != "abgeschlossen" or eintrag.get("heimgekehrt"):
                continue
            eintrag["heimgekehrt"] = True
            if eintrag.get("art") == "stationieren":
                continue                      # bleibt am Ziel: kommt nicht heim
            for name, anzahl in (eintrag.get("einheiten") or {}).items():
                if name in self.units:
                    self.units[name].count = int(self.units[name].count) + int(anzahl)
                    ergebnis["heimgekehrt"][name] = ergebnis["heimgekehrt"].get(name, 0) + int(anzahl)
        self.auftraege[:] = [e for e in self.auftraege
                             if not (e.get("status") == "abgeschlossen" and e.get("heimgekehrt"))]
        return ergebnis

    def tick(self, dt_seconds: float):
        dt_h = dt_seconds / 3600.0
        levels = {k: v.level for k, v in self.research.items()}
        # Rohstoffe kommen aus den BEBauten FELDERN der Siedlungskarten (W4b-4, 04.10.2026).
        for res, rate_pro_stunde in self.stundenertrag().items():
            if res in self.resources:
                self.resources[res].amount = round(
                    self.resources[res].amount + rate_pro_stunde * dt_h, 2)
        for bot in self.bots:
            if bot.settlements and random.random() < 0.05 * bot.aggression:
                # nur Kaempfer und Kundschafter verteidigen — Karren und Belagerungswaffen nicht
                defense = sum(self.units[u].defense * max(1, self.units[u].count)
                              for u in self.units if einheiten.ist_kaempfer(u))
                loss = max(0, int(get_military_multiplier(levels) * 10 * bot.aggression - get_medic_redution(levels)))
                self.resources["nahrung"].amount = max(0, self.resources["nahrung"].amount - loss)
        # FIX 2+3: Tag fortschreiben (86400s = 1 Spieltag) + Noobschutz nach Tag 3 deaktivieren
        # Siedlergrenze und Siedlerzuwachs kommen aus den Haeusern der Siedlungskarten (W4b-5):
        # 10 Siedler je Siedlung, +5 je Haus, 1 neuer Siedler je Stunde (Handbuch Seite 11),
        # mit Heilkunde +10 % je Stufe. Vorher stand hier ein erfundener Zuwachs von 30 je Stunde.
        self.max_population = gebaeude_wirkung.bevoelkerungsgrenze(self.settlements)
        zuwachs = gebaeude_wirkung.siedler_zuwachs_pro_stunde(self.settlements, levels) * dt_h
        if zuwachs > 0 and self.population < self.max_population:
            self.population = min(float(self.max_population), self.population + zuwachs)
        self._day_accum = getattr(self, "_day_accum", 0.0) + dt_seconds
        if self._day_accum >= 86400:
            self._day_accum -= 86400
            self.day += 1
        if self.day >= 3 and self.noob_protection:
            self.noob_protection = False
            self.messages.append({"text": "Noobschutz aufgehoben - die Welt ist jetzt gefaehrlich!", "type": "system"})
        # W3: fertige Waren aus den Werkstatt-Warteschlangen ins Lager buchen (genau einmal).
        self.werkstatt_fortschreiben(time.time())
        # W7: Auftraege weiterlaufen lassen (Ankunft buchen, Heimkehrer gutschreiben).
        self.auftraege_fortschreiben(time.time())
        self.last_tick = time.time()

    def save(self, path: str):
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

    def load(self, path: str):
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
        for k, v in data.get("resources", {}).items():
            if k in self.resources:
                self.resources[k] = Resource(**v)
        for k, v in data.get("buildings", {}).items():
            if k in self.buildings:
                self.buildings[k] = Building(**v)
        for k, v in data.get("research", {}).items():
            if k in self.research:
                self.research[k] = Research(**v)
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
        self.messages = data.get("messages", [])
        self.settlements = [Settlement(**s) for s in data.get("settlements", [])]
        self.noob_protection = data.get("noob_protection", True)
        self.goods = data.get("goods", {key: 0 for key in GOODS})
        # W5-2: Portalzustand (eigene Dimension, bekannte Dimensionen, letzter Wechsel)
        self.eigene_dimension = int(data.get("eigene_dimension", 1) or 1)
        self.eigene_dimensionen = list(data.get("eigene_dimensionen") or [1])
        self.letzter_wechsel = data.get("letzter_wechsel")
        # W3: Warenlager (immer alle 17 Originalwaren) und die Werkstatt-Warteschlangen
        geladene_waren = data.get("waren") or {}
        self.waren = {name: int(geladene_waren.get(name, 0) or 0) for name in WARE_EINTRAEGE}
        self.werkstaetten = {k: v for k, v in (data.get("werkstaetten") or {}).items()
                             if isinstance(v, dict)}
        # W7: laufende Auftraege (unterwegs befindliche Einheiten sind hier schon abgezogen)
        self.auftraege = [e for e in (data.get("auftraege") or []) if isinstance(e, dict)]
        # FIX 4b: Karte + Bots laden (wurde vorher nicht persistiert)
        saved_tiles = data.get("map_tiles")
        saved_bots = data.get("bots")
        if saved_tiles:
            self.map_tiles = [MapTile(**t) for t in saved_tiles]
        else:
            self.generate_map(self.current_map)
        if saved_bots:
            self.bots = [BotPlayer(**b) for b in saved_bots]
        self._day_accum = 0.0
        return True

    def _log(self, msg: str):
        self.log.append(msg)
        if len(self.log) > 200:
            self.log = self.log[-200:]


# ---------- GUI ----------

class NebelseetalApp:
    def __init__(self, root: tk.Tk, tor_pfad: Optional[str] = None):
        self.root = root
        self.root.title("Nebelseetal Remake")
        self.root.geometry("1024x720")
        self.state = GameState()
        self.state.generate_map(self.state.current_map)
        # Spielstand: im Entwicklungsbetrieb neben dem Quelltext, in der EXE im Nutzerordner
        # (der Programmordner kann schreibgeschuetzt sein und wird beim Einzeldatei-Start entpackt).
        if ist_verpackt():
            self.save_path = os.path.join(schreibordner(), "savegame.json")
        else:
            self.save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "savegame.json")
        # W8 (Vorschlag aus docs/UMSETZUNG_EINHAENGEN.md, 4.2): liegengebliebene Zwischendateien
        # eines abgebrochenen Schreibvorgangs entfernen - Zieldatei und Sicherung bleiben unberuehrt.
        speichern.aufraeumen(self.save_path)
        self.current_view = "Dorfzentrum"
        self.skin_name = "standard"
        self.skin = SKINS[self.skin_name]
        self._icon_cache: Dict[str, object] = {}   # haelt Tk-Bilder am Leben (sonst raeumt Tk sie weg)
        # Schritt 8 (docs/WEG_ZUR_EXE.md): erst das Passworttor, dann das Spiel.
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
            self.root.after(600, self._build_loading_screen)
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
            self.root.after(400, self._build_loading_screen)
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

    def _build_main_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg=self.skin["bg"])

        top = tk.Frame(self.root, bg=self.skin["topbar"], height=40)
        top.pack(fill=tk.X, side=tk.TOP)
        top.pack_propagate(False)
        tk.Label(top, text="Nebelseetal", font=("Blackletter", 16, "bold"), fg=self.skin["gold"], bg=self.skin["topbar"]).pack(side=tk.LEFT, padx=10)
        self.res_labels_top = {}
        ertrag_jetzt = self.state.stundenertrag()
        for r in RESOURCES:
            icon = RESOURCE_ICONS[r]
            amount = int(self.state.resources[r].amount)
            rate = ertrag_jetzt.get(r, 0.0)
            prod_text = f"+{rate:g}/h" if rate else "0"
            lbl = tk.Label(top, text=f"{icon} {int(amount)} ({prod_text})", fg=self.skin["text"], bg=self.skin["topbar"], font=("Arial", 9))
            lbl.pack(side=tk.LEFT, padx=6)
            self.res_labels_top[r] = lbl
        for txt, cmd in [("Speichern", self._save), ("Laden", self._load), ("Skin", self._cycle_skin), ("Beenden", self.root.quit)]:
            tk.Button(top, text=txt, command=cmd, bg=self.skin["button"], fg=self.skin["gold"], relief=tk.FLAT, padx=8, pady=2).pack(side=tk.RIGHT, padx=4)
        self.lbl_day = tk.Label(top, text=f"Tag {self.state.day}", fg=self.skin["gold"], bg=self.skin["topbar"])
        self.lbl_day.pack(side=tk.RIGHT, padx=10)

        # Statuszeile unten: muss VOR dem expandierenden main-Frame gepackt werden,
        # sonst frisst main den ganzen Platz und die Zeile bleibt 1 px hoch.
        self.lbl_status = tk.Label(self.root, text="Willkommen in Nebelseetal.", fg=self.skin["text"],
                                   bg=self.skin["topbar"], anchor=tk.W, font=("Arial", 9), padx=8)
        self.lbl_status.pack(fill=tk.X, side=tk.BOTTOM)

        main = tk.Frame(self.root, bg=self.skin["bg"])
        main.pack(fill=tk.BOTH, expand=True)

        left = tk.Frame(main, bg=self.skin["sidebar"], width=180)
        left.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(left, text="Menü", fg=self.skin["gold"], bg=self.skin["sidebar"], font=("Arial", 10, "bold")).pack(anchor=tk.W, padx=8, pady=(8, 4))
        self.menu_buttons = {}
        for item in MENU_ITEMS:
            btn = tk.Button(left, text=item, fg=self.skin["red"], bg=self.skin["sidebar"], activebackground=self.skin["button_active"], activeforeground=self.skin["gold"],
                            relief=tk.FLAT, anchor=tk.W, padx=12, command=lambda i=item: self._switch_view(i))
            btn.pack(fill=tk.X, pady=1, ipady=2)
            self.menu_buttons[item] = btn

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

        # FIX 1: Tick-Loop starten (Produktion, Tag, Bewegung, Render laufen lassen)
        if not getattr(self, "_tick_started", False):
            self._tick_started = True
            self.root.after(1000, self._tick_loop)

    def _switch_view(self, view: str):
        self.current_view = view
        for item, btn in self.menu_buttons.items():
            btn.config(fg=self.skin["gold"] if item == view else "#e53935")
        self._render_view()

    def _rad_rollen(self, ereignis):
        """Mausrad im Inhaltsbereich — schuetzt sich selbst, falls noch kein Rollbereich da ist."""
        try:
            if self.content_canvas.winfo_exists():
                self.content_canvas.yview_scroll(int(-ereignis.delta / 120), "units")
        except Exception:
            pass

    def _render_view(self):
        for widget in self.content.winfo_children():
            widget.destroy()
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
            "Marktplatz": self._render_market,
            "Gilde": self._render_guild,
            "Nachrichten": self._render_messages,
            "Portal": self._render_portal,
            "Karten": self._render_maps,
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
        tk.Label(self.content, text="Siedlungsübersicht", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        tk.Label(self.content, text="Eine Übersicht aller Gebäude.", fg=self.skin["text"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)
        _grenze = gebaeude_wirkung.bevoelkerungsgrenze(self.state.settlements)
        tk.Label(self.content, text=f"Bevölkerung: {int(self.state.population)} / {_grenze}",
                 fg="#DAA520", bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)
        frame = tk.Frame(self.content, bg=self.skin["panel"])
        frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(frame, text="Siedlungen:", fg=self.skin["gold"], bg=self.skin["panel"]).pack(anchor=tk.W, padx=5)
        for i, s in enumerate(self.state.settlements):
            row = tk.Frame(self.content, bg=self.skin["panel"])
            row.pack(fill=tk.X, padx=10, pady=2)
            tk.Label(row, text=f"{s.name} ({s.map_id})", fg=self.skin["text"], bg=self.skin["panel"], width=20, anchor=tk.W).pack(side=tk.LEFT, padx=5)
            tk.Label(row, text=f"Gebäude: {len(s.buildings)}", fg="#DAA520", bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
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
        tk.Button(self.content, text="Neue Siedlung gründen", command=self._found_settlement, bg="#3e2723", fg=self.skin["gold"]).pack(anchor=tk.W, padx=10, pady=10)

        # W7: die laufenden Auftraege (im Original steht unten "Laufende Auftraege"). Die Einheiten
        # sind waehrend der Reise aus dem Bestand genommen; angekommen liefert den Bericht in die
        # Nachrichten. Gezeigt wird nur, was `auftraege.fortschritt` wirklich hergibt.
        tk.Label(self.content, text="Laufende Aufträge:", fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(6, 0))
        if not self.state.auftraege:
            tk.Label(self.content, text="keine — Aufträge startet man in der Diplomatie.",
                     fg="#8a8a8a", bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)
        else:
            stand = auftraege.fortschritt(self.state.auftraege, time.time())
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
        tk.Label(wirk, text=f"Siedlergrenze {_grenze} · Zuwachs "
                            f"{gebaeude_wirkung.siedler_zuwachs_pro_stunde(self.state.settlements):g} Siedler/Stunde "
                            f"(1 je Siedlung, Handbuch S. 11)",
                 fg=self.skin["text"], bg=self.skin["panel"]).pack(anchor=tk.W, padx=5)
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
        for _k in ("werkstaetten", "baukunst", "lager"):
            _luecke = gebaeude_wirkung.luecken().get(_k)
            if _luecke:
                tk.Label(wirk, text=f"Noch offen: {_luecke}", fg="#C0C0C0", bg=self.skin["panel"],
                         wraplength=780, justify=tk.LEFT).pack(anchor=tk.W, padx=5)

    def _upgrade_building(self, key: str):
        """Ausbau eines GLOBALEN Gebaeudes — gibt es seit W4b-5 nicht mehr.

        Die Wirkungen der 20 Originalgebaeude haengen an den bebauten FELDERN der
        Siedlungskarten; ausgebaut wird dort: Siedlungskarte oeffnen, Feld waehlen, "Ausbauen".
        Diese Methode nennt den richtigen Weg, statt still nichts zu tun — alte Aufrufe und
        Spielstaende landen hier.
        """
        self._log(f"'{key}' ist kein globales Gebäude: die Wirkungen kommen aus den bebauten "
                  f"Feldern der Siedlungskarten — dort das Feld wählen und 'Ausbauen' benutzen.")

    def _found_settlement(self):
        if len(self.state.settlements) >= SIEDLUNGEN_MAXIMUM:
            self._log(f"Maximale Siedlungsanzahl erreicht ({SIEDLUNGEN_MAXIMUM}).")
            return
        cfg = next(m for m in MAPS if m["id"] == self.state.current_map)
        size = cfg["size"]
        attempts = 0
        while attempts < 200:
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            tile = self.state.get_tile(x, y, size)
            if tile and tile.terrain != "water" and not tile.npc_faction:
                name = f"Siedlung {len(self.state.settlements)+1}"
                if any(s.name == name for s in self.state.settlements):
                    attempts += 1
                    continue
                # Handbuch S. 313: zufällige Karte, niemals dieselbe wie eine andere eigene Siedlung.
                try:
                    karte = neue_siedlungskarte([s.karte for s in self.state.settlements])
                except RuntimeError as fehler:
                    self._log(f"Keine Siedlung gegründet: {fehler}")
                    return
                sett = Settlement(name=name, map_id=self.state.current_map, x=x, y=y, karte=karte)
                self.state.settlements.append(sett)
                tile.npc_faction = "spieler"
                tile.sector_name = name
                self._log(f"Neue Siedlung '{name}' auf {self.state.current_map} bei {x}:{y} gegründet.")
                self._log(f"  Karte: {karte['typ_name']} — {karte['vorteil']}")
                self._log(f"  {gelaende.karte_beschreiben(karte)}")
                return
            attempts += 1
        self._log("Kein geeigneter Platz für eine Siedlung gefunden.")

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

    def _transport_to_settlement(self, settlement: Settlement):
        if settlement.map_id != self.state.current_map:
            self._log("Transport nur zur aktuellen Karte möglich.")
            return
        amount = 10
        resource = "holz"
        self.state.resources[resource].amount = max(0, self.state.resources[resource].amount - amount)
        self._log(f"Transport von {amount} {resource} zur Siedlung {settlement.name} gestartet.")

    # ---------- Siedlungskarte (Handbuch S. 259/283/292/313) ----------

    def _oeffne_siedlungskarte(self, siedlung):
        self.karten_siedlung = siedlung
        self.karten_feld = None
        self._switch_view("Siedlungskarte")

    def _karten_feld_waehlen(self, feld: int):
        self.karten_feld = feld
        self._render_view()

    def _karten_bauen(self, gebaeude_key: str):
        siedlung = getattr(self, "karten_siedlung", None)
        feld = getattr(self, "karten_feld", None)
        if siedlung is None or feld is None:
            return
        name = gelaende.gebaeude_name(gebaeude_key)
        kosten = baukosten(gebaeude_key)
        if not kosten:
            self._log(f"Für {name} ist kein Preis hinterlegt — Bau abgebrochen.")
            return
        # Rohstoff-Kosten prüfen; der Siedler kommt aus der Bevölkerung, nicht aus dem Lager.
        fehlt = [r for r, v in kosten.items()
                 if r != "siedler" and self.state.resources[r].amount < v]
        braucht_siedler = kosten.get("siedler", 0)
        if braucht_siedler > self.state.population:
            fehlt.append("siedler")
        if fehlt:
            self._log(f"Nicht genug Rohstoffe für {name}: es fehlt "
                      f"{', '.join(sorted(fehlt))}.")
            return
        ok, meldung = bauen_auf_karte(siedlung, gebaeude_key, feld)
        if not ok:
            self._log(f"Bau nicht möglich: {meldung}")
            return
        for r, v in kosten.items():
            if r == "siedler":
                self.state.population = max(0.0, self.state.population - v)
            else:
                self.state.resources[r].amount -= v
        self._log(f"{name} gebaut — {meldung}")
        self.karten_feld = None
        self._render_view()

    def _karten_abreissen(self):
        siedlung = getattr(self, "karten_siedlung", None)
        feld = getattr(self, "karten_feld", None)
        if siedlung is None or feld is None:
            return
        gebaut = siedlung.bauten.pop(str(feld), None)
        siedlung.stufen.pop(str(feld), None)
        if gebaut:
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
        gebaut = siedlung.bauten.get(str(feld))
        if not gebaut:
            return
        name = gelaende.gebaeude_name(gebaut)
        stufe = gebaeude_wirkung.stufe_von_feld(siedlung, feld)
        grenze = gebaeude_wirkung.max_stufe(gebaut)
        if grenze is None:
            self._log(f"{name} kennt keinen Ausbau — das Handbuch nennt für dieses Gebäude "
                      f"keine Stufen.")
            return
        if stufe >= grenze:
            self._log(f"{name} ist bereits auf der höchsten Stufe ({grenze}).")
            return
        kosten = baukosten(gebaut, stufe + 1)
        fehlt = [r for r, v in kosten.items()
                 if r != "siedler" and self.state.resources[r].amount < v]
        if kosten.get("siedler", 0) > self.state.population:
            fehlt.append("siedler")
        if fehlt:
            self._log(f"Nicht genug Rohstoffe für den Ausbau von {name}: es fehlt "
                      f"{', '.join(sorted(fehlt))}.")
            return
        for r, v in kosten.items():
            if r == "siedler":
                self.state.population = max(0.0, self.state.population - v)
            else:
                self.state.resources[r].amount -= v
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
                 fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)
        tk.Label(self.content, text=f"Vorteil: {karte['vorteil']}", fg=self.skin["text"],
                 bg=self.skin["bg"], wraplength=780, justify=tk.LEFT).pack(anchor=tk.W, padx=10)
        zaehlung = ", ".join(f"{gelaende.name(a)} {n}" for a, n in karte["zaehlung"].items() if n)
        tk.Label(self.content, text=zaehlung, fg=self.skin["text"], bg=self.skin["bg"],
                 wraplength=780, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=(2, 6))

        raster_rahmen = tk.Frame(self.content, bg=self.skin["bg"])
        raster_rahmen.pack(anchor=tk.W, padx=10)
        for i, art in enumerate(karte["raster"]):
            gebaut = siedlung.bauten.get(str(i))
            beschriftung = gelaende.gebaeude_name(gebaut)[:6] if gebaut else str(i)
            knopf = tk.Button(raster_rahmen, text=beschriftung, width=6, height=2,
                              bg=gelaende.farbe(art), fg="#F2ECDF", activebackground=gelaende.farbe(art),
                              relief=(tk.SUNKEN if gebaut else tk.RAISED), bd=2,
                              command=lambda idx=i: self._karten_feld_waehlen(idx))
            knopf.grid(row=i // karte["spalten"], column=i % karte["spalten"], padx=1, pady=1)
            if i == getattr(self, "karten_feld", None):
                knopf.config(highlightbackground="#FFC300", highlightthickness=3)

        legende = tk.Frame(self.content, bg=self.skin["bg"])
        legende.pack(anchor=tk.W, padx=10, pady=(6, 2))
        for art in gelaende.GELAENDEARTEN:
            tk.Label(legende, text="   ", bg=gelaende.farbe(art)).pack(side=tk.LEFT, padx=(5, 1))
            tk.Label(legende, text=gelaende.name(art), fg=self.skin["text"],
                     bg=self.skin["bg"]).pack(side=tk.LEFT)
        tk.Label(self.content, text="Sumpf ist nicht bebaubar (Handbuch S. 11). "
                                   "Feld anklicken zeigt die Eignung (Handbuch S. 7/8).",
                 fg=self.skin["text"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(2, 4))

        info = tk.Frame(self.content, bg=self.skin["panel"])
        info.pack(fill=tk.X, padx=10, pady=6)
        feld = getattr(self, "karten_feld", None)
        if feld is None:
            tk.Label(info, text="Ein Feld auf der Karte anklicken, um dort zu bauen.",
                     fg=self.skin["text"], bg=self.skin["panel"]).pack(anchor=tk.W, padx=6, pady=6)
            return

        art = karte["raster"][feld]
        gebaut = siedlung.bauten.get(str(feld))
        tk.Label(info, text=f"Feld {feld} — {gelaende.name(art)}", fg=self.skin["gold"],
                 bg=self.skin["panel"], font=("TkDefaultFont", 11, "bold")).pack(anchor=tk.W, padx=6, pady=(6, 2))

        if gebaut:
            stufe = gebaeude_wirkung.stufe_von_feld(siedlung, feld)
            grenze = gebaeude_wirkung.max_stufe(gebaut)
            erlaubt, warum = gelaende.bau_moeglich(gebaut, art)
            tk.Label(info, text=f"Hier steht: {gelaende.gebaeude_name(gebaut)} — "
                                f"{gebaeude_wirkung.stufen_name(gebaut, stufe)} ({warum})",
                     fg=self.skin["text"], bg=self.skin["panel"], wraplength=780,
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
                kosten = baukosten(gebaut, stufe + 1)
                tk.Button(knopfreihe, text=f"Ausbauen auf Stufe {stufe + 1} ({kosten_text(kosten)})",
                          command=self._karten_ausbauen, bg=self.skin["button"],
                          fg=self.skin["gold"], activebackground="#5D4037").pack(side=tk.LEFT)
            tk.Button(knopfreihe, text="Abreißen", command=self._karten_abreissen, bg="#3e2723",
                      fg=self.skin["gold"]).pack(side=tk.LEFT, padx=6)
            return

        passend = [(k, g) for k, g in sorted(gelaende.alle_gebaeude().items(),
                                             key=lambda x: x[1]["name"])
                   if gelaende.bau_moeglich(k, art)[0]]
        if not passend:
            tk.Label(info, text="Auf diesem Gelände kann nichts gebaut werden.",
                     fg=self.skin["text"], bg=self.skin["panel"]).pack(anchor=tk.W, padx=6, pady=6)
            return

        tk.Label(info, text=f"Hier möglich ({len(passend)} Gebäude):", fg=self.skin["text"],
                 bg=self.skin["panel"]).pack(anchor=tk.W, padx=6)
        knopfreihe = tk.Frame(info, bg=self.skin["panel"])
        knopfreihe.pack(anchor=tk.W, padx=6, pady=6)
        for i, (k, g) in enumerate(passend):
            kosten = baukosten(k)
            tk.Button(knopfreihe, text=f"{g['name']}  ({kosten_text(kosten)})",
                      command=lambda kk=k: self._karten_bauen(kk), bg=self.skin["button"],
                      fg=self.skin["gold"], activebackground="#5D4037").grid(
                row=i // 3, column=i % 3, padx=3, pady=2, sticky=tk.W)

    def _dimensionsname(self, z: int) -> str:
        """Der Name einer Dimension aus dem Limbus-Raster (`src/portalraum.py`)."""
        eintraege = portalraum.dimensionen()
        nummer = int(z)
        if 1 <= nummer <= len(eintraege):
            return str(eintraege[nummer - 1].get("name") or f"Dimension {nummer:02d}")
        return f"unbekannte Dimension {z}"

    def _sperre_text(self) -> str:
        """Restzeit bis zum naechsten Koordinatenwechsel (belegte 24-Stunden-Sperre)."""
        if self.state.letzter_wechsel is None:
            return "noch nie gewechselt"
        reste = 24 * 3600 - (time.time() - float(self.state.letzter_wechsel))
        if reste <= 0:
            return "abgelaufen"
        return f"noch {reste / 3600.0:.2f} h"

    def _portal_wechsel(self, nach_z: int):
        """Ein Koordinatenwechsel: erst pruefen, dann GENAU EINMAL abbuchen (W5-2)."""
        von_z = int(self.state.eigene_dimension)
        mana = float(self.state.resources["mana"].amount)
        erlaubt, meldung = portalraum.wechsel_erlaubt(von_z, nach_z, mana,
                                                      self.state.letzter_wechsel, time.time())
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
        meldung = (f"Koordinatenwechsel nach Dimension {nach_z:02d} "
                   f"({self._dimensionsname(nach_z)}): {gebucht['kosten']} Mana abgebucht, "
                   f"24 Stunden gesperrt.")
        self._log(meldung)
        self.state.messages.append({"text": meldung, "type": "portal"})
        self._render_view()
        return True

    def _render_portal(self):
        """Portalansicht aus `portalraum.py` (W5-2): das 20x20-Raster des Limbus.

        Eigene Dimensionen sind gruen, fremde rot — wörtlich belegt (portal.php 2005: „Eure Welt
        wird durch ein gruenes Banner markiert, fremde Welten durch rote"). `portalfarbe` liefert
        die Farbe als WORT; hier wird sie in eine Tk-Farbe übersetzt.
        """
        farben = {"gruen": "#2ecc40", "rot": "#e53935"}
        tk.Label(self.content, text="Portal", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        tk.Label(self.content, text=portalraum.beschreibung(), fg="#C0C0C0", bg=self.skin["bg"], wraplength=760, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=(0, 6))

        z = int(self.state.eigene_dimension)
        eigene = list(self.state.eigene_dimensionen)
        felder = portalraum.anzeige_raster(z, 10, eigene)
        kante = portalraum._achsen()
        tk.Label(self.content, text=f"Dimension {z:02d} — {self._dimensionsname(z)} "
                                    f"({'eigene Welt (gruen)' if z in eigene else 'fremde Welt (rot)'})",
                 fg="#DAA520", bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)
        zeichenflaeche = tk.Canvas(self.content, width=400, height=400, bg=self.skin["bg"], highlightthickness=0)
        zeichenflaeche.pack(anchor=tk.W, padx=10, pady=4)
        zelle = max(4, 400 // max(1, kante))
        for feld in felder:
            x1, y1 = feld["x"] * zelle, feld["y"] * zelle
            zeichenflaeche.create_rectangle(x1, y1, x1 + zelle, y1 + zelle,
                                            fill=farben.get(feld["farbe"], "#555555"), outline="#111111")

        mana = float(self.state.resources["mana"].amount)
        erlaubt, meldung = portalraum.wechsel_erlaubt(z, z, mana, self.state.letzter_wechsel, time.time())
        tk.Label(self.content, text=f"Mana: {int(mana)} · Wechsel kostet {portalraum.wechselkosten()} "
                                    f"· Sperre: {self._sperre_text()}",
                 fg=self.skin["text"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(4, 2))
        tk.Label(self.content, text=("Koordinatenwechsel möglich." if erlaubt else f"Zurzeit nicht möglich: {meldung}"),
                 fg="#DAA520" if erlaubt else self.skin["red"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)
        tk.Label(self.content, text="(Unser Mana liegt in EINEM gemeinsamen Vorrat — das Handbuch verlangt "
                                    "die 5.000 Mana aus einer Siedlung. Vermerkt, noch nicht je Siedlung.)",
                 fg="#8a8a8a", bg=self.skin["bg"], wraplength=760, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=(0, 6))

        knopfreihe = tk.Frame(self.content, bg=self.skin["bg"])
        knopfreihe.pack(anchor=tk.W, padx=10, pady=2)
        for eintrag in portalraum.dimensionen():
            nummer = int(str(eintrag["kennung"]).lstrip("d"))
            eigen = nummer in eigene
            tk.Button(knopfreihe, text=f"{nummer:02d}", width=3,
                      bg="#1b5e20" if eigen else "#7f1d1d", fg=self.skin["gold"],
                      command=lambda n=nummer: self._portal_wechsel(n)).pack(side=tk.LEFT, padx=1, pady=1)

        tk.Label(self.content, text="Welten anderer Spieler:", fg="#C0C0C0", bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 0))
        for bot in self.state.bots:
            frame = tk.Frame(self.content, bg=self.skin["panel"])
            frame.pack(fill=tk.X, padx=10, pady=2)
            tk.Label(frame, text=bot.name, fg=self.skin["text"], bg=self.skin["panel"], width=15, anchor=tk.W).pack(side=tk.LEFT, padx=5)
            tk.Label(frame, text=f"Fraktion: {bot.faction}", fg="#DAA520", bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
            tk.Button(frame, text="Besuchen", command=lambda b=bot: self._visit_bot(b), bg="#3e2723", fg=self.skin["gold"]).pack(side=tk.RIGHT, padx=5)

    def _visit_bot(self, bot: BotPlayer):
        self._log("Besuche andere Spielerwelten nicht im Singleplayer-Modus.")

    def _render_storage(self):
        print("[DEBUG] _render_storage called")
        tk.Label(self.content, text="Lager", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        tk.Label(self.content, text="Waren und Einheiten in dieser Siedlung.", fg=self.skin["text"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)
        tk.Label(self.content, text="Waren (die 17 Originalwaren aus data/items.json):", fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 0))
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
        tk.Label(self.content, text="Einheiten:", fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 0))
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

        # W3: die Werkstaetten. Gezeigt wird nur, was WIRKLICH auf der Siedlungskarte steht
        # (`werkstatt.werkstaetten_bestand`), je Ware mit ihrer belegten Voraussetzung.
        tk.Label(self.content, text="Werkstätten:", fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 0))
        schlangen = self.state.werkstatt_schlangen()
        if not schlangen:
            tk.Label(self.content, text="Noch keine Werkstatt gebaut — auf der Siedlungskarte bauen.",
                     fg="#8a8a8a", bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)
        for kennung, schlange in sorted(schlangen.items()):
            rahmen = tk.Frame(self.content, bg=self.skin["panel"])
            rahmen.pack(fill=tk.X, padx=10, pady=3)
            tk.Label(rahmen, text=f"{schlange.get('werkstatt')} ({schlange.get('kapazitaet')} Plätze)",
                     fg=self.skin["text"], bg=self.skin["panel"], width=24, anchor=tk.W).pack(side=tk.LEFT, padx=5)
            for ware in werkstatt.waren_der_werkstatt(kennung):
                erfuellt, grund = self.state.ware_voraussetzung(ware)
                knopf = tk.Button(rahmen, text=ware, command=lambda k=kennung, w=ware: self._ware_herstellen(k, w),
                                  bg="#3e2723" if erfuellt else "#4a4a4a",
                                  fg=self.skin["gold"] if erfuellt else "#9e9e9e")
                if not erfuellt:
                    knopf.config(state=tk.DISABLED)
                knopf.pack(side=tk.LEFT, padx=2)
            tk.Label(self.content, text="   " + werkstatt.fortschritt(schlange, time.time())["text"],
                     fg="#C0C0C0", bg=self.skin["bg"]).pack(anchor=tk.W, padx=12)

    def _ware_herstellen(self, kennung: str, ware: str):
        """Eine Ware in die Warteschlange EINER Werkstatt stellen (W3).

        Ablauf wie im Rueckruf-Vertrag: erst pruefen (Werkstatt gebaut? Voraussetzung erfuellt?),
        dann einreihen; abgelehnt wird VOR jeder Aenderung.
        """
        schlange = self.state.werkstatt_schlangen().get(kennung)
        if not schlange:
            self._log(f"Keine Werkstatt '{kennung}' gebaut - zuerst auf der Siedlungskarte bauen.")
            return False
        erfuellt, grund = self.state.ware_voraussetzung(ware)
        if not erfuellt:
            self._log(f"{ware} nicht möglich: {grund}")
            return False
        stufe = 1
        for siedlung in self.state.settlements:
            stufe = max(stufe, werkstatt.werkstatt_stufe(siedlung, kennung))
        werkstatt.fortschritt(schlange, time.time())     # die Uhr stellen, bevor eingereiht wird
        ok, meldung = werkstatt.einreihen(schlange, ware, 1, stufe)
        self._log(meldung)
        if ok:
            self._render_view()
        return ok

    def _render_profiles(self):
        tk.Label(self.content, text="Spielerprofile", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        tk.Label(self.content, text="Erstelle ein Profil über dich oder deinen Charakter.", fg="#C0C0C0", bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)
        tk.Entry(self.content, bg=self.skin["panel"], fg=self.skin["text"], insertbackground="#F5F5DC").pack(anchor=tk.W, padx=10, pady=10)
        tk.Button(self.content, text="Profil speichern", bg="#3e2723", fg=self.skin["gold"], command=self._save_profile).pack(anchor=tk.W, padx=10, pady=5)
        self.lbl_profile = tk.Label(self.content, text="Kein Profil gespeichert.", fg="#DAA520", bg=self.skin["bg"])
        self.lbl_profile.pack(anchor=tk.W, padx=10, pady=5)

    def _save_profile(self):
        self._log("Profil gespeichert. Noch ohne dauerhafte Speicherung.")

    def _render_maps(self):
        tk.Label(self.content, text="Karten", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        cfg = next(m for m in MAPS if m["id"] == self.state.current_map)
        size = cfg["size"]
        frame = tk.Frame(self.content, bg=self.skin["panel"])
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.map_canvas = tk.Canvas(frame, width=520, height=520, bg=self.skin["bg"], highlightthickness=0)
        self.map_canvas.pack()
        self.map_canvas.bind("<Button-1>", self._on_map_click)
        self._map_size = size
        self._show_buildings = True
        tk.Button(self.content, text="Keine Gebäude", command=self._toggle_buildings, bg=self.skin["button"], fg=self.skin["gold"]).pack(anchor=tk.W, padx=10, pady=(2, 6))
        self._render_map_controls()
        self._draw_map(size)

    def _render_map_controls(self):
        """Kartenliste mit Betreten/Stationieren/Angreifen/Zerstören."""
        ctrl = tk.Frame(self.content, bg=self.skin["panel"])
        ctrl.pack(fill=tk.X, padx=10, pady=(0, 10))
        tk.Label(ctrl, text="Kartenverwaltung", fg=self.skin["gold"], bg=self.skin["panel"]).pack(anchor=tk.W, padx=5, pady=(4, 2))
        for m in MAPS:
            row = tk.Frame(ctrl, bg=self.skin["panel"])
            row.pack(fill=tk.X, padx=5, pady=1)
            if m["id"] in self.state.active_maps:
                status = "aktiv (hier)" if m["id"] == self.state.current_map else "aktiv"
            elif m["id"] in self.state.unlocked_maps:
                status = "freigeschaltet"
            else:
                status = "gesperrt"
            garrison = sum(self.state.map_garrison.get(m["id"], {}).values())
            tk.Label(row, text=f"{m['name']} [{status}] Besatzung: {garrison}",
                     fg=self.skin["text"], bg=self.skin["panel"], width=40, anchor=tk.W).pack(side=tk.LEFT, padx=2)
            if m["id"] in self.state.active_maps:
                if m["id"] != self.state.current_map:
                    tk.Button(row, text=f"Betreten ({self.state.map_switch_cost} 💰)",
                              command=lambda mid=m["id"]: self._enter_map(mid),
                              bg="#3e2723", fg=self.skin["gold"]).pack(side=tk.RIGHT, padx=2)
                tk.Button(row, text="Stationieren", command=lambda mid=m["id"]: self._station_on_map(mid),
                          bg="#3e2723", fg=self.skin["gold"]).pack(side=tk.RIGHT, padx=2)
                if m["id"] != "kontinent":
                    tk.Button(row, text="Angreifen", command=lambda mid=m["id"]: self._attack_map(mid),
                              bg="#3e2723", fg=self.skin["red"]).pack(side=tk.RIGHT, padx=2)
                    tk.Button(row, text="Zerstören", command=lambda mid=m["id"]: self._destroy_map(mid),
                              bg="#3e2723", fg=self.skin["red"]).pack(side=tk.RIGHT, padx=2)
            else:
                tk.Label(row, text="Portal ausbauen oder Vermessung erforschen",
                         fg="#8a8a8a", bg=self.skin["panel"]).pack(side=tk.RIGHT, padx=5)

    def _enter_map(self, map_id: str):
        self._activate_map(map_id)
        self._render_view()

    def _destroy_map(self, map_id: str):
        self.state.destroy_map(map_id)
        self._render_view()

    def _toggle_buildings(self):
        self._show_buildings = not self._show_buildings
        cfg = next(m for m in MAPS if m["id"] == self.state.current_map)
        self._draw_map(cfg["size"])

    def _draw_map(self, size: int):
        if not hasattr(self, "map_canvas"):
            return
        self.map_canvas.delete("all")
        w = 520
        h = 520
        cell_w = w / size
        cell_h = h / size
        colors = {
            "forest": "#1b5e20", "plains": "#33691e", "mountain": "#4e342e",
            "water": "#0d47a1", "village": "#ff8f00", "ruins": "#4a148c"
        }
        icons = {
            "forest": "🌲", "plains": "🌾", "mountain": "⛰️",
            "water": "🌊", "village": "🏠", "ruins": "🏚️"
        }
        for tile in self.state.map_tiles:
            x1 = tile.x * cell_w
            y1 = tile.y * cell_h
            x2 = x1 + cell_w
            y2 = y1 + cell_h
            color = colors.get(tile.terrain, "#111")
            self.map_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#000")
            if tile.npc_faction or tile.quest or tile.resources:
                symbol = icons.get(tile.terrain, "?")
                self.map_canvas.create_text(x1 + cell_w/2, y1 + cell_h/2, text=symbol, fill="#fff", font=("Arial", int(min(cell_w, cell_h)/2.5)))
            if tile.sector_name:
                self.map_canvas.create_text(x1 + 2, y1 + 2, text=tile.sector_name, anchor=tk.NW, fill="#FFD700", font=("Arial", 7))
        # movements
        now = time.time()
        for m in self.state.movements[:]:
            remaining = max(0, int(m["arrival"] - now))
            if remaining <= 0:
                continue
            mins, secs = divmod(remaining, 60)
            hours, mins = divmod(mins, 60)
            timer_txt = f"{hours:02d}:{mins:02d}:{secs:02d}"
            # draw marker on target
            tx, ty = m["to"].split(":")
            cx = int(tx) * cell_w + cell_w/2
            cy = int(ty) * cell_h + cell_h/2
            self.map_canvas.create_text(cx, cy, text=f"⚔️{timer_txt}", fill="#FFD700", font=("Arial", 8))

    # ---------- Angriff: kampf + kampfbericht (Umsetzungsplan, Abschnitte 1.3 und 2) ----------
    #
    # Vorher rechnete die Oberflaeche mit einer eigenen Daumenformel ("mehr Kampfkraft als der
    # Verteidiger") und erfand Beute. Jetzt laeuft JEDER Angriff durch denselben Ablauf:
    # Truppenpruefung -> Vorrunde/Wallschwellen -> bis zu zehn Kampfsequenzen -> Beute nach
    # Karrenladung -> Bericht in den Reiter "Nachrichten" -> Verluste und Beute in den Spielstand.

    def _truppen_nach_rolle(self):
        """Teilt die eigenen Einheiten in die Rollen des Handbuchs (einheiten.py)."""
        kaempfer, belagerung, karren = {}, {}, {}
        for kennung, einheit in self.state.units.items():
            if einheit.count <= 0:
                continue
            rolle = einheit.rolle or einheiten.rolle(kennung)
            if rolle in ("kaempfer", "kundschafter"):
                kaempfer[kennung] = einheit.count
            elif rolle == "belagerung":
                belagerung[kennung] = einheit.count
            elif rolle == "karren":
                karren[kennung] = einheit.count
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

    def _angriff_durchfuehren(self, ziel_name: str, verteidiger: dict, wall_stufe: int = 0,
                              wall_zustand: float = 100.0, vorraete=None,
                              verteidiger_karren=None, vorrat_ziel=None) -> bool:
        """Ein Angriff vom Klick bis zum Bericht (Umsetzungsplan, Abschnitt 2).

        Gibt ``False`` zurueck, wenn gar nicht gekaempft wurde (keine Truppen). Der Spielstand
        wird nur bei einem wirklich durchgefuehrten Angriff veraendert.
        """
        kaempfer, belagerung, karren = self._truppen_nach_rolle()
        if not kaempfer and not belagerung:
            # Belegter Wortlaut (spielschicht.py:525-526): ohne Schlagkraft kein Angriff.
            meldung = "Keine Kaempfer und keine Belagerungswaffen vorhanden."
            self.state.messages.append({"text": meldung, "type": "kampf"})
            self._log(meldung)
            return False

        angreifer = dict(kaempfer)
        angreifer.update(belagerung)
        if vorraete is None:
            vorraete = self._vorraete_des_ziels(vorrat_ziel if vorrat_ziel is not None else {})

        ergebnis = kampf.fuehre_schlacht(
            angreifer, dict(verteidiger or {}), int(wall_stufe), float(wall_zustand),
            angreifer_karren=karren or None, verteidiger_karren=verteidiger_karren or None,
            vorraete=dict(vorraete or {}), rng=random.Random())

        # Verluste und Beute in den Spielstand buchen (kampfbericht rechnet, main.py schreibt).
        vorher = {"ressourcen": {k: v.amount for k, v in self.state.resources.items()},
                  "einheiten": {k: v.count for k, v in self.state.units.items()}}
        neu = kampfbericht.spieldaten_anwenden(vorher, ergebnis)
        for stoff, menge in neu.get("ressourcen", {}).items():
            if stoff in self.state.resources:
                self.state.resources[stoff].amount = float(menge)
        for kennung, anzahl in neu.get("einheiten", {}).items():
            if kennung in self.state.units:
                self.state.units[kennung].count = max(0, int(anzahl))

        bericht = kampfbericht.bericht(ergebnis)
        self.state.messages.append(
            {"text": bericht["titel"] + "\n" + "\n".join(bericht["zeilen"]), "type": "kampf"})
        self._log(f"{bericht['titel']} — Ziel {ziel_name}, Ausgang {ergebnis.get('ausgang')}.")
        return True

    def _attack_map(self, map_id: str):
        ziel = next((m for m in MAPS if m["id"] == map_id), None)
        garrison = dict(self.state.map_garrison.get(map_id, {}) or {})
        self._angriff_durchfuehren(ziel["name"] if ziel else map_id, garrison,
                                   wall_stufe=0, wall_zustand=100.0, vorrat_ziel=ziel or map_id)

    def _activate_map(self, map_id: str):
        if map_id not in self.state.active_maps:
            self._log("Karte nicht aktiv.")
            return
        if self.state.current_map == map_id:
            self._log("Bereits auf dieser Karte.")
            return
        if self.state.resources["gold"].amount < self.state.map_switch_cost:
            self._log("Nicht genug Geld für Kartenwechsel.")
            return
        self.state.resources["gold"].amount -= self.state.map_switch_cost
        self.state.current_map = map_id
        self.state.generate_map(map_id)
        self.state.map_switch_cost += 50
        self._log(f"Gewechselt zu {map_id}. Nächster Wechsel: {self.state.map_switch_cost}")

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
        cfg = next(m for m in MAPS if m["id"] == self.state.current_map)
        size = cfg["size"]
        w = self.map_canvas.winfo_width()
        h = self.map_canvas.winfo_height()
        if w < 10 or h < 10:
            return
        cell_w = w / size
        cell_h = h / size
        x = int(event.x / cell_w)
        y = int(event.y / cell_h)
        tile = self.state.get_tile(x, y, size)
        if tile:
            tile.discovered = True
            if cfg.get("sectors") and tile.sector_name:
                label = f"Sektor {tile.sector_name} ({tile.sector})"
            else:
                label = f"Karte {x},{y}"
            if tile.resources:
                msg = ", ".join(f"{k}: {int(v)}" for k, v in tile.resources.items())
                self._log(f"{label}: {tile.terrain} — {msg}")
            elif tile.npc_faction:
                self._log(f"{label}: {tile.terrain} — NPC: {tile.npc_faction}")
            elif tile.quest and not tile.quest_done:
                tile.quest_done = True
                self.state.ruf += 15
                self.state.resources["gold"].amount += 20
                self._log(f"Quest abgeschlossen: {tile.quest}. Ruf +15, Geld +20")
            else:
                self._log(f"{label}: {tile.terrain}")
            # original movement
            if hasattr(self, "_pending_move"):
                _, start_tile = self._pending_move
                if abs(start_tile.x - x) + abs(start_tile.y - y) == 1:
                    # FIX 5: Truppen fuer Bewegung abbuchen (Klon-Exploit verhindern)
                    moving = {u: self.state.units[u].count for u in self.state.units if self.state.units[u].count > 0}
                    units = {u: max(1, c) for u, c in moving.items()}
                    if sum(units.values()) > 0:
                        for u, c in units.items():
                            self.state.units[u].count = max(0, self.state.units[u].count - c)
                        distance = abs(start_tile.x - x) + abs(start_tile.y - y)
                        duration = max(2, distance * 5)
                        target_map = self.state.current_map
                        target_bot = None
                        for bot in self.state.bots:
                            if random.random() < 0.3:
                                target_bot = bot
                                break
                        self.state.movements.append({
                            "from": f"{start_tile.x}:{start_tile.y}",
                            "to": f"{x}:{y}",
                            "units": units,
                            "arrival": time.time() + duration * 60,
                            "map": target_map,
                            "target_bot": target_bot.name if target_bot else None,
                            "tile_key": f"{x}:{y}",
                        })
                        self._log(f"Truppen bewegen nach {x}:{y}. Ankunft in {duration} Minuten.")
                del self._pending_move
                self._render_view()
            else:
                self._pending_move = ("move", tile)

    def _render_diplomacy(self):
        tk.Label(self.content, text="Diplomatie", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        for bot in self.state.bots:
            frame = tk.Frame(self.content, bg=self.skin["panel"])
            frame.pack(fill=tk.X, padx=10, pady=2)
            tk.Label(frame, text=bot.name, fg=self.skin["text"], bg=self.skin["panel"], width=15, anchor=tk.W).pack(side=tk.LEFT, padx=5)
            tk.Label(frame, text=f"Handel: {int(bot.trading*100)}%", fg="#DAA520", bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
            tk.Label(frame, text=f"Aggression: {int(bot.aggression*100)}%", fg=self.skin["red"], bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
            tk.Button(frame, text="Handeln", command=lambda b=bot: self._trade(b), bg="#3e2723", fg=self.skin["gold"]).pack(side=tk.RIGHT, padx=5)
            tk.Button(frame, text="Angreifen", command=lambda b=bot: self._attack(b), bg="#3e2723", fg=self.skin["red"]).pack(side=tk.RIGHT, padx=5)
            # W7 (Auftrags-Oberflaeche): EIN Angriff als Auftrag - mit Reisezeit, Rueckkehr und
            # Bericht in den Nachrichten. Der Name ist die Vorgabe aus der Uebergabe.
            tk.Button(frame, text="Angriff entsenden",
                      command=lambda b=bot: self._auftrag_angriff(b),
                      bg="#3e2723", fg=self.skin["gold"]).pack(side=tk.RIGHT, padx=5)

    def _trade(self, bot: BotPlayer):
        if bot.trading <= 0.3:
            self._log(f"{bot.name} handelt nicht.")
            return
        levels = {k: v.level for k, v in self.state.research.items()}
        bonus = get_trade_bonus(levels)
        gains = {"holz": random.randint(15, 35), "stein": random.randint(10, 30), "nahrung": random.randint(20, 40)}
        res = random.choice(list(gains.keys()))
        gain = int(gains[res] * bonus)
        self.state.resources[res].amount += gain
        self.state.ruf += 2
        self._log(f"Handel mit {bot.name}: +{gain} {res}")

    def _attack(self, bot: BotPlayer):
        if self.state.noob_protection and bot.noob_protection:
            self._log(f"{bot.name} steht unter Noobschutz. Angriff nicht möglich.")
            return
        # W2/W2b: kein Daumenvergleich mehr, sondern der Originalablauf. Die Verteidiger sind
        # die Armee des Bots, seine Vorraete liefert `_vorraete_des_ziels` (bis Schritt 8 aus
        # den VORSCHLAG-Spannen in botkern, danach aus dem Bot selbst). Einen Wall hat ein Bot
        # in unseren Daten nicht - also Stufe 0, ehrlich, ohne erfundenen Wert.
        self._angriff_durchfuehren(bot.name, dict(bot.army or {}), wall_stufe=0,
                                   wall_zustand=100.0, vorrat_ziel=bot)

    # ---------- W7: Auftraege (Missionen) in der Oberflaeche ----------

    def _auftrag_entfernung(self, siedlung=None) -> float:
        """Die Entfernung eines Auftrags in Feldern.

        Das Modul rechnet 1 Feld = 1 Stunde bei Geschwindigkeit 1 (VORSCHLAG; das Handbuch nennt
        nur Beispielstunden). Bot-Siedlungen fuehren bei uns **keine** Koordinaten — es gilt
        deshalb die Kartenmitte als Zielort. Das ist eine Annahme und steht so im Bericht.
        """
        cfg = next((m for m in MAPS if m["id"] == self.state.current_map), None)
        mitte = int(cfg["size"]) // 2 if cfg else 10
        start = siedlung or (self.state.settlements[0] if self.state.settlements else None)
        if start is None:
            return float(max(1, mitte))
        return float(max(1, abs(int(start.x) - mitte) + abs(int(start.y) - mitte)))

    def _auftrag_angriff(self, bot: BotPlayer):
        """Einen Angriff als AUFTRAG entsenden: mit Reisezeit, Rueckkehr und Bericht (W7)."""
        if not self.state.settlements:
            self._log("Für einen Auftrag braucht es zuerst eine eigene Siedlung.")
            return False
        kaempfer, belagerung, karren = self._truppen_nach_rolle()
        truppen = dict(kaempfer)
        truppen.update(belagerung)
        truppen.update(karren)          # Transportkarren tragen die Beute (Handbuch S. 23)
        if not truppen:
            self._log("Keine Kaempfer und keine Belagerungswaffen vorhanden.")
            return False
        ziel = {"name": bot.name, "fremd": True, "wall_stufe": 0, "wall_zustand_prozent": 100.0,
                "vorraete": self._vorraete_des_ziels(bot)}
        entfernung = self._auftrag_entfernung()
        ok, meldung = self.state.auftrag_starten("angreifen", truppen,
                                                 self.state.settlements[0].name, ziel, entfernung)
        text = meldung if ok else f"Auftrag nicht gestartet: {meldung}"
        self.state.messages.append({"text": text, "type": "auftrag"})
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
            rng=random.Random())
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
        wall_stufe = gebaeude_wirkung.wall_stufe(self.state.settlements)
        total_units = sum(self.state.units[u].count for u in self.state.units)
        tk.Label(self.content, text="Ruhmeshalle", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        tk.Label(self.content, text="Eure Punkte", fg="#C0C0C0", bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)
        tk.Label(self.content, text=f"Forschung: {punkte.forschungspunkte(staende)}", fg="#DAA520", bg=self.skin["bg"]).pack(anchor=tk.W, padx=20)
        tk.Label(self.content, text=f"Krieg: {punkte.kriegspunkte(einheiten, wall_stufe)}", fg=self.skin["red"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=20)
        tk.Label(self.content, text=f"Wallstufe: {wall_stufe}", fg=self.skin["text"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=20)
        tk.Label(self.content, text=f"Truppen: {total_units}", fg=self.skin["text"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=20)
        tk.Label(self.content, text=f"Gesamt: {punkte.gesamtpunkte(staende, einheiten, wall_stufe)}", fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=20)

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
            color = "#e53935" if msg.get("type") == "kampf" else "#DAA520"
            tk.Label(self.content, text=msg["text"], fg=color, bg=self.skin["bg"], wraplength=600, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=(0, 5))

    def _render_settings(self):
        tk.Label(self.content, text="Einstellungen", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        tk.Label(self.content, text="Spieleinstellungen folgen in einer späteren Version.", fg="#C0C0C0", bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)

    def _render_help(self):
        tk.Label(self.content, text="Anleitung", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        tk.Label(self.content, text="Klicke auf die Karte, um Sektoren zu erkunden. Klicke zuerst auf ein Feld, dann auf ein Nachbarfeld, um Truppen zu bewegen.", fg="#C0C0C0", bg=self.skin["bg"], wraplength=600, justify=tk.LEFT).pack(anchor=tk.W, padx=10)

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

    def _render_research(self):
        tk.Label(self.content, text="Forschung", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        levels = {k: v.level for k, v in self.state.research.items()}
        for key, r in self.state.research.items():
            frame = tk.Frame(self.content, bg=self.skin["panel"])
            frame.pack(fill=tk.X, padx=10, pady=2)
            tk.Label(frame, text=r.name, fg=self.skin["text"], bg=self.skin["panel"], width=15, anchor=tk.W).pack(side=tk.LEFT, padx=5)
            tk.Label(frame, text=f"Stufe {r.level}/{r.max_level}", fg="#DAA520", bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
            tk.Label(frame, text=r.effect, fg="#C0C0C0", bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
            if r.level < r.max_level:
                tk.Button(frame, text="Forschen", command=lambda k=key: self._start_research(k), bg="#3e2723", fg=self.skin["gold"]).pack(side=tk.RIGHT, padx=5)

    def _start_research(self, key: str):
        # W4b-5: Forschung braucht eine Bibliothek auf einer Siedlungskarte (Handbuch Seite 12).
        erlaubt, meldung = gebaeude_wirkung.forschung_erlaubt(self.state.settlements)
        if not erlaubt:
            self._log(meldung)
            return
        r = self.state.research[key]
        # Rohstoffkosten nach Handbuch Seite 13: Stufe 1 = 50 Holz, je weitere Stufe das Doppelte.
        cost = spieldaten.forschungs_kosten(r.level + 1)
        levels = {k: v.level for k, v in self.state.research.items()}
        unbekannt = [k for k in cost if k not in self.state.resources]
        if unbekannt:
            self._log(f"Forschung nicht möglich: unbekannte Rohstoffe {unbekannt}")
            return
        if all(self.state.resources[k].amount >= v for k, v in cost.items()):
            for k, v in cost.items():
                self.state.resources[k].amount -= v
            r.level += 1
            self.state.score += 10
            self._log(f"{r.name} auf Stufe {r.level} erforscht. Kosten: {cost}")
        else:
            self._log(f"Nicht genug Ressourcen für Forschung. Benötigt: {cost}")

    def _render_barracks(self):
        tk.Label(self.content, text="Kaserne", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        tk.Label(self.content, text="Ausgebildet wird auf der Siedlungskarte (W4b-5): Kriegerakademie "
                                    "für Kampfeinheiten, Diebesgilde für Kundschafter, Stellmacher für "
                                    "Karren und Belagerungswaffen. Steht die Stätte nicht, fehlt hier "
                                    "die Schaltfläche — die Stufe der Stätte bestimmt das Tempo.",
                 fg="#C0C0C0", bg=self.skin["bg"], wraplength=780,
                 justify=tk.LEFT).pack(anchor=tk.W, padx=10)
        for key, u in self.state.units.items():
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
            tk.Label(frame, text=f"Anzahl: {u.count}", fg="#C0C0C0", bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
            # W4b-5: Die Ausbildungsstätte steht auf der Siedlungskarte (data/units.json nennt sie
            # je Einheit). Fehlt sie, gibt es keine Schaltfläche — sondern den ehrlichen Grund.
            _da, _staette, _stufe = gebaeude_wirkung.ausbildungsstaette(self.state.settlements, key)
            if _da:
                tk.Button(frame, text=f"Ausbilden ({gelaende.gebaeude_name(_staette)} Stufe {_stufe})",
                          command=lambda k=key: self._train_unit(k), bg="#3e2723",
                          fg=self.skin["gold"]).pack(side=tk.RIGHT, padx=5)
            else:
                _fehlt = gelaende.gebaeude_name(_staette) if _staette else "Ausbildungsstätte unbekannt"
                tk.Label(frame, text=f"braucht {_fehlt}", fg="#e53935",
                         bg=self.skin["panel"]).pack(side=tk.RIGHT, padx=5)

    def _train_unit(self, key: str):
        u = self.state.units[key]
        levels = {k: v.level for k, v in self.state.research.items()}
        # W4b-5: Ausgebildet wird in der Stätte, die zu dieser Einheit gehört (data/units.json):
        # Kriegerakademie, Diebesgilde oder Stellmacher. Ohne sie gibt es keine Ausbildung, und
        # die STUFE der Stätte bestimmt das Tempo (vorher: erfundene Kaserne, Stufe global).
        da, staette, stufe = gebaeude_wirkung.ausbildungsstaette(self.state.settlements, key)
        if not da:
            fehlt = gelaende.gebaeude_name(staette) if staette else "Ausbildungsstätte unbekannt"
            self._log(f"{u.name} braucht {fehlt} auf einer Siedlungskarte — noch nicht gebaut.")
            return
        building_level = stufe
        time_min = get_training_time(key, levels, building_level)
        cost = u.cost
        # Siedler sind im Original die Bevoelkerung, keine lagerbare Ressource
        # (Handbuch Seite 10): der Siedleranteil wird von der Bevoelkerung bezahlt.
        siedler = int(cost.get("siedler", 0))
        rohstoffe = {k: v for k, v in cost.items() if k != "siedler"}
        unbekannt = [k for k in rohstoffe if k not in self.state.resources]
        if unbekannt:
            # Kein stilles Ueberspringen: ein unbekannter Rohstoff ist ein Datenfehler.
            self._log(f"Ausbildung nicht möglich: unbekannte Rohstoffe {unbekannt}")
            return
        genug = (all(self.state.resources[k].amount >= v for k, v in rohstoffe.items())
                 and self.state.population >= siedler)
        if genug:
            for k, v in rohstoffe.items():
                self.state.resources[k].amount -= v
            self.state.population -= siedler
            u.count += 1
            self._log(f"{u.name} ausgebildet. Ausbildungszeit: {time_min:.1f} min")
        else:
            self._log("Nicht genug Ressourcen für Ausbildung.")

    def _save(self):
        ok = self.state.save(self.save_path)
        if ok:
            self._log("Spiel gespeichert.")
        else:
            self._log("Speichern fehlgeschlagen - siehe vorige Meldung.")

    def _load(self):
        geladen = self.state.load(self.save_path)
        if hasattr(self, "content"):
            self._render_view()
            self._render()
        if geladen:
            self._log("Spiel geladen.")
        else:
            self._log("Laden fehlgeschlagen - der bisherige Stand bleibt stehen (siehe Meldungen).")

    def _log(self, msg: str):
        self.state._log(msg)
        print(msg)
        try:
            if hasattr(self, "lbl_status"):
                self.lbl_status.config(text=msg)
        except Exception:
            pass

    def _tick_loop(self):
        now = time.time()
        dt = now - self.state.last_tick
        if dt > 0:
            self.state.tick(dt)
        # movements arrival
        for m in self.state.movements[:]:
            if now >= m["arrival"]:
                tile_key = m.get("tile_key") or m["to"]
                x_str, y_str = tile_key.split(":")
                x, y = int(x_str), int(y_str)
                cfg = next((mm for mm in MAPS if mm["id"] == m.get("map", self.state.current_map)), None)
                size = cfg["size"] if cfg else 20
                tile = self.state.get_tile(x, y, size)
                target_bot_name = m.get("target_bot")
                if self.state.noob_protection and target_bot_name:
                    report = f"Truppen sind in {m['to']} eingetroffen. Noobschutz aktiv: keine Plünderung gegen {target_bot_name}."
                else:
                    loot = {}
                    if tile and tile.resources:
                        for res, amount in tile.resources.items():
                            gain = int(amount * random.uniform(0.1, 0.4))
                            if gain > 0:
                                loot[res] = gain
                                if res in self.state.resources:
                                    self.state.resources[res].amount += gain
                    if target_bot_name and random.random() < 0.4:
                        loss = random.randint(1, 4)
                        unit_key = random.choice(list(self.state.units.keys()))
                        self.state.units[unit_key].count = max(0, self.state.units[unit_key].count - loss)
                        report = f"Truppen sind in {m['to']} eingetroffen. Kampf gegen {target_bot_name}: Verlust {loss} {unit_key}."
                    elif loot:
                        parts = ", ".join(f"+{v} {k}" for k, v in loot.items())
                        report = f"Truppen sind in {m['to']} eingetroffen. Beute: {parts}."
                    else:
                        report = f"Truppen sind in {m['to']} eingetroffen."
                # FIX 5b: Truppen kehren nach Mission zurueck
                for u, c in m.get("units", {}).items():
                    if u in self.state.units:
                        self.state.units[u].count += c
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
            res = self.state.resources[r]
            rate = ertrag_jetzt.get(r, 0.0)
            prod_text = f"+{rate:g}/h" if rate else "0"
            lbl.config(text=f"{RESOURCE_ICONS[r]} {int(res.amount)} ({prod_text})")
        self.lbl_day.config(text=f"Tag {self.state.day}")
        # W6: die Punktanzeige kommt aus den Originalformeln (src/punkte.py, Handbuch S. 3/5/6).
        # Vorher standen hier `score`, `ruf` und eine selbst gebaute Summe - die Gesamtzahl
        # war damit nachweislich falsch.
        staende = {k: v.level for k, v in self.state.research.items()}
        einheiten = {k: v.count for k, v in self.state.units.items()}
        wall_stufe = gebaeude_wirkung.wall_stufe(self.state.settlements)
        self.lbl_forschung.config(text=f"Forschung: {punkte.forschungspunkte(staende)}")
        self.lbl_krieg.config(text=f"Krieg: {punkte.kriegspunkte(einheiten, wall_stufe)}")
        self.lbl_gesamt.config(text=f"Gesamt: {punkte.gesamtpunkte(staende, einheiten, wall_stufe)}")


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
        app = NebelseetalApp(root)
        root.mainloop()
    finally:
        try:
            os.remove(lock_path)
        except Exception:
            pass


if __name__ == "__main__":
    main()
