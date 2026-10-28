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
