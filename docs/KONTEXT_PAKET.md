# KONTEXT-PAKET — Nebelseetal Remake (Stand 05.10.2026, 19:45 · Zeiten mit `date` geholt)

**Diese Datei ist die Übergabe. Lies SIE zuerst (≈ 7 KB) und sonst nur, was hier als Zeiger steht —
`docs/PROJEKT_STAND.md` (67 KB) und `docs/ENTWICKLUNGSPROTOKOLL.md` (75 KB) sind Nachschlagewerke,
keine Einstiegslektüre.** Projekt: `D:\Arbeiten\Nebelseetal_Remake` (bash/MSYS, `python -X utf8`).
Ziel: fertige, fehlerfrei spielbare, passwortgeschützte Einzelspieler-`.exe` (Handbuch 2009 = Wahrheit).

---

## 1. Belegter Ist-Stand

| Was | Beleg |
|---|---|
| **Sammellauf** | **3553 bestanden · 0 Fehler · 21 Befunde · 50 Dateien** (19:36; `…/cache/scratch/sammellauf.py`) |
| **Arbeitsbaum** | **sauber** (`git status --short` leer), letzter Commit **`fdac05b`** — 19:39 |
| **`.exe`** | **14.607.530 Byte**, SHA256 `942e07046df3add46237442f61cc85cce528528444c907de1d30a21768b0a873`, 19:34; genau **eine** `.exe`, `build/`+`dist/` aufgeräumt |
| **Startprüfung** | aus `…\hermes\cache\scratch\exestart` (anderer Ordner): Fenstertitel „Nebelseetal Remake", **0** Fehlerberichte, danach **0 offene Spielprozesse** |
| **Sicherung** | `docs/SICHERUNGEN.md` — 16 führende Papiere mit Prüfsummen (19:37) |
| **Zielregister** | kein fremdes aktives Ziel; **diese** Sitzung auf `cleared` gesetzt (Grund im Datensatz) |
| **Kosten** | **6,38 EUR / 4,00 EUR = „UEBER_LIMIT"** (7,16 USD, 50 Sitzungen, 5 Modelle) → **nur kostenlose/lokale Wege, bis Daniel freigibt** |

`git log --oneline -3` · `git status --short` · `python tools/zieluebergabe.py --pruefen` → alles in Sekunden.

## 2. Der EINE nächste Schritt

**Handels-Paar `handel_start` / `handel_abschluss`** in **`src/spieloekonomie.py`** (Vorbild: die
fertige `transport_start`, dort ab **Z. 290**) — Vorgabe **Entwurf `docs/audits/entwurf_spieloekonomie_sol_2026-10-05.txt` Z. 752**: bestätigte Einzelangebote mit echter Handelskarawane,
Preis beim Angebot fest, Mengen/Gegenleistung vor dem Start sperren, Abschluss nach der Reise,
Rückgabe bei Ablehnung, **keine Netzfunktionen, keine Gratisgewinne** — und **nie** `_trade`/Altpfad
weiterverwenden. **Neu dazu:** `tests/test_handel_transaktion.py`, Eintrag in `run_tests.bat`.
**Erwartet:** neue Prüfdatei grün, Sammellauf **3553 + N** ohne Fehler.

Danach Schritt 9 (`main`-Anbindung, Migration, Anzeige) und Schritt 10 (`tick_bis`/Ereignisschleife,
**erst dann** Aktivierung des Ökonomiemodus; Entwurf Z. 1092).

## 3. Roadmap Ökonomie-Paket (Reihenfolge des Papiers, „kein Halbumbau")

| Schritt | Inhalt | Beleg |
|---|---|---|
| 0 | 4 Handbuch-Korrekturen (Götterschutz 7 Tage, Steinmetz ohne Forschung, Forschung sperrt Siedlung, Rinderfarm Nahrung+Leder) | `203e2fa` |
| 1 | Kartenvorrat + `data/spieloekonomie.json` | `c68a60f` |
| 2 | Kern `src/spieloekonomie.py` (Achsen, Preise, Vergabe) | `a50edd6` |
| 3 | lokale Lager + Transportbuchung (Karrenpflicht) | `40` |
| 4 | Warenrezepte + lokale Ausbildung | `e6fd766`, `3bdbc6a` |
| 5 | Spieluhr `ort_tick`, `fensterproduktion` | `319c16b`, `a83ec25` |
| 6 | Forschung je Siedlung (`forschung_start`, `forschung_abschluss`) | `1d64cd6`, `c590951` |
| 7 | `zielstatus` (Zielprüfung + Haltefenster 24 h) | `a2b6531`, `eee604e` |
| **8a** | `botkern.oekonomie_kartenwahl`, `oekonomie_angebot` | `3785b5d` |
| **8b** | **Handels-Paar + Prüfdatei ← nächster Schritt** | offen |
| 9 | `main`-Anbindung + Migration | offen |
| 10 | `tick_bis` + **Aktivierung** | offen |

**Zustand im Spiel:** der **Altmodus läuft unverändert** — nichts im Spiel ruft `src/spieloekonomie.py`
auf. Das ist Zusage und wird von Prüfdateien mitgeprüft. Prüfzahlen je Schritt: `test_oekonomie_uhr`
42 · `test_lokale_forschung` 47 · `test_versorgungsziel` 69 · `test_oekonomie_kern_unabhaengig` 158 ·
`test_lokale_lager` 70 · `test_warentransport` 45 · `test_warenrezepte` 26 · `test_ausbildungsauftraege`
49 · `test_spieloekonomie` 370 · `test_botkern` 90.

## 4. Arbeitsweise (Vorgabe Daniel — gilt unverändert)

Nach **jedem** Schritt: betroffener **Einzeltest** + **einmal Sammellauf** (keine Spielprozesse offen
lassen), **eine Protokollzeile** in `docs/ENTWICKLUNGSPROTOKOLL.md` (Zeit mit `date`), dann
`python tools/protokoll_sichern.py --protokoll`, **kleiner Commit**. **Prüfende Unteragenten erst
NACH dem Commit.** Handbuch gewinnt bei Widerspruch (Zitat + Zeilennummer belegen). Berührt ein
Schritt eine **belegte** Handbuchregel: erst lesen, dann ändern.

## 5. Teuer gelernte Fallen (nicht wiederholen)

| Falle | Regel |
|---|---|
| `git add -A` | **Nie** vor der Kinderprüfung — sonst wandern ungeprüfte Dateien in den Commit. `git status --short` muss genau die erwarteten neuen Dateien zeigen. |
| Kindberichte | sind **Selbstauskunft**: ERGEBNIS-Zahl selbst nachfahren, Wachen-Namen überfliegen, erst dann committen. |
| Kinder parallel zum Sammellauf | stören ihn — nicht gleichzeitig laufen lassen. |
| `.exe`-Bau | währenddessen **kein** Spiel starten. Nach dem Bau: Startprüfung aus einem **anderen** Ordner. |
| `run_tests.bat` hat CRLF | `sed -i` findet dort **nichts** (still, exit 1) → `patch`-Werkzeug benutzen, danach mit `grep -o` prüfen. |
| Prüfmodule | führen sich beim `import` **aus** (`sys.exit(bericht())`) — Helfer nur über `try: import … / except SystemExit: sys.modules[…]` holen. |
| `src/botkern.py` | muss **reines ASCII** bleiben (Prüfung „reines ASCII"); `—` bricht sie. |
| `docs/PROJEKT_STAND.md`, Abschnitt „Der EINE nächste Schritt" | darf **kein `###`** enthalten (`test_zieluebergabe`) → Zwischentitel als `**Fett**`. |
| Prüf-Fehler ≠ Ausreißer | ein „Umgebungs-Ausreißer" der ersten Prüfdatei war in Wahrheit eine zu lockere Prüfung (Haus auf unerlaubtem Feld) — erst nachsehen, dann abtun. |
| Messfehler zuerst bei sich suchen | zwei „Fehler" in Schritt 7 waren **Datensatzfehler** (Verbrauch in nur einem Ort; Produktion nur bis zur Startzeit), nicht Code. |
| Kinderarbeit | nur `deepseek-flash`; Kindberichte sind kein Beweis. |

## 6. Nicht erneut zu prüfen (Beleg + Datum)

* Schritte **0–8a** — Commits und Prüfzahlen in Abschnitt 3 + Tabelle in `PROJEKT_STAND.md` 0c.
* `test_baseline` ist seit **18:17 deterministisch** (Haus wird jetzt auf ein erlaubtes Feld gesetzt;
  dreimal 40/0/0 belegt, seither kein Ausreißer).
* Die `.exe` startet (**19:35** aus anderem Ordner, Titel + 0 Fehlerberichte + 0 offene Prozesse).
* Der Sammellauf wird **nur nach einer echten Änderung an `src/`** wiederholt (nicht nach Dokument-Commits).
* Fehlend von Schritt 8a: Prüfdatei `tests/test_bot_oekonomie.py` und Audit `docs/audits/pruefung_schritt8.md`
  — die zwei prüfenden Kinder wurden für die saubere Übergabe **gestoppt, bevor sie Dateien anlegten**
  (Auftragstext steht in Protokollzeile **53**, in Sekunden neu auslösbar).

## 7. Offene Entscheidungen für Daniel (nichts eigenmächtig geändert)

1. **Kampfverluste verdrahten** — Handbuchregel wörtlich (S. 23: Verlierer verliert einen Teil seiner
   Karren/Belagerungswaffen, Fluchtchance 40 % + 5 % je Sequenz; unentschieden kostet nichts); `src/kampf.py`
   hat sie **gebaut**, es fehlt die Anbindung. Offene Frage: **Prozent-Untergrenze oder nur Simulation?**
   → `docs/ENTWURF_KAMPFVERLUSTE.md`.
2. **Forschungsstufe global oder je Siedlung?** Handbuch **schweigt**; Bibliothek/Auftrag/Sperre belegt je
   Siedlung → `docs/audits/belege_forschung_je_siedlung.md` (V1/V2/V3).
3. **Reserve-Anzeige** in `zielstatus` (`bool(orte)`) ist gekennzeichneter **VORSCHLAG**, ändert den Sieg nicht.
4. **Skill-Kopie im Profil `coding` veraltet** (4.589 Byte vom 04.10. gegen 38 KB in `default`) — nur auf
   Daniels Wort nachziehen.
5. **Kostendeckel heute überschritten** (siehe Abschnitt 1).

## 8. Wo die Details liegen (nur bei Bedarf lesen)

* Handbuch (Wahrheit): `docs/original/Spielanleitung_2009_Textfassung.txt`
* Ökonomie-Entwurf (die Vorgabe in 10 Schritten): `docs/audits/entwurf_spieloekonomie_sol_2026-10-05.txt`
* Handbuch-Abgleich: `docs/audits/handbuch_abgleich_2026-10-05.txt`
* Audits je Schritt: `docs/audits/pruefung_schritt3_4.md`, `…_schritt5.md`, `…_schritt6.md`, `…_schritt7.md`
* Stand/Historie: `docs/PROJEKT_STAND.md` (0c Tabelle, 0e Übergabe) · `docs/ENTWICKLUNGSPROTOKOLL.md`
* Werkzeuge: `tools/zieluebergabe.py` · `tools/protokoll_sichern.py` · `tools/build_exe.py`
* Sammellauf: `C:\Users\saras\AppData\Local\hermes\cache\scratch\sammellauf.py` (liest `run_tests.bat`)
