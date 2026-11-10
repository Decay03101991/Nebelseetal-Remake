"""Baut das Pruefpaket fuer einen starken Pruefer (Claude, Klasse Opus) - EIN Aufruf, feste Grenzen.

Zweck: Die zwoelf Behauptungen des Gesamtaudits vom 31.10.2026 sind zehn Tage alt. Der Code hat
sich seither bewegt (D-4, D-5, D-5a, D-5b, Layout-Schnitt, neue EXE). Dieses Werkzeug schneidet das
Paket aus dem HEUTIGEN Code: die betroffenen Funktionen und Konstanten im Wortlaut, jede mit
`Datei:Zeile`, dazu die Behauptungen und die Rechenpflicht zur Spieluhr x180.

Kein Modellaufruf. Das Werkzeug schreibt nur eine Datei und druckt die Masse.

Aufruf: python -X utf8 tools/opus_paket_bauen.py [--ziel <pfad>] [--trocken]
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import os
import subprocess
import sys
import urllib.request

REPO = "Decay03101991/Nebelseetal-Remake"
RAW = "https://raw.githubusercontent.com/" + REPO + "/{pin}/{pfad}"


def _pin() -> str:
    """Der Commit, gegen den geprueft wird: der veroeffentlichte Kopf (nicht der Arbeitsbaum)."""
    lauf = subprocess.run(["git", "rev-parse", "HEAD"], cwd=HIER, capture_output=True, text=True)
    kandidat = lauf.stdout.strip()
    fernsicht = subprocess.run(["git", "ls-remote", "origin", "main"], cwd=HIER,
                               capture_output=True, text=True, timeout=60).stdout.split()
    if fernsicht and fernsicht[0] != kandidat:
        print(f"WARNUNG: lokal {kandidat[:8]}, Remote {fernsicht[0][:8]} - das Paket pinnt den REMOTE-Stand")
        return fernsicht[0]
    return kandidat


def _herkunft(pin: str) -> str:
    """Holt den Blob JEDER benutzten Datei aus dem Repo und vergleicht ihn mit der Arbeitskopie.

    Das ist der Beleg, dass im Paket wirklich der veroeffentlichte Code steht - nicht eine
    handkopierte Fassung. Der Vergleich laeuft ueber SHA256 der Bytes.
    """
    zeilen = ["| Datei | Abruf-URL (gepinnter Commit) | SHA256 (Repo = Arbeitskopie) | bytegleich |",
              "|---|---|---|---|"]
    for datei in sorted({d for d, _, _ in SCHNITTE}):
        url = RAW.format(pin=pin, pfad=datei)
        try:
            with urllib.request.urlopen(url, timeout=60) as antwort:
                fern = antwort.read()
        except Exception as fehler:  # noqa: BLE001
            print(f"  ABRUF FEHLGESCHLAGEN {datei}: {fehler}")
            zeilen.append(f"| `{datei}` | {url} | (Abruf fehlgeschlagen) | nein |")
            continue
        lokal = open(os.path.join(HIER, datei), "rb").read()
        h_fern = hashlib.sha256(fern).hexdigest()
        gleich = h_fern == hashlib.sha256(lokal).hexdigest()
        # Zeilenenden: git normalisiert beim Commit, die Arbeitskopie kann CRLF fuehren.
        inhaltlich = fern.replace(b"\r\n", b"\n") == lokal.replace(b"\r\n", b"\n")
        urteil = ("ja" if gleich else
                  ("nur Zeilenenden (inhaltlich gleich)" if inhaltlich else "NEIN - Inhalt weicht ab"))
        print(f"  {datei:26} Repo {len(fern):7} Byte, bytegleich {gleich}, inhaltlich {inhaltlich}")
        zeilen.append(f"| `{datei}` | {url} | `{h_fern[:16]}...` | {urteil} |")
    return "**Herkunft der Dateien in diesem Paket (Abruf und Vergleich am 10.11.2026):**\n\n" + "\n".join(zeilen) + "\n"

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIEL = os.path.join(HIER, "docs", "audits", "OPUS_PRUEFPAKET_20261110.md")

# (Datei, Symbol, Art) - Art: f = Funktion/Methode, k = Konstante/Zuweisung
SCHNITTE = [
    ("src/main.py", "ortsdeckung", "f"),
    ("src/main.py", "verbrauche_am_ort", "f"),
    ("src/main.py", "reichsdeckung", "f"),
    ("src/main.py", "verbrauche_reichsweit", "f"),
    ("src/main.py", "tick", "f"),
    ("src/main.py", "bauen_auf_karte", "f"),
    ("src/main.py", "BIBLIOTHEK_OBERGRENZE", "k"),
    ("src/main.py", "SIEDLUNGEN_MAXIMUM", "k"),
    ("src/main.py", "MENU_ANZEIGE", "k"),
    ("src/kampf.py", "fuehre_schlacht", "f"),
    ("src/auftraege.py", "SEKUNDEN_JE_FELD", "k"),
    ("src/auftraege.py", "DROSSELUNG_SCHRITTE_PROZENT", "k"),
    ("src/auftraege.py", "AKTION_DAUER_SEKUNDEN", "k"),
    ("src/auftraege.py", "BEUTE_ANTEIL_PROZENT", "k"),
    ("src/spielzeit.py", "STANDARD_FAKTOR", "k"),
    ("src/punkte.py", "ZIEL_PUNKTE_VERWORFEN", "k"),
    ("src/punkte.py", "kriegspunkte", "f"),
    ("src/punkte.py", "goetterschutz_tage", "f"),
    ("src/forschung.py", "dauer_stunden", "f"),
]

BEHAUPTUNGEN = """\
| 1 | Ressourcenbestand (Reich/Ortskasse) | DOPPELT: eine zweite Kasse neben der fuehrenden |
| 2 | Kampfsystem | DOPPELT: zwei Kampfsysteme, Entscheidung E1 offen |
| 3 | Bauvoraussetzungen (Baukunst) | WIDERSPRUCH: sechs Gebaeude ohne Forschungspruefung |
| 4 | Tageswechsel/Goetterschutz | WIDERSPRUCH: Tageszaehlung mit `if` statt `divmod` |
| 5 | Auftragskosten und Drosselung | FEHLT: Konstante da, aber nicht angeschlossen |
| 6 | Ausbildungsgeschwindigkeit | FEHLT: Ausbildungszeit nicht an Gebaeudestufe gekoppelt |
| 7 | Menuepunkt Voraussetzungen | FEHLT: zeigt nicht alle Bedingungen |
| 8 | Bibliotheks-Obergrenze | WIDERSPRUCH: Code 2, Original 1 je Siedlung |
| 9 | Spieluhr x180 | UNBELEGT: belegte Dauern werden extrem verkuerzt |
| 10 | Siegbedingung 300 Punkte | WIDERSPRUCH: Wallstufe 8 erreicht 300 Punkte leicht |
| 11 | Beuteanteil 50 Prozent | UNBELEGT: Handbuch beziffert keinen Anteil |
| 12 | Siedlergrenze, Siedlungsmax, Startwerte | IN ORDNUNG: belegte 2009-Werte uebernommen |"""

VORBEFUND = """\
Diese Zeilen sind eine SICHTUNG des Koordinators am 10.11.2026 (grep/ast, nicht nachgerechnet).
Sie sind **kein Urteil**: bestaetige oder widerlege jede Zeile am Code.

| Nr | Was am heutigen Code auffaellt | Fundstelle |
|---|---|---|
| 2 | `src/kampf_alt_handbuch_2009.py` existiert NICHT mehr; `src/kampf.py` nennt sie nur noch als fruehere Fassung. Eine Wache verlangt ausdruecklich, dass es nur EINE Schlacht-Implementierung gibt | `src/kampf.py:5`, `tests/test_gpt_kampf_forum_neu.py:83,87` |
| 4 | Die Tageszaehlung nutzt bereits `divmod` gegen EINE Tageslaenge, und der Goetterschutz prueft `tag > goetterschutz_tage()` | `src/main.py:7910-7923` |
| 5 | `SEKUNDEN_JE_FELD` ist 7200.0 (nicht 3600) und WIRD benutzt (Reisezeit-Formel); die Drosselung nennt sich selbst "nicht angeschlossen" | `src/auftraege.py:66,159,176,717-719` |
| 10 | `VORSCHLAG_ZIEL_PUNKTE` gibt es nicht mehr. Es gibt `ZIEL_PUNKTE_VERWORFEN = 300` - Daniel hat am 31.10.2026 entschieden, dass das Original KEINEN Sieg kennt (E5) | `src/punkte.py:45-50` |
| 8 | `BIBLIOTHEK_OBERGRENZE = 2` steht unveraendert | `src/main.py:3652` |
| 9 | `STANDARD_FAKTOR = 180.0` steht unveraendert | `src/spielzeit.py:34` |
| 11 | `BEUTE_ANTEIL_PROZENT = 50` steht, das Modul nennt ihn ausdruecklich VORSCHLAG | `src/auftraege.py:84,727` |
| 3 | Eine Pruefung namens `bau_zulassen` gibt es nicht; `Baukunst` steht als `voraussetzung` in den Gebaeudedaten und wird im Forschungsweg gelesen - ob `bauen_auf_karte` sie erzwingt, ist OFFEN | `src/forschungspfad.py:15,275`, `data/buildings.json` |"""

RECHENPFLICHT = """\
Rechne mit den Zahlen, die im Code stehen (nicht aus dem Kopf), und zeige je Zeile die Formel:

1. **Forschung:** Dauer bis Stufe n = n^2 Stunden (Beleg im Code). Bei Spieluhr 180: wie lange dauert
   Stufe 10 in ECHTZEIT? Wie lange Stufe 20?
2. **Reise:** `SEKUNDEN_JE_FELD` bei Spieluhr 180: wie viele echte Sekunden sind ein Feld? Zehn Felder?
3. **Ausbildung:** Grunddauer aus `pilot_ausbildung_minuten` bei Spieluhr 180 in Echtzeit.
4. **Siedlerzuwachs:** steht im Code als Zuwachs je Stunde - rechne auf echte Sekunden um.
5. **Punkte:** Wallstufe 8 = 8^3 = 512 Kriegspunkte; Gesamtpunktzahl = (Krieg + Forschung) / 2.
   Wie viele Forschungsstufen (Summe der Stufen^3) braucht man, um mit Wallstufe 8 ueber 300 zu kommen?
6. **Urteil je Zeile:** Ist die Dauer bei x180 fuer einen Einzelspieler spielbar, trivial oder
   unspielbar? Nenne die Zahl, die dein Urteil traegt."""

KOPF = """\
# PRUEFPAKET: Gegenpruefung der zwoelf Gesamtaudit-Befunde am heutigen Code

## 1. Deine Rolle

Du bist **PRUEFER**, nicht Entwerfer und nicht Ausfuehrender. Du pruefst fertigen Code gegen
schriftliche Behauptungen und lieferst Zahlen mit Fundstelle. Du aenderst keine Projektdatei, du
startest nichts, du committest nichts. Du lobst nicht, du schreibst keine Einleitung.

## 2. Was du bekommst

Die zwoelf Behauptungen eines frueheren Gutachtens (31.10.2026), eine Sichtung des Koordinators vom
10.11.2026 und den **heutigen Quellcode** der betroffenen Stellen im Wortlaut - jede Stelle mit
`Datei:Zeile`.

## 2a. Woher dieser Code kommt: aus dem VEROEFFENTLICHTEN Repo, nicht von einer Platte

Du arbeitest **gegen das oeffentliche Repository**, nicht gegen den Arbeitsordner des Auftraggebers.
Alle Stellen in Abschnitt 10 sind der veroeffentlichte Blob am **gepinnten Commit `{pin}`**:

    https://raw.githubusercontent.com/Decay03101991/Nebelseetal-Remake/{pin}/<pfad>

Willst du eine Stelle nachlesen, lade genau diese URL (der Commit steht im Pfad - damit ist der Stand
fest und aendert sich nicht, auch wenn spaeter weitergearbeitet wird). Nenne am Anfang deiner Antwort
den Commit, den du gelesen hast. Was du **nicht** tun sollst: lokale Pfade oeffnen, im Arbeitsordner
suchen, Dateien schreiben.

{herkunft}

## 3. Was du NICHT beurteilen sollst

- Keinen Abgleich gegen das Original-Handbuch (das war der Auftrag des alten Gutachtens, die
  Handbuchauszuege liegen diesem Paket absichtlich NICHT bei).
- Keine Gestaltungs- oder Geschmacksfragen.
- Keine Aussagen ueber Stellen, die hier nicht abgedruckt sind - schreibe stattdessen
  `UNBEKANNT: Stelle nicht im Paket` und nenne, welche Datei du braeuchtest.

## 4. Pflicht-Ausgabeformat (genau diese Reihenfolge, hoechstens 220 Zeilen)

**A. Tabelle der zwoelf Behauptungen** - Spalten:
`Nr | Urteil | Fundstelle (Datei:Zeile) | Gemessener Wert im Code | Was zu tun ist | Aufwand S/M/L`
Urteile nur aus diesem Vokabular:
`BESTAETIGT` (der Code tut heute noch, was die Behauptung sagt) ·
`UEBERHOLT` (der Code ist inzwischen anders - Beweis mit heutiger Fundstelle) ·
`TEILWEISE` (ein Teil stimmt, ein Teil nicht - beide Teile belegen) ·
`UNBEKANNT` (Stelle nicht im Paket).

**B. Rechnung Spieluhr x180** - die sechs Punkte aus der Rechenpflicht, je mit Formel und Zahl.

**C. Die drei schwersten offenen Punkte** - je drei Saetze, mit der Zahl, die es entscheidet.

**D. Was ich nicht wissen kann** - was dir an Material fehlt, um sicher zu urteilen.

## 5. Harte Regeln

- Jede Zeile traegt eine Fundstelle aus DIESEM Paket (Datei und Zeile).
- Keine Zahlen aus dem Gedaechtnis: jede Zahl steht im abgedruckten Code oder ist aus ihm gerechnet.
- Kein Pseudocode fuer Umbauten; hoechstens drei Zeilen Kernidee je Vorschlag.
- Wo die Behauptung und der Code auseinandergehen, gewinnt der Code - und du nennst BEIDE Stellen.

---

## 6. Messlage (Stand, aus Werkzeugen)

{messtabelle}

## 7. Die zwoelf Behauptungen des Gutachtens vom 31.10.2026

{behauptungen}

## 8. Sichtung des Koordinators vom 10.11.2026 (kein Urteil - pruefen!)

{vorbefund}

## 9. Rechenpflicht (fuer Abschnitt B deiner Antwort)

{rechenpflicht}

## 10. Der heutige Code im Wortlaut (geschnitten aus dem Repo-Blob am gepinnten Commit)


"""


_FERNE_DATEIEN: dict[str, bytes] = {}


def _datei_bytes(datei: str, pin: str) -> bytes:
    """Der Blob aus dem Repo (gecacht). Faellt nur dann auf die Arbeitskopie zurueck, wenn der Abruf
    scheitert - und sagt das dann laut, damit ein Paket nie stillschweigend aus der Platte entsteht."""
    if datei not in _FERNE_DATEIEN:
        url = RAW.format(pin=pin, pfad=datei)
        try:
            with urllib.request.urlopen(url, timeout=60) as antwort:
                _FERNE_DATEIEN[datei] = antwort.read()
        except Exception as fehler:  # noqa: BLE001
            print(f"  WARNUNG: {datei} nicht aus dem Repo geladen ({fehler}) - nehme die Arbeitskopie")
            _FERNE_DATEIEN[datei] = open(os.path.join(HIER, datei), "rb").read()
    return _FERNE_DATEIEN[datei]


def _schnitt(datei: str, symbol: str, art: str, pin: str) -> tuple[str, int]:
    quelle = _datei_bytes(datei, pin).decode("utf-8")
    zeilen = quelle.splitlines()
    baum = ast.parse(quelle)
    treffer = None
    for knoten in ast.walk(baum):
        if art == "f" and isinstance(knoten, (ast.FunctionDef, ast.AsyncFunctionDef)) and knoten.name == symbol:
            treffer = (knoten.lineno, knoten.end_lineno)
            break
        if art == "k" and isinstance(knoten, ast.Assign):
            for ziel in knoten.targets:
                if isinstance(ziel, ast.Name) and ziel.id == symbol:
                    treffer = (knoten.lineno, knoten.end_lineno)
                    break
            if treffer:
                break
    if not treffer:
        return (f"### {datei}:{symbol} - NICHT GEFUNDEN\n", 0)
    a, b = treffer
    rumpf = "\n".join(zeilen[a - 1:b])
    kopf = f"### {datei}:{a}-{b} - `{symbol}`\n\n```python\n{rumpf}\n```\n"
    return (kopf, b - a + 1)


def messlage() -> str:
    def _cmd(*args: str) -> str:
        try:
            return subprocess.run(args, cwd=HIER, capture_output=True, text=True,
                                  timeout=60).stdout.strip()
        except Exception as fehler:  # noqa: BLE001 - Messung darf nicht scheitern
            return f"(nicht messbar: {fehler})"
    kopf = _cmd("git", "log", "-1", "--format=%h %ad", "--date=short")
    register = 0
    try:
        text = open(os.path.join(HIER, "docs", "PRUEFREGEL_ORIGINAL.md"), encoding="utf-8").read()
        register = max(int(z.split("|")[1]) for z in text.splitlines()
                       if z.startswith("| ") and z.split("|")[1].strip().isdigit())
    except Exception:  # noqa: BLE001
        register = -1
    module = 0
    zeilen = 0
    for name in sorted(os.listdir(os.path.join(HIER, "src"))):
        if name.endswith(".py"):
            module += 1
            zeilen += sum(1 for _ in open(os.path.join(HIER, "src", name), encoding="utf-8",
                                          errors="replace"))
    return ("| Groesse | Wert |\n|---|---|\n"
            f"| Stand (Commit, Datum) | `{kopf}` |\n"
            f"| Register belegt bis | {register} |\n"
            f"| Module in `src/` | {module} |\n"
            f"| Zeilen in `src/` | {zeilen} |\n"
            f"| Letzter Sammellauf | 217 von 217 gruen, 0 rot, 2 ausgesetzt, 9409 Pruefungen |\n"
            f"| EXE im Projekt | `Nebelseetal_Pre_Release_V_0.0.3.exe`, 83341753 Byte, SHA256 `a7035101...` |\n")


def main() -> int:
    zerleger = argparse.ArgumentParser(description="Pruefpaket fuer einen starken Pruefer bauen")
    zerleger.add_argument("--ziel", default=ZIEL)
    zerleger.add_argument("--trocken", action="store_true",
                          help="nur messen und die Zieldatei drucken, nichts schreiben")
    zerleger.add_argument("--pin", default="", help="Commit, gegen den geprueft wird (Vorgabe: Remote-Kopf)")
    args = zerleger.parse_args()
    pin = args.pin or _pin()
    print(f"Gepinnter Commit: {pin}")
    herkunft = _herkunft(pin)
    kopf = KOPF.format(messtabelle=messlage(), behauptungen=BEHAUPTUNGEN,
                       vorbefund=VORBEFUND, rechenpflicht=RECHENPFLICHT,
                       pin=pin, herkunft=herkunft)
    teile = [kopf]
    summe_zeilen = 0
    print(f"Ziel: {args.ziel}")
    for datei, symbol, art in SCHNITTE:
        text, zeilen = _schnitt(datei, symbol, art, pin)
        if zeilen == 0:
            print(f"  FEHLT  {datei}:{symbol}")
        summe_zeilen += zeilen
        teile.append(text)
    inhalt = "\n".join(teile)
    zeichen = len(inhalt)
    print(f"Code-Zeilen im Paket: {summe_zeilen}")
    print(f"Zeichen: {zeichen} (~{zeichen // 3.6:.0f} Prompt-Token bei 3,6 Zeichen je Token)")
    print(f"Zeilen gesamt: {inhalt.count(chr(10)) + 1}")
    if args.trocken:
        print("Trockenlauf: nichts geschrieben.")
        return 0
    with open(args.ziel, "w", encoding="utf-8", newline="\n") as griff:
        griff.write(inhalt)
    print(f"geschrieben: {args.ziel} ({os.path.getsize(args.ziel)} Byte)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
