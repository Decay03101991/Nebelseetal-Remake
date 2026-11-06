"""Langzeit-Balancing MESSEN (Auftrag Daniel 31.10.2026).

Frage: Fuehren unsere Zahlen in einem LANGEN Spiel zu erreichbaren, ausgeglichenen und ueberhaupt
spielbaren Situationen - oder sind Truppen, Forschung, Ausruestung und Beute so bemessen, dass ein
Spieler entweder nie angreifen kann oder in wenigen Tagen alles hat?

Gerechnet wird AUSSCHLIESSLICH aus den Projektdaten und den echten Kernfunktionen:
  data/originalkarten/katalog.json   Gelaende je Originalkarte (127 Karten, 10x10)
  data/buildings.json                Ertrag je Gebaeude und Gelaende, Standortregeln, Wallstufen
  data/units.json                    Kosten, Werte, Ausruestungswaren je Einheit
  data/warenrezepte.json             Materialkosten und Dauer je Ware
  data/research.json                 Forschungsregeln (Dauer Stufe^2, Kosten verdoppeln)
  einheiten.ladung_der_gruppe / schlagkraft, kampfbericht.beute_staffel,
  kampf.fuehre_schlacht, auftraege.reisezeit_sekunden / kosten_der_mission, forschung.kosten

Spielzeit = 24 Spielstunden je Spieltag. Die Spieluhr (Faktor aus data/spielzeit.json) aendert nur
das Tempo der Anzeige, nicht die Verhaeltnisse.

Aufruf:  python -X utf8 tools/balancing_messung.py
         python -X utf8 tools/balancing_messung.py --tage 7,30,90,180
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, ROOT)

import auftraege  # noqa: E402
import einheiten as E  # noqa: E402
import forschung  # noqa: E402
import kampf  # noqa: E402
import kampfbericht  # noqa: E402


def lade(name):
    with open(os.path.join(ROOT, "data", name), encoding="utf-8") as f:
        return json.load(f)


GEBAEUDE = {g["id"]: g for g in lade("buildings.json")["gebaeude"]}
WALLSTUFEN = GEBAEUDE["verteidigungswall"]["stufen"]
UNITS = lade("units.json")["einheiten"]
REZEPTE = lade("warenrezepte.json")
KARTEN = lade(os.path.join("originalkarten", "katalog.json"))["karten"]
SPIELZEIT = lade("spielzeit.json")
MAX_SIEDLUNGEN = 6

# Ausbauplan je Siedlung: das ist eine ANNAHME (klar als solche benannt), kein Originalwert.
PLAN_WOHN = 10
PLAN_SONSTIGE = {"bibliothek": 1, "kriegerakademie": 1, "stellmacher": 1,
                 "schmiede": 2, "naehstube": 1, "bogenbauer": 1, "verteidigungswall": 1}


def name_von(anfang):
    """Ein Einheitenname aus den DATEN (Umlaute nicht tippen)."""
    for n in UNITS:
        if n.lower().startswith(anfang.lower()):
            return n
    return None


def wert(tabelle, name):
    """Wert aus einer Rohstofftabelle, Gross-/Kleinschreibung egal."""
    for k, v in (tabelle or {}).items():
        if str(k).lower() == str(name).lower():
            return float(v)
    return 0.0


def feld_statistik():
    summe = Counter()
    for k in KARTEN:
        felder = (k.get("original_attribute") or {}).get("felder") or {}
        for art, n in felder.items():
            summe[str(art).lower()] += int(n or 0)
    n = max(1, len(KARTEN))
    return {art: summe[art] / n for art in summe}, len(KARTEN)


def baubar_je_gebaeude(stat):
    ergebnis = {}
    for kennung, g in GEBAEUDE.items():
        nur = [str(x).lower() for x in (g.get("nur_auf") or [])]
        ergebnis[kennung] = (sum(stat.get(a, 0.0) for a in nur) if nur else sum(stat.values()))
    return ergebnis


def ausbau_je_siedlung(stat, baubar):
    belegt = Counter()

    def nimm(kennung, anzahl):
        anzahl = max(0.0, min(float(anzahl), baubar.get(kennung, 0.0) - belegt[kennung]))
        belegt[kennung] += anzahl
        return anzahl

    plan = Counter()
    plan["haus"] = nimm("haus", PLAN_WOHN)
    for kennung, anzahl in PLAN_SONSTIGE.items():
        plan[kennung] = nimm(kennung, anzahl)
    berg = max(0.0, stat.get("berg", 0.0) - belegt["steinmetz"] - belegt["erzmine"]
               - belegt["goldmine"])
    for kennung, anteil in (("steinmetz", 0.30), ("erzmine", 0.40), ("goldmine", 0.30)):
        plan[kennung] = nimm(kennung, berg * anteil)
    gras = max(0.0, stat.get("grasland", 0.0) - belegt["farm"])
    for kennung, anteil in (("farm", 0.35), ("schafszucht", 0.25), ("pferdezucht", 0.20),
                            ("rinderfarm", 0.20)):
        plan[kennung] = nimm(kennung, gras * anteil)
    wald = max(0.0, stat.get("wald", 0.0) - belegt["jaeger"])
    plan["holzfaeller"] = nimm("holzfaeller", wald * 0.6)
    plan["jaeger"] = nimm("jaeger", wald * 0.4)
    plan["tempel"] = nimm("tempel", max(0.0, stat.get("nebelsee", 0.0) - belegt["bibliothek"]))
    return plan


def ertrag_je_stunde(plan):
    """Stundenertrag je Rohstoff (nur die ERSTE, beste Gelaendeart je Gebaeude - konservativ)."""
    ertrag = Counter()
    for kennung, anzahl in plan.items():
        if anzahl <= 0:
            continue
        g = GEBAEUDE.get(kennung) or {}
        tabelle = g.get("ertrag_pro_stunde")
        if not isinstance(tabelle, dict) or not tabelle:
            continue
        art, wertigkeit = next(iter(tabelle.items()))
        if isinstance(wertigkeit, dict):
            for stoff, menge in wertigkeit.items():
                ertrag[stoff] += anzahl * float(menge)
        else:
            ertrag[str(g.get("rohstoff"))] += anzahl * float(wertigkeit)
    return ertrag


def siedlergrenze():
    return 10 + 5 * PLAN_WOHN


def kosten_der_einheit(name):
    e = UNITS[name]
    kosten = dict(e.get("kosten") or {})
    waren = list(e.get("waren") or [])
    material = Counter()
    sekunden = 0.0
    for ware in waren:
        r = REZEPTE.get(ware) or {}
        for stoff, menge in (r.get("kosten") or {}).items():
            material[stoff] += float(menge)
        sekunden += float(r.get("dauer") or 0)
    return kosten, waren, material, sekunden


def forschungs_kette(ziel):
    kosten = 0
    stunden = 0
    for stufe in range(1, int(ziel) + 1):
        kosten += sum(forschung.kosten(stufe).values())
        stunden += stufe * stufe
    return kosten, stunden


def reicher_wert(reich, stoff, tage):
    for k, v in reich.items():
        if str(k).lower() == str(stoff).lower():
            return v * 24 * tage
    return 0.0


def kampf_probe(angreifer, verteidiger, wall, zustand, vorraete, laeufe=40):
    siege = 0
    verluste = Counter()
    beute = Counter()
    vorrunden = 0
    for i in range(laeufe):
        ergebnis = kampf.fuehre_schlacht(dict(angreifer), dict(verteidiger), wall_stufe=wall,
                                        wall_zustand=zustand, vorraete=dict(vorraete),
                                        rng=random.Random(1000 + i))
        if ergebnis.get("vorrunde_bestanden"):
            vorrunden += 1
        if ergebnis.get("ausgang") == "angreifer":
            siege += 1
        for n, k in (ergebnis.get("verluste_angreifer") or {}).items():
            verluste[n] += k
        zustand_nach = float(ergebnis.get("mauer_zustand") or zustand)
        uebrig = (sum(verteidiger.values())
                  - sum((ergebnis.get("verluste_verteidiger") or {}).values()))
        genommen = kampfbericht.beute_staffel(angreifer, vorraete,
                                             wall_zustand_vor=zustand_nach,
                                             verteidiger_uebrig=uebrig)
        beute.update(genommen)
    return vorrunden, siege, verluste, beute, laeufe


def kennzahlen_bezug():
    """Die JUNGSTE gemessene Partie aus `docs/balancing/kennzahlen.jsonl` - oder None.

    Warum hier: diese Messung rechnet aus den Daten (Ertraege, Kosten, Schlachten), nicht aus
    einer gespielten Partie. Damit ihre Zahlen nicht neben einer unbekannten Wirklichkeit
    stehen, nennt sie die letzte gemessene Partie und WARNT, wenn deren `daten_hash` nicht
    mehr zu den heutigen Datendateien passt (dann ist das Blatt veraltet). Es wird NICHTS
    nachgerechnet - die Zeile ist die EINE Quelle (Ablauf Schritt 2).
    """
    pfad = os.path.join(ROOT, "docs", "balancing", "kennzahlen.jsonl")
    if not os.path.isfile(pfad):
        return None                                     # noch keine Partie gemessen
    letzte = None
    with open(pfad, encoding="utf-8") as f:
        for zeile in f:
            zeile = zeile.strip()
            if zeile:
                letzte = json.loads(zeile)              # die LETZTE Zeile ist die juengste
    if letzte is None:
        return None
    try:
        sys.path.insert(0, os.path.join(ROOT, "tools"))
        import spieltest_simulation as SIM               # EINE Hash-Implementierung
        letzte["_hash_aktuell"] = (letzte.get("daten_hash") == SIM.daten_hash())
    except Exception:                                   # noqa: BLE001 - Bezug ist eine Zugabe
        letzte["_hash_aktuell"] = None
    return letzte


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tage", default="7,30,90,180")
    args = p.parse_args()
    tage = [float(t) for t in args.tage.split(",") if t.strip()]

    krieger = name_von("Krieger")
    bogen = name_von("Kurzbogen")
    handkarren = name_von("Handkarren")
    zweispaenner = name_von("Zweisp")
    karawane = name_von("Handelskarawane")
    print("# Balancing-Messung — Nebelseetal Remake (Spieluhr-Faktor %s)"
          % SPIELZEIT.get("faktor"))

    # 0 --------------------------------------------------------------- Bezug
    # Die Kennzahlen sind eine ZUGABE: fehlt das Blatt, laeuft die Messung unveraendert.
    bezug = kennzahlen_bezug()
    if bezug:
        sw = bezug.get("startwert") or {}               # Saat, Stil, Laenge der Partie
        st = bezug.get("stand") or {}
        print("\n## 0. Bezug: die juengste gemessene Partie (docs/balancing/kennzahlen.jsonl)")
        print("\n| Groesse | Wert |")
        print("|---|---|")
        print("| Startwert | Saat %s, Stil %s, %s Spieltage |"
              % (sw.get("saat"), sw.get("stil"), sw.get("tage")))
        print("| Stand | %s%s |" % (st.get("kopf") or "?",
                                     "" if st.get("sauber") is not False else " (Arbeitsbaum schmutzig)"))
        print("| Haus / Bibliothek / Ware / Krieger / Gefecht | %s / %s / %s / %s / %s |"
              % tuple("-" if bezug.get(k) is None else bezug.get(k) for k in
                      ("tag_erstes_haus", "tag_erste_bibliothek", "tag_erste_ware",
                       "tag_erster_krieger", "tag_erstes_gefecht")))
        print("| Ruhm-Stufe / Leerlauf | %s / %s s |"
              % (bezug.get("ruhm_stufe"), bezug.get("leerlauf_sek")))
        print("| Handelspunkte | %s |"
              % ("nicht gemessen (kein Zaehler, G-8)" if bezug.get("handelspunkte") is None
                 else bezug.get("handelspunkte")))
        print("| groesste Luecke ohne Meilenstein | %s Spieltage |"
              % bezug.get("abstand_meilensteine_max"))
        if bezug.get("_hash_aktuell") is False:
            print("\n**WARNUNG: das Kennzahlenblatt ist aelter als die Datendateien** "
                  "(daten_hash stimmt nicht). Neue Partie messen mit "
                  "`python -X utf8 tools/spieltest_simulation.py --tage 12 --kennzahlen`, "
                  "sonst stehen diese Zahlen neben einem anderen Datenstand.")

    # 1 ------------------------------------------------------------------- Karte
    stat, n_karten = feld_statistik()
    baubar = baubar_je_gebaeude(stat)
    plan = ausbau_je_siedlung(stat, baubar)
    ertrag = ertrag_je_stunde(plan)
    reich = {k: v * MAX_SIEDLUNGEN for k, v in ertrag.items()}
    print("\n## 1. Was passt auf eine Originalkarte? (%d Karten, 10x10)" % n_karten)
    print("\n| Gelaende | Felder je Karte |")
    print("|---|---|")
    for art in sorted(stat, key=lambda a: -stat[a]):
        print("| %s | %.1f |" % (art, stat[art]))
    print("\n**Ausbauplan je Siedlung (ANNAHME):** " + ", ".join(
        "%s %.1f" % (k, v) for k, v in sorted(plan.items()) if v > 0))
    print("\nStundenertrag je Siedlung: " + ", ".join(
        "%s %.1f" % (k, v) for k, v in sorted(ertrag.items())))
    print("\nReich (%d Siedlungen): " % MAX_SIEDLUNGEN + ", ".join(
        "%s %.0f/h = %.0f/Tag" % (k, v, v * 24) for k, v in sorted(reich.items())))

    # 2 ------------------------------------------------------------------ Bestand
    print("\n## 2. Bestand, wenn NICHTS ausgegeben wird")
    stoffe = sorted(ertrag, key=lambda k: -ertrag[k])
    print("\n| Spieltage | " + " | ".join(stoffe) + " | Summe |")
    print("|---" * (len(stoffe) + 2) + "|")
    for t in tage:
        werte = [reicher_wert(reich, k, t) for k in stoffe]
        print("| %.0f | %s | %.0f |" % (t, " | ".join("%.0f" % w for w in werte), sum(werte)))

    # 3 ----------------------------------------------------- Siedler als Grenze
    grenze = siedlergrenze()
    print("\n## 3. Die harte Grenze sind SIEDLER, nicht Rohstoffe")
    print("\nSiedlergrenze je Siedlung: **%d** (10 + 5 je Haus) · Reich: **%d** Soldaten maximal."
          % (grenze, grenze * MAX_SIEDLUNGEN))
    print("Jede Einheit UND jeder Karren kostet Siedler - Armee und Transport teilen denselben Topf.")

    # 4 ------------------------------------------------------ Einheitenkosten
    print("\n## 4. Was kostet eine Armee? (je Stueck, aus data/units.json + warenrezepte.json)")
    print("\n| Einheit | Siedler | Gold | Pferde | Ausruestung | Material | Werkstatt h |")
    print("|---|---|---|---|---|---|---|")
    for n in (name_von("Kaempfer"), krieger, name_von("Ritter"), bogen,
              handkarren, zweispaenner, karawane):
        if not n:
            continue
        kosten, waren, material, sekunden = kosten_der_einheit(n)
        print("| %s | %s | %s | %s | %s | %s | %.1f |" % (
            n, kosten.get("siedler", 0), kosten.get("gold", 0), kosten.get("pferde", 0),
            ", ".join(waren) or "-",
            ", ".join("%s %g" % (k, v) for k, v in material.items()) or "-",
            sekunden / 3600))
    if krieger:
        kosten, waren, material, sekunden = kosten_der_einheit(krieger)
        for anzahl in (50, 100, 200):
            gold = wert(kosten, "gold") * anzahl
            print("- **%d %s**: %d Gold (= %.0f Spieltage des ganzen Goldertrags), %d Siedler, "
                  "%s, %.0f Werkstatt-Stunden = %.0f Spieltage in 2 Schmieden"
                  % (anzahl, krieger, gold, gold / max(1.0, wert(reich, "gold") * 24),
                     anzahl * int(kosten.get("siedler", 1)),
                     ", ".join("%s %g" % (k, v * anzahl) for k, v in material.items()),
                     sekunden * anzahl / 3600, sekunden * anzahl / 3600 / 24 / 2))

    # 5 ------------------------------------------------------------------ Forschung
    print("\n## 5. Forschung: Dauer = Stufe^2 Stunden, Kosten verdoppeln sich")
    print("\n| Stufe | Kosten der Stufe | Gesamt (Holz) | Gesamtdauer |")
    print("|---|---|---|---|")
    for stufe in (1, 3, 5, 7, 8, 10):
        k, h = forschungs_kette(stufe)
        print("| %d | %d | %d | %.0f h = %.1f Spieltage |"
              % (stufe, sum(forschung.kosten(stufe).values()), k, h, h / 24))
    holz_tag = wert(reich, "holz") * 24
    k10, h10 = forschungs_kette(10)
    print("\nAlle 21 Gebiete auf Stufe 10 waeren **%d Holz** — %.1f Spieltage, wenn der GANZE Holzertrag"
          " (%.0f/Tag) nur dorthin geht." % (k10 * 21, k10 * 21 / max(1.0, holz_tag), holz_tag))

    # 6 ------------------------------------------------------- Wall und Schlagkraft
    print("\n## 6. Wall: wie viele Truppen oeffnen ihn? (SK-Schwellen aus den Daten)")
    sk_krieger = E.schlagkraft(krieger) if krieger else 0
    print("\nSchlagkraft %s = %s · die Schwelle gilt fuer die NAHKAMPF-Einheiten." % (krieger, sk_krieger))
    print("\n| Wallstufe | Name | Schwelle Fuss | noetige %s | Schwelle Belagerung |" % krieger)
    print("|---|---|---|---|---|")
    for w in WALLSTUFEN:
        noetig = w["schwellenwert_fussttruppen"]
        print("| %d | %s | %d | %s | %s |" % (
            w["stufe"], w["name"], noetig,
            ("%.0f" % (noetig / sk_krieger)) if sk_krieger else "?",
            w.get("schwellenwert_belagerungswaffen") or "-"))

    # 7 ------------------------------------------------------------ Kampf 2:1
    print("\n## 7. Kampf: Angreifer mit DOPPELTER Staerke gegen die Haelfte (echte Simulation)")
    haelfte = 20
    angreifer = {krieger: haelfte * 2, handkarren: 10} if krieger and handkarren else {}
    verteidiger = {krieger: haelfte} if krieger else {}
    for wall in (0, 2, 3, 4, 6):
        vorrunden, siege, verluste, beute, laeufe = kampf_probe(
            angreifer, verteidiger, wall, 100.0, {"Holz": 5000, "Stein": 5000, "Metall": 2000})
        print("- Wall %d: Vorrunde bestanden %d/%d · Siege %d/%d · eigene Verluste Ø %.1f von %d ·"
              " Beute Ø %s" % (wall, vorrunden, laeufe, siege, laeufe,
                                sum(verluste.values()) / laeufe, sum(angreifer.values()),
                                {k: round(v / laeufe) for k, v in beute.items()} or "keine"))

    # 8 -------------------------------------------------------------- Beute
    print("\n## 8. Beute: Karren, Siedler und Wellen bis \"alles gestohlen\"")
    print("\nStaffel (VORSCHLAG, Register 45): %s" % kampfbericht.BEUTE_STAFFEL_PROZENT)
    print("\n| Karren | Ladung je Stueck | Siedler je Stueck | Ladung je Siedler |")
    print("|---|---|---|---|")
    for n in (handkarren, zweispaenner, karawane):
        if not n:
            continue
        l = E.ladung(n)
        s = int((UNITS[n].get("kosten") or {}).get("siedler", 1))
        print("| %s | %d | %d | %.0f |" % (n, l, s, l / max(1, s)))
    for t in tage:
        bestand = sum(reicher_wert(reich, k, t) for k in stoffe)
        kapazitaet = E.ladung_der_gruppe({zweispaenner: 24}) if zweispaenner else 0
        rest = bestand
        wellen = 0
        for anteil in (0.10, 0.60, 1.00):
            if rest <= 0:
                break
            wellen += 1
            rest -= min(kapazitaet, rest * anteil)
        print("- **%.0f Spieltage**: Bestand %.0f · 24 %s tragen %d · nach %d Wellen (10/60/100 %%)"
              " bleiben %.0f uebrig" % (t, bestand, zweispaenner, kapazitaet, wellen, rest))

    # 8b ------------------------------------------------- Feldzug mit Nachproduktion
    print("\n## 8b. Feldzug: Wellen, Nachproduktion und was ein Siedler-Budget hergibt")
    print("\nAnnahme: 240 Siedler fuer Soldaten, 120 fuer Karren (Zweispänner, 2 Siedler je Stueck"
          " = 60 Karren, Ladung %d). Jede Welle: %.1f h hin und zurueck, Beuteanteil 10/30/60/100 %%,"
          " waehrend der Fahrt produziert das Reich weiter."
          % (E.ladung_der_gruppe({zweispaenner: 60}) if zweispaenner else 0, 3.2))
    kapazitaet = E.ladung_der_gruppe({zweispaenner: 60}) if zweispaenner else 0
    stunden_je_welle = 3.2
    for t in tage:
        bestand = sum(reicher_wert(reich, k, t) for k in stoffe)
        zuwachs = sum(reich.values()) * stunden_je_welle
        rest = bestand
        anteile = (0.10, 0.30, 0.60, 1.00)
        wellen = 0
        geholt = 0.0
        while wellen < 20 and rest > bestand * 0.05:
            anteil = anteile[min(wellen, len(anteile) - 1)]
            rest += zuwachs
            nimm = min(kapazitaet, rest * anteil)
            rest -= nimm
            geholt += nimm
            wellen += 1
        print("- **%.0f Spieltage**: Bestand %.0f · in %d Wellen %.0f geholt, %.0f bleiben (%.0f %%"
              " des Ausgangsbestands)" % (t, bestand, wellen, geholt, rest, 100 * rest / max(1.0, bestand)))

    # 9 ------------------------------------------------- Reise, Kosten, Taktung
    print("\n## 9. Weg, Kosten je Welle und Taktung")
    armee = {krieger: 40} if krieger else {}
    for entfernung in (5, 10, 20):
        sekunden = auftraege.reisezeit_sekunden(entfernung, 25)
        kosten = auftraege.kosten_der_mission(armee, entfernung, 25, fremdes_ziel=True)
        print("- %2d Felder: eine Strecke %.1f h, Hin und Rueck %.1f h · Gold %.0f · Nahrung %.1f ·"
              " Mana %.1f" % (entfernung, sekunden / 3600, 2 * sekunden / 3600,
                              kosten.get("gold", 0), kosten.get("nahrung", 0),
                              kosten.get("mana", 0)))
    print("\nEine Welle ist EIN Auftrag (Ziel, Truppen, Bestaetigung). Die Grenze ist nicht die"
          " Oberflaeche, sondern die Zahl der Truppen und Karren: was unterwegs ist, verteidigt"
          " nicht zu Hause.")

    # 10 ------------------------------------------------------------- Verdikt
    print("\n## 10. Verdikt aus den Messwerten (maschinell, ohne Deutung)")
    # Gold fuer 100 Einheiten kommt aus den DATEN, nicht aus einer getippten Zahl: Register 225
    # (05.11.2026) hat die Goldkosten der Militaereinheiten gesenkt - eine feste 500 im Werkzeug
    # haette danach eine falsche Spieltagszahl gemeldet (Werkzeugbefund, kein Spielbefund).
    print("\n- Soldaten-Deckel: %d im Reich (Siedler)." % (grenze * MAX_SIEDLUNGEN))
    _krieger_gold = wert(kosten_der_einheit(krieger)[0], "gold") if krieger else 0   # Gold je Einheit
    print("- Gold fuer 100 %s: %d = %.0f Spieltage des vollen Goldertrags." % (
        krieger, 100 * _krieger_gold, 100 * _krieger_gold / max(1.0, wert(reich, "gold") * 24)))
    print("- Alle 21 Forschungen auf Stufe 10: %d Holz = %.0f Spieltage des vollen Holzertrags." % (
        k10 * 21, k10 * 21 / max(1.0, holz_tag)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
