"""Misst, wie gut die Quelldateien fuer Menschen lesbar sind (Daniel, 31.10.2026).

Frage: "in den reinen Codes soll kurz beschrieben werden, was die einzelnen Codes fuer Aufgaben
erfuellen - damit es auch Anfaenger verstehen". Dieses Werkzeug sagt, WO das schon gut ist und
wo nicht - damit die Arbeit nicht blind ueber 20.000 Zeilen geht.

Gemessen wird je Datei:
  * Zeilen gesamt, Kommentarzeilen (#), Docstring-Zeilen, Code-Zeilen
  * Funktionen/Klassen gesamt und wie viele davon einen Docstring haben
  * ob die Datei einen Modul-Docstring hat (der erste Satz sagt, wozu die Datei da ist)

Aufruf:
    python -X utf8 tools/kommentar_luecken.py            # Uebersicht + schwaechste Dateien
    python -X utf8 tools/kommentar_luecken.py --liste     # jede Funktion ohne Docstring
"""
from __future__ import annotations

import ast
import io
import os
import sys
import tokenize

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HIER, "src")


def messen(pfad: str) -> dict:
    with open(pfad, encoding="utf-8") as f:
        text = f.read()
    zeilen = text.splitlines()
    kommentar = sum(1 for z in zeilen if z.strip().startswith("#"))
    doc_zeilen = 0
    try:
        for tok in tokenize.generate_tokens(io.StringIO(text).readline):
            if tok.type == tokenize.STRING and tok.string.lstrip().startswith(('"""', "'''")):
                doc_zeilen += tok.end[0] - tok.start[0] + 1
    except tokenize.TokenError:
        pass
    try:
        baum = ast.parse(text)
    except SyntaxError:
        return {"datei": pfad, "fehler": "SyntaxError"}
    funktionen = []

    def sammeln(knoten, tiefe=0):
        for kind in ast.walk(knoten):
            if isinstance(kind, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                funktionen.append({
                    "name": kind.name,
                    "zeile": kind.lineno,
                    "doc": bool(ast.get_docstring(kind)),
                })

    sammeln(baum)
    return {
        "datei": os.path.basename(pfad),
        "zeilen": len(zeilen),
        "kommentar": kommentar,
        "doc_zeilen": doc_zeilen,
        "modul_doc": bool(ast.get_docstring(baum)),
        "funktionen": funktionen,
        "ohne_doc": [f for f in funktionen if not f["doc"]],
    }


def main() -> int:
    liste = "--liste" in sys.argv
    dateien = sorted(f for f in os.listdir(SRC) if f.endswith(".py"))
    ergebnisse = [messen(os.path.join(SRC, f)) for f in dateien]
    ergebnisse = [e for e in ergebnisse if "fehler" not in e]
    gesamt_f = sum(len(e["funktionen"]) for e in ergebnisse)
    ohne = sum(len(e["ohne_doc"]) for e in ergebnisse)
    ohne_modul = [e["datei"] for e in ergebnisse if not e["modul_doc"]]
    print(f"Dateien: {len(ergebnisse)} | Funktionen/Klassen: {gesamt_f} | ohne Docstring: {ohne} "
          f"({ohne / max(1, gesamt_f) * 100:.0f} %)")
    print(f"Ohne Modul-Docstring (wofuer ist die Datei da?): {len(ohne_modul)} -> {', '.join(ohne_modul)}")
    print()
    print(f"{'Datei':32s} {'Zeilen':>6s} {'#':>5s} {'Doc':>5s} {'Funkt':>5s} {'ohne':>5s}")
    for e in sorted(ergebnisse, key=lambda x: -len(x["ohne_doc"])):
        print(f"{e['datei']:32s} {e['zeilen']:6d} {e['kommentar']:5d} {e['doc_zeilen']:5d} "
              f"{len(e['funktionen']):5d} {len(e['ohne_doc']):5d}")
    if liste:
        print("\nFunktionen ohne Docstring:")
        for e in ergebnisse:
            for f in e["ohne_doc"]:
                print(f"  {e['datei']}:{f['zeile']:5d}  {f['name']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
