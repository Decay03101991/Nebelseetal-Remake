"""Baut das Paket P1 (Spieltest-Bewertung) fuer ein grosses Modell.

Es nimmt den NEUESTEN Simulations-Lauf (`docs/audits/SPIELTEST_LOG_*.md`) und stellt ihn einem
starken Modell als Pruefmaterial hin - mit festem Auftrag und festem Ausgabeformat. Ergebnis ist
eine Datei, die Daniel und der naechsten Sitzung als Kritik vorliegt.

Aufruf:
    python -X utf8 tools/spieltest_paket_bauen.py
"""
from __future__ import annotations

import glob
import os

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIEL = os.path.join(HIER, "docs", "audits", "auftraege", "P1_spieltest.md")

RAHMEN = """ROLLE
Du bist erfahrener Spieldesigner und Playtester. Du bewertest einen ECHTEN, ohne Oberflaeche
gefahrenen Spielverlauf eines Remakes (Python, Einzelspieler gegen Bots) und sagst, was dem
Spieler Spass macht und was ihn vertreibt. Du erfindest keine Zahlen und keine Quellen; was du
nicht weisst, schreibst du als "nicht beurteilbar".

WAS DAS SPIEL IST
* Remake eines deutschen Browserspiels von 2006/2009. Original: viele Spieler, Handel, Krieg,
  Ruhmeshalle. Remake: EIN Mensch, wenige Bots.
* Spieluhr x180: 1 Spielstunde = 20 echte Sekunden, 1 Spieltag = 8 echte Minuten.
* Reisezeit = 2 * Distanz / Geschwindigkeit (Spielstunden), Rueckweg doppelt.
* KEIN Sieg (das Original kennt keine Siegbedingung). Stattdessen vier Auszeichnungen:
  Feldherr (Kriegspunkte), Forscher (Forschungspunkte), Haendler (Handelspunkte, nur 2006 belegt),
  Gesamtherrscher ((Krieg+Forschung)/2).
* Beute gestaffelt nach Wallzustand und ueberlebenden Verteidigern: 10/30/60/100 Prozent,
  immer begrenzt durch Karrenladung und Vorrat (Hausregel, das Original kennt nur 100 Prozent).
* Goetterschutz: 7 Tage; bis 299 Punkte darf nur im Band +/- 20 Prozent angegriffen werden.
* Mana: 5 je Stunde auf Nebelsee, sonst 1 (Handbuch 2009).
* Gold kommt aus der Goldmine (Berg/Huegel), Nahrung aus Farm (Grasland/Steppe) und Jaeger,
  Holz aus Holzfäller (Wald/Steppe), Stein aus Steinmetz (Berg/Huegel).
* Einheiten brauchen Gold, Siedler und eine Ausbildungsstaette (Kriegerakademie, Diebesgilde,
  Stellmacher); die Ausbildungsdauer ist 20 Spielminuten / Gebaeudestufe (Richtung belegt,
  Zahl VORSCHLAG).

WAS DU BEKOMMST
Der Spielverlauf unten ist mit einer einfachen, ausdruecklich NICHT optimalen Spielerpolitik
erzeugt: alle 20 Spielminuten ein Schritt, Gebaeude in fester Reihenfolge (je hoechstens 2),
Forschung wenn bezahlbar, Ausbildung wenn bezahlbar, ab Spieltag 2 ein Angriff.

AUFGABE
1. LIES den Verlauf und beantworte: Was bremst diesen Lauf? Nenne die Engstelle mit Zahl
   (Rohstoff, Tag, Menge).
2. Ist das Tempo bei x180 richtig? Rechne zwei Beispiele nach (Bau, Forschung) und sage, ob ein
   Mensch in den ersten 20 echten Minuten etwas Sinnvolles tun kann.
3. Was fehlt einem Spieler in den ersten 30 Minuten, um zu verstehen, was er tun soll?
   Hoechstens 5 Punkte, je ein Satz.
4. Fuenf konkrete Aenderungen, jede mit Zahl und Aufwand S/M/L. Keine allgemeinen Ratschlaege.
5. Was kannst du mit diesem Verlauf NICHT beurteilen?
6. Eine Frage, die du Daniel stellen wuerdest, bevor du weiterarbeitest.

AUSGABEFORMAT - halte es GENAU ein, nichts davor und nichts danach
## Engstelle
| Rohstoff | Tag | Wert | Beleg im Verlauf | Was zu tun ist |
## Tempo bei x180
| Beispiel | Rechnung | Urteil |
## Erste 30 Minuten
## Fuenf Aenderungen
| Nr | Aenderung | Zahl | Aufwand | Wirkung |
## Nicht beurteilbar
## Die eine Frage

Sprache: Deutsch. Keine Einleitung, kein Lob.
"""


def neuester_log() -> str:
    dateien = sorted(glob.glob(os.path.join(HIER, "docs", "audits", "SPIELTEST_LOG_*.md")))
    if not dateien:
        raise SystemExit("Kein Simulationslauf gefunden - erst tools/spieltest_simulation.py laufen lassen.")
    return dateien[-1]


def main() -> int:
    log_datei = neuester_log()
    with open(log_datei, encoding="utf-8") as f:
        log = f.read()
    text = (RAHMEN
            + "\n==============================================================================\n"
            + "SPIELVERLAUF (Simulation, ohne Oberflaeche)\n"
            + "==============================================================================\n\n"
            + log
            + "\n\n(Ende des Verlaufs. Er stammt aus `tools/spieltest_simulation.py`, nicht aus einem "
              "menschlichen Spiel.)\n")
    os.makedirs(os.path.dirname(ZIEL), exist_ok=True)
    with open(ZIEL, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"Paket: {ZIEL}")
    print(f"Quelle: {os.path.basename(log_datei)}")
    print(f"Groesse: {len(text)} Zeichen (~{len(text) / 3.5:.0f} Prompt-Token, "
          f"~{len(text) / 3.5 / 1e6 * 0.66 + 12000 / 1e6 * 1.98:.4f} USD je Lauf)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
