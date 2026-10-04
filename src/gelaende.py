"""
Gelaende und Siedlungskarte fuer das Nebelseetal-Remake.

Belegt (Handbuch 2009, S. 9-11):
  * sieben Gelaendearten: Grasland, Steppe, Wald, Huegel, Berg, Nebelsee, Sumpf
  * Sumpf ist nicht bebaubar
  * Erträge haengen vom Gelaende ab (Holzfäller Wald 4/Steppe 2, Steinmetz Berg 4/Huegel 2,
    Erzmine Berg 3/Huegel 1,5, Goldmine Berg 3/Huegel 1,5, Farm Grasland 4/Steppe 2,
    Schafszucht/Rinderfarm/Pferdezucht Grasland 3/Steppe 1,5, Jaeger Wald Nahrung 2 + Leder 2,
    Nebelsee-Steppe 1 + 1, Tempel Nebelsee 5 / sonst 1)
  * beim Bauen zeigt das Spiel die Eignung des Gelaendes an

NICHT belegt (als Vorschlag gekennzeichnet, in data/gelaende.json aenderbar):
  * Kartenmass (8x5 = 40 Bauplaetze) und die Haeufigkeit der Gelaendearten
  * wo Gebaeude OHNE Gelaendebezug (Schmiede, Haus, Lager, Bibliothek) stehen duerfen
"""
from __future__ import annotations

import json
import random
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
DATEN = WURZEL / "data"


def _lade(name: str) -> dict:
    return json.loads((DATEN / name).read_text(encoding="utf-8"))


_GELAENDE = _lade("gelaende.json")
_GEBAEUDE = {g["id"]: g for g in _lade("buildings.json")["gebaeude"]}

# Anzeigenamen und Kennungen
ARTEN = {a["id"]: a for a in _GELAENDE["gelaendearten"]}
NACH_NAME = {a["name"]: a["id"] for a in _GELAENDE["gelaendearten"]}
GELAENDEARTEN = [a["id"] for a in _GELAENDE["gelaendearten"]]
SUMPF = "sumpf"

# Kartentypen mit verschiedenen Vorteilen (Produktentscheidung Daniel, 04.10.2026).
KARTENTYPEN = {t["id"]: t for t in _GELAENDE["kartentypen"]["listen"]}
KARTENTYP_REIHENFOLGE = [t["id"] for t in _GELAENDE["kartentypen"]["listen"]]


def karten_typ(seed) -> dict:
    """Waehlt den Kartentyp zu einer Saat (gleiche Saat -> gleicher Typ, wichtig fuer Speichern)."""
    rng = random.Random(f"typ-{seed}")
    liste = _GELAENDE["kartentypen"]["listen"]
    summe = sum(t["haeufigkeit"] for t in liste)
    r = rng.uniform(0, summe)
    k = 0.0
    for t in liste:
        k += t["haeufigkeit"]
        if r <= k:
            return t
    return liste[-1]


def name(art_id: str) -> str:
    """Anzeigename einer Gelaendeart."""
    return ARTEN[art_id]["name"]


def _norm(s: str) -> str:
    """Vergleichsform eines Namens: klein, ohne Umlaute (Spiel schreibt 'holzfäller', Daten 'holzfaeller')."""
    return (str(s).lower().replace("ä", "ae").replace("ö", "oe")
            .replace("ü", "ue").replace("ß", "ss"))


def finde_gebaeude(name_oder_id: str):
    """Findet die Kennung eines Gebaeudes — akzeptiert Kennung UND Anzeigename, mit oder ohne Umlaut."""
    if name_oder_id in _GEBAEUDE:
        return name_oder_id
    n = _norm(name_oder_id)
    for gid, geb in _GEBAEUDE.items():
        if _norm(gid) == n or _norm(geb.get("name", "")) == n:
            return gid
    return None


def ist_bebaubar(art_id: str) -> bool:
    return bool(ARTEN[art_id]["bebaubar"])


def farbe(art_id: str) -> str:
    return ARTEN[art_id]["farbe"]


def alle_gebaeude() -> dict:
    """Alle Gebaeude aus data/buildings.json als {kennung: eintrag}."""
    return dict(_GEBAEUDE)


def gebaeude_name(kennung: str) -> str:
    """Anzeigename eines Gebaeudes (akzeptiert Kennung oder Name)."""
    gid = finde_gebaeude(kennung)
    return _GEBAEUDE[gid]["name"] if gid else str(kennung)


# --------------------------------------------------------------------------
# Erträge
# --------------------------------------------------------------------------

def ertrag_pro_stunde(gebaeude_id: str, gelaende: str):
    """
    Ertrag eines Gebaeudes auf einem Gelaende.

    Rueckgabe: Zahl (ein Rohstoff), dict {Rohstoff: Zahl} (mehrere, z. B. Jaeger)
               oder None, wenn das Gebaeude dort nicht gebaut werden kann.
    `gelaende` darf die Kennung ('wald') oder der Anzeigename ('Wald') sein.
    """
    art = NACH_NAME.get(gelaende, gelaende)
    anzeige = ARTEN[art]["name"] if art in ARTEN else gelaende
    geb = _GEBAEUDE.get(finde_gebaeude(gebaeude_id))
    if geb is None:
        return None
    tabelle = geb.get("ertrag_pro_stunde")
    if not tabelle:                      # Gebaeude ohne Gelaendebezug
        return None
    if anzeige in tabelle:
        return tabelle[anzeige]
    for schluessel, wert in tabelle.items():
        if schluessel.startswith("alle") and anzeige != "Sumpf":
            return wert
    return None


def bau_moeglich(gebaeude_id: str, gelaende: str) -> tuple:
    """
    Darf dieses Gebaeude auf diesem Gelaende stehen?

    Rueckgabe: (ja/nein, Begruendung) — die Begruendung ist fuer die Anzeige gedacht,
    damit der Spieler sieht, WARUM es nicht geht (Handbuch: die Eignung wird angezeigt).
    """
    art = NACH_NAME.get(gelaende, gelaende)
    if art not in ARTEN:
        return False, f"Unbekanntes Gelände: {gelaende}"
    geb = _GEBAEUDE.get(finde_gebaeude(gebaeude_id))
    if geb is None:
        return False, f"Unbekanntes Gebäude: {gebaeude_id}"
    gname = ARTEN[art]["name"]

    if not ARTEN[art]["bebaubar"]:
        return False, f"{gname} kann nicht bebaut werden."

    # Belegte Standortregel (W4b-5): manche Gebaeude duerfen nur auf bestimmten Gelaendearten
    # stehen — z. B. die Bibliothek nur auf Grasland, Steppe oder Nebelsee. Steht als 'nur_auf'
    # in data/buildings.json; fehlt der Eintrag, gilt die Regel nicht.
    nur_auf = geb.get("nur_auf")
    if nur_auf:
        erlaubte = [NACH_NAME.get(a, a) for a in nur_auf]
        if art not in erlaubte:
            namen = ", ".join(ARTEN[a]["name"] for a in erlaubte if a in ARTEN)
            return False, f"{geb['name']} darf nur auf {namen} stehen."
        return True, f"{geb['name']} auf {gname} (belegte Standortregel)."

    ertrag = ertrag_pro_stunde(gebaeude_id, art)
    if ertrag is not None:
        if isinstance(ertrag, dict):
            teile = ", ".join(f"{w} {z}/Stunde" for w, z in ertrag.items())
        else:
            teile = f"{ertrag} {geb.get('rohstoff') or ''}/Stunde".strip()
        return True, f"{geb['name']} auf {gname}: {teile}"

    if not geb.get("ertrag_pro_stunde"):
        # ANNAHME: Gebaeude ohne Gelaendebezug (Schmiede, Bogenbauer, Naehstube, Bibliothek,
        # Haus, Lager, Wall, Ausbildungsstaetten) stehen auf jedem bebaubaren Gelaende.
        # Das Handbuch sagt dazu nichts.
        return True, f"{geb['name']} braucht kein bestimmtes Gelände ({gname} ist bebaubar)."

    return False, f"{geb['name']} liefert auf {gname} nichts."


# --------------------------------------------------------------------------
# Siedlungskarte
# --------------------------------------------------------------------------

def siedlungskarte_erzeugen(seed, mass: dict = None, typ_id: str = None) -> dict:
    """
    Erzeugt die Gelaendekarte einer Siedlung.

    Gleicher seed ergibt immer dieselbe Karte (wichtig fuer Speichern/Laden) — samt Kartentyp.
    Jeder Kartentyp hat eigene Gewichte und damit eigene Vorteile (data/gelaende.json).
    Die Karte erfuellt die Mindestbesatz-Regel, damit jede Siedlung spielbar ist
    (Holz, Stein, Nahrung, Nebelsee fuer den Tempel).
    """
    rng = random.Random(seed)
    mass = mass or _GELAENDE["kartenmass"]
    regeln = _GELAENDE["regeln"]
    spalten, zeilen = mass["spalten"], mass["zeilen"]
    plaetze = spalten * zeilen

    typ = KARTENTYPEN[typ_id] if typ_id else karten_typ(seed)
    gewichte = typ["gewichte"]
    erlaubt = [a for a in _GELAENDE["gelaendearten"]]

    def ziehen(aus: list) -> str:
        s = sum(gewichte.get(a["id"], a["haeufigkeit"]) for a in aus)
        r = rng.uniform(0, s)
        k = 0.0
        for a in aus:
            k += gewichte.get(a["id"], a["haeufigkeit"])
            if r <= k:
                return a["id"]
        return aus[-1]["id"]

    raster = [ziehen(erlaubt) for _ in range(plaetze)]

    # Mindestbesatz sicherstellen: fehlende Gelaendearten auf zufaelligen Feldern erzwingen
    def haeufigkeit(art_id: str) -> int:
        return raster.count(art_id)

    def ersetzen(art_id: str, wieviele: int) -> None:
        for _ in range(wieviele):
            # bevorzugt ein Feld ersetzen, das selbst nicht zu einer knappen Art gehoert
            for _versuch in range(60):
                i = rng.randrange(plaetze)
                alt = raster[i]
                mindest = regeln["mindestbesatz"]
                knapp = [k for k, n in mindest.items()
                         if not k.startswith("_") and haeufigkeit(k) <= n]
                if alt not in knapp:
                    raster[i] = art_id
                    break
            else:
                raster[rng.randrange(plaetze)] = art_id

    for art_id, mindest in regeln["mindestbesatz"].items():
        if art_id.startswith("_"):
            continue
        fehlt = mindest - haeufigkeit(art_id)
        if fehlt > 0:
            ersetzen(art_id, fehlt)

    # Sumpf deckeln, falls er die Obergrenze reisst
    grenze = regeln["sumpf_hoechstens"]
    while haeufigkeit(SUMPF) > grenze:
        i = raster.index(SUMPF)
        raster[i] = ziehen([a for a in erlaubt if a["id"] != SUMPF])

    zeilen_liste = [raster[i * spalten:(i + 1) * spalten] for i in range(zeilen)]
    zaehlung = {a: raster.count(a) for a in GELAENDEARTEN}
    return {
        "seed": seed,
        "spalten": spalten,
        "zeilen": zeilen,
        "bauplaetze": plaetze,
        "raster": raster,
        "zeilen_raster": zeilen_liste,
        "zaehlung": zaehlung,
        "typ": typ["id"],
        "typ_name": typ["name"],
        "vorteil": typ["vorteil"],
        "beschreibung": typ["beschreibung"],
        "profil": karte_profil(zaehlung),
    }


def karte_profil(zaehlung: dict) -> dict:
    """
    Theoretischer Höchstertrag je Rohstoff und Stunde, wenn jedes Feld mit dem besten
    passenden Gebäude bebaut wird. Damit sieht man den Vorteil einer Karte in Zahlen.
    """
    beste: dict = {}
    for geb in _GEBAEUDE.values():
        tabelle = geb.get("ertrag_pro_stunde")
        if not tabelle:
            continue
        # Geländeart -> Ertrag. Erst die Regel 'alle Gelände außer Sumpf' als Grundwert,
        # DANN die ausdrücklich genannten Geländearten — sie haben Vorrang (Tempel:
        # Nebelsee 5, sonst 1). Die Reihenfolge ist wichtig, sonst überschreibt der
        # Grundwert den Sonderfall.
        je_art = {}
        for schluessel, wert in tabelle.items():
            if schluessel.startswith("alle"):
                for a in _GELAENDE["gelaendearten"]:
                    if a["id"] != SUMPF:
                        je_art[a["name"]] = wert
        for schluessel, wert in tabelle.items():
            if not schluessel.startswith("alle"):
                je_art[schluessel] = wert
        for anzeige, wert in je_art.items():
            art = NACH_NAME.get(anzeige)
            if art is None:
                continue
            if isinstance(wert, dict):
                for roh, zahl in wert.items():
                    beste.setdefault(_norm(roh), {})[art] = max(
                        beste.get(_norm(roh), {}).get(art, 0), zahl)
            else:
                roh = _norm(geb.get("rohstoff") or "")
                if not roh:
                    continue
                beste.setdefault(roh, {})[art] = max(beste.get(roh, {}).get(art, 0), wert)
    return {roh: round(sum(zaehlung.get(art, 0) * zahl for art, zahl in je_art.items()), 1)
            for roh, je_art in beste.items()}


def karte_beschreiben(karte: dict) -> str:
    """Kurze Textfassung der Karte (fuer Berichte und Pruefungen)."""
    teile = [f"{ARTEN[a]['name']}: {n}" for a, n in karte["zaehlung"].items() if n]
    return (f"{karte['typ_name']} {karte['spalten']}x{karte['zeilen']} "
            f"({karte['bauplaetze']} Plätze, Saat {karte['seed']}): " + ", ".join(teile))


def karte_als_text(karte: dict) -> str:
    """Die Karte als lesbares Raster (Kuerzel je Feld)."""
    kuerzel = {"grasland": "Gr", "steppe": "St", "wald": "Wa", "huegel": "Hü",
               "berg": "Be", "nebelsee": "Ns", "sumpf": "Su"}
    return "\n".join(" ".join(kuerzel[a] for a in zeile) for zeile in karte["zeilen_raster"])
