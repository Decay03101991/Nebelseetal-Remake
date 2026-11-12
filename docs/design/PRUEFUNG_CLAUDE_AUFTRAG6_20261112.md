# Prüfung: Claudes Antwort auf Auftrag Nr. 6 (Gebäudehintergrund 1:1)

**Gegenstand:** `Claude_Opus_5.5_Antwort_Auftrag6_Gebaeudehintergrund.md`, Daniels Abo-Lauf im Browser.
**Geprüft:** 12.11.2026, 17:1x, von Hermes (Weltenfresser). **Verfahren:** eigene Rechnung und eigene
Messung an den Bildern und im Fenster, kein Modell.

## 1. Ergebnis in einer Zeile

**Claudes Rechnung stimmt vollständig — und mein Auftrag war an einer Stelle falsch:** die Zeile
„239 px Höhe fehlen (1120 − 881)“ zieht eine **Breite** von einer **Höhe** ab. Er hat recht, das ist
mein Fehler. Sein **Weg 2** (breit schneiden, Höhe ergänzen) ist der richtige.

## 2. Nachgerechnet (alle Werte selbst gerechnet)

| Größe | Claude | gerechnet |
|---|---|---|
| Verlust Weg 1 (1536 → 881) | 42,6 % | **42,64 %** (655 px) |
| Verlust Weg 2 (1536 → 1142) | 25,7 % | **25,65 %** (394 px) |
| Vergrößerung Weg 1 | ×1,296 | **1,2963** |
| Ergänzung Weg 2 | 256 px = 128 + 128 | **256 = 128 + 128** |
| Motivmitte im Ausschnitt | 661 | **(180 + 1142) / 2 = 661,0** |
| grösster x0 | 394 | **1536 − 1142 = 394** |
| zulässige Gebäudebreite | 1094 | **1142 − 48 = 1094** |
| Hintergrundgrenze unter Text | Leuchtdichte 0,1335 | **0,1335** |
| Hintergrundgrenze unter Zeichen | Leuchtdichte 0,0581 | **0,0581** |
| Text #F2E3BF auf Fensterfarbe #17212B | 12,81 | **12,81** |

**Damit ist Weg 2 belegt:** er verliert 17 Prozentpunkte weniger Bild und muss nicht vergrößern —
Kriterium E3 (Schärfe) ist von selbst erfüllt.

## 3. Seine UNBEKANNT — hier gemessen (an den echten Bildern)

**3a. Ist der Grund des Wappenbildes einfarbig?** **JA.** Vier 32 × 32-Eckfelder, Mittelwert und
Streuung je Kanal:

| Ecke | Mittel (R,G,B) | Streuung |
|---|---|---|
| oben links | 192,8 / 188,6 / 183,1 | 0,9 |
| oben rechts | 194,2 / 190,0 / 184,5 | 0,7 |
| unten links | 192,5 / 189,2 / 185,2 | 0,6 / 0,7 / 0,6 |
| unten rechts | 192,8 / 189,5 / 185,4 | 0,8 |

Abweichung der Mittelwerte je Kanal: **1,7 / 1,3 / 2,3** (Grenze 4), grösste Streuung **0,9** (Grenze 3).
**Folge:** das einfache Verfahren reicht, kein Verlaufsmodell nötig. **Achtung:** das Wappenbild ist
**1024 × 1024**, nicht 1536 × 864 — es wird nicht beschnitten, nur freigestellt.

**3b. Liegt ein Horizont in den Randzeilen?** **Nein, in keinem der neun Bilder.** Grösster Sprung
zweier Nachbarzeilen in den oberen und unteren 128 Zeilen:

| Bild | oben | unten | Bild | oben | unten |
|---|---|---|---|---|---|
| menschlich | 3,0 | 5,3 | Bibliothek | 3,3 | 2,5 |
| elfisch | 4,1 | 6,2 | Kriegerakademie | 4,3 | 3,2 |
| zwergisch | 3,0 | 4,5 | Stellmacher | **11,2** | 6,5 |
| gnomisch | 4,7 | 5,5 | | | |
| trollisch | 2,3 | 4,6 | | | |
| ghulisch | 2,8 | 6,1 | | | |

Alle unter seiner Schwelle 12 (der Stellmacher liegt mit 11,2 knapp darunter, dort ist die obere
Kante unruhig). **Folge:** die Spiegelung ist überall erlaubt, die Sonderregel „nur Farbfläche“ wird
nirgends gebraucht.

## 4. Seine Zonen — im Fenster nachgemessen (1460 × 940)

| Grösse | Claude nimmt an | gemessen | Folge |
|---|---|---|---|
| Kopfzeile | 56 px, liegt AUF dem Bild | **122 px** (Leiste 34 + 28 + 21 + 30 + Rahmen) | liegt **über** dem Bild, nicht darauf (Bild beginnt bei y = 128) |
| linke Spalte | 180 px, evtl. über dem Bild | **157 px**, links **neben** dem Bild (x = 0 bis 157) | liegt **nicht** über dem Bild |
| Statuszeile | ≤ 128 px, über dem Bild | **21 px**, eigene Leiste **unter** dem Inhalt | liegt **nicht** über dem Bild |
| sichtbare Inhaltsfläche | 1142 × 1120 | **1037 × 589** (Canvas), scrollbarer Inhalt **1037 × 1881** | das Bild ist breiter als das Fenster und wird beschnitten/gescrollt |

**Wichtig:** keine Bedienelemente liegen über der Bildfläche. Die Zonen-Tabelle aus Teil D ist damit
einfacher als gedacht — die oberen 128 Zeilen müssen NICHT abgedunkelt werden, um Text zu tragen.
Das Abdunkeln bleibt trotzdem sinnvoll (Rand, Übergang), aber es ist keine Kontrastpflicht.

**Offen (nicht geklärt, gehört in den Bau):** woher die **1142 × 1120** kommen. Register 469 hat sie
als Bildmass entschieden; im 1460er Fenster ist die sichtbare Fläche **1037 × 589**. Das Bild wird
also breiter gezeichnet, als das Fenster zeigt. Vor dem Einbau muss klar sein, ob 1142 die
**Bilddatei** meint (dann wird beschnitten) oder die sichtbare Fläche (dann ist die Datei zu breit).

## 5. Was noch fehlt (Daniel)

| # | Was | Warum nur er |
|---|---|---|
| 1 | **Weg 2 bestätigen** (ein Wort) | Claude bittet ausdrücklich darum, weil er die Rechnung im Auftrag anzweifelt |
| 2 | **cx-Liste für die neun Bilder** | die Motivmitte bestimmt man mit dem Auge; Kontaktbogen mit Lineal liegt unter `docs/audits/meshy_cx_bogen_20261112.png` |
| 3 | **Wappengrössen** (klein für die Karte, gross für den Kopf) | Claude empfiehlt nicht unter 32 px; die Karte zeigt heute eine flache Silhouette in 14/16 px |
| 4 | **Schlagschatten am Wappen?** | nur mit dem Auge zu sehen (auf Magenta legen) |

## 6. Empfehlung für den Bau

1. Weg 2, wie von Claude beschrieben (Spiegelband, Unschärfe, Farbfläche, Abdunkeln) — aber die
   Abdunkelung ist **Schmuck**, keine Kontrastpflicht (Abschnitt 4).
2. Wappen: einfarbiger Grund ist belegt, also Claudes Stufen 1 bis 6 unverändert; Zielgrössen nach
   Daniels Antwort.
3. Die cx-Liste ist die einzige echte Sperre — ohne sie wird geraten, und Raten ist hier verboten.
