"""
Nebelseetal Remake — Central Bonus System
All research/building bonuses flow through these helpers so values stay consistent.
"""
from __future__ import annotations
from typing import Dict


# ---------- Base Stats ----------

UNIT_BASE: Dict[str, Dict[str, float]] = {
    "siedler":  {"attack": 2,  "defense": 2,  "hp": 200,  "speed": 1.0},
    "krieger":  {"attack": 12, "defense": 8,  "hp": 600,  "speed": 0.9},
    "bogenschütze": {"attack": 16, "defense": 6,  "hp": 480,  "speed": 0.8},
    "reiter":  {"attack": 20, "defense": 10, "hp": 800,  "speed": 1.2},
    "mönch":   {"attack": 6,  "defense": 5,  "hp": 400,  "speed": 0.7},
    "golem":   {"attack": 28, "defense": 18, "hp": 1400, "speed": 0.5},
    "spion":   {"attack": 4,  "defense": 3,  "hp": 300,  "speed": 1.4},
}

UNIT_TRAIN_BASE: Dict[str, float] = {
    "siedler": 1.0,
    "krieger": 2.0,
    "bogenschütze": 2.5,
    "reiter": 4.0,
    "mönch": 3.0,
    "golem": 6.0,
    "spion": 1.5,
}

BUILDING_BASE_COST: Dict[str, Dict[str, float]] = {
    "holzfäller": {"holz": 10, "stein": 5,  "nahrung": 1},
    "steinmetz": {"holz": 5,  "stein": 10, "nahrung": 1},
    "jäger":     {"holz": 25, "stein": 25, "nahrung": 1},
    "haus":      {"holz": 80, "stein": 50},
    "schmiede": {"holz": 40, "stein": 60, "eisen": 20},
    "bibliothek":{"holz": 60, "stein": 40, "kristall": 20},
    "markt":     {"holz": 50, "stein": 50, "geld": 20},
    "kaserne":   {"holz": 80, "stein": 80, "eisen": 40},
    "turm":      {"stein": 120, "eisen": 60},
    "portal":    {"kristall": 100, "geld": 100, "wissen": 50},
}

# Tier scaling: T1=1.0, T2=2.0, T3=3.0, T4=4.5, T5=6.0
TIER_SCALE: Dict[str, float] = {
    "siedler": 1.0,
    "krieger": 1.5,
    "bogenschütze": 2.0,
    "reiter": 3.0,
    "mönch": 2.5,
    "golem": 4.5,
    "spion": 1.2,
}


# ---------- Bonus Calculation ----------

def get_military_multiplier(research_levels: Dict[str, int], building_bonus: float = 0.0) -> float:
    """ATK/DEF/HP bonus from research + watchtower."""
    mil = research_levels.get("militär", 0)
    base = 1.0 + 0.08 * mil
    if building_bonus > 0:
        base *= (1.0 + building_bonus)
    return base


def get_production_multiplier(research_levels: Dict[str, int], resource: str) -> float:
    """Production bonus for a resource from research."""
    if resource == "nahrung":
        return 1.0 + 0.12 * research_levels.get("landwirtschaft", 0)
    if resource in ("stein", "eisen"):
        return 1.0 + 0.12 * research_levels.get("bergbau", 0)
    if resource == "holz":
        return 1.0 + 0.10 * research_levels.get("bergbau", 0)
    return 1.0


def get_building_cost_multiplier(research_levels: Dict[str, int]) -> float:
    """Cost reduction from Architektur."""
    arch = research_levels.get("architektur", 0)
    return max(0.5, 1.0 - 0.06 * arch)  # min 50% cost


def get_training_time_multiplier(research_levels: Dict[str, int], building_level: int = 0) -> float:
    """Training speed bonus."""
    train_res = research_levels.get("training", 0)
    base = 1.0 + 0.12 * train_res
    if building_level > 0:
        base *= (1.0 + 0.05 * building_level)
    return base


def get_trade_bonus(research_levels: Dict[str, int]) -> float:
    return 1.0 + 0.08 * research_levels.get("handel", 0)


def get_defense_bonus(tower_level: int = 0) -> float:
    return 0.5 * tower_level  # +50% per tower level


def get_medic_redution(research_levels: Dict[str, int]) -> int:
    return research_levels.get("medizin", 0) * 2


def get_unit_stats(unit_id: str, count: int, research_levels: Dict[str, int], tower_level: int = 0) -> Dict[str, float]:
    """Return scaled stats for a unit type including all bonuses."""
    base = UNIT_BASE.get(unit_id, {})
    tier = TIER_SCALE.get(unit_id, 1.0)
    mil = get_military_multiplier(research_levels, get_defense_bonus(tower_level))
    return {
        "attack": base.get("attack", 0) * tier * mil * count,
        "defense": base.get("defense", 0) * tier * mil * count,
        "hp": base.get("hp", 0) * tier * mil * count,
        "speed": base.get("speed", 1.0),
        "count": count,
    }


def get_combat_power(units: Dict[str, int], research_levels: Dict[str, int]) -> float:
    """Total combat power for scoreboard."""
    total = 0.0
    for uid, count in units.items():
        if count <= 0:
            continue
        base = UNIT_BASE.get(uid, {})
        tier = TIER_SCALE.get(uid, 1.0)
        mil = get_military_multiplier(research_levels)
        total += (base.get("attack", 0) + base.get("defense", 0) + base.get("hp", 0) * 0.01) * tier * mil * count
    return total


def get_building_cost(building_id: str, level: int, research_levels: Dict[str, int]) -> Dict[str, float]:
    """Scaled building cost."""
    base = BUILDING_BASE_COST.get(building_id, {})
    mult = get_building_cost_multiplier(research_levels)
    return {r: max(1, int(v * (level + 1) * mult)) for r, v in base.items()}


def get_training_time(unit_id: str, research_levels: Dict[str, int], building_level: int = 0) -> float:
    """Training time in minutes."""
    base = UNIT_TRAIN_BASE.get(unit_id, 2.0)
    mult = get_training_time_multiplier(research_levels, building_level)
    return max(0.5, base / mult)


def get_map_switch_cost(base_cost: int, switch_count: int) -> int:
    return base_cost + 50 * switch_count
