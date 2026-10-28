"""
Nebelseetal Remake — Core Game Engine
Single-player, local, portable Windows desktop app.
Multi-map system, trade, combat, research, bots, stationing.
"""
from __future__ import annotations
import json
import math
import os
import random
import time
import tkinter as tk
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple

from bonus_system import (
    # Nur noch, was main.py wirklich benutzt. Die erfundenen Kampf- und Preisformeln
    # (`get_combat_power`, `get_unit_stats`, `get_building_cost`, `get_map_switch_cost`,
    # `UNIT_BASE`, `UNIT_TRAIN_BASE`, `BUILDING_BASE_COST`, `TIER_SCALE`) sind hier nicht mehr
    # im Spiel: Kaempfe rechnet src/kampf.py, Preise kommen aus data/*.json, Punkte aus src/punkte.py.
    get_military_multiplier, get_trade_bonus, get_defense_bonus,
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
import forschung  # W4c: Forschung braucht Zeit - die Stufe steigt erst nach Ablauf
import welt        # W4d: die Weltkarte des Limbus (20 Dimensionen, sechs belegte Welten)
import spielzeit   # Spieluhr: der Zeitfaktor (Vorgabe Daniel 05.10.2026, Spielbericht)
import spieloekonomie  # Oekonomie-Paket Schritt 9: Ortslager, Gruendungskosten, Verbrauch je Ort
# Feinere Kartenoptik (Kinder-Arbeit vom 05.10.2026, vom Koordinator nachgerechnet): beide Module
# liefern Zeichenplaene als DATEN und zeichnen sie ueber `zeichne` auf eine beliebige Leinwand.
# Sie ersetzen die duennen Einzelstriche der ersten Fassung — Siedlungskarte UND Weltkarte.
import karten_optik   # Siedlungskarte: der Renderer (`zeichne`) fuer beide Plan-Fassungen
import welt_optik     # Weltkarte: der Renderer (`zeichne`) fuer beide Plan-Fassungen
# Zweite astra-Auswertung (05.10.2026) — die FEINERE Fassung. Beide Module liefern nur Plaene
# (Daten), gezeichnet werden sie mit `karten_optik.zeichne` bzw. `welt_optik.zeichne`.
import karten_optik_fein   # Baukoerper 44x46, Ufer nur an echten Grenzen, Wege, Leiste, Pips
import welt_optik_fein     # zusammenhängende Landschaften, Ortssilhouetten, Panelmasse
# Vorgabe Daniel 05.10.2026: Einheiten brauchen ihre AUSRUESTUNG, nicht nur die Forschung.
# `ausruestung` liest den Warenbedarf aus data/units.json und rechnet Fehlmengen und Verbrauch.
import ausruestung
import forschungspfad  # Forschung: was jetzt geht, was blockiert ist und was es freischaltet


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
    # W5 (botkern): die Felder, mit denen `src/botkern.py` rechnet. Sie sind der EINE Ort, an dem
    # ein Bot Vorräte, Wagenpark und Handels-Temperament führt; `bot_als_dict`/`bot_aus_dict`
    # uebersetzen sie in die dict-Form des Kerns und wieder zurueck (keine zweite Wahrheit).
    temperament: float = 0.0
    vorraete: Dict[str, int] = field(default_factory=dict)
    lager: Dict[str, int] = field(default_factory=dict)
    naechster_angriff: float = 0.0
    letzter_angriff: Optional[float] = None
    angriffe: int = 0
    gebaut: int = 0
    geforscht: int = 0
    gehandelt: int = 0
    punkte: int = 0


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
    BotPlayer("Krank", "monster", aggression=0.9, trading=0.0),
]
# W5 (botkern): Der Bot-Zug. Der Entwurf nennt den Pruefrhythmus "alle 6 bis 24 Stunden"
# (VORSCHLAG, in botkern.py belegt vermerkt); `botkern.tick` wuerde bei jedem Sekundentakt eine
# Meldung erzeugen, deshalb wird der Bot-Zug stundenweise gefahren.
BOT_TAKT_SEKUNDEN = 3600.0
# W5: Grundlage des Handels-Schwellenpreises. Das Handbuch nennt keinen Warenpreis; die einzige
# BELEGTE Preistafel im Projekt ist der Einheitenpreis (`data/units.json`). Genommen wird der
# Kaempfer (1 Siedler + 250 Gold) -> Referenzpreis 250 x 1,2 = 300 (VORSCHLAG der Wahl).
BOT_BESCHAFFUNGSKOSTEN = 250.0
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
        self.messages: List[dict] = []
        self.settlements: List[Settlement] = []
        # Ökonomie-Paket, Schritt 9, Teil 5 (Entwurf Z. 777): der feste KARTENVORRAT für
        # Neugründungen (Startkarte + zehn Koloniekarten, data/gelaende.json). Der Vorrat ist
        # Spielzustand — eine vergebene Karte bleibt vergeben — und wird deshalb mitgespeichert.
        # Er wird beim ersten Zugriff angelegt (`kartenvorrat_anlegen`), damit ein ALTER Spielstand
        # ihn nachträglich bekommt, ohne dass sich etwas an seinen Siedlungen ändert.
        self.kartenvorrat: Dict[str, dict] = {}
        self.kartenvorrat_seed: str = ""
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

    def punktestand(self) -> dict:
        """Forschungs-, Kriegs- und Gesamtpunkte nach den Originalformeln (Handbuch S. 3/5/6).

        EINE Quelle: src/punkte.py. Vorher rechnete die Oberflaeche an mehreren Stellen eigene
        Summen — so entstand nachweislich eine falsche Gesamtzahl.
        Die Einheiten kommen aus `alle_einheiten()`: anwesende **und** unterwegs befindliche,
        jede genau einmal (Entwurf Z. 786).
        """
        staende = {k: v.level for k, v in self.research.items()}
        einheiten = self.alle_einheiten()
        wall = gebaeude_wirkung.wall_stufe(self.settlements)
        return {
            "staende": staende,
            "einheiten": einheiten,
            "wall_stufe": wall,
            "forschung": punkte.forschungspunkte(staende),
            "krieg": punkte.kriegspunkte(einheiten, wall),
            "gesamt": punkte.gesamtpunkte(staende, einheiten, wall),
        }

    def spielausgang(self) -> Tuple[str, str]:
        """('sieg'|'niederlage'|'weiter', Begruendung) aus src/punkte.py.

        Vorgabe Daniel 05.10.2026 (Option A): Sieg, sobald die Gesamtpunktzahl die Zielzahl
        erreicht (300, `punkte.VORSCHLAG_ZIEL_PUNKTE`); Niederlage, sobald keine Siedlung UND
        keine Einheit mehr da ist. Vor der ersten Siedlung laeuft nichts — sonst waere die
        Partie in der ersten Sekunde verloren.
        """
        if not self.hatte_siedlung:
            return ("weiter", "Noch keine Siedlung gegruendet — die Partie hat nicht begonnen.")
        stand = self.punktestand()
        return punkte.sieg_oder_niederlage({
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

    def ortsdeckung(self, siedlung: Settlement, kosten: dict) -> Dict[str, float]:
        """Was FEHLT, wenn auch der Reichsbestand mitzahlen darf. Leer = gedeckt.

        Geprüft wird gegen die zwei Quellen, aus denen `verbrauche_am_ort` wirklich zahlt: das
        LOKALE Lager des Ortes und den Reichsbestand (Übergang). So wird nie halb gebucht.
        """
        fehlt: Dict[str, float] = {}
        for r, v in (kosten or {}).items():
            if r == "siedler":
                haben = float(siedlung.bevoelkerung) + float(self.population)
            else:
                haben = float(siedlung.vorraete.get(r, 0.0))
                if r in self.resources:
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
                if rest > 0:
                    self.population = max(0.0, float(self.population) - rest)
                continue
            aus_ort = min(float(siedlung.vorraete.get(stoff, 0.0)), float(menge))
            siedlung.vorraete[stoff] = round(float(siedlung.vorraete.get(stoff, 0.0)) - aus_ort, 2)
            rest = float(menge) - aus_ort
            if rest > 0 and stoff in self.resources:
                self.resources[stoff].amount = round(float(self.resources[stoff].amount) - rest, 2)
        return True, ""

    def reichsdeckung(self, kosten: dict) -> Dict[str, float]:
        """Was FEHLT, wenn das GANZE Reich zahlt (alle Ortslager + Reichsbestand). Leer = gedeckt.

        Für **globale** Aktionen, die zu keiner einzelnen Siedlung gehören (z. B. der Kartenwechsel
        auf der Weltkarte, Handbuch S. 19).
        """
        fehlt: Dict[str, float] = {}
        for r, v in (kosten or {}).items():
            if r == "siedler":
                haben = float(self.population) + sum(float(s.bevoelkerung) for s in self.settlements)
            else:
                haben = float(self.resources[r].amount) if r in self.resources else 0.0
                haben += sum(float(s.vorraete.get(r, 0.0)) for s in self.settlements)
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
            if stoff in self.resources:
                nimm = min(rest, float(self.resources[stoff].amount))
                self.resources[stoff].amount = round(float(self.resources[stoff].amount) - nimm, 2)
                rest -= nimm
            for s in sorted(self.settlements, key=lambda x: x.id):
                if rest <= 1e-9:
                    break
                nimm = min(rest, float(s.vorraete.get(stoff, 0.0)))
                s.vorraete[stoff] = round(float(s.vorraete.get(stoff, 0.0)) - nimm, 2)
                rest -= nimm
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
        if stoff in self.resources:
            self.resources[stoff].amount = max(
                0.0, round(float(self.resources[stoff].amount) - menge, 2))
        verfuegbar = sum(float(s.vorraete.get(stoff, 0.0)) for s in self.settlements)
        if verfuegbar <= 0:
            return menge
        anteil = min(1.0, menge / verfuegbar)
        for s in self.settlements:
            vorher = float(s.vorraete.get(stoff, 0.0))
            s.vorraete[stoff] = round(vorher - vorher * anteil, 2)
        return menge

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
        ladung = int(auftraege.ladung_der_mission(karren))
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
            verfuegbar = int(self.units[name].count) if name in self.units else 0
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
                                                          {stoff: menge}, jetzt)
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
            self.messages.append({"type": "auftrag", "text":
                                  f"Transport angekommen in {m.get('nach')}: "
                                  + ", ".join(f"{int(v)} {k.capitalize()}"
                                              for k, v in sorted(fracht_vorher.items()))
                                  + " im Ortslager gutgeschrieben."})
        if m.get("heimgekehrt_lokal") and not vorher_heim:
            self.messages.append({"type": "auftrag", "text":
                                  f"Transport heimgekehrt nach {m.get('von')}: "
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
        ladung = int(auftraege.ladung_der_mission(karawane))
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
            verfuegbar = int(self.units[name].count) if name in self.units else 0
            if verfuegbar < rest:
                return False, (f"Nicht genug {name}: der Ort hat {im_ort}, im Reichsheer stehen "
                               f"{verfuegbar} — gebraucht werden {anzahl}.")
            aus_reich_karren[name] = rest
        gold_im_ort = float((getattr(quelle, "vorraete", None) or {}).get("gold", 0.0))
        aus_reich_gold = max(0.0, gold_gesamt - gold_im_ort)
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
                "vorraete", jetzt)
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
            self.messages.append({"text": text, "type": "handel"})
            self._log(text)
        abgerechnet_jetzt = bool(m.get("abgerechnet")) and not abgerechnet_vorher
        if abgerechnet_jetzt:
            if m.get("angenommen"):
                text = ("Handel abgeschlossen: %d %s sind im Ortslager von %s angekommen."
                        % (menge, stoff, m.get("von")))
            else:
                text = ("Handel abgelehnt: %s schickt die Karawane MIT den %d %s zurück — "
                        "Gold wurde nicht übertragen." % (m.get("nach"), menge, stoff))
            self.messages.append({"text": text, "type": "handel"})
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
                         id=siedlung_kennung("spieler", self.current_map, x, y))
        neu.vorraete = {r: float(v) for r, v in absicht["paket"].items()}
        neu.bevoelkerung = float(siedler)
        self.settlements.append(neu)
        self.kartenvorrat[karte_id]["besitzer"] = "spieler"
        self.hatte_siedlung = True
        size = next(m for m in MAPS if m["id"] == self.current_map)["size"]
        tile = self.get_tile(x, y, size)
        if tile is not None:
            tile.npc_faction = "spieler"
            tile.sector_name = name
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
                                        float(entfernung), float(self.spielsekunden), fracht)
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
            vorher = {"ressourcen": {k: v.amount for k, v in self.resources.items()},
                      "einheiten": {k: u.count for k, u in self.units.items()}}
            neu = auftraege.spieldaten_anwenden(vorher, eintrag)
            for stoff, menge in (neu.get("ressourcen") or {}).items():
                if stoff in self.resources:
                    self.resources[stoff].amount = float(menge)
            for name, anzahl in (neu.get("einheiten") or {}).items():
                if name in self.units:
                    self.units[name].count = max(0, int(anzahl))
            # Echter Fund beim Ökonomie-Paket, Schritt 9 (Teil 2, 05.10.2026): ein STATIONIERENDER
            # Auftrag verlor seine Truppe ZWEIMAL. `auftrag_starten` nimmt die Einheiten schon beim
            # Start aus dem Bestand (Z. 836, „sie sind ab jetzt unterwegs"); der Auftragskern zieht
            # für die Art „stationieren" bei der Ankunft noch einmal ab (sein Vertrag, in
            # tests/test_auftraege.py belegt: Eingabe „Kämpfer 2" -> 0). Hier wird der Kern-Abzug
            # deshalb aufgehoben: die Truppe bleibt am Ziel, sie geht genau EINMAL ab.
            if eintrag.get("art") == "stationieren":
                for name in (eintrag.get("einheiten") or {}):
                    if name in self.units and name in vorher["einheiten"]:
                        self.units[name].count = max(0, int(vorher["einheiten"][name]))
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
            for name, anzahl in (eintrag.get("einheiten") or {}).items():
                if name in self.units:
                    self.units[name].count = int(self.units[name].count) + int(anzahl)
                    ergebnis["heimgekehrt"][name] = ergebnis["heimgekehrt"].get(name, 0) + int(anzahl)
        self.auftraege[:] = [e for e in self.auftraege
                             if not (e.get("status") == "abgeschlossen" and e.get("heimgekehrt"))]
        return ergebnis

    def kampf_am_ziel(self, eintrag: dict) -> dict:
        """Den echten Kampf am Ziel austragen (Handbuch S. 21-23) - W7, Schritt 7 abgeschlossen.

        `auftraege.py` rechnet nur Reisezeit und Beute; es erwartet `vorrunde` und `beute` als
        **Eingabe**. Hier wird deshalb mit `kampf.fuehre_schlacht` gekaempft: die gefallenen
        Einheiten gehen von den Auftrags-Einheiten ab (Heimkehrer sind also die Ueberlebenden),
        und die Beute des Gefechts wird in `eintrag['beute']` uebernommen. Gebucht wird sie
        gleich danach von `auftraege.spieldaten_anwenden` - also GENAU EINMAL.
        """
        ziel = eintrag.get("ziel") or {}
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
            kaempfer, dict(ziel.get("verteidiger") or {}),
            int(ziel.get("wall_stufe") or 0), float(ziel.get("wall_zustand_prozent") or 100.0),
            angreifer_karren=geraet or None,
            verteidiger_karren=dict(ziel.get("verteidiger_karren") or {}) or None,
            vorraete=dict(ziel.get("vorraete") or {}), rng=random.Random())

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
        eintrag["beute"] = dict(ergebnis.get("beute") or {})
        eintrag["vorrunde"] = {"bestanden": ergebnis.get("ausgang") != "unentschieden",
                               "grund": ergebnis.get("bericht", "")}

        bericht = kampfbericht.bericht(ergebnis)
        self.messages.append({"text": f"Am Ziel {eintrag.get('nach')} — " + bericht["titel"] +
                                      "\n" + "\n".join(bericht["zeilen"]), "type": "kampf"})
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
                "gehandelt": int(bot.gehandelt)}

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

    def bot_vorrat_anlegen(self, bot: BotPlayer) -> None:
        """Startvorräte und Wagenpark eines Bots anlegen.

        Die Spannen sind VORSCHLAG (`botkern.VORSCHLAG_START_VORRAETE`; die Vorlage nennt kein
        Bot-Inventar). Zusaetzlich bekommt der Bot die BELEGTEN Startwerte des Spielers
        (Handbuch S. 7: 10 Siedler, 100 Holz, 100 Steine) — ohne sie koennte er keine einzige
        Einheit bezahlen, weil die belegten Preise Siedler nennen.
        """
        if not bot.vorraete:
            rng = random.Random(f"nebel-bot-vorrat-{bot.name}")
            bot.vorraete = {stoff: rng.randint(lo, hi)
                            for stoff, (lo, hi) in botkern.VORSCHLAG_START_VORRAETE.items()}
        for stoff, menge in (("siedler", 10), ("holz", 100), ("stein", 100)):
            if stoff not in bot.vorraete:
                bot.vorraete[stoff] = menge
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
        for name in sorted(einheiten.namen(), key=lambda n: (einheiten.rolle(n) != "kaempfer", n)):
            if einheiten.rolle(name) not in ("kaempfer", "kundschafter"):
                continue
            rohkosten = einheiten.alle()[name].get("kosten") or {}
            kosten = {str(k): int(v) for k, v in rohkosten.items()}
            if not kosten or not all(bot.vorraete.get(k, 0) >= v for k, v in kosten.items()):
                continue
            for stoff, menge in kosten.items():
                bot.vorraete[stoff] = bot.vorraete.get(stoff, 0) - menge
            bot.army[name] = bot.army.get(name, 0) + 1
            return name
        return None

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
        letzter = float(getattr(self, "_letzter_bot_takt", 0.0) or 0.0)
        if jetzt - letzter < BOT_TAKT_SEKUNDEN:
            return ergebnis
        self._letzter_bot_takt = jetzt
        ergebnis["bots"] = len(self.bots)

        rng = random.Random()
        welt = {"vorraete": {k: int(v.amount) for k, v in self.resources.items()},
                "referenzpreis": botkern.referenzpreis_aus_beschaffung(BOT_BESCHAFFUNGSKOSTEN)}
        daten = [self.bot_als_dict(b) for b in self.bots]
        stand = botkern.bots_tick(daten, welt, jetzt, rng)
        ergebnis["aktionen"] = dict(stand.get("aktionen") or {})

        for start, zug in zip(daten, stand.get("ergebnisse") or []):
            bot = next((b for b in self.bots if b.name == str(start.get("name"))), None)
            if bot is None:
                continue
            if zug.get("aktion") == "angreifen":
                beute = dict((zug.get("wirkung") or {}).get("beute") or {})
                if beute and getattr(self, "noob_protection", False):
                    # Der Götterschutz (Handbuch S. 6: die ersten sieben Tage bzw. bis zum ersten
                    # Kriegspunkt) schuetzt die Startwerte. Vorher zog der erste Bot SOFORT und
                    # pluenderte 50 % — von 100 Holz/100 Stein blieben 30/30, bevor der Spieler
                    # etwas bauen konnte.
                    self.messages.append({
                        "text": f"Götterschutz aktiv: {zug.get('meldung')} Die Beute bleibt uns.",
                        "type": "bot"})
                else:
                    for stoff, menge in beute.items():
                        # Teil 3: die Beute trifft Reichsbestand UND Ortslager anteilig - sonst
                        # laufen die Buecher auseinander (Reich = Uebergangsrest + Ortslager).
                        self.reich_abzug(stoff, float(menge))
                    if beute:
                        self.messages.append({"text": zug.get("meldung"), "type": "bot"})
                ergebnis["angriffe"].append(zug.get("meldung"))
            # Erst den Zug des Kerns uebernehmen (Beute, Zaehler, naechstes Fenster), DANN aus
            # der eigenen Kasse aufstellen - sonst waere die Beute wieder weg.
            self.bot_aus_dict(bot, botkern.wirkung_anwenden(start, zug))
            self.bot_armee_aufstellen(bot)

        for zeile in stand.get("nachrichten") or []:
            self._log(str(zeile))
        return ergebnis

    def tick(self, dt_seconds: float):
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
        _vorher_orte = {}
        _schluessel33 = {}
        for _nr33, _s33 in enumerate(self.settlements):
            # Ein Ort OHNE Kennung (kommt in Prüfungen und Hilfsbauten vor) bekommt hier einen
            # Arbeitsplatz-Schlüssel. Wichtig: NICHT nach `id` filtern — sonst fiele so ein Ort
            # stillschweigend aus dem Takt (gefunden von den Wachen P27/P28 am 06.10.2026).
            _k33 = _s33.id or "__ort_ohne_kennung_%d" % _nr33
            _vorher_orte[_k33] = asdict(_s33)
            _schluessel33[_k33] = _s33
        _neu_orte, _keine_missionen, _wissen, _zeit, _ereigniszeiten = spieloekonomie.tick_bis(
            _vorher_orte, [], _wissen, _ab, _bis)
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
                if abs(zuwachs) > 1e-12 and res in self.resources:
                    self.resources[res].amount = round(float(self.resources[res].amount) + zuwachs, 2)
            zuwachs_leute = float(_neu.get("bevoelkerung", 0.0)) - _vorher_leute
            if abs(zuwachs_leute) > 1e-12:
                self.population = float(self.population) + zuwachs_leute
        # Gestiegene Forschungsstufen aus dem Kern in den Spielstand uebernehmen (Teil 6 Rest).
        self._forschung_abschluss_buchen(_wissen)
        # Die Uhr steht genau auf dem Ende des Takts (`tick_bis` liefert die erreichte Spielzeit).
        self.spielsekunden = _zeit
        # W5: Die Bots handeln nach `botkern` (Angriffstakt 6-24 h, Handelsschwelle, Wirtschaft).
        # Vorher stand hier eine erfundene Schaedigung: 5 % x Aggression, fester Nahrungsabzug.
        self.bots_fortschreiben(self.spielsekunden)
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
        if self._day_accum >= 86400:
            self._day_accum -= 86400
            self.day += 1
        if self.noob_protection:
            # Götterschutz (Handbuch S. 6, Z. 215-217; KORREKTUR 05.10.2026): neue Spieler sind die
            # ersten SIEBEN Tage geschützt, der Schutz endet früher mit dem ERSTEN Kriegspunkt.
            # Vorher stand hier ein fester Tag 3 — belegter Widerspruch gegen das Handbuch
            # (docs/audits/handbuch_abgleich_2026-10-05.txt, Punkt 1). `self.day` startet bei 1,
            # also sind „die ersten sieben Tage“ day 1..7 und der Schutz endet ab day 8.
            krieg = punkte.kriegspunkte({k: int(v.count) for k, v in self.units.items()},
                                        gebaeude_wirkung.wall_stufe(self.settlements))
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
            # Ökonomie-Paket, Teil 5: der Kartenvorrat ist Spielzustand (eine vergebene Karte
            # bleibt vergeben) — ohne ihn könnte ein geladener Stand Karten doppelt vergeben.
            "kartenvorrat": self.kartenvorrat,
            "kartenvorrat_seed": self.kartenvorrat_seed,
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
            "_day_accum": getattr(self, "_day_accum", 0.0),
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
        self.messages = data.get("messages", [])
        self.settlements = [Settlement(**s) for s in data.get("settlements", [])]
        # Ökonomie-Paket Schritt 9: Altspielstände kennen die Ort-Kennung nicht. Sie bekommen sie
        # hier EINMALIG deterministisch aus Besitzer und Weltfeld — nicht aus dem Namen, damit ein
        # späteres Umbenennen die Kennung nie ändert (Entwurf Z. 774).
        for s in self.settlements:
            if not s.id:
                s.id = siedlung_kennung(s.besitzer, s.map_id, s.x, s.y)
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
        if not self.kartenvorrat:
            self.kartenvorrat_anlegen()
        self.hatte_siedlung = bool(data.get("hatte_siedlung", bool(self.settlements)))
        self.spielende = data.get("spielende")
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
            self.bots = [BotPlayer(**b) for b in saved_bots]
        # Teil 8b (Entwurf Z. 789: "_day_accum zusaetzlich sichern statt beim Laden auf 0 setzen"):
        # der Tagesrest kommt jetzt aus dem Spielstand. Ein Stand, der das Feld nicht kennt (alles
        # vor Teil 8b), beginnt unveraendert bei 0 — kein Absturz, keine erfundene Zahl.
        self._day_accum = float(data.get("_day_accum") or 0.0)
        # Der Bot-Zug darf nach dem Laden nicht sofort losgehen (sonst pluendern die Bots
        # genau in der Sekunde, in der ein alter Spielstand geoeffnet wird).
        self._letzter_bot_takt = float(self.spielsekunden)
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
        # Schritt 9, Teil 3b: diese Leiste zeigt den GESAMTBESTAND (Reich), nicht das Lager einer
        # Siedlung — seit Teil 3a fuehren die Ortslager. Ohne das Wort "Reich" liest der Spieler
        # die Zahl als "mein Lager" (KONTEXT_PAKET, Abschnitt 2, Teil 3b).
        tk.Label(top, text="Reich:", fg=self.skin["gold"], bg=self.skin["topbar"],
                 font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=(4, 0))
        self.res_labels_top = {}
        ertrag_jetzt = self.state.stundenertrag()
        for r in RESOURCES:
            icon = RESOURCE_ICONS[r]
            amount = int(self.state.resources[r].amount)
            rate = ertrag_jetzt.get(r, 0.0)
            prod_text = f"+{rate:g}/h" if rate else "0"
            # Ein Kernrohstoff ohne Erzeuger wird als Warnung gezeigt: „(0)" sieht sonst aus
            # wie ein Anzeigefehler — genau der Eindruck aus Daniels Spielbericht vom 05.10.2026.
            ohne_quelle = rate <= 0 and r in ("holz", "stein", "nahrung") and bool(self.state.settlements)
            lbl = tk.Label(top, text=f"{icon} {int(amount)} ({'⚠' if ohne_quelle else prod_text})",
                           fg=("#FDBA74" if ohne_quelle else self.skin["text"]),
                           bg=self.skin["topbar"], font=("Arial", 9))
            lbl.pack(side=tk.LEFT, padx=6)
            self.res_labels_top[r] = lbl
        for txt, cmd in [("Speichern", self._save), ("Laden", self._load), ("Skin", self._cycle_skin), ("Beenden", self.root.quit)]:
            tk.Button(top, text=txt, command=cmd, bg=self.skin["button"], fg=self.skin["gold"], relief=tk.FLAT, padx=8, pady=2).pack(side=tk.RIGHT, padx=4)
        self.lbl_day = tk.Label(top, text=f"Tag {self.state.day}", fg=self.skin["gold"], bg=self.skin["topbar"])
        self.lbl_day.pack(side=tk.RIGHT, padx=10)
        # Zeitfaktor sichtbar machen: sonst fragt man sich, warum nichts wächst.
        self.lbl_tempo = tk.Label(top, text=f"Tempo {spielzeit.text()}", fg=self.skin["text"],
                                  bg=self.skin["topbar"], font=("Arial", 9))
        self.lbl_tempo.pack(side=tk.RIGHT, padx=10)

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
        # Sieg/Niederlage (Vorgabe Daniel 05.10.2026, Option A): das Ziel und der Stand stehen
        # sichtbar in der Seitenleiste, damit der Spieler weiss, worauf er hinarbeitet.
        self.lbl_ziel = tk.Label(right, text=f"Ziel: 0 / {punkte.VORSCHLAG_ZIEL_PUNKTE} Punkte",
                                 fg=self.skin["text"], bg=self.skin["sidebar"], wraplength=200,
                                 justify=tk.LEFT)
        self.lbl_ziel.pack(anchor=tk.W, padx=5, pady=(0, 10))

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
        # Eine Pruefung darf eine App ohne aufgebaute Oberflaeche benutzen (z. B.
        # tests/test_gebaeude_wirkung.py baut nur den Zustand und ruft Aktionen direkt).
        # Dann gibt es nichts zu zeichnen — die Neuzeichnung ist trotzdem kein Fehler.
        if getattr(self, "content", None) is None:
            return
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
        tk.Label(self.content, text="Dorfzentrum", font=("Blackletter", 20, "bold"), fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(10, 2))
        _grenze = gebaeude_wirkung.bevoelkerungsgrenze(self.state.settlements)

        # ---- Aufgabenkarte: der EINE naechste Schritt (astra-Bildgutachten 05.10.2026) ----
        # Vorher stand hier "Eine Übersicht aller Gebäude" — die Startansicht sagte dem Spieler
        # nicht, was zu tun ist, und der Knopf "Karte öffnen" war zwischen Verwaltung versteckt.
        _schritt = self.naechster_schritt()
        _karte = tk.Frame(self.content, bg="#263B47", highlightbackground="#38BDF8", highlightthickness=1)
        _karte.pack(fill=tk.X, padx=10, pady=(6, 10))
        tk.Label(_karte, text="Dein nächster Schritt", fg="#7FD1FF", bg="#263B47",
                 font=("TkDefaultFont", 12, "bold")).pack(anchor=tk.W, padx=10, pady=(8, 0))
        tk.Label(_karte, text=_schritt["text"], fg="#F3F4F6", bg="#263B47",
                 wraplength=760, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=(2, 6))
        tk.Button(_karte, text=_schritt["knopf"], command=_schritt["aktion"], bg="#2563EB",
                  fg="white", activebackground="#1D4ED8", activeforeground="white",
                  font=("TkDefaultFont", 11, "bold")).pack(anchor=tk.W, padx=10, pady=(0, 10))

        # ---- Kennzahlen in Klartext (vorher "Bevölkerung: 60 / 15" ohne Erklärung) ----
        _bewohnt = int(self.state.population)
        _ueber = _bewohnt > _grenze
        tk.Label(self.content,
                 text=f"Siedler (Reich): {_bewohnt} · Wohnraum: {_grenze}"
                      + ("  ⚠ überbelegt — es wächst kein Siedler nach, bis ein Haus steht."
                         if _ueber else ""),
                 fg=("#FDBA74" if _ueber else "#DAA520"),
                 bg=self.skin["bg"], wraplength=780, justify=tk.LEFT).pack(anchor=tk.W, padx=10)
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
        tk.Label(wirk, text=f"Siedlergrenze {_grenze} · Zuwachs "
                            f"{gebaeude_wirkung.siedler_zuwachs_pro_stunde(self.state.settlements):g} Siedler/Stunde "
                            f"(1 je Siedlung, Handbuch S. 11)",
                 fg=self.skin["text"], bg=self.skin["panel"]).pack(anchor=tk.W, padx=5)
        # astra-Nachprüfung: „Zuwachs 1 Siedler/Stunde" widersprach der Überbelegungs-Warnung.
        # Angezeigt wird jetzt, was WIRKLICH passiert, und was möglich wäre.
        _moeglich = gebaeude_wirkung.siedler_zuwachs_pro_stunde(self.state.settlements)
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

        s = st.settlements[-1]
        gebaut = len(getattr(s, "bauten", {}) or {})
        if gebaut == 0:
            return {"text": f"Deine Siedlung „{s.name}“ hat noch kein Gebäude. Öffne ihre Karte "
                            "und baue einen Holzfäller auf ein Waldfeld — er liefert Holz pro "
                            "Stunde. (Grün/Steppe sind für Farmen, Berge für Minen.)",
                    "knopf": f"„{s.name}“ öffnen — Gebäude bauen",
                    "aktion": (lambda ss=s: self._oeffne_siedlungskarte(ss))}

        erlaubt, _ = gebaeude_wirkung.forschung_erlaubt(st.settlements)
        # astra-Nachprüfung 05.10.2026: die Aufgabenkarte muss den SICHTBAREN Engpass nennen.
        # Überbelegung blockiert das Siedlerwachstum — das ist wichtiger als alles andere.
        if int(st.population) >= gebaeude_wirkung.bevoelkerungsgrenze(st.settlements):
            return {"text": f"Deine Siedlung ist überbelegt ({int(st.population)} Siedler, "
                            f"{gebaeude_wirkung.bevoelkerungsgrenze(st.settlements)} Wohnraum). "
                            "Baue ein Haus auf ein freies Feld — jedes Haus schafft 5 Wohnraum, "
                            "erst dann wachsen wieder Siedler nach.",
                    "knopf": f"„{s.name}“ öffnen — Haus bauen",
                    "aktion": (lambda ss=s: self._oeffne_siedlungskarte(ss))}
        # Daniels Spielbericht 05.10.2026: „so kann es passieren, dass man kein holz mehr bekommt,
        # weil man keinen holzfäller gebaut hatte". Die Karte nennt deshalb jetzt den fehlenden
        # Erzeuger samt Feld und Preis, BEVOR sie zum Forschen schickt.
        ertrag = st.stundenertrag()
        for stoff, geb_key, felder_text in (
                ("holz", "holzfaeller", "auf Wald 4 Holz/h, auf Steppe 2"),
                ("stein", "steinmetz", "auf Berg 4 Stein/h, auf Hügel 2"),
                ("nahrung", "farm", "auf Grasland 4 Nahrung/h, auf Steppe 2")):
            if float(ertrag.get(stoff, 0.0)) > 0:
                continue
            eintrag = gelaende.alle_gebaeude().get(geb_key) or {}
            preis = kosten_text(baukosten(geb_key) or {})
            return {"text": f"Ohne {stoff.capitalize()}-Quelle geht es nicht weiter: es ist kein "
                            f"{stoff.capitalize()} da und es wächst keines nach. Baue einen "
                            f"{eintrag.get('name', geb_key)} — {felder_text}"
                            + (f" (Kosten: {preis})." if preis else "."),
                    "knopf": f"„{s.name}“ öffnen — {eintrag.get('name', geb_key)} bauen",
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
        karte = spieloekonomie.startkarte(self.state.kartenvorrat_seed, "spieler")
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
                              id=siedlung_kennung("spieler", self.state.current_map, x, y))
            sett.vorraete = dict(start)
            sett.bevoelkerung = bevoelkerung_start
            self.state.settlements.append(sett)
            # Die Startwerte werden EINMAL übernommen (verschoben, nicht kopiert) — sonst stünden
            # sie doppelt: einmal im Ortslager und einmal im Reichsbestand (Entwurf Z. 775).
            for r in list(start):
                self.state.resources[r].amount = 0.0
            self.state.population = 0.0
            self.state.hatte_siedlung = True
            tile.npc_faction = "spieler"
            tile.sector_name = sett.name
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
        _zeile("Ladeplätze: " + (", ".join(f"{k}x {n} ({einheiten.ladung(n)} Plätze)"
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
        _zeile("Ladeplätze: " + (", ".join("%s x%d (%d Plätze)" % (n, a, einheiten.ladung(n) * a)
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

    def _oeffne_siedlungskarte(self, siedlung):
        self.karten_siedlung = siedlung
        # Teil 6: wer eine Siedlungskarte öffnet, meint DIESEN Ort — Lager, Kaserne und Forschung
        # beziehen sich von jetzt an darauf (eine Quelle: `state.aktive_siedlung()`).
        if getattr(siedlung, "id", ""):
            self.state.aktive_siedlung_id = siedlung.id
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
        # Rohstoff- UND Siedler-Kosten gegen dieselben zwei Quellen prüfen, aus denen
        # `verbrauche_am_ort` gleich zahlt (Ortslager zuerst, dann der Reichsbestand). Vorher las
        # diese Vorprüfung nur den Reichsbestand - seit Teil 3 liegt der Startbestand aber im
        # ORT, und der Bau wurde mit "es fehlt holz" abgelehnt, obwohl die Siedlung es hatte
        # (gefunden vom Sammellauf: test_startspiel, test_durchspiel, test_gui_fehler).
        fehlt = self.state.ortsdeckung(siedlung, kosten)
        if fehlt:
            self._log(f"Nicht genug Rohstoffe für {name}: es fehlt "
                      f"{', '.join(sorted(fehlt))}.")
            return
        ok, meldung = bauen_auf_karte(siedlung, gebaeude_key, feld)
        if not ok:
            self._log(f"Bau nicht möglich: {meldung}")
            return
        # Oekonomie-Paket, Schritt 9, Teil 3: bezahlt wird aus dem LAGER DIESER Siedlung (Siedler
        # aus ihrer Bevoelkerung). Die Vorpruefung oben und die Buchung hier benutzen dieselben
        # zwei Quellen (Ortslager + Reichsbestand als Uebergang) - deshalb kann die Zahlung nicht
        # mehr halb gelingen.
        ok_zahlung, meldung_zahlung = self.state.verbrauche_am_ort(siedlung, kosten)
        if not ok_zahlung:
            self._log(f"Nicht genug im Lager von {siedlung.name} für {name}: {meldung_zahlung}")
            return
        self._log(f"{name} gebaut — {meldung}")
        # astra-Nachprüfung 05.10.2026: „Nach dem Bau bleibt dasselbe Feld ausgewählt und das
        # Panel wechselt zur Gebäudeansicht." Vorher löschte das Spiel hier die Auswahl — der
        # Spieler sah nach dem Bauen kein Ergebnis, nur die Statuszeile.
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
        # Handbuch S. 12 (Z. 423-424): Während eines Forschungsauftrags darf die Bibliothek NICHT
        # ausgebaut werden (KORREKTUR 05.10.2026). Die Bibliothek ist die eine Forschungsstätte,
        # also gilt die Sperre, solange irgendein Forschungsauftrag läuft.
        _forschend = next((s for s in self.state.settlements
                           if getattr(s, "forschungsauftrag", None)), None)
        if gebaut == "bibliothek" and _forschend is not None:
            laufend = (_forschend.forschungsauftrag or {}).get("gebiet", "")
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
        kosten = baukosten(gebaut, stufe + 1)
        # Dieselbe Deckungsfrage wie beim Bauen: Ortslager zuerst, dann der Reichsbestand.
        fehlt = self.state.ortsdeckung(siedlung, kosten)
        if fehlt:
            self._log(f"Nicht genug Rohstoffe für den Ausbau von {name}: es fehlt "
                      f"{', '.join(sorted(fehlt))}.")
            return
        # Oekonomie-Paket, Schritt 9, Teil 3: der Ausbau zahlt aus dem Lager DIESER Siedlung.
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
        `docs/audits/ux_astra_karten_feinheit_2026-10-05.txt`, Kinder-Arbeit, vom Koordinator
        nachgerechnet): Baukörper 44 × 46 px je Gebäudefamilie mit Dach, Sockel, Tür und
        Stufenpips (4 × 4 px), Gelände mit größeren Strukturformen, Uferband nur an echten
        Land-Wasser-Grenzen, Wege 8 px mit 4 px Innenlinie, goldener Auswahlrahmen mit vier
        Eckwinkeln und die Koordinaten in einer 18 px breiten äußeren Rasterleiste.

        Gezeichnet wird in vier Durchgängen: (1) Gelände, Koordinaten · (2) Wege · (3) Gebäude ·
        (4) Auswahlrahmen zuletzt. So liegen die Wege unter den Baukörpern und die Auswahl
        sichtbar über allem.

        Die Beschriftung der Leiste sind die Buchstaben der Siedlungskarte (A–H) — dieselben, die
        das Detailpanel und der Spielstand nennen (`_spaltenname`). Ohne sie zeigte die Leiste
        Ziffern und das Panel daneben „D3": zwei Wahrheiten für dieselbe Koordinate.
        """
        zelle = 64
        spalten = int(karte.get("spalten") or 8)
        zeilen = int(karte.get("zeilen") or 7)
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

        # ---- Durchgang 1: das Gelände (Fläche, Struktur, Uferband, Innenkanten) -------------
        for i, art in enumerate(raster):
            x0, y0 = _feld_ecke(i)
            tag = f"feld:{i}"
            karten_optik.zeichne(
                canvas,
                karten_optik_fein.gelaende_plan_fein(art, x0, y0, zelle, _nachbararten(i)),
                tags=(tag,))
            canvas.tag_bind(tag, "<Button-1>", lambda _e, idx=i: self._karten_feld_waehlen(idx))

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
            karten_optik.zeichne(
                canvas,
                karten_optik_fein.gebaeude_baukasten_plan(
                    gebaut, x0, y0, zelle, stufe=stufe,
                    max_stufe=gebaeude_wirkung.max_stufe(gebaut)),
                tags=(f"feld:{i}",))

        # ---- Durchgang 4: der Auswahlrahmen ZULETZT (liegt über allem) ----------------------
        if gewaehlt is not None and 0 <= int(gewaehlt) < len(raster):
            x0, y0 = _feld_ecke(int(gewaehlt))
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
        feld = getattr(self, "karten_feld", None)
        if feld is None:
            tk.Label(info, text="Ein Feld auf der Karte anklicken, um dort zu bauen.",
                     fg=self.skin["text"], bg=self.skin["panel"]).pack(anchor=tk.W, padx=6, pady=6)
            return

        art = karte["raster"][feld]
        gebaut = siedlung.bauten.get(str(feld))
        _spalten = int(karte.get("spalten") or 8)
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

        # astra-Bildgutachten: der Knopfteppich verschwieg die entscheidende Frage „Was bringt
        # mir das hier?". Jetzt steht der Ertrag auf DIESEM Feld im Knopf, und was noch fehlt,
        # wird benannt statt still abgelehnt.
        tk.Label(info, text=f"Hier kannst du {len(passend)} Gebäude bauen — der Ertrag gilt für "
                            f"dieses Feld ({gelaende.name(art)}):",
                 fg=self.skin["text"], bg=self.skin["panel"], wraplength=300,
                 justify=tk.LEFT).pack(anchor=tk.W, padx=6)
        # Eine Zeile je Gebäude (Daniels Skizze: „auflisten") — vorher drei nebeneinander.
        knopfreihe = tk.Frame(info, bg=self.skin["panel"])
        knopfreihe.pack(anchor=tk.W, fill=tk.X, padx=6, pady=6)
        for i, (k, g) in enumerate(passend):
            kosten = baukosten(k) or {}
            # Dieselbe Deckungsfrage wie die Zahlung selbst (Ortslager zuerst, dann der
            # Reichsbestand) - sonst zeigt der Knopf "fehlt noch: holz", obwohl die Siedlung
            # das Holz hat (Fund des Sammellaufs nach Teil 3).
            _fehlt = self.state.ortsdeckung(siedlung, kosten)
            text = f"{g['name']}\n{self._ertrag_kurz(k, art)} · {kosten_text(kosten)}"
            if _fehlt:
                text += f"\nfehlt noch: {', '.join(sorted(_fehlt))}"
            tk.Button(knopfreihe, text=text, justify=tk.LEFT, anchor=tk.W,
                      command=lambda kk=k: self._karten_bauen(kk), bg=self.skin["button"],
                      fg=self.skin["gold"], activebackground="#5D4037").grid(
                row=i, column=0, padx=2, pady=2, sticky=tk.EW)

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

        # W4d: die WELTKARTE des Limbus aus `src/welt.py` — die 20 Dimensionen an ihren Plaetzen
        # (x/y aus data/welten.json), eigene gruen, fremde rot. Die sechs BELEGTEN Weltnamen sind
        # die einzigen, die das Handbuch nennt; die Anordnung ist der VORSCHLAG der Datei.
        meine_kennung = f"d{int(z):02d}"
        tk.Label(self.content, text="Weltkarte des Limbus — die sechs belegten Welten: "
                                    + ", ".join(str(d["welt"]) for d in welt.welten()),
                 fg=self.skin["gold"], bg=self.skin["bg"]).pack(anchor=tk.W, padx=10, pady=(6, 0))
        tk.Label(self.content, text=welt.beschreibung(meine_kennung), fg=self.skin["text"],
                 bg=self.skin["bg"], wraplength=760, justify=tk.LEFT).pack(anchor=tk.W, padx=10)
        karte = tk.Canvas(self.content, width=310, height=310, bg=self.skin["bg"], highlightthickness=0)
        karte.pack(anchor=tk.W, padx=10, pady=4)
        kachel = max(8, 310 // 10)
        for _d in welt.dimensionen():
            _nr = int(str(_d["kennung"]).lstrip("d"))
            _x1, _y1 = int(_d["x"]) * kachel, int(_d["y"]) * kachel
            karte.create_rectangle(_x1, _y1, _x1 + kachel - 2, _y1 + kachel - 2,
                                   fill=farben["gruen"] if _nr in eigene else farben["rot"],
                                   outline="#111111")
            karte.create_text(_x1 + kachel // 2 - 1, _y1 + kachel // 2 - 1,
                              text=f"{_nr:02d}", fill="#ffffff", font=("Arial", 7))
        _nachbarn = welt.nachbarn(meine_kennung)[:4]
        if _nachbarn:
            tk.Label(self.content, text="Portalpreise in die Nachbardimensionen: " + " · ".join(
                        f"{n['kennung']} ({int(n['_entfernung'])} Schritte) "
                        f"{welt.portalkosten(meine_kennung, n['kennung'])} Mana" for n in _nachbarn),
                     fg=self.skin["text"], bg=self.skin["bg"], wraplength=760,
                     justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=(0, 4))

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
            for ware in werkstatt.waren_der_werkstatt(kennung):
                erfuellt, grund = self.state.ware_voraussetzung(ware)
                knopf = tk.Button(rahmen, text=ware, command=lambda w=ware: self._ware_herstellen(w),
                                  bg="#3e2723" if erfuellt else "#4a4a4a",
                                  fg=self.skin["gold"] if erfuellt else "#9e9e9e")
                if not erfuellt:
                    knopf.config(state=tk.DISABLED)
                knopf.pack(side=tk.LEFT, padx=2)
            if schlange:
                tk.Label(self.content,
                         text="   " + werkstatt.fortschritt(schlange, self.state.spielsekunden)["text"],
                         fg="#C0C0C0", bg=self.skin["bg"]).pack(anchor=tk.W, padx=12)

    def _ware_herstellen(self, ware: str):
        """Eine Ware in der Werkstatt DIESES Ortes herstellen lassen — ueber den Kern (`ware_start`).

        Oekonomie-Paket, Schritt 9, Teil 6c (Entwurf Z. 779: „Herstellung gegen gewaehlten Ort").
        Der Kern prueft: freigegebenes Rezept, Forschungsvoraussetzungen der Ware, **Werkstatt VOR
        ORT** und die **Materialkosten im lokalen Lager**. Abgelehnt wird VOR jeder Aenderung —
        gearbeitet wird auf einer Kopie, uebernommen erst nach Erfolg. Fertig wird die Ware in
        `ort_tick`, und zwar im **Ortslager** (genau einmal).

        Die fruehere reichsweite Warteschlange (`werkstatt_schlangen`) ist damit fuer die
        Herstellung weg: sie hatte EINE Schlange fuer alle Siedlungen und buchte die Ware in den
        GLOBALEN Bestand — die Ware konnte so in einer Stadt entstehen und in einer anderen liegen.
        """
        ort = self.state.aktive_siedlung()
        if ort is None:
            self._log("Keine Siedlung — es gibt keine Werkstatt vor Ort.")
            return False
        levels = {k: int(v.level) for k, v in self.state.research.items()}
        try:
            neu = spieloekonomie.ware_start(asdict(ort), ware, levels, self.state.spielsekunden)
        except ValueError as fehler:
            self._log(f"{ware} nicht möglich: {fehler}")
            return False
        self.state._ort_uebernehmen(ort.id, neu)
        self._log(f"{ware} in der Werkstatt von {ort.name} in Arbeit.")
        self._render_view()
        return True

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
                tk.Button(rahmen, text="Angreifen", command=lambda mid=map_id: self._attack_map(mid),
                          bg=self.skin["button"], fg=self.skin["red"]).pack(anchor=tk.W, pady=2)
                tk.Button(rahmen, text="Karte zerstören",
                          command=lambda mid=map_id: self._destroy_map(mid),
                          bg=self.skin["button"], fg=self.skin["red"]).pack(anchor=tk.W, pady=2)
        else:
            tk.Label(rahmen, text="Freigeschaltet, aber noch nicht betreten — der Wechsel "
                                  "kostet Gold.", fg=self.skin["text"], bg=self.skin["panel"],
                     wraplength=560, justify=tk.LEFT).pack(anchor=tk.W)

    def _render_maps(self):
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
        # Kleine, belegte Verbesserung (offener Punkt aus Schritt 3): das ZIEL steht in der
        # Meldung, nicht nur im Log — sonst weiss man im Reiter „Nachrichten" nicht, wozu der
        # Bericht gehoert. Der Wortlaut des Berichts selbst bleibt unveraendert.
        self.state.messages.append(
            {"text": f"Ziel {ziel_name} — " + bericht["titel"] + "\n" + "\n".join(bericht["zeilen"]),
             "type": "kampf"})
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
        dauer = max(2, abstand * 5)
        ziel_bot = None
        for bot in self.state.bots:
            if random.random() < 0.3:
                ziel_bot = bot
                break
        self.state.movements.append({
            "from": f"{int(start[0])}:{int(start[1])}",
            "to": f"{int(ziel[0])}:{int(ziel[1])}",
            "units": dict(moving),
            "arrival": float(self.state.spielsekunden) + float(dauer) * 60.0,
            "map": self.state.current_map,
            "target_bot": ziel_bot.name if ziel_bot else None,
            "tile_key": f"{int(ziel[0])}:{int(ziel[1])}",
        })
        for u, anzahl in moving.items():
            self.state.units[u].count = max(0, self.state.units[u].count - anzahl)
        self._welt_start = None
        self.welt_auswahl = (int(ziel[0]), int(ziel[1]))
        self._log(f"Truppen bewegen nach {self._welt_koordinate(*ziel)}. "
                  f"Ankunft in {dauer} Minuten.")
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
            tk.Button(frame, text="Angreifen", command=lambda b=bot: self._attack(b), bg="#3e2723", fg=self.skin["red"]).pack(side=tk.RIGHT, padx=5)
            # W7 (Auftrags-Oberflaeche): EIN Angriff als Auftrag - mit Reisezeit, Rueckkehr und
            # Bericht in den Nachrichten. Der Name ist die Vorgabe aus der Uebergabe.
            tk.Button(frame, text="Angriff entsenden",
                      command=lambda b=bot: self._auftrag_angriff(b),
                      bg="#3e2723", fg=self.skin["gold"]).pack(side=tk.RIGHT, padx=5)

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
        if self.state.noob_protection and bot.noob_protection:
            self._log(f"{bot.name} steht unter Götterschutz. Angriff nicht möglich.")
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
                "vorraete": self._vorraete_des_ziels(bot),
                "verteidiger": dict(bot.army or {})}
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
            spielzeit.setzen(wert)
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
        tk.Label(self.content, text="Forschung braucht eine Bibliothek und Zeit: die Dauer ist die "
                                    "Stufe zum Quadrat in Stunden (Handbuch S. 12/13). Die Stufe "
                                    "steigt erst nach Ablauf.",
                 fg="#C0C0C0", bg=self.skin["bg"], wraplength=780,
                 justify=tk.LEFT).pack(anchor=tk.W, padx=10)
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
            tk.Label(frame, text=r.name, fg=self.skin["text"], bg=self.skin["panel"], width=15, anchor=tk.W).pack(side=tk.LEFT, padx=5)
            tk.Label(frame, text=f"Stufe {r.level}/{r.max_level}", fg="#DAA520", bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
            tk.Label(frame, text=r.effect, fg="#C0C0C0", bg=self.skin["panel"]).pack(side=tk.LEFT, padx=5)
            zustand = laufend.get(key) or {}
            if zustand.get("laufend"):
                rest = float(zustand.get("reststunden") or 0.0)
                tk.Label(frame, text=f"läuft auf Stufe {zustand.get('zielstufe')} · noch {rest:.1f} h",
                         fg=self.skin["gold"], bg=self.skin["panel"]).pack(side=tk.RIGHT, padx=5)
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
                if _frei:
                    _knopf.pack(side=tk.RIGHT, padx=5)
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
                        tk.Label(frame, text="schaltet frei — " + " · ".join(_teile),
                                 fg="#8FBF7F", bg=self.skin["panel"]).pack(side=tk.RIGHT, padx=5)
                else:
                    _knopf.config(state=tk.DISABLED, disabledforeground="#8a8a8a")
                    _knopf.pack(side=tk.RIGHT, padx=5)
                    tk.Label(frame, text=f"gesperrt: {_warum}", fg="#FDBA74",
                             bg=self.skin["panel"]).pack(side=tk.RIGHT, padx=5)

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
                _knopf = tk.Button(frame, text=f"Ausbilden ({gelaende.gebaeude_name(_staette)} Stufe {_stufe})",
                                   command=lambda k=key: self._train_unit(k), bg="#3e2723",
                                   fg=self.skin["gold"])
                if _frei:
                    _knopf.pack(side=tk.RIGHT, padx=5)
                    if ausruestung.bedarf(key):
                        # Teil 6c: die Ausruestung wird VOR ORT verbraucht — also wird auch die
                        # Anzeige gegen das Ortslager gerechnet (dieselbe Quelle wie die Ausbildung).
                        tk.Label(frame, text="Waren: " + ausruestung.bestand_text(
                            ausruestung.fehlende(key, (getattr(_ort_k, "waren", None) or {})
                                                 if _ort_k else self.state.waren)),
                            fg="#C0C0C0", bg=self.skin["panel"]).pack(side=tk.RIGHT, padx=5)
                else:
                    _knopf.config(state=tk.DISABLED, disabledforeground="#8a8a8a")
                    _knopf.pack(side=tk.RIGHT, padx=5)
                    tk.Label(frame, text=_grund, fg="#FDBA74", bg=self.skin["panel"],
                             wraplength=380, justify=tk.LEFT).pack(side=tk.RIGHT, padx=5)
            else:
                _fehlt = gelaende.gebaeude_name(_staette) if _staette else "Ausbildungsstätte unbekannt"
                tk.Label(frame, text=f"braucht {_fehlt}", fg="#e53935",
                         bg=self.skin["panel"]).pack(side=tk.RIGHT, padx=5)

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

    def _train_unit(self, key: str):
        """Eine Einheit in DIESEM Ort ausbilden lassen — ueber den Kern (`ausbildung_start`).

        Oekonomie-Paket, Schritt 9, Teil 6c (Entwurf Z. 781: „Ausbildung gegen gewaehlten Ort").
        Der Kern prueft VIER Dinge: Forschungsstufe der Einheit, **Ausbildungsstaette VOR ORT**,
        **genug freie Siedler im Ort** und die **Ausruestung im lokalen Warenlager**. Verbraucht
        werden Kosten, Siedler und Ausruestung; die Einheit entsteht erst am Ende der
        Ausbildungszeit in `ort_tick` — genau einmal.

        Der Altpfad ist damit weg: das fruehere **sofortige Hochzaehlen der Einheit** gibt es nicht
        mehr. Er haette die Einheit
        sofort und ohne Ortsbezug in den Reichsbestand gesetzt und die Ausruestung GLOBAL
        verbraucht — zwei Wege zu derselben Einheit sind genau das, was der Entwurf verbietet
        („Altmodus liest alte Felder; Neumodus nur einheiten", Z. 774).
        """
        u = self.state.units[key]
        ort = self.state.aktive_siedlung()
        if ort is None:
            # Wie beim Bauen: ohne Siedlung gibt es kein Ortslager — der Grund nennt trotzdem die
            # fehlende Stätte (sie steht in data/units.json).
            _staette = (einheiten.alle().get(key) or {}).get("gebaeude")
            _name = gelaende.gebaeude_name(_staette) if _staette else "Ausbildungsstätte"
            self._log(f"{u.name} braucht {_name} auf einer Siedlungskarte — es gibt noch keine "
                      f"Siedlung.")
            return False
        # Die Stätte ist die GRUNDBEDINGUNG: ohne sie gibt es keinen Ort, an dem ausgebildet wird.
        # Sie steht deshalb VOR der Forschungs-/Ausrüstungsprüfung — und ihr Name kommt aus derselben
        # Quelle wie beim Bauen. (Der Kern prüft sie ebenfalls; hier geht es um den genauen Grund.)
        _da, _staette, _stufe = gebaeude_wirkung.ausbildungsstaette([ort], key)
        if not _da:
            _name = gelaende.gebaeude_name(_staette) if _staette else "Ausbildungsstätte"
            meldung = f"{u.name} braucht {_name} auf einer Siedlungskarte — noch nicht gebaut."
            self._log(meldung)
            self.state.messages.append({"text": meldung, "type": "ausbildung"})
            self._render_view()
            return False
        # Erst die BEGRUENDUNG aus derselben Quelle wie die Ansicht (Soll/Ist), dann die verbindliche
        # Pruefung im Kern: so liest der Spieler den genauen Grund, und der Kern entscheidet.
        frei, grund = self._ausbildungs_hindernis(key)
        if not frei:
            meldung = f"{u.name} {grund}."
            self._log(meldung)
            self.state.messages.append({"text": meldung, "type": "ausbildung"})
            self._render_view()
            return False
        levels = {k: int(v.level) for k, v in self.state.research.items()}
        try:
            neu = spieloekonomie.ausbildung_start(asdict(ort), key, levels, self.state.spielsekunden)
        except ValueError as fehler:
            grund = str(fehler)
            # Der Kern sagt knapp, WAS fehlt ("Ausbildungsstätte fehlt vor Ort."). Der Spieler
            # braucht den Namen des Gebaeudes — er kommt aus derselben Quelle wie beim Bauen.
            if "Ausbildungsstätte fehlt vor Ort" in grund:
                _staette = (einheiten.alle().get(key) or {}).get("gebaeude")
                _name = gelaende.gebaeude_name(_staette) if _staette else "Ausbildungsstätte"
                grund = f"es fehlt {_name} in dieser Siedlung"
            meldung = f"{u.name} nicht ausgebildet: {grund}"
            self._log(meldung)
            self.state.messages.append({"text": meldung, "type": "ausbildung"})
            self._render_view()
            return False
        self.state._ort_uebernehmen(ort.id, neu)
        _auftrag = (neu.get("ausbildung") or [{}])[-1]
        _minuten = max(0.0, float(_auftrag.get("ende", self.state.spielsekunden))
                       - float(self.state.spielsekunden)) / 60.0
        self._log(f"{u.name} in Ausbildung vor Ort ({ort.name}) — fertig in {_minuten:.1f} "
                  f"Spielminuten. Die Einheit entsteht am Ende der Zeit im Ortslager.")
        self._render_view()
        return True

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

    def _pruefe_spielende(self):
        """Sieg/Niederlage pruefen und EINMAL festhalten (Vorgabe Daniel 05.10.2026, Option A).

        Wird aus dem Takt aufgerufen. Ist die Partie entschieden, steht sie im Zustand
        (`state.spielende`), in den Nachrichten und im Log — und die Spieluhr wird danach nicht
        mehr weitergezogen (siehe `_tick_loop`). Rueckgabe: 'sieg', 'niederlage' oder None.
        Die Bedingung selbst kommt aus `src/punkte.py` (dort als VORSCHLAG gekennzeichnet,
        weil das Handbuch keine nennt).
        """
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
        now = time.time()
        dt = now - self.state.last_tick
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
            ohne_quelle = rate <= 0 and r in ("holz", "stein", "nahrung") and bool(self.state.settlements)
            lbl.config(text=f"{RESOURCE_ICONS[r]} {int(res.amount)} ({'⚠' if ohne_quelle else prod_text})",
                       fg=("#FDBA74" if ohne_quelle else self.skin["text"]))
        self.lbl_day.config(text=f"Tag {self.state.day}")
        if getattr(self, "lbl_tempo", None) is not None:
            self.lbl_tempo.config(text=f"Tempo {spielzeit.text()}")
        # W6: die Punktanzeige kommt aus den Originalformeln (src/punkte.py, Handbuch S. 3/5/6).
        # Vorher standen hier `score`, `ruf` und eine selbst gebaute Summe - die Gesamtzahl
        # war damit nachweislich falsch.
        staende = {k: v.level for k, v in self.state.research.items()}
        einheiten = {k: v.count for k, v in self.state.units.items()}
        wall_stufe = gebaeude_wirkung.wall_stufe(self.state.settlements)
        self.lbl_forschung.config(text=f"Forschung: {punkte.forschungspunkte(staende)}")
        self.lbl_krieg.config(text=f"Krieg: {punkte.kriegspunkte(einheiten, wall_stufe)}")
        self.lbl_gesamt.config(text=f"Gesamt: {punkte.gesamtpunkte(staende, einheiten, wall_stufe)}")
        # Schritt 31: Ziel und Spielende sichtbar machen (Vorgabe Daniel 05.10.2026, Option A).
        # ZUERST pruefen, DANN anzeigen — sonst zeigt die Leiste einen Takt lang den alten Stand.
        self._pruefe_spielende()
        ziel = punkte.VORSCHLAG_ZIEL_PUNKTE
        stand = self.state.punktestand()
        if getattr(self, "lbl_ziel", None) is not None:
            if self.state.spielende == "sieg":
                self.lbl_ziel.config(text=f"SIEG — Ziel von {ziel} Punkten erreicht.",
                                     fg=self.skin["gold"])
            elif self.state.spielende == "niederlage":
                self.lbl_ziel.config(text="NIEDERLAGE — keine Siedlung und keine Einheit mehr.",
                                     fg=self.skin["red"])
            else:
                self.lbl_ziel.config(text=f"Ziel: {stand['gesamt']} / {ziel} Punkte",
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
