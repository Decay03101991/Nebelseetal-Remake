"""Freischaltungs-Kette aus den Projektdaten ableiten (Vorgabe Daniel 30.10.2026).

Daniel: "sicher ist die reihenfolge im orginal offensichtlich keine kette. aber es lassen sich
logische ketten daraus ableiten wenn man sich ankukt was angegeben ist und was fehlt und man
versucht die luecken logisch zu fuellen das das gesamt konzept erfuellt wird."

Das Werkzeug liest NUR die Datendateien und leitet daraus ab:
  * welche Gebaeude ohne Forschung baubar sind (Stufe 0),
  * welche Forschung welches Gebaeude freischaltet,
  * welche Forschung + welches Gebaeude welche Einheit ermoeglicht,
  * wo eine Luecke ist (etwas hat keine Voraussetzung, obwohl es eine braeuchte).

Es erfindet keine Bedingungen: was in den Daten steht, gilt; was fehlt, wird als LUECKE gemeldet.

Aufruf: python -X utf8 tools/freischaltung.py            (gibt die Kette aus)
        python -X utf8 tools/freischaltung.py --schreiben (schreibt docs/GENERIERT_FREISCHALTUNG.md)
"""
import json
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIEL = os.path.join(WURZEL, "docs", "GENERIERT_FREISCHALTUNG.md")


def lade(name):
    with open(os.path.join(WURZEL, "data", name), encoding="utf-8") as f:
        return json.load(f)


def eintraege(daten, schluessel):
    """Liste von (Kennung, Eintrag). Bei dict-Daten ist der Schluessel die Kennung.

    Wichtig: `data/units.json` haelt die Einheiten unter ihrem NAMEN als Schluessel und fuehrt
    kein Feld 'name' - wer nur die Werte nimmt, verliert die Namen (am 30.10. selbst erlebt:
    die Tabelle zeigte lauter '?').
    """
    wert = daten.get(schluessel) if isinstance(daten, dict) else daten
    if isinstance(wert, dict):
        return [(str(k), v) for k, v in wert.items() if isinstance(v, dict)]
    return [(str(v.get("id") or v.get("name") or "?"), v) for v in (wert or [])
            if isinstance(v, dict)]


def gebaeude_liste(daten):
    roh = daten.get("gebaeude") if isinstance(daten, dict) else daten
    if isinstance(roh, dict):
        liste = []
        for kennung, wert in roh.items():
            if isinstance(wert, dict):
                wert = dict(wert)
                wert.setdefault("id", kennung)
                liste.append(wert)
        return liste
    return [v for v in (roh or []) if isinstance(v, dict)]


FORSCHUNG_MUSTER = re.compile(r"([A-ZÄÖÜ][A-Za-zäöüß]+)(?:\s*(?:Stufe\s*)?(\d+))?")


def voraussetzung_lesen(text):
    """Aus 'Baukunst 1' / 'Baukunst' / 'keine (ohne Forschung baubar)' die (Forschung, Stufe) holen.

    Fallen aus dem Datenbestand (30.10.2026 selbst erlebt): `data/buildings.json` fuehrt oft nur
    den NAMEN ("Baukunst") ohne Stufe, und einmal "keine belegt". Ein Muster, das eine Ziffer
    verlangt, haelt dann ALLE Gebaeude fuer forschungsfrei - daraus entstand ein falscher Befund
    ("20 Gebaeude ohne Forschung"). Deshalb: fehlt die Ziffer, gilt Stufe 1.
    """
    if not text or not isinstance(text, str):
        return None
    if text.strip().lower().startswith("keine"):
        return None
    treffer = FORSCHUNG_MUSTER.search(text)
    if not treffer:
        return None
    return treffer.group(1), int(treffer.group(2) or 1)


def baue_kette():
    gebaeude = gebaeude_liste(lade("buildings.json"))
    einheiten = eintraege(lade("units.json"), "einheiten")
    forschungen = lade("research.json")
    forschungen = forschungen.get("forschungen", forschungen)

    stufe0, geb_mit_forschung, luecken = [], [], []
    for g in gebaeude:
        kennung = str(g.get("id") or g.get("name") or "?")
        art = voraussetzung_lesen(g.get("voraussetzung"))
        if art is None:
            stufe0.append(kennung)
        else:
            geb_mit_forschung.append((kennung, art[0], art[1]))
        if not g.get("name"):
            luecken.append(f"Gebaeude '{kennung}' hat keinen Namen")

    einheiten_nach_gebaeude = {}
    einheiten_mit_forschung = []
    for name, e in einheiten:
        geb = str(e.get("gebaeude") or "").strip()
        einheiten_nach_gebaeude.setdefault(geb or "(ohne Gebaeude)", []).append(name)
        forschung = e.get("voraussetzung") or {}
        if isinstance(forschung, dict) and forschung.get("forschung"):
            einheiten_mit_forschung.append(
                (name, forschung.get("forschung"), int(forschung.get("stufe") or 0), geb))
        if not geb:
            luecken.append(f"Einheit '{name}' nennt kein Ausbildungsgebaeude")

    # Forschungen und ihre eigenen Voraussetzungen (z. B. "Bibliothek 1")
    forschungs_bedingungen = []
    for kennung, wert in (forschungen.items() if isinstance(forschungen, dict) else []):
        if not isinstance(wert, dict):
            continue
        forschungs_bedingungen.append((kennung, wert.get("voraussetzung") or "—"))

    return {
        "stufe0": sorted(stufe0),
        "geb_mit_forschung": sorted(geb_mit_forschung),
        "einheiten_nach_gebaeude": einheiten_nach_gebaeude,
        "einheiten_mit_forschung": sorted(einheiten_mit_forschung),
        "forschungs_bedingungen": sorted(forschungs_bedingungen),
        "luecken": luecken,
    }


def bericht(kette):
    zeilen = []
    z = zeilen.append
    z("# Freischaltung — aus den Projektdaten berechnet\n")
    z("**Erzeugt von** `tools/freischaltung.py` (nicht von Hand geschrieben). Grundlage sind nur")
    z("`data/buildings.json`, `data/units.json` und `data/research.json`; was dort fehlt, steht unter")
    z("„Lücken“ und wird **nicht** erfunden.\n")
    z("## Stufe 0 — ohne jede Forschung baubar\n")
    for g in kette["stufe0"]:
        z(f"- {g}")
    z("\n## Gebaeude, die eine Forschung verlangen\n")
    z("| Gebaeude | Forschung | Stufe |")
    z("|---|---|---|")
    for kennung, forschung, stufe in kette["geb_mit_forschung"]:
        z(f"| {kennung} | {forschung} | {stufe} |")
    z("\n## Forschungen und ihre Bedingung\n")
    z("| Forschung | Bedingung (wörtlich aus den Daten) |")
    z("|---|---|")
    for kennung, bedingung in kette["forschungs_bedingungen"]:
        z(f"| {kennung} | {bedingung} |")
    z("\n## Einheiten je Ausbildungsgebaeude\n")
    z("| Gebaeude | Einheiten |")
    z("|---|---|")
    for geb in sorted(kette["einheiten_nach_gebaeude"]):
        namen = ", ".join(sorted(kette["einheiten_nach_gebaeude"][geb]))
        z(f"| {geb} | {namen} |")
    z("\n## Einheiten mit eigener Forschungsvoraussetzung\n")
    z("| Einheit | Forschung | Stufe | Gebaeude |")
    z("|---|---|---|---|")
    for name, forschung, stufe, geb in kette["einheiten_mit_forschung"]:
        z(f"| {name} | {forschung} | {stufe} | {geb} |")
    z("\n## Luecken (hier fehlt eine Angabe — Entscheidung noetig)\n")
    if kette["luecken"]:
        for l in kette["luecken"]:
            z(f"- {l}")
    else:
        z("- keine Luecke gefunden: jede Einheit nennt ein Gebaeude, jedes Gebaeude einen Namen.")
    return "\n".join(zeilen) + "\n"


def main():
    kette = baue_kette()
    text = bericht(kette)
    print(text)
    if "--schreiben" in sys.argv:
        with open(ZIEL, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print(f"\nGeschrieben: {ZIEL}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
