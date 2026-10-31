"""Isolierter Wallkern fuer Nebelseetal (GPT-Zuarbeit, 28.10.2026).

Das Remake-Modell (keine Behauptung ueber Originalbaukosten):
- Verteidigungsanlagen: einmal erforschter, reichsweiter Technologiestand (1..10).
- Jede Siedlung aktiviert ihre eigene Verteidigung durch eine einmalige
  Aktion 'Wall errichten / Wache besetzen', OHNE einen Kartenplatz zu belegen.
- Aktiver Wall entspricht der freigeschalteten Stufe. Die Forschung wirkt
  automatisch; Zustand/Schaden bleibt in jeder Siedlung separat.
- Die einmalige Errichtung kostet den BEREITS HINTERLEGTEN Wall-Preis,
  der laut data/baupreise.json ein Vorschlag und nicht originalbelegt ist.
- SK-Schwellen werden nicht erfunden: gebaeude_wirkung.wall_schwelle.

Nur Regeln, kein UI/Dateizugriff, keine Mutation bei fehlgeschlagener Buchung.
Integration ab GPT-W02 in src/main.py auf isolierter GPT-Arbeitskopie; Hermes fuehrt.
"""
from __future__ import annotations

from typing import Any, Mapping


def _feld(objekt: Any, name: str, standard=None):
    """Liest ein Feld aus einem Verzeichnis ODER aus einem Objekt (beide Formen kommen vor)."""
    return objekt.get(name, standard) if isinstance(objekt, dict) else getattr(objekt, name, standard)


def _setzen(objekt: Any, name: str, wert):
    """Schreibt ein Feld in ein Verzeichnis oder in ein Objekt - die zweite Haelfte des Zugriffs."""
    if isinstance(objekt, dict):
        objekt[name] = wert
    else:
        setattr(objekt, name, wert)


def forschungsstand(forschungen: Mapping[str, Any]) -> int:
    """Forschungsstufe der Verteidigungsanlagen (NICHT Mauerbau)."""
    eintrag = (forschungen or {}).get('Verteidigungsanlagen', 0)
    if isinstance(eintrag, dict):
        wert = eintrag.get('stufe', eintrag.get('level', 0))
    elif hasattr(eintrag, 'level'):
        wert = eintrag.level
    else:
        wert = eintrag
    try:
        return min(10, max(0, int(wert)))
    except (ValueError, TypeError):
        return 0


def stufe(siedlung: Any, forschungen: Mapping[str, Any]) -> int:
    """Tatsaechlich geschuetzter Ort: ohne Aktivierung bleibt Stufe null."""
    return forschungsstand(forschungen) if bool(_feld(siedlung, 'mauer_besetzt', False)) else 0


def zustand(siedlung: Any) -> float:
    """Mauerzustand eines Ortes in Prozent (100 = unversehrt, 0 = eingerissen)."""
    try:
        wert = float(_feld(siedlung, 'mauer_zustand', 100.0))
    except (TypeError, ValueError):
        wert = 100.0
    return min(100.0, max(0.0, wert))


def kennwerte(siedlung: Any, forschungen: Mapping[str, Any]) -> dict:
    """Liefert den Originalwall-Eintrag samt lokalem Zustand, ohne ihn zu aendern."""
    import gebaeude_wirkung as gw
    nr = stufe(siedlung, forschungen)
    schwelle = gw.wall_schwelle(nr) if nr else {'fusstruppen': None, 'belagerungswaffen': None}
    return {'stufe': nr, 'name': gw.wall_name(nr) if nr else 'Kein Wall',
            'zustand_prozent': zustand(siedlung) if nr else 0.0,
            'fusstruppen': schwelle['fusstruppen'],
            'belagerungswaffen': schwelle['belagerungswaffen']}


def wache_besetzen(siedlung: Any, forschungen: Mapping[str, Any],
                    ortslager: dict, baukosten: Mapping[str, Any]) -> tuple[bool, str]:
    """Einmalige lokale Errichtung; keine neue Einheit und kein Rasterfeld.

    `baukosten` ist der bestehende Eintrag fuer `verteidigungswall` aus
    data/baupreise.json. Die GUI/Spielschicht muss ihn unveraendert uebergeben.
    """
    if bool(_feld(siedlung, 'mauer_besetzt', False)):
        return False, 'Wall ist hier bereits errichtet.'
    if forschungsstand(forschungen) < 1:
        return False, 'Zuerst Verteidigungsanlagen erforschen.'
    kosten = {k: float(v) for k, v in (baukosten or {}).items()
              if k in ('holz', 'stein', 'metall', 'mana', 'nahrung', 'gold', 'wolle', 'leder', 'pferde')
              and isinstance(v, (float, int)) and v > 0}
    if not kosten:
        return False, 'Kein gueltiger Preis hinterlegt; Errichtung gesperrt.'
    fehlend = [f'{k}: {menge - float(ortslager.get(k, 0) or 0):g}'
               for k, menge in kosten.items() if float(ortslager.get(k, 0) or 0) < menge]
    if fehlend:
        return False, 'Im Dorflager fehlen ' + ', '.join(fehlend)
    for k, menge in kosten.items():
        ortslager[k] = float(ortslager.get(k, 0) or 0) - menge
    _setzen(siedlung, 'mauer_besetzt', True)
    _setzen(siedlung, 'mauer_zustand', 100.0)
    return True, 'Wall errichtet; Wache besetzt. Kein Bauplatz verbraucht.'


def rahmen_plan(spalten: int, zeilen: int, zelle: int, rand: int,
                mauerstufe: int, mauerzustand: float = 100.0) -> list[dict]:
    """Zeichenplan fuer Kartenumrandung inkl. Tor, ohne tkinter oder Feldbelegung.

    Jede Form ist eine Linie mit 4 Koordinaten, Farbe und Breite. Das Tor bleibt
    mittig an der Suedseite sichtbar. Nur aktive Wallstufen >=1 zeichnen.
    """
    if not (1 <= int(mauerstufe) <= 10):
        return []
    x1, y1 = rand, rand
    x2, y2 = rand + spalten*zelle, rand + zeilen*zelle
    tor = max(12, int(zelle*0.58))
    mitte = (x1+x2)/2
    # Farblogik nur Darstellungsvorschlag; Original liefert keine Pixelwerte.
    farbe = '#927552' if mauerstufe < 3 else ('#A99C79' if mauerstufe < 6 else '#BEC2C5')
    breite = 4 if mauerstufe < 5 else 7
    zust = min(100.0, max(0.0, float(mauerzustand)))
    if zust < 50:
        farbe = '#80645B'
    kanten = [(x1, y1, x2, y1), (x1, y1, x1, y2), (x2, y1, x2, y2),
              (x1, y2, mitte - tor/2, y2), (mitte + tor/2, y2, x2, y2)]
    return [{'linie': kanten[i], 'farbe': farbe, 'breite': breite, 'teil':
             ('nord', 'west', 'ost', 'sued-links', 'sued-rechts')[i]}
            for i in range(len(kanten))]
