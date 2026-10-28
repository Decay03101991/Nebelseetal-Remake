# Nebelseetal Remake — Plan: vom vorbereiteten Prototyp zum spielbaren Einzelspieler-Spiel

> **Für Hermes:** Paketweise abarbeiten (W0 → W10). Nach jedem Paket Testlauf + Kurzbericht.
> Kein Paket gilt als fertig ohne ausgeführten Test.

**Ziel:** Ein lokales, portables Windows-Einzelspieler-Spiel, in dem eine vollständige Partie möglich ist:
Siedlung aufbauen → Einheiten ausbilden → Karte erkunden → Kämpfe mit Ablauf und Bericht →
Gegner handeln → Ziel erreicht oder Niederlage → Speichern/Laden. Original-Optik (Icons aus dem
Original), kostenlos lauffähig, ohne Abo und ohne Server.

**Architektur:** Trennung von Daten (JSON-Definitionen), Regeln (Services: Wirtschaft, Kampf, Gegner),
Zustand (Model) und Oberfläche (tkinter-Views). `bonus_system` bleibt die **einzige** Wertequelle —
derzeit gibt es zwei widersprechende Tabellen, das ist die Hauptursache für „nicht spielbar".

**Technik:** Python 3.14 + tkinter (Standardbibliothek), JSON-Speicherstand, Icon-Schnitt mit
reiner Standardbibliothek (zlib/struct) — **keine Zusatzpakete nötig**, keine Kosten, offline.

---

## 1. Zielbild: Was „spielbar" konkret bedeutet (Abnahmekriterien)

| # | Kriterium | Prüfung |
|---|---|---|
| A1 | Start ohne Fehlermeldung, Fenster erscheint | Prozess läuft, Fenstertitel vorhanden |
| A2 | Neues Spiel: Gebäude bauen, Einheiten ausbilden, Siedlung gründen | Klickpfad im Testskript nachgestellt |
| A3 | **Jede** Einheit hat echte, konsistente Kampfwerte (keine 0-Werte) | automatischer Test über alle Einheiten |
| A4 | Kampf ist ein **Ablauf**: Runden, beidseitige Verluste, Bericht, Beute, Rückmarsch | Kampftest mit erwarteten Größenordnungen |
| A5 | Gegner handeln sichtbar (bauen, angreifen, handeln) | Bot-Zug im Log nachweisbar |
| A6 | Ziel, Sieg und Niederlage sind definiert und auslösbar | Testsieg + Testniederlage |
| A7 | Speichern, Laden, Autosave, Versionskennung | Rundlauf-Test inkl. altem Spielstand |
| A8 | 15 Minuten Dauerlauf ohne Absturz und ohne Speicherleck | Dauerlauf-Test |
| A9 | Einheiten- und Gegenstands-Icons stammen aus dem Original, keine Doppelbelegung | Zuordnungstest: 1 Icon pro Einheit |
| A10 | Gegenstände (Items) existieren als System mit Wirkung | Ausrüsten → Wert ändert sich messbar |

---

## 2. Ist-Stand (gemessen, nicht geschätzt)

| Prüfung | Ergebnis | Beleg |
|---|---|---|
| Start über `Nebelseetal_Remake.bat` | **läuft**, Fenster „Nebelseetal Remake" öffnet | PID 3380, Fenstertitel ausgelesen |
| Alle 17 Menüansichten rendern | **alle ohne Fehler** | Testskript über alle Views |
| Kernaktionen (Ausbauen, Forschen, Ausbilden, Gründen, Handel, Angriff, Speichern, Laden) | **ohne Absturz** | Testskript, 13 Aktionen |
| Engine: 5 Karten generierbar, Produktion, Speichern/Laden | **funktioniert** | Tilezahlen, Holz 10→46, Rundlauf |
| Einheiten im Code | **36** | `main.UNITS` |
| Einheiten mit echten Kampfwerten | **7** | `bonus_system.UNIT_BASE` |
| Einheiten mit **Kampfkraft 0** | **29 von 36** | u. a. Drache, Trebuchet, Katapult, Riese, Ork, Troll |
| Kampfauflösung | **ein Vergleich zweier Zufallszahlen**, keine Runden, keine Verluste | `_attack` / `_simulate_random_battle` |
| Icon-Dateien vorhanden | **17** für 36 Einheiten | `assets/icons/original_units/` |
| Mehrfachbelegung | **8 Einheiten teilen `Kämpfer.png`**, 5 teilen `Krieger.png`, 4 teilen `Paladin.png` | automatischer Zuordnungstest |
| Gegenstands-System | **existiert nicht** | kein Item-Code in `src/` |
| Waren (17) | nur Emoji-Symbole | `main.GOODS` |
| Sieg / Niederlage | nicht definiert (`is_defeated()` ist unerreichbar, da „kontinent" nie zerstörbar) | Codeprüfung |
| Bot-Verhalten | Bots hatten **keine Siedlungen und keine Armee** → Angriffe liefen ins Leere (in dieser Sitzung bereits nachgebessert) | Codeprüfung |

### Der entscheidende Beleg

```
Kampfkraft pro Einheit (1 Stück) nach der Formel, die der Kampf benutzt:
  krieger              39.0
  bogenschütze         53.6
  drache                0.0
  trebuchet             0.0
  katapult              0.0
  riese                 0.0

  Einheiten mit Kampfkraft 0: 29 von 36
```

```
Zwei widersprechende Werte-Tabellen:
  main.UNITS['drache']    : 45 / 20       (wird nur ANGEZEIGT)
  bonus_system.UNIT_BASE  : NICHT VORHANDEN  (RECHNET den Kampf)
```

Der Drache wird in der Kaserne mit „ATK 45 / DEF 20" angezeigt und zählt im Kampf **null**.
Der Golem zeigt „Schaden 32", rechnet aber mit **270**. Anzeige und Rechnung widersprechen sich.

---

## 3. Ursachen (nicht Symptome)

- **U1 — Zwei Wertequellen.** `main.UNITS` (Anzeige) und `bonus_system.UNIT_BASE` (Rechnung) sind
  getrennt gepflegt und laufen auseinander. Genau davor warnt schon der Archiv-Skill
  („Do not scatter bonus math across UI code").
- **U2 — Unvollständige Kampftabelle.** 29 von 36 Einheiten fehlen in `UNIT_BASE`, `TIER_SCALE`,
  `UNIT_TRAIN_BASE` → sie sind im Kampf wertlos und haben keine Trainingszeit.
- **U3 — Kein Kampf-Ablauf.** Es gibt keinen Schlachtverlauf: keine Runden, keine Verluste auf
  Angreiferseite, keine Garnisons- und Mauerwirkung, keinen Bericht, keinen Rückmarsch mit Beute.
- **U4 — Icons sind Platzhalter.** 17 Originaldateien wurden auf 36 Einheiten verteilt; 8 Einheiten
  teilen sich dieselbe Grafik. Zusätzlich liegen **28 echte Einheiten-Icons** ungenutzt in 5 Sheets.
- **U5 — Gegenstände fehlen.** 13 Gegenstands-Icons liegen bereit, es gibt aber kein System dafür.
- **U6 — Kein Ziel.** Ohne Sieg-/Niederlagebedingung und ohne handelnde Bots entsteht kein Spiel.
- **U7 — Logik und Oberfläche in einer Datei.** 1400 Zeilen `main.py` mischen Regelwerk und tkinter.
  Jede Änderung ist riskant und langsam — das bremst jede weitere Verbesserung.

---

## 4. Icon-Bestand (aus den Dateien ausgemessen)

Alle Sheets haben schwarzen Hintergrund und ein gleichmäßiges Raster mit ca. 90 px Zellenbreite.

| Datei | Größe | Zellbreite | **Icons** | Inhalt |
|---|---|---|---|---|
| `Nahkämpfer_Icons.png` | 450×82 | 90 | **5** | Nahkämpfer |
| `Fernkämpfer_Icons.png` | 357×81 | 89 | **4** | Fernkämpfer |
| `Belagerungseinheiten_Icons.png` | 635×81 | 91 | **7** | Belagerung |
| `Karren_Icons.png` | 541×72 | 90 | **6** | Karren/Transport |
| `Zusatzeinheiten_Icons.png` | 547×85 | 91 | **6** | Zusatzeinheiten |
| | | | **28** | = genau die 28 Einheitenarten aus der Recherche |
| `WaffenWerkzeuge_Icons.png` | 627×77 | 90 | **7** | Waffen und Werkzeuge |
| `RüstungenMäntel_Icons.png` | 545×67 | 91 | **6** | Rüstungen und Mäntel |
| | | | **13** | Gegenstände |
| `Einheiten_Icons_Sammlung.png` | 861×587 | — | — | **Original-Screenshot** der Armeeübersicht („Folgende Einheiten sind in dieser Siedlung stationiert") — Belegdokument, keine Grafikquelle |

Die bereits vorhandenen 17 Einzeldateien in `assets/icons/original_units/` sind Ausschnitte
derselben Sheets (90×82 / 89×81 / 86×72 / 75×81). **Sie bleiben unangetastet** — neue Ausschnitte
kommen in neue Ordner, die Originaldateien werden nicht umbenannt oder verschoben.

---

## 5. Zielarchitektur

```
Nebelseetal_Remake/
├── Nebelseetal_Remake.bat          Start (bleibt)
├── run_tests.bat                   NEU: ein Befehl, der alles prüft
├── README.md                       NEU: Start, Bedienung, Datenablage
├── data/                           (bisher leer)
│   ├── units.json                  NEU: Einheiten + Werte (EINE Quelle)
│   ├── items.json                  NEU: Gegenstände
│   ├── buildings.json              NEU: Gebäude + Bauzeiten
│   ├── research.json               NEU: Forschungen
│   ├── maps.json                   NEU: Karten (Kontinent mit Sektoren)
│   └── bots.json                   NEU: Gegnerprofile
├── src/
│   ├── main.py                     Einstieg + GUI (schlank)
│   ├── model.py                    NEU: Spielzustand, Speichern/Laden
│   ├── bonus_system.py             bleibt: EINZIGE Wertequelle
│   ├── services/
│   │   ├── economy.py              NEU: Produktion, Bau, Ausbildung, Bevölkerung
│   │   ├── combat.py               NEU: Kampf-Ablauf (Runden, Verluste, Bericht)
│   │   ├── bots.py                 NEU: Gegnerverhalten
│   │   └── goals.py                NEU: Sieg/Niederlage/Fortschritt
│   └── ui/                         NEU: je Menüpunkt eine Ansicht
├── assets/icons/units/             NEU: 28 geschnittene Einheiten-Icons
├── assets/icons/items/             NEU: 13 geschnittene Gegenstands-Icons
├── tools/slice_icons.py            NEU: Icon-Schnitt (Standardbibliothek)
└── tests/                          NEU: automatische Prüfungen ohne Fenster
```

**Regel:** Daten in `data/*.json`, Regeln in `services/`, Anzeige in `ui/`.
`main.py` wird dadurch von 1400 auf wenige hundert Zeilen reduziert.

---

## 6. Werkzeug- und Kostenstrategie

### Was auf diesem Rechner vorhanden ist (geprüft)

| Werkzeug | Status | Nutzen |
|---|---|---|
| Python 3.14.7 + pip | vorhanden | gesamte Entwicklung |
| uv | vorhanden | Pakete, falls nötig |
| node + npm | vorhanden (Hermes) | nicht nötig |
| git | vorhanden (2.x) | Versionssicherung des Projekts |
| pandoc | vorhanden | Doku/Druck |
| **Codex CLI** | **nicht vorhanden** | — |
| **Claude Code CLI** | **nicht vorhanden** | — |
| **OpenCode / Aider / Gemini CLI** | **nicht vorhanden** | — |
| **gh CLI** | **nicht vorhanden** | — |
| Hermes-Profil „coding" | **nicht vorhanden** (nur `schulprojekt`) | — |

**Folge:** Die externen Coding-Agenten stehen **nicht** bereit. Sie würden zusätzlich Abo- oder
API-Kosten erzeugen und sind mit der 4-EUR-Tagesgrenze nicht vereinbar. Der Plan kommt ohne sie aus.

### Was stattdessen arbeitet

1. **Ich selbst** (Standardmodell `deepseek-v4-flash`) als Bauherr: analysieren, umsetzen, testen.
2. **Unteragenten** (`delegate_task`) für getrennte, gut abgegrenzte Pakete (z. B. Icon-Schnitt,
   Kampf-Engine, Bot-Verhalten) — gleicher Anbieter, gleicher Preis, keine Zusatzkosten.
3. **Automatische Prüfungen** (`tests/`, `run_tests.bat`) — der eigentliche Qualitätshebel.
   Jedes Paket wird ohne Fenster geprüft, damit Fehler sofort auffallen statt erst im Spiel.
4. **Lokale, kostenlose Werkzeuge**: eigener PNG-Leser/Schreiber in der Standardbibliothek
   (kein Pillow nötig), Emoji/Text-UI, JSON. Keine Bildgenerierung, keine Web-APIs.

### Was ich bewusst **nicht** tue

- Kein bezahlter Coding-Dienst, kein Modellwechsel, keine Bildgenerierung.
- Keine Zusatzpakete, solange die Standardbibliothek reicht (weniger Ausfallrisiko nach Hermes-Updates).
- Kein Anlegen neuer Profile/Berechtigungen/Cronjobs ohne ausdrückliche Freigabe.

### Kosten

Gemessen heute: **1,09 EUR von 4,00 EUR** verbraucht, 2,91 EUR frei.
Ein Arbeitstakt (Analyse + Umsetzung + Test) liegt bei etwa **0,05–0,25 EUR**.
Der gesamte Plan (W0–W10) wird auf **ca. 1,50–3,00 EUR** geschätzt, verteilt über mehrere Tage —
also innerhalb der geltenden Grenze, ohne Sonderfreigabe. Vor jedem größeren Takt wird neu gemessen.

---

## 7. Arbeitspakete

### W0 — Sicherheitsnetz (zuerst, sonst nichts)

**Ziel:** Jede spätere Änderung ist rücknehmbar und prüfbar.

- `git init` im Projekt, `.gitignore` für `build/`, `dist/`, `*.spec`, `__pycache__`, `*.lock`, `savegame.json`.
- Erster Commit des Ist-Stands (inkl. aller Assets).
- `tests/` + `run_tests.bat` anlegen: ein Befehl prüft Syntax, Engine, Datenbestand, alle Ansichten.
- Der Testläufer ist **fensterlos** (kein sichtbares Fenster nötig), damit er oft laufen kann.

**Akzeptanz:** `run_tests.bat` läuft durch und meldet für den Ist-Stand: „29 Einheiten ohne Kampfwerte"
und „8 Einheiten mit gleichem Icon" — also genau die bekannten Mängel, als Ausgangsmarke.
**Kosten:** ~0,10 EUR.

### W1 — Eine Wertequelle (U1, U2)

**Ziel:** Jede Einheit hat echte, konsistente Werte in **einer** Datei, Anzeige und Rechnung stimmen überein.

- `data/units.json` als einzige Quelle: Angriff, Verteidigung, Trefferpunkte, Tempo, Kosten,
  Ausbildungszeit, Stufe/Rang, Rolle, Belagerungsschaden (für Belagerungswaffen).
- `main.UNITS` und `bonus_system.UNIT_BASE/TIER_SCALE/UNIT_TRAIN_BASE` werden daraus erzeugt,
  nicht mehr doppelt gepflegt.
- `tests/test_units.py`: für **jede** Einheit müssen Angriff > 0, Verteidigung ≥ 0, Trefferpunkte > 0,
  Kosten > 0 und Ausbildungszeit > 0 sein; Kampfkraft jeder Einheit > 0.
- Gegenprobe: Anzeigewert in der Kaserne == Rechenwert im Kampf (Toleranz 0).

**Akzeptanz:** Test meldet „36 von 36 Einheiten mit Kampfkraft > 0"; der Drachenwert in der Kaserne
entspricht exakt dem Wert im Kampfbericht.
**Kosten:** ~0,20 EUR. **Offene Entscheidung E1 (siehe Abschnitt 11).**

### W2 — Kampfablauf (U3) — das Herzstück

**Ziel:** Ein Kampf ist ein nachvollziehbarer Ablauf, nicht eine Zufallszahl.

- `services/combat.py` mit klaren Schritten:
  1. Aufstellung: Angreifer-Truppen ausgewählt, Verteidiger = Garnison + Siedlungseinheiten.
  2. Verteidigungsbonus aus Wachturm/Mauer und Forschung (über `bonus_system`).
  3. Runden: pro Runde Schaden beider Seiten, Verluste anteilig nach Trefferpunkten.
  4. Belagerungswaffen wirken zusätzlich gegen Bauwerke (eigener Schadenswert).
  5. Fernkampf zuerst (Bogenschützen/Armbrust), dann Nahkampf, Reiterei wirkt verstärkt gegen Fernkämpfer.
  6. Ergebnis: beidseitige Verluste, Beute (gedeckelt durch Lagerkapazität), Rufpunkte,
     vollständiger **Kampfbericht** (Textzeilen), Rückmarsch der Überlebenden mit Ankunftszeit.
- `tests/test_combat.py`: Übermacht gewinnt; Unterzahl verliert; Verluste auf **beiden** Seiten;
  Belagerungswaffe beschädigt Bauwerke; Bericht enthält alle Runden; keine negativen Bestände;
  **Sicherheit**: kein Test darf Ressourcen oder Einheiten „erschaffen" (Erhaltungssatz geprüft).

**Akzeptanz:** Ein Kampf Drache + 20 Krieger gegen 40 Speerträger ergibt einen Bericht mit Runden,
beidseitigen Verlusten und Beute; dieselben Zahlen wiederholbar bei gleichem Zufallsstartwert.
**Kosten:** ~0,35 EUR.

### W3 — Icons aus dem Original (U4)

**Ziel:** Jede Einheit hat ihr eigenes Original-Icon, keine Doppelbelegung.

- `tools/slice_icons.py`: liest die Sheets mit dem bereits erprobten Standardbibliothek-PNG-Leser,
  schneidet auf dem Raster (Zellbreite aus der Breite hergeleitet, ca. 90 px), schreibt einzelne
  PNGs nach `assets/icons/units/` bzw. `assets/icons/items/`. **Originale bleiben unverändert.**
- Erzeugt zusätzlich ein **Kontaktblatt** (alle Ausschnitte mit Nummern) zur Abnahme.
- **Abnahme durch Daniel:** einmal kurz aufs Kontaktblatt schauen und bestätigen oder korrigieren,
  welche Nummer welche Einheit ist. Erst danach wird die Zuordnung festgeschrieben.
  (Der Archiv-Skill verlangt ausdrücklich: Nutzerbilder nicht eigenmächtig umsortieren.)
- `data/units.json` bekommt je Einheit den Dateinamen; `tests/test_icons.py` prüft:
  jede Datei existiert, ist ladbar, und **kein Icon ist doppelt** belegt.

**Akzeptanz:** 28 Einheiten-Icons, 13 Gegenstands-Icons, 0 Doppelbelegungen, jede Datei vorhanden.
**Kosten:** ~0,25 EUR (inkl. eines Vision-Durchgangs zum Bestimmen der Ausschnitte).

### W4 — Gegenstände (U5)

**Ziel:** Gegenstände sind ein System, nicht nur Bilder.

- `data/items.json`: 13 Gegenstände in Kategorien (Waffe, Werkzeug, Rüstung, Mantel) mit Wirkung
  (Angriff, Verteidigung, Trefferpunkte, Tempo, Ertrag), Fundort/Kaufpreis, Seltenheit.
- Ausrüsten: Gegenstand einer Einheitengruppe oder dem Herrscher zuordnen; Wirkung fließt über
  `bonus_system` in Produktion und Kampf ein.
- Sichtbar: eigener Menüpunkt „Ausrüstung" mit Icon, Wirkungstext und Vergleich zum aktuellen Wert.
- `tests/test_items.py`: Ausrüsten verändert den Kampfwert **messbar**; Ablegen stellt den alten Wert
  exakt wieder her; kein Gegenstand doppelt ausgerüstet.

**Akzeptanz:** Ein Rüstungsteil erhöht den Verteidigungswert der gewählten Gruppe sichtbar und wird
im nächsten Kampfbericht wirksam.
**Kosten:** ~0,30 EUR.

### W5 — Wirtschaft in Echtzeit

**Ziel:** Bauen und Ausbilden dauern Zeit, wie im Original.

- Bauaufträge mit Restzeit und Anzeige; Ausbildungs-Warteschlange je Kaserne.
- Bevölkerung: wächst bis zum Wohnraum, wird für Bauvorhaben verbraucht.
- Lagerkapazität je Ressource; Überlauf wird abgewiesen statt still verbucht.
- `tests/test_economy.py`: Bauzeit läuft korrekt ab; Auftrag blockiert nicht die Oberfläche;
  Kapazitätsgrenze greift; kein Bau ohne Ressourcen; Abbruch erstattet anteilig.

**Akzeptanz:** Ein Bauvorhaben zeigt Countdown und schließt zuverlässig ab (Test mit beschleunigter Zeit).
**Kosten:** ~0,30 EUR.

### W6 — Welt und Gegner (U6)

**Ziel:** Es gibt echte Gegner mit sichtbarem Verhalten.

- `data/bots.json`: Profile mit Fraktion, Aggression, Handelsneigung, Siedlungen, Armee (in dieser
  Sitzung bereits ein erster Ansatz eingebaut).
- `services/bots.py`: Zyklus pro Spielminute — produzieren, forschen, Einheiten ausbilden,
  Siedlungen gründen, handeln, angreifen (nach Aggression und Rufabstand).
- Bots greifen wirklich an: Überfall auf Siedlungen mit Bericht und Verlusten;
  Noobschutz für 7 Tage wie im Original respektiert.
- `tests/test_bots.py`: Bot baut über Zeit spürbar auf; aggressiver Bot greift innerhalb N Spieltagen
  an; passiver Bot handelt stattdessen; Noobschutz wird eingehalten.

**Akzeptanz:** Nach einem simulierten Spieltag ist im Log mindestens ein Bot-Zug und ein Kampf sichtbar.
**Kosten:** ~0,35 EUR.

### W7 — Ziel, Sieg, Niederlage

**Ziel:** Die Partie hat einen Anfang und ein Ende.

- `services/goals.py`: Fortschrittsziele (Meilensteine wie „Kaserne Stufe 3", „erste Eroberung",
  „Portal errichtet") mit Belohnung, und ein Endziel.
- Sieg: Endziel erreicht (Vorschlag E3, siehe Abschnitt 11).
- Niederlage: alle Siedlungen verloren **und** keine Truppen mehr (nicht mehr der unerreichbare
  Kontinent-Fall). Klare Meldung mit Statistik, Neuanfang möglich.
- `tests/test_goals.py`: Ziel wird erkannt und belohnt; Niederlage wird korrekt ausgelöst;
  nach Sieg/Niederlage läuft kein Spielzug weiter.

**Akzeptanz:** Ein Testspiel kann sowohl gewonnen als auch verloren werden.
**Kosten:** ~0,25 EUR.

### W8 — Oberfläche

**Ziel:** Die vorhandene Optik bleibt, wird aber klar und informativ.

- Duplikate entfernen (in dieser Sitzung schon teilweise erledigt: `_build_main_ui`, `_render_settings`).
- Kaserne: Wertetabelle je Einheit mit Icon, Angriff/Verteidigung/Trefferpunkten, Belagerungsschaden,
  Dauer und Kosten — deckungsgleich mit den Rechenwerten.
- Lager: echte Original-Icons statt Emoji für Einheiten und Gegenstände, Mengen gut lesbar.
- Karten: Kartenverwaltung mit Betreten/Stationieren/Angreifen/Zerstören (in dieser Sitzung verdrahtet),
  Truppenbewegungen mit laufendem Countdown.
- Kampfbericht als eigener Menüpunkt mit Runden und Verlusten, aus dem Nachrichtenarchiv erreichbar.
- Statuszeile unten (in dieser Sitzung eingebaut) zeigt jede Meldung auch ohne Konsole.
- `tests/test_ui.py`: jede Ansicht baut fehlerfrei; keine Ansicht zeigt 0-Werte für Einheiten.

**Akzeptanz:** Kein Einheitenwert in der Oberfläche ist 0; jede Aktion erzeugt eine sichtbare Meldung.
**Kosten:** ~0,35 EUR.

### W9 — Speichern und Laden robust

- Kennung `save_version` im Spielstand; ältere Stände werden erkannt und nachgezogen statt zu brechen.
- Autosave alle 5 Minuten und beim Beenden; eine Sicherungskopie des letzten Standes.
- Fehlerhafte oder fehlende Datei führt zu klarer Meldung, nie zu Absturz.
- `tests/test_save.py`: Rundlauf, alter Stand, beschädigte Datei, fehlende Datei, Autosave.

**Akzeptanz:** Alle vier Fälle laufen ohne Absturz und ohne Datenverlust.
**Kosten:** ~0,20 EUR.

### W10 — Verpackung und Dokumentation

- `README.md`: Zweck, Start, Bedienung, Datenablage, bekannte Grenzen, Backup-Hinweis.
- Portable Windows-Version (PyInstaller), Start über `run.bat`, geprüft auch mit Leerzeichen im Pfad.
- Keine Mehrfach-EXEs, keine Reste (`build/`, `dist/`, `*.spec` werden aufgeräumt).
- Icon des Programms aus dem vorhandenen `nebelseetal.ico` (Mehrgrößen-ICO wie im Archiv-Skill beschrieben).

**Akzeptanz:** Start von einem anderen Laufwerk, Spielstand wird geschrieben und gelesen.
**Kosten:** ~0,25 EUR. **Offene Entscheidung E4 (Name der EXE).**

---

## 8. Test- und Qualitätsstrategie

- **Ein Befehl:** `run_tests.bat` führt alles aus (Syntax, Engine, Daten, Kampf, Wirtschaft, Bots, UI).
- **Fensterlos:** Tests laufen ohne sichtbares Fenster — deshalb nach jeder Änderung möglich.
- **Ausgangsmarke:** Der Testlauf auf dem Ist-Stand **muss die bekannten Mängel melden**
  (29 Einheiten ohne Kampfwerte, 8 Einheiten mit gleichem Icon). Erst dadurch ist belegt,
  dass die Tests wirklich prüfen und nicht nur grün leuchten.
- **Erhaltungssatz:** Kein Test darf Ressourcen oder Einheiten erschaffen. Vorher/Nachher wird summiert.
- **Sichtprüfung am Ende** jedes Pakets, das die Oberfläche berührt: Fenster starten, Screenshot,
  Blick auf die betroffene Ansicht.
- **Fertig heißt geprüft:** Jedes Paket endet mit Testlauf **und** kurzem Bericht: was umgesetzt,
  was geprüft, was offen.

---

## 9. Reihenfolge und Meilensteine

| Meilenstein | Pakete | Ergebnis | Kosten (Schätzung) |
|---|---|---|---|
| **M1 — Spielbarer Kern** | W0, W1, W2 | Kämpfe möglich und korrekt, Werte stimmen | ~0,65 EUR |
| **M2 — Welt und Aussehen** | W3, W4, W5, W6 | Original-Icons, Gegenstände, Gegner, Echtzeit-Bau | ~1,20 EUR |
| **M3 — Fertige Partie** | W7, W8, W9 | Ziel, Sieg, Niederlage, klare Oberfläche, stabiles Speichern | ~0,80 EUR |
| **M4 — Lieferung** | W10 | Portable Windows-Version + README | ~0,25 EUR |
| | | **Gesamt** | **~2,90 EUR**, über mehrere Tage |

Wenn Daniel zuerst etwas anderes sehen will (z. B. unbedingt die Icons), lässt sich W3 vorziehen —
W0 bleibt aber immer der Anfang.

---

## 10. Risiken und Gegenmaßnahmen

| Risiko | Wirkung | Gegenmaßnahme |
|---|---|---|
| Umbau bricht die Oberfläche | Spiel startet nicht mehr | W0-Sicherheitsnetz, Tests nach jedem Schritt, git-Rücknahme möglich |
| Icon-Zuordnung stimmt nicht | falsche Bilder je Einheit | Kontaktblatt zur Abnahme, keine automatische Umbenennung |
| Umfang der 36 Einheiten wird zu groß | Balancing wird unübersichtlich | Entscheidung E1: auf 28 Originalarten zurückführen |
| Originalwerte fehlen (keine Quelle) | Werte sind Nachbau, nicht original | offen kennzeichnen; alle Werte in `data/units.json` an einer Stelle änderbar |
| tkinter wirkt altmodisch | Optik-Einbuße | vorhandene Skin-Farben und Original-Icons nutzen; keine teure Neuentwicklung |
| Hermes-Update tauscht die Python-Laufzeit | Zusatzpakete verschwinden | Standardbibliothek bevorzugen; wenige Abhängigkeiten |

---

## 11. Entscheidungen, die Daniel treffen muss

- **E1 — Einheitenumfang:** Die Original-Icons belegen **28** Einheitenarten, der Code hat **36**.
  Empfehlung: auf die 28 Originalarten zurückführen (originaltreu, ein Icon je Einheit, klarer zu balancieren).
  Alternative: 36 behalten und mehrere Einheiten bewusst dasselbe Basisbild mit Farbvariante geben.
- **E2 — Karten:** Der Kontinent ist als Sektorkarte mit Koordinaten angelegt. Frage: Reicht ein
  großer Kontinent mit Sektoren als Hauptkarte, oder sollen die vier kleineren Welten voll ausgebaut werden?
- **E3 — Siegbedingung:** Vorschlag: Endziel = alle fünf Welten freigeschaltet **und** 3 feindliche
  Siedlungen erobert **und** Punktzahl X erreicht. Alternative: reine Punktzahl-Meisterschaft.
- **E4 — Name der Startdatei:** weiterhin `Nebelsee Memory.exe` oder neuer Name
  (z. B. `Nebelseetal_Remake.exe`)? Es soll weiterhin **genau eine** EXE im Projektordner liegen.
- **E5 — Arbeitssystem:** Darf ich für die parallele Abarbeitung ein eigenes Hermes-Profil mit
  Kanban-Anbindung anlegen (Systemänderung, deshalb Rückfrage)? Ohne Freigabe arbeite ich
  weiter allein + mit Unteragenten — das funktioniert, ist aber langsamer.
- **E6 — Kampftempo:** Original war Echtzeit; auf einem Speedserver das 200-Fache. Frage: normale
  Geschwindigkeit (Bauen dauert Minuten) oder beschleunigt (Bauen dauert Sekunden) als Standard?

---

## 12. Was heute schon erledigt wurde (in dieser Sitzung)

Damit nichts doppelt gebaut wird:

- Zustand geprüft und belegt: Spiel startet, alle 17 Ansichten rendern, 13 Kernaktionen ohne Fehler.
- Doppelte Definitionen entfernt (`_build_main_ui`, `_render_settings`).
- Statuszeile unten ergänzt (Meldungen sind ohne Konsole sichtbar) — Pack-Reihenfolge korrigiert.
- „Laden" aktualisiert jetzt die Oberfläche statt einen veralteten Stand zu zeigen.
- **Kartenverwaltung verdrahtet**: Betreten (mit Wechselkosten), Stationieren, Angreifen und
  Zerstören waren fertig programmiert, aber im Spiel **nicht erreichbar** — jetzt als Menü vorhanden.
- Bots erhalten echte Siedlungen und Armeen (vorher leer → Angriffe liefen ins Leere).
- Bevölkerung wächst nun bis zum Wohnraum (war ein toter Wert) und wird im Dorfzentrum angezeigt.
- Karte zeichnet im Sekundentakt neu, damit Truppen-Countdowns mitlaufen.
- Sicherung der Originaldatei: `main.py` von vor dem Umbau liegt unter
  `%LOCALAPPDATA%\hermes\cache\scratch\nebel_backup\`.

---

## 13. Vorgänger und Kontinuität

Dieses Projekt wurde **nicht neu begonnen**. Es wurde in der Session `20260905_124210_04ba4a`
(05.–08.09.2026, 1811 Nachrichten, 739 Werkzeugaufrufe, 13 Untersitzungen) vom selben Agenten
gebaut — im Profil `default`, nicht von einem getrennten Coding-Dienst. Belegt durch die
Sitzungsdatenbank: alle 230 Sitzungen dieses Systems laufen unter `profile_name = default`;
ein eigenes Coding-Profil hat es bis heute nicht gegeben (das neue Profil `coding` vom 04.10.2026
ist ein **Arbeiter für die Zukunft**, kein Ersatz für etwas Bestehendes).

Sein Projektwissen darf nicht im Archiv liegen bleiben. Es wurde deshalb am 04.10.2026 wieder
aktiv geführt:

| Was | Wo vorher | Wo jetzt |
|---|---|---|
| Projektregeln und Fallen | `skills\.archive\desktop-game-remake\` | Abschnitt „Vorgänger-Regeln" im Skill `nebelseetal-remake` |
| Rollendefinition für Coding-Aufgaben | Skill `coding-bot` | unverändert aktiv, gilt weiter |
| Übergabeformat an den Coding-Bot | Skill `coding-task-format` | unverändert aktiv, gilt weiter |
| Produktbau-Regeln | Skill `python-product-builder` | unverändert aktiv, gilt weiter |

Ausdrücklich **nicht** angetastet: die 17 Original-Icons in `assets/icons/original_units/`,
die Sheets in `Einheiten Icons\` und `Item Icons\`, die vorhandene `Nebelsee Memory.exe`.
Seine Arbeit wurde nicht überschrieben, sondern gesichert (Sicherung der `main.py` vom 04.10.2026)
und fortgeführt.

**Falls ein anderer Coding-Agent gemeint ist** (eigener Rechner, Claude Code/Codex, ein Bot-Name):
Auf diesem System existiert dafür kein Eintrag — keine Profilspur, kein Bot-Eintrag
(`bot_relay\roster.json` ist leer), kein Werkzeugprotokoll. Dann bitte den Namen nennen; ich suche
gezielt danach, statt ihn zu übergehen.

---

*Erstellt am 04.10.2026. Grundlage: eigene Messungen (Kampfkraft-Test, Icon-Zuordnungstest,
Startprüfung, Bildschirmaufnahme), die Sitzungsdatenbank `state.db` und `docs/nebelseetal_research.md`.*
