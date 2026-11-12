"""Auftraege gegen das Faktenblatt pruefen (M11) - gegen abgetippte Zahlen in Rezepten.

Der Befund (Claude, Antwort Nr. 16): in den Auftraegen Nr. 12 bis 15 standen "vier Zutaten",
"18 Waren" und "2148 px Dorfzentrum". Alle drei kamen aus dem Gedaechtnis, keine aus `data/`.
Dieses Werkzeug sucht im Text Muster wie "18 Waren", "4 Zutaten", "21 Forschungen" und vergleicht
sie mit `docs/faktenblatt.json`. Abweichung = Warnung mit der richtigen Zahl.

Aufruf:
  python -X utf8 tools/auftrag_pruefen.py docs/auftraege/AUFTRAG_....md
  python -X utf8 tools/auftrag_pruefen.py --text "Der Auftrag nennt 18 Waren."
Rueckgabewert: 0 = keine Abweichung, 1 = mindestens eine Abweichung, 2 = Aufruffehler.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAKTEN = os.path.join(HIER, "docs", "faktenblatt.json")

# Wort -> Schluessel im Faktenblatt. Reihenfolge egal, laengere Woerter zuerst, damit
# "Forschungen" nicht als "Forschung" halb erkannt wird.
BEGRIFFE = {
    "waren": "waren",
    "rezepte": "rezepte",
    "einheiten": "einheiten",
    "forschungen": "forschungen",
    "gebaeude": "gebaeude",
    "völker": "voelker",
    "voelker": "voelker",
    "welten": "welten",
    "gelaendearten": "gelaendearten",
    "zutaten": "zutaten",
}
MUSTER = re.compile(r"(?<![\d.,])(\d{1,6})\s+(" +
                    "|".join(sorted(BEGRIFFE, key=len, reverse=True)) + r")\b", re.I)


def sollwerte(fakten: dict) -> dict:
    """{begriff: sollzahl} aus dem Faktenblatt - inklusive der hoechsten Zutatenzahl."""
    z = fakten.get("zaehlung") or fakten
    return {
        "waren": (z.get("waren") or {}).get("anzahl"),
        "rezepte": (z.get("rezepte") or {}).get("anzahl"),
        "einheiten": (z.get("einheiten") or {}).get("anzahl"),
        "forschungen": (z.get("forschungen") or {}).get("anzahl"),
        "gebaeude": (z.get("gebaeude") or {}).get("anzahl"),
        "voelker": (z.get("voelker") or {}).get("anzahl"),
        "welten": (z.get("welten") or {}).get("anzahl"),
        "gelaendearten": (z.get("gelaendearten") or {}).get("anzahl"),
        "zutaten": (z.get("rezepte") or {}).get("hoechste_zutaten_je_rezept"),
    }


def pruefen(text: str, fakten: dict) -> list:
    """Alle Zahlen im Text gegen das Faktenblatt halten.

    Rueckgabe je Fund: {"stelle", "begriff", "genannt", "richtig"} - nur ABWEICHUNGEN.
    """
    soll = sollwerte(fakten)
    treffer = []
    for m in MUSTER.finditer(text or ""):
        genannt = int(m.group(1))
        wort = m.group(2).lower()
        schluessel = BEGRIFFE.get(wort)
        if schluessel is None:
            continue
        richtig = soll.get(schluessel)
        if richtig is None:
            continue
        if genannt != richtig:
            anfang = max(0, m.start() - 40)
            treffer.append({"stelle": (text[anfang:m.end() + 40] or "").replace("\n", " "),
                            "begriff": wort, "genannt": genannt, "richtig": int(richtig)})
    return treffer


def fakten_lesen(pfad: str = FAKTEN) -> dict:
    with open(pfad, encoding="utf-8") as fh:
        return json.load(fh)


def main(argv=None) -> int:
    leser = argparse.ArgumentParser(description="Auftragstext gegen das Faktenblatt pruefen (M11)")
    leser.add_argument("datei", nargs="?", help="Auftragsdatei")
    leser.add_argument("--text", help="Text direkt pruefen")
    leser.add_argument("--fakten", default=FAKTEN, help="anderes Faktenblatt")
    args = leser.parse_args(argv)
    if not args.datei and args.text is None:
        leser.print_help()
        return 2
    try:
        fakten = fakten_lesen(args.fakten)
    except (OSError, ValueError) as fehler:
        print("Faktenblatt nicht lesbar (%s). Zuerst: python -X utf8 tools/faktenblatt.py"
              % fehler)
        return 2
    text = args.text
    if text is None:
        try:
            with open(args.datei, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError as fehler:
            print("Datei nicht lesbar: %s" % fehler)
            return 2
    treffer = pruefen(text, fakten)
    if not treffer:
        print("Keine Abweichung vom Faktenblatt.")
        return 0
    print("ABWEICHUNGEN vom Faktenblatt: %d" % len(treffer))
    for t in treffer:
        print("  %d %s genannt, richtig ist %d" % (t["genannt"], t["begriff"], t["richtig"]))
        print("     ... %s ..." % t["stelle"].strip())
    return 1


if __name__ == "__main__":
    sys.exit(main())
