# ANTWORT AUF AUFTRAG NR. 11: Der Portalsprung der Bots

| | |
|---|---|
| **Auftrag von** | Hermes Agent „Weltenfresser“, `deepseek-v4-flash`, Top-Koordinator des Projekts |
| **Antwort von** | Claude Opus 5.5 (Thinking: Mittel) |
| **Meine Rolle** | Ich arbeite zu. Ich schlage eine Regel mit Grenzen vor. Weltenfresser zerlegt, misst, baut und führt das Register, und Daniel entscheidet. |
| **Antwort auf** | AUFTRAG NR. 11 AN CLAUDE (Klasse Opus 5.5): DER PORTALSPRUNG DER BOTS, `AUFTRAG_CLAUDE_PORTALSPRUNG_NR11.md`, Stand 12.11.2026, 20:1x |
| **Für** | Daniel Kössl |
| **Art** | D1 (Vorprüfung vor dem Bau) |

**Kennzeichnung:** **PLATZHALTER** = Zahl, die Daniel setzt. **UNBEKANNT** = bitte messen oder nachsehen. **HART** = darf nicht scheitern. **Startwert** = darf angepasst werden.

---

## 0. Was Daniel dazu schon gesagt hat (wichtig, bitte zuerst lesen)

In **Auftrag Nr. 5, Abschnitt 3.2** steht als Daniels Absicht:

> „Feinde hat der Spieler dort erst später: wenn er selbst erkundet oder wenn Bots stark genug sind, mit ihren **Nebendörfern** einen **Portalsprung** zu machen.“

Daraus folgen schon drei Antworten:
1. **Auslöser:** Stärke.
2. **Wer springt:** Nebendörfer, nicht das ganze Volk.
3. **Wohin:** auch auf die Welt des Spielers.

Meine Regel unten baut genau darauf auf. Die Möglichkeit „nie“ würde Daniels Absicht widersprechen.

---

## A) Auslöser

**Regel: Ausdehnungssprung. Ein Bot schickt ein Nebendorf durchs Portal, sobald er stark genug ist.**

Ein Bot springt in einem Takt genau dann, wenn **alle** Bedingungen erfüllt sind:

| # | Bedingung | Art |
|---|---|---|
| A1 | Punkte des Bots ≥ **PLATZHALTER `S_sprung`** (Punkteschwelle) | Daniel setzt die Zahl |
| A2 | Seit dem letzten Portalsprung **dieses Bots** sind ≥ **PLATZHALTER `T_abstand`** vergangen (Mindestabstand) | Daniel setzt die Zahl |
| A3 | Er hat ein Nebendorf, das noch **nie** gesprungen ist | HART |
| A4 | Für dieses Dorf ist kein eigener Marsch unterwegs, **und kein Marsch zielt auf es** | HART |
| A5 | Es gibt eine Zielwelt nach der Regel unten | HART |

Sind mehrere Nebendörfer geeignet, springt das mit der **kleinsten Dorfnummer** (Reihenfolge im Spielstand). Es wird **nichts gewürfelt**.

**Flucht für Bots: aus.** Würde ein Bot jedem Angriff durch einen Sprung entkommen, liefe jeder Angriff des Spielers ins Leere. Das wäre frustrierend. Wenn Daniel das später doch will, wird es ein eigener **Schalter, PLATZHALTER `bot_flucht` = aus**.

**Wie oft:** höchstens **einmal je Nebendorf und Spiel**, bei bis zu 3 Nebendörfern also höchstens 3 Sprünge je Bot. Es gibt **keinen Rücksprung**. Damit entfällt die Frage „wie lange nicht zurück“.

**Zielwelt** (aus vorhandenen Daten berechenbar, ohne Zufall):
1. Ausgeschlossen sind Welten, auf denen dieser Bot schon ein Dorf hat. Die Heimatwelt ist damit immer ausgeschlossen.
2. Unter den übrigen gewinnt die Welt mit den **wenigsten Dörfern insgesamt** (Spieler und alle Bots, gezählt über `dimension`).
3. Bei Gleichstand gewinnt die **kleinere Weltnummer** (1 bis 6).

**Option für Daniel:** Die Welt des Spielers erst ab **PLATZHALTER `S_spielerwelt`** (≥ `S_sprung`) zulassen. Ohne diese Option wird sie früh gewählt, weil auf ihr am wenigsten steht.

**Zielfeld:** das erste **freie Feld** nach der vorhandenen Streuung (`bottaktik.dorf_position`, CRC32). Frei heißt: kein Dorf, kein Drache, keine Ruine, kein Nebelsee, kein unbebaubares Gelände. Es gilt **dieselbe Prüfung wie beim Spielersprung**. Gibt es kein freies Feld, springt der Bot nicht, und A2 beginnt **nicht** neu zu zählen.

---

## B) Ein Dorf, nicht alle

**Es springt immer genau ein Nebendorf. Das Hauptdorf springt nie.** Begründung:
- Das entspricht Daniels Wortlaut („mit ihren Nebendörfern“).
- Das Hauptdorf bindet den Bot an seine Heimatwelt (`welt_fraktionen.json`). Die Zuordnung „Fraktion → Heimat“ bleibt dadurch immer gültig.
- Würde der ganze Bot springen, wäre seine Heimatwelt plötzlich leer. Jede Karte und jede Strategie müsste dann damit umgehen. Das ist ein deutlich größerer Umbau.

**Gründen:** **Nur auf der Welt des Hauptdorfs.** Gesprungene Dörfer bleiben Außenposten. Die Höchstzahl von 4 Dörfern je Bot bleibt unverändert.

---

## C) Märsche

| Fall | Regel |
|---|---|
| 1. Ein Marsch des Spielers zielt auf ein Dorf, das springen will | **Kommt nicht vor:** A4 sperrt den Sprung. Rückfall (zum Beispiel bei alten Spielständen): wie Regel 9 A, also `ziel_gesprungen`, Umkehr ohne Kampf. |
| 2. Ein Marsch des Bots ist unterwegs, während sein Dorf springen will | **Kommt nicht vor:** A4 sperrt den Sprung. Rückfall: Der Marsch kämpft am Ziel und kehrt per Luftweg zur **neuen** Position zurück, auch über die Welten hinweg. |
| 3. Zwei Märsche auf dasselbe Feld, einer mit `ziel_gesprungen` | **Jeder Marsch bekommt seinen eigenen Bericht.** Der gesprungene sagt „Ziel nicht mehr da, umgekehrt“ und nennt keine Verluste. Der andere kämpft normal. Die Berichte werden **nie zusammengelegt**. |

---

## D) Anzeige für den Spieler

| Wo | Wann |
|---|---|
| **Postfach** | **genau einmal je Sprung**, aber nur, wenn der Spieler auf der Start- **oder** Zielwelt ein Dorf hat |
| **Statuszeile** | zusätzlich einmal, wenn die **gerade offene** Weltkarte die Start- oder Zielwelt ist. Die Karte wird dann neu gezeichnet; der Spieler bleibt auf seiner Karte. |
| Bot-Stimme | nur, wenn `data/bot_stimmen.json` schon eine passende Gruppe hat (UNBEKANNT). Keine neuen Schlüssel ohne Daniel. |

**Bauplan der Meldung**, kein fertiger Text:

> [Fraktion] · [Dorfname] · hat [Startwelt] verlassen · → [Zielwelt] · (nur wenn die Zielwelt eine Welt mit einem Dorf des Spielers ist:) bei Feld [x, y]

**Darf der Spieler die Zielwelt erfahren? Ja.** Er kann sie ohnehin besuchen. Ein Geheimnis würde keine Spielmechanik schützen, sondern nur verwirren.

Ist das gesprungene Dorf gerade **ausgewählt**, wird die Auswahl aufgehoben (Regel B7 aus Antwort Nr. 5).

---

## E) Ausschlüsse (prüfbar)

| # | Darf nie passieren | Prüfung |
|---|---|---|
| E1 | Ein **Hauptdorf** springt | Zählung: 0 Sprünge von Hauptdörfern |
| E2 | Ein Dorf springt, während ein eigener Marsch unterwegs ist oder ein Marsch auf es zielt. Das gilt auch für laufende Belagerungen; ob es die gibt, ist UNBEKANNT. | Prüfung je Sprung gegen die Marschliste |
| E3 | Sprung auf ein nicht freies Feld oder in eine Welt, auf der der Bot schon ein Dorf hat | Prüfung je Sprung |
| E4 | Die Ansicht des Spielers wechselt die Welt | Messung: geöffnete Welt vor und nach dem Sprung gleich |
| E5 | **Zufall:** Derselbe Spielstand führt zweimal zu unterschiedlichen Sprüngen | Spielstand zweimal laden, gleiche Takte laufen lassen, Ergebnisse vergleichen |

---

## F) Stellen im Code

Deine Liste stimmt. Ich **streiche nichts** und **ergänze**:

| Stelle | Warum |
|---|---|
| Prüffunktion „freies Feld“ des **Spielersprungs** (Register 482) | **wiederverwenden, nicht kopieren** (siehe Z3) |
| `welten_belegt` / `data/welten.json` | Zählung der Dörfer je Welt für die Wahl der Zielwelt |
| `data/welt_fraktionen.json` | Heimatwelt, um das Hauptdorf zu erkennen |
| Gründung neuer Bot-Dörfer | auf die Welt des Hauptdorfs beschränken |
| Auswahl und Seitenpanel der Portalansicht | Auswahl aufheben, wenn das ausgewählte Dorf springt |
| Marker-Cache und Neuzeichnen der Portalansicht (Antwort Nr. 10) | neu zeichnen, wenn die offene Welt betroffen ist |
| Kampfbericht | getrennte Berichte (Fall C3) |
| alle Zufallsaufrufe im Bot-Takt | dürfen den Sprung nicht beeinflussen (E5) |

**Neue Datenschlüssel:** Es sind vier: `S_sprung`, `T_abstand`, optional `S_spielerwelt` und `bot_flucht`.
- Sie gehören in die **vorhandene** Datei mit den Bot-Einstellungen, falls es eine gibt (UNBEKANNT, bitte nachsehen).
- Sonst wäre eine neue Datei `data/bot_portalsprung.json` nötig. Beides nur mit Daniels Zustimmung.
- **Im Spielstand** braucht jedes Bot-Dorf ein Merkmal „schon gesprungen“, und jeder Bot einen „Zeitpunkt des letzten Sprungs“. Bei alten Spielständen ist der Standardwert „nein“ bzw. „nie“.

---

## G) Abnahme

| # | Kriterium | Art | Prüfweg |
|---|---|---|---|
| 1 | Sprünge nur, wenn A1 bis A5 erfüllt sind, und nie zufällig | HART | Zählung über 100 Spielstände, dazu E5 |
| 2 | Nach dem Sprung steht das Dorf auf der Zielwelt, auf deren Karte sichtbar und auf der alten nicht | HART | Messung im Fenster |
| 3 | Hauptdorf und die anderen Nebendörfer sind unverändert | HART | Messung |
| 4 | Fälle C1 und C2 kommen nicht vor; C3 erzeugt zwei Berichte | HART | Prüfung je Fall |
| 5 | Die Meldung kommt genau einmal, nur unter der Bedingung aus D | HART | Prüfung |
| 6 | E1 bis E5 treten nie ein | HART | wie in E |
| 7 | Ein alter Spielstand lädt ohne Absturz; seine Dörfer gelten als „noch nie gesprungen“ | HART | Ladeprobe |
| 8 | Höchstens 3 Sprünge je Bot und Spiel | HART | Zählung |

---

## Was ich nicht geprüft habe

- Ob es eine Datei mit Bot-Einstellungen gibt und wie `data/bot_stimmen.json` gegliedert ist.
- Ob es Belagerungen als eigenen Zustand gibt.
- Ob die CRC32-Streuung in `bottaktik.dorf_position` ein freies Feld garantiert oder nur einen Vorschlag liefert. Im zweiten Fall braucht es die Prüfung aus A noch zusätzlich.
- Wie Punkte im Spiel entstehen. Sie sind laut T08 ein Feld der Ressourcenleiste; ob Bots denselben Wert haben, ist UNBEKANNT.

---

## Anmerkungen an Weltenfresser (zusätzlich, nicht beauftragt)

> Diesen Abschnitt hast du in Auftrag 11, Abschnitt 5 erlaubt. Alles hier ist ein Hinweis, keine Anweisung.

**Z1 Zwei Bedeutungen von „Zufallssprung“.**
- In meinen Sprungregeln (`Claude_Opus_5.5_Sprungregeln_Weltkarte.md`, Regel 3a) heißt **Zufallssprung**: „Das Spiel sucht das **Zielfeld** zufällig aus.“
- In deinem Auftrag steht Daniels Regel 3 als „es wird nicht gewürfelt, **wer** springt“.

Das sind zwei verschiedene Dinge. Bitte bei Daniel klären, welches er meinte; vermutlich beides. Meine Antwort erfüllt beide Lesarten, denn nichts wird gewürfelt.

**Z2 Deine Umformulierung von G2 (Antwort Nr. 10) ist richtig.** Ich habe sie geprüft: Alle sechs Formen und die Raute habe ich auf der **echten Palette aus `data/gelaende.json`** gerendert, bei f = 20.
- Auf Wald, Sumpf, Nebelsee und Hügel verschmilzt der dunkle Halo mit dem Gelände. Dann trägt der **Creme-Ring** den Umriss (gegen den Halo 15,13).
- Die Form bleibt dabei überall klar erkennbar. Der Marker wirkt auf dunklem Gelände nur bis zu 4 px kleiner.
- **„Mindestens ein Ring ≥ 3“ ist damit das richtige Kriterium.** Die Palette muss nicht geändert werden.

**Z3 Nicht kopieren.** Der Spielersprung hat schon eine Prüfung „Feld frei“, mit Drache, Ruine und unbebaubarem Gelände. Kleine Modelle neigen dazu, solche Prüfungen für den Bot **neu zu schreiben**. Dann laufen beide auseinander, sobald eine geändert wird. Bitte **dieselbe Funktion** aufrufen.

**Z4 Alte Spielstände einmal beim Laden umstellen.**
- Hat ein Dorf `herkunftswelt == 0`, wird `herkunftswelt` beim Laden **einmal** auf die Heimatwelt seiner Fraktion gesetzt.
- Dann braucht der Kartenfilter keine Sonderregel mehr, und „Hauptdorf erkennen“ funktioniert auch bei alten Spielständen.
- Das ist eine Codeänderung, keine Datenänderung.

**Z5 Ganzzahlige Punktlisten (dein Tipp 1) für Antwort Nr. 10.** Die Werte sind im vierfachen Raum (×4A), gerundet mit „+0,5, dann abschneiden“. Zu jedem Punkt kommt noch der Versatz 4 × Ringbreite hinzu (Bot: +16).

| A | Form | Punkte (x, y) |
|---|---|---|
| 16 | Menschen | (0,0) (64,0) (64,26) (61,40) (52,51) (32,64) (12,51) (3,40) (0,26) |
| 16 | Zwerge | (32,0) (60,16) (60,48) (32,64) (4,48) (4,16) |
| 16 | Ghule | (32,3) (64,61) (0,61) |
| 16 | Trolle | (32,3) (41,22) (62,25) (47,40) (51,61) (32,51) (13,61) (17,40) (2,25) (23,22) |
| 16 | Raute | (32,0) (64,32) (32,64) (0,32) |
| 33 | Menschen | (0,0) (132,0) (132,53) (125,82) (108,106) (66,132) (24,106) (7,82) (0,53) |
| 33 | Zwerge | (66,0) (123,33) (123,99) (66,132) (9,99) (9,33) |
| 33 | Ghule | (66,5) (132,127) (0,127) |
| 33 | Trolle | (66,6) (85,46) (129,52) (97,83) (105,126) (66,105) (27,126) (35,83) (3,52) (47,46) |
| 33 | Raute | (66,0) (132,66) (66,132) (0,66) |
| 42 | Menschen | (0,0) (168,0) (168,67) (160,104) (138,134) (84,168) (30,134) (8,104) (0,67) |
| 42 | Zwerge | (84,0) (157,42) (157,126) (84,168) (11,126) (11,42) |
| 42 | Ghule | (84,7) (168,161) (0,161) |
| 42 | Trolle | (84,8) (109,58) (164,66) (124,105) (133,160) (84,134) (35,160) (44,105) (4,66) (59,58) |
| 42 | Raute | (84,0) (168,84) (84,168) (0,84) |

- **Kreis und Quadrat** brauchen keine Liste, nur Rahmen bzw. Rahmen und Eckenradius.
- Für jedes andere A gilt dieselbe Rechnung. Die Formel ist sicherer als die Tabelle.

**Z6 Danke für die Rückmeldung.** Alle fünf Tipps übernehme ich ab jetzt: ganze Pixel, HART und Startwert, Datei und Schlüssel, Bauplan statt Satz, PLATZHALTER.

---

Ende der Antwort auf Auftrag Nr. 11.
