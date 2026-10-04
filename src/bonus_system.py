"""
Nebelseetal Remake — Central Bonus System
All research/building bonuses flow through these helpers so values stay consistent.
"""
from __future__ import annotations
from typing import Dict


# ---------- Base Stats (aus den Originaldaten) ----------
#
# Vorher standen hier 7 erfundene Einheiten (siedler, krieger, reiter, golem ...) mit
# attack/defense/hp. Einheiten, die nur in der Anzeigetabelle standen, rechneten deshalb mit 0.
# Jetzt kommt alles aus `data/units.json` ueber die Bruecke `einheiten.py` — eine Quelle.

import einheiten as _E

# Angriff / Abwehr / Leben / Geschwindigkeit aus den Originalwerten AT / PA / LE / GS.
# Karren und Belagerungswaffen haben im Handbuch keine AT/PA — sie kaempfen nicht; ihre
# Rolle steht in `_E.rolle()` und ihr Beitrag kommt aus SK bzw. Ladung.
UNIT_BASE: Dict[str, Dict[str, float]] = {
    name: {
        "attack": _E.angriff(name),
        "defense": _E.verteidigung(name),
        "hp": _E.leben(name),
        "speed": _E.geschwindigkeit(name),
    }
    for name in _E.namen()
}

# Kein Stufenfaktor im Handbuch: die Wirkung kommt dort aus Forschung, Waren und Wallstufe.
TIER_SCALE: Dict[str, float] = {name: 1.0 for name in _E.namen()}

# Das Handbuch nennt fuer die Einheiten Kosten, aber KEINE Ausbildungsdauer.
# Deshalb 0.0 = "nicht angegeben" statt eines erfundenen Werts. (Offene Entscheidung,
# siehe docs/PROJEKT_STAND.md.)
UNIT_TRAIN_BASE: Dict[str, float] = {name: 0.0 for name in _E.namen()}


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
    """Gesamtstaerke zum Vergleich — rollenbewusst.

    Kampfeinheiten und Kundschafter zaehlen mit Angriff + Abwehr (AT + PA).
    Belagerungswaffen zaehlen mit ihrer Schlagkraft (SK) — damit brechen sie Mauern (Seite 20).
    Karren kaempfen nicht; sie erscheinen hier nicht, ihre Tragekapazitaet steht in
    `einheiten.kapazitaet()`.
    """
    mil = get_military_multiplier(research_levels)
    total = 0.0
    for uid, count in units.items():
        if count <= 0:
            continue
        rolle = _E.rolle(uid)
        if rolle in ("kaempfer", "kundschafter"):
            total += (_E.angriff(uid) + _E.verteidigung(uid)) * mil * count
        elif rolle == "belagerung":
            total += _E.schlagkraft(uid) * mil * count
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
