"""Misst den Spielcode und findet die Fettstellen (Stufe 0 der Aufraeumrunde, 31.10.2026).

Daniels Frage: "es ist immer wieder neuer Code hinzugefuegt worden, aber nie darauf geachtet
worden, Funktionen klug zusammen zu fuehren." Dieses Werkzeug beantwortet: WO ist das passiert?

Gemessen wird je Datei und insgesamt:
  * Zeilen gesamt / Codezeilen (ohne Leerzeilen, Kommentare, Docstrings)
  * Funktionen und Klassen, laengste Funktion
  * Funktionen ab 40 Zeilen (Kandidaten zum Aufteilen) und ab 60 (dringend)
  * doppelte Bloecke: 6 aufeinanderfolgende Codezeilen, die woanders genauso stehen
  * Importe, die im Code nicht benutzt werden
  * Module, die von niemandem importiert werden (moegliche Reste)

Aufruf:
    python -X utf8 tools/code_mass.py                # Uebersicht + Rangliste
    python -X utf8 tools/code_mass.py --duplikate    # doppelte Bloecke mit Fundstellen
    python -X utf8 tools/code_mass.py --lang         # alle Funktionen ab 40 Zeilen
"""
from __future__ import annotations

import ast
import collections
import io
import os
import sys
import tokenize

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HIER, "src")


def zaehle(pfad: str) -> dict:
    with open(pfad, encoding="utf-8") as f:
        text = f.read()
    zeilen = text.split("\n")
    try:
        baum = ast.parse(text)
    except SyntaxError as fehler:
        return {"datei": os.path.basename(pfad), "fehler": str(fehler)}
    doc_zeilen = set()
    for knoten in ast.walk(baum):
        if isinstance(knoten, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)) \
                and ast.get_docstring(knoten):
            erste = knoten.body[0]
            doc_zeilen.update(range(erste.lineno, (erste.end_lineno or erste.lineno) + 1))
    kommentar_zeilen = set()
    try:
        for tok in tokenize.generate_tokens(io.StringIO(text).readline):
            if tok.type == tokenize.COMMENT:
                kommentar_zeilen.add(tok.start[0])
    except tokenize.TokenError:
        pass
    leer = {i for i, z in enumerate(zeilen, start=1) if not z.strip()}
    code_zeilen = len(zeilen) - len(leer - doc_zeilen) - len(kommentar_zeilen)
    funktionen = []
    for knoten in ast.walk(baum):
        if isinstance(knoten, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funktionen.append((knoten.name, knoten.lineno,
                               (knoten.end_lineno or knoten.lineno) - knoten.lineno + 1))
    importe = []
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Import):
            importe += [(a.asname or a.name.split(".")[0], a.name) for a in knoten.names]
        elif isinstance(knoten, ast.ImportFrom) and knoten.module and knoten.level == 0:
            for a in knoten.names:
                importe.append((a.asname or a.name, knoten.module))
    rumpf = "\n".join(z for i, z in enumerate(zeilen, start=1) if i not in kommentar_zeilen)
    ungenutzt = [name for name, _ in importe
                 if len([1 for m in __import__("re").finditer(r"\b" + __import__("re").escape(name) + r"\b", rumpf)]) <= 1]
    return {
        "datei": os.path.basename(pfad), "zeilen": len(zeilen), "code": max(0, code_zeilen),
        "kommentar": len(kommentar_zeilen), "doku": len(doc_zeilen),
        "funktionen": funktionen, "ungenutzt": ungenutzt,
    }


def main() -> int:
    dateien = sorted(f for f in os.listdir(SRC) if f.endswith(".py"))
    daten = [zaehle(os.path.join(SRC, f)) for f in dateien]
    daten = [d for d in daten if "fehler" not in d]
    alle_f = [(d["datei"], n, l, z) for d in daten for n, l, z in d["funktionen"]]
    lang40 = [x for x in alle_f if x[3] >= 40]
    lang60 = [x for x in alle_f if x[3] >= 60]

    print(f"Dateien: {len(daten)} | Zeilen: {sum(d['zeilen'] for d in daten)} | "
          f"Codezeilen: {sum(d['code'] for d in daten)} | Funktionen: {len(alle_f)}")
    print(f"Funktionen ab 40 Zeilen: {len(lang40)} | ab 60 Zeilen: {len(lang60)}")
    print(f"\n{'Datei':34s} {'Zeilen':>6s} {'Code':>6s} {'Funkt':>6s} {'laengste':>8s}")
    for d in sorted(daten, key=lambda x: -x["code"]):
        laengste = max([z for _, _, z in d["funktionen"]], default=0)
        print(f"{d['datei']:34s} {d['zeilen']:6d} {d['code']:6d} {len(d['funktionen']):6d} {laengste:8d}")

    print("\nLaengste Funktionen (Kandidaten zum Aufteilen):")
    for datei, name, zeile, z in sorted(lang60, key=lambda x: -x[3])[:12]:
        print(f"  {z:4d} Zeilen  {datei}:{zeile}  {name}")

    ungenutzt = [(d["datei"], u) for d in daten for u in d["ungenutzt"]]
    if ungenutzt:
        print(f"\nImporte, die nicht benutzt werden ({len(ungenutzt)}):")
        for datei, name in ungenutzt[:15]:
            print(f"  {datei}: {name}")

    importiert = set()
    for datei in dateien:
        with open(os.path.join(SRC, datei), encoding="utf-8") as f:
            t = f.read()
        for d in daten:
            modul = d["datei"][:-3]
            if modul != datei[:-3] and ("import " + modul) in t:
                importiert.add(modul)
    reste = [d["datei"] for d in daten if d["datei"][:-3] not in importiert
             and d["datei"] not in ("main.py",)]
    if reste:
        print(f"\nVon niemandem importiert (moegliche Reste, main.py ist Einstieg): {', '.join(reste)}")

    if "--lang" in sys.argv:
        print("\nAlle Funktionen ab 40 Zeilen:")
        for datei, name, zeile, z in sorted(lang40, key=lambda x: -x[3]):
            print(f"  {z:4d}  {datei}:{zeile}  {name}")

    if "--duplikate" in sys.argv:
        bloecke = collections.defaultdict(list)
        for d in daten:
            with open(os.path.join(SRC, d["datei"]), encoding="utf-8") as f:
                z = [s.strip() for s in f.read().split("\n")]
            for i in range(len(z) - 5):
                stueck = tuple(z[i:i + 6])
                if all(stueck) and sum(len(s) for s in stueck) > 120:
                    bloecke[stueck].append((d["datei"], i + 1))
        mehrfach = [(f, k) for k, f in bloecke.items() if len(f) > 1]
        print(f"\nDoppelte 6-Zeilen-Bloecke: {len(mehrfach)}")
        for fundstellen, block in sorted(mehrfach, key=lambda x: -len(x[0]))[:12]:
            orte = ", ".join(f"{d}:{l}" for d, l in fundstellen[:4])
            print(f"  {len(fundstellen)}x {orte}")
            print(f"      {block[0][:100]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
