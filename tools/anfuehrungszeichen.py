"""Vereinheitlicht die deutschen Anfuehrungszeichen in den Markdown-Dokumenten.

Regel: Ein Zitat beginnt mit „ (unten) und endet mit “ (oben). In vielen Dateien steht als
Schlusszeichen ein gerades " - das faellt beim Lesen sofort auf, auch in GitHub.

Was NICHT angefasst wird:
  * Code-Bloecke (``` ... ```)
  * Buchstaben. Hier wird ausschliesslich das Schlusszeichen getauscht.

Aufruf:
    python -X utf8 tools/anfuehrungszeichen.py --pruefen    # nur zaehlen
    python -X utf8 tools/anfuehrungszeichen.py --schreiben  # schreiben
"""
from __future__ import annotations

import os
import re
import sys

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OEFFNEN = "\u201e"     # deutsches Anfuehrungszeichen unten
SCHLIESSEN = "\u201c"  # deutsches Anfuehrungszeichen oben
MUSTER = re.compile(OEFFNEN + '([^' + SCHLIESSEN + OEFFNEN + '"]{1,300})"', re.S)


def dateien() -> list:
    pfade = [os.path.join(HIER, "README.md")]
    for ordner in ("docs", os.path.join("docs", "audits")):
        voll = os.path.join(HIER, ordner)
        if not os.path.isdir(voll):
            continue
        for name in sorted(os.listdir(voll)):
            if name.endswith(".md"):
                pfade.append(os.path.join(voll, name))
    return [p for p in pfade if os.path.isfile(p)]


def umbauen(text: str):
    """Gibt (neuer Text, Anzahl Tauschungen, Zeilen mit Restfehler) zurueck."""
    bloecke = []

    def block_merken(m):
        bloecke.append(m.group(0))
        return "\x01%d\x01" % (len(bloecke) - 1)

    ohne_code = re.sub(r"```.*?```", block_merken, text, flags=re.S)
    neu, tausch = MUSTER.subn(lambda m: OEFFNEN + m.group(1) + SCHLIESSEN, ohne_code)
    for i, stueck in enumerate(bloecke):
        neu = neu.replace("\x01%d\x01" % i, stueck)
    offen = []
    for nummer, zeile in enumerate(neu.split("\n"), start=1):
        if zeile.lstrip().startswith(("    ", "|", ">")) or "```" in zeile:
            continue
        if zeile.count(OEFFNEN) != zeile.count(SCHLIESSEN):
            offen.append("Zeile %d: %s" % (nummer, zeile.strip()[:90]))
    return neu, tausch, offen


def main() -> int:
    schreiben = "--schreiben" in sys.argv
    gesamt, betroffen, probleme = 0, 0, []
    for pfad in dateien():
        with open(pfad, encoding="utf-8") as f:
            alt = f.read()
        neu, n, offen = umbauen(alt)
        if n:
            betroffen += 1
            gesamt += n
            print("%-48s %4d" % (os.path.relpath(pfad, HIER), n))
        for o in offen[:3]:
            probleme.append("%s %s" % (os.path.relpath(pfad, HIER), o))
        if schreiben and n and neu != alt:
            with open(pfad, "w", encoding="utf-8", newline="\n") as f:
                f.write(neu)
    print("\nDateien betroffen: %d | Zeichen getauscht: %d | %s"
          % (betroffen, gesamt, "GESCHRIEBEN" if schreiben else "nur geprueft"))
    if probleme:
        print("Zeilen mit ungleicher Anzahl (von Hand ansehen): %d" % len(probleme))
        for p in probleme[:10]:
            print("  -", p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
