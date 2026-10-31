ROLLE
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

==============================================================================
SPIELVERLAUF (Simulation, ohne Oberflaeche)
==============================================================================

# Spieltest-Simulation — 8 Spieltage, ohne Fenster gefahren

**Erzeugt:** 31.10.2026 11:32 von `tools/spieltest_simulation.py` — reine Spiellogik (`src/spielschicht.py`), keine Oberflaeche.
**Spielerpolitik (dokumentiert, nicht optimal):** alle 20 Spielminuten ein Schritt; erst produzierende Gebaeude bauen, dann ausbauen; Forschung wenn bezahlbar; Einheiten ausbilden; ab Spieltag 2 ein Angriff auf Wallstufe 1.

## Tagesbilanzen

| Spieltag | Holz | Stein | Nahrung | Gold | Mana | Krieg | Forschung | Gesamt | Einheiten | Gebaeude |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 90 | 95 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 1 |
| 1 | 242 | 64 | 91 | 0 | 0 | 0 | 0 | **0** | 0 | 4 |
| 2 | 458 | 88 | 187 | 0 | 0 | 0 | 0 | **0** | 0 | 4 |
| 3 | 674 | 111 | 283 | 0 | 0 | 0 | 0 | **0** | 0 | 4 |
| 4 | 890 | 135 | 378 | 0 | 0 | 0 | 0 | **0** | 0 | 4 |
| 5 | 1106 | 159 | 474 | 0 | 0 | 0 | 0 | **0** | 0 | 4 |
| 6 | 1322 | 183 | 570 | 0 | 0 | 0 | 0 | **0** | 0 | 4 |
| 7 | 1538 | 206 | 666 | 0 | 0 | 0 | 0 | **0** | 0 | 4 |
| 8 | 1754 | 230 | 761 | 0 | 0 | 0 | 0 | **0** | 0 | 4 |

## Gebaut (Spieltag, was)

T0.01 holzfäller, T0.03 holzfäller, T0.04 jaeger, T0.06 jaeger

## Forschung

_keine gestartet_

## Ausbildung

_keine_

## Kaempfe

_kein Kampf zustande gekommen (keine Kaempfer oder keine Karren)._

## Ende

* Spieltag 8.0
* Punkte: {'forschungspunkte': 0, 'kriegspunkte': 0, 'gesamtpunkte': 0, 'ruf': 0, 'wall_stufe': 0, 'goetterschutz': False, 'lage': 'weiter', 'lage_grund': 'kein Sieg vorgesehen (E5): das Handbuch nennt keine Siegbedingung, jeder Spieler hat seine eigenen Ziele.'}
* Einheiten: {}
* Rohstoffe: {'holz': 1754.0, 'stein': 230.08, 'metall': 0, 'mana': 0, 'nahrung': 761.43, 'gold': 0, 'wolle': 0, 'leder': 761.43, 'pferde': 0}

## Was ein Pruefer daraus ablesen kann

* **Tempo:** wie viele Spieltage bis zum ersten Gebaeude, zur ersten Forschung, zum ersten Kampf?
* **Engstelle:** welcher Rohstoff bremst (Tabelle oben)? 
* **Stillstand:** gibt es Tage ohne einen einzigen Bau? Warum?
* **Kampf:** Vorrunde bestanden? Beute in brauchbarer Hoehe? Truppenverlust?
* **Punkte:** wachsen sie plausibel (Krieg + Forschung)/2?


(Ende des Verlaufs. Er stammt aus `tools/spieltest_simulation.py`, nicht aus einem menschlichen Spiel.)
