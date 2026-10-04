#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pruefe_verdrahtung.py

Beweist aus dem TEXT von src/main.py, welche Projektmodule wirklich in die GUI
einghaengt sind - und welche nur importiert oder gar nicht eingebunden sind.
Zusaetzlich: zweite Wahrheit (Formeln/Konstanten) und doppelte Definitionen.

Es wird NICHTS importiert (main.py wird nur als Text gelesen).
Reine Standardbibliothek.

Aufruf:    python -X utf8 tools/pruefe_verdrahtung.py
Rueckgabe: 0 = alles verdrahtet und sauber, 1 = etwas zu tun.
"""

from __future__ import annotations

import os
import re
import sys

# Die Module, die laut Projektauftrag in src/main.py einghaengt sein muessen.
MODULE = [
    "spieldaten", "einheiten", "kampf", "kampfbericht", "gebaeude_wirkung",
    "punkte", "speichern", "portalraum", "werkstatt", "auftraege", "botkern",
    "forschung", "welt", "gelaende", "wirtschaft", "berater", "tor",
]

# Formeln/Konstanten, die aus den Modulen kommen sollen und in main.py eine
# ZWEITE Wahrheit waeren. Wortgetreue Suche.
DOPPELTE_WAHRHEIT = [
    "player_power",
    "defense_power",
    "self.state.score + self.state.ruf",
    "json.dump(data",
    "MAPS[",
    "min(20, len(UNITS))",
]

MAX_NAMEN_IN_TABELLE = 3


def projektwurzel() -> str:
    hier = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(hier)


def lies(pfad: str) -> str:
    with open(pfad, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def finde_importe(main_zeilen) -> set:
    """Namen, die main.py importiert ('import x' und 'from x import ...')."""
    namen = set()
    for z in main_zeilen:
        s = z.strip()
        if s.startswith("import "):
            rest = s[len("import "):].split("#", 1)[0]
            for teil in rest.split(","):
                teil = teil.split(" as ")[0].strip()
                name = teil.split(".")[0]
                if re.match(r"^[A-Za-z_]\w*$", name):
                    namen.add(name)
        elif s.startswith("from "):
            rest = s[len("from "):].split("#", 1)[0].strip()
            if " import " in rest:
                mod = rest.split(" import ", 1)[0].strip().split(".")[0]
                if re.match(r"^[A-Za-z_]\w*$", mod):
                    namen.add(mod)
    return namen


def oeffentliche_funktionen(text: str) -> list:
    """Oeffentliche Funktionen = Zeilen, die mit 'def ' beginnen, ohne '_'."""
    namen = []
    for z in text.splitlines():
        if z.startswith("def "):
            m = re.match(r"def\s+([A-Za-z_]\w*)\s*\(", z)
            if m and not m.group(1).startswith("_"):
                namen.append(m.group(1))
    return namen


def aufgerufene_funktionen(main_text: str, modul: str, funktionen) -> dict:
    """{funktion: erste_zeilennummer} fuer 'modul.funktion(' in main.py."""
    treffer = {}
    for f in funktionen:
        muster = re.compile(
            r"(?<![\w.])" + re.escape(modul) + r"\." + re.escape(f) + r"\s*\(")
        m = muster.search(main_text)
        if m:
            zeile = main_text.count("\n", 0, m.start()) + 1
            treffer[f] = zeile
    return treffer


def pruefe_doppelte_defs(main_zeilen):
    """Findet 'def NAME' je Gueltigkeitsbereich (Modul oder Klasse).

    Doppelt im SELBEN Bereich = echter Fehler (Python nimmt stumm die letzte
    Fassung). Gleicher Name in VERSCHIEDENEN Klassen ist zulaessig (z.B. die
    Methode __init__ je Klasse) und wird nur als Hinweis gemeldet.
    """
    stack = []            # (einschub, bereichsname)
    defs = []             # (bereich, name, zeilennummer)
    for i, z in enumerate(main_zeilen, 1):
        s = z.strip()
        if not s or s.startswith("#"):
            continue
        roh = z[:len(z) - len(z.lstrip())]
        einschub = len(roh.expandtabs(4))
        while stack and stack[-1][0] >= einschub:
            stack.pop()
        if s.startswith("def "):
            m = re.match(r"def\s+([A-Za-z_]\w*)", s)
            if m:
                name = m.group(1)
                bereich = stack[-1][1] if stack else "@modul"
                defs.append((bereich, name, i))
                stack.append((einschub, name))
        elif s.startswith("class "):
            m = re.match(r"class\s+([A-Za-z_]\w*)", s)
            if m:
                stack.append((einschub, "class:" + m.group(1)))
    return defs


def main() -> int:
    wurzel = projektwurzel()
    main_pfad = os.path.join(wurzel, "src", "main.py")
    print("Nebelseetal Remake - Verdrahtungspruefung (Textbeweis)")
    if not os.path.isfile(main_pfad):
        print("FEHLER: src/main.py nicht gefunden: " + main_pfad)
        return 1
    main_text = lies(main_pfad)
    main_zeilen = main_text.splitlines()
    print("Quelle: src/main.py (%d Zeilen)" % len(main_zeilen))

    importe = finde_importe(main_zeilen)

    # ---- Daten je Modul sammeln ----
    daten = []
    for modul in MODULE:
        modul_pfad = os.path.join(wurzel, "src", modul + ".py")
        if os.path.isfile(modul_pfad):
            funktionen = oeffentliche_funktionen(lies(modul_pfad))
        else:
            funktionen = []
        importiert = modul in importe
        treffer = aufgerufene_funktionen(main_text, modul, funktionen)
        if not importiert:
            status = "NICHT-EINGEBUNDEN"
        elif not treffer:
            status = "NUR-IMPORTIERT"
        else:
            status = "VERDRAHTET"
        daten.append({
            "modul": modul,
            "importiert": importiert,
            "treffer": treffer,
            "status": status,
        })

    # ---- Tabelle ----
    print("")
    print("Modul                 Import  Aufgerufene Funktionen" + " " * 14 + "Status")
    print("-" * 21 + " " + "-" * 6 + "  " + "-" * 38 + " " + "-" * 19)
    for d in daten:
        namen = sorted(d["treffer"].items(), key=lambda kv: (kv[1], kv[0]))
        kurz = [n for n, _ in namen[:MAX_NAMEN_IN_TABELLE]]
        if len(namen) > MAX_NAMEN_IN_TABELLE:
            kurz.append("+%d weitere" % (len(namen) - MAX_NAMEN_IN_TABELLE))
        text = ", ".join(kurz) if kurz else "-"
        if len(text) > 38:
            text = text[:35] + "..."
        print("%-21s %-6s  %-38s %s" % (
            d["modul"], "ja" if d["importiert"] else "nein", text, d["status"]))

    # ---- Verdrahtungsinventar ----
    print("")
    print("Verdrahtungsinventar (modul -> erster Aufruf in main.py)")
    for d in daten:
        if d["status"] == "VERDRAHTET":
            namen = sorted(d["treffer"].items(), key=lambda kv: (kv[1], kv[0]))
            fn, zeile = namen[0]
            print("  %-20s %s.%s(  -> Zeile %d" % (d["modul"], d["modul"], fn, zeile))

    # ---- Zweite Wahrheit ----
    print("")
    print("WARNUNGEN: moegliche zweite Wahrheit in main.py")
    treffer_gesamt = 0
    ohne = []
    for muster in DOPPELTE_WAHRHEIT:
        laenge = len(re.findall(re.escape(muster), main_text))
        if laenge == 0:
            ohne.append(muster)
            continue
        for i, z in enumerate(main_zeilen, 1):
            if muster in z:
                print("  WARNUNG [%s] Zeile %d" % (muster, i))
                treffer_gesamt += 1
    print("  Summe Treffer: %d" % treffer_gesamt)
    if ohne:
        print("  ohne Treffer: " + ", ".join(ohne))

    # ---- Doppelte Definitionen ----
    print("")
    print("Doppelte Definitionen in main.py")
    defs = pruefe_doppelte_defs(main_zeilen)
    pro_bereich = {}
    for bereich, name, zeile in defs:
        pro_bereich.setdefault((bereich, name), []).append(zeile)
    echte_dups = []
    for (bereich, name), zl in sorted(pro_bereich.items()):
        if len(zl) > 1:
            echte_dups.append((name, bereich, zl))
    if echte_dups:
        for name, bereich, zl in echte_dups:
            print("  FEHLER '%s' %dx im selben Bereich '%s' (Zeilen %s)"
                  % (name, len(zl), bereich, ", ".join(str(x) for x in zl)))
    else:
        print("  OK: keine Namenskollision im selben Bereich")

    namen_nach_bereich = {}
    for bereich, name, zeile in defs:
        namen_nach_bereich.setdefault(name, set()).add(bereich)
    mehrfach = sorted(n for n, b in namen_nach_bereich.items() if len(b) > 1)
    if mehrfach:
        print("  HINWEIS (kein Fehler): Name in mehreren Bereichen: "
              + ", ".join(mehrfach))

    # ---- Ergebnis ----
    verdrahtet = sum(1 for d in daten if d["status"] == "VERDRAHTET")
    nur_import = sum(1 for d in daten if d["status"] == "NUR-IMPORTIERT")
    nicht = sum(1 for d in daten if d["status"] == "NICHT-EINGEBUNDEN")
    fehler = bool(echte_dups) or (nur_import + nicht) > 0

    print("")
    print("ERGEBNIS: %d verdrahtet, %d nur importiert, %d nicht eingebunden"
          % (verdrahtet, nur_import, nicht))
    print("Rueckgabewert: %d (0 = keine Fehler)" % (1 if fehler else 0))
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())
