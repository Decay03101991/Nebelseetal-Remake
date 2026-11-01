"""Kleiner Pruefrahmen ohne Zusatzpakete.

Unterscheidet bewusst zwei Dinge:
  FEHLER  = etwas ist kaputt (Ausnahme, falsche Anzahl) -> muss behoben werden
  BEFUND  = bekannte Luecke im Ist-Stand -> wird gemeldet, faerbt aber nicht rot
Damit ein gruener Lauf nicht faelschlich "alles fertig" bedeutet.
"""
from __future__ import annotations

import sys
import traceback

_fehler: list[str] = []
_befunde: list[str] = []
_ok: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> bool:
    if cond:
        _ok.append(name)
        print(f"  OK     {name}" + (f" — {detail}" if detail else ""))
    else:
        _fehler.append(f"{name} {detail}".strip())
        print(f"  FEHLER {name}" + (f" — {detail}" if detail else ""))
    return bool(cond)


def befund(name: str, detail: str = "") -> None:
    """Bekannte Luecke: melden, nicht als Fehler zaehlen."""
    _befunde.append(f"{name} {detail}".strip())
    print(f"  BEFUND {name}" + (f" — {detail}" if detail else ""))


def abschnitt(titel: str) -> None:
    print(f"\n=== {titel} ===")


def ausnahme(name: str, fn):
    """Fuehrt fn aus und meldet eine Ausnahme als Fehler statt abzustuerzen."""
    try:
        return fn()
    except Exception as e:
        _fehler.append(f"{name}: {e!r}")
        print(f"  FEHLER {name} — Ausnahme {e!r}")
        traceback.print_exc()
        return None


def angriff_mit_marsch(app, ziel_name: str, verteidiger, wall_stufe: int = 0,
                       wall_zustand: float = 100.0, vorraete=None,
                       verteidiger_karren=None, vorrat_ziel=None, entfernung=None):
    """Einen Angriff als AUFTRAG starten und bis zur Heimkehr laufen lassen.

    ENTSCHEIDUNG 1 (Daniel, 01.11.2026): es gibt keinen Sofortangriff mehr - jeder Angriff
    reist. Dieser Helfer bildet den Marsch in der Pruefung ab, ohne eine Zeit zu erfinden: er
    springt genau auf die Rueckkehrzeit des Auftrags und laesst den Kern buchen
    (Ankunft -> `kampf_am_ziel`, Rueckkehr -> `einsatz_zurueck`).

    Rueckgabe wie beim Start: True, wenn der Auftrag wirklich unterwegs ist. Ohne Truppen
    oder bei fehlender Siedlung kommt False zurueck und es wird nichts gebucht.
    """
    ok = app._angriff_auftrag_starten(ziel_name, verteidiger, wall_stufe=wall_stufe,
                                      wall_zustand=wall_zustand, vorraete=vorraete,
                                      verteidiger_karren=verteidiger_karren,
                                      vorrat_ziel=vorrat_ziel, entfernung=entfernung)
    if not ok:
        return ok
    eintrag = app.state.auftraege[-1]
    ende = float(eintrag.get("rueckkehr") or eintrag.get("ankunft") or 0.0) + 1.0
    app.state.spielsekunden = max(float(app.state.spielsekunden), ende)
    app.state.auftraege_fortschreiben(app.state.spielsekunden)
    return ok


def bericht() -> int:
    print("\n" + "=" * 58)
    print(f"ERGEBNIS: {len(_ok)} bestanden, {len(_fehler)} Fehler, {len(_befunde)} Befunde")
    if _befunde:
        print("\nBefunde (bekannte Luecken, kein Fehler):")
        for b in _befunde:
            print("  -", b)
    if _fehler:
        print("\nFehler (muessen behoben werden):")
        for f in _fehler:
            print("  -", f)
    print("=" * 58)
    return 1 if _fehler else 0


# Projektwurzel und src in den Suchpfad
def projektwurzel():
    import os
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def import_src():
    import os
    root = projektwurzel()
    src = os.path.join(root, "src")
    for p in (root, src):
        if p not in sys.path:
            sys.path.insert(0, p)
    return root, src
