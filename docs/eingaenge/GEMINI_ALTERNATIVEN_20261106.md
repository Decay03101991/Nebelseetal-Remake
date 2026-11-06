# Gemini: drei alternative Lösungswege (Daniel, 06.11.2026)

**Herkunft:** Daniel hat diese drei Zusammenfassungen am 06.11.2026 gegen 05:35 aus dem Gemini-Chat
in die Sitzung gegeben, mit dem Auftrag: „irgendwie sinnvoll als Info hinterlegen … Gute brauchbare
Infos aber evtl nicht notwendig für uns.“ **Wörtlich übernommen, nichts gebaut.**

**Beurteilung der Sitzung (Stand 06.11.2026, nach S2):**

| Vorschlag | Urteil | Begründung |
|---|---|---|
| 1. Zustandsloser Event-Evaluator für Rachetopf und Gunst, gesteuert rein über `data/` | **BRAUCHBAR für S4** | Deckt sich mit unserer Querschnittsregel 5 (kein neues Modul für eine gelöste Aufgabe) und mit dem Muster der bestehenden Fachdateien (`botkern`, `bottaktik`, `dorfwall`). Die Rechnung gehört in eine Fachdatei, die Daten in `data/` — die Oberfläche liest nur. **Kein `tools/event_evaluator.py` außerhalb von `src/`**: Werkzeuge sind bei uns Prüf- und Bauwerkzeuge, das Spiel liest `src/`. |
| 2. Zustandsbasierte Entscheidungsmatrix in den vorhandenen `bot_*.json` statt ereignisgesteuerter Loops | **SCHON SO GEBAUT** | Der Bot-Takt hängt an festen Spielzeitpunkten, der Bauplan steht je Taktik in `data/bot_bauplan.json` (S-8 Stufe 3), Vorräte und Bedarf in `data/bot_wirtschaft.json`/`bot_bedarf.json`. Ein Loop wäre ein zweiter Takt neben dem Kern. |
| 3. Atomare Transaktionen: Guard Clauses mit `.get()`, Prüfung VOR der Buchung | **BESTÄTIGT, gerade umgesetzt** | Genau das Muster von S2: `dorfwall.reparatur_pruefen` sammelt ALLE Bedingungen, `reparatur_starten` bucht erst danach — bei einem fehlenden Posten bleibt das Lager unverändert (Wache: „Lager unveraendert (kein Teilabzug)“). Für S3 gilt dasselbe Muster (`heilung_moeglich` vor dem Buchen). |

**Was daraus NICHT folgt:** kein Umbau von `main.py` in dieser Nacht, kein neues Modul, keine
Ereignis-Maschine. Für S4 ist Vorschlag 1 eine brauchbare Vorlage, aber erst nach der S0-Tabelle V-4
(Zahlen) und nach Daniels Abnahme.

## Die drei Vorschläge im Wortlaut

### Zentrales Event- und Rache-Management (für S3 & S4)

Alternative: Anstatt ereignisspezifische Logik verstreut in main.py oder neue Einzelmodule zu
schreiben, wird ein zustandsloser Event-Evaluator (tools/event_evaluator.py bzw. direkt in
Fachdateien) vorgeschlagen, der den Rachetopf und diplomatische Gunstwerte (0–100) rein über Daten
aus data/ steuert.

Vorteil: Verhindert das Anwachsen der main.py und hält die Bot-Logik transparent.

### Erweiterte Bot-Persönlichkeiten & Interaktion (Schließung der Bot-Lücken)

Alternative: Da 69 von 74 Bot-Funktionen in src/main.py liegen, schlagen wir vor, das Bot-Verhalten
über eine zustandsbasierte Entscheidungsmatrix in den vorhandenen bot_*.json-Dateien abzubilden,
anstatt komplexe ereignisgesteuerte KI-Loops zu bauen. Bots prüfen im Tick lediglich ihre aktuelle
Gunst und Ressourcenreserve.

Vorteil: Keine unnötige CPU-Last, stabiles Offline-Verhalten und einfache Testbarkeit.

### Atomare Transaktionen bei Reparatur und Heilung (S2 & S3)

Alternative: Nutzung strenger Vorab-Prüfungen (Guard Clauses) mit standardisiertem .get() für
Spielstände, um fehlerhafte oder fehlende Schlüssel ohne Dateimigration abzufangen.
Ressourcenabbucheinträge werden vor dem Start der Warteschlange atomar validiert.
