# Externes Feedback zum öffentlichen GitHub-Stand — Ablage und Einordnung

**Gegenstand:** `Feedback_zum_Github_Nebelseetal_Online_Stand01.11.26-2.md`, 31.499 Byte,
SHA256 `dff014761b723af355ab69bd5e3d260af8657a45dc83fd6e3945c2a19854ec03`.
**Ablage:** `archiv/eingaben/20261101_github_feedback/` (Archiv, nicht im Git-Baum).
**Prüfdatum des Berichts:** 01.11.2026. **Adressat:** Hermes/Weltenfresser.
**Behandlung laut Bericht:** nachrangiger Ideen- und Qualitäts-Backlog, keine sofortige Umsetzung, kein
Push, kein Release, keine automatische Übernahme von Regeln oder Skills.

**Rang dieser Datei:** Sie ordnet den Bericht ein und verweist auf vorhandene Aufgaben. Sie ist **keine**
zweite führende Stand-Datei — führend bleiben `docs/AKTUELLER_STAND.md`, `docs/PRUEFREGEL_ORIGINAL.md`
und `docs/ENTWICKLUNGSPROTOKOLL.md`.

---

## 1. Was der Bericht am öffentlichen Stand gemessen hat

Der Bericht prüft ausschließlich den **öffentlichen** Stand (`Decay03101991/Nebelseetal-Remake`):
`main` auf dem FIX04j-Stand, Pre-Release `v0.4.0-test.1` vom 28.10.2026, offener PR #1 mit eigener
Wurzel, Actions ohne sichtbare Läufe. Den lokalen Arbeitsstand konnte er nicht sehen — er sagt das
selbst und ausdrücklich (Abschnitt 11 des Berichts).

Damit gilt für jeden Befund dieselbe Regel wie bei den früheren externen Prüfungen: **erst am heutigen
Code nachmessen, dann übernehmen.** Ein Befund über den öffentlichen Stand ist kein Befund über `HEAD`.

Die positive Bewertung, die erhalten bleiben soll (POS-01 bis POS-09), deckt sich mit dem, was im Projekt
ohnehin gilt: getrennter öffentlicher Einstieg (`src/public_start.py`) und getrennter Bau
(`tools/build_public_exe.py`), eigenes Infopaket in `release_vorlage/`, Prüfsummen je Artefakt,
`.gitignore` für private Stände, `docs/ENTWICKLUNGSPROTOKOLL.md` als führende Chronik.

---

## 2. Freigabe-Gates einer Demo (übernommen, verdichtet)

Der Bericht schlägt sieben Gates vor. Sie werden hier festgehalten, weil sie zur Demo-Freigabe gehören —
**kein neuer Steuermechanismus**, sondern die Prüfliste vor dem Upload:

| Gate | Muss vor dem Upload belegt sein |
|---|---|
| G-01 Versionswahrheit | Version, Release-Tag und geprüfter Quell-Commit passen zusammen; keine ungeklärten divergierenden Branch-Wahrheiten |
| G-02 Spielbarkeit | Frischer Spielerstart ohne Admin, Grundaufbau, Speichern/Laden, eine in sich schlüssige Spielrunde |
| G-03 EXE-Abnahme | Öffentliche EXE **aus dem entpackten ZIP** auf Windows gestartet, Hauptwege geprüft, Fehler dokumentiert |
| G-04 Artefakte | ZIP enthält genau die vorgesehenen Dateien; SHA-256 für ZIP **und** EXE getrennt, nach dem Upload zurückgelesen |
| G-05 Keine Privatdaten | Paket auf Zugänge, Spielstände, PII und absolute private Pfade geprüft |
| G-06 Verständlichkeit | README, Release-Notizen, bekannte Grenzen, Startanleitung und Build widersprechen sich nicht |
| G-07 Nutzerentscheidung | Daniel bestätigt ausdrücklich die Veröffentlichung **dieser** Fassung |

**G-05 ist seit 01.11.2026 technisch untersetzt:** `tools/build_public_exe.py` bricht den Bau ab, wenn in
`data/` oder `assets/` ein Spielstand, ein Admin-Teststand, das Passworttor oder eine Sperrdatei liegt
(Register 101), und die Demo hat einen eigenen, nie benutzten Speicherordner. Prüfdatei
`tests/test_demo_leer.py`.

---

## 3. Backlog — aufgenommen, nachrangig, ohne Verdrängung

Reihenfolge wie im Bericht vorgeschlagen. „Vorhanden“ heißt: es gibt dazu bereits eine Stelle im Projekt,
der Punkt wird dort geführt und **nicht** doppelt angelegt.

| Nr. | Punkt | Bezug im Projekt | Zeitpunkt |
|---:|---|---|---|
| 1 | Versionswahrheit in README, Release und Branchstatus herstellen (GH-01/05, REL-03) | `README.md`, `docs/RELEASE_PUBLIC_FIX04j.md` | vor der Demo-Ankündigung |
| 2 | Hommage und Eigenentwicklung klar beschreiben (GH-02/09) | `README.md`, Textpaket H-01/G-01 (geprüft, `docs/audits/PRUEFVERMERK_GPT_TEXTPAKET_20261101.md`) | vor der Neupositionierung |
| 3 | Download prominent verlinken (GH-04) | `README.md` | mit der Demo-Vorbereitung |
| 4 | ZIP- und EXE-Hashes eindeutig beschriften (REL-01) | `release_vorlage/`, `tools/build_public_exe.py` | nächste Release-Notizen |
| 5 | Echte aktuelle Screenshots (GH-03/11, MED-01 bis MED-04) | `docs/BILDINVENTAR.md` | wenn die Demo-Ansichten stabil sind |
| 6 | Release-ZIP entpackt prüfen, Hashes zurücklesen (REL-04/10) | Gate G-03/G-04 | konkretes Freigabe-Gate |
| 7 | Spieler-README von Entwicklertext entlasten (GH-06/08) | `README.md`, `docs/` | wenn die Texte stehen |
| 8 | Branch- und Merge-Strategie bewusst klären (STR-01/02) | offener PR #1, eigene Wurzel | vor einem größeren GitHub-Wechsel |
| 9 | Community-Credits und Quellverweise (FAN-01/02) | `docs/BILDINVENTAR.md` | ohne Feature-Arbeit zu verdrängen |
| 10 | Fehlerformular (REL-09) | `release_vorlage/FEHLER_MELDEN.txt` | vor ersten externen Testern |
| 11 | Projektnavigation, alte Ordner kontrolliert (GH-07, STR-04) | Repo-Wurzel | später |
| 12 | Lizenz für den eigenen Code (STR-10) | — | **Entscheidung Daniel** |
| 13 | Optionaler manueller CI-Nachweis (REL-05) | `.github/workflows/` | nach der Demo |
| 14 | Optional Spielvideo/Galerie (MED-09) | — | nach stabilem Demo-Gameplay |

**Nicht aufgenommen als eigene Aufgabe**, weil bereits gedeckt: Release-Checkliste, öffentliche
Bau-Routine, Bildinventar, Textpaket (H-/R-/G-Texte) und die Wiedergabe der Demo-Grenzen.

---

## 4. Was ausdrücklich NICHT umgesetzt wird

Aus dem Bericht Abschnitt 10, hier als bindende Grenze für spätere Sitzungen:

- keine neuen Spielmechaniken **nur** für eine schönere GitHub-Seite;
- keine massenhafte Entfernung historischer Bilder oder Dokumente;
- kein Löschen der Admin-Module aus dem Repo (der getrennte Einstieg ist die Schutzgrenze);
- kein Merge des PR #1 mit unabhängigen Historien ohne Prüfung;
- keine neue Projektstruktur, kein neues Framework, kein zusätzlicher Dienst für optische Aufgaben;
- kein Push und kein Release aufgrund dieses Berichts.

**Zwei Punkte bleiben bei Daniel und werden nicht vom Agenten entschieden:** eine Lizenz für den eigenen
Code (STR-10) und die rechtliche Einordnung der historischen Grafiken (FAN-03/04). Festgehalten wird nur,
was Daniel selbst gesagt hat: die Grafiken stammen überwiegend aus öffentlich zugänglichen Fan- und
Spielerquellen und gelten nach seiner Angabe als zur Nutzung freigegeben; der Code ist eigenständig.
