"""Gesamtaudit: EIN begrenzter Aufruf an deepseek-v4-pro ueber Dossier + festen Auftrag.

Daniel (31.10.2026): das starke Modell soll einmal das GESAMTE Projekt (Mechaniken und
Logiken) gegen die bekannten Spielinfos abgleichen - in einem begrenzten Format, damit
keine unendlichen Kosten entstehen.

Begrenzung (belegt durch fruehere Laeufe, siehe docs/ENTWICKLUNGSPROTOKOLL.md):
  * genau EIN Aufruf (kein Agentenlauf, keine Werkzeuge, keine Nachfragen),
  * Eingabe = docs/audits/GESAMTAUDIT_DOSSIER_20261031.md (festes Zeichenbudget),
  * max_tokens 48000 (bei 16000 ging alles im Nachdenken verloren -> 0 Zeichen),
  * Stillstandsschwelle 240 s statt festem Timeout, Ergebnis waehrend des Laufs gesichert,
  * Ausgabeformat mit harter Obergrenze (12 Befunde, 5 Unklares, 3 Massnahmen).

Aufruf: python -X utf8 tools/gesamtaudit_lauf.py [--stillstand 240]
"""
from __future__ import annotations

import datetime
import json
import os
import sys
import time
import urllib.error
import urllib.request

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER = os.path.join(HIER, "docs", "audits", "GESAMTAUDIT_DOSSIER_20261031.md")
ZIEL = os.path.join(HIER, "docs", "audits", "GESAMTAUDIT_BEFUNDE_20261031.md")
HERMES = r"C:\Users\saras\AppData\Local\hermes"
MESSUNG = os.path.join(r"D:\Arbeiten\Hermes\Kosten",
                       "usage_gesamtaudit_%s.json" % time.strftime("%Y%m%d_%H%M"))
LOG = os.path.join(r"C:\Users\saras\AppData\Local\hermes\cache\scratch", "gesamtaudit.log")

AUFTRAG = """ROLLE
Du bist PRUEFER, nicht Entwerfer. Du pruefst ein fertiges Remake (Python/tkinter,
Einzelspieler gegen Bots) gegen die mitgelieferten Originalquellen eines deutschen
Browserspiels. Du urteilst ausschliesslich nach dem beigefuegten Dossier. Was dort nicht
steht, gilt als "im Dossier nicht belegt" - du erfindest keine Zeilennummern, keine
Seitenzahlen, keine Werte und keine Quellen. Du lobst nicht und schreibst keine Einleitung.

MATERIAL (im Dossier, in dieser Reihenfolge)
  A  Rahmen, Daniels Regeln, Projektstand
  B1 Pruefregister des Originals (40 Punkte mit Seite/Zeile)
  B2 Belegte Auswertung Kampf/Auftraege/Punkte/Schutz
  B3 Belegte Auswertung Gebaeude/Freischaltung/Erträge
  B4 Abweichungen Vorversion 2006 gegen Handbuch 2009
  C1 Module, C2 Spielzahlen im Code, C3 Funktionen, C4 Datendateien
  D1 offene Luecken laut Modulen, D2 Fehlerregister, D3 aktueller Stand

AUFGABE - pruefe in dieser Reihenfolge, jede Zeile muss belegbar sein
1. MECHANIK GEGEN QUELLE: Wo sagt der Code (C2/C3/C4) etwas anderes als die Quelle (B1-B4)?
   Nur echte Widersprueche, keine Geschmacksfragen.
2. DOPPELTE SYSTEME: Wo gibt es zwei Wahrheiten fuer dieselbe Sache (Bewegung, Kampf, Beute,
   Punkte, Wall)? Nenne beide Fundstellen.
3. FEHLENDE MECHANIK: Welche in B1-B4 belegte Regel kommt im Inventar C ueberhaupt nicht vor?
4. SPIELBARKEIT BEI SPIELUHR x180 (1 Spielstunde = 20 echte Sekunden): Rechne nach, wo belegte
   Zahlen dadurch trivial oder unspielbar werden (Produktion, Reisezeit, Forschung, Ausbildung,
   Siedlerzuwachs, Wallpunkte, Siegbedingung). Nenne die Rechnung in einer Kurzform.
5. WIDERSPRUECHE ZWISCHEN DOKUMENTEN: Register/Auswertung (B) gegen Code-Zahlen (C).

AUSGABEFORMAT - halte es GENAU ein, nichts davor und nichts danach

## Befunde

| Nr | Mechanik | CODE-BELEG | QUELL-BELEG | Urteil | Empfehlung | Aufwand |
|---|---|---|---|---|---|---|
| 1 | ... | datei/modul oder konstante, wie im Dossier benannt | Seite/Zeile oder "im Dossier nicht belegt" | WIDERSPRUCH/FEHLT/DOPPELT/UNBELEGT/IN ORDNUNG | ein Satz, umsetzbar | S/M/L |

Regeln fuer die Tabelle:
- hoechstens 12 Zeilen, sortiert nach Wirkung auf das Spiel (groesste zuerst),
- jeder Befund nur EINMAL (gleiche Ursache nicht in mehreren Zeilen wiederholen),
- "IN ORDNUNG" nur, wenn du es ausdruecklich geprueft hast - hoechstens 2 solche Zeilen,
- in CODE-BELEG nur Namen, die im Dossier vorkommen (Modul, Konstante, Datendatei, Funktion).

## Nicht beurteilbar
- hoechstens 5 Punkte, je ein Satz mit dem Grund (z. B. "UI-Verhalten fehlt im Dossier").

## Die drei wichtigsten Massnahmen
1. ...
2. ...
3. ...

Sprache: Deutsch. Kein Vorwort, keine Schlussbemerkung."""


def key():
    with open(os.path.join(HERMES, ".env"), encoding="utf-8", errors="replace") as f:
        for zeile in f:
            if zeile.startswith("DEEPSEEK_API_KEY="):
                return zeile.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("DEEPSEEK_API_KEY fehlt in .env")


def log(text):
    zeile = f"{datetime.datetime.now():%H:%M:%S} {text}"
    print(zeile, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(zeile + "\n")


def main():
    stillstand = 240
    if "--stillstand" in sys.argv:
        stillstand = int(sys.argv[sys.argv.index("--stillstand") + 1])
    # Gezielte Audits: eigener Ausschnitt und eigene Zieldatei, damit nicht jedes Mal
    # das ganze Dossier (129.000 Zeichen) bezahlt wird - Daniel: "keine unnoetigen Tokens".
    dossier = DOSSIER
    ziel = ZIEL
    nur_paket = "--paket" in sys.argv
    if "--dossier" in sys.argv:
        dossier = os.path.abspath(sys.argv[sys.argv.index("--dossier") + 1])
    if "--ziel" in sys.argv:
        ziel = os.path.abspath(sys.argv[sys.argv.index("--ziel") + 1])
    with open(dossier, encoding="utf-8") as f:
        dossier = f.read()
    if nur_paket:
        # Die Pakete A1-A4 sind selbsttragend: Rolle, Vorgaben, Quellen, Ausgabeformat stehen
        # schon drin. Ein zweiter Auftragskopf davor widerspraeche ihrem Format und kostet nur
        # Kontext - deshalb wird das Paket allein gesendet.
        prompt = dossier
    else:
        prompt = AUFTRAG + "\n\n" + "=" * 78 + "\nDOSSIER\n" + "=" * 78 + "\n\n" + dossier
    log(f"Prompt {len(prompt)} Zeichen (~{len(prompt) / 3.5:.0f} Token), "
        f"Ziel {os.path.basename(ziel)}, Stillstandsschwelle {stillstand} s, max_tokens 48000")
    daten = json.dumps({
        "model": "deepseek-v4-pro",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 48000,
        "stream": True,
        "stream_options": {"include_usage": True},
    }).encode("utf-8")
    anfrage = urllib.request.Request(
        "https://api.deepseek.com/v1/chat/completions", data=daten,
        headers={"Authorization": "Bearer " + key(), "Content-Type": "application/json",
                 "Accept": "text/event-stream"})

    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    if "--trocken" in sys.argv:
        # Kostet nichts: zeigt nur, was gesendet WUERDE (Prompt, Zieldatei, Aufrufe).
        print(f"TROCKEN: Prompt {len(prompt)} Zeichen, Ziel {ziel}, Modell deepseek-v4-pro")
        print(f"TROCKEN: geschaetzt {len(prompt) / 3.5 / 1e6 * 0.66 + 15000 / 1e6 * 1.98:.4f} USD")
        print("--- erste 3 Zeilen Prompt ---")
        print("\n".join(prompt.splitlines()[:3]))
        return 0
    teile, nutzung, stuecke = [], {}, 0
    start = time.time()
    letztes_leben = start
    abbruch = None
    try:
        with urllib.request.urlopen(anfrage, timeout=60) as antwort:
            with open(ziel, "w", encoding="utf-8", newline="\n") as datei:
                for roh in antwort:
                    if time.time() - letztes_leben > stillstand:
                        abbruch = f"kein Lebenszeichen seit {stillstand} s"
                        break
                    zeile = roh.decode("utf-8", "replace").strip()
                    if not zeile or not zeile.startswith("data:"):
                        continue
                    inhalt = zeile[5:].strip()
                    if inhalt == "[DONE]":
                        break
                    try:
                        paket = json.loads(inhalt)
                    except ValueError:
                        continue
                    letztes_leben = time.time()
                    if paket.get("usage"):
                        nutzung = paket["usage"]
                    for wahl in paket.get("choices") or []:
                        stueck = (wahl.get("delta") or {}).get("content")
                        if stueck:
                            teile.append(stueck)
                            stuecke += 1
                            datei.write(stueck)
                            datei.flush()
                            if stuecke % 60 == 0:
                                log(f"{stuecke} Stuecke, {sum(len(t) for t in teile)} Zeichen, "
                                    f"{time.time() - start:.0f} s")
    except urllib.error.HTTPError as fehler:
        abbruch = f"HTTP {fehler.code}: {fehler.read().decode('utf-8', 'replace')[:300]}"
    except Exception as fehler:  # noqa: BLE001
        abbruch = f"{type(fehler).__name__}: {fehler}"

    text = "".join(teile)
    dauer = round(time.time() - start, 1)
    log(f"Ende nach {dauer} s - {len(text)} Zeichen, Abbruch: {abbruch or 'nein'}")
    if nutzung:
        ein, aus = nutzung.get("prompt_tokens", 0), nutzung.get("completion_tokens", 0)
        kosten = ein / 1e6 * 0.66 + aus / 1e6 * 1.98
        log(f"Tokens: {nutzung}")
        log(f"Kosten: {kosten:.4f} USD")
    os.makedirs(os.path.dirname(MESSUNG), exist_ok=True)
    with open(MESSUNG, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"auftrag": "gesamtaudit", "modell": "deepseek-v4-pro", "dauer_s": dauer,
                   "zeichen_prompt": len(prompt), "zeichen_antwort": len(text),
                   "usage": nutzung, "abbruch": abbruch,
                   "zeit": datetime.datetime.now().isoformat(timespec="seconds")},
                  f, ensure_ascii=False, indent=1)
    if not text.strip():
        log("LEER - die Antwort hat keinen Inhalt (nur Nachdenken). Nicht als Erfolg werten.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
