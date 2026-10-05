"""Pruefung der neuen Oekonomie-Regeldaten (Schritt 1 des Oekonomie-Pakets).

Gegenstand: die DATEN, noch keine Aktivierung. Geprueft wird
  * `data/gelaende.json` → `kartenvorrat` (Startkarte + neun Koloniekarten) **exakt** gegen
    Tabelle B in `docs/audits/entwurf_spieloekonomie_sol_2026-10-05.txt` (Z. 68-80),
    * `data/spieloekonomie.json` (neue Regeldaten) samt Ableitung der Gruendungszahlen aus
    den ECHTEN Quellen (`data/baupreise.json`, `data/units.json`),
  * dass die ALTEN Kartenliste (`kartentypen.listen`) und die 21 Forschungen unangetastet sind.

Aufruf:  python -X utf8 tests/test_spieloekonomie.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import abschnitt, bericht, check, import_src, projektwurzel

ROOT, SRC = import_src()
import spieldaten as S
import spieloekonomie as O

DATA = os.path.join(projektwurzel(), "data")
G = json.loads(open(os.path.join(DATA, "gelaende.json"), encoding="utf-8").read())
E = json.loads(open(os.path.join(DATA, "spieloekonomie.json"), encoding="utf-8").read())
BP = json.loads(open(os.path.join(DATA, "baupreise.json"), encoding="utf-8").read())["preise"]
U = json.loads(open(os.path.join(DATA, "units.json"), encoding="utf-8").read())["einheiten"]

ARTEN = ["grasland", "steppe", "wald", "huegel", "berg", "nebelsee", "sumpf"]
SPERRFELDER = G["regeln"]["sperrfelder"]
MASS = G["kartenmass"]["spalten"] * G["kartenmass"]["zeilen"]
MINDEST = {k: v for k, v in G["regeln"]["mindestbesatz"].items() if not k.startswith("_")}

# Tabelle B, woertlich (Reihenfolge: grasland, steppe, wald, huegel, berg, nebelsee, sumpf).
TABELLE_B = {
    "start":        (8, 8, 8, 7, 7, 2, 16),
    "ausgleich_a":  (9, 7, 8, 6, 8, 2, 16),
    "ausgleich_b":  (7, 9, 9, 7, 6, 2, 16),
    "ausgleich_c":  (8, 8, 7, 8, 7, 2, 16),
    "holz":         (3, 2, 28, 2, 4, 1, 16),
    "minen":        (3, 2, 2, 10, 22, 1, 16),
    "farmen":       (27, 6, 2, 2, 2, 1, 16),
    "holz_minen":   (3, 2, 16, 5, 13, 1, 16),
    "holz_farmen":  (17, 2, 16, 2, 2, 1, 16),
    "minen_farmen": (17, 2, 2, 5, 13, 1, 16),
}


def als_tupel(gewichte: dict) -> tuple:
    return tuple(int(gewichte.get(a, 0)) for a in ARTEN)


# ==========================================================================
abschnitt("1. kartenvorrat ist vorhanden und in der richtigen Form")

check("data/gelaende.json hat den Schluessel kartenvorrat", "kartenvorrat" in G)
vorrat = G.get("kartenvorrat") or {}
check("kartenvorrat nennt eine Startkarte", "start" in vorrat)
check("kartenvorrat nennt neun Koloniekarten",
      isinstance(vorrat.get("kolonien"), list) and len(vorrat["kolonien"]) == 9,
      f"{len(vorrat.get('kolonien') or [])} Koloniekarten")
check("kartenvorrat ist als VORSCHLAG mit Herkunft gekennzeichnet",
      "VORSCHLAG" in str(vorrat.get("_herkunft", ""))
      and "entwurf_spieloekonomie_sol_2026-10-05" in str(vorrat.get("_herkunft", "")))

alle = [vorrat["start"]] + list(vorrat["kolonien"])
kennungen = [k["id"] for k in alle]
check("die zehn Kennungen sind genau die der Tabelle B",
      kennungen == list(TABELLE_B), str(kennungen))
check("keine Kennung doppelt", len(set(kennungen)) == len(kennungen))

# ==========================================================================
abschnitt("2. Jede Karte traegt exakt die Feldkontingente der Tabelle B")

for eintrag in alle:
    kennung = eintrag["id"]
    soll = TABELLE_B[kennung]
    gewichte = eintrag["gewichte"]
    check(f"{kennung}: genau die sieben Geländearten",
          set(gewichte) == set(ARTEN), str(sorted(gewichte)))
    check(f"{kennung}: die Werte stimmen Zeichen fuer Zeichen",
          als_tupel(gewichte) == soll, f"{als_tupel(gewichte)} != {soll}")

# ==========================================================================
abschnitt("3. Kontingente, Sperrfelder und Mindestbesatz halten")

for eintrag in alle:
    kennung = eintrag["id"]
    t = als_tupel(eintrag["gewichte"])
    check(f"{kennung}: Summe aller Felder = {MASS}", sum(t) == MASS, str(sum(t)))
    check(f"{kennung}: Summe ohne Sumpf = 40 bebaubar",
          sum(t[:6]) == MASS - SPERRFELDER, str(sum(t[:6])))
    check(f"{kennung}: Sumpf = {SPERRFELDER} Sperrfelder", t[6] == SPERRFELDER, str(t[6]))
    fehlt = {a: (MINDEST[a], t[i]) for i, a in enumerate(ARTEN[:6])
             if a in MINDEST and t[i] < MINDEST[a]}
    check(f"{kennung}: Mindestbesatz erfuellt", not fehlt, str(fehlt))

check("die Startkarte hat von jedem der neun Rohstoffe Potenzial (alle sechs Arten besetzt)",
      all(w > 0 for w in als_tupel(vorrat["start"]["gewichte"])[:6]))
spez = [e["id"] for e in vorrat["kolonien"]
        if min(als_tupel(e["gewichte"])[:6]) <= 2]
check("die spezialisierten Karten sind wirklich einseitig (mindestens eine Achse fast leer)",
      len(spez) >= 3, str(spez))

# ==========================================================================
abschnitt("4. spieloekonomie.json — Schluessel, Zahlen, Herkunft")

for schluessel in ("version", "baukunst_mindeststufe", "gruendung", "vergabe_stunden",
                   "versorgung_stunden", "mindestsiedlungen", "spezialistenfaktor",
                   "portfoliofaktor", "plan", "kartenpreisgrenzen", "vorratspreisgrenzen",
                   "pilot_ausbildung_minuten", "pilot_waren_minuten", "bots", "bot_startplan"):
    check(f"spieloekonomie.json kennt '{schluessel}'", schluessel in E)

check("Version ist oekonomie-1", E["version"] == "oekonomie-1", str(E["version"]))
check("Herkunft nennt den Entwurf und VORSCHLAG",
      "VORSCHLAG" in E["_herkunft"] and "entwurf_spieloekonomie_sol_2026-10-05" in E["_herkunft"])
check("vier Siedlungen sind das Minimum (Vorgabe Daniel)",
      E["mindestsiedlungen"] == 4, str(E["mindestsiedlungen"]))
check("Spezialistenschwelle 1,4", abs(E["spezialistenfaktor"] - 1.4) < 1e-9)
check("Portfoliofaktor 1,0", abs(E["portfoliofaktor"] - 1.0) < 1e-9)
check("Vergabe- und Versorgungsfenster sind 24 Spielstunden",
      E["vergabe_stunden"] == 24 and E["versorgung_stunden"] == 24)
check("Preisgrenzen wie im Entwurf (Karte 0,5/4 · Vorrat 0,5/2)",
      E["kartenpreisgrenzen"] == [0.5, 4.0] and E["vorratspreisgrenzen"] == [0.5, 2.0],
      f"{E['kartenpreisgrenzen']} / {E['vorratspreisgrenzen']}")

check("der Planbedarf nennt genau die neun Rohstoffe",
      set(E["plan"]) == {"holz", "stein", "metall", "mana", "nahrung", "gold",
                         "wolle", "leder", "pferde"},
      str(sorted(E["plan"])))
check("Gold ist der groesste Planposten (300)",
      E["plan"]["gold"] == 300 and max(E["plan"].values()) == 300, str(E["plan"]))
check("die Pilotzeiten sind 20 Minuten (Ware und Ausbildung)",
      E["pilot_waren_minuten"] == 20 and E["pilot_ausbildung_minuten"] == 20)

# ==========================================================================
abschnitt("5. Die Gruendungszahlen sind aus den ECHTEN Quellen ableitbar (nachgerechnet)")

haus = {k: float(v) for k, v in BP["haus"].items() if isinstance(v, (int, float))}
check("Hauspreis ist belegt 80 Holz, 50 Stein",
      haus == {"holz": 80.0, "stein": 50.0}, str(haus))

r = E["gruendung"]
preis = {k: v * r["hausmultiplikator"] for k, v in haus.items()}
paket = {k: v * r["reserve_hausmultiplikator"] for k, v in haus.items()}
preis["nahrung"] = U[r["karren"]]["kosten"]["nahrung"] * r["nahrung_karrenanteil"]
paket["nahrung"] = U[r["reserve_nahrung_einheit"]]["kosten"]["nahrung"]
minimum = {k: preis.get(k, 0) + paket.get(k, 0) for k in set(preis) | set(paket)}

check("Gruendungsgebuehr ergibt 320 Holz / 200 Stein / 150 Nahrung",
      preis == {"holz": 320.0, "stein": 200.0, "nahrung": 150.0}, str(preis))
check("Startpaket ergibt 160 Holz / 100 Stein / 100 Nahrung",
      paket == {"holz": 160.0, "stein": 100.0, "nahrung": 100.0}, str(paket))
check("Mindestbestand ergibt 480 Holz / 300 Stein / 250 Nahrung",
      minimum == {"holz": 480.0, "stein": 300.0, "nahrung": 250.0}, str(minimum))
check("der Siedlerkarren ist der belegte Karren (Wagenbau 1 erforderlich)",
      r["karren"] == "Siedlerkarren" and r["forschung"] == "Wagenbau" and r["stufe"] == 1)
check("der Siedlerkarren kostet belegt 200/80/150/100/4/5/300",
      U["Siedlerkarren"]["kosten"] == {"holz": 200, "metall": 80, "leder": 150, "wolle": 100,
                                       "pferde": 4, "siedler": 5, "nahrung": 300},
      str(U["Siedlerkarren"]["kosten"]))

# ==========================================================================
abschnitt("6. Bot-Stufen: leicht / mittel / schwer (Vorgabe Daniel)")

check("genau drei Bot-Stufen", set(E["bots"]) == {"leicht", "mittel", "schwer"}, str(set(E["bots"])))
check("leicht gruendet nicht", E["bots"]["leicht"]["gruenden"] is False)
check("mittel und schwer gruenden", E["bots"]["mittel"]["gruenden"] is True
      and E["bots"]["schwer"]["gruenden"] is True)
check("schwer plant am haeufigsten (1 Stunde), leicht am seltensten (24)",
      E["bots"]["schwer"]["bewerten_stunden"] == 1
      and E["bots"]["leicht"]["bewerten_stunden"] == 24)
check("kein Ablehnungsnutzen geschenkt (alle 0,0)",
      all(float(E["bots"][s]["ablehnungsnutzen"]) == 0.0 for s in E["bots"]))
check("der Bot-Startplan nennt Grundbau und Ausbau",
      "grundbau" in E["bot_startplan"] and "ausbau" in E["bot_startplan"])
check("der Grundbau entspricht dem nachgerechneten Plan E",
      E["bot_startplan"]["grundbau"] == {"holzfaeller": 2, "steinmetz": 2, "jaeger": 1,
                                         "bibliothek": 1},
      str(E["bot_startplan"]["grundbau"]))

# ==========================================================================
abschnitt("7. Nichts Bestehendes wurde umgebogen (Altmodus bleibt)")

typen = G["kartentypen"]["listen"]
check("die alten kartentypen.listen bleiben bei fuenf Typen", len(typen) == 5, str(len(typen)))
check("die alten Kartentypen behalten ihre Gewichte als Haeufigkeiten (nicht ueberschrieben)",
      all("haeufigkeit" in t and "gewichte" in t for t in typen))
check("der neue Vorrat ist NICHT in kartentypen.listen eingetragen",
      "kartenvorrat" not in G["kartentypen"])
check("die 21 Originalforschungen sind unveraendert", len(S.forschungen()) == 21,
      str(len(S.forschungen())))
check("es gibt KEIN neues Forschungsgebiet (keine erfundene 22. Forschung)",
      "vermessung" not in {k.lower() for k in S.forschungen()},
      str([k for k in S.forschungen() if "vermess" in k.lower()]))
check("das Kartenmass ist unveraendert 8 x 7 = 56, 40 bebaubar",
      G["kartenmass"]["spalten"] == 8 and G["kartenmass"]["zeilen"] == 7
      and G["kartenmass"]["felder"] == 56 and G["kartenmass"]["bauplaetze"] == 40,
      str(G["kartenmass"]))
check("Sperrfelder bleiben 16", SPERRFELDER == 16, str(SPERRFELDER))


# ==========================================================================
abschnitt("8. Der deterministische Kern (src/spieloekonomie.py, Schritt 2)")


def wirft(fn) -> str:
    """Name der Ausnahme, oder leerer Text, wenn nichts geworfen wurde."""
    try:
        fn()
    except Exception as e:  # noqa: BLE001
        return type(e).__name__
    return ""


SAATEN = ["kern-1", "kern-2", "kern-3", "referenz"]
for saat in SAATEN:
    start_karte = O.startkarte(saat, "spieler")
    kartenliste = [start_karte] + [v["karte"] for v in O.vorrat(saat).values()]
    check(f"{saat}: Startkarte + neun Koloniekarten", len(kartenliste) == 10, str(len(kartenliste)))
    for k in kartenliste:
        check(f"{saat}/{k['typ']}: 56 Felder", k["felder"] == 56 and len(k["raster"]) == 56)
        check(f"{saat}/{k['typ']}: 40 bebaubar", k["bauplaetze"] == 40, str(k["bauplaetze"]))
        check(f"{saat}/{k['typ']}: 16 Sumpf", k["raster"].count("sumpf") == 16,
              str(k["raster"].count("sumpf")))
        check(f"{saat}/{k['typ']}: Mindestbesatz eingehalten",
              all(k["raster"].count(a) >= MINDEST[a] for a in MINDEST),
              str({a: k["raster"].count(a) for a in MINDEST}))
        check(f"{saat}/{k['typ']}: Zaehlung = Tabelle B",
              k["zaehlung"] == {a: TABELLE_B[k["typ"]][i] for i, a in enumerate(ARTEN)})

_gew = dict(vorrat["start"]["gewichte"])
check("gleiche Saat ergibt dasselbe Raster",
      O.feste_karte("gleich", vorrat["start"])["raster"]
      == O.feste_karte("gleich", vorrat["start"])["raster"])
check("andere Saat ergibt ein anderes Raster",
      O.feste_karte("gleich", vorrat["start"])["raster"]
      != O.feste_karte("anders", vorrat["start"])["raster"])
check("ein falsches Kartenmass wird abgewiesen",
      wirft(lambda: O.feste_karte("x", {"id": "x", "name": "x",
                                        "gewichte": {**_gew, "wald": 29}})) == "ValueError")
check("ein falsches Sumpfkontingent wird abgewiesen",
      wirft(lambda: O.feste_karte("x", {"id": "x", "name": "x",
                                        "gewichte": {**_gew, "grasland": 9, "sumpf": 15}})) == "ValueError")
check("ein verletzter Mindestbesatz wird abgewiesen",
      wirft(lambda: O.feste_karte("x", {"id": "x", "name": "x",
                                        "gewichte": {**_gew, "wald": 1, "grasland": 9}})) == "ValueError")

# --------------------------------------------------------------------------
abschnitt("9. Achsen, Kartenqualitaet und der Siegfilter (Entwurf Abschnitt A/B)")

start = O.startkarte("fest", "spieler")
v = O.vorrat("fest")


def k(kennung):
    return v[kennung]["karte"]


check("Startkarte: Achsen sind (48, 42, 48) — die Startreferenz des Entwurfs",
      O.achsen(start) == (48, 42, 48), str(O.achsen(start)))
check("Startkarte relativ = (1, 1, 1)", all(abs(x - 1) < 1e-9 for x in O.relativ(start)),
      str(O.relativ(start)))

q1 = O.kartenqualitaet([start])
check("eine Karte allein erfuellt den Verbund nicht (mindestens vier Siedlungen)",
      q1["erfuellt"] is False)
q2 = O.kartenqualitaet([start, k("ausgleich_a"), k("ausgleich_b"), k("ausgleich_c")])
check("Start plus NUR ausgeglichene Karten scheitert am Spezialistennachweis",
      q2["erfuellt"] is False, str(q2["beste"]))
check("und der beste Holzfaktor ist genau 1,125 (Entwurf Z. 31)",
      abs(q2["beste"][0] - 1.125) < 1e-9, str(q2["beste"][0]))
q3 = O.kartenqualitaet([start, k("holz"), k("minen"), k("farmen")])
check("Start + Holz + Minen + Farmen besteht die Kartenpruefung", q3["erfuellt"] is True)
check("Achsenmittel = (1,0208; 1,0833; 1,0417) wie im Entwurf (Z. 99)",
      all(abs(a - b) < 5e-5 for a, b in zip(q3["mittel"], (1.0208, 1.0833, 1.0417))),
      str(q3["mittel"]))
check("bester Einzelwert = (2,4167; 2,5714; 2,5) wie im Entwurf (Z. 99)",
      all(abs(a - b) < 5e-5 for a, b in zip(q3["beste"], (2.4167, 2.5714, 2.5))),
      str(q3["beste"]))
q4 = O.kartenqualitaet([start, k("holz_minen"), k("holz_farmen"), k("minen_farmen")])
check("Start + die drei Mischungen besteht ebenfalls", q4["erfuellt"] is True)
check("und liefert die Spezialistennachweise 1,4167 / 1,4762 / 1,5 (Entwurf Z. 101)",
      all(abs(a - b) < 5e-5 for a, b in zip(q4["beste"], (1.4167, 1.4762, 1.5))),
      str(q4["beste"]))
check("der Kartennutzen waechst, wenn die Karte eine Luecke fuellt",
      O.kartennutzen([start, k("holz")], k("minen")) > O.kartennutzen([start, k("holz")], k("ausgleich_a")))

# --------------------------------------------------------------------------
abschnitt("10. Gruendung, Absicht und gemeinsame Vergabe (Entwurf Abschnitt C)")

preis, paket, minimum = O.gruendungskosten()
check("Gebuehr 320 Holz / 200 Stein / 150 Nahrung",
      preis == {"holz": 320.0, "stein": 200.0, "nahrung": 150.0}, str(preis))
check("Startpaket 160 Holz / 100 Stein / 100 Nahrung",
      paket == {"holz": 160.0, "stein": 100.0, "nahrung": 100.0}, str(paket))
check("Mindestbestand 480 Holz / 300 Stein / 250 Nahrung",
      minimum == {"holz": 480.0, "stein": 300.0, "nahrung": 250.0}, str(minimum))

freie = O.vorrat("vergabe")
quelle = {"id": "A", "besitzer": "spieler", "siedlungsgrenze": 6,
          "einheiten": {O.REGELN["gruendung"]["karren"]: 1},
          "vorraete": {"holz": 1000.0, "stein": 1000.0, "nahrung": 1000.0}}
a = O.absicht(quelle, "holz", [start], freie, {"Wagenbau": 1}, 0)
check("zulaessige Absicht wird angenommen", a["karte_id"] == "holz" and a["runde"] == 0)
check("das Sperrgut ist der Mindestbestand", a["sperrgut"] == minimum, str(a["sperrgut"]))
check("die Absicht traegt einen Nutzen", isinstance(a["nutzen"], float))


def absicht_mit(**aenderung):
    q = dict(quelle)
    q.update(aenderung)
    return q


check("ohne Siedlerkarren wird abgelehnt",
      wirft(lambda: O.absicht(absicht_mit(einheiten={}), "holz", [start], freie,
                              {"Wagenbau": 1}, 0)) == "ValueError")
check("ohne Wagenbau-Forschung wird abgelehnt",
      wirft(lambda: O.absicht(quelle, "holz", [start], freie, {}, 0)) == "ValueError")
check("ohne Mindestbestand wird abgelehnt",
      wirft(lambda: O.absicht(absicht_mit(vorraete={"holz": 479.0, "stein": 1000.0,
                                                    "nahrung": 1000.0}),
                              "holz", [start], freie, {"Wagenbau": 1}, 0)) == "ValueError")
check("auf eine vergebene Karte wird abgelehnt",
      wirft(lambda: O.absicht(quelle, "holz", [start],
                              {**freie, "holz": {"karte": k("holz"), "besitzer": "bot"}},
                              {"Wagenbau": 1}, 0)) == "ValueError")
check("ueber die Siedlungsgrenze wird abgelehnt",
      wirft(lambda: O.absicht(absicht_mit(siedlungsgrenze=1), "holz", [start], freie,
                              {"Wagenbau": 1}, 0)) == "ValueError")


def absicht_von(besitzer, karte_id, nutzen, runde=0):
    return {"quelle": besitzer, "besitzer": besitzer, "karte_id": karte_id, "runde": runde,
            "sperrgut": minimum, "preis": preis, "paket": paket, "nutzen": nutzen}


erg = O.vergabe([absicht_von("B", "holz", 1.0), absicht_von("A", "holz", 2.0)],
                O.vorrat("v2"), "saat", 0)
gewinner = [x["besitzer"] for x, ok in erg if ok]
verlierer = [x["besitzer"] for x, ok in erg if not ok]
check("hoeherer Nutzen gewinnt die umkaempfte Karte", gewinner == ["A"], str(gewinner))
check("der Verlierer bekommt sie nicht", verlierer == ["B"], str(verlierer))
erg2 = O.vergabe([absicht_von("A", "holz", 2.0), absicht_von("B", "holz", 1.0)],
                 O.vorrat("v2"), "saat", 0)
check("die Reihenfolge der Absichten aendert das Ergebnis nicht",
      [(x["besitzer"], ok) for x, ok in erg2] == [(x["besitzer"], ok) for x, ok in erg])
check("zwei Absichten desselben Besitzers werden abgelehnt",
      wirft(lambda: O.vergabe([absicht_von("A", "holz", 2.0), absicht_von("A", "minen", 1.0)],
                              O.vorrat("v2"), "saat", 0)) == "ValueError")
check("eine veraltete Runde wird abgelehnt",
      wirft(lambda: O.vergabe([absicht_von("A", "holz", 2.0, runde=1)],
                              O.vorrat("v2"), "saat", 0)) == "ValueError")
erg3 = O.vergabe([absicht_von("A", "holz", 2.0), absicht_von("B", "minen", 1.0)],
                 O.vorrat("v2"), "saat", 0)
check("zwei verschiedene Karten gehen an beide", all(ok for _, ok in erg3), str(erg3))

# --------------------------------------------------------------------------
abschnitt("11. Schattenpreise, Bezahlbarkeit und Buchung (Entwurf Abschnitt D)")

check("Gold hat immer den Schattenpreis 1", O.schattenpreis(start, "gold", 10, 10) == 1.0)
check("Holz auf der Startkarte kostet 0,75 Gold (Grundpreis, Entwurf Z. 142)",
      abs(O.schattenpreis(start, "holz", 100, 100) - 0.75) < 1e-9,
      str(O.schattenpreis(start, "holz", 100, 100)))
check("Holz auf der Holzkarte ist billiger (Kartenfaktor greift)",
      O.schattenpreis(k("holz"), "holz", 100, 100) < 0.75,
      str(O.schattenpreis(k("holz"), "holz", 100, 100)))
check("Stein auf der Farmkarte ist teurer (3,5-facher Kartenfaktor)",
      abs(O.schattenpreis(k("farmen"), "stein", 100, 100) - 2.625) < 1e-9,
      str(O.schattenpreis(k("farmen"), "stein", 100, 100)))
check("Holz auf der Minenkarte trifft die Obergrenze 4 (0,75 x 4 = 3,0)",
      abs(O.schattenpreis(k("minen"), "holz", 100, 100) - 3.0) < 1e-9,
      str(O.schattenpreis(k("minen"), "holz", 100, 100)))
check("der Vorratsfaktor senkt den Preis bei vollem Lager",
      O.schattenpreis(start, "holz", 1000, 100) < O.schattenpreis(start, "holz", 100, 100))
check("bezahlbar erkennt fehlende Mittel", O.bezahlbar({"holz": 10}, {"holz": 11}) is False)
check("bezahlbar erkennt gedeckte Mittel", O.bezahlbar({"holz": 11}, {"holz": 11}) is True)
check("buchen verbucht korrekt", O.buchen({"holz": 10}, {"holz": -5}) == {"holz": 5.0},
      str(O.buchen({"holz": 10}, {"holz": -5})))
check("buchen lehnt einen negativen Bestand ab",
      wirft(lambda: O.buchen({"holz": 10}, {"holz": -11})) == "ValueError")
check("buchen lehnt nicht endliche Mengen ab",
      wirft(lambda: O.buchen({"holz": 10}, {"holz": float("inf")})) == "ValueError")

sys.exit(bericht())
