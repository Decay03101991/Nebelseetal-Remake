"""Nebelseetal Remake - Warenrezepte aus dem Oekonomie-Entwurf ableiten (Werkzeug).

Quelle: archiv/analysen/audits/entwurf_spieloekonomie_sol_2026-10-05.txt, Abschnitt "4. Pilotrezepte,
lokale Ausbildung und echte Verbrauchsbelege", Codeblock Zeilen 507-534.

Das ist ein REINES STANDARDWERKZEUG. Es liest die Projektdateien, leitet fuer JEDE Ware aus
data/items.json["waren"] ein Rezept ab und schreibt das Ergebnis nach data/warenrezepte.json.

WICHTIG fuer spaeter: Zur LAUFZEIT DES SPIELS wird NUR diese fertige data/warenrezepte.json
gelesen. Es wird NICHT bei jedem Start neu abgeleitet - so steht es im Entwurf. Dieses
Werkzeug laeuft von Hand, wenn sich items.json, die Werkstattdaten oder die Ertraege aendern.

Die Ableitung selbst stammt woertlich aus dem Entwurf. Sie baut KEINE zweite Wahrheit der
Erträge auf: der Normertrag kommt aus spieloekonomie.einzelmaximum(), die einzige belegte
Dauer aus werkstatt.BELEGTE_DAUER_SEKUNDEN, die Werkstatt aus werkstatt.werkstatt_fuer und
die Forschungsnamen aus spieldaten.forschungen().

Hinweis zum Entwurf: Zeile 529 liest die Pilotdauer als REGELN["pilot_waren_minuten"]*60;
der hier freigegebene Auszug schreibt die 20 Minuten fest (20*60). Beide Werte sind gleich
(data/spieloekonomie.json: pilot_waren_minuten = 20), deshalb ist die Ableitung dieselbe.

Aufruf:  python -X utf8 tools/warenrezepte_ableiten.py
"""
from __future__ import annotations

import json
import math
import os
import re
import sys


def _pfade_bereitstellen():
    """Projektwurzel und src in den Suchpfad legen (wie tests/harness.import_src)."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for p in (root, os.path.join(root, "src")):
        if p not in sys.path:
            sys.path.insert(0, p)
    return root


ROOT = _pfade_bereitstellen()

import spieldaten        # noqa: E402
import spieloekonomie    # noqa: E402
import werkstatt         # noqa: E402

# Der Vorschlagstext, der in JEDEM Rezept als Herkunft steht (so im Entwurf vorgesehen).
HERKUNFT = "VORSCHLAG: Normertrag mal Pilotdauer; Schwertdauer separat belegt"


def lade(name: str) -> dict:
    """Eine Datendatei aus data/ laden - dieselbe Funktion wie in src/spieloekonomie.py."""
    return spieloekonomie.lade(name)


def warenforderungen(name: str, waren: dict | None = None) -> dict:
    """{forschung: stufe} der Voraussetzungen einer Ware; {} bei 'keine'.

    Woertlich aus dem Entwurf (Zeilen 514-524). `waren` ist optional: ohne Angabe kommt die
    Warenliste aus data/items.json. Der Parameter dient nur der Pruefbarkeit (kuenstlicher
    Fall einer ungeklaerten Voraussetzung), die normale Ableitung uebergibt ihn nicht.
    """
    if waren is None:
        waren = lade("items.json")["waren"]
    t = waren[name]["voraussetzung"]
    if t == "keine":
        return {}
    out = {}
    for teil in t.split("+"):
        treffer = re.fullmatch(r"\s*(.*?)\s+(\d+)\s*", teil)
        if treffer is None or treffer[1] not in spieldaten.forschungen():
            raise ValueError("Ungeklaerte Warenvoraussetzung: " + t)
        out[treffer[1]] = int(treffer[2])
    return out


def pilotrezept(name: str, waren: dict | None = None) -> dict:
    """Ein VORSCHLAGS-Rezept fuer eine Ware aus Normertrag und Pilotdauer (Entwurf Z. 526-534)."""
    forderungen = warenforderungen(name, waren)
    belegt = werkstatt.BELEGTE_DAUER_SEKUNDEN.get(name)
    # Die Pilotdauer kommt aus den Regeldaten (data/spieloekonomie.json) — KEINE zweite Wahrheit
    # als Literal. Der Entwurf (Z. 529) liest sie genau so: REGELN["pilot_waren_minuten"]*60.
    _pilot = spieloekonomie.REGELN["pilot_waren_minuten"] * 60
    dauer = belegt if belegt is not None else _pilot * (1 + sum(forderungen.values()))
    typ = werkstatt.werkstatt_fuer(name)
    material = ("metall" if typ == "schmiede"
                else "holz" if typ == "bogenbauer"
                else "leder" if ("Leder" in name or "Fell" in name)
                else "wolle")
    menge = math.ceil(spieloekonomie.einzelmaximum()[material] * dauer / 3600)
    return {"kosten": {material: menge}, "dauer": dauer, "voraussetzungen": forderungen,
            "_herkunft": HERKUNFT}


def rezepte_ableiten(waren: dict | None = None) -> dict:
    """Fuer ALLE Waren aus data/items.json["waren"] ein Rezept ableiten (Reihenfolge bleibt)."""
    if waren is None:
        waren = lade("items.json")["waren"]
    return {name: pilotrezept(name, waren) for name in waren}


def schreibe_rezepte(ziel: str | None = None) -> str:
    """Die abgeleiteten Rezepte als eingefrorene Datendatei schreiben und den Pfad liefern."""
    if ziel is None:
        ziel = os.path.join(ROOT, "data", "warenrezepte.json")
    rezepte = rezepte_ableiten()
    with open(ziel, "w", encoding="utf-8") as f:
        json.dump(rezepte, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return ziel


def main() -> int:
    ziel = schreibe_rezepte()
    rezepte = rezepte_ableiten()
    print(f"{len(rezepte)} Warenrezepte abgeleitet -> {ziel}")
    for name, r in rezepte.items():
        material, menge = next(iter(r["kosten"].items()))
        print(f"  {name}: {menge} {material}, {r['dauer']} s, {r['voraussetzungen']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
