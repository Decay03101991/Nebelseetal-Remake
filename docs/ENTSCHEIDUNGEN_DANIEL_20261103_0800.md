# Entscheidungen Daniel - 03.11.2026, Fragenrunde 08:00

**Wozu:** die neun offenen Fragen dieser Sitzung, seine Antwort WOERTLICH und was daraus folgt.
Woertlich, damit spaeter belegbar ist, was gemeint war (nicht paraphrasiert).

| Nr | Frage | Antwort Daniel (woertlich) | Folge | Stand |
|---|---|---|---|---|
| 1 | Ertragsweg der Bots (`ertrag_weg`) | "\"karte\" bleibt - deine Vorgabe B-4 gilt (empfohlen)" | `data/bot_wirtschaft.json` bleibt auf `"ertrag_weg": "karte"`; der Felder-Weg bleibt gebaut und geprueft, aber ungenutzt (Register 155) | **erledigt, nichts zu tun** |
| 2 | Forschungsreihenfolge der Bots (S-4) | "Ich lege sie je Taktik als begruendete Datendatei fest (empfohlen)" | S-4 bekommt `data/bot_forschung.json` mit Reihenfolge je Taktik, jede Zahl mit Begruendung - gleiche Form wie `data/bot_bauplan.json` | **Auftrag fuer S-4** |
| 3 | Demo-Termin | "22.11.2026 - Begeisterung vor Tempo (empfohlen)" | Gates G1 08.11., G2/G3 15.11. bleiben als Zwischenziele, **Release 22.11.2026**; Doku und Gates-Tabelle nachziehen | **Dokument, kein Code** |
| 4 | Stufe der Bot-Kartenwahl | "\"mittel\" - ich baue dafuer zuerst einen Bedarf je Rohstoff" | `kartenwahl_stufe` bleibt VORLAEUFIG auf `schwer`, bis der Bedarf je Rohstoff existiert (neue Mechanik: Verbrauch je Rohstoff messen/fuehren); danach auf `mittel` stellen. **Nicht umstellen, bevor der Bedarf da ist** - `mittel` faellt sonst auf die Gold-Regel zurueck | **offen, eigene Aufgabe** |
| 5 | Marktplatz-Motiv und Seiten ohne Hintergrund | "Fuer den Marktplatz und die Hintergruende der Seiten die noch ohne Hintergrund sind, sollen im gleichen Stil vorbereitet werden und dann kannst du diese bereitgestellten Hintergrund bilder nutzen." | Ich bereite Marktplatz-Motiv und die Seiten ohne Hintergrund im gleichen Stil vor; Daniel stellt die Hintergrundbilder bereit, danach werden sie eingehaengt. Bis dahin kein erfundenes Motiv | **offen, wartet auf Bilder** |
| 6 | `karten_teiler` | "10 bleibt (empfohlen)" | `data/bot_wirtschaft.json`: `karten_teiler` 10,0 unveraendert | **erledigt, nichts zu tun** |
| 7 | Duerfen duenne Bots den abwesenden Spieler bestehlen? | "Ja, aber nur mit Bericht im Postfach" | Neue Mechanik noetig: Diebstahl nur gegen schwache Bots moeglich, **jeder Fall als Nachricht ins Postfach** (wer, wann, was, wieviel). Kein stiller Verlust. Eigener Schnitt nach S-6 | **offen, neue Aufgabe** |
| 8 | Zahl der Bot-Doerfer | "Bei 4 bleiben (1 Startdorf + 3 Gruendungen), bis S-6 steht (empfohlen)" | `gruendungen_je_bot` 3 / `doerfer_je_bot_hoechstens` 4 bleiben; S-6 setzt sie um | **erledigt, nichts zu tun** |
| 9 | Journal-Deckel | "Deckel 500 Zeilen je Ort, aelteste fallen weg (empfohlen)" | `produktionsjournal` bei Spieler UND Bots auf 500 Zeilen je Ort deckeln (aelteste zuerst); Wache: Deckel greift, Versorgungsfenster rechnet weiter | **offen, kleine Aufgabe mit Wache** |

## Was daraus sofort gilt

- Der Ertragsweg bleibt beim Kartenprofil - **kein Umbau** an `bot_dorf_ertrag`.
- Die Kartenwahl bleibt auf `schwer`, bis der Bedarf je Rohstoff gebaut ist.
- Das Journal wird gedeckelt (500), aber erst mit eigener Wache und vollem Lauf.
- Der Diebstahl am abwesenden Spieler ist erlaubt, aber **nur mit Postfach-Bericht**.
