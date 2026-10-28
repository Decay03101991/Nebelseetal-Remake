"""Reproduzierbarer Admin-Teststand: keine Aenderung von Originalertraegen.

* Sechs unterschiedliche Karten (Start, Ausgleich, Holz, Minen, Farmen, Mischkarte)
* Gebietsspezifische Produktion, mit expliziter Stein- und Holzquelle
* Lokale Vorratslager, Einheiten und Testausruestung nur fuer Admin-Tests
* Keine Gratisressourcen im regulaeren Spiel; kein heimlicher Sieg
"""
from __future__ import annotations

from copy import deepcopy

import einheiten
import gelaende
import spieloekonomie

TEST_SEED = "ADMIN_TEST_2026_ORIGINALKARTEN_10x10"
KARTEN_IDS = ("start", "original-015", "original-037", "original-005", "original-019", "original-051")
NAMEN = ("Test-Hauptstadt", "Test-Ausgleich", "Test-Holzdorf", "Test-Bergdorf", "Test-Farmdorf", "Test-Mischdorf")
# Ausschliesslich Admin-Testvorrat. Nicht Teil der Wirtschaft, Preise oder Startwerte.
TEST_VORRAT = {"holz": 2500, "stein": 2500, "nahrung": 2500, "metall": 1500,
               "gold": 1500, "leder": 1200, "wolle": 1200, "pferde": 300,
               "mana": 800}
PRODUKTIONSGEB = ("holzfaeller", "steinmetz", "jaeger", "farm", "erzmine", "goldmine",
                  "schafszucht", "rinderfarm", "pferdezucht", "tempel")
KETTENGEB = ("bibliothek", "haus", "stellmacher", "schmiede", "bogenbauer", "naehstube",
             "kriegerakademie", "diebesgilde")


def _setzen(siedlung, gebaeude, anzahl=1):
    for _ in range(anzahl):
        feld_frei = None
        for feld, gel in enumerate(siedlung.karte["raster"]):
            if str(feld) in siedlung.bauten:
                continue
            if gelaende.bau_moeglich(gebaeude, gel)[0]:
                feld_frei = feld
                break
        if feld_frei is None:
            return False
        siedlung.bauten[str(feld_frei)] = gebaeude
        siedlung.stufen[str(feld_frei)] = 1
    return True


def teststand_aufbauen(state, settlement_typ, kennung_funktion):
    """Baut einen frischen Testzustand, kein Zugriff auf andere Spielstandsdateien.

    Wird nur ueber die separate Adminfreigabe der GUI angeboten. Es erfolgt kein
    heimlicher Write auf bestehende Slots oder den alten savegame.json.
    """
    state.settlements = []
    state.admin_teststand = True
    state.mode = "oeokonomie-1"
    state.oekonomie_aktiv = True
    state.spielende = None
    state.hatte_siedlung = True
    state.day = 1
    state.spielsekunden = 0.0
    state._day_accum = 0.0
    state.auftraege = []
    state.movements = []
    state.messages = []
    state.log = []
    state.kartenvorrat_anlegen(TEST_SEED)
    state._weltkarte_sicherstellen()
    felder = state.freie_weltfelder(anzahl=32)
    welt_size = max((tile.x for tile in state.map_tiles), default=-1) + 1
    if len(felder) < len(KARTEN_IDS):
        raise ValueError("Nicht genug freie Weltfelder fuer sechs Testdoerfer.")
    state.kartenvorrat_seed = TEST_SEED
    for index, (kennung, name) in enumerate(zip(KARTEN_IDS, NAMEN)):
        if kennung == "start":
            karte = spieloekonomie.startkarte(TEST_SEED, "spieler")
        else:
            if kennung not in state.kartenvorrat:
                raise ValueError(f"Testkarte fehlt: {kennung}")
            karte = deepcopy(state.kartenvorrat[kennung]["karte"])
            state.kartenvorrat[kennung]["besitzer"] = "spieler"
        x, y = felder[index]
        s = settlement_typ(name=name, map_id=state.current_map, x=x, y=y,
                           karte=karte, id=kennung_funktion("spieler", state.current_map, x, y))
        s.vorraete = dict(TEST_VORRAT)
        s.bevoelkerung = 35.0
        s.importiert = {}
        # Gefuelltes Warenlager ist explizit nur eine Admin-Testvorbereitung.
        s.waren = {name: 12 for name in state.waren}
        s.einheiten = {}
        # Der Teststand hat absichtlich eine breite Grundversorgung und Ausbauketten.
        for geb in ("holzfaeller", "steinmetz", "jaeger", "farm"):
            _setzen(s, geb)
        for geb in KETTENGEB:
            _setzen(s, geb)
        # Mehr als ein Produzent im jeweils spezialisierten Dorf.
        fokus = {"original-037": "holzfaeller", "original-005": "steinmetz",
                 "original-019": "farm", "original-051": "steinmetz",
                 "original-015": "holzfaeller"}.get(kennung)
        if fokus:
            _setzen(s, fokus, 2)
        for geb in PRODUKTIONSGEB:
            _setzen(s, geb)
        # Tatsaechliche Testeinheiten gehoeren ins Dorf, nicht in einen globalen Pool.
        for einheit in ("Handkarren", "Siedlerkarren", "Handelskarawane",
                        "Bürgerwehr", "Krieger", "Kurzbogenschütze", "Dieb"):
            if einheit in einheiten.namen():
                s.einheiten[einheit] = 3
        state.settlements.append(s)
        tile = state.get_tile(x, y, welt_size)
        if tile is not None:
            tile.npc_faction = "spieler"
            tile.sector_name = s.name
    state.aktive_siedlung_id = state.settlements[0].id
    for k, v in state.research.items():
        if k in ("Baukunst", "Wagenbau", "Felderwirtschaft", "Steinbruch", "Forstwirtschaft",
                 "Kriegskunst", "Waffentechnik", "Rüstungsbau", "Schmiedekunst",
                 "Nähkunst", "Heimlichkeit", "Bogenbau", "Nähen"):
            v.level = max(v.level, 3)
    state._reichsanzeige_aus_orten()
    # Alle verbindlichen Testketten muessen wirklich vorhanden sein; nicht
    # stillschweigend einen unbekannten Gebaeudenamen uebergehen.
    for ort in state.settlements:
        fehlend = sorted(set(KETTENGEB) - set(ort.bauten.values()))
        if fehlend:
            raise ValueError(f"Admin-Teststand unvollstaendig: {ort.name}, fehlt: {fehlend}")
    return state
