# Bildcontent (Pixella, 04.11.2026)

Daniel hat am 04.11.2026 um 17:00 Uhr mit einer einmaligen Zahlung von 0,98 EUR Bildcontent
organisiert. Die Lieferung besteht aus **12 Uebersichten** (je 1998x1859 px), in denen mehrere
Einzelbilder nebeneinander liegen - "groesstenteils ungeschnitten", so Daniels eigenes Wort.

## Was hier liegt

- `schnitt/` - **79 Einzelbilder**, aus den Uebersichten geschnitten, in zwoelf Themenordnern
  (`gebaeude_a`, `gebaeude_b`, `burgen`, `ghule`, `gnome`, `menschen`, `panorama_a`, `panorama_b`-
  aehnlich, `zwerge_a/b/c`). Je Ordner ein Panorama (falls vorhanden) und die Kacheln.
- `VERZEICHNIS.json` - Datei, Breite, Hoehe je Einzelbild; Quelle und Ablage der Rohfassungen.

## Wo die Rohfassungen liegen

`archiv/eingaben/20261104_pixella_bildcontent/` (12 Dateien, SHA256 gegen den Desktop geprueft).
`archiv/` ist gitignored - die Rohfassungen sind absichtlich **nicht** im Repo.

## Wie geschnitten wurde (und wo es hakt)

1. Weisse Raender und die gruenen Anfasser des Auswahlwerkzeugs werden erkannt und abgeschnitten.
   Wer sie mitzaehlt, schneidet mitten in die Kacheln (erster Fehlversuch).
2. Zwischen den Kacheln gibt es **keine** weissen Fugen - die goldenen Rahmen beruehren sich.
   Geteilt wird deshalb nach gemessener Geometrie: 4x2, 6x2, oder Panorama plus 4 bzw. 3x2 Kacheln.
3. Wo echte weisse Fugen existieren (drei der Panorama-Dateien), werden sie benutzt.

**Ehrliche Grenze:** von 79 Schnitten sind etwa **10 bis 15 sichtbar unsauber** - meist die
Panoramastreifen, deren Hoehe nicht aus den Daten hervorgeht, und einzelne Kacheln, in denen zwei
Motive liegen. Die Kachelraster mit klarer Geometrie (4x2 und 6x2) sitzen sauber.
Wer eine Kachel braucht, die nicht sitzt: die Rohfassung liegt im Archiv, der Schnitt ist in
`nebel_schnitt3.py` (Scratch) in Minuten nachzuziehen.
