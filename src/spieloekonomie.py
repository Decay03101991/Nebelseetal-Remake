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

import auftraege
import einheiten  # noqa: F401  (vom Entwurf vorgesehen; hier für spätere Schritte)
import gelaende
import spieldaten
import werkstatt
import wirtschaft

DATEN = Path(spieldaten.projektwurzel()) / "data"


def lade(name: str) -> dict:
    return json.loads((DATEN / name).read_text(encoding="utf-8"))


REGELN = lade("spieloekonomie.json")
G = lade("gelaende.json")
BP = lade("baupreise.json")["preise"]
U = lade("units.json")["einheiten"]
# Die freigegebenen Warenrezepte (Oekonomie-Paket, Schritt 4). Zur Laufzeit wird AUSSCHLIESSLICH
# diese eingefrorene Datei gelesen - nicht neu abgeleitet (Entwurf Z. 588). Erzeugt von
# `tools/warenrezepte_ableiten.py`.
WARENREZEPTE = lade("warenrezepte.json")


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


# ---------------------------------------------------------------------------
# Schritt 3 — lokale Lager und Transportbuchung (Entwurf Z. 417-505)
# ---------------------------------------------------------------------------
#
# Eine lokale Wirtschaft ist Voraussetzung, nicht Kür für: Vorräte, Waren, Einheiten und
# Werkstatt-/Bibliotheksauftrag — sie liegen JE SIEDLUNG. Gemeinsame Summen sind nur abgeleitete
# Anzeige; kein Auftrag darf damit bezahlen. „Beute gibt es nur mit Transportkarren" ist
# belegt (Handbuch S. 23) und wird von `auftraege.starten` für die Art „transportieren"
# bereits erzwungen („Transportieren braucht mindestens einen Karren.").
#
# WICHTIG für die spätere main-Anbindung (Entwurf Z. 505): `auftraege.spieldaten_anwenden`
# darf auf einen EIGENTRANSPORT niemals angewendet werden — eigene Transporte bucht
# ausschließlich `transport_fortschritt`.


def verbrauchen(ort: dict, kosten: dict, jetzt: float) -> dict:
    """Bucht Kosten aus dem LOKALEN Lager ab und schreibt die Importherkunft mit.

    Der Verbrauch wird anteilig aus dem importierten Bestand gedeckt — so belegt das
    Verbrauchsjournal, dass wirklich eine gelieferte Fracht genutzt wurde (Siegnachweis,
    Schritt 7). Reicht das lokale Lager nicht, ist das ein Fehler, keine stille Nullbuchung.
    """
    neu = copy.deepcopy(ort)
    if not bezahlbar(neu["vorraete"], kosten):
        raise ValueError("Lokales Lager reicht nicht.")
    for r, m in kosten.items():
        v = neu["vorraete"].get(r, 0)
        importiert = neu["importiert"].get(r, 0)
        genutzt = 0 if v <= 0 else m * importiert / v
        neu["vorraete"][r] = v - m
        neu["importiert"][r] = max(0, importiert - genutzt)
        if genutzt > 0:
            neu["verbrauchsjournal"].append({"zeit": jetzt, "rohstoff": r, "menge": genutzt,
                                             "ziel": ort["id"]})
    return neu


def transport_start(quelle: dict, ziel: dict, bestand: dict, fracht: dict, jetzt: float,
                    frachtkanal: str = "vorraete"):
    """Startet einen Transport zwischen EIGENEN Siedlungen. Liefert (neue_quelle, mission).

    ``frachtkanal`` ist ``"vorraete"`` (Rohstoffe) oder ``"waren"``. Importherkunft und
    Verbrauchsjournal gelten nur für Rohstoffe — der Siegnachweis zählt keine Waren.
    Jede Ablehnung wirft ``ValueError``; es wird nichts halb gebucht.
    """
    if frachtkanal not in ("vorraete", "waren"):
        raise ValueError("Unbekannter Frachtkanal.")
    if quelle["besitzer"] != ziel["besitzer"]:
        raise ValueError("Für eigene Transporte muss der Besitzer übereinstimmen.")
    if quelle["dimension"] != ziel["dimension"]:
        raise ValueError("Dimensionswechsel braucht eigene Portalregeln.")
    if not bestand or not all(type(n) is int and n > 0 for n in bestand.values()):
        raise ValueError("Ungültige Transporttruppe.")
    if any(quelle["einheiten"].get(n, 0) < m for n, m in bestand.items()):
        raise ValueError("Einheiten sind nicht am Ausgangsort.")
    if any(type(m) is not int or m < 0 for m in fracht.values()):
        raise ValueError("Fracht muss aus nichtnegativen ganzen Mengen bestehen.")
    if frachtkanal == "vorraete" and set(fracht) - set(quelle["vorraete"]):
        raise ValueError("Unbekannter Rohstoff; Waren brauchen ausdrücklich einen Warenauftrag.")
    if not bezahlbar(quelle[frachtkanal], fracht):
        raise ValueError("Fracht fehlt am Ausgangsort.")
    d = abs(quelle["x"] - ziel["x"]) + abs(quelle["y"] - ziel["y"])
    liste = []
    ok, meldung = auftraege.starten(liste, "transportieren", bestand, quelle["id"], ziel["id"],
                                    d, jetzt, fracht)
    if not ok:
        raise ValueError(meldung)
    neu = copy.deepcopy(quelle)
    anteil = {}
    for r, m in fracht.items():
        v = neu[frachtkanal][r]
        anteil[r] = (0 if (v <= 0 or frachtkanal != "vorraete")
                     else m * neu["importiert"].get(r, 0) / v)
        neu[frachtkanal][r] -= m
        if frachtkanal == "vorraete":
            neu["importiert"][r] = max(0, neu["importiert"].get(r, 0) - anteil[r])
    for n, m in bestand.items():
        neu["einheiten"][n] -= m
    mission = liste[0]
    mission.update({"eigentransport": True, "ziel_id": ziel["id"], "quelle_id": quelle["id"],
                    "frachtkanal": frachtkanal, "ursprung_import": anteil,
                    "geliefert_lokal": False, "heimgekehrt_lokal": False})
    mission["besitzer"] = quelle["besitzer"]
    return neu, mission


def transport_fortschritt(mission: dict, orte: dict, jetzt: float):
    """Bucht Ankunft und Rückkehr eines eigenen Transports **genau einmal**. (orte, mission).

    Bei Ankunft wird die Fracht am Ziel gutgeschrieben; bei Rückkehr kehrt sie (samt
    Importherkunft) zum Ausgangsort zurück. Ist der Ausgangsort verloren oder erobert, gilt
    er wie ein nicht mehr vorhandener: dann wird eine eigene Ersatzsiedlung gesucht, sonst
    bleibt die Fracht am Auftrag — **keine** Geistergutschrift.
    """
    neu = copy.deepcopy(orte)
    m = copy.deepcopy(mission)
    kanal = m.get("frachtkanal", "vorraete")
    ziel = neu.get(m["ziel_id"])
    if jetzt >= m["ankunft"] and not m["geliefert_lokal"]:
        if ziel is not None and ziel["besitzer"] == m["besitzer"]:
            for r, n in m["fracht"].items():
                ziel[kanal][r] = ziel[kanal].get(r, 0) + n
                if kanal == "vorraete":
                    # Nicht als lokaler Verbrauch werten: erst ein späterer echter Auftrag zählt.
                    ziel["importiert"][r] = ziel["importiert"].get(r, 0) + n
            m["fracht"] = {}
            if m.get("stationieren_lokal"):
                for n, k in m["einheiten"].items():
                    ziel["einheiten"][n] = ziel["einheiten"].get(n, 0) + k
                m["einheiten"] = {}
                m["heimgekehrt_lokal"] = True
        m["geliefert_lokal"] = True
    if jetzt >= m["rueckkehr"] and not m["heimgekehrt_lokal"]:
        quelle = neu.get(m["quelle_id"])
        if quelle is not None and quelle["besitzer"] != m["besitzer"]:
            quelle = None            # eroberter Ausgangsort zählt wie ein verlorener
        if quelle is None:
            quelle = next((o for _, o in sorted(neu.items()) if o["besitzer"] == m["besitzer"]),
                          None)
            m["ersatzort"] = quelle["id"] if quelle is not None else None
        if quelle is not None:
            for n, k in m["einheiten"].items():
                quelle["einheiten"][n] = quelle["einheiten"].get(n, 0) + k
            for r, k in m["fracht"].items():
                quelle[kanal][r] = quelle[kanal].get(r, 0) + k
                if kanal == "vorraete":
                    quelle["importiert"][r] = (quelle["importiert"].get(r, 0)
                                               + m["ursprung_import"].get(r, 0))
            m["fracht"] = {}
            m["heimgekehrt_lokal"] = True
        # KEINE eigene Siedlung vorhanden: Fracht und Einheiten BLEIBEN am Auftrag, und der
        # Merker bleibt AUS (Entwurf Z. 492/500: „Fracht bleibt am Auftrag und ist nicht global
        # verfuegbar"). So kann ein spaeter auftauchender eigener Ort die Fracht noch erhalten —
        # es wird nichts erfunden und an Fremde nichts verteilt.
        # Fund der unabhaengigen Abweichungspruefung (docs/audits/pruefung_schritt3_4.md, Punkt 12).
    return neu, m


def station_start(quelle: dict, ziel: dict, bestand: dict, fracht: dict, jetzt: float):
    """Ein Transport, dessen Einheiten am Ziel bleiben (Stationierung). (neue_quelle, mission)."""
    q, m = transport_start(quelle, ziel, bestand, fracht, jetzt)
    m["stationieren_lokal"] = True
    return q, m


# ---------------------------------------------------------------------------
# Schritt 4 — Pilotrezepte, lokale Ausbildung und echte Verbrauchsbelege
# (Entwurf Z. 507-590)
# ---------------------------------------------------------------------------
#
# Die Rezepte stehen eingefroren in `data/warenrezepte.json` (erzeugt von
# `tools/warenrezepte_ableiten.py`); zur Laufzeit wird ausschliesslich diese Datei gelesen.
# Alle Dauerangaben ausser dem Schwert (1200 s, belegt) sind VORSCHLAG.


def ware_start(ort: dict, ware: str, forschung: dict, jetzt: float,
               rezepte: dict = None) -> dict:
    """Reiht eine Ware in die Werkstatt DIESER Siedlung ein. Liefert den neuen Ort.

    Geprueft werden (1) ein freigegebenes Rezept, (2) die Forschungsvoraussetzungen der Ware,
    (3) eine Werkstatt VOR ORT, (4) die Materialkosten im lokalen Lager. Die Dauer kommt aus
    dem Rezept in die Warteschlange — die einzige belegte Dauer (Schwert) bleibt unberuehrt.
    """
    neu = copy.deepcopy(ort)
    rezepte = WARENREZEPTE if rezepte is None else rezepte
    if ware not in rezepte:
        raise ValueError("Keine freigegebene Rezeptangabe.")
    rezept = rezepte[ware]
    if any(forschung.get(f, 0) < n for f, n in rezept["voraussetzungen"].items()):
        raise ValueError("Warenvoraussetzung fehlt.")
    typ = werkstatt.werkstatt_fuer(ware)
    if typ is None:
        raise ValueError("Ware gehoert zu keiner Werkstatt.")
    zahl = werkstatt.werkstaetten_bestand([neu])[typ]
    if zahl <= 0:
        raise ValueError("Werkstatt nicht in dieser Stadt.")
    neu = verbrauchen(neu, rezept["kosten"], jetzt)
    schlange = neu["werkstaetten"].setdefault(typ, werkstatt.neue_warteschlange(typ, zahl))
    schlange["werkstaetten"] = zahl
    schlange["kapazitaet"] = werkstatt.kapazitaet(zahl)
    werkstatt.fortschritt(schlange, jetzt)
    ok, meldung = werkstatt.einreihen(schlange, ware, 1, 1, rezepte)
    if not ok:
        raise ValueError(meldung)
    return neu


def ausbildung_start(ort: dict, name: str, forschung: dict, jetzt: float) -> dict:
    """Beginnt die Ausbildung EINER Einheit vor Ort. Liefert den neuen Ort.

    Geprueft werden (1) die Forschungsstufe der Einheit, (2) die Ausbildungsstaette VOR ORT
    (Kriegerakademie / Diebesgilde / Stellmacher), (3) genug freie Siedler, (4) die
    Ausruestung im lokalen Warenlager. Verbraucht werden Kosten, Siedler und Ausruestung —
    die Einheit selbst entsteht erst am Ende der Ausbildungszeit (`ort_tick`, Schritt 5).
    """
    eintrag = U.get(name)
    if eintrag is None:
        raise ValueError("Unbekannte Einheit: " + str(name))
    voraus = eintrag.get("voraussetzung") or {}
    if voraus and forschung.get(voraus.get("forschung"), 0) < voraus.get("stufe", 0):
        raise ValueError("Einheitenforschung fehlt.")
    import gebaeude_wirkung
    geb = gelaende.finde_gebaeude(str(eintrag.get("gebaeude") or ""))
    stufe = gebaeude_wirkung.gebaeude_stufe(ort, geb)
    if stufe <= 0:
        raise ValueError("Ausbildungsstätte fehlt vor Ort.")
    kosten = dict(eintrag.get("kosten") or {})
    siedler = kosten.pop("siedler", 0)
    if ort["bevoelkerung"] < siedler:
        raise ValueError("Freie Siedler fehlen vor Ort.")
    import ausruestung
    if ausruestung.fehlende(name, ort["waren"]):
        raise ValueError("Ausrüstung fehlt vor Ort.")
    neu = verbrauchen(ort, kosten, jetzt)
    neu["bevoelkerung"] -= siedler
    neu["waren"] = ausruestung.verbrauchen(neu["waren"], name)
    freie_zeit = max([jetzt] + [a["ende"] for a in neu["ausbildung"] if a["gebaeude"] == geb])
    # Pilotregel: die Dauer ist kein Originalwert (das Handbuch nennt keine Ausbildungsdauer).
    neu["ausbildung"].append({"einheit": name, "gebaeude": geb, "start": freie_zeit,
                              "ende": freie_zeit + REGELN["pilot_ausbildung_minuten"] * 60,
                              "gebucht": False})
    return neu
