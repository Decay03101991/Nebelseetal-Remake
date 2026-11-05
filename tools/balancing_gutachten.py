# -*- coding: utf-8 -*-
"""Balancing-Gutachten mit dem GROSSEN DeepSeek-Modell (Daniels Freigabe 05.11.2026, 3,61 USD).

Baut zuerst ein Fakten-Dossier aus den ECHTEN Projektdateien (keine erfundenen Zahlen), schickt es
mit einer praezisen Frage an `deepseek-v4-pro` und schreibt die Antwort nach
`docs/BALANCING_GUTACHTEN_20261105.md`. Streaming, damit ein Haenger erkannt wird; die Antwort wird
waehrend des Laufs mitgeschrieben.

Kosten: ein Aufruf, max_tokens 48000 (reasoning zaehlt mit). Kein zweiter Aufruf ohne Not.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.request

ROOT = r"D:\Arbeiten\Nebelseetal_Remake"
ENV = os.path.join(os.environ.get("LOCALAPPDATA", r"C:\Users\saras\AppData\Local"), "hermes", ".env")
ZIEL = os.path.join(ROOT, "docs", "BALANCING_GUTACHTEN_20261105.md")
DOSSIER = os.path.join(os.environ.get("TEMP", "."), "nebel_balancing_dossier.txt")
MODELL = "deepseek-v4-pro"
MAX_TOKENS = 48000


def schluessel() -> str:
    """Den DeepSeek-Schluessel aus der Hermes-.env lesen (nie ausgeben)."""
    with open(ENV, encoding="utf-8", errors="ignore") as f:
        for zeile in f:
            if zeile.strip().startswith("DEEPSEEK_API_KEY"):
                return zeile.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("DEEPSEEK_API_KEY fehlt")


def lies(pfad: str, von: int = 0, bis: int = 0) -> str:
    """Eine Datei lesen, optional einen Zeilenbereich."""
    with open(pfad, encoding="utf-8") as f:
        zeilen = f.read().splitlines()
    return "\n".join(zeilen[von:bis or len(zeilen)])


def dossier() -> str:
    """Die Fakten aus dem Projekt sammeln - nur was wirklich in den Dateien steht."""
    teile = []
    d = os.path.join(ROOT, "docs")

    # 1. Die Messdokumente, gekuerzt auf ihre Tabellen und Verdicts
    for name, grenze in (("SPIELBALANCING_TEST.md", 26000), ("BEFUND_BEUTE_REIHENFOLGE_20261105.md", 6000)):
        p = os.path.join(d, name)
        if os.path.exists(p):
            teile.append("### " + name + "\n" + lies(p)[:grenze])

    # 2. Die Kerndaten als kompakte Auszuege
    for name, pfad in (
        ("Einheiten (Kosten, Werte)", "data/units.json"),
        ("Rohstoffe (Ertrag je Stunde)", "data/resources.json"),
        ("Drachen (Wache, Schwellen, Atem, Beute)", "data/drachen.json"),
        ("Nahrungsverbrauch", "data/nahrungsverbrauch.json"),
        ("Karrenkapazitaet", "data/karrenkapazitaet.json"),
        ("Beute-Vorrang", "data/beute_vorrang.json"),
    ):
        p = os.path.join(ROOT, pfad)
        if os.path.exists(p):
            roh = open(p, encoding="utf-8").read()
            teile.append("### " + name + " (" + pfad + ")\n" + roh[:9000])
    return "\n\n".join(teile)


FRAGE = """Du bist ein erfahrener Aufbau- und Strategiespiel-Designer und Balancing-Auditor. Unten steht
ein FAKTEN-DOSSIER aus einem laufenden Remake des Browserspiels "Nebelseetal" (Python, Einzelspieler
gegen Bots, Spieluhr-Faktor, Siedlungsaufbau mit 6 Siedlungen, 9 Rohstoffen, 17 Waren, 28 Einheiten,
21 Forschungen, Kaempfen gegen Bots und drei Drachen).

Deine Aufgabe: **die fuenf wertvollsten Balancing- oder Mechanik-Korrekturen** benennen, die dieses
Spiel messbar besser machen - und zwar mit Zahlen, die aus dem Dossier stammen.

Regeln, die du einhalten MUSST:
- Jede Zahl, die du nennst, muss im Dossier stehen oder aus Dossier-Zahlen GERECHNET sein. Rechne
  die Rechnung hin. Erfinde keine Quelle, kein Handbuchzitat, keinen Wert.
- Wo das Dossier etwas nicht hergibt, schreibe ausdruecklich UNBELEGT und nenne, welche Messung fehlt.
- Kein Code, keine Dateinamen erfinden. Du lieferst Urteile und Zahlen, kein Programm.
- Deutsch, knapp, Tabellen wo sinnvoll. Keine Emojis.
- Priorisiere nach Wirkung je Risiko: was macht das Spiel am staerksten besser, ohne bewaehrtes
  Verhalten umzuwerfen?

Antworte in GENAU dieser Form:

## 1. Kurzurteil
Drei bis fuenf Saetze: wo steht das Spiel balancing-technisch, was ist der groesste Engpass?

## 2. Die fuenf Vorschlaege (Tabelle)
| Nr | Befund (mit Dossier-Zahl) | Aenderung (exakte Werte) | Erwartete Wirkung | Risiko | Wie pruefen |
Jeweils eine Zeile je Vorschlag, hoechste Wirkung zuerst.

## 3. Rechnungen
Fuer jeden Vorschlag die Rechnung, die ihn stuetzt (Ertraege, Kosten, Verlustquoten, Spieltage).

## 4. Was du NICHT empfiehlst
Zwei bis vier Eingriffe, die verlockend klingen, aber dem Spiel schaden wuerden - mit Grund.

## 5. Offene Messungen
Welche drei Messungen fehlen, um die Vorschlaege zu belegen?

DOSSIER:
"""


def main() -> int:
    fakten = dossier()
    with open(DOSSIER, "w", encoding="utf-8") as f:
        f.write(fakten)
    print("Dossier:", len(fakten), "Zeichen ->", DOSSIER)
    kopf = FRAGE + fakten

    rumpf = json.dumps({
        "model": MODELL,
        "messages": [{"role": "user", "content": kopf}],
        "max_tokens": MAX_TOKENS,
        "stream": True,
    }).encode("utf-8")
    anfrage = urllib.request.Request(
        "https://api.deepseek.com/v1/chat/completions", data=rumpf,
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + schluessel()})
    stuecke, text, letzte = 0, [], time.time()
    stuecke_denken = []
    with open(ZIEL, "w", encoding="utf-8") as f:
        f.write("# Balancing-Gutachten (deepseek-v4-pro, 05.11.2026)\n\n")
        f.write("> Automatisch erzeugt aus dem Projekt-Dossier; Zahlen stammen aus den Datendateien.\n\n")
        with urllib.request.urlopen(anfrage, timeout=900) as antwort:
            for roh in antwort:
                zeile = roh.decode("utf-8").strip()
                if not zeile.startswith("data:"):
                    continue
                nutz = zeile[5:].strip()
                if nutz == "[DONE]":
                    break
                try:
                    stueck = json.loads(nutz)
                except ValueError:
                    continue
                wahl = (stueck.get("choices") or [{}])[0]
                delta = wahl.get("delta") or {}
                # DENKEN zaehlt als Lebenszeichen: ein starkes Modell sendet minutenlang nur
                # reasoning_content und noch keinen Text - wer nur auf Text wartet, bricht zu frueh ab.
                if delta.get("reasoning_content"):
                    letzte = time.time()
                    stuecke_denken.append(1)
                teil = delta.get("content") or ""
                if teil:
                    text.append(teil)
                    f.write(teil)
                    f.flush()
                    stuecke += 1
                    letzte = time.time()
                if time.time() - letzte > 600:
                    print("HAENGER: 600 s ohne Stueck")
                    return 2
    fertig = "".join(text)
    print("Antwort:", len(fertig), "Zeichen,", stuecke, "Textstuecke,", len(stuecke_denken), "Denkstuecke")
    if len(fertig) < 500:
        print("ZU KURZ - Lauf war wertlos")
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
