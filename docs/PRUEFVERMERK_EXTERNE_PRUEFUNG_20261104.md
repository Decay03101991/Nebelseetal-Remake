# Pruefvermerk: externe Projektpruefung vom 04.11.2026

**Was gelaufen ist:** Zwei Aufrufe `deepseek-v4-pro` (lokal auf demselben Laptop, Daten nur als Text,
keine Zugangsdaten, kein Dateizugriff). Gutachten A (Arbeitsweise) 13.791 Zeichen / 16.338 Token;
Gutachten B (Spiel, Story, Code) 10.037 Zeichen / 17.392 Token; zusammen **33.730 Token**, 287
Sekunden Modellzeit. Die Unterlagen lagen nur im Zwischenspeicher und wurden nach dem Einarbeiten
geloescht - im Projekt bleibt dieser Vermerk.

**Verfahren:** Jeder Befund wurde gegen den Code oder die Messungen gehalten. Urteile: **BESTAETIGT**
(mit Beleg), **TEILWEISE**, **WIDERLEGT** (mit Gegenbeleg), **VERTAGT** (Daniel entscheidet).

# 1. Die drei Kernbefunde (BESTAETIGT, mit eigener Messung)

| Befund der Pruefung | Eigene Gegenmessung | Urteil |
|---|---|---|
| Die Dokumentenpflege ist groesser als der Bau | **294 von 532 Commits (55 Prozent) aendern ausschliesslich Dateien unter `docs/`** (`git log --pretty --name-only`), nur 235 enthalten Code | BESTAETIGT |
| Der Sammellauf ist ein Monolith und bremst jeden Schnitt | 162 Pruefdateien, 9-12 Minuten je Lauf; nach einem Code-Schnitt zweimal (einmal rot, einmal gruen) | BESTAETIGT |
| Die Story fehlt: ein Neuling findet keine Geschichte | Im Code steht kein Intro; die einzigen Weltbezuege sind die Statuszeile "Willkommen in Nebelseetal." und Berater-Antworten zu Limbus und Portalen | BESTAETIGT |

**Einschraenkung (TEILWEISE):** Die Pruefung schreibt, der volle Sammellauf laufe nach JEDER
Aenderung. Fuer reine Dokument-Commits ist das nicht wahr - dort laufen nur die vier
Dokumentpruefungen (so auch heute zweimal geschehen). Fuer Code-Schnitte ist es wahr und teuer.

# 2. Was ich uebernehme (mit Reihenfolge)

| Nr | Massnahme der Pruefung | Mein Urteil | Umsetzung |
|---|---|---|---|
| 1 | **Teststufen** (smoke / kern / voll) statt immer alles | Richtig und sofort nutzbar: die Regel "ein Sammellauf gilt nur, wenn er nach dem letzten Fix startete" bleibt fuer CODE-Schnitte unangetastet, fuer Dokument-Commits gibt es eine eigene, kleinere Stufe | als naechster Schritt: `tools/sammellauf.py` mit den Stufen smoke, kern und voll mit Auswahl nach geaenderten Pfaden, und eine Wache, die belegt, dass "voll" weiter alles faehrt |
| 2 | **Story-Intro** (Weltbruch + Auftrag, 3-4 Saetze) als erster Story-Schritt | Richtig; Daniel hat die Story selbst als wichtig bezeichnet, sie stand aber hinter V-1..V-5 | eigener Schnitt "Story 1" (Intro + Vorgeschichte-Datei, Text aus dem Original) |
| 3 | **Bot-Stimmen** (`data/bot_stimmen.json`, Meldungen je Ereignis) | Richtig und billig: die Meldungen gibt es schon, es fehlt nur der Text je Bot und Situation | eigener Schnitt "Story 2" nach dem Intro |
| 4 | **Fraktions-Kurztexte** im Voelkerwahl-Fenster | Richtig: die Boni stehen heute als nackte Zahlen | Teil von "Story 2" |
| 5 | **Sieg-/Niederlage-Text** | Richtig, klein | Teil von "Story 1" |
| 6 | **Konsistenz-Wache Anzeige gegen Rechnung** | Bereits Projektregel (F-04), aber es gibt keine Wache, die ALLE Anzeigen gegen den Kern haelt - als eigene Wache sinnvoll | spaeterer Schnitt, nach der Story |
| 7 | **`main.py` zerlegen** | Sachlich richtig (13.479 Zeilen), aber ein Umbau an der Wurzel; die Projektregel sagt ausdruecklich: Ordner- und Strukturumbau entscheidet Daniel | **VERTAGT** - Frage an Daniel |
| 8 | **Skill auf 25-35k kuerzen** | Berechtigt: 74.370 Zeichen Hauptdatei plus 28 Referenzen passen kaum in ein Kontextfenster | **VERTAGT** - Frage an Daniel (Kuerzen heisst Inhalt wegwerfen oder weiter auslagern) |

# 3. Was ich ablehne (mit Grund)

> **Nachtrag 04.11.2026:** Ein Punkt dieser Liste war falsch - die Limbus-Dimensionen. Er ist unten
durchgestrichen und korrigiert; alles andere gilt.

| Empfehlung | Warum nicht |
|---|---|
| **Das Entwicklungsprotokoll abschaffen** und durch Commit-Nachrichten ersetzen | Das Protokoll ist **Daniels** Chronik (seine Vorgabe seit dem 05.10.); er liest darin die Entstehung des Spiels. Eine Empfehlung gegen seine ausdrueckliche Einrichtung wird nicht umgesetzt, sondern ihm vorgelegt. Die Pruefung konnte das nicht wissen. |
| **Die 20 Dimensionen im Limbus auf 1-2 reduzieren** | ~~Die 20 Dimensionen sind Originaldaten (Handbuch 2009: 20 Dimensionen, je 20 x 20 Felder). Eine Reduktion waere ein Bruch der Originaltreue.~~ **KORREKTUR (04.11.2026, Daniel):** Das Remake hat sich vom Original geloest - es ist **unser eigenes Spiel mit SECHS Welten und sechs Fraktionen**; Nebelseetal ist nur noch Ursprung und Referenz. Gemessen: `welt.DIMENSIONEN` fuehrt 20 Eintraege, davon **6 benannte Welten** (Armageddon, Ragnaroek, Utgard, Midgard, Valhalla, Limbus) und **14 leere Platzhalter** `Dimension 07` bis `Dimension 20` ohne Welt - sie stammen aus dem Handbuch (Limbus teilt sich in 20 Dimensionen, S. 80) und sind als VORSCHLAG gekennzeichnet. Die Pruefung hatte mit ihrer Reduktionsempfehlung also **recht**, meine Ablehnung war falsch. Beschluss: die 14 Platzhalter werden entfernt, das Spiel fuehrt sechs Welten (Cut "W-6"). |
| **"Jede Zeile kommentiert" abschaffen** | Das ist Daniels ausdrueckliche Vorgabe (01.11.2026), damit er mitlesen kann. Ein Vorschlag dagegen wird ihm vorgelegt, nicht heimlich umgesetzt. |
| **Fragen nur an Daniel, wenn sie Designfragen sind** | Bereits gelebte Praxis (Fragen werden gesammelt, technische Fragen beantwortet der Agent selbst). Die Pruefung hat den Ablauf hier unterschaetzt. |
| **Uebergabe maschinell aus Stand und Register erzeugen** | Richtig im Kern (die Uebergabe wiederholt den Stand-Block), aber die Uebergabe traegt auch Handwerk und Fallstricke, die in keinem Register stehen. Vorschlag: Uebergabe auf zwei Teile - maschineller Zustandsteil und kurzer Handwerksteil. |

# 4. Was die Pruefung uebersehen hat (weil sie den Code nicht lesen konnte)

- **Der Sammellauf laeuft nicht nach jedem Commit** - Dokument-Commits bekommen seit jeher nur die
  vier Dokumentpruefungen.
- **Die Pruefungen lesen ihre Soll-Werte aus den Daten** (Konvention seit dem 01.11.), nicht als
  getippte Zahlen. Der Rotfall von heute kam von einer geaenderten Entscheidung (Kartenwahl-Stufe),
  nicht von einer Balance-Zahl.
- **Fuenf der acht Kampfregeln sind schon gebaut** (eigenes Audit heute,
  `docs/AUDIT_KAMPFREGELN_20261104.md`); die Pruefung schlaegt sie als "drei offene" vor - das ist
  richtig, aber die Reihenfolge ist bereits beschlossen.

# 5. Was ich fuer die naechsten Schritte vorschlage (nach Daniels Entscheid)

1. **Teststufen** (klein, sofort): `smoke` fuer Dokument-Aenderungen, `kern` fuer ein Modul, `voll`
   fuer Code-Schnitte. Messbar: Zeit je Schnitt sinkt von 9-12 auf 2-4 Minuten bei kleinen Aenderungen.
2. **Story 1** (Intro, Vorgeschichte, Siegtext) - der Punkt, den die Pruefung am haertesten trifft und
   der am schnellsten Wirkung zeigt.
3. **Story 2** (Bot-Stimmen, Fraktions-Kurztexte in einer Datendatei).
4. Danach die bereits beschlossene Reihenfolge weiter: Kampfregeln 2/4/6, C (fluessige Ansichten).

**Offene Entscheidungen fuer Daniel:** `main.py` zerlegen (ja/nein/spaeter), Skill kuerzen
(ja/nein), Protokoll behalten (die Pruefung riet zum Abschaffen - ich halte es fuer falsch),
Uebergabe zweiteilen (ja/nein).
