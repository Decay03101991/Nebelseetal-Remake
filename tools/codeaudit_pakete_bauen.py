"""Baut die Pakete fuer den Code-Audit (31.10.2026) - je Paket eine enge Frage.

Daniels Auftrag: "lasse ein grosses model den code checken und beauftrage es nach kompakteren
kluegeren code loesungen zu suchen ... alle funktionen unbeeintraechtigt ... ordnerstruktur
angepasst aber sauber."

Aufbau jedes Pakets:
  1. Rolle und harte Regeln (Spiel bleibt Spiel, keine Verhaltensaenderung, Tests sind der Beweis)
  2. Die gemessenen Zahlen des Projekts (damit das Modell nicht raten muss)
  3. Der Code der betroffenen Dateien im Wortlaut
  4. Ein festes Ausgabeformat (Tabelle + Begruendung), damit ich die Antwort pruefen kann

Aufruf:
    python -X utf8 tools/codeaudit_pakete_bauen.py P1            # ein Paket
    python -X utf8 tools/codeaudit_pakete_bauen.py --alle        # alle Pakete
"""
from __future__ import annotations

import os
import sys

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIELORDNER = os.path.join(HIER, "docs", "audits", "code")

KOPF = """# Code-Audit Nebelseetal Remake — Paket {kennung}: {titel}

## Deine Rolle

Du bist Software-Architekt und prüfst einen gewachsenen Python-Code (tkinter-Spiel, deutsch
kommentiert, 18.400 Zeilen Prüfcode). Der Code ist über Monate **angebaut** worden: neue Funktionen
kamen dazu, alte blieben, Doppelungen wurden nie zusammengeführt. Deine Aufgabe ist **nicht**,
Eleganz zu predigen, sondern konkrete, umsetzbare Zusammenführungen zu benennen.

## Harte Regeln (daran wird deine Antwort gemessen)

1. **Das Spiel bleibt unser Spiel.** Kein Verhalten darf sich ändern: keine anderen Zahlen, keine
   anderen Regeln, keine andere Bedienung. Reine Struktur- und Lesbarkeitsarbeit.
2. **Jede Funktion bleibt erhalten**, solange sie aufgerufen wird. Was niemand aufruft, nennst du
   ausdrücklich als „entfernbar" mit Begründung.
3. **Der Prüfcode ist der Beweis.** Zu jedem Vorschlag gehört: welche vorhandene Prüfdatei
   (tests/*.py) muss danach grün bleiben? Wenn keine existiert, sagst du das offen.
4. **Deutsch, ASCII in Code-Kommentaren** (das Projekt hält `src/botkern.py` bewusst ASCII).
5. **Keine erfundenen Zeilenzahlen.** Wenn du eine Ersparnis schätzt, schreib „geschätzt".

## Was das Projekt über sich sagt (gemessen, nicht geschätzt)

* `src/`: 49 Dateien, 21.703 Zeilen, 17.406 Codezeilen, 904 Funktionen/Methoden.
* `main.py` allein: 7.375 Zeilen, 240 Methoden, davon 27 `_render_*`-Methoden.
* Funktionen ab 60 Zeilen: 47 (längste 205 Zeilen, `_render_settlement_map`).
* 58 Sechs-Zeilen-Blöcke stehen mehrfach identisch im Code.
* `kampf.py` (398 Z.) und `kampf_alt_handbuch_2009.py` (401 Z.) enthalten je eine
  `fuehre_schlacht` (188 bzw. 194 Zeilen) — `kampf.py` importiert die alte Fassung.
* Oberfläche: tkinter, alles in einer Klasse; Ansichten `_render_*`, Aufbau `_build_main_ui`.
* Prüfcode: `tests/` 18.418 Zeilen, 98 Dateien, Aufruf über `tools/sammellauf.py`.

## Deine Aufgabe

{frage}

## Der Code

{code}

## Ausgabeformat (genau so, nichts anderes)

### 1. Befund in fünf Sätzen
Was ist hier wirklich das Problem — mit Zahlen aus dem Code.

### 2. Vorschläge (Tabelle, absteigend nach Nutzen)

| # | Was | Dateien/Funktionen | Zeilen vorher → nachher | Risiko (klein/mittel/groß) | Beweis: welche Prüfdatei | Reihenfolge |
|---|---|---|---|---|---|---|

### 3. Zusammenführung im Detail
Für die zwei wichtigsten Vorschläge: welche Funktionen verschmelzen zu welcher neuen Funktion,
welche Parameter, welcher Rückgabewert, was passiert mit Sonderfällen. Kein vollständiger Code —
nur Signatur plus drei bis fünf Zeilen Kern.

### 4. Was du NICHT anfassen würdest
Und warum. (Beispiel: Zeichencode der Oberfläche, der auf Pixel wirkt.)

### 5. Ordnung
Wie sähe eine saubere Ordner-/Dateistruktur für diesen Teil aus? Namen der Dateien, was in welche
gehört, und **in welcher Reihenfolge man umzieht, ohne dass Importe brechen**.
"""

PAKETE = {
    "P1": {
        "titel": "Aufteilung von main.py (7.375 Zeilen, 240 Methoden)",
        "frage": (
            "`main.py` enthält Fensteraufbau, Spielzustand, Spiellogik-Verdrahtung, alle Ansichten und "
            "die Kartenzeichnung. Entwirf die Aufteilung in thematische Module: **welche Funktionen "
            "gehören in welche neue Datei**, wie heißen sie, was importiert was (keine Zyklen!), und in "
            "welcher Reihenfolge zieht man um, ohne dass die EXE oder die 98 Prüfdateien brechen. "
            "Nenne zusätzlich die 27 `_render_*`-Methoden, die so viel Gerüst teilen, dass ein "
            "gemeinsamer Helfer sie ersetzt (welcher Helfer, welche Parameter)."),
    },
    "P2": {
        "titel": "Zwei Schlacht-Implementierungen (kampf.py und kampf_alt_handbuch_2009.py)",
        "frage": (
            "Es gibt zwei `fuehre_schlacht` (188 und 194 Zeilen) und `kampf.py` importiert die alte "
            "Fassung. Stelle fest: was ist in der alten Fassung anders, was wird davon noch gebraucht, "
            "und was kann ersatzlos weg? Ziel: **eine** Schlachtfunktion, ohne dass sich das Ergebnis "
            "der Kämpfe ändert. Wenn die alte Fassung einen Sonderfall abdeckt, den die neue nicht "
            "kennt, benenne ihn genau."),
    },
    "P3": {
        "titel": "Doppelte Rechenwege in Wirtschaft und Aufträgen",
        "frage": (
            "In `auftraege.py`, `spieloekonomie.py`, `werkstatt.py` und `kampfbericht.py` gibt es "
            "mehrfach Rechnungen für Reisezeit, Kosten, Bestand und Beute. Finde die Dubletten und "
            "schlage je eine gemeinsame Funktion vor (Name, Parameter, Rückgabe, wo sie hingehört). "
            "Wichtig: die Werte müssen exakt gleich bleiben — nenne für jede Dublette, ob die "
            "Formeln heute wirklich identisch sind oder nur ähnlich aussehen."),
    },
    "P4": {
        "titel": "Vier Zeichenmodule der Karten (2.960 Zeilen Optik)",
        "frage": (
            "`welt_optik.py`, `welt_optik_fein.py`, `karten_optik.py` und `karten_optik_fein.py` "
            "zeichnen Welten und Siedlungen in unterschiedlicher Feinheit. Prüfe: wie viel davon ist "
            "gemeinsames Gerüst (Flächen, Pfade, Symbole, Farben), wie viel ist wirklich verschieden? "
            "Vorschlag: welche gemeinsamen Bausteine, welche Dateien bleiben, welche fallen weg — "
            "ohne dass ein Pixel anders aussieht."),
    },
    "P5": {
        "titel": "Ordnerstruktur des ganzen Projekts",
        "frage": (
            "Entwirf aus der Modulliste die Zielstruktur für `src/`, `tests/` und `tools/`: welche "
            "Themenordner, welche Datei wohin, wie bleiben Importe, PyInstaller-Build "
            "(`tools/build_exe.py`) und die 98 Prüfdateien intakt? Nenne die Umzugsreihenfolge in "
            "Schritten, sodass nach **jedem** Schritt alles noch läuft. Bevorzuge flache, sprechende "
            "Namen gegenüber tiefer Verschachtelung."),
    },
}


def dateien_fuer(kennung: str) -> list[str]:
    return {
        "P1": ["src/main.py"],
        "P2": ["src/kampf.py", "src/kampf_alt_handbuch_2009.py"],
        "P3": ["src/auftraege.py", "src/spieloekonomie.py", "src/werkstatt.py", "src/kampfbericht.py"],
        "P4": ["src/welt_optik.py", "src/welt_optik_fein.py", "src/karten_optik.py", "src/karten_optik_fein.py"],
        "P5": [],
    }[kennung]


def modulliste() -> str:
    zeilen = ["```"]
    for name in sorted(os.listdir(os.path.join(HIER, "src"))):
        if name.endswith(".py"):
            pfad = os.path.join(HIER, "src", name)
            with open(pfad, encoding="utf-8") as f:
                anzahl = len(f.read().split("\n"))
            zeilen.append(f"src/{name:34s} {anzahl:5d} Zeilen")
    zeilen.append("```")
    return "\n".join(zeilen)


def bauen(kennung: str) -> str:
    info = PAKETE[kennung]
    teile = []
    for rel in dateien_fuer(kennung):
        with open(os.path.join(HIER, rel.replace("/", os.sep)), encoding="utf-8") as f:
            inhalt = f.read()
        teile.append(f"### Datei `{rel}` ({len(inhalt.split(chr(10)))} Zeilen)\n\n```python\n{inhalt}\n```\n")
    if kennung == "P5":
        teile.append("### Modulliste\n\n" + modulliste() + "\n")
    code = "\n".join(teile) if teile else "(kein Code - nur die Modulliste unten)"
    return KOPF.format(kennung=kennung, titel=info["titel"], frage=info["frage"], code=code)


def main() -> int:
    os.makedirs(ZIELORDNER, exist_ok=True)
    kennungen = list(PAKETE) if "--alle" in sys.argv else [a for a in sys.argv[1:] if a in PAKETE]
    if not kennungen:
        print("Aufruf: python tools/codeaudit_pakete_bauen.py P1|P2|P3|P4|P5|--alle")
        return 2
    for k in kennungen:
        text = bauen(k)
        pfad = os.path.join(ZIELORDNER, f"CODE_{k}_{PAKETE[k]['titel'].split('(')[0].strip().replace(' ', '_')[:40]}.md")
        with open(pfad, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print(f"{k}: {len(text):7d} Zeichen (~{len(text) // 4:6d} Token) -> {os.path.relpath(pfad, HIER)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
