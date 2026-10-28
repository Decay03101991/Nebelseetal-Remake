"""Reine Vorabpruefung auf selbst verschuldete Rohstoff-Sackgassen.

GPT-Zuarbeit 28.10.2026. Aendert weder Preise, Ertrag, Spielstand noch
Originalregeln. Die genau eine Preisquelle wird als Funktion uebergeben.

Nur fuer die aktivierte lokale Oekonomie anzuwenden; alte Saves brauchen
eine eigene und explizite Migration. Die Pruefung ist bewusst konservativ:
Sie verlangt einen lokal moeglichen Weg zu Stein- und Holzproduktion,
auch wenn ein Import eventuell helfen koennte. Admin-Tests sind ausgenommen.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Callable
import math

import gelaende
import wirtschaft

PRODUZENT = {'holz': 'holzfaeller', 'stein': 'steinmetz'}


def _wert(objekt, name, sonst=None):
    return objekt.get(name, sonst) if isinstance(objekt, dict) else getattr(objekt, name, sonst)


def _normalisiere(siedlung):
    return {'karte': deepcopy(_wert(siedlung, 'karte')),
            'bauten': deepcopy(_wert(siedlung, 'bauten') or {}),
            'vorraete': dict(_wert(siedlung, 'vorraete') or {}),
            'bevoelkerung': float(_wert(siedlung, 'bevoelkerung', 0) or 0)}


def _quellen(ort):
    """Nur tatsaechliche Produktionsraten, keine Anzeige-Summenkasse."""
    # GPT-OEK01: die wirksame Ortsproduktion MUSS dieselbe Ertragsfunktion
    # wie spieloekonomie.ort_tick verwenden. Auf Originalkarten gehoeren
    # 1 Holz + 1 Stein pro Stunde zum Grundeinkommen (Jolly Roger, S. 3).
    # Nur den Gebaeudeanteil zu betrachten erzeugt eine falsche Softlock-
    # Sperre, obwohl die Rohstoffe durch Warten wieder erwirtschaftet werden.
    d = wirtschaft.ertrag_gesamt([ort])
    return {r: float(d.get(r.capitalize(), d.get(r, 0)) or 0) for r in PRODUZENT}


def _felder(ort, kennung):
    return [i for i, art in enumerate(ort['karte']['raster'])
            if str(i) not in ort['bauten'] and gelaende.bau_moeglich(kennung, art)[0]]


def _anlauf_moeglich(ort, preis_funktion, tiefe=0):
    """Probiert beide Bau-Reihenfolgen und respektiert echte Grundproduktion."""
    produktiv = _quellen(ort)
    fehlende = [r for r in PRODUZENT if produktiv[r] <= 0]
    if not fehlende:
        return True
    if tiefe >= 2:
        return False
    for res in fehlende:
        geb = PRODUZENT[res]
        freie = _felder(ort, geb)
        if not freie:
            continue
        preis = preis_funktion(geb)
        if not preis:
            continue
        # Warten nur auf nachweisbar PRODUZIERTE Rohstoffe: Holz/Stein.
        # Fehlender Siedler kann nach Originalregel nachwachsen, solange
        # das Wachstum nicht als Beleg fuer unendliche Baustoffe gilt.
        ohne_eigene_produktion_fehlend = any(
            key in PRODUZENT and produktiv[key] <= 0 and
            float(ort['vorraete'].get(key, 0)) + 1e-9 < float(menge)
            for key, menge in preis.items())
        if ohne_eigene_produktion_fehlend:
            continue
        if any(key not in PRODUZENT and key != 'siedler' and
               float(ort['vorraete'].get(key, 0)) + 1e-9 < float(menge)
               for key, menge in preis.items()):
            continue
        # Sobald eine Quelle laeuft, kann man dort bis zur benoetigten
        # Menge warten. Der Test behauptet keine konkrete Wartezeit.
        nachher = deepcopy(ort)
        for key, menge in preis.items():
            if key == 'siedler':
                continue
            vorhanden = float(nachher['vorraete'].get(key, 0))
            nachher['vorraete'][key] = max(0.0, vorhanden - float(menge))
        nachher['bauten'][str(freie[0])] = geb
        if _anlauf_moeglich(nachher, preis_funktion, tiefe + 1):
            return True
    return False


def risiko_nach_ausgabe(siedlung, kosten: dict, preis_funktion: Callable,
                        bau: tuple | None = None) -> list[str]:
    """Prueft unveraendernd, ob nach der Ausgabe beide Grundquellen erreichbar sind.

    Historische 10x10-Karten liefern 1 Holz und 1 Stein pro Stunde bereits
    ohne Produzenten. Dies ist ein ECHTER dauerhafter Produktionsweg, daher
    darf der Schutz keine künstliche Holzfäller-/Steinmetz-Pflicht erzeugen.
    Auf 8x7-Altentwürfen bleibt die strengere Erzeugerlogik erhalten.

    `bau=(gebaeude_id, feldindex)` simuliert auch die Belegung des gewaehlten
    Feldes. Keine Empfehlung zu kostenloser Ernte oder Originalwertaenderung.
    Gibt Warnungstexte zurueck; die GUI entscheidet, ob sie den Bau blockt.
    """
    if not _wert(siedlung, 'karte'):
        return []
    ort = _normalisiere(siedlung)
    for res, menge in kosten.items():
        if isinstance(menge, bool) or not isinstance(menge, (int,float)) or not math.isfinite(menge) or menge < 0:
            raise ValueError('Unzulaessiger Baupreis: ' + str(res))
        if res == 'siedler':
            ort['bevoelkerung'] -= menge
        else:
            ort['vorraete'][res] = float(ort['vorraete'].get(res, 0)) - menge
    if bau is not None:
        kennung, feld = bau
        if str(feld) not in ort['bauten']:
            ort['bauten'][str(feld)] = gelaende.finde_gebaeude(kennung) or kennung
    if _anlauf_moeglich(ort, preis_funktion):
        return []
    ertrag = _quellen(ort)
    fehlen = [roh for roh in PRODUZENT if ertrag[roh] <= 0]
    return ["VERSORGUNGSWARNUNG: Nach dieser Ausgabe ist keine eigenstaendige "
            "Holz- und Steinversorgung mehr gesichert. Erst Holzfaeller und "
            "Steinmetz auf geeigneten Feldern bauen (oder einen Transport "
            "organisieren). Es wird nichts abgebucht."] if fehlen else []


def offene_luecken():
    return ('Importe und unterwegs befindliche Karren werden hier bewusst nicht als '
            'garantierte Notversorgung gewertet. Bereits festgefahrene alte Saves '
            'werden nicht still veraendert; keine Ressourcen-Schenkungen.')


def risiko_nach_abriss(siedlung, feld: int, preis_funktion: Callable) -> list[str]:
    """Schuetzt die letzte bezahlbare Holz-/Steinquelle vor versehentlichem Abriss.

    Wenn die Siedlung *bereits* keine eigenstaendige Versorgung hat,
    wird ein Abriss nicht blockiert: er kann gerade ein geeignetes
    Feld fuer einen rettenden Produzenten freimachen.
    Keine Veraenderung am uebergebenen Spielzustand.
    """
    ort = _normalisiere(siedlung)
    index = str(feld)
    if index not in ort['bauten'] or not ort['karte']:
        return []
    if not _anlauf_moeglich(ort, preis_funktion):
        return []
    ort['bauten'].pop(index)
    if _anlauf_moeglich(ort, preis_funktion):
        return []
    return [
        'VERSORGUNGSWARNUNG: Dieser Abriss wuerde die letzte gesicherte '
        'Holz-/Steinversorgung abschneiden. Erst einen Ersatzproduzenten '
        'bauen oder genug Material fuer einen Neubau bereitstellen. '
        'Es wurde nichts abgerissen.'
    ]
