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
        return False, 'Kein gültiger Preis hinterlegt; Errichtung gesperrt.'
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
             ('nord', 'west', 'ost', 'süd-links', 'süd-rechts')[i]}
            for i in range(len(kanten))]


# ---------------------------------------------------------------------------
# S2 (06.11.2026): Mauerreparatur - Preis, Dauer und Ablauf an EINER Stelle.
#
# Vorgabe Daniel (Runde 2, Frage 2): der Preis je Prozentpunkt wird aus dem EINEN belegten
# Wallpreis (16 Holz / 16 Stein fuer Stufe 1) und der Stufe gerechnet, nicht erfunden.
# Ergebnis (docs/S0_TABELLEN_20261107.md, V-1): je Prozentpunkt 16 * Stufe / 100 in Holz UND
# Stein; 0 auf 100 Prozent kostet damit genau den Wallpreis mal Stufe und dauert 10 Spielstunden.
# ---------------------------------------------------------------------------

WALLPREIS_HOLZ = 16.0          # belegter Wallpreis fuer Stufe 1 in Holz (data/baupreise.json)
WALLPREIS_STEIN = 16.0         # belegter Wallpreis fuer Stufe 1 in Stein
SEKUNDEN_JE_PROZENT = 360.0    # 0,1 Spielstunde je Prozentpunkt (1 Spielstunde = 3600 Spielsekunden)


def reparatur_preis(stufe: int, von_prozent: float, bis_prozent: float = 100.0) -> dict:
    """Holz und Stein fuer eine Reparatur von `von_prozent` auf `bis_prozent` (V-1).

    Der Preis waechst linear mit der Wallstufe, weil der Ausbau selbst linear ist
    (`data/baupreise.json` -> regeln.ausbau_linear).
    """
    stufe = max(1, min(10, int(stufe or 0)))                       # Wallstufen gibt es nur 1 bis 10
    fehlt = max(0.0, float(bis_prozent) - float(von_prozent))       # wie viele Prozentpunkte fehlen
    je = WALLPREIS_HOLZ * stufe / 100.0                            # Holz je Prozentpunkt (Stein gleich)
    stein_je = WALLPREIS_STEIN * stufe / 100.0                     # Stein je Prozentpunkt
    return {"holz": je * fehlt, "stein": stein_je * fehlt}


def reparatur_sekunden(von_prozent: float, bis_prozent: float = 100.0) -> float:
    """Dauer einer Reparatur in SPIELSEKUNDEN (1 Prozentpunkt = 360 Spielsekunden)."""
    return max(0.0, float(bis_prozent) - float(von_prozent)) * SEKUNDEN_JE_PROZENT


def reparatur_laeuft(siedlung: Any) -> bool:
    """Laeuft an diesem Ort gerade eine Mauerreparatur?"""
    return float(_feld(siedlung, 'mauer_reparatur_ziel', 0.0) or 0.0) > 0.0


def reparatur_abbrechen(siedlung: Any) -> bool:
    """Bricht eine laufende Reparatur ab (bei einem Angriff) - der Zustand bleibt, wie er ist."""
    if not reparatur_laeuft(siedlung):
        return False
    _setzen(siedlung, 'mauer_reparatur_ziel', 0.0)                 # kein Ziel mehr
    _setzen(siedlung, 'mauer_reparatur_ende', 0.0)                 # kein Endzeitpunkt mehr
    _setzen(siedlung, 'mauer_reparatur_stufe', 0)                  # keine gemerkte Stufe mehr
    return True


def reparatur_pruefen(siedlung: Any, forschungen: Mapping[str, Any], ortslager: dict,
                      forschungsauftraege: Any = None, jetzt: float = 0.0) -> dict:
    """Alle Bedingungen der Reparatur EINZELN - die eine Rechenstelle fuer Kern und Anzeige.

    Rueckgabe:: {"moeglich", "gruende" (Liste), "preis", "ziel", "sekunden", "zustand", "stufe",
                 "naechster_schritt"}
    Ein Grund ist ein fertiger Satz; die Anzeige zeigt sie einzeln, nie als Sammel-Meldung.
    """
    wallstufe = stufe(siedlung, forschungen)                       # Stufe dieses Ortes (0 = kein Wall)
    zust = zustand(siedlung)                                       # Zustand in Prozent, nie negativ
    ergebnis = {"moeglich": False, "gruende": [], "preis": {}, "ziel": 100.0, "sekunden": 0.0,
                "zustand": zust, "stufe": int(wallstufe), "naechster_schritt": ""}
    if not bool(_feld(siedlung, 'mauer_besetzt', False)):
        ergebnis["gruende"].append("Es steht noch kein Wall in diesem Dorf.")
        ergebnis["naechster_schritt"] = "Zuerst Verteidigungsanlagen erforschen und den Wall errichten."
        return ergebnis
    if wallstufe <= 0:
        ergebnis["gruende"].append("Die Wallstufe ist 0.")
        ergebnis["naechster_schritt"] = "Zuerst die Forschung Verteidigungsanlagen auf Stufe 1 bringen."
        return ergebnis
    if reparatur_laeuft(siedlung):
        ergebnis["gruende"].append("Es l\u00e4uft bereits eine Reparatur an dieser Mauer.")
        ergebnis["naechster_schritt"] = "Die laufende Reparatur abwarten."
        return ergebnis
    if zust >= 100.0:
        ergebnis["gruende"].append("Die Mauer ist unbesch\u00e4digt (100 Prozent).")
        ergebnis["naechster_schritt"] = "Nichts zu tun."
        return ergebnis
    if _ausbau_laeuft(forschungsauftraege):
        ergebnis["gruende"].append("Die Mauer wird gerade ausgebaut (Forschung Verteidigungsanlagen l\u00e4uft).")
        ergebnis["naechster_schritt"] = "Den Ausbau abwarten, danach reparieren."
        return ergebnis
    preis = reparatur_preis(wallstufe, zust)                       # Holz und Stein aus V-1
    ergebnis["preis"] = preis
    ergebnis["sekunden"] = reparatur_sekunden(zust)
    for rohstoff, betrag in preis.items():                         # jede fehlende Menge EINZELN
        haben = float((ortslager or {}).get(rohstoff, 0) or 0)
        if haben < betrag:
            ergebnis["gruende"].append("Im Dorflager fehlen %s %s."
                                       % (_zahl(betrag - haben), rohstoff.capitalize()))
    if ergebnis["gruende"]:
        ergebnis["naechster_schritt"] = "Zuerst die fehlenden Rohstoffe im Dorflager auffuellen."
        return ergebnis
    ergebnis["moeglich"] = True
    ergebnis["naechster_schritt"] = "Mauer reparieren (Ziel 100 Prozent)."
    return ergebnis


def reparatur_starten(siedlung: Any, forschungen: Mapping[str, Any], ortslager: dict,
                      jetzt: float, forschungsauftraege: Any = None) -> tuple:
    """Bucht die Reparatur ATOMAR und setzt Start, Ziel und Endzeitpunkt.

    Entweder alle Posten werden gebucht oder keiner - deshalb erst pruefen, dann buchen.
    Rueckgabe:: (bool, Meldung)
    """
    pruefung = reparatur_pruefen(siedlung, forschungen, ortslager, forschungsauftraege, jetzt)
    if not pruefung["moeglich"]:
        return False, " ".join(pruefung["gruende"])
    preis = pruefung["preis"]
    for rohstoff, betrag in preis.items():                         # atomar: geprueft ist schon
        ortslager[rohstoff] = float(ortslager.get(rohstoff, 0) or 0) - float(betrag)
    _setzen(siedlung, 'mauer_reparatur_start_zustand', float(pruefung["zustand"]))
    _setzen(siedlung, 'mauer_reparatur_start_zeit', float(jetzt))
    _setzen(siedlung, 'mauer_reparatur_ziel', float(pruefung["ziel"]))      # Ziel: volle Mauer
    _setzen(siedlung, 'mauer_reparatur_ende', float(jetzt) + float(pruefung["sekunden"]))
    _setzen(siedlung, 'mauer_reparatur_stufe', int(pruefung["stufe"]))      # Stufe merken
    return True, ("Reparatur gestartet: Ziel 100 Prozent in %d Spielsekunden (%s Holz, %s Stein)."
                  % (int(pruefung["sekunden"]), _zahl(preis["holz"]), _zahl(preis["stein"])))


def reparatur_tick(siedlung: Any, jetzt: float, forschungen: Mapping[str, Any]) -> bool:
    """Laesst den Zustand stueckweise steigen; gibt True zurueck, wenn sie fertig wurde.

    Der Zustand folgt der Uhr: Anteil der verstrichenen Zeit an der Gesamtdauer. Aendert sich die
    Wallstufe waehrend der Reparatur (Forschung), bricht sie ab - der bezahlte Preis passt dann
    nicht mehr zur Stufe.
    """
    if not reparatur_laeuft(siedlung):
        return False
    gemerkte_stufe = int(_feld(siedlung, 'mauer_reparatur_stufe', 0) or 0)
    if stufe(siedlung, forschungen) != gemerkte_stufe:              # Stufe hat sich geaendert: abbrechen
        reparatur_abbrechen(siedlung)
        return False
    ziel = float(_feld(siedlung, 'mauer_reparatur_ziel', 0.0) or 0.0)
    start_zustand = float(_feld(siedlung, 'mauer_reparatur_start_zustand', 0.0) or 0.0)
    start_zeit = float(_feld(siedlung, 'mauer_reparatur_start_zeit', 0.0) or 0.0)
    ende = float(_feld(siedlung, 'mauer_reparatur_ende', 0.0) or 0.0)
    dauer = reparatur_sekunden(start_zustand, ziel)
    anteil = 1.0 if dauer <= 0 else (float(jetzt) - start_zeit) / dauer
    anteil = max(0.0, min(1.0, anteil))
    neu = start_zustand + (ziel - start_zustand) * anteil
    _setzen(siedlung, 'mauer_zustand', min(100.0, max(0.0, neu)))
    if dauer <= 0 or float(jetzt) >= ende:                          # Zeit ist um: fertig
        _setzen(siedlung, 'mauer_zustand', ziel)
        reparatur_abbrechen(siedlung)
        return True
    return False


def _ausbau_laeuft(forschungsauftraege: Any) -> bool:
    """Laeuft irgendwo ein Forschungsauftrag Verteidigungsanlagen? (Sperre Reparatur/Ausbau.)"""
    if not forschungsauftraege:
        return False
    eintraege = forschungsauftraege.values() if isinstance(forschungsauftraege, dict) else forschungsauftraege
    for eintrag in eintraege or []:
        if not isinstance(eintrag, dict):
            continue
        if str(eintrag.get('gebiet') or eintrag.get('forschung') or '') == 'Verteidigungsanlagen':
            return True
    return False


def _zahl(wert: Any) -> str:
    """Eine Menge lesbar machen: ganze Zahlen ohne Nachkommastellen, sonst eine Stelle."""
    try:
        zahl = float(wert)
    except (TypeError, ValueError):
        return str(wert)
    if abs(zahl - round(zahl)) < 1e-9:
        return "%d" % int(round(zahl))
    return ("%.1f" % zahl).replace(".", ",")
