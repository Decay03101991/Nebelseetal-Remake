"""Isolierte Admin-Testwerkzeuge (keine Aenderung der normalen Spielregeln).

Alle Mutationen brauchen eine explizite Admin-Freigabe UND den Teststand-Marker.
Authentifizierung erfolgt in der GUI ueber das separate Passworttor, nicht hier.
Quellen fuer Kennungen/Werte: vorhandene Spieldaten, keine neuen Fantasy-Einheiten.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict
import math
import random

import einheiten
import gelaende
import spieloekonomie
import spieldaten

ROHSTOFFE = ("holz", "stein", "metall", "mana", "nahrung", "gold", "wolle", "leder", "pferde")
MAX_ZUGABE = 1_000_000


def _pruefe_admin(state, freigabe):
    if not freigabe or not getattr(state, "admin_teststand", False):
        raise PermissionError("Admin-Werkzeug nur mit separater Freigabe im Admin-Teststand.")
    if not getattr(state, "oekonomie_aktiv", False):
        raise ValueError("Admin-Testwerkzeuge erfordern die lokale Oekonomie.")


def spielerhilfe_modus_setzen(state, modus, *, freigabe=False):
    """Nur im Admin-Teststand: UI-Sichtbarkeit, nicht Götterschutz oder Spielwerte."""
    _pruefe_admin(state, freigabe)
    import spielerhilfe
    if type(modus) is not str or modus not in spielerhilfe.ADMIN_HILFE_MODI:
        raise ValueError("Ungueltiger Spielerhilfe-Anzeigemodus.")
    state.admin_hilfe_modus = modus
    if hasattr(state, "_log"):
        state._log(f"ADMIN-TEST: Spielerhilfe-Sichtbarkeit auf {modus} gesetzt.")
    return modus


def _ort(state, siedlung_id):
    ort = next((s for s in state.settlements if s.id == siedlung_id), None)
    if ort is None:
        raise ValueError("Unbekannte Siedlung.")
    return ort


def verfuegbare_posten(kategorie):
    """Aus den originalgetreuen Datentabellen (nicht aus veralteter GOODS-Liste)."""
    if kategorie == "Rohstoff":
        return tuple(ROHSTOFFE)
    if kategorie == "Ware":
        return tuple(sorted(spieldaten.waren()))
    if kategorie == "Einheit":
        return tuple(sorted(einheiten.namen()))
    raise ValueError("Unbekannte Kategorie.")


def geben(state, siedlung_id, kategorie, name, menge, *, freigabe=False):
    """Fuegt Bestand nur dem gewaehltEN Ortslager hinzu, kein zweites Reichslager."""
    _pruefe_admin(state, freigabe)
    ort = _ort(state, siedlung_id)
    if name not in verfuegbare_posten(kategorie):
        raise ValueError("Unbekannter Originalposten oder falsche Kategorie.")
    if type(menge) is not int or not (1 <= menge <= MAX_ZUGABE):
        raise ValueError("Menge muss ganzzahlig zwischen 1 und 1.000.000 liegen.")
    bestand = (ort.vorraete if kategorie == "Rohstoff" else
               ort.waren if kategorie == "Ware" else ort.einheiten)
    vorher = float(bestand.get(name, 0))
    if not math.isfinite(vorher) or vorher < 0 or vorher + menge > 100_000_000:
        raise ValueError("Unzulaessiger oder zu hoher Lagerbestand.")
    bestand[name] = vorher + menge if kategorie == "Rohstoff" else int(vorher) + menge
    if hasattr(state, "_reichsanzeige_aus_orten"):
        state._reichsanzeige_aus_orten()
    if hasattr(state, "_log"):
        state._log(f"ADMIN-TEST: {menge} {name} ({kategorie}) an {ort.name} vergeben.")
    return bestand[name]


def _karte_id(karte):
    return (karte or {}).get("typ")


def freie_karten(state, siedlung_id):
    """Fuer Neuvergabe zulaessige Karten inkl. aktueller Karte, keine Dopplung."""
    _ort(state, siedlung_id)
    besetzt = {_karte_id(s.karte) for s in state.settlements if s.id != siedlung_id}
    # Neu: Die private Karte hat eine echte Original-ID (Nr. 36). Das alte
    # Schluesselwort 'start' bleibt als Admin-Alias fuer alte Testmasken erhalten.
    moeglich = {"start"} if "original-036" not in besetzt and "start" not in besetzt else set()
    moeglich.update(k for k in state.kartenvorrat if k not in besetzt)
    if _karte_id(_ort(state, siedlung_id).karte) == "original-036":
        moeglich.add("start")
    return tuple(sorted(moeglich))


def _bauten_uebertragen(ort, neue_karte):
    """Bestehende Bauten nur auf zulaessige Felder umsetzen, sonst ohne Mutation scheitern."""
    raster = neue_karte["raster"]
    bauten, stufen = {}, {}
    for index, geb in sorted(ort.bauten.items(), key=lambda kv: int(kv[0])):
        alt = int(index)
        kandidaten = ([alt] if alt < len(raster) else []) + [i for i in range(len(raster)) if i != alt]
        neu = next((i for i in kandidaten if str(i) not in bauten and
                    gelaende.bau_moeglich(geb, raster[i])[0]), None)
        if neu is None:
            raise ValueError(f"Auf dieser Karte ist fuer {geb} kein geeignetes freies Feld uebrig.")
        bauten[str(neu)] = geb
        stufen[str(neu)] = ort.stufen.get(index, 1)
    return bauten, stufen


def karte_waehlen(state, siedlung_id, karten_id, *, freigabe=False):
    _pruefe_admin(state, freigabe)
    ort = _ort(state, siedlung_id)
    if karten_id not in freie_karten(state, siedlung_id):
        raise ValueError("Karte unbekannt oder bereits einer anderen Siedlung zugewiesen.")
    alt = _karte_id(ort.karte)
    if alt == karten_id:
        return ort.karte
    if karten_id == "start":
        karte = spieloekonomie.startkarte(state.kartenvorrat_seed or "admin", "spieler")
    else:
        karte = deepcopy(state.kartenvorrat[karten_id]["karte"])
    bauten, stufen = _bauten_uebertragen(ort, karte)
    # Erst nach VOLLSTAENDIGER Pruefung Bestandsdaten veraendern.
    if alt in state.kartenvorrat:
        state.kartenvorrat[alt]["besitzer"] = None
    if karten_id in state.kartenvorrat:
        state.kartenvorrat[karten_id]["besitzer"] = "spieler"
    ort.karte, ort.bauten, ort.stufen = karte, bauten, stufen
    if hasattr(state, "_log"):
        state._log(f"ADMIN-TEST: {ort.name} erhaelt Karte {karten_id}, Bauten regelkonform umgesetzt.")
    return karte


def _weltgroesse(karten_id, konfiguration):
    item = next((e for e in konfiguration if e["id"] == karten_id), None)
    if item is None:
        raise ValueError("Unbekanntes Weltgebiet.")
    return int(item["size"])


def gebiet_wechseln(state, karten_id, konfiguration, *, freigabe=False):
    """Admin-only Gebietswechsel ohne Kosten; pro Gebiet eigene persistent gespeicherte Tiles.

    Bots bleiben als Reichsgegner bestehen (generate_map duerfte sie sonst ersetzen).
    """
    _pruefe_admin(state, freigabe)
    _weltgroesse(karten_id, konfiguration)
    if not hasattr(state, "admin_weltkarten"):
        state.admin_weltkarten = {}
    if state.current_map == karten_id:
        return state.map_tiles
    if state.map_tiles:
        state.admin_weltkarten[state.current_map] = [asdict(t) for t in state.map_tiles]
    target = state.admin_weltkarten.get(karten_id)
    if target is not None:
        klasse = type(state.map_tiles[0])
        state.map_tiles = [klasse(**e) for e in target]
    else:
        bisherige_bots = state.bots
        state.generate_map(karten_id)
        state.bots = bisherige_bots
    state.current_map = karten_id
    if karten_id not in state.unlocked_maps:
        state.unlocked_maps.append(karten_id)
    if karten_id not in state.active_maps:
        state.active_maps.append(karten_id)
    for ort in state.settlements:
        if ort.map_id == karten_id:
            tile = state.get_tile(ort.x, ort.y, _weltgroesse(karten_id, konfiguration))
            if tile is not None:
                tile.npc_faction = "spieler"
                tile.sector_name = ort.name
    return state.map_tiles


def _ziel_vorpruefen(state, ort, karten_id, x, y, groesse):
    """Keine Mutationen; vor dem Verschieben muessen alle Sperren greifen."""
    ziel = state.get_tile(x, y, groesse)
    if ziel is None or ziel.terrain == "water":
        raise ValueError("Wasserfeld: kein gueltiger Siedlungsstandort.")
    belegt = any(s.id != ort.id and s.map_id == karten_id and s.x == x and s.y == y
                 for s in state.settlements)
    if belegt or (ziel.npc_faction not in (None, "spieler")):
        raise ValueError("Ziel bereits belegt; keine NPCs oder Siedlungen ueberschreiben.")
    if ziel.npc_faction == "spieler" and not (ort.map_id == karten_id and ort.x == x and ort.y == y):
        raise ValueError("Ziel besitzt bereits einen Spieler-Marker.")


def positionieren(state, siedlung_id, karten_id, x, y, konfiguration, *, freigabe=False):
    """Versetzt eine TESTsiedlung zu einer gueltigen Weltposition, auch in ein anderes Gebiet.

    Kein Teleport von Truppen mit aktiven Missionsreferenzen: Kennung bleibt stabil.
    Ein besetztes oder unbebaubares Feld wird nicht geraeumt.
    """
    _pruefe_admin(state, freigabe)
    ort = _ort(state, siedlung_id)
    groesse = _weltgroesse(karten_id, konfiguration)
    if type(x) is not int or type(y) is not int or not (0 <= x < groesse and 0 <= y < groesse):
        raise ValueError(f"Koordinaten fuer {karten_id}: 0 bis {groesse-1}.")
    # Reiseauftraege referenzieren die stabile Siedlungs-ID.
    # Vor dem Wechsel ein vollstaendiges Weltkarten-Checkpoint erstellen.
    # Ein unzulaessiger Zielort darf weder Karte/Bots/Marker noch
    # Freischaltungen veraendern (kein halber Admin-Teleport).
    zufallszustand = random.getstate()
    snapshot = {
        "current_map": state.current_map,
        "map_tiles": deepcopy(state.map_tiles),
        "bots": deepcopy(state.bots),
        "admin_weltkarten": deepcopy(getattr(state, "admin_weltkarten", {})),
        "unlocked_maps": list(state.unlocked_maps),
        "active_maps": list(state.active_maps),
    }
    try:
        gebiet_wechseln(state, karten_id, konfiguration, freigabe=True)
        _ziel_vorpruefen(state, ort, karten_id, x, y, groesse)
    except Exception:
        for name, wert in snapshot.items():
            setattr(state, name, wert)
        random.setstate(zufallszustand)
        raise
    ziel = state.get_tile(x, y, groesse)
    altes_gebiet, ax, ay = ort.map_id, ort.x, ort.y
    if altes_gebiet == karten_id:
        alt = state.get_tile(ax, ay, groesse)
        if alt is not None and alt.npc_faction == "spieler":
            alt.npc_faction = None
            alt.sector_name = None
    else:
        vorher = (getattr(state, "admin_weltkarten", {}) or {}).get(altes_gebiet, [])
        alte_groesse = _weltgroesse(altes_gebiet, konfiguration)
        index = ay * alte_groesse + ax
        if 0 <= index < len(vorher) and vorher[index].get("npc_faction") == "spieler":
            vorher[index]["npc_faction"] = None
            vorher[index]["sector_name"] = None
    ort.map_id, ort.x, ort.y = karten_id, x, y
    state.aktive_siedlung_id = ort.id
    ziel.npc_faction = "spieler"
    ziel.sector_name = ort.name
    if hasattr(state, "_log"):
        state._log(f"ADMIN-TEST: {ort.name} nach {karten_id} ({x},{y}) versetzt.")
    return ort
