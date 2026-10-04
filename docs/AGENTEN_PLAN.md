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

Es gibt **zwei** Fassungen desselben Bretts — eine für Menschen, eine für die Kinder:

| Fassung | Wo | Wozu |
|---|---|---|
| **Tagebuch (menschlich)** | `docs/BOARD.md` | Der Hauptagent trägt hier zusammen, was die Kinder gemeldet haben. Daniel liest hier. |
| **Postfach (Maschine)** | `board/` + `tools/brett.py` | Jedes Kind liest und schreibt hier. **Ein Eintrag = eine Datei** — damit überschreiben sich zwei Kinder nie (dieselbe Falle wie zwei Kinder in derselben Quelldatei). |

Die Befehle (jedes Kind benutzt sie selbst):

```bash
python tools/brett.py lesen        # erst lesen: wer hat was belegt, was ist frei
python tools/brett.py belegen --agent kind-a --dateien "src/a.py,tests/test_a.py" --text "baue Modul a"
python tools/brett.py melden  --agent kind-a --text "fertig, 42 Pruefungen gruen" --pruefung "42/0"
python tools/brett.py freigeben --agent kind-a --text "Dateien wieder frei"
python tools/brett.py luecken      # was noch belegt und nicht freigegeben ist
```

Regeln: vor der Arbeit lesen, Dateien belegen, danach melden und freigeben. Nur anhängen —
Einträge werden nie umgeschrieben. Kollisionen meldet das Kind hier, es löst sie nicht selbst.
Der Hauptagent trägt die Meldungen gesammelt in `docs/BOARD.md` nach.

## 5. Auftragsvorlage für ein Kind (kopieren und anpassen)

```
Goal (one sentence, what must exist when done).

Context:
- Project path: D:/Arbeiten/Nebelseetal_Remake (Windows, bash/MSYS; native tools need C:/... paths).
- Read first: `python tools/brett.py lesen` (Postfach: wer hat was belegt?) und `python tools/brett.py luecken`.
- Then read the source files you must obey (never change them).
- Sources you may read but NEVER change: <exact paths>.
- The rule set to obey (original vs proposal): <the belegt facts, verbatim>.
- Deliverable: exactly these files — <new files>.
- Forbidden: touching any existing file, committing, changing data others read, opening windows.
- Write in German (user-facing texts) / plain ASCII in code paths.

Work steps:
1. `python tools/brett.py belegen --agent <name> --dateien "<deine Dateien>" --text "<kurz>"`.
2. Bauen. Eigene Pruefdatei schreiben und laufen lassen.
3. `python tools/brett.py melden --agent <name> --text "<Ergebnis>" --pruefung "<gruen>/<rot>"`.
4. `python tools/brett.py freigeben --agent <name>`.

Acceptance criteria:
- <test file> ends with sys.exit(bericht()) and reports at least N checks.
- Run: python -X utf8 <test file> — report the REAL output.
- Post your entry with tools/brett.py when done.

Report back (max 15 lines): files created, checks passed/failed, what did not work, what you could
not verify. Never prettify a red check.
```

### 5b. Was sich in der Praxis bewährt hat (04.10.2026, Nachtrag)

Sechs Kinder liefen nach dieser Vorlage. Was den Unterschied machte:

1. **Die Funktionsnamen im Auftrag vorgeben.** Das Kind darf die Schnittstelle nicht selbst
   erfinden — sonst passt sie beim Einhängen nicht. Die exakten Signaturen in den Auftrag
   schreiben (`def faktor(forschungsstaende: dict, rohstoff: str) -> float`). Der Hauptagent hat
   sie vorher ausgedacht; das Kind füllt sie.
2. **Die belegten Zahlen WÖRTLICH in den Auftrag.** Nicht „schau im Handbuch nach", sondern die
   Zahlen und ihre Quelle hineinschreiben. Kinder, die selbst suchen, erfinden Werte.
3. **Prüfrahmen und Stil benennen.** „Nutze `tests/harness.py`, sieh dir `tests/test_gebaeude_wirkung.py`
   als Vorbild an, Ende mit `sys.exit(bericht())`" — ohne diesen Satz entstehen eigene
   Prüfgerüste, die sich nicht in `run_tests.bat` einfügen.
4. **Verbot von Fenstern und Git.** Kinder sollen keine tkinter-Fenster bauen (sie stören Daniel
   am Rechner) und nicht committen (der Hauptagent committet erst nach eigener Prüfung).
5. **Eine Datei + eine Prüfdatei je Kind.** Mehr wird unprüfbar; zwei Kinder in derselben Datei
   erzeugen stille Mischschäden.
6. **Was das Handbuch NICHT sagt, gehört in den Auftrag als Lücke.** Jedes Kind soll eine
   Funktion `offene_luecken()` mitliefern. Das hält die Ehrlichkeit an einer Stelle fest.
7. **Die Kinder prüfen sich selbst, der Hauptagent prüft ANDERS.** Ein Kind, das seinen eigenen
   Test grün meldet, hat noch nichts bewiesen — der Hauptagent rechnet nach.
8. **Nebenläufigkeit 3–4.** Mehr gleichzeitig hat den Prüflauf und den Rechner ausgelastet
   (gemessen); bei 3 Kindern bleibt der Rechner für den Hauptagenten benutzbar.
9. **Nach jeder Welle ein Bericht ans Brett und ein Commit.** Sonst weiß die nächste Sitzung nicht,
   was wirklich steht.

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
