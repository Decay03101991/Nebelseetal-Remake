# -*- coding: ascii -*-
"""Baut das Entscheidungsverzeichnis aus dem Pruefregister (Daniel 03.11.2026, 22:4x).

WARUM
-----
Entscheidungen lagen verstreut: Register (176 Zeilen), mehrere ENTSCHEIDUNGEN_*.md und die
Datendateien selbst. Die Frage "was gilt gerade zu X, und ist es noch aktuell?" kostete jedes Mal
Sucherei. Dieses Werkzeug macht daraus EINE Tabelle - ohne neuen Inhalt und ohne eine Entscheidung zu
bewerten: es liest nur, was im Register steht.

WAS ES TUT
----------
Es liest `docs/PRUEFREGEL_ORIGINAL.md`, nimmt jede Tabellenzeile `| <Nr> | ... |` und schreibt je
Entscheidung EINE Zeile: Nummer, Kurzbezeichnung (der erste fett gesetzte Text), Stand (aus
Schluesselwoertern der Zeile abgeleitet), Tag und Fundstelle. Die Handpflege steht in
`docs/ENTSCHEIDUNGSVERZEICHNIS.md` NUR im Abschnitt "Ersetzt durch" - alles andere wird erzeugt.

AUFRUF
------
    python -X utf8 tools/entscheidungsverzeichnis_bauen.py [--schreiben]
Ohne `--schreiben` wird nur geprueft und die Zeilenzahl gemeldet (kein Schreibzugriff).
"""
from __future__ import annotations

import argparse  # Kommandozeile
import io        # Lesen und Schreiben mit festen Zeilenenden
import os        # Pfade
import re        # Muster fuer die Zeilen

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # Projektwurzel
REGISTER = os.path.join(WURZEL, "docs", "PRUEFREGEL_ORIGINAL.md")             # Quelle
ZIEL = os.path.join(WURZEL, "docs", "ENTSCHEIDUNGSVERZEICHNIS.md")            # Ziel

# Stand-Schluesselwoerter in der Reihenfolge ihrer Aussagekraft: das ERSTE Trefferwort gewinnt.
STAENDE = (
    ("ABGESEGNET", ("ABGESEGNET",)),                                         # entschieden, Bau offen
    ("GEBAUT", ("GEBAUT", "ERLEDIGT", "EINGEBAUT")),                         # umgesetzt und geprueft
    ("VERWORFEN", ("VERWORFEN", "ZURUECKGENOMMEN", "ABGELEHNT")),            # ausdruecklich nicht
    ("BLOCKIERT", ("BLOCKIERT", "WARTET", "OFFEN")),                         # haengt an etwas
    ("VORSCHLAG", ("VORSCHLAG",)),                                           # noch nicht entschieden
)


def register_zeilen(pfad: str):
    """Alle Entscheidungszeilen des Registers als (Nummer, Text) - ohne Kopf und Trennzeilen."""
    with io.open(pfad, encoding="utf-8", newline="") as datei:                # feste Zeilenenden lesen
        text = datei.read()
    ergebnis = []                                                             # gesammelte Zeilen
    for zeile in text.replace("\r\n", "\n").split("\n"):                      # Zeile fuer Zeile
        treffer = re.match(r"^\|\s*(\d+)\s*\|\s*(.*)$", zeile)                # Nummer am Zeilenanfang
        if not treffer:                                                       # keine Entscheidungszeile
            continue                                                          # ueberspringen
        ergebnis.append((int(treffer.group(1)), treffer.group(2)))            # Nummer und Rest
    return ergebnis                                                           # fertig


def kurzbezeichnung(text: str) -> str:
    """Der erste fett gesetzte Text der Zeile - das ist die Kennung der Entscheidung."""
    treffer = re.search(r"\*\*(.+?)\*\*", text)                               # erster Fettdruck
    if treffer:                                                               # gefunden
        kurz = treffer.group(1)                                               # Text daraus
    else:                                                                     # kein Fettdruck
        kurz = text.split("|")[0]                                             # dann der erste Abschnitt
    kurz = re.sub(r"\s+", " ", kurz).strip()                                  # Leerraum glaetten
    kurz = kurz.replace("|", "/")                                             # Pipes brechen die Tabelle
    return kurz[:160]                                                         # Laenge begrenzen


def stand(text: str) -> str:
    """Der Stand der Entscheidung aus ihren Schluesselwoertern (erstes Trefferwort gewinnt)."""
    oben = text.upper()                                                       # Grossschreibung vergleichen
    for name, woerter in STAENDE:                                             # je Stand die Woerter
        for wort in woerter:                                                  # jedes Schluesselwort
            if wort in oben:                                                  # gefunden
                return name                                               # dann dieser Stand
    return "unbekannt"                                                        # nichts gefunden


def tag(text: str) -> str:
    """Das Datum aus der letzten Zelle der Zeile (TT.MM.JJJJ), sonst leer."""
    zellen = [z.strip() for z in text.rstrip("|").split("|")]                 # Zellen der Zeile
    for zelle in reversed(zellen):                                            # von hinten suchen
        treffer = re.search(r"\d{2}\.\d{2}\.\d{4}", zelle)                    # Datum im Text
        if treffer:                                                           # gefunden
            return treffer.group(0)                                           # zurueckgeben
    return ""                                                                 # kein Datum


def bauen() -> str:
    """Das Verzeichnis als Markdown bauen (Tabelle plus Kopf und Pflegehinweis)."""
    zeilen = register_zeilen(REGISTER)                                        # Register lesen
    kopf = [
        "# Entscheidungsverzeichnis (erzeugt aus dem Register)",
        "",
        "> **Erzeugt** von `tools/entscheidungsverzeichnis_bauen.py` aus `docs/PRUEFREGEL_ORIGINAL.md`.",
        "> Nicht von Hand ergaenzen: eine neue Entscheidung gehoert ins Register, dann neu erzeugen.",
        "> **Handpflege gibt es nur im Abschnitt Ersetzungen** - dort steht, welche Entscheidung eine",
        "> fruehere abgeloest hat. Alles andere ist Ableitung, keine zweite Wahrheit.",
        "",
        "| Nr | Gegenstand | Stand | Tag |",
        "|---|---|---|---|",
    ]
    for nummer, text in zeilen:                                               # je Entscheidung
        kopf.append("| %d | %s | %s | %s |" % (nummer, kurzbezeichnung(text), stand(text), tag(text)))
    kopf += [
        "",
        "## Ersetzungen (Handpflege)",
        "",
        "Eine abgeloeste Entscheidung bleibt im Register stehen; hier steht, WODURCH sie ersetzt wurde.",
        "",
        "| Alt | Ersetzt durch | Was sich geaendert hat |",
        "|---|---|---|",
    ]
    return "\n".join(kopf) + "\n"                                             # fertiges Dokument


def main_lauf() -> int:
    """Kommandozeile: bauen, melden, optional schreiben."""
    parser = argparse.ArgumentParser(description="Entscheidungsverzeichnis aus dem Register bauen")
    parser.add_argument("--schreiben", action="store_true", help="Datei wirklich schreiben")
    args = parser.parse_args()                                                # Argumente
    text = bauen()                                                            # Dokument bauen
    zeilen = [z for z in text.split("\n") if z.startswith("| ") and z[2].isdigit()]   # Entscheidungszeilen
    staende = {}                                                              # Verteilung der Staende
    for z in zeilen:                                                          # je Zeile
        feld = z.split("|")[3].strip()                                        # die Stand-Spalte
        staende[feld] = staende.get(feld, 0) + 1                              # zaehlen
    print("Entscheidungen: %d | Staende: %s" % (len(zeilen), sorted(staende.items())))
    if args.schreiben:                                                        # Schreiben gewuenscht
        with io.open(ZIEL, "w", encoding="utf-8", newline="\n") as datei:     # feste Zeilenenden
            datei.write(text)                                                 # schreiben
        print("geschrieben:", ZIEL)                                           # Quittung
    else:                                                                     # nur pruefen
        print("(nicht geschrieben - --schreiben fehlt)")                      # Hinweis
    return 0                                                                  # Erfolg


if __name__ == "__main__":
    raise SystemExit(main_lauf())
