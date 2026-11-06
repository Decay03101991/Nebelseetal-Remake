# Wo was liegt - der Wegweiser durch das Projekt (Stand 06.11.2026)

Diese Seite ist die Karte. Sie beantwortet die Frage "wo steht das?" in einer Minute, damit niemand
95 Dokumente durchsuchen muss. Wenn ein Dokument hier fehlt, gehört es in eine der Gruppen unten -
und wird hier eingetragen.

## Zuerst: die vier Dokumente, die den Stand tragen

| Dokument | Was darin steht | Wann lesen |
|---|---|---|
| `docs/SPIELKONZEPT.md` | **das EINE aktuelle Spielkonzept**: Vision, Mechaniken, Zahlenmaßstab, Belegpflicht, offene Punkte | immer zuerst |
| `docs/AKTUELLER_STAND.md` | Tagesstand: was gebaut ist, was gemessen wurde, was als Nächstes kommt | Sitzungsbeginn |
| `docs/ABLAUF_LLM_20261106.md` | die Arbeitsreihenfolge (13 Schritte plus Dokumentenschritt) | vor jedem Schritt |
| `docs/ENTWICKLUNGSPROTOKOLL.md` | die Entstehungsgeschichte, eine Zeile je grobem Schritt | beim Einordnen eines Befunds |

**Protokoll-Hefte:** das laufende Heft ist `docs/ENTWICKLUNGSPROTOKOLL.md`; das vorige Heft
(02.11. bis 06.11.2026, 319 Zeilen) steht vollstaendig in
`archiv/dokumentation/protokoll_alte_fassungen/ENTWICKLUNGSPROTOKOLL_BIS_20261106.md`, die
Historie in `docs/ENTWICKLUNGSPROTOKOLL_HISTORIE_*.md`. Ein Heft wird nie gekuerzt - bei
320 Zeilen beginnt ein neues, und der erste Eintrag ist der letzte des alten.

Dazu das Register `docs/PRUEFREGEL_ORIGINAL.md`: **jede** geprüfte Zahl mit Quelle und Urteil
(BELEGT / WIDERSPRUCH / NICHT BELEGT / VORSCHLAG). Was dort steht, wird nicht erneut geprüft.

## Arbeit und Planung

| Ort | Inhalt |
|---|---|
| `docs/ARBEITSPLAN_AB_20261105.md` | der größere Arbeitsplan hinter dem Ablauf |
| `docs/PLAN_Einzelspieler.md` | der ursprüngliche Bauplan (Pakete) |
| `docs/ENTSCHEIDUNGSVERZEICHNIS.md` | Daniels Entscheidungen in Kurzform, nummeriert |
| `docs/FRAGEN_AN_DANIEL_20261107.md` | die laufende Fragenakte (Antworten als Nachträge) |
| `docs/ANFORDERUNGEN_DANIEL_*.md` | wörtliche Ansagen mit Beleglage je Punkt |
| `docs/AGENTEN_PLAN.md` | Regeln für zuarbeitende Kinder (Dateigrenzen, Prüfpflicht) |

## Messen und Balance

| Ort | Inhalt |
|---|---|
| `docs/balancing/README_KENNZAHLEN.md` | **wie gemessen wird**: die 16 Pflichtschlüssel und ihre Herkunft |
| `docs/balancing/kennzahlen.jsonl` | eine Zeile je Partie (die Vorher-Zahlen) |
| `docs/balancing/KENNZAHLEN_<datum>.md` | die lesbare Tabelle dazu |
| `docs/SPIELBALANCING_TEST.md` | die große Balancing-Messung (Ertrag, Einheiten, Schlachten) |
| `docs/BALANCING_GUTACHTEN_20261105.md` | das Gutachten zum Spielgefühl |
| `tools/spieltest_simulation.py` | der fensterlose Spieltest (`--tage`, `--stil`, `--kennzahlen`) |
| `tools/sammellauf.py` | der volle Prüflauf (eine Ergebniszeile je Datei) |

## Quellen und Originaltreue

| Ort | Inhalt |
|---|---|
| `docs/original/` | Handbuch 2009, die 2006er Seiten, Originaltabellen |
| `docs/quellen/` | Ableitungen, Abweichungen 2006 zu 2009, Original-UI-Befunde |
| `docs/design/` | Entwürfe zu Optik, Startwahl, Weltbild (mit Bildschirmbildern) |
| `docs/audits/` | Prüfberichte, Sammellauf-Protokolle, externe Prüfungen |

## Eingänge, Aufträge, Übergaben

| Ort | Inhalt |
|---|---|
| `docs/eingaenge/` | Antworten fremder Modelle, je Runde ein Ordner (`LLM_20261106`, `LLM_20261106_runde2`, `GEMINI_20261106`) - **Eingang, keine Freigabe** |
| `docs/eingaben/` | sonstige Zulieferungen |
| `docs/auftraege/` | Auftragspakete an fremde Modelle (ab 06.11.2026 hier; ältere Dokumente nennen noch `docs/`) |
| `docs/archiv/uebergaben/` | alte Sitzungsübergaben (ab 06.11.2026 hier) |
| `docs/archiv/fragen/` | abgeschlossene Fragenakten (ab 06.11.2026 hier) |
| `docs/archiv/` | Vorfassungen verdichteter Dokumente (Protokoll) |
| `D:\Arbeiten\Hermes\Uebergaben\` | die Übergaben der letzten Sitzungen, je Zeitstempel ein Ordner |

## Für Besucher (Wurzel des Repos, absichtlich dort)

`README.md` (Einstieg), `SPIEL_ERKLAERUNG.md` (was das Spiel ist und was nicht), `BESUCHER.md`
(Entstehung, Arbeitsweise, Sicherheit), `FRAKTIONEN_WELTEN.md` (sechs Häuser, sechs Welten),
`VORSCHAU.md` (Bilder), `CHRONIK_DER_WELT.md` und `.pdf` (die Geschichte der Welt),
`index.html` (die Besucherseite auf GitHub Pages).

## Regeln für dieses Verzeichnis (damit die Ordnung hält)

1. **Ein neues Dokument gehört in eine der Gruppen**, nicht in `docs/` als 96. Einzeldatei. Was
   wirklich oben stehen muss, ist ein Dokument, das den Stand trägt - davon gibt es vier.
2. **Kein zweites Protokoll in `docs/`** ohne `_HISTORIE` im Namen (sonst wird die Projektordnung
   rot). Vorfassungen gehören nach `docs/archiv/`.
3. **Kein Inhalt löschen, um aufzuräumen.** Verschieben ist erlaubt und wird hier eingetragen;
   Löschen braucht Daniels Zustimmung.
4. **Eingänge werden nicht zu Freigaben**: Antworten fremder Modelle liegen unter `docs/eingaenge/`
   und werden erst nach einer Messung übernommen (Beispiel: `docs/ABGLEICH_LLM_20261106_runde2.md`).
