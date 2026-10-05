"""Nebelseetal Remake — deterministischer Kern der Spielökonomie (Ökonomie-Paket, Schritt 2).

Quelle: `docs/audits/entwurf_spieloekonomie_sol_2026-10-05.txt` (Abschnitt F, Schritt 2,
Codeblock Z. 237-414). Reine Rechenlogik **ohne** Oberfläche und **ohne** main-Abhängigkeit:
Karten aus festen Kontingenten, Kartenqualität (drei Achsen), Schattenpreise und die
Gründungs-Transaktion.

Bewusste Grenzen dieses Schritts (stehen so im Entwurf):
  * Die alten `kartentypen.listen` und ihr Generator bleiben **unverändert**; dieser Kern
    benutzt ausschließlich `data/gelaende.json` → `kartenvorrat` als Wahrheit.
  * Nichts ruft dieses Modul auf. Der Ökonomiemodus wird erst nach dem letzten
    Integrationsschritt aktiviert; bis dahin läuft der Altmodus unverändert.
  * Alle Schwellen, Gewichte und Gebühren sind **VORSCHLAG** (siehe `data/spieloekonomie.json`).

Die Kontingente sind exakte Feldzahlen: `feste_karte` prüft selbst, dass sie zum Kartenmaß
passen, das Sumpfkontingent einhalten und den Mindestbesatz erfüllen — ein falscher Eintrag
fällt sofort auf, statt eine unspielbare Karte zu erzeugen.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import random
from pathlib import Path

import einheiten  # noqa: F401  (vom Entwurf vorgesehen; hier für spätere Schritte)
import gelaende
import spieldaten
import wirtschaft

DATEN = Path(spieldaten.projektwurzel()) / "data"


def lade(name: str) -> dict:
    return json.loads((DATEN / name).read_text(encoding="utf-8"))


REGELN = lade("spieloekonomie.json")
G = lade("gelaende.json")
BP = lade("baupreise.json")["preise"]
U = lade("units.json")["einheiten"]


def mengen(kosten) -> dict:
    """Nur die echten Mengen eines Kosten-Eintrags (Kennzeichnungen wie ``_belegt`` fallen weg)."""
    return {k: float(v) for k, v in kosten.items()
            if isinstance(v, (int, float)) and not isinstance(v, bool)}


def gruendungskosten():
    """(Gebühr, Startpaket, Mindestbestand) aus den Regeldaten und den echten Preisen."""
    r = REGELN["gruendung"]
    haus = mengen(BP["haus"])
    preis = {k: v * r["hausmultiplikator"] for k, v in haus.items()}
    paket = {k: v * r["reserve_hausmultiplikator"] for k, v in haus.items()}
    preis["nahrung"] = U[r["karren"]]["kosten"]["nahrung"] * r["nahrung_karrenanteil"]
    paket["nahrung"] = U[r["reserve_nahrung_einheit"]]["kosten"]["nahrung"]
    minimum = {k: preis.get(k, 0) + paket.get(k, 0) for k in preis.keys() | paket.keys()}
    return preis, paket, minimum


def feste_karte(seed, eintrag: dict) -> dict:
    """Eine Karte aus festen Kontingenten (nur die Positionen sind durch die Saat gemischt)."""
    w = eintrag["gewichte"]
    if set(w) != set(gelaende.GELAENDEARTEN):
        raise ValueError("Kontingente müssen genau die bekannten Geländearten enthalten.")
    if any(type(v) is not int or v < 0 for v in w.values()):
        raise ValueError("Kontingente müssen nichtnegative ganze Zahlen sein.")
    m = G["kartenmass"]
    if sum(w.values()) != m["spalten"] * m["zeilen"]:
        raise ValueError("Kontingente passen nicht zum Kartenmaß.")
    if w[gelaende.SUMPF] != G["regeln"]["sperrfelder"]:
        raise ValueError("Sumpfkontingent verletzt die Sperrfeldregel.")
    for art, minimum in G["regeln"]["mindestbesatz"].items():
        if not art.startswith("_") and w[art] < minimum:
            raise ValueError("Mindestbesatz verletzt: " + art)
    raster = [art for art in gelaende.GELAENDEARTEN for _ in range(w[art])]
    random.Random(str(seed)).shuffle(raster)
    breite = m["spalten"]
    return {"seed": str(seed), "spalten": breite, "zeilen": m["zeilen"],
            "felder": len(raster), "bauplaetze": len(raster) - w[gelaende.SUMPF],
            "raster": raster, "zeilen_raster": [raster[i:i + breite] for i in range(0, len(raster), breite)],
            "zaehlung": dict(w), "typ": eintrag["id"], "typ_name": eintrag["name"],
            "vorteil": "Feste Kontingente; Ertragsprofil und Versorgungsplan beachten."}


def vorrat(seed) -> dict:
    """Der feste Kartenvorrat für Neugründungen (Koloniekarten, noch ohne Besitzer)."""
    return {e["id"]: {"karte": feste_karte(f"{seed}:{e['id']}", e), "besitzer": None}
            for e in G["kartenvorrat"]["kolonien"]}


def startkarte(seed, eigentuemer) -> dict:
    """Die private, ausgeglichene Startkarte eines Akteurs (nicht Teil des Vorrats)."""
    return feste_karte(f"{seed}:start:{eigentuemer}", G["kartenvorrat"]["start"])


def kapazitaeten(karte) -> dict:
    """Theoretische Stundenerträge einer Karte, Kennungen in Kleinschreibung."""
    return {k.lower(): float(v) for k, v in wirtschaft.kapazitaet({"karte": karte}).items()}


def achsen(karte) -> tuple:
    """Die drei Vergleichsachsen (Holz, Gestein, Agrar) — je die unabhängige Obergrenze."""
    n = karte["zaehlung"]
    return (n["wald"] * gelaende.ertrag_pro_stunde("holzfaeller", "wald")
            + n["steppe"] * gelaende.ertrag_pro_stunde("holzfaeller", "steppe"),
            n["berg"] * gelaende.ertrag_pro_stunde("steinmetz", "berg")
            + n["huegel"] * gelaende.ertrag_pro_stunde("steinmetz", "huegel"),
            n["grasland"] * gelaende.ertrag_pro_stunde("farm", "grasland")
            + n["steppe"] * gelaende.ertrag_pro_stunde("farm", "steppe"))


def relativ(karte) -> tuple:
    """Die drei Achsen einer Karte im Verhältnis zur Startreferenz."""
    basis = achsen(feste_karte("referenz", G["kartenvorrat"]["start"]))
    return tuple(a / b for a, b in zip(achsen(karte), basis))


def kartenqualitaet(karten: list) -> dict:
    """Erfüllt ein Verbund die drei Bedingungen (Anzahl, Mittelwert, Spezialist)?

    ``mittel`` = Mittelwert der Achsen über alle Karten, ``beste`` = bester Einzelwert je
    Achse. Alle Werte sind Verhältnisse zur Startreferenz.
    """
    if not karten:
        return {"erfuellt": False, "mittel": (0, 0, 0), "beste": (0, 0, 0)}
    werte = [relativ(k) for k in karten]
    mittel = tuple(sum(w[i] for w in werte) / len(werte) for i in range(3))
    beste = tuple(max(w[i] for w in werte) for i in range(3))
    ok = (len(karten) >= REGELN["mindestsiedlungen"]
          and min(mittel) >= REGELN["portfoliofaktor"]
          and min(beste) >= REGELN["spezialistenfaktor"])
    return {"erfuellt": ok, "mittel": mittel, "beste": beste}


def kartennutzen(karten: list, kandidat) -> float:
    """Marginaler Nutzen einer Karte für ein bestehendes Portfolio (Defizite zählen mehr)."""
    vorher = [relativ(k) for k in karten]
    neu = relativ(kandidat)
    if not vorher:
        return sum(neu)
    # Defizite und fehlende Spezialisten, nicht maximale Holzsumme.
    bedarf = [max(0, REGELN["portfoliofaktor"] * len(vorher) - sum(w[i] for w in vorher))
              + max(0, REGELN["spezialistenfaktor"] - max(w[i] for w in vorher))
              for i in range(3)]
    return sum(neu[i] * (1 + bedarf[i]) for i in range(3))


def _begrenzen(wert, grenzen):
    return min(grenzen[1], max(grenzen[0], wert))


def einzelmaximum() -> dict:
    """Bester Einzelfeldertrag je Rohstoff über alle baubaren Geländearten."""
    beste = {}
    for art in gelaende.GELAENDEARTEN:
        if not gelaende.ist_bebaubar(art):
            continue
        for kennung, geb in gelaende.alle_gebaeude().items():
            e = gelaende.ertrag_pro_stunde(kennung, art)
            if isinstance(e, (int, float)):
                e = {geb["rohstoff"]: e}
            for r, v in (e or {}).items():
                beste[r.lower()] = max(beste.get(r.lower(), 0), float(v))
    return beste


def schattenpreis(karte, rohstoff: str, bestand: float, reserve: float) -> float:
    """Lokaler Schattenpreis eines Rohstoffs in Gold (Gold selbst ist immer 1)."""
    if rohstoff == "gold":
        return 1.0
    beste = einzelmaximum()
    lokal = kapazitaeten(karte).get(rohstoff, 0)
    start = kapazitaeten(feste_karte("preis", G["kartenvorrat"]["start"]))[rohstoff]
    ratio = start / lokal if lokal > 0 else math.inf
    k = _begrenzen(ratio, REGELN["kartenpreisgrenzen"])
    v = 1.0 if reserve <= 0 else _begrenzen(2 * reserve / (reserve + bestand), REGELN["vorratspreisgrenzen"])
    return beste["gold"] / beste[rohstoff] * k * v


def bezahlbar(bestand: dict, kosten: dict) -> bool:
    return all(math.isfinite(v) and v >= 0 and bestand.get(r, 0) >= v
               for r, v in kosten.items())


def buchen(bestand: dict, delta: dict) -> dict:
    """Bucht ein Delta auf einen Bestand; negative Bestände sind ein Fehler, keine Rundung."""
    neu = dict(bestand)
    for r, v in delta.items():
        if not math.isfinite(v):
            raise ValueError("Nicht endliche Buchung.")
        neu[r] = neu.get(r, 0) + v
        if neu[r] < -1e-9:
            raise ValueError("Nicht genügend Bestand: " + r)
        neu[r] = max(0.0, neu[r])
    return neu


def absicht(quelle: dict, karte_id: str, karten: list, freie: dict,
            forschung: dict, runde: int) -> dict:
    """Prüft eine Gründungsabsicht und liefert das Sperrgut (noch wird nichts gebucht)."""
    r = REGELN["gruendung"]
    if karte_id not in freie or freie[karte_id]["besitzer"] is not None:
        raise ValueError("Karte nicht frei.")
    if len(karten) >= quelle["siedlungsgrenze"]:
        raise ValueError("Siedlungsgrenze erreicht.")
    if forschung.get(r["forschung"], 0) < r["stufe"]:
        raise ValueError("Gründungsforschung fehlt.")
    if quelle["einheiten"].get(r["karren"], 0) < 1:
        raise ValueError("Siedlerkarren fehlt.")
    preis, paket, minimum = gruendungskosten()
    if not bezahlbar(quelle["vorraete"], minimum):
        raise ValueError("Lokaler Mindestbestand fehlt.")
    return {"quelle": quelle["id"], "besitzer": quelle["besitzer"], "karte_id": karte_id,
            "runde": runde, "sperrgut": minimum, "preis": preis, "paket": paket,
            "nutzen": kartennutzen(karten, freie[karte_id]["karte"])}


def vergabe(absichten: list, freie: dict, seed, runde: int) -> list:
    """Vergibt die Karten einer Runde: höherer Nutzen gewinnt, Gleichstand über SHA-256.

    Die Sortierung ist **unabhängig** von Listen- oder Klickreihenfolge; jede Kennung wird
    höchstens einmal vergeben, veraltete Absichten werden abgelehnt.
    """
    def rang(a):
        text = f"{seed}:{runde}:{a['karte_id']}:{a['besitzer']}"
        return (-a["nutzen"], hashlib.sha256(text.encode("utf-8")).hexdigest())

    ergebnis, akteure, vergeben = [], set(), set()
    for a in sorted(absichten, key=rang):
        if a["runde"] != runde or a["besitzer"] in akteure:
            raise ValueError("Unzulässige doppelte oder veraltete Absicht.")
        akteure.add(a["besitzer"])
        ok = (a["karte_id"] in freie and freie[a["karte_id"]]["besitzer"] is None
              and a["karte_id"] not in vergeben)
        ergebnis.append((a, ok))
        if ok:
            vergeben.add(a["karte_id"])
    return ergebnis
