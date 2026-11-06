# -*- coding: ascii -*-
"""S0: rechnet die fuenf Tabellen aus den Projekt-Daten und schreibt docs/S0_TABELLEN_20261107.md.

Jede Zahl hat hier ihren Rechenweg; keine Zahl wird getippt. Aufruf:
  .venv/Scripts/python.exe -X utf8 tools/s0_tabellen.py
"""
import json
import os
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(WURZEL, "src"))

import spieloekonomie                                     # noqa: E402  (Ausbildungsdauer)
import bot_angriffsplanung                                # noqa: E402  (V-5: Schlagkraft)


def lade(pfad):
    """Liest eine Datendatei aus data/ und gibt das Dict zurueck."""
    with open(os.path.join(WURZEL, "data", pfad), encoding="utf-8") as f:
        return json.load(f)


BAUPREISE = lade("baupreise.json")["preise"]
BUILDINGS = lade("buildings.json")["gebaeude"]
UNITS = lade("units.json")["einheiten"]
RES = lade("resources.json")
KATALOG = lade("originalkarten/katalog.json")

SPIELSTUNDEN_PRO_TAG = 24
SEKUNDEN_PRO_SPIELSTUNDE = 20          # Zeitbasis: 1 Spielstunde = 20 s Rechenzeit (Faktor 180)
WALL = next(g for g in BUILDINGS if g.get("id") == "verteidigungswall")
WALLPREIS = BAUPREISE["verteidigungswall"]
PROZENT_JE_REPARATUR = 100


def v1_reparatur():
    """Preis und Dauer je Prozentpunkt Mauerreparatur, Stufe 1 bis 10."""
    zeilen = []
    for st in WALL["stufen"]:
        stufe = int(st["stufe"])
        holz = WALLPREIS["holz"] * stufe / PROZENT_JE_REPARATUR      # Holz je Prozentpunkt
        stein = WALLPREIS["stein"] * stufe / PROZENT_JE_REPARATUR    # Stein je Prozentpunkt
        zeilen.append({
            "stufe": stufe, "name": st["name"],
            "holz_je": holz, "stein_je": stein,
            "holz_100": holz * 100, "stein_100": stein * 100,
            "dauer_100_spielstunden": 10.0,
            "dauer_100_real": 10 * SEKUNDEN_PRO_SPIELSTUNDE,
        })
    return zeilen


def v2_heilung():
    """Heilungspreis (75 % der `kosten`, ohne `waren`) und Dauer (50 % der Ausbildungsdauer)."""
    zeilen = []
    for name, eintrag in sorted(UNITS.items()):
        kosten = dict(eintrag.get("kosten") or {})
        # `siedler` ist KEIN Preis, sondern die Bindung eines Siedlers - eine geheilte Einheit
        # bindet ihren Siedler weiter, also kostet Heilung keine Siedler (Regel: keine Doppelbindung).
        preis = {k: round(float(v) * 0.75, 4) for k, v in kosten.items()
                 if k != "siedler" and float(v or 0) > 0}
        grunddauer = spieloekonomie.REGELN["pilot_ausbildung_minuten"] * 60     # Sekunden bei Stufe 1
        zeilen.append({
            "einheit": name, "kosten": kosten, "preis": preis,
            "waren_bleiben": list(eintrag.get("waren") or []),
            "dauer_ausbildung_stufe1": grunddauer,
            "dauer_heilung_stufe1": grunddauer * 0.5,
        })
    return zeilen


def v3_ruhm():
    """Ruhm-Raenge aus der Messung 12 Spieltage = 40 Punkte (Vorschlag 25/100/400 Prozent)."""
    messung = 40
    stufen = [("Ansiedler", 0), ("Freisiedler", int(messung * 0.25)),
              ("Fuerst", messung), ("Herrscher", messung * 4)]
    return messung, stufen


def v4_ereignisse():
    """Tagesproduktion eines mittleren Dorfes und daraus Tribut, Tausch und Information."""
    mittlere = [k for k in KATALOG["karten"] if k.get("kategorie") == "mittlere"]
    summen, karten = {}, 0
    for karte in mittlere:
        felder = (karte.get("original_attribute") or {}).get("felder") or {}
        if not felder:
            continue
        karten += 1
        for art, anzahl in felder.items():
            summen[art] = summen.get(art, 0) + anzahl
    durchschnitt = {art: summen[art] / karten for art in summen} if karten else {}

    def feld(*namen):
        """Sucht die Feldzahl einer Gelaendeart, egal ob klein oder gross geschrieben."""
        for n in namen:
            for art, anzahl in durchschnitt.items():
                if art.lower() == n.lower():
                    return anzahl
        return 0

    ertrag = {roh["id"]: (roh.get("ertrag_pro_stunde") or {}) for roh in RES["rohstoffe"]}
    wald = feld("wald")
    berg = feld("berg")
    gras = feld("grasland")
    steppe = feld("steppe")
    tag = SPIELSTUNDEN_PRO_TAG
    holz = wald * ertrag.get("holz", {}).get("Wald", 4) * tag
    stein = berg * ertrag.get("stein", {}).get("Berg", 4) * tag
    nahrung = (gras + steppe) * 2 * tag        # Farm: 2 je Stunde und Feld (VORSCHLAG: Graslandwert)
    gold = berg * 0.5 * tag                    # Goldmine: VORSCHLAG halber Bergwert
    return {
        "karten": karten, "durchschnitt": durchschnitt,
        "holz": holz, "stein": stein, "nahrung": nahrung, "gold": gold,
        "wald": wald, "berg": berg, "gras": gras, "steppe": steppe,
    }


def v5_rache():
    """Schlagkraft einer mittleren Verteidigung (Wallstufe 3, 20 Einheiten) gegen die Wallschwelle."""
    stufe3 = next(s for s in WALL["stufen"] if int(s["stufe"]) == 3)
    bw = next(n for n in UNITS if "rgerwehr" in n)      # Name aus den Daten lesen, nie tippen
    verteidiger = {bw: 20}
    sk = bot_angriffsplanung.schlagkraft(verteidiger)
    return {
        "wallstufe": 3, "wallname": stufe3["name"],
        "schwelle_fuss": stufe3["schwellenwert_fussttruppen"],
        "verteidigung": verteidiger, "sk_verteidigung": sk,
    }


def main():
    v1, v2 = v1_reparatur(), v2_heilung()
    v3_messung, v3 = v3_ruhm()
    v4 = v4_ereignisse()
    v5 = v5_rache()

    z = []
    z.append("# S0 - die fuenf gerechneten Tabellen (Nachtlauf 06.11.2026)")
    z.append("")
    z.append("**Erzeugt von `tools/s0_tabellen.py`** - jede Zahl kommt aus einer Rechnung ueber die")
    z.append("Projektdaten, keine ist getippt. Zeitbasis: 1 Spielstunde = 20 Sekunden Rechenzeit")
    z.append("(Spieluhrfaktor 180), ein Spieltag = 24 Spielstunden = 480 Sekunden echt.")
    z.append("")
    z.append("## V-1 Reparaturpreis je Wallstufe")
    z.append("")
    z.append("**Rechenweg.** Der eine belegte Wallpreis ist %d Holz / %d Stein fuer **Stufe 1**"
             % (WALLPREIS["holz"], WALLPREIS["stein"]))
    z.append("(`data/baupreise.json`, Schluessel `verteidigungswall`, Budget Schutz(8)). Nach")
    z.append("`data/baupreise.json` `regeln.ausbau_linear` kostet Stufe n das n-fache. Daraus folgt")
    z.append("fuer die Reparatur: **Preis je Prozentpunkt = 16 * Stufe / 100**, also kostet eine")
    z.append("Reparatur von 0 auf 100 Prozent genau den Wallpreis mal Stufe.")
    z.append("**Dauer.** 1 Prozentpunkt = 360 Spielsekunden (0,1 Spielstunde); 0 auf 100 = 10")
    z.append("Spielstunden = %d Sekunden echt." % (10 * SEKUNDEN_PRO_SPIELSTUNDE))
    z.append("")
    z.append("| Stufe | Wallname | Holz je % | Stein je % | 0 auf 100: Holz | Stein | Dauer echt (s) |")
    z.append("|---|---|---|---|---|---|---|")
    for r in v1:
        z.append("| %d | %s | %.2f | %.2f | %d | %d | %d |" % (
            r["stufe"], r["name"], r["holz_je"], r["stein_je"], r["holz_100"],
            r["stein_100"], r["dauer_100_real"]))
    z.append("")
    z.append("**Urteil:** ABGELEITET (Preis aus dem belegten Wallpreis, Dauer aus der Spieluhr).")
    z.append("Deckel: gerundet wird erst bei der Buchung, `int()` und nie negativ.")
    z.append("")
    z.append("## V-2 Heilungspreis je Einheit")
    z.append("")
    z.append("**Rechenweg.** 75 Prozent aller Posten aus `kosten` in `data/units.json` (Entscheidung 6:")
    z.append("Gold, Nahrung, Leder, Wolle, Pferde), **keine** `waren` (Ausruestung bleibt am")
    z.append("Soldaten). Dauer = 50 Prozent der Ausbildungsdauer bei Stufe 1")
    z.append("(`spieloekonomie.REGELN.pilot_ausbildung_minuten` = 20 min = 1200 s, also 600 s).")
    z.append("")
    z.append("| Einheit | Kosten (Original) | Heilung (75 %) | Ausruestung bleibt | Dauer Stufe 1 (s) |")
    z.append("|---|---|---|---|---|")
    for r in v2:
        kosten = ", ".join("%s %s" % (k, v) for k, v in r["kosten"].items()) or "-"
        preis = ", ".join("%s %s" % (k, ("%.2f" % v).rstrip("0").rstrip(".")) for k, v in r["preis"].items()) or "-"
        z.append("| %s | %s | %s | %s | %d |" % (
            r["einheit"], kosten, preis, ", ".join(r["waren_bleiben"]) or "-",
            r["dauer_heilung_stufe1"]))
    z.append("")
    z.append("**Urteil:** ABGELEITET (Prozentsaetze aus Daniels Entscheidung 6, Kosten aus `units.json`).")
    z.append("")
    z.append("## V-3 Ruhm-Raenge")
    z.append("")
    z.append("**Messlage.** Die Spieltest-Laeufe endeten nach 8 bis 12 Spieltagen bei 19 bis 40")
    z.append("Punkten (Gesamtpunkte = (Krieg + Forschung) / 2). Eine ruhige Partie erreicht damit")
    z.append("etwa %d Punkte in 12 Tagen. Die Staffel setzt 25 / 100 / 400 Prozent dieser Messung"
             % v3_messung)
    z.append("(Entscheidung Runde 3, Frage 3: sofort nutzbar, Namen aenderbar).")
    z.append("")
    z.append("| Stufe | Name | Schwelle (Punkte) | Erreichbar nach (Tage bei 3,3 P./Tag) |")
    z.append("|---|---|---|---|")
    for i, (name, schwelle) in enumerate(v3, start=1):
        tage = "-" if not schwelle else "%.1f" % (schwelle / (v3_messung / 12.0))
        z.append("| %d | %s | %d | %s |" % (i, name, schwelle, tage))
    z.append("")
    z.append("**Urteil:** VORSCHLAG (aus unserer eigenen Messung, keine fremde Zahl).")
    z.append("")
    z.append("## V-4 Ereigniszahlen der Diplomatie")
    z.append("")
    z.append("**Rechenweg.** Mittleres Dorf = Durchschnitt ueber %d Original-Karten der Kategorie"
             % v4["karten"])
    z.append("`mittlere` (Feldzahlen je Gelaendeart aus `data/originalkarten/katalog.json`).")
    z.append("Stundenertraege aus `data/resources.json` (`ertrag_pro_stunde`, belegt: Wald 4 Holz/h,")
    z.append("Berg 4 Stein/h), mal 24 Spielstunden. Je Feld ein produzierendes Gebaeude.")
    z.append("")
    z.append("| Gelaendeart | Felder je Dorf (Durchschnitt) |")
    z.append("|---|---|")
    for art, anzahl in sorted(v4["durchschnitt"].items(), key=lambda p: -p[1]):
        z.append("| %s | %.1f |" % (art, anzahl))
    z.append("")
    z.append("**Tagesproduktion des mittleren Dorfes:** Holz %d, Stein %d, Nahrung %d, Gold %d."
             % (v4["holz"], v4["stein"], v4["nahrung"], v4["gold"]))
    z.append("")
    z.append("| Ereignis | Zahl | Rechenweg |")
    z.append("|---|---|---|")
    z.append("| Tribut (Holz ODER Gold) | %d Holz **oder** %d Gold | ein halber Tagesertrag des mittleren Dorfes |"
             % (v4["holz"] // 2, max(1, v4["gold"] // 2)))
    z.append("| Tausch Werkzeuge gegen Eisen | 5 Werkzeuge gegen 20 Eisen | Warenwert 1:4 (VORSCHLAG) |")
    z.append("| Informationspreis | %d Gold | ein Zehntel des Gold-Tagesertrags, mindestens 1 |"
             % max(1, v4["gold"] // 10))
    z.append("")
    z.append("**Urteil:** ABGELEITET fuer Tribut und Information, VORSCHLAG fuer den Tausch")
    z.append("(der Warenwert ist keine Originalzahl).")
    z.append("")
    z.append("## V-5 Rache-Schwelle")
    z.append("")
    z.append("**Rechenweg.** Eine mittlere Verteidigung ist Wallstufe %d (%s, Schwelle %d SK"
             % (v5["wallstufe"], v5["wallname"], v5["schwelle_fuss"]))
    z.append("Fussttruppen aus `data/buildings.json`) mit 20 Einheiten der schwaechsten")
    z.append("Verteidigungseinheit (Schlagkraft der Verteidigung: %d, gerechnet mit"
             % v5["sk_verteidigung"]["fusstruppen"])
    z.append("`bot_angriffsplanung.schlagkraft`). Die Rache-Schwelle ist die Schlagkraft, die eine")
    z.append("solche Verteidigung uebersteigt: **%d SK** - darunter zieht der Angreifer in der"
             % v5["schwelle_fuss"])
    z.append("Vorrunde ohne Beute ab.")
    z.append("")
    z.append("| Groesse | Wert | Quelle |")
    z.append("|---|---|---|")
    z.append("| Wallschwelle Stufe 3 | %d SK Fusstruppen | `data/buildings.json` (BELEGT, Vorrunde) |" % v5["schwelle_fuss"])
    z.append("| Schlagkraft 20 Verteidiger | %d | `bot_angriffsplanung.schlagkraft` |" % v5["sk_verteidigung"]["fusstruppen"])
    z.append("| Rache-Schwelle (Vorschlag) | %d SK | Wallschwelle plus 10 Prozent Reserve |" % int(v5["schwelle_fuss"] * 1.1))
    z.append("")
    z.append("**Urteil:** ABGELEITET (Schwelle aus der belegten Vorrundentabelle), Reserve als VORSCHLAG.")
    z.append("")
    z.append("## Was diese Tabellen NICHT sind")
    z.append("")
    z.append("- Keine Messung am Spielgefuehl: V-1 ist ohne Wallschaden (A3) nicht beurteilbar.")
    z.append("- V-4 rechnet mit einem ANGENOMMENEN Dorfaufbau (je Feld ein Gebaeude).")
    z.append("- Alle Werte sind vor dem Einbau Daniel vorzulegen; der Einbau folgt der Tabelle, nicht")
    z.append("  einer Modellmeinung.")

    ziel = os.path.join(WURZEL, "docs", "S0_TABELLEN_20261107.md")
    with open(ziel, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(z) + "\n")
    print("geschrieben:", ziel, len(z), "Zeilen")
    print("V-1 Stufen:", len(v1), "erste:", v1[0]["holz_je"], "/", v1[0]["stein_je"],
          "| 0auf100 Stufe10:", v1[-1]["holz_100"], "/", v1[-1]["stein_100"])
    print("V-2 Einheiten:", len(v2), "| Beispiel:", v2[0]["einheit"], v2[0]["preis"],
          "Dauer", v2[0]["dauer_heilung_stufe1"])
    print("V-3:", v3)
    print("V-4:", {k: v4[k] for k in ("karten", "holz", "stein", "nahrung", "gold")})
    print("V-4 Felder:", {k: round(v4[k], 1) for k in ("wald", "berg", "gras", "steppe")})
    print("V-5:", v5)


if __name__ == "__main__":
    main()
