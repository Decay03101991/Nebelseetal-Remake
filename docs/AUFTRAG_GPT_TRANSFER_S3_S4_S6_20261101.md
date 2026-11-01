# AUFTRAG 9 an das Chat-Modell — Transfer zwischen Dörfern (S-3, S-4, S-6) auf dem gemessenen Stand

**Datum:** 01.11.2026, 19:30. **Rolle:** externe Entwurfsarbeit, ausschließlich Papier. **Adressat:** Daniels
Chat-Modell. **Umsetzung:** Weltenfresser/Hermes nach Gegenprüfung.

**Arbeitsstand, auf den sich dieser Auftrag bezieht:** `D:\Arbeiten\Nebelseetal_Remake`, Branch `main`,
Kopf `22530a3`; der Arbeitsbaum enthält zusätzlich die Änderungen für die leere Demo (Register 101), die im
selben Commit liegen. Der öffentliche GitHub-Stand (`954097aa`) ist **älter** und für keine Aussage über den
Code zu gebrauchen.

## 0. Pflichtabschnitt — was du nicht tust

1. **Kein Code, kein Patch, kein Commit, kein Push.** Du lieferst ein Papier.
2. **Keine Zahl ohne Quelle.** Jede Zahl trägt die Stelle, aus der sie stammt (Datei, Feld, Zeile oder
   Registernummer). Was du nicht weißt, schreibst du `UNBEKANNT — Hermes messen` und rätst nicht.
3. **Keine zweite Wahrheit.** Wo im Projekt bereits eine Funktion, ein Datenfeld oder eine Entscheidung
   existiert, benennst du sie und baust darauf — du erfindest keine Parallelstruktur.
4. **Kein Umbau des Speicherformats.** Neue Felder nur additiv und mit Vorgabewert, damit alte Spielstände
   ohne Migration laden. Eine Umbenennung bestehender Felder ist ausgeschlossen.
5. **Kein Balancing-Vorschlag ohne Rechnung.** Preise und Dauern nur als VORSCHLAG mit nachvollziehbarer
   Herleitung.
6. **Nichts über Veröffentlichung.** Das Online-Repository, die README, die Release-Texte und die
   GitHub-Präsentation sind **nicht** Teil dieses Auftrags (siehe Abschnitt 6).
7. Sprache Deutsch, Tabellen statt Fließtext, keine Emojis.

## 1. Gemessener Ist-Stand (jede Zeile ist am Code geprüft)

| Gegenstand | Stand | Beleg |
|---|---|---|
| Siedlungen | bis zu sechs Dörfer; jede Siedlung ist ein eigener Ort mit eigener Karte, eigenen Vorräten, eigenen Gebäuden und eigenen Einheiten | `Settlement` in `src/main.py` (`vorraete`, `bauten`, `stufen`, `einheiten`, `karte`) |
| Aktives Dorf | `GameState.aktive_siedlung_id` bestimmt, welches Dorf die Oberfläche zeigt | `src/main.py` |
| Forschung startet IM Dorf | `spieloekonomie.forschung_start(ort, gebiet, wissen, jetzt, weitere_orte)` prüft die Bibliotheksstufe **dieses** Ortes, bezahlt aus **dessen** Lager und setzt `ort["forschungsauftrag"]` | `src/spieloekonomie.py` |
| Forschung wird REICHSWEIT gelernt | `forschung_abschluss(ort, wissen, jetzt)` gibt `(ort, wissen)` zurück und hebt die Stufe in der **einen** Wissenskarte `wissen` — nicht im Ort | `src/spieloekonomie.py` |
| Doppelforschung gesperrt | dieselbe Zielstufe darf nicht gleichzeitig in zwei Dörfern laufen (Meldung nennt den Grund) | `forschung_start`, Parameter `weitere_orte` |
| Wissensstände lesen | `GameState.forschungs_stufen()` ist die EINE Lesestelle `{Gebiet: Stufe}` | `src/main.py` |
| Einheiten stehen IM Dorf | `Settlement.einheiten`; Ausbildung braucht die passende Ausbildungsstätte **dieses** Dorfes | `src/main.py`, `data/buildings.json` |
| Ausbildungsstätten | drei: Kriegerakademie (9 Einheiten), Diebesgilde (6), Stellmacher (13) = 28 Einheiten | `data/units.json` Feld `gebaeude` |
| Aufträge und Wege | `auftraege.starten(..., quelle_id)` bucht Abgang und Heimkehr im **Ort**, `kampf_am_ziel` ist der EINE Kampfweg | `src/auftraege.py`, Register 67 |
| Portal und Weltensprung | 20 Weltkarten, Start Midgard; Sprung kostet heute **5.000 Mana** (`portalraum._MANA_WECHSEL`), gesperrt solange etwas unterwegs ist, danach **24 Stunden** Sperre; die 5.000 sind der belegte Originalwert für einen *Koordinatenwechsel* | `src/portalraum.py`, `src/main.py` `_portal_wechsel` |
| Weltkarten-Gelände | seit S-5 gebaut: sieben Geländearten in 2×2-Blöcken, stabiler Seed je Welt (`weltkarten_seed`) — **reine Anzeige, keine Ertragswirkung** | Register 91, `portalraum.weltbild` |
| Dorfzentrum | kostenlos mit jeder Gründung, Platz wählt der Spieler, ein Dorfzentrum je Dorf, nicht abreißbar | Register 89/90 |

**Bereits entschieden und daher NICHT mehr zu fragen** (Register 92–99, 101):

| # | Entscheidung |
|---|---|
| 92 | S-5 ist freigegeben und gebaut |
| 93 | **Weltensprung kostet 500 Mana plus 100 Gold**; die 5.000 bleiben als belegter Originalwert stehen |
| 94 | `weltkarten_seed` ist ein fester Konfigurationswert |
| 95/96/97 | „Demo“ steht im Titel; Handbuch-Release erst nach S-5; Handbuch als eigene Datei |
| 98 | Limbus bleibt Weltname, die Ebene heißt „der magische Limbus“ |
| 99 | Die Demo wird ein möglichst weit umgesetztes **Testspiel**; Funktionen gehen vor Release-Texten |
| 101 | Die Demo wird **leer** ausgeliefert (kein Spielstand im Paket, eigener Demo-Speicherordner) |

## 2. Die Aufgabe — drei Schnitte, ein zusammenhängendes Papier

Der Anlass: `docs/design/VERBUND_FORSCHUNG_EINHEITEN_TRANSFER_20261101.md` (ein früheres Papier desselben
Modells) entwirft S-3, S-4 und S-6, konnte aber **13 Punkte nicht am Code messen** und stellt acht
Entscheidungen (Q-01 bis Q-08). Die Messungen aus Abschnitt 1 und die Entscheidungen aus Abschnitt 1b
liegen jetzt vor. Deine Aufgabe ist **kein neues Papier von vorn**, sondern die **baureife Fassung** auf
dieser Grundlage.

### S-3 — Forschungsübernahme zwischen Dörfern

Der gemessene Zustand ist bereits ein Verbund: **bezahlt wird im Dorf, gelernt wird reichsweit.** Zu klären:

1. Ist das die gewollte Regel, oder soll Wissen künftig am Dorf hängen (dann braucht es einen
   Übernahmeweg und eine Regel, was bei Abriss oder Verlust eines Dorfes mit seinem Wissen passiert)?
2. Was passiert bei Abriss der Bibliothek, aus der geforscht wurde — bleibt das Gelernte?
3. Wie wird ein **laufender** Forschungsauftrag behandelt, wenn das Dorf transferiert wird (S-6)?
4. Welche Anzeige sagt dem Spieler, wo er forscht und wo das Ergebnis gilt?
5. Wie verhindert die Regel doppelte Zahlungen, ohne zwei Dörfer unnötig zu blockieren?

### S-4 — Einheiten-Übernahme zwischen Dörfern

Heute stehen Einheiten im Dorf und bewegen sich nur über Aufträge. Zu entwerfen ist der Weg, Einheiten
**ohne Kampfauftrag** von einem eigenen Dorf ins andere zu bringen:

1. Ablauf (Ziel wählen, Trupp wählen, Dauer, Kosten, Ankunft).
2. Gilt die Wegzeit- und Temporegel der Aufträge (langsamste Einheit bestimmt das Tempo, Rückweg gleich
   lang) oder eine eigene?
3. Was ist gesperrt: laufende Aufträge, blockierte Dörfer, ein Dorf auf einer anderen Weltkarte?
4. Was passiert mit Ausrüstung, Karrenladung und Siedlern beim Übertragen?
5. Abweisungen mit Grund und nächstem Schritt — je ein Satz, den der Spieler lesen kann.

### S-6 — Dorftransfer auf eine andere Weltkarte

Der Weltensprung ist gebaut (`_portal_wechsel`), der **Dorfumzug** nicht. Zu entwerfen:

1. Was zieht mit (Gebäude, Vorräte, Einheiten, Forschung, offene Aufträge) und was bleibt zurück?
2. Kosten: 500 Mana plus 100 Gold (Register 93) — aus welchem Lager, je Dorf oder je Umzug?
3. Sperren: laufende Aufträge, offene Baufelder, offenes Dorfzentrum (`dorfzentrum_offen`), Götterschutz.
4. Der Spieler wählt das Zielfeld auf der Weltkarte (Klick ist bereits verdrahtet,
   `_portal_feld_waehlen` bucht heute nichts).
5. Was passiert, wenn das Zielfeld belegt ist oder die Welt nicht bespielbar ist?
6. Bleibt die 24-Stunden-Sperre nach einem Weltensprung bestehen — für den umziehenden Spieler, für das
   Dorf oder für beide?

## 3. Randbedingungen für jeden Entwurf

- **Eine Quelle je Zahl.** Preise, Dauern, Stufen: immer aus `data/*.json` oder einer benannten Funktion.
- **Additive Datenfelder** mit Vorgabewert; alte Spielstände müssen ohne Migration laden.
- **Der Kern rechnet, die Anzeige liest.** Keine zweite Rechenstelle für dieselbe Größe
  (Muster: `spieloekonomie` rechnet, `main` zeigt).
- **Zeit ist Spielzeit** (`state.spielsekunden`), nie Rechnerzeit.
- **Jede Abweisung nennt drei Dinge:** Aktion abgelehnt, Grund, nächster Schritt.
- **Grenzfälle sind Pflicht:** −1 / exakt 0 / exakt Soll / +1 für Betrag, Anzahl, Zeit und Entfernung.
- **Prüffälle ohne Fenster** sind möglich; jeder Schnitt bekommt eine eigene Prüfdatei (Vorschlag für
  Namen), die das Papier mitliefert.
- **ASCII-Regel:** Prüfdateien im Projekt sind reines ASCII (`ae/oe/ue`), Umlaute nur in Anzeigetexten.

## 4. Was du liefern sollst

| Teil | Inhalt |
|---|---|
| A | Ein Papier mit drei Abschnitten (S-3, S-4, S-6), je: Ablauf in Schritten, beteiligte Funktionen mit Namen, Datenfelder (additiv), Kosten mit Quelle, Sperren, Abweisungstexte, Anzeige |
| B | Eine Tabelle der Prüffälle je Schnitt: mindestens zehn, davon vier Grenzfälle, jeder mit Erwartung |
| C | Eine Liste der Stellen, die du **nicht** beurteilen konntest (`UNBEKANNT`), mit dem Befehl, mit dem Hermes es misst |
| D | Höchstens acht offene Entscheidungen für Daniel, je mit Empfehlung zuerst, Alternative und Folge |
| E | Ein Absatz „Was ich am bestehenden Verbund-Papier geändert habe und warum“ — mit Verweis auf Q-01 bis Q-08 (welche durch die Messungen beantwortet sind, welche offen bleiben) |

## 5. Prüfmaßstab, an dem dein Papier gemessen wird

1. Jede Zahl hat eine Quelle aus diesem Auftrag oder aus dem Projekt; keine erfundene Zahl.
2. Kein Vorschlag widerspricht einer Entscheidung aus Register 92–101.
3. Kein Vorschlag erzeugt eine zweite Rechen- oder Speicherwahrheit.
4. Jeder Schnitt ist so beschrieben, dass eine Sitzung ihn **ohne Rückfrage** bauen kann.
5. Die Prüffälle decken Grenzfälle ab und prüfen auch, was **nicht** passieren darf.
6. Wo du etwas nicht weißt, steht `UNBEKANNT` statt einer plausiblen Zahl.

## 6. Was ausdrücklich NICHT Teil dieses Auftrags ist

- **Die GitHub-/Online-Präsentation.** Dazu liegt ein externes Feedback vom 01.11.2026 vor (31.499 Byte,
  SHA256 `dff01476…`), abgelegt unter `archiv/eingaben/20261101_github_feedback/` und eingeordnet in
  `docs/EXTERNES_FEEDBACK_GITHUB_20261101.md` (Register 102). Es betrifft **nur** das Online-Repo, ist
  reines Feedback mit Vorschlägen vor der Demo-Veröffentlichung und wird **nachrangig** behandelt.
  Nimm dazu nicht Stellung.
- Balancing-Zahlen für Kampf, Beute oder Bots (`docs/SPIELBALANCING_TEST.md` ist ein lebendes Dokument,
  Zahlen dort ersetzen, nicht ergänzen).
- Die Bot-Taktik (S-7): dafür liegt ein eigenes Paket vor, das gerade geprüft wird.
- Regeln, Skills oder Werkzeuge des Hermes-Systems.

## 7. Abgabe

Eine Datei, Markdown, deutsch, Tabellen. Kopf mit Auftragsnummer 9, Datum und dem Stand `22530a3`.
Wer eine Zahl nennt, nennt die Quelle. Wer etwas nicht weiß, schreibt es hin.
