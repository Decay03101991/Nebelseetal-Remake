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

# Spieltest-Simulation — 10 Spieltage, ohne Fenster gefahren

**Erzeugt:** 31.10.2026 12:38 von `tools/spieltest_simulation.py` — reine Spiellogik (`src/spielschicht.py`), keine Oberflaeche.
**Spielerpolitik (dokumentiert, nicht optimal):** alle 20 Spielminuten ein Schritt; erst produzierende Gebaeude bauen, dann ausbauen; Forschung wenn bezahlbar; Einheiten ausbilden; ab Spieltag 2 ein Angriff auf Wallstufe 1.

## Tagesbilanzen

| Spieltag | Holz | Stein | Nahrung | Gold | Mana | Krieg | Forschung | Gesamt | Einheiten | Gebaeude |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 90 | 95 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 1 |
| 1 | 30 | 116 | 153 | 123 | 0 | 0 | 1 | **0** | 0 | 12 |
| 2 | 48 | 300 | 354 | 267 | 0 | 0 | 4 | **2** | 0 | 12 |
| 3 | 44 | 356 | 556 | 411 | 0 | 0 | 4 | **2** | 0 | 12 |
| 4 | 60 | 572 | 763 | 555 | 0 | 0 | 18 | **9** | 0 | 12 |
| 5 | 76 | 788 | 974 | 699 | 0 | 0 | 32 | **16** | 0 | 12 |
| 6 | 4 | 788 | 1185 | 843 | 0 | 0 | 32 | **16** | 0 | 12 |
| 7 | 20 | 1004 | 1396 | 987 | 0 | 0 | 32 | **16** | 0 | 12 |
| 8 | 36 | 1220 | 1614 | 1131 | 0 | 0 | 51 | **25** | 0 | 12 |
| 9 | 52 | 1436 | 1835 | 1275 | 0 | 0 | 70 | **35** | 0 | 12 |
| 10 | 68 | 1652 | 2056 | 1419 | 0 | 0 | 89 | **44** | 0 | 12 |

## Gebaut (Spieltag, was)

T0.01 holzfäller, T0.03 holzfäller, T0.04 bibliothek, T0.06 farm, T0.07 farm, T0.08 goldmine, T0.11 steinmetz, T0.14 steinmetz, T0.21 goldmine, T0.32 jaeger, T0.43 ausbau Feld 10, T0.56 jaeger, T0.69 kriegerakademie, T0.86 ausbau Feld 10, T1.08 ausbau Feld 10, T2.06 ausbau Feld 10, T2.36 ausbau Feld 19, T2.81 ausbau Feld 19, T5.25 ausbau Feld 19, T5.99 ausbau Feld 19

## Forschung

T0.04 Felderwirtschaft, T1.32 Kriegskunst, T1.56 Baukunst, T1.78 Verteidigungsanlagen, T3.26 Felderwirtschaft, T3.72 Kriegskunst, T4.19 Baukunst, T4.65 Verteidigungsanlagen, T6.92 Felderwirtschaft, T7.83 Kriegskunst, T8.76 Baukunst, T9.69 Verteidigungsanlagen

## Ausbildung

_keine_

## Kaempfe

_kein Kampf zustande gekommen (keine Kaempfer oder keine Karren)._

## Ende

* Spieltag 10.0
* Punkte: {'forschungspunkte': 89, 'kriegspunkte': 0, 'gesamtpunkte': 44, 'ruf': 0, 'wall_stufe': 0, 'goetterschutz': False, 'lage': 'weiter', 'lage_grund': 'kein Sieg vorgesehen (E5): das Handbuch nennt keine Siegbedingung, jeder Spieler hat seine eigenen Ziele.'}
* Einheiten: {}
* Rohstoffe: {'holz': 68.0, 'stein': 1651.98, 'metall': 0, 'mana': 0, 'nahrung': 2055.99, 'gold': 1419.0, 'wolle': 0, 'leder': 915.79, 'pferde': 0}

## Was ein Pruefer daraus ablesen kann

* **Tempo:** wie viele Spieltage bis zum ersten Gebaeude, zur ersten Forschung, zum ersten Kampf?
* **Engstelle:** welcher Rohstoff bremst (Tabelle oben)? 
* **Stillstand:** gibt es Tage ohne einen einzigen Bau? Warum?
* **Kampf:** Vorrunde bestanden? Beute in brauchbarer Hoehe? Truppenverlust?
* **Punkte:** wachsen sie plausibel (Krieg + Forschung)/2?


(Ende des Verlaufs. Er stammt aus `tools/spieltest_simulation.py`, nicht aus einem menschlichen Spiel.)
