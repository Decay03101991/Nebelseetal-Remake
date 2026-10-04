# Agenten- und Modellplan

**Vorgabe für jede Sitzung an diesem Projekt.** Beruht auf gemessenen Erfahrungen der Sitzung vom
04.10.2026, nicht auf Vermutungen.

---

## 1. Grundregel: Einer führt, viele bauen

Der **Hauptagent (die Sitzung) ist der Dirigent** und behält:

- alle gemeinsamen Dateien — vor allem `src/main.py` (das Einhängen macht er **selbst**, nacheinander),
- die Prüfgesellschaft: **jede** Kinder-Meldung wird gegen die Quelle gehalten, mit einem **anderen
  Verfahren** als dem des Kindes (z. B. eigene Rechnung statt Kind-Test),
- die Entscheidungen, die Daniel gehören (Produkt, Gefühl, Zahlen ohne Originalvorlage),
- die Commits.

Kinder bauen **Neues in eigenen Dateien**. Sie committen nie, sie fassen Bestehendes nie an.

## 2. Aufteilung: nach DATEIEN, nicht nach Themen

Zwei Kinder in derselben Datei erzeugen stille Mischschäden, die Prüfungen meist nicht bemerken.
Deshalb:

| Für ein Kind geeignet | Nicht für ein Kind |
|---|---|
| neues Modul + eigene Prüfdatei | Änderungen an `main.py` oder an fremden Modulen |
| Datendatei aus einer genannten Quelle bauen | Daten ändern, die andere schon lesen |
| eine abgegrenzte Recherche mit Belegpflicht | Aufgaben mit Geschmacksentscheidung |
| eine Prüfdatei für ein bestehendes Modul (nur lesend) | mehr als ein Denkschritt mit Abhängigkeit |

**Umfang je Kind:** eine Datei plus eine Prüfdatei. Mehr wird unprüfbar.

**Nebenläufigkeit:** 2–4 Kinder gleichzeitig. Sechs gleichzeitig (drei Coding + drei Recherche) hat
gemessen den gesamten Prüflauf spürbar verlangsamt und den Rechner ausgelastet.

## 3. Welches Modell wann — und unter welchen Bedingungen

| Aufgabe | Modell | Weg | Gemessener Preis |
|---|---|---|---|
| Mechanisch und eng beschrieben (Modul mit vorgegebenen Funktionsnamen, Prüfdatei, Suche mit Belegpflicht) | `deepseek-flash` | `delegate_task` (Standard) | Bruchteile eines Cents |
| Entwurf, Analyse, Bewertung, Nachrechnen, Audit | `deepseek-v4-pro` | `hermes chat -q "…" -m deepseek-v4-pro --provider deepseek --reasoning medium` | **0,04–0,12 USD** |
| **Nur Bilddeutung** | `gpt-6-astra` | `hermes chat -q "…" -m gpt-6-astra --provider openai-api --reasoning medium` | **0,47 USD für 3 Bilder** |

**Bedingungen, unter denen ein teureres Modell erlaubt ist:**

1. `deepseek-v4-pro` statt `flash`: wenn die Aufgabe ein **Urteil** braucht (Entwurf, Abwägung, Audit,
   Nachrechnen einer Ableitung) **oder** wenn ein `flash`-Kind zweimal an derselben Aufgabe
   gescheitert ist. Freigabe durch Daniel nicht nötig — es kostet Cent-Beträge.
2. `gpt-6-astra` **nur**, wenn ein **Bild** gedeutet werden muss (Screenshots, Fotos, gescannte
   Seiten). Für Textarbeit ist es nachweislich das Zehnfache ohne Mehrwert.
3. **Nie** ein teures Modell als Werkzeugschleife: ein Umlauf, kleiner Kontext, keine Werkzeuge
   (Ausnahme Bildwerkzeug), danach abbrechen. Jeder zusätzliche Umlauf bezahlt den ganzen Kontext neu.
4. **Kontostände beachten:** OpenAI (astra) hatte am 04.10. nach 4,54 USD noch ~1,02 USD Reserve;
   DeepSeek 3,32 USD, davon **muss ein Rest bleiben**. Ohne Guthaben fragen, nie Schulden erzeugen.
5. **Nach jedem teuren Aufruf messen** und in `docs/PROJEKT_STAND.md` fortschreiben:
   OpenAI `/v1/organization/costs?...&group_by=line_item` (Tageswert wird in Schüben aktualisiert —
   Differenz nehmen), DeepSeek `/user/balance` vorher/nachher.
6. **Antwort sofort sichern**: `docs/audits/` (Zwischenspeicher wird nach 24 h geleert!).

## 4. Das Kommunikationsbrett

Jedes Kind liest vor der Arbeit `docs/BOARD.md`, trägt seinen Anspruch ein, arbeitet, trägt das
Ergebnis mit echten Prüfzahlen ein. Kollisionen werden dort gemeldet, nicht eigenmächtig gelöst.
Immer nur anhängen, nie fremde Zeilen ändern.

## 5. Auftragsvorlage für ein Kind (kopieren und anpassen)

```
Goal (one sentence, what must exist when done).

Context:
- Project path: D:/Arbeiten/Nebelseetal_Remake (Windows, bash/MSYS; native tools need C:/... paths).
- Read first: docs/BOARD.md (claims and messages), then the source files you must obey.
- Sources you may read but NEVER change: <exact paths>.
- The rule set to obey (original vs proposal): <the belegt facts, verbatim>.
- Deliverable: exactly these files — <new files>.
- Forbidden: touching any existing file, committing, changing data others read.
- Write in German (user-facing texts) / plain ASCII in code paths.

Acceptance criteria:
- <test file> ends with sys.exit(bericht()) and reports at least N checks.
- Run: python -X utf8 <test file> — report the REAL output.
- Post your entry on docs/BOARD.md when done.

Report back (max 15 lines): files created, checks passed/failed, what did not work, what you could
not verify. Never prettify a red check.
```

## 6. Erste Aufteilung für die nächsten Schritte

| Schritt | Wer | Modell | Warum |
|---|---|---|---|
| **W4b-4** Kartenerträge an `GameState.tick` hängen + die Lücke im Produktionsfaktor | **Hauptagent selbst** | — | gemeinsame Datei `main.py`, braucht Urteil |
| Prüfdatei für `src/berater.py` erweitern | Kind A | `flash` | eng umrissen, eigene Datei |
| `data/gebaeude_preise.json`: die belegten Preise + Ableitungsregel für die übrigen 16 | Kind B | `flash` | Datenarbeit mit Quelle |
| `src/welt.py` + `data/welten.json` auf 20×20 je Dimension umbauen | Kind C | `deepseek-v4-pro` oder `flash` | Umbau mit Urteil, aber klar umrissen |
| Prüfdatei für `src/gelaende.py` um die Farbwelt erweitern | Kind D | `flash` | klein |
| Menüliste des Originals gegen unsere Oberfläche stellen (Abweichungsliste) | Kind E | `flash` | Vergleich, keine Entscheidung |
| Ein Bild muss gedeutet werden? | astra | `gpt-6-astra` | nur dann |

## 7. Nach jedem Paket

`run_tests.bat` (alle elf Dateien), Ergebnis in `docs/PROJEKT_STAND.md`, kleiner Commit,
Brett-Eintrag, **und eine Zeile ins Entwicklungsprotokoll** (`docs/ENTWICKLUNGSPROTOKOLL.md`) mit
Zeit, Schritt, Ergebnis und Beleg. Nur anhängen, nie umschreiben — auch Fehler und Irrwege gehören
hinein, denn Daniel schreibt die Entstehung des Spiels damit mit. Erst dann das nächste Paket.
