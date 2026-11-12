"""Auswahl nach Aenderung (M2) - welche Pruefdateien ein Commit wirklich braucht.

Claudes Regel (Antwort Nr. 16, Teil B, M2). Warum sie noetig ist: `main` steht in **184 von 230**
Dateien in BETRIFFT; eine Auswahl nach Modul allein zieht bei jeder Zeile in `main.py` fast alles.
Darum wird fuer `main.py` nach FUNKTIONEN ausgewaehlt (Regel 6).

Die acht Regeln in Worten
-------------------------
1. Aenderung **nur in `docs/`** (ausser dem Protokoll) -> nur die Metawachen, Stufe 1.
2. Aenderung an `tests/harness.py` oder `tools/sammellauf.py` -> Stufe 3, alles ausser T4, denn der
   Pruefstand selbst ist beruehrt.
3. Geaenderte Pruefdatei -> laeuft selbst.
4. Geaenderte Datei in `data/` -> alle Dateien mit dieser Datei in `PRUEF_DATEN`.
5. Geaendertes Modul `x` (nicht `main`) -> alle Dateien mit `x` in `PRUEF_BETRIFFT`.
6. **`main.py`:** die geaenderten FUNKTIONEN werden bestimmt (`git diff -U0`, Zeilen dem umgebenden
   `def` zugeordnet, im alten UND neuen Stand). Ausgewaehlt werden Dateien mit `main:<funktion>` in
   BETRIFFT; `main:*` heisst "irgendeine Funktion" und zieht die Datei bei jeder Aenderung in
   `main.py`. Liegt eine Aenderung ausserhalb jeder Funktion (Modulebene, Importe, Konstanten),
   wird Stufe 3 empfohlen.
7. **Eine Stufe Aufrufer:** fuer jedes geaenderte Modul ausser `main` und ausser Hubs kommen die
   Module dazu, die es importieren - und davon nur Dateien der Stufen 1 und 2.
   Hubs sind Module mit mehr als 25 Dateien in BETRIFFT (aus den Koepfen gezaehlt, nicht gesetzt).
8. **Deckel:** liegt die geschaetzte Dauer ueber 120 s (Mediane aus `docs/audits/laeufe.jsonl`),
   laeuft die Auswahl nicht stillschweigend - sie empfiehlt Stufe 3 und meldet die Zahl.

Aufruf:
  python -X utf8 tools/auswahl.py --seit HEAD~1        # Aenderungen seit einem Commit
  python -X utf8 tools/auswahl.py --pfade src/welt.py  # Aenderungen von Hand nennen
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
import statistics
import subprocess
import sys

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS = os.path.join(HIER, "tests")
SRC = os.path.join(HIER, "src")
LAEUFE = os.path.join(HIER, "docs", "audits", "laeufe.jsonl")
PROTOKOLL = "docs/ENTWICKLUNGSPROTOKOLL.md"
META = ("test_pruefstand_kopf.py", "test_textqualitaet.py", "test_projektpfade.py",
        "test_m12_laeufe.py", "test_rot_historie.py", "test_faktenblatt.py")
T4 = ("test_produktionskette_ohne_cheats.py", "test_durchspiel.py", "test_overlay_ingame.py",
      "test_doppelpuffer.py", "test_bot_gruendung.py", "test_bot_takt_scheiben.py",
      "test_bot_warenkette.py", "test_kaserne_ohne_gebaeude.py")
HUB_GRENZE = 25
DECKEL_SEKUNDEN = 120.0
STUFE_META = 1
STUFE_ALLES = 3


# --------------------------------------------------------------------------
# 1. Koepfe, Hubs und Aufrufer
# --------------------------------------------------------------------------
def koepfe_lesen(tests_ordner: str = TESTS) -> dict:
    """{dateiname: kopf} fuer alle Pruefdateien - ueber `harness.kopf_lesen`, ohne Import."""
    sys.path.insert(0, tests_ordner)
    try:
        import harness
    except ImportError:
        return {}
    ergebnis = {}
    for name in sorted(os.listdir(tests_ordner)):
        if not (name.startswith("test_") and name.endswith(".py")):
            continue
        try:
            ergebnis[name] = harness.kopf_lesen(os.path.join(tests_ordner, name))
        except OSError:
            continue
    return ergebnis


def module_in(betrifft) -> set:
    """Die Modulnamen aus BETRIFFT (ohne `:funktion`)."""
    return {str(b).split(":", 1)[0] for b in betrifft or []}


def hubs_aus(koepfe: dict, grenze: int = HUB_GRENZE) -> set:
    """Module, die in mehr als `grenze` Dateien stehen - aus den Koepfen gezaehlt."""
    zaehler = {}
    for kopf in koepfe.values():
        for modul in module_in(kopf.get("betrifft")):
            zaehler[modul] = zaehler.get(modul, 0) + 1
    return {modul for modul, anzahl in zaehler.items() if anzahl > grenze}


def aufrufer_karte(src_ordner: str = SRC) -> dict:
    """{modul: {module, die es importieren}} aus den Importzeilen - ohne die Module zu laden."""
    karte = {}
    for name in sorted(os.listdir(src_ordner)):
        if not name.endswith(".py"):
            continue
        modul = name[:-3]
        try:
            with open(os.path.join(src_ordner, name), encoding="utf-8", errors="replace") as fh:
                quelle = fh.read()
        except OSError:
            continue
        try:
            baum = ast.parse(quelle)
        except SyntaxError:
            continue
        for knoten in ast.walk(baum):
            if isinstance(knoten, ast.Import):
                for alias in knoten.names:
                    ziel = alias.name.split(".")[0]
                    karte.setdefault(ziel, set()).add(modul)
            elif isinstance(knoten, ast.ImportFrom) and knoten.module:
                ziel = knoten.module.split(".")[0]
                karte.setdefault(ziel, set()).add(modul)
    return {k: v for k, v in karte.items() if k}


# --------------------------------------------------------------------------
# 2. Aenderungen (Git-Teil, duenn)
# --------------------------------------------------------------------------
def _git(*argumente, cwd=HIER) -> str:
    p = subprocess.run(["git"] + list(argumente), capture_output=True, text=True, cwd=cwd,
                       timeout=120)
    return (p.stdout or "") if p.returncode == 0 else ""


def _def_bereiche(quelle: str) -> list:
    """[(anfang, ende, name)] der Funktionen einer Quelldatei (1-basiert, inklusive)."""
    try:
        baum = ast.parse(quelle)
    except SyntaxError:
        return []
    bereiche = []
    for knoten in ast.walk(baum):
        if isinstance(knoten, (ast.FunctionDef, ast.AsyncFunctionDef)):
            bereiche.append((knoten.lineno, getattr(knoten, "end_lineno", knoten.lineno),
                             knoten.name))
    return sorted(bereiche)


def _zeilen_aus_diff(diff: str) -> tuple:
    """(alte Zeilen, neue Zeilen) als Mengen aus einem `git diff -U0`."""
    alt, neu = set(), set()
    for zeile in (diff or "").splitlines():
        treffer = re.match(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", zeile)
        if not treffer:
            continue
        a_start, a_anzahl = int(treffer.group(1)), int(treffer.group(2) or 1)
        n_start, n_anzahl = int(treffer.group(3)), int(treffer.group(4) or 1)
        alt.update(range(a_start, a_start + max(a_anzahl, 1)))
        neu.update(range(n_start, n_start + max(n_anzahl, 1)))
    return alt, neu


def main_funktionen(commit: str = "HEAD") -> tuple:
    """(Funktionsnamen, modulebene) der Aenderungen an `src/main.py` seit `commit`.

    `commit` ist der Stand VOR den Aenderungen (z. B. HEAD~1 oder der letzte gruene Commit).
    """
    diff = _git("diff", "-U0", commit, "--", "src/main.py")
    if not diff.strip():
        return set(), False
    alt_zeilen, neu_zeilen = _zeilen_aus_diff(diff)
    alt_quelle = _git("show", "%s:src/main.py" % commit)
    try:
        with open(os.path.join(SRC, "main.py"), encoding="utf-8", errors="replace") as fh:
            neu_quelle = fh.read()
    except OSError:
        neu_quelle = ""
    treffer = set()
    modulebene = False
    for bereiche, zeilen in ((_def_bereiche(alt_quelle), alt_zeilen),
                             (_def_bereiche(neu_quelle), neu_zeilen)):
        for nummer in zeilen:
            drin = [name for anfang, ende, name in bereiche if anfang <= nummer <= ende]
            if drin:
                treffer.update(drin)
            elif nummer > 0:
                modulebene = True
    return treffer, modulebene


def aenderungen_seit(commit: str = "HEAD") -> dict:
    """Die Aenderungen seit `commit` als Woerterbuch, wie `auswahl()` es braucht."""
    roh = _git("diff", "--name-only", commit)
    pfade = sorted(p.strip() for p in (roh or "").splitlines() if p.strip())
    neu = {"pfade": pfade, "datendateien": set(), "module": set(), "pruefdateien": set(),
           "main_funktionen": set(), "main_modulebene": False}
    for pfad in pfade:
        pfad = pfad.replace("\\", "/")
        if pfad.startswith("data/"):
            neu["datendateien"].add(os.path.basename(pfad))
        elif pfad.startswith("tests/") and os.path.basename(pfad).startswith("test_"):
            neu["pruefdateien"].add(os.path.basename(pfad))
        elif pfad.startswith("src/") and pfad.endswith(".py"):
            neu["module"].add(os.path.basename(pfad)[:-3])
    if "main" in neu["module"]:
        funktionen, modulebene = main_funktionen(commit)
        neu["main_funktionen"] = funktionen
        neu["main_modulebene"] = modulebene
    return neu


# --------------------------------------------------------------------------
# 3. Die Auswahl selbst (rein, ohne Git)
# --------------------------------------------------------------------------
def auswahl(aenderungen: dict, koepfe: dict, aufrufer: dict = None, hubs: set = None) -> tuple:
    """(sortierte Dateiliste, empfohlene Stufe) nach den acht Regeln aus Nr. 16."""
    aufrufer = aufrufer or {}
    hubs = hubs if hubs is not None else hubs_aus(koepfe)
    pfade = [str(p).replace("\\", "/") for p in aenderungen.get("pfade") or []]
    datendateien = set(aenderungen.get("datendateien") or [])
    module = set(aenderungen.get("module") or [])
    pruefdateien = set(aenderungen.get("pruefdateien") or [])
    main_funktionen = set(aenderungen.get("main_funktionen") or [])
    main_modulebene = bool(aenderungen.get("main_modulebene"))

    # Regel 1: nur docs/ (ausser dem Protokoll) -> Metawachen, Stufe 1
    if pfade and all(p.startswith("docs/") and p != PROTOKOLL for p in pfade):
        return sorted(set(META) & set(koepfe) or set(META)), STUFE_META
    # Regel 2: der Pruefstand selbst ist beruehrt
    if any(p in ("tests/harness.py", "tools/sammellauf.py") for p in pfade):
        return sorted(n for n in koepfe if n not in T4), STUFE_ALLES

    dateien = {n for n in pruefdateien if n in koepfe}          # Regel 3
    for name, kopf in koepfe.items():
        if set(kopf.get("daten") or []) & datendateien:        # Regel 4
            dateien.add(name)
        for eintrag in kopf.get("betrifft") or []:
            modul, _, funktion = str(eintrag).partition(":")
            if modul != "main":
                if modul in module:                            # Regel 5
                    dateien.add(name)
                continue
            # Regel 6: main nach FUNKTIONEN - nur wenn main.py ueberhaupt geaendert wurde
            if "main" not in module:
                continue
            if main_modulebene:
                return sorted(n for n in koepfe if n not in T4), STUFE_ALLES
            if funktion == "*" or funktion in main_funktionen:
                dateien.add(name)
    # Regel 7: eine Stufe Aufrufer, nur Stufen 1 und 2, nicht fuer main und nicht fuer Hubs
    for modul in module - {"main"} - hubs:
        for auf in aufrufer.get(modul, set()) - {"main"}:
            for name, kopf in koepfe.items():
                if auf in module_in(kopf.get("betrifft")) and int(kopf.get("stufe") or 3) <= 2:
                    dateien.add(name)
    dateien |= {n for n in META if n in koepfe}                 # Metawachen immer
    return sorted(dateien), 2


def geschaetzte_dauer(dateien, pfad: str = LAEUFE) -> float:
    """Summe der Median-Dauern aus `laeufe.jsonl` (0, wenn keine Zahl vorliegt)."""
    werte = {}
    try:
        with open(pfad, encoding="utf-8") as fh:
            for zeile in fh:
                zeile = zeile.strip()
                if not zeile:
                    continue
                try:
                    z = json.loads(zeile)
                except ValueError:
                    continue
                name, dauer = z.get("datei"), z.get("dauer")
                if not name or dauer is None:
                    continue
                werte.setdefault(name, []).append(float(dauer))
    except OSError:
        return 0.0
    summe = 0.0
    for name in dateien:
        if name in werte and werte[name]:
            summe += statistics.median(werte[name])
    return summe


def empfehlung(dateien, stufe: int, dauer: float) -> str:
    """Der Satz, den der Mensch liest - inklusive Deckel-Regel 8."""
    if dauer > DECKEL_SEKUNDEN and stufe < STUFE_ALLES:
        return ("Auswahl %d Dateien, %.0f s > %.0f s -> T3 empfohlen (Deckel, Regel 8)"
                % (len(dateien), dauer, DECKEL_SEKUNDEN))
    return "Auswahl %d Dateien, %.0f s -> T%d" % (len(dateien), dauer, stufe)


def main(argv=None) -> int:
    leser = argparse.ArgumentParser(description="Pruefdateien nach Aenderung auswaehlen (M2)")
    leser.add_argument("--seit", default="HEAD", help="Stand VOR den Aenderungen")
    leser.add_argument("--pfade", nargs="*", help="Aenderungen von Hand nennen")
    leser.add_argument("--nur-zeigen", action="store_true", help="nur rechnen, nichts laufen")
    args = leser.parse_args(argv)
    koepfe = koepfe_lesen()
    if not koepfe:
        print("Keine Koepfe lesbar - ist tests/harness.py in Ordnung?")
        return 2
    if args.pfade:
        aenderungen = {"pfade": args.pfade, "datendateien": set(), "module": set(),
                       "pruefdateien": set(), "main_funktionen": set(), "main_modulebene": False}
        for pfad in args.pfade:
            pfad = pfad.replace("\\", "/")
            if pfad.startswith("data/"):
                aenderungen["datendateien"].add(os.path.basename(pfad))
            elif pfad.startswith("src/") and pfad.endswith(".py"):
                aenderungen["module"].add(os.path.basename(pfad)[:-3])
    else:
        aenderungen = aenderungen_seit(args.seit)
    dateien, stufe = auswahl(aenderungen, koepfe, aufrufer_karte(), hubs_aus(koepfe))
    dauer = geschaetzte_dauer(dateien)
    print(empfehlung(dateien, stufe, dauer))
    for name in dateien:
        print("  %s" % name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
