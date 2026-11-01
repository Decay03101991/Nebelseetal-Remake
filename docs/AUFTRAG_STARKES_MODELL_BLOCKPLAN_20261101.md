# Blockplan für das starke Modell — `deepseek-v4-pro`, acht Blöcke, rund 4 USD

**Datum:** 01.11.2026, 20:15. **Kopf des Arbeitsbaums:** `6888aa3`. **Projekt:** `D:\Arbeiten\Nebelseetal_Remake`,
Branch `main`. **Remote:** `954097aa` — absichtlich alt, **nicht pushen**.

**Daniels Auftrag, wörtlich (01.11.2026, 19:50):** „ich will das du ein rießen arbeitspaket für das schwere
starke model von deepseek vorbereitest das für uns sehr sehr viel Balancen Abgleichen und Spieltesten und
bewerten soll und lass es große teile der offenen aufgaben übernehmen und am besten auch umsetzen. Ich
empfehle mehrere blöcke in auftrag zu geben die insgesamt ein deepseek guthaben von 4 USD nutzen sollen …
Stelle dem großen model alle wichtigen pfade zur verfügung die es benötigt damit es nicht suchen muss und
plane die aufträge kontext orientiert so das es klug ist und wir maximal davon profitieren.“

**Kontostand bei Erstellung:** 11,60 USD (Daniel hat 10 EUR aufgeladen). Der Plan verbraucht davon rund
**4,00 USD**, danach bleiben ~7,6 USD Reserve.

---

## 0. Rolle des starken Modells und Grenzen

| Punkt | Regel |
|---|---|
| Rolle | **Umsetzer und Messingenieur** — kein Berater. Es baut, misst, prüft selbst und berichtet mit Zahlen. |
| Erlaubt | Dateien im Projekt ändern (nur die je Block genannten), neue Prüfdateien anlegen, Werkzeuge unter `tools/` schreiben, `python -X utf8`-Läufe, `git status`/`git diff` **lesen** |
| Verboten | `git add/commit/push` (macht Hermes), Dateien außerhalb des Projekts, `docs/PRUEFREGEL_ORIGINAL.md`/`docs/ENTWICKLUNGSPROTOKOLL.md`/`docs/AKTUELLER_STAND.md` schreiben, Daten in `data/` ohne Beleg ändern, Kennungen umbenennen, Felder im Spielstand entfernen, Zahlen erfinden |
| Pflicht am Ende jedes Blocks | **voller Sammellauf** (`python -X utf8 -u tools/sammellauf.py`), Ergebnis in den Bericht, und „FERTIG <Datei> <Zeilen>“ als letzte Zeile |
| Bei rotem Sammellauf | **zurücknehmen statt passend biegen** — alte Wachen werden umbenannt, nie gelöscht, und die Entscheidung steht als Satz im Kommentar |
| Zeitbasis | immer `state.spielsekunden`, nie Rechnerzeit |
| Prüfdateien | reines ASCII (`# -*- coding: ascii -*-`), Umlaute nur als `ae/oe/ue`; Anzeigetexte dürfen Umlaute haben |
| Sprache | Deutsch, Tabellen, keine Emojis |

---

## 1. Pfad-Register (damit das Modell nicht suchen muss)

| Pfad | Was dort steht | Wofür im Block |
|---|---|---|
| `src/main.py` | Einstieg + GUI, `GameState` (ab ~Z. 830), `NebelseetalApp` (ab ~Z. 3000), `_render_portal`, `_portal_wechsel`, `_bau_pruefen`, `_erste_siedlung_gruenden`, `_dorfzentrum_setzen` | B3, B5, B6 |
| `src/spieloekonomie.py` | Kern: `ort_tick`, `forschung_start`, `forschung_abschluss`, `ausbildung_start`, `ware_start`, `transport_start`, `handel_start`, `tagesbedarf_nahrung` | B1, B4 |
| `src/auftraege.py` | Aufträge, Wege, `starten(..., quelle_id)`, `laufende()`, `ladung_der_mission` | B5, B6 |
| `src/kampf.py` | `fuehre_schlacht` (die EINE Kampffunktion) | B2, B7 |
| `src/kampfbericht.py` | `beute_am_ziel`, `beute_staffel` (die EINE Beuterechnung) | B2 |
| `src/portalraum.py` | Weltkarten, `weltbild`, `wechsel_erlaubt`, `nach_wechsel`, `_MANA_WECHSEL` | B6 |
| `src/botkern.py` | Bot-Wirtschaft, `BOT_NAMEN`, `bot_punkte` | B3 |
| `src/bottaktik.py` | Zustandsautomat mit acht Zuständen und fünf Taktiken — **nicht angeschlossen** | B3 |
| `src/punkte.py` | `spielausgang`, `auszeichnungen`, `handelspunkte` | B7 |
| `src/einheiten.py` | Rollen, AT/SK, Ladung, `ladung_der_gruppe` | B2, B5 |
| `src/gelaende.py` | Gelände, `finde_gebaeude` (Kennung + Name + `alias`), `bau_moeglich` (liefert **Tupel**) | B5 |
| `src/gebaeude_wirkung.py` | Erträge je Gebäude/Gelände, `bibliothek_stufe`, Ausbildungsstätten | B1 |
| `src/forschungspfad.py` | Voraussetzungen der 21 Forschungen | B4 |
| `src/spielstaende.py` | drei Speicherslots, `slot_status`, `altstand_pfad` | B6 |
| `src/public_start.py` | Demo-Einstieg, eigener Speicherordner `…\Nebelseetal_Remake\Demo` | B8 |
| `data/*.json` | `buildings.json`, `units.json`, `items.json`, `research.json`, `gelaende.json`, `welten.json`, `baupreise.json`, `nahrungsverbrauch.json`, `karrenkapazitaet.json`, `gebaeude_wirkung.json`, `spieloekonomie.json`, `spielzeit.json` | alle Blöcke |
| `tests/harness.py` | `check(name, cond, detail)`, `befund(name, detail)`, `abschnitt(titel)`, `ausnahme(name, fn)`, `bericht()` — **`bericht()` nimmt KEIN Argument** | alle Prüfungen |
| `tests/test_produktionskette_ohne_cheats.py` | Muster für eine E2E-Kette ohne gesetzte Zustände | B7 |
| `tests/test_weltbild_gelaende.py` | Muster für die jüngste Prüfdatei (S-5) | alle |
| `tools/sammellauf.py` | voller Prüflauf, schreibt `docs/audits/sammellauf_<TS>.log` | Abnahme |
| `tools/balancing_messung.py`, `tools/balancing_karten.py` | vorhandene Messwerkzeuge (Erträge, Einheiten, Schlachten, Beute, Reise) | B1, B2, B7 |
| `tools/build_exe.py`, `tools/build_public_exe.py` | Entwickler- und Demo-EXE (Demo prüft Spielstände im Paket) | B8 |
| `docs/PRUEFREGEL_ORIGINAL.md` | **102 Punkte**, je mit Quelle und Urteil — hier steht, was belegt ist | alle (nur lesen) |
| `docs/SPIELBALANCING_TEST.md` | lebendes Balance-Dokument (Zahlen ersetzen, Datum im Kopf ändern) | B7 |
| `docs/audits/PRUEFVERMERK_S7_S8_ENTWURF_20261101.md` | Mana-Bilanz am Code gemessen, Reiseformeln, F-01…F-05 offen | B3, B7 |
| `docs/design/VERBUND_FORSCHUNG_EINHEITEN_TRANSFER_20261101.md` | Verbund-Papier mit Q-01…Q-08 | B4 |
| `docs/AUFTRAG_GPT_TRANSFER_S3_S4_S6_20261101.md` | mein Auftrag 9 an das Chat-Modell | B4, B5, B6 |
| `archiv/eingaben/20261101_gpt_antworten/AUFTRAG_9_TRANSFER_S3_S4_S6_ENTWURF_22530a3_20261101.md` | **Antwort** von Auftrag 9 (42.447 Byte) — Entwurf, nicht Beleg | B4, B5, B6 |
| `archiv/eingaben/20261101_gpt_antworten/GPT_Taktikpaket_HERMES_ENTWURF_BOTVERHALTEN_TAKTIKPAKETE_20261101.md` | Taktikpaket (47.159 Byte) — Entwurf, nicht Beleg | B3 |
| `docs/EXTERNES_FEEDBACK_GITHUB_20261101.md` | Online-Repo-Backlog + Gates G-01…G-07 | B8 (nur lesen) |
| `docs/original/Nebelseetal_Spielanleitung_2009.pdf` + `docs/original/Spielanleitung_2005/` | Originalquellen (Handbuch 2009, Vorversion 2006 als Text) | B1, B2, B7 |

---

## 2. Die acht Blöcke

| # | Block | Art | Kosten (Schätzung) | Abhängig von |
|---:|---|---|---:|---|
| B1 | Wirtschaft messen (Erträge, Siedler, Gold, Mana) | Messwerkzeug + Bericht | 0,35–0,45 USD | — |
| B2 | Kampf messen (Wall, SK, Beute, 40 Läufe je Stufe) | Messwerkzeug + Bericht | 0,35–0,45 USD | B1 |
| B3 | S-7 Bots erlebbar (`bottaktik` anbinden) | **Umbau** | 0,60–0,75 USD | B1 |
| B4 | S-3 Forschungsverbund absichern | Umbau (klein) | 0,35–0,45 USD | B1 |
| B5 | S-4 Einheitenverlegung | **Umbau** | 0,50–0,65 USD | B4 |
| B6 | S-6 Dorftransfer | **Umbau** | 0,55–0,70 USD | B5 |
| B7 | Balance-Abgleich und Spielbarkeits-Kette | Messung + Doku | 0,45–0,55 USD | B1, B2, B3–B6 |
| B8 | Demo-Reifeprüfung (Gates G-01…G-07) | Prüfung + Bericht | 0,40–0,50 USD | alle |
| | **Summe** | | **3,55–4,50 USD** | |

### B1 — Wirtschaft messen (kein Umbau am Spiel)

**Ziel:** ein wiederverwendbares Messwerkzeug `tools/mess_wirtschaft.py`, das die Wirtschaft des Spiels
aus Daten und Kernfunktionen **rechnet** und einen Bericht schreibt.

**Muss messen:** Erträge je Gebäude und Gelände (gegen `data/buildings.json` und Handbuch 2009 S. 9–11),
Siedlerzuwachs und Siedlerdecke (10 + 5 je Haus, max. 6 Dörfer → 360), Goldfluss je Spieltag, Mana je
Spielstunde (Tempel 5 auf Nebelsee, 1 sonst, **0 auf Sumpf**, Götterkunde +5 %/Stufe), Nahrungsverbrauch
8 je Einheit und Spieltag, Waren- und Ausbildungsdauern.

**Muss prüfen (Abweichungen benennen, nicht glätten):** Werte in `data/` gegen `docs/original/` — jede
Abweichung mit Quelle und Urteil (BELEGT / WIDERSPRUCH / NICHT BELEGT / VORSCHLAG).

**Erlaubt:** neue Datei `tools/mess_wirtschaft.py`, neuer Bericht `docs/audits/MESS_WIRTSCHAFT_<datum>.md`.
**Verboten:** `src/` anfassen.
**Abnahme:** Werkzeug läuft mit `python -X utf8`, gibt je Kennzahl eine Zeile mit Quelle aus, Bericht nennt
drei Kernaussagen und **jede** Abweichung.

### B2 — Kampf messen (kein Umbau am Spiel)

**Ziel:** `tools/mess_kampf.py` — echte Schlachten über `kampf.fuehre_schlacht`, 40 Läufe je Wallstufe,
Beute über `kampfbericht.beute_am_ziel`, Reisekosten über die vorhandene Wegzeitfunktion.

**Muss messen:** Trefferquote/Verluste je Wallstufe 0…10, Schwellenverhalten (die Wallprüfung rechnet mit
**SK**, nicht mit AT — Register 54), Beute-Staffel 10/30/60/100 % **gegen die mitnehmbare Menge**
(Register: „gegen die MITNEHMBARE Menge rechnen“), Ladungsdeckel je Karrenart (40/100/250/1.000/2.500,
Wagenbau-Bonus +10 %/Stufe, Deckel Faktor 2,0).

**Erlaubt:** `tools/mess_kampf.py`, Bericht `docs/audits/MESS_KAMPF_<datum>.md`.
**Verboten:** `src/` anfassen, Zahlen in `data/` ändern.
**Abnahme:** 40 Läufe je Stufe sind im Bericht als Tabelle sichtbar; auffällige Ausreißer werden benannt,
nicht geglättet.

### B3 — S-7: Bots erlebbar machen (Umbau)

**Ziel:** `bottaktik` (Zustandsautomat, acht Zustände, fünf Taktiken, **heute nicht angeschlossen**) so
anbinden, dass Bots ein erkennbares Verhalten zeigen: Verhalten je Dorf, Volksattribute dauerhaft,
Verhaltensboni befristet, Umschalten mit Sperrzeit und Ankündigung — im Rahmen dessen, was das Taktikpaket
als umsetzbar belegt **und** was ohne neue Wahrheit in `botkern` passt.

**Muss beachten:** keine zweite Entscheidungs- oder Kampfwahrheit; `bot_punkte` bleibt
`(Krieg + Forschung) // 2`; Bots greifen in der Demo **nicht** an (Daniels Entscheidung, Register/Paper);
Spielzeit statt Rechnerzeit; Speicherformat nur additiv.

**Erlaubt:** `src/bottaktik.py`, `src/botkern.py`, `src/main.py` (nur Bot-Anzeige und Anbindung),
`data/bots*.json` (nur neue Felder mit Vorgabewert), neue Prüfdatei `tests/test_s7_botverhalten.py`.
**Abnahme:** neue Prüfdatei ≥ 40 Prüfungen grün, Nachbarn grün (`test_punkte`, `test_gpt_wall_bot_kampf`,
`test_kampf_botbeute_echte_kasse`), voller Sammellauf 0 rot, Bericht `docs/audits/BERICHT_S7_<datum>.md`.

### B4 — S-3 Forschungsverbund absichern (kleiner Umbau)

**Ziel:** die heute schon geltende Regel (bezahlt im Dorf, gelernt reichsweit) **absichern und anzeigen**:
Abriss einer Bibliothek mit laufender Forschung ablehnen, Dorfverlust blockieren, Transfer mit laufender
Forschung blockieren, Anzeige trennt Bibliotheksstufe und Verbundwissen.

**Erlaubt:** `src/spieloekonomie.py`, `src/main.py` (Anzeige, Abriss-Sperre), neue Prüfdatei
`tests/test_s3_forschungsverbund.py`.
**Abnahme:** Prüfdatei ≥ 30 grün inklusive Grenzfälle (−1/0/Soll/+1), Nachbar `test_forschung*` grün,
voller Sammellauf 0 rot.

### B5 — S-4 Einheitenverlegung (Umbau)

**Ziel:** Einheiten zwischen **eigenen** Dörfern verlegen, ohne Kampfauftrag: Ablauf, Dauer nach der
langsamsten Einheit, Rückweg gleich lang, Kosten aus dem Ortslager, Abweisung mit Grund und nächstem
Schritt. Verlegung blockiert einen Weltensprung genauso wie ein Auftrag.

**Erlaubt:** `src/auftraege.py`, `src/spieloekonomie.py`, `src/main.py` (Ansicht + Meldungen), neue
Prüfdatei `tests/test_s4_einheitenverlegung.py`.
**Abnahme:** Prüfdatei ≥ 35 grün, E2E-Fall (Einheit verlegen, ankommen, Bestand im Zielort) ohne gesetzte
Zustände, voller Sammellauf 0 rot.

### B6 — S-6 Dorftransfer auf eine andere Weltkarte (Umbau)

**Ziel:** ein Dorf springt auf eine andere Weltkarte: Zielfeld über die vorhandene Portalauswahl,
Kosten **500 Mana + 100 Gold** (Register 93 — der belegte Originalwert 5.000 bleibt als Konstante stehen,
der Spielwert kommt daneben), Sperren wie beim Weltensprung, kein Verlust von Gebäuden/Vorräten/Einheiten.

**Erlaubt:** `src/portalraum.py`, `src/main.py` (`_portal_wechsel`, `_portal_feld_waehlen`), `src/welt.py`,
`data/welten.json` (neuer Konfigurationswert), neue Prüfdatei `tests/test_s6_dorftransfer.py`.
**Abnahme:** Prüfdatei ≥ 40 grün inklusive „anderes Dorf bleibt unberührt“, „Sperre bei laufendem Auftrag“,
„genau einmal abgebucht“, Alter Spielstand lädt ohne Migration, voller Sammellauf 0 rot.

### B7 — Balance-Abgleich und Spielbarkeits-Kette

**Ziel:** die gemessenen Zahlen aus B1/B2 mit dem echten Spiel zusammenbringen: eine **Kette ohne Cheats**
(Rohstoff → Bibliothek → Forschung Baukunst → Ware → Ausrüstung → Ausbildung → Bewegung → Kampf →
Rückkehr → Speichern/Laden) fahren und die Gates G-1…G-6 aus `docs/SPIELBALANCING_TEST.md` neu beurteilen.

**Muss liefern:** aktualisiertes `docs/SPIELBALANCING_TEST.md` (Zahlen ersetzen, Datum im Kopf, Gates neu),
Bericht mit den drei größten Ungleichgewichten **mit Zahl und Quelle**, Liste der offenen Balance-Fragen an
Daniel (höchstens acht, Empfehlung zuerst).

**Verboten:** `data/`-Zahlen ohne Daniels Entscheidung ändern.
**Abnahme:** Kette nachweislich bis zum Kampf gefahren (Ausgabe im Bericht), Gates mit Urteil je Gate.

### B8 — Demo-Reifeprüfung (Gates G-01…G-07)

**Ziel:** prüfen, ob die Demo auslieferbar ist, ohne etwas zu veröffentlichen: Bau der Demo-EXE über
`tools/build_public_exe.py`, Prüfung, dass im Paket **kein Spielstand** liegt (Register 101), ZIP entpacken,
EXE aus dem entpackten ZIP starten (getrennte Vordergrundaufrufe, PID + Fenstertitel + Fensterhandle als
Beleg), Hashes für ZIP **und** EXE getrennt auslesen, danach Gates beurteilen.

**Muss liefern:** `docs/audits/DEMO_REIFEPRUEFUNG_<datum>.md` mit einer Zeile je Gate (erfüllt / offen /
blockiert + Beleg), den gemessenen Hashes und einer klaren Aussage, was vor einem Upload noch fehlt.
**Verboten:** hochladen, pushen, Release anlegen, „Demo“ im Titel einer öffentlichen Seite.
**Abnahme:** Bericht mit sieben Gate-Zeilen, keinen erfundenen Werten, EXE-Start belegt.

---

## 3. Reihenfolge und Budget

1. **B1 → B2** (Messblöcke, kein Risiko, liefern die Zahlen für alles Weitere)
2. **B3** (Bots — größter Erlebnisgewinn, hängt nur an B1)
3. **B4 → B5 → B6** (Transfer-Kette, baut aufeinander auf)
4. **B7** (Balance, braucht die Umbauten)
5. **B8** (Demo-Reife, braucht alles)

Nach **jedem** Block: Hermes prüft, committet oder nimmt zurück, trägt Kosten ein. Bricht ein Block ab,
wird der nächste nicht gestartet, bevor der Zustand geklärt ist.

**Budget-Wache:** nach jedem Block den gemessenen Verbrauch aus der `usage_*.json` gegen die Schätzung
stellen und in `docs/ENTWICKLUNGSPROTOKOLL.md` eintragen. Ist die Summe bei 3,00 USD erreicht, wird
**angehalten** und Daniel gefragt, bevor Block B7/B8 startet.

---

## 4. Laufverfahren (Hermes, je Block)

```bash
cd D:/Arbeiten/Nebelseetal_Remake && env -u HERMES_SESSION_ID -u HERMES_SESSION_KEY \
  -u HERMES_GATEWAY_SESSION hermes -z "Lies zuerst vollstaendig <paketdatei> und fuehre diesen Auftrag \
  genau aus. Schreibe deinen Bericht ausschliesslich nach <berichtdatei>. Aendere KEINE andere Datei als \
  die im Auftrag genannten, committe nichts, pushe nichts. Antworte am Ende nur mit: FERTIG <zeilen>." \
  -m deepseek-v4-pro --provider deepseek --usage-file docs/audits/usage_<block>_<ts>.json --yolo
```

- **Einzeln starten, nie zwei gleichzeitig** (der Laptop ist während eines großen Laufs beschäftigt).
- **Fertig ist ein Lauf an der `usage_*.json`**, nicht an der Berichtsdatei.
- Netzaussetzer: bis zu drei Versuche, 20–30 s Pause; ein Lauf zählt erst ab ~2.000 Zeichen Bericht.
- Nach dem Lauf: `git status --short` — hat das Modell nur seine Dateien angefasst?

---

## 5. Nachrechnen (das ist der eigentliche Wert)

Für **jeden** Block gilt die Regel aus dem Skill: das Modell liefert einen Entwurf, **nie** Belege.

1. Jede Kernzahl mit einem eigenen Einzeiler nachrechnen (`print(...)` gegen die Daten).
2. Jede zitierte Stelle in der Datei aufschlagen (Datei **und** Zeile).
3. `git diff` lesen, bevor committet wird — auch bei „grün“.
4. Voller Sammellauf, und zwar **nach** dem letzten Fix, nicht davor.
5. Erst dann Commit; bei rot: zurücknehmen, nicht passend machen.

---

## 6. Was ausdrücklich NICHT Teil des Pakets ist

- Veröffentlichen, pushen, ein Release anlegen, die README neu schreiben.
- Neue Spielmechaniken, die kein Registerpunkt und keine Daniels-Entscheidung deckt.
- Änderungen an `data/`-Zahlen ohne Entscheidung (Balancing ist Vorschlag, Entscheidung bei Daniel).
- Alles am Hermes-System (Skills, Regeln, Konfiguration).
- Der Online-Repo-Backlog aus `docs/EXTERNES_FEEDBACK_GITHUB_20261101.md` — der läuft **nach** der Demo.
