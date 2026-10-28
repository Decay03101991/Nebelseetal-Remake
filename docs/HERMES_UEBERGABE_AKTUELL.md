# VORRANGIGE WIEDERAUFNAHME – GPT-FIX04j (28.10.2026)

**Hermes ist und bleibt ALLEINIGER HEAD-KOORDINATOR.** Vorherige Kapitel darunter sind Historie; neuester vorläufiger Arbeitsstand ist FIX04j. Nutzerforderung: **vollständiges GitHub-Repository inklusive Admin-Code, Admin-Tests, Admin-Dokumentation**. **Nur die öffentliche Windows-Test-EXE soll im Spielmenü keinen Adminzugriff bieten**. Der Adminbereich bleibt in der lokalen Entwicklerfassung erhalten.

**Nach Wiederaufnahme exakt diese Reihenfolge:** (1) `docs/ENTWICKLUNGSPROTOKOLL.md` neuesten FIX04j-Abschnitt und `docs/RELEASE_PUBLIC_FIX04j.md` lesen. (2) den eigenen tatsächlichen lokalen Git-HEAD und das Windows-Hauptprojekt mit dem isolierten FIX04j-Patch abgleichen, keine Archive blind überschreiben. (3) `src/main.py`, `src/public_start.py`, `src/ausgabemodus.py` auf ordentliche Editionssperre, Datenschutz und fehlerfreie normale Slots prüfen. (4) `tools/build_public_exe.py` und `PUBLIC_TEST_EXE_BAUEN_WINDOWS.bat` auf Windows ausführen; Windows Public-Build und separate Entwickler-EXE manuell testen. (5) Öffentliches Repo mit allen Admin-Quellen und Dokumenten, Tests und aktuellen Karten pflegen, aber nie private Archive, Token, Passwörter, Saves, lokale `.env` oder alte ZIPs hochladen. (6) GitHub Releases erst nach Rechte-/Sicherheits-/Praxistest als Vorabversion freigeben und den verwendeten Commit dokumentieren.

**Neu für Hermes-Lernaufgabe, Skills und Laptop-Cleanup:** Unterschied zwischen *Edition*, *Berechtigung* und *Source Control* systematisch prüfen. Ein UI-versteckter Adminbereich ist bei öffentlich lesbarem Python-Code **keine** harte Sicherheitsgrenze. Bei jedem Release muss vollständig dokumentiert sein, welche Quellen ins GitHub-Repo kommen und welche Laufzeitfunktionen im Public-Build ausgeschaltet sind. Separater Speicher- und Passwortpfad ist Pflicht. Build-Output, Archive und sensible Daten im Cleanup nur vorschlagen/prüfen, nie blind löschen. Bestehende Skills vor Erweiterung lesen und Dopplungen vermeiden. Cronjob selbst hier nicht geändert.

**Explizite offene Punkte:** FIX04j wurde in einer isolierten Linux-Umgebung vorbereitet und getestet, **nicht unter Windows als neue EXE gebaut** und **nicht gepusht**. Historische Spielstände und Entwickler-EXE unangetastet. Manuell Windows, Slotpersistenz, kein Admin-Einstieg, GUI/DPI, ZIP-Prüfsumme, Rechte für Originalmaterial und eventuell veraltete Statuspassagen prüfen. Für Systemanforderungen keine ungetestete Mindestzahl behaupten. Archivaufbewahrung für öffentliche Testversion bleibt offen.

---

# VORRANGIGE UEBERGABE – FIX04i (28.10.2026) – GUI-Schildmotiv, Admin-Leiste

**STATUS:** isolierter Testpatch auf FIX04h. Hermes bleibt alleiniger Hauptkoordinator. Bestehende Spielstandverwaltung/Privatarchive NICHT umbauen; normale Spieler sehen weiter nur aktive Slots. Kein GitHub-Push und keine EXE-Freigabe erfolgt.

**Neu:** `src/main.py::_build_main_ui` teilt die zu kleine obere Leiste in Ressourcen- und Aktionszeilen; der zuvor abgeschnittene Button `Admin-Spielstaende` bleibt erreichbar. Ein zentraler `_schild_dialog_inhalt` nutzt **die unveraenderte originale PNG** `assets/loadingpage/Nebelseetal_Loadingpage.png` als sichtbaren Schildhintergrund fuer Speicherslot-Laden/Speichern, Slotverwaltung und Admin-Entwicklerarchiv. Links bleibt eine deckende, gut lesbare Bedienflaeche. Kein zweites oder erfundenes Motiv, keine PIL-Runtime-Abhaengigkeit, keine Spielregel-/Berechtigungsveraenderung. Bei fehlender Grafik funktionieren die Dialoge weiterhin.

**Verifizierte Tests unter Linux/Xvfb:** FIX04i GUI 6/6, FIX04h Slot-GUI 6/6, FIX04g Speicherarchiv 13/13, Profillogin 9/9, Admin-Hilfe 7/7. Keine Windows-Freigabe und nicht die gesamte Suite. Der bisherige FIX04h Spielstandsarchiv-Test wurde nur auf rekursive Widget-Suche angepasst, weil eine neue Layout-Frame-Ebene dazwischen liegt.

**Hermes-Checkliste nach Wiederaufnahme:** (1) EINZIGES aktuelles Protokoll `docs/ENTWICKLUNGSPROTOKOLL.md` Abschnitt GPT-FIX04i lesen; (2) lokales Git-HEAD/FIX04h-Basis vergleichen; (3) Patch einzeln pruefen und zulaessig integrieren; (4) Windows 11 UI mit DPI-Skalierung, Admin- und Normalprofil testen; (5) Isolationsrechte und Spielstandarchiv kontrollieren; (6) EXE neu bauen und pruefen; (7) GitHub erst nach Geheimnis-/Rechte-/Releasepruefung aktualisieren. UX-Regel: Originalassets zentral nutzen und Nebenfenster konsistent halten, Aktionen auf schmalen Fenstern nicht abschneiden; Cronjob/Cleanup darf GUI-Assets nicht als ueberfluessiges Duplikat einstufen.

---

# VORRANGIGE UEBERGABE – FIX04h SPIELSTAND-UI (28.10.2026)

**Immer diese Zeilen vor den historischen Nachtraegen lesen.** Hermes bleibt alleiniger HEAD-KOORDINATOR, ChatGPT nur zeitweilig Coding-Agent auf isolierter Projektkopie. GitHub ist bis zur verifizierten Freigabe unveraendert.

**Nachgewiesener Nutzerablauf:** In FIX04g wurden unter Windows Speichern → Archivieren Slot 2 → Wiederherstellen → Laden erfolgreich ausprobiert. Das alte GUI zeigte dabei eine Wiederherstellungszeile optisch zwischen Slot 2 und dem leeren Slot 3. Normale Spieler sollten entfernte Staende nicht automatisch wieder als Ladeangebote sehen. Das Archiv kann mit der Zeit unbegrenzt anwachsen.

**Neu in FIX04h:**
1. `src/main.py::_spielstand_verwaltung` zeigt im NORMALEN Profil nur noch aktive Slots 1–3 mit korrektem Slotstatus und gesicherter Loeschaktion. Es werden **keine** archivierten Standslisten, Restore-Auswahlfelder oder automatischen Wiederherstellungsangebote gerendert.
2. Nur ein **explizit authentifizierter Admin-Teststand** kann `src/main.py::_archiv_wiederherstellung_dialog` oeffnen. Im Admin-Werkzeug gibt es getrennte Zugriffe auf Admin-Testarchiv und normale Spielerslot-Archive (letztere zur Entwicklung/Fehleranalyse). Die GUI listet nur wirklich vorhandene Archive mit **klarer Slotnummer und Datum/Zeit** auf. Kein Phantom-Restore fuer Slot 3. Rueckspielen ist explizit zu bestaetigen; ein belegter Slot erfordert ebenfalls bewusste Ueberschreibung. ARCHIVQUELLE BLEIBT BESTEHEN.
3. `src/spielstand_archiv.py::archiv_groesse` zaehlt privat/lesend Dateien und Bytes, ohne Loeschung. Admin-Werkzeug zeigt Groesse und Warnung ab 250 MiB. Automatische Loeschung, Ablaufdatum, Komprimierung und Loesch-Automatisierung sind **nicht** implementiert.
4. Bei RELEASE-Planung erneut Nutzerentscheidung einholen: Entwicklungsarchiv abschalten oder als optionale sichere, begrenzte Sicherung weiterfuehren? Vorher keine automatischen Loeschungen, keine echten Spielstaende auf GitHub, keine Migration von privaten Daten ohne Test. WARNUNG: Normalspieler koennen derzeit geloeschte Staende nicht direkt selbst rueckholen; dies ist eine bewusste Entwicklungsvorgabe, nicht als endgueltiges Produktkonzept freigeben.
5. Fuehrender Beleg: EINZIGES `docs/ENTWICKLUNGSPROTOKOLL.md` Abschnitt GPT-FIX04h; neuer Test `tests/test_gpt_spielstand_gui_fix04h.py`, aktualisiert `tests/test_gpt_spielstandarchiv_fix04g.py`, `run_tests.bat`. Nur `src/main.py` und `src/spielstand_archiv.py` aendern die Laufzeit. Andere Funktionen, Startskripte und aktive Karten unveraendert. Linux-Xvfb-Tests sind keine Windows-EXE-Freigabe.

**Konkrete Wiederaufnahme (auch fuer kleines LLM):** (1) Diese Uebergabe lesen; (2) `docs/AKTUELLER_STAND.md` und einziges Protokoll lesen; (3) aktuellen lokalen Windows-Git-HEAD sowie `PROJEKTDATEIEN` des FIX04h-Patches vergleichen, keine historische ZIP blind integrieren; (4) ausgewiesene Testdateien einzeln, dann volle Suite testen, auf Testtext UND Exitcode achten; (5) Windows-EXE aus aktueller Quelle bauen und Save-Archivierung/Restore mit Testslots pruefen; (6) erst nach Geheimnis-, Rechte- und Buildpruefung GitHub aktualisieren, Protokoll fortschreiben. Hermes uebernimmt Skills/Cleanup-Regeln nur nach Abgleich mit seinen vorhandenen Skills; keine Dubletten.

---

# VORRANGIGE UEBERGABE – FIX04e/f/g (28.10.2026)

**Hermes bleibt alleiniger HEAD-KOORDINATOR.** ChatGPT implementiert nur temporaer in getrennter Arbeitskopie. Keine automatischen GitHub-Pushes, keine geheime Konfiguration im Paket. Fuehrender Nachweis: `docs/ENTWICKLUNGSPROTOKOLL.md` Abschnitt `GPT-FIX04e/f/g`. Diese Fassung ist ein kumulativer Patch **gegen FIX04d**. Fuer einen anderen realen Git-HEAD zuerst diffen und kontrolliert integrieren.

**Neue Nutzerregeln:**
1. Dorfzentrum-`Dein naechster Schritt` ist **Pflicht** bis eine erste Siedlung existiert und dort **aktiv** Holz, Stein und Nahrung produziert wird; passives Anfangseinkommen reicht nicht. Dies hat Vorrang vor `ausblenden` und Ende des Goetterschutzes. Die rechte allgemeine Hilfesaeule respektiert weiterhin Admin-Override und Schutzstatus.
2. [HISTORISCH FIX04g - DURCH FIX04h ABGELOEST] Alle normalen Spielslots und der separate Admin-Teststand besassen `Loeschen (archivieren)` und `Wiederherstellen`. Absichtliches Ueberschreiben per Save/Neu-Teststand ersetzt direkt und erzeugt kein zusaetzliches Archivereignis; die technische `.bak`-Datei des Speicher-Moduls bleibt.
3. **Privates Runtime-Archiv** im jeweiligen Save-Ordner: `archiv/spielstaende/spieler/slot_1..3/`, `archiv/spielstaende/admin/`, `archiv/spielstaende/abgebrochen/`, `archiv/spielstaende/testbereinigung/` (letzterer nur vorbereitet). Jede Loeschung im Spiel per datiertem Eventordner; Restore nur auf explizite Anweisung. `archiv/spielstaende/` IM PROJEKT zeigt eine leere Musterstruktur. Keine echten Saves in GitHub; `.gitignore` pruefen.
4. Lernregel fuer Skills und Laptop-Cleanup: **Speicherverlustpraevention**. Jede neue Loesch-, Reset-, Testbereinigungs- oder Migrationsfunktion erst auf `archiviere statt loeschen`, eindeutigem Datum/Zeit/ID, Berechtigung, Wiederherstellbarkeit, Backup-/Overwrite-Ausnahme und GitHub-Ausschluss pruefen. Keine automatischen Archivloeschungen. Vorschlaege im existierenden Cleanup-Cronjob erst nach Abgleich und Freigabe umsetzen; Cronjob selbst wurde NICHT geaendert.
5. Nach Wiederaufnahme `src/main.py`, `src/spielstand_archiv.py`, `src/speichern.py`, `src/spielerhilfe.py`, `run_tests.bat`, `.gitignore` und drei neue `tests/test_gpt_*_fix04e/f/g.py` pruefen. Windows-EXE aus NEUEM Quellstand bauen und reale Save-Archiv/Restore-Tests mit kuenstlichen Testdaten ausfuehren; nicht die aeltere EXE als neuen Stand ausgeben.

**Teststand:** 12 gezielt ausgewaehlte Testdateien erfolgreich (genaue Zahlen im Protokoll), Linux/Xvfb, keine komplette Suite und keine Windows-Freigabe.

---

# EINZIGE AKTUELLE UEBERGABE FUER HERMES

## VORRANG: Aktueller Arbeitsstand FIX04d – 28.10.2026

**Zuerst diesen Absatz lesen, dann die Chronik weiter unten.** Hermes ist alleiniger Head-Koordinator und bleibt verantwortlich fuer Roadmap, Git-Integration, offizielle Freigaben, Skills und Cronjob. ChatGPT hat zeitweise den Code in einer **isolierten** Hauptfassung erweitert; keine Aenderung an Daniels laufendem Windows-Hauptordner oder GitHub durch ChatGPT. Voller Nachweis: `docs/ENTWICKLUNGSPROTOKOLL.md` (Abschnitt GPT-FIX04c / FIX04d). Der alte Hinweis auf `START_HIER.txt` ist historisch; aktuelle Einstiege: `README.md` (Spielstart), diese Datei (Hermes), `docs/AKTUELLER_STAND.md` (Bereiche), `docs/ENTWICKLUNGSPROTOKOLL.md` (einziges aktives Protokoll).

**Neuer Spielstand:** 127 originale 10x10-Siedlungskarten als Runtime-Grafik; historisches kategorisiertes Baumenue, Standorttipps und eine Spielerhilfe mit zehn Fragen sind in der GPT-FIX04d-Arbeitskopie. Das Hilfepanel erscheint automatisch nur waehrend des echten Goetterschutzes; ueber "Spielerhilfe" ist die Hilfe immer erreichbar. **Admin-Ausnahme:** Admin-Werkzeuge → "Spielerhilfe / Anzeige": `auto`, `anzeigen`, `ausblenden`. Diese Auswahl gilt nur fuer den separaten Admin-Teststand und aendert keinen Kampf- oder Schutzwert; das Speichern ist ausschliesslich im Admin-Save erlaubt. 7/7 spezielle Tests plus benachbarte Regressionen erfolgreich, **keine** komplette Suite/Windows-FIX04d-Abnahme.

**Naechste Uebernahme-/Lernaufgaben fuer Hermes (in dieser Reihenfolge):**
1. Aktuellen Windows-Stand und Git-HEAD, `README.md`, `docs/AKTUELLER_STAND.md`, dieses Protokoll und `archiv/manifeste/` lesen. Nie unkontrolliert Archive zurueckkopieren.
2. FIX04d-Delta mit dem echten Hauptstand vergleichen, Tests unabhaengig ausfuehren und neue Windows-EXE aus aktiven Quellen bauen. FIX03-EXE war beim Nutzer lauffaehig, enthaelt aber FIX04d nicht.
3. Im Admin-Teststand vor/nach Schutzende die drei Modibedingungen pruefen, anschliessend Adminstand speichern/laden. Normalen Spielerslot unabhaengig pruefen.
4. Neue **Admin-Testbarkeitspruefung als Skill-Regel** pflegen: bei jeder groesseren Spielaenderung gezielt nach Ein/Aus, Reset, Reproduzierbarkeit, Berechtigung und Seiteneffektfreiheit fragen. Nicht ungeprueft Cheats einfuehren. Regressionstests und genaues Protokoll sind Pflicht.
5. Eigenen Laptop-Cleanup-Cronjob und Skillbestand auf doppelte/veraltete Anleitungen, falsche Pfade und redundante Protokolle **read-only** pruefen; Vorschlaege ausarbeiten; nicht automatisch aktiv loeschen oder Cronjob ohne separate Freigabe aendern.
6. Erst nach Sicherheitspruefung und Freigabe öffentliche GitHub-Quelle synchronisieren; Windows-EXE nur nach echtem Bauen und Praxistest als Testrelease anbieten. Geheimnisse, Admin-Tor, Spielstaende und `archiv/` privat halten. `https://github.com/Decay03101991/Nebelseetal-Remake`.

**Hardwarehinweise:** Windows 11 Home x64, ca. 12 GB RAM. Die lokale, funktionierende Windows-Python-Installation wurde als Astral/uv CPython 3.11.16 mit Tkinter identifiziert. Python 3.14.4 in WSL/Ubuntu ist **kein** Windows-EXE-Builder. Builds und grosse Tests am Nutzerrechner seriell ausfuehren. Keine personenbezogenen Identifikatoren protokollieren.

---

**28.10.2026 / konsolidierter Arbeitsstand aus letzter GPT-FIX01-Kopie. Auftrag des Nutzers: aktive Ordnerstruktur jetzt bereinigen, historische Entwicklung erhalten, nur ein Protokoll.**

## Geltungsbereich

Dieses Paket ist eine **eigenstaendige neue Arbeitskopie**. Originaldateien auf Daniels Windows-PC, dortige Git-Historie und GitHub wurden durch diese Arbeit **nicht veraendert**. Nutzer hat Bereinigung „wie Hermes“ beauftragt; Hermes bleibt fuer die spaetere Uebernahme, Tests und Remote-Verwaltung verantwortlich. Neuester realer Windows-/Git-HEAD war hier nicht lesbar, Basis ist die am 28.10.2026 uebermittelte Projektkopie und die bereits gepruefte GPT-Testfassung inklusive FIX01.

## Reihenfolge bei Wiederaufnahme

1. `START_HIER.txt`, `docs/AKTUELLER_STAND.md` und `docs/ENTWICKLUNGSPROTOKOLL.md` lesen.
2. `docs/AGENTEN_PLAN.md` mit Hermes eigener, aktueller Roadmap und Git-HEAD abgleichen.
3. Dateiumzuege aus `archiv/manifeste/ORDNER_UMZUGSPLAN.json` verfolgen; aktive Pfade `src`, `assets`, `data`, `tests`, `tools` erhalten.
4. **Wichtig:** vorherige Hermes-Fassung unter `archiv/altstaende/` als Vergleich; Archive duerfen nicht ins aktive `src` kopiert werden. Voller Originalstand inklusive Git bleibt weiterhin auf Daniels Rechner und im bisherigen Git.
5. Tests/Baupruefung auf Windows und End-to-End-Rundlauf ausfuehren. FIX01 hatte nur selektierte Erfolge; bekannte Fehler bleiben.
6. Erst nach Vergleich/Tests die konsolidierte Hauptfassung uebernehmen und auf GitHub aktualisieren. Bei Konflikt oder Geheimnisfund STOPP statt Force-Push.

## Aufraeumarbeiten in diesem Paket

- **Ein aktuelles Protokoll**: `docs/ENTWICKLUNGSPROTOKOLL.md` (bisherige Historie angehaengt, nicht ersetzt).
- 5 alte 00_START_HERMES-Varianten und alle parallel benannten GPT-Entwicklungsprotokolle sowie alte Projektstatusfassungen unter `archiv/`.
- Alte Analysen/Preview-Bilder/Screenshots/Quarantaene und historische Dokumente unter `archiv/` gegliedert.
- Icon-Quellblaetter und Originaltitel-/Symbolbilder geordnet nach `assets/quellbilder/`. Werkzeug- und Testpfade an neue Standorte angepasst.
- `tests/vorlagen/` statt loser Root-Vorlagen. Windows-Starter arbeiten weiterhin vom relativen Projektverzeichnis.
- `docs/BAUMENUE_ABGLEICH.md` analysiert Original-Screenshot und konkrete GUI-Aufgaben; keine neue GUI als erledigt behaupten.
- Bildinventar unter `docs/BILDINVENTAR.md`, volle Liste/Pruefsummen unter `archiv/manifeste/`. Kein ungeprueftes Loeschen von Bildern.

## GitHub ist Hermes' laufende Verantwortung

https://github.com/Decay03101991/Nebelseetal-Remake (`main`). Daniel hat oeffentliche Besucheransicht eingerichtet. Hermes soll fortan **nach jeder freigegebenen Aenderung** selbst lokal Git abgleichen, vertrauliche Dateien inkl. alten Commits verhindern, `README.md`, aktuelle Spielbereiche, Entwicklungschronik und Issues pflegen, Tests ausfuehren, committen/pushen und den Remote-Stand verifizieren.

**Kein Passwort in GitHub.** Jeder Spieler waehlt beim ersten Start ein eigenes lokales Passwort. Passwortpruefwerte, `tor.json`, `.env`, Tokens, Spielstaende bleiben privat. Oeffentlicher Python-Code ist nicht durch das Startpasswort geschuetzt. Originalgrafiken/-dokumente auf Publikationsrechte pruefen. `archiv/` nicht pushen (auch weil Altstaende oder persoenliche Quellen enthalten sein koennen).

## Offene Prioritaeten

- Bestehende fehlgeschlagene Wirtschafts-/Gebaeude-/Handels-/GUI-Tests beheben und Vollsuite erneut ausfuehren.
- Bot-Wirtschaft/Belagerungsstrategie fertigstellen, 25 Originalraster pruefen, vollstaendiger E2E.
- Original-Baumenue nach vorhandener Screenshotreferenz nutzbar integrieren (keine losgeloeste Bildkopie).
- Windows-EXE/GUI/Ressourcen/Persistenz unabhaengig pruefen, erst dann Release.
- Alle Erkenntnisse mit Testnachweis und genauen Pfaden **nur** in das zentrale Protokoll schreiben.

## Aufraeumprotokoll

Siehe Abschnitt **GPT-KONSOLIDIERUNG-01** am Ende von `docs/ENTWICKLUNGSPROTOKOLL.md` und die maschinenlesbaren Umzugsprotokolle unter `archiv/manifeste/`.

## Erweiterte Dokumenten- und Windows-Build-Aufgaben (28.10.2026)

- Nutzer fordert vollstaendige Projektordnung und einen aus dem neuesten **aktivem** Spielstand gebauten Windows-EXE, der direkt im aktiven Hauptordner liegt. In der Linux-Arbeitsumgebung war diese EXE nicht erzeugbar. **Hermes muss den Windows-Build ausfuehren und mit Praxis- und Rauchtests freigeben**. Keinesfalls die alte EXE aus dem Baseline-Archiv als neue verwenden. Einstieg: `EXE_NEUESTEN_STAND_BAUEN.bat`, `docs/WINDOWS_EXE_HERSTELLUNG.md`. Optionaler manueller Windows-CI-Build: `.github/workflows/windows-test-exe.yml` (nicht automatisch publizieren).
- Alle vorhandenen textbasierten Dokumente wurden technisch eingelesen, in `archiv/manifeste/DOKUMENTE_VOLLINVENTAR.json` indexiert und in `docs/QUELLEN_UND_DOKUMENTE.md` eingeordnet. Unterschied: automatische Textextraktion ist **nicht** gleich inhaltliche Abnahme aller historischen Quellen; alle Zweifel offenlegen.
- Eine falsch benannte `.odt`-Datei erwies sich als bytegleiche PDF-Duplikatkopie und liegt jetzt im Archiv. Im Original-PDF mit Dateinamen `...2009.pdf` steht der historische Stand **01.09.2006**. Keine stillschweigende Quellenkorrektur von Zahlen ableiten.
- Hermes soll weiterhin **genau ein** aktives Entwicklungsprotokoll weiterfuehren; dieses Dokument bleibt die einzige aktuelle Uebergabe. Alle alten Texte im Archiv bewahren, nicht in aktiven Status zurueckkopieren.
- Beim echten Windows-Hauptprojekt nach Neustart erst Differenzen zu Hermes' Git-HEAD, externe Bauten und aktuelle Spielstaende pruefen. Die hier archivierte Baseline ist *nicht* zwingend der aktuellste Stand.


## AKTUELLSTE ERGAENZUNG – NUR ORIGINALKARTEN (28.10.2026)

**Diese Sektion hat Vorrang** vor älteren Hinweisen auf 8×7, Zufalls-/Kartentyp-Generatoren, Geländesymbole und Kartenanzahl. Daniel hat ausdrücklich entschieden: **Es dürfen zukünftig nur die neu hinzugefügten 127 Originalkarten verwendet werden.** Nicht aus dem Gedächtnis zusammengestellte Ersatzkarten; keine Wiederverwendung in Bot-Logik, Wirtschaft, GUI oder Spielständen.

**Neue Pfade und Auswirkung:**

1. Original-Bildquellen: `assets/karten/original/{beste,mittlere,schlechte}/` (**unverändert**, Hash geprüft).
2. Laufzeit-Grafik: `assets/karten/spielfeld/original-*.png`, 127 PNG 640×640 NEAREST aus authentischen Quellen; `data/originalkarten/grafik_manifest.json` verbindet alle IDs und SHA-256-Prüfsummen.
3. Kartendaten: `data/originalkarten/katalog.json`; Runtime-Zuordnung: `src/originalkarten.py` plus **neu** `src/originalkarten_grafik.py`.
4. GUI `src/main.py::_zeichne_siedlungskarte` zieht den authentischen Originalhintergrund; die Gebäude, Wege, Wälle, Pips, Auswahlrahmen, Koordinaten kommen weiterhin als Overlays darüber. `karten_optik_fein.gelaende_plan_fein` wird für die Siedlungsgrafik **nicht** mehr aufgerufen; kein Fantasiegelände-Fallback.
5. `src/gelaende.py::siedlungskarte_erzeugen` liefert nur noch originalbasierte Karte ohne alte `typ_id`-/`mass`-Parameter; `src/spieloekonomie.py::feste_karte` lehnt alte 8×7-Generierung ausdrücklich ab. Die alten Kartentyp- und Maß-Einträge wurden aus `data/gelaende.json` entfernt, Regeln anderer Systeme blieben erhalten. Alte Quellen liegen unter `archiv/legacy_karten_8x7/`.
6. Der `GameState.load`-Weg lehnt vorhandene 8×7-/ID-lose Siedlungskarten und Kartenvorräte vor Mutation ab, damit keine alten Karten aktiv werden. Historische Savegames NICHT löschen, nicht automatisch migrieren. Der alte separate `savegame.json`-Ladeknopf wurde deaktiviert.
7. Ältere kartenabhängige Tests wurden unter `archiv/tests_legacy_8x7/` verwahrt. Sie wurden **nicht** repariert und zählen NICHT zur grünen aktiven Testabdeckung. Der neue `tests/test_originalkarten_only.py` prüft die 127 IDs, Hashes, 10×10, Grafik und Tk-Öffnung; am 28.10.2026 **7/7 grün** unter virtueller Linux-Grafik. `test_gpt_wallsystem_eingehaengt.py` nutzt jetzt eine echte 10×10-Fixture und bestand 9/9.
8. Testbefund `test_startspiel.py`: 45 Einzelkontrollen bestanden, **5 Fehler**, 1 Befund. Weitere vollständige Windows-/GUI-Prüfung offen. 25 Kartenraster sind anhand der Originalbilder noch manuell zu kontrollieren. Keine vollständige Abnahme behaupten.
9. Reproduktionswerkzeug `tools/originalkarten_grafiken_bauen.py` (Pillow nur für Build, nicht fürs Spiel). Windows-EXE-Build enthält alle `assets/` und `data/`. **Windows-EXE weiterhin nicht vorhanden**; alter EXE-Build ausdrücklich nicht aktuell.
10. **Lern-/Skill-/Regelübernahme:** `docs/HERMES_KONTROLLE_UND_SKILLS.md` lesen. **Alt→Neu-Manifest:** `archiv/manifeste/ORIGINALKARTEN_UMSTELLUNG_20261028.json` plus `ORDNER_UMZUGSPLAN.json`.

Hermes bleibt Head-Koordinator, ChatGPT ist zeitweise Coding-Agent. Bei Rückübernahme prüft Hermes seine Skills, die reale lokale Git-Historie, die offenen Tests und die Sicherheitsprüfung. GitHub nur nach freigegebener Integration aktualisieren.

**Zusaetzlicher Speichertest (28.10.2026):** `tests/test_originalkarten_savegames.py` ist mit 2/2 gruen: eine neue echte Originalkarte uebersteht Save/Load und eine alte 8x7-Karte wird vor Zustandsschaeden abgewiesen.


## GPT-FIX02 – aktuellste Coding-Arbeit (28.10.2026)

**DIESEN ABSCHNITT VOR ALTER TESTSTATISTIK LESEN.** ChatGPT arbeitet voruebergehend am konsolidierten Spiel; Hermes bleibt Head-Koordinator, Lerndokumentation/Skill-Regeln und spaetere Integration liegen bei Hermes. **Kein GitHub-Push vor Abschluss der weiteren Fehlerarbeit** (ausdrueckliche neueste Nutzerentscheidung).

- `src/main.py::_zeichne_siedlungskarte`: die echten 127 Originalgrafiken bleiben. Weil der Hintergrund ein Bild ist, hatten nur bebaute oder selektierte Felder ein `feld:i`-Canvas-Tag; 100 transparente `kartenfeld`-Regionsobjekte loesen dies, ohne Bilder/Gelaende zu veraendern.
- `tests/test_startspiel.py`: echte Nahrungsknappheit/Grundrate und regulare Baukunst-Forschungs-/Ausbildungsfolge, **61 bestanden / 0 Fehler / 1 Befund**.
- `tests/test_durchspiel.py`: echtes 10x10 und Forschung vor Akademie/Schmiede; lokale und reichsweite Anzeige sauber getrennt, Werkstatt-Vorschlagsdauer und korrekte Fertigstellung, **64/0/2**.
- `tests/test_gpt_wall_gui.py`: Originalkarten statt kuenstlichem 8x7-Raster, **4/4**.
- `tests/test_gpt_originalkarten_feldklick.py`: neu, 100 Tag-Regionen und sechs echte Klickpositionen, **2/2**.
- **24 selektierte Testdateien nach Fix bestanden.** `test_gui_fehler.py` hing anfangs an der menschlichen Abrissbestaetigung/alten Slot- und Wallannahmen; als isolierter, nichtinteraktiver Regressionstest korrigiert, danach **23/0/1** bei 18 Ansichten und 13 Aktionen, inklusive absichtlicher Callback-Fehlerfalle. Die Vollsuite, 25 Kartendatenraster, Windows-EXE und Bot-Wirtschaft bleiben offen.
- Vor Integration Aenderungsmanifest `archiv/manifeste/GPT_FIX02_AENDERUNGEN.json` pruefen. Bei gleichen Spielcodezeilen Konflikte manuell in Hermes-HEAD aufloesen; nur eine aktive Entwicklungschronik bleibt `docs/ENTWICKLUNGSPROTOKOLL.md`.
- Next: alten Kartenansichtstest mit den fehlenden 11 Kontrollen auf echte Originalkarten/Ortskassen umstellen; dann volle Testbatterie und Windows-Build. `run_tests.bat` listet den neuen Feldklicktest, Windows-Aufruf bleibt ungeprueft. Keine Tests alleine durch Archivierung als behoben darstellen.


## Nachtrag GPT-FIX02b – aktive Bau-/Ortskassen-Regressionsprüfung

Im aktiven `tests/test_gpt_originalkarten_baukasse.py` sind vier reale Tkinter-Tests hinzugekommen. **4/4 grün**, damit 25 gezielt ausgewählte Testdateien grün; die komplette Testsuite bleibt offen. Der Test verwendet ausschließlich eine reguläre 10×10-Originalkarte, belastet nur das lokale Ortslager und verifiziert die daraus abgeleitete Reichsanzeige. Prüft auch Doppelbau und fehlende Ressourcen ohne Zustandsveränderung sowie Originalkarten-Grafik nach Bau. `run_tests.bat` wurde ergänzt. Code der eigentlichen Wirtschaft wurde dabei **nicht** umgeschrieben.

Hermes soll daraus die Skills *Bauaktionen atomar testen*, *Ortslager als eine Quelle*, *historische Prüfannahmen explizit archivieren statt unsichtbar entfernen* und *GUI-Karte auch nach Mutation testen* mit eigenen bestehenden Regeln abgleichen; keine doppelten Skills anlegen. Der noch alte `archiv/tests_legacy_8x7/test_kartenansicht.py` mit elf Fehlkontrollen bleibt als Vergleich und für noch nicht portierte UI-Anforderungen erhalten. Alle Änderungen einschließlich Alt→Neu-Pfaden stehen im zentralen `docs/ENTWICKLUNGSPROTOKOLL.md` und Manifest `archiv/manifeste/GPT_FIX02_AENDERUNGEN.json`. Ein aktualisierter Remote-Push erfolgt nach Daniels letzter Entscheidung **erst am Ende**.


## LATEST – GPT-FIX02c, Paketprüfung & GitHub-Nächster Schritt (28.10.2026)

- Daniel hat alle sieben FIX02-Teil-ZIPs in seinen neuen Hauptordner entpackt. ZIP-Upload `Nebelseetal_Remake(2).zip`: alle 1.229 Projektdateien nach SHA-256 identisch, null fehlende; ZIP-CRC gut. `.git` enthalten (lokaler historischer Head `1c4dffa`, ohne Remote `origin`); **nicht** als GitHub-Clone behandeln. Der als Backup erwähnte Ordner `Alles alte` ist nicht Teil der geprüften ZIP – Aufbewahrung vor Ort separat bestätigen.
- In einer **isolierten GPT-Auditkopie** wurden Pfade der alten Protokoll-/Zielübergabe-Tests auf aktuelle `docs/` bzw. historische `archiv/` korrigiert. Detaillierter Teststand und Pfade stehen im zentralen `docs/ENTWICKLUNGSPROTOKOLL.md`, Abschnitt GPT-FIX02c. Zuvor laufende zehn zentrale Spieltests grün; Gesamt- und Windows-Prüfung weiterhin offen.
- **Neue Nutzerentscheidung:** Nach Prüfung soll die konsolidierte Fassung auf das bestehende öffentliche Repository `Decay03101991/Nebelseetal-Remake`, vorzugsweise mit aktueller Windows-EXE. Vorbereiten ja; Push erst nach Kontrolle von Änderungen, Rechten, Geheimnissen und Codehistorie. Die `.github/workflows/windows-test-exe.yml` kann auf GitHub manuell den Windows-EXE-Artefaktbau ausführen; Artefakt ist **nicht** automatisch ein freigegebener Release. Erst reale Windows-GUI-, Passwort-, Karten-, Lager- und Speichertests; anschließend als Pre-Release bereitstellen. Hermes pflegt später GitHub selbständig mit Freigaben und sauberem Protokoll.
- **Erste Wiederaufnahme für Hermes:** `docs/HERMES_UEBERGABE_AKTUELL.md`, `docs/AKTUELLER_STAND.md`, `docs/HERMES_KONTROLLE_UND_SKILLS.md`, `docs/ENTWICKLUNGSPROTOKOLL.md`; die `archiv/`-Pfadmanifeste nur bei Bedarf. Keine Parallelagenten an gemeinsamen Code, Root/Repo und Windows-Build prüfen, Lernregeln aus verifizierten Regressionen ableiten.

**Nachweis der Pfadprüfung:** Nach Korrektur 16/0/1 (`tests/test_protokoll.py`) und 26/0/0 (`tests/test_zieluebergabe.py`) in isolierter Arbeitskopie. Der eine historische Befund betrifft 24 umformulierte Absatzanfänge, nicht vergessene Commitkennungen oder Prüfzahlen. Veröffentlichungspfad und offene Release-Hürden: `docs/GITHUB_VEROEFFENTLICHUNG_FIX02c.md`.

**Build-Prüfregel:** Windows-Bauvorprüfung in `tools/gpt_windows_vorpruefung.py` musste einen nicht existenten Originaltreue-Test gegen den vorhandenen Originalkarten-Katalogtest austauschen. Sechs ausgewählte Vorprüfdateien unter Linux/Xvfb grün; Windows bleibt ausstehend. Zusätzlich sind drei noch fehlende Referenzen in `tools/gpt_abschluss_tests.py` offen. Keine automatische Releasefreigabe aus grünen Vorprüfungen ableiten.


## GPT-FIX02d-R2 - Verbindliche aktuelle Einstiegskonvention (28.10.2026)

**Vorrang vor allen aelteren Start-Hier-Hinweisen:** Es gibt **keine aktive `START_HIER.txt`**. Fuer Spieler, technische Nutzer und GitHub gilt `README.md` (enthaelt jetzt Python-Spielstart, Passwort beim Erststart, aktuelle EXE-Bauanleitung und Testhinweise). Fuer dich, Hermes, gilt **dieses Dokument** als einziger Wiedereinstieg. Die einzige aktive Chronik ist `docs/ENTWICKLUNGSPROTOKOLL.md`, der kompakte Ist-Stand ist `docs/AKTUELLER_STAND.md`. Bestehende Roadmap und Skills bleiben bestehen. Historische Anleitungen, Statusfassungen und doppelte .bat-Wrapper liegen mit Alt->Neu-Pfaden und SHA-256 unter `archiv/ordnungsbereinigung_FIX02d_20261028/DATEIUMZUEGE.json`.

**Beim Wiederanlauf:** (1) Diese Uebergabe und `docs/AKTUELLER_STAND.md`, dann das zentrale Protokoll lesen; keine historische Anleitung als aktive Anweisung behandeln. (2) Den lokalen Git-HEAD mit dieser Arbeitskopie und dem GitHub-Remote vergleichen; `Alles alte` bleibt privat und unangetastet. (3) Den bestehenden Laptop-Cleanup-Cronjob und vorhandene Projektordnungs-Skills erst auslesen und sichern; eine **lesende** Pruefung fuer doppelte Einstiege, tote Links und zusammenfassbare Dokumente ergaenzen, NICHT einen neuen Job anlegen. (4) Aenderungen fuer Daniel **proaktiv vorschlagen**: Pfad, Quelle, SHA-256, Abhaengigkeiten, Testauswirkung, Rueckweg. Keine automatische Loeschung oder Verschiebung aktiver Dateien durch Cleanup. (5) Nach Freigabe ordnungsgemaess archivieren, Code-/Test-/Buildreferenzen pruefen, das EINZIGE Protokoll ergaenzen und aus bestaetigten Ursachen neue Skillregeln ableiten; keine doppelten Skills. (6) Aktuelle Windows-EXE ist noch nicht erstellt oder getestet; GitHub bleibt bis zur Freigabe unveraendert. Nach realem Windows-Test und Secret-/Rechtepruefung die neue GitHub-Version pflegen.

**Rollen:** ChatGPT ist voruebergehend Coding-Zuarbeit. Hermes bleibt alleiniger, uneingeschraenkter Head-Koordinator. Die lokale Cronjob-Integration ist **nur beauftragt**, nicht schon umgesetzt.


## GPT-FIX02d-R2 - Technische Windows-Umgebung und sichere Ausfuehrung

Bekannter Zielrechner: Windows 11 Home x64 (Build 26300), Intel 64-Bit-Prozessor ca. 2,3 GHz, 12 GB physischer Speicher; beim Nutzerbericht waren rund 3,1 GB davon frei. Das ist keine dauerhafte Verfuegbarkeitsgarantie. Vor groesseren Tests/EXE-Build Festplattenspeicher und freien RAM neu messen. **Keine parallelen Schwerlast-Builds**. Windows-EXE separat mit 64-Bit-Python und Tkinter erstellen, anschliessend reale GUI-/Save-/Originalkarten-Rauchtests. Den Build nicht automatisch nach GitHub pushen; erst manuelle Freigabe. Nutzeridentifikatoren, E-Mail, Produkt-IDs, IP-Adressen und BIOS-Serien nicht in Projektberichte schreiben.


## FIX04 – derzeit neueste isolierte Coding-Runde (28.10.2026)

**Unbedingt zuerst mit realem Git-HEAD vergleichen; nur Hermes gibt frei.** Neu sind `src/baumenue_info.py`, geaendert wurden `src/main.py` (Rubrikmenue/Anzeige der Voraussetzungen), `tests/test_startspiel.py` (robuste Originalnamen), `tests/test_gpt_baumenue_kategorien_fix04.py` (5/5 Tk-GUI), `run_tests.bat` (Windows-Python 3.11 Astral und neuer Test), `docs/AKTUELLER_STAND.md` sowie dieses Handoff und das **einzige** aktive `docs/ENTWICKLUNGSPROTOKOLL.md` (Abschnitt GPT-FIX04). Die genauen Inhalte und Risiken stehen dort. **Kein GitHub-Push oder neuer Windows-Build aus FIX04 durch ChatGPT.** Daniels FIX03-Windows-EXE startete nach eigener Rueckmeldung mit Admin-Zugang und funktionierendem Speichern/Laden; fuer FIX04 neu bauen und die Rubrikwahl in Produktion/Werkstatt/Ausbildung/Verteidigung/Sonstiges testen.

**Kompakter Hermes-Wiederaufnahmeweg auch fuer DeepSeek V4 Flash:** (1) Hauptordner und aktuelles Git-HEAD feststellen; `Alles alte`/`archiv` nicht als aktiv zaehlen. (2) Nur `docs/AKTUELLER_STAND.md`, diesen Abschnitt und Protokoll GPT-FIX04 lesen; Detailquellen erst bedarfsweise. (3) Aenderungsdateien und Tests diffen, echte Originalkarten und Bildhashes beibehalten. (4) Eigenen Lern-/Skill-Katalog auf den bestehenden Regelkern, GUI-Aktions- und Ortskassen-Regressionen pruefen; neue Regeln nur ohne Doppelungen in bestehende Skills und Cleanup-Cronjob einfuegen, Dokumente nicht automatisch loeschen. (5) Windows-Neubau aus FIX04, normaler Spielmodus, Admin, Baukunst-Sperre und drei Slots speichern/laden. (6) Nach vollstaendiger Test- und Sicherheitspruefung denselben GitHub-Remote aktualisieren, Release **nur** nach erfolgreichem Test. Die Rechte an historischen Bildern vor oeffentlichem Release gesondert klaeren.

**Pfadregel:** `README.md` = Spieler/GitHub, `docs/AKTUELLER_STAND.md` = Spielbereiche, `docs/HERMES_UEBERGABE_AKTUELL.md` = einzige aktive Hermes-Uebergabe, `docs/ENTWICKLUNGSPROTOKOLL.md` = einziges aktives Protokoll. **`START_HIER.txt` ist historisch und gehört ins Archiv**, nicht zur aktuellen Lesereihenfolge. Alles unter `archiv` nur Referenz, nichts ungeprueft erneut in den Spielkern kopieren.
