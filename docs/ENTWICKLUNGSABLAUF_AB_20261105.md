# Entwicklungsablauf ab 05.11.2026 — und die neue Rangfolge der Quellen

Daniel 05.11.2026, woertlich: "Wir brauchen ebenfalls für die weitere Entwicklung einen klaren ablauf
und darum muss vorab schon viel mehr abgeklärt werden. Ab jetzt werden viele schritte von dir und mir
entschieden und es kann kaum noch rücksicht auf die orginalwerte genommen werden. Sie bleiben als
richtwerte aber das Spiel balancing im gesamten geht vor."

## 1. Rangfolge der Quellen (neu, verbindlich)

| Rang | Quelle | Was sie ab jetzt entscheidet |
|---|---|---|
| 1 | **Gesamtbalancing des Spiels** | ob eine Zahl bleibt, steigt oder faellt — Spielgefuehl, Aufbauzeit, Erreichbarkeit aller Ketten |
| 2 | **Daniels Entscheidung** | jede Abweichung von Rang 1 bis 3, wo die Zahlen nicht eindeutig sind |
| 3 | **Original (Handbuch 2009, Seiten 2006)** | **Richtwert**: Startpunkt jeder Zahl, Beleg fuer Struktur und Mechanik |
| 4 | Vorschlag mit Kennzeichnung | nur wo keine Quelle existiert; nie als "belegt" ausgeben |

**Was das praktisch heisst:** Eine Originalzahl wird nicht mehr verteidigt, weil sie im Handbuch steht,
sondern nur noch, weil sie dem Gesamtbalancing dient. Jede Abweichung bleibt aber **dokumentiert**
(`docs/quellen/ABWEICHUNGEN_2006_zu_2009.md` bzw. das Register) mit Quelle, altem Wert, neuem Wert und
Begruendung. Was hier frueher galt ("Balance-Zahlen aus 2009, Struktur aus beiden Fassungen"), ist damit
abgeloest — die Struktur bleibt aus den Quellen, die ZAHLEN folgen dem Gesamtbild.

**Was NICHT erlaubt ist:** eine Zahl ohne Messung und ohne Entscheidung aendern; einen Vorschlag als
belegt ausgeben; eine Kette schliessen, ohne die Aufbauzeit mitzurechnen (Leitlinie "Aufbauspiel",
Register 237).

## 2. Der Ablauf in sieben Phasen (je Schnitt)

| Phase | Was passiert | Fertig-Kriterium |
|---|---|---|
| **0 Aufnehmen** | Fragen, Wuensche und Befunde sammeln (`docs/FRAGEN_AN_DANIEL_<datum>.md`) | jede Frage hat Messlage, 2 bis 3 Moeglichkeiten mit Folge und eine Empfehlung |
| **1 Messen** | Ist-Stand messen: `tools/balancing_messung.py`, `tools/spieltest_simulation.py`, Kennzahlen-Tabelle "Spieltage bis Gebaeude n / Forschung n / erste Einheit / erster Weltwechsel / voll ausgebaut" | Zahlen mit Befehl und Datum, keine Schaetzung |
| **2 Zielbild** | Was soll nach dem Schnitt gelten (Zahl, Zeitfenster, Spielgefuehl)? Widerspruch zu Phase 1 benennen | ein Satz Ziel + eine Zahl, gegen die gemessen wird |
| **3 Entscheiden** | EINE Runde Fragen an Daniel (Formular, Empfehlung zuerst, freie Antwort immer) | alle Entscheidungen schriftlich mit Folge in `docs/ENTSCHEIDUNGEN_DANIEL_<datum>.md` |
| **4 Paket bauen** | Auftrag an das grosse Modell: **fertige Dateien oder Patches + eigene Wache + erwartete Zahlen**; Paket klein halten (`--trocken` zeigt Zeichenzahl und Kosten) | Paket liegt unter `docs/auftraege/` und ist ohne Rueckfrage ausfuehrbar |
| **5 Einbauen** | Kernzahlen selbst nachpruefen, Datei fuer Datei einbauen, Wache fahren, Register + Protokoll + Stand-Block | Einzelwachen gruen, jede Zahl belegt |
| **6 Pruefen** | voller Sammellauf **nach jeder Aenderung an `src/`**; danach ein bis zwei Spieltest-Laeufe mit Urteil | Sammellauf 0 rot; Urteile abgelegt; Kosten protokolliert |
| **7 Ausliefern** | Version erhoehen, EXE bauen, am Bildschirm pruefen, Release ankuendigen, Repo pushen | Release online, Downloads geprueft, Ankuendigung raus |

**Kein Schritt ohne Phase 3:** Ab jetzt wird **vorab** geklaert — wer baut, bevor die Entscheidungen
schriftlich sind, baut zweimal. Fragen, die die Sitzung selbst entscheiden darf, werden als VORSCHLAG
im Register angekuendigt, nicht gestellt.

## 3. Was "vorab viel mehr abklaeren" konkret bedeutet

Vor jedem groesseren Schnitt liegt eine **Entscheidungsliste** vor, die mindestens nennt:

1. **Ziel des Schnitts** in einem Satz und die Zahl, an der er gemessen wird.
2. **Eingriff**: welche Datei, welche Zahl, alt -> neu.
3. **Nebenwirkungen**: was wird dadurch schneller, was langsamer, welche Kette beruehrt das.
4. **Aufbauzeit-Effekt**: Spieltage bis "voll ausgebaut" vorher/nachher (Leitlinie Aufbauspiel).
5. **Quellenlage**: BELEGT / WIDERSPRUCH / NICHT BELEGT / VORSCHLAG.
6. **Rueckrollweg**: welche Datei, welcher Hash.

Erst wenn 1 bis 6 dastehen, geht ein Auftrag an das grosse Modell oder eine Aenderung in den Code.

## 4. Arbeitsteilung (Daniel 21:15)

- **Das grosse Modell** liefert fertige Umsetzungspakete (Code/Patches mit Wache, erwartete Zahlen).
  Budget **4,00 USD** fuer die naechste Sitzung; Kosten je Lauf protokollieren, leere Antworten nicht
  als Ergebnis zaehlen.
- **Die Sitzung** prueft jede Kernzahl nach, baut ein, faehrt Sammellauf und Spieltest, schreibt
  Register, Protokoll, Stand und kuendigt die Version an.
- **Daniel** entscheidet in einer Runde je Schnitt; die Sitzung bringt Empfehlungen mit, keine offenen
  Fragen ins Unreine.

## 5. Erster Durchlauf nach diesem Ablauf

Der naechste Schnitt ist die **Voraussetzungsanzeige** (Waffentechnik 3, Schmiede, fehlende Ware;
`src/main.py:11653`, `:14213`). Er laeuft die Phasen 0 bis 7 einmal vollstaendig durch — als Muster fuer
alles Folgende. Die Balancing-Runde (Mana, Forschungsdauern, Aufbauzeit) folgt direkt danach und
beginnt mit Phase 1.
