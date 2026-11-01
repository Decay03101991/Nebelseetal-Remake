# Weltkarten, Transfer, Bots und Spionage — Daniels Antworten vom 01.11.2026 (verbindlich)

Diese Datei ist **Anhang 3** zum Modell `docs/KONZEPT_SECHS_DOERFER_20261101.md` (dort stehen
Anhang 1 und 2). Sie hält die zweite Fragerunde vollständig fest: 35 Fragen, 35 Antworten. Wo die
Antwort eine frühere Entscheidung **ändert**, steht das ausdrücklich dabei — nichts wird umgedeutet.

## 1. Die vier Restpunkte aus der Übergabe

| Frage | Antwort | Folge |
|---|---|---|
| 1. Transferkosten: welche Währung? | **Mana** — der Tempel ist der Reiseort und erzeugt Mana; Höhe im Spieltest einstellen | Der Transfer rechnet in Mana; kein Gold-Anteil beim einfachen Dorftransfer |
| 2. Bot-Umfang | **Bots erst nur mit Koordinaten, Taktiken später** (abweichend von der Empfehlung) | Das Taktik-Modul `src/bottaktik.py` bleibt liegen, bis die Taktik-Pakete kommen |
| 3. Götterschutz | **so lassen wie im Code, nur anzeigen** (7 Tage oder erster Kriegspunkt) | Keine neue Zahl; nur eine Nachricht beim Ende |
| 4. Kartenziehung (Entscheidung 10) | **nach dem Dorf-Umbau (S-1 bis S-8)** | Bleibt am Ende der Reihe |

## 2. Mana, Beute, Bots, Weltbild

| Frage | Antwort | Folge |
|---|---|---|
| 5. Weiterarbeiten mit dem Restbudget? | **Nein — erst alle Fragen durch, dann eine neue Übergabe** | Diese Sitzung baut nichts mehr |
| 6. Mana-Bilanz | **Transfer billiger (z. B. 500 Mana statt 5.000) UND Tempelertrag anheben (z. B. 20/h Nebelsee, 5/h sonst)** — Zahlen als VORSCHLAG, im Spieltest fein stellen | Zwei Zahlen ändern sich, beide gekennzeichnet; die belegte Richtung bleibt |
| 7. Beute-Regel | **gestaffelte Beute ist die eine Wahrheit; die Bot-Prozente entwickeln wir später mit den Taktiken** | `kampfbericht.beute_staffel` gewinnt; die 50 % im Bot-Kern bleiben vorerst stehen |
| 8. Bots nur mit Koordinaten | **6 Bots, je 1 Dorf mit fester Position, kein Taktikverhalten** | S-7 wird kleiner: Position, Dorf, Sichtbarkeit |
| 9. Erkennbarkeit im Weltbild | **offen — Daniels Vorschlag:** jeder Bot bekommt später ein eigenes Wappen; solange gilt ein farbiger Rahmen mit Bot-Nummer; später richtige kleine Festungen | Rahmen + Nummer jetzt, Wappen und Festungen später |
| 10. Dürfen Bots in dieser Stufe angreifen? | **Nein — erst wenn sie Taktiken haben** | Kein Bot-Angriff im Code, solange die Taktik-Pakete fehlen |

## 3. Das Leben der Bots und der Kampf

| Frage | Antwort | Folge |
|---|---|---|
| 11. Was tun Bots ohne Angriff? | **wirtschaften, handeln und wachsen — je nach später gewählter Taktik** | `botkern` bleibt die Wirtschaft; Angriff wird abgeschaltet |
| 12. Wappen | **erst nur ein farbiger Rahmen mit Bot-Nummer; Wappen kommen mit den Festungen** | Keine Grafik erfinden |
| 13. Weltenwechsel-Preis | **zusätzliche Manakosten und ein klein wenig Gold, später anpassen oder umentscheiden** | Zwei Posten, beide VORSCHLAG |
| 14. Kampfplanungsseite | **Ziel oder Ziele wählen, Reisezeit und Kosten anzeigen; der erwartete Ausgang kommt aus einem Spionage-Bericht, der auch stationierte Truppen und Wallstufe zeigt** | Neue Mechanik: Spionage (Fragen 16–17, 28) |
| 15. Götterschutz-Anzeige | **nur eine Nachricht beim Ende, keine Daueranzeige** | Keine Kopfzeilen-Uhr |

## 4. Spionage und Weltkarten

| Frage | Antwort | Folge |
|---|---|---|
| 16. Wie kommt der Spionage-Bericht zustande? | **ein Späher reist als Auftrag** (eigene Einheit, Hin- und Rückweg, Bericht im Postfach, kann scheitern) | Neue Auftragsart `spaehen` auf dem bestehenden Auftragsweg |
| 17. Genauigkeit | **exakt: Truppenzahl und Wallstufe stehen genau im Bericht** | Keine Spannen, keine Schätzformel |
| 18. Wo sitzen die Bot-Dörfer? | **zufällig je Spielstart verteilt, dann fest**; ein Bot kann später bis zu fünf weitere Dörfer gründen und je nach Taktik auf der Weltkarte setzen; ein Bot wechselt die Weltkarte **nicht so leicht wie der Spieler**, muss aber nach dem Götterschutz auch über Welten hinweg angreifen können — dann mit langen Laufwegen und hohen Manakosten. Billiger und direkter sind Angriffe, wenn das angreifende Dorf nahe am Ziel steht. **Genaue Werte werden entwickelt, nicht angenommen** | Bot-Positionen deterministisch aus dem Spielstart-Seed; Weltkarten-Angriffe später mit eigenen Kosten |
| 19. Was passiert mit den sieben Karten? | **der Menüpunkt muss weg** (nicht brauchbar). Stattdessen zeigt das **Portal** eine schöne Übersicht, welche Weltkarte man bereisen will: man transferiert z. B. drei Dörfer aus der Heimat Midgard in eine andere Weltkarte, greift dort an und kehrt mit den Dörfern zurück. **Das Wort Dimensionen soll aus dem Spiel verschwinden** — es heißt Weltensprünge und Weltkarten | Menüpunkt Karten entfällt, Portal bekommt die Übersicht; Begriffsumstellung |
| 20. Welche Weltkarten? | **Midgard, Valhalla und die anderen früheren Realms/Server sind bei uns die Weltkarten, in denen man auf Koordinaten sitzt und durch den Tempel wechselt** | Die belegten sechs Weltnamen werden die Weltkarten |

## 5. Namen, Grenzen, Fahrplan

| Frage | Antwort | Folge |
|---|---|---|
| 21. Zwei Weltkarten oder alle sechs? | **zum Start zwei Weltkarten, Rest später** | Wurde in Frage 26 und 31 präzisiert |
| 22. Startwelt | **Midgard** — die anderen Welten sind Ziele | Midgard ist die Heimat |
| 23. Dorftransfer | **immer genau ein Dorf je Transfer**, aber in einer gut durchdachten Oberfläche: **freies Feld auf der Weltkarte anklicken**, dann auswählen, welches Dorf dorthin transferiert wird — aus denen, die gerade genug Rohstoffe haben. **Kein Koordinaten-Dropdown** | Klick aufs Feld ist der Einstieg; die Dorfauswahl folgt daraus |
| 24. Bot-Dörfer gründen? | **ja, ganz normal wie der Spieler**; taktisches Know-how für die Kartenwahl kommt mit den Taktik-Paketen | Bots gründen über die Zeit bis zu fünf weitere Dörfer |
| 25. Umbenennung Dimensionen | **schrittweise und sicher, damit das Spiel lückenlos angepasst wird und kaputte Teststände auffallen und repariert werden können** | Kein Hau-Ruck-Umbenennen |
| 26. Name der zweiten Welt | **Es gibt immer die sechs Weltkarten Armageddon, Ragnarök, Utgard, Midgard, Valhalla und Limbus. Sie bilden die gesamte Spielwelt.** | Alle sechs stehen in den Daten |
| 27. Sechs Dörfer | **insgesamt über alle Welten — die Grenze bleibt global** | `SIEDLUNGEN_MAXIMUM = 6` gilt weltübergreifend |
| 28. Spionage im Fahrplan | **zusammen mit der Kampfplanungsseite** — sie liefert den Bericht, den die Planung braucht | Ein Paket: Spionage + Kampfplanungsseite |
| 29. Größe der Weltkarten | **beide 20 × 20 Felder wie heute die Karten** | Kein neues Rastermaß |
| 30. Portal-Menü | **oben die Liste der Weltkarten mit Namen, darunter das Geländekästchen der aktuellen Welt zum Anklicken** | Genau dieser Aufbau |
| 31. Widerspruch 21 gegen 26 | **ja: alle sechs stehen in Daten und Anzeige, erreichbar und bespielbar sind zuerst Midgard und Valhalla, die übrigen vier folgen später** | Auflösung des Widerspruchs, so ist es gemeint |
| 32. Spionage-Einheit | **die bestehende Kundschafter-Einheit benutzen, keine neue Zahl erfinden** | `data/units.json` bleibt unverändert |
| 33. Spionage scheitert | **nur, wenn das Ziel stark verteidigt ist** | Schwelle an der Verteidigung, kein Würfelglück |
| 34. Wann verschwinden die 50 % aus dem Bot-Kern? | **mit den Taktik-Paketen, weil der Bot-Angriff dort erst entsteht** | Bleibt vorerst stehen, mit Hinweis im Docstring |
| 35. Umbenennung sichtbar ab wann? | **ab S-2 (Dorfzentrum und Portal) in der Anzeige; Code und Speicherformat danach Schritt für Schritt** | Anzeige zuerst, Technik danach |

## 6. Was daraus für die Umsetzung folgt (geänderter Fahrplan)

1. **S-1 Gründung** — unverändert: Tempel, Holzfäller, Steinmetz, 10/100/100. Der Entwurf liegt
   anwendbar in `docs/audits/S1_ENTWURF_20261101/`; **sieben** Prüfdateien müssen dabei nachgezogen
   werden (nicht vier — siehe Übergabe).
2. **S-2 Dorfzentrum, Lager und Portal-Übersicht** — Menüpunkt Karten entfällt; Dorfzentrum als
   Menüpunkt und Lagergebäude; Portal-Menü mit Weltkartenliste oben und Geländekästchen der aktuellen
   Welt darunter; hier beginnt die Umbenennung in der Anzeige (Weltkarten, Weltensprung).
3. **S-3 Forschung über die Bibliothek**, **S-4 Einheitenregel** — unverändert.
4. **S-5 Weltbild** — zwanzig mal zwanzig Geländekästchen, Felder anwählbar, eigene Dörfer farbig,
   Gegner als Rahmen mit Nummer, Hover zeigt nach ein paar Sekunden die Transferkosten.
5. **S-6 Dorftransfer** — genau ein Dorf je Vorgang, Klick aufs freie Feld, danach Dorfauswahl aus
   denen mit genug Rohstoffen; Herold holt die Kosten ab, Postfach bestätigt die neue Koordinate; ein
   Dorf nur transferieren, wenn nichts unterwegs ist (Weltenwechsel gesperrt).
6. **S-7 Bots** — sechs Bots, je ein Dorf (später bis zu fünf weitere), Positionen zufällig je
   Spielstart und dann fest, farbiger Rahmen mit Nummer, **kein Angriff**; `botkern` wirtschaftet und
   handelt weiter.
7. **S-8 Bilanz** — sechs Dörfer, Mana (500 Transfer, 20/5 Tempel als VORSCHLAG), Reisekosten.
8. **Danach: Spionage + Kampfplanungsseite** — Kundschafter-Auftrag (Hin- und Rückweg, Bericht im
   Postfach, scheitert nur bei starker Verteidigung, Truppenzahl und Wallstufe exakt), Planungsseite
   mit Zielwahl, Reisezeit, Kosten.
9. **Danach: Kartenziehung** (Entscheidung 10), Taktik-Pakete für Bots, Weltenwechsel-Kosten
   feinjustieren.

## 7. Was noch offen ist (Fragenliste für die nächste Runde, gesammelt)

1. **Wappen der sechs Bots und kleine Festungen** — Stil, Größe, woher die Bilder kommen (Vorschlag:
   selbst zeichnen im Originalstil, ersetzt später die Rahmen-Nummer).
2. **Kostenhöhe Weltenwechsel** — Mana und Gold als VORSCHLAG; nach dem Spieltest zu bestätigen.
3. **Spionage-Schwelle** — was heißt „stark verteidigt“ (Zahl der Verteidiger? Wallstufe? beides?).
4. **Bot-Angriffe über Welten hinweg** — Laufwege und Manakosten, sobald Taktiken existieren.
5. **Sichtbarkeit von Bot-Dörfern** — sofort sichtbar oder erst nach Späherkontakt? (Bisher: sichtbar,
   weil das Weltbild die Gegner zeigen soll.)
6. **Beute-Prozente der Bots** — kommen mit den Taktik-Paketen.
7. **Kartenwahl der Bots** — taktisches Know-how, wie der Spieler es hat, ebenfalls mit den Taktiken.
8. **Weltensprung mit laufendem Auftrag** — bleibt gesperrt (Anhang 2); zu prüfen ist, ob das auch für
   den Späher gilt, der gerade unterwegs ist.
