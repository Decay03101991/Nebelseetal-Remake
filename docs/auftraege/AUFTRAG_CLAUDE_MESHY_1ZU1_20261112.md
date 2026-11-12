# AUFTRAG NR. 6 AN CLAUDE (Klasse Opus 5.5): DER GEBAEUDEHINTERGRUND 1:1

| | |
|---|---|
| **Auftrag von** | Hermes Agent „Weltenfresser“, Projekt Nebelseetal Remake, Stand 12.11.2026, 15:1x |
| **Fuer** | Daniel Koessl |
| **Ort im Spiel** | Gebaeudeansicht (die Flaeche, auf der die Gebaeude stehen) |
| **Vorgaenger** | Antwort auf Auftrag Nr. 5 (T08 Ressourcenleiste) — gebaut, Register 488 |
| **Umsetzendes Modell** | `deepseek-v4-flash` (schnelles, kleines Modell) — der Auftrag muss dafuer umsetzbar sein |
| **Sprache der Antwort** | Deutsch, knapp, mit Zahlen |

> **BERICHTIGUNG 12.11.2026, 17:1x (nach Claudes Antwort):** der Satz „Es fehlen 239 px Hoehe
> (1120 - 881)“ in Abschnitt 1 ist **falsch** - er zieht eine Breite von einer Hoehe ab. Richtig ist
> **Weg 2**: auf **1142 px Breite** beschneiden (Verlust **25,65 Prozent**) und **256 px Hoehe**
> ergaenzen (128 oben, 128 unten), ohne Vergroesserung. Weg 1 (881 px breit, dann Faktor 1,296) war
> die schlechtere der beiden Varianten. Nachgerechnet in `docs/design/PRUEFUNG_CLAUDE_AUFTRAG6_20261112.md`.

## 1. Die Lage (alles gemessen, nicht geschaetzt)

Das Spiel zeigt die Gebaeude auf einer **gezeichneten Flaeche von 1142 x 1120 px (1:1)** — im
laufenden Fenster gemessen. Daniel hat am 12.11.2026 entschieden, dass jedes Gebaeude-Bild genau in
dieser Groesse gemalt bzw. angepasst wird (Register 469).

Meshy hat geliefert (Register 484, `docs/eingaenge/MESHY_20261112_BILDASSETS/`):

| Satz | Dateien | Masse |
|---|---|---|
| Voelker-Panoramen | 6 (menschlich, elfisch, zwergisch, gnomisch, trollisch, ghulisch) | **1536 x 864 (16:9)** |
| Elfen-Gebaeude | Bibliothek, Kriegerakademie, Stellmacher | **1536 x 864 (16:9)** |
| Elfen-Wappen und Banner | ein Satz aus Schild und Banner auf **einfarbig grauem Grund** | 1536 x 864, **nicht freigestellt** |

**Daniels Entscheidung vom 12.11.2026:** es wird **kein neuer Mal-Lauf** gemacht. Die vorhandenen
16:9-Bilder werden **mittig beschnitten** und **oben/unten ergaenzt**, bis sie 1142 x 1120 ergeben.

Der Weg kostet rund **45 Prozent der Bildbreite** (1536 -> 881 px bei gleicher Hoehe) und braucht
danach eine Vergroesserung um Faktor **1,30** auf 1142 px. Die Ergaenzung ist also keine Kleinigkeit:
sie ist der Teil, den man spaeter sieht.

## 2. Was ich von dir will

### A) Wo wird geschnitten?

Ein 16:9-Bild hat links und rechts Rand, der beim Beschnitt verloren geht. Sag mir **fuer jeden der
drei Bildtypen** (Panorama, Gebaeude, Wappen-Satz), **was in der Mitte stehen muss** und was weg
darf: Horizonte, Himmel, Boden, Gebaeudemitte, Figuren. Wenn du es an einer Regel festmachen kannst
(z. B. „die senkrechte Bildachse durch die Hauptmasse des Gebaeudes“), schreib die Regel — nicht nur
ein Beispiel.

### B) Wie wird ergaenzt, ohne dass es billig aussieht?

Nach dem Beschnitt fehlen **239 px Hoehe** (1120 - 881). Nenne **ein** Verfahren und seine Grenzen:

- Fortsetzung der Randspalten (Spiegelung? gestreckte Kante? Farbverlauf?),
- wie verhindert wird, dass die Spiegelachse als Linie sichtbar wird,
- was mit einem Horizont passiert, der genau auf der Ergaenzung liegt,
- ob eine Vignette oder ein dunkler Verlauf oben/unten die Naht kaschiert — und ob das den Kontrast
  der Bedienelemente darueber gefaehrdet.

**Messbare Kriterien**, die ich pruefen kann: Unterschied der Randspalten in Farbwerten, Helligkeit
der Ergaenzungszone gegen das Original, senkrechte Kanten (Kantendetektion), Schärfe (Varianz des
Laplace-Filters) vor und nach der Vergroesserung.

### C) Das Wappen freistellen

Das Elfen-Wappen ist ein **Satz aus Schild und Banner auf einfarbig grauem Grund**. Ich brauche es
freigestellt in **zwei Groessen** (wie sie im Spiel vorkommen): klein fuer die Karte, gross fuer den
Kopf. Sag mir:

- welches Verfahren (Farbabstand zum Grau? Kantenglaettung? Alpha-Kante?),
- wie die **Halbtransparenz** an den Kanten behandelt wird, damit kein grauer Saum bleibt,
- wie ich pruefe, dass nichts fehlt (Umriss-Laenge? Deckungsgrad in Prozent?),
- ob der Grund wirklich einfarbig ist oder ein Verlauf — und was dann anders wird.

### D) Wo darf das Motiv liegen?

Ueber der Flaeche liegen Bedienelemente: eine Kopfzeile oben (34 px hoch plus zwei Textzeilen),
links eine Spalte mit Ebenen und Punkten (rund 180 px breit), unten eine Statuszeile. Damit die
Gebaeude nicht unter der Kopfzeile verschwinden: **welche Zonen der 1142 x 1120 px bleiben ruhig**
(kein wichtiges Motiv), und welche Zone traegt die Hauptsache?

### E) Abnahme (das will ich messen)

| # | Kriterium | Wie ich es pruefe |
|---|---|---|
| 1 | Ergebnis ist exakt 1142 x 1120 | Bildmass |
| 2 | Keine sichtbare senkrechte Naht in der Ergaenzung | Kantendetektion, Spaltenvergleich |
| 3 | Schaerfe nicht schlechter als 10 Prozent gegen das Original | Laplace-Varianz |
| 4 | Bedienelemente bleiben lesbar (Text 4,5 : 1, Zeichen 3 : 1) | WCAG gegen die hellsten Pixel darunter |
| 5 | Wappen ohne grauen Saum | Alpha-Kante geprueft, Deckungsgrad genannt |

## 3. Die Regeln fuer deine Antwort

1. **Kein Code, keine Dateien, kein Patch.** Du lieferst einen Text, ich baue.
2. **`data/` bleibt unberuehrt** — keine neuen Datenschluessel vorschlagen, die es nicht gibt.
3. **Keine Mechanik-Zahlen** (Kosten, Ertrate, Kampfwerte). Es geht nur um Bilder.
4. **Keine fremden Bilder** vorschlagen; benutzt wird, was in `docs/eingaenge/MESHY_20261112_BILDASSETS/`
   liegt.
5. **Keine geratenen Masse.** Was du nicht kennst, schreibst du als **UNBEKANNT** hin — ich messe es
   nach und antworte.
6. **Umsetzbar fuer `deepseek-v4-flash`:** jeder Schritt in EINEM Arbeitsgang, ohne Auslegung, ohne
   Zusatzwerkzeuge (nur Pillow, das im Projekt schon benutzt wird).
7. **Knapp.** Kein Handbuch, keine Wiederholung des Auftrags. Hoechstens eine Seite je Teil A bis E.

## 4. Was ich schon weiss (damit du es nicht fragen musst)

| Frage | Antwort |
|---|---|
| Wie gross ist die Flaeche wirklich? | **1142 x 1120 px**, im Fenster gemessen |
| Wie gross sind die Bilder? | **1536 x 864 px** (16:9), alle neun Gebaeude/Panoramen |
| Wird neu gemalt? | **Nein** — Daniel hat Beschnitt plus Ergaenzung entschieden |
| Gibt es schon ein Band/Bild in der Oberflaeche? | Nur die Ressourcenleiste (gebaut, ohne Bilddatei) |
| Welche Farbe hat der Grund der Oberflaeche? | Skin `#1a0a09` fuer Baender, Fenster `#17212B` fuer Flaechen |
| Wie hoch ist die Kopfzeile? | 34 px Leiste plus zwei Textzeilen (rund 56 px zusammen) |
| Wo steht das Spiel? | `main` = `238e8aa`, 224 von 224 Pruefungen gruen |

## 5. Abgabe

Eine Antwort als Text, gegliedert **A bis E**, jede Antwort mit Zahlen oder mit **UNBEKANNT**.
Am Ende ein Absatz „Was ich nicht geprueft habe“ — wie in deinen letzten beiden Antworten, das war
sehr nuetzlich.
