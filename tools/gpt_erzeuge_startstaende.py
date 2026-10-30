"""Testvorlagen im Zielordner erstellen, keine Benutzerdateien ueberschreiben.

Externe GPT-Zuarbeit (28.10.2026). Original-Handbuch und bestehende
Spiel-Methoden sind Quelle fuer Startwerte und Karten, keine Zufallsboni.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from pathlib import Path
import random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import admin_teststand
import main
import spielstaende

@contextmanager
def deterministic(seed: int):
    vor = random.getstate()
    random.seed(seed)
    try:
        yield
    finally:
        random.setstate(vor)


def neu_erzeugen():
    """Nutze den echten GUI-Pfad zur Gruendung, nur ohne Fenster."""
    state = main.GameState()
    gui = main.NebelseetalApp.__new__(main.NebelseetalApp)
    gui.state = state
    gui._log = state._log
    gui._render_view = lambda: None
    with deterministic(20261028):
        gui._erste_siedlung_gruenden()
    if len(state.settlements) != 1:
        raise RuntimeError('Startstadt wurde nicht gruendet')
    s = state.settlements[0]
    assert s.karte['spalten'] == 10 and s.karte['zeilen'] == 10
    assert len(s.karte['raster']) == 100 and s.karte.get('originalkarte_id')
    assert s.vorraete == {'holz':100.0,'stein':100.0}
    assert s.bevoelkerung == 10.0 and not s.bauten
    assert state.spielende is None and not state.admin_teststand
    return state


def admin_erzeugen():
    state = main.GameState()
    with deterministic(20261028):
        admin_teststand.teststand_aufbauen(state, main.Settlement, main.siedlung_kennung)
    assert state.admin_teststand
    assert len(state.settlements) == 6
    return state


def erzeugen(ausgabe):
    basis = Path(ausgabe)
    basis.mkdir(parents=True, exist_ok=True)
    neu = spielstaende.slot_pfad(str(basis), 1)
    admin = spielstaende.admin_pfad(str(basis))
    for pfad in (neu, admin):
        if Path(pfad).exists():
            raise FileExistsError(f'Bestehender Stand wird NICHT ueberschrieben: {pfad}')
    a = neu_erzeugen()
    if not a.save(neu):
        raise RuntimeError('Normalen Slot nicht gespeichert')
    b = admin_erzeugen()
    if not b.save(admin, admin_freigabe=True):
        raise RuntimeError('Admin-Teststand nicht gespeichert')
    # Rundlauf wirklich im GameState, nicht nur JSON-Parser.
    normal_neu = main.GameState()
    admin_neu = main.GameState()
    assert normal_neu.load(neu) and not normal_neu.admin_teststand
    assert not admin_neu.load(admin)
    assert admin_neu.load(admin, admin_freigabe=True) and admin_neu.admin_teststand
    assert normal_neu.settlements[0].vorraete['stein'] == 100.0
    assert len(admin_neu.settlements) == 6
    return neu, admin

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--ausgabe',required=True)
    ns=p.parse_args()
    for name in erzeugen(ns.ausgabe):
        print('ERSTELLT',name)
