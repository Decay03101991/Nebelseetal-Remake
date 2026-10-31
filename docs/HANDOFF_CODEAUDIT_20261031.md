# Übergabe: Code-Audit und Aufräumrunde (31.10.2026, ab 14:00)

**Für eine neue Sitzung.** Diese Datei ist der einzige Startpunkt; alles Weitere steht belegt darin.
Sie ersetzt keine früheren Übergaben — `docs/HANDOFF_20261031_1400.md` bleibt gültig für den
Funktionsstand.

## 1. Wo wir stehen (belegt, nicht geschätzt)

| Gegenstand | Wert |
|---|---|
| Arbeitsverzeichnis | `D:\Arbeiten\Nebelseetal_Remake` |
| Letzter Commit | `973f733` (Branch `stand-20261031-1400`, gepusht; `main` unberuehrt bei `954097a`) |
| GitHub | Branch `stand-20261031-1400` gepusht, `main` unberührt bei `954097a` |
| Prüflauf | **98 Dateien, 97 grün, 0 rot, 1 ausgesetzt** (Lauf 13:12, 573 s). **Achtung:** seither kamen zwei neue Prüfdateien dazu (`test_textqualitaet`, `test_projektpfade`) und P2 hat eine Prüfung umgedreht - vor der naechsten Arbeit einen vollen Lauf starten |
| EXE | 45.959.096 Byte, SHA256 `bb97d204…`, gebaut 13:24 aus `dfead8e`, Rauchtest bestanden. **Stand ist aelter als der Code** (P2 danach) - nach dem naechsten gruenen Lauf neu bauen |
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

## 2a. Verbindliche Entscheidungen Daniels

Alle offenen Fragen sind beantwortet: **`docs/ENTSCHEIDUNGEN_CODEAUDIT_20261031.md`** (zehn Punkte, aus zwei Auswahlrunden). Dort steht auch die Regel fuer die zwei Fragen, deren Entscheidung Daniel an mich uebertragen hat (Zeitlimit, Auswahl der sechs Dimensionen): erst Quelle, dann Indiz, dann eigene Loesung - und jede eigene Festlegung im Register als VORSCHLAG fuehren.

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

## 7. So wird umgesetzt — nach Daniels Entscheidungen (31.10.2026)

| Schritt | Was | Beweis |
|---|---|---|
| 0 | Voller Prüflauf + EXE neu bauen (Basis) | `tools/sammellauf.py` 0 rot |
| 1 | P3.1–P3.3: gemeinsame Helfer, Karrenladung, Reisezeit-Kette | `test_auftraege`, `test_beute_*`, `test_kampf_einhaengung` |
| 2 | P4: Zeichenmodule teilen | `test_welt_optik*`, `test_karten_optik*` |
| 3 | Aufräumen: ungenutzte Methoden löschen, Belegdateien ins Archiv | `test_oberflaeche_original` (wandert mit), Sammellauf |
| 4 | P5: Paketgerüst **mit `__init__.py`**, Umzug in Wellen, Shims bleiben vorerst | Sammellauf nach jeder Welle |
| 5 | P1: **zuerst** der gemeinsame Render-Helfer, dann Spielkern, dann Ansichten | `test_startspiel`, `test_weltkarte`, `test_durchspiel` |
| 6 | Prüfdateien in Themenordner umziehen (`tests/kern/`, `tests/ui/` …) | Sammellauf findet sie rekursiv |
| 7 | Shims am Ende entfernen | Sammellauf + EXE-Bau |
| 8 | Die fünf Mechaniken: Kartenkampf, Aufträge auf der Karte, Zeitlimit-/Tempo-Option, Dimensionen (6 aktiv), Spionage (nur Aufklärung) | je eigene Prüfdatei + Registereintrag |
| 9 | Skills und Cleanup-Cronjob nachziehen; Git-Größe prüfen und berichten (nicht ändern) | Bericht, keine Codeänderung |

**Harte Regel für jeden Schritt:** ein Vorschlag = ein Commit = ein grüner Prüflauf. Wird etwas rot,
zurücknehmen statt anpassen. Registereintrag, Modulkarte neu bauen, Kosten notieren.

## 8. Budget und Kostenführung

* Obergrenze **3 EUR** aus dem DeepSeek-Guthaben (Daniel). Jeder Lauf misst sich selbst; Kosten
  stehen am Ende der Ausgabe (`Kosten: … USD`) und in `docs/audits/BEFUND_CODE_*.md`.
* Bisher in dieser Runde: noch kein Lauf abgerechnet (Kette läuft).
* **Nicht** mehrere Läufe parallel starten (Laptop + WLAN). Bei Abbruch den Einzellauf wiederholen.
* **Entscheidung Daniels (31.10.2026):** Restbudget **nur für die Umsetzung**, keine Gegenpruefungs-Pakete
  an grosse Modelle. Die Umsetzung macht Hermes selbst; ein Modellaufruf nur, wenn eine Frage ohne ihn
  nicht zu beantworten ist - dann vorher melden.
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

## 10. Nachtrag 15:00 — Läufe abgeschlossen, Kosten gemessen

| Paket | Datei | Zeichen | Kosten |
|---|---|---|---|
| P2 | `docs/audits/BEFUND_CODE_P2.md` | 6.986 | 0,0351 USD |
| P5 | `docs/audits/BEFUND_CODE_P5.md` | 10.143 | 0,0498 USD |
| P3 | `docs/audits/BEFUND_CODE_P3.md` | 9.218 | 0,0673 USD |
| P4 | `docs/audits/BEFUND_CODE_P4.md` | 9.388 | 0,0617 USD |
| P1 | `docs/audits/BEFUND_CODE_P1.md` | 15.097 | 0,1050 USD |
| **Summe** | | | **0,3189 USD** (≈ 0,29 EUR von 3 EUR) |

**Wichtigster Befund (P1, `main.py`):** fünf Zuständigkeiten in einer Datei, zehn Vorschläge.
Die drei mit dem besten Verhältnis:
1. Spielkern (`GameState` + Datenmodelle + Baupreise + Menü) nach `spielkern/` → ~2.600 Zeilen.
2. 27 `_render_*` über einen gemeinsamen Helfer `seite_aufbauen(titel, untertitel, content)`
   → 150–200 Zeilen, weil alle dasselbe Gerüst wiederholen.
3. Ansichten als Mixins nach `gui/ansichten/` → ~3.000 Zeilen.

**Wo das Modell rät (vor Umsetzung prüfen):** es nennt Prüfdateien, die es nicht gibt
(`test_spieloekonomie.py`), und empfiehlt `_render_news` und `_upgrade_building` zu löschen —
mit `grep` nachprüfen, ob wirklich niemand sie aufruft.

**Erledigt und nicht mehr anzufassen:**
* P2 umgesetzt (Register 65, `298510a`): eine Schlachtfunktion, `src/` 21.703 → 21.302 Zeilen.
* Zwei neue Prüfungen grün: `test_textqualitaet` (169), `test_projektpfade` (101).
* Kostenakte aktualisiert: neuer DeepSeek-Export vom 31.10. übernommen (Oktober **16,8062 USD**,
  Gesamt **33,3243 USD**, 31.10. allein **2,1200 USD / 1.228 Requests**), ZIP hashgleich in
  `D:\Arbeiten\Finanzen\_Uebersicht\DeepSeek_Kosten\Rohdaten\`.

**Offen (in dieser Reihenfolge):**
1. Vollen Prüflauf starten (zwei neue Prüfdateien, P2-Änderung) — das ist der Startpunkt.
2. P3.1–P3.3 umsetzen: gemeinsame Helfer (`als_zahl`, `als_int`, `aufzaehlung`), Karrenladung,
   Reisezeit-Kette. Beweis: `test_auftraege`, `test_beute_*`, `test_kampf_einhaengung`.
3. P4 auswerten (`karten_optik`/`welt_optik` teilen `_punkte`, `_box`, `_fuell` Zeile für Zeile).
   **Fallstrick, selbst erlebt:** ein neues Modul in `src/` wurde von den Prüfdateien zunächst nicht
   gefunden (Windows-Verzeichnis-Cache, `ModuleNotFoundError` trotz vorhandener Datei). Erst eine
   Kopie in denselben Ordner frischte den Cache auf. Also: nach dem Anlegen eines Moduls **sofort
   einen Lauf starten** und bei `ModuleNotFoundError` einmal `python -c "import sys;sys.path.insert(0,'src');import <modul>"` prüfen, bevor du den Umbau verdächtigst.
4. P5: Ordnerstruktur. **Entscheidung gehört Daniel:** klassische Pakete mit `__init__.py`
   (sicherer für PyInstaller) oder flach bleiben. Vor dem Umzug prüfen, welche Module wirklich
   ungenutzt sind — P5 lag bei `originalkarten.py` falsch (wird von 4 Modulen und 6 Prüfdateien benutzt).
5. P1: `main.py` teilen, zuletzt. Nach jedem Modul ein Commit und ein voller Prüflauf.
6. **Skill- und Regelpflege** (ausdrückliche Anweisung Daniels): neue Werkzeuge
   (`code_mass.py`, `modulkarte_bauen.py`, `codeaudit_pakete_bauen.py`, `anfuehrungszeichen.py`,
   `zitatkorrekturen.py`) und die zwei Prüfungen in die passenden Skills aufnehmen, Cleanup-Cronjob
   gegenprüfen.
7. Nach jedem Schritt: Registereintrag, `tools/modulkarte_bauen.py` neu laufen lassen,
   `tools/sammellauf.py` grün, EXE bauen, Kosten in die Kostenakte.

## 11. Startzeile (kopierfertig)

```
Lies docs/HANDOFF_CODEAUDIT_20261031.md und docs/audits/AUDIT_ZUSAMMENFASSUNG_20261031.md.
Stand: Commit 973f733 auf Branch stand-20261031-1400 (main unberuehrt), Code-Audit fertig
(fuenf Befunde, 0,3189 USD verbraucht, Budget 3 EUR). P2 ist umgesetzt, src/ hat jetzt 21.302 Zeilen.
Erster Schritt: vollen Prueflauf starten (zwei neue Pruefdateien, P2-Aenderung), dann EXE neu bauen.
Danach in dieser Reihenfolge umsetzen: P3.1-P3.3 (gemeinsame Helfer) -> P4 (Zeichenmodule) ->
P5 (Ordnerstruktur, Entscheidung Daniel einholen) -> P1 (main.py teilen).
Regeln: Spiel bleibt Spiel, keine Zahl aendert sich, jede Umsetzung = ein Commit + voller gruener
Prueflauf + Registereintrag; Modulkarte danach neu bauen; Skills und Cleanup-Cronjob mitpflegen.
Fuer die Umsetzung stehen rund 2,9 EUR des Audit-Budgets bereit - Zwischenpruefungen der Umbauten
sind eingeplant (Diff-Paket an deepseek-v4-pro, ~0,10 USD je Runde).
```
