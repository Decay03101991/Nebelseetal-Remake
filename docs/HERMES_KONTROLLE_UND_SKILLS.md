# Hermes – Leitregeln, Skill-Prüfung und Kontrollübernahme

**Autorität:** Hermes ist und bleibt Head-Koordinator. ChatGPT führt zeitweise isolierte Coding-Arbeit aus. Dieser Text gibt Hermes auch mit begrenztem Kontext / einem kompakten Modell einen sicheren Wiedereinstieg.

## Sofortstart für Hermes (abzuarbeiten)

1. `docs/AKTUELLER_STAND.md` → `docs/HERMES_UEBERGABE_AKTUELL.md` → aktuelle Abschnitte in `docs/ENTWICKLUNGSPROTOKOLL.md` lesen. `START_HIER.txt` ist archiviert, keine parallele alte Übergabe verwenden.
2. Echtes lokales Git-HEAD und bisherige Roadmap vergleichen; **nicht** behaupten, dass diese ZIP-Fassung automatisch auf dem lokalen Head oder GitHub liegt.
3. Prüfe `archiv/manifeste/ORDNER_UMZUGSPLAN.json` und `archiv/manifeste/ORIGINALKARTEN_UMSTELLUNG_20261028.json`. Die alte Hermes-Version und bisherige Tests bleiben im Archiv, nicht blind überschreiben.
4. `tests/test_originalkarten_only.py` starten (Tk unter Windows), `run_tests.bat` sowie vollständige E2E-Checks; Fehltext **und** Rückgabecode prüfen.
5. Ungeprüfte Karte-Raster, Bot-Ökonomie, Baumenü und Windows-Build als offen weiterführen. `docs/ENTWICKLUNGSPROTOKOLL.md` ist das **einzige** aktuelle Protokoll.
6. Freigabe nur nach nachvollziehbarem Diff und Regression. Anschließend GitHub-Commit/Push durch Hermes, README und Besucherstatus aktualisieren.

## Regeln, die bestehen bleiben müssen

- **Originaldaten vor Annahmen:** 127 Siedlungskarten 10×10 aus Originalbildern, keine nachgebauten Fantasie-Raster; 25 Raster weiter offen. Original-Quellgrafik/Hash bleibt unverändert.
- **Ein Code-Stand:** `src/main.py` und alle verwendeten Module nur in EINER aktiven Hauptversion; kein alter Parallel-Ordner als zweites Spiel. Gemeinsame Dateien nicht gleichzeitig durch mehrere Kind-Agenten ändern.
- **Ein Entwicklungsprotokoll:** `docs/ENTWICKLUNGSPROTOKOLL.md` mit Datum, Beleg, Testresultat und geänderten Pfaden. Frühere Protokolle ausschließlich `archiv/`.
- **Ein aktiver Status und eine aktive Übergabe:** `docs/AKTUELLER_STAND.md`, `docs/HERMES_UEBERGABE_AKTUELL.md`. Keine neuen `START_HERMES_*`, `GPT_STATUS_*` als Parallelwahrheiten.
- **Lernen aus Regressionen:** Ursache → Abstellmaßnahme → automatisierter Test → Skillregel. Nur neue Skills/Regeln ergänzen, wenn vorhandene nicht reichen. Nach Patches Dateien zurücklesen und erneut messen.
- **Passwort und Privatdaten:** `tor.json`, `admin_tor.json`, `.env`, Schlüssel, Spielstände, Archive keinesfalls in öffentlichen GitHub-Commits. Spieler legt sein eigenes Startpasswort fest; kein echter Kopierschutz bei Python-Code.
- **Keine falsche EXE:** Windows-Neubau aus aktuellem Code, Hash/Buildprotokoll, echter Start-/Speichertest, erst dann Freigabe. Eine alte EXE im Archiv bleibt alt.
- **Fehler sichtbar halten:** kein Test 'grün' melden, wenn 8×7-Tests nur verschoben sind; aktive/archivierte Testmengen und kritische Fehlfunktionen getrennt berichten.
- **Kontextbudget beachten:** diesen Text als Einstieg, ergänzende Tiefenrecherche nur bei anstehendem Arbeitsschritt. Compact Checkliste statt alle alten Dokumente ins Kontextfenster laden.
- **Bots:** interne wirtschaftliche Versorgung plausibel (keine Gratis-Truppen); Kommunikation an Bots erst in späterer Entwicklungsphase, automatische Spielereignisse weiterhin vorgesehen.

## Skills, die Hermes prüfen bzw. schärfen muss

| Skill / Kompetenz | Konkrete Anpassung |
|---|---|
| Git und sichere Veröffentlichung | Aktiven Spielkern und öffentliche Dateien synchronisieren; Archiv/Secrets nicht pushen; Remotestand nach Push prüfen |
| Repository-Aufräumen | Alt→Neu-Pfade lesen, beim Refactoring Import-, Test- und Buildpfade automatisiert prüfen |
| Originalquellen-Grafik | Karte, Grafikmanifest und 10×10-Feldtyp als Trio validieren; 25 offene Karten manuell nacharbeiten |
| Python/Tkinter-GUI | Echte Originalgrafik verwenden, Overlays separat; tk.PhotoImage-Referenz halten; Tk-Smoketest auf Windows |
| State/Persistenz | Alte 8×7-Stände nicht stillschweigend migrieren, Abbruch vor Mutation; Originalkarten-ID je Siedlung verifizieren |
| Economy/Kampf-Bots | Lokal gebuchte Ressourcen, reale Kosten, Save/Load, Transport und Belagerung als Regressionen |
| Test-Harness | Test-Erfolg anhand Rückgabe + Inhalt; archivierte Legacytests separat erfassen und neu modellieren |
| Windows-PyInstaller | Alle Originalgrafiken ins Build nehmen; keine vorhandene alte EXE als neuesten Build ausgeben |
| Dokumentation/Protokoll | Nur eine aktive Chronik; neue Aufgaben zuerst in Status, dann Detaildoku; keine duplizierten Übergaben |
| Rechte/Quellen | Nachweis der Nutzungs-/Veröffentlichungsrechte für historische Bilder und Dokumente vor öffentlichem GitHub-Push |

## Hermes-Abarbeitungszustände (nicht verwechseln)

- **Fertig in isolierter GPT-Kopie:** Originalkarten-Hintergrund, neues Verzeichnis, getestete Quellgrafikzuordnung, ältere Generatoren deaktiviert, Archivierung und Übergabe.
- **Offen:** Übernahme in Daniels tatsächliches Projekt/Git, vollständige 88er-Suite, 25 Grafikraster, authentische Baumenü-GUI, Windows-EXE, Releasetest und Rechtefreigabe.


## GPT-FIX02d-R2 - Projektordnung als lernender Cleanup-Check

**Ab jetzt keine `START_HIER.txt` und keine zweite aktuelle Projektuebersicht anlegen.** Start-/Testanleitung gehoert in `README.md`, Hermes-Checkliste und Arbeitsauftrag nach `docs/HERMES_UEBERGABE_AKTUELL.md`, Entwicklungen nach `docs/ENTWICKLUNGSPROTOKOLL.md`, spielbereichsbezogener Ist-Stand nach `docs/AKTUELLER_STAND.md`. Kein zweites Statusdokument. Beim Laptop-Cleanup nach **verifizierten** Duplikaten, alten Links und unbenutzten Dateien suchen; nur Belege + Vorschlaege liefern, nicht automatisch verschieben/loeschen. SHA-256 und Alt->Neu-Pfad, Leser/Imports und Testfolgen dokumentieren. `tools/projekt_ordnung_audit.py` ist ein read-only Werkzeug, das Hermes nach Pruefung in seinen bereits bestehenden Cleanup-Cronjob integrieren soll. Noch kein Cronjob und kein Hermes-Skill wurden durch ChatGPT auf Daniels Laptop veraendert.


## Hardware-Rahmen fuer ressourcenschonende Entwicklung (GPT-FIX02d-R2)

Daniels Testrechner: Windows 11 Home x64, Windows-Build 26300 (Angabe vom 28.10.2026), Intel 64-Bit-CPU (ca. 2,3 GHz), rund **12 GB RAM**. Bei der Auskunft waren nur ca. **3,1 GB physischer RAM frei**; das ist eine Momentaufnahme, nicht dauerhaft verfuegbarer Speicher. Vor grossem EXE-Build freien RAM und **freien Festplattenspeicher** neu pruefen; letzterer wurde nicht angegeben. Python und PyInstaller in 64 Bit verwenden, Builds/Tests nacheinander statt parallel ausfuehren, unnoetige speicherintensive Programme schliessen. Unter Windows pruefen: Interpreter, Tkinter, Compiler-/Build-Log, Dateipfade, Laufzeitstart, Grafik/Originalkarten, Spielstand. Nichts als Windows-verifiziert bezeichnen, was nur unter Linux geprueft wurde.

**Datenschutz:** E-Mail, Windows-Produkt-ID, Netzwerkadressen, Hostname, exakte BIOS-Kennungen und andere nutzerbezogene Systeminformationen NICHT in Repo, Diagnoselogs oder externe Uebergaben uebernehmen. Nur notwendige, nicht identifizierende System- und Ressourcenangaben sind hier festgehalten. Keine versteckte Telemetrie, keine automatischen Downloads ohne Freigabe. Fuer den bereits bestehenden Laptop-Cleanup zuerst reale Aufgabenplanung/Task-Scheduler/Cron-Definition sowie bestehende Skills feststellen; nur einen read-only Vorschlag fuer Ordnungsscans an passender Stelle integrieren und keinesfalls mehrere redundante Cleanup-Jobs anlegen.


## Skill-Ergaenzung FIX04

- Baumenue-Kategorien aus `data/buildings.json`; keine weitere zweite Preis-/Forschungskonfiguration.
- Statusanzeigen verwenden `bauen_auf_karte(..., nur_pruefen=True)`, `baukosten` und `ortsdeckung`. Echte Transaktion ausschliesslich ueber `_karten_bauen` / `verbrauche_am_ort`.
- In realen Tk-Tests ueber sichtbare Bedienelemente wechseln und Feld-/Lagerzustand pruefen. Etikettentext ist kein kanonischer Gebaeudeschluessel.
- Laptop-Cleanup als **Vorschlagsroutine** erweitern: doppelte Starter und Dokumente, alte Pfade, verwaiste Testreferenzen und auseinanderlaufende GitHub-README/Hermes-Statusdateien erfassen, aber keine Spiel- oder Protokolldatei automatisch loeschen. Realen Cronjob erst nach Hermes-Neustart mit Freigabe aendern.
- Nutzer-Umgebung: Windows 11 x64, ~12 GB RAM, Windows-Python 3.11.16 (Astral/uv) mit Tkinter und PyInstaller; WSL Ubuntu-Python 3.14.4 ist separat. Build/Tests ressourcenschonend nacheinander; weder private Hostdaten noch Zugangsdaten ins Repo.


### FIX04d – Pflichtregel: Admin-Testbarkeitspruefung je groesserer Funktion

Vor einer groesseren GUI-, Wirtschafts-, Zeit-, Kampf-, Speicher- oder Kartenfunktion dokumentieren: (a) Admin-Testfall erforderlich? (b) Option fuer gezieltes An/Aus oder Reproduzieren, ohne eigentliche Spielmechanik zu verfaelschen? (c) saubere Berechtigungsgrenze und getrennte Spielstaende? (d) resetbare Voreinstellung? (e) Regressionen normal + Admin, inklusive Save/Load, Anzeige und Schutz vor Nebeneffekten? **Nicht pauschal Cheats schaffen**. Das aktuelle Muster ist `admin_werkzeuge.spielerhilfe_modus_setzen` mit `auto/anzeigen/ausblenden`; ausschliesslich die Anzeige wird uebersteuert, nicht der Götterschutz. Hermes vergleicht diese Regel mit bestehenden Skills und uebernimmt sie ohne Dopplung. Neue Regeln im zentralen Protokoll und bestehendem Cleanup-Pruefplan pflegen; keine automatischen Datei-Loeschungen.
