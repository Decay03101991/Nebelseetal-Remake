"""Prueft die Arbeitsordner-Sperre in tools/opus_lauf.py (belegt 10.11.2026).

Der scharfe Opus-Lauf starb am 10.11.2026 um 11:08, BEVOR ein Modell aufgerufen wurde, an
`os.path.commonpath`: der Arbeitsordner liegt im Temp (Laufwerk C:), das Projekt auf Laufwerk D:,
und `commonpath` wirft dann `ValueError: Paths don't have the same drive`. Die Sperre war also genau
dann kaputt, wenn der Normalfall eintritt.

Diese Wache haelt vier Dinge fest:
  1. Der Temp-Ordner gilt NICHT als "im Projekt" (verschiedene Laufwerke sind der Normalfall).
  2. Der Projektordner selbst und jeder Unterordner gelten als "im Projekt".
  3. Ein Ordner mit gleichem Namensanfang aber anderem Ende gilt NICHT als "im Projekt".
  4. Die Pruefung wirft keine Ausnahme, auch wenn `commonpath` fuer dasselbe Paar eine wirft.

ASCII-only: ein Umlaut hier waere ein SyntaxError beim Import.
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "quelltext"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['main:*']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import sys
import tempfile

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(WURZEL, "tools"))

import opus_lauf  # noqa: E402  (Pfad steht erst jetzt)

FEHLER = []
PRUEFUNGEN = 0


def check(name, bedingung, meldung=""):
    global PRUEFUNGEN
    PRUEFUNGEN += 1
    if not bedingung:
        FEHLER.append(f"{name}: {meldung}")


def main() -> int:
    hier = opus_lauf.HIER
    temp = tempfile.gettempdir()

    # 1. Der Normalfall, der den Lauf gekillt hat: Temp auf C:, Projekt auf D:.
    check("1 Arbeitsordner im Temp gilt nicht als im Projekt",
          opus_lauf._im_projekt(os.path.join(temp, "opus_pruefung_20261110_1108")) is False,
          temp)
    # 4. Dieselbe Frage ohne Ausnahme - die alte Zeile warf hier ValueError.
    try:
        opus_lauf._im_projekt(temp)
        ohne_ausnahme = True
        meldung = ""
    except Exception as e:                                    # noqa: BLE001
        ohne_ausnahme = False
        meldung = repr(e)
    check("4 Pruefung wirft keine Ausnahme (auch laufwerksuebergreifend)", ohne_ausnahme, meldung)

    # 2. Projekt und Unterordner muessen als "im Projekt" gelten.
    check("2 Projektordner selbst gilt als im Projekt", opus_lauf._im_projekt(hier) is True, hier)
    check("2a Unterordner gilt als im Projekt",
          opus_lauf._im_projekt(os.path.join(hier, "docs", "audits")) is True)
    check("2b gleichnamiger Ordner unter dem Temp gilt nicht als im Projekt",
          opus_lauf._im_projekt(os.path.join(temp, "Nebelseetal_Remake", "cache")) is False,
          "Ordner ausserhalb des Projekts, auch wenn er so heisst")

    # 3. Namensanfang ist nicht genug: der Trenner entscheidet.
    check("3 Ordner mit gleichem Namensanfang gilt nicht als im Projekt",
          opus_lauf._im_projekt(hier + "_alt") is False, hier + "_alt")

    # 7. Der Aufruf muss STARTBAR sein: eine echte EXE, keine endungslose POSIX-Huelle.
    exe = opus_lauf._claude_exe()
    check("7 Claude-Code-Aufruf gefunden", exe is not None and os.path.isfile(exe), str(exe))
    check("7a Aufruf ist eine echte EXE (startbar ohne cmd.exe)",
          exe is not None and exe.lower().endswith(".exe"), str(exe))
    befehl = opus_lauf._claude_befehl(["-p", "hallo"])
    check("7b Kommando beginnt mit genau diesem Aufruf", bool(befehl) and befehl[0] == exe,
          str(befehl[:1]))
    check("7c Kommando laeuft nicht ueber cmd.exe", bool(befehl) and befehl[0].lower().endswith(".exe"),
          str(befehl[:2]))
    check("7d keine endungslose POSIX-Huelle als Aufruf",
          exe is not None and os.path.splitext(exe)[1] != "", str(exe))

    # Die alte, kaputte Zeile darf nicht zurueckkommen.
    with open(os.path.join(WURZEL, "tools", "opus_lauf.py"), "rb") as griff:
        quelle = griff.read().decode("utf-8", "replace")
    check("5 kein commonpath-Aufruf mehr im Werkzeug", "commonpath([" not in quelle)
    check("6 Sperre benutzt _im_projekt", "_im_projekt(arbeitsordner)" in quelle)

    print(f"ERGEBNIS: {PRUEFUNGEN - len(FEHLER)} bestanden, {len(FEHLER)} Fehler")
    for f in FEHLER[:20]:
        print("  -", f)
    return 1 if FEHLER else 0


if __name__ == "__main__":
    sys.exit(main())
