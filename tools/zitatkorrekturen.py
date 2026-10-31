"""Korrigiert die Schreibfehler in den ZITIERTEN Originaltexten - mit vollstaendigem Nachweis.

Daniels Anweisung am 31.10.2026: "ich moechte bitte das du gepruefte schreibfehler aus den
originalen zitate bitte schon verbesserst. Dies muss aber ausdruecklich festgehalten werden."

Also: jede einzelne Aenderung wird vorher/nachher protokolliert und in
docs/ZITATKORREKTUREN.md eingetragen. Es werden NUR Schreibfehler berichtigt (Buchstaben,
Wortendungen, fehlende Leerzeichen nach Satzzeichen) - kein Wortlaut, keine Zahlen, keine
Bedeutung.

Aufruf:
    python -X utf8 tools/zitatkorrekturen.py --pruefen     # zeigt, was passieren wuerde
    python -X utf8 tools/zitatkorrekturen.py --schreiben   # schreibt Aenderungen + Bericht
"""
from __future__ import annotations

import os
import re
import sys

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATEI = os.path.join(HIER, "docs", "audits", "AUFTRAG_EXTERNE_PRUEFUNG_20261031.md")
BERICHT = os.path.join(HIER, "docs", "ZITATKORREKTUREN.md")

# Woerter, die falsch geschrieben sind - alt -> neu. Bewusst Wort fuer Wort, nichts Automatisches:
# eine Auto-Korrektur koennte Sinn veraendern.
WORTE = [
    ("auf dern Fernkampfwert", "auf dem Fernkampfwert", "falscher Fall: dern -> dem"),
    ("Schaden ermittel die eine Belagerungswaffe macht", "Schaden ermittelt die eine Belagerungswaffe macht",
     "fehlendes t: ermittel -> ermittelt"),
    ("Hier seit ihr sicher", "Hier seid ihr sicher", "seit -> seid (Verb)"),
    ("mit einender verbinden", "mit einander verbinden", "einender -> einander"),
]

# Fehlende Leerzeichen nach Satzzeichen: "Kampfablauf:Aktuell" -> "Kampfablauf: Aktuell".
# Nur, wenn direkt ein Grossbuchstabe folgt und kein Datum/keine Uhrzeit/kein Link betroffen ist.
LEERZEICHEN = re.compile(r"(?<![0-9])([.:;,])([A-ZÄÖÜ][a-zäöüß])")


def main() -> int:
    schreiben = "--schreiben" in sys.argv
    with open(DATEI, encoding="utf-8") as f:
        text = f.read()
    zeilen = text.split("\n")
    aenderungen = []

    # 1. Wortfehler (ganze Datei)
    for alt, neu, grund in WORTE:
        anzahl = text.count(alt)
        if anzahl:
            text = text.replace(alt, neu)
            aenderungen.append((alt, neu, grund, anzahl, "Wortfehler"))

    # 2. Fehlende Leerzeichen, Zeile fuer Zeile nachvollziehbar
    neu_zeilen = []
    for nummer, zeile in enumerate(text.split("\n"), start=1):
        if zeile.lstrip().startswith(("```", "    ", "#")) or "http" in zeile or "](" in zeile:
            neu_zeilen.append(zeile)
            continue
        def machen(m, nummer=nummer):
            vorher = m.group(1) + m.group(2)
            nachher = m.group(1) + " " + m.group(2)
            aenderungen.append((vorher, nachher, "fehlendes Leerzeichen nach Satzzeichen",
                                1, "Zeile %d" % nummer))
            return nachher

        neu_zeilen.append(LEERZEICHEN.sub(machen, zeile))
    text = "\n".join(neu_zeilen)

    print(f"Datei: {os.path.relpath(DATEI, HIER)}")
    print(f"Aenderungen insgesamt: {len(aenderungen)}")
    for a in aenderungen:
        print(f"  {a[4]:22s} {a[0][:40]!r} -> {a[1][:40]!r}  ({a[3]}x)")

    if schreiben:
        with open(DATEI, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        with open(BERICHT, "w", encoding="utf-8", newline="\n") as f:
            f.write(_bericht(aenderungen))
        print("geschrieben:", os.path.relpath(DATEI, HIER), "und", os.path.relpath(BERICHT, HIER))
    return 0


def _bericht(aenderungen) -> str:
    kopf = (
        "# Korrekturen in zitierten Originaltexten\n\n"
        "**Anweisung von Daniel am 31.10.2026:** „ich möchte bitte das du geprüfte schreibfehler aus\n"
        "den originalen zitate bitte schon verbesserst. Dies muss aber ausdrücklich festgehalten\n"
        "werden.\"\n\n"
        "Diese Datei ist der Nachweis. Betroffen ist ausschließlich\n"
        "`docs/audits/AUFTRAG_EXTERNE_PRUEFUNG_20261031.md` — dort stehen die Texte der alten Website\n"
        "und des Forums im Wortlaut. Korrigiert wurden **nur** Buchstaben, Wortendungen und fehlende\n"
        "Leerzeichen nach Satzzeichen. Kein Wort wurde ersetzt, keine Zahl geändert, kein Satz\n"
        "umgestellt.\n\n"
        "## Die Änderungen im Einzelnen\n\n"
        "| # | Art | vorher | nachher | Stellen |\n|---|---|---|---|---|\n"
    )
    zeilen = [kopf]
    for i, (alt, neu, grund, anzahl, wo) in enumerate(aenderungen, start=1):
        a = alt.replace("|", "\\|")
        b = neu.replace("|", "\\|")
        zeilen.append(f"| {i} | {grund} ({wo}) | `{a}` | `{b}` | {anzahl} |\n")
    zeilen.append(
        "\n## Was absichtlich NICHT korrigiert wurde\n\n"
        "* **Eigenheiten der Quelle:** „Ruhmeshalle\", „Nebelseetal-Online\", Großschreibung von „Du\" — "
        "das ist Stil der Zeit, kein Fehler.\n"
        "* **Dateinamen der Quelle:** `Grundlegenes.html` heißt im Original wirklich so.\n"
        "* **Zahlen und Werte:** unangetastet. Sie sind der Grund, warum zitiert wird.\n\n"
        "## Regel für die Zukunft\n\n"
        "Zitate dürfen berichtigt werden — aber nur mit Eintrag hier (vorher, nachher, Stelle) und nur\n"
        "für Schreibfehler. Sobald sich der Sinn ändern könnte, wird nicht korrigiert, sondern in einer\n"
        "Fußnote angemerkt. Werkzeug: `tools/zitatkorrekturen.py`.\n")
    return "".join(zeilen)


if __name__ == "__main__":
    raise SystemExit(main())
