"""Prueft die Textqualitaet der Dokumente - strenger als ein Mensch beim Ueberfliegen.

Warum: Am 31.10.2026 fanden wir 372 falsche Anfuehrungszeichen und 38 eingeklebte Saetze
("Kampfablauf:Aktuell"). Solche Fehler entstehen beim Einfuegen und fallen niemandem auf -
deshalb prueft es ab jetzt ein Test, nicht das Auge.

Geprueft wird in jeder Markdown-Datei (README, docs/*.md, docs/audits/*.md):
  1. Deutsche Anfuehrungszeichen sind gepaart: „ ... “ - gleich viele auf und zu.
  2. Nach einem Satzzeichen klebt kein Wort: "Text.weiter" ist falsch, "Text. weiter" richtig.
  3. Kein gerades " direkt nach einem geoeffneten „ (das war der haeufigste Fehler).
  4. Keine doppelten Woerter ("die die" nur, wenn grammatisch richtig - darum NICHT geprueft).

Code-Bloecke (```) und Inline-Code (`...`) werden ausgenommen: dort stehen absichtlich Zeichen.
"""
from __future__ import annotations

# --- Pruefstand-Kopf (M1, 12.11.2026): Art, Stufe, BETRIFFT, DATEN ----------------
# Gelesen von harness.kopf_lesen und tools/auswahl.py. Vorschlag aus Paket 15b
# (gemessene Art und Dauer des Sammellaufs). Beim Anfassen der Datei genauer machen.
PRUEF_ART = "rechnen"
PRUEF_STUFE = 1
PRUEF_BETRIFFT = ['main:*']
PRUEF_DATEN = []
# --- Ende Pruefstand-Kopf -------------------------------------------------------

import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(WURZEL, "tests"))            # harness liegt hier
OEFFNEN, SCHLIESSEN = "\u201e", "\u201c"
# Technische Schreibweisen sind kein Textfehler: "Datei:Zeile" in Tabellen,
# "tk.PhotoImage" in einem Satz. Diese Woerter sind erlaubt.
ERLAUBT = {"Zeile", "Spalte", "Datei", "Pfad", "Kapitel", "Seite"}
KLEBEND = re.compile(r"(?<![0-9])[.:,]([A-ZÄÖÜ][a-zäöüß]{3,})")
GERADE_NACH_AUF = re.compile(OEFFNEN + '([^' + SCHLIESSEN + OEFFNEN + '"]{1,200})"')

# F-80 (Daniel 13.11.2026): eigene Zaehlung durch `harness` ersetzt - dieselben Pruefungen,
# jetzt mit Messwerten, Befundkanal und einer ERGEBNIS-Zeile. `check(name, bedingung, meldung)`
# hat dieselbe Signatur wie `harness.check`.
from harness import bericht, check  # noqa: E402


def dateien():
    pfade = [os.path.join(WURZEL, "README.md")]
    for ordner in ("docs", os.path.join("docs", "audits")):
        voll = os.path.join(WURZEL, ordner)
        if os.path.isdir(voll):
            pfade += [os.path.join(voll, n) for n in sorted(os.listdir(voll)) if n.endswith(".md")]
    # Rohe Modellantworten (BEFUND_*, GESAMTAUDIT_*, PROMPT_*) werden nicht redigiert -
    # sie sind Belege. Fuer sie gilt die Textpruefung nicht.
    roh = ("BEFUND_", "GESAMTAUDIT_", "PROMPT_")
    return [p for p in pfade if os.path.isfile(p)
            and not os.path.basename(p).startswith(roh)]


def ohne_code(text: str) -> str:
    text = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    return re.sub("`[^`" + chr(10) + "]*`", "", text)


def main() -> int:
    alle = dateien()
    check("1 Es gibt Dokumente zu pruefen", len(alle) >= 20, f"nur {len(alle)} gefunden")

    for pfad in alle:
        name = os.path.relpath(pfad, WURZEL)
        with open(pfad, encoding="utf-8") as f:
            roh = f.read()
        text = ohne_code(roh)

        auf, zu = text.count(OEFFNEN), text.count(SCHLIESSEN)
        check(f"2 {name} Anfuehrungszeichen gepaart", auf == zu, f"{auf} auf, {zu} zu")

        klebend = []
        for m in KLEBEND.finditer(text):
            wort = m.group(1)
            davor = text[max(0, m.start() - 12):m.start() + 1]
            if wort in ERLAUBT or "." in davor:
                continue  # "Datei:Zeile" oder "tk.PhotoImage" - technische Schreibweise
            if "„" in text[max(0, m.start() - 40):m.start()]:
                continue  # Zitat eines Fehlers, absichtlich so geschrieben
            klebend.append(wort)
        check(f"3 {name} keine eingeklebten Woerter", not klebend,
              f"{len(klebend)} Stellen: {', '.join(klebend[:5])}")

        gerade = GERADE_NACH_AUF.findall(text)
        check(f"4 {name} kein gerades Anfuehrungszeichen als Schluss", not gerade,
              f"{len(gerade)} Stellen")

        # 5. Kaputte Markdown-Links auf lokale Dateien
        for ziel in re.findall(r"\]\(([^)]+)\)", text):
            ziel = ziel.split("#")[0].strip()
            if not ziel or ziel.startswith(("http", "mailto:", "MEDIA:", "::")):
                continue
            voll = os.path.normpath(os.path.join(os.path.dirname(pfad), ziel))
            check(f"5 {name} Linkziel vorhanden", os.path.exists(voll), ziel)

    from harness import messwert
    messwert("dokumente", len(alle), "Stueck")
    return bericht()


if __name__ == "__main__":
    sys.exit(main())
