# VORLAGE: jeder Auftrag an ein Modell (Daniels Regel vom 12.11.2026)

**Diese Vorlage ist Pflicht.** Jeder Auftrag an ein Modell — Claude, GPT, Gemini, ein Subagent —
beginnt mit demselben Kopf, und **jede Antwort gibt den Kopf zurueck**.

## Warum

Daniel, 12.11.2026, woertlich: „Hermes Agent bzw ‚Weltenfresser' bleibt der unberuehrbare
Top-Koordinator egal welcher auftrag von welcher ki bearbeitet wird, und in jedem auftrag muss klar
sein welches model an welches model beauftragt damit klar ist das umsetzung und verstaendnis geregelt
bleiben. solche infos sind fuer auftraege wichtig und auch das sie in der antwort ebenfalls
zurueckgegeben werden.“

**Der Grund in einem Satz:** bei zwei oder mehr Modellen in einer Kette muss jederzeit erkennbar sein,
**wer beauftragt hat, wer liefert und wer entscheidet** — sonst entstehen Auftraege ohne Auftraggeber
und Antworten, die niemanden binden.

## Der Kopf (genau diese Zeilen, in dieser Reihenfolge)

| | |
|---|---|
| **Auftraggeber (Modell)** | Hermes Agent „Weltenfresser“, `deepseek-v4-flash` — **Top-Koordinator des Projekts** |
| **Auftragsnehmer (Modell)** | *Modell und Fassung, z. B. „Claude Opus 5.5 (Thinking: Mittel)“* |
| **Rangordnung** | Weltenfresser bleibt der **unberuehrbare Top-Koordinator**: er zerlegt die Arbeit, misst, prueft, baut und fuehrt Register. Der Auftragsnehmer **arbeitet zu** — er gibt keine Anweisungen an den Koordinator und aendert die Rollen nicht. |
| **Pflicht in der Antwort** | Der Auftragsnehmer nennt **oben in seiner Antwort dieselben zwei Modelle** („Auftrag von …“ / „Antwort von …“) und in einem Satz, **welche Rolle** er darin hatte. |
| **Rueckgabe** | Antwort in Deutsch, mit Zahlen; **Annahmen getrennt von Messwerten**; Zusatzinformationen in einem eigenen, gekennzeichneten Abschnitt |

## Was daraus fuer jeden Auftrag folgt

1. **Ort und Gegenstand nennen** — z. B. „Weltkarte 20 x 20“ gegen „Siedlungskarte 10 x 10“. Dieselben
   Woerter meinen sonst verschiedene Dinge.
2. **Herkunft jeder Zahl markieren**: *gemessen* (mit Zahl und Ort), *gerechnet* (mit Rechnung),
   *angenommen* (ausdruecklich als Annahme). Nie mischen.
3. **Bildschirmfoto beilegen**, wenn es ums Aussehen geht.
4. **Allgemeine Regel statt Einzelwert** pruefen: gilt eine Zahl nur in EINEM Fenster? Dann die Formel
   verlangen, nicht den Wert.
5. **Regeln des Auftraggebers gelten weiter** (Register, Daniel-Entscheidungen, `data/` unberuehrt,
   keine Mechanik-Zahlen ohne Daniel).
6. **Was der Auftragsnehmer nicht pruefen kann**, schreibt er als **UNBEKANNT** hin — der Koordinator
   misst nach.

## Was der Koordinator mit jeder Antwort macht

1. **Nachrechnen, bevor gebaut wird** — jede Zahl selbst nachrechnen, ins Register eintragen.
2. **UNBEKANNT beantworten** — messen, nicht schaetzen.
3. **Erst dann bauen**, mit Wache und Gegenprobe.
4. **Irrwege offen benennen** — eigene Fehler zuerst.

Ablage: `docs/auftraege/`, Dateiname `AUFTRAG_CLAUDE_<THEMA>_NR<n>_<JJJJMMTT>.md`; die Fassung fuer
Daniel liegt als `.txt` (UTF-8 mit BOM, CRLF), die Fassung fuer ein Modell als `.md`.
