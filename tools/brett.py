"""
Brett fuer die Unteragenten (nebenlaeufigkeitssicher).

Warum eine eigene Datei je Eintrag: `docs/BOARD.md` ist ein **Tagebuch** — es ist lesbar, aber
wenn zwei Kinder gleichzeitig schreiben, ueberschreibt einer den anderen (dieselbe Klasse Fehler
wie zwei Kinder in derselben Quelldatei). Deshalb gilt hier das Postfach-Muster:

  * **Ein Eintrag = eine Datei** in ``board/``: ``<zeit>_<agent>_<kurz>.md``.
    Schreiben ist damit ein reines Anlegen — kein Sperren, kein Ueberschreiben.
  * **Lesen = Ordner lesen** (nach Zeit sortiert). Was ein Kind geschrieben hat, sieht jedes
    andere beim naechsten Lesen.
  * ``docs/BOARD.md`` bleibt die **menschliche** Fassung: der Hauptagent traegt dort zusammen,
    was die Kinder gemeldet haben. Das Postfach ist die Maschinenfassung.

Benutzung (jedes Kind vor der Arbeit und danach):

    python tools/brett.py lesen                       # alle Eintraege, aelteste zuerst
    python tools/brett.py lesen --seit 2026-10-04     # nur neuere
    python tools/brett.py belegen --agent kind-a --dateien "src/a.py,tests/test_a.py" --text "baue das Modul a"
    python tools/brett.py melden  --agent kind-a --text "fertig: 42 Pruefungen gruen" --pruefung "42/0"
    python tools/brett.py freigeben --agent kind-a --text "Datei wieder frei"
    python tools/brett.py luecken                     # was noch offen ist (unfreigegebene Belegungen)

Regeln (stehen auch in docs/AGENTEN_PLAN.md): erst lesen, dann belegen, nie fremde Dateien
anfassen, danach melden und freigeben. Nur anhaengen — Eintraege werden nie umgeschrieben.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import time
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
BRETT = WURZEL / "board"

ARTEN = {"belegen": "BELEGT", "melden": "MELDUNG", "freigeben": "FREI", "hinweis": "HINWEIS"}


def _sicher(text: str, laenge: int = 40) -> str:
    """Ein kurzer, dateisicherer Teil aus einem Text (a-z, 0-9, -)."""
    sauber = re.sub(r"[^a-zA-Z0-9]+", "-", (text or "")).strip("-").lower()
    return (sauber[:laenge] or "eintrag")


def _dateien() -> list:
    if not BRETT.exists():
        return []
    return sorted(BRETT.glob("*.md"))


def _kopf(inhalt: str) -> dict:
    """Die Kopfzeilen eines Eintrags als dict (zwischen --- ... ---)."""
    daten = {}
    for zeile in inhalt.splitlines():
        if zeile.startswith("---"):
            continue
        if ":" in zeile:
            schluessel, wert = zeile.split(":", 1)
            daten[schluessel.strip()] = wert.strip()
    return daten


def schreibe(art: str, agent: str, text: str, dateien: str = "", pruefung: str = "") -> Path:
    """Legt EINEN Eintrag als eigene Datei an (kein Ueberschreiben, kein Sperren)."""
    BRETT.mkdir(exist_ok=True)
    jetzt = time.strftime("%Y-%m-%d_%H%M%S")
    ziel = BRETT / f"{jetzt}_{_sicher(agent)}_{_sicher(text, 24)}.md"
    while ziel.exists():                      # gleiche Sekunde: haengt eine Zahl an
        ziel = ziel.with_name(ziel.stem + "_x.md")
    inhalt = (
        "---\n"
        f"art: {ARTEN.get(art, art.upper())}\n"
        f"agent: {agent}\n"
        f"zeit: {time.strftime('%d.%m.%Y %H:%M:%S')}\n"
        f"dateien: {dateien}\n"
        f"pruefung: {pruefung}\n"
        "---\n\n"
        f"{text}\n"
    )
    ziel.write_text(inhalt, encoding="utf-8")
    return ziel


def lesen(seit: str = "") -> list:
    """Alle Eintraege, aelteste zuerst."""
    eintraege = []
    for pfad in _dateien():
        if seit and pfad.name < seit:
            continue
        eintraege.append((pfad.name, pfad.read_text(encoding="utf-8")))
    return eintraege


def luecken() -> list:
    """Belegungen ohne passende Freigabe — die offene Arbeit.

    Verglichen wird der Agentenname: wer sich belegt hat, muss sich freigeben.
    """
    belegt, frei = {}, set()
    for name, inhalt in lesen():
        kopf = _kopf(inhalt)
        art, agent = kopf.get("art", ""), kopf.get("agent", "")
        if art == "BELEGT":
            belegt.setdefault(agent, []).append((name, kopf.get("dateien", "")))
        elif art == "FREI":
            frei.add(agent)
    return [(agent, eintraege) for agent, eintraege in belegt.items() if agent not in frei]


def main() -> int:
    parser = argparse.ArgumentParser(description="Brett fuer die Unteragenten")
    befehle = parser.add_subparsers(dest="befehl", required=True)
    p_lesen = befehle.add_parser("lesen", help="alle Eintraege zeigen")
    p_lesen.add_argument("--seit", default="")
    for name in ("belegen", "melden", "hinweis"):
        p = befehle.add_parser(name)
        p.add_argument("--agent", required=True)
        p.add_argument("--text", required=True)
        p.add_argument("--dateien", default="")
        p.add_argument("--pruefung", default="")
    p_frei = befehle.add_parser("freigeben")
    p_frei.add_argument("--agent", required=True)
    p_frei.add_argument("--text", default="Arbeit beendet")
    befehle.add_parser("luecken", help="unfreigegebene Belegungen")

    args = parser.parse_args()

    if args.befehl == "lesen":
        eintraege = lesen(args.seit)
        if not eintraege:
            print("(noch keine Eintraege auf dem Brett)")
        for name, inhalt in eintraege:
            print("=" * 70)
            print(f"# {name}")
            print(inhalt.rstrip())
        return 0

    if args.befehl == "luecken":
        offen = luecken()
        if not offen:
            print("keine offenen Belegungen — alle Dateien sind frei")
        for agent, eintraege in offen:
            for name, dateien in eintraege:
                print(f"offen: {agent} (seit {name}) — {dateien}")
        return 0

    pfad = schreibe(args.befehl, args.agent, args.text,
                    getattr(args, "dateien", ""), getattr(args, "pruefung", ""))
    print(f"Eintrag angelegt: {pfad.relative_to(WURZEL)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
