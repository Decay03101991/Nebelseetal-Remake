# GESAMTAUDIT 11.11.2026 — vier Prüfgänge, jeder Befund nachgerechnet

**Auftrag:** Daniel, 11.11.2026, 13:38: »Ja, jetzt starten (eigener Lauf, nur lesend, Repo bleibt
unberührt)« (Register 396). **Letzter Gesamtaudit:** 31.10.2026. **Verfahren:** vier parallele Prüfgänge,
danach **eigene Nachrechnung jedes einzelnen Befunds** durch den Auftraggeber-Agenten.

**Ergebnis in einer Zeile:** 32 Befunde geliefert, **30 bestätigt**, **einer in der behaupteten Form
widerlegt**, **einer teilweise** (Restbefund bleibt). Kein `src/`- und kein `data/`-Eingriff, keine
Änderung an der EXE.

---

## 1. Verfahren und Grenzen

| Was | Wie |
|---|---|
| Prüfer | vier Teil-Läufe parallel, Modell `deepseek-flash`, je **höchstens 8** Befunde |
| Belegpflicht | je Befund `Datei:Zeile` **und** der Befehl, mit dem man es nachprüft |
| Rolle | **read-only** — kein Schreiben, kein `git`, keine Änderung am Spiel |
| Nachrechnung | **jeder** Befund wurde danach von mir selbst gemessen (Skript `nachrechnen_audit.py` + Einzelgriffe) |
| Dauer | 992 s für die vier Läufe, danach rund 15 min Nachrechnung |
| Kosten | Modellzeit `deepseek-flash` (kein USD-Betrag abgelesen — Buchhaltung folgt bei der nächsten Ablesung) |

**Grenzen, ausdrücklich:** die übrigen rund 200 Prüfdateien wurden nicht einzeln durchgesehen; es wurde
**kein Spiel gestartet** (keine Spielstand-Änderung, Daniels Frischstart bleibt heil); das Handbuch wurde
**nicht** erneut abgeglichen (das ist der andere Auftrag, `AUFTRAG_CLAUDE_DESIGN_20261111.md` betrifft die
Präsentation).

## 2. Die vier schwersten Befunde (eigene Messung)

### 2.1 Der Kampfbericht nennt die doppelte Beute

`src/kampf.py:142` rechnet die Beute mit `_beute` (nur Ladungsgrenze), `src/main.py:6243` bucht aber eine
andere Zahl. **Gemessen** (`kampf._beute` gegen `kampfbericht.beute_am_ziel`, Handkarren, 100 Holz/Stein):
Bericht **20/20**, gebucht **10/10**. Der Spieler sucht Gut, das nie im Lager liegt. **Fehler.**

### 2.2 Die Wallpunkte werden an zwei Stellen verschieden summiert

`main.punktestand` summiert je Dorf (`main.py:4056-4061`), `spielschicht.punkte` nimmt nur die **höchste**
Stufe (`spielschicht.py:849`). **Gemessen** mit zwei Dörfern Wallstufe 2: je Dorf summiert **16**,
`wall_stufe` **2**, `spielschicht.punkte` **8**. Betroffen ist unter anderem das Messwerkzeug
`tools/spieltest_simulation.py` — die Registerzahl »3,5 Punkte je Spieltag« stammt aus diesem Weg. **Fehler.**

### 2.3 `run_tests.bat` ist rot — und zwar dauerhaft

`tests/test_weltkarte.py` steht in `run_tests.bat` und bricht ab: **`AttributeError: 'NebelseetalApp'
object has no attribute 'welt_zelle'`**, ohne `ERGEBNIS`-Zeile (selbst gelaufen, 11.11.2026). Der
Sammellauf ist davon nicht betroffen (er setzt die Datei aus), aber der Einstiegspunkt für Daniel meldet
damit **immer** »FEHLER vorhanden«. **Fehler im Prüfstand, nicht im Spiel.**

### 2.4 Ein Siedler wird nur den Bots abgezogen

`spielschicht._baukosten("holzfäller", 1)` liefert `{'holz': 10, 'stein': 5, 'siedler': 1}`, während
`wirtschaft.siedler_bindung_aktiv()` **False** ist und `main.py:2982` den Posten beim Spieler entfernt.
Daniels Entscheidung vom 31.10.2026 gilt also nur für den Spieler; der Bot-Pfad zahlt weiter. **Fehler.**

## 3. Alle 32 Befunde mit meinem Urteil

Legende: **B** = bestätigt (selbst gemessen) · **B-Frage** = gemessen richtig, aber eine Gestaltungsfrage ·
**W** = in der behaupteten Form widerlegt · **T** = teilweise.

| Nr | Befund | Beleg | Urteil |
|---|---|---|---|
| K1 | Kampfbericht doppelte Beute | `kampf.py:142` / `main.py:6243` | **B** |
| K2 | Wallpunkte zwei Summen (16 / 2 / 8) | `main.py:4056-4061`, `spielschicht.py:849` | **B** |
| K3 | Siedler-Posten nur auf dem Bot-Pfad | `spielschicht.py:109`, `main.py:2982` | **B** |
| K4 | Wall errichten 16/16, Reparatur 16 × Stufe | `main.py:4077`, `dorfwall.py:141-151` | **B-Frage** |
| K5 | `bonus_system` liest Forschungsschlüssel `militär`, den es nicht gibt; `research_multiplier` ohne Aufrufer | `bonus_system.py:57`, `main.py:3835` | **B** |
| K6 | Taktik-Sperrzeit doppelt (Datei gegen Codekonstante) | `boni.py:64`, `bottaktik.py:50/54` | **W** — der Schlüssel heißt `sperrzeit_stunden` und wird gelesen; bottaktik führt eigene, als Vorschlag markierte Werte. Rest: `boni.sperrzeit_sekunden()` hat **keinen Aufrufer** |
| K7 | `ausbildbare_einheiten` ohne Aufrufer, Begründung veraltet | `gebaeude_wirkung.py:240` | **B** (Aufräumen) |
| K8 | Weitere Rechenwege ohne Aufrufer (`kriegspunkte_verteidigung`, `forschung.punkte`, `dauer_sekunden`) | `spieldaten.py:260`, `forschung.py:52/83/225` | **T** — `kriegspunkte_verteidigung` hat einen Test; die anderen bleiben verdächtig |
| U1 | Baumenü hell, Klick bricht an der Bibliotheksgrenze ab | `main.py:11894` / `11128-11131` | **B** |
| U2 | Forschungsansicht rechnet Bibliothek über **alle** Dörfer, der Klick nur vor Ort | `main.py:15634` / `spieloekonomie.py:1555` | **B** |
| U3 | Knopf »Wall errichten« ohne Forschungsprüfung | `main.py:15144` / `4075` | **B** |
| U4 | `beute_gutschreiben` nie aufgerufen, Beute direkt addiert | `main.py:16793`, `4614` | **B** |
| U5 | `_render_news` ist eine tote zweite Neuigkeiten-Ansicht | `main.py:14996` | **B** (Aufräumen) |
| U6 | Tick prüft `current_view == "Karten"` — keine Stelle setzt diesen Wert | `main.py:16830`, kein `current_view = "Karten"` | **B** (tote Wache) |
| U7 | Ruhmeshalle baut `einheiten` und benutzt es nie; »Truppen« zählt nur `state.units` | `main.py:14985-14987` | **B** |
| U8 | `except …: pass` verschluckt die Zeile »Freie Siedler« | `main.py:11046-11047` | **B** |
| D1 | Ganzer Siedler-/Rohstoffblock in `data/resources.json` wird von keinem Python-Code gelesen | 6 Feldnamen, je **0 Treffer** in `src/`, `tools/` | **B** |
| D2 | `bot_wirtschaft.json` führt tote Zwillinge; gelesen wird `bot_gruendung.json` | `gruendungen_je_bot` 0, `doerfer_je_bot_hoechstens` 0, `hoechstens_doerfer` **6** Treffer | **B** |
| D3 | `test_drachen` prüft gegen `pruefwerte` aus derselben Datei | `test_drachen.py:13` | **B** |
| D4 | `test_punkte:167` vergleicht einen Aufruf mit sich selbst | `test_punkte.py:167` | **B** |
| D5 | Wallstufe wird gegen das Literal `4 ** 3` geprüft, nicht gegen die Quelle | `test_punkte.py:128` | **B** |
| D6 | Keine Prüfdatei startet einen Auftrag **mit** Drosselung | `tests/` 1 Treffer, nur `kosten_der_mission` | **B** |
| D7 | `noob_protection` hat keine Rundlauf-Wache (`to_dict`/`from_dict`: 0 Treffer in `tests/`) | `main.py:7975/8215` | **B** |
| D8 | `run_tests.bat` ist rot (siehe 2.3) | `tests/test_weltkarte.py:129` | **B** |
| P1 | `index.html` sagt, Pakt/Rache/Ereignisse seien nicht eingebaut — `pakt_anbieten` ist gebaut | `main.py:14633/14736` | **B** |
| P2 | `index.html` sagt, Handelspunkte würden nicht gebucht — sie werden gebucht | `main.py:5376` | **B** |
| P3 | README nennt ZIP/EXE-Namen, die es nicht gibt | `README.md:35/37` gegen `data/version.json` | **B** |
| P4 | Die Infodateien im ZIP tragen V_0.0.1 und »rund 82 MB« (ZIP ist 101.818.049 Byte) | `release_vorlage/*.txt` | **B** |
| P5 | README nennt Speicherordner eine Ebene zu hoch (Code legt `…\Nebelseetal_Remake\Demo` an) | `README.md:42` gegen `public_start.py:18` | **B** |
| P6 | README behauptet 20 Limbus-Dimensionen, 14 leer — `data/welten.json` führt **6**, keine leer | `README.md:115-116` | **B** |
| P7 | Register 307 verankert den Götterschutz an `main.py:7786`; dort steht eine Bot-Taktik-Zeile | `docs/PRUEFREGEL_ORIGINAL.md` Zeile 344 | **B** |
| P8 | Register 2 nennt `gebaeude_wirkung.siedlergrenze_je_siedlung` — den Schlüssel gibt es nicht | `data/gebaeude_wirkung.json` | **B** |

## 4. Was daraus folgt — Reihenfolge für den Bau (nach Daniels Test)

**Stufe 1 — Spieler merkt es sofort (Fehler):** K1 (Beute), K3 (Siedler beim Bot), U1, U2, U3 (heller Knopf,
Klick bricht ab), U4 (Beute verschwindet), U7 (Ruhmeshalle zählt zu wenig).

**Stufe 2 — Prüfstand und Messung lügen:** K2 (Wallpunkte), D8 (`run_tests.bat` rot), D4/D3/D5 (Wachen, die
nichts prüfen), D6/D7 (fehlende Wachen für die neuesten Entscheidungen).

**Stufe 3 — Öffentliche Texte sagen Unwahres:** P1 bis P6. **Das ist derselbe Stoff, den der neue
Claude-Auftrag zur Präsentation prüft** (`AUFTRAG_CLAUDE_DESIGN_20261111.md`, Verdachtsliste V2/V3/V5) —
die Befunde hier sind die gemessene Grundlage dafür.

**Stufe 4 — Aufräumen ohne Spielwirkung:** K5, K6-Rest, K7, K8, U5, U6, D1, D2, P7, P8.

## 5. Was ich nicht geprüft habe

- **Kein Spielstart.** Die Befunde stammen aus Code, Daten und Prüfläufen; ob ein Fehler im laufenden Spiel
  sichtbar wird, sagt dieser Audit **nicht** — dafür ist Daniels Test da.
- **Kein Handbuchabgleich.** Der letzte liegt vom 05.10.2026 vor.
- **Nicht alle 200 übrigen Prüfdateien** wurden einzeln gelesen; geprüft wurden die genannten Stellen.
- **GitHub-Release-Tag `v_0.0.3`** wurde nicht erneut abgerufen (der Link in `index.html:61` bleibt damit
  ungeprüft; die Release-API vom selben Tag kennt den Tag).

## 6. Belege zu diesem Dokument

- Vier Läufe: `deleg_5e06718e`, 992 s, je 19 bis 78 Werkzeugaufrufe, Transkripte unter
  `C:\Users\saras\AppData\Local\hermes\cache\delegation\live\deleg_5e06718e\task-0.log` bis `task-3.log`
- Nachrechnung: `C:\Users\saras\AppData\Local\hermes\cache\scratch\nachrechnen_audit.py` (read-only)
- Laufzeit `tests/test_weltkarte.py`: 11.11.2026, AttributeError Zeile 129, keine `ERGEBNIS`-Zeile
