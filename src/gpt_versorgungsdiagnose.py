"""Nur-lesende Versorgungsdiagnose fuer Nebelseetal.

GPT-Zuarbeit 002: keine Aenderung an Spielregeln, Spielstand oder Hermes-Dateien.
Quellen: src/gelaende.py, src/wirtschaft.py, data/baupreise.json und Handbuch.
Die Diagnose verwendet nur LOKALE Vorratsdaten. Reichs-/Fremdbestaende sind
NICHT als kostenlos verfuegbare Baukasse einzurechnen.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import gelaende
import spieldaten
import wirtschaft

PREISE = json.loads((Path(spieldaten.projektwurzel()) / 'data' / 'baupreise.json').read_text(encoding='utf-8'))['preise']
GRUNDVERSORGUNG = {
    'holz': ('holzfaeller',),
    'stein': ('steinmetz',),
    'nahrung': ('jaeger', 'farm'),
}


def _feld(obj, key, default=None):
    return obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)


def _kostensatz(kennung):
    """Originale Gebaeudepreise, soweit belegt; andere Preise sind Vorschlaege."""
    return {k: float(v) for k, v in PREISE[kennung].items()
            if k in {'holz', 'stein', 'nahrung', 'metall', 'gold', 'wolle', 'leder', 'pferde', 'mana', 'siedler'}
            and isinstance(v, (int, float)) and not isinstance(v, bool)}


def _arten_freier_felder(ort):
    karte = _feld(ort, 'karte') or {}
    raster = karte.get('raster') or []
    bauten = _feld(ort, 'bauten') or {}
    return [art for i, art in enumerate(raster) if str(i) not in bauten]


def _pruefe_kauf(ort, kosten, rate):
    vorrat = _feld(ort, 'vorraete') or {}
    siedler = float(_feld(ort, 'bevoelkerung', 0) or 0)
    max_zeit = 0.0
    fehler = []
    for roh, menge in kosten.items():
        haben = siedler if roh == 'siedler' else float(vorrat.get(roh, 0) or 0)
        mangel = max(0.0, menge - haben)
        if mangel < 1e-9:
            continue
        ertrag = float(rate.get(roh, 0))
        if roh == 'siedler':
            # Einwohnerwachstum braucht separate Beleg-/Grenzpruefung; nicht als gratis behandeln.
            fehler.append({'rohstoff': roh, 'fehlt': mangel, 'grund': 'Siedler fehlen; Siedlerwachstum separat pruefen'})
        elif ertrag <= 0:
            fehler.append({'rohstoff': roh, 'fehlt': mangel, 'grund': 'keine laufende Eigenproduktion'})
        else:
            max_zeit = max(max_zeit, mangel / ertrag)
    if fehler:
        return {'status': 'nicht_aus_eigener_produktion_erreichbar', 'wartezeit_stunden': None,
                'blockaden': fehler}
    if max_zeit > 0:
        return {'status': 'durch_warten_erreichbar', 'wartezeit_stunden': round(max_zeit, 3), 'blockaden': []}
    return {'status': 'sofort_baubar', 'wartezeit_stunden': 0.0, 'blockaden': []}


def untersuche(ort, forschung=None):
    """Berichtet ueber die DREI Grundressourcen und Baupfade.

    Reine Diagnose, keine Ressourcenbuchung und KEINE definitive Aussage, dass
    ein Spielstand nicht rettbar sei (Importe, Abbruch, Gegner koennen helfen).
    """
    forschung = forschung or {}
    karte = _feld(ort, 'karte') or {}
    raster = karte.get('raster') or []
    if not raster:
        raise ValueError('Es ist keine Siedlungskarte mit Raster vorhanden.')
    rate = {k.lower(): float(v) for k, v in wirtschaft.ertrag_gesamt([ort], forschung).items()}
    freie = _arten_freier_felder(ort)
    ausgabe = {}
    for roh, gebaeude_ids in GRUNDVERSORGUNG.items():
        optionen = []
        for gid in gebaeude_ids:
            if gid == 'farm' and int(forschung.get('Baukunst', 0) or 0) < 1:
                optionen.append({'gebaeude': gid, 'status': 'forschung_fehlend',
                                 'grund': 'Baukunst mindestens Stufe 1 erforderlich'})
                continue
            gel = sorted(set(art for art in freie if gelaende.bau_moeglich(gid, art)[0]
                             and gelaende.ertrag_pro_stunde(gid, art) is not None))
            if not gel:
                optionen.append({'gebaeude': gid, 'status': 'kein_freies_passendes_feld'})
                continue
            kosten = _kostensatz(gid)
            kauf = _pruefe_kauf(ort, kosten, rate)
            optionen.append({'gebaeude': gid, 'gelande': gel, 'kosten': kosten, **kauf})
        aktive_rate = float(rate.get(roh, 0))
        kann = any(o['status'] in ('sofort_baubar','durch_warten_erreichbar') for o in optionen)
        status = ('laufende_produktion' if aktive_rate > 0 else
                  'produzent_erschliessbar' if kann else 'ohne_import_blockiert')
        ausgabe[roh] = {'bestand_lokal': float((_feld(ort, 'vorraete') or {}).get(roh, 0) or 0),
                        'produktion_pro_spielstunde': aktive_rate, 'status': status,
                        'bauoptionen': optionen}
    return {
        'siedlung': str(_feld(ort, 'name', _feld(ort, 'id', '?'))),
        'kartenfelder': len(raster),
        'freie_felder': len(freie),
        'bebaubare_felder': sum(gelaende.ist_bebaubar(a) for a in raster),
        'grundversorgung': ausgabe,
        'warnungen': [f'{roh}: keine laufende Produktion und kein aus eigener Produktion erreichbarer Neubau'
                      for roh, eintrag in ausgabe.items() if eintrag['status'] == 'ohne_import_blockiert'],
        'hinweis': 'Diagnose ist KEIN Auto-Rettungssystem. Ortslager zuerst; Fremdversorgung nur durch echte Transporte. Baupreise ausser vier belegten Positionen sind Vorschlaege.'
    }


def drucktext(bericht):
    zeilen = [f"Versorgung {bericht['siedlung']}: {bericht['kartenfelder']} Felder / {bericht['bebaubare_felder']} bebaubar"]
    for roh, d in bericht['grundversorgung'].items():
        zeilen.append(f"{roh}: {d['bestand_lokal']:g} im Ort, {d['produktion_pro_spielstunde']:g}/h, {d['status']}")
        for o in d['bauoptionen']:
            zeilen.append('  ' + o['gebaeude'] + ': ' + o['status'] + (f", fruehestens {o['wartezeit_stunden']:g} h" if o.get('wartezeit_stunden') else ''))
    zeilen.extend('WARNUNG: ' + w for w in bericht['warnungen'])
    return '\n'.join(zeilen)
