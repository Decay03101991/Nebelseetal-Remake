"""Externer Regressionstest: Admin-Gaben, Kartenwechsel, Weltteleport-Transaktionen.

Keine Veraenderung am Hauptprojekt. Originalwerte und freie Karten aus src/data.
"""
from __future__ import annotations
from dataclasses import asdict
from copy import deepcopy
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import abschnitt, check, ausnahme, bericht, import_src
import_src()
import main
import admin_teststand
import admin_werkzeuge as a
import einheiten
import spielstaende
import tempfile


def muss_ablehnen(aktion):
    try:
        aktion()
    except (ValueError, PermissionError, TypeError):
        return True
    return False


def pruefen():
    state = main.GameState()
    state.generate_map(state.current_map)
    admin_teststand.teststand_aufbauen(state, main.Settlement, main.siedlung_kennung)
    s0 = state.settlements[0]
    s1 = state.settlements[1]
    abschnitt('Vollstaendige Testwirtschaft')
    for ort in state.settlements:
        fehlend = set(admin_teststand.KETTENGEB) - set(ort.bauten.values())
        check(ort.name + ': alle 8 Kettengebaeude aufgebaut', not fehlend, str(fehlend))
    check('Rohstoffe: 9 Originalsorten', len(a.verfuegbare_posten('Rohstoff')) == 9)
    check('Waren: 17 Originalsorten', len(a.verfuegbare_posten('Ware')) == 17)
    check('Einheiten: 28 Originalsorten', len(a.verfuegbare_posten('Einheit')) == 28)
    check('nicht vorhandene Kategorie unzulaessig', muss_ablehnen(lambda: a.verfuegbare_posten('Cheat')))
    abschnitt('Admin-Freigabe und lokale Bestandsvergabe')
    vorher = s0.vorraete['stein']
    fremd = s1.vorraete['stein']
    check('ohne Adminfreigabe gesperrt', muss_ablehnen(lambda: a.geben(state, s0.id, 'Rohstoff', 'stein', 5)))
    check('nicht existierende Rohstoffe gesperrt', muss_ablehnen(lambda: a.geben(state, s0.id, 'Rohstoff', 'kristall', 5, freigabe=True)))
    for schlecht in (-1, 0, 1.5, True, 1000001):
        check(f'ungueltige Menge {schlecht!r} gesperrt', muss_ablehnen(lambda schlecht=schlecht: a.geben(state, s0.id, 'Rohstoff', 'stein', schlecht, freigabe=True)))
    neu = a.geben(state, s0.id, 'Rohstoff', 'stein', 9, freigabe=True)
    check('Stein nur einmal lokal vergeben', neu == vorher + 9 and s0.vorraete['stein'] == vorher + 9)
    check('Nachbardorf bei Adminvergabe unveraendert', s1.vorraete['stein'] == fremd)
    ware = a.verfuegbare_posten('Ware')[0]
    einheit = a.verfuegbare_posten('Einheit')[0]
    w0 = s0.waren.get(ware, 0)
    e0 = s0.einheiten.get(einheit, 0)
    a.geben(state, s0.id, 'Ware', ware, 3, freigabe=True)
    a.geben(state, s0.id, 'Einheit', einheit, 4, freigabe=True)
    check('Warenvergabe im Ortslager', s0.waren[ware] == w0 + 3)
    check('Truppenvergabe im Ortslager', s0.einheiten[einheit] == e0 + 4)
    abschnitt('Siedlungskarten wahlweise und ohne Doppelbelegung')
    check('keine vergebenen Karten zur Neuwahl', s1.karte['typ'] not in a.freie_karten(state, s0.id))
    freie = [k for k in a.freie_karten(state, s0.id) if k != s0.karte['typ']]
    check('weitere Karte frei aus Vorrat', bool(freie))
    vor_bauten = sorted(s0.bauten.values())
    if freie:
        alte_karte = s0.karte['typ']
        try:
            neue = a.karte_waehlen(state, s0.id, freie[0], freigabe=True)
            check('Karte durch Admin zugewiesen', neue['typ'] == freie[0] and s0.karte['typ'] == freie[0])
            check('alle Bauten bleiben nach Kartenwechsel', sorted(s0.bauten.values()) == vor_bauten)
            check('Kartentyp je Dorf weiterhin einzigartig', len(set(s.karte['typ'] for s in state.settlements)) == len(state.settlements))
        except ValueError as e:
            check('Kartenwechsel moeglich', False, str(e))
    abschnitt('Admin-Weltreise: gesperrte Ziele haben keine Seiteneffekte')
    aktuelle_karte = state.current_map
    region = 'wald'
    n = next(m['size'] for m in main.MAPS if m['id'] == region)
    tiles = [asdict(main.MapTile(x=x, y=y, terrain=('water' if (x, y)==(0, 0) else 'forest')))
             for y in range(n) for x in range(n)]
    state.admin_weltkarten[region] = tiles
    vorher = (s0.map_id, s0.x, s0.y)
    anzeige = deepcopy(state.map_tiles)
    bots = deepcopy(state.bots)
    check('Positionierung ohne Freigabe gesperrt', muss_ablehnen(lambda: a.positionieren(state, s0.id, region, 1, 1, main.MAPS)))
    check('negative Koordinaten gesperrt', muss_ablehnen(lambda: a.positionieren(state, s0.id, region, -1, 1, main.MAPS, freigabe=True)))
    check('Wasserziel gesperrt', muss_ablehnen(lambda: a.positionieren(state, s0.id, region, 0, 0, main.MAPS, freigabe=True)))
    check('nach Ablehnung dieselbe Welt', state.current_map == aktuelle_karte)
    check('nach Ablehnung dieselben Kartentiles', state.map_tiles == anzeige)
    check('nach Ablehnung dieselben Bots', state.bots == bots)
    check('nach Ablehnung dieselbe Dorfposition', (s0.map_id, s0.x, s0.y) == vorher)
    check('nach Ablehnung kein Weltgebiet freigeschaltet', region not in state.unlocked_maps)
    a.positionieren(state, s0.id, region, 1, 1, main.MAPS, freigabe=True)
    check('gültige Weltreise aktualisiert Dorf', (s0.map_id, s0.x, s0.y) == (region, 1, 1))
    check('gültige Weltreise zeigt Zielgebiet', state.current_map == region)
    check('Zielkarte traegt sichtbaren Spieler-Marker', state.get_tile(1, 1, n).sector_name == s0.name)
    check('alte Weltkarte hat Marker nicht mehr', state.admin_weltkarten[aktuelle_karte][vorher[2]*20 + vorher[1]]['npc_faction'] is None)
    abschnitt('Admin-Teststand nach Gebietswechsel speicherbar')
    with tempfile.TemporaryDirectory() as ordner:
        pfad=spielstaende.admin_pfad(ordner)
        check('speichert im Admin-Pfad', state.save(pfad,admin_freigabe=True))
        geladen=main.GameState()
        check('nur mit Freigabe ladbar', muss_ablehnen(lambda: a.geben(geladen, s0.id,'Rohstoff','stein',1,freigabe=True)))
        check('Admin-Teststand laedt separat', geladen.load(pfad,admin_freigabe=True))
        check('Admin-Weltkarte nach Laden erhalten', geladen.current_map == region and loaded_len(geladen) == len(state.map_tiles))
        check('Admin-Gebietscache erhalten', aktuelle_karte in geladen.admin_weltkarten)
        check('Admin-Stand nicht normal speicherbar', not geladen.save(spielstaende.slot_pfad(ordner,1)))


def loaded_len(state):
    return len(state.map_tiles)


if __name__ == '__main__':
    ausnahme('Adminwerkzeuge und Weltposition', pruefen)
    sys.exit(bericht())
