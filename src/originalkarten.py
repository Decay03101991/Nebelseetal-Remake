"""Original-Kartenkatalog Nebelseetal, 127 archivierte Grafiken in 3 Qualitaetsgruppen.

Der Katalog enthaelt sowohl geschriebene Quellzahlen als auch das automatisch aus
Originalbildern abgeleitete 10x10-Spielraster. Der spaetere Spielbetrieb verwendet
nur das Raster; Quellwerte bleiben zur Kontrolle getrennt (nicht als Ressourcenbonus).
Erstellt/integriert: ChatGPT, externer Entwicklungsagent, 28.10.2026.
"""
from __future__ import annotations

from functools import lru_cache
import hashlib
import json
import random
from pathlib import Path

import spieldaten

KATALOG_DATEI = "data/originalkarten/katalog.json"
START_ID = "original-036"  # Singleplayer-Auswahl, keine Handbuchvorgabe.

@lru_cache(maxsize=1)
def _katalog():
    pfad = Path(spieldaten.projektwurzel()) / KATALOG_DATEI
    daten = json.loads(pfad.read_text(encoding="utf-8"))
    if daten.get("mass") != {"spalten": 10, "zeilen": 10}:
        raise ValueError("Originalkarten-Katalog hat kein 10x10-Raster.")
    return daten

@lru_cache(maxsize=1)
def _index():
    return {e["id"]: e for e in _katalog()["karten"]}

def alle(kategorie=None):
    """Metadaten aller Karten; grafische Originalbilder liegen unter `assets/karten/original`."""
    return [e for e in _katalog()["karten"] if kategorie is None or e["kategorie"] == kategorie]

def kennungen():
    return list(_index())

def daten(kennung):
    """Quellattribute EINER Karte, ohne Veraenderung."""
    return _index()[kennung]

def karte(kennung, seed=None):
    """Neues spielbares 10x10-Raster aus einer originalen Kartengrafik.

    `seed` bleibt nur aus Kompatibilitaetsgruenden im Rueckgabeformat; die
    ORIGINALFELDER werden dabei niemals gemischt oder neu gewuerfelt.
    """
    import gelaende
    eintrag = _index()[kennung]
    raster = list(eintrag["spielraster"])
    if len(raster) != 100 or any(x not in gelaende.GELAENDEARTEN for x in raster):
        raise ValueError("Originalkarte unvollstaendig: " + kennung)
    zaehlung = {a: raster.count(a) for a in gelaende.GELAENDEARTEN}
    result = {"seed": str(seed if seed is not None else kennung), "spalten": 10,
              "zeilen": 10, "felder": 100,
              "bauplaetze": 100 - zaehlung["sumpf"],
              "raster": raster, "zeilen_raster": [raster[i:i+10] for i in range(0,100,10)],
              "zaehlung": zaehlung, "typ": eintrag["id"],
              "typ_name": eintrag["name"],
              "vorteil": "Originalkarte (%s): Goldwert %s, Lederwert %s / h, ohne Forschung" %
                 (eintrag["kategorie"],eintrag["original_attribute"]["goldwert"],
                  eintrag["original_attribute"]["gras_steppenwert"]),
              "beschreibung": "Originalkarte aus Kartensammlung von Kathrin Hildebrand",
              "profil": gelaende.karte_profil(zaehlung),
              "originalkarte_id": eintrag["id"],
              "originalkarte_bild": eintrag["originalbild"],
              "originalkarte_quelle": eintrag["quelle"]["website"],
              "originalkarte_pruefung_offen": bool(eintrag["raster_nachweis"]["manuelle_sichtpruefung_ausstehend"])}
    return result

def startkarte(seed, eigentuemer):
    """Spieler: feste versorgbare Karte; Bots: deterministische Auswahl anderer Originale."""
    if eigentuemer == "spieler":
        ident = START_ID
    else:
        kandidaten = ["original-005", "original-015", "original-019", "original-030",
                      "original-034", "original-036", "original-037", "original-051", "original-052"]
        n = int(hashlib.sha256(f"{seed}:{eigentuemer}".encode("utf-8")).hexdigest()[:12],16)
        ident = kandidaten[n % len(kandidaten)]
    return karte(ident, seed=f"{seed}:start:{eigentuemer}")

def vorrat(seed):
    """Alle dokumentierten Originalkarten mit reproduzierbaren eindeutigen IDs.

    Die private Spieler-Startkarte bleibt bewusst ausserhalb des Kolonievorrats.
    """
    return {e["id"]: {"karte": karte(e["id"], seed=f"{seed}:{e['id']}"), "besitzer": None}
            for e in alle() if e["id"] != START_ID}

def ziehchancen(vergeben=()):
    """Reine Information zur *optionalen* gleichverteilten Zufallsziehung.

    Die Gründungsmaske erlaubt bislang die FREIE Kartenwahl; dabei gibt es
    keine Zufallswahrscheinlichkeit. Historische Gruppen sind nur
    Dokumentation, keine Gewichte in der Ziehung. Die feste Spieler-Startkarte
    gehoert nicht zum Kolonievorrat.
    """
    vergeben = set(vergeben) | {START_ID}
    freie = [e for e in alle() if e["id"] not in vergeben]
    n = len(freie)
    gruppen = {k: 0 for k in ("beste", "mittlere", "schlechte")}
    for e in freie:
        gruppen[e["kategorie"]] += 1
    return {"modus": "nur_optionale_zufallsziehung_nicht_freie_auswahl",
            "anzahl_frei": n,
            "wahrscheinlichkeit_pro_karte": 1.0 / n if n else 0.0,
            "gruppen": {k: {"anzahl": v, "wahrscheinlichkeit": v / n if n else 0.0}
                        for k, v in gruppen.items()}}


def zufalls_originalkarte(seed, vergeben=()):
    """Gleichverteilte, reproduzierbare Ziehung aus dem *freien* Originalvorrat.

    Der Zufallsweg ist optional. Die eigentliche Gründungsmaske nutzt weiterhin
    ihre vom Nutzer schon festgelegte manuelle Auswahl. Gruppenqualitäten
    beeinflussen die Ziehchance nicht. START_ID ist immer reserviert.
    """
    vergeben = set(vergeben) | {START_ID}
    kandidaten = [kennung for kennung in kennungen() if kennung not in vergeben]
    if not kandidaten:
        raise ValueError("Alle Originalkarten bereits vergeben.")
    # Python Random.randrange verwendet keine modulo-Verzerrung; mit festem
    # Seed bleibt die Ziehung reproduzierbar, z.B. nach Laden eines Spielstands.
    rng = random.Random("nebelseetal-originalkarten:" + str(seed))
    return karte(kandidaten[rng.randrange(len(kandidaten))], seed=seed)
