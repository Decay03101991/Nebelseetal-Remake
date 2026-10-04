"""
Nebelseetal Remake - Waren und Werkstaetten (Paket W3, 04.10.2026).

Die 17 Waren des Originals werden in drei Werkstaetten gefertigt:

  Schmiede   -> Waffen und Ruestungen (Messer ... Magischer Paladinharnisch), 8 Waren
  Bogenbauer -> Fernwaffen (Kurzbogen ... Armbrust), 4 Waren
  Naehstube  -> Stoff- und Fellkleidung (Wollumhang ... Fellruestung), 5 Waren

BELEGT ist (Handbuch 2009, Seite 13/14; data/buildings.json; data/items.json):
  * welche Ware in welcher Werkstatt entsteht,
  * dass Waren ueber WARTSCHLANGEN laufen,
  * dass mehrere GLEICHE Werkstaetten nebeneinander fertigen - das Handbuchbeispiel
    lautet: 10 Schwerter a 20 Minuten mit ZWEI Schmieden = 100 statt 200 Minuten,
  * dass der Warenbestand im Lager geprueft wird.

NICHT belegt und darum bewusst NICHT erfunden:
  * die Fertigungsdauer jeder anderen Ware - das Handbuch nennt die 20 Minuten NUR
    fuer das Schwert-Beispiel. `dauer_sekunden` gibt fuer alle anderen Waren None
    zurueck; `dauer_belegt` ist nur fuer Schwert True.
  * der Stufen-Einfluss auf die Fertigungsdauer der Werkstaetten. Er ist hier als
    VORSCHLAG (+10 % Tempo je Stufe, wie die belegten +10 %-Stufenregeln des Spiels)
    umgesetzt und in den Meldungen als solcher gekennzeichnet.

Das Modul zeichnet nichts, aendert keine fremde Datei und nutzt nur die
Standardbibliothek plus die Projektdaten (`spieldaten`, `gelaende`).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import gelaende
import spieldaten

# Die drei Werkstatt-Kennungen - so heissen die Werkstaetten in data/buildings.json.
WERKSTAETTEN = ("schmiede", "bogenbauer", "naehstube")

# Die einzige BELEGTE Fertigungsdauer: das Handbuchbeispiel nennt 20 Minuten fuer ein Schwert.
BELEGTE_DAUER_SEKUNDEN: Dict[str, float] = {"Schwert": 20 * 60}

# VORSCHLAG (nicht belegt): hoehere Werkstattstufe macht schneller, +10 % Tempo je Stufe
# ueber Stufe 1 hinaus. Grundlage ist die belegte Stufenlogik des Spiels (z. B. Heilkunde
# +10 % je Stufe). In `data/...` gibt es dafuer keinen Wert; hier ist er ehrlich markiert.
STUFE_TEMPO_PROZENT = 10

# Belegte Zweitnamen aus der Quellenlage: die Auswertung fuehrt das Gebaeude als "Bogner",
# das Handbuch 2009 als "Bogenbauer" (data/buildings.json, Anmerkung). Beide sind gueltig.
WERKSTATT_ALIASE: Dict[str, str] = {
    "Bogner": "bogenbauer",
    "bogenbauer": "bogenbauer",
    "schmiede": "schmiede",
    "naehstube": "naehstube",
}


# --------------------------------------------------------------------------
# 1. Die drei Werkstaetten aus data/buildings.json
# --------------------------------------------------------------------------

def _werkstatt_eintraege() -> List[Dict[str, Any]]:
    return [g for g in spieldaten.gebaeude()
            if g.get("kategorie") == "Werkstatt" and g.get("id")]


def werkstaetten() -> Dict[str, str]:
    """{kennung: Anzeigename} der drei Werkstaetten - direkt aus data/buildings.json."""
    return {g["id"]: g.get("name") or g["id"] for g in _werkstatt_eintraege()}


def _namen_nach_kennung() -> Dict[str, str]:
    """{vergleichsname: kennung} - Anzeigename und belegte Aliase (Bogner)."""
    zu: Dict[str, str] = {}
    for kennung, anzeige in werkstaetten().items():
        zu[_vergleich(anzeige)] = kennung
    for name, kennung in WERKSTATT_ALIASE.items():
        zu.setdefault(_vergleich(name), kennung)
    return zu


def _vergleich(name: str) -> str:
    """Vergleichsform eines Werkstattnamens: klein, ohne Umlaute (wie gelaende._norm)."""
    return gelaende._norm(name)


def _werkstatt_kennung(typ: str) -> Optional[str]:
    """Eine Werkstattkennung aus Kennung ODER Anzeigename ODER belegtem Zweitnamen (Bogner)."""
    if not typ:
        return None
    kennung = gelaende.finde_gebaeude(typ)
    if kennung in werkstaetten():
        return kennung
    return _namen_nach_kennung().get(_vergleich(typ))


# --------------------------------------------------------------------------
# 2. Waren je Werkstatt (aus data/items.json) und Rueckrichtung
# --------------------------------------------------------------------------

def _waren() -> Dict[str, Dict[str, Any]]:
    return spieldaten.waren()


def waren_der_werkstatt(typ: str) -> List[str]:
    """Alle Waren einer Werkstatt in der Reihenfolge von data/items.json."""
    kennung = _werkstatt_kennung(typ)
    if not kennung:
        return []
    treffer: List[str] = []
    for ware, eintrag in _waren().items():
        name = eintrag.get("werkstatt") or ""
        ziel = _namen_nach_kennung().get(_vergleich(name))
        if ziel == kennung:
            treffer.append(ware)
    return treffer


def werkstatt_fuer(ware: str) -> Optional[str]:
    """Die Kennung der Werkstatt einer Ware - None, wenn die Ware zu keiner Werkstatt gehoert."""
    if not ware:
        return None
    eintrag = _waren().get(ware)
    if not eintrag:
        return None
    name = eintrag.get("werkstatt") or ""
    return _namen_nach_kennung().get(_vergleich(name))


# --------------------------------------------------------------------------
# 3. Dauer - nur wo belegt, sonst ehrlich None
# --------------------------------------------------------------------------

def _stufe_wert(stufe: Any) -> int:
    try:
        s = int(stufe)
    except (TypeError, ValueError):
        s = 1
    return max(1, s)


def _stufe_faktor(stufe: int) -> float:
    """Tempo-Faktor der Werkstattstufe (VORSCHLAG, siehe Modulkopf)."""
    return 1.0 + STUFE_TEMPO_PROZENT / 100.0 * (_stufe_wert(stufe) - 1)


def dauer_sekunden(ware: str, stufe: int = 1) -> Optional[float]:
    """Fertigungsdauer in Sekunden - None, wenn das Handbuch keine Dauer nennt.

    Belegt ist nur das Schwert-Beispiel mit 20 Minuten (1200 s). Fuer alle anderen Waren
    wird NICHTS geschaetzt. Hoehere Stufe verkuerzt die belegte Grunddauer (VORSCHLAG).
    """
    basis = BELEGTE_DAUER_SEKUNDEN.get(ware)
    if basis is None:
        return None
    return round(basis / _stufe_faktor(stufe), 3)


def dauer_belegt(ware: str) -> bool:
    """True nur fuer Waren mit BELEGTER Dauer - das ist allein das Schwert (20 Minuten)."""
    return ware in BELEGTE_DAUER_SEKUNDEN


# --------------------------------------------------------------------------
# 4. Warteschlange: n gleiche Werkstaetten fertigen n Waren gleichzeitig
# --------------------------------------------------------------------------

def kapazitaet(anzahl_werkstaetten: int) -> int:
    """Wie viele Waren gleichzeitig fertigen - 1 Platz je Werkstatt."""
    try:
        n = int(anzahl_werkstaetten)
    except (TypeError, ValueError):
        return 0
    return max(0, n)


def neue_warteschlange(typ: str, anzahl_werkstaetten: int) -> Dict[str, Any]:
    """Ein leerer Auftragsstapel einer Werkstatt mit n parallelen Plaetzen."""
    kennung = _werkstatt_kennung(typ) or typ
    try:
        anzahl = int(anzahl_werkstaetten)
    except (TypeError, ValueError):
        anzahl = 0
    return {
        "typ": kennung,
        "werkstatt": werkstaetten().get(kennung, kennung),
        "werkstaetten": anzahl,
        "kapazitaet": kapazitaet(anzahl),
        "auftraege": [],
        "einheiten": [],
        "_basis": None,
        "_uhr": None,
    }


def einreihen(schlange: Dict[str, Any], ware: str,
              anzahl: int, stufe: int = 1) -> Tuple[bool, str]:
    """Eine Ware in die Warteschlange stellen. (ok, Meldung)."""
    if not isinstance(schlange, dict) or "einheiten" not in schlange:
        return False, "Keine gueltige Warteschlange uebergeben."
    if ware not in _waren():
        return False, f"'{ware}' ist keine bekannte Ware."
    ziel = werkstatt_fuer(ware)
    if ziel is None:
        return False, f"'{ware}' gehoert zu keiner Werkstatt."
    if ziel != schlange.get("typ"):
        return False, (f"'{ware}' gehoert nicht in die Werkstatt "
                       f"{schlange.get('werkstatt')}.")
    try:
        menge = int(anzahl)
    except (TypeError, ValueError):
        return False, "Die Anzahl muss eine ganze Zahl sein."
    if menge <= 0:
        return False, "Die Anzahl muss groesser als 0 sein."

    s = _stufe_wert(stufe)
    dauer = dauer_sekunden(ware, s)
    ab = schlange.get("_uhr")
    for _ in range(menge):
        schlange["einheiten"].append({
            "ware": ware, "stufe": s, "dauer": dauer, "ab": ab,
            "gemeldet": False, "start": None, "ende": None,
        })
    schlange["auftraege"].append({"ware": ware, "anzahl": menge, "stufe": s, "dauer": dauer})

    if dauer is None:
        return True, (f"{menge}x {ware} eingereiht - Dauer nicht belegt, "
                      f"die Ware wartet im Stapel.")
    return True, f"{menge}x {ware} eingereiht ({dauer / 60.0:.1f} Minuten je Stueck)."


def _fortschreiben(schlange: Dict[str, Any], jetzt: float) -> float:
    """Plant alle Einheiten ab dem Queue-Start und liefert die aktuelle Stapelzeit."""
    try:
        jetzt = float(jetzt)
    except (TypeError, ValueError):
        jetzt = 0.0
    if schlange.get("_basis") is None:
        schlange["_basis"] = jetzt
    basis = float(schlange["_basis"])
    if jetzt < basis:
        jetzt = basis
    uhr = schlange.get("_uhr")
    if uhr is None or jetzt > float(uhr):
        schlange["_uhr"] = jetzt

    n = int(schlange.get("kapazitaet") or 0)
    einheiten = schlange.get("einheiten", [])
    if n < 1:
        for e in einheiten:
            e["start"] = None
            e["ende"] = None
        return float(schlange["_uhr"])

    slots = [basis] * n
    for e in einheiten:
        i = min(range(n), key=lambda k: slots[k])          # fruehester freier Platz
        ab = e.get("ab")
        start = slots[i] if ab is None else max(slots[i], float(ab))
        e["start"] = start
        if e.get("dauer") is None:
            e["ende"] = None
            slots[i] = float("inf")                        # belegter Platz bleibt belegt
        else:
            e["ende"] = start + float(e["dauer"])
            slots[i] = e["ende"]
    return float(schlange["_uhr"])


def fortschritt(schlange: Dict[str, Any], jetzt: float) -> Dict[str, Any]:
    """Was laeuft, was ist fertig und wie lange der Stapel noch braucht."""
    t = _fortschreiben(schlange, jetzt)
    laeuft: List[Dict[str, Any]] = []
    fertig: List[Dict[str, Any]] = []
    wartend: List[Dict[str, Any]] = []
    unbelegt: List[Dict[str, Any]] = []
    enden: List[float] = []

    for e in schlange.get("einheiten", []):
        if e.get("dauer") is None:
            unbelegt.append({"ware": e["ware"], "stufe": e["stufe"]})
            continue
        start = e.get("start")
        ende = e.get("ende")
        if start is None or ende is None:          # kein Platz geplant (Kapazitaet 0)
            wartend.append({"ware": e["ware"], "stufe": e["stufe"]})
            continue
        enden.append(float(ende))
        if start <= t < ende:
            laeuft.append({"ware": e["ware"], "stufe": e["stufe"],
                           "start": start, "ende": ende,
                           "rest_sekunden": round(ende - t, 3)})
        elif ende <= t:
            fertig.append({"ware": e["ware"], "stufe": e["stufe"], "ende": ende})
        else:
            wartend.append({"ware": e["ware"], "stufe": e["stufe"]})

    if unbelegt:
        rest: Optional[float] = None
        hinweis = "Dauer nicht belegt"
    else:
        rest = round(max(0.0, (max(enden) - t) if enden else 0.0), 3)
        hinweis = ""

    return {
        "typ": schlange.get("typ"),
        "werkstatt": schlange.get("werkstatt"),
        "kapazitaet": schlange.get("kapazitaet", 0),
        "zeit": t,
        "laeuft": laeuft,
        "fertig": fertig,
        "fertig_anzahl": len(fertig),
        "wartend": wartend,
        "unbelegt": unbelegt,
        "rest_sekunden": rest,
        "hinweis": hinweis,
        "text": _fortschritt_text(schlange.get("werkstatt"), laeuft, fertig, wartend,
                                  unbelegt, rest),
    }


def _fortschritt_text(werkstatt: Any, laeuft, fertig, wartend, unbelegt,
                      rest: Optional[float]) -> str:
    teile = [f"Werkstatt {werkstatt}"]
    if laeuft:
        teile.append(f"in Arbeit: {len(laeuft)}")
    teile.append(f"fertig: {len(fertig)}")
    if wartend:
        teile.append(f"wartend: {len(wartend)}")
    if unbelegt:
        teile.append(f"ohne belegte Dauer: {len(unbelegt)} (Dauer nicht belegt)")
    if rest is None:
        teile.append("Restzeit nicht berechenbar - Dauer nicht belegt")
    else:
        teile.append(f"Restzeit {rest / 60.0:.1f} Minuten")
    return " | ".join(teile)


def fertige_waren(schlange: Dict[str, Any], jetzt: float) -> Dict[str, int]:
    """{ware: menge} - was SEIT dem letzten Aufruf fertig geworden ist."""
    t = _fortschreiben(schlange, jetzt)
    neu: Dict[str, int] = {}
    for e in schlange.get("einheiten", []):
        if e.get("dauer") is None or e.get("ende") is None:
            continue
        if e["ende"] <= t and not e.get("gemeldet"):
            e["gemeldet"] = True
            neu[e["ware"]] = neu.get(e["ware"], 0) + 1
    return neu


# --------------------------------------------------------------------------
# 5. Siedlungskarte: die gebauten Werkstaetten (wie gebaeude_wirkung.py)
# --------------------------------------------------------------------------

def _feld(objekt, name, vorgabe=None):
    if isinstance(objekt, dict):
        return objekt.get(name, vorgabe)
    return getattr(objekt, name, vorgabe)


def werkstaetten_bestand(siedlungen) -> Dict[str, int]:
    """{kennung: anzahl} der gebauten Werkstaetten ueber alle Siedlungskarten."""
    zaehlung: Dict[str, int] = {k: 0 for k in werkstaetten()}
    for siedlung in siedlungen or []:
        for _feldindex, gebaut in (_feld(siedlung, "bauten") or {}).items():
            kennung = gelaende.finde_gebaeude(gebaut)
            if kennung in zaehlung:
                zaehlung[kennung] += 1
    return zaehlung


def werkstatt_stufe(siedlung, typ: str) -> int:
    """Hoechste Ausbaustufe einer Werkstatt in EINER Siedlung (0 = nicht gebaut)."""
    kennung = _werkstatt_kennung(typ)
    if not kennung:
        return 0
    stufen = _feld(siedlung, "stufen") or {}
    beste = 0
    for feldindex, gebaut in (_feld(siedlung, "bauten") or {}).items():
        if gelaende.finde_gebaeude(gebaut) == kennung:
            try:
                beste = max(beste, int(stufen.get(str(feldindex), 1)))
            except (TypeError, ValueError):
                beste = max(beste, 1)
    return beste


# --------------------------------------------------------------------------
# 6. Lager: lesbare Bestandszeile
# --------------------------------------------------------------------------

def lager_text(bestand: Dict[str, Any]) -> str:
    """Eine lesbare Zeile des Warenbestands im Lager (Handbuch Seite 14)."""
    if not bestand:
        return "Lager: leer"
    teile: List[str] = []
    for ware in sorted(bestand):
        try:
            menge = int(bestand[ware])
        except (TypeError, ValueError):
            continue
        if menge > 0:
            teile.append(f"{menge} {ware}")
    if not teile:
        return "Lager: leer"
    return "Lager: " + ", ".join(teile)
