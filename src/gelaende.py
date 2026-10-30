"""
Gelaende und Siedlungskarte fuer das Nebelseetal-Remake.

Belegt (Handbuch 2009, S. 9-11):
  * sieben Gelaendearten: Grasland, Steppe, Wald, Huegel, Berg, Nebelsee, Sumpf
  * Sumpf ist nicht bebaubar
  * Erträge haengen vom Gelaende ab (Holzfäller Wald 4/Steppe 2, Steinmetz Berg 4/Huegel 2,
    Erzmine Berg 3/Huegel 1,5, Goldmine Berg 3/Huegel 1,5, Farm Grasland 4/Steppe 2,
    Schafszucht/Rinderfarm/Pferdezucht Grasland 3/Steppe 1,5, Jaeger Wald Nahrung 2 + Leder 2,
    Nebelsee-Steppe 1 + 1, Tempel Nebelsee 8 / sonst 2)
  * beim Bauen zeigt das Spiel die Eignung des Gelaendes an

NICHT belegt (als Vorschlag gekennzeichnet, in data/gelaende.json aenderbar):
  * Historische Generator-Kartenmass (8x7 = 56 Felder, 40 bebaubar; Entscheidung 05.10.2026);
    NUR fuer Legacy-Kompatibilitaet. Neue Karten aus `originalkarten.py` sind 10x10
    (Originalsammlung des Nutzers vom 28.10.2026) und haben individuelle Baufeldzahlen.
  * wo Gebaeude OHNE Gelaendebezug (Schmiede, Haus, Lager, Bibliothek) stehen duerfen
"""
from __future__ import annotations

import json
from pathlib import Path

import spieldaten

# Wurzel ueber EINE Stelle (spieldaten.projektwurzel) — sie findet die Datendateien auch in der
# fertigen EXE, wo `__file__` nicht auf den entpackten Ordner zeigt.
WURZEL = Path(spieldaten.projektwurzel())
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

# Neue Siedlungen nutzen ausschliesslich den verifizierbaren Originalkarten-Katalog.
# Die alten 8x7-Kartentypen und deren Zufallsgenerator sind im Archiv.

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
    """Kompatibilitaets-Einstieg fuer Originalkarten; NIEMALS 8x7 generieren.

    Ueberholte typ_id/mass-Aufrufe muessen umgestellt werden: Ein alter
    Kartentyp darf nicht unbemerkt auf eine erfundene Bildkarte abgebildet werden.
    """
    import originalkarten
    if mass is not None or typ_id is not None:
        raise ValueError("8x7-Altparameter nicht erlaubt: Originalkarte per ID waehlen")
    return originalkarten.startkarte(seed, "spieler")


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
    felder = karte.get("felder") or karte["spalten"] * karte["zeilen"]
    return (f"{karte['typ_name']} {karte['spalten']}x{karte['zeilen']} "
            f"({karte['bauplaetze']} von {felder} Feldern bebaubar, Saat {karte['seed']}): "
            + ", ".join(teile))


def karte_als_text(karte: dict) -> str:
    """Die Karte als lesbares Raster (Kuerzel je Feld)."""
    kuerzel = {"grasland": "Gr", "steppe": "St", "wald": "Wa", "huegel": "Hü",
               "berg": "Be", "nebelsee": "Ns", "sumpf": "Su"}
    return "\n".join(" ".join(kuerzel[a] for a in zeile) for zeile in karte["zeilen_raster"])
