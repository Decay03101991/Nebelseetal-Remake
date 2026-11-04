# Bildcontent (Pixella, Daniel, 04.11.2026)

Daniel hat am 04.11.2026 um 17:00 Uhr mit einer **einmaligen Zahlung von 0,98 EUR** Bildcontent
organisiert. Es sind **12 Uebersichten** zu je 1998x1859 px. In jeder Uebersicht liegen **mehrere
Einzelbilder** nebeneinander, jeweils mit einem goldenen Rahmen - "groesstenteils ungeschnitten", so
Daniels eigenes Wort.

## Was hier liegt

`uebersichten/` - die **12 Originaldateien, unveraendert**. Kein Schnitt, keine Skalierung, kein
Umbenennen. SHA256 je Datei in `VERZEICHNIS.json`; alle 12 sind hashgleich mit den Rohfassungen im
Archiv und mit der Lieferung auf dem Desktop.

| Datei | Thema (von Daniel benannt) | Inhalt |
|---|---|---|
| `Bildcontent.png` | Gebaeude, Reihe A | 8 Gebaeudebilder (4x2) |
| `Bildcontent2.png` | Gebaeude, Reihe B | 8 Gebaeudebilder (4x2) |
| `Burgbilder_Hintergründe.png` | Burgen | 12 Burg- und Landschaftsbilder (6x2) |
| `Ghule_fraktion1.png` | Ghule | 1 Panorama + 4 Kacheln |
| `Gnome_fraktion.png` | Gnome | 1 Panorama + Kacheln |
| `menschlich_fraktion.png` | Menschen | 1 Panorama + 4 Kacheln |
| `Zwerge_fraktion1/2/3.png` | Zwerge | je 1 Panorama + 4 Kacheln |
| `Panorama und Stilbilder für Nebelseetal.png` | Panoramen | 1 Panorama + 6 Kacheln (3x2) |
| `Panorama und Stilbilder für Nebelseetal2.png` | Panoramen | 1 Panorama + 6 Kacheln (3x2) |
| `Panorama und Stilbilder BURG für Nebelseetal3.png` | Burgen-Panorama | 1 Panorama + 6 Kacheln (3x2) |

## Warum hier NICHT geschnitten ist (Lehre vom 04.11.2026)

Ein automatischer Schnitt wurde zweimal versucht und von Daniel **verworfen**: die Kacheln enthielten
Teile des Nachbarbildes oder waren mitten im Motiv angeschnitten. Drei Messungen dazu, die weiter gelten:

1. **Zwischen den Kacheln gibt es keine weissen Fugen.** Die goldenen Rahmen beruehren sich; weisse
   Stellen gibt es nur an den abgerundeten Ecken. Eine Fugen-Suche findet deshalb nichts.
2. **Die gruenen Anfasser des Auswahlwerkzeugs** (Pixella-Screenshot) liegen ausserhalb der Bilder und
   ziehen jede Bounding-Box nach unten - wer sie mitzaehlt, schneidet einen weissen Streifen mit.
3. **Die Hoehe eines Panoramas** ist aus den Bilddaten nicht ableitbar; geschaetzte Werte lagen
   daneben, gemessene weisse Zeilen trafen nur zufaellig.

**Folge:** die Blaetter werden als Ganzes genutzt (Titelseite, Kapitelauftakt, Bildtafel). Wer einzelne
Kacheln braucht, schneidet sie **von Hand** - oder liefert die Einzelbilder direkt aus dem Generator.

## Wo die Rohfassungen liegen

`archiv/eingaben/20261104_pixella_bildcontent/` - dieselben 12 Dateien, gitignored. Die Fassung hier
ist die Projektkopie, damit das Repo die Bilder traegt.
