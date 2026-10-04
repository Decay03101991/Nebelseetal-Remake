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
    get_military_multiplier, get_production_multiplier, get_building_cost_multiplier,
    get_training_time_multiplier, get_trade_bonus, get_defense_bonus, get_medic_redution,
    get_unit_stats, get_combat_power, get_building_cost, get_training_time, get_map_switch_cost,
    UNIT_BASE, UNIT_TRAIN_BASE, BUILDING_BASE_COST, TIER_SCALE,
)


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
    "eisenbarren": Goods("Eisenbarren", "🔩", {"eisen": 40}, "Metallverarbeitung."),
    "stoffballen": Goods("Stoffballen", "🧶", {"stoff": 30}, "Textil."),
    "glas": Goods("Glas", "🔮", {"kristall": 30}, "Magisches Glas."),
    "goldmünzen": Goods("Goldmünzen", "🪙", {"geld": 50}, "Währung."),
    "buch": Goods("Buch", "📕", {"wissen": 40}, "Wissen aufschreiben."),
    "zaubertrank": Goods("Zaubertrank", "🧪", {"kristall": 30, "wissen": 20}, "Magisch."),
    "schwert": Goods("Schwert", "⚔️", {"eisen": 40, "holz": 20}, "Waffe."),
    "rüstung": Goods("Rüstung", "🛡️", {"eisen": 50, "leder": 30}, "Schutz."),
    "pfeil": Goods("Pfeil", "➳", {"holz": 20, "eisen": 10}, "Munition."),
    "katapultmunition": Goods("Katapultmunition", "💣", {"stein": 30, "holz": 20}, "Belagerung."),
    "medizin": Goods("Medizin", "💉", {"wissen": 20, "kristall": 15}, "Heilung."),
    "seide": Goods("Seide", "👘", {"stoff": 40, "geld": 30}, "Luxus."),
    "trank": Goods("Trank", "🧪", {"kristall": 20, "nahrung": 10}, "Stärkung."),
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


# ---------- Config ----------

RESOURCES = ["holz", "stein", "nahrung", "kristall", "gold", "eisen", "leder", "stoff", "geld", "wissen"]
RESOURCE_ICONS = {
    "holz": "🌲", "stein": "🪨", "nahrung": "🌾", "kristall": "🔮", "gold": "💎",
    "eisen": "⛏️", "leder": "🦬", "stoff": "🧵", "geld": "💰", "wissen": "📖"
}
UNIT_ICONS = {
    "siedler": "assets/icons/original_units/Soldat.png",
    "krieger": "assets/icons/original_units/Krieger.png",
    "bogenschütze": "assets/icons/original_units/Einfacher Bogenschütze.png",
    "reiter": "assets/icons/original_units/Zweispänner.png",
    "mönch": "assets/icons/original_units/Krieger.png",
    "golem": "assets/icons/original_units/Paladin.png",
    "spion": "assets/icons/original_units/Kämpfer.png",
    "katapult": "assets/icons/original_units/Katapult.png",
    "mauerbrecher": "assets/icons/original_units/Karren.png",
    "trebuchet": "assets/icons/original_units/Einfacher Belagerungsturm.png",
    "speerträger": "assets/icons/original_units/Soldat.png",
    "schwertkämpfer": "assets/icons/original_units/Kämpfer.png",
    "armbrustschütze": "assets/icons/original_units/Armbrustschütze.png",
    "lanzenreiter": "assets/icons/original_units/Zweispänner.png",
    "bogenschütze_beritten": "assets/icons/original_units/HandelsKarawane.png",
    "pikeniere": "assets/icons/original_units/Soldat.png",
    "schwere_kavallerie": "assets/icons/original_units/Paladin.png",
    "belagerungsturm": "assets/icons/original_units/Einfacher Belagerungsturm.png",
    "worg": "assets/icons/original_units/Kämpfer.png",
    "hexe": "assets/icons/original_units/Krieger.png",
    "drache": "assets/icons/original_units/Ritter.png",
    "zauberer": "assets/icons/original_units/Krieger.png",
    "schamane": "assets/icons/original_units/Kämpfer.png",
    "geist": "assets/icons/original_units/elfen_portrait.png",
    "riese": "assets/icons/original_units/Paladin.png",
    "wächter": "assets/icons/original_units/Ritter.png",
    "bote": "assets/icons/original_units/Siedlungskarren.png",
    "troll": "assets/icons/original_units/Kämpfer.png",
    "schildmaid": "assets/icons/original_units/Armbrustschütze.png",
    "skalde": "assets/icons/original_units/Händler.png",
    "bär": "assets/icons/original_units/Paladin.png",
    "adler": "assets/icons/original_units/elfen_portrait.png",
    "wolf": "assets/icons/original_units/Kämpfer.png",
    "goblin": "assets/icons/original_units/Kämpfer.png",
    "ork": "assets/icons/original_units/Krieger.png",
    "skelett": "assets/icons/original_units/Kämpfer.png",
}
MAX_ACTIVE_MAPS = 5
BUILDINGS: Dict[str, Building] = {
    "holzfäller": Building("holzfäller", "Holzfäller", description="Erzeugt Holz.", base_cost={"holz": 10, "stein": 5, "nahrung": 1}),
    "steinmetz": Building("steinmetz", "Steinmetz", description="Fördert Stein.", base_cost={"holz": 5, "stein": 10, "nahrung": 1}),
    "jäger": Building("jäger", "Jäger", description="Erzeugt Nahrung.", base_cost={"holz": 25, "stein": 25, "nahrung": 1}),
    "haus": Building("haus", "Haus", description="+5 Bevölkerung.", base_cost={"holz": 80, "stein": 50}),
    "schmiede": Building("schmiede", "Schmiede", description="Eisenverarbeitung.", base_cost={"holz": 40, "stein": 60, "eisen": 20}),
    "bibliothek": Building("bibliothek", "Bibliothek", description="+Forschung.", base_cost={"holz": 60, "stein": 40, "kristall": 20}),
    "markt": Building("markt", "Marktplatz", description="Handel mit Bots.", base_cost={"holz": 50, "stein": 50, "geld": 20}),
    "kaserne": Building("kaserne", "Kaserne", description="Einheitenausbildung.", base_cost={"holz": 80, "stein": 80, "eisen": 40}),
    "turm": Building("turm", "Wachturm", description="Verteidigung +", base_cost={"stein": 120, "eisen": 60}),
    "portal": Building("portal", "Portal", description="Kartenwechsel + Forschung.", base_cost={"kristall": 100, "geld": 100, "wissen": 50}),
}
UNITS: Dict[str, Unit] = {
    "siedler": Unit("siedler", "Siedler", cost={"nahrung": 50}, training_time=1.0, description="Arbeiter für neue Siedlungen."),
    "krieger": Unit("krieger", "Krieger", attack=8, defense=5, cost={"holz": 30, "eisen": 20}, training_time=2.0),
    "bogenschütze": Unit("bogenschütze", "Bogenschütze", attack=11, defense=4, cost={"holz": 40, "eisen": 15}, training_time=2.5),
    "reiter": Unit("reiter", "Reiter", attack=14, defense=7, cost={"eisen": 70, "nahrung": 50}, training_time=4.0),
    "mönch": Unit("mönch", "Mönch", attack=4, defense=3, cost={"wissen": 30, "kristall": 15}, training_time=3.0, description="Heilung/Wissen."),
    "golem": Unit("golem", "Golem", attack=18, defense=14, cost={"stein": 120, "kristall": 60}, training_time=6.0),
    "spion": Unit("spion", "Spion", attack=2, defense=2, cost={"geld": 40, "leder": 20}, training_time=1.5, description="Aufklärung/Sabotage."),
    "katapult": Unit("katapult", "Katapult", attack=25, defense=5, cost={"holz": 80, "stein": 60}, training_time=6.0, description="Belagerungswaffe."),
    "mauerbrecher": Unit("mauerbrecher", "Mauerbrecher", attack=20, defense=15, cost={"eisen": 60, "nahrung": 40}, training_time=5.5, description="Belagerungswaffe."),
    "trebuchet": Unit("trebuchet", "Trebuchet", attack=40, defense=8, cost={"holz": 120, "stein": 80, "eisen": 40}, training_time=8.0, description="Belagerungswaffe."),
    "speerträger": Unit("speerträger", "Speerträger", attack=6, defense=12, cost={"holz": 20, "eisen": 10}, training_time=1.8),
    "schwertkämpfer": Unit("schwertkämpfer", "Schwertkämpfer", attack=13, defense=6, cost={"holz": 50, "eisen": 30}, training_time=3.0),
    "armbrustschütze": Unit("armbrustschütze", "Armbrustschütze", attack=16, defense=5, cost={"holz": 60, "eisen": 25}, training_time=3.5),
    "lanzenreiter": Unit("lanzenreiter", "Lanzenreiter", attack=20, defense=10, cost={"eisen": 90, "nahrung": 60}, training_time=5.0),
    "bogenschütze_beritten": Unit("berittener Bogenschütze", "Berittener Bogenschütze", attack=19, defense=7, cost={"holz": 70, "eisen": 50}, training_time=5.5),
    "pikeniere": Unit("pikeniere", "Pikeniere", attack=9, defense=18, cost={"holz": 40, "eisen": 20}, training_time=2.5),
    "schwere_kavallerie": Unit("schwere_kavallerie", "Schwere Kavallerie", attack=28, defense=16, cost={"eisen": 140, "nahrung": 80}, training_time=7.0),
    "belagerungsturm": Unit("belagerungsturm", "Belagerungsturm", attack=22, defense=25, cost={"holz": 100, "stein": 120}, training_time=7.5, description="Belagerung."),
    "worg": Unit("worg", "Worg", attack=24, defense=6, cost={"leder": 60, "nahrung": 40}, training_time=4.5, description="Schnell."),
    "hexe": Unit("hexe", "Hexe", attack=15, defense=8, cost={"kristall": 50, "wissen": 40}, training_time=5.0, description="Magisch."),
    "drache": Unit("drache", "Drache", attack=45, defense=20, cost={"kristall": 200, "geld": 150}, training_time=12.0, description="Legendär."),
    "zauberer": Unit("zauberer", "Zauberer", attack=21, defense=10, cost={"wissen": 80, "kristall": 60}, training_time=6.5),
    "schamane": Unit("schamane", "Schamane", attack=17, defense=12, cost={"leder": 50, "kristall": 40}, training_time=5.0),
    "geist": Unit("geist", "Geist", attack=12, defense=5, cost={"kristall": 30, "stoff": 20}, training_time=3.5),
    "riese": Unit("riese", "Riese", attack=38, defense=30, cost={"stein": 180, "nahrung": 120}, training_time=10.0),
    "wächter": Unit("wächter", "Wächter", attack=10, defense=22, cost={"stein": 80, "eisen": 40}, training_time=3.0),
    "bote": Unit("bote", "Bote", attack=1, defense=1, cost={"geld": 20}, training_time=0.5, description="Nur zum Senden."),
    "troll": Unit("troll", "Troll", attack=32, defense=18, cost={"nahrung": 100, "leder": 60}, training_time=8.5),
    "schildmaid": Unit("schildmaid", "Schildmaid", attack=7, defense=20, cost={"holz": 60, "eisen": 30}, training_time=3.5, description="Verteidigungsspezialist."),
    "skalde": Unit("skalde", "Skalde", attack=5, defense=4, cost={"wissen": 50, "stoff": 20}, training_time=3.0, description="Unterstützung/Moral."),
    "bär": Unit("bär", "Bär", attack=35, defense=22, cost={"nahrung": 120, "leder": 80}, training_time=9.0),
    "adler": Unit("adler", "Adler", attack=16, defense=5, cost={"geld": 60, "stoff": 30}, training_time=3.5, description="Aufklärung."),
    "wolf": Unit("wolf", "Wolf", attack=18, defense=7, cost={"nahrung": 40, "leder": 40}, training_time=2.8, description="Schnell."),
    "goblin": Unit("goblin", "Goblin", attack=4, defense=2, cost={"nahrung": 15}, training_time=0.8),
    "ork": Unit("ork", "Ork", attack=24, defense=14, cost={"holz": 70, "eisen": 50}, training_time=5.5),
    "skelett": Unit("skelett", "Skelett", attack=10, defense=3, cost={"kristall": 20}, training_time=1.5, description="Untot."),
}
RESEARCHES: Dict[str, Research] = {
    "landwirtschaft": Research("landwirtschaft", "Landwirtschaft", max_level=5, cost={"wissen": 10}, effect="+12% Nahrung/Min"),
    "bergbau": Research("bergbau", "Bergbau", max_level=5, cost={"wissen": 10}, effect="+12% Stein/Eisen/Min"),
    "militär": Research("militär", "Militärtaktik", max_level=5, cost={"wissen": 12}, effect="+8% Angriff/Verteidigung"),
    "vermessung": Research("vermessung", "Vermessung", max_level=3, cost={"wissen": 15}, effect="Mehr Karteninformationen"),
    "handel": Research("handel", "Handel", max_level=5, cost={"wissen": 10}, effect="+8% Handelsbonus"),
    "architektur": Research("architektur", "Architektur", max_level=5, cost={"wissen": 12}, effect="-6% Baukosten"),
    "alchemie": Research("alchemie", "Alchemie", max_level=3, cost={"wissen": 20, "kristall": 15}, effect="Kristallproduktion frei"),
    "spionage": Research("spionage", "Spionage", max_level=3, cost={"wissen": 15}, effect="Mehr Spionerfolg"),
    "navigation": Research("navigation", "Navigation", max_level=3, cost={"wissen": 15}, effect="Portal effizienter"),
    "medizin": Research("medizin", "Medizin", max_level=3, cost={"wissen": 12}, effect="Weniger Verluste nach Kampf"),
    "taktik": Research("taktik", "Taktik", max_level=5, cost={"wissen": 15}, effect="+10% Angriff"),
    "verteidigung": Research("verteidigung", "Verteidigung", max_level=5, cost={"wissen": 15}, effect="+10% Verteidigung"),
    "logistik": Research("logistik", "Logistik", max_level=3, cost={"wissen": 20}, effect="Mehr Truppenkapazität"),
    "alchemie_2": Research("alchemie_2", "Alchemie II", max_level=3, cost={"wissen": 30, "kristall": 25}, effect="Mehr Kristall"),
    "wirtschaft": Research("wirtschaft", "Wirtschaft", max_level=5, cost={"wissen": 12}, effect="+10% Produktion"),
    "diplomatie": Research("diplomatie", "Diplomatie", max_level=3, cost={"wissen": 18}, effect="Handelsbonus +"),
    "magie": Research("magie", "Magie", max_level=3, cost={"wissen": 30, "kristall": 20}, effect="Magische Einheiten"),
    "zauberei": Research("zauberei", "Zauberei", max_level=3, cost={"wissen": 35, "kristall": 25}, effect="Zaubermacht"),
}
MAPS = [
    {"id": "kontinent", "name": "Der Kontinent", "size": 20, "difficulty": 1, "bonus": "nahrung", "npcs": ["dorf", "händler"], "quests": ["Erstes Zuhause", "Siedlerzug"], "sectors": True},
    {"id": "wald", "name": "Nebelwald", "size": 8, "difficulty": 2, "bonus": "holz", "npcs": ["jäger", "schamane"], "quests": ["Geister des Waldes", "Verlorenes Artefakt"]},
    {"id": "berge", "name": "Hochfels", "size": 8, "difficulty": 3, "bonus": "stein", "npcs": ["zwerge", "drachen"], "quests": ["Der verborgene Schacht", "Drachenei"]},
    {"id": "sümpfe", "name": "Glimmersümpfe", "size": 7, "difficulty": 2, "bonus": "kristall", "npcs": ["hexe", "banditen"], "quests": ["Sumpffieber", "Banditenlager"]},
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
    levels = {k: v.level for k, v in state.research.items()}
    if key == "militär":
        return get_military_multiplier(levels, get_defense_bonus(state.buildings.get("turm", Building("", "")).level))
    if key == "landwirtschaft":
        return get_production_multiplier(levels, "nahrung")
    if key == "bergbau":
        return get_production_multiplier(levels, "stein")
    if key == "handel":
        return get_trade_bonus(levels)
    if key == "architektur":
        return get_building_cost_multiplier(levels)
    return 1.0


# ---------- Game State ----------

class GameState:
    def __init__(self):
        self.resources: Dict[str, Resource] = {r: Resource(r) for r in RESOURCES}
        self.resources["holz"].amount = 10
        self.resources["stein"].amount = 10
        self.resources["nahrung"].amount = 10
        self.buildings: Dict[str, Building] = {k: Building(**asdict(v)) for k, v in BUILDINGS.items()}
        self.units: Dict[str, Unit] = {k: Unit(**asdict(v)) for k, v in UNITS.items()}
        self.research: Dict[str, Research] = {k: Research(**asdict(v)) for k, v in RESEARCHES.items()}
        self.map_tiles: List[MapTile] = []
        self.bots: List[BotPlayer] = []
        self.current_map = "kontinent"
        self.unlocked_maps: List[str] = ["kontinent"]
        self.active_maps: List[str] = ["kontinent"]
        self.map_switch_cost = 150
        self.population = 0
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

    def _unlock_next_map(self):
        if len(self.active_maps) >= MAX_ACTIVE_MAPS:
            return
        candidates = [m for m in MAPS if m["id"] not in self.unlocked_maps]
        if not candidates:
            return
        portal = self.buildings.get("portal")
        verm = self.research.get("vermessung")
        if portal and portal.level >= 1 or (verm and verm.level >= 1):
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
                        tile.resources = {"stein": random.randint(50, 150), "eisen": random.randint(20, 80)}
                    elif terrain == "ruins":
                        tile.resources = {"wissen": random.randint(30, 100), "kristall": random.randint(20, 60)}
                    elif terrain == "village":
                        tile.resources = {"nahrung": random.randint(40, 120), "geld": random.randint(10, 40)}
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
                        tile.resources = {"stein": random.randint(30, 90), "eisen": random.randint(5, 30)}
                    elif terrain == "ruins":
                        tile.resources = {"wissen": random.randint(10, 40), "kristall": random.randint(5, 20)}
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

    def tick(self, dt_seconds: float):
        dt_min = dt_seconds / 60.0
        levels = {k: v.level for k, v in self.research.items()}
        for b in self.buildings.values():
            if b.level > 0:
                for res, rate in b.production.items():
                    if res in self.resources:
                        mult = get_production_multiplier(levels, res)
                        self.resources[res].amount += rate * mult * dt_min
                        self.resources[res].amount = round(self.resources[res].amount, 2)
        for bot in self.bots:
            if bot.settlements and random.random() < 0.05 * bot.aggression:
                defense = sum(self.units[u].defense * max(1, self.units[u].count) for u in self.units)
                loss = max(0, int(get_military_multiplier(levels) * 10 * bot.aggression - get_medic_redution(levels)))
                self.resources["nahrung"].amount = max(0, self.resources["nahrung"].amount - loss)
        # FIX 2+3: Tag fortschreiben (86400s = 1 Spieltag) + Noobschutz nach Tag 3 deaktivieren
        # Bevoelkerung waechst langsam bis zum Limit (Haus erhoeht das Limit)
        haus_level = self.buildings.get("haus", Building("", "")).level
        self.max_population = 10 + 5 * haus_level
        if self.population < self.max_population:
            self.population = min(float(self.max_population), self.population + dt_min * 0.5)
        self._day_accum = getattr(self, "_day_accum", 0.0) + dt_seconds
        if self._day_accum >= 86400:
            self._day_accum -= 86400
            self.day += 1
        if self.day >= 3 and self.noob_protection:
            self.noob_protection = False
            self.messages.append({"text": "Noobschutz aufgehoben - die Welt ist jetzt gefaehrlich!", "type": "system"})
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
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load(self, path: str):
        if not os.path.exists(path):
            return
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
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

    def _log(self, msg: str):
        self.log.append(msg)
        if len(self.log) > 200:
            self.log = self.log[-200:]


# ---------- GUI ----------

class NebelseetalApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Nebelseetal Remake")
        self.root.geometry("1024x720")
        self.state = GameState()
        self.state.generate_map(self.state.current_map)
        self.save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "savegame.json")
        self.current_view = "Dorfzentrum"
        self.skin_name = "standard"
        self.skin = SKINS[self.skin_name]
        self._build_loading_screen()

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

    def _resource_building_key(self, resource: str) -> str:
        mapping = {
            "holz": "holzfäller",
            "stein": "steinmetz",
            "nahrung": "jäger",
            "kristall": "bibliothek",
            "gold": "portal",
            "eisen": "schmiede",
            "leder": "jäger",
            "stoff": "markt",
            "geld": "markt",
            "wissen": "bibliothek",
        }
        return mapping.get(resource, "")

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
        for r in RESOURCES:
            icon = RESOURCE_ICONS[r]
            amount = int(self.state.resources[r].amount)
            prod = self.state.buildings.get(self._resource_building_key(r), Building("", "")).level
            prod_text = f"+{prod}" if prod else "0"
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

        self.content = tk.Frame(main, bg=self.skin["bg"])
        self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6, pady=6)
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

    def _render_view(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        mapping = {
            "Dorfzentrum": self._render_overview,
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
        tk.Label(self.content, text=f"Bevölkerung: {int(self.state.population)} / {self.state.max_population}",
                 fg="#DAA520", bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)
        frame = tk.Frame(self.content, bg=self.skin["panel"])
        frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(frame, text="Siedlungen:", fg=self.skin["gold"], bg=self.skin["panel"]).pack(anchor=tk.W, padx=5)
        for i, s in enumerate(self.state.settlements):
            row = tk.Frame(self.content, bg=self.skin["panel"])
            row.pack(fill=tk.X, padx=10, pady=2)
            tk.Label(row, text=f"{s.name} ({s.map_id})", fg=self.skin["text"], bg=self.skin["panel"], width=20, anchor=tk.W).pack(side=tk.LEFT, padx=5)
            tk.Label(row, text=f"Gebäude: {len(s.buildings)}", fg="#DAA520", bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
            entry = tk.Entry(row, bg=self.skin["panel"], fg=self.skin["text"], width=18)
            entry.insert(0, s.name)
            entry.pack(side=tk.LEFT, padx=5)
            tk.Button(row, text="Umbenennen", command=lambda ss=s, e=entry: self._rename_settlement(ss, e.get()), bg="#3e2723", fg=self.skin["gold"]).pack(side=tk.RIGHT, padx=5)
            tk.Button(row, text="Transport", command=lambda ss=s: self._transport_to_settlement(ss), bg="#3e2723", fg=self.skin["gold"]).pack(side=tk.RIGHT, padx=5)
        tk.Button(self.content, text="Neue Siedlung gründen", command=self._found_settlement, bg="#3e2723", fg=self.skin["gold"]).pack(anchor=tk.W, padx=10, pady=10)
        for key, b in self.state.buildings.items():
            frame = tk.Frame(self.content, bg=self.skin["panel"], relief=tk.FLAT, borderwidth=1)
            frame.pack(fill=tk.X, padx=10, pady=2)
            tk.Label(frame, text=b.name, fg=self.skin["text"], bg=self.skin["panel"], width=15, anchor=tk.W).pack(side=tk.LEFT, padx=5, pady=3)
            tk.Label(frame, text=f"Stufe {b.level}", fg="#DAA520", bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
            tk.Button(frame, text="Ausbauen", command=lambda k=key: self._upgrade_building(k), bg="#3e2723", fg=self.skin["gold"], activebackground="#5D4037").pack(side=tk.RIGHT, padx=5, pady=2)

    def _upgrade_building(self, key: str):
        b = self.state.buildings[key]
        cost = get_building_cost(key, b.level, {k: v.level for k, v in self.state.research.items()})
        if all(self.state.resources[r].amount >= v for r, v in cost.items()):
            for r, v in cost.items():
                self.state.resources[r].amount -= v
            b.level += 1
            if b.id == "haus":
                self.state.max_population += 5
                b.production = {}
            elif b.id == "bibliothek":
                b.production = {"wissen": b.level * 2.0}
            elif b.id == "kaserne":
                b.production = {}
            elif b.id == "portal":
                b.production = {"wissen": b.level * 1.0}
                self._unlock_next_map()
            else:
                prod_map = {
                    "holzfäller": {"holz": b.level * 1.2},
                    "steinmetz": {"stein": b.level * 1.2},
                    "jäger": {"nahrung": b.level * 1.0},
                    "schmiede": {"eisen": b.level * 0.8},
                    "markt": {"geld": b.level * 0.5},
                    "turm": {},
                }
                b.production = prod_map.get(b.id, {})
            self._log(f"{b.name} auf Stufe {b.level} ausgebaut.")
        else:
            self._log("Nicht genug Ressourcen.")

    def _found_settlement(self):
        if len(self.state.settlements) >= 3:
            self._log("Maximale Siedlungsanzahl erreicht.")
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
                sett = Settlement(name=name, map_id=self.state.current_map, x=x, y=y)
                self.state.settlements.append(sett)
                tile.npc_faction = "spieler"
                tile.sector_name = name
                self._log(f"Neue Siedlung '{name}' auf {self.state.current_map} bei {x}:{y} gegründet.")
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

    def _render_portal(self):
        tk.Label(self.content, text="Portal", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        tk.Label(self.content, text="Freigeschaltete Karten:", fg="#C0C0C0", bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)
        tk.Label(self.content, text=f"{', '.join(self.state.unlocked_maps)}", fg="#DAA520", bg=self.skin["bg"]).pack(anchor=tk.W, padx=20)
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
        tk.Label(self.content, text="Waren:", fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 0))
        goods_frame = tk.Frame(self.content, bg=self.skin["panel"])
        goods_frame.pack(fill=tk.X, padx=10, pady=5)
        cols = 6
        for idx, (key, g) in enumerate(GOODS.items()):
            row = idx // cols
            col = idx % cols
            cell = tk.Frame(goods_frame, bg=self.skin["panel"], padx=10, pady=10, relief=tk.RIDGE, borderwidth=1)
            cell.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
            goods_frame.grid_columnconfigure(col, weight=1)
            goods_frame.grid_rowconfigure(row, weight=1)
            tk.Label(cell, text=g.icon, fg=self.skin["text"], bg=self.skin["panel"], font=("Arial", 28)).pack(pady=(0, 4))
            tk.Label(cell, text=g.name, fg=self.skin["text"], bg=self.skin["panel"], font=("Arial", 9)).pack()
            tk.Label(cell, text=str(self.state.goods.get(key, 0)), fg=self.skin["gold"], bg=self.skin["panel"], font=("Arial", 11, "bold")).pack(pady=(2, 0))
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
            icon_path = UNIT_ICONS.get(key)
            if icon_path:
                full_path = os.path.join(base_dir, icon_path)
                if os.path.exists(full_path):
                    try:
                        img = tk.PhotoImage(file=full_path)
                        lbl = tk.Label(cell, image=img, bg=self.skin["panel"])
                        lbl.image = img
                        lbl.pack(pady=(0, 4))
                    except Exception:
                        tk.Label(cell, text="?", fg=self.skin["text"], bg=self.skin["panel"], font=("Arial", 16)).pack(pady=(0, 4))
                else:
                    tk.Label(cell, text="?", fg=self.skin["text"], bg=self.skin["panel"], font=("Arial", 16)).pack(pady=(0, 4))
            else:
                tk.Label(cell, text="?", fg=self.skin["text"], bg=self.skin["panel"], font=("Arial", 16)).pack(pady=(0, 4))
            tk.Label(cell, text=u.name, fg=self.skin["text"], bg=self.skin["panel"], font=("Arial", 9)).pack()
            tk.Label(cell, text=str(u.count), fg=self.skin["gold"], bg=self.skin["panel"], font=("Arial", 11, "bold")).pack(pady=(2, 0))

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

    def _attack_map(self, map_id: str):
        levels = {k: v.level for k, v in self.state.research.items()}
        military = get_military_multiplier(levels)
        player_power = get_combat_power({u: max(1, self.state.units[u].count) for u in self.state.units}, levels)
        defense_power = 20 + sum(v * 3 for v in self.state.map_garrison.get(map_id, {}).values())
        if player_power > defense_power:
            loot = random.randint(10, 30)
            bonus = next(m for m in MAPS if m["id"] == map_id)["bonus"]
            self.state.resources[bonus].amount += loot
            self.state.ruf += 10
            report = f"Eroberung auf {map_id}: +{loot} {bonus}, Ruf +10"
            self.state.messages.append({"text": report, "type": "kampf"})
            self._log(report)
        else:
            loss = random.randint(5, 15)
            self.state.resources["nahrung"].amount = max(0, self.state.resources["nahrung"].amount - loss)
            report = f"Angriff auf {map_id} fehlgeschlagen. -{loss} Nahrung"
            self.state.messages.append({"text": report, "type": "kampf"})
            self._log(report)

    def _activate_map(self, map_id: str):
        if map_id not in self.state.active_maps:
            self._log("Karte nicht aktiv.")
            return
        if self.state.current_map == map_id:
            self._log("Bereits auf dieser Karte.")
            return
        if self.state.resources["geld"].amount < self.state.map_switch_cost:
            self._log("Nicht genug Geld für Kartenwechsel.")
            return
        self.state.resources["geld"].amount -= self.state.map_switch_cost
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
                self.state.resources["geld"].amount += 20
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
        levels = {k: v.level for k, v in self.state.research.items()}
        military = get_military_multiplier(levels, get_defense_bonus(self.state.buildings.get("turm", Building("", "")).level))
        player_power = sum(get_unit_stats(u, max(1, self.state.units[u].count), levels, self.state.buildings.get("turm", Building("", "")).level)["attack"] for u in self.state.units)
        bot_power = random.randint(20, 80) * bot.aggression + bot.ruf
        if player_power > bot_power:
            gain_ruf = max(5, int(15 * military))
            self.state.ruf += gain_ruf
            for res in ["holz", "stein", "geld"]:
                self.state.resources[res].amount += random.randint(5, 15)
            report = f"Sieg über {bot.name}! Ruf +{gain_ruf}, Ressourcen geplündert."
            self.state.messages.append({"text": report, "type": "kampf"})
            self._log(report)
        else:
            loss = max(0, random.randint(8, 25) - get_medic_redution(levels))
            self.state.resources["nahrung"].amount = max(0, self.state.resources["nahrung"].amount - loss)
            report = f"Niederlage gegen {bot.name}. -{loss} Nahrung"
            self.state.messages.append({"text": report, "type": "kampf"})
            self._log(report)

    def _render_battle_simulator(self):
        tk.Label(self.content, text="Kampfsimulator", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        tk.Label(self.content, text="Simuliere einen Kampf mit deinen aktuellen Einheiten.", fg="#C0C0C0", bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)
        frame = tk.Frame(self.content, bg=self.skin["panel"])
        frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(frame, text="Eigene Stärke:", fg=self.skin["text"], bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
        levels = {k: v.level for k, v in self.state.research.items()}
        player_power = get_combat_power({u: max(1, self.state.units[u].count) for u in self.state.units}, levels)
        tk.Label(frame, text=f"{int(player_power)}", fg="#DAA520", bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Zufallsangriff", command=self._simulate_random_battle, bg="#3e2723", fg=self.skin["gold"]).pack(side=tk.RIGHT, padx=5)

    def _simulate_random_battle(self):
        levels = {k: v.level for k, v in self.state.research.items()}
        military = get_military_multiplier(levels)
        player_power = get_combat_power({u: max(1, self.state.units[u].count) for u in self.state.units}, levels)
        enemy_power = random.randint(20, 120)
        if player_power >= enemy_power:
            self.state.ruf += 10
            self._log(f"Sieg im Simulator! Gegner Stärke {enemy_power}, deine Stärke {int(player_power)}")
        else:
            self._log(f"Niederlage im Simulator. Gegner Stärke {enemy_power}, deine Stärke {int(player_power)}")

    def _render_hall_of_fame(self):
        levels = {k: v.level for k, v in self.state.research.items()}
        total_units = sum(self.state.units[u].count for u in self.state.units)
        total_combat = int(get_combat_power({u: max(1, self.state.units[u].count) for u in self.state.units}, levels))
        tk.Label(self.content, text="Ruhmeshalle", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        tk.Label(self.content, text="Eure Punkte", fg="#C0C0C0", bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)
        tk.Label(self.content, text=f"Forschung: {self.state.score}", fg="#DAA520", bg=self.skin["bg"]).pack(anchor=tk.W, padx=20)
        tk.Label(self.content, text=f"Krieg: {self.state.ruf}", fg=self.skin["red"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=20)
        tk.Label(self.content, text=f"Truppen: {total_units}", fg=self.skin["text"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=20)
        tk.Label(self.content, text=f"Gesamt: {self.state.score + self.state.ruf + total_combat}", fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=20)

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
        tk.Label(self.content, text="Chat", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        tk.Label(self.content, text="Chat ist offline.", fg="#C0C0C0", bg=self.skin["bg"]).pack(anchor=tk.W, padx=10)

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
        r = self.state.research[key]
        cost = r.cost
        levels = {k: v.level for k, v in self.state.research.items()}
        if all(self.state.resources[k].amount >= v for k, v in cost.items()):
            for k, v in cost.items():
                self.state.resources[k].amount -= v
            r.level += 1
            self.state.score += 10
            self._log(f"{r.name} auf Stufe {r.level} erforscht.")
        else:
            self._log("Nicht genug Ressourcen für Forschung.")

    def _render_barracks(self):
        tk.Label(self.content, text="Kaserne", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 5))
        for key, u in self.state.units.items():
            frame = tk.Frame(self.content, bg=self.skin["panel"])
            frame.pack(fill=tk.X, padx=10, pady=2)
            tk.Label(frame, text=u.name, fg=self.skin["text"], bg=self.skin["panel"], width=15, anchor=tk.W).pack(side=tk.LEFT, padx=5)
            info = f"ATK {u.attack} / DEF {u.defense}"
            if "belagerung" in key or key == "golem":
                info += f" / Schaden {u.attack + u.defense}"
            tk.Label(frame, text=info, fg="#DAA520", bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
            tk.Label(frame, text=f"Anzahl: {u.count}", fg="#C0C0C0", bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
            tk.Button(frame, text="Ausbilden", command=lambda k=key: self._train_unit(k), bg="#3e2723", fg=self.skin["gold"]).pack(side=tk.RIGHT, padx=5)

    def _train_unit(self, key: str):
        u = self.state.units[key]
        levels = {k: v.level for k, v in self.state.research.items()}
        building_level = self.state.buildings.get("kaserne", Building("", "")).level
        time_min = get_training_time(key, levels, building_level)
        cost = u.cost
        if all(self.state.resources[k].amount >= v for k, v in cost.items()):
            for k, v in cost.items():
                self.state.resources[k].amount -= v
            u.count += 1
            self._log(f"{u.name} ausgebildet. Ausbildungszeit: {time_min:.1f} min")
        else:
            self._log("Nicht genug Ressourcen für Ausbildung.")

    def _save(self):
        self.state.save(self.save_path)
        self._log("Spiel gespeichert.")

    def _load(self):
        self.state.load(self.save_path)
        if hasattr(self, "content"):
            self._render_view()
            self._render()
        self._log("Spiel geladen.")

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
        for r, lbl in self.res_labels_top.items():
            res = self.state.resources[r]
            prod = self.state.buildings.get(self._resource_building_key(r), Building("", "")).level
            prod_text = f"+{prod}" if prod else "0"
            lbl.config(text=f"{RESOURCE_ICONS[r]} {int(res.amount)} ({prod_text})")
        self.lbl_day.config(text=f"Tag {self.state.day}")
        total_units = sum(self.state.units[u].count for u in self.state.units)
        self.lbl_forschung.config(text=f"Forschung: {self.state.score}")
        self.lbl_krieg.config(text=f"Krieg: {self.state.ruf}")
        self.lbl_gesamt.config(text=f"Gesamt: {self.state.score + self.state.ruf + total_units}")


def main():
    import sys
    import os
    lock_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game.lock")
    if os.path.exists(lock_path):
        try:
            with open(lock_path, "r") as f:
                pid = int(f.read().strip())
            os.kill(pid, 0)
            print("Spiel läuft bereits.")
            sys.exit(0)
        except Exception:
            pass
    with open(lock_path, "w") as f:
        f.write(str(os.getpid()))
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
