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
import ausruestung
import einheiten  # noqa: F401  (vom Entwurf vorgesehen; hier für spätere Schritte)
import forschung
import forschungspfad
import gebaeude_wirkung
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


# ---------------------------------------------------------------------------
# Schritt 5 — gemeinsame Spieluhr: lokale Produktion und Fortschritt
# (Entwurf Z. 592-648)
# ---------------------------------------------------------------------------
#
# Der Ökonomiemodus hat EINE Uhr: `spielsekunden` (Spielzeit, nicht Rechnerzeit). Dieses Modul
# rechnet nur damit; `main._tick_loop` multipliziert genau einmal mit `spielzeit.faktor()`.
# Solange der Ökonomiemodus nicht aktiviert ist, ruft niemand diese Funktionen auf.


def ort_tick(ort: dict, ab: float, bis: float, forschung: dict) -> dict:
    """Einen Ort von Spielzeit `ab` bis `bis` fortschreiben. Liefert den neuen Ort.

    Produziert über `wirtschaft.ertrag_gesamt` (dieselbe Quelle wie die Anzeige), schreibt
    Siedlerzuwachs bis zur Grenze fort, holt fertige Werkstattwaren ins Lager und bucht
    abgeschlossene Ausbildungen **genau einmal** (`gebucht`). Jede Produktionsspanne landet im
    `produktionsjournal` — Grundlage des Versorgungsfensters (Schritt 7).
    """
    if bis < ab:
        raise ValueError("Spielzeit darf nicht zurücklaufen.")
    neu = copy.deepcopy(ort)
    ertrag = {k.lower(): v for k, v in wirtschaft.ertrag_gesamt([neu], forschung).items()}
    produktion = {}
    for r, rate in ertrag.items():
        menge = rate * (bis - ab) / 3600.0
        neu["vorraete"][r] = neu["vorraete"].get(r, 0) + menge
        produktion[r] = menge
    grenze = gebaeude_wirkung.bevoelkerungsgrenze([neu])
    zuwachs = gebaeude_wirkung.siedler_zuwachs_pro_stunde([neu], forschung) * (bis - ab) / 3600.0
    neu["bevoelkerung"] = min(grenze, neu["bevoelkerung"] + zuwachs)
    if bis > ab:
        neu["produktionsjournal"].append({"ab": ab, "bis": bis, "mengen": produktion})
    for schlange in neu["werkstaetten"].values():
        for ware, n in werkstatt.fertige_waren(schlange, bis).items():
            neu["waren"][ware] = neu["waren"].get(ware, 0) + n
            neu["fertigjournal"].append({"zeit": bis, "art": "ware", "name": ware})
    for a in neu["ausbildung"]:
        if not a["gebucht"] and a["ende"] <= bis:
            name = a["einheit"]
            neu["einheiten"][name] = neu["einheiten"].get(name, 0) + 1
            a["gebucht"] = True
            neu["fertigjournal"].append({"zeit": a["ende"], "art": "einheit", "name": name})
    return neu


def fensterproduktion(orte: list, jetzt: float) -> dict:
    """Tatsächlich produzierte Mengen im Versorgungsfenster (rückblickend bis `jetzt`).

    Zählt aus den `produktionsjournal`-Zeilen anteilig — eine Zeile, die nur halb ins Fenster
    reicht, zählt auch nur halb. So kann eine Momentaufnahme die Versorgung nicht vortäuschen.
    """
    start = jetzt - REGELN["versorgung_stunden"] * 3600
    out: dict = {}
    for ort in orte:
        for zeile in ort.get("produktionsjournal") or []:
            dauer = zeile["bis"] - zeile["ab"]
            anteil = max(0.0, min(jetzt, zeile["bis"]) - max(start, zeile["ab"]))
            if dauer > 0 and anteil > 0:
                for r, n in (zeile.get("mengen") or {}).items():
                    out[r] = out.get(r, 0) + n * anteil / dauer
    return out


# ---------------------------------------------------------------------------
# Schritt 6 — Forschung JE SIEDLUNG: lokaler Forschungsstart statt globaler
# Bibliotheksabkürzung (Entwurf Z. 650-686)
# ---------------------------------------------------------------------------
#
# BELEGT (Handbuch 2009): die Bibliothek ist je Siedlung (Z. 404 „In jeder Siedlung kann nur eine
# einzige Bibliothek gebaut werden."), und die Sperre gilt „in der Siedlung, in der geforscht wird"
# (Z. 423-424); Z. 245 spricht von den „in den Siedlungen laufenden Forschungen" (Mehrzahl) — zwei
# Siedlungen dürfen also **verschiedene** Gebiete gleichzeitig erforschen. Der laufende Auftrag hängt
# darum am **Ort** (`ort["forschungsauftrag"]`), nicht am Spieler.
#
# Die erreichte **Stufe** bleibt in `wissen` (dem übergebenen Stand) — ob dieser Stand je Siedlung
# oder für das ganze Volk gilt, sagt das Handbuch **nicht** (Z. 104-106 „Dein Volk" gegen Z. 397
# „Deine Siedlungen"); das ist offen und in `docs/audits/belege_forschung_je_siedlung.md` festgehalten.


def forschung_start(ort: dict, gebiet: str, wissen: dict, jetzt: float,
                    weitere_orte: list = ()) -> dict:
    """Einen Forschungsauftrag **in dieser Siedlung** erteilen. Liefert den neuen Ort.

    Prüft: keine zweite Forschung in derselben Bibliothek · bekanntes Gebiet · Voraussetzungen
    über `forschungspfad.erfuellt` (mit der Bibliotheksstufe **dieses** Ortes) · Rohstoffe.
    Die Kosten werden beim Start verbraucht; die Stufe steigt erst am Ende (`forschung_abschluss`).

    `weitere_orte` sind die übrigen **eigenen** Orte. Der Entwurf (Z. 685) verlangt ausdrücklich,
    dass dieselbe Zielstufe nicht gleichzeitig in zwei Städten läuft — sonst zahlt man zweimal und
    lernt einmal. Verschiedene Gebiete dürfen in verschiedenen Bibliotheken parallel laufen.
    """
    neu = copy.deepcopy(ort)
    if neu.get("forschungsauftrag") is not None:
        raise ValueError("Diese Bibliothek forscht bereits.")
    if gebiet not in spieldaten.forschungen():
        raise ValueError("Unbekanntes Forschungsgebiet.")
    bibliothek = gebaeude_wirkung.bibliothek_stufe([neu])
    ok, grund = forschungspfad.erfuellt(gebiet, wissen, bibliothek)
    if not ok:
        raise ValueError(grund)
    ziel = wissen.get(gebiet, 0) + 1
    for anderer in weitere_orte or ():
        a = (anderer or {}).get("forschungsauftrag")
        if a and a.get("gebiet") == gebiet and a.get("zielstufe") == ziel:
            raise ValueError(f"{gebiet} Stufe {ziel} forscht bereits eine andere Siedlung — "
                             f"zweimal dieselbe Stufe zahlt doppelt und bringt nichts.")
    kosten = forschung.kosten(ziel)
    neu = verbrauchen(neu, kosten, jetzt)
    stand = {gebiet: {"stufe": wissen.get(gebiet, 0), "auftrag": None}}
    # Material ist oben schon transaktional bezahlt → `forschung.starten` darf nichts abziehen.
    ok, grund = forschung.starten(gebiet, stand, jetzt, bibliothek > 0, None)
    if not ok:
        raise ValueError(grund)
    neu["forschungsauftrag"] = {"gebiet": gebiet, **stand[gebiet]["auftrag"]}
    return neu


def forschung_abschluss(ort: dict, wissen: dict, jetzt: float) -> tuple:
    """Eine abgelaufene Forschung **dieser Siedlung** verbuchen. Liefert ``(ort, wissen)``.

    Die Stufe steigt nur nach oben (`max`) — zweimal abschließen kann nichts doppeln —, der Auftrag
    wird gelöscht und die Fertigstellung ins `fertigjournal` geschrieben (Grundlage der Zielprüfung,
    Schritt 7).
    """
    neu, kenntnis = copy.deepcopy(ort), dict(wissen)
    a = neu.get("forschungsauftrag")
    if a and a["startzeit"] + a["dauer_stunden"] * 3600 <= jetzt:
        kenntnis[a["gebiet"]] = max(kenntnis.get(a["gebiet"], 0), a["zielstufe"])
        neu["forschungsauftrag"] = None
        neu["fertigjournal"].append({"zeit": jetzt, "art": "forschung", "name": a["gebiet"]})
    return neu, kenntnis


# ---------------------------------------------------------------------------
# Schritt 7 — Zielprüfung und Haltefenster, UNABHÄNGIG von den Originalpunkten
# (Entwurf Z. 688-715)
# ---------------------------------------------------------------------------
#
# Der Altmodus gewinnt über Punkte (`punkte.sieg_oder_niederlage`). Der Ökonomiemodus gewinnt
# über eine **versorgte Wirtschaft**: gute Karten, gedeckter Plan, gehaltene Reserve, echter
# Handel, beide Rollen, Ware **und** Forschung fertig — und das alles **ein volles
# Versorgungsfenster lang** (Haltefenster). Die Original-Punkteformeln bleiben unangetastet.
#
# Der Zweck ist ausdrücklich der **Ausschluss von Scheinsiegen**: wer nur Punkte farmt, Fracht
# sinnlos hin und her schiebt oder seine Schlüsselkarte verliert, erfüllt die Bedingungen nicht
# und verliert damit auch das Haltefenster wieder (Entwurf Z. 715).
#
# `reserve` (was ein Ort im Fenster zurücklegen WILL) wird je Ort erwartet — gesetzt wird es von
# der Aufstellung/Planung (Schritt 8/9). Fehlt es, gilt „keine Reserve gefordert": dann kann der
# Plan nicht gedeckt sein und das Ziel ist nicht erreicht (VORSCHLAG, konservativ — der Entwurf
# verlangt genau diese Strenge, damit ein Sieg nicht zufällig geschieht).


def zielstatus(orte: list, jetzt: float, haltestart=None) -> dict:
    """Sind die Bedingungen des Versorgungsziels erfüllt — und wie lange schon?

    Liefert ``sieg``, ``haltestart`` (None, wenn gerade nicht erfüllt — dann beginnt das
    Haltefenster neu), ``qualitaet``, ``deckung``, ``reserve``, ``handel``, ``armee`` und ``plan``.

    Gemessen wird **rückblickend**: die Deckung kommt aus dem tatsächlichen Produktionsjournal
    (`fensterproduktion`), der Handel aus dem Verbrauchsjournal (mindestens **zwei Rohstoffe**
    aus **zwei Orten** müssen wirklich verbraucht worden sein) — nicht aus einer Momentaufnahme.
    """
    orte = [o for o in (orte or []) if isinstance(o, dict)]
    # Ohne Orte liefert `kartenqualitaet` selbst schon `{"erfuellt": False, ...}` (eigene Zeile
    # dort) — die frühere Sonderbehandlung hier war unnötig und änderte die FORM des Feldes
    # (ohne "mittel"/"beste"). Fund der Abweichungsprüfung zu Schritt 7.
    q = kartenqualitaet([o["karte"] for o in orte])
    menge = fensterproduktion(orte, jetzt)
    plan = REGELN["plan"]
    reserviert = {r: sum((o.get("reserve") or {}).get(r, 0) for o in orte) for r in plan}
    plan_ok = bezahlbar(reserviert, plan)
    deckung = min((menge.get(r, 0) / n for r, n in plan.items() if n > 0), default=0.0)
    # VORSCHLAG (nicht belegt), bewusst vom Entwurf abweichend: der Entwurf schreibt hier
    # `all(...)` ohne die Ortsgrenze. Die Prüfung zu Schritt 7 hat dargelegt, dass das den SIEG
    # **nicht** ändert (ein leerer Verbund scheitert ohnehin an der Kartenqualität, die vier
    # Siedlungen verlangt) — die frühere Begründung „ein leerer Spielstand hätte gehalten" war
    # also falsch. Es bleibt eine **Anzeige**-Korrektur: `reserve` soll für einen Verbund ohne
    # Siedlungen nicht „gehalten" melden. Auf `ok`/`sieg` wirkt sie nicht. Daniel kann sie
    # streichen lassen; dann gilt wieder zeichengleich der Entwurf.
    reserve = bool(orte) and all(bezahlbar(o.get("vorraete") or {}, o.get("reserve") or {})
                                 for o in orte)
    ab = jetzt - REGELN["versorgung_stunden"] * 3600
    importe = {(o.get("id"), z["rohstoff"]) for o in orte
               for z in (o.get("verbrauchsjournal") or [])
               if ab < z["zeit"] <= jetzt and z["menge"] > 0}
    handel = len({r for _, r in importe}) >= 2 and len({i for i, _ in importe}) >= 2
    rollen = {einheiten.rolle(n) for o in orte for n, k in (o.get("einheiten") or {}).items()
              if k > 0}
    armee = "kaempfer" in rollen and "kundschafter" in rollen
    fertig = {z["art"] for o in orte for z in (o.get("fertigjournal") or [])}
    ok = (bool(q.get("erfuellt")) and plan_ok and deckung >= 1 and reserve and handel and armee
          and {"ware", "forschung"} <= fertig)
    start = (jetzt if haltestart is None else haltestart) if ok else None
    sieg = bool(ok and start is not None
                and jetzt - start >= REGELN["versorgung_stunden"] * 3600)
    # `plan` ist über den Entwurf hinaus — er nennt die Rückgabe ohne diesen Schlüssel, verlangt
    # aber „messbare Fehlgründe" (Z. 714). Nur eine Anzeige, keine Rechnung.
    return {"sieg": sieg, "haltestart": start, "qualitaet": q, "deckung": deckung,
            "reserve": reserve, "handel": handel, "armee": armee, "plan": plan_ok}


# ---------------------------------------------------------------------------
# Schritt 8b — bestätigter Fremdhandel: Angebot, beidseitige Sperre, Abschluss
# (Entwurf Z. 752 sowie Z. 878-940)
# ---------------------------------------------------------------------------
#
# Ein bestätigtes EINZELANGEBOT mit echter Handelskarawane — **keine** Netzfunktionen. Der alte
# `_trade`-Pfad (Gratisrohstoffe) wird dafür **nicht** weiterverwendet, sondern ersetzt.
#
# BELEGT (Handbuch 2009, Z. 1120 ff. — Zitat und Zeile in
# `docs/audits/handbuch_abgleich_2026-10-05.txt`): Handel zwischen eigenen Siedlungen ist belegt;
# für den Handel mit Fremden nennt das Handbuch die Handelskarawane und die Rückkehr MIT den Waren
# bei Ablehnung (S. 20). Der Preis wird beim Angebot festgelegt und danach nicht mehr verhandelt.
#
# Das Wesen der Transaktion ist die **Sperre**: Kaufpreis (Gold des Käufers) und Handelsgut (Lager
# des Verkäufers) verlassen ab dem Start ihre Lager und liegen AM VERTRAG. Erst die Ankunft der
# Karawane macht das Angebot wahr; kehrt sie ohne Annahme zurück, erhält jede Seite das Ihre
# vollständig zurück — samt der **Importherkunft** (dieselbe anteilige Sperrlogik wie in
# `transport_start`). So entstehen weder Gratisgewinne noch Geistergutschriften.
#
# Der Vertrag ist eine Mission mit `fremdvertrag=True`; gebucht wird er **ausschließlich** von
# `handel_abschluss` — `auftraege.spieldaten_anwenden` lässt ihn unberührt (genau wie einen
# Eigentransport). Die Ereignisschleife (Schritt 10) unterscheidet beide Wege an diesem Merkmal.
#
# **Die Annahme ist eine Entscheidung, kein Zufall** (Handbuch S. 20, belegt in
# `auftraege.auftragsarten`: „Bei Ablehnung kehrt die Karawane MIT den Waren zurück, Gold wird nie
# uebertragen."). Der Verkäuferort hält sie im Vertragsfeld `entscheidung` fest
# (`handel_entscheiden`): `True` nimmt an, `False` lehnt ab, `None` überlässt die Entscheidung der
# Ankunft — dann nimmt der Ort an, sobald die Karawane bei ihm steht und er noch seiner ist.
# Ohne dieses Feld wäre die belegte Ablehnungsregel **nicht erreichbar** (der Entwurfscode nahm
# immer an, sobald der Verkäuferort lebte) — gefunden beim Bau dieser Prüfdatei, eigener Zusatz,
# den Daniel streichen kann.
#
# WICHTIG (Entwurf Z. 939): Der **Sieg-Handelsnachweis** bleibt ausschließlich den eigenen
# Transporten vorbehalten. Ein Fremdkauf erhöht `importiert`/`verbrauchsjournal` des Käufers
# deshalb NICHT — sonst könnte man sich den Handelsnachweis einfach kaufen.


def handel_start(kaeufer: dict, verkaeufer: dict, einheitenbestand: dict, ware: str,
                 menge: int, preis: float, kanal: str, jetzt: float):
    """Ein bestätigtes Einzelangebot starten. Liefert ``(kaeufer_neu, verkaeufer_neu, vertrag)``.

    ``kanal`` ist ``"vorraete"`` (Rohstoff) oder ``"waren"``. Geprüft wird **vor** jeder Buchung:
    Kanal und Handelsgut, positives ganzzahliges Angebot, positiver endlicher Preis, fremder
    Besitzer, gleiche Dimension, Karawane vor Ort, beidseitige Deckung (Lager **und** Gold) und
    die Rückladung der Karawane. Jede Ablehnung ist ein ``ValueError`` — es wird nichts halb
    gebucht, die übergebenen Orte bleiben unverändert.
    """
    if kanal not in ("vorraete", "waren"):
        raise ValueError("Unbekannter Frachtkanal.")
    if type(menge) is not int or menge <= 0:
        raise ValueError("Ungültige Handelsmenge.")
    if isinstance(preis, bool) or not isinstance(preis, (int, float)) or not math.isfinite(preis) \
            or preis <= 0:
        raise ValueError("Ungültiger Preis.")
    if ware == "gold":
        raise ValueError("Gold ist kein Handelsgut, sondern die Gegenleistung.")
    if kaeufer["besitzer"] == verkaeufer["besitzer"]:
        raise ValueError("Eigener Warentransport braucht keinen Kaufvertrag.")
    if kaeufer["dimension"] != verkaeufer["dimension"]:
        raise ValueError("Fremde Dimension benötigt noch unbelegte Missionstarife.")
    if not einheitenbestand or any(type(n) is not int or n <= 0
                                   for n in einheitenbestand.values()):
        raise ValueError("Ungültige Karawanentruppe.")
    if any(kaeufer["einheiten"].get(n, 0) < m for n, m in einheitenbestand.items()):
        raise ValueError("Karawane fehlt vor Ort.")
    if verkaeufer[kanal].get(ware, 0) < menge:
        raise ValueError("Angebot nicht gedeckt: dem Verkäufer fehlt die Ware.")
    gold = menge * preis
    if kaeufer["vorraete"].get("gold", 0) < gold:
        raise ValueError("Angebot nicht gedeckt: dem Käufer fehlt das Gold.")
    d = abs(kaeufer["x"] - verkaeufer["x"]) + abs(kaeufer["y"] - verkaeufer["y"])
    liste = []
    ok, grund = auftraege.starten(liste, "handeln", einheitenbestand, kaeufer["id"],
                                  verkaeufer["id"], d, jetzt, {})
    if not ok:
        raise ValueError(grund)
    # Erst nach dem Auftragskern: die Karawanenpflicht steht BELEGT in `auftraege.auftragsarten`
    # („Nur Handelskarawanen") — diese Meldung ist besser als eine selbst erfundene. Gebucht ist
    # bis hierher nichts: `starten` füllt nur die Liste, die bei einer Ablehnung verworfen wird.
    if menge > auftraege.ladung_der_mission(einheitenbestand):
        raise ValueError("Kaufmenge übersteigt die Rückladung der Karawane.")
    k, v, vertrag = copy.deepcopy(kaeufer), copy.deepcopy(verkaeufer), liste[0]

    # Gegenleistung sperren: das Gold des Käufers (mit seinem Importanteil).
    goldbestand = k["vorraete"].get("gold", 0)
    sperrgold_import = 0.0 if goldbestand <= 0 else min(
        k["importiert"].get("gold", 0), gold * k["importiert"].get("gold", 0) / goldbestand)
    k["vorraete"]["gold"] = goldbestand - gold
    k["importiert"]["gold"] = max(0.0, k["importiert"].get("gold", 0) - sperrgold_import)

    # Handelsgut sperren: die Ware des Verkäufers (mit ihrem Importanteil, nur Rohstoffkanal).
    verkauft_import = {}
    if kanal == "vorraete":
        lager = v["vorraete"].get(ware, 0)
        anteil = 0.0 if lager <= 0 else menge * v["importiert"].get(ware, 0) / lager
        verkauft_import[ware] = anteil
        v["importiert"][ware] = max(0.0, v["importiert"].get(ware, 0) - anteil)
    v[kanal][ware] = v[kanal].get(ware, 0) - menge

    for n, z in einheitenbestand.items():
        k["einheiten"][n] = k["einheiten"].get(n, 0) - z

    vertrag.update({"fremdvertrag": True, "kaeufer": k["id"], "verkaeufer": v["id"],
                    "kaeufer_owner": k["besitzer"], "verkaeufer_owner": v["besitzer"],
                    "ware": ware, "menge": menge, "preis": float(preis), "kanal": kanal,
                    "angenommen": False, "abgerechnet": False, "entscheidung": None,
                    "sperrgold": gold, "sperrgold_import": sperrgold_import,
                    "verkauft_import": verkauft_import})
    vertrag["besitzer"] = k["besitzer"]
    return k, v, vertrag


def handel_entscheiden(vertrag: dict, angenommen: bool) -> dict:
    """Die Entscheidung des Verkäuferorts festhalten (vor dem Abschluss). Liefert den Vertrag.

    ``True`` nimmt das Angebot an, ``False`` lehnt es ab (belegt, Handbuch S. 20). Ein bereits
    abgerechneter Vertrag lässt sich nicht mehr entscheiden.
    """
    neu = copy.deepcopy(vertrag)
    if neu.get("abgerechnet"):
        raise ValueError("Der Vertrag ist bereits abgerechnet.")
    neu["entscheidung"] = bool(angenommen)
    return neu


def handel_abschluss(vertrag: dict, orte: dict, jetzt: float):
    """Ankunft und Rückkehr eines Fremdvertrags buchen — **genau einmal**. ``(orte, vertrag)``.

    * **Ankunft:** nimmt der Verkäuferort an (Feld `entscheidung`; ohne Entscheidung nimmt er an,
      sobald die Karawane bei ihm steht und der Ort noch seiner ist), wandert das gesperrte Gold
      zu ihm — mit der Importherkunft. Bei Ablehnung oder verlorenem Ort bleibt alles gesperrt.
    * **Rückkehr:** bei Annahme kommt die Ware beim Käufer an, bei Ablehnung kehren Gold **und**
      Ware vollständig zurück (belegte Regel, Handbuch S. 20); die Karawane kommt in beiden
      Fällen heim.
    * Ist der **Käuferort** verloren, bleibt das Gut AM VERTRAG — keine Geistergutschrift, keine
      Schenkung an einen neuen Besitzer (Entwurf Z. 924/932).
    """
    neu, m = copy.deepcopy(orte), copy.deepcopy(vertrag)
    kaeufer, verkaeufer = neu.get(m["kaeufer"]), neu.get(m["verkaeufer"])

    if jetzt >= m["ankunft"] and not m["angenommen"]:
        if m.get("entscheidung") is not False and verkaeufer is not None \
                and verkaeufer["besitzer"] == m["verkaeufer_owner"]:
            verkaeufer["vorraete"]["gold"] = verkaeufer["vorraete"].get("gold", 0) + m["sperrgold"]
            verkaeufer["importiert"]["gold"] = (verkaeufer["importiert"].get("gold", 0)
                                               + m["sperrgold_import"])
            m["sperrgold"], m["sperrgold_import"] = 0.0, 0.0
            m["angenommen"] = True

    if jetzt >= m["rueckkehr"] and not m["abgerechnet"]:
        if kaeufer is None or kaeufer["besitzer"] != m["kaeufer_owner"]:
            return neu, m          # Gut bleibt am Vertrag; ein späterer eigener Ort kann es noch erhalten.
        if m["angenommen"]:
            kaeufer[m["kanal"]][m["ware"]] = kaeufer[m["kanal"]].get(m["ware"], 0) + m["menge"]
            # Bewusst KEIN Eintrag in `importiert`: ein Fremdkauf ist kein eigener Handelsnachweis.
        else:
            kaeufer["vorraete"]["gold"] = kaeufer["vorraete"].get("gold", 0) + m["sperrgold"]
            kaeufer["importiert"]["gold"] = (kaeufer["importiert"].get("gold", 0)
                                            + m["sperrgold_import"])
            m["sperrgold"], m["sperrgold_import"] = 0.0, 0.0
            if verkaeufer is not None and verkaeufer["besitzer"] == m["verkaeufer_owner"]:
                verkaeufer[m["kanal"]][m["ware"]] = (verkaeufer[m["kanal"]].get(m["ware"], 0)
                                                     + m["menge"])
                if m["kanal"] == "vorraete":
                    verkaeufer["importiert"][m["ware"]] = (
                        verkaeufer["importiert"].get(m["ware"], 0)
                        + m["verkauft_import"].get(m["ware"], 0))
            else:
                # Verlorenes Verkäufergut bleibt vermerkt; nicht an einen neuen Besitzer schenken.
                m["verlorenes_sperrgut"] = {m["ware"]: m["menge"]}
        for n, z in m["einheiten"].items():
            kaeufer["einheiten"][n] = kaeufer["einheiten"].get(n, 0) + z
        m["abgerechnet"] = True
    return neu, m
