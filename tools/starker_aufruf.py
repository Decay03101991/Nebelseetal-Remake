"""Ruft das starke Modell (deepseek-v4-pro) fuer ein Auftragspaket auf - mit Streaming.

Warum direkt per urllib statt `hermes -z`: der CLI-Weg blieb schon einmal stundenlang bei einem
Update haengen (belegt). Der Schluessel steht in `%LOCALAPPDATA%\\hermes\\.env` und wird hier
gelesen, nie ausgegeben.

Regeln aus dem Skill:
  * `max_tokens: 48000` - sonst frisst das Nachdenken die ganze Antwort (0 Zeichen = Geld verbrannt)
  * Streaming: jedes Stueck ist ein Lebenszeichen; 240 s ohne Stueck = echter Haenger
  * Antwort haengt an > 0 Zeichen; die Token-Zahlen aus `usage` werden mitgeschrieben (Kosten MESSEN)
  * waehrend des Laufs in die Zieldatei schreiben, damit ein Abbruch nur den Rest kostet

Aufruf:
    python -X utf8 tools/starker_aufruf.py <auftrag.md> <zieldatei.md>
"""
from __future__ import annotations

import io
import json
import os
import sys
import time
import urllib.request

ENV = os.path.join(os.environ.get("LOCALAPPDATA", ""), "hermes", ".env")  # Schluesselablage
API = "https://api.deepseek.com/v1/chat/completions"  # DeepSeek-Endpunkt
MODELL = "deepseek-v4-pro"  # das starke Modell
MAX_TOKENS = 48000  # Denkzeit + Antwort; kleiner verbrennt Geld ohne Antwort
STILLE_GRENZE = 240  # Sekunden ohne Stueck = Haenger


def schluessel():
    """Liest DEEPSEEK_API_KEY aus der .env, ohne ihn je auszugeben."""
    with io.open(ENV, encoding="utf-8") as datei:
        for zeile in datei:
            zeile = zeile.strip()
            if zeile.startswith("DEEPSEEK_API_KEY"):
                return zeile.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("DEEPSEEK_API_KEY nicht in %s gefunden" % ENV)


def aufruf(pfad_auftrag, pfad_ziel):
    """Schickt den Auftrag und schreibt die Antwort Stueck fuer Stueck mit."""
    auftrag = io.open(pfad_auftrag, encoding="utf-8").read()
    kopf = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + schluessel(),
    }
    koerper = {
        "model": MODELL,
        "messages": [
            {"role": "system",
             "content": "Du bist Spieldesigner und Regel-Autor. Antworte auf Deutsch, in Markdown, "
                        "mit Tabellen, ohne Emojis. Halte dich exakt an das Antwortformat im Auftrag."},
            {"role": "user", "content": auftrag},
        ],
        "max_tokens": MAX_TOKENS,
        "stream": True,
        "stream_options": {"include_usage": True},
    }
    anfrage = urllib.request.Request(
        API, data=json.dumps(koerper).encode("utf-8"), headers=kopf, method="POST")
    start = time.time()  # Startzeit fuer die Dauer
    stuecke = 0  # Zahl der Streaming-Stuecke
    zeichen = 0  # Laenge der Antwort
    letztes = time.time()  # Zeit des letzten Stuecks
    nutzung = {}  # Token-Zahlen aus dem letzten Stueck
    with io.open(pfad_ziel, "w", encoding="utf-8", newline="\n") as ziel:
        with urllib.request.urlopen(anfrage, timeout=600) as antwort:
            for roh in antwort:  # zeilenweise SSE
                if not roh.startswith(b"data: "):
                    continue
                daten = roh[6:].strip()
                if daten == b"[DONE]":
                    break
                try:
                    stueck = json.loads(daten)
                except json.JSONDecodeError:
                    continue
                if stueck.get("usage"):  # Token-Zahlen kommen am Ende
                    nutzung = stueck["usage"]
                for wahl in stueck.get("choices") or []:
                    text = (wahl.get("delta") or {}).get("content") or ""
                    if text:
                        ziel.write(text)  # sofort schreiben: ein Abbruch kostet nur den Rest
                        ziel.flush()
                        stuecke += 1
                        zeichen += len(text)
                        letztes = time.time()
                if time.time() - letztes > STILLE_GRENZE:
                    raise SystemExit("HAENGER: %d s ohne Stueck" % STILLE_GRENZE)
    dauer = time.time() - start  # gemessene Dauer
    print("Stuecke: %d | Zeichen: %d | Dauer: %.0f s" % (stuecke, zeichen, dauer))
    print("Token (usage):", json.dumps(nutzung, ensure_ascii=False))
    if zeichen == 0:
        raise SystemExit("LEERE ANTWORT - max_tokens erhoehen, Geld ist verbrannt")
    return zeichen, nutzung


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit("Aufruf: python tools/starker_aufruf.py <auftrag.md> <zieldatei.md>")
    aufruf(sys.argv[1], sys.argv[2])
