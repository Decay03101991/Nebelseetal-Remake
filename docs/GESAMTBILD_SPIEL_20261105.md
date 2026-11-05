# Das Spiel als Ganzes — Mechanik- und Bot-Landkarte (Stand 05.11.2026, 22:00)

**Auftrag Daniel, woertlich:** "wir müssen anfangen das spiel jetzt als ganzes zu betrachten, welche
mechaniken machen das spiel aus? Welche Bots gibt es was können sie, wie handlungsfähig sind sie aufs
gesamtspiel betrachtet und im vergleich was sie können sollten. Das alles muss gut vorgearbeitet werden
von nun an wird nicht mehr ziellos herum gearbeitet." Und: "Mein Eigenes Spiel als ommage an das
Nebelseetal."

Dieses Dokument ist das **Gesamtbild**: was das Spiel ausmacht, was davon gebaut ist (gemessen), wo die
Luecken sind. Der **Arbeitsplan** daraus steht in `docs/ARBEITSPLAN_AB_20261105.md`; der Ablauf je
Schnitt in `docs/ENTWICKLUNGSABLAUF_AB_20261105.md`.

**Gemessene Grundlage (nicht geschaetzt):** 60 Module in `src/`, 178 Pruefdateien, 628 Commits;
**74 verschiedene `bot_*`-Funktionen**, davon **69 in `src/main.py`** (in der Oberflaechen-Klasse),
2 in `src/botkern.py`, 2 in `src/drachen.py`, 1 in `src/bottaktik.py`; **9 Bot-Datendateien**
(`data/bot_bauplan|bedarf|diebstahl|forschung|gruendung|raubzug|stimmen|wappen|wirtschaft.json`);
**29 Bot-Wachen** in `tests/` (`ls tests/ | grep -i bot`).

## 1. Was das Spiel ausmacht — der Kernkreis

| # | Mechanik | Wozu sie im Spiel dient | Zustand | Beleg (Modul, Daten, Wache) |
|---|---|---|---|---|
| 1 | **Gruenden** (Karte, Fraktion, Startkarte, Siedlung 2 bis 6) | Anfang und Ausbreitung | gebaut | `originalkarten.py`, `voelker.py`, `data/startkarte.json`; `test_startseite`, `test_startkartenwahl` |
| 2 | **Produzieren** (Gebaeude, Gelaende, Erze, Werkstaetten, Waren) | Rohstoffe und Waren | gebaut | `wirtschaft.py`, `werkstatt.py`, `data/buildings.json`, `data/warenrezepte.json`; `test_produktionskette_ohne_cheats` |
| 3 | **Forschen** (21 Gebiete, Bibliothek, Pfade) | schaltet Gebaeude, Waren, Einheiten frei | gebaut | `forschung.py`, `forschungspfad.py`, `data/research.json`; `test_forschung*` |
| 4 | **Ausruesten und Ausbilden** (28 Einheiten, Warenbedarf, Akademie/Gilde/Stellmacher) | Armee und Karren | gebaut | `einheiten.py`, `ausruestung.py`, `data/units.json`; `test_ausbildungsauftraege`, `test_bot_ausbildung_je_ort` |
| 5 | **Bewegen** (Marsch, Wegzeit, Auftraege, Transport) | alles Langsame im Spiel | gebaut | `auftraege`, `marsch_optik.py`, `spieloekonomie.py`; `test_auftraege`, `test_rueckmarsch` |
| 6 | **Kaempfen** (Vorrunde, Wallstufen, Verluste, Beute ueber Karrenladung) | der Konflikt | gebaut, **Messluecke** | `kampf.py`, `kampfbericht.py`, `dorfwall.py`; `test_kampf*`; Ziel im Spieltest ist ein FIXES Dorf (16/10/12 Beute, 0 Verluste) |
| 7 | **Punkten und Auszeichnen** (Kriegs-, Forschungs-, Handels-, Gesamtpunkte; kein Sieg) | Ziel und Motivation | gebaut, Handelspunkte ungemessen | `punkte.py`, `data/*punkte*`; `test_punkte_einhaengung`; in jedem Lauf 0 Handelspunkte |
| 8 | **Siedlergrenze und Siedler** (10 + 5 je Haus, Deckel 360) | harte Grenze des Wachstums | gebaut | `haeuser.py`, `gebaeude_wirkung.py`; `test_haeuser` |
| 9 | **Nahrung als zweiter Engpass** (8 je Einheit und Spieltag) | bremst Armeen | gebaut | `data/nahrungsverbrauch.json`, `spieloekonomie.tagesbedarf_nahrung`; `test_nahrungsnot_sperre` |
| 10 | **Welten und Portal** (Herkunftswelten, Weltwechsel fuer 5.000 Mana) | Reisen zwischen Welten | gebaut, **Kette faktisch zu** | `welt.py`, `portalraum.py`; Messlage: Tempel 120 Mana/Spieltag -> ~41,7 Spieltage je Wechsel |
| 11 | **Drachen und Ruinen** (Weltpunkte, Trophaeen, Deckung in Ruinen) | Endgame und Gefahr | gebaut, Bots ohne Regel | `drachen.py`, `ruinendeckung.py`, `data/drachen.json`; `test_drachen`, `test_ruinendeckung` |
| 12 | **Goetterschutz und Sperren** | Schutz vor Rueckstand | gebaut | `versorgungsschutz.py`, `punkte.py`; `test_versorgungsschutz*` |
| 13 | **Bots als Gegenspieler** | der eigentliche Gegner im Einzelspieler-Spiel | **teilweise** | siehe Abschnitt 3 - das groesste offene Feld |
| 14 | **Story und Stimmen** (Erzaehlschicht, Bot-Stimmen) | Stimmung, Nebelsee-Gefuehl | gebaut | `story.py`, `stimmen.py`, `data/story.json`, `data/bot_stimmen.json`; `test_story*` |
| 15 | **Speichern, Spielstande, Passworttor, Demo-Leere** | Verlaesslichkeit | gebaut | `speichern.py`, `tor.py`, `public_start.py`; `test_demo_leer`, `test_spielstaende` |

**Querschnitt durch alle 15:** Spieluhr x180 (1 Spielstunde = 20 echte Sekunden, 1 Spieltag = 8 echte
Minuten), 127 Originalkarten als Grundlage, keine Kapazitaetslager (Ortslager), Goetterschutz.

## 2. Was das Spiel zusammenhält (die drei Spannungsboegen)

1. **Wachstum gegen Grenzen:** Siedler, Nahrung, Gold und Siedlungsdeckel begrenzen die Armee; wer nur
   baut, hat keine Armee, wer nur kaempft, hat keine Wirtschaft.
2. **Zeit gegen Nutzen:** jede Bewegung kostet Reisezeit (Rueckweg doppelt), jede Forschung Spieltage,
   jeder Weltwechsel Mana - das Spiel ist eine Entscheidung darueber, WOFUER die Zeit ausgegeben wird.
3. **Gegner gegen Aufbau:** die Bots muessen den Aufbau des Spielers bedrohen, sonst ist es eine
   Sandkiste. **Genau hier ist die groesste Luecke** (Abschnitt 3 und 4).

## 3. Die Bots — Ist-Stand, gemessen am Code

### 3a. Was Bots heute koennen (belegt durch Funktion, Daten und Wache)

| Faehigkeit | Umsetzung | Daten | Wache | Zustand |
|---|---|---|---|---|
| Wirtschaft aufbauen (Gebaeude je Dorf, Anlagen, Kartenprofil) | `bot_dorf_wirtschaft`, `bot_dorf_bauen` | `bot_wirtschaft.json`, `bot_bauplan.json` | `test_bot_dorf_wirtschaft`, `test_bot_bauen`, `test_bot_kartenprofil` | gebaut |
| Forschen (Plan, Baukunst zuerst) | `bot_dorf_forschung`, `bot_forschungsplan` | `bot_forschung.json` | `test_bot_forschung` | gebaut |
| Nahrung und Vorraete (Bedarf, Fenster, Reserve) | `bot_nahrungsbedarf`, `bot_vorrat_anlegen` | `bot_bedarf.json` | `test_bot_nahrung`, `test_bot_bedarf` | gebaut |
| Ausbilden (je Ort) | `bot_dorf_*ausbilden*` | `units.json`, `bot_wirtschaft.json` | `test_bot_ausbildung_je_ort` | gebaut |
| Karren bauen | `bot_karren_bauen` | `bot_wirtschaft.json` | `test_bot_karrenbau` | gebaut |
| Warenkette (Werkstatt/Ware) | `bot_dorf_warenkette` | `warenrezepte.json` | `test_bot_warenkette` | gebaut |
| Gruenden (Karte beurteilen, kaufen, erinnern) | `bot_dorf_gruenden`, `bot_kartenurteil` | `bot_gruendung.json` | `test_bot_gruendung`, `test_kartenwahl_bot` | gebaut |
| Dorf aufgeben | `bot_siedlung_aufgeben` | `bot_gruendung.json` Block `aufgeben` | `test_bot_aufgeben` | gebaut (05.11.) |
| Wall bauen | `dorfwall.py` + Bot-Takt | `buildings.json` | `test_gpt_wall_bot_kampf` | gebaut |
| Raubzug auf Doerfer | `bot_angriffsplanung` | `bot_raubzug.json` | `test_bot_raubzug_bot`, `test_gpt_bot_angriffsplanung` | gebaut |
| Diebstahl | `bot_diebstahl` | `bot_diebstahl.json` | `test_bot_diebstahl` | gebaut |
| Spionage-Bericht lesen | `bot_dorf_spionagebericht` | `spionage.py` | - | teilweise (Bericht vorhanden, kein aktives Spionieren belegt) |
| Ruinen raeumen | `bot_ruinenzug` | `bot_wirtschaft.json` | `test_bot_ruinenzug` | gebaut |
| Takte, Punkte, Stimmen, Welten, Wappen | `bottaktik.py`, `bot_takt_*`, `stimmen.py` | `bot_stimmen.json`, `bot_wappen.json` | `test_bottaktik`, `test_bot_takt_kern`, `test_bot_welten`, `test_bot_wappen` | gebaut |

### 3b. Was fehlt oder nur scheinbar da ist (ehrlich)

| Luecke | Befund | Beleg |
|---|---|---|
| **Drachen** | Bots haben keine Drachenregel - sie greifen den Drachen weder an noch meiden sie ihn | offener Punkt der Uebergabe 1828; kein `bot_drachen` im Code |
| **Handel** | nur eine Neigung als Text (`handelsneigung` kauffreudig/mittel/zurueckhaltend); kein belegter Handelszug gegen den Spieler | `src/botkern.py` (Text, kein Pfad) |
| **Angriff auf den SPIELER** | `bot_angriffsplanung` nennt keine Spielersiedlung; die Bedrohung des Spielers ist damit nicht belegt und in keinem Spieltest aufgetreten | `grep -rn "spieler" src/bot_angriffsplanung.py` = 0 Treffer |
| **Aktive Spionage** | nur Bericht-Lesen, kein Ausloesen eines Spionageauftrags durch den Bot | `bot_dorf_spionagebericht` |
| **Reaktion auf Spielerfortschritt** | Bots skalieren nach eigener Lage, nicht nach der Staerke des Spielers (kein Schwellenwert "Spieler ist maechtiger, jetzt ruesten") | `bot_raubzug.json` nennt `armee_schwelle`, `staerke_faktor` - ohne Spielerbezug |
| **Schwierigkeitsgrade** | `bot_wirtschaft.json` kennt Stufen (`leicht`/`mittel`...) fuer Gruenden/Bewerten, aber kein durchgehendes Persoenlichkeitsprofil (aggressiv, wirtschaftlich, forschend) | `data/spieloekonomie.json` Block `bots` |
| **Struktur** | **69 der 74 `bot_*`-Funktionen stehen in `src/main.py`** - der Bot laesst sich ohne Oberflaeche kaum einzeln messen oder balancieren | Zaehlung oben |
| **Messbarkeit im Spieltest** | die Simulation tritt gegen EIN fixes Dorf an; kein simulierter Bot-Gegner im Verlauf | `tools/spieltest_simulation.py`, Ziel `Bot-Siedlung` mit festen Vorraeten |

## 4. Was Bots koennen SOLLTEN (Zielbild, aus dem Spiel gedacht)

Ein Einzelspieler-Remake lebt davon, dass die Bots **dieselben Wege gehen wie der Spieler, nur
schlechter**. Zielbild in fuenf Saetzen:

1. Ein Bot **baut, forscht, ruestet, bildet aus und kaempft** mit denselben Funktionen wie der Spieler
   (kein Sonderweg) - das ist heute ueberwiegend so und soll es bleiben.
2. Ein Bot **greift den Spieler an**, wenn er sich stark genug fuehlt, und **ruestet nach**, wenn der
   Spieler davonzieht (Reaktion auf den Spieler, nicht nur auf das eigene Dorf).
3. Ein Bot **handelt** (Waren gegen Rohstoffe, Karawanen) und **spioniert aktiv**.
4. Ein Bot **kennt den Drachen** - er greift ihn an, wenn er kann, und meidet das Gebiet sonst.
5. Bots haben **Profile** (Wirtschaftler, Forscher, Feldherr), die man im Spiel an ihrer Anzeige und
   ihrem Verhalten erkennt; Schwierigkeit ist eine Frage des Profils und der Startvorteile, nicht des
   Betrugs (keine geschenkten Ressourcen).

**Leitplanke (Daniel, Register 237):** Bots duerfen den Aufbau des Spielers bedrohen, aber sie duerfen
das Aufbauspiel nicht ersetzen - wer nur kaempft, soll verlieren, wer aufbaut, soll gewinnen koennen.

## 5. Ommage statt Kopie (Daniel 22:00)

"Mein Eigenes Spiel als ommage an das Nebelseetal." Folge fuer alle Entscheidungen:

- **Struktur und Geist bleiben:** Nebelsee, Siedlungen auf Karten, Goetterschutz, kein Sieg sondern
  Auszeichnungen, Bots als Mitspieler, Aufbau vor Kampf.
- **Zahlen und Feinheiten duerfen abweichen** (Rangfolge Register 238: Gesamtbalancing vor
  Originalwerten); jede Abweichung bleibt dokumentiert.
- **Was es NICHT wird:** ein reines Kampfspiel, ein Idle-Spiel, eine Kopie mit anderen Namen. Der
  Aufbau bleibt der Kern, das Erzaehlerische (Story, Stimmen) bleibt die Seele.
