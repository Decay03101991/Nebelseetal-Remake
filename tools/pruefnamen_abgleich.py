"""Pruefnamen-Abgleich auf den GEPRUEFTEN GEGENSTAND (F-83, Daniel 13.11.2026).

WOZU
----
Die 90-Prozent-Regel aus F-74 verglich Pruefnamen als deutsche Saetze. Zwei Dateien formulieren
denselben Gegenstand fast immer anders - deshalb erreichte kein Kandidat die Schwelle, auch wenn
inhaltlich alles doppelt war. Auf Daniels Wort („zusaetzlich auf den geprueften Gegenstand stuetzen
(Funktion oder Datenfeld je Pruefname), 90 % darauf rechnen“) misst dieses Werkzeug ZWEI Dinge:

1. **Wortlaut** - derselbe Pruefname als Zeichenkette.
2. **Gegenstand** - die Bezeichner, die IN DER BEDINGUNG der Pruefung wirklich gelesen werden
   (`spieloekonomie.WARENREZEPTE`, `state.settlements`, `main.rueckmarsch_eintrag` …). Zwei
   Pruefungen gelten als deckungsgleich, wenn sich ihre Gegenstands-Mengen zu mindestens
   `--jaccard` (Standard 0,6) ueberschneiden.

Die 90-Prozent-Regel wird auf den GEGENSTAND gerechnet (F-83) und zusaetzlich auf den Wortlaut
ausgegeben - damit man sieht, wie weit beide auseinanderliegen.

Aufruf
------
  python -X utf8 tools/pruefnamen_abgleich.py tests/test_ressourcenleiste.py tests/test_ressourcenleiste_t08.py
  python -X utf8 tools/pruefnamen_abgleich.py A B --json   # maschinenlesbar
  python -X utf8 tools/pruefnamen_abgleich.py A B --jaccard 0.5 --schwelle 90

Rueckgabe: 0 = Schwelle auf den Gegenstand erreicht, 1 = nicht erreicht, 2 = Aufruffehler.
"""
from __future__ import annotations

import argparse
import ast
import json
import sys
from typing import Dict, List, Optional, Set

# So heissen Zusicherungen in den Pruefdateien dieses Projekts.
PRUEF_NAMEN = {"check", "ok", "ck", "hcheck", "assert_check", "pruefe"}
# Rauschen, das kein Gegenstand ist.
OHNE = {
    "check", "ok", "ck", "hcheck", "pruefe", "self", "app", "root", "len", "str", "int", "float",
    "round", "abs", "all", "any", "sum", "min", "max", "range", "enumerate", "sorted", "list",
    "dict", "set", "tuple", "print", "True", "False", "None", "isinstance", "getattr", "hasattr",
    "open", "format", "bool", "repr", "zip", "map", "filter", "type", "id", "os", "sys", "json",
    "re", "tk", "Path", "tmp", "temp", "datei", "pfad", "text", "name", "wert", "detail", "wert_",
}


def _name_text(knoten: ast.AST) -> str:
    """Einen Bezeichner (auch `a.b.c`) als Text - sonst leer."""
    if isinstance(knoten, ast.Name):
        return knoten.id
    if isinstance(knoten, ast.Attribute):
        links = _name_text(knoten.value)
        return f"{links}.{knoten.attr}" if links else knoten.attr
    if isinstance(knoten, ast.Subscript):
        return _name_text(knoten.value)
    if isinstance(knoten, ast.Call):
        return _name_text(knoten.func)
    return ""


def _gegenstand(knoten: Optional[ast.AST]) -> Set[str]:
    """Alle gelesenen Bezeichner eines Ausdrucks, ohne Rauschen und ohne Literale."""
    out: Set[str] = set()
    if knoten is None:
        return out
    for kind in ast.walk(knoten):
        if isinstance(kind, ast.Attribute):
            text = _name_text(kind)
            if text:
                out.add(text)
        elif isinstance(kind, ast.Name):
            out.add(kind.id)
    # nur das laengste Glied jeder Kette behalten (`a.b` statt zusaetzlich `a`)
    kurz = set()
    for text in out:
        if any(text != anderes and text.startswith(anderes + ".") for anderes in out):
            kurz.add(text)
    out -= kurz
    return {t for t in out if t.split(".")[0] not in OHNE and len(t) > 2}


def _pruefungen(pfad: str) -> List[Dict[str, object]]:
    """Alle Zusicherungen einer Datei: Name (Text), Gegenstand (Menge), Zeile."""
    with open(pfad, "r", encoding="utf-8", errors="replace") as griff:
        quelle = griff.read()
    baum = ast.parse(quelle, filename=pfad)
    treffer: List[Dict[str, object]] = []

    def sammeln(knoten: ast.AST, name: str) -> None:
        args = list(knoten.args)                                  # type: ignore[attr-defined]
        # der Pruefname ist das erste Zeichenketten-Literal unter den Argumenten
        text = ""
        for arg in args:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                text = arg.value
                break
        # die Bedingung ist das erste Argument, das KEIN Zeichenketten-Literal ist
        bedingung = next((a for a in args if not (isinstance(a, ast.Constant)
                                                 and isinstance(a.value, str))), None)
        treffer.append({"name": text or f"(ohne Namen, Zeile {knoten.lineno})",
                        "zeile": knoten.lineno,
                        "gegenstand": sorted(_gegenstand(bedingung))})

    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Call):
            _f = _name_text(knoten.func).split(".")[-1]
            if _f in PRUEF_NAMEN:
                sammeln(knoten, _f)
        elif isinstance(knoten, ast.Assert):                     # nackte assert-Zeilen
            treffer.append({"name": f"(assert, Zeile {knoten.lineno})",
                            "zeile": knoten.lineno,
                            "gegenstand": sorted(_gegenstand(knoten.test))})
    return treffer


def _jaccard(a: Set[str], b: Set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / float(len(a | b))


def abgleich(kandidat: str, partner: str, schwelle_jaccard: float = 0.6) -> Dict[str, object]:
    """Deckung des Kandidaten durch den Partner - woertlich und auf den Gegenstand."""
    kand = _pruefungen(kandidat)
    part = _pruefungen(partner)
    woertlich: Set[str] = {str(p["name"]) for p in part}
    zeilen = []
    for pruef in kand:
        gegenstand = set(pruef["gegenstand"])                     # type: ignore[arg-type]
        treffer = None
        bester = 0.0
        for andere in part:
            wert = _jaccard(gegenstand, set(andere["gegenstand"]))  # type: ignore[arg-type]
            if wert > bester:
                bester, treffer = wert, andere
        zeilen.append({
            "name": pruef["name"],
            "zeile": pruef["zeile"],
            "gegenstand": sorted(gegenstand),
            "woertlich": str(pruef["name"]) in woertlich,
            "bester_partner": (treffer or {}).get("name", ""),
            "jaccard": round(bester, 3),
            "gedeckt": bester >= schwelle_jaccard,
        })
    n = len(zeilen) or 1
    return {
        "kandidat": kandidat,
        "partner": partner,
        "pruefungen_kandidat": len(zeilen),
        "pruefungen_partner": len(part),
        "woertlich": sum(1 for z in zeilen if z["woertlich"]),
        "gedeckt": sum(1 for z in zeilen if z["gedeckt"]),
        "prozent_woertlich": round(100.0 * sum(1 for z in zeilen if z["woertlich"]) / n, 1),
        "prozent_gegenstand": round(100.0 * sum(1 for z in zeilen if z["gedeckt"]) / n, 1),
        "schwelle_jaccard": schwelle_jaccard,
        "zeilen": zeilen,
    }


def main() -> int:
    bauer = argparse.ArgumentParser(description="Pruefnamen-Abgleich auf den geprueften Gegenstand (F-83)")
    bauer.add_argument("kandidat", help="Datei, die gestrichen werden soll")
    bauer.add_argument("partner", help="Datei, die sie ersetzen soll")
    bauer.add_argument("--jaccard", type=float, default=0.6,
                       help="ab welcher Gegenstands-Ueberschneidung eine Pruefung als gedeckt gilt (Standard 0,6)")
    bauer.add_argument("--schwelle", type=float, default=90.0,
                       help="geforderten Prozentsatz auf den Gegenstand (Standard 90)")
    bauer.add_argument("--json", action="store_true", help="maschinenlesbar ausgeben")
    bauer.add_argument("--alle", action="store_true", help="auch die gedeckten Pruefungen einzeln zeigen")
    args = bauer.parse_args()

    ergebnis = abgleich(args.kandidat, args.partner, args.jaccard)
    if args.json:
        print(json.dumps(ergebnis, ensure_ascii=False, indent=2))
    else:
        print("Pruefnamen-Abgleich auf den GEGENSTAND (F-83)")
        print("  Kandidat: %s (%d Pruefungen)" % (args.kandidat, ergebnis["pruefungen_kandidat"]))
        print("  Partner : %s (%d Pruefungen)" % (args.partner, ergebnis["pruefungen_partner"]))
        print("  Wortlaut    : %d von %d = %.1f %%"
              % (ergebnis["woertlich"], ergebnis["pruefungen_kandidat"], ergebnis["prozent_woertlich"]))
        print("  Gegenstand  : %d von %d = %.1f %% (Jaccard ab %.2f)"
              % (ergebnis["gedeckt"], ergebnis["pruefungen_kandidat"],
                 ergebnis["prozent_gegenstand"], args.jaccard))
        print("  Schwelle %.0f %% auf den Gegenstand: %s"
              % (args.schwelle, "ERREICHT" if ergebnis["prozent_gegenstand"] >= args.schwelle
                 else "NICHT ERREICHT"))
        print()
        print("  %-4s %-6s %-5s %-5s %s" % ("Zeile", "gedeckt", "Wort", "Jac.", "Pruefname"))
        for zeile in ergebnis["zeilen"]:                          # type: ignore[union-attr]
            if zeile["gedeckt"] and not args.alle:
                continue
            print("  %-4d %-7s %-5s %-5.2f %s"
                  % (zeile["zeile"], "ja" if zeile["gedeckt"] else "NEIN",
                     "ja" if zeile["woertlich"] else "nein", zeile["jaccard"], zeile["name"][:78]))
        print()
        print("  (nur ungedeckte Zeilen; --alle zeigt alle, --json die Gegenstaende je Pruefung)")

    return 0 if ergebnis["prozent_gegenstand"] >= args.schwelle else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as fehler:                                   # noqa: BLE001
        print("FEHLER beim Abgleich: %r" % (fehler,), file=sys.stderr)
        raise SystemExit(2)
