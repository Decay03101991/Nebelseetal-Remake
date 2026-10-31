# Übergabe: Code-Audit und Aufräumrunde (31.10.2026, ab 14:00)

**Für eine neue Sitzung.** Diese Datei ist der einzige Startpunkt; alles Weitere steht belegt darin.
Sie ersetzt keine früheren Übergaben — `docs/HANDOFF_20261031_1400.md` bleibt gültig für den
Funktionsstand.

## 1. Wo wir stehen (belegt, nicht geschätzt)

| Gegenstand | Wert |
|---|---|
| Arbeitsverzeichnis | `D:\Arbeiten\Nebelseetal_Remake` |
| Letzter Commit (lokal) | `0e1c798` + die Commits dieser Runde (siehe `git log --oneline -12`) |
| GitHub | Branch `stand-20261031-1400` gepusht, `main` unberührt bei `954097a` |
| Prüflauf | **98 Dateien, 97 grün, 0 rot, 1 ausgesetzt** (`docs/audits/sammellauf_20261031_1312.log`, 573 s) |
| EXE | 45.959.096 Byte, SHA256 `bb97d204…`, gebaut 13:24 aus `dfead8e`, Rauchtest bestanden |
| Prüfregister | 64 Punkte (`docs/PRUEFREGEL_ORIGINAL.md`) |
| Kosten heute | Modell-Läufe ≈ 1,35 USD bis 14:00; **Budget für den Code-Audit: 3 EUR** (Daniel, 31.10.2026), Guthaben 6,43 USD |

## 2. Daniels Auftrag für diese Runde

Wörtlich: „lasse ein großes model den code checken und beauftrage es nach kompakteren klügeren
code lösungen zu suchen, damit wir platz sparen … alle funktionen unbeeinträchtigt … die
ordnerstruktur angepasst aber sauber und übersichtlich … du darfst für die code überprüfung bis zu
3 EUR budget verwenden … ich erwarte sogar das du die 3 EUR voll nutzt.“

Zusätzlich festgelegt:
* **Zitate** dürfen berichtigt werden, aber jede Stelle muss nachweisbar sein (Register 64,
  `docs/ZITATKORREKTUREN.md`) — erledigt.
* **Tests** beim Durchgehen mit verschärfen (Textqualität, Pfade) — angefangen.
* **Klügerer Code darf modern sein** (dataclasses, pathlib, Enums, Type-Hints), solange er
  „ordentlich erklärt daneben“ steht.
* **Laptop und WLAN schonen:** Modell-Läufe nacheinander, keine schweren Prüfläufe parallel.

## 3. Was in dieser Runde schon gebaut ist

| Werkzeug/Datei | Zweck |
|---|---|
| `tools/code_mass.py` | Misst Zeilen, Codezeilen, lange Funktionen (≥40/≥60), doppelte 6-Zeilen-Blöcke, unbenutzte Importe, von niemandem importierte Module |
| `tools/modulkarte_bauen.py` → `docs/MODULKARTE.md` | Erzeugt die Karte „welche Datei wofür, wer ruft wen“ direkt aus dem Code (49 Dateien) |
| `tools/codeaudit_pakete_bauen.py` | Baut die fünf Audit-Pakete mit gemeinsamem Kopf (Rolle, harte Regeln, Ausgabeformat) |
| `tools/anfuehrungszeichen.py` | Vereinheitlicht „…“ → „…“ (372 + 10 Stellen), schützt Code und Inline-Code |
| `tools/zitatkorrekturen.py` | Berichtigt Schreibfehler in zitierten Originaltexten mit vollständigem Nachweis |
| `tests/test_textqualitaet.py` | **neu** — prüft Anführungszeichen-Paare, eingeklebte Wörter, Linkziele in 50+ Dokumenten |

## 4. Die Messung, die den Auftrag begründet

```
49 Dateien, 21.703 Zeilen, 17.406 Codezeilen, 904 Funktionen/Methoden
main.py        7.375 Zeilen, 240 Methoden, 27 _render_*, längste Funktion 205 Zeilen
≥60 Zeilen:    47 Funktionen | ≥40 Zeilen: 106
Doppelt:       58 identische 6-Zeilen-Blöcke
Doppelung:     kampf.py (398 Z.) und kampf_alt_handbuch_2009.py (401 Z.), je eine fuehre_schlacht
```

## 5. Die fünf Audit-Pakete (liegen fertig in `docs/audits/code/`)

| Paket | Frage | Größe |
|---|---|---|
| P5 | Ordnerstruktur für `src/`, `tests/`, `tools/` — Umzugsreihenfolge ohne Bruch | 1.452 Token |
| P2 | `kampf.py` gegen `kampf_alt_handbuch_2009.py`: eine Schlachtfunktion | 10.079 Token |
| P3 | Doppelte Rechenwege (Reisezeit, Kosten, Bestand, Beute) in auftraege/spieloekonomie/werkstatt/kampfbericht | 31.698 Token |
| P4 | Vier Zeichenmodule (2.960 Z.): gemeinsames Gerüst statt vier Kopien | 34.920 Token |
| P1 | Aufteilung von `main.py` in thematische Module + gemeinsamer Helfer für die `_render_*` | 106.825 Token |

**Wichtig:** P1 ist mit ~107 k Token nahe am Kontextfenster. Wenn der Lauf abbricht oder Unsinn
liefert, wird `main.py` geteilt (Aufbau/Zustand bis Zeile ~3200, Ansichten danach) und mit zwei
Paketen gefragt.

## 6. Stand der Läufe (bitte zuerst prüfen!)

Eine Kette läuft/lief: **P5 → P2 → P3 → P4** (nacheinander, je ein Aufruf), Ergebnisse nach
`docs/audits/BEFUND_CODE_<P>.md`.

Prüfen mit:
```bash
ls -l docs/audits/BEFUND_CODE_*.md
grep -c "" docs/audits/BEFUND_CODE_*.md
```
Ein Befund unter ~2.000 Zeichen ist wahrscheinlich ein Abbruch (WLAN) — dann diesen einen Lauf
wiederholen, nicht die ganze Kette:
```bash
python -X utf8 tools/gesamtaudit_lauf.py --paket --dossier docs/audits/code/CODE_P3_*.md --ziel docs/audits/BEFUND_CODE_P3.md
```

## 7. So wird umgesetzt (Reihenfolge nach Nutzen und Risiko)

1. **P2 (zuerst):** alte Schlachtfassung entfernen oder zusammenführen — kleinster Eingriff,
   klarer Gewinn, `tests/test_gpt_kampf_forum_neu.py` und `test_kampf_einhaengung.py` sind der Beweis.
2. **P3:** gemeinsame Helfer für Reisezeit/Kosten/Bestand/Beute — Register-Pflicht, weil sich Zahlen
   ändern könnten (dann ist es kein Refactoring mehr, sondern eine Regeländerung).
3. **P4:** gemeinsames Gerüst der Zeichenmodule — Vorsicht: Pixel dürfen sich nicht verschieben,
   `test_welt_optik*`, `test_karten_optik*` vergleichen Zeichenpläne.
4. **P5:** Ordner umziehen, **ein Schritt je Commit**, danach `tools/sammellauf.py` + EXE-Bau.
5. **P1 (zuletzt):** `main.py` teilen — größter Hebel, größtes Risiko. Nach jedem Modul ein Commit
   und ein voller Prüflauf.

**Harte Regel für alle Schritte:** ein Vorschlag = ein Commit = ein grüner Prüflauf. Wird etwas rot,
zurücknehmen statt anpassen. Jeder Umbau bekommt einen Registereintrag; die Modulkarte wird nach dem
letzten Schritt neu erzeugt (`tools/modulkarte_bauen.py`).

## 8. Budget und Kostenführung

* Obergrenze **3 EUR** aus dem DeepSeek-Guthaben (Daniel). Jeder Lauf misst sich selbst; Kosten
  stehen am Ende der Ausgabe (`Kosten: … USD`) und in `docs/audits/BEFUND_CODE_*.md`.
* Bisher in dieser Runde: noch kein Lauf abgerechnet (Kette läuft).
* **Nicht** mehrere Läufe parallel starten (Laptop + WLAN). Bei Abbruch den Einzellauf wiederholen.
* Kosten nach jedem Lauf notieren; am Ende Summe gegen 3 EUR stellen und in
  `D:\Arbeiten\Finanzen\00_Uebersicht\DeepSeek_Kosten\README_Kostenuebersicht.md` fortschreiben.

## 9. Startzeile für die neue Sitzung

```
Lies docs/HANDOFF_CODEAUDIT_20261031.md (diese Datei) und docs/MODULKARTE.md.
Stand: Commit 0e1c798 + Aufräumrunde, Prüflauf 97/98 grün, 0 rot. Budget 3 EUR für den Code-Audit.
Erster Schritt: prüfe, welche docs/audits/BEFUND_CODE_*.md schon fertig sind (P5, P2, P3, P4 liefen),
dann Umsetzung in der Reihenfolge P2 → P3 → P4 → P5 → P1, je ein Commit je Vorschlag mit vollem
Prüflauf. Regeln: Spiel bleibt Spiel, jede Zahl bleibt gleich, Register fortschreiben,
Modulkarte am Ende neu bauen, GitHub-Branch stand-20261031-1400 weiterführen (main unberührt).
```

---

## 10. Nachtrag 14:35 — Stand der Läufe und Kosten

| Paket | Datei | Zeichen | Kosten |
|---|---|---|---|
| P2 | `docs/audits/BEFUND_CODE_P2.md` | 6.986 | 0,0351 USD |
| P5 | `docs/audits/BEFUND_CODE_P5.md` | 10.143 | 0,0498 USD |
| P3 | `docs/audits/BEFUND_CODE_P3.md` | 9.218 | Log |
| P4 | `docs/audits/BEFUND_CODE_P4.md` | 6.719 | Log |
| P1 | `docs/audits/BEFUND_CODE_P1.md` | läuft (107 k Token Prompt) | offen |

**Zusammengefasst und geprüft:** `docs/audits/AUDIT_ZUSAMMENFASSUNG_20261031.md` — dort steht auch,
welche Modellbefunde ich nachgemessen habe (drei richtig, einer falsch, einer halb richtig) und in
welcher Reihenfolge umgesetzt wird.

**Bereits umgesetzt:** P2 (Register 65, Commit `298510a`) — alte Schlachtfassung raus, `src/` von
21.703 auf 21.302 Zeilen.

**Offen für die nächste Sitzung (wichtig):**
1. Umsetzung P3.1–P3.3 (gemeinsame Helfer) — klein, testbar.
2. P4 und P1 auswerten und umsetzen (P1 zuletzt).
3. **Skill- und Regelpflege nachziehen** (Daniel, 31.10.2026: „achte darauf das clean up cronjob und
   deine skill und regelwerke auch immer schön mit allen veränderungen mithalten"): neue Werkzeuge
   (`code_mass.py`, `modulkarte_bauen.py`, `codeaudit_pakete_bauen.py`, `anfuehrungszeichen.py`,
   `zitatkorrekturen.py`) und die zwei neuen Prüfungen in `continuous-improvement` bzw. das passende
   Skill aufnehmen; Cleanup-Cronjob prüfen, ob er die neuen Dateien kennt.
