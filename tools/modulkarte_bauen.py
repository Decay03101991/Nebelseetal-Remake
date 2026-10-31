"""Baut docs/MODULKARTE.md aus dem echten Code (31.10.2026).

Zweck: Eine Seite, die sagt, welche Datei wofuer da ist und wer wen aufruft. Nutzen:
  * Daniel kann nachlesen, wo eine Aufgabe hingehoert.
  * Ein Modell-Lauf braucht spaeter diese Karte + eine Datei statt des ganzen Projekts
    (kleinerer Kontext = billiger und treffsicherer).

Die Karte wird NICHT von Hand gepflegt, sondern erzeugt:
    python -X utf8 tools/modulkarte_bauen.py
"""
from __future__ import annotations

import ast
import os

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HIER, "src")
ZIEL = os.path.join(HIER, "docs", "MODULKARTE.md")


def zweck(baum) -> str:
    doku = ast.get_docstring(baum) or ""
    for zeile in doku.split("\n"):
        zeile = zeile.strip()
        if zeile:
            return zeile
    return "(kein Docstring)"


def main() -> int:
    dateien = sorted(f for f in os.listdir(SRC) if f.endswith(".py"))
    module = {f[:-3]: f for f in dateien}
    daten = {}
    for f in dateien:
        pfad = os.path.join(SRC, f)
        with open(pfad, encoding="utf-8") as fh:
            text = fh.read()
        baum = ast.parse(text)
        importe = set()
        for knoten in ast.walk(baum):
            if isinstance(knoten, ast.Import):
                importe.update(a.name.split(".")[0] for a in knoten.names)
            elif isinstance(knoten, ast.ImportFrom) and knoten.module and knoten.level == 0:
                importe.add(knoten.module.split(".")[0])
        eigene = sorted(i for i in importe if i in module and i != f[:-3])
        funktionen = [n.name for n in baum.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))]
        daten[f] = {"zweck": zweck(baum), "importiert": eigene,
                    "zeilen": len(text.split("\n")), "namen": len(funktionen)}

    nutzer = {f[:-3]: [] for f in dateien}
    for f, d in daten.items():
        for ziel in d["importiert"]:
            nutzer.setdefault(ziel, []).append(f)

    zeilen = [
        "# Modulkarte — welche Datei wofür, und wer wen aufruft\n\n",
        "**Erzeugt von `tools/modulkarte_bauen.py` — nicht von Hand ändern.** Stand: siehe Git-Historie.\n\n",
        f"{len(dateien)} Dateien in `src/`, "
        f"{sum(d['zeilen'] for d in daten.values())} Zeilen, "
        f"{sum(d['namen'] for d in daten.values())} Funktionen und Klassen auf oberster Ebene.\n\n",
        "## Die Karte\n\n",
        "| Datei | Zeilen | Zweck (erste Zeile des Docstrings) | wird gebraucht von |\n",
        "|---|---:|---|---|\n",
    ]
    for f in sorted(dateien, key=lambda x: -daten[x]["zeilen"]):
        wer = ", ".join(sorted(nutzer.get(f[:-3], []))) or "— (Einstieg oder ungenutzt)"
        zeilen.append(f"| `{f}` | {daten[f]['zeilen']} | {daten[f]['zweck']} | {wer} |\n")

    zeilen.append("\n## Lesart der Spalte „wird gebraucht von\"\n\n")
    zeilen.append("Steht dort `—`, ist die Datei entweder der Einstieg (`main.py`) oder sie wird von "
                  "niemandem mehr importiert (möglicher Rest, siehe `tools/code_mass.py`).\n")
    with open(ZIEL, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("".join(zeilen))
    print(f"Modulkarte geschrieben: {ZIEL} ({len(dateien)} Dateien)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
