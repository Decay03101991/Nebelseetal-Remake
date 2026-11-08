# Opus als Werkzeug: Auftraege ohne Desktop, Antworten im Repo (Daniel 08.11.2026)

**Daniels Ansage (Chat, 08.11.2026 abends):** der Koordinator darf Claude selbststaendig Auftraege
geben, ohne dass eine Auftragsdatei auf dem Desktop liegt; die Antwort darf direkt an ihn
zurueckkommen; beide duerfen sich nicht stoeren; **der Koordinator bleibt der Chef**.

## Der Weg

```
.venv/Scripts/python.exe -X utf8 tools/frage_opus.py --titel <kurzname> "<Auftrag>"
.venv/Scripts/python.exe -X utf8 tools/frage_opus.py --titel <kurzname> --aus-datei auftrag.txt
```

Das Werkzeug startet `claude -p ... --model opus --effort medium --output-format json` mit
`--allowedTools Read,Grep,Bash` (**nur lesen**) und `--max-turns` (Standard 26), misst Dauer, Zuege
und Listenpreis-Aequivalent und legt Auftrag + Antwort als Markdown unter
`docs/extern/antworten/<JJJJMMTT_HHMM>_<kurzname>.md` ab.

## Feste Grenzen

| Punkt | Regel | Warum |
|---|---|---|
| Schreiben | Opus bekommt **kein** `Edit`/`Write` | gebaut wird nur vom Koordinator, jede Zahl wird gegen den Code geprueft (Register 313) |
| Kosten | nur das Abo (Claude Pro); `total_cost_usd` ist Listenpreis, KEINE Zahlung | kein `ANTHROPIC_API_KEY` gesetzt; nichts kann still auf API-Abrechnung laufen |
| Gleichzeitigkeit | kein Opus-Lauf waehrend eines Sammellaufs und waehrend Daniels Spieltest | 2 Kerne; waehrend seines Tests ist der Rechner SEINE Maschine |
| Umfang | eine Frage je Lauf, Ausgabe in Teilen zu hoechstens ~150 Zeilen | instabiles WLAN bricht lange Antworten ab |
| Ablage | Antwort immer unter `docs/extern/antworten/`, nie auf dem Desktop | eine Chronik, kein Desktop-Verkehr |
| Pruefung | Opus-Irrtum ist der Normalfall: 3 eigene Befunde hat Opus am 08.11. selbst verworfen | der Koordinator misst jede Zahl nach |

## Aufruf-Details, die gemessen sind

- **Der richtige Programmweg ist die `.exe` im node_modules**, nicht der Shell-Wrapper:
  `AppData/Local/hermes/node/node_modules/@anthropic-ai/claude-code/bin/claude.exe`.
  `claude` (ohne Endung) ist ein POSIX-Skript und `claude.cmd` braucht `cmd.exe` - aus `subprocess`
  kommen beide mit `WinError 193`. `tools/frage_opus.py` nimmt die `.exe` zuerst.
- **Zuege knapp halten:** ein Lauf mit vielen Leseauftraegen lief 15 Zuege lang in
  `error_max_turns` und lieferte KEINE Antwort; derselbe Auftrag mit genau benannten Stellen
  brauchte 6 Zuege (247 s) und mit einer einzigen Frage 3 Zuege (17 s).
- **Antworten sind Vorschlaege.** Uebernommen wird nur, was gegen `src/` und `tests/` gemessen ist;
  im Protokoll steht dann "nach Entwurf Opus, umgesetzt und gemessen von Hermes".

## Erster Lauf mit Wert (08.11.2026, 18:47)

Opus pruefte den eigenen Umbau `2f12471` und fand sieben Punkte. Fuenf waren berechtigt und sind
behoben (Erzeuger des Diebstahlberichts nicht belegt, Docstring-Liste zerstoert, Pruefung 8d zu
schwach), zwei sind als Grenze notiert (unbegrenztes Postfach-Wachstum bei ungelesenen Berichten;
`test_ausbildung_vorschau` braucht ein echtes Fenster). Dazu kam der Patch-Plan fuer E1
(Handelspreis je Rohstoff), der als naechster Bauabschnitt vorliegt.
