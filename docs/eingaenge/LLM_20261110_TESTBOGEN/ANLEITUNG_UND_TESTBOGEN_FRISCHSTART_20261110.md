# ANLEITUNG und TESTBOGEN — Frischstart (Nebelseetal Remake V 0.0.3)

**Für dich, Daniel.** Zwei Dinge liegen auf dem Desktop: diese Anleitung und die EXE. Sonst nichts.
Diese Datei ist beides — die Anleitung **und** der Bogen, den du beim Spielen ausfüllst.

**Diese EXE wird geprüft:** `Nebelseetal_Pre_Release_V_0.0.3.exe`, **83.342.035 Byte**,
SHA256 `4124b335065366fbcf8e1696edf3c3f1fa8045090b7a7791641b9e0214c67df8`
(Stand 10.11.2026, 21:48 — gebaut nach G2 und G3, Register 384 und 385; Sammellauf 218/218 grün).
**Die alte Fassung von heute Nacht** (SHA256 `a7035101…`) liegt unverändert in
`D:\Arbeiten\Nebelseetal_Remake\archiv\builds\20261110_vor_g2_g3\`, falls du vergleichen willst.

**Was heute neu ist gegenüber deinem letzten Test:**
1. **Du fängst komplett bei null an.** Deine drei alten Spielstände sind gesichert und weggeräumt
   (`C:\Users\saras\.nebelseetal\archiv\vor_frischstart_20261110_2117\`) — das Spiel legt einen neuen an.
   Das Passworttor bleibt wie es war, dein Passwort gilt weiter.
2. **Götterschutz:** Anzeige und Mechanik rechnen jetzt dieselbe Regel (7 Tage **oder** erster
   Kriegspunkt).
3. **Drosselung:** eine gedrosselte Reise dauert jetzt länger (nicht nur billiger). **Aber:** es gibt
   noch **kein Bedienelement** dafür — bitte nicht als Fehler notieren, das ist bekannt und gebaut,
   sobald du sagst, wo der Regler sitzen soll.

**So füllst du aus:** schreibe deine Antwort hinter die Zeile, zwischen die beiden senkrechten
Striche. Eine Zahl, ein ja/nein, oder ein kurzer Satz. Kannst du etwas nicht beurteilen: **weiss
nicht** — das ist ein gültiges Ergebnis. Bei Fehlern bitte den Text **wörtlich** in Block F.
Am Ende speichern, das genügt.

**Bilder (freiwillig):** `Win + Shift + S`, dann in `C:\Users\saras\Desktop\` einfügen und den
Dateinamen mit der Punktnummer beginnen (`C01_goldrahmen.png`). Kein Pflichtteil.

---

## 0. Dein Gerät (ohne das kann ich Layout-Befunde nicht deuten)

| Nr | Frage | Deine Antwort |
|---|---|---|
| 0.1 | Bildschirmauflösung (Windows: Einstellungen > System > Anzeige) | |
| 0.2 | Skalierung in Prozent (100 %, 125 %, 150 %) | |
| 0.3 | Fenstergröße des Spiels beim Start, falls ablesbar (Breite × Höhe in px) | |
| 0.4 | Uhrzeit Beginn / Ende des Tests | |

---

## A. Start und Tor

| Nr | Frage | Antwort | Bemerkung |
|---|---|---|---|
| A0 | Hash der EXE geprüft? In der Eingabeaufforderung im Desktop-Ordner: `certutil -hashfile Nebelseetal_Pre_Release_V_0.0.3.exe SHA256` — stimmt er mit der Zeile oben? (ja / nein / nicht geprüft) | | |
| A1 | Erscheint das Passworttor? | | |
| A2 | Wie viele Sekunden von Doppelklick bis das Tor steht? (grob zählen) | | |
| A3 | Kommst du mit deinem Passwort hinein? | | |
| A4 | Was kommt nach dem Anmelden: Intro/Geschichte, eine Auswahl, direkt die Karte? (beschreiben) | | |
| A5 | Musst du eine Startkarte oder ein Volk wählen? Welche Auswahl steht da? | | |
| A6 | Steht danach ein **leerer** Zustand da (kein alter Spielstand sichtbar)? | | |

---

## B. Die ersten Schritte im neuen Spiel

| Nr | Frage | Antwort | Bemerkung |
|---|---|---|---|
| B01 | Ist eine Siedlung mit Karte da, oder musst du sie erst gründen? | | |
| B02 | Welche Vorräte stehen am Anfang da? (Zahlen aufschreiben: Holz / Stein / Nahrung / Gold) | | |
| B03 | Wie viele Siedler hast du am Anfang? | | |
| B04 | Baumenü: sind alle Gebäude da, die du erwartest? Welches fehlt? | | |
| B05 | Bauen auf der Karte: klappt es, und wird der Preis **genau einmal** abgebucht? (Vorher/Nachher-Zahlen) | | |
| B06 | Forschung: welche Dauer zeigt das Spiel für die nächste Stufe? (Zahl **und** Einheit) | | |
| B07 | Lässt sich die Forschung starten, und läuft die Restzeit sichtbar herunter? | | |
| B08 | Siedlerzuwachs: wächst die Zahl, und wie schnell? (grob) | | |
| B09 | Bewegung: schick eine Einheit auf ein Nachbarfeld — wird eine Dauer angezeigt, und wirkt sie plausibel? | | |
| B10 | Speichern und wieder laden: klappt es, steht danach derselbe Stand da? | | |
| B11 | Steht der Götterschutz irgendwo sichtbar, und passt die Zahl zu deinem Spieltag? | | |
| B12 | Wird irgendwo eine Zahl ohne Einheit oder mit falscher Einheit angezeigt? (wo) | | |

---

## C. Was diese Fassung neu trägt (D-5, D-5a, D-5b)

| Nr | Frage | Antwort | Bemerkung |
|---|---|---|---|
| C01 | Goldrahmen am Geländekästchen: **sichtbar**? | | |
| C02 | Goldrahmen: **gerade** (nicht schief, nicht verrutscht)? | | |
| C03 | Goldrahmen: liegt er **über** dem Geländebild, ohne es zu verdecken? | | |
| C04 | Goldrahmen: sieht er an **allen** Kästchen gleich aus? (ja / nein + welches fällt aus) | | |
| C05 | Goldrahmen: **Ecken** — stört dich der Radius 14 px, oder fällt es dir nicht auf? | | |
| C06 | Die neun Menü-Icons: erkennst du jedes Gebäude **ohne** Text darunter? (Zahl 0–9) | | |
| C07 | Welches Icon ist **nicht** eindeutig? (Name) | | |
| C08 | Marktplatz: steht das **Kennzeichen** links vom Titel? | | |
| C09 | Marktplatz: wirkt die Größe des Kennzeichens stimmig (zu groß / passt / zu klein)? | | |
| C10 | Weltkarte: welche Geländeart ist **schwer** von einer anderen zu unterscheiden? (Namen) | | |
| C11 | Portal-Kopfband: ist das Bild oben **scharf** oder verpixelt? | | |
| C12 | Zwei Bildstile nebeneinander (elf Gebäude noch im alten Stil): fällt es dir **störend** auf? | | |

---

## D. Die bekannten Grenzen — bitte gezielt prüfen

| Nr | Frage | Antwort | Bemerkung |
|---|---|---|---|
| D1 | Bei **1024 × 720**: ist die **Legendenzeile** unten ganz zu sehen? | | |
| D2 | Bei **1024 × 720**: ist die **Knopfzeile** ganz zu sehen? | | |
| D3 | Stößt die **Ressourcenleiste** oben an den Rand, oder wird etwas abgeschnitten? | | |
| D4 | Verkleinere das Fenster schmal (z. B. 900 px breit): **was bricht zuerst**? | | |
| D5 | Ab welcher Breite ist das Spiel **nicht mehr bedienbar**? (px, grob) | | |
| D6 | Gibt es eine Stelle, an der ein Text **mitten im Wort** abgeschnitten wird? (wo) | | |

---

## E. DEIN Block — eigene Tests

**Hier gehört alles hin, was DU ausprobieren willst.** Ich habe nichts vorgegeben: keine Fragen, keine
Erwartungen. Schreib zu jedem Versuch, was du gemacht hast, was du erwartet hättest und was passiert
ist. Genau das ist oft der wertvollste Teil.

| Nr | Was ich ausprobiert habe | Was ich erwartet hätte | Was passiert ist |
|---|---|---|---|
| E1 | | | |
| E2 | | | |
| E3 | | | |
| E4 | | | |
| E5 | | | |
| E6 | | | |
| E7 | | | |
| E8 | | | |
| E9 | | | |
| E10 | | | |
| E11 | | | |
| E12 | | | |

---

## F. Fehler und Abstürze (wörtlich)

| Nr | Was du gemacht hast | Was passiert ist (Text wörtlich) | Uhrzeit |
|---|---|---|---|
| F1 | | | |
| F2 | | | |
| F3 | | | |

---

## G. Abschluss

| Nr | Frage | Antwort |
|---|---|---|
| G1 | Ist das Spiel für dich **so** spielbar (ja / nein / mit Einschränkung)? | |
| G2 | Größter Einzelpunkt, den ich zuerst angehen soll | |
| G3 | Was hat dir am Frischstart am besten gefallen? | |
| G4 | Fertig um (Uhrzeit) | |

**Speichern:** diese Datei einfach speichern (gleicher Ort) — ich lese sie danach aus und trage jeden
Punkt als eigene Zeile ins Prüfregister, mit deiner Antwort als Beleg.
