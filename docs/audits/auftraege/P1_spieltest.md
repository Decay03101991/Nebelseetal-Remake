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

# Spieltest-Simulation — 10 Spieltage, ohne Fenster gefahren (Stil krieg)

**Erzeugt:** 05.11.2026 19:02 von `tools/spieltest_simulation.py` — reine Spiellogik (`src/spielschicht.py`), keine Oberflaeche.
**Spielerpolitik (dokumentiert, nicht optimal):** Stil **krieg** — alle 20 Spielminuten ein Schritt; Baukette holzfäller, bibliothek, goldmine, schmiede, naehstube, kriegerakademie, stellmacher, farm, erzmine, schafszucht, steinmetz, jaeger, haus; Forschung wenn bezahlbar; Ausbildungsziele 4 Kämpfer, 2 Bürgerwehr, 1 Handkarren; Angriff ab Spieltag 2, danach alle 1 Spieltage.

## Tagesbilanzen

| Spieltag | Holz | Stein | Nahrung | Gold | Mana | Krieg | Forschung | Gesamt | Einheiten | Gebaeude |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 90 | 95 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 1 |
| 1 | 6 | 63 | 103 | 123 | 0 | 0 | 1 | **0** | 0 | 20 |
| 2 | 20 | 175 | 105 | 92 | 0 | 4 | 4 | **4** | 3 | 22 |
| 3 | 64 | 205 | 306 | 61 | 0 | 6 | 4 | **5** | 4 | 23 |
| 4 | 4 | 227 | 508 | 30 | 0 | 8 | 4 | **6** | 5 | 24 |
| 5 | 16 | 443 | 717 | 174 | 0 | 8 | 25 | **16** | 5 | 24 |
| 6 | 115 | 575 | 938 | 143 | 0 | 11 | 32 | **21** | 7 | 24 |
| 7 | 155 | 587 | 1159 | 287 | 0 | 11 | 32 | **21** | 7 | 24 |
| 8 | 3 | 495 | 1380 | 431 | 0 | 11 | 32 | **21** | 7 | 24 |
| 9 | 131 | 723 | 1601 | 575 | 0 | 11 | 51 | **31** | 7 | 24 |
| 10 | 58 | 951 | 1832 | 719 | 0 | 11 | 70 | **40** | 7 | 24 |

## Gebaut (Spieltag, was)

T0.01 holzfäller, T0.03 holzfäller, T0.04 bibliothek, T0.06 goldmine, T0.07 farm, T0.08 farm, T0.11 steinmetz, T0.14 steinmetz, T0.18 Holzfäller (Engpass holz), T0.24 goldmine, T0.29 erzmine, T0.33 erzmine, T0.39 schafszucht, T0.44 schafszucht, T0.51 schmiede, T0.6 schmiede, T0.67 naehstube, T0.75 naehstube, T0.82 ausbau Feld 10, T0.9 jaeger, T0.99 jaeger, T1.08 kriegerakademie, T1.19 stellmacher, T1.31 ausbau Feld 10, T1.46 ausbau Feld 10, T2.14 ausbau Feld 10, T2.33 ausbau Feld 7, T2.54 ausbau Feld 28, T2.81 haus, T3.06 haus, T3.36 ausbau Feld 7, T3.68 ausbau Feld 28, T5.64 ausbau Feld 7, T6.04 ausbau Feld 28, T6.51 ausbau Feld 7, T7.03 ausbau Feld 8, T7.49 ausbau Feld 9, T8.0 ausbau Feld 28

## Forschung

T0.04 Felderwirtschaft, T1.62 Kriegskunst, T1.78 Baukunst, T1.94 Verteidigungsanlagen, T4.0 Felderwirtschaft, T4.32 Kriegskunst, T4.64 Baukunst, T4.96 Verteidigungsanlagen, T8.58 Felderwirtschaft, T9.24 Kriegskunst, T9.82 Baukunst

## Ausbildung

T1.36 Kämpfer, T1.47 Bürgerwehr, T2.0 Bürgerwehr, T2.58 Kämpfer, T3.79 Kämpfer, T5.01 Kämpfer, T5.28 Handkarren

## Kaempfe

* Tag 5.28: Truppen {'Kämpfer': 4, 'Bürgerwehr': 2, 'Handkarren': 1} -> Ausgang **angreifer**, Vorrunde bestanden: True, Beute {'holz': 16, 'nahrung': 10, 'stein': 12}
* Tag 6.28: Truppen {'Kämpfer': 4, 'Bürgerwehr': 2, 'Handkarren': 1} -> Ausgang **angreifer**, Vorrunde bestanden: True, Beute {'holz': 16, 'nahrung': 10, 'stein': 12}
* Tag 7.28: Truppen {'Kämpfer': 4, 'Bürgerwehr': 2, 'Handkarren': 1} -> Ausgang **angreifer**, Vorrunde bestanden: True, Beute {'holz': 16, 'nahrung': 10, 'stein': 12}
* Tag 8.28: Truppen {'Kämpfer': 4, 'Bürgerwehr': 2, 'Handkarren': 1} -> Ausgang **angreifer**, Vorrunde bestanden: True, Beute {'holz': 16, 'nahrung': 10, 'stein': 12}
* Tag 9.28: Truppen {'Kämpfer': 4, 'Bürgerwehr': 2, 'Handkarren': 1} -> Ausgang **angreifer**, Vorrunde bestanden: True, Beute {'holz': 16, 'nahrung': 10, 'stein': 12}

## Ende

* Spieltag 10.0
* Punkte: {'forschungspunkte': 70, 'kriegspunkte': 11, 'gesamtpunkte': 40, 'ruf': 0, 'wall_stufe': 0, 'goetterschutz': False, 'lage': 'weiter', 'lage_grund': 'kein Sieg vorgesehen (E5): das Handbuch nennt keine Siegbedingung, jeder Spieler hat seine eigenen Ziele.'}
* Einheiten: {'Kämpfer': 4, 'Bürgerwehr': 2, 'Handkarren': 1}
* Rohstoffe: {'holz': 58.31, 'stein': 950.98, 'metall': 1380.0, 'mana': 0, 'nahrung': 1832.48, 'gold': 719.0, 'wolle': 575.0, 'leder': 752.19, 'pferde': 0}

## Uebersprungene Schritte (der Lauf wurde NICHT abgebrochen)

_keine - jeder Schritt liess sich ausfuehren._

## Fehlversuche mit Grund (Grundbilanz)

Was die Spielerpolitik versucht hat und WARUM es nicht ging - gleiche Gruende werden gezaehlt. Ohne diesen Abschnitt sieht ein Lauf mit 0 Einheiten wie ein Spielfehler aus, obwohl nur eine Ware oder eine Werkstatt fehlte.

| Stelle | Anzahl | Grund |
|---|---|---|
| ausbauen | 558 | Bibliothek hat die höchste belegte Stufe 5 erreicht. |
| bauen | 500 | alle Gebaeude der Kette stehen (je 2) oder sind gesperrt |
| ausbauen | 251 | Stellmacher hat die höchste belegte Stufe 5 erreicht. |
| ausbauen | 144 | Kriegerakademie hat die höchste belegte Stufe 5 erreicht. |
| angriff | 88 | keine Kaempfer (5) / keine Karren (0) |
| angriff | 87 | keine Kaempfer (4) / keine Karren (0) |
| ausbildung | 85 | Handkarren: Handkarren braucht Stellmacher -- nicht gebaut. |
| ausbildung | 77 | Kämpfer: Kämpfer braucht Kriegerakademie -- nicht gebaut. |
| ausbildung | 77 | Bürgerwehr: Bürgerwehr braucht Kriegerakademie -- nicht gebaut. |
| angriff | 42 | keine Kaempfer (3) / keine Karren (0) |
| ware | 36 | Kurzschwert: Keine Schmiede in dieser Siedlung -- erst bauen. |
| angriff | 19 | keine Kaempfer (6) / keine Karren (0) |
| ausbildung | 12 | Kämpfer: Im Lager fehlen für Kämpfer: Lederrüstung. |
| ausbildung | 12 | Kämpfer: Im Lager fehlen für Kämpfer: Kurzschwert, Lederrüstung. |

## Was ein Pruefer daraus ablesen kann

* **Tempo:** wie viele Spieltage bis zum ersten Gebaeude, zur ersten Forschung, zum ersten Kampf?
* **Engstelle:** welcher Rohstoff bremst (Tabelle oben)? 
* **Stillstand:** gibt es Tage ohne einen einzigen Bau? Warum?
* **Kampf:** Vorrunde bestanden? Beute in brauchbarer Hoehe? Truppenverlust?
* **Punkte:** wachsen sie plausibel (Krieg + Forschung)/2?


(Ende des Verlaufs. Er stammt aus `tools/spieltest_simulation.py`, nicht aus einem menschlichen Spiel.)
