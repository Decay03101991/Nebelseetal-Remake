# GEMINI_20261106 - aller Gemini-Stoff an EINEM Ort

**Angelegt 06.11.2026** auf Daniels Vorgabe: „infos von Gemini können alle samt in einem Ordner
angelegt für Gemini Aufträge bzw der Antworten abgelegt werden“.

**Was hier liegt:** der gefilterte Eingang, unsere Aufträge an das Chat-Modell, seine Antworten und
unsere Auswertungen dazu. **Was hier NICHT liegt:** Spielcode, Entscheidungen, Register.

## Aufbau

| Ordner | Inhalt | Regel |
|---|---|---|
| `eingang/` | der von uns gefilterte Gemini-Input (6 Dokumente: README, brauchbar, teilweise, abgelehnt, Lücken, Bewertung) | unverändert, nur gelesen |
| `auftraege/` | unsere sechs Aufträge (fünf Fachaufträge vom 06.11. + der Google-Auftrag mit drei Teilen) | die Wahrheit dessen, was wir gefragt haben |
| `antworten/` | acht Antworten (fünf Fachantworten, Menüstories, Arbeitsweise-Feedback, Google-Antwort) | unverändert, **nie** blind übernehmen |
| `auswertungen/` | unsere Prüfvermerke und Einordnungen | **hier steht das Urteil** - das ist die führende Sicht |

## Pfadänderung (alte Verweise bleiben gültig)

Zum 06.11.2026 sind die Dateien umgezogen. **Register, Protokoll und ältere Übergaben nennen noch die
alten Pfade** - sie werden nicht umgeschrieben (Historie), hier steht die Zuordnung:

| Alter Pfad | Neuer Pfad |
|---|---|
| `docs/eingaenge/GEMINI_INPUT_20261106/` | `docs/eingaenge/GEMINI_20261106/eingang/` |
| `docs/auftraege/20261106/` | `docs/eingaenge/GEMINI_20261106/auftraege/` |
| `docs/eingaenge/AUFTRAG_GOOGLE-KI_20261106.txt` | `docs/eingaenge/GEMINI_20261106/auftraege/` |
| `docs/eingaenge/GEMINI_ANTWORTEN_20261106/` | `docs/eingaenge/GEMINI_20261106/antworten/` |
| `docs/eingaenge/GEMINI_ANTWORT_AUFTRAG_20261106.txt` | `docs/eingaenge/GEMINI_20261106/antworten/` |
| `docs/PRUEFVERMERK_GEMINI_*.md` | `docs/eingaenge/GEMINI_20261106/auswertungen/` |
| `docs/eingaenge/EINORDNUNG_GEMINI_*.md`, `GEMINI_ALTERNATIVEN_*.md`, `GEMINI_WEITERE_VORSCHLAEGE_*.txt` | `docs/eingaenge/GEMINI_20261106/auswertungen/` |

## Urteil je Quelle (Stand 06.11.2026)

| Datei | Urteil | Wofür nutzbar |
|---|---|---|
| `eingang/01_BRAUCHBAR.md` | BRAUCHBAR | Ideen, die zum Spiel passen (Menügeschichten, Postfach, Mauerreparatur) |
| `eingang/02_TEILWEISE.md` | TEILWEISE | gute Richtung, falsche Umsetzung (dict-Zugriffe statt Felder) |
| `eingang/03_ABGELEHNT.md` | ABGELEHNT | passt nicht zu unseren Mechaniken (siehe Begründung dort) |
| `eingang/04_LUECKEN.md`, `05_BEWERTUNG.md` | BEFUND | was Gemini nicht wusste - wichtig für künftige Aufträge |
| `antworten/Antwort_Gemini_AUFTRAG_01_POSTFACH_UND_RUHM` | TEILWEISE | Anzeige-Ideen brauchbar; **Fristen standen als Konstanten im Code** - bei uns in `data/nachrichten.json` gelöst |
| `antworten/Antwort_Gemini_AUFTRAG_02_MAUERREPARATUR` | TEILWEISE | Rechenrichtung brauchbar, Preis war erfunden - bei uns aus dem belegten Wallpreis gerechnet (V-1) |
| `antworten/Antwort_Gemini_AUFTRAG_03_VERWUNDETENHEILUNG` | TEILWEISE | verwies auf `data/kaserne.json`, die es nicht gibt; Einheitenkosten sind bei uns nicht einheitlich Gold |
| `antworten/Antwort_Gemini_AUFTRAG_04_DIPLOMATIE_UND_RACHE` | BRAUCHBAR als Textvorlage | für S4; Zahlen daraus NICHT übernehmen (V-4 gilt) |
| `antworten/Antwort_Gemini_AUFTRAG_05_SIEDLUNGSUMZUG` | ABGELEHNT (Mechanik) | schlug Verlust aller Gebäude vor; Daniel will sie mitziehen (Entscheidung 8) |
| `antworten/Antwort_Gemini_MENUESTORIES` | TON FALSCH | vier Themen brauchbar, Texte bei uns neu geschrieben (`data/story.json`) |
| `antworten/Gemini_Feedback_Arbeitsweise` | BRAUCHBAR | Hinweise zur Zusammenarbeit (kleine Pakete, klare Grenzen) |
| `antworten/GEMINI_ANTWORT_AUFTRAG_20261106.txt` (Google) | **TEIL A + B BRAUCHBAR, TEIL C UNBRAUCHBAR** | Teil A: 26 Testfälle für S3 (**Fall 17: 50 statt 60 Prozent**). Teil B: Diplomatietexte (Kennungen laufen B1-B12). Teil C: C3/C4 nennen keine Menge, C5 keine Restzeit |
| `auswertungen/PRUEFVERMERK_GEMINI_ANTWORTEN_20261106.md` | FÜHREND | vier Codefehler belegt - vor jedem Einbau lesen |
| `auswertungen/PRUEFVERMERK_GEMINI_MENUESTORIES_20261106.md` | FÜHREND | Tonprüfung der vier Geschichten |
| `auswertungen/EINORDNUNG_GEMINI_ANTWORT_AUFTRAG_20261106.md` | FÜHREND | die drei Fehler der Google-Antwort |
| `auswertungen/EINORDNUNG_GEMINI_VORSCHLAEGE_20261106.md` | FÜHREND | **falsche Reparaturformel (`/10` statt `/100`)**, zweiter Sammellauf unnötig |
| `auswertungen/GEMINI_ALTERNATIVEN_20261106.md` | BRAUCHBAR für S4 | zustandsloser Event-Evaluator, Entscheidungsmatrix in `bot_*.json`, atomare Buchungen |

## Vier Prüffragen vor JEDEM übernommenen Vorschlag (Daniel, 06.11.2026)

1. **Passt es zu unseren Mechaniken?** (Ortslager statt Reichslager, eine Uhr in Spielsekunden, Wall
   ortsgebunden, Bots mit eigener Wirtschaft, ein Kampfweg.) Was eine zweite Wahrheit einführt, fliegt.
2. **Ist die Zahl belegt?** Jede Zahl muss aus `data/`, dem Handbuch 2009, der Vorversion 2006 oder
   einer S0-Tabelle kommen. Sonst ist sie ein VORSCHLAG und wird Daniel vorgelegt.
3. **Hilft es dem Spielgefühl?** Ziel ist ein stimmiges Spiel aus Aufbau, Wirtschaft und Nebelseetal-
   Geschichte - kein Mechanik-Sammelsurium. Was nur „auch möglich" ist, wird nicht gebaut.
4. **Braucht es ein neues Bauteil?** Eine gelöste Aufgabe bekommt kein zweites Modul. Rechnung gehört
   in die vorhandene Fachdatei, Text in die Datendatei, Anzeige liest den Kern.

Wer einen Vorschlag übernimmt, schreibt das Urteil in die zuständige `EINORDNUNG_*`-Datei **und** eine
Registerzeile. Ohne Urteil gilt der Vorschlag als nicht geprüft.
