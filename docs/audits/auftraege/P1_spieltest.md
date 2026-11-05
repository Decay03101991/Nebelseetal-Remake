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

# Spieltest-Simulation — 12 Spieltage, ohne Fenster gefahren (Stil krieg)

**Erzeugt:** 05.11.2026 19:58 von `tools/spieltest_simulation.py` — reine Spiellogik (`src/spielschicht.py`), keine Oberflaeche.
**Spielerpolitik (dokumentiert, nicht optimal):** Stil **krieg** — alle 20 Spielminuten ein Schritt; Baukette holzfäller, bibliothek, goldmine, schmiede, naehstube, kriegerakademie, stellmacher, farm, erzmine, schafszucht, steinmetz, jaeger, haus; Forschung wenn bezahlbar; Ausbildungsziele 4 Kämpfer, 2 Bürgerwehr, 1 Handkarren; Angriff ab Spieltag 2, danach alle 1 Spieltage.
**Hinweis zur Saat:** die Startkarte ist FEST (Register 229) - `--saat` wirkt in diesem
Lauf also nicht, solange keine zweite Siedlung gegruendet wird. Unterschiedliche Verlaeufe
entstehen ueber `--stil` (breit/krieg) und `--tage`.

## Tagesbilanzen

| Spieltag | Holz | Stein | Nahrung | Gold | Mana | Krieg | Forschung | Gesamt | Einheiten | Gebaeude |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 90 | 95 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 1 |
| 1 | 6 | 63 | 94 | 123 | 0 | 0 | 1 | **0** | 0 | 20 |
| 2 | 60 | 135 | 86 | 267 | 0 | 2 | 2 | **2** | 2 | 22 |
| 3 | 84 | 155 | 278 | 411 | 0 | 2 | 2 | **2** | 2 | 24 |
| 4 | 20 | 239 | 481 | 555 | 0 | 3 | 9 | **6** | 3 | 24 |
| 5 | 92 | 275 | 683 | 699 | 0 | 3 | 9 | **6** | 3 | 24 |
| 6 | 99 | 283 | 885 | 843 | 0 | 3 | 9 | **6** | 3 | 24 |
| 7 | 107 | 291 | 1087 | 987 | 0 | 3 | 9 | **6** | 3 | 24 |
| 8 | 85 | 519 | 1289 | 1131 | 0 | 3 | 31 | **17** | 3 | 24 |
| 9 | 113 | 747 | 1501 | 575 | 0 | 11 | 47 | **29** | 7 | 24 |
| 10 | 40 | 975 | 1722 | 719 | 0 | 11 | 63 | **37** | 7 | 24 |
| 11 | 128 | 1053 | 1943 | 863 | 0 | 11 | 70 | **40** | 7 | 24 |
| 12 | 216 | 1131 | 2164 | 1007 | 0 | 11 | 70 | **40** | 7 | 24 |

## Gebaut (Spieltag, was)

T0.01 holzfäller, T0.03 holzfäller, T0.04 bibliothek, T0.06 goldmine, T0.07 farm, T0.08 farm, T0.11 steinmetz, T0.14 steinmetz, T0.18 Holzfäller (Engpass holz), T0.24 goldmine, T0.29 erzmine, T0.33 erzmine, T0.39 schafszucht, T0.44 schafszucht, T0.51 schmiede, T0.6 schmiede, T0.67 naehstube, T0.75 naehstube, T0.82 ausbau Feld 10, T0.9 jaeger, T0.99 jaeger, T1.08 kriegerakademie, T1.19 stellmacher, T1.31 ausbau Feld 10, T1.46 ausbau Feld 10, T1.82 ausbau Feld 10, T2.01 ausbau Feld 7, T2.22 ausbau Feld 28, T2.49 haus, T2.74 haus, T3.04 ausbau Feld 7, T3.35 ausbau Feld 28, T4.35 ausbau Feld 7, T4.76 ausbau Feld 28, T5.22 ausbau Feld 7, T5.74 ausbau Feld 8, T6.21 ausbau Feld 9, T6.71 ausbau Feld 28, T10.65 ausbau Feld 8, T11.36 ausbau Feld 9

## Forschung

T0.04 Schmiedekunst, T1.62 Waffentechnik, T3.68 Waffentechnik, T7.31 Waffentechnik, T7.68 Nähen, T7.72 Nähkunst, T7.79 Rüstungsbau, T8.06 Rüstungsbau, T8.22 Felderwirtschaft, T8.54 Felderwirtschaft, T8.71 Kriegskunst, T9.01 Kriegskunst, T9.18 Baukunst, T9.44 Baukunst, T9.61 Verteidigungsanlagen, T9.93 Verteidigungsanlagen

## Ausbildung

T1.47 Bürgerwehr, T2.0 Bürgerwehr, T4.0 Handkarren, T8.28 Kämpfer, T8.4 Kämpfer, T8.53 Kämpfer, T8.65 Kämpfer

## Kaempfe

* Tag 2.0: Truppen {'Bürgerwehr': 2} -> Ausgang **angreifer**, Vorrunde bestanden: True, Beute {}
* Tag 3.0: Truppen {'Bürgerwehr': 2} -> Ausgang **angreifer**, Vorrunde bestanden: True, Beute {}
* Tag 4.0: Truppen {'Bürgerwehr': 2, 'Handkarren': 1} -> Ausgang **angreifer**, Vorrunde bestanden: True, Beute {'holz': 16, 'nahrung': 10, 'stein': 12}
* Tag 5.0: Truppen {'Bürgerwehr': 2, 'Handkarren': 1} -> Ausgang **angreifer**, Vorrunde bestanden: True, Beute {'holz': 16, 'nahrung': 10, 'stein': 12}
* Tag 6.0: Truppen {'Bürgerwehr': 2, 'Handkarren': 1} -> Ausgang **angreifer**, Vorrunde bestanden: True, Beute {'holz': 16, 'nahrung': 10, 'stein': 12}
* Tag 7.0: Truppen {'Bürgerwehr': 2, 'Handkarren': 1} -> Ausgang **angreifer**, Vorrunde bestanden: True, Beute {'holz': 16, 'nahrung': 10, 'stein': 12}
* Tag 8.0: Truppen {'Bürgerwehr': 2, 'Handkarren': 1} -> Ausgang **angreifer**, Vorrunde bestanden: True, Beute {'holz': 16, 'nahrung': 10, 'stein': 12}
* Tag 9.0: Truppen {'Bürgerwehr': 2, 'Kämpfer': 4, 'Handkarren': 1} -> Ausgang **angreifer**, Vorrunde bestanden: True, Beute {'holz': 16, 'nahrung': 10, 'stein': 12}
* Tag 10.0: Truppen {'Bürgerwehr': 2, 'Kämpfer': 4, 'Handkarren': 1} -> Ausgang **angreifer**, Vorrunde bestanden: True, Beute {'holz': 16, 'nahrung': 10, 'stein': 12}
* Tag 11.0: Truppen {'Bürgerwehr': 2, 'Kämpfer': 4, 'Handkarren': 1} -> Ausgang **angreifer**, Vorrunde bestanden: True, Beute {'holz': 16, 'nahrung': 10, 'stein': 12}
* Tag 12.0: Truppen {'Bürgerwehr': 2, 'Kämpfer': 4, 'Handkarren': 1} -> Ausgang **angreifer**, Vorrunde bestanden: True, Beute {'holz': 16, 'nahrung': 10, 'stein': 12}

## Ende

* Spieltag 12.0
* Punkte: {'forschungspunkte': 70, 'kriegspunkte': 11, 'gesamtpunkte': 40, 'ruf': 0, 'wall_stufe': 0, 'goetterschutz': False, 'lage': 'weiter', 'lage_grund': 'kein Sieg vorgesehen (E5): das Handbuch nennt keine Siegbedingung, jeder Spieler hat seine eigenen Ziele.'}
* Einheiten: {'Bürgerwehr': 2, 'Handkarren': 1, 'Kämpfer': 4}
* Rohstoffe: {'holz': 215.83, 'stein': 1130.98, 'metall': 1652.0, 'mana': 0, 'nahrung': 2164.23, 'gold': 1007.0, 'wolle': 719.0, 'leder': 927.71, 'pferde': 0}

## Uebersprungene Schritte (der Lauf wurde NICHT abgebrochen)

_keine - jeder Schritt liess sich ausfuehren._

## Fehlversuche mit Grund (Grundbilanz)

Was die Spielerpolitik versucht hat und WARUM es nicht ging - gleiche Gruende werden gezaehlt. Ohne diesen Abschnitt sieht ein Lauf mit 0 Einheiten wie ein Spielfehler aus, obwohl nur eine Ware oder eine Werkstatt fehlte.

| Stelle | Anzahl | Grund |
|---|---|---|
| ausbauen | 723 | Bibliothek hat die höchste belegte Stufe 5 erreicht. |
| bauen | 667 | alle Gebaeude der Kette stehen (je 2) oder sind gesperrt |
| ausbildung | 491 | Kämpfer: Im Lager fehlen für Kämpfer: Kurzschwert, Lederrüstung. |
| ausbauen | 488 | Stellmacher hat die höchste belegte Stufe 5 erreicht. |
| ausbauen | 379 | Kriegerakademie hat die höchste belegte Stufe 5 erreicht. |
| ware | 276 | Kurzschwert: Warenvoraussetzung fehlt: Waffentechnik Stufe 3 nötig, vorhanden ist Stufe 2 |
| ware | 157 | Kurzschwert: Warenvoraussetzung fehlt: Waffentechnik Stufe 3 nötig, vorhanden ist Stufe 1 |
| ausbildung | 85 | Handkarren: Handkarren braucht Stellmacher -- nicht gebaut. |
| ware | 83 | Kurzschwert: Warenvoraussetzung fehlt: Waffentechnik Stufe 3 nötig, vorhanden ist Stufe 0 |
| ausbildung | 77 | Kämpfer: Kämpfer braucht Kriegerakademie -- nicht gebaut. |
| ausbildung | 77 | Bürgerwehr: Bürgerwehr braucht Kriegerakademie -- nicht gebaut. |
| ausbildung | 51 | Kämpfer: Im Lager fehlen für Kämpfer: Lederrüstung. |
| forschung | 39 | Waffentechnik: In dieser Siedlung forscht bereits Waffentechnik — erst nach dessen Abschluss ist eine weitere Forschung möglich (Handbuch S. 12). |
| ware | 36 | Kurzschwert: Keine Schmiede in dieser Siedlung -- erst bauen. |

## Was ein Pruefer daraus ablesen kann

* **Tempo:** wie viele Spieltage bis zum ersten Gebaeude, zur ersten Forschung, zum ersten Kampf?
* **Engstelle:** welcher Rohstoff bremst (Tabelle oben)? 
* **Stillstand:** gibt es Tage ohne einen einzigen Bau? Warum?
* **Kampf:** Vorrunde bestanden? Beute in brauchbarer Hoehe? Truppenverlust?
* **Punkte:** wachsen sie plausibel (Krieg + Forschung)/2?


(Ende des Verlaufs. Er stammt aus `tools/spieltest_simulation.py`, nicht aus einem menschlichen Spiel.)
