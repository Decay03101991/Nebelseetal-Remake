# LLM_20261106 - der Auftrag an externe Modelle und die vier Antworten

**Angelegt:** 06.11.2026, 09:00. **Grund:** Daniel hat den Auftrag aus
`docs/extern/Nebelseetal_LLM_Auftrag_20261106.md` an vier Modelle gegeben und die Antworten am
06.11.2026 auf dem Desktop abgelegt (Ordner `Antworten_Nebelseetal_LLM_Auftraege`). Hier liegen sie
vollstaendig, hashgeprueft und mit Index - so wie die Gemini-Unterlagen in
`docs/eingaenge/GEMINI_20261106/`.

## Der gestellte Auftrag

`auftraege/Nebelseetal_LLM_Auftrag_20261106.md` - **37.297 Byte**,
SHA256 `f75cb37f9ca2ff85ae3f3a5e594720f1cc342a8d54a9069574f78ceb94a2e7ec`. Alle vier Laeufe haben
nachweislich **dieselbe** Datei bekommen (die Kopie im Antwortordner war hashgleich). Inhalt: Spiel,
Mechaniken mit belegten Zahlen, Codeaufbau, gebauter Stand S0 bis S3, geplanter Stand S4/S5,
sieben Abschlussbedingungen A-1 bis A-7, Balancing-Auftrag, Lieferformat in acht Teilen,
Ablagehinweise und die Warnung vor ungepruefter Uebernahme.

## Die vier Antworten

| Datei | Modell | Byte | SHA256 (Anfang) | Format | Struktur |
|---|---|---|---|---|---|
| `antworten/Antwort_ClaudeOpus55_AUFTRAG_20261106.md` | Claude Opus 5.5 | 46.259 | `e9bc61892a62d8e5` | Markdown | 8 Teile eingehalten, **11 Schnitte**, Teil 7a mit Z-1 bis Z-5, Antworten auf Anhang B |
| `antworten/Antwort_UseAI-Instant_AUFTRAG_20261106.md` | UseAI Instant | 86.957 | `e21b914e40aa6418` | Markdown | 8 Teile, **9 Schnitte**, **11 Einwaende** (E-1 bis E-11), laengste Antwort |
| `antworten/Antwort_Grok_Auftrag_20261106.odt` | Grok 4.5 | 25.066 | `eb55e3823ad37d3e` | OpenDocument | eine zusammenhaengende Antwort, Schnitte als Tabellen, 5 Einwaende; Text vollstaendig lesbar (`read_file` extrahiert ODT) |
| `antworten/Antwort_Gemini_AUFTRAG_20261106.md` | Gemini | 8.673 | `abe719935dea98df` | Markdown | 8 Teile, S4 in **einem** Schnitt zusammengefasst, kuerzeste und groebste Antwort |

Alle vier nennen Modell, Datum und die Version des Auftragsdokuments (`V_0.0.3`) am Kopf und markieren
eigene Zahlen als VORSCHLAG - das war die Pflicht aus Abschnitt 11 und 14 des Auftrags.

## Rangfolge fuer den Abgleich (Daniel 06.11.2026)

**Die Claude-Opus-Antwort ist besonders wichtig:** groesstes Modell, und Daniel hat den Zusatz-Content
(Teil 7a, Z-1 bis Z-5) ausdruecklich genehmigt. Reihenfolge deshalb:

1. **Claude Opus 5.5** vollstaendig lesen, Schnitt fuer Schnitt pruefen, Teil 7a getrennt beurteilen
   (Arbeitsprotokoll je Schnitt, Korrekturvorschlaege am Code, Spielgefuehl-Befunde, Vorlage
   `data/diplomatie.json`, Skizze `tools/balance_kreis.py`).
2. **UseAI Instant** als Gegenprobe: es stellt elf Einwaende gegen unseren Stand - jedes davon ist eine
   Frage an unsere eigene Messung, nicht an das Modell.
3. **Grok** fuer die Tabellenform der Schnitte und die fuenf Einwaende.
4. **Gemini** zuletzt: geringste Detailtiefe, brauchbar als Kontrolle, ob die anderen vier Punkte
   uebersehen haben.

## Was vorlaeufig auffaellt (Struktur, KEIN Urteil)

- **Alle vier** halten das Acht-Teile-Format ein - der Auftrag war also verstaendlich.
- **Claude** liefert als einziges einen Zusatzteil zum Arbeitsablauf und Code-Korrekturen; es ist die
  einzige Antwort, die den Ablauf je Schnitt als Protokoll mitdenkt.
- **UseAI** ist am ausfuehrlichsten bei den Einwaenden (11) und den Abschlussbedingungen; mit 86.957
  Byte aber auch die mit Abstand laengste Datei.
- **Gemini** fasst S4 in einen Schnitt und nennt nur zwei VORSCHLAG-Marken - das ist wenig Trennschaerfe
  fuer ein Thema mit vier Unterteilen.
- **Grok** liefert die sauberste Tabellenform je Schnitt (Ziel, Dateien, Aenderung, Daten, Wache,
  Fertig-Kriterium, Aufbauzeit-Effekt, Abloesung, Risiko) - direkt als Vorlage brauchbar.

**Kein Urteil ueber Zahlen.** Jede Zahl aus diesen Antworten ist bis zum Beleg ein VORSCHLAG; die
Pruefung gegen Handbuch 2009, die 2006er Seiten, `data/` und `docs/S0_TABELLEN_20261107.md` macht die
naechste Sitzung beim Einbau.

## Regeln vor jeder Uebernahme (unveraendert)

1. **Nichts ungepruft uebernehmen.** Mehrere Antworten gegeneinander abgleichen, dann die nach unseren
   Prinzipien beste Methode integrieren - nie die neuere, nie die laengste.
2. **Vier Prueffragen je Vorschlag:** Passt es zur Mechanik? Ist die Zahl belegt? Hilft es dem
   Spielgefuehl? Braucht es ein neues Bauteil, und wenn ja, warum kein vorhandenes?
3. **Abloesungen** alter Ablaeufe nur als eigener Schnitt mit Beleg: was faellt, was bleibt, was
   migriert (Daniel, Frage 4 der Runde vom 06.11.2026).
4. **S5 bleibt gesperrt** (Daniel, Frage 5). Vorschlaege dazu sind erlaubt, Einbau nicht.
5. **Ein Schnitt = ein Commit = ein voller Sammellauf.**

## Ablage-Nachweis

Alle fuenf Dateien wurden am 06.11.2026, 08:5x vom Desktop hierher **verschoben** (nicht kopiert), die
SHA256 vor und nach dem Verschieben verglichen - **alle hashgleich**. Der Desktop-Ordner ist danach
entfernt; der Desktop enthaelt nur noch die Uebergabe und die LLM-Auftragsdatei. Nichts geloescht,
nichts umgeschrieben: die Antworten liegen in ihrer Rohform.
