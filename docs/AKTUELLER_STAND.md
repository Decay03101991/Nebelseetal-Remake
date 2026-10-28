> **WICHTIGER NEUERER STAND (FIX04j, 28.10.2026):** Oeffentliche Test-EXE wird getrennt vom Admin-Entwicklerbuild vorbereitet. Das Repository enthaelt **saemtliche** Admin-Module und Dokumente; nur der oeffentliche EXE-Einstieg bietet keine Admin-UI. Es liegt hier **noch kein gebauter und unter Windows abgenommener FIX04j-Release** vor. Details: `docs/RELEASE_PUBLIC_FIX04j.md`, neuester Protokollabschnitt. Aeltere Statusangaben weiter unten sind historisch und nicht automatisch gueltig.

> **Neuester isolierter GUI-Stand FIX04i (28.10.2026):** Im Adminbereich sind Ressourcen und Aktionen auf getrennten Zeilen; das Schildmotiv der vorhandenen Ladebild-PNG wird in Spieler- und Admin-Speicherfenstern als Hintergrund angezeigt, mit lesbarem Bedienfeld. Fachlogik von FIX04h bleibt erhalten. Neue und benachbarte Tests erfolgreich; **Windows- und EXE-Abnahme ausstehend.**

> **Neuester isolierter Entwicklungsstand FIX04h (28.10.2026):** Spielstandverwaltung aufgeraeumt: normale Spieler sehen nur aktive Slots und keine archivierten Fassungen; explizite Wiederherstellung nur im autorisierten Admin-Entwicklerarchiv mit klarer Slotzuordnung. Archivgroesse wird lesend angezeigt, keine automatische Loeschung. Kuenftige Beibehaltung/Begrenzung/Abschaltung des Entwicklungsarchivs **offen**. FIX04g unter Windows vom Nutzer bis Save→Archiv→Restore→Load bestaetigt; FIX04h erst unter Linux/Xvfb getestet, Windows-Neubau noch ausstehend.

> **Neuester isolierter Entwicklungsstand FIX04g (28.10.2026):** Pflicht-Starthilfe bis echte Grundproduktion, Admin-Hilfeausnahmen, private datierte Spielstandarchive, Spieler-/Admin-Slotverwaltung, manuelles Wiederherstellen. Details: `docs/ENTWICKLUNGSPROTOKOLL.md` / `docs/HERMES_UEBERGABE_AKTUELL.md`. **Nicht** als Windows-Release getestet; lokaler Windows-/GitHub-Stand kann abweichen.

# Nebelseetal Remake – EINZIGER aktueller Entwicklungsstand

**Stand:** 28.10.2026 | **Arbeitskopie:** konsolidierter GPT-Entwicklungsstand nach FIX01 und Originalkarten-Umstellung. **Nicht:** Hermes-HEAD / freigegebene Windows-Version.

## Projektstruktur

- `src/`: ein aktiver Spielcode; Einstieg `src/main.py`, Originalgrafik-Zuordnung `src/originalkarten_grafik.py`, Karten-Daten `src/originalkarten.py`.
- `assets/`: aktuell benötigte Spielgrafiken; `assets/karten/original/` die 127 unveränderten Quellbilder, `assets/karten/spielfeld/` die 127 daraus für den Spielbetrieb hergeleiteten 640×640-PNGs (nearest neighbor, keine erfundenen Landschaftssymbole).
- `data/`: Regeln und aktueller Originalkarten-Katalog (`originalkarten/katalog.json`, Grafikmanifest).
- `tests/`: aktive Tests; ältere 8×7-Tests liegen separat im Archiv und gelten **nicht** als bestanden.
- `tools/`: Bau-/Test-/Quellenwerkzeuge, z.B. `originalkarten_grafiken_bauen.py`, `build_exe.py`.
- `docs/`: ein aktuelles `ENTWICKLUNGSPROTOKOLL.md`, eine aktuelle Hermes-Übergabe, Quellen und aktueller Status.
- `archiv/`: alte Zwischenstände, Tests, Protokollfassungen, alte Übergaben, Bildstudien; **nicht veröffentlichen**.

## Aktueller Spielstand nach Systemen

| Teil | Implementiert / Bedeutung | Noch offen |
|---|---|---|
| Siedlungskarten | 127 historisch belegte Originalbilder, im Spiel als Bilder statt Zeichenvorschlag; 10×10-Daten/Index; freier Kartenvorrat | 25 automatisch klassifizierte Kartenraster visuell noch nicht abgenommen; Raster-Bild-Kongruenz manuell prüfen |
| Gelände | Originalbild zeigt Wald-Baumgruppen, Fels-/Berg- und Grasfelder, Gebäude/Wege/Koordinaten als separate Überlagerung | Unterschiede zwischen Pixelbild und automatisch erkanntem Feldtyp für die 25 ungeprüften Karten korrigieren |
| Frühere 8×7-Karten | Generator und Kartentypen im aktiven Spiel **abgeschaltet**; Quellen/Tests archiviert | Ältere Savegames nur als historische Dateien; keine automatische Migration / kein stilles Zurückkehren der alten Welt |
| Produktion / Wirtschaft | lokales Ortslager, Holz/Stein, Waren, Ausbildung, Forschung, Karren | Altprüfungen auf Originalkarten umstellen, echte Regressionen reparieren, keine kostenlosen Bot-Ressourcen |
| Bau-Menü | Bau-/Auswahlfunktionen; Screenshots `docs/nebelseetal_gamestar2.jpg` als Referenz | historische Bauoberfläche (Navigation, Kosten, Siedlerbedarf, Baufelder) noch nicht vollständig nachgebaut |
| Kampf / Mauern / Bots | Grundfunktionen, lokaler Wall/Kampf/Beute | KI-Ökonomie, Belagerung, gesamter End-to-End-Durchlauf |
| Speichern / Laden | 3 Spielerslots und Adminbereich, Schutz vor nicht-originalen Kartenständen im Ladepfad | Reale Windows-Spielstände prüfen; kein verdecktes 8×7-Upgrade; nötigenfalls getrennte manuelle Import-Routine mit Freigabe entwerfen |
| Windows EXE | Python-Spiel plus `.bat`-Buildablauf | **Keine** aktuelle auf Windows neu kompilierte/verifizierte EXE in dieser Lieferung |
| GitHub | Öffentliche Seite `Decay03101991/Nebelseetal-Remake` | Hermes nach Rückübernahme zuständig für geprüfte Commits, Protokoll- und README-Pflege; keine Zugangsdaten/Archive veröffentlichen |

## Getestet und nicht getestet

- Vor der Originalgrafik-Umstellung: 35 ausgewählte Tests, 34 erfolgreich, 1 alter Kartenansichtstest mit 11 Fehlkontrollen. Nicht als komplette Suite zählen.
- Nach der Umstellung: neuer Originalkarten-Test besteht mit **7/7**; darin Nachweis aller 127 Bilddateien, Bilddatei-Prüfsummen, GUI-PhotoImage-Smoketest und Sperren gegen Legacy-Karten.
- Separate Nachbartests wurden selektiv geprüft; nicht alle älteren Testfälle gelten für die aktuelle Datenstruktur (siehe `archiv/tests_legacy_8x7/`).
- **GPT-FIX02 (28.10.2026):** `test_startspiel.py` nun **61/0/1** (Nahrung vs. Holz-Grundrate korrekt, 100 Originalkarten-Feldtags, Baukunst->Akademie->Ausbildung). `test_durchspiel.py` **64/0/2** (Bauen/Forschung/Ausbildung/Handel/Save/Load/Portal/Werkstatt inklusive Fertigstellung). `test_gpt_wall_gui.py` **4/4**, neuer `test_gpt_originalkarten_feldklick.py` **2/2**. 24 gezielt ausgewählte Testdateien nach Korrekturen gruen; `test_gui_fehler.py` anfangs blockiert, nach Ersetzung veralteter Dialog-/Wall-/Slot-Annahmen **23/0/1**. Dies ersetzt die alten historischen Befunde NUR fuer diese geprueften Dateien, nicht fuer die Gesamtsuite.
- Keine reale Windows-EXE, keine vollständige Windows- oder Gesamtspielabnahme. Release-Status: **NEIN**.

## Next actions für den temporären Coding-Agenten

1. Original-Raster und sichtbares Originalbild für die 25 Karten manuell Feld für Feld abnehmen; automatische Klassifikation nicht ungeprüft korrigieren.
2. Historische Wirtschafts-/Baumenü-Tests mit 10×10-Originalkarten neu aufbauen (Archiv bewahren), fehlende UI-Funktionen implementieren.
3. Bot-Ökonomie, Handel, Produktion, Kampf, Save/Load als echte Spielrunde nachweisen.
4. Unter Windows aus `EXE_NEUESTEN_STAND_BAUEN.bat` kompilieren, startetest und Releaseprüfung.
5. Hermes nach Rückkehr gegen sein reales Git-HEAD vergleichen lassen; nur nach Tests offizielles Repo aktualisieren.

**Führende Detaildokumente:** `docs/HERMES_UEBERGABE_AKTUELL.md`, `docs/HERMES_KONTROLLE_UND_SKILLS.md`, `docs/KARTEN_NUR_ORIGINALE.md`, `docs/ENTWICKLUNGSPROTOKOLL.md`.

**Zusaetzlicher Speichertest (28.10.2026):** `tests/test_originalkarten_savegames.py` ist mit 2/2 gruen: eine neue echte Originalkarte uebersteht Save/Load und eine alte 8x7-Karte wird vor Zustandsschaeden abgewiesen.


## Letzte Entwicklungsrunde – GPT-FIX02, 28.10.2026

Die einzige aktive Spiellogik-Aenderung ist in `src/main.py`: 100 unsichtbare Felderkennungen ueber dem unveraenderten Originalkartenbild. Dazu wurden die Durchspiel-/Wall-/Starttests auf reale Spielregeln und Originalkarten angepasst und eine neue GUI-Regression ergaenzt. **24 selektierte Testdateien bestehen, darunter der reparierte GUI-Aktionstest mit 18 Ansichten/13 Aktionen.** Kein neuer Windows-Build. Keine GitHub-Aktualisierung – die erfolgt auf ausdruecklichen Wunsch Daniels erst am Ende. Alle Einzelheiten und Befunde siehe `docs/ENTWICKLUNGSPROTOKOLL.md` Abschnitt GPT-FIX02.


### Ergänzende Originalkarten-Bauprüfung – GPT-FIX02b

`tests/test_gpt_originalkarten_baukasse.py`: unter Tkinter/Xvfb **4/4 erfolgreich**: Ortslager-Zahlung ohne Doppelbuchung, belegte Felder bleiben unverändert, Rohstoffmangel ohne Seiteneffekte, echtes Originalkartenbild nach Bau. Damit sind **25 ausgewählte Testdateien** grün. Die 11 alten Kartenansicht-Fehlkontrollen sind noch **nicht** vollständig ersetzt (siehe einziges Entwicklungsprotokoll). Kein neuer Windows-Build oder GitHub-Push.


## Zusatzprüfung GPT-FIX02c (28.10.2026)

Der von Daniel wieder zusammengesetzte Stand ist bytegenau identisch mit dem FIX02-Paket (1.229 Projektdateien). Zusätzlich lokales `.git` aus altem Hermes-Head, aber **kein** aktueller Windows-EXE-Build. Historische Protokoll-/Zielübergabe-Pfade in isolierter Kopie korrigiert (belegt im einzigen Entwicklungsprotokoll). Zehn zentrale Spieltestdateien nach Entpackung bestanden; die vollständige Testsuite und ein Windows-Praxistest fehlen. Neue GitHub-Fassung darf erst nach Sichtung des GitHub-Clone-Diffs, Geheimnis-/Rechtekontrolle und echter Windows-Prüfung zum Release werden.

**FIX02c Buildgate-Nachtrag:** Vorprüfskript auf vorhandenen Originalkarten-Katalogtest korrigiert; 6/6 unter Linux/Xvfb erfolgreich. Keine Windows-EXE vorhanden oder freigegeben. Drei fehlende Tests im historischen GPT-Abschluss-Teststarter bleiben offen.


### FIX04 – aktueller isolierter Entwicklungsstand vom 28.10.2026

- Kartenbild: weiterhin ausschliesslich die authentischen 127 Siedlungskarten 10x10; Originalbilder nicht veraendert.
- Siedlungs-Baumenue: Bereiche Produktion/Werkstatt/Ausbildung/Verteidigung/Sonstiges im Auswahlfeld, je Bauangebot Zweck, Ertrag, Preis, Siedler- und Forschungsbedarf sowie konkrete Sperr-/Fehlmengen. Eine einzige Baukasse und ein einziger Bauaktionsweg bleiben erhalten; Dorfwall bleibt separate Siedlungsfunktion.
- GUI-Kontrolle: neuer FIX04-Test **5/5**, Spielstarttest **61/0/1** nach korrigierter Beschriftungserwartung; weitere ausgewählte Spieltests bestanden. Vollsuite und Windows-FIX04-EXE noch offen.
- Letzter praktischer Windows-Build: FIX03 unter Python 3.11.16 (Astral), von Daniel mit funktionierendem Start, Admin und Speichern/Laden bestaetigt. Jede Codeaenderung FIX04 erfordert danach einen *neuen* Windows-Build; noch kein GitHub-Push.
- Offene Risiken: GUI bei kleiner Bildschirmaufloesung; alte Weltregionen in `main.MAPS` (nicht mit 127 Original-Siedlungskarten verwechseln), Bot-Oekonomie/Belagerungen, 25 visuelle Kartenraster und alle Tests vor Release.


### 28.10.2026 – Vorlaeufige Entwicklung FIX04d (noch nicht Windows-veroeffentlicht)

FIX04 ergaenzt das Baumenue der 127 Originalkarten um Rubriken und regelbasierte Statusanzeige. FIX04b/c enthalten Standorttipps und eine begleitende Spielerhilfe mit zehn Fragen. FIX04d ergaenzt einen nur im Admin-Teststand zulaessigen Anzeige-Override (`auto`, `anzeigen`, `ausblenden`) ohne Eingriff in den Goetterschutz. 7/7 neue Admin-Tests erfolgreich; benachbarte GUI-, Start-, Save- und Durchspieltests erfolgreich. Vollsuite, Windows-FIX04d-EXE, Botwirtschaft und 25 visuell offene Kartenraster bleiben offen. Auf GitHub ist dieser Stand noch **nicht** veroeffentlicht; bisherige FIX03-EXE ist nicht FIX04d.
