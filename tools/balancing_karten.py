"""Balancing-Test Teil 2: KARTEN, DOERFER UND PECH (Daniel, 31.10.2026).

Daniels Wortlaut: "Integriere in das balancing testing auch verschiedene karten doerfer die
spieler besitzen koennen bis zu welchen zeitpunkten und beachte dabei das man auch richtig pech
haben kann nur schlechte karten bekommt und deswegen sehr viele ressourcen verbraucht bevor man
eine richtige neue karte besiedelt sowas kann enormen einfluss auf das spielverhalten haben."

Was dieses Werkzeug rechnet (NUR aus Projektdaten und Kernfunktionen):
  1. Jede der 127 Originalkarten einzeln: freie Felder, bester Ausbauplan, Stundenertrag.
     Damit ist "beste / mittlere / schlechte Karte" eine MESSUNG, keine Behauptung.
  2. Was eine Gruendung kostet (Mindestbestand + Siedlerkarren + Wagenbau 1) und wie viele
     Spieltage man dafuer mit 1..5 Siedlungen braucht - samt Break-even der neuen Karte.
  3. ZWEI Ziehungsarten:
       A) FREIE WAHL (so ist der Code heute: `originalkarten.vorrat` gibt alle Karten frei)
       B) ZUFALL (so beschreibt es das Original, Handbuch Z. 313 "Karten per Zufall")
     Fuer B wird gewuerfelt (gleichverteilt ueber den freien Vorrat) und das PECH-Szenario
     ausdruecklich mitgerechnet (nur die schlechtesten Karten).
  4. Gates G-8/G-9 beurteilen: traegt auch eine Pech-Partie noch eine Gruendung?

Aufruf:
  python -X utf8 tools/balancing_karten.py                # Standardbericht
  python -X utf8 tools/balancing_karten.py --spiele 4000  # mehr Zufallspartien
  python -X utf8 tools/balancing_karten.py --seed 42
Ergebnis: Bericht auf stdout (Zahlen gehoeren nach docs/SPIELBALANCING_TEST.md).
"""
from __future__ import annotations

import argparse
import json
import os
import random
import statistics
import sys
from collections import Counter

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HIER, "src"))
sys.path.insert(0, os.path.join(HIER, "tools"))

import balancing_messung as B  # noqa: E402  (gleiche Quellen, keine zweite Rechnung)
import originalkarten as K     # noqa: E402
import spieloekonomie as O     # noqa: E402

DATEN = os.path.join(HIER, "data")


def lade(name):
    with open(os.path.join(DATEN, name), encoding="utf-8") as f:
        return json.load(f)


KATALOG = {e["id"]: e for e in lade(os.path.join("originalkarten", "katalog.json"))["karten"]}
UNITS = lade("units.json")["einheiten"]
GRUENDUNG = O.REGELN["gruendung"]
MAX_SIEDLUNGEN = B.MAX_SIEDLUNGEN


# ------------------------------------------------------------------ Karten einzeln
def karte_messen(kennung: str) -> dict:
    """Freie Felder, Ausbauplan und Stundenertrag EINER Karte (gleiche Methode wie Teil 1)."""
    karte = K.karte(kennung, seed="balancing")
    stat = {a: float(v) for a, v in (karte.get("zaehlung") or {}).items()}
    frei = sum(stat.values()) - stat.get("sumpf", 0.0)
    plan = B.ausbau_je_siedlung(stat, B.baubar_je_gebaeude(stat))
    ertrag = {str(a).lower(): v for a, v in B.ertrag_je_stunde(plan).items()}
    return {"id": kennung, "kategorie": KATALOG[kennung]["kategorie"], "name": KATALOG[kennung]["name"],
            "frei": frei, "sumpf": stat.get("sumpf", 0.0), "ertrag": ertrag,
            "achsen": O.relativ(karte)}


def alle_karten() -> dict:
    return {kid: karte_messen(kid) for kid in KATALOG}


def kategorie_tabelle(karten: dict) -> None:
    print("\n## 1. Die Karten selbst - gemessen, nicht behauptet")
    print("\n| Kategorie | Karten | freie Felder (min/median/max) | Nahrung/h | Holz/h | Gold/h |")
    print("|---|---|---|---|---|---|")
    for kat in ("beste", "mittlere", "schlechte"):
        werte = [k for k in karten.values() if k["kategorie"] == kat]
        if not werte:
            continue
        frei = [k["frei"] for k in werte]
        nah = [k["ertrag"].get("nahrung", 0.0) for k in werte]
        holz = [k["ertrag"].get("holz", 0.0) for k in werte]
        gold = [k["ertrag"].get("gold", 0.0) for k in werte]
        print("| %s | %d | %.0f / %.0f / %.0f | %.1f / %.1f / %.1f | %.1f / %.1f / %.1f | %.1f / %.1f / %.1f |" % (
            kat, len(werte),
            min(frei), statistics.median(frei), max(frei),
            min(nah), statistics.median(nah), max(nah),
            min(holz), statistics.median(holz), max(holz),
            min(gold), statistics.median(gold), max(gold)))

    sortiert = sorted(karten.values(), key=lambda k: k["ertrag"].get("gold", 0.0))
    print("\n**Gold - die Engstelle des Spiels (100 Krieger = 41 Spieltage Vollertrag):**")
    print("\n| | Karte | Kategorie | Gold/h | Nahrung/h | Holz/h | freie Felder |")
    print("|---|---|---|---|---|---|---|")
    for k in sortiert[:3] + sortiert[-3:]:
        print("| %s | %s (%s) | %s | %.2f | %.1f | %.1f | %.0f |" % (
            "schwaechste" if k in sortiert[:3] else "staerkste",
            k["id"], k["name"], k["kategorie"],
            k["ertrag"].get("gold", 0.0), k["ertrag"].get("nahrung", 0.0),
            k["ertrag"].get("holz", 0.0), k["frei"]))
    print("\n**Befund:** die Kategorie entscheidet NICHT ueber die Feldzahl (fast jede Karte hat "
          "80-100 freie Felder), sondern ueber die MISCHUNG - Gold reicht von 0 bis %.1f/h, "
          "Nahrung von %.1f bis %.1f/h." % (
              max(k["ertrag"].get("gold", 0.0) for k in karten.values()),
              min(k["ertrag"].get("nahrung", 0.0) for k in karten.values()),
              max(k["ertrag"].get("nahrung", 0.0) for k in karten.values())))


# --------------------------------------------------------------- Gruendungskosten
def gruendungs_bedarf() -> dict:
    """Was eine Gruendung SOFORT kosten muss (Ortslager) - alles aus Daten/Kernfunktionen."""
    preis, paket, minimum = O.gruendungskosten()
    karren = {k: float(v) for k, v in UNITS[GRUENDUNG["karren"]]["kosten"].items()
              if isinstance(v, (int, float)) and k != "siedler"}
    forschung = GRUENDUNG["forschung"]
    stufe = int(GRUENDUNG["stufe"])
    forschungskosten = 0.0
    for s in range(1, stufe + 1):
        for stoff, menge in (B.forschung.kosten(s) or {}).items():
            if str(stoff).lower() == "holz":
                forschungskosten += float(menge)
    gesamt = Counter()
    for quelle in (minimum, karren):
        for stoff, menge in quelle.items():
            gesamt[str(stoff).lower()] += float(menge)
    gesamt["holz"] += forschungskosten
    return {"preis": preis, "paket": paket, "minimum": minimum, "karren": karren,
            "forschung": (forschung, stufe, forschungskosten), "gesamt": dict(gesamt)}


def ausbau_kosten(plan: dict) -> dict:
    """Was der AUSBAU einer neuen Siedlung kostet (Preise aus `data/baupreise.json`)."""
    summe = Counter()
    for kennung, anzahl in plan.items():
        preis = O.BP.get(str(kennung)) or {}
        for stoff, menge in preis.items():
            if isinstance(menge, (int, float)) and stoff not in ("budget", "_belegt"):
                summe[str(stoff).lower()] += float(menge) * float(anzahl)
    return dict(summe)


def ausbau_tabelle(karten: dict) -> None:
    """Daniels Punkt: bis eine neue Karte WIRKLICH traegt, geht weit mehr als die Gruendungsgebuehr."""
    print("\n## 2b. Was der AUSBAU der neuen Siedlung kostet (das eigentliche Loch)")
    print("\nDer Ausbauplan je Karte sind 10 Haeuser, Bibliothek, Ausbildungs- und Werkstattgebaeude "
          "plus die Produktionsgebaeude auf allen freien Feldern. Die Preise sind belegt bzw. als "
          "Vorschlag gefuehrt (`data/baupreise.json`).")
    sortiert = sorted(karten.values(), key=lambda k: sum(k["ertrag"].values()))
    wahl = [("schwaechste Karte", sortiert[0]),
            ("mittlere Karte", sortiert[len(sortiert) // 2]),
            ("staerkste Karte", sortiert[-1])]
    print("\n| Karte | Kategorie | Holz | Stein | Metall | Leder | Wolle | Pferde |")
    print("|---|---|---|---|---|---|---|---|")
    werte = {}
    for titel, k in wahl:
        karte = K.karte(k["id"], seed="balancing")
        stat = {a: float(v) for a, v in (karte.get("zaehlung") or {}).items()}
        plan = B.ausbau_je_siedlung(stat, B.baubar_je_gebaeude(stat))
        kosten = ausbau_kosten(plan)
        werte[titel] = kosten
        print("| %s (%s) | %s | %s |" % (titel, k["name"], k["kategorie"], " | ".join(
            ("%.0f" % kosten[s]) if kosten.get(s) else "-"
            for s in ("holz", "stein", "metall", "leder", "wolle", "pferde"))))
    print("\n**Befund:** eine neue Siedlung ist mit der Gruendungsgebuehr NICHT bezahlt - der Ausbau "
          "kostet ein Vielfaches. Das ist der Grund, warum eine schwache Karte trotz gleicher Gebuehr "
          "viel teurer wird: man baut dieselben Gebaeude auf schlechteren Feldern.")


def gruendung_gesamt(karten: dict, bedarf: dict) -> None:
    """Gruendungsgebuehr + Ausbau der ersten Stufe = was WIRKLICH investiert wird."""
    sortiert = sorted(karten.values(), key=lambda k: sum(k["ertrag"].values()))
    for titel, k in (("schwaechste Karte", sortiert[0]), ("staerkste Karte", sortiert[-1])):
        karte = K.karte(k["id"], seed="balancing")
        stat = {a: float(v) for a, v in (karte.get("zaehlung") or {}).items()}
        plan = B.ausbau_je_siedlung(stat, B.baubar_je_gebaeude(stat))
        kosten = ausbau_kosten(plan)
        gesamt = {s: bedarf["gesamt"].get(s, 0.0) + kosten.get(s, 0.0) for s in
                  set(bedarf["gesamt"]) | set(kosten)}
        print("\n- **%s (%s, %s):** Ausbau allein %s · mit Gebuehr/Karren/Forschung %s" % (
            titel, k["id"], k["kategorie"],
            ", ".join("%s %.0f" % (s, v) for s, v in sorted(kosten.items()) if v >= 1),
            ", ".join("%s %.0f" % (s, v) for s, v in sorted(gesamt.items()) if v >= 1)))


def tage_fuer_bedarf(bedarf: dict, ertrag_tag: dict) -> float:
    """Spieltage, bis das LOKALLAGER den Bedarf deckt - der ENGSTE Rohstoff zaehlt."""
    tage = 0.0
    for stoff, menge in bedarf.items():
        if stoff in ("siedler", "pferde") or menge <= 0:
            continue
        rate = ertrag_tag.get(stoff, 0.0)
        if rate <= 0:
            return float("inf")
        tage = max(tage, menge / rate)
    return tage


def gruendungs_tabelle(karten: dict, bedarf: dict) -> dict:
    print("\n## 2. Was eine Gruendung kostet und wann sie sich lohnt")
    print("\n| Posten | Holz | Stein | Nahrung | Metall | Leder | Wolle | Pferde |")
    print("|---|---|---|---|---|---|---|---|")
    for titel, quelle in (("Mindestbestand (Ortslager)", bedarf["minimum"]),
                          ("Siedlerkarren (%s)" % GRUENDUNG["karren"], bedarf["karren"]),
                          ("Forschung %s %d" % (bedarf["forschung"][0], bedarf["forschung"][1]),
                           {"holz": bedarf["forschung"][2]}),
                          ("**Summe**", bedarf["gesamt"])):
        print("| %s | %s |" % (titel, " | ".join(
            ("%.0f" % quelle.get(s, 0)) if quelle.get(s, 0) else "-"
            for s in ("holz", "stein", "nahrung", "metall", "leder", "wolle", "pferde"))))

    mittel = sorted(karten.values(), key=lambda k: k["ertrag"].get("gold", 0.0))[len(karten) // 2]
    # "Beste Karte" heisst hier: das hoechste Gesamtertrag, das ALLE Gruendungsposten selbst erzeugt -
    # sonst waere die Zahl unendlich (eine reine Holzkarte kann keine Karren bauen).
    noetig = [s for s in bedarf["gesamt"] if s not in ("siedler",)]
    kandidaten = [k for k in karten.values() if all(k["ertrag"].get(s, 0.0) > 0 for s in noetig)]
    gute = max(kandidaten, key=lambda k: sum(k["ertrag"].values())) if kandidaten else None
    print("\n**WICHTIG - Lesart der Tage:** gerechnet ist der VOLLERTRAG ab Tag 1 (jede Siedlung hat "
          "sofort den ganzen Ausbauplan). Das ist eine **Untergrenze**: in Wahrheit muessen Gebaeude "
          "erst gebaut und Forschungen bezahlt werden. Die Anlaufzeit fehlt hier bewusst und steht als "
          "offener Punkt in `docs/SPIELBALANCING_TEST.md`.")
    print("\n| Siedlungen | Reichsertrag/Tag (mittlere Karte dazu) | Tage bis zur naechsten Gruendung "
          "| mit bester Karte (alle Posten gedeckt) |")
    print("|---|---|---|---|")
    ergebnis = {}
    for anzahl in range(1, MAX_SIEDLUNGEN):
        tag = {s: mittel["ertrag"].get(s, 0.0) * 24 * anzahl for s in bedarf["gesamt"]}
        tag_best = ({s: gute["ertrag"].get(s, 0.0) * 24 * anzahl for s in bedarf["gesamt"]}
                    if gute else {})
        d_mittel = tage_fuer_bedarf(bedarf["gesamt"], tag)
        d_best = tage_fuer_bedarf(bedarf["gesamt"], tag_best) if gute else float("inf")
        ergebnis[anzahl] = (d_mittel, d_best)
        print("| %d → %d | %s | **%.1f** | %s |" % (
            anzahl, anzahl + 1,
            ", ".join("%s %.0f" % (s, tag[s]) for s in ("holz", "stein", "nahrung") if s in tag),
            d_mittel, ("%.1f" % d_best) if gute else "keine Karte deckt alles"))
    return ergebnis


# ------------------------------------------------------------------- Ziehungsarten
def ertrag_von(karten_liste) -> dict:
    summe = Counter()
    for k in karten_liste:
        for stoff, menge in k["ertrag"].items():
            summe[stoff] += menge
    return dict(summe)


def pech_und_glueck(karten: dict, bedarf: dict, spiele: int, seed: int) -> dict:
    print("\n## 3. Zwei Ziehungsarten - freie Wahl (Code heute) gegen Zufall (Original)")
    frei_pool = [k for kid, k in sorted(karten.items()) if kid != K.START_ID]
    rang = sorted(frei_pool, key=lambda k: sum(k["ertrag"].values()))
    schlechteste = rang[:MAX_SIEDLUNGEN - 1]
    beste = rang[-(MAX_SIEDLUNGEN - 1):]

    print("\n| Szenario | Reichsertrag/Tag (5 Koloniekarten) | Gold/Tag | Tage bis zur letzten Gruendung |")
    print("|---|---|---|---|")
    for titel, auswahl in (("PECH: nur die %d schlechtesten Karten" % len(schlechteste), schlechteste),
                           ("GLUECK: die %d besten Karten" % len(beste), beste)):
        e = ertrag_von(auswahl + [karten[K.START_ID]])
        tag = {s: v * 24 for s, v in e.items()}
        # bei Pech/Glick: jede neue Siedlung erst, wenn der Bestand reicht
        tage = 0.0
        for n in range(1, MAX_SIEDLUNGEN):
            zwischen = {s: v * n for s, v in tag.items()}
            tage += tage_fuer_bedarf(bedarf["gesamt"], zwischen)
        print("| %s | %s | %.0f | **%.0f** |" % (
            titel, ", ".join("%s %.0f" % (s, tag.get(s, 0)) for s in ("holz", "stein", "nahrung")),
            tag.get("gold", 0.0), tage))

    zufall = random.Random(seed)
    lagen, gold, tage_liste = [], [], []
    for _ in range(spiele):
        gezogen = zufall.sample(frei_pool, MAX_SIEDLUNGEN - 1)
        e = ertrag_von(gezogen + [karten[K.START_ID]])
        tag = {s: v * 24 for s, v in e.items()}
        lagen.append(sum(tag.values()))
        gold.append(tag.get("gold", 0.0))
        t = 0.0
        for n in range(1, MAX_SIEDLUNGEN):
            t += tage_fuer_bedarf(bedarf["gesamt"], {s: v * n for s, v in tag.items()})
        tage_liste.append(t)

    def q(werte, anteil):
        return sorted(werte)[max(0, min(len(werte) - 1, int(anteil * (len(werte) - 1))))]

    print("\n**Zufall (%d Partien, gleichverteilt aus den %d freien Originalkarten):**" % (
        spiele, len(frei_pool)))
    print("\n| Kennzahl | 5 % schlechteste | Median | 5 % beste |")
    print("|---|---|---|---|")
    print("| Reichsertrag/Tag (6 Siedlungen, Summe) | %.0f | %.0f | %.0f |" % (
        q(lagen, 0.05), statistics.median(lagen), q(lagen, 0.95)))
    print("| Gold/Tag | %.0f | %.0f | %.0f |" % (
        q(gold, 0.05), statistics.median(gold), q(gold, 0.95)))
    print("| Spieltage bis zur 6. Siedlung | %.0f | %.0f | %.0f |" % (
        q(tage_liste, 0.05), statistics.median(tage_liste), q(tage_liste, 0.95)))
    return {"pech_tage": tage_liste and max(tage_liste), "median_tage": statistics.median(tage_liste)}


# ------------------------------------------------------------------------- Gates
def gates(karten: dict, bedarf: dict, ergebnis: dict) -> None:
    print("\n## 4. Gates fuer Karten und Pech")
    mittel = sorted(karten.values(), key=lambda k: k["ertrag"].get("gold", 0.0))[len(karten) // 2]
    start = karten[K.START_ID]
    tag1 = {s: start["ertrag"].get(s, 0.0) * 24 for s in bedarf["gesamt"]}
    d1 = tage_fuer_bedarf(bedarf["gesamt"], tag1)
    print("\n| Gate | Bedingung | Heute |")
    print("|---|---|---|")
    print("| G-8 Erste Gruendung | die STARTKARTE allein traegt den Gruendungsbedarf in <= 10 Spieltagen | %s (%.1f Tage) |" % (
        "**erfuellt**" if d1 <= 10 else "**verfehlt**", d1))
    print("| G-9 Pech nicht ruinoes | auch die schlechteste Kartenlage traegt die 6. Siedlung in <= 120 Spieltagen | %s |" % (
        "**erfuellt**" if (ergebnis.get("pech_tage") or 0) <= 120 else "**verfehlt**"))
    print("\n**Regel:** ein verfehltes Gate ist kein Codefehler, sondern eine offene Balancing-Frage "
          "an Daniel (`docs/FRAGEN_AN_DANIEL_<TTMM>.md`).")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--spiele", type=int, default=2000)
    p.add_argument("--seed", type=int, default=20261031)
    a = p.parse_args()
    print("# Balancing-Test Teil 2 - Karten, Doerfer und Pech (Nebelseetal Remake)")
    karten = alle_karten()
    print("\nGemessen: %d Originalkarten (davon 1 feste Startkarte `%s`), %d Siedlungen Maximum."
          % (len(karten), K.START_ID, MAX_SIEDLUNGEN))
    kategorie_tabelle(karten)
    bedarf = gruendungs_bedarf()
    ergebnis = gruendungs_tabelle(karten, bedarf)
    ausbau_tabelle(karten)
    gruendung_gesamt(karten, bedarf)
    ergebnis.update(pech_und_glueck(karten, bedarf, a.spiele, a.seed))
    gates(karten, bedarf, ergebnis)
    return 0


if __name__ == "__main__":
    sys.exit(main())
